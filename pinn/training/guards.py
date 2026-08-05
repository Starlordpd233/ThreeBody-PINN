"""Phase 41 / CTRL-07 — Tier-1+2 auto-guard callback + disk-floor-safe failure/.

Per-step guards (CTX-60) trip into the EXISTING stage-exit RECOVER/HALT seam
via ``StageDisposition`` — this module does NOT mint a new disposition type.

Family → disposition mapping (LOW-1, mechanism default — not an R-1 threshold):
  * Tier-1 NaN/Inf            → RECOVER  (transient-numeric)
  * Tier-2 loss-explosion     → RECOVER  (transient-numeric)
  * Tier-2 disk-floor         → HALT     (resource-exhaustion)
  * Tier-2 memory-watermark   → HALT     (resource-exhaustion)

Threshold VALUES are ⚖ provisional and read from the injected ``run.guards``
config (R-1); they are NEVER hard-coded as ratified numbers. The family →
disposition assignment is the mechanism default grounded in
``transient-numeric → RECOVER, resource-exhaustion → HALT``.

Failure bundle (CTX-61): Tier-A (README.txt + trip.json, scalar-only) always;
Tier-B (tail.log + last-good-checkpoint / config.yaml references) best-effort.
No raw tensor/grad dumps so the bundle stays writable at the disk floor.
"""

from __future__ import annotations

import json
import math
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence, Union

from pinn.training.atomic_io import atomic_write_text
from pinn.training.stage_exit import StageDisposition

PathLike = Union[str, Path]

# ⚖ Platform capacity for the M5 Pro unified-memory default — injectable so
# unit tests and non-24 GB hosts can override. NOT a universal constant; the
# value is recorded in trip.json as provenance, never presented as ratified.
_DEFAULT_MEMORY_TOTAL_BYTES = 24 * (1024 ** 3)  # 24 GB M5 Pro platform value

# Guard evaluation order (first-tripped-wins for primary name; HALT wins
# disposition when a RECOVER-family and a HALT-family trip coincide).
_GUARD_ORDER = (
    "nan_inf",
    "loss_explosion",
    "disk_floor",
    "memory_watermark",
    "invariant_a",
    "invariant_b",
    "causal_stats_missing",
)

_HALT_FAMILY = frozenset(
    {
        "disk_floor",
        "memory_watermark",
        "invariant_a",
        "invariant_b",
        "causal_stats_missing",
    }
)
_RECOVER_FAMILY = frozenset({"nan_inf", "loss_explosion"})

_TAIL_LOG_LINES = 200


def _as_path(path: PathLike) -> Path:
    return path if isinstance(path, Path) else Path(path)


def _extract_guard_thresholds(config: Any) -> Mapping[str, float]:
    """Duck-typed extraction of ⚖ guard thresholds from an injected config.

    Accepts:
      * an object with ``.guards`` exposing the three threshold attributes
        (``RunConfig`` / ``TrainingConfig.run`` / nested SimpleNamespace)
      * an object exposing the three attributes directly (``GuardConfig``)
      * a ``TrainingConfig``-like object with ``.run.guards``
    """
    guards_obj: Any = None
    if hasattr(config, "run") and hasattr(getattr(config, "run"), "guards"):
        guards_obj = config.run.guards
    elif hasattr(config, "guards"):
        guards_obj = config.guards
    else:
        guards_obj = config

    try:
        return {
            "loss_explosion_ceiling": float(guards_obj.loss_explosion_ceiling),
            "disk_floor_fraction": float(guards_obj.disk_floor_fraction),
            "memory_watermark_fraction": float(guards_obj.memory_watermark_fraction),
        }
    except AttributeError as exc:
        raise TypeError(
            "StepGuards config must expose loss_explosion_ceiling, "
            "disk_floor_fraction, and memory_watermark_fraction "
            f"(got {type(config)!r} / guards={type(guards_obj)!r})"
        ) from exc


def _extract_invariant_window(config: Any) -> Optional[int]:
    """Read the optional owner-owned invariant-B window from a config.

    The fallback chain keeps StepGuards usable with the duck-typed test
    configs used by Phase 41, which do not have a ``run.invariants`` section.
    """
    run_obj = getattr(config, "run", None)
    if run_obj is None:
        run_obj = config
    invariants = getattr(run_obj, "invariants", None)
    if invariants is None and run_obj is not config:
        invariants = getattr(config, "invariants", None)
    window = getattr(invariants, "front_advance_window_n", None)
    if window is None:
        return None
    if not isinstance(window, int) or isinstance(window, bool) or window <= 0:
        raise ValueError(
            "front_advance_window_n must be a positive int or None "
            f"(got {window!r})"
        )
    return int(window)


def _is_nonfinite(value: Any) -> bool:
    if value is None:
        return False
    try:
        v = float(value)
    except (TypeError, ValueError):
        return False
    return not math.isfinite(v)


def _loss_total(loss_terms: Optional[Mapping[str, Any]]) -> Optional[float]:
    if not loss_terms:
        return None
    if "total" in loss_terms:
        try:
            return float(loss_terms["total"])
        except (TypeError, ValueError):
            return None
    # Fall back to summing finite scalar terms if "total" is absent.
    acc = 0.0
    saw = False
    for v in loss_terms.values():
        try:
            fv = float(v)
        except (TypeError, ValueError):
            continue
        if math.isfinite(fv):
            acc += fv
            saw = True
    return acc if saw else None


def _json_safe_scalar(value: Any) -> Any:
    """Convert a scalar for JSON: non-finite floats → string sentinel."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, str)):
        return value
    try:
        fv = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(fv):
        if math.isnan(fv):
            return "NaN"
        return "Inf" if fv > 0 else "-Inf"
    return fv


def _default_memory_signal() -> Optional[int]:
    """Read MPS driver-allocated memory; None when the API is unavailable.

    RESEARCH Open Question 2 recommendation: ``torch.mps.driver_allocated_memory``
    rather than ``resource.getrusage().ru_maxrss`` (macOS bytes-vs-KB gotcha).

    Phase-40 training-module ban: no ``.is_available()`` probe — try the API
    and treat any failure as "signal unavailable" (None / Tier-B skip).
    """
    try:
        import torch
    except ImportError:
        return None
    if not hasattr(torch, "mps"):
        return None
    try:
        return int(torch.mps.driver_allocated_memory())
    except Exception:
        return None


@dataclass(frozen=True)
class GuardOutcome:
    """Result of one per-step guard poll.

    ``disposition is None`` means no trip — keep training. Otherwise the
    disposition is the per-family StageDisposition (RECOVER or HALT), never a
    uniform RECOVER, so 41-04 can journal a HALT-family trip as HALT.
    """

    disposition: Optional[StageDisposition]
    guard: Optional[str] = None
    tier: Optional[int] = None
    metric: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None
    threshold_provisional: bool = True
    step: Optional[int] = None
    stage: Optional[int] = None
    phase: Optional[str] = None
    reason: str = ""
    tripped_guards: tuple[str, ...] = ()
    loss_terms: Optional[Mapping[str, Any]] = None
    grad_norm: Optional[float] = None
    extras: Mapping[str, Any] = field(default_factory=dict)


class StepGuards:
    """Per-step Tier-1+2 auto-guard callback (CTX-60).

    Config is duck-typed: any object exposing the three ⚖ guard thresholds
    (directly or via ``.guards`` / ``.run.guards``) works. Thresholds are
    NEVER hard-coded here — they are injected so the mechanism implements the
    FORM, not a calibrated pass level (R-1 provisional).

    ``memory_total_bytes`` and ``memory_signal`` are injectable so unit tests
    and non-M5-Pro hosts can drive the memory-watermark guard without 24 GB
    unified memory or ``torch.mps`` (MEDIUM fix from cross-AI review).
    """

    def __init__(
        self,
        config: Any,
        *,
        disk_root: Optional[PathLike] = None,
        memory_total_bytes: Optional[int] = None,
        memory_signal: Optional[Callable[[], Optional[int]]] = None,
    ) -> None:
        self._thresholds = dict(_extract_guard_thresholds(config))
        self._front_advance_window_n = _extract_invariant_window(config)
        self.front_high_water = -1
        self.last_advance_step: Optional[int] = None
        self._disk_root = _as_path(disk_root) if disk_root is not None else Path(".")
        self._memory_total_bytes = (
            int(memory_total_bytes)
            if memory_total_bytes is not None
            else _DEFAULT_MEMORY_TOTAL_BYTES
        )
        if self._memory_total_bytes <= 0:
            raise ValueError(
                f"memory_total_bytes must be positive (got {self._memory_total_bytes!r})"
            )
        self._memory_signal = (
            memory_signal if memory_signal is not None else _default_memory_signal
        )

    @property
    def thresholds(self) -> Mapping[str, float]:
        """Read-only view of the injected ⚖ thresholds (for tests / logging)."""
        return dict(self._thresholds)

    def invariant_b_state_dict(self) -> dict[str, Any]:
        """Return JSON-serializable cross-step state for invariant B."""
        return {
            "front_high_water": int(self.front_high_water),
            "last_advance_step": (
                None
                if self.last_advance_step is None
                else int(self.last_advance_step)
            ),
        }

    def load_invariant_b_state(self, state: Mapping[str, Any]) -> None:
        """Restore invariant-B cross-step state from a checkpoint mapping."""
        if not isinstance(state, Mapping):
            raise TypeError(
                f"invariant B state must be a mapping (got {type(state)!r})"
            )
        high_water = state.get("front_high_water")
        last_step = state.get("last_advance_step")
        if (
            not isinstance(high_water, int)
            or isinstance(high_water, bool)
            or high_water < -1
        ):
            raise ValueError(
                "invariant B front_high_water must be an int >= -1 "
                f"(got {high_water!r})"
            )
        if last_step is not None and (
            not isinstance(last_step, int) or isinstance(last_step, bool) or last_step < 0
        ):
            raise ValueError(
                "invariant B last_advance_step must be a non-negative int or None "
                f"(got {last_step!r})"
            )
        self.front_high_water = int(high_water)
        self.last_advance_step = None if last_step is None else int(last_step)

    def check(
        self,
        step: int,
        stage: int,
        phase: str,
        loss_terms: Optional[Mapping[str, Any]] = None,
        grad_norm: Optional[float] = None,
        *,
        disk_root: Optional[PathLike] = None,
        w_n_stats: Optional[Mapping[str, Any]] = None,
        n_colloc: Optional[int] = None,
        physics_evaluated: bool = False,
    ) -> GuardOutcome:
        """Evaluate Tier-1 then Tier-2 guards; return one coherent outcome.

        Order: NaN/Inf first (mirrors ``StageExitMachine``'s ``had_nan_inf``-
        first), then loss-explosion, disk-floor, memory-watermark. A step-0
        trip is handled with no prior-step assumption. Simultaneous multi-
        guard trips yield ONE outcome; if a HALT-family and a RECOVER-family
        trip coincide, HALT wins (never downgraded to RECOVER).
        """
        root = _as_path(disk_root) if disk_root is not None else self._disk_root
        trips: list[dict[str, Any]] = []

        # ---- Tier-1: NaN/Inf in loss terms or gradient (RECOVER) ----
        nan_metric: Optional[str] = None
        nan_value: Optional[float] = None
        if loss_terms:
            for key, val in loss_terms.items():
                if _is_nonfinite(val):
                    nan_metric = f"loss.{key}"
                    try:
                        nan_value = float(val)
                    except (TypeError, ValueError):
                        nan_value = float("nan")
                    break
        if nan_metric is None and _is_nonfinite(grad_norm):
            nan_metric = "grad_norm"
            nan_value = float(grad_norm)  # type: ignore[arg-type]
        if nan_metric is not None:
            trips.append(
                {
                    "guard": "nan_inf",
                    "tier": 1,
                    "metric": nan_metric,
                    "value": nan_value,
                    "threshold": None,
                    "disposition": StageDisposition.RECOVER,
                    "reason": f"NaN/Inf in {nan_metric}",
                }
            )

        # ---- Tier-2: loss-explosion (RECOVER) ----
        ceiling = float(self._thresholds["loss_explosion_ceiling"])
        total = _loss_total(loss_terms)
        if total is not None and math.isfinite(total) and total > ceiling:
            trips.append(
                {
                    "guard": "loss_explosion",
                    "tier": 2,
                    "metric": "loss.total",
                    "value": total,
                    "threshold": ceiling,
                    "disposition": StageDisposition.RECOVER,
                    "reason": (
                        f"loss total {total} > ⚖ ceiling {ceiling}"
                    ),
                }
            )

        # ---- Tier-2: disk-floor (HALT) ----
        floor = float(self._thresholds["disk_floor_fraction"])
        try:
            usage = shutil.disk_usage(str(root))
            free_frac = float(usage.free) / float(usage.total) if usage.total else 0.0
        except OSError:
            free_frac = None
        if free_frac is not None and free_frac < floor:
            trips.append(
                {
                    "guard": "disk_floor",
                    "tier": 2,
                    "metric": "disk_free_fraction",
                    "value": free_frac,
                    "threshold": floor,
                    "disposition": StageDisposition.HALT,
                    "reason": (
                        f"disk free fraction {free_frac} < ⚖ floor {floor}"
                    ),
                }
            )

        # ---- Tier-2: memory-watermark (HALT) ----
        mem_frac_thr = float(self._thresholds["memory_watermark_fraction"])
        allocated: Optional[int]
        try:
            allocated = self._memory_signal()
        except Exception:
            allocated = None
        extras: dict[str, Any] = {
            "memory_total_bytes": self._memory_total_bytes,
        }
        if allocated is None:
            extras["memory_signal"] = "SKIPPED-MPS-UNAVAILABLE"
        else:
            mem_frac = float(allocated) / float(self._memory_total_bytes)
            extras["memory_allocated_bytes"] = int(allocated)
            if mem_frac > mem_frac_thr:
                trips.append(
                    {
                        "guard": "memory_watermark",
                        "tier": 2,
                        "metric": "memory_fraction",
                        "value": mem_frac,
                        "threshold": mem_frac_thr,
                        "disposition": StageDisposition.HALT,
                        "reason": (
                            f"memory fraction {mem_frac} > ⚖ watermark "
                            f"{mem_frac_thr}"
                        ),
                    }
                )

        # ---- GATE-03 causal statistics + invariants (HALT) ----
        if physics_evaluated:
            required_stats = ("w_min", "w_mean", "w_max", "front_idx")
            if not isinstance(w_n_stats, Mapping) or any(
                key not in w_n_stats for key in required_stats
            ):
                trips.append(
                    {
                        "guard": "causal_stats_missing",
                        "tier": 2,
                        "metric": "w_n_stats",
                        "value": None,
                        "threshold": None,
                        "disposition": StageDisposition.HALT,
                        "reason": (
                            "causal statistics missing on a physics-evaluated step"
                        ),
                    }
                )
            else:
                invalid_metric: Optional[str] = None
                invalid_value: Any = None
                for key in ("w_min", "w_mean", "w_max"):
                    try:
                        numeric = float(w_n_stats[key])
                    except (TypeError, ValueError):
                        numeric = float("nan")
                    if not math.isfinite(numeric):
                        invalid_metric = key
                        invalid_value = w_n_stats[key]
                        break
                if invalid_metric is None:
                    try:
                        w_min = float(w_n_stats["w_min"])
                        front_idx = int(w_n_stats["front_idx"])
                    except (TypeError, ValueError):
                        invalid_metric = "front_idx"
                        invalid_value = w_n_stats["front_idx"]
                    else:
                        if w_min <= 0.0:
                            invalid_metric = "w_min"
                            invalid_value = w_min
                        elif front_idx == -1:
                            invalid_metric = "front_idx"
                            invalid_value = front_idx
                if invalid_metric is not None:
                    threshold = 0.0 if invalid_metric == "w_min" else None
                    if invalid_metric == "front_idx":
                        reason = "causal front_idx sentinel/invalid value"
                    else:
                        reason = f"invalid causal weight statistic: {invalid_metric}"
                    trips.append(
                        {
                            "guard": "invariant_a",
                            "tier": 2,
                            "metric": f"w_n_stats.{invalid_metric}",
                            "value": invalid_value,
                            "threshold": threshold,
                            "disposition": StageDisposition.HALT,
                            "reason": reason,
                        }
                    )
                else:
                    # Invariant B is evaluated only from a valid physics
                    # statistics sample.  Its state is a monotone high-water
                    # mark: transient front regressions never reset the age.
                    if self.front_high_water < 0:
                        self.front_high_water = front_idx
                        self.last_advance_step = int(step)
                    elif front_idx > self.front_high_water:
                        self.front_high_water = front_idx
                        self.last_advance_step = int(step)

                    if (
                        self._front_advance_window_n is not None
                        and self.last_advance_step is not None
                        and isinstance(n_colloc, int)
                        and not isinstance(n_colloc, bool)
                        and n_colloc > 0
                    ):
                        age = int(step) - int(self.last_advance_step)
                        saturated = self.front_high_water >= int(n_colloc) - 1
                        if age > self._front_advance_window_n and not saturated:
                            trips.append(
                                {
                                    "guard": "invariant_b",
                                    "tier": 2,
                                    "metric": "steps_since_front_advance",
                                    "value": age,
                                    "threshold": self._front_advance_window_n,
                                    "threshold_provisional": False,
                                    "disposition": StageDisposition.HALT,
                                    "reason": (
                                        "causal front high-water mark did not advance "
                                        f"within N={self._front_advance_window_n} steps"
                                    ),
                                }
                            )

        gnorm = _as_optional_float(grad_norm)

        if not trips:
            return GuardOutcome(
                disposition=None,
                step=int(step),
                stage=int(stage),
                phase=str(phase),
                loss_terms=dict(loss_terms) if loss_terms else None,
                grad_norm=gnorm,
                extras=extras,
            )

        # Order trips by _GUARD_ORDER for primary selection.
        order_index = {name: i for i, name in enumerate(_GUARD_ORDER)}
        trips.sort(key=lambda t: order_index.get(t["guard"], 99))
        tripped_names = tuple(t["guard"] for t in trips)

        # Disposition: HALT wins over RECOVER if both families present.
        has_halt = any(t["guard"] in _HALT_FAMILY for t in trips)
        if has_halt:
            # Prefer the first HALT-family trip as the primary record.
            primary = next(t for t in trips if t["guard"] in _HALT_FAMILY)
            disposition = StageDisposition.HALT
        else:
            primary = trips[0]
            disposition = StageDisposition.RECOVER

        return GuardOutcome(
            disposition=disposition,
            guard=str(primary["guard"]),
            tier=int(primary["tier"]),
            metric=str(primary["metric"]) if primary["metric"] is not None else None,
            value=_as_optional_float(primary["value"]),
            threshold=_as_optional_float(primary["threshold"]),
            threshold_provisional=bool(primary.get("threshold_provisional", True)),
            step=int(step),
            stage=int(stage),
            phase=str(phase),
            reason=str(primary["reason"]),
            tripped_guards=tripped_names,
            loss_terms=dict(loss_terms) if loss_terms else None,
            grad_norm=gnorm,
            extras=extras,
        )


def _as_optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def write_failure_bundle(
    run_dir: PathLike,
    trip_info: Union[GuardOutcome, Mapping[str, Any]],
    *,
    log_lines: Optional[Sequence[str]] = None,
    last_good_checkpoint: Optional[PathLike] = None,
    last_good_digest: Optional[str] = None,
    config_yaml_path: Optional[PathLike] = None,
) -> Path:
    """Write the always-on failure/ diagnostic bundle (CTX-61).

    Tier-A (always): ``failure/README.txt`` (one line) + ``failure/trip.json``
    (scalar-only fields). Tier-B (best-effort, failures swallowed):
    ``failure/tail.log`` (~last 200 lines) + last-good-checkpoint reference +
    config.yaml reference. Never dumps raw tensors/gradients.

    NOTE: this owns the DIAGNOSTIC text/json bundle only. The failure
    checkpoint (``.pt`` model/optimizer/RNG state) is a SEPARATE artifact
    saved by the guard_hook via ``store.save_anchor`` (41-02/41-04).
    """
    root = _as_path(run_dir)
    fail_dir = root / "failure"
    fail_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(trip_info, GuardOutcome):
        info = _outcome_to_trip_dict(trip_info)
    else:
        info = dict(trip_info)

    # Attach optional Tier-B references into the trip dict when present.
    if last_good_checkpoint is not None:
        info["last_good_checkpoint"] = {
            "path": str(last_good_checkpoint),
            "digest": last_good_digest,
        }
    if config_yaml_path is not None:
        info["config_yaml"] = {"path": str(config_yaml_path)}

    guard = info.get("guard", "unknown")
    step = info.get("step", "?")
    stage = info.get("stage", "?")
    reason = info.get("reason", "")
    readme_line = f"guard={guard} step={step} stage={stage} reason={reason}\n"

    # ---- Tier-A ALWAYS ----
    atomic_write_text(fail_dir / "README.txt", readme_line)
    atomic_write_text(
        fail_dir / "trip.json",
        json.dumps(info, sort_keys=True, indent=2, default=str) + "\n",
    )

    # ---- Tier-B BEST-EFFORT ----
    try:
        if log_lines is not None:
            tail = list(log_lines)[-_TAIL_LOG_LINES:]
            atomic_write_text(
                fail_dir / "tail.log",
                "\n".join(str(line) for line in tail) + ("\n" if tail else ""),
            )
    except OSError:
        pass
    # References already folded into trip.json above; no extra files required
    # for path+digest (kept scalar-only inside trip.json so disk-floor trips
    # stay writable). A separate reference file is intentionally omitted.

    return fail_dir


def _outcome_to_trip_dict(outcome: GuardOutcome) -> dict[str, Any]:
    loss_scalars: Optional[dict[str, Any]] = None
    if outcome.loss_terms is not None:
        loss_scalars = {
            str(k): _json_safe_scalar(v) for k, v in outcome.loss_terms.items()
        }
    disp = outcome.disposition.value if outcome.disposition is not None else None
    payload: dict[str, Any] = {
        "guard": outcome.guard,
        "tier": outcome.tier,
        "step": outcome.step,
        "stage": outcome.stage,
        "phase": outcome.phase,
        "timestamp": time.time(),
        "metric": outcome.metric,
        "value": _json_safe_scalar(outcome.value),
        "threshold": _json_safe_scalar(outcome.threshold),
        "threshold_provisional": bool(outcome.threshold_provisional),
        "disposition": disp,
        "reason": outcome.reason,
        "tripped_guards": list(outcome.tripped_guards),
        "loss_terms": loss_scalars,
        "grad_norm": _json_safe_scalar(outcome.grad_norm),
    }
    # Fold extras (memory provenance, SKIPPED-MPS-UNAVAILABLE, etc.).
    for key, val in (outcome.extras or {}).items():
        if key not in payload:
            payload[key] = _json_safe_scalar(val) if not isinstance(val, (dict, list)) else val
    return payload


__all__ = [
    "GuardOutcome",
    "StepGuards",
    "write_failure_bundle",
]
