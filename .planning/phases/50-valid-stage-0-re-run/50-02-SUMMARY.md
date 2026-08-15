---
phase: 50-valid-stage-0-re-run
plan: 02
subsystem: training-orchestration
tags: [pinn, stage0, smoke, run-ledger, calibration, terminal-closeout, data-06]

requires:
  - phase: 50-valid-stage-0-re-run
    provides: --stage-0-only guard, four Phase-50 configs, pre-registration, empty v2 ledger scaffold
provides:
  - "Band generation 2 bound at git_head 7dd9ad92 with immutable corpus/environment snapshots"
  - "Finished ACC-02 smoke with same-head stage0-timing.json and first real-corpus s_h/eps_h/n_train"
  - "Seed-41 failed at first validation with DATA-06 StageZeroUnderpopulated 227<240"
  - "Terminal forensic closeout and phase50-terminal-manifest/v1 for generation 2"
affects: [50-03-evidence-extraction, 51-authorized-evaluation]

actuals:
  tokens: 180000
  tasks: 3
  commits: 1

tech-stack:
  added: []
  patterns:
    - "D-17 no-commit run window with uncommitted ledger appends until a single closeout commit"
    - "Detached nohup launch; do not wait on pinn.train inside a wrapper timeout"
    - "DATA-06 validation-split underpopulation vs replay_count 240 is terminal, not a replay_count edit"

key-files:
  created:
    - .planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-2.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-2.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-2-smoke-attempt-03-invocation-01.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/verify/generation-2-smoke-attempt-03-invocation-01-marker.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-smoke-attempt-03/
    - .planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-01/
  modified:
    - .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md
    - .planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json
    - .planning/phases/50-valid-stage-0-re-run/50-02-SUMMARY.md

key-decisions:
  - "Generation 1 closed terminal records were not rewritten except artifact_dir/archive_move after a hash-verified leftover move off the canonical smoke path"
  - "Seed-41 DATA-06 failure was not retried and did not authorize lowering replay_count from 240 to the observed 227"
  - "Seeds 42 and 43 were not launched after the intrinsic/unknown validation-batch failure"
  - "RUN-01/RUN-02 checkboxes are not flipped; D-16 remains undischarged because seed 42 never ran"

patterns-established:
  - "A later band generation reuses canonical run names only after leftover dead directories are hash-reconciled and archived"
  - "A missing setsid(1) launcher is a pre-construction setup failure (new attempt), not a resume"

requirements-completed: []

coverage:
  - id: D1
    description: "Band generation 2 opened at git_head 7dd9ad92 with pre-registration ancestry, committed config-set hashes, environment snapshot, and full admitted-corpus digest"
    requirement: RUN-01
    verification:
      - kind: other
        ref: "<home>/miniforge3/bin/conda run -n pinn-train python /tmp/gsd-50-02-gen2/band_ops.py open-generation"
        status: pass
    human_judgment: false
  - id: D2
    description: "ACC-02 calibration smoke finished with valid same-head stage0-timing.json and first real-corpus s_h/eps_h/n_train"
    requirement: RUN-01
    verification:
      - kind: other
        ref: "Task 1 automated SMOKE-OK check"
        status: pass
    human_judgment: false
  - id: D3
    description: "Graded seeds 41, 42, and 43 finished at the smoke git head"
    requirement: RUN-02
    verification: []
    human_judgment: true
    rationale: "Seed 41 failed at step 100 with DATA-06 StageZeroUnderpopulated; seeds 42 and 43 were not launched because that class is terminal"
  - id: D4
    description: "Terminal forensic closeout committed the generation-2 ledger, receipts, transcripts, attempt copies, and terminal manifest"
    verification:
      - kind: other
        ref: "plan 50-02 Task 3 automated ledger check (LEDGER-COMPLETE mode=terminal)"
        status: pass
    human_judgment: false

duration: 19min
completed: 2026-08-13
status: complete
halt_resolved: 2026-08-15
halt_resolved_by: GAP-50-02
halt_continuation: 50-04
---

# Phase 50 Plan 02: No-Commit Stage-0 Run Window Summary

**Opened band generation 2 at `7dd9ad92`, finished the ACC-02 smoke with a same-head calibration, then closed the window terminally after seed 41 raised DATA-06 `StageZeroUnderpopulated` (validation Stage-0 pool 227 < required `replay_count` 240) at the first validation batch.**

## Performance

- **Duration:** 19 min
- **Started:** 2026-08-13T05:28:08Z
- **Completed:** 2026-08-13T05:47:17Z
- **Tasks:** 3 of 3 entered (Task 1 tracer finished; Task 2 stopped after seed 41; Task 3 terminal closeout)
- **Files modified:** phase-local evidence tree + this SUMMARY (runtime surface untouched)

## Accomplishments

- Opened generation 2 at `git_head=7dd9ad929d29a1c1fa70c4f5ec354526b4f02bf4` with pre-registration ancestor `abd5f8d9`, committed config-set sha256 `e6e1fd53…e078`, corpus digest `9fdc39c4…9fdd` (38,017 files, 6,667,358,966 bytes), and environment snapshot `5df13523…2a34`. Generation 1 remains immutable terminal history at `584ffddd`.
- Reconciled leftover `runs/stage0-rerun-smoke` against generation-1 `terminal_artifact_sha256` (12/12 equal) and the committed attempt archive, then moved it to `runs/stage0-rerun-smoke-attempt-01-interrupted-20260813T052918Z` with `hashes_equal: true`. Observed dispositions were not rewritten.
- Finished smoke attempt 3 (`--stage-0-only`, no `--resume`): `disposition=finished`, `preflight_status=passed` including affirmative `invariant_b_window` at `N=500`, `training_metadata` `s_h=22.321729071058996` `eps_h=0.0022321729071058997` `n_train=1812`, calibration `valid=true` `s_per_step=0.13972535059194488` `git_head=7dd9ad92`. D-18 gate input `139.7s` (not an ETA). `pinn.verify` GREEN.
- Smoke attempt 2 was a pre-construction setup failure (`setsid` not present on this host); no run directory; not a resume.
- Seed 41 attempt 1 failed at step 100: `Stage-0 population 227 < required 240`. Preflight had passed; 99 Adam steps were finite; `failure/` empty; D-12 splits `MATCH`. Not a disk/memory transient. Seeds 42 and 43 were not launched.
- Task 3 terminal closeout: generation 2 `status=terminal`, `final_band_generation=null`, forensic copies under `evidence/attempts/`, `terminal-manifest.json` with `observed_mismatch.applicable=false`.

## Task Commits

D-17 override: Tasks 1 and 2 make zero commits. The plan's only commit is this Task 3 closeout.

1. **Task 1: End-to-end calibration smoke** — no commit (live window); SMOKE-OK
2. **Task 2: Graded band** — stopped after seed 41 DATA-06 terminal; 42/43 not launched
3. **Task 3: Terminal forensic closeout + SUMMARY** — this commit

## Files Created/Modified

- `.planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md` — generation 2 plus smoke attempts 2/3 and seed-41 attempt 1
- `.planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-2.json` — immutable admitted-corpus snapshot
- `.planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-2.json` — immutable runtime identity snapshot
- `.planning/phases/50-valid-stage-0-re-run/evidence/calibration/generation-2-smoke-attempt-03-invocation-01.json` — produced smoke calibration
- `.planning/phases/50-valid-stage-0-re-run/evidence/verify/generation-2-smoke-attempt-03-invocation-01-marker.json` — GREEN verify marker
- `.planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/generation-2-*.json` — open/pre/post receipts
- `.planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/` — smoke attempts 2/3, seed 41, and verify
- `.planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-smoke-attempt-03/` — forensic copies
- `.planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-01/` — forensic copies
- `.planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json` — generation-2 fail-closed terminal manifest
- `runs/stage0-rerun-smoke/` and `runs/stage0-rerun-seed41/` — gitignored run artifacts (not committed)

## Decisions Made

- Followed the intrinsic-failure rule rather than the one-retry transient rule: no `--resume`, no `replay_count` edit, no seed 42/43.
- Treated smoke curriculum `HALT` at step 300 as stage-exit after Adam budget exhaustion under `--stage-0-only`, not a guard or invariant-B HALT.
- Recorded smoke validation-gate `TypeError` warnings without using them to change any rule (D-19).
- Did not treat seed-41 `n_train=1812` or the observed 227 as a licence to change DATA-05/DATA-06.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `setsid` missing on this macOS host**
- **Found during:** Task 1 (first detached launch attempt)
- **Issue:** The first generation-2 smoke wrapper used `setsid nohup …`; `setsid` is not present. No training process started and no run directory was created.
- **Fix:** Closed smoke attempt 2 as a pre-construction setup failure (`exit_code=127`) and launched attempt 3 with `nohup` only. No code/config/seed change.
- **Files modified:** phase-local evidence only
- **Verification:** attempt 2 `artifact_dir=null`; attempt 3 reached `disposition=finished`
- **Committed in:** this closeout commit

---

**Total deviations:** 1 environment/launcher fix (0 scientific auto-fixes).
**Impact on plan:** Did not change the experiment. The scientific terminal is the later seed-41 DATA-06 failure.

## Issues Encountered

- Seed 41 raised `StageZeroUnderpopulated: Stage-0 population 227 < required 240` while constructing the first validation batch (`validation_every=100`). The graded configs omit `stage.replay_count`, so it resolves to the DATA-05 default 240. The smoke used `replay_count: 32` and therefore never hit this floor. This is a dataset-vs-recipe first-contact fact, not a transient.
- Smoke validation-gate passes at steps 100/200/300 warned `TypeError` and left `eval01_precondition_iii=false`. Recorded only.
- Global `*.pt` gitignore still prevents committing copied `run_start_rng.pt`; digests remain in `terminal_artifact_sha256`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Generation 2 remains immutable terminal history (`final_band_generation` is null; `--resume` remains forbidden). The designed DATA-06 stop is accepted, not reversed.

**Halt resolution (2026-08-15):** Owner selected GAP-50-02 Option A (full held-out Stage-≤k validation pool; `replay_count` stays 240) and authorized `/gsd-execute-phase 50` to treat this SUMMARY as `complete` so GSD #2830 unblocks dependents. Continuation is **50-04** (conformance repair + generation-3 source identity), then **50-05** (fresh generation-3 run window), then **50-03** (evidence extraction). Do not synthesize a band from generation 2.

## Self-Check: PASSED

Terminal-closeout branch. Task 1 printed `SMOKE-OK gate_input_1000=139.7s`. Task 3 printed `LEDGER-COMPLETE mode=terminal attempts=4 invocations=4`. `BAND-OK` was not printed because seed 41 failed and seeds 42/43 did not launch. Runtime surface stayed clean. `GSD_DATA_ROOT` / `GSD_ALLOW_PARTIAL_DATA_ROOT` were never set. Zero commits occurred between generation-2 open and this closeout.

---
*Phase: 50-valid-stage-0-re-run*
*Completed: 2026-08-13*
