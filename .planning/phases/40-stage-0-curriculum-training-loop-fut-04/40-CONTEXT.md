# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) - Context

**Gathered:** 2026-07-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 40 builds the **training driver layer** — the outer curriculum loop
(`CurriculumController`) and inner two-phase optimization loop
(`RunController`) that drive Stage 0 from the Phase-39 batches through the
Phase-38 model, transcribing the `ctl_instruction.md` Stage-0 contract into
runnable, numerically-checkable behavior. The model, loss catalog, and data
substrate all exist; no driver does. Phase 40 builds exactly that driver:
two-phase Adam→L-BFGS closure, PHYS-05 scheduled weights, collocation
sampler interface, merged gradient clipping, the ADVANCE/RECOVER/HALT
stage-exit machine, and the sL-BFGS preflight refusal.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**7 requirements are locked (TRAIN-01..07).** See `40-SPEC.md` for full
requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `40-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**
- `CurriculumController` / `RunController` driver pair (a training module under `pinn/`)
- Two-phase Adam→L-BFGS closure loop, Stage 0–2 full-batch path only
- PHYS-05 scheduled loss-weight module (warmup, per-stage λ^max caps, frozen-during-L-BFGS, re-warm)
- Collocation sampler interface (uniform + spec-adaptive, stateful `(model, last_residuals)` hook)
- Merged gradient clipping (LOOP-04 C-table, Adam-only)
- ADVANCE/RECOVER/HALT stage-exit machine (gate *form*; provisional thresholds)
- sL-BFGS preflight typed refusal
- Dataset-free `tests/phase40` unittest contract (deferred-import skip guards)

**Out of scope (from SPEC.md):**
- Config / checkpoint / resume / determinism (Phase 41, CTRL-01..08) — the loop *consumes* a config object and *can* be checkpointed; the keyed-YAML, atomic-checkpoint, promotion, `--hold-stage` rollback, and seed/RNG contracts are Phase 41
- Operator runbook / monitoring surface (Phase 42, OPS-01..06) — Phase 40 logs only what the loop needs to operate
- Verification / smoke test / Stage-0 pilot / acceptance verdict (Phase 43, ACC-01..06)
- Stochastic-L-BFGS implementation for stages 3–6 — deferred PLAT-02; Phase 40 only *refuses* it
- Full multi-stage curriculum beyond the Stage 0–2 full-batch path — deferred PLAT-01
- Calibrated threshold values (`ε_phys`, `ε_energy`, `ε_plateau`, MAX_EPOCHS, stagnation windows) — provisional pending Phase-43 pilot calibration

</spec_lock>

<decisions>
## Implementation Decisions

Labels continue the CTX namespace from Phase 39 (which ended at CTX-32).

### Module Layout
- **CTX-33:** The Phase 40 driver lands as a **`pinn/training/` subpackage**
  (~6 modules: controllers, PHYS-05 schedule, collocation sampler, gradient
  clipping, stage-exit machine, sL-BFGS preflight — exact filenames planner
  discretion). This follows the `pinn/data/` and `pinn/verification/`
  precedent for a cohesive multi-module concern; Phase 38's CTX-15 "flat
  modules" precedent covered single-purpose science modules, not a
  six-module driver layer. Phase 41/42 seams import from one namespace.

### Gradient-Clip Constants (the §4.4 FUT-deferred set — this phase IS that FUT)
- **CTX-34:** `C_stage` for stages 0–1 is implemented as a **provisional,
  config-overridable default of 8.5** per REQUIREMENTS TRAIN-05.
  **Provenance correction (must not propagate):** SPEC.md:84 cites 8.5 as
  "trainex-r1a-ratified"; that citation does not hold. `8.5` appears nowhere
  in the trainex-r1 package, the framework specs, or `.planning` outside
  TRAIN-05 itself. r1a B-1 records the early-stage value as "left open by
  the spec itself"; `pinn_architecture.md` §4.4 routes it to FUT and "does
  not tag the early-stage value as locked" (spec range: 7–10; 8.5 is the
  midpoint). The build is grounded (a REQUIREMENTS requirement is a
  grounding source) but the value is **provisional, surfaced for ACC-05
  pilot calibration** — treated like the other ⚖ seams, never cited as
  ratified. Stages 2–3: 5.0; stages 4–6: 3.0 (same provisional treatment;
  rolling window = last 100 norms per §4.4).
- **CTX-35:** Bootstrap median before the 100-norm window fills = **median
  of the partial window**, from step 1 onward. Same formula over a shorter
  history: always defined and finite (satisfies the SPEC's held-out edge
  test), leaves no unclipped early window, invents no constant. At step 1,
  `clip = C_stage × that single norm`.
- **CTX-36:** Median lower floor = **config seam defaulting to the spec's
  own worked example `1e-6`, flagged provisional**. Without a floor, a
  converged stage drives `median(grad_norm) → 0` and `clip_value → 0`,
  silently annihilating every gradient. The default uses the only number
  §4.4 puts on the page; ACC-05 calibrates it against observed Stage-0
  norms.
- **CTX-37:** Gradient-norm history is **cleared at every stage boundary**.
  Parallels D7-b's complete Adam reset and the L-BFGS-history rule (nothing
  optimizer-stateful crosses a boundary), and is correct on the merits:
  `C_stage` changes at boundaries (8.5→5.0→3.0) and the new stage's gradient
  scale differs, so a stale median would mis-clip the new stage's first
  steps. Pairs with CTX-35's partial-window bootstrap.

### Provisional-Threshold Mechanics (CURR-03 gate)
- **CTX-38:** The ADVANCE-gate thresholds CURR-03 supplies (β = 0.98,
  patience = 200, ε_plateau = 1e-5, ε_phys = 1e-4, ε_energy = 1e-4 with
  energy floor `ε_H = 1e-4·S_H`) are **transcribed as provisional-tagged
  config defaults**, each carrying provenance (spec section +
  `provisional: true`), and the loop **logs the full provisional set once at
  run start** so every run folder records which values were uncalibrated.
  Phase 41 freezes the same fields into `config.yaml` verbatim.
- **CTX-39:** MAX_EPOCHS (per-stage), the stagnation window, and the
  percentile-10 relaxation are **config-required — the RunController raises
  at construction if unset**. CURR-03 marks all three "claimed-unverified
  (D5-05; CLM-08/09), not transcribed as locked"; no value exists anywhere
  in the corpus, and SCOPE-19 forbids inventing one. Mirrors the D4-a
  pattern: the owner picks once, at the designed moment, informed by
  ACC-02's measured s/step. Also bounds every run on the single M5 Pro.
- **CTX-40:** ε_phys is a **single scalar (1e-4 provisional), no per-stage
  table**. CURR-03 explicitly declines to transcribe the issue-doc per-stage
  table (claimed-unverified, D5-05/CLM-08/09); building the table shape
  would import a structure the spec rejected.
- **CTX-41:** RECOVER at the ratified default `recover.retries: 0` = **roll
  back to the last well-formed checkpoint, record the RECOVER disposition,
  then transition to HALT/REVIEW without any retraining attempt**.
  `retries: 0` means zero *retries*, not zero rollback: the run folder is
  left holding a numerically valid state (Tier-1 "stop-and-preserve"
  satisfied) and the SPEC's AC wording ("rollback … transitions to
  HALT/REVIEW after the single attempt") is satisfied literally. NaN/Inf
  routes to RECOVER regardless of phase (Adam or L-BFGS, per SPEC edge
  coverage).

### Phase-41 Seam (config + checkpoint)
- **CTX-42:** The loop consumes a **top-level `TrainingConfig` composed of
  nested frozen dataclasses whose grouping mirrors CTRL-01's keyed-YAML
  sections (run / stage / opt / loss)**, each sub-config validating its own
  invariants at construction (the `ArchitectureSpec`/`RuntimeSpec` pattern,
  CTX-18). No YAML parsing in Phase 40 (CTX-19 carries forward); Phase 41
  maps YAML sections onto these dataclasses field-for-field. The
  config-required CTX-39 fields live here and raise if unset.
- **CTX-43:** Checkpointing is a **`CheckpointStore` protocol** (save →
  id, load-latest → state, rollback semantics) that the controllers depend
  on, plus a **deliberately naive `torch.save` implementation** sufficient
  for the dataset-free tests and RECOVER's contract. Phase 41 swaps in the
  atomic/retention/promotion implementation (CTRL-02..04) behind the same
  interface without touching controller code. The seam is the interface.
- **CTX-44:** Every stateful training component exposes
  **`state_dict()` / `load_state_dict()`** (torch convention); the
  RunController composes them into one nested dict keyed by component.
  Values are plain tensors/containers + python scalars so Phase 41's
  `weights_only`-clean requirement (CTRL-03) is satisfiable; CTRL-08's RNG
  capture later slots in as one more key. TRAIN-03's "schedule state
  serialized into checkpoints" is met by the schedule module's state_dict.

### Phase-42 Seam (logging)
- **CTX-45:** Loop-operational logging goes through **stdlib
  `logging.getLogger('pinn.training.*')` with machine-readable key/value
  payloads passed via `extra`**. Zero new dependencies, testable with
  unittest's `assertLogs`, consistent with the Phase-39 adapter's `mem:`
  line pattern. Phase 42 attaches a JSONL handler/formatter to the same
  logger tree (OPS-03's widened field set becomes a formatter concern) —
  the seam is the logger names + payload discipline. Events Phase 40 must
  emit: the CTX-38 run-start provisional-threshold set, stage-exit
  dispositions (ADVANCE/RECOVER/HALT), and Adam→L-BFGS handoff events.

### Optimizer & Loop Details (auto-resolved under owner's 2026-07-16 autonomy directive; rationale logged)
- **CTX-46:** Plateau-handoff detector (TRAIN-02) = **per-epoch finite
  difference of `log10(L_phys)` with a 50-consecutive-epoch counter that
  resets on any violating epoch** — the literal transcription of
  `d(log10 L_phys)/d(epoch) > −5e-3` for 50 consecutive epochs. The SPEC's
  AC (flat curve → handoff at epoch ≥ 50; descending → never) is satisfied
  by exactly this form; windowed-regression smoothing would be invented.
  Note this is DISTINCT from CURR-03 gate criterion 1 (β-smoothed total-loss
  plateau, patience 200) — two different criteria, both implemented.
- **CTX-47:** L-BFGS: `history_size = 10` and Wolfe line search
  (`line_search_fn="strong_wolfe"`) are spec-fixed; `max_iter` is a
  **provisional config default of 20** within the spec's open 20–50 range —
  the conservative wall-time end on a single M5 Pro (D5-a's flagged
  uncertainty is full-batch closure wall-time) and torch's own default.
  Flagged provisional like CTX-34.
- **CTX-48:** Adam cosine-annealing horizon: **`T_max = N_Adam,k`**, the
  stage's configured Adam epoch budget. PHYS-05's warmup formula
  (`I_warm = min(2000, 0.1·N_Adam,k)`) already treats `N_Adam,k` as a known
  per-stage quantity; it joins the CTX-39 config-required set (owner-picked,
  informed by ACC-02). Adam β = (0.9, 0.999), ε = 1e-8, per-stage
  `LR_k = 1e-3 × 0.7^k`, complete Adam reset at boundaries (D7-b) — all
  spec-fixed, transcribed.
- **CTX-49:** Validation cadence: the knob's existence is mandated (r1a
  B-4/U-5 "needed-now D5 skeleton fact"); no spec value exists. As an
  **operational knob** (not a science threshold) it takes the U-6 precedent
  — set at implementation with a logged rationale: **provisional default
  `validation_every = 10` epochs**. Rationale: gate criterion 1's patience
  is 200 epochs, so a 10-epoch cadence gives criterion 2's min-tracking ~20
  validation points per patience window — adequate resolution without a
  full val-set forward pass every epoch.

### Claude's Discretion
- Exact module filenames within `pinn/training/` (CTX-33 constrains the
  shape, not the names; must not collide with v1.3-era files).
- Controller-internal test seams for the SPEC's forced-ADVANCE /
  forced-HALT injection ACs (TRAIN-01) — any clean injection mechanism.
- Logger payload key names (CTX-45 fixes the mechanism and required events).
- The per-epoch batch/resample cadence is NOT discretion — it is answered
  by LOOP-01..03 and the Phase-39 contracts (DATA-04 per-epoch seeded
  shuffle, DATA-05 selection rules); the researcher/planner reads those
  sections rather than deciding.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase 40 scope
- `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-SPEC.md` — Locked requirements (TRAIN-01..07), boundaries, acceptance criteria, edge coverage, prohibitions. MUST read before planning.
- `.planning/REQUIREMENTS.md` — TRAIN-01..07 requirement text; SCOPE-16..21; the owner-carved seam table (D1-p, D4-a, D4-c/R-2, R-1, B-5).

### Training-loop contracts (the science being transcribed)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Stage-0 contract: two-phase Adam→L-BFGS loop shape, CURR-03 stage-exit machine (§ "dual-path stage-transition state machine", lines ~1924–1998: ADVANCE four-criterion gate with provisional values β=0.98/patience=200/ε_plateau=1e-5/ε_phys=1e-4/ε_energy=1e-4, RECOVER, HALT/REVIEW), LOSS-04 causal-training mode, consolidated hyperparameter schedule (LR `1e-3×0.7^k`), LOOP-01..04 batch/step contracts.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — §4.4 Adaptive Gradient Clipping (normative listing: 100-norm rolling window, `C_stage · median`; the FUT-deferred set CTX-34..37 resolves), PHYS-05 warmup schedule (`I_warm = min(2000, 0.1·N_Adam,k)`, per-stage λ^max, `λ_E^max ≤ 1`), §3 loss-term math homes.

### Ratified build-engineering decisions
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` — D5-a (two-phase closure loop, accumulate-in-closure, sL-BFGS preflight refusal), D5-b (sampler interface, `(model, last_residuals)` hook), D5-c (scheduled-weights module + empty rebalance seam; U-6 set-at-implementation precedent), D7-b (complete Adam reset), D7-c/D7-d (rollback/promotion context for the CTX-43 seam), B-1 (stage-0 schedule; C-value "left open by the spec itself"), B-3 (controller naming), B-4/U-5 (validation-cadence knob existence).
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — ratification record for the above (owner-ratified 2026-07-05).

### Prior-phase substrate and locked conventions
- `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-CONTEXT.md` — CTX-15..32: module conventions, frozen-dataclass config pattern (CTX-18/19), `resolve_runtime`-only precision/device flow (CTX-20), v1.3-code prohibition (CTX-17).
- `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md` — Phase-39 adapter/batch/split decisions the loop consumes; `pinn/data-handling/` legacy import ban.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `pinn/loss_catalog.py` — `LossWeights` frozen dataclass was built FOR this
  phase (docstring: "matching Phase 40's PHYS-05 weight vector";
  `lambda_data` pinned 1.0); `compose_total(terms, weights)` is the
  composition seam the schedule module feeds. `causal_physics_loss` already
  settles U-6 (exponent deliberately unclipped; underflow → w_n → 0 is
  correct causal gating) — do NOT re-open.
- `pinn/network.py` `build_network(spec, *, dtype, device)` +
  `pinn/architecture_spec.py` frozen `ArchitectureSpec` — model entry.
- `pinn/runtime.py` `resolve_runtime(precision, device)` — the ONLY
  precision/device source (CTX-20).
- `pinn/data/batches.py` — `select_stage_records`, `sample_data_points`,
  `sample_collocation_points`, `build_stage_batch`; already emits
  replay-only (`B_lookahead = 0`) at the final stage (SPEC edge coverage).
- `pinn/data/adapter.py` / `splits.py` — admitted-set source and
  stage-stratified split the gate's held-out validation consumes.
- `pinn/physics_residual.py` — PHYS-02 componentwise AD residual for the
  physics/energy loss path.

### Established Patterns
- Frozen typed dataclass validated at construction (`ArchitectureSpec`,
  `RuntimeSpec`, `LossWeights`) — CTX-42 configs follow it.
- `tests/phaseNN` stdlib-unittest with deferred-import skip guards; conda
  env `pinn-train` via `<home>/miniforge3/bin/conda run -n
  pinn-train` (conda is off-PATH; repo .venv/system pythons have no torch).
- Structured log lines with machine-readable payloads (adapter's `mem:`
  line) — CTX-45 extends this discipline.
- v1.3-era files (`basic_architecture.py`,
  `data-processing-pipeline-full.py`, `data-handling/`) are reference-only
  and MUST NOT be imported (CTX-17, Phase-39 ban).

### Integration Points
- `pinn/training/` (new) sits on top of `pinn/data/` (batches in) and
  `pinn/network.py` + `pinn/loss_catalog.py` (model/loss), under
  `tests/phase40` (dataset-free contract tests).
- Phase 41 attaches at exactly two seams: the CTX-42 `TrainingConfig`
  dataclasses (YAML mapping) and the CTX-43 `CheckpointStore` protocol
  (atomic/retention/promotion impl).
- Phase 42 attaches at the CTX-45 logger tree (JSONL/TensorBoard handlers).
- Phase 43's verify ladder and pilot consume the CTX-38 run-start
  provisional log and the CTX-39 config-required fields.

</code_context>

<specifics>
## Specific Ideas

- The SPEC's one 🧪 backstop edge (empty/partial grad-norm window: "the
  clip must be defined and finite for a window with fewer than the
  rolling-length entries") is resolved by CTX-35 and MUST be carried into
  plan-phase `must_haves` as a held-out test, per SPEC Edge Coverage.
- TRAIN-01's AC requires forced-signal injection (ADVANCE → Δstage=+1,
  HALT → Δstage=0) — the controllers need a deliberate injection seam, not
  test-only monkey-patching.
- The two plateau criteria must not be conflated: TRAIN-02's Adam→L-BFGS
  handoff (log10-slope > −5e-3, 50 consecutive epochs) is a *within-stage
  optimizer transition*; CURR-03 criterion 1 (β-smoothed relative change
  < ε_plateau, patience 200) is a *stage-exit gate input*. Both exist,
  separately.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` (D-06 static-epsilon
  sensitivity check) — matched Phase 40 only on generic keywords
  ("safe, phase"); it is an admitted-set physics/data probe closer to
  Phase 38/43 territory, not training-driver work.
- `trainex-r1-research-handoff.md` (r1a+r1b sub-package handoff review) —
  matched on generic keywords ("review, two"); research-process task with
  no code surface in the training loop.

</deferred>

---

*Phase: 40-stage-0-curriculum-training-loop-fut-04*
*Context gathered: 2026-07-16*
