---
title: Trainex R1b Findings — Runbook and Operations Knowledge for CTL-PINN Training Execution
package: trainex-r1b
status: deliverable
date: 2026-06-12
research_basis: attached files (RESEARCH-CONTEXT-MASTER.md, 2026-06-10-training-execution-design.md, pinn_architecture.md, ctl_instruction.md) + primary web sources verified 2026-06-12
companion: trainex-r1a (decision menus; consumes K4 estimates at consolidation)
self_contained: true
---

# Trainex R1b Findings — Runbook and Operations Knowledge

All findings in this document were verified or derived on **2026-06-12**. Every external claim carries a numbered citation; sources are listed in full at the end (§8). Anything that could not be verified from primary sources, and every ambiguity found in the attached project documents, is listed in the claims-and-uncertainty register (§7) rather than asserted. Findings that imply a project decision are stated as observations with evidence in §6 — not adjudicated.

**How this document maps onto the design's surfaces.** The training-execution design (`2026-06-10-training-execution-design.md`) commits to five user entry points — Setup, Configure, Launch, Monitor, Resume — and three monitoring surfaces: the live terminal log, the dashboard (TensorBoard per `ctl_instruction.md` Implementation Notes), and the Mac system monitor (Activity Monitor). Each topic below states explicitly which entry point or surface a finding feeds. Topic order follows priority: K4, K5, then K1, K2, K3.

---

## 1. K4 — Training Feasibility Envelope (highest priority)

### 1.1 What is being estimated, and from what

The question is whether one curriculum stage and one full curriculum run on the project's MacBook mean **hours, days, or weeks**. The estimate below is built from three legs: (a) the committed architecture and AD contract in `pinn_architecture.md`, from which parameter counts and the per-step arithmetic structure are derived exactly; (b) the curriculum staging and per-stage optimization protocol in `ctl_instruction.md`, from which the per-step sample counts are taken and the steps-per-stage range is bounded; and (c) the 2025–2026 Apple-Silicon training-throughput evidence base, which — this is the central honest finding — does **not** contain a published benchmark close enough to this workload (a ~0.7M-parameter MLP whose every training step requires second-order automatic differentiation) to pin the per-step time tighter than about a factor of 30. The estimate is therefore delivered as a parameterized envelope plus a named, cheap measurement (the K5 smoke test, §2 rung 6) that collapses the envelope to a real forecast in five minutes. The R1a "first-run recipe" should treat the smoke-test measurement as the join point.

### 1.2 Derived workload structure (exact, from the attached specs)

**Network size.** `pinn_architecture.md` Table 1 commits 12 hidden layers × 256 neurons, 14-dimensional input, 9-dimensional linear output head, LayerNorm with no learnable parameters (`elementwise_affine=False`). The parameter count follows directly:

| Component | Calculation | Parameters |
|---|---|---:|
| First layer (14 → 256) | 14·256 + 256 | 3,840 |
| Hidden layers 2–12 (256 → 256, ×11) | 11·(256·256 + 256) | 723,712 |
| Output head (256 → 9) | 256·9 + 9 | 2,313 |
| **Total** | | **≈ 729,900 (~0.73 M)** |

That is ≈ 2.9 MB of weights in float32, ≈ 8.8 MB with Adam's two moment buffers. **This is a small model.** Memory is not the binding constraint on the 24 GB machine (see §1.6); wall-clock per step is.

**Per-sample forward cost.** One forward pass ≈ 2 × params ≈ **1.5 MFLOP per sample** (the LayerNorm and element-wise squaring on the six odd skip paths add < 1% and are ignored).

**Per-step sample counts (spec defaults).** From `pinn_architecture.md` §3.1 Listing 2 and `ctl_instruction.md` "Mini-Batch Construction": data branch N_data = batch 256 trajectories × 32 points = **8,192 samples**; collocation branch N_col = **2,048–4,096 points** (Listing 3, "recommended: 2048–4096"); IC branch = 256 samples at u = 0. Note that the author of `pinn_architecture.md` has flagged the batch-construction listing as "not consistent with the CTL instruction plan" (SI-PINN-003); the estimate below parameterizes over N_data and N_col precisely so that the eventual reconciliation moves the answer rather than invalidating it.

**The dominant cost term: second-order AD per collocation point.** The PHYS-02 contract requires, at every collocation point, all nine componentwise first derivatives dr′/du and all nine second derivatives d²r′/du² with respect to the scalar time leaf u, with the sum-trick VJP explicitly forbidden, followed by backpropagation of the total loss through that double-derivative graph to the ~0.73 M parameters. How many forward-pass-equivalents (FE) this costs per collocation point depends enormously on the AD pattern — and the spec's two named "acceptable patterns" sit at the expensive end of the range:

| AD pattern for (v′, a′) per collocation point | Approx. cost, forward-equivalents incl. parameter backward | Notes |
|---|---:|---|
| Forward-over-forward (jvp of jvp w.r.t. the scalar u) | ~8–20 | One tangent pass yields all 9 components at once because u is a **scalar**; cheapest known structure. Qualifies as the spec's "equivalent full-Jacobian method" — see decision observation D-4. |
| `jacrev` + `vmap` (spec pattern A) | ~30–80 | 9 reverse passes for v′, then reverse again through the enlarged graph for a′. |
| Explicit 9-component Python loop (spec pattern B) | ~60–200 | Same arithmetic as above plus per-component graph/dispatch overhead; on GPU backends the kernel-launch overhead of many tiny ops can dominate the FLOPs entirely. |

Call this multiplier κ. PINN literature independently documents that residual evaluation cost grows superlinearly with depth and derivative order and that the PDE-loss branch dominates training cost and peak memory [12]; the table is consistent with that.

**FLOPs per training step** (data branch ≈ 3 FE per sample for forward+backward; IC branch ≈ 6 FE; collocation branch κ FE):

FLOPs_step ≈ [ N_data·3 + 256·6 + N_col·κ ] × 1.5 MFLOP

| Scenario | N_col | κ | GFLOP / step |
|---|---:|---:|---:|
| Efficient AD, small collocation | 2,048 | 10 | ≈ 70 |
| Efficient AD, large collocation | 4,096 | 10 | ≈ 100 |
| Spec-pattern reverse AD | 4,096 | 60 | ≈ 400 |
| Naive per-component loop | 4,096 | 150 | ≈ 930 |

### 1.3 Hardware leg: what is actually known about the machine (2026-06-12)

The attached design states the machine as "M5 Pro: 16 CPU cores, 15 GPU cores, 24 GB unified." Apple's shipping M5 Pro configurations (announced 2026-03-03, available 2026-03-11) are a **15-core CPU / 16-core GPU** base part and an 18-core CPU / 20-core GPU upgrade, with 24 GB or 48 GB unified memory and **307 GB/s** memory bandwidth [1][2][3]. No shipping M5 Pro matches "16 CPU / 15 GPU"; the numbers appear transposed. The estimates below assume the base 15-CPU/16-GPU/24 GB part (closest match). This is decision observation D-1: confirm the actual hardware before R1a consolidation.

Apple does not publish FP32 TFLOPS for the M5 Pro GPU, and no primary benchmark of this workload class on M5-generation silicon was found (claims register C-9). Two well-evidenced qualitative facts stand in for a single number. First, for small-tensor workloads, framework dispatch overhead — not peak FLOPs — frequently dominates on Apple-Silicon GPU backends; per-operation benchmark suites show order-of-magnitude spreads between MLX-GPU, PyTorch-MPS, and CPU depending on op type and size [8][9][10]. Second, a 2025 profiling study of ML training on Apple Silicon found PyTorch-MPS missing training-path optimizations that are mature on CUDA, with FP16 giving MPS essentially no speedup and MLX only 20–30% [10] — so float32 throughput is the planning basis. The envelope below therefore brackets the *effective* sustained throughput for this workload at **0.2–3 TFLOPS** on the GPU path and treats anything tighter as unknowable without measurement. The CPU path (15 cores) is plausibly within a factor of a few of the dispatch-bound GPU path for a model this small — genuinely an empirical question (see the framework branching in §1.5).

Per-step wall-clock under that bracket:

| | Effective 3 TFLOPS | 1 TFLOPS | 0.2 TFLOPS |
|---|---:|---:|---:|
| 100 GFLOP/step (efficient) | 0.03 s | 0.10 s | 0.5 s |
| 400 GFLOP/step (spec-pattern) | 0.13 s | 0.40 s | 2.0 s |
| 930 GFLOP/step (naive) | 0.31 s | 0.93 s | 4.7 s |

Additionally, in dispatch-bound regimes (the naive per-component loop launching hundreds of small Metal kernels per step), measured step time can exceed the FLOP-derived figure by several × — which is why the bracket's pessimistic corner below is taken at **5 s/step**. Headline parameterization: **t_step ∈ [0.03 s, 5 s], central expectation 0.1–1 s** for a competently vectorized float32 implementation on the GPU path. *The smoke test measures t_step directly and replaces this entire subsection.*

### 1.4 Steps per stage and per full run (from `ctl_instruction.md`)

The spec never states an epoch or step count per stage; Adam terminates on a plateau criterion (physics-loss log-slope > −5×10⁻³ for 50 consecutive epochs) and stage advancement requires four validation criteria. One indirect anchor exists: the PHYS-05 warmup schedule sets I_warm = min(2000, 0.1·N_Adam,k), which only makes sense if the designers envisioned N_Adam,k ≳ 20,000 Adam iterations per stage (otherwise the min never binds). General PINN practice runs 10⁴–10⁵ Adam steps before quasi-Newton refinement [13]. Parameterization: **S_Adam ∈ [10⁴, 10⁵] steps per stage**, central 2–5×10⁴ (claims register C-1).

L-BFGS refinement adds full-batch iterations (stages 0–2: history 10, Wolfe line search, max 20–50 iterations) or mini-batch sL-BFGS (stages 3–6). With 2–4 loss evaluations per line-searched iteration and full-batch cost proportional to the cumulative stage dataset, the L-BFGS phase is typically 5–20% of the Adam phase's wall-clock for early stages — but see the stage-2 memory flag in §1.6.

Stage count: the curriculum defines stages 0–6, with sub-stages 1a/1b and 4a/4b. Whether sub-stages are separate optimization segments (9 segments total) or merged (7) is not stated (claims register C-5). **Segments ∈ [7, 9].**

**Full-run envelope** (segments × S_Adam × t_step, +10% L-BFGS):

| Scenario | Total Adam steps | t_step | Wall-clock |
|---|---:|---:|---:|
| Optimistic (7 × 10⁴, efficient AD, fast device) | 70 k | 0.03 s | **≈ 0.7 h** |
| Central-low (8 × 2.5×10⁴) | 200 k | 0.1 s | **≈ 6 h** |
| Central-high (8 × 5×10⁴) | 400 k | 0.5 s | **≈ 2.5 days** |
| Pessimistic (9 × 10⁵, spec-pattern AD, throttled/dispatch-bound) | 900 k | 2 s | **≈ 21 days** |
| Worst credible (naive loop, plateau criteria never bite early) | 900 k | 5 s | **≈ 52 days** |

**One stage** is correspondingly **minutes-to-days, central a few hours** (e.g., 2.5×10⁴ steps × 0.1–1 s ≈ 0.7–7 h).

### 1.5 Per-framework branching (all three candidates, status verified 2026-06-12)

These are findings that condition the estimate, not framework recommendations (the decision lives in R1a/PH-1).

**PyTorch + MPS.** The MPS backend does not support float64 at all — Metal-stack GPU compute is float32/float16 only across Apple's frameworks [4][14]. Anything the specs require in float64 (the S_H scale is computed "once in float64" per PHYS-04) must run on CPU; that particular computation is one-time preprocessing and is unproblematic, but if the project's open precision adjudication lands on float64 anywhere *inside* the training loop, the GPU path is excluded entirely (decision observation D-3). Double-backward (create_graph) support on MPS has a documented history of per-op gaps — `linear_backward`'s second derivative was missing as late as PyTorch 2.0 and fixed later; pooling ops retained gaps [5] — so the K5 AD probe must run **on the MPS device**, not on CPU, before any long run (D-13). The estimate above applies with the κ table as given; `torch.func.jacrev` + `vmap` (the spec's pattern A) is the realistic mid-range. Silent-correctness regressions on MPS tied to both macOS updates and PyTorch version bumps are documented repeatedly [6][7][15][16] — this drives K2's upgrade discipline rather than the duration estimate.

**MLX.** Composable grad-of-grad is a first-class design feature (`mx.grad(mx.grad(f))` is documented and supported to arbitrary order) [8], and unified memory is native, so the AD contract is structurally satisfiable. The documented practical friction (March 2025, still open as a feature gap as of the last check) is exactly this project's pattern: per-component input Jacobians across a batch of collocation points fall back to Python loops that break under `mx.compile`, and no built-in batched-Jacobian (`jacfwd`/`jacrev` equivalent) existed [9]. Uncompiled MLX runs the loop correctly but lands in the dispatch-bound (high-κ) corner of the envelope. GPU compute is float32/16; float64 is unavailable on the GPU path (C-10).

**JAX (+ Optax + Equinox).** The decisive 2025–2026 development: Apple's `jax-metal` plugin is **effectively dead** — maintainers closed its issues in December 2025 citing no active development, and the plugin fails to run on recent macOS versions [17][18]; Apple's own compatibility page still lists float64 as unsupported and the plugin as experimental [4]. A community PJRT plugin (`jax-mps`, built on MLX) exists as of May 2026 but is explicitly experimental, pinned to specific jaxlib versions, and reports only ~3.7× over CPU on a ResNet18 example [19][20]. **For planning purposes, "JAX on this Mac" means the CPU backend** (which does support float64 via `jax_enable_x64`, and where `jax.jacfwd`/forward-over-forward Hessians are ergonomic and compiled). For a 0.73 M-parameter MLP with scalar-input second derivatives, JIT-compiled CPU JAX on 15 performance-class cores is plausibly within the same order of magnitude as the dispatch-bound GPU paths — only the smoke-test measurement can rank them (D-2).

### 1.6 Memory footprint

Steady-state training memory decomposes as: weights + Adam state ≈ 10 MB; per-step activation and AD-graph storage ≈ (N_data + N_col × graph-depth factor 3–8) × ~12 kB/sample ≈ **0.2–0.6 GB**; the dataset held in RAM — 15,028 trajectories whose per-trajectory snapshot count is unknown (dt_out is specified as 0.08/0.17/0.01 code units but t_max is not; claims register C-2) — ≈ **0.3–3 GB** in float32 depending on snapshot counts; Python + framework + Metal runtime ≈ 1–3 GB. **Total expectation 2–7 GB, comfortably inside 24 GB.** Two genuine memory risks, both flagged as decision observations: (i) the MPS allocator's cached memory grows over long runs and the design's "swap used and growing" stop rule is the correct user-visible guard — the trainer should expose `torch.mps.empty_cache()`-style hygiene internally; (ii) **full-batch L-BFGS at stage 2** spans the cumulative dataset *including* high-resolution Set 2a (2,749 trajectories at 8× temporal density) — a single full-batch loss-plus-gradient evaluation with 9-component second-derivative residuals over millions of points will exceed 24 GB unless gradient accumulation / chunked evaluation is used; "full-batch" needs an executable definition (D-7).

### 1.7 Numbers the project must supply to tighten the estimate

1. **Measured t_step** from the K5 smoke test, per candidate framework and device — collapses a 30× uncertainty; single highest-value number.
2. Realized steps-to-plateau on a real stage-0 run (the spec's own author note says transition criteria are theoretical until stage 0 is attempted).
3. N_col default (2,048 vs 4,096 vs other).
4. Reconciled N_data per step (resolves SI-PINN-003: 256×32 batch construction vs CTL plan).
5. Stage population counts after invariant binning of the 15,028 trajectories (the spec's own author note proposes a data scan before fixing thresholds).
6. Snapshots per trajectory / t_max (memory leg and full-batch L-BFGS cost).
7. Whether sub-stages 1a/1b/4a/4b are separate optimization segments.
8. L-BFGS max-iteration and line-search-evaluation counts actually configured.
9. Resolution of the numerical-precision contract (float32-GPU vs float64-anywhere-in-loop — branches the device choice entirely).
10. Validation-evaluation cadence and cost (each stage-advance check evaluates the hold-out split; at 10–20% of cumulative data this is non-trivial late in the curriculum).

### 1.8 Outcome ranges that pressure the no-cloud constraint, and downstream implications

The constraint comes under pressure when **a single full curriculum run exceeds roughly two weeks** of continuous laptop time — the pessimistic-to-worst corner of §1.4 (t_step ≳ 2 s and/or ≳ 10⁵ steps per stage). The pressure is flagged here, not designed around. What it would imply downstream:

- **Checkpoint cadence (feeds R1a's checkpoint policy):** the maximum tolerable loss on interruption is checkpoint_every × t_step. The design's default checkpoint_every = 1,000 means 100 s of lost work at t_step = 0.1 s but **83 minutes** at 5 s/step. A wall-clock-based cadence (e.g., every 15–30 min) is robust across the whole envelope; a step-based default is only safe after t_step is measured.
- **Thermal planning (feeds K2):** central-band runs (≤ 2.5 days) are ordinary unattended-laptop territory; multi-week runs make sustained-load thermal behavior, lid/sleep policy, and the upgrade freeze (K2) load-bearing rather than precautionary, and make a hard-surface, ventilated, AC-powered, lid-open station mandatory rather than recommended.
- **Monitoring rhythm (feeds K1 and the design §6.1):** the design's "every ~5 minutes" health glance suits hour-scale runs. For day-scale-plus runs the rhythm becomes: smoke-test forecast at launch → first 30 minutes watched live → thereafter a twice-daily check of the terminal tail, the dashboard per-term curves, and Activity Monitor swap/thermal state, plus the K1 watchlist as the triage table.
- **If the worst corner materializes**, the in-scope mitigations are implementation-side (the κ column: forward-mode AD, vectorization, `mx.compile`/`torch.compile` where supported, smaller N_col early) before any constraint-level conversation; the κ spread of ~15× is larger than the device spread.

---

## 2. K5 — Trainer-Correctness Verification Ladder (co-priority)

### 2.1 Why a ladder, and what it must catch

PINN trainers fail silently: a residual sign error, a wrong coordinate frame, a chain-rule factor applied on the wrong leaf, or a missing double-backward kernel can all produce smooth, decreasing loss curves while the learned physics is garbage. This is not hypothetical for this project — the failure classes are documented in the literature (loss-landscape pathologies that make even correct implementations converge to wrong solutions [11][12][13]), and the spec itself encodes three trap doors: the forbidden sum-trick VJP (PHYS-02), the conditional 2×/4× chain-rule factors that apply only on the τ-leaf path, and the MPS per-op double-backward gaps (§1.5). The operator cannot eyeball wrong physics; the ladder below is the mechanical substitute. It is ordered cheapest-first, each rung assuming the ones below it passed, and is written to lift directly into the runbook's pre-flight section (Launch entry point: the rule is **no run longer than 30 minutes may start unless every rung is green on the current environment**).

The three-body domain is unusually well-suited to rung 5: exact and special reference solutions exist whose parameterizations are verified from the literature below.

### 2.2 The ladder

| # | Rung | What it catches | Pass criterion | Cost |
|---|---|---|---|---|
| 0 | **Environment & device sanity.** One command prints framework version, device availability, and a 10-element tensor round-trip on the training device. | Broken install; MPS unavailable after an OS/framework change [16]; wrong environment activated. | Exact expected output printed (versions match the lockfile; device reports available). | seconds |
| 1 | **Componentwise AD probe vs. analytic derivatives, on the training device.** The spec's own synthetic trajectory (§10.3 / PHYS-02): r′(u) = [sin 2πu, cos 2πu, u²], comparing AD-computed dr′/du and d²r′/du² against the closed-form derivatives, in the exact code path the trainer uses (same jacrev/vmap or loop, same device, same dtype). | The forbidden sum-trick VJP; τ-vs-u leaf confusion (missing or spurious 2×/4× factors); missing/incorrect double-backward kernels on MPS [5]; silent CPU fallback changing semantics. | Spec tolerance: relative error < 10⁻⁶. Caveat: in float32 on GPU, second derivatives may legitimately land near 10⁻⁵–10⁻⁶; run the identical probe in float64 on CPU as the reference arm and require the float32-device arm within ~10⁻⁴ of it (tolerance split is a project decision — D-13, C-6). | < 1 min |
| 2 | **AD-vs-finite-difference gradient checks, float64 on CPU.** Two layers, following standard practice of running gradient checks in double precision because finite differencing magnifies float32 noise [21]: (a) network-output derivatives w.r.t. u vs. central differences (step h ≈ ε_machine^(1/3) for first derivatives); (b) the gradient of the *total loss* w.r.t. parameters vs. finite differences on a tiny copy of the network (e.g., 2×32 layers) — PyTorch ships this as `torch.autograd.gradcheck` / `gradgradcheck` [21]; JAX/MLX equivalents are a 20-line utility. | Residual-assembly wiring errors that rung 1's pure-kinematics probe cannot see; loss terms accidentally detached from the graph; `stopgrad` placed on the wrong tensor in the causal weights. | Relative error < 10⁻⁵ (float64). | minutes |
| 3 | **Residual-on-ground-truth zero check.** Take one BRUTUS trajectory from the dataset; feed its *true* positions (not network output) through the trainer's force-assembly code and compare against finite-difference accelerations of the same trajectory. Independently, run the spec's own §10 probes: scaling consistency (< 10⁻¹⁰), COM projection (|COM| < 10⁻¹⁰), force–energy consistency (−∇H_ε matches the residual force, < 10⁻⁵), and the loss-stability dry run (all five terms finite on random inputs). | Sign errors in the residual; wrong frame (non-COM data reaching the loss); mismatched softening between force and Hamiltonian (ε_train must be the same 10⁻⁵ in both per PHYS-04); unit/scaling errors in D and T. | Residual on ground truth ≈ 0 to integrator+FD tolerance (≲ 10⁻⁴ in scaled units at the BRUTUS dt; looser for the dt = 0.17 low-fidelity set); spec probes at their stated thresholds. | minutes |
| 4 | **Overfit-a-single-batch.** Train on exactly one trajectory (then a handful) with the full loss for a few thousand steps. A correctly plumbed trainer with a 0.73 M-parameter network must drive data loss to ≈ 0 and the physics residual down by orders of magnitude on so small a problem; failure to overfit a single batch is the classic signature of a plumbing bug, not a capacity limit — a first-class step in the standard neural-net troubleshooting recipe [22]. | Optimizer wiring (LR schedule, Adam state, clipping) bugs; data-loader/label misalignment; loss-weight schedule errors; the LayerNorm-skip-path implementation. | Data loss < 10⁻⁶ (scaled Huber) and physics loss ↓ ≥ 3 orders of magnitude within ≤ 5,000 steps on one trajectory (exact thresholds: project decision, D-15). | 5–20 min |
| 5 | **Known-solution fixtures** (§2.3 below). Train (or fine-tune) the trainer on each fixture's IC, pushed through the same Phase 18 preprocessing pipeline as BRUTUS data, and require the predicted trajectory to reproduce the analytic/reference orbit. | Everything the synthetic rungs cannot: end-to-end correctness of preprocessing → IC13 encoding → conditioning → physics, on dynamics with known truth. A trainer that fits BRUTUS data but cannot reproduce the Lagrange circle has a physics or frame bug, full stop. | Proposed (project decision, D-15): scaled-position RMSE over one period < 10⁻³ for Lagrange/Euler, < 10⁻² for the figure-eight; energy drift |ΔH| < 10⁻⁴ throughout; for the figure-eight, ‖L(t)‖ stays ≈ 0 in absolute terms (see the L_scale caveat in §2.3). | 0.5–2 h per fixture |
| 6 | **The ~5-minute smoke test** — a first-class runbook step, the cheapest *end-to-end* rung. A real launch with a tiny budget: stage-0 subset (e.g., 32 trajectories), N_col = 256, ~300 steps, checkpoint_every = 100. Verifies the full mechanical surface: the `runs/<name>/` directory appears with config copy, logs, checkpoints; loss lines print with all five terms finite; one Ctrl-C produces a graceful checkpoint; `--resume` continues from it; and **the measured s/step is recorded** — this number feeds straight into the K4 forecast (forecast = planned steps × measured t_step; D-5). | Launch/Resume entry-point breakage; run-directory contract violations; the dispatch-bound performance corner (a smoke test at 5 s/step is the early warning that the full run means weeks); environment drift after any upgrade (K2). | All design-§5.7 files appear; all loss terms finite for 300 steps; resume reproduces step count and loss continuity; s/step recorded into `runs/<name>/summary.json`. | ~5 min |

Where it lands among the entry points (K3 mapping): rungs 0–3 are a **Setup-verification script** run once per environment and re-run after any upgrade (K2); rungs 4–6 are the **Launch pre-flight**, with rung 6 mandatory before every real run and rungs 4–5 mandatory before the *first* real run and after any code change to loss/AD/preprocessing.

### 2.3 Known-solution fixtures: verified parameterizations and convention mapping

All three fixtures are stated in the G = 1, equal-mass (m₁ = m₂ = m₃ = 1) nondimensional convention, which matches the spec's unit system directly (raw-mass nondimensionalization, G absorbed). All are planar (z = 0); the spec's pipeline is 3-D with Jacobi velocities "fully 3D" (`ctl_instruction.md` Step 2), so planar fixtures are admissible inputs with zero z-components. **Fixtures must enter through the same Phase 18 preprocessing (COM removal, zero-momentum boost, canonical ordering/rotation, scaling, IC13 assembly) as BRUTUS data — never as hand-built IC13 vectors** — otherwise the fixture validates the network but not the pipeline. All three are exact solutions of the *unsoftened* Newtonian equations; with the training softening ε_train = 10⁻⁵ and inter-body distances of order 1, the Plummer perturbation is of relative size (ε/d)² ≈ 10⁻¹⁰ — far below every pass threshold, so the fixtures remain valid against the softened residual.

**Fixture A — Lagrange equilateral solution (Lagrange 1772; standard reference: Murray & Dermott, *Solar System Dynamics*, 1999, central configurations).** Three bodies at the vertices of an equilateral triangle of side d rotate rigidly about the COM with angular velocity ω satisfying **ω² = G(m₁+m₂+m₃)/d³** — valid for arbitrary masses. Equal-mass concrete instance (m = 1, G = 1, d = 1): each body at distance R = d/√3 from the origin, e.g. r₁ = (1/√3, 0), r₂ = R(cos 120°, sin 120°), r₃ = R(cos 240°, sin 240°); velocities v_i = ω ẑ × r_i with ω = √3; period T = 2π/√3 ≈ 3.6276. Smoothest fixture; the trainer should nail it. *(The ω² = GM/d³ relation is classical and derivable in three lines; cited to the standard text rather than a primary 1772 source — see C-7.)*

**Fixture B — Euler collinear solution, equal-mass instance (Euler 1767; same standard references).** Bodies at (−a, 0), (0, 0), (+a, 0) rotating rigidly about the origin. Net force on an outer body = Gm²/a² + Gm²/(2a)² = (5/4)Gm²/a², so **ω² = (5/4)Gm/a³**; the central body sits at the COM force-free. Concrete instance (m = 1, a = 1): ω = √(5)/2 ≈ 1.1180, T = 2π/ω ≈ 5.620; outer velocities (0, ±ω·a), central velocity 0. For unequal masses the spacing satisfies Euler's quintic — out of scope; the equal-mass instance suffices as a fixture. Note this configuration is dynamically *unstable*: tiny errors grow, which is exactly what makes it a sharper test than Fixture A over one period.

**Fixture C — the figure-eight choreography (discovered numerically by Moore 1993; existence proved and initial conditions published by Chenciner & Montgomery 2000, with the numerical values due to Carles Simó) [23][24].** Equal masses, zero angular momentum, all three bodies chasing each other on one figure-eight curve. Verified initial conditions, exactly as printed in Chenciner & Montgomery (Annals of Mathematics 152, 2000; arXiv:math/0011268) [23]:

```
m1 = m2 = m3 = 1,  G = 1
x1 = ( 0.97000436, -0.24308753, 0)      x2 = -x1      x3 = (0, 0, 0)
v3 = (-0.93240737, -0.86473146, 0)      v1 = v2 = -v3/2
Period T = 6.32591398
```

(Sources differ by an overall reflection/sign convention — e.g., x₁ = (−0.97000436, 0.24308753) with the matching velocity signs appears in secondary literature [24][25]; both describe the same orbit. Use the Chenciner–Montgomery printing above as canonical.) COM = 0 and total momentum = 0 hold exactly by construction, so the fixture is already in the spec's frame before preprocessing.

**Convention flags discovered while mapping fixtures to the attached specs** (recorded per the research contract rather than improvised around):

- **Zero angular momentum vs. the L_L loss scale.** The angular-momentum loss normalizes drift by L_scale = ‖L₀′‖ + ε_L with ε_L = 10⁻⁸ (`pinn_architecture.md` §3.5). For the figure-eight, ‖L₀′‖ = 0 exactly, so L_scale = 10⁻⁸ and any absolute drift of, say, 10⁻⁶ becomes a *relative* drift of 100 — the L_L term would dominate the loss by orders of magnitude on this fixture. This is not a spec bug for BRUTUS data (generic trajectories have L₀ ≠ 0) but it makes the figure-eight unusable under the default loss without a fixture-specific accommodation (evaluate L conservation as an absolute metric for this fixture, or exclude L_L). Recorded as D-6 / C-8.
- **Energy slot of IC13.** The fixtures' energies are computable in closed form (Lagrange d = 1 equal-mass: V = −3, T_kin = 3·½ω²R² = ½·3·(1/3)·3 = 1.5, E = −1.5; verify in code rather than trusting this arithmetic) and must pass through the same tanh(E/E_scale) normalization with the *dataset's* E_scale — a fixture evaluated with a different E_scale than training silently changes the conditioning input (C-8).
- **Characteristic time T = t_max.** The spec scales time by the dataset's t_max. A fixture trained standalone over exactly one period uses T = its own period; a fixture evaluated *inside* the main pipeline inherits the dataset T. The runbook step must say which (D-6).

---

## 3. K1 — PINN Training-Health Watchlist and Failure Modes

### 3.1 Evidence base

The documented failure modes of PINN training, verified against the primary literature on 2026-06-12, group into five families, each of which maps onto a signal visible on one of the design's three monitoring surfaces (terminal loss lines / dashboard curves / system monitor):

1. **Loss-term imbalance and gradient pathologies.** Multi-term PINN losses develop stiff gradient imbalances — one term's gradients dwarf another's — causing convergence to solutions that fit data but violate physics or vice versa (Wang, Teng & Perdikaris 2021 [11]; the NTK analysis showing the terms converge at intrinsically different rates: Wang, Yu & Perdikaris, J. Comput. Phys. 449:110768, 2022 [12]).
2. **Hard-to-optimize loss landscapes / apparent convergence to wrong solutions.** Even expressive networks fail on modestly harder PDE regimes because the soft physics constraint ill-conditions the landscape; curriculum regularization is one of the two canonical mitigations (Krishnapriyan et al., NeurIPS 2021 [13]) — this project's CTL design is itself an instance of that mitigation, which means *stage transitions are where this failure family concentrates*.
3. **Propagation failure / trivial solutions.** Time-dependent PINNs can satisfy the residual near the initial condition and collapse to a trivial or constant solution at later times; the solution must "propagate" from the IC outward, and poor sampling or weighting leaves it stuck (Daw et al. 2023 [26]; theoretical and empirical treatments of trivial fixed points cited therein). Causal weighting (Wang, Sankaran & Perdikaris, CMAME 421:116813, 2024 [27]) — which this project adopts as the default L_phys — is the canonical mitigation, **and it introduces its own observable failure mode: causal-weight collapse**, where a stubborn early-time residual drives w_n = exp(−η_c Σ R̄) toward 0 for all later points and training silently stops covering most of the time domain (the spec's required exponent clipping prevents underflow, not collapse).
4. **Divergence and instability events.** NaN/Inf from the 1/r³ force terms during close encounters (bounded but enormous at r_safe → ε_train = 10⁻⁵: force magnitudes up to ~10¹⁰ in scaled units), gradient explosions, and post-stage-transition divergence from distribution shift plus λ re-warmup.
5. **Generalization-level failures** — memorization, mode collapse, energy drift, chaos-blindness — already enumerated at the outcome level in design §6.5; the watchlist below covers their *in-run* precursors.

### 3.2 The watchlist (signal → what it likely means → first response a non-expert can take)

Surface key: **T** = terminal log line (step, five loss terms, lr, s/step, ETA per design §5.4), **D** = dashboard (TensorBoard per-term curves; `ctl_instruction.md` requires logging all five terms, scheduled λ values, gradient statistics, and conservation metrics), **S** = system monitor (Activity Monitor / `powermetrics`).

| Signal (where) | What it likely means | First response (non-expert) |
|---|---|---|
| Total loss jumps sharply exactly at a stage boundary (T, D) | **Scheduled, usually not a failure**: the new stage re-warms λ_phys/λ_E/λ_L and resets Adam state per spec; λ_E and λ_L switch on at stage 2 (0 → 10⁻² per PHYS-05), which steps the total. | Look at the *unweighted per-term* curves, not the total. If each term resumes a downward trend within ~2,000 steps, keep watching. Record the boundary step in the run notes. |
| Per-term curves: data loss falls, physics loss flat or rising for >10k steps (D) | Loss-term imbalance [11][12]: the network is fitting trajectory points while ignoring the ODE — the classic "clean loss curve ≠ correct physics" precursor. | Confirm the λ warmup actually ramped (dashboard logs scheduled λ values). If λ_phys is at max and physics is still flat, stop at the next checkpoint and report; do not hand-tune weights mid-run. |
| Physics loss falls, data loss flat at a high value (D) | Possible trivial/over-smooth solution satisfying the ODE without tracking trajectories (failure family 3) — or data pipeline mis-scaling. | Run the rung-4 single-trajectory overfit on the current code. If that passes, report as suspected propagation/imbalance issue. |
| Residual low near u = 0, large at later u; or the residual-vs-time plot never flattens beyond early times (D — *requires a per-time-bin residual panel, see D-9*) | Propagation failure [26]: the solution hasn't propagated from the IC anchor. | Check the causal-weight diagnostic (next row). If weights are healthy, this usually resolves with more steps in-stage; if it persists to the plateau criterion, report before advancing stages. |
| Causal-weight diagnostic: mean/min w_n ≈ 0, or "fraction of w_n > 0.5" stuck near 0 for many epochs (D — *requires logging w_n statistics, see D-9*) | Causal-weight collapse: an unresolved early-time residual is gating the entire later domain; training is effectively frozen on the first time bins [27]. | Note the step and the w_n statistics, keep the run alive (it is not diverging), and report. (Spec-level remedies — η_c, sampling — are project decisions, not operator moves.) |
| NaN/Inf in any loss term (T) | Divergence: close-encounter force blow-up or LR too high; the spec's adaptive median clipping (C = 7–10 early, 3 late) should normally absorb spikes. | Design §5.8 row applies: Ctrl-C, restore last good checkpoint, restart; if it recurs at the same curriculum stage, report with the log tail. Never resume past a NaN without restoring. |
| Loss oscillates violently, no trend; gradient-norm log shows clipping firing every step (T, D) | LR too high for the stage, or clip threshold C mismatched to the stage's difficulty schedule. | Verify the config's LR matches the spec's LR_k = 10⁻³·0.7^k for the current stage k (the terminal prints lr). If it matches, report; if it doesn't, the config is wrong — fix and restart from checkpoint. |
| Validation loss rises while training loss falls, sustained across evaluations (D) | Memorization (design §6.5) — in-run precursor. | Note the step where val bottomed; the stage-advance criterion 2 (val ≤ running min) will correctly refuse to advance. If stuck >2× the patience window, stop and report. |
| Energy-drift metric trends upward during training (D — conservation metrics are required logging) | The soft conservation regularizers are losing to the other terms; precursor of the gate's ε_H failure. | Confirm λ_E is nonzero for the current stage (it is 0 by schedule in stages 0–1 — drift there is *expected and unpenalized*). From stage 2 on, persistent upward drift is reportable. |
| s/step drifting upward over hours (T) | Thermal throttling (K2 §4.2), memory pressure/swap, or MPS allocator growth. | Check S: Activity Monitor → Memory (swap growing? stop at checkpoint, restart) and fan/CPU-temp state (hot room/soft surface? fix environment per K2; the run can continue). |
| GPU utilization ≈ 0% during training (S) | Training silently on CPU — wrong device in config, MPS unavailable after an update, or a per-op CPU fallback (`PYTORCH_ENABLE_MPS_FALLBACK`) capturing the hot path [5][16]. | Check the launch banner ("Found device: mps"). If it said mps but GPU is idle, stop, run ladder rung 0–1, report. Note: for this small model some GPU-residency dips are normal — compare against the smoke test's baseline, not an absolute 60–95% band (D-11). |
| Step number frozen ≥ 5 min, no new lines (T) | Hung run (design's hard rule). | Design §5.8: Ctrl-C, read log tail, restore checkpoint, restart. |
| "Swap used" nonzero and growing (S) | Memory leak or dataset/full-batch phase exceeding RAM (§1.6). | Design §6.1 rule: stop at checkpoint; if it happened during an L-BFGS phase, report that specifically (D-7). |

Two notes for the runbook's framing of this table. First, the operator's job at every row is *name → bounded action → report*, never diagnose-and-tune — this matches the design's stated philosophy ("the user does not need to fix these — they need to name them") and the SRE evidence on why pre-written responses beat improvisation (§5). Second, the watchlist's first row exists because curriculum training makes scheduled discontinuities *normal*; a watchlist that doesn't say so trains the operator to panic at every stage boundary.

---

## 4. K2 — Unattended Training Operations on a MacBook (macOS 15-era, verified 2026-06-12)

### 4.1 Sleep, lid, and terminal survival

**Preventing sleep: `caffeinate` is the official, built-in tool** (shipped in /usr/bin, documented in its man page) and the standard current practice for long unattended compute on macOS [28][29]. The runbook-ready pattern is to wrap the training command so the sleep assertion lives exactly as long as the run:

```
caffeinate -is python -m pinn.train --config configs/runs/my-run.yaml
```

(`-i` prevents idle system sleep; `-s` prevents system sleep while on AC power; the assertion ends automatically when training exits.) The design's §5.10 note "use `caffeinate -d`" prevents *display* sleep, which is unnecessary for a terminal run and wastes power — `-is` is the better default (D-10).

**Lid close is not survivable by default.** On Apple Silicon laptops, closing the lid sleeps the machine regardless of `caffeinate` unless the Mac is in **clamshell mode** — which Apple supports only with all three of: AC power, an external display, and an external keyboard/mouse [28][29]. The blunt alternative `sudo pmset -a disablesleep 1` does keep a closed-lid Mac awake but disables sleep globally until reversed and is widely cautioned against for thermal reasons (the closed chassis sheds heat worse) [28][29]. **Finding for the runbook:** the Launch step should state "leave the lid open and the Mac on AC power for the whole run; closing the lid pauses training mid-step." The design's current stop-rule text — "MacBook sleep / lid close → training continues when lid reopens" — is optimistic: the process is suspended, GPU work may or may not resume cleanly across sleep, and the reliable recovery path is checkpoint-resume, not wake-and-hope (D-10).

**Surviving a closed terminal.** Closing the Terminal window (or the SSH session) sends SIGHUP and kills the run. Current practice offers two patterns: (a) **simplest-reliable** — a dedicated Terminal window that stays open, machine on AC, lid open; (b) **resilient** — run inside `tmux` (`tmux new -s train`, launch, detach with Ctrl-B D, reattach with `tmux attach -t train`), which survives window closes and lets the operator reattach after an accidental close. `nohup ... &` also works but gives the non-expert no way to see live output again. Recommendation-shaped finding: pattern (a) for the first runs, with tmux introduced as a single optional Launch sub-step once runs exceed a workday — it is the standard tool and the two commands above are its entire required surface. Whether to *advise* it is a runbook-design decision (it adds one concept to a non-expert's plate) — flagged for the Launch entry point.

### 4.2 Thermal behavior: what is real vs. folklore

Real, with current evidence: Apple Silicon does thermally/power throttle under sustained combined load — it never disappeared with the efficiency gains. On the current (M5-generation, March 2026) MacBook Pros, sustained stress testing shows the 14-inch chassis holding roughly 75% of peak in the default Automatic mode and ~93% in High Power Mode for the top chip, with the base single-fan M5 model reaching ~99 °C package temperatures under stress [30][31][32]; throttling on Apple Silicon generally engages around 95–100 °C [33]. **High Power Mode** (System Settings → Battery → Energy Mode, available on MacBook Pro models with Pro/Max-class chips) is real and works mainly by removing the fan-speed governor to sustain clocks longer [34][31].

Real mitigations: AC power for the whole run (battery operation both throttles and would drain in hours); hard flat surface with the rear vents unobstructed (never a duvet/sofa); a cool room; High Power Mode for multi-day runs if the model offers it; lid open (closed-lid clamshell reduces dissipation [29]). Folklore or out-of-scope for a non-expert: repasting/thermal-pad mods (warranty risk, marginal), third-party fan-control apps (functional but an unnecessary failure mode to hand a non-expert), cooling pads/ice (condensation risk).

Proportionality note that belongs in the runbook: this project's workload (a 0.73 M-parameter MLP) is far below Cinebench-class stress; sustained moderate fan noise is the expected steady state, and the operative signal is not temperature readouts but the K1 watchlist row "**s/step drifting upward**" — throttling that matters shows up there first.

### 4.3 Power settings and safe manual stop

Settings checklist for the Setup entry point: plug in (96 W or better adapter, not a low-watt USB-C charger); System Settings → Battery → Options → **"Prevent automatic sleeping on power adapter when the display is off" = on** (belt-and-suspenders alongside `caffeinate`); Energy Mode = Automatic (or High Power for multi-day runs); leave optimized battery charging on (it is fine for a machine living on AC). Inspect effective state with `pmset -g`.

Safe manual stop semantics, cooperating with checkpointing (this is the design's §5.4 contract, restated as operational truth): **one Ctrl-C** (SIGINT) → graceful checkpoint-and-exit; the equivalent from another window is `kill <pid>` (SIGTERM) — the trainer should treat SIGTERM like a single Ctrl-C so that tmux-detached runs are stoppable too (D-10); **two Ctrl-Cs** → immediate exit, losing work since the last checkpoint; **force-quit / `kill -9` / lid close / battery death** → as-if-crash; recovery is always `--resume` from `latest.pt`. The worst-case loss on any non-graceful stop is checkpoint_every × t_step — which ties the checkpoint-cadence decision to K4's measured step time (§1.8).

### 4.4 Environment maintenance over a multi-year project

The training stack sits on the fastest-moving corner of the ML ecosystem, and the failure mode is precisely the one the research contract names: "I updated macOS" silently becoming "my loss curves changed." This is documented, not hypothetical — PyTorch's tracker contains *silent-correctness* MPS regressions triggered by a macOS point update alone (Sonoma 14.3 → 14.4 broke models on unchanged PyTorch [6]), by PyTorch version bumps on unchanged macOS (2.4.1 → 2.5.1 producing garbage output 40% slower [7]; a 2.8.0 SDPA correctness regression [15]), and by new macOS majors breaking ops or device availability outright (macOS 26 issues [16][35]). Three findings, each runbook-shaped:

**Pin and export, at Setup time.** The environment is an artifact: create it from a lockfile, and regenerate the lockfile only deliberately. Concretely (Miniforge3 per the design): keep both `environment.yml` (human intent, `conda env export --from-history`) and a full transcript of the solved environment (`conda list --explicit > conda-spec.txt`, or a `conda-lock` lockfile; for pip-layer packages, `pip freeze > requirements-lock.txt`). Additionally record, into every `runs/<name>/` directory at launch: `sw_vers` output (macOS version/build), `python -V`, and the framework version+build string. The design's run-directory contract ("give a colleague `runs/<name>/` and they can reproduce") is only true if the environment fingerprint is in it (D-12).

**Upgrade policy: freeze by default, upgrade deliberately.** Never upgrade anything mid-run. Defer macOS *major* upgrades during active training phases entirely, and take point updates only between stages; turn off automatic macOS update installation (System Settings → General → Software Update) for the project's duration. Framework and Python upgrades are taken only for a reason (a needed fix or a security issue), one component at a time, between runs. Take a Time Machine snapshot (or at minimum archive the conda env transcript) before any OS update so the previous state is restorable.

**Re-validation after any upgrade = re-run the cheap rungs.** After *any* change to macOS, the framework, Python, or drivers: re-run ladder rungs 0–3 plus the 5-minute smoke test (rung 6), and compare the smoke test's recorded loss trajectory and s/step against the previous environment's recorded values on the same fixed seed/config ("golden smoke run"). Numerical results need not be bit-identical across GPU stacks — but a loss curve that departs the golden run beyond a small tolerance, or an AD probe that newly fails, is exactly the silent change the documented regressions produce, caught in ten minutes instead of after a wasted week. This makes the upgrade procedure a Setup/maintenance runbook page: *snapshot → upgrade one thing → rungs 0–3 → smoke vs. golden → only then resume real runs.*

---

## 5. K3 — Runbook Design Patterns for Non-Expert Operators

### 5.1 Evidence base

Three bodies of well-regarded operational-documentation practice apply, each verified against its primary source. **(1) SRE playbooks.** Google's SRE book reports that pre-written playbooks produce "roughly a 3x improvement in MTTR" over improvising, even for skilled engineers, and that the practiced on-call engineer armed with a playbook outperforms the hero generalist [36]; the SRE Workbook's playbook-entry structure — trigger, severity/impact, debugging suggestions, mitigation actions — is the canonical entry format [37][38]. The lesson transfers directly: this project's "on-call engineer" is a non-expert, which makes the pre-written-response advantage larger, not smaller. **(2) Checklists.** The aviation/surgery checklist literature (Gawande, *The Checklist Manifesto*, 2009; the WHO surgical checklist trial, Haynes et al., NEJM 2009, which measurably cut complications) distinguishes **READ-DO** checklists (read a step, do it, confirm, next — for procedures the operator doesn't know by heart) from **DO-CONFIRM** checklists (do the work from memory, then pause and verify the killer items), and insists checklists stay short at each pause point — the killer items only, not an exhaustive procedure [39] (cited as the standard texts; see C-11). **(3) Error-message and instruction usability.** Long-standing usability guidance for error surfaces: state what happened in plain language, why it matters, and exactly what to do next, in the error itself or one hop away; never make the user translate codes [40] (C-11). The design's §5.8 symptom table already embodies this — the findings below extend it.

### 5.2 Pattern findings, mapped to the five entry points

**Pattern: commands inline, verbatim, with expected output.** (Pattern → example → where it applies.) Every step shows the exact command to paste and, immediately after, "you should see:" with the literal success output — the SRE-playbook property that steps are executable under stress without interpretation [36][37]. Example: the design's §5.4 launch sequence already lists the five things the user sees in order; extend the same treatment to Setup (after the conda create step: "your prompt now starts with `(pinn-train)`") and to every verification rung ("PASS: AD probe, max rel err 3.1e-7"). Applies to: **Setup, Launch, Resume** — every command-bearing step.

**Pattern: READ-DO for procedures, DO-CONFIRM for gates.** Setup and Resume are READ-DO checklists (the operator has never done them; number every step, one action per step). The Launch pre-flight is a DO-CONFIRM gate: a short list of killer items the trainer itself should verify and print as a block — environment fingerprint matches lockfile, ladder rungs green, dataset hash matches, disk space sufficient, AC power connected, caffeinate active — with the human confirming the green block rather than performing checks manually [39]. Keep each pause point ≤ ~7 items; push everything else into automation or links. Applies to: **Setup, Launch**.

**Pattern: error → meaning → action tables, one row per known symptom, flat until proven otherwise.** The SRE entry structure compresses, for a single-system single-operator project, to exactly the design's §5.8 three-column table — keep it flat. Troubleshooting *trees* earn their complexity only when a symptom genuinely branches on a diagnostic the operator can perform; with ≲ 10 known errors a flat table is faster to scan and easier to maintain, and the catch-all row ("unknown error → copy the log tail, ask for help") bounds the operator's worst case [37][38]. Revisit the flat-vs-tree choice only when the error corpus outgrows one screen. The K1 watchlist (§3.2) is the same pattern applied to *in-run* signals rather than errors. Applies to: **Launch (failures), Monitor**.

**Pattern: decision junctures as explicit gates with pre-stated criteria and one default.** Wherever the operator must decide (advance a stage? resume or restart? upgrade now?), the runbook presents: the criteria (already pre-stated by the specs — e.g., the four stage-advance criteria), the evidence surface to read them from (which dashboard panel / which summary.md line), the **default action**, and the explicit alternative with its cost. Open-ended choices mid-procedure are the documented failure mode of operational docs [37]; every juncture gets a recommended default the operator can take without expertise. The design's gate check (§6.3) already renders pass/fail visibly — extend that rendering style to stage transitions ("ADVANCE: 4/4 criteria met" printed by the trainer). Applies to: **Monitor, Resume**, and the stage-transition moments inside Launch.

**Pattern: context inline only when load-bearing; background one link away.** The runbook page for a step contains what's needed to perform and verify the step — command, expected output, the one-sentence "why" if skipping it is tempting (e.g., why the pre-flight is mandatory) — and links out to this document, the specs, and upstream docs for everything else. Inline context that isn't load-bearing trains operators to skim, which defeats checklists [39]. A practical corollary for a single-user project: the runbook must be usable offline (the Mac may be deliberately disconnected during long runs), so linked-out *external* pages get a one-line summary inline. Applies to: **all five entry points**.

**Pattern: the run directory is the report.** SRE practice ties every alert to its playbook entry [37]; the equivalent binding here is that everything the operator is asked to *report* (watchlist rows, gate failures, errors) is phrased as "attach `runs/<name>/logs/train.log` tail + `status.json`" — pre-deciding the evidence package so reporting is a copy operation, not a judgment call. Applies to: **Monitor, Resume**, and the design's "honesty layer."

### 5.3 Entry-point summary table

| Entry point | Primary pattern | Concrete artifact the runbook should contain |
|---|---|---|
| Setup | READ-DO checklist + idempotent script | Numbered paste-one-at-a-time commands, each with "you should see"; lockfile install; verification script = ladder rungs 0–3; environment fingerprint capture |
| Configure | Annotated single-file template | One commented YAML per run; required-field validation errors phrased as error→meaning→action; advanced knobs hidden per design §5.3 |
| Launch | DO-CONFIRM pre-flight gate + verbatim command | Trainer-printed pre-flight block (rungs green, hashes, power, caffeinate); the `caffeinate -is python -m pinn.train ...` line; the "what you'll see, in order" sequence; smoke test as mandatory step 0 of every real run |
| Monitor | Flat signal tables | K1 watchlist (§3.2) verbatim; the design's §6.1 action set; "scheduled discontinuities are normal" framing; twice-daily rhythm for multi-day runs (§1.8) |
| Resume | READ-DO + invariant gate | Single resume command; the three resume invariants as trainer-enforced errors; post-crash triage order (status.json → log tail → watchlist) |

---

## 6. Decision-Relevant Observations

Findings that imply a project decision, stated with evidence and **not adjudicated**; these merge with R1a's decision menus at consolidation.

- **D-1 — Hardware spec mismatch.** No shipping M5 Pro matches the design's "16 CPU / 15 GPU"; Apple's lineup (March 2026) is 15-CPU/16-GPU base or 18/20 upgrade, 24/48 GB, 307 GB/s [1][2][3]. The actual machine (and its memory: 24 vs 48 GB) should be confirmed before R1a consolidation; K4 assumed the base part.
- **D-2 — JAX candidate has effectively no supported GPU path.** jax-metal is unmaintained/dead (Dec 2025) and fails on recent macOS [17][18]; the community jax-mps plugin is experimental [19][20]. The R1a framework decision should evaluate JAX as a CPU-backend candidate (where it is float64-capable and AD-ergonomic), not a GPU one.
- **D-3 — Precision adjudication couples to device choice.** Float64 is unavailable on every Apple GPU path (MPS, MLX-GPU, Metal plugins) [4][14]. If the open precision contract lands on float64 anywhere inside the training loop, GPU training is excluded on all three candidates; if float32-in-loop is confirmed, the K5 rung-1 dual-arm tolerance (float64-CPU reference vs float32-device) becomes the verification contract.
- **D-4 — Scalar-time forward-mode AD is a ~order-of-magnitude cost lever.** Because the differentiation variable u is a scalar, jvp-based forward(-over-forward) AD computes all 9 first/second derivative components in O(1) passes vs 9 reverse passes for the spec's named patterns (§1.2 κ table). PHYS-02's "equivalent full-Jacobian method" clause appears to admit it; making that admission explicit in the spec would let the implementation target the cheap corner of K4's envelope.
- **D-5 — The smoke test should be promoted to the K4 calibration instrument.** Record s/step into `summary.json` at every smoke test and have the trainer print "forecast for N steps: X hours" at launch. This turns the 30×-wide envelope of §1.3 into a per-run forecast for free, and gives R1a's first-run recipe its duration number.
- **D-6 — Fixture-suite conventions need three rulings** (§2.3): (i) figure-eight vs L_scale = ‖L₀‖+10⁻⁸ (zero-angular-momentum fixture makes the L_L term explode; needs an absolute-drift evaluation mode or exclusion for that fixture); (ii) fixtures must be ingested through Phase 18 preprocessing, not hand-built IC13; (iii) which characteristic time T a standalone fixture run uses.
- **D-7 — "Full-batch L-BFGS" at stage 2 needs an executable definition.** The cumulative stage-2 dataset includes high-resolution Set 2a; a literal full-batch second-derivative residual evaluation over millions of points exceeds 24 GB without chunked/accumulated evaluation (§1.6). Defining full-batch as "accumulated over chunks, including/excluding full collocation" is a spec-level decision.
- **D-8 — Sub-stage segmentation (1a/1b, 4a/4b) is unspecified** and moves the full-run duration ~30% (7 vs 9 segments).
- **D-9 — Two monitoring surfaces should be added to the design's dashboard list**, both cheap: a per-time-bin physics-residual panel (detects propagation failure [26]) and causal-weight statistics (min/mean w_n, fraction > 0.5; detects weight collapse [27]). Without them, two of K1's highest-value signals are invisible.
- **D-10 — Three design §5 corrections shaped by K2 evidence:** lid-close does *not* pause-and-resume benignly (revise §5.4 stop rules to "lid open for the whole run; recovery is checkpoint-resume"); `caffeinate -is` not `-d` (§5.10); the trainer should handle SIGTERM identically to a single Ctrl-C so detached runs are stoppable gracefully.
- **D-11 — The §6.1 "GPU utilization 60–95%" health band is unreliable for this workload.** A 0.73 M-parameter, dispatch-heavy double-backward workload can be healthy at much lower GPU residency [8][9][10]; the runbook should compare against the smoke test's recorded baseline rather than absolute thresholds.
- **D-12 — Run-directory contract should include the environment fingerprint** (sw_vers, python -V, framework version/build, lockfile hash) for the "give a colleague runs/<name>/" promise to hold, and to make K2's upgrade re-validation diffable.
- **D-13 — The AD probe must run on the training device, in the training dtype**, with a float64-CPU reference arm; MPS double-backward coverage is op-dependent and has regressed historically [5][6][7].
- **D-14 — Config-architecture conflict to reconcile:** `ctl_instruction.md` mandates a three-file Hydra stack (stage/opt/loss.yaml) with the resolved config written into the run folder; the design commits to a single per-run YAML (§5.3). Both can't be the surface; the resolved-config-frozen-into-the-run-folder property is the part worth preserving either way.
- **D-15 — Pass thresholds for ladder rungs 4–5 are proposals** (§2.2) and need project ratification; they are operational tolerances, not literature constants.
- **D-16 — Test-harness skeleton implied by K5:** rungs 0–3 as a `verify` script (idempotent, device-aware, exits nonzero on any red), rungs 4–5 as pytest-style fixtures with the three reference solutions checked into the repo as data files (ICs + reference trajectories from a high-precision integrator), rung 6 as a `--smoke` flag on the trainer itself. The golden-smoke comparison (K2 §4.4) needs the trainer to support a fixed-seed deterministic-enough mode on the chosen backend — which couples to R1a's determinism policy.

---

## 7. Claims-and-Uncertainty Register

Open items: things not verifiable from primary sources today, plus ambiguities/contradictions found in the attached materials. None of these are asserted anywhere above without their hedge.

- **C-1 — Steps per stage (N_Adam,k) is nowhere specified.** Inferred ≳ 2×10⁴ from the I_warm = min(2000, 0.1·N_Adam,k) formula's structure; the spec's own author note says all transition criteria are theoretical until stage 0 runs. K4 parameterizes [10⁴, 10⁵].
- **C-2 — Snapshots per trajectory / t_max unknown.** dt_out is given (0.08 / 0.17 / 0.01) but trajectory duration is not; memory and full-batch-cost legs are parameterized over it.
- **C-3 — Stage population counts unknown** until the invariant binning is run over the 15,028 trajectories (the spec's author note proposes exactly that data scan; thresholds may then change).
- **C-4 — SI-PINN-003 (author-flagged):** the 256×32 batch construction in `pinn_architecture.md` is inconsistent with the CTL plan, per the spec's own reconciliation note. K4's N_data is parameterized to survive the reconciliation.
- **C-5 — Sub-stage segmentation** (see D-8): treated as a [7, 9]-segment range.
- **C-6 — Rung-1 tolerance vs dtype:** the spec's 10⁻⁶ relative AD tolerance (§10.3) may be unachievable for float32 second derivatives on GPU; the dual-arm scheme in §2.2 is a proposal pending the precision adjudication.
- **C-7 — Classical-fixture attributions** (Lagrange 1772, Euler 1767, ω² = GM/d³, the equal-mass Euler ω² = (5/4)Gm/a³) are standard-text results cited to Murray & Dermott (1999)-class references and re-derivable in a few lines; the primary 18th-century sources were not consulted. The figure-eight values, by contrast, were verified verbatim against Chenciner & Montgomery 2000 [23]. Note also the sign-convention split across figure-eight sources (§2.3) — both conventions are in the literature [23][24][25].
- **C-8 — Fixture/pipeline interactions not resolvable from the attached files:** the E_scale used in the IC13 energy slot for a standalone fixture; whether canonical ordering/rotation in Phase 18 is well-defined for the perfectly symmetric Lagrange configuration (degenerate orderings); these surface only when the preprocessing code exists.
- **C-9 — No published training benchmark close to this workload on M5-class hardware was found** (small MLP + second-order AD). Apple publishes no GPU TFLOPS for M5 Pro. The 0.2–3 TFLOPS effective bracket and the κ table are reasoned estimates with stated assumptions, to be replaced by the smoke-test measurement.
- **C-10 — MLX float64 status** was verified only by absence on the GPU path (Metal stack is fp32/16 [4][14]; MLX docs/issues discuss fp32 workflows [8][9]); whether current MLX exposes float64 on the *CPU* stream was not conclusively verified and is not relied on anywhere above.
- **C-11 — K3's checklist and error-message sources** (Gawande 2009; Haynes et al., NEJM 2009; classic usability error-message guidelines) are standard, stable references cited from established knowledge rather than re-fetched primary text today; the SRE claims, by contrast, were verified against sre.google [36][38].
- **C-12 — Design §6.3 gate direction looks inverted as written:** "ε_H (energy error) > 10⁻⁵" as a *requirement* — with the worked example failing at 8.2×10⁻⁶ — reads backwards for an error metric whose plain-English gloss says "smaller is better. < 10⁻⁵ is excellent." Likely a typo for "< 10⁻⁵" (or ε_H here means something other than error); flagged, not corrected.
- **C-13 — Files referenced but not attached, treated as unavailable per the research contract:** `sampling_method.md`, `PINN_architecture_plan.tex`, the §10 probe scripts under `.planning/...`, `simulation_data/`, the project `CLAUDE.md`/STOP protocol, the EVID-05 evidence file `M4.md`, and the design's source S-1…S-6 local context. Nothing above depends on their contents.
- **C-14 — "16 CPU / 15 GPU" M5 Pro** (design §2.1 and the research-context constraints) matches no shipping configuration found [1][2][3]; see D-1.
- **C-15 — Thermal numbers are chassis/chip-specific:** the sustained-load figures cited are for M5 Max 14-inch (Notebookcheck) and base M5 [30][31]; no M5 *Pro*-specific sustained-throughput test was found. The qualitative guidance in §4.2 does not depend on the exact percentages.

---

## 8. Sources

All URLs accessed 2026-06-12.

1. Apple — MacBook Pro Tech Specs (M5 / M5 Pro / M5 Max lineup, core counts, memory, bandwidth). https://www.apple.com/macbook-pro/specs/
2. Apple Newsroom — "Apple debuts M5 Pro and M5 Max…" (2026-03-03; availability 2026-03-11). https://www.apple.com/newsroom/2026/03/apple-debuts-m5-pro-and-m5-max-to-supercharge-the-most-demanding-pro-workflows/
3. Apple Support — MacBook Pro (14-inch, M5 Pro or M5 Max) Tech Specs (15-core CPU / 5 super + 10 performance configuration). https://support.apple.com/en-us/126318
4. Apple Developer — "Accelerated JAX on Mac" (Metal plug-in experimental; unsupported dtypes incl. float64). https://developer.apple.com/metal/jax/
5. pytorch/pytorch issue #98498 — higher-order derivatives failing on MPS (`derivative for aten::linear_backward is not implemented`, PyTorch 2.0 era; linear case later fixed, pooling gaps tracked separately). https://github.com/pytorch/pytorch/issues/98498
6. pytorch/pytorch issue #122016 — "[MPS] Regression from macOS 14.3 to 14.4" (silent correctness, macOS update alone). https://github.com/pytorch/pytorch/issues/122016
7. pytorch/pytorch issue #141471 — MPS silent-correctness regression PyTorch 2.4.1 → 2.5.1. https://github.com/pytorch/pytorch/issues/141471
8. MLX documentation — Function Transforms (composable grad-of-grad to arbitrary order). https://ml-explore.github.io/mlx/build/html/usage/function_transforms.html
9. ml-explore/mlx issue #1927 — PINN bulk-Jacobian feature request; per-component grad loops fail under `mx.compile` (2025-03). https://github.com/ml-explore/mlx/issues/1927
10. Feng et al., "Profiling Apple Silicon Performance for ML Training," arXiv:2501.14925 (2025) — MPS training-path gaps; FP16 yields ~0% (MPS) / 20–30% (MLX) speedup. https://arxiv.org/pdf/2501.14925
11. Wang, Teng, Perdikaris — "Understanding and mitigating gradient flow pathologies in physics-informed neural networks," SIAM J. Sci. Comput. 43(5), 2021 (loss-term gradient imbalance).
12. Wang, Yu, Perdikaris — "When and why PINNs fail to train: A neural tangent kernel perspective," J. Comput. Phys. 449:110768 (2022). (Also: "Mollifier Layers…," arXiv:2505.11682, for PDE-loss compute/memory dominance measurements.)
13. Krishnapriyan, Gholami, Zhe, Kirby, Mahoney — "Characterizing possible failure modes in physics-informed neural networks," NeurIPS 34:26548 (2021), arXiv:2109.01050 (ill-conditioned landscapes; curriculum regularization as mitigation). https://arxiv.org/abs/2109.01050
14. PyTorch — MPS backend notes (float32-only GPU dtype surface; macOS 14.0+ requirement), docs.pytorch.org/docs/stable/notes/mps.html (as referenced by the design's S-1/S-2 and the 2025 hardware survey, https://tunguz.github.io/PyTorch_Hardware_2025/).
15. pytorch/pytorch issue #163597 — SDPA MPS correctness regression in 2.8.0 (macOS 15.6.1). https://github.com/pytorch/pytorch/issues/163597
16. pytorch/pytorch issues #161265 (macOS 26 silent wrong results for ≥4 GB tensors) and the general module:mps correctness label. https://github.com/pytorch/pytorch/issues/161265
17. Apple Developer Forums thread 815139 — JAX maintainers closed jax-metal issues citing no active development (Dec 2025). https://developer.apple.com/forums/thread/815139
18. jax-ml/jax issue #34109 — jax-metal fails on recent macOS (2025-12-26). https://github.com/jax-ml/jax/issues/34109
19. jax-ml/jax discussion #34648 — community MPS backends after jax-metal's abandonment (2026-01). https://github.com/jax-ml/jax/discussions/34648
20. jax-mps on PyPI — experimental MLX-based PJRT plugin; jaxlib pinning; ~3.7× over CPU on ResNet18/M4 Air (2026-05). https://pypi.org/project/jax-mps/
21. PyTorch Tutorials — "Double Backward with Custom Functions" (gradcheck/gradgradcheck in double precision "because finite differencing method magnifies errors"). https://docs.pytorch.org/tutorials/intermediate/custom_function_double_backward_tutorial.html
22. Karpathy — "A Recipe for Training Neural Networks" (2019): overfit-a-single-batch as a canonical plumbing check. https://karpathy.github.io/2019/04/25/recipe/
23. Chenciner & Montgomery — "A remarkable periodic solution of the three-body problem in the case of equal masses," Annals of Mathematics 152:881–901 (2000); ICs by C. Simó. arXiv:math/0011268. https://arxiv.org/pdf/math/0011268
24. Fenucci & Gronchi (eds. context) — "Local minimality properties of circular motions… and of the figure-eight solution," arXiv:2201.01205 (independent printing of the Simó ICs and T = 6.32591398292621).
25. R. Montgomery — N-body choreography page (reflected-convention IC printing). https://people.ucsc.edu/~rmont/Nbdy.html
26. Daw, Bu, Wang, Perdikaris, Karpatne — "Mitigating Propagation Failures in PINNs using Retain-Resample-Release (R3) Sampling," ICML 2023, arXiv:2207.02338 (propagation failures; trivial-solution literature surveyed therein). https://arxiv.org/pdf/2207.02338
27. Wang, Sankaran, Perdikaris — "Respecting causality for training physics-informed neural networks," Comput. Methods Appl. Mech. Eng. 421:116813 (2024). (Plus Wang, Sankaran, Wang, Perdikaris, "An expert's guide to training PINNs," arXiv:2308.08468, 2023, for step-count and training-practice norms [13]-adjacent.)
28. Macworld — "How to use a MacBook with the lid closed: clamshell mode, sleep settings" (2026; pmset disablesleep caveats, clamshell requirements). https://www.macworld.com/article/673295/how-to-use-macbook-with-lid-closed-stop-closed-mac-sleeping.html
29. "Let AI Agents Work Overnight: Disable Laptop Sleep on Lid Close" (2026-04; caffeinate flag patterns, clamshell as the only Apple-supported closed-lid mode, Apple-Silicon thermal rationale). https://pasqualepillitteri.it/en/news/779/disable-laptop-sleep-lid-close-ai-agents
30. Notebookcheck — MacBook Pro 14 M5 Max review (2026-03): sustained-load throttling to ~75% (Automatic) / ~92.6% (High Power Mode); 52 W sustained package power. https://www.notebookcheck.net/M5-Max-with-inconsistent-performance-and-throttling-issues-Apple-MacBook-Pro-14-Review.1246064.0.html
31. TweakTown — base M5 MacBook Pro single-fan thermals, ~99 °C under load (2025-10). https://www.tweaktown.com/news/108478/
32. MacRumors forums — M5-generation 14-inch thermal discussion (2026-03; corroborating, forum-grade). https://forums.macrumors.com/threads/14-macbookpro-cant-handle-m5-mx-max-throttling-due-to-heating.2479303/
33. BreezeKit — Mac thermal throttling guide (throttling onset ~95–100 °C on Apple Silicon; secondary source). https://breezekit.app/en/guides/mac-thermal-throttling-explained
34. iDropNews — "High Power Mode comes to all M4 Pro Macs" (2024-11; HPM mechanism = sustained performance via fan governor). https://www.idropnews.com/news/high-power-mode-comes-to-all-m4-pro-macs/229739/
35. pytorch/pytorch issue #177819 — MPS unavailable on macOS 26.3.1 with nightly (2026-03). https://github.com/pytorch/pytorch/issues/177819
36. Google SRE Book, Ch. 1 (Introduction) — playbooks ≈ 3× MTTR improvement vs. improvisation. https://sre.google/sre-book/introduction/
37. TechTarget — SRE documentation best practices (playbook entry elements: trigger, severity, impact, mitigation). https://www.techtarget.com/searchitoperations/tip/An-introduction-to-SRE-documentation-best-practices
38. Google SRE Workbook — incident response & playbook definition. https://sre.google/workbook/incident-response/
39. Gawande, *The Checklist Manifesto* (2009); Haynes et al., "A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population," NEJM 360:491–499 (2009). (Standard texts; see C-11.)
40. Classic error-message usability guidance (plain-language statement of problem + constructive next action), e.g., Nielsen Norman Group heuristics/error-message guidelines. (Standard reference; see C-11.)

*End of trainex R1b deliverable.*
