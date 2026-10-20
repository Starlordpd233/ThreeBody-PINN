---
phase: 60-single-system-learnability
plan: 11
subsystem: verification
tags: [learnability-harness, physics-arms, frozen-monitor, lbfgs-handoff, cpu-float64-cross-check, counting-rule, record-validator, tdd]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-05's physics Adam step, frozen monitor log and frozen-handoff polish objective; Plan 60-08's timing run, budget driver, ratified schedule, clipper and owner-stop writer; Plan 60-10's admit_arm contract, protocol facts and drift pins"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard functions tier_of, counts and better_state, and the two-Kepler singles rows every counted arm is compared with"

provides:
  - "pinn/verification/learnability_run.py: physics arms (Rung 2a, Rung 2b and probe Rung-2b), cross_check_state, CrossCheckDisagreement, the counting rule with probes excluded, build_real_record, validate_record and REQUIRED_REAL_FIELDS (54 dotted fields)"
  - "tests/phase60/test_physics_arm.py (21 tests), tests/phase60/test_cross_check.py (15 tests) and tests/phase60/test_protocol_records.py (33 tests); test_budget_driver.py and test_run_short.py updated where this plan supersedes their premises"

affects: [60-12, 60-13, 60-14, 60-16, 60-20, 60-21]

actuals:
  tokens: 30546
  tasks: 3
  commits: 1
  plan_head_before: 58920e96cf728a8dafaa9bafd7673e0c324bd5ed

tech-stack:
  added: []
  patterns:
    - "One stepper interface, chosen by the arm's loss and shared by the timing run and the arm, so the timed configuration cannot drift from the trained one"
    - "A frozen handoff object the polish closure reads, so no closure can redraw the rows or recompute the causal weights"
    - "The cross-check builds its own CPU float64 network at the arm's first_omega_0, so the official build path keeps exactly the two calls the timing-parity test pins"
    - "Record provenance comes from the admission and the loaded protocol, never from the run's own mapping"
    - "One dotted-path required-field list behind one presence loop, so a new required field is one line"
    - "Two generators of the same seed: a throwaway one for the timing run and the arm's own, with the frozen monitor set drawn from it before step 1"

key-files:
  created:
    - tests/phase60/test_physics_arm.py
    - tests/phase60/test_cross_check.py
    - tests/phase60/test_protocol_records.py
  modified:
    - pinn/verification/learnability_run.py
    - tests/phase60/test_budget_driver.py
    - tests/phase60/test_run_short.py

key-decisions:
  - "A real arm without an admission keeps the Plan 60-08 record shape; the strict build_real_record and validate_record path is the admitted one, which is the only path Plan 60-12's command line uses. The alternative was to refuse every unadmitted real arm, which would fail the retained RealArmBudgetTests"
  - "fixture_r_ref is a new keyword (default None) and a fixture arm with a physics term must pass it explicitly, because the plan says fixtures pass r_ref explicitly but names no keyword for it"
  - "The probe formula field keys on the arm's rung (probe-1, probe-2b), not on counted alone, so a Plan 60-01 fixture arm keeps its fixture note while a probe-shaped arm records the ratified not-applicable string"
  - "epsilon_H stays None where the stage's energy weight is zero rather than an invented number; a stage whose energy weight is above zero refuses to run without the admission's S_H"
  - "counts is called once per scored state on the official tier and E, once per state inside the CPU cross-check (the compared boolean), and once on the result, which is five calls for a counted two-state arm"
  - "A clipped-step count, a timing-run draw and a cross-check score are all observations; none of them can change the official tier, which is why the CPU score never reaches better_state"

patterns-established:
  - "Guard the write, not the caller: run_arm cannot create record.json until validate_record has accepted the assembled payload"
  - "A stop writes its own record before it re-raises, and every handler that names OwnerRouted ends in a bare raise"

requirements-completed: [INST-05, FEAS-03, FEAS-04, FEAS-09]

coverage:
  - id: D1
    description: "A physics arm runs end to end on the trainer's memory-bounded step: the ratified Adam schedule and the PHYS-05 warmup over its own budget, a fresh 4,096-row stratified collocation draw from its seed-42 generator on every step, and both states scored (D-01, Rung 2a never evaluating the data term)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_physics_arm.py#PhysicsTracerTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "D-06: one frozen monitor set is drawn before step 1 and the seven statistics are logged at exactly the budget-rule readings; the runner never names a front index, so no value of it can branch"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_physics_arm.py#PhysicsTracerTests.test_the_monitor_log_is_recorded_at_exactly_the_reading_steps"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_physics_arm.py#PhysicsTracerTests.test_nothing_in_the_runner_reads_a_front_index_to_branch"
        status: pass
    human_judgment: false
  - id: D3
    description: "GAP-60-05 and 57-RULING.md:112-124: the handoff freezes the rows, the pass-1 causal weights, the bin counts and the loss weights once, and the polish redraws nothing"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_physics_arm.py#PhysicsTracerTests.test_the_polish_redraws_nothing_after_the_handoff"
        status: pass
    human_judgment: false
  - id: D4
    description: "D-08, GAP-60-10 and GAP-60-12: the record names the Stage-0 reference in force with its path, SHA-256 and the ratified note, the governed scorer-context reference, and the persisted S_H and eps_H for the probe Rung-2b arms, with the D-05 readout note"
    requirement: "FEAS-09"
    verification:
      - kind: unit
        ref: "tests/phase60/test_physics_arm.py#PhysicsTracerTests.test_the_reference_in_force_and_the_scorer_context_are_recorded"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_protocol_records.py#ProbeRecordTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "GAP-60-07 and SPEC Requirement 3: both scored states are re-scored on the CPU in float64 from the saved weights on the same float32-rounded IC13; a tier or counts difference writes owner-stop.json (stage cross_check) and raises CrossCheckDisagreement; better_state never sees the CPU score and the better of the two is never taken"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_cross_check.py#AgreementTests, DisagreementTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "SPEC Requirement 7: a counted arm compares its position error with the committed two-Kepler rows through the frozen counts (strictly less, Tier 1 eligible with a non-finite eps_H); a missing formula writes owner-stop.json (stage counts) and re-raises the same OwnerRouted; a probe calls counts zero times and records not applicable: no hierarchical split"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_cross_check.py#CountsTests, ProbeCountsTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "SPEC Requirements 4 and 5 and D-10: REQUIRED_REAL_FIELDS lists 54 dotted fields, each one proven by removal; literals (seed 42, MPS float32, the harness schema, diagnostic, run_kind, the weights file names, the zero attestation counters, the tier range, the better state, both horizons, the sentinels) and the continue-arm ruling block are checked; build_real_record assembles provenance from the admission and the protocol; run_arm writes no invalid record"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_protocol_records.py#ValidatorTests, RealRecordAssemblyTests, WriteStepTests"
        status: pass
    human_judgment: false
  - id: D8
    description: "GAP-60-08 and D-10: the two .weights files load with weights_only=True, hold CPU float32 tensors, match the record's file SHA-256 and tensor digest, and no ignored extension (.pt, .pth, .npz, .npy, .ckpt, .pkl) is written"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_protocol_records.py#WeightsFormatTests"
        status: pass
    human_judgment: false
  - id: D9
    description: "Readings of the plan text that the sources leave open (listed under Decisions Made): the unadmitted real-arm record shape, the fixture_r_ref keyword, the probe formula keyed on the rung, the inert epsilon_H and the five counts calls"
    verification: []
    human_judgment: true
    rationale: "Each fails closed and moves no locked value, but together they fix the shapes Plan 60-12's command line and Plan 60-13's verifier read, so the owner or verifier should confirm them before the protocol is sealed"
  - id: D10
    description: "Two Plan 60-01 and 60-08 tests were rewritten in place because their premises are superseded here: the data-only-only gate and the single OwnerRouted handler"
    verification: []
    human_judgment: true
    rationale: "The rewritten tests pin the new rules (a physics fixture arm needs its reference; every owner-stop handler re-raises) rather than deleting coverage, but they live outside the plan's files_modified list"

duration: 70min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 11: Physics arms, the CPU float64 cross-check and the validated real-arm record Summary

**Physics arms now train on the trainer's own memory-bounded step with the PHYS-05 warmup, one frozen monitor set logged at every budget reading and a handoff frozen for the whole polish; every scored state is re-scored on the CPU in float64 with a disagreement stopping for the owner, counted arms compare against the committed two-Kepler formula while probes never count, and no real-arm record is written until it carries all 54 required fields.**

In plain language: the harness can now learn from the equations of motion the same way the trainer does, it double-checks every official score in higher precision instead of trusting one device, and it refuses to save a result that is missing any fingerprint SPEC Requirements 4 and 5 name.

## Performance

- **Duration:** about 70 min of wall clock (context loading and implementation first, then the retained verification logs from 16:52Z to 17:20Z; the full discovery took 11 of those minutes).
- **Tasks:** 3 (Task 1 tracer, Tasks 2 and 3 test-first).
- **Files:** 3 created (`test_physics_arm.py` 490 lines, `test_cross_check.py` 351 lines, `test_protocol_records.py` 732 lines) and 3 modified (`learnability_run.py` +1,267 net lines, and two existing tests rewritten where this plan supersedes them).

## Accomplishments

- **Physics arms (Tasks 1 and 2).** `run_arm` no longer refuses a loss arm with a physics term. It builds an arm stream with `np.random.default_rng(SEED)` after the timing run (the timing run keeps its own throwaway generator), draws the frozen monitor set *first*, then draws a fresh 16-bin stratified collocation set on every Adam step and calls `physics_adam_step` with `ScheduledWeights.current(step)` over the arm's own budget. `physics_ic` passes `data_points=None`, so Rung 2a never evaluates a data term. `h0` and `l0` come from the training record's own `true_r0`/`true_v0` through `loss_catalog._matched_plummer_hamiltonian` and `_angular_momentum`; `eps_h` is the admission's `1e-4 x S_H` and stays `None` where the stage's energy weight is zero.
- **The frozen monitor (D-06).** `frozen_monitor_log` runs at every budget reading, never per step, and its seven statistics plus the step go into `record.monitor_log`. The runner never names `front_idx` (checked by a test that reads the module source), so nothing can branch on it.
- **The frozen handoff (GAP-60-05).** At the handoff the code calls `scheduled.freeze()`, takes `scheduled.current(0)`, draws one row set, runs pass 1 once, and hands the rows, `w_n`, the bin counts and the `LossWeights` to `physics_polish_objective` through a closure. A recorder test shows one draw before the monitor, one per Adam step, exactly one at the handoff and none after the first polish call.
- **The reference and the scale (D-08, GAP-60-10, GAP-60-12).** `record.r_ref` is `{value, path, sha256, note "Stage-0 reference in force, applied unchanged"}` from the admission (a fixture passes `fixture_r_ref` explicitly), `record.scorer_context_r_ref` is the governed artifact, and `record.s_h` carries the persisted `S_H`/`eps_H` for the probe Rung-2b arms, with the D-05 from-scratch note in `readout_notes`.
- **The CPU float64 cross-check (GAP-60-07).** `cross_check_state` builds a float64 CPU network at the arm's `first_omega_0`, moves each saved tensor to the CPU and then widens it, feeds the float32-rounded normalized IC13 widened back to float64, and scores the gold view. `run_arm` runs it after each state's weights are written. A tier or counts difference writes `owner-stop.json` (stage `cross_check`, both scores and both counts) and raises `CrossCheckDisagreement`; `better_state` is never called with a CPU score, which a spy proves by seeing zero calls.
- **Counting (SPEC Requirement 7).** Counted arms read `E_formula` from the committed Phase 59 `two_kepler.json` (recording its SHA-256) and call the frozen `counts` on each scored state and on the result. A missing formula goes through the module's one owner-routed clause, which writes `owner-stop.json` (stage `counts`) and re-raises the same exception object. A probe calls `counts` zero times and records `not applicable: no hierarchical split`.
- **The record contract (SPEC Requirements 4 and 5, D-10).** `REQUIRED_REAL_FIELDS` holds 54 dotted paths; `validate_record` checks presence, then the literals and types (seed 42, MPS float32, schema, diagnostic, `run_kind`, 64-hex digests, the two weights file names, zero attestation counters, a tier in 0..3, `adam`/`polish`, both horizons, non-finite values only as the JSON sentinels, the formula rule, the physics fields and the continue ruling). `build_real_record` fills versions, code, `config_sha256`, the four protocol digests, the attestation, the normalizer digest and `wall.hours` from the admission, the protocol and the context. `run_arm` writes nothing it has not validated.
- **Weights (GAP-60-08).** A fixture arm run on MPS float32 writes only `adam.weights`, `polish.weights` and `record.json`; both files load with `weights_only=True`, hold CPU float32 tensors, and match the record's file hash and tensor digest.

## Task Commits

1. **Tasks 1-3, the plan-named commit: the completed runner and its three test modules** - `b5f47fac` (feat, subject `complete physics arms, cross-check and records`; its body names D-01, D-05, D-06, D-08, D-10, GAP-60-05, GAP-60-07, GAP-60-10 and GAP-60-12)
2. **Plan metadata:** the SUMMARY commit that follows this file (docs).

The plan asks for one code commit after all three tasks, and that is what this plan has: no RED/GREEN split was committed (see TDD Gate Compliance for the retained RED evidence).

## Files Created/Modified

- `pinn/verification/learnability_run.py` - physics steppers and inputs, the physics-aware timing run and polish, `_official_counts`, `cross_check_state` and `CrossCheckDisagreement`, `formula_reference`, `governed_context_reference`, `REQUIRED_REAL_FIELDS`, `validate_record`, `build_real_record`, and the reworked `run_arm` with the `fixture_n_slots`, `fixture_r_ref`, `admission` and `protocol` keywords.
- `tests/phase60/test_physics_arm.py` - `PhysicsTracerTests` (two fixture physics arms, monitor log, handoff, data-term gating), `FixtureKnobTests`, `ModuleContractTests`.
- `tests/phase60/test_cross_check.py` - `AgreementTests`, `DisagreementTests`, `CountsTests`, `ProbeCountsTests`.
- `tests/phase60/test_protocol_records.py` - `ValidatorTests`, `RealRecordAssemblyTests`, `WriteStepTests`, `ProbeRecordTests`, `WeightsFormatTests`.
- `tests/phase60/test_run_short.py` - the Plan 60-01 "only the data-only loss arm" test now asserts the new rule (a fixture physics arm needs `fixture_r_ref`).
- `tests/phase60/test_budget_driver.py` - the Plan 60-08 "only handler" test now asserts that every owner-routed handler re-raises.

## Decisions Made

Readings of the plan text that its sources leave open. Each fails closed and none moves a locked value; they are listed for the owner or verifier because Plan 60-13 seals the protocol around them (coverage items D9 and D10).

1. **The strict real-record path is the admitted one.** The plan says every real-arm record cites the protocol, and also that `RealArmBudgetTests` (Plan 60-08) keeps running a `run_kind="real"` arm with no admission. Those cannot both hold if an unadmitted real arm is refused, so `run_arm` engages `build_real_record` + `validate_record` when an admission and a protocol are supplied, and otherwise keeps the Plan 60-08 record shape. Every real arm Plan 60-12 launches is admitted, so the production path is the strict one. A real arm given only one of the two is refused, and the admitted path refuses any runtime other than MPS float32.
2. **`fixture_r_ref`.** The plan says "fixtures pass r_ref explicitly" but names no keyword; the artifacts list names only `fixture_n_slots` and `fixture_timing_steps`. `fixture_r_ref=None` defaults to "not supplied", and a fixture arm with a physics term without it is refused before anything is read. This is the only reason the Plan 60-01 gate test could be rewritten rather than deleted.
3. **The probe formula keys on the rung.** `counted` alone would turn every Plan 60-01 fixture arm's `not applicable: fixture record` into the probe string. An arm whose rung starts with `probe` records `not applicable: no hierarchical split`; a fixture arm that is not a probe keeps the fixture note; any other uncounted real arm records the probe string.
4. **No invented energy scale.** A stage below 2 has `lambda_E^max = 0`, so the energy term is never evaluated and `eps_h` stays `None`; a stage whose weight is above zero refuses to run without the admission's `S_H` block.
5. **Five `counts` calls for a counted two-state arm.** One per scored state on the official tier and `E`, one per state inside the CPU cross-check (the boolean being compared), and one on the result. Reading "calls counts on both states and on the result" as three calls would undercount the cross-check comparison.
6. **`module_sha256` is the protocol's pin mapping.** The record carries the mapping the protocol pins (path to digest) rather than a single digest over it, so a verifier can name the changed module.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Two existing tests encode premises this plan removes**
- **Found during:** Task 1 and Task 2 implementation
- **Issue:** `test_run_short::test_only_the_data_only_loss_arm_is_trained_here` asserts that `run_arm` refuses a physics loss arm, which Task 1 removes; `test_budget_driver::test_the_only_handler_for_an_owner_stop_re_raises` asserts exactly one `except OwnerRouted` in the module, which Task 2 must add. Both files are outside the plan's `files_modified`, but leaving them would fail the plan's own full-discovery verify.
- **Fix:** Both were rewritten in place, not deleted: the first now pins the new gate (a fixture physics arm needs `fixture_r_ref`, nothing written), the second pins the rule that every owner-routed handler ends in a bare raise and names both handlers.
- **Files modified:** `tests/phase60/test_run_short.py`, `tests/phase60/test_budget_driver.py`
- **Verification:** both modules pass in the full discovery
- **Committed in:** `b5f47fac`

**2. [Rule 2 - Missing critical] The cross-check builds its own network**
- **Found during:** Task 2
- **Issue:** Routing the CPU float64 network through `build_arm_network` gave the timing-parity test four builder calls where it pins two, and mixed the official and diagnostic build paths.
- **Fix:** `_cross_check_network` builds float64 on the CPU at the arm's `first_omega_0` through `build_network` or `build_network_with_first_omega`, which is exactly what GAP-60-07 names.
- **Files modified:** `pinn/verification/learnability_run.py`
- **Verification:** `tests/phase60/test_schedule.py#TimingParityTests`
- **Committed in:** `b5f47fac`

### Process

**3. One code commit, no separate RED commits.** The plan names a single commit after all three tasks; Tasks 2 and 3 carry `tdd="true"`, so their RED evidence was retained from a log instead of committed (below). **Impact:** none on behaviour.

**4. Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.

**Total deviations:** 2 auto-fixed (one Rule 3, one Rule 2) and 2 process notes. **Impact on plan:** no frozen value, threshold, catalog entry or schema field changed.

### Plan-coverage items

- The plan's "no test-only runtime switch in the real path" is enforced where it matters (the admitted path refuses a non-MPS runtime) but a real arm with no admission can still run at another runtime: that is the Plan 60-08 budget test, and its record never reaches `validate_record` because the strict path is not engaged (decision 1).
- Task 3's `build_real_record` takes the reference in force and `S_H` from the admission rather than from `run_parts`, so the probe and continue records cannot carry a reference the admission did not authorize.

## TDD Gate Compliance

- **Task 1** is a tracer, not test-first: its tests landed with its code in `b5f47fac`, and its `<verify>` was re-run alone on the committed tree as the tracer gate (21 tests, OK, exit 0, 41 s). Not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, and the verify holds only an automated command, so it was re-run and expansion continued: "Tracer verified end-to-end - expanding".
- **Tasks 2 and 3** carry `tdd="true"`. RED evidence is retained at `/tmp/gsd-60-11/tdd-red.log`: both new modules were run against `HEAD`'s `learnability_run.py` (SHA-256 `0fbcb160...4d18`, restored byte-for-byte afterwards and re-checked against the new file's SHA-256 `dad7e218...0a55`). The run reports `Ran 2 tests`, `FAILED (errors=2)`: `ImportError: cannot import name 'CrossCheckDisagreement'` and `ImportError: cannot import name 'REQUIRED_REAL_FIELDS'`, i.e. the module under test is missing, which is the honest RED for a module whose new symbols do not exist yet. GREEN is the same two modules at `b5f47fac` (15 and 33 tests, OK).
- `gsd_run check tdd-red-evidence` parses Node TAP output and does not apply to Python `unittest` output, so the RED evidence is recorded from the retained log, as in Plans 60-05, 60-08 and 60-10.
- No mutation pass was run: this plan's tests are behavioural proofs over real fixture runs and pure assemblers, and the plan does not ask for one.

## Verification Results

Logs are retained outside the repository under `/tmp/gsd-60-11/`. Each log starts with its command, HEAD, working directory and start time and ends with its exit status and elapsed seconds.

| Command | Result |
|---|---|
| Task 1 verify, `python -B -m unittest tests.phase60.test_physics_arm -v` (committed tree, tracer gate) | Ran 21 tests in 39.770 s, OK, exit 0, 41 s (`task1-verify.log`) |
| Task 2 verify, `python -B -m unittest tests.phase60.test_cross_check tests.phase60.test_static_guards -v` | Ran 41 tests in 16.195 s, OK, exit 0, 17 s, no `FAILED` or `Error` line (`task2-verify.log`) |
| Task 3 verify 1, `python -B -m unittest discover -s tests/phase60 -t . -v` | Ran 911 tests in 645.660 s, OK (skipped=1, the opt-in `PHASE60_PLATFORM_PROBES` platform probe), exit 0, 647 s (`full-discovery.log`, run once at module SHA-256 `dad7e218...0a55`) |
| Task 3 verify 2, `tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests `-v` | Ran 35 tests in 1.692 s, OK, exit 0, 2 s (`task3-verify2.log`) |
| Focused regression during development: `test_static_guards test_cross_check test_refusals test_arm_spec test_run_short test_budget_driver test_schedule` | Ran 215 tests in 96.300 s, OK |
| RED evidence, both new modules against `HEAD`'s runner | `Ran 2 tests`, `FAILED (errors=2)` (two ImportErrors); module restored and its SHA-256 re-checked (`tdd-red.log`) |

The full discovery ran once, at the final code, and was not repeated; its complete stdout and stderr are retained. The new modules account for 69 of the 911 tests.

## Known Stubs

None in the module or its tests. Two planned hand-offs remain by design and are named in `60-08-SUMMARY.md` and `60-10-SUMMARY.md`: the real-arm command line, lock and resume are Plan 60-12, and the real protocol, preflight and verify are Plan 60-13. `.planning/WINDOWS.md` was not appended: no stub, skipped test or unrun verify was left behind.

## Threat Flags

None. The plan adds no endpoint, authentication path or file format. Threat register: T-60-19 mitigated (the CPU score never reaches `better_state`, a difference stops for the owner; `DisagreementTests`); T-60-11 mitigated (one module-level `counts` clause that writes the stop and re-raises; the static guard's handler rule; `CountsTests`); T-60-07 mitigated (`validate_record` before the exclusive write; 54 removal sub-tests and `WriteStepTests`); T-60-02 mitigated (`torch.load(..., weights_only=True)` literal; `WeightsFormatTests` and the static guard); T-60-09 mitigated (256-row chunks throughout; the monitor runs only at readings); T-60-SC accepted (nothing installed).

## Issues Encountered

- A first draft of `WriteStepTests` ran an unadmitted real arm with no timing override, so the frozen rule gave it a multi-million-step budget and the module hung; it now patches `timing_steps_for` to 50 and `budget_from_timing` to 40, the same shape Plan 60-08's `RealArmBudgetTests` uses.
- `np.random.default_rng` was first patched on the wrong module object in the stream test; the test now compares the timing run's generator and the arm's generator by identity and their first draw, which is the stronger claim anyway.
- The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-12 (the arm command line, lock, graceful stop and resume).** `run_arm` now takes `admission=` and `protocol=`; pass them from `learnability_protocol.admit_arm` and `load_protocol`. A real arm without them keeps the Plan 60-08 shape, but a launched arm must pass both. `run_arm` still takes `clock=`, `clip_enabled=` and `ruling=` from Plan 60-08.
- **Plan 60-13 (the real protocol and preflight).** Every edit to `learnability_run.py` must land before the protocol is written: it is a pinned module. The record's `module_sha256` is that mapping.
- **Open for the owner or verifier:** coverage items D9 and D10 in this SUMMARY, chiefly decision 1 (the unadmitted real-arm record shape), decision 2 (`fixture_r_ref`) and the two rewritten test files.

---

*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- The three created files exist on disk and are tracked and clean; the code commit `b5f47fac` exists and deleted no tracked file; `git rev-list --count 58920e96..HEAD` is 1 before this file.
- Every task's `<verify>` was re-run on the committed code and the results are the table above; the full discovery and the prohibition suite pass with no `FAILED` line.
- `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md` and `.planning/config.json` were not touched by this plan; the governed `r_ref_stage0.json` and the frozen scorecard were not edited; no real arm record, no `runs/phase60` directory and no protocol or preflight was written.
