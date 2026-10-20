---
phase: 60-single-system-learnability
plan: 23
subsystem: testing
tags: [learnability-harness, override-refusal, closed-arm-catalog, omega-builder, preflight, split-allowlist, open-attestation]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-01's data-only arm runner, ArmSpec and fixture_arm, the allowlisted data seam, the exclusive record writer and the Phase 60 static guard; Plan 60-02's MPS-safe shared scorer; Plan 60-04's Phase 59 verifier that accepts the scorer successor"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard (gate_g2 grid and locked value), the split allowlist and open attestation, the shared scorer"
provides:
  - "learnability_arms: the closed 42-arm catalog, the 51 closed sequence names, the exit codes, OverrideRefused, UnknownArm, resolve_first_omega_0 and check_override"
  - "diagnostic_architecture.build_network_with_first_omega and DiagnosticOmegaError (ArchitectureSpec stays omega-locked)"
  - "learnability_run: first_omega_0 routing in build_arm_network and run_arm (override check before any read or build), grid_omega in the record, run_arm(ruling=)"
  - "learnability_data.preflight_records (SPEC Requirement 8)"
  - "tests/phase60: test_arm_spec, test_refusals, test_data_seam and test_preflight (83 tests)"
affects: [60-06, 60-07, 60-08, 60-09, 60-10, 60-11, 60-12, 60-13, 60-15, 60-16, 60-21]

actuals:
  tokens: 22776
  tasks: 3
  commits: 3
plan_head_before: c7d8d7b7ea0bb0de8559b5ecb17370dc3c19e7dd

tech-stack:
  added: []
  patterns:
    - "A closed catalog built from literals at import, served as a read-only mapping, and pinned by a hand-written table in the test so the test does not repeat the generator"
    - "Authorize first: a pure check on exact values runs before anything else in the runner, and spies prove that nothing is read, built or written before it refuses"
    - "A control process beside every zero-count attestation test, to show the audit hook is live in that process"
    - "A fallback hazard is tested by leaving a readable sibling where a fallback would find it"
    - "Mutation checks with a scratch harness that restores the file and compares its SHA-256 after each mutation"

key-files:
  created:
    - pinn/verification/diagnostic_architecture.py
    - tests/phase60/test_arm_spec.py
    - tests/phase60/test_refusals.py
    - tests/phase60/test_data_seam.py
    - tests/phase60/test_preflight.py
  modified:
    - pinn/verification/learnability_arms.py
    - pinn/verification/learnability_data.py
    - pinn/verification/learnability_run.py
    - tests/phase60/test_run_short.py

key-decisions:
  - "check_override compares exact values only: locked provenance passes at the scorecard locked value and carries no grid_omega; owner_approved passes only at the value a ruling that answers continue names (on or off the grid, GAP-60-11); the two grid provenances pass only on a data-only arm whose grid_omega equals the value and is one of the four scorecard grid values; non-finite, non-positive, bool and string values are refused"
  - "run_arm resolves and checks the setting before runtime resolution, fixture gating, the FirstResultExists test, any data read and any network build, and gains a ruling=None keyword so an owner_approved arm can run once a ruling is supplied"
  - "The three new exception types do not subclass HarnessHalt (learnability_arms must stay light): OverrideRefused is a RuntimeError, UnknownArm and DiagnosticOmegaError are ValueErrors, so launchers map them to EXIT_REFUSED explicitly"
  - "catalog() is a read-only mapping arm_id to ArmSpec in the plan's order; every arm is scored on its system's gold record with the base record of that system beside it, so only the ten records of 60-RESEARCH Finding G are ever named"
  - "preflight_records reports an empty file as empty by catching the IndexError the production admission gate raises for a file with no complete snapshot block, because the reader never returns a zero-snapshot record; the literal zero-count rule is kept as well"
  - "preflight_records adds inner_pair to an ok entry because Plan 60-13 compares the entries with the inner pairs of Finding G"

requirements-completed: [INST-05]

coverage:
  - id: D1
    description: "Closed arm catalog of 42 arms (records, loss, stages, provenance, grid, counted), the 51 closed sequence names, the panel and probe constants and the exit codes; any other id raises UnknownArm"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_arm_spec.py#CatalogTests, SequenceTests, RecordKeyTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "INST-05(e): a first_omega_0 other than 30 is legal only where the scorecard grid, the arm's loss and the committed ruling allow it, and run_arm refuses an unauthorized setting before any read, build or write"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_arm_spec.py#OverrideTests, OverrideBeforeBuildTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_refusals.py#OverrideOrderTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "build_network_with_first_omega: bitwise equal to build_network at 30, only the first layer's omega_0 and the forward differ at other values, ArchitectureSpec and build_network untouched"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_arm_spec.py#BuilderTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "INST-05(c), override half: the evaluator (CheckpointOwnershipError, no evaluation-attempt.json) and the production checkpoint store (NoValidCheckpointError) refuse the weights of an override record at first_omega_0 = 60 as they refuse the locked record's"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_refusals.py#RefusalTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "INST-05(b): a test-split key in any role is refused before any file is opened, an arm never accepts a path, and a process that loads, refuses and preflights reports test_split_opened, blocked_attempts and refused_before_open all 0"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_data_seam.py#TestSplitRefusalTests, AttestationTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "SPEC Requirement 8 preflight function: ok, refused, missing, empty and unreadable per assigned key, window counts from the scorecard horizon, no fallback to another record, no path in the report"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_preflight.py#PreflightTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "The frozen scorecard, the production modules the plan forbids touching, the Phase 59 pinned producers and the Phase 59 evidence are byte-unchanged"
    verification:
      - kind: other
        ref: "git diff --quiet c7d8d7b7 HEAD -- pinn/architecture_spec.py pinn/network.py pinn/evaluate.py pinn/train.py pinn/verification/__init__.py pinn/verification/feasibility_scorecard.py pinn/verification/artifacts/feasibility_scorecard_v1.json (and the pinned producers, Phase 59 and Phase 60 evidence, pinn/data, pinn/training)"
        status: pass
    human_judgment: false
  - id: D8
    description: "Contract details the plan leaves implicit, settled conservatively: a locked-provenance arm that carries a grid_omega is refused; the catalog's rung and path labels for arms the plan lists only by name; every arm scored on gold with the base record beside; OverrideRefused and UnknownArm are not HarnessHalt; an empty file is recognized by the production admission gate's IndexError; inner_pair in an ok preflight entry; run_arm(ruling=)"
    verification: []
    human_judgment: true
    rationale: "Each choice fails closed and moves no locked value, but they set the record and refusal shapes that Plans 60-06 to 60-13 read. The owner or verifier should confirm them before the first real arm, or ask for a gap entry."

duration: 32min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 23: Arm catalog, omega override refusal and assigned-record preflight Summary

**The harness now runs only the 42 arms of a closed catalog, refuses any first-layer frequency but the locked 30 unless the grid, the arm's loss and the committed ruling allow it (before any read or build), builds a non-locked network only through a separate builder that leaves ArchitectureSpec locked, preflights every assigned record without fallback, and its override record's weights are refused by the evaluator and the production checkpoint store.**

## Performance

- **Duration:** about 32 min from the restart at 2026-10-20T02:22:00Z. An earlier session was stopped by a rate limit before any change was made; the coordinator restarted the plan from the top, and the reading done before that stop is not counted.
- **Started:** 2026-10-20T02:22:00Z
- **Completed:** 2026-10-20T02:54:00Z (approximate; the SUMMARY commit follows)
- **Tasks:** 3 (Task 1 tracer, Tasks 2 and 3)
- **Files:** 5 created, 4 modified; 1,954 lines added, 23 removed, no file deleted (`git diff --numstat c7d8d7b7 HEAD`)

## Accomplishments

- **Closed catalog (Task 2).** `catalog()` is a read-only mapping of the 42 ids (r1, g2s, g2c, r2a, r2b, p1, p2b and the c- family) in the plan's order. `arm_spec` accepts exact catalog ids only; `../r1-1632`, `R1-1632`, an absolute path, a `Path`, `None` and every id outside the 42 raise `UnknownArm`. `SEQUENCES` holds the nine named sequences and one `arm:<id>` name per arm (51 names), sweeps in grid order and Rung 2b before 2a. The panel, lap and probe constants and the six exit codes are in place. The expected tables in the test are written out by hand, row by row.
- **Override refusal (Tasks 1 and 2).** `resolve_first_omega_0` and `check_override` compare literal values only. `run_arm` calls them first, so an unauthorized setting raises `OverrideRefused` with `build_arm_network` and `load_arm_data` uncalled and nothing written under the evidence root. The matrix is tested over physics arms, all 16 sweep and confirmation arms at every grid value, locked arms, and owner-approved arms against ruling stand-ins (absent, another value, not `continue`, off the grid at 37.5). The grid and the locked value are read from the scorecard: a stand-in scorecard with another grid changes the outcome.
- **Omega builder (Tasks 1 and 2).** `build_network_with_first_omega` copies the validated `ArchitectureSpec(seed=42)` fields, replaces `first_omega_0` and seeds a local generator as `build_network` does. At 30 every parameter and the forward output are bitwise equal to the production network; at 60 every parameter is still equal, `input_layer.omega_0` is 60 and the forward differs; the global random state is untouched; `ArchitectureSpec(first_omega_0=60.0)` still raises.
- **Override record end to end (Task 1).** A fixture arm at `first_omega_0 = 60` runs through the builder and records `first_omega_0` 60, `grid_omega` 60 and `g2_sweep_override`. Re-scoring its weights with the omega-60 network reproduces the recorded error, and the omega-30 network does not. `evaluate_run` raises `CheckpointOwnershipError` on all four weights files (this record and Plan 60-01's) with no `evaluation-attempt.json`; `TorchSaveCheckpointStore.load_checkpoint` raises `NoValidCheckpointError` on copies of all four inside its root, while a valid seven-key payload loads from the same root.
- **Test-split refusal (Task 3).** A test key in the train, score or beside role, and an unknown key, raise `SplitRefused` with `builtins.open`, `io.open`, `Path.open` and `Path.read_text` recording zero calls. A string or `Path` is never an arm record. In child processes that each own one data root, the open attestation after `load_arm_data` (allowed, then refused) and `preflight_records` reads `test_split_opened` 0, `blocked_attempts` 0, `refused_before_open` 0 and four train opens; a control child shows the hook counts a direct open of the withheld file (`blocked_attempts` 1).
- **Preflight (Task 3).** `preflight_records(keys, context, *, scorecard)` returns `{record_key_str: entry}` with `refused`, `missing`, `empty`, `unreadable` or `ok`. An ok entry carries `split`, `n_snapshots`, `n_within_t` (scorecard horizon), `dt_out_measured`, `inner_pair` and `windowed_sha256`, equal to the digest an arm record carries. A missing gold record whose base sibling is readable never has the sibling probed or read. The report holds no path (a directory placed where a file belongs gives a redacted `IsADirectoryError`).

## Task Commits

1. **Task 1: Tracer, override check, omega builder and routing** - `b913e5a0` (feat)
2. **Task 2: Closed catalog, sequences, exit codes, override matrix, builder identity** - `e15c32eb` (feat)
3. **Task 3: Assigned-record preflight and test-split refusal** - `64c843eb` (feat)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after Task 1: not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, and the verify block holds only an automated command, so it was re-run on the committed tree (75 tests OK) before Task 2 started: "Tracer verified end-to-end - expanding".

## Files Created/Modified

- `pinn/verification/learnability_arms.py` - catalog, `arm_spec`, `SEQUENCES`, constants, exit codes, `OverrideRefused`, `UnknownArm`, `resolve_first_omega_0`, `check_override`; `fixture_arm` now raises `TypeError` for a non-`RecordKey` before reading any attribute
- `pinn/verification/diagnostic_architecture.py` (new) - `build_network_with_first_omega`, `DiagnosticOmegaError`
- `pinn/verification/learnability_run.py` - `build_arm_network` routing, the override check first in `run_arm`, `grid_omega` in the record, `ruling=None`
- `pinn/verification/learnability_data.py` - `preflight_records`
- `tests/phase60/test_arm_spec.py` (new, 47 tests), `test_refusals.py` (new, 11), `test_data_seam.py` (new, 10), `test_preflight.py` (new, 15)
- `tests/phase60/test_run_short.py` - one test replaced (see Deviations)

## Decisions Made

- **Exact values, no tolerance.** `check_override` uses `==` against the scorecard locked value, the four grid values and the ruling's value. `60.0000001`, `59.999999` and `30.0000001` are refused, as are `True`, `"30"`, `nan` and `inf`.
- **Authorize first.** The override check precedes every other gate in `run_arm`, so an illegal setting is reported as `OverrideRefused` even for a real-kind spec that would also be halted for another reason.
- **Locked means locked.** A locked-provenance arm that carries a `grid_omega` is refused. Plan 60-01's runner halted on it; keeping the refusal avoids a record with `first_omega_0` 30 and `grid_omega` 60.
- **A ruling is trusted only for what it says.** The ruling object needs `answer == "continue"` and a finite positive `approved_first_omega_0`. A `go-to-verdict` ruling, a missing value, zero, a negative, a bool or a string authorizes nothing.
- **Catalog labels.** Rung labels are as the plan lists them; path labels follow the five ladder paths: r1 `rung1`, g2s `g2_sweep`, g2c `g2_confirmation`, r2a, r2b, p1 and p2b `g2_passed`, every c- arm `continue`. These mappings are inferred from the names (see D8).
- **Light module.** `learnability_arms` still imports only `evidence_io`, `pinn.constants` and `pinn.data.types`; the exception types are defined there instead of importing `HarnessHalt` from the torch-importing data module.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] A Plan 60-01 test pinned the locked-only behavior this plan removes**
- **Found during:** Task 1 (first RED run)
- **Issue:** `test_run_short.FixtureGatingTests.test_an_omega_override_is_not_routed_by_this_runner` required `build_arm_network(60.0)` and two override specs to raise `HarnessHalt`. The plan reverses the first (routing to the omega builder, the interface note says "30.0 only until this plan"), and its own verify commands run `tests.phase60.test_run_short`, so they could not pass. `tests/phase60/test_run_short.py` is not in the plan's `files_modified`.
- **Fix:** replaced the test with `test_a_spec_with_an_unauthorized_omega_is_refused_before_anything_is_written`, which expects `OverrideRefused` for the two specs and nothing written; the routing itself is covered by `BuilderTests` and `RefusalTests`. The file was added to `GIT_AGENT_OWNED_PATHS` for the Task 1 commit only.
- **Files modified:** `tests/phase60/test_run_short.py`
- **Verification:** 38 tests in the module pass
- **Committed in:** `b913e5a0`
- **Consequence:** Task 3's acceptance bullet that each task commit lists only paths from `files_modified` holds for `e15c32eb` and `64c843eb` but not for `b913e5a0`, which also lists `test_run_short.py`. No Phase 59 docstring marker appears in any touched file.

**2. [Rule 1 - Bug] The plan's preflight procedure cannot label an empty file**
- **Found during:** Task 3 (probing the reader before writing the tests)
- **Issue:** The plan catches `NotAdmitted`, `ValueError` and `OSError` around the read and labels a zero snapshot count `empty`. For a file with no complete snapshot block (zero bytes, blank lines, text without blocks, a partial block) the production admission gate raises `IndexError` ("arrays used as indices must be of integer (or boolean) type"), not `NotAdmitted`, so the plan's handler would let it escape and the read never returns a zero-snapshot record. The plan's own test expects an empty file to report `empty`.
- **Fix:** catch exactly `IndexError` around the load and report `empty`, and keep the literal zero-count rule. Every other unclassified error still propagates (tested for `RuntimeError`, `KeyError`, `TypeError`, `AttributeError`). A file with one complete block is `NotAdmitted` (`insufficient_snapshots`) and reported `unreadable`.
- **Files modified:** `pinn/verification/learnability_data.py`, `tests/phase60/test_preflight.py`
- **Verification:** `PreflightTests.test_a_file_with_no_complete_snapshot_block_is_empty`, `test_a_file_that_cannot_be_parsed_or_admitted_is_unreadable`
- **Committed in:** `64c843eb`
- **Production code is not edited:** `pinn/data/admission.py` is out of scope (see Deferred Issues).

---

**Total deviations:** 2 auto-fixed (1 Rule 1, 1 Rule 3)
**Impact on plan:** Both are needed for the plan's own verify commands and behavior lines to hold. Beyond them, five additions to the plan text are listed under Decisions and D8 (`ruling=` on `run_arm`, `inner_pair`, the locked-arm coherence refusal, the read-only mapping return types, the exception base classes). Nothing outside the owned set changed and no frozen value moved.

### Process notes

- **RED evidence.** Each task's tests were written first and run against the code as it stood: Task 1 `FAILED (failures=8, errors=3)` (the override fixture run halted with `HarnessHalt ... no override is routed`; the order tests failed on the missing `OverrideRefused`), Task 2 `FAILED (failures=34)` (every one a missing symbol; the builder tests already passed because the builder landed in Task 1), Task 3 `FAILED (failures=23)` (15 on the missing `preflight_records`, the rest from a test-helper bug fixed before GREEN: the scorecard file was read inside the open spies). `gsd check tdd-red-evidence` was not used; it parses Node TAP output (Plan 60-04 note). Logs: `$HOME/.cache/3bp-phase60-logs/p60-23-task{1,2,3}-red.log`.
- **Mutation checks, 38 distinct mutations.** Task 1: 6 of 6 caught. Task 2: 16 of 16 caught; one (the builder resetting the global random state) first escaped because an earlier test had already left the generator in the seed-42 state, so that test now sets a known other state first. Task 3: 16 distinct, 15 caught and one equivalent (`NotAdmitted` subclasses `ValueError`, so naming it changes nothing); two escaped the first tests (a missing key probing its base sibling, and a lazy key type check) and the tests were strengthened. The Task 3 commit body says "eighteen"; the exact figures are these. The commit was not amended, to avoid rewriting history. Every mutated file was restored byte-identically (SHA-256 checked each time).
- **Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.
- **Branch assertions.** The generic executor rule that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The cwd-drift and protected-branch assertions ran before each commit.
- **Not touched.** `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` (INST-05 is declared by many plans in this phase, so the shared-ID gate leaves it to the orchestrator), the other uncommitted files in the tree, and `.planning/WINDOWS.md` (no stub, skipped test or unrun verify was left). The Sequentialthinking MCP named in `CLAUDE.md` and `ToolSearch` were not available to this executor.
- **Expensive commands.** None. The longest run was 17 s, so no retained evidence needed reuse.

## Verification Results

| Command | Result |
|---|---|
| Task 1 verify: `tests.phase60.test_refusals test_run_short test_static_guards` | 75 tests OK, 10.7 s; re-run on the committed tree as the tracer gate, 75 OK |
| Task 2 verify: `tests.phase60.test_arm_spec test_refusals test_run_short` | 96 tests OK, 10.3 s |
| Task 3 verify 1 and plan verification 1: the six-module command (`test_data_seam test_preflight test_arm_spec test_refusals test_run_short test_static_guards`) | 147 tests OK, 16.4 s on the committed tree at `64c843eb` |
| Task 3 verify 2 and plan verification 2: `tests.phase39.test_prohibitions` with the four named `tests.phase38.test_prohibitions` tests | 35 tests OK, 1.7 s |
| Plan verification 3: `git diff --quiet HEAD -- pinn/architecture_spec.py pinn/network.py pinn/evaluate.py pinn/train.py pinn/verification/__init__.py pinn/verification/feasibility_scorecard.py pinn/verification/artifacts/feasibility_scorecard_v1.json` | exit 0; also exit 0 against the plan base `c7d8d7b7` |
| `git diff --quiet c7d8d7b7 --` the nine Phase 59 pinned producers, the Phase 59 and Phase 60 evidence trees, `pinn/data`, `pinn/training`, `pinn/loss_catalog.py`, `pinn/physics_residual.py` | exit 0 |
| Extra: `tests.phase59.test_static_guards` (the plan does not rerun it) | 15 tests OK |
| Extra: `tests.phase60.test_mps_lbfgs_smoke` (adjacent, imports `learnability_losses`) | 4 tests OK |
| Retained-log failure strings (`FAILED`, `Error`, `Ran 0 tests`) in the Task 3 and closeout logs | none |
| `git diff --diff-filter=D --name-only HEAD~1 HEAD` after each commit | no deletions |

Complete logs are retained outside the repository under `$HOME/.cache/3bp-phase60-logs/` (`p60-23-*.log`; each starts with the command, HEAD and working directory and ends with `EXIT=`).

## Known Stubs

None.

## Deferred Issues

- **Production admission gate crashes on an empty trajectory.** `pinn/data/admission.py` `evaluate_admission` builds its finite-block mask with `np.array([...])` over the snapshot list, which is a float64 array when the list is empty, then indexes with it, so a file with no complete block raises `IndexError` instead of being rejected as `insufficient_snapshots`. It is pre-existing, outside this plan's files, and not fixed. The preflight classifies exactly that error as `empty` (Deviation 2). If the gate is ever fixed to reject such records with `NotAdmitted`, the preflight would report them as `unreadable` and `test_a_file_with_no_complete_snapshot_block_is_empty` would fail, which flags the change.

## Threat Flags

None. The edits add no endpoint, auth path or corpus access outside the allowlisted reader. Threat register: T-60-01 mitigated (allowlist before any path, `RecordKey`-only inputs, zero-open spies, subprocess attestation); T-60-03 mitigated (evaluator and production store refuse plain and override weights, with a valid-payload control); T-60-05 mitigated (closed catalog, exact keys, 38 mutations including catalog and `arm_spec` ones); T-60-06 mitigated (redacted messages, no path in any entry); T-60-22 mitigated (override check first, exact grid and ruling equality); T-60-SC accepted (no package installed).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-06 (ruling loader).** `check_override` and `resolve_first_omega_0` read `answer` (the literal `continue`) and `approved_first_omega_0` from the ruling object; `Checkpoint4Ruling` as specified has both.
- **Plans 60-07, 60-08, 60-11, 60-12 (launcher, budget driver, physics, resume).** `SEQUENCES`, `catalog()` (iterate `.values()` for specs) and `EXIT_*` are final. `run_arm` begins with the resolve and check and has `ruling=None`; later plans that add `admission=` can feed the same object. `OverrideRefused` and `UnknownArm` are not `HarnessHalt`, so a command line must map them to `EXIT_REFUSED` itself.
- **Plans 60-09 and 60-11 (GATE-04 re-measure, CPU cross-check).** `build_network_with_first_omega(first_omega_0, *, seed, dtype, device)` is the builder to use for a non-locked value.
- **Plans 60-10 and 60-13 (protocol and preflight evidence).** `preflight_records` entries are described in D6 and Accomplishments; the `windowed_sha256` equals the one in an arm record, and `inner_pair` is present for the comparison with Finding G. A blocked key must be reported by the caller; this function only classifies.
- **Open for the owner or verifier:** coverage item D8, the inferred contract details.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All nine created or modified source and test files exist on disk; commits `b913e5a0`, `e15c32eb` and `64c843eb` exist and `git log --grep='(60-23)'` returns exactly them; the 18 retained logs exist.
- Task acceptance criteria re-run against the final tree: Task 1 (refusals on both records and the override record, order before any build or read, the static guard scanning `diagnostic_architecture.py`, production files unchanged) all pass; Task 2 (42 ids and the closed sequence names, the override matrix with spies, builder identity at 30 and 60) all pass; Task 3 (zero open calls, `TypeError` for a string or `Path`, attestation zeros, the six statuses) pass, and the commit-contents bullet passes for two of three task commits (Deviation 1).
- Plan-level verification re-run on the committed tree: 147 and 35 tests OK, frozen files unchanged.
