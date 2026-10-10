# Requirements: v2.4 Stage-0 Feasibility Checkpoint

**Defined:** 2026-10-09
**Core value:** An evidence-backed answer to whether the CTL-PINN approach can learn three-body motion at all — measured in physical units on a ladder of experiments from one Stage-0 system to the full Stage-0 control, and ending in a go / pivot-training / rethink-representation verdict on which the owner decides whether the project continues.
**Total:** 20 requirements (6 FEAS + 2 DIAG + 3 INST + 2 CONF + 4 SPEC + 1 GATE + 1 RUN + 1 VER) + scope boundaries SCOPE-39..44.

**Source:** the v2.4 roadmap proposal
(`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`),
ratified under owner delegation on 2026-10-09 at commit `0b400dfa`. It builds
on the `trainex-r4` decision-sheet ruling
(`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/trainex-r4-ruling.md`,
`c4bea18a`), whose picks, composed control and pre-registered readout it keeps.

## Why this milestone exists

After four build milestones (v2.0–v2.3) the owner has no assurance that the
project can work. The record explains why:

- **No conformant training run exists.**
  - The v2.0 pilot diverged from the locked specs in five verified ways (v2.1
    audit).
  - Generation 7 of v2.3 evaluated the physics term on one trajectory per
    step, the lowest-ID replay draw (`milestones/v2.3-GAPS.md`, "Post-close
    finding").
- **No test has measured a trained network's accuracy in physical units,**
  apart from energy-error gates on those non-conformant runs:
  - v2.0's held-out `ε_H` was 237.2.
  - Generation 7's worst-case validation `ε_H` over 227 systems was 15.65 at
    step 100 and 50.63 at step 900 (`runs/stage0-v23g7-seed42/validation.jsonl`),
    while its validation loss fell from 16,499 to 5,278.

  The locked bar is `10⁻⁵` (`pinn_architecture.md:1087`).
- **The only evidence the network can learn at all is a wiring check.** The
  data-matching loss fell at least 1,000-fold on one trajectory, with the 13
  starting-condition inputs set to zero (Phase 38 NET-05,
  `pinn/verification/overfit_probe.py:1-9`).
- **The ruling's corrected control is narrower than the owner's question.** It
  shows whether the causal front advances at full scale. It does not show
  whether the network reaches useful accuracy, or where it breaks.

v2.4 answers the owner's question (2026-10-09, verbatim in the proposal: *"I
have not yet obtained any kinds of assurance as to is this actually doable"*)
with a ladder of experiments. Each rung is cheaper than the next. Each is
scored in physical units against a scorecard frozen before it runs. A failure
at any rung shows which part is the bottleneck.

## Grounding (authoritative inputs)

1. **The v2.4 proposal** (`0b400dfa`) and the **`trainex-r4` ruling**
   (`c4bea18a`). The ruling's own basis is the consolidated document
   (`53b7c008`), the Rule-19 verification (`b4b975e9`, `d97328d4`,
   `654d6ffe`) and the re-framing ruling R-1..R-7 (`DELIVERY-NOTE.md`).
2. **The locked framework specs** (`ctl_instruction.md`,
   `pinn_architecture.md`) as amended through v2.3 (SPEC-01..06, Phases 53 and
   56).
3. **The v2.3 closure record:** `milestones/v2.3-GAPS.md` ("Milestone close"
   and "Post-close finding"), `58-VERDICT.md`, `57-RULING.md` and
   `54-RULING.md`.
4. **Existing tooling:**
   - the Phase-38 overfit probe (`pinn/verification/overfit_probe.py`);
   - the INST-04 architecture characterization probe;
   - GATE-04 (`gate04_train_free.py`);
   - the generation-7 launcher.
5. **Dataset facts:** 1,812 Stage-0 training systems (`n_train`,
   `runs/stage0-v23g7-seed42/training_metadata.json`) and 227 Stage-0
   validation systems (`validation.jsonl`, `gate_n_trajectories`).

**Not reopened:**

- the 14D `[τ, IC₁₃]` input, Jacobi IC₁₃, the COM projection head;
- PHYS-03 softening, the raw-mass `D` convention;
- the v1.5–v2.3 data, validation and conformance contracts;
- the v2.3 recalibration (`A1 + B2 + C1 + D3 + E1`, `R_ref` normalization,
  4096 rows in 16 bins);
- every `trainex-r4` pick (`JD-0`..`JD-11`) and answer (`OQ-1`..`OQ-5`).

## v2.4 Requirements

### Feasibility Ladder & Verdict (FEAS)

- [ ] **FEAS-01**: **Pre-register the feasibility scorecard before any rung runs.** It has four parts.
  - **(i) Metrics in physical units,** each over the whole window against the Brutus reference:
    - the position error of the network's trajectory, both for the three bodies (normalized by the system's size) and for the inner pair's separation vector (normalized by the inner separation), so that a good outer orbit cannot hide a wrong inner binary;
    - the valid-horizon fraction `h_δ` for `δ` = 1% and 10%;
    - the gate's own `ε_H = max_t |(H(t) − H(0)) / H(0)|`, from the network's positions and autograd velocities (`ctl_instruction.md:567`);
    - the physics residual normalized by `R_ref`, for context only.
  - **(ii) Tiers 0–3 per system,** where Tier 3 is the locked `10⁻⁵` bar.
  - **(iii) The budget rule,** including the definition of "still improving" and the single doubling extension.
  - **(iv) The decision rule:** RETHINK-REPRESENTATION, PIVOT-TRAINING or GO, as drafted in the proposal.

  **Acceptance:**
  - The scorecard and a scorer under `pinn/verification/` are committed before the first rung's run record.
  - A test shows that the scorer, given the Brutus reference against itself, returns zero position error and the reference's own `ε_H`.
  - No threshold is set after any result is seen (SCOPE-42). [proposal "The feasibility scorecard"]
- [ ] **FEAS-02**: **A Stage-0 difficulty census, and the panels drawn from it.** The census uses Brutus training-split data alone.
  - **Per system:** inner and outer revolutions per window, minimum and maximum pairwise separation, and the acceleration range.
  - **Panel selection** follows a deterministic rule declared before the census runs:
    - three single-system panel members at declared quantiles of the difficulty measure (easy, median, hard);
    - a 16-system panel spanning the census;
    - a validation panel drawn from the 227 validation systems.

  **Acceptance:**
  - The census script and its output are committed and re-derivable.
  - The panel IDs are committed with their rule before any rung runs.
  - No test-split file is opened, and this is asserted, not assumed. [proposal Phase 59]
- [ ] **FEAS-03**: **Rung 1, the supervised ceiling.** The data-only arm of the INST-05 harness runs on each of the three panel systems, within FEAS-01's budget rule.

  **Acceptance:**
  - Each system has its tier, `h_δ`, `ε_H` and convergence trace recorded.
  - Gate G2 is evaluated and recorded: Rung 1 below Tier 1 on 2 or more of 3 means RETHINK-REPRESENTATION, and the milestone skips to Phase 64. [proposal Phase 60]
- [ ] **FEAS-04**: **Rung 2, learning from the physics.** Two arms run on the same three systems:
  - **(a) physics + IC only:** the ratified causal physics term with `R_ref` normalization, plus the IC term, and no data term;
  - **(b) the full ratified loss.**

  **Acceptance:**
  - Each arm and system has its tier, `h_δ`, `ε_H` and trace recorded.
  - The comparison against Rung 1 is recorded.
  - Arm (a) is reported and does not gate. It decides how the method is described: a solver that learns from the equations, or a surrogate that physics regularizes. [proposal Phase 60]
- [ ] **FEAS-05**: **Rung 3, the small family.** The corrected trainer runs in diagnostic mode (INST-07) on the 16-system panel, within FEAS-01's budget rule. It is scored on the 16 training systems and on the validation panel.

  **Acceptance:**
  - Each system has its tier recorded.
  - The count at Tier 1 or above is compared with the decision rule.
  - Validation-panel scores are reported as an early, non-gating signal. [proposal Phase 62]
- [ ] **FEAS-06**: **The feasibility verdict.** A document, written plain language first, records:
  - the tier each rung reached, and where along the window each broke;
  - the control's readout branch;
  - the best `ε_H` reached, against the locked bar;
  - the result under FEAS-01's pre-registered rule;
  - the next milestone the result routes to.

  It is presented at owner checkpoint ①.

  **Acceptance:**
  - The owner's decision is recorded verbatim: continue, change course or stop, together with whether the `10⁻⁵` held-out bar stays the success criterion.
  - Every exit path reaches this requirement, including an early exit at G2 or an unfixable gate. [proposal Phase 64]

### Diagnostics & Readout (DIAG)

- [ ] **DIAG-07**: **The ruling's read-only experiments on retained generation-7 checkpoints,** run against the code that produced them:
  - **`JX-1` executed half:** per-term gradient decomposition, Adam-preconditioned shares, and the IC position/velocity split;
  - **`JX-2`:** monitor-estimator noise;
  - **`JX-3`:** the exposure panel, including validation-split trajectories;
  - **`JX-4`:** relative against absolute;
  - **`JX-5`:** Codex's initialization split, at the default architecture;
  - **`JX-10`:** verification completion.

  The ruling names checkpoint 900, but the retained set is `stage-0-init`, steps 931, 941 and 951, `best` and `latest`. The plan fixes the stand-in before running anything.

  **Acceptance:**
  - Each result is recorded with its command, its checkpoint provenance, and the reading it supports or falsifies.
  - Gate G1 is recorded: a `JX-1` physics share of `10⁻²` or more re-opens the conformance-first premise before Phase 61.
  - No training runs, and no test split is opened. [`trainex-r4-ruling.md`, "The experiments"; JX-1..JX-10 definitions in `trainex-r4-resolution-doc.md` JOIN-4]
- [ ] **DIAG-08**: **The pre-registered readout of the corrected control.** It takes exactly one branch, (a) to (d) (`trainex-r4-ruling.md:167-193`), and records the evidence for it. It is read together with FEAS-01's absolute measures on the validation panel (`JD-3`). [ruling `JD-3`, `JD-4`; proposal Phase 63]

### Instrumentation (INST)

- [ ] **INST-05**: **The learnability harness.** It is committed, tested tooling under `pinn/verification/` that extends the Phase-38 overfit probe. It trains the production architecture on a fixed panel of training-split systems under a named loss arm: data only, physics + IC, or the full ratified loss. It has:
  - real normalized IC13;
  - the trainer's own loss and residual functions, with no re-implementation;
  - FEAS-01's scorer at a fixed cadence;
  - a budget cap;
  - run records marked diagnostic;
  - refusal of test-split paths.

  **Acceptance:** tests prove each of these:
  - **(a)** the loss functions are the trainer's, by a mutation test in the manner of INST-04's SC3;
  - **(b)** test-split paths are refused;
  - **(c)** the graded-run and evaluator paths refuse a harness record;
  - **(d)** a short run completes on one system. [proposal Phase 60]
- [ ] **INST-06**: **`JD-10`, the full telemetry set.**
  - **Every step:** the selected identities, and the monitor's prefixes, front, high-water mark and threshold margins.
  - **Every 50 steps:** per-term gradient norms with Adam-preconditioned shares, and the IC position/velocity split.
  - **Also:** per-identity monitor profiles (`OQ-4`) and the `train.log` hand-off message fix (`C-F05`).

  **Acceptance:** a short synthetic run writes every field, and a schema test pins them. [ruling `JD-10`]
- [ ] **INST-07**: **The diagnostic modes.** There are three:
  - an **observe-only invariant-B guard:** the ratified rule (`57-RULING.md:95-107`) is computed every step on the corrected 256-identity monitor and logged with its margins and the step at which it would halt, and it halts nothing;
  - an **explicit, logged Adam-only switch,** not `max_epochs == n_adam`, which a plateau firing bypasses;
  - an **observe-only plateau detector.**

  The modes are written into the run's configuration record.

  **Acceptance:**
  - A test exercises each mode.
  - The graded-run path and the evaluator refuse any run record that used a diagnostic mode. [ruling `JD-4`, `JD-6`]

### Conformance (CONF)

- [ ] **CONF-10**: **`JD-0`, per-slot conformance.** Physics collocation rows, the invariant-B monitor and validation each use their own slot's IC13 and masses. The production-conformance verifier records the IC and mass inputs it evaluated, replacing the constant `"anchor_only": False` (`pinn/verification/phase57_production_conformance.py:533`).

  **Acceptance:**
  - An identity-dependent assertion: perturbing a non-anchor slot's IC13 must change both the physics loss and the IC loss. The assertion fails on the generation-7 code path and passes on the corrected one.
  - The corrected code consumes the batch random stream unchanged, checked against the replayed sequence (verification Part 1, A.2), so that the seed-42 pairing with generation 7 holds.
  - A mechanical code-against-spec check of each changed contract passes. A passing plan verification is not evidence. [ruling `JD-0`; `57-GAPS.md:214-218`]
- [ ] **CONF-11**: **`JD-1` B1: the IC term is the mean over the selected slots.** Each slot contributes the spec's per-trajectory `L_IC = L_IC,r + β_v L_IC,v` (`pinn_architecture.md:511-515`), with `λ_IC = 1` and `β_v = 1`. Replacement multiplicity is preserved, so a slot selected twice counts twice.

  **Acceptance:** a test shows that the IC loss equals the mean over slots, and that a duplicated slot counts twice. [ruling `JD-1`]

### Framework-Spec Clarifying Amendments (SPEC)

Each is a clarification of a silence or an inconsistency, not a value change.
The owner sees each and may veto it (owner checkpoint ②; SCOPE-43).

- [ ] **SPEC-07**: **Amendment: `JD-1`'s IC batch rule,** "the mean over the selected slots, multiplicity preserved", written where `L_IC` is defined (`pinn_architecture.md` §3, at `:511-515`). [ruling `JD-1`]
- [ ] **SPEC-08**: **Amendment: `OQ-2`, an "epoch" is one optimizer step** for budgets, the plateau window, the validation cadence and the replay rule. It rewrites the parenthesis "(standard once-per-epoch coverage)" (`ctl_instruction.md:1829`), and the replay sampler stays as executed. [ruling `OQ-2`]
- [ ] **SPEC-09**: **Amendment: `OQ-3`.** The invariant-B monitor contract (`57-RULING.md:93-110`) is transcribed into `pinn_architecture.md` §3.2, where `:452` cites "the fixed-monitor boundary above". No value changes. [ruling `OQ-3`]
- [ ] **SPEC-10**: **GAP-56-02, inherited and DEFERRED on 2026-10-04.** It decides and applies the §2.4 Table 1 locked-vs-default treatment of `first_omega_0`, whose "Recommended Value" header labels a §2.2-locked constant. The record's recommendation is a minimal footnote (option B, `56-GAPS.md`). [`milestones/v2.3-GAPS.md`, obligation 3]

### Gates (GATE)

- [ ] **GATE-05**: **Gates on the corrected code, fail-closed, before any run that uses it.** In order:
  1. `R_ref` is re-measured by the ratified six-case procedure (`pinn_architecture.md:454`).
  2. GATE-04 is re-run, and a complete PASS is required.
  3. The `OQ-1` check runs: with the re-measured `R_ref`, the frozen monitor's 256 training identities at initialization must give neither floor-bound nor degenerate weights (GATE-04's own conditions, `pinn_architecture.md:452`). If the probe passes and the monitor fails, stop: the probe is amended to training-split ICs before any run.
  4. `JX-1`'s conformant half runs at initialization, as structural evidence.

  **Acceptance:** provenance-bound artifacts for each step, and a failure blocks FEAS-05 and RUN-06. [ruling `JD-0`, `OQ-1`, `JX-1`]

### Control Run (RUN)

- [ ] **RUN-06**: **The corrected control, as composed in `trainex-r4-ruling.md:148-165`.**
  - **Seeds:** 42 first, then 41 and 43. If seed 42 exposes an implementation defect, that defect is fixed first.
  - **Run:** 1,000 Adam steps each, with the observe-only guard and plateau detector and the full telemetry.
  - **Not graded:** no graded slot, no evaluation.
  - **Launch:** detached, with the generation-7 launcher's safeguards.

  **Preconditions:** CONF-10, CONF-11, INST-06, INST-07 and GATE-05 pass.

  **Acceptance:** a complete run record per seed, or a recorded defect that stops the line. [ruling `JD-4`..`JD-7`]

### Traceability (VER)

- [ ] **VER-22**: **Traceability.** Every v2.4 requirement maps to exactly one phase, with no orphans and no duplicates. This is re-verified at close against the final requirement count, not carried forward from the roadmap-creation check. [VER-21 lineage]

## Scope Boundaries (ratified under owner delegation 2026-10-09; hard constraints)

| ID | Boundary |
|---|---|
| SCOPE-39 | **Stage-0 only.** No Stage-1+, no PLAT-01..07. SCOPE-36 is carried forward. |
| SCOPE-40 | **Nothing graded, nothing held out.** No graded run and no held-out evaluation in v2.4. No experiment opens a test-split file. The single preserved evaluation stays unspent (SCOPE-35 is carried forward; v2.4 spends nothing). |
| SCOPE-41 | **Every training run is diagnostic.** It runs in a configuration the graded-run path refuses, and it never alters the ratified recipe. The ladder's loss arms are measurement configurations, not recipe proposals. Recipe tuning stays out of scope (SCOPE-37's rule is carried forward). |
| SCOPE-42 | **Pre-registration.** Each rung's metrics, tiers, budget and consequences are committed before it runs, and a threshold is never re-set after a result is seen. A result outside the pre-registered branches goes to the owner. |
| SCOPE-43 | **Locked values move only by formal amendment** (SCOPE-38 discipline). v2.4's spec edits are SPEC-07..10 only: clarifications the owner can veto, with no recipe value changed. |
| SCOPE-44 | **Compute discipline.** Budgets are fixed from a measured seconds-per-step before launch, with at most one extension per arm. Runs execute one at a time, detached, with the generation-7 launcher's safeguards. |

## Owner Checkpoints

1. **The verdict (FEAS-06, Phase 64).** The owner decides whether to continue,
   change course or stop, and whether the `10⁻⁵` held-out bar stays the
   success criterion. This blocks the milestone's close.
2. **Spec amendments (SPEC-07..10, Phase 61).** The owner sees each and may
   veto it. This blocks only the amendment concerned.
3. **Off-script results.** Any result outside a pre-registered branch blocks
   only the work that depends on it (the ruling's "Later decisions" rule).

Everything else proceeds under the owner's delegation (2026-10-07, re-confirmed
2026-10-09) and is reported at each phase gate.

## Exit Paths (every path ends at the verdict)

| Exit | Trigger | What happens |
|---|---|---|
| Normal | Phases 59–63 complete | Phase 64 applies the decision rule to all the evidence |
| Early, at G2 | Rung 1 below Tier 1 on 2 or more of 3 systems | Phases 61–63 are skipped. Phase 64 records RETHINK-REPRESENTATION with the ladder evidence |
| Early, at G3 | A GATE-05 failure that cannot be fixed within the milestone | Phase 64 decides on the ladder evidence (Rungs 1–2, and Rung 3 if it ran) |
| Re-examination, at G1 | `JX-1` shows a physics share of `10⁻²` or more in generation 7 | The conformance-first premise of Phases 61–63 is re-examined before Phase 61 opens. If the plan changes, the change is recorded |

## Future Requirements (deferred beyond v2.4)

- **On GO:** a Stage-0 production-training milestone, covering training to
  convergence, graded seeds, and the preserved held-out evaluation under its
  preconditions. Stage 1 is planned from there.
- **The pre-registered next arms, by readout branch:**
  - (a) stage 2: the budget from the measured rate, reachable L-BFGS (`JD-6` B/C), the guard's statistic (`JD-4` B/C), and the absolute tolerances (`JD-3`);
  - (b) adaptive `λ_IC` (`JD-2` C), drafted as an amendment;
  - (c) the constant-rate arm (`JX-7`);
  - (d) the `JX-5` sweep, `JX-7`, and more seeds.
- **On RETHINK-REPRESENTATION:** representation pivots named at the verdict
  (for example time-windowed networks, a different output frame, input
  features or architecture, or a shorter window).
- **PLAT-01..07 and Stage-1+.** Blocked pending a GO.
- **The general verification-enforcement regime.** Inherited unchanged from
  v2.3.

## Out of Scope

| Exclusion | Reason |
|---|---|
| A graded run or any held-out evaluation | SCOPE-40. A feasibility milestone spends nothing; the evaluation stays preserved for a run that actually trains. |
| Tuning the recipe (weights, schedules, `η_c`, `ω₀`, architecture) | SCOPE-41. The ladder measures the ratified recipe; the readout pre-registers which arm comes next. |
| `JX-6` (`λ_phys = 0` on the executed code) | Declined by the ruling. It would train the non-conformant objective. Rung 1 is different: one system, on the harness, measuring the ceiling. |
| Changing the `10⁻⁵` held-out bar | The owner decides at the verdict. v2.4 only measures the distance to it. |
| Moving the v2.3 phase folders 53–58 | Decided in the proposal: they stay through v2.4, because the Phase-57 verifier and tests hardcode the path. |
| The 18 open items in STATE.md's Deferred Items | Outside this milestone's question; they stay deferred. |
| The GSD 4-agent domain-research pass | v2.0–v2.3 precedent. This milestone's research is the `trainex-r4` round. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FEAS-01 | Phase 59 | Pending |
| FEAS-02 | Phase 59 | Pending |
| DIAG-07 | Phase 59 | Pending |
| INST-05 | Phase 60 | Pending |
| FEAS-03 | Phase 60 | Pending |
| FEAS-04 | Phase 60 | Pending |
| CONF-10 | Phase 61 | Pending |
| CONF-11 | Phase 61 | Pending |
| INST-06 | Phase 61 | Pending |
| INST-07 | Phase 61 | Pending |
| SPEC-07 | Phase 61 | Pending |
| SPEC-08 | Phase 61 | Pending |
| SPEC-09 | Phase 61 | Pending |
| SPEC-10 | Phase 61 | Pending |
| GATE-05 | Phase 62 | Pending |
| FEAS-05 | Phase 62 | Pending |
| RUN-06 | Phase 63 | Pending |
| DIAG-08 | Phase 63 | Pending |
| FEAS-06 | Phase 64 | Pending |
| VER-22 | Phase 64 | Pending |

**Coverage:**
- v2.4 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0 ✓

---
*Requirements defined: 2026-10-09*
*Last updated: 2026-10-09 at roadmap creation*
