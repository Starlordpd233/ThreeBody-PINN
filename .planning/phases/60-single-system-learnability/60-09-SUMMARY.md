---
phase: 60-single-system-learnability
plan: 09
subsystem: verification
tags: [gate04, omega-remeasure, r-ref, first-omega-0, d-07, governed-artifact, branch-ladder, tdd, mutation-tests]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-23's build_network_with_first_omega, Plan 60-06's committed-ruling loader, REMEASURE_REL, R_REF_APPROVED_REL and the phase60-gate04-remeasure/v1 reader behind the branch ladder, Plan 60-01's exclusive record writer"
  - phase: 56-contract-amendment-train-free-gate
    provides: "gate04_train_free (run_gate, write_r_ref_artifact, the complete-pass definition) and the governed r_ref_stage0.json"
provides:
  - "gate04_train_free: an optional keyword-only first_omega_0=None on _measure_raw_bin_means, compute_r_ref, evaluate_case and run_gate; the default path is unchanged"
  - "gate04_omega_remeasure: remeasure, main, EXIT_PASS, EXIT_REFUSED, EXIT_BLOCK and REMEASURE_SCHEMA, the continue-path re-measure entry (tokens GATE04-PASS, GATE04-REFUSED, GATE04-BLOCK)"
  - "The continue-path evidence layout under evidence/continue: gate04-evidence.json, r-ref-approved.json (PASS only) and gate04-remeasure.json (written last)"
  - "tests/phase60/test_gate04_remeasure.py (41 tests)"
affects: [60-10, 60-11, 60-13, 60-19]

actuals:
  tokens: 14044
  tasks: 2
  commits: 4
plan_head_before: f1238d9e175f66e61aa5fd69b5bf207fbab444eb

tech-stack:
  added: []
  patterns:
    - "A shared keyword seam with an unchanged default, proven by reproducing the committed bin means and by bitwise equality at the locked value"
    - "A record written last with an exclusive create, after a first-run check that looks at every output, so the first result is never replaced"
    - "Fixture verdicts rebuilt by running the real gate over the committed raw bin means, so no network is built and the verdict is a genuine complete PASS"

key-files:
  created:
    - pinn/verification/gate04_omega_remeasure.py
    - tests/phase60/test_gate04_remeasure.py
  modified:
    - pinn/verification/gate04_train_free.py

key-decisions:
  - "A gate PASS that is not a complete pass (a case set other than the six defaults, or unratified conditions) is recorded as BLOCK with an added reason, because the record schema pairs PASS with complete_pass true"
  - "A missing or uncommitted sweep curve is a refusal before any measurement, because on_grid and equals_confirmed need the committed confirmed value"
  - "The first-run rule refuses when any of the three outputs exists, not only the record"
  - "The record holds exactly the plan's field list; the case evidence is a separate file in the GATE-04 command line's own evidence shape"

patterns-established:
  - "The entry never imports the GATE-04 command line or the arm runner, and the unit tests prove it from the module's AST"
  - "Every refusal is tested through both entries (remeasure raises RemeasureRefused, main prints GATE04-REFUSED and exits 2) and asserts that run_gate was never called and that nothing was written"

requirements-completed: [FEAS-04, FEAS-09]

coverage:
  - id: D1
    description: "gate04_train_free takes an optional keyword-only first_omega_0=None on its four measurement functions; None keeps the locked ArchitectureSpec path (the first default case's raw bin means equal the committed row to rtol 1e-12) and 30.0 is bitwise equal to it; a value builds the network through the omega override builder (D-07, Pitfall 1)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#SeamDefaultTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "remeasure runs from a committed continue ruling to Phase 60 evidence: it validates the setting before any measurement, runs the gate once on the six defaults at the approved setting (CPU, float64) and writes only under evidence/continue, with the record last (D-07, D-11)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#RemeasureTracerTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The governed r_ref_stage0.json is hashed before and after, never written, and a change during the run halts with no record; no terminal-state.json is written and no absolute path enters a written file (GAP-60-10, Pitfall 9, T-60-13, T-60-06)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#RemeasureTracerTests, GovernedReferenceTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "A BLOCK exits 5 with GATE04-BLOCK, records the reasons, writes no reference and leaves the branch ladder at BRANCH-PENDING with GATE-04 BLOCK; a PASS exits 0 and opens the ladder at the approved setting with provenance owner_approved (D-07 stop rule)"
    requirement: "FEAS-09"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#BlockTests, CommandLineTests, BranchLinkTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "A ruling that is not a committed continue, a value that is not finite and positive, and a sweep curve that is missing or uncommitted are each refused before run_gate is called with exit 2 and nothing written; a second run refuses before measuring and never replaces the first record (T-60-04)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#RefusalTests, SecondRunTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "on_grid and equals_confirmed are recorded in every record, and any finite positive setting the ruling names is accepted (GAP-60-11)"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_gate04_remeasure.py#BranchLinkTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "Choices the plan and the gap register leave open: a missing sweep curve refuses instead of reading as 'confirmed nothing'; a gate PASS over another case set is recorded as BLOCK; any existing output stops a new run"
    verification: []
    human_judgment: true
    rationale: "Neither the plan, 60-GAPS.md nor 60-RESEARCH.md says what the entry does in these three cases. Each choice fails closed and none can change a legitimate continue (the branch ladder already requires the committed curve), but the owner or verifier should confirm them"

duration: 25min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 09: The omega seam and the D-07 re-measure entry Summary

**GATE-04 now accepts an optional first_omega_0 with an unchanged default path, and gate04_omega_remeasure runs the D-07 re-measure from the committed checkpoint 4 ruling, writes only evidence/continue, records PASS or BLOCK with on_grid and equals_confirmed, and leaves the governed r_ref_stage0.json byte-identical.**

In plain language: if the owner approves a different first-layer frequency, the physics term's yardstick (R_ref) has to be measured again at that setting and the starting-point check has to pass again before any physics experiment. This plan builds that measurement so that it can only write Phase 60 files. It was not run for real: the real six-case re-measure belongs to the continue path (Plan 60-19).

## Performance

- **Duration:** about 25 min of execution after context loading
- **Started:** 2026-10-20T10:08:26Z
- **Completed:** 2026-10-20T10:33:27Z (production commits; this file follows)
- **Tasks:** 2 (Task 1 tracer and Task 2, both test-first)
- **Files:** 1 modified (`pinn/verification/gate04_train_free.py`, 29 insertions and 9 deletions), 2 created (`pinn/verification/gate04_omega_remeasure.py`, 403 lines; `tests/phase60/test_gate04_remeasure.py`, 807 lines, 41 tests)

## Accomplishments

- **The seam.** `_measure_raw_bin_means`, `compute_r_ref`, `evaluate_case` and `run_gate` each take a keyword-only `first_omega_0=None`, threaded through to the one place the network is built. `None` runs the existing `build_network(ArchitectureSpec(seed=case.seed), ...)` line unchanged. A value builds through `diagnostic_architecture.build_network_with_first_omega`, so `ArchitectureSpec` stays omega-locked. The diff against `f1238d9e` removes exactly nine lines (the four signatures, the model line and four call lines) and adds the keyword, its threading, the branch with a one-line comment, and one import; no default, docstring or command-line behavior changed.
- **Default path proven unchanged.** The first default case's raw bin means, measured for real on the CPU in float64, equal the committed `r_ref_stage0.json` `raw_bin_means[0]` row (the maximum relative difference was 0.0, so the 1e-12 tolerance had room to spare), and the 30.0 path is bitwise equal to the `None` path. Spies prove `None` calls `build_network` with an `ArchitectureSpec` and 60.0 calls the override with 60.0, and another test proves the keyword reaches all twelve measurements of `run_gate` and each of the other three functions.
- **The entry.** `remeasure()` refuses when any output already exists, loads the committed ruling (continue only), validates the value again as finite and positive (because `run_gate` turns every exception into BLOCK), reads the committed sweep curve for `on_grid` and `equals_confirmed`, hashes the governed file, runs `run_gate(DEFAULT_CASES, precision="float64", device="cpu", first_omega_0=value)`, and writes under `evidence/continue/`: `gate04-evidence.json` (the cases and verdict in the GATE-04 command line's own evidence shape), on a complete PASS `r-ref-approved.json` through `write_r_ref_artifact` with a repo-relative `gate_evidence_path`, and last `gate04-remeasure.json` with an exclusive create.
- **The command line.** `main` takes only `--evidence-root` and prints one token line: `GATE04-PASS` (exit 0), `GATE04-REFUSED` (exit 2) or `GATE04-BLOCK` (exit 5, with each reason on its own line). It never calls `gate04_train_free.main`, never writes `terminal-state.json` and never imports the arm runner; the unit tests check the last two from the module's AST.
- **The record.** `phase60-gate04-remeasure/v1` with exactly the plan's fields. `learnability_g2.parse_remeasure` accepts both a PASS and a BLOCK record, and the branch ladder prints `BRANCH-TAKEN: ladder (continue; first_omega_0 120.0; owner_approved)` after a PASS and `BRANCH-PENDING: ladder (GATE-04 BLOCK at 120.0; owner)` after a BLOCK (committed in a synthetic repository built on Plan 60-06's fixtures).

## Task Commits

1. **Task 1 RED: failing seam and omega re-measure tracer tests** - `da946364` (test)
2. **Task 1 GREEN: the first_omega_0 seam and the omega re-measure tracer** - `c9b3f597` (feat)
3. **Task 2 RED: failing command line and second-run refusal tests** - `7f7088b5` (test)
4. **Task 2 GREEN, the plan-named commit: the command line, the first-run rule and the matching docstring** - `b4fd949c` (feat, subject `add the omega seam and the d-07 re-measure entry`)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The plan asks for one commit of Task 2. Both tasks are test-first and Task 1 is a tracer with its own gate, so there are four production commits and the plan-named subject is on the last. Its body names D-07, GAP-60-10 and GAP-60-11 and states that the governed `r_ref_stage0.json` is never written. The trailer names Claude Sonnet 5.5 (the plan text names Opus 5.5; the orchestrator's override was followed).

The tracer feedback gate ran after `c9b3f597`: not auto mode (`_auto_chain_active` false, `workflow.auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, verify carries only `<automated>`, no `gate` attribute. The Task 1 verify (`tests.phase60.test_gate04_remeasure tests.phase57.test_gate_and_evaluation -v`) was run on that tree: 35 tests, OK, no FAILED or Error text. Tracer verified end-to-end, expansion continued.

## Files Created/Modified

- `pinn/verification/gate04_train_free.py` - the optional `first_omega_0` keyword, its threading, the construction branch and its import
- `pinn/verification/gate04_omega_remeasure.py` - `remeasure`, `main`, the exit constants, `RemeasureRefused` and `RemeasureHalt`
- `tests/phase60/test_gate04_remeasure.py` - SeamDefaultTests (6), RemeasureTracerTests (8), CommandLineTests (3), BlockTests (3), RefusalTests (7), NonCanonicalTests (3), SecondRunTests (4), GovernedReferenceTests (1), BranchLinkTests (3), ModuleContractTests (3)

## Decisions Made

- **Complete pass.** The gate's own definition (`gate04_train_free.main`): the six canonical default cases, verdict PASS, no blocking reasons, no unratified conditions. The canonical test checks both the cases asked for and the cases returned, and a test varies each independently.
- **A non-complete PASS is recorded as BLOCK.** `parse_remeasure` forces PASS to be a complete pass and BLOCK not to claim one, so a gate PASS over another case set (reachable only through the Python entry, never the command line) cannot be written as PASS. The record says BLOCK and adds the reason `not a complete pass: ...` to the gate's own reasons.
- **Case evidence.** The evidence file is named `gate04-evidence.json`, uses the `phase56-gate04-cli-evidence/v1` shape that the re-measured artifact's provenance already claims for it, and is built from the command line's own record helpers. Its provenance and configuration carry the setting and repo-relative paths only (no argv, no absolute path). On a BLOCK its `r_ref_path` is null because no reference is written.
- **Repository root.** `main` finds the repository from the evidence root's git top level, as `learnability_g2` does, so the committed ruling is read from the same repository the evidence lives in. With no argument it uses this repository's Phase 60 evidence tree.
- **Docstrings in `gate04_train_free.py` were left alone** so that the diff stays within the permitted lines; the keyword is documented in the new module and in a one-line comment at the branch.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical] A missing or uncommitted sweep curve is refused before any measurement**
- **Found during:** Task 1 (the record needs `equals_confirmed` from "the committed sweep curve's confirmed value")
- **Issue:** The plan names the committed curve as the source and does not say what happens when there is none. Reading a missing curve as "confirmed nothing" would record `equals_confirmed: false` for a reason that is not true.
- **Fix:** `_confirmed_first_omega_0` refuses (exit 2, nothing measured) when `g2/sweep-curve.json` is absent, not tracked and clean, not JSON, or lacks the field. A curve that exists and confirmed nothing (`null`) is accepted and gives `equals_confirmed: false`. A legitimate continue always has the committed curve, because `learnability_g2` only routes a continue after it verifies the outcome, curve and rescue.
- **Files modified:** `pinn/verification/gate04_omega_remeasure.py`
- **Verification:** `RefusalTests.test_a_missing_sweep_curve_is_refused`, `test_an_uncommitted_sweep_curve_is_refused`; mutants M17 and M18 were caught
- **Committed in:** `c9b3f597`

**2. [Rule 2 - Missing critical] The second-run refusal covers every output, and happens before any work**
- **Found during:** Task 2 (the Task 2 RED run showed the Task 1 code failing late)
- **Issue:** The plan's second-run refusal rests on the exclusive record write, which fires after the six-case measurement and after the evidence file and the reference have been rewritten, and a leftover partial output would be silently replaced. Plan 60-19's resume rule (d) says a partial `evidence/continue/` is for the owner to clear.
- **Fix:** `_refuse_existing_outputs` checks the record and both other outputs first and raises `RemeasureRefused`. The exclusive create of the record remains as a second net.
- **Files modified:** `pinn/verification/gate04_omega_remeasure.py`
- **Verification:** `SecondRunTests` (a recorded PASS or BLOCK, and each leftover output alone); mutants M6 and M7 were caught
- **Committed in:** `b4fd949c`

---

**Total deviations:** 2 auto-fixed (2 Rule 2)
**Impact on plan:** Both are fail-closed input checks. No frozen value, schema field, threshold or default changed, and a legitimate continue is unaffected. Both are also listed as coverage item D7 for confirmation.

### Plan-coverage items

- **Command 2 was not run as a separate invocation.** `tests.phase60.test_gate04_remeasure` (41 tests), `tests.phase60.test_g2` (146) and `tests.phase60.test_static_guards` (26), 213 tests in all, ran inside the single full discovery on identical file digests and all passed. Re-running `test_g2` (about four minutes) would only have proved the same fact again, so the discovery log is cited instead.
- **One extra single-case measurement outside the suite.** Before writing the test I ran one default-path measurement of the first case in a scratch script (CPU, float64, `first_omega_0` None, about 18 s) to check that the committed row reproduces to 1e-12 on this machine. It is the same operation as the first SeamDefaultTests measurement. No six-case run was ever made, and the test runs that include SeamDefaultTests (four, each with its two measurements) are the only other real measurements.
- **The plan's baseline hash.** The plan and acceptance criteria cite HEAD `0d0ec297`; this execution started at `f1238d9e`. The governed artifact is byte-identical to the starting HEAD (SHA-256 `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`, git blob `f78084543dbb4e42d6c56bc7922782cf8f61a8af`).
- **Task 1's behavior list covers only `remeasure`.** `main` and the up-front refusal were left to Task 2 so that its RED run was real; the Task 1 action text describes the whole module and the end state matches it.
- **`.planning/WINDOWS.md` was not appended.** There is no stub, skipped test or unrun verify, and the file is outside this plan's owned paths.

## TDD Gate Compliance

- **Task 1** (tracer, test-first): RED `da946364`, GREEN `c9b3f597`. RED run: `python -B -m unittest tests.phase60.test_gate04_remeasure` exited 1 with 14 tests and 13 failures, all assertions and no errors: 5 report that the four gate functions lack a keyword-only `first_omega_0` defaulting to None, 8 that `pinn.verification.gate04_omega_remeasure` does not exist yet. The one pass, the check that the committed rows reproduce the committed complete PASS through the existing gate code, is a characterization test and doubles as the check of the fixture verdict. GREEN run: 14 tests OK (35 with `tests.phase57.test_gate_and_evaluation`).
- **Task 2** (test-first): RED `7f7088b5`, GREEN `b4fd949c`. RED run: 27 tests in the eight new classes, exit 1, 29 failures and no errors (a second-run test that first errored on a late exception was changed to assert the exception type, so RED reads as a failure): 25 report that the module has no `main`, 1 that `main` is not exported, 2 that a leftover output without a record is not refused, 1 that a second run is not refused up front. The other 9 tests (non-canonical case sets, unratified conditions, the governed-file halt, the branch link, the docstring marker and the import checks) already passed because Task 1 delivered them; they are characterization tests, proven by mutation below. GREEN run: 35 tests in those classes plus the tracer class, OK.
- **Mutation evidence.** 32 single-line mutations were applied one at a time, each followed by the targeted fast tests and a byte-for-byte restore checked by SHA-256: 7 of the seam (inverted branch, override never used, wrong omega to the builder, and the keyword dropped at each of four threading sites) and 25 of the module (continue not required, value check removed, either canonical-set condition removed, unratified ignored, reference written without a complete pass, first-run check removed or reduced to the record, governed-hash check removed, record verdict following the gate, block or refused exit code or token changed, gate run without the setting or at float32, absolute paths in the record or artifact, a terminal-state file written, ruling errors escaping, the curve checks removed, grid facts swapped, a wrong ruling hash, a reference path named on a BLOCK). All 32 were caught. One mutation that would have redirected the reference write to the governed path was deliberately not run, because it would have overwritten the real file.
- `gsd_run check tdd-red-evidence` parses Node TAP output and does not apply to Python `unittest` output, so the RED evidence is recorded here from the retained logs. There is no REFACTOR commit.

## Verification Results

Logs are retained outside the repository under `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/10794de1-0511-4472-97f9-694399233015/scratchpad/`.

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_gate04_remeasure tests.phase57.test_gate_and_evaluation -v` | Ran 62 tests in 40.775 s, OK, exit 0, no FAILED or Error text (`final-cmd1.log`) |
| `python -B -m unittest tests.phase60.test_gate04_remeasure tests.phase60.test_g2 tests.phase60.test_static_guards -v` | not run separately; 213 tests (41 + 146 + 26) ran inside the discovery below, all ok (see Plan-coverage items) |
| `python -B -m unittest tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests `-v` | Ran 35 tests in 1.646 s, OK, exit 0 (`final-cmd3.log`) |
| `python -B -m unittest discover -s tests/phase60 -t . -v` | Ran 698 tests in 332.201 s, OK (skipped=1, the opt-in platform probe), exit 0, 334 s elapsed, no FAILED or Error text (`phase60_full_discovery.log`) |
| `python -B -m unittest tests.phase60.test_static_guards` | Ran 26 tests, OK (`final-static.log`) |
| `shasum -a 256 pinn/verification/artifacts/r_ref_stage0.json` and `find . -name terminal-state.json -not -path './.git/*'` | `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`, unchanged; only the Phase 57 file exists; `.planning/phases/60-single-system-learnability/evidence/continue` does not exist |

The full discovery ran once, on the three changed files at digests `cc6504a7985f034f3aa7651c6250c6b58a3006b87bccd93af15324fc451c0849` (`gate04_train_free.py`), `81ade6f2821fb40928eeaf1d6185d8ad51de871a587c4115c806ca111b301318` (`gate04_omega_remeasure.py`) and `e440ea3faa2dda14fea4e6a605d600abf87591be4dae75ae7e5d97653328775b` (`test_gate04_remeasure.py`), which are the digests committed in `b4fd949c` (checked by `shasum -c` before and after the run) and was not repeated. The count rose from 657 (Plan 60-08) to 698, the 41 new tests.

## Known Stubs

None.

## Issues Encountered

None that blocked work. A scratch script run by path did not find the `pinn` package (it needed `PYTHONPATH`), and the first draft of the second-run RED test errored instead of failing; both were corrected before they mattered.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-10** can read the continue-path reference in force from the record: `r_ref_artifact.path` and `.sha256`, and `r_ref` for the value. `r-ref-approved.json` loads under the trainer's own `load_frozen_r_ref_artifact`.
- **Plan 60-19** runs `python -B -m pinn.verification.gate04_omega_remeasure` with no arguments, after `learnability_g2 branch continue-gate` prints BRANCH-TAKEN. It needs the committed ruling to be clean, `g2/sweep-curve.json` committed, and nothing under `evidence/continue/`. The first token line begins `GATE04-PASS` or `GATE04-BLOCK` as 60-19's grep expects. One single-case measurement took about 18 s here, so the twelve measurements of the gate should take of the order of four minutes on this CPU (an estimate; it has not been run).
- **Open for the owner or verifier:** coverage item D7 (the three fail-closed choices above).

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- Both created files exist (`gate04_omega_remeasure.py`, `test_gate04_remeasure.py`); commits `da946364`, `c9b3f597`, `7f7088b5` and `b4fd949c` exist; `git rev-list --count f1238d9e..HEAD` was 4 before this file.
- Every task's acceptance criteria were re-run on the committed code: the seam and tracer tests (command 1, 62 tests OK), the block, refusal and ladder tests (inside the 698-test discovery), the seam diff (exactly nine removed lines, all signatures, the model line and the threaded calls), and the governed SHA-256 (unchanged).
- The plan-level verification holds: `test_gate04_remeasure`, `test_g2`, `test_gate_and_evaluation` and the Phase 60 static guard pass, the prohibition suites pass, and the governed `r_ref_stage0.json` is byte-identical.
- `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md` and `.planning/config.json` were not touched by this plan, no `terminal-state.json` or `evidence/continue` exists, and `git status --short` for the three owned source paths is empty.
