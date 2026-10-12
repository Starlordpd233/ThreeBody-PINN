# Phase 59: Read-Only Baseline & Scorecard - Research

**Researched:** 2026-10-11
**Domain:** Pre-registered physical-unit scoring, read-only baselines and read-only checkpoint measurements on a PINN training stack for the three-body problem (Python 3.11, PyTorch 2.12.1 with MPS, NumPy 2.4.6, macOS arm64, 24 GB)
**Confidence:** HIGH for data, split, frame, environment and pitfall findings (each was measured this session on the real corpus and the retained checkpoints, train and validation files only). MEDIUM for the stage-survey and `τ_L` design (the spec is ambiguous and the estimator is owner-pending). MEDIUM for the DIAG-07 execution design (no model forward pass was allowed during research).

**Research-side compliance:** every corpus file opened this session went through an allowlist built from `runs/stage0-v23g7-seed42/splits.json` (train plus validation); no test-split ID was requested, and the guard refuses before a path is built. No optimizer, no training step and no model forward pass ran. `torch.load` was used on CPU for checkpoint keys and metadata only. No `gsd-tools` state verb was run. Nothing was committed. Scratch scripts live in the session scratchpad, not in the repository; every number below that came from them must be re-derived by committed code (marked `[VERIFIED: scratch measurement]`).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

(Copied verbatim from `59-CONTEXT.md` `## Implementation Decisions`, plus its in-scope and out-of-scope boundary.)

**Phase boundary.** In scope: FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07 (`.planning/REQUIREMENTS.md`).

Out of scope:
- any optimizer step on any network;
- any rung;
- any graded run or held-out evaluation;
- opening any test-split file;
- any framework-spec edit (SPEC-07..10 belong to Phase 61);
- recipe changes.

The DIAG-07 experiments compute forward and backward passes on retained checkpoints. The ruling authorizes that, and no optimizer step is taken.

**Gate G1** (it gates Phase 61, not Phase 60): `JX-1` shows a physics share of `10⁻²` or more of generation 7's Adam-preconditioned update → the conformance-first premise is re-examined before Phase 61 opens.

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

### Deferred Ideas (OUT OF SCOPE)

The rungs (Phase 60), conformance (Phase 61), Rung 3 and the gates
(Phase 62), the control (Phase 63), and the verdict and charter (Phase 64).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FEAS-01 | Pre-register the feasibility scorecard (metrics in physical units, tiers 0–3, budget rule, decision rule, counting rule, optimizer fairness, G2 grid, accuracy cadence) and a scorer under `pinn/verification/`, with known-error tests, committed before any rung runs | Q3 (frames, `ε_H`, autograd velocity API), Q11 (aliasing), Conflicts C-3/C-4, the closed-form fixtures in Validation Architecture, the strict-loader precedent (`r_ref_stage0.json`), Q7 (L-BFGS parameters) and the G2 grid evidence table |
| FEAS-02 | Stage-0 difficulty census (inner and outer revolutions, separations, accelerations, phase-accuracy figure) and the panels drawn from it, re-derivable, no test file opened | Q1/Q2 (data root, allowlist), Q4 (cadence), Q11 (alias-safe `N_in`, measured distributions, preview panel IDs), Q12 (runtime) |
| FEAS-07 | Two-Kepler formula on every panel system and nearest-neighbour copy on the validation panel, scored by FEAS-01's scorer, committed before any rung | Q5 (IC13 normalizer recovered from the retained checkpoints), Q10 (validated propagator and pitfalls), baseline previews (formula Tier 0 on 1,811 of 1,812; copy Tier 0 on 227 of 227) |
| FEAS-08 | Read-only whole-dataset survey and predictability envelope over training-split data for every stage, plus the FEAS-09 pick rule | Q6 (stage criteria, what is empty or degenerate, `τ_L` estimator hazards, cost), invariant and `τ_L` measurements, Conflict C-5 |
| DIAG-07 | The ruling's read-only experiments (`JX-1` executed half, `JX-2`, `JX-3`, `JX-4`, `JX-5` split, `JX-10`) on retained generation-7 checkpoints, against the generation-7 code, with Gate G1 recorded | Q7 (code revision and checkpoint inventory), Q8 (definitions, inputs, outputs, existing tooling), Conflict C-1 (`best.pt` is step 900), C-2 (adapter reads test files), C-11 (G1 definition), Q12 (cost) |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

Extracted from `./CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.claude-max/CLAUDE.md` and `.claude/rules/*.md`. They have the authority of locked decisions.

- **Tooling.** The project file says to use the Sequentialthinking MCP server for any task of more than one step. It was not available as a tool in this research session. The planner and executor should use it if they have it.
- **Gaps (v2.4 delegation, ROADMAP "Delegation and gaps").** A source-silent semantic decision is recorded in the phase-local `59-GAPS.md` and the milestone index `.planning/milestones/v2.4-GAPS.md` (created on the first gap) with every STOP-protocol field. It may be resolved `RESOLVED-WITH-INSTRUCTION` under the owner's delegation (2026-10-07, re-confirmed 2026-10-09), except where it would move a locked value, spend the evaluation, or pre-empt the verdict. Section "Open Questions" lists candidate gap entries.
- **Git.** Run `git status --short --branch` at session start and before committing. Commit only with `scripts/agent-commit` with both `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set; stage explicit paths; no `--no-verify`; message `<type>(<scope>): <lowercase imperative subject>` (types include `feat`, `test`, `evidence`, `verify`, `plan`, `docs`; scopes `59` or `59-NN`); body required for multi-file or `.planning/` commits; an `Agent-Assisted-By` trailer; no push from `milestone/*`. Do not use `scripts/agent-commit -F` (it scans argv for a trailer and appends its own `-m`; pass several `-m` paragraphs with the trailer last).
- **STATE.md is maintained by hand.** Never run `gsd-tools` state verbs (planned-phase, record-session, add-decision, complete-phase, update-progress): they regress counters.
- **Corpus is read-only.** `simulation_data/` is strictly read-only; evidence never lands under it (existing guards: `_reject_dataset_evidence_root` in `pinn/verification/overfit_probe.py:79`, `_REPOSITORY_CORPUS_ROOT` in `pinn/data/splits.py:733-734`).
- **Live-code policy.** `pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py` and `pinn/data-handling/**` (including `rosenstein_lyapunov.py`) are v1.3-era, reference-only. The rest of `pinn/` is the v2.0 production system (STATE.md: "`pinn/` ban lifted for v2.0").
- **Frozen or read-only specs.** `sampling_method.md` is frozen; `data_quality_assessment.md`, `review-of-framework.md` and `stage-strat-revision.md` are read-only. No framework-spec edit in Phase 59 (SPEC-07..10 are Phase 61).
- **Docs.** Files under `docs/work/` need the frontmatter block and a date-prefixed name, in `docs/work/{plans,reviews,designs}/milestone_v2.4/<phase>/`; read `docs/README.md` in full before creating, moving or deleting any file in `docs/`; no legacy paths; no `review1.md`-style names.
- **Environment.** The `pinn-train` conda env is locked (`environment.yml`, `requirements-lock.txt`) and its fingerprint is pinned by the duration gate: install nothing into it, pytest included (`57-CONTEXT.md` D-18).
- **Owner is not a specialist.** Every result artifact opens with a plain-language summary (CONTEXT "Specifics").
- **No emojis** in any written output.

## Summary

Phase 59 can be built almost entirely from production functions that already exist. The corpus is at `<home>/Desktop/3_body_problem/simulation_data/Data` (the default data root resolved from a linked worktree); the 1,812 Stage-0 training systems, the 227 validation systems and every other train or validation record are readable one file at a time through `parse_brutus_file`, `evaluate_admission`, `preprocess_trajectory`, `compute_invariants` and `build_raw_ic13`. That per-file path reproduced the retained generation-7 monitor batch bitwise (400 sampled rows, 210 records, 0 mismatches), so it is "the same admitted, preprocessed trajectories the trainer sees". The whole census, both baselines and the whole-dataset invariants take seconds to a few minutes on this Mac. Generation 7's code is commit `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b`, and `pinn/` and `configs/` at HEAD are byte-identical to it.

Seven findings change how the plan must be written (full list under "Conflicts with CONTEXT.md"). (1) The production `AdmittedSetAdapter` parses every file in all four corpus folders, test-split files included, so it cannot be used under D-26; the plan must build an allowlist-bound reader from the per-file functions, and must recover the production IC13 normalization statistics from a retained checkpoint because the adapter computes them over the whole corpus and never persists them (the recovery reproduces 256 records by 13 slots to 5.5e-8). (2) The production gate's `ε_H` differentiates predicted positions by finite differences; on Brutus's own reference at the dataset cadence that gives 3.5e-2 to 3.8e-1, against 5e-15 to 3e-14 with the file's velocities, so Tier 2 and Tier 3 are unreachable unless the scorer uses autograd velocities as FEAS-01 says. (3) `best.pt` is the step-900 checkpoint (global step 900, Adam step 900, written in the same second as the step-900 validation sidecar), so D-22's step-931 stand-in is unnecessary. (4) The hierarchical output cadence (0.08) is aliased for the fastest inner binaries (1.5% of systems have an inner period under two samples; naive angle unwrapping returns negative lap counts above about 60 laps), so `N_in` must come from an alias-safe method. (5) Stage 3's virial window cannot be met by any standard quasi-random record (Q at most 0.12), Stage 6's clause holds for every record, and the spec's `τ_L` snippet is degenerate and needs `scipy`, which the training environment lacks. (6) The environment has no `scipy`, `pytest`, `pandas`, `sklearn` or `psutil`, and `resolve_runtime` refuses float32 on CPU. (7) An existing test (`tests/phase39/test_prohibitions.py`) fails any new `pinn/` module that names a corpus folder, so the one new corpus-touching module must be added to its allowlist or avoid the tokens.

Preview results (research scratch, to be re-derived by committed code): the two-Kepler formula is Tier 0 on 1,811 of 1,812 Stage-0 training systems and 227 of 227 validation systems (median `E` about 0.98); the nearest-neighbour copy is Tier 0 on all 227 validation systems (median `E` 2.1). So the owner's "does the formula already reach Tier 1" question has the answer no, and the counting rule's second clause will almost never bind on Stage 0.

**Primary recommendation:** build one choke-point module (`pinn/verification/split_allowlist.py`) that is the only new code allowed to touch the corpus (manifest-hash-checked allowlist, refusal before any path is built, a `sys.addaudithook` attestation); put the scorer, Kepler formula, nearest-neighbour copy, census and survey on top of its `ReferenceTrajectory` objects using numpy and the existing `gate_metrics` and `componentwise_du` functions; recover the IC13 normalizer from the retained checkpoint; run DIAG-07 through a duck-typed allowlisted source and a refusing checkpoint store, against the proven-identical generation-7 tree, on the run's own MPS float32 runtime with a float64 CPU cross-check; and record every source-silent choice (stage precedence, `τ_L` window, `G1` share formula, scoring grid) in `59-GAPS.md` before running.

## Conflicts with CONTEXT.md

Each item is a place where the code or data contradicts, or makes ambiguous, a locked decision. None is silently worked around; each needs an explicit plan decision. Items C-1, C-2 and C-3 contradict the text of a decision. C-4 to C-12 are hazards or under-specifications.

| # | Decision | What the evidence shows | Recommended handling |
|---|----------|------------------------|----------------------|
| C-1 | D-22 (step 931 is the stand-in for 900) and DIAG-07's "retained set is ... best and latest" | `best.pt` carries `counters.global_step: 900`, `curriculum.step: 900`, Adam `step: 900` in every optimizer-state entry, and was written at `Oct 3 02:42:01`, the same second as `validation_gate/step-00000900.json`. The committed Phase-58 verdict packet already lists "gen 7, step 900 (`best.pt`)" and its replay script uses `best.pt` for step 900. So the ruling's checkpoint 900 exists and needs no stand-in. [VERIFIED: torch.load metadata of `best.pt`; `ls -l` timestamps; `v2.3-closure-evidence-bundle.md:209,384`] | Use `best.pt` for checkpoint 900, assert `global_step == 900` in code, keep step 931/941 as supplementary readings. Record as a factual correction in `59-GAPS.md` (not a value change). |
| C-2 | D-12 ("read through the production data path") together with D-26 (allowlist, no test file opened) | `AdmittedSetAdapter._scan_and_admit` loops over all four `BRUTUS_FOLDER_TABLE` folders, `sorted(folder_dir.glob("*.txt"))`, and calls `parse_brutus_file` on every file (`pinn/data/adapter.py:814-820`). The splits are applied afterwards, in memory (`StageIndex.from_split`, `splits.py:170-186`). The stock replay path (`pinn.train._build_admitted_sources`, `train.py:498-533`) and `RunController.__init__` (it builds a monitor from a train source, `controllers.py:819-820`) therefore parse test-split files. The Phase-46 probe and the Phase-58 replay script both used it. [VERIFIED: Read of the cited lines] | Do not instantiate `AdmittedSetAdapter`, `_build_admitted_sources`, or any reader that globs the corpus folders. Use the adapter's public per-file functions behind the allowlist. The production IC13 statistics are computed over the whole corpus (`adapter.py:938-942`) and never persisted: recover them from the retained checkpoint (Q5). |
| C-3 | D-04 and D-01 ("`ε_H` is the gate's own definition" and "autograd `dr′/du`") | The production gate computes velocity by finite differences of predicted positions over the snapshot times (`pinn/verification/gate_metrics.py:84-122`, used by `compute_trajectory_gate_metrics` at `:211-222` and by `compute_validation_gate`, `validation_gate.py:257-259`). On 25 sampled Stage-0 training references at dt_out 0.08 the finite-difference `ε_H` of the Brutus reference itself is 3.5e-2 to 3.8e-1; with the file's own velocities it is 5e-15 to 3.4e-14. So Tier 2 (1e-3) and Tier 3 (1e-5) are unreachable by any arm if "the gate's own definition" is implemented by calling the production gate function. Generation 7's logged gate values (10 to 50 on validation) are finite-difference values. [VERIFIED: scratch measurement; Read of `gate_metrics.py`] | Define `ε_H` in the scorecard as the formula (`ctl_instruction.md:567`) evaluated with autograd velocities (networks), analytic velocities (formula) and Brutus velocities (copy), using `matched_plummer_hamiltonian_series` and `trajectory_eps_h` (`gate_metrics.py:130-200`) and never `compute_trajectory_gate_metrics`. Report the finite-difference value as a separate, labelled context column for continuity with generation 7. Record in `59-GAPS.md`. |
| C-4 | D-02 ("over the reference's output times") | The hierarchical base grid is 0.08 (126 snapshots, all 2,039 Stage-0 train and validation files). Estimated inner periods reach 0.099, so 28 of 1,812 training systems (1.5%) have fewer than two samples per period, 7.8% fewer than three, and 29.7% fewer than five. An aliased orbit cannot be detected on that grid. The gold sibling (dt 0.01) agrees with the base trajectory at the shared times to 5.7e-9 at worst (300 systems), so it is a legitimate dense view of the same reference. [VERIFIED: scratch measurement] | Keep D-02's grid as the frozen primary. Add to the scorecard a per-system "samples per inner period" flag, and a second, pre-registered column `E_dense` scored on the gold sibling's grid (restricted to `t ≤ 10`). Decide in the plan whether `E_dense` is reported or gating; recommended: reported, with the single-system picks required to have at least 3 samples per inner period. |
| C-5 | D-18 ("applies the spec's own criteria"; "a criterion that cannot be computed is reported") | (a) Stage 3 requires `0.9 ≤ Q ≤ 1.1`; the 2,199 training-split standard base records have `Q` from 0.001 to 0.119, so Stage 3 is empty (0 of 2,199). (b) Stage 6's `s_min < 0.5` holds for all 6,085 training-split base records (standard `s_min` 0.147 to 0.44, hierarchical 0.014 to 0.084), so it needs a precedence rule. (c) The `τ_L` snippet (`ctl_instruction.md:1369-1435`) imports `scipy`, which is absent from `pinn-train`, and its `max_iter = M − max(nn)` collapses to 1 point on 4 of 6 sampled records, where `np.polyfit` raises `LinAlgError`. (d) `τ_L` class fractions depend strongly on the fit window (standard base: 5% to 32% in (2, 5] for windows of 1 to 3 time units). (e) Production labels every gold record `UNASSIGNED` (`stages.py` docstring), so Stage 2 and Stage 5 have no production label. [VERIFIED: scratch measurement; Read of the spec and `stages.py`] | Record the survey's rules as gap entries before the survey runs: precedence = ascending stage number with Stage 6 as the residual ("All remaining data", `ctl_instruction.md:252-253`); Stage-3 percentile population = training-split standard base records; `τ_L` parameters and fit-window rule pre-declared, with sensitivity columns. Report Stage 3 as empty with its reason (Q at most 0.119). |
| C-6 | D-07 ("at most 50 iterations per call") | The spec says "max iterations: 20-50" (`ctl_instruction.md:1909-1910`); the resolved generation-7 config has `opt.lbfgs_max_iter: 20`, `lbfgs_history_size: 10`, `lbfgs_line_search: strong_wolfe`, `lbfgs_chunk_size: 1024`. | 50 is inside the spec range; freeze 50 as the harness polish parameter and note that the production default is 20. No owner decision needed. |
| C-7 | D-23 (temporary detached worktree) | `git diff --quiet 629b1a6c HEAD -- pinn configs` exits 0 and `git status --short pinn configs` is empty, so the current tree's `pinn/` and `configs/` are byte-identical to generation 7's. Phase-59 code added under `pinn/verification/` would not exist in a detached snapshot, so a driver inside `pinn/` cannot be imported from it. | Keep D-23 (snapshot by `git worktree add --detach` or `git archive 629b1a6c pinn configs`), put the DIAG-07 driver under `.planning/phases/59-.../evidence/diag07/` with a `--code-root` option that is inserted first on `sys.path` before any `pinn` import, assert `pinn.__file__` is under it, and record the identity proof beside the result. |
| C-8 | D-28 ("Tools run in the `pinn-train` environment ... Python reads [downloaded files] with `-I`") | `pinn-train` has torch 2.12.1, numpy 2.4.6, PyYAML 6.0.3, h5py, sympy, tensorboard and no `scipy`, `pytest`, `pandas`, `psutil`, `sklearn`. `python -I -m pinn...` cannot import `pinn` (isolated mode drops the cwd from `sys.path`). The corpus is project-generated, not a download. `conda run` buffers output until exit. | Tests are `unittest.TestCase` classes run with `python -m unittest` (they also run under `.venv/bin/python -m pytest`, which has pytest 9.1.1 and scipy 1.17.1, as a convenience only). Use `-I` only for scripts that read untrusted downloads (none are needed). Use the env interpreter path directly for long runs so output streams. |
| C-9 | (Not a decision; a standing test) | `tests/phase39/test_prohibitions.py:199-205` scans every `pinn/**/*.py` and fails any module with a corpus token (`brutus_hierarchical`, `brutus_standard`, `ic_hierarchical`, `ic_standard`) or a `glob/rglob(... .txt` in executable source unless it is in `ALLOWED_CORPUS_READERS` (`:46-50`: `adapter.py`, `fixture_loader.py`, `target_frame_probe.py`). Plan 46-04 added `target_frame_probe.py` to that set. | Add exactly one new module (`split_allowlist.py`) to `ALLOWED_CORPUS_READERS` with a comment, as Phase 46 did, and add a test that no other Phase-59 module contains a corpus token. |
| C-10 | D-14 and D-13 (rule details) | The rule does not fix the `N_in` estimator, the percentile method, the bin-size rule (1,812 / 16 = 113.25, so bin sizes cannot all be equal), the median of an even-sized bin, or what happens when a bin's nearest-to-median system is one of the three singles. | Pin them in the plan before the census runs (Q11 gives a concrete rule). |
| C-11 | Gate G1 and D-24 | The sources give the threshold (`10⁻²`) but not the share formula or the checkpoint set; the only wording is Claude's "the share of the Adam-preconditioned update (from the stored moments) along −g_phys". `stage-0-init.pt` has `optimizer: None`, so checkpoint 0 has no stored moments. | Pre-register the formula and the rule (G1 fires if the share is `≥ 10⁻²` at checkpoint 900 or 951, on the frozen monitor batch) before computing anything. Q8 gives candidate definitions. |
| C-12 | D-15 and D-20 | All 4,857 hierarchical groups are Stage 0 or Stage 1 (2,265 + 2,592); the Stage-4b and Stage-6 pools are standard quasi-random records only, which have no hierarchical split. | The two-Kepler formula is "not applicable: no hierarchical split" on both FEAS-09 systems. State this in the baselines evidence. |

## Architectural Responsibility Map

This project has no web tiers; the tiers are the repository's layers.

| Capability | Primary tier | Secondary tier | Rationale |
|------------|-------------|----------------|-----------|
| Corpus access, split enforcement, admission, preprocessing | Data layer (`pinn/data/*` functions, called through one new allowlist module) | Verification tooling | `adapter.py` is the sole corpus reader; the allowlist module is the only new code allowed to name corpus paths (C-9). |
| IC13 normalization (production statistics) | Data layer (`normalize_ic13`) | Verification tooling (statistics recovered from a retained checkpoint) | The adapter computes the statistics privately over the whole corpus (`adapter.py:938-942`). |
| Scorecard definition and freeze | Verification tooling (`pinn/verification/artifacts/*.json` plus a strict loader) | Docs (`docs/work/designs/milestone_v2.4/...`) | Mirrors the governed `r_ref_stage0.json` artifact. |
| Scoring (`E`, `h_δ`, `ε_H`, tier, counting rule) | Verification tooling | Model layer (autograd velocity through `componentwise_du`) | Must be importable by the Phase-60 harness and independent of training code. |
| Baselines (two-Kepler, nearest-neighbour copy) | Verification tooling (numpy only) | Data layer | Analytic or table lookup; no model. |
| Census, panels, survey, `τ_L` | Offline batch analysis (CLI modules under `pinn/verification/`) | Evidence layer | Read-only, deterministic, seconds to minutes. |
| Checkpoint experiments (DIAG-07) | Evidence-layer driver run against the generation-7 trainer code | Model and trainer layer (`RunController` methods) | D-23: the code that produced the run. |
| Guardrails (no test file, no training) | Verification tooling (allowlist, audit hook, AST checks) | Test layer (`tests/phase59`) | D-26, D-27. |
| Provenance and hashes | Planning evidence (`.planning/phases/59-.../evidence/`) | — | Committed state, not `/tmp`. |

## Standard Stack

### Core

| Library | Version | Purpose | Why standard |
|---------|---------|---------|--------------|
| Python (`pinn-train`) | 3.11.15 | Runtime | The locked training env (`environment.yml`: `python=3.11.*`). [VERIFIED: `sys.version`] |
| PyTorch | 2.12.1 (MPS available in this shell) | Model, `componentwise_du`/`jacrev`, `torch.load` | `requirements-lock.txt` pins `torch==2.12.1`. [VERIFIED: `pip list`, `torch.backends.mps.is_available()` is True] |
| NumPy | 2.4.6 | All array work: scorer, Kepler, census, survey, `τ_L` | Lock pins `numpy==2.4.6`. [VERIFIED] |
| PyYAML | 6.0.3 | Config loading (`load_config`) | Lock pins it. [VERIFIED] |
| stdlib `unittest`, `hashlib`, `json`, `csv`, `argparse`, `sys.addaudithook`, `resource`, `subprocess` | — | Tests, hashes, evidence, attestation, git identity checks | `pinn-train` has no pytest; Phase 57 used stdlib unittest only. |

### Supporting

| Library | Version | Purpose | When to use |
|---------|---------|---------|-------------|
| sympy | 1.14.0 | Present in the env | Not needed; closed-form fixtures are plain numpy. |
| h5py, tensorboard | 3.16.0, 2.21.0 | Present | Not needed. |
| `.venv` (pytest 9.1.1, scipy 1.17.1, torch 2.12.0, Python 3.12.13) | — | Convenience test runner only | Never for evidence, never for tools; `h5py` is absent there. |

### Alternatives considered

| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| numpy Newton Kepler solver | `scipy.optimize` / astropy / poliastro | Not installed in `pinn-train`; installing would perturb the pinned env fingerprint (D-18). The solver is about 25 lines and was validated. |
| numpy `τ_L` | The spec snippet with `scipy.spatial.distance` | Needs scipy and is degenerate (C-5). |
| stdlib `csv` | pandas | Not installed. |

**Installation:** none. Do not install anything into `pinn-train`.

**Version verification:** `pip list` in `<home>/miniforge3/envs/pinn-train` showed torch 2.12.1, numpy 2.4.6, PyYAML 6.0.3, h5py 3.16.0, sympy 1.14.0, tensorboard 2.21.0, packaging 26.2. These match `requirements-lock.txt`. `requirements-lock.txt` and `environment.yml` are unchanged by this phase.

## Package Legitimacy Audit

No external package is installed or recommended by this phase, so the legitimacy gate (`gsd_run query package-legitimacy check`) does not apply and was not run. Every import is from the locked `pinn-train` environment or the standard library. If a later plan wants scipy, pytest or pandas, that is a change to the pinned environment and goes to the owner, not a Phase-59 task.

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
 runs/stage0-v23g7-seed42/splits.json ──sha256 vs generation-7-retention.json──> SplitManifest.from_dict
          │ (7,606 groups; group["split"] in {train, validation, test})
          v
   SplitAllowlist(train ∪ validation)  ── withheld = test physical keys (counts only in evidence)
          │
          │  require(key) raises TestSplitRefused BEFORE any path is built
          v
 data root: explicit > GSD_DATA_ROOT > default_data_root()  (= <git common dir parent>/simulation_data/Data)
          │
          v
 AllowlistedCorpusReader.read(key)  [+ sys.addaudithook attestation: every "open" under the root is logged,
          │                           a withheld filename raises before the OS open]
          │   parse_brutus_file(path, root=root)           (adapter.py:386)
          │   evaluate_admission(...)  -> must be "admit"   (admission.py:128)
          │   preprocess_trajectory(...) -> permutation, r_gauge/v_gauge (scaled, gauged), masses_ordered
          │   compute_invariants(...) -> E, Q, s_min, l_ratio ; build_raw_ic13(...)
          v
 ReferenceTrajectory  (float64; pipeline frame r', u = t/T; inner/outer slots via permutation)
     │                         │                              │                        │
     │ gold sibling (dt 0.01)  │ raw IC13 + recovered         │                        │
     v                         v production normalizer        v                        v
 stage0_census         nn_copy (train pool ->          two_kepler (Kepler f,g       dataset_survey
 (alias-safe N_in)      227 validation systems)        propagation, COM frame)      (stages 0-6, tau_L, FEAS-09 picks)
     │                         │                              │                        │
     v                         └───────────┬──────────────────┘                        v
 panels.json (rule + census hash)          v                                     survey.json (non-gating)
                              feasibility_scorer.score(): e_sys, e_in, E, h_δ,
                              ε_H (matched_plummer_hamiltonian_series with analytic /
                              Brutus / autograd velocity), tier, counting rule
                                           │
                                           v
                   feasibility_scorecard_v1.json (strict loader, SHA-256 recorded)

 gen-7 checkpoints (sha256 vs generation-7-retention.json; torch.load(weights_only=True))
          │  RunController (duck-typed allowlisted source, refusing checkpoint store, MPS float32 + CPU float64 check)
          v
 DIAG-07 driver: JX-1 (per-term grads, cosines, Adam-preconditioned shares), JX-2, JX-3, JX-4, JX-5, JX-10
          v
 jx*.json + G1 record  -> evidence/manifest.json (sha256 of every artifact) -> verify_phase59_evidence.py
```

### Recommended Project Structure

```
pinn/verification/
├── split_allowlist.py          # NEW, the only new corpus-touching module (add to ALLOWED_CORPUS_READERS)
├── production_reference.py     # ReferenceTrajectory loader, IC13 normalizer recovery (imports split_allowlist)
├── feasibility_scorecard.py    # strict loader, SHA-256, tier/counting/decision/budget rule functions
├── feasibility_scorer.py       # position errors, h_δ, ε_H, tier, network -> (r', dr'/du)
├── two_kepler.py               # Kepler f,g propagator + two-orbit formula + NotApplicable
├── nn_copy.py                  # nearest-neighbour copy in production-normalized IC13
├── stage0_census.py            # N_in/N_out estimators, census CSV, panel rule, --check
├── dataset_survey.py           # stage predicates, tau_L estimator, ranking, FEAS-09 picks, --check
└── artifacts/feasibility_scorecard_v1.json     # the frozen machine-readable scorecard
tests/phase59/
├── __init__.py  _fixtures.py
├── test_split_allowlist.py  test_static_guards.py
├── test_scorecard.py  test_scorer_known_errors.py
├── test_two_kepler.py  test_nn_copy.py
├── test_census.py  test_survey.py  test_diag07.py
.planning/phases/59-read-only-baseline-scorecard/evidence/
├── manifest.json               # sha256 + size of every artifact
├── verify_phase59_evidence.py  # subcommands: scorecard-frozen, census, baselines, survey, diag07, guardrails, final
├── census/  baselines/  survey/  diag07/  audit/
docs/work/designs/milestone_v2.4/59-read-only-baseline-scorecard/<date>-feasibility-scorecard.md   # plain-language scorecard (frontmatter required)
```

### Pattern 1: One choke point for corpus access (D-26)

**What:** a manifest-hash-checked allowlist plus a reader. Refusal happens before a path is built; an audit hook is a second, independent line that also records what was opened.
**When to use:** every Phase-59 tool, with no exceptions.
**Why two lines:** CPython raises the `open` audit event from `_io.FileIO.__init__` and from `_Py_open_impl` before the OS call, and a hook that raises aborts the open before any handle exists; the docs also say audit hooks are not a sandbox (an accident guard, which is the threat here). [CITED: github.com/python/cpython Modules/_io/fileio.c and Python/fileutils.c via Context7 `/python/cpython/v3.11.14`; empirically verified: `Path.read_text` and `numpy.loadtxt` both raise it in `pinn-train`]
**Example:**
```python
# Source: derived from pinn/data/splits.py:390-395 (SplitManifest.physical_keys) and adapter.py:81-86
class TestSplitRefused(PermissionError): ...
class SplitAllowlist:
    @classmethod
    def from_manifest(cls, path, *, expected_sha256):
        raw = Path(path).read_bytes()                          # an artifact, not a trajectory file
        if hashlib.sha256(raw).hexdigest() != expected_sha256: raise ValueError("splits.json hash mismatch")
        m = SplitManifest.from_dict(json.loads(raw), path=path)  # validates schema and Hamilton counts
        return cls(allowed=m.physical_keys("train") | m.physical_keys("validation"),
                   withheld=m.physical_keys("test"))
    def require(self, key):                                    # called BEFORE a path exists
        pk = key.physical_key
        if pk in self.withheld or pk not in self.allowed:
            raise TestSplitRefused(f"{pk.variant}:{pk.id} is not in the train/validation allowlist")
        return pk
# folder for (variant, fidelity): invert BRUTUS_FOLDER_TABLE; filename: f"brutus_{variant}_{id:04d}.txt"
```
The expected hash of `splits.json` is committed already: `generation-7-retention.json` records `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` (4,159,982 bytes) for both the seed-42 and the smoke run (byte-identical).

### Pattern 2: The scorer, in the pipeline frame, with explicit velocity provenance (D-01, D-02, D-04)

**What:** inputs are positions `(Nt, 3, 3)`, velocities, masses and the reference in one declared frame (`"r_prime_u"` for the pipeline's `(r′, u)`, or `"raw_t"`); outputs `E`, `e_sys` and `e_in` series, `h_0.01`, `h_0.10`, `ε_H`, tier, and a `velocity_source` label.
**Why the pipeline frame is the default:** the network predicts there; `R_sys` and `e_in` are scale- and rotation-invariant ratios, and `ε_H` is invariant because `H′ = D·H` (`ctl_instruction.md:575-578`) and `D³ = T²` with `G = 1`.
**Example:**
```python
# Sources: gate_metrics.py:130-200 (H and eps_H), controllers.py:1091-1095 and :1160-1163 (autograd velocity)
def position_errors(pred_r, ref_r, inner):                      # both (Nt,3,3), COM-centred, same frame
    a, b = inner
    r_sys = np.linalg.norm(ref_r, axis=2).max()                  # max over t and bodies
    e_sys = np.linalg.norm(pred_r - ref_r, axis=2).max(axis=1) / r_sys
    s_ref, s_hat = ref_r[:, b] - ref_r[:, a], pred_r[:, b] - pred_r[:, a]
    e_in = np.linalg.norm(s_hat - s_ref, axis=1) / np.linalg.norm(s_ref, axis=1)
    return e_sys, e_in
def eps_h(pos, vel, masses):                                     # vel: autograd / analytic / Brutus, never finite-difference
    from pinn.verification.gate_metrics import matched_plummer_hamiltonian_series, trajectory_eps_h
    return trajectory_eps_h(matched_plummer_hamiltonian_series(pos, vel, masses))   # eps_inv = 1e-10
# network -> (r', dr'/du): mirror the trainer
def traj(u):                                                     # scalar u -> (3,3), COM-projected r'
    x = torch.cat([(2.0 * u - 1.0).reshape(1), ic13]).unsqueeze(0)
    return model(x, masses.unsqueeze(0)).reshape(3, 3)
first = torch.func.vmap(torch.func.jacrev(lambda u: traj(u).reshape(-1)))(u_leaf)   # (Nt, 9) = dr'/du
```
`componentwise_du(traj, u_leaf)` (`physics_residual.py:102-147`) returns the same first derivative plus an unused second one; use it only if "the trainer's own function" is wanted for a test, otherwise first-derivative `jacrev` halves the cost.

### Pattern 3: Pre-registered, strictly loaded scorecard (D-11)

**What:** `pinn/verification/artifacts/feasibility_scorecard_v1.json` with `schema_version`, tier thresholds, `δ` list, the frame declaration, the velocity-source rule, the budget rule (3 h, 8 h, 1,000 steps, 50-step timing run, 25% and 75% marks, 10% relative, one doubling, 5% cadence), the L-BFGS block (history 10, `strong_wolfe`, 50 iterations, stop rule, result rule), the G2 grid, the accuracy cadence (100), the counting rule and the decision rule (2 of 3, 12 of 16, branch (a)). A strict loader rejects unknown keys. The SHA-256 of the file's raw bytes goes in `evidence/manifest.json`, and `SCORECARD_SHA256` is exported for run records. Precedent: `load_frozen_r_ref_artifact` and `r_ref_stage0.json` (`schema_version "phase56-r-ref-stage0/v1"`).
**Freeze ordering check:** `verify_phase59_evidence.py scorecard-frozen` confirms the scorecard's commit is an ancestor of every census, baseline and survey evidence commit (SCOPE-42 is procedural, so test it procedurally).

### Pattern 4: The Kepler f-g propagator for the two-orbit formula (D-15)

**What:** propagate each relative orbit with the difference-of-eccentric-anomaly form of the universal-variable solution. It needs no pericentre direction, so eccentricity near 0 and the 3D inclination are non-issues, and `F′(ΔE) = r/a > 0` so Newton from `ΔE = n·Δt` is monotone. Validated this session against RK4 (h = 1e-4) over T = 10 for eccentricities 0.02 to 0.52 (relative position error at most 3.8e-7, dominated by RK4); at e = 0.96 RK4 itself is the inaccurate side.
**Example:** [VERIFIED: scratch validation; CITED: orbital-mechanics.space universal variables, where `a = (2/r₀ − v₀²/μ)⁻¹` and, for an ellipse, `χ = √a (E − E₀)`]
```python
def propagate_bound(s0, v0, mu, dt):                 # dt: array of times since the initial state
    r0 = np.linalg.norm(s0); inv_a = 2 / r0 - v0 @ v0 / mu
    if inv_a <= 0: raise NotApplicable("unbound")    # never patched (D-15)
    a = 1 / inv_a; n = np.sqrt(mu / a**3); sig = (s0 @ v0) / np.sqrt(mu)
    k1, k2, M = 1 - r0 / a, sig / np.sqrt(a), n * dt
    dE = M.copy()
    for _ in range(60):
        step = (dE - k1*np.sin(dE) + k2*(1 - np.cos(dE)) - M) / (1 - k1*np.cos(dE) + k2*np.sin(dE))
        dE -= step
        if np.max(np.abs(step)) < 1e-14 * max(1.0, np.max(np.abs(dE))): break
    else: raise RuntimeError("Kepler Newton did not converge")
    c, s_ = np.cos(dE), np.sin(dE)
    r = a + (r0 - a)*c + sig*np.sqrt(a)*s_
    f, g = 1 - (a/r0)*(1 - c), dt - (dE - s_)/n
    fd, gd = -(np.sqrt(mu*a)/(r*r0))*s_, 1 - (a/r)*(1 - c)
    return f[:, None]*s0 + g[:, None]*v0, fd[:, None]*s0 + gd[:, None]*v0
```
The two-orbit assembly is: inner relative orbit with `μ = m_a + m_b`; outer relative orbit of body `c` about the inner COM with `μ = M`; then `R_ab = COM − (m_c/M)ρ`, `r_c = COM + ((m_a+m_b)/M)ρ`, `r_a = R_ab − (m_b/m_ab)s`, `r_b = R_ab + (m_a/m_ab)s`, and the same combinations for velocities. In the scaled frame `(r′, u)` the same code works unchanged with the same masses, because `μT²/D³ = μ` when `D³ = T²` and `G = 1`. [VERIFIED: constants.py:19-27; arithmetic]

### Pattern 5: Alias-safe revolution counting (D-13)

**What:** count `N_in` as the unwrapped accumulated signed angle of the inner separation vector about the initial orbit normal, divided by `2π`, evaluated on the gold sibling's grid (dt 0.01, at least 10 samples per period at the fastest observed `P_in`), clipped to `t ≤ 10`. Cross-check with a mean-motion-assisted unwrap on the base grid. Do not unwrap the base grid directly.
**Measured on 300 random Stage-0 training systems** [VERIFIED: scratch measurement, gold unwrap as reference]:

| Estimator | Median error | p95 error | Max error | Verdict |
|-----------|--------------|-----------|-----------|---------|
| Plain unwrap, base grid (0.08) | -0.09% | 22.5% | 161% (returns negative counts above about 60 laps) | Unsafe |
| Mean-motion integral, base grid | +0.48% | 2.0% | 9.4% | Acceptable cross-check |
| Mean-motion-assisted unwrap, base grid | 0.006% | 0.54% | 33% (99.3% within 2%; per-step residual reached 2.91 rad, close to the π safety bound) | Cross-check with a flag |
| Kepler period from the initial state | -0.8% | 3.6% | 320% | Do not use for ranking |
| Gold-grid unwrap (reference) | — | — | — | Primary |

```python
def unwrap_total(s, normal):                          # s: (Nt,3) separation vectors; valid if each step < pi
    d = np.arctan2(np.cross(s[:-1], s[1:]) @ normal, np.sum(s[:-1] * s[1:], axis=1))
    return d.sum() / (2 * np.pi)
# assisted (base grid): d_k += 2*pi*round((nbar_k*dt_k - d_k)/(2*pi)), nbar_k = sqrt(mu*(2/r - v^2/mu)^3)
```
The gold file for a Stage-0 base record exists for all 1,812 training systems (signature gold stage `UNASSIGNED`, not `MISSING_GOLD`) and agrees with the base file at the common times to at most 5.7e-9 relative to system size. Outer revolutions are fractional (14% of systems have `N_out < 1`); report the real-valued turn count, not a floor.

### Pattern 6: Recover the production IC13 normalizer (D-16, DIAG-07)

**What:** the production statistics are the mean and standard deviation of the first 12 raw IC13 slots and the energy scale `|median(E)| + 1e-8` over the entire admitted corpus (`preprocessing.py:327-339`, called at `adapter.py:938-942`). They are not persisted anywhere (grep of `pinn/`, `tests/`, `.planning/`, `runs/` finds no stored values). A retained checkpoint stores the already-normalized IC13 rows of its 256 training monitor identities (`front_monitor.batch.data.tau_ic13`, 8,192 rows). Compute the raw IC13 of those 256 records with the production per-file functions and solve, per slot, `atanh(z) = (raw − μ)/(σ + 1e-8)` by least squares.
**Result, measured:** the fit reproduces every stored row of all 256 records and 13 slots to a maximum absolute error of 5.5e-8 (float32 rounding). Recovered values: μ = [1.408782, 0.927368, 0.66385, 0.345032, 0.118058, 0.090548, 0.002431, -0.01502, -0.880282, -0.011614, 0.007261, 0.320012], σ = [0.368234, 0.171871, 0.291758, 0.138143, 0.125898, 0.118283, 0.221326, 2.978675, 3.294257, 0.207178, 1.704346, 1.921839], `e_scale` = 8.778435460009458. [VERIFIED: scratch measurement on `stage-0-init.pt`] The plan must recompute these in committed code, assert the residual bound, and commit the values with the checkpoint's SHA-256. The statistics are dominated by the standard variant (for example slot 5 has σ = 0.118 against a Stage-0 spread of 0.0026), which is exactly why recomputing them from train and validation records alone would not be the production normalizer.

### Pattern 7: DIAG-07 through the trainer's own methods, with a restricted source

**What:** `RunController` needs a train source and a validation source, and its constructor builds a monitor from the train source (`controllers.py:819-820`, `_build_front_monitor` at `:909-956`), then `load_state_dict` replaces it with the checkpoint's serialized monitor after verifying `batch_hash` and `monitor_hash` (`:958-1024`). `pinn/verification/phase57_production_conformance.py:212-324` already constructs a `RunController` on a duck-typed in-memory source (`_SyntheticStageQuery`) at float64 CPU; replace it with an allowlisted real-record source exposing the same accessor set (`blacklisted_physical_keys`, `gold_numeric_stage_count`, `has_stage`, `records_at`, `records_at_or_below`, `record_keys`, `get`, `n_snapshots`, `snapshot_times/positions/velocities`, `acceleration_magnitudes`, `stage_label`, `is_blacklisted`; `get(key)` returns an object with `ic13`, `masses`, `stage_label`, `n_snapshots`), and pass a checkpoint store that raises on `save` (D-27). The restricted source is validated by reproducing the checkpoint's monitor-batch targets, times and masses bitwise (done by scratch for 400 rows, 0 mismatches) and its IC13 within 1e-7.
**Alternative:** skip `RunController` and call its pure helpers directly on the serialized monitor batch; JX-1/2/4/10 need only the model, the batch and the anchor's ground truth at `t = 0`.

### Anti-Patterns to Avoid

- **Instantiating `AdmittedSetAdapter` or `_build_admitted_sources`:** opens test-split files (C-2).
- **Calling `compute_trajectory_gate_metrics` or `compute_validation_gate` for tiers:** finite-difference velocity (C-3).
- **Hard-coding the inner pair as canonical slots (0, 1):** canonical order is by descending mass; the inner pair is slots (1, 2) in 93.7% of Stage-0 systems and (0, 2) in 6.3% (train: 1,697 and 115; validation: 213 and 14). The closest-pair-at-`t=0` check holds on all 2,039 train and validation Stage-0 systems.
- **Comparing `MISSING_GOLD` with a string:** `SplitManifest.from_dict` decodes it to the enum sentinel in `pinn.data.types`; use `is`.
- **Writing evidence with absolute home paths:** record `data_root_source` as a label (the adapter's own `evidence_lines` redaction pattern, `adapter.py:1004-1040`).
- **Tests that cannot fail:** see Pitfall 11.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| Parsing, admission, gauge, scaling, invariants | A new parser or frame code | `parse_brutus_file`, `evaluate_admission`, `preprocess_trajectory`, `compute_invariants`, `build_raw_ic13`, `normalize_ic13` | Bitwise-reproduces the trainer's resident tensors (400 rows, 0 mismatches). |
| Split membership | Own hashing or regex over file names | `SplitManifest.from_path`/`from_dict` and `.physical_keys(...)` | Validates schema, duplicates, signature counts and Hamilton allocation. |
| Hamiltonian and `ε_H` | A new `H` | `matched_plummer_hamiltonian_series`, `trajectory_eps_h` (`gate_metrics.py:130-200`) | Gate convention (`eps_inv = 1e-10`, strict boundary). Not `compute_trajectory_gate_metrics`. |
| Autograd velocity | Finite differences; a summed-output VJP | `torch.func.jacrev` per output, or `componentwise_du` | `physics_residual.py:102-147` forbids the summed-output VJP. |
| Network and runtime construction | Own model builder | `build_network(ArchitectureSpec(seed=...), dtype, device)`, `resolve_runtime` | Same parameters and init as the run. |
| Monitor re-score, per-term loss helpers | Re-derived residual or loss formulas | `RunController._evaluate_front_monitor`, `_collocation_chunk_raw`, `_adam_frozen_causal_weights`, `_data_term`, `ic_anchor_loss` | D-23, and the chunking already bounds memory (D-25). |
| Atomic evidence writes | `open(...).write` | `pinn.training.atomic_io.atomic_write_text` | Existing convention. |
| Percentiles and ties | A custom quantile | `np.percentile` (linear) with an explicit `|N − q|` nearest rule and lowest-ID tie-break | Pin in the plan (C-10). |
| Kepler solver | Any package (none installed) | The 25-line `propagate_bound` above | Validated; scipy is unavailable. |

**Key insight:** the expensive mistakes in this phase are definitional (which velocity, which grid, which normalizer, which stage precedence), not numerical. Reuse the production functions and spend the effort on pinning definitions before any result is seen.

## Common Pitfalls

### Pitfall 1: Using the stock adapter and opening test files
**What goes wrong:** a run that "uses the production data path" parses all 7,606 groups.
**Why:** the adapter has no concept of splits at scan time (`adapter.py:814-820`).
**Avoid:** per-file functions behind `SplitAllowlist`; the test in Pattern 1; the audit hook.
**Warning signs:** a run that takes minutes and holds gigabytes; any `glob("*.txt")` in a Phase-59 module.

### Pitfall 2: Finite-difference `ε_H` makes Tiers 2 and 3 unreachable
**What goes wrong:** every arm, and the reference itself, scores Tier 0 or 1 on energy.
**Why:** a central difference over dt 0.08 cannot resolve inner periods of 0.1 to 1.5.
**Avoid:** autograd, analytic or Brutus velocities (C-3). **Warning sign:** a "reference against itself" `ε_H` above 1e-10.

### Pitfall 3: Assuming the inner pair is canonical slots (0, 1)
See the Anti-Patterns line. Track the pair through `preprocess_trajectory(...).permutation` (the adapter does not keep it, so re-run the per-file preprocessing; it costs about 2.6 ms per record).

### Pitfall 4: Aliased angle unwrapping
Plain unwrap on the 0.08 grid is exact for 91% of systems and wildly wrong for the fastest binaries (negative lap counts above about 60 laps). Use Pattern 5 and keep a "samples per inner period" column.

### Pitfall 5: The `MISSING_GOLD` sentinel
`group.signature[2]` is the enum `MISSING_GOLD`, not the string. A string comparison silently treats all 184 gold-less standard groups as having gold, and the next file open raises `FileNotFoundError` (this happened in a scratch script).

### Pitfall 6: The spec's `τ_L` snippet
It needs `scipy`, and `max_iter = M − max(nn)` can collapse to a single divergence point, so `np.polyfit` raises `LinAlgError`. Its Python loops also cost seconds per record. Use a vectorized numpy transcription whose divergence curve averages over all pairs still in range, with a pre-declared fit rule; keep the snippet's own defaults (`dt = 0.01`, `embedding_dim = 5`, `delay = 10`, `theiler_window = 100`) and linear resampling to `dt`. Report sensitivity to the window.

### Pitfall 7: Stage criteria that are empty or all-inclusive
Stage 3 is empty; Stage 6's clause is true of everything. Use the recorded precedence rule and report the counts.

### Pitfall 8: Interpreter and environment
`python -I -m pinn...` fails to import `pinn`; `conda run` buffers; `pinn-train` lacks pytest and scipy; `resolve_runtime` accepts only `("float32", "mps")` and `("float64", "cpu")` (`runtime.py:44-57`), so a "CPU float32" replay is not constructible through it.

### Pitfall 9: `RunController` construction and checkpoint integrity
The constructor builds a monitor from the train source before `load_state_dict` replaces it. `load_state_dict` raises if `front_monitor` or `lbfgs_segment_state` is missing and verifies the monitor hashes. Load checkpoints with `torch.load(path, map_location="cpu", weights_only=True)`; all 15 generation-7 seed-42 and smoke checkpoints load that way. [CITED: PyTorch 2.12 serialization notes, via Context7 `/websites/pytorch_2_12`: `weights_only=True` is the default since 2.6 and restricts the unpickler to tensors, primitive types and allowlisted globals; `weights_only=False` can execute arbitrary code.]

### Pitfall 10: Replay numerics differ across devices
The Phase-58 packet's monitor values were computed on MPS float32. A float64 CPU re-score will differ at roughly the 1e-6 level, and MPS-to-MPS runs are not guaranteed bit-identical. Declare the tolerance before running (front index exact; prefix sums within a stated relative tolerance).

### Pitfall 11: Known-error tests that cannot fail
On a rigid-rotation reference such as the Lagrange equilateral fixture (`tests/phase46/_fixtures.py:317-366`, wrapped by `make_dual_frame_trajectory` at `:401`), `H(t)` is constant, so scaling all velocities by any factor leaves `ε_H = 0`. That test passes for a broken scorer. The velocity-scaling test needs a reference with time-varying kinetic energy (an eccentric Kepler orbit, whose expected `ε_H` follows from vis-viva). The same fixture is ideal for the offset, time-shift (rigid rotation by `ωΔ` gives `E = 2 sin(ωΔ/2)` exactly) and frame-invariance tests.

### Pitfall 12: Pre-existing failing test
`tests/phase57/test_resource_preflight.py::FootprintReaderTests::test_current_footprint_rises_and_falls_with_a_touched_allocation` fails on this OS (STATE.md:640-646). Do not put `tests/phase57` discovery in a Phase-59 regression command; name adjacent suites explicitly. The same note means a memory guard that relies on the footprint falling cannot be trusted here; record `resource.getrusage` high-water marks instead.

### Pitfall 13: Gold file edges
Hierarchical gold files have 1,002 snapshots and end at about 10.01; base files have 126 snapshots ending at 10.000000000000007; standard base has 60 snapshots (one record has 59) ending at 10.03. Clip dense counts to `t ≤ 10`.

## Code Examples

### Safe checkpoint load and integrity check
```python
# Source: committed manifest .planning/phases/57-.../evidence/generation-7-retention.json (67 files, sha256 per file)
ck = torch.load(path, map_location="cpu", weights_only=True)
assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == retention[rel_path]["sha256"]
assert ck["counters"]["global_step"] == 900            # best.pt
assert ck["optimizer"]["state"][0]["step"] == 900.0    # keys: exp_avg, exp_avg_sq, step
```

### Refusal-before-open test pattern
```python
# unittest; dataset-free (tests.phase39._fixtures.TinyCorpus builds a miniature corpus under a TemporaryDirectory)
class RefusalBeforeOpenTests(unittest.TestCase):
    def test_test_split_id_refused_before_any_open(self):
        with TinyCorpus() as corpus:
            reader = AllowlistedCorpusReader(root=corpus.root, allowlist=make_allowlist(test_ids={7}))
            with mock.patch("pathlib.Path.read_text", side_effect=AssertionError("opened")) as spy, \
                 mock.patch("builtins.open", side_effect=AssertionError("opened")):
                with self.assertRaises(TestSplitRefused):          # not AssertionError: nothing was opened
                    reader.read(RecordKey("hierarchical", "base", 7))
            spy.assert_not_called()
    def test_missing_root_distinguishes_refusal_from_io(self):     # refusal must precede path/IO errors
        reader = AllowlistedCorpusReader(root=Path("/nonexistent"), allowlist=make_allowlist(test_ids={7}))
        with self.assertRaises(TestSplitRefused): reader.read(RecordKey("hierarchical", "base", 7))
        with self.assertRaises(FileNotFoundError): reader.read(RecordKey("hierarchical", "base", 1))
```

### Static no-training and no-evaluator checks
```python
# AST scan of every Phase-59 module (pattern: tests/phase46/test_isolation.py:192-239 and phase39/test_prohibitions.py:89-108)
FORBIDDEN_ATTRS = {"optim", "Optimizer", "save", "save_checkpoint", "TorchSaveCheckpointStore"}
FORBIDDEN_IMPORT = "pinn.evaluate"           # the held-out evaluator (SCOPE-40)
# plus a subprocess import: python -c "import pinn.verification.feasibility_scorer, sys; assert 'pinn.evaluate' not in sys.modules"
```

## State of the Art

| Old approach | Current approach | When changed | Impact |
|--------------|------------------|--------------|--------|
| `torch.load` unpickles arbitrary objects | Default `weights_only=True` | PyTorch 2.6 | Safe loads of the retained checkpoints; no code execution. |
| Gate `ε_H` from finite-difference velocity (v2.2 Phase 46) | `ε_H` from autograd or analytic velocity for accuracy tiers (this phase) | Phase 59 | Tier 2 and 3 become reachable by construction. |
| Stage labels 0 and 1 only (production) | Static spec criteria for a diagnostic survey (this phase) | Phase 59 | Non-gating; the final stage mapping stays owner-pending (`ctl_instruction.md:326-347`). |

**Deprecated or outdated:**
- `pinn/data-handling/processing/rosenstein_lyapunov.py`: v1.3-era; imports `scipy` and `sklearn`, and `sklearn` is absent from both `pinn-train` and `.venv`. A cross-check needs a stubbed `sklearn.decomposition` (its `full_state` path does not use PCA) and the `.venv` interpreter; never the source.
- The `batches.py:271-273` citation in the `validation_gate.py` docstring is stale; cite `build_gate_inputs` (`validation_gate.py:177-191`) for `τ = 2·(t/T) − 1`.

## Answers to the Twelve Planning Questions

### Q1. Data root

**Answer.** Generation 7 read `<home>/Desktop/3_body_problem/simulation_data/Data` (the main checkout), by the default rule. Evidence:
- `runs/stage0-v23g7-seed42/config.yaml:3` `root: null`; the launch config `configs/stage0-v23g7-seed42.yaml` has `data: source: admitted, blacklist_path: ../Documentation/problematic_ics_blacklist.json` and no `root`.
- Resolution order (`adapter.py:743-753`): explicit root, then env `GSD_DATA_ROOT` (`DATA_ROOT_ENV`, `adapter.py:560`), then `default_data_root()` (`:594-606`), the parent of `git rev-parse --git-common-dir` plus `simulation_data/Data`. From this worktree, `git rev-parse --git-common-dir` prints `<home>/Desktop/3_body_problem/.git`. `GSD_DATA_ROOT` is unset in the agent shell, and `launch.json` records argv, cwd and `git_head` but not the environment, so a launch-time override cannot be excluded from the record alone; congruence is proven by data instead (below).
- The full corpus is there: `brutus_output` folders hold 4,857 / 4,857 / 2,749 / 2,565 files (hierarchical, hierarchical gold, standard, standard gold), `ic_final` holds 4,857 and 2,749, 4.8 GB and 30 MB. This worktree's `simulation_data/Data/` holds only `brutus_output`, `forensic`, `ic_final` and `testing_data` stubs. The blacklist `simulation_data/Documentation/problematic_ics_blacklist.json` exists (647 bytes).
- Congruence proof, measured: 7,606 manifest groups equal the 4,857 + 2,749 IDs on disk; all 6,085 training-split base records parse and preprocess with 0 failures; 400 sampled rows of the generation-7 monitor batch (210 records) match the recomputed targets, times and masses bitwise.

**API (production per-file path, not the adapter):** `pinn.data.adapter.default_data_root`, `DATA_ROOT_ENV`, `BRUTUS_FOLDER_TABLE` (`:81-86`), `parse_brutus_file(path, root=...)` (`:386`, containment through `resolve_within_root`), `to_parsed_trajectory`, `load_blacklist_file` (`:609`), `pinn.data.admission.evaluate_admission` (`:128`), `pinn.data.preprocessing.preprocess_trajectory`, `compute_invariants`, `build_raw_ic13`, `normalize_ic13`.

**Plan action:** a data-root check as the first task: resolve the root, assert every allowlisted manifest group's base file exists, and assert the monitor-batch bitwise reproduction (this is also the Q5 and DIAG-07 equivalence test).

### Q2. Splits

**Structure** (`splits.json`, `algorithm group-signature-hamilton-v1`, seed 42, ratios 0.8 / 0.1 / 0.1): top-level keys `algorithm, groups, ratios, schema_version, seed, signatures, tie_order`. `groups` is a list of 7,606 dicts with keys `physical_key {id, variant}`, `records` (each `{fidelity, id, stage, variant}`, with `stage` 0, 1 or `"UNASSIGNED"`), `signature {base_stage, gold_stage, variant}` and `split` in `{train, validation, test}`. The per-group split assignment lives in `group["split"]`.

| Signature (variant, base stage, gold stage) | Train | Validation | Test |
|---|---|---|---|
| hierarchical, 0, UNASSIGNED | 1,812 | 227 | 226 |
| hierarchical, 1, UNASSIGNED | 2,074 | 259 | 259 |
| standard, UNASSIGNED, UNASSIGNED | 2,052 | 257 | 256 |
| standard, UNASSIGNED, MISSING_GOLD | 147 | 19 | 18 |
| Total groups | 6,085 | 762 | 759 |

The Stage-0 population is `signature == ("hierarchical", 0, "UNASSIGNED")`: 1,812 train (matches `training_metadata.json` `n_train: 1812`) and 227 validation. Training-split files: 6,085 base plus 5,938 gold (3,886 hierarchical, 2,052 standard) = 12,023.

**Building the allowlist and proving refusal:** Pattern 1, plus the audit hook, plus the unit test in Code Examples. **Existing enforcement:** `SplitManifest.physical_keys`/`.splits` (`splits.py:376-395`), `StageIndex.from_split` (`:170-186`, in-memory views that require the full source to match the manifest), `write_split_manifest` (`:779`, refuses a run directory inside the repository corpus), the Phase-46 `resolve_probe_population` (`target_frame_probe.py:1006-1069`, a pure function with an exclusion ledger), and the Phase-46 isolation tests (AST scan plus fresh-subprocess import check, `tests/phase46/test_isolation.py:192-239`). None prevents a file from being opened; Phase 59 adds that.

### Q3. Frames

- **Network frame:** input `[τ, IC13]` with `τ = 2·(t/T) − 1` (`validation_gate.py:177-191`: `tau = (2.0 * (t / float(T_CHARACTERISTIC_TIME)) - 1.0)`), output the mass-weighted COM-projected `r′` (`network.py:210-228`). Constants: `D_CHARACTERISTIC_LENGTH = 100.0 ** (1.0 / 3.0)` and `T_CHARACTERISTIC_TIME = 10.0` (`constants.py:19,27`); spec `ctl_instruction.md:998-999`: `T = t_max = 10`, `D = (G*T**2)^(1/3)`.
- **Pipeline transform** (`preprocess_trajectory`, `preprocessing.py:174-221`): COM recentre and zero-momentum boost, canonical order (descending mass, then position norm, velocity norm, file order; `:112-123`), rotation gauge from the Jacobi basis at `t = 0` (`:126-171`), then `r′ = r/D`, `v′ = v/V` with `V = D/T`. It returns `masses_ordered`, `permutation`, `r_com_ordered`/`v_com_ordered` (ordered but not rotated or scaled), `r_gauge`/`v_gauge` (the scaled, gauged arrays the network predicts in), `R0`, `D`, `T`. Resident arrays keep native times; `dr′/du = v′`.
- **Masses:** `ordered_raw` (the frame record in `training_metadata.json`: `mass_convention ordered_raw`, `position_frame r_prime`, `time_coord u_t_over_T`).
- **Network output to `(r, v)` for `H`:** `r′` from the forward pass; `dr′/du` from `jacrev` (Pattern 2); `H′(r′, dr′/du) = D·H(r, v)`, so `ε_H` needs no conversion and is the same in either frame (a test: pass the raw-frame arrays and the scaled-frame arrays of `make_dual_frame_trajectory`).
- **Where the existing gate computes `ε_H`:** `gate_metrics.matched_plummer_hamiltonian_series` (`:130-172`) and `trajectory_eps_h` (`:180-200`); the FD route is `compute_trajectory_gate_metrics` (`:211-222`) called from `compute_validation_gate` (`validation_gate.py:257-259`). Constants: `EPS_INV = 1e-10` (`:59`), `GATE_EPS_H_REJECT_THRESHOLD = 1e-5`, `GATE_SCS_REJECT_THRESHOLD = -5.0` (`:64-65`); the boundary passes (strict-inequality reject).
- **Trainer's own autograd velocity:** `controllers.py:1160-1163` (`first0, _second0 = componentwise_du(anchor_ctx.traj, zero_u)`; `pred_v0 = first0.reshape(3, 3)`) and `:1173-1176`.

### Q4. Brutus trajectory format

Blocks of `t N t_cpu` plus three `m x y z vx vy vz` rows, blank-line separated; velocities are in the file (`adapter.py:330-366`, `parse_brutus_text`). Hierarchical base: 126 snapshots, `t = 0` to `10.000000000000007`, dt 0.08 exactly, for all 1,812 train and 227 validation Stage-0 files. Hierarchical gold: 1,002 snapshots, dt 0.01, ending near 10.01. Standard base: 60 snapshots (one record 59), dt 0.17, ending 10.03. Standard gold: dt 0.01. Output is float64 with 30 to 40 significant digits. Trajectories are complete iff the final time is at least 9.5. Admission recomputes `ε_H` from the file's own velocities; the reference values are 5e-15 to 3e-14 on the 25 sampled systems.

### Q5. IC13 normalization

Formula: `tanh((z − μ)/(σ + 1e-8))` for slots 0 to 11 and `tanh(E/e_scale)` for slot 12 (`preprocessing.py:342-348`); IC13 layout `[m1, m2, m3, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]` (`:290-317`). Statistics: computed once over every admitted record of all four folders (`adapter.py:892-893`, `:938-942`), private, never persisted. Recovery from a retained checkpoint: Pattern 6. Fallback if the recovery assertion fails: recompute from train and validation records and record the deviation as a gap (the result would not be the production normalizer).

### Q6. Stages beyond 1

- **Production:** `classify_stage_label` (`stages.py:58-85`) returns only `STAGE_0`, `STAGE_1`, `UNASSIGNED`, and only for hierarchical base records; every gold record is `UNASSIGNED`. The manifest already carries these labels (`records[*].stage`), so Stage 0 and 1 need no recomputation.
- **Spec criteria** (`ctl_instruction.md:138-264`, verbatim thresholds): Stage 0: `E < -0.5`, `L/L_max > 0.5`, `0.7 ≤ Q ≤ 1.3`, `s_min > s_0` (hierarchical base). Stage 1a: `-0.5 ≤ E < -0.1`; Stage 1b: `E < -0.5`, `0.1 ≤ L/L_max < 0.5`. Stage 2: hierarchical gold of the same systems ("Union of Stage 0 and Stage 1 criteria"). Stage 3 (low-fidelity quasi-random): `E ≤ E^LF_25%`, `L/L_max ≥ L^LF_75%`, `0.9 ≤ Q ≤ 1.1`. Stage 4a: `τ_L > 5`; 4b: `2 < τ_L ≤ 5` (remaining low-fidelity). Stage 5: gold quasi-random, "Same as Stage 4". Stage 6: `s_min < 0.5` OR `|E| < 0.01`, "All remaining data; HF+LF". The stage mapping beyond 0 and 1 is "owner-pending the FUT admitted-set EDA run" (`ctl_instruction.md:326-347`, `:1654-1665`).
- **Recorded invariants for all variants:** yes. `compute_invariants` on the scaled `t = 0` state (`preprocessing.py:241-259`) gives `E, Q, s_min, l_ratio` for every admitted record of every variant and fidelity, with no metrics file needed (the `metrics/` JSONs are in raw units, hold conservation and separation statistics and no `τ_L`, and admission forbids them as an input). Gold records share their base record's initial state.
- **Measured invariants, training split, base records** [VERIFIED: scratch measurement, 6,085 records, 9.0 s, 0 failures]:

| Population | n | E (min / median / max) | Q range | s_min range | L/L_max range | Notes |
|---|---|---|---|---|---|---|
| Standard base | 2,199 | -13.55 / -8.60 / -6.31 | 0.001 to 0.119 | 0.147 to 0.440 | 0.002 to 0.091 | `Q ∈ [0.9, 1.1]`: 0; `s_min < 0.5`: all |
| Hierarchical Stage 0 | 1,812 | -32.6 / -7.37 / -2.5 | 0.889 to 1.166 | 0.017 to 0.084 | 0.500 to 0.683 | |
| Hierarchical Stage 1 | 2,074 | -51.8 / -11.59 / -3.46 | 0.795 to 1.153 | 0.014 to 0.083 | 0.141 to 0.500 | all are Stage 1b; 1a is empty (E at most -3.46) |

  Implied survey populations (ascending precedence, training split): Stage 0: 1,812; Stage 1: 2,074; Stage 2: 3,886 (hierarchical gold); Stage 3: 0; Stage 4a/4b/6 and Stage 5 split the 2,199 standard base and 2,052 standard gold records by `τ_L`.
- **`τ_L` cost and sensitivity** [VERIFIED: scratch measurement, vectorized numpy]: 0.02 to 0.05 s per record, so about 12,000 training-split records take 4 to 10 minutes single-threaded (the spec's Python-loop snippet would take hours). Class fractions on 100 sampled standard base records: fit window 0.5 time units: 65% `τ_L ≤ 2`, 3% in (2, 5]; window 1.0: 63% and 5%; window 2.0: 49% and 19%; window 3.0: 10% and 32%; "half-pairs" rule (fit until fewer than half the reference pairs remain, about 3.8 time units): 37% `τ_L = ∞`, 27% in (2, 5], 9% `≤ 2`. On Stage-0 hierarchical samples the median `τ_L` is about 10 with 22% to 27% in (2, 5], so even regular orbits score as weakly chaotic. These are diagnostic values; the Stage-4b median pick depends on the pre-declared rule (C-5).
- **Cross-check reality:** the legacy `rosenstein_lyapunov.py` cannot be imported in either environment (needs `sklearn`); stub it and run under `.venv` for a handful of systems, as a sanity check of order of magnitude only.
- **Plan actions:** pre-declare the precedence, the Stage-3 percentile population, and the `τ_L` window rule in `59-GAPS.md`; compute `τ_L` with the committed vectorized estimator; report Stage 3 as empty with its measured `Q` range.

### Q7. Generation-7 code revision and checkpoints

- **Commit:** `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b` (`plan(57): prepare generation-seven detached band`, 2026-10-02 21:44 -0500). Recorded in four independent places: `runs/.launch/stage0-v23g7-seed42/invocation-1/launch.json:14` (`git_head`), `generation-7-verify-marker.json` (`fingerprint.git_head`), `terminal-state.json` (`git_head`), and `run-ledger.md`. The Phase-57 `admit-run-window` verifier (C14) passes only for a clean immutable HEAD. Reachable from `milestone/v2.3` and `milestone/v2.4`.
- **Identity with HEAD:** `git diff --quiet 629b1a6c HEAD -- pinn configs` exits 0; `git status --short pinn configs` is empty. The only later commits touching tests are `7247d503` (test paths) and `e0ec85f6` (evidence).
- **Launch:** `/usr/bin/caffeinate -is <home>/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/stage0-v23g7-seed42.yaml --stage-0-only`, MPS float32, torch 2.12.1, Python 3.11.15, macOS 26.5.1, 11,662 s, tripped invariant B at step 951.
- **Checkpoints** (all load with `weights_only=True`; SHA-256 prefixes equal the committed `generation-7-retention.json`):

| File | `global_step` | Adam moments (`exp_avg`, `exp_avg_sq`, `step`) | SHA-256 prefix | Use |
|---|---|---|---|---|
| `stage-0-init.pt` | 0 | no (`optimizer: None`) | c8eab3e7a8e894da | checkpoint 0 (JX-1, JX-3, JX-5) |
| `ckpt-158375347798.pt` | 0 | no | eb579d840b0f0e3b | run-start anchor, recorded |
| `best.pt` | 900 | yes, step 900 | 21c69f2d9f975689 | **checkpoint 900** (C-1) |
| `step-000931.pt` | 931 | yes | 1983092ecb6b47b7 | supplementary |
| `step-000941.pt` | 941 | yes | 1d9cad46a660e3ab | supplementary |
| `step-000951.pt` | 951 | yes | 810235516ffdd304 | **checkpoint 951** |
| `latest.pt` | 951 | yes | 2ef786a44f23f93d | recorded |
| `failure-stage-0-step-951.pt` | 951 | yes | d94516f3315fcda1 | recorded |
| smoke `step-000100/200/300.pt` (`runs/stage0-v23g7-smoke`) | 100/200/300 | yes | 7de5f691…, db5fac7b…, 5e3d804b… | JX-10 |

JX-1 needs the Adam moments, so it runs on `best.pt` and `step-000951.pt`; at `stage-0-init.pt` there are no stored moments (C-11). Full 64-hex hashes are in `generation-7-retention.json`.

### Q8. JX experiment definitions, inputs and outputs

Source: `trainex-r4-resolution-doc.md:644-655` (JOIN-4-EXPERIMENTS table) and `trainex-r4-ruling.md:124-137` (checkpoints 0, 900 and 951 for JX-1; JX-3 validation-split trajectories allowed; no test file).

| ID | Definition (quoted or closely paraphrased) | Inputs | Outputs | Supports or falsifies |
|---|---|---|---|---|
| JX-1 (executed half) | Per-term gradients `g_IC`, `g_phys`, `g_data`; their cosines; the share of the Adam-preconditioned update (from the stored moments) along `−g_phys`; the IC term's position/velocity split. Run on the frozen monitor batch | Checkpoints 0, 900, 951; the serialized monitor batch (8,192 data rows, 4,096 collocation rows, 256 identities); anchor trajectory 28 (`replay_keys[0]`, the lowest-ID replay identity, `controllers.py:1075-1079`) ground truth at `t = 0` from one allowlisted train file | Per-term gradient norms, 3 cosines, shares, IC position and velocity components, per checkpoint | "Physics was a passenger": share `≲ 10⁻⁴` confirms (readout branch b), `≳ 10⁻²` overstates it (branch c) and fires Gate G1; in between is branch (d) |
| JX-2 | Trajectory 28's prefix sums under K = 20 fresh stratified time draws at each retained checkpoint (about 15 min) | Model weights, trajectory 28's IC13 and masses (in the monitor batch), fresh 4,096-row stratified draws | Spread of the monitor estimator per checkpoint | Separates estimator noise from parameter motion (J1.c, J5.a) |
| JX-3 | Prefix profile and IC error at checkpoints 0 and 951 for high-exposure anchors, never-anchored training trajectories and validation trajectories (about 1 h for 40 trajectory-checkpoints) | Weights, IC13 and ground truth of chosen trajectories (allowlisted train and validation files), exposure counts from a replay of the executed selection stream | Per-trajectory profiles | Global improvement (amplitude shedding) versus exposure-specific fitting |
| JX-4 | Raw residuals, IC errors and trajectory errors on fixed training-only fixtures; and the monitor batch with each slot's residual divided by its true `‖a′‖²` scale | Weights, fixtures, true accelerations (softened force from ground-truth positions, `softened_acceleration`, `physics_residual.py:193`) | Relative-versus-absolute table | Informs `JD-3`'s physical normalization only |
| JX-5 (split) | Initialization-only decomposition at the default architecture: acceleration, force, IC position/velocity error, mixed derivatives, skip contributions | `build_network(ArchitectureSpec(seed=42))` or `stage-0-init.pt` | Scale table per component | Apportions derivative scale (structural evidence; not a generation-7 measurement) |
| JX-10 | Re-score the smoke's frozen monitor at steps 100, 200, 300; reproduce the monitor-recompute values; from checkpoint contents only | Smoke checkpoints (generation-7; generations 5 and 6 are also retained with the same steps) | Front index and prefix sums per step | Closes `C-F14`, `F-H2b`, `C-07` (front 0 at steps 100/200/300; transient at step 93) |

**Existing tooling:**
- `pinn/verification/architecture_characterization_probe.py` (Phase 55): initialization-only residual measurement through the trainer's own `causal_physics_loss`, `componentwise_du`, `softened_acceleration`; covers part of JX-5 (`‖r′‖`, `‖v′‖`, `‖a′‖`, `‖F_grav‖`) but not IC error or skip contributions.
- `pinn/verification/gate04_train_free.py`: init-case R_ref gate; not a JX tool, relevant only for Phase 62.
- `pinn/verification/phase57_production_conformance.py`: precedent for `RunController` on a duck-typed source.
- Phase-58 replay script, verbatim in `v2.3-closure-evidence-bundle.md:304-392` (script SHA-256 `0e1297faf4aa1cfe495869eb316beac6bcbc883e7fb98f9fd7fb99c07e2b9bcd`): builds `RunController`, loads each checkpoint, calls `_evaluate_front_monitor`; its raw output (`:400-408`) gives reference values for JX-10 (for example step 900 `best.pt`: front 1, `prefix_through_front 0.7277`; step 951: front 2, `1.1891`).
- The trainer's microbatched Adam step already computes per-term raw gradient vectors for its logged norms (`controllers.py:1822-2017`, `raw_grads` via `torch.autograd.grad` per term); only the norms are kept, so JX-1 needs a driver that mirrors that Pass 2 using `_adam_frozen_causal_weights`, `_collocation_chunk_raw` and the same `row_weight_chunk` formula (`:1918-1921`), and checks its norms against `_run_adam_step_microbatched(..., want_diagnostics=True)`, which does backward but no optimizer step. Logged cross-check at step 900 (training batch, not the monitor batch): `grad_norm_raw_ic` 3.03e6, `grad_norm_raw_phys` 109.0, `grad_norm_raw_data` 1.46, `lr` 2.447e-5 (`logs/train.log.jsonl`).
- The EDL-style candidate definitions for the G1 share, to be pre-registered: primary = `⟨Pg_phys, Pg_tot⟩ / ‖Pg_tot‖²` with `P = diag(1/(√v̂ + ε))` from the stored `exp_avg_sq` (bias-corrected by the stored step) and `g_tot = Σ λ_k g_k` at the scheduled weights (the shares then sum to 1); secondary = the same with the stored first moment `m̂` in place of `g_tot`. Report both; evaluate G1 on the primary.

### Q9. Verification patterns

- **Layout:** `tests/phaseNN/__init__.py`, `_fixtures.py`, `test_*.py` as `unittest.TestCase`; shared fixtures to reuse: `tests/phase39/_fixtures.py::TinyCorpus` (deterministic on-disk miniature corpus, context manager), `tests/phase40/_fixtures.py::make_stub_model`, `tests/phase46/_fixtures.py::{StubStageSource, make_dual_frame_trajectory}`.
- **Run (Phase-57 convention, `57-VALIDATION.md`):** `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phaseNN -p 'test_*.py' -v`; for streaming output on long runs call `<home>/miniforge3/envs/pinn-train/bin/python` directly. Baseline this session: `tests.phase39.test_prohibitions tests.phase39.test_splits tests.phase39.test_adapter tests.phase46.test_isolation` = 175 tests OK in 1.5 s (use `python -B` to avoid writing bytecode).
- **Tool shape:** `pinn/verification/<tool>.py` with `main(argv=None)`, `argparse`, `__all__`, an evidence root default under `.planning/phases/<phase>/evidence/`, `_reject_dataset_evidence_root`, atomic writes (`overfit_probe.py:79-136`).
- **Evidence hashing:** Phase 57 committed `evidence/*.json` with byte sizes and SHA-256 per file (`generation-7-retention.json`: 67 files), `gate04/<UTC>/raw.json` whose hash is recorded in the governed artifact, an append-only `run-ledger.md`, and a verifier script with subcommands (`verify_phase57_evidence.py`). Mirror this: `evidence/manifest.json` plus `verify_phase59_evidence.py`.

### Q10. Two-Kepler formula

No Kepler or orbital-element propagation code exists in the repository (a grep of the Python sources finds none outside reference material). `simulation_data/Scripts/ic_generation/ic_generation_utils.py:344-420` only constructs ICs (circular velocity at `r_inner = a_inner(1 − e_inner cos M)`, then Gaussian N(0, 0.01) on every component, so the measured osculating inner eccentricity at `t = 0` is 0.002 to 0.368, median 0.084). Use Pattern 4. Pitfalls and how the design avoids them: eccentricity near 0 (no pericentre direction used), inclination (vectors, not elements), unbound orbit (`NotApplicable`), long durations (`ΔE` up to about 630 rad converges with Newton from `n·Δt`), frames (propagate in the pipeline frame with the same masses). All 1,812 + 227 Stage-0 systems have bound inner and outer orbits.

### Q11. Inner-lap counting and the real distribution

Pattern 5 for the method. Aliasing relative to dt 0.08: Kepler-estimated `P_in` (train) ranges 0.099 to 1.577 (median 0.54); fewer than two samples per period for 28 systems (1.5%), fewer than three for 7.8%, fewer than five for 29.7%. Measured distribution on all 1,812 training systems (gold-grid unwrap, `t ≤ 10`) [VERIFIED: scratch measurement, 18.9 s]:

| Quantile | 0 | 1 | 5 | 10 | 25 | 50 | 75 | 90 | 95 | 99 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `N_in` | 2.82 | 7.95 | 9.46 | 10.47 | 13.27 | 18.61 | 27.75 | 39.35 | 47.55 | 64.86 | 101.74 |

`N_out`: 0.44 to 12.0, median 1.82, 14.0% below 1. Phase-accuracy figure `δ/(2πN_in)`: for `δ = 0.10`, median 8.6e-4 (1 part in 1,170), 1 in 653 at `N = 10.4`, 1 in 2,450 at `N = 39`, 1 in 6,350 at `N = 101` (this matches the amendment's "1 part in 600–5,000"); for `δ = 0.01`, ten times tighter (median 1 in 11,700). Preview single systems (nearest to the 10th, 50th, 90th percentile of this estimator, by `|N − q|`, lowest ID on ties): ID 1632 (`N_in` 10.47), ID 851 (18.61), ID 4658 (39.35). They depend on the pinned estimator; use them only to sanity-check the committed code.

**Pinning the panel rule (C-10), recommended text:** percentiles by `np.percentile(N_in, q)` (linear); a system's distance is `|N_in − q|`; ties go to the lowest ID. Family: sort by `(N_in, id)`; `np.array_split` into 16 bins (sizes 114 for the first 4 bins and 113 for the other 12); the bin median is `np.median` of the bin's `N_in` values; pick the system with the smallest `|N_in − median|` not among the three singles, lowest ID on ties. Validation panel: all 227.

**G2 grid evidence** (first-layer weights are `U[-1/14, 1/14]`, `network.py:81-83`, so the initial time-frequency edge is `ω₀/14` rad per unit `τ`; a system with `N` laps needs about `πN` rad per unit `τ`):

| `ω₀` | 30 (locked) | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|
| Initial edge `ω₀/14` (rad per unit `τ`) | 2.1 | 4.3 | 8.6 | 17.1 | 34.3 |

| Census quantile of `N_in` | p10 | p50 | p90 | p99 | max |
|---|---|---|---|---|---|
| Required `πN` (rad per unit `τ`) | 33 | 58 | 124 | 204 | 320 |

The CONTEXT default grid `{60, 120, 240, 480}` tops out at about the p10 requirement, which is the right calibration because Phase 60 runs the sweep first on the failing system with the fewest inner laps; higher `ω₀` also needs weight growth for harder systems. Recommendation: keep the default grid; if the plan wants the top value to reach the median requirement, replace 60 with 960 (initial edge 68.6). The choice is the plan's; freeze it in the scorecard.

### Q12. Memory and runtime

Measured on this M5 Pro Mac (24 GB, 15 cores, macOS 26.5.1, MPS available, 605 GiB free):

| Task | Cost |
|---|---|
| Parse and preprocess 2,039 Stage-0 base files | 3.6 s |
| Invariants for all 6,085 training-split base records | 9.0 s |
| Gold-grid census over 1,812 systems | 18.9 s |
| Two-Kepler formula over 1,812 + 227 systems | 4.1 s |
| Nearest-neighbour copy over 227 validation systems | under 1 s after loading |
| `τ_L` (vectorized) | 0.02 to 0.05 s per record; about 12,000 records in 4 to 10 min |
| Survey file reads | about 30 s |
| JX-1 at 3 checkpoints | minutes (forward and backward on 4,096 collocation plus 8,192 data rows in 256-row microbatches) |
| JX-2 (K = 20 draws, 5 checkpoints) | about 15 min per the resolution doc |
| JX-3 (40 trajectory-checkpoints) | about 1 h (about 45 s each, `F-X2` unverified) |
| JX-4, JX-5, JX-10 | minutes each; the Phase-58 replay of 8 checkpoints took 359 s including the adapter scan |
| Whole phase, machine time | on the order of 2 to 3 hours, dominated by JX-3 |

Memory: all pure-numpy work is well under 1 GB. The unchunked monitor evaluation built every physics term's graph at once and measured 1.5 to 22.8 GB of footprint (`controllers.py:1033-1037`); the trainer's microbatched path (`opt.adam_microbatch_size: 256`) bounds it. Reuse `_evaluate_front_monitor`, `_collocation_chunk_raw` and `_release_chunk_memory`; do not write a new full-batch evaluation. Record `resource.getrusage(RUSAGE_SELF).ru_maxrss` as a high-water mark (the footprint reader is unreliable on this OS, Pitfall 12).

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|-------|---------|---------------|
| A1 | Gate G1 will probably not fire: logged raw gradient norms at step 900 give a physics-to-IC ratio near 4e-5, and Adam's preconditioning should keep the share in the 1e-5 to 1e-4 range | Q8 | Low: only a forecast; the experiment decides. |
| A2 | A float64 CPU re-score agrees with the Phase-58 MPS float32 values to about 1e-6 relative | Pitfall 10 | Medium: tolerances must be declared before running; a wider gap would need an MPS replay. |
| A3 | The gold sibling is an acceptable dense view of the base reference for all Stage-0 systems (agreement at most 5.7e-9 on 300 sampled systems) | Pattern 5, C-4 | Low: check all 1,812 in the committed census. |
| A4 | The `π` safety bound for the mean-motion-assisted unwrap holds on the gold-less populations | Pattern 5 | Low: it is only a cross-check with a flag. |
| A5 | "Stage 6 = residual after Stages 0 to 5" is the intended reading of "All remaining data" | C-5, Q6 | Medium: the alternative (Stage 6 evaluated first) labels almost everything Stage 6. Resolve by a gap entry. |
| A6 | Stage-3 percentile thresholds are meant over the training-split low-fidelity population | C-5 | Low: Stage 3 is empty either way because of the `Q` window. |
| A7 | The G1 share formulas in Q8 match what the ruling meant | C-11 | Medium: Gate G1 depends on it; pre-register and report both. |
| A8 | "The smoke" in JX-10 is the generation-7 smoke (steps 100/200/300 exist for generations 5, 6 and 7) | Q8 | Low. |
| A9 | For the nearest-neighbour copy, `ε_H` uses the neighbour's own masses (moot at Tier 0 everywhere in the preview) | Q6 | Low. |
| A10 | The preview baseline numbers and panel IDs will be reproduced by the committed code | Summary, Q11 | Low: they are checks on the code, not inputs. |

## Open Questions (RESOLVED)

Each question below was resolved before planning; the pointer after it names where (orchestrator, 2026-10-11).

1. **Gate G1: share formula and checkpoint rule.** Known: threshold `10⁻²`; Claude's wording; checkpoint 0 has no moments. Unclear: primary formula, which checkpoints. Recommendation: pre-register the primary and secondary formulas of Q8 and "fires if the primary share is at least `10⁻²` at checkpoint 900 or 951" in `59-GAPS.md` before the experiment runs. **RESOLVED:** GAP-59-05 and D-34.
2. **Scoring grid.** Known: D-02 uses the base output times; 1.5% to 7.8% of systems are aliased on it. Unclear: whether a dense-grid `E_dense` is gating. Recommendation: reported, with the aliasing flag, and single-system picks required to have at least 3 samples per inner period. **RESOLVED:** GAP-59-07 and D-31. The dense grid was made tier-defining, which is stricter than this recommendation.
3. **IC13 normalizer source.** Recommendation: recovered from the retained checkpoint, with the residual assertion; fallback is a recorded deviation. **RESOLVED:** GAP-59-06 and D-35.
4. **DIAG-07 execution path.** Duck-typed allowlisted source with `RunController` (Pattern 7) versus direct helper calls. Recommendation: the `RunController` path, because the ruling asks for the code that produced the run, with the bitwise monitor-batch equivalence test as its acceptance gate. **RESOLVED:** the RunController path is adopted (D-36; plan 59-07), with the bitwise monitor-batch equivalence test as its acceptance gate.
5. **Device.** Recommendation: MPS float32 (the run's own runtime; available in this shell) as the primary and a float64 CPU cross-check on JX-1 and JX-10. **RESOLVED:** D-36: MPS float32 primary, CPU float64 cross-check.
6. **`τ_L` rule.** Recommendation: spec defaults (`dt = 0.01`, `d = 5`, `delay = 10`, `Theiler = 100`) with linear resampling; divergence averaged over all pairs in range; fit over the "half-pairs" range; sensitivity columns for fixed windows of 1, 2 and 3 time units; the FEAS-09 pick follows the primary rule and reports whether it changes under the sensitivity windows. **RESOLVED:** GAP-59-04 and D-33.
7. **Candidate gap entries** (resolvable under the delegation, none moves a locked value): GAP-59-01 `best.pt` is checkpoint 900 (D-22); GAP-59-02 `ε_H` velocity source (C-3); GAP-59-03 stage precedence and the empty Stage 3 (C-5); GAP-59-04 `τ_L` parameters and fit-window rule; GAP-59-05 G1 share formula (C-11); GAP-59-06 IC13 normalizer source; GAP-59-07 dense-grid column (C-4). **RESOLVED:** all recorded as GAP-59-01..07 in 59-GAPS.md.
8. **Allowlist edit.** Editing `tests/phase39/test_prohibitions.py` is a cross-phase test edit with precedent (plan 46-04). Recommendation: do it for exactly one module, with a comment. **RESOLVED:** D-35: exactly one module.

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `pinn-train` Python | All tools and tests | yes | 3.11.15 (`<home>/miniforge3/envs/pinn-train/bin/python`) | none needed |
| conda launcher | `conda run -n pinn-train` | yes | `<home>/miniforge3/bin/conda` | call the env interpreter directly |
| torch with MPS | DIAG-07, scorer on networks | yes | 2.12.1, `mps.is_available()` True | float64 CPU (`resolve_runtime("float64", "cpu")`) |
| numpy, PyYAML | everything | yes | 2.4.6, 6.0.3 | — |
| scipy, pandas, sklearn, psutil | not needed | no (in `pinn-train`) | `.venv` has scipy 1.17.1 only | numpy and stdlib |
| pytest | optional convenience | no (in `pinn-train`); yes in `.venv` | 9.1.1 | `unittest` |
| Full corpus | census, baselines, survey, DIAG-07 | yes | `<home>/Desktop/3_body_problem/simulation_data/Data` | none (blocking if absent) |
| Gen-7 run directory and checkpoints | DIAG-07 | yes (gitignored, in this worktree) | 8 seed-42 files, 7 smoke files | none |
| `splits.json` | allowlist | yes | sha256 `5846ae5b…8d6` | none |
| Disk, RAM, CPUs | all | yes | 605 GiB free, 24 GiB, 15 cores | — |
| `git` | identity proof, snapshot | yes | worktree layout confirmed | — |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** scipy, pytest, pandas, sklearn (use numpy and `unittest`).

## Validation Architecture

> `workflow.nyquist_validation` is `true` in `.planning/config.json`, so this section is required and feeds `59-VALIDATION.md`.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` (tests are `TestCase` classes, also runnable under pytest in `.venv`) |
| Config file | none; new package `tests/phase59/` (Wave 0) |
| Quick run command | `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest tests.phase59.<module> -v` |
| Full suite command | `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest discover -s tests/phase59 -p 'test_*.py' -v` |
| Adjacent regression | `... python -B -m unittest tests.phase39.test_prohibitions tests.phase39.test_splits tests.phase39.test_adapter tests.phase46.test_isolation` (175 tests, 1.5 s baseline) |
| Real-corpus checks | `... python -m pinn.verification.stage0_census --check`, `... baselines --check`, `... dataset_survey --check`, and `python .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py <subcommand>` |

### Phase Requirements to Test Map

| Req ID | Behavior | Test type | Automated command | File exists? |
|--------|----------|-----------|-------------------|-------------|
| FEAS-01 | Scorecard strict-load, unknown key rejected, SHA-256 stable, thresholds equal the pre-registered golden values (tiers, 0.01/0.10, caps, 25%/75%, 10%, 5%, L-BFGS block, grid, cadence 100) | unit | `... unittest tests.phase59.test_scorecard -v` | Wave 0 |
| FEAS-01 | Reference against itself: `E = 0`, `h = 1`, `ε_H` equals the reference's own analytic value | unit | `... tests.phase59.test_scorer_known_errors.SelfTests` | Wave 0 |
| FEAS-01 | Constant offset gives `e_sys` exactly the imposed fraction and `e_in = 0`; time shift on the rigid-rotation fixture gives `2 sin(ωΔ/2)` | unit | `... .OffsetShiftTests` | Wave 0 |
| FEAS-01 | Velocity scaling gives the analytic `ε_H` on a time-varying-kinetic-energy (eccentric Kepler) fixture; a guard test shows the rigid-rotation fixture is vacuous | unit | `... .VelocityScalingTests` | Wave 0 |
| FEAS-01 | Inner-pair-only phase error: `e_in = 2 sin(φ/2)`, small `e_sys` | unit | `... .InnerPairPhaseTests` | Wave 0 |
| FEAS-01 | Frame invariance (raw versus scaled dual-frame fixture): equal scores and `ε_H` to 1e-9 | unit | `... .FrameInvarianceTests` | Wave 0 |
| FEAS-01 | Pair tracking through synthetic permutations `(2,0,1)` and `(0,2,1)`; real corpus: closest pair equals tracked pair on all 2,039 Stage-0 train and validation systems | unit + evidence | `... .PairTrackingTests`; `verify_phase59_evidence.py pair-tracking` | Wave 0 |
| FEAS-01 | Tier table with boundaries, counting rule, decision rule (2 of 3, 12 of 16, branch a), budget rule (still-improving, doubling, inconclusive) on synthetic curves | unit | `... tests.phase59.test_scorecard_rules` | Wave 0 |
| FEAS-01 | The scorer never uses the finite-difference gate path | static | `... tests.phase59.test_static_guards.ScorerVelocitySourceTests` | Wave 0 |
| FEAS-01 | Scorecard committed before any census, baseline or survey evidence (SCOPE-42) | procedural | `verify_phase59_evidence.py scorecard-frozen` | Wave 0 |
| FEAS-02 | `N_in` on synthetic orbits of known revolutions, including an aliased case where plain unwrap is wrong and the dense estimator is right; fractional `N_out` | unit | `... tests.phase59.test_census` | Wave 0 |
| FEAS-02 | Panel rule determinism: percentile method, tie to lowest ID, 16 bins of 114/113, exclusion of the singles, validation panel of 227 | unit | `... tests.phase59.test_census.PanelRuleTests` | Wave 0 |
| FEAS-02 | Census CSV re-derives byte-identically; panels carry the rule hash and the census hash | evidence | `... stage0_census --check`; `verify_phase59_evidence.py census` | Wave 0 |
| FEAS-07 | Kepler propagator against RK4 at several eccentricities; `t = 0` identity; unbound gives `NotApplicable`; COM-frame rebuild conserves momentum | unit | `... tests.phase59.test_two_kepler` | Wave 0 |
| FEAS-07 | Nearest-neighbour copy: candidate set is the Stage-0 train pool only, ties to lowest ID, a validation system never matches itself, deterministic | unit | `... tests.phase59.test_nn_copy` | Wave 0 |
| FEAS-07 | Baseline outputs re-derive; only train and validation files opened | evidence | `... baselines --check`; `verify_phase59_evidence.py baselines` | Wave 0 |
| FEAS-08 | Stage predicates and precedence on synthetic records; Stage 0/1 read from the manifest; Stage 3 empty case; Stage 6 residual | unit | `... tests.phase59.test_survey` | Wave 0 |
| FEAS-08 | Vectorized `τ_L` equals the literal loop transcription on a short synthetic series; degenerate curves return a reasoned `not computable`, never a crash | unit | `... tests.phase59.test_survey.TauLTests` | Wave 0 |
| FEAS-08 | FEAS-09 pick rule (median, lowest ID), and the empty-stage record | unit | `... tests.phase59.test_survey.PickRuleTests` | Wave 0 |
| FEAS-08 | Survey is non-gating: nothing under `pinn/training` or `pinn/train.py` imports it | static | `... tests.phase59.test_static_guards.SurveyNonGatingTests` | Wave 0 |
| DIAG-07 | Checkpoint registry: step mapping asserted (`best.pt` is 900), SHA-256 equals the committed retention manifest, `weights_only=True` | unit + evidence | `... tests.phase59.test_diag07.RegistryTests`; `verify_phase59_evidence.py diag07` | Wave 0 |
| DIAG-07 | Share formula on a toy two-parameter case with a known answer; per-term gradient vectors against finite differences on `make_stub_model`; microbatched equals unchunked within 1e-6 | unit | `... tests.phase59.test_diag07.GradientDecompositionTests` | Wave 0 |
| DIAG-07 | G1 function at the `10⁻²` boundary | unit | `... .GateG1Tests` | Wave 0 |
| DIAG-07 | Driver leaves model parameters bitwise unchanged, constructs no optimizer, refuses checkpoint saves, leaves `runs/` hashes unchanged; code-root identity proof recorded | unit + evidence | `... .NonInterferenceTests`; `verify_phase59_evidence.py guardrails` | Wave 0 |
| D-26 | Refusal before any open; refusal precedes missing-root IO error; manifest hash mismatch rejected; audit hook records and blocks a withheld filename; no module other than `split_allowlist.py` names a corpus folder | unit + static | `... tests.phase59.test_split_allowlist`; `tests.phase39.test_prohibitions` | Wave 0 |
| D-27 | AST scan: no `optim`, `Optimizer`, `save`, `save_checkpoint` in Phase-59 modules; no import of `pinn.evaluate`; subprocess import check | static | `... tests.phase59.test_static_guards` | Wave 0 |
| D-28 | Phase-59 modules import only stdlib, numpy, torch, yaml and `pinn.*` (no scipy, pandas, sklearn, pytest) | static | `... tests.phase59.test_static_guards.ImportSurfaceTests` | Wave 0 |

### Sampling Rate

- **Per task commit:** the task's own test module (a few seconds, dataset-free) plus `tests.phase39.test_prohibitions`.
- **Per wave merge:** the full `tests/phase59` discovery plus the adjacent regression (about 5 s).
- **Phase gate:** full suite green, every `--check` re-derivation green, and `verify_phase59_evidence.py final` green before `/gsd-verify-work`. The DIAG-07 results are not re-run by the verifier (hours); it checks their retained JSON against the committed manifest hashes.
- **Plan-gate note:** project memory records that a plan-checker "VERIFICATION PASSED" has missed residual instances of its own blocker, and that the decision-coverage parser breaks on a decision bullet with no `:` or ` — ` right after its bold label. Grep the plans for each `D-NN` and for the sibling-plan uniformity of every guard before accepting the gate.

### Wave 0 Gaps

- [ ] `tests/phase59/__init__.py` and `_fixtures.py` (Lagrange and eccentric-Kepler closed-form fixtures, `TinyCorpus` helpers, a synthetic manifest builder)
- [ ] `tests/phase59/test_split_allowlist.py`, `test_static_guards.py`, `test_scorecard.py`, `test_scorecard_rules.py`, `test_scorer_known_errors.py`, `test_two_kepler.py`, `test_nn_copy.py`, `test_census.py`, `test_survey.py`, `test_diag07.py`
- [ ] `ALLOWED_CORPUS_READERS` extended in `tests/phase39/test_prohibitions.py` (one module, with a comment)
- [ ] `evidence/verify_phase59_evidence.py` skeleton with the subcommands above
- [ ] Framework install: none

## Security Domain

> `security_enforcement` is absent from `.planning/config.json`, so this section applies.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | — |
| V3 Session Management | no | — |
| V4 Access Control | yes (data access) | Allowlist of train and validation physical keys, refusal before any path is built, audit hook |
| V5 Input Validation | yes | Strict manifest loader (`SplitManifest.from_dict`), filename grammar and containment (`_BRUTUS_NAME_RE`, `resolve_within_root`), strict scorecard loader |
| V6 Cryptography | no (integrity only) | `hashlib.sha256` over file bytes; no custom crypto |
| V12 Files and Resources | yes | Read-only corpus; evidence never under `simulation_data/`; atomic writes; `torch.load(weights_only=True)` for untrusted-by-default pickles |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard mitigation |
|---------|--------|---------------------|
| Accidental read of a test-split file (the one real threat) | Information disclosure / Tampering with the held-out boundary | `SplitAllowlist.require` before path construction, audit hook with a blocking mode for withheld names, recorded `files_opened` summary with `test_split_opened: 0` |
| Pickle code execution through a checkpoint | Elevation of privilege | `weights_only=True`; SHA-256 equality with the committed retention manifest before loading |
| Silent write to `runs/` or a checkpoint (training side effect) | Tampering | Refusing checkpoint store, AST scan, before and after hash manifest of `runs/` |
| Absolute home path or data root leaking into committed evidence | Information disclosure | Record a `data_root_source` label, as the adapter's redaction does (`adapter.py:1004-1040`) |
| Held-out evaluator pulled in transitively | Tampering | AST and fresh-subprocess checks that `pinn.evaluate` is not imported (SCOPE-40) |
| Threshold edited after results are seen (SCOPE-42) | Repudiation | Scorecard hash in committed state; ancestor-commit check |

## Sources

### Primary (HIGH confidence)
- Repository files read this session (line ranges quoted above): `.planning/phases/59-.../59-CONTEXT.md`, `.planning/REQUIREMENTS.md` (FEAS-01..10, DIAG-07/08, INST-05, SCOPE-39..44), `.planning/ROADMAP.md` (Phase 59 section), `.planning/STATE.md`, `docs/work/designs/cross_cutting/v2.4-milestone-proposal/{2026-10-09-v2.4-roadmap-proposal.md, 2026-10-11-v2.4-feasibility-amendments.md}`, `pinn/data/{adapter,preprocessing,splits,stages,types,admission,batches}.py`, `pinn/verification/{gate_metrics,fixture_loader,overfit_probe,target_frame_probe,phase57_production_conformance}.py`, `pinn/training/{validation_gate,controllers}.py`, `pinn/{network,physics_residual,runtime,constants,train}.py`, `ctl_instruction.md` (:138-264, :326-347, :565-579, :994-1001, :1294-1435, :1600-1665, :1897-1917), `pinn_architecture.md` (:176-185, :450-456), `sampling_method.md` (:1-64), `trainex-r4-ruling.md` and `trainex-r4-resolution-doc.md` (:628-674), the Phase-57 `57-CONTEXT.md`, `57-VALIDATION.md`, `57-RULING.md` and `evidence/` records, `tests/phase39/test_prohibitions.py`, `tests/phase46/{test_isolation,_fixtures}.py`.
- Runtime measurements this session: `runs/stage0-v23g7-seed42/*` (config, status, validation, logs, checkpoints), `runs/stage0-v23g7-smoke/checkpoints`, the train and validation corpus files through the allowlist.
- Context7 `/websites/pytorch_2_12` (`torch.load`, `weights_only`) and `/python/cpython/v3.11.14` (`open` audit event, audit hooks are not a sandbox).

### Secondary (MEDIUM confidence)
- Rosenstein, Collins and De Luca, "A practical method for calculating largest Lyapunov exponents from small data sets", Physica D 65:117-134 (1993), https://ui.adsabs.harvard.edu/abs/1993PhyD...65..117R
- Universal-variable Kepler propagation: https://orbital-mechanics.space/time-since-periapsis-and-keplers-equation/universal-variables.html and https://www.mathworks.com/help/aerotbx/ug/orbit-pop-algorithms.html
- Breen et al., arXiv:1910.07291, and arXiv:2607.23501 (cited by the amendment; not re-fetched).

### Tertiary (LOW confidence)
- The `τ_L` class fractions and the survey stage populations beyond Stage 0/1 (estimator-dependent, diagnostic).

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH, the environment is locked and every package was listed from the live env.
- Architecture: HIGH for the data, split and scorer design (each element reproduced a production quantity bitwise or to float32 rounding); MEDIUM for DIAG-07 execution, because no model forward pass was allowed here.
- Pitfalls: HIGH, each was observed this session.
- Stage survey and `τ_L`: MEDIUM, ambiguity is in the spec, not the code.

**Research date:** 2026-10-11
**Valid until:** 2026-11-10 (the repository facts are stable until `pinn/` or the corpus changes; re-run the byte-identity and hash checks if either does)
