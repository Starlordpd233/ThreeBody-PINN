# Phase 19 Plan Repair Meta-Plan

**Created:** 2026-05-22  
**Purpose:** Provide the edit plan for repairing the Phase 19 execution plans after independent review-audit validation.

## Method

This meta-plan uses a `ce-optimize`-style convergence pass over the review reports in `docs/findings/milestone_v1.4/reviewing_phase19_plans/`: one read-only validation agent reviewed each report independently, then a team-lead pass deduplicated the findings and resolved conflicts. The final planning structure follows `ce-plan`: concrete target files, sequencing, grounding rules, and acceptance checks.

The goal is to edit the Phase 19 plans safely. This document does not execute those edits.

## Source Inputs

- `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-claude-ce-doc-review-phase-19-plans.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-codex-phase-19-plan-review.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-glm-independent-phase-19-plan-review.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-plan-review-convergence.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-ultrathink-phase19-grounding-verification.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/REVIEW.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/ce-doc-review-phase19-synthesis.md`
- `docs/findings/milestone_v1.4/reviewing_phase19_plans/phase19-plans-review.md`

Primary grounding sources for the repair plan:

- `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`
- `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`

## Consensus Verdict

The Phase 19 decision set is largely sound. The repair need is not a physics re-adjudication; it is a plan-quality repair pass for transcription mistakes, unsafe parallel writes, under-specified STOP handling, and weak verification.

Critical corrections:

- `ε_H = 10^-8` is ungrounded. `19-02-PLAN.md` invents a value, while `ctl_pinn_resolution.md` only names `ε_H` symbolically.
- P01/P02 Wave 1 is unsafe as written because both plans mutate the issue ledger and Issue Doc.
- P04 verification can pass on weak token matches instead of proving all six AC-PHYS structural checks passed.
- P03 cannot “log and continue” on cross-reference defects that affect closure.
- Several formula repairs are directly grounded and should not be treated as open gaps: `L_IC` reduction, `L_L` normalization, removal of `G'`, and `L_data` Huber.

## Gap Handling Rules

Before editing the plans, add a repair task that creates or uses `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md` when the first Phase 19 gap is surfaced, then updates `.planning/milestones/v1.4-GAPS.md`.

Surface-only decisions:

- `ε_H` default value: must be logged as a Phase 19 gap before dependent P02 work. Valid options include leaving `ε_H` symbolic, setting `10^-8`, or another explicit user choice. Do not choose silently.
- Causal clipping bound: the clipping requirement is grounded, but a numeric clamp is not. Add non-numeric clipping language; surface only if a concrete bound is needed.
- Zero or near-zero `L_0'`: do not change `L_scale = ||L_0'|| + ε_L`. Surface only if adding prescreening, formula changes, or Phase 21 low-`L_0` probe scope.
- New Phase 21 numeric acceptance criteria, tolerances, or disposable-probe pass thresholds remain out of Phase 19 unless explicitly approved.

Do not surface as gaps:

- `L_IC` reduction: resolution §8.3 gives the formula.
- `L_L` component normalization: resolution §8.6 gives `1/(3N_t)`.
- `η_gauge` and `ε_L` sharing the numeric value `10^-8`: context already separates the symbol families.
- Warmup behavior for `k > 6`: current grounded curriculum stages are `0..6`.

## Implementation Units

### Unit 1: Repair Context And Governance

Target files:

- `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`
- `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md`
- `.planning/milestones/v1.4-GAPS.md`

Required edits:

- Correct any “current spec uses MSE” wording for `L_data`; the current `pinn_architecture.md` data loss is MAE/L1, and the repair is to change it to Huber per `ctl_pinn_resolution.md` §8.2.
- Clarify D-12 Wave 1: P01/P02 may stay parallel only for disjoint spec-file edits. Shared artifacts (`16-ISSUE-LEDGER.md`, evidence lifecycle transitions, and Issue Doc annotations) must be serialized or moved to one coordination task.
- Clarify D-14 Issue Doc annotation mechanics so the edit preserves the existing GFM table row and column count. The plan should say the annotation goes inside the existing row/cell, not as a free-standing line that breaks the table.
- Clarify D-19 to the Phase 17/18 five-column divergence schema: `Surface | Live code (file:line) | Spec target (Phase 19 decision) | FUT-01 item | FUT-01 priority`.
- Add explicit instruction that live `pinn/` references in `19-CODE-DIVERGENCE.md` are FUT-01 handoff coordinates only, not v1.4 grounding.
- Log the `ε_H` gap before any plan text preserves or relies on `ε_H = 10^-8`.

Acceptance checks:

- `19-GAPS.md` exists if the `ε_H` gap remains unresolved during plan repair.
- `v1.4-GAPS.md` indexes any new Phase 19 gap.
- D-12, D-14, and D-19 no longer imply unsafe parallel writes, table-breaking annotations, or a divergent schema.

### Unit 2: Repair P01

Target file:

- `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md`

Required edits:

- Replace the B-02 evidence-packet derivation at the Task 1 instructions with the resolution doc’s direct raw-mass proof. Do not introduce opaque `M_scale` wording.
- Fix the false statement that the issue doc’s `6.694` value corresponds to `M_tot=1`. It corresponds to the mass-fraction alternative `D=(G*M_tot*T^2)^(1/3)` with physical total mass `M_tot=3` in the issue doc example.
- Add non-numeric causal exponent clipping language to the CTL total-loss block. Do not choose a clipping bound.
- Make PHYS-02 and total-loss cross-references section-agnostic where possible: use PHYS IDs and term names rather than brittle future section numbers.
- Tighten `s_min` wording: every `s_min` reference must remain geometric/unsoftened unless it is a non-contractual scale or metadata reference.
- Remove or serialize Issue Doc and ledger writes from P01 if P02 is still parallel. Shared artifact updates should land in a single serialized task.
- Convert any “verify after commit” ordering into “run task verification before commit.”

Acceptance checks:

- B-02 text matches the raw-mass convention in `ctl_pinn_resolution.md` §3.1-3.2.
- No P01 task can race P02 on `16-ISSUE-LEDGER.md` or `pinn_instruction/issues/01-architecture-and-physics-foundations.md`.
- P01 does not invent a causal clipping bound.

### Unit 3: Repair P02

Target file:

- `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md`

Required edits:

- Remove `G'` from Plummer force and Hamiltonian snippets. Raw-mass nondimensionalization absorbs `G`, so the scaled coefficient is 1.
- Add an explicit rewrite of `pinn_architecture.md` §3.1 from L1/MAE to Huber with `δ_r=1`.
- Replace `L_IC` shorthand `MSE(...)` with exact resolution formulas:
  - `L_IC,r = (1/3) Σ_i ||r'_theta,i(0) - r'_i(0)||^2`
  - `L_IC,v = (1/3) Σ_i ||v'_theta,i(0) - v'_i(0)||^2`
- Change `L_L` to the exact resolution normalization: `1/(3N_t) Σ_n Σ_alpha Huber_1.0(...)`.
- State that `v'_theta` used by `L_IC,v` and `L_L` comes from the PHYS-02 componentwise AD contract.
- Remove or surface `ε_H = 10^-8`; do not preserve the numeric value unless the user resolves the gap.
- Add non-numeric causal exponent clipping language.
- Clarify the AD listing as illustrative, not a FUT-01 implementation prescription. If keeping `jacrev + vmap`, make the shapes coherent and state batching uses `vmap`.
- Add optional non-target guidance for broad epsilon sweeps so executors do not rewrite unrelated `10^-8` constants outside softening contexts.
- Remove or serialize Issue Doc and ledger writes if P01 is still parallel.

Acceptance checks:

- `L_data`, `L_IC`, `L_L`, Plummer force, Plummer Hamiltonian, and causal weighting match the resolution doc without ungrounded numeric additions.
- P02 no longer reintroduces a free gravitational coefficient.
- P02 does not treat direct resolution formulas as gaps.

### Unit 4: Repair P03

Target file:

- `.planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md`

Required edits:

- Replace “log any cross-reference gap found and continue” with closure-safe routing:
  - mechanical cross-reference repairs in `pinn_architecture.md` remain in P03 scope;
  - CTL-side mechanical repairs require a targeted P01/P03/P04 repair task before closure;
  - semantic or process-schema defects must be logged in `19-GAPS.md` and block dependent closure.
- Make the D-07 literal total-loss formula the authority, not whichever spec committed first.
- Avoid fixed future section numbers where section names or PHYS IDs are safer.

Acceptance checks:

- P03 cannot pass if either spec contradicts D-07.
- P03 cannot silently defer a cross-reference defect that P04 later treats as verified.

### Unit 5: Repair P04 Verification And Closure

Target file:

- `.planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md`

Required edits:

- Replace token-presence verification with a strict `19-VERIFICATION.md` template containing one row per AC:
  - AC ID
  - command or manual check
  - expected result
  - actual result
  - `PASS` or `FAIL`
- Require all six exact markers before ledger closure:
  - `PASS: AC-PHYS-01`
  - `PASS: AC-PHYS-02`
  - `PASS: AC-PHYS-03`
  - `PASS: AC-PHYS-04`
  - `PASS: AC-PHYS-05`
  - `PASS: AC-PHYS-06`
- Add a hard `FAIL` absence check before any ledger row moves to `VERIFIED`.
- Replace broad positive checks for forbidden text with scoped negative checks, for example:
  - HNN-style architecture claims absent from active prose.
  - pseudo-ALM default terms absent from default-loss sections.
  - stale `epsilon_soft`, `eps_soft`, additive softening, and malformed Plummer/additive mixes absent from active contract text.
- Replace the stale-status ledger regex with a grouped pattern that actually detects any Phase 19 row left at `IN_PROGRESS` or `FIX_APPLIED`.
- Verify source files directly, not only the presence of `PASS` text in `19-VERIFICATION.md`.
- Keep Phase 19 structural. Do not invent Phase 21 numeric thresholds.

Acceptance checks:

- P04 cannot mark any Phase 19 finding `VERIFIED` unless all six structural checks explicitly pass.
- P04 fails if any `FAIL` appears in `19-VERIFICATION.md`.
- P04 fails if any Phase 19 ledger row exits at `IN_PROGRESS` or `FIX_APPLIED`.
- P04 includes no `pinn/` edits.

## Rejected Findings And No-Ops

Do not implement these review suggestions:

- Re-open M4 with convention-dependence language. Phase 19 already locks reconstructive gauge-fixed encoding while crediting the issue doc arithmetic.
- Add `k > 6` warmup behavior. The grounded stage range is `0..6`.
- Add a special `η_gauge` / `ε_L` cross-reference note. The context already separates geometry tolerance from loss stability scale.
- Treat `L_IC` or `L_L` formulas as semantic gaps. The resolution doc answers them.
- Add live-code “not read” attestations. Use “not used as v1.4 grounding; no `pinn/` edits.”
- Apply the claim that the B-09 additive-softening derivation is mathematically wrong as written. At most clarify that the plan compares the current unmatched additive-cubic force with the current additive potential and then locks the Plummer matched pair.
- Add Phase 21 numeric acceptance criteria or disposable-probe tolerances during Phase 19 plan repair.

## Suggested Edit Order

1. Update context/governance first: D-12, D-14, D-19, `L_data` wording, and `19-GAPS.md` handling.
2. Log or resolve `ε_H` before any dependent P02 repair.
3. Repair P01 and P02 in parallel only for disjoint plan text, not shared lifecycle artifacts.
4. Repair P03 after P01/P02 semantics are stable.
5. Repair P04 last so its verification gates reflect the final plan structure.
6. Run a document-level review pass over the repaired plans before execution.

## Verification For The Repair Pass

After applying this meta-plan to the Phase 19 plans, verify:

- `rg -n "ε_H = 10|epsilon_H.*10|epsilon_H = 10|ε_H.*10" .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md` returns no unapproved numeric default.
- `rg -n "G'|dimensionless gravitational constant" .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md` returns no free coefficient in the final Plummer snippets.
- `rg -n "1/\\(3N|3N_t|3\\s*·\\s*N" .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md` confirms `L_L` component normalization.
- `rg -n "Huber.*δ_r|Huber.*delta_r|L_data.*Huber" .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md` confirms the §3.1 `L_data` rewrite is explicit.
- `rg -n "PASS: AC-PHYS-01|PASS: AC-PHYS-02|PASS: AC-PHYS-03|PASS: AC-PHYS-04|PASS: AC-PHYS-05|PASS: AC-PHYS-06" .planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md` confirms strict PASS markers are required.
- `rg -n "log any cross-reference gap found and continue|log.*continue" .planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md` returns no closure-unsafe wording.

## Completion Criteria

The Phase 19 plans are ready for execution only when:

- all direct grounded repairs above are represented in the relevant plan files;
- every open semantic/process gap has a `19-GAPS.md` entry and milestone index entry;
- no unresolved gap-dependent task is marked autonomous or executable;
- P01/P02 shared-file writes are serialized;
- P04 verification cannot pass from token presence alone;
- invalid review suggestions are explicitly ignored rather than silently incorporated.
