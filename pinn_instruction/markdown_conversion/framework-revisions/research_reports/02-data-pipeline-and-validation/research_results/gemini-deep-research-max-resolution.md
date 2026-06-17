# Issue 02 Resolution: Data Pipeline and Validation

## Executive Summary
The data pipeline exhibits physically robust trajectories, yet critical integration gaps exist between the generation of numerical simulations and the ingestion mechanics of the physics-informed neural network. The locked v1.4 conventions supersede the non-authoritative recommendations presented in the issue documents, necessitating strict adherence to established mathematical scaling and validation gates. Furthermore, missing data fallbacks pose a methodological dilemma that currently lacks sufficient evidentiary grounding, representing a critical STOP-gap.

To guarantee architectural compliance across all 14 foundational queries, this resolution mandates the following actions:
- **Q-A1:** Enforce a trajectory-completeness gate bounded strictly by `final_timestep >= 9.5`, rejecting arbitrary snapshot-count limits.
- **Q-A2:** Build an `id_to_path` dictionary to map non-contiguous IDs, absolutely prohibiting linear array indexing.
- **Q-A3:** Actively load the blacklist at initialization to explicitly and silently exclude the 65 known-bad trajectories from the curriculum, preventing massive initial residual spikes from corrupting the causal-weighting logic.
- **Q-A4:** Escalate the missing 184 gold-standard counterparts as a STOP-gap, as generating low-resolution proxies induces uncontrolled spectral bias.
- **Q-A5:** Apply definitive folder-level parameter defaults (`tol`, `dt_out`) for missing or minimal footers, explicitly flagging these parameters as inferred.
- **Q-A6:** Retain HDF5 (or .npy) as the primary tensor-ingestion format due to zero-copy memory requirements, utilizing JSON strictly for isolated human debugging and offline metadata inspection.
- **Q-B1:** Implement an adaptive points-per-trajectory sampling cap to prevent temporal exhaustion on sparse base datasets, ensuring sustainable stochasticity during mini-batch construction.
- **Q-B2:** Institute an exact mass-drift check at $t=0$ utilizing double-precision `float64`, triggering fallback decimal parsing only upon text-truncation failures.
- **Q-B3:** Standardize `float64` for all downstream validation metrics; it provides sufficient mantissa depth for the $10^{-5}$ physics soft constraints.
- **Q-B4:** Unconditionally uphold the locked raw-mass convention ($D \approx 4.6416$) to define the characteristic length scale, rejecting mass-fraction alternatives.
- **Q-C1:** Enforce the post-v1.3 logarithmic drift gate ($SCS > -5$) for Symplectic Conservation Score screening, dismissing raw-ratio propositions.
- **Q-C2:** Define Stiffness-Aware Sampling Density (SASD) data-side via the acceleration/velocity ratio, isolating $SASD > 0.5$ cases for resampling.
- **Q-C3:** Calculate Interpolation Physics Residual (IPR) via Cubic Hermite Splines, rigorously tied to the dynamic training softening parameter $\epsilon = 10^{-5}$.
- **Q-C4:** Compute Phase Space Coverage (PSC) entropy across discretized pairwise distance grids to quantify dataset diversity.

Training a Physics-Informed Neural Network (PINN) to resolve chaotic n-body gravitational systems requires a pipeline that respects both the arbitrary-precision numerics of the Brutus integrator and the causal training dynamics of the neural architecture. Because chaotic systems exhibit extreme sensitivity to initial conditions and timescale variations during close encounters, the standard machine-learning paradigm of uniform data ingestion is insufficient. The research package provided enumerates multiple discrepancies between the theoretical dataset requirements and the physical realities of the generated files. This report adjudicates these conflicts, prioritizing locked project constraints while explicitly evaluating the empirical dataset claims to formulate precise, actionable recommendations for the data pipeline.

## 0 Scope and Decision Standard

This resolution document addresses the questions posed in the `framed-research-questions.md` package regarding Issue 02. The analysis relies on the provided manifest and intact framework specifications (`ctl_instruction.md`, `pinn_architecture.md`, `data_quality_assessment.md`, `sampling_method.md`), the consolidated context fragments, the claims table (`claims-table.md`), and the subsequent erratum (`ERRATUM-2026-06-10.md`).

Explicitly excluded from this scope are topics deferred to the downstream "doc-03" milestone. This includes the implementation of collocation-density scaling (M16), the architectural selection of causal-training modes (G6), and the dynamic training-loop integration of metric sampling (such as Stiffness-Aware Sampling Density weighting or Phase Space Coverage replay). 

The evidentiary standard applied herein evaluates claims hierarchically. First, locked v1.4 conventions (Hard Constraints) are treated as immutable mathematical axioms. Second, empirically verified dataset facts—specifically those confirmed by the `ERRATUM-2026-06-10.md` or marked as `verified` in the claims register—override conflicting theoretical assumptions. Third, unverified claims (`claimed-unverified`) are utilized functionally but flagged for downstream verification (Phase 24). Finally, the non-authoritative recommendations proposed within the issue documentation are treated strictly as candidate hypotheses. 

## 1 Decision Matrix

To provide an immediate overview of the adjudications, the following matrix summarizes the verdict for each framed research question alongside its confidence level. 

| Question ID | Verdict Summary | Confidence |
| :--- | :--- | :--- |
| **Q-A1** | Enforce `final_timestep >= 9.5`; reject arbitrary snapshot-count bounds. | High |
| **Q-A2** | Implement `TrajectoryIndex` mapping IDs to paths; prohibit linear array indexing. | High |
| **Q-A3** | Enforce blacklist loading at initialization; loudly exclude listed IDs. | High |
| **Q-A4** | **STOP-gap**: Insufficient evidence to adjudicate fallback for missing gold data. | Low |
| **Q-A5** | Apply verified folder-level defaults for missing/minimal footers; flag as inferred. | High |
| **Q-A6** | Retain HDF5 as primary; permit JSON strictly for debugging/inspection. | High |
| **Q-B1** | Implement an adaptive points-per-trajectory cap to prevent temporal exhaustion. | High |
| **Q-B2** | Enforce mass-drift check at $t=0$ via `float64`; fallback to Decimal if needed. | High |
| **Q-B3** | `float64` is sufficient for validation; exact precision reserved for initial masses. | High |
| **Q-B4** | Uphold locked $D \approx 4.6416$ raw-mass convention; reject $6.694$ mass-fraction alternative. | High |
| **Q-C1** | Enforce logarithmic gate $SCS > -5$; reject non-authoritative raw-ratio limits. | High |
| **Q-C2** | Define data-side SASD via acceleration/velocity ratio; flag $> 0.5$ for resampling. | High |
| **Q-C3** | Define IPR via Cubic Hermite Splines utilizing dynamic training softening $\epsilon = 10^{-5}$. | High |
| **Q-C4** | Define PSC via Shannon entropy over discretized phase-space distance grids. | High |

These summaries abstract the complex physics and computational constraints detailed in the following sections.

## 2 Cluster A — Ingestion & Selection

The data ingestion pipeline forms the bridge between the raw outputs of the arbitrary-precision Brutus integrator and the mini-batch constructor of the PyTorch DataLoader. 

### Q-A1: Stage 4 to Stage 5 Validation Gate

The transition from offline metric extraction (Stage 4) to live PINN training (Stage 5) lacks a formalized gate. The issue document proposes a `TrajectoryValidator` enforcing a snapshot-count floor ($\ge 200$ for Stage 4+, $\ge 2$ for Stage 0-3) in addition to a temporal gate (`final_timestep >= 9.5`).

**Verdict / Recommendation:**
The DataLoader must implement a `TrajectoryValidator` that enforces `final_timestep >= 9.5` as the sole trajectory-completeness gate. The proposed `snapshot_count >= 200` threshold must be strictly rejected. 

**Reasoning:**
The dataset exhibits massive temporal resolution heterogeneity. As recorded in the claims register (CLM-10, `claimed-unverified`), standard quasi-random base trajectories contain approximately 59 snapshots per file. If a $\ge 200$ snapshot-count gate were implemented, the pipeline would systematically reject the entirety of the standard base dataset, catastrophically starving the curriculum of low-resolution chaotic regimes. The `final_timestep >= 9.5` rule is explicitly grounded in the dataset documentation's Completeness Checks and represents a physically meaningful threshold (ensuring the simulation reached at least 95% of its $t=10$ objective). The prevalence of this completeness (CLM-11) will be empirically verified by Phase 24, but the logical gate is sound.

**Evidence:**
- `simulation_data/Documentation/README.md` Completeness Checks explicitly ground the `final_timestep >= 9.5` logic.
- CLM-10 (~59 snapshots for standard trajectories) fundamentally invalidates the $\ge 200$ threshold.

**Confidence:** High. The primary risk is if Phase 24 reveals CLM-11 failure rates are exceptionally high, but the threshold logic itself remains valid.
**Verification:** Construct a unit test providing a valid trajectory with 59 snapshots terminating at $t=10.03$. The validator must accept it. 

### Q-A2: Non-Contiguous IDs (ID $\ne$ Array Index)

Curriculum logic currently assumes dense, contiguous linear indexing, matching an array index to a file ID. The issue document claims this causes silent mapping failures.

**Verdict / Recommendation:**
The DataLoader must construct an `id_to_path` dictionary by scanning the actual filesystem filenames upon initialization. Curriculum stage assignment must strictly query trajectories via a `get_by_id(file_id)` method. Dense linear indexing is explicitly forbidden.

**Reasoning:**
The numeric identifiers in the dataset are artifact labels, not sequential indices. The existence of ID gaps is an intentional byproduct of the sampling methodology, stemming from prescreen leapfrog rejections, simulation timeouts, and continuation runs. The claimed gap magnitudes—31.2% in the standard dataset (CLM-01) and 2.9% in the hierarchical dataset (CLM-02)—mean that a naive `array[427]` lookup will almost certainly fetch a trajectory with an ID completely disconnected from the intended initial conditions, misaligning the $IC_{13}$ network input vector with the Brutus ground-truth trajectory. The Erratum confirms that base and gold files share the exact same numeric prefix (`brutus_standard_XXXX.txt`); the folder dictates the fidelity, meaning the ID perfectly maps the entity across variants.

**Evidence:**
- `claims-table.md` CLM-01 and CLM-02.
- `ERRATUM-2026-06-10.md` confirms file naming prefix conventions.

**Confidence:** High. Relying on contiguous IDs in filtered datasets is a standard machine learning anti-pattern.
**Verification:** Pass an array of files `[0001, 0003, 0005]` to the `TrajectoryIndex`. Requesting `get_by_id(2)` must raise a `KeyError`, not return `0003`.

### Q-A3: Blacklist Loading and Consumption

An audit finding (M11) states that the `problematic_ics_blacklist.json` file is ignored during training ingestion, allowing known-bad trajectories into the network.

**Verdict / Recommendation:**
The `TrajectoryValidator` must load the blacklist JSON at initialization. Any trajectory whose ID matches a blacklisted entry for its respective variant (hierarchical or standard) must be silently excluded from the available training pool, and the total exclusion count must be logged.

**Reasoning:**
Chaotic gravitational simulations occasionally produce numerically unstable states—such as near-perfect singularities—that pass prescreening but fail to conserve energy within the tolerances of the PINN's capability. Ingesting these trajectories injects infinite loss spikes into the network. Under the causal-training architecture described in the specifications, a single massive residual early in the temporal sequence will drive the causal weight $w_n \to 0$ for all subsequent time steps (the "Causal Firewall" effect). Therefore, the 65 blacklisted IDs (CLM-03, `claimed-unverified`) must be actively filtered to preserve optimization stability. 

**Evidence:**
- `simulation_data/Documentation/problematic_ics_blacklist.json` contains the 65 IDs (CLM-03).
- `data_quality_assessment.md` outlines the Causal Firewall effect.

**Confidence:** High. The verification of the exact loading mechanism is pending Phase 24 (DATA-02).
**Verification:** Initialize the DataLoader. The length of the parsed trajectory set must equal the number of files on disk minus the length of the parsed blacklist.

### Q-A4: 184 Standard IDs Without a Gold Counterpart

A subset of 184 standard base IDs lacks a high-resolution gold counterpart. The issue doc poses two fallback policies: skip to Stage 6, or use low-fidelity data with a flag.

**Verdict / Recommendation:**
**STOP-gap.** There is insufficient evidence and no governing architectural constraint to safely adjudicate this policy. The decision must be escalated to the project owners. 

**Reasoning:**
The framework relies on a multi-stage curriculum. The 184 IDs (CLM-04, `verified`) exist in the base folder but not in the gold folder. If the pipeline "skips to Stage 6," it risks stranding these trajectories in lower stages without exposing them to terminal chaotic regimes, effectively removing difficult edge cases from late-stage training. Conversely, if the pipeline admits low-fidelity standard samples into a high-fidelity "gold" stage, the mini-batch constructor will mix $dt\_out = 0.17$ and $dt\_out = 0.01$ data inside the same gradient update. Because the doc-03 boundary defers collocation-density scaling (M16) to future work, mixing temporal resolutions in the current architecture risks severe spectral bias artifacts. Neither fallback is methodologically safe without explicit downstream adjustments.

**Evidence:**
- `standard_quasi_random_ids_not_in_gold.md` establishes the verified CLM-04 count.
- The `03-curriculum-and-training-loop.md` boundary prohibits defining collocation-scaling workarounds here.

**Confidence:** Low (Intentional STOP-gap). Deciding this without architectural clearance violates the evidentiary standard.
**Verification:** The project owner must select a path that aligns with the downstream causal-training implementation.

### Q-A5: Footer and Parameter Heterogeneity

Footer schemas across the Brutus output files vary, with a subset of files missing tolerance (`tol`) fields or omitting the footer entirely.

**Verdict / Recommendation:**
The DataLoader must parse the `Result:` footer strictly as optional metadata. If `tol`, `eta`, or the footer itself is absent, the parser must fall back to the folder-level defaults. A metadata flag `tol_confidence` must be assigned to each trajectory: `'direct'` if parsed from the footer, `'inferred'` if assigned via fallback.

**Reasoning:**
The `ERRATUM-2026-06-10.md` explicitly corrected the dataset narrative: 219 standard-gold files (CLM-07, `verified`) and numerous base files end with their final snapshot block and contain *no footer whatsoever*. Rejecting files lacking footers would unnecessarily discard thousands of valid trajectories. Because the dataset structures variants strictly by folder, the folder defaults (CLM-09, `verified`) are scientifically reliable proxies for the missing integration parameters. The specific folder-level defaults for all four variants must be applied independently as follows:
*   **Standard quasi-random base:** `tol = 1e-13`, `dt_out = 0.17`
*   **Standard quasi-random gold:** `tol = 1e-13`, `dt_out = 0.01`
*   **Hierarchical base:** `tol = 1e-15`, `dt_out = 0.08`
*   **Hierarchical gold:** `tol = 1e-13`, `dt_out = 0.01`

