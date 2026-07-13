---
phase: 38
reviewers: [claude-glm, claude-deepseek, grok, agy, claude-max, codex, claude-kimi]
rerun_reviewers: [claude-glm, claude-kimi]
reviewed_at: 2026-07-13T06:03:22Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T055421Z-31166
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 38

## claude-glm Review

_claude-glm failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=claude-glm
- exit_code=143
- elapsed_seconds=541
- timeout_seconds=540
- watchdog=triggered
- timeout_after_seconds=540
- command=ccp glm -p - 
- stdout_bytes=0
- stderr_bytes=192

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T055421Z-31166/xreview-claude-glm-38.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T055421Z-31166/xreview-claude-glm-38.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T055421Z-31166/xreview-claude-glm-38.meta

Stderr excerpt:
```
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors

```

---

## claude-deepseek Review


# Phase 38 Plan Review: PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Phase 38 delivers the spec-faithful `pinn/` model package — SQR-SkipResNet-SIREN network, COM projection head, PHYS-02 autograd physics residuals, and five-term loss catalog — proven by three named proof rungs (gradcheck, residual-on-ground-truth, single-trajectory overfit). The 6 plans span 18 tasks across 5 waves, covering 5 requirements (NET-01..05) with 12 acceptance criteria. Plans are TDD-structured, spec-grounded, and mechanically thorough. The phase boundary is well-defined against Phases 39–43.

**Overall scope alignment:** The plans directly address all 5 NET requirements and 12 SPEC acceptance criteria. No scope creep into data ingestion, training loop, config, or monitoring was observed. The prohibition enforcement plan (38-06) closes the two mechanical checks the SPEC left descriptor-empty.

## 2. Strengths

- **Exceptional spec-grounding.** Every module, constant, and test traces to specific framework-spec sections (`pinn_architecture.md` §2.x/§3.x/§5.3.1, `ctl_instruction.md` §2.5). The PHYS-02 chain-factor reconciliation in 38-03 is a model of careful source-treatment — it identifies an apparent contradiction between the SPEC phrasing and §5.3.1, and resolves it authoritatively from the spec.
- **Rigorous TDD discipline.** Every task pair is RED-test-first with deferred-import skip guards (mirroring Phase 37's `_load_*` pattern), so suites skip cleanly before modules exist rather than erroring. Test interfaces are specified before implementation actions.
- **Comprehensive prohibition enforcement.** Plan 38-06 wires all four SPEC must-NOTs as mechanical checks: spec sha256 byte-identity, no `simulation_data/` writes, AST-based no-precision-default scan, and AST-based no-v1.3-import scan — closing the two checks the SPEC `--auto` mode left descriptor-empty.
- **Well-surfaced edge cases.** The 3 unresolved SPEC edge rows (R3: softening-active points, R4: Huber transitions / causal-weight extremes, R5: overfit non-convergence) are explicitly admitted as planner assumptions with concrete handling strategies, not silently dropped.
- **Per-plan threat models.** Each plan carries a STRIDE register with disposition and mitigation, covering integrity, elevation, and denial-of-service threats specific to that wave's artifacts.
- **Correct parallelism analysis.** Wave 4 correctly identifies that 38-04 (probes) and 38-05 (loss catalog) both depend on 38-03 but not on each other, enabling parallel execution.

## 3. Concerns

### HIGH

**H1: No test for SIREN principled weight-initialization distribution.** Plan 38-02-02 specifies the SIREN principled init (first layer `U[-1/n_in, 1/n_in]`, hidden layers `U[-sqrt(6/n_in)/ω₀, +...]`), and 38-02-03 tests topology + deterministic seeded reproduction. However, no test verifies that initialized weights actually follow the specified distribution bounds. SIREN networks are notoriously sensitive to init — Kaiming or Xavier init substituted for the SIREN-specific uniform init would silently produce a trainable-looking network that converges poorly or not at all. A distribution-sampling test (instantiate N times with different seeds, verify weight statistics fall within the expected bounds) would close this gap. **Impact:** Silent training failure downstream in Phase 40.

**H2: Overfit probe default `--max-steps 3000` is uncalibrated.** The SPEC requires `≥ 10³×` data-loss reduction. The plan fixes 3000 as the default step cap, acknowledging it as a build-engineering value with no empirical basis. If 3000 is too low, the probe FAILs on a correctly-wired stack; if too high, it wastes time. The `--max-steps` override mitigates this, but the first operator invocation is likely to hit the default. **Mitigation exists** (the override), but the uncalibrated default risks a false-FAIL verdict on the first run.

**H3: `soft_energy_loss` `eps_H` denominator source unspecified for Phase 38 probes.** Plan 38-05-02 states `eps_H` is a "SUPPLIED metadata scalar (not recomputed per minibatch)." The overfit probe (38-06) consumes the loss catalog and needs to supply this value, but Phase 38 has no config system (Phase 41) and no mechanism for deriving `|H₀|` from the loaded trajectory. The probe would naturally compute it from the trajectory's t=0 state, but this integration step is not described in either 38-05 or 38-06. **Impact:** Implementation ambiguity — the overfit probe executor must invent the derivation, risking inconsistency with Phase 40's config-derived value.

### MEDIUM

**M1: Residual probe's finite-difference acceleration computation undescribed.** Plan 38-04-02 says the residual probe computes "Newtonian residual `‖f_i‖ = ‖a'_fd − Σ F_ij‖` using a finite-difference acceleration on the dense trajectory" as a diagnostic. The fixture loader parses positions and velocities from Brutus output (format: `m x y z vx vy vz`), which has no acceleration field. Finite-difference acceleration from velocity data requires a differentiation scheme that is not specified (central differences? forward/backward at endpoints? what order?). This is recorded as diagnostic-only (not the PASS gate), so the risk is limited to evidence quality.

**M2: Fixture loader folder mapping lacks cross-reference to canonical dataset rules.** Plan 38-03's `<default_trajectory>` section manually encodes the variant→folder mapping. The `.claude/rules/dataset-reference.md` rule file (if it exists) would be the canonical source for this mapping. The plan should reference that rule or the `simulation_data/Documentation/README.md` File Naming Conventions section as the authority, rather than inlining the mapping.

**M3: `LossWeights` excludes data-term weight but this asymmetry is unremarked.** Plan 38-05-01 defines `LossWeights` with fields `lambda_ic, lambda_phys, lambda_e, lambda_l` — no `lambda_data`. The SPEC says data term is unweighted per `pinn_architecture.md` §3.1, and the composer hardcodes `L_data` (no coefficient). This is correct per spec but creates an asymmetry: Phase 40's PHYS-05 scheduler produces a 5-field weight vector but Phase 38's container has 4 fields. If Phase 40 expects a 5-field container, this becomes a silent mismatch. The plan would benefit from an explicit note that the data weight is fixed at 1.0 and why.

### LOW

**L1: Plan 38-01-03 hardcodes `power_p != 2` as a validation error.** The validation rejects any `power_p` value other than 2. This is consistent with the locked ARCH-02 spec, but prevents the `ArchitectureSpec` from being reused if a future experiment explores power values. Minor — the spec is locked.

**L2: Plans reference Phase 37 SUMMARY.md files that don't exist yet.** Plans 38-02 through 38-06 list `38-0X-SUMMARY.md` in their context blocks. These files won't exist until the prior wave's execution completes. This is normal for sequential planning but means an executor must validate file existence before importing context. The executor workflow should handle this gracefully.

**L3: `componentwise_du` uses `torch.func.jacrev` — PyTorch 2.12 compatibility.** `torch.func` was stabilized in PyTorch 2.0 but the `jacrev` API surface has evolved. The Phase 37 probe (`componentwise_ad.py`) already uses these patterns successfully, so this is low risk, but the plan doesn't note the API version dependency.

## 4. Suggestions

1. **Add a SIREN init-distribution test** to 38-02-03 or 38-02-02: instantiate the network N times with different seeds, collect weight statistics, assert they fall within the principled-init uniform bounds. This is a one-test addition that catches the most dangerous silent failure mode in SIREN networks.

2. **Document the `eps_H` derivation path** in 38-06-01: specify that the overfit probe computes `|H₀|` from the trajectory's t=0 state (positions, velocities, masses) via the matched-Plummer Hamiltonian and supplies it to `soft_energy_loss`. This closes the integration ambiguity.

3. **Run a one-shot calibration of `--max-steps`** before the first operator invocation: execute the overfit probe on a synthetic fixture with a generous step budget (e.g., 10000), observe the actual convergence step count, and set the default to 2–3× that value. Record the calibration in evidence.

4. **Cross-reference `simulation_data/Documentation/README.md`** in 38-03's `<default_trajectory>` as the authoritative source for the folder mapping, rather than inlining it.

5. **Add an explicit note** in 38-05-01 that `LossWeights` has 4 fields because the data term is fixed at λ=1.0 per §3.1, and that Phase 40's scheduler must account for this when producing its 5-value vector.

## 5. Overall Risk: **MEDIUM**

The plans are thorough, well-grounded, and structurally sound. The 18 tasks correctly decompose the 5 requirements with clean wave parallelism. All 12 acceptance criteria have corresponding tests or probes, and the 4 prohibitions get mechanical enforcement. The HIGH concerns are real but narrow — each is a single-test or single-documentation gap, not a structural plan defect. The missing SIREN init test is the most consequential: wrong init silently poisons every downstream physics check. With that gap closed and the `eps_H` integration path specified, these plans are ready for execution.

---

## grok Review


I'll review Phase 38 by reading the six plan files first, then pull CONTEXT/SPEC only where needed to verify concerns.

---

## agy Review


# Cross-AI Plan Review: Phase 38

## 1. Summary
The Phase 38 plans provide a highly detailed, mechanically verified roadmap for rebuilding the PINN model from specs. The architecture, physics residuals, loss catalog, and probes are well-scoped. However, there is a critical task dependency ordering flaw that will break automated execution across almost all plans.

## 2. Strengths
- **Strict Read-Only & Purity Discipline:** The plans enforce idempotency, read-only dataset access, and explicitly disallow global state mutation (e.g., `set_default_dtype`).
- **Mechanical Prohibition Checks:** Using AST-level checks to prevent precision hardcoding and legacy v1.3 imports is a robust way to ensure compliance without manual review.
- **Fail-Loud Edge Case Handling:** Requirements for failing on `NaN/Inf` or non-convergence (instead of hanging) show excellent foresight into automated verification risks.

## 3. Concerns
- **[HIGH] TDD Task Dependency Ordering:** In plans 38-02 through 38-06, the implementation tasks (Tasks 01 and 02) are ordered *before* the test-authoring task (Task 03). However, Tasks 01 and 02 are marked `tdd="true"` and their `<verify>` blocks run the test suites (e.g., `conda run ... python -m unittest tests.phase38.test_com_projection`). Automated execution will fail on Task 01 because the test files do not exist yet. Plan 38-01 correctly authors tests in Task 01; the others regress.
- **[MEDIUM] Missing Path Traversal Sanitization:** In 38-03-01, `fixture_loader.py` uses the user-provided `variant` and `id` to construct dataset paths. The plan does not explicitly require sanitizing these inputs (e.g., against `../` path traversal), which could allow arbitrary reads outside `simulation_data/`.
- **[LOW] Underspecified Min-Separation Filter:** In 38-04-02, the residual probe is supposed to exclude "softening-active near-collision points", but the exact implementation of the pairwise separation filter (and what the default `--min-separation-guard` value should be) is left vague, potentially leading to inconsistent implementations.

## 4. Suggestions
- **Reorder Tasks:** Move the test-authoring task (currently Task 03) to be Task 01 in plans `38-02-PLAN.md`, `38-03-PLAN.md`, `38-04-PLAN.md`, `38-05-PLAN.md`, and `38-06-PLAN.md` to ensure the TDD workflow has test files available for the `<verify>` steps.
- **Add Validation:** Explicitly specify that `resolve_trajectory_path` must validate `variant` and `id` (e.g., using a strict regex for alphanumeric and underscores) to prevent path traversal.
- **Specify Default Guard:** Define a concrete default value for `--min-separation-guard` in 38-04 so the residual probe's fallback behavior is deterministic.

## 5. Overall Risk
**HIGH** (Automated execution will reliably fail at 38-02-01 due to the `ModuleNotFoundError` / missing test suite dependency).

---

## claude-max Review


I have read all six plan files, the SPEC, the CONTEXT, and verified the key physics claim against the authoritative spec §5.3.1. Below is the review.

---

# Phase 38 Plan Review — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Six wave-ordered plans rebuild the spec-faithful `pinn/` model from `pinn_architecture.md`/`ctl_instruction.md`: a locked-constants + architecture-spec substrate (01), the SQR-SkipResNet-SIREN network + COM head (02), the PHYS-02 residual + read-only fixture loader (03), the gradcheck/residual probes (04), the five-term loss catalog (05), and the overfit probe + phase-wide prohibition checks (06). The plans are unusually disciplined: per-constant spec citations, mechanical byte-identity/no-write/AST prohibition gates, non-overwriting timestamped evidence, and transparently surfaced planner assumptions. Scope is clean — every modified file is under `pinn/` or `tests/phase38/`; no spec, dataset, or v1.3-file edits. Wave dependencies (1→2→3→{4,4}→5) are correct and file-disjoint, so waves 4a/4b parallelize safely. The plans do achieve the phase goal, with the reservations below.

## 2. Strengths

- **Chain-factor discrepancy caught, not silently applied.** SPEC NET-03 literally states `dr'/du = 2·dr'/dτ`, `d²r'/du² = 4·d²r'/dτ²`. Plan 03 correctly reconciles this against the authoritative §5.3.1 (verified: "differentiating w.r.t. `u` … with no chain factor; the factors 2 and 4 apply only to a direct `τ = 2u−1` leaf") and guards it with a symbolic-oracle test on the §5.3.1 worked example. This is exactly the right grounding behavior.
- **Locked constants centralized and cited**, with `D = 6.694` explicitly barred as a selectable value (SCOPE-12).
- **Structural, not conventional, no-unprojected-consumption guarantee** (projected output is the only public `forward` return; raw tensor via named test hook).
- **Falsifiable probes** with PASS/FAIL exit codes, mutated-input negative tests, and recorded measured-vs-threshold evidence.
- **Prohibition checks are mechanical and data-driven** (iterate the full new-module list, so a new module is auto-covered).

## 3. Concerns

**HIGH — none blocking; the items below are worth resolving before execution.**

**MEDIUM**

- **[Coverage] No rung gates the actual "residual-on-ground-truth" (plan 04).** Rung 3's PASS gate is force-energy *self-consistency* (`−∇V_eps == ΣF_ij`), a math identity true by construction and computable on synthetic fixtures. Because both sides scale together, it is **blind to shared errors in `D`, mass convention, or `eps_soft`**. The genuine scientific check — does a real Brutus trajectory nearly satisfy the softened EOM — is relegated to a *non-gating diagnostic*. Net: a systematically mis-scaled physics wiring could pass all three rungs. Partially mitigated by `test_constants`/`test_loss_catalog` asserting `D≈4.6416`, but the phase goal ("proven correct … before it feeds any training run") implies rung 3 should have teeth on the ground-truth residual. Recommend documenting an expected pass/fail band on the real-trajectory Newtonian residual, or explicitly justifying diagnostic-only status.
- **[Correctness] COM-head mass provenance inside `forward()` is ambiguous (plan 02).** The projection needs *raw* masses, but IC₁₃'s mass slots are `tanh`-normalized in the network input (per `.claude/rules/pinn-reference.md`), so raw masses cannot be recovered from `forward(tau_ic13)` alone. The action hedges — "masses supplied per forward call or via the spec's fixed 3-body layout" — which conflicts with NET-01's `forward(tau_ic13)` signature. The equal-mass default trajectory (1,1,1) masks this; hierarchical (unequal-mass) trajectories would expose a wrong projection. Pin the `forward` masses interface explicitly.
- **[Ordering] Within-plan TDD/verify sequencing is inconsistent in plans 02, 04, 06.** Implementation tasks are marked `tdd=true` and their `<verify>` runs `tests.phase38.test_*`, but the test modules are authored in the *last* task of each plan (e.g. 38-02-03 writes `test_com_projection` after 38-02-01/02 already verify against it). As written, those verify commands error ("module not found") at task-completion time. Plan 01 does it correctly (tests first). Recommend reordering 02/04/06 to author tests first, matching 01.

**LOW**

- **SPEC NET-03 wording is misleading.** An executor reading only the SPEC (not plan 03's `planner_assumptions`) could apply the 2/4 factors literally. The phase SPEC is editable — correct the text to match §5.3.1.
- **NET-05 "end-to-end" is slightly overstated (plan 06).** The overfit rung drives the **DATA term only**; it does not exercise the PHYS-02/AD path or the other four loss terms, though it claims to overfit "using the R1–R4 stack." AD is covered separately by gradcheck. Reword the claim or route physics through the overfit.
- **Spec byte-identity baseline hardcodes sha256 digests in the committed test (plan 06).** Correct for detecting Phase 38 edits, but a legitimate spec change in a later milestone breaks this phase-scoped test. Acceptable; note the maintenance coupling.
- **fp32-MPS paths skip when MPS is unavailable.** The production-default branch may be unverified in non-MPS CI; relies on the operator running on the M5 Pro. Acceptable given SCOPE-20, but the in-worktree suite does not certify the production path.

## 4. Suggestions

1. Give rung 3 a documented pass/fail band on the real-trajectory Newtonian residual (or state explicitly why it is diagnostic-only), so a shared-scaling error is catchable.
2. Fix the `forward()` mass interface: specify raw masses as an explicit argument to `forward`/`project_com`, and add a projection test with **unequal** (hierarchical) masses, not just (1,1,1).
3. Reorder tasks in 02/04/06 to author the test suite first (as 01 does), so every `tdd=true` verify has a target.
4. Correct SPEC NET-03's chain-factor sentence to match §5.3.1.
5. Add a numerical test that the odd-layer update actually computes `SIREN(x) + LayerNorm(x)^p` (not just that a LayerNorm module is present on odd layers).

## 5. Overall Risk

**LOW–MEDIUM.** The plans are rigorous, well-grounded, and scope-clean, and will produce a spec-faithful model. The MEDIUM items are correctness/coverage refinements (rung-3 gate teeth, `forward` mass provenance) and a mechanical ordering fix, all resolvable without restructuring the phase. None threaten data integrity or introduce destructive operations — read-only discipline on specs and `simulation_data/` is enforced mechanically.

*Note: I did not read `AGENTS.md`, `PROJECT.md`, `REQUIREMENTS.md`, or `ROADMAP.md` in full — the SPEC/CONTEXT and the six plans were internally consistent and self-sufficient for these findings; the §5.3.1 chain-factor claim was verified directly against `pinn_architecture.md`. No files were edited.*

---

## codex Review


## 1. Summary

Phase 38 plans are thorough and mostly well sequenced. I could read all requested phase plan/support files. The main risk is that several checks can pass on synthetic or internal-consistency paths while the phase goal requires stronger proof of spec-faithful real-trajectory behavior.

## 2. Strengths

- Clear six-step dependency chain from constants/spec dataclass to network, residuals, loss catalog, and probes.
- Strong scope boundaries against Phase 39/40 data ingestion and training-loop work.
- Good prohibition coverage: no spec edits, no `simulation_data/` writes, no precision defaults, no v1.3 implementation derivation.
- TDD structure is explicit, with focused tests and evidence-writing requirements per rung.
- Planner assumptions are surfaced instead of hidden, especially for softening, Huber/causal edges, and non-convergence.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

**HIGH — COM projection mass source is ambiguous.**  
[38-02-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-02-PLAN.md:144) leaves masses “supplied per forward call or via the spec’s fixed 3-body layout,” while the public model contract is `forward(tau_ic13)`. This is a core interface decision: masses should likely be extracted from the IC13 input, not separately supplied or assumed equal. If unresolved, hierarchical unequal-mass cases can pass structure tests while violating NET-02.

**HIGH — Rung 3 may not actually gate on ground-truth residual accuracy.**  
[38-SPEC.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-SPEC.md:32) requires a residual-on-ground-truth probe. But [38-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-04-PLAN.md:90) makes the PASS gate force-energy self-consistency, with real trajectory residual magnitude only diagnostic. That validates internal math consistency, not necessarily agreement with Brutus trajectory dynamics.

**MEDIUM — Rung 4 data-only overfit under-tests the claimed R1-R4 stack.**  
[38-06-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-06-PLAN.md:94) optimizes the DATA term only, while [38-SPEC.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-SPEC.md:39) frames the probe as confirming model + AD + loss wiring. A broken physics residual or non-data loss path could still pass the overfit probe.

**MEDIUM — Real-data proof depends on operator execution outside automated checks.**  
[38-03-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-03-PLAN.md:101) notes no Brutus payload exists in this worktree, so synthetic fixtures drive in-worktree checks. That is pragmatic, but the plans should make real-dataset evidence a phase-close gate, not an informal operator follow-up.

**LOW — Spec byte-identity checks land late.**  
[38-06-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-06-PLAN.md:46) adds the hash test in the final plan. Better to establish baseline hashes in 38-01 or require the check after each subplan so earlier accidental spec edits cannot slip into the baseline.

## 4. Suggestions

- Pin the model forward contract: `forward(tau_ic13)` should derive masses from IC13, with tests covering unequal masses.
- Split Rung 3 into two gates if needed: force-energy identity and real Brutus residual agreement. Do not let the identity check substitute for ground-truth validation.
- In Rung 4, either evaluate/record all five loss terms during overfit or narrow the claim to “data-path overfit” and rely on separate rungs for AD/physics.
- Add an explicit phase-close acceptance item: real recommended/default trajectory evidence must exist, or the phase remains blocked/deferred.
- Move prohibition/hash tests earlier and run them throughout the phase.

## 5. Overall Risk

**HIGH**. The plans are strong structurally, but as written they could pass while under-verifying the real-trajectory residual and full-stack loss/AD behavior that Phase 38 is meant to prove.

---

## claude-kimi Review

# Phase 38 Plan Review — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

The six plans (`38-01` through `38-06`) describe a coherent, TDD-driven rebuild of the PINN model package from the locked framework specs. They correctly inherit Phase 37's precision/device seam (`resolve_runtime`), reuse the `tests/phase37/` patterns (deferred-import guards, AST source inspection, evidence discipline), and keep the Phase 39/40/41 boundaries explicit. The wave ordering (constants/spec → network/COM → residual/loader → probes/loss → overfit/prohibitions) is largely sound, and the four SPEC prohibitions are wired into mechanical checks. Overall the plans should achieve the Phase 38 goal, but a few implementation ambiguities need clarification before execution.

## 2. Strengths

- **Spec-grounded, not v1.3-derived**: every plan cites `pinn_architecture.md` / `ctl_instruction.md` sections and treats v1.3-era files as reference-only.
- **TDD discipline**: RED tests are written before production modules (e.g., `38-01-01` before `38-01-02/03`), with deferred-import skip guards so suites stay green-before-implementation.
- **Precision/device hygiene**: explicit `dtype`/`device` passing, no `torch.set_default_dtype`, no availability probes, and a phase-wide AST check in `38-06`.
- **Mechanical prohibition enforcement**: spec byte-identity sha256 check, no-`simulation_data`/write check, no-precision-default AST check, and no-v1.3-import AST check.
- **Clear phase boundaries**: Phase 39 adapter, Phase 40 scheduler, Phase 41 YAML mapping, and Phase 43 verify ladder are all explicitly out of scope.
- **Fail-loud probe design**: NaN/Inf and max-step cap produce typed FAILs rather than hangs.

## 3. Concerns

### HIGH

- **H1 — COM projection mass source is ambiguous.** `38-02` says the projection head receives "masses supplied per forward call or via the spec's fixed 3-body layout," but `38-01` defines `ArchitectureSpec` with no mass field. The network `forward()` signature and the mass-weighted COM contract need a single decided source before `pinn/network.py` and `pinn/com_projection.py` are implemented; otherwise tests in `38-02-03` will disagree with the implementation.
- **H2 — Fixture-loader dataset mapping is unverified against real payload.** `38-03` documents a folder-to-variant mapping (`standard_quasi_random_gold_standard`, `hierarchical`, etc.), but the worktree has no Brutus payload. If the real folder names or file prefixes differ, rungs 3–4 will fail on the operator's first real run. The mapping is a planner assumption that should be validated or explicitly flagged as a pre-execution check.
- **H3 — Residual probe finite-difference acceleration is underspecified.** `38-04` says rung 3 will report a Newtonian residual diagnostic `||a'_fd - ΣF_ij||` using "a finite-difference acceleration on the dense trajectory." It does not state whether `a'_fd` comes from the Brutus velocity column, a second-difference of positions, or a derivative of the spline — each choice has different error and softening behavior. This could make the diagnostic non-reproducible.
- **H4 — Overfit step cap lacks empirical basis.** The default `--max-steps 3000` for a 12-layer SIREN overfit is a planner guess. If it is too low, the phase's acceptance gate (`L0/Lf ≥ 1e3`) may fail for reasons unrelated to wiring. A pre-flight calibration note or an adaptive cap-with-target would reduce this risk.

### MEDIUM

- **M1 — `LossWeights` field count is inconsistent with "five-field" label.** `38-05` describes a "five-field frozen named weights container" but defines only `lambda_ic`, `lambda_phys`, `lambda_e`, `lambda_l` (the data term is unweighted). This is terminologically confusing; the plan should call it a four-λ container for five terms.
- **M2 — `soft_energy_loss` signature is confusing.** The parameter `s_h_or_eps_h` in `38-05-02` is unclear. The plan states it is a supplied `eps_H` metadata scalar, so the name should reflect that.
- **M3 — Spec sha256 baselines are brittle.** `test_prohibitions.py` hardcodes digests for `ctl_instruction.md` and `pinn_architecture.md`. This correctly detects accidental Phase 38 edits, but any legitimate future spec-milestone update will break the test until the baseline is regenerated. Document the regeneration command in the test or plan.
- **M4 — Wave-4 parallelism may obscure ordering.** `38-04` and `38-05` are both wave 4 and depend on `38-03` and `38-02` respectively. They can run in parallel, but `38-06` depends on both. The plan should state explicitly that `38-04` and `38-05` are independent and can be executed in any order.

### LOW

- **L1 — No explicit check that `torch.optim.Adam` is available in the `pinn-train` env.** It almost certainly is, but a one-line verification in `38-06` would match the plan's otherwise thorough environmental discipline.
- **L2 — MPS-specific numerical behavior for `LayerNorm(...)**2` is not discussed.** Odd-layer SQR skips raise LayerNorm outputs to power `p=2`; MPS has historically had edge cases with `pow` on certain dtypes. A note to guard or test this under fp32-MPS would be prudent.
- **L3 — Fixture loader missing file-not-found / empty-file handling.** Beyond the completeness gate (`final_timestamp >= 9.5`), the loader should fail loudly if the resolved file does not exist or contains zero snapshots.

## 4. Suggestions

1. **Clarify the mass source for COM projection** in `38-02` before implementation: either add `masses` to `ArchitectureSpec`, or require `masses` as a `forward()` argument, and make the test suite assert the chosen contract.
2. **Validate or flag the dataset folder mapping** in `38-03` by adding a pre-execution checklist item: "operator confirms `simulation_data/Data/` folder names match the mapping before first real run."
3. **Specify the finite-difference method** in `38-04` (e.g., second-order central difference on positions, or direct use of Brutus velocities) so the residual diagnostic is reproducible.
4. **Rename `s_h_or_eps_h` to `eps_H`** and document that it is a supplied metadata scalar, not recomputed per minibatch.
5. **Add a dry-run calibration note** for the overfit step cap, or make `--max-steps` default clearly overrideable without code change.
6. **Document the sha256 baseline regeneration procedure** in `tests/phase38/test_prohibitions.py` or `38-06`.

## 5. Overall Risk

**MEDIUM**

The plans are well-scoped, spec-grounded, and mechanically sound. The MEDIUM/HIGH concerns are all clarifiable before code is written; none appear to invalidate the phase goal. The biggest execution risks are the unverified dataset folder mapping (H2) and the COM-head mass-source ambiguity (H1), both of which should be resolved in the next planning pass or at execution kickoff.

---

## Consensus Summary

Panel health: 5 of 7 real reviews (claude-deepseek, agy, claude-max, codex, claude-kimi). claude-glm timed out twice (watchdog 540 s, stub kept per one-retry rule). grok exited 0 but returned only a preamble sentence — no findings; treated as an empty review. claude-kimi succeeded on the subset rerun.

### Unresolved HIGH (consensus-judged, deduped)

1. **TDD/verify task-ordering incoherence in plans 38-02..38-06** (agy HIGH; claude-max MEDIUM; verified against all six plans). In each of 38-02/03/04/05/06 the implementation tasks are `tdd="true"` and their `<verify>` runs `tests.phase38.test_*` modules that are authored only in the plan's final task (e.g. 38-02-01 verifies `tests.phase38.test_com_projection`, written in 38-02-03). Plan 38-01 correctly authors tests first. As written, each earlier task's verify hits ModuleNotFoundError or forces the executor to author files owned by a later task. Fix: reorder (tests-first, matching 38-01) or re-scope the verify commands.
2. **COM projection mass provenance in `forward()` is unpinned** (codex HIGH; claude-kimi HIGH; claude-max MEDIUM). 38-02-02 hedges "masses supplied per forward call or via the spec's fixed 3-body layout" while the public contract is `forward(tau_ic13)`; raw masses are not recoverable from the tanh-normalized IC₁₃ slots, and equal-mass fixtures mask a wrong projection on hierarchical trajectories. Fix: pin the masses interface (explicit argument to `forward`/`build_network`) and add an unequal-mass projection test.
3. **Rung-3 PASS gate has no ground-truth teeth** (codex HIGH; claude-max MEDIUM). The gate is force-energy self-consistency (`-∇V_eps == ΣF_ij`, §10.4 `relative_error < 1e-5`) — a math identity blind to shared errors in D / mass convention / eps_soft; the real-trajectory Newtonian residual is diagnostic-only. Fix: add a documented pass/fail band on the real-trajectory residual (or an explicit in-plan justification for diagnostic-only status).
4. **SIREN principled-init distribution is implemented but never tested** (claude-deepseek HIGH). §2.2/Table (`pinn_architecture.md:983`) fixes the exact uniform bounds; 38-02 tests cover topology/omega/determinism but not init bounds. Wrong init silently degrades training. Fix: add an init-bounds statistics test to 38-02.

### Actionable non-HIGH (deduped; not yet incorporated in the plans)

- Overfit `--max-steps 3000` is uncalibrated (deepseek H2 + kimi H4, judged down: override + fail-loud + evidence already planned; add a calibration note or FAIL-retry guidance to 38-06-01).
- Rung-3 finite-difference acceleration diagnostic has no specified differencing scheme (deepseek M1, kimi H3; non-gating → judged MEDIUM; specify scheme in 38-04-02).
- Rung-4 claims "overfits using the R1–R4 stack"/end-to-end but optimizes the DATA term only (codex M, claude-max L; narrow the claim or evaluate/record all five terms during overfit).
- Real-dataset operator evidence is not an explicit phase-close gate (codex M; add an acceptance item in 38-06).
- Spec sha256 baseline provenance: digests recorded at wave-5 execution time could baseline an earlier accidental spec edit; regeneration procedure undocumented (codex L, kimi M3, claude-max L; pin digests to the pre-phase committed state in 38-06-02).
- `resolve_trajectory_path` input validation unstated — unknown variant / non-numeric id should raise typed errors (agy M).
- `--min-separation-guard` has no documented default value (agy L; 38-04).
- 38-05 naming/semantics: `LossWeights` labeled "five-field" but defines four λ fields; `s_h_or_eps_h` must be disambiguated — the spec (`pinn_architecture.md:531,542`) persists BOTH `S_H` and `ε_H = 1e-4·S_H` as metadata; state which is supplied and where the 1e-4 factor applies (deepseek M3, kimi M1+M2).

### Raised but judged resolved / not applicable

- deepseek H3 (overfit probe needs an `eps_H` derivation path): not applicable — 38-06-01 optimizes the DATA term only; `soft_energy_loss` is not on the overfit path.
- deepseek M2 (folder mapping lacks canonical cross-reference): already incorporated — 38-03-01 read_first cites `.claude/rules/dataset-reference.md` (exists) and the dataset README File Naming section.
- kimi H2 (dataset folder mapping unverified): mapping verified in-worktree against `simulation_data/Documentation/README.md:175-177,193,214-215` (gold folders keep base-prefix filenames; gold reads base IC folders per :155); plan already flags operator confirm-at-execution + fail-loud fallback.
- kimi M4 (wave-4 parallelism): encoded mechanically in frontmatter (`wave: 4`, disjoint `depends_on`/files).
- claude-max LOW (SPEC NET-03 chain-factor wording): the §5.3.1 reconciliation is already explicit in 38-03 `<planner_assumptions>` and verified against `pinn_architecture.md:890`; a SPEC text touch-up is optional.
- deepseek L1/L2/L3, kimi L1/L2/L3, claude-max LOW (fp32-MPS skip; accepted per SCOPE-20): excluded — no plan change needed.

## xreview Diagnostics

### claude-glm
- reviewer=claude-glm
- exit_code=143
- elapsed_seconds=541
- timeout_seconds=540
- watchdog=triggered
- timeout_after_seconds=540
- command=ccp glm -p - 
- stdout_bytes=0
- stderr_bytes=192

### claude-deepseek
- status: preserved from existing REVIEWS.md

### grok
- status: preserved from existing REVIEWS.md

### agy
- status: preserved from existing REVIEWS.md

### claude-max
- status: preserved from existing REVIEWS.md

### codex
- status: preserved from existing REVIEWS.md

### claude-kimi
- reviewer=claude-kimi
- exit_code=0
- elapsed_seconds=233
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp kimi -p - 
- stdout_bytes=6807
- stderr_bytes=192

## Verification coverage

Source-grounding pass over every symbol the six PLAN.md files cite as **already existing**. Authority: `grep` (`gsd-tools drift-guard authority --raw`). Severity mapping under this authority: VERIFIED → none, AMBIGUOUS → MEDIUM, UNCHECKABLE → INFO, MISSING → needs-acknowledgement; **hardBlock: false for every verdict below — no hard blocks**. Symbols the plans declare as new Phase 38 artifacts (`pinn/constants.py`, `pinn/architecture_spec.py` `ArchitectureSpec`, `pinn/network.py` `SQRSkipResNetSIREN`/`build_network`, `pinn/com_projection.py` `project_com`, `pinn/physics_residual.py` `physics_residual`/`softened_acceleration`/`componentwise_du`, `pinn/verification/fixture_loader.py` `load_trajectory`/`resolve_trajectory_path`/`sha256_file`/`TrajectoryFixture`, the three rung probes and their `main`/`run_*` entry points, `pinn/loss_catalog.py` `LossWeights`/`LossTerms`/five term callables/`compose_total`, all `tests/phase38/*` modules, the new-probe CLI flags `--precision`/`--device`/`--path`/`--variant`/`--id`/`--residual-threshold`/`--min-separation-guard`/`--max-steps`/`--evidence-root`, and the evidence directories) are excluded per the review contract.

### Existing files cited in plan context/read_first — all VERIFIED (exist on disk)

`pinn/runtime.py` · `pinn/__init__.py` · `pinn/verification/__init__.py` · `pinn/verification/componentwise_ad.py` · `scripts/run_precision_probe.py` · `tests/phase37/__init__.py` · `tests/phase37/test_runtime.py` · `tests/phase37/test_componentwise_ad.py` · `tests/phase37/test_precision_orchestrator.py` · `simulation_data/Documentation/README.md` · `.claude/rules/dataset-reference.md` · `.claude/rules/pinn-reference.md` · `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` · `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` · `pinn/basic_architecture.py` · `pinn/data-processing-pipeline-full.py` · `pinn/data-handling/` (all three v1.3 banned-reference targets exist) · `.planning/ROADMAP.md` · `.planning/REQUIREMENTS.md` · `.planning/STATE.md` · `38-SPEC.md` · `38-CONTEXT.md` · `38-PATTERNS.md` · `~/.claude-max/gsd-core/workflows/execute-plan.md` · `~/.claude-max/gsd-core/templates/summary.md`

### Code symbols in existing modules

| Symbol (plan citation) | Verdict | Evidence |
|---|---|---|
| `RuntimeSpec` frozen dataclass (cited runtime.py:23-38) | VERIFIED | `pinn/runtime.py:23-24` (`@dataclass(frozen=True)` / `class RuntimeSpec:`) |
| `resolve_runtime` + fail-closed validation (cited :84-95) | VERIFIED | `pinn/runtime.py:65` (def), `:85,:91` (`raise ValueError`) |
| `_ALLOWED_PROFILES` / `_ALLOWED_PAIR_DESCRIPTION` | VERIFIED | `pinn/runtime.py:44` / `:59` |
| `synthetic_trajectory` (cited componentwise_ad.py:62-76) | VERIFIED | `pinn/verification/componentwise_ad.py:62` |
| `AGGREGATE_CRITERION = 1e-6` (cited :113-118) | VERIFIED | `pinn/verification/componentwise_ad.py:113` |
| `torch.func.jacrev` usage (cited :128-157) | VERIFIED | `pinn/verification/componentwise_ad.py:131,139` |
| same-dtype/device `as_tensor` constants (cited :73-76) | VERIFIED | `pinn/verification/componentwise_ad.py:73-74` |
| non-finite refusal (cited :193-206) | VERIFIED | `pinn/verification/componentwise_ad.py:193-194` |
| argparse required `--precision`/`--device` (cited :371-394) | VERIFIED | `pinn/verification/componentwise_ad.py:376-377` |
| result-dict pattern (cited :215-229) | VERIFIED | `pinn/verification/componentwise_ad.py:215` |
| `PYTORCH_ENABLE_MPS_FALLBACK` pre-import capture (cited :30-41) | VERIFIED | `pinn/verification/componentwise_ad.py:31,37` |
| `_sha256_file` (cited run_precision_probe.py:109-113) | VERIFIED | `scripts/run_precision_probe.py:109` |
| `write_evidence_run` + `run_id` (cited :380-420/:390-420) | VERIFIED | `scripts/run_precision_probe.py:390,:395` |
| `_load_*` deferred-import guards | VERIFIED | `tests/phase37/test_runtime.py:14` (`_load_runtime`), `:28` (`_load_torch`) |
| frozen-dataclass assertion (cited test_runtime.py:66-73) | VERIFIED | `tests/phase37/test_runtime.py:66-69` |
| default-dtype invariance (cited :122-137) | VERIFIED | `tests/phase37/test_runtime.py:122-125` |
| AST executable-code technique (cited :139-183) | VERIFIED | `tests/phase37/test_runtime.py:146-157` (`import ast`, `ast.parse`, `ast.walk`) |
| `pinn/__init__.py` surface: `RuntimeSpec`/`resolve_runtime` only + "Phase 38" docstring note | VERIFIED | `pinn/__init__.py:5,18,20` |
| `pinn/verification/__init__.py` docstring ("belongs to Phase 38 and is not present") + `componentwise_ad` re-export | VERIFIED | `pinn/verification/__init__.py:5,8` |
| `tdd="true"` task semantics in executor workflow | VERIFIED | `~/.claude-max/gsd-core/workflows/execute-plan.md:191` |

### Framework-spec sections and locked values

| Claim (plan citation) | Verdict | Evidence |
|---|---|---|
| §5.3.1 PHYS-02: u leaf, NO chain factor; 2×/4× only on direct τ leaf; componentwise; `r.sum()` VJP forbidden | VERIFIED | `pinn_architecture.md:888-898` (contract text at :890) |
| §10.2 COM invariance `abs(COM) < 1e-10` | VERIFIED | `pinn_architecture.md:1021-1022` |
| §10.4 force-energy consistency `relative_error < 1e-5` | VERIFIED | `pinn_architecture.md:1031-1032` |
| §2.2 principled SIREN init: first `U[-1/n_in, 1/n_in]`, hidden `U[±sqrt(6/n_in)/hidden_omega_0]` | VERIFIED | `pinn_architecture.md:177,983` |
| §2.3 odd-layer update `x = f_sr(x_prev) + (LayerNorm(x_prev))^p`, p=2; even plain SIREN | VERIFIED | `pinn_architecture.md:205-207,981` |
| §2.4 Table 1: depth 12 / width 256 / LayerNorm `elementwise_affine=False, eps=1e-5` odd layers / `first_omega_0=30`, `hidden_omega_0=1` | VERIFIED | `pinn_architecture.md:248-251,259-261` |
| §3.1 data Huber `delta_r = 1`, data term unweighted | VERIFIED | `pinn_architecture.md:303-307` |
| §3.2 causal weights `w_1=1`, `w_n = exp(-eta_c Σ stopgrad(Rbar_m))`, `eta_c=1` (D-04 Option A owner-ratified), clip bound deferred to FUT | VERIFIED | `pinn_architecture.md:414,424,646` |
| §3.2/§3.4 training softening `ε_train = 1e-5` (plan names it `EPS_SOFT`) | VERIFIED | `pinn_architecture.md:379-381,403,516` |
| §3.3 IC anchor `β_v = 1`, `λ_IC = 1` | VERIFIED | `pinn_architecture.md:475-481` |
| §3.4 `ΔH_n = (H − H_0)/(|H_0| + ε_H)`; `ε_H = 1e-4·S_H`; both persisted as supplied training metadata (never recomputed/floored) | VERIFIED | `pinn_architecture.md:527,531,542` |
| §3.5 `ε_L = 1e-8`, componentwise angular-momentum Huber | VERIFIED | `pinn_architecture.md:615-616,991` |
| §5.3 Output Frame (COM head context) | VERIFIED | `pinn_architecture.md:847` |
| ctl §2.5 Global scaling: raw-mass `D = (G T²)^{1/3} ≈ 4.6416` canonical (PIPE-09); `6.694` mass-fraction form rejected, non-selectable; PHYS-03 additive-eps-on-norm anti-pattern prohibited | VERIFIED | `ctl_instruction.md:992,1005,1011,1024` |
| ctl "Phase 2: Total Training Loss" assembly | VERIFIED | `ctl_instruction.md:1744` |

### Dataset README claims (fixture-loader grounding)

| Claim | Verdict | Evidence |
|---|---|---|
| completeness gate: final timestep ≥ 9.5 | VERIFIED | `simulation_data/Documentation/README.md:526,553` |
| snapshot header `t N t_cpu` | VERIFIED | `README.md:257,262` |
| IC/body line `m x y z vx vy vz` | VERIFIED | `README.md:277` |
| folder mapping incl. gold folders; base-prefix filenames (`brutus_standard_XXXX.txt` in gold folders); gold reads base IC folders | VERIFIED | `README.md:102-104,151-155,175-177,193,200,214-215` |
| gold `dt_out = 0.01` density | VERIFIED | `README.md:180` |
| `Result:` footer optional / schema varies | VERIFIED | `README.md:267,283` |
| Mass Normalization (standard masses exactly (1,1,1)) | VERIFIED | `README.md:314` |

### Planning/requirement IDs

| ID | Verdict | Evidence |
|---|---|---|
| NET-01..NET-05 | VERIFIED | `.planning/REQUIREMENTS.md:40-44` |
| SCOPE-18 / SCOPE-20 | VERIFIED | `.planning/REQUIREMENTS.md:126,128` |
| SCOPE-12 | VERIFIED | referenced at `.planning/REQUIREMENTS.md:43`; defined in archived `.planning/milestones/v1.6-REQUIREMENTS.md:25`; substance (6.694 rejected) independently grounded at `ctl_instruction.md:1024` |
| CTX-14 / CTX-26 / CTX-32 (25 CTX refs total) | VERIFIED | `38-CONTEXT.md:114,132,162` |
| SPEC edge rows R3/R4/R5 marked UNRESOLVED (planner-assumption handling) | VERIFIED | `38-SPEC.md:93-95` |
| SPEC descriptor-empty prohibition rows (CTX-32 wiring target) | VERIFIED | `38-SPEC.md:105` |
| R-6 dual-arm tolerance framing | VERIFIED | `38-SPEC.md:67,173` |
| integrity-r2 PB-2 | VERIFIED | `.planning/REQUIREMENTS.md:43` |
| D-04 Option A (owner-ratified) | VERIFIED | `pinn_architecture.md:424` |

### UNCHECKABLE (severity INFO, hardBlock false — not treated as verified or missing)

| Symbol | Reason |
|---|---|
| conda env `pinn-train` (every plan `<verify>` command) | Environment state, not repo text; `conda` is not on this review session's PATH. In-repo references to prior successful use: Phase 37 plans/summaries/UAT (`.planning/phases/37-developer-environment-precision-adjudication/`). |
| `torch.autograd.gradcheck`, `torch.optim.Adam` | External PyTorch API; not import-verifiable without the env. `torch.func.jacrev` has in-repo working precedent (`componentwise_ad.py:139`). |
| `simulation_data/Data/brutus_output/...` payload files on disk | Declared absent by the plans themselves ("no Brutus trajectory payload exists in this worktree"); naming/mapping verified against the README text above. |

### Totals

VERIFIED: 60+ symbols/claims (all resolvable citations, including every quoted line-range). MISSING: 0. AMBIGUOUS: 0. UNCHECKABLE: 3 (all environment/runtime state, severity INFO). **No hardBlock findings.**
