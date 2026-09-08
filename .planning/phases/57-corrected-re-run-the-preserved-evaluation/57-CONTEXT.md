# Phase 57: Corrected Re-Run & the Preserved Evaluation - Context

**Gathered:** 2026-09-07
**Status:** Ready for planning — GAP-57-01 was resolved on 2026-09-07;
GAP-56-01, GAP-54-06, and owner checkpoints ③/④ were resolved by direct owner
instruction on 2026-09-08 and are recorded in `57-RULING.md`. Before any run,
the bounded implementation, separate production-path verification, and a new
complete GATE-04 PASS still must finish.

> **Discussion mode.** Serviced autonomously per owner instruction (2026-09-07):
> every gray area below is dispositioned with the best-reasoned option, grounded
> in `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `54-RULING.md`, the
> v2.2 Phase 50 CONTEXT (the direct analog), and the shipped `pinn/` operating
> surface. **The CLAUDE.md STOP protocol is NOT waived for this milestone**
> (v2.3 adjudication milestone; the autonomous best-judgment directive does not
> waive the semantic / cross-phase-reframing MUST-surface class). One decision —
> whether and how the amended (SPEC-01/SPEC-06) recipe is implemented in `pinn/`
> code so RUN-04 can run it — was a cross-phase-scope call fixed by no source and
> was surfaced as **GAP-57-01**, not invented. The owner resolved it on
> 2026-09-07 by selecting bounded Option A with separate pre-RUN-04
> verification. On 2026-09-08 the owner directly fixed GAP-56-01 and
> checkpoints ③/④; `57-RULING.md` supersedes the packet-only descriptions below
> where they conflict. Checkpoint ⑤ remains owner-only. Everything else below
> is a mechanical, operational, or sequencing call in the discuss-phase's lane.

<domain>
## Phase Boundary

Phase 57 owns **RUN-04, RUN-05, EVAL-02** — the corrected Stage-0 re-run and the
single preserved held-out evaluation. It is the second attempt at the run v2.2's
Phase 50 could not complete: v2.2 re-ran Stage-0 under the conformance-corrected
recipe and it HALTed at the invariant-B causal-front gate (step 501,
`front_idx = 0` for the full `N = 500` window) because the SIREN `ω₀ = 30`
second-derivative scale collided with the unnormalized `η_c = 1` causal-weight
calibration. v2.3 Phases 54–56 produced and landed the owner-ratified
recalibration (`A1 + B2 residual-wide + C1 + D3 + E1`) as a framework-spec
**contract amendment** and built GATE-04, the train-free gate that refuses a run
whose causal weighting is still saturated shut.

**What this phase delivers:**

- **RUN-04** — Stage-0 runs end-to-end under the SPEC-01/SPEC-06-corrected
  recipe, and invariant B records the causal front **actually advancing**
  (`front_idx` increasing within the owner-re-ratified window, not merely off
  the floor). Gated on GATE-04 passing to a **complete** verdict. Iteration is
  conformance-only (SCOPE-37).
- **RUN-05** — the three-seed band is re-established under the same corrected
  recipe, matching the v2.0/v2.2 protocol so the runs are comparable.
- **EVAL-02** — the **sole preserved held-out evaluation** (the one v2.2 never
  attempted — RUN-03/EVAL-01 preserved unspent by the 2026-08-17 owner
  decision) is spent **exactly once**, on the pre-registered spending seed,
  only after its three preconditions (the v2.2 EVAL-01 structure, adapted for
  the new recipe) are verified and recorded, and only after a dataset-free
  regression **and** a pre-invocation assertion prove the evaluator pairs
  canonical predicted `r′` with `u = t/T` (GAP-46-01's delegated ruling,
  2026-07-26).

**Owner checkpoints ③/④, discharged on 2026-09-08 before any run:**

- **Checkpoint ③** — `N = 500` is explicitly re-ratified; invariant B uses one
  frozen training-only monitor; and the L-BFGS samples and detached causal
  weights remain frozen for the entire L-BFGS segment.
- **Checkpoint ④** — seed 42 is pre-registered, with fallback order 41 then 43
  only for structural ineligibility. `57-RULING.md` is the timestamped record.

**Declared terminal state (carried explicitly — roadmap SC5, SCOPE-35/37):** if
GATE-04 refused the recalibration train-free, **or** RUN-04's causal front still
fails to advance under the ratified recipe, the evaluation is **not** spent — it
is preserved unspent, that fact is recorded, and the phase closes there rather
than iterating. SCOPE-37 forbids any further tuning without a new owner decision.

**Out of the phase (grounded boundaries, not gray areas):**

- **No re-tuning of any ratified value.** `η_c`, the `R̄` normalization / `R_ref`,
  `ω₀`, `N_t`/`n_col` are locked by `54-RULING.md`. Any pressure to change one
  against an observed run result routes to the owner as a **new** decision
  (SCOPE-37). Iteration inside the phase is conformance-only.
- **No Stage-1+ / PLAT-01..07 work.** SCOPE-36 — still blocked pending a `go`
  verdict at DIAG-06 (Phase 58). Enforced by the `--stage-0-only` switch.
- **No framework-spec edit.** SCOPE-33's spec-edit authorization was for the
  VER-20 items + the `n_col`/`N_t` disposition, all landed in Phases 53/56.
- **No second held-out evaluation.** SCOPE-35 — exactly one; any further
  evaluation requires a new owner decision.
- **No DIAG-06 verdict.** That is Phase 58, checkpoint ⑤.
- **No re-litigation** of the nine v2.2 conformance repairs (C-01..C-09), of
  DIAG-05, or of the `54-RULING.md` recalibration.

</domain>

<decisions>
## Implementation Decisions

### 1. The amended-recipe implementation — GAP-57-01 (✅ LOCKED: owner Option A)

- **D-01: Phase 57 owns a bounded amended-recipe conformance patch as an explicit
  first implementation wave, followed by separate verification before RUN-04.**
  Owner instruction 2026-09-07 resolved GAP-57-01 with Option A. The ratified
  v2.3 roadmap proposal put implementation in its
  Phase D scope ("SPEC-01 + SPEC-06 amendment **and implementation**";
  `2026-08-17-v2.3-roadmap-proposal.md:267`), but the roadmap as ratified maps
  Phase 56 to `SPEC-01, SPEC-06, GATE-04` only, and Phase 56 executed the
  amendment **spec-only** — `pinn/train.py:1033` still reads
  `collocation_count = 16`, `pinn/loss_catalog.py::causal_physics_loss` still
  forms a raw per-point 16-term prefix over unnormalized `R̄`, there is no
  `R_ref` normalization of either the causal exponent or the outer physics loss,
  and `56-VERIFICATION.md` truth 3 confirms "no production file edited … the
  trainer rebuild is FUT-01." `.planning/PROJECT.md:344` corrects that shorthand:
  FUT-01 shipped in v2.0; only PLAT-01..07 / Stage-1+ remain deferred. This later
  owner instruction expressly supersedes Phase 56's deferral and
  `pinn_architecture.md:458`'s no-production-edit sentence **only for the bounded
  amended-recipe path**.

  Scope follows the behavior, not a closed file list. The patch reaches every
  necessary production call site in the causal loss, collocation sampler and
  allocation, controller, and config wiring. In particular, it replaces the
  current one-anchor physics execution with contributions from all selected
  slots and implements the exact §3.2 allocation, batch-global 16-bin prefix,
  frozen-`R_ref` exponent and residual-wide `L_phys` normalization,
  microbatch-preserved aggregates, gradients, and raw/normalized diagnostics.
  `pinn/loss_catalog.py` and `pinn/train.py` are examples, not a sufficient
  inventory. Focused tests and production-path verification are part of the
  authorization. Resource failure at 4096 rows fails closed rather than
  authorizing a reduced count.

  The boundary excludes retuning, architecture redesign, data-policy changes,
  Stage-1+, PLAT-01..07, and a new wholesale trainer rebuild. Any required
  expansion stops for a new owner decision.
  — **Reversibility:** the code change is `costly`; the scope ruling is one-way
  in effect because it sets what SCOPE-37 conformance means and what RUN-04 may
  test.

- **D-02: Implementation authorization is not run authorization.** The first
  wave implements the bounded path; a separate verification wave must prove the
  production training path's allocation, normalization, gradients, and
  diagnostics before RUN-04. The decision gates are now resolved in
  `57-RULING.md`, but RUN-04 remains blocked until their production wiring is
  verified and GATE-04 records a new complete PASS. Evaluator-pairing,
  evidence-contract, and operating-surface work may proceed in parallel with
  the bounded implementation and verification work.

### 2. Owner checkpoints ③ and ④ — ✅ LOCKED by `57-RULING.md`

- **D-03: Checkpoint ③ is discharged before any run.** `N = 500` is explicitly
  re-ratified for the amended recipe. Each run uses one frozen training-only
  monitoring context for invariant B; resampled training-batch fronts remain
  diagnostic-only. The existing front/high-water/window semantics continue
  without a new margin, cadence, or persistence threshold. For the full
  Stage-0 L-BFGS segment, freeze the segment's samples and detached causal
  weights at handoff; do not redraw or recompute them in line-search closures
  or between outer calls. Exact resume and provenance obligations are in
  `57-RULING.md`. This resolves inherited GAP-54-06.

- **D-04: Checkpoint ④ is discharged by timestamped pre-registration.** The
  spending seed is 42. Fallback order is 41 then 43, only for structural
  ineligibility and never for observed scientific metrics. The v2.2 Phase-50
  structural-eligibility and `best.pt` candidate structure carries forward,
  subject to Phase 57's stricter GATE-04, invariant-B, terminal-state, and
  canonical-frame preconditions. If the terminal branch fires or no eligible
  candidate exists, the evaluation remains unspent. `57-RULING.md` and its
  commit ancestry are the pre-run registration.

- **D-05: The GATE-04 precondition must be a *complete* PASS — GAP-56-01 is
  resolved, but production wiring and a fresh gate run remain.** Phase 56
  shipped GATE-04 with conditions
  (i) and (iii) wired and condition (ii) — "a weight vector carrying
  differential information (not all-floor, not degenerate)" and the re-issued
  AC's "a front that cannot respond to controlled residual reduction" — as a
  **structurally-present, never-satisfiable slot** (`condition_ii_verdict`
  raises `NotImplementedError`; every verdict carries
  `unratified_conditions = ("ii",)` and prints `INCOMPLETE`). The owner now
  requires a `2:1` non-anchor spread and the fixed all-residual reduction from
  `57-RULING.md`, ending at expected `w'_15 = 1/sqrt(2)`, with
  `front_idx = 15` and every perturbed weight `>= 0.70`. RUN-04 may not spend a
  run until this is implemented and GATE-04 is re-run to a complete PASS. Two
  structural findings from `56-OPEN-ITEMS.md` §2 that the owner's condition-(ii)
  ruling MUST account for: (1) `front_idx = 0` at initialization is the
  **expected healthy** result under the amended recipe (each case's `w_2` is
  already below the half-threshold), so a fixed positive-front check rejects
  every healthy case; (2) a residual reduction confined to late bins cannot move
  `front_idx` at any magnitude (exclusive-prefix structure), so a
  controlled-reduction test that perturbs only late bins reports a
  non-response that says nothing about recipe health. The owner's all-bin
  reduction respects both findings.

### 3. RUN-05 — the three-seed band, budget, and comparability

- **D-06: The band is seeds 41 / 42 / 43, matching the v2.0/v2.2 protocol.**
  RUN-05's comparability requirement is at the **protocol layer, not
  byte-identity of config** (v2.2 Phase 50 D-02): same seeds, same admitted
  corpus, same environment, same artifact set; the three graded configs differ
  only in `run.seed` / `run.run_name`. Grounding: the v2.0 pilot and v2.2 Phase
  50 both used 41/42/43; DIAG re-derivation and the v2.0 `ε_H = 237.2086`
  baseline are per-seed-42 held-out population.

- **D-07: Budget is the shipped Stage-0 config — `stage.max_epochs = 1000`,
  `stage.n_adam = 1000` — NOT the v2.0 300-step smoke** (v2.2 Phase 50 D-01,
  three-fold grounding carried forward): (a) invariant-B `N` was ratified
  *explicitly as `0.5 · N_Adam,0`* against `N_Adam,0 = 1000` — a shorter budget
  makes the window arithmetically unreachable and converts a ratified gate into
  decoration; (b) the v2.0 pilot config carries `run.smoke: true` — it is the
  ACC-02 mechanical smoke budget; (c) `ctl_instruction.md` marks `MAX_EPOCHS`
  etc. "provisional pending FUT Stage-0 pilot calibration (SCOPE-14)" — it
  assigns the value to the calibrated artifact, and `configs/stage0-example.yaml`
  is that artifact. **Not SCOPE-37 tuning** — 1000 was committed long before any
  conformant number existed, and checkpoint ③ now explicitly re-ratifies
  `N = 500` against that budget.

- **D-08: The graded configs are derived from the existing
  `configs/stage0-rerun-seed4{1,2,3}.yaml`** (tracked; built in v2.2 Phase 50
  plan 50-01, `abd5f8d9`), updated **only** for: the re-ratified `N` and its
  provenance (checkpoint ③); what the resolved Option-A amended-recipe
  implementation requires (collocation count, `R_ref` path, normalization flags);
  and distinct run names that do **not** collide with the v2.2
  `stage0-rerun-seed4X` artifacts (preserve the v2.2 HALT record intact — use a
  v2.3-distinct name, e.g. `stage0-v23-seed4X`). No other change. The
  `stage0-rerun-smoke.yaml` is the calibration-smoke base (D-09).

### 4. First contact — the calibration smoke is a hard precondition

- **D-09: The phase opens with a calibration smoke on the final code state, and
  the plan's wave decomposition MUST honour "no commit between the smoke and the
  graded runs."** `_check_duration_gate` (`pinn/train.py`) refuses any non-smoke
  launch without a valid persisted timing calibration
  (`runs/.calibration/stage0-timing.json`) matching the launch's **full**
  fingerprint — device, dtype, torch version, python version, **and `git_head`**
  (`git rev-parse HEAD`). The Option-A amended-recipe implementation commit
  changes `git_head`, so the persisted v2.0-era calibration cannot match and a
  fresh smoke is mandatory. The amended recipe's larger collocation count
  (`n_col` 16 → 4096) also changes per-step wall time
  materially, so the calibration must be measured on the amended recipe, not
  assumed. **A commit landing between the smoke and any graded launch
  invalidates the calibration** (project memory
  `reference-train-duration-gate-git-head.md`) — the plan sequences the amended
  code commit, then the smoke, then all three graded runs, then EVAL-02, with no
  intervening commit; per-plan GSD commit cadence is adapted accordingly.

- **D-10: The smoke is also the amended recipe's first real-corpus contact and
  the `S_H` cross-check** (v2.2 Phase 50 D-14/D-16). Run the smoke at **seed 42**;
  the seed-42 smoke and the seed-42 graded run must produce byte-identical
  `splits.json` and then **exactly equal** `s_h` / `n_train` — asserted as phase
  evidence. A mismatch is a defect to route as a gap, never a number to accept.
  The smoke carries the re-ratified `front_advance_window_n` (checkpoint ③),
  copied not chosen, so first contact walks the identical preflight path the
  graded runs will (`REQUIRED_RUN_START_CHECKS` `invariant_b_window`).

- **D-11: Reuse the `--stage-0-only` switch** (`pinn/train.py:214`,
  `pinn/training/controllers.py:1670` — shipped in v2.2 Phase 50). It is a
  fresh-run-only guard (invalid with `--resume`) that returns success after a
  Stage-0 `ADVANCE` before incrementing the stage / invoking `stage_factory` /
  writing `stage-1-init`. This is the mechanism that enforces SCOPE-36; every
  graded run and the smoke pass it. Re-verify it behaves correctly against the
  amended code state.

### 5. EVAL-02 — evaluator assembly, the pairing proof, and the three preconditions

- **D-12: The GAP-46-01 obligation is a hard gate before EVAL-02 and is
  RUN-04-mapped, not a fourth eligibility precondition.** GAP-46-01 (delegated
  ruling 2026-07-26, refined option A): EVAL-02 is for the **corrected
  conformant model**, so the held-out evaluator must pair **canonical predicted
  `r′` with `u = t/T`**. Phase 57 must add (a) a **dataset-free assembly
  regression** — proves, with no held-out access, that the evaluator's
  prediction/target pairing is the canonical `(r′, u = t/T)` contract
  (CONF-09's `RATIFIED_VALIDATION_FRAME` re-ratified 2026-07-31) — and (b) a
  **pre-access assertion** in the EVAL-02 invocation path that fails closed
  before any `test`-split materialization if the pairing is wrong. A raw-target
  CONF-01 verdict "diagnoses the historical path but does not authorize a
  raw-frame EVAL-01 run" — EVAL-02 is canonical-frame only.

- **D-13: `pinn/evaluate.py` must be characterized against the canonical
  contract before it is trusted.** It is **Phase 43 vintage** (pre-CONF-09):
  it reconstructs the persisted held-out `test` split from a checkpoint's owning
  run (frozen `config.yaml` + `splits.json`), runs one forward pass under
  `.eval()` + `torch.no_grad()`, and renders `pinn.verification.gate_metrics`
  (the post-v1.3 binary gate — worst-case-max aggregate per SPEC-05) to
  `metrics.json` + `evaluation-receipt.json`. It uses the
  `tau = 2·(t/T) − 1` map (`pinn/evaluate.py:267`). The researcher confirms
  whether its prediction frame is the CONF-09 canonical residency and whether
  its target construction matches — **if it does not, its bounded fix is
  governed separately by D-12 / GAP-46-01, not by the causal-path authorization
  in resolved GAP-57-01.** Note this independent Phase-57 code path.

- **D-14: The EVAL-02 three preconditions are the v2.2 EVAL-01 structure,
  adapted (roadmap SC5; v2.2 `REQUIREMENTS.md` "Evaluation Policy"):**
  (i) **preflight conformance passes with zero unwaived divergences** — for
  v2.3 this **includes** a complete GATE-04 PASS (D-05) on the amended recipe;
  (ii) **the frame question is resolved** — for v2.3 this is CONF-09's canonical
  `(r′, u = t/T)` contract, with the GAP-46-01 pairing proof (D-12) as its
  evidence (the v2.2 CONF-01 / RG-02 operational raw/native frame was for the
  historical diagnosis and does **not** carry into an EVAL-02 run); (iii)
  **validation-side gate metrics are recorded** for the run being submitted.
  No evaluation may be spent on a run that has not passed (i)–(iii). Phase 57 is
  the **verifier** of the three preconditions; it re-checks them immediately
  before the single invocation.

- **D-15: The single invocation is exactly once, on the pre-registered seed's
  run, on `checkpoints/best.pt`.** `pinn/evaluate.py`'s attempt/receipt
  single-use claim is per owning run; the phase does not invoke it twice, does
  not re-run on a fallback seed after a value is seen, and does not evaluate any
  run other than the pre-registered one unless that run is **structurally
  ineligible** (D-04 fallback).

### 6. Conformance-only iteration (SCOPE-37) operationalized

- **D-16: A change made during Phase 57 is "conformance-only" iff its
  justification does NOT cite what a run produced.** (v2.2 Phase 50 iteration
  policy, adapted from SCOPE-29 to SCOPE-37.) Fixing a code/spec mismatch
  against the amended `pinn_architecture.md` §3.2, a preflight-divergence repair,
  or an environment fix is conformance. Adjusting `η_c`, the `R_ref` /
  normalization, `ω₀`, `N_t`/`n_col`, the LR schedule, the loss weights, or the
  budget **because a run looked bad** is SCOPE-37-forbidden and routes to the
  owner as a new decision. An honest invariant-B HALT is a **deliverable**, not
  a failure to fix — the failure mode to guard against is an agent quietly
  raising `N` and reporting a clean run.

### 7. Execution environment

- **D-17: Phase 57 runs inline on the data-bearing checkout — not via
  worktree-isolated `gsd-executor` subagents.** (Project memory
  `project-trainex-gitignored-data-inline-execution.md`: phases reading
  gitignored `runs/` / `brutus_output/` / `ic_final/` cannot use fresh
  worktrees — they lack the data; STOP-protocol phases also favour inline so the
  parent owns gaps.) `config.json` already has `use_worktrees: false`.

- **D-18: The training environment is the `pinn-train` conda env, invoked
  off-PATH** (project memory `project-pinn-train-conda-env.md`):
  `<home>/miniforge3/bin/conda run -n pinn-train ...`. The env has
  **no pytest** — the dataset-free regression (D-12) and any GATE-04 re-run must
  be runnable under `unittest`; do **not** install pytest during the run band
  (it perturbs the env fingerprint the duration gate pins).

- **D-19: The admitted-corpus data root is a run precondition the plan
  resolves.** `pinn/data/adapter.py` (`default_data_root` / `DATA_ROOT_ENV` /
  `ALLOW_PARTIAL_ENV`, `DataSourceRootMissing` / `DataSourceRootIncomplete`)
  resolves the `simulation_data/` admitted set. Worktrees may lack the full
  gitignored payload (project memory `project-dataset-payload-master-root-only.md`)
  — the plan confirms the full admitted corpus is reachable (env var or
  location) before the smoke, and the partial-copy guard is respected.

### 8. Evidence contract

- **D-20: Carry the v2.2 Phase 50 evidence contract forward** (format is
  Claude's discretion, following the established layout): a **run ledger**, a
  **band record** (per-seed validation `ε_H` distribution, quantiles), the
  **pre-registration record** (D-04), a **config-delta record** proving the band
  varied only `seed` / `run_name` (v2.2 D-04 — do not assert "the band varied
  only the seed" without diffing the configs), the **checkpoint-③/④ packets and
  their discharge records**, the **GATE-04 complete-PASS evidence** on the
  amended recipe, the **GAP-46-01 pairing-proof artifacts**, and `sha256`
  manifests for every extracted artifact. Two "checks that cannot fail" are
  forbidden by the Phase-49 lesson and must be real: asserting "no evaluation
  was spent" without checking for the `evaluation/` directory, and asserting
  "the band varied only the seed" without diffing the configs.

### Claude's Discretion

The planner and executor own, without re-opening anything above: the wave
decomposition and how D-09's no-commit-mid-band constraint is expressed in it;
whether the smoke and the band extraction are one plan or several; attended
(`python -m pinn.train`) versus unattended (`scripts/train-unattended.sh`)
launch; the file format and layout of the run ledger, band record,
pre-registration record, config-delta record, and evidence manifests; which
quantiles the band distribution reports; the exact v2.3-distinct run names
(only locked property: distinct from the v2.2 `stage0-rerun-seed4X` names);
the dataset-free regression test's exact shape (only locked properties: no
held-out access, runnable under `unittest`, committed); and the placement of
evidence directories under `.planning/phases/57-*/evidence/<category>/<timestamp>/`.
Those choices must preserve every decision above, add no dependency, introduce
no new threshold or selection rule, and change nothing that enters a loss term,
an optimizer, the data path, or a gate beyond resolved GAP-57-01 and the other
explicitly grounded Phase-57 obligations.

### Owner-Routed Decisions (STOP protocol — not invented)

Full records in `57-GAPS.md` and `.planning/milestones/v2.3-GAPS.md`.

- **GAP-57-01 (HIGH) — RESOLVED-WITH-INSTRUCTION, owner Option A
  (2026-09-07).** Phase 57 owns the bounded amended-recipe conformance patch and
  a separate production-path verification step before RUN-04. The functional
  boundary includes the causal loss, all-selected-slot collocation allocation,
  sampler/controller/config wiring, exact §3.2 normalization and diagnostics,
  and focused tests; it is not limited to two named files. It excludes retuning,
  redesign, data-policy changes, Stage-1+, PLAT-01..07, and a wholesale rebuild.
  A 4096-row resource failure fails closed. This later instruction supersedes
  the earlier implementation deferral for this bounded path only. FUT-01 itself
  shipped in v2.0 (`PROJECT.md:344`). The resolution does not discharge any
  remaining owner gate below.

- **Checkpoint ③ — RESOLVED-WITH-INSTRUCTION (2026-09-08).** Explicitly
  re-ratify `N = 500`; use one frozen training-only invariant-B monitor; freeze
  L-BFGS samples and detached causal weights for the entire segment. This also
  resolves inherited GAP-54-06. Exact record: `57-RULING.md`.

- **Checkpoint ④ — RESOLVED-WITH-INSTRUCTION (2026-09-08).** Seed 42 is
  pre-registered, with fallback 41 then 43 only for structural ineligibility.
  Exact timestamped record: `57-RULING.md`.

- **GAP-56-01 — RESOLVED-WITH-INSTRUCTION (2026-09-08).** Require a `2:1`
  spread among non-anchor weights, then the fixed all-residual reduction from
  `57-RULING.md`; require `front_idx = 15` and all perturbed weights `>= 0.70`.
  Implementation and a new complete GATE-04 PASS still block RUN-04.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope, owner checkpoints, and the terminal state
- `.planning/ROADMAP.md` "Phase 57: Corrected Re-Run & the Preserved Evaluation"
  — goal, dependency (Phase 56 GATE-04), the 5 success criteria, and the
  "Adjudication discipline" block (owner checkpoints ③–⑤, the declared terminal
  state, the gap-discipline rule).
- `.planning/REQUIREMENTS.md` — RUN-04, RUN-05, EVAL-02 (verbatim); SCOPE-35
  (single held-out evaluation), SCOPE-36 (Stage-0 only), SCOPE-37 (post-edit
  iteration is conformance-only), SCOPE-38 (amend-a-locked-contract discipline);
  "Owner Checkpoints" 3 & 4; "Declared Terminal State".
- `.planning/milestones/v2.3-GAPS.md` — GAP-54-06 and GAP-56-01
  (RESOLVED-WITH-INSTRUCTION 2026-09-08), and GAP-57-01
  (RESOLVED-WITH-INSTRUCTION, owner Option A).
- `docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md`
  — the ratified proposal; **line 267** ("Phase D: SPEC-01 + SPEC-06 amendment
  **and implementation**; GATE-04") is the source of the GAP-57-01
  proposal-vs-executed discrepancy.

### The ratified recalibration and its downstream boundaries
- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` — read in
  full: the checkpoint-② ruling (`A1 + B2 residual-wide + C1 + D3 + E1`), the
  "Checkpoint ② discharge — scientific basis" section, the **"Optimizer-phase
  boundary — explicitly deferred"** paragraph (GAP-54-06), the **"Front-monitoring
  boundary"** paragraph (checkpoint ③'s fixed-monitor requirement), the "Batch
  allocation and bin policy" section, and the four SCOPE-38 re-ratification
  blocks.
- `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md`
  — the later governing record for resolved GAP-56-01, checkpoint ③/GAP-54-06,
  and checkpoint ④; where it conflicts with an earlier deferral, it controls.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §3.2 — the **amended** causal-weight / collocation / `R_ref` contract Phase 56
  landed (Block 1 causal exponent, Block 4 collocation allocation, the frozen
  `R_ref` definition + invalidation-trigger list, the re-issued AC-LOSS-04).
  This is the spec of record the RUN-04 implementation must honour. Anchors are
  line-drifted — re-derive by content.
- `.planning/phases/56-contract-amendment-train-free-gate/56-CONTEXT.md` and
  `56-OPEN-ITEMS.md` — D-01/D-02/D-03 (the amendment is transcription; `pinn/`
  is not edited; the trainer rebuild is FUT-01); `56-OPEN-ITEMS.md` §1
  (GAP-56-01 slot), §2 (the two `front_idx` structural findings the owner's
  condition-(ii) ruling accounts for), §3 (GAP-56-02).
- `.planning/phases/56-contract-amendment-train-free-gate/56-VERIFICATION.md`
  truth 3 — "no production file edited"; `pinn/train.py:1033` still
  `collocation_count = 16`.

### The direct analog — v2.2's Stage-0 re-run
- `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-CONTEXT.md` —
  **the pattern this phase adapts**: D-01 (budget = shipped config, not the
  smoke), D-02 (comparability = protocol layer), D-04 (config-delta discipline),
  D-07..D-12 (the pre-registration structure, seed-dependent split, ineligibility
  -only fallback, no-eligible-seed → owner), D-13..D-17 (the calibration smoke as
  a hard precondition, `S_H` cross-check, no-commit-mid-band), the iteration
  policy, the evidence contract, and the "Specific Ideas" (one-job-one-temptation,
  pre-registration expires, honest HALT is a deliverable, checks that cannot
  fail).
- `.planning/milestones/v2.2-REQUIREMENTS.md` "Evaluation Policy" — the EVAL-01
  three preconditions (i)–(iii) verbatim, and the "corrected implementation is a
  new question, not a re-run" clarification.
- `.planning/milestones/v2.2-GAPS.md` — GAP-46-01 (the evaluator-pairing
  obligation: canonical `r′` ↔ `u = t/T`, dataset-free assembly regression +
  pre-access assertion), GAP-46-06 (the CONF-01 qualification), GAP-50-01..03
  (the v2.2 band's DATA-06 / invariant-B HALT history), and "Milestone close".
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`
  — §6a/§6b/§6c: the retained seed-41 HALT log, the six-row initialization
  table, the mechanism narrative.

### Frame / residency contracts EVAL-02 depends on
- `.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md` — CONF-09's
  `RATIFIED_VALIDATION_FRAME = (r_prime, u_t_over_T, ordered_raw)`, re-ratified
  2026-07-31; the `S_H` / `ε_H` pipeline.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  §10.6 (SPEC-05, worst-case-max aggregate), §3.1 (SPEC-04, `L_data` reduction),
  `:567` (`ε_H` within-trajectory reduction).

### Operating surface (modify only within resolved decisions)
- `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md` — the
  five entry points (Setup / Configure / Launch / Monitor / Resume), the error
  surface table, the M5-Pro notes.
- `configs/stage0-example.yaml` (the shipped recipe: R-1, R-2, D4-a,
  `front_advance_window_n: 500`), `configs/stage0-rerun-seed4{1,2,3}.yaml` +
  `configs/stage0-rerun-smoke.yaml` (the v2.2 Phase 50 band configs — the
  derivation base per D-08), `configs/smoke.yaml`.
- `pinn/train.py` — `_check_duration_gate` (the `git_head`-pinned calibration
  refusal), `--stage-0-only` (`:214`), `collocation_count = 16` (`:1033`, the
  GAP-57-01 site).
- `pinn/loss_catalog.py` — `causal_physics_loss(..., return_details=True)`,
  `resolve_causal_clip_facts`; the raw per-point prefix that the amended recipe
  restructures (GAP-57-01).
- `pinn/verification/gate04_train_free.py` — GATE-04; `condition_ii_verdict`
  (the GAP-56-01 slot), `condition_iii_diagnostics`, `Gate04Verdict`.
- `pinn/verification/architecture_characterization_probe.py` — the INST-04
  probe + `ratified_causal_weights` / `stratified_collocation_times` /
  `bin_mean_residuals` helpers (the *specified* recipe arithmetic, as a
  reference for the RUN-04 implementation).
- `pinn/verification/artifacts/r_ref_stage0.json` — the frozen `R_ref` (written
  by Phase 56 GATE-04); the amended recipe consumes this value.
- `pinn/evaluate.py` — the EVAL-02 entry point (`--checkpoint`, `--output`
  canonical-`evaluation/` guard, `tau = 2·(t/T) − 1` at `:267`); Phase-43
  vintage, characterize against CONF-09 (D-13).
- `pinn/data/splits.py` (`_partition_by_signature`, `SplitManifest`),
  `pinn/data/adapter.py` (`default_data_root`, `DATA_ROOT_ENV`),
  `pinn/training/run_metadata.py` (`compute_s_h` / `validate_s_h`),
  `pinn/training/controllers.py` (invariant-B state, `front_idx`, `stage_0_only`),
  `pinn/training/{guards,checkpoint,summary}.py`,
  `pinn/conformance/{preflight,census,table,register}.py` +
  `divergence_register.json` (the gate RUN-04 runs against real data;
  `evaluate_eval01_precondition_i`).

### Governance
- `.worktrees/trainex/CLAUDE.md` "CRITICAL GOVERNANCE" — the STOP protocol
  (v2.3 applicability), the git branch-awareness / destructive-op / commit
  protocol, the docs placement rules.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`configs/stage0-rerun-seed4{1,2,3}.yaml` + `stage0-rerun-smoke.yaml`** —
  the v2.2 Phase 50 band configs (tracked, `abd5f8d9`). Copied verbatim from
  `stage0-example.yaml`; the D-08 derivation base. Update only for the
  re-ratified `N`, the GAP-57-01 recipe requirements, and v2.3-distinct run
  names.
- **`--stage-0-only` switch** (`pinn/train.py:214`,
  `pinn/training/controllers.py:1670`) — shipped in v2.2 Phase 50; the SCOPE-36
  enforcement mechanism. Fresh-run-only (rejects `--resume`).
- **`_check_duration_gate`** (`pinn/train.py`) + `runs/.calibration/stage0-timing.json`
  — the `git_head`-pinned calibration refusal; forces the D-09 calibration smoke.
- **`pinn/evaluate.py`** — the one-time held-out gate: split reconstruction from
  the owning run, single `.eval()` forward pass, `gate_metrics` render,
  attempt/receipt single-use claim. Phase-43 vintage — needs D-13 characterization.
- **`pinn/verification/gate04_train_free.py`** — GATE-04; RUN-04 imports and
  calls it as a hard precondition (`56-CONTEXT.md` integration point). Its
  verdict must be a **complete** PASS (not `INCOMPLETE`).
- **`pinn/verification/architecture_characterization_probe.py`** — the
  INST-04 probe and the `ratified_causal_weights` / `stratified_collocation_times`
  / `bin_mean_residuals` / `RATIFIED_N_BINS` helpers: the specified recipe
  arithmetic, available as a reference implementation for the GAP-57-01 patch.
- **`pinn/verification/artifacts/r_ref_stage0.json`** — the frozen `R_ref`
  (Phase 56 GATE-04 authoritative run, `20260907T033409Z`); the amended recipe
  reads it, never recomputes online.
- **The v2.2 Phase 50 evidence layout** (`.planning/milestones/v2.2-phases/50-*/evidence/{calibration,corpus,attempts,...}/`)
  — the D-20 evidence-contract pattern.

### Established Patterns
- **Pre-registration is the cheapest protection and it expires** — seed,
  checkpoint, and fallback order committed with a timestamp *before* the first
  graded run are a receipt; the same choices written after are a rationalization
  (the split is seed-dependent).
- **The calibration smoke is a discovered precondition of the shipped code**, not
  a discretionary de-risk step — every graded launch refuses without a matching
  persisted calibration, and any commit between smoke and graded run invalidates
  it.
- **An honest invariant-B HALT is a deliverable.** The failure mode to guard is
  an agent quietly raising `N` and reporting a clean run.
- **STOP protocol** — v2.3 adjudication milestone; any source-silent
  physics/spec/scope adjudication call is recorded in `57-GAPS.md` **and**
  `.planning/milestones/v2.3-GAPS.md` and routed to the owner, never decided
  inline. Subagents return findings; the parent decides gap status.
- **Inline execution** (`use_worktrees: false`), conda `pinn-train` off-PATH, no
  pytest in the env, per-phase test dirs (`tests/phase57/`), `agent-commit` with
  `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`, two-digit phase scope `57`.

### Integration Points
- **RUN-04 → `gate04_train_free`** — the import edge Phase 56 built to;
  precondition call before any launch, verdict must be complete PASS.
- **RUN-04 implementation → `pinn_architecture.md` §3.2** — the amended spec is
  the exact contract the bounded GAP-57-01 Option-A code change must honour;
  `57-GAPS.md` records the later owner authorization that supersedes §3.2's
  Phase-56 implementation deferral for this path.
- **EVAL-02 → `pinn/evaluate.py` → the pre-registered run's `checkpoints/best.pt`**
  — single invocation; the pre-access assertion (D-12) fires before any `test`
  split materialization.
- **Checkpoint-③ ruling → the run configs** — the re-ratified `N` and the
  fixed-monitor context enter `run.invariants` (and possibly a new monitor
  block); the GAP-54-06 ruling governs the L-BFGS closure path in
  `pinn/training/controllers.py`.
- **Phase 58 (DIAG-06)** consumes the band record, the EVAL-02 result (or the
  recorded terminal branch), and the checkpoint-③ provenance.

</code_context>

<specifics>
## Specific Ideas

- **The phase has one job and one temptation.** The job: produce a run that is
  the specified experiment under the ratified recipe, and — only if it trains —
  spend the one evaluation. The temptation: after the first number appears,
  adjust a ratified value. Every decision above is answerable to that — if a
  change's justification cites what a run produced, it is a new owner decision,
  not this phase's work (SCOPE-37).
- **This is v2.2's Phase 50 with a recipe that (should) train and an evaluation
  that (may) be spent.** The v2.2 phase HALTed before pre-registration mattered;
  this phase reaches the evaluation, so checkpoint ④ and the single-look
  discipline are load-bearing, not precautionary.
- **The declared terminal state is a clean close, not a failure.** GATE-04
  refusing, or the front still not advancing, routes straight to a
  `rethink`-flavoured DIAG-06 with the evaluation preserved unspent. Naming it
  up front (roadmap SC5) is what keeps that outcome from becoming a drift into
  an un-authorized tuning pass.
- **Two "checks that cannot fail" are forbidden by the Phase-49 lesson** and
  must be real here: asserting "no evaluation was spent" without checking for
  the `evaluation/` directory, and asserting "the band varied only the seed"
  without diffing the configs.

</specifics>

<deferred>
## Deferred Ideas

- **Any new wholesale trainer rebuild** — FUT-01 itself shipped in v2.0
  (`PROJECT.md:344`). GAP-57-01 authorizes only the bounded causal-loss and
  collocation-path conformance patch; it does not authorize rebuilding the
  package again.
- **Stage-1+ / PLAT-01..07 platform work** — SCOPE-36; re-opens only on a `go`
  verdict at DIAG-06 (Phase 58).
- **The DIAG-06 go / adjust / rethink verdict and VER-21 traceability close** —
  Phase 58, owner checkpoint ⑤.
- **Any second held-out evaluation** — SCOPE-35; requires a new owner decision.
- **Re-tuning `η_c` / `R_ref` / `ω₀` / `N_t` against an observed result** —
  SCOPE-37; a new owner decision, not Phase 57 work.

### Reviewed Todos (not folded)
- **d-06-static-epsilon-sensitivity-check** (score 0.6, keyword-only match) — a
  spec-side `epsilon_soft` dual-context sensitivity question with no VER-20
  routing; folding it would breach SCOPE-33's narrow spec-edit authorization
  (which in v2.3 is spent, Phases 53/56). Phases 55 and 56 both reviewed and did
  not fold it — same disposition. Remains in `.planning/todos/pending/`; revisit
  at milestone close.
- **trainex-r1-research-handoff** (the r1b tuning round, score 0.6,
  keyword-only) — unrelated to RUN/EVAL scope; not folded (same as Phases 55/56).

</deferred>

---

*Phase: 57-Corrected Re-Run & the Preserved Evaluation*
*Context gathered: 2026-09-07*
