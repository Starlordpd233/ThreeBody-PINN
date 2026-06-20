Based on the provided transport package, I have adjudicated the open questions for the doc-03 ("Curriculum and Training Loop") revision. This assessment strictly honors the SCOPE-12 hard constraints, treats the framework specs (`ctl_instruction.md`, `pinn_architecture.md`) as the source of truth, and evaluates the non-authoritative issue doc (`03-curriculum-and-training-loop.md`) against that baseline.

---

### Executive Summary & Hard Constraint Acknowledgment
All reconciliations below are bounded by the **SCOPE-12 Hard Constraints** (`scope-12-hard-constraints.md`). Crucially:
1.  **Network Input**: The 14D `[τ, IC₁₃]` vector is locked. Invariant-heavy descriptors are metadata, not network inputs.
2.  **Loss-Side Softening**: `eps_soft = 1e-5` is locked for the training loss (PHYS-03).
3.  **Characteristic Length**: `D ≈ 4.6416` (raw-mass convention) is locked (PHYS-01). The issue doc's `D = 6.694` is rejected.
4.  **Source of Truth**: Live-code citations in the issue doc are overridden; the framework specs govern.

---

### Section 2: Decisions Requiring Human Approval

#### 1. The Causal-Training-Mode Decision
*   **Issue-Doc Premise**: Frames a choice between Option A (causal), Option B (global + ALM), and Option C (hybrid), claiming Option B is the "current SOT."
*   **Framework-Spec Reality**: The issue doc's premise is **factually incorrect**. `ctl_instruction.md` ("Loss Function Formulation") explicitly *rejects* the dense-residual pseudo-ALM formulation and adopts **causal weighting** ($w_n = \exp(-\eta_c \sum \dots)$) as the PHYS-05 default. `pinn_architecture.md` (§3.2, §4.1) mirrors this. ALM is confined to a P2 ablation for *scalar* conservation constraints only.
*   **Adjudication**: The spec baseline is already **Option A** (Causal Weighting without dense ALM). The framework owner must decide whether to retain the spec's Option A, adopt the issue doc's Option C (Time-Windowed Hybrid, which requires an end-to-end rewrite of the Adam phase), or intentionally regress to Option B (Global + ALM).
*   **Spec-Edit Target**: `ctl_instruction.md` (Phase 2: Total Training Loss) and `pinn_architecture.md` (§3.2).

#### 2. The `s_min`-Frame Decision
*   **Issue-Doc Position**: Proposes Option A (unsoftened geometric gate, softened loss) vs. Option B (softened everywhere).
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 3) explicitly defines $s_{min}$ from "true pairwise separations (no softening)" for the geometric gate, while using $\varepsilon_{inv} = 10^{-10}$ for the static potential and the locked $\varepsilon_{train} = 10^{-5}$ for the training loss.
*   **Adjudication**: The spec **already implements Option A**. The geometric stage gate uses unsoftened $s_{min}$ to honestly flag close encounters, while the network only ever sees softened physics.
*   **Recommendation**: Confirm Option A as the locked spec baseline. No spec edit is required, only documentation reinforcement.

#### 3. The Epsilon-Strategy Decision
*   **Locked Constraint**: Loss-side `eps_soft = 1e-5` (PHYS-03).
*   **Open Question**: Reconcile the static/invariant-computation softening (`1e-10` vs `1e-5`).
*   **Framework-Spec Reality**: The specs already utilize a **Dual-Context** arrangement. `ctl_instruction.md` (Step 3) and `pinn_architecture.md` (§3.4) explicitly separate the offline static invariant softening ($\varepsilon_{inv} = 10^{-10}$) from the dynamic training loss ($\varepsilon_{train} = 10^{-5}$).
*   **Adjudication**: The spec baseline is **Option B (Dual-Context)**. The owner must decide if this scientific split is acceptable, or if the static invariant computation (which dictates stage assignment) should be collapsed to the locked `1e-5` (Option A), thereby altering the physics of the curriculum gates.

---

### Section 3: Confirmed Findings (BLOCKING and MAJOR)

| Finding | Adjudication & Reconciliation | Spec-Edit Target |
| :--- | :--- | :--- |
| **B-07** (Replay/Lookahead) | **Aligned.** `ctl_instruction.md` ("Mini-Batch Construction") already specifies 240 replay, 16 lookahead, and $n_{pts} = \min(cap, snapshots)$ with a 50/50 split. The issue doc's claim that this is "not implemented" applies to legacy code, which is overridden. | None required (Implementation must follow spec). |
| **B-08** (Data vs. Collocation) | **Aligned but needs explicit constructor contract.** `pinn_architecture.md` separates the data term (§3.1, $N=8192$) and physics residual (§3.2). The spec must explicitly mandate that the batch constructor draws these as *independent* point sets to prevent conflation. | `ctl_instruction.md` (Unified Batch Construction). |
| **M6** ($L_{norm}$ clamping) | **Obsolete.** The issue doc claims $L_{norm}$ needs clamping before IC-vector mapping. However, per the locked 14D input constraint, `ctl_instruction.md` (Step 4) explicitly removes $L_{norm}$ from the network input vector; it is now metadata. Clamping is irrelevant to the NN, though it may be retained for staging logic. | None. |
| **M7** ($\tau_L$ excluded) | **Aligned.** Both the issue doc and `ctl_instruction.md` (Step 4) exclude $\tau_L$ from the $IC_{13}$ vector, retaining it strictly for stage gating and evaluation metadata. | None. |
| **M14** (Gradient Clipping) | **Merge Required.** `pinn_architecture.md` (§4.4) uses a fixed `5.0 * median`, while `ctl_instruction.md` defines a per-stage `C` schedule (7-10 / 5 / 3). The spec must be edited to merge these: `clip_value = C_stage * median(grad_history)`. | `pinn_architecture.md` (§4.4). |
| **M15** (Energy Weight) | **Conflict.** Issue doc proposes a `cap_table` (**CLM-11**). Spec (`pinn_architecture.md` §4.1, PHYS-05) uses a linear warmup schedule $\lambda_E^{max}(k)$. Owner must select which schedule governs late-stage training. | `pinn_architecture.md` (§4.1). |
| **M16** ($dt_{out}$ Scaling) | **Hook exists, rule missing.** `ctl_instruction.md` exposes $dt_{out}$ as metadata but defers the scaling rule. Owner must adopt a rule (e.g., $n_{col} \propto dt_{base}/dt_{out}$ using verified **CLM-17** values) and encode it in the spec. | `ctl_instruction.md` (Mini-Batch Construction). |
| **D5** (Stage Transitions) | **Fallback Missing.** Spec lists 4 strict criteria but lacks the dual-path fallback and per-stage thresholds (**CLM-08**, **CLM-09**) proposed by the issue doc. The spec must be edited to include the fallback path to prevent infinite loops. | `ctl_instruction.md` (Stage Transition Criteria). |
| **NS-12** (Componentwise AD) | **Aligned.** `pinn_architecture.md` (§5.3.1, PHYS-02) already mandates componentwise AD and explicitly forbids the summed-output proxy anti-pattern. | None. |
| **NS-13** (Huber $\delta$) | **Conflict.** Issue doc suggests tuning $\delta$ to `0.01-0.1`. Spec (`pinn_architecture.md` §3.4) fixes $\delta = 1.0$. Owner must decide whether to keep the spec baseline or adopt quantile-tuning. | `pinn_architecture.md` (§3.4). |
| **NS-18** (Loss Scaling) | **Misframed by Issue Doc.** Issue doc demands an L1/MAE data-loss contract. Spec (`pinn_architecture.md` §3.1) already has a strict scaling contract but uses **Huber** for the data term. The spec's Huber contract stands under the locked $D$ and $\varepsilon_{train}$. | None. |

---

### Section 6: Data-Driven Adaptive Stage Assignment
*   **Issue-Doc Position**: Proposes replacing fixed thresholds with PCA/K-means clustering and quantile-based boundaries.
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 5) relies on fixed theoretical thresholds (e.g., $E < -0.5$, $s_{min} > 2$).
*   **Adjudication**: This is a fundamental methodology shift. The owner must decide whether to retain the deterministic threshold tables or replace them with the data-driven methodology.
*   **GAP LOGGED**: The deep-dive methodology report (`stage_strat_revision.md`) referenced in the prompt's master and the framed questions **is not attached** in the knowledge base. I cannot evaluate the exact clustering mechanics or population safeguards without it.

---

### Section 7: $\tau_L$, $L_{max}$, and the $D$ Conflict

#### The $D$ Conflict (Worked Seed-Conflict)
*   **Locked Constraint**: $D \approx 4.6416$ (raw-mass, PHYS-01, **CLM-19**).
*   **Issue-Doc Claim**: $D = 6.694$ (total-mass, **CLM-01**).
*   **Adjudication**: The issue doc's $D=6.694$ is definitively rejected. All downstream formulas must be reconciled under $D \approx 4.6416$.

#### $\tau_L$ and $L_{max}$ Computation Formulas
*   **Issue-Doc Position**: Provides a shadow-trajectory routine for $\tau_L$ utilizing split epsilons ($\varepsilon_{pert} = 10^{-8}$, $\varepsilon_{soft} = 10^{-10}$).
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 3) defines $L_{max}$ but lacks the shadow-trajectory $\tau_L$ routine.
*   **Adjudication**: The spec must be edited to inline the $\tau_L$ shadow-trajectory contract. Crucially, this routine must be mathematically re-derived to use the locked raw-mass scaling ($D \approx 4.6416$) rather than the issue doc's total-mass scaling. The split static-softening context ($\varepsilon_{soft} = 10^{-10}$) must be preserved and kept distinct from the locked loss-side $\varepsilon_{train} = 10^{-5}$.
*   **GAP LOGGED**: The attached texts state *that* the $\tau_L$ derivation must be reconciled under $D \approx 4.6416$, but they **do not provide the explicit re-derived mathematical equations or code block** for the shadow trajectory scaling under the raw-mass convention. This derivation is required from the framework owner.

---

### Section 15: ALM $\mu_p$ Clamp
*   **Issue-Doc Position**: Proposes clamping $\mu_p \in [10^{-4}, 100.0]$ to prevent divergence.
*   **Framework-Spec Reality**: The spec explicitly rejects dense-residual ALM. ALM survives *only* as a P2 ablation for scalar conservation constraints (`pinn_architecture.md` §4.2).
*   **Adjudication**: The $\mu_p$ clamp is irrelevant to the baseline training loop. It should be provisionally adopted **only** for the P2 scalar-constraint ALM ablation.
*   **Spec-Edit Target**: `pinn_architecture.md` (§4.2 Optional ALM Ablation).

---

### Registered Gaps & Missing Evidence
The following items are logged as gaps where the attached materials are silent or missing, preventing full autonomous resolution:

1.  **Missing Baseline Report**: `stage_strat_revision.md` is referenced in the `RESEARCH-CONTEXT-MASTER.md` and `framed-research-questions.md` but is **not included** in the attached knowledge base. The data-driven adaptive staging methodology (Section 6) cannot be fully adjudicated without it.
2.  **Missing Mathematical Derivation**: The exact transformed equations for the $\tau_L$ shadow-trajectory perturbation and integration under the locked raw-mass convention ($D \approx 4.6416$) are not present in the text (Section 7).
3.  **Unverified Design Hypotheses**: The per-stage threshold tables (**CLM-08**) and `MAX_EPOCHS` schedules (**CLM-09**) required for the D5 dual-path fallback are `claimed-unverified` design hypotheses in the issue doc. The spec currently lacks them entirely; they must be empirically calibrated by the owner during the Stage-0 pilot.