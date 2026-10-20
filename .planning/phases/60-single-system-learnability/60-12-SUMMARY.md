---
phase: 60-single-system-learnability
plan: 12
subsystem: verification
tags: [learnability-harness, command-line, launch-lock, governed-stop, exact-resume, signal-handlers, tdd]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-10's admit_arm contract, load_protocol and drift pins; Plan 60-11's run_arm with physics arms, the CPU float64 cross-check, counting and the validated real-arm record; Plan 60-08's timing run, budget driver, ratified schedule, clipper and owner-stop writer; Plan 60-23's EXIT_* constants"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard the budget, polish, cadence and tier rules come from"

provides:
  - "pinn/verification/learnability_run.py: main(argv), request_stop, stop_requested, install_stop_handlers, GovernedStop, _StopRequested, ResumeRefused, ClaimExists, save_resume_checkpoint, load_resume_checkpoint, _resume_payload, run_arm(..., resume=False, run_dir=None), timing_run(stop_fn=) and drive_adam(stop_fn=, resume_state=); record blocks launch {invocations, stops} and timing_runs; checkpoint schema phase60-resume/v1"
  - "tests/phase60/test_resume.py (25 tests) and tests/phase60/test_cli.py (24 tests)"

affects: [60-13, 60-14, 60-15, 60-16, 60-17, 60-18, 60-19, 60-20, 60-21, 60-22]

actuals:
  tokens: 23013
  tasks: 2
  commits: 1
  plan_head_before: a10351b628f81d13c3afc82e4329dcbb5a22d391

tech-stack:
  added: []
  patterns:
    - "A signal handler only sets a flag and an exit code; the runner checkpoints at its next safe boundary and raises a BaseException the run cannot swallow"
    - "One checkpoint format for every arm: tensors, numbers, strings, lists and dicts only, so torch.load(weights_only=True) is the only loader"
    - "Opt-in continuation: the checkpoint records the driver state, so the budget driver resumes at a step boundary instead of being restarted"
    - "The aborted L-BFGS call is not part of the polish: parameters and a pre-call L-BFGS state dict are restored, and its wall time is never counted"
    - "Every stop keeps its own marker and its own launch.stops entry, so the exit history is auditable from the record alone"

key-files:
  created:
    - tests/phase60/test_resume.py
    - tests/phase60/test_cli.py
  modified:
    - pinn/verification/learnability_run.py
    - tests/phase60/test_budget_driver.py

key-decisions:
  - "The run tree of a direct run_arm call defaults to <evidence-root>/runs/phase60/<arm-id>; the command line passes the plan's canonical runs/phase60/<arm-id> explicitly, so a fixture or a test writes nothing into the repository"
  - "The first governed signal wins: request_stop records the signal and its code once and later signals do not change it, because a checkpoint written under one exit code must not be resumed under another"
  - "The Adam-to-polish boundary is an Adam boundary: a stop there checkpoints adam_complete=True, so the resume goes straight to the handoff and no scored state is repeated"
  - "ClaimExists is a distinct exception from FirstResultExists: a claim means an earlier invocation owns the run tree, not that the arm has a result"
  - "timing_run returns None when a stop interrupts it, because its three-key return mapping is pinned by existing tests; timing_runs counts attempts, so an interrupted timing run plus its repeat records 2"
  - "A polish checkpoint must also carry its L-BFGS state_dict, and a resume also refuses a changed first_omega_0: both would be unrestorable, and the plan names only the segment and the digests"
  - "The available-memory figure is logged in process.json and may be null: it is advisory and never gates a launch"
  - "Every arm now carries an arm np.random.default_rng(SEED), not only a physics arm, so one checkpoint format holds all four RNG streams and exact continuation is one code path"

patterns-established:
  - "Checkpoint the state, not the decision: a resume re-enters the budget driver's own loop, so the extension decision at B is made once, by the same frozen function"
  - "Refuse before reading: a checkpoint is vetted (schema, arm, protocol, module digests, phase, segment, L-BFGS state) before a record or a corpus file is touched"

requirements-completed: [INST-05, FEAS-03]

coverage:
  - id: D1
    description: "The command line accepts exactly one catalog arm id plus --resume or --admit-only; an unknown id, a path, a fixture id or any runtime/precision flag exits 2 before the corpus is opened, and --admit-only prints ADMIT-OK/ADMIT-REFUSED and creates nothing"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_cli.py#ArgvTests, AdmitOnlyTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "A run writes runs/phase60/<arm-id>/process.json with its own PID before run_arm, takes the Phase 60 one-launch lock, releases it on every path, and a second concurrent main prints LAUNCH-REFUSED and exits 2"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_cli.py#LifecycleTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "OwnerRouted and CrossCheckDisagreement print OWNER-ROUTED and exit 3 with exactly one run_arm call; GovernedStop exits 129, 130 or 143; an unexpected RuntimeError and a HarnessHalt propagate"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_cli.py#ExitMappingTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Real SIGHUP, SIGINT and SIGTERM to a running arm exit 129, 130 and 143 with resume.pt, one stop-<n>.json and no abandoned .tmp file; SIGKILL leaves no stop marker and the resume is refused"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#SignalSubprocessTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "An arm stopped at Adam step 5 and resumed matches the uninterrupted run field for field (readings, trace E, budget outcome, both weights digests), the budget is not re-timed, the timing run is not repeated, and the summed Adam wall seconds equal the uninterrupted run"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#ExactContinuationTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "A stop exactly at step B resumes into the same extension decision, and the concatenated learning-rate trace of the two segments equals the uninterrupted two-cosine trace"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#ExtensionResumeTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "A stop during the second polish outer call restores the parameters from before that call, checkpoints the pre-call L-BFGS state, the segment rows, w_n, bin counts and frozen weights at 143, and the resume finishes with identical polish weights, outer-call count and trace; the aborted call adds no polish wall time"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#PolishResumeTests"
        status: pass
    human_judgment: false
  - id: D8
    description: "A physics arm stopped at an Adam step resumes with the restored numpy Generator and draws exactly the collocation rows of the uninterrupted run for the remaining steps"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#PhysicsResumeTests"
        status: pass
    human_judgment: false
  - id: D9
    description: "A resume is refused when the checkpoint or a stop marker is missing, for another arm id, a changed protocol SHA-256 or pinned module digest, or a polish checkpoint without its segment state, in the trainer's wording; a fresh run over a claimed tree is refused"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#ResumeRefusalTests"
        status: pass
    human_judgment: false
  - id: D10
    description: "A stop during the timing run leaves no timing record, and the resume repeats the timing run and records timing_runs 2 with two launch invocations"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_resume.py#TimingInterruptTests"
        status: pass
    human_judgment: false
  - id: D11
    description: "Readings of the plan text that its sources leave open (listed under Decisions Made): the per-evidence-root default run tree, the first-signal-wins rule, the Adam-to-polish boundary checkpoint, ClaimExists, timing_run returning None, the extra L-BFGS and first_omega_0 refusals, the nullable memory field and the data-only arm's generator"
    verification: []
    human_judgment: true
    rationale: "Each fails closed and moves no locked value, but together they fix the shapes Plan 60-13 seals into the protocol and its verifier reads, so the owner or verifier should confirm them before the protocol is written"

duration: 50min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 12: The arm command line, the one-launch lock and exact resume Summary

**A real arm now starts only through admission, holds the one-launch lock, records its own PID, stops cleanly on SIGHUP, SIGINT or SIGTERM at an Adam boundary or between polish outer calls, and resumes exactly where it stopped - including inside the L-BFGS polish - while anything that cannot be restored is refused and goes to the owner.**

In plain language: a three-to-seven-hour experiment can now be paused when the owner needs the machine or the laptop lid closes, and it picks up from the same numbers rather than starting over; a run that ended badly is never silently restarted.

## Performance

- **Duration:** about 50 min of wall clock (context loading and implementation first, then the retained verification logs from 17:39Z; the full discovery took 13 of those minutes and the RED evidence 1).
- **Tasks:** 2 (Task 1 a tracer, Task 2 test-first).
- **Files:** 2 created (`test_resume.py` 773 lines, `test_cli.py` 345 lines) and 2 modified (`learnability_run.py` +1,081 net lines, and one existing test rewritten where this plan supersedes its premise).

## Accomplishments

- **The command line (Task 2).** `python -B -m pinn.verification.learnability_run <arm-id> [--resume | --admit-only]` parses only a catalog arm id and the two mutually exclusive flags; any runtime, precision, seed or path argument is a usage refusal (exit 2) before admission. `admit_arm` runs before anything else and prints `ADMIT-OK <id>` or `ADMIT-REFUSED: <reason>`; `--admit-only` returns there, opens no corpus and creates no run tree.
- **One launch at a time (SCOPE-44).** A run writes `runs/phase60/<arm-id>/process.json` with `os.getpid()`, the UTC start, the arm id, the resume flag and the advisory free-memory figure *before* `run_arm`, takes `evidence_io.begin_long_step("phase60", arm_id, ...)` under the Phase 60 evidence root, and releases it in a `finally` on every path. A second concurrent invocation prints the lock's own `LAUNCH-REFUSED` line and exits 2 without opening the corpus.
- **The governed exits (SPEC Requirement 8).** One top-level handler maps `OwnerRouted` and `CrossCheckDisagreement` to `OWNER-ROUTED: <message>` with exit 3, exactly once and with no retry, and `GovernedStop` to its 129, 130 or 143. An unexpected `RuntimeError` or `HarnessHalt` propagates as a non-governed failure. The codes are 0 (ok), 2 (refused), 3 (owner-routed), 129 (SIGHUP), 130 (SIGINT), 143 (SIGTERM).
- **The stop (Task 1).** `request_stop(signum)` only sets a flag and a code; `install_stop_handlers()` installs SIGHUP, SIGINT and SIGTERM in the runner (`pinn/training/signals.py` is not edited). `run_arm` checkpoints at an Adam step boundary (through a `stop_fn` the budget driver consults), at the Adam-to-polish boundary, and between polish outer calls, where the closure raises `_StopRequested(BaseException)` so a long outer call aborts at its next evaluation; the parameters are restored from before that call and the pre-call L-BFGS `state_dict` is checkpointed. Each stop writes `stop-<n>.json` with `write_record_exclusive` and appends `{signal, exit_code, phase, step}` to `launch.stops`, so every stop is kept.
- **The checkpoint.** `phase60-resume/v1` in `resume.pt` via `atomic_write_torch`, holding the model (CPU state dict), Adam, the scheduler and its cosine index, `ScheduledWeights`, `GradClipper`, the four RNG streams from `determinism.capture_rng_state`, the readings, trace and monitor log, B, the extension flag, the summed Adam and polish wall seconds, the timing record, the frozen monitor rows, the frozen handoff segment, the L-BFGS state during the polish, the polish counters, the Adam state's scores, and the protocol SHA-256 with the pinned module digests. Tensors, numbers, strings, lists and dicts only; the two `torch.load` calls in the module pass the literal `weights_only=True`.
- **The resume.** `run_arm(..., resume=True)` restores every component after the objects are rebuilt (optimizer and scheduler state, `last_epoch` and the cosine index, the schedule and clipper windows, the numpy Generator by assigning `bit_generator.state`, the torch CPU and MPS streams), continues the budget driver from its saved step and readings (so the extension decision at B is made once, by the frozen function), never re-runs the timing run unless the stop came during it (the record then says `timing_runs` 2), never re-times B, and adds each segment's time to the summed Adam and polish wall seconds.
- **The refusals.** `ResumeRefused` covers a missing checkpoint or stop marker, another arm id, a changed protocol SHA-256, a changed pinned module digest, an unknown phase, and a polish checkpoint without its segment state - in the trainer's words, `resume checkpoint is missing active L-BFGS segment state; refusing to redraw samples or causal weights` (mirroring `controllers.py` lines 845-850 and 2213-2218). `ClaimExists` refuses a fresh start over an owned run tree.

## Task Commits

1. **Tasks 1-2, the plan-named commit: the command line, the stop and the resume with both test modules** - `2da19abe` (feat, subject `add the arm command line and exact resume`; its body names SPEC Requirement 8, SCOPE-44 and the six governed exit codes)
2. **Plan metadata:** the SUMMARY commit that follows this file (docs).

The plan asks for one code commit after both tasks, and that is what this plan has: no RED/GREEN split was committed (see TDD Gate Compliance for the retained RED evidence).

## Files Created/Modified

- `pinn/verification/learnability_run.py` - the stop flag, `request_stop`, `stop_requested`, `install_stop_handlers`, `GovernedStop`, `_StopRequested`, `ResumeRefused`, `ClaimExists`, the claim/checkpoint/marker helpers, `save_resume_checkpoint`, `load_resume_checkpoint`, `_pin_facts`, the resume branches of `run_arm`, `stop_fn` in `timing_run` and `drive_adam` with `resume_state`, the dict-returning `_polish` with `resume` and `stop_fn`, the `launch` and `timing_runs` record blocks, and `main(argv)` with `_parse_argv`, `_write_process` and `_available_memory`.
- `tests/phase60/test_resume.py` - `ExactContinuationTests`, `ExtensionResumeTests`, `PolishResumeTests`, `PhysicsResumeTests`, `ResumeRefusalTests`, `TimingInterruptTests` and `SignalSubprocessTests`, with a counter clock and stepper hooks.
- `tests/phase60/test_cli.py` - `ArgvTests`, `AdmitOnlyTests`, `LifecycleTests` and `ExitMappingTests`, all against a temporary repository root.
- `tests/phase60/test_budget_driver.py` - the Plan 60-11 owner-stop handler test now names the third handler (`main`, the top-level mapper) and keeps the re-raise rule for the two that write a stop.

## Decisions Made

Readings of the plan text that its sources leave open. Each fails closed and none moves a locked value; they are listed for the owner or verifier because Plan 60-13 seals the protocol around them (coverage item D11).

1. **The default run tree belongs to the evidence root.** The plan names `runs/phase60/<arm-id>`. The command line passes exactly that. `run_arm` called directly (tests, and any future in-process driver) defaults to `<evidence-root>/runs/phase60/<arm-id>`, so a fixture arm never writes into the checkout; two existing test modules reused one fixture arm id under separate temporary roots and would otherwise share a claim.
2. **The first governed signal wins.** A handler records the signal and its code once; a later signal does not change them, because a checkpoint written under one exit code must not be resumed under another. `pinn/training/signals.py` is not edited and its second-SIGINT escalation does not apply here.
3. **The Adam-to-polish boundary is an Adam boundary.** A stop requested between the Adam cross-check and the handoff writes a checkpoint with `adam_complete=True`, so the resume goes straight to the handoff and no scored state is repeated.
4. **`ClaimExists` is its own exception.** The plan says a fresh `run_arm` refuses a claimed tree but names no exception; a claim means an earlier invocation owns the run tree, not that the arm has a result, so it is distinct from `FirstResultExists`.
5. **`timing_run` returns `None` when stopped.** Its `{steps, wall_seconds, seconds_per_step}` mapping is pinned by existing tests, so a stop is signalled by `None` rather than a fourth key. `timing_runs` counts attempts, which is why an interrupted timing run plus its repeat records 2.
6. **Two extra refusals.** A polish checkpoint must also carry its L-BFGS `state_dict`, and a resume also refuses a changed `first_omega_0`; both would be unrestorable, and the plan names only the segment state and the digests.
7. **The memory figure may be null.** `vm_stat` can fail on this macOS; the value is logged in `process.json` as an advisory field and never gates a launch.
8. **Every arm carries an arm generator.** `run_arm` now builds `np.random.default_rng(SEED)` for every arm, not only a physics arm, so one checkpoint format holds all four RNG streams and exact continuation is one code path. The generator is unused on a data-only arm.
9. **A crash without a governed stop goes to the owner.** The claim and the run directory survive an uncaught failure, so admission refuses a fresh start and there is no checkpoint to resume: the arm is stuck for the owner, which is SPEC Requirement 8's rule.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] One existing test encodes a premise this plan removes**
- **Found during:** Task 2 implementation
- **Issue:** `test_budget_driver::test_every_handler_for_an_owner_stop_re_raises` asserts that exactly two `except OwnerRouted` handlers exist in the module. `main` adds a third, and it is the one handler that must *not* re-raise: the plan requires it to print `OWNER-ROUTED` and exit 3.
- **Fix:** The test was rewritten in place, not deleted: it now asserts the re-raise rule for `_official_counts` and `run_arm` and pins `main` as the top-level mapper.
- **Files modified:** `tests/phase60/test_budget_driver.py`
- **Verification:** the module passes in the full discovery
- **Committed in:** `2da19abe`

### Process

**2. One code commit, no separate RED commits.** The plan names a single commit after both tasks; Tasks 1 and 2 carry `tdd="true"`, so their RED evidence was retained from a log instead of committed (below). **Impact:** none on behaviour.

**3. Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.

**Total deviations:** 1 auto-fixed (Rule 3) and 2 process notes. **Impact on plan:** no frozen value, threshold, catalog entry or schema field changed.

### Plan-coverage items

- `PINNED_MODULES` includes `learnability_run.py`; this plan is the last edit to it before Plan 60-13 writes the protocol. Its committed SHA-256 is `a031b9373db7dbd7a15429f7e699fb1743b7f33f2563b6f01ac3166a63bf711c` (the pre-plan file was `dad7e218...0a55`, the digest Plan 60-11 recorded).
- `main` prints `ADMIT-OK` on a run as well as on `--admit-only`; the plan requires the token only for `--admit-only`, and the launcher's preflight uses `--admit-only`.

## TDD Gate Compliance

- **Task 1** is a tracer: its tests landed with its code in `2da19abe`, and its `<verify>` was run on the final tree (25 tests, OK, 133 s). Not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, and the verify holds only an automated command, so it was run and expansion continued: "Tracer verified end-to-end - expanding".
- **Task 2** carries `tdd="true"`. RED evidence is retained at `/tmp/gsd-60-12/tdd-red.log`: both new modules were run against `HEAD~1`'s `learnability_run.py` (SHA-256 `dad7e218...0a55`, restored byte-for-byte afterwards and re-checked against the committed file's SHA-256 `a031b937...f711c`). The run reports `Ran 2 tests`, `FAILED (errors=2)`: `ImportError: cannot import name 'ClaimExists'` and `ImportError: cannot import name 'GovernedStop'`, i.e. the module under test is missing every new symbol, which is the honest RED. GREEN is the full discovery at the final code.
- `gsd_run check tdd-red-evidence` parses Node TAP output and does not apply to Python `unittest` output, so the RED evidence is recorded from the retained log, as in Plans 60-05, 60-08, 60-10 and 60-11.
- No mutation pass was run: the plan does not ask for one, and every behaviour line is a behavioural proof over real fixture runs or a real child process.

## Verification Results

Logs are retained outside the repository under `/tmp/gsd-60-12/`. Each log starts with its command, HEAD, working directory and start time and ends with its exit status and elapsed seconds.

| Command | Result |
|---|---|
| Task 1 verify, `python -B -m unittest tests.phase60.test_resume -v` | Ran 25 tests in 132.948 s, OK, exit 0 (`task1-verify-3.log`) |
| Task 2 verify 1, `python -B -m unittest discover -s tests/phase60 -t . -v` | Ran 960 tests in 802.474 s, OK (skipped=1, the opt-in `PHASE60_PLATFORM_PROBES` platform probe), exit 0, 804 s (`full-discovery.log`, run once at the final code, HEAD `a10351b6` + working tree) |
| Task 2 verify 2, `tests.phase42.test_signals` + `tests.phase39.test_prohibitions` + the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests `-v` | Ran 43 tests in 306.313 s, OK, exit 0 (`prohibition-suite.log`; run while the discovery held the CPU, hence the long elapsed) |
| Task 2 verify 3, `python -B -m pinn.verification.learnability_run r1-1632 --admit-only` | `ADMIT-REFUSED: there is no run protocol: .planning/phases/60-single-system-learnability/evidence/run-protocol.json`, exit 2, nothing created under `runs/` |
| `python -B -m unittest tests.phase60.test_cli -v` (during development) | Ran 24 tests in 0.113 s, OK |
| Focused regression, `test_physics_arm test_cross_check test_schedule test_refusals test_launcher test_admission -v` | Ran 233 tests in 382.987 s, OK |
| RED evidence, both new modules against `HEAD~1`'s runner | `Ran 2 tests`, `FAILED (errors=2)` (two ImportErrors); module restored and SHA-256 re-checked (`tdd-red.log`) |

The full discovery ran once, at the final code, and was not repeated; its complete stdout and stderr are retained. The two new modules account for 49 of the 960 tests.

## Known Stubs

None. `pinn/training/signals.py` is untouched and the SIGHUP handler lives in the runner, as the plan requires. `.planning/WINDOWS.md` was not appended: no stub, skipped test or unrun verify was left behind.

## Threat Flags

None. The plan adds no endpoint, authentication path or file format outside the ignored run tree. Threat register: T-60-02 mitigated (`torch.load(..., weights_only=True)` literal; a payload of tensors and plain containers; `load_resume_checkpoint`); T-60-07 mitigated (the claim, one marker per stop, `launch.stops` in the record, and refusals on drift or a missing segment; `ResumeRefusalTests` and `SignalSubprocessTests`); T-60-09 mitigated (`begin_long_step` under the Phase 60 evidence root; `LifecycleTests`); T-60-11 mitigated (one top-level mapping to exit 3 with no retry; `ExitMappingTests`); T-60-12 mitigated (resume refuses any change of protocol SHA-256 or pinned module digest); T-60-SC accepted (nothing installed).

## Issues Encountered

- Two test modules reuse the fixture arm id `fixture-hierarchical-gold-0` under separate temporary roots. A repo-level default run tree made them share a claim, which is what forced decision 1 (the per-evidence-root default).
- The first draft resumed an Adam-phase checkpoint with the checkpoint's driver result already marked `stopped`, so the resumed run tried to write a second stop with no signal. The driver is now re-entered when the checkpoint says Adam is incomplete, and reused only when `adam_complete` is true.
- The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-13 (the real protocol and preflight).** `learnability_run.py` is final for this phase. Its SHA-256 is `a031b937...f711c`; the protocol's `module_sha256` mapping must record that value, and any later edit is drift. `main` calls `admit_arm(arm_id, resume=...)`, `load_protocol(...)`, `open_real_context(...)` and `load_scorecard()`, and the launcher's argv (`caffeinate -is <python> -B -m pinn.verification.learnability_run <id> [--resume]`) is unchanged.
- **Plans 60-14 to 60-22** launch real arms through `main`; the run tree is `runs/phase60/<arm-id>` with `claim.json`, `process.json`, `resume.pt` and `stop-<n>.json`, none of it committed.
- **Open for the owner or verifier:** coverage item D11 in this SUMMARY (the nine readings above), beside the earlier ones from 60-10 (D8), 60-09 (D7), 60-08 (D10 and D11), 60-07 (D9), 60-06 (D8), 60-05 (D7), the two GAP-60-05 polish-stopping readings, the 60-23 contract details (D8) and the 60-11 readings (D9 and D10).

---

*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- The two created test files and this SUMMARY exist on disk; the code commit `2da19abe` exists and created `test_resume.py` and `test_cli.py` while deleting no tracked file (`git show --stat`).
- Every task's `<verify>` was run on the final code and the results are the table above; the full discovery and the prohibition suite pass with no `FAILED` line, and the real `--admit-only` exits 2 with one `ADMIT-REFUSED:` line and no `runs/phase60` directory.
- The staged commit held exactly the four owned paths; `.planning/config.json`, the v2.2 design brief and every other pre-existing dirty or untracked path were left untouched, and nothing under `runs/` was staged.
- `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` are updated after this file by hand, as the orchestrator's state rule requires.

