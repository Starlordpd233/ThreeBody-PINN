# Phase 59: Read-Only Baseline & Scorecard - Context

**Gathered:** 2026-10-11
**Status:** Ready for planning
**Source of decisions:** the orchestrator wrote these under the owner's standing
delegation (2026-10-07, re-confirmed 2026-10-09: *"I shouldn't be ruling on
anything"*), in place of an interactive discuss-phase. Every decision applies
the ratified v2.4 proposal (`0b400dfa`) as amended on 2026-10-11 (`e72060da`,
`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`).
None moves a locked value, spends the evaluation or pre-empts the verdict.

## In plain language

Phase 59 trains nothing. It builds the ruler and takes the measurements that
every later experiment is judged against:
- **the scorecard:** how a predicted orbit is scored, in physical terms, and
  the pass marks, frozen before any experiment runs;
- **how hard Stage 0 is:** how many inner laps each system makes, and how
  precisely a network would have to time them;
- **two no-learning comparison points:** a textbook two-orbit formula, and
  copying the nearest training system;
- **a read-only look at every later stage:** how chaotic and how violent each
  stage is;
- **the ruling's read-only checks on generation 7's saved checkpoints.**

<domain>
## Phase Boundary

**In scope:** FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07 (`.planning/REQUIREMENTS.md`).

**Out of scope:**
- any optimizer step on any network;
- any rung;
- any graded run or held-out evaluation;
- opening any test-split file;
- any framework-spec edit (SPEC-07..10 belong to Phase 61);
- recipe changes.

The DIAG-07 experiments compute forward and backward passes on retained
checkpoints. The ruling authorizes that, and no optimizer step is taken.

**Gate G1** (it gates Phase 61, not Phase 60): `JX-1` shows a physics share of
`10⁻²` or more of generation 7's Adam-preconditioned update → the
conformance-first premise is re-examined before Phase 61 opens.
</domain>

<decisions>
## Implementation Decisions

### 0. Post-research revisions (2026-10-11) — these override the decisions they name

`59-RESEARCH.md` found twelve places where the code or data contradicts or
under-specifies the decisions below. They were recorded in `59-GAPS.md` and
resolved under the owner's delegation before any code ran. Where this section
and a later decision differ, this section governs.

- **D-29: Checkpoint 900 is `best.pt`** (GAP-59-01; it revises D-22).
  - Assert `global_step == 900` in code.
  - `JX-1` reads `stage-0-init.pt` (step 0, no optimizer moments), `best.pt`
    (900) and `step-000951.pt` (951).
  - `step-000931.pt` and `step-000941.pt` are supplementary.
- **D-30: Velocity sources for `ε_H`** (GAP-59-02; it revises D-01 and D-04).
  - **Velocity source:** networks use autograd `dr′/du`, the formula its
    analytic velocities, and the copy Brutus's velocities.
  - **Hamiltonian:** computed with `gate_metrics.matched_plummer_hamiltonian_series`
    and `trajectory_eps_h`.
  - **Finite differences:** `compute_trajectory_gate_metrics` is never
    called by the scorer, and a static test enforces it. The
    finite-difference value is reported only as a labelled context column,
    for continuity with generation 7.
- **D-31: The dense grid is tier-defining** (GAP-59-07; it revises D-02's grid).
  - **Grid:** `E`, `h_δ` and `ε_H` are computed on the gold sibling's 0.01 grid,
    restricted to `t ≤ 10`. Base-grid (0.08) values are reported beside them.
  - **Agreement check:** the census verifies gold-base agreement at shared
    times on every Stage-0 training and validation system before the panels
    are fixed.
  - **Flag:** every scored system carries a "base-grid samples per inner
    period" flag.
- **D-32: The panel rule, pinned** (it revises D-13 and D-14; 59-RESEARCH Q11 and C-10).
  - **`N_in`:** from the alias-safe unwrap of the inner separation angle on
    the gold grid.
  - **Percentiles:** `np.percentile(..., q)`, linear; distance `|N_in − q|`;
    ties go to the lowest ID.
  - **Single systems:** chosen only among systems with at least 3 base-grid
    samples per inner period, so the representation test is not confounded
    with aliased training data.
  - **The 16-system family:** sort by `(N_in, id)` and split with
    `np.array_split` into 16 bins (4 of 114, 12 of 113). From each bin take
    the system nearest `np.median` of the bin, excluding the three singles,
    with ties to the lowest ID. The family is otherwise unrestricted.
  - **The validation panel:** all 227.
- **D-33: Survey stage rules** (GAP-59-03 and GAP-59-04; they revise D-18).
  - **Precedence:** ascending, with Stage 6 the residual.
  - **Stage 3:** its percentile population is the training-split standard
    base records. Stage 3 is reported empty, with its measured Q range.
  - **`τ_L` settings:** the spec's defaults (resampled `dt = 0.01`, `d = 5`,
    delay 10, Theiler window 100), fitted over the "half-pairs" range, with
    sensitivity windows of 1, 2 and 3 time units.
  - **Implementation:** a vectorized numpy estimator, tested against a
    literal loop transcription. Degenerate cases return "not computable"
    with a reason.
  - **Labelling:** values are diagnostic.
- **D-34: The Gate G1 formula** (GAP-59-05; it extends D-24).
  - **Primary share:** `⟨P g_phys, P g_tot⟩ / ‖P g_tot‖²`, with
    `P = diag(1/(√v̂ + ε))` taken from the stored `exp_avg_sq`,
    bias-corrected by the stored step, and `g_tot` summed at the scheduled
    weights.
  - **Secondary share:** the same with `m̂`. Both are reported.
  - **Firing rule:** G1 fires if the primary share is at least `10⁻²` at
    checkpoint 900 or 951, on the frozen monitor batch.
  - **Registration:** the rule is written into the scorecard before `JX-1`
    runs.
- **D-35: Corpus access** (GAP-59-06; it revises D-12, D-16 and D-26).
  - **Data root:** `pinn.data.adapter.default_data_root()`, which from this
    worktree resolves to `<home>/Desktop/3_body_problem/simulation_data/Data`.
    Generation 7 read the same corpus; the research proved the monitor batch
    reproduces bitwise.
  - **The one choke point:** a single new module,
    `pinn/verification/split_allowlist.py`, is the only Phase-59 code that
    touches the corpus. It works per file (`parse_brutus_file`,
    `evaluate_admission`, `preprocess_trajectory`, `compute_invariants`,
    `build_raw_ic13`), behind an allowlist built from a hash-checked
    `splits.json`, refusing before any path is built.
  - **Never instantiated:** `AdmittedSetAdapter` and `_build_admitted_sources`,
    because they open every test file.
  - **The normalizer:** IC13 statistics are recovered from the retained
    checkpoint, with a residual assertion of at most 1e-6.
  - **The prohibitions test:** `tests/phase39/test_prohibitions.py`
    `ALLOWED_CORPUS_READERS` gains exactly this one module, with a comment.
    That follows the Plan 46-04 precedent.
- **D-36: Generation-7 code identity** (it refines D-23).
  - **The commit:** `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b`. HEAD's `pinn/`
    and `configs/` are byte-identical to it, so
    `git diff --quiet 629b1a6c HEAD -- pinn configs` exits 0.
  - **The driver:** the `DIAG-07` driver lives under
    `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/`, with
    a `--code-root` option inserted first on `sys.path`. It runs against a
    detached snapshot of that commit and asserts that `pinn.__file__` lies
    under it.
  - **The runtime:** primary is MPS float32, the run's own runtime; JX-1 and
    JX-10 are cross-checked on CPU float64, within tolerances declared
    before running.
- **D-37: Tests and environment** (it refines D-28).
  - **Framework:** tests are `unittest.TestCase` in `tests/phase59/`, run with
    `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest ...`.
  - **Long runs:** call `<home>/miniforge3/envs/pinn-train/bin/python`
    directly, so output streams.
  - **Imports:** `pinn-train` has no scipy, pandas, sklearn, psutil or pytest,
    so Phase-59 modules import only the stdlib, numpy, torch, yaml and
    `pinn.*`.
  - **`-I`:** not used for `pinn` modules, because isolated mode drops the
    repository from `sys.path`. The corpus is project-generated, not
    downloaded.
- **D-38: The formula on the probe systems.** The Stage-4b and Stage-6 pools
  are standard quasi-random only. The two-Kepler formula is therefore "not
  applicable: no hierarchical split" on both FEAS-09 systems, and the
  baselines evidence says so.
- **D-39: L-BFGS `max_iter = 50`** is frozen for the harness polish. It is
  inside the spec's 20–50; the production config's default is 20.
- **D-40: Which splits each piece reads** (from the plan checker's note I-8).
  - **The FEAS-02 census proper** (lap counts, difficulty measures, panel
    selection) uses training-split records only, as FEAS-02 says.
  - **Validation records** (the 227 Stage-0 validation systems) are read only
    for two purposes: the D-31 gold-base agreement check, and the validation
    panel that FEAS-02 itself names and FEAS-07 scores.
  - **The test split** is never read.
  - **Scope of this rule.** D-40 governs FEAS-02, FEAS-07 and FEAS-08 (the
    census, the baselines and the survey). DIAG-07 may also read
    validation-split records:
    - JX-3's validation group, which the ruling explicitly allows
      (`trainex-r4-ruling.md:124-137`);
    - the Stage-0 and Stage-1 validation records the generation-7
      controller's validation source needs at construction, built as in
      Phase 58.

    These reads are validation only, never test (SCOPE-40). The orchestrator
    clarified this on 2026-10-11, in answer to the planner's query.
- **D-41: DIAG-07 is not a SCOPE-44 run, but long steps run detached** (from
  the plan checker's note I-6).
  - **Why SCOPE-44 does not apply.** It governs training runs. DIAG-07
    performs read-only forward and backward passes on retained checkpoints,
    with no optimizer step.
  - **Detached launch.** Generation 6 was lost with its agent session. Any
    single DIAG-07 or survey step expected to exceed about 10 minutes (JX-2,
    JX-3, the survey's `τ_L` pass) is therefore launched detached
    (`nohup …`), with output to a log under `evidence/`.
  - **Memory preflight.** Before launch, available memory is checked with
    `vm_stat`, not the footprint reader (Pitfall 12). `ru_maxrss` is recorded
    as the high-water mark.
  - **Completion.** The step writes a completion marker, and its result is
    accepted only if that marker and the result hash are present.
- **Plan size (plan checker W-4).** Six plans exceed the estimator's
  smart-zone budget by 5–30%, at low confidence. This is accepted as
  advisory, with no re-slice: each plan is one coherent measurement, and
  splitting adds hand-offs without reducing risk.
- **Open, and not blocking this phase: GAP-59-08.** The validation gate and
  held-out evaluator compute `ε_H` from finite differences, which fail even
  the exact answer. This is owner-routed. Phase 59 reports it, and does not
  fix it.
- **Research preview, non-binding** (to be re-derived by committed code):
  - the two-Kepler formula is Tier 0 on 1,811 of 1,812 training systems and
    on all 227 validation systems (median `E` about 0.98);
  - the nearest-neighbour copy is Tier 0 on all 227 (median `E` 2.1);
  - median `N_in` is 18.6.

### 1. The scorecard (FEAS-01)

- **D-01: One consistent frame, with dimensionless scores.** Every position
  metric is a ratio, and `ε_H` is a relative error. The scorer states the
  frame it works in, and converts network outputs (`r′` as a function of
  `u = t/T`, with autograd `dr′/du`) to physical positions and velocities
  before computing the Hamiltonian. A test shows that the Brutus reference
  gives the same scores and the same `ε_H` whether it is passed in the raw
  frame or in the pipeline's scaled frame.
- **D-02: The position-error forms.**
  - `e_sys(t) = max_i |r̂_i(t) − r_i(t)| / R_sys`, where
    `R_sys = max over t and i of |r_i(t)|`, taken from the reference in its
    centre-of-mass frame.
  - `e_in(t) = |ŝ(t) − s(t)| / |s(t)|`, where `s = r_b − r_a` is the inner
    pair's separation vector.
  - The tier-defining error is `E = max_t max(e_sys(t), e_in(t))` over the
    reference's output times.
  - `h_δ` is the first output time at which `max(e_sys, e_in) > δ`, divided
    by `T`; it is 1 if that never happens.
  - **Why the larger of the two:** a good outer orbit must not hide a wrong
    inner binary (amendment, weakness 4).
- **D-03: Identifying the inner pair.** By construction it is bodies 1 and 2
  of the IC file (`sampling_method.md:23`, `:47-50`). The production
  preprocessing reorders bodies (`pinn/data/preprocessing.py:112-123`,
  `:191-194`, which returns `permutation`). The scorer therefore tracks the
  pair through that permutation. A test checks that on every Stage-0 panel
  system the tracked pair is also the closest pair at `t = 0`.
- **D-04: Tiers,** as in the proposal:

  | Tier | Condition |
  |---|---|
  | 3 | `E ≤ 0.01` and `ε_H ≤ 10⁻⁵` |
  | 2 | `E ≤ 0.01` and `ε_H ≤ 10⁻³` |
  | 1 | `E ≤ 0.10` |
  | 0 | otherwise |

  `ε_H` is the gate's own definition (`ctl_instruction.md:567`), computed on
  the predicted trajectory. Baselines use their own velocities: analytic for
  the formula, Brutus's for the copy.
- **D-05: The counting rule.** A system counts when it is at Tier ≥ 1 and its
  `E` is below the two-Kepler formula's `E` on that system (amendment,
  "Counting").
- **D-06: The budget rule.**
  - **Caps.** Each arm's step budget comes from a timing run of at least 50
    steps. The caps are about 3 hours for a single-system arm and about 8
    hours for Rung 3. The control keeps 1,000 steps.
  - **"Still improving."** The best `E` over the final 25% of the budget is
    at least 10% lower, relatively, than the best `E` at the 75% mark.
  - **Extension.** One extension doubles the budget. If the arm is still
    improving after it, it is reported as inconclusive, with its measured
    rate of improvement.
  - **Cadence.** Arms are scored at least every 5% of their budget.
- **D-07: The L-BFGS polish.**
  - **Optimizer:** full-batch L-BFGS with the spec's parameters: history 10,
    Wolfe line search, at most 50 iterations per call
    (`ctl_instruction.md:1897-1912`).
  - **Freeze:** arms with a physics term use the ratified freeze
    (`57-RULING.md:112-124`).
  - **Stop:** the polish ends at the first of two things: 5 consecutive outer
    calls without improving the training loss, or wall time equal to 25% of
    the arm's Adam wall time.
  - **Result:** the arm's result is its better scored state, by `E` and then
    `ε_H`. Both states are reported.
- **D-08: The G2 settings-sweep grid.**
  - **Default grid:** `first_omega_0 ∈ {60, 120, 240, 480}`, against the
    locked 30 (`pinn_architecture.md:181`). The reason: by estimate, Stage 0
    holds 10–80 inner laps per window. That is up to about `2π·80 ≈ 500`
    radians across the window, or about 250 per unit of the network's time
    input `τ = 2u − 1 ∈ [−1, 1]`. A higher first-layer frequency is the
    standard lever against spectral bias.
  - **Alternative grid:** the researcher may recommend a different set of four
    values, with evidence (for example, values derived from the census's
    inner-lap counts). The plan freezes the final grid in the scorecard.
  - **Where it runs:** first on the failing panel system with the fewest inner
    laps, then confirmed on the next failing system. The sweep is data-only.
- **D-09: The accuracy-reading cadence.** Every 100 optimizer steps, plus the
  initial and final states:
  - Rung 3: scored on its 16 systems and on the validation panel;
  - the control: scored on the validation panel.
- **D-10: Known-error tests** (FEAS-01 acceptance), in `tests/phase59/`:
  - the reference against itself;
  - a constant offset, and a time shift, each returning exactly the error
    imposed;
  - velocities scaled by a known factor, returning the analytic `ε_H`;
  - an inner-pair-only phase error, giving a small `e_sys` and a large
    `e_in`;
  - D-01's frame invariance;
  - D-03's pair tracking.
- **D-11: Freezing.**
  - **Form:** the scorecard is a committed plain-language document plus a
    machine-readable file that the scorer loads.
  - **Hash:** the machine-readable file's SHA-256 is recorded in the phase
    artifacts. Later phases' run records must carry it.
  - **Changes:** changing a threshold after any rung has run goes to the
    owner (SCOPE-42).

### 2. The census and panels (FEAS-02)

- **D-12: The population** is the 1,812 Stage-0 training systems exactly as
  generation 7 used them (`runs/stage0-v23g7-seed42/training_metadata.json`
  `n_train`, `splits.json`). The reference trajectories are read through the
  production data path, as the same admitted, preprocessed trajectories the
  trainer sees. This worktree's `simulation_data/Data/` does not hold the
  full corpus, so the researcher must establish the data root generation 7
  used (`config.yaml` `root: null`; compare `57-CONTEXT.md` D-19).
- **D-13: The difficulty measure.** The primary measure is the inner
  revolutions per window, `N_in`: the count of full turns of the inner pair's
  separation angle over `[0, T]`. Also recorded: outer revolutions, minimum
  and maximum pairwise separation, the acceleration range, and the
  phase-accuracy figure `δ / (2π N_in)` for `δ` = 0.01 and 0.10.
- **D-14: The panel rule**, declared in the plan before the census runs:
  - **Single systems:** the systems nearest the 10th, 50th and 90th
    percentiles of `N_in`; ties go to the lowest ID.
  - **The 16-system family:** sort by `N_in` and split into 16 equal-count
    bins. From each bin, take the system nearest the bin median, with the
    lowest ID on a tie, and exclude the three single systems.
  - **The validation panel:** all 227 Stage-0 validation systems, with no
    selection.

### 3. The comparison points (FEAS-07)

- **D-15: The two-Kepler formula.**
  - **Construction:** bodies 1 and 2 (tracked per D-03) form a Kepler orbit
    with mass `m₁ + m₂`, from their initial relative state. Body 3 follows a
    Kepler orbit about their centre of mass, with mass `m₁ + m₂ + m₃`.
  - **Solver and frame:** propagation is analytic, by a Kepler-equation
    solver, with velocities from the same solution. Positions are rebuilt in
    the centre-of-mass frame.
  - **When it does not apply:** if a two-body orbit is unbound, the formula is
    reported as not applicable for that system, never patched.
  - **Where it runs:** every panel system, and the FEAS-09 systems wherever a
    hierarchical split exists.
- **D-16: The nearest-neighbour copy.**
  - **Distance:** Euclidean, in the production-normalized IC13.
  - **Candidates:** the 1,812 Stage-0 training systems.
  - **Prediction:** the neighbour's Brutus positions and velocities.
  - **Where it is scored:** on all 227 validation systems.
- **D-17: Order.** Both baselines are scored and committed before any rung
  runs, because the counting rule depends on them.

### 4. The whole-dataset survey (FEAS-08)

- **D-18: Stage labels and their sources.** Every label records where it came
  from.
  - **The production code labels only Stages 0 and 1**
    (`pinn/data/stages.py:58`, `classify_stage_label`).
  - **The survey applies the spec's own criteria to the other stages**
    (`ctl_instruction.md:138-264`):
    - Stage 6 needs no `τ_L` (`s_min < 0.5` or `|E| < 0.01`);
    - Stage 2 follows its data-source rule;
    - Stages 3–5 need `τ_L`.
  - **`τ_L`** is computed by the spec's Rosenstein-style revisable-baseline
    estimator (`ctl_instruction.md:1294-1363`).
    - The legacy v1.3-era `pinn/data-handling/processing/rosenstein_lyapunov.py`
      is a cross-check only, never the source; the live-code policy makes
      v1.3-era code reference-only.
    - The values are labeled diagnostic: the final estimator is owner-pending
      (D-33-07). They are used only by this non-gating survey and by the probe
      selection.
  - **A criterion that cannot be computed** is reported, and that stage is
    left unlabelled with the reason. No criterion is invented.
- **D-19: Per-stage measures.**
  - system count;
  - `N_in` and outer revolutions, for hierarchical systems;
  - closest approach and acceleration range;
  - `τ_L` and the error growth `e^{T/τ_L}`;
  - the phase-accuracy figure;
  - the stages ranked by these measures, against the curriculum order.
- **D-20: The FEAS-09 picks.** Each is the training-split system at the median
  of its stage's primary measure, with the lowest ID on a tie:
  - Stage 4b, by `τ_L`;
  - Stage 6, by `s_min`.

  If either stage has no labeled training-split system, the plan records that
  and makes no substitute pick without owner sight.
- **D-21: The survey reports and never gates.**

### 5. The read-only checkpoint experiments (DIAG-07)

- **D-22: The stand-in for the ruling's checkpoint 900** is `step-000931.pt`.
  It is the nearest retained step after 900 and before the step-951 trip.
  - `stage-0-init.pt` serves the initialization comparisons.
  - `best.pt`, `latest.pt`, `step-000941.pt`, `step-000951.pt` and the
    failure checkpoint are recorded, not substituted.
  - All are in `runs/stage0-v23g7-seed42/checkpoints/`.
- **D-23: The code they run against.** The experiments run against the code
  revision that produced generation 7, in a temporary detached worktree at
  that commit, edited by nothing. The researcher establishes the commit from
  the run's provenance. If it cannot be established, that is a gap for the
  plan to record, never a guess.
- **D-24: Definitions.** `JX-1` (the executed half), `JX-2`, `JX-3`, `JX-4`,
  `JX-5` (the split) and `JX-10` are as pooled in
  `trainex-r4-resolution-doc.md` "JOIN-4-EXPERIMENTS" (`:628` onward) and
  ratified in `trainex-r4-ruling.md`. Each result records:
  - the command;
  - the checkpoint's SHA-256;
  - the reading it supports or falsifies.
- **D-25: Memory.** The monitor evaluation is chunked, per the
  generation-2 lesson: an unchunked 4096-row evaluation thrashed 24 GB.

### 6. Guardrails

- **D-26: Test-split refusal.** Every Phase-59 tool resolves files through an
  allowlist built from `splits.json`, holding training and validation records
  only. A test proves that a test-split ID is refused before any file is
  opened.
- **D-27: No training.** No Phase-59 tool constructs an optimizer step or
  writes a model checkpoint. A test or a static check asserts this.
- **D-28: Environment.** Tools run in the `pinn-train` environment
  (`57-CONTEXT.md` D-18), inline on this checkout, with the data root from
  D-12. Downloaded files are untrusted; Python reads them with `-I`.

### Claude's Discretion

- module names and layout under `pinn/verification/`, as long as the scorer
  and the baselines are importable by the Phase-60 harness;
- artifact formats (JSON or CSV beside a plain-language Markdown summary);
- how the work is split into plans and waves.

### Owner-Routed Decisions

None are open for Phase 59. The owner's choices on purpose, budget and the
pass bar are due at Phase 64 (FEAS-10). Any change to a frozen threshold
after a rung has run goes to the owner.
</decisions>

<canonical_refs>
## Canonical References

- `.planning/REQUIREMENTS.md`: FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07;
  SCOPE-39..44.
- `.planning/ROADMAP.md`: Phase 59 goal, Gate G1, success criteria 1–6.
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`:
  the decision rule, the counting rule, the baselines and the ladder.
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`:
  the scorecard draft.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r4/trainex-r4-ruling.md`,
  and `trainex-r4-resolution-doc.md` (JOIN-4, `JX-*`).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`:
  - `:138-264` the stages;
  - `:567` `ε_H`;
  - `:998` `T`;
  - `:1294-1363` `τ_L`;
  - `:1894-1912` L-BFGS.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`:
  - `:181` `first_omega_0`;
  - `:454` the `R_ref` invalidation;
  - `:1087` the held-out gate.
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md:23-63`:
  the hierarchical construction and the inner pair.
- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md:112-124`:
  the L-BFGS freeze.
- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-CONTEXT.md`:
  D-17..D-19, the environment and the data root.
- `runs/stage0-v23g7-seed42/` (gitignored): `splits.json`,
  `training_metadata.json`, `validation.jsonl`, `checkpoints/`.
</canonical_refs>

<code_context>
## Existing Code Insights (the researcher extends this)

- `pinn/data/preprocessing.py`: the canonical body ordering and its
  `permutation`.
- `pinn/data/stages.py`: Stage-0/1 classification only.
- `pinn/data/splits.py`, `pinn/data/adapter.py`: splits, stage labels and
  record access.
- `pinn/verification/overfit_probe.py`: the Phase-38 probe, which Phase 60
  extends.
- `pinn/verification/`: the INST-04 probe and GATE-04 tooling, as patterns
  for the committed verification tools.
- `pinn/data-handling/processing/rosenstein_lyapunov.py`: legacy, a
  cross-check only.
</code_context>

<specifics>
## Specific Ideas

- The owner is not a specialist. Every result artifact opens with a
  plain-language summary.
- The phase report should say directly whether the formula already reaches
  Tier 1 on Stage 0, because that changes how hard GO is to earn.
</specifics>

<deferred>
## Deferred Ideas

The rungs (Phase 60), conformance (Phase 61), Rung 3 and the gates
(Phase 62), the control (Phase 63), and the verdict and charter (Phase 64).
</deferred>
