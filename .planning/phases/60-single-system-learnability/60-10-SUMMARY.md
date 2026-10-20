---
phase: 60-single-system-learnability
plan: 10
subsystem: verification
tags: [run-protocol, pre-registration, drift-refusal, record-preflight, arm-admission, branch-ladder, tdd, mutation-tests]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-23's closed 42-arm catalog, the closed sequences and preflight_records; Plan 60-06's branch_state, ruling loaders and re-measure record reader; Plan 60-09's re-measure record; Plan 60-02's scorer successor record; Plan 60-07's launcher (a pinned file)"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard, the panel singles and inner laps, the FEAS-09 picks and the two-Kepler formula rows that the protocol pins"
provides:
  - "pinn/verification/learnability_protocol.py: build_protocol, write_protocol, load_protocol (drift refusal), write_preflight, admit_arm and a command line (write, check, preflight, admit)"
  - "tests/phase60/test_protocol.py (75 tests) and tests/phase60/test_admission.py (69 tests)"
affects: [60-11, 60-12, 60-13, 60-14, 60-15, 60-16, 60-17, 60-18, 60-19, 60-20, 60-21, 60-22]

actuals:
  tokens: 42002
  tasks: 2
  commits: 5
plan_head_before: 31467d7eb056431759fdb98fd961827f36eb7e27

tech-stack:
  added: []
  patterns:
    - "A pre-registration built only from the code's own constants, frozen scorecard sections and committed evidence, normalized to plain JSON so the in-memory protocol equals the file"
    - "Drift refusal by SHA-256 of every pinned file plus every recorded source file; the exception carries the list of paths"
    - "Admission as an ordered series of cheap committed-file checks, each refusal one line, with the branch decided by the Plan 60-06 query"
    - "Synthetic git repositories built once per process from byte-identical copies of the pinned files, with the real preflight writer and protocol builder run inside them"
    - "Mutation checks with a scratch driver that restores the file and compares its SHA-256 after each mutation"

key-files:
  created:
    - pinn/verification/learnability_protocol.py
    - tests/phase60/test_protocol.py
    - tests/phase60/test_admission.py
  modified: []

key-decisions:
  - "A record whose window holds a sample count other than the verified one (1,001 gold, 126 hierarchical base, 59 standard base) blocks the arms that use it, although SPEC Requirement 8 names only missing, empty and unreadable records; it is the verified-corpus check of 60-RESEARCH assumption A10"
  - "ProtocolDrift also reports a protocol that is absent, untracked, dirty or malformed, so one exception type and one CLI token cover every case in which the registered procedure cannot be shown to be the one that would run"
  - "load_protocol also compares the recorded digest of each input the protocol cites (Phase 59 panels, picks and two-Kepler rows, the Stage-0 metadata, the scorer successor record) with the current file, not only the 33 pinned modules"
  - "The admission result gains scorer_context_r_ref (the governed reference the scorer's context column always uses) and the ruling block gains answer and approved_first_omega_0, so the runner can hand the block to check_override unchanged"
  - "c-r1u arms wait for the re-measure PASS because the plan says every c- arm needs the ladder taken, although a data-only arm needs no reference; admission does not order the arms of a sequence (the closed sequence names do)"

patterns-established:
  - "Plain JSON types only in build_protocol's result, so build, write and load round-trip with equality"
  - "A test seam that keeps the corpus closed: every preflight-writer test patches open_real_context to fail if it is reached"

requirements-completed: [INST-05, FEAS-03, FEAS-04, FEAS-09]

coverage:
  - id: D1
    description: "build_protocol assembles phase60-run-protocol/v1 from the trainer's constants, the frozen scorecard sections and the committed Phase 59 and Phase 60 inputs: seed, runtimes, D-01 to D-05 schedule, GAP-60-03 clipping, GAP-60-04 timing, cadence, GAP-60-05 polish, GAP-60-06 divergence, GAP-60-07 cross-check, GAP-60-08 weights, the G2 grid, laps, sweep pairs and GAP-60-09 stop, the two skip reasons, GAP-60-10 to GAP-60-13, the nine owner stops and the readout notes"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_protocol.py#ContentTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "A panel, lap count, probe pick, S_H or eps_H value, scorer or scorecard digest that does not match its pin makes build_protocol raise ProtocolDrift naming the file; the owner's two answers (clipping veto, failed-confirmation pre-answer) are the only free arguments and any other value raises"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_protocol.py#PinCheckTests, VetoTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "write_protocol and load_protocol round-trip; load_protocol accepts only a tracked, clean protocol whose 33 pinned files and recorded source files still hash as recorded, names every file that differs, and write_protocol refuses once a record or owner stop exists"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_protocol.py#RoundTripTests, DriftTests, CommandLineTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "write_preflight checks the ten assigned records once, records status and the verified window count per key and ok or blocked per arm, embeds the open attestation with zero test-split opens, never names the data root, is written once, and substitutes nothing for a blocked key"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_admission.py#PreflightWriterTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "admit_arm admits a real arm only under a drift-free protocol, a cleared preflight the protocol pins, the amendment in the history, the registered scorer and scorecard, no existing result and the branch the committed G2 records have taken (all 42 arms checked against the admitted set in nine scenarios)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_admission.py#AdmissionRung1Tests, AdmissionBranchTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "Admission returns the Stage-0 reference in force (governed at the locked setting, the re-measured one after a continue), the governed reference for the scorer's context column, S_H for the probe Rung-2b arms, the clipping flag and the ruling facts (SHA-256, on_grid, equals_confirmed) for continue arms"
    requirement: "FEAS-09"
    verification:
      - kind: unit
        ref: "tests/phase60/test_admission.py#ReferenceInForceTests, AdmissionBranchTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "The Phase 60 static guard, the Phase 38 and 39 prohibition suites and the full tests/phase60 discovery pass; the frozen scorecard, the governed R_ref and every other committed module are byte-identical, and no real evidence file or runs/phase60 directory exists"
    verification:
      - kind: unit
        ref: "python -B -m unittest discover -s tests/phase60 -t . -v (842 tests, OK, skipped=1)"
        status: pass
    human_judgment: false
  - id: D8
    description: "Readings of the plan text that the sources leave open (listed under Decisions Made): a wrong window count blocks an arm, ProtocolDrift covers an absent protocol, load_protocol checks recorded source digests, extra protocol sections and admission keys, c-r1u waits for the re-measure"
    verification: []
    human_judgment: true
    rationale: "Each fails closed and moves no locked value, but they fix the shape of the protocol, the preflight and the admission result that Plans 60-11 to 60-13 read, and the protocol is sealed in Plan 60-13. The owner or verifier should confirm them before the seal or ask for a gap entry."

duration: 71min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 10: Run protocol, preflight and arm admission Summary

**A run protocol built from the code's own constants and SHA-pinned to 33 modules and 5 cited inputs, a ten-record preflight that blocks without substituting, and an admission check that starts an arm only under a drift-free protocol, a cleared record, the amendment and the branch the committed G2 records have taken.**

In plain language: before the first real experiment the project writes down exactly how every experiment will run and fingerprints the code that will run it. This plan builds the machinery for that and for the guard behind it. Nothing real was written: the real protocol and the real preflight are Plan 60-13's. Each experiment, once the protocol is sealed, refuses to start if any fingerprinted file changed, if its data file is missing or has an unexpected length, or if the earlier results say it should not run.

## Performance

- **Duration:** about 71 min of wall clock (2026-10-20T14:19:38Z to the SUMMARY at about 15:30Z). The single full discovery run took 18 min 36 s of it on a loaded machine.
- **Tasks:** 2 (Task 1 tracer, Task 2), both test-first
- **Files:** 3 created, none modified: `learnability_protocol.py` (1,497 lines), `test_protocol.py` (1,099 lines, 75 tests) and `test_admission.py` (1,080 lines, 69 tests)

## Accomplishments

- **The protocol (Task 1).** `build_protocol(repo_root, amendment_commit, clip_data_only_arms=True, failed_confirmation_pre_answer=None, preflight_sha256=None)` returns plain JSON types (build, write and load round-trip with equality). Sections: seed 42; runtime and cross-check runtime; `schedule` (LR base, decay, betas, eps and the per-stage rates from the trainer's `OptConfig`, warmup `min(2000, floor(0.1 B))`, the second-cosine extension); `budget` and `cadence` and `timing` from the scorecard and `TIMING_STEPS`; `clip` (the trainer's table for stages 0, 4 and 6, median floor, `clip_data_only_arms`); `polish` (the scorecard's `lbfgs_polish` plus the GAP-60-05 rules); `divergence`, `cross_check`, `weights`, `first_result`; `panel`, `probes` and `formula` from the Phase 59 files; `g2` (grid, locked value, inner laps, the four sweep pairs derived by `sweep_plan`, the sweep, confirmation, rescue and failed-confirmation rules, `failed_confirmation_pre_answer`); `skip_reasons` (the two byte-exact strings); `decisions` (D-06 to D-11); `r_ref_governed` and `r_ref_rule`; `approved_omega_rule`; `s_h`; `normalizer_stats_sha256`; `catalog` and `sequences` (42 arms, 51 names); the nine `owner_stops`; the four `readout_notes`; and the digests (`scorecard_sha256`, `scorer_sha256` equal to the successor record, `module_sha256` over `PINNED_MODULES`, `preflight_sha256`, `amendment_commit`).
- **Drift refusal.** `load_protocol(repo_root=None, evidence_root=None, require_committed=True)` accepts only a tracked, clean protocol that pins exactly `PINNED_MODULES` and whose pinned files and recorded source files still hash as recorded; `ProtocolDrift(message, paths)` names every file that differs. `write_protocol` refuses (`HarnessHalt`) once any `record.json` or `owner-stop.json` exists under `evidence/arms`. A `LoadedProtocol(payload, sha256, path)` is returned.
- **The preflight (Task 2).** `write_preflight(repo_root=None, evidence_root=None, context=None, key_map=None)` reads the ten assigned records through `preflight_records`, records per key the status, the sample count within T and the verified count (`expected_within_t`, `count_ok`), derives ok or blocked for each of the 42 arms with the blocking keys, embeds the open attestation (`HarnessHalt` on a nonzero counter or a missing attestation, nothing written), is written once with `write_record_exclusive`, and hands `write_record_exclusive` the data root so the redaction guard refuses any text that names it. A blocked probe key blocks only the four arms that use it.
- **Admission (Task 2).** `admit_arm(arm_id, *, repo_root=None, evidence_root=None, resume=False)` checks, in order: the protocol loads without drift; the arm is in the closed catalog; its train, score and beside keys are cleared in the committed preflight that the protocol pins (and the preflight's open counters are zero); the amendment commit is an ancestor of HEAD; the scorer and scorecard on disk are the registered ones; no `record.json` or `owner-stop.json` exists and a fresh start has no `runs/phase60/<arm-id>` while a resume has one; and the branch the committed records have taken allows the arm. Nine scenario trees check all 42 arms against the admitted set (start: the three Rung-1 arms; G2 fired: the four sweep arms of the recorded system; curve written: the one recorded confirmation arm; no rescue, skipped, rescue unanswered, go to the verdict: none; G2 not fired: the ten ladder arms; a continue with a passed re-measure: the uncovered Rung 1 and the ten `c-` arms).
- **What admission returns.** `arm_id`, `protocol_sha256`, `preflight_sha256`, `first_omega_0`, `omega_provenance`, `ruling` (path, SHA-256, answer, approved value, `on_grid`, `equals_confirmed`) for continue arms, `r_ref_in_force` (path, SHA-256, value, the note "Stage-0 reference in force, applied unchanged") and `scorer_context_r_ref` for physics arms, `s_h` for the probe Rung-2b arms, `clip_enabled` (the protocol's flag for data-only arms, true for physics arms) and `failed_confirmation_pre_answer`.
- **Command line.** `python -B -m pinn.verification.learnability_protocol {write --amendment-commit SHA [--no-clip-data-only-arms] [--failed-confirmation-pre-answer {no_rescue,rescue}] | check | preflight | admit ARM}`, each with `--evidence-root`. Tokens: `PROTOCOL-WRITTEN`, `PROTOCOL-OK`, `PROTOCOL-DRIFT`, `PROTOCOL-REFUSED`, `PREFLIGHT-OK`, `PREFLIGHT-BLOCKED`, `PREFLIGHT-REFUSED`, `ADMIT-OK <arm-id>`, `ADMIT-REFUSED: <reason>`; exit 0 or 2.
- **Real-corpus smoke (read-only, not a committed test, nothing written).** `write_preflight` was run against the real corpus with `write_record_exclusive` replaced by a capture and a temporary evidence root: all ten keys `ok` in the train split with 126 (hierarchical base), 1,001 (gold) and 59 (standard base) samples within T, as 60-RESEARCH Finding G records; 42 of 42 arms ok; the attestation showed 266 train opens (the normalizer recovery plus the ten records) and 0 test-split opens, 0 blocked and 0 refused; the payload held no data-root text. The evidence directory still held only the two earlier files afterwards.

## Task Commits

1. **Task 1 RED: failing run protocol tests** - `108ca2e8` (test)
2. **Task 1 GREEN: the run protocol builder, writer and loader** - `304742bf` (feat)
3. **Task 2 RED: failing preflight and admission tests** - `763fc8c8` (test)
4. **Task 2 GREEN, the plan-named commit: the run protocol, preflight and admission** - `2d78ab9d` (feat, subject `add the run protocol, preflight and admission`; its body names SPEC Requirements 4 and 8, D-08, D-11 and GAP-60-03 to GAP-60-13)
5. **Hardening after the mutation pass: stronger admission tests and two unreachable checks removed** - `af81ac24` (test)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after `304742bf`: not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, and the tracer's verify holds only an automated command, so it was re-run on the committed tree (75 tests OK, exit 0, none of the fails_when strings) before Task 2 started: "Tracer verified end-to-end - expanding".

## Files Created/Modified

- `pinn/verification/learnability_protocol.py` - the module (constants `PROTOCOL_SCHEMA`, `PREFLIGHT_SCHEMA`, `PROTOCOL_REL`, `PROTOCOL_DOC_REL`, `PREFLIGHT_REL`, `PINNED_MODULES`, `EXPECTED_WITHIN_T`; `ProtocolDrift`, `AdmissionRefused`, `LoadedProtocol`; the functions above)
- `tests/phase60/test_protocol.py` - ModuleContractTests (7), ContentTests (19), PinCheckTests (14), VetoTests (5), RoundTripTests (8), DriftTests (12), CommandLineTests (10)
- `tests/phase60/test_admission.py` - ContractTests (2), PreflightWriterTests (15), AdmissionRung1Tests (19), AdmissionBranchTests (18), ReferenceInForceTests (9), CommandLineTests (6)

## Decisions Made

Readings of the plan text that the sources leave open. All fail closed and none moves a locked value; they are listed for the owner or verifier because the protocol is sealed in Plan 60-13 (coverage item D8).

1. **A wrong window count blocks an arm.** The plan's behavior line says "expected-count checks" and its must_haves list "per-arm ok or blocked". SPEC Requirement 8 names missing, empty and unreadable. I treat a record that reads cleanly but holds another count as blocked, because 60-RESEARCH assumption A10 says "preflight catches any change", and Plan 60-13's verifier fails on such a count. The constants `EXPECTED_WITHIN_T` carry the plan's three numbers, and a test proves them equal to `floor(T / dt) + 1` for the grids (0.01, 0.08, and 0.17 from the SPEC background).
2. **One exception type for every unusable protocol.** `ProtocolDrift` is raised for a changed pinned file, and also for a protocol that is absent, untracked, dirty, not JSON, of another schema or missing a field admission reads. The plan names only `ProtocolDrift` and `AdmissionRefused`.
3. **Recorded source digests are checked as well.** The protocol records the SHA-256 of the Phase 59 panels, picks and two-Kepler files, the Stage-0 metadata and the scorer successor record; `load_protocol` compares each with the current file. The plan's list of pins does not include them; the plan's interface section does say the first four are "read here".
4. **Extra protocol sections.** `budget`, `panel`, `probes`, `formula` (the E_formula of 1632, 851 and 4658 from `two_kepler.json`, per the interface note), `decisions` (D-06 to D-11), `r_ref_rule`, `approved_omega_rule`, `normalizer_rule`, `first_result`, `weights`, `divergence`, `cross_check`. Rule texts are paraphrases of CONTEXT, GAPS and the SPEC, each citing its decision or gap id. The runtime rule avoids the identifier of the production runtime resolver because the static guard forbids that name even in a string; it says the resolver "is not consulted".
5. **Admission result extras.** `scorer_context_r_ref` (from the plan's must_have that the scorer's context column always uses the governed artifact) and `answer` and `approved_first_omega_0` in the ruling block.
6. **The uncovered system's data-only Rung 1 waits for the re-measure.** The plan says every `c-` arm needs the ladder taken at the ruling's value, and the ladder is taken only after a passed re-measure, although a data-only arm needs no reference. Admission also does not require `c-r1u-<uncovered>` to finish before the other `c-` arms; the closed sequence `continue-rung2-<uncovered>` orders them.
7. **Command-line tokens beyond the plan's list:** `PROTOCOL-WRITTEN`, `PROTOCOL-REFUSED`, `PREFLIGHT-BLOCKED` (exit 2, and the file is still written because it is the record of the blocked arms) and `PREFLIGHT-REFUSED`. `write` requires an existing preflight of the right schema and an amendment commit that is an ancestor of HEAD, and prints no success token without writing.
8. **`write_protocol` refuses with `HarnessHalt`**, and rewriting before any result is allowed (the plan says `write_json`, an atomic overwrite).

## Deviations from Plan

### Process

**1. Five commits instead of one.** The plan names one commit for Tasks 1 and 2. Both tasks are test-first and Task 1 is a tracer with its own gate, so there are RED and GREEN commits per task, the plan-named subject is on the Task 2 GREEN commit, and one hardening commit follows the mutation pass. Same shape as Plan 60-09.

**2. Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.

**3. The hardening commit body miscounts.** `af81ac24` says the mutation pass "left seven uncaught at first" for the preflight, admission and command line. The exact figures are eight: four weak tests (the preflight file did not have to list its blocked arms; a sweep refusal could come from a missing key rather than from the branch; a re-measured artifact that is clean in git but is not the cited file; the right bytes cited under another path), two defences with no test that reached them (a setting an arm is not entitled to; a ruling that disagrees with the ladder), and two checks that could never trigger and were removed (the ladder state's setting versus the resolved value; a passed re-measure when the ladder is taken). Two earlier misses in the protocol builder (a non-object input, a non-protocol payload to the writer) were fixed before the first GREEN commit. The commit was not amended, to avoid rewriting history.

No Rule 1 bug or Rule 3 blocker arose in the plan's own scope. The additions in Decisions Made (3, 4, 5 and the command-line checks in 7) are Rule 2 hardening inside the plan's own threat model (T-60-12, T-60-16); they are in `304742bf` and `2d78ab9d`.

**Total deviations:** 3 process notes. **Impact on plan:** none; every behavior line and acceptance bullet holds.

### Plan-coverage items

- `PINNED_MODULES` includes `learnability_protocol.py` itself and `learnability_run.py`, which Plans 60-11 and 60-12 edit. A protocol is meant to be written in Plan 60-13 after those edits; any edit to a pinned file after the write is drift. The tests compute expected digests from the files at test time and never hard-code one.
- The plan says not to run the `write`, `preflight` or `admit` subcommands against the real repository, and none was. No file under `evidence/` and no `runs/phase60` exists (checked below).

## TDD Gate Compliance

- **Task 1** (tracer, test-first): RED `108ca2e8`, GREEN `304742bf`. RED run: `python -B -m unittest tests.phase60.test_protocol -v` exited 1 with 70 tests and 70 failures, every one `AssertionError: pinn.verification.learnability_protocol is missing`, no errors (the test reaches the module through a helper). GREEN: 75 tests OK.
- **Task 2** (test-first): RED `763fc8c8`, GREEN `2d78ab9d`. RED run: 66 tests, 66 failures (`write_preflight is missing`), no errors. GREEN: 66 tests OK; the hardening commit raised the file to 69.
- `gsd_run check tdd-red-evidence` parses Node TAP output and does not apply to Python `unittest` output, so the RED evidence is recorded from the retained logs. There is no REFACTOR commit; `af81ac24` is the hardening commit.
- **Mutation evidence.** 80 single-line mutations, one at a time with the targeted tests and a byte-for-byte restore checked by SHA-256 after each: 29 in the builder, writer and loader (rounds of 27 caught, 2 missed, then fixed) and 51 in the preflight, admission and command line (43 caught at first, 8 missed, then fixed). On the final code all 80 are caught (29 in `mutation-task1-rerun.log`, 51 in `mutation-task2-all.log`).

## Verification Results

Logs are retained outside the repository under the session scratchpad `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/10794de1-0511-4472-97f9-694399233015/scratchpad/` (`exec-60-10/` for the plan's own logs; each log starts with its command, HEAD and working directory).

| Command | Result |
|---|---|
| Task 1 verify, `python -B -m unittest tests.phase60.test_protocol -v` (tracer gate, committed tree `304742bf`) | Ran 75 tests, OK, exit 0 (`exec-60-10/task1-tracer-gate.log`) |
| Task 2 verify 1, `... tests.phase60.test_admission tests.phase60.test_protocol tests.phase60.test_static_guards -v` (final code) | Ran 170 tests in 162.850 s, OK, exit 0, no failure strings (`exec-60-10/final-verify1.log`). An earlier run on `2d78ab9d` ran 167 tests in 94.998 s, OK (`task2-verify1.log`) |
| Task 2 verify 2, `... tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests `-v` | Ran 35 tests, OK, exit 0 (`exec-60-10/final-verify2.log`) |
| Full discovery, `python -B -m unittest discover -s tests/phase60 -t . -v` at HEAD `af81ac24` | Ran 842 tests in 876.105 s, OK (skipped=1, the opt-in platform probe), exit 0, 1,116 s elapsed (`scratchpad/phase60_full_discovery_w10.log`) |
| `shasum -a 256 pinn/verification/artifacts/r_ref_stage0.json` | `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`, unchanged; the scorecard JSON (`f4b17688...444b`) and `feasibility_scorecard.py` (`12fcb230...5edfe5`) equal their pre-plan hashes |
| `find .planning/phases/60-single-system-learnability/evidence -type f` | exactly `launch_phase60_arm.py` and `scorer-successor.json` |
| `ls runs/phase60` | does not exist |
| `git diff --quiet 31467d7e HEAD --` the frozen and shared modules, `pinn/training`, `pinn/data`, `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md`, `test_static_guards.py` and the Phase 38, 39 and 59 suites | exit 0 (unchanged); `git diff --name-only 31467d7e HEAD` lists only the three owned files |
| `git status --short -- <owned paths>` | empty |

The discovery ran once, at the final code; it took 876 s of test time against 332 s for 698 tests in Plan 60-09, because the machine was loaded (load average about 1.8 with other sessions running). The 144 new tests account for about 100 to 160 s of that, mostly the nine scenario repositories of the branch tests. It was not repeated.

## Known Stubs

None.

## Threat Flags

None. The module adds no endpoint or authentication path. It reads committed JSON, runs `git` with fixed argument lists, and reads the corpus only through the allowlisted `preflight_records`. Threat register: T-60-12 mitigated (33 module and artifact pins plus 5 recorded sources, `ProtocolDrift` naming the paths, `write_protocol` refusing after a result; `DriftTests`, `RoundTripTests`); T-60-16 mitigated (the branch query, the recorded sweep system, confirmation arm and uncovered system, the ruling value, skip records and the re-measure artifact; `AdmissionBranchTests` over all 42 arms); T-60-01 mitigated (allowlist-only reads, zero test-split opens required, the real corpus kept closed in every writer test); T-60-06 mitigated (redaction guard given the data root, repo-relative paths and digests only, no home or absolute path in the protocol, the preflight or any refusal message); T-60-SC accepted (nothing installed).

## Issues Encountered

None that blocked work. `test_admission` takes 70 to 160 s depending on load because each branch scenario builds a synthetic repository (about 35 file copies and ten commits) once per process, and the matrix tests run all 42 admissions. A first draft of one test asserted that no `runs/` directory exists, which was wrong because the mirror copies `runs/stage0-v23g7-seed42/training_metadata.json`; it now checks `runs/phase60`. The Sequentialthinking MCP named in `CLAUDE.md` and ToolSearch were not available to this executor.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-13 (writes and seals the real protocol and preflight).** Order: `learnability_protocol preflight` (writes `evidence/preflight/records.json` once; `PREFLIGHT-OK` expected with 10 records and 42 arms ok; `PREFLIGHT-BLOCKED` exit 2 if any arm is blocked, with the file still written), commit it; ask the owner the two GAP questions; `learnability_protocol write --amendment-commit <hash of spec(60-03)> [--no-clip-data-only-arms] [--failed-confirmation-pre-answer ...]` (reads the preflight's SHA-256 itself; `PROTOCOL-WRITTEN`); commit; `check` prints `PROTOCOL-OK`. Preflight JSON: `schema`, `plain_language`, `scorecard_sha256`, `t_max`, `data_root_source`, `records{key: {status, split, n_snapshots, n_within_t, dt_out_measured, windowed_sha256, inner_pair, expected_within_t, count_ok}}`, `arms{id: {status, train_key, score_key, beside_key, blocked_by}}`, `blocked_arms` (sorted), `attestation` (the `phase59-files-opened/v1` summary). Protocol top-level keys: `schema`, `plain_language`, `amendment_commit`, `preflight_sha256`, `seed`, `runtime`, `runtime_rule`, `cross_check_runtime`, `scorecard_sha256`, `scorer_sha256`, `scorer_successor`, `module_sha256`, `schedule`, `budget`, `clip`, `timing`, `cadence`, `polish`, `divergence`, `cross_check`, `weights`, `first_result`, `panel`, `g2`, `skip_reasons`, `probes`, `formula`, `decisions`, `r_ref_governed`, `r_ref_rule`, `approved_omega_rule`, `s_h`, `normalizer_stats_sha256`, `normalizer_rule`, `catalog`, `sequences`, `owner_stops`, `readout_notes`. The verifier's checks map to: tracked and clean, `module_sha256` current, `scorecard_sha256` equal to `f4b17688...444b`, `scorer_sha256` equal to the successor record, the amendment commit an ancestor, `preflight_sha256` equal to the committed preflight, and the five recorded sources.
- **Plans 60-11 and 60-12 (record contract, command line, resume).** `load_protocol()` returns `LoadedProtocol(payload, sha256, path)`; `payload["module_sha256"]` is the mapping a resume checkpoint compares. `admit_arm(arm_id, repo_root=None, evidence_root=None, resume=False)` returns the dict listed above and raises `AdmissionRefused` with a one-line reason; the `ruling` block can be wrapped as an object with `answer`, `approved_first_omega_0` and `sha256` and handed to `check_override`. Admission reads committed files only and creates nothing, so `--admit-only` can call it before touching `runs/`. Finish every edit to a pinned file (`learnability_run.py` and the rest of `PINNED_MODULES`) before Plan 60-13 writes the protocol.
- **Open for the owner or verifier:** coverage item D8 (the eight readings under Decisions Made), chiefly 1 (a wrong count blocks), 3 (recorded sources are checked) and 6 (the uncovered Rung 1 waits for the re-measure).

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- The three created files exist on disk and are tracked and clean; commits `108ca2e8`, `304742bf`, `763fc8c8`, `2d78ab9d` and `af81ac24` exist and `git log --grep='(60-10)'` returns exactly them (`git rev-list --count 31467d7e..HEAD` is 5 before this file); the module docstring begins "Phase 60 (SPEC R4)".
- Both tasks' acceptance criteria were re-run on the final code: the verify commands above pass, ContentTests, PinCheckTests, DriftTests, PreflightWriterTests, AdmissionBranchTests and ReferenceInForceTests cover the bullets, and the git status after the tests shows only this plan's files.
- `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md` and `.planning/config.json` were not touched by this plan; the frozen scorecard and the governed R_ref are byte-identical; no real evidence file and no `runs/phase60` directory exists; `.planning/WINDOWS.md` was not appended (no stub, skipped test or unrun verify was left).
