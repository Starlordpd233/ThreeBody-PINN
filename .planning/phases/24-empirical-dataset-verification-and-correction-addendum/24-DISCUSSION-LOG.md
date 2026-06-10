# Phase 24: Empirical Dataset Verification and Correction Addendum - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-10
**Phase:** 24-empirical-dataset-verification-and-correction-addendum
**Areas discussed:** Probe implementation & evidence capture; Verification checklist scope; Verdict semantics & documentation contradictions; Mass-drift probe design (DATA-05); DATA-07 addendum form & delivery; Issue-ledger seeding
**Mode:** `--all --auto` — user instructed Claude to select the best option per area using best judgment; no interactive ratification. Selections grounded in REQUIREMENTS.md / ROADMAP.md / committed Phase 23 artifacts wherever possible.

---

## Probe implementation & evidence capture

| Option | Description | Selected |
|--------|-------------|----------|
| Disposable committed probe scripts + captured outputs under phase dir | Read-only scripts, command+path recorded per fact; self-contained evidence | ✓ |
| Ad-hoc commands recorded only in prose | Lighter, but weakens re-derivability and review | |
| Extend existing `simulation_data/Validation/` audit scripts | Reuses code but mutates grounding-source tree and couples to the audit workstream | |

**Choice rationale:** SCOPE-06 requires probe outputs "recorded with method and command so claims are re-derivable"; VER-09 mandates disposable probes; FUT-03 explicitly defers reusable packaging. Citing the 2026-06-10 doc-integrity audit instead of re-probing was rejected so the ledger evidence is self-contained (`[auto]` selected, recommended default).

## Verification checklist scope

| Option | Description | Selected |
|--------|-------------|----------|
| CLM-01..12 + bounded prose sweep of package docs (CLM-14+ extension IDs); CLM-13 excluded | Matches DATA-07's "every package-stated dataset claim"; erratum proved prose claims escape the register | ✓ |
| Claims-table rows only | Simpler but provably incomplete (gold-infix claim had no CLM row) | |
| Full re-audit of all package text incl. specs snapshots | Over-scope; framework-spec snapshots are intact copies, not dataset claims | |

**Choice rationale:** DATA-07's language is broader than the 13 registered rows; the ERRATUM-2026-06-10 precedent shows narrative claims exist outside the table. CLM-13 exclusion is the claims table's own routing (row note → Phase 25/27). (`[auto]` selected.)

## Verdict semantics & documentation contradictions

| Option | Description | Selected |
|--------|-------------|----------|
| {confirmed/corrected/unverified}; "~" claims judged at claimed precision against recorded distributions; README contradictions surfaced for user sign-off | Vocabulary transcribed from roadmap success criterion 1; sign-off mirrors audit precedent commits | ✓ |
| Binary pass/fail per claim | Loses the "cannot probe within grounding" case (e.g., M11 consumption in `pinn/`) | |
| Auto-correct README on contradiction | Violates the user-sign-off precedent for dataset-doc edits | |

**Choice rationale:** Vocabulary is grounded (not invented); DATA-06 mandates distributions; empirical observation outranks doc text (SCOPE-06) but documentation edits stay user-gated (precedent `d18f676`/`31b2cff`/`ae609f3`). (`[auto]` selected.)

## Mass-drift probe design (DATA-05)

| Option | Description | Selected |
|--------|-------------|----------|
| Full-population t=0 sweep; seeded stratified fallback if runtime prohibits; hierarchical-perturbation baseline contingency flagged as potential STOP gap | First-block parsing is cheap; full coverage kills sampling-bias debate; method already fixed by DATA-05 | ✓ |
| Fixed small sample (e.g., 50/variant) | Satisfies "documented sample" minimally but invites coverage questions feeding PIPE-07 | |
| Standard-variant-only sweep | Misses the hierarchical perturbation wrinkle entirely | |

**Choice rationale:** Only the sample was open (method/tolerance fixed by DATA-05 text). The hierarchical-IC-perturbation contingency is written into CONTEXT as a STOP-gap trigger, not silently resolved. (`[auto]` selected.)

## DATA-07 addendum form & delivery

| Option | Description | Selected |
|--------|-------------|----------|
| Sibling file inside `research_package/`, manifest untouched, supersedes erratum, folds its 2 corrections, nil-addendum case, ships on probe completion | Mirrors the established ERRATUM sibling-file pattern; matches DELIVERY-NOTE promise and STATE.md decision | ✓ |
| Phase-dir artifact only | Breaks the package-side delivery channel the DELIVERY-NOTE announced | |
| Amend claims-table.md in place | Violates package byte-stability (manifest hashes) | |

**Choice rationale:** Erratum precedent + STATE.md 2026-06-10 decision ("Phase 24 DATA-07 CLM-keyed correction addendum is the authoritative follow-up and must fold these in") + DATA-07 text (ships when probes finish, nil addendum allowed). (`[auto]` selected.)

## Issue-ledger seeding

| Option | Description | Selected |
|--------|-------------|----------|
| `24-ISSUE-LEDGER.md` in Phase 24 dir; v1.4 16-ISSUE-LEDGER schema + roadmap state machine; seed = full finding inventory @PENDING + CLM/DATA-keyed verified facts + anomalies section | Path and state machine transcribed from roadmap; schema from user-ratified v1.4 precedent | ✓ |
| New ledger schema designed for v1.5 | Process-artifact schema invention — STOP-protocol risk; precedent exists | |
| Defer all ledger creation to Phase 25 | Contradicts roadmap success criterion 5 ("seeds the issue ledger") | |

**Choice rationale:** Roadmap prescribes path locus and states; v1.4 precedent supplies the format; Phase 24 initializes only — operating protocol stays with Phase 25. (`[auto]` selected.)

---

## Claude's Discretion

- Probe language per probe (Python vs shell); probe/evidence file naming; `probes/` subfolder layout.
- Exact addendum filename (self-describing, e.g. `DATA-07-CORRECTION-ADDENDUM.md`).
- Verified-facts register placement (standalone file vs ledger section) — either satisfies roadmap criterion 5.
- Prose-sweep recording format for CLM-14+ extension rows.

## Deferred Ideas

- Adjudication verdicts and root-cause conflict resolution (ratio-SCS, `D = 6.694`) — Phases 25/27/28.
- README/dataset-doc corrections — proposed for user sign-off only; edits not Phase 24 work.
- Reusable probe packaging — FUT-03.
- M16 / G6 / training-loop metric usage — doc-03 milestone (SCOPE-11).

---

## Open Decisions — WR-01..04 Carry-In (surfaced, NOT decided)

> These four decisions were carried forward from Phase 23's review (`23-REVIEW.md:115-173`). The Phase 24 discuss step does not resolve them — they require user input per v1.5 STOP governance. If any is decided during planning without a grounding source, it becomes a `24-GAPS.md` entry.

### (a) WR-04: CLM-05 schema — split vs amend

**Decision point:** CLM-05 currently covers two distinct observables (IC folder counts and Brutus output file counts) that happen to coincide today but can diverge. Should the claims register split CLM-05 into CLM-05a (IC folders) / CLM-05b (Brutus output folders), or amend CLM-05's text to name both observables and require separate counts?

**Classification:** process-artifact schema → MUST-surface.
**Status:** OPEN

### (b) WR-01: Register sample-size figure as a new CLM row?

**Decision point:** The issue doc is internally inconsistent on sample size (line 204: 1000 pairs; P2-2 line 292: 100 pairs). The framed question's correction will report both figures neutrally. Should the sample-size figure be registered as a new CLM row to formally track this conflict, or is the neutral report in the framed-questions correction sufficient?

**Classification:** process-artifact schema → surface.
**Status:** OPEN

### (c) WR-02/WR-03: Correction channel for spec-citation fixes

**Decision point:** WR-02 and WR-03 are spec-citation typos in `framed-research-questions.md` — not dataset claims, so they do not fit the CLM-keyed DATA-07 addendum cleanly. Channel options: (A) a non-CLM appendix in the DATA-07 addendum, or (B) an interim extension to `ERRATUM-2026-06-10.md` so in-flight researchers get corrected pointers sooner.

**Classification:** operational coordination → surface.
**Status:** OPEN

### (d) Interim erratum extension vs consolidated addendum

**Decision point:** Should the corrected citations (WR-02/03) and conflict surfacing (WR-01) be issued as an interim erratum extension now, or held for the consolidated DATA-07 addendum after probes complete? The trade-off is timeliness for in-flight researchers vs a single canonical correction document.

**Classification:** operational coordination → surface.
**Status:** OPEN
