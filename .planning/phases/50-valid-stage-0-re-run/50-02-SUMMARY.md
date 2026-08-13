---
phase: 50-valid-stage-0-re-run
plan: 02
subsystem: training-orchestration
tags: [pinn, stage0, smoke, run-ledger, calibration, terminal-closeout]

requires:
  - phase: 50-valid-stage-0-re-run
    provides: --stage-0-only guard, four Phase-50 configs, pre-registration, empty v2 ledger scaffold
provides:
  - "Band generation 1 bound at git_head 584ffddd with immutable corpus/environment snapshots"
  - "One ledgered smoke attempt (interrupted) with invocation transcript and terminal artifact hashes"
  - "Terminal forensic closeout and phase50-terminal-manifest/v1"
affects: [50-03-evidence-extraction, 51-authorized-evaluation]

actuals:
  tokens: 5951517
  tasks: 2
  commits: 1

tech-stack:
  added: []
  patterns:
    - "D-17 no-commit run window with uncommitted ledger appends until a single closeout commit"
    - "Executor-loss interruption closes terminally; Phase 50 never resumes"

key-files:
  created:
    - .planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-1.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-1.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json
    - .planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-smoke-attempt-01/
    - .planning/phases/50-valid-stage-0-re-run/50-02-SUMMARY.md
  modified:
    - .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md

key-decisions:
  - "The interrupted smoke was not resumed and was not retried: interruption is a terminal Phase-50 class, not a disk/memory transient"
  - "RUN-01/RUN-02 checkboxes are not flipped; D-13/D-14/D-16/D-18 remain undischarged"

patterns-established:
  - "A wrapper-timeout that loses wait() status is recorded as recovered_after_executor_loss with null exit_code rather than an invented zero"

requirements-completed: []

coverage:
  - id: D1
    description: "Band generation 1 opened at one git head with pre-registration ancestry, committed config-set hashes, environment snapshot, and full admitted-corpus digest"
    requirement: RUN-01
    verification:
      - kind: other
        ref: "<home>/miniforge3/bin/conda run -n pinn-train python /tmp/gsd-50-02/band_ops.py open-generation"
        status: pass
    human_judgment: false
  - id: D2
    description: "ACC-02 calibration smoke finished with valid same-head stage0-timing.json"
    requirement: RUN-01
    verification:
      - kind: other
        ref: "runs/stage0-rerun-smoke/summary.json disposition"
        status: fail
    human_judgment: true
    rationale: "Smoke recorded disposition interrupted before any Adam step and wrote no calibration; this is the prescribed terminal path, not a finished tracer"
  - id: D3
    description: "Graded seeds 41, 42, and 43 finished at the smoke git head"
    requirement: RUN-02
    verification: []
    human_judgment: true
    rationale: "Task 2 was not entered because an interruption closes the band terminally"
  - id: D4
    description: "Terminal forensic closeout committed the generation-1 ledger, receipts, transcript, attempt copies, and terminal manifest"
    verification:
      - kind: other
        ref: "plan 50-02 Task 3 automated ledger check (LEDGER-COMPLETE mode=terminal)"
        status: pass
    human_judgment: false

duration: 13min
completed: 2026-08-13
status: halted
---

# Phase 50 Plan 02: No-Commit Stage-0 Run Window Summary

**Opened band generation 1 at `584ffddd`, launched the ACC-02 smoke with `--stage-0-only`, then closed the window terminally after an executor-wrapper timeout interrupted the smoke before any training step or calibration write.**

## Performance

- **Duration:** 13 min
- **Started:** 2026-08-13T05:07:24Z
- **Completed:** 2026-08-13T05:20:00Z
- **Tasks:** 2 of 3 entered (Task 1 tracer + Task 3 terminal closeout; Task 2 not launched)
- **Files modified:** phase-local evidence tree + this SUMMARY (runtime surface untouched)

## Accomplishments

- Bound generation 1 to `git_head=584ffddd8e7e090200b722131aa15907732440cd`, pre-registration ancestor `abd5f8d9`, committed config-set sha256 `e6e1fd53…e078`, corpus digest `9fdc39c4…9fdd` (38,017 files, 6,667,358,966 bytes), and environment snapshot `5df13523…2a34`.
- Archived the stale v2.0 `runs/.calibration/stage0-timing.json` (`git_head ae250c77`, `s_per_step 0.10190`) to a unique hash-verified archive/evidence copy and required the canonical path absent before launch.
- Launched `<home>/miniforge3/bin/conda run -n pinn-train bash scripts/train-unattended.sh --config configs/stage0-rerun-smoke.yaml --stage-0-only`. Real-corpus preflight passed, including the affirmative `invariant_b_window` check at `N=500`. Setup wrote `training_metadata.json` with observed `s_h=22.321729071058996`, `eps_h=0.0022321729071058997`, `n_train=1812`. Those numbers are interrupted-attempt observations, not a finished D-14 record.
- The launch shell was killed by a tool-wrapper timeout. PID 78968 was reparented to launchd, then recorded `disposition=interrupted` / `status.state=interrupted` at 2026-08-13T05:15:11.301739+00:00 with no `stage0-timing.json`, empty `train.log.jsonl`, and no failure bundle. Phase 50 forbids `--resume`; this is not a disk/memory transient, so no fresh retry was authorized.
- Task 3 performed terminal forensic closeout: hashed present D-29 artifacts, copied bounded evidence under `evidence/attempts/stage0-rerun-smoke-attempt-01/`, wrote `evidence/terminal-manifest.json` (`observed_mismatch.applicable=false`), marked generation 1 `terminal`, and left `final_band_generation` null.

## Task Commits

D-17 override: Tasks 1 and 2 make zero commits. The plan's only commit is this Task 3 closeout.

1. **Task 1: End-to-end calibration smoke** — no commit (live window)
2. **Task 2: Graded band** — not started (terminal interruption)
3. **Task 3: Terminal forensic closeout + SUMMARY** — this commit

## Files Created/Modified

- `.planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md` — generation 1 + one interrupted smoke record
- `.planning/phases/50-valid-stage-0-re-run/evidence/corpus/generation-1.json` — immutable admitted-corpus snapshot
- `.planning/phases/50-valid-stage-0-re-run/evidence/environment/generation-1.json` — immutable runtime identity snapshot
- `.planning/phases/50-valid-stage-0-re-run/evidence/calibration/pre-smoke-20260813T051154Z-d931a3fbda20.json` — archived stale v2.0 calibration
- `.planning/phases/50-valid-stage-0-re-run/evidence/cleanliness/` — open and post-interrupt runtime/corpus/environment receipts
- `.planning/phases/50-valid-stage-0-re-run/evidence/launch-transcripts/stage0-rerun-smoke-attempt-01-invocation-01-train.txt` — recovered transcript after wrapper-loss
- `.planning/phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-smoke-attempt-01/` — forensic copies (global `*.pt` ignore blocks committing `run_start_rng.pt`; its sha256 is in the ledger)
- `.planning/phases/50-valid-stage-0-re-run/evidence/terminal-manifest.json` — fail-closed terminal manifest
- `runs/stage0-rerun-smoke/` — gitignored interrupted attempt (preserved on disk, not committed)

## Decisions Made

- Followed the interruption rule rather than the one-retry transient rule: no `--resume`, no second smoke, no seed 41/42/43.
- Did not treat `curriculum.jsonl`'s `HALT` at step 0 as an invariant-B owner checkpoint. There is no failure bundle, `final_guard_disposition` is null, and `summary.json` disposition is `interrupted`.
- Did not treat the setup-time `s_h`/`n_train` pair as D-14/D-16 discharge. Those gates require a finished smoke and a finished seed-42 run.

## Deviations from Plan

### Auto-fixed Issues

None.

### Execution-environment interruption (prescribed terminal path)

**1. [Rule 3 - Blocking] Launch-wrapper timeout lost the smoke process group**
- **Found during:** Task 1 (ACC-02 smoke launch)
- **Issue:** The first `conda run … train-unattended.sh --stage-0-only` invocation was started without a disabled wrapper timeout. The shell was killed; `python -m pinn.train` continued briefly under launchd and then recorded `interrupted`.
- **Fix:** Monitored the live PID instead of launching again; after exit, performed Task 3 terminal closeout. No code, config, threshold, or seed was changed.
- **Files modified:** phase-local evidence only
- **Verification:** `summary.json` disposition `interrupted`; no live `pinn.train`; LEDGER-COMPLETE mode=terminal
- **Committed in:** this closeout commit

---

**Total deviations:** 1 environment interruption handled by the plan's terminal path (0 scientific auto-fixes).
**Impact on plan:** The band did not complete. A later 50-02 re-execution must start a fresh generation from step zero after this closeout commit.

## Issues Encountered

- Tool-wrapper timeout on the smoke launch (self-inflicted interruption). Not a disk/memory transient and not a scientific HALT.
- Global `*.pt` gitignore prevented committing the copied `run_start_rng.pt`; the digest remains in `terminal_artifact_sha256`.
- Observed setup-time `n_train=1812` on the interrupted smoke. Recorded only; not used to change any rule.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Not ready for 50-03 candidate extraction.** `final_band_generation` is null. Plan 50-03 must not synthesize a band/candidate until the owner authorizes a revised continuation. The honest next step is a fresh 50-02 generation at a new head after this evidence commit (50-01 source identities remain valid if no code/config repair is made). `--resume` remains forbidden.

## Self-Check: PASSED

Terminal-closeout branch only. Task 3 automated check printed `LEDGER-COMPLETE mode=terminal attempts=1 invocations=1`. `SMOKE-OK` and `BAND-OK` were not printed because the smoke did not finish and no graded seed launched. Runtime surface stayed clean. `GSD_DATA_ROOT` / `GSD_ALLOW_PARTIAL_DATA_ROOT` were never set. Zero commits occurred between generation open and this closeout.

---
*Phase: 50-valid-stage-0-re-run*
*Completed: 2026-08-13*
