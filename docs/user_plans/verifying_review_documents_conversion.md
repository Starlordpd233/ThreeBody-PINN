     Verification Prompts — Thematic Document Audit
     #for kimi's agent swarm

     Prompt 1: Verify 01-architecture-and-physics-foundations.md

     You are verifying the migration accuracy of "01-architecture-and-physics-foundations.md" against
     the master archive of 7 original audit/issue files.

     ## FILES TO READ
     1. Read: pinn_instruction/original_latex/review-of-framework/issues/01-architecture-and-physics-fo
     undations.md
     2. Read: pinn_instruction/original_latex/review-of-framework/issues/MIGRATION.md
     3. Read: pinn_instruction/original_latex/review-of-framework/issues/archive/ARCHIVE_MASTER.md
        - This file contains all 7 originals wrapped in <!-- FILE_BEGIN / FILE_END --> markers.
        - Extract each embedded file by locating its markers. The 7 files are:
          (a) next steps.txt
          (b) stage-assignment-issue.txt
          (c) next-step-for-data-processing-pipeline.txt
          (d) review.md
          (e) Issue_on_data_validation_protocol_and_compatbility_with_project_context.md
          (f) three_body_pinn_pre-implementation_audit_2026-04-27.md
          (g) Causal_Trainingmismatch_resolution_blueprint.md

     ## SCOPE FOR THIS DOCUMENT
     Doc 01 covers these topics (per MIGRATION.md provenance map):
     - SIREN hidden-layer init formula defect (B-01): from three_body_pinn_pre-implementation_audit +
     basic_architecture.py live code check
     - Characteristic length D formula error (B-02): from audit + Causal_Trainingmismatch + next
     steps.txt
     - Input vector dimensionality conflict (B-03, M1, M2): from audit §5 + next steps.txt
     - Input vector composition: trig encoding vs shape invariants (B-04): from audit §5.3 vs
     Causal_Trainingmismatch
     - COM frame violation in hierarchical ICs (B-05): from audit + Causal_Trainingmismatch +
     next-step-for-data-processing-pipeline.txt
     - Softening parameter 5-OoM mismatch (B-09): from audit + Causal_Trainingmismatch + next steps.txt
      Issue 15
     - Dynamic omega0 scheduling has no runtime effect (B-10): from audit + next steps.txt Issue 4
     - AD chain-rule factor missing (from review.md): derivative conversion rules verbatim
     - Explicit AD implementation requirement (from next steps.txt Issue 12)
     - Dual-Context Epsilon Strategy (from Causal_Trainingmismatch): eps=1e-10 static vs eps_soft=1e-5
     dynamic
     - Input Vector Normalization Formulas table (from next steps.txt Issue 19)
     - Frame Convention: Galilean Boost Mandate (from Causal_Trainingmismatch)
     - LayerNorm analysis (from audit D2/D3 + PINN architecture doc)
     - Quantitative Impact of D Formula Error table
     - Verbatim Option A trig encoding spec (from audit §5, copied verbatim)
     - Recommended Option B: Shape Invariants + Direction Cosines (from Causal_Trainingmismatch
     synthesis)

     ## VERIFICATION CHECKS
     For each major section in doc 01, verify:

     ### 1. Finding Accuracy
     - Every finding ID (B-01, B-02, B-03, M1-M5, M8-M10, D1-D4, D6, D8-D10) must match the severity,
     description, and location cited in the original archive source.
     - Check: was the severity upgraded/downgraded without explicit rationale?
     - Check: was any finding's location reference changed incorrectly?

     ### 2. Mathematical Correctness
     - D = cbrt(G * M_tot * T^2) = cbrt(1 * 3 * 100) = 6.694 — verify this computation matches the
     archive's corrected form.
     - SIREN init: bound = sqrt(6/n_in) / omega_0 — verify against Sitzmann et al. (2020) as stated in
     the archive.
     - Chain-rule factors: d/du = 2*d/dtau, d²/du² = 4*d²/dtau² — verify these match review.md exactly.
     - Normalization formulas table: verify each formula matches next steps.txt Issue 19 verbatim.
     - Quantitative Impact table: verify the relative error percentages (44% for positions, 108% for
     L_norm, 90% for Q) are mathematically consistent with the D=4.64→D=6.694 correction.

     ### 3. Synthesis Integrity
     - Where doc 01 synthesizes multiple sources (e.g., the dual-epsilon strategy combining
     Causal_Trainingmismatch with audit B-09), verify the synthesis does NOT create a new claim that
     contradicts any individual source.
     - The recommended Option B (shape invariants + direction cosines) should be clearly labeled as a
     recommendation, not as verbatim archive content. Verify this distinction is preserved.
     - The verbatim Option A spec (audit §5) must match the archive's §5 word-for-word. Spot-check 3-5
     lines.

     ### 4. Omission Check
     - Cross-reference the MIGRATION.md provenance rows that point to doc 01. For each row, verify the
     corresponding content exists in doc 01.
     - Check that all 36 unique findings claimed as preserved in MIGRATION.md that route to doc 01 are
     present.
     - Verify the Executive Summary accurately reflects the scope without introducing claims not found
     in any source.

     ### 5. Drift Check
     - Check that no finding was softened (e.g., "BLOCKING" → "MAJOR" without rationale).
     - Check that the AD chain-rule section preserves the review.md content verbatim (it is listed as
     "Synthesized; derivative rules verbatim").
     - Check that the COM transform ordering (COM FIRST, then scale) matches the archive's resolution,
     not an inverted version.

     ### 6. Internal Consistency
     - Verify doc 01 does not contain self-contradictions (e.g., stating D=6.694 in one section and
     using D=4.64 in a formula elsewhere).
     - Verify the normalization formulas table is consistent with the Option B spec section.
     - Verify the verbatim Option A and recommended Option B are clearly separated and not mixed.

     ## OUTPUT FORMAT
     Produce a structured report with these sections:
     1. **PASS / FAIL / PASS-WITH-NOTES** verdict for doc 01
     2. **Findings Verified:** count of finding IDs checked and confirmed accurate
     3. **Mathematical Checks:** each formula checked, with result (CORRECT / ERROR)
     4. **Discrepancies Found:** any errors, drifts, omissions, or unauthorized modifications — each
     with: section name, expected (from archive), actual (in doc 01), severity (CRITICAL / MAJOR /
     MINOR)
     5. **Verbatim Spot-Checks:** for sections marked "verbatim", report whether they match the archive
     6. **Summary:** one paragraph confirming overall migration quality or listing critical issues

     ---
     Prompt 2: Verify 02-data-pipeline-and-validation.md

     You are verifying the migration accuracy of "02-data-pipeline-and-validation.md" against the
     master archive of 7 original audit/issue files.

     ## FILES TO READ
     1. Read:
     pinn_instruction/original_latex/review-of-framework/issues/02-data-pipeline-and-validation.md
     2. Read: pinn_instruction/original_latex/review-of-framework/issues/MIGRATION.md
     3. Read: pinn_instruction/original_latex/review-of-framework/issues/archive/ARCHIVE_MASTER.md
        - Extract the 7 embedded files using the <!-- FILE_BEGIN / FILE_END --> markers.

     ## SCOPE FOR THIS DOCUMENT
     Doc 02 covers these topics (per MIGRATION.md provenance map):
     - Non-contiguous ID handling (B-11): from audit + next-step-for-data-processing-pipeline.txt
     - Blacklist not loaded (M11): from audit, re-classified as BLOCKING
     - Trajectory completeness gate missing (B-06): from audit
     - 184 standard IDs without gold counterpart (M13): from audit
     - Brutus footer schema variance: from audit + next steps.txt
     - Data Validation Protocol — 6-Gap Analysis: from
     Issue_on_data_validation_protocol_and_compatbility_with_project_context.md
     - Validation Threshold Clarifications: from
     Issue_on_data_validation_protocol_and_compatbility_with_project_context.md §5
     - Validation Metrics as Live Training Parameters (SCS, SASD, IPR, PSC): from
     Causal_Trainingmismatch_resolution_blueprint.md
     - File Format: h5 vs txt/json decision: from next-step-for-data-processing-pipeline.txt
     - Brutus Output Handling — Footer/Mass Drift Protocol: from audit B-06/D6
     - Precision Handling in Validation: from Issue_on_data_validation_protocol (Gap 5) + audit D6
     - Global Scale Computation (compute_globals): from next steps.txt Issue 17, corrected B-02 form
     - Temporal Resolution Bridging (dt_out heterogeneity): from
     Causal_Trainingmismatch_resolution_blueprint.md
     - DataLoader Requirements spec
     - Dataset Inventory table
     - Pipeline Stage Checklist
     - Recommended Resolutions (P1-1 through P2-2)
     - Severity Reclassification Ledger (M11, M12 reclassified from MAJOR to BLOCKING)

     ## VERIFICATION CHECKS
     For each major section in doc 02, verify:

     ### 1. Finding Accuracy
     - Every finding ID (B-06, B-11, M11-M13, D7) must match the severity, description, and location in
      the original archive.
     - M11 and M12 are re-classified from MAJOR to BLOCKING. Verify the Severity Reclassification
     Ledger explicitly documents the rationale (which it does: DataLoader cannot ship with
     silently-corrupted data; 32-points-per-trajectory is infeasible for 59-snapshot trajectories).
     - Verify the 6-Gap Analysis table accurately reflects
     Issue_on_data_validation_protocol_and_compatbility_with_project_context.md.

     ### 2. Mathematical Correctness
     - compute_globals function: verify D = cbrt(G * M_tot_ref * t_max^2) = 6.694 is used (corrected
     form), NOT the original D = cbrt(G * t_max^2) = 4.64.
     - Verify the corrected D value is explicitly called out as the "B-02 corrected form" in the doc.
     - SCS formula: max_t |H(t) - H(0)| / |H(0)| — verify against Causal_Trainingmismatch.
     - SASD formula: Δt_i * ||a(t_i)|| / ||v(t_i)|| — verify against Causal_Trainingmismatch.
     - IPR formula: (1/M) * Σ |d²q_spline/dt²(τ_k) - F_gravity^{ε=1e-5}(q_spline(τ_k))|² — verify
     epsilon value matches the doc's claim (eps=1e-5, not eps=1e-10).
     - Verify the resolution approach for dt_out scaling: n_col scales as dt_out/dt_base where
     dt_base=0.01, gold=1x, hier=8x, standard=17x.

     ### 3. Synthesis Integrity
     - The 6-Gap Analysis synthesizes from Issue_on_data_validation_protocol. Verify each gap (G1-G6)
     maps to a specific audit finding or decision without inventing new gaps.
     - The Validation Metrics section (SCS, SASD, IPR, PSC) synthesizes from Causal_Trainingmismatch.
     Verify each metric's formula, threshold, and role description matches the source.
     - Verify the Temporal Resolution Bridging section accurately reflects Causal_Trainingmismatch's
     treatment of the 17x dt_out variation.

     ### 4. Omission Check
     - Cross-reference MIGRATION.md rows pointing to doc 02. Verify each mapped section exists.
     - Verify the DataLoader Requirements section captures all requirements from the source files
     without losing any.
     - Check that the Pipeline Stage Checklist accurately reflects the 4-stage pipeline + gap
     description from the archive.

     ### 5. Drift Check
     - Check that no finding severity was changed without rationale (only M11 and M12 should have
     severity changes, and they must have explicit rationale in the Severity Reclassification Ledger).
     - Verify the recommended resolution for file format (Option A: Keep HDF5 + optional JSON export)
     matches next-step-for-data-processing-pipeline.txt's framing.
     - Verify the precision handling guidance (float64 acceptable, Decimal for mass verification)
     matches the archive sources.

     ### 6. Internal Consistency
     - Verify doc 02 does not contradict itself on key values:
       - dt_out values: gold=0.01, hier=0.08, standard=0.17
       - Snapshot counts: gold~1000, hier~125, standard~59
       - Blacklist count: 65 IDs
       - Missing gold IDs: 184
       - Final timestamp gate: >= 9.5
     - Verify the Recommended Resolutions list is consistent with the findings table (every BLOCKING
     and MAJOR finding has a corresponding resolution).

     ## OUTPUT FORMAT
     Produce a structured report with these sections:
     1. **PASS / FAIL / PASS-WITH-NOTES** verdict for doc 02
     2. **Findings Verified:** count of finding IDs checked and confirmed accurate
     3. **Mathematical Checks:** each formula checked, with result (CORRECT / ERROR)
     4. **Discrepancies Found:** any errors, drifts, omissions, or unauthorized modifications — each
     with: section name, expected (from archive), actual (in doc 02), severity (CRITICAL / MAJOR /
     MINOR)
     5. **Gap Analysis Verification:** confirm each of the 6 gaps matches the Issue_on_data_validation
     source
     6. **Summary:** one paragraph confirming overall migration quality or listing critical issues

     ---
     Prompt 3: Verify 03-curriculum-and-training-loop.md

     You are verifying the migration accuracy of "03-curriculum-and-training-loop.md" against the
     master archive of 7 original audit/issue files.

     ## FILES TO READ
     1. Read:
     pinn_instruction/original_latex/review-of-framework/issues/03-curriculum-and-training-loop.md
     2. Read: pinn_instruction/original_latex/review-of-framework/issues/MIGRATION.md
     3. Read: pinn_instruction/original_latex/review-of-framework/issues/archive/ARCHIVE_MASTER.md
        - Extract the 7 embedded files using the <!-- FILE_BEGIN / FILE_END --> markers.

     ## SCOPE FOR THIS DOCUMENT
     Doc 03 covers these topics (per MIGRATION.md provenance map):
     - Batch construction not implemented (B-07): from audit §6 + CTL Sec 5.3.2
     - Data-fidelity and collocation points conflated (B-08): from audit + CTL
     - Causal training mismatch: Option A vs Option B (from Issue_on_data_validation +
     Causal_Trainingmismatch)
     - Resolution: Time-Windowed Causal-ALM Hybrid (from
     Causal_Trainingmismatch_resolution_blueprint.md)
     - L_norm lacks clamping (M6): from audit
     - Lyapunov time tau_L dropped from IC vector (M7): from audit
     - Gradient clipping spec divergence (M14): from audit
     - Energy loss weight risks overwhelming (M15): from audit
     - dt_out heterogeneity collocation density (M16): from audit + Causal_Trainingmismatch
     - Stage transition criteria unattainable (D5): from audit §6.3
     - Data-Driven Adaptive Stage Assignment: PCA + K-means + quantiles (from
     stage-assignment-issue.txt)
     - tau_L and L_max Formula Resolution: from next steps.txt Issue 1
     - Huber delta calibration: from next steps.txt Issue 13
     - Loss Component Scaling Contract: from next steps.txt Issue 18 + main_pinn.tex + main_CTL.tex
     - ALM Parameter Update Spec: from audit §6
     - Gradient Clipping Merged Spec: from audit M14
     - Energy Loss Weight Schedule (capped hybrid): from audit
     - Implementation Checklist (P3 and P4 items): from audit §7
     - Verbatim Reference Specification — Unified Batch Construction: from audit §6, copied verbatim
     - Stage Inventory Summary table
     - Decision Priority Queue
     - Open Decisions: causal training mode + s_min collision criterion frame

     ## VERIFICATION CHECKS
     For each major section in doc 03, verify:

     ### 1. Finding Accuracy
     - Every finding ID (B-07, B-08, M6-M7, M14-M16, D5, NS-12, NS-13, NS-18) must match severity,
     description, and location in the original archive.
     - Verify the BLOCKING findings table accurately captures audit B-07 (batch construction) and B-08
     (data-fidelity/collocation conflation).
     - Verify NS-12 and NS-13 correctly trace to next steps.txt Issues 12 and 13 respectively.

     ### 2. Mathematical Correctness
     - tau_L computation function: verify the shadow trajectory divergence approach matches next
     steps.txt Issue 1. Check: D = 6.694 (corrected), horizon=50.0, n_pert=3, delta_t=0.1.
     - L_max computation: L_max = M_total * r_char * v_char where v_char = sqrt(2|E|/M_total). Verify
     this matches next steps.txt Issue 1 resolution.
     - L_norm computation: verify the function uses np.clip(L/(L_max+eps), 0, 1) — this is the M6 fix.
     - Stage transition thresholds: verify the table (Stage 0: 5e-3, Stage 1: 2e-3, ..., Stage 5-6:
     1e-4) matches audit §6.3.
     - Energy loss weight schedule: verify cap_table {0:1.0, 1:5.0, 2:20.0, 3:50.0, 4:100.0, 5:200.0,
     6:500.0} and base = 10^(stage-3) match the archive.
     - Gradient clipping: verify C_table {0:0.5, 1:0.5, 2:1.0, 3:1.0, 4:2.0, 5:3.0, 6:5.0} and formula
     C_stage * median(grad_norms[-100:]) matches audit M14.
     - ALM update: verify lambda_p += mu_p * L_physics, v_p = 0.99*v_p + 0.01*(L_physics^2), mu_p =
     0.01/sqrt(v_p + 1e-8), mu_p clipped to [1e-4, 100.0].
     - Huber delta: verify the recommendation delta_energy = np.clip(np.quantile(abs_delta_H_train,
     0.75), 0.01, 0.1) matches next steps.txt Issue 13.

     ### 3. Verbatim Section Check
     - The "Verbatim Reference Specification — Unified Batch Construction" section (audit §6) must
     match the archive's §6 word-for-word. Spot-check:
       - B_replay=240, B_lookahead=16
       - 50/50 uniform/acceleration-weighted sampling
       - n_col_per_traj=16
       - ALM update: lambda_p += mu_p * L_physics.item()
       - Stage transition criteria table
       - Energy loss weight schedule function

     ### 4. Synthesis Integrity
     - The Causal Training Mismatch section synthesizes from Issue_on_data_validation AND
     Causal_Trainingmismatch. Verify Option A, Option B, and the Hybrid Resolution accurately reflect
     the sources.
     - The Time-Windowed Causal-ALM Hybrid (4 phases) must match
     Causal_Trainingmismatch_resolution_blueprint.md's description.
     - The Data-Driven Adaptive Stage Assignment methodology (PCA + K-means + quantiles) must match
     stage-assignment-issue.txt's approach.
     - Verify the Loss Component Scaling Contract accurately synthesizes from next steps.txt Issue 18,
     main_pinn.tex, and main_CTL.tex.

     ### 5. Omission Check
     - Cross-reference MIGRATION.md rows pointing to doc 03. Verify each mapped section exists.
     - Verify the Implementation Checklist captures all P3 and P4 items from audit §7.
     - Verify the Executive Summary accurately reflects the scope without introducing claims not found
     in any source.

     ### 6. Drift Check
     - Check that the causal training decision is preserved as OPEN (not silently resolved to one
     option). The doc should present Option A, B, and Hybrid without declaring a winner.
     - Verify the s_min collision criterion open decision preserves the dual approach: unsoftened for
     stage gate, max(s_min, epsilon_soft) for training loss.
     - Verify the dt_out-aware collocation scaling recommendation is consistent with doc 02's treatment
      of the same issue (M16 in doc 02's MAJOR table).

     ### 7. Internal Consistency
     - Verify doc 03 does not contradict itself on key values:
       - Batch size: 240 replay + 16 lookahead = 256 total
       - Data-fidelity points: 8192; collocation points: 4096
       - 50/50 uniform/acceleration-weighted for BOTH data and collocation
       - MAX_EPOCHS: {0:500, 1:600, 2:700, 3:800, 4:900, 5:1000, 6:1200}
     - Verify the Decision Priority Queue is consistent with the Recommended Resolutions list.
     - Verify the Stage Inventory Summary table is consistent with the stage transition criteria.

     ## OUTPUT FORMAT
     Produce a structured report with these sections:
     1. **PASS / FAIL / PASS-WITH-NOTES** verdict for doc 03
     2. **Findings Verified:** count of finding IDs checked and confirmed accurate
     3. **Mathematical Checks:** each formula/code block checked, with result (CORRECT / ERROR)
     4. **Verbatim Spot-Checks:** for sections marked "verbatim", report whether they match the archive
     5. **Discrepancies Found:** any errors, drifts, omissions, or unauthorized modifications — each
     with: section name, expected (from archive), actual (in doc 03), severity (CRITICAL / MAJOR /
     MINOR)
     6. **Cross-Document Consistency:** note any conflicts between doc 03 and doc 01 or doc 02 on
     shared topics (e.g., M16 dt_out scaling, ALM spec, stage thresholds)
     7. **Summary:** one paragraph confirming overall migration quality or listing critical issues

     ---
     Usage Notes

     - Each prompt is self-contained. The agent can run them independently without shared context.
     - All three prompts instruct the agent to read MIGRATION.md for the provenance map, but also embed
      the complete scope information inline so the prompt works even if MIGRATION.md is unavailable.
     - Prompts are structured to produce comparable, machine-parseable output (verdict + counts +
     discrepancy tables).
     - For best results, run the three verifications in parallel using separate agent instances.