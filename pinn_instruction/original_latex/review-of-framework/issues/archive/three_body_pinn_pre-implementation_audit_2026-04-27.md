# Three-Body PINN System — Comprehensive Technical Audit Report

**Audit Date:** 2026-04-27
**Scope:** README.md (dataset & pipeline docs), main_CTL.pdf (curriculum training learning plan), main_pinn.pdf (PINN architecture blueprint)
**Methodology:** 6 parallel thematic audits (Data Pipeline, Preprocessing & Physics, Input Vector, Architecture & Initialization, Loss & Training Loop, Author-Flagged Uncertainties) + cross-validation synthesis
**Auditors:** 6 specialized sub-agents + orchestrator integration

---

## EXECUTIVE SUMMARY

### Overall Readiness Assessment: **NOT READY FOR IMPLEMENTATION**

The three-body PINN system as documented has **fundamental mathematical, architectural, and pipeline-level errors** that will cause training failure, silent data corruption, or physically inconsistent predictions if implementation proceeds without remediation. The three source documents contain **28 author-flagged uncertainties**, **11 critical blockers**, **20+ major inconsistencies**, and **multiple unresolved design ambiguities**.

### Top 3 Blocking Issues

| Rank | Issue | Consequence if Unresolved |
|------|-------|--------------------------|
| **1** | **SIREN hidden-layer init formula multiplies by omega0 instead of dividing** (main_pinn.pdf Table 1) | At hidden_omega0=1 the bug is latent; if ever changed, variance explodes 810,000x → instant NaN across 12 layers. Contradicts Sitzmann et al. (2020) NeurIPS. |
| **2** | **Characteristic length D has two contradictory formulas** — CTL says D = cbrt(3GT^2) ≈ 4.64 (wrongly omitting M_tot); PINN says D = sqrt(3GT^2) ≈ 10 (dimensionally invalid). Correct: **D = (G*M_tot*T^2)^(1/3) = 6.694**. | All normalized quantities (E, L_norm, Q, velocities) are silently corrupted. Stage assignments depend on scaled energy — wrong D means wrong curriculum stages. |
| **3** | **Input vector dimensionality is claimed as 12D, 13D, and 14D simultaneously** across the documents. Trigonometric angle encodings ("5 values for 3 angles" in PINN doc) are **completely absent** from CTL. | Training code cannot be written — the first Linear layer requires a fixed input dimension. The 14D claim is the only one matching the PINN architecture, but CTL's pipeline produces only 11D. |

### Secondary Blockers ( severity)

4. **COM frame violation**: Hierarchical ICs have |COM| ~ 9e-3 after perturbation, but the PINN outputs in COM frame. Separate COM scripts for ICs vs. Brutus outputs with no mass-consistency check.
5. **Missing validation gate**: No gate between Stage 4 (metrics) and Stage 5 (training). Incomplete trajectories can silently enter training.
6. **Batch construction contradictory**: CTL requires replay/lookahead split (240+16 trajectories); PINN implements flat batch without replay. Author acknowledged inconsistency.
7. **Softening mismatch**: CTL uses epsilon=1e-10 for stage assignment; PINN uses epsilon_soft=1e-5 for physics/energy losses. Network learns different physics than curriculum sorts by.
8. **Dynamic omega0 scheduling is architecturally meaningless**: omega0 is an initialization-only parameter; scheduling it during training has no effect unless weights are re-initialized.
9. **Non-contiguous IDs break curriculum mapping**: 31% gap rate in standard dataset means linear indexing produces 45% wrong stage assignments.
10. **Stage transition criteria are theoretically unattainable**: Monotonically-decreasing validation loss requirement with limited data and Adam optimizer will block curriculum progression indefinitely.
11. **Energy loss weight schedule risks late-stage destabilization**: lambda_E=1000 at Stage 6 could make energy term 100-5000x larger than physics term, drowning dynamics learning.

---

## 1. CRITICAL ISSUES (BLOCKERS)

### B-01: SIREN Hidden-Layer Init Formula — Wrong Operator
| Field | Detail |
|-------|--------|
| **Issue** | Weight init uses `U[-omega0*sqrt(6/n), omega0*sqrt(6/n)]` (multiplies); should be `U[-sqrt(6/n)/omega0, sqrt(6/n)/omega0]` (divides) |
| **Location** | main_pinn.pdf Table 1, "Weight Init. (Hidden)" row; Section 2.2 |
| **Root Cause** | Author misread Sitzmann et al. (2020). Official code (vsitzmann/siren/modules.py:622) divides by omega0. |
| **Impact** | At hidden_omega0=1, wrong=correct (latent). At omega0=30, variance is 810,000x too large → instant NaN after 12 layers. |
| **Fix** | ```python
bound = np.sqrt(6.0 / n_in) / hidden_omega0  # DIVIDE, not multiply
m.weight.uniform_(-bound, bound)
``` |
| **Evidence** | Sitzmann et al., NeurIPS 2020, arXiv:2006.09661, Section 3.2; official implementation confirms. |

### B-02: Characteristic Length D — Two Wrong Formulas
| Field | Detail |
|-------|--------|
| **Issue** | CTL: D = cbrt(3GT^2) claims ~4.64 but cbrt(300)=6.69. PINN: D = sqrt(3GT^2) claims ~10 but sqrt(300)=17.32. Both dimensionally inconsistent. |
| **Location** | main_CTL.pdf Sec 4.2; main_pinn.pdf Table 2 |
| **Root Cause** | CTL omits M_tot=3 factor (uses cbrt(100)=4.64). PINN uses square root instead of cube root (dimensionally L^(3/2)/M^(1/2), not L). |
| **Impact** | All scaled energies off by 75%+, L_norm off by 77%, Q off by 90%. Stage assignment thresholds are in scaled units — systems near boundaries get wrong stages. |
| **Fix** | **D = (G * M_tot * T^2)^(1/3) = (3 * 100)^(1/3) = 6.694**. V = D/T = 0.669. Update both documents and recompute ALL stage assignments. |

### B-03: Input Vector Dimensionality — Three Conflicting Claims
| Field | Detail |
|-------|--------|
| **Issue** | 12D (CTL Sec 4.5 title, Sec 5.1.1), 13D (CTL Sec 4.5 "13-component IC" — mathematically inconsistent: 1+13=14, not 12), 14D (CTL closing note, PINN Table 2) |
| **Location** | main_CTL.pdf Sec 4.5 (internal contradiction); main_pinn.pdf Table 2 |
| **Root Cause** | Multiple edits without reconciliation. IC component count oscillates between 11 and 13. |
| **Impact** | **Cannot allocate first Linear layer.** No fixed n_in for weight matrix initialization. |
| **Fix** | Adopt **14D** as canonical: t' (1D) + IC (13D). CTL must replace 11-component IC description with 13-component spec including trigonometric encodings. Update all references. |

### B-04: Trigonometric Angle Encodings — Missing from CTL Entirely
| Field | Detail |
|-------|--------|
| **Issue** | PINN Table 2 specifies "5 values for 3 trigonometrically encoded angles" in IC vector. This component is NOWHERE in CTL Sections 4.4-4.5. |
| **Location** | main_pinn.pdf Table 2 vs main_CTL.pdf Sec 4.5 |
| **Root Cause** | Architecture decision (angle encodings) captured in PINN doc but never propagated to training plan (CTL). |
| **Impact** | CTL pipeline produces 11D IC; PINN expects 13D IC. At runtime: dimension mismatch, 2 dangling inputs receive garbage/zero, network cannot encode spatial orientation. |
| **Fix** | Add to CTL Sec 4.5. **Angles = (theta_L, phi_L, gamma_orb)** where (theta_L, phi_L) = spherical coords of L_hat, gamma_orb = orbital phase. Encoding: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]` = 5 values. All in [-1,1]. See Section 5 of this report for full specification. |

### B-05: COM Frame Violation in Hierarchical ICs
| Field | Detail |
|-------|--------|
| **Issue** | Hierarchical ICs perturbed out of COM/P=0 (|COM| median ~9e-3, |P| median ~3e-2). PINN assumes COM-frame outputs. Two separate COM scripts with no mass-consistency check. |
| **Location** | README.md lines 328-335; main_CTL.pdf Sec 4.3; main_pinn.pdf Sec 5.2 |
| **Root Cause** | Gaussian perturbations (sigma=0.01) applied AFTER COM enforcement in hierarchical IC generation. COM transformation is Step 2.5 in CTL, AFTER scaling in Step 2 — wrong order. |
| **Impact** | Network trained on targets that are NOT in COM frame learns wrong reference frame. COM offset ~0.01 is 5-20% of inner binary separation (a~0.1-0.3) — NOT negligible. |
| **Fix** | **Single unified COM transformer**: (a) COM recenter + reboost on RAW positions/velocities FIRST, (b) THEN scale by D, (c) Use IC masses as canonical for both ICs and Brutus outputs, (d) Assert `np.allclose(m_ic, m_brutus)` at t=0. Verification: ||P|| < 1e-12 after transform. |

### B-06: Missing Stage 4-to-5 Validation Gate
| Field | Detail |
|-------|--------|
| **Issue** | `calculate_metrics.py` generates metrics for ALL Brutus files including partial/errored runs. No completeness check at training time. |
| **Location** | README.md lines 677-678; main_CTL.pdf Stage 4 -> 5 gap |
| **Root Cause** | The only validity signal (`final_timestep >= 9.5`) runs at Stage 3 (runner scripts), never re-validated at DataLoader initialization. |
| **Impact** | 10-snapshot trajectories (failed early, t_final=9.5 by luck) can enter training. Lyapunov time needs 200+ snapshots — 10-snapshot trajectories break Stage 4+ assignment. |
| **Fix** | Insert `TrajectoryValidator` at DataLoader init: enforce `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0-3, AND `final_timestep >= 9.5`. Log rejections explicitly. |

### B-07: Batch Construction — No Replay/Lookahead Split
| Field | Detail |
|-------|--------|
| **Issue** | PINN `get_batch()` implements flat batch (256 random trajectories). CTL requires 240 replay (stages <=k) + 16 lookahead (stage k+1). |
| **Location** | main_pinn.pdf Sec 3.1; main_CTL.pdf Sec 5.3.2; author note: "[Comment: This above batch construction is not consistent with the CTL instruction plan]" |
| **Root Cause** | PINN doc drafted before CTL batch spec finalized; never reconciled. |
| **Impact** | No replay = catastrophic forgetting of earlier stages. No lookahead = abrupt stage transitions, training instability. |
| **Fix** | Two-phase sampler: (1) `B_replay=240` from cumulative `D_<=k`, (2) `B_lookahead=16` from `D_{k+1}`, (3) Per trajectory: n_pts=32 with 50/50 uniform/acceleration-weighted. See pseudo-code in Section 6. |

### B-08: Data-Fidelity vs. Collocation Points Conflated
| Field | Detail |
|-------|--------|
| **Issue** | CTL describes "sampling time points from Brutus trajectories" without separating data-fidelity points (must match ground truth) from physics collocation points (anywhere in [0,T]). |
| **Location** | main_CTL.pdf Sec 5.3.2; main_pinn.pdf Sec 3.2 |
| **Root Cause** | CTL omits collocation point concept entirely. PINN has collocation sampling but doesn't reconcile with CTL batch spec. |
| **Impact** | If physics loss only evaluated at Brutus snapshot times, network cannot learn correct behavior between snapshots — defeats PINN's key generalization capability. |
| **Fix** | Define TWO independent point sets: (a) Data-fidelity points from Brutus snapshots (L1 loss vs. r_true), 8192 points; (b) Collocation points anywhere in [0,T] (physics residual + energy loss), 4096 points. Both use 50/50 uniform/weighted time sampling but are sampled independently. |

### B-09: Softening Parameter Mismatch by 10^5x
| Field | Detail |
|-------|--------|
| **Issue** | CTL uses epsilon=1e-10 for invariant E (stage assignment). PINN uses epsilon_soft=1e-5 for physics residual and energy loss. |
| **Location** | main_CTL.pdf Sec 4.4; main_pinn.pdf Sec 3.2, 3.3 |
| **Root Cause** | Two documents chose softening independently without coordination. |
| **Impact** | Energy loss penalizes deviation from H_0(eps=1e-5), but curriculum gates on E(eps=1e-10). For r ~ 0.001, potential differs by 1%. Stage assignment uses different physics than training. |
| **Fix** | Unify at **epsilon = 1e-8**. Error at r=0.001 is 0.01% (acceptable). Prevents division-by-zero for all r > 1e-8. Recompute ALL H_0 and ALL stage assignments after change. |

### B-10: Dynamic omega0 Scheduling Has No Runtime Effect
| Field | Detail |
|-------|--------|
| **Issue** | `update_omega0()` decays first_omega0 from 30 to 10 over epochs, but omega0 is used ONLY at weight initialization. Changing it post-init doesn't affect weights. |
| **Location** | main_pinn.pdf Sec 2.2, Listing 1; author note: "[Need more detail on this dynamic scheduling...]" |
| **Root Cause** | Fundamental misunderstanding of SIREN initialization. omega0 controls the frequency scaling BAKED INTO weight magnitudes at init time. |
| **Impact** | Entire scheduling function is a no-op. Adds complexity with zero benefit. Confuses stage-based curriculum with epoch-based scheduling. |
| **Fix** | **Remove the scheduling function.** Use fixed first_omega0=30, hidden_omega0=1. If cross-stage re-initialization is desired, document it explicitly as a separate architectural decision. |

### B-11: Non-Contiguous IDs Break Curriculum Mapping
| Field | Detail |
|-------|--------|
| **Issue** | Standard dataset: 1,250 gaps out of 4,000 (31.2% gap rate). Hierarchical: 143/5,000 (2.9%). CTL assumes ID == array index. |
| **Location** | README.md lines 148-153; main_CTL.pdf Stage assignment logic |
| **Root Cause** | Gaps from generation continuation, prescreen rejection, problematic IC moves. Linear indexing ignores them. |
| **Impact** | Stage assignment via dense array indexing produces 45.5% wrong mappings in standard dataset. Network trains on Stage-k data labeled as Stage-j, destroying curriculum progression. |
| **Fix** | Build `id_to_path` dictionary mapping from actual on-disk filenames at DataLoader init. Never assume ID == index. `TrajectoryIndex` class with `get_by_id(file_id)` method. |

---

## 2. MAJOR INCONSISTENCIES & GAPS

| # | Conflict | Docs Involved | Resolution Strategy |
|---|----------|---------------|---------------------|
| **M1** | Input vector: CTL assembles 11D IC (masses + 5 invariants + 3 shape invariants). PINN expects 13D IC (masses + 5 invariants + 5 trigonometric values). | main_CTL.pdf Sec 4.5 vs main_pinn.pdf Table 2 | Adopt PINN's 13D IC as architecture contract. Replace shape invariants (I_1,I_2,I_3) with 5 trigonometric values in CTL. Update Listing 8. |
| **M2** | Total dimension: 12D (CTL title+Sec 5.1.1), 13D (CTL "13-component IC"), 14D (CTL closing note, PINN). No consistent count. | main_CTL.pdf (internal) vs main_pinn.pdf | Adopt **14D** as canonical: [t', IC_13D]. Fix ALL references in both docs. There is no mathematically consistent 12D or 13D count. |
| **M3** | Scaling order: CTL scales in Step 2, then COM-transforms in Step 2.5. For hierarchical ICs with |COM|~0.01, scaled COM offset survives at ~0.002. | main_CTL.pdf Sec 4.2 vs Sec 4.3 | **COM transform FIRST, then scale.** Scaling preserves non-zero COM. Reorder: raw COM -> scale -> verify. |
| **M4** | Constraint counting error: "13 constraints for an 8-dimensional reduced phase space" — but 18-13=5 != 8. Correct: 18 - 3(COM) - 3(P) - 3(SO(3)) = 9 DOF. | main_CTL.pdf Sec 4.5 "Mathematical Guarantees" | Correct to: "9 constraints reduce 18-DOF phase space to 9 dimensions. The scalar invariants project onto this reduced space." |
| **M5** | I_3 claimed "already in [-1,1]" but formula gives I_3 in [0,1]. Triangle inequality guarantees d_s+d_m >= d_l, so I_3 >= 0. | main_CTL.pdf Listing 7 | Apply I3_norm = 2*I3 - 1 to map [0,1] to [-1,1]. Equilateral gives I3_norm = -1/3. |
| **M6** | L_norm lacks clamping — values >1 possible numerically, producing L_norm_normalized > 1. | main_CTL.pdf Listing 7 | Add `np.clip(L_norm, 0, 1)` before 2*x-1 mapping. |
| **M7** | Lyapunov time tau_L computed in CTL Sec 4.4 but dropped from IC vector assembly in Sec 4.5. No decision documented. | main_CTL.pdf Sec 4.4 vs 4.5 | **Exclude tau_L from IC vector** by design (it's a derived dynamical property, not an IC invariant). Document justification. Use only for stage gating. |
| **M8** | LayerNorm on skip path attributed to SQR-SkipResNet paper, but original paper (arXiv:2310.15690v2) has NO LayerNorm anywhere. | main_pinn.pdf Sec 2.3 | Re-attribute as **author modification** (acceptable if justified). Do NOT cite as from SQR-SkipResNet paper. |
| **M9** | E_norm only uses [-1, 0) — positive half of input range never used since E < 0 for bound systems. | main_CTL.pdf Listing 7 | Acceptable for SIREN (no dead neurons). Document that positive range is unused. Monitor training; consider `E_norm_shifted = 2*tanh(E/E_scale) + 1` if underutilization detected. |
| **M10** | m_norm range asymmetric for hierarchical masses: [-0.93, 0.585] not centered on 0. | main_CTL.pdf Sec 4.5 | Acceptable but document. The asymmetry carries information about mass hierarchy. |
| **M11** | Blacklist (`problematic_ics_blacklist.json`, 65 IDs) not loaded by current runners. | README.md line 1011 | Load blacklist in DataLoader `__init__` and exclude blacklisted IDs. Log exclusion count. |
| **M12** | Standard trajectories (dt_out=0.17, ~59 snapshots) cannot support 32 points/trajectory (54% sampling ratio). | README.md dt_out table; main_CTL.pdf Sec 5.3.2 | Adaptive cap: `n_pts = min(32, int(0.5 * n_snapshots))`. For standard: 29 points. |
| **M13** | 184 standard IDs have no gold counterpart — Stage 5 training data incomplete. | README.md line 182; main_CTL.pdf Stage 5 | Check gold counterpart existence before Stage 5 assignment. Skip to Stage 6 if no gold data, or use low-fidelity standard fallback with warning flag. |
| **M14** | Gradient clipping spec divergence: PINN uses median-based adaptive; CTL uses curriculum-aware C schedule. | main_pinn.pdf Sec 4.3; main_CTL.pdf Sec 5.3.3 | **Merge both**: `clip_value = C_stage * median(grad_norm_history)`, where C_stage from CTL schedule and median from PINN rolling window. |
| **M15** | Energy loss lambda_E=1000 at Stage 6 risks overwhelming physics and data terms by 100-5000x. | main_CTL.pdf Table 3; main_pinn.pdf Sec 3.3 | Implement hybrid capped schedule: `lambda_E(k) = min(10^(k-3), cap[k])` where cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}. Add safeguard: if `lambda_E * L_energy > 10 * L_data`, warn and reduce. |
| **M16** | `dt_out` varies 17x across datasets (0.01 to 0.17) but collocation density is uniform. | README.md; main_pinn.pdf Sec 3.2 | Collocation density should be proportional to temporal resolution. Use `n_col_per_traj = base_n_col * (dt_base / dt_out)` for data-aware density. |

---

## 3. DESIGN AMBIGUITIES & UNRESOLVED QUESTIONS

| # | Question | Context | Proposed Experiment/Decision Path |
|---|----------|---------|-----------------------------------|
| **D1** | What exactly are the 3 angles for trigonometric encoding? | PINN Table 2 mentions "5 values for 3 trigonometrically encoded angles" but never defines them. | **Proposed**: (theta_L, phi_L) = spherical coords of L_hat = L/|L|; gamma_orb = orbital phase of body 1 in orbital plane. Encoding: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]`. **Experiment**: Compute on 100 sample ICs; verify smooth distributions and span. |
| **D2** | Does LayerNorm on skip path actually help? | Original SQR-SkipResNet has no LayerNorm. Gradient explosion source is physics loss (1/r^3), not skip connections. | **Ablate**: Train with/without skip-path LayerNorm. Monitor: max gradient norm per layer, activation histograms, training stability. If no benefit, remove. |
| **D3** | LayerNorm `affine=True` or `affine=False`? | `affine=True` adds learnable scale/shift that could interfere with SIREN's carefully designed frequency spectrum. | **Default `affine=False`** (safer). Ablate if needed. LayerNorm's purpose is normalization, not feature transformation. |
| **D4** | Should quasi-random IC Brutus outputs get COM-corrected? | CTL says skip unless verification fails. Float64 parsing may introduce O(1e-16) drift. | **Experiment**: Parse 100 quasi-random trajectories. Compute |COM| and |P| at final snapshot. If drift > 1e-12, apply lightweight COM correction. Otherwise skip (document threshold). |
| **D5** | How should stage transition criteria work with limited data? | Author acknowledged: "All of this transition criteria is theoretical now... limited training data, maybe not even enough." | **Pilot Stage 0 first.** Define minimal success: data loss < 1e-3, physics loss < 1e-2. Calibrate thresholds empirically. Treat Sec 5.5 criteria as hypotheses, not fixed rules. Use relaxed criteria + max-epochs fallback (see Section 6). |
| **D6** | How to handle Brutus mass drift between snapshots? | Brutus arbitrary-precision arithmetic should preserve masses exactly, but text output may round. | **Experiment**: Parse 1000 IC-Brutus pairs. Compare m_IC vs m_Brutus_t=0 with `np.allclose(rtol=1e-15)`. If mismatch: use `decimal.Decimal` for mass parsing. If match: document IC masses as canonical. |
| **D7** | What tolerance for 219 standard gold files with minimal footers (no tol)? | README.md lines 620-628: 219 files lack tol in footer. Folder default is 1e-13 but 592 files have 1e-14. | Use folder-level default 1e-13. Add `tol_confidence` flag: 'direct' (footer has tol) vs 'inferred' (minimal footer). Log count of inferred tolerances. |
| **D8** | Should s_min use softening for Stage 6 collision criterion? | CTL says s_min is "true pairwise separations (no softening)". But for r_ij < epsilon, geometric and softened separations differ. | **Decision**: Keep s_min unsoftened (measures actual physical separation). Add floor: `s_min_eff = max(s_min, epsilon)` for collision criterion to avoid flagging numerical noise. |
| **D9** | Is the orientation representational gap fatal? | Input vector has only rotationally invariant scalars. Network outputs absolute 3D positions. Without orientation angles, network cannot know spatial orientation. | The trigonometric encodings (D1) resolve this IF they encode L_hat direction and orbital phase. **Verify**: Train a small MLP to reconstruct absolute positions from (IC_13D, t). If MSE < 1e-4, encoding is sufficient. If not, expand to 17D by adding I_1,I_2,I_3 back. |
| **D10** | Can training start with standard SIREN init while D formula is being fixed? | D fix requires recomputing all scaled quantities and stage assignments — significant pipeline work. | **Yes, partially.** Use D=6.694 (correct) from day one to avoid retraining. If D=4.64 or 10 used temporarily, ALL training must be restarted after D fix. Priority P0. |

---

## 4. AUTHOR-FLAGGED UNCERTAINTIES — RESOLUTION STATUS

Out of **28 flagged items** found across all three documents:

| Severity | Count | Blocking? |
|----------|-------|-----------|
| CRITICAL | 8 | 7 blocking |
| MAJOR | 10 | 3 blocking |
| MINOR | 6 | 0 blocking |
| INFO | 4 | 0 blocking |
| **Total** | **28** | **10 blocking** |

### Priority Resolution Queue

| Priority | Item | Document | Resolution |
|----------|------|----------|------------|
| **P0** | COM frame violation (#2) | main_CTL.pdf Sec 4.3 | Fix: COM-first ordering, unified transformer. See B-05. |
| **P1** | SIREN init incorrect (#13) | main_pinn.pdf Sec 2.2 | Fix: divide by omega0. See B-01. |
| **P2** | Batch construction inconsistency (#14) | main_pinn.pdf Sec 3.1 | Fix: two-phase replay/lookahead. See B-07. |
| **P3** | Training loop data flow (#8) | main_CTL.pdf Sec 5 | Fix: write end-to-end data-flow spec. See Section 6. |
| **P4** | Canonical ordering details (#3) | main_CTL.pdf Sec 4.5 | Fix: document decision tree with quaternary tie-breaker. |
| **P5** | Mathematical guarantees (#7) | main_CTL.pdf Sec 4.5 | Fix: correct constraint counting to 9D. Verify injectivity with peer review. |
| **P6** | Stage transition criteria (#9) | main_CTL.pdf Sec 5.5 | Fix: pilot Stage 0, calibrate empirically. See D5. |
| **P7** | Suspicious paragraphs (#5) | main_CTL.pdf Sec 4.4 | Fix: independent verification of inertia/shape invariant derivations. |
| **P8** | Omega_0 scheduling (#11) | main_pinn.pdf Sec 2.2 | Fix: remove scheduling, use fixed omega0=30. See B-10. |
| **P9** | IC data scan suggestion (#1) | main_CTL.pdf Sec 2.3 | Run descriptive stats on all 15,028 ICs; derive data-driven stage thresholds. |

---

## 5. CORRECTED INPUT VECTOR SPECIFICATION

### 5.1 Final Input Vector: 14 Dimensions

```
Input = [t', m_norm(3), E_norm, L_norm_norm, Q_norm, s_min_norm, I_norm, trig_vec(5)]
        = [1D  + 3D      + 1D    + 1D         + 1D    + 1D         + 1D    + 5D      ]
        = 14D
```

### 5.2 Component Specifications

| Component | Dim | Normalization | Formula | Range |
|-----------|-----|---------------|---------|-------|
| t' | 1 | `2*t/T_max - 1` | T_max = 10 | [-1, 1] |
| m_norm | 3 | `2*(m_i/m_total) - 1` | m_total = sum(m_i) | [-0.93, 0.585] (hier); [-1/3, -1/3] (equal) |
| E_norm | 1 | `tanh(E / E_scale)` | E_scale = |median(E)| | [-1, 0) — **document** |
| L_norm_norm | 1 | `2*clip(L/L_max, 0, 1) - 1` | L_max = M_tot * r_char * v_char | [-1, 1] |
| Q_norm | 1 | `tanh((Q - 1) / 0.5)` | Q_scale = 0.5 (fixed) | ~[-0.54, 0.54] |
| s_min_norm | 1 | `tanh(s_min / s_min_scale)` | s_min_scale = median(r_char) | [0, 1) |
| I_norm | 1 | `tanh(I_trace / (M_tot * r_char^2))` | I_trace = tr(sum_i m_i * (||r'||^2 * I - r'(r')^T)) | [-1, 1] |
| trig_vec | 5 | `[sin(tL), cos(tL), sin(pL), cos(pL), sin(gO)]` | tL=theta_L, pL=phi_L, gO=gamma_orb | Each in [-1,1] |

### 5.3 Trigonometric Angle Computation (NEW — missing from CTL)

```python
# After canonical ordering, compute angular momentum direction
L_vec = sum(m[i] * cross(r_prime[i], v_prime[i]) for i in range(3))
L_hat = L_vec / (norm(L_vec) + 1e-10)

# Polar and azimuthal angles of L_hat
theta_L = arccos(clip(L_hat[2], -1, 1))   # [0, pi]
phi_L = arctan2(L_hat[1], L_hat[0])        # [0, 2*pi)

# Orbital phase: project r'_1 (heaviest body) onto orbital plane
r1 = r_prime[0]  # after canonical ordering
r1_perp = r1 - dot(r1, L_hat) * L_hat
# Reference direction in orbital plane
if abs(L_hat[2]) < 0.99:
    e_ref = cross(L_hat, [0, 0, 1])
else:
    e_ref = cross(L_hat, [1, 0, 0])
e_ref = e_ref / (norm(e_ref) + 1e-10)
e_ref_perp = cross(L_hat, e_ref)
gamma_orb = arctan2(dot(r1_perp, e_ref_perp), dot(r1_perp, e_ref))

trig_vec = [sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]
```

### 5.4 Canonical Ordering (Corrected — with Quaternary Tie-Breaker)

```python
def canonical_ordering(m, r_prime, v_prime):
    """
    Total ordering with guaranteed determinism.
    Primary: -mass (descending)
    Secondary: |r'| (ascending)  
    Tertiary: |v'| (ascending)
    Quaternary: x, y, z (lexicographic — deterministic tie-breaker)
    """
    keys = []
    for i in range(3):
        key = (-m[i], norm(r_prime[i]), norm(v_prime[i]),
               r_prime[i][0], r_prime[i][1], r_prime[i][2])
        keys.append(key)
    
    idx = sorted(range(3), key=lambda i: keys[i])
    return m[idx], r_prime[idx], v_prime[idx]
```

### 5.5 Removed Components (vs. CTL original)

- **I_1, I_2, I_3 (shape invariants)**: Replaced by trig_vec which encodes orientation. Shape information is partially recoverable from (s_min, Q, I_norm) combination.
- **tau_L (Lyapunov time)**: Excluded by design — derived dynamical property, not IC invariant.

---

## 6. UNIFIED BATCH CONSTRUCTION SPECIFICATION

### 6.1 Design Principles

1. **Two independent point sets**: Data-fidelity (Brutus snapshots, L1 loss) and collocation (anywhere in [0,T], physics+energy loss)
2. **Replay/lookahead trajectory split**: 240 replay + 16 lookahead per CTL
3. **Mixed time sampling**: 50% uniform + 50% acceleration-weighted for BOTH data and collocation points
4. **Per-trajectory collocation**: Each of 256 trajectories gets 16 collocation points

### 6.2 Complete Training Step Pseudo-Code

```python
def training_step(dataset, model, stage, optimizer, lambda_p, mu_p, v_p):
    # ---- STEP 1: Trajectory batch (CTL Sec 5.3.2) ----
    B_replay, B_lookahead = 240, 16
    replay_trajs = dataset.sample_replay(n=B_replay, max_stage=stage)
    if dataset.has_stage(stage + 1):
        lookahead_trajs = dataset.sample_lookahead(n=B_lookahead, stage=stage+1)
        batch_trajs = replay_trajs + lookahead_trajs
    else:
        batch_trajs = replay_trajs
    
    # ---- STEP 2: Data-fidelity points (50/50 sampling) ----
    t_data, r_true, ic_data = [], [], []
    for traj in batch_trajs:
        times, positions = traj['times'], traj['positions']  # Brutus snapshots
        n_u, n_w = 16, 16  # 50/50 split of 32 points
        idx_u = np.random.choice(len(times), n_u, replace=False)
        acc_norms = np.abs(traj['accelerations']).max(axis=1)
        weights = acc_norms / acc_norms.sum()
        idx_w = np.random.choice(len(times), n_w, p=weights, replace=False)
        idx = np.concatenate([idx_u, idx_w])
        t_data.extend(2.0 * times[idx] / T_max - 1.0)  # normalize to [-1,1]
        r_true.extend(positions[idx].reshape(-1, 9))
        ic_data.extend(np.tile(traj['ic_vector'], (32, 1)))
    
    # ---- STEP 3: Collocation points (separate, 50/50) ----
    n_col_per_traj = 16  # 4096 / 256
    t_col, ic_col, H0_col = [], [], []
    for traj in batch_trajs:
        n_u, n_w = n_col_per_traj // 2, n_col_per_traj - n_col_per_traj // 2
        t_u = np.random.uniform(-1, 1, size=n_u)
        acc_norms = np.abs(traj['accelerations']).max(axis=1)
        weights = acc_norms / acc_norms.sum()
        t_w_phys = np.random.choice(traj['times'], size=n_w, p=weights)
        t_w = 2.0 * t_w_phys / T_max - 1.0
        t_col.extend(np.concatenate([t_u, t_w]))
        ic_col.extend(np.tile(traj['ic_vector'], (n_col_per_traj, 1)))
        H0_col.extend(np.full(n_col_per_traj, traj['H_0']))
    
    # ---- STEP 4: Forward passes ----
    # Data fidelity
    input_data = torch.cat([tensor(t_data).unsqueeze(-1), tensor(ic_data)], dim=-1)
    r_pred_data = model(input_data)
    L_data = torch.mean(torch.abs(r_pred_data - tensor(r_true)))
    
    # Physics + Energy (collocation)
    input_col = torch.cat([tensor(t_col).unsqueeze(-1), tensor(ic_col)], dim=-1)
    t_col_req = tensor(t_col, requires_grad=True)  # for autodiff
    r_pred_col = model(torch.cat([t_col_req.unsqueeze(-1), tensor(ic_col)], dim=-1))
    L_physics = compute_physics_residual(t_col_req, r_pred_col, tensor(ic_col))
    L_energy = compute_energy_loss(r_pred_col, tensor(H0_col))
    
    # ---- STEP 5: Total loss with ALM ----
    lambda_E = get_lambda_E(stage)  # capped hybrid schedule
    L_total = L_data + lambda_p * L_physics + (mu_p / 2.0) * L_physics**2 + lambda_E * L_energy
    
    # ---- STEP 6: Backprop + ALM update ----
    optimizer.zero_grad()
    L_total.backward()
    C = get_clip_c(stage)  # curriculum-aware C
    clip_grad_norm_(model.parameters(), C * median(grad_norm_history))
    optimizer.step()
    
    # ALM parameter update (excluded from autograd)
    with torch.no_grad():
        lambda_p += mu_p * L_physics.item()
        v_p = 0.99 * v_p + 0.01 * (L_physics.item() ** 2)
        mu_p = 0.01 / np.sqrt(v_p + 1e-8)
        mu_p = np.clip(mu_p, 1e-4, 100.0)
```

### 6.3 Stage Transition Criteria (Practical Fallbacks)

```
ADVANCE when EITHER:

PATH A (Strict — all four met):
    A1. Training plateau: |L_smooth(i) - L_smooth(i-200)| / L_smooth(i) < 1e-5
    A2. Validation stable: L_val(i) <= percentile_10(val_history)  [relaxed from min]
    A3. Physics residual: L_val_phys < epsilon_phys[stage]  [stage-dependent]
    A4. Energy drift: avg |H(t_final) - H(0)| / |H(0)| < epsilon_energy[stage]

PATH B (Fallback — any trigger):
    B1. MAX_EPOCHS reached: {0:500, 1:600, 2:700, 3:800, 4:900, 5:1000, 6:1200}
    B2. Stagnation: no val improvement >1% for 400 epochs
    B3. NaN/Inf: rollback to last checkpoint, LR *= 0.5, retry

Stage-dependent thresholds:
    Stage | epsilon_phys | epsilon_energy
    ------|-------------|---------------
    0     | 5e-3        | 5e-3
    1     | 2e-3        | 2e-3
    2     | 1e-3        | 1e-3
    3     | 5e-4        | 5e-4
    4     | 2e-4        | 2e-4
    5-6   | 1e-4        | 1e-4
```

### 6.4 Energy Loss Weight (Capped Hybrid Schedule)

```python
def get_lambda_E(stage, L_energy_current=None):
    """Stage-dependent energy weight with adaptive soft cap."""
    base = 10 ** (stage - 3)
    cap_table = {0: 1.0, 1: 5.0, 2: 20.0, 3: 50.0, 4: 100.0, 5: 200.0, 6: 500.0}
    lambda_E = min(base, cap_table[stage])
    if L_energy_current is not None and L_energy_current < 0.01:
        lambda_E *= 0.5  # Reduce if already well-conserved
    return lambda_E
```

---

## 7. IMPLEMENTATION CHECKLIST

### Phase 0: Pre-Implementation Blockers (DO NOT CODE UNTIL COMPLETE)

- [ ] **P0-1**: Fix D formula to `D = (G*M_tot*T^2)^(1/3) = 6.694` in BOTH documents
- [ ] **P0-2**: Fix SIREN hidden init to divide by omega0, not multiply
- [ ] **P0-3**: Decide on and document 14D input vector with 13D IC including trig_vec
- [ ] **P0-4**: Write trigonometric angle encoding specification (5 values for 3 angles)
- [ ] **P0-5**: Implement unified COM transformer (COM-first, then scale, single function for ICs + Brutus)
- [ ] **P0-6**: Unify softening to epsilon = 1e-8 everywhere; recompute ALL H_0 and stage assignments
- [ ] **P0-7**: Write end-to-end data-flow spec answering author's "biggest question"

### Phase 1: Data Pipeline Hardening

- [ ] **P1-1**: Implement `TrajectoryValidator` gate between Stage 4 and Stage 5
- [ ] **P1-2**: Build `TrajectoryIndex` with `id_to_path` dictionary for non-contiguous IDs
- [ ] **P1-3**: Load and enforce `problematic_ics_blacklist.json` in DataLoader
- [ ] **P1-4**: Add adaptive `points_per_trajectory = min(32, int(0.5 * n_snapshots))`
- [ ] **P1-5**: Add gold counterpart check before Stage 5 assignment
- [ ] **P1-6**: Implement `COMFrameTransformer` with mass consistency assertion
- [ ] **P1-7**: Add quaternary tie-breaker to canonical ordering for deterministic total ordering

### Phase 2: Architecture Fixes

- [ ] **P2-1**: Replace SIREN init formula in code (Table 1 fix)
- [ ] **P2-2**: Remove dynamic omega0 scheduling; use fixed first_omega0=30, hidden_omega0=1
- [ ] **P2-3**: Add `affine=False` default to LayerNorm; ablate vs. True
- [ ] **P2-4**: Add comment that skip-path LayerNorm is author modification, not from SQR-SkipResNet paper

### Phase 3: Training Loop Implementation

- [ ] **P3-1**: Implement two-phase replay/lookahead batch construction
- [ ] **P3-2**: Separate data-fidelity and collocation point sampling (two independent sets)
- [ ] **P3-3**: Add `strategy='mixed'` to collocation sampler (50/50 uniform/weighted)
- [ ] **P3-4**: Implement merged gradient clipping: `C_stage * median(grad_norm_history)`
- [ ] **P3-5**: Add mu_p clamping [1e-4, 100] to ALM update
- [ ] **P3-6**: Implement capped hybrid energy weight schedule
- [ ] **P3-7**: Implement stage-dependent transition criteria with max-epochs fallback
- [ ] **P3-8**: Run Stage 0 pilot; calibrate thresholds empirically

### Phase 4: Verification & Documentation

- [ ] **P4-1**: Re-run stage assignment for all ~15K trajectories with corrected D and epsilon
- [ ] **P4-2**: Verify all IC vector components in [-1,1] with bounds-checking unit test
- [ ] **P4-3**: Run COM verification on 100 quasi-random + 100 hierarchical samples
- [ ] **P4-4**: Verify injectivity claim with peer review or symbolic check
- [ ] **P4-5**: Ablate skip-path LayerNorm (with/without)
- [ ] **P4-6**: Document all resolved ambiguities and final design decisions

---

## 8. CROSS-ISSUE INTERACTION MATRIX

| Interaction | Issues | Description | Severity |
|-------------|--------|-------------|----------|
| D + epsilon + COM | B-02, B-05, B-09 | Incorrect D corrupts scaled positions; COM transform order affects whether offsets survive; softening mismatch changes potential at close encounters | **Critical** |
| D + curriculum | B-02, B-09 | Stage assignment thresholds in scaled units. Wrong D + wrong epsilon = wrong stages for systems near boundaries. | **Critical** |
| Input vector dimension | B-03, B-04, M1, M2 | Dimension conflict blocks coding; missing trig values means no orientation info; all must be resolved together. | **Critical** |
| Batch + collocation | B-07, B-08 | Replay/lookahead is trajectory-level; collocation is point-level. Both must be implemented together for consistent training. | **Major** |
| SIREN init + omega0 schedule | B-01, B-10 | Init formula must be fixed BEFORE deciding on omega0 strategy. Removing scheduling simplifies the init fix. | **Major** |
| COM + mass consistency | B-05, B-11 | COM transform requires consistent masses. Blacklist filtering must happen before COM computation. | **Major** |
| Stage criteria + limited data | B-08, D5 | Transition criteria depend on validation loss being meaningful, which requires enough data. Max-epochs fallback prevents infinite loops. | **Major** |
| Precision + softening | D4, B-09 | Float64 precision sufficient with epsilon=1e-5. If epsilon reduced below 1e-10, arbitrary precision parsing needed. | **Minor** |

---

## 9. QUANTITATIVE IMPACT SUMMARY

| Fix | Quantities Affected | Impact if Unfixed |
|-----|--------------------|--------------------|
| D = 6.694 (not 4.64 or 10) | E_scaled, L_norm, Q, V, all normalized inputs | E_scaled off by 75%, L_norm off by 77%. Stage misassignment for ~15% of trajectories near boundaries. |
| epsilon = 1e-8 unified | V_soft, H_0, E_stage, physics residual, energy loss | 1% error in potential at r=0.001. Stage flips for close-encounter systems. |
| COM-first ordering | All hierarchical trajectory targets (4,857 trajectories) | COM offset ~0.002 in scaled units. Network learns from wrong reference frame. |
| 14D input vector | First Linear layer weight matrix | Cannot allocate [14, 512] vs [12, 512]. Runtime dimension mismatch. |
| Trig_vec added | Network's ability to predict absolute positions | No orientation info = cannot predict 3D positions in fixed frame. |
| Replay/lookahead | Curriculum progression across 7 stages | Catastrophic forgetting. Stage 6 network forgets Stage 0-1 data. |
| Separate collocation | Physics generalization between snapshots | Physics only enforced at data points = poor interpolation between snapshots. |
| SIREN init fix | Activation variance through 12 layers | At omega0=30, 810,000x variance explosion = instant NaN. |
| Stage criteria fix | Training time, curriculum effectiveness | Infinite loop without fallback. 7000+ epochs theoretically. |

---

*End of Comprehensive Technical Audit Report*

*Generated: 2026-04-27 | Methodology: 6 parallel thematic audits + cross-validation synthesis*
