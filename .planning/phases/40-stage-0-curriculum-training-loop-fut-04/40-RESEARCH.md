# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) - Research

**Researched:** 2026-07-17
**Domain:** PyTorch training-loop engineering (two-phase Adam→L-BFGS optimization, scheduled loss weights, adaptive gradient clipping, curriculum stage-exit state machine) implementing an already-locked physics/science contract.
**Confidence:** HIGH on PyTorch API mechanics (verified against official 2.12 docs); MEDIUM on the "accumulate-in-closure" full-batch sizing question (spec wording is genuinely ambiguous and flagged below); the numeric thresholds throughout are deliberately provisional per SPEC.md and must not be treated as anything but placeholders.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Labels continue the CTX namespace from Phase 39 (which ended at CTX-32).

**Module Layout**
- **CTX-33:** The Phase 40 driver lands as a **`pinn/training/` subpackage** (~6 modules: controllers, PHYS-05 schedule, collocation sampler, gradient clipping, stage-exit machine, sL-BFGS preflight — exact filenames planner discretion). Follows the `pinn/data/` and `pinn/verification/` precedent for a cohesive multi-module concern.

**Gradient-Clip Constants (the §4.4 FUT-deferred set — this phase IS that FUT)**
- **CTX-34:** `C_stage` for stages 0–1 = **provisional, config-overridable default of 8.5** (TRAIN-05). Provenance correction: SPEC.md's "trainex-r1a-ratified" citation for 8.5 does NOT hold — 8.5 appears nowhere in the trainex-r1 package or framework specs; the spec range is 7–10 and 8.5 is the midpoint, left open by the spec itself. Treat as provisional, surfaced for ACC-05 pilot calibration, never as ratified. Stages 2–3: 5.0; stages 4–6: 3.0 (same provisional treatment; rolling window = last 100 norms per §4.4).
- **CTX-35:** Bootstrap median before the 100-norm window fills = **median of the partial window**, from step 1 onward. At step 1, `clip = C_stage × that single norm`.
- **CTX-36:** Median lower floor = **config seam defaulting to the spec's own worked example `1e-6`, flagged provisional**.
- **CTX-37:** Gradient-norm history is **cleared at every stage boundary** (parallels the complete Adam reset and L-BFGS-history-never-crosses-a-boundary rule).

**Provisional-Threshold Mechanics (CURR-03 gate)**
- **CTX-38:** ADVANCE-gate thresholds (β=0.98, patience=200, ε_plateau=1e-5, ε_phys=1e-4, ε_energy=1e-4 with energy floor `ε_H = 1e-4·S_H`) are **transcribed as provisional-tagged config defaults** with provenance + `provisional: true`; the loop **logs the full provisional set once at run start**.
- **CTX-39:** MAX_EPOCHS (per-stage), the stagnation window, and the percentile-10 relaxation are **config-required — the RunController raises at construction if unset**. No value exists anywhere in the corpus; SCOPE-19 forbids inventing one.
- **CTX-40:** ε_phys is a **single scalar (1e-4 provisional), no per-stage table** (the issue-doc per-stage table is claimed-unverified and rejected).
- **CTX-41:** RECOVER at `recover.retries: 0` = **roll back to the last well-formed checkpoint, record the RECOVER disposition, then transition to HALT/REVIEW without any retraining attempt.** NaN/Inf routes to RECOVER regardless of phase (Adam or L-BFGS).

**Phase-41 Seam (config + checkpoint)**
- **CTX-42:** The loop consumes a **top-level `TrainingConfig` composed of nested frozen dataclasses** mirroring CTRL-01's keyed-YAML sections (run/stage/opt/loss), each validating its own invariants at construction (the `ArchitectureSpec`/`RuntimeSpec` pattern). No YAML parsing in Phase 40.
- **CTX-43:** Checkpointing is a **`CheckpointStore` protocol** (save→id, load-latest→state, rollback semantics) plus a **deliberately naive `torch.save` implementation** sufficient for dataset-free tests and RECOVER. Phase 41 swaps in the atomic/retention/promotion implementation behind the same interface.
- **CTX-44:** Every stateful training component exposes **`state_dict()`/`load_state_dict()`**; the RunController composes them into one nested dict keyed by component. Values are plain tensors/containers + python scalars for Phase 41's `weights_only`-clean requirement.

**Phase-42 Seam (logging)**
- **CTX-45:** Loop-operational logging goes through **stdlib `logging.getLogger('pinn.training.*')` with machine-readable key/value payloads via `extra`**. Events Phase 40 must emit: the CTX-38 run-start provisional-threshold set, stage-exit dispositions (ADVANCE/RECOVER/HALT), Adam→L-BFGS handoff events.

**Optimizer & Loop Details (auto-resolved under owner's 2026-07-16 autonomy directive)**
- **CTX-46:** Plateau-handoff detector (TRAIN-02) = **per-epoch finite difference of `log10(L_phys)` with a 50-consecutive-epoch counter that resets on any violating epoch** — literal transcription of `d(log10 L_phys)/d(epoch) > −5e-3` for 50 consecutive epochs. DISTINCT from CURR-03 gate criterion 1 (β-smoothed total-loss plateau, patience 200) — both exist, separately.
- **CTX-47:** L-BFGS: `history_size = 10` and `line_search_fn="strong_wolfe"` are spec-fixed; `max_iter` is a **provisional config default of 20** within the spec's open 20–50 range.
- **CTX-48:** Adam cosine-annealing horizon: **`T_max = N_Adam,k`**, the stage's configured Adam epoch budget (joins the CTX-39 config-required set). Adam β=(0.9, 0.999), ε=1e-8, per-stage `LR_k = 1e-3 × 0.7^k`, complete Adam reset at boundaries — all spec-fixed.
- **CTX-49:** Validation cadence: **provisional default `validation_every = 10` epochs** (operational knob, not a science threshold).

### Claude's Discretion
- Exact module filenames within `pinn/training/` (CTX-33 constrains the shape, not the names; must not collide with v1.3-era files).
- Controller-internal test seams for the SPEC's forced-ADVANCE/forced-HALT injection ACs (TRAIN-01) — any clean injection mechanism.
- Logger payload key names (CTX-45 fixes the mechanism and required events).
- **NOT discretion:** the per-epoch batch/resample cadence — answered by LOOP-01..03 and Phase-39 (DATA-04 per-epoch seeded shuffle, DATA-05 selection rules).

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope. Two todos reviewed and NOT folded in: `d-06-static-epsilon-sensitivity-check.md` (Phase 38/43 territory) and `trainex-r1-research-handoff.md` (research-process task, no code surface).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TRAIN-01 | `CurriculumController` + `RunController` drive outer/inner loops, implementing (not re-deciding) the Stage-0 contract | Architecture Patterns (system diagram, controller responsibilities); Code Examples (injection-seam pattern); Don't Hand-Roll (state-machine libraries not needed — a small explicit class suffices) |
| TRAIN-02 | Two-phase Adam→L-BFGS closure loop; accumulate-in-closure; frozen-λ + no-clip during L-BFGS | Code Examples (`torch.optim.LBFGS` closure contract, verified via context7/PyTorch 2.12 docs); Common Pitfalls (closure-consistency requirement, create_graph memory-leak risk, accumulate-in-closure semantics); Open Questions (full-batch sizing ambiguity) |
| TRAIN-03 | PHYS-05 scheduled loss-weight module (warmup, per-stage λ^max, frozen/re-warm, checkpointable state) | Architecture Patterns (ScheduledWeights module contract); Code Examples (warmup formula, `state_dict`/`load_state_dict` pattern already established by `ArchitectureSpec`/`RuntimeSpec`) |
| TRAIN-04 | Collocation sampler interface (uniform + adaptive `(model, last_residuals)` hook) | Architecture Patterns (sampler interface, relationship to `pinn/physics_residual.py`'s residual tensor shape); Open Questions (residual-reduction shape is genuinely undefined — low risk, TRAIN-04's AC does not test adaptive-mode's internal density algorithm) |
| TRAIN-05 | Merged gradient clipping: `clip_value = C_stage · median(grad_norm_history)`, Adam-only | Common Pitfalls (**`torch.median` even-length semantics — verified via official docs, differs from numpy/statistics median and is load-bearing for the floating-tolerance AC**); Code Examples (`clip_grad_norm_` verified signature/return/`error_if_nonfinite`) |
| TRAIN-06 | ADVANCE/RECOVER/HALT stage-exit machine, no fallback advancement | Architecture Patterns (state-machine responsibilities); Don't Hand-Roll (NaN detection via `clip_grad_norm_(error_if_nonfinite=True)` instead of manual `isnan` scanning) |
| TRAIN-07 | sL-BFGS preflight typed refusal for stages ≥3 | Code Examples (typed-exception pattern, mirrors Phase 39's `StageZeroUnderpopulated`/`DataVersionHashMismatch` sentinel-exception style) |
</phase_requirements>

## Summary

Phase 40 is a **pure implementation-technique phase**: every science decision (loop shape, warmup formula, clip formula, stage-exit criteria) is already locked by `ctl_instruction.md` §"Phase 2" / `pinn_architecture.md` §4.1/§4.4 and by the CTX-33..49 engineering decisions in `40-CONTEXT.md`. What remains is translating that locked contract into correct PyTorch code. This research therefore focuses on **PyTorch API mechanics that are easy to get subtly wrong**: the `torch.optim.LBFGS` closure contract, the exact (and non-obvious) definition of `torch.median` on even-length windows, the `create_graph=True` reference-cycle memory-leak warning that directly touches the physics-residual second-derivative path, and the precise meaning of "accumulate-in-closure" full-batch L-BFGS given the existing Phase-39 batch-construction interface.

The existing codebase (Phase 38 model/loss, Phase 39 data) already establishes every pattern Phase 40 needs to reuse: frozen validated dataclasses (`ArchitectureSpec`, `RuntimeSpec`, `LossWeights`) for config objects, explicit-dtype/device construction (no defaults, no availability probes), `state_dict`-style component composition, deferred-import `unittest` skip guards, and typed sentinel exceptions (`StageZeroUnderpopulated`, `DataVersionHashMismatch`). Phase 40 should extend these patterns, not invent new ones.

**Primary recommendation:** Build `pinn/training/` as six small modules around one `RunController.run_stage(k)` method that (1) runs an Adam loop with per-epoch resampled batches (`build_stage_batch`), the PHYS-05 schedule, and Adam-only clipping, gated by a 50-epoch flat-`log10(L_phys)`-slope detector; (2) hands off to a single `torch.optim.LBFGS` phase operating on ONE FIXED batch (drawn once at hand-off, not resampled per closure call) via a closure that recomputes forward+backward from scratch each invocation with λ frozen and no clipping; (3) evaluates the CURR-03 four-criterion ADVANCE gate, the NaN/Inf RECOVER path, and the HALT/REVIEW path as a small explicit state object, not a state-machine library. A `SLBFGSPreflight.check(stage)` typed refusal gates any stage ≥3 request before either phase runs.

## Architectural Responsibility Map

This is a single-machine ML training pipeline (no browser/API/DB tiers). Tiers below are the domain-appropriate analog: **Driver** (the new Phase 40 code), **Optimizer Library** (torch native, external), **Model** (Phase 38), **Data Supply** (Phase 39), **Config/Checkpoint** (Phase 41 seam only), **Observability** (Phase 42 seam only).

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Outer curriculum progression (stage k, ADVANCE/RECOVER/HALT) | Driver (`CurriculumController`) | Config/Checkpoint (seam) | Stage-exit decisions are training-loop logic; checkpoint I/O is a seam Phase 40 depends on but does not implement |
| Inner Adam/L-BFGS optimization | Driver (`RunController`) | Optimizer Library (`torch.optim`) | Loop control (when to hand off, when to clip) is Driver; the actual step math is torch's own optimizer classes — never hand-rolled |
| PHYS-05 scheduled weights | Driver (`ScheduledWeights` module) | Model (consumes `pinn.loss_catalog.LossWeights`) | Scheduling logic is new Driver code; the weight *container* type is already Phase 38's frozen `LossWeights` |
| Gradient clipping | Driver (`GradClipper`) | Optimizer Library (`torch.nn.utils.clip_grad_norm_`) | Driver owns the median/C_stage/window bookkeeping; the norm computation and in-place clip are torch's own function |
| Collocation sampling | Driver (`CollocationSampler`) | Model (adaptive hook receives the model + `pinn.physics_residual` residuals) | New Driver code; the adaptive hook's inputs come from Model-tier objects |
| Forward/backward/loss composition | Model (`pinn.network`, `pinn.loss_catalog`) | Driver (calls it each step) | Unchanged Phase 38 code; Driver is only a caller |
| Batch supply (which trajectories, which points) | Data Supply (`pinn.data.batches`) | Driver (calls it each epoch) | Unchanged Phase 39 code; LOOP-01..03 batch/resample cadence is NOT Phase-40 discretion |
| Checkpoint persistence | Config/Checkpoint (seam: `CheckpointStore` protocol, naive impl) | Driver (calls save/load/rollback) | Phase 40 defines the interface and a placeholder impl only; Phase 41 owns atomicity/retention |
| Structured logging | Observability (seam: `logging.getLogger('pinn.training.*')`) | Driver (emits events) | Phase 40 emits events through stdlib logging only; Phase 42 owns JSONL/TensorBoard formatting |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| PyTorch | 2.12.1 (installed, confirmed via `conda run -n pinn-train python -c "import torch; print(torch.__version__)"`) | `torch.optim.Adam`, `torch.optim.LBFGS`, `torch.optim.lr_scheduler.CosineAnnealingLR`, `torch.nn.utils.clip_grad_norm_` | Already the project's locked runtime (Phase 37 ENV-01..04); no alternative framework is in scope |
| `torch.median` | stdlib to torch | Rolling-window median for TRAIN-05's clip formula | `pinn_architecture.md` §4.4's normative pseudocode literally calls `torch.median(torch.stack(grad_history))` — this is the spec-mandated function, not a free choice |

No new third-party packages are introduced by this phase. `unittest` (stdlib) is the test framework, matching Phase 37/38/39 (`pytest` is neither installed nor required in the `pinn-train` conda env).

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| stdlib `logging` | — | CTX-45 event emission | Every stage-exit disposition, Adam→L-BFGS handoff, run-start provisional-threshold dump |
| stdlib `dataclasses` | — | `TrainingConfig` nested frozen dataclasses (CTX-42) | Same pattern as `ArchitectureSpec`/`RuntimeSpec`/`LossWeights` |
| stdlib `unittest` | — | `tests/phase40/*` dataset-free contract tests | Matches the Phase 37/38/39 deferred-import skip-guard convention |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| A small explicit Python class for the ADVANCE/RECOVER/HALT machine | A formal state-machine library (`transitions`, `python-statemachine`) | Rejected: the state space is 3 dispositions with no reentrant sub-states; a library adds a dependency and indirection for no benefit, and CONTEXT.md's Don't-Hand-Roll instinct here is inverted — the *state machine* is trivial, the *four-criterion gate evaluation* is the substantive logic and belongs in plain code anyway |
| `torch.optim.LBFGS` (spec-mandated) | Third-party L-BFGS implementations (e.g. `hjmshi/PyTorch-LBFGS`, found in web research) that support genuine stochastic mini-batch L-BFGS | Not applicable here: the spec locks stages 0–2 to standard full-batch `torch.optim.LBFGS`; a third-party sL-BFGS package is exactly what TRAIN-07's preflight refusal defers (PLAT-02), not something Phase 40 should adopt |

**Installation:** none required — `torch` is already installed in the `pinn-train` conda environment (verified: `torch.__version__ == '2.12.1'`, `torch.backends.mps.is_available() == True`).

## Package Legitimacy Audit

**Not applicable.** This phase introduces zero new external packages; it consumes the already-verified `torch`/`numpy` stack from Phase 37 (ENV-01) and the existing `pinn/` modules from Phases 38–39. No `npm view`/`pip index versions` gate applies.

## Architecture Patterns

### System Architecture Diagram

```
Phase-39 StageQuery/adapter (admitted set, in-memory fp32)
        │
        ▼
build_stage_batch(source, stage=k, rng, dtype, device)   [pinn/data/batches.py — unchanged]
        │  FixedBatch { DataFidelityPoints, PhysicsCollocationPoints, replay_keys, lookahead_keys }
        ▼
┌───────────────────────────── CurriculumController (outer loop) ─────────────────────────────┐
│  owns: current stage k, CheckpointStore, ScheduledWeights re-warm trigger, curriculum.jsonl   │
│                                                                                                │
│  loop:                                                                                         │
│    SLBFGSPreflight.check(k)          # TRAIN-07 — raises before k >= 3 is ever entered         │
│    disposition = RunController.run_stage(k)                                                   │
│    match disposition:                                                                          │
│      ADVANCE  -> checkpoint stage-{k}-final.pt + stage-{k+1}-init.pt; k += 1; re-warm schedule │
│      RECOVER  -> CheckpointStore.rollback(); (retries:0 => immediately) -> HALT/REVIEW          │
│      HALT     -> stop; surface for owner review (no further stages)                            │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
        │  per call: RunController.run_stage(k)
        ▼
┌───────────────────────────────── RunController (inner two-phase loop) ──────────────────────┐
│                                                                                                │
│  ── Phase 2a: Adam ──────────────────────────────────────────────────────────────────────    │
│  fresh torch.optim.Adam(params, lr=LR_k, betas=(0.9,0.999), eps=1e-8)     [D7-b: full reset]  │
│  fresh CosineAnnealingLR(optimizer, T_max=N_Adam,k)                        [CTX-48]           │
│  ScheduledWeights.rewarm()                                                 [PHYS-05, CTX-38]  │
│  GradNormHistory.clear()                                                   [CTX-37]           │
│  for epoch in range(N_Adam,k):                                                                │
│      batch = build_stage_batch(source, stage=k, rng=seeded_rng, ...)      [per-epoch resample,│
│                                                                             DATA-04/05 — NOT   │
│                                                                             discretion]        │
│      colloc = CollocationSampler(model, last_residuals)  -> physics/energy points [TRAIN-04]  │
│      pred = model(batch.tau_ic13, batch.masses)           [pinn/network.py, unchanged]        │
│      terms = {data, ic, phys, energy, angmom}  via pinn/loss_catalog.py functions              │
│      weights = ScheduledWeights.current(epoch)             [I_warm, lambda^max, CTX-38]        │
│      loss_terms = compose_total(terms, weights)                                                │
│      loss_terms.total.backward()                                                               │
│      last_residuals = physics_residual(...)   # feeds next epoch's adaptive sampler call       │
│      GradClipper.clip(model.parameters(), stage=k)          [TRAIN-05, Adam-only]              │
│      optimizer.step(); scheduler.step()                                                        │
│      PlateauDetector.update(log10(L_phys))                 [CTX-46: 50-epoch flat-slope]       │
│      if PlateauDetector.fires(): break  -> hand off to L-BFGS                                  │
│                                                                                                 │
│  ── Phase 2b: L-BFGS ────────────────────────────────────────────────────────────────────      │
│  ScheduledWeights.freeze()                                  [frozen λ during L-BFGS]           │
│  fixed_batch = build_stage_batch(source, stage=k, rng=seeded_rng, ...)  [drawn ONCE — see       │
│                                                                           Open Questions below] │
│  lbfgs = torch.optim.LBFGS(params, history_size=10,                                             │
│                             line_search_fn="strong_wolfe", max_iter=20)  [CTX-47]               │
│  def closure():                                                                                 │
│      lbfgs.zero_grad()                                                                          │
│      pred = model(fixed_batch...)   # recomputed fresh each call — no held graph across calls  │
│      loss = compose_total(...).total                                                            │
│      loss.backward()                # NO clip_grad_norm_ call here                              │
│      return loss                                                                                 │
│  lbfgs.step(closure)                 # torch internally re-invokes closure() for its line search│
│                                                                                                 │
│  ── Stage-exit evaluation ───────────────────────────────────────────────────────────────       │
│  StageExitMachine.evaluate(train_loss_history, val_loss_history, val_phys, val_energy,          │
│                             had_nan_inf, epoch_count)  -> ADVANCE | RECOVER | HALT   [TRAIN-06] │
│  return disposition to CurriculumController                                                     │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
pinn/training/
├── __init__.py             # package marker only (mirrors pinn/data/__init__.py minimalism)
├── config.py                # TrainingConfig nested frozen dataclasses (CTX-42)
├── controllers.py            # CurriculumController, RunController (CTX-33, B-3 naming)
├── scheduled_weights.py       # PHYS-05 warmup/λ^max/freeze/rewarm module (CTX-38, D5-c)
├── collocation_sampler.py     # uniform + adaptive (model, last_residuals) hook (TRAIN-04, D5-b)
├── grad_clip.py               # median-based rolling-window clipper (TRAIN-05, CTX-34..37)
├── stage_exit.py              # ADVANCE/RECOVER/HALT machine (TRAIN-06, CURR-03)
├── slbfgs_preflight.py        # typed refusal for stage >= 3 (TRAIN-07)
└── checkpoint.py              # CheckpointStore protocol + naive torch.save impl (CTX-43)

tests/phase40/
├── __init__.py
├── _fixtures.py               # stub model / stub StageQuery batch source (mirrors tests/phase39/_fixtures.py)
├── test_controllers.py        # TRAIN-01 forced-ADVANCE/forced-HALT injection
├── test_optimizer_phase.py    # TRAIN-02 handoff timing + frozen-λ + no-clip-during-LBFGS spies
├── test_scheduled_weights.py  # TRAIN-03 warmup length, lambda_E <= 1, freeze, rewarm
├── test_collocation_sampler.py# TRAIN-04 uniform/adaptive count + bounds + hook signature
├── test_grad_clip.py          # TRAIN-05 clip formula per stage + partial-window backstop + Adam-only spy
├── test_stage_exit.py         # TRAIN-06 four-criterion conjunction, RECOVER, HALT, no-fallback
├── test_slbfgs_preflight.py   # TRAIN-07 typed refusal for stage >= 3, accept for {0,1,2}
└── test_prohibitions.py       # AST/discovery audit mirroring tests/phase38-39 (no v1.3 imports, no hardcoded precision)
```

### Pattern 1: `torch.optim.LBFGS` closure contract (verified, PyTorch 2.12 official docs)
**What:** `optimizer.step(closure)` internally re-invokes `closure()` an implementation-determined number of times (bounded by `max_iter`/`max_eval`) to perform its line search / curvature updates. The closure itself is fully responsible for `zero_grad()`, the forward pass, `backward()`, and returning the scalar loss.
**When to use:** Every L-BFGS phase invocation (TRAIN-02).
**Example:**
```python
# Source: https://docs.pytorch.org/docs/2.12/optim.html (context7, verified)
def closure():
    optimizer.zero_grad()
    output = model(input)
    loss = loss_fn(output, target)
    loss.backward()
    return loss

optimizer.step(closure)
```
Configurable LBFGS params confirmed by the same doc set: `lr`, `max_iter` (max iterations **per `step()` call**), `max_eval`, `tolerance_grad`, `tolerance_change`, `history_size`, `line_search_fn` (e.g. `"strong_wolfe"`). Source: https://docs.pytorch.org/docs/2.12/generated/torch.optim.lbfgs.LBFGS.html

### Pattern 2: median-based rolling clip (verified formula + verified `torch.median` semantics)
**What:** `clip_value = C_stage * torch.median(torch.stack(grad_history))`, applied via `torch.nn.utils.clip_grad_norm_`.
**When to use:** Every Adam step only (TRAIN-05); never during L-BFGS.
**Example:**
```python
# Source: pinn_architecture.md §4.4 Listing 6 (normative, not executable) + context7-verified API
grad_history = []  # rolling window, cleared at stage boundaries (CTX-37)

# after loss.backward(), during the Adam phase only:
total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=float("inf"))
grad_history.append(total_norm.detach())
if len(grad_history) > 100:
    grad_history.pop(0)
clip_value = C_stage * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)
optimizer.step()
```
`clip_grad_norm_(parameters, max_norm, norm_type=2.0, error_if_nonfinite=False, foreach=None)` clips **in-place** and **returns the pre-clip total norm as a `Tensor`**; `error_if_nonfinite=True` raises instead of silently proceeding on a NaN/Inf norm — a clean detection point for the RECOVER path (TRAIN-06). Source: https://docs.pytorch.org/docs/2.12/generated/torch.nn.utils.clip_grad_norm_.html (context7, verified).

### Pattern 3: fresh optimizer + scheduler at every stage boundary (spec-mandated, D7-b)
**What:** Never reuse an `Adam`/`CosineAnnealingLR` instance across a stage boundary — construct both fresh so no momentum buffer or LR-schedule position carries over.
**When to use:** Start of every stage's Adam phase.
**Example:**
```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3 * (0.7 ** k),
                              betas=(0.9, 0.999), eps=1e-8)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_adam_epochs_k)
```

### Anti-Patterns to Avoid
- **Reusing one `Adam`/`LBFGS` instance across stage boundaries:** contradicts the spec's "Critical: Completely reset Adam's internal state" and D7-b; momentum buffers from stage k-1 bias stage k's early gradients.
- **Calling `clip_grad_norm_` inside the L-BFGS closure:** violates TRAIN-05's Adam-only scope and TRAIN-02's "no clipping during L-BFGS" AC; the spy-based test (clip-call count = 0 in L-BFGS) will catch this mechanically.
- **Resampling the batch inside the L-BFGS closure on every internal call:** L-BFGS's quasi-Newton curvature estimate assumes a *consistent* objective across the calls within one `step()`; resampling per call is functionally indistinguishable from a broken stochastic L-BFGS and is exactly the failure mode TRAIN-07 refuses for stages ≥3. Draw the batch once at hand-off, hold it fixed for the whole L-BFGS phase.
- **Using `numpy.median`/`statistics.median` anywhere near the clip formula:** see the dedicated Common Pitfall below — this silently disagrees with `torch.median` on even-length windows and will fail TRAIN-05's floating-tolerance AC nondeterministically depending on window parity.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Global-norm gradient clipping | A manual loop computing `sqrt(sum(p.grad.norm()**2 for p in params))` and scaling in place | `torch.nn.utils.clip_grad_norm_` | Already vectorized, already returns the total norm needed for `grad_history`, already has an `error_if_nonfinite` escape hatch for NaN/Inf detection |
| Cosine LR annealing | A hand-rolled `lr = lr_min + 0.5*(lr_max-lr_min)*(1+cos(...))` formula | `torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=...)` | Spec only fixes the *shape* (cosine annealing) and `T_max`; torch's scheduler is the standard, tested implementation and composes correctly with `optimizer.step()`/`scheduler.step()` ordering |
| Quasi-Newton refinement (L-BFGS) | Any custom BFGS/Hessian-approximation code | `torch.optim.LBFGS` | Spec-mandated (`history_size=10`, `strong_wolfe`); a hand-rolled implementation would also have to reproduce PyTorch's own closure-reevaluation contract, which is exactly the subtle part this research verified |
| NaN/Inf detection for the RECOVER path | Manually scanning every parameter's `.grad` for `isnan`/`isinf` | `clip_grad_norm_(..., error_if_nonfinite=True)` (raises), or `torch.isfinite(loss)` on the returned scalar | One call already computes the global norm the clip formula needs; reusing it for detection avoids a second full pass over all parameters |
| ADVANCE/RECOVER/HALT bookkeeping | A generic state-machine library (`transitions`, `python-statemachine`) | A small explicit class evaluating the 3-outcome, 4-criterion conjunction directly | Considered under Alternatives above — the state space is trivial; a library adds indirection without reducing the real complexity (which is in the four ADVANCE criteria, not the dispatch) |

**Key insight:** every piece of "hard" numerical machinery in this phase (clipping, cosine annealing, quasi-Newton refinement) already has a first-party, spec-compatible torch implementation. The actual engineering risk in Phase 40 is not reimplementing math — it's correctly *sequencing* torch's own primitives (closure contract, clip-then-step ordering, fresh-optimizer-per-boundary, frozen-λ-during-L-BFGS) and correctly matching `torch.median`'s specific (non-numpy) semantics.

## Common Pitfalls

### Pitfall 1: `torch.median` on an even-length window does NOT match `numpy.median`/`statistics.median`
**What goes wrong:** A test or implementation that uses `numpy.median`/`statistics.median` for the rolling grad-norm window will silently disagree with an implementation (or test) that uses `torch.median`, whenever the window has an even number of entries — which is common early in a stage (CTX-35's partial-window bootstrap starts at length 1, 2, 3, ... and is frequently even) and structurally guaranteed every time the window straddles the 100-entry cap from below.
**Why it happens:** `torch.median()` on an even-count tensor returns the **lower** of the two middle values, not their average. `numpy.median`/`statistics.median` average the two middle values. `torch.quantile(q=0.5)` computes the true midpoint average if that's ever needed instead.
**How to avoid:** `pinn_architecture.md` §4.4's own normative pseudocode calls `torch.median(torch.stack(grad_history))` — treat this as the spec-mandated function and use `torch.median` consistently in both the implementation and the TRAIN-05 tests (do not reach for `numpy`/`statistics` median anywhere near this formula, even in test fixtures that build a reference value by hand).
**Warning signs:** TRAIN-05's floating-tolerance AC (`clip value == C_stage * median(history)`) passes on odd-length fixtures and fails on even-length fixtures with a discrepancy of roughly half the gap between the two middle values.
*Confidence: HIGH — verified directly against the official PyTorch 2.12 `torch.median` documentation (context7).*

### Pitfall 2: "accumulate-in-closure" is gradient accumulation for memory, not just "recompute fresh each call"
**What goes wrong:** Reading "accumulate-in-closure" as merely "don't hold a persistent graph across `optimizer.step()` calls" understates the actual concern the ratified engineering decision (D5-a, r1b D-7) is addressing: a literal single forward+backward over the *entire* full-batch point set, through the physics/energy residual's second-derivative (create_graph) path, was flagged as capable of exceeding the M5 Pro's 24 GB unified memory if built as one graph.
**Why it happens:** The physics/energy loss terms require a second derivative (`d²r'/du²`) computed with graph connectivity back to the network weights (PHYS-02), which is memory-heavier per point than a plain forward pass. Building that graph for the whole full batch (thousands of collocation + data points) simultaneously multiplies that per-point cost.
**How to avoid:** Structure the L-BFGS closure to internally chunk the fixed full batch into smaller sub-batches and **accumulate** gradients across chunks within the same closure call — i.e., `zero_grad()` once, then for each chunk: forward, compute the chunk's (correctly-scaled) partial loss, `backward()` (accumulates into `.grad` since `zero_grad()` is not called between chunks), and finally return the summed/scaled total loss for L-BFGS's own bookkeeping. This is the standard PyTorch gradient-accumulation pattern (verified via context7's `notes/amp_examples.rst` gradient-accumulation recipe), applied inside one L-BFGS closure invocation instead of across an outer training loop.
**Warning signs:** MPS memory pressure / OOM specifically during the first L-BFGS phase of Stage 0–2 (not during Adam, which already operates on the smaller 256-trajectory per-epoch batch).
*Confidence: MEDIUM — the memory-bound reasoning is grounded in the ratified trainex-r1a text (D5-a / r1b D-7), and the accumulation mechanics are verified against official PyTorch docs; but neither CONTEXT.md nor SPEC.md pins an exact chunk size. See Open Questions.*

### Pitfall 3: `backward(create_graph=True)` reference-cycle memory leak
**What goes wrong:** PyTorch's own documentation warns that calling `.backward()` with `create_graph=True` can form a reference cycle between a parameter and its `.grad`, leaking memory across repeated calls — directly relevant to Phase 40's second-order physics-residual path, which is invoked on every epoch of a training run spanning potentially thousands of epochs per stage.
**Why it happens:** `create_graph=True` retains the backward graph attached to `.grad` so it can itself be differentiated again; if the tensor referenced by `.grad` is not cleared, a cycle forms.
**How to avoid:** The existing Phase 38 `pinn/physics_residual.py` already uses the SAFER pattern for its internal second-derivative computation (`torch.func.jacrev`/`torch.autograd.grad`-based, not raw `tensor.backward(create_graph=True)`) — the official docs' own recommended mitigation is "use `autograd.grad` for graph creation" instead of `backward()`. Phase 40 must preserve this discipline: do not "simplify" any part of the training step to call `.backward(create_graph=True)` directly, and if any future refactor does, explicitly break the cycle by clearing `.grad` after use.
**Warning signs:** Steadily increasing memory (RSS / MPS allocator) over the course of a long Adam phase that does not correspond to any legitimate growth (e.g., grad-norm history, which is capped at 100 entries).
*Confidence: HIGH — verified directly against official PyTorch `torch.autograd.backward` documentation (context7); the mitigating fact that Phase 38's existing code already uses the safe pattern is a direct code read, not an assumption.*

### Pitfall 4: conflating the two "plateau" criteria
**What goes wrong:** TRAIN-02's Adam→L-BFGS handoff detector (`d(log10 L_phys)/d(epoch) > -5e-3` for 50 consecutive epochs, a *within-stage optimizer-phase transition*) is a textually similar but functionally distinct criterion from CURR-03's ADVANCE gate criterion 1 (β=0.98-smoothed relative change in *total* loss below `ε_plateau=1e-5`, patience=200, a *stage-exit gate input*). Implementing only one, or sharing state between them, silently breaks either the handoff timing or the stage-exit gate.
**Why it happens:** Both are called "plateau" in the spec and both operate on a loss-trend signal, inviting code reuse that conflates two independently-specified detectors.
**How to avoid:** Implement as two separate objects (e.g., `PlateauDetector` for the handoff, and the total-loss EMA smoother inside `StageExitMachine`/CURR-03), each with its own state, tested independently (`test_optimizer_phase.py` vs `test_stage_exit.py`).
*Confidence: HIGH — directly stated in 40-CONTEXT.md's "Specific Ideas" section; carried here because it is exactly the class of bug a shared-code refactor would introduce.*

### Pitfall 5: gradient clip applied to the wrong optimizer phase, or in the wrong order relative to `optimizer.step()`
**What goes wrong:** `clip_grad_norm_` must run strictly after `backward()` and strictly before `optimizer.step()`, and strictly only during the Adam phase (never inside the L-BFGS closure). A misplaced call either clips gradients the optimizer never sees, or leaks clipping into L-BFGS and violates its assumed trust-region property (the spec's explicit rationale for the Adam-only scope: "line-search creates a trust region").
**How to avoid:** Gate the clip call on an explicit `phase == "adam"` flag rather than inferring it from optimizer type, so the TRAIN-02/TRAIN-05 spy tests can assert clip-call-count = 1 in Adam / 0 in L-BFGS unambiguously.
*Confidence: HIGH — directly required by SPEC.md's AC wording ("clip-call count = 1 in Adam, 0 in L-BFGS") and confirmed by the verified `clip_grad_norm_` semantics above.*

## Code Examples

### Deferred-import `unittest` skip-guard (established Phase 38/39 pattern — reuse verbatim)
```python
# Source: tests/phase38/test_loss_catalog.py:29-40 (existing codebase, read directly)
import importlib
import unittest

MODULE = "pinn.training.controllers"

def _import_symbol(name: str):
    """Deferred import so a missing symbol becomes a SKIP, not an ERROR."""
    try:
        mod = importlib.import_module(MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{MODULE} has not landed yet: {exc}") from exc
    if not hasattr(mod, name):
        raise unittest.SkipTest(f"{MODULE}.{name} has not landed yet")
    return getattr(mod, name)
```

### Typed sentinel exception (established Phase 39 pattern — reuse for TRAIN-07)
```python
# Pattern source: pinn/data/types.py StageZeroUnderpopulated / DataVersionHashMismatch
class StochasticLBFGSNotImplemented(Exception):
    """Typed refusal: stages >= 3 require sL-BFGS, which the v2.0 slice does not implement (PLAT-02)."""

    def __init__(self, stage: int) -> None:
        self.stage = stage
        super().__init__(
            f"stage {stage} requires stochastic L-BFGS (stages 3-6), which has no "
            f"implementation in this build (deferred PLAT-02); refusing rather than "
            f"silently deviating from the spec"
        )

def check_stage_preflight(stage: int) -> None:
    if stage >= 3:
        raise StochasticLBFGSNotImplemented(stage)
```

### `clip_grad_norm_` NaN/Inf detection feeding RECOVER
```python
# Verified API: https://docs.pytorch.org/docs/2.12/generated/torch.nn.utils.clip_grad_norm_.html
try:
    total_norm = torch.nn.utils.clip_grad_norm_(
        model.parameters(), max_norm=clip_value, error_if_nonfinite=True,
    )
except RuntimeError:
    # non-finite gradient norm -> route to RECOVER, not a crash
    return StageDisposition.RECOVER
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `torch.nn.utils.clip_grad_norm_` implemented as one monolithic function | Same public signature, now internally composed of `get_total_norm()` + `clip_grads_with_norm_()` (both independently callable) | PyTorch 2.x refactor (present in 2.12 docs) | No behavior change for Phase 40's call sites; worth knowing the two sub-functions exist if a future phase wants to compute the norm without clipping, or clip a pre-computed norm without recomputing it |
| Ad-hoc "run Adam for N epochs then switch to L-BFGS" scripts in PINN tutorials/community code | The spec's own explicit plateau-detector handoff (`d(log10 L_phys)/d(epoch)` slope test) | N/A — this project always specified the slope-based handoff, but community PINN code (verified via web search) commonly hardcodes a fixed epoch count instead | Fixed-epoch handoffs are simpler but do not adapt to per-run training-speed variance; the spec's criterion is the intentionally more robust choice already locked by CTX-46 |

**Deprecated/outdated:** none directly relevant — `torch.optim.LBFGS`, `clip_grad_norm_`, and `CosineAnnealingLR` are all current, unchanged, stable APIs in PyTorch 2.12.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Community-sourced characterization that "Adam-then-LBFGS with a correctly-wired closure is the standard PINN pattern, and a broken closure is a common community bug source" | State of the Art; Pitfall 2 framing | Low — used only as motivating background for why closure correctness is worth testing carefully; no numeric or structural claim rests on it |
| A2 | "Full-batch L-BFGS" (stages 0–2) operates on the SAME `build_stage_batch`-produced 256-trajectory `FixedBatch` used for that stage — not a separate query over the entire cumulative admitted population — because `pinn/data/batches.py` exposes no "whole corpus" query and its docstring frames Phase 40 as a caller of `build_stage_batch` | Architecture Patterns (system diagram); Pitfall 2 | Medium — if the intended reading is instead "literally the entire admitted Stage-≤k population" (a plain reading of `ctl_instruction.md`'s "the entire dataset"), the planner would need a NEW Phase-39-adjacent whole-corpus batch path that does not exist today, which is a scope question the discuss-phase pass did not surface. See Open Questions below — this is flagged for explicit planner decision, not silently assumed into the plan. |
| A3 | The L-BFGS closure's internal gradient-accumulation chunk size is left as an implementation default (not specified anywhere in CONTEXT.md/SPEC.md/framework specs) | Pitfall 2; Architecture Patterns | Low-Medium — any reasonable chunk size preserves correctness (it only trades wall-time/memory), but an unstated default risks silently reintroducing the 24GB-graph risk the ratified decision was meant to prevent if chosen too large (e.g., chunk size == full batch) |
| A4 | The adaptive collocation sampler's `last_residuals` argument shape (e.g., raw `(N_t,3,3)` residual tensor vs. a reduced per-point scalar magnitude) is unresolved by any source, since adaptive density strategies are deferred (PLAT-05) and TRAIN-04's AC only requires the hook to be *called* with `(model, last_residuals)` and to return the right count/bounds | Architecture Patterns; Phase Requirements table | Low — TRAIN-04's AC does not test the internal adaptive algorithm, only the interface; any consistent shape choice satisfies the locked AC |

## Open Questions

1. **What exactly does "full-batch" mean for the Stage 0–2 L-BFGS phase — the 256-trajectory `FixedBatch`, or the entire cumulative admitted Stage-≤k population?**
   - What we know: `ctl_instruction.md` says "Use standard full-batch on the entire dataset" for stages 0–2; the ratified D5-a rationale explicitly worries about "a literal full-batch second-order graph over the cumulative stage-2 set" exceeding 24 GB, which reads as concern about the full admitted population, not merely the 256-trajectory Adam sample. But the ONLY batch-construction interface Phase 39 built (`build_stage_batch`) always draws the fixed 240-replay + 16-lookahead sample; there is no "give me every admitted Stage-≤k trajectory" query anywhere in `pinn/data/`.
   - What's unclear: whether Phase 40 is expected to build a new whole-corpus batch path (expanding scope into data-layer territory that 40-SPEC.md's boundaries assign to Phase 39, which is closed) or whether "full-batch" is meant relative to the later-stage stochastic mini-batch size of 32 (i.e., "full" = the existing 256-trajectory batch, treated as one batch rather than sub-batched to 32).
   - Recommendation: the planner should treat the 256-trajectory `FixedBatch` as the L-BFGS full batch (reusing `build_stage_batch` unchanged, drawn once and held fixed for the whole L-BFGS phase) — this keeps Phase 40 inside its stated boundary ("Two-phase Adam→L-BFGS closure loop... Stage 0–2 full-batch path only", not a new data-layer feature) and is consistent with the closed Phase-39 interface. If this reading is wrong, it is a scope question significant enough to route through the project's gap-surfacing convention before planning proceeds, since it would require new Phase-39-adjacent code the phase boundary explicitly excludes.

2. **Gradient-accumulation chunk size for "accumulate-in-closure"**
   - What we know: the concern is peak second-order-autograd memory on a single M5 Pro (24 GB unified memory); the mechanism (accumulate gradients across `.backward()` calls without intervening `zero_grad()`) is a standard, verified PyTorch pattern.
   - What's unclear: no source specifies a chunk size (e.g., "process 512 collocation points per closure sub-pass").
   - Recommendation: expose it as a config knob with a conservative default (e.g., process the data-fidelity and collocation point sets in fixed-size sub-chunks of a few hundred points each) and record the choice as a CTX-level decision at plan time, since Phase 43's smoke test (ACC-02) is exactly the mechanism designed to reveal if the default is too slow or still memory-risky.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| PyTorch | All of TRAIN-01..07 | ✓ | 2.12.1 (confirmed via `conda run -n pinn-train python -c "import torch; print(torch.__version__)"`) | — |
| MPS backend | fp32-MPS production runtime (D1-p resolved) | ✓ | `torch.backends.mps.is_available() == True` | fp64-CPU escape hatch already exists (`resolve_runtime`) |
| `pinn-train` conda env | Test execution (`tests/phase40`) | ✓ | Miniforge3 arm64, confirmed working from Phase 37 | — |
| `unittest` (stdlib) | Test framework | ✓ | Python 3.11 stdlib | — |
| `pytest` | N/A | ✗ (not installed, not required) | — | Not needed — Phase 37/38/39 convention is stdlib `unittest` only |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none — everything Phase 40 needs is already present and verified.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | stdlib `unittest` (no `pytest`) |
| Config file | none — `unittest discover` |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase40 -p 'test_*.py' -v` |
| Full suite command | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -p 'test_*.py' -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TRAIN-01 | Forced ADVANCE -> Δstage=+1; forced HALT -> Δstage=0 | unit | `python -m unittest tests.phase40.test_controllers -v` | ❌ Wave 0 |
| TRAIN-02 | Handoff fires only after ≥50 flat-slope epochs; λ frozen + no clip during L-BFGS | unit | `python -m unittest tests.phase40.test_optimizer_phase -v` | ❌ Wave 0 |
| TRAIN-03 | Warmup length, `λ_E<=1`, freeze, re-warm at boundary | unit | `python -m unittest tests.phase40.test_scheduled_weights -v` | ❌ Wave 0 |
| TRAIN-04 | Uniform/adaptive count + bounds + hook signature | unit | `python -m unittest tests.phase40.test_collocation_sampler -v` | ❌ Wave 0 |
| TRAIN-05 | Clip formula per stage (incl. partial-window backstop); Adam-only spy | unit | `python -m unittest tests.phase40.test_grad_clip -v` | ❌ Wave 0 |
| TRAIN-06 | Four-criterion conjunction; RECOVER; HALT; no fallback advance | unit | `python -m unittest tests.phase40.test_stage_exit -v` | ❌ Wave 0 |
| TRAIN-07 | Typed refusal for stage ≥3; accept {0,1,2} | unit | `python -m unittest tests.phase40.test_slbfgs_preflight -v` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** the targeted test module for that task, paired with `tests.phase40.test_prohibitions` (Phase 38/39 convention: every production-module change re-runs the prohibitions audit).
- **Per wave merge:** `python -m unittest discover -s tests/phase40 -p 'test_*.py' -v`.
- **Phase gate:** full suite (`tests/` discover) green before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] `tests/phase40/__init__.py` — package marker
- [ ] `tests/phase40/_fixtures.py` — stub model (a tiny `nn.Module` or the real `build_network` on a minimal `ArchitectureSpec`) + stub `StageQuery`/batch source, mirroring `tests/phase39/_fixtures.py`
- [ ] All eight test files listed in Recommended Project Structure above — none exist yet
- [ ] `tests/phase40/test_prohibitions.py` — extend the Phase 38/39 AST/discovery audit to `pinn/training/*.py` (no v1.3 imports, no hardcoded precision/device, no corpus-path access)
- [ ] Framework install: none — `unittest` is stdlib, already available

## Security Domain

This is a local, single-machine ML training pipeline (no network listener, no multi-tenant surface, no authentication boundary). Most ASVS categories are not applicable; the two genuinely relevant surfaces are config-value validation and checkpoint deserialization.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — local CLI/script execution only |
| V3 Session Management | No | No sessions |
| V4 Access Control | No | Single-user local process |
| V5 Input Validation | Yes | `TrainingConfig` nested frozen dataclasses validate at construction (CTX-42), matching the established `ArchitectureSpec`/`RuntimeSpec` fail-closed pattern — reject out-of-contract values (negative epoch counts, non-finite thresholds) before any tensor is built |
| V5.5 Deserialization Prevention | Yes | `CheckpointStore`'s `torch.save`/`torch.load` round-trip must use `weights_only=True`-compatible payloads (plain tensors/containers/scalars per CTX-44) so a future `torch.load` call can safely pass `weights_only=True`; this is directly why CTX-44 requires `state_dict()`/`load_state_dict()` composition instead of pickling arbitrary Python objects |
| V6 Cryptography | No | No secrets/credentials in this phase's scope |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Arbitrary code execution via unpickled checkpoint payload (`torch.load` without `weights_only`) | Tampering / Elevation of Privilege | CTX-44's plain-tensor/scalar `state_dict` composition is exactly the discipline that makes a future `weights_only=True` load safe; do not serialize arbitrary Python objects (callables, custom classes without registered safe globals) into checkpoints |
| NaN/Inf gradient poisoning a run silently (e.g., a pathological close-encounter sample) | Denial of Service (of the training run) | RECOVER path (TRAIN-06) + `clip_grad_norm_(error_if_nonfinite=True)` fail-loud detection, matching the codebase's established "refuse rather than emit a passing/silent result" discipline (`pinn/physics_residual.py`'s non-finite refusal) |
| Malformed/adversarial config values (e.g., negative `MAX_EPOCHS`, zero `history_size`) silently accepted | Tampering | Frozen-dataclass `__post_init__` validation at construction, matching `LossWeights`'/`ArchitectureSpec`'s existing fail-closed pattern |

## Sources

### Primary (HIGH confidence)
- `/websites/pytorch_2_12` (context7) — `torch.optim.LBFGS` closure contract and parameters, `torch.nn.utils.clip_grad_norm_` signature/return/`error_if_nonfinite`, `torch.median` even-length semantics, `torch.autograd.backward`'s `create_graph=True` reference-cycle warning, gradient-accumulation recipe (`notes/amp_examples.rst`)
- Direct reads of the existing codebase: `pinn/network.py`, `pinn/loss_catalog.py`, `pinn/physics_residual.py`, `pinn/runtime.py`, `pinn/constants.py`, `pinn/data/batches.py`, `pinn/data/types.py`, `tests/phase38/test_loss_catalog.py`
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (Phase 2a/2b, Stage Transition Criteria, Consolidated Hyperparameter Schedule sections, read in full) and `pinn_architecture.md` (§4.1 PHYS-05, §4.2 ALM ablation, §4.3 Two-Phase Optimization, §4.4 Adaptive Gradient Clipping, read in full)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` (D5-a/b/c, D7-b/c/d, B-1/3/4, U-5/6/7 sections, read directly)
- `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-CONTEXT.md` and `40-SPEC.md` (read in full)
- `.planning/phases/38-*/38-PATTERNS.md`, `.planning/phases/39-*/39-PATTERNS.md`, `38-06-SUMMARY.md`, `39-14-SUMMARY.md` (read in full)
- Direct shell verification: `conda run -n pinn-train python -c "import torch; print(torch.__version__); print(torch.backends.mps.is_available())"` -> `2.12.1` / `True`

### Secondary (MEDIUM confidence)
- Tavily web search cross-referencing community PINN Adam→L-BFGS practice (StackOverflow closure-bug thread, arXiv 2501.16371 optimizer survey) — used only as motivating background for Common Pitfalls, not as a source of any numeric or structural claim

### Tertiary (LOW confidence)
- None retained as load-bearing; all LOW-confidence findings were folded into the Assumptions Log with explicit risk framing rather than presented as fact

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages, versions verified directly against the running conda environment
- Architecture: HIGH for the parts locked by CONTEXT.md/SPEC.md; MEDIUM for the "accumulate-in-closure" full-batch sizing question, explicitly flagged as an Open Question rather than silently resolved
- Pitfalls: HIGH — every pitfall is either a direct codebase read or a claim verified against official PyTorch 2.12 documentation via context7

**Research date:** 2026-07-17
**Valid until:** 30 days (stable PyTorch API surface; the framework-spec/CONTEXT.md grounding does not expire until the milestone re-adjudicates it)
