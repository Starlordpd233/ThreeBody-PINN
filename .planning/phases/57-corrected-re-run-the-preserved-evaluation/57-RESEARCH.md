# Phase 57: Corrected Re-Run & the Preserved Evaluation - Research

**Researched:** 2026-09-08  
**Domain:** PyTorch causal-PINN recipe conformance, guarded Stage-0 execution, and single-look evaluation  
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

<context_copy delimiter="PH57-7KQ2-ZM9A">
PH57-7KQ2-ZM9A_START

### Locked Decisions

- **D-01: Phase 57 owns a bounded amended-recipe conformance patch as an explicit first implementation wave, followed by separate verification before RUN-04.**
- **D-02: Implementation authorization is not run authorization.**
- **D-03: Checkpoint ③ is discharged before any run.** `front_advance_window_n = 500` is explicitly re-ratified as the invariant-B step deadline for the amended recipe. Separately, each run uses one frozen training-only monitoring context for invariant B; `500` is not its cardinality, and resampled training-batch fronts remain diagnostic-only. For the full Stage-0 L-BFGS segment, freeze the segment's samples and detached causal weights at handoff; do not redraw or recompute them in line-search closures or between outer calls.
- **D-04: Checkpoint ④ is discharged by timestamped pre-registration.** The spending seed is 42. Fallback order is 41 then 43, only for structural ineligibility and never for observed scientific metrics.
- **D-05: The GATE-04 precondition must be a *complete* PASS.** Require a `2:1` spread among non-anchor weights, then the fixed all-residual reduction from `57-RULING.md`; require `front_idx = 15` and all perturbed weights `>= 0.70`.
- **D-06: The band is seeds 41 / 42 / 43, matching the v2.0/v2.2 protocol.**
- **D-07: Budget is the shipped Stage-0 config — `stage.max_epochs = 1000`, `stage.n_adam = 1000` — NOT the v2.0 300-step smoke.**
- **D-08: The graded configs are derived from the existing `configs/stage0-rerun-seed4{1,2,3}.yaml`.**
- **D-09: The phase opens with a calibration smoke on the final code state, and the plan's wave decomposition MUST honour "no commit between the smoke and the graded runs."**
- **D-10: The smoke is also the amended recipe's first real-corpus contact and the `S_H` cross-check.** Run the smoke at **seed 42**.
- **D-11: Reuse the `--stage-0-only` switch.**
- **D-12: The GAP-46-01 obligation is a hard gate before EVAL-02 and is RUN-04-mapped, not a fourth eligibility precondition.**
- **D-14: The EVAL-02 three preconditions are the v2.2 EVAL-01 structure, adapted:** (i) preflight conformance passes with zero unwaived divergences, including a complete GATE-04 PASS; (ii) the canonical `(r′, u = t/T)` pairing is proved; (iii) validation-side gate metrics are recorded.
- **D-15: The single invocation is exactly once, on the pre-registered seed's run, on `checkpoints/best.pt`.**
- **D-16: A change made during Phase 57 is "conformance-only" iff its justification does NOT cite what a run produced.**
- **D-17: Phase 57 runs inline on the data-bearing checkout.**
- **D-18: The training environment is the `pinn-train` conda env, invoked off-PATH.** The env has **no pytest**; the dataset-free regression and GATE-04 must be runnable under `unittest`.
- **D-19: The admitted-corpus data root is a run precondition the plan resolves.**
- **D-20: Carry the v2.2 Phase 50 evidence contract forward.**
- If GATE-04 refuses the recalibration train-free, or RUN-04's causal front still fails to advance under the ratified recipe, the evaluation is not spent; the phase records the terminal branch and closes rather than tuning.

### the agent's Discretion

The planner and executor own, without re-opening anything above: the wave decomposition and how D-09's no-commit-mid-band constraint is expressed in it; whether the smoke and the band extraction are one plan or several; attended (`python -m pinn.train`) versus unattended (`scripts/train-unattended.sh`) launch; the file format and layout of the run ledger, band record, pre-registration record, config-delta record, and evidence manifests; which quantiles the band distribution reports; the exact v2.3-distinct run names (only locked property: distinct from the v2.2 `stage0-rerun-seed4X` names); the dataset-free regression test's exact shape (only locked properties: no held-out access, runnable under `unittest`, committed); and the placement of evidence directories under `.planning/phases/57-*/evidence/<category>/<timestamp>/`. Those choices must preserve every decision above, add no dependency, introduce no new threshold or selection rule, and change nothing that enters a loss term, an optimizer, the data path, or a gate beyond resolved GAP-57-01 and the other explicitly grounded Phase-57 obligations.

### Deferred Ideas (OUT OF SCOPE)

- **Any new wholesale trainer rebuild** — FUT-01 itself shipped in v2.0 (`PROJECT.md:344`). GAP-57-01 authorizes only the bounded causal-loss and collocation-path conformance patch; it does not authorize rebuilding the package again.
- **Stage-1+ / PLAT-01..07 platform work** — SCOPE-36; re-opens only on a `go` verdict at DIAG-06 (Phase 58).
- **The DIAG-06 go / adjust / rethink verdict and VER-21 traceability close** — Phase 58, owner checkpoint ⑤.
- **Any second held-out evaluation** — SCOPE-35; requires a new owner decision.
- **Re-tuning `η_c` / `R_ref` / `ω₀` / `N_t` against an observed result** — SCOPE-37; a new owner decision, not Phase 57 work.

PH57-7KQ2-ZM9A_END
</context_copy>

[VERIFIED: `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-CONTEXT.md:91-403,616-641`; `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md:15-140`]
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| RUN-04 | Re-run Stage-0 under the corrected recipe; invariant B must show front advancement within the ratified window. | Exact production seam map, fixed-monitor/L-BFGS state design, conformance verifier, GATE-04 and smoke gates. |
| RUN-05 | Re-establish the comparable three-seed band. | Immutable final-HEAD sequence, config-delta proof, seeds 41/42/43, common evidence extraction. |
| EVAL-02 | Spend the sole evaluation once, after three preconditions and canonical-frame proof. | Dataset-free assembly regression, pre-access assertion, Phase-50 eligibility-only candidate selection, receipt check. |

[VERIFIED: `.planning/REQUIREMENTS.md:117-121` — the requirement IDs are quoted verbatim as `RUN-04`, `RUN-05`, and `EVAL-02`.]
</phase_requirements>

## Summary

The ratified recipe is precise enough for implementation without another scientific choice: `4096` total rows, `16` equal-time bins, `256` rows per bin, selected-slot allocation, one batch-global exclusive prefix, and one frozen `R_ref` used in both exponent and residual-wide outer physics loss. Resource inability at `4096` fails closed. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:452-458` — verbatim values: `n_col = 4096`, `M = 16`, and `exactly 256 rows per bin`.]

The current production controller does not execute that contract. `build_stage_batch` materializes selected-slot collocation rows, but Adam and L-BFGS ask for one row, discard `FixedBatch.collocation_points`, select one anchor identity, and draw a separate time vector. The causal loss then prefixes raw per-time residuals and normalizes neither exponent nor outer loss. [VERIFIED: `pinn/data/batches.py:314-414`; `pinn/training/controllers.py:560-702,1078-1085,1300-1335`; `pinn/loss_catalog.py:283-347`.]

**Primary recommendation:** make the existing production owners conform exactly, finalize and execute the exact GATE-04 rule so it refreshes the governed `R_ref`, then prove the real controller path separately against that final artifact before permitting smoke → graded band → eligibility-only candidate finalization → exactly one evaluation. No training begins during implementation or verification.

## Project Constraints (from AGENTS.md)

- Use the STOP protocol for an ungrounded semantic, process-schema, or cross-phase decision; this research found none beyond the resolved records. Preserve unrelated worktree changes. [VERIFIED: `AGENTS.md:39-119`.]
- Work on `milestone/v2.3` in the `trainex` worktree; run status/worktree checks before phase operations and commits. Use `scripts/agent-commit` with explicit owned paths if a later executor commits. [VERIFIED: `AGENTS.md:153-231`; read-only checks on 2026-09-08 found HEAD `7ec4f54b` and pre-existing unrelated changes.]
- Do not broaden the production patch, access held-out data during implementation, change framework specs, or train before the ordered gates. [VERIFIED: `57-CONTEXT.md:27-89,302-352`.]

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale |
|---|---|---|---|
| Exact selected-slot collocation allocation | Data/batch | Training controller | Batch construction owns rows; controller must consume, not redraw. |
| Causal arithmetic and gradients | Loss | Physics residual | Loss owns normalized prefix/reduction; residual path supplies differentiable row values. |
| Frozen monitor and L-BFGS segment | Training controller | Checkpoint | Runtime owns evaluation cadence; checkpoint owns exact resume bytes/state. |
| Recipe/provenance wiring | Training entry/config | Checkpoint | Strict config and launch path bind the measured artifact to a run. |
| GATE-04 and production proof | Verification | Training/loss/data | Gate must exercise imported production arithmetic and fail closed. |
| Candidate/evaluation discipline | Evidence/evaluator | Split/validation gate | Structural selection precedes the single protected held-out access. |

[VERIFIED: `pinn/data/batches.py:314-414`; `pinn/loss_catalog.py:283-347`; `pinn/training/controllers.py:492-702,1078-1085,1300-1335`; `pinn/train.py:683-712,1031-1208`; `pinn/evaluate.py:323-425`.]

## Standard Stack

### Core

| Component | Version/source | Purpose | Direction |
|---|---|---|---|
| Python | `3.11.15` | Production/test runtime | Keep `pinn-train`; do not alter environment. |
| PyTorch | `2.12.1` | AD, optimizers, checkpoint tensors | Use existing tensor/autograd paths. |
| NumPy | `2.4.6` | Evidence/probe numerics | Use existing dependency only. |
| `unittest` | stdlib | Focused and dataset-free tests | New Phase-57 critical tests must not import pytest. |

[VERIFIED: environment probe in `pinn-train`, 2026-09-08; `57-CONTEXT.md:315-337`.]

No package installation is authorized or needed; therefore no package-legitimacy audit applies. [VERIFIED: `57-CONTEXT.md:354-370` says the discretionary choices must `add no dependency`.]

## Architecture Patterns

### Execution and Gate Flow

```text
ratified §3.2 + frozen R_ref
        ↓
focused tests → bounded production conformance → exact complete GATE-04
                                                    ↓ PASS refreshes governed R_ref
final-R_ref-bound independent real-path proof ──────┴─→ fail: stop/block safely
        ↓ pass
final-HEAD seed-42 calibration smoke
        ↓ pass, then no commit
graded seeds 41/42/43 → invariant-B decision
        ↓ advance                         ↓ halt: terminal/unspent
Phase-50 structural eligibility: 42 → 41 → 43
        ↓ eligible
three EVAL-02 preconditions + pre-access frame assertion
        ↓
exactly one evaluation of selected `best.pt`
```

[VERIFIED: `57-CONTEXT.md:27-89,141-300,339-403`; `57-RULING.md:15-140`.]

### Component and Symbol Map

| Existing path / symbol | Observed state | Required bounded change |
|---|---|---|
| `pinn/data/types.py::{PhysicsCollocationPoints,FixedBatch}` | Exact fields are `"times", "tau_ic13", "masses", "record_keys"` and `"data_points", "collocation_points", "replay_keys", "lookahead_keys"`. | Preserve the carrier; make rows encode exact bin/slot allocation or add only the minimal provenance needed to verify it. |
| `pinn/data/batches.py::{allocate_collocation_quota,sample_collocation_points,build_stage_batch}` | Already expands selected-slot records to an exact total, but uses global uniform draws rather than the ratified 16-bin scheme. | Materialize all 4096 rows: full 256 slots × 16 bins; replay-only policy exactly as §3.2; fail closed if incomplete. |
| `pinn/training/controllers.py::{_stage_batch,_select_anchor_key,_build_anchor_context,_non_data_terms}` | Requests `collocation_count=1`, ignores materialized rows, and computes physics for one anchor. | Remove anchor-only physics from the production causal path; consume every selected-slot row and preserve complete-bin aggregates across microbatches. |
| `pinn/loss_catalog.py::causal_physics_loss` | Forms a raw exclusive prefix and `(weights * rbar).mean()`. | Accept 16 raw bin means plus frozen positive `R_ref`; normalize exponent and outer residual term; expose raw/normalized diagnostics; retain residual gradients. |
| `pinn/training/guards.py::InvariantBGuard` | Consumes current batch `w_n_stats`; state is front high-water and last advancement step. | Feed one persisted frozen training-only monitor; keep resampled fronts diagnostic-only and retain `front_advance_window_n = 500` as the separate step deadline/high-water rule, never as monitor cardinality. |
| `pinn/training/controllers.py` L-BFGS segment | Freezes scheduled λ values and times locally, but causal weights are recomputed by closures and segment state is not resumable. | At handoff freeze samples and detached causal weights for the entire segment; closures recompute residuals only; persist and exact-restore or fail closed. |
| `pinn/training/checkpoint.py`, controller state, `train.py` restore/hooks | Required checkpoint keys are `"model", "optimizer", "curriculum", "rng", "counters", "config_identity", "schema_version"`; monitor/L-BFGS state is absent. | Extend versioned payload/restore validation for monitor provenance and active segment state without weakening existing required keys. |
| `pinn/verification/gate04_train_free.py::{condition_ii_verdict,gate04_verdict}` | Condition ii raises `NotImplementedError`; unratified tuple is `("ii",)`. | Encode the owner formula and require empty unratified conditions plus complete PASS across all six cases. |
| `pinn/evaluate.py::evaluate_run` | Builds the test adapter after claiming an attempt; no explicit ratified-frame assertion precedes test materialization. | Add committed dataset-free assembly regression and assert the canonical frame before constructing any test split object. |
| archived Phase-50 `build_phase50_evidence.py::{_structural_facts,cmd_candidate}` | Selects the first structurally eligible seed and hashes `best.pt`; tests cover fallback/no-candidate. | Copy the bounded pattern forward; use fixed order 42→41→43 and never consult scientific metrics. |

[VERIFIED: `pinn/data/types.py:283-320`; `pinn/data/batches.py:149-175,314-414`; `pinn/training/controllers.py:492-702,1078-1085,1300-1335`; `pinn/loss_catalog.py:283-347`; `pinn/training/guards.py:320-362,487-617`; `pinn/training/checkpoint.py:31-43`; `pinn/verification/gate04_train_free.py:1-159,316-486`; `pinn/evaluate.py:323-425`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:722-820`.]

### Required Arithmetic Pattern

The production loss should implement exactly this already-ratified relationship, not a tunable variant:

```python
# x[b] = raw_bin_mean[b] / frozen_r_ref, b=0..15
prefix = exclusive_cumsum(x)          # one global prefix
weights = exp(-prefix)                # eta_c = 1
loss_phys = mean(weights * x)          # R_ref also normalizes outer loss
```

For GATE-04 quote the fixed values verbatim: `P_15 = sum(x_b for b = 0..14)`, `alpha = log(2) / (2 * P_15)`, `w'_15 = 1 / sqrt(2) ~= 0.707106781187`, and require `front_idx = 15` with every perturbed weight at least `0.70`. [VERIFIED: `57-RULING.md:31-75`; `pinn_architecture.md:452-458`.]

### Ordered Implementation Waves

1. **Focused tests first:** add pure-`unittest` Phase-57 tests for exact full/replay-only allocation, all-slot contribution, single-prefix normalized loss and gradients, raw/normalized diagnostics, 4096 fail-closed behavior, frozen monitor/resume, and L-BFGS closure/outer-call immutability.
2. **Bounded production conformance:** update batch, loss, controller, strict config wiring, checkpoint/restore, and v2.3-derived configs only where the tests demand the ratified behavior.
3. **Complete GATE-04 and refresh `R_ref`:** replace the unratified condition with the fixed owner rule, update gate tests/evidence generation, run the explicit Phase-57 CLI, require a fresh six-case complete PASS, and refresh the governed artifact with matching evidence provenance. Shell exit success alone is insufficient; inspect the persisted verdict and both artifacts.
4. **Separate production-path verification against final `R_ref`:** add a dataset-free verifier under `pinn/verification/` that instruments the real `RunController` path and proves allocation, loss equivalence, nonzero/all-slot gradients, diagnostics, monitor immutability, and checkpoint round-trip while recording and validating the refreshed artifact hash/provenance. Do not accept a probe-only helper as proof of training wiring.
5. **Calibration smoke:** after all code/test/config commits, confirm the full admitted corpus is reachable and run seed 42 `--stage-0-only`; preserve timing and `S_H`/split evidence.
6. **Graded band:** make no commit after smoke; launch seeds 41/42/43 with only `run.seed` and `run.run_name` differing. Any invariant-B HALT takes the declared terminal branch.
7. **Candidate and EVAL-02:** finalize structurally in order 42→41→43; verify all three preconditions and canonical-frame pre-access assertion; invoke the evaluator exactly once on the selected `best.pt`.

[VERIFIED: `57-CONTEXT.md:91-403`; `57-RULING.md:15-156`; `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:452-458`.]

## Don't Hand-Roll

| Problem | Do not build | Use instead |
|---|---|---|
| Collocation carrier | Parallel ad-hoc tensors detached from selected records | Existing `PhysicsCollocationPoints` in `FixedBatch`. |
| Physics AD | Finite differences or duplicate force equations | Existing `physics_residual` callable/AD path. |
| Single-use evaluation | New marker protocol | Existing attempt/receipt claim in `pinn/evaluate.py`. |
| Candidate selection | Metric-based ranking | Phase-50 structural-facts/candidate machinery with fixed fallback order. |
| `R_ref` | Online/refitted scalar or hard-coded measured number | Frozen provenance-validated Phase-56 artifact. |

[VERIFIED: `pinn/data/types.py:283-320`; `pinn/physics_residual.py:238-292`; `pinn/evaluate.py:69-108,323-425`; `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:722-820`; `pinn_architecture.md:452-458`.]

## Common Pitfalls

- **Count-only conformance:** setting 4096 while keeping random global times, one anchor, or per-microbatch prefixes is still nonconformant. Assert the slot/bin multiset and one global aggregate. [VERIFIED: `pinn_architecture.md:452-456`.]
- **Weight-only normalization:** dividing only returned weights or only the exponent leaves the outer physics loss wrong. Assert both exponent and residual-wide loss use the same frozen `R_ref`. [VERIFIED: `pinn_architecture.md:452-454`.]
- **Breaking gradients with frozen weights:** only causal weights are detached for L-BFGS; trial residuals must retain gradients. Compare analytic/finite perturbation behavior in focused tests. [VERIFIED: `57-RULING.md:119-131`.]
- **Resume drift:** a regenerated monitor or L-BFGS sample set changes the experiment. Byte-identical restore is required; malformed/missing active state fails closed. [VERIFIED: `57-RULING.md:101-131`.]
- **Gate false positive:** the current CLI can finish while condition ii is unratified. Require verdict `PASS` and no unresolved/unratified conditions in the persisted artifact. [VERIFIED: `pinn/verification/gate04_train_free.py:382-444,1007-1108`.]
- **Calibration invalidation:** any commit after smoke changes the `git_head` fingerprint and invalidates graded launches. [VERIFIED: `57-CONTEXT.md:218-240`.]
- **Selection leakage:** validation loss, front trajectory, or any observed scientific value cannot trigger fallback. [VERIFIED: `57-RULING.md:135-151`.]
- **Premature held-out access:** the frame assertion must run before any test `StageIndex`/adapter construction, not merely before metric computation. [VERIFIED: `57-CONTEXT.md:254-300`; `pinn/evaluate.py:323-425`.]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | Python stdlib `unittest` in `pinn-train` |
| Focused command | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phase57 -p 'test_*.py' -v` |
| Adjacent regression | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase39.test_batches -v` plus pure-unittest Phase-48/49/50 modules selected by the plan |
| Gate command | Run `python -m pinn.verification.gate04_train_free` under `pinn-train`, then validate persisted complete-PASS JSON |

[VERIFIED: `57-CONTEXT.md:315-337,354-370`; `tests/phase39/test_batches.py:65-103`; `tests/phase50/test_candidate_finalization.py:40-105`.]

### Requirement-to-Test Map

| Requirement | Automated proof before expensive execution | Status |
|---|---|---|
| RUN-04 | Allocation/loss/gradient/controller/monitor/L-BFGS/resume unit tests; production-path verifier; complete GATE-04 | Wave 0/2 additions required |
| RUN-05 | Config-delta test; split/`S_H` equality check; per-seed run-evidence schema | Existing Phase-50 pattern, Phase-57 copy required |
| EVAL-02 | Dataset-free canonical assembly; assertion-before-test-access; structural fallback/no-candidate; single-use receipt | Existing machinery plus Phase-57 regression required |

### Sampling Rate

- Per implementation task: focused Phase-57 `unittest` command.
- Per wave: focused suite plus adjacent pure-`unittest` regressions.
- Pre-run phase gate: production-path verifier and fresh complete GATE-04 PASS.
- No training is a test substitute; smoke begins only after code verification completes.

## Environment Availability

| Dependency | Required by | Available | Version/status | Fallback |
|---|---|---|---|---|
| `conda` | All production checks/runs | yes | `26.3.2` | none needed |
| `pinn-train` | PyTorch runtime | yes | Python 3.11.15; torch 2.12.1; MPS available | fail closed if unavailable |
| `pytest` in `pinn-train` | Not required | no | absent | stdlib `unittest` |
| admitted data root | Smoke/runs only | path exists | parent `simulation_data/Data` present; corpus contents not accessed | resolve approved root before smoke |

[VERIFIED: read-only environment probes on 2026-09-08; `57-CONTEXT.md:315-337`.]

## Security Domain

Authentication, sessions, access-control services, and cryptography are not part of this local training phase. The applicable controls are input/provenance validation, resource exhaustion, split-boundary enforcement, and tamper-evident evidence. [VERIFIED: inspected production and phase scope; `57-CONTEXT.md:27-89`.]

| ASVS / threat | Applies | Required control |
|---|---|---|
| V5 input validation / Tampering | yes | Strict config keys; finite positive `R_ref`; artifact schema/provenance/hash; fail closed on malformed checkpoint/state. |
| V4 access control / Information disclosure | analogous data boundary | Training monitor may contain training split only; evaluator assertion precedes held-out materialization. |
| Resource exhaustion | yes | Attempt exact 4096 rows; resource failure blocks rather than silently reducing count. |
| V2/V3/V6 | no | No authentication, session, or cryptographic surface is introduced. |

[VERIFIED: `pinn/training/config_yaml.py:197-248`; `57-RULING.md:101-151`; `pinn_architecture.md:452-458`; `pinn/evaluate.py:323-425`.]

## Assumptions Log

None. All semantic and numeric choices used here are ratified or directly observed; mechanical naming/layout remains within the recorded discretion.

## Open Questions

**RESOLVED — no planning decision remains.** Resource feasibility is an execution-time preflight fact, not an open scientific or planning choice. The already-ratified outcome is fail closed and leave the phase incomplete on resource failure; never lower the 4096-row count. [VERIFIED: `57-CONTEXT.md:91-139`; `pinn_architecture.md:454-458`.]

## Sources

### Primary (HIGH confidence)

- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-CONTEXT.md`, `57-RULING.md`, `57-GAPS.md` — scope and resolved owner decisions.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:429-458` — authoritative amended §3.2 contract.
- `pinn/data/{types,batches}.py`, `pinn/loss_catalog.py`, `pinn/training/{controllers,guards,checkpoint}.py`, `pinn/train.py` — production execution seams.
- `pinn/verification/{architecture_characterization_probe,gate04_train_free}.py` and Phase-56 tests/evidence — train-free arithmetic and incomplete-gate seam.
- Archived Phase-50 preregistration, evidence builder, and candidate-finalization tests — structural eligibility and single-look precedent.
- `pinn/evaluate.py`, `pinn/training/validation_gate.py` — evaluation and canonical-frame boundary.

## Metadata

**Confidence breakdown:** Standard stack HIGH (live environment); architecture HIGH (source paths read directly); pitfalls HIGH (ratified contract compared with current production); validation HIGH (existing adjacent tests and runtime probed).  
**Research date:** 2026-09-08  
**Valid until:** Phase-57 implementation changes these mapped seams.
