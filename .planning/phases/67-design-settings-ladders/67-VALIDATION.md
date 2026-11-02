---
phase: "67"
slug: "design-settings-ladders"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-01"
---

# Phase 67 validation strategy

This is the prospective validation contract for EXP-02 through EXP-05. It
does not record a passing implementation or authorize a corpus run.

## Test infrastructure

Use the existing Python standard-library unittest infrastructure and
`<home>/miniforge3/envs/pinn-train/bin/python -B`. No new dependency
or test framework is required. Proposed Phase 67 modules do not exist yet.

- Quick checks run the targeted `tests.phase67` module named by each task.
- The Phase 67 suite command is `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase67 -t .`.
- Compatibility checks use `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -t .`
  and `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase66 -t .`.
- All unit and integration fixtures must be synthetic, with no real corpus,
  held-out evaluator or registered science launch.

Targeted feedback should take under 30 seconds where practical. Split slow
numerical cases rather than weaken assertions. Runtime is an execution-time
measurement, not a verified estimate in this planning document.

## Sampling rate

After each code task, run its targeted suite. After each code wave, run the
Phase 67 discovery. Before real timing or science admission, and again at
the phase gate, run the Phase 65/66 compatibility suites and applicable
historical-byte checks. Run `git diff --check` before each task commit.

Every runnable plan verification command must have an observable failure
signal. A future test path is covered by the task that creates it; its
absence before that task is not a passing test.

## Verification coverage

| Requirement | Behavior | Proposed synthetic suite | Initial status |
|---|---|---|---|
| EXP-02 | Exact depths, locked controls, parameter counts and all-layer logging | `tests.phase67.test_catalog` | Pending creation |
| EXP-03 | Exact rates, cost-only equal-update budgets and continuation refusal | `tests.phase67.test_budget` | Pending creation |
| EXP-04 | Raw14 interface, encoded dimensions, buffers, analytic derivatives, COM and feature-frequency applicability | `tests.phase67.test_time_features` | Pending creation |
| EXP-05 | Signed first-crossing brackets, inclusive prefix, unchanged tau and matching baselines | `tests.phase67.test_windows` | Pending creation |
| All | Registration/orbit/window/settings identity and malformed-evidence refusals | `tests.phase67.test_records` | Pending creation |
| All | TRAIN-only pre-open refusal, diagnostic isolation, power gate and historical preservation | `tests.phase67.test_isolation` | Pending creation |

The final plans may split these modules into smaller cohesive suites. Each
task must identify the test it creates or depends on and a concrete command;
there must be no three consecutive code tasks without automated verification.

## Wave 0 requirements

- Create `tests/phase67/__init__.py` and shared synthetic fixtures in the
  first harness slice.
- Add the relevant suites before depending on new catalog, feature, lap,
  budget, record or launch behavior.
- Prove one fixture traverses registration, guarded fit, frozen scoring,
  logging and result reading before expanding the catalog.
- Keep ordinary test runs independent of weekend AC eligibility by injecting
  the gate clock and power reader into fixtures, never bypassing the real gate.

## Registered execution checks

Real metadata capture, timing and science runs are separate execution tasks.
Their exact settings, algorithms, reading rules and admission receipts must
be committed first. They run only under the established weekend AC gate.
Timing supplies costs only; final update counts are not chosen from scores.

Re-derive prediction/registration/run chronology from Git and record the
supporting hashes in committed evidence. Each result check must confirm its
registration, exact variant/orbit/seed/window, expected layer/cadence rows,
finite scored values, same-window comparisons, access attestation and power
receipt. A failed or partial record is an explicit mechanical problem.

Confirm a contrast only under the prospective reading rule with both repeat
cases. Compare results with predictions before dependent work continues.
An unsettled or out-of-rule result follows the registered owner escalation;
it is not grounds to tune the rule or alter roadmap scope automatically.

## Owner decisions

SCOPE-49 plan changes require the owner's answer. No owner decision is
needed merely to supply scientific constants already delegated to the agent.
Energy-metric and pass-bar decisions remain in Phase 68. The final redesign
decision remains in Phase 69.

## Per-task verification map

The exact runnable commands and immediate failure signals live in each
task's `<verify>` block. This map accounts for every final task. Phase 67
test modules and diagnostic commands are prospective until the named code
plan creates them. The existing Phase 65/66 suites and protocol loader are
already available.

| Task | Wave | Requirement | Verification target | Initial status |
|---|---:|---|---|---|
| 67-01-01 | 1 | EXP-02..05 | Synthetic tracer | Pending implementation |
| 67-01-02 | 1 | EXP-02..05 | Tracer, admission, historical tests and protocol loader | Pending implementation |
| 67-02-01 | 2 | EXP-02..04 | Catalog and time-feature tests | Pending implementation |
| 67-02-02 | 2 | EXP-02..04 | Time-feature, catalog and tracer tests | Pending implementation |
| 67-03-01 | 2 | EXP-05 | Window tests | Pending implementation |
| 67-03-02 | 2 | EXP-05 | Window and baseline tests | Pending implementation |
| 67-04-01 | 3 | EXP-02..05 | Checkpoint and tracer tests | Pending implementation |
| 67-04-02 | 3 | EXP-02..05 | Cost-only budget tests | Pending implementation |
| 67-05-01 | 4 | EXP-02..05 | Record refusal tests | Pending implementation |
| 67-05-02 | 4 | EXP-02..05 | Reading-rule and record tests | Pending implementation |
| 67-06-01 | 5 | EXP-02..05 | Page and workflow tests | Pending implementation |
| 67-06-02 | 5 | EXP-02..05 | Isolation, workflow and tracer tests | Pending implementation |
| 67-07-01 | 6 | EXP-02..05 | Phase 65/66/67 discovery and protocol loader | Pending implementation |
| 67-08-01 | 7 | EXP-02 | Committed design check | Pending registered execution |
| 67-08-02 | 7 | EXP-02 | Metadata and timing-matrix checks | Pending registered execution |
| 67-08-03 | 7 | EXP-02 | Budget and science-matrix checks | Pending registered execution |
| 67-09-01 | 8 | EXP-02 | All 15 science-row checks | Pending registered execution |
| 67-09-02 | 8 | EXP-02 | Committed result/review assertions | Pending registered execution |
| 67-09-03 | 8 | EXP-02 | Review admission, conditional actual ruling | Pending registered execution |
| 67-10-01 | 9 | EXP-03 | Committed design check | Pending registered execution |
| 67-10-02 | 9 | EXP-03 | Metadata and timing-matrix checks | Pending registered execution |
| 67-10-03 | 9 | EXP-03 | Budget and science-matrix checks | Pending registered execution |
| 67-11-01 | 10 | EXP-03 | All 15 science-row checks | Pending registered execution |
| 67-11-02 | 10 | EXP-03 | Committed result/review assertions | Pending registered execution |
| 67-11-03 | 10 | EXP-03 | Review admission, conditional actual ruling | Pending registered execution |
| 67-12-01 | 11 | EXP-04 | Committed design check | Pending registered execution |
| 67-12-02 | 11 | EXP-04 | Metadata and timing-matrix checks | Pending registered execution |
| 67-12-03 | 11 | EXP-04 | Budget and science-matrix checks | Pending registered execution |
| 67-13-01 | 12 | EXP-04 | All 18 science-row checks | Pending registered execution |
| 67-13-02 | 12 | EXP-04 | Committed result/review assertions | Pending registered execution |
| 67-13-03 | 12 | EXP-04 | Review admission, conditional actual ruling | Pending registered execution |
| 67-14-01 | 13 | EXP-05 | Committed design check | Pending registered execution |
| 67-14-02 | 13 | EXP-05 | Metadata and timing-matrix checks | Pending registered execution |
| 67-14-03 | 13 | EXP-05 | Budget and science-matrix checks | Pending registered execution |
| 67-15-01 | 14 | EXP-05 | All 12 science-row checks | Pending registered execution |
| 67-15-02 | 14 | EXP-05 | Committed result/review assertions | Pending registered execution |
| 67-15-03 | 14 | EXP-05 | Review admission, conditional actual ruling | Pending registered execution |
| 67-16-01 | 15 | EXP-02..05 | Phase audit and deterministic saved-index check | Pending registered execution |
| 67-16-02 | 15 | EXP-02..05 | Phase 65/66/67 discovery, protocol and final audit | Pending registered execution |

The conditional ruling rows are skipped only for the already-reviewed
in-scope continuation branch. Their read-only `check-review` remains
mandatory before dependent work. The three descriptor-less transparency
prohibitions in Plans 05/06 remain flagged judgment checks; passing unit
tests does not silently discharge those narrative review obligations.

## Validation sign-off

- [ ] Every task has an automated check or an explicit dependency creating it.
- [ ] All proposed test paths are created before reliance on them.
- [ ] The complete plan verification map is checked against final task IDs.
- [ ] Synthetic tests prove raw14 derivative compatibility and exact prefix semantics.
- [ ] Historical evidence and production locks retain their committed bytes.
- [ ] Registered result checks validate every declared arm and both repeat cases.
- [ ] Measured test feedback fits the stated sampling policy.
- [ ] Implementation has been validated before changing `nyquist_compliant`.

Approval remains pending implementation and the validation audit. Planning
checks establish plan readiness only.
