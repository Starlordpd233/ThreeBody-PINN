# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) — Specification

**Created:** 2026-07-16
**Ambiguity score:** 0.13 (gate: ≤ 0.20)
**Requirements:** 7 locked (TRAIN-01..07)

## Goal

A `CurriculumController` / `RunController` trainer runs the Stage-0 curriculum end-to-end — the two-phase Adam→L-BFGS closure loop with PHYS-05 scheduled weights, the collocation sampler, merged gradient clipping (LOOP-04), and the ADVANCE/RECOVER/HALT stage-exit machine (CURR-03) — implementing the locked `ctl_instruction.md` Stage-0 contract **without re-deciding it**.

## Background

The v2.0 viability slice builds the CTL-PINN training stack from the authoritative framework specs (the `pinn/` live-code ban is lifted for FUT-01/FUT-04). The substrate this phase consumes already exists:

- **Phase 38 (FUT-01, model)** landed `pinn/network.py` (SQR-SkipResNet-SIREN, 14→256×12→9), `pinn/architecture_spec.py` (frozen `ArchitectureSpec`), `pinn/com_projection.py` (mass-weighted COM head), `pinn/physics_residual.py` (PHYS-02 componentwise AD), `pinn/loss_catalog.py` (five-term Huber catalog), `pinn/runtime.py`, and the `pinn/verification/` probes (gradcheck / residual-on-ground-truth / overfit). Phase 38 is held open only on GAP-38-01 (real-trajectory evidence DEFERRED); the model code itself is built.
- **Phase 39 (data)** landed `pinn/data/adapter.py` (`AdmittedSetAdapter`, D3-C in-memory fp32, `n_snapshots`/`dt_out` metadata), `pinn/data/batches.py` (replay/lookahead two-point-set constructor, LOOP-01/02/03), `pinn/data/splits.py` (stage-stratified split), and `pinn/data/stage_scan.py` (Stage-0 population scan, DATA-06). Phase 39 is closed (27/27 UAT).

What does **not** exist today: any training driver. There is no outer curriculum loop, no inner two-phase optimization loop, no scheduled-weight module wiring PHYS-05 into the step, no stateful collocation sampler, no merged gradient clip, and no stage-exit state machine. Phase 40 builds exactly that driver layer on top of the Phase-38 model and Phase-39 batches, transcribing the `ctl_instruction.md` Stage-0 contract (Phase 2a Adam exploration → Phase 2b full-batch L-BFGS refinement; CURR-03 stage transitions) into runnable, numerically-checkable behavior.

The v2.0 slice is Stage-0-first, single M5 Pro, in-memory, manual rollback (`pinn-train` env, fp32-MPS per the D1-p ruling). Stages 3–6 (stochastic L-BFGS) are explicitly out of the slice and must be refused, not silently skipped.

## Requirements

1. **Curriculum/Run controller structure (TRAIN-01)**
   - Current: No `CurriculumController` or `RunController` exists. The Phase-38 model and Phase-39 batch source have no driver that wires them into an outer curriculum / inner optimization loop.
   - Target: A training module under `pinn/` exposes a `CurriculumController` (outer: stage progression + stage-exit decisions) and a `RunController` (inner: per-stage two-phase optimization) that drive Stage 0 from the Phase-39 batches through the Phase-38 model, implementing the `ctl_instruction.md` Stage-0 contract rather than re-deciding it.
   - Acceptance: A dataset-free `tests/phase40` unittest (deferred-import skip guard, Phase 37/38/39 pattern) constructs both controllers against the frozen `ArchitectureSpec` and a stub batch source, and confirms: injecting a forced ADVANCE signal advances the outer loop by exactly one stage boundary (Δstage = +1); injecting a forced HALT signal leaves the stage unchanged (Δstage = 0).

2. **Two-phase Adam→L-BFGS closure (TRAIN-02)**
   - Current: No optimizer loop exists. The contract specifies Adam (per-stage LR `LR_k = 1e-3 × (0.7)^k`, cosine annealing, β=(0.9, 0.999), ε=1e-8, Adam-state reset at each stage boundary) → plateau handoff (`d(log10 L_phys)/d(epoch) > −5e-3` for 50 consecutive epochs) → full-batch L-BFGS (history size 10, Wolfe line search, max-iter 20–50) via accumulate-in-closure; λ frozen and no clipping during L-BFGS.
   - Target: Each stage runs Adam with PHYS-05 warmup until the plateau-handoff criterion is met, then switches to full-batch L-BFGS via accumulate-in-closure, with λ frozen and no gradient clipping applied during the L-BFGS phase.
   - Acceptance: A dataset-free test injects loss curves and asserts (a) the Adam→L-BFGS handoff fires only after ≥50 epochs of slope `> −5e-3` (flat curve → handoff at epoch ≥50; descending curve → no handoff), and (b) across the L-BFGS phase a spy confirms the scheduled λ is frozen (λ_entry == λ_exit to floating tolerance) and the clip path is not taken.

3. **PHYS-05 scheduled loss-weight module (TRAIN-03)**
   - Current: `pinn/loss_catalog.py` computes the five-term loss but applies no warmup/λ schedule. The contract (PHYS-05 / LOSS-02): warmup `I_warm = min(2000, 0.1·N_Adam,k)`; per-stage `λ^max` with `λ_E^max ≤ 1`; λ frozen during L-BFGS; re-warmed at stage boundaries; schedule state serialized into checkpoints.
   - Target: A scheduled loss-weight module implements the PHYS-05 schedule — warmup length `min(2000, 0.1·N_Adam,k)`, per-stage `λ^max` caps with `λ_E^max ≤ 1`, frozen-during-L-BFGS, re-warm at stage boundaries — and exposes its state for checkpoint serialization.
   - Acceptance: A dataset-free test drives the module through one stage and asserts (a) warmup length `== min(2000, 0.1·N_Adam)` steps, (b) `λ_E ≤ 1.0` at every sampled step, (c) λ frozen (entry == exit) across a simulated L-BFGS phase, (d) re-warm fires at a stage boundary (λ returns to the warmup schedule).

4. **Collocation sampler interface (TRAIN-04)**
   - Current: `pinn/data/batches.py` emits the data-fidelity + collocation point sets, but there is no stateful collocation sampler with the `(model, last_residuals)` adaptive hook signature (LOOP-03 / D5-b).
   - Target: A collocation sampler interface (uniform + spec-adaptive) with the stateful `(model, last_residuals)` hook signature supplies interior collocation points for the physics loss term.
   - Acceptance: A dataset-free test constructs the sampler, calls it with a stub `(model, last_residuals)`, and asserts (a) uniform mode returns exactly N points all within `[0, T]`, (b) adaptive mode invokes the hook with the `(model, last_residuals)` signature and returns exactly N points within `[0, T]`, (c) the returned count equals the configured budget.

5. **Merged gradient clipping (TRAIN-05)**
   - Current: No gradient clipping exists in any trainer. The contract (LOOP-04 / B-1 / AC-LOOP-04): during Adam only, the global L2 norm is clipped to `clip_value = C_stage · median(grad_norm_history)` over a rolling window, with the per-stage C-table (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0); no clipping during L-BFGS.
   - Target: Merged gradient clipping applies `clip_value = C_stage · median(grad_norm_history)` with the per-stage C-table and a rolling window, during Adam only; no clipping during L-BFGS.
   - Acceptance: A dataset-free test injects a known grad-norm history and asserts (a) the computed clip value equals `C_stage · median(history)` to floating tolerance for each stage `k ∈ {0..6}` with `C_stage ∈ {8.5, 8.5, 5.0, 5.0, 3.0, 3.0, 3.0}`, and (b) a spy confirms the clip is applied during the Adam step and is NOT applied during the L-BFGS step (clip-call count = 1 in Adam, 0 in L-BFGS).

6. **ADVANCE/RECOVER/HALT stage-exit machine (TRAIN-06)**
   - Current: No stage-exit state machine exists. The contract (CURR-03 / D4-c / R-1/R-2): ADVANCE is the only path to the next stage and requires the four-criterion success gate (training-loss plateau + validation-loss stability + `ε_phys` + `ε_energy`) on a held-out validation set; RECOVER rolls back to the last checkpoint on NaN/Inf gradients with a bounded retry budget (default `recover.retries: 0`); HALT/REVIEW surfaces max-epoch/stagnation for owner review. There is no fallback advancement. All thresholds are provisional pending the Phase-43 Stage-0 pilot calibration.
   - Target: The stage-exit state machine implements ADVANCE (four-criterion conjunction), RECOVER (NaN/Inf rollback with bounded retries, default 0), and HALT/REVIEW (max-epoch/stagnation → owner review), with no fallback advancement; thresholds are owner-ratified provisional placeholders, not invented values.
   - Acceptance: A dataset-free test injects signals and asserts (a) ADVANCE fires only when all four gate criteria pass (any one failing → not ADVANCE), (b) a NaN/Inf gradient triggers RECOVER rollback to the last checkpoint and, with `recover.retries: 0`, transitions to HALT/REVIEW after the single attempt, (c) reaching max-epoch without the gate transitions to HALT/REVIEW. The gate is exercised on its *form* (all four criteria evaluated); no calibrated pass threshold is asserted.

7. **sL-BFGS preflight refusal (TRAIN-07)**
   - Current: No preflight exists. The contract routes stages 3–6 to stochastic L-BFGS, which is not implemented in the v2.0 slice (deferred PLAT-02).
   - Target: A preflight check refuses to enter the stochastic-L-BFGS stages (3–6) with a typed error (not a silent science deviation) until a concrete sL-BFGS implementation exists.
   - Acceptance: A dataset-free test asserts requesting a stage `≥ 3` raises a typed refusal exception with a non-empty message, and requesting a stage in `{0, 1, 2}` does not raise.

## Boundaries

**In scope:**
- `CurriculumController` / `RunController` driver pair (a training module under `pinn/`)
- Two-phase Adam→L-BFGS closure loop, Stage 0–2 full-batch path only
- PHYS-05 scheduled loss-weight module (warmup, per-stage λ^max caps, frozen-during-L-BFGS, re-warm)
- Collocation sampler interface (uniform + spec-adaptive, stateful `(model, last_residuals)` hook)
- Merged gradient clipping (LOOP-04 C-table, Adam-only)
- ADVANCE/RECOVER/HALT stage-exit machine (gate *form*; provisional thresholds)
- sL-BFGS preflight typed refusal
- Dataset-free `tests/phase40` unittest contract (deferred-import skip guards)

**Out of scope:**
- Config / checkpoint / resume / determinism (Phase 41, CTRL-01..08) — the loop *consumes* a config object and *can* be checkpointed, but the keyed-YAML, atomic-checkpoint, promotion, `--hold-stage` rollback, and full seed/RNG-recording contracts are Phase 41.
- Operator runbook / monitoring surface (Phase 42, OPS-01..06) — the canonical JSONL/TensorBoard field set, `runs/<name>/` contract, and written runbook are Phase 42; Phase 40 logs only what the loop needs to operate.
- Verification / smoke test / Stage-0 pilot / acceptance verdict (Phase 43, ACC-01..06) — the `verify` ladder, `evaluate` gate rendering, seed-band pilot, and go/adjust/rethink verdict are Phase 43.
- Stochastic-L-BFGS implementation for stages 3–6 — deferred PLAT-02; Phase 40 only *refuses* it.
- Full multi-stage curriculum beyond the Stage 0–2 full-batch path — deferred PLAT-01.
- Calibrated threshold values (`ε_phys`, `ε_energy`, `ε_plateau`, MAX_EPOCHS, stagnation windows) — provisional pending the Phase-43 Stage-0 pilot calibration; Phase 40 uses owner-ratified placeholders and implements the gate *form*, not calibrated pass levels.

## Constraints

- **Stage-0–only viability slice**: single M5 Pro, fp32-MPS (D1-p ruling), in-memory data via the Phase-39 adapter, manual rollback.
- **Numerically-defined acceptance** per requirement (probe / count / observed behavior / floating tolerance), per the v2.0 verification protocol (ROADMAP) — no prose-only criteria.
- **Implements, does not re-decide**: the locked v1.4/v1.5/v1.6 framework-spec outcomes are hard constraints the trainer consumes — 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-02 AD contract, PHYS-03 softening `eps_soft = 1e-5`, PHYS-05 schedule, the post-v1.3 SCS gate (`ε_H > 1e-5` / `SCS > −5`), raw-mass `D ≈ 4.6416`, and the LOOP-01..04 batch/clip contracts.
- **C-table provenance note**: REQUIREMENTS TRAIN-05 locks `C_stage` for stages 0–1 at **8.5**; `ctl_instruction.md` (AC-LOOP-04) specifies the early-stage value as a **7–10 range** left open for calibration. The v2.0 requirement narrows the range to 8.5 for this slice (trainex-r1a-ratified); the planner should preserve 8.5 as the Stage-0 default and keep the 7–10 range visible as the spec provenance.
- **Test substrate**: conda env `pinn-train`, stdlib `unittest` (not pytest), `tests/phase40` deferred-import skip guards — matching the Phase 37/38/39 pattern.
- **Depends on**: Phase 38 (model) and Phase 39 (data adapter + batches).

## Acceptance Criteria

- [ ] `CurriculumController` + `RunController` exist under `pinn/` and drive Stage 0 from Phase-39 batches through the Phase-38 model; forced-ADVANCE advances Δstage = +1 and forced-HALT yields Δstage = 0 (TRAIN-01).
- [ ] Adam→L-BFGS handoff fires only after ≥50 epochs of physics-loss slope `> −5e-3`; during L-BFGS λ is frozen (entry == exit) and no clip is applied (TRAIN-02).
- [ ] PHYS-05 schedule module produces warmup length `min(2000, 0.1·N_Adam)`, `λ_E ≤ 1.0` at all steps, frozen λ across L-BFGS, and re-warm at a stage boundary (TRAIN-03).
- [ ] Collocation sampler returns exactly N points in `[0, T]` in both uniform and adaptive modes, with adaptive mode invoking the `(model, last_residuals)` hook (TRAIN-04).
- [ ] Gradient clip value equals `C_stage · median(grad_norm_history)` per stage `k ∈ {0..6}` (C ∈ {8.5, 8.5, 5.0, 5.0, 3.0, 3.0, 3.0}); clip applied in Adam, not in L-BFGS (TRAIN-05).
- [ ] Stage-exit machine ADVANCEs only on all four gate criteria; NaN/Inf → RECOVER rollback → HALT/REVIEW at `recover.retries: 0`; max-epoch without gate → HALT/REVIEW; no fallback advancement (TRAIN-06).
- [ ] Requesting stage ≥ 3 raises a typed sL-BFGS refusal with a non-empty message; stages {0,1,2} are accepted (TRAIN-07).

## Edge Coverage

**Coverage:** 5/5 applicable edges resolved · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| Stage-0 cold start (no k−1 model) | R1, R2 | ✅ covered | AC: at k=0 no prior-model load occurs; Adam state initialized fresh (spec: reset Adam buffers at each new stage). |
| Final stage (`has_stage(k+1)` false) | R1 | ✅ covered | Phase-39 `batches.py` already emits replay-only (`B_lookahead = 0`); trainer consumes it unchanged (LOOP-01 GAP-34-01 Option A). |
| NaN/Inf during L-BFGS (not just Adam) | R6 | ✅ covered | AC: NaN/Inf → RECOVER rollback regardless of phase; L-BFGS line-search failure routes to RECOVER, not silent advance. |
| Retry budget exhausted | R6 | ✅ covered | AC: `recover.retries: 0` → single attempt → HALT/REVIEW (never ADVANCE). |
| Empty / stale grad-norm history window | R5 | 🧪 backstop | Median-over-empty-window is a real edge (spec routes the bootstrap median fallback to FUT calibration). Held-out test: the clip must be defined and finite for a window with fewer than the rolling-length entries — carried into plan-phase `must_haves` as a backstop test. |

`--auto` resolution log: 4 covered (defensible acceptance criterion written into AC), 1 backstop (no calibrated fallback value may be invented — held-out edge test instead), 0 dismissed.

## Prohibitions (must-NOT)

**Coverage:** 5/5 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT auto-advance past a failed success gate (no fallback advancement) | R6 | resolved / test | Negative test: max-epoch / NaN-with-retries-0 / any-gate-fail must NOT produce ADVANCE. Contract: CURR-03. |
| MUST NOT silently enter the sL-BFGS stages (3–6) | R7 | resolved / test | Typed-refusal test (R7 AC). A silent skip or no-op pass-through fails the phase. |
| MUST NOT apply gradient clipping during L-BFGS | R2, R5 | resolved / test | Spy asserts clip-call count = 0 during L-BFGS (R2/R5 AC). |
| MUST NOT update λ (or dual variables) during an L-BFGS line search | R2, R3 | resolved / test | λ_entry == λ_exit across L-BFGS (R2/R3 AC). |
| MUST NOT invent calibrated threshold values or re-decide the locked framework specs | R6 (all) | resolved / judgment | The trainer transcribes the contract; `ε_phys`/`ε_energy`/`ε_plateau`/MAX_EPOCHS are owner-ratified provisional placeholders, and the locked v1.4/v1.5/v1.6 spec outcomes are consumed unchanged. Routes to judgment review (no mechanical check for "did not invent"). |

`--auto` resolution log: 4 resolved/test (mechanically checkable negatives), 1 resolved/judgment (the "do not invent / do not re-decide" governance prohibition is real but not mechanically checkable — routes to judgment review). 0 dismissed, 0 unresolved. Canon items (deterministic seeding, numeric safety) are not minted here: full seed/RNG recording is Phase 41 (CTRL); fp32 numeric safety is owned by the Phase-38 model + D1-p ruling.

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                              |
|--------------------|-------|------|--------|--------------------------------------------------------------------|
| Goal Clarity       | 0.90  | 0.75 | ✓      | Stage-0 end-to-end trainer; contract-defined, not re-decided.      |
| Boundary Clarity   | 0.90  | 0.70 | ✓      | Stage-0–2 only; explicit out-of-scope (Phases 41/42/43, sL-BFGS, multi-stage). |
| Constraint Clarity | 0.82  | 0.65 | ✓      | Numerically-defined acceptance; thresholds provisional-by-design; C-table 8.5 vs spec 7–10 noted. |
| Acceptance Criteria| 0.85  | 0.70 | ✓      | 7 requirements × concrete checks (counts, tolerances, state transitions). |
| **Ambiguity**      | 0.13  | ≤0.20| ✓      |                                                                    |

## Interview Log

`--auto` mode: no interactive interview. Initial ambiguity assessed at 0.13 (≤ 0.20, all minimums met) from ROADMAP Phase 40 + REQUIREMENTS TRAIN-01..07 + the `ctl_instruction.md` Stage-0 contract, so the SPEC was derived directly from existing context per the workflow's `--auto` short-circuit.

| Round | Perspective     | Question summary                                              | Decision locked (auto-selected) |
|-------|-----------------|---------------------------------------------------------------|---------------------------------|
| —     | Researcher      | What exists for the training loop today?                      | Phase-38 model + Phase-39 data substrate exist; no driver. |
| —     | Simplifier      | What is the irreducible Stage-0 core?                         | Adam→L-BFGS closure + PHYS-05 + clip + ADVANCE/RECOVER/HALT + sL-BFGS refusal. |
| —     | Boundary Keeper | What is NOT Phase 40?                                         | Config/checkpoint/determinism (41), runbook/monitoring (42), verify/pilot (43), sL-BFGS impl, multi-stage. |
| —     | Failure Analyst | What breaks the requirements?                                 | Cold-start k=0, NaN-in-L-BFGS, retry exhaustion, empty clip window → covered/backstop above. |

---

*Phase: 40-stage-0-curriculum-training-loop-fut-04*
*Spec created: 2026-07-16*
*Next step: /gsd-discuss-phase 40 — implementation decisions (controller internals, optimizer wiring, checkpoint seam for Phase 41, logging seam for Phase 42). SPEC requirements are locked; discuss-phase focuses on HOW.*
