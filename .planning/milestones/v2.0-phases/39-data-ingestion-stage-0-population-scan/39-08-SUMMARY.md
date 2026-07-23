---
status: active
purpose: implementation-plan
created: '2026-07-15'
milestone: v2.0
phase: 39-data-ingestion-stage-0-population-scan
retirement_trigger: Phase 39 closes and the summary is consumed by verify-work.
execution_status: executed
executed_at: '2026-07-15T22:16:00'
review_status: passed
---

# Plan 39-08 Summary: Preserve selected-slot multiplicity in collocation batches

## Objective

Close the DATA-05 multiplicity gap by preserving replacement-padded selected slots through GAP-39-12 collocation allocation.

## Changes

### `pinn/data/batches.py`

`sample_collocation_points` now treats the sorted selected-slot multiset (`record_keys`, length M=256) as the canonical identity set rather than deduplicating to unique keys. It calls `allocate_collocation_quota(len(record_keys), collocation_count, rng)` to produce one near-even per-slot quota, so a RecordKey occupying k selected slots accumulates k per-slot quotas. The total is always exactly `collocation_count` (4096), regardless of key repetition. Per-slot inline validation (RecordKey type, hierarchical/base, blacklist) replaces the removed `set(record_keys)` dedup.

### `tests/phase39/test_batches.py`

Added two integrated `build_stage_batch` regressions:

- `test_pool_size_one_lookahead_key_receives_all_256_collocation_rows`: Stage-1 pool size 1 — one replacement-padded lookahead slot (16 entries, one unique key) receives 256 aggregate collocation rows; 240 replay slots receive 3840.
- `test_pool_size_fifteen_preserves_per_key_occurrence_multiplicity`: Stage-1 pool size 15 — each key's emitted collocation count equals 16 × its occurrence count in `replay_keys + lookahead_keys`.

## Verification

```
$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v
```

29 tests, 0 failures.

## Notes

- A test bug was fixed: the pool-size-1 lookahead assertion summed `collocation_owners[key]` over the 16-entry replacement-padded multiset (all one key), yielding 4096 instead of 256. Fixed to sum over `set(batch.lookahead_keys)`.
