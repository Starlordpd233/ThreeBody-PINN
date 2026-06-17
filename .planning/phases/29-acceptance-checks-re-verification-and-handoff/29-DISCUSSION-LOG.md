# Phase 29: Acceptance Checks, Re-verification, and Handoff - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-16
**Phase:** 29-acceptance-checks-re-verification-and-handoff
**Areas discussed:** Loose todo match (trainex-r1); Gray-area selection (all four); Gold-completeness reconciliation scope (GAP-29-01); After-ruling proceed mode
**Mode:** `--all --auto` invoked; STOP-protocol governance overrode `--auto` auto-resolution for the one source-silent semantic fork (GAP-29-01), which was surfaced instead of auto-picked.

---

## Loose todo match — `trainex-r1-research-handoff.md`

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Review only | Likely false-positive; record as reviewed, not folded into Phase 29 scope | ✓ |
| 2. Fold it | Include as Phase 29 handoff input | |
| 3. Defer note | Mention as deferred/non-v1.5 handoff note | |

**User's choice:** Option 1 — review only, not folded.
**Notes:** The todo belongs to the *trainex* (training-execution) track; v1.5 is the
*specwork* track. Correctly a false-positive for Phase 29. Recorded in CONTEXT.md
`<deferred>` → Reviewed Todos.

---

## Gray-area selection

| Option | Description | Selected |
|--------|-------------|----------|
| 1. All four | rerun evidence, gold/PSC reconciliation, ledger/SI closure, FUT-01 handoff packaging | ✓ |
| 2. Core three | rerun evidence, gold/PSC reconciliation, ledger/SI closure | |
| 3. Gold/PSC only | gold/PSC only | |

**User's choice:** Option 1 — all four, plus "surface and identify any other questions and grey-areas."
**Notes:** Analysis found three of the four areas already GROUNDED — rerun evidence (SPEC
Req 2 / VER-07/09), ledger/SI closure (SPEC Req 3/4, VER-11/12), and FUT-01 packaging
(grounded by the v1.4 Phase 21 two-artifact precedent: `21-HANDOFF.md` +
`21-CODE-DIVERGENCE.md`). Only gold/PSC reconciliation contained a genuine source-silent
fork (below).

---

## Gold-completeness reconciliation scope — GAP-29-01 (the surfaced fork)

| Option | Description | Selected |
|--------|-------------|----------|
| A. Reconcile planning layer; surface cascade | Phase 29 updates only the records it owns (ledger gold rows, GAP-28-03/GAP-26-01 rationale, STATE.md, 29-UAT table); AC-PIPE-05 reruns PASS 184/184; promotion + framework-spec/AC cascade deferred to a STOP gap. PSC stays DEFERRED. | ✓ |
| B. Full promote + cascade now | Promote 117 (gold 2,565→2,682) + all 6 cascade edits, each LOCKED-ruling edit with a sign-off line. Closes v1.5 fully consistent but mutates dataset + LOCKED specs. | |
| C. Document-only (touch nothing) | Record the reconciliation table only; even planning-layer corrections handed to FUT-01/follow-up. | |

**User's choice:** Option A.
**Notes:** Surfaced rather than auto-picked because `29-SPEC.md` Req 5 leaves promotion
open ("promoted or intentionally left staged") and the 2026-06-14 ruling flags the M13/AC
edits as "a semantic change to a LOCKED ruling — surface, do not silently invent." Key
mechanic: `AC-PIPE-05` is a set-difference probe consistent at 184/184 only while the 117
stay unpromoted; promotion forces a coupled 184→67 cascade across not_in_gold.md,
ctl Step 5, counts, AC-PIPE-05, runner, and the M13 packet. Resolution recorded as
GAP-29-01 RESOLVED-WITH-INSTRUCTION with an embedded DEFERRED promote+cascade sub-item.

---

## After-ruling proceed mode

| Option | Description | Selected |
|--------|-------------|----------|
| A. Write CONTEXT.md, then pause for review | Capture decisions + record the gap, then STOP before plan-phase | ✓ |
| B. Honor --auto/--chain: auto-advance to plan | Write CONTEXT.md, record gap, then launch /gsd-plan-phase 29 --auto | |

**User's choice:** Option A — pause for review (no auto-advance to plan-phase).
**Notes:** Safer for the terminal, milestone-closing phase. The `--auto`/`--chain`
auto-advance is intentionally suppressed.

## Claude's Discretion

- Table-vs-prose formatting and section ordering within the Phase 29 named artifacts —
  follow v1.4 Phase 21 precedent where one exists.

## Deferred Ideas

- **GAP-29-01** — promote the 117 + apply the 184→67 framework-spec/AC/dataset cascade —
  DEFERRED to a separate explicit user ruling; recorded as a FUT-01 forward obligation.
- **PSC/VAL-04 composition** (dedup-prefer-gold + equal-record) — user-deferred
  (GAP-28-03); revisit on explicit reopen.
- **`trainex-r1-research-handoff`** — trainex track, out of v1.5 specwork scope.
