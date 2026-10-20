---
phase: 60-single-system-learnability
plan: 07
subsystem: testing
tags: [detached-launcher, supervisor, caffeinate, governed-resume-gate, status-query, dry-run-admission, stdlib-only, argv-only]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-23's closed SEQUENCES map, 42-arm catalog and EXIT_* codes; Plan 60-01's RUNS_REL and Phase 60 static guard; Plan 60-06 as a coupling edge only"
provides:
  - "launch_phase60_arm.py: a detached supervisor that runs one closed sequence of arms one at a time, records every exit, resumes only after a governed 129/130/143 stop, answers --status and admits arms with --dry-run"
  - "tests/phase60/test_launcher.py: 90 stub-only tests, including survival of a hangup and kill of the launching process group"
affects: [60-12, 60-13, 60-14, 60-15, 60-16, 60-20, 60-21, 60-22]

actuals:
  tokens: 20627
  tasks: 2
  commits: 2
plan_head_before: 97672611710bafe3d9c0d283a35c82206177219a

tech-stack:
  added: []
  patterns:
    - "A long-lived supervisor that imports only the standard library (the arm catalog is imported lazily, so it never loads torch)"
    - "Exclusive-create launch records (open 'x', mkdir exist_ok=False) so an invocation directory and its files are never reused or rewritten"
    - "Test base class that makes an accidental real launch impossible: caffeinate is patched to /usr/bin/true and the Metal host probe fails the test if reached"
    - "Stub arms gated on a file the test controls, so ordering and 'returns at once' are proved without sleeps"
    - "Scratch mutation driver that restores the file byte-identically and checks its SHA-256 after every mutation"

key-files:
  created:
    - .planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py
    - tests/phase60/test_launcher.py
  modified: []

key-decisions:
  - "A resume is accepted only for an arm that exited by its own handler with 129, 130 or 143 and a recorded stopped arm that belongs to the sequence; any death by a signal (even SIGTERM, code 143) is refused because the handler never ran and no checkpoint exists"
  - "The supervisor stays standard-library only: learnability_arms is imported on first use, and GOVERNED_STOP_CODES is a literal pinned by a test to the catalog's EXIT_SIGHUP, EXIT_SIGINT and EXIT_SIGTERM"
  - "start() writes process.json itself and returns at once; the supervisor has no handlers, its own session and process group, stdin from /dev/null"
  - "A supervisor that is gone without an exit record is refused (owner decides), never reported as running and never given a fifth status token"
  - "--dry-run relays the runner's own ADMIT lines, probes every arm, and passes only when every arm exited 0 and printed ADMIT-OK"

requirements-completed: [INST-05, FEAS-03]

coverage:
  - id: D1
    description: "Closed sequence names (the 51 names of learnability_arms.SEQUENCES) and argv-only arm commands: caffeinate -is, the pinned python -B -m pinn.verification.learnability_run, the arm id, and --resume on a resume; any other name or arm id is refused"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#SequenceTests, ArmArgvTests, StaticShapeTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "A detached supervisor runs the arms strictly one at a time, records every exit (a signal death is 128 plus the signal number, SIGKILL is 137), stops at the first non-zero exit and writes exit.json last; start() returns before the first arm ends"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#SupervisorOrderTests, StopAtFailureTests, SignalDeathTests, ExitDescriptionTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Launch records stay in the ignored runs/.launch/phase60 tree, each file created exclusively; launch.json holds no working directory; the supervisor has its own session and group and its stdin, stdout and stderr go to /dev/null, supervisor.out and supervisor.err"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#LaunchRecordTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Governed resume gate: only a stop by 129, 130 or 143 resumes, as a new invocation that restarts the stopped arm with --resume and then the arms after it; a completed sequence, a refused arm, an owner-routed arm, a SIGKILL or any signal death, a missing exit record or any other code goes to the owner"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#InvocationTests, ResumeGateTests, LaunchTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "--status prints SEQUENCE-NOT-LAUNCHED, SEQUENCE-RUNNING with ARM-PID, SEQUENCE-COMPLETE or SEQUENCE-STOPPED <arm-id> <code> and creates nothing; the real command on rung1 prints SEQUENCE-NOT-LAUNCHED"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#StatusTests, CommandLineTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py --sequence rung1 --status (exit 0, stdout exactly SEQUENCE-NOT-LAUNCHED)"
        status: pass
    human_judgment: false
  - id: D6
    description: "--dry-run runs the runner's --admit-only for every arm in the foreground and starts no supervisor; it passes only when every arm exited 0 and printed ADMIT-OK"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#DryRunTests, CommandLineTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "The supervisor outlives a hangup and a kill of the launching process group and still completes its sequence and writes exit.json"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_launcher.py#SurvivalTests"
        status: pass
    human_judgment: false
  - id: D8
    description: "The Phase 60 static guard scans the launcher (weights_only rule, forbidden names, evaluator imports) and passes; the prohibition suites still pass"
    verification:
      - kind: unit
        ref: "tests/phase60/test_static_guards.py; tests.phase39.test_prohibitions"
        status: pass
    human_judgment: false
  - id: D9
    description: "Readings of the plan text that the sources leave open (listed under 'Readings of the plan text'): refusing every signal death at the launcher gate, the unreadable-supervisor case of --status, the dry-run admission rule and the process.json writer"
    verification: []
    human_judgment: true
    rationale: "Each fails closed and moves no locked value, but they fix the launcher's refusal and output shapes that Plans 60-12 to 60-22 read. The owner or verifier should confirm them before the first real arm, or ask for a gap entry."

duration: 35min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 07: Detached arm launcher Summary

**A standard-library-only supervisor that runs one closed sequence of learnability arms one at a time under caffeinate in its own session, records how every arm ended, resumes only after a governed 129, 130 or 143 stop (every other ending goes to the owner), answers `--status`, admits arms with `--dry-run`, and survives a hangup and kill of the session that launched it.**

## Performance

- **Duration:** about 35 min. The start time was not captured at spawn; the first timestamp captured was 2026-10-20T08:07:14Z, after the plan and its references had been read.
- **Completed:** 2026-10-20T08:40:00Z (approximate; the SUMMARY commit follows)
- **Tasks:** 2 (Task 1 tracer, Task 2)
- **Files:** 2 created, none modified: `launch_phase60_arm.py` (543 lines) and `test_launcher.py` (1,209 lines)

## Accomplishments

- **Closed set, argv only.** `sequence_arms` resolves a name only through `learnability_arms.SEQUENCES` (51 names: nine named sequences and one `arm:<id>` per catalog arm). `arm_argv` builds `[/usr/bin/caffeinate, -is, <pinned python>, -B, -m, pinn.verification.learnability_run, <arm-id>]` and appends `--resume` on a resume; an id outside the 42-arm catalog is refused. No test or source line uses a shell, and a static test checks it.
- **Detached supervisor (Task 1).** `start()` writes `launch.json` (exclusive create), starts `[sys.executable, <this file>, --supervise, <dir>]` with `start_new_session=True`, stdin `/dev/null`, stdout and stderr to `supervisor.out` and `supervisor.err`, `close_fds=True`, records it in `process.json` and returns at once. `supervise()` runs each arm in order into one `output.log`, writes `arm-<i>.json` after each exit (a death by signal is exit code 128 plus the signal number, so SIGKILL is 137), stops at the first non-zero exit and writes `exit.json` last. It installs no signal handlers and imports nothing from the repository.
- **Governed resume (Task 2).** `next_invocation_dir` refuses a fresh launch over any existing launch directory and a resume unless the latest invocation's `exit.json` names a stopped arm of the sequence with code 129, 130 or 143 and no signal death. `resume_argvs` builds the stopped arm with `--resume` followed by the arms after it, so a resume is a new invocation and never a silent restart.
- **Status and dry run.** `--status` prints exactly one of `SEQUENCE-NOT-LAUNCHED`, `SEQUENCE-RUNNING` (plus `ARM-PID <pid>` read from the running arm's own `runs/phase60/<arm-id>/process.json`), `SEQUENCE-COMPLETE` or `SEQUENCE-STOPPED <arm-id> <code>`, and creates nothing. `--dry-run` runs the runner's `--admit-only` for every arm, relays its lines, starts no supervisor and fails unless every arm admitted. `launch()` checks the sequence name, the Metal device and the invocation gate, then starts the supervisor; `main` prints `LAUNCHED <sequence> invocation-<n>`.
- **Survival.** A helper in its own session starts a gated stub sequence, is sent SIGHUP and then SIGKILL as a process group, and dies; the supervisor (own session, own group) is still alive afterwards and finishes both arms. A second test uses a launching helper whose stdin is an open pipe and reads the supervisor's descriptors with `lsof`: fd 0 is `/dev/null`, fd 1 and 2 are its own files.

## Task Commits

1. **Task 1: Tracer, a detached supervisor runs a closed stub sequence one at a time** - `ba8d30f6` (feat)
2. **Task 2: Governed resume gate, status query, dry-run admission, survival** - `e1f64139` (feat)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after Task 1: not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, and the tracer's verify holds only an automated command, so it was re-run on the committed tree (29 tests OK, no failure strings) before Task 2 started: "Tracer verified end-to-end - expanding".

## Files Created/Modified

- `.planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py` - the launcher (`LaunchError`, `sequence_arms`, `arm_argv`, `admit_argv`, `describe_exit`, `next_invocation_dir`, `resume_arm_ids`, `resume_argvs`, `start`, `supervise`, `status`, `dry_run`, `launch`, `main`)
- `tests/phase60/test_launcher.py` - 90 tests in 15 classes; every launch runs stubs under a temporary directory

## Decisions Made

- **Governed means handled.** A resume is accepted only for an arm that exited by its own handler with 129, 130 or 143. `exit.json` records `signal`, and any non-null signal refuses the resume, because a raw SIGTERM death (return code -15, recorded as 143) means the runner's handler never ran and no checkpoint was written. A graceful stop exits normally and records `signal: null`, so no legitimate resume is blocked.
- **Light supervisor.** The supervisor sits idle for hours beside an arm that needs 6 GiB free. Importing the arm catalog pulls in `torch` and `numpy`, so `learnability_arms` is imported on first use and the supervisor never loads it. `GOVERNED_STOP_CODES` is a literal `(129, 130, 143)` that a test pins to `EXIT_SIGHUP`, `EXIT_SIGINT` and `EXIT_SIGTERM`; another test loads the launcher in a fresh interpreter and asserts `torch`, `numpy` and `pinn` are absent.
- **Identity carries the arm ids.** `start(invocation_dir, argvs, *, cwd, identity)` has no other channel for them, so `identity["arm_ids"]` (one id per command) is required and `start` refuses a mismatch before writing anything. The supervisor's `stopped_arm` comes from it.
- **No working directory in launch.json.** The plan allows no home path beyond the pinned interpreter path, so the supervisor inherits `cwd` from `start()` and passes it to every arm.
- **A recorded process id of zero or below is never probed.** `os.kill(0, 0)` addresses the caller's whole process group and would report a missing supervisor as alive, so `_supervisor_alive` treats ids at or below zero, booleans and non-integers as gone (tested).
- **Test safety net.** The test base class patches `CAFFEINATE` to `/usr/bin/true` and the Metal probe to fail the test, so an unpatched path could not start a real arm. Every launch test injects its own stub command builder.

## Readings of the plan text

Each is a place where the plan, SPEC, CONTEXT, PATTERNS and the later plans leave a choice. None changes a locked value. "Fails closed" says whether the chosen reading refuses when in doubt.

1. **Signal deaths at the gate.** The plan lists "a signal death such as SIGKILL (returncode -9, exit code 137)" beside "any other code". Chosen: every death by a signal refuses the resume, including SIGHUP, SIGINT and SIGTERM (codes 129, 130, 143), by checking `exit.json`'s `signal`. The alternative reads only `stopped_code`, so a raw SIGTERM death would pass the launcher gate and rely on the runner's checkpoint and stop-marker refusal (Plan 60-12). Chosen reading fails closed; the alternative fails open at the launcher layer only. A hand-written record with no `signal` key is treated as a graceful stop.
2. **Checkpoint and marker in the gate.** `60-PATTERNS.md` adds "only when a valid resume checkpoint and a stop marker exist"; the plan's gate names only `exit.json`. Followed the plan. The launcher cannot see the checkpoint, and Plan 60-12 refuses a resume (exit 2) when `resume.pt` or the stop marker is missing, so the two layers together fail closed.
3. **Lost supervisor.** The plan lists four `--status` outcomes and "RUNNING while the supervisor is alive". A supervisor that is gone with no `exit.json` has none. Chosen: `--status` and the resume gate raise a fail-closed `LaunchError` ("owner decides", exit 1, nothing on stdout) rather than print a fifth token or report RUNNING. Later plans that read the first status line see a non-zero exit. Fails closed. Not a gap: no new token was invented.
4. **Who writes `process.json`.** The plan lists it among `start()`'s steps and says `start()` returns immediately, so `start()` writes it right after `Popen`. The Phase 57 analog had the supervisor write it and `start()` wait. A supervisor that dies on arrival is therefore noticed by `--status` (reading 3) rather than by `start()`. Fails closed via reading 3.
5. **`--dry-run` rule.** Command is `[pinned python, -B, -m, ...learnability_run, <arm>, --admit-only]` (no caffeinate: nothing trains). Its output is relayed because Plans 60-13 and 60-14 count `ADMIT-OK` lines. Every arm is probed even after a refusal. Admitted means exit 0, an `ADMIT-OK` first-token line (the runner prints `ADMIT-OK <arm>`) and no `ADMIT-REFUSED` line. The plan says only "exits non-zero unless every arm prints ADMIT-OK"; requiring exit 0 is stricter. Fails closed.
6. **Order inside a real launch.** Closed sequence name, then the Metal probe, then the invocation gate, then start. The plan says the launch "first calls `_assert_host_mps`"; a mistyped name needs no Metal probe. Both fail closed.
7. **`arm:<id>` directory names** keep the colon literally (`runs/.launch/phase60/arm:r1-1632/`). APFS allows it and a test covers it. Sanitizing would be the alternative.
8. **Extra refusals the plan does not name** (all fail closed): `arm_argv` and `admit_argv` refuse an id outside the catalog; a stopped arm that is not in the sequence goes to the owner; a launch directory with no invocation, a gap in the invocation numbers and an unreadable record are refused.
9. **Signatures.** `status` prints the lines and also returns them; `repo_root` is optional (defaults to the repository). `main`, `resume_argvs` and `launch` gained keyword-only test seams (`repo_root`, `command_builder`, `argv_builder`, `host_check`). Calls written to the plan's signatures still work. Added public names: `admit_argv`, `describe_exit`, `resume_arm_ids`, `dry_run`, `launch`.
10. **`-B` in the arm command.** The plan's truth and behavior include `-B`; `60-PATTERNS.md` shows the command without it. Followed the plan.
11. **Limits, not readings.** Liveness is `kill(pid, 0)` existence, so a reused process id would not be detected. The launcher does not itself stop two different sequences from running together; the runner's one-launch lock (Plan 60-12) does.

## Deviations from Plan

### Process

**1. Two commits instead of one.** Task 2's action names a single commit (`feat(60-07): add the detached phase 60 arm launcher`). The orchestrator asks for one commit per task, and Task 1 is a self-consistent tracer, so Task 1 has its own commit (`ba8d30f6`) and Task 2 carries the plan's named subject (`e1f64139`).

**2. Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.

No auto-fixed bugs, missing-critical additions or blockers were found in the plan's own scope. The extra refusals and the process-id guard above are additions to my own new code.

**Total deviations:** 2 process notes. **Impact on plan:** none; every plan behavior and acceptance bullet holds.

### Process notes

- **TDD.** Both tasks are task-level `tdd="true"` inside a `type: execute` plan, and `workflow.tdd_mode` is unset, so the phase's established practice was followed: tests first with logged RED evidence, one commit per task (no separate `test(60-07)` commit). RED, Task 1: skeleton with constants only, 24 tests, 103 errors, every one a missing symbol. RED, Task 2: skeleton raising `NotImplementedError`, 87 tests, 103 errors (89 `NotImplementedError`, 12 signature `TypeError`, 2 `AttributeError` from my own test code reading `caught.exception` after a swallowed error; fixed). `gsd check tdd-red-evidence` was not used (it parses Node TAP output, as Plan 60-04 noted). Logs: `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/b79d9e64-f5b6-42fe-85da-ff68416ec12e/scratchpad/exec-60-07/` (`task1-red.log`, `task2-red.log`, `task1-green*.log`, `task2-green*.log`, `final-verify1.log`, and the mutation logs).
- **Mutation checks, 81 injected faults, 80 caught, 1 equivalent.** First pass on Task 1 found two escapes (the supervisor keeping stdin; `mkdir(exist_ok=True)`). The first escaped because the test runner's own stdin is already `/dev/null`, so the test now launches from a helper whose stdin is an open pipe; the second because a reused directory is also refused by the exclusive `launch.json`, so a test now starts into a pre-existing empty directory. Both are then caught. The one equivalent mutant drops the `not arm_id` guard in `_governed_stop`; the membership check in `resume_arm_ids` refuses the same input. The driver restored the launcher byte-identically (SHA-256 checked) after every mutation.
- **Expensive commands.** Only the two mutation passes exceeded 60 s (3 min 45 s and 1 min 26 s); they are diagnostic, each ran once, and their 32 s tests came from injected faults that left stubs waiting for their 30 s timeout. No validation command took over 5 s. The final verify evidence was gathered once on the final code and the committed bytes are identical to it (launcher SHA-256 `03ebf555...6ad2`, test `605873a8...8d0`), so nothing was rerun at closeout.
- **Isolation.** The generic executor rule that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The cwd-drift and protected-branch assertions ran before each commit. `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md` and `.planning/config.json` were not touched (`git diff --quiet 97672611 HEAD` on them exits 0); `.planning/WINDOWS.md` was not appended (no stub, skipped test or unrun verify). The Sequentialthinking MCP, `ToolSearch` and the context-mode tools were not available to this executor.

## Verification Results

| Command | Result |
|---|---|
| Task 1 verify, `python -B -m unittest tests.phase60.test_launcher -v` | RED 24 tests, 103 errors; GREEN 24 OK; committed tree (tracer gate) `Ran 29 tests`, OK |
| Task 2 verify 1, `python -B -m unittest tests.phase60.test_launcher tests.phase60.test_static_guards -v` | `Ran 116 tests in 3.646s`, OK (90 launcher, 26 static guard), no failure strings |
| Task 2 verify 2, `launch_phase60_arm.py --sequence rung1 --status` | exit 0, stdout exactly `SEQUENCE-NOT-LAUNCHED`, stderr empty, `runs/` listing hash unchanged, no `runs/phase60` |
| `python -B -m unittest tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests | `Ran 35 tests`, OK |
| `python -B -m unittest tests.phase59.test_static_guards` (its scan covers the Phase 59 evidence directory only) | `Ran 15 tests`, OK |
| `ruff check` (no repository config, default rules) on both files | All checks passed |
| Static guard scan set (`discover_scan_set()["evidence"]`) | contains `launch_phase60_arm.py`, so its torch-load, forbidden-name and evaluator-import rules ran on it |
| `git status --porcelain` before each commit | only this plan's files differed from the other sessions' pre-existing changes; no test wrote outside its temporary directory; no `__pycache__` under `tests/phase60` or the Phase 60 evidence directory |
| Final process check | none of mine remain; only another session's heartbeat `caffeinate -i -t 300` (parent 32132, new PID each time) |

Not run, by design: the whole `tests/phase60` package (the orchestrator's wave gate runs it; this plan adds two files and edits no shared code), a real launch, and `--dry-run` against the real runner (the runner's command line is Plan 60-12's, and the plan forbids touching real data).

## Known Stubs

None. The only unimplemented pieces are other plans' work: the runner's command line, `--admit-only` output and `runs/phase60/<arm-id>/process.json` (Plan 60-12).

## Threat Flags

None. The edits add no network endpoint, auth path or file access outside the plan's threat register: T-60-10 mitigated (argv lists, closed names, `SequenceTests`, `ArmArgvTests`, a no-shell static test), T-60-07 mitigated (governed codes only, exclusive-create files, `ResumeGateTests`), T-60-17 mitigated (own session and group, stdin `/dev/null`, `caffeinate -is`, `SurvivalTests`), T-60-06 accepted (launch files stay in the ignored `runs/` tree and hold no working directory), T-60-SC accepted (no package installed).

## Issues Encountered

None that blocked work. Two tests of mine were weaker than they looked (stdin and `exist_ok`); the mutation pass exposed them and both were strengthened before the first commit.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-12 (the runner command line)** must provide what the launcher reads: `python -B -m pinn.verification.learnability_run <arm-id> [--resume | --admit-only]`; `--admit-only` printing `ADMIT-OK <arm-id>` (exit 0) or `ADMIT-REFUSED: <reason>` (exit 2); exit codes 0, 2, 3 and 129, 130, 143 through the arm's own handlers; and `runs/phase60/<arm-id>/process.json` with an integer `pid` key. The launcher refuses a resume after any death by a signal, so a graceful stop must exit by the handler.
- **Plans 60-13 to 60-22** can call `launch_phase60_arm.py --sequence NAME [--dry-run | --status | --resume]`. Their automated checks match: `--status` prints a token on its first line and exits 0, `--dry-run` prints one `ADMIT-OK` line per arm and the output contains `FAIL-CLOSED` or `ADMIT-REFUSED` on a refusal, and a real launch prints `LAUNCHED <sequence> invocation-<n>`. A `--status` that exits 1 with "owner decides" is the lost-supervisor case (reading 3); a `--resume` that exits 1 with "arm cannot resume; owner decides" goes to the owner.
- **Open for the owner or verifier before the first real arm:** coverage item D9, the readings above, chiefly 1 (every signal death refuses), 3 (lost supervisor) and 5 (the dry-run admission rule).

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- Both created files exist on disk; commits `ba8d30f6` and `e1f64139` exist and `git log --grep='(60-07)'` returns exactly them; no stub, TODO or skipped test; the committed bytes of both files equal the bytes the final verify ran on.
- Task acceptance criteria re-checked against the final code (logs retained): Task 1 (ordering and non-overlap, no second start after a failure, `137` and `SIGKILL`, nothing written outside a temporary directory) and Task 2 (resume gate accepts exactly 129, 130 and 143 and refuses 0, 1, 2, 3 and 137, survival of a hangup and kill, the real `--status` output, the static guard scanning the launcher) all pass; the plan-level verification passes.
