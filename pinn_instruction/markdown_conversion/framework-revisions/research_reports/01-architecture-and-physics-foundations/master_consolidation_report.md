# Master Research Report: Architecture and Physics Foundations Consolidation
## 1. Purpose and Preservation Rules
This document consolidates four independent architecture-and-physics research reports. It is archival and source-preserving: it organizes existing findings, maps disagreements, and records unique insights. It does not introduce new technical recommendations.

Preservation rules:
- Source reports remain unchanged.
- Report labels are preserved as aliases, not normalized away.
- Consensus is assessed by semantic issue, not raw issue ID.
- Disagreements are retained with source-labeled reasoning.
- Deduplication is allowed only for identical boilerplate or repeated formulas after logging the omitted block.

Source paths:
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/MASTER-AUDIT-2026-05-11.md`
- `pinn_instruction/issues/archive/ARCHIVE_MASTER.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/prompts_for_AI/prompt_for_consolidating_research_results.md`

## 2. Source Reports Inventory
| Report | Path | Lines | `##` count | `###` count | SHA-256 before consolidation |
|---|---|---:|---:|---:|---|
| ChatGPT | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md` | 1142 | 7 | 20 | `955108df182694af825a7e652b3aa3e1818714dd0e8c035e93edabc83db426cd` |
| Claude 1 | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md` | 318 | 9 | 17 | `9ffb9611668f7b897afbb03bba6c3ced4dee195008eadfc0a01a3250b1f7bff8` |
| Claude 2 | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md` | 193 | 6 | 14 | `55c57d1e0674da5681dea6903c0b74f61022f5b878a7fd9f1513f076d1844d87` |
| Gemini | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md` | 176 | 6 | 16 | `bf97859808404e0ccbd98fb27935243ed1f3469ea243d89d7317e6210953976e` |
| Total | four reports | 1829 | 28 | 67 | — |

Inventory note: the verified line and heading counts match the implementation plan. The four source reports were initially untracked in this checkout; they were staged with the master report so the plan's `git ls-files` pre-check now lists them. Unchanged-source verification also records SHA-256 before/after hashes in Section 13.

## 3. Semantic Issue Map and Label Alias Table
Issue labels are not globally stable across reports. A raw label such as B-02, B-04, M10, or D-01 can refer to different topics depending on the report. The consolidation therefore uses semantic issue keys as primary identifiers and preserves report-local labels as aliases. Aliases reference report-local issue IDs (B-02, M3, D-01, etc.), not heading text — the full heading text is preserved verbatim under each Task 6 source block, so a reader can map ID → heading → source content without ambiguity.

| Semantic issue key | Canonical source | ChatGPT label | Claude 1 label | Claude 2 label | Gemini label | Handling rule |
|---|---|---|---|---|---|---|
| SIREN hidden-layer initialization | B-01 | B-01 | B-01 | B-01 | B-01 | Safe same-label agreement candidate after source verification. |
| Characteristic length D and mass scaling | B-02 | B-02 | M3 | B-02/B-03 | B-02 | Preserve ChatGPT dissent that current raw-mass convention may make `D=(G*T^2)^(1/3)` internally consistent. Preserve other reports' `M_tot` argument. |
| Input vector dimensionality and 3D-vs-planar encoding | B-03, M1, M2, B-06 | B-03, M1/M2 | B-06, M1 | B-02/B-03, M1/M2/M3 | B-03/M1/M2 | Treat dimension size, 3D encoding, and planar/3D mismatch as one issue. |
| Input vector composition and open decision D-01 | B-04, D-01 | B-04, D-01 | — | — | B-04, D-01 | Do not treat raw B-04 as semantic agreement. Include Option A, Option B, and current SOT Option C. Keep separate from loss-balancing D-01. |
| COM frame and scaling order | B-05, M3 | B-05, M3 | B-03/B-05 | B-05 | B-05/M3 | Source-verify whether each report recommends recenter/reboost before scaling. |
| Softening mismatch and force-energy consistency | B-09 | B-09, Missed Issue 1 | B-04 | B-06 | B-09 | Preserve dual-epsilon recommendation and ChatGPT's force-law/energy-law incompatibility nuance. |
| Dynamic `omega0` scheduling | B-10 | B-10 | No direct epochwise-scheduling coverage; What Was NOT Flagged item 2 discusses stage/frequency retuning | No substantive coverage; B-10 is constraint counting | B-10 | Mark absent or sparse rather than forcing four-report coverage. |
| AD chain-rule and derivative collapse | AD Chain-Rule section | AD Chain-Rule Factor and Derivative Collapse | B-02 | B-04 | AD Chain-Rule Factor Missing | Treat as one semantic issue even though it is not canonical B-02 in the issue document. |
| Loss-balancing D-01 | D-01/loss-balancing material, B-07/B-08 where present | Missed Issue 3 | B-07/B-08, M8, M9, D-01 | B-07, B-08/B-09, M4, D-01 | Unflagged Gap 2 | Keep separate from input-vector D-01. Explicitly note that D-01 means different things across reports. |
| Constraint counting | M4 | M4 | M2 | B-10, M1/M2/M3 | M4 | Cross-check whether the report discusses 3D active constraints, reduced phase-space DOF, or both. |
| `I_3` and `I_norm` normalization | M5, D-02 | M5, D-02 | No substantive coverage; M3 is characteristic-D normalization, not `I_3`/`I_norm` | M1/M2/M3 normalization discussion | M5, D-02 | Distinguish `I_3` mapping from `I_norm` tanh wrapper. Do not mark D-02 fully settled. |
| LayerNorm attribution and affine setting | M8, D2, D3 | M8 | No direct coverage | No substantive coverage; M8/M9/M10 is a broad remaining-majors sweep | M8, D2/D3 | Mark report gaps explicitly. |
| `E_norm` and mass normalization ranges | M9, M10 | M9/M10 | No substantive coverage; M10 is curriculum-threshold related, not same semantic issue | No substantive coverage; M8/M9/M10 is a broad remaining-majors sweep | M9, M10 | Do not raw-merge Claude 1 M10 or Claude 2 M8/M9/M10 with canonical M9/M10. |
| Minor issue triage D1-D10 | D1-D10 | Minor Issues Triage | Minor Issues Triage | Minor-Issue Triage | Minor Issues Triage | Build a separate minor-triage table with canonical D labels and report-specific notes. |
| Unflagged gaps and unique risks | Gap registry | Missed Issues 1-3 | What Was NOT Flagged | What Was Not Flagged | Unflagged Gaps 1-2 | Preserve as a registry first, then link back to semantic issues where applicable. |

## 4. Executive Summaries
### ChatGPT executive summary

_Source: ChatGPT; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md:3`_

````markdown
## 1. Executive Summary

My overall assessment is that the framework is **not yet ready for implementation**, but not for exactly the reasons the consolidated review claims.

The most serious **confirmed blockers** in the supplied specifications are:

1. An unresolved and mathematically under-specified input/output gauge for the 14D conditioning vector.
2. Inconsistent handling of COM-frame targets.
3. Incorrect automatic-differentiation usage for time derivatives.
4. An internally inconsistent softened dynamics contract between the physics residual and the energy regularizer.

By contrast, the review's claim that the characteristic length must be changed from

$$
D = (G T^2)^{1/3}
$$

to

$$
D = (G M_{\mathrm{tot}} T^2)^{1/3}
$$

is **not correct under the mass convention actually written in the CTL and PINN specs**. That alternative length scale is valid only if all equations are simultaneously rewritten using normalized masses

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}}.
$$

The supplied markdown files are therefore closer to being salvageable than the review suggests, but they still require a disciplined contract rewrite before training.

The highest-confidence conclusions are:

- The hidden-layer SIREN initialization used in the supplied `pinn_architecture.md` is already aligned with the original SIREN derivation. The review is only partially right because the bad formula appears to be an upstream source-document problem, not a problem in the supplied markdown spec.
- The review is right that the input-vector contract is broken across documents, but its preferred “shape invariants + direction cosines” repair is not sufficient for raw Cartesian COM-frame outputs.
- The review is right that derivative handling is wrong in spirit, but it understates the severity: the current formulation drops required chain-rule factors **and** collapses a 9D output derivative into a vector-Jacobian product with `grad_outputs=ones`, which is not the same object as the componentwise time derivative needed for velocities and accelerations.
- The softening problem is worse than reported, because the force law and energy law in the supplied PINN spec are not gradients of the same softened potential.

My smallest mathematically sound repair, without changing the SQR-SkipResNet-SIREN backbone or the CTL curriculum logic, is:

1. Keep the current raw-mass scaling convention and therefore keep

   $$
   D = (G T^2)^{1/3}.
   $$

2. Introduce one unified preprocessing transform that performs COM recentering, zero-momentum boosting, and a **canonical rotation gauge** before invariant computation or supervision.
3. Fix AD derivatives with explicit componentwise Jacobians and the missing factors of $2$ and $4$.
4. Replace the current softened force/potential pair with one consistent softened Hamiltonian.
5. Remove epochwise $\omega_0$ scheduling from the spec.
6. Lock one 14D input contract in both documents.

With those changes, the framework becomes internally coherent enough to test empirically.

---
````

### Claude 1 preface and executive summary

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:3`_

````markdown
## Preface: Source Material and Method

**Important limitation.** This auditor did not have direct access to the three uploaded files (`ctl_instruction.md`, `pinn_architecture.md`, `01-architecture-and-physics-foundations.md`). The audit is therefore conducted against the **structured claims, numbered issues (B-01 … B-10, M1–M10, D1–D10, D-01/D-02), formulas, and design decisions described in the task prompt**, supplemented by ~18 targeted searches into primary literature (Sitzmann 2020; Greydanus 2019; Cranmer 2020; Jin et al. 2020; Wang/Karniadakis NTK; Basir & Senocak ALM/PECANN; Chen et al. GradNorm; Hénon units / NEMO docs; Boekholt & Portegies Zwart 2015 / 2020; Mikkola & Tanikawa 2007; Breen et al. 2020; Badura 2024 AMOS; Scorsoglio et al. 2023) and one focused subagent verification pass on SIREN initialization and PINN time-chain-rule arithmetic. Wherever a claim could not be independently checked because the underlying spec text was unavailable, the report says so explicitly.

---

## 1. Executive Summary

**The framework is not yet trainable as specified.** Of the issues the review enumerates, at least four blockers are unambiguously real (SIREN initialization, AD chain-rule factor, COM-frame data/output mismatch, softening-length scaling mismatch) and at least one major (M-class) issue — the dimension/constraint accounting around 3D vs planar data — is a latent correctness bug that propagates through every loss term. Together these would cause a SIREN-PINN of the depth/width specified (12×256, ω₀ scaling) to either diverge at initialization or to converge on a solution that violates Newton's equations by a constant geometric factor invisible inside the dimensionless training loss. The good news: every blocker except D-01 is a localized formula or pipeline fix; no architectural rewrite is required. SQR-SkipResNet-SIREN with ALM balancing remains viable.

**Highest-impact recommendations**, in order:

1. **Adopt the verified SIREN init formula exactly** (B-01): first layer `U(−1/fan_in, +1/fan_in)` with `sin(ω₀·(Wx+b))`; hidden layers `U(−√(6/fan_in)/ω₀, +√(6/fan_in)/ω₀)`. Multiplication by ω₀ (rather than division) in the hidden-layer bound — a common bug — would produce variance ~ω₀⁴ per layer rather than O(1) and is exactly the failure mode the review is worried about.
2. **Apply the explicit (2/T)ᵏ scaling factors to AD derivatives** at every order. With u = t/T and τ = 2u − 1, velocity = (2/T)·∂r/∂τ and acceleration = (2/T)²·∂²r/∂τ². The Badura 2024 AMOS paper formalizes this exactly.
3. **Move all data into the COM frame before scaling, not after**, and either subtract the COM-output drift or hard-constrain the network output to a 6-DOF representation. Without this, the data-loss term and the residual term live in incompatible frames.
4. **Use a single softening length, expressed in the network's working units**, identical in the Brutus data generator and in the residual loss. ε must be scaled along with positions when units change.
5. **For D-01 (energy regularization methodology), recommend a soft, curriculum-gated energy penalty as the primary tool** — explicitly do NOT switch to HNN- or SympNet-style structural energy parametrization, which would require an architectural rewrite ruled out by the prompt's guardrails.

Below, each blocker and major is treated in proportion to its impact.

---
````

### Claude 2 executive summary

_Source: Claude 2; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md:3`_

````markdown
## 1. Executive Summary

The CTL-PINN framework, as described across CTL Instruction and PINN Architecture, is **not training-ready in its current state, but it is recoverable with a focused P0 fix pass**. The audit's catalogue of BLOCKING, MAJOR, MINOR, and Open-Decision issues is, in substance, well-founded: most BLOCKING items reflect genuine mathematical or physics-of-data problems rather than stylistic preferences. However, a meaningful subset of the audit's flags are documentation errors masquerading as code errors, and at least one (B-01, SIREN initialization) is almost certainly a documentation-only ambiguity that does not require a code change.

The three issues that must be fixed before any further engineering work, regardless of where they sit in the audit's P0–P2 queue, are:

1. **The autograd chain-rule for the $\tau = 2(t/T) - 1$ reparameterization (the B-04 family).** Until velocity and acceleration outputs are correctly scaled by $2/T$ and $(2/T)^2$, the physics residual loss is comparing apples to oranges and the network cannot in principle converge to the true dynamics. This single failure mode silently invalidates every other loss term.
2. **Strict COM-frame enforcement at both input and output (the B-05 frame-handling family).** Mixed-frame data destroys translational equivariance and biases every conserved-quantity penalty. This must be settled before loss-weighting work is meaningful.
3. **Open Decision D-01 (loss-balancing methodology).** Without resolving D-01, no amount of constraint-loss tuning will give reproducible results, because the Augmented Lagrangian Method (ALM) as specified is not the right tool for a sensitive-to-initial-conditions chaotic ODE system.

Items that reduce to documentation drift (B-01 SIREN init wording, D-02 routine cleanup) should be corrected by editing the specs to match the live code, not the other way around. Items that touch the physical contract of the data (characteristic length $D$, softening $\varepsilon$, integrals-of-motion counting) require a single coherent edit pass across both specs.

Overall assessment: **not training-ready; training-ready after P0 fixes (B-01 doc-only, B-02 through B-10 code/spec, D-01 methodology).** Estimated effort is small relative to the architecture itself, because most fixes are localized scalar corrections, dimensional sanity passes, or a single change to the loss-balancer module.
````

### Gemini executive summary

_Source: Gemini; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md:15`_

````markdown
## 1. Executive Summary

While the live codebase occasionally sidesteps the documentation's flaws (such as the SIREN initialization bug), the theoretical blueprint contains contradictions that will systematically corrupt the network's physics loss and curriculum staging. The framework's overarching readiness and core components are assessed as follows:

1. **Readiness Assessment:** The framework is explicitly **not ready for implementation**. Moving forward without rectifying the core scaling and derivative errors will result in a catastrophically failed training loop.
2. **Blockers & Major Issues:** The most severe issues stem from dimensional scaling errors (characteristic length $D$) and missing chain-rule factors in the automatic differentiation pipeline. Furthermore, SIREN weight initialization, constraint counting errors, layer normalization attribution, and normalization range mappings contain severe discrepancies that must be rectified.
3. **Open Decisions:** Option B (Shape Invariants + Direction Cosines) is strongly recommended for the 14-D input vector to circumvent chaotic gimbal lock. The $I_{\text{norm}}$ definition must be wrapped in a `tanh` activation for all network inputs.
4. **Minor Issues Triage:** Issue D4 (COM for Brutus outputs) was elevated to MAJOR. Issues D2/D3 require ablation studies, while D6/D8 are confirmed and deferred. Issues D1, D9, and D10 have been explicitly triaged and resolved, prioritizing $D=6.694$ scaling implementation from day one.
5. **Cross-Issue Dependencies:** The priority queue is validated with critical modifications, ensuring that $D$ scaling, AD chain-rules, and COM transformations strictly block all downstream architectural tasks.
6. **Unflagged Gaps:** A rigorous independent review discovered two critical unflagged gaps regarding missing mass scaling parameters in both the physics residual ($\mathcal{L}_{\text{physics}}$) and the Hamiltonian Energy Regularizer ($\mathcal{L}_{\text{energy}}$), as well as a severe ALM momentum desynchronization vulnerability.
````

## 5. Consensus Matrix
| Semantic issue | Canonical reference | ChatGPT stance | Claude 1 stance | Claude 2 stance | Gemini stance | Consensus status |
|---|---|---|---|---|---|---|
| SIREN hidden-layer initialization | B-01 | Confirms hidden-layer SIREN initialization must divide by hidden omega0. | Confirms paper and reference implementation divide by omega0. | Confirms prose/spec should use paper-exact hidden initialization. | Confirms initialization mismatch and cites literature alignment. | VERIFIED CONSENSUS |
| Characteristic length D and mass scaling | B-02 | SPLIT: current raw-mass convention may keep `D=(G*T^2)^(1/3)` self-consistent. | Supports `D=(G*M_tot*T^2)^(1/3)` under M3. | Supports `D=(G*M_tot*T^2)^(1/3)` under B-02/B-03. | Supports `D=(G*M_tot*T^2)^(1/3)` and adds mass-scaling cascade. | VERIFIED SPLIT |
| Input vector dimensionality and 3D-vs-planar encoding | B-03, M1, M2, B-06 | Confirms 14D input and discusses 3D-vs-planar dimensional conflict. | Confirms 3D/planar dimension conflict but is limited by missing source docs. | Discusses dimension conflicts downstream and links them to D/dimensional consistency. | Confirms 14D input and groups B-03/B-04/M1/M2. | VERIFIED MAJORITY |
| Input vector composition and open decision D-01 | B-04, D-01 | Recommends unified preprocessing; says documented alternatives are incomplete and current SOT is a third option. | No input-vector D-01 coverage; D-01 means energy regularization in this report. | No input-vector D-01 coverage; D-01 means loss balancing in this report. | Recommends Option B under B-04/D-01. | VERIFIED SPLIT |
| COM frame and scaling order | B-05, M3 | Confirms COM-frame issue and discusses scaling/order nuance. | Requires lab-frame data and model outputs to be brought into the same COM frame. | Favors COM-frame consistency with architectural projection. | Requires Galilean correction before normalization/scaling. | VERIFIED SPLIT |
| Softening mismatch and force-energy consistency | B-09 | Confirms softening mismatch and adds force-law/energy-law incompatibility. | Confirms residual softening can differ from Brutus physics. | Confirms softened residual can diverge from pure-Newton labels. | Confirms epsilon mismatch and links to mass-scaling residual risk. | VERIFIED MAJORITY |
| Dynamic `omega0` scheduling | B-10 | Recommends removing runtime omega0 scheduling because omega0 is initialization-only. | No direct epochwise scheduling coverage; separately flags stage/frequency retuning risk. | No substantive coverage; B-10 is constraint counting. | Recommends removing or replacing scheduling with reinitialization. | VERIFIED MAJORITY |
| AD chain-rule and derivative collapse | AD Chain-Rule section | Confirms chain-rule factors and derivative-collapse severity. | Confirms missing chain-rule factor under its AD heading. | Confirms missing tau-to-time conversion under its AD heading. | Confirms missing AD chain-rule factor. | VERIFIED CONSENSUS |
| Loss-balancing D-01 | D-01/loss-balancing material, B-07/B-08 where present | Says the current ALM formulation is not a standard augmented Lagrangian. | Keeps ALM but layers GradNorm-style balancing for soft residuals. | Recommends causal weighting as primary residual balancer and ALM only for hard invariants. | Flags ALM moving-average desynchronization under adaptive collocation. | VERIFIED SPLIT |
| Constraint counting | M4 | Confirms constraint-counting and injectivity argument need correction. | Confirms constraint-counting errors under M2. | Confirms active conserved quantities should be counted differently. | Confirms constraint counting error. | VERIFIED CONSENSUS |
| `I_3` and `I_norm` normalization | M5, D-02 | Separates I3 mapping and tanh-wrapped I_norm; recommendations differ from Gemini for I3 mapping. | No substantive I3/I_norm coverage; M3 is characteristic-D normalization. | Touches normalization bugs in a broader M1/M2/M3 block. | Recommends `2*I3 - 1` and tanh-wrapped I_norm. | VERIFIED SPLIT |
| LayerNorm attribution and affine setting | M8, D2, D3 | Confirms LayerNorm attribution issue and discusses affine setting. | No direct coverage. | No substantive coverage for LayerNorm; broad M8/M9/M10 block preserved separately. | Confirms attribution issue and affine ablation/defaults. | VERIFIED MAJORITY |
| `E_norm` and mass normalization ranges | M9, M10 | Demotes E_norm and mass asymmetry to documentation/acceptable behavior. | No substantive same-topic coverage; M10 is curriculum-threshold motivation. | No substantive same-topic coverage; broad M8/M9/M10 block preserved separately. | Accepts asymmetry/range behavior with documentation. | VERIFIED SPLIT |
| Minor issue triage D1-D10 | D1-D10 | Triages minor items and conditionally elevates some follow-up concerns. | Treats minor issues as mostly routine once blockers are addressed. | Keeps minor issue triage compact and spec-edit oriented. | Elevates selected minor items and preserves routine cleanup. | VERIFIED SPLIT |
| Unflagged gaps and unique risks | Gap registry | Adds unique softening, D-01, and ALM formulation risks. | Adds unique optimizer, spectral, precision, symmetry, replay, and methodology risks. | Adds unique representational, adversarial-loss, precision, and width risks. | Adds unique mass-scaling residual and ALM sampling risks. | UNIQUE |

Consensus-status caveat: statuses are keyed by semantic issue. The canonical-reference column preserves report-local aliases and must not be read as raw issue-ID consensus.

## 6. Issue-by-Issue Consolidation
### SIREN hidden-layer initialization

**Canonical references:** B-01

_Canonical source excerpt(s):_

````markdown
| B-01 | **BLOCKING** | The source architecture document's hidden-layer init table gives a wrong formula: it scales with omega0 instead of dividing by omega0. At hidden_omega0=1 the bug is latent; at omega0=30 variance would explode 810,000x across 12 layers. The live `pinn/basic_architecture.py` implementation already divides by `self.omega_0`; this is a source-document/specification defect, not a current-code defect. | `main_pinn.tex` Table 1 / `sqr_skipresnet_siren_backbone.tex`; live code check: `pinn/basic_architecture.py:37` | Keep/verify `bound = np.sqrt(6.0 / n_in) / hidden_omega0` in code; update the architecture document when LaTeX is revised. |
````
**Report aliases:** ChatGPT: B-01; Claude 1: B-01; Claude 2: B-01; Gemini: B-01

**Consensus status:** VERIFIED CONSENSUS

**Consolidated reading:**
Source blocks below cover the same SIREN initialization defect. Read ChatGPT for source/spec distinction, Claude 1 for the primary-literature derivation, Claude 2 for spec-edit framing, and Gemini for concise issue triage.

**Source: ChatGPT**

_Source heading: `### B-01 — SIREN Hidden-Layer Initialization`_

````markdown
### B-01 — SIREN Hidden-Layer Initialization

**Review reference:** “Confirmed Findings,” row B-01.  
**Affected specs:** `pinn_architecture.md`, section “A Principled Initialization Scheme for SIREN Layers,” plus the architecture summary table.

#### Assessment: Partially confirmed

The review is correct about the underlying mathematics. For hidden SIREN layers with activation

$$
\sin(\omega_0 W x + b),
$$

the principled hidden-layer initialization is

$$
W \sim \mathcal{U}
\left[
-\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0},
\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0}
\right].
$$

The original SIREN derivation treats the first layer differently, choosing small first-layer weights while using a larger fixed $\omega_0$ to span multiple periods over the input domain.

However, the **supplied markdown architecture file already uses the correct hidden-layer divide-by-$\omega_0$ formula**. The problem is not present in the user-provided markdown spec itself. The review is therefore right about the upstream source discrepancy, but wrong if read as a defect in the supplied markdown specification.

#### Solution

Keep the current markdown formula and explicitly freeze the SIREN contract as:

$$
W^{(0)}
\sim
\mathcal{U}
\left[
-\frac{1}{n_{\mathrm{in}}},
\frac{1}{n_{\mathrm{in}}}
\right],
$$

$$
W^{(\ell \ge 1)}
\sim
\mathcal{U}
\left[
-\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0},
\frac{\sqrt{6/n_{\mathrm{in}}}}{\omega_0}
\right].
$$

Add this clarification:

> $\omega_0$ is a fixed layer hyperparameter that must match the initialization contract. It is not a free epochwise scheduling knob.

This is a **document error**, not a current markdown-spec error.

---
````

**Source: Claude 1**

_Source heading: `### B-01 — SIREN weight initialization`_

````markdown
### B-01 — SIREN weight initialization

**Affected sections.** PINN Architecture: SIREN initialization for the 12 hidden layers of 256 neurons. (Review classification: BLOCKING.)

**Review claim (as described in the prompt).** The framework's SIREN init formula is wrong.

**Verdict: CONFIRMING.** This is the single most consequential blocker, and the primary literature is unambiguous. The Sitzmann et al. 2020 paper ("Implicit Neural Representations with Periodic Activation Functions," NeurIPS, arXiv:2006.09661) specifies, in §3.2 ("Distribution of activations, frequencies, and a principled initialization scheme") and Theorem 1.8 of the supplement, the following construction (verified verbatim from the paper plus the official reference implementation at github.com/vsitzmann/siren):

- **First layer.** Weights drawn from `U(−1/fan_in, +1/fan_in)`. Activation is `sin(ω₀·(W·x + b))` with ω₀ a frequency multiplier *inside* the sine, typically ω₀ = 30. The 1/fan_in (linear, **not** 1/√fan_in) is chosen specifically so that the pre-activation ω₀·W·x spans multiple periods of the sine over input x ∈ [−1, 1]. Sitzmann §3.2 states the goal: *"to initialize the first layer of the sine network with weights so that the sine function sin(ω₀·Wx + b) spans multiple periods over [−1, 1]."*
- **Hidden layers.** Weights drawn from `U(−√(6/fan_in)/ω₀, +√(6/fan_in)/ω₀)`. The ω₀ is in the **denominator** (division). This compensates for the ω₀ factor inside the sine so that the pre-sine input remains approximately N(0,1) and the post-sine output remains arcsine-distributed on (−1, 1), preserving signal variance through depth.

**Why this matters mathematically.** Sitzmann's derivation (paper §3.2 plus supplement Theorem 1.8) chains three facts: (i) for X ~ U(−1,1), y = sin(aX+b) is arcsine-distributed on (−1,1) independent of (a,b); (ii) if each weight is U(−c/√n, c/√n), then by CLT wᵀx → N(0, c²/6) as fan-in n grows; (iii) choosing c = √6 makes the pre-sine input N(0,1), and feeding N(0,1) through sine gives arcsine output again — so variance is exactly preserved through every hidden layer. If the hidden bound is taken as `√(6/fan_in) · ω₀` (multiplication, a very common transcription error), then pre-activations have variance ~ω₀²/6 per layer; after 12 layers, signal variance blows up by a factor ω₀²⁴. For ω₀ = 30 this is roughly 10³⁵ — catastrophic at step 0.

**Proposed concrete fix (drop-in PyTorch logic).** In every `SineLayer` constructor:

```python
# omega_0 is the frequency multiplier; w_0_first = 30, w_0_hidden = 1 (or 30) per Sitzmann
if is_first:
    nn.init.uniform_(self.linear.weight, -1.0 / in_features, 1.0 / in_features)
else:
    bound = math.sqrt(6.0 / in_features) / self.omega_0   # DIVISION, not multiplication
    nn.init.uniform_(self.linear.weight, -bound, bound)
# forward:  y = torch.sin(self.omega_0 * (self.linear(x)))
```

If the spec gives `bound = sqrt(6/fan_in) * omega_0` or applies ω₀ outside the linear, both are bugs.

**Stage-0/curriculum implication.** The CTL curriculum's Stage-0 "pre-train on near-Keplerian data" assumes the network can faithfully reproduce a smooth low-frequency signal. With wrong init, Stage 0 cannot converge, and every downstream curriculum threshold becomes meaningless. **B-01 must be fixed before any other stage is benchmarked.**

---
````

**Source: Claude 2**

_Source heading: `### B-01 — SIREN initialization wording (PINN Architecture §, "SIREN initialization")`_

````markdown
### B-01 — SIREN initialization wording (PINN Architecture §, "SIREN initialization")

**CONFIRMED as a documentation-only ambiguity. The live code is almost certainly correct; the spec text should be edited to match it, not vice versa.**

Re-deriving from Sitzmann et al. (2020, NeurIPS), §3 and supplementary §1.5: the first hidden layer uses
$$W^{(1)} \sim \mathcal{U}\!\left(-\tfrac{1}{n},\, \tfrac{1}{n}\right),$$
where $n$ is the fan-in, and subsequent hidden layers use
$$W^{(\ell)} \sim \mathcal{U}\!\left(-\tfrac{\sqrt{6/n}}{\omega_0},\, \tfrac{\sqrt{6/n}}{\omega_0}\right).$$
The official reference implementation (`vsitzmann/siren`, `explore_siren.py`) realises this exactly as `self.linear.weight.uniform_(-np.sqrt(6 / self.in_features) / self.omega_0, np.sqrt(6 / self.in_features) / self.omega_0)`, with the in-code comment stating that for non-first layers "the weights will be divided by `omega_0` so as to keep the magnitude of activations constant, but boost gradients to the weight matrix (see supplement Sec. 1.5)". The semantic role of $\omega_0 = 30$ is a frequency-scaling hyperparameter that pre-multiplies the linear-layer output inside the sine, $\sin(\omega_0(Wx + b))$; dividing the uniform bounds by $\omega_0$ at init compensates so that the pre-sine argument remains approximately unit-variance Gaussian, preserving the alternating-arcsine-vs-normal post-activation pattern derived in Sitzmann's appendix.

The PINN Architecture spec phrases the bound as "U(−sqrt(6/n), sqrt(6/n)) / omega_0". This is mathematically equivalent to the paper's formula because dividing a uniform variable by $\omega_0$ yields a uniform on the divided support — but the prose is ambiguous and easy to misread as "draw weights from $\mathcal{U}(-\sqrt{6/n}, \sqrt{6/n})$, then divide tensors by $\omega_0$ after init", which is a different operation only if interpreted with that ordering. **Recommendation:** treat the live code as ground truth; rewrite the spec line to the unambiguous, paper-exact form
$$W^{(\ell)} \sim \mathcal{U}\!\left(-\tfrac{\sqrt{6/n}}{\omega_0},\, \tfrac{\sqrt{6/n}}{\omega_0}\right), \qquad \omega_0 = 30,$$
with an explicit note that this applies only to hidden layers and that the first layer uses $\mathcal{U}(-1/n, 1/n)$. This is a **doc edit, not a code edit**, conditional on a one-line verification that the code matches the canonical form above. If the code does *not* match it, the bug is in the code; if it does, the bug is in the prose.
````

**Source: Gemini**

_Source heading: `### B-01: SIREN Initialization Mismatch`_

````markdown
### B-01: SIREN Initialization Mismatch
**Context:** The `pinn_architecture.md` document (Section 2.2 "A Principled Initialization Scheme for SIREN Layers" and Section 2.4 "Finalized Architectural Hyperparameters", Table 1) defines the hidden-layer weight initialization formula as scaling *with* $\omega_0$ (i.e., $\mathcal{U}[-\frac{\omega_0}{6 n_{in}}, \dots]$).
**Analysis:** I fully confirm the audit's finding that this formula is incorrect and catastrophic. The original Sitzmann et al. (2020) formulation mandates that pre-activations (the input to the sine function) maintain a standard normal distribution to prevent the frequency from growing uncontrollably with depth [cite: 1, 2, 3]. To achieve this, the weights must be drawn from $\mathcal{U}(-\sqrt{6/n}, +\sqrt{6/n})$. If a custom hidden $\omega_0$ is utilized (though typically $\omega_0 = 1$ for hidden layers), the bounds must be *divided* by $\omega_0$ [cite: 1, 3]. Scaling the variance by a factor of 30 rather than dividing by it would exponentially explode the activation variance across 12 layers.
**Resolution:** The live code (`basic_architecture.py`) is correct. The `pinn_architecture.md` specification must be rewritten to explicitly state:
$$W_i \sim \mathcal{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\omega_0}, \frac{\sqrt{6/n_{\text{in}}}}{\omega_0}\right]$$
````

**Preservation notes:**
All four source blocks are retained verbatim. No issue-specific content was omitted. See Section 12 for cross-reference and omission accounting.

### Characteristic length D and mass scaling

#### Minority/Dissenting Position: ChatGPT

ChatGPT argues that under the raw-mass convention used in the supplied specs, $D = (G T^2)^{1/3}$ is internally consistent and that switching to $D = (G M_{tot} T^2)^{1/3}$ would require simultaneously normalizing all masses. The other three reports support the $M_{tot}$ form. The consolidation does not declare a winner.

**Canonical references:** B-02

_Canonical source excerpt(s):_

````markdown
| B-02 | **BLOCKING** | Characteristic length D has the same wrong formula in both documents: `D = cbrt(G*T^2) ≈ 4.64`, omitting M_tot=3. **Correct:** `D = (G * M_tot * T^2)^(1/3) = (3 * 100)^(1/3) = 6.694` | `main_CTL.pdf` Sec 4.2, `main_pinn.pdf` Table 2 | Adopt D = 6.694 everywhere. Recompute ALL scaled quantities and stage assignments. |

## Quantitative Impact of D Formula Error

CTL's incorrect formula `D = T^(2/3) ≈ 4.6416` is equivalent to using `M_tot = 1`. The correct scale for this project is `D = (G * M_tot * T^2)^(1/3) ≈ 6.6943` for `G = 1`, `M_tot = 3`, and `T = 10`. Therefore

```
D_correct / D_wrong = (300 / 100)^(1/3) = 3^(1/3) ≈ 1.4422495703
```

All wrong-D vs. correct-D relative errors reduce to powers of this exact ratio:

| Quantity | Scaling | Wrong-D vs. Correct-D Factor | Relative Error |
|----------|---------|------------------------------|----------------|
| Scaled positions `r' = r/D` | `r' ∝ 1/D` | `3^(1/3) ≈ 1.4422495703` | **+44.22%** |
| Scaled velocities `v' = vT/D` | `v' ∝ 1/D` | `3^(1/3) ≈ 1.4422495703` | **+44.22%** |
| Scaled kinetic energy `KE' ∝ v'^2` | `∝ 1/D^2` | `3^(2/3) ≈ 2.0800838231` | **+108.01%** |
| Scaled potential magnitude `\|PE'\| ∝ 1/r'` | `∝ D` | `3^(-1/3) ≈ 0.6933612744` | **-30.66%** |
| Raw scaled angular momentum `\|L'\| ∝ r' x v'` | `∝ 1/D^2` | `3^(2/3) ≈ 2.0800838231` | **+108.01%** |
| Virial ratio `Q ∝ v'^2 * r'` | `∝ 1/D^3` | `3` | **+200.00%** |

The angular-momentum row refers to raw scaled `\|L'\|`, not the clamped IC-vector component `L_norm_norm = 2*clip(L/L_max, 0, 1) - 1`. If `L` and `L_max` are recomputed with the same corrected scaling convention, the normalized ratio must be analyzed separately from the raw `D^-2` factor above.

The total signed scaled energy `E' = KE' + PE'` should not be summarized by a single universal percentage: the kinetic component grows by 108.01%, while the potential magnitude shrinks by 30.66%, so the signed total depends on the system's virial state. Quote the per-component values instead.

These errors propagate into every D-dependent normalized IC-vector component fed to the network and into every stage assignment threshold. Systems near curriculum boundaries get systematically wrong stage labels, destroying the curriculum's progressive-learning design.

---
````
**Report aliases:** ChatGPT: B-02; Claude 1: M3; Claude 2: B-02/B-03; Gemini: B-02

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover characteristic length and mass scaling. The main disagreement is ChatGPT's raw-mass convention dissent versus the other reports' M_tot scaling. Read ChatGPT for the dissent, Claude 1 for dimensional analysis, Claude 2 for combined D/dimensional consistency, and Gemini for cascade effects.

**Source: ChatGPT**

_Source heading: `### B-02 — Characteristic Length $D$`_

````markdown
### B-02 — Characteristic Length $D$

**Review reference:** “Confirmed Findings,” row B-02.  
**Affected specs:** `ctl_instruction.md`, “Step 2: Preprocessing: Scaling to Dimensionless Units”; `pinn_architecture.md`, blueprint summary table.

#### Assessment: Disputed

Under the equations actually written in the supplied specs, masses are **not** nondimensionalized by $M_{\mathrm{tot}}$. The CTL and PINN documents continue to use the raw $m_i$ in the scaled energy, angular momentum, physics residual, and energy regularizer.

If one scales only

$$
\mathbf{r}_i = D \mathbf{r}'_i,
\qquad
t = T u,
$$

while leaving $m_i$ unchanged, Newton's law becomes

$$
\frac{d^2 \mathbf{r}'_i}{d u^2}
=
\frac{G T^2}{D^3}
\sum_{j \ne i}
m_j
\frac{
\mathbf{r}'_j - \mathbf{r}'_i
}{
\left\lVert \mathbf{r}'_j - \mathbf{r}'_i \right\rVert^3
}.
$$

To preserve coefficient $1$ in front of the mass-weighted force term, the correct choice under this convention is

$$
D = (G T^2)^{1/3},
$$

which is exactly the convention written in the supplied CTL and PINN specs.

The review's proposed formula

$$
D = (G M_{\mathrm{tot}} T^2)^{1/3}
$$

is only correct if the dynamics are simultaneously rewritten in terms of normalized masses:

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}}.
$$

That is a different scaling convention. The review skipped the second half of the contract.

#### Solution

Choose one convention and carry it through all formulas.

The **minimal-change** choice is to keep the current convention:

$$
D = (G T^2)^{1/3},
\qquad
V = \frac{D}{T},
$$

and retain raw masses in the scaled equations, energy, and residuals.

If the framework owner strongly prefers the review's mass-aware length scale, then all physics equations must be rewritten using normalized masses:

$$
\mu_i = \frac{m_i}{M_{\mathrm{tot}}},
$$

everywhere, not merely in the preprocessing line.

As written, the review's “fix $D=6.694$” would make the specs **less** self-consistent, not more.

---
````

**Source: Claude 1**

_Source heading: `### M3 — Normalization bugs (characteristic length D = (G M_tot T²)^(1/3))`_

````markdown
### M3 — Normalization bugs (characteristic length D = (G M_tot T²)^(1/3))

**Affected sections.** CTL Instruction: data preprocessing and invariant calculations.

**Verdict on the formula.** The framework prompt states "D = (G·M_tot·T²)^(1/3)" as the characteristic length. This is the Kepler-third-law derived length scale: given an orbital period T and a central mass M_tot, the semi-major axis is `a = (G M_tot T²/4π²)^(1/3)`. Dropping the 4π² factor (which is conventional in dimensionless N-body work) yields exactly D = (G M_tot T²)^(1/3). This is dimensionally correct: [G][M][T]² = (L³/(M·T²))·M·T² = L³, cube-root = L. **Confirming the formula's dimensional validity, with the caveat that the conventional factor of (4π²)^(-1/3) is absorbed.**

**Is M_tot or M_avg used?** Hénon units set M_tot = 1, so the choice is moot inside the unit system. If the framework ever leaves Hénon units (e.g. for astrophysical reporting), M_tot is the correct choice — using M_avg would give a length that's smaller by 3^(1/3) ≈ 1.44× for the equal-mass case and break Kepler's third law as written.

**M_avg is wrong.** Recommendation: **use M_tot, and document that the conventional 4π² is absorbed into the definition** (Aarseth 2003, *Gravitational N-Body Simulations*, the standard reference, uses this convention; see NEMO/Hénon-units docs at teuben.github.io/nemo/man_html/units.5.html which state explicitly *"G = 1, M = 1, E = −1/4 where G is the gravitational constant, M the total initial mass, and E the initial energy. The corresponding units of mass, length and time are then U_m = M, U_l = −G M²/(4E), U_t = G M^2.5 /(−4E)^1.5"*).

**Hénon convention cross-check.** In strict Hénon units, with G=1, M=1, E=−¼, the length unit U_l = −GM²/(4E) = 1, which is *defined by energy*, not period. The framework's D = (G M T²)^(1/3) is a *different* length scale — the Kepler-period length, useful when no global E is fixed (e.g. for an open chaotic configuration). These two scales are mutually consistent for a bound system but differ for unbound ejections. **The spec should explicitly say which scale it uses; if both are used in different places, that itself is a major bug.**
````

**Source: Claude 2**

_Source heading: `### B-02 / B-03 — Characteristic length $D$ and dimensional consistency (CTL Instruction §2, "Scales")`_

````markdown
### B-02 / B-03 — Characteristic length $D$ and dimensional consistency (CTL Instruction §2, "Scales")

**CONFIRMED that $D = (G\, M_{\mathrm{tot}}\, T^2)^{1/3}$ is dimensionally correct, but the audit is right that the mass convention requires an explicit spec lock-down.**

Dimensional check with SI: $[G] = \mathrm{m^3\,kg^{-1}\,s^{-2}}$, $[M] = \mathrm{kg}$, $[T^2] = \mathrm{s^2}$, so $[G\,M\,T^2] = \mathrm{m^3}$ and $D$ has units of metres. This is the form Kepler's third law takes when solved for the semi-major axis: $a = (G M T^2 / 4\pi^2)^{1/3}$. The CTL spec drops the $4\pi^2$ factor, which is acceptable for a *characteristic* (not physical) length provided it is used consistently in every downstream rescaling. In natural units with $G = 1$ and $M_{\mathrm{tot}} = 1$ (the Hénon-units convention; Hénon 1971, formalized for stellar dynamics with $G = M = 1$ and virial radius normalized to unity), the relation reduces to $D = T^{2/3}$, which is internally consistent.

The substantive Major issue is **which mass goes into $D$**. The defensible candidates are: (i) $M_{\mathrm{tot}} = \sum_i m_i$; (ii) the reduced mass $\mu$ (ill-defined for three bodies); (iii) the n-body Kepler-analog mass $\left(\sum_{i<j}(m_i m_j)^3/\sum_k m_k\right)^{1/6}$ that appears in Sun's dimensional-analysis generalization of Kepler's third law,
$$T_3 |E_3|^{3/2} = \frac{\pi}{\sqrt{2}} G \left[\frac{(m_1 m_2)^3 + (m_1 m_3)^3 + (m_2 m_3)^3}{m_1 + m_2 + m_3}\right]^{1/2}.$$
For a curriculum where data come from arbitrary-mass three-body systems integrated by Brutus, the only convention that is unambiguous and that matches Hénon-units N-body practice is
$$D \;=\; \left(\frac{G\, M_{\mathrm{tot}}\, T^2}{4\pi^2}\right)^{1/3}, \qquad M_{\mathrm{tot}} = \sum_{i=1}^{3} m_i.$$
**Recommendation:** lock the spec to use $M_{\mathrm{tot}}$ (the simple sum), retain or drop the $4\pi^2$ at the team's discretion *but document the choice in exactly one place* (CTL Instruction §2, "Characteristic Scales"), and propagate that constant explicitly into every downstream rescaling — the velocity unit $D/T$, the energy unit $G M_{\mathrm{tot}}^2/D$, the specific-angular-momentum unit $D^2/T$.
````

**Source: Gemini**

_Source heading: `### B-02: Characteristic Length ($D$) Formula`_

````markdown
### B-02: Characteristic Length ($D$) Formula
**Context:** The `ctl_instruction.md` document (Section Phase 1 - Step 2: "Preprocessing: Scaling to Dimensionless Units") and `pinn_architecture.md` (Section 5.3 "Output Frame and File Format", Table 2) define $D = \sqrt[3]{G T^2}$, omitting total mass.
**Analysis:** I confirm this is a critical dimensional error. From Kepler's Third Law and basic dimensional analysis of Newton's gravitational constant ($[G] = L^3 M^{-1} T^{-2}$), a characteristic length scale derived from time and gravity *must* incorporate mass. Specifically, $L^3 = G M T^2$. Omitting $M_{\text{tot}}$ assumes $M_{\text{tot}} = 1$. In a hierarchical three-body problem where masses sum to approximately 3, this introduces a systematic scaling error of $3^{1/3} \approx 1.44$. All scaled positions, velocities, and energies would be fundamentally distorted. Specifically, this omission introduces relative errors of 44.22% for scaled positions and velocities, 108.01% for scaled kinetic energy and raw scaled angular momentum, -30.66% for scaled potential magnitude, and a severe 200.00% distortion in the virial ratio.
**Resolution:** Adopt the correct formula globally:
$$D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$$
*Note:* This correction triggers a massive hidden dependency regarding the physics residual, which is addressed in Section 6 of this report.
````

**Preservation notes:**
The dissenting ChatGPT block and the three M_tot-supporting blocks are retained. Claude 2 B-02/B-03 is pasted here as the primary location and cross-referenced from input dimensionality. See Section 12 for cross-reference and omission accounting.

### Input vector dimensionality and 3D-vs-planar encoding

**Canonical references:** B-03, M1, M2, B-06

_Canonical source excerpt(s):_

````markdown
| B-03 | **BLOCKING** | Input vector dimensionality claimed as 12D, 13D, and 14D simultaneously across documents. No fixed n_in for the first Linear layer. | `main_CTL.pdf` Sec 4.5, `main_pinn.pdf` Table 2 | Adopt **14D** as canonical: t' (1D) + IC (13D). |
| M1 | MAJOR | CTL assembles 11D IC (masses + 5 invariants + 3 shape invariants); PINN expects 13D IC. Dimension gap of 2 components. | Adopt PINN's 13D IC as architecture contract. |
| M2 | MAJOR | Total dimension claims: 12D (CTL title), 13D (CTL "13-component IC"), 14D (CTL closing note, PINN). No consistent count. | Adopt **14D** as canonical: [t', IC_13D]. |
````
**Report aliases:** ChatGPT: B-03, M1/M2; Claude 1: B-06, M1; Claude 2: B-02/B-03, M1/M2/M3; Gemini: B-03/M1/M2

**Consensus status:** VERIFIED MAJORITY

**Consolidated reading:**
Source blocks below cover fixed input size and 3D/planar encoding. The main preserved difference is how each report scopes the problem. Read ChatGPT for 14D accounting, Claude 1 for planar-vs-3D concerns, Claude 2 via the D block cross-reference, and Gemini for concise grouped triage.

**Source: ChatGPT**

_Source heading: `### B-03 — Input-Vector Dimensionality Conflict`_

````markdown
### B-03 — Input-Vector Dimensionality Conflict

**Review reference:** “Confirmed Findings,” row B-03.  
**Affected specs:** `ctl_instruction.md`, “Step 4: Formulating the Input Vector”; `pinn_architecture.md`, blueprint summary table and input-vector description.

#### Assessment: Confirmed

The CTL spec describes an “11-component IC” and a “12-dimensional input vector,” while the architecture spec describes a 14D input with a 13-component IC vector.

This is a genuine contract break because all of the following depend on one fixed dimension:

- `n_in` for the first linear layer.
- Dataset assembly.
- Normalization.
- Checkpoint compatibility.
- Input serialization.

#### Solution

Lock the interface as

$$
x = [\tau, IC],
\qquad
\tau \in [-1,1],
\qquad
IC \in \mathbb{R}^{13}.
$$

Therefore the network input is

$$
x \in \mathbb{R}^{14}.
$$

Rewrite CTL Step 4 so it enumerates all 13 IC components in the same order as the architecture document.

This blocker cannot be fully closed until D-01 is resolved, because the unresolved five-slot subvector is exactly what keeps the count unstable.

---
````

_Source heading: `### M1 and M2 — IC-Vector Size and Total Input Size`_

````markdown
### M1 and M2 — IC-Vector Size and Total Input Size

**Review reference:** “Confirmed Findings,” rows M1 and M2.  
**Affected specs:** `ctl_instruction.md`, “Step 4”; `pinn_architecture.md`, blueprint summary table.

#### Assessment: Confirmed

M1 and M2 are the major-level manifestations of B-03.

The CTL document currently assembles 11 IC values, while the architecture document reserves space for 13 IC values and a 14D total input.

This cannot be left as “to be clarified later,” because it directly changes:

- `n_in`.
- Checkpoint shapes.
- Data-pipeline serialization.
- Normalization arrays.
- Model compatibility across stages.

#### Solution

Once D-01 is approved, publish a single canonical IC ordering and keep it fixed everywhere:

$$
IC =
[
m_1^{\mathrm{norm}},
m_2^{\mathrm{norm}},
m_3^{\mathrm{norm}},
E^{\mathrm{norm}},
L_{\mathrm{norm}}^{\mathrm{in}},
Q^{\mathrm{norm}},
s_{\min}^{\mathrm{norm}},
I_{\mathrm{norm}}^{\mathrm{in}},
g_1,
g_2,
g_3,
g_4,
g_5
].
$$

The meaning of

$$
g_1,\dots,g_5
$$

must be locked once and never reinterpreted differently across documents.

---
````

**Source: Claude 1**

_Source heading: `### B-06 — Dimension conflicts in the input vector / 3D vs planar`_

````markdown
### B-06 — Dimension conflicts in the input vector / 3D vs planar

**Affected sections.** CTL Instruction (input vector assembly) and Review (mentions "3-body 3D data, not planar" in guardrails).

**Review claim (interpreted).** Inconsistent dimension counts between input-vector size, output dimension, and the planar/3D choice.

**Verdict: PARTIALLY CONFIRMING — cannot fully verify without seeing the spec.** The framework prompt is explicit: "three-body 3D data (not planar)". Breen et al. (2020), in contrast, used **planar** (2D) data; if the spec inadvertently borrowed Breen's input layout (3 bodies × 2D = 6 spatial coordinates) while declaring 3D outputs, the input vector would be 6 short for full initial conditions. A correctly assembled 3D initial-condition vector should have:

- 3 bodies × 3 positions = 9 (or 6 after COM removal),
- 3 bodies × 3 velocities = 9 (or 6 after p_COM = 0),
- 3 masses = 3,
- 1 time scalar = 1,

for a total of typically **18 + 1 = 19** in the lab frame or **12 + 3 + 1 = 16** with COM/momentum reductions applied. The output (3 bodies × 3 positions = 9) is downstream of the time input, while masses+ICs gate the network behavior.

**Proposed fix.** Adopt a single canonical input layout, document it explicitly:

```
input_vec = concat(
    [tau_scalar],                              #  1
    [m1, m2, m3],                              #  3   masses (Henon: m1+m2+m3 = 1)
    [r1_0, r2_0],                              #  6   3D positions of bodies 1 and 2 (r3_0 derived)
    [v1_0, v2_0]                               #  6   3D velocities of bodies 1 and 2 (v3_0 derived)
)                                              # total 16
output  = [r1(t), r2(t), r3(t)]                #  9   positions in COM frame
velocity, acceleration  ← AD of output w.r.t. tau, then scaled by (2/T) and (2/T)²
```

This is consistent with COM reduction, with 3D physics, and with the Hénon mass-normalization convention.

---
````

_Source heading: `### M1 — Dimension gap in 3D vs 2D physical invariants`_

````markdown
### M1 — Dimension gap in 3D vs 2D physical invariants

Covered under B-06/B-07. **Confirming.** Angular momentum must be vector-valued; energy is invariant; linear momentum is vector. All three must use the same canonical 3D form.
````

**Source: Claude 2**

Cross-reference: See `### Characteristic length D and mass scaling` for Claude 2 `B-02 / B-03`; that block is the primary paste for the shared D/dimensional-consistency text.

_Source heading: `### M1, M2, M3 — Dimension gaps, constraint counting errors, normalization bugs`_

````markdown
### M1, M2, M3 — Dimension gaps, constraint counting errors, normalization bugs

These are downstream of B-02/B-03/B-08/B-10 and resolve once those are settled by the unit-discipline pass and the constraint-count correction. **Confirmed.** Fix as part of a single coherent edit to CTL Instruction §2–§3 and PINN Architecture §5.
````

**Source: Gemini**

_Source heading: `### B-03, B-04, M1, M2: Input Vector Dimensionality and Composition`_

````markdown
### B-03, B-04, M1, M2: Input Vector Dimensionality and Composition
**Context:** Discrepancies exist across `ctl_instruction.md` (Section Phase 1 - Step 4: "Assemble the Final 12-Component Input Vector") and `pinn_architecture.md` (Section 5.3, Table 2) claiming the input vector is 12D, 13D, or 14D. Furthermore, the 5 "orientation" slots in the Initial Condition (IC) vector are disputed.
**Analysis:** I confirm the severity of this inconsistency. A neural network requires a rigid, static input dimension for its first linear layer. The framework cannot proceed until this is locked. The 14D formulation (1 Time component + 13 IC components) provides the requisite information to fully constrain the 9 degrees of freedom of a 3-body system in a COM frame. The composition of this vector is resolved in the "Open Decisions" section below.
**Resolution:** Standardize the architecture to a strict 14D input vector: $[t', \text{IC}_{13D}]$.
````

**Preservation notes:**
ChatGPT, Claude 1, and Gemini blocks are retained. Claude 2 B-02/B-03 is cross-referenced to the characteristic-D subsection to avoid duplicate pasting; its M1/M2/M3 block is retained here. See Section 12 for cross-reference and omission accounting.

### Input vector composition and open decision D-01

**Canonical references:** B-04, D-01

_Canonical source excerpt(s):_

````markdown
| B-04 | **BLOCKING** | Input vector composition is unresolved. Audit recommends 5 trig values for 3 angles. Causal_Trainingmismatch argues trig encodings suffer gimbal lock during chaotic scattering and proposes shape invariants + direction cosines. | `main_pinn.pdf` Table 2 vs `main_CTL.pdf` Sec 4.5 (synthesis: Audit §5.3 vs Causal_Trainingmismatch §Input Vector) | **Recommended:** shape invariants + direction cosines (see Open Decisions and Section 5). Human approval still required before coding the first Linear layer. <!-- Restored primary-source location refs (main_pinn.pdf Table 2; main_CTL.pdf Sec 4.5) per audit B-04 source. --> |

### [CRITICAL] D-01 — 14-D input vector composition

**Status:** Awaiting human approval
**Source:** issues/01-architecture-and-physics-foundations.md, "Open Decisions" section
**Conflict with current SOT:** Yes — both Option A and Option B differ from the current SOT

What the SOT says today:
- `review_of_framework.md` §2.3 table (lines 208-225) definitively specifies a 13-component IC vector with **shape invariants (I_1, I_2, I_3) PLUS velocity angles (theta_1, theta_2)** — the angle between r' and v' for each body. This is neither Option A nor Option B.
- `ctl_instruction.md` Step 4 (lines 670-818) lists an 11-component IC (missing velocity angles entirely) and labels the total "12-dimensional input vector" — a pre-existing inconsistency documented as SI-CTL-001 below.

What is being asked:
- Which 5 components occupy the orientation/shape slots in the 13-component IC vector?

Options on the table:
- Option A: Trigonometric encoding — 5 values [sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)] from spherical coordinates of L_hat and orbital phase. (Audit B-04, §5.3)
- Option B: Shape invariants + direction cosines — 5 values [I_1, I_2, I_3, cos(theta), sin(theta)] where theta is the angle between L_hat and the z-axis. (Causal_Trainingmismatch blueprint)
- Option C (current SOT): Shape invariants + velocity angles — 5 values [I_1, I_2, I_3, theta_1, theta_2] where theta_i is the angle between r'_i and v'_i. (review_of_framework.md §2.3 table)

**Cross-reference SI-CTL-001:** `ctl_instruction.md` already documents a dimension-count inconsistency (Source Issue SI-CTL-001). The IC vector listing in Step 4 (line 802) shows 11 components labelled "11-component IC" while the code listing (lines 716-740) and `review_of_framework.md` §2.3 table both specify 13 IC components (14D total with time). The dimension-count bug is a symptom of the same underlying ambiguity about what goes into the IC vector.

Why this needs YOU (the framework owner):
- Changing the IC vector composition alters the first Linear layer's input contract, the canonical-ordering logic, the normalization formulas, and the SIREN first_omega0=30 spectral tuning. This is the most consequential single decision in the framework. The issue doc frames Option A vs Option B as a 2-way choice, but the SOT already defines a third option (shape invariants + velocity angles) that neither matches. You must decide among three alternatives.

Cross-link: see [Open Decisions](#open-decisions) for full rationale.
````
**Report aliases:** ChatGPT: B-04, D-01; Claude 1: —; Claude 2: —; Gemini: B-04, D-01

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover input-vector composition. The main disagreement is ChatGPT's three-option framing versus Gemini's Option B recommendation. Claude 1 and Claude 2 use D-01 for a different semantic issue, so their absence is preserved rather than filled with unrelated D-01 content.

**Source: ChatGPT**

_Source heading: `### B-04 — Input-Vector Composition`_

````markdown
### B-04 — Input-Vector Composition

**Review reference:** “Confirmed Findings,” row B-04 and “Open Decisions.”  
**Affected specs:** `ctl_instruction.md`, “Step 4”; `pinn_architecture.md`, input-vector summary; review “Decisions Requiring Human Approval” and “Open Decisions.”

#### Assessment: Problem confirmed; proposed solution disputed

The problem is real: the five disputed slots are unresolved across the documents.

However, the review's recommended Option B,

$$
[I_1, I_2, I_3, \cos\theta, \sin\theta],
$$

is **not sufficient** if the network is asked to predict raw Cartesian COM-frame trajectories.

Those two direction-cosine slots encode only the **inclination** of the invariant plane normal relative to the $z$-axis, not its azimuth. Therefore they do not fix the full 3D rotational gauge.

Option A is also not satisfactory as written, because using only

$$
\sin(\gamma_{\mathrm{orb}})
$$

loses phase information, and the spherical-angle representation becomes ill-conditioned when

$$
L_x = L_y = 0.
$$

Option C preserves more velocity geometry but still needs a gauge choice to become sensible.

#### Solution

Do **not** approve Option B as written.

The smallest sound repair is to add a deterministic **canonical rotation** in preprocessing, so the network is trained in a canonical COM frame rather than an arbitrary raw inertial orientation.

Once that gauge is fixed, the five disputed slots can be populated in a stable and near-minimal way. My recommended D-01 choice is given in the Open Decisions section below.

---
````

_Source heading: `### D-01 — 14D Input-Vector Composition`_

````markdown
### D-01 — 14D Input-Vector Composition

I do **not** recommend approving the review's Option B as written.

Its final two slots,

$$
(\cos\theta, \sin\theta),
$$

encode only one rotational degree of freedom and are insufficient for raw Cartesian COM-frame targets.

I also do not recommend approving Option A as written, because

$$
[
\sin\theta_L,
\cos\theta_L,
\sin\phi_L,
\cos\phi_L,
\sin\gamma_{\mathrm{orb}}
]
$$

is not robustly injective:

- The $\phi_L$ parameterization is ill-conditioned at the poles.
- Using only $\sin\gamma_{\mathrm{orb}}$ loses orbital phase information.

Option C is the closest to usable, but only after the framework fixes the rotational gauge directly in preprocessing.

#### Recommendation

Adopt a **small but critical methodology change**: add a canonical rotation to the CTL preprocessing pipeline.

After COM recentering and momentum removal:

1. Compute the initial angular-momentum unit vector:

   $$
   \widehat{\mathbf{L}}(0)
   =
   \frac{\mathbf{L}(0)}
   {\lVert \mathbf{L}(0) \rVert}.
   $$

2. Rotate the system so

   $$
   \widehat{\mathbf{L}}(0)
   \mapsto
   \widehat{\mathbf{z}}.
   $$

3. Define the in-plane $+\widehat{\mathbf{x}}$ axis using the projected position of the canonically ordered heaviest body at $t=0$.
4. Define $+\widehat{\mathbf{y}}$ by a right-handed basis.
5. Apply that same rotation to the IC and to every target snapshot.
6. Store the inverse rotation for postprocessing back to the original COM frame.

This removes arbitrary global rotational gauge from the learning problem without changing the neural architecture.

Under that gauge-fixed pipeline, approve a **revised Option C** for the last five IC slots:

$$
[g_1,\dots,g_5]
=
[
I_1^{\mathrm{norm}},
I_2^{\mathrm{norm}},
I_3^{\mathrm{norm}},
c_1,
c_2
],
$$

where

$$
I_1^{\mathrm{norm}} = 2I_1 - 1,
$$

$$
I_2^{\mathrm{norm}} = 2I_2 - 1,
$$

$$
I_3^{\mathrm{norm}} = 6I_3 - 1,
$$

and

$$
c_i
=
\cos\theta_i
=
\frac{
\mathbf{r}'_i \cdot \mathbf{v}'_i
}{
\lVert \mathbf{r}'_i \rVert
\lVert \mathbf{v}'_i \rVert
+
\varepsilon
},
\qquad
i=1,2.
$$

Here $i=1,2$ refers to the first two canonically ordered bodies after canonical rotation.

The full recommended canonical 14D input is

$$
x =
[
\tau,
m_1^{\mathrm{norm}},
m_2^{\mathrm{norm}},
m_3^{\mathrm{norm}},
E^{\mathrm{norm}},
L_{\mathrm{norm}}^{\mathrm{in}},
Q^{\mathrm{norm}},
s_{\min}^{\mathrm{norm}},
I_{\mathrm{norm}}^{\mathrm{in}},
I_1^{\mathrm{norm}},
I_2^{\mathrm{norm}},
I_3^{\mathrm{norm}},
c_1,
c_2
].
$$

If the owner rejects canonical rotation and insists on raw Cartesian COM-frame targets, then none of the three currently documented options is sufficient, and D-01 should remain open rather than being “resolved” by Option B.

---
````

Cross-reference: See Section 7, `#### ChatGPT: D-01 alternatives mathematically incomplete`, for ChatGPT's unflagged extension of this issue.

**Source: Claude 1**

No substantive coverage for input-vector D-01; this report uses D-01 for energy regularization.

**Source: Claude 2**

No substantive coverage for input-vector D-01; this report uses D-01 for loss balancing.

**Source: Gemini**

Cross-reference: See `### Input vector dimensionality and 3D-vs-planar encoding` for Gemini `B-03, B-04, M1, M2`; it is the primary paste for the grouped blocker/major block.

_Source heading: `### D-01: 14-D Input Vector Composition`_

````markdown
### D-01: 14-D Input Vector Composition
**Recommendation: Strictly adopt Option B (Shape Invariants + Direction Cosines).**

The decision between trigonometric encoding (Option A) and shape invariants with direction cosines (Option B) dictates how the network understands the spatial configuration of the three-body system. 

| Feature / Metric | Option A: Trigonometric Encoding | Option B: Shape Invariants + Direction Cosines |
| :--- | :--- | :--- |
| **Data Components** | $\sin(\theta_L), \cos(\theta_L), \sin(\phi_L), \cos(\phi_L), \sin(\gamma_{orb})$ | $I_1, I_2, I_3$ (Mutual Distances), $\cos(\theta), \sin(\theta)$ |
| **Reference Frame Reliance** | Heavily relies on spherical coordinate alignment (external frame). | Describes internal triangle geometry independently of external rotation. |
| **Chaotic Regime Stability** | **Poor.** Vulnerable to "Gimbal Lock." If orbital plane flips, derivatives of $\phi_L$ explode to infinity. | **Excellent.** Shape invariants and direction cosines have no coordinate singularities at the poles. |
| **Gradient Behavior** | Injects massive, erratic gradient spikes during close-encounter ejections (Stages 4-6). | Continuous and smooth through all physical encounters (except direct, hard collisions). |
| **Injectivity** | Topological discontinuities can confuse network phase-space mapping. | Highly unique, over-determined mapping of the system's state. |
| **Final Recommendation** | **REJECTED** | **APPROVED / STRONGLY RECOMMENDED** |

Option A proposes encoding the angular momentum vector via spherical coordinates. While common in rigid-body dynamics, this formulation is disastrous for chaotic scattering events. When the angular momentum vector aligns near the z-axis ($\theta_L \approx 0$ or $\pi$), the system enters "gimbal lock." The azimuthal angle $\phi_L$ becomes mathematically undefined, and its derivatives approach infinity. In Stages 4 through 6 of the curriculum, violent ejections and orbital plane flipping are common. Passing near a coordinate singularity will flood the network's first layer with extreme gradient spikes, destroying the Adam optimizer's momentum buffers.

Option B proposes replacing this with shape invariants ($I_1, I_2, I_3$) and direction cosines ($\cos(\theta), \sin(\theta)$). This formulation is vastly superior because mutual distances perfectly define the internal triangle of the three bodies independently of their absolute rotation. They are continuous and smooth through all physical encounters. Direction cosines smoothly track the tilt of the orbital plane without requiring an azimuthal angle, entirely bypassing gimbal lock. Because the bodies are already canonically sorted by mass and distance, this provides a fully unique, over-determined mapping of the system's state without topological discontinuities.
````

**Preservation notes:**
ChatGPT B-04 and D-01 plus Gemini D-01 are retained. Gemini grouped B-03/B-04/M1/M2 is cross-referenced from the dimensionality subsection. ChatGPT Missed Issue 2 is preserved under Section 7 and linked here. See Section 12 for cross-reference and omission accounting.

### COM frame and scaling order

**Canonical references:** B-05, M3

_Canonical source excerpt(s):_

````markdown
| B-05 | **BLOCKING** | COM frame violation in hierarchical ICs. |COM| ~ 9e-3 after Gaussian perturbation. PINN assumes COM-frame outputs but targets are not in COM frame. | `README.md` lines 328-335, `main_CTL.pdf` Sec 4.3, `main_pinn.pdf` Sec 5.2 | Unified COM transformer: recenter + reboost FIRST, then scale. Assert mass consistency. <!-- Added main_pinn.pdf Sec 5.2 reference (was missing) per audit B-05 source. --> |
| M3 | MAJOR | Scaling order: CTL scales in Step 2, COM-transforms in Step 2.5. For hierarchical ICs, scaled COM offset survives. | **COM transform FIRST, then scale.** |

## Frame Convention: Galilean Boost Mandate

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

Hierarchical ICs are perturbed out of the COM frame (Gaussian noise σ=0.01 after COM enforcement). Quasi-random ICs are generated in the COM frame. The PINN architecture assumes all output positions are in the COM frame. Training on mixed-frame data destroys the model's geometric inductive bias — the network expends capacity learning linear coordinate transformations instead of nonlinear gravitational dynamics.

**Resolution:** Apply an aggressive automated Galilean boost during preprocessing, BEFORE any invariant calculation or scaling:

1. Compute COM position and velocity vectors from raw IC masses
2. Subtract COM position/velocity from all raw state vectors
3. Assert `||P_total|| < 1e-12` after transform
4. Only then proceed to scaling (r' = r/D, v' = v/(D/T))
5. Apply the same boost to Brutus output trajectories using the IC-derived COM

This ensures all training data uniformly aligns with the COM-frame output assumption.

**COM transform ordering (M3 fix):** COM transform FIRST, then scale. Scaling preserves non-zero COM; reordering eliminates this artifact.

---
````
**Report aliases:** ChatGPT: B-05, M3; Claude 1: B-03/B-05; Claude 2: B-05; Gemini: B-05/M3

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover COM-frame consistency. All agree the frame mismatch matters, but they differ on ordering and enforcement: ChatGPT preserves a commutation nuance, Claude 1 focuses data/output frames, Claude 2 emphasizes projection, and Gemini requires COM correction before scaling.

**Source: ChatGPT**

_Source heading: `### B-05 — COM-Frame Violation`_

````markdown
### B-05 — COM-Frame Violation

**Review reference:** “Confirmed Findings,” row B-05.  
**Affected specs:** `ctl_instruction.md`, “Step 2.5: Verify Center-of-Mass (COM) Frame”; `pinn_architecture.md`, “Output Frame and File Format.”

#### Assessment: Confirmed

The CTL document states that hierarchical ICs are not initially in the COM frame and that corresponding Brutus outputs may also require transformation. The PINN architecture explicitly assumes COM-frame outputs.

If targets are not in the same frame as the network's inductive bias and input invariants, the model is forced to learn arbitrary translational motion that should have been removed analytically.

#### Solution

Implement exactly one reusable preprocessing transform for both IC files and every Brutus snapshot.

Define

$$
\mathbf{R}_{\mathrm{COM}}
=
\frac{1}{M}
\sum_i
m_i \mathbf{r}_i,
\qquad
\mathbf{V}_{\mathrm{COM}}
=
\frac{1}{M}
\sum_i
m_i \mathbf{v}_i,
$$

where

$$
M = \sum_i m_i.
$$

Then transform

$$
\mathbf{r}_i^{\mathrm{COM}}
=
\mathbf{r}_i - \mathbf{R}_{\mathrm{COM}},
\qquad
\mathbf{v}_i^{\mathrm{COM}}
=
\mathbf{v}_i - \mathbf{V}_{\mathrm{COM}}.
$$

Assert after transformation:

$$
\left\lVert
\sum_i m_i \mathbf{r}_i^{\mathrm{COM}}
\right\rVert
<
10^{-12},
$$

$$
\left\lVert
\sum_i m_i \mathbf{v}_i^{\mathrm{COM}}
\right\rVert
<
10^{-12}.
$$

If D-01 adopts the canonical rotation recommended below, append that rotation to the same transformer so the pipeline has one unambiguous frame contract.

---
````

_Source heading: `### M3 — Order of COM Transform and Scaling`_

````markdown
### M3 — Order of COM Transform and Scaling

**Review reference:** “Confirmed Findings,” row M3.  
**Affected specs:** `ctl_instruction.md`, “Step 2” and “Step 2.5.”

#### Assessment: Disputed as a mathematical bug; accepted as a clarity problem

Under the current convention, $D$ is a global constant and COM subtraction is linear. Therefore scaling and COM correction commute:

$$
\frac{\mathbf{r}_i-\mathbf{R}_{\mathrm{COM}}}{D}
=
\frac{\mathbf{r}_i}{D}
-
\frac{\mathbf{R}_{\mathrm{COM}}}{D},
$$

and

$$
\frac{\mathbf{v}_i-\mathbf{V}_{\mathrm{COM}}}{V}
=
\frac{\mathbf{v}_i}{V}
-
\frac{\mathbf{V}_{\mathrm{COM}}}{V}.
$$

So “COM must happen before scaling” is not, by itself, a mathematical necessity in the current framework.

The real issue is having a single formal transformer, not the order of two commuting linear operations.

#### Solution

Define one preprocessing function whose documented order is:

1. COM/boost correction.
2. Optional canonical rotation.
3. Scaling.

This order is easier to audit and reason about. But the current text should not be classified as a physics error solely because Step 2 is written before Step 2.5.

---
````

**Source: Claude 1**

_Source heading: `### B-03 / B-05 (COM-frame violations) — Lab-frame data vs COM-frame output`_

````markdown
### B-03 / B-05 (COM-frame violations) — Lab-frame data vs COM-frame output

**Affected sections.** CTL Instruction: data preprocessing & invariant calculations. PINN Architecture: output head specification (review says outputs are in COM frame).

**Review claim.** Training data is in lab frame while network outputs are in COM frame, causing inconsistency.

**Verdict: CONFIRMING.** This is a Galilean-invariance hygiene failure with a known, well-understood remedy in the ML-for-N-body literature. The three-body Newtonian equations are translation-invariant; the COM drifts at uniform velocity (Scholarpedia, *Three-body problem*: *"the linear momentum P = Σ m_i ṙ_i conserves; by an appropriate choice of a Galilean frame one can suppose that P = 0 and that the center of mass is at the origin"*). HNN (Greydanus 2019), LNN (Cranmer 2020), and the Breen et al. (2020) three-body neural network — Breen, Foley, Boekholt & Portegies Zwart, "Newton versus the machine: solving the chaotic three-body problem using deep neural networks," *MNRAS* 494(2), 2465–2470 (May 2020) — all assume COM-frame data. Breen et al. explicitly state (§2): *"We restricted the training set to … three equal-mass particles with zero initial velocity, located in a plane. The three particles … are initially positioned at x₁ ≡ (1, 0) with (x₂, x₃) randomly situated somewhere in the unit semicircle in the negative x-axis,"* which is a stronger reduction (translation + rotation + scaling).

Two failure modes follow from a lab-vs-COM mismatch:

1. **Data-loss term** matches lab-frame positions (which include a linear COM drift) while the network is structurally trying to output COM-frame positions. The data MSE has an irreducible floor equal to the COM-drift kinetic energy summed over time.
2. **Energy/HNN regularizer** computes E in COM frame using network outputs while the conserved E of the dataset is in lab frame; these differ by ½ M v_COM² which is constant per trajectory but varies across the dataset, biasing the regularizer.

**Proposed fix.** Standardize on COM-frame data **before** scaling, as is standard practice:

```
For each Brutus trajectory:
  v_COM = Σ m_i v_i(t=0) / Σ m_i              # use t=0 to define the frame
  r_COM = Σ m_i r_i(t=0) / Σ m_i
  r_i'(t) ← r_i(t) − r_COM − v_COM · t        # remove COM drift
  v_i'(t) ← v_i(t) − v_COM
Then apply Hénon-unit scaling.
```

This subtracts the (constant) COM position and the (constant) COM velocity from every snapshot. After this step, the data has identically zero linear momentum and zero COM, matching the network's output convention, and the COM-residual constraint becomes redundant rather than active.

**Alternative ("structural" fix).** Have the network output only 6 of the 9 degrees of freedom (e.g. r₁ and r₂) and derive r₃ = −(m₁ r₁ + m₂ r₂)/m₃ analytically. This enforces COM=0 exactly and removes one redundant DOF from the loss. The framework should pick one approach and document it; doing both is redundant, doing neither is the current bug.

---
````

**Source: Claude 2**

_Source heading: `### B-05 — COM-frame consistency`_

````markdown
### B-05 — COM-frame consistency

**CONFIRMED. This is a structural issue with the data pipeline, not just a normalization preference.**

For the translation-invariant Newtonian Lagrangian there is an exact translational equivariance: if $(\mathbf{r}_i(t))$ is a solution then so is $(\mathbf{r}_i(t) + \mathbf{c})$ for any constant $\mathbf{c}$. A SIREN with no built-in translational-equivariance bias does not know this; if the training distribution is "mostly but not strictly" COM-aligned, the network must waste capacity learning approximate translation invariance on top of the dynamics. Worse, the energy and angular-momentum invariants are *defined* in the COM frame — otherwise $\mathbf{L} = \mathbf{L}_{\mathrm{COM}} + \mathbf{R}_{\mathrm{COM}} \times \mathbf{P}$ contains a spurious second term and kinetic energy carries an additive offset. A physics residual computed on mixed-frame samples will therefore be systematically biased.

The correct discipline is twofold: (i) input the initial conditions in the COM frame, $\sum_i m_i \mathbf{r}_i(0) = 0$ and $\sum_i m_i \dot{\mathbf{r}}_i(0) = 0$; (ii) post-process the network's three position outputs by subtracting the mass-weighted mean inside the model so that the output satisfies $\sum_i m_i \hat{\mathbf{r}}_i(t) = 0$ exactly at every $t$. The latter is a single layer added to the head — it is cheap and removes three degrees of freedom (the three components of COM position) by construction, leaving the network to learn only the six independent COM-frame position degrees of freedom for the three-body system in 3D.

**Recommendation:** make COM-frame enforcement a hard architectural constraint (output projection layer subtracting $\frac{1}{M_{\mathrm{tot}}}\sum_i m_i \hat{\mathbf{r}}_i$ from each $\hat{\mathbf{r}}_i$), not a soft penalty. Document in CTL Instruction §3 ("Frame conventions") that every sample, every initial condition, and every loss term is COM-frame.
````

**Source: Gemini**

_Source heading: `### B-05 & M3: COM Frame Violation and Scaling Order`_

````markdown
### B-05 & M3: COM Frame Violation and Scaling Order
**Context:** Hierarchical ICs are perturbed out of the Center of Mass (COM) frame, but the PINN output assumes a COM frame, as noted in `ctl_instruction.md` (Section Phase 1 - Step 2.5: "Verify Center-of-Mass (COM) Frame") and `pinn_architecture.md` (Section 5.3 "Output Frame and File Format").
**Analysis:** I fully confirm this finding. If the initial conditions possess a net momentum, the network is forced to learn a continuous Galilean translation superimposed on complex non-linear dynamics. Neural networks struggle significantly with mixed reference frames because it destroys the translational invariance inductive bias. Furthermore, scaling coordinates before zeroing the COM permanently bakes scaled offset artifacts into the trajectories.
**Resolution:** Implement a strict preprocessing pipeline ordering:
1. Calculate raw COM position and velocity.
2. Shift all raw ICs and Brutus trajectory snapshots to the COM frame.
3. Assert that total momentum is $< 10^{-12}$.
4. Apply the characteristic scaling factors ($D$ and $V$).
````

**Preservation notes:**
All relevant source blocks are retained verbatim. The split is kept because enforcement mechanism and scaling order are not identical across reports. See Section 12 for cross-reference and omission accounting.

### Softening mismatch and force-energy consistency

**Canonical references:** B-09

_Canonical source excerpt(s):_

````markdown
| B-09 | **BLOCKING** | Softening parameter mismatch by 10^5×. CTL uses eps=1e-10 for invariant E (stage assignment). PINN uses eps_soft=1e-5 for physics residual and energy loss. Different physics for curriculum vs training. | `main_CTL.pdf` Sec 4.4, `main_pinn.pdf` Sec 3.2-3.3 | **Override note:** the 2026-04-27 audit recommended unifying softening at 1e-8; this consolidation overrides that recommendation in favor of the dual-context strategy from `Causal_Trainingmismatch_resolution_blueprint.md`. Adopt Dual-Context Epsilon Strategy: eps=1e-10 for static invariants (CPU/float64), eps_soft=1e-5 for dynamic loss (GPU/float32). See resolution below. <!-- Added override note: dual-epsilon strategy supersedes audit's 1e-8 unify recommendation; sourced from Causal_Trainingmismatch_resolution_blueprint.md. --> |

## Dual-Context Epsilon Strategy

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

The softening parameter epsilon serves two fundamentally different roles that require two different values:

| Context | Hardware | Epsilon | Justification |
|---------|----------|---------|---------------|
| Static invariant calculation (E, Q, stage assignment) | CPU / float64 | **1e-10** | Negligible softening preserves true Newtonian fidelity. Calculated invariants accurately shadow the unsoftened Hamiltonian. |
| Dynamic loss optimization (physics residual, energy loss) | GPU / float32 | **1e-5** | Numerical regularization floor prevents gradient explosion and NaN propagation during close encounters in single-precision arithmetic. |

The dual-epsilon approach cleanly separates ground-truth physical precision from GPU numerical regularization. The network learns exact Hamiltonian dynamics regularized by a microscopic floor calibrated to GPU precision limits — it does NOT learn "softened physics."
````
**Report aliases:** ChatGPT: B-09, Missed Issue 1; Claude 1: B-04; Claude 2: B-06; Gemini: B-09

**Consensus status:** VERIFIED MAJORITY

**Consolidated reading:**
Source blocks below cover softening mismatch. The shared topic is inconsistent physics between data, residuals, and energy calculations. Read ChatGPT for force/energy incompatibility, Claude 1 and Claude 2 for Brutus/residual mismatch, and Gemini for concise issue triage plus related mass-scaling gap.

**Source: ChatGPT**

_Source heading: `### B-09 — Softening Mismatch`_

````markdown
### B-09 — Softening Mismatch

**Review reference:** “Confirmed Findings,” row B-09.  
**Affected specs:** `ctl_instruction.md`, “Step 3” energy and stage features; `pinn_architecture.md`, “Physics Residual Term” and “HNN-Style Energy Regularizer.”

#### Assessment: Confirmed, but the review's resolution is incomplete

The review is right that the CTL and PINN specs currently use different $\epsilon$ values for invariant computation versus training losses.

But the more serious issue is that the supplied PINN spec uses a force law proportional to

$$
\frac{\Delta \mathbf{r}}{(r+\epsilon)^3},
$$

while its energy regularizer uses a potential proportional to

$$
-\frac{1}{r+\epsilon}.
$$

These are **not** force and potential from the same softened Hamiltonian.

Indeed,

$$
-\nabla
\left(
\frac{1}{r+\epsilon}
\right)
=
\frac{\Delta \mathbf{r}}{r(r+\epsilon)^2},
$$

not

$$
\frac{\Delta \mathbf{r}}{(r+\epsilon)^3}.
$$

So the physics residual and energy regularizer are currently enforcing different softened dynamics. The review noticed the epsilon mismatch but missed this deeper incompatibility.

#### Solution

First choose one softened Hamiltonian family for training. The cleanest option is Plummer softening:

$$
V_\epsilon
=
-
\sum_{i<j}
\frac{m_i m_j}{\sqrt{r_{ij}^2+\epsilon^2}},
$$

with matched acceleration

$$
\mathbf{a}_i
=
\sum_{j\ne i}
m_j
\frac{
\mathbf{r}_j-\mathbf{r}_i
}{
\left(r_{ij}^2+\epsilon^2\right)^{3/2}
}.
$$

This is a matched force/potential pair.

After that, decide the epsilon policy. A dual-context policy can be justified:

- Near-unsoftened invariants for curriculum metrics.
- Softened dynamics for training stability.

But it must be documented honestly as “different numerical roles,” not “the same physics.”

---
````

Cross-reference: See Section 7, `#### ChatGPT: Force–energy incompatibility under softening`, for the unflagged force/energy-law extension.

**Source: Claude 1**

_Source heading: `### B-04 — Plummer softening mismatch`_

````markdown
### B-04 — Plummer softening mismatch

**Affected sections.** CTL Instruction (Brutus data softening setting) vs PINN Architecture (softening used in the gravitational residual).

**Review claim.** Softening epsilon in the data integrator differs from softening in the residual.

**Verdict: CONFIRMING (mathematically severe).** Plummer softening replaces the Newtonian force pair `F = −G m₁ m₂ r̂ / r²` with the regularized form `F = −G m₁ m₂ r / (r² + ε²)^(3/2)` (Aarseth 2003; Dehnen 2001; Zhang et al., *MNRAS* 487, 1227, 2019, which writes the Plummer form explicitly and *"ε is termed as gravitational softening length"*). The choice of ε defines an entirely different dynamical system; trajectories at close approach diverge between any two ε values.

If Brutus is run with `ε_data` (possibly 0 or 10⁻⁶ in arbitrary-precision mode) and the residual evaluator uses `ε_resid` ≠ `ε_data`, then the residual is computing forces from a different physical system than the one that produced the data. Worse, **after unit rescaling**, if ε is treated as a constant in physical units rather than rescaled with positions, the dimensionless ε in the working units differs across stages of the curriculum.

**Verdict on the typical Brutus convention.** Brutus is explicitly an arbitrary-precision N-body code; Boekholt & Portegies Zwart (2015, "On the reliability of N-body simulations," *Comput. Astrophys.* — arXiv:1411.6671) emphasize it integrates the un-softened problem (this is precisely the point of arbitrary precision: close encounters are resolved by adding digits, not by softening). Therefore the data is most likely **un-softened** (ε_data = 0), and the residual softening ε_resid > 0 introduces a systematic O(ε²/r²) force error at close approaches — exactly where the chaotic three-body problem spends most of its informative dynamics.

**Proposed fix.**

1. **Default recommendation: ε_resid = 0** (match Brutus). To avoid the singularity in AD, clamp the pair distance with `r_safe = sqrt(r² + ε_min²)` with `ε_min` set to single-precision machine epsilon (~1e-7) only, not a dynamics-altering softening.
2. If softening is required for stability, then ε_data **must equal** ε_resid, both expressed in **scaled (working) units**, and rescaled at every curriculum stage where the length unit changes.
3. Document ε explicitly in the spec; the review's concern about "softening mismatches" is correct and should not be settled by leaving ε undefined.

---
````

**Source: Claude 2**

_Source heading: `### B-06 — Softening parameter mismatch`_

````markdown
### B-06 — Softening parameter mismatch

**CONFIRMED. Any mismatch between training-data $\varepsilon$ and residual-loss $\varepsilon$ is a silent systematic bias on close encounters.**

The Plummer-softened force is
$$\mathbf{F}_{ij} = -G m_i m_j \, \frac{\mathbf{r}_j - \mathbf{r}_i}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}.$$
Brutus is an arbitrary-precision integrator designed (per Boekholt & Portegies Zwart 2015) to resolve close encounters through precision rather than softening. Their canonical Pythagorean three-body benchmark sets $\varepsilon = 0$ and tightens the precision parameter to recover a "true" converged trajectory. If the PINN physics residual uses $\varepsilon > 0$ (a common ML default to avoid divergent gradients near close encounters) while training labels come from $\varepsilon = 0$ Brutus runs, the residual is comparing to a softened force law while the data come from a pure-Newton trajectory; the two are indistinguishable at long range but diverge during the close-passages that dominate three-body chaos.

**Recommendation:** match $\varepsilon$ exactly. Two acceptable patterns: (a) regenerate training data with the same $\varepsilon$ used in the residual; (b) use $\varepsilon = 0$ in the residual and handle the gradient instability either by per-sample gradient clipping or by excluding collocation points with pairwise distance below an $r_{\min}$ threshold from the physics-loss computation during early stages, re-introducing them in late curriculum stages. Option (b) preserves the Brutus contract and is preferred. State the chosen value and physical motivation explicitly in PINN Architecture §5 ("Physics residual").
````

**Source: Gemini**

_Source heading: `### B-09: Softening Parameter ($\epsilon$) Mismatch`_

````markdown
### B-09: Softening Parameter ($\epsilon$) Mismatch
**Context:** The framework uses $\epsilon=10^{-10}$ for calculating invariants and curriculum stages (`ctl_instruction.md` Section Phase 1 - Step 3: "Necessary Calculations of Invariants"), but $\epsilon_{\text{soft}}=10^{-5}$ for the neural network's loss function (`pinn_architecture.md` Section 3.2 "Physics Residual Term" and Section 3.3 "HNN-Style Energy Regularizer").
**Analysis:** I dispute the previous audit's recommendation to unify this at $10^{-8}$ and strongly endorse the "Dual-Context Epsilon Strategy." Neural network training on GPUs using FP32 arithmetic is highly susceptible to gradient explosions and NaN propagation. When $r \to 0$ during close encounters, the $1/r^3$ derivative in the physics loss will overflow FP32 limits without a sufficient regularization floor (like $10^{-5}$). Conversely, curriculum stage assignment happens on CPUs in FP64 arithmetic. Using $10^{-10}$ allows the curriculum to accurately shadow unsoftened Hamiltonian dynamics.
**Resolution:** Maintain the dual-context approach. Explicitly document that the network learns Hamiltonian dynamics regularized by a microscopic GPU-precision floor, not "softened physics."
````

**Preservation notes:**
Primary B-09/B-04/B-06 blocks are retained. ChatGPT Missed Issue 1 is preserved in Section 7 and cross-referenced rather than duplicated here. See Section 12 for cross-reference and omission accounting.

### Dynamic `omega0` scheduling

**Canonical references:** B-10

_Canonical source excerpt(s):_

````markdown
| B-10 | **BLOCKING** | Dynamic omega0 scheduling has no runtime effect. `update_omega0()` decays first_omega0 from 30 to 10 over epochs, but omega0 is used ONLY at weight initialization. Changing it post-init does nothing. | `main_pinn.pdf` Sec 2.2, Listing 1 | **Remove the scheduling function.** Use fixed first_omega0=30, hidden_omega0=1. |

## Dynamic Omega0 Scheduling — Removal

**Source:** Audit B-10

The `update_omega0()` function in the PINN architecture document decays first_omega0 from 30 to 10 over epochs. However, omega0 is an **initialization-only parameter** in the SIREN architecture — it controls the frequency scaling baked into weight magnitudes at init time. Changing it post-initialization has no effect on the weights.

**Fix:** Remove the scheduling function entirely. Use fixed `first_omega0=30`, `hidden_omega0=1`. If cross-stage re-initialization is desired for curriculum purposes, document it explicitly as a separate architectural decision with per-stage weight re-initialization — not epoch-based scheduling.

---
````
**Report aliases:** ChatGPT: B-10; Claude 1: No direct epochwise-scheduling coverage; What Was NOT Flagged item 2 discusses stage/frequency retuning; Claude 2: No substantive coverage; B-10 is constraint counting; Gemini: B-10

**Consensus status:** VERIFIED MAJORITY

**Consolidated reading:**
Source blocks below cover runtime omega0 scheduling where present. ChatGPT and Gemini directly address removal. Claude 1 is preserved as sparse adjacent coverage through its spectral-bottleneck gap, while Claude 2 is explicitly marked absent because its B-10 means constraint counting.

**Source: ChatGPT**

_Source heading: `### B-10 — Dynamic $\omega_0$ Scheduling`_

````markdown
### B-10 — Dynamic $\omega_0$ Scheduling

**Review reference:** “Confirmed Findings,” row B-10 and “Dynamic Omega0 Scheduling — Removal.”  
**Affected specs:** `pinn_architecture.md`, “A Principled Initialization Scheme for SIREN Layers.”

#### Assessment: Partially confirmed

I agree that the epochwise scheduler should be removed from the specification.

However, I do **not** accept the review's reasoning without qualification. In standard SIREN, $\omega_0$ is not merely an initialization-only variable; it also appears in the forward-pass sine scaling.

The real problem is that the original SIREN derivation assumes a matched pair:

1. Fixed $\omega_0$.
2. Initialization calibrated to that fixed $\omega_0$.

Changing $\omega_0$ epoch by epoch either:

- Does nothing because it is dead code, or
- Changes the network's frequency scaling after initialization was chosen for a different value.

Both are bad, but they are different bads. From the supplied markdown files alone, I can confirm the **specification error**, but not whether the live implementation makes the function dead or active.

#### Solution

Delete epochwise $\omega_0$ scheduling from the architecture spec.

Use fixed values within a stage:

$$
\texttt{first\_omega\_0} = 30,
\qquad
\texttt{hidden\_omega\_0} = 1.
$$

If the curriculum owner wants stage-dependent frequency priors, do that only at **stage boundaries**, together with a newly documented reinitialization or a new model instance.

This is partly a **document error** and partly a potentially dead-code issue whose runtime status cannot be verified from the supplied files alone.

---
````

**Source: Claude 1**

Cross-reference: No direct epochwise-scheduling coverage. See `### Unflagged gaps and unique risks` and Section 7 for Claude 1 item 2 on stage/frequency retuning.

**Source: Claude 2**

No substantive coverage. Claude 2 B-10 is constraint counting, not omega0 scheduling.

**Source: Gemini**

_Source heading: `### B-10: Dynamic $\omega_0$ Scheduling`_

````markdown
### B-10: Dynamic $\omega_0$ Scheduling
**Context:** `update_omega0()` decays `first_omega_0` from 30 to 10 over epochs in `pinn_architecture.md` (Section 2.2 "A Principled Initialization Scheme...", Listing 1).
**Analysis:** I confirm this is dead code based on a fundamental misunderstanding of the SIREN architecture. The $\omega_0$ parameter dictates the spatial frequency of the initial weights before training begins. Dynamically altering a scalar multiplier in an initialization function during the training loop has absolutely zero effect on the instantiated weight matrices [cite: 1, 3]. 
**Resolution:** Delete the scheduling function. Lock `first_omega_0 = 30` and `hidden_omega_0 = 1`.
````

**Preservation notes:**
ChatGPT and Gemini B-10 blocks are retained. Claude 1 spectral-bottleneck discussion is preserved under Sections 6 and 7 as a separate unflagged gap, not merged into raw B-10. See Section 12 for cross-reference and omission accounting.

### AD chain-rule and derivative collapse

**Canonical references:** AD Chain-Rule section

_Canonical source excerpt(s):_

````markdown
## AD Chain-Rule Factor — Missing Derivative Conversion

**Source:** `review.md` (scaling-contract review)

**Finding (MAJOR):** The PINN takes normalized time τ = 2t/T - 1 as input and outputs dimensionless positions r'(τ). Automatic differentiation computes derivatives with respect to τ, but the physics residual and energy loss require derivatives with respect to physical time t (or dimensionless time u = t/T). The chain-rule conversion factors are:

```
u = t/T
τ = 2u - 1

d/du = 2 * d/dτ        (first derivative: factor of 2)
d²/du² = 4 * d²/dτ²    (second derivative: factor of 4)
```

**Impact if unfixed:**
- Physics residual (uses d²/dτ² as though it were d²/du²): **off by factor of 4**
- Kinetic energy (uses d/dτ as though it were d/du): **off by factor of 4**

**Recommended three-layer separation formalism:**

```
(t, r, v)_raw  →  (u, r', v')_physics-scaled  →  (τ, IC_norm)_network-input
```

With explicit conversion rules:
- `r' = r / D`, `v' = v / (D/T)` (forward scaling)
- `dr'/du = 2 * dr'/dτ` (first derivative conversion)
- `d²r'/du² = 4 * d²r'/dτ²` (second derivative conversion)
- `v = (2D/T) * dr'/dτ`, `a = (4D/T²) * d²r'/dτ²` (back to original units)

Every loss function must declare which space it lives in. The physics loss converts AD derivatives in τ back to derivatives in u before computing the residual.
````
**Report aliases:** ChatGPT: AD Chain-Rule Factor and Derivative Collapse; Claude 1: B-02; Claude 2: B-04; Gemini: AD Chain-Rule Factor Missing

**Consensus status:** VERIFIED CONSENSUS

**Consolidated reading:**
Source blocks below cover derivative scaling from normalized time and component-wise AD. The reports agree this is a correctness issue. Read ChatGPT for derivative-collapse detail, Claude 1 for chain-rule derivation, Claude 2 for tau conversion, and Gemini for compact verification.

**Source: ChatGPT**

_Source heading: `### AD Chain-Rule Factor and Derivative Collapse`_

````markdown
### AD Chain-Rule Factor and Derivative Collapse

**Review reference:** “AD Chain-Rule Factor — Missing Derivative Conversion” and “Explicit AD Implementation Requirement.”  
**Affected specs:** `pinn_architecture.md`, “Physics Residual Term,” “Energy Regularizer,” and “Output Layer and Kinematic Consistency via Automatic Differentiation”; `ctl_instruction.md`, time normalization in Step 4.

#### Assessment: Strongly confirmed; should be elevated to blocking in implementation

The network input is

$$
\tau = \frac{2t}{T} - 1.
$$

Equivalently,

$$
u = \frac{t}{T},
\qquad
\tau = 2u - 1.
$$

Autograd on the input coordinate produces derivatives with respect to $\tau$, not $u$ and not physical time $t$.

The required conversions are

$$
\frac{d}{du}
=
2\frac{d}{d\tau},
$$

and

$$
\frac{d^2}{du^2}
=
4\frac{d^2}{d\tau^2}.
$$

Therefore the correct network-derived dimensionless kinematics are

$$
\mathbf{v}'
=
\frac{d\mathbf{r}'}{du}
=
2
\frac{d\mathbf{r}'}{d\tau},
$$

and

$$
\mathbf{a}'
=
\frac{d^2\mathbf{r}'}{du^2}
=
4
\frac{d^2\mathbf{r}'}{d\tau^2}.
$$

In physical units,

$$
\mathbf{v}
=
\frac{D}{T}\mathbf{v}'
=
\frac{2D}{T}
\frac{d\mathbf{r}'}{d\tau},
$$

and

$$
\mathbf{a}
=
\frac{D}{T^2}\mathbf{a}'
=
\frac{4D}{T^2}
\frac{d^2\mathbf{r}'}{d\tau^2}.
$$

Additionally, using `autograd.grad` with

```python
grad_outputs=torch.ones_like(positions)
```

computes a vector-Jacobian product, not the full componentwise derivative tensor needed for a 9D position output.

#### Solution

Compute derivatives componentwise, or use a Jacobian API that returns the full output-by-input derivative.

The implementation contract should be:

$$
\mathbf{r}' = f_\theta(\tau, IC),
$$

$$
\frac{d\mathbf{r}'}{du}
=
2
\frac{\partial f_\theta}{\partial \tau},
$$

$$
\frac{d^2\mathbf{r}'}{du^2}
=
4
\frac{\partial^2 f_\theta}{\partial \tau^2}.
$$

Until this is fixed, the physics residual and the energy regularizer are numerically inconsistent with the stated preprocessing.

---
````

**Source: Claude 1**

_Source heading: `### B-02 — Missing chain-rule factor in automatic differentiation`_

````markdown
### B-02 — Missing chain-rule factor in automatic differentiation

**Affected sections.** PINN Architecture (AD-based velocity/acceleration) + CTL Instruction (input-vector assembly, time scaling).

**Review claim.** AD chain-rule factor missing.

**Verdict: CONFIRMING.** This is a quantitative correctness bug, not a style issue. With the standard PINN pipeline of:

- normalized time u = t/T (T = curriculum-stage time horizon in working units),
- reparameterized SIREN input τ = 2u − 1 to map into [−1, 1],
- network output r(τ) = position trajectory,

then by chain rule:

- `dr/dt = (dr/dτ) · (dτ/du) · (du/dt) = (dr/dτ) · 2 · (1/T) = (2/T) · ∂r/∂τ`
- `d²r/dt² = (4/T²) · ∂²r/∂τ²`

These factors are necessary for the Newton residual `m·d²r/dt² − F_grav(r) = 0` to make dimensional sense. Without them, the residual loss is being computed in units of (position/τ²), but F_grav is in units of (position/t²), with the two differing by 4/T². For Stage 0 (typical T ~ few Hénon time units) the discrepancy is modest (factor ~10), but for late curriculum stages with T ~ 10³ Hénon times, the factor becomes ~4·10⁶, and ALM lambda multipliers will be driven to grotesque values trying to compensate.

This exact chain-rule treatment is formalized in Badura et al. (2024, AMOS conference proceedings, App. B, Eqs. 18–20) for PINN-based orbit determination, citing Scorsoglio, Ghilardi & Furfaro, "A Physic-Informed Neural Network Approach to Orbit Determination," *J. Astronaut. Sci.* 70(4), 2023. Badura is explicit (verbatim from §App. B): *"the first and second order partial derivatives that are computed by the automatic differentiation procedure must be scaled by the factors c and c², respectively, in order to provide appropriately scaled velocity and accelerations,"* where c = 2/(t_f − t₀).

**Proposed fix.** Wherever the residual is computed:

```python
# u = t / T;  tau = 2*u - 1  is the SIREN input
r = net(tau, ic_vec)                                 # shape (B, 9)  — 3 bodies × 3 dims
dr_dtau   = grad(r, tau, ones, create_graph=True)
d2r_dtau2 = grad(dr_dtau, tau, ones, create_graph=True)
v   = (2.0 / T) * dr_dtau          # velocity in canonical units
acc = (2.0 / T)**2 * d2r_dtau2     # acceleration in canonical units
residual = m * acc - F_grav(r)
```

**Per-component vs collapsed-Jacobian subtlety.** The 9-D output must be differentiated per scalar component (or with `torch.autograd.grad(..., is_grads_batched=True)` / `jacrev`). A single `grad(r.sum(), tau)` is mathematically equivalent only if the user intends to sum residuals — which the framework does not. The review's worry about "component-wise vs collapsed Jacobian" is well founded; the safe pattern is to call `grad` once per output dimension or use `functorch.jacrev` / `torch.func.jacrev` (PyTorch ≥2.0).

---
````

**Source: Claude 2**

_Source heading: `### B-04 — Autograd chain rule for $\tau = 2(t/T) - 1$ (PINN Architecture §, "AD-derived velocities/accelerations")`_

````markdown
### B-04 — Autograd chain rule for $\tau = 2(t/T) - 1$ (PINN Architecture §, "AD-derived velocities/accelerations")

**CONFIRMED as a genuine math-and-code issue with the largest single potential impact on training of any BLOCKER.**

The reparameterization is $u = t/T$, $\tau = 2u - 1 \in [-1,1]$. By the chain rule,
$$\frac{d\mathbf{x}}{dt} = \frac{d\mathbf{x}}{d\tau}\cdot\frac{d\tau}{dt} = \frac{2}{T}\frac{d\mathbf{x}}{d\tau}, \qquad \frac{d^2\mathbf{x}}{dt^2} = \left(\frac{2}{T}\right)^2\frac{d^2\mathbf{x}}{d\tau^2} = \frac{4}{T^2}\frac{d^2\mathbf{x}}{d\tau^2}.$$
Whether this is a code bug depends entirely on which tensor is the autograd leaf. If $t$ is the leaf and $\tau$ is computed from $t$ inside the model's forward pass, PyTorch handles the Jacobian automatically and the factors above are encoded implicitly. If $\tau$ is itself the leaf (the network's input), then `torch.autograd.grad(output, tau)` returns $d\mathbf{x}/d\tau$ and $d^2\mathbf{x}/d\tau^2$, and the factors $2/T$ and $4/T^2$ must be applied manually before insertion into any physics residual that compares against physical velocities or accelerations.

Because PINN Architecture describes $\tau$ as the SIREN input and CTL Instruction describes "velocities/accelerations derived via AD through the time variable", there is a strong likelihood that the leaf is in fact $\tau$ and the Jacobian factors are missing. A single missing factor of $2/T$ on velocities will be silently absorbed by the network's output magnitude during the data-fitting term, but the physics residual
$$\ddot{\mathbf{r}}_i \;=\; \sum_{j\ne i} \frac{G m_j (\mathbf{r}_j - \mathbf{r}_i)}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}$$
will then be off by a constant $T^2/4$ on the LHS, and the network will converge to a pseudo-solution that satisfies a rescaled gravity law, not the physical one. This is precisely the kind of bug that produces a network that "looks like" it trains (loss decreases) but generalizes catastrophically out of distribution.

**Recommendation:** instrument the forward pass so that $t$ (physical time, in units of $T$) is the explicit autograd leaf; compute $\tau = 2t/T - 1$ inside the model; obtain $\dot{\mathbf{x}}$ and $\ddot{\mathbf{x}}$ via `torch.autograd.grad` w.r.t. $t$ directly. Alternatively, keep $\tau$ as the leaf and explicitly multiply derivatives by $2/T$ and $4/T^2$ before any physics-residual use. Add a unit test in which on a Kepler two-body sub-problem (closed-form solution), the recovered velocity matches the analytical $\dot{\mathbf{r}}$ to within float32 noise. That single test would catch the bug in five minutes and constitutes the highest-leverage diagnostic in the entire fix queue.
````

**Source: Gemini**

_Source heading: `### AD Chain-Rule Factor Missing`_

````markdown
### AD Chain-Rule Factor Missing
**Context:** The network takes normalized time $\tau \in [-1, 1]$ but must evaluate physics in dimensionless time $u = t/T$ per `pinn_architecture.md` (Section 3.2 "Physics Residual Term" and Section 5.2 "Output Layer and Kinematic Consistency...").
**Analysis:** I confirm this is a catastrophic mathematical oversight. Because $\tau = 2u - 1$, the first derivative $d/du = 2(d/d\tau)$ and the second derivative $d^2/du^2 = 4(d^2/d\tau^2)$. If the PINN calculates acceleration directly from $d^2/d\tau^2$ without multiplying by 4, the network will attempt to learn a gravitational force that is four times weaker than reality. This will irreparably conflict with the data fidelity loss, causing the Augmented Lagrangian Method (ALM) parameters to oscillate wildly and fail to converge.
**Resolution:** The explicit PyTorch component-wise derivative code provided in the review must be adopted, ensuring `acceleration_u = 4.0 * acceleration_tau` is explicitly hard-coded into the physics residual calculation.
````

**Preservation notes:**
All four source blocks are retained verbatim. No source reasoning was deduplicated. See Section 12 for cross-reference and omission accounting.

### Loss-balancing D-01

**Canonical references:** D-01/loss-balancing material, B-07/B-08 where present

No canonical heading found; issue inferred from report aliases.

**Report aliases:** ChatGPT: Missed Issue 3; Claude 1: B-07/B-08, M8, M9, D-01; Claude 2: B-07, B-08/B-09, M4, D-01; Gemini: Unflagged Gap 2

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover energy regularization, ALM wording, and loss-balancing methodology. The main disagreement is method selection: ChatGPT critiques current ALM, Claude 1 proposes a hybrid, Claude 2 recommends causal weighting plus limited ALM, and Gemini flags moving-average desynchronization.

**Source: ChatGPT**

Cross-reference: See Section 7, `#### ChatGPT: Current scalar ALM rule is not a standard ALM`, for the full source block.

**Source: Claude 1**

_Source heading: `### B-07 / B-08 — Dead code and dimension conflicts in the loss assembly`_

````markdown
### B-07 / B-08 — Dead code and dimension conflicts in the loss assembly

**Verdict: PARTIALLY CONFIRMING — these are documentation/spec bugs.** The review identifies "dead code" and "dimension conflicts" — without the spec text, I cannot confirm exact line numbers. The most plausible reading: an angular-momentum invariant or a 2D cross-product term was left in the spec after migrating from planar to 3D. In 3D, angular momentum is a vector L = Σ m_i (r_i × v_i), not a scalar; if the code computes a scalar L = Σ m_i (x_i v_yi − y_i v_xi) it captures only L_z and silently drops L_x, L_y. Recommended fix: rewrite all conserved quantities as vector quantities and take the appropriate norms (|L|, |P|) in residuals.

---
````

_Source heading: `### M8 — Loss-balancing methodology (ALM vs alternatives)`_

````markdown
### M8 — Loss-balancing methodology (ALM vs alternatives)

**Affected sections.** PINN Architecture: ALM loss balancing.

**Verdict: PARTIALLY CONFIRMING.** ALM (Basir & Senocak's PECANN, J. Comp. Phys. 2022; Son et al.'s AL-PINN, Neurocomputing 2023) is a legitimate and increasingly mainstream choice for PINN loss balancing — Basir & Senocak show convergence guarantees for Helmholtz, Burgers, Klein–Gordon. However, the literature also documents known failure modes:

- **Hyperparameter sensitivity to the penalty schedule.** The penalty parameter μ_k must be increased on a schedule; too slow and constraints aren't enforced, too fast and the problem becomes ill-conditioned (Son et al. 2023, "AL-PINN").
- **Instability on chaotic dynamics.** No published study has demonstrated ALM on a chaotic Hamiltonian problem (three-body, double pendulum). All ALM-PINN results are on parabolic/elliptic PDEs.
- **Alternatives.** NTK-based adaptive weighting (Wang, Yu, Perdikaris, "When and why PINNs fail to train: A neural tangent kernel perspective," *J. Comp. Phys.* 449, 110768, 2022) attacks the same imbalance pathology with theoretical backing in the infinite-width limit. GradNorm (Chen, Badrinarayanan, Lee, Rabinovich, ICML 2018, arXiv:1711.02257) is a multi-task method that has not been widely adopted in PINNs but is mathematically cleaner. Self-adaptive PINNs (McClenny & Braga-Neto, "Self-adaptive physics-informed neural networks," *J. Comput. Phys.* 474, 111722, 2023, doi:10.1016/j.jcp.2022.111722) use per-sample trainable weights.

**Proposed recommendation.** Keep ALM as the primary balancer for the data+IC+BC constraints (its theoretical guarantees suit those terms), but **layer a GradNorm-style rescaling on top** for the energy-conservation and angular-momentum-conservation residuals, which are not Lagrangian constraints in the strict sense (they are derived consequences of the dynamics). This separates "hard" constraints (data, IC) from "soft" consistency terms (E, L). This hybrid is consistent with the recent conditionally adaptive ALM literature (Hu, Basir & Senocak, "Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems," arXiv:2508.15695, 2025).
````

_Source heading: `### M9 — HNN-style energy regularization placement`_

````markdown
### M9 — HNN-style energy regularization placement

See D-01 below — this is conceptually intertwined with the open decision.
````

_Source heading: `### D-01 — Energy regularization methodology (HEAVY analytical weight)`_

````markdown
### D-01 — Energy regularization methodology (HEAVY analytical weight)

**Statement of the choice (as I understand it from the prompt).** Should the framework enforce energy conservation by (a) HNN-style scalar-energy parametrization (network outputs H, dynamics derived from symplectic gradient), (b) soft penalty on |E(t) − E(0)|, (c) symplectic-network architecture (SympNets, Jin et al. 2020), or (d) leave energy unconstrained and rely on data?

**Recommendation: (b), a soft, curriculum-gated energy penalty, as the primary tool, with (a) and (c) explicitly rejected for this framework.**

**Rationale.**

1. **HNN's structural constraint is incompatible with the network's output topology.** HNN (Greydanus, Dzamba & Yosinski, *NeurIPS 2019*, arXiv:1906.01563) parametrizes a *scalar Hamiltonian* H(q,p) and derives dynamics via ∂H/∂p, −∂H/∂q. The current framework's network outputs *positions* r(t) directly, with velocity and acceleration derived by AD — this is a PINN, not an HNN. Switching to HNN would require a complete architectural rewrite (no SIREN as direct trajectory predictor) and is ruled out by the prompt's "no wholesale architectural rewrites" guardrail.
2. **SympNets are also incompatible.** SympNets (Jin, Zhang, Zhu, Tang & Karniadakis, "SympNets: Intrinsic structure-preserving symplectic networks for identifying Hamiltonian systems," *Neural Networks* 132, 166–179, 2020, arXiv:2001.03750) learn symplectic *maps* (one-step integrators), not trajectories. They have universal approximation guarantees over symplectic diffeomorphisms, and Jin et al. specifically demonstrated them on the three-body problem with excellent long-term energy conservation. But replacing the SIREN-trajectory predictor with a SympNet integrator is a complete architectural change.
3. **Soft energy penalty is sufficient when data is plentiful.** Greydanus et al. (2019, Figs. 1–3) shows qualitatively that vanilla MLPs *do* drift in energy (the paper's iconic mass-spring spiral plot), but the drift is data-dependent and typically a small fraction of E over the prediction horizon when training data is dense. For a curriculum that starts at short horizons, the drift is negligible at Stages 0–2; the penalty only becomes load-bearing at Stages 3+. **Therefore enable the energy penalty starting at Stage 3, ramping its ALM weight from 0 to 1 over Stage 3's first 25% of iterations**, with the multiplier λ_E updated by ALM dual ascent: λ_E ← λ_E + μ_k · mean(E(t) − E(0))².
4. **Add angular momentum** as a vector penalty: L_residual = ‖Σ m_i r_i(t) × v_i(t) − L(0)‖. In 3D, this gives three independent constraints rather than one. Galilean reduction (Section B-03) makes the linear-momentum constraint redundant; angular momentum is not redundant.
5. **Virial-theorem check as diagnostic, not loss.** The virial theorem ⟨2T⟩ = −⟨U⟩ holds only for bound, time-averaged orbits; using it as a per-snapshot loss would actively suppress chaotic excursions. Keep it as a Stage-6 validation metric only.

**Why NOT HNN as primary loss.** If the energy regularizer dominates, the network is trained to match a constant (E_0) along trajectories that are by construction chaotic and divergence-sensitive. The dominant gradient direction becomes "stay on the energy surface," not "match Brutus trajectories." In the chaotic regime, two trajectories on the same energy surface are *as different as possible*; the energy constraint is necessary but vastly insufficient.
````

**Source: Claude 2**

_Source heading: `### B-07 — HNN-style energy regularization form`_

````markdown
### B-07 — HNN-style energy regularization form

**PARTIALLY CONFIRMED. The spec's "HNN-style" label is misleading; the term as described is a soft energy-conservation penalty, not an HNN parameterization.**

Greydanus, Dzamba & Yosinski (2019, NeurIPS) parameterize a scalar $H_\theta(\mathbf{q}, \mathbf{p})$ and obtain dynamics by symplectic gradient $\dot{\mathbf{q}} = \partial H/\partial \mathbf{p}$, $\dot{\mathbf{p}} = -\partial H/\partial \mathbf{q}$, which guarantees conservation by construction. The CTL-PINN does not parameterize a scalar Hamiltonian — it parameterizes positions $\hat{\mathbf{r}}_i(t)$ directly and (per the audit) penalizes deviations of $H(\hat{\mathbf{r}}, \dot{\hat{\mathbf{r}}}) = T + V$ from its initial value $H_0$. This is a soft energy penalty, not an HNN. For the three-body system in the COM frame the Hamiltonian is
$$H \;=\; \sum_{i=1}^{3} \frac{|\mathbf{p}_i|^2}{2 m_i} \;-\; \sum_{i<j} \frac{G m_i m_j}{|\mathbf{r}_i - \mathbf{r}_j|},$$
with $\mathbf{p}_i = m_i \dot{\hat{\mathbf{r}}}_i$.

**Recommendation:** retain the soft penalty (replacing it with a true HNN is the "wholesale architectural rewrite" the user has explicitly forbidden), but (i) relabel it in the spec as "soft energy-conservation regularizer", reserving the HNN label for any future architectural pivot; (ii) compute $H$ using the chain-rule-corrected velocities from B-04 in the COM frame; (iii) penalize $|H(t) - H_0|$ summed over collocation times, normalized by $|H_0|$ so the loss is dimensionless and scale-comparable to other terms. Adding three soft linear-momentum penalties is redundant with B-05 (which fixes linear momentum to zero by construction), but three angular-momentum penalties are not redundant and should be retained.
````

_Source heading: `### B-08, B-09 — Dimensional conflicts in loss terms; dead code paths`_

````markdown
### B-08, B-09 — Dimensional conflicts in loss terms; dead code paths

**CONFIRMED in spirit, with the caveat that without the verbatim audit text the specific dimensional conflict cannot be verified from first principles.** The category of bug is, however, real and common in PINN frameworks: if the data-fitting loss is on rescaled positions (dimensionless $\hat{r}/D$) while the physics residual is on physical accelerations (units of $D/T^2$) and the energy term is on physical $H$ (units of $G M^2/D$), the three terms differ in magnitude by orders of magnitude *before* any ALM multiplier is applied. The fix is a unit-discipline pass: rescale every loss term to be dimensionless using $\{D, T, M_{\mathrm{tot}}\}$ as the unit set, so the remaining magnitude differences are physical, not unit-conversion, and the loss balancer is doing real work.

For "dead code paths" (B-09 family): without access to the live code, this is unverifiable, but the audit's framing suggests stubs or branches prototyped and never wired in. **Recommendation:** delete and document, not refactor; the goal is to make the live code a faithful instantiation of the corrected spec.
````

_Source heading: `### M4 — ALM specification details`_

````markdown
### M4 — ALM specification details

**CONFIRMED as a Major issue and the technical hook for D-01 below.** The AL-PINN method of Son, Cho & Hwang (arXiv:2205.01059) has a narrowly bounded operating regime: per the paper's own abstract, "the sequence of minimizers of the proposed loss functions converges to an actual solution for the Helmholtz, viscous Burgers, and Klein–Gordon equations" — no chaotic or stiff system appears in the paper's experimental set, and the convergence proof does not extend to chaotic ODEs. The same paper documents in §4.1 a penalty-parameter pathology: "both the total loss and the relative error rapidly converge to relatively high values as $\beta_n$ increases. This phenomenon is somewhat explained by the fact that a large value of $\beta$ causes the dominance of the boundary condition over the residual loss, which makes the training unstable." The CTL-PINN is applying a method outside its proven regime, on a chaotic system, with no published evidence of stability. This is a substantive risk, resolved under D-01.
````

_Source heading: `### D-01 — Loss-balancing methodology (FIRM recommendation)`_

````markdown
### D-01 — Loss-balancing methodology (FIRM recommendation)

**Recommendation: Replace bare ALM with the causal-training weighting of Wang, Sankaran & Perdikaris (arXiv:2203.07404) as the primary residual-loss balancer, and demote ALM to a secondary role enforcing only the small number of hard physical invariants — total energy and the three components of angular momentum.**

Justification in three parts.

First, **ALM as the sole balancer is the wrong tool for a chaotic ODE system trained from data**. The Son/Cho/Hwang AL-PINN paper, the canonical reference for ALM-PINNs, contains no chaotic-system experiment; the paper's convergence theorems are stated only for the Helmholtz, viscous Burgers, and Klein-Gordon equations (all smooth, well-posed PDEs). The same paper documents that convergence fails both when the penalty parameter $\beta$ is too small — Remark 3.6 states "a large value of $\beta$ stabilizes the augmented Lagrangian method. Since the uniform boundedness of $\{\|\lambda_n\|_{L^2(\partial\Omega)}\}$ is essential to guarantee the $\Gamma'$-convergence, a large $\beta$ stabilizes the proposed AL-PINNs as in convex optimization" — and when $\beta$ is too large, where boundary-condition gradients dominate and training becomes unstable. For a problem whose true loss landscape inherits the sensitivity-to-initial-conditions of the underlying chaotic dynamics, this is a poor foundation.

Second, **causal training has been demonstrated on exactly the class of problem at hand**. Wang et al. (arXiv:2203.07404) introduce the temporal weighting
$$w_i \;=\; \exp\!\left(-\varepsilon \sum_{k=1}^{i-1} \mathcal{L}_r(t_k, \theta)\right), \quad i = 2, \ldots, N_t,$$
and apply it specifically to the chaotic Lorenz system, the Kuramoto–Sivashinsky equation in its chaotic regime, and the Navier–Stokes equations in the turbulent regime. Per Table 1 of Wang et al. (arXiv:2203.07404), on the Lorenz system with $\sigma = 3$, $\rho = 28$, $\beta = 8/3$, initial condition $(1,1,1)$, and $T = 20$, the method achieves relative $L^2$ errors of $1.139 \times 10^{-2}$, $1.656 \times 10^{-2}$, and $7.038 \times 10^{-3}$ on the $x$, $y$, and $z$ components respectively, and on the chaotic Kuramoto–Sivashinsky benchmark a relative $L^2$ error of $2.26 \times 10^{-2}$. The authors state in §1 of that paper: "To the best of our knowledge, this is the first time that PINNs have been successful in simulating systems such as the chaotic Lorenz system, the Kuramoto–Sivashinsky equation in the chaotic regime, and the Navier–Stokes equations in the turbulent regime." This is direct primary evidence that causal weighting is appropriate for the regime the CTL-PINN inhabits; ALM has no equivalent published demonstration on chaotic systems.

Third, **the hybrid is natural and preserves the spirit of the existing spec**. The conserved scalars $E, L_x, L_y, L_z$ are exact algebraic constraints (independent of $t$) on any physically valid trajectory; for these four scalars, ALM's interpretation as a sequential max–min on Lagrange multipliers is appropriate and well-conditioned because the multiplier vector has dimension four, not thousands. By contrast, the per-collocation-point ODE residual is fundamentally a temporal-causality problem (errors at early times propagate to late times in a chaotic system), which is the regime causal training was designed for. The recommended hybrid is therefore: (i) cumulative-residual causal weighting on the ODE residual, with the annealing schedule recommended by Wang et al. — $\varepsilon \in \{10^{-2}, 10^{-1}, 10^0, 10^1, 10^2\}$ advanced via stage transitions on the criterion $\min_i w_i > \delta = 0.99$; (ii) ALM with four multipliers on the conserved-quantity penalties, with a fixed modest $\beta$ rather than an aggressive update schedule. The Wang et al. paper itself recommends $\lambda_{ic} = 10^3$ and $\delta = 0.99$ as default hyperparameters, which can be adopted as defaults pending empirical tuning.

This change does not require a wholesale architectural rewrite: the SQR-SkipResNet-SIREN body is unchanged, the curriculum stages are unchanged, and the energy/angular-momentum penalties are retained — they are simply restructured to fit the role each method handles best.
````

**Source: Gemini**

Cross-reference: See Section 7, `#### Gemini: ALM moving-average desynchronization`, for the full source block.

**Preservation notes:**
Claude 1 and Claude 2 loss sections are retained. ChatGPT Missed Issue 3 and Gemini Unflagged Gap 2 are fully preserved in Section 7 and cross-referenced here to avoid duplicate semantic pasting. See Section 12 for cross-reference and omission accounting.

### Constraint counting

**Canonical references:** M4

_Canonical source excerpt(s):_

````markdown
| M4 | MAJOR | Constraint counting error: "13 constraints for 8-D reduced phase space" — but 18 - 3(COM) - 3(P) - 3(SO(3)) = 9 DOF, not 8. | Correct to: "9 constraints reduce 18-DOF to 9 dimensions." |
````
**Report aliases:** ChatGPT: M4; Claude 1: M2; Claude 2: B-10, M1/M2/M3; Gemini: M4

**Consensus status:** VERIFIED CONSENSUS

**Consolidated reading:**
Source blocks below cover constraint-counting failures. The reports agree the current accounting is wrong, while details differ between phase-space reduction and active conserved quantities. Read ChatGPT for injectivity framing, Claude 1 for 3D-vs-2D context, Claude 2 for conserved-quantity loss, and Gemini for concise correction.

**Source: ChatGPT**

_Source heading: `### M4 — Constraint Counting and Injectivity Argument`_

````markdown
### M4 — Constraint Counting and Injectivity Argument

**Review reference:** “Confirmed Findings,” row M4.  
**Affected specs:** `ctl_instruction.md`, “Mathematical Guarantees” in Step 4.

#### Assessment: Partially confirmed

The CTL sentence claiming “13 constraints for an 8-dimensional reduced phase space” is wrong.

The review's arithmetic correction to

$$
18 - 3 - 3 - 3 = 9
$$

is the standard count for kinematic degrees of freedom after quotienting:

- Translations: $3$.
- Total momentum: $3$.
- Global rotation: $3$.

But that patch is still incomplete for the actual framework because the network currently predicts **raw Cartesian COM-frame trajectories**, not trajectories already quotiented by global rotation.

Therefore, the present “injectivity proof” in CTL is not established by merely changing $8$ to $9$.

#### Solution

Remove the current uniqueness claim and replace it with a conditional statement.

The IC descriptor is only plausibly injective **after a specified gauge choice**, including:

- COM frame.
- Zero total momentum.
- Canonical body ordering.
- Canonical rotation.

Without that gauge, the current proof sketch should be deleted rather than merely “arithmetically corrected.”

---
````

**Source: Claude 1**

_Source heading: `### M2 — Constraint counting errors`_

````markdown
### M2 — Constraint counting errors

In the 3-body, 3D problem with G = M_total = 1 in Hénon units, the conserved quantities are: E (1), L (3 components), P (3 components, can be set to 0 by frame choice). After fixing COM and zeroing P, the active independent constraints are E (1) and L (3). The review's reference to constraint-counting errors most likely conflates a planar 2D analysis (1 + 1 + 1 active constraints) with the spec's 3D requirements. **Confirming.** Recommended count: **4 independent active conservation residuals (1 energy + 3 angular momentum)**, plus the 6-DOF COM/momentum constraint as a soft regularizer until B-03/B-05 is fixed.
````

**Source: Claude 2**

_Source heading: `### B-10 — Constraint counting in 3D three-body PINN`_

````markdown
### B-10 — Constraint counting in 3D three-body PINN

**CONFIRMED. The classical Newtonian three-body system in 3D has exactly:**

- 18 phase-space DOF (3 bodies × 3 position components + 3 bodies × 3 velocity components);
- 10 classical first integrals — **3** components of center-of-mass position (uniform motion), **3** components of total linear momentum $\mathbf{P}$, **3** components of total angular momentum $\mathbf{L}$, and **1** total energy $E$, as established by Bruns (1887) who proved no further algebraic integrals exist;
- in the COM frame, the 3 COM-position and 3 linear-momentum integrals are fixed by construction to zero and become coordinate choices rather than active constraints.

The remaining active dynamical integrals are therefore the three components of $\mathbf{L}$ and the scalar $E$ — **four scalar conserved quantities**, not seven. If the framework's loss enforces "energy + 3 angular-momentum + 3 linear-momentum" terms, it is double-counting with the COM-projection layer recommended in B-05. **Recommendation:** the conserved-quantity loss should sum to exactly four scalar penalties ($E$ and $L_x, L_y, L_z$), with the COM-frame architectural projection handling the linear-momentum and COM-position integrals. Update the spec to reflect this.
````

**Source: Gemini**

_Source heading: `### M4: Constraint Counting Error`_

````markdown
### M4: Constraint Counting Error
**Context:** Documented in `ctl_instruction.md` (Section Phase 1 - Step 4: "Mathematical Guarantees").
**Analysis:** The text claims "13 constraints for 8-D reduced phase space." This is a fundamental mathematical error in identifying the degrees of freedom. A three-body system begins with 18 degrees of freedom ($3 \text{ bodies} \times 3 \text{ spatial coordinates} \times 2 \text{ for position/velocity}$). Subtracting 3 for COM position, 3 for COM momentum, and 3 for overall SO(3) rotational invariance leaves exactly 9 degrees of freedom, not 8.
**Resolution:** Correct the documentation to accurately reflect the topology: "9 constraints reduce 18-DOF to 9 dimensions."
````

**Preservation notes:**
All four source blocks are retained. Claude 2 M1/M2/M3 also appears in input dimensionality and is retained there; B-10 is the primary constraint-counting paste. See Section 12 for cross-reference and omission accounting.

### `I_3` and `I_norm` normalization

**Canonical references:** M5, D-02

_Canonical source excerpt(s):_

````markdown
| M5 | MAJOR | I_3 claimed "already in [-1,1]" but formula gives I_3 in [0,1]. | Apply `I3_norm = 2*I3 - 1` to map [0,1] → [-1,1]. |

### [ROUTINE] D-02 — I_norm: raw ratio vs tanh-wrapped

**Status:** Awaiting human approval
**Source:** issues/01-architecture-and-physics-foundations.md, "Open Decisions" section
**Conflict with current SOT:** No — both forms coexist in the SOT with distinct purposes

What the SOT says today:
- `ctl_instruction.md` Step 3 (line 443): defines `I_norm` as part of the invariants tuple computed from scaled ICs.
- `ctl_instruction.md` Step 4 normalization code (line 739): applies `I_norm = np.tanh(I_norm)` for the input vector.
- `review_of_framework.md` §2.3 table (line 223): specifies `tanh(I_trace / (M_total * r_char^2))` as the normalization formula.

What is being asked:
- Confirm that the tanh-wrapped form is canonical for the input vector, and the raw ratio serves as the intermediate physics descriptor. This is a documentation reconciliation, not a methodology change.

Options on the table:
- Option A: Adopt the tanh-wrapped form as canonical (matches review_of_framework.md §2.3 and ctl_instruction.md Step 4 normalization listing).
- Option B: Keep the raw ratio in the CTL text and add a note that the tanh wrapper is applied only for neural network input.

Why this needs YOU (the framework owner):
- Methodology impact: zero. The SOT is already internally consistent — both forms coexist with distinct purposes (raw ratio for physics descriptor, tanh-wrapped for neural network input). This is documentation cleanup to ensure the CTL text and normalization listing are reconciled in the LaTeX revision phase.

Cross-link: see [Open Decisions](#open-decisions) for full rationale.
````
**Report aliases:** ChatGPT: M5, D-02; Claude 1: No substantive coverage; M3 is characteristic-D normalization, not `I_3`/`I_norm`; Claude 2: M1/M2/M3 normalization discussion; Gemini: M5, D-02

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover I3 mapping and I_norm wrapping. The preserved split is between ChatGPT and Gemini normalization details, with Claude 1 absent and Claude 2 only broad. Read ChatGPT for expanded reasoning, Claude 2 for broad normalization context, and Gemini for concise D-02 handling.

**Source: ChatGPT**

_Source heading: `### M5 — $I_3$ Normalization`_

````markdown
### M5 — $I_3$ Normalization

**Review reference:** “Confirmed Findings,” row M5.  
**Affected specs:** `ctl_instruction.md`, “Universal Shape Invariants” and “Apply Normalization to [-1,1].”

#### Assessment: Confirmed bug; review's numeric range disputed

The CTL document says $I_3$ is already in $[-1,1]$, which is false.

But the review's claim that the formula yields

$$
I_3 \in [0,1]
$$

is also too loose.

Because the mutual distances form a triangle, the triangle inequality implies

$$
0
\le
d_{\mathrm{short}} + d_{\mathrm{mid}} - d_{\mathrm{long}}
\le
\frac{1}{3}
\left(
d_{\mathrm{short}} + d_{\mathrm{mid}} + d_{\mathrm{long}}
\right).
$$

Therefore the actual range is

$$
I_3 \in \left[0,\frac{1}{3}\right].
$$

The review's proposed repair

$$
I_3^{\mathrm{norm}} = 2I_3 - 1
$$

does **not** map the attainable range to all of $[-1,1]$.

#### Solution

If keeping the current $I_3$ definition, the minimal correct normalization is

$$
I_3^{\mathrm{norm}} = 6I_3 - 1.
$$

A better long-run design is to revisit the three shape invariants during D-01, because they are partly redundant. But

$$
I_3^{\mathrm{norm}} = 6I_3 - 1
$$

is the correct local repair.

---
````

_Source heading: `### D-02 — $I_{\mathrm{norm}}$: Raw Ratio Versus Tanh-Wrapped`_

````markdown
### D-02 — $I_{\mathrm{norm}}$: Raw Ratio Versus Tanh-Wrapped

I recommend approving the **tanh-wrapped form as the canonical network input** and keeping the raw ratio only as an intermediate physics descriptor:

$$
I_{\mathrm{norm}}^{\mathrm{raw}}
=
\frac{
\operatorname{tr}(I)
}{
M_{\mathrm{tot}} r_{\mathrm{char}}^2
},
$$

$$
I_{\mathrm{norm}}^{\mathrm{in}}
=
\tanh
\left(
I_{\mathrm{norm}}^{\mathrm{raw}}
\right).
$$

This reconciles the CTL text with the normalization code path and preserves the stated “all IC components into $[-1,1]$” contract.

This is a documentation decision, not a methodological one.

---
````

**Source: Claude 1**

No substantive coverage. Claude 1 M3 is about characteristic-D normalization, not I3/I_norm.

**Source: Claude 2**

Cross-reference: See `### Input vector dimensionality and 3D-vs-planar encoding` for Claude 2 `M1, M2, M3`, which includes broad normalization-bug discussion.

**Source: Gemini**

_Source heading: `### M5: $I_3$ Normalization Mapping`_

````markdown
### M5: $I_3$ Normalization Mapping
**Context:** Outlined in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The document claims that the third shape invariant $I_3$ is "already in [-1,1]". However, the underlying formula dictates $I_i / I_{\max}$, which strictly places the value within the positive domain of $[0,1]$. Passing an asymmetric positive domain into a layer optimized for zero-centered inputs destabilizes the initial SIREN activations.
**Resolution:** Apply the normalization mapping `I3_norm = 2*I3 - 1` to strictly enforce the `[-1,1]` boundary constraint.
````

_Source heading: `### D-02: $I_{\text{norm}}$ Definition`_

````markdown
### D-02: $I_{\text{norm}}$ Definition
**Recommendation: Adopt the `tanh` wrapper globally for network inputs.**

The CTL text defines $I_{\text{norm}}$ as a raw ratio, while the code wraps it in `tanh`. Because the moment of inertia traces can spike during highly expansive trajectories (especially for marginally bound systems in Stage 6), feeding raw unbounded values into a SIREN network will force the pre-activations far out of their standard normal distribution, severely hampering the network's spectral learning capabilities. Wrapping the ratio in `tanh` perfectly maps the domain to $[-1, 1]$, satisfying the input contract required by the $\omega_0=30$ initialization [cite: 1, 3]. The CTL text must be updated to match the code perfectly.
````

**Preservation notes:**
ChatGPT and Gemini M5/D-02 blocks are retained. Claude 1 M3 is not reused because it concerns characteristic-D normalization. Claude 2 M1/M2/M3 is cross-referenced from input dimensionality. See Section 12 for cross-reference and omission accounting.

### LayerNorm attribution and affine setting

**Canonical references:** M8, D2, D3

_Canonical source excerpt(s):_

````markdown
| M8 | MAJOR | LayerNorm on skip path attributed to SQR-SkipResNet paper, but the original paper (arXiv:2310.15690v2) has NO LayerNorm anywhere. | Re-attribute as author modification. |
| D2 | MINOR | Does LayerNorm on skip path actually help? | Ablate: train with/without skip-path LayerNorm. |
| D3 | MINOR | LayerNorm affine=True or affine=False? | Default `affine=False` (safer). LayerNorm's purpose is normalization, not feature transformation. |

## LayerNorm Analysis

**Why LayerNorm on skip connections?** The physics residual involves 1/r³ terms. During close encounters (r → 0), gradient magnitudes spike by 3-4 orders of magnitude. These spikes propagate through skip connections — without normalization, the power term (element-wise square) amplifies already-large activations. LayerNorm normalizes the skip-path activations to zero mean and unit variance before the power operation, capping the maximum skip-contribution magnitude.

**affine=True vs affine=False (D3):** `affine=True` adds learnable scale (γ) and shift (β) parameters after normalization. For SIREN layers, which are carefully tuned for specific frequency spectra, learnable affine transforms on the skip path could interfere with the frequency-spreading design. **Default recommendation:** `affine=False` is safer. Ablate to confirm.

**Empirical ablation protocol (D2):**
1. Train a Stage 0 model with affine=True (baseline) and affine=False (comparison)
2. Monitor: max gradient norm per layer, activation histogram spread, training loss trajectory
3. Expected: if affine=True adds value, loss should converge faster; if not, both should reach similar final loss
4. If no benefit from affine=True, remove it to reduce parameter count and simplify the architecture

---
````
**Report aliases:** ChatGPT: M8; Claude 1: No direct coverage; Claude 2: No substantive coverage; M8/M9/M10 is a broad remaining-majors sweep; Gemini: M8, D2/D3

**Consensus status:** VERIFIED MAJORITY

**Consolidated reading:**
Source blocks below cover LayerNorm attribution and affine-setting uncertainty. ChatGPT and Gemini are the substantive sources. Claude 1 is absent, and Claude 2's broad remaining-major block is preserved separately rather than raw-merged into this LayerNorm issue.

**Source: ChatGPT**

_Source heading: `### M8 — LayerNorm Attribution`_

````markdown
### M8 — LayerNorm Attribution

**Review reference:** “Confirmed Findings,” row M8.  
**Affected specs:** `pinn_architecture.md`, “The Power-Enhanced SkipResNet Formulation” and summary table.

#### Assessment: Confirmed

LayerNorm on the skip path is not part of the original Power-Enhanced SkipResNet paper. The current architecture may still be valid, but the attribution is wrong.

This is a **citation-and-design provenance** issue, not evidence that the LayerNorm variant is invalid.

#### Solution

Relabel LayerNorm as a **project-specific stabilization modification**.

If keeping it, the safer first-ablation default is:

```text
elementwise_affine = False
```

LayerNorm should be tested through ablation after the hard physics contracts are repaired.

---
````

**Source: Claude 1**

No direct coverage.

**Source: Claude 2**

No substantive coverage. See Section 9 for preserved broad M8/M9/M10 source-only block.

**Source: Gemini**

_Source heading: `### M8: LayerNorm Attribution`_

````markdown
### M8: LayerNorm Attribution
**Context:** Described in `pinn_architecture.md` (Section 2.3 "The Power-Enhanced SkipResNet...").
**Analysis:** The documentation attributes the application of LayerNorm on the skip path to the original SQR-SkipResNet paper. However, a review of the foundational SQR-SkipResNet literature confirms that the original architecture contains no such LayerNorm application.
**Resolution:** Re-attribute this explicitly as a custom author modification designed to bound the quadratic power term during extreme gradient spikes common in close encounters.
````

**Preservation notes:**
ChatGPT and Gemini M8 blocks are retained. Claude 2 M8/M9/M10 is preserved in Section 9 as source-only material, not used as LayerNorm evidence. See Section 12 for cross-reference and omission accounting.

### `E_norm` and mass normalization ranges

**Canonical references:** M9, M10

_Canonical source excerpt(s):_

````markdown
| M9 | MAJOR | E_norm only uses [-1, 0) — positive input range never used since E < 0 for bound systems. | Acceptable for SIREN. Document that positive range is unused. |
| M10 | MAJOR | m_norm range asymmetric for hierarchical masses: [-0.93, 0.585], not centered on 0. | Acceptable — asymmetry carries mass hierarchy information. |
````
**Report aliases:** ChatGPT: M9/M10; Claude 1: No substantive coverage; M10 is curriculum-threshold related, not same semantic issue; Claude 2: No substantive coverage; M8/M9/M10 is a broad remaining-majors sweep; Gemini: M9, M10

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover E_norm range and asymmetric mass normalization. ChatGPT and Gemini agree these are documentation or acceptable-behavior issues, but the reports differ in framing. Claude 1 and Claude 2 same-number labels are explicitly not reused for this semantic issue.

**Source: ChatGPT**

_Source heading: `### M9 and M10 — $E_{\mathrm{norm}}$ Range and Asymmetric Mass Normalization`_

````markdown
### M9 and M10 — $E_{\mathrm{norm}}$ Range and Asymmetric Mass Normalization

**Review reference:** “Confirmed Findings,” rows M9 and M10.  
**Affected specs:** `ctl_instruction.md`, “Apply Normalization to [-1,1]”; `pinn_architecture.md`, summary table.

#### Assessment: Mostly disputed as bugs

The fact that

$$
E^{\mathrm{norm}}
=
\tanh\left(\frac{E}{E_{\mathrm{scale}}}\right)
$$

may occupy mostly the negative half-line if the dataset is mostly bound is not a correctness problem. It is simply a statement about the data manifold.

It is also not clear from the supplied files that all trajectories are guaranteed bound.

Likewise, the asymmetric range of normalized mass fractions is not a defect. It is an expected consequence of an asymmetric mass-ratio distribution and carries useful hierarchy information.

#### Solution

Demote both to documentation cleanup.

Add one sentence:

> The realized support of a normalized feature need not fill all of $[-1,1]$; asymmetry in $m_i^{\mathrm{norm}}$ is expected when the training distribution over mass ratios is asymmetric.

---
````

**Source: Claude 1**

No substantive coverage. Claude 1 M10 is curriculum-threshold motivation, not E_norm or mass-range normalization.

**Source: Claude 2**

No substantive coverage. See Section 9 for preserved broad M8/M9/M10 source-only block.

**Source: Gemini**

_Source heading: `### M9: $E_{\text{norm}}$ Range Unused`_

````markdown
### M9: $E_{\text{norm}}$ Range Unused
**Context:** Documented in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The normalization formula relies on `tanh(E / E_scale)`. Because all bound systems inherently have $E < 0$, the resulting mapping exclusively occupies the domain `[-1, 0)`. The positive input range is mathematically never utilized by the network.
**Resolution:** This asymmetric saturation is acceptable for SIREN networks provided the architecture is explicitly aware of it. Document clearly that the positive range is unused and verify that this lack of symmetry does not bias the first-layer spectral density.
````

_Source heading: `### M10: $m_{\text{norm}}$ Range Asymmetry`_

````markdown
### M10: $m_{\text{norm}}$ Range Asymmetry
**Context:** Outlined in `ctl_instruction.md` (Section Phase 1 - Step 4: "Apply Normalization").
**Analysis:** The mass normalization formula consistently yields values spanning roughly `[-0.93, 0.585]` for hierarchical mass distributions, failing to center perfectly on zero. 
**Resolution:** This is physically accurate and mathematically acceptable. The asymmetry inherently encodes the explicit mass hierarchy information, allowing the network to distinguish primary, secondary, and tertiary bodies without requiring an artificial zero-centered shift.
````

**Preservation notes:**
ChatGPT M9/M10 and Gemini M9/M10 are retained. Claude 1 M10 and Claude 2 M8/M9/M10 are preserved in Section 9 as source-only blocks, not merged into this row. See Section 12 for cross-reference and omission accounting.

### Minor issue triage D1-D10

**Canonical references:** D1-D10

_Canonical source excerpt(s):_

````markdown
| D1 | MINOR | What exactly are the 3 angles for trigonometric encoding? | Proposed: (theta_L, phi_L) = spherical coords of L_hat; gamma_orb = orbital phase. |
| D2 | MINOR | Does LayerNorm on skip path actually help? | Ablate: train with/without skip-path LayerNorm. |
| D3 | MINOR | LayerNorm affine=True or affine=False? | Default `affine=False` (safer). LayerNorm's purpose is normalization, not feature transformation. |
| D4 | MINOR | Should quasi-random IC Brutus outputs get COM-corrected? | Experiment: parse 100 trajectories. If COM drift > 1e-12, apply correction. |
| D6 | MINOR | How to handle Brutus mass drift between snapshots? | Compare m_IC vs m_Brutus_t=0 with np.allclose(rtol=1e-15). |
| D8 | MINOR | Should s_min use softening for Stage 6 collision criterion? | Canonical split lives in `03-curriculum-and-training-loop.md`: use unsoftened `s_min` for curriculum stage gates and diagnostics; use `max(s_min, epsilon_soft)` only inside training-loss collision criteria. |
| D9 | MINOR | Is the orientation representational gap fatal? | The recommended direction-cosines encoding addresses this if Option B is accepted. Verify with small MLP: if MSE < 1e-4, sufficient. |
| D10 | MINOR | Can training start with standard SIREN init while D formula is being fixed? | Yes partially. Use D=6.694 from day one to avoid retraining. Priority P0. |
````
**Report aliases:** ChatGPT: Minor Issues Triage; Claude 1: Minor Issues Triage; Claude 2: Minor-Issue Triage; Gemini: Minor Issues Triage

**Consensus status:** VERIFIED SPLIT

**Consolidated reading:**
Source blocks below cover minor triage. The reports do not flatten to one minor table because they elevate different items under different evidence limits. Read each source block as report-local triage rather than a raw D-label consensus.

**Source: ChatGPT**

_Source heading: `## 5. Minor Issues Triage`_

````markdown
## 5. Minor Issues Triage

Most of the review's minor issues can remain minor **after** the core physics contract is repaired.

- D1 is documentation only.
- D2 and D3 should remain ablations, not preconditions.
- D4 and D6 are good engineering checks but not architectural blockers once a unified COM/mass-consistency transformer is in place.
- D8 is minor if the stage-gating metric is explicitly documented as unsoftened geometry rather than softened training physics.
- D10 is minor once the SIREN initialization contract is frozen.

The exception is **D9**. I would elevate D9 from minor to **blocking**, because the representational gap is not hypothetical: the review's preferred Option B does not provide enough information for raw Cartesian COM-frame prediction.

If the owner accepts the canonical-rotation recommendation above, D9 drops back down. Otherwise it should be treated as a first-tier blocker.

---
````

**Source: Claude 1**

_Source heading: `## 5. Minor Issues — Triage`_

````markdown
## 5. Minor Issues — Triage

**Recommendation: do not elevate any of D1–D4, D6, D8–D10** unless they intersect a blocker. The likely candidates — naming conventions, plot styles, log-file formats — are pure cleanup and should be batched into a single documentation-cleanup PR after P0/P1 fixes land. **One exception**: if D6 concerns the choice of optimizer (Adam → L-BFGS handoff), the L-BFGS phase is known to be highly sensitive to gradient noise; ensure L-BFGS is launched only after Adam has converged the data-loss to within an order of magnitude of the residual loss (a standard heuristic from the Raissi/Karniadakis 2019 PINN paper).

---
````

**Source: Claude 2**

_Source heading: `## 4. Minor-Issue Triage`_

````markdown
## 4. Minor-Issue Triage

Without the verbatim minor-issue text, the triage below is based on the issue-label semantics described in the project context. **None of the eight Minor items (D1, D2, D3, D4, D6, D8, D9, D10) appears to require elevation to MAJOR**, on the following rationale.

D1 through D4 and D6 read as design-ambiguity items — likely concerning curriculum-stage transition thresholds (Lyapunov-time stratification cutoffs, virial-ratio bin edges, stage-success criteria), the Adam-to-L-BFGS handover heuristic, and similar tuning surface. These are properly empirical questions whose answers depend on training runs and should not be locked by the spec; defer to a "Hyperparameter Card" appendix once P0 fixes are in. The virial ratio $Q = -T/V$ is a defensible stratification variable — the virial theorem $2T + V = 0$ at equilibrium makes $Q = 0.5$ a natural reference and $|Q - 0.5|$ a natural disequilibrium proxy — but the precise bin edges are empirical.

D8 through D10 read as documentation gaps (missing citation for the virial-ratio choice, ambiguity in Brutus integrator settings, etc.). These should be folded into the D-02 cleanup pass — they cost nothing to fix and reduce future ambiguity for reviewers, but they do not block training.

The one Minor item that deserves a watching brief is whichever item concerns Lyapunov-time stratification thresholds for the curriculum (M10 if Major, or one of D1/D6 if Minor). The literature on curriculum learning for chaotic systems (notably the "Curriculum-Driven Training for Robust Forecasting of Chaotic Dynamics" approach, arXiv:2510.04342, which stratifies a 50-system ODE/PDE library by largest Lyapunov exponent and attractor dimension) supports stratifying by Lyapunov-exponent quantile but does not give universal threshold values. **If during Stage 0→1 training the transition shows hysteresis or the stage-success rate falls below approximately 50%, this Minor item should be re-elevated to MAJOR and bin edges recalibrated empirically.**
````

**Source: Gemini**

_Source heading: `## 4. Minor Issues Triage`_

````markdown
## 4. Minor Issues Triage

The minor issues identified in the audit require the following explicit triage treatments to ensure no hidden blockers emerge during late-stage training:

*   **D1 (What exactly are the 3 angles for trigonometric encoding?):** *Defer / Resolved.* Because Option B (Shape Invariants + Direction Cosines) has been strongly recommended and selected over Option A, defining the exact trigonometric angles is rendered obsolete. 
*   **D2 & D3 (LayerNorm affine parameters):** *Confirm Ablation.* The SQR-SkipResNet literature does not mandate LayerNorm. Adding it stabilizes the power-term amplifications during close encounters, but setting `affine=True` allows the network to learn a scale ($\gamma$) and shift ($\beta$). In a SIREN architecture, learnable affine transformations *before* the sine activation can overwrite the carefully controlled frequency spectrum. Set `affine=False` as the default until ablation proves otherwise.
*   **D4 (COM for Brutus outputs):** *Elevate to MAJOR.* The Brutus outputs must absolutely be checked and corrected for COM drift. High-precision integrators can accumulate round-off errors over thousands of time steps, leading to a slow drift of the system's barycenter. If the PINN's data loss ($\mathcal{L}_{\text{data}}$) trains on drifting targets, it will attempt to model numerical error as physical forces. Apply the Galilean boost to Brutus data automatically.
*   **D6 (Mass drift in Brutus):** *Defer.* Mass is a constant parameter in Brutus. A simple `np.allclose()` assertion at data loading is sufficient.
*   **D8 (Stage 6 Collision Softening):** *Confirm.* Use raw, unsoftened $s_{\min}$ for stage logic to ensure rigorous ground-truth classification. Use $\max(s_{\min}, \epsilon_{\text{soft}})$ exclusively inside the network's loss functions.
*   **D9 (Is the orientation representational gap fatal?):** *Defer / Resolved.* The audit noted potential issues with replacing trigonometric angles. The recommended Option B utilizing direction cosines cleanly and fully closes this representational gap, rendering the concern resolved.
*   **D10 (Can training start with standard SIREN init while D formula is being fixed?):** *Elevate to Priority P0.* Yes. Training can and should commence with the corrected $D=6.694$ value immediately from day one to avoid costly, mandatory retraining later.
````

**Preservation notes:**
All four minor-triage sections are retained verbatim. Differences in D-label interpretation are preserved in Section 8. See Section 12 for cross-reference and omission accounting.

### Unflagged gaps and unique risks

**Canonical references:** Gap registry

No canonical heading found; issue inferred from report aliases.

**Report aliases:** ChatGPT: Missed Issues 1-3; Claude 1: What Was NOT Flagged; Claude 2: What Was Not Flagged; Gemini: Unflagged Gaps 1-2

**Consensus status:** UNIQUE

**Consolidated reading:**
Source blocks below preserve each report's unique risks. These are not forced into consensus because each report contributes different uncovered gaps. Read ChatGPT for three missed issues, Claude 1 for six risk bullets, Claude 2 for chaotic-training risks, and Gemini for mass-scaling and ALM desynchronization.

**Source: ChatGPT**

_Source heading: `## 7. What Was Not Flagged`_

````markdown
## 7. What Was Not Flagged
````

**Source: Claude 1**

_Source heading: `## 7. What Was NOT Flagged (Gaps the Review Missed)`_

````markdown
## 7. What Was NOT Flagged (Gaps the Review Missed)

This auditor flags the following as worth adding to the issue list:

1. **L-BFGS sensitivity to ALM dual updates.** The Adam → L-BFGS handoff specified in CTL Instruction is mathematically fragile when ALM is updating λ multipliers between iterations: L-BFGS builds a quasi-Newton approximation of the Hessian assuming a stationary objective, but ALM's λ updates change the objective. Standard remedy: freeze λ during L-BFGS phase, only update between phases.
2. **SIREN's spectral bottleneck.** Chandravamsi, Shenoy, Zinn, Pisnoy & Frankel (Technion), "Spectral Bottleneck in Sinusoidal Representation Networks: Noise is All You Need," arXiv:2509.09719 (2025), and its companion "WINNER" initialization paper (Chandravamsi, Shenoy & Frankel, arXiv:2509.12980, 2025), show SIREN can suffer "spectral bottleneck" when target frequency support is misaligned with ω₀. For three-body dynamics, characteristic frequencies vary by 3+ orders of magnitude between Stage-0 (Keplerian) and Stage-6 (close encounters). A single ω₀ = 30 will be wrong for one end of the curriculum. **Recommendation: re-tune ω₀ per stage** (or use the FINER / WINNER initialization which broadens frequency support).
3. **Brutus precision contract.** The CTL Instruction presumably trusts Brutus output as "ground truth." Boekholt & Portegies Zwart (2015, arXiv:1411.6671) and Boekholt et al. (2020, *MNRAS* 493, 3932) emphasize that *individual* Brutus trajectories beyond ~3.5 Lyapunov times are themselves chaotic-divergent and only their *ensemble statistics* are physically meaningful. The framework should not be trained on long single trajectories beyond ~5 Lyapunov times; train on ensembles of short trajectories instead, then validate on ensemble distributional metrics (à la Portegies Zwart & Boekholt 2018).
4. **No mention of permutation symmetry.** The three-body problem is invariant under particle re-labeling. The Breen et al. (2020, *MNRAS* 494, 2465) reduction (fixing particle 1, semicircle for particle 2) implicitly breaks this; a full 3D framework that doesn't either canonicalize ordering or use a permutation-invariant network is wasting ~6× capacity. **Recommendation: sort bodies by some canonical invariant** (e.g. distance from initial COM) and apply the same sorting in residuals.
5. **No discussion of train/test distributional shift across curriculum stages.** When Stage k→k+1 widens the IC distribution, transfer learning typically benefits from a *replay buffer* of old-stage data to prevent catastrophic forgetting. The CTL framework should include a replay-buffer specification.
6. **Inconsistency between "3D not planar" guardrail and Breen et al. inheritance.** The spec inherits Breen et al.'s methodology, but Breen et al. is planar (per their §2: bodies in the unit semicircle of the negative x-axis with zero initial velocity). If the spec ever cites Breen's "10,000 simulations from semicircle" but uses 3D, the methodology has been silently extended without justification — a methodology disclosure gap.

---
````

**Source: Claude 2**

_Source heading: `## 6. What Was Not Flagged`_

````markdown
## 6. What Was Not Flagged

Three categories of latent risk do not appear in the issue list described.

First, **single-network-output for a chaotic system is a representational ceiling**. The most successful published chaotic-three-body machine-learning effort (Santos Pereira et al., arXiv:2503.04585, "Advancing Solutions for the Three-Body Problem Through Physics-Informed Neural Networks") explicitly restricts training to "systems with three unitary masses and initial velocity equal to zero, corresponding to a restricted form of the problem," following the planar restriction of Breen et al. (MNRAS 494, 2020). A single SIREN body asked to predict full-3D, general-mass three-body trajectories across multiple Lyapunov times will face a representational ceiling unrelated to any of the issues in the audit. The curriculum (Stage 0→6) is the right structural mitigation, but the spec should record an explicit "valid prediction horizon" target (for example, three to five Lyapunov times) and a stopping criterion if Stage 4+ fails to converge after a budgeted number of epochs.

Second, **Santos Pereira et al. provide a primary-source warning that the data-loss minima and the physics-loss minima are *adversarial* in this problem, not aligned**. Their paper reports that low values of the physics-loss coefficient (around $\alpha \approx 0.001$) gave good early-epoch performance, that the benefit saturated by 100 epochs, and that higher coefficients made early-epoch training significantly volatile but benefited later stages; their attempted gradual ramp from $\alpha_0$ to $\alpha_{\max}$ caused training to degenerate despite the gradual introduction. They conclude that the standard data-MAE minima are "incompatible" with the physics-informed minima. The CTL-PINN curriculum implicitly assumes the two are aligned (the network learns data first, then physics tightens the prediction). The framework should plan for the contingency that adding the physics term in late stages destabilizes a converged data-loss solution; the causal-weighting recommendation under D-01 mitigates this, but the spec should additionally require an explicit physics-loss warmup with the residual coefficient ramped from zero over several thousand iterations, mirroring the Santos Pereira et al. empirical finding.

Third, **the framework does not specify a numerical-precision contract on the training data**. Brutus is an arbitrary-precision integrator whose primary value is producing converged solutions whose digit-accuracy is itself a tunable parameter (Boekholt & Portegies Zwart 2015 use a Bulirsch-Stoer convergence parameter $p$, with $p = 3$ as the standard production setting and $p = 15$ reserved for high-precision benchmarking). If training data are generated at $p = 3$, the training labels themselves diverge exponentially from any "true" trajectory on a timescale set by the Lyapunov exponent, and the PINN cannot learn a more accurate mapping than its labels permit. The spec should record (i) the Brutus convergence parameter $p$ used to generate training data, (ii) the resulting maximum trustworthy prediction horizon, and (iii) a Stage 4+ data-regeneration step with higher $p$ for the chaotic-regime stages. This is the kind of issue that, if discovered after 50 GPU-hours of training, would invalidate the run.

Finally, an inconsistency between the two specs worth verifying directly: CTL Instruction states the data are "fully 3D (not planar)" while a substantial fraction of the published three-body ML literature (Breen et al., Santos Pereira et al.) trains on planar restrictions. If the SIREN width of 256 was originally chosen with planar-data papers in mind, 12 hidden layers × 256 neurons may be undersized for general 3D three-body chaos. This is not yet a confirmed issue — it is a quantity to measure at Stage 2 of the curriculum — but the spec should record it as an empirical open question with a measurable trigger (for example, "if Stage 2 validation MSE plateaus above $10^{-3}$ on COM-frame positions for more than 20 000 iterations, width should be doubled before further stage advancement").
````

**Source: Gemini**

_Source heading: `## 6. What Was NOT Flagged (Critical Uncovered Gaps)`_

````markdown
## 6. What Was NOT Flagged (Critical Uncovered Gaps)

Diligent mathematical review of the interactions between the documents reveals two severe gaps that the previous audits completely missed.
````

**Preservation notes:**
All What Was Not Flagged blocks are retained verbatim here and split into source-labeled subsections in Section 7. Claude 2 width undersizing is included to prevent the Task 8 list from dropping it. See Section 12 for cross-reference and omission accounting.

## 7. Unflagged Gaps and Unique Risks
This section splits each report's unflagged-gap material into source-labeled entries. Resolution text remains the source report's recommendation, not a new recommendation from the consolidation.

#### ChatGPT: Force–energy incompatibility under softening

_Source: ChatGPT; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md:1058`_

````markdown
### Missed Issue 1 — Force–Energy Incompatibility Under Softening

The review flagged the epsilon mismatch but did not notice that the current softened force law and softened potential in `pinn_architecture.md` are not derivatives of one another.

This should be treated as a **new blocking issue**, because it breaks the internal contract between

$$
\mathcal{L}_{\mathrm{physics}}
$$

and

$$
\mathcal{L}_{\mathrm{energy}}.
$$

---
````

#### ChatGPT: D-01 alternatives mathematically incomplete

_Source: ChatGPT; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md:1076`_

````markdown
### Missed Issue 2 — D-01 Alternatives Are Mathematically Incomplete

The review's own D-01 alternatives are incomplete:

- Option A uses only $\sin\gamma_{\mathrm{orb}}$, which is not injective in orbital phase.
- Option B loses an orientation degree of freedom.
- M5 understates the $I_3$ range problem by treating

  $$
  I_3 \in [0,1]
  $$

  instead of the tighter range

  $$
  I_3 \in \left[0,\frac{1}{3}\right].
  $$

These are not stylistic problems. They materially affect whether the proposed IC vector can uniquely condition the network.

---
````

#### ChatGPT: Current scalar ALM rule is not a standard ALM

_Source: ChatGPT; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md:1098`_

````markdown
### Missed Issue 3 — The “ALM” Formulation Is Not a Standard Augmented Lagrangian

The supplied architecture defines

$$
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{data}}
+
\lambda_p \mathcal{L}_{\mathrm{physics}}
+
\frac{\mu_p}{2}
\mathcal{L}_{\mathrm{physics}}^2
+
\lambda_E
\mathcal{L}_{\mathrm{energy}},
$$

where $\mathcal{L}_{\mathrm{physics}}$ is already an MSE of residuals.

That makes the quadratic AL term effectively a **quartic penalty in the raw residual norm**.

A standard augmented Lagrangian would apply multipliers and quadratic penalties to the raw constraint, not to an already-squared scalar loss. Therefore the framework should either:

1. Reformulate this as a true ALM on pointwise residual constraints, or
2. Stop calling the current scalar rule “ALM” and treat it as an adaptive penalty heuristic.

The PINN optimization literature documents serious loss-balancing pathologies, which is why methods such as NTK weighting, GradNorm, and self-adaptive weighting exist. So the current ALM-like scalar rule should be treated as an empirical heuristic unless rewritten.
````

#### Claude 1: L-BFGS sensitivity to ALM dual updates

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:298`_

````markdown
1. **L-BFGS sensitivity to ALM dual updates.** The Adam → L-BFGS handoff specified in CTL Instruction is mathematically fragile when ALM is updating λ multipliers between iterations: L-BFGS builds a quasi-Newton approximation of the Hessian assuming a stationary objective, but ALM's λ updates change the objective. Standard remedy: freeze λ during L-BFGS phase, only update between phases.
````

#### Claude 1: SIREN spectral bottleneck

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:299`_

````markdown
2. **SIREN's spectral bottleneck.** Chandravamsi, Shenoy, Zinn, Pisnoy & Frankel (Technion), "Spectral Bottleneck in Sinusoidal Representation Networks: Noise is All You Need," arXiv:2509.09719 (2025), and its companion "WINNER" initialization paper (Chandravamsi, Shenoy & Frankel, arXiv:2509.12980, 2025), show SIREN can suffer "spectral bottleneck" when target frequency support is misaligned with ω₀. For three-body dynamics, characteristic frequencies vary by 3+ orders of magnitude between Stage-0 (Keplerian) and Stage-6 (close encounters). A single ω₀ = 30 will be wrong for one end of the curriculum. **Recommendation: re-tune ω₀ per stage** (or use the FINER / WINNER initialization which broadens frequency support).
````

#### Claude 1: Brutus precision contract

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:300`_

````markdown
3. **Brutus precision contract.** The CTL Instruction presumably trusts Brutus output as "ground truth." Boekholt & Portegies Zwart (2015, arXiv:1411.6671) and Boekholt et al. (2020, *MNRAS* 493, 3932) emphasize that *individual* Brutus trajectories beyond ~3.5 Lyapunov times are themselves chaotic-divergent and only their *ensemble statistics* are physically meaningful. The framework should not be trained on long single trajectories beyond ~5 Lyapunov times; train on ensembles of short trajectories instead, then validate on ensemble distributional metrics (à la Portegies Zwart & Boekholt 2018).
````

#### Claude 1: Permutation symmetry waste

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:301`_

````markdown
4. **No mention of permutation symmetry.** The three-body problem is invariant under particle re-labeling. The Breen et al. (2020, *MNRAS* 494, 2465) reduction (fixing particle 1, semicircle for particle 2) implicitly breaks this; a full 3D framework that doesn't either canonicalize ordering or use a permutation-invariant network is wasting ~6× capacity. **Recommendation: sort bodies by some canonical invariant** (e.g. distance from initial COM) and apply the same sorting in residuals.
````

#### Claude 1: Curriculum distributional shift / replay buffer gap

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:302`_

````markdown
5. **No discussion of train/test distributional shift across curriculum stages.** When Stage k→k+1 widens the IC distribution, transfer learning typically benefits from a *replay buffer* of old-stage data to prevent catastrophic forgetting. The CTL framework should include a replay-buffer specification.
````

#### Claude 1: 3D-vs-planar methodology disclosure gap

_Source: Claude 1; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report.md:303`_

````markdown
6. **Inconsistency between "3D not planar" guardrail and Breen et al. inheritance.** The spec inherits Breen et al.'s methodology, but Breen et al. is planar (per their §2: bodies in the unit semicircle of the negative x-axis with zero initial velocity). If the spec ever cites Breen's "10,000 simulations from semicircle" but uses 3D, the methodology has been silently extended without justification — a methodology disclosure gap.
````

#### Claude 2: Single-network representational ceiling

_Source: Claude 2; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md:188`_

````markdown
First, **single-network-output for a chaotic system is a representational ceiling**. The most successful published chaotic-three-body machine-learning effort (Santos Pereira et al., arXiv:2503.04585, "Advancing Solutions for the Three-Body Problem Through Physics-Informed Neural Networks") explicitly restricts training to "systems with three unitary masses and initial velocity equal to zero, corresponding to a restricted form of the problem," following the planar restriction of Breen et al. (MNRAS 494, 2020). A single SIREN body asked to predict full-3D, general-mass three-body trajectories across multiple Lyapunov times will face a representational ceiling unrelated to any of the issues in the audit. The curriculum (Stage 0→6) is the right structural mitigation, but the spec should record an explicit "valid prediction horizon" target (for example, three to five Lyapunov times) and a stopping criterion if Stage 4+ fails to converge after a budgeted number of epochs.
````

#### Claude 2: Adversarial data-loss vs physics-loss minima

_Source: Claude 2; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md:190`_

````markdown
Second, **Santos Pereira et al. provide a primary-source warning that the data-loss minima and the physics-loss minima are *adversarial* in this problem, not aligned**. Their paper reports that low values of the physics-loss coefficient (around $\alpha \approx 0.001$) gave good early-epoch performance, that the benefit saturated by 100 epochs, and that higher coefficients made early-epoch training significantly volatile but benefited later stages; their attempted gradual ramp from $\alpha_0$ to $\alpha_{\max}$ caused training to degenerate despite the gradual introduction. They conclude that the standard data-MAE minima are "incompatible" with the physics-informed minima. The CTL-PINN curriculum implicitly assumes the two are aligned (the network learns data first, then physics tightens the prediction). The framework should plan for the contingency that adding the physics term in late stages destabilizes a converged data-loss solution; the causal-weighting recommendation under D-01 mitigates this, but the spec should additionally require an explicit physics-loss warmup with the residual coefficient ramped from zero over several thousand iterations, mirroring the Santos Pereira et al. empirical finding.
````

#### Claude 2: Brutus precision contract unspecified

_Source: Claude 2; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md:192`_

````markdown
Third, **the framework does not specify a numerical-precision contract on the training data**. Brutus is an arbitrary-precision integrator whose primary value is producing converged solutions whose digit-accuracy is itself a tunable parameter (Boekholt & Portegies Zwart 2015 use a Bulirsch-Stoer convergence parameter $p$, with $p = 3$ as the standard production setting and $p = 15$ reserved for high-precision benchmarking). If training data are generated at $p = 3$, the training labels themselves diverge exponentially from any "true" trajectory on a timescale set by the Lyapunov exponent, and the PINN cannot learn a more accurate mapping than its labels permit. The spec should record (i) the Brutus convergence parameter $p$ used to generate training data, (ii) the resulting maximum trustworthy prediction horizon, and (iii) a Stage 4+ data-regeneration step with higher $p$ for the chaotic-regime stages. This is the kind of issue that, if discovered after 50 GPU-hours of training, would invalidate the run.
````

#### Claude 2: General-3D width undersizing open question

_Source: Claude 2; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/claude_research_report_2.md:194`_

````markdown
Finally, an inconsistency between the two specs worth verifying directly: CTL Instruction states the data are "fully 3D (not planar)" while a substantial fraction of the published three-body ML literature (Breen et al., Santos Pereira et al.) trains on planar restrictions. If the SIREN width of 256 was originally chosen with planar-data papers in mind, 12 hidden layers × 256 neurons may be undersized for general 3D three-body chaos. This is not yet a confirmed issue — it is a quantity to measure at Stage 2 of the curriculum — but the spec should record it as an empirical open question with a measurable trigger (for example, "if Stage 2 validation MSE plateaus above $10^{-3}$ on COM-frame positions for more than 20 000 iterations, width should be doubled before further stage advancement").
````

#### Gemini: Source list and framing

_Source: Gemini; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md:1`_

````markdown
# Comprehensive Analysis and Resolution Report: CTL-PINN Framework for the Three-Body Problem

**Disclaimer:** This document is for informational purposes only and does not constitute professional, financial, engineering, or safety-critical advice. The implementation of complex neural network architectures for chaotic dynamical systems carries inherent computational and theoretical risks.

**Key Points:**
- **Readiness Assessment:** The framework is currently **not ready for implementation**. Fundamental mathematical discrepancies block execution.
- **Critical Interventions:** The characteristic length ($D$) scaling and the Automatic Differentiation (AD) chain-rule applications contain systemic mathematical errors that will prevent the Physics-Informed Neural Network (PINN) from learning valid dynamics.
- **Architectural Corrections:** SIREN weight initialization and dynamic $\omega_0$ scheduling are incorrectly specified in the documentation and must be aligned with established literature. 
- **Input Vector Finalization:** Option B (Shape Invariants + Direction Cosines) is strongly recommended over trigonometric encodings to avoid gimbal lock during chaotic scattering.

The Curriculum-Trained Physics-Informed Neural Network (CTL-PINN) framework for the three-body problem presents a highly sophisticated, synergistic approach to modeling chaotic dynamics. By fusing a Sinusoidal Representation Network (SIREN) with a Power-Enhanced SkipResNet (SQR-SkipResNet) and an Augmented Lagrangian Method (ALM) for physics constraints, the architecture is theoretically well-equipped to handle the non-linear, multi-scale nature of gravitational interactions. However, the foundational specifications currently contain severe mathematical and geometric misalignments. 

This report provides an exhaustive issue-by-issue analysis of the consolidated "Architecture & Physics Foundations Review." It evaluates all BLOCKING and MAJOR issues, resolves the open decisions regarding the input vector space, triages minor issues, and exposes critical unflagged gaps that were missed in previous audits.
````

#### Gemini: Physics residual and Hamiltonian mass scaling discrepancy

_Source: Gemini; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md:148`_

````markdown
### Unflagged Gap 1: Physics Residual and Hamiltonian Mass Scaling Discrepancy
The audit correctly identified that the characteristic length $D$ must include total mass: $D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$. However, neither the authors nor the audit traced how this change propagates into the physics residual equation ($\mathcal{L}_{\text{physics}}$) or the Hamiltonian Energy Regularizer ($\mathcal{L}_{\text{energy}}$). 

If we start with Newton's law:
$$\frac{d^2 \mathbf{r}_i}{dt^2} = G \sum_{j \neq i} \frac{m_j (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$
And substitute the scaled variables $t = T \cdot u$ and $\mathbf{r} = D \cdot \mathbf{r}'$:
$$\frac{D}{T^2} \frac{d^2 \mathbf{r}'_i}{du^2} = G \sum_{j \neq i} \frac{m_j D (\mathbf{r}'_j - \mathbf{r}'_i)}{D^3 |\mathbf{r}'_j - \mathbf{r}'_i|^3}$$
$$\frac{d^2 \mathbf{r}'_i}{du^2} = \frac{G T^2}{D^3} \sum_{j \neq i} \frac{m_j (\mathbf{r}'_j - \mathbf{r}'_i)}{|\mathbf{r}'_j - \mathbf{r}'_i|^3}$$
Substituting the corrected $D^3 = G \cdot M_{\text{tot}} \cdot T^2$, the coefficient $\frac{G T^2}{D^3}$ perfectly simplifies to $\frac{1}{M_{\text{tot}}}$. 

Therefore, the true dimensionless equation of motion is:
$$a'_i = \frac{1}{M_{\text{tot}}} \sum_{j \neq i} \frac{m_j (\mathbf{r}'_j - \mathbf{r}'_i)}{|\mathbf{r}'_j - \mathbf{r}'_i|^3}$$

However, `pinn_architecture.md` Section 3.2 defines the residual without this mass factor, explicitly stating: *"Masses (unchanged, as G=1 in the dimensionless system)"*. 
**Resolution:** This is a fatal omission. If the physics residual does not include the $1/M_{\text{tot}}$ division (or equivalently, if the raw masses $m_j$ are not scaled to mass fractions $m'_j = m_j / M_{\text{tot}}$ before entering the loss calculation), the network will attempt to learn accelerations that are intrinsically mismatched to the data loss. The physics loss implementation must divide the gravitational sum by $M_{\text{tot}}$.

**The Next Logical Question: Does $\mathcal{L}_{\text{energy}}$ also require this adjustment?**
Yes. In the PINN Architecture Document (Section 3.3), the Hamiltonian $H_{\text{total}}$ is defined using the raw unscaled masses $m_i$ alongside the scaled dimensionless kinematics ($r', v'$). The true kinetic energy relies on $v_i^2$, which scales as $\frac{D^2}{T^2} v_i'^2$, and potential energy relies on $1/r_{ij}$, which scales as $1/(D r_{ij}')$. Because $\frac{D^2}{T^2} = \frac{M_{\text{tot}}}{D}$ (derived from $D^3 = G M_{\text{tot}} T^2$), calculating the Hamiltonian with raw masses fundamentally breaks the conservation of energy mapping in dimensionless space. 
To maintain thermodynamic and kinetic energy conservation, the $\mathcal{L}_{\text{energy}}$ implementation must explicitly scale the raw input masses to mass fractions ($m'_i = m_i / M_{\text{tot}}$) or apply a global conversion scalar to the baseline $H_0$ target. Failure to implement this parallel correction ensures the energy loss term will forever fight the physics residual term, preventing the network from reaching convergence.
````

#### Gemini: ALM moving-average desynchronization

_Source: Gemini; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/gemini_research_report.md:168`_

````markdown
### Unflagged Gap 2: ALM Moving Average De-synchronization
The Augmented Lagrangian Method (ALM) relies on an exponential moving average of the squared physics loss ($v_p$) to adaptively update the penalty coefficient $\mu_p$. `pinn_architecture.md` specifies an "adaptive" collocation point sampling strategy that biases sampling toward high-acceleration regions. 
If the collocation points change dynamically and drastically from batch to batch, the baseline variance of $\mathcal{L}_{\text{physics}}$ will fluctuate wildly. The ALM's momentum buffer $\beta = 0.99$ assumes a relatively stationary loss landscape. Rapid fluctuations caused by adaptive point sampling will cause $\mu_p$ to destabilize, oscillating between under-penalizing physics (leading to non-physical solutions) and over-penalizing physics (stalling convergence).
**Resolution:** During early training stages (Stages 0-2), enforce the `uniform` collocation point strategy to allow $v_p$ and $\mu_p$ to stabilize. Only introduce `adaptive` collocation sampling in Stages 4-6 when the network requires high-density sampling around close encounters, and consider reducing the ALM momentum $\beta$ to 0.90 to allow it to react faster to sampling-induced variance.

**Sources:**
1. [computationalimaging.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhmJaxQlB8KTOgmqot9-MSZ60UM9wnZU77BpkaLhQBbVnzdajgEZkYjkeQ8cEmlPwM0rKDT8vSsRahQwBqzidr5DC-vr3ovKyA3-y8KkpTJDV8lX4WBGDMhOgTF8vZAvMtkb8kvDl1IipRPR5F)
2. [neurips.cc](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg7OKf36xhvWu0cC2pVWOMvT5I_3yhqxVml5wBjjhltBCeq6ng0Op2l5VZEDGwuOkI3RfPUlP6XFnbq-1chN5YcPjs8IKYFgiBg2BnRYBifkznh9_v9rnDv1BgUBie_wESe5q__eiYFoF60TrwZ8iHZDlBL5Y6fhGXupsqGEPy4-dFuevBG5n9x6-MLtvX)
3. [emergentmind.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHWv6j8gOdk0VMlzHNDwNO9mJjAX_RKawVICT8S9-YOFtzN9bP6K5kDafzmaCRIHCtnzjkQCEVLQcM435hqruqWZet8qtm6fEKpuxj-OO9uMoSOtEoax7e9RoMeFb-KNe05xWni3fZS8cKq4g==)
````

## 8. Open Decisions and Minor-Issue Triage
Open decisions are split by semantic meaning, not report-local D labels. Input-vector D-01 appears in Section 6 under input composition; loss-balancing D-01 appears in Section 6 under loss balancing. D-02 remains a routine documentation/input-normalization decision rather than fully settled implementation guidance.

| Decision or minor label | Semantic location | Report-local handling |
|---|---|---|
| D-01 | Input-vector composition and open decision D-01; Loss-balancing D-01 | ChatGPT/Gemini use D-01 for input vector; Claude 1/Claude 2 use D-01 for energy/loss balancing. |
| D-02 | `I_3` and `I_norm` normalization | ChatGPT/Gemini discuss tanh-wrapped `I_norm`; Claude reports use D-02 mostly for routine cleanup. |
| D1-D10 | Minor issue triage D1-D10 | All source minor tables are preserved in Section 6; do not merge by raw D label without reading source heading/context. |

## 9. Unique Per-Report Insights Registry
| Report | Unique insight | Source block retained at | Registry status |
|---|---|---|---|
| ChatGPT | Force law and energy law are not gradients of the same softened potential. | Section 7: ChatGPT force–energy incompatibility; Section 6: Softening mismatch and force-energy consistency | VERIFIED |
| ChatGPT | D-01 alternatives are mathematically incomplete without enough shape/orientation information. | Section 7: ChatGPT D-01 alternatives; Section 6: Input vector composition and open decision D-01 | VERIFIED |
| ChatGPT | Current scalar ALM formulation is effectively a quartic penalty, not a standard ALM. | Section 7: ChatGPT scalar ALM; Section 6: Loss-balancing D-01 | VERIFIED |
| Claude 1 | L-BFGS is fragile when ALM dual updates change the objective. | Section 7: Claude 1 L-BFGS sensitivity; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 1 | SIREN may have a spectral bottleneck across curriculum stages. | Section 7: Claude 1 SIREN spectral bottleneck; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 1 | Brutus precision and Lyapunov-horizon contract should be explicit. | Section 7: Claude 1 Brutus precision contract; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 1 | Permutation symmetry may waste model capacity without canonical ordering or equivariance. | Section 7: Claude 1 permutation symmetry waste; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 1 | Curriculum expansion may need replay buffers to prevent catastrophic forgetting. | Section 7: Claude 1 replay buffer gap; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 1 | 3D-vs-planar inheritance needs explicit methodology disclosure. | Section 7: Claude 1 methodology disclosure gap; Section 6: Input dimensionality and unflagged gaps | VERIFIED |
| Claude 2 | A single SIREN output model may hit a representational ceiling for full 3D chaos. | Section 7: Claude 2 representational ceiling; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 2 | Data-loss and physics-loss minima may be adversarial rather than aligned. | Section 7: Claude 2 adversarial minima; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 2 | Training-data precision contract is unspecified. | Section 7: Claude 2 Brutus precision; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Claude 2 | Width 256 may be undersized if inherited from planar-data assumptions. | Section 7: Claude 2 width undersizing; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Gemini | Physics residual and Hamiltonian energy regularizer may miss the `1/M_tot` acceleration scaling. | Section 7: Gemini mass-scaling discrepancy; Section 6: Unflagged gaps and unique risks | VERIFIED |
| Gemini | ALM moving average can desynchronize under adaptive collocation. | Section 7: Gemini ALM desynchronization; Section 6: Unflagged gaps and unique risks | VERIFIED |

### Additional Source-Specific Blocks Preserved for Heading Coverage

#### Claude 1 remaining blockers sparse evidence

_Source: Claude 1_

````markdown
### B-09 / B-10 — Remaining blockers (sparse evidence)

Without the spec, I can flag plausible candidates: (i) a missing factor of ½ in kinetic energy, (ii) a sign error in the gradient of the potential (the −G m₁ m₂/r vs +), (iii) a softmax/temperature applied to physical outputs. All three are common in PINN reimplementations of HNN-style energies. These should be unit-tested by integrating a Kepler orbit analytically and comparing.

---
````

#### Claude 1 citation inaccuracies

_Source: Claude 1_

````markdown
### M4 — Citation inaccuracies

Without the spec I cannot enumerate. Common errors in this literature: citing "SIREN" as Stanford-only when it's Sitzmann (Stanford) + Sitzmann/Martel/Bergman/Lindell/Wetzstein; citing HNN as "Google" when it's Greydanus (Google Brain) + Dzamba (PetCube) + Yosinski (Uber); citing Brutus as 2018 when it's Boekholt & Portegies Zwart 2015 (arXiv:1411.6671). All citations should be re-verified against MNRAS/NeurIPS-listed records.
````

#### Claude 1 recommended fix queue

_Source: Claude 1_

````markdown
### M5 — Recommended fix queue P0–P2 prioritization

The review's queue should be: P0 = B-01, B-02, B-03/B-05, B-04 (all are correctness-critical, all are localized fixes); P1 = M1, M2, M3 (correctness, but with workarounds); P2 = M4, D1–D4 (cleanup).
````

#### Claude 1 curriculum threshold motivation

_Source: Claude 1_

````markdown
### M10 — Curriculum threshold motivation

**Verdict: CONFIRMING the review's concern that thresholds need physical motivation.** The Mikkola & Tanikawa (2007, *MNRAS Letters* 379, L21–L24) paper establishes that in the equal-mass three-body problem, the disruption time t_d and Lyapunov time t_L follow a two-part power-law relationship (Urminsky & Heggie 2009, *MNRAS* 392, 1051); the Lyapunov time itself scales roughly as the crossing time t_c. **Recommended curriculum thresholds**, in Hénon time units:

- Stage 0 (Keplerian / hierarchical): T ≤ 1 t_c (~0.5 Lyapunov times)
- Stage 1: T ≤ 5 t_c
- Stage 2: T ≤ 20 t_c (~10 Lyapunov times — the regime where Breen et al. trained)
- Stage 3: T ≤ 100 t_c (early dissolution regime)
- Stage 4–6: progressively longer, with the understanding that beyond ~30 Lyapunov times, no point-wise prediction is meaningful and the network is being trained to match ensemble statistics, not trajectories (Boekholt, Moerman & Portegies Zwart 2020, *MNRAS* 493, 3932; Portegies Zwart & Boekholt 2018).

The current spec's thresholds (whatever they are) should be expressed in Lyapunov-time multiples, not absolute time, so they transfer across different initial conditions of differing energy.

---
````

#### Claude 1 routine documentation cleanup

_Source: Claude 1_

````markdown
### D-02 — Routine documentation cleanup (LIGHT weight)

**Recommendation:** standardize all formulas to one notation (suggest: Latin indices i,j ∈ {1,2,3} for bodies, Greek for spatial dimensions, t for canonical time, τ for SIREN input τ ∈ [−1, 1], explicit dimensions in every equation). Add a single "Conventions" appendix to the spec. Resolve M4 citation issues at the same pass.

---
````

#### Claude 1 final readiness assessment

_Source: Claude 1_

````markdown
## 8. Final Readiness Assessment

| Layer | Status |
|---|---|
| SIREN backbone math | **NOT READY** — fix B-01 first |
| AD-based dynamics | **NOT READY** — fix B-02 |
| Data pipeline (Brutus → tensors) | **NOT READY** — fix B-03/B-05 and B-04 |
| Loss balancing (ALM) | **Acceptable**, with caveats on chaotic regime |
| Curriculum design | **Conceptually sound**, thresholds need physical motivation (M10) |
| Energy regularization | **Open decision D-01** — recommend soft penalty, curriculum-gated |
| Documentation | **Routine cleanup needed** (D-02 and M4) |

Once B-01, B-02, B-03/B-05, B-04, and B-06 are landed (estimated 1–2 weeks of focused work), Stage-0 training should reach a clean baseline; Stages 1–3 will exercise the M-class issues and the D-01 decision; Stages 4–6 are research-grade and depend on the SIREN spectral question (Gap #2 above) being resolved.
````

#### Claude 2 citation inaccuracies

_Source: Claude 2_

````markdown
### M5 — Citation inaccuracies

**Likely confirmed but unverifiable without the audit text.** Doc-only; fold into D-02.
````

#### Claude 2 remaining majors broad sweep

_Source: Claude 2_

````markdown
### M8, M9, M10 — Remaining Majors

Without the verbatim audit, I treat these as downstream of the same unit-discipline and COM-frame fix passes already prescribed under B-02, B-05, and B-08. Specifically, M8 and M9 are almost certainly corollaries of either the characteristic-length convention (M8) or the SIREN init prose (M9), and should be addressed by the one-pass spec edits described above. M10 likely concerns Lyapunov-time normalization in the curriculum stratification, addressed in the Minor triage below. **Recommendation:** sweep all three in the same revision that closes B-02, B-05, and B-08.
````

#### Claude 2 routine documentation cleanup

_Source: Claude 2_

````markdown
### D-02 — Routine documentation cleanup (FIRM recommendation)

Adopt a single spec edit pass that, in one commit, performs the following: (i) fixes the SIREN init prose per B-01 to the paper-exact form; (ii) locks $M_{\mathrm{tot}}$ as the mass constant in $D$ per B-02; (iii) declares "all positions, velocities, accelerations, energies, and angular momenta are computed in the COM frame, enforced architecturally" per B-05; (iv) states the chosen $\varepsilon$ in the physics residual per B-06; (v) corrects the constraint count to "$E$ plus three components of $\mathbf{L}$" per B-10; (vi) replaces "HNN-style energy regularization" with "soft energy-conservation regularizer" per B-07. No prose-only branches, no future-tense placeholders. This is one editor-day of work and should be completed before the code-side P0 fixes so that the spec is the source of truth those fixes are validated against.
````

## 10. Cross-Issue Dependencies
Cross-issue dependencies are preserved as source blocks. They identify relationships between issues but do not create new consolidation-layer recommendations.

### ChatGPT: Cross-issue dependencies

````markdown
## 6. Cross-Issue Dependencies

The review's priority queue should be reordered.

The first dependency is **not** “fix $D$ to 6.694,” because that fix is tied to a different mass-scaling convention than the one the specs currently use.

The true first dependency is:

$$
\text{D-01} + \text{B-03} + \text{M1} + \text{M2} + \text{M4}.
$$

That is, decide the gauge and the exact 14D input contract first.

Then proceed in this order:

1. **Unify preprocessing.** Implement one transformer for COM correction, zero-momentum boosting, optional canonical rotation, and scaling. This closes B-05 and resolves the real content behind M3.
2. **Fix AD derivatives.** Compute componentwise time derivatives and apply the missing factors of $2$ and $4$. Until this is fixed, the physics loss is not the stated physics loss.
3. **Fix the softened dynamics contract.** Replace the current force/potential softening pair with one consistent softened Hamiltonian and state the epsilon policy explicitly.
4. **Lock the SIREN contract.** Retain the current hidden-layer initialization, remove epochwise $\omega_0$ scheduling, and then do citation-level cleanup on B-01 and M8.
5. **Run ablations and cleanup.** After the above, evaluate LayerNorm and complete remaining documentation tasks.

---
````

### Claude 1: Cross-issue dependencies

````markdown
## 6. Cross-Issue Dependencies

| Must fix first | Before fixing |
|---|---|
| B-01 (SIREN init) | Anything; training cannot start otherwise |
| B-03/B-05 (COM frame) | B-04 (softening), M2 (constraint counts), D-01 (energy reg) — all depend on a consistent frame |
| B-02 (chain rule) | M3 (length normalization sanity check), any quantitative residual evaluation |
| B-04 (softening) | M10 (curriculum thresholds, which depend on close-approach behavior) |
| M3 (normalization) | M10 (curriculum thresholds expressed in dimensionless units) |
| B-06 (input dimension) | Everything downstream of the input layer |

**Recommended sequencing.** Land B-01, B-06, and B-02 simultaneously in one PR (these touch the network class and the dataset class but not the loss). Then land B-03/B-05 and B-04 together (these touch the data pipeline and the residual). Then revisit M-class issues. D-01 should be decided **before** Stage-3 training begins, but does not block Stages 0–2.

---
````

### Claude 2: Cross-issue dependencies

````markdown
## 5. Cross-Issue Dependencies and Revised Priority

The audit's P0→P2 ordering is broadly correct but should be re-sequenced because several apparently-independent items share a single root cause.

The dependency graph in prose: every loss term in the physics residual depends on velocities and accelerations, which depend on the autograd chain rule (B-04). Every conserved-quantity penalty depends on COM-frame consistency (B-05). Every dimensional balance across loss terms depends on the characteristic-length convention (B-02). Therefore B-04, B-05, and B-02 are the three root-cause fixes; B-07 (energy regularizer), B-08 (dimensional conflict), B-10 (constraint count), and M1–M3, M8–M10 are all downstream and resolve as side-effects once the three roots are settled.

The softening parameter (B-06) is independent of the roots and can be fixed in parallel — it is a single line in the residual computation and a one-sentence note in the data-generation contract.

D-01 (loss balancer) depends on B-04 and B-05 being settled, because the loss values being balanced have to be computed from the correct physical quantities before the balancer can do meaningful work. It does *not* depend on the unit-discipline pass, because causal weighting is scale-invariant in $\varepsilon$ relative to a single residual, and the ALM-on-conserved-quantities sub-system has only four scalars, so balance pathology is contained.

B-01 (SIREN init prose) and D-02 (doc cleanup) are independent of everything else; they should land first because they cost nothing and remove a source of future confusion when reviewing code-side fixes.

**Revised P0 (in order to apply):**

1. **B-01 + D-02** spec cleanup pass — one editor-day, zero risk.
2. **B-02** — lock $M_{\mathrm{tot}}$ in $D$, one spec line.
3. **B-05** — COM-frame architectural projection at the output head.
4. **B-04** — autograd chain rule; add a Kepler unit test as the regression guard.
5. **D-01** — replace bare ALM with causal-weighting + small-ALM hybrid in the loss module.

**Revised P1:**

6. **B-06** — softening match (or $\varepsilon = 0$ with collocation-point exclusion near close encounters).
7. **B-07** — rename and re-derive the energy regularizer in COM frame using chain-rule-corrected velocities.
8. **B-08, B-10** — unit-discipline pass and constraint recount.
9. **M1, M2, M3, M8, M9, M10** — sweep in the same pass.

**Revised P2:**

10. **M5 and Minor items D1–D10** — fold the documentation Minors into D-02; defer empirical Minors to post-first-training-run.
````

### Gemini: Cross-issue dependencies

````markdown
## 5. Cross-Issue Dependencies

The implementation priority queue provided in the audit is validated, provided the critical modifications listed below are strictly enforced. The dependencies cascade linearly, and attempting to train the model out of order will result in silently corrupted models.

1. **The Dimension Update (P0-1):** Fixing $D = (G \cdot M_{\text{tot}} \cdot T^2)^{1/3}$ is the absolute ground zero of the project. Because $D$ dictates $r'$, $v'$, and all subsequent invariants ($E, L_{\text{norm}}, Q, s_{\min}$), *every single data file* and stage assignment threshold must be recomputed before any other action is taken. 
2. **The Chain-Rule Fix (P0-5):** Once the data is properly scaled, the network must accurately map AD derivatives to physical derivatives. This must be implemented alongside the hidden unflagged gap identified below.
3. **The SIREN Contract (P0-2 & P0-6):** Only after the physical data is correct can the neural architecture be stabilized by fixing the hidden layer initialization and stripping the dead $\omega_0$ scheduling code.
````

## 11. Evidentiary Limitations and Caveats
Claude 1's preface is preserved in Section 4 and limits what that report could verify from source material. ChatGPT's evidentiary limitation is copied below because it is a caveat about audit scope, not a new technical gap.

#### ChatGPT: Evidentiary Limitation

_Source: ChatGPT; span: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/chatgpt_research_report.md:1129`_

````markdown
### Evidentiary Limitation

Because this audit was performed on the supplied markdown specifications rather than the live code, I cannot verify two implementation-state claims from the review with certainty:

1. Whether `update_omega0()` is actually dead code.
2. Whether the live derivative routine already avoids the collapsed vector-Jacobian pattern.

Where that distinction matters, I classify the issue as one of:

- **Document error**.
- **Code risk**.
- **Unverified implementation claim**.

I do not treat unverified implementation claims as confirmed code defects.
````

### Checkout Caveat

The implementation plan expected the four source reports to be tracked by git. In this checkout they were initially present as untracked files, so the exact report inputs and this master report were staged before final verification. The current `git ls-files` pre-check lists all four source reports, and Section 13 records before/after SHA-256 hashes to verify the source reports were not modified.

## 12. Omitted Content Log
| Source report | Source heading | Omitted content type | Reason | Replacement or retained location |
|---|---|---|---|---|
| Claude 2 | B-02 / B-03 — Characteristic length $D$ and dimensional consistency | cross-reference (not omission) | Block applies to both characteristic-D and input-dimensionality semantics; primary paste is under characteristic-D to preserve dissent handling. | `## 6` → `### Characteristic length D and mass scaling`; cross-reference from input dimensionality. |
| Gemini | B-03, B-04, M1, M2: Input Vector Dimensionality and Composition | cross-reference (not omission) | Grouped block applies to both dimensionality and composition; primary paste is under dimensionality. | `## 6` → `### Input vector dimensionality and 3D-vs-planar encoding`; cross-reference from input-vector composition. |
| ChatGPT | Missed Issue 3 — The “ALM” Formulation Is Not a Standard Augmented Lagrangian | cross-reference (not omission) | Block is fully preserved in unflagged gaps and linked from loss-balancing D-01. | `## 7` → `#### ChatGPT: Current scalar ALM rule is not a standard ALM`; cross-reference from loss-balancing D-01. |
| Gemini | Unflagged Gap 2: ALM Moving Average De-synchronization | cross-reference (not omission) | Block is fully preserved in unflagged gaps and linked from loss-balancing D-01. | `## 7` → `#### Gemini: ALM moving-average desynchronization`; cross-reference from loss-balancing D-01. |
| ChatGPT | Missed Issue 1 — Force–Energy Incompatibility Under Softening | cross-reference (not omission) | Block is fully preserved in unflagged gaps and linked from softening mismatch. | `## 7` → `#### ChatGPT: Force–energy incompatibility under softening`; cross-reference from softening mismatch. |
| ChatGPT | Missed Issue 2 — D-01 Alternatives Are Mathematically Incomplete | cross-reference (not omission) | Block is fully preserved in unflagged gaps and linked from input-vector D-01. | `## 7` → `#### ChatGPT: D-01 alternatives mathematically incomplete`; cross-reference from input-vector composition. |
| All reports | Prompt boilerplate or generic repeated caveats | none omitted | No source report content was removed solely for brevity; duplicate semantic uses are cross-referenced instead. | Source-preserved blocks in Sections 4, 6, 7, 9, 10, and 11. |

## 13. Verification Checklist
- Source inventory line counts match the plan: ChatGPT 1142, Claude 1 318, Claude 2 193, Gemini 176, total 1829.
- Heading counts match the plan: ChatGPT 7/20, Claude 1 9/17, Claude 2 6/14, Gemini 6/16 for `##`/`###`.
- Source reports are treated as read-only; before/after SHA-256 hashes are recorded in addition to the staged-file `git ls-files` and `git diff -- <source reports>` checks.
- Consensus statuses are semantic-issue statuses, not raw report-label statuses.
- The characteristic-D split preserves ChatGPT's raw-mass dissent and the other reports' `M_tot` position.
- Input-vector D-01 and loss-balancing D-01 are separate semantic issues.
- The omitted-content log records cross-references and confirms no source block was dropped solely for brevity.

### Source Hash Verification

| Report | SHA-256 before | SHA-256 after | Status |
|---|---|---|---|
| ChatGPT | `955108df182694af825a7e652b3aa3e1818714dd0e8c035e93edabc83db426cd` | `955108df182694af825a7e652b3aa3e1818714dd0e8c035e93edabc83db426cd` | unchanged |
| Claude 1 | `9ffb9611668f7b897afbb03bba6c3ced4dee195008eadfc0a01a3250b1f7bff8` | `9ffb9611668f7b897afbb03bba6c3ced4dee195008eadfc0a01a3250b1f7bff8` | unchanged |
| Claude 2 | `55c57d1e0674da5681dea6903c0b74f61022f5b878a7fd9f1513f076d1844d87` | `55c57d1e0674da5681dea6903c0b74f61022f5b878a7fd9f1513f076d1844d87` | unchanged |
| Gemini | `bf97859808404e0ccbd98fb27935243ed1f3469ea243d89d7317e6210953976e` | `bf97859808404e0ccbd98fb27935243ed1f3469ea243d89d7317e6210953976e` | unchanged |

### Source Heading Coverage Register

| Source report | Line | Source heading | Coverage status | Retained or accounted location |
|---|---:|---|---|---|
| ChatGPT | 3 | `## 1. Executive Summary` | PRESENT | Section 4 executive summaries |
| ChatGPT | 59 | `## 2. Issue-by-Issue Analysis: Blocking Findings` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| ChatGPT | 61 | `### B-01 — SIREN Hidden-Layer Initialization` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: SIREN hidden-layer initialization |
| ChatGPT | 120 | `### B-02 — Characteristic Length $D$` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Characteristic length D and mass scaling |
| ChatGPT | 200 | `### B-03 — Input-Vector Dimensionality Conflict` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| ChatGPT | 241 | `### B-04 — Input-Vector Composition` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector composition and open decision D-01 |
| ChatGPT | 284 | `### B-05 — COM-Frame Violation` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: COM frame and scaling order |
| ChatGPT | 355 | `### B-09 — Softening Mismatch` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Softening mismatch and force-energy consistency |
| ChatGPT | 434 | `### B-10 — Dynamic $\omega_0$ Scheduling` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Dynamic `omega0` scheduling |
| ChatGPT | 475 | `## 3. Issue-by-Issue Analysis: Major Findings` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| ChatGPT | 477 | `### M1 and M2 — IC-Vector Size and Total Input Size` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| ChatGPT | 529 | `### M3 — Order of COM Transform and Scaling` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: COM frame and scaling order |
| ChatGPT | 572 | `### M4 — Constraint Counting and Injectivity Argument` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Constraint counting |
| ChatGPT | 612 | `### M5 — $I_3$ Normalization` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `I_3` and `I_norm` normalization |
| ChatGPT | 674 | `### AD Chain-Rule Factor and Derivative Collapse` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: AD chain-rule and derivative collapse |
| ChatGPT | 793 | `### M8 — LayerNorm Attribution` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: LayerNorm attribution and affine setting |
| ChatGPT | 818 | `### M9 and M10 — $E_{\mathrm{norm}}$ Range and Asymmetric Mass Normalization` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `E_norm` and mass normalization ranges |
| ChatGPT | 849 | `## 4. Open Decisions Recommendation` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| ChatGPT | 851 | `### D-01 — 14D Input-Vector Composition` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector composition and open decision D-01 |
| ChatGPT | 987 | `### D-02 — $I_{\mathrm{norm}}$: Raw Ratio Versus Tanh-Wrapped` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `I_3` and `I_norm` normalization |
| ChatGPT | 1016 | `## 5. Minor Issues Triage` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Minor issue triage D1-D10 |
| ChatGPT | 1032 | `## 6. Cross-Issue Dependencies` | PRESENT AS PART OF SEMANTIC ISSUE | Section 10 cross-issue dependencies |
| ChatGPT | 1056 | `## 7. What Was Not Flagged` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Unflagged gaps and unique risks |
| ChatGPT | 1058 | `### Missed Issue 1 — Force–Energy Incompatibility Under Softening` | PRESENT | Section 7 unflagged gaps |
| ChatGPT | 1076 | `### Missed Issue 2 — D-01 Alternatives Are Mathematically Incomplete` | PRESENT | Section 7 unflagged gaps |
| ChatGPT | 1098 | `### Missed Issue 3 — The “ALM” Formulation Is Not a Standard Augmented Lagrangian` | PRESENT | Section 7 unflagged gaps |
| ChatGPT | 1129 | `### Evidentiary Limitation` | PRESENT | Section 11 evidentiary limitations |
| Claude 1 | 3 | `## Preface: Source Material and Method` | PRESENT | Section 4 executive summaries |
| Claude 1 | 9 | `## 1. Executive Summary` | PRESENT | Section 4 executive summaries |
| Claude 1 | 25 | `## 2. Issue-by-Issue Analysis — Blockers (Deep Treatment)` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Claude 1 | 27 | `### B-01 — SIREN weight initialization` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: SIREN hidden-layer initialization |
| Claude 1 | 58 | `### B-02 — Missing chain-rule factor in automatic differentiation` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: AD chain-rule and derivative collapse |
| Claude 1 | 95 | `### B-03 / B-05 (COM-frame violations) — Lab-frame data vs COM-frame output` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: COM frame and scaling order |
| Claude 1 | 125 | `### B-04 — Plummer softening mismatch` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Softening mismatch and force-energy consistency |
| Claude 1 | 145 | `### B-06 — Dimension conflicts in the input vector / 3D vs planar` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| Claude 1 | 177 | `### B-07 / B-08 — Dead code and dimension conflicts in the loss assembly` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 1 | 183 | `### B-09 / B-10 — Remaining blockers (sparse evidence)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 1 | 189 | `## 3. Issue-by-Issue Analysis — Major Issues (Moderate Treatment)` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Claude 1 | 191 | `### M1 — Dimension gap in 3D vs 2D physical invariants` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| Claude 1 | 195 | `### M2 — Constraint counting errors` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Constraint counting |
| Claude 1 | 199 | `### M3 — Normalization bugs (characteristic length D = (G M_tot T²)^(1/3))` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Characteristic length D and mass scaling |
| Claude 1 | 211 | `### M4 — Citation inaccuracies` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 1 | 215 | `### M5 — Recommended fix queue P0–P2 prioritization` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 1 | 219 | `### M8 — Loss-balancing methodology (ALM vs alternatives)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 1 | 231 | `### M9 — HNN-style energy regularization placement` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 1 | 235 | `### M10 — Curriculum threshold motivation` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 1 | 249 | `## 4. Open Decisions — Recommendation` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Claude 1 | 251 | `### D-01 — Energy regularization methodology (HEAVY analytical weight)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 1 | 267 | `### D-02 — Routine documentation cleanup (LIGHT weight)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 1 | 273 | `## 5. Minor Issues — Triage` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Minor issue triage D1-D10 |
| Claude 1 | 279 | `## 6. Cross-Issue Dependencies` | PRESENT AS PART OF SEMANTIC ISSUE | Section 10 cross-issue dependencies |
| Claude 1 | 294 | `## 7. What Was NOT Flagged (Gaps the Review Missed)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Unflagged gaps and unique risks |
| Claude 1 | 307 | `## 8. Final Readiness Assessment` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 2 | 3 | `## 1. Executive Summary` | PRESENT | Section 4 executive summaries |
| Claude 2 | 17 | `## 2. Issue-by-Issue Analysis — BLOCKERS and MAJORS` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Claude 2 | 19 | `### B-01 — SIREN initialization wording (PINN Architecture §, "SIREN initialization")` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: SIREN hidden-layer initialization |
| Claude 2 | 33 | `### B-02 / B-03 — Characteristic length $D$ and dimensional consistency (CTL Instruction §2, "Scales")` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Characteristic length D and mass scaling |
| Claude 2 | 45 | `### B-04 — Autograd chain rule for $\tau = 2(t/T) - 1$ (PINN Architecture §, "AD-derived velocities/accelerations")` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: AD chain-rule and derivative collapse |
| Claude 2 | 59 | `### B-05 — COM-frame consistency` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: COM frame and scaling order |
| Claude 2 | 69 | `### B-06 — Softening parameter mismatch` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Softening mismatch and force-energy consistency |
| Claude 2 | 79 | `### B-07 — HNN-style energy regularization form` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 2 | 89 | `### B-08, B-09 — Dimensional conflicts in loss terms; dead code paths` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 2 | 95 | `### B-10 — Constraint counting in 3D three-body PINN` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Constraint counting |
| Claude 2 | 105 | `### M1, M2, M3 — Dimension gaps, constraint counting errors, normalization bugs` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| Claude 2 | 109 | `### M4 — ALM specification details` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 2 | 113 | `### M5 — Citation inaccuracies` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 2 | 117 | `### M8, M9, M10 — Remaining Majors` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 2 | 121 | `## 3. Open-Decision Recommendation` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Claude 2 | 123 | `### D-01 — Loss-balancing methodology (FIRM recommendation)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Loss-balancing D-01 |
| Claude 2 | 139 | `### D-02 — Routine documentation cleanup (FIRM recommendation)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 9 additional source-specific blocks |
| Claude 2 | 143 | `## 4. Minor-Issue Triage` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Minor issue triage D1-D10 |
| Claude 2 | 153 | `## 5. Cross-Issue Dependencies and Revised Priority` | PRESENT AS PART OF SEMANTIC ISSUE | Section 10 cross-issue dependencies |
| Claude 2 | 184 | `## 6. What Was Not Flagged` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Unflagged gaps and unique risks |
| Gemini | 15 | `## 1. Executive Summary` | PRESENT | Section 4 executive summaries |
| Gemini | 26 | `## 2. Issue-by-Issue Analysis (Blockers & Major)` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Gemini | 30 | `### B-01: SIREN Initialization Mismatch` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: SIREN hidden-layer initialization |
| Gemini | 36 | `### B-02: Characteristic Length ($D$) Formula` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Characteristic length D and mass scaling |
| Gemini | 43 | `### B-03, B-04, M1, M2: Input Vector Dimensionality and Composition` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector dimensionality and 3D-vs-planar encoding |
| Gemini | 48 | `### B-05 & M3: COM Frame Violation and Scaling Order` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: COM frame and scaling order |
| Gemini | 57 | `### B-09: Softening Parameter ($\epsilon$) Mismatch` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Softening mismatch and force-energy consistency |
| Gemini | 62 | `### B-10: Dynamic $\omega_0$ Scheduling` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Dynamic `omega0` scheduling |
| Gemini | 67 | `### AD Chain-Rule Factor Missing` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: AD chain-rule and derivative collapse |
| Gemini | 72 | `### M4: Constraint Counting Error` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Constraint counting |
| Gemini | 77 | `### M5: $I_3$ Normalization Mapping` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `I_3` and `I_norm` normalization |
| Gemini | 82 | `### M8: LayerNorm Attribution` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: LayerNorm attribution and affine setting |
| Gemini | 87 | `### M9: $E_{\text{norm}}$ Range Unused` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `E_norm` and mass normalization ranges |
| Gemini | 92 | `### M10: $m_{\text{norm}}$ Range Asymmetry` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `E_norm` and mass normalization ranges |
| Gemini | 97 | `## 3. Open Decisions Recommendation` | CROSS-REFERENCED | Section 13 heading coverage register; child blocks or section-specific extracts preserve associated content |
| Gemini | 101 | `### D-01: 14-D Input Vector Composition` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Input vector composition and open decision D-01 |
| Gemini | 119 | `### D-02: $I_{\text{norm}}$ Definition` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: `I_3` and `I_norm` normalization |
| Gemini | 124 | `## 4. Minor Issues Triage` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Minor issue triage D1-D10 |
| Gemini | 136 | `## 5. Cross-Issue Dependencies` | PRESENT AS PART OF SEMANTIC ISSUE | Section 10 cross-issue dependencies |
| Gemini | 144 | `## 6. What Was NOT Flagged (Critical Uncovered Gaps)` | PRESENT AS PART OF SEMANTIC ISSUE | Section 6: Unflagged gaps and unique risks |
| Gemini | 148 | `### Unflagged Gap 1: Physics Residual and Hamiltonian Mass Scaling Discrepancy` | PRESENT | Section 7 unflagged gaps |
| Gemini | 168 | `### Unflagged Gap 2: ALM Moving Average De-synchronization` | PRESENT | Section 7 unflagged gaps |
