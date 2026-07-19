"""Phase 41 / CTRL-01+05+08 — ``python -m pinn.train`` composition root.

Wires: keyed YAML config → freeze → resolve_runtime / strict-CPU override →
build_network (seed fan-out) → CheckpointStore + StepGuards → RunController
hooks → CurriculumController.run().

Minimal-but-runnable Option A driver. Dataset-free synthetic Stage-0 sources
are used when no data path is wired (v2.0 falsifiability floor). Canonical
logging schema + operator ergonomics stay Phase 42.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import build_network
from pinn.runtime import RuntimeSpec, resolve_runtime
from pinn.training import determinism
from pinn.training.checkpoint import (
    CHECKPOINT_SCHEMA_VERSION,
    TorchSaveCheckpointStore,
)
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import TrainingConfig
from pinn.training.config_yaml import freeze_resolved_config, load_config
from pinn.training.controllers import (
    CurriculumController,
    RunController,
    build_checkpoint_payload,
)
from pinn.training.grad_clip import GradClipper
from pinn.training.guards import StepGuards, write_failure_bundle
from pinn.training.resume import (
    RESUME_FIELD_REGISTRY,
    HoldStageTargetError,
    IdentityCoverageError,
    ResumeConfigRefused,
    RunFolderExistsError,
    build_config_identity_envelope,
    build_identity_payload,
    identity_coverage_check,
    load_resume_target,
    resume_config_diff,
    validate_hold_stage_target,
)
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine

# Overridable for tests (inject synthetic sources / alternate runs root).
_RUNS_ROOT: Path = Path("runs")
_SOURCE_FACTORY: Optional[Callable[[TrainingConfig], tuple[Any, Any]]] = None
_HAS_DATASET: bool = False  # v2.0 wires no real data source


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m pinn.train")
    parser.add_argument("--config", required=True, help="path to keyed YAML config")
    parser.add_argument(
        "--resume",
        default=None,
        help="checkpoint file, run directory, or 'latest'",
    )
    parser.add_argument(
        "--hold-stage",
        action="store_true",
        dest="hold_stage",
        help="with --resume <stage-k-final.pt>, re-enter stage k instead of advancing",
    )
    return parser


def _derive_run_name(config: TrainingConfig) -> str:
    if config.run.run_name:
        return str(config.run.run_name)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"run-{stamp}-seed{int(config.run.seed)}"


def _resolve_run_dir(name: str, runs_root: Path) -> Path:
    """Join runs/<name>/ and reject path-traversal escapes (cycle-2 codex MEDIUM)."""
    runs_root = runs_root.resolve()
    run_dir = (runs_root / name).resolve()
    try:
        if not run_dir.is_relative_to(runs_root):
            raise ValueError(
                f"run_name escapes runs/ root: {name!r} → {run_dir}"
            )
    except AttributeError:
        try:
            run_dir.relative_to(runs_root)
        except ValueError as exc:
            raise ValueError(
                f"run_name escapes runs/ root: {name!r} → {run_dir}"
            ) from exc
    return run_dir


def _synthetic_split_sources(
    *, n_train: int = 240, n_validation: int = 240
) -> tuple[Any, Any]:
    """Dataset-free StageQuery-shaped sources (v2.0 falsifiability floor).

    Defaults meet the Stage-0 population floor (240) enforced by
    ``build_stage_batch`` for BOTH train and validation splits.
    """
    # Local import keeps train import light; mirrors phase40 stub shape without
    # importing the tests package.
    from types import SimpleNamespace

    from pinn.data.types import RecordKey, StageLabel

    class _StubSource:
        def __init__(self, stage0_ids):
            self._s0 = [RecordKey("hierarchical", "base", i) for i in stage0_ids]
            self._black = set()

        @property
        def blacklisted_physical_keys(self):
            return frozenset()

        def has_stage(self, k):
            return k == 0 and bool(self._s0)

        def records_at(self, k):
            return tuple(self._s0 if k == 0 else ())

        def records_at_or_below(self, k):
            return tuple(self._s0 if k >= 0 else ())

        def record_keys(self):
            return tuple(self._s0)

        def get(self, key):
            return SimpleNamespace(
                record_key=key,
                physical_key=key.physical_key,
                stage_label=StageLabel.STAGE_0,
                n_snapshots=self.n_snapshots(key),
                ic13=np.linspace(0.0, 1.2, 13, dtype=np.float64) + key.id / 10000.0,
                masses=np.array(
                    [1.0 + key.id / 10000.0, 2.0, 3.0], dtype=np.float64
                ),
            )

        def n_snapshots(self, key):
            return 32

        def snapshot_times(self, key):
            return np.linspace(0.0, 9.5, self.n_snapshots(key), dtype=np.float64)

        def snapshot_positions(self, key):
            times = self.snapshot_times(key)
            positions = np.zeros((len(times), 3, 3), dtype=np.float64)
            positions[:, 0, 0] = times + key.id / 1000.0
            positions[:, 1, 1] = 2.0 * times
            positions[:, 2, 2] = -times
            return positions

        def snapshot_velocities(self, key):
            times = self.snapshot_times(key)
            velocities = np.zeros((len(times), 3, 3), dtype=np.float64)
            velocities[:, 0, 0] = times ** 2
            velocities[:, 1, 1] = times
            return velocities

        def acceleration_magnitudes(self, key):
            return np.arange(1, self.n_snapshots(key) + 1, dtype=np.float64)

        def stage_label(self, key):
            return StageLabel.STAGE_0

        def is_blacklisted(self, physical_key):
            return False

        @property
        def gold_numeric_stage_count(self):
            return 0

    train = _StubSource(tuple(range(n_train)))
    val = _StubSource(tuple(range(10_000, 10_000 + n_validation)))
    return train, val


def _build_sources(config: TrainingConfig) -> tuple[Any, Any]:
    if _SOURCE_FACTORY is not None:
        return _SOURCE_FACTORY(config)
    return _synthetic_split_sources()


def _resolve_runtime_spec(config: TrainingConfig) -> RuntimeSpec:
    """HIGH 4: strict-CPU returns forced float64/cpu RuntimeSpec."""
    if config.run.strict_cpu_determinism:
        # apply_strict_cpu_determinism BEFORE any build_network call; its
        # returned RuntimeSpec is what build_network consumes (not
        # resolve_runtime of config.run.precision/device).
        return determinism.apply_strict_cpu_determinism(int(config.run.seed))
    return resolve_runtime(config.run.precision, config.run.device)


def _derive_resume_plan(
    payload: Mapping[str, Any],
    *,
    hold_stage: bool,
    resume_arg: str,
) -> tuple[int, Optional[dict[str, Any]]]:
    """Return (initial_stage, resume_ctx) from a loaded checkpoint payload."""
    curriculum = payload.get("curriculum") or {}
    stage = int(curriculum.get("stage", 0) or 0)
    phase = curriculum.get("phase")
    epoch = int(curriculum.get("epoch", 0) or 0)
    basename = Path(str(resume_arg)).name

    is_stage_final = bool(
        basename.startswith("stage-") and basename.endswith("-final.pt")
    )
    if hold_stage and is_stage_final:
        # Re-enter stage k from its final boundary (start of stage, no mid-epoch).
        return stage, None
    if is_stage_final and not hold_stage:
        # Advance past the completed stage.
        return stage + 1, None
    # Mid-stage rolling (or other non-final): re-enter with epoch context.
    ctx: Optional[dict[str, Any]] = None
    if phase in ("2a", "2b"):
        ctx = {"phase": phase, "epoch": epoch}
    return stage, ctx


def _restore_run_controller(controller: RunController, payload: Mapping[str, Any]) -> None:
    """Restore model/optimizer/rng/counters from a CTX-53 or nested payload."""
    if "run_controller" in payload and isinstance(payload["run_controller"], Mapping):
        controller.load_state_dict(payload["run_controller"])
        return
    # Flat CTX-53 envelope.
    if "model" in payload:
        controller.load_state_dict(dict(payload))


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry — returns process exit code (0 success, non-zero refuse/error)."""
    args = _parser().parse_args(list(argv) if argv is not None else None)

    # ---- Fail-closed CLI validation BEFORE construction ----
    if args.resume is not None and args.resume != "latest":
        resume_path = Path(args.resume)
        if not resume_path.exists():
            print(
                f"error: --resume path does not exist: {args.resume}",
                file=sys.stderr,
            )
            return 1

    if args.hold_stage:
        if args.resume is None:
            print(
                "error: --hold-stage requires --resume <stage-{{N}}-final.pt>",
                file=sys.stderr,
            )
            return 1
        try:
            validate_hold_stage_target(args.resume)
        except HoldStageTargetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    try:
        config = load_config(args.config)
    except Exception as exc:
        print(f"error: failed to load config: {exc}", file=sys.stderr)
        return 1

    # Run-folder name + path-traversal + collision check.
    try:
        run_name = _derive_run_name(config)
        runs_root = Path(_RUNS_ROOT)
        run_dir = _resolve_run_dir(run_name, runs_root)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    is_resume = args.resume is not None
    if run_dir.exists() and not is_resume:
        err = RunFolderExistsError(run_dir)
        print(f"error: {err}", file=sys.stderr)
        return 1

    run_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir = run_dir / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # Freeze resolved config (CTRL-01 / CTX-51). On resume, rewrite only when
    # the frozen file is absent so we do not thrash an existing freeze.
    frozen_path = run_dir / "config.yaml"
    if not frozen_path.is_file():
        freeze_resolved_config(config, run_dir)
    else:
        # Fresh launch always freezes; resume reuses existing freeze unless missing.
        if not is_resume:
            freeze_resolved_config(config, run_dir)

    # Strict-CPU override (HIGH 4) — single runtime_spec for the whole run.
    try:
        runtime_spec = _resolve_runtime_spec(config)
    except Exception as exc:
        print(f"error: runtime resolve failed: {exc}", file=sys.stderr)
        return 1

    # Run-start RNG record (CTRL-08, GAP-41-01 representation B): the four
    # streams land in runs/<name>/run_start_rng.pt beside the frozen config.
    # Recorded AFTER runtime resolve (so a strict-CPU reseed is reflected) on
    # the same generator RunController consumes. Fresh launch only — resume
    # must never overwrite the original run-start record.
    run_rng = np.random.default_rng(int(config.run.seed))
    if not is_resume:
        determinism.record_run_start_rng(run_dir, run_rng)

    # Seed fan-out: ArchitectureSpec.seed = config.run.seed (RESEARCH OQ1).
    arch_spec = ArchitectureSpec(seed=int(config.run.seed))

    # Identity payload + coverage check (cycle-2 MEDIUM + cycle-4 MEDIUM-3).
    identity_fields = build_identity_payload(
        config, arch_spec, effective_runtime_spec=runtime_spec
    )
    try:
        identity_coverage_check(
            RESUME_FIELD_REGISTRY,
            identity_fields,
            has_dataset=_HAS_DATASET,
        )
    except IdentityCoverageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    config_identity = build_config_identity_envelope(
        config, arch_spec, effective_runtime_spec=runtime_spec
    )

    # Network build against the (possibly forced) runtime_spec.
    model = build_network(
        arch_spec,
        dtype=runtime_spec.dtype,
        device=runtime_spec.torch_device,
    )

    train_source, validation_source = _build_sources(config)

    store = TorchSaveCheckpointStore(ckpt_dir, config=config)
    step_guards = StepGuards(config, disk_root=run_dir)

    scheduled_weights = ScheduledWeights(
        int(config.stage.n_adam),  # type: ignore[arg-type]
        lambda_e_max=float(config.loss.lambda_e_max),
    )
    grad_clipper = GradClipper()
    collocation_sampler = CollocationSampler(
        collocation_count=16,
        rng=np.random.default_rng(int(config.run.seed)),
    )
    stage_exit_machine = StageExitMachine(config)

    # Curriculum is constructed after run_controller so the accessor closes over it.
    curriculum_holder: dict[str, Any] = {"curriculum": None}

    def curriculum_state_accessor() -> dict[str, Any]:
        cur = curriculum_holder["curriculum"]
        rc = curriculum_holder.get("run_controller")
        stage = int(getattr(cur, "stage", 0) if cur is not None else 0)
        phase = getattr(rc, "_active_phase", None) if rc is not None else None
        epoch = int(getattr(rc, "_active_epoch", 0) if rc is not None else 0)
        step = int(getattr(rc, "_global_step", 0) if rc is not None else 0)
        return {
            "stage": stage,
            "phase": phase,
            "epoch": epoch,
            "step": step,
            "disposition_log_pointer": None,
        }

    best_val_cell: dict[str, float] = {"best": float("inf")}

    def checkpoint_hook(controller: RunController, global_step: int) -> None:
        elapsed = float(store._clock()) - float(store.last_written_time)
        if store.should_checkpoint(int(global_step), elapsed):
            payload = build_checkpoint_payload(
                controller,
                curriculum_state_accessor(),
                config_identity,
                CHECKPOINT_SCHEMA_VERSION,
            )
            store.save_rolling(payload, int(global_step))
        # best.pt producer (cycle-4 MEDIUM-1)
        val = getattr(controller, "_last_val_total", None)
        if val is not None and float(val) < best_val_cell["best"]:
            best_val_cell["best"] = float(val)
            payload = build_checkpoint_payload(
                controller,
                curriculum_state_accessor(),
                config_identity,
                CHECKPOINT_SCHEMA_VERSION,
            )
            store.save_best(payload)

    def guard_hook(
        controller: RunController,
        loss_terms: Any,
        grad_norm: Any,
        global_step: int,
        stage: int,
        phase: str,
    ) -> Any:
        # Coerce loss_terms to a mapping of scalars for StepGuards.
        terms_map: Optional[Mapping[str, Any]] = None
        if loss_terms is not None:
            if isinstance(loss_terms, Mapping):
                terms_map = loss_terms
            else:
                terms_map = {}
                for key in ("total", "data", "phys", "ic", "energy", "angmom"):
                    if hasattr(loss_terms, key):
                        try:
                            terms_map[key] = float(getattr(loss_terms, key).detach())
                        except Exception:
                            try:
                                terms_map[key] = float(getattr(loss_terms, key))
                            except Exception:
                                pass
        outcome = step_guards.check(
            int(global_step),
            int(stage),
            str(phase),
            loss_terms=terms_map,
            grad_norm=grad_norm,
            disk_root=run_dir,
        )
        if outcome is not None and outcome.disposition is not None:
            try:
                write_failure_bundle(
                    run_dir,
                    outcome,
                    config_yaml_path=run_dir / "config.yaml",
                )
            except Exception as exc:
                print(f"warning: failure bundle write failed: {exc}", file=sys.stderr)
            try:
                payload = build_checkpoint_payload(
                    controller,
                    curriculum_state_accessor(),
                    config_identity,
                    CHECKPOINT_SCHEMA_VERSION,
                )
                store.save_anchor(
                    tag=f"failure-stage-{int(stage)}-step-{int(global_step)}",
                    stage=int(stage),
                    payload=payload,
                )
            except Exception as exc:
                print(f"warning: failure checkpoint write failed: {exc}", file=sys.stderr)
        return outcome

    run_controller = RunController(
        model=model,
        train_source=train_source,
        validation_source=validation_source,
        config=config,
        scheduled_weights=scheduled_weights,
        grad_clipper=grad_clipper,
        collocation_sampler=collocation_sampler,
        stage_exit_machine=stage_exit_machine,
        checkpoint_store=store,
        runtime=runtime_spec,
        rng=run_rng,
        checkpoint_hook=checkpoint_hook,
        guard_hook=guard_hook,
    )
    curriculum_holder["run_controller"] = run_controller

    initial_stage = 0
    resume_ctx: Optional[dict[str, Any]] = None
    from_resume = False

    if is_resume:
        from_resume = True
        try:
            payload = load_resume_target(store, args.resume)
        except Exception as exc:
            print(f"error: failed to load resume target: {exc}", file=sys.stderr)
            return 1

        ckpt_identity = payload.get("config_identity")
        if ckpt_identity is None and isinstance(payload.get("run_controller"), Mapping):
            # Nested Phase-40 payload — no identity; refuse fail-closed if missing.
            ckpt_identity = {}
        try:
            resume_config_diff(
                config,
                arch_spec,
                ckpt_identity if isinstance(ckpt_identity, Mapping) else {},
                effective_runtime_spec=runtime_spec,
            )
        except ResumeConfigRefused as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

        _restore_run_controller(run_controller, payload)
        initial_stage, resume_ctx = _derive_resume_plan(
            payload, hold_stage=bool(args.hold_stage), resume_arg=str(args.resume)
        )

    curriculum = CurriculumController(
        config=config,
        checkpoint_store=store,
        scheduled_weights=scheduled_weights,
        run_controller=run_controller,
        initial_stage=initial_stage,
    )
    # Stash frozen config identity for CurriculumController boundary anchors.
    curriculum._config_identity_payload = config_identity  # type: ignore[attr-defined]
    curriculum_holder["curriculum"] = curriculum

    # Reproducibility honesty (CTX-64) — never bitwise.
    scope = determinism.reproducibility_scope()
    print(f"reproducibility_scope={scope}")
    print(f"run_dir={run_dir}")
    print(f"runtime precision={runtime_spec.precision} device={runtime_spec.requested_device}")

    try:
        disposition = curriculum.run(
            resume_ctx=resume_ctx,
            from_resume=from_resume,
        )
    except Exception as exc:
        print(f"error: training failed: {exc}", file=sys.stderr)
        return 1

    print(f"terminal_disposition={getattr(disposition, 'value', disposition)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
