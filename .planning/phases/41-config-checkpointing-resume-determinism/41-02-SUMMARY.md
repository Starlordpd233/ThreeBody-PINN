---
phase: 41-config-checkpointing-resume-determinism
plan: 02
subsystem: training-checkpoint
tags: [ctrl-02, ctrl-03, ctrl-04, checkpoint-store, atomic-io, fallback-scan, retention, curriculum-ledger, weights-only]

requires:
  - phase: 41-config-checkpointing-resume-determinism
    provides: atomic_io.atomic_write_torch, CheckpointCadence (every_n_steps/wall_clock_ceiling_s/rolling_keep/failure_keep), tests/phase41 scaffold
provides:
  - production TorchSaveCheckpointStore (name preserved) behind CTX-43 Protocol
  - CHECKPOINT_SCHEMA_VERSION single source of truth
  - NoValidCheckpointError / PromotionRefused typed errors
  - save_rolling / save_best / save_anchor committed save-class surface
  - should_checkpoint dual-trigger with last_written_time reset
  - fallback_scan + load_checkpoint exact-path load
  - curriculum.jsonl idempotent disposition ledger + ordered promote
affects:
  - 41-04 controllers extension (build_checkpoint_payload imports CHECKPOINT_SCHEMA_VERSION; wires save_rolling/save_best/save_anchor/record_disposition/promote)
  - 41-05 resume + pinn.train (--resume exact-file via load_checkpoint; load_latest/fallback_scan)

tech-stack:
  added: []
  patterns:
    - "atomic_write_torch for every .pt write (tmp+fsync+os.replace+dir-fsync)"
    - "weights_only=True at every torch.load site (inspect.getsource count equality)"
    - "CTX-53 structural validity = required-key PRESENCE not truthiness"
    - "dual-trigger should_checkpoint with last_written_step + last_written_time reset"
    - "failure-* distinct retention class excluded from fallback_scan and latest.pt"
    - "curriculum.jsonl idempotent 4-tuple append (single write+fsync)"

key-files:
  created:
    - tests/phase41/test_checkpoint.py
  modified:
    - pinn/training/checkpoint.py

key-decisions:
  - "TorchSaveCheckpointStore class NAME preserved as production body so phase-40 imports stay green"
  - "EmptyCheckpointStore remains RuntimeError and is also constructible as no-op store (HIGH 5)"
  - "curriculum.jsonl at root.parent when root.name==checkpoints else root/curriculum.jsonl"
  - "terminal_stage default 2 (Adam-only slice) for promote beyond-terminal refusal"
  - "Compatibility _ids list retained for phase-40 cold-start RECOVER introspection"

patterns-established:
  - "CHECKPOINT_SCHEMA_VERSION owned by checkpoint.py; controllers import, never redefine"
  - "save_rolling refreshes latest; save_best does not; stage-*-init does; failure-* does not"
  - "load_checkpoint exact-path with path.resolve().is_relative_to(store root)"

requirements-completed: [CTRL-02, CTRL-03, CTRL-04]

coverage:
  - id: D1
    description: Atomic weights_only-clean writes + fallback_scan + load_checkpoint (CTRL-03)
    requirement: CTRL-03
    verification:
      - kind: unit
        ref: tests/phase41/test_checkpoint.py#AtomicityTests|FallbackScanTests|LoadCheckpointTests|WeightsOnlyProhibitionTests|RoundTripTests
        status: pass
    human_judgment: false
  - id: D2
    description: Dual-trigger cadence + rolling/best/latest/failure retention (CTRL-02)
    requirement: CTRL-02
    verification:
      - kind: unit
        ref: tests/phase41/test_checkpoint.py#DualTriggerTests|RetentionTests|FailureRetentionTests
        status: pass
    human_judgment: false
  - id: D3
    description: Stage anchors + ordered promote + curriculum.jsonl ledger (CTRL-04 store half)
    requirement: CTRL-04
    verification:
      - kind: unit
        ref: tests/phase41/test_checkpoint.py#AnchorTests|PromotionLedgerTests
        status: pass
    human_judgment: false

duration: 5min
completed: 2026-07-18
status: complete
---

# Phase 41 Plan 02: Production CheckpointStore Summary

**Production CheckpointStore delivers atomic weights_only-clean writes, dual-trigger rolling/best/anchor retention, fallback scan, exact-path load_checkpoint, and an idempotent curriculum.jsonl promotion ledger behind the preserved CTX-43 Protocol**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-07-18T08:10:07Z
- **Completed:** 2026-07-18T08:15:31Z
- **Tasks:** 3/3
- **Files modified:** 2 (1 created, 1 rewritten)

## Accomplishments

- Replaced naive `TorchSaveCheckpointStore` internals with production CTRL-02/03/04 store half while keeping the class name and `CheckpointStore` Protocol so phase-40 imports and 163/163 regression stay green.
- Defined `CHECKPOINT_SCHEMA_VERSION = 1` as the single source of truth; fallback_scan and load_checkpoint validate CTX-53 required-key presence (not truthiness) plus matching schema; `failure-*` excluded from auto-resume (LOW-2).
- Dual-trigger `should_checkpoint(step, elapsed)` with `last_written_step` + `last_written_time` reset (elapsed = time-since-last-write); injectable `time.monotonic` clock; `save_rolling` / `save_best` / `save_anchor` committed surface; rolling_keep + failure_keep retention.
- Idempotent `save_anchor`, ordered `promote` (skip/regress/beyond-terminal → `PromotionRefused`), and `record_disposition` → `curriculum.jsonl` 4-tuple ledger; EmptyCheckpointStore no-op surface for 41-04 unconditional calls.

## Task Commits

Each task was committed atomically:

1. **Tasks 1–3: Production CheckpointStore (CTRL-02/03/04 store half)** — `3d080663` (feat)
   - Task 1 (CTRL-03 atomic + weights_only + fallback + load_checkpoint)
   - Task 2 (CTRL-02 dual-trigger + rolling/best/failure retention)
   - Task 3 (CTRL-04 anchors + promote + curriculum.jsonl)
   - Landed as one feat commit because all three tasks rewrite the same two files with tightly coupled surface.

**Plan metadata:** (docs commit after this SUMMARY)

## Files Created/Modified

- `pinn/training/checkpoint.py` — production store: Protocol preserved; `TorchSaveCheckpointStore` production body; `CHECKPOINT_SCHEMA_VERSION`; `NoValidCheckpointError`; `PromotionRefused`; EmptyCheckpointStore no-op methods; full save-class + cadence + retention + ledger surface
- `tests/phase41/test_checkpoint.py` — ProtocolShape, RoundTrip, Atomicity, FallbackScan, LoadCheckpoint, WeightsOnly, DualTrigger, Retention, FailureRetention, Anchor, PromotionLedger tests

## Decisions Made

- Keep `TorchSaveCheckpointStore` as the production class name (alias-free) so phase-40 `from pinn.training.checkpoint import TorchSaveCheckpointStore` needs no change.
- `EmptyCheckpointStore` remains a `RuntimeError` subclass *and* is constructible as a no-op store (HIGH 5) — `load_checkpoint` raises `NoValidCheckpointError` naming the path.
- Ledger path: `root.parent / curriculum.jsonl` when `root.name == "checkpoints"`, else `root / curriculum.jsonl` (test-friendly).
- Default `terminal_stage=2` (Adam-only slice) for promote beyond-terminal, injectable for tests.
- Retained `_ids` append-only list on Protocol `save()` for phase-40 cold-start RECOVER test introspection (Rule 1 / Rule 3 compatibility).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Phase-40 cold-start RECOVER test introspected `_ids`**
- **Found during:** Task 1 verification (full phase40 suite)
- **Issue:** `tests/phase40/test_controllers.py::ColdStartRecoverTests` asserts `store._ids == []` on a genuinely empty store; production rewrite dropped the naive index attribute → AttributeError, 162/163.
- **Fix:** Keep a minimal append-only `self._ids` list updated only by Protocol `save()` (not used for latest/fallback resolution).
- **Files modified:** `pinn/training/checkpoint.py`
- **Verification:** phase40 suite 163/163 green
- **Committed in:** `3d080663`

**2. [Rule 3 - Blocking] weights_only count inflated by class docstring**
- **Found during:** Task 1 WeightsOnlyProhibitionTests
- **Issue:** Class docstring mentioned ``weights_only=True`` so `inspect.getsource(cls).count` saw 4 vs 3 torch.load sites.
- **Fix:** Rephrase docstring to avoid the literal token (prohibition test counts class source, not AST-stripped module source).
- **Files modified:** `pinn/training/checkpoint.py`
- **Committed in:** `3d080663`

## Auth Gates

None.

## Known Stubs

None — store methods are fully implemented; payload *composition* remains owned by 41-04's `build_checkpoint_payload` (store receives payloads verbatim by design).

## Threat Flags

None beyond plan threat model T-41-05..T-41-09 (all mitigated in-plan: weights_only, atomic writes, structural fallback, retention bounds, failure exclusion, provisional ceiling from config).

## Validation

```
<home>/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_checkpoint tests.phase41.test_prohibitions -v
# 53 tests OK

<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase41 -p 'test_*.py' -q
# 94 tests OK

<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase40 -p 'test_*.py' -q
# 163 tests OK
```

## Self-Check: PASSED

- FOUND: `pinn/training/checkpoint.py`
- FOUND: `tests/phase41/test_checkpoint.py`
- FOUND: commit `3d080663`
- FOUND: `CHECKPOINT_SCHEMA_VERSION`, `NoValidCheckpointError`, `save_rolling`, `save_best`, `save_anchor`, `should_checkpoint`, `fallback_scan`, `load_checkpoint`, `record_disposition`, `promote`
