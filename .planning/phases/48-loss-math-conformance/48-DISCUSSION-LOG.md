# Phase 48: Loss-Math Conformance - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-31
**Phase:** 48-loss-math-conformance
**Areas discussed:** `Rbar` assembly and causal clip, Stage-0 energy-weight correction, per-term gradient observability, assembly-boundary conformance coverage, `L_data` component reduction

---

## `Rbar` Assembly and Causal Clip

### Assembly seam

| Option | Description | Selected |
|--------|-------------|----------|
| Correct the assembly seam | Build `(1/3) sum_i ||f_i||^2` where the `(N_t,3,3)` residual becomes per-time `Rbar`; keep the downstream consumer unchanged | ✓ |
| Scale inside `causal_physics_loss` | Multiply every supplied `Rbar` in the component function, including already-correct callers | |
| Compensate in `lambda_phys` | Hide the factor in the scheduled weight rather than repairing the locked formula | |

**Choice:** Correct the assembly seam (auto-selected recommended option).

**Notes:** The conformance audit isolates C-03 to
`RunController._non_data_terms`; `(weights * Rbar).mean()` is verified clean.
The assembly test must intercept the actual value passed to the consumer so the
same seam cannot escape behind supplied-`Rbar` component tests again.

### Exponent bound

| Option | Description | Selected |
|--------|-------------|----------|
| Dtype-derived smallest-normal bound | Clamp the exponent at `log(torch.finfo(dtype).tiny)`; record the resolved dtype, bound, and minimum weight | ✓ |
| Fixed exponent floor | Use an empirical constant such as `-30` | |
| Fixed weight floor | Clamp `w_n` after exponentiation to an arbitrary positive constant | |

**Choice:** Dtype-derived smallest-normal bound (auto-selected recommended option).

**Notes:** GAP-45-04 delegated the number to the implementer while mandating
invariant A. The selected formula is numerical-range conformance rather than a
front-advance calibration: it prevents exact zero on both precision arms and
does not use retained-run outcomes. Invariant B and its `N` remain Phase 49.

---

## Stage-0 Energy-Weight Correction

| Option | Description | Selected |
|--------|-------------|----------|
| Correct resolved defaults/configs | Set Stage-0 and smoke `lambda_e_max` to zero and retain the generic scheduler | ✓ |
| Hard-code scheduler zero | Remove the later-stage non-zero schedule from the generic scheduler | |
| Shadow downstream zero | Leave the divergent config intact and cancel it after scheduling | |

**Choice:** Correct resolved defaults/configs and retain the scheduler
(auto-selected recommended option).

**Notes:** GAP-45-02/03 already establish that the full PHYS-05 table binds and
the Stage-0 `1.0` override is drift. Phase 49 owns general preflight table
enforcement; Phase 48 repairs the current Stage-0 path and its tests.

---

## Per-Term Gradient Observability

| Option | Description | Selected |
|--------|-------------|----------|
| Raw and applied per-term L2 norms | Log five unweighted global parameter-gradient norms and their lambda-scaled applied norms at the canonical step event | ✓ |
| Applied norms only | Omit the raw signal, losing observability whenever a lambda is zero | |
| Aggregate norm only | Keep the existing total pre-clip norm, which cannot identify term balance | |

**Choice:** Raw and applied per-term L2 norms (auto-selected recommended option).

**Notes:** Raw norms preserve the evidence needed to reason about currently
zero-weighted terms; applied norms show what reached optimization. Diagnostic
gradient computation must not alter `.grad`, clipping, or optimizer behavior.
JSONL remains canonical, with the existing non-finite policy and the existing
L-BFGS last-closure provenance stated explicitly.

---

## Assembly-Boundary Conformance Coverage

| Option | Description | Selected |
|--------|-------------|----------|
| Assembly interception plus same-change corrections | Inspect actual `Rbar`/`eps_H` consumer inputs and correct divergence-defending tests alongside their fixes | ✓ |
| Component tests only | Test functions with caller-supplied correct inputs while leaving assembly unobserved | |
| End-to-end training smoke | Spend a training run to infer a deterministic math/config repair | |

**Choice:** Assembly interception plus same-change corrections (auto-selected
recommended option).

**Notes:** Phase 47 already supplied the `eps_H` assembly-boundary proof and
corrected the former C-04 test. Phase 48 verifies that proof remains and adds
the missing `Rbar` interception, clip, Stage-0 schedule, reduction-provenance,
and gradient-log coverage. Verified-clean component math stays closed.

---

## `L_data` Component Reduction — Blocking Owner Checkpoint

| Option | Description | Selected |
|--------|-------------|----------|
| Mean over all components | Mean Huber over time, bodies, and coordinates; retained-run average `0.1539..0.1630` | ✓ |
| Sum over components | Sum nine component Hubers and average over time; retained-run average `1.3852..1.4673`, exactly 9x | |

**User's choice:** Option A — mean over all components. The owner replied
`proceed` after the orchestrator explicitly recommended Option 1 and requested
ratification.

**Notes:** The retained runs were non-conformant and lacked per-term gradient
statistics, so their magnitudes document impact but do not determine intent.
The recommendation was based on a per-coordinate Huber interpretation: it keeps
`delta_r = 1` coordinate-local, remains invariant to tensor cardinality, and
does not encode a body/component-count multiplier inside fixed
`lambda_data = 1`. The later framework-spec amendment remains VER-20 scope.

---

## Agent's Discretion

The owner invoked `--all --auto` and delegated non-checkpoint gray areas to the
agent. Auto-selected items were:

- the exact helper/module names and phase-scoped test organization;
- the established run-record artifact/schema migration for clip provenance;
- the graph-safe implementation of raw per-term norms and derived applied
  norms; and
- whether TensorBoard mirrors the new canonical JSONL fields.

These remain constrained by `48-CONTEXT.md`; they may not add a dependency,
tuning signal, new cadence, evaluator path, or competing durable record.

## Deferred Ideas

- Invariant B threshold `N`, full PHYS-05 preflight enforcement, placeholder
  census, and known-divergence register — Phase 49.
- Stage-0 re-run and single authorized evaluation — Phases 50-51.
- Explicit `L_data` spec-formula amendment — VER-20 routing to a later spec
  milestone.
- Recipe tuning and automatic dominance reweighting — v2.3.
- Pending todos `d-06-static-epsilon-sensitivity-check` and
  `trainex-r1-research-handoff` — reviewed and not folded because both are
  outside Phase 48 scope.
