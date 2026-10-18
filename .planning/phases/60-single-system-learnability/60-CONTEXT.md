# Phase 60: Single-System Learnability - Context

**Gathered:** 2026-10-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 60 builds the diagnostic learnability harness, fixes network scoring on MPS, and runs the single-system arms. What those arms measure, which records they train on, and when Rung 2 and the probes are skipped is locked in `60-SPEC.md`. This context locks how the arms are trained, halted, scaled, stored, and authorized.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**8 requirements are locked.** See `60-SPEC.md` for full requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `60-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- The SCOPE-39 / FEAS-04 / FEAS-09 / SCOPE-44 / roadmap amendment
- The learnability harness and INST-05 tests (a)–(e)
- The in-place GAP-59-13 scorer fix and its MPS regression test
- The run protocol, committed before the first real rung
- Rung 1 on 1632, 851, and 4658
- The G2 sweep, confirmation, and checkpoint ④ hold
- Rung 2a and Rung 2b when the ladder continues
- The uncovered system's data-only Rung 1 when the owner continues
- The two hard-stage probes when the ladder continues
- Skip records, machine hours, and the Phase 64 handoff on a stop

**Out of scope (from SPEC.md):**
- Editing the frozen scorecard
- Editing `pinn_architecture.md` or the other framework specs
- Conformance, per-slot physics, telemetry, and the observe-only trainer modes
- Rung 3, the 16-system family, and the validation-panel accuracy curve
- The corrected control
- The verdict document and the charter
- A second seed, a second confirmation, or a silent restart
- Graded runs, held-out evaluation, and test-split files
- Curriculum training beyond Stage 0

</spec_lock>

<decisions>
## Implementation Decisions

### Learning-rate schedule

- **D-01:** Physics arms use the ratified Adam schedule and do not change it. Initial rate `LR_k = 1e-3 × (0.7)^k`, cosine annealing to zero over that arm's step budget, Adam `β1 = 0.9`, `β2 = 0.999`, `ε = 1e-8`, and the PHYS-05 warmup. SCOPE-41 forbids a different schedule. Stage 0 uses `k = 0`. Stage 4b uses `k = 4`. Stage 6 uses `k = 6` (`1e-3 × 0.7^6 ≈ 1.18e-4`).
- **D-02:** The cosine's step count is the frozen 3-hour cap divided by that arm's timing-run seconds per step. The timing run is not part of the cosine.
- **D-03:** The one ×2 extension, if the frozen still-improving test grants it, is a second cosine of that same length. It starts again at that stage's initial rate, keeps Adam's state, and does not repeat the physics-weight ramp.
- **D-04:** Every data-only arm uses the Stage-0 cosine (`k = 0`), not the Phase 38 constant `1e-3`. The frozen still-improving test is unchanged. Its 75%–100% window is therefore the low-rate tail of the cosine, and the readout says so.
- **D-05:** Probe Rung-2b arms use that stage's `LR_k`, not Stage 0's rate. The readout names the confound: the 0.7 factor assumes weights carried forward from the previous stage, and these probes start from scratch.

### No self-halt

- **D-06:** A physics arm never halts on invariant B or any other causal-front rule. On the budget-rule readings (both ends, and no gap larger than 5% of the step budget), it logs the frozen monitor's per-bin causal weights and front. It does not run a live 256-identity monitor every step. Phase 61 builds the observe-only guard. This phase does not.

### R_ref and GATE-04

- **D-07:** If the owner continues at checkpoint ④, re-measure `R_ref` and re-run GATE-04 at the approved `first_omega_0` before any physics arm. Neither step trains. GATE-04 is the ratified complete-pass rule in `57-RULING.md` (GAP-56-01): non-anchor spread at least 2:1, then the fixed residual reduction. A fail stops for the owner. The checkpoint question says that continue includes this step.
- **D-08:** Probe physics arms reuse the committed Stage-0 `R_ref`. They do not re-measure it. `R_ref` is ratified for the whole of Stage 0. The probes are Stage 4b and Stage 6, and none of the invalidation triggers in `pinn_architecture.md` change for them: `T = 10`, and the six measurement cases use no real system. The run record says the value is the Stage-0 reference applied unchanged.

### Phase 59 verifier after the scorer fix

- **D-09:** `verify_phase59_evidence.py` accepts exactly one successor SHA-256 for `pinn/verification/feasibility_scorer.py`, named in a committed Phase 60 record. Every other producer hash is still checked against the Phase 59 result files. Phase 59 evidence is not re-run, and Phase 59 is not reduced to "verifies only at `45f65228`".

### Weights in git

- **D-10:** Both scored states of every real arm are committed in plain git, not Git LFS. That is about 2.8 MiB per state: about 45 MiB on the stop path (8 arms, counting one confirmation) and about 106 MiB on the continue path (19 arms). Resume checkpoints and timing-run weights stay out of git. Re-deriving a result re-scores the committed weights.

### Checkpoint ④ authorization

- **D-11:** A continue-path arm is legal only when a committed ruling file quotes the owner's message and names the approved `first_omega_0`. The file is written only from the owner's words. Every continue-path arm record cites it. A physics arm refuses any other value.

### Claude's Discretion

- The data term uses every point of the assigned record on each Adam step (1,001 on a gold record with `T = 10` and step 0.01). The polish uses that same set.
- The timing run is a separate run of at least 50 steps of the exact arm configuration, immediately before the arm. Its weights are discarded. The arm then starts from the seed-42 initialization, and its cosine covers only the arm's budgeted steps.
- Launch and resume use the generation-7 launcher's safeguards. A handler saves a checkpoint when the run is terminated or its terminal closes. Resume uses the trainer's L-BFGS segment state and refuses a resume that lacks it (`pinn/training/controllers.py`, the amended-checkpoint check near line 846 and `_start_lbfgs_segment` near line 2213). Line 262 is the record-key parser, not this check.
- The footprint preflight is unreliable on this macOS. Before a long arm, ask the owner to close browsers. The arm needs 6 GiB free.
- Module layout, the shape of the INST-05 tests, the plan split, and the order of the three Rung-1 arms are the planner's.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked phase contract
- `.planning/phases/60-single-system-learnability/60-SPEC.md` — locked requirements. Read before planning.
- `.planning/REQUIREMENTS.md` — SCOPE-39, SCOPE-41, SCOPE-44, FEAS-03, FEAS-04, FEAS-09, INST-05
- `.planning/ROADMAP.md` — Phase 60 gate G2 and success criteria

### Schedule, reference scale, and the gate
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Adam schedule at the stage-start block (`LR_k = 1e-3 × (0.7)^k`, cosine annealing) and the consolidated hyperparameter table
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — PHYS-05 warmup, and the frozen-residual-reference block whose invalidation list includes `first_omega_0`
- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md` — GATE-04 complete-pass rule (GAP-56-01)
- `pinn/verification/artifacts/r_ref_stage0.json` — the Stage-0 reference the probes reuse
- `pinn/verification/artifacts/feasibility_scorecard_v1.json` — budget, polish, tiers, and `g2_fires` inputs. Do not edit it.

### Code the harness extends
- `pinn/verification/overfit_probe.py` — the Phase 38 probe. Its constant `1e-3` is not the data-only schedule.
- `pinn/verification/feasibility_scorer.py` — `network_trajectory` and `tier_of`. The MPS fix lands here.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` — re-hashes `producer_sha256` for every Phase 59 result
- `pinn/training/controllers.py` — trainer loss path and the L-BFGS segment resume refusal
- `pinn/loss_catalog.py` — the trainer's loss functions the harness must call

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `pinn/verification/overfit_probe.py` — single-trajectory data-term training. The harness extends it and replaces the zero IC13 and the constant learning rate.
- `pinn/verification/gate04_train_free.py` — the train-free gate to re-run after an approved `first_omega_0` change.
- `pinn/verification/feasibility_scorer.py` — official scores. Widen MPS tensors on the CPU before float64.
- Phase 59's corpus allowlist — the way to read a gold record without teaching the production base-only pool to accept gold.

### Established Patterns
- `verify_phase59_evidence.py` fails when a named producer's current SHA-256 differs from the result file. A successor has to be an explicit exception, not a silent hash edit.
- Resume checkpoints already carry `lbfgs_segment_state`. A resume without it is refused.
- Generation 7's launcher is the safeguard pattern SCOPE-44 names: detached, one run at a time.

### Integration Points
- The harness calls the trainer's loss functions. It does not enter the production training loop, so the production invariant-B halt does not apply unless this phase adds it. D-06 says not to add it.
- `decision_verdict` already refuses later-rung inputs after G2 fires. The harness must not work around that.
- Continue-path physics arms read the D-11 ruling file before they accept a `first_omega_0` other than 30.

</code_context>

<specifics>
## Specific Ideas

- Compare every data-only arm with Rung 2 under one Stage-0 cosine, so a data-only failure is not an artifact of the Phase 38 constant rate.
- The still-improving test will see the cosine's low-rate tail. Keep the frozen test and name that fact in the readout.
- SCOPE-44's 15-hour sweep and 12-hour probe estimates omit the polish, which can add 25% of Adam's running time. At 3.75 hours per arm the stop path is about 30 hours and the continue path about 71 hours, before any granted extension. An extension doubles that arm. These are planning notes. They do not change the frozen caps.
- A stop with no Tier ≥ 1 setting has seven arms, not eight, because there is no confirmation. The 45 MiB figure counts one confirmation.

</specifics>

<deferred>
## Deferred Ideas

- The observe-only invariant-B guard and plateau detector are INST-07 in Phase 61. This phase only logs the frozen monitor on the budget-rule readings.
- Closing the stale `trainex-r1` handoff todo is housekeeping outside Phase 60. The r1a and r1b results are already committed, and rounds r2–r4 followed. The todo still says R1b has not returned.

### Reviewed Todos (not folded)

- **D-06 static-epsilon sensitivity check** — not folded. It asks whether training softening `1e-5` versus offline energy checks at `1e-10` moves stage labels or validation gates. Phase 60 sets neither. The closest approach in any record this phase trains on is 0.0050 on 2279 gold, where the two softenings differ by about 2 parts in a million. Phase 59's survey already found 33 of 12,023 records within `1e-3`, all in Stages 5–6, and none within `1e-4`, measured on saved time points. Leave it for whichever work next sets stage labels or gates.
- **trainex-r1 research handoff** — not folded. It is finished. Close the stale todo outside this phase.

</deferred>

---

*Phase: 60-Single-System Learnability*
*Context gathered: 2026-10-18*
