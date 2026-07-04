---
title: Trainex R1b Findings — Runbook and Operations Knowledge (CTL-PINN training execution)
package: trainex-r1b
role: cited, structured research findings for topics K1–K5 (runbook-and-operations-knowledge half)
date_compiled: 2026-06-19
source_baseline: c17e23ed0642f01d2eda7e7f65c0f18ed7081487
inputs_used: RESEARCH-CONTEXT-MASTER.md, 2026-06-10-training-execution-design.md, pinn_architecture.md, ctl_instruction.md (+ primary web sources, accessed 2026-06-19)
status: findings only — NOT decision menus; decisions routed to "Decision-Relevant Observations"
---

# Trainex R1b — Findings for K1–K5

This document delivers cited, runbook-ready findings for the five research topics in
`RESEARCH-CONTEXT-MASTER.md`, in the order the master file prioritizes them (K4 and K5 first,
then K1, K2, K3). Everything here is **evidence, not adjudication**: where a finding implies a
project decision it is recorded in **§Decision-Relevant Observations**; where something could not
be verified it is in the **§Claims-and-Uncertainty Register**. All web facts were checked against
primary or well-evidenced sources on **2026-06-19** and are date-stamped where they are
time-sensitive.

A short orientation section (§0) records the numbers I derived from the two framework specs,
because the K4 and K5 findings are built on them.

---

## 0. What the specs commit (derived facts the estimates rest on)

**Network (`pinn_architecture.md`, Table 2 / §2.4 / §5.2).** A SQR-SkipResNet-SIREN: **12 hidden
layers (6 SQR-SkipResNet blocks), width 256**, sine activations, LayerNorm on the odd-layer skip
path with `elementwise_affine=False` (zero parameters). **Input is 14-dimensional** `[τ, IC₁₃]`
where the autograd leaf is `u = t/T` and `τ = 2u − 1`; `IC₁₃` is the ordered Jacobi-state vector
from `ctl_instruction.md` Step 4. **Output is a 9-dimensional position vector** (3 bodies × xyz)
with a linear head, passed through a hard mass-weighted **COM-projection head** before any loss
sees it. Velocities and accelerations are **derived by automatic differentiation** of the projected
positions with respect to `u`.

**Parameter count (computed).** Counting an input SineLayer (14→256) + 12 hidden (256→256) +
output Linear (256→9), with biases: **≈ 0.80M parameters**; under the alternative reading where the
14→256 layer is itself hidden-layer #1 (11 × 256→256), **≈ 0.73M**. Take **≈ 0.73–0.80M params
(~0.75M)**. Weights are **~3 MB in fp32**; weights + Adam state (2× moments) are **< 10 MB**. By
modern standards this is a *tiny* network — a fact that drives the entire K4 analysis below.

**The expensive operation is double-backward, done component-wise.** The physics residual needs the
**second** time-derivative (acceleration). `pinn_architecture.md` §5.3.1 (PHYS-02) forbids the
`grad(r.sum(), u)` shortcut (an all-ones vector-Jacobian product) and **requires all nine
individual derivatives** via `jacrev`+`vmap` or an explicit per-component loop, each built with
`create_graph=True`, then differentiated again. The parameter-gradient backprop then runs through a
graph that already contains those second derivatives. This "double backward" is the standard reason
PINN steps cost several-fold more than a same-size supervised step.

**Curriculum (`ctl_instruction.md`).** ~9 stages — 0, 1a, 1b, 2, 3, 4a, 4b, 5, 6 — with **replay**
(each stage's training set includes all prior data; by stages 5–6 it is the full dataset of
**15,028 IC/BRUTUS pairs**: Set 1a 4857, 1b 4857, 2a 2749, 2b 2565). Per-stage optimization is
two-phase: **Adam → L-BFGS**. Batch is **256 trajectories** (240 replay + 16 look-ahead) × **32
time points** = 8,192 data points; collocation points are **2,048–4,096** (default 4,096). Adam LR
is `1e-3 × 0.7^k` with cosine decay and a state reset each stage; the **hand-off to L-BFGS is
plateau-driven**, not a fixed iteration count. There is also a conceptual **Phase 3 (active
learning)** that can add training rounds.

**Hardware (constraints + design §2.1).** One **MacBook Pro M5 Pro**, **24 GB unified memory** (48 GB
on a higher BTO), macOS 15+, arm64. Apple's published M5 Pro base is **15-core CPU / 16-core GPU,
16-core Neural Engine, 307 GB/s** memory bandwidth, with GPU Neural Accelerators (matmul units)
[1][2]. *Note the project docs list "16 CPU / 15 GPU cores" — a transposition relative to Apple's
spec; it does not change any estimate (see Claims Register C-1).* The Neural Engine is not reachable
by PyTorch/MLX/JAX training paths.

---

## K4 — Training Feasibility Envelope (HIGHEST PRIORITY)

**Headline.** Memory is **not** the binding constraint; **wall-clock is**, and wall-clock is
governed less by the M5 Pro's raw throughput than by two project-side unknowns — **how many
optimizer steps each stage runs** (plateau-driven) and **how efficiently the chosen framework
executes component-wise double-backward**. Order-of-magnitude, a full curriculum run is plausibly
**half a day to a few days**, with a real tail risk into **1–2 weeks** if step counts are high *and*
the AD path is slow. That tail is the scenario that pressures the no-cloud constraint.

### K4.1 Why the hardware is not the story here

For a ~0.75M-parameter network the GPU is **latency / kernel-launch bound, not FLOP bound**: there
is not enough arithmetic per layer to saturate 16 GPU cores, so the M5's headline "4× AI compute"
(which comes from the matmul Neural Accelerators [1]) and its 307 GB/s bandwidth translate poorly
into speed-up for this workload. Independent Apple-Silicon ML profiling reports that the MPS backend
still lacks several training-path optimizations and shows clear overhead specifically on the
**vector-Jacobian-product kernel** — exactly the kernel a PINN leans on [9]. The practical
consequence: **per-step time is dominated by autograd-graph traversal and the 9-way derivative
structure**, and the dominant lever on total time is the number of steps, not the chip.

### K4.2 Memory footprint (one stage and full run)

| Component | Estimate | Basis |
|---|---|---|
| Model weights (fp32) | ~3 MB | 0.75M params × 4 B |
| Weights + Adam moments | < 10 MB | 3× weights |
| Forward activations, ~12k pts | ~0.1–0.2 GB | 12 layers × 256 × 4 B × (Ncol+Ndata) |
| Double-backward graph retention | ×~3–5 over activations | retains 1st-deriv graph to build 2nd |
| Component-wise Jacobian (`jacrev`+`vmap`, 9 outputs) | ×~up to 9 if naive | materializes per-output graphs |
| L-BFGS history (size 10) | ~30 MB | 10 × gradient vector |
| **Total training memory** | **~1–4 GB (typical), low-GB worst case** | sum, dominated by AD graph |

**Conclusion: comfortably inside 24 GB**, with the OS's share intact; the 48 GB BTO is not needed
for capacity. The only realistic ways to blow the budget are (a) a **naive component-wise AD loop**
that materializes nine full graphs, or (b) accidentally loading the **entire dataset** into one
"full-batch" L-BFGS forward graph (see needed-number N5). Both are implementation choices, not
hardware limits. *Memory pressure is therefore a monitoring nicety, not the feasibility question.*

### K4.3 Per-step compute and wall-clock (parameterized, computed)

Per-sample forward matmul ≈ **1.58 MFLOP**. Applying a literature-style double-backward multiplier
of ~5–15× (the physics path computes 2nd derivatives and then differentiates a loss containing
them) and a per-step batch of Ncol + Ndata ≈ 10.2k–12.3k points gives **~80–290 GFLOP/step**
(≈ 0.08–0.29 TFLOP/step). Converting to wall-clock requires a *realized* throughput, which for a
tiny launch-bound net is a small fraction of peak — I bracket 0.05–2 TFLOP/s realized:

| Realized throughput | low (Ncol 2048, 5×) | mid (Ncol 4096, 5×) | high (Ncol 4096, 15×) |
|---|---|---|---|
| 0.05 TFLOP/s | ~1.6 s/step | ~1.9 s/step | ~5.8 s/step |
| 0.2 TFLOP/s | ~410 ms | ~490 ms | ~1.5 s |
| 0.5 TFLOP/s | ~160 ms | ~195 ms | ~580 ms |
| 2.0 TFLOP/s | ~40 ms | ~50 ms | ~150 ms |

**Realistic middle band: ~0.2–0.5 s/step.** The design's mock log line of **"12 s/step" is a
placeholder at/above the worst case** — it would require < ~0.025 TFLOP/s realized, reachable only if
double-backward falls back to CPU or a naive Python 9-way loop dominates. A competent vectorized
implementation should land sub-second.

Full-run wall-clock, parameterized over steps/stage × 9 stages × sec/step:

| Steps/stage | sec/step 0.05 | 0.2 | 0.5 | 2.0 |
|---|---|---|---|---|
| 5,000 (45k total) | 0.6 h | 2.5 h | 6.2 h | 25 h |
| 20,000 (180k total) | 2.5 h | 10 h | 25 h | **4.2 days** |
| 50,000 (450k total) | 6.2 h | 25 h | **2.6 days** | **10.4 days** |

(L-BFGS adds cost not captured above: each L-BFGS *iteration* runs several line-search function +
gradient evaluations, so the spec's "20–50 iterations" per stage is roughly 100–500 step-equivalents
of extra work per stage — material but not order-changing.)

### K4.4 Per-framework framing (feasibility, not recommendation)

The three R1a candidates differ most in **how they execute higher-order AD on Apple Silicon** and in
**maintenance risk** over a multi-year laptop project. (R1a owns the choice; this is evidence.)

- **PyTorch + MPS.** Current stable is **2.12.1 (2026-06-17)** [3], Python ≥ 3.10. Largest ecosystem
  (Hydra, TensorBoard, `torch.save` checkpointing — all assumed by the specs). Double-backward
  **mostly works** but op coverage on MPS is **not guaranteed 100%**: the historical `aten::linear`
  double-backward gap is **fixed**, and remaining gaps are tracked op-by-op (issue #77764) [4][5].
  Crucially, when an op lacks an MPS second derivative the failure is an **explicit error**
  (`derivative for aten::… is not implemented`), not silent garbage [4]. The op set here is
  Linear (fixed), `sin`/`cos` (elementwise, fine), and **LayerNorm (must be verified)**. Fallback if
  an op is missing: run that piece on CPU, or restructure with `torch.func` transforms.
- **MLX (Apple).** Composable function transforms (`grad`, `vmap`, `vjp`, `jvp`) with **first-class
  higher-order AD** — `mx.grad(mx.grad(f))` is documented to work — and it natively uses the M5 GPU
  Neural Accelerators and unified memory [6][7]. This is the cleanest AD fit for a PINN. Costs:
  younger ecosystem; **no built-in L-BFGS** in `mlx.optimizers` to verify (the spec leans on
  L-BFGS); Hydra/TensorBoard are less idiomatic. Throughput vs MPS is **workload-dependent and
  within a small factor** (MLX wins some ops like Linear/sort; MPS historically faster for some
  training loops) [9][10][11] — neither is decisively faster for a small MLP.
- **JAX + Optax + Equinox.** Best-in-class AD (`grad`∘`grad`, `hessian`, `jacrev`/`jacfwd`). **But the
  Apple-GPU backend is the weak link:** `jax-metal` is experimental, pins to specific
  jaxlib/macOS combinations, and **as of December 2025 is effectively unmaintained** — recent JAX
  fails on Metal and users must downgrade hard (e.g. `jax==0.4.35`); the Apple Developer forums
  report all Metal issues closed citing no active development [12][13][14]. Only an experimental
  community fork (`jax-mps`, ~3× over CPU on an M4) exists [15]. In practice JAX on this Mac is
  **CPU-bound or dependent on an unmaintained plugin** — the highest maintenance risk for a
  multi-year single-machine project. (See DRO-1.)

### K4.5 Numbers the project must supply to tighten this (the needed-numbers list)

These collapse most of the spread above. The first two matter most.

| # | Number needed | Why it dominates | How to get it cheaply |
|---|---|---|---|
| **N1** | **Adam steps per stage** (plateau-driven; spec gives only `I_warm = min(2000, 0.1·N_Adam,k)`, implying ~20k if the cap binds) | Linear multiplier on total time | First stage's actual plateau curve |
| **N2** | **Measured per-step wall-clock** on the actual machine, per framework | Converts FLOPs → time; spans 40 ms–6 s | **K5's 5-min smoke test reads this directly** |
| **N3** | Whether component-wise double-backward runs on **GPU or CPU** for {Linear, sin, LayerNorm} | Decides which throughput row applies | K5's AD pre-flight test / `probe_loss_stability.py` |
| **N4** | **L-BFGS iterations/stage** and line-search evals per iteration | Adds 100–500 step-equiv/stage | First stage's L-BFGS phase |
| **N5** | Whether **"full-batch L-BFGS" (stages 0–2)** loads all collocation points or all 15k trajectories at once | Memory headroom + step cost | Read the loop / one instrumented step |
| **N6** | Actual **Ncol** (2048 vs 4096) and **points/trajectory** (default 32) | ±~1.5× on per-step FLOPs | `loss.yaml` / `stage.yaml` |
| **N7** | **Phase 3 (active learning)** scope: how many extra rounds/epochs | Could multiply total run time | Curriculum owner |
| **N8** | Dataset size **actually loaded per stage** (replay growth) | Per-step data-loss cost grows late | Split manifest sizes |

### K4.6 Constraint-pressure flags and downstream implications

- **Benign band (most likely): full run ≈ 6 h – ~1 day.** No pressure on no-cloud. Checkpoint cadence
  of every 1,000 steps (design default) is fine; thermal planning routine.
- **Amber: full run ≈ 1–3 days.** A single uninterrupted multi-day laptop run is **operationally
  fragile** (sleep, lid, thermal, crash). This *does not* break the no-cloud constraint but raises the
  stakes on **checkpoint/resume** (K2), **lid/sleep handling** (K2 — note the lid-close finding
  below), and **monitoring rhythm** (K1). Implication: tighten checkpoint cadence (e.g. also a
  wall-clock-based checkpoint, not only step-based) and make resume bullet-proof.
- **Red: full run ≳ 1 week** (high step counts × slow AD path, e.g. CPU-fallback double-backward).
  **This is the scenario that pressures the no-cloud decision.** Flag it explicitly. Mitigations that
  stay inside the constraint: reduce Ncol toward 2048; cap Adam steps/stage; ensure GPU double-backward
  (avoid CPU fallback); consider the framework whose AD path is fastest for *this* op set (measured,
  not assumed). If none suffice, the project owner — not this research — owns whether to revisit
  no-cloud.

**Key linkage:** N2 and N3 (the two biggest unknowns) are **read directly by K5's 5-minute smoke
test**. Running that smoke test on each candidate framework, once, converts this whole envelope from
parameterized to measured. *The smoke test is the K4 measurement instrument as much as a K5
correctness gate.*

---

## K5 — Trainer-Correctness Verification Ladder (CO-PRIORITY)

PINNs fail **silently**: a residual sign error, a wrong coordinate frame, or an AD-graph mistake in
the double-backward can all produce a smooth, plausible-looking loss curve while the model learns
garbage [16]. The operator cannot eyeball wrong physics, so the trainer must climb a ladder of cheap,
decisive checks **before** any real run burns days. The rungs run cheapest-first so a failure is
caught before the expensive rungs.

### K5.1 The ladder (liftable into the runbook's "pre-flight check" section)

| # | Rung | What it catches | Pass criterion | Cost |
|---|---|---|---|---|
| **0** | **Environment & device check** | Wrong Python/arch; GPU not reachable; non-finite on random input | Prints expected device; `probe_loss_stability` (spec §10.5) returns finite loss on random tensors | seconds |
| **1** | **AD vs finite-difference gradient check** | Residual/AD-graph bugs; the forbidden all-ones VJP; wrong τ↔u chain-rule factor; missing `create_graph` | AD `dr/du`, `d²r/du²` match central finite differences to ~1e-4–1e-6 rel.; matches the spec's synthetic-trajectory check (spec §10.3 / §5.3.1: `r(u)=[sin2πu, cos2πu, u²]`) | seconds–1 min |
| **2** | **Component-wise AD shape/contract test** | The "9 derivatives collapsed into one VJP" anti-pattern; per-body indexing errors | All nine `dr'_{i,α}/du` recovered independently (spec §5.3.1 worked example) | seconds |
| **3** | **Force / energy self-consistency** | Sign error or wrong softening in residual vs Hamiltonian; frame inconsistency | −∇V (matched-Plummer, same ε_train=1e-5) equals the residual's force to ~1e-5 (spec §10.4 `probe_force_energy`); COM of projected output ≈ 0 (spec §10.2) | seconds |
| **4** | **Overfit a single tiny batch** | Plumbing/capacity/optimizer wiring; loss that *can't* be driven down | Total loss → ~0 (to optimizer tolerance) on one trajectory / a handful of collocation points; if it cannot, stop — the bug is upstream of data | 1–5 min |
| **5** | **Known-solution fixture (physics ground truth)** | Wrong equations of motion, wrong frame, broken conservation — the silent-garbage class | Given a reference IC, the trainer reproduces the analytic trajectory and conserves E and L to tight tolerance over ≥1 period (see K5.2) | minutes |
| **6** | **~5-minute end-to-end smoke test** | Config/wiring/throughput/checkpoint-resume faults under the *real* pipeline; also **measures step time and GPU-vs-CPU AD path** (feeds K4 N2/N3) | Runs N steps, loss finite and generally decreasing, a checkpoint is written, `--resume` continues from it; records s/step and device | ~5 min |

Rung 6 is the cheapest *full-system* rung and the last gate before a real run; rungs 1–3 are the
cheapest *physics* rungs and the ones that catch the silent failures the operator can't see.

### K5.2 Known-solution fixtures (cited to literature, expressed against the specs' conventions)

The three-body problem is unusually blessed with exact/special reference solutions. All values below
are in the spec's units (**G = 1**, equal masses unless noted) and must be **passed through the same
Phase 18 preprocessing** (COM recenter, zero-momentum boost, canonical ordering, rotation gauge,
global scaling) and **encoded as `IC₁₃`** before the network sees them — see the convention flags at
the end of this subsection.

**(a) Figure-eight choreography** (Moore 1993 [21]; existence proved by Chenciner & Montgomery,
*Annals of Mathematics* 152, 2000 [17]; standard numerical ICs from Simó, restated on Montgomery's
own page [18] and reproduced widely [19][20]). Three **equal masses (m=1)**, **zero angular
momentum**, planar:

- Positions: `r₁ = (−0.97000436, 0.24308753, 0)`, `r₂ = −r₁ = (0.97000436, −0.24308753, 0)`,
  `r₃ = (0, 0, 0)`.
- Velocities: the body at the origin carries `v₃ = (0.93240737, 0.86473146, 0)`; the other two each
  carry `v₁ = v₂ = −v₃/2 = (−0.46620368, −0.43236573, 0)`.
- Period: `T ≈ 6.32591398292621` [19].
- (Body labels differ across sources — what is invariant is *two bodies symmetric about the origin +
  one at the origin*, with the central body's velocity twice-and-opposite the others'.)

This is the **strongest physics fixture**: a stable, exactly periodic orbit whose energy and angular
momentum the trainer must conserve over ≥1 period if its residual, frame, and double-backward are
correct.

**(b) Lagrange equilateral solution** (Lagrange 1772 [16-context][8]). Three equal masses at the
vertices of an equilateral triangle of side `a`, rotating rigidly about the COM. From Newton's law
(derived; standard result): the angular velocity satisfies `ω² = (m₁+m₂+m₃)/a³ = 3m/a³` with G=1.
Each body moves on a circle of radius `a/√3`. A clean **circular-orbit fixture** with closed-form E
and L.

**(c) Euler collinear solution** (Euler 1767 [16-context][8]). Three bodies on a rotating line. The
**equal-mass symmetric** case is the cleanest fixture and avoids Euler's quintic: central body at the
origin, outer two at `±d`, rigid rotation with (derived) `ω² = 5m/(4d³)` (each outer body feels
`Gm²/d²` from the centre plus `Gm²/(4d²)` from the far body). The general unequal-mass Euler solution
requires solving the **Euler quintic** for the position ratio (Euler 1767) — use only if unequal-mass
coverage is wanted.

**Convention flags (route mismatches to the Claims Register, do not improvise):**

- **Frame:** all three fixtures are COM-centred by construction for equal masses, consistent with the
  spec's COM-projection head — good. But the spec's **canonical rotation gauge and canonical ordering**
  (`ctl_instruction.md` §2.3–§2.4) may *rotate/relabel* the fixture; the test must compare in the
  gauge the preprocessing produces, not the raw literature frame. (C-3)
- **Coordinates:** fixtures are Cartesian; the network input is **Jacobi `IC₁₃`**. The fixture must be
  mapped through Step 4's Jacobi assembly and per-slot tanh normalization before use. (C-3)
- **Units/time:** map the fixture's `G=1, m=1` to the spec's `T = t_max`, `D = (GT²)^{1/3}`,
  `u = t/T`, `τ = 2u−1`. (C-3)
- **Distribution mismatch (important):** the **figure-eight has L = 0 and equal masses**, whereas the
  curriculum's easy stages require **`L/L_max > 0.5`** (high angular momentum). So the figure-eight is
  **out-of-distribution for the data loss** but **ideal for the physics machinery** (residual, AD,
  conservation). Treat fixtures (a)–(c) as **unit tests of the trainer's physics**, not as data-fit
  benchmarks. (C-4)
- **Softening caveat:** the spec trains with **Plummer softening ε_train = 1e-5**; the reference
  solutions are for the *unsoftened* 1/r² law. At the fixtures' separations (order 0.1–1) the softened
  and exact forces agree to ~1e-10, so the fixture remains valid — but the comparison tolerance should
  account for softening near any close approach. (C-5)

---

## K1 — PINN Training-Health Watchlist

The runbook must let a non-expert answer "is training healthy?" from the surfaces the design exposes:
the **live terminal log** (one line per `log_freq` steps with the loss terms, LR, s/step, ETA), the
**TensorBoard dashboard** (loss-vs-step curves), and the **macOS system monitor** (Activity Monitor
GPU/Memory tabs). The documented PINN failure modes below are mapped to *signal → likely meaning →
first response a non-expert can take*. Because several failures are **silent on the total-loss
curve**, the watchlist leans on per-term curves and the conservation diagnostics.

| Signal (where it shows) | Likely meaning (with literature) | First response (non-expert) |
|---|---|---|
| `nan`/`inf` in any loss term (log) | Divergence — usually a close-encounter gradient spike through the 1/r³ force [arch §4.4] | Ctrl-C, restore last good checkpoint, restart with smaller LR; confirm gradient clipping active |
| Total loss flat but **physics term** stuck high while data term low (dashboard, per-term) | **Propagation failure** — net fits data points but doesn't satisfy the ODE between them; classic silent PINN failure [16][Daw R3, 25] | Don't trust the run; check residual/AD via K5 rungs 1–3; consider denser/adaptive collocation |
| One loss term **orders of magnitude** larger than others; training tracks only the big one (per-term) | **Loss-term imbalance / gradient pathology** — mismatched gradient scales [Wang-Teng-Perdikaris 22] | This is expected early; verify the warmup/λ schedule (PHYS-05) is running; if persistent, it's a weighting issue for the owner |
| Loss falls then **plateaus before ~10k steps** (dashboard) | Ill-conditioned loss landscape from the soft physics constraint [16]; or NTK spectral imbalance [Wang-Yu-Perdikaris 22] | Wait — some plateaus clear after ~10k more steps; if not, it's a stage/curriculum signal for the owner |
| **Energy/angular-momentum drift** rising even as loss falls (conservation logs) | Net is fitting data but **not learning the physics** — the headline red flag [ctl eval §] | Stop trusting the model; this is the gate's job to catch; re-check residual sign/frame (K5 rung 3/5) |
| **Causal weights `w_n` not approaching 1** over the time domain (if logged) | Residual not yet driven down in causal (earlier-time-first) order [Wang causality 24] | Healthy training drives `w_n → 1`; if they stay near 0 late, training hasn't converged in time order — keep training or revisit |
| Loss **oscillates wildly, no trend** (dashboard) | LR too high or batch too small | Ctrl-C, reduce LR, restart from checkpoint |
| **Divergence right after a stage transition** (log/curve at stage boundary) | New harder data + Adam state reset + re-warmup shock [ctl §, 16 curriculum] | Expected to wobble briefly; if it diverges, restore the pre-transition checkpoint and slow the LR for the new stage |
| Step number **stuck 5+ min**, no new line (log) | Hang (design's own hard rule) | Ctrl-C, read log tail, restore checkpoint, restart |
| **GPU util 0%** (Activity Monitor) | Training is on CPU (MPS unavailable, or AD fell back) | Stop; fix device/AD path — this also explains slow steps (K4 N3) |
| **Swap used growing** (Activity Monitor Memory) | Memory leak or batch too big | Ctrl-C, reduce batch/Ncol, restart; for this tiny net, growth implies a leak (e.g. retained graphs) |

**Literature backbone (verified, dated):** Krishnapriyan et al., *Characterizing possible failure
modes in PINNs*, NeurIPS 2021 [16] (soft constraints make the landscape hard to optimize; curriculum
and seq2seq are the documented remedies — validating this project's curriculum design); Wang, Teng &
Perdikaris, *Gradient flow pathologies in PINNs*, SIAM J. Sci. Comput. 43 (2021); Wang, Yu &
Perdikaris, *When and why PINNs fail to train: an NTK perspective*, JCP 449 (2022); Wang, Sankaran &
Perdikaris, *Respecting causality…*, CMAME 421 (2024) — the causal-weight-→1 convergence diagnostic
used above and the causal weighting the architecture already implements; Daw et al., *Mitigating
propagation failures (R3 sampling)*, ICML 2023; Wang, Sankaran, Wang & Perdikaris, *An Expert's Guide
to Training PINNs*, arXiv:2308.08468 (2023) — consolidated best practices and benchmark difficulties.

---

## K2 — Unattended Training Operations on a MacBook (macOS 15 era)

### K2.1 Sleep, lid close, and terminal survival — with one sharp correction

**The single most important operational finding, and it contradicts the design's casual note.** On
**Apple Silicon running macOS Ventura and later (which includes macOS 15+), closing the lid forces a
hardware-level sleep that NEITHER `caffeinate` NOR `sudo pmset -a disablesleep 1` can override.** The
lid magnet triggers sleep at a level below those tools. The only ways to keep a run alive are
**lid-open**, or **clamshell mode** (external display + power + keyboard/mouse, or an HDMI dummy
plug) [22][23][24]. The design §5.4/§5.10 ("lid close → training continues when lid reopens"; "use
`caffeinate -d` to prevent sleep") is **incomplete/misleading for lid-closed runs** (DRO-2).

What actually works:

- **`caffeinate` prevents *idle* sleep only, lid open.** Flags: `-d` (display), `-i` (idle system),
  `-m` (disk idle), `-s` (system sleep — effective on AC power), `-u` (declare user active), `-t SEC`
  (timed). **Best practice for the runbook:** wrap the training command so the assertion lives exactly
  as long as the job and releases automatically when it ends:
  `caffeinate -i -s python -m pinn.train --config …`. (Also `caffeinate -w <PID>` to attach to an
  already-running process.) [22][23]
- **Lid-closed unattended run → use clamshell** (external display + power) or **keep the lid open**.
  Do **not** run lid-closed in a bag — heat builds up [techradar/caffeinate].
- **Diagnostic:** `pmset -g assertions` shows what is currently preventing sleep; `pmset -g` shows
  power settings. Confirm the caffeinate assertion is listed before walking away.
- **Terminal survival:** for a *non-expert*, the simplest robust pattern is **lid-open, foreground,
  caffeinate-wrapped**, watching the live log — this matches the design's mental model and avoids
  detachment pitfalls. If detachment is wanted, `tmux`/`screen` (re-attachable session) is safer and
  more legible to a beginner than `nohup … &`; either way the **checkpoint/resume contract is the real
  safety net**, not the terminal. (DRO-3: the runbook's Launch step should adopt the caffeinate
  wrapper and state the lid rule explicitly.)

### K2.2 Thermal throttling — real, but mild for *this* workload

Apple Silicon **does** still throttle under sustained load — the firmware reduces clocks to protect
the chip — but the distinction that matters is **chassis**: the fanless MacBook **Air** drops 30–60%
from peak to a throttled floor within ~8–15 minutes, whereas the **actively-cooled MacBook Pro**
(this project's machine) sustains near-peak "for hours" [18-thermal][box]. Two project-specific
softeners:

- The Pro's **dual-fan active cooling is the right hardware** for multi-hour runs; the Air would
  throttle hard.
- This PINN's network is **tiny and launch-bound** (K4.1), so the **GPU is rarely pinned at 100%** —
  there is natural breathing room between kernel launches, unlike sustained LLM inference that
  saturates the GPU. Expect **mild** throttling at most. (Verify, don't assume — see diagnostics.)

**Real mitigations (vs folklore):** hard flat surface (not bed/couch), a stand with airflow
underneath, cooler ambient temperature, keep the lid open (also helps dissipation), close background
load; **plug in** and set **Battery → 80% charge limit** for longevity on long plugged-in runs
[thermal-evidence]. **Diagnostics:** `sudo powermetrics --samplers smc` shows CPU/GPU temperature and
any throttling; `pmset -g therm` shows thermal pressure / CPU speed-limit. Folklore to ignore:
chasing fan noise as a proxy — macOS keeps fans quiet by design and will throttle *before* ramping
fans hard, so quiet ≠ unthrottled. **Runbook step:** a "fans full + clocks below base = throttled,
move to a cooler room or pause" check (the design already gestures at this) plus the `powermetrics`
one-liner.

### K2.3 Environment pinning and multi-year upgrade discipline

The training stack sits on the **fastest-moving corner of the ML ecosystem** (Apple-Silicon
backends), and a non-expert will not connect "I updated macOS" with "my loss curves changed." Two
documented practices, mapped to runbook steps:

**Pin and export the environment (two-file model — the documented best practice [26][27][28]).**

- A **loose, human-edited spec** of direct dependencies for upgrades:
  `conda env export --from-history > environment.yml` (records only what you explicitly asked for,
  stripping solver noise) [27].
- A **fully pinned lockfile** for exact reproduction: `conda-lock` (cross-platform, pins
  version+build+channel, skips solving on recreate) [28][29], or **conda 26.5+'s native lockfiles**
  (`conda export`/`create`/`install` now treat lockfiles as first-class) [26].
- **pip-installed packages are NOT captured by conda lockfiles by default** — and PyTorch/MLX/JAX are
  typically pip-installed — so **also** run `pip freeze > requirements.txt` (or use conda-lock's pip
  section) [26]. Missing this is the most common silent reproducibility hole.
- **Multi-year caveat:** a lockfile pins exact packages but they must still exist when you recreate; if
  a wheel is yanked, recreate fails [26]. For a multi-year project, **archive the actual wheels** (e.g.
  `pip download`) alongside the lockfile.

**Upgrade cadence and re-validation.**

- **Defer** framework/Python/macOS upgrades mid-experiment; take them on a **defined cadence** (e.g.
  monthly/quarterly) with a changelog entry per change and a **kept history of lockfiles for rollback**
  [24-conda][27]. Don't upgrade between stages of a live curriculum run.
- **GPU-path numerics can change silently across versions.** Evidence from this round: MPS op coverage
  and behavior evolve release-to-release [4][5]; `jax-metal` pins to exact jaxlib/macOS pairs and
  breaks on others [13][14]. Reduction order / fast-math / kernel changes can shift GPU results without
  any code change.
- **Therefore: after ANY upgrade (framework, Python, or macOS), re-run K5's cheap rungs (0–3, ideally
  5) before trusting new runs.** The architecture spec's own acceptance checks (§10.1–§10.5) are
  exactly this regression suite. (DRO-4: make "re-run pre-flight after upgrade" a named maintenance
  step, and pin a known-good environment in Setup.)

---

## K3 — Runbook Design Patterns for Non-Expert Operators

The deliverable of trainex is a step-by-step runbook for a non-expert. Well-regarded operational
documentation converges on a few patterns that fit the design's **five entry points (Setup /
Configure / Launch / Monitor / Resume)**.

### K3.1 Separate the four documentation modes (Diátaxis) and map them to the entry points

The Diátaxis framework [30] separates docs by user need: **tutorial** (learning, user *at study*),
**how-to** (a goal, user *at work*), **reference** (neutral facts), **explanation** (understanding) —
and insists you keep them apart, keep *action* docs free of distraction, and **link out** for
explanation rather than inlining it. Mapping:

| Entry point | Primary mode | Pattern |
|---|---|---|
| **Setup** (once) | Tutorial + Reference | A guaranteed-success first-time walkthrough; the exact commands as reference. Pin the known-good environment here (K2.3) |
| **Configure** (per run) | Reference | A field-by-field table of the config knobs; "advanced" knobs hidden/commented (as the design intends) |
| **Launch** (per run) | How-to (+ Tutorial first time) | Goal-oriented steps; the **caffeinate-wrapped** command (K2.1); "what you should see, in order" |
| **Monitor** (while running) | Reference + minimal Explanation | The K1 *signal → meaning → action* table; one-line "what healthy looks like", linking out to the why |
| **Resume** (after stop/crash) | How-to | The single resume command + invariants (same config → continue; different config → hard error) |

This directly answers the master file's "how much context inline vs link out": **minimal inline
explanation in action docs, with a pointer to a separate explanation page** ("Here we use
`caffeinate` because the Mac would otherwise idle-sleep; see *Why runs need caffeinate*") [30].

### K3.2 Operational-runbook patterns (Google SRE) and error-surface design

- **Playbook/runbook entries carry: severity/impact, debugging hints, and concrete mitigating
  actions** — and exist to cut stress, time-to-repair, and human error [31][32]. The design's
  *Symptom → Meaning → Action* error table (§5.8) and the K1 watchlist are exactly this; keep that
  three-column shape.
- **Generic mitigations** — actions that "stop the bleeding" before the root cause is understood [33].
  For a non-expert this is the key pattern: the canonical response to most red signals is **"restore
  the last good checkpoint and restart with a smaller learning rate"** — safe, requires no diagnosis,
  and is the single most reusable instruction in the runbook.
- **Keep entries general so they go stale slowly** [31][32]: prefer a few broad, durable entries
  (e.g. one "loss diverged / NaN" entry) over many brittle specific ones that rot as the code changes.
- **Error messages should be actionable** — name the problem, the likely cause, and the next action —
  not just report a failure. The design's table already does this; carry it into every emitted error
  string.

### K3.3 Checklist format and troubleshooting structure

- **Read-do vs do-confirm checklists** (Gawande, *The Checklist Manifesto*, drawn from aviation):
  *read-do* = read each step then perform it; *do-confirm* = perform from memory then pause to confirm.
  Because this operator runs the procedure **rarely and is non-expert**, **Setup/Launch/Resume should
  be read-do checklists** — read the command, run it, **verify the expected output before proceeding**
  (the design's "On success: prompt shows `(pinn-train)`" is the verify-step pattern; put one after
  each command).
- **Troubleshooting tree vs flat FAQ:** a **short decision tree** beats a flat FAQ when the first
  symptom is ambiguous (e.g. "training looks wrong" → branch on *NaN? / stuck step? / plateau? /
  drift?*), but the leaves should resolve to the same **small set of generic mitigations** above.
  Keep the tree shallow (one or two branches) so a beginner doesn't get lost.
- **Practice the failure paths once.** SRE teams keep readiness with "Wheel of Misfortune" drills
  [32]; the solo analog is to **deliberately trigger a Ctrl-C and a resume, and (optionally) force a
  NaN, during the smoke test**, so the operator has done the recovery before they need it for real.

---

## Decision-Relevant Observations (evidence, NOT adjudicated)

These imply project decisions (structural, policy, constraint, or test-harness). They are stated as
evidence for R1a/the owner to merge and decide; nothing here is decided.

- **DRO-1 — Framework choice is shaped by AD-on-Apple-GPU maturity and maintenance risk, not just
  throughput.** Evidence: `jax-metal` is experimental and effectively unmaintained as of Dec 2025
  [12][13][14][15]; MPS double-backward is mature-but-not-total and fails *loudly* per op [4][5];
  MLX has first-class composable higher-order AD but lacks built-in L-BFGS and a mature ops ecosystem
  [6][7]. R1a owns the call; this is the feasibility evidence it should weigh.

- **DRO-2 — The design's sleep/lid guidance is wrong for lid-closed runs and should be corrected.**
  On Apple Silicon + macOS 15+, neither `caffeinate` nor `pmset disablesleep` keeps a lid-closed
  machine awake; only clamshell mode or lid-open does [22][23][24]. The Launch/Monitor runbook steps
  must say so.

- **DRO-3 — Adopt a `caffeinate`-wrapped launch command and an explicit lid rule as runbook steps.**
  `caffeinate -i -s python -m pinn.train …` ties the no-sleep assertion to the job's lifetime [22][23].

- **DRO-4 — "Re-run pre-flight (K5 cheap rungs / spec §10 acceptance checks) after any framework,
  Python, or macOS upgrade" should be a named maintenance step**, because GPU-path numerics can shift
  silently across versions [4][5][13][14]. Pair with the two-file environment pinning (loose
  `environment.yml` + lockfile + `pip freeze`) in Setup [26][27][28].

- **DRO-5 — The monitoring surface should log all five loss terms, not three.** The design's mock log
  line shows `data/physics/ic` (3 terms), but the actual objective is
  `data + IC + physics_causal + energy + angular-momentum` (5 terms; `pinn_architecture.md` §3–§4).
  The energy and angular-momentum drift terms are exactly the silent-failure detectors K1 relies on,
  so they must be visible in the live log and dashboard.

- **DRO-6 — Checkpoint cadence should consider wall-clock, not only steps, in the amber/red K4 bands.**
  A multi-day laptop run is fragile; a time-based checkpoint (in addition to the step-based default of
  every 1,000) bounds lost work after an unexpected sleep/crash.

- **DRO-7 — Test-harness skeleton (from K5).** The pre-flight ladder implies a small `tests/`
  (or `probes/`) suite: an AD-vs-FD gradient test, a component-wise-derivative shape test, a
  force/energy-consistency test, a single-batch overfit test, three known-solution fixtures
  (figure-eight, Lagrange, Euler) **encoded through the real Phase-18 preprocessing + Jacobi `IC₁₃`
  path**, and a ~5-minute smoke test that also records s/step and the GPU-vs-CPU AD path. The spec's
  §10 acceptance checks already cover several rungs and can seed this suite.

- **DRO-8 — Fixtures are physics unit-tests, not data-fit benchmarks, and need a gauge-consistent
  comparison.** The figure-eight is L=0 / equal-mass (outside the curriculum's `L/L_max>0.5` easy
  band) and all fixtures must be compared in the spec's canonical rotation gauge/ordering, not the raw
  literature frame (see Claims C-3/C-4).

- **DRO-9 — K5's 5-minute smoke test doubles as the K4 measurement instrument.** Running it once per
  candidate framework converts the feasibility envelope from parameterized to measured (needed-numbers
  N2/N3). Consider making it the first action when build work starts.

---

## Claims-and-Uncertainty Register

Anything not verifiable from primary sources, or ambiguous/contradictory in the attached materials, is
listed open rather than asserted.

- **C-1 — CPU/GPU core counts transposed.** Project docs say "16 CPU / 15 GPU cores"; Apple's published
  M5 Pro base is **15-core CPU / 16-core GPU** (configurable to 18/20) [1][2]. Does not change any
  estimate; flagged for correctness.

- **C-2 — Steps per stage are unspecified (the dominant K4 unknown).** `ctl_instruction.md` gives only
  plateau criteria and `I_warm = min(2000, 0.1·N_Adam,k)`; no fixed Adam/L-BFGS iteration count exists.
  Wall-clock cannot be pinned without N1/N4. Estimates are parameterized accordingly.

- **C-3 — Fixture↔spec convention mapping is not worked out in the attached specs.** Converting the
  Cartesian reference ICs into the spec's COM/zero-momentum/canonical-ordering/rotation-gauge/scaling
  pipeline and into Jacobi `IC₁₃` is implied but not specified for these particular fixtures; the
  rotation gauge may rotate/relabel them. Comparison must be gauge-consistent. Open until the
  preprocessing is run on the fixtures.

- **C-4 — Figure-eight is out-of-distribution for the data loss.** L=0, equal masses conflict with the
  curriculum's easy-stage `L/L_max>0.5`. It tests the physics machinery, not data fit; do not interpret
  a data-loss number on it as a quality metric.

- **C-5 — Softened vs exact force in fixtures.** Training uses Plummer softening ε_train=1e-5; reference
  solutions are unsoftened. Agreement is ~1e-10 at the fixtures' separations, so they remain valid, but
  tolerances near any close approach should account for softening.

- **C-6 — Realized Apple-Silicon throughput for *this* double-backward workload is not directly
  benchmarked anywhere I could find.** Published M-series benchmarks are for CNNs/transformers/LLM
  inference, not component-wise second-order AD on a small SIREN [9][10][11]. The 0.05–2 TFLOP/s realized
  bracket and the 5–15× double-backward multiplier are reasoned estimates, not measured for this case —
  hence the parameterization and the reliance on K5's smoke test to measure N2.

- **C-7 — `jax-metal` "unmaintained" status is from Apple Developer forum posts and a GitHub
  discussion (Dec 2025–Jan 2026) [12][13][14][15], not an official Google/Apple deprecation
  announcement.** Well-evidenced and consistent across sources, but treat as community-reported status,
  not a vendor statement.

- **C-8 — MLX optimizer/L-BFGS coverage not fully verified.** MLX higher-order AD is confirmed first-class
  [6][7], but whether `mlx.optimizers` ships an L-BFGS (which the spec's Phase-2b uses) was not confirmed
  from primary docs in this round. Flag for R1a.

- **C-9 — Spec internal notes flag unresolved items the trainer will inherit.** `pinn_architecture.md`
  carries author comments (e.g. SI-PINN-002/003: "batch construction is not consistent with the CTL
  instruction plan"; an unresolved causal-exponent underflow clip "surface a gap if needed"); these are
  the project's to reconcile and are not adjudicated here, but they touch the data-batch and physics-loss
  paths the K5 ladder exercises.

- **C-10 — `summary.md`/gate thresholds in the design are placeholders.** The design's gate
  (`ε_H > 1e-5`, `SCS > −5`) and the `metrics.md` mock are explicitly first-trial/illustrative; they are
  not a verified acceptance contract and should not be treated as final.

- **C-11 — Number of curriculum "stages" counted as 9** (0, 1a, 1b, 2, 3, 4a, 4b, 5, 6). If sub-stages
  are run as single stages or split further, the ×stages multiplier in K4.3 shifts proportionally.

---

## References (accessed 2026-06-19)

1. Apple Newsroom, *Apple debuts M5 Pro and M5 Max…*, 2026-03 — M5 Pro 15/18-core CPU, 16/20-core GPU, 307 GB/s, Neural Accelerators.
2. Apple Support, *MacBook Pro (14-inch, M5 Pro or M5 Max) Tech Specs* (HT126318).
3. PyPI, `torch` release history — 2.12.1 (2026-06-17), 2.12.0 (2026-05-13); PyTorch RELEASE.md schedule.
4. GitHub, pytorch/pytorch issue #98498 — MPS higher-order derivative (`aten::linear` double-backward) fixed; double-backward op tracking.
5. GitHub, pytorch/pytorch issue #77764 — MPS double-backward op coverage tracker.
6. Scaleway / MLX docs — composable transforms (`grad`, `vmap`, `vjp`, `jvp`); `mx.grad(mx.grad(...))` example.
7. Apple Machine Learning Research, *Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU*.
8. arXiv:2002.07250 — historical summary: Euler (1767) collinear, Lagrange (1772) equilateral, Moore (1993) figure-eight.
9. arXiv:2501.14925, *Profiling Apple Silicon Performance for ML Training* (2025) — MPS training-path gaps; VJP-kernel overhead; MLX/MPS gap.
10. GitHub, ml-explore/mlx issue #243 — PyTorch MPS vs MLX training/inference throughput (2023).
11. Towards Data Science (2025-01) — MLX vs PyTorch MPS small-model training/inference timings.
12. Apple Developer Forums thread 815139 — "Is JAX for Apple Silicon still supported?" (Metal issues closed, no active development, Dec 2025).
13. Apple Developer Forums thread 811608 — recent JAX fails on Metal; downgrade to jax==0.4.35.
14. PyPI, `jax-metal` — version/compat table (Sonoma 14.4+, jaxlib pins); "experimental, not all functionality supported."
15. GitHub, jax-ml/jax discussion #34648 — `jax-mps` community PJRT plugin (~3× over CPU on M4); jax-metal "no longer maintained."
16. Krishnapriyan, Gholami, Zhe, Kirby, Mahoney, *Characterizing possible failure modes in PINNs*, NeurIPS 2021 (arXiv:2109.01050).
17. Chenciner & Montgomery, *A remarkable periodic solution of the three-body problem in the case of equal masses*, Annals of Mathematics 152 (2000) 881–901.
18. R. Montgomery, *On the N-body problem* (UCSC) — canonical figure-eight initial conditions.
19. arXiv:2201.01205 — figure-eight ICs and period T ≈ 6.32591398292621 (after Simó).
20. arXiv:2304.01004 — figure-eight ICs restated (Runge–Kutta), equal masses, zero angular momentum.
21. C. Moore, *Braids in classical gravity*, Phys. Rev. Lett. 70 (1993) 3675.
22. KeepingYouAwake README / Apple `caffeinate` man page — caffeinate only prevents sleep with the lid open; flag semantics.
23. pasqualepillitteri.it (2026-04) and VoiceMode portable guide — caffeinate prevents idle (not lid-close) sleep; `caffeinate -i -s <cmd>` pattern; `pmset -g assertions`.
24. Macworld, *Use a MacBook with the lid closed* (2026-05) — on Apple Silicon (Ventura+) neither pmset disablesleep nor caffeinate bypasses lid-close sleep; clamshell/dummy-plug required.
25. Daw, Bu, Wang, Perdikaris, Karpatne, *Mitigating propagation failures in PINNs (R3 sampling)*, ICML 2023.
26. docs.conda.io, *New features* (conda 26.5) — native lockfiles; lockfiles capture conda packages only (pip not by default; yanked-package caveat).
27. tech-champion.com / pythonspeed.com (2025) — two-file model: `conda env export --from-history` + lockfile; update cadence and rollback.
28. GitHub, conda/conda-lock; PyPI conda-lock (2025-12) — cross-platform fully-pinned lockfiles; pip section support.
29. Anaconda, *conda Environment Management Guide* (2025) — locked vs loose specs; build-string pinning; deterministic recreate.
30. Diátaxis (diataxis.fr) — tutorial / how-to / reference / explanation; keep modes separate; minimal inline explanation in action docs.
31. Google SRE Workbook, *Being On-Call* (sre.google) — playbooks: severity/impact + debugging + mitigations; keep entries general to age slowly.
32. Google SRE, *Incident Management Guide* / *Effective Troubleshooting* — playbook-per-alert; "Wheel of Misfortune" drills.
33. Google SRE Workbook, *Incident Response* — "generic mitigations" (stop the bleeding before root cause is known).
34. (General) A. Gawande, *The Checklist Manifesto* — read-do vs do-confirm checklist taxonomy.

Plus the four attached project files: `RESEARCH-CONTEXT-MASTER.md`, `2026-06-10-training-execution-design.md`, `pinn_architecture.md`, `ctl_instruction.md`.
