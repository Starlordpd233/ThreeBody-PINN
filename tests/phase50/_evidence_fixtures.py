"""Dataset-free Phase-50 evidence fixture factory.

Builds a temporary Git repository with a schema-valid ledger, historical
generations 1-3, one finished smoke, three finished graded seeds, ten
referenced sidecars per seed, D-29 stand-ins, and committed owner-summary
blobs. Used only by tests; no real corpus or training job is touched.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import sys
import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from pinn.training import validation_gate
from pinn.verification import gate_metrics

PHASE = Path(".planning/phases/50-valid-stage-0-re-run")
EVIDENCE = PHASE / "evidence"
LEDGER_REL = EVIDENCE / "run-ledger.md"
PRE_REG_REL = PHASE / "50-PRE-REGISTRATION.md"
CONFIG_DELTA_REL = PHASE / "50-CONFIG-DELTA.md"
AUTH_SUMMARY_REL = PHASE / "50-08-SUMMARY.md"
SMOKE_AUTH_REL = PHASE / "50-10-SUMMARY.md"
SOURCE_MANIFEST_REL = EVIDENCE / "source-manifest.json"
BAND_RECORD_REL = EVIDENCE / "band-record.md"
CANDIDATE_REL = EVIDENCE / "candidate-receipt.json"
FINAL_MANIFEST_REL = EVIDENCE / "manifest.json"
IDENTITY_BASELINE_REL = EVIDENCE / "identity-baseline-generation-4.json"

REPO_ROOT = Path(__file__).resolve().parents[2]
# The v2.3 milestone start (12e16d7b) archived Phase 50 under milestones/. Only
# the scripts' own location moved: they still resolve PHASE relative to the
# --repo-root they are given, and the fixture repositories keep that layout.
ARCHIVED_PHASE = Path(".planning/milestones/v2.2-phases/50-valid-stage-0-re-run")
BUILDER = REPO_ROOT / ARCHIVED_PHASE / "evidence" / "build_phase50_evidence.py"
VERIFIER = REPO_ROOT / ARCHIVED_PHASE / "evidence" / "verify_phase50_evidence.py"
PYTHON = sys.executable

CONFIG_PATHS = (
    "configs/stage0-rerun-smoke.yaml",
    "configs/stage0-rerun-seed41.yaml",
    "configs/stage0-rerun-seed42.yaml",
    "configs/stage0-rerun-seed43.yaml",
)
SCOPED_DRIFT_PATHS = (
    "pinn/",
    "configs/",
    "tests/phase50/",
    str(EVIDENCE),
    str(PHASE),
)
SELECTION_POLICY = {
    "allowed_transient_causes": ["disk_pressure", "external_memory_pressure"],
    "candidate_order": [42, 41, 43],
    "checkpoint_relative_path": "checkpoints/best.pt",
    "eligibility_facts": [
        "eval01_precondition_i == true",
        "final-attempt guard/invariant rule satisfied: no unresolved guard or invariant HALT at the final in-band attempt (an archived, positively-identified transient disk/external-memory HALT does not disqualify a later successful fresh attempt in the same generation; every scientific/invariant/loss-explosion/non-finite/intrinsic-memory/unknown HALT is terminal)",
        "final_process_disposition == 'finished' AND ledger_disposition == 'finished'",
        "eval01_precondition_iii == true AND independent production validation_gate sidecar validation passes",
    ],
    "missing_state": ["collocation_sampler_rng"],
    "primary_seed": 42,
    "prior_authorized_transient_halt_disqualifies": False,
    "resume_allowed": False,
    "retry_ceiling": "at most one fresh transient retry per logical run name per band generation",
    "terminal_cause_classes": [
        "scientific",
        "invariant",
        "loss_explosion",
        "non_finite",
        "intrinsic_memory",
        "unknown",
    ],
}
SCOPE_ACKS = {
    "not_causal_success_forecast": True,
    "not_smoke_or_graded_launch_authority": True,
    "preserves_unchanged_recipe_n500_seed_order_no_held_out": True,
    "does_not_reopen_gap_50_03": True,
}
SMOKE_STEPS = (100, 200, 300)
GRADED_STEPS = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
V2_SPLIT_HASHES = {
    41: "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
    42: "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
    43: "a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dumps_compact(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def dumps_pretty(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def selection_policy_sha256(policy: Mapping[str, Any] | None = None) -> str:
    return sha256_text(dumps_compact(policy or SELECTION_POLICY))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    write_text(path, dumps_pretty(payload))


def encode_metric(value: float) -> Any:
    return validation_gate.json_safe_float(value)


def script_env() -> dict[str, str]:
    """Environment for running the archived scripts.

    Each script puts ``Path(__file__).parents[4]`` on ``sys.path`` to import
    ``pinn``; from the archived location that is ``.planning/``, not the
    repository root, so the root is supplied through ``PYTHONPATH`` instead.
    """
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (str(REPO_ROOT), env.get("PYTHONPATH", "")) if p
    )
    return env


def _link_or_copy(src: str, dst: str) -> str:
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    return dst


def build_historical_repo(dest: Path, *, with_runs: bool) -> Path:
    """Rebuild Phase 50's pre-archive layout around the archived bytes.

    The terminal manifest and ledger record repository-relative paths under
    PHASE, so the historical record only verifies in that layout. This copies
    the archived phase folder as it exists on disk to PHASE, plus the committed
    run configs, and commits them. With ``with_runs`` it also hard-links (or
    copies) the local ``runs/stage0-rerun-*`` directories. Nothing in the real
    repository is written.

    The record also depends on files Git has never tracked (``*.pt`` is
    ignored): the run directories and the five ``run_start_rng.pt`` attempt
    copies. The test skips, naming them, when they are absent from this checkout.
    """
    archived = REPO_ROOT / ARCHIVED_PHASE
    runs = sorted((REPO_ROOT / "runs").glob("stage0-rerun-*"))
    rng_copies = sorted((archived / "evidence" / "attempts").glob("*/run_start_rng.pt"))
    if with_runs and not (runs and rng_copies):
        raise unittest.SkipTest(
            "local-only v2.2 evidence is absent from this checkout "
            "(runs/stage0-rerun-* and the archived attempts/*/run_start_rng.pt copies)"
        )
    shutil.copytree(archived, dest / PHASE, ignore=shutil.ignore_patterns("__pycache__"))
    for rel in CONFIG_PATHS:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / rel, dest / rel)
    git(dest, "init", "-q")
    git_commit(dest, "phase50 pre-archive layout")
    if with_runs:
        for run in runs:
            shutil.copytree(run, dest / "runs" / run.name, copy_function=_link_or_copy)
    return dest


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo),
        check=check,
        capture_output=True,
        text=True,
    )


def git_head(repo: Path) -> str:
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def git_tree(repo: Path, spec: str = "HEAD") -> str:
    return git(repo, "rev-parse", f"{spec}^{{tree}}").stdout.strip()


def git_commit(
    repo: Path,
    message: str,
    *,
    trailers: Mapping[str, str] | None = None,
) -> str:
    git(repo, "add", "-A")
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "phase50-fixture"
    env["GIT_AUTHOR_EMAIL"] = "phase50-fixture@example.test"
    env["GIT_COMMITTER_NAME"] = env["GIT_AUTHOR_NAME"]
    env["GIT_COMMITTER_EMAIL"] = env["GIT_AUTHOR_EMAIL"]
    body = [message]
    if trailers:
        body.append("")
        for key, value in trailers.items():
            body.append(f"{key}: {value}")
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "\n".join(body)],
        cwd=str(repo),
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return git_head(repo)


def make_sidecar(
    *,
    run_dir_name: str,
    step: int,
    seed: int,
    include_nonfinite: bool = False,
    extra_eps: list[float] | None = None,
) -> dict[str, Any]:
    values = extra_eps if extra_eps is not None else [
        1.0e-6 * (1 + (step // 100) * 0.01 + (seed % 10) * 0.001),
        2.0e-6 * (1 + (step // 200) * 0.02),
        4.0e-6,
    ]
    if include_nonfinite:
        values = [values[0], float("nan"), values[-1]]
    rows = []
    for index, eps_h in enumerate(values):
        rows.append(
            {
                "record_key": {
                    "variant": "hierarchical",
                    "fidelity": "base",
                    "id": index,
                },
                "eps_h": encode_metric(eps_h),
                "scs": encode_metric(gate_metrics.scs_from_eps_h(eps_h)),
            }
        )
    aggregate = gate_metrics.aggregate_gate_verdict(values)
    payload = {
        "schema_version": validation_gate.GATE_SIDECAR_SCHEMA_VERSION,
        "run_dir": run_dir_name,
        "sidecar_path": validation_gate.sidecar_relative_path(step),
        "global_step": int(step),
        "stage": 0,
        "split": "validation",
        "frame": {
            "position_frame": validation_gate.RATIFIED_VALIDATION_FRAME.position_frame,
            "time_coord": validation_gate.RATIFIED_VALIDATION_FRAME.time_coord,
            "mass_convention": validation_gate.RATIFIED_VALIDATION_FRAME.mass_convention,
            "conf01_evidence_ref": (
                validation_gate.RATIFIED_VALIDATION_FRAME.conf01_evidence_ref
            ),
        },
        "n_trajectories": len(rows),
        "rows": rows,
        "n_nonfinite": sum(1 for value in values if not math.isfinite(value)),
        "eps_h_reject_threshold": float(gate_metrics.GATE_EPS_H_REJECT_THRESHOLD),
        "scs_reject_threshold": float(gate_metrics.GATE_SCS_REJECT_THRESHOLD),
        "aggregate_eps_h": encode_metric(aggregate.eps_h),
        "aggregate_scs": encode_metric(aggregate.scs),
        "verdict": aggregate.verdict,
        "gate_status": "ok",
    }
    validation_gate.validate_sidecar_payload(
        payload,
        expected_run_dir_name=run_dir_name,
        expected_global_step=step,
        expected_sidecar_path=validation_gate.sidecar_relative_path(step),
    )
    return payload


def _step_record(step: int, *, front_idx: int, total: float, lambda_phys: float) -> dict[str, Any]:
    return {
        "event": "step",
        "step": step,
        "stage": 0,
        "phase": "2a",
        "epoch": step,
        "loss_data": 0.05,
        "loss_ic": 10.0,
        "loss_phys": 100.0,
        "loss_energy": 1.0,
        "loss_angmom": 0.2,
        "total": total,
        "lambda_data": 1.0,
        "lambda_ic": 1.0,
        "lambda_phys": lambda_phys,
        "lambda_e": 0.0,
        "lambda_l": 0.0,
        "grad_norm": 1.0,
        "grad_norm_raw_data": 0.1,
        "grad_norm_raw_ic": 0.2,
        "grad_norm_raw_phys": 0.3,
        "grad_norm_raw_energy": 0.4,
        "grad_norm_raw_angmom": 0.5,
        "grad_norm_applied_data": 0.1,
        "grad_norm_applied_ic": 0.2,
        "grad_norm_applied_phys": 0.3 * lambda_phys,
        "grad_norm_applied_energy": 0.0,
        "grad_norm_applied_angmom": 0.0,
        "grad_stats_provenance": "pre_total_backward",
        "grad_stats_complete": True,
        "w_min": 1.1754998158862984e-38,
        "w_mean": 0.5,
        "w_max": 1.0,
        "front_idx": front_idx,
        "lr": 0.001,
        "s_per_step": 0.1,
        "eta_seconds": None,
        "record_complete": True,
        "finite": True,
        "nonfinite_keys": [],
    }


def make_train_log(*, finished_step: int, advance_by: int = 200) -> str:
    lines: list[str] = []
    points = {1, 50, 100, 101, finished_step}
    if finished_step >= 500:
        points.update({200, 300, 400, 500, 600, 700, 800, 900, 1000})
    else:
        points.update({200, 300})
    for step in sorted(points):
        if step > finished_step:
            continue
        front = 0 if step < advance_by else 1 + (step - advance_by) // 100
        lambda_phys = 0.0 if step < 101 else 1.0
        total = 50.0 if step != 50 else 80.0
        lines.append(json.dumps(_step_record(step, front_idx=front, total=total, lambda_phys=lambda_phys)))
    return "\n".join(lines) + "\n"


def make_validation_jsonl(
    *,
    run_name: str,
    steps: tuple[int, ...],
    seed: int,
    sidecar_hashes: Mapping[int, str],
) -> str:
    lines = []
    previous = None
    for index, step in enumerate(steps):
        sidecar = f"validation_gate/step-{step:08d}.json"
        payload = {
            "step": step,
            "stage": 0,
            "final_val_loss": 1.0 + index * 0.01,
            "trend": "unavailable" if previous is None else "improving",
            "gate_schema_version": validation_gate.GATE_SIDECAR_SCHEMA_VERSION,
            "gate_status": "ok",
            "gate_verdict": "FAIL",
            "gate_eps_h": 4.0e-6,
            "gate_scs": math.log10(4.0e-6),
            "gate_n_trajectories": 3,
            "gate_n_nonfinite": 1 if step == steps[-1] else 0,
            "gate_sidecar": sidecar,
            "gate_sidecar_sha256": sidecar_hashes[step],
        }
        previous = payload["final_val_loss"]
        lines.append(json.dumps(payload, sort_keys=True))
    return "\n".join(lines) + "\n"


def make_summary(
    *,
    run_name: str,
    seed: int,
    finished_step: int,
    git_head: str,
    frozen_config_sha256: str,
    splits_sha256: str,
    sidecar_rel: str,
    include_nonfinite_terminal: bool,
) -> dict[str, Any]:
    gate_eps = 4.0e-6
    return {
        "schema_version": 1,
        "run_name": run_name,
        "disposition": "finished",
        "eval01_precondition_i": True,
        "final_losses": {
            "angmom": 0.2,
            "data": 0.05,
            "energy": 1.0,
            "ic": 10.0,
            "phys": 100.0,
            "total": 111.25,
        },
        "header": {
            "config_identity_digest": frozen_config_sha256[:16],
            "device": "mps",
            "precision": "float32",
            "run_name": run_name,
            "seed": seed,
            "git_head": git_head,
            "env_fingerprint": {
                "python_version": "3.11.15",
                "sw_vers": "macOS-fixture",
                "torch_build": "fixture",
                "torch_version": "2.12.1",
            },
        },
        "conformance": {
            "preflight_status": "passed",
            "schema_version": 1,
            "assertions": [
                {
                    "event": "run_start",
                    "stage": 0,
                    "status": "passed",
                    "open_divergences": [],
                    "checks": [
                        {"name": "invariant_b_window", "actual": 500, "passed": True, "tier": "advisory"}
                    ],
                }
            ],
        },
        "curriculum": [
            {
                "disposition": "HALT",
                "from_stage": 0,
                "step": finished_step,
                "to_stage": 0,
            }
        ],
        "validation": {
            "eval01_precondition_iii": True,
            "final_val_loss": 1.1,
            "gate_eps_h": gate_eps,
            "gate_n_nonfinite": 1 if include_nonfinite_terminal else 0,
            "gate_n_trajectories": 3,
            "gate_schema_version": validation_gate.GATE_SIDECAR_SCHEMA_VERSION,
            "gate_scs": math.log10(gate_eps),
            "gate_sidecar": sidecar_rel,
            "gate_status": "ok",
            "gate_verdict": "FAIL",
            "step": finished_step,
            "trend": "improving",
        },
        "test_preview": None,
    }


def make_status(*, run_name: str, step: int) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "run_name": run_name,
        "state": "finished",
        "stage": 0,
        "step": step,
        "epoch": step,
        "phase": "2a",
        "losses": {
            "angmom": 0.2,
            "data": 0.05,
            "energy": 1.0,
            "ic": 10.0,
            "phys": 100.0,
            "total": 111.25,
        },
    }


def make_training_metadata(*, s_h: float = 22.321729071058996, n_train: int = 1812) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "s_h": s_h,
        "eps_h": s_h * 0.0001,
        "n_train": n_train,
        "energy_floor_factor": 0.0001,
        "eps_train": 1e-5,
        "frame": {
            "mass_convention": "ordered_raw",
            "position_frame": "r_prime",
            "time_coord": "u_t_over_T",
        },
    }


def make_preflight() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": "passed",
        "eval01_precondition_i": True,
        "assertions": [
            {
                "event": "run_start",
                "stage": 0,
                "status": "passed",
                "checks": [
                    {"name": "run_start", "passed": True},
                    {"name": "census", "passed": True},
                    {"name": "invariant_b_window", "actual": 500, "passed": True},
                ],
            }
        ],
    }


def make_splits(*, seed: int, match_v2: bool = False) -> dict[str, Any]:
    if match_v2:
        return {"algorithm": "group-signature-hamilton-v1", "seed": seed, "v2_pin": V2_SPLIT_HASHES[seed]}
    return {
        "algorithm": "group-signature-hamilton-v1",
        "seed": seed,
        "groups": [
            {
                "physical_key": {"id": 0, "variant": "hierarchical"},
                "records": [
                    {"fidelity": "base", "id": 0, "stage": 0, "variant": "hierarchical"}
                ],
                "split": "train",
            },
            {
                "physical_key": {"id": 1, "variant": "hierarchical"},
                "records": [
                    {"fidelity": "base", "id": 1, "stage": 0, "variant": "hierarchical"}
                ],
                "split": "validation",
            },
        ],
    }


def make_config_yaml(*, seed: int, run_name: str, smoke: bool) -> str:
    n_adam = 300 if smoke else 1000
    replay = 32 if smoke else None
    replay_line = f"  replay_count: {replay}\n" if replay is not None else ""
    return (
        f"run:\n"
        f"  seed: {seed}\n"
        f"  run_name: {run_name}\n"
        f"  smoke: {str(smoke).lower()}\n"
        f"  invariants:\n"
        f"    front_advance_window_n: 500\n"
        f"stage:\n"
        f"  max_epochs: {n_adam}\n"
        f"  n_adam: {n_adam}\n"
        f"{replay_line}"
        f"opt:\n"
        f"  validation_every: 100\n"
        f"  log_every: 50\n"
        f"loss:\n"
        f"  lambda_e_max: 0.0\n"
        f"device: mps\n"
        f"precision: float32\n"
    )


def fence(payload: Mapping[str, Any]) -> str:
    return "```json\n" + dumps_pretty(payload).rstrip() + "\n```\n"


def make_pre_registration(
    *,
    config_hashes: Mapping[str, str],
    split_hashes: Mapping[str, str],
    parent: str | None,
    extra_binding: Mapping[str, Any] | None = None,
) -> str:
    set_hash = sha256_text(dumps_compact(dict(sorted(config_hashes.items()))))
    binding = {
        "committed_config_set_sha256": set_hash,
        "committed_config_sha256_by_path": dict(sorted(config_hashes.items())),
        "expected_splits_sha256": dict(sorted(split_hashes.items())),
        "forbidden_launch_flags": ["--resume"],
        "parent_pre_registration_commit": parent,
        "required_launch_flags": ["--stage-0-only"],
        "source_config_sha256": config_hashes["configs/stage0-rerun-seed42.yaml"],
    }
    if extra_binding:
        binding.update(extra_binding)
    blob = {
        "generation_binding": binding,
        "schema": "phase50-pre-registration/v2",
        "selection_policy": SELECTION_POLICY,
        "selection_policy_sha256": selection_policy_sha256(),
    }
    return (
        "# Fixture pre-registration\n\n"
        "Synthetic Phase-50 pre-registration used only by dataset-free tests.\n\n"
        + fence(blob)
    )


def make_owner_summary(
    *,
    schema: str,
    option: str,
    plan_50_06: str,
    plan_50_07: str,
    extra: Mapping[str, Any] | None = None,
) -> str:
    decision = {
        "schema": schema,
        "selected_option": option,
        "owner_response_verbatim": f"{option}; scope acknowledged",
        "scope_acknowledgements": dict(SCOPE_ACKS),
        "plan_50_06_commit": plan_50_06,
        "plan_50_07_commit": plan_50_07,
    }
    if extra:
        decision.update(extra)
    return (
        f"# Fixture owner decision\n\n"
        f"This is a synthetic committed owner blob.\n\n"
        + fence(decision)
    )


def historical_generation(n: int, *, git_head: str, pre_reg: str) -> dict[str, Any]:
    corpus_rel = f"{EVIDENCE}/corpus/generation-{n}.json"
    env_rel = f"{EVIDENCE}/environment/generation-{n}.json"
    clean_rel = f"{EVIDENCE}/cleanliness/generation-{n}-open-runtime.json"
    return {
        "band_generation": n,
        "git_head": git_head,
        "pre_registration_commit": pre_reg,
        "committed_config_sha256_by_path": {},
        "committed_config_set_sha256": "0" * 64,
        "corpus_snapshot": {
            "path": corpus_rel,
            "file_sha256": None,
            "corpus_snapshot_sha256": sha256_text(f"corpus-{n}"),
        },
        "environment_snapshot": {
            "path": env_rel,
            "file_sha256": None,
            "environment_snapshot_sha256": sha256_text(f"env-{n}"),
        },
        "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": git_head,
            "git_head_available": True,
        },
        "summary_env_fingerprint": {
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
        },
        "opened_utc": "2026-08-13T00:00:00+00:00",
        "closed_utc": "2026-08-13T00:01:00+00:00",
        "cleanliness_receipts": [
            {
                "boundary": "runtime",
                "path": clean_rel,
                "sha256": None,
            }
        ],
        "verify_invocations": [],
        "status": "terminal",
    }


@dataclass
class AttemptSpec:
    seed: int
    run_name: str
    attempt_ordinal: int
    kind: str
    in_final_band: bool
    finished_step: int
    steps: tuple[int, ...]
    eligible: bool = True


@dataclass
class EvidenceRepo:
    root: Path
    commits: dict[str, str] = field(default_factory=dict)
    config_hashes: dict[str, str] = field(default_factory=dict)
    split_hashes: dict[str, str] = field(default_factory=dict)
    attempt_roots: dict[str, Path] = field(default_factory=dict)
    sidecar_paths: dict[tuple[str, int], Path] = field(default_factory=dict)

    def path(self, rel: str | Path) -> Path:
        return self.root / rel

    def run_tool(self, script: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(script), *args],
            cwd=str(self.root),
            capture_output=True,
            text=True,
            env=script_env(),
        )

    def extract(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool(BUILDER, ["extract", "--repo-root", str(self.root)])

    def band(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool(BUILDER, ["band", "--repo-root", str(self.root)])

    def candidate(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool(BUILDER, ["candidate", "--repo-root", str(self.root)])

    def finalize(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool(BUILDER, ["finalize", "--repo-root", str(self.root)])

    def verify(self, command: str, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        args = [command, "--repo-root", str(self.root)]
        if extra:
            args.extend(extra)
        return self.run_tool(VERIFIER, args)


def _init_repo(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    git(root, "init", "-b", "milestone/v2.2")
    git(root, "config", "user.email", "phase50-fixture@example.test")
    git(root, "config", "user.name", "phase50-fixture")
    write_text(root / ".gitignore", "runs/\n*.log\n")
    write_text(root / "pinn/__init__.py", "# fixture pinn package marker\n")
    write_text(root / "tests/phase50/__init__.py", "# fixture tests marker\n")
    write_text(root / PHASE / "README.md", "fixture phase tree\n")


def _write_source_configs(repo: EvidenceRepo) -> None:
    mapping = {
        "configs/stage0-rerun-smoke.yaml": make_config_yaml(seed=42, run_name="stage0-rerun-smoke", smoke=True),
        "configs/stage0-rerun-seed41.yaml": make_config_yaml(seed=41, run_name="stage0-rerun-seed41", smoke=False),
        "configs/stage0-rerun-seed42.yaml": make_config_yaml(seed=42, run_name="stage0-rerun-seed42", smoke=False),
        "configs/stage0-rerun-seed43.yaml": make_config_yaml(seed=43, run_name="stage0-rerun-seed43", smoke=False),
    }
    for rel, text in mapping.items():
        write_text(repo.path(rel), text)
        repo.config_hashes[rel] = sha256_text(text)


def _write_historical_artifacts(repo: EvidenceRepo, generations: list[dict[str, Any]]) -> None:
    for generation in generations:
        n = generation["band_generation"]
        corpus = {
            "schema": "phase50-corpus-snapshot/v1",
            "band_generation": n,
            "corpus_snapshot_sha256": generation["corpus_snapshot"]["corpus_snapshot_sha256"],
        }
        environment = {
            "schema": "phase50-environment-snapshot/v1",
            "band_generation": n,
            "environment_snapshot_sha256": generation["environment_snapshot"]["environment_snapshot_sha256"],
        }
        cleanliness = {"boundary": "runtime", "band_generation": n, "clean": True}
        write_json(repo.path(generation["corpus_snapshot"]["path"]), corpus)
        write_json(repo.path(generation["environment_snapshot"]["path"]), environment)
        write_json(repo.path(generation["cleanliness_receipts"][0]["path"]), cleanliness)
        generation["corpus_snapshot"]["file_sha256"] = sha256_file(
            repo.path(generation["corpus_snapshot"]["path"])
        )
        generation["environment_snapshot"]["file_sha256"] = sha256_file(
            repo.path(generation["environment_snapshot"]["path"])
        )
        generation["cleanliness_receipts"][0]["sha256"] = sha256_file(
            repo.path(generation["cleanliness_receipts"][0]["path"])
        )
        generation["committed_config_sha256_by_path"] = dict(repo.config_hashes)
        generation["committed_config_set_sha256"] = sha256_text(
            dumps_compact(dict(sorted(repo.config_hashes.items())))
        )


def _write_attempt(
    repo: EvidenceRepo,
    spec: AttemptSpec,
    *,
    git_head: str,
    source_config: str,
    corpus_sha: str,
    env_sha: str,
    qualify_split: bool = True,
) -> dict[str, Any]:
    run_dir = repo.path(f"runs/{spec.run_name}")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    config_text = make_config_yaml(
        seed=spec.seed,
        run_name=spec.run_name,
        smoke=spec.kind == "smoke",
    )
    write_text(run_dir / "config.yaml", config_text)
    frozen_hash = sha256_text(config_text)
    splits = make_splits(seed=spec.seed, match_v2=not qualify_split)
    write_json(run_dir / "splits.json", splits)
    splits_hash = sha256_file(run_dir / "splits.json")
    repo.split_hashes[str(spec.seed)] = splits_hash
    write_json(run_dir / "preflight.json", make_preflight())
    write_json(run_dir / "training_metadata.json", make_training_metadata())
    write_text(run_dir / "curriculum.jsonl", json.dumps({"disposition": "HALT", "from_stage": 0, "step": spec.finished_step, "to_stage": 0}) + "\n")
    write_text(run_dir / "summary.md", f"# {spec.run_name}\n")
    write_json(run_dir / "status.json", make_status(run_name=spec.run_name, step=spec.finished_step))
    write_text(run_dir / "run_start_rng.pt", f"rng-{spec.run_name}-{spec.attempt_ordinal}\n")
    write_text(run_dir / "logs/train.log.jsonl", make_train_log(finished_step=spec.finished_step))
    write_text(run_dir / "checkpoints/best.pt", f"best-bytes-{spec.run_name}\n")
    write_text(run_dir / "checkpoints/latest.pt", f"latest-bytes-{spec.run_name}\n")
    write_text(run_dir / f"checkpoints/step-{spec.finished_step:06d}.pt", f"step-bytes-{spec.run_name}\n")
    sidecar_hashes: dict[int, str] = {}
    for step in spec.steps:
        payload = make_sidecar(
            run_dir_name=spec.run_name,
            step=step,
            seed=spec.seed,
            include_nonfinite=(step == spec.steps[-1]),
        )
        dest = run_dir / payload["sidecar_path"]
        write_json(dest, payload)
        sidecar_hashes[step] = sha256_file(dest)
        repo.sidecar_paths[(spec.run_name, step)] = dest
    write_text(
        run_dir / "validation.jsonl",
        make_validation_jsonl(
            run_name=spec.run_name,
            steps=spec.steps,
            seed=spec.seed,
            sidecar_hashes=sidecar_hashes,
        ),
    )
    terminal_sidecar = validation_gate.sidecar_relative_path(spec.steps[-1])
    summary = make_summary(
        run_name=spec.run_name,
        seed=spec.seed,
        finished_step=spec.finished_step,
        git_head=git_head,
        frozen_config_sha256=frozen_hash,
        splits_sha256=splits_hash,
        sidecar_rel=terminal_sidecar,
        include_nonfinite_terminal=True,
    )
    if not spec.eligible:
        summary["eval01_precondition_i"] = False
        summary["conformance"]["preflight_status"] = "failed"
    write_json(run_dir / "summary.json", summary)
    transcript_rel = EVIDENCE / "launch-transcripts" / f"{spec.run_name}-attempt-{spec.attempt_ordinal:02d}-invocation-01-train.txt"
    write_text(repo.path(transcript_rel), f"launch {spec.run_name}\n")
    artifact_map = {
        "config.yaml": sha256_file(run_dir / "config.yaml"),
        "summary.json": sha256_file(run_dir / "summary.json"),
        "summary.md": sha256_file(run_dir / "summary.md"),
        "preflight.json": sha256_file(run_dir / "preflight.json"),
        "training_metadata.json": sha256_file(run_dir / "training_metadata.json"),
        "splits.json": splits_hash,
        "curriculum.jsonl": sha256_file(run_dir / "curriculum.jsonl"),
        "validation.jsonl": sha256_file(run_dir / "validation.jsonl"),
        "status.json": sha256_file(run_dir / "status.json"),
        "logs/train.log.jsonl": sha256_file(run_dir / "logs/train.log.jsonl"),
        "run_start_rng.pt": sha256_file(run_dir / "run_start_rng.pt"),
        "checkpoints/best.pt": sha256_file(run_dir / "checkpoints/best.pt"),
        "checkpoints/latest.pt": sha256_file(run_dir / "checkpoints/latest.pt"),
        f"checkpoints/step-{spec.finished_step:06d}.pt": sha256_file(
            run_dir / f"checkpoints/step-{spec.finished_step:06d}.pt"
        ),
    }
    for step, digest in sidecar_hashes.items():
        artifact_map[validation_gate.sidecar_relative_path(step)] = digest
    command = (
        f"{PYTHON} -m pinn.train --config {source_config} --stage-0-only"
    )
    record = {
        "band_generation": 4,
        "run_name": spec.run_name,
        "attempt_ordinal": spec.attempt_ordinal,
        "artifact_dir": f"runs/{spec.run_name}",
        "config": source_config,
        "source_config_sha256": repo.config_hashes[source_config],
        "frozen_config_sha256": frozen_hash,
        "config_identity_digest": frozen_hash[:16],
        "corpus_snapshot_sha256": corpus_sha,
        "environment_snapshot_sha256": env_sha,
        "git_head": git_head,
        "invocations": [
            {
                "invocation_ordinal": 1,
                "launch_kind": "fresh",
                "status": "closed",
                "intended_artifact_dir": f"runs/{spec.run_name}",
                "launch_command": command,
                "launch_transcript": str(transcript_rel),
                "transcript_sha256": sha256_file(repo.path(transcript_rel)),
                "external_start_utc": "2026-08-15T00:00:00+00:00",
                "external_end_utc": "2026-08-15T00:10:00+00:00",
                "exit_code": 0,
                "git_head": git_head,
                "source_config_sha256": repo.config_hashes[source_config],
                "frozen_config_sha256": frozen_hash,
                "corpus_snapshot_sha256": corpus_sha,
                "environment_snapshot_sha256": env_sha,
                "resume_checkpoint": None,
                "calibration_before": None,
                "calibration_after": None,
                "observed_summary_disposition": "finished",
                "observed_guard_disposition": None,
                "artifact_sha256_at_exit": dict(artifact_map),
                "invocation_snapshot": None,
            }
        ],
        "final_process_disposition": "finished",
        "final_guard_disposition": None,
        "ledger_disposition": "finished",
        "protocol_labels": [],
        "in_final_band": spec.in_final_band,
        "terminal_artifact_sha256": dict(artifact_map),
        "reason": f"fixture {spec.kind}",
        "retry_authorization": None,
    }
    repo.attempt_roots[spec.run_name] = run_dir
    return record


def _write_ledger(
    repo: EvidenceRepo,
    *,
    generations: list[dict[str, Any]],
    records: list[dict[str, Any]],
    final_band_generation: int | None,
) -> None:
    payload = {
        "schema": "phase50-run-ledger/v2",
        "final_band_generation": final_band_generation,
        "band_generations": generations,
        "records": records,
    }
    write_text(
        repo.path(LEDGER_REL),
        "# Fixture run ledger\n\n<!-- phase50-run-ledger-schema: phase50-run-ledger/v2 -->\n\n"
        + fence(payload),
    )


def _generation_4(
    repo: EvidenceRepo,
    *,
    git_head: str,
    pre_reg: str,
    status: str,
) -> dict[str, Any]:
    corpus_rel = str(EVIDENCE / "corpus/generation-4.json")
    env_rel = str(EVIDENCE / "environment/generation-4.json")
    clean_rel = str(EVIDENCE / "cleanliness/generation-4-open-runtime.json")
    calib_rel = str(EVIDENCE / "calibration/generation-4-smoke.json")
    corpus_sha = sha256_text("corpus-4")
    env_sha = sha256_text("env-4")
    write_json(
        repo.path(corpus_rel),
        {"schema": "phase50-corpus-snapshot/v1", "band_generation": 4, "corpus_snapshot_sha256": corpus_sha},
    )
    write_json(
        repo.path(env_rel),
        {"schema": "phase50-environment-snapshot/v1", "band_generation": 4, "environment_snapshot_sha256": env_sha},
    )
    write_json(repo.path(clean_rel), {"boundary": "runtime", "band_generation": 4, "clean": True})
    write_json(repo.path(calib_rel), {"schema": "phase50-calibration/v1", "band_generation": 4, "valid": True})
    return {
        "band_generation": 4,
        "git_head": git_head,
        "pre_registration_commit": pre_reg,
        "committed_config_sha256_by_path": dict(repo.config_hashes),
        "committed_config_set_sha256": sha256_text(dumps_compact(dict(sorted(repo.config_hashes.items())))),
        "corpus_snapshot": {
            "path": corpus_rel,
            "file_sha256": sha256_file(repo.path(corpus_rel)),
            "corpus_snapshot_sha256": corpus_sha,
        },
        "environment_snapshot": {
            "path": env_rel,
            "file_sha256": sha256_file(repo.path(env_rel)),
            "environment_snapshot_sha256": env_sha,
        },
        "timing_fingerprint": {
            "device": "mps",
            "dtype": "torch.float32",
            "torch_version": "2.12.1",
            "python_version": "3.11.15",
            "git_head": git_head,
            "git_head_available": True,
        },
        "summary_env_fingerprint": {
            "python_version": "3.11.15",
            "torch_version": "2.12.1",
        },
        "opened_utc": "2026-08-15T00:00:00+00:00",
        "closed_utc": None if status in (None, "", "open") else "2026-08-15T01:00:00+00:00",
        "cleanliness_receipts": [
            {
                "boundary": "runtime",
                "path": clean_rel,
                "sha256": sha256_file(repo.path(clean_rel)),
            }
        ],
        "verify_invocations": [],
        "calibration_expectation": {
            "path": calib_rel,
            "sha256": sha256_file(repo.path(calib_rel)),
        },
        "status": status,
    }


def build_fixture(
    root: Path,
    *,
    mode: str = "complete",
    candidate_variant: str = "primary42",
    qualify_split: bool = True,
) -> EvidenceRepo:
    """Create a temporary evidence repository.

    Modes:
      authorization — committed 50-08 blob, no generation 4
      preregistered — unopened generation 4 scaffold
      run-window — opened generation 4 with no invocations
      complete — finished smoke + seeds 41/42/43
    """
    _init_repo(root)
    repo = EvidenceRepo(root=root)
    _write_source_configs(repo)
    write_text(repo.path(CONFIG_DELTA_REL), "# Fixture config delta\n\nNo causal recipe change.\n")
    write_text(repo.path(PHASE / "50-06-marker.md"), "50-06 fixture marker\n")
    repo.commits["50-06"] = git_commit(root, "fix(50-06): fixture conformance repair")
    write_text(repo.path(PHASE / "50-07-marker.md"), "50-07 fixture marker\n")
    repo.commits["50-07"] = git_commit(root, "feat(50-07): fixture evidence tooling")

    auth_text = make_owner_summary(
        schema="phase50-owner-preregistration-decision/v1",
        option="authorize-preregistration",
        plan_50_06=repo.commits["50-06"],
        plan_50_07=repo.commits["50-07"],
    )
    write_text(repo.path(AUTH_SUMMARY_REL), auth_text)
    repo.commits["50-08"] = git_commit(
        root,
        "plan(50): record preregistration owner decision",
        trailers={"Decision-Summary-SHA256": sha256_text(auth_text)},
    )

    smoke_auth = make_owner_summary(
        schema="phase50-owner-smoke-decision/v1",
        option="authorize-smoke",
        plan_50_06=repo.commits["50-06"],
        plan_50_07=repo.commits["50-07"],
        extra={"one_use": True, "authorizes_graded": False},
    )

    historical_head = repo.commits["50-08"]
    generations = [
        historical_generation(1, git_head=historical_head, pre_reg=repo.commits["50-08"]),
        historical_generation(2, git_head=historical_head, pre_reg=repo.commits["50-08"]),
        historical_generation(3, git_head=historical_head, pre_reg=repo.commits["50-08"]),
    ]
    _write_historical_artifacts(repo, generations)

    if mode == "authorization":
        _write_ledger(repo, generations=generations, records=[], final_band_generation=None)
        write_text(
            repo.path(PRE_REG_REL),
            make_pre_registration(
                config_hashes=repo.config_hashes,
                split_hashes={str(k): v for k, v in V2_SPLIT_HASHES.items()},
                parent=None,
            ),
        )
        git(root, "add", "-A")
        git(root, "commit", "-m", "docs(50): fixture authorization state", check=False)
        repo.commits["HEAD"] = git_head(root)
        return repo

    split_pins = {str(k): v for k, v in V2_SPLIT_HASHES.items()}
    write_text(
        repo.path(PRE_REG_REL),
        make_pre_registration(
            config_hashes=repo.config_hashes,
            split_hashes=split_pins,
            parent=repo.commits["50-08"],
            extra_binding={
                "source_commit": None,
                "authorization_commit": repo.commits["50-08"],
            },
        ),
    )
    repo.commits["prereg"] = git_commit(root, "evidence(50): fixture preregistration")
    pre_reg = repo.commits["prereg"]
    gen4 = _generation_4(repo, git_head=pre_reg, pre_reg=pre_reg, status="open")
    if mode == "preregistered":
        _write_ledger(repo, generations=generations + [gen4], records=[], final_band_generation=None)
        repo.commits["HEAD"] = git_commit(root, "evidence(50): fixture unopened generation 4")
        return repo

    if mode == "run-window":
        write_text(repo.path(SMOKE_AUTH_REL), smoke_auth)
        _write_ledger(repo, generations=generations + [gen4], records=[], final_band_generation=None)
        repo.commits["50-10"] = git_commit(
            root,
            "plan(50): record smoke owner decision",
            trailers={"Decision-Summary-SHA256": sha256_text(smoke_auth)},
        )
        # Registered source HEAD must equal the smoke-authorization commit.
        repo.commits["HEAD"] = repo.commits["50-10"]
        return repo

    write_text(repo.path(SMOKE_AUTH_REL), smoke_auth)
    repo.commits["50-10"] = git_commit(
        root,
        "plan(50): record smoke owner decision",
        trailers={"Decision-Summary-SHA256": sha256_text(smoke_auth)},
    )
    band_head = repo.commits["50-10"]
    gen4["git_head"] = band_head
    gen4["status"] = "complete"
    gen4["closed_utc"] = "2026-08-15T01:00:00+00:00"

    eligibility = {
        "primary42": {41: True, 42: True, 43: True},
        "fallback41": {41: True, 42: False, 43: True},
        "fallback43": {41: False, 42: False, 43: True},
        "none": {41: False, 42: False, 43: False},
    }[candidate_variant]

    specs = [
        AttemptSpec(42, "stage0-rerun-smoke", 1, "smoke", False, 300, SMOKE_STEPS),
        AttemptSpec(41, "stage0-rerun-seed41", 1, "graded", True, 1000, GRADED_STEPS, eligibility[41]),
        AttemptSpec(42, "stage0-rerun-seed42", 1, "graded", True, 1000, GRADED_STEPS, eligibility[42]),
        AttemptSpec(43, "stage0-rerun-seed43", 1, "graded", True, 1000, GRADED_STEPS, eligibility[43]),
    ]
    records = []
    corpus_sha = gen4["corpus_snapshot"]["corpus_snapshot_sha256"]
    env_sha = gen4["environment_snapshot"]["environment_snapshot_sha256"]
    config_for = {
        "stage0-rerun-smoke": "configs/stage0-rerun-smoke.yaml",
        "stage0-rerun-seed41": "configs/stage0-rerun-seed41.yaml",
        "stage0-rerun-seed42": "configs/stage0-rerun-seed42.yaml",
        "stage0-rerun-seed43": "configs/stage0-rerun-seed43.yaml",
    }
    for spec in specs:
        records.append(
            _write_attempt(
                repo,
                spec,
                git_head=band_head,
                source_config=config_for[spec.run_name],
                corpus_sha=corpus_sha,
                env_sha=env_sha,
                qualify_split=qualify_split,
            )
        )
    _write_ledger(
        repo,
        generations=generations + [gen4],
        records=records,
        final_band_generation=4,
    )
    repo.commits["HEAD"] = git_commit(root, "docs(50): fixture complete generation 4")
    return repo


def clone_complete(root: Path, **kwargs: Any) -> EvidenceRepo:
    return build_fixture(root, mode="complete", **kwargs)


def fail_closed_message(proc: subprocess.CompletedProcess[str]) -> str:
    return (proc.stderr or "") + (proc.stdout or "")
