---
edl_id: EDL-19-01
linked_gap: GAP-19-01
status: OPEN-RESEARCH-NEEDED
phase: 19-physics-and-loss-contracts
topic: epsilon_H energy-drift denominator floor
created: 2026-05-24
blocking_level: dependency-scoped
canonical: false
---

# EDL-19-01: `epsilon_H` Energy-Drift Denominator Floor

## Short Answer Needed

Determine how Phase 19 should handle the numerical default for `epsilon_H` in the energy-drift denominator:

- leave `epsilon_H` symbolic for now;
- bind a numeric default now;
- define a scale-relative or data-dependent rule;
- run an EDL probe before binding it;
- defer binding to Phase 21 or FUT-01 with explicit conditions.

The agent should not choose this on its own.

## Current Project State

Phase 19 is revising physics and loss contracts. The total-loss replacement includes an energy conservation regularizer `L_E`, framed as a soft conservation regularizer rather than an HNN. The Phase 19 context locks the formula shape from the resolution document, but keeps `epsilon_H` symbolic because the source materials name the denominator floor without assigning a numeric value.

The existing phase gap is `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md` `GAP-19-01`. That gap is the canonical blocking record. This EDL brief exists to help the user research the decision externally and return an instruction.

## Why This Is A Gap

The resolution document defines the energy-drift normalization formula:

```text
Delta H_n =
  (H_epsilon(r_theta'(u_n), v_theta'(u_n)) - H_epsilon(r_0', v_0'))
  / (|H_epsilon(r_0', v_0')| + epsilon_H)
```

It also defines `L_E` as a Huber average over `Delta H_n`. It does not assign a numeric value or scaling rule to `epsilon_H`.

The issue document discusses softening values for static invariants and training loss. That is related numerical-stability context, but it does not directly answer the denominator-floor question because `epsilon_H` is not a force/potential softening parameter. It normalizes a scalar conservation-drift term.

The Phase 19 context records this distinction and explicitly says `epsilon_H` is symbolic until `GAP-19-01` is resolved.

## Agent Understanding

`epsilon_H` stabilizes division by the initial matched-Plummer Hamiltonian magnitude when computing relative energy drift. Its value changes how strongly low-`|H_0|` trajectories contribute to `L_E`.

A smaller value keeps the relative normalization stricter, but risks very large drift values when `|H_0|` is close to zero. A larger value floors the denominator more often, which can prevent blowups but changes the effective weighting of low-energy or marginally bound trajectories.

This is distinct from:

- `epsilon_train`, which regularizes matched Plummer force/potential terms during training loss evaluation;
- `epsilon_inv`, which regularizes static invariant calculations;
- `epsilon_L`, which normalizes angular-momentum drift.

The tempting value `1e-8` is familiar as a numerical floor, but familiarity is not grounding under v1.4 governance.

## Candidate Resolutions

### Option A: Leave `epsilon_H` Symbolic

Phase 19 states the formula with symbolic `epsilon_H` and records that binding the default requires later empirical validation or user instruction.

Impact: safest for source-grounding, but it leaves Phase 21 loss-stability probe design incomplete until the symbol is bound or scoped.

### Option B: Bind A Fixed Numeric Default

User instructs a fixed value such as `1e-12`, `1e-10`, `1e-8`, or `1e-6`.

Impact: simplest to document and implement, but can be arbitrary unless research justifies why the value is suitable for dimensionless Hamiltonian magnitudes in this framework.

### Option C: Bind A Scale-Relative Rule

Define `epsilon_H` relative to an energy scale, distribution statistic, machine precision, or representative dataset quantity.

Impact: may be more robust than a fixed floor, but requires clear definition of the scale and when it is computed.

### Option D: Run EDL Before Binding

Design a small probe to compare candidate floors over analytic fixtures, dataset scans, perturbation tests, or surrogate loss behavior.

Impact: provides evidence before locking the contract, but requires extra work before dependent `L_E` numeric defaults and Phase 21 loss-stability checks can close.

### Option E: Defer To Phase 21 Or FUT-01

Keep the Phase 19 contract symbolic and explicitly bind `epsilon_H` when executable loss-stability validation is designed.

Impact: preserves Phase 19 progress if the symbolic contract is acceptable, but the phase or milestone must record the deferral clearly.

## Dependency Map

- **Blocked work:**
  - assigning a numeric default to `epsilon_H`;
  - any Phase 19 `pinn_architecture.md` text that claims a concrete `epsilon_H` value;
  - Phase 21 loss-stability probe design that requires a concrete `epsilon_H`;
  - any downstream implementation plan that needs the numeric denominator floor.

- **Safe independent work:**
  - raw-mass nondimensionalization (`PHYS-01`);
  - componentwise AD contract (`PHYS-02`);
  - matched Plummer force/potential form where it does not bind `epsilon_H`;
  - HNN-to-soft-regularizer prose cleanup;
  - ALM scope restriction and total-loss skeleton, if `epsilon_H` remains symbolic;
  - M4 constraint-counting replacement (`PHYS-06`).

- **Phase-completion impact:**
  - Phase 19 cannot claim a fully concrete `L_E` default while `epsilon_H` remains unresolved.
  - Phase 19 may continue independent edits if they preserve symbolic `epsilon_H`.
  - Phase 19 completion requires either user resolution or an explicit deferral that states what remains symbolic and when it will be bound.

## Core Files To Audit

1. `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md`
   - Why: canonical blocking record for `GAP-19-01`.
   - Check: whether the decision point, source silence, and dependency impact are accurate.

2. `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`
   - Why: locked Phase 19 decision context.
   - Check: D-07 total-loss replacement and the `L_E` row that keeps `epsilon_H` symbolic.

3. `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md`
   - Why: execution plan that edits the `pinn_architecture.md` formula-bearing loss section.
   - Check: whether any task still depends on or implies a numeric `epsilon_H` default.

4. `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
   - Why: candidate source for the `L_E` formula.
   - Check: lines around the `Delta H_n` definition and Huber `L_E` definition; verify that the source names `epsilon_H` but does not bind a value.

5. `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
   - Why: issue-side discussion of softening and numerical stability.
   - Check: whether any epsilon rationale transfers to a scalar energy-drift denominator floor, or whether it applies only to force/potential softening contexts.

## External Research Questions

1. In PINN or Hamiltonian-regularized dynamics losses, how are relative conservation-drift denominators usually floored when the conserved quantity can be close to zero?
2. Should an energy-drift denominator floor be absolute, machine-precision-derived, scale-relative, or dataset-statistic-derived?
3. For dimensionless three-body Hamiltonians after this framework's preprocessing and scaling, what is the expected distribution of `|H_0|`? Are near-zero values common or physically meaningful?
4. If `|H_0|` is near zero, should the energy-drift term behave as a strict relative error, an absolute error, a hybrid relative/absolute error, or a Huber-capped quantity?
5. Does the Huber cap with `delta = 1.0` sufficiently mitigate denominator-collapse risk, or does `epsilon_H` still materially affect gradient scale and sample weighting?
6. Should `epsilon_H` share any logic with `epsilon_L`, or are energy and angular-momentum drift scales sufficiently different that they should remain independent?

## Possible EDL Directions

These are provisional directions only. They are not approved experiment designs.

1. **Dataset scan**
   Compute matched-Plummer `H_0` over representative existing initial conditions, then inspect quantiles of `|H_0|` and how often candidate floors dominate the denominator.

2. **Candidate sweep**
   Compare fixed candidates and scale-relative rules by measuring denominator activation rate, normalized drift quantiles, and ranking stability under synthetic drift magnitudes.

3. **Low-energy stress fixture**
   Construct or identify marginally bound samples where `|H_0|` is small and measure whether the Huber cap alone prevents extreme contribution.

4. **Gradient-scale proxy**
   Use a fake predictor or synthetic perturbations to approximate how candidate floors affect per-sample loss and gradient weighting without building the full PINN.

## Return Format

Return one explicit instruction, preferably in this shape:

```text
For GAP-19-01 / EDL-19-01, choose Option <A/B/C/D/E>.
Instruction: <exact contract or deferral rule>.
Rationale: <short research basis or source>.
Scope: <Phase 19 now / Phase 21 / FUT-01>.
```

If choosing EDL execution now, include whether the probe should be a dataset scan, analytic fixture, perturbation test, surrogate training test, or another shape.
