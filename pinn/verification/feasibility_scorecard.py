"""Phase 59 (FEAS-01, SCOPE-42): the frozen feasibility scorecard and its pre-registered rules.

The module is read-only. It writes nothing, constructs no optimizer, and
imports only the standard library (hashlib, json, math, dataclasses, pathlib,
types, typing). The scorecard file is never rewritten here, and the loader
keeps no mutable global state: every call reads the bytes once.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

__all__ = [
    "load_scorecard",
    "Scorecard",
    "ScorecardError",
    "OwnerRouted",
    "SCORECARD_SHA256",
    "SCORECARD_SCHEMA_VERSION",
    "SCORECARD_RELATIVE_PATH",
    "tier_of",
    "counts",
    "g2_fires",
    "decision_verdict",
    "steps_budget",
    "still_improving",
    "budget_outcome",
    "scoring_cadence_ok",
    "polish_should_stop",
    "better_state",
    "g1_fires",
    "jx1_reading",
]

SCORECARD_SCHEMA_VERSION = "phase59-feasibility-scorecard/v1"
SCORECARD_RELATIVE_PATH = Path("pinn/verification/artifacts/feasibility_scorecard_v1.json")
_REPO_ROOT = Path(__file__).resolve().parents[2]
SCORECARD_SHA256 = "f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b"

_FAMILY_BIN_COUNT = 16
_FAMILY_BIN_SUM = 1812
_TIER_ORDER = (3, 2, 1)


class ScorecardError(ValueError):
    """The scorecard bytes, schema, or pinned digest are not the frozen contract."""


class OwnerRouted(Exception):
    """A result outside a pre-registered branch.

    Callers must surface it to the owner and never handle it silently.
    """


class _Object:
    """Exact key set of one JSON object. ``None`` children are leaves."""

    def __init__(self, **children: Any) -> None:
        self.children = children


class _ListOf:
    """A JSON array whose elements share one object schema."""

    def __init__(self, item: _Object) -> None:
        self.item = item


_PACKET_ROW = _Object(
    front_idx=None,
    prefix_through_front=None,
    prefix_to_cross_next=None,
    rtilde_bins_0_5=None,
    raw_rbar_bin0=None,
    rtilde_median_all_bins=None,
)

_EXPECTED_KEYS = _Object(
    schema_version=None,
    frozen=None,
    provenance=_Object(
        phase=None,
        requirement=None,
        decisions=None,
        superseded=_Object(
            **{
                "D-02 grid": None,
                "D-04 velocity source": None,
                "D-14 rule details": None,
                "D-18 precedence and tau_L": None,
                "D-22 stand-in": None,
            }
        ),
        owner_routing=None,
        sources=None,
    ),
    frame=_Object(
        name=None,
        position=None,
        time=None,
        velocity=None,
        masses=None,
        D=None,
        T=None,
    ),
    metrics=_Object(
        position_error_forms=None,
        e_sys_normalizer=None,
        e_in_pair=None,
        tier_defining_error=None,
        valid_horizon_deltas=None,
        valid_horizon_rule=None,
        eps_h_formula=None,
        eps_h_hamiltonian=None,
        eps_h_eps_inv=None,
        physics_residual_role=None,
        physics_residual_definition=None,
        physics_residual_statistic=None,
        physics_residual_r_ref_artifact=None,
        physics_residual_acceleration_sources=_Object(
            network=None,
            two_kepler=None,
            nn_copy=None,
        ),
    ),
    velocity_sources=_Object(
        network=None,
        two_kepler=None,
        nn_copy=None,
        context_only=None,
    ),
    scoring_grid=_Object(
        tier_defining=None,
        gold_dt=None,
        base_dt=None,
        t_max=None,
        reported_beside=None,
        samples_per_inner_period=None,
        gold_base_agreement_max=None,
    ),
    tiers=_Object(
        comparison=None,
        levels=_ListOf(_Object(tier=None, E_max=None, eps_h_max=None)),
        otherwise=None,
        non_finite_E_tier=None,
    ),
    counting_rule=_Object(
        min_tier=None,
        formula_comparison=None,
        formula_not_applicable=None,
    ),
    decision_rule=_Object(
        rung2b_min_count=None,
        rung2b_panel_size=None,
        rung3_min_count=None,
        rung3_panel_size=None,
        control_branch_for_go=None,
        control_branches=None,
        rung1_representation_qualifier_min_count=None,
        reported_not_gating=None,
    ),
    gate_g2=_Object(
        trigger_below_tier=None,
        trigger_min_systems=None,
        panel_size=None,
        parameter=None,
        locked_value=None,
        grid=None,
        arm=None,
        first_system=None,
        confirm_system=None,
        rescue_tier=None,
        on_rescue=None,
        on_no_rescue=None,
    ),
    budget_rule=_Object(
        timing_run_min_steps=None,
        seconds_per_step=None,
        cap_hours_single_system=None,
        cap_hours_rung3=None,
        control_adam_steps=None,
        still_improving_statistic=None,
        still_improving_reference_fraction=None,
        still_improving_final_fraction=None,
        still_improving_min_relative_drop=None,
        extensions_max=None,
        extension_factor=None,
        after_extension=None,
        scoring_cadence_max_fraction=None,
    ),
    lbfgs_polish=_Object(
        applies_to=None,
        full_batch=None,
        lbfgs_history_size=None,
        lbfgs_line_search=None,
        lbfgs_max_iter=None,
        physics_arm_freeze=None,
        stop_after_outer_calls_without_improvement=None,
        stop_at_fraction_of_adam_wall_time=None,
        result_rule=None,
        report_both_states=None,
    ),
    accuracy_cadence=_Object(
        every_steps=None,
        include_initial=None,
        include_final=None,
        rung3_panels=None,
        control_panels=None,
    ),
    panel_rule=_Object(
        population=None,
        population_size=None,
        difficulty_measure=None,
        n_in_estimator=None,
        percentile_method=None,
        singles_percentiles=None,
        singles_percentile_population=None,
        singles_min_samples_per_inner_period=None,
        distance=None,
        tie_break=None,
        family_size=None,
        family_sort=None,
        family_split=None,
        family_bin_sizes=None,
        family_pick=None,
        validation_panel=None,
        validation_panel_size=None,
    ),
    census_rules=_Object(
        population_signature=None,
        unwrap_max_step_rad=None,
        inner_normal=None,
        outer_vector=None,
        base_cross_check=None,
        base_cross_check_flag_relative=None,
        phase_accuracy_deltas=None,
        acceleration=None,
        pair_tracking=None,
        gold_base_agreement=None,
        on_check_failure=None,
    ),
    survey_rules=_Object(
        population=None,
        labels_are_diagnostic=None,
        official_mapping=None,
        precedence=None,
        stage0_1_source=None,
        stage1_substages=_Object(**{"1a": None, "1b": None}),
        stage2_source=None,
        stage3=_Object(
            source=None,
            percentile_population=None,
            E_percentile=None,
            E_comparison=None,
            l_ratio_percentile=None,
            l_ratio_comparison=None,
            Q_min=None,
            Q_max=None,
        ),
        stage4=_Object(
            source=None,
            a_tau_L_gt=None,
            b_tau_L_gt=None,
            b_tau_L_le=None,
        ),
        stage5=_Object(source=None, criteria=None),
        stage6=_Object(rule=None, clause_recorded=None),
        tau_not_computable=None,
        tau_L=_Object(
            positions=None,
            time=None,
            resample=None,
            dt=None,
            t_max=None,
            embedding_dim=None,
            delay=None,
            theiler_window=None,
            min_distance=None,
            primary_fit=None,
            sensitivity_fit_windows=None,
            min_fit_points=None,
            non_positive_slope=None,
        ),
        error_growth=None,
        ordering_statistic=None,
        ordering_agreement=None,
        picks=_Object(
            stage4b=None,
            stage6=None,
            nearest=None,
            tie_break=None,
            empty_stage=None,
            sensitivity_report=None,
        ),
    ),
    gate_g1=_Object(
        threshold=None,
        comparison=None,
        checkpoints=None,
        fires_if=None,
        batch=None,
        primary=None,
        preconditioner=None,
        v_hat=None,
        m_hat=None,
        physics_vector=None,
        total_vector=None,
        weights=None,
        secondary=None,
        non_finite_share=None,
        on_fire=None,
        on_no_fire=None,
        checkpoint_files=_Object(**{"0": None, "900": None, "951": None}),
    ),
    diag07=_Object(
        code_commit=None,
        code_snapshot=None,
        overlay_modules=None,
        primary_runtime=None,
        cross_check_runtime=None,
        cross_checked=None,
        microbatch_size=None,
        memory_high_water=None,
        checkpoint_load=None,
        checkpoints=_Object(
            **{
                "stage0-v23g7-seed42": _Object(
                    **{
                        "stage-0-init.pt": None,
                        "best.pt": None,
                        "step-000931.pt": None,
                        "step-000941.pt": None,
                        "step-000951.pt": None,
                        "latest.pt": None,
                        "failure-stage-0-step-951.pt": None,
                    }
                ),
                "stage0-v23g7-smoke": _Object(
                    **{
                        "step-000100.pt": None,
                        "step-000200.pt": None,
                        "step-000300.pt": None,
                    }
                ),
            }
        ),
        tolerances=_Object(
            phase58_packet_front_idx=None,
            phase58_packet_rounded_abs=None,
            phase58_packet_raw_rbar_bin0_rel=None,
            cpu_vs_mps_front_idx=None,
            cpu_vs_mps_rtilde_and_prefix_rel=None,
            cpu_vs_mps_grad_norm_rel=None,
            cpu_vs_mps_share_rel=None,
            cpu_vs_mps_share_abs_floor=None,
            cpu_vs_mps_g1_outcome=None,
            driver_vs_trainer_grad_norm_rel=None,
            monitor_reproduction_targets_times_masses=None,
            monitor_reproduction_ic13_abs=None,
            normalizer_recovery_max_abs=None,
            on_failure=None,
        ),
        jx1=_Object(
            checkpoints=None,
            batch=None,
            terms=None,
            cosine_pairs=None,
            ic_split=None,
            shares_need_moments=None,
            passenger_share_le=None,
            overstated_share_ge=None,
        ),
        jx2=_Object(
            trajectory=None,
            checkpoints=None,
            draws=None,
            draw_seed_base=None,
            draw=None,
            statistic=None,
            statistic_bin=None,
            parameter_motion_if=None,
            otherwise=None,
        ),
        jx3=_Object(
            checkpoints=None,
            high_exposure_count=None,
            never_anchored_count=None,
            never_anchored_seed=None,
            validation_count=None,
            validation_seed=None,
            anchor_steps=None,
            anchor_replay=None,
            times=None,
            statistics=None,
            exposure_specific_if=None,
            global_if=None,
            otherwise=None,
        ),
        jx4=_Object(
            checkpoints=None,
            fixtures=None,
            draw_seed=None,
            physical_scale=None,
            physical_front=None,
            relative_descent_without_accuracy_if=None,
            accuracy_with_descent_if=None,
            otherwise=None,
            informs=None,
        ),
        jx5=_Object(
            checkpoint=None,
            trajectory=None,
            times=None,
            subset=None,
            components=None,
            reading=None,
        ),
        jx10=_Object(
            smoke_checkpoints=None,
            smoke_expected_front=None,
            seed42_reproduction=None,
            phase58_packet=_Object(
                **{
                    "stage-0-init.pt": _PACKET_ROW,
                    "best.pt": _PACKET_ROW,
                    "step-000931.pt": _PACKET_ROW,
                    "step-000941.pt": _PACKET_ROW,
                    "step-000951.pt": _PACKET_ROW,
                }
            ),
            supports_if=None,
            otherwise=None,
        ),
    ),
)


def _dotted(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def _as_real(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number; got {type(value).__name__}")
    return float(value)


def _check_keys(value: Any, spec: Any, path: str) -> None:
    if isinstance(spec, _ListOf):
        if not isinstance(value, list):
            where = path or "scorecard"
            raise ScorecardError(f"{where} must be a JSON array")
        for index, item in enumerate(value):
            _check_keys(item, spec.item, f"{path}[{index}]")
        return
    if not isinstance(spec, _Object):
        raise ScorecardError(f"internal schema error at {path or 'scorecard'}")
    if not isinstance(value, dict):
        where = path or "scorecard"
        raise ScorecardError(f"{where} must be a JSON object")
    expected = set(spec.children)
    actual = set(value)
    unknown = sorted(actual - expected)
    if unknown:
        raise ScorecardError(f"unknown key: {_dotted(path, unknown[0])}")
    missing = sorted(expected - actual)
    if missing:
        raise ScorecardError(f"missing key: {_dotted(path, missing[0])}")
    for key in sorted(spec.children):
        child = spec.children[key]
        if child is None:
            continue
        _check_keys(value[key], child, _dotted(path, key))


def _require_finite_numbers(value: Any, path: str) -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, (int, float)):
        if not math.isfinite(value):
            where = path or "scorecard"
            raise ScorecardError(f"non-finite number at {where}")
        return
    if isinstance(value, dict):
        for key in sorted(value):
            _require_finite_numbers(value[key], _dotted(path, str(key)))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _require_finite_numbers(item, f"{path}[{index}]")
        return
    where = path or "scorecard"
    raise ScorecardError(f"unsupported JSON value at {where}")


def _check_values(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != SCORECARD_SCHEMA_VERSION:
        raise ScorecardError(
            "schema_version must be "
            f"{SCORECARD_SCHEMA_VERSION!r}; got {payload.get('schema_version')!r}"
        )
    if payload.get("frozen") is not True:
        raise ScorecardError("frozen must be literally true")
    _require_finite_numbers(payload, "")
    levels = payload["tiers"]["levels"]
    order = [level.get("tier") if isinstance(level, dict) else None for level in levels]
    if order != list(_TIER_ORDER):
        raise ScorecardError("tiers.levels must be ordered 3, 2, 1")
    bins = payload["panel_rule"]["family_bin_sizes"]
    if not isinstance(bins, list) or len(bins) != _FAMILY_BIN_COUNT:
        raise ScorecardError(
            f"panel_rule.family_bin_sizes must have {_FAMILY_BIN_COUNT} entries"
        )
    if sum(bins) != _FAMILY_BIN_SUM:
        raise ScorecardError(
            f"panel_rule.family_bin_sizes must sum to {_FAMILY_BIN_SUM}"
        )


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _canonical_bytes(payload: Any) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("ascii")


@dataclass(frozen=True)
class Scorecard:
    """One loaded scorecard. ``sections`` is read-only at every level."""

    sha256: str
    sections: MappingProxyType

    def section(self, name: str) -> Mapping[str, Any]:
        try:
            value = self.sections[name]
        except KeyError as exc:
            raise KeyError(name) from exc
        if not isinstance(value, Mapping):
            raise ScorecardError(f"{name} is not an object section")
        return value


def load_scorecard(
    path: Path | None = None,
    *,
    expected_sha256: str = SCORECARD_SHA256,
) -> Scorecard:
    """Read the scorecard once and reject any drift from the frozen contract.

    Checks run in order: one read, JSON parse, canonical bytes, exact keys,
    value constraints, then the SHA-256 of those same bytes. The hash is last
    so a schema error is reported even when the caller passes the copy's own
    digest.
    """
    artifact = _REPO_ROOT / SCORECARD_RELATIVE_PATH if path is None else Path(path)
    try:
        raw = artifact.read_bytes()
    except OSError as exc:
        raise ScorecardError(f"scorecard is unreadable: {artifact}") from exc
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ScorecardError(f"scorecard is not JSON: {artifact}") from exc
    if not isinstance(payload, dict):
        raise ScorecardError("scorecard must be a JSON object")
    try:
        canonical = _canonical_bytes(payload)
    except UnicodeEncodeError as exc:
        raise ScorecardError("scorecard bytes are not canonical ASCII JSON") from exc
    if raw != canonical:
        raise ScorecardError("scorecard bytes are not canonical JSON")
    _check_keys(payload, _EXPECTED_KEYS, "")
    _check_values(payload)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ScorecardError(f"SHA-256 mismatch: got {digest}, expected {expected_sha256}")
    return Scorecard(sha256=digest, sections=_freeze(payload))


def tier_of(E: float, eps_h: float, *, scorecard: Scorecard) -> int:
    """Return the inclusive tier for position error ``E`` and energy error ``eps_h``.

    Levels are walked from 3 to 1. A level whose ``eps_h_max`` is null has no
    energy-error condition. A non-finite ``E`` is tier 0. A non-finite
    ``eps_h`` fails every level that has an energy-error condition.
    """
    if not isinstance(scorecard, Scorecard):
        raise TypeError("scorecard must be a Scorecard")
    tiers = scorecard.section("tiers")
    position_error = _as_real(E, "E")
    energy_error = _as_real(eps_h, "eps_h")
    if not math.isfinite(position_error):
        return int(tiers["non_finite_E_tier"])
    for level in tiers["levels"]:
        if position_error > _as_real(level["E_max"], "E_max"):
            continue
        bound = level["eps_h_max"]
        if bound is None:
            return int(level["tier"])
        if math.isfinite(energy_error) and energy_error <= _as_real(bound, "eps_h_max"):
            return int(level["tier"])
    return int(tiers["otherwise"])


def _require_scorecard(scorecard: Scorecard) -> Scorecard:
    if not isinstance(scorecard, Scorecard):
        raise TypeError("scorecard must be a Scorecard")
    return scorecard


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _require_bools(values: Any, name: str, size: int) -> list[bool]:
    if not isinstance(values, (list, tuple)) or len(values) != size:
        raise ValueError(f"{name} must have length {size}")
    if any(not isinstance(item, bool) for item in values):
        raise ValueError(f"{name} must contain only booleans")
    return list(values)


def _best_windows(
    readings: Any,
    budget_steps: Any,
    scorecard: Scorecard,
) -> tuple[float | None, float | None, int]:
    budget = _require_int(budget_steps, "budget_steps")
    if budget < 0:
        raise ValueError("budget_steps must be non-negative")
    if not isinstance(readings, (list, tuple)):
        raise ValueError("readings must be a sequence of (step, E) pairs")
    cut = float(scorecard.section("budget_rule")["still_improving_reference_fraction"]) * budget
    reference: list[float] = []
    final: list[float] = []
    for item in readings:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError("each reading must be a (step, E) pair")
        step = _require_int(item[0], "step")
        if step < 0 or step > budget:
            raise ValueError(f"step {step} is outside 0..{budget}")
        error = _as_real(item[1], "E")
        if not math.isfinite(error):
            continue
        if step <= cut:
            reference.append(error)
        else:
            final.append(error)
    return (
        min(reference) if reference else None,
        min(final) if final else None,
        budget,
    )


def _state_key(state: Any, name: str) -> tuple[float, float]:
    if not isinstance(state, Mapping) or "E" not in state or "eps_h" not in state:
        raise ValueError(f"{name} must include E and eps_h")
    position = _as_real(state["E"], f"{name}.E")
    energy = _as_real(state["eps_h"], f"{name}.eps_h")
    return (
        position if math.isfinite(position) else math.inf,
        energy if math.isfinite(energy) else math.inf,
    )


def counts(
    tier: int,
    E: float,
    E_formula: float | None,
    *,
    scorecard: Scorecard,
) -> bool:
    """True when the tier counts and ``E`` is strictly below the formula."""
    rule = _require_scorecard(scorecard).section("counting_rule")
    if E_formula is None:
        raise OwnerRouted("two-Kepler formula not applicable on a counted system")
    tier_value = _require_int(tier, "tier")
    position = _as_real(E, "E")
    formula = _as_real(E_formula, "E_formula")
    return (
        tier_value >= int(rule["min_tier"])
        and math.isfinite(position)
        and math.isfinite(formula)
        and position < formula
    )


def g2_fires(rung1_tiers: Any, *, scorecard: Scorecard) -> bool:
    """True when enough Rung-1 tiers sit strictly below the trigger tier."""
    gate = _require_scorecard(scorecard).section("gate_g2")
    panel = int(gate["panel_size"])
    if not isinstance(rung1_tiers, (list, tuple)) or len(rung1_tiers) != panel:
        raise ValueError(f"rung1_tiers must have length {panel}")
    below = int(gate["trigger_below_tier"])
    needed = int(gate["trigger_min_systems"])
    count = sum(1 for tier in rung1_tiers if _require_int(tier, "tier") < below)
    return count >= needed


def decision_verdict(
    *,
    g2_fired: bool,
    sweep_rescued: bool,
    rung2b_counts: Any,
    rung3_counts: Any,
    control_branch: str | None,
    rung1_beats_formula: Any,
    scorecard: Scorecard,
) -> dict[str, Any]:
    """Apply the amended decision rule. Constants come from the scorecard."""
    card = _require_scorecard(scorecard)
    if not isinstance(g2_fired, bool) or not isinstance(sweep_rescued, bool):
        raise ValueError("g2_fired and sweep_rescued must be booleans")
    gate = card.section("gate_g2")
    decision = card.section("decision_rule")
    if g2_fired:
        if sweep_rescued:
            raise OwnerRouted("owner checkpoint 4")
        later = {
            "rung2b_counts": rung2b_counts,
            "rung3_counts": rung3_counts,
            "control_branch": control_branch,
            "rung1_beats_formula": rung1_beats_formula,
        }
        present = [name for name, value in later.items() if value is not None]
        if present:
            raise ValueError(
                "later-rung inputs must be None when G2 fired: " + ", ".join(present)
            )
        return {
            "verdict": gate["on_no_rescue"],
            "representation_limit_qualifier": False,
            "reasons": ["G2 fired and the sweep rescued nothing"],
        }
    rung2b_size = int(decision["rung2b_panel_size"])
    rung3_size = int(decision["rung3_panel_size"])
    rung2b = _require_bools(rung2b_counts, "rung2b_counts", rung2b_size)
    rung3 = _require_bools(rung3_counts, "rung3_counts", rung3_size)
    rung1 = _require_bools(rung1_beats_formula, "rung1_beats_formula", rung2b_size)
    branches = decision["control_branches"]
    if control_branch not in branches:
        raise ValueError(f"unknown control branch: {control_branch!r}")
    reasons: list[str] = []
    rung2b_min = int(decision["rung2b_min_count"])
    rung3_min = int(decision["rung3_min_count"])
    go_branch = decision["control_branch_for_go"]
    if sum(rung2b) < rung2b_min:
        reasons.append(f"Rung 2b counts on fewer than {rung2b_min} of {rung2b_size}")
    if sum(rung3) < rung3_min:
        reasons.append(f"Rung 3 counts on fewer than {rung3_min} of {rung3_size}")
    if control_branch != go_branch:
        reasons.append(f"the control's readout is not branch ({go_branch})")
    qualifier_min = int(decision["rung1_representation_qualifier_min_count"])
    return {
        "verdict": "GO" if not reasons else "PIVOT-TRAINING",
        "representation_limit_qualifier": sum(rung1) < qualifier_min,
        "reasons": reasons,
    }


def steps_budget(
    cap_hours: float,
    timing_wall_seconds: float,
    timing_steps: int,
    *,
    scorecard: Scorecard,
) -> int:
    """Floor of the step budget implied by a timing run and an hour cap."""
    rule = _require_scorecard(scorecard).section("budget_rule")
    steps = _require_int(timing_steps, "timing_steps")
    minimum = int(rule["timing_run_min_steps"])
    if steps < minimum:
        raise ValueError(f"timing_steps must be >= {minimum}")
    wall = _as_real(timing_wall_seconds, "timing_wall_seconds")
    cap = _as_real(cap_hours, "cap_hours")
    if not math.isfinite(wall) or wall <= 0.0:
        raise ValueError("timing_wall_seconds must be finite and positive")
    if not math.isfinite(cap) or cap < 0.0:
        raise ValueError("cap_hours must be finite and non-negative")
    seconds_per_step = wall / steps
    return math.floor(cap * 3600.0 / seconds_per_step)


def still_improving(readings: Any, budget_steps: int, *, scorecard: Scorecard) -> bool:
    """True when the final window improves on the reference window by the frozen drop."""
    card = _require_scorecard(scorecard)
    best_ref, best_final, _budget = _best_windows(readings, budget_steps, card)
    if best_final is None:
        return False
    if best_ref is None:
        return True
    drop = float(card.section("budget_rule")["still_improving_min_relative_drop"])
    return best_final <= (1.0 - drop) * best_ref


def budget_outcome(
    readings: Any,
    budget_steps: int,
    *,
    extended: bool,
    scorecard: Scorecard,
) -> dict[str, Any]:
    """Extend once, otherwise report complete or an inconclusive rate."""
    card = _require_scorecard(scorecard)
    if not isinstance(extended, bool):
        raise ValueError("extended must be a boolean")
    best_ref, best_final, budget = _best_windows(readings, budget_steps, card)
    if not still_improving(readings, budget_steps, scorecard=card):
        return {"outcome": "complete"}
    rule = card.section("budget_rule")
    if not extended:
        scaled = float(rule["extension_factor"]) * budget
        new_budget: int | float = int(scaled) if float(scaled).is_integer() else scaled
        return {"outcome": "extend", "new_budget_steps": new_budget}
    if best_ref is None or best_final is None or best_ref == 0.0:
        raise OwnerRouted(
            "improvement rate is not determinable without a finite reference-window reading"
        )
    final_fraction = float(rule["still_improving_final_fraction"])
    rate = (best_ref - best_final) / (best_ref * final_fraction * budget)
    return {"outcome": "inconclusive", "rate_per_step": rate}


def scoring_cadence_ok(
    reading_steps: Any,
    budget_steps: int,
    *,
    scorecard: Scorecard,
) -> bool:
    """True when readings include both ends and no gap exceeds the frozen fraction."""
    card = _require_scorecard(scorecard)
    budget = _require_int(budget_steps, "budget_steps")
    if budget < 0:
        raise ValueError("budget_steps must be non-negative")
    if not isinstance(reading_steps, (list, tuple)):
        raise ValueError("reading_steps must be a sequence")
    steps: list[int] = []
    for step in reading_steps:
        value = _require_int(step, "step")
        if value < 0 or value > budget:
            raise ValueError(f"step {value} is outside 0..{budget}")
        steps.append(value)
    ordered = sorted(set(steps))
    if not ordered or ordered[0] != 0 or ordered[-1] != budget:
        return False
    limit = float(card.section("budget_rule")["scoring_cadence_max_fraction"]) * budget
    return all(right - left <= limit for left, right in zip(ordered, ordered[1:]))


def polish_should_stop(
    outer_calls_without_improvement: int,
    polish_wall_seconds: float,
    adam_wall_seconds: float,
    *,
    scorecard: Scorecard,
) -> bool:
    """True once the call limit or the Adam-wall fraction is reached."""
    polish = _require_scorecard(scorecard).section("lbfgs_polish")
    calls = _require_int(outer_calls_without_improvement, "outer_calls_without_improvement")
    if calls < 0:
        raise ValueError("outer_calls_without_improvement must be non-negative")
    polish_wall = _as_real(polish_wall_seconds, "polish_wall_seconds")
    adam_wall = _as_real(adam_wall_seconds, "adam_wall_seconds")
    if not math.isfinite(polish_wall) or polish_wall < 0.0:
        raise ValueError("polish_wall_seconds must be finite and non-negative")
    if not math.isfinite(adam_wall) or adam_wall <= 0.0:
        raise ValueError("adam_wall_seconds must be finite and positive")
    call_limit = int(polish["stop_after_outer_calls_without_improvement"])
    fraction = float(polish["stop_at_fraction_of_adam_wall_time"])
    return calls >= call_limit or polish_wall >= fraction * adam_wall


_POLISH_RESULT_RULE = "lexicographic_E_then_eps_h_non_finite_last_tie_keeps_adam"


def better_state(
    adam_state: Mapping[str, Any],
    polish_state: Mapping[str, Any],
    *,
    scorecard: Scorecard,
) -> str:
    """Return ``polish`` only when it is strictly better on (E, eps_h)."""
    rule = _require_scorecard(scorecard).section("lbfgs_polish")["result_rule"]
    if rule != _POLISH_RESULT_RULE:
        raise ScorecardError(f"unsupported polish result rule: {rule}")
    if _state_key(polish_state, "polish_state") < _state_key(adam_state, "adam_state"):
        return "polish"
    return "adam"


def g1_fires(primary_shares: Mapping[Any, Any], *, scorecard: Scorecard) -> dict[str, Any]:
    """Fire when any primary share reaches the frozen threshold at a named checkpoint."""
    gate = _require_scorecard(scorecard).section("gate_g1")
    expected = tuple(gate["checkpoints"])
    if not isinstance(primary_shares, Mapping) or set(primary_shares) != set(expected):
        raise ValueError("primary_shares keys must equal gate_g1.checkpoints")
    values = [
        _as_real(primary_shares[checkpoint], f"share[{checkpoint}]")
        for checkpoint in expected
    ]
    checked = tuple(expected)
    if any(not math.isfinite(share) for share in values):
        return {
            "fires": None,
            "outcome": "not determinable (owner-routed)",
            "checked_checkpoints": checked,
        }
    fires = any(share >= float(gate["threshold"]) for share in values)
    return {
        "fires": fires,
        "outcome": gate["on_fire"] if fires else gate["on_no_fire"],
        "checked_checkpoints": checked,
    }


def jx1_reading(share: float, *, scorecard: Scorecard) -> str:
    """Name the pre-registered JX-1 reading for one physics share."""
    bounds = _require_scorecard(scorecard).section("diag07")["jx1"]
    value = _as_real(share, "share")
    if not math.isfinite(value):
        return "not determinable"
    if value <= float(bounds["passenger_share_le"]):
        return "supports: physics was a passenger (PC-2)"
    if value >= float(bounds["overstated_share_ge"]):
        return "falsifies: PC-2 overstated (Gate G1 fires)"
    return "neither: between 1e-4 and 1e-2"
