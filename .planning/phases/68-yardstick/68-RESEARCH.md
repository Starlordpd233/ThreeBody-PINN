# Phase 68 yardstick research

**Research date** 2026-11-08  
**Evidence** Committed repository sources, split and scorecard metadata,
synthetic checks, and the primary papers cited below. The Brutus audit
measurements belong to execution.

<user_constraints>
## User constraints

The decisions, technical discretion and deferrals below are reproduced from
`68-CONTEXT.md`.

### Implementation decisions

### Inputs and comparisons

- **D-01: Use the per-record TRAIN reader.** Reuse `Stage0TrainingReader`,
  the hash-checked split manifest and the process open attestation. Limit
  the audit to the hierarchical base/gold pairs for 1632, 851 and 4658. The
  base record supplies the physical orbit's Stage-0 label, so the gold
  sibling's own `UNASSIGNED` label does not exclude it. Require TRAIN and
  Stage 0 before resolving a corpus path. Record the keys admitted and
  the actual split opens. Use `load_reference` for the existing gauge,
  body permutation and ordered masses.
- **D-02: Compare matched samples within each grid.** Use the frozen
  scorecard's native gold window through `t = 10` for the primary score.
  Use the persisted base sibling for the coarse comparison. Within each
  grid and window, feed the reference positions and recorded velocities
  to `score_trajectory` for the correct answer. For the constant answer,
  repeat each body's mean position over the corresponding sampled window
  and supply analytic zero velocity. This is the existing diagnostic
  baseline. Keep the gold and base windows, sample counts and measured
  cadences explicit. Verify that the compared records have matching body
  order and use the existing grid agreement evidence.

### Measurement and evidence

- **D-03: Call the shared gate calculations on the same inputs.** For the
  finite-difference energy comparison, use `compute_trajectory_gate_metrics`
  and `aggregate_gate_verdict` from `gate_metrics`. Pair `r_prime` with
  `u = t/T` via `gate_time_coordinate`, using ordered raw masses. Use the
  same gold positions and times for the recorded-velocity reference and
  the finite-difference probe. Retain the production stencil, including
  its endpoints, and record the native base result separately. Map the
  shared calls to `compute_validation_gate` and `evaluate_run`, including
  any input dtype differences relevant to the reading. The audited
  aggregate is over the TRAIN panel. Exercise the calculation with
  in-memory inputs, outside the evaluator's attempt and receipt path.
- **D-04: Distinguish the verdict from the audit finding.** Report the
  existing bar and verdict alongside the expected known answer. A complete
  audit can expose a correct-answer failure or a constant-prediction pass.
  Preserve separate FEAS-01 tier, finite-difference gate and context-only
  results. A constant with finite nonzero initial energy conserves energy
  relative to its own initial state. The measured floor describes the drift on the
  sampled Brutus references. If it drives a decision, inspect the returned
  Hamiltonian series to explain whether the initial value or endpoint
  estimates contribute to the discrepancy. Publish provenance, a rerun
  command and results at the precision needed to reproduce verdicts. Use
  the edge checks in `68-SPEC.md` to verify the existing boundaries and
  record any refusal or missing row as such.

### Owner checkpoint and research handoff

- **D-05: Bring checkpoint 2 the committed audit first.** Present the
  charter's three C-7 choices with the measured base/gold comparisons and
  the consequences for production validation and evaluation. Ask for C-7
  explicitly. Then present C-2 and C-4 through C-6 with that disposition
  stated, including the C-5 dependency on C-7. Use the frozen comparison
  points and primary published evidence, explaining differences in tasks
  and metric definitions. Record each owner answer verbatim or record the
  row as open. C-6 and C-7 require individual answers. GAP-59-08 stays OPEN
  and YARD-02 stays unsatisfied until an explicit C-7 ruling. On instruction,
  close the original gap with a cross-reference to the verbatim ruling.
  Route resulting changes, including evaluation text under C-11, to v2.6.

### Agent discretion for research and planning

Research should confirm the native record and caller-input conventions,
the smallest reproducible audit entry point, and the evidence needed to
distinguish an inaccurate prediction from a measurement error. Planning
chooses file layout, result encoding and focused checks using existing
repository patterns. The accepted specification defines coverage and
verdict semantics. Any source-silent semantic choice or proposal to
change scope follows the applicable STOP and SCOPE-49 rules.

### Deferred ideas

- The v2.6 direction and commissioning of `trainex-r5` go to Phase 69.
- Framework and production changes follow the owner's instructions into v2.6.

### Reviewed todos, outside scope

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`
  concerns the effect of changing softening on corpus admission and stage
  labels. It remains a separate check. The yardstick holds softening fixed
  while comparing velocity measurements.
</user_constraints>

## Summary

Use a read-only audit entry point over the six named records. First carry
a synthetic pair through the real reader and scoring path. Then capture
the fixed panel, publish its exact values with a readable report, and verify
a replay. Checkpoint 2 starts from the committed evidence. The owner resolves
C-7 first, then considers C-2 and C-4 through C-6.

The scorer and gate answer different questions. FEAS-01 checks position
against a reference and uses explicit velocities for tier-defining energy.
The production gate compares energy to the prediction's own initial energy.
At fixed positions with zero velocity the Hamiltonian is constant. With
positive masses and finite positions its softened potential is negative, so
the initial denominator is nonzero. A constant can therefore pass the gate
while missing the orbit. Conversely, replacing the true velocities with a
difference estimate changes kinetic energy even when position error is zero.

## Responsibility map

| Layer | Reuse | Phase 68 responsibility |
|---|---|---|
| Input admission | `SplitAllowlist.from_manifest`, `expected_splits_sha256`, `Stage0TrainingReader`, `install_open_attestation` | Verify the frozen manifest and all six keys before corpus paths. Read only those records through the per-file reader. |
| Reference | `production_reference.load_reference`, `diagnostic_data.physical_window`, `stage0_census.gold_base_agreement` | Check paired body order, masses and grid agreement. Use the frozen window and preserve each retained native grid. |
| Position and explicit-velocity energy | `load_scorecard`, `score_trajectory`, `ScoreResult.to_json_dict` | Feed the correct and time-mean answers. Report both position components, E, horizons, energy and tiers with their existing roles. |
| Production energy | `gate_time_coordinate`, `RATIFIED_VALIDATION_FRAME`, `compute_trajectory_gate_metrics`, `aggregate_gate_verdict` | Measure the shared calculation on the same allowed inputs. Trace both callers and record a labelled float32 input sensitivity. |
| Evidence | `evidence_io.require_frozen_scorecard`, `module_hashes`, `files_opened_record`, `provenance_record` | Pin code and scored inputs. Publish a replayable JSON and the readable audit report. |
| Owner checkpoint | `64-CHARTER.md`, `59-GAPS.md`, committed audit | Keep evidence, recommendation and verbatim instruction distinct. Route amendments to v2.6. |

## Admitted inputs and representation

The planning preflight verified scorecard freeze commit
`4ea3b1bc95e2dc3794fec4fb2047b9d32b5e889f`, scorecard SHA-256
`f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`
and split-manifest SHA-256
`5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`.
All six `RecordKey("hierarchical", fidelity, id)` combinations passed
`require_stage0_training` using manifest metadata alone. Each base record
has stage 0. Each gold sibling has record stage `UNASSIGNED` and physical
orbit stage 0. The default root resolved to an existing directory through
the Git common directory. Retained snapshot data remains to be read.

| System | Gold / base window counts in Phase 59 census | Base samples per inner period | Census gold/base max deviation |
|---|---:|---:|---:|
| 1632 | 1001 / 126 | 11.93659958850399 | 4.6940684029730735e-11 |
| 851 | 1001 / 126 | 6.716079680723276 | 4.540598344767957e-10 |
| 4658 | 1001 / 126 | 3.1766824484729326 | 6.227120895660836e-10 |

Sources for the historical metadata are `59-CONTEXT.md` D-30, D-31 and D-35,
and `evidence/census/{panels.json,census.csv,census.json}` under the Phase 59
directory. Use the existing `gold_base_agreement` with a frozen maximum
relative deviation of `1e-6`. It matches persisted base times to gold
within `1e-9` and scales by the largest base reference radius. Check
finite arrays and matching permutation, ordered masses and inner-pair slots
before comparison. Report the measured grids and retained counts from this
audit. The expected `0.01` and `0.08` native cadences come from the frozen
scorecard. `pinn/data/adapter.py` measures cadence as the median of native
intervals and flags more than 1% relative disagreement. Check the expected
counts and cadence with those existing references and report the interval
range so an irregular grid is visible. An unexpected grid needs evidence
before it can supply the required native-cadence result. Use the recorded
samples for every calculation.

`load_reference` applies the production COM translation and boost, canonical
body order, fixed rotation, and characteristic scaling. It returns native
time, `r_prime` and recorded `dr_prime/du` in float64. The ordered masses
remain raw. The existing constants give `D = 100**(1/3)` and `T = 10`.
Pass native time to the scorer for horizons and `u = t/T` to the gate
through `gate_time_coordinate`. Use the exact `0 <= t <= 10` mask on both
grids. Gold sets the FEAS-01 tier. Base scores provide coarse context.
The mean for each constant is the sample mean over that grid and window.
See `pinn/data/preprocessing.py`, `pinn/constants.py`,
`pinn/verification/production_reference.py` and
`pinn/verification/diagnostic_fit.py::_comparison_rows`.

## Metric and caller inventory

| Measurement | Current reading | Source |
|---|---|---|
| `e_sys_max`, `e_in_max`, `E` | Largest body error over reference system radius and inner separation-vector error over reference separation, respectively. E is the worst of the two over all sampled times. | `feasibility_scorer.position_errors`, `tier_defining_error` |
| `h_0.01`, `h_0.1` | First time either position error strictly exceeds the delta, divided by T. Return 1 when there is no crossing. Neither horizon has an approved standalone pass bar here. | `feasibility_scorer.valid_horizon`, frozen metrics section |
| FEAS-01 `epsilon_H`, tier | Relative drift from own H(0) with explicit velocities. Tier 1 E <= 0.1, Tier 2 E <= 0.01 and drift <= 1e-3, Tier 3 E <= 0.01 and drift <= 1e-5. | `feasibility_scorer.eps_h_from_velocities`, `feasibility_scorecard.tier_of` |
| Finite-difference energy | Same Hamiltonian with one-sided endpoints and centered interior differences over the supplied grid. Report this value as FEAS-01 context and as the input to the existing production gate. | `gate_metrics.compute_trajectory_gate_metrics`, `feasibility_scorer.fd_context_eps_h` |
| Gate drift, SCS and verdict | Maximum over trajectories. SCS is log10 of that maximum. Nonfinite drift fails, finite drift > 1e-5 fails, equality passes. Zero drift has SCS = -infinity. | `gate_metrics.aggregate_gate_verdict`, `pinn_architecture.md` §10.6 |
| Physics residual mean/max | Optional context under FEAS-01. The frozen known-answer call has no required acceleration input. Keep these fields unavailable with an explanation. | `ScoreResult`, `physics_residual_context`, `59-SCORECARD.md` |

Both production callers use the same `compute_trajectory_gate_metrics`
and `aggregate_gate_verdict`. `pinn/train.py` calls
`validation_gate.compute_validation_gate` for the current-stage validation
pool. The validation wrapper promotes resident times and masses to CPU64
and sends model predictions to CPU64 before the shared calls.
`pinn/evaluate.py::evaluate_run` builds the held-out pool after claiming
the evaluation attempt. It keeps times, masses and predictions in runtime
dtype before the gate's CPU64 math. Both start from float32 residency for
time and mass. The retained generation-7 configuration specifies float32
MPS. For this audit, native float64 inputs isolate the stencil on the
recorded positions and times. A separate CPU calculation on those same
samples rounded to float32 before the shared calls illustrates that
callers' input precision. It represents input rounding only. Model
arithmetic, pool membership and qualification are separate.
See `pinn/data/adapter.py`, `pinn/train.py`,
`pinn/training/validation_gate.py`, `pinn/evaluate.py` and
`configs/stage0-v23g7-seed42.yaml`.

Report H(0), the last H, and the peak absolute difference from H(0) with
its time and endpoint/interior label for the paired routes. Compute the
metric and verdict with the existing functions. An endpoint velocity
estimate has first-order error in the spacing for smooth motion. On a
uniform grid a centered interior difference is second order. The effect
on drift also depends on the change in kinetic energy and the estimated
initial denominator. This is why an interior-only or re-based result
would answer a different question. A nonfinite measurement or missing
required row remains visible and blocks a complete numeric audit. Valid
finite gate failures and conservation passes are findings. See
`gate_metrics.finite_difference_velocity` and `trajectory_eps_h`.

## Evidence for checkpoint 2

The old coarse readings 0.047, 0.21 and 0.38 and recorded-velocity values of
order 1e-14 are historical. Keep them attributed to GAP-59-08. The matched
native gold readings are still unknown. For C-7 A, an autograd route would
differentiate the network's `r_prime` in `u` before detaching. The existing
`feasibility_scorer.network_trajectory` and
`pinn.physics_residual.componentwise_du` show the available derivative
contract. Recorded Brutus velocity checks the Hamiltonian input path
without establishing a model's derivative accuracy or the runtime cost of
a future evaluator. For B, compare every gold drift with the existing
threshold and report any effect of the endpoint or precision choices. A
finite sampled result bounds the claim to those records, cadences and
windows. For C, explain which correct-answer or constant outcomes the
existing route would give. Keep the original C-7 alternatives without
carrying forward the historical universal impossibility claim.

The frozen formula median E is 0.9890032980038623 on TRAIN and
0.940265743143744 on validation. The copy median E is 2.135396659314407 on
validation. The formula reaches Tier 1 or better on 1/1812 TRAIN and 0/227
validation systems. The copy reaches it on 0/227 validation systems. The
frozen family has 16 TRAIN systems. The charter's 12/16 supplies the 75%
proportion in C-4 A, and the recorded validation panel has 227 systems.
Use committed baselines for these comparisons. See Phase 59
`evidence/baselines/baselines.json`, `evidence/census/panels.json` and
`64-CHARTER.md` C-4.

Phase 66's position E values were 0.011431234453278821 on 1632/42,
0.01720558902801923 on 851/42 and 0.07898485527313073 on 1632/41. Each was
Tier 1 on a fitted TRAIN orbit. The control changed depth, width and first
frequency together. Phase 67 confirmed worsening at learning rate 1e-3.
The depth, time-input and window contrasts remained unsettled under their
registered rules. Use those task limits in the C-2 and C-4 comparisons,
including the remaining work for unseen-IC Stage-0 generalization. See
`66-VERIFICATION.md` and `67-CLOSEOUT.md` in their phase directories.

### Primary literature comparisons

| Source | Task and reported measurement | Use in the packet |
|---|---|---|
| Breen et al., MNRAS 2020 | Supervised family with planar, equal-mass, zero-velocity initial states reduced to two free IC parameters. Their MAE is not E. Figure 6 and Appendix C report typical energy error near 1e-2 from separate position and velocity ANNs, with larger close-encounter errors. Projection toward the correct energy surface reduces the example to order 1e-5. | Separate the raw and projected results. Their comparison to correct initial energy and their restricted family differ from our self-drift and Stage-0 generalization task. [Author manuscript §2, Fig. 6, App. C](https://arxiv.org/pdf/1910.07291v1) |
| Kollias and Matzakos, 2026 preprint | Forward tests fit individual periodic orbits. Appendix A.5 Table 12 gives maximum relative drift from own initial energy of 7.74e-4, 3.23e-2 and 1.64e-4 for Euler, Lagrange and figure-eight over one period. Tables 9–11 use max position error or RMSE. | Use the forward results for scale. The Hamiltonian there is Newtonian and the runs are per orbit. Separate the inverse orbit-discovery ensembles from unseen-IC prediction. [Preprint §4, Appendix A](https://arxiv.org/pdf/2607.23501v1) |
| Pereira et al., IAC 2024 | Physics-informed and supervised models over equal unit masses with zero initial velocities. The models predict positions and velocities. Table 2 reports MAE, RMSE and SMAPE. Table 3 reports a separate mean-square physics residual. | Context for family-level physics-informed work under restricted ICs. The reported results supply no matching Stage-0 position or energy bar. [Conference manuscript §§4, 6](https://arxiv.org/pdf/2503.04585v1) |

These results inform the difficulty and scope of C-2, C-4 and C-5. Use
the audit, charter C-1, and the frozen comparisons to make a recommendation
after measurement. C-5 A is conditional on C-7 A. State the consequences
of adopting, retaining, or deferring the locked C-6 bar separately.

## Validation Architecture

The local `pinn-train` Python 3.11.15 environment has NumPy 2.4.6 and
PyTorch 2.12.1 on arm64 macOS. Use the repository's `unittest` style and
CPU tensors. No new dependency, service or GPU run is needed.

The focused preflight ran 80 tests in 1.823 seconds.

```sh
<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase59.test_scorecard tests.phase59.test_scorer_known_errors tests.phase59.test_split_allowlist tests.phase43.test_gate_boundary tests.phase65.test_isolation.Stage0AdmissionTests tests.phase65.test_isolation.AttestationIntegrationTests
```

Add one focused audit test module for the new wiring. It should cover a
matched synthetic pair, admission before
opens, a deliberate missing/duplicate row, precision and key preservation,
and a modified replay record. Reuse the existing scorer and gate boundary
suites. Check values one representable step below, equal to and above each
required tier/gate boundary and the strict horizon deltas wherever existing
coverage is incomplete. Use an ordered nonfinite failure and a valid zero
drift case to distinguish JSON sentinels and gate outcomes.

Phase 68's full-panel replay is the YARD-01 integration check. The first
fixture task supplies any new test code, so no separate Wave 0 is needed.
Git chronology and the byte/hash checks cover checkpoint inputs. Verbatim
authority, the scientific reading and the actual choice remain judgment
checks. The validation map separates those from file-existence checks.

## Open questions (resolved)

- **How to cover both callers safely.** Use the shared computation with the
  ratified frame and labelled input precision. Keep production entry
  points, adapters, models and receipts outside the audit call path.
- **How to record data versions.** Hash the exact retained native arrays and
  ordered masses used in each row. Record identity, source grid, shapes and
  a stable encoding. The input fingerprint describes transformed score
  inputs and needs no second corpus read for a raw-file hash.
- **How to keep the old freeze valid after a ruling.** The scorecard verifier
  checks `59-GAPS.md` in `ancestor_state` mode. A scoped post-audit update
  to GAP-59-08 can cite the ruling while preserving the freeze commit.
  Rerun the existing freeze check after that update.

The native results and the owner's choices are planned outputs. Neither is
a premise required to plan the audit.

## Planning preflight notes

The context-drift advisory reports that the spec predates the context.
The spec defines the work and the later context chooses the reader,
comparisons and checkpoint order within it. This research reconciles the
two by tracing D-01 through D-05 to the locked criteria. The codebase map
advisory flags newer files including generated run paths. This phase uses
the tracked live reader and calculation sources above. No UI, AI
integration, new API or database schema is in scope.
