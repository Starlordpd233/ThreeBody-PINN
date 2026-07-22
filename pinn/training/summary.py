"""Stub-then-finalize honesty writer for ``summary.md`` + ``summary.json`` (OPS-05 / E4).

``summary.md`` + ``summary.json`` are written at run start as an honest "run in
progress / did not complete" template (:func:`stub_summary`) and **atomically
replaced** at the terminal transition with the final one-pager
(:func:`finalize_summary`; finished / failed / interrupted variants). Presence is
thereby guaranteed under **every** death mode including SIGKILL — a
write-at-exit-only design cannot satisfy E4's presence invariant (CTX-77).

Honesty invariants (must-NOT #1):
    A failed/interrupted summary names its state and leaves metrics null — never a
    placeholder number, never a "finished"/healthy reading for a run that diverged
    or was terminated. A loss term that never finalized stays null (CTX-67 null
    policy; never fabricated).

Redaction (must-NOT #2 / CTX-79):
    The one-pager records run-directory-relative identity only — no absolute
    ``/Users/…`` paths, no hostnames, no secrets. The ratified environment
    fingerprint (``sw_vers``, ``python -V``, torch version/build) lives in the
    ``summary.json`` run header ONLY (B-6/D-12), never in ``summary.md``.

Provenance:
    The config-identity digest is ``sha256(<run_dir>/config.yaml bytes)[:16]`` over
    the frozen resolved config that ``pinn/training/config_yaml.py``'s
    ``freeze_resolved_config`` writes at launch (``sort_keys`` → stable identity
    digest, 41-05). The curriculum progression is RENDERED from the existing
    ``runs/<name>/curriculum.jsonl`` — never recomputed. Every write reuses
    ``pinn.training.atomic_io.atomic_write_text`` (do NOT reimplement atomic write).

Generation is a pure render + atomic write; the composition root (42-08) calls it
on every exit path.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Union

from pinn.training.atomic_io import atomic_write_text

PathLike = Union[str, Path]

# summary.json schema version. Bump only on a breaking schema change.
SCHEMA_VERSION = 1

# Canonical loss terms: five terms + total (CTX-68 / CTX-77). A term that never
# finalized stays null (CTX-67; never fabricated — must-NOT #1).
_LOSS_TERMS = ("data", "ic", "phys", "energy", "angmom", "total")

# Disposition → human-readable status line for summary.md. The failed/interrupted
# templates deliberately avoid the substring "finished" so a non-success one-pager
# can never read as a success (must-NOT #1).
_STATUS_TEXT = {
    "in_progress": "in progress (did not complete)",
    "finished": "finished",
    "failed": "failed",
    "interrupted": "interrupted",
}

_HONESTY_NOTES = (
    "Healthy validation does not mean the model works.",
    "Run-to-run comparison does not prove progress.",
    "A clean loss curve does not establish correct physics.",
)


def _null_if_nonfinite(value: Any) -> Optional[float]:
    """CTX-67 null policy for a single scalar: None / NaN / Inf → JSON null."""
    if value is None:
        return None
    try:
        fv = float(value)
    except (TypeError, ValueError):
        return None
    if fv != fv or fv in (float("inf"), float("-inf")):  # NaN / ±Inf without math
        return None
    return fv


def _config_identity_digest(run_dir: Path) -> Optional[str]:
    """First 16 hex chars of sha256 over the frozen ``<run_dir>/config.yaml`` bytes.

    Provenance: ``pinn/training/config_yaml.py:freeze_resolved_config`` writes the
    fully-resolved config to ``<run_dir>/config.yaml`` at launch (``sort_keys`` for
    stable identity digests, 41-05). A missing/unreadable file yields ``null`` —
    never an invented digest.
    """
    config_path = run_dir / "config.yaml"
    try:
        return hashlib.sha256(config_path.read_bytes()).hexdigest()[:16]
    except OSError:
        return None


def _env_fingerprint() -> Dict[str, Optional[str]]:
    """Ratified environment fingerprint (B-6/D-12) — summary.json header ONLY.

    ``sw_vers`` (OS version, not hostname), ``python -V``, and torch version/build.
    Best-effort: any probe failure yields null. No machine identity, home path,
    hostname, or secret (CTX-79). torch is imported lazily (no module-load dep).
    """
    fp: Dict[str, Optional[str]] = {}
    try:
        proc = subprocess.run(
            ["sw_vers"], capture_output=True, text=True, timeout=5
        )
        fp["sw_vers"] = proc.stdout.strip() if proc.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        fp["sw_vers"] = None
    fp["python_version"] = sys.version.split()[0] if sys.version else None
    try:
        import torch

        fp["torch_version"] = getattr(torch, "__version__", None)
        fp["torch_build"] = getattr(getattr(torch, "version", None), "git_version", None)
    except Exception:
        fp["torch_version"] = None
        fp["torch_build"] = None
    return fp


def _render_curriculum(curriculum_path: Optional[PathLike]) -> List[Dict[str, Any]]:
    """Render (NOT recompute) the curriculum progression from ``curriculum.jsonl``.

    Returns the parsed JSON records in order; a missing/unreadable file yields an
    empty progression. Malformed lines are skipped (best-effort render).
    """
    if curriculum_path is None:
        return []
    path = Path(curriculum_path)
    if not path.exists():
        return []
    records: List[Dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict):
            records.append(rec)
    return records


def _read_json_mapping(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Read one persisted JSON object, returning unavailable on any bad input."""
    if path is None:
        return None
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        return None
    return dict(value) if isinstance(value, Mapping) else None


def _read_jsonl_mappings(path: Optional[PathLike]) -> List[Dict[str, Any]]:
    """Read persisted JSONL records in order without deriving replacement data."""
    if path is None:
        return []
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    records: List[Dict[str, Any]] = []
    for line in lines:
        try:
            value = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(value, Mapping):
            records.append(dict(value))
    return records


def _validation_summary(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Select the last persisted validation record; never infer a trend."""
    records = _read_jsonl_mappings(path)
    if not records:
        return None
    record = records[-1]
    final_val_loss = _null_if_nonfinite(record.get("final_val_loss"))
    trend = record.get("trend")
    if not isinstance(trend, str) or not trend:
        trend = None
    step = record.get("step")
    return {
        "final_val_loss": final_val_loss,
        "trend": trend,
        "step": step,
    }


def _test_preview(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Project the committed evaluation artifact into the summary payload."""
    metrics = _read_json_mapping(path)
    if metrics is None:
        return None
    verdict = metrics.get("verdict")
    if verdict not in ("PASS", "FAIL"):
        verdict = None
    return {
        "eps_h": _null_if_nonfinite(metrics.get("eps_h")),
        "scs": _null_if_nonfinite(metrics.get("scs")),
        "verdict": verdict,
        "n_test_trajectories": metrics.get("n_test_trajectories"),
    }


def _comparison_hint(
    prior_summary_path: Optional[PathLike],
    *,
    current_preview: Optional[Mapping[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Render persisted current/prior values side by side without judging progress."""
    prior = _read_json_mapping(prior_summary_path)
    if prior is None:
        return None
    prior_run_name = prior.get("run_name")
    if prior_run_name is None and isinstance(prior.get("header"), Mapping):
        prior_run_name = prior["header"].get("run_name")
    if not isinstance(prior_run_name, str) or not prior_run_name:
        return None
    prior_preview = prior.get("test_preview")
    if not isinstance(prior_preview, Mapping):
        prior_preview = {}
    return {
        "prior_run_name": prior_run_name,
        "current_eps_h": (
            current_preview.get("eps_h") if current_preview is not None else None
        ),
        "prior_eps_h": _null_if_nonfinite(prior_preview.get("eps_h")),
        "current_scs": (
            current_preview.get("scs") if current_preview is not None else None
        ),
        "prior_scs": _null_if_nonfinite(prior_preview.get("scs")),
        "current_verdict": (
            current_preview.get("verdict") if current_preview is not None else None
        ),
        "prior_verdict": prior_preview.get("verdict"),
    }


def _final_losses_dict(final_losses: Optional[Mapping[str, Any]]) -> Dict[str, Optional[float]]:
    src: Mapping[str, Any] = final_losses or {}
    return {term: _null_if_nonfinite(src.get(term)) for term in _LOSS_TERMS}


def _compose(
    *,
    run_dir: Path,
    disposition: str,
    header: Optional[Mapping[str, Any]],
    final_losses: Optional[Mapping[str, Any]],
    curriculum: List[Dict[str, Any]],
    validation_records_path: Optional[PathLike] = None,
    metrics_path: Optional[PathLike] = None,
    prior_summary_path: Optional[PathLike] = None,
) -> "tuple[Dict[str, Any], str]":
    """Build the (summary.json payload, summary.md text) pair for ``disposition``."""
    hdr: Mapping[str, Any] = header or {}
    success = disposition == "finished"
    preview = _test_preview(metrics_path) if success else None
    payload: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "disposition": disposition,
        "run_name": hdr.get("run_name"),
        "header": {
            "run_name": hdr.get("run_name"),
            "start_utc": hdr.get("start_utc"),
            "end_utc": hdr.get("end_utc"),
            "wall_clock_secs": hdr.get("wall_clock_secs"),
            "device": hdr.get("device"),
            "precision": hdr.get("precision"),
            "seed": hdr.get("seed"),
            "config_identity_digest": _config_identity_digest(run_dir),
            # B-6/D-12 environment fingerprint lives in summary.json ONLY.
            "env_fingerprint": _env_fingerprint(),
        },
        "final_losses": _final_losses_dict(final_losses if success else None),
        "validation": _validation_summary(validation_records_path) if success else None,
        "curriculum": curriculum if success else [],
        "test_preview": preview,
        "comparison": (
            _comparison_hint(prior_summary_path, current_preview=preview)
            if success
            else None
        ),
    }
    return payload, _render_md(payload)


def _render_md(payload: Mapping[str, Any]) -> str:
    """Render the human-readable one-pager (no env-fingerprint, no absolute paths)."""
    disposition = payload["disposition"]
    header: Mapping[str, Any] = payload["header"]
    losses: Mapping[str, Any] = payload["final_losses"]
    curriculum: List[Dict[str, Any]] = payload["curriculum"]
    validation = payload.get("validation")
    test_preview = payload.get("test_preview")
    comparison = payload.get("comparison")
    status_text = _STATUS_TEXT.get(disposition, str(disposition))

    lines: List[str] = ["# Run Summary", "", f"**Status:** {status_text}", ""]
    lines.append("## Run header")
    lines.append("")
    lines.append(f"- run_name: {header.get('run_name')}")
    lines.append(f"- start_utc: {header.get('start_utc')}")
    lines.append(f"- end_utc: {header.get('end_utc')}")
    lines.append(f"- wall_clock_secs: {header.get('wall_clock_secs')}")
    lines.append(f"- device: {header.get('device')} / precision: {header.get('precision')}")
    lines.append(f"- seed: {header.get('seed')}")
    lines.append(f"- config_identity_digest: {header.get('config_identity_digest')}")
    lines.append("")
    if disposition != "finished":
        # Honest non-success early return: header only; no metric-bearing sections.
        lines.append("The run did not complete.")
        lines.append("")
        return "\n".join(lines)
    lines.append("## Final losses")
    lines.append("")
    for term in _LOSS_TERMS:
        value = losses.get(term)
        lines.append(f"- {term}: {value if value is not None else 'null'}")
    lines.append("")
    lines.append("## Validation summary")
    lines.append("")
    if isinstance(validation, Mapping):
        value = validation.get("final_val_loss")
        lines.append(f"- final_val_loss: {value if value is not None else 'null'}")
        lines.append(f"- trend: {validation.get('trend') or 'unavailable'}")
        lines.append(f"- step: {validation.get('step')}")
    else:
        lines.append("- (validation records unavailable)")
    lines.append("")
    lines.append("## Curriculum progression")
    lines.append("")
    if curriculum:
        for rec in curriculum:
            stage = rec.get("stage")
            phase = rec.get("phase")
            step = rec.get("step")
            if any(field is not None for field in (stage, phase, step)):
                lines.append(f"- stage={stage} phase={phase} step={step}")
            else:
                lines.append(f"- {json.dumps(rec, sort_keys=True)}")
    else:
        lines.append("- (no curriculum records)")
    lines.append("")
    lines.append("## Test-set preview")
    lines.append("")
    if isinstance(test_preview, Mapping):
        eps_h = test_preview.get("eps_h")
        scs = test_preview.get("scs")
        lines.append(f"- eps_H: {eps_h if eps_h is not None else 'null'}")
        lines.append(f"- SCS: {scs if scs is not None else 'null'}")
        lines.append(f"- verdict: {test_preview.get('verdict') or 'unavailable'}")
        lines.append(
            f"- n_test_trajectories: {test_preview.get('n_test_trajectories')}"
        )
    else:
        lines.append("- (test metrics unavailable)")
    lines.append("")
    lines.append("## Comparison hint")
    lines.append("")
    if isinstance(comparison, Mapping):
        lines.append(f"- prior_run: {comparison.get('prior_run_name')}")
        lines.append(f"- current_eps_H: {comparison.get('current_eps_h')}")
        lines.append(f"- prior_eps_H: {comparison.get('prior_eps_h')}")
        lines.append(f"- current_verdict: {comparison.get('current_verdict')}")
        lines.append(f"- prior_verdict: {comparison.get('prior_verdict')}")
    else:
        lines.append("- (named prior summary unavailable)")
    lines.append("")
    lines.append("## Honesty notes")
    lines.append("")
    lines.extend(f"- {note}" for note in _HONESTY_NOTES)
    lines.append("")
    return "\n".join(lines)


def stub_summary(run_dir: PathLike, *, header: Optional[Mapping[str, Any]]) -> Path:
    """Write the honest launch-time stub ``summary.md`` + ``summary.json``.

    Marked "in progress / did not complete" with no fabricated metrics. Called once
    at run start so the one-pager is present under every death mode (E4). Both
    writes go through ``atomic_write_text``; ``summary.md`` is never absent after
    launch.
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    payload, md = _compose(
        run_dir=run_dir,
        disposition="in_progress",
        header=header,
        final_losses=None,
        curriculum=[],
    )
    atomic_write_text(
        run_dir / "summary.json",
        json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n",
    )
    atomic_write_text(run_dir / "summary.md", md)
    return run_dir / "summary.md"


def finalize_summary(
    run_dir: PathLike,
    *,
    disposition: str,
    header: Optional[Mapping[str, Any]],
    final_losses: Optional[Mapping[str, Any]],
    curriculum_path: Optional[PathLike],
    validation_records_path: Optional[PathLike] = None,
    metrics_path: Optional[PathLike] = None,
    prior_summary_path: Optional[PathLike] = None,
) -> Path:
    """Atomically replace ``summary.md`` + ``summary.json`` with the terminal one-pager.

    ``disposition`` ∈ {finished, failed, interrupted}. A finished run renders final
    losses + curriculum progression; a failed/interrupted run names the state and
    leaves metrics null (never placeholder numbers — must-NOT #1). The curriculum
    progression is rendered from ``curriculum_path`` (not recomputed). Both writes
    go through ``atomic_write_text``.
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    curriculum = (
        _render_curriculum(curriculum_path) if disposition == "finished" else []
    )
    payload, md = _compose(
        run_dir=run_dir,
        disposition=disposition,
        header=header,
        final_losses=final_losses,
        curriculum=curriculum,
        validation_records_path=validation_records_path,
        metrics_path=metrics_path,
        prior_summary_path=prior_summary_path,
    )
    atomic_write_text(
        run_dir / "summary.json",
        json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n",
    )
    atomic_write_text(run_dir / "summary.md", md)
    return run_dir / "summary.md"


def refresh_completed_summary(
    run_dir: PathLike,
    *,
    metrics_path: PathLike,
    validation_records_path: Optional[PathLike] = None,
    curriculum_path: Optional[PathLike] = None,
    prior_summary_path: Optional[PathLike] = None,
) -> Optional[Path]:
    """Refresh one already-finished run from committed evaluation artifacts.

    The existing ``summary.json`` is the sole source for the terminal run header
    and final losses. Missing/malformed summaries, non-success dispositions, and
    missing/malformed metrics are no-ops: evaluation must never turn a failed or
    interrupted run into a completed one, nor create a fabricated preview.
    """
    run_dir = Path(run_dir)
    existing = _read_json_mapping(run_dir / "summary.json")
    if existing is None or existing.get("disposition") != "finished":
        return None
    if _test_preview(metrics_path) is None:
        return None
    header = existing.get("header")
    losses = existing.get("final_losses")
    if not isinstance(header, Mapping) or not isinstance(losses, Mapping):
        return None
    return finalize_summary(
        run_dir,
        disposition="finished",
        header=header,
        final_losses=losses,
        curriculum_path=(
            curriculum_path
            if curriculum_path is not None
            else run_dir / "curriculum.jsonl"
        ),
        validation_records_path=(
            validation_records_path
            if validation_records_path is not None
            else run_dir / "validation.jsonl"
        ),
        metrics_path=metrics_path,
        prior_summary_path=prior_summary_path,
    )
