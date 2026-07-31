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
import json
import logging
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np

from pinn.architecture_spec import ArchitectureSpec
from pinn.network import build_network
from pinn.runtime import RuntimeSpec, resolve_runtime
from pinn.training import determinism, validation_gate
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
from pinn.training.heartbeat import (
    HeartbeatThread,
    emit_mem_line,
    sample_memory_fields,
)
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
from pinn.training.run_metadata import (
    TRAINING_METADATA_FILENAME,
    compute_s_h,
    load_training_metadata,
    validate_s_h,
    write_training_metadata,
)
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.signals import SignalState, install_signal_handlers
from pinn.training.stage_exit import StageExitMachine
from pinn.training.step_log import HumanStepHandler, JsonlStepHandler
from pinn.training.summary import finalize_summary, stub_summary
from pinn.training.tb_sink import TbSink

# Overridable for tests (inject synthetic sources / alternate runs root).
_RUNS_ROOT: Path = Path("runs")
_SOURCE_FACTORY: Optional[Callable[[TrainingConfig], tuple[Any, Any]]] = None
_HAS_DATASET: bool = False  # v2.0 wires no real data source


def _append_validation_record(
    path: Path,
    *,
    step: int,
    final_val_loss: float,
    previous_val_loss: Optional[float],
    gate_fields: Optional[Mapping[str, Any]] = None,
) -> float:
    """Persist one validation observation and its contemporaneous trend.

    Every validation event leaves exactly one JSON-safe JSONL line, including
    a non-finite ``final_val_loss`` or a failed gate pass (D-20/CR-05): a
    later invalid event must never leave an older eligible record looking
    like the current one, so this seam never returns early without appending
    (T-46-10-05/06). The step is validated through
    ``validation_gate.sidecar_relative_path`` BEFORE conversion so a
    bool/fraction/string/negative step can never name a record (WR-01).
    """
    validation_gate.sidecar_relative_path(step)  # strict identity check only
    value = float(final_val_loss)
    previous_finite = (
        previous_val_loss is not None and math.isfinite(float(previous_val_loss))
    )
    if not math.isfinite(value) or not previous_finite:
        trend = "unavailable"
    elif value < float(previous_val_loss):
        trend = "improving"
    elif value > float(previous_val_loss):
        trend = "worsening"
    else:
        trend = "flat"
    record = {
        "step": int(step),
        "final_val_loss": validation_gate.json_safe_float(value),
        "trend": trend,
    }
    if gate_fields is not None:
        # Gate values are already json-safe (finite numbers or string sentinels)
        # per 46-03, so the existing allow_nan=False serialization stands.
        record.update(dict(gate_fields))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()
    return value


def _run_validation_gate_pass(
    model,
    validation_source,
    *,
    stage: int,
    global_step: int,
    run_dir: Path,
    runtime_spec: Any,
) -> dict[str, Any]:
    """Compute, durably publish, and compact one full-pool gate observation.

    The testable seam ``checkpoint_hook`` calls at the existing validation event
    boundary. Instrumentation must never kill training (D-15/D-20), so every
    exception converts to a ``failed:`` status record carrying no pointer: the
    run stays inspectable as EVAL-01-ineligible while training control flow is
    unchanged. The sidecar is published BEFORE any pointer field is produced,
    and the pointer fields come only from ``compact_validation_fields``, which
    re-validates the durable sidecar (D-17).
    """
    try:
        observation = validation_gate.compute_validation_gate(
            model,
            validation_source,
            stage=int(stage),
            global_step=int(global_step),
            frame=validation_gate.RATIFIED_VALIDATION_FRAME,
            dtype=runtime_spec.dtype,
            device=runtime_spec.torch_device,
        )
        validation_gate.publish_gate_sidecar(run_dir, observation)
        return validation_gate.compact_validation_fields(observation, run_dir)
    except Exception as exc:  # deliberately broad: D-15/D-20
        print(
            f"warning: validation gate pass failed at step {int(global_step)}: "
            f"{type(exc).__name__}",
            file=sys.stderr,
        )
        return {
            "gate_schema_version": validation_gate.GATE_SIDECAR_SCHEMA_VERSION,
            "gate_status": "failed:" + type(exc).__name__,
        }


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
                k0=self.k0(key),
                uabs0=self.uabs0(key),
            )

        def k0(self, key):
            # Deterministic positive CONF-02 fixture components so the
            # synthetic dev path exercises the same S_H pipeline instead of
            # bypassing it; a source lacking the accessors refuses fail-closed.
            return 0.5 + key.id / 10000.0

        def uabs0(self, key):
            return 2.0 + key.id / 10000.0

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


class DataReachabilityError(ValueError):
    """The admitted corpus root is unreachable.

    A fail-closed refusal raised BEFORE any expensive construction / optimizer /
    checkpoint, preserving CTX-79's corpus policy: no automatic copy, no
    master-corpus mutation, and no silent fallback to synthetic data.
    """


# The two locked CTX-79 reachability fallbacks, named verbatim in every refusal
# so the operator gets an actionable message rather than a mid-run corpus crash.
_CTX79_FALLBACKS = (
    "Reachability fallbacks (CTX-79): (1) run from the main-root checkout that "
    "contains the gitignored corpus, OR (2) make a gitignored, read-only Stage-0 "
    "copy in the trainex worktree and set data.root to its Data/ directory. The "
    "corpus is never copied or mutated automatically, and an admitted run never "
    "silently falls back to synthetic data."
)


def _admitted_data_preflight(config: TrainingConfig) -> Path:
    """Refuse an admitted run whose corpus root is unreachable, before construction.

    Resolution order (CTX-79): the explicit ``data.root`` when set, else
    ``default_data_root()`` (main-repo ``simulation_data/Data`` via the shared
    git-common dir). A missing / non-directory root raises
    ``DataReachabilityError`` naming BOTH locked CTX-79 fallbacks, so a missing
    corpus is an actionable refusal rather than a mid-run crash. This checks
    reachability only — it never copies, mutates the master corpus, or falls back
    to synthetic data; the adapter's own scan performs admission afterward.
    """
    from pinn.data.adapter import default_data_root

    if config.data.root is not None:
        root = Path(config.data.root)
        source = "data.root"
    else:
        try:
            root = Path(default_data_root())
        except Exception as exc:
            raise DataReachabilityError(
                f"could not resolve the default corpus root "
                f"(default_data_root failed: {exc}). {_CTX79_FALLBACKS}"
            ) from exc
        source = "default_data_root"

    if not root.exists() or not root.is_dir():
        raise DataReachabilityError(
            f"admitted corpus root is unreachable: {root} (via {source}) does not "
            f"exist or is not a directory. {_CTX79_FALLBACKS}"
        )
    return root.resolve()


def _resolve_admitted_data_root(config: TrainingConfig) -> Path:
    """Mirror ``AdmittedSetAdapter._resolve_root``'s precedence (explicit
    ``data.root`` -> ``GSD_DATA_ROOT`` env -> ``default_data_root()``) so a
    relative ``data.blacklist_path`` (DI-43-06-01) resolves against the SAME
    root the adapter will actually use. Duplicated (not imported) because this
    plan's owned files exclude ``pinn/data/adapter.py``; keep in sync with
    ``AdmittedSetAdapter._resolve_root`` if that precedence ever changes.
    """
    from pinn.data.adapter import DATA_ROOT_ENV, default_data_root

    if config.data.root is not None:
        return Path(config.data.root).resolve()
    if os.environ.get(DATA_ROOT_ENV):
        return Path(os.environ[DATA_ROOT_ENV]).resolve()
    return Path(default_data_root()).resolve()


def _resolve_blacklist_path(config: TrainingConfig) -> Optional[str]:
    """Resolve ``data.blacklist_path`` against the ADMITTED DATA ROOT, never the
    CWD (DI-43-06-01), so a relative path stays portable across machines and
    worktrees in a committed config (e.g. ``configs/smoke.yaml``). An absolute
    path is used as-is. ``None`` preserves the adapter's own default
    (``<data_root>/problematic_ics_blacklist.json``).
    """
    raw = config.data.blacklist_path
    if raw is None:
        return None
    candidate = Path(raw)
    if candidate.is_absolute():
        return str(candidate)
    return str((_resolve_admitted_data_root(config) / candidate).resolve())


def _build_admitted_sources(config: TrainingConfig, run_dir: Path) -> tuple[Any, Any]:
    """Compose the sole production admitted corpus into leakage-free split views.

    Constructs the ``AdmittedSetAdapter`` on CPU/float32 residency REGARDLESS of
    the model runtime (43-03 ACC-02 / DATA-01): the adapter owns fp32 CPU tensors
    and each batch is moved onto the model device only at sampling time, so an
    MPS/fp32 model and the CPU/fp32 adapter coexist. A deterministic
    ``SplitManifest`` is created (or reloaded on resume) and atomically persisted
    as ``runs/<run>/splits.json`` BEFORE any batch is drawn, so evaluation can
    later reconstruct the exact held-out ``StageIndex``. Only the train and
    validation split views are returned — the test split never reaches training.
    """
    # Deferred imports keep the composition root's import light (mirrors
    # ``_synthetic_split_sources``); the heavy data stack loads only for a real run.
    from pinn.data.adapter import AdmittedSetAdapter
    from pinn.data.splits import SplitManifest, StageIndex, write_split_manifest

    adapter = AdmittedSetAdapter(
        root=config.data.root,
        blacklist_path=_resolve_blacklist_path(config),
        precision="float32",
        device="cpu",
        run_dir=run_dir,
    )

    manifest_path = Path(run_dir) / "splits.json"
    if manifest_path.is_file():
        # Resume: reuse the frozen split provenance rather than re-partitioning.
        manifest = SplitManifest.from_path(manifest_path)
    else:
        # Fresh launch: partition and atomically write splits.json BEFORE batches.
        manifest = write_split_manifest(adapter, run_dir, seed=int(config.run.seed))

    train_index = StageIndex.from_split(adapter, manifest, "train")
    validation_index = StageIndex.from_split(adapter, manifest, "validation")
    return train_index, validation_index


def _build_sources(config: TrainingConfig, run_dir: Path) -> tuple[Any, Any]:
    if _SOURCE_FACTORY is not None:
        return _SOURCE_FACTORY(config)
    if config.data.source == "admitted":
        return _build_admitted_sources(config, run_dir)
    return _synthetic_split_sources()


def _assert_s_h_matches_artifact(run_dir, train_source, *, energy_floor_factor) -> float:
    """CONF-02 D-18 resume gate: re-derive S_H and compare with the artifact.

    Loads ``run_dir/training_metadata.json`` via ``load_training_metadata``
    (which re-validates structure, the D-17 predicate, the ``eps_h`` product,
    the frame block, and the persisted-vs-live softening/factor bindings),
    recomputes ``S_H`` and ``N_train`` from the LIVE train source, and refuses
    fail-closed on any mismatch — semantic-recomputation discipline: the
    persisted number is trusted only after a live re-derivation agrees, and a
    refusal NEVER overwrites the artifact. Returns the validated ``s_h`` so
    both setup branches bind the same local (plan 47-03 threads it into
    ``RunController``).
    """
    metadata = load_training_metadata(run_dir, expected_energy_floor_factor=float(energy_floor_factor))
    live_s_h, live_n_train = compute_s_h(train_source)
    if live_s_h != metadata["s_h"]:
        raise ValueError(
            f"live S_H recompute {live_s_h!r} != persisted artifact "
            f"{metadata['s_h']!r}: the train population or its admission "
            "capture changed since training_metadata.json was written; "
            "refusing to resume"
        )
    if live_n_train != metadata["n_train"]:
        raise ValueError(
            f"live n_train recompute {live_n_train!r} != persisted artifact "
            f"{metadata['n_train']!r}: refusing to resume"
        )
    return float(metadata["s_h"])


def _effective_runtime_labels(config: TrainingConfig) -> tuple[str, str]:
    """Return the precision/device labels the launch will actually execute."""
    if config.run.strict_cpu_determinism:
        return ("float64", "cpu")
    return (config.run.precision, config.run.device)


def _write_smoke_timing_calibration(
    config: TrainingConfig, run_controller: RunController, runs_root: Path
) -> None:
    """Persist a fresh-launch timing calibration after a successful smoke.

    Fail-closed (SPEC edge R2): writes the versioned
    ``runs/.calibration/stage0-timing.json`` ONLY when the run measured a finite,
    strictly-positive per-step EMA. Absent a measurement the calibration is not
    written — a fresh launch then finds no forecast rather than an invented one.
    The measured partial s/step already lives in the run's ``status.json``
    heartbeat evidence on any outcome; only a terminal-success measurement is
    ever marked calibration-``valid``. A write failure never fails the run.
    """
    from pinn.training import timing

    s_per_step = getattr(run_controller, "s_per_step", None)
    if s_per_step is None or not math.isfinite(float(s_per_step)) or float(s_per_step) <= 0.0:
        return
    try:
        precision, device = _effective_runtime_labels(config)
        timing.write_calibration(
            s_per_step=float(s_per_step),
            full_stage0_steps=int(config.stage.max_epochs),
            precision=precision,
            device=device,
            runs_root=runs_root,
        )
    except Exception as exc:  # never let a calibration write fail the run
        print(f"warning: smoke timing calibration write failed: {exc}", file=sys.stderr)


# ACC-01 / SPEC prohibition 4: no projected >30-minute run may proceed without a
# green verify ladder. 1800 s is the 30-minute boundary; a forecast of EXACTLY
# 1800 s PASSES (SPEC edge R1 — the reject is the strict inequality > 1800).
_DURATION_GATE_LIMIT_S = 1800.0


class DurationGateError(ValueError):
    """Typed refusal: the >30-min launch duration gate refused a fresh launch.

    Raised BEFORE any run-directory / checkpoint / optimizer construction
    (fail-closed, ACC-01). Two refusal modes, both reported to stderr with no
    warning-only path:

    * no valid persisted 43-03 Stage-0 timing calibration is available for a
      non-smoke launch — there is no honest forecast, and the gate never
      fabricates one from a step count or a default estimate (SPEC edge R2);
    * the measured forecast is strictly above 1800 s and no fresh GREEN
      full-fingerprint 43-01 verify marker authorizes the run.
    """


def _check_duration_gate(config: TrainingConfig, *, runs_root: Path) -> None:
    """Fail-closed >30-min launch duration gate (ACC-01); raise to refuse.

    Wired into the launch preflight BEFORE run-directory creation so a refused
    run leaves no run-dir behind. The forecast is the PERSISTED measured
    seconds-per-step (plan 43-03 ``runs/.calibration/stage0-timing.json``) times
    THIS launch's own declared Stage-0 budget (``config.stage.max_epochs``) — the
    authoritative launch forecast, recomputed from the launch's own budget rather
    than the calibration record's recorded budget (43-03 SUMMARY). A run whose
    forecast is strictly above 1800 s additionally needs a fresh GREEN
    full-fingerprint verify marker (plan 43-01 ``marker_is_green_and_fresh``);
    a forecast of exactly 1800 s passes (SPEC edge R1).

    Exemptions: ``run.smoke`` (the ~5-min smoke is the gate's own calibration
    source) and resume (a resume re-enters a run that was already authorized at
    its fresh launch; re-gating it would lock an operator out of their own run
    once the 24 h marker window lapses). The caller applies the resume exemption.
    """
    if config.run.smoke:
        return

    # Deferred imports keep the composition root's top-level import light and
    # avoid a load-time cycle (pinn.training.timing imports pinn.verify).
    from pinn import verify
    from pinn.training import timing

    # One runtime+code fingerprint certifies BOTH the calibration read and the
    # marker predicate, so they authorize the identical device/dtype/torch/
    # python/git-head identity.
    precision, device = _effective_runtime_labels(config)
    fingerprint = verify.current_fingerprint(
        precision=precision, device=device
    )
    requested_steps = int(config.stage.max_epochs)
    forecast = timing.forecast_from_calibration(
        runs_root, requested_steps=requested_steps, fingerprint=fingerprint
    )
    if forecast is None:
        raise DurationGateError(
            f"no valid persisted Stage-0 timing calibration is available for a "
            f"non-smoke launch ({requested_steps} steps on "
            f"{precision}/{device}); refusing before "
            f"construction rather than forecasting without a measurement. Run the "
            f"ACC-02 smoke (configs/smoke.yaml) to persist a calibration first."
        )
    if forecast > _DURATION_GATE_LIMIT_S:
        marker = verify.read_verify_marker(runs_root)
        if not verify.marker_is_green_and_fresh(marker, fingerprint=fingerprint):
            raise DurationGateError(
                f"projected run duration {forecast:.1f} s exceeds the "
                f"{_DURATION_GATE_LIMIT_S:.0f} s (30 min) limit and no fresh green "
                f"full-fingerprint verify marker authorizes it; refusing before "
                f"construction (SPEC prohibition 4). Run `python -m pinn.verify` "
                f"to green the ladder first."
            )


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

    # ACC-01 >30-min launch duration gate — fail-closed BEFORE run-dir creation.
    # A fresh non-smoke launch must present a valid persisted 43-03 timing
    # calibration (and, for a forecast strictly > 1800 s, a fresh green 43-01
    # verify marker). Resume re-enters an already-authorized run and is exempt.
    if not is_resume:
        try:
            _check_duration_gate(config, runs_root=runs_root)
        except DurationGateError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    run_dir.mkdir(parents=True, exist_ok=True)
    for directory in ("logs", "tb", "failure"):
        (run_dir / directory).mkdir(exist_ok=True)
    ckpt_dir = run_dir / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    run_started_at = datetime.now(timezone.utc)
    summary_header = {
        "run_name": run_name,
        "start_utc": run_started_at.isoformat(),
        "end_utc": None,
        "wall_clock_secs": None,
        "device": config.run.device,
        "precision": config.run.precision,
        "seed": int(config.run.seed),
    }
    monitor = config.run.monitor
    heartbeat = HeartbeatThread(
        run_dir / "status.json",
        heartbeat_secs=int(monitor.heartbeat_secs),
        staleness_factor=int(monitor.staleness_factor),
        run_name=run_name,
        pid=os.getpid(),
    )
    heartbeat.write_initial()
    stub_summary(run_dir, header=summary_header)

    training_logger = logging.getLogger("pinn.training")
    training_logger.setLevel(logging.INFO)
    tracked_handlers = [
        JsonlStepHandler(run_dir / "logs" / "train.log.jsonl"),
        HumanStepHandler(run_dir / "logs" / "train.log"),
        TbSink(run_dir / "tb"),
    ]
    for handler in tracked_handlers:
        training_logger.addHandler(handler)

    signal_state = SignalState()

    def on_escalate() -> None:
        try:
            heartbeat.transition("interrupted")
        except Exception:
            pass
        for handler in tracked_handlers:
            try:
                handler.flush()
            except Exception:
                pass

    restore_handlers = install_signal_handlers(signal_state, on_escalate=on_escalate)
    heartbeat.start()

    def finish_run(
        disposition: str,
        exit_code: int,
        final_losses: Optional[Mapping[str, Any]] = None,
    ) -> int:
        """Finalize one catchable run and release process-global resources."""
        try:
            finished_at = datetime.now(timezone.utc)
            summary_header["end_utc"] = finished_at.isoformat()
            summary_header["wall_clock_secs"] = (
                finished_at - run_started_at
            ).total_seconds()
            heartbeat.transition(disposition)
            finalize_summary(
                run_dir,
                disposition=disposition,
                header=summary_header,
                final_losses=final_losses if disposition == "finished" else None,
                curriculum_path=run_dir / "curriculum.jsonl",
                validation_records_path=run_dir / "validation.jsonl",
            )
        finally:
            heartbeat.stop()
            heartbeat.join()
            for handler in tracked_handlers:
                training_logger.removeHandler(handler)
                handler.close()
            restore_handlers()
        return exit_code

    # Fail-closed corpus reachability BEFORE runtime resolve / network build /
    # adapter scan / optimizer (CTX-79-preserving refusal; never a silent
    # synthetic fallback for an admitted run).
    if config.data.source == "admitted":
        try:
            _admitted_data_preflight(config)
        except DataReachabilityError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return finish_run("failed", 1)

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
        return finish_run("failed", 1)

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
        return finish_run("failed", 1)

    config_identity = build_config_identity_envelope(
        config, arch_spec, effective_runtime_spec=runtime_spec
    )

    # Network build against the (possibly forced) runtime_spec.
    model = build_network(
        arch_spec,
        dtype=runtime_spec.dtype,
        device=runtime_spec.torch_device,
    )

    # Adapter admission runs here; a reachable-but-empty/incomplete corpus is a
    # fail-closed refusal (never a half-started run), matching the preflight.
    try:
        train_source, validation_source = _build_sources(config, run_dir)
    except ValueError as exc:
        print(f"error: failed to build data sources: {exc}", file=sys.stderr)
        return finish_run("failed", 1)

    # CONF-02 (D-13..D-18): S_H = median_train(K0 + Uabs0), computed once in
    # float64 over the train split at setup, persisted with eps_H BEFORE any
    # step, and re-validated on resume by live recompute-and-compare. An
    # invalid value is a fail-closed refusal before step 1 (D-17) — never a
    # substituted value.
    try:
        energy_floor_factor = float(config.stage.energy_floor_factor)
        if (run_dir / TRAINING_METADATA_FILENAME).is_file():
            # Resume: re-validate the artifact and match it against a live
            # recompute; the return BINDS s_h from the checked artifact.
            s_h = _assert_s_h_matches_artifact(
                run_dir, train_source, energy_floor_factor=energy_floor_factor
            )
        else:
            # Fresh launch: compute, validate, persist, then re-read through
            # the same gate so the just-written artifact is proven loadable.
            s_h, n_train = compute_s_h(train_source)
            s_h = validate_s_h(s_h)
            write_training_metadata(
                run_dir,
                s_h=s_h,
                n_train=n_train,
                energy_floor_factor=energy_floor_factor,
            )
            _assert_s_h_matches_artifact(
                run_dir, train_source, energy_floor_factor=energy_floor_factor
            )
    except ValueError as exc:
        print(
            f"error: failed to establish S_H training metadata: {exc}",
            file=sys.stderr,
        )
        return finish_run("failed", 1)
    # Both branches bind the same s_h local; plan 47-03 threads it into the
    # RunController(...) construction below (shared main() scope).

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
    validation_state_cell: dict[str, Any] = {
        "previous": None,
        "last_step": None,
    }
    last_losses_cell: dict[str, Optional[Mapping[str, Any]]] = {"losses": None}

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
        validation_every = int(config.opt.validation_every)
        if (
            val is not None
            and int(global_step) % validation_every == 0
            and validation_state_cell["last_step"] != int(global_step)
        ):
            # Gate-aligned validation seam (46-07): same branch, same
            # validation_every condition, same validation_state_cell dedup --
            # D-10 forbids any new cadence, knob, or trigger.
            gate_fields = _run_validation_gate_pass(
                model,
                validation_source,
                stage=int(curriculum_state_accessor()["stage"]),
                global_step=int(global_step),
                run_dir=run_dir,
                runtime_spec=runtime_spec,
            )
            validation_state_cell["previous"] = _append_validation_record(
                run_dir / "validation.jsonl",
                step=int(global_step),
                final_val_loss=float(val),
                previous_val_loss=validation_state_cell["previous"],
                gate_fields=gate_fields,
            )
            validation_state_cell["last_step"] = int(global_step)
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
        last_losses_cell["losses"] = dict(terms_map or {})
        mem_fields = sample_memory_fields()
        heartbeat.update(
            step=int(global_step),
            stage=int(stage),
            phase=str(phase),
            epoch=int(getattr(controller, "_active_epoch", 0)),
            losses=terms_map,
            s_per_step_ema=getattr(controller, "_s_per_step_ema", None),
            mem=mem_fields,
        )
        # OPS-04 periodic mem: line — same main-thread update that cached the
        # value (heartbeat.py emit_mem_line contract), thinned to mem_every.
        if int(monitor.mem_every) > 0 and int(global_step) % int(monitor.mem_every) == 0:
            emit_mem_line(mem_fields)
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
        should_stop=lambda: signal_state.stop_requested,
        replay_count=config.stage.replay_count,
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
            return finish_run("failed", 1)

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
            return finish_run("failed", 1)

        _restore_run_controller(run_controller, payload)
        initial_stage, resume_ctx = _derive_resume_plan(
            payload, hold_stage=bool(args.hold_stage), resume_arg=str(args.resume)
        )

    curriculum = CurriculumController(
        config=config,
        checkpoint_store=store,
        scheduled_weights=scheduled_weights,
        run_controller=run_controller,
        recover_retries=config.run.recover_retries,
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
    heartbeat.transition("running")

    run_raised = False
    try:
        disposition = curriculum.run(
            resume_ctx=resume_ctx,
            from_resume=from_resume,
        )
    except Exception as exc:
        run_raised = True
        disposition = None
        print(f"error: training failed: {exc}", file=sys.stderr)

    # HALT alone is ambiguous: an operator-visible failure is derived from
    # interruption, failure artifacts, non-finite logging, or an exception.
    if signal_state.stop_requested:
        checkpoint_payload = build_checkpoint_payload(
            run_controller,
            curriculum_state_accessor(),
            config_identity,
            CHECKPOINT_SCHEMA_VERSION,
        )
        store.save_rolling(checkpoint_payload, int(run_controller._global_step))
        return finish_run("interrupted", signal_state.exit_code)

    jsonl_handler = tracked_handlers[0]
    failed = (
        run_raised
        or any((run_dir / "failure").iterdir())
        or getattr(jsonl_handler, "last_step_finite", None) is False
    )
    if failed:
        return finish_run("failed", 1)

    # Terminal success: a smoke persists its measured s/step calibration (fail-
    # closed — no valid calibration without a finite positive measurement).
    if config.run.smoke:
        _write_smoke_timing_calibration(config, run_controller, runs_root)

    print(f"terminal_disposition={getattr(disposition, 'value', disposition)}")
    return finish_run("finished", 0, last_losses_cell["losses"])


if __name__ == "__main__":
    sys.exit(main())
