---
phase: 24-empirical-dataset-verification-and-correction-addendum
plan: 01
subsystem: testing
tags: [data-verification, dataset-probes, verified-facts-register, read-only, v1.5]

# Dependency graph
requires:
  - phase: 23 (research package assembly)
    provides: RESEARCH-CONTEXT-MASTER.md CLM Claims Register (the claimed values this plan re-derives)
provides:
  - probes/data01_id_gaps.py (DATA-01 ID-gap probe — both [0..max] and [0..nominal] conventions)
  - probes/data02_blacklist.py (DATA-02 blacklist composition + nuanced consumption map)
  - probes/data03_gold_gap.py (DATA-03 authoritative base−gold set-diff)
  - 24-VERIFIED-FACTS.md seeded with CLM-01/02/03/04/05/12 rows + Anomalies + D-13 grounding sections
affects: [phase 24-02 (completes the register), phase 24-03 (DATA-07 addendum + ledger consume the register), phase 25 (ledger seed)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Disposable read-only probe under probes/ with a D-02 re-derivability header (repo-root run command + dataset paths + what it records)"
    - "ID-gap computed as a missing-ID SET against the nominal range (regex ID parse), never from a bare file count (D-13)"
    - "Authoritative set-diff base_ids − gold_ids (not a 4-digit grep that captures summary numbers — Pitfall 5)"
    - "Verified-facts register row schema: CLM ID · owning DATA · claimed · observed · probe command · dataset path · run date · verdict (D-02/D-08)"

key-files:
  created:
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data01_id_gaps.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data02_blacklist.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data03_gold_gap.py"
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md"
  modified: []

key-decisions:
  - "D-13 nominal-range convention GROUNDED (no STOP gap): README.md:146-153 declares ID ranges 0000-3998 / 0000-4999 with Gaps 1,250 / 143; adopted nominal end = observed max ID, gaps[0..max] authoritative. The conditional D-13 STOP-gap branch did NOT fire."
  - "CLM-01 confirmed at 1,250 (standard gaps[0..max]); gaps[0..3999]=1,251 emitted as a non-canonical artifact for transparency"
  - "CLM-05 recorded with BOTH observables inline (IC folder 2,749; Brutus base 2,749; Brutus gold 2,565) per WR-04 PROBE disposition; the register-schema split into CLM-05a/CLM-05b was the user's WR-04 gate (plan 24-04), applied later"
  - "M11 (blacklist not loaded at training time) recorded unverified — outside grounding limits (SCOPE-10/D-10), deferred to Phase 25 + FUT-01"

patterns-established:
  - "Every register row cites an executable .venv/bin/python repo-root probe command + dataset path + run date so any later agent reproduces the count without this session's context"
  - "DATA-02 consumption recorded as a nuanced map (readiness-checks load the json; current runners use Documentation/problematic_ics/ dirs; README:1005 calls the json legacy), not a flat yes/no"

requirements-completed: [DATA-01, DATA-02, DATA-03]

# Metrics
duration: ~12min
completed: 2026-06-11
---

# Phase 24, Plan 01 Summary

**Three read-only filesystem/ID probes (DATA-01/02/03) authored and run over the on-disk dataset, seeding the verified-facts register with CLM-01/02/03/04/05/12 — all confirmed, with the D-13 nominal-range convention grounded in README so no STOP gap fired.**

## Performance

- **Duration:** ~12 min (approximate; reconstructed at closure)
- **Started:** 2026-06-11 ~13:13 GMT+8 (Wave 1)
- **Completed:** 2026-06-11 (Wave 1)
- **Tasks:** 3 of 3 completed
- **Files created:** 4 (3 probes + register) + 1 (this summary)

## Accomplishments

- **DATA-01 ID gaps (CLM-01/02/12):** `data01_id_gaps.py` parses zero-padded 4-digit IDs via regex and computes the missing-ID set against the nominal range. Standard: n=2,749, min=0, max=3,998, gaps[0..max]=**1,250** (gaps[0..3999]=1,251 also emitted). Hierarchical: n=4,857, max=4,999, gaps=**143**. CLM-01/02/12 all **confirmed**.
- **DATA-02 blacklist (CLM-03):** `data02_blacklist.py` re-derives `problematic_ics_blacklist.json` as `{hierarchical: 2, standard: 63}` = **65** (confirmed). Consumption recorded as a nuanced map: `dataset_readiness_checks` loads the json; current Brutus runners do not (use `Documentation/problematic_ics/{type}/`; README:1005 "legacy"); the `pinn/` training-time aspect (M11) recorded `unverified — outside grounding limits (SCOPE-10/D-10)`.
- **DATA-03 gold gap (CLM-04/05):** `data03_gold_gap.py` computes the authoritative `base_ids − gold_ids` set diff = **184**, exact 184/184 match against `standard_quasi_random_ids_not_in_gold.md` (not a naive grep). Per WR-04 it counts IC folders AND Brutus output folders **separately**: IC `ic_standard_quasi_random` = 2,749; Brutus base = 2,749; Brutus gold = 2,565. CLM-04 **confirmed**; CLM-05 observables recorded for the later WR-04 schema gate.
- **Register seeded:** `24-VERIFIED-FACTS.md` created with CLM-01/02/03/04/05/12 rows (each carrying probe command + dataset path + run date + verdict), the D-13 nominal-range grounding section, the DATA-02 nuanced consumption map, a D-11 doc-contradiction check (no contradictions for these rows), and a reserved Anomalies (D-12) section.
- **Read-only fences held (D-01):** `git status --short simulation_data/` clean after every probe; no writes under `simulation_data/`, `Scripts/`, `Validation/`, or `pinn/`.

## Task Commits

Each task was committed atomically (single Wave 1 atomic commit per D-25):

1. **Task 1: DATA-01 ID-gap probe** — `0ca0e2d6` (evidence)
2. **Task 2: DATA-02 blacklist + DATA-03 gold-gap probes** — `0ca0e2d6` (evidence)
3. **Task 3: initialize verified-facts register** — `0ca0e2d6` (evidence)

**Plan metadata / commit:** `0ca0e2d6` `evidence(24-01): id-gap blacklist and gold-gap probes with verified-facts register` (Agent-Assisted-By trailer present).

## Files Created/Modified

- `probes/data01_id_gaps.py` — DATA-01 ID-gap probe (regex ID parse; emits gaps[0..max] and gaps[0..nominal]).
- `probes/data02_blacklist.py` — DATA-02 blacklist composition + consumption-grep harness.
- `probes/data03_gold_gap.py` — DATA-03 authoritative set-diff gold-counterpart probe (IC + Brutus counted separately, WR-04).
- `24-VERIFIED-FACTS.md` — verified-facts register seeded with CLM-01/02/03/04/05/12, D-13 grounding, consumption map, anomalies section.
- `24-01-SUMMARY.md` — this summary.

## Decisions Made

- D-13 nominal-range convention is grounded (README:146-153) → adopted nominal end = observed max ID; the conditional semantic STOP-gap branch did NOT fire.
- CLM-05's two observables (IC vs Brutus folder counts) recorded inline pending the WR-04 register-schema gate (plan 24-04), which later split them into CLM-05a/CLM-05b.

## Deviations from Plan

- **Summary authored at Phase 24 closure (2026-06-11), not at plan-execution time.** Waves 1–2 committed their probe/register evidence atomically without per-plan SUMMARY.md files; this summary is reconstructed from the committed artifacts (`0ca0e2d6`), the verified-facts register, and the 24-UAT.md re-verification pass (all DATA-01/02/03 probes re-run and confirmed byte-identical 2026-06-11). Timings are approximate.
- **`probes/outputs/*` stdout not committed:** the git policy (`scripts/git_policy/validate_staged_paths.py`) blocks `outputs/*` from staging. Per D-02, the register rows (probe command + dataset path) are the committed, re-derivable evidence; stdout is regenerated on demand. Recorded deviation; no other deviation occurred.

## Issues Encountered

None — all three probes ran read-only under `.venv/bin/python`; observed values matched the package claims.

## Next Phase Readiness

- Register ready for plan 24-02 to complete (CLM-06..11 + DATA-05 + CLM-13 PENDING + prose sweep).
- No blockers introduced by this plan.

---
*Phase: 24-empirical-dataset-verification-and-correction-addendum*
*Completed: 2026-06-11*
