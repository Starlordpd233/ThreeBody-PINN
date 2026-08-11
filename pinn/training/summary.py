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
import math
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

# Phase 46 gate keys projected verbatim from the last validation record (D-19).
# Persisted-bytes passthrough: never recomputed, never null-collapsed (D-20).
_GATE_KEYS = (
    "gate_schema_version",
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
)

# Fixed render order for summary.md (differs from _GATE_KEYS: metrics first).
_GATE_MD_ORDER = (
    "gate_eps_h",
    "gate_scs",
    "gate_verdict",
    "gate_status",
    "gate_n_trajectories",
    "gate_n_nonfinite",
    "gate_sidecar",
    "gate_schema_version",
)

# Phase 49 conformance fields are projected from the validated preflight artifact
# without borrowing Phase 46's gate_* vocabulary (D-27/D-28).  The nested
# artifact's schema_version/preflight_status/assertions names are persisted
# contract fields, so this tuple is intentionally a direct key list rather than
# a recomputed summary schema.
_CONFORMANCE_KEYS = (
    "schema_version",
    "preflight_status",
    "assertions",
)

# Fixed render order keeps summary.md stable while preserving the full payload
# in summary.json.  Assertions are rendered last because they carry the open
# caveat records a human needs to inspect.
_CONFORMANCE_MD_ORDER = (
    "preflight_status",
    "assertions",
    "schema_version",
)

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


def _read_latest_validation_event(
    path: Optional[PathLike],
) -> "tuple[bool, Optional[Dict[str, Any]]]":
    """``(present, value)`` for the PHYSICAL latest validation.jsonl line.

    Never falls back past an invalid latest line to an older valid one
    (D-19/CR-05/T-46-10-07):

    * a missing file, or a file with no lines at all, is the legacy
      "missing/empty" state -- ``(False, None)``, which keeps the existing
      ``validation=None`` projection;
    * a present PHYSICAL latest line (the last entry ``str.splitlines()``
      returns) that is blank-only, malformed JSON, torn, or decodes to a
      non-mapping -- ``(True, None)``: the caller renders the existing
      12-key block with every persisted field null and
      ``eval01_precondition_iii`` False;
    * a present, well-formed mapping latest line -- ``(True, <the mapping>)``.
    """
    if path is None:
        return False, None
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return False, None
    except UnicodeDecodeError:
        # Undecodable bytes are a TORN physical write, not an absent stream:
        # UnicodeDecodeError is a ValueError, not an OSError, so without this
        # branch it escapes the honesty layer entirely and no summary is
        # written at all (finish_run wraps finalize_summary in a bare
        # try/finally). Fail closed as present-but-invalid, which is the same
        # projection a torn JSON line already gets (D-19/CR-05).
        return True, None
    lines = text.splitlines()
    if not lines:
        return False, None
    latest = lines[-1]
    if not latest.strip():
        # Blank-only content IS physically present at the latest position --
        # an invalid/ineligible event, never treated as absent.
        return True, None
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        return True, None
    if not isinstance(value, Mapping):
        return True, None
    return True, dict(value)


def _json_scalar_equal(a: Any, b: Any) -> bool:
    """Type-AND-value equality for JSON-decoded scalars (T-46-10-08).

    ``bool`` is a distinct JSON type from ``int``/``float``: ``False``/``0``
    and ``True``/``1`` must never compare equal. An ``int`` is a distinct
    JSON type from an equal-valued ``float`` (``json.loads`` never blends
    them). A numeric string is never a number. Plain ``==`` alone cannot
    express this because Python's ``bool``/``int``/``float`` interoperate
    under ``==`` by design.
    """
    return type(a) is type(b) and a == b


def _eval01_precondition_iii(
    record: Mapping[str, Any], path: Optional[PathLike]
) -> bool:
    """True only for the SAME event's exact, contained, fully valid sidecar.

    Fail-closed eligibility render (D-19/D-20/CR-03): every identity, schema,
    and value check binds the JSONL record to ONE durable, semantically
    valid receipt at the run's own exact step-derived path -- never an
    arbitrary, cross-run, wrong-step, or partially matching sidecar. It
    reads and re-validates persisted bytes; it never recomputes eps_H, SCS,
    or the verdict itself (that recomputation lives in
    ``validation_gate.validate_sidecar_payload``). The validator import is
    function-local on purpose — summary.py is the stdlib-only honesty layer
    rendered under EVERY death mode, while ``pinn.training.validation_gate``
    transitively imports torch via gate_metrics, so an ImportError degrades
    the flag to False instead of breaking the terminal summary render. Any
    import, read, parse, validation, identity, or equality failure renders
    False -- never raises.
    """
    if path is None:
        return False
    try:
        from pinn.training import validation_gate as vg

        final_val_loss = record.get("final_val_loss")
        if isinstance(final_val_loss, bool) or not isinstance(final_val_loss, (int, float)):
            return False
        if not math.isfinite(float(final_val_loss)):
            return False

        step = record.get("step")
        if isinstance(step, bool) or not isinstance(step, int) or step < 0:
            return False

        if record.get("gate_status") != "ok":
            return False

        expected_rel = vg.sidecar_relative_path(step)
        if record.get("gate_sidecar") != expected_rel:
            return False

        run_dir = Path(path).resolve().parent
        candidate = (run_dir / expected_rel).resolve()
        candidate.relative_to(run_dir)
        if not candidate.is_file():
            return False

        payload = json.loads(candidate.read_text(encoding="utf-8"))
        fields = vg.compact_validation_fields_from_payload(
            payload,
            expected_run_dir_name=run_dir.name,
            expected_global_step=step,
            expected_sidecar_path=expected_rel,
        )
        for key in _GATE_KEYS:
            if not _json_scalar_equal(record.get(key), fields[key]):
                return False
        return True
    except Exception:
        return False


def _conformance_run_dir(path: PathLike) -> Path:
    """Resolve either a run directory or its ``preflight.json`` path."""
    candidate = Path(path)
    if candidate.name == "preflight.json":
        return candidate.parent
    return candidate


def _conformance_record(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Load the persisted preflight payload without projecting a second schema.

    The conformance artifact is optional for a run that refused before preflight
    could write it, so absence becomes ``None``.  Import and validation failures
    are also fail-closed here: the terminal summary must remain renderable even
    when a hand-edited or torn artifact cannot be loaded.
    """
    if path is None:
        return None
    try:
        from pinn.conformance import preflight

        return preflight.load_preflight(_conformance_run_dir(path))
    except Exception:
        return None


def _eval01_precondition_i(path: Optional[PathLike]) -> bool:
    """Return the fail-closed EVAL-01 precondition-(i) standing.

    The loader import, artifact read, parse, and validation all live inside the
    fail-closed boundary so no death mode can make summary rendering raise.
    The eligibility predicate itself lives behind the ``pinn/conformance/``
    module boundary (D-32) as ``preflight.evaluate_eval01_precondition_i``;
    summary loads fail-closed and delegates.  The divergence-vs-qualification
    filter rationale (D-23/D-26) lives on that predicate.
    """
    if path is None:
        return False
    try:
        from pinn.conformance import preflight

        payload = preflight.load_preflight(_conformance_run_dir(path))
        return bool(preflight.evaluate_eval01_precondition_i(payload))
    except Exception:
        return False


def _validation_summary(path: Optional[PathLike]) -> Optional[Dict[str, Any]]:
    """Project the PHYSICAL latest validation event; never fall back (D-19).

    Missing/empty input keeps the legacy ``None`` projection. A present but
    blank/malformed/torn/non-mapping latest line renders the existing 12-key
    block with every persisted field null and eligibility False -- it is
    NEVER skipped in favor of an older, valid record (CR-05/T-46-10-06/07).
    """
    present, record = _read_latest_validation_event(path)
    if not present:
        return None
    if record is None:
        summary: Dict[str, Any] = {"final_val_loss": None, "trend": None, "step": None}
        for key in _GATE_KEYS:
            summary[key] = None
        summary["eval01_precondition_iii"] = False
        return summary
    final_val_loss = _null_if_nonfinite(record.get("final_val_loss"))
    trend = record.get("trend")
    if not isinstance(trend, str) or not trend:
        trend = None
    step = record.get("step")
    summary = {
        "final_val_loss": final_val_loss,
        "trend": trend,
        "step": step,
    }
    # Gate fields pass through UNCHANGED — a finite number or a string sentinel.
    # _null_if_nonfinite must NOT touch them: collapsing "Infinity" to null would
    # render a metric FAIL as missing data (D-20). Absent keys (pre-Phase-46
    # records) default to None.
    for key in _GATE_KEYS:
        summary[key] = record.get(key)
    summary["eval01_precondition_iii"] = _eval01_precondition_iii(record, path)
    return summary


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
    conformance = _conformance_record(run_dir)
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
        # D-27 deliberately differs from the success-gated validation and
        # curriculum projections: a refused run's persisted preflight evidence
        # is exactly the caveat record INST-03 requires to travel with the run.
        "conformance": conformance,
        "eval01_precondition_i": _eval01_precondition_i(run_dir),
        "curriculum": curriculum if success else [],
        "test_preview": preview,
        "comparison": (
            _comparison_hint(prior_summary_path, current_preview=preview)
            if success
            else None
        ),
    }
    return payload, _render_md(payload)


def _render_conformance_section(
    lines: List[str],
    conformance: Any,
    eval01_precondition_i: Any,
) -> None:
    """Append the fixed-order Conformance section to ``summary.md``."""
    lines.append("## Conformance")
    lines.append("")
    if isinstance(conformance, Mapping):
        for key in _CONFORMANCE_MD_ORDER:
            value = conformance.get(key)
            if value is None:
                rendered = "null"
            elif isinstance(value, (Mapping, list)):
                rendered = json.dumps(value, sort_keys=True)
            else:
                rendered = str(value)
            lines.append(f"- {key}: {rendered}")
    else:
        lines.append("- (conformance record unavailable)")
    lines.append(f"- eval01_precondition_i: {bool(eval01_precondition_i)}")
    lines.append("")


def _render_md(payload: Mapping[str, Any]) -> str:
    """Render the human-readable one-pager (no env-fingerprint, no absolute paths)."""
    disposition = payload["disposition"]
    header: Mapping[str, Any] = payload["header"]
    losses: Mapping[str, Any] = payload["final_losses"]
    curriculum: List[Dict[str, Any]] = payload["curriculum"]
    validation = payload.get("validation")
    conformance = payload.get("conformance")
    eval01_precondition_i = payload.get("eval01_precondition_i", False)
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
        _render_conformance_section(lines, conformance, eval01_precondition_i)
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
        for key in _GATE_MD_ORDER:
            gate_value = validation.get(key)
            lines.append(f"- {key}: {gate_value if gate_value is not None else 'null'}")
        lines.append(
            "- eval01_precondition_iii: "
            f"{bool(validation.get('eval01_precondition_iii'))}"
        )
    else:
        lines.append("- (validation records unavailable)")
    lines.append("")
    _render_conformance_section(lines, conformance, eval01_precondition_i)
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
