---
phase: 41-config-checkpointing-resume-determinism
plan: 03
subsystem: training-control
tags: [ctrl-07, ctrl-08, guards, determinism, failure-bundle, rng, strict-cpu, provisional-seams]

requires:
  - phase: 41-config-checkpointing-resume-determinism
    provides: run.guards ⚖ thresholds + provisional_fields, atomic_io.atomic_write_text, StageDisposition RECOVER/HALT seam
provides:
  - StepGuards Tier-1+2 auto-guard callback with per-family disposition (LOW-1)
  - write_failure_bundle Tier-A always / Tier-B best-effort disk-floor-safe diagnostic
  - capture_rng_state / restore_rng_state four-stream exact continuation
  - apply_strict_cpu_determinism → RuntimeSpec float64/cpu (HIGH 4)
  - REPRODUCIBILITY_SCOPE honesty string (statistical-equivalence + exact-continuation)
affects:
  - 41-04 controllers per-step guard_hook + RNG in state_dict / checkpoint payload
  - 41-05 pinn.train startup (strict-CPU override before resolve_runtime; run reporting emits scope string)

tech-stack:
  added: []
  patterns:
    - "per-family StageDisposition on GuardOutcome (transient-numeric→RECOVER, resource-exhaustion→HALT)"
    - "first-tripped-wins primary + HALT-wins multi-trip coherent outcome"
    - "Tier-A scalar-only failure/ bundle via atomic_write_text; Tier-B best-effort swallow"
    - "injectable memory_total_bytes + memory_signal for CI/host portability"
    - "restore bit_generator.state exact continuation ≠ default_rng(seed) reseed"
    - "apply_strict_cpu_determinism returns RuntimeSpec via resolve_runtime escape hatch"

key-files:
  created:
    - pinn/training/guards.py
    - pinn/training/determinism.py
    - tests/phase41/test_guards.py
    - tests/phase41/test_determinism.py
  modified: []

key-decisions:
  - "Memory signal = torch.mps.driver_allocated_memory fraction of injectable memory_total_bytes (default 24 GB M5 Pro); MPS-unavailable → SKIPPED-MPS-UNAVAILABLE no-op"
  - "GuardOutcome.disposition is per-family RECOVER/HALT (LOW-1), never uniform RECOVER"
  - "apply_strict_cpu_determinism RETURNS RuntimeSpec so pinn.train can force build_network onto CPU (HIGH 4)"
  - "REPRODUCIBILITY_SCOPE omits the word 'bitwise' while denying bit-identical cross-machine claims"

patterns-established:
  - "StepGuards duck-typed config surface mirrors StageExitMachine threshold injection"
  - "write_failure_bundle owns diagnostic text only; failure .pt checkpoint is store.save_anchor (41-02/41-04)"
  - "RNG capture keys ordered torch/torch_mps/numpy/python_random; numpy is injected Generator only"

requirements-completed: [CTRL-07, CTRL-08]

coverage:
  - id: D1
    description: Tier-1+2 StepGuards with per-family RECOVER/HALT + disk-floor-safe failure/ bundle (CTRL-07)
    requirement: CTRL-07
    verification:
      - kind: unit
        ref: tests/phase41/test_guards.py#NanInfGuardTests|LossExplosionGuardTests|DiskFloorGuardTests|MemoryWatermarkGuardTests|StepZeroAndSimultaneousTests|ThresholdInjectionTests|DiskFloorBackstopTests
        status: pass
    human_judgment: false
  - id: D2
    description: Four-stream RNG exact continuation + strict-CPU RuntimeSpec return + repro honesty string (CTRL-08)
    requirement: CTRL-08
    verification:
      - kind: unit
        ref: tests/phase41/test_determinism.py#RngCaptureRestoreTests|StrictCpuSwitchTests|ReproHonestyTests
        status: pass
    human_judgment: false

duration: 5min
completed: 2026-07-18
status: complete
---

# Phase 41 Plan 03: Guards + Determinism Summary

**Injectable StepGuards (Tier-1+2, per-family RECOVER/HALT, disk-floor-safe failure/) and four-stream RNG exact-continuation + strict-CPU RuntimeSpec return with statistical-equivalence honesty — CTRL-07/08 modules ready for 41-04/41-05 wiring**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-07-18T08:18:22Z
- **Completed:** 2026-07-18T08:22:45Z
- **Tasks:** 2/2
- **Files modified:** 4 (4 created)

## Accomplishments

- Delivered `StepGuards` + `GuardOutcome` with LOW-1 per-family disposition mapping (NaN/Inf + loss-explosion → RECOVER; disk-floor + memory-watermark → HALT), ⚖ thresholds from injected `run.guards`, step-0 + multi-trip HALT-wins coherence, and injectable memory signal/total for CI hosts.
- Delivered `write_failure_bundle` with Tier-A always (README.txt + trip.json scalars via `atomic_write_text`) and Tier-B best-effort (tail.log + checkpoint/config references), so disk-floor trips still leave a diagnostic.
- Delivered `capture_rng_state` / `restore_rng_state` (torch, torch.mps, numpy Generator.bit_generator.state, python random) for exact continuation, proven distinct from reseed; `apply_strict_cpu_determinism` returns float64/cpu `RuntimeSpec`; `REPRODUCIBILITY_SCOPE` honesty string for 41-05 reporting.
- Full `tests/phase41` suite green: 119 tests OK.

## Task Commits

1. **Task 1: guards.py — Tier-1+2 auto-guard + failure/ bundle (CTRL-07)** — `46f83667` (feat)
2. **Task 2: determinism.py — four-stream RNG + strict-CPU + honesty (CTRL-08)** — `7c281dbd` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `pinn/training/guards.py` — `GuardOutcome`, `StepGuards`, `write_failure_bundle`
- `pinn/training/determinism.py` — `capture_rng_state`, `restore_rng_state`, `apply_strict_cpu_determinism`, `REPRODUCIBILITY_SCOPE`
- `tests/phase41/test_guards.py` — per-family + edge + threshold-injection + backstop tests
- `tests/phase41/test_determinism.py` — capture/restore exactness, strict-CPU, honesty wording

## Decisions Made

- Memory watermark reads `torch.mps.driver_allocated_memory()` as a fraction of injectable `memory_total_bytes` (default 24 GB M5 Pro platform value with provenance in trip.json); when the signal returns `None`, the guard records `SKIPPED-MPS-UNAVAILABLE` and does not trip (plan assumptions).
- Simultaneous multi-guard trips produce one coherent `GuardOutcome`; if both RECOVER- and HALT-family guards fire, disposition is HALT (never downgraded).
- Strict-CPU returns `RuntimeSpec` from `resolve_runtime("float64","cpu")` so 41-05 can override production precision/device at build time (HIGH 4).
- Guard thresholds remain ⚖ provisional from config — never presented as owner-ratified.

## Deviations from Plan

None - plan executed exactly as written (implementation choices match plan assumptions block; no Rule 1–4 deviations required).

## Known Stubs

None. Modules are unit-complete injectable surfaces; live per-step wiring is intentionally 41-04/41-05 scope.

## Threat Flags

None beyond plan `<threat_model>` mitigations (T-41-10..13 addressed by guards + honesty tests).

## Self-Check: PASSED

- FOUND: `pinn/training/guards.py`
- FOUND: `pinn/training/determinism.py`
- FOUND: `tests/phase41/test_guards.py`
- FOUND: `tests/phase41/test_determinism.py`
- FOUND: commit `46f83667`
- FOUND: commit `7c281dbd`
- Tests: `tests.phase41.test_guards` + `test_determinism` + full phase41 (119) OK
