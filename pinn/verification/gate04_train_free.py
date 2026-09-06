"""GATE-04 — the fail-closed train-free acceptance gate on the ratified recalibration.

Requirement GATE-04; ROADMAP Phase 56 success criteria 4 and 5. Before Phase
57's RUN-04 may spend the milestone's single preserved Stage-0 run, this gate
measures the audited initialization cases under the amended (SPEC-01/SPEC-06)
recipe and renders exactly one verdict: PASS or BLOCK.

This module is import-only tooling in the ``pinn/verification/`` family: it is
deliberately NOT registered in any CI or verify ladder (no sibling probe is).
Phase 57's RUN-04 imports it and calls :func:`run_gate` as a hard
precondition. Running this module as a script (``python -m
pinn.verification.gate04_train_free``) is the operator CLI: it renders the
verdict over the six default cases (or a supplied ``--cases-config`` list)
and writes a provenance-complete evidence record, mirroring the Phase 55
probe's own ``main`` shape.

The causal-weight arithmetic lives in exactly one place in the repository —
``pinn.loss_catalog.causal_physics_loss`` — reached here only through
``architecture_characterization_probe.ratified_causal_weights``. The dtype
clamp floor is read from ``pinn.loss_catalog.resolve_causal_clip_facts`` at
call time, never copied as a literal. A resource failure at the ratified total
batch count is a fail-closed result, not permission to reduce the count
silently (``54-RULING.md``, "Reference invalidation").
"""

from __future__ import annotations

# This must precede Torch and pinn.runtime imports: it is the only reliable
# record of the fallback environment that existed before Torch initialization.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None

import argparse
import datetime as dt
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from pinn.architecture_spec import ArchitectureSpec
from pinn.constants import CAUSAL_ETA_C, T_CHARACTERISTIC_TIME
from pinn.loss_catalog import resolve_causal_clip_facts
from pinn.network import build_network
from pinn.physics_residual import componentwise_du, softened_acceleration
from pinn.runtime import resolve_runtime
from pinn.training.atomic_io import atomic_write_text
from pinn.verification.architecture_characterization_probe import (
    DEFAULT_CASES,
    MEDIAN_CONVENTION,
    RATIFIED_N_BINS,
    RATIFIED_PER_BIN,
    _REPO_ROOT,
    _front_idx,
    _git_worktree_dirty,
    _ic13_for_case,
    _new_run_dir,
    _reject_dataset_evidence_root,
    bin_mean_residuals,
    load_cases_config,
    ratified_causal_weights,
    stratified_collocation_times,
)
from pinn.verify import git_head

VERDICT_PASS = "PASS"
VERDICT_BLOCK = "BLOCK"

R_REF_SCHEMA_VERSION = "phase56-r-ref-stage0/v1"
R_REF_ARTIFACT_PATH = Path(__file__).resolve().parent / "artifacts" / "r_ref_stage0.json"

# The operator CLI's own evidence record (distinct from the governed
# R_ref artifact above): one per invocation, written to a non-overwriting
# timestamped run directory under --evidence-root.
EVIDENCE_SCHEMA_VERSION = "phase56-gate04-cli-evidence/v1"
EVIDENCE_TOP_LEVEL_KEYS = frozenset({
    "schema_version",
    "provenance",
    "configuration",
    "verdict",
    "cases",
    "failure",
})
_GATE04_PROG = "python -m pinn.verification.gate04_train_free"
_DEFAULT_EVIDENCE_ROOT = (
    _REPO_ROOT / ".planning" / "phases" /
    "56-contract-amendment-train-free-gate" / "evidence" / "gate04"
)

# 54-RULING.md "Reference invalidation" — transcribed verbatim, one entry per
# named surface, in the ruling's order (56-CONTEXT.md D-02 enumerates the same
# fifteen surfaces). Any change to one of these surfaces re-measures R_ref and
# re-runs this gate. The ruling's closing policy — a resource failure at the
# ratified total batch count is a fail-closed result, not permission to reduce
# the count silently — is carried in the module docstring, not in this list,
# because it is a run policy rather than a named surface.
INVALIDATION_TRIGGERS: tuple[str, ...] = (
    "first_omega_0",
    "depth",
    "width",
    "power-skip exponent",
    "LayerNorm placement or stabilizer",
    "initialization bounds",
    "D",
    "T",
    "epsilon_soft",
    "IC13 normalization",
    "n_col",
    "M",
    "count unit",
    "selected-slot semantics",
    "bin/allocation semantics",
)

_CONDITIONS = ("i", "ii", "iii")
# GAP-56-01 (OPEN, owner-routed): condition (ii)'s pass criterion is
# unratified — no source in this repository defines a numeric or structural
# test for a weight vector "carrying differential information (not
# all-floor, not degenerate)". Condition (iii) is now wired as the capability
# structure 54-RULING.md specifies (see condition_iii_diagnostics), so only
# condition (ii) remains a structurally-present, never-satisfiable slot — a
# PASS from this plan's gate is still an INCOMPLETE result while it is open
# (see gate04_verdict's docstring).
_UNRATIFIED_CONDITIONS: tuple[str] = ("ii",)

# 56-RESEARCH.md section b.4's sensitivity-sweep ladder, reproduced here so it
# travels with the code: the factor by which condition_iii_diagnostics scales
# the normalized bin residuals (uniformly, or bins late_bin_start.. only) to
# record the front index's response. This is a DIAGNOSTIC INSTRUMENT ONLY —
# GAP-56-01 (OPEN) covers both the reduction magnitude and the response
# margin a healthy recipe must meet; neither is fixed by this ladder.
CONDITION_III_DIAGNOSTIC_FACTORS: tuple[float, ...] = (
    1.0, 0.9, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001,
)

__all__ = [
    "CONDITION_III_DIAGNOSTIC_FACTORS",
    "EVIDENCE_SCHEMA_VERSION",
    "EVIDENCE_TOP_LEVEL_KEYS",
    "Gate04CaseResult",
    "Gate04Verdict",
    "INVALIDATION_TRIGGERS",
    "R_REF_ARTIFACT_PATH",
    "R_REF_SCHEMA_VERSION",
    "VERDICT_BLOCK",
    "VERDICT_PASS",
    "compute_r_ref",
    "condition_ii_diagnostics",
    "condition_ii_verdict",
    "condition_iii_diagnostics",
    "evaluate_case",
    "gate04_verdict",
    "main",
    "run_gate",
    "write_r_ref_artifact",
]


@dataclass(frozen=True)
class Gate04CaseResult:
    """One case's measured evidence under the ratified recipe.

    Structural validation only: the three vector fields must be exactly
    ``RATIFIED_N_BINS`` numeric entries, but their VALUES are evidence, not
    pre-cleared physics — a non-finite or floor-pinned entry must survive
    construction so :func:`gate04_verdict` can see it and BLOCK. Finiteness
    and floor checks live in the verdict function, not here.

    ``condition_ii_diagnostics`` and ``condition_iii_diagnostics`` are
    present-but-``None`` slots in this plan; 56-02 fills them once GAP-56-01
    is ratified. No threshold is invented here.
    """

    label: str
    seed: int
    raw_bin_means: tuple[float, ...]
    r_tilde: tuple[float, ...]
    weights: tuple[float, ...]
    front_idx: int
    min_weight: float
    condition_i_satisfied: bool
    condition_ii_diagnostics: object
    condition_iii_diagnostics: object

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or self.label == "":
            raise ValueError(
                f"Gate04CaseResult.label must be a non-empty str; got {self.label!r}"
            )
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError(
                "Gate04CaseResult.seed must be a non-negative int (not bool); "
                f"got {self.seed!r}"
            )
        for name in ("raw_bin_means", "r_tilde", "weights"):
            original = getattr(self, name)
            try:
                values = tuple(float(item) for item in original)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Gate04CaseResult.{name} must be a {RATIFIED_N_BINS}-entry "
                    f"numeric sequence; got {original!r}"
                ) from exc
            if len(values) != RATIFIED_N_BINS:
                raise ValueError(
                    f"Gate04CaseResult.{name} must hold exactly "
                    f"{RATIFIED_N_BINS} entries; got {len(values)}"
                )
            object.__setattr__(self, name, values)
        if (
            isinstance(self.front_idx, bool)
            or not isinstance(self.front_idx, int)
            or self.front_idx < -1
            or self.front_idx >= RATIFIED_N_BINS
        ):
            raise ValueError(
                f"Gate04CaseResult.front_idx must be an int in "
                f"[-1, {RATIFIED_N_BINS}); got {self.front_idx!r}"
            )
        object.__setattr__(self, "min_weight", float(self.min_weight))
        if not isinstance(self.condition_i_satisfied, bool):
            raise ValueError(
                "Gate04CaseResult.condition_i_satisfied must be a bool; "
                f"got {self.condition_i_satisfied!r}"
            )


@dataclass(frozen=True)
class Gate04Verdict:
    """The single GATE-04 outcome: one verdict, its reasons, and its evidence.

    Fail-closed coherence rules (construction rejects an incoherent object):
    ``verdict`` is exactly ``VERDICT_PASS`` or ``VERDICT_BLOCK`` — no third
    state exists (D-04). A PASS requires at least one evaluated case, an empty
    ``blocking_reasons``, and a finite positive ``r_ref``. A BLOCK requires at
    least one named blocking reason. ``r_ref`` may be NaN on a BLOCK whose
    evaluation never completed (the reference was never computed).
    """

    verdict: str
    blocking_reasons: tuple[str, ...]
    unratified_conditions: tuple[str, ...]
    cases: tuple[Gate04CaseResult, ...]
    r_ref: float
    causal_clip_min_weight: float
    precision: str
    device: str

    def __post_init__(self) -> None:
        if self.verdict not in (VERDICT_PASS, VERDICT_BLOCK):
            raise ValueError(
                f"Gate04Verdict.verdict must be {VERDICT_PASS!r} or "
                f"{VERDICT_BLOCK!r}; got {self.verdict!r}"
            )
        reasons = tuple(str(reason) for reason in self.blocking_reasons)
        object.__setattr__(self, "blocking_reasons", reasons)
        unknown = [c for c in self.unratified_conditions if c not in _CONDITIONS]
        if unknown:
            raise ValueError(
                f"Gate04Verdict.unratified_conditions holds unknown conditions "
                f"{unknown!r}; known conditions are {_CONDITIONS!r}"
            )
        object.__setattr__(
            self, "unratified_conditions", tuple(self.unratified_conditions)
        )
        cases = tuple(self.cases)
        for case in cases:
            if not isinstance(case, Gate04CaseResult):
                raise ValueError(
                    "Gate04Verdict.cases entries must be Gate04CaseResult; "
                    f"got {type(case).__name__}"
                )
        object.__setattr__(self, "cases", cases)
        object.__setattr__(self, "r_ref", float(self.r_ref))
        object.__setattr__(
            self, "causal_clip_min_weight", float(self.causal_clip_min_weight)
        )
        if not math.isfinite(self.causal_clip_min_weight) or self.causal_clip_min_weight <= 0.0:
            raise ValueError(
                "Gate04Verdict.causal_clip_min_weight must be finite and "
                f"positive; got {self.causal_clip_min_weight!r}"
            )
        if self.precision not in ("float32", "float64"):
            raise ValueError(
                f"Gate04Verdict.precision must be 'float32' or 'float64'; "
                f"got {self.precision!r}"
            )
        if self.device not in ("mps", "cpu"):
            raise ValueError(
                f"Gate04Verdict.device must be 'mps' or 'cpu'; got {self.device!r}"
            )
        if self.verdict == VERDICT_PASS:
            if reasons:
                raise ValueError(
                    "a PASS verdict must carry no blocking reasons; "
                    f"got {reasons!r}"
                )
            if not cases:
                raise ValueError(
                    "a PASS verdict requires at least one evaluated case — "
                    "no evidence never reads as satisfied"
                )
            if not math.isfinite(self.r_ref) or self.r_ref <= 0.0:
                raise ValueError(
                    f"a PASS verdict requires a finite positive r_ref; "
                    f"got {self.r_ref!r}"
                )
        elif not reasons:
            raise ValueError("a BLOCK verdict must name at least one blocking reason")


def _blocking_reasons(case_results, *, causal_clip_min_weight: float) -> tuple[str, ...]:
    """Rule-ordered blocking reasons — the audit behind :func:`gate04_verdict`.

    Rules, evaluated in this fixed order so two runs over identical inputs
    produce byte-identical reason sequences:

    1. An empty case sequence blocks: GATE-04 never passes on no evidence.
    2. Per case, in input order: any non-finite entry of the raw bin-mean
       residuals, of the normalized ``r_tilde``, of the exclusive-prefix terms
       accumulated over ``r_tilde``, or of the weight vector blocks. The
       prefix audit recomputes the running sums as plain Python floats — a
       finiteness inspection of the intermediates the trainer's formula
       consumes, never a second implementation of that formula.
    3. Per case, in input order: any finite weight less than or equal to
       ``causal_clip_min_weight`` blocks — a strict-inequality reject: a
       weight exactly at the floor is pinned, and only strictly-greater
       weights satisfy condition (i). Non-finite weights are already named by
       rule 2 and are not double-counted here.
    """
    floor = float(causal_clip_min_weight)
    reasons: list[str] = []
    cases = tuple(case_results)
    if not cases:
        reasons.append("empty case set: GATE-04 never passes on no evidence")
        return tuple(reasons)
    for case in cases:
        for index, value in enumerate(case.raw_bin_means):
            if not math.isfinite(value):
                reasons.append(
                    f"case {case.label!r}: non-finite residual entry "
                    f"raw_bin_means[{index}]={value!r}"
                )
        for index, value in enumerate(case.r_tilde):
            if not math.isfinite(value):
                reasons.append(
                    f"case {case.label!r}: non-finite normalized residual entry "
                    f"r_tilde[{index}]={value!r}"
                )
        prefix = 0.0
        for index, value in enumerate(case.r_tilde):
            # `prefix` here is the exclusive-prefix term entering bin `index`.
            if not math.isfinite(prefix):
                reasons.append(
                    f"case {case.label!r}: non-finite prefix term at bin "
                    f"{index} (and every later bin)"
                )
                break
            prefix += value
        for index, value in enumerate(case.weights):
            if not math.isfinite(value):
                reasons.append(
                    f"case {case.label!r}: non-finite weight entry "
                    f"weights[{index}]={value!r}"
                )
    for case in cases:
        for index, value in enumerate(case.weights):
            if math.isfinite(value) and value <= floor:
                reasons.append(
                    f"case {case.label!r}: causal weight pinned at the dtype "
                    f"clamp floor (weights[{index}]={value!r} <= "
                    f"causal_clip_min_weight={floor!r}); condition (i) "
                    "requires every weight strictly greater than the floor"
                )
    return tuple(reasons)


def gate04_verdict(case_results, *, causal_clip_min_weight: float) -> str:
    """The ONE function that decides GATE-04 PASS versus BLOCK.

    Rules, in order (the full rule text lives in :func:`_blocking_reasons`):
    (1) an empty ``case_results`` sequence yields BLOCK; (2) any non-finite
    residual, prefix, or weight entry yields BLOCK — this is also condition
    (iii)'s only wired rule: a weight vector so degenerate that its front
    index cannot be trusted (a non-finite entry) is already caught here, so
    no separate condition-(iii) check is added; (3) any weight less than or
    equal to ``causal_clip_min_weight`` — the dtype clamp floor read from the
    runtime by the caller, never a copied literal — yields BLOCK
    (strict-inequality reject: a weight exactly at the floor is pinned);
    otherwise PASS.

    Deliberately the ONLY source of the verdict string, in the
    ``gate_metrics.gate_verdict`` convention, so the gate is never rendered as
    two independently-driftable booleans. The verdict vocabulary is exactly
    two values (D-04); no third state exists.

    A PASS from this plan's gate evaluates condition (i), condition (iii)'s
    grounded finiteness rule, and the non-finite pre-checks: condition (iii)'s
    CAPABILITY structure (:func:`condition_iii_diagnostics`) is measured and
    recorded on every case but carries no pass threshold of its own —
    GAP-56-01 makes that threshold inseparable from condition (ii).
    ``Gate04Verdict.unratified_conditions`` is therefore ``("ii",)``. A PASS
    carrying a non-empty ``unratified_conditions`` is an INCOMPLETE result —
    whether RUN-04 may proceed on one is an open owner question tracked as
    GAP-56-01, not a decision this module makes.
    """
    if _blocking_reasons(case_results, causal_clip_min_weight=causal_clip_min_weight):
        return VERDICT_BLOCK
    return VERDICT_PASS


def condition_ii_verdict(weights) -> None:
    """Never returns: condition (ii)'s pass criterion is unratified (GAP-56-01).

    ``54-RULING.md``'s re-issued AC-LOSS-04 requires GATE-04 to fail closed on
    a degenerate weight vector, but neither that ruling nor any other source
    in this repository defines what "degenerate" or "carrying differential
    information" means numerically. That decision is GAP-56-01, status OPEN,
    awaiting the owner.

    This function raises ``NotImplementedError`` UNCONDITIONALLY, for every
    ``weights`` input, so the slot cannot be filled by accident in either
    direction (a false PASS or a false BLOCK). Nothing else in this module
    calls it: :func:`condition_ii_diagnostics` reports descriptive statistics
    with no comparison and no threshold, and :func:`gate04_verdict` never
    references condition (ii) at all.
    """
    raise NotImplementedError(
        "GATE-04 condition (ii)'s pass criterion is unratified (GAP-56-01, "
        "status OPEN): no source in this repository defines a numeric or "
        "structural test for a weight vector 'carrying differential "
        "information (not all-floor, not degenerate)'. See "
        ".planning/phases/56-contract-amendment-train-free-gate/56-GAPS.md "
        "for the four candidate options the owner has not yet ruled on: "
        "(A) a dispersion floor on the non-boundary weights, (B) a "
        "controlled-residual-reduction response test only, (C) both A and "
        "B, or (D) deferring the numeric bound to Phase 57 checkpoint (3) "
        "with condition (ii) logged as a non-blocking diagnostic until "
        "then. This function must not be filled in without an owner ruling."
    )


def condition_ii_diagnostics(weights, causal_clip_min_weight: float) -> dict:
    """Descriptive statistics for condition (ii) — measured, never adjudicated.

    Returns the statistics 56-RESEARCH.md Part (b) computed for the six
    audited cases under the ratified recipe: the coefficient of variation of
    the tail entries ``weights[1:]`` (index 0 is fixed at ``1.0`` by
    construction — the exclusive prefix into bin 0 is empty — so it carries
    no dispersion information of its own), whether the full 16-entry vector
    is monotone non-increasing, the base-10 span
    (``log10(max) - log10(min)``) between the largest and smallest entry, and
    the count of entries strictly above ``causal_clip_min_weight``.

    These are recorded so the owner's eventual GAP-56-01 ruling has real
    post-amendment data to rule against. GATE-04 currently treats condition
    (ii) as measured-but-not-adjudicated rather than as satisfied: this
    function performs NO comparison against any constant and returns NO
    verdict-shaped field (no key named or implying a threshold, a pass, or an
    "ok" state) — :func:`condition_ii_verdict` is the only place a pass/fail
    call for condition (ii) could be made, and it always raises.
    """
    values = np.asarray([float(w) for w in weights], dtype=np.float64)
    if values.size != RATIFIED_N_BINS:
        raise ValueError(
            f"condition_ii_diagnostics requires exactly {RATIFIED_N_BINS} "
            f"weight entries; got {values.size}"
        )
    floor = float(causal_clip_min_weight)
    tail = values[1:]
    tail_mean = float(np.mean(tail))
    cv_tail = float(np.std(tail) / tail_mean) if tail_mean != 0.0 else float("nan")
    monotone_non_increasing = bool(np.all(np.diff(values) <= 0.0))
    dynamic_range_decades = float(np.log10(np.max(values)) - np.log10(np.min(values)))
    distinct_non_floor_count = int(np.sum(values > floor))
    return {
        "coefficient_of_variation_tail": cv_tail,
        "monotone_non_increasing": monotone_non_increasing,
        "dynamic_range_decades": dynamic_range_decades,
        "distinct_non_floor_count": distinct_non_floor_count,
        "status": "UNRATIFIED",
    }


def condition_iii_diagnostics(
    raw_bin_means,
    r_ref,
    *,
    eta_c=CAUSAL_ETA_C,
    dtype,
    device,
    t_max=T_CHARACTERISTIC_TIME,
    factors: "tuple[float, ...]" = CONDITION_III_DIAGNOSTIC_FACTORS,
    late_bin_start: int = 8,
) -> dict:
    """Condition (iii)'s front-CAPABILITY record — never a fixed front check.

    Two structural findings, established by direct computation
    (56-RESEARCH.md Part b.3-b.5) and re-asserted here so they travel with
    the code, not only with the planning artifacts:

    1. All six audited cases produce an unperturbed front index of 0 at
       initialization under the healthy, amended recipe — every case's
       second weight already falls below 0.5 — so a fixed positive-front
       check (the front index compared against zero) would reject every
       healthy case. A front index of 0 here is EXPECTED, not a failure
       signal.
    2. A reduction confined to bins ``late_bin_start`` onward cannot move
       ``front_idx`` at any magnitude, because the weight at bin ``n``
       depends only on the exclusive prefix over bins ``0..n-1``: nothing
       that happens at or after bin ``n`` can change it. A no-response
       result from a late-bin-only perturbation is therefore a structural
       artifact of the formula, not evidence about recipe health.

    For each entry of ``factors`` (default
    :data:`CONDITION_III_DIAGNOSTIC_FACTORS`), this scales the normalized bin
    residuals ``r_tilde = raw_bin_means / r_ref`` uniformly — equivalently,
    scales ``raw_bin_means`` by the same factor since ``r_ref`` is held
    fixed, the two are exactly proportional — and recomputes the weight
    vector through :func:`ratified_causal_weights`, never a second
    implementation, recording the resulting front index via the probe
    module's own front-index helper (the trainer formula: the largest
    0-indexed ``n`` with ``w_n`` strictly greater than 0.5, so ``w_n == 0.5``
    does not advance the front). It separately records the front index under
    a reduction applied ONLY to bins ``late_bin_start`` through the end
    (bins before ``late_bin_start`` are left unperturbed), for the same
    factors.

    Applies NO pass threshold — this is a measurement record only, carrying
    ``status: "UNRATIFIED"``. GAP-56-01 (OPEN) covers both the reduction
    magnitude and the response margin a healthy recipe must meet; neither is
    invented here.
    """
    means = np.asarray([float(v) for v in raw_bin_means], dtype=np.float64)
    if means.size != RATIFIED_N_BINS:
        raise ValueError(
            f"condition_iii_diagnostics requires exactly {RATIFIED_N_BINS} "
            f"raw bin means; got {means.size}"
        )
    if (
        isinstance(late_bin_start, bool)
        or not isinstance(late_bin_start, int)
        or not (0 <= late_bin_start <= RATIFIED_N_BINS)
    ):
        raise ValueError(
            f"late_bin_start must be an int in [0, {RATIFIED_N_BINS}]; "
            f"got {late_bin_start!r}"
        )
    factors_tuple = tuple(float(f) for f in factors)

    def _front_for(scaled_means: np.ndarray) -> int:
        weights = ratified_causal_weights(
            scaled_means, r_ref, eta_c=eta_c, dtype=dtype, device=device, t_max=t_max,
        )
        return _front_idx(weights.tolist())

    unperturbed_front_idx = _front_for(means)
    uniform_response_front_idx = []
    late_bin_only_response_front_idx = []
    for factor in factors_tuple:
        uniform_response_front_idx.append(_front_for(means * factor))
        late_scaled = means.copy()
        late_scaled[late_bin_start:] = late_scaled[late_bin_start:] * factor
        late_bin_only_response_front_idx.append(_front_for(late_scaled))

    return {
        "factors": factors_tuple,
        "late_bin_start": int(late_bin_start),
        "unperturbed_front_idx": unperturbed_front_idx,
        "uniform_response_front_idx": tuple(uniform_response_front_idx),
        "late_bin_only_response_front_idx": tuple(late_bin_only_response_front_idx),
        "status": "UNRATIFIED",
    }


def _measure_raw_bin_means(case, *, dtype, torch_device) -> np.ndarray:
    """One case's sixteen raw bin-mean residuals at initialization.

    The session-verified composition (56-RESEARCH.md "Code Examples"): the
    network built from ``ArchitectureSpec(seed=case.seed)``, the ratified
    4096 stratified times drawn from ``numpy.random.default_rng(case.seed)``
    (256 per each of the 16 fixed equal-``u`` bins), the per-point residual
    ``a' - F_grav`` computed exactly as the probe's ``measure_case`` does
    (``componentwise_du`` + ``softened_acceleration``), reduced by
    ``bin_mean_residuals``. Any non-finite per-point residual or bin mean
    raises ``ValueError`` here — before the weight computation reaches the
    exponent clamp (54-RULING.md Block 3's re-issued acceptance criterion).
    """
    model = build_network(ArchitectureSpec(seed=case.seed), dtype=dtype, device=torch_device)
    model.eval()
    ic13 = _ic13_for_case(case, dtype=dtype, device=torch_device)
    masses_t = torch.as_tensor(case.masses, dtype=dtype, device=torch_device)

    def traj(u_scalar: torch.Tensor) -> torch.Tensor:
        tau = (2.0 * u_scalar - 1.0).reshape(1)
        pos = model(torch.cat([tau, ic13], dim=0).unsqueeze(0), masses_t.unsqueeze(0))
        return pos.reshape(3, 3)

    times_sorted, bin_index = stratified_collocation_times(
        rng=np.random.default_rng(case.seed),
    )
    u_leaf = torch.as_tensor(
        times_sorted / T_CHARACTERISTIC_TIME, dtype=dtype, device=torch_device,
    )
    _first, second = componentwise_du(traj, u_leaf)
    positions = torch.func.vmap(lambda s: traj(s).reshape(-1))(u_leaf)
    positions = positions.reshape(-1, 3, 3)
    f_grav = softened_acceleration(positions, masses_t, dtype=dtype, device=torch_device)
    residual = second.reshape(-1, 3, 3) - f_grav
    # CONF-04 / D-05: one vector-space average per time index — the locked R̄
    # contract averages the three body-vector energies, not nine scalars.
    rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
    rbar_np = np.asarray(rbar.detach().cpu(), dtype=np.float64)
    if not bool(np.all(np.isfinite(rbar_np))):
        bad = int(np.argmin(np.isfinite(rbar_np)))
        raise ValueError(
            f"case {case.label!r}: non-finite per-point residual at "
            f"index {bad}: {rbar_np[bad]!r}"
        )
    means = bin_mean_residuals(rbar_np, bin_index, n_bins=RATIFIED_N_BINS)
    if not bool(np.all(np.isfinite(means))):
        bad = int(np.argmin(np.isfinite(means)))
        raise ValueError(
            f"case {case.label!r}: non-finite bin-mean residual at "
            f"bin {bad}: {means[bad]!r}"
        )
    return means


def compute_r_ref(cases, *, precision: str, device: str) -> tuple[float, tuple[tuple[float, ...], ...]]:
    """The ratified reference scale: the median of all raw bin means.

    Measures every case's sixteen raw bin means, concatenates them (six cases
    x 16 bins = 96 values for the default sweep), and returns
    ``float(numpy.median(...))`` — the even-N convention that averages the two
    central order statistics, recorded in the artifact as
    ``MEDIAN_CONVENTION`` and explicitly NOT torch.median's lower-of-two —
    together with the per-case bin-mean vectors. ``cases`` must be non-empty:
    GATE-04 never computes a reference from nothing. A non-finite or
    non-positive median raises rather than returning a reference the gate
    cannot use.
    """
    case_tuple = tuple(cases)
    if not case_tuple:
        raise ValueError(
            "compute_r_ref requires a non-empty case sequence; got no cases"
        )
    runtime = resolve_runtime(precision, device)
    per_case = tuple(
        _measure_raw_bin_means(
            case, dtype=runtime.dtype, torch_device=runtime.torch_device
        )
        for case in case_tuple
    )
    concatenated = np.concatenate(per_case)
    r_ref = float(np.median(concatenated))
    if not math.isfinite(r_ref) or r_ref <= 0.0:
        raise ValueError(
            f"R_ref must be finite and strictly positive; got {r_ref!r} "
            f"from {concatenated.size} bin means"
        )
    return r_ref, tuple(
        tuple(float(value) for value in means) for means in per_case
    )


def evaluate_case(case, r_ref: float, *, precision: str, device: str) -> Gate04CaseResult:
    """Measure one case under the ratified recipe and assemble its evidence.

    Recomputes the case's raw bin means (the same deterministic construction
    ``compute_r_ref`` uses — same recorded seeds, same values), normalizes by
    ``r_ref``, and evaluates the weight vector through
    ``ratified_causal_weights`` — the trainer's own formula reached via the
    probe helper, never forked here. ``condition_i_satisfied`` records whether
    every weight clears the runtime clamp floor strictly; the verdict function
    re-derives that comparison from the recorded weights and never trusts this
    field. The condition-(ii)/(iii) diagnostic fields are populated from
    :func:`condition_ii_diagnostics` and :func:`condition_iii_diagnostics` —
    measured records only; neither carries a pass/fail verdict, and GAP-56-01
    remains OPEN.
    """
    runtime = resolve_runtime(precision, device)
    clip_facts = resolve_causal_clip_facts(runtime.dtype, runtime.torch_device)
    floor = float(clip_facts["causal_clip_min_weight"])
    try:
        r_ref_value = float(r_ref)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"evaluate_case requires a finite positive r_ref; got {r_ref!r}"
        ) from exc
    if not math.isfinite(r_ref_value) or r_ref_value <= 0.0:
        raise ValueError(
            f"evaluate_case requires a finite positive r_ref; got {r_ref!r}"
        )
    raw = _measure_raw_bin_means(
        case, dtype=runtime.dtype, torch_device=runtime.torch_device
    )
    weights = ratified_causal_weights(
        raw, r_ref_value, dtype=runtime.dtype, device=runtime.torch_device
    )
    weight_tuple = tuple(float(w) for w in weights)
    return Gate04CaseResult(
        label=case.label,
        seed=case.seed,
        raw_bin_means=tuple(float(v) for v in raw),
        r_tilde=tuple(float(v) for v in raw / r_ref_value),
        weights=weight_tuple,
        front_idx=_front_idx(weight_tuple),
        min_weight=min(weight_tuple),
        condition_i_satisfied=all(w > floor for w in weight_tuple),
        condition_ii_diagnostics=condition_ii_diagnostics(weight_tuple, floor),
        condition_iii_diagnostics=condition_iii_diagnostics(
            raw, r_ref_value, dtype=runtime.dtype, device=runtime.torch_device,
        ),
    )


def run_gate(cases=DEFAULT_CASES, *, precision: str = "float64", device: str = "cpu") -> Gate04Verdict:
    """Run GATE-04 over ``cases`` and return the single verdict object.

    Resolves the runtime, reads the dtype clamp floor from
    ``resolve_causal_clip_facts`` AT CALL TIME, computes ``R_ref`` by the
    ratified median-of-96 procedure, evaluates every case, and renders the
    verdict through :func:`gate04_verdict`. There is no parameter, keyword,
    environment variable, or exception path by which a caller obtains a result
    without a verdict, and no default under which an unevaluated condition
    reads as satisfied: any failure during measurement or evaluation returns
    BLOCK with the failure named, and an empty case list returns BLOCK without
    measuring anything. Caller-contract violations — an unknown precision or
    device label — raise from ``resolve_runtime`` before any measurement, the
    same validate-first discipline as ``SweepCase``.
    """
    runtime = resolve_runtime(precision, device)
    clip_facts = resolve_causal_clip_facts(runtime.dtype, runtime.torch_device)
    floor = float(clip_facts["causal_clip_min_weight"])
    case_tuple = tuple(cases)
    if not case_tuple:
        return Gate04Verdict(
            verdict=gate04_verdict((), causal_clip_min_weight=floor),
            blocking_reasons=_blocking_reasons((), causal_clip_min_weight=floor),
            unratified_conditions=_UNRATIFIED_CONDITIONS,
            cases=(),
            r_ref=float("nan"),
            causal_clip_min_weight=floor,
            precision=runtime.precision,
            device=runtime.requested_device,
        )
    try:
        r_ref, _per_case_means = compute_r_ref(
            case_tuple, precision=precision, device=device
        )
        results = tuple(
            evaluate_case(case, r_ref, precision=precision, device=device)
            for case in case_tuple
        )
        reasons = _blocking_reasons(results, causal_clip_min_weight=floor)
        verdict = gate04_verdict(results, causal_clip_min_weight=floor)
    except Exception as exc:  # noqa: BLE001 - a gate that cannot evaluate fails closed
        return Gate04Verdict(
            verdict=VERDICT_BLOCK,
            blocking_reasons=(
                f"GATE-04 evaluation did not complete: "
                f"{type(exc).__name__}: {exc}",
            ),
            unratified_conditions=_UNRATIFIED_CONDITIONS,
            cases=(),
            r_ref=float("nan"),
            causal_clip_min_weight=floor,
            precision=runtime.precision,
            device=runtime.requested_device,
        )
    return Gate04Verdict(
        verdict=verdict,
        blocking_reasons=reasons,
        unratified_conditions=_UNRATIFIED_CONDITIONS,
        cases=results,
        r_ref=r_ref,
        causal_clip_min_weight=floor,
        precision=runtime.precision,
        device=runtime.requested_device,
    )


def write_r_ref_artifact(verdict: Gate04Verdict, path=R_REF_ARTIFACT_PATH) -> Path:
    """Persist the governed ``R_ref`` artifact through the atomic writer.

    The payload carries exactly the frozen top-level key set (the Task-1
    contract, confirmed by the owner 2026-09-06): ``schema_version``,
    ``r_ref``, ``statistic``, ``statistic_convention``, ``cases``,
    ``raw_bin_means``, ``configuration``, ``provenance``,
    ``invalidation_triggers``, ``valid``. Serialized with
    ``json.dumps(..., sort_keys=True, indent=2)`` and written through
    ``pinn.training.atomic_io.atomic_write_text`` (tmp + fsync + replace) —
    never a bare file write.

    Fail-closed integrity: the artifact is a governed, run-gating value
    (D-09), so the writer raises rather than persist an inconsistent one —
    the verdict must carry at least one case, every recorded bin mean must be
    finite, and ``r_ref`` must equal ``numpy.median`` of the recorded means
    exactly (the artifact claims the value IS the median of THESE numbers).
    ``valid`` is true exactly when the verdict is PASS. Case identities are
    enriched from ``DEFAULT_CASES`` (masses, IC13 mode); a case that no
    ``DEFAULT_CASES`` entry matches by ``(label, seed)`` raises — the
    governed artifact never records an unidentified case. Each case entry
    also carries its ``condition_ii_diagnostics`` / ``condition_iii_diagnostics``
    records (56-02 Task 2) — the descriptive statistics and front-response
    series alongside the value, never a verdict for either condition.
    """
    if not isinstance(verdict, Gate04Verdict):
        raise TypeError(
            f"write_r_ref_artifact expects a Gate04Verdict; "
            f"got {type(verdict).__name__}"
        )
    if not verdict.cases:
        raise ValueError(
            "cannot persist an R_ref artifact from a verdict with no cases"
        )
    recorded = [list(case.raw_bin_means) for case in verdict.cases]
    concatenated = np.concatenate(
        [np.asarray(row, dtype=np.float64) for row in recorded]
    )
    if not bool(np.all(np.isfinite(concatenated))):
        raise ValueError(
            "cannot persist an R_ref artifact with a non-finite recorded "
            "bin mean"
        )
    recomputed = float(np.median(concatenated))
    if verdict.r_ref != recomputed:
        raise ValueError(
            f"verdict.r_ref {verdict.r_ref!r} is not numpy.median of the "
            f"recorded bin means {recomputed!r}; refusing to persist an "
            "inconsistent artifact"
        )
    case_entries = []
    for case in verdict.cases:
        matches = [
            candidate
            for candidate in DEFAULT_CASES
            if candidate.label == case.label and candidate.seed == case.seed
        ]
        if len(matches) != 1:
            raise ValueError(
                f"case ({case.label!r}, seed={case.seed}) does not match "
                "exactly one DEFAULT_CASES entry; the governed artifact "
                "never records an unidentified case"
            )
        canonical = matches[0]
        case_entries.append(
            {
                "label": canonical.label,
                "seed": canonical.seed,
                "masses": list(canonical.masses),
                "ic13_mode": canonical.ic13_mode,
                "min_weight": case.min_weight,
                "front_idx": case.front_idx,
                "condition_i_satisfied": case.condition_i_satisfied,
                "condition_ii_diagnostics": case.condition_ii_diagnostics,
                "condition_iii_diagnostics": case.condition_iii_diagnostics,
            }
        )
    git_sha, git_available = git_head()
    dirty, dirty_available = _git_worktree_dirty()
    bin_edges_u = [b / RATIFIED_N_BINS for b in range(RATIFIED_N_BINS + 1)]
    payload = {
        "schema_version": R_REF_SCHEMA_VERSION,
        "r_ref": verdict.r_ref,
        "statistic": "median",
        "statistic_convention": MEDIAN_CONVENTION,
        "cases": case_entries,
        "raw_bin_means": recorded,
        "configuration": {
            "precision": verdict.precision,
            "device": verdict.device,
            "torch_version": torch.__version__,
            "numpy_version": np.__version__,
            "eta_c": float(CAUSAL_ETA_C),
            "t_max": float(T_CHARACTERISTIC_TIME),
            "n_bins": RATIFIED_N_BINS,
            "per_bin": RATIFIED_PER_BIN,
            "total_points": RATIFIED_N_BINS * RATIFIED_PER_BIN,
            "bin_edges_u": bin_edges_u,
            "bin_edge_convention": (
                "[b/16,(b+1)/16) for b=0..14; [15/16,1] closed "
                "(54-RULING.md batch allocation and bin policy)"
            ),
            "case_seeds": {case.label: case.seed for case in verdict.cases},
        },
        "provenance": {
            "git_sha": git_sha,
            "git_available": git_available,
            "git_worktree_dirty": dirty,
            "git_worktree_dirty_available": dirty_available,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        },
        "invalidation_triggers": list(INVALIDATION_TRIGGERS),
        "valid": verdict.verdict == VERDICT_PASS,
    }
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    return atomic_write_text(path, text)


def _command_string(argv) -> str:
    parts = [_GATE04_PROG, *(str(item) for item in argv)]
    return " ".join(parts) if argv else _GATE04_PROG


def _cli_provenance(argv, args) -> dict:
    git_sha, git_available = git_head()
    dirty, dirty_available = _git_worktree_dirty()
    return {
        "argv": [str(item) for item in argv],
        "command": _command_string(argv),
        "git_sha": git_sha,
        "git_available": git_available,
        "git_worktree_dirty": dirty,
        "git_worktree_dirty_available": dirty_available,
        "torch_version": torch.__version__,
        "numpy_version": np.__version__,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def _cli_configuration(args) -> dict:
    return {
        "precision": args.precision,
        "device": args.device,
        "cases_config": None if args.cases_config is None else str(args.cases_config),
        "evidence_root": str(args.evidence_root),
        "r_ref_path": str(args.r_ref_path),
    }


def _case_record(case: Gate04CaseResult) -> dict:
    return {
        "label": case.label,
        "seed": case.seed,
        "raw_bin_means": list(case.raw_bin_means),
        "r_tilde": list(case.r_tilde),
        "weights": list(case.weights),
        "front_idx": case.front_idx,
        "min_weight": case.min_weight,
        "condition_i_satisfied": case.condition_i_satisfied,
        "condition_ii_diagnostics": case.condition_ii_diagnostics,
        "condition_iii_diagnostics": case.condition_iii_diagnostics,
    }


def _verdict_record(verdict: Gate04Verdict) -> dict:
    return {
        "verdict": verdict.verdict,
        "blocking_reasons": list(verdict.blocking_reasons),
        "unratified_conditions": list(verdict.unratified_conditions),
        "r_ref": verdict.r_ref,
        "causal_clip_min_weight": verdict.causal_clip_min_weight,
        "precision": verdict.precision,
        "device": verdict.device,
    }


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=_GATE04_PROG,
        description=(
            "GATE-04: the fail-closed train-free acceptance gate on the "
            "ratified recalibration. Renders exactly one verdict (PASS or "
            "BLOCK) over the six audited cases or a supplied case list, and "
            "writes a provenance-complete evidence record. Does not judge "
            "condition (ii) — GAP-56-01 is OPEN."
        ),
    )
    parser.add_argument(
        "--precision",
        default="float64",
        choices=("float32", "float64"),
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=("mps", "cpu"),
    )
    parser.add_argument("--cases-config", type=Path, default=None)
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=_DEFAULT_EVIDENCE_ROOT,
    )
    parser.add_argument(
        "--r-ref-path",
        type=Path,
        default=R_REF_ARTIFACT_PATH,
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Operator CLI entry point: run GATE-04 and write its evidence record.

    Mirrors the Phase 55 probe's own ``main`` shape and its separation of
    "did the tool run" from "what did it find": the process exit code
    reports whether the tool COMPLETED (0) or did not (1) — an unreadable
    ``--cases-config`` is "did not complete"; a rendered BLOCK verdict is
    "completed, and found BLOCK" (still exit 0). The printed verdict line is
    the only place the verdict itself is surfaced, and it appends the token
    ``INCOMPLETE`` plus the GAP-56-01 reference whenever
    ``unratified_conditions`` is non-empty, so no reader can mistake a PASS
    for a complete GATE-04 clearance.

    The case list resolves through the probe module's own
    ``load_cases_config`` when ``--cases-config`` is supplied, and through
    ``DEFAULT_CASES`` otherwise (D-07) — no second parser, no second case
    list. The evidence root is checked against the probe's
    dataset-evidence-root rejection BEFORE anything else runs, so a hostile
    path is refused before the (potentially minutes-long) measurement is
    even attempted, and before any directory is created.
    """
    args = _parse_args(argv)
    recorded_argv = list(argv) if argv is not None else sys.argv[1:]

    try:
        _reject_dataset_evidence_root(args.evidence_root)
    except Exception as exc:  # noqa: BLE001 - reported to the operator, not raised
        print(f"error: {exc}", file=sys.stderr)
        return 1

    verdict_obj = None
    try:
        cases = (
            load_cases_config(args.cases_config)
            if args.cases_config is not None
            else DEFAULT_CASES
        )
        verdict_obj = run_gate(cases, precision=args.precision, device=args.device)
        raw = {
            "schema_version": EVIDENCE_SCHEMA_VERSION,
            "provenance": _cli_provenance(recorded_argv, args),
            "configuration": _cli_configuration(args),
            "verdict": _verdict_record(verdict_obj),
            "cases": [_case_record(case) for case in verdict_obj.cases],
            "failure": None,
        }
        completed = True
    except Exception as exc:  # noqa: BLE001 - a gate that cannot run records why, not silently
        raw = {
            "schema_version": EVIDENCE_SCHEMA_VERSION,
            "provenance": _cli_provenance(recorded_argv, args),
            "configuration": _cli_configuration(args),
            "verdict": None,
            "cases": [],
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
        completed = False

    try:
        run_dir = _new_run_dir(args.evidence_root)
        atomic_write_text(
            run_dir / "raw.json", json.dumps(raw, sort_keys=True, indent=2) + "\n",
        )
        # Refresh the governed R_ref artifact only for the canonical
        # six-case default run (D-09): a custom --cases-config cannot match
        # DEFAULT_CASES by construction, and write_r_ref_artifact's own
        # fail-closed rule refuses to record an unidentified case.
        if args.cases_config is None and verdict_obj is not None and verdict_obj.cases:
            write_r_ref_artifact(verdict_obj, path=args.r_ref_path)
    except Exception:
        return 1

    if verdict_obj is not None:
        line = f"verdict={verdict_obj.verdict}"
        if verdict_obj.unratified_conditions:
            line += (
                " INCOMPLETE (unratified: "
                + ",".join(verdict_obj.unratified_conditions)
                + "; GAP-56-01 OPEN, see 56-GAPS.md)"
            )
    else:
        line = "verdict=NONE (GATE-04 did not complete)"
    print(line)
    print(f"evidence={run_dir}")
    return 0 if completed else 1


if __name__ == "__main__":
    sys.exit(main())
