"""Phase 59 DIAG-07: shared driver library for the read-only generation-7 checkpoint experiments.

No pinn import at module import time. Call bootstrap before any other pinn import.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
GEN7_COMMIT = "629b1a6ca4462915b6340a59b8d4e3ad8df75d8b"
OVERLAY_MODULES = (
    "pinn.verification.feasibility_scorecard",
    "pinn.verification.evidence_io",
    "pinn.verification.split_allowlist",
    "pinn.verification.production_reference",
    "pinn.verification.feasibility_scorer",
)
SEED42 = "stage0-v23g7-seed42"
SMOKE = "stage0-v23g7-smoke"
_COMMON_REL = (
    ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py"
)
_OVERLAY_REL = {
    "pinn.verification.feasibility_scorecard": "pinn/verification/feasibility_scorecard.py",
    "pinn.verification.evidence_io": "pinn/verification/evidence_io.py",
    "pinn.verification.split_allowlist": "pinn/verification/split_allowlist.py",
    "pinn.verification.production_reference": "pinn/verification/production_reference.py",
    "pinn.verification.feasibility_scorer": "pinn/verification/feasibility_scorer.py",
}
_RESULT_KEYS = (
    "schema",
    "experiment",
    "plain_language",
    "command",
    "code_identity",
    "runtimes",
    "checkpoints",
    "scorecard_sha256",
    "results",
    "reading",
    "tolerance_checks",
    "memory",
    "non_interference",
    "files_opened",
    "producer_sha256",
)


class CheckpointWriteRefused(RuntimeError):
    """A measurement tried to write a checkpoint."""


class RefusingCheckpointStore:
    """Checkpoint store whose every write and load method refuses."""

    def __init__(self) -> None:
        self.write_attempts = 0

    def _refuse(self) -> None:
        self.write_attempts += 1
        raise CheckpointWriteRefused("checkpoint write refused")

    def save(self, *_args, **_kwargs):
        self._refuse()

    def save_rolling(self, *_args, **_kwargs):
        self._refuse()

    def save_best(self, *_args, **_kwargs):
        self._refuse()

    def save_anchor(self, *_args, **_kwargs):
        self._refuse()

    def promote(self, *_args, **_kwargs):
        self._refuse()

    def record_disposition(self, *_args, **_kwargs):
        self._refuse()

    def load_latest(self, *_args, **_kwargs):
        self._refuse()

    def load_checkpoint(self, *_args, **_kwargs):
        self._refuse()

    def rollback(self, *_args, **_kwargs):
        self._refuse()

    def fallback_scan(self, *_args, **_kwargs):
        self._refuse()

    def should_checkpoint(self, *_args, **_kwargs) -> bool:
        return False


def _under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _git_blob(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(path) -> str:
    file = Path(path)
    if file.is_absolute():
        return file.resolve().relative_to(REPO_ROOT).as_posix()
    return file.as_posix()


def verify_snapshot(code_root, repo_root) -> dict:
    """Return the snapshot digest after every pinn and configs blob matches."""
    code_root = Path(code_root).resolve()
    repo_root = Path(repo_root).resolve()
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", "-r", GEN7_COMMIT, "--", "pinn", "configs"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git ls-tree failed")
    listed = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        listed[path] = meta.split()[2]
    for path, blob in listed.items():
        file = code_root / path
        if not file.is_file():
            raise RuntimeError(f"snapshot missing {path}")
        actual = _git_blob(file.read_bytes())
        if actual != blob:
            raise RuntimeError(f"snapshot blob mismatch for {path}")
    extras = []
    for folder in ("pinn", "configs"):
        root = code_root / folder
        if not root.is_dir():
            raise RuntimeError(f"snapshot missing {folder}")
        for file in root.rglob("*"):
            if not file.is_file() or file.is_symlink():
                continue
            if "__pycache__" in file.parts or file.suffix == ".pyc":
                continue
            relative = file.relative_to(code_root).as_posix()
            if relative not in listed:
                extras.append(relative)
    if extras:
        raise RuntimeError("snapshot has extra files: " + ", ".join(sorted(extras)[:8]))
    lines = [f"{path} {listed[path]}" for path in sorted(listed)]
    digest = hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()
    return {
        "commit": GEN7_COMMIT,
        "snapshot_files": len(listed),
        "snapshot_digest": digest,
    }


def _overlay_path(repo_root: Path, name: str) -> Path:
    leaf = name.rsplit(".", 1)[1]
    return repo_root / "pinn" / "verification" / f"{leaf}.py"


def bootstrap(code_root, repo_root) -> dict:
    """Put the snapshot first on sys.path and load the five repository overlays."""
    code_root = Path(code_root).resolve()
    repo_root = Path(repo_root).resolve()
    loaded = [
        name for name in sys.modules
        if name == "pinn" or name.startswith("pinn.")
    ]
    if loaded:
        raise RuntimeError("pinn is already imported")
    identity = verify_snapshot(code_root, repo_root)
    sys.path.insert(0, str(code_root))
    import pinn

    if not _under(Path(pinn.__file__).resolve(), code_root):
        raise RuntimeError("pinn.__file__ is not under the snapshot")
    overlays = {}
    for name in OVERLAY_MODULES:
        path = _overlay_path(repo_root, name)
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load overlay {name}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        parent = sys.modules.get("pinn.verification")
        if parent is not None:
            setattr(parent, name.rsplit(".", 1)[1], module)
        spec.loader.exec_module(module)
        overlays[name] = _sha256_file(path)
    from pinn.verification.feasibility_scorecard import load_scorecard

    expected = set(load_scorecard().section("diag07")["overlay_modules"])
    if set(OVERLAY_MODULES) != expected:
        raise RuntimeError("overlay set does not match the scorecard")
    identity["pinn_module_root"] = "code_root"
    identity["overlay_modules"] = overlays
    return identity


def assert_module_provenance(code_root, repo_root, overlay) -> None:
    """Refuse a pinn module that is neither snapshot code nor a known overlay."""
    code_root = Path(code_root).resolve()
    repo_root = Path(repo_root).resolve()
    del overlay
    overlay_files = {
        name: _overlay_path(repo_root, name).resolve() for name in OVERLAY_MODULES
    }
    for name, module in list(sys.modules.items()):
        if module is None or not (name == "pinn" or name.startswith("pinn.")):
            continue
        file = getattr(module, "__file__", None)
        if name in overlay_files:
            if file is None or Path(file).resolve() != overlay_files[name]:
                raise RuntimeError(f"{name} is not the repository overlay")
            continue
        if file is None:
            paths = [Path(item).resolve() for item in getattr(module, "__path__", [])]
            if paths and all(_under(item, code_root) for item in paths):
                continue
            raise RuntimeError(f"{name} has no file under the snapshot")
        if not _under(Path(file).resolve(), code_root):
            raise RuntimeError(f"{name} loaded from outside the snapshot")


def _as_step(value) -> float:
    import torch

    if torch.is_tensor(value):
        flat = value.detach().cpu().reshape(-1)
        if int(flat.numel()) != 1:
            raise ValueError("adam step is not scalar")
        return float(flat[0])
    return float(value)


def load_registry_checkpoint(repo_root, run, file_name, *, scorecard):
    """Load one retention-pinned checkpoint and require every Adam step."""
    from pinn.verification.production_reference import load_retained_checkpoint

    expected = int(scorecard.section("diag07")["checkpoints"][run][file_name])
    payload, provenance = load_retained_checkpoint(
        repo_root, run, file_name, expected_step=expected,
    )
    provenance = dict(provenance)
    optimizer = payload.get("optimizer")
    if optimizer is None:
        provenance["adam_step"] = None
        return payload, provenance
    steps = []
    for entry in (optimizer.get("state") or {}).values():
        step = _as_step(entry.get("step"))
        if step != float(expected):
            raise ValueError(f"adam step {step} != expected {expected}")
        steps.append(step)
    provenance["adam_step"] = steps[0] if steps else None
    return payload, provenance


def build_sources(repo_root, data_root, data_root_source, scorecard) -> dict:
    """Allowlisted stage 0 and 1 resident records and the recovered normalizer."""
    from pinn.data.splits import StageIndex
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.production_reference import (
        NormalizerRecoveryError,
        fallback_normalizer_from_allowlist,
        load_reference,
        recover_normalizer_from_checkpoint,
        resident_record,
        stats_digest,
    )
    from pinn.verification.split_allowlist import (
        GENERATION7_SPLITS_REL,
        AllowlistedCorpusReader,
        SplitAllowlist,
        expected_splits_sha256,
        install_open_attestation,
    )

    del load_scorecard
    repo_root = Path(repo_root)
    data_root = Path(data_root)
    allowlist = SplitAllowlist.from_manifest(
        repo_root / GENERATION7_SPLITS_REL,
        expected_sha256=expected_splits_sha256(repo_root),
    )
    reader = AllowlistedCorpusReader(
        allowlist=allowlist,
        data_root=data_root,
        data_root_source=data_root_source,
    )
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=data_root_source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    init_payload, _init_provenance = load_registry_checkpoint(
        repo_root, SEED42, "stage-0-init.pt", scorecard=scorecard,
    )
    tolerance = float(
        scorecard.section("diag07")["tolerances"]["normalizer_recovery_max_abs"]
    )
    deviation = False
    try:
        recovered = recover_normalizer_from_checkpoint(
            reader, init_payload, tolerance=tolerance,
        )
    except NormalizerRecoveryError:
        recovered = fallback_normalizer_from_allowlist(reader, allowlist)
        deviation = True
    stats = recovered["stats"]
    grouped = {"train": [], "validation": []}
    for split in ("train", "validation"):
        keys = []
        for stage in (0, 1):
            keys.extend(allowlist.records(
                split, variant="hierarchical", fidelity="base", stage=stage,
            ))
        print(f"loading {split} records {len(keys)}", file=sys.stderr, flush=True)
        for index, key in enumerate(keys, start=1):
            reference = load_reference(reader, key)
            grouped[split].append(resident_record(reference, stats))
            if index % 500 == 0:
                print(f"loaded {split} {index}", file=sys.stderr, flush=True)
    normalizer = {
        "stats_digest": stats_digest(stats),
        "residual": recovered.get("residual"),
        "source": recovered.get("source"),
        "deviation": deviation,
    }
    return {
        "train_index": StageIndex(grouped["train"]),
        "validation_index": StageIndex(grouped["validation"]),
        "reader": reader,
        "allowlist": allowlist,
        "attestation": attestation,
        "normalizer": normalizer,
        "stats": stats,
    }


def build_controller(code_root, repo_root, run, sources, runtime_pair):
    """Build one refusing RunController for a generation-7 run config."""
    import numpy as np

    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network
    from pinn.runtime import resolve_runtime
    from pinn.training.collocation_sampler import CollocationSampler
    from pinn.training.config import load_frozen_r_ref_artifact
    from pinn.training.config_yaml import load_config
    from pinn.training.controllers import RunController
    from pinn.training.grad_clip import GradClipper
    from pinn.training.scheduled_weights import ScheduledWeights
    from pinn.training.stage_exit import StageExitMachine

    code_root = Path(code_root)
    repo_root = Path(repo_root)
    config = load_config(code_root / "configs" / f"{run}.yaml")
    runtime = resolve_runtime(*runtime_pair)
    model = build_network(
        ArchitectureSpec(seed=int(config.run.seed)),
        dtype=runtime.dtype,
        device=runtime.torch_device,
    )
    metadata = json.loads((repo_root / "runs" / run / "training_metadata.json").read_text())
    r_ref = load_frozen_r_ref_artifact(code_root / config.loss.r_ref_artifact_path)
    store = RefusingCheckpointStore()
    controller = RunController(
        model,
        sources["train_index"],
        sources["validation_index"],
        config,
        ScheduledWeights(int(config.stage.n_adam)),
        GradClipper(),
        CollocationSampler(2, np.random.default_rng(int(config.run.seed) + 1000)),
        StageExitMachine(config),
        store,
        runtime,
        s_h=float(metadata["s_h"]),
        rng=np.random.default_rng(int(config.run.seed)),
        replay_count=int(config.stage.replay_count),
        r_ref=r_ref,
    )
    return controller


def monitor_fields(controller) -> dict:
    """Score the frozen monitor and derive the Phase 58 packet fields."""
    import numpy as np

    stats = controller._evaluate_front_monitor()
    rtilde = [float(value) for value in stats["residuals_per_bin"]]
    raw = [float(value) for value in stats["raw_residuals_per_bin"]]
    prefix = [0.0]
    for value in rtilde:
        prefix.append(prefix[-1] + float(value))
    front = int(stats["w_n_stats"]["front_idx"])
    through = prefix[front + 1] if front >= 0 else None
    following = prefix[front + 2] if front >= 0 and front + 2 <= len(rtilde) else None
    bins = rtilde[:6]
    median = float(np.median(np.asarray(rtilde, dtype=np.float64)))

    def rounded(value):
        if value is None:
            return None
        return round(float(value), 4)

    return {
        "front_idx": front,
        "rtilde": rtilde,
        "raw_rbar": raw,
        "prefix": prefix,
        "prefix_through_front": through,
        "prefix_to_cross_next": following,
        "rtilde_bins_0_5": bins,
        "raw_rbar_bin0": raw[0] if raw else None,
        "rtilde_median_all_bins": median,
        "w_min": float(stats["w_n_stats"]["w_min"]),
        "w_mean": float(stats["w_n_stats"]["w_mean"]),
        "w_max": float(stats["w_n_stats"]["w_max"]),
        "rounded": {
            "prefix_through_front": rounded(through),
            "prefix_to_cross_next": rounded(following),
            "rtilde_bins_0_5": [rounded(value) for value in bins],
            "rtilde_median_all_bins": rounded(median),
        },
    }


def param_fingerprints(model) -> list:
    """SHA-256 of each parameter's CPU bytes, in parameter order."""
    digests = []
    for parameter in model.parameters():
        array = parameter.detach().cpu().contiguous().numpy()
        digests.append(hashlib.sha256(array.tobytes()).hexdigest())
    return digests


def file_hashes(paths) -> dict:
    """SHA-256 of each path, keyed by the given path string."""
    return {str(path): _sha256_file(Path(path)) for path in paths}


def producer_hashes(driver_path) -> dict:
    """SHA-256 of this library, the driver, and the five overlay modules."""
    from pinn.verification import evidence_io

    paths = [_COMMON_REL, _relative(driver_path)]
    for name in OVERLAY_MODULES:
        paths.append(_OVERLAY_REL[name])
    return evidence_io.module_hashes(paths)


def _drop_stale_markers(evidence_root: Path, planned_results) -> None:
    planned = {str(name) for name in planned_results}
    for path in sorted(Path(evidence_root).glob("*.done.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        files = payload.get("result_files") if isinstance(payload, dict) else None
        if isinstance(files, dict) and planned.intersection(files):
            path.unlink()


def start_run(evidence_root, planned_results, *, label, command, required_bytes) -> dict:
    """Freeze, take the shared launch lock, preflight, then drop stale markers."""
    from pinn.verification import evidence_io

    evidence_io.require_frozen_scorecard()
    run_id = evidence_io.begin_long_step("diag07", label, command=command)
    try:
        preflight = evidence_io.memory_preflight(required_bytes)
    except evidence_io.MemoryPreflightError as exc:
        evidence_io.record_long_step_failure(str(exc), run_id=run_id)
        raise
    _drop_stale_markers(evidence_root, planned_results)
    return {
        "run_id": run_id,
        "preflight": preflight,
        "utc_started": datetime.now(timezone.utc).isoformat(),
        "monotonic_started": time.monotonic(),
    }


def finish_run(evidence_root, label, result_names, *, command, run_info) -> Path:
    """Write the completion marker, then release the launch lock."""
    from pinn.verification import evidence_io

    root = Path(evidence_root)
    finished = datetime.now(timezone.utc).isoformat()
    evidence_io.write_completion_marker(
        root,
        label,
        command=command,
        utc_started=run_info["utc_started"],
        utc_finished=finished,
        elapsed_seconds=time.monotonic() - float(run_info["monotonic_started"]),
        result_paths=[root / name for name in result_names],
        preflight=run_info["preflight"],
    )
    evidence_io.end_long_step(run_info["run_id"])
    return root / f"{label}.done.json"


def fail_run(run_info, reason) -> None:
    """Record a long-step failure and release the launch lock."""
    from pinn.verification import evidence_io

    evidence_io.record_long_step_failure(str(reason), run_id=run_info["run_id"])


def write_result(evidence_root, name, payload, *, data_root) -> str:
    """Write one diag07 result after the contract keys are present."""
    from pinn.verification import evidence_io

    missing = [key for key in _RESULT_KEYS if key not in payload]
    if missing:
        raise RuntimeError("diag07 result missing " + ", ".join(missing))
    producers = payload.get("producer_sha256")
    if not isinstance(producers, dict) or not producers:
        raise RuntimeError("diag07 result producer_sha256 is missing")
    return evidence_io.write_json(
        Path(evidence_root) / name, payload, data_root=data_root,
    )


def write_summary(evidence_root, *, data_root) -> None:
    """Rebuild summary.md from the result files. No timestamps."""
    from pinn.verification import evidence_io

    root = Path(evidence_root)
    paragraphs = []
    rows = []
    for path in sorted(root.glob("jx*.json")):
        if path.name.endswith(".done.json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        paragraphs.append(str(payload.get("plain_language") or "").strip())
        outcome = payload.get("reading", {}).get("outcome")
        if not isinstance(outcome, str):
            outcome = json.dumps(outcome, sort_keys=True, ensure_ascii=True)
        checkpoints = payload.get("checkpoints") or []
        names = []
        for item in checkpoints:
            if isinstance(item, dict) and item.get("file"):
                names.append(str(item["file"]))
        rows.append((str(payload.get("experiment")), outcome, ", ".join(names)))
    gate_path = root / "g1.json"
    if gate_path.is_file():
        gate = json.loads(gate_path.read_text(encoding="utf-8"))
        paragraphs.append(str(gate.get("plain_language") or "").strip())
        rows.append(("G1", str(gate.get("outcome")), "900, 951"))
    lines = ["## In plain language", ""]
    for paragraph in paragraphs:
        if paragraph:
            lines.append(paragraph)
            lines.append("")
    lines.extend([
        "## Readings",
        "",
        "| Experiment | Reading outcome | Checkpoints |",
        "| --- | --- | --- |",
    ])
    for experiment, outcome, checkpoints in rows:
        lines.append(f"| {experiment} | {outcome} | {checkpoints} |")
    lines.append("")
    evidence_io.write_text(root / "summary.md", "\n".join(lines), data_root=data_root)
