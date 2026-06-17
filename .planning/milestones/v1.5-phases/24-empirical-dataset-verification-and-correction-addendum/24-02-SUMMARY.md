---
phase: 24-empirical-dataset-verification-and-correction-addendum
plan: 02
subsystem: testing
tags: [data-verification, dataset-probes, mass-drift, stop-gap, verified-facts-register, v1.5]

# Dependency graph
requires:
  - phase: 24-01 (Wave 1 probes + register init)
    provides: 24-VERIFIED-FACTS.md scaffold (CLM-01/02/03/04/05/12 rows); probes/ directory
provides:
  - probes/data04_footers.py (DATA-04 footer-schema + no-footer-population probe)
  - probes/data05_mass_drift.py (DATA-05 float64 np.allclose mass-drift probe)
  - probes/data06_snapshots.py (DATA-06 snapshot-count + final-timestep distribution probe)
  - 24-VERIFIED-FACTS.md completed (CLM-06..11 + DATA-05 row + CLM-13 PENDING + zero CLM-14+)
  - 24-GAPS.md (GAP-24-01 — DATA-05 semantic STOP gap, later RESOLVED-WITH-INSTRUCTION)
  - .planning/milestones/v1.5-GAPS.md (milestone index, created with GAP-24-01)
affects: [phase 24-03 (DATA-07 addendum + ledger), phase 26 (PIPE-06 footers), phase 27 (PIPE-04 snapshots, PIPE-07 mass precision)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Interpreter gate (HARD): DATA-05 float64 np.allclose(rtol=1e-15) runs only under .venv/bin/python (numpy); system python3 aborts"
    - "No-footer population characterized as files with NO Result: footer at all AND NO parameter fields — never 'partial/minimal footer' (D-07)"
    - "Distributions per variant (min/median/mode/max + modal counts), not single examples; integer-rounded MEDIAN authoritative for CLM-10 (D-09)"
    - "Semantic STOP gap when empirical fact is clear but provenance/baseline is source-silent — verdict held, never silently chosen (D-16)"

key-files:
  created:
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data05_mass_drift.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data06_snapshots.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-GAPS.md"
    - ".planning/milestones/v1.5-GAPS.md"
  modified:
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md"

key-decisions:
  - "DATA-05 D-16 STOP gap FIRED: 70/4,857 base-hier files show m_Brutus(t=0) != m_IC at rtol=1e-15 (abs diff 0.1-1.0), while gold-hier matches 0/4,857; provenance source-silent → GAP-24-01 raised semantic, DATA-05 verdict HELD. Not recorded as a decimal.Decimal precision issue (diffs too large)."
  - "CLM-10 CORRECTED at integer-rounded MEDIAN per D-09 lock 2026-06-11: standard 59→61, hierarchical 125→127, gold 1000→1003; mode and pilot central value recorded as evidence only"
  - "CLM-07 (219) / CLM-08 (592) / CLM-09 (folder-default tol/dt_out) all confirmed; the 1,550/701/219 no-footer populations characterized per D-07 (no footer at all)"
  - "CLM-11 prevalence final_timestep>=9.5 = 1.000 across probe-applicable population; rule not re-adjudicated (D-06)"
  - "CLM-13 PENDING (D-05; not probed, routed Phase 25 EVID-10 / Phase 27 PIPE-09); CLM-06 ownership kept DATA-03/04 (D-04)"
  - "Prose sweep over RESEARCH-CONTEXT-MASTER.md + DELIVERY-NOTE.md found zero unregistered figures — no CLM-14+ rows; package byte-stable against 605c0227"

patterns-established:
  - "Erratum corrections re-probed from Phase 24's own evidence (D-07), not transcribed: no _gold_ infix; 1,550/701/219 no-footer populations"
  - "STOP-gap entry carries the full field list (decision point, source silence with file:line, math/engineering grounding, options A/B/C, confidence) — GAP-24-01 demonstrates the math grounding (mass is a dynamics parameter; 0.1-1.0 drift is neither round-trip nor perturbation)"

requirements-completed: [DATA-04, DATA-05, DATA-06]

# Metrics
duration: ~15min
completed: 2026-06-11
---

# Phase 24, Plan 02 Summary

**Three content-level probes (DATA-04/05/06) completed the verified-facts register (CLM-06..11 + CLM-13 PENDING); CLM-10 corrected at the median (61/127/1003); and DATA-05 surfaced GAP-24-01 — 70 base-hier mass-drift files with source-silent provenance — as a semantic STOP gap rather than silently picking a baseline.**

## Performance

- **Duration:** ~15 min (approximate; reconstructed at closure)
- **Started:** 2026-06-11 ~13:18 GMT+8 (Wave 2)
- **Completed:** 2026-06-11 (Wave 2)
- **Tasks:** 3 of 3 completed
- **Files created:** 3 probes + 2 gap registers + 1 (this summary); 1 modified (register)

## Accomplishments

- **DATA-04 footers (CLM-07/08/09):** `data04_footers.py` confirms **219** standard-gold files with NO `Result:` footer at all (D-07 characterization, agrees with `footer_audit_20251224_170141.md`), **592** `tol=1e-14` standard-gold footers (CLM-08), and per-variant modal `tol` values matching folder defaults (CLM-09). No-footer populations 1,550 / 701 / 219 / 0 across variants. All **confirmed**.
- **DATA-05 mass drift (D-16 STOP gap):** `data05_mass_drift.py` (numpy-gated, `np.allclose(rtol=1e-15)`, full population 15,028 pairs) found **70/4,857 base-hier mismatches** (abs diff 0.1–1.0), **0** in gold-hier / base-std / gold-std. Because perturbation does not touch masses (`ic_generation_utils.py:417-420`) and the gold variant matches the same IDs perfectly, the IC↔Brutus baseline for the 70 base-hier files was **source-silent** → raised **GAP-24-01** (semantic) and **held** the DATA-05 verdict per D-16. Not framed as a `decimal.Decimal` precision issue (diffs too large for round-trip).
- **DATA-06 snapshots (CLM-10 corrected, CLM-11):** `data06_snapshots.py` records per-variant distributions; integer-rounded **medians 61 / 127 / 1003** (standard / hier / gold) → CLM-10 **corrected** (claim ~59/~125/~1000) with mode and pilot value as evidence only. `final_timestep >= 9.5` prevalence **1.000** across the probe-applicable population (CLM-11 confirmed).
- **Register completed + prose sweep:** CLM-06 (4,857; DATA-03/04 ownership preserved per D-04), CLM-13 **PENDING** (routed Phase 25/27, D-05), and the D-06 prose sweep over `RESEARCH-CONTEXT-MASTER.md` + `DELIVERY-NOTE.md` found **zero** unregistered figures (no CLM-14+). Package **byte-stable** against `605c0227`.
- **Read-only fences held (D-01):** `git status --short simulation_data/` clean after every probe.

## Task Commits

Single Wave 2 atomic commit per D-25:

1. **Task 1: DATA-04 footer-schema probe** — `b1c948ee` (evidence)
2. **Task 2: DATA-05 mass-drift probe (+ GAP-24-01)** — `b1c948ee` (evidence)
3. **Task 3: DATA-06 distributions + register completion** — `b1c948ee` (evidence)

**Plan metadata / commit:** `b1c948ee` `evidence(24-02): footer / mass-drift / snapshot probes with register and gap` (Agent-Assisted-By trailer present).

## Files Created/Modified

- `probes/data04_footers.py` — DATA-04 footer-schema + no-footer-population probe.
- `probes/data05_mass_drift.py` — DATA-05 float64 `np.allclose(rtol=1e-15)` mass-drift probe (numpy-gated).
- `probes/data06_snapshots.py` — DATA-06 snapshot-count + final-timestep distribution probe (`\n\n` block split).
- `24-VERIFIED-FACTS.md` — completed with CLM-06..11 rows, DATA-05 row, CLM-13 PENDING, zero CLM-14+, Anomalies (D-12) entry for the base-hier mass drift.
- `24-GAPS.md` — GAP-24-01 semantic STOP gap (DATA-05 hierarchical mass-drift baseline).
- `.planning/milestones/v1.5-GAPS.md` — milestone gap index created with GAP-24-01.
- `24-02-SUMMARY.md` — this summary.

## Decisions Made

- DATA-05 raised as a semantic STOP gap (GAP-24-01) instead of choosing a baseline — the empirical fact was clear, the provenance was not. Resolved later the same day by user instruction (current ICs canonical; 70 base-hier outputs quarantined pending targeted rerun).
- CLM-10 corrected at the integer-rounded median (D-09 lock 2026-06-11); the `~` claim prefix preserved, empirical medians recorded as the authoritative fact.

## Deviations from Plan

- **Summary authored at Phase 24 closure (2026-06-11), not at plan-execution time.** Reconstructed from the committed evidence (`b1c948ee`), the verified-facts register, `24-GAPS.md`, and the 24-UAT.md re-verification pass (all three probes re-run 2026-06-11 and confirmed consistent with committed stdout; only difference a benign DeprecationWarning stderr line). Timings approximate.
- **DATA-05 STOP gap fired (expected branch):** the plan's D-16 contingency was exercised — this is governed behavior, not a deviation in the failure sense. GAP-24-01 was raised, the verdict held, and Phase 24 closure / PIPE-07 consumption were blocked until the user resolved it.
- **`probes/outputs/*` stdout not committed:** git policy blocks `outputs/*`; register rows are the committed re-derivable evidence (D-02). Recorded deviation.

## Issues Encountered

- **GAP-24-01 (DATA-05):** 70 base-hier files with unexplained mass drift. Resolved 2026-06-11 by user instruction → `RESOLVED-WITH-INSTRUCTION`: current ICs canonical; 70 affected outputs (`0005`-`0059`, `0061`-`0075`) invalid/stale, quarantined from training/metrics/PIPE-07 pending targeted rerun. The rerun was subsequently executed and validated 2026-06-11 (separate remediation, `24-DATA05-RERUN-REMEDIATION.md`; post-swap probe reports 0/4,857 mismatches).

## Next Phase Readiness

- Register complete for CLM-01..12 + CLM-13 PENDING — ready for plan 24-03 (DATA-07 addendum + issue-ledger seed).
- DATA-05 verdict resolved as a decision; the data-repair boundary is tracked separately and must not be read as "files already fixed" at the time of this plan.

---
*Phase: 24-empirical-dataset-verification-and-correction-addendum*
*Completed: 2026-06-11*
