# Phase 38: PINN Model Rebuild from Specs (FUT-01) — Specification

**Created:** 2026-07-12
**Ambiguity score:** 0.13 (gate: ≤ 0.20)
**Requirements:** 5 locked

## Goal

`pinn/` carries a spec-faithful model — the SQR-SkipResNet-SIREN network with the hard mass-weighted COM projection head, PHYS-02 autograd physics residuals, and the locked five-term loss catalog — rebuilt from `ctl_instruction.md` / `pinn_architecture.md` (not the v1.3-era code), and proven correct by the gradcheck, residual-on-ground-truth, and single-trajectory-overfit rungs before it feeds any training run.

## Background

Phase 37 delivered the verified substrate: the `pinn-train` env (Python 3.11.15, PyTorch 2.12.1 + MPS), the `pinn/runtime.py` `resolve_runtime` precision/device seam (ENV-04, no defaults encoded), and the §10.3 componentwise-AD dual-arm probe in `pinn/verification/componentwise_ad.py`. The owner recorded the D1-p branch **fp32-MPS** (`precision=float32, device=mps`; fp64-CPU is the in-framework escape hatch) on 2026-07-12 (GAP-37-01 `RESOLVED-WITH-INSTRUCTION`), unblocking this phase.

What does NOT exist: a spec-faithful model. `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` are v1.3-era reference-only files, superseded by the locked specs and replaced by this rebuild (the `pinn/` live-code ban is lifted for v2.0; those files are NOT grounding). There is no network module matching the locked architecture, no COM projection head, no PHYS-02 residual module, and no five-term loss catalog. Phase 38 builds them from the two authoritative grounding sources: the locked framework specs (`pinn_architecture.md` §2.3/§2.4 architecture, §3 loss terms, §4.1 PHYS-05 weights, §5.3.1 PHYS-02 AD contract; `ctl_instruction.md` loss-function contract) and the ratified trainex-r1a decision set (§5 pre-flight rungs 2–4).

## Requirements

1. **Network architecture (NET-01)**: The rebuilt `pinn/` package carries the SQR-SkipResNet-SIREN backbone — 14-dim input `[τ, IC₁₃]` → 12 hidden layers × 256 → 9-dim output, SIREN `first_omega_0=30.0` / `hidden_omega_0=1.0`, skip connections + LayerNorm (`elementwise_affine=False`) on odd layers — instantiated from a config-supplied architecture spec.
   - Current: Only the v1.3-era `basic_architecture.py` exists (reference-only, not spec-faithful, not grounding); no spec-derived model module.
   - Target: A new model module built from `pinn_architecture.md` §2.3/§2.4, instantiated from a config-supplied architecture block, running identically under both `resolve_runtime` branches (fp32-MPS / fp64-CPU).
   - Acceptance: A structure test confirms the exact topology (14→256 input layer, 12 hidden 256×256 layers, 256→9 output), the SIREN ω values, and LayerNorm placement/affine setting; instantiation from the same config + seed is deterministic and side-effect-free; a forward pass succeeds under both precision branches.

2. **COM projection head (NET-02)**: The hard mass-weighted COM projection head is applied to the 9-dim output before any loss or metric consumes it.
   - Current: Does not exist.
   - Target: A projection component subtracting the mass-weighted center of mass from the predicted positions, wired so that no loss or metric code path can consume the unprojected output (v1.4 D-02 locked).
   - Acceptance: For arbitrary network outputs and admitted-set masses, the projected positions satisfy `Σ mᵢ·rᵢ′ = 0` within dtype-appropriate tolerance; the projection is idempotent (projecting an already-projected output is a no-op within tolerance); a test confirms losses/metrics receive only projected output.

3. **Autograd physics residuals (NET-03)**: Physics residuals are computed by autograd per the PHYS-02 AD contract — componentwise second derivatives w.r.t. the autograd leaf `u`, with chain-rule factors `d²r′/du² = 4·d²r′/dτ²`, `dr′/du = 2·dr′/dτ`, and PHYS-03 softening `eps_soft = 1e-5` — validated by an fp64-CPU `gradcheck` and a residual-on-ground-truth probe.
   - Current: The §10.3 dual-arm AD probe (`pinn/verification/componentwise_ad.py`) exercises the AD patterns on a synthetic trajectory; no residual module computing Newtonian residuals exists.
   - Target: A physics-residual module implementing the PHYS-02 contract against the locked equations of motion in the shared dimensionless system, consuming the projected output of R2.
   - Acceptance: `torch.autograd.gradcheck` passes on the residual computation under the fp64-CPU branch; the residual-on-ground-truth probe evaluates residuals on a Brutus ground-truth trajectory and exits PASS against its documented threshold, with measured values recorded as evidence.

4. **Five-term loss catalog (NET-04)**: The loss is the locked five-term catalog — data Huber (`δ_r = 1`) on Brutus snapshots, IC squared-error anchors, causally-weighted physics residual, soft-energy Huber (`δ = 1.0`), componentwise angular-momentum Huber (`δ = 1.0`) — evaluated under supplied PHYS-05 scheduled weights in the shared dimensionless system (`t_τ ∈ [-1,1]`, `r′ = r/D`, raw-mass `D ≈ 4.6416`), per `pinn_architecture.md` §3/§4.1 and the `ctl_instruction.md` loss-function contract.
   - Current: Does not exist.
   - Target: A loss module implementing all five terms with the locked δ values, causal weighting (owner-ratified D-04 Option A mode), and dimensionless conversions; it consumes a supplied loss-weight vector (the PHYS-05 *scheduler* that produces that vector over training is Phase 40 / TRAIN-03).
   - Acceptance: Each of the five terms evaluates finite on a synthetic batch under both precision branches; term-level unit tests confirm the locked δ values, the causal-weight application, and the `D ≈ 4.6416` / `t_τ` conversions against spec formulas; the total is a weighted sum under a supplied λ vector.

5. **Single-trajectory overfit probe (NET-05)**: A single-trajectory overfit probe drives the data loss to near-zero, confirming model + AD + loss are wired correctly end-to-end.
   - Current: Does not exist.
   - Target: A probe (trainex-r1a §5 pre-flight rung 4) that overfits one admitted trajectory using the R1–R4 stack and records the loss trajectory as evidence.
   - Acceptance: The probe reduces the data loss by at least 10³× from its initial value to a recorded floor (the falsifiable operationalization of "near-zero"; exact floor recorded in evidence) and exits PASS/FAIL accordingly.

## Boundaries

**In scope:**
- The rebuilt spec-faithful `pinn/` model package: network module (SQR-SkipResNet-SIREN), COM projection head, PHYS-02 physics-residual module, five-term loss catalog.
- A config-supplied architecture spec (the architecture block consumed at instantiation); precision/device resolved through the existing `resolve_runtime` seam.
- The three proof rungs for this phase: fp64-CPU `gradcheck`, residual-on-ground-truth probe, single-trajectory overfit probe — with recorded evidence and tests following the `tests/phase37` pattern.
- A minimal probe-local trajectory fixture loader — just enough to feed rungs 3–4 with one Brutus trajectory. It is NOT the Phase 39 adapter (no Step-1A gate, no splits, no batch construction).

**Out of scope:**
- Data ingestion: the in-memory admitted-set adapter, Step-1A admission gate, `data_version_hash` refusal, split manifest, replay/lookahead batch constructor, Thrust-A scan — Phase 39 (DATA-01..06).
- The training loop: `CurriculumController`/`RunController`, Adam→L-BFGS, the PHYS-05 scheduled-weight *module* (warmup state machine + checkpoint serialization), collocation sampler, gradient clipping, stage-exit machine — Phase 40 (TRAIN-01..07). Phase 38's loss consumes a supplied weight vector.
- Config/checkpointing/resume/guards/determinism — Phase 41 (CTRL-01..08).
- Operator runbook and monitoring — Phase 42 (OPS-01..06); packaging the rungs into the `verify` ladder, the smoke test, and the Stage-0 pilot — Phase 43 (ACC-01..06).
- Editing the framework specs — SCOPE-18: build-discovered spec defects are surfaced as gaps and routed to a spec milestone, never fixed here.
- Deleting the v1.3-era reference files (`basic_architecture.py`, `data-processing-pipeline-full.py`, `data-handling/`) — they remain in place as reference-only; retirement is a later cleanup decision, not this phase's.
- Multi-stage curriculum, stochastic-L-BFGS, RAD collocation, streaming residency — deferred (PLAT-01..07).

## Constraints

- **Precision/device flow only through `resolve_runtime`** (ENV-04): production default is the owner-recorded D1-p branch fp32-MPS (`precision=float32, device=mps`); fp64-CPU is the in-framework escape hatch; the `gradcheck` rung runs fp64-CPU by contract. No `pinn/` module encodes a precision default (CTX-14).
- **Read-only grounding**: `ctl_instruction.md` / `pinn_architecture.md` are authoritative read-only inputs (SCOPE-18/21); the ratified trainex-r1a decision set is authoritative for build-engineering; v1.3-era `pinn/` code is reference-only, never grounding.
- **Locked science constants** (SCOPE-12): dimensionless system `t_τ ∈ [-1,1]`, `r′ = r/D`, raw-mass `D ≈ 4.6416`; PHYS-03 softening `eps_soft = 1e-5`; SIREN ω values; Huber δ values per the loss contract.
- **Single M5 Pro** (SCOPE-20): no cloud/distributed; MPS discipline per Phase 37 (`PYTORCH_ENABLE_MPS_FALLBACK` unset in probes that certify MPS behavior).
- **Probe tolerances**: where trainex-r1a §5 leaves a rung tolerance numerically open, plan-phase fixes the value and records the rationale (informed by the R-6 dual-arm tolerance framing, ~1e-4 fp32-vs-fp64 relative); these are build-engineering values, not owner-carved seams.
- **Git protocol**: one atomic commit per plan via `scripts/agent-commit`; no protected-branch push; work on `milestone/v2.0` in `.worktrees/trainex`.

## Acceptance Criteria

- [ ] A structure test confirms the instantiated model's exact topology (14→256; 12 hidden 256×256; 256→9), `first_omega_0=30.0` / `hidden_omega_0=1.0`, and LayerNorm (`elementwise_affine=False`) on odd layers with skip connections, per `pinn_architecture.md` §2.3/§2.4.
- [ ] The model instantiates and completes a forward pass under both `resolve_runtime` branches (fp32-MPS and fp64-CPU) through the same code path.
- [ ] Instantiation from the same config + seed yields identical parameters, and performs no filesystem or global-state writes (edge: R1 concurrency/re-entry).
- [ ] Projected outputs satisfy `Σ mᵢ·rᵢ′ = 0` within dtype tolerance; the projection is idempotent (edge: R2); a test proves no loss/metric consumes unprojected output.
- [ ] `torch.autograd.gradcheck` passes on the physics-residual computation under fp64-CPU.
- [ ] The residual-on-ground-truth probe runs on a Brutus trajectory and exits PASS against its documented threshold, with the threshold and measured values recorded as evidence.
- [ ] All five loss terms evaluate finite on a synthetic batch; term-level tests confirm δ values, causal weighting, and dimensionless conversions (`D ≈ 4.6416`).
- [ ] The single-trajectory overfit probe reduces data loss ≥ 10³× from its initial value and records the achieved floor as evidence.
- [ ] MUST NOT: `ctl_instruction.md` / `pinn_architecture.md` are byte-identical before and after every Phase 38 commit.
- [ ] MUST NOT: no `pinn/` module hard-codes precision/device or encodes a precision default outside the config→`resolve_runtime` seam.
- [ ] MUST NOT: no implementation code is derived from the v1.3-era `pinn/` files (spec-derived only).
- [ ] MUST NOT: no Phase 38 code or probe writes under `simulation_data/`.

## Edge Coverage

**Coverage:** 2/5 applicable edges resolved · 3 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| concurrency | R1 | ✅ covered | AC #3: deterministic seeded instantiation, no side effects — safe under re-entry/parallel instantiation |
| concurrency | R2 | ✅ covered | AC #4: projection is a pure, idempotent function (double-projection is a fixed point) |
| unclassified | R3 | ⚠ UNRESOLVED | No shape cue (#1110). Candidate edge for planner: gradcheck/residual behavior at softening-active (near-collision) points — planner must treat as assumption |
| unclassified | R4 | ⚠ UNRESOLVED | No shape cue (#1110). Candidate edge for planner: Huber transition at `|x| = δ` and causal-weight extremes (`w_n → 0`) — planner must treat as assumption |
| unclassified | R5 | ⚠ UNRESOLVED | No shape cue (#1110). Candidate edge for planner: overfit non-convergence/divergence detection (probe must FAIL loudly, not hang) — planner must treat as assumption |

[`--auto` never auto-backstops an unclassified row: a missing shape cue is not evidence an edge exists. The three unresolved rows are flagged planner assumptions, not held-out test obligations.]

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT edit `ctl_instruction.md` / `pinn_architecture.md` (spec defects → gap register, routed to a spec milestone) | R1–R5 | resolved | verification: test (no wired check captured — descriptor left empty per `--auto`; mechanical byte-identity check is plan-phase's to wire) |
| MUST NOT derive implementation from the v1.3-era `pinn/` files (`basic_architecture.py`, `data-processing-pipeline-full.py`) | R1–R4 | resolved | verification: judgment (spec-faithfulness review; v1.3 code is reference-only, never grounding) |
| MUST NOT hard-code precision/device or encode a precision default outside the config→`resolve_runtime` seam (CTX-14 / ENV-04) | R1, R3, R4 | resolved | verification: judgment (code review: dtype/device always flow from resolved runtime) |
| MUST NOT write under `simulation_data/` from any Phase 38 code or probe | R3, R5 | resolved | verification: test (no wired check captured — descriptor left empty per `--auto`) |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                              |
|--------------------|-------|------|--------|-----------------------------------------------------|
| Goal Clarity       | 0.90  | 0.75 | ✓      | Spec-faithful rebuild proven by 3 named rungs       |
| Boundary Clarity   | 0.85  | 0.70 | ✓      | Phase 39/40 seams + SCOPE-18/20/21 explicit         |
| Constraint Clarity | 0.85  | 0.65 | ✓      | Locked constants, precision seam, read-only specs   |
| Acceptance Criteria| 0.85  | 0.70 | ✓      | 12 pass/fail criteria (8 positive + 4 negative)     |
| **Ambiguity**      | 0.13  | ≤0.20| ✓      | Gate passed on initial assessment (no interview)    |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 0 | (auto — no interview) | Initial assessment from ROADMAP + REQUIREMENTS scored 0.13 ≤ 0.20 with all minimums met | SPEC derived directly from the roadmap phase entry, NET-01..05, STATE.md decisions (D1-p fp32-MPS; integrity-r2 clearance), and Phase 37 artifacts |

`--auto` decisions logged:
- **Probe data source**: rungs 3–4 use a minimal probe-local fixture loader for one Brutus trajectory, NOT the Phase 39 adapter — Phase 39 is roadmap-independent of Phase 38, so Phase 38 cannot depend on its adapter.
- **"Near-zero" operationalized**: NET-05's "near-zero" is specified as ≥ 10³× data-loss reduction with the achieved floor recorded — falsifiable, while leaving the exact floor as recorded evidence rather than an invented ratified constant.
- **PHYS-05 boundary**: the loss catalog consumes a *supplied* λ weight vector; the scheduled-weight module (warmup state machine, checkpoint serialization) is Phase 40 / TRAIN-03 per the roadmap.
- **v1.3 file retirement**: explicitly out of scope (kept reference-only); deletion is a later cleanup decision.
- Edge probe: 2 covered, 0 backstop, 3 unresolved (unclassified rows left unresolved per the #1110 `--auto` exception). Prohibition probe: 4 resolved, 0 unresolved, 0 dismissed.

---

*Phase: 38-pinn-model-rebuild-from-specs-fut-01*
*Spec created: 2026-07-12*
*Next step: /gsd-discuss-phase 38 — implementation decisions (module layout, config schema shape, probe CLI form, test organization)*
