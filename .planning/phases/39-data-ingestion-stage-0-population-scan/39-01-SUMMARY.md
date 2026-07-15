---
phase: 39-data-ingestion-stage-0-population-scan
plan: "01"
subsystem: testing
tags: [unittest, test-contract, nyquist-wave-0, data-ingestion, fixtures, prohibitions, deferred-imports]

# Dependency graph
requires:
  - phase: 38-pinn-model-rebuild-from-specs-fut-01
    provides: pinn/verification/fixture_loader.py parse patterns, gradcheck_probe atomic-write/CLI patterns, runtime/architecture_spec frozen-dataclass patterns, tests/phase38 unittest + prohibition style
provides:
  - Complete nine-file dataset-free Wave-0 test contract for all Phase 39 behaviors (DATA-01..06)
  - Deterministic TinyCorpus on-disk fixture builder (read-only, TemporaryDirectory-scoped, README 4->2 mapping)
  - Executable mechanical boundary audit (sole-reader allowlist, sole-classifier, no-floor/footer/metrics/s0-mutation) that runs green today and self-tests every detector
  - Frozen executable expectations Plans 02-06 must implement against (types, adapter, classifier, admission, splits, batches, stage-scan)
affects: [39-02, 39-03, 39-04, 39-05, 39-06, 39-07, pinn/data]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Single _SKIP_PHRASE constant imported by every module-local _require helper; skip reason = '<phrase> <module>.<symbol>' for the Wave-5 deterministic grep"
    - "Per-symbol deferred import (SkipTest not ImportError) so contract files land before production without discovery ERRORs"
    - "Pure mechanical detectors + per-detector self-tests so the audit can FAIL on injected violations before production code exists"
    - "Contract decomposition into pure boundary helpers (conservation eps_H->SCS, near-zero-H0 predicate, collocation quota) so exact boundaries are testable dataset-free"

key-files:
  created:
    - tests/phase39/__init__.py
    - tests/phase39/_fixtures.py
    - tests/phase39/test_adapter.py
    - tests/phase39/test_stages.py
    - tests/phase39/test_admission.py
    - tests/phase39/test_splits.py
    - tests/phase39/test_batches.py
    - tests/phase39/test_stage_scan.py
    - tests/phase39/test_prohibitions.py
  modified: []

key-decisions:
  - "Executed tasks in dependency order 39-01-02 -> 39-01-01 -> 39-01-03 because test_adapter/test_stages import _SKIP_PHRASE from __init__.py and consume _fixtures.py (both owned by task 02); each task still committed its own files atomically"
  - "requirements-completed left empty: Wave 0 delivers only the executable test contract; DATA-01..06 are completed by later waves (production + real-corpus gate), so marking them complete now would be a false traceability claim"
  - "Followed 39-PATTERNS.md type vocabulary as the frozen contract: Variant/Fidelity enums on records, str variant/fidelity on PhysicalKey/RecordKey, closed StageLabel {0,1,UNASSIGNED}, MISSING_BASE/MISSING_GOLD as split-only sentinels"
  - "Modeled degenerate-Lmax as a NaN angular-momentum ratio so the classifier returns UNASSIGNED without inventing a bespoke attribute"

patterns-established:
  - "Wave-0 deferred-contract scaffold: discoverable, dataset-free, skip-clean until production lands"
  - "TinyCorpus deterministic relative-bytes manifest for two-build determinism checks"

requirements-completed: []

coverage:
  - id: D1
    description: "Nine-file Phase 39 test suite is discoverable and dataset-free — unittest discover collects all 105 tests with zero import ERRORs; absent production symbols cause localized skips via the single _SKIP_PHRASE, never discovery failures"
    verification:
      - kind: unit
        ref: "python -m unittest discover -s tests/phase39 -p 'test_*.py' => Ran 105, OK (skipped=80)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Deterministic read-only TinyCorpus fixture + mechanical boundary audit run green now: sole-reader allowlist (GAP-39-02), sole-classifier/no-floor/footer/metrics/s0 bans (GAP-39-08), per-detector self-tests, and TinyCorpus determinism/containment/4->2-mapping/asymmetric-pairing contract"
    verification:
      - kind: unit
        ref: "tests/phase39/test_prohibitions.py => 24 pass, 2 deferred skips"
        status: pass
    human_judgment: false
  - id: D3
    description: "Deferred executable contracts for DATA-01..06 (shared types, adapter residency/version/labels, sole classifier, seven admission clauses + GAP-39-04/05, grouped Hamilton split + GAP-39-11 MISSING_BASE, replay/lookahead + GAP-39-10/12, Stage-0 scan + 239/240 fatal mechanics) encode the frozen behavior Plans 02-06 must satisfy"
    verification:
      - kind: unit
        ref: "tests/phase39/{test_adapter,test_stages,test_admission,test_splits,test_batches,test_stage_scan}.py collect + skip cleanly (80 deferred skips)"
        status: pass
    human_judgment: true
    rationale: "The contracts are discoverable and skip-clean today, but their CORRECTNESS as a faithful encoding of the SPEC/GAP behaviors is only proven when Waves 1-4 turn them green; a reviewer/verifier must confirm the encoded expectations match DATA-01..06 before relying on them as the acceptance gate"

# Metrics
duration: 18min
completed: 2026-07-15
status: complete
---

# Phase 39 Plan 01: Data-Ingestion Wave-0 Test Contract Summary

**Nine-file dataset-free Nyquist Wave-0 unittest contract for DATA-01..06: a deterministic read-only TinyCorpus fixture, a self-testing mechanical boundary audit (green today), and deferred executable expectations that Plans 02-06 implement against — no production `pinn/data` code introduced.**

## Performance

- **Duration:** 18 min
- **Started:** 2026-07-15T01:38:30Z
- **Completed:** 2026-07-15T01:56:07Z
- **Tasks:** 3
- **Files modified:** 9 created

## Accomplishments

- Landed the complete `tests/phase39` nine-file scaffold: every DATA-01..06 behavior has a discoverable, dataset-free unittest module before production implementation, including a dedicated sole-classifier suite (base Set 1a vs gold Set 2a).
- Built a deterministic `TinyCorpus` on-disk fixture (read-only, `TemporaryDirectory`-scoped) modeling the README 4->2 Brutus->IC mapping (two IC folders, four Brutus folders, no `_for_gold_standard` IC), sparse IDs, base/gold siblings, optional/misleading footers, valid/invalid blacklist JSON, version metadata, non-finite/malformed snapshots, the HIGH-3 gold-with-base-IC case, and both asymmetric IC/Brutus pairing anomalies (N4). It never writes beneath `simulation_data/`.
- Shipped a mechanical boundary audit that runs green against the current tree AND self-tests every detector (unauthorized reader, v1 import, global-default mutation, denominator floor, footer/metrics energy gate, s0 mutation, numeric-classifier-outside-stages, corpus-write containment) so the gate is demonstrably able to fail on injected violations before production exists.
- Encoded the resolved gaps as frozen contracts: GAP-39-03/08 base-Set-1a-only classifier with `gold_numeric_stage_count == 0`, GAP-39-04 scale-aware near-zero-H0 (no denominator floor), GAP-39-05 whole-trajectory non-finite quarantine with separate drop accounting, GAP-39-06 complete-signature Hamilton split, GAP-39-11 split-only `MISSING_BASE`, GAP-39-10 global `T = 10.0`/no `FixedBatch.T`, GAP-39-12 Option-C collocation quotas, and the DATA-06 239-fatal/240-nonfatal/full>=240-with-low-train-nonfatal boundary.
- Provided the deferred synthetic end-to-end wiring smoke (adapter -> split -> build_stage_batch -> build_population_report on one TinyCorpus, N6) and the single `_SKIP_PHRASE` constant consumed by every `_require` helper for the Wave-5 grep.

## Task Commits

Each task was committed atomically (executed in dependency order 02 -> 01 -> 03):

1. **Task 39-01-02: deterministic tiny corpus + prohibition audit** — `c2e188e` (test) — `__init__.py`, `_fixtures.py`, `test_prohibitions.py`
2. **Task 39-01-01: deferred adapter, type, and classifier contracts** — `26bdd5a` (test) — `test_adapter.py`, `test_stages.py`
3. **Task 39-01-03: DATA-01..06 behavior tests as deferred contracts** — `e9bf9db` (test) — `test_admission.py`, `test_splits.py`, `test_batches.py`, `test_stage_scan.py`

**Plan metadata:** this SUMMARY + STATE.md + ROADMAP.md (docs commit)

## Files Created/Modified

- `tests/phase39/__init__.py` — the sole `_SKIP_PHRASE = "skipped Phase39 production symbol"` definition.
- `tests/phase39/_fixtures.py` — `TinyCorpus` deterministic read-only corpus builder + containment helpers.
- `tests/phase39/test_prohibitions.py` — AST sole-reader/sole-classifier/ban audit, per-detector self-tests, TinyCorpus contract.
- `tests/phase39/test_adapter.py` — shared-type identities/outcomes, GAP-39-07 resident-bytes, deferred adapter residency/version/labels, N6 wiring smoke.
- `tests/phase39/test_stages.py` — pure `classify_stage_label` contract (GAP-39-03/08).
- `tests/phase39/test_admission.py` — seven-clause Step-1A gate, GAP-39-04/05 boundaries.
- `tests/phase39/test_splits.py` — grouped Hamilton split, GAP-39-06/08/11.
- `tests/phase39/test_batches.py` — replay/lookahead selection, GAP-39-10/12.
- `tests/phase39/test_stage_scan.py` — Stage-0 scan + DATA-06 fatal boundary mechanics.

## Decisions Made

- **Execution order 02 -> 01 -> 03.** `test_adapter.py`/`test_stages.py` (task 01) import `_SKIP_PHRASE` from `__init__.py` and use `_fixtures.py` (task 02), so task 02 ran first to keep each task's `<verify>` command runnable in isolation. Every task still committed only its own files.
- **`requirements-completed: []`.** Wave 0 delivers only the executable contract; DATA-01..06 are completed by later waves plus the real-corpus gate. Marking them complete now would be a false traceability claim, so REQUIREMENTS.md is left unchanged.
- **Type vocabulary follows 39-PATTERNS.md** (Variant/Fidelity enums on records; str variant/fidelity on keys; closed StageLabel; MISSING_BASE/MISSING_GOLD as split-only sentinels) — this is the frozen contract Plans 02-06 implement against.
- **Degenerate-Lmax modeled as NaN `l_ratio`** so the classifier returns UNASSIGNED without a bespoke attribute.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Task execution reordered to satisfy module dependencies**
- **Found during:** Task 39-01-01 planning (before edits)
- **Issue:** Task 01's files (`test_adapter.py`, `test_stages.py`) import `_SKIP_PHRASE` from `tests/phase39/__init__.py` and consume `tests/phase39/_fixtures.py`, both owned by Task 02. Running Task 01's `<verify>` command (`python -m unittest tests.phase39.test_adapter tests.phase39.test_stages`) before Task 02 exists would ERROR on import, failing the acceptance gate.
- **Fix:** Executed the tasks in dependency order 02 -> 01 -> 03. File ownership per task is unchanged; each task committed exactly its planned files.
- **Files modified:** none beyond the planned per-task file sets.
- **Verification:** each task's `<verify>` command passed after its commit; full `discover` green (105 collected, OK skipped=80).
- **Committed in:** c2e188e / 26bdd5a / e9bf9db (task commits, unchanged scope).

---

**Total deviations:** 1 auto-fixed (1 blocking — sequencing only).
**Impact on plan:** No scope change; all nine planned files delivered with unchanged per-task ownership. Reordering was a build-order necessity, not a content change.

## Issues Encountered

None. All three per-task `<verify>` commands and the plan-level verification (`discover -s tests/phase39`, `git diff --check`) passed. No `pinn/data` production file was created; the framework specs were not touched.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The nine-file contract is discoverable, dataset-free, and skip-clean; Plans 39-02/39-03 can now implement `pinn/data` production symbols and watch the deferred skips turn green.
- The mechanical boundary audit and TinyCorpus contract already run green and will tighten automatically (sole-reader allowlist, sole-classifier, module superset) as each production file lands.
- The type vocabulary and helper signatures in these tests are the frozen contract; if a later-wave executor needs a different shape, it must reconcile against these expectations (the Wave-0 purpose) rather than silently diverging.

## Self-Check: PASSED

- All nine `tests/phase39/*.py` files exist on disk (verified).
- Task commits `c2e188e`, `26bdd5a`, `e9bf9db` exist in `git log` on `milestone/v2.0` (verified).
- Plan verification re-run: `python -m unittest discover -s tests/phase39 -p 'test_*.py'` => Ran 105, OK (skipped=80); `git diff --check -- pinn/data tests/phase39` clean; `pinn/data` absent (no production introduced).

---
*Phase: 39-data-ingestion-stage-0-population-scan*
*Completed: 2026-07-15*
