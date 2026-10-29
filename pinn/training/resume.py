"""Phase 41 / CTRL-05 — multi-module identity digest + fail-safe resume diff.

The resume config-diff compares a STRUCTURED, NAMED identity payload spanning
TrainingConfig identity fields, ArchitectureSpec, pinn.constants, and the
EFFECTIVE RuntimeSpec used at run start — NOT TrainingConfig alone.

Refuse decision is made by FIELD-LEVEL NAMED COMPARISON (not digest-only).
Any identity OR unclassified delta refuses; only explicitly-whitelisted
OPERATIONAL fields may differ.

B-5 / CTX-57 field classification is a ⚖ SURFACED PROPOSAL — owner-ratify
before run #1. The fail-safe unclassified→refuse RULE is LOCKED.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from pinn.constants import (
    D_CHARACTERISTIC_LENGTH,
    EPS_SOFT,
    T_CHARACTERISTIC_TIME,
)
from pinn.training.config_yaml import resolved_config_to_dict

PathLike = Union[str, Path]

# Coverage tags for IDENTITY categories (cycle-4 MEDIUM-3).
COVERAGE_REPRESENTED = "REPRESENTED"
COVERAGE_DEFERRED = "DEFERRED-NOT-REPRESENTABLE"

# Classification labels.
CLASS_IDENTITY = "IDENTITY"
CLASS_OPERATIONAL = "OPERATIONAL"
CLASS_UNCLASSIFIED = "UNCLASSIFIED"

# ⚖ PROVISIONAL — CTX-57 Conservative identity line + operational whitelist.
# Owner-ratify before run #1. Fail-safe: any field NOT in this registry
# defaults to UNCLASSIFIED → refuse.
# Each entry: {"class": ..., "coverage": ... (IDENTITY only), "provisional": True}
RESUME_FIELD_REGISTRY: dict[str, dict[str, Any]] = {
    # ---- IDENTITY (REPRESENTED — concrete fields in build_identity_payload) ----
    "run.seed": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.precision": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.device": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    # cycle-2 claude-max MEDIUM: explicit IDENTITY (not unclassified-default)
    "run.strict_cpu_determinism": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "stage.max_epochs": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.guards.loss_explosion_ceiling": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.guards.disk_floor_fraction": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "run.guards.memory_watermark_fraction": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.hidden_depth": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.hidden_width": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.first_omega_0": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.hidden_omega_0": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.skip_cadence": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.layernorm_elementwise_affine": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.layernorm_eps": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.power_p": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "arch.seed": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "constants.D": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "constants.eps_soft": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "constants.T": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "effective_runtime.precision": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    "effective_runtime.device": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_REPRESENTED,
        "provisional": True,
    },
    # ---- IDENTITY (DEFERRED-NOT-REPRESENTABLE — no v2.0 config source) ----
    "dataset.version_hash": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_DEFERRED,
        "provisional": True,
    },
    "dataset.ic_vector_definition": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_DEFERRED,
        "provisional": True,
    },
    "split.policy": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_DEFERRED,
        "provisional": True,
    },
    "loss_catalog.structure": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_DEFERRED,
        "provisional": True,
    },
    # curriculum/stage definitions beyond max_epochs (provisional location)
    "curriculum.stage_definitions": {
        "class": CLASS_IDENTITY,
        "coverage": COVERAGE_DEFERRED,
        "provisional": True,
    },
    # ---- OPERATIONAL whitelist (CTX-57) ----
    "run.checkpoint.every_n_steps": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "run.checkpoint.wall_clock_ceiling_s": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "run.checkpoint.rolling_keep": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "run.checkpoint.failure_keep": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "run.log_every": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "opt.validation_every": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
    "run.num_workers": {
        "class": CLASS_OPERATIONAL,
        "provisional": True,
    },
}

# Stage-final basename pattern for --hold-stage validation (cycle-4 MEDIUM-6).
_STAGE_FINAL_RE = re.compile(r"stage-\d+-final\.pt")


class ResumeConfigRefused(ValueError):
    """Raised when resume refuses due to identity or unclassified config drift.

    Message NAMES the changed field(s) — never a bare 'identity mismatch'.
    """

    def __init__(self, changed_fields: list[str], detail: str = "") -> None:
        self.changed_fields = list(changed_fields)
        fields_str = ", ".join(self.changed_fields) if self.changed_fields else "(unknown)"
        msg = f"resume refused: identity/unclassified config drift in [{fields_str}]"
        if detail:
            msg = f"{msg}; {detail}"
        super().__init__(msg)


class HoldStageTargetError(ValueError):
    """Raised when --hold-stage targets a non stage-{N}-final.pt path."""

    def __init__(self, target: PathLike) -> None:
        self.target = str(target)
        super().__init__(
            f"--hold-stage requires a stage-{{N}}-final.pt anchor; "
            f"got {self.target!r}"
        )


class IdentityCoverageError(ValueError):
    """Raised when IDENTITY coverage is incomplete or a real-data blind spot."""

    def __init__(self, category: str, reason: str = "") -> None:
        self.category = category
        msg = f"identity coverage error for {category!r}"
        if reason:
            msg = f"{msg}: {reason}"
        super().__init__(msg)


class RunFolderExistsError(ValueError):
    """Raised when a fresh launch would clobber an existing runs/<name>/."""

    def __init__(self, path: PathLike) -> None:
        self.path = str(path)
        super().__init__(
            f"run folder already exists (refuse to clobber): {self.path}"
        )


def _runtime_to_plain(spec: Any) -> Optional[dict[str, str]]:
    """Serialize a RuntimeSpec (or dict) to JSON-safe precision/device labels."""
    if spec is None:
        return None
    if isinstance(spec, Mapping):
        precision = spec.get("precision")
        device = spec.get("device") or spec.get("requested_device")
        if precision is None or device is None:
            return None
        return {"precision": str(precision), "device": str(device)}
    precision = getattr(spec, "precision", None)
    device = getattr(spec, "requested_device", None) or getattr(spec, "device", None)
    if precision is None or device is None:
        return None
    return {"precision": str(precision), "device": str(device)}


def _effective_runtime_from_config(config: Any) -> dict[str, str]:
    """Derive effective runtime labels from config without side-effect reseeding.

    When ``strict_cpu_determinism`` is True the forced pair is float64/cpu
    (matching ``apply_strict_cpu_determinism``); otherwise the config's
    precision/device pair is recorded as-is.
    """
    run = getattr(config, "run", config)
    if bool(getattr(run, "strict_cpu_determinism", False)):
        return {"precision": "float64", "device": "cpu"}
    return {
        "precision": str(getattr(run, "precision", "float32")),
        "device": str(getattr(run, "device", "mps")),
    }


def build_identity_payload(
    config: Any,
    arch_spec: Any,
    *,
    effective_runtime_spec: Any = None,
) -> dict[str, Any]:
    """Build a NAMED multi-module identity field map (NOT a pre-hashed digest).

    Spans TrainingConfig identity fields, ArchitectureSpec, pinn.constants,
    and the effective RuntimeSpec actually used at run start.
    """
    run = config.run
    stage = config.stage
    guards = run.guards

    if effective_runtime_spec is not None:
        eff = _runtime_to_plain(effective_runtime_spec)
    else:
        eff = _effective_runtime_from_config(config)
    if eff is None:
        eff = _effective_runtime_from_config(config)

    payload: dict[str, Any] = {
        "run.seed": int(run.seed),
        "run.precision": str(run.precision),
        "run.device": str(run.device),
        "run.strict_cpu_determinism": bool(run.strict_cpu_determinism),
        "stage.max_epochs": int(stage.max_epochs),
        "run.guards.loss_explosion_ceiling": float(guards.loss_explosion_ceiling),
        "run.guards.disk_floor_fraction": float(guards.disk_floor_fraction),
        "run.guards.memory_watermark_fraction": float(
            guards.memory_watermark_fraction
        ),
        "arch.hidden_depth": int(arch_spec.hidden_depth),
        "arch.hidden_width": int(arch_spec.hidden_width),
        "arch.first_omega_0": float(arch_spec.first_omega_0),
        "arch.hidden_omega_0": float(arch_spec.hidden_omega_0),
        "arch.skip_cadence": str(arch_spec.skip_cadence),
        "arch.layernorm_elementwise_affine": bool(
            arch_spec.layernorm_elementwise_affine
        ),
        "arch.layernorm_eps": float(arch_spec.layernorm_eps),
        "arch.power_p": int(arch_spec.power_p),
        "arch.seed": int(arch_spec.seed),
        "constants.D": float(D_CHARACTERISTIC_LENGTH),
        "constants.eps_soft": float(EPS_SOFT),
        "constants.T": float(T_CHARACTERISTIC_TIME),
        "effective_runtime.precision": str(eff["precision"]),
        "effective_runtime.device": str(eff["device"]),
    }
    return payload


def identity_digest(payload: Mapping[str, Any]) -> str:
    """sha256 of canonical JSON (sort_keys, compact separators) — fast-path check."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_config_identity_envelope(
    config: Any,
    arch_spec: Any,
    *,
    effective_runtime_spec: Any = None,
) -> dict[str, Any]:
    """Full config_identity structure stored in CTX-53 checkpoints."""
    identity_fields = build_identity_payload(
        config, arch_spec, effective_runtime_spec=effective_runtime_spec
    )
    eff = {
        "precision": identity_fields["effective_runtime.precision"],
        "device": identity_fields["effective_runtime.device"],
    }
    return {
        "digest": identity_digest(identity_fields),
        "identity_fields": identity_fields,
        "resolved_config_snapshot": resolved_config_to_dict(config),
        "effective_runtime": eff,
    }


def _classify_field(field_name: str) -> str:
    entry = RESUME_FIELD_REGISTRY.get(field_name)
    if entry is None:
        return CLASS_UNCLASSIFIED
    return str(entry.get("class", CLASS_UNCLASSIFIED))


def _flatten_dict(obj: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten nested mappings to dotted paths (leaves only)."""
    out: dict[str, Any] = {}
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, Mapping):
                out.update(_flatten_dict(value, path))
            else:
                out[path] = value
    return out


def _values_equal(a: Any, b: Any) -> bool:
    if a is b:
        return True
    if isinstance(a, float) or isinstance(b, float):
        try:
            return abs(float(a) - float(b)) < 1e-15
        except (TypeError, ValueError):
            return False
    return a == b


def resume_config_diff(
    incoming_config: Any,
    incoming_arch_spec: Any,
    checkpoint_config_identity: Mapping[str, Any],
    *,
    effective_runtime_spec: Any = None,
) -> None:
    """Field-level named resume diff — refuse on identity/unclassified delta.

    ``checkpoint_config_identity`` shape::

        {
          "digest": str,
          "identity_fields": dict,
          "resolved_config_snapshot": dict,
          "effective_runtime": dict,  # optional legacy
        }

    Fast path: matching digests AND matching resolved-config snapshots → proceed.
    Digest match with snapshot mismatch still runs the field walk (defense in depth).
    """
    if not isinstance(checkpoint_config_identity, Mapping):
        raise ResumeConfigRefused(
            ["config_identity"],
            detail=f"checkpoint config_identity must be a mapping "
            f"(got {type(checkpoint_config_identity)!r})",
        )

    incoming_payload = build_identity_payload(
        incoming_config,
        incoming_arch_spec,
        effective_runtime_spec=effective_runtime_spec,
    )
    incoming_digest = identity_digest(incoming_payload)
    stored_digest = checkpoint_config_identity.get("digest")
    stored_fields = checkpoint_config_identity.get("identity_fields") or {}
    stored_snapshot = checkpoint_config_identity.get("resolved_config_snapshot") or {}
    incoming_snapshot = resolved_config_to_dict(incoming_config)

    digest_match = stored_digest is not None and stored_digest == incoming_digest
    snapshot_match = stored_snapshot == incoming_snapshot

    if digest_match and snapshot_match:
        return  # fast path — no field walk

    # Field-level named diff across identity fields + flattened snapshots.
    deltas: list[tuple[str, Any, Any, str]] = []

    # 1) Identity payload fields (always compared by name).
    all_identity_keys = set(incoming_payload) | set(stored_fields)
    for key in sorted(all_identity_keys):
        new_v = incoming_payload.get(key, _MISSING)
        old_v = stored_fields.get(key, _MISSING)
        if new_v is _MISSING or old_v is _MISSING or not _values_equal(new_v, old_v):
            classification = _classify_field(key)
            deltas.append((key, old_v, new_v, classification))

    # 2) Flattened resolved-config snapshot (catches operational + unclassified).
    flat_in = _flatten_dict(incoming_snapshot)
    flat_stored = _flatten_dict(stored_snapshot)
    all_snap_keys = set(flat_in) | set(flat_stored)
    seen_identity = {d[0] for d in deltas}
    for key in sorted(all_snap_keys):
        if key in seen_identity or key in incoming_payload or key in stored_fields:
            # Already handled via identity payload (or will be if present).
            if key in incoming_payload or key in stored_fields:
                continue
        new_v = flat_in.get(key, _MISSING)
        old_v = flat_stored.get(key, _MISSING)
        if new_v is _MISSING or old_v is _MISSING or not _values_equal(new_v, old_v):
            classification = _classify_field(key)
            deltas.append((key, old_v, new_v, classification))

    if not deltas:
        return

    # Refuse on any identity OR unclassified; allow operational-only.
    refuse_fields = [
        name
        for name, _old, _new, cls in deltas
        if cls in (CLASS_IDENTITY, CLASS_UNCLASSIFIED)
    ]
    if refuse_fields:
        detail_parts = []
        for name, old_v, new_v, cls in deltas:
            if name in refuse_fields:
                detail_parts.append(
                    f"{name} ({cls}): {old_v!r} → {new_v!r}"
                )
        raise ResumeConfigRefused(refuse_fields, detail="; ".join(detail_parts))
    # All deltas operational → proceed.


_MISSING = object()


def load_resume_target(store: Any, resume_arg: PathLike) -> Any:
    """Route --resume to store.load_checkpoint (file) or load_latest (dir/latest).

    Assumes main() already validated path existence (except the literal
    ``latest``). Does not re-validate existence.

    Plan 65-03 (INST-08 d): the RETURNED payload is boundary-checked — a
    diagnostic envelope never leaves this function even if a non-production
    store returned one, surfacing as the NoValidCheckpointError-compatible
    ``DiagnosticCheckpointRefused``.
    """
    from pinn.training.checkpoint import DiagnosticCheckpointRefused
    from pinn.verification.diagnostic_guard import carries_diagnostic_marker

    arg = str(resume_arg)
    if arg == "latest":
        payload = store.load_latest()
    else:
        path = Path(arg)
        if path.is_file():
            payload = store.load_checkpoint(path)
        else:
            # Path was validated by main as existing; treat non-file/dir as
            # latest (directory and other forms route to load_latest()).
            payload = store.load_latest()
    if carries_diagnostic_marker(payload):
        raise DiagnosticCheckpointRefused(resume_arg)
    return payload


def validate_hold_stage_target(resume_arg: PathLike) -> None:
    """Fail-closed: --hold-stage requires basename stage-{N}-final.pt."""
    arg = str(resume_arg)
    if arg == "latest":
        raise HoldStageTargetError(arg)
    basename = os.path.basename(arg.rstrip("/"))
    if not basename or basename in (".", ".."):
        raise HoldStageTargetError(arg)
    # Directory path (no .pt suffix, or ends with path sep semantics).
    path = Path(arg)
    if path.is_dir() or (not basename.endswith(".pt") and path.suffix != ".pt"):
        # Also reject directories even when not yet on disk (basename has no .pt).
        if not basename.endswith(".pt"):
            raise HoldStageTargetError(arg)
    if not _STAGE_FINAL_RE.fullmatch(basename):
        raise HoldStageTargetError(arg)


def identity_coverage_check(
    registry: Mapping[str, Mapping[str, Any]],
    payload: Mapping[str, Any],
    *,
    has_dataset: bool = False,
) -> None:
    """Assert every IDENTITY category is REPRESENTED or DEFERRED-NOT-REPRESENTABLE.

    With ``has_dataset=True``, any DEFERRED IDENTITY category is a pre-run
    blocker (resume drift would be undetectable).
    """
    for name, entry in registry.items():
        if entry.get("class") != CLASS_IDENTITY:
            continue
        coverage = entry.get("coverage")
        if coverage == COVERAGE_REPRESENTED:
            # Must have a concrete field in the payload. Registry key may equal
            # the payload key, or the category may be a parent of payload keys.
            if name not in payload and not any(
                k == name or k.startswith(name + ".") for k in payload
            ):
                # Category-level keys (e.g. arch.* covered by arch.hidden_depth)
                # — if the registry key itself is the payload key, require it.
                # For leaf registry keys that ARE payload keys, require presence.
                # DEFERRED categories use different names; REPRESENTED leaves
                # must appear.
                if "." in name and name not in payload:
                    # Leaf not present — bug.
                    raise IdentityCoverageError(
                        name,
                        "REPRESENTED IDENTITY category missing from payload",
                    )
            continue
        if coverage == COVERAGE_DEFERRED:
            if has_dataset:
                raise IdentityCoverageError(
                    name,
                    "DEFERRED-NOT-REPRESENTABLE IDENTITY category present "
                    "with has_dataset=True (undetectable resume drift)",
                )
            continue
        raise IdentityCoverageError(
            name,
            "IDENTITY category is neither REPRESENTED nor "
            "DEFERRED-NOT-REPRESENTABLE",
        )


def resume_field_classification_provisional_entry() -> dict[str, Any]:
    """⚖ provisional_fields() entry for the B-5 registry seam."""
    return {
        "name": "resume_field_classification_registry",
        "value": "PROVISIONAL",
        "provisional": True,
        "provenance": (
            "⚖ PROVISIONAL (B-5 / CTX-57 Conservative identity line): "
            "RESUME_FIELD_REGISTRY in pinn.training.resume covers architecture, "
            "IC-vector+dataset version/hash, loss-catalog+constants, seed, "
            "precision+device, strict_cpu_determinism, curriculum/stage, split "
            "policy, MAX_EPOCHS, guard thresholds + operational whitelist. "
            "Unclassified→refuse is LOCKED. Exact field-location mapping for "
            "DEFERRED categories (dataset/split/loss-catalog) is owner-carved "
            "before run #1 — not silently reduced."
        ),
    }


__all__ = [
    "CLASS_IDENTITY",
    "CLASS_OPERATIONAL",
    "CLASS_UNCLASSIFIED",
    "COVERAGE_DEFERRED",
    "COVERAGE_REPRESENTED",
    "HoldStageTargetError",
    "IdentityCoverageError",
    "RESUME_FIELD_REGISTRY",
    "ResumeConfigRefused",
    "RunFolderExistsError",
    "build_config_identity_envelope",
    "build_identity_payload",
    "identity_coverage_check",
    "identity_digest",
    "load_resume_target",
    "resume_config_diff",
    "resume_field_classification_provisional_entry",
    "validate_hold_stage_target",
]
