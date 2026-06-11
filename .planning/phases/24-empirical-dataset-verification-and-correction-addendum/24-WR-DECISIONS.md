---
phase: 24-empirical-dataset-verification-and-correction-addendum
plan: 04
type: record
created: 2026-06-11
status: RESOLVED-WITH-INSTRUCTION (all four)
blocking_24_03: false
source: 24-04 user gate; verbatim framing per 24-DISCUSSION-LOG.md §"Open Decisions — WR-01..04 Carry-In" (lines 91-125)
---

# WR-01..04 — User Decisions Record (Phase 24, plan 24-04)

> The four OPEN WR-01..04 decisions from the Phase 23 review carry-in have been surfaced to the user via the 24-04 blocking gate and answered verbatim below. The orchestrator (Claude Code, primary loop) records the user's selections; the 24-04 executor was unable to run the gate in subagent context and returned a structured checkpoint, which the orchestrator satisfied here.
>
> All four decisions are `RESOLVED-WITH-INSTRUCTION`. No decision is `OPEN`. Per the user's P1-4 governance decision (2026-06-11), any OPEN WR answer would block 24-03 Task 1 in its entirety; that condition is not met.

## (a) WR-04 — CLM-05 schema (split vs amend)

**Classification:** process-artifact schema (MUST-surface).
**Verbatim framing** (per 24-DISCUSSION-LOG.md:95-100): CLM-05 currently covers two distinct observables (IC folder counts and Brutus output file counts) that happen to coincide today but can diverge. Should the claims register split CLM-05 into CLM-05a (IC folders) / CLM-05b (Brutus output folders), or amend CLM-05's text to name both observables and require separate counts?

**User answer (verbatim, 2026-06-11):**

> "WR-04: Option 1, with a traceability note.
> Split CLM-05 into CLM-05a / CLM-05b. Preserve CLM-05 as the historical parent/alias; do not renumber other CLM IDs. CLM-05a = IC folder counts. CLM-05b = Brutus output folder/file counts. Each should carry its own observed values, probe citation, and verdict."

**Resolution note:** Adopt the split. Plan 24-03 (addendum assembly) and the 24-VERIFIED-FACTS.md register both render CLM-05a (IC folders) and CLM-05b (Brutus output folder/file counts) as separate rows. CLM-05 is preserved as a historical parent/alias in the register's traceability column or footer — no renumbering of other CLM IDs. Each split row carries its own observed values, probe citation, and verdict. The 24-01 probe already reports both observables separately per WR-04 (CLM-05a, CLM-05b), so the schema decision is purely a register-rendering choice — no new probing needed.

**Status:** `RESOLVED-WITH-INSTRUCTION`

---

## (b) WR-01 — Register sample-size as a new CLM row?

**Classification:** process-artifact schema (surface).
**Verbatim framing** (per 24-DISCUSSION-LOG.md:102-107): The issue doc is internally inconsistent on sample size (line 204: 1000 pairs; P2-2 line 292: 100 pairs). The framed question's correction will report both figures neutrally. Should the sample-size figure be registered as a new CLM row to formally track this conflict, or is the neutral report in the framed-questions correction sufficient?

**User answer (verbatim, 2026-06-11):**

> "WR-01: Option 2, with explicit non-CLM surfacing.
> Do not create a new CLM row. The 1000-vs-100 conflict is an issue-doc-internal methodology/sample-size conflict, not a dataset observation figure. Keep CLM for dataset claims. Still surface WR-01 in the DATA-07 non-CLM appendix so researchers see the conflict."

**Resolution note:** Do NOT create a new CLM row for the 1000-vs-100 sample-size conflict — the conflict is a methodology/sample-size disagreement internal to the issue document, not a dataset observation figure, and the CLM register is scoped to dataset claims. The DATA-07 addendum (plan 24-03) carries a non-CLM appendix that surfaces WR-01 with both figures (1000 and 100) reported neutrally and cross-references the framed-questions correction. The 24-ISSUE-LEDGER.md (plan 24-03 Task 2) does NOT add a new row for WR-01 either.

**Status:** `RESOLVED-WITH-INSTRUCTION`

---

## (c) WR-02 / WR-03 — Correction channel for spec-citation fixes

**Classification:** operational coordination (surface).
**Verbatim framing** (per 24-DISCUSSION-LOG.md:109-116, 2026-06-11 update applied): WR-02 and WR-03 are spec-citation typos in `framed-research-questions.md` — not dataset claims, so they do not fit the CLM-keyed DATA-07 addendum cleanly. Within the current Phase 24 plan set, the live channel option is a non-CLM appendix in the DATA-07 addendum; the user may also explicitly defer the channel decision. Direct correction in `RESEARCH-CONTEXT-MASTER.md` is not a live option (would require a separate user-authorized D-18-waiver replan with a concrete master-edit task).

**User answer (verbatim, 2026-06-11):**

> "WR-02/WR-03: Option 1.
> Route the citation typos through a non-CLM appendix in the DATA-07 addendum, keyed by WR ID."

**Resolution note:** The DATA-07 addendum (plan 24-03) carries a non-CLM appendix section that records the two spec-citation typos:
- **WR-02** — `framed-research-questions.md` line 972 → 967 (§10.2 "COM Invariance" lines 967-971)
- **WR-03** — `framed-research-questions.md` §5.3.2 → Step 5 "Mini-Batch Construction" line ~1201 (treated as an example line-cite, not a 32-pt contract)
Each WR entry is keyed by WR ID and cites the source-text line(s). The delivered `RESEARCH-CONTEXT-MASTER.md` stays byte-stable against the post-consolidation baseline `605c0227` (D-18); the appendix is the correction channel, never an in-place doc edit (D-11).

**Status:** `RESOLVED-WITH-INSTRUCTION`

---

## (d) Timing — interim fix NOW vs consolidated addendum

**Classification:** operational coordination (surface).
**Verbatim framing** (per 24-DISCUSSION-LOG.md:118-125, 2026-06-11 update applied): Should the corrected citations (WR-02/03) and conflict surfacing (WR-01) be issued in the consolidated DATA-07 addendum after probes complete, or explicitly deferred until a separate user-authorized D-18-waiver/replan exists? The trade-off is timeliness for in-flight researchers vs preserving the current phase's byte-stability invariant. The "interim erratum extension" vehicle is removed (consolidation retired ERRATUM-2026-06-10.md); "interim fix NOW" as a direct master edit is not executable by the current plan set.

**User answer (verbatim, 2026-06-11):**

> "Timing: Option 1.
> Issue WR-01/02/03 in the consolidated DATA-07 addendum after probes complete. Do not request a D-18 waiver or edit the master in place."

**Resolution note:** WR-01, WR-02, WR-03 are folded into the DATA-07 addendum at the conclusion of plan 24-03 (after 24-01 and 24-02 probes complete). The addendum ships in this Phase 24 milestone; no D-18 waiver is requested; the master is not edited in place. Researchers see the corrections in the same delivery as the data corrections, with provenance traceable to the WR IDs in this file.

**Status:** `RESOLVED-WITH-INSTRUCTION`

---

## Downstream — 24-03 Blocking Status

Per the user's P1-4 governance decision (2026-06-11): "any OPEN WR answer blocks all of 24-03."

- (a) CLM-05 schema: `RESOLVED-WITH-INSTRUCTION`
- (b) WR-01 sample-size: `RESOLVED-WITH-INSTRUCTION`
- (c) WR-02/03 channel: `RESOLVED-WITH-INSTRUCTION`
- (d) Timing: `RESOLVED-WITH-INSTRUCTION`

**24-03 Task 1 (DATA-07 addendum assembly):** `UNBLOCKED`. No OPEN WR answers. Plan 24-03 executor may proceed.

**Separately blocking Phase 24 closure (not WR-related):** `GAP-24-01` (D-16 STOP, semantic, OPEN) — 70/4,857 base-hier files show `m_Brutus(t=0) ≠ m_IC` at `np.allclose(rtol=1e-15)`; gold-hier and both standard variants match. Base-runner / backfill provenance is undocumented. User adjudication required (24-02 gap-surfaced). This blocks Phase 24 closure AND PIPE-07 (Phase 27) consumption regardless of WR status. See `.planning/milestones/v1.5-GAPS.md` and `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-GAPS.md`.

---

## Provenance

- **Recorded by:** Claude Code orchestrator (primary loop), 2026-06-11, after the 24-04 subagent returned a structured checkpoint (it lacked `AskUserQuestion` access).
- **Source for verbatim framing:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DISCUSSION-LOG.md` §"Open Decisions — WR-01..04 Carry-In" (lines 91-125).
- **Source for live-option menu restriction:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-04-PLAN.md` (2026-06-11 revision; see lines 100-102 and 105-107).
- **Audit fix driver:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/review_of_plans/2026-06-11-phase-24-plan-execution-readiness-review.md` (P0-1 + Open Q1).
- **Governance:** v1.5 STOP protocol (CLAUDE.md CRITICAL GOVERNANCE). The agent does not invent WR answers; the user does.
