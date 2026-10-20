---
phase: 60-single-system-learnability
plan: 01
subsystem: testing
tags: [learnability-harness, split-allowlist, adam-cosine, lbfgs-polish, plain-git-weights, static-guard]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: frozen scorecard rules, shared scorer, split allowlist, production reference, evidence writer
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: retention-pinned generation-7 checkpoint that the IC13 normalizer is recovered from
provides:
  - "pinn/verification/learnability_{arms,data,losses,run}.py: the data-only arm path (allowlisted read, Stage-0 cosine Adam, frozen polish, both states scored, one exclusive record, plain-git weights)"
  - "tests/phase60 package: tiny gold corpus fixture, 38 run/seam/polish tests, 26 static-guard tests"
  - "The Phase 60 static guard every later plan reruns (discovery by docstring marker)"
affects: [60-02, 60-03, 60-05, 60-08, 60-11, 60-12, 60-23, phase-64-handoff]

actuals:
  tokens: 23019
  tasks: 2
  commits: 2
plan_head_before: ad30cb3125c0028d853681439b6bd79838e53a29

tech-stack:
  added: []
  patterns:
    - "Compose the trainer's functions by bare-name import so mock.patch.object moves the output"
    - "Exclusive record create (O_CREAT|O_EXCL, fsync file and directory); the first completed run is the result"
    - "Plain state-dict weights files (.weights) with a file SHA-256 and a canonical per-tensor digest"
    - "Static guard whose detectors are pure functions of source text, each with an injected-violation self-test"

key-files:
  created:
    - pinn/verification/learnability_arms.py
    - pinn/verification/learnability_data.py
    - pinn/verification/learnability_losses.py
    - pinn/verification/learnability_run.py
    - tests/phase60/__init__.py
    - tests/phase60/_fixtures.py
    - tests/phase60/test_run_short.py
    - tests/phase60/test_static_guards.py
  modified: []

key-decisions:
  - "GAP-60-05 improvement is judged on the full-batch objective evaluated at the iterate each outer call ends with, against the best so far, starting from the objective at the Adam result (LBFGS.step returns the objective at the START of a call, so using its return value would make the baseline coincide with call 1)"
  - "Wall accounting: Adam wall = Adam steps plus budget readings through step B; polish wall = the whole polish phase including its per-call scoring (symmetry with GAP-60-05's steps-plus-readings)"
  - "Fixture budgets are recorded against the frozen scoring cadence but not held to it (whole steps cannot meet 5% of a budget below 20 steps); real arms are refused in this plan"
  - "readout_notes is a list; this plan writes one string (D-04). The per-record hash field is named windowed_sha256"

requirements-completed: [INST-05]

coverage:
  - id: D1
    description: "Allowlisted data seam: key checked before any read, horizon windowing, real normalized IC13, raw-IC13 identity across train/score/beside records"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_run_short.py#DataSeamTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Data-only arm runner: production network, trainer's Huber loss, Stage-0 cosine Adam, frozen L-BFGS polish, both states scored on gold and base grids (INST-05 d)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_run_short.py#ShortRunTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_run_short.py#PolishSemanticsTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Fixture record is created once and never replaced; second run raises FirstResultExists before any optimizer step"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_run_short.py#ShortRunTests.test_second_run_is_refused_before_any_optimizer_step"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_run_short.py#ExclusiveWriterTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Evaluator refuses both fixture weights files with CheckpointOwnershipError before any claim (INST-05 c, base half)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_run_short.py#ShortRunTests.test_evaluator_refuses_both_weights_files_before_any_claim"
        status: pass
    human_judgment: false
  - id: D5
    description: "Plain-git weights: CPU state dict in the runtime dtype, loadable with weights_only=True, file SHA-256 and canonical tensor digest in the record"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_run_short.py#ShortRunTests.test_weights_files_load_with_weights_only_and_match_the_record"
        status: pass
    human_judgment: false
  - id: D6
    description: "Phase 60 static guard (weights_only, forbidden symbols, evaluator imports, swallowed owner stops, training-package imports) with detector self-tests"
    verification:
      - kind: unit
        ref: "tests/phase60/test_static_guards.py"
        status: pass
    human_judgment: false
  - id: D7
    description: "Frozen scorecard bytes and production modules unchanged"
    verification:
      - kind: other
        ref: "git diff --quiet ad30cb31 HEAD -- pinn/architecture_spec.py pinn/network.py pinn/evaluate.py pinn/train.py pinn/verification/__init__.py pinn/verification/feasibility_scorecard.py pinn/verification/artifacts/feasibility_scorecard_v1.json pinn/training"
        status: pass
    human_judgment: false
  - id: D8
    description: "Two readings of GAP-60-05 that the sources leave open: the instant at which a polish call's objective is taken, and whether per-call scoring time counts in the polish wall"
    verification: []
    human_judgment: true
    rationale: "Both change when the polish stops on a real arm; the register's text supports the chosen reading but does not state it. The owner or verifier should confirm before the first real arm."

duration: 55min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 01: Data-only arm runner and static guard Summary

**One data-only fixture arm now runs end to end through the production network, the trainer's own Huber loss, Adam on the Stage-0 cosine and the frozen L-BFGS polish, is scored on the gold and base grids in both states, and leaves one exclusive record plus two plain-git weights files that the evaluator refuses; a Phase 60 static guard covers every later module.**

## Performance

- **Duration:** about 55 min (start time was not captured at spawn; estimated from the first scratch artifact)
- **Started:** 2026-10-19T23:50:00Z (approximate)
- **Completed:** 2026-10-20T00:45:00Z
- **Tasks:** 2 (Task 1 tracer, Task 2 static guard)
- **Files created:** 8 (4 modules, 4 test files); 2,246 lines; no file modified

## Accomplishments

- **Data seam.** `load_arm_data` asks the allowlist about all three keys before any read, windows every record to `t <= 10 + 1e-9`, builds the trainer's data points (`[2u - 1, normalized IC13]`) and refuses records whose raw IC13 or body order differ. `open_real_context` recovers the IC13 normalizer from the retention-pinned checkpoint and halts unless its digest is `77526e53...79f6`.
- **Arm runner.** `run_arm` follows D-04 (Stage-0 cosine, `lr_for_stage(0)`, betas, eps from `OptConfig`), reads the scorer at step 0, every `max(1, floor(f B))` steps and at `B`, then runs the frozen polish with GAP-60-05 semantics, scores Adam and polish on gold and base, and applies the frozen `better_state`.
- **One result.** `record.json` is created with `O_CREAT|O_EXCL`; a second run raises `FirstResultExists` before any optimizer step. `adam.weights` and `polish.weights` are CPU state dicts in the runtime dtype (about 3.04 MiB each in float32), each recorded with its file SHA-256 and a canonical tensor digest (GAP-60-08).
- **Refusal.** `pinn.evaluate.evaluate_run` raises `CheckpointOwnershipError` on both weights files before any claim; no `evaluation-attempt.json` exists afterwards. Arm directories never hold `config.yaml` or `splits.json`.
- **Static guard.** 26 tests; scan set found by docstring marker plus the 11 planned paths, so later modules join without a list edit.
- **Real-corpus smoke (not a committed test).** `open_real_context()` matched the pinned digest. `load_arm_data` on the gold and base records of 1632, 851 and 4658 gave 1,002 to 1,001 gold points and 126 base points, with identical raw IC13. The open attestation counted 262 train opens, 0 test and 0 validation. No real training was run.

## Task Commits

1. **Task 1: Tracer, one data-only fixture arm end to end** - `5e31f46a` (feat)
2. **Task 2: Phase 60 static guard** - `a9cc3c14` (test)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after Task 1: not auto mode (`AUTO_CHAIN` and `AUTO_CFG` false), mode `end-of-phase`, verify has only `<automated>` entries, so both verify commands were re-run on the committed tree (38 tests OK, 35 tests OK) before Task 2 started.

## Files Created/Modified

- `pinn/verification/learnability_arms.py` - `ArmSpec`, `fixture_arm`, arm path rules, `write_record_exclusive`, `FirstResultExists`, shared constants
- `pinn/verification/learnability_data.py` - `DataContext`, `open_real_context`, `fixture_context`, `window`, `load_arm_data`, `HarnessHalt`
- `pinn/verification/learnability_losses.py` - `data_only_loss`, `data_polish_objective` (bare-name imports of `data_huber_loss` and `accumulate_chunked_data_term`)
- `pinn/verification/learnability_run.py` - `run_arm`, `build_arm_network`, `weights_digest`, `save_weights`
- `tests/phase60/_fixtures.py` - `gold_corpus_fixture()` yields `data_root`, `data_root_source`, `manifest_path`, `manifest_sha256`, `blacklist_path`, `allowlist`, `reader`, `stats`, `base_key`, `gold_key`, `test_key`
- `tests/phase60/test_run_short.py` - 38 tests: short run, GAP-60-05 polish rules, gating, data seam, path rules, exclusive writer
- `tests/phase60/test_static_guards.py` - 26 tests: discovery, real scans, detector self-tests

## Decisions Made

- **GAP-60-05 improvement instant.** The objective for a call is taken at the iterate that call ends with. `torch.optim.LBFGS.step` returns the objective at the start of the call, so using it would make call 1 always tie the Adam-result baseline and lag every later comparison by one call. The polish state is the iterate after the last call, or the parameters from before a call with a non-finite objective or parameters.
- **Wall accounting.** Adam wall covers steps plus the budget readings through step B. Polish wall covers the whole polish phase including the per-call scored `E`. The record's per-call `elapsed_seconds` is the quantity compared with 25% of the Adam wall.
- **Stop-reason probe.** To name why the polish stopped without copying the frozen thresholds, the runner calls `polish_should_stop` a second time with a zero polish wall; it is called once per outer call for the decision.
- **Masses and IC13 for scoring.** Scoring takes the float64 reference masses and the float32-resident normalized IC13 widened to float64, so a float32 run sees exactly its training inputs.
- **Co-author trailer.** Commits carry `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The plan's cadence precondition cannot hold at the fixture budget of 10**
- **Found during:** Task 1 (first end-to-end run)
- **Issue:** The plan requires `scoring_cadence_ok(reading_steps, B)` to be True before step 1, and also fixes `B = 10` with readings 0 to 10. The frozen rule allows a gap of at most `0.05 * B = 0.5` steps; whole-step gaps are at least 1, so no integer reading set meets it below `B = 20`.
- **Fix:** The frozen function is still called. A fixture budget is recorded as `cadence_ok: false`, `cadence_enforced: false` and `budget.rule: "fixture"`. Real arms are refused in this plan, so enforcement belongs to the budget driver (Plan 60-08) where `B` is large.
- **Files modified:** `pinn/verification/learnability_run.py`
- **Verification:** `ShortRunTests.test_readings_run_from_step_zero_to_the_budget`
- **Committed in:** `5e31f46a`

**2. [Rule 2 - Missing critical] The runner refuses specs it cannot honor**
- **Found during:** Task 1 (review before commit)
- **Issue:** `ArmSpec` accepts physics loss arms and override provenances, but this runner trains only the data loss at the locked frequency. Such a spec would train data-only while recording another label.
- **Fix:** `HarnessHalt` for `loss_arm != "data_only"`, for `grid_omega` or a non-`locked` provenance, and `build_arm_network` refuses any frequency other than 30.0.
- **Files modified:** `pinn/verification/learnability_run.py`, `tests/phase60/test_run_short.py`
- **Verification:** `FixtureGatingTests`
- **Committed in:** `5e31f46a`

**3. [Rule 2 - Missing critical] Small hardening beyond the plan text**
- `write_record_exclusive` also calls `evidence_io.reject_evidence_root` (as `write_json` does), so a record cannot land in the corpus tree.
- `ArmSpec` validates `run_kind`, `arm_id` and the three key types at construction, not only at path time.
- `load_arm_data` also compares body order (permutation) across the three records.
- The static guard resolves aliased `torch.load` forms and adds a fresh-interpreter check that no Phase 60 module loads `pinn.evaluate` or `pinn.train`.
- **Committed in:** `5e31f46a`, `a9cc3c14`

---

**Total deviations:** 3 auto-fixed (1 Rule 1, 2 Rule 2)
**Impact on plan:** No scope creep beyond hardening the same contracts; nothing outside the owned files changed.

### Process notes

- Task 2 is `tdd="true"` but its deliverable is the test file, so there is no separate production commit. RED evidence is by injection: the detector self-tests fire on violating source, and each rule was also made to fail by injecting a real violation into the actual scan paths (7 injections, all caught, then restored). Task 1's tests were mutation-checked the same way (9 mutations, all caught).
- The generic executor check that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` were not touched; INST-05 is declared by other plans too and is left for the orchestrator.
- `.planning/WINDOWS.md` was not appended: there are no stubs, skipped tests or unrun verifies. The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_run_short tests.phase60.test_static_guards -v` (plan-level) | Ran 64 tests in 8.292s, OK |
| `python -B -m unittest tests.phase39.test_prohibitions` + four named `tests.phase38.test_prohibitions` tests + `tests.phase59.test_static_guards -v` | Ran 50 tests in 7.601s, OK |
| Task 1 verify, re-run as the tracer gate on the committed tree | 38 tests OK; 35 tests OK |
| `git diff --quiet ad30cb31 HEAD -- <frozen and production files>` | exit 0 (unchanged); `load_scorecard()` verified SHA-256 `f4b17688...444b` |
| `git diff --quiet HEAD -- tests/phase39/test_prohibitions.py tests/phase38/test_prohibitions.py` | exit 0 |

Complete logs are retained outside the repository in the session scratchpad. Expensive-command policy: nothing in this plan exceeded 60 s (longest run 9 s), so no command was rerun to reformat output.

## Known Stubs

None. Intentional limits that later plans lift: real arms are refused until the budget rule exists (60-08); the closed catalog and omega overrides (60-23); physics terms (60-05, 60-11); gradient clipping and divergence handling (60-08); resume and signals (60-12); the CPU float64 cross-check.

## Issues Encountered

None that blocked work. The fixture polish usually ends after one outer call by the Adam-wall fraction, so the multi-call counter logic is proved with controlled tests (scripted objectives, a fake clock) rather than by the short run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 60-02 (scorer MPS fix) can proceed; these tests call `score_network` on CPU float64, so the MPS widening is not exercised here.
- Interfaces later plans rely on are as the plan stated: `run_arm(spec, *, context, scorecard, runtime, evidence_root, fixture_budget_steps=None, clock=time.monotonic)`, `write_record_exclusive`, `save_weights`, `ArmSpec.lr_stage` and `clip_stage`, `data_only_loss`. Record fields added here include `budget.cadence_ok`, `budget.cadence_enforced`, per-call polish trace fields (`call`, `objective`, `best_objective`, `improved`, `calls_without_improvement`, `restored`, `E`, `eps_h`, `tier`, `elapsed_seconds`) and `records.<train|score|beside>.windowed_sha256`.
- Open for the owner or verifier: the two GAP-60-05 readings in coverage item D8.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All 8 created files exist on disk; commits `5e31f46a` and `a9cc3c14` exist; the four module docstrings start "Phase 60 (INST-05)".
- Task acceptance criteria re-run against the final code: all pass (logs above).
