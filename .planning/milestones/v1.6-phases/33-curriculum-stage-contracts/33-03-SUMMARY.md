---
phase: 33-curriculum-stage-contracts
plan: 03
subsystem: specwork
tags: [framework-spec, curriculum, ctl_instruction, curr-03, curr-05, stage-transition, state-machine, advance-recover-halt, s_min, epsilon, matched-plummer, packet-first]
requires:
  - .planning/phases/33-curriculum-stage-contracts/33-01-SUMMARY.md
  - .planning/phases/33-curriculum-stage-contracts/33-02-SUMMARY.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/d5-stage-transitions.md
  - .planning/phases/33-curriculum-stage-contracts/33-SPEC.md
  - .planning/phases/33-curriculum-stage-contracts/33-CONTEXT.md
  - .planning/phases/33-curriculum-stage-contracts/33-GAPS.md
  - .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md
  - .planning/milestones/v1.6-GAPS.md
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
provides:
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  - .planning/phases/33-curriculum-stage-contracts/33-03-SUMMARY.md
affects:
  - .planning/STATE.md
  - .planning/ROADMAP.md
  - .planning/REQUIREMENTS.md
tech-stack:
  added: []
  patterns:
    - Section reconciliation: stale pre-decision Author-note blockquote removed and existing advance-only list folded into a named ADVANCE/RECOVER/HALT-REVIEW state machine (xconverge-cycle-1 HIGH coherence finding)
    - Packet-first framework-spec transcription: grounded evidence packet -> Phase 33 contract blockquote with explicit provisional-pending-Stage-0-pilot clauses and rejected-issue-doc-framing markers
    - Negative-token verification: forbidden stale phrasings (`test train stage 0 and see how it goes`, `All of this transition creteria is`, softened Stage-6 gate) asserted absent; `max(s_min, epsilon)` permitted only with explicit rejection marker
    - Cross-phase handoff discipline: Phase 34 (replay/ALM) and Phase 35 (loss-side softening) named as handoffs only, not defined
key-files:
  created:
    - .planning/phases/33-curriculum-stage-contracts/33-03-SUMMARY.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/STATE.md
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md
decisions:
  - CURR-03 ADVANCE/RECOVER/HALT-REVIEW state machine transcribed into Stage Transition Criteria section (D-33-08/09; resolution doc 1.11; evidence/d5-stage-transitions.md)
  - Stale pre-decision Author-note blockquote removed and the four advance criteria folded into the ADVANCE success gate (xconverge HIGH coherence finding; no contradictory advance-only list remains)
  - Issue-doc fallback-advancement framing (MAX_EPOCHS/stagnation/NaN as alternate advancement triggers) rejected; those conditions route to HALT/REVIEW and RECOVER respectively
  - All numeric thresholds, per-stage epsilon_phys table, MAX_EPOCHS table, stagnation window, retry limits, and percentile-10 relaxation marked provisional pending FUT Stage-0 pilot calibration (claimed-unverified D5-05)
  - CURR-05 Stage-6 curriculum collision gate transcribed as unsoftened geometric s_min from true pairwise separations (GAP-32-02 Option A; D-05); raw value logged for diagnostics
  - Loss-side matched-Plummer softening (epsilon_train = 1e-5) routed to Phase 35; Phase 33 does not define loss contracts (D-33-15)
  - Dual-context epsilon transcribed: offline invariants retain epsilon_inv = 1e-10; training retains epsilon_train = 1e-5 (GAP-32-03 Option A; D-06); Option C rejected
  - Issue-doc max(s_min, epsilon) phrasing marked rejected per PHYS-03 (additive + epsilon on distance norm is the PHYS-03 anti-pattern)
  - CURR-03 and CURR-05 marked Complete (contract text defined) in REQUIREMENTS.md; AC-CURR-03/05 verification remains owned by Plan 33-04
metrics:
  duration: ~20 minutes
  completed: 2026-06-23
  tasks_completed: 2
  files_touched: 4
status: complete
---

# Phase 33 Plan 03: Stage-Transition State Machine and s_min Stage-Gate (CURR-03/05) Framework-Spec Transcription Summary

Reconciled the Stage Transition Criteria section into one coherent dual-path
ADVANCE/RECOVER/HALT-REVIEW state machine (removing the stale pre-decision
Author-note blockquote and folding the four advance criteria into the ADVANCE
success gate), and transcribed the Stage-6 curriculum `s_min` gate and
dual-context epsilon contract next to the Stage-6 catch-all inventory. No
source-silent transition threshold, softened stage gate, REVIEW sub-state, or
Phase 34/35 contract was introduced.

## What Was Built

### `ctl_instruction.md` edits (the only framework spec touched)

**Stage Transition Criteria section** (Task 1, was at L1800-1840; cited as
L1666 in the plan / evidence packet — that line number predates Plan 33-02's
earlier insertions):

- Removed the stale pre-decision Author-note blockquote (the musing that ended
  with "Should we first test train stage 0 and see how it goes"). It was a
  pre-decision conversational artifact superseded by the now-grounded
  ADVANCE/RECOVER/HALT-REVIEW contract and could not coexist with it.
- Folded the section's existing advance-only "all four criteria" gate into the
  ADVANCE success gate so there is no longer a separate one-way advance-only
  list contradicting the new machine (xconverge cycle-1 HIGH coherence
  finding).
- Added a Phase 33 contract blockquote (CURR-03; D-33-08/09; AC-CURR-03;
  grounded by resolution doc §1.11 and `evidence/d5-stage-transitions.md`)
  stating the three-state contract: ADVANCE only on the approved success gate;
  RECOVER for NaN/Inf rollback with bounded retry; HALT/REVIEW for max-epoch or
  stagnation, with explicit owner authorization required for any degraded
  advancement.
- Renamed the four criteria headers to "Training-Loss Plateau (ADVANCE
  criterion 1 of 4)", "Validation-Loss Stability (ADVANCE criterion 2 of 4)",
  "Physics-Residual Threshold (ADVANCE criterion 3 of 4, stage-dependent)",
  "Energy-Conservation Check (ADVANCE criterion 4 of 4)" so they are visibly
  part of the ADVANCE gate rather than a standalone advance-only list.
- Added explicit RECOVER and HALT/REVIEW subsections: RECOVER rolls back to the
  last well-formed checkpoint on NaN/Inf and retries with a bounded retry
  budget; exhaustion routes to HALT/REVIEW, never ADVANCE. HALT/REVIEW surfaces
  max-epoch / stagnation failures for owner review; advancing past a failed
  success gate requires an explicit owner decision logged in the gap register.
- Marked the per-stage `epsilon_phys` table, the per-stage `MAX_EPOCHS` table,
  the stagnation window, retry limits, and the percentile-10 relaxation as
  **claimed-unverified (D5-05; CLM-08/09)** and provisional pending FUT
  Stage-0 pilot calibration (SCOPE-14).
- Preserved the locked PHYS-04/D-20 (GAP-19-01) energy denominator floor
  `epsilon_H = 1e-4 * S_H` unchanged.
- Explicitly **rejected** the issue-doc "fallback advancement" framing that
  treats `MAX_EPOCHS`, stagnation, or NaN/Inf as alternate *advancement*
  triggers (it silently relaxes the success criterion).

**Stage-6 curriculum `s_min` gate and dual-context epsilon contract blockquote**
(Task 2, inserted next to the Stage-6 catch-all inventory blockquote at L283):

- Added a Phase 33 contract blockquote (CURR-05; D-33-13/14/15; AC-CURR-05;
  grounded by Phase 32 `GAP-32-02` / `GAP-32-03` owner decisions and the
  `D-05` / `D-06` evidence packets).
- States the Stage-6 curriculum collision gate uses **unsoftened geometric
  s_min** from the true pairwise separations (Step 3 item 1); the gate value
  is the raw geometric minimum separation, logged for diagnostics.
- States the gate does **not** apply any Plummer, additive, or epsilon-floored
  softening; the issue-doc `max(s_min, epsilon)` phrasing is **rejected** per
  PHYS-03 (additive `+ epsilon` on the distance norm is the PHYS-03
  anti-pattern).
- Routes loss-side matched-Plummer softening (`epsilon_train = 1e-5`) to
  **Phase 35**, not the curriculum gate; Phase 33 does not define loss
  contracts.
- States the dual-context epsilon instruction: offline invariants retain
  `epsilon_inv = 1e-10` (consistent with v1.5-locked IPR GAP-28-02 and
  Step 3 item 1); training retains `epsilon_train = 1e-5`. The two contexts
  are distinct and are not conflated.
- Adds cross-phase handoff wording only: Phase 34 owns replay/lookahead
  batching, batch construction, ALM, and training-side metric contracts;
  Phase 35 owns loss-side softened `s_min`, loss scaling, energy weighting,
  Huber delta, and causal training mode. Phase 33 records these handoffs only.
- Implements `GAP-32-02` Option A and `GAP-32-03` Option A (= issue-doc Option
  B); Option C (collapse static `epsilon_inv` to `1e-5`) is rejected.

**Intentionally NOT edited (out of scope for Plan 33-03):**

- The existing Step 3 item 1 `s_min` definition (already computes `s_min`
  geometrically with no softening, and already carries the dual-context
  epsilon text at L1109-1111). Plan 33-03's Task 2 contract blockquote cites
  and consolidates that existing text rather than rewriting it — no
  contradiction was discovered.
- `pinn_architecture.md` — untouched (verified by `git diff --name-only`). No
  STOP-safe cross-link was required because no contradiction was found.
- `sampling_method.md` (frozen), the read-only reports
  (`data_quality_assessment.md`, `review-of-framework.md`,
  `stage-strat-revision.md`), and any live `pinn/` code — untouched.

## Packet-First Constraint Compliance

Both grounded contracts preserve the owner-pending / Phase-boundary
constraints from the resolved Phase 32 / Phase 33 gaps and the v1.6 spec:

- **CURR-03 transition thresholds:** the contract states explicitly that the
  `epsilon_phys` table, the `MAX_EPOCHS` table, the stagnation window, retry
  limits, and the percentile-10 relaxation are claimed-unverified (D5-05) and
  provisional pending the FUT Stage-0 pilot (SCOPE-14) per D-33-09. The
  state-machine *form* is grounded; the calibrated values are FUT.
- **CURR-03 failure routing:** failure and instability cases route through
  RECOVER (NaN/Inf) or HALT/REVIEW (max-epoch, stagnation), never through
  automatic degraded advancement. Degraded advancement requires an explicit
  owner decision.
- **CURR-05 s_min gate:** the contract states the Stage-6 curriculum gate uses
  unsoftened geometric `s_min`; no softened / Plummer / epsilon-floored form
  is authorized. Loss-side matched-Plummer softening is routed to Phase 35.
- **CURR-05 dual-context epsilon:** offline invariants retain
  `epsilon_inv = 1e-10`; training retains `epsilon_train = 1e-5`; the two are
  not conflated (GAP-32-03 Option A; Option C rejected).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Plan cited line L1666 for the Stage Transition Criteria section; actual location is L1800-1840**
- **Found during:** Task 1 `read_first`
- **Issue:** The plan and `evidence/d5-stage-transitions.md` both cite the
  Stage Transition Criteria section at `ctl_instruction.md:1666-1706`. After
  Plan 33-02's earlier insertions (adaptive-stage-assignment and L_max/tau_L
  contract blockquotes earlier in the document), the section had shifted to
  L1800-1840. The plan's `<automated>` verify checks are regex/substring-based
  (not line-number-based), so they remained valid; the line-number citation is
  informational only.
- **Fix:** Located the section by heading (`## Stage Transition Criteria`) and
  the stale Author-note anchor strings (`test train stage 0 and see how it
  goes`, `All of this transition creteria is`) instead of by line number.
  Executed the Task 1 reconciliation against the actual section text.
- **Files modified:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- **Commit:** `856be39`

**2. [Rule 1 - Bug] Plain-phrase substring requirement for `unsoftened geometric s_min`**
- **Found during:** Task 2 verify 1
- **Issue:** The plan's verify 1 check requires the exact literal substring
  `unsoftened geometric s_min` (plain, no formatting). My initial contract
  blockquote wrote it as `**unsoftened geometric \`s_min\`**` with backtick
  fencing around `s_min`, which broke the plain substring match.
- **Fix:** Changed `**unsoftened geometric \`s_min\`**` to
  `**unsoftened geometric s_min** (the raw \`s_min\` from Step 3 item 1)` —
  dropping the inner backticks so the literal substring matches while
  preserving the inline-code reference to Step 3 item 1 one clause later.
  Semantics unchanged.
- **Files modified:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- **Commit:** `f1f243a`

No other deviations. The plan's grounded scope, packet citations, STOP
conditions, and xconverge-cycle-1 mandatory reconciliation actions were
executed exactly as written.

## STOP / Gap Handling

No STOP condition hit and no new gap opened. The plan's two STOP conditions
were checked explicitly:

- **Task 1 STOP condition** (four advance criteria cannot be mapped onto the
  ADVANCE gate without a source-silent semantic choice): NOT triggered. The
  four existing criteria — training-loss plateau, validation-loss stability,
  physics-residual threshold, energy-conservation check — map directly onto
  the ADVANCE success gate as named in `evidence/d5-stage-transitions.md`
  L77-82 and resolution doc §1.11. No semantic choice was required.
- **Task 2 STOP condition** (existing spec already contains a softened/clamped
  Stage-6 `s_min` gate contradicting the unsoftened contract and not covered
  by GAP-32-02/D-05/33-SPEC R5): NOT triggered. The existing Step 3 item 1
  `s_min` definition is already geometric (no softening), and the existing
  dual-context epsilon text at L1109-1111 already aligns with GAP-32-02/03.
  The Stage-6 catch-all inventory blockquote names `s_min < 0.5` as a
  threshold but does not soften it. No contradiction was discovered.

Per the SUBAGENT GAP RULE, no entries were written to `33-GAPS.md` or
`.planning/milestones/v1.6-GAPS.md` by this plan.

## Known Stubs

None. Every contract blockquote carries explicit provisional-pending-Stage-0
language or Phase-34/35-handoff routing rather than a placeholder value. No
hardcoded transition threshold, no softened stage gate, no `max(s_min, epsilon)`
adopted as a curriculum gate, no per-stage `epsilon_phys` / `MAX_EPOCHS` table
locked, no REVIEW sub-state invented, and no Phase 34/35 contract defined.

## Self-Check: PASSED

Created files (FOUND):

- `.planning/phases/33-curriculum-stage-contracts/33-03-SUMMARY.md`

Modified files (FOUND):

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `.planning/STATE.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`

All plan-level `<automated>` verify checks pass:

- Task 1 check 1 (whole-file required tokens: `ADVANCE`, `RECOVER`,
  `HALT/REVIEW`, `NaN`, `Inf`, `provisional`, `Stage-0 pilot`,
  `degraded advancement`): PASS
- Task 1 check 2 (stale Author-note prose absent: `test train stage 0 and see
  how it goes`, `All of this transition creteria is`): PASS
- Task 1 check 3 (section-anchored Stage Transition Criteria regex: ADVANCE /
  RECOVER / HALT/REVIEW / provisional present inside the section, no Author
  note inside the section): PASS
- Task 1 check 4 (out-of-scope guard: `git diff --name-only HEAD --
  pinn_instruction/` equals exactly `{ctl_instruction.md}`): PASS
- Task 2 check 1 (whole-file required tokens: `unsoftened geometric s_min`,
  `Phase 35`, `matched-Plummer`, `epsilon_inv = 1e-10`,
  `epsilon_train = 1e-5`): PASS
- Task 2 check 2 (no softened Stage-6 gate regex; `max(s_min, epsilon)`
  present only with rejection marker): PASS
- Task 2 check 3 (`pinn_architecture.md` has no diff): PASS
- Task 2 check 4 (out-of-scope guard): PASS
- Re-confirmed Task 1 checks 1-3 still PASS after the Task 2 edit (no
  regression): PASS

Commits:

- `856be39` plan(33): reconcile stage transition state machine
- `f1f243a` plan(33): transcribe stage-6 s_min gate and epsilon handoff

Out-of-scope guard (plan-level, against plan start `a9907c69`):
`git diff --name-only a9907c69 HEAD -- pinn_instruction/` returns exactly
`pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`. No
framework spec other than `ctl_instruction.md`, no frozen / read-only report,
no live `pinn/` code, no generated data, no schema file, and no unrelated dirty
docs plan was modified by Plan 33-03. The pre-existing dirty working-tree files
at plan start (the cross-cutting review-resilience plan and the new
`33-REVIEWS*.md` review files) were preserved untouched.
