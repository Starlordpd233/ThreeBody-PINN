---
phase: 41-config-checkpointing-resume-determinism
plan: 01
subsystem: training-config
tags: [ctrl-01, config-yaml, atomic-io, provisional-seams, training-config, determinism]

requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04
    provides: frozen TrainingConfig dataclasses (run/stage/opt/loss), CheckpointStore Protocol, phase40 fixtures
provides:
  - atomic_io shared write primitive (text + torch)
  - RunConfig precision/device/strict_cpu_determinism/run_name surface
  - ⚖ GuardConfig + CheckpointCadence nested under run
  - keyed YAML load_config + freeze_resolved_config (CTRL-01)
  - tests/phase41 Wave-0 scaffold for 41-02..41-05
affects:
  - 41-02 production CheckpointStore (consumes atomic_io + cadence fields)
  - 41-03 guards + determinism (consumes run.guards + strict_cpu_determinism)
  - 41-04 controllers extension (consumes cadence hooks)
  - 41-05 resume + pinn.train entry (consumes freeze_resolved_config, run_name, identity paths)

tech-stack:
  added: []  # PyYAML already present in pinn-train
  patterns:
    - "tmp.{pid} → flush → fsync(file) → os.replace → fsync(dir) atomic write"
    - "recursive _map_section unknown-key walk with dotted ConfigKeyError paths"
    - "provisional_fields() registry for ⚖ owner-carved seams (value + provenance)"
    - "tuple coercion of YAML lists before dataclass construction (adam_betas)"

key-files:
  created:
    - pinn/training/atomic_io.py
    - pinn/training/config_yaml.py
    - tests/phase41/__init__.py
    - tests/phase41/_fixtures.py
    - tests/phase41/test_prohibitions.py
    - tests/phase41/test_atomic_io.py
    - tests/phase41/test_config_yaml.py
  modified:
    - pinn/training/config.py
    - tests/phase40/test_config.py

key-decisions:
  - "Checkpoint cadence nested under run.checkpoint (not a fifth top-level YAML section) to preserve CTX-50 run/stage/opt/loss surface"
  - "Guard thresholds nested under run.guards matching RESEARCH Pattern 2 identity-payload paths"
  - "frozen_config_rng_recording_format registered as UNDECIDED with candidates A/B — pure TrainingConfig freeze ships; RNG carriage deferred to owner pick"
  - "failure_keep is plain disk-hygiene retention (default 10), NOT a ⚖ owner-carved scientific seam"
  - "RunConfig validates precision/device type only; pair validity stays resolve_runtime (CTX-20)"

patterns-established:
  - "atomic_io: single shared text/torch atomic write for config/checkpoint/guards"
  - "ConfigKeyError sibling of ConfigRequiredError for UNKNOWN keys with full dotted path"
  - "provisional_fields includes Phase-41 ⚖ seams + undecided representation sentinel"
  - "tests/phase41 _SKIP_PHRASE + _require deferred-import SkipTest scaffold"

requirements-completed: [CTRL-01]

coverage:
  - id: D1
    description: Shared atomic_io primitive (atomic_write_text + atomic_write_torch) with crash-before-rename fault injection
    requirement: CTRL-01
    verification:
      - kind: unit
        ref: tests/phase41/test_atomic_io.py
        status: pass
    human_judgment: false
  - id: D2
    description: RunConfig precision/device/strict_cpu/run_name + ⚖ guards/cadence seams registered in provisional_fields including frozen_config_rng_recording_format=UNDECIDED
    requirement: CTRL-01
    verification:
      - kind: unit
        ref: tests/phase41/test_config_yaml.py#RunFieldTests|GuardConfigTests|ProvisionalSeamTests|RunNameValidationTests
        status: pass
    human_judgment: false
  - id: D3
    description: Keyed YAML load_config with recursive ConfigKeyError + freeze_resolved_config re-parse equality
    requirement: CTRL-01
    verification:
      - kind: unit
        ref: tests/phase41/test_config_yaml.py#YamlMappingTests|NestedUnknownKeyTests|FrozenCopyRoundTripTests
        status: pass
    human_judgment: false
  - id: D4
    description: tests/phase41 Wave-0 scaffold (_SKIP_PHRASE, _require, fixtures, prohibition seeds)
    requirement: CTRL-01
    verification:
      - kind: unit
        ref: tests/phase41/test_prohibitions.py
        status: pass
    human_judgment: false

duration: 6min
completed: 2026-07-18
status: complete
---

# Phase 41 Plan 01: Config Foundation Summary

**CTRL-01 library floor: keyed YAML ↔ frozen TrainingConfig with recursive fail-loud keys, atomic frozen copy, shared atomic_io, and ⚖ provisional cadence/guard/RNG-format seams**

## Performance

- **Duration:** ~6 min
- **Started:** 2026-07-18T08:02:09Z
- **Completed:** 2026-07-18T08:08:00Z
- **Tasks:** 3/3 (+ 1 auto-fix deviation commit)
- **Files modified:** 9 (7 created, 2 modified)

## Accomplishments

- Promoted the three-site atomic-write idiom into `pinn/training/atomic_io.py` (`atomic_write_text` + `atomic_write_torch`) with fsync-before-rename and crash-injection tests.
- Extended `TrainingConfig` / `RunConfig` with precision/device/strict_cpu_determinism/run_name, nested `GuardConfig` (R-1 ⚖) and `CheckpointCadence` (D4-a ⚖ wall-clock + operational retention), and registered all provisional seams including `frozen_config_rng_recording_format=UNDECIDED` (candidates A/B enumerated).
- Delivered `config_yaml.py`: `ConfigKeyError`, recursive `_map_section`, `load_config`, `resolved_config_to_dict`, `freeze_resolved_config` via atomic write — CTRL-01 re-parse equality holds (tuple fields preserved).
- Stood up `tests/phase41` Wave-0 scaffold for downstream plans 41-02..41-05.

## Task Commits

Each task was committed atomically:

1. **Task 1: Shared atomic-io primitive + Wave-0 tests/phase41 scaffold** — `a8f35434` (feat)
2. **Task 2: Extend config.py — precision/device/strict-CPU + ⚖ cadence & guard seams** — `b0fc53c2` (feat)
3. **Deviation fix: phase40 config test for new run.precision/device fields** — `ef7bab5a` (fix)
4. **Task 3: config_yaml.py — keyed YAML resolver + fail-loud unknown-key + atomic frozen copy** — `4550d1d2` (feat)

**Plan metadata:** (docs commit after this SUMMARY)

## Files Created/Modified

- `pinn/training/atomic_io.py` — shared atomic text/torch write primitive
- `pinn/training/config.py` — RunConfig extensions, GuardConfig, CheckpointCadence, provisional_fields
- `pinn/training/config_yaml.py` — load_config / freeze_resolved_config / ConfigKeyError
- `tests/phase41/__init__.py` — `_SKIP_PHRASE`
- `tests/phase41/_fixtures.py` — StubClock, StubStepCounter, make_synthetic_stage0_loop
- `tests/phase41/test_prohibitions.py` — `_require` + CTRL-03/T-41-01 scaffolds
- `tests/phase41/test_atomic_io.py` — round-trip + crash-before-rename
- `tests/phase41/test_config_yaml.py` — field surface + YAML mapping + freeze round-trip
- `tests/phase40/test_config.py` — updated boundary test (YAML still banned in config.py; precision/device now on run.*)

## Decisions Made

- Nested checkpoint cadence under `run.checkpoint` and guards under `run.guards` (no fifth top-level YAML section) so CTX-50's run/stage/opt/loss surface is preserved and RESEARCH Pattern 2 identity paths (`config.run.precision` / `config.run.guards` / …) line up for 41-05.
- Shipped pure-TrainingConfig `freeze_resolved_config` only; RNG-in-config representation left as ⚖ `UNDECIDED` with candidates A (sidecar `_runtime_state`) and B (sibling `run_start_rng.pt`) — not silently implemented.
- `failure_keep` default 10 is operational hygiene (like `rolling_keep`), not registered as a ⚖ scientific seam.
- Path-safe `run_name` validation at construction (cycle-2 codex MEDIUM); 41-05 still adds resolved-path defense-in-depth.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Phase 40 test asserted absence of run.precision/device**
- **Found during:** Task 2 verification (phase40 suite after config extension)
- **Issue:** `tests/phase40/test_config.py::test_no_precision_device_yaml` required `hasattr(cfg.run, "precision")` to be false — the Phase 40 boundary that Phase 41 CTRL-01 intentionally lifts.
- **Fix:** Renamed/rewrote the test to keep the YAML-parser ban on `config.py` while asserting precision/device live under `run.*` (not flat on TrainingConfig).
- **Files modified:** `tests/phase40/test_config.py`
- **Verification:** `python -m unittest tests.phase40.test_config` — 15/15 OK
- **Committed in:** `ef7bab5a`

## Threat Flags

None beyond the plan's `<threat_model>` mitigations (T-41-01 safe_load, T-41-02 atomic freeze, T-41-03 fail-closed keys, T-41-04 provisional tagging) — no new network/auth/schema surfaces.

## Known Stubs

None that block CTRL-01. Intentional open representation:

- `frozen_config_rng_recording_format` value=`UNDECIDED` — RNG carriage in frozen config.yaml is owner-carved; freeze path ships pure TrainingConfig only until owner pick (HIGH cross-AI finding, registered not invented).

## Verification

```
<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase41 -p 'test_*.py' -v
# Ran 46 tests — OK
```

Also: `tests.phase40.test_config` 15/15 OK after the boundary-test update.

## Self-Check: PASSED

- [x] `pinn/training/atomic_io.py` exists
- [x] `pinn/training/config_yaml.py` exists
- [x] `tests/phase41/` scaffold complete
- [x] Commits `a8f35434`, `b0fc53c2`, `ef7bab5a`, `4550d1d2` present on `milestone/v2.0`
- [x] phase41 suite green (46 tests)
