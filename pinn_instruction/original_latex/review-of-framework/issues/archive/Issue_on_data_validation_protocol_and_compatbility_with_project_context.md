# Pre‑Agent Assessment: Data Validation Protocol vs. Full Project Context

**Date:** 2026‑04‑26  
**Purpose:** This document summarises the gaps, resolutions, and critical issues identified while reviewing the four project documents before tasking an agent to evaluate the data validation protocol. It is intended to be handed to the agent together with the other documents to give full context and remove avoidable ambiguities.

---

## 1. Documents analysed

1. **`main-data-quality-assess.pdf`** – The proposed *Staged Gate* validation protocol.
2. **`<home>/Desktop/3_body_problem/simulation_data/Documentation/README.md`** – Full dataset documentation (simulation data pipeline, folder structure, Brutus output formats, anomalies, etc.).
3. **`main_pinn.pdf`** – The PINN architecture blueprint (SQR‑SkipResNet‑SIREN, loss function, training strategy).
4. **`main_CTL.pdf`** – The Curriculum‑Training‑Labeled (CTL) framework: data preparation, curriculum staging, and the detailed training loop.

---

## 2. Gaps identified from the initial two documents (README + validation PDF)

When only the README and the validation PDF were available, several unknowns prevented a thorough protocol assessment:

1. **Uniform vs. non‑uniform sampling**  
   - Validation PDF assumes **non‑uniform** temporal steps (adaptive Δt from Brutus) and builds the SASD metric around that.  
   - README shows all Brutus output is saved at **fixed** `dt_out` (0.08, 0.17, 0.01).  
   - → *Unknown: which representation would the PINN consume?*

2. **COM/momentum handling for energy metrics**  
   - Hierarchical ICs have non‑zero COM and momentum (median |P| ≈ 0.03).  
   - The PDF’s SCS uses raw lab‑frame data.  
   - → *Should the validation pipeline first recentre to the COM frame?*

3. **Which dataset variants are in scope**  
   - Four Brutus output folders (hierarchical/standard × regular/gold) with different dt_out and tolerances.  
   - → *Do the generic SCS, SASD, IPR thresholds need variant‑specific tuning?*

4. **CTL‑PINN architecture and training role of data**  
   - Without knowing the network’s input/output, collocation strategy, or whether data is used for full supervision vs. boundary conditions, we could not judge if IPR faithfully predicts the PINN’s physics loss or whether the “Overfit Challenge” thresholds are meaningful.

5. **Numerical environment**  
   - Brutus output has 30+ significant digits; validation metrics are in floating point.  
   - → *Is double precision used, and is loss of precision acceptable relative to the PINN’s training noise floor?*

6. **Meaning of “Overfit Challenge” precision**  
   - The PDF says to overfit to “machine precision (< 10⁻⁶)”, but what scale and under what training budget?

---

## 3. Gaps resolved by the PINN architecture and CTL documents

After receiving `main_pinn.pdf` and `main_CTL.pdf`, many of the above uncertainties were eliminated:

| Gap | Resolution |
|-----|------------|
| Uniform vs. non‑uniform sampling | The CTL document confirms the PINN is trained on the existing Brutus snapshots, i.e. **uniform dt_out**. The agent can reinterpret SASD and IPR in a constant‑Δt setting. |
| COM/momentum handling | CTL Step 2.5 explicitly transforms hierarchical ICs (and Brutus outputs) to the **centre‑of‑mass frame** before scaling. The validation pipeline must do the same; the agent can now mandate COM correction for SCS. |
| Dataset variants in scope | The CTL curriculum defines exactly which data tiers (hierarchical, quasi‑random, gold) are used at each stage and their dt_out/tolerances. The agent can calibrate validation thresholds accordingly. |
| PINN architecture & training role | Clear now: 14‑dim input (t + 13 ICs) → 9‑dim position output; velocities/accelerations via AD; loss = data MAE + physics MSE + energy Huber, balanced by ALM; two‑phase Adam→L‑BFGS. The agent can evaluate all validation gates against this concrete model. |
| Numerical environment | CTL uses double‑precision invariant calculation and dimensionless scaling. The validation code will use the same; the remaining float32/float64 training ambiguity is minor. |
| Input/output structure | The network is conditioned on [t, IC] to predict the full state at that instant, without recurrence. The data is used as full supervision (not just initial conditions). This validates the relevance of the IPR metric. |

Thus, the **overall architecture and data usage** are now sufficiently specified for the agent to critique the protocol in detail.

---

## 4. Critical remaining issue: Causal training mismatch

The most important unresolved conflict is between the **causal loss weighting** assumed by the validation PDF and the **actual CTL training loop**.

- **Validation PDF** builds its entire risk analysis around a time‑sequential loss:
  \[
  w_i \propto \exp\!\bigl(-\lambda \sum_{j<i} \mathcal{L}_j\bigr)
  \]
  It warns of “causal firewalls” (a single bad early segment kills the loss for all later times) and designs the SASD/IPR metrics to prevent this.

- **CTL training document** does **not** use any such causal weighting. Instead, it samples time points **globally** (uniform or acceleration‑weighted) from each trajectory, computes standard physics‑informed loss over those points, and balances terms via an Augmented Lagrangian Method (ALM). The curriculum advances **across trajectories** (stable → chaotic), not sequentially within a single trajectory’s time axis.

**Implication** – If the final code follows the CTL document, the causal firewall risk **does not exist**. The SASD metric, while still a useful stiffness indicator, would not have the catastrophic consequence that the validation PDF attributes to it. The entire “Staged Gate” logic, as currently motivated, would need to be either re‑framed or simplified.

The agent **cannot** fully assess the protocol until this ambiguity is resolved. Therefore, the user must explicitly state which of the following is true:

> **A)** The CTL training loop will be augmented with the per‑time‑step causal loss weighting described in the validation PDF.  
> **B)** The validation PDF’s causal logic was an early draft; the actual training will follow the global‑sampling + ALM scheme of the CTL document with **no** sequential time weights.

Without this decision, the agent may waste effort evaluating a risk that is absent, or conversely fail to flag a missing mechanism if causal training is intended.

---

## 5. Minor remaining clarifications

Even if the causal question is resolved, a few secondary points would help the agent work efficiently:

1. **Overfit Challenge precision** – The validation PDF says “machine precision (< 10⁻⁶)”. The CTL stage‑0 physics‑loss threshold is 10⁻⁴. Should the Overfit target be aligned with the curriculum thresholds, or is 10⁻⁶ a fixed requirement?

2. **Input vector dimension inconsistency** – The PINN document’s table lists 14 components (t + 13). The CTL text occasionally mentions 12‑dim (t + 11). While this does not directly affect the validation protocol, the agent might get sidetracked. State which is authoritative.

3. **Gold‑standard data in validation** – The gold subsets have dt_out = 0.01 (much finer than regular sets). Should the same SASD and IPR thresholds be applied to them, or are they assumed to automatically pass the stiffness checks? A brief guideline will prevent over‑flagging.

---

## 6. Recommended information package for the agent

To ensure the agent can produce a precise, actionable assessment, provide:

- All four documents (already available).
- This summary document.
- The definitive statement on **causal training** (Option A or B).
- Clarifications on the three minor points above.

With these, the agent will be able to:
- Judge whether the validation protocol’s causal‑firewall logic is well‑founded.
- Evaluate the mathematical correctness and practicality of SCS, SASD, IPR, and PSC under the actual data format and training setup.
- Identify any integration conflicts between the validation pipeline and the CTL training pipeline.
- Propose improvements without guessing about the intended training methodology.