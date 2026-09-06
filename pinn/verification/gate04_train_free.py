"""GATE-04 — the fail-closed train-free acceptance gate on the ratified recalibration.

Requirement GATE-04; ROADMAP Phase 56 success criteria 4 and 5. Before Phase
57's RUN-04 may spend the milestone's single preserved Stage-0 run, this gate
measures the audited initialization cases under the amended (SPEC-01/SPEC-06)
recipe and renders exactly one verdict: PASS or BLOCK.

This module is import-only tooling in the ``pinn/verification/`` family: it is
deliberately NOT registered in any CI or verify ladder (no sibling probe is).
Phase 57's RUN-04 imports it and calls :func:`run_gate` as a hard
precondition. The operator CLI, the evidence-directory writer, and the
condition-(ii)/(iii) surfaces land in plan 56-02; this module is the
condition-(i) + finiteness slice, composed end-to-end so every later surface
builds on a proven path.

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

import datetime as dt
import json
import math
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
    _front_idx,
    _git_worktree_dirty,
    _ic13_for_case,
    bin_mean_residuals,
    ratified_causal_weights,
    stratified_collocation_times,
)
from pinn.verify import git_head

VERDICT_PASS = "PASS"
VERDICT_BLOCK = "BLOCK"

R_REF_SCHEMA_VERSION = "phase56-r-ref-stage0/v1"
R_REF_ARTIFACT_PATH = Path(__file__).resolve().parent / "artifacts" / "r_ref_stage0.json"

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
# unratified, and condition (iii)'s controlled-reduction response test is
# inseparable from it (56-RESEARCH.md A.6). Both are carried as
# structurally-present, never-satisfiable slots — a PASS from this plan's
# gate is an INCOMPLETE result (see gate04_verdict's docstring).
_UNRATIFIED_CONDITIONS: tuple[str, str] = ("ii", "iii")

__all__ = [
    "Gate04CaseResult",
    "Gate04Verdict",
    "INVALIDATION_TRIGGERS",
    "R_REF_ARTIFACT_PATH",
    "R_REF_SCHEMA_VERSION",
    "VERDICT_BLOCK",
    "VERDICT_PASS",
    "compute_r_ref",
    "evaluate_case",
    "gate04_verdict",
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
    residual, prefix, or weight entry yields BLOCK; (3) any weight less than
    or equal to ``causal_clip_min_weight`` — the dtype clamp floor read from
    the runtime by the caller, never a copied literal — yields BLOCK
    (strict-inequality reject: a weight exactly at the floor is pinned);
    otherwise PASS.

    Deliberately the ONLY source of the verdict string, in the
    ``gate_metrics.gate_verdict`` convention, so the gate is never rendered as
    two independently-driftable booleans. The verdict vocabulary is exactly
    two values (D-04); no third state exists.

    A PASS from this plan's gate evaluates condition (i) and the finiteness
    pre-checks ONLY: ``Gate04Verdict.unratified_conditions`` is ``("ii",
    "iii")``. A PASS carrying a non-empty ``unratified_conditions`` is an
    INCOMPLETE result — whether RUN-04 may proceed on one is an open owner
    question tracked as GAP-56-01, not a decision this module makes.
    """
    if _blocking_reasons(case_results, causal_clip_min_weight=causal_clip_min_weight):
        return VERDICT_BLOCK
    return VERDICT_PASS


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
    field. The condition-(ii)/(iii) diagnostic slots are present but ``None``;
    plan 56-02 fills them once GAP-56-01 is ratified.
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
        condition_ii_diagnostics=None,
        condition_iii_diagnostics=None,
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
    governed artifact never records an unidentified case.
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
