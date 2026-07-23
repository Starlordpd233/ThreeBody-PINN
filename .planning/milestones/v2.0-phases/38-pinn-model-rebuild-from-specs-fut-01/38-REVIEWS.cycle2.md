---
phase: 38
reviewers: [claude-glm, claude-deepseek, grok, agy, claude-max, codex, claude-kimi]
rerun_reviewers: [claude-glm, grok]
reviewed_at: 2026-07-13T07:13:10Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070919Z-65190
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 38

## claude-glm Review

API Error: 529 [1305][该模型当前访问量过大，请您稍后再试][20260713151309183fef8897544c58]. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (127.0.0.1:4148).

---

## claude-deepseek Review



Now I have a thorough understanding of all six plans plus the SPEC and CONTEXT. Let me produce the review.

---

# Cross-AI Plan Review: Phase 38 — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Phase 38 has 6 plans, 18 tasks, across 5 waves — all following a strict TDD (tests-first) pattern. Wave 1 establishes the foundation (locked constants + architecture spec dataclass). Wave 2 builds the network backbone and COM projection head. Wave 3 implements PHYS-02 autograd physics residuals and a minimal Brutus fixture loader. Wave 4 delivers two standalone CLI probes (gradcheck + residual-on-ground-truth) and the five-term loss catalog. Wave 5 delivers the overfit probe and mechanical prohibition checks.

The plan has already been through one cross-AI review cycle (cycle 1) and incorporates resolutions for 4 HIGH, 8 MEDIUM, and 3 LOW findings. The replanned version addresses most structural concerns from cycle 1: task reordering for TDD, COM mass provenance via explicit `forward(tau_ic13, masses)`, SIREN principled-init testing, a dual PASS gate for rung 3 with genuine ground-truth teeth, and explicit phase-close real-dataset evidence gating.

## 2. Strengths

- **Spec-first grounding**: Every decision traces to a specific framework-spec section (§2.2, §3.1, §5.3.1, etc.). The planner-assumptions section in each plan surfaces unresolved edges (R3–R5) transparently rather than dropping them.
- **Phase-boundary discipline**: Each plan has an explicit "out of scope" section — no Phase 39/40/41 leakage. CTX-15..32 provide clear build-engineering decisions with documented rationale.
- **Prohibition enforcement**: The mechanical checks in 38-06-03 (spec byte-identity, no simulation_data writes, AST no-precision-default, AST no-v1.3-import) are thorough and inspect the full new-module list, not a hardcoded subset.
- **Dual PASS gate for rung 3**: Gate B (Newtonian-residual band comparing finite-differenced acceleration against the softened force) gives rung 3 real teeth — a D/mass/eps_soft mis-scaling that passes the self-consistency identity (Gate A) will FAIL Gate B because `a'_fd` is independent of those constants.
- **Full-stack evidence in rung 4**: The overfit probe evaluates all five loss-catalog terms (including the PHYS-02 AD path) at initial and final steps, even though it only optimizes the data term. A broken AD/physics path is visible in evidence without slowing the overfit.
- **Threat modeling per plan**: Each plan has a STRIDE register with explicit trust boundaries, severity, disposition, and mitigation — rare and valuable for a build-phase plan.

## 3. Concerns

### HIGH

**H1 — Rung 4 overfit probe: `eps_h` and `h0` provenance for full-stack loss evaluation is unspecified** (38-05-03, 38-06-02)

The overfit probe evaluates `soft_energy_loss(pred_positions, pred_velocities, h0, eps_h, ...)` as full-stack diagnostic evidence. The plan correctly states that `eps_h = 1e-4 * S_H` is computed UPSTREAM (Phase 39/40 metadata pipeline) and the loss term must not recompute it. But the overfit probe runs IN Phase 38 — before any metadata pipeline exists. Where does `eps_h` come from during the probe's diagnostic evaluation? The plan needs to specify: (a) a hardcoded synthetic default for the probe's diagnostic pass, OR (b) an explicit `--eps-h` / `--h0` CLI flag, OR (c) a planner note that the energy term in the full-stack evidence is conditional on supplied metadata and records "N/A" when absent. Without this, the overfit probe's energy-term evaluation is unimplementable.

**H2 — Residual-probe Gate A risks being a tautology** (38-04-03)

The plan says Gate A computes the matched-Plummer potential `V_eps` and its analytic gradient `-d V_eps / d r'_i`, then compares against `softened_acceleration`. But the analytic gradient of `V_eps = -sum m_i m_j / r_safe` is exactly `sum_{j!=i} m_i m_j (r'_j - r'_i) / r_safe^3` — which is what `softened_acceleration` computes (38-03-03). If Gate A computes the gradient manually using the same formula rather than via autograd on `V_eps`, it becomes a tautology (comparing the function against itself). The implementation MUST compute `-d V_eps / d r'_i` via `torch.autograd.grad(V_eps, positions)` (independent autograd path) for Gate A to have verification value beyond what `test_physics_residual.py` already provides. The plan's action text is ambiguous on this point — it says "compute the matched-Plummer potential ... and its analytic gradient" without specifying the mechanism. If implemented as a manual formula, Gate A is dead weight; if via autograd on `V_eps`, it's a genuine consistency check that autograd through the potential yields the same result as the hand-coded force.

### MEDIUM

**M1 — `com_projection.py` batch-dimension handling is underspecified relative to downstream consumers** (38-02-02, 38-03-03, 38-05-03)

38-02-02 says `project_com` supports "both a single 9-vector and a batched (N, 9) input shape." But 38-03-03's `physics_residual` docs suggest it operates per-time-point (the residual formula `f_i(u_n)` is per-snapshot). The loss catalog (38-05) operates on batches. The plans don't specify:
- Whether `physics_residual` accepts batched (N_t, 9) positions or a single (9,) vector
- Whether `causal_physics_loss` (which calls `physics_residual`) iterates over time points or operates on the full batch
- Whether `soft_energy_loss` receives batched positions/velocities or per-snapshot

This batch-dimension ambiguity across the residual → loss interface could cause a refactor at the 38-05 boundary. The plans would benefit from a one-sentence batch-contract statement (e.g., "all loss terms operate on batched tensors of shape (N_t, ...) and reduce to a scalar").

**M2 — Overfit probe optimizer hyperparameters are undocumented** (38-06-02)

The overfit probe uses Adam with an uncalibrated `--max-steps 3000`. But the learning rate, betas, and any LR schedule are never specified. For a probe whose PASS/FAIL verdict depends on achieving ≥10³× reduction within a step cap, the LR is a critical parameter — a wrong default LR could cause spurious FAILs even with correct wiring. The plan should pin a default LR (e.g., 1e-3 for Adam on this problem class) with documented rationale, and make it overridable via `--lr`.

**M3 — `TrajectoryFixture` container is referenced but never specified as an export** (38-03-02)

The fixture loader returns a `TrajectoryFixture` with "times, positions, velocities, masses, provenance." But the exact field names, shapes, and types are never specified. Downstream plans (38-04, 38-06) reference `load_trajectory` but assume its return type. The artifacts section for 38-03 lists exports as `["load_trajectory", "resolve_trajectory_path", "sha256_file"]` — `TrajectoryFixture` is missing. A named tuple or dataclass with documented fields would prevent silent interface drift between the loader and its consumers.

**M4 — Gate B synthetic fixture generation creates a testing circularity risk** (38-04-01)

The test for Gate B must "construct a physically-consistent synthetic trajectory by integrating the softened Newtonian EOM for a few small-dt steps." This requires a numerical integrator inside the test. The risk: if the same softened-force formula is used for both integration (fixture generation) and verification (Gate B computation), the test could mask a shared bug. Mitigation: the test should use an independent integration scheme (e.g., Runge-Kutta with a small fixed step) and document the integrator. The plan acknowledges this implicitly by requiring the finite-difference scheme to use the documented central-difference method, but doesn't address the integrator used for fixture generation.

**M5 — `ic_anchor_loss` requires IC state at u=0 (tau=-1), which the fixture loader may not provide** (38-05-02, 38-03-02)

The IC anchor loss evaluates at `u=0` (tau=-1), requiring the model's prediction at the initial condition. The fixture loader parses the IC file (3 lines: `m x y z vx vy vz`) which gives the t=0 state. But `u=0` in the model's input space corresponds to `tau = -1`, which IS the t=0 physical time. So the IC file provides what's needed. However, the plan doesn't explicitly wire the IC file's position/velocity into the loss — 38-03-02 says the loader parses masses from the IC file, but doesn't mention exposing the t=0 position/velocity. The IC anchor loss needs both the true position and velocity at u=0. This is resolvable (the loader already reads the IC file — just expose the parsed values), but the current plan text has a small gap.

### LOW

**L1 — Architecture spec forbids `power_p != 2` but the spec says p=2 is locked** (38-01-03)

38-01-03 says `__post_init__` raises on `power_p != 2`. This is correct (p=2 is a locked constant per ARCH-02). But the validator is overly specific — if a later phase introduces power-p as a tunable (unlikely given ARCH-02 is locked, but possible), the validator must be updated. This is minor; the fail-closed design is the right call.

**L2 — `EPS_SOFT` naming vs. `eps_train` in the spec** (38-01-02)

The constant is named `EPS_SOFT` with citation to `pinn_architecture.md §3.2/§3.4` where it's called `eps_train`. The plan's note says it's training-time Plummer softening. The naming is fine (it's the softening epsilon used throughout), but a comment clarifying "this is eps_train from §3.2/§3.4" would prevent confusion since "EPS_SOFT" doesn't appear verbatim in the spec.

**L3 — `componentwise_du` return type not specified** (38-03-01)

38-03-01 says `componentwise_du` returns first and second derivatives. The return type (tuple of two tensors? dict with keys?) isn't specified. `physics_residual` calls it internally, and `test_physics_residual.py` tests against symbolic oracles — so the interface is internally consistent. But without a documented return type, the test author and implementor may interpret the API differently.

**L4 — Evidence directory path is repeated across plans but not centralized** (38-04, 38-06)

The evidence root path `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/evidence/<rung>/<UTC>/` is repeated verbatim in plans 04 and 06. A centralized constant or `pathlib` convention in a shared module would reduce drift risk. Low priority, but worth noting for implementation.

## 4. Suggestions

1. **Add `--eps-h` and `--h0` flags to the overfit probe** (or document a hardcoded synthetic default) so the full-stack energy-term evaluation is implementable before Phase 39/40 metadata exists. Label the evidence as "diagnostic (metadata synthetic)" to distinguish from real-training evidence.

2. **Require Gate A to use `torch.autograd.grad(V_eps, positions)`** — compute the potential `V_eps` as a scalar, then differentiate via autograd. This makes Gate A a genuine independent-path consistency check rather than comparing `softened_acceleration` against itself.

3. **Add a batch-contract statement** in 38-03 and 38-05: "All loss-term callables accept batched tensors (N_t, ...) and reduce to a scalar. `physics_residual` accepts batched positions of shape (N_t, 9) and returns per-time-point residuals of shape (N_t, 3, 3)."

4. **Pin default Adam LR** for the overfit probe (e.g., `--lr 1e-3`) with rationale, and make it overridable. Document in the planner assumptions section alongside the uncalibrated `--max-steps`.

5. **Add `TrajectoryFixture` to the 38-03 exports** and define it as a named tuple or frozen dataclass with documented fields (`times`, `positions`, `velocities`, `masses`, `provenance` as a dict with `variant`, `id`, `path`, `sha256`).

6. **Document the Gate B synthetic-fixture integrator** (e.g., "4th-order Runge-Kutta with dt=0.001, using an independent implementation of the softened EOM") in the test-acceptance criteria to avoid testing circularity.

## 5. Overall Risk: **MEDIUM**

The plans are thorough, well-structured, and already incorporate a full cycle of adversarial review. The five HIGH concerns from cycle 1 are credibly resolved. The remaining gaps are real but narrow: the overfit probe's `eps_h`/`h0` provenance (H1) and the Gate A tautology risk (H2) are the two issues that could produce misleading PASS results if not addressed at implementation time. The medium concerns are all resolvable with small clarifications during execution. The phase goal — a spec-faithful model package proven by three rungs — is achievable with these plans.

The strongest risk mitigant is the phase-close real-dataset gate (rung 3 and rung 4 must run against a REAL Brutus trajectory before phase close). This gate catches any synthetic-fixture blind spots, including the ones flagged above.

---

## grok Review

I'll review the Phase 38 plans by reading the plan files first, then checking context only where needed for verification.Reading the six plan files next, then spot-checking SPEC/CONTEXT only where needed.

---

## agy Review



# Cross-AI Plan Review: Phase 38 (PINN Model Rebuild)

## 1. Summary
The Phase 38 plans provide a highly detailed, defensively engineered blueprint for rebuilding the PINN model from the framework specs. The execution is broken into test-driven, atomic steps with exceptionally strong mechanical guarantees (e.g., AST-based codebase compliance checks, dataset immutability validation). However, a critical mathematical oversight in the finite-difference dimension scaling (Rung 3) will cause false failures against ground-truth data, and diagnostic metadata dependencies in the overfit probe are underspecified.

## 2. Strengths
- **TDD Rigor:** The consistent tests-first methodology using deferred-import skip guards ensures test suites cleanly encode acceptance criteria before any production implementation occurs.
- **Fail-Safe Prohibitions:** The mechanical AST checks for precision defaults and v1.3-era imports, alongside the `simulation_data` read-only validation, provide excellent automated guardrails to prevent regression and drift.
- **Verification-Driven Integrity:** The inclusion of standalone, reproducible probes (fp64-CPU gradcheck, residual-on-ground-truth, and single-trajectory overfit) with dual PASS gates builds immense confidence in the physics wiring.
- **Reproducible Evidence Collection:** Non-overwriting, timestamped evidence emission that strictly records hyperparameters (e.g., max steps, initial/final losses) and fallback facts prevents silent failures and "close enough" optimizations.

## 3. Concerns

- **HIGH: Dimensional Mismatch in Rung 3 Finite Difference (`38-04-03`)**  
  Gate B (Newtonian-residual band) computes `a'_fd` using Brutus time `t` and scales velocity to `v/D`. This yields `a'_fd = a / D`. However, the model residual `f_i` and the softened force `sum F_ij` are evaluated w.r.t the canonical leaf `u = t / T`, making them equal to `a * T^2 / D` (since `D^3 = T^2`). Comparing `a'_fd` directly to `sum F_ij` means Gate B will consistently fail by a factor of `T^2` (e.g., 100x error if `T=10`). 

- **MEDIUM: Missing Metadata for Full-Stack Loss Evaluation (`38-06-02`)**  
  Rung 4 (overfit probe) evaluates all five loss terms to provide full-stack diagnostic evidence. However, `soft_energy_loss` requires `eps_h` and `h0` (`eps_h` is explicitly noted as an upstream-supplied metadata scalar), and `angular_momentum_loss` requires `l0`. The minimal `fixture_loader` (`38-03-02`) does not compute or provide these. The overfit probe will either crash or be forced to duplicate Phase 39/40 logic to derive them.

- **LOW: Implicit `dtype`/`device` Propagation in `forward` (`38-02-03`)**  
  The network's `forward` method calls `project_com(raw_output, masses, dtype=..., device=...)` but does not receive `dtype` or `device` as arguments. The implementation should explicitly extract them from `tau_ic13` or the model's parameters to prevent runtime mismatch errors (particularly on MPS).

- **LOW: Underspecified SIREN Bias Initialization (`38-02-03`)**  
  The plan enforces strict principled bounds for layer weights (`U[-1/n_in, 1/n_in]`, etc.) but omits bias initialization bounds. If the `test_network_structure` suite rigidly asserts bounds for all parameters, PyTorch's default bias initialization might cause spurious test failures.

## 4. Suggestions
1. **Fix Rung 3 Dimensionality:** Update `38-04-03` to define the finite-difference scheme w.r.t `u` instead of `t`. Map the Brutus timestamps to `u = t / T` and scale velocities to `v' = dr'/du = v * (T / D)` before differencing.
2. **Mock or Compute Probe Metadata:** Amend the `fixture_loader` (`38-03-02`) to compute `h0`, `eps_h` (or compute `S_H` and apply the `1e-4` factor locally just for the probe), and `l0` directly from the `t=0` state of the loaded trajectory, or explicitly mock these metadata scalars in the overfit probe.
3. **Explicit Device Extraction:** Add a brief instruction in `38-02-03` to extract `dtype` and `device` dynamically from the input tensor `tau_ic13` inside the `forward` method before passing them to `project_com`.
4. **Clarify Bias Init:** Clarify the expected bias initialization bounds for SIREN layers in `38-02-03` and its corresponding test in `38-02-01` to prevent `test_network_structure` from flaking.

## 5. Overall Risk
**MEDIUM**  
The core architecture and testing strategy are highly robust and thoughtfully planned. However, the mathematical oversight in the finite-difference dimension scaling (Rung 3) must be patched to unblock successful probe execution and prevent frustrating false positives against ground-truth data.

---

## claude-max Review



I have enough to write the review. Key verification results: `e7226ff0` is confirmed as the last commit touching `ctl_instruction.md`, but `pinn_architecture.md` was last touched by the older `583a010f` (still functionally fine, since `e7226ff0` is a later commit whose blob for that spec equals current). REQUIREMENTS.md contains no `S_H`/`H_0`/`L_0` metadata definition, confirming a wiring gap for the probe's five-term evaluation.

---

# Phase 38 Plan Review — PINN Model Rebuild from Specs (FUT-01)

## 1. Summary

Six plans (38-01…38-06) rebuild the spec-faithful `pinn/` model — constants + `ArchitectureSpec` (01), SQR-SkipResNet-SIREN network + COM head (02), PHYS-02 residual + read-only fixture loader (03), gradcheck & residual probes (04), five-term loss catalog (05), overfit probe + phase-wide prohibition checks (06). The plans are unusually rigorous: strict TDD (tests-first in every wave), executable PASS/FAIL probes, mechanical prohibition backstops (spec byte-identity, no-`simulation_data`-writes, AST no-precision-default / no-v1.3-import), and a documented cross-AI review cycle already folded in. Dependency waves are coherent and the phase boundary (vs. Phase 39/40/41) is cleanly held. The build path to all five requirements (NET-01…05) is sound; the residual concerns live at the evidence/diagnostic layer and one imprecise provenance note.

## 2. Strengths

- **Guardrails are excellent.** Read-only specs enforced by sha256 byte-identity; `simulation_data/` write-guard; `resolve_trajectory_path` digits-only validation blocking `../` traversal; AST checks over a *data-driven* module list so new modules are covered automatically.
- **Real teeth, not theater.** Rung 3's dual gate (Gate A self-consistency + Gate B ground-truth Newtonian band) explicitly defeats the "blind to shared D/mass/eps_soft errors" failure mode; the SIREN principled-init *statistics* test defeats a silent Kaiming/Xavier substitution; the odd-layer update is asserted numerically, not by module presence.
- **Precision seam discipline** (CTX-14/ENV-04) is consistently threaded — no module encodes a precision default; probes require explicit `--precision/--device`.
- **Falsifiability is designed in.** Every probe has an explicit numeric criterion, a fail-loud path, and recorded measured-vs-threshold evidence; the overfit cap makes non-convergence a bounded FAIL, never a hang.
- **Honest scope on evidence.** The synthetic-in-worktree vs. real-dataset distinction is surfaced as an explicit phase-close gate (commit real rung-3/rung-4 evidence OR log a DEFERRED gap), not an informal follow-up.

## 3. Concerns

**MEDIUM — Overfit probe's five-term full-stack evaluation is under-specified (38-06 × 38-05).** The review-#7-added requirement makes `run_overfit` evaluate all five loss terms at init/final. But `soft_energy_loss` needs `h0` **and** a *supplied* `eps_h = 1e-4·S_H`, and `angular_momentum_loss` needs `l0`; both energy/angular terms also need `pred_velocities` (only obtainable via the PHYS-02 AD `dr'/du` path — the model returns positions only). `h0`/`l0` are derivable from the loader's initial snapshot, but `eps_h`/`S_H` is explicitly a Phase 39/40 metadata artifact with **no Phase 38 source** (confirmed: REQUIREMENTS has no `S_H`/`H_0`/`L_0` definition), and `soft_energy_loss`'s own contract forbids recomputing `S_H`. No plan states how the probe obtains `eps_h` or derives `pred_velocities` for this diagnostic. The executor will hit an undefined input. Recommend: pin, in 38-06, how the probe sources `h0`/`l0`/`eps_h`/velocities (e.g., compute `h0`/`l0` from the initial snapshot, AD-derive velocities, and either compute a probe-local `S_H` or record energy/ang-mom as "not evaluated — requires Phase 39/40 metadata"). It does not gate the PASS criterion, so it is diagnostic-only, but as written it blocks the added evaluation.

**LOW — Spec byte-identity baseline provenance is factually imprecise (38-06-03).** The plan states "the specs were last touched at commit `e7226ff0`." Verified: `e7226ff0` touched only `ctl_instruction.md`; `pinn_architecture.md` was last touched by the older `583a010f`. Deriving both baselines from `git show e7226ff0:<spec>` still yields the *correct* current content for both (nothing touched `pinn_architecture.md` after `583a010f`, and `e7226ff0` is a later commit), so the check functions correctly — but the prose should be corrected to avoid an executor picking the wrong ref for the architecture spec.

**LOW — COM-projection data-loss floor for non-COM-zero trajectories (38-06/38-03).** The overfit optimizes `data_huber_loss(projected_pred, scaled_GT)`. The model output is mass-weighted-COM-zero by construction; if an override trajectory's ground truth is not COM-centered (possible for `hierarchical`), the data loss has an irreducible floor and the ≥10³× gate may be unreachable. The chosen default (`standard_quasi_random_gold_standard`, exact COM=0) avoids this, and it is documented — but the probe accepts arbitrary trajectories with no guard/warning. A one-line note ("override trajectories must be COM-consistent, or recenter GT") would close it.

**LOW — Overfit optimizer hyperparameters unspecified (38-06-02).** `run_overfit` fixes `--max-steps` (3000, explicitly uncalibrated) but says nothing about the Adam learning rate. On a `first_omega_0=30` SIREN, an ill-chosen default LR can prevent the ≥10³× reduction within the cap, producing a spurious (bounded) FAIL. Left to executor discretion is acceptable, but naming it as a build-engineering knob with the calibration guidance would prevent a false negative.

**LOW — "End-to-end" in NET-05 is met by the rung *ensemble*, not rung 4 alone.** NET-05's wording ("model + AD + loss wired correctly end-to-end") is only partly delivered by rung 4 (data-term-only optimization). The plan correctly narrows the claim and leans on rungs 2–3 for the AD/physics path. This is a sound decomposition and was owner-surfaced (#7); flagging only so verification checks the *set* of rungs against NET-05, not rung 4 in isolation.

## 4. Suggestions

- In 38-06, add one explicit sentence resolving `h0`/`l0`/`eps_h`/`pred_velocities` provenance for the five-term evaluation (the MEDIUM). This is the single change most likely to save an execution stall.
- Correct the 38-06-03 provenance prose to name the correct last-touch commit per spec (or state "derive each baseline via `git show <phase-base-ref>:<spec>`" without asserting a single shared touch commit).
- Add a COM-consistency guard/warning in the overfit and residual probes for override trajectories.
- Name the overfit Adam LR (and its calibration note) alongside `--max-steps`.

## 5. Overall Risk

**MEDIUM (low end).** The core build-and-prove path is thorough, well-sequenced, and strongly guarded — most projects would ship this as-is. The one genuine execution risk is the under-specified five-term evaluation metadata in the overfit probe (a review-added requirement that outran its inputs); the remaining items are diagnostic-layer or documentation refinements. Resolving the MEDIUM before executing wave 5 would drop this to LOW.

---

## codex Review


_codex failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=codex
- exit_code=143
- elapsed_seconds=360
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=0
- stderr_bytes=759449

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-codex-38.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-codex-38.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-codex-38.meta

Stderr excerpt:
```
s become `v'=dr'/du`; otherwise the real-trajectory residual evidence can false-pass or false-fail.

- **LOW:** The “physically-consistent synthetic trajectory” for residual-probe tests is specified conceptually but not as a deterministic fixture-generation recipe. This is probably manageable, but it leaves room for flaky or accidentally self-validating tests.

## 4. Suggestions

- Add the real-evidence and deferred-gap artifacts to `38-06` ownership/frontmatter, or add an explicit phase-close operator plan that owns them.
- Move a lightweight spec byte-identity check into every wave’s verification, or create it in `38-01` and run it before each commit.
- Amend `38-04` to spell out the exact `raw t → u`, `raw v → v'`, and acceleration scaling used by Gate B, with a unit test on a known trajectory.
- Define the synthetic residual fixture generator parameters: initial state, integrator method, step size, tolerance, and fixed seed.

## 5. Overall Risk (LOW/MEDIUM/HIGH)

**MEDIUM**. The architecture and test strategy are strong, but the phase-close artifact ownership and residual-scaling ambiguity are important enough to fix before execution.
hook: Stop
hook: Stop
hook: Stop

```

---

## claude-kimi Review


_claude-kimi failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=0
- stderr_bytes=192

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-claude-kimi-38.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-claude-kimi-38.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070228Z-31550/xreview-claude-kimi-38.meta

Stderr excerpt:
```
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors

```

---

## Consensus Summary

**Cycle 2 — fresh panel against the REVISED plans (post-replan commit 05273b4c; adjudicated against working-tree 38-01..38-06 on 2026-07-13). Cycle-1 report preserved at `38-REVIEWS.cycle1.md`.**

### Panel health

- **Full reviews (3):** claude-deepseek, agy, claude-max.
- **codex:** watchdog-timed-out at 360 s twice with 0 stdout, BUT its complete review reached stderr before the kill (recovered from `xreview-codex-38.err` in the first-rerun directory; stub retained above per protocol). Its findings are adjudicated below as reviewer signal.
- **Stubs after one retry each:** claude-glm (upstream 529 "model overloaded" both attempts — same reviewer failed both cycle-1 attempts too), grok (exit 0 with a preamble-only sentence both attempts, 18 s — identical to its cycle-1 failure mode), claude-kimi (540/360 s watchdog timeout, 0 bytes both attempts).

### Cycle-1 resolution check (verified in revised plan text)

All four cycle-1 HIGHs and the addressed MEDIUM/LOWs are visibly incorporated: tests-first task reorder in every plan; `forward(tau_ic13, masses)` explicit raw-mass interface with an unequal-mass test; SIREN init-statistics test; rung-3 dual PASS gate; five-field `LossWeights`; `s_h_or_eps_h` -> `eps_h` rename with supplied-metadata semantics; pinned central-difference scheme; `--min-separation-guard` default 1e-3 with rationale; phase-close real-dataset gate; spec-baseline pinned to the pre-phase commit. No cycle-1 finding is re-counted here; the three HIGHs below are defects in the NEWLY ADDED mechanisms themselves.

### Unresolved HIGH concerns (3, deduplicated)

1. **Rung-3 Gate B finite-difference scaling is dimensionally wrong as written** (agy HIGH; codex MEDIUM corroboration; 38-04:93, 38-04:197). The plan pins `a'_fd(n) = (v'(n+1) - v'(n-1))/(t(n+1) - t(n-1))` with "positions/velocities scaled to r' = r/D first" — i.e. differencing D-scaled velocities against RAW Brutus time. Independent check (grounded: `pinn_architecture.md:980` `T = t_max`, `D = (G T^2)^(1/3)`; dataset horizon `t_end = 10`, README:287; PIPE-09 `D^3 = G T^2`, ctl:1024): the residual force `sum F_ij` in r' units equals `(T^2/D) * a_brutus`, while the plan's `a'_fd` = `a_brutus/D` (or `(T/D) a` if v' means dr'/du) — Gate B disagrees by `T^2 = 100` (or `T = 10`) on a CORRECT implementation; the median relative residual lands at ~99, far above the 1e-1 band, so Gate B always FAILs (or the executor silently invents the missing conversion). Note `pinn/constants.py`'s planned inventory has no `T` constant, so the t->u map cannot even be written from the constants module. Fix: difference w.r.t. `u = t/T` (v' = v*T/D, denominator Delta-u), or equivalently scale `a'_fd` by `T^2`; add the characteristic time to the constants inventory; align the 38-04-01 synthetic-fixture recipe.
2. **Overfit-probe five-term evaluation has unspecified inputs** (deepseek HIGH + agy MEDIUM + claude-max MEDIUM — 3-reviewer consensus; 38-06:96, 38-06-02, vs 38-05:93/187). The probe must evaluate all five loss terms at initial+final, but `soft_energy_loss` needs `h0` and a SUPPLIED `eps_h = 1e-4*S_H` (a Phase 39/40 metadata artifact with no Phase 38 source; 38-05 forbids recomputing it), `angular_momentum_loss` needs `l0`, and both need `pred_velocities` (the model returns positions only; the AD path is implied, never stated). As written the mandated evaluation is unimplementable — the executor hits undefined inputs. Fix: one 38-06 sentence pinning provenance (derive `h0`/`l0` from the fixture's t=0 snapshot; AD-derive velocities; either compute a probe-local `S_H` labeled diagnostic-only or record energy/ang-mom as "not evaluated — requires Phase 39/40 metadata").
3. **Gate A gradient mechanism unpinned — tautology risk** (deepseek HIGH; 38-04-03:196). "Compute the matched-Plummer potential V_eps ... and its analytic gradient" does not pin HOW the gradient is obtained; spec §10.4 (`pinn_architecture.md:1029-1032`) is likewise method-agnostic ("its negative position gradient"). A hand-coded gradient reproduces the exact closed form of `softened_acceleration`, making Gate A a self-comparison with no verification value; the planned mutated-force falsifiability test passes either way, so nothing forces the independent path. Fix: require `torch.autograd.grad(V_eps, positions)` explicitly.

### Actionable non-HIGH concerns (6, deduplicated; none incorporated or explicitly deferred in the current plans)

4. **Overfit Adam LR unpinned** (deepseek M2 + claude-max LOW; 38-06-02). `--max-steps` is documented but no default learning rate or `--lr` override exists; an ill-chosen LR on a `first_omega_0=30` SIREN can produce a spurious bounded FAIL of the 1e3x gate. Add a default LR + `--lr` with the calibration note.
5. **Phase-close evidence / gap-register ownership** (codex HIGH, adjudicated down to actionable-MEDIUM). The phase-close gate (38-06 must_haves truth 5) requires committing real rung-3/4 evidence OR a DEFERRED gap entry, but no plan's `files_modified`/tasks own the committed evidence or the register entry, and `38-GAPS.md` does not exist. Downgrade rationale: gap registers are created-on-demand per standing project convention; the gate is operator-owned and stated in three places (must_haves, planner_assumptions, success_criteria); runtime evidence dirs are consistently declared under `<artifacts_produced>` across plans, so "execution-blocked" does not hold. Remaining fix: a one-line ownership note in 38-06 naming who commits the evidence/DEFERRED entry and under which paths.
6. **Batch-dimension contract across the residual->loss seam** (deepseek M1; 38-03/38-05). `project_com` batching is pinned (38-02-02) and every loss formula is per-n with N_t reduction, but `physics_residual`/`componentwise_du` batch semantics stay implicit while 38-04 and 38-05 consume the 38-03 interface as PARALLEL wave-4 executors. Add the one-sentence batch contract.
7. **Gate-B synthetic-fixture integrator recipe** (deepseek M4 + codex LOW; 38-04-01). "Integrate the softened Newtonian EOM" names no integrator, step size, or seed, and if the fixture generator reuses the production softened-force code a shared bug self-validates (only the real-data phase-close gate would catch it). Pin an independent integrator + deterministic parameters.
8. **Spec-baseline provenance prose is factually imprecise** (claude-max LOW — VERIFIED by git this cycle; 38-06:97, 38-06-03). `e7226ff0` last touched only `ctl_instruction.md` (2026-07-11); `pinn_architecture.md` was last touched by `583a010f` (2026-06-29). `git show e7226ff0:<spec>` still yields correct bytes for both, so the check functions — but the "the specs were last touched at commit e7226ff0" sentence should be corrected so an executor cannot pick a wrong ref.
9. **COM-consistency guard for override trajectories** (claude-max LOW; 38-06/38-04). The COM-zero default trajectory avoids the irreducible data-loss floor, but the probes accept arbitrary overrides with no guard/warning; a non-COM-centered hierarchical GT can make the 1e3x gate unreachable. Add a one-line guard or recenter note.

### Raised but requiring no plan change (adjudicated against revised text)

- `TrajectoryFixture` fields/shapes are pinned in 38-03 (`times, positions (n,3,3), velocities, masses (3,), provenance{variant,id,path,sha256}`); only the frontmatter exports-array entry is missing — cosmetic (deepseek M3).
- IC-anchor t=0 state: the loader "parse[s] the paired IC file ... for raw masses (and t=0 state)" and the trajectory arrays include t=0 (deepseek M5 — closed by the revision).
- Per-commit spec byte-identity timing (codex MEDIUM): the pre-phase pinned baseline makes wave-5 detection sound regardless of when drift occurred, and every plan's verification block already asserts spec byte-identity per plan.
- `EPS_SOFT`/`eps_train` naming: the clarifying parenthetical is in 38-01-02 (deepseek L2 — closed).
- dtype/device propagation into `project_com` inside forward (agy LOW): the mandated both-precision forward tests catch any mismatch; implementation detail.
- SIREN bias init (agy LOW): the init-statistics test explicitly targets WEIGHT tensors, so the flake scenario does not arise; bias init is executor build-engineering discretion.
- `componentwise_du` return type (deepseek L3), evidence-path centralization (deepseek L4), `power_p` validator breadth (deepseek L1), NET-05 rung-ensemble wording (claude-max LOW): intra-plan/tests-first-converged or informational; no plan change needed.

### Verdict

The revised plans genuinely closed cycle 1 (structure, interfaces, falsifiability, phase-close gating). The remaining risk is concentrated in the two rung-3 gates and the rung-4 five-term evaluation — all three introduced BY the cycle-1 fixes and all three fixable with a few sentences in 38-04/38-06 (plus 6 small actionable notes). Recommend `/gsd-plan-phase 38 --reviews` targeting 38-04 and 38-06 before execution.

## xreview Diagnostics

### claude-glm
- reviewer=claude-glm
- exit_code=1
- elapsed_seconds=231
- timeout_seconds=540
- watchdog=not_triggered
- command=ccp glm -p - 
- stdout_bytes=245
- stderr_bytes=192

### claude-deepseek
- status: preserved from existing REVIEWS.md

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=18
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260713T070919Z-65190/xreview-prompt-38.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=923
- stdout_bytes=205
- stderr_bytes=0

### agy
- status: preserved from existing REVIEWS.md

### claude-max
- status: preserved from existing REVIEWS.md

### codex
- status: preserved from existing REVIEWS.md

### claude-kimi
- status: preserved from existing REVIEWS.md

## Verification coverage

**Cycle-2 source-grounding pass** over every symbol the six REVISED PLAN.md files cite as already existing (enumerated from the current working-tree plan text, 2026-07-13). Authority: `grep` (`gsd-tools drift-guard authority --raw`). Severity mapping under this authority (per `drift-guard severity`): VERIFIED -> `none`, MISSING -> `needs-acknowledgement`, AMBIGUOUS -> `MEDIUM`, UNCHECKABLE -> `INFO`; **hardBlock: false for every verdict — no hard blocks this cycle.**

**Excluded as phase-produced artifacts** (declared under each plan's `<artifacts_produced>`): `pinn/constants.py` and its 10 constant names; `pinn/architecture_spec.py` `ArchitectureSpec` + its 11 fields; `pinn/network.py` `SQRSkipResNetSIREN`/`build_network`/the unprojected test hook; `pinn/com_projection.py` `project_com`; `pinn/physics_residual.py` `physics_residual`/`softened_acceleration`/`componentwise_du`; `pinn/verification/fixture_loader.py` `load_trajectory`/`resolve_trajectory_path`/`sha256_file`/`TrajectoryFixture`; the three rung probes with `main`/`run_gradcheck`/`run_residual_on_ground_truth`/`run_overfit` and CLI flags `--precision --device --evidence-root --path --variant --id --residual-threshold --newtonian-residual-threshold --min-separation-guard --max-steps --lr(absent)`; `pinn/loss_catalog.py` `LossWeights` (5 lambda_* fields)/`LossTerms`/`data_huber_loss`/`ic_anchor_loss`/`causal_physics_loss`/`soft_energy_loss`/`angular_momentum_loss`/`compose_total`; all `tests/phase38/*` modules; evidence dirs under `.planning/phases/38-*/evidence/`; the six `38-0N-SUMMARY.md` outputs.

### Existing files cited in context/read_first — all VERIFIED (exist on disk)

`pinn/runtime.py` · `pinn/__init__.py` · `pinn/verification/__init__.py` · `pinn/verification/componentwise_ad.py` · `scripts/run_precision_probe.py` · `tests/phase37/__init__.py` · `tests/phase37/test_runtime.py` · `tests/phase37/test_componentwise_ad.py` · `tests/phase37/test_precision_orchestrator.py` · `simulation_data/Documentation/README.md` · `.claude/rules/dataset-reference.md` · `.claude/rules/pinn-reference.md` · `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` · `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` · `pinn/basic_architecture.py` · `pinn/data-processing-pipeline-full.py` · `pinn/data-handling/` (v1.3 banned-reference targets all present) · `.planning/ROADMAP.md` · `.planning/REQUIREMENTS.md` · `.planning/STATE.md` · `38-SPEC.md` · `38-CONTEXT.md` · `38-PATTERNS.md` · `~/.claude-max/gsd-core/workflows/execute-plan.md` · `~/.claude-max/gsd-core/templates/summary.md`

### Code symbols in existing modules

| Symbol (citing plan:line) | Verdict | Evidence (file:line) |
|---|---|---|
| `RuntimeSpec` frozen dataclass, cited `runtime.py:23-38` (38-01:144) | VERIFIED | `pinn/runtime.py:23-24` (`@dataclass(frozen=True)` / `class RuntimeSpec:`) |
| `resolve_runtime` fail-closed raise, cited `:84-95` (38-01:144) | VERIFIED | `pinn/runtime.py:65` (def), raise ValueError inside 84-95 |
| `_ALLOWED_PROFILES` / `_ALLOWED_PAIR_DESCRIPTION` (38-01:116) | VERIFIED | `pinn/runtime.py:44` / `:59` |
| `AGGREGATE_CRITERION = 1e-6`, cited `componentwise_ad.py:113-118` (38-01:117) | VERIFIED | `pinn/verification/componentwise_ad.py:113` |
| `synthetic_trajectory` pure fn, cited `:62-76` (38-02:138) | VERIFIED | `pinn/verification/componentwise_ad.py:62` |
| same-dtype/device `as_tensor` discipline, cited `:73-76` (38-02:138) | VERIFIED | `componentwise_ad.py:73-76` (2 `as_tensor` hits) |
| explicit-leaf tensor construction, cited `:137-138,196-199` (38-02:171) | VERIFIED | `componentwise_ad.py:137` (`u_leaf = _torch.tensor(..., dtype=dtype, device=device`) / `:196` |
| `torch.func.jacrev` usage, cited `:128-157` (38-03:188) | VERIFIED | `componentwise_ad.py` jacrev x2 within 128-157 |
| non-finite refusal, cited `:193-206` (38-03:188) | VERIFIED | 4 finite/refus hits within 193-206 |
| result-dict pattern, cited `:215-229` (38-05:181) | VERIFIED | `componentwise_ad.py:215` (`return {`) |
| fallback capture before torch import, cited `:30-41` (38-04:151) | VERIFIED | `PYTORCH_ENABLE_MPS_FALLBACK` x2 within 30-41 |
| argparse required `--precision`/`--device`, cited `:371-394` (38-04:151) | VERIFIED | 3 precision/device hits within 371-394 |
| `_sha256_file`, cited `run_precision_probe.py:109-113` (38-03:156, 38-06:183) | VERIFIED | `scripts/run_precision_probe.py:109` |
| `write_evidence_run` + `run_id`, cited `:380-420`/`:390-420` (38-04:152) | VERIFIED | `scripts/run_precision_probe.py:390` |
| deferred-import `_load_*` guards (38-01:87) | VERIFIED | `tests/phase37/test_runtime.py:14,28` |
| frozen-dataclass assertion, cited `test_runtime.py:66-73` (38-01:87) | VERIFIED | 4 frozen/AttributeError hits within 66-73 |
| default-dtype invariance, cited `:122-137` (38-02:109) | VERIFIED | 3 default_dtype hits within 122-137 |
| AST executable-code technique, cited `:139-183` (38-06:180) | VERIFIED | 6 `ast.` hits within 139-183 |
| `pinn/__init__.py` surface (RuntimeSpec/resolve_runtime + Phase-38 docstring note) (38-02:172) | VERIFIED | `pinn/__init__.py:5` |
| `pinn/verification/__init__.py` docstring ("belongs to Phase 38 and is not present") (38-03:158) | VERIFIED | `pinn/verification/__init__.py:5` |

### Framework-spec sections, dataset facts, and planning artifacts

| Claim (citing plan) | Verdict | Evidence (file:line) |
|---|---|---|
| §5.3.1 PHYS-02 header + u-leaf/no-chain-factor contract (38-03:91,187) | VERIFIED | `pinn_architecture.md:888` (header), `:797` (canonical leaf u, 2x/4x tau-leaf-only) |
| §5.3.1 worked example r'(u)=[sin2piu, cos2piu, u^2] + symbolic dr'/du, d2r'/du2 (38-03:128,194) | VERIFIED | `pinn_architecture.md:924-928` |
| `r.sum()` VJP anti-pattern FORBIDDEN (38-03:19) | VERIFIED | `pinn_architecture.md:911` |
| §2.2 principled init: first layer U[-1/n_in,1/n_in]; hidden U[+-sqrt(6/n_in)/hidden_omega_0]; line 983 (38-02:111,168) | VERIFIED | `pinn_architecture.md:149` (§2.2), `:177`, `:263`, `:983` |
| §2.3 odd-layer update x = f_sr(x_prev) + (LayerNorm(x_prev))^p, p=2 (38-02:168) | VERIFIED | `pinn_architecture.md:190` (§2.3), `:207`, `:981` |
| §2.4 Table 1: depth 12 / width 256 / LayerNorm(elementwise_affine=False, eps=1e-5) odd layers / omega 30/1 (38-02:168) | VERIFIED | `pinn_architecture.md:248,251,256,236,167,261` |
| §3.1 data Huber delta_r, unweighted data term (38-05:113,148) | VERIFIED | `pinn_architecture.md:292,303-307` |
| §3.2 softened force, r_safe = sqrt(||.||^2 + eps_train^2) (38-03:20,187) | VERIFIED | `pinn_architecture.md:362,379` |
| §3.2 causal weights w_n = exp(-eta_c sum stopgrad(Rbar_m)), eta_c=1, D-04 Option A owner-ratified (38-05:17,178) | VERIFIED | `pinn_architecture.md:414,424` |
| §3.3 IC anchor beta_v (38-05:113,148) | VERIFIED | `pinn_architecture.md:473,475` |
| §3.4 V_eps = -sum m_i m_j / r_safe; Delta H_n; eps_H = 1e-4*S_H; persist BOTH S_H and eps_H — cited lines 527/531/542 (38-05:102,124,178) | VERIFIED (exact) | `pinn_architecture.md:497,514,527,531,542` — plan line citations match exactly |
| §3.5 L_L componentwise Huber, L_scale = \|\|L_0'\|\| + eps_L, eps_L=1e-8 (38-05:178) | VERIFIED | `pinn_architecture.md:611,613,615` |
| §10.2 COM invariance abs(COM) < 1e-10 (38-02:139) | VERIFIED | `pinn_architecture.md:1019-1022` |
| §10.4 force-energy consistency relative_error < 1e-5 (38-04:91,182) | VERIFIED — but mechanism-agnostic | `pinn_architecture.md:1029-1032`; the spec says "its negative position gradient" without pinning autograd vs hand-derived — feeds unresolved HIGH #3 (Gate A tautology) |
| Unit system: T = t_max, D = cbrt(G T^2), G=1 (38-04 Gate B basis) | VERIFIED | `pinn_architecture.md:980`; grounds HIGH #1 (T=10 with dataset horizon) |
| eps_train = 1e-5 (§3.2/§3.4 citations in 38-01:126) | VERIFIED | `pinn_architecture.md:379,516,542` |
| tau = 2u - 1 (38-01:18; 38-05:121) | VERIFIED | `pinn_architecture.md:487` |
| ctl §2.5 / PIPE-09: D = (G T^2)^(1/3) ~= 4.6416 canonical; 6.694 rejected; no config may select mass-fraction (38-01:91,126) | VERIFIED | `ctl_instruction.md:1005,1011,1016,1024` (normative PIPE-09 block) |
| PHYS-03 anti-pattern: additive +eps on distance norm prohibited (38-03:201) | VERIFIED | `ctl_instruction.md:1024` |
| ctl "Loss Function Formulation" / "Phase 2: Total Training Loss" (38-05:114,149) | VERIFIED | `ctl_instruction.md:1742,1744` |
| ctl optimizer-phase note: L-BFGS phase 2b; lambda values frozen, no dual updates in line search (38-05:179) | VERIFIED | `ctl_instruction.md:1706,1765` |
| Dataset README: File Schemas (`t N t_cpu` header, `m x y z vx vy vz`), Result: footer optional (38-03:129,155) | VERIFIED | `README.md:16` (TOC), `:267` (Result schema) |
| Dataset README: File Naming Conventions + folder->variant mapping incl. all four Brutus folders and both IC folders (38-03:100) | VERIFIED | `README.md:15,98-104,148-151` |
| Dataset README: G=1 natural units, total mass ~3 (38-03:155) | VERIFIED | `README.md:243` |
| Dataset README: Mass Normalization — standard exactly (1,1,1); hierarchical varies (38-02:141) | VERIFIED | `README.md:314` |
| Dataset README: completeness rule final timestep >= 9.5, not footer (38-03:22,155) | VERIFIED | `README.md:553,642,699` |
| Dataset README: gold dt_out = 0.01; horizon t_end = 10 (38-03:99) | VERIFIED | `README.md:180,287` |
| Commit `e7226ff0` = last spec touch (38-06:97,186: "the specs were last touched at commit e7226ff0") | AMBIGUOUS (severity MEDIUM, hardBlock false) | `git log`: `e7226ff0` (2026-07-11) last touched ONLY `ctl_instruction.md`; `pinn_architecture.md` last touched `583a010f` (2026-06-29). `git show e7226ff0:<spec>` still yields current bytes for both, so the check functions; prose imprecise — actionable item #8 |
| NET-01..NET-05 requirement IDs (all plans) | VERIFIED | `.planning/REQUIREMENTS.md` (10 references) |
| CTX-14..CTX-32 decision IDs (all plans) | VERIFIED | `38-CONTEXT.md` (all IDs CTX-14 through CTX-32 present) |
| SCOPE-12 / SCOPE-18 / SCOPE-20 / ENV-04 (38-03:20; 38-06:45; 38-04:20; 38-01:42) | VERIFIED | `.planning/REQUIREMENTS.md:43,126,128,36` |
| D-04 Option A (38-05:17) | VERIFIED | `pinn_architecture.md:424` (owner-ratified) + `38-CONTEXT.md:64` |
| 38-SPEC Prohibitions table + edges R1-R5 (38-06:181; all plans) | VERIFIED | `38-SPEC.md:99,103`; R1-R5 present |
| conda env `pinn-train` (every verify command) | VERIFIED | `~/miniforge3/envs/pinn-train` exists on disk |
| `shasum -a 256` (38-06:186) | VERIFIED | `/usr/bin/shasum` |

### MISSING (acknowledged in-plan)

| Symbol | Verdict | Notes |
|---|---|---|
| `simulation_data/Data/brutus_output/{brutus_standard_quasi_random_gold_standard, brutus_standard_quasi_random, brutus_hierarchical, brutus_hierarchical_gold_standard}/` and `simulation_data/Data/ic_final/{ic_standard_quasi_random, ic_hierarchical}/` (38-03:100) | MISSING on disk (severity needs-acknowledgement, hardBlock false) | `simulation_data/Data/` holds only `forensic/` + `testing_data/` — the bulk payload is absent from this worktree. The plans themselves acknowledge this (38-03 `<default_trajectory>` orchestrator fact: "no Brutus trajectory payload exists on disk in this worktree") and route around it (synthetic tmp fixtures for automated tests + the 38-06 phase-close real-dataset gate with an explicit DEFERRED path). Acknowledgement requirement satisfied in-plan. |

### UNCHECKABLE (reasons)

| Symbol | Verdict | Reason |
|---|---|---|
| `torch.autograd.gradcheck(eps/atol/rtol)`, `torch.func.jacrev`, `torch.as_tensor`, `torch.Generator`, `nn.LayerNorm(elementwise_affine=, eps=)`, torch Huber C1-knot behavior (38-02/03/04/05) | UNCHECKABLE (severity INFO, hardBlock false) | External-library API surface; signatures not verifiable under grep authority. Repo precedent for the exact usage patterns exists in committed Phase-37 code (`componentwise_ad.py:73-76,128-157`), which is the strongest grep-visible evidence available. |
| `git show <phase-base-ref>:<spec> \| shasum -a 256` semantics (38-06:186) | UNCHECKABLE (severity INFO, hardBlock false) | Standard tooling semantics; binary presence verified (`/usr/bin/shasum`), command behavior not verifiable by grep. |
| `PYTORCH_ENABLE_MPS_FALLBACK` runtime effect (38-04:20) | UNCHECKABLE (severity INFO, hardBlock false) | Env-var runtime semantics external to repo; the capture-before-import PATTERN is VERIFIED at `componentwise_ad.py:30-41`. |
