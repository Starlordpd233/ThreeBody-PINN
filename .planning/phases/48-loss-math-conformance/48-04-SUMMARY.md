---
phase: 48-loss-math-conformance
plan: 04
subsystem: training-observability
tags: [pytorch, autograd, adam, lbfgs, jsonl, conformance, tdd]

# Dependency graph
requires:
  - phase: 48-loss-math-conformance
    provides: Corrected controller-side /3 Rbar producer and locked loss/config contracts from Plans 48-01 through 48-03
provides:
  - Observation-only Adam and last-closure L-BFGS raw/applied gradient telemetry
  - Canonical JSONL provenance and fail-closed gradient-stat completeness
  - Optimizer-equivalence and graph-isolation conformance coverage for INST-02
affects: [phase-49-conformance-gate, phase-50-valid-stage-0-rerun]

# Actuals (#2632)
actuals:
  tokens: 8052
  tasks: 2
  commits: 5

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Fixed-parameter-tuple autograd.grad diagnostics with no .grad mutation
    - Explicit step-local telemetry mapping separated from validation details
    - Last-closure overwrite semantics for L-BFGS optimizer-step attribution
    - JSON sanitizer plus required-field completeness gate for durable telemetry

key-files:
  created:
    - tests/phase48/test_gradient_observability.py
  modified:
    - pinn/training/controllers.py
    - pinn/training/step_log.py
    - tests/phase42/test_step_log_jsonl.py

key-decisions:
  - "Compute five unweighted global parameter-gradient norms with autograd.grad(create_graph=False, allow_unused=True, materialize_grads=False); graphless present terms record exact numeric zero without invoking autograd.grad."
  - "Adam telemetry is captured before total backward with provenance pre_total_backward; L-BFGS data uses accumulated data-only gradients and the four live non-data graphs, with the last closure evaluation emitted."
  - "Applied norms are the nonnegative scheduled lambda times raw norms, including exact zero for zero-weight energy, and telemetry never controls losses, schedules, clipping, or optimizer updates."
  - "Missing or non-finite required statistics remain null after JSON sanitization and force grad_stats_complete=false and step_completed=false."

patterns-established:
  - "Keep optimizer-step telemetry in an explicit local mapping rather than validation-overwritable widened-detail state."
  - "Clear transient non-data term references after ordinary L-BFGS backward so diagnostic graphs are not retained."

requirements-completed: [INST-02]

coverage:
  - id: D1
    description: "Adam emits five finite raw and five applied global parameter-gradient norms at canonical step cadence with pre-total-backward provenance."
    requirement: INST-02
    verification:
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_adam_gradient_stats_match_hand_oracle"
        status: pass
      - kind: integration
        ref: "tests/phase48/test_gradient_observability.py#test_adam_step_emits_complete_gradient_stats"
        status: pass
    human_judgment: false
  - id: D2
    description: "L-BFGS emits detached statistics from the last closure, preserving accumulated data gradients, live non-data gradients, frozen weights, and explicit provenance."
    requirement: INST-02
    verification:
      - kind: integration
        ref: "tests/phase48/test_gradient_observability.py#test_lbfgs_gradient_stats_use_last_closure"
        status: pass
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_lbfgs_gradient_stats_do_not_change_update"
        status: pass
    human_judgment: false
  - id: D3
    description: "Telemetry diagnostics do not mutate parameter gradients, clipping, graph lifetime, or Adam/L-BFGS optimizer updates; unused parameters contribute zero and disconnected terms are exact zero."
    requirement: INST-02
    verification:
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_adam_gradient_stats_do_not_change_update"
        status: pass
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_unused_parameter_contributes_zero"
        status: pass
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_disconnected_term_yields_zero_norm"
        status: pass
    human_judgment: false
  - id: D4
    description: "Canonical JSONL represents absent/non-finite required gradient statistics as null, reports nonfinite keys, and fails both telemetry completeness and step completion."
    requirement: INST-02
    verification:
      - kind: unit
        ref: "tests/phase48/test_gradient_observability.py#test_gradient_stats_missing_or_nonfinite_fail_completion"
        status: pass
      - kind: unit
        ref: "tests/phase42/test_step_log_jsonl.py#test_e1_nonfinite_whole_file_parseability"
        status: pass
    human_judgment: false

# Metrics
duration: 20 min
completed: 2026-08-03
status: complete
---

# Phase 48 Plan 04: Loss-Math Conformance Summary

**Observation-only Adam and last-closure L-BFGS raw/applied gradient telemetry now reaches canonical JSONL with explicit provenance and fail-closed completion semantics.**

## Performance

- **Duration:** 20 min (including the approved tracer verification checkpoint)
- **Started:** 2026-08-03T02:18:56Z
- **Completed:** 2026-08-03T02:38:33Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added fixed-parameter-tuple `autograd.grad` helpers and wired all ten raw/applied term norms into Adam's pre-total-backward event and L-BFGS's last closure evaluation without changing ordinary backward, clipping, or optimizer behavior.
- Added canonical registry fields for the ten norms plus provenance/completeness; non-finite values sanitize to JSON `null`, are named in `nonfinite_keys`, and fail `grad_stats_complete` and `step_completed`.
- Added hand-oracle, disconnected/unused-parameter, graph-lifetime, validation-overwrite, cadence, missing/non-finite, and instrumented-versus-control optimizer tests for both optimizers.

## Task Commits

Each task was committed atomically; Task 1 used the required tracer RED/GREEN gates and Task 2 used test/implementation/assertion commits:

1. **Task 1 RED: Add Adam gradient observability red gate** - `ea96e2e2` (test)
2. **Task 1 GREEN: Emit Adam per-term gradient telemetry** - `5c8ca357` (feat)
3. **Task 2 tests: Cover L-BFGS telemetry and completion** - `5effc8d3` (test)
4. **Task 2 implementation: Capture last-closure L-BFGS gradient stats** - `f6f1685e` (feat)
5. **Task 2 assertion: Preserve zero applied L-BFGS energy norm** - `82bf7e0` (test)

**Plan metadata:** final GSD state/roadmap/requirements metadata is committed separately with this summary.

## Files Created/Modified

- `pinn/training/controllers.py` - Computes and emits Adam/L-BFGS raw/applied telemetry, preserves closure-local state, and gates completion on finite required statistics.
- `pinn/training/step_log.py` - Registers the twelve gradient-stat fields and documents their canonical/provisional status.
- `tests/phase42/test_step_log_jsonl.py` - Updates canonical and non-finite JSONL fixtures for the new completeness contract.
- `tests/phase48/test_gradient_observability.py` - Provides numerical, cadence, safety, graph-release, validation-isolation, and optimizer-equivalence coverage.

## Decisions Made

- Diagnostics use `torch.autograd.grad` with no higher-order graph and never write parameter `.grad`; graphless terms are distinguished from unavailable terms by recording exact numeric zero versus null.
- L-BFGS captures data-only gradients after full chunk accumulation, computes non-data norms from live graphs before ordinary backward, overwrites detached stats on every closure, and emits only the last closure with `last_closure_evaluation` provenance.
- Telemetry is observation-only. The existing scheduled weights remain the source for applied norms, including exact zero energy where the locked lambda is zero; no configuration knob or optimizer control path was added.

## TDD Gate Compliance

- Task 1 RED (`ea96e2e2`) failed before implementation as required; Task 1 GREEN (`5c8ca357`) passed the tracer and Adam checks before the human verification gate.
- Task 2's tests (`5effc8d3`) preceded the implementation (`f6f1685e`), followed by the targeted zero-energy assertion (`82bf7e0`).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Preserve gradient telemetry on Adam's no-guard clip-failure record**
- **Found during:** Task 2 review of all Task 1 `_log_step` paths
- **Issue:** The no-guard non-finite clipping path did not pass the newly captured `gradient_stats` mapping, so a failed step could lose the telemetry required by the canonical event contract.
- **Fix:** Pass the same explicit step-local gradient-stat mapping through that logging path.
- **Files modified:** `pinn/training/controllers.py`
- **Verification:** Combined Phase-48 observability/JSONL tests and Phase-40 optimizer tests passed.
- **Committed in:** `f6f1685e`

---

**Total deviations:** 1 auto-fixed (Rule 1: 1)
**Impact on plan:** Necessary logging correctness fix; no scope expansion or training-semantics change.

## Issues Encountered

No unresolved issues. A focused Ruff check reports only pre-existing unused imports/locals outside this plan's scope; no new warning was introduced. No authentication gate, package installation, training run, held-out evaluation, framework-spec edit, or source-silent adjudication gap occurred.

## Phase-50 handoff

- Instrumentation cost is always on: under locked D-16, each Adam optimizer step and each L-BFGS closure performs five additional `autograd.grad` backward traversals. There is intentionally no configuration knob; this remains observation-only instrumentation.
- `step_completed` consumer audit (`rg -n 'step_completed' pinn tests`) found only the canonical field registry/documentation, the controller's event producer, and test fixtures/assertions. No production consumer couples telemetry completeness to optimizer advancement, step counting, resume behavior, checkpoint cadence, or gate eligibility.

## Auth Gates

None - no external service or authentication was required.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. No placeholder, TODO/FIXME, empty UI data source, or intentionally skipped verification was introduced in the files owned by this plan.

## Next Phase Readiness

INST-02 is complete for both optimizers. Phase 49 can consume canonical finite/incomplete telemetry without inferring optimizer progress from `step_completed`; Phase 50 has the explicit always-on cost and consumer audit needed for planning.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/48-loss-math-conformance/48-04-SUMMARY.md`.
- Task commits `ea96e2e2`, `5c8ca357`, `5effc8d3`, `f6f1685e`, and `82bf7e0` are present in Git history.
- Combined Plan 48-04 and Phase-40 optimizer verification passes; `git diff --check` passes.

---
*Phase: 48-loss-math-conformance*
*Plan: 04*
*Completed: 2026-08-03*
