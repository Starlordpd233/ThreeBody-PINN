"""Phase 43 / ACC-03 (43-02 Task 2) — ``python -m pinn.evaluate`` one-time gate.

The milestone's ONLY acceptance metric: reconstructs the persisted held-out
test split from a checkpoint's OWNING run (frozen ``config.yaml`` + persisted
``splits.json`` — plan 43-03's contract), runs the model forward pass ONCE
under ``.eval()`` + ``torch.no_grad()`` over that split's IC13/raw-mass/time
metadata, and renders the authoritative post-v1.3 binary gate
(``pinn.verification.gate_metrics``) to ``metrics.json`` / ``metrics.md`` /
``evaluation-receipt.json`` under the owning run's canonical ``evaluation/``
directory.

Closed data flow (SPEC prohibition: the held-out set is evaluated only once
and is never selected by training/validation evidence):

* ``--checkpoint`` resolves its OWNING run directory (the one containing a
  frozen ``config.yaml`` and a persisted ``splits.json`` — never inferred any
  other way); a checkpoint outside such a run is a fail-closed refusal
  (``CheckpointOwnershipError``), never a partial/synthetic evaluation.
* The evaluator loads that run's config and manifest, builds the SAME
  CPU/float32 ``AdmittedSetAdapter`` contract plan 43-03 defines, and selects
  ``StageIndex.from_split(adapter, manifest, "test")`` — it NEVER calls
  ``write_split_manifest`` (no split is rebuilt) and takes no
  training/validation split as an argument.
* An empty test view is refused (``EmptyTestSetError``) rather than rendering
  a verdict over zero trajectories.
* ``--output`` MUST resolve to the owning run's canonical ``evaluation/``
  directory. A fixed ``evaluation-attempt.json`` is created there with
  ``O_CREAT | O_EXCL`` before corpus access. A pre-existing attempt OR receipt
  refuses a second evaluation (``EvaluationReceiptExistsError``), so neither
  output redirection nor a crash/concurrent evaluator can replay the budget.
* Every metric flows through ``pinn.verification.gate_metrics`` (Task 1);
  this module never differentiates the gate and never fabricates a value for
  a non-finite result — ``metrics.json``/``metrics.md`` render the honest
  FAIL instead.
* ``--output`` is also path-guarded beneath a ``runs/`` root
  (``OutputPathEscapeError`` on escape) — mirrors ``pinn.verify``'s /
  ``pinn.training.timing``'s marker path-guard convention. Plotting is
  explicitly NOT implemented here (SPEC boundary: ``metrics.json`` /
  ``metrics.md`` never depend on it).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence

import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.adapter import AdmittedSetAdapter
from pinn.data.splits import SplitManifest, StageIndex
from pinn.network import build_network
from pinn.runtime import resolve_runtime
from pinn.train import _resolve_blacklist_path
from pinn.training.atomic_io import atomic_write_text
from pinn.training.config_yaml import load_config
from pinn.training.summary import refresh_completed_summary
from pinn.verification import gate_metrics

__all__ = [
    "METRICS_SCHEMA_VERSION",
    "ATTEMPT_SCHEMA_VERSION",
    "RECEIPT_SCHEMA_VERSION",
    "CheckpointOwnershipError",
    "OutputPathEscapeError",
    "EmptyTestSetError",
    "EvaluationReceiptExistsError",
    "EvaluationOutcome",
    "evaluate_run",
    "main",
]

METRICS_SCHEMA_VERSION = "phase43-evaluate-metrics/v1"
ATTEMPT_SCHEMA_VERSION = "phase43-evaluation-attempt/v1"
RECEIPT_SCHEMA_VERSION = "phase43-evaluation-receipt/v1"

#: Overridable for tests, mirroring ``pinn.train._RUNS_ROOT`` / ``pinn.verify``.
_RUNS_ROOT: Path = Path("runs")


class CheckpointOwnershipError(ValueError):
    """The checkpoint is not owned by a run with a frozen config + splits."""


class OutputPathEscapeError(ValueError):
    """``--output`` escapes the runs root or is not the canonical run output."""


class EmptyTestSetError(ValueError):
    """The persisted held-out test split has zero records."""


class EvaluationReceiptExistsError(RuntimeError):
    """A prior evaluation attempt or receipt exists for this owning run.

    The held-out test set is evaluated only ONCE (SPEC prohibition); no
    automatic rerun is authorized unless an explicit new milestone procedure
    changes the contract.
    """


# ---------------------------------------------------------------------------
# Checkpoint ownership + output path guard.
# ---------------------------------------------------------------------------


def _resolve_owning_run(checkpoint_path: Path) -> Path:
    """The run directory owning ``checkpoint_path`` — one with a frozen
    ``config.yaml`` AND a persisted ``splits.json`` sibling.

    Checked first at the conventional ``runs/<name>/checkpoints/<file>.pt``
    layout (``pinn.train`` composition root), then at the checkpoint's own
    parent directory (defensive fallback). A checkpoint anywhere else is a
    fail-closed refusal rather than a silently-partial evaluation.
    """
    checkpoint_path = Path(checkpoint_path)
    if not checkpoint_path.is_file():
        raise CheckpointOwnershipError(
            f"checkpoint does not exist: {checkpoint_path}"
        )
    candidates = []
    if checkpoint_path.parent.name == "checkpoints":
        candidates.append(checkpoint_path.parent.parent)
    candidates.append(checkpoint_path.parent)
    for run_dir in candidates:
        if (run_dir / "config.yaml").is_file() and (run_dir / "splits.json").is_file():
            return run_dir.resolve()
    raise CheckpointOwnershipError(
        f"checkpoint {checkpoint_path} is not owned by a run with a frozen "
        f"config.yaml and a persisted splits.json (checked "
        f"{[str(c) for c in candidates]}); evaluate reconstructs the held-out "
        "split ONLY from a run's own frozen provenance"
    )


def _validate_output_dir(output_dir: Path, *, runs_root: Optional[Path] = None) -> Path:
    """Resolve ``output_dir`` and refuse anything escaping the runs root."""
    root = Path(runs_root if runs_root is not None else _RUNS_ROOT).resolve()
    resolved = Path(output_dir).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise OutputPathEscapeError(
            f"--output must resolve beneath the runs root {root}; got {resolved}"
        ) from exc
    return resolved


def _single_use_refusal(path: Path) -> EvaluationReceiptExistsError:
    return EvaluationReceiptExistsError(
        f"a prior evaluation attempt or receipt already exists at {path}; the "
        "held-out test set is evaluated only once (SPEC single-eval discipline) "
        "— failed, abandoned, concurrent, and completed attempts all consume "
        "the budget"
    )


def _assert_evaluation_unclaimed(*, attempt_path: Path, receipt_path: Path) -> None:
    """Cheap fail-closed guard before frozen-input validation.

    The exclusive create in ``_claim_evaluation_attempt`` is the authoritative
    race guard. This preliminary check provides a clear refusal without loading
    config or touching the admitted corpus when a durable claim already exists.
    """
    for path in (attempt_path, receipt_path):
        if path.exists():
            raise _single_use_refusal(path)


def _claim_evaluation_attempt(
    attempt_path: Path,
    *,
    run_dir: Path,
    checkpoint_path: Path,
    stamp: datetime,
) -> None:
    """Atomically and durably consume this run's one held-out evaluation.

    The claim is intentionally never removed. If anything after this function
    fails, the in-progress record remains the honest evidence that corpus
    access began and a retry is forbidden.
    """
    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(attempt_path, flags, 0o600)
    except FileExistsError as exc:
        raise _single_use_refusal(attempt_path) from exc

    payload = {
        "schema_version": ATTEMPT_SCHEMA_VERSION,
        "status": "in_progress",
        "run_dir": str(run_dir),
        "checkpoint_path": str(checkpoint_path),
        "claimed_at": stamp.isoformat(),
    }
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    directory_fd = os.open(attempt_path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _finalize_evaluation_attempt(
    attempt_path: Path,
    *,
    run_dir: Path,
    checkpoint_path: Path,
    receipt_path: Path,
    claimed_at: datetime,
    completed_at: datetime,
) -> None:
    """Mark a successfully rendered PASS/FAIL gate receipt as completed.

    ``atomic_write_text`` replaces the in-progress payload but not its fixed
    path. A crash before this call therefore leaves the original consumed
    claim intact rather than restoring a clean slate.
    """
    payload = {
        "schema_version": ATTEMPT_SCHEMA_VERSION,
        "status": "completed",
        "run_dir": str(run_dir),
        "checkpoint_path": str(checkpoint_path),
        "receipt_path": str(receipt_path),
        "claimed_at": claimed_at.isoformat(),
        "completed_at": completed_at.isoformat(),
    }
    atomic_write_text(
        attempt_path, json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )


# ---------------------------------------------------------------------------
# Digests.
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Held-out inference inputs (IC13 + raw masses + persisted times only).
# ---------------------------------------------------------------------------


def _build_tau_ic13(times: torch.Tensor, ic13: Any, *, dtype, device) -> torch.Tensor:
    """The model-facing ``[tau, IC13]`` (N, 14) input for one record's snapshots.

    ``tau = 2*(t/T_CHARACTERISTIC_TIME) - 1`` — the SAME map
    ``pinn.data.batches.sample_data_points`` uses; the IC13 slice is supplied
    WHOLESALE (never re-normalized here, per ``pinn.network`` NET-02).
    """
    times_t = torch.as_tensor(times, dtype=dtype, device=device).reshape(-1)
    tau = 2.0 * (times_t / T_CHARACTERISTIC_TIME) - 1.0
    ic13_t = torch.as_tensor(ic13, dtype=dtype, device=device).reshape(1, 13)
    ic13_t = ic13_t.expand(times_t.shape[0], 13)
    return torch.cat((tau.reshape(-1, 1), ic13_t), dim=1)


# ---------------------------------------------------------------------------
# Result + JSON-safe rendering (a NaN/Inf metric is rendered honestly, never
# a crash and never silently dropped — SPEC edge R3 / prohibition 2).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EvaluationOutcome:
    output_dir: Path
    metrics_path: Path
    metrics_md_path: Path
    receipt_path: Path
    verdict: str
    eps_h: float
    scs: float
    n_test_trajectories: int


def _json_safe_float(value: float):
    v = float(value)
    if math.isnan(v):
        return "NaN"
    if math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    return v


def _display_float(value: float) -> str:
    v = float(value)
    if math.isnan(v):
        return "nan"
    if math.isinf(v):
        return "inf" if v > 0 else "-inf"
    return f"{v:.6e}"


def _record_key_dict(key: Any) -> dict[str, Any]:
    return {"variant": key.variant, "fidelity": key.fidelity, "id": key.id}


# ---------------------------------------------------------------------------
# The closed one-time evaluation.
# ---------------------------------------------------------------------------


def evaluate_run(
    *,
    checkpoint_path,
    output_dir,
    runs_root: Optional[Path] = None,
) -> EvaluationOutcome:
    """Run the ACC-03 one-time held-out gate and write its artifacts.

    Fail-closed ordering: checkpoint ownership -> canonical output guard ->
    prior attempt/receipt check -> frozen config/manifest load -> manifest-only
    empty-test refusal -> EXCLUSIVE durable claim -> CPU/float32 adapter +
    test-split selection -> model load (``weights_only=True``) -> the single
    no-grad forward pass -> gate metrics -> atomic artifact writes -> completed
    attempt marker. No admitted-corpus access occurs before the claim.
    """
    checkpoint_path = Path(checkpoint_path)
    run_dir = _resolve_owning_run(checkpoint_path)
    resolved_output = _validate_output_dir(output_dir, runs_root=runs_root)
    canonical_output = (run_dir / "evaluation").resolve()
    if resolved_output != canonical_output:
        raise OutputPathEscapeError(
            f"--output for checkpoint {checkpoint_path} must resolve to its "
            f"owning run's canonical evaluation directory {canonical_output}; "
            f"got {resolved_output}"
        )

    receipt_path = resolved_output / "evaluation-receipt.json"
    attempt_path = resolved_output / "evaluation-attempt.json"
    _assert_evaluation_unclaimed(
        attempt_path=attempt_path, receipt_path=receipt_path
    )

    config = load_config(run_dir / "config.yaml")
    manifest = SplitManifest.from_path(run_dir / "splits.json")
    if not manifest.fixed_order("test"):
        raise EmptyTestSetError(
            f"held-out test split is empty for run {run_dir}; refusing to "
            "render a gate verdict over zero trajectories"
        )

    claim_stamp = datetime.now(timezone.utc)
    _claim_evaluation_attempt(
        attempt_path,
        run_dir=run_dir,
        checkpoint_path=checkpoint_path,
        stamp=claim_stamp,
    )

    # CPU/float32 ONLY — the same 43-03 DATA-01 residency contract, never the
    # model's runtime device (mirrors ``pinn.train._build_admitted_sources``).
    adapter = AdmittedSetAdapter(
        root=config.data.root,
        blacklist_path=_resolve_blacklist_path(config),
        precision="float32",
        device="cpu",
    )
    test_index = StageIndex.from_split(adapter, manifest, "test")
    test_keys = test_index.record_keys()
    if not test_keys:
        raise EmptyTestSetError(
            f"held-out test split is empty for run {run_dir}; refusing to "
            "render a gate verdict over zero trajectories"
        )

    runtime_spec = resolve_runtime(config.run.precision, config.run.device)
    arch_spec = ArchitectureSpec(seed=int(config.run.seed))
    model = build_network(
        arch_spec, dtype=runtime_spec.dtype, device=runtime_spec.torch_device
    )
    payload = torch.load(checkpoint_path, weights_only=True)
    try:
        model.load_state_dict(payload["model"])
    except KeyError as exc:
        raise CheckpointOwnershipError(
            f"checkpoint {checkpoint_path} has no 'model' state dict "
            "(malformed checkpoint payload)"
        ) from exc

    per_trajectory: list[dict[str, Any]] = []
    model.eval()
    try:
        with torch.no_grad():
            for key in test_keys:
                record = test_index.get(key)
                times_native = test_index.snapshot_times(key)
                tau_ic13 = _build_tau_ic13(
                    times_native, record.ic13,
                    dtype=runtime_spec.dtype, device=runtime_spec.torch_device,
                )
                times_t = torch.as_tensor(
                    times_native, dtype=runtime_spec.dtype, device=runtime_spec.torch_device
                ).reshape(-1)
                masses_row = torch.as_tensor(
                    record.masses, dtype=runtime_spec.dtype, device=runtime_spec.torch_device
                ).reshape(1, 3)
                masses_batch = masses_row.expand(times_t.shape[0], 3)

                predicted = model(tau_ic13, masses_batch)
                positions = predicted.reshape(-1, 3, 3).detach()

                trajectory_metrics = gate_metrics.compute_trajectory_gate_metrics(
                    positions, times_t.detach(), masses_row.reshape(3).detach(),
                )
                per_trajectory.append(
                    {"record_key": key, "eps_h": trajectory_metrics.eps_h}
                )
    finally:
        model.train()

    aggregate = gate_metrics.aggregate_gate_verdict(
        [item["eps_h"] for item in per_trajectory]
    )

    stamp = datetime.now(timezone.utc)
    _write_metrics_json(
        resolved_output / "metrics.json", run_dir=run_dir, checkpoint_path=checkpoint_path,
        aggregate=aggregate, per_trajectory=per_trajectory, stamp=stamp,
    )
    _write_metrics_md(
        resolved_output / "metrics.md", run_dir=run_dir, checkpoint_path=checkpoint_path,
        aggregate=aggregate, n_test_trajectories=len(test_keys), stamp=stamp,
    )
    _write_receipt(
        receipt_path, run_dir=run_dir, checkpoint_path=checkpoint_path,
        aggregate=aggregate, stamp=stamp,
    )
    _finalize_evaluation_attempt(
        attempt_path,
        run_dir=run_dir,
        checkpoint_path=checkpoint_path,
        receipt_path=receipt_path,
        claimed_at=claim_stamp,
        completed_at=stamp,
    )
    # ACC-04: only after BOTH metrics and the one-time receipt are committed,
    # project those persisted artifacts into this run's existing finished
    # summary. The refresh is a no-op for absent/failed/interrupted summaries;
    # it never evaluates again or selects a checkpoint.
    refresh_completed_summary(
        run_dir,
        metrics_path=resolved_output / "metrics.json",
        validation_records_path=run_dir / "validation.jsonl",
        curriculum_path=run_dir / "curriculum.jsonl",
    )

    return EvaluationOutcome(
        output_dir=resolved_output,
        metrics_path=resolved_output / "metrics.json",
        metrics_md_path=resolved_output / "metrics.md",
        receipt_path=receipt_path,
        verdict=aggregate.verdict,
        eps_h=aggregate.eps_h,
        scs=aggregate.scs,
        n_test_trajectories=len(test_keys),
    )


# ---------------------------------------------------------------------------
# Artifact writers (atomic; JSON/Markdown carry the SAME numbers + verdict).
# ---------------------------------------------------------------------------


def _write_metrics_json(
    path: Path, *, run_dir: Path, checkpoint_path: Path, aggregate, per_trajectory, stamp,
) -> None:
    payload = {
        "schema_version": METRICS_SCHEMA_VERSION,
        "run_dir": str(run_dir),
        "checkpoint": str(checkpoint_path),
        "n_test_trajectories": len(per_trajectory),
        "eps_h": _json_safe_float(aggregate.eps_h),
        "scs": _json_safe_float(aggregate.scs),
        "eps_h_reject_threshold": gate_metrics.GATE_EPS_H_REJECT_THRESHOLD,
        "scs_reject_threshold": gate_metrics.GATE_SCS_REJECT_THRESHOLD,
        "verdict": aggregate.verdict,
        "per_trajectory": [
            {
                **_record_key_dict(item["record_key"]),
                "eps_h": _json_safe_float(item["eps_h"]),
            }
            for item in per_trajectory
        ],
        "timestamp": stamp.isoformat(),
    }
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _write_metrics_md(
    path: Path, *, run_dir: Path, checkpoint_path: Path, aggregate, n_test_trajectories: int, stamp,
) -> None:
    check_mark = "✅" if aggregate.verdict == "PASS" else "❌"
    lines = [
        "# Phase 43 Evaluation Metrics",
        "",
        f"Run: `{run_dir}`",
        f"Checkpoint: `{checkpoint_path}`",
        f"Held-out test trajectories: {n_test_trajectories}",
        f"Generated: {stamp.isoformat()}",
        "",
        "## Gate Check",
        "",
        f"- ε_H: {_display_float(aggregate.eps_h)} (reject if > 1e-5) → {check_mark}",
        f"- SCS: {_display_float(aggregate.scs)} (reject if > -5) → {check_mark}",
        "",
        f"**OVERALL: {aggregate.verdict}**",
        "",
        (
            "ε_H (epsilon_H) is the worst-case relative Hamiltonian drift "
            "across the held-out test trajectories: `max_t |(H(t) - H(0)) / "
            "H(0)|`, computed on detached CPU float64 tensors with the Plummer "
            "softening `eps_inv = 1e-10` (distinct from the training-time "
            "softening). A smaller value means the model's predicted "
            "trajectory conserves energy more closely to that trajectory's "
            "own initial energy."
        ),
        "",
        (
            "SCS (Scaled Conservation Score) is `log10(ε_H)`; a smaller "
            "(more negative) SCS is better. The gate REJECTS if `ε_H > "
            "1e-5` (equivalently `SCS > -5`); the boundary itself PASSES "
            "(strict-inequality reject)."
        ),
        "",
    ]
    atomic_write_text(path, "\n".join(lines) + "\n")


def _write_receipt(
    path: Path, *, run_dir: Path, checkpoint_path: Path, aggregate, stamp,
) -> None:
    payload = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "run_dir": str(run_dir),
        "checkpoint_path": str(checkpoint_path),
        "checkpoint_sha256": _sha256_file(checkpoint_path),
        "config_sha256": _sha256_file(run_dir / "config.yaml"),
        "splits_sha256": _sha256_file(run_dir / "splits.json"),
        "timestamp": stamp.isoformat(),
        "verdict": aggregate.verdict,
        "eps_h": _json_safe_float(aggregate.eps_h),
        "scs": _json_safe_float(aggregate.scs),
    }
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pinn.evaluate",
        description=(
            "Run the ACC-03 one-time held-out evaluation and render the "
            "authoritative post-v1.3 binary gate to metrics.json/metrics.md."
        ),
    )
    parser.add_argument(
        "--checkpoint", required=True, type=Path, help="checkpoint file to evaluate",
    )
    parser.add_argument(
        "--output", required=True, type=Path,
        help="runs-rooted output directory for metrics/receipt artifacts",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry — returns 0 on a completed evaluation (PASS or FAIL gate),
    non-zero on a refusal (empty test set, ownership, path escape, rerun,
    or a malformed frozen input)."""
    args = _parser().parse_args(list(argv) if argv is not None else None)
    try:
        outcome = evaluate_run(checkpoint_path=args.checkpoint, output_dir=args.output)
    except (
        CheckpointOwnershipError,
        OutputPathEscapeError,
        EmptyTestSetError,
        EvaluationReceiptExistsError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # malformed frozen inputs fail honestly, not a crash
        print(f"error: evaluation failed: {exc}", file=sys.stderr)
        return 1

    print(f"metrics: {outcome.metrics_path}")
    print(f"OVERALL: {outcome.verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
