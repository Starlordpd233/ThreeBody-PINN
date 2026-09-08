"""Independent Phase-57 production-path conformance verifier.

This verifier is intentionally separate from ``tests/phase57`` and from the
implementation modules it checks.  It builds a deterministic in-memory
StageQuery, loads the committed Phase-57 configuration and governed ``R_ref``,
then exercises the public batch/controller/loss/checkpoint seams on CPU.  It
does not read ``simulation_data``, launch ``pinn.train``, or access a held-out
split.

The verifier is an evidence producer, not a second implementation of the
causal arithmetic or allocation.  Allocation and loss values are obtained
from ``pinn.data.batches`` and ``RunController``; this module only validates
their observable shape, provenance, gradients, and immutable state.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.data.types import RecordKey, StageLabel
from pinn.network import build_network
from pinn.runtime import resolve_runtime
from pinn.training.atomic_io import atomic_write_text
from pinn.training.checkpoint import CHECKPOINT_SCHEMA_VERSION, TorchSaveCheckpointStore
from pinn.training.collocation_sampler import CollocationSampler
from pinn.training.config import load_frozen_r_ref_artifact
from pinn.training.config_yaml import load_config
from pinn.training.controllers import RunController, build_checkpoint_payload
from pinn.training.grad_clip import GradClipper
from pinn.training.scheduled_weights import ScheduledWeights
from pinn.training.stage_exit import StageExitMachine
from pinn.verification.architecture_characterization_probe import (
    RATIFIED_N_BINS,
    RATIFIED_PER_BIN,
    RATIFIED_TOTAL,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "stage0-v23-seed42.yaml"
DEFAULT_R_REF_PATH = REPO_ROOT / "pinn" / "verification" / "artifacts" / "r_ref_stage0.json"
DEFAULT_GATE_EVIDENCE_ROOT = (
    REPO_ROOT
    / ".planning"
    / "phases"
    / "57-corrected-re-run-the-preserved-evaluation"
    / "evidence"
    / "gate04"
)
PRODUCTION_SCHEMA_VERSION = "phase57-production-conformance/v1"
GATE_SCHEMA_VERSION = "phase56-gate04-cli-evidence/v1"
REQUIRED_GATE_LABELS = ("41", "42", "43", "0", "7", "41-variable-mass")


class ConformanceFailure(RuntimeError):
    """A production-path or provenance fact failed closed."""


def _fail(message: str) -> None:
    raise ConformanceFailure(f"phase57 production conformance FAIL-CLOSED: {message}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonable(value: Any) -> Any:
    if isinstance(value, torch.Tensor):
        return {
            "tensor": True,
            "dtype": str(value.dtype),
            "shape": list(value.shape),
            "device": str(value.device),
            "bytes": value.detach().cpu().contiguous().numpy().tobytes().hex(),
        }
    if isinstance(value, Mapping):
        return {str(key): _jsonable(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return {
            "ndarray": True,
            "dtype": str(value.dtype),
            "shape": list(value.shape),
            "bytes": np.ascontiguousarray(value).tobytes().hex(),
        }
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _digest(value: Any) -> str:
    encoded = json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _finite_float(value: Any, *, name: str) -> float:
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        _fail(f"{name} is not numeric: {value!r}")
        raise AssertionError from exc
    if not math.isfinite(converted):
        _fail(f"{name} is not finite: {value!r}")
    return converted


def _resolve_repo_path(raw: str | Path, *, what: str) -> Path:
    supplied = Path(raw)
    resolved = supplied if supplied.is_absolute() else REPO_ROOT / supplied
    resolved = resolved.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        _fail(f"{what} escapes the repository: {raw!r}")
    if resolved.is_symlink():
        _fail(f"{what} is a symlink: {raw!r}")
    return resolved


def _gate_raw_for_artifact(r_ref_path: Path, gate_root: Path) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    if not r_ref_path.is_file():
        _fail(f"governed R_ref artifact is missing: {r_ref_path}")
    try:
        artifact = json.loads(r_ref_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"governed R_ref artifact is unreadable: {exc}")
    if not isinstance(artifact, Mapping):
        _fail("governed R_ref artifact is not a JSON object")
    provenance = artifact.get("provenance")
    if not isinstance(provenance, Mapping):
        _fail("governed R_ref artifact has no provenance object")
    recorded_path = provenance.get("gate_evidence_path")
    recorded_digest = provenance.get("gate_evidence_sha256")
    if not isinstance(recorded_path, str) or not recorded_path:
        _fail("governed R_ref artifact does not identify Gate raw evidence")
    if not isinstance(recorded_digest, str) or len(recorded_digest) != 64:
        _fail("governed R_ref artifact has no valid Gate raw-evidence digest")
    raw_path = Path(recorded_path)
    if not raw_path.is_absolute():
        raw_path = (REPO_ROOT / raw_path).resolve()
    else:
        raw_path = raw_path.resolve()
    try:
        raw_path.relative_to(gate_root.resolve())
    except ValueError:
        _fail(f"artifact Gate raw evidence is outside the supplied root: {raw_path}")
    if not raw_path.is_file():
        _fail(f"artifact Gate raw evidence is missing: {raw_path}")
    actual_digest = _sha256(raw_path)
    if actual_digest != recorded_digest:
        _fail(
            "governed R_ref artifact Gate raw-evidence digest mismatch: "
            f"recorded {recorded_digest}, actual {actual_digest}"
        )
    try:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"Gate raw evidence is unreadable: {exc}")
    if not isinstance(raw, Mapping) or raw.get("schema_version") != GATE_SCHEMA_VERSION:
        _fail("Gate raw evidence schema mismatch")
    if raw.get("failure") is not None:
        _fail("Gate raw evidence reports a measurement failure")
    verdict = raw.get("verdict")
    if not isinstance(verdict, Mapping):
        _fail("Gate raw evidence has no verdict object")
    if verdict.get("verdict") != "PASS":
        _fail(f"Gate raw evidence verdict is not PASS: {verdict.get('verdict')!r}")
    if verdict.get("blocking_reasons") != [] or verdict.get("unratified_conditions") != []:
        _fail("Gate raw evidence is not a complete PASS")
    cases = raw.get("cases")
    if not isinstance(cases, list) or len(cases) != len(REQUIRED_GATE_LABELS):
        _fail(f"Gate raw evidence must contain exactly six cases, got {len(cases or [])}")
    labels = tuple(case.get("label") for case in cases if isinstance(case, Mapping))
    if labels != REQUIRED_GATE_LABELS:
        _fail(f"Gate raw evidence labels/order mismatch: {labels!r}")
    if provenance.get("gate_case_count") not in (None, len(REQUIRED_GATE_LABELS)):
        _fail("governed artifact Gate case count disagrees with the six-case record")
    if provenance.get("gate_case_labels") not in (None, list(REQUIRED_GATE_LABELS)):
        _fail("governed artifact Gate case labels disagree with raw evidence")
    if provenance.get("gate_verdict") not in (None, "PASS"):
        _fail("governed artifact Gate verdict disagrees with raw evidence")
    if artifact.get("valid") is not True:
        _fail("governed R_ref artifact is not marked valid")
    return raw_path, dict(raw), dict(artifact)


class _SyntheticStageQuery:
    """Deterministic in-memory StageQuery with disjoint training identities."""

    def __init__(self) -> None:
        self._stage0 = tuple(
            RecordKey("hierarchical", "base", index) for index in range(240)
        )
        self._stage1 = tuple(
            RecordKey("hierarchical", "base", 10_000 + index) for index in range(16)
        )

    @property
    def blacklisted_physical_keys(self):
        return frozenset()

    @property
    def gold_numeric_stage_count(self):
        return 0

    def has_stage(self, stage: int) -> bool:
        return {0: bool(self._stage0), 1: bool(self._stage1)}.get(stage, False)

    def records_at(self, stage: int):
        return self._stage0 if stage == 0 else self._stage1 if stage == 1 else ()

    def records_at_or_below(self, stage: int):
        if stage <= 0:
            return self._stage0
        return self._stage0 + self._stage1

    def record_keys(self):
        return self._stage0 + self._stage1

    def get(self, key: RecordKey):
        return SimpleNamespace(
            record_key=key,
            physical_key=key.physical_key,
            stage_label=self.stage_label(key),
            n_snapshots=self.n_snapshots(key),
            # Identity-dependent IC/mass values make accidental anchor-only
            # paths observable without reading a corpus file.
            ic13=np.linspace(0.0, 1.2, 13, dtype=np.float64) + key.id / 10_000.0,
            masses=np.array([1.0 + key.id / 10_000.0, 2.0, 3.0], dtype=np.float64),
        )

    def n_snapshots(self, _key: RecordKey) -> int:
        return 24

    def snapshot_times(self, _key: RecordKey):
        return np.linspace(0.0, 9.5, self.n_snapshots(_key), dtype=np.float64)

    def snapshot_positions(self, key: RecordKey):
        times = self.snapshot_times(key)
        positions = np.zeros((times.size, 3, 3), dtype=np.float64)
        positions[:, 0, 0] = times + key.id / 1000.0
        positions[:, 1, 1] = 2.0 * times
        positions[:, 2, 2] = -times
        return positions

    def snapshot_velocities(self, _key: RecordKey):
        times = self.snapshot_times(_key)
        velocities = np.zeros((times.size, 3, 3), dtype=np.float64)
        velocities[:, 0, 0] = times**2
        velocities[:, 1, 1] = times
        return velocities

    def acceleration_magnitudes(self, _key: RecordKey):
        return np.arange(1, self.n_snapshots(_key) + 1, dtype=np.float64)

    def stage_label(self, key: RecordKey):
        if key in self._stage0:
            return StageLabel.STAGE_0
        if key in self._stage1:
            return StageLabel.STAGE_1
        return StageLabel.UNASSIGNED

    def is_blacklisted(self, _physical_key):
        return False


def _config_for_cpu(config):
    run = dataclasses.replace(config.run, precision="float64", device="cpu")
    return dataclasses.replace(config, run=run)


def _build_controller(config, source, r_ref: float, root: Path) -> RunController:
    runtime = resolve_runtime("float64", "cpu")
    model = build_network(
        ArchitectureSpec(seed=int(config.run.seed)),
        dtype=runtime.dtype,
        device=runtime.torch_device,
    )
    scheduled = ScheduledWeights(int(config.stage.n_adam))
    clipper = GradClipper()
    sampler = CollocationSampler(2, np.random.default_rng(int(config.run.seed) + 1000))
    exit_machine = StageExitMachine(config)
    store = TorchSaveCheckpointStore(root)
    return RunController(
        model,
        source,
        source,
        config,
        scheduled,
        clipper,
        sampler,
        exit_machine,
        store,
        runtime,
        s_h=1.0,
        rng=np.random.default_rng(int(config.run.seed)),
        replay_count=int(config.stage.replay_count or 240),
        r_ref=r_ref,
    )


def _global_grad_norm(model) -> float:
    squared = 0.0
    for parameter in model.parameters():
        if parameter.grad is not None:
            squared += float(torch.sum(parameter.grad.detach() ** 2))
    return math.sqrt(squared)


def _assert_condition(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def run_verification(
    *,
    r_ref_path: Path = DEFAULT_R_REF_PATH,
    gate_evidence_root: Path = DEFAULT_GATE_EVIDENCE_ROOT,
    output: Path,
) -> dict[str, Any]:
    r_ref_path = _resolve_repo_path(r_ref_path, what="R_ref artifact")
    gate_root = _resolve_repo_path(gate_evidence_root, what="Gate evidence root")
    raw_path, gate_raw, artifact = _gate_raw_for_artifact(r_ref_path, gate_root)
    r_ref = _finite_float(artifact.get("r_ref"), name="artifact.r_ref")
    loaded_r_ref = _finite_float(load_frozen_r_ref_artifact(r_ref_path), name="loaded R_ref")
    _assert_condition(loaded_r_ref == r_ref, "R_ref loader value disagrees with artifact")
    config_path = DEFAULT_CONFIG_PATH
    config = _config_for_cpu(load_config(config_path))
    _assert_condition(config.run.seed == 42, "verifier config is not the pre-registered seed-42 config")
    _assert_condition(config.stage.collocation_count == RATIFIED_TOTAL, "config does not bind collocation_count=4096")
    _assert_condition(config.stage.replay_count == 240, "config does not bind replay_count=240")
    _assert_condition(
        config.run.invariants.front_advance_window_n == 500,
        "config does not bind front_advance_window_n=500",
    )
    _assert_condition(
        config.loss.r_ref_artifact_path == "pinn/verification/artifacts/r_ref_stage0.json",
        "config R_ref path does not match the governed artifact",
    )

    source = _SyntheticStageQuery()
    synthetic_source_id = "phase57-synthetic-stagequery-v1"
    with tempfile.TemporaryDirectory(prefix="phase57-conformance-") as tmp:
        tmp_root = Path(tmp)
        controller = _build_controller(config, source, r_ref, tmp_root / "checkpoint-a")
        monitor_before = controller.front_monitor_state
        monitor_hash_before = _digest(monitor_before)
        monitor_rows = int(monitor_before.get("n_collocation_rows", -1))
        monitor_bins = int(monitor_before.get("n_bins", -1))
        monitor_keys = tuple(tuple(key) for key in monitor_before.get("record_keys", ()))
        _assert_condition(monitor_before.get("enabled") is True, "front monitor is not enabled")
        _assert_condition(monitor_before.get("split") == "train", "front monitor is not training-only")
        _assert_condition(monitor_rows == RATIFIED_TOTAL, "front monitor row count is not 4096")
        _assert_condition(monitor_bins == RATIFIED_N_BINS, "front monitor bin count is not 16")
        _assert_condition(len(monitor_keys) == RATIFIED_TOTAL, "front monitor lacks per-row identity provenance")
        _assert_condition(
            int(config.run.invariants.front_advance_window_n) != monitor_rows,
            "front_advance_window_n was conflated with monitor cardinality",
        )
        _assert_condition(
            all(key[0] == "hierarchical" and key[1] == "base" for key in monitor_keys),
            "front monitor contains a non-training/non-base key",
        )

        batch = controller._stage_batch(
            source, stage=0, collocation_count=RATIFIED_TOTAL,
        )
        collocation = batch.collocation_points
        row_count = int(collocation.times.numel())
        selected_slot_keys = tuple(batch.replay_keys) + tuple(batch.lookahead_keys)
        _assert_condition(row_count == RATIFIED_TOTAL, "production batch did not emit exactly 4096 rows")
        _assert_condition(len(selected_slot_keys) == 256, "production batch did not select 256 slots")
        _assert_condition(len(collocation.record_keys) == row_count, "collocation row provenance is incomplete")
        unique_bins = []
        for time_value in collocation.times.detach().cpu().tolist():
            normalized = float(time_value) / 10.0
            unique_bins.append(min(15, int(math.floor(max(0.0, normalized) * RATIFIED_N_BINS))))
        bin_counts = [unique_bins.count(index) for index in range(RATIFIED_N_BINS)]
        _assert_condition(
            bin_counts == [RATIFIED_PER_BIN] * RATIFIED_N_BINS,
            f"production batch bin counts are not exact 16x256: {bin_counts}",
        )
        _assert_condition(
            len(set(collocation.record_keys)) > 1,
            "production batch collapsed to one anchor identity",
        )

        anchor_context = controller._build_anchor_context(source, batch, None)
        controller.model.zero_grad(set_to_none=True)
        terms = controller._non_data_terms(anchor_context)
        phys_loss = terms["phys"]
        _assert_condition(bool(torch.isfinite(phys_loss)), "production normalized physics loss is non-finite")
        _assert_condition(bool(phys_loss.requires_grad), "production physics loss detached the model graph")
        phys_loss.backward()
        gradient_norm = _global_grad_norm(controller.model)
        _assert_condition(math.isfinite(gradient_norm) and gradient_norm > 0.0, "production physics gradients are absent or non-finite")
        details = controller._last_widened_details or {}
        raw_bins = tuple(float(value) for value in details.get("raw_residuals_per_bin", ()))
        normalized_bins = tuple(float(value) for value in details.get("residuals_per_bin", ()))
        weights = tuple(float(value) for value in details.get("weights", ()))
        _assert_condition(len(raw_bins) == RATIFIED_N_BINS, "raw production residual bins are incomplete")
        _assert_condition(len(normalized_bins) == RATIFIED_N_BINS, "normalized production residual bins are incomplete")
        _assert_condition(len(weights) == RATIFIED_N_BINS, "production causal weights are incomplete")
        _assert_condition(
            all(math.isfinite(a) and math.isfinite(b) for a, b in zip(raw_bins, normalized_bins)),
            "production raw/normalized residual diagnostics are non-finite",
        )
        _assert_condition(
            all(math.isclose(b, a / r_ref, rel_tol=1e-12, abs_tol=1e-12) for a, b in zip(raw_bins, normalized_bins)),
            "production normalized residual bins do not use the governed R_ref",
        )
        details_r_ref = _finite_float(details.get("r_ref"), name="production details.r_ref")
        _assert_condition(details_r_ref == r_ref, "production loss used a different R_ref")
        _assert_condition(int(details.get("n_collocation_rows", -1)) == RATIFIED_TOTAL, "production diagnostics row count mismatch")
        _assert_condition(int(details.get("n_bins", -1)) == RATIFIED_N_BINS, "production diagnostics bin count mismatch")
        monitor_hash_after_loss = _digest(controller.front_monitor_state)
        _assert_condition(monitor_hash_after_loss == monitor_hash_before, "front monitor changed during loss evaluation")

        # Start the real segment and invoke one real L-BFGS closure without
        # calling optimizer.step: this proves fixed samples/weights are used
        # against a live trial graph, without turning the verifier into a run.
        fixed_batch, fixed_context, frozen_weights = controller._start_lbfgs_segment(0, lbfgs_start=0)
        segment_state_before = controller.state_dict()["lbfgs_segment_state"]
        segment_hash_before = _digest(segment_state_before)
        frozen_hash_before = _digest(frozen_weights)
        optimizer = torch.optim.LBFGS(controller.model.parameters(), max_iter=1, line_search_fn="strong_wolfe")
        closure_state: dict[str, Any] = {"non_finite": False, "last_loss": None, "gradient_stats": None}
        closure = controller._make_lbfgs_closure(
            optimizer,
            fixed_batch,
            fixed_context,
            controller.scheduled_weights.current(0),
            int(config.opt.lbfgs_chunk_size),
            closure_state,
        )
        closure_result = closure()
        _assert_condition(bool(torch.isfinite(closure_result)), "L-BFGS production closure returned a non-finite loss")
        _assert_condition(closure_state.get("gradient_stats") is not None, "L-BFGS production closure emitted no gradient stats")
        segment_state_after = controller.state_dict()["lbfgs_segment_state"]
        _assert_condition(_digest(segment_state_after) == segment_hash_before, "L-BFGS segment state mutated during a trial closure")
        _assert_condition(_digest(frozen_weights) == frozen_hash_before, "L-BFGS frozen weights mutated during a trial closure")
        _assert_condition(
            segment_state_before.get("samples_hash") == segment_state_before.get("weights_hash")
            or isinstance(segment_state_before.get("samples_hash"), str),
            "L-BFGS segment hashes are absent",
        )

        invariant_b_state = {
            "front_advance_window_n": int(config.run.invariants.front_advance_window_n),
            "front_high_water": int((controller.front_monitor_state.get("stage") or 0)),
            "last_advancement_step": 0,
        }
        payload = build_checkpoint_payload(
            controller,
            curriculum_state={"stage": 0},
            config_identity={"config_sha256": _sha256(config_path)},
            schema_version=CHECKPOINT_SCHEMA_VERSION,
            invariant_b_state=invariant_b_state,
        )
        checkpoint_store = controller.checkpoint_store
        checkpoint_store.save(payload)
        restored_payload = checkpoint_store.load_latest()
        restored = _build_controller(config, source, r_ref, tmp_root / "checkpoint-b")
        restored.load_state_dict(restored_payload)
        _assert_condition(
            _digest(restored.front_monitor_state) == monitor_hash_before,
            "checkpoint/resume did not restore the exact front monitor bytes",
        )
        _assert_condition(
            _digest(restored.state_dict()["lbfgs_segment_state"]) == segment_hash_before,
            "checkpoint/resume did not restore the exact L-BFGS segment bytes",
        )
        _assert_condition(
            restored.state_dict()["front_monitor"].get("split") == "train",
            "checkpoint/resume restored a non-training front monitor",
        )
        resume_hash = _digest(restored.state_dict())
        record = {
            "schema_version": PRODUCTION_SCHEMA_VERSION,
            "status": "PASS",
            "evaluation": "preserved-unspent",
            "source": {
                "id": synthetic_source_id,
                "training_only": True,
                "held_out_accessed": False,
                "n_stage0": 240,
                "n_stage1": 16,
            },
            "config": {
                "path": str(config_path.relative_to(REPO_ROOT)),
                "sha256": _sha256(config_path),
                "seed": int(config.run.seed),
                "run_name": config.run.run_name,
                "precision": config.run.precision,
                "device": config.run.device,
                "cpu_override": True,
                "collocation_count": int(config.stage.collocation_count),
                "replay_count": int(config.stage.replay_count),
                "front_advance_window_n": int(config.run.invariants.front_advance_window_n),
            },
            "allocation": {
                "n_rows": row_count,
                "n_bins": RATIFIED_N_BINS,
                "rows_per_bin": RATIFIED_PER_BIN,
                "bin_counts": bin_counts,
                "selected_slots": len(selected_slot_keys),
                "unique_emitted_slots": len(set(collocation.record_keys)),
                "anchor_only": False,
            },
            "loss": {
                "raw_residuals_per_bin": list(raw_bins),
                "normalized_residuals_per_bin": list(normalized_bins),
                "weights": list(weights),
                "r_ref": r_ref,
                "r_ref_sha256": _sha256(r_ref_path),
                "physics_loss": float(phys_loss.detach()),
                "normalization_verified": True,
                "gradients": {
                    "physics_loss_requires_grad": True,
                    "global_l2_norm": gradient_norm,
                    "finite": True,
                    "nonzero": True,
                },
            },
            "front_monitor": {
                "schema_version": monitor_before.get("schema_version"),
                "split": monitor_before.get("split"),
                "n_rows": monitor_rows,
                "n_bins": monitor_bins,
                "hash": monitor_hash_before,
                "unchanged_after_loss": monitor_hash_after_loss == monitor_hash_before,
                "independent_window_n": int(config.run.invariants.front_advance_window_n),
                "monitor_window_conflated": False,
            },
            "lbfgs_segment": {
                "schema_version": segment_state_before.get("schema_version"),
                "samples_hash": segment_state_before.get("samples_hash"),
                "weights_hash": segment_state_before.get("weights_hash"),
                "frozen_weights_hash": segment_state_before.get("frozen_weights_hash"),
                "state_hash_before_closure": segment_hash_before,
                "state_hash_after_closure": _digest(segment_state_after),
                "immutable_during_closure": True,
                "closure_gradient_stats": _jsonable(closure_state.get("gradient_stats")),
            },
            "checkpoint_resume": {
                "schema_version": CHECKPOINT_SCHEMA_VERSION,
                "payload_keys": sorted(payload),
                "monitor_hash": monitor_hash_before,
                "segment_hash": segment_hash_before,
                "restored_monitor_hash": _digest(restored.front_monitor_state),
                "restored_segment_hash": _digest(restored.state_dict()["lbfgs_segment_state"]),
                "exact_monitor_restore": True,
                "exact_segment_restore": True,
                "restored_state_digest": resume_hash,
            },
            "gate_provenance": {
                "raw_path": str(raw_path.relative_to(REPO_ROOT)),
                "raw_sha256": _sha256(raw_path),
                "schema_version": gate_raw.get("schema_version"),
                "verdict": gate_raw.get("verdict"),
                "case_count": len(gate_raw.get("cases", [])),
                "case_labels": list(REQUIRED_GATE_LABELS),
                "artifact_sha256": _sha256(r_ref_path),
            },
            "provenance": {
                "git_head": _git_head(),
                "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "python": sys.version.split()[0],
                "torch": torch.__version__,
                "numpy": np.__version__,
                "training_launched": False,
                "held_out_evaluation_launched": False,
            },
        }
    atomic_write_text(output, json.dumps(record, sort_keys=True, indent=2) + "\n")
    return record


def _git_head() -> str | None:
    try:
        import subprocess

        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="python -m pinn.verification.phase57_production_conformance")
    parser.add_argument("--r-ref-path", type=Path, default=DEFAULT_R_REF_PATH)
    parser.add_argument("--gate-evidence-root", type=Path, default=DEFAULT_GATE_EVIDENCE_ROOT)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = _parse_args(argv)
    try:
        output = _resolve_repo_path(args.output, what="conformance output")
        record = run_verification(
            r_ref_path=args.r_ref_path,
            gate_evidence_root=args.gate_evidence_root,
            output=output,
        )
    except Exception as exc:  # noqa: BLE001 - CLI must report a nonzero fail-closed result
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"status={record['status']}")
    print(f"output={output}")
    print(f"r_ref_sha256={record['loss']['r_ref_sha256']}")
    print(f"gate_raw_sha256={record['gate_provenance']['raw_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
