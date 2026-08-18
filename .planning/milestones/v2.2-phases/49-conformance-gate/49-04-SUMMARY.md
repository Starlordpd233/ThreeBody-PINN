---
phase: 49-conformance-gate
plan: 04
subsystem: testing
tags: [conformance, census, divergence-register, preflight, pytest]

# Dependency graph
requires:
  - phase: 49-conformance-gate
    provides: "49-01 run-start PHYS-05 table assertion and preflight artifact seam"
provides:
  - "Explicit D-07/D-09 placeholder census with instrumentation and provisional-field disagreement findings"
  - "Fail-closed INST-03 divergence register with proof-test and waiver validation"
  - "Composed preflight evidence containing table checks, census results, open register entries, and findings"
affects: [49-05 evaluation eligibility, 49-06 end-to-end seam, phase-50 evaluation]

# Actuals (#2632)
actuals:
  tokens: 14791
  tasks: 3
  commits: 8

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Explicit ordered conformance manifests with class-specific runtime probes"
    - "Fail-closed JSON envelopes and deterministic atomic artifact serialization"
    - "Refusal-first preflight evidence that preserves all open caveats"

key-files:
  created:
    - pinn/conformance/register.py
    - pinn/conformance/divergence_register.json
    - pinn/conformance/census.py
    - tests/phase49/test_gate02_census.py
    - tests/phase49/test_inst03_register.py
  modified:
    - pinn/conformance/preflight.py

key-decisions:
  - "The census population is a hand-authored, spec-cited manifest in declaration order; it is never inferred from reflection or provisional fields."
  - "Every closed register entry must cite a real passing proof-test node, while waivers only cite already-granted authority and never grant authority themselves."
  - "Open register entries of every kind are copied verbatim into preflight evidence; only downstream evaluation eligibility applies the divergence-kind gate."
  - "Accelerator metadata resolution retries on CPU after a runtime device failure, avoiding a backend availability probe prohibited by the repository's precision-default checks."

patterns-established:
  - "Census class-4 placeholders block without an explicit waiver and disagreements are recorded without adopting either classification."
  - "Preflight writes failed evidence before propagating a table or census refusal."

requirements-completed: [GATE-02, INST-03]

coverage:
  - id: D1
    description: "Explicit placeholder census covers the D-08 population, blocks unwaived placeholders, records provisional disagreements, and checks instrumentation fields."
    requirement: GATE-02
    verification:
      - kind: unit
        ref: "tests/phase49/test_gate02_census.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "Divergence register validates fail-closed, preserves mandatory entries, and executes every closed proof-test node."
    requirement: INST-03
    verification:
      - kind: unit
        ref: "tests/phase49/test_inst03_register.py::test_every_closed_register_entry_has_a_real_passing_proof_test"
        status: pass
    human_judgment: false
  - id: D3
    description: "Run-start preflight composes table, census, open-register, and findings evidence with refusal-first and byte-idempotent writes."
    requirement: INST-03
    verification:
      - kind: integration
        ref: "tests/phase49/test_inst03_register.py::test_refusal_writes_failing_census_artifact_before_raise"
        status: pass
      - kind: integration
        ref: ".venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py tests/phase49/test_inst03_register.py tests/phase49/test_gate01_table.py"
        status: pass
    human_judgment: false

# Metrics
duration: 20min
completed: 2026-08-04
status: complete
---

# Phase 49 Plan 04 Summary

**Explicit GATE-02 census and self-defending INST-03 divergence register composed into refusal-first preflight evidence**

## Performance

- **Duration:** 20 minutes
- **Started:** 2026-08-04T22:20:23-07:00
- **Completed:** 2026-08-04T22:37:10-07:00
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Added the ordered 28-entry census manifest, resolution probes, placeholder blocking, provisional disagreement reporting, and STEP_LOG_FIELDS instrumentation precondition.
- Added the validated divergence register and committed D-24 entries, including mandatory qualifications, scoped waivers, open divergences, and proof-test meta-validation.
- Extended `run_start_preflight` without changing `pinn/train.py`; preflight now persists census/register/findings evidence on both success and refusal paths.

## Task Commits

Each TDD task was committed atomically (RED test followed by GREEN implementation):

1. **Task 1: The divergence register — schema, loader, and D-24 contents** - `2f1e2e23` (test), `11e2de00` (feat)
2. **Task 2: The placeholder census — manifest, resolution classes, and verdict** - `58fece1b` (test), `85c41a68` (feat)
3. **Task 3: Preflight composition — census, register, findings, and refusal ordering** - `d989ad89` (test), `d43d98bf` (feat)
4. **Rule-1 correction:** `93225ba3` (fix)

**Plan metadata:** pending final GSD metadata commit.

## Files Created/Modified

- `pinn/conformance/register.py` - strict schema loader/writer with duplicate, proof-test, and waiver checks.
- `pinn/conformance/divergence_register.json` - 16-entry derived register with closed proof nodes and cited waivers.
- `pinn/conformance/census.py` - explicit manifest, class resolution, findings, and instrumentation checks.
- `pinn/conformance/preflight.py` - composed run-start evidence and refusal-first artifact writes.
- `tests/phase49/test_gate02_census.py` - census completeness, blocking, disagreement, instrumentation, and determinism tests.
- `tests/phase49/test_inst03_register.py` - schema, proof-test, composition, ordering, collision, and consistency tests.

## Decisions Made

The implementation follows the plan's D-07/D-09/D-25/D-27 contracts. The census remains authoritative for population and class expectations, while provisional configuration disagreements are findings only. The register remains a derived reporting artifact: it grants no waiver and all open entries travel verbatim into preflight for downstream interpretation.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Blocking prohibition] Removed backend availability probe from preflight metadata resolution**

- **Found during:** bounded broader-suite validation after Task 3
- **Issue:** `torch.backends.mps.is_available()` in the new preflight module violated the repository's precision-default prohibition test.
- **Fix:** Resolve clip facts on the configured device and retry on CPU only after a runtime device failure; no backend availability probe remains.
- **Files modified:** `pinn/conformance/preflight.py`
- **Verification:** `tests/phase38/test_prohibitions.py -k no_precision_default_in_discovered_modules` and the full focused Phase-49 selection both pass.
- **Committed in:** `93225ba3`

**2. [Plan evidence adjustment] Used a focused Phase-48 proof node for C-05**

- **Found during:** Task 1 proof-test selection
- **Issue:** the shipped YAML launch fixture currently fails before training because its empty invariants mapping is interpreted as `None` by the pre-existing 49-02 configuration path; it cannot serve as a passing closed-proof node.
- **Fix:** C-05 cites the passing focused Stage-0 energy configuration test, preserving a real executable proof without changing unrelated Phase-41 fixtures.
- **Files modified:** `pinn/conformance/divergence_register.json`
- **Verification:** the register proof-test meta-test passes.
- **Committed in:** `11e2de00`

**Total deviations:** 2 (one correctness fix, one proof-node selection adjustment).

## Issues Encountered

The bounded broad selection (`tests/phase38`, `tests/phase40`–`tests/phase49` and selected Phase-43 modules) was stopped after approximately 161 seconds at 18 failures and 471 passes while entering a long Phase-42 fixture. The known failures are primarily the pre-existing Phase-41 launch fixtures using `lambda_e_max: 1.0`, which the 49-01 locked Stage-0 gate correctly rejects; those fixtures are outside this plan's owned paths and are already documented by the prior phase summaries. Focused Phase-49 validation is fully green: 48 tests passed in 12.07 seconds, and the targeted prohibition test passed with 48 subtests.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

GATE-02 and INST-03 are ready for 49-05's evaluation-eligibility predicate and 49-06's end-to-end seam. The register's `INV-B-N-UNSET` entry remains intentionally open and unwaived pending the owner decision reserved for the later phase; no value was invented here.

---
*Phase: 49-conformance-gate*
*Plan: 04*
*Completed: 2026-08-04*

## Self-Check: PASSED

- Summary file exists at the canonical phase path.
- All seven task/fix commits are present in git history.
- No unintentional generated or placeholder stub files were introduced.
