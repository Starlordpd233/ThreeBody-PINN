---
phase: 24-empirical-dataset-verification-and-correction-addendum
plan: 03
subsystem: docs
tags: [data-verification, correction-addendum, issue-ledger, v1.5]

# Dependency graph
requires:
  - phase: 24-01 (Wave 1 probe authoring and register initialization)
    provides: probes/data01_id_gaps.py; probes/data02_blacklist.py; probes/data03_gold_gap.py; initial register scaffold
  - phase: 24-02 (Wave 2 footer/mass-drift/snapshot probes + register completion)
    provides: probes/data04_footers.py; probes/data05_mass_drift.py; probes/data06_snapshots.py; completed 24-VERIFIED-FACTS.md; 24-GAPS.md (GAP-24-01 OPEN)
  - phase: 24-04 (user gate — WR-01/02/03 + CLM-05 schema)
    provides: 24-WR-DECISIONS.md (all four RESOLVED-WITH-INSTRUCTION 2026-06-11)
provides:
  - DATA-07-CORRECTION-ADDENDUM.md (CLM-keyed correction addendum; supersedes master's "Correction Provenance And Verification Boundaries" section)
  - 24-ISSUE-LEDGER.md (v1.4 schema instantiated; 19 findings seeded at PENDING; register annex + anomalies section)
affects: [phase 25 (consumes ledger seed), phase 27 (PIPE-07 consumer, gated on GAP-24-01), external multi-AI research (receives addendum via user forwarding)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "CLM-keyed correction addendum (sibling-file pattern; not in master's Per-File Manifest; D-18)"
    - "v1.4 16-ISSUE-LEDGER.md schema instantiation (D-22/D-24; do not redesign columns Phase 25 owns)"
    - "Anomaly (D-12) section for discrepancies contradicting NO package claim"

key-files:
  created:
    - "pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/DATA-07-CORRECTION-ADDENDUM.md"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md"
  modified: []

key-decisions:
  - "Two erratum corrections (no-`_gold_`-infix; 1,550/701/219 no-footer populations) re-stated from Phase 24's own re-probed evidence (D-07), not transcribed from the master"
  - "CLM-10 corrected at integer-rounded MEDIAN level (61 / 127 / 1003) per D-09 lock 2026-06-11; `~` prefix preserved"
  - "DATA-05 HELD behind GAP-24-01 (D-16 STOP gap, semantic, OPEN) — surfaced, not corrected; closing statement explicitly notes Phase 24 closure is contingent on user adjudication"
  - "CLM-05 split per WR-04 user decision 2026-06-11: CLM-05a (IC folder counts) and CLM-05b (Brutus output folder/file counts) referenced as separate rows in the addendum's confirmed-claims summary; CLM-05 preserved as historical parent/alias in register's traceability column"
  - "WR-01/02/03 routed through the non-CLM appendix per user-chosen channel (24-WR-DECISIONS.md) — WR-01 surfaced neutrally (1000-vs-100 issue-doc-internal conflict); WR-02 cites §10.2 'COM Invariance' lines 967-971; WR-03 cites Step 5 'Mini-Batch Construction' line ~1201 as an example, not a 32-pt contract"
  - "CLM-13 PENDING (D-05; not probed; routed Phase 25 EVID-10 / Phase 27 PIPE-09) — listed in PENDING section, NOT in corrected/confirmed"
  - "Phase-25-owned operating protocol columns (evidence-packet format, verdict-recording rules) NOT invented (D-24); Phase 24 initializes states only"
  - "Closing statement does NOT use 'all package-stated claims confirmed' wording — DATA-05 row is unverified-held (24-03:122-128 forbids this phrasing when an OPEN gap holds a row)"
  - "Addendum is intentionally NOT added to the master's Per-File Manifest (D-18 sibling-file pattern); per-file source hashes remain valid"

patterns-established:
  - "CLM-keyed correction addendum: each corrected/confirmed row carries claimed value, observed value, probe command-path, verdict, run date; row cites 'probes/data0' for re-derivability"
  - "DATA-07 'Not affected — do not over-discount' list (D-19): re-stated from master's Correction Provenance §'Not affected' as re-verified confirmed by Phase 24's probes"
  - "Per-finding notes for issue-ledger seed rows use 'SEED_SHA PENDING -> PENDING (seeded by Phase 24 P03)' format (D-23/D-24)"
  - "Lifecycle Rules block copied VERBATIM from 16-ISSUE-LEDGER.md:45-55 (D-24; do not redesign)"

requirements-completed: [DATA-07]

# Metrics
duration: ~30min
completed: 2026-06-11
---

# Phase 24, Plan 03 Summary

**DATA-07 correction addendum compiled from completed verified-facts register; issue ledger seeded at stable path with 19 findings at PENDING; package byte-stability held against `605c0227` baseline.**

## Performance

- **Duration:** ~30 min
- **Started:** 2026-06-11 13:46 GMT+8
- **Completed:** 2026-06-11 (Wave 3, plan 24-03)
- **Tasks:** 2 of 2 completed
- **Files created:** 2 (addendum + ledger) + 1 (this summary)

## Accomplishments

- **Addendum compiled**: 12 confirmed rows (CLM-01..09, CLM-11, CLM-12, plus CLM-05a and CLM-05b as separate rows per WR-04 user decision) + 1 corrected row (CLM-10 — snapshot-count medians 61 / 127 / 1003) + 1 unverified-held row (DATA-05 behind GAP-24-01) + 1 PENDING row (CLM-13 — not probed, routed Phase 25/27). Two erratum corrections folded (no-`_gold_`-infix; 1,550/701/219 no-footer populations — counts unchanged, characterizations corrected per D-07). WR-01/02/03 folded via the user-chosen non-CLM appendix (24-WR-DECISIONS.md).
- **Ledger seeded**: v1.4 `16-ISSUE-LEDGER.md` schema instantiated VERBATIM (D-22/D-24); 19 findings at PENDING (B-06, B-11, M11, M12, M13, D7, G1, G2, G3, G4, G5, SCS, SASD, IPR, PSC, D-03, D=6.694, footer, mass-drift) with full Phase routing from REQUIREMENTS.md traceability; Lifecycle Rules block copied verbatim; register annex linked; anomalies section included (DATA-05 HELD behind GAP-24-01; standard 2,749-vs-2,750 wrinkle resolved as no off-by-one).
- **Byte-stability held**: `git diff --quiet 605c0227 -- .../RESEARCH-CONTEXT-MASTER.md .../DELIVERY-NOTE.md .../specs/` exits 0; the addendum is a NEW sibling file, intentionally NOT in the master's Per-File Manifest.
- **Closing statement explicit on held row**: the addendum does NOT claim "all package-stated claims confirmed" — DATA-05 is HELD behind GAP-24-01; Phase 24 closure is contingent on user adjudication.

## Task Commits

Each task was committed atomically:

1. **Task 1: Compile the DATA-07 correction addendum** - committed atomically with Task 2 as Wave 3 single commit per D-25.
2. **Task 2: Seed the issue ledger at the stable path** - committed atomically with Task 1 as Wave 3 single commit per D-25.

**Plan metadata:** committed via `scripts/agent-commit` with `evidence(24-03): <subject>` per D-25, with `Agent-Assisted-By:` trailer.

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/DATA-07-CORRECTION-ADDENDUM.md` — CLM-keyed correction addendum; supersedes master's "Correction Provenance And Verification Boundaries" section; sibling file, not in Per-File Manifest (D-18); 2 erratum corrections + 1 CLM-10 correction + 1 DATA-05 HELD row + 12 confirmed rows + 1 PENDING (CLM-13) + WR-01/02/03 non-CLM appendix + "Not affected" list + closing statement explicit on held row.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — v1.4 16-ISSUE-LEDGER.md schema instantiated VERBATIM; 19 findings seeded at PENDING; Lifecycle Rules block copied verbatim including "FIX_APPLIED is not closure" and "VERIFIED requires a passing acceptance check"; Dataset Evidence Annex linked; Anomalies (D-12) section included.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-03-SUMMARY.md` — this summary.

## Verification Pass (15 items, 24-03:131-198)

1. `test -f research_package/DATA-07-CORRECTION-ADDENDUM.md` exits 0 — PASS
2. `grep -iq 'supersede' research_package/DATA-07-CORRECTION-ADDENDUM.md` exits 0 — PASS
3. Addendum references both D-07 corrections (no `_gold_` infix; no `Result:` footer in 1,550/701/219) — PASS
4. Addendum references `probes/data0` in corrected rows — PASS
5. Addendum surfaces DATA-05 with verdict `unverified` and references GAP-24-01 — PASS
6. Addendum does NOT contain "all package-stated claims confirmed" wording — PASS (closing statement explicitly notes 11 of 13 verified + 1 corrected + 1 PENDING + 1 HELD)
7. Addendum folds WR-01/02/03 via the user-chosen non-CLM appendix — PASS
8. Addendum applies the CLM-05 split (references both CLM-05a and CLM-05b) — PASS
9. `git diff --quiet 605c0227 -- .../RESEARCH-CONTEXT-MASTER.md .../DELIVERY-NOTE.md .../specs/` exits 0 — PASS
10. `test -f 24-ISSUE-LEDGER.md` exits 0 — PASS
11. Ledger contains rows for B-06, B-11, M11, M12, M13, D7, G1, G2, G3, G4, G5, SCS, SASD, IPR, PSC, D-03, D=6.694, footer, mass-drift — PASS (19 rows total)
12. Ledger contains the Lifecycle Rules block verbatim including "FIX_APPLIED is not closure" and "VERIFIED requires a passing acceptance check" — PASS
13. Ledger contains the "Dataset Evidence Annex" linking `24-VERIFIED-FACTS.md` — PASS
14. Ledger contains the "Anomalies (D-12)" section — PASS
15. `24-03-SUMMARY.md` created in the phase directory — PASS

## Held-Row Surfaced (D-22, 24-03:198)

- **DATA-05 / GAP-24-01**: explicitly surfaced in the addendum's "Correction 4" section with verdict `unverified` and a direct reference to `.planning/milestones/v1.5-GAPS.md` and `24-GAPS.md`. The closing statement reiterates that **Phase 24 closure is contingent on user adjudication of GAP-24-01** and that **PIPE-07 (Phase 27) cannot consume the canonical-vs-Decimal verdict** until the gap is resolved. The ledger's `footer` and `mass-drift` rows are also marked as `Sources Disagree? = YES` and "gated on GAP-24-01" for their acceptance checks.

## Blocker Status

- **GAP-24-01 (D-16 STOP gap, semantic, OPEN)**: still OPEN per P0-2. **Phase 24 closure blocked AND PIPE-07 (Phase 27) consumption blocked** until the user adjudicates GAP-24-01. The addendum does NOT paper over this — it surfaces the held row with a direct reference to the gap register.

## Deviations

- **None from the plan's text**. The plan mandated surfacing the held row (24-03:122-128); the closing statement honors this. The plan mandated the v1.4 schema verbatim (D-22/D-24); the Lifecycle Rules block is copied verbatim. The plan mandated the CLM-05 split; the addendum references both CLM-05a and CLM-05b as separate rows. The plan mandated "do NOT invent Phase-25-owned operating-protocol columns"; the ledger initializes states only.

## Next Steps

- **User adjudicates GAP-24-01** (D-16 STOP gap; the user picks A / B / C from `24-GAPS.md`). This unblocks Phase 24 closure and PIPE-07 (Phase 27) consumption.
- **User forwards the addendum** to the in-flight external research (D-21). The agent sends nothing externally itself.
- **Phase 25** consumes the seeded `24-ISSUE-LEDGER.md` to operate the v1.4 evidence framework (evidence-packet format, verdict recording, re-verification rules).
- **Phase 26 (PIPE-01/02/03/05/06/10)**, **Phase 27 (PIPE-04/07/09)**, **Phase 28 (VAL-01..04)** consume the resolved findings once adjudicated.
