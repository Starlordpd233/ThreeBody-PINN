---
status: active
phase: 36-acceptance-checks-re-verification-handoff
milestone: v1.6
total_gaps: 2
open_gaps: 0
resolved_gaps: 2
deferred_gaps: 0
created: 2026-07-01
last_updated: 2026-07-01
---

# Phase 36 Gap Register — Acceptance Checks, Re-verification & Handoff

STOP-protocol gaps detected while planning Phase 36. Both were surfaced by the
Phase 36 researcher as "Findings for Orchestrator" (`36-RESEARCH.md:339-350`, F1/F2)
and confirmed by direct observation before logging. Both shape the **R6 traceability +
status-reconciliation** task (VER-14), so planning of that task is halted until the
owner resolves them. R1–R5 and the 32/32 *mapping* half of R6 are independent and
ready to plan.

---

## GAP-36-01 — Does R6 reconciliation flip PKG-05..08, which have no Phase 32 ledger row?

- **Decision point:** During the R6 status reconciliation, must Phase 36 flip
  `PKG-05`, `PKG-06`, `PKG-07`, `PKG-08` from `Pending` to `Complete` in
  `.planning/REQUIREMENTS.md` — anchored on Phase 30's completion evidence rather than a
  Phase 32 ledger row — or leave them `Pending` / outside the ledger-anchored
  reconciliation scope?
- **Where in artifact:** `.planning/REQUIREMENTS.md:118-121` (PKG-05..08 = `Pending` → Phase 30);
  the R6 reconciliation task to be planned, governed by `36-SPEC.md:53-56` (R6) and
  `36-CONTEXT.md:62` (D-36-17).
- **Task context:** Planning the R6 traceability + status-reconciliation task. The planner
  must name the exact set of `REQUIREMENTS.md` status flags to flip, the terminal anchor for
  each, and mechanically-verifiable `must_haves`/acceptance for the flip — it cannot do this
  for PKG without knowing whether PKG is in R6's flip scope.
- **Classification:** process-artifact-schema.
- **Source silence:**
  - `36-SPEC.md:54` (R6 "Current") enumerates only `LOOP-04/07/08` + the `VER` rows as stale — **silent on PKG**.
  - `36-CONTEXT.md:62` (D-36-17) anchors reconciliation to "ledger-terminal values" and requires "each flipped flag must match a terminal Phase 32 ledger row" — PKG has **no** ledger row.
  - `.planning/REQUIREMENTS.md:118-121` shows PKG-05..08 `Pending`; `.planning/ROADMAP.md` progress table shows Phase 30 **Complete (5/5, 2026-06-18)**. The two records disagree, but no source says whether Phase 36 must reconcile PKG.
  - `.planning/phases/32-.../32-ISSUE-LEDGER.md` has no PKG row (research-package work predates the Phase 32 ledger).
  - `.planning/milestones/v1.6-GAPS.md`, `36-DISCUSSION-LOG.md`: silent (verified).
- **Mathematical / engineering grounding:** Traceability status flags are the milestone's
  closure ground-truth, and R6's acceptance criterion says "no v1.6 status flag contradicts
  terminal state" (`36-SPEC.md:99`). PKG-05..08 are terminal by Phase 30's completion record,
  but the reconciliation **rule** (D-36-17) recognizes only Phase 32 ledger rows as terminal
  anchors. Two defensible readings result: (a) PKG "contradicts terminal state" (Phase 30 done →
  should be `Complete`), so R6 must flip them anchored on Phase 30 evidence; (b) PKG is outside
  the ledger-anchored rule, so leaving it `Pending` is not a contradiction the rule covers.
  Choosing silently either fabricates a completion flag without a ledger anchor (violating the
  D-36-17 rule and SPEC Prohibition 5, `36-SPEC.md:146`) or leaves a satisfied requirement
  permanently `Pending` (arguably violating the no-contradiction criterion). PKG-05..08 are 4 of
  the 32 v1.6 rows the R6 audit ranges over, so the choice is inside R6's scope-of-concern.
- **Agent was tempted to:** flip PKG-05..08 → `Complete` anchored on the Phase 30 ROADMAP
  completion record (5/5, 2026-06-18), treating "terminal evidence" as "ledger row OR
  phase-completion record," because it removes a real Pending-vs-Complete contradiction.
- **What the user needs to decide:**
  - **Option A — In scope, flip on Phase 30 evidence:** flip PKG-05..08 → `Complete`, anchored on the Phase 30 completion record; extend "terminal anchor" to phase-completion records for pre-ledger requirement families, recorded explicitly in R6.
  - **Option B — Out of scope, leave as-is:** R6 reconciliation covers only requirements with a terminal Phase 32 ledger row (plus the VER rows); PKG staleness is noted in the audit but not flipped.
  - **Option C — Flip + amend the rule:** flip PKG-05..08 → `Complete` AND add a one-line D-36-17 amendment legitimizing phase-completion records as terminal anchors for pre-ledger families, so rule and outcome are consistent.
- **Confidence of impact:** MEDIUM — determines whether the R6 "no flag contradicts terminal state" criterion is read as violated at closure, and whether four flags flip.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-01)
- **Resolution note:** Owner selected **Option A** via AskUserQuestion (2026-07-01): flip
  PKG-05, PKG-06, PKG-07, PKG-08 `Pending` → `Complete`, anchored on the Phase 30 completion
  record (ROADMAP progress table, 5/5, 2026-06-18). Per Option A the "terminal anchor" definition
  **extends to phase-completion records for pre-ledger requirement families (PKG)**; the R6
  reconciliation task records this anchor extension explicitly, and each PKG flip cites Phase 30
  completion as its anchor. No PKG flip is made without that citation. This is now the grounding
  for the R6 reconciliation of the PKG rows (see also GAP-36-02 for the combined rule).

---

## GAP-36-02 — R6's "match a terminal ledger row" rule is unsatisfiable for LOOP-07/08

- **Decision point:** The locked R6 rule requires "each flipped flag must match a terminal
  Phase 32 ledger row," but `LOOP-07` and `LOOP-08` have **no** dedicated ledger row while
  SPEC R6's "Current" text names them as stale flags to flip. Should Phase 36 flip
  LOOP-07/08 → `Complete` using `34-VERIFICATION.md` SATISFIED as the terminal anchor in lieu
  of a ledger row, leave them `Pending` to honor the literal rule, or assign a distinct
  provisional terminal status?
- **Where in artifact:** `.planning/REQUIREMENTS.md:138-139` (LOOP-07/08 = `Pending`);
  `36-SPEC.md:54` (names them stale); `36-SPEC.md:56` + `36-CONTEXT.md:62` (D-36-17, ledger-row
  rule); `34-VERIFICATION.md:118-119` (no ledger row).
- **Task context:** Same R6 reconciliation task. The planner must write LOOP-07/08's flip
  disposition and a matching, mechanically-verifiable acceptance/`must_have`. The locked
  stale-list and the locked flip-rule contradict each other for exactly these two rows.
- **Classification:** process-artifact-schema (with a semantic edge — what counts as a "terminal anchor").
- **Source silence / conflict:**
  - `36-SPEC.md:54` names LOOP-07/08 as reading `Pending` "though Phase 34 closed them VERIFIED/SATISFIED" → implies flip.
  - `36-SPEC.md:56` + D-36-17 (`36-CONTEXT.md:62`): "each flipped flag must match a terminal Phase 32 ledger row."
  - `34-VERIFICATION.md:118-119`: LOOP-07/08 "✓ SATISFIED | **no dedicated ledger row (provisional carry-forward)**."
  - No source reconciles the contradiction (flip-list says flip; flip-rule says only-with-ledger-row; these rows have none). Contrast `LOOP-04`, which HAS the M14 ledger row (`34-VERIFICATION.md:115`) and is cleanly flippable.
- **Mathematical / engineering grounding:** The rule encodes a provenance invariant — a flag
  may be flipped to terminal only when backed by an independent terminal record, to prevent
  fabricated completion. Phase 34 deliberately carried LOOP-07/08 as **provisional**
  (forward-referenced to v1.5 VAL-02/03/04), which is *why* they have no ledger row: the ledger
  is for adjudicated findings, and these are carry-forwards awaiting downstream calibration. So
  "SATISFIED (provisional)" is a weaker terminal state than a `VERIFIED` ledger row. Flipping to
  `Complete` on a *provisional* SATISFIED risks over-stating closure; leaving `Pending`
  under-states the Phase-34 verification that did occur. The choice also determines whether the
  R6 idempotency edge (`36-SPEC.md:134`, "each reconciled flag must equal the ledger's terminal
  state for that finding") is even defined for a finding with no ledger row.
- **Agent was tempted to:** flip LOOP-07/08 → `Complete` using `34-VERIFICATION.md` truths 6-7 /
  coverage rows 118-119 as the terminal anchor, treating a phase-VERIFICATION SATISFIED as an
  acceptable substitute for a ledger row, because SPEC R6 explicitly lists them as stale.
- **What the user needs to decide:**
  - **Option A — Flip on VERIFICATION anchor:** flip LOOP-07/08 → `Complete`, anchoring on `34-VERIFICATION.md` SATISFIED/VERIFIED; amend D-36-17 to "terminal ledger row OR terminal phase-VERIFICATION record."
  - **Option B — Leave Pending, honor literal rule:** keep LOOP-07/08 `Pending`; record in R6 that they are intentionally not flipped (provisional carry-forwards without a ledger row), and surface that SPEC R6's stale-list is partially aspirational (SPEC correction).
  - **Option C — Distinct provisional status:** introduce a non-`Complete` terminal status for provisional carry-forwards (e.g., `Satisfied (provisional)`), flip LOOP-07/08 to it, and record the distinction — removes the `Pending` contradiction without over-stating closure.
- **Confidence of impact:** MEDIUM — determines LOOP-07/08 final flags, whether the R6
  idempotency/no-contradiction criteria are satisfiable as locked, and whether the SPEC's
  stale-list or its flip-rule needs a correction.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-01)
- **Resolution note:** Owner selected **Option A** via AskUserQuestion (2026-07-01): flip
  LOOP-07 and LOOP-08 `Pending` → `Complete`, anchored on `34-VERIFICATION.md` SATISFIED/VERIFIED
  (truths 6-7; coverage rows `:118-119`). **D-36-17 is amended** to read "each flipped flag must
  match a terminal Phase 32 ledger row **OR** a terminal phase-VERIFICATION record." Combined with
  GAP-36-01, the resolved R6 reconciliation rule is: **flip each v1.6 status flag to its terminal
  state, where "terminal" = a terminal Phase 32 ledger row OR a terminal phase-VERIFICATION /
  phase-completion record; every flip cites its specific anchor; no flag is flipped without a
  matching terminal record, and none is left `Pending` whose finding is terminal by one of these
  anchors.** The R6 task records this amended rule; LOOP-04 continues to anchor on its M14 ledger
  row.

---

## Non-blocking findings carried to the planner (not OPEN gaps)

- **F3 (already tracked, not re-opened):** `SI-DQA-003` disposition is governed by **D-36-18**
  (`36-CONTEXT.md:63`) — an execution-time, STOP-governed Issue-03-relevance call, not a
  plan-time blocker. The planner's SI-reconciliation task must resolve it against sources and,
  if genuinely source-silent, surface a STOP gap rather than invent. New consideration to carry:
  `SI-PINN-002`'s preserve disposition is analogous to the v1.5 Phase 29 `SI-PINN-002` case,
  which used a **D-08 human-approval checkpoint** — the planner should weigh a
  `checkpoint:human-verify` for the SI-PINN-002 / SI-DQA-003 *preserve* dispositions
  (`36-RESEARCH.md:347`, F3).
- **F4 (mechanical):** (a) `36-CONTEXT.md:115` cites the Phase 29 precedent dir as
  `29-acceptance-checks-reverification-handoff`, but the on-disk path is
  `.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff` — the
  planner must use the correct path. (b) The dirty/untracked set now includes `36-PATTERNS.md`
  and `36-RESEARCH.md` (and this `36-GAPS.md`) in the Phase 36 dir in addition to `AGENTS.md`;
  the D-36-15 dirty-file exclusion guard must account for them (`36-RESEARCH.md:349`, F4).
