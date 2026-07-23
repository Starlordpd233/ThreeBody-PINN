---
status: partial
phase: 38-pinn-model-rebuild-from-specs-fut-01
source: [38-01-SUMMARY.md, 38-02-SUMMARY.md, 38-03-SUMMARY.md, 38-04-SUMMARY.md, 38-05-SUMMARY.md, 38-06-SUMMARY.md]
started: 2026-07-13T13:04:33Z
updated: 2026-07-13T13:04:33Z
verifier: gsd-verify-work (agent-run automated verification; code phase, no manual-UI UAT)
---

## Current Test

[testing paused — 1 item outstanding: real admitted-Brutus rung 3/4 phase-close gate (GAP-38-01, DEFERRED)]

## Tests

### 1. NET-01 — SQR-SkipResNet-SIREN architecture matches locked spec
expected: 14→256 input, 12×256 hidden (6 odd SQR-Skip blocks + 6 plain SIREN), 256→9 head; SIREN first_omega_0=30.0 / hidden_omega_0=1.0; LayerNorm(elementwise_affine=False, eps=1e-5, power p=2) on odd layers; SIREN uniform init; instantiated from a config-supplied ArchitectureSpec; deterministic + side-effect-free; forward pass under both fp32-MPS and fp64-CPU.
result: pass
source: automated
evidence: tests/phase38/test_architecture_spec.py + test_network_structure.py green (part of 128 OK); ArchitectureSpec.__post_init__ raises on any wrong locked constant; adversarial spec audit FAITHFUL 8/8 (constants single-homed in pinn/constants.py; cited pinn_architecture.md §2.3/§2.4). Tests recompute the SIREN bound from the spec formula and reject a normal init (non-tautological).

### 2. NET-02 — hard mass-weighted COM projection head, projected-only output
expected: Σ mᵢ·rᵢ′ = 0 within dtype tolerance; projection idempotent; weights are raw ordered masses; no loss/metric can consume the unprojected 9-dim output.
result: pass
source: automated
evidence: tests/phase38/test_com_projection.py green (<1e-10 COM, idempotence, equal-vs-unequal-mass guard proving the weighting is applied); network.forward returns project_com(raw, masses) — raw reachable only via private _forward_unprojected; audit FAITHFUL (pinn_architecture.md §10.2).

### 3. NET-03a — physics residual + AD chain-rule + fp64-CPU gradcheck
expected: PHYS-02 u-leaf AD (d²r'/du² via jacrev∘jacrev, not the forbidden summed-output VJP); PHYS-03 eps_soft=1e-5 additive on the squared norm; torch.autograd.gradcheck PASS on fp64-CPU with non-loosened tolerances; evidence recorded.
result: pass
source: automated
evidence: evidence/gradcheck/20260713T121039Z/{summary.md,raw.json}: gradcheck_result=true (float64/cpu, eps=1e-6/atol=1e-5/rtol=1e-3, torch 2.12.1, no pre-import MPS fallback). Audit confirms the D³=G·T² raw-mass nondimensionalization makes the dimensionless residual unit-coefficient — the absence of any explicit D/T/2×/4× factor in physics_residual is CORRECT, not a missing factor; test_u_leaf_carries_no_manual_chain_factor proves the 2×/4× arise automatically via autograd.

### 4. NET-03b — residual-on-ground-truth dual-gate probe
expected: Gate A (autograd −∇V_ε/m vs direct softened force, <1e-5) and Gate B (u-leaf central-difference accel vs force, median <1e-1) both PASS on a ground-truth trajectory; thresholds physically meaningful, with mutation teeth.
result: pass
source: automated
evidence: tests/phase38/test_residual_probe.py green incl. dual-gate PASS + wrong-length-scale mutation FAIL (Gate B is the real D-convention anchor). NOTE: exercised on a SYNTHETIC fixture — proof on a real admitted-Brutus trajectory is test 8 (DEFERRED).

### 5. NET-04 — five-term loss catalog in the shared dimensionless system
expected: data Huber δ_r=1; IC squared-error (/3, β_v=1); causally-weighted physics residual (exclusive prefix-cumsum, stopgrad, η_c=1); soft-energy Huber δ=1 (matched Plummer, ε_train=1e-5, supplied ε_H); componentwise angular-momentum Huber δ=1 (ε_L=1e-8); dimensionless with raw-mass D≈4.6416 (mass-fraction D=6.694 rejected and absent); compose_total applies the SUPPLIED λ vector, λ_data≡1, and structurally forbids a 6th term.
result: pass
source: automated
evidence: tests/phase38/test_loss_catalog.py green (11); D pinned to 4.6416 AND "6.694" asserted absent in source (governance-clean, honors v1.5 EVID-10); audit FAITHFUL 8/8 (pinn_architecture.md §3.1–3.5 / §4.1 PHYS-05; ctl_instruction.md loss contract).

### 6. NET-05 — single-trajectory overfit probe drives data loss ≥10³×
expected: data loss reduced ≥1000× from its initial value to a recorded floor; real model+COM+AD+loss+Adam stack; fail-loud on NaN / cap-without-target / non-finite diagnostics.
result: pass
source: automated
evidence: observed live — L0≈0.18064 → Lf≈0.0001068, ratio≈1691 ≥ 1000 → PASS (gate uses min post-update data loss, so the ratio measures real optimization progress); tests/phase38/test_overfit_probe.py green incl. FAIL paths. NOTE: synthetic 2-snapshot fixture with IC13=zeros(13) placeholder (physically-normalized IC → Phase 39) and soft-energy term disabled unless --eps-h — documented NET-05 wiring-proof scoping, not a defect.

### 7. MUST-NOT prohibitions (4 negative acceptance criteria)
expected: ctl_instruction.md / pinn_architecture.md byte-identical before/after every commit; no pinn module hard-codes precision/device outside the config→resolve_runtime seam; no code derived from the v1.3-era pinn/ files; no Phase 38 code/probe writes under simulation_data/.
result: pass
source: automated
evidence: git clean on framework-specs (byte-identical since phase start); importing all pinn modules leaves torch default dtype float32 (no global-state mutation); tests/phase38/test_prohibitions.py green — endpoint sha256 + history-aware git-log for both specs, write-spy over I/O entry points, AST no-precision-default / no-v1.3-import over glob-discovered pinn/**/*.py.

### 8. Phase-close gate — real admitted-Brutus rung 3/4 evidence
expected: the residual-on-ground-truth and overfit probes run on ONE real admitted Brutus trajectory (real tol / Lw / dt_out provenance), with evidence committed under evidence/{residual,overfit}/.
result: blocked
blocked_by: prior-phase
reason: "GAP-38-01 (DEFERRED 2026-07-13): no Brutus payload under simulation_data/Data/ in .worktrees/trainex. The automated NET-03b/NET-05 bar is green on synthetic fixtures (which prove model+AD+loss wiring); the real-integrator-trajectory proof requires the dataset payload. Owner decision A (keep deferred) / B (provide payload + re-run) / C (waive) is logged and pending in 38-GAPS.md and v2.0-GAPS.md."

## Summary

total: 8
passed: 7
issues: 0
pending: 0
skipped: 0
blocked: 1

Ground-truth automated evidence re-run this session (not merely trusting SUMMARY claims):
- tests/phase38 discover: 128 tests OK (0 fail / 0 error / 0 skip) — 15.5s
- tests/phase37 regression: 55 tests OK — no regression from the pinn/__init__.py re-exports
- gradcheck fp64-CPU evidence: gradcheck_result=true
- adversarial spec-faithfulness audit (3 independent auditors): FAITHFUL on all NET-01..05 checks; zero discrepancies

## Gaps

[none — no code defects found. Test 8 is a prerequisite gate (missing dataset payload), not a code issue; it is tracked as GAP-38-01 (DEFERRED) in 38-GAPS.md / v2.0-GAPS.md, awaiting an owner decision.]

## Notes (verification observations — non-blocking; for owner awareness)

- SPEC-SILENT reduction convention — data loss: loss_catalog.py `data_huber_loss` reduces with `.mean()` over (N_t, 3 bodies, 3 coords) → 1/(9·N_t), whereas a literal `(1/N_t)·Σ_n Σ_i` reading implies 1/N_t. pinn_architecture.md is silent on how the per-body Huber reduces over the 3-vector; the code is internally consistent across all five terms. Because λ_data≡1 is the reference scale, this rescales the effective relative weight of the other four terms by ~9×. It is absorbed by λ calibration (the PHYS-05 scheduler is Phase 40 / TRAIN-03). Per SCOPE-18 (build-discovered spec ambiguity → surface, never fix here): recommend routing an explicit decision to the spec milestone and/or the Phase-40 λ-calibration. NOT a spec-faithfulness failure (no code↔spec contradiction).
- Cosmetic: dead `_ = D_CHARACTERISTIC_LENGTH` touch in `data_huber_loss` (loss_catalog.py:183) — D scaling is applied by callers, not inside the term.
- Process gate: no canonical `*-VERIFICATION.md` exists (the execute-phase verify step did not complete for Phase 38). The GSD phase-completion predicate (`phase uat-passed --require-verification`) therefore blocks phase transition until a passing VERIFICATION.md is produced, independent of this UAT result.
