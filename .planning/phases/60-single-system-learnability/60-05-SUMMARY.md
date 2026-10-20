---
phase: 60-single-system-learnability
plan: 05
subsystem: testing
tags: [learnability-harness, trainer-function-composition, oracle-equality, mutation-test, chunked-physics, frozen-monitor, polish-freeze]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-01 data-only half of learnability_losses, the Phase 60 static guard and the tests/phase60 package; Plan 60-23 run_arm flow that test_run_short still exercises"
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "the memory-bounded controller step used as the oracle, the stub-source fixtures, and the L-BFGS segment freeze ruling (57-RULING.md lines 112-124)"
provides:
  - "pinn/verification/learnability_losses.py physics half: make_trajectory, draw_collocation_times, collocation_chunk_raw, physics_pass1, ic_term, physics_pass2_backward, physics_adam_step, physics_polish_objective, frozen_monitor_log, release_chunk_memory"
  - "tests/phase60/test_losses_trainer_functions.py: oracle equality, identity, mutation, 256-row chunk bound, D-06 monitor and frozen-handoff polish proofs (64 tests)"
affects: [60-11]

actuals:
  tokens: 17531
  tasks: 2
  commits: 2
plan_head_before: 6db3c02a93f8dbdfdac6ca17abaeeab68aa3f96e

tech-stack:
  added: []
  patterns:
    - "Compose the trainer's functions by bare-name import so mock.patch.object on the harness module moves the output"
    - "Equivalence oracle: a real RunController step on the Phase 57 stub source, compared term by term and gradient by gradient"
    - "A partial last chunk (256 + 144 rows) so per-chunk fractions differ from 1/n_chunks"
    - "Fault injection into the live module to show that tests which pass at once are not vacuous"

key-files:
  created:
    - tests/phase60/test_losses_trainer_functions.py
  modified:
    - pinn/verification/learnability_losses.py

key-decisions:
  - "The committed oracle uses 400 collocation rows (chunks of 256 and 144), not 4,096, because one production-shape step costs about 29 s on this CPU; a separate one-off production-shape run (4,096 rows, 16 chunks) was also bit-identical"
  - "physics_pass2_backward gates the energy and angular-momentum terms on their own weights, and a skipped term reports exactly 0.0"
  - "frozen_monitor_log returns exactly the seven keys the plan and Plan 60-11 name; the per-bin weight vector is derivable from residuals_per_bin but is not itself logged (open item D7)"
  - "Non-oracle tests run on a small smooth network with the production call shape, since identity, mutation, chunk-bound, monitor and polish properties belong to the composition"

patterns-established:
  - "Mutation tests patch one named trainer function and assert exact doubling (places=12) for linear terms, a change for derivative functions"
  - "Spy on componentwise_du records the size of every u vector to prove the chunk bound on every evaluation path"

requirements-completed: [INST-05, FEAS-04]

coverage:
  - id: D1
    description: "A harness physics Adam step equals the trainer's microbatched step on every per-term loss and every parameter gradient, for the Stage-0 weights and for lambda_e = lambda_l = 1 (INST-05 a)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#TracerOracleTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Each trainer function the module imports is the trainer's own object, and patching any of eight named functions (plus compose_total) moves the harness output"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#IdentityTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#MutationTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Pass 1, pass 2, the frozen monitor, the polish objective and the Adam step never evaluate more than 256 rows at a time and release each chunk"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#ChunkBoundTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#ReleaseChunkMemoryTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "D-06: the frozen monitor is logged on demand through the chunked pass 1 and has no halt path; a stalled front returns front_idx -1"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#MonitorTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "GAP-60-05: the physics polish objective uses rows, causal weights, bin counts and loss weights frozen at the handoff and the chunked pass 2, never a full-batch evaluation"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#PolishObjectiveTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#ModuleContractTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "FEAS-04 arm (a): Rung 2a never evaluates the data term and hands compose_total a zero tensor; energy and angular momentum are evaluated only when their own weight is above zero"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_losses_trainer_functions.py#ZeroWeightAndRungTwoATests"
        status: pass
    human_judgment: false
  - id: D7
    description: "The monitor log carries the seven keys Plan 60-11 expects; D-06's wording says it logs the per-bin causal weights, and the weight vector itself is not one of the seven keys"
    requirement: "INST-05"
    verification: []
    human_judgment: true
    rationale: "The weights are a deterministic function of the logged normalized residuals (w_n = exp(-eta_c * exclusive cumulative sum), eta_c = 1.0), so no information is lost, but whether the owner wants the vector written out is a reading of D-06 that no test can settle. Adding one key w_n to frozen_monitor_log and to the Plan 60-11 key test would be a one-line change."

duration: 31min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 05: Physics step composed from the trainer's functions Summary

**The harness now builds the physics Adam step, the frozen-monitor log and the frozen-handoff polish objective from the trainer's own functions, and one harness step is bit-identical to the controller's memory-bounded step on every term and every gradient, in 256-row chunks throughout.**

## Performance

- **Duration:** 31 min
- **Started:** 2026-10-20T03:01:04Z
- **Completed:** 2026-10-20T03:31:48Z
- **Tasks:** 2 (Task 1 tracer, Task 2 auto with tdd)
- **Files:** 1 created (1,247 lines of tests), 1 modified (module grew from 49 to 508 lines); no other file touched

## Accomplishments

- **Physics step from the trainer's functions.** `physics_adam_step` runs the trainer's order: pass 1 freezes the causal weights, `(data + IC).backward()`, then the pass-2 chunk loop with the constant row weight `w_n[bin] / (16 * r_ref * count[bin])`. Every loss, derivative and bin function is imported by bare name, so `mock.patch.object` on the module moves the output. All tensors and constants are explicit arguments. `r_ref` is always an argument and the module reads no file.
- **Oracle equality.** A real `RunController` over the Phase 57 stub source (CPU float64, production network) and one harness step agree on `data`, `ic`, `phys`, `energy`, `angmom`, `total` and on all 28 parameter gradients at `rtol 1e-10`, `atol 1e-12`, for the Stage-0 weights and for `lambda_e = lambda_l = 1`. Measured agreement is exact (every difference 0.0), including at the full production shape (see Verification Results).
- **Mutation and identity proofs (INST-05 a).** Twelve trainer objects are identical (`is`) to the trainer's. Patching `data_huber_loss`, `ic_anchor_loss`, a `causal_physics_loss` that doubles `w_n`, `soft_energy_loss`, `angular_momentum_loss` and `accumulate_chunked_data_term` doubles the matching output to 12 places; patching `componentwise_du` or `softened_acceleration` changes the physics term and nothing else; `compose_total` also moves the total.
- **256-row bound.** A spy on `componentwise_du` shows a maximum of 256 rows and exactly 16 chunk evaluations per pass over 4,096 rows in pass 1, pass 2, the frozen monitor, the polish objective and the Adam step (32 for the two-pass step), with a release after every chunk; a microbatch of 100 gives 40 chunks of 100 and one of 96.
- **D-06.** `frozen_monitor_log` runs the chunked pass 1 on a fixed 4,096-row set only when called and returns `w_min`, `w_mean`, `w_max`, `front_idx` (largest bin with `w_n > 0.5`, else -1), the normalized and raw residuals of the 16 bins and `r_ref` as plain JSON values. It has no threshold, no halt and no return code; a stalled or collapsed front returns normally with `front_idx -1`, and an AST test finds no `raise`, `assert` or `try` in it.
- **GAP-60-05.** `physics_polish_objective` takes frozen rows, `w_n`, bin counts and `LossWeights`, never redraws or recomputes them (spies on `causal_physics_loss` and `_stratified_full_slot_rows` see zero calls), uses `accumulate_chunked_data_term` for the data term, clears gradients first, and equals the Adam step's value and gradient when `w_n` is the pass-1 result.
- **FEAS-04 arm (a).** Rung 2a (`data_points=None`) never calls `data_huber_loss` and gives `compose_total` a zero tensor with `lambda_data` still 1.0; its gradient equals the full gradient minus the data-only gradient.

## Task Commits

1. **Task 1: Tracer, one harness physics Adam step equals the trainer's microbatched step** - `4fc9f60f` (feat)
2. **Task 2: Mutation and identity proofs, the 256-row bound, the D-06 monitor and the frozen-handoff polish objective** - `042ed09d` (feat)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

Tracer feedback gate: not auto mode (`AUTO_CHAIN` and `AUTO_CFG` false), `HUMAN_VERIFY_MODE` is `end-of-phase`, and the tracer verify has only `<automated>`, so the verify was re-run on the committed tree before Task 2 (4 tests OK). Tracer verified end-to-end; expansion followed.

## Files Created/Modified

- `pinn/verification/learnability_losses.py` - the physics half: ten new functions plus the extended bare-name imports; `data_only_loss` and `data_polish_objective` bodies are unchanged
- `tests/phase60/test_losses_trainer_functions.py` - `TracerOracleTests`, `IdentityTests`, `MutationTests`, `ZeroWeightAndRungTwoATests`, `DrawTests`, `ChunkBoundTests`, `ReleaseChunkMemoryTests`, `MonitorTests`, `PolishObjectiveTests`, `ModuleContractTests`

## Decisions Made

- **Oracle size.** One production-shape step (4,096 rows, production network, CPU float64) takes about 29 s (47 s with diagnostics), so two weight cases would use most of the plan's 30 s module budget. The committed oracle uses 400 collocation rows: two chunks at microbatch 256 (256 then 144, fractions 0.64 and 0.36, so a `1 / n_chunks` mistake cannot hide), unequal rows per bin, and times at 0 and `T`. `microbatch_size=256` and `want_diagnostics=True` follow the plan. The module runs in 18.1 s.
- **Degenerate stub quantities.** The stub's initial angular momentum is exactly zero, which makes the angular-momentum scale `1e-8` and swamps every other gradient. The `lambda_e = lambda_l = 1` case therefore replaces `h0`, `eps_h` and `l0` through `dataclasses.replace` on the anchor context and uses unequal lambdas (`lambda_ic 1e-3`, `lambda_phys 0.7`), so the physics gradient is a visible part of the total and no lambda is silently fixed at 1. The Stage-0 case uses the controller's own schedule.
- **Per-term gating.** "Energy and angular momentum evaluated only when `weights.lambda_e` or `weights.lambda_l` is above zero" is read as each term on its own weight (the pattern map says "their ramped weight"). A skipped term reports exactly 0.0, so the oracle compares energy and angular momentum only where the weight is positive; the totals still agree.
- **Monitor keys.** Exactly the seven keys named by the plan and by Plan 60-11's test. See open item D7.
- **Polish composition.** The value is `weighted_data + (weighted_ic + lambda_phys * phys + lambda_e * energy + lambda_l * angmom)`, the trainer closure's association, and a detached 0-d tensor like `data_polish_objective`'s.
- **Small network for the other classes.** Identity, mutation, chunk-bound, monitor and polish properties belong to the composition, so they run on a 10-unit smooth network with the production call shape and a self-calibrated `r_ref`; only the oracle pays for the production network.
- **Additions beyond the named classes.** `DrawTests` (the draw is the ratified stratified rows; one slot gives one row per bin, as Plan 60-11's fixture arms need), `ReleaseChunkMemoryTests` (the helper the static guard exempts), `ZeroWeightAndRungTwoATests` (must-have truth 3) and `ModuleContractTests` (the planned twelve exports; the module names no full-batch trainer path, halting rule, governed-artifact reader or file read). Each traces to a must-have truth.
- **Commit shape.** Task 2 carries `tdd="true"`; the plan fixes one commit with a stated subject, so RED evidence was recorded instead of a failing-test commit (below). The trailer names `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text says Opus 5.5.

## Deviations from Plan

None - plan executed as written. The additions above are tests that trace to the plan's own truths; no semantic choice beyond the plan's text was made.

## Issues Encountered

None that blocked work. Two items for the record:

- The expected cost of the oracle (above) forced the reduced row count; the full-shape equality was checked once outside the suite.
- My first fault-injection run reported one fault as missed because the test module binds `physics_adam_step` at import, so patching the harness module did not reach it. This was a defect in the scratch runner, not in the tests; with the binding patched the fault was caught.

## Verification Results

| Command | Result |
|---|---|
| Task 1 verify: `python -B -m unittest tests.phase60.test_losses_trainer_functions.TracerOracleTests -v` | Ran 4 tests in 16.385s, OK; re-run on the committed tree as the tracer gate: Ran 4 tests in 17.293s, OK |
| Task 1 acceptance: `tests.phase60.test_static_guards tests.phase60.test_run_short -v` | Ran 64 tests in 7.844s, OK |
| Task 2 RED (new classes against Task 1 code) | Ran 60 tests, failures=2, errors=31: 16 `AttributeError` for `frozen_monitor_log`, 15 for `physics_polish_objective`, the export-set test, and the monitor-has-no-halt-path test (finds 0 definitions); the other 32 tests (identity, mutation, zero-weight and Rung 2a, draw, release) passed at once |
| Task 2 GREEN (same classes after implementation) | Ran 60 tests in 2.289s, OK |
| Task 2 verify 1: `tests.phase60.test_losses_trainer_functions tests.phase60.test_static_guards tests.phase60.test_run_short -v` | Ran 128 tests in 25.687s, OK (no "Error" or "FAILED" in the output) |
| Task 2 verify 2: `tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions` tests `-v` | Ran 35 tests in 1.557s, OK |
| Module alone (acceptance: about 30 s or less) | Ran 64 tests in 18.126s, OK |
| Whole package: `python -B -m unittest discover -s tests/phase60 -t . -v` | Ran 285 tests in 83.787s, OK (skipped=1: the opt-in platform probe in `test_scorer_mps`, needs `PHASE60_PLATFORM_PROBES=1`) |
| Oracle fault injection (6 faults: chunk fraction 1/2, mean count, `lambda_phys` dropped, `r_ref` ignored, IC backward omitted, energy scaled by 1+1e-9) | all 6 caught |
| Non-oracle fault injection (19 faults across polish, monitor, chunking, release, draw sort, Rung 2a and gating) | all 19 caught |
| One-off production-shape oracle (full 256-slot batch, 4,096 rows in 16 chunks of 256, 8,192 data points, both weight cases; not a committed test) | every term difference 0.0; `max_abs_diff` and `max_rel_diff` of all 28 gradients 0.0; 116 s |

Complete logs and the scratch probes are retained outside the repository in the session scratchpad (`.../scratchpad/exec-60-05/`). Expensive-command policy: the production-shape probe (116 s) and the package regression (84 s) each ran once and were not repeated; the only repeated verify was the tracer gate, which the protocol requires.

## Known Stubs

None.

## Threat Flags

None. The module opens no file and adds no endpoint, authentication path or schema. T-60-14 is mitigated by the identity, mutation and oracle tests; T-60-09 by `ChunkBoundTests`; T-60-11 by `MonitorTests` plus the existing static ban on `PlateauDetector`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-11** can import `make_trajectory`, `draw_collocation_times(record_key, rng, *, n_slots=256)`, `physics_pass1`, `physics_adam_step`, `physics_polish_objective`, `frozen_monitor_log` and `release_chunk_memory` with the signatures its interface block lists. `n_slots=1` gives the 16-row draw its fixture arms use.
- **Caller duties.** `physics_adam_step` leaves gradients in `.grad`; the caller clears them first, clips, and steps the optimizer. `physics_polish_objective` clears them itself. Both take `r_ref` explicitly; the polish must be given the same `r_ref` that produced the frozen `w_n`. `w_n` and the bin counts must be the tensors `physics_pass1` returns (same dtype and device); a resume that restores them from a checkpoint (Plan 60-12) has to rebuild exactly those.
- **Skipped terms.** At `k = 0` the harness reports `energy` and `angmom` as exactly 0.0 because they are not evaluated, whereas the trainer evaluates them and logs their unweighted values. Plan 60-11's record should say "not evaluated", not "zero loss".
- **Cost.** A production-size physics step on CPU float64 takes about 29 s, so fixture arms must keep `fixture_n_slots` small, as the plan already says.
- **Open for the owner or verifier (coverage item D7).** Whether `frozen_monitor_log` should also write the 16 causal weights, given D-06's wording; a one-line change if so.
- The oracle's equality claim at the production shape rests on a one-off probe, not a committed test; the committed oracle uses 400 rows.

Process notes: `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` were not touched (INST-05 and FEAS-04 are declared by other plans too). `.planning/WINDOWS.md` was not appended: there are no stubs, skipped tests or unrun verifies from this plan, and it is outside the owned paths. The `read_first` item `tests/phase55/test_architecture_characterization.py:283-320` was read after the Task 2 commit; the committed tests already follow that pattern (the same `side_effect` wrappers; the derivative mutation here scales only the second derivative, which isolates the physics term more sharply). The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- Both owned files exist on disk; commits `4fc9f60f` and `042ed09d` exist; the module docstring starts "Phase 60 (INST-05)".
- Task acceptance criteria re-run against the final tree: all pass (Verification Results above). The Phase 60 static guard passes, `RunController` is named nowhere in the module's executable source, and `test_run_short` still passes.
- The working tree holds only the user-owned changes (`.planning/config.json` and the v2.2 halt brief) besides this file.
