---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "01"
subsystem: verification
tags: [tdd, red, causal-loss, r-ref, collocation-allocation, invariant-b, l-bfgs, gate-04, evaluation-boundary, stdlib-unittest]

requires:
  - phase: 56-contract-amendment-train-free-gate
    provides: "pinn.verification.gate04_train_free (Gate04Verdict/gate04_verdict/condition_ii_verdict stub/run_gate/write_r_ref_artifact), pinn/verification/artifacts/r_ref_stage0.json, the committed six-case raw.json this plan replays"
  - phase: 55-architecture-characterization-probe
    provides: "pinn.verification.architecture_characterization_probe (RATIFIED_N_BINS/RATIFIED_PER_BIN/RATIFIED_TOTAL, ratified_causal_weights, stratified_collocation_times, bin_mean_residuals)"
  - phase: 54-recalibration-decision-grounding
    provides: "54-RULING.md — the ratified A1+B2+C1+D3+E1 recipe and Batch allocation and bin policy this plan's tests encode"
provides:
  - "tests/phase57/ — 46 focused stdlib-unittest tests across 3 modules, all discoverable and RED for the missing bounded amended-recipe conformance patch (never for import/syntax/fixture/data/environment reasons)"
  - "tests/phase57/_fixtures.py — deterministic CPU/float64 dataset-free/held-out-free fixtures: make_full_slot_source/make_replay_only_source (256-slot and 240-replay-only StageQuery stubs), bin_index_for_time/bin_counts (independent bin-edge re-derivation), build_run_controller (real RunController over stub sources), geometric_weight_vector"
  - "The exact bounded production-conformance contract the next implementation plan must satisfy (see key-decisions) for causal_physics_loss, condition_ii_verdict, the checkpoint envelope, pinn.evaluate, and a new pinn.verification.candidate_eligibility module"
affects: [phase-57-02, RUN-04, RUN-05, EVAL-02]

actuals:
  tokens: 17186
  tasks: 3
  commits: 3
  plan_head_before: 0a3be0f2ed60d844244ab82605cfdffe6806c6fc

tech-stack:
  added: []
  patterns:
    - "Real-committed-evidence-as-oracle: Gate04RulingTests replays the already-committed, sha256-pinned Phase-56 six-case raw.json (fast JSON parse) instead of re-running a ~170s real network measurement inside a focused unit suite"
    - "importlib.util.find_spec existence probing for a not-yet-existing module: never a bare top-level import of an absent module, so one missing module cannot fail collection for every sibling test class in the same file"
    - "Independent closed-form oracle: LossNormalizationTests' expected weights/loss are computed by a from-scratch Python reference, never by calling ratified_causal_weights (which itself calls the function under test) as its own oracle"
    - "Observable-behavior RED over new-API RED where possible: AllocationContractTests calls the CURRENT sample_collocation_points signature unchanged and asserts on its (wrong) bin distribution, rather than requiring a new parameter — a stronger proof that today's allocation is non-conformant"

key-files:
  created:
    - tests/phase57/__init__.py
    - tests/phase57/_fixtures.py
    - tests/phase57/test_recipe_production_path.py
    - tests/phase57/test_runtime_freeze.py
    - tests/phase57/test_gate_and_evaluation.py
  modified: []

key-decisions:
  - "causal_physics_loss target signature: causal_physics_loss(raw_bin_means, *, r_ref, eta_c=..., times=None, dtype, device, return_details=False) — a NEW required keyword-only r_ref that normalizes both the exclusive-prefix exponent and the outer (weights * r_tilde).mean() in one call, plus a NEW optional frozen_weights keyword that, when supplied, skips weight computation entirely and reuses the given vector against the freshly-evaluated residual (GAP-54-06 L-BFGS freeze). return_details=True must additionally expose raw_rbar (unnormalized) and r_ref alongside the existing w_n/rbar keys."
  - "condition_ii_verdict target signature: condition_ii_verdict(raw_bin_means, r_ref, *, eta_c=CAUSAL_ETA_C, dtype, device, t_max=T_CHARACTERISTIC_TIME) -> Mapping with at least {satisfied, baseline_spread, alpha, w_prime_15, front_idx, min_perturbed_weight} — recomputes the controlled-reduction response through ratified_causal_weights at the owner's alpha=log(2)/(2*P_15) scale, never inspecting a static weight vector alone."
  - "Checkpoint envelope needs two NEW keys: build_checkpoint_payload(...) must gain 'front_monitor' (the frozen training-only monitor's own identities/collocation rows/bin assignments/normalized times, distinct from the existing two-scalar 'invariant_b_state'), and RunController.state_dict() must gain 'lbfgs_segment_state' (the frozen L-BFGS segment samples + detached causal weights) for exact resume."
  - "pinn.evaluate needs a new assert_canonical_frame_precondition() called from evaluate_run BEFORE StageIndex.from_split(...) -- proven by source-text ordering, not by triggering the assertion to fail (there is no dataset-free way to force a 'bad frame' condition, so ordering is the checkable contract)."
  - "New module target pinn.verification.candidate_eligibility (not the v2.2 git-ledger CLI-script pattern) hosting structural_facts(record)/select_candidate(facts_by_seed) (the ported Phase-50 four-fact eligibility + fixed 42->41->43 order) and classify_run_outcome(outcome) (terminal vs. blocking run-failure classification) -- chosen because RUN-05/EVAL-02 name pinn.verification as the target seam and an importable module is directly unit-testable, unlike Phase 50's standalone script."
  - "v2.3-distinct config file names fixed as configs/stage0-v23-seed4{1,2,3}.yaml + configs/stage0-v23-smoke.yaml (D-08's own suggested pattern), not yet created; ConfigProtocolTests pins their required run.seed/stage.max_epochs/stage.n_adam/run.invariants.front_advance_window_n/run.run_name values for the implementation plan to satisfy."
  - "Gate04RulingTests verifies 'across all six cases' against the real, already-committed, sha256-pinned Phase-56 evidence (.planning/phases/56-.../evidence/gate04/20260907T033409Z/raw.json) rather than re-measuring the network -- a full six-case compute_r_ref() timed at 167s, unsuitable for a routine unit suite; the real production-path re-measurement is explicitly the separate, later verification wave's job (57-RESEARCH.md wave 4)."

patterns-established:
  - "Checks-that-cannot-fail avoided by construction: every 'X must be distinct from Y' assertion first asserts X's presence (a missing key trivially satisfies 'distinct from', which is not a real proof) -- caught and fixed once in MonitorContractTests during this plan's own verification pass."
  - "Failure-message hygiene: assertions against a RunController.state_dict()/build_checkpoint_payload() result use assertTrue(key in container, msg=...) with an explicit key-list in the message, never assertIn/assertEqual against the raw container (which would dump full model tensors into the failure output)."

requirements-completed: []

duration: 63 min
completed: 2026-09-08
status: complete
---

# Phase 57 Plan 01: Start Red — Amended-Recipe Conformance Contracts Summary

**46 focused stdlib-unittest tests across three new `tests/phase57/` modules define the exact bounded §3.2 allocation/normalization, invariant-B monitor, L-BFGS freeze, GATE-04 ruling, and EVAL-02 canonical-frame contracts the next implementation plan must satisfy — all 46 are dataset-free, held-out-free, discoverable under `pinn-train`'s stdlib `unittest`, and RED against current production code for the missing conformance, never for an import/syntax/fixture/data/environment error.**

## Performance

- **Duration:** ~63 min (estimated from the preceding plan-authoring commit `0a3be0f2` to the final task commit; upfront research/design reading is additional, untimed context-gathering)
- **Started:** 2026-09-08T04:29:58Z
- **Completed:** 2026-09-08T05:32:48Z
- **Tasks:** 3/3
- **Files created:** 5 (0 modified)

## Accomplishments

- `ProductionPathContractTests` drives one real `RunController._stage_batch` → `_build_anchor_context` → `_non_data_terms` step and proves the current implementation reaches for a `CollocationSampler`-sized per-anchor draw instead of the ratified 16-bin, 4096-row, all-selected-slot `FixedBatch.collocation_points` — and that raw/normalized diagnostics are absent.
- `AllocationContractTests` drives `pinn.data.batches.sample_collocation_points` directly (unchanged signature) and proves the current global-uniform-per-slot-quota draw does **not** stratify to exactly 256 rows per bin, for both the 256-slot (240 replay + 16 lookahead) and the real Stage-0-only 240-replay-only shapes — plus a fail-closed refusal for an out-of-contract slot count.
- `LossNormalizationTests` targets `causal_physics_loss`'s bounded `r_ref` contract against an independent closed-form reference (never production code as its own oracle): one batch-global exclusive prefix, `R_ref` normalizing both the exponent and the outer loss, finite gradients to the raw residual, and raw+normalized diagnostics.
- `MonitorContractTests`/`WindowContractTests`/`LbfgsFreezeTests` target the checkpoint-③ frozen training-only monitor (a new `front_monitor` checkpoint key, distinct from the existing two-scalar `invariant_b_state`), the `front_advance_window_n=500` step-deadline/monitor-cardinality separation, and the GAP-54-06 L-BFGS `frozen_weights` freeze (reused byte-identical across trial residuals, with gradient isolation) plus a new `lbfgs_segment_state` checkpoint key.
- `Gate04RulingTests` targets `condition_ii_verdict`'s bounded 2:1-spread + `alpha = log(2)/(2*P_15)` controlled-reduction rule, verified against the real, sha256-pinned, already-committed Phase-56 six-case evidence (no network re-measurement) and against a fresh Phase-57 complete-PASS evidence file that does not exist yet.
- `EvaluationBoundaryTests`/`EvidenceSelectionTests`/`RunFailureClassificationTests` pin the already-correct `tau = 2*(t/T) - 1` assembly and single-use evaluation claim, and target a new `assert_canonical_frame_precondition()` (proven by source-order inspection to precede `StageIndex.from_split`) plus a new `pinn.verification.candidate_eligibility` module porting the Phase-50 four-structural-facts eligibility test, the fixed `42 -> 41 -> 43` selection order, and a terminal-vs-blocking run-outcome classifier.
- `ConfigProtocolTests` pins the required contents of the not-yet-created `configs/stage0-v23-seed4{1,2,3}.yaml` / `stage0-v23-smoke.yaml` band and a new `pinn.training.run_metadata.assert_smoke_matches_graded(...)` helper.

## Task Commits

1. **Task 1: Start red with one controller-level amended-recipe path** — `21e05bab` (`test(57-01)`)
2. **Task 2: Pin normalization, gradients, runtime freeze, and exact GATE-04** — `53eba812` (`test(57-01)`)
3. **Task 3: Pin immutable band, structural selection, and one-look evaluation boundaries** — `4d51ba67` (`test(57-01)`)

**Plan metadata:** committed with this SUMMARY (`docs(57-01)`).

_No `feat`/`refactor` commits: this plan is deliberately RED-only by phase design (D-01/D-02; see TDD Gate Compliance below) — no production file is created or modified._

## Files Created/Modified

- `tests/phase57/__init__.py` — package docstring naming the three test modules and the required `pinn-train`/stdlib-`unittest` invocation.
- `tests/phase57/_fixtures.py` — `make_full_slot_source`/`make_replay_only_source` (built on `tests.phase40._fixtures.make_stub_source`), `bin_index_for_time`/`bin_counts` (an independent re-derivation of the ratified bin-edge convention), `make_training_config`, `build_run_controller` (a real `RunController` over stub sources, mirroring `tests/phase40/test_controllers.py`'s construction pattern), `geometric_weight_vector`.
- `tests/phase57/test_recipe_production_path.py` — `ProductionPathContractTests`, `AllocationContractTests`, `LossNormalizationTests` (12 tests).
- `tests/phase57/test_runtime_freeze.py` — `MonitorContractTests`, `WindowContractTests`, `LbfgsFreezeTests`, `ConfigProtocolTests` (13 tests).
- `tests/phase57/test_gate_and_evaluation.py` — `Gate04RulingTests`, `EvaluationBoundaryTests`, `EvidenceSelectionTests`, `RunFailureClassificationTests` (21 tests).

## Decisions Made

Recorded in full in frontmatter `key-decisions` (six entries) — these are the executable specification the next implementation plan (the "bounded production conformance" wave, 57-RESEARCH.md step 2) must satisfy without reinterpretation. The two most consequential:

1. **`causal_physics_loss` gains `r_ref` (required) and `frozen_weights` (optional) keyword-only parameters** rather than a second function — keeps the causal-weight arithmetic in exactly one place in the repository (57-RESEARCH.md's own constraint), with the L-BFGS freeze and the R_ref normalization as two independent, composable capabilities of the same call.
2. **`condition_ii_verdict` changes from a single-argument always-raising stub to a `(raw_bin_means, r_ref, ...) -> Mapping` function** that recomputes the controlled-reduction response through the real production arithmetic — because the owner's ruling requires proving the WIRING, not just inspecting a precomputed weight vector.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a vacuously-passing "distinctness" assertion during self-verification**
- **Found during:** Task 2 (`MonitorContractTests.test_front_monitor_key_is_distinct_from_invariant_b_state`), while running the exact `<verify>` command
- **Issue:** `assertNotEqual(payload.get("front_monitor"), payload.get("invariant_b_state"))` passes trivially today because `.get("front_monitor")` returns `None` (key absent) — `None != {...}` is always true, so the test could never catch a future implementation that aliases the two keys. This is exactly the "checks that cannot fail" anti-pattern 57-CONTEXT.md's Specific Ideas names (citing the Phase-49 lesson).
- **Fix:** added a preceding `assertTrue("front_monitor" in payload, ...)` so the test is genuinely RED today (key missing) and will only reach the distinctness check once the key exists.
- **Files modified:** `tests/phase57/test_runtime_freeze.py`
- **Verification:** re-ran the exact Task 2 `<verify>` command; the test now reports `FAIL` (was a vacuous `ok`); the assertion message reports the actual key set.
- **Committed in:** `53eba812` (Task 2 commit — caught before commit, not a follow-up fix)

**2. [Rule 1 - Bug] Fixed two assertions that would dump the full model state dict on failure**
- **Found during:** Task 2, first `<verify>` run (`MonitorContractTests.test_checkpoint_payload_carries_a_dedicated_front_monitor_key`, `LbfgsFreezeTests.test_segment_state_restores_exactly`)
- **Issue:** `self.assertIn("key", full_state_dict, msg)` prints the ENTIRE container (including every model weight tensor) in its failure diff, producing ~100KB+ of noise per failing run and making the real `<verify>` output hard to read.
- **Fix:** switched both to `self.assertTrue("key" in container, msg=f"... got keys {sorted(container.keys())!r}")`, which reports only the key list on failure.
- **Files modified:** `tests/phase57/test_runtime_freeze.py`
- **Verification:** re-ran both `<verify>` commands; output dropped from ~125KB to ~19KB with identical pass/fail outcomes.
- **Committed in:** `53eba812` (Task 2 commit — caught before commit)

**Total deviations:** 2 auto-fixed (both Rule 1, both caught during this plan's own required `<verify>` runs before committing, not as post-hoc follow-ups). **Impact on plan:** none to scope or contract — both fixes strengthen the test suite's own correctness; no test's target behavior or named production-contract requirement changed.

## TDD Gate Compliance

This plan's frontmatter is `type: tdd`, but `.planning/config.json` does not set `workflow.tdd_mode` (absent — not enabled), so the RED/GREEN/REFACTOR gate-enforcement mechanism in `gsd-core/references/tdd.md` is inactive for this project. Independent of that config flag, the plan's own `<objective>` explicitly splits the cycle across MULTIPLE plans by design (D-01/D-02: "Phase 57 owns a bounded amended-recipe conformance patch as an explicit first implementation wave, followed by separate verification before RUN-04" — implementation authorization is not run authorization), matching 57-RESEARCH.md's "Ordered Implementation Waves" (step 1 = this plan's focused tests; step 2 = a later, separate "bounded production conformance" plan).

- **RED gate:** satisfied for all three tasks. Each task's exact `<verify>` command was run against the real `pinn-train` conda environment before its commit and confirmed: nonzero exit, the plan-required target test name present in output, zero occurrences of the literal string `ImportError`. Per-task results: Task 1 — 6/7 fail (1 legitimate pin); Task 2 — 17/19 fail across the module set (2 legitimate pins); Task 3 — 17/20 fail (3 legitimate pins). Full `tests/phase57/` discovery: 46 tests, 40 fail (29 failures + 11 errors), 6 legitimate protective pins pass.
- **GREEN gate:** not applicable — no production code is created or modified by this plan (files_modified in the plan frontmatter lists only `tests/phase57/*`). GREEN is the next plan's job.
- **REFACTOR gate:** not applicable, same reason.

## Issues Encountered

- A full six-case `compute_r_ref(DEFAULT_CASES, ...)` real-network measurement was timed at 167s during design — too slow for inclusion in a routine focused unit suite. Resolved by using the real, already-committed, sha256-verified Phase-56 evidence file (`.planning/phases/56-contract-amendment-train-free-gate/evidence/gate04/20260907T033409Z/raw.json`) as `Gate04RulingTests`' six-case data source instead — fast (JSON parse only) and still genuine, physically-grounded evidence rather than synthetic placeholders.
- Two self-caught test-quality issues during verification (vacuous assertion; noisy failure output) — see Deviations above.

## User Setup Required

None — no external service configuration required. No package was installed (57-RESEARCH.md: "No package installation is authorized or needed").

## Next Phase Readiness

- The bounded production-conformance implementation plan (57-RESEARCH.md wave 2) has an executable, committed specification to satisfy: run `python -m unittest discover -s tests/phase57 -p 'test_*.py' -v` under `pinn-train` and drive every currently-failing assertion to green through the API shapes recorded in `key-decisions` above — without inventing a cadence, tolerance, eligibility rule, or scientific threshold the plan's decisions do not name (57-CONTEXT.md "Claude's Discretion" boundary).
- GATE-04 must then be re-run to a complete PASS (empty `unratified_conditions`) with evidence written under `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/gate04/<timestamp>/raw.json` before `Gate04RulingTests.test_persisted_complete_pass_and_r_ref_provenance` can pass — this plan intentionally leaves that evidence absent.
- No run, training step, or held-out access occurred or is authorized by this plan (D-02). RUN-04/RUN-05/EVAL-02 remain unstarted; `requirements-completed: []` is correct — this plan defines the contract those requirements must satisfy, it does not satisfy them.

---
*Phase: 57-corrected-re-run-the-preserved-evaluation*
*Completed: 2026-09-08*

## Self-Check: PASSED

All five created files exist on disk (`tests/phase57/__init__.py`, `tests/phase57/_fixtures.py`, `tests/phase57/test_recipe_production_path.py`, `tests/phase57/test_runtime_freeze.py`, `tests/phase57/test_gate_and_evaluation.py`); all three task commits exist in `git log --all` (`21e05bab`, `53eba812`, `4d51ba67`); the full `tests/phase57/` discovery run reproduces the reported 46-test / 40-non-ok count.
