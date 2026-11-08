# Phase 68 Owner Checkpoint 2: The Yardstick Decision Packet

**Audience:** The project owner (reading time: ~5 minutes).  
**Purpose:** Present the committed known-answer yardstick audit results, the empirical resolution of GAP-59-08, and recommendations for the five reserved charter decisions (C-7, C-2, C-4, C-5, C-6).  
**Committed Audit Evidence:** `.planning/phases/68-yardstick/evidence/yardstick-audit.json`  
**Audit Evidence Commit:** `605d7ad6e10eb96ebfca09f19db1d6a629636254`  
**Audit Evidence SHA-256:** `4b82c21918ba578c9f889cc21f1a93494d12aaa60940b2dac5ef073318922fe4`  
**Status:** `OWNER-DECISION-PENDING` (all five charter rows are open pending owner ruling).

---

## The Decision on One Page

You are asked to make decisions for five reserved charter items. **C-7 must be decided first** because C-5 and the pass bars depend directly on how velocity and energy are measured.

| ID | Item | Recommended Answer | Other Options | Current State |
|---|---|---|---|:---:|
| **C-7** | **Velocity measurement for energy gate (GAP-59-08)** | **A: Autograd velocities in evaluator & validation gate**, via formal clarifying amendment to `pinn_architecture.md` §10.6 | **B:** Dense-grid finite differences;<br>**C:** Retain current coarse gate as-is | **PENDING OWNER RULING** |
| **C-2** | **Definition of Done (PoC target)** | **A: Level 6 at Stage 0** (one network passes the one-shot Stage-0 held-out exam at the C-4 and C-5 bar) | **B:** Level 3 (single-system memorization on 2 of 3 seeds);<br>**C:** Level 9 (every stage 0–6 at its bar) | Pending C-7 ruling |
| **C-4** | **Stage-0 pass bar: position error ($E$)** | **A: Tier 1 ($E \le 0.1$) AND strictly beats both formula and copy** on at least 75% of Stage-0 validation panel | **B:** Valid horizon $h(0.1) \ge 0.5$ on $\ge 75\%$ of validation panel;<br>**C:** Owner-named criterion | Pending C-7 ruling |
| **C-5** | **Stage-0 pass bar: energy drift ($\text{eps}_H$)** | **A: $\text{eps}_H \le 10^{-2}$ from autograd velocities** (conditional on C-7 = A; Tier 2 $\text{eps}_H \le 10^{-3}$ as stretch) | **B:** $\text{eps}_H \le 10^{-3}$;<br>**C:** $\text{eps}_H \le 10^{-5}$ | Pending C-7 ruling |
| **C-6** | **The locked $10^{-5}$ held-out bar** | **A: Replace it by formal amendment** in milestone v2.6 with evidence-based criteria (C-4 & C-5) | **B:** Keep $10^{-5}$ as the unachievable gate | Pending C-7 ruling |

---

## Part 1: C-7 — How Velocity and Energy Drift Are Measured (GAP-59-08)

### 1.1 In Plain Language

In Phase 59, we locked the "ruler" (the FEAS-01 feasibility scorecard). At the same time, we noticed a major potential defect in the production validation gate (`GAP-59-08`): the gate code does not use the model's actual velocities, but instead estimates velocity from predicted positions using finite differences (numerical slope between consecutive output snapshots).

We have now executed the Phase 68 Yardstick Audit on the real numerical ground truth (the Brutus solver trajectories) for the three representative Stage-0 training panel systems (`1632` with 10 inner laps, `851` with 18 inner laps, and `4658` with 39 inner laps).

The audit produced two decisive empirical findings:

1. **The Brutus Numerical Ground Truth Fails the Production Gate:**
   - When we measure energy using Brutus's **explicit recorded velocities** (the FEAS-01 metric), Brutus conserves energy to within machine precision ($\text{eps}_H \le 2.2 \times 10^{-11}$ on gold and $\le 1.9 \times 10^{-14}$ on base), easily reaching **Tier 3**.
   - But when we feed the exact same Brutus positions into the **production finite-difference validation gate**, Brutus **FAILS** the $10^{-5}$ pass mark on every single system, even at the highest native resolution ($dt = 0.01$):
     - System 1632: $\text{eps}_H = 1.09 \times 10^{-3}$ ($109\times$ above the pass line)
     - System 851: $\text{eps}_H = 3.44 \times 10^{-3}$ ($344\times$ above the pass line)
     - System 4658: $\text{eps}_H = 2.38 \times 10^{-2}$ ($2380\times$ above the pass line)
   - On the coarse base grid ($dt = 0.08$), Brutus fails by up to $37,900\times$ ($\text{eps}_H = 0.379$).
   - **Why this happens:** In chaotic 3-body motion, bodies accelerate rapidly during close encounters. Approximating velocity by connecting position points with a straight line incurs a truncation error proportional to $\Delta t^2$ times the third time derivative (jerk). Even with $\Delta t = 0.01$, this error is $10^{-3} - 10^{-2}$.
   - **What this means:** Under finite differences, **not even the true physical solution can pass the $10^{-5}$ gate**. If a neural network were trained to match Brutus positions with 100% accuracy, the gate would fail it.

2. **The Constant Predictor Passes the Production Gate:**
   - A trivial model that always predicts a fixed average position with zero velocity completely fails position accuracy ($E \approx 1.14 - 1.24$, Tier 0).
   - But because its velocity is identically zero, its kinetic energy is zero and its potential energy never changes. Thus $\Delta H \equiv 0$, $\text{eps}_H = 0.0$, $\text{SCS} = -\infty$, and the production gate gives it a **`PASS`**.
   - **What this means:** Finite-difference energy error alone without position accuracy can certify complete nonsense.

### 1.2 Known-Answer Audit Summary Table

| System | Grid | Cadence | Prediction | FEAS-01 Tier | Position Error $E$ | Explicit Velocity $\text{eps}_H$ | Production FD $\text{eps}_H$ | Production FD SCS | Gate Verdict | Ratio to $10^{-5}$ Line |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1632 | gold | $dt=0.01$ | Brutus | **Tier 3** | $0.0000$ | $3.44 \times 10^{-12}$ | **$1.09 \times 10^{-3}$** | -2.96 | **FAIL** | $109\times$ |
| 1632 | gold | $dt=0.01$ | Constant | Tier 0 | $1.1538$ | $0.0000$ | $0.0000$ | -Infinity | **PASS** | $0\times$ |
| 851 | gold | $dt=0.01$ | Brutus | **Tier 3** | $0.0000$ | $2.17 \times 10^{-11}$ | **$3.44 \times 10^{-3}$** | -2.46 | **FAIL** | $344\times$ |
| 851 | gold | $dt=0.01$ | Constant | Tier 0 | $1.2337$ | $0.0000$ | $0.0000$ | -Infinity | **PASS** | $0\times$ |
| 4658 | gold | $dt=0.01$ | Brutus | **Tier 3** | $0.0000$ | $9.15 \times 10^{-12}$ | **$2.38 \times 10^{-2}$** | -1.62 | **FAIL** | $2380\times$ |
| 4658 | gold | $dt=0.01$ | Constant | Tier 0 | $1.1396$ | $0.0000$ | $0.0000$ | -Infinity | **PASS** | $0\times$ |
| *Panel Agg* | *gold* | *$dt=0.01$* | *Brutus* | *Tier 3* | *$0.0000$* | *$2.17 \times 10^{-11}$* | **$0.023797$** | *-1.62* | **FAIL** | **$2380\times$** |
| *Panel Agg* | *base* | *$dt=0.08$* | *Brutus* | *Tier 3* | *$0.0000$* | *$1.88 \times 10^{-14}$* | **$0.378998$** | *-0.42* | **FAIL** | **$37,899\times$** |

### 1.3 The Three C-7 Options

- **Option A (Recommended): Autograd velocities in the evaluator and validation gate.**
  - *Mechanism:* For any neural network prediction, compute $\mathbf{v}(t) = \frac{\partial \mathbf{r}_{\text{pred}}}{\partial t}$ via PyTorch automatic differentiation (`autograd`).
  - *Pros:* Evaluates the true instantaneous velocity implied by the network's continuous trajectory. Completely eliminates the finite-difference truncation error floor ($O(\Delta t^2)$). Aligns the validation gate with the frozen FEAS-01 scorecard convention.
  - *Cons:* Requires a formal clarifying amendment to `pinn_architecture.md` §10.6 in milestone v2.6, and requires the evaluation runner to enable gradient computation with respect to input time $t$.
  - *Recommendation:* **Choose Option A.** It is the only option that restores physical meaning to the energy validation gate.

- **Option B: Finite differences on a dense grid.**
  - *Mechanism:* Keep finite differences, but evaluate on a much denser time grid (e.g., $dt < 0.001$).
  - *Pros:* Retains the gradient-free velocity estimator.
  - *Cons:* As proven by the audit at $dt = 0.01$, truncation error still produces $\text{eps}_H \approx 2.4\%$, far above $10^{-5}$. To reach $10^{-5}$ on close encounters would require $dt \sim 10^{-5}$ (millions of evaluation points per trajectory), making validation prohibitively slow on a Mac.

- **Option C: Retain the existing gate as-is.**
  - *Mechanism:* Keep coarse finite differences ($dt = 0.08$) and the $10^{-5}$ threshold.
  - *Pros:* Requires no specification amendments.
  - *Cons:* Guaranteed 100% failure rate for all valid physical orbits (Brutus fails with $\text{eps}_H \approx 38\%$), while passing the static constant predictor ($\text{eps}_H = 0.0$). The gate ceases to function as a scientific validation tool.

---

## Part 2: C-2, C-4, C-5, C-6 — The Proof-of-Concept Target and Bars

Once C-7 is resolved, we must define what counts as a successful research proof of concept (PoC) for milestone v2.6.

### 2.1 C-1 Context (Recorded Purpose)

Your recorded guidance from 2026-10-25 establishes the foundation:
> "1 and 2. we're not aiming for a perfect research result. I think this project could be more for like a PoC because not many people have done training PINN for 3 body problems in the past... i'm just a freshman in college, and all i have this macbook. so reasonably we wouldn't achieve something great here. but it's just good to see some positive results coming out."

### 2.2 Empirical Baseline Anchors

To set realistic pass bars, we compare against all established benchmarks:

1. **Frozen Baselines (Phase 59):**
   - Two-Kepler Analytic Formula: Median $E = 0.989$ on TRAIN, $0.940$ on validation. Reaches Tier 1 on 0 of 227 validation systems.
   - Nearest-Neighbor Copy: Median $E = 2.135$ on validation. Reaches Tier 1 on 0 of 227 validation systems.
   - Time-Mean Constant Predictor: Median $E = 1.140$ to $1.234$.
2. **Phase 66 Single-Orbit Overfitting Runs:**
   - Overfitting a single Stage-0 training orbit for 1000 steps reached $E = 0.011$ (1632) and $0.017$ (851), proving that the network architecture has sufficient capacity to represent individual orbits at Tier 1.
3. **Primary Scientific Literature:**
   - *Breen et al. (MNRAS 2020):* Trained separate position and velocity ANNs on a restricted 2-parameter equal-mass planar family. Typical energy error without projection was near $10^{-2}$ ($1\%$), with larger spikes during close encounters.
   - *Kollias & Matzakos (2026 preprint):* Forward PINN tests on individual periodic orbits (Euler, Lagrange, figure-eight) achieved energy drift of $7.7 \times 10^{-4}$ to $3.2 \times 10^{-2}$.
   - *Pereira et al. (IAC 2024):* PINN on equal-mass zero-velocity initial conditions reported position errors and physics residuals, but did not attempt unseen chaotic generalization.

### 2.3 Options for C-2: Definition of Done

- **Option A (Recommended): Level 6 at Stage 0.**
  - *Definition:* One trained network passes the one-shot Stage-0 held-out exam (227 validation systems) at the pre-registered C-4 position bar and C-5 energy bar.
  - *Rationale:* Demonstrates genuine out-of-sample generalization on chaotic 3-body motion under a governed, unspent exam. Achieves a real scientific PoC without overclaiming.
- **Option B: Level 3 (Memorization of single orbits).**
  - *Definition:* Learns 1 system on 2 of 3 seeds (Rung 2b). Too weak; already achieved in Phase 66.
- **Option C: Level 9 (All Stages 0–6).**
  - *Definition:* Pass bars on all stages 0 to 6. Impossible today because Stage 3 is empty and Stages 1–6 lack defined data.

### 2.4 Options for C-4: Stage-0 Position Bar ($E$)

- **Option A (Recommended): Tier 1 ($E \le 0.1$) AND strictly beats both formula and copy on $\ge 75\%$ of the Stage-0 validation panel.**
  - *Rationale:* Tier 1 requires the worst body error and inner-pair error to stay within $10\%$ of system scale. Requiring the network to beat both the two-Kepler formula ($E \approx 0.94$) and the copy baseline ($E \approx 2.14$) on $75\%$ of systems ensures genuine physical learning far beyond baseline heuristics.
- **Option B: Valid horizon $h(0.1) \ge 0.5$ on $\ge 75\%$ of validation panel.**
  - Requires trajectories to stay within $10\%$ error for at least half the 10-time-unit integration window.
- **Option C: Owner-specified position criterion.**

### 2.5 Options for C-5: Stage-0 Energy Bar ($\text{eps}_H$)

*Prerequisite: Assumes C-7 is decided as Option A (autograd velocities).*

- **Option A (Recommended): $\text{eps}_H \le 10^{-2}$ (1% energy drift) on autograd velocities; Tier 2 ($\text{eps}_H \le 10^{-3}$) as stretch.**
  - *Rationale:* Matches published results in primary literature (Breen et al. achieved $\sim 10^{-2}$ on restricted families; Kollias & Matzakos achieved $10^{-3} - 10^{-2}$ on periodic orbits). For chaotic orbits across 227 unseen systems, $10^{-2}$ is an ambitious but physically achievable target for a PoC.
- **Option B: $\text{eps}_H \le 10^{-3}$ (0.1% energy drift).**
  - A strict stretch goal; may be overly restrictive for a first PoC on a single MacBook.
- **Option C: $\text{eps}_H \le 10^{-5}$.**
  - The legacy bar; extremely difficult to achieve without specialized projection heads or millions of training steps.

### 2.6 Options for C-6: The Locked $10^{-5}$ Held-Out Bar

- **Option A (Recommended): Replace by formal amendment in milestone v2.6 with the evidence-based bars of C-4 and C-5.**
  - *Rationale:* Aligns the formal project success criteria with the empirical reality established by the yardstick audit and primary literature.
- **Option B: Keep $10^{-5}$ as the formal gate.**
  - *Consequence:* Guarantees project failure regardless of model quality.

---

## Part 3: Next Steps and Instructions for Replying

To proceed, please reply in the chat with your decision on **C-7 first**. You may decide all five items at once if you wish.

**Example Reply Format:**
> `C-7: A`  
> `C-2: A`  
> `C-4: A`  
> `C-5: A`  
> `C-6: A`

Upon receiving your reply, the agent will:
1. Record your exact verbatim ruling in `.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md`.
2. Update `GAP-59-08` in `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md` to `RESOLVED-WITH-INSTRUCTION`.
3. Route the required specification amendments cleanly to milestone `v2.6`.
