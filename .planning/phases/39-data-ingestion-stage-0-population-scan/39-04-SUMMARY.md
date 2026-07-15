---
phase: 39-data-ingestion-stage-0-population-scan
plan: "04"
subsystem: data
tags: [stage-index, physical-key-splits, hamilton-apportionment, canonical-json, atomic-write]

# Dependency graph
requires:
  - phase: 39-03
    provides: "Production AdmittedSetAdapter, immutable PhysicalKey/RecordKey/StageLabel identities, persisted GAP-39-08 stage labels, and zero-gold-numeric invariant"
provides:
  - "Immutable memory-only StageIndex with the canonical StageIndex.from_split(adapter, manifest, split_name) leakage-prevention seam"
  - "Complete-signature physical-group Hamilton partition with explicit MISSING_BASE/MISSING_GOLD metadata and deterministic rare-stratum deviations"
  - "Byte-stable atomic splits.json writer, typed manifest round-trip/validation, seeded train epoch order, and fixed validation/test order"
affects: [39-05, 39-06, 39-07, 40-training-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Materialize an admitted adapter once through its memory-only record_keys/get accessors; consume only persisted StageLabel values"
    - "Group by PhysicalKey before local NumPy RNG; Hamilton-apportion every canonical complete signature independently"
    - "Canonical sorted JSON plus sibling-temp flush/fsync/os.replace and parent-directory fsync"

key-files:
  created:
    - pinn/data/splits.py
  modified:
    - tests/phase39/test_splits.py

key-decisions:
  - "StageIndex.from_split accepts the production adapter directly by materializing record_keys()/get() once, while lightweight sources may expose records(), admitted_records(), or iteration; no independent stage map exists."
  - "The frozen Wave-0 build_split_manifest name is an identity alias to write_split_manifest, preserving old wiring without creating a second partition or serializer implementation; write_split_manifest remains the canonical Plan-06 API and sole exported writer."
  - "Manifest variant values preserve PhysicalKey verbatim (hierarchical/standard); the plan prose's standard_quasi_random spelling is not substituted because that value is rejected by the frozen identity type and would break adapter keys."

patterns-established:
  - "Split-only sentinels serialize as MISSING_BASE/MISSING_GOLD in signature metadata but never enter record StageLabel values or numeric pools."
  - "Typed manifest parsing re-derives physical uniqueness, group signatures, ratios, Hamilton quotas/counts, and deviations before accepting disk content."

requirements-completed: [DATA-04]

coverage:
  - id: D1
    description: "Immutable persisted-label StageIndex and train/validation split restriction over the production adapter"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: "tests/phase39/test_splits.py#StageIndexContract"
        status: pass
      - kind: integration
        ref: "tests/phase39/test_splits.py#ManifestWriterContract.test_production_adapter_is_the_direct_writer_and_from_split_source"
        status: pass
    human_judgment: false
  - id: D2
    description: "Leakage-free complete-signature Hamilton partition with deterministic rare-stratum evidence"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: "tests/phase39/test_splits.py#SignaturePartitionContract"
        status: pass
    human_judgment: false
  - id: D3
    description: "Canonical atomic splits.json persistence, typed round-trip, containment, tamper checks, and deterministic iteration"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: "tests/phase39/test_splits.py#ManifestWriterContract"
        status: pass
      - kind: integration
        ref: "$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v"
        status: pass
    human_judgment: false

# Metrics
duration: 14min
completed: 2026-07-15
status: complete
---

# Phase 39 Plan 04: Deterministic Physical-Group Split Manifest Summary

**A persisted-label `StageIndex` and complete-signature Hamilton allocator now keep every physical base/gold group indivisible, expose a train-only batching seam, and atomically write a byte-stable, typed `splits.json`.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-07-15T10:28:06Z
- **Completed:** 2026-07-15T10:42:02Z
- **Tasks:** 2
- **Files modified:** 2 production/test files (plus this summary and the DATA-04 requirement status)

## Accomplishments

- Built immutable `StageIndex(records)` and `StageIndex.from_split(adapter, manifest, split_name)` over each admitted record's persisted `stage_label`; missing/invalid labels, numeric gold labels, and numeric non-base/non-hierarchical labels hard-fail, while `UNASSIGNED` stays outside numeric pools.
- Implemented group-before-RNG complete signatures `(variant, base_stage_or_MISSING_BASE, gold_UNASSIGNED_or_MISSING_GOLD)` and per-signature 0.8/0.1/0.1 Hamilton largest-remainder allocation with fixed train -> validation -> test ties, canonical local seeded permutation, exact totals, and deterministic deviation records.
- Added the canonical `write_split_manifest(source, run_dir, seed, ratios)` entry point: adapter materialization and partition occur internally; sorted JSON omits paths/timestamps/temp names; sibling-temp flush/fsync/replace is failure-clean; parsing re-validates group/signature/Hamilton invariants; train order is locally seeded while validation/test remain fixed.

## Task Commits

Both tasks followed RED -> GREEN TDD and were committed atomically through `scripts/agent-commit`:

1. **Task 39-04-01 RED: persisted-label StageIndex contract** — `4d6f0bd6` (test)
2. **Task 39-04-01 GREEN: StageIndex and grouped Hamilton partition** — `c472375c` (feat)
3. **Task 39-04-02 RED: canonical manifest writer contract** — `b1a9b395` (test)
4. **Task 39-04-02 GREEN: atomic typed split manifest** — `bd7ebd84` (feat)

**Plan metadata:** this SUMMARY plus `.planning/REQUIREMENTS.md` (docs commit)

## Files Created/Modified

- `pinn/data/splits.py` — immutable StageIndex, adapter-restricted split view, ratios/manifest types, private complete-signature Hamilton partition, typed parser, deterministic iteration helpers, and atomic writer.
- `tests/phase39/test_splits.py` — activated the Wave-0 split contract and added StageIndex, source-seam, exact Hamilton, local-RNG, missing-sentinel, byte-determinism, atomicity, containment, tamper, typed-round-trip, and production-adapter tests.

## Decisions Made

- **Use the production adapter's existing public memory-only surface.** Plan prose described `.records()`/iteration, but Plan 39-03's delivered adapter exposes `record_keys()` plus `get()`. The source materializer calls that pair once, preserving the canonical `StageIndex.from_split(adapter, manifest, "train")` signature without changing adapter ownership.
- **Preserve one canonical writer while keeping frozen wiring live.** `build_split_manifest` is the same function object as `write_split_manifest` and is excluded from `__all__`; this activates the existing Wave-0 end-to-end contract without creating a divergent serializer or public partition helper.
- **Preserve structural variant identity verbatim.** `PhysicalKey` and the adapter use `"standard"`; the allocator does not rewrite it to the plan prose's `"standard_quasi_random"`, which the frozen type rejects.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking interface mismatch] Materialized the actual adapter through `record_keys()` / `get()`**
- **Found during:** Task 39-04-01
- **Issue:** The plan's explanatory source protocol named `.records()`/iteration, but the required Plan-39-03 `AdmittedSetAdapter` exposes only `record_keys()` and `get()` for complete in-memory enumeration.
- **Fix:** Added one-shot materialization through the adapter's existing public accessors, after checking `.records()` / `.admitted_records()` and before generic iteration. The public call remains `StageIndex.from_split(adapter, manifest, split_name)`.
- **Files modified:** `pinn/data/splits.py`, `tests/phase39/test_splits.py`
- **Verification:** `test_from_split_materializes_adapter_once_and_excludes_other_splits`; direct TinyCorpus production-adapter writer/from-split integration test.
- **Committed in:** `c472375c`, `bd7ebd84`

**2. [Rule 3 - Blocking frozen-contract compatibility] Kept `build_split_manifest` as an identity alias**
- **Found during:** Task 39-04-02
- **Issue:** The Wave-0 `test_splits.py` and deferred cross-module wiring test require `build_split_manifest`, while the final plan standardizes `write_split_manifest` as the sole canonical signature.
- **Fix:** Bound `build_split_manifest = write_split_manifest`; the two names are the same function object/signature and share the one private `_partition_by_signature` implementation. Only `write_split_manifest` is listed in `__all__` and quoted by Plan 06.
- **Files modified:** `pinn/data/splits.py`, `tests/phase39/test_splits.py`
- **Verification:** `test_writer_is_single_canonical_signature_and_materializes_once` asserts object identity and the exact four-parameter signature; all prior Wave-0 tests activate and pass.
- **Committed in:** `bd7ebd84`

**3. [Rule 1 - Plan nomenclature bug] Preserved the canonical `PhysicalKey` standard variant**
- **Found during:** Task 39-04-01 signature construction
- **Issue:** The plan prose calls the second variant `standard_quasi_random` while the required frozen `PhysicalKey` validator and production adapter use `standard` (the latter is the actual structural key value).
- **Fix:** Signature and manifest variant fields are copied verbatim from `RecordKey`/`PhysicalKey`; no lossy identity translation is introduced.
- **Files modified:** `pinn/data/splits.py`, `tests/phase39/test_splits.py`
- **Verification:** Direct production-adapter integration includes standard records and round-trips their canonical keys without validation failure.
- **Committed in:** `c472375c`, `bd7ebd84`

---

**Total deviations:** 3 auto-fixed (2 blocking cross-plan interface compatibilities, 1 plan nomenclature bug). **Impact:** all fixes preserve the already-frozen Phase-39 contracts and the plan's canonical public APIs; no scope expansion or new dependency.

## Issues Encountered

None. The initial macOS `/var` -> `/private/var` resolution difference was handled by preserving the caller-visible `manifest.path` spelling while using resolved paths for containment and writes.

## Known Stubs

None. No placeholder values, TODO/FIXME markers, or unwired data sources exist in the files created/modified by this plan.

## User Setup Required

None. The writer receives a caller-owned run directory; real-corpus execution remains Plan 39-07's responsibility.

## Next Phase Readiness

- Plan 39-05 can pass `StageIndex.from_split(adapter, manifest, "train")` directly to its batch constructor and receive only train-assigned base Set-1a numeric keys with `gold_numeric_stage_count == 0`.
- Plan 39-06 can call `write_split_manifest(adapter, run_dir=run_dir, seed=seed, ratios=ratios)` verbatim and derive its diagnostic train count from the returned typed manifest.
- DATA-05 and DATA-06 remain pending; no Plan-39-05/06/07 artifact or source file was touched.

## Self-Check: PASSED

- `pinn/data/splits.py`, `tests/phase39/test_splits.py`, and this SUMMARY exist on disk.
- TDD commits `4d6f0bd6`, `c472375c`, `b1a9b395`, and `bd7ebd84` exist in `milestone/v2.0` history.
- Focused split suite: 30 tests, 0 failures, 0 skips.
- Full Phase-39 discovery: 195 tests, 0 failures, 18 intentional future Plan-39-05/06 skips.
- DATA-04 is complete in both REQUIREMENTS checklist and traceability table; DATA-05/06 remain pending.
- Coverage classifier: 3/3 deliverables auto-covered, no schema errors.
- `git diff --check` passes; no stubs or unexpected deletions were found.

---
*Phase: 39-data-ingestion-stage-0-population-scan*
*Completed: 2026-07-15*
