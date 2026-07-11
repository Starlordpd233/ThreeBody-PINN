---
title: CTL-PINN Pre-Build Audit — Consolidated Master Resolution
status: candidate (owner disposes)
scope: project
purpose: consolidation of three independent external audit reports into one master resolution
created: 2026-07-07
inputs: chatgpt-FINAL-RESOLUTION.md, gemini-FINAL-RESOLUTION.md, glm-FINAL-RESOLUTION.md
audit_prompt: RESEARCH-AGENT-PROMPT-STORM.md
---

# CTL-PINN Pre-Build Audit — Consolidated Master Resolution

**What this document is.** Three external research agents (ChatGPT, Gemini, GLM) independently executed the STORM pre-build audit defined in `RESEARCH-AGENT-PROMPT-STORM.md` §7 against the same seven project files. This document consolidates their three reports into one master resolution. Consolidation was **verification-based**: every proven problem claimed by any report was re-checked against the attached sources before admission, every conflict between reports was adjudicated with the quoted text, and findings that failed verification were rejected with reasons (Part 0). The result follows the §7 report shape so it can stand in for the individual reports as the audit of record.

**Inventory of the seven project files** (all consolidated findings were re-verified against these): `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `v2.0-build-plan.md`, `trainex-r1a-resolution-doc.md`, `RATIFICATION.md`, `DATASET-CONTEXT.md`.

**Numbering.** Master IDs `IR2-001..IR2-008` are assigned fresh, worst-first, per the §7 schema. The cross-walk in Part 0 maps every master ID to its source-report ID(s).

---

## Part 0 — Consolidation record

### 0.1 Cross-walk: master findings ↔ source reports

| Master ID | Finding (short) | ChatGPT | Gemini | GLM | Verification outcome |
|---|---|---|---|---|---|
| IR2-001 | Stage 0/1 `s_min > 2` criterion geometrically unsatisfiable → Stages 0–2 empty | — (missed) | — (missed) | IR2-002 | **Verified** (derivation re-run; sample-IC distances recomputed; blast radius extended to Stages 1a/1b/2 — see finding) |
| IR2-002 | Build plan NET-04 specifies three-term L1/MAE loss vs the locked five-term Huber contract | IR2-001 | — (missed) | IR2-001 | **Verified** (both quotes exact; severity rationale corrected — see finding) |
| IR2-003 | Build plan DATA-05 misdescribes replay/lookahead vs data/collocation point sets and 50/50 sampling | IR2-002 (Serious, must-fix) | — (missed) | IR2-005 (Minor) | **Verified**; severity adjudicated Serious/must-fix-first (see 0.2-c) |
| IR2-004 | Train/val/test split not grouped by `physical_key` → base/gold leakage risk | IR2-003 (must-fix) | — (missed) | — (missed) | **Verified** (spec and plan silent on grouping; dataset verifiably contains base/gold twins); severity adjudicated handle-with-a-condition (see 0.2-d) |
| IR2-005 | `ctl_instruction.md` dataset table swaps Set 1b / Set 2a counts vs Tier-1 verified counts | IR2-004 | — (missed; Part-5 row 17 marked MATCH) | IR2-003 | **Verified**; GLM's propagation analysis into the trainex-r1a memory arithmetic confirmed and its snapshot totals corrected by 100 (8,228,794, not 8,228,894) |
| IR2-006 | Build plan DATA-02 summarizes the Step-1A gate incompletely (omits conservation reject gate, blacklist, etc.) | — | — | IR2-004 | **Verified** (all seven clauses confirmed in spec) |
| IR2-007 | Step-3 `L_norm` code snippet silently ε-floors what the same section's contract says must carry a diagnostic flag | IR2-005 | — | — (marked Step 3 clean) | **Verified** (prose formula vs snippet compared line-by-line) |
| IR2-008 | Step-1A clause 2 still frames the 70-file DATA-05 quarantine as pending, vs Tier-1 "remediation executed, all quarantines lifted" | IR2-006 | — | — | **Verified with correction**: the clause is conditional ("until rerun validation … passes") and the condition is Tier-1-satisfied, so this is stale-text drift, not a mutual exclusion (see 0.2-e) |

### 0.2 Rejected and adjudicated items

**(a) Gemini IR2-001 (MPS double-backward "guaranteed fatal crash") — rejected as a proven problem; demoted to side-list SL-1.** The claim that missing `aten::linear_backward` second-order kernels on MPS "guarantees a fatal compilation abort" is (i) a library-behavior claim asserted for PyTorch 2.12 on citations that are not resolvable (Gemini's report has no Part 8 and its `[1]..[10]` markers point nowhere), and (ii) precisely the known-open item the ratification carves out: `trainex-r1a-resolution-doc.md` U-9 records "MPS double-backward kernel coverage for this net — Open until the §10.3 probe runs on-device with fallback **unset** (first build act)", with the fp64-CPU branch as the in-framework escape (D1-p, `RATIFICATION.md`). The audit prompt (§4) forbids flagging owner-carved items as defects. The legitimate residual — coverage must be measured — is the consolidated SL-1, where ChatGPT (SL-1) and GLM (SL-1) had already placed it.

**(b) Gemini IR2-002 (softening ↔ energy-loss "mathematical contradiction") — rejected: contradicted by the spec verbatim.** Gemini claims `L_E` "evaluates conservation drift against an unsoftened exact Newtonian formulation" while the physics loss uses the softened potential. `pinn_architecture.md` §3.4 states the opposite: "the analytic **matched-Plummer Hamiltonian** $H_\epsilon$ … is evaluated", "using the **same** $r_{safe,ij} = \sqrt{\lVert r'_j - r'_i\rVert^2 + \epsilon_{train}^2}$ as the residual force term", and "The same value $\epsilon_{train} = 10^{-5}$ is used consistently in both the physics residual and energy calculations"; the `compute_initial_energy` listing applies `epsilon_train` to $H_0$ as well, so numerator and denominator of $\Delta H_n$ are both matched-softened. Gemini's suggested fix describes what §3.4 already specifies. The one legitimate residual — training-ε vs validation-ε ($10^{-5}$ vs $10^{-10}$) drift can diverge at close encounters — is an empirical doubt, kept as consolidated SL-5 (GLM SL-5).

**(c) IR2-003 severity (ChatGPT Serious/must-fix vs GLM Minor) — adjudicated Serious / must-fix-first.** GLM's Minor rationale (the spec is authoritative; DATA-05 cites LOOP-01/02/03) is real, but the build plan's own verification protocol makes each requirement's success criterion the phase's acceptance test ("Numerically-defined acceptance per requirement"). A success criterion that itself encodes the wrong contract lets Phase 39 pass while violating the spec — the same defect class as NET-04, which both reports rated must-fix-first. GLM's supplementary arithmetic (data-fidelity draws from 240 + 16 = 256 trajectories; 256 × 32 = 8,192, so "240 replay, 8192 pts" is internally inconsistent) is adopted into the proof.

**(d) IR2-004 severity (ChatGPT must-fix-first) — adjudicated Serious / handle-with-a-condition.** The fix is a one-line invariant added to DATA-04 before Phase 39 (a roadmap tweak in the §5 sense); Phases 37–38 are unaffected, and within the Stage-0-only slice the trained/tested records are hierarchical-base only. The risk is nonetheless real and latent in the persistent manifest: Stage 2 explicitly re-uses "the *same* … hierarchical IC files used for **Stage 0** and **Stage 1**" at gold resolution (`ctl_instruction.md`, Stratification, Stage 2), so an ungrouped `record_key` split lets a physical system's base record land in train while its gold twin lands in val/test.

**(e) IR2-008 framing (ChatGPT "mutually exclusive states") — softened.** Step-1A clause 2 quarantines the 70 files "**until** rerun validation from the current canonical ICs passes", and `DATASET-CONTEXT.md` (Tier 1) verifies that validation passed (2026-06-11; "0 mismatches across all 15,028 pairs"; "All quarantines are lifted"). The spec's own condition is therefore satisfied — the two documents are not in contradiction; the spec text is stale in presentation (it reads as an active pending state) and should become a historical note. Minor.

**(f) Gemini IR2-003 (no adaptive loss balancing) — rejected as a proven problem; residual folded into SL-4.** The claim that the locked design provides "absolutely no mechanism" against term dominance mischaracterizes the specs: the physics residual carries residual-adaptive **causal weighting** ($w_n = \exp(-\eta_c \sum_{m<n}\mathrm{stopgrad}(\bar R_m))$, owner-ratified Option A, `pinn_architecture.md` §3.2/§4.1 — the Wang-et-al. causal-training mechanism its own citation recommends); the PHYS-05 warmup schedule ramps weights with per-stage caps $\lambda^{max} \le 1$; the conservation weights are $\lambda_E^{max} = \lambda_L^{max} = 0$ for stages 0–1 (no dominance possible in the viability slice); and LOSS-02 explicitly adjudicated automatic dominance reweighting as **deferred until measured weighted-loss/gradient evidence exists**, with the required instrumentation already ratified (B-2/B-10 widened log fields: five loss terms, λ vector, grad-norm, `w_n` stats). Gemini's recommended mitigation (log per-component gradient magnitudes in the Stage-0 pilot) is thus already locked in. The steelman requirement of the locked-decision challenge protocol was not met (it engages "static warmup", not the actual design). The legitimate empirical kernel — multi-term PINN loss dynamics must be watched — is consolidated SL-4.

**(g) Gemini IR2-004 (normalization constants un-invertible) — rejected: rests on an invented normalization scheme.** Gemini asserts un-normalization requires a per-trajectory "dynamic spatial scaling factor … defined as $\max(|r|)$". The spec scales by **global constants defined once across the entire dataset**: `T = t_max = 10`, `D = (G·T²)^(1/3) ≈ 4.6416`, `r' = r/D`, `v' = v/V`, `V = D/T` (`ctl_instruction.md` §2.5 "Global scaling"). Inversion needs only spec constants plus the ordered raw mass metadata the output-head contract already carries (`pinn_architecture.md` §5.3). The worked example ("$r_{max} \approx 10^{-5}$") is incompatible with the sampling envelope ($a_{inner} \ge 0.1$; pre-screen min distance 0.01). At most a documentation nicety remains (echo `D`, `T`, `V` in inference-output metadata); it is not recorded as a problem.

**(h) GLM internal inconsistency — corrected in IR2-001.** GLM's Part-4 note "(Stages 1–6 criteria checked: sound)" conflicts with its own finding: Stages 1a and 1b impose the identical `s_min > 2` criterion (`ctl_instruction.md` lines ~156, ~171), and Stage 2's criteria are "Union of Stage 0 and Stage 1 criteria". The consolidated finding carries the full blast radius (Stages 0, 1a, 1b, and 2 all unpopulatable as written).

**(i) GLM severity rationale for IR2-002 (loss) — corrected.** GLM argued the three-term loss would fail ACC-03 "because nothing in the three-term L1/MAE loss penalizes energy drift." Under the *correct* spec loss, $\lambda_E^{max} = \lambda_L^{max} = 0$ for stages 0–1 as well, so Stage-0 training has zero energy-loss weight either way; the finding's severity rests instead on (i) the Huber-vs-L1 mismatch, which bites immediately at Stage 0, (ii) the absent $L_E$/$L_L$ modules contradicting Phase 40's own TRAIN-03 (`λ_E^max ≤ 1` scheduled-weight module) and every stage ≥ 2, and (iii) a wrong acceptance criterion in a phase billed as "rebuilt from specs". Whether the ε_H gate is achievable at Stage 0 at all is a separate empirical question, added as SL-10.

### 0.3 Source-report quality assessment (consolidator's summary)

- **GLM — strongest report.** Fully §7-compliant (only report with a complete, date-stamped Part 8); every proven claim verified accurate on re-derivation; sole discoverer of the most consequential defect (IR2-001) with a correct steelman-flagged locked-decision challenge; correct carve-out discipline (MPS → side-list); deepest Part 6 register. Deductions: missed IR2-004 and IR2-007; the Part-4 internal inconsistency in 0.2-h; a 100-snapshot arithmetic slip (immaterial); an overstated severity rationale corrected in 0.2-i.
- **ChatGPT — solid second.** All six findings verified (two unique: IR2-004, IR2-007); correct carve-out discipline; complete report shape with resolvable sources. Deductions: missed IR2-001 entirely (marked the Stratification heading only with the count/L_norm issues); IR2-008 framing overstated; coverage-table and Part-5 entries thinner than GLM's.
- **Gemini — not reliable.** Two of four proven problems are contradicted by the spec text verbatim (0.2-b, 0.2-g); one flags an owner-carved item with unsupported certainty (0.2-a); one mischaracterizes the locked design and fails the steelman protocol (0.2-f). It missed every defect that survived verification, its Part 5 contains multiple factual errors (row 17 marked MATCH despite the seeded cross-check against `DATASET-CONTEXT.md`; an invented `1e-6` energy floor in row 13; "9-body continuous positions" in row 8; softening marked "absent" in `ctl_instruction.md` in row 9 despite Step 3's explicit `ε_inv = 1e-10` / `ε_train` cross-reference), and Part 8 is missing entirely, leaving all `[n]` citations unverifiable — a direct §7/§9 compliance failure. Its NO-GO verdict is reached, but on grounds that do not survive verification. Salvageable content: side-list-grade doubts (L-BFGS memory, SIREN aliasing, fp32 AD precision), all merged into SL-1/SL-3/SL-8.

---

## Part 1 — Verdict

**Recommendation: NO-GO — blocked on IR2-001, IR2-002, and IR2-003.** (Recommendation, not binding; the owner disposes.)

The locked foundation is largely sound — the SQR-SkipResNet-SIREN architecture, the PHYS-02 AD contract, the matched-Plummer dual-ε design, the Step-1A gate family, the curriculum state machine, and the ratified trainex-r1a engineering decisions all survive adversarial re-derivation. Three proven defects gate the build: **(1)** the Stage-0/1 stratification criterion `s_min > 2` is geometrically unsatisfiable by the frozen dataset's own sampling envelope, leaving Stages 0–2 empty and the viability slice with nothing to train on (IR2-001, a spec defect requiring an owner decision before Phase 39); **(2)** the build plan's Phase 38 success criterion specifies a superseded three-term L1/MAE loss where the locked specs require the five-term Huber catalog (IR2-002); and **(3)** the build plan's Phase 39 batch-constructor criterion inverts the locked data-fidelity/collocation contract (IR2-003). Two further Serious findings are handled with conditions (IR2-004 split grouping; IR2-005 dataset-table correction); three Minor findings are recorded (IR2-006..008). All three source reports independently recommended NO-GO; only the blockers above survive verification.

---

## Part 2 — Pre-build punch-list

Only decisions that gate a Serious finding appear here (fix-or-waive before the build starts).

### PB-1. Repair the `s_min > 2` stratification criterion so Stages 0–2 are populatable
- **Option A:** Replace the fixed threshold with a **data-derived criterion** ratified from the admitted-set `s_min` distribution (the Phase 39 DATA-06 Thrust-A scan already computes it; the spec's own author note in the Stratification section proposes exactly this data-first approach). Decide the *mechanism* now; ratify the value at the scan, mirroring how the other owner-carved thresholds work. — Trade-off: the concrete number lands mid-Phase-39 rather than today.
- **Option B:** Lower the threshold to a fixed safety floor in scaled code units (e.g. `s_min > 0.01`, matching the `MIN_DISTANCE_THRESHOLD = 0.01` pre-screening floor in `sampling_method.md` §4). Effectively neutralizes `s_min` as a discriminator and lets `E`, `L/L_max`, `Q` do the stratification. — Trade-off: simplest, but abandons the "well-separated" intent rather than re-deriving it.
- **Option C:** Redefine the gating `s_min` as the tertiary separation (inner-binary COM ↔ body 3), which *is* large for hierarchical triples. — Trade-off: matches the physical intent but forks the Step-3 invariant definition (dual-context `s_min`), which the Stage-6 Phase 33 contract deliberately avoided.
- **Source problems:** IR2-001.
- **Recommended:** **A** (with B as the interim default until the scan reports) — it preserves the criterion's intent, uses a mechanism the project already trusts for threshold calibration, and requires no second `s_min` definition.

### PB-2. Correct build-plan Phase 38 NET-04 to the locked loss contract
- **Option A:** Rewrite NET-04 to the five-term catalog: data Huber (δ_r = 1) + IC squared-error + causal physics + soft-energy Huber (δ = 1.0) + angular-momentum componentwise Huber (δ = 1.0), with PHYS-05 scheduled weights, per `pinn_architecture.md` §3/§4.1 and `ctl_instruction.md` "Loss Function Formulation". — Trade-off: none of substance; Phase 38 is billed as "rebuilt from specs".
- **Option B:** Keep the three-term wording as a smoke-only probe, explicitly prohibited as a training objective, with Phase 40 required to add the missing terms. — Trade-off: leaves a wrong-spec literal reading in a success criterion; high drift risk for a non-expert builder.
- **Source problems:** IR2-002.
- **Recommended:** **A** — a one-line transcription fix; Option B preserves a defect by fencing it.

### PB-3. Correct build-plan Phase 39 DATA-05 to the locked batch/collocation contract
- **Option A:** Rewrite DATA-05: the batch selects 240 replay + 16 lookahead (= 256) **trajectories**; data-fidelity points are drawn from those trajectories' snapshots at `n_pts = min(32, n_snapshots)` (~8,192 pts, provisional budget); collocation points are **continuous samples from [0, T]** (~4,096 pts, provisional), energy reusing the physics collocation set; the 50/50 uniform + acceleration-weighted sampler applies to **data-fidelity points only** (mixed continuous collocation remains deferred per LOOP-03). — Trade-off: none; it is what LOOP-01/02/03 already say.
- **Option B:** Unfreeze the spec to make lookahead a collocation-only mechanism and mandate 50/50 on collocation. — Trade-off: a spec-unfreeze with no rationale on record; contradicts the deliberate Phase 34 deferral.
- **Source problems:** IR2-003.
- **Recommended:** **A** — this is a build-plan transcription error, not a science choice.

### PB-4. Adopt `physical_key` as the split unit
- **Option A:** Add a split invariant to DATA-04: partition by `physical_key = (variant, id)` first, then expand each key to all its `record_key`s; assert no `physical_key` spans splits. — Trade-off: one invariant plus one assertion; slightly constrains per-stage split ratios.
- **Option B:** Split by `record_key` and record an explicit owner waiver that held-out metrics may be optimistic where base/gold twins straddle splits. — Trade-off: preserves the plan text at the cost of the acceptance gate's credibility for the full platform.
- **Source problems:** IR2-004.
- **Recommended:** **A** — the dataset verifiably contains base/gold realizations of the same ICs, and the spec's own blacklist contract already attaches exclusion semantics at `physical_key` granularity, confirming the intended unit.

### PB-5. Correct the `ctl_instruction.md` dataset table to the Tier-1 verified counts
- **Option A:** Swap the Set 1b / Set 2a count cells ("Set 1b (2749) Standard @ 0.17"; "Set 2a (4857) Hierarchical @ 0.01"), and note the propagation: the trainex-r1a corpus arithmetic built on the stale table (≈6.24 M snapshots ≈ 0.55 GB fp32) becomes ≈8.23 M snapshots ≈ 0.72 GB fp32 / 1.45 GB fp64 — still comfortably in-memory, so no ratified decision changes. — Trade-off: a spec edit, but of a demonstrably wrong empirical figure against Tier-1 facts.
- **Option B:** Leave the table and add a rule that all counts/roles come from `DATASET-CONTEXT.md` and folder scans. — Trade-off: the wrong figures keep propagating (they already reached the trainex-r1a memory estimate and `RATIFICATION.md`'s "~0.55 GB" line).
- **Source problems:** IR2-005.
- **Recommended:** **A** — `DATASET-CONTEXT.md` is Tier-1 and not challengeable; the spec table must move.

---

## Part 3 — Proven problems, in full

Worst first. Every proof below was independently re-verified against the attached files during consolidation; quotes are verbatim.

### IR2-001 — The Stage-0/1 `s_min > 2` criterion is geometrically unsatisfiable by the frozen dataset, leaving Stages 0–2 empty  `locked-decision challenge`
- **What's wrong:** The stratification criterion `s_min > 2` (imposed identically by Stages 0, 1a, and 1b, and inherited by Stage 2 via "Union of Stage 0 and Stage 1 criteria") cannot be satisfied by any hierarchical IC the locked `sampling_method.md` pipeline produces; under the literal spec, Stages 0–2 are empty and the Stage-0-first viability slice has no training population.
- **Where:** `ctl_instruction.md` §"Multi-Stage Data Stratification by Difficulty" (Stage 0/1a/1b criteria bullets; Stage 2 union rule), with the criterion's normative statement in the invariant glossary of the same document.
- **Steelman (the strongest case FOR the locked choice):** The intent is legitimate and stated in the spec's own prose — "Stage 0 imposes $s_{\min}>2$ (in code units) to avoid any incipient close approaches." For the easiest stage, excluding systems already headed into a close encounter at $t=0$ is a sound filter, and for a hierarchical triple the true encounter risk sits between the inner-binary COM and the tertiary, not inside the bound, stably orbiting inner pair. The criterion was carried through deliberate v1.x adjudication (including the Phase 33 decision that gating `s_min` is the *unsoftened geometric* Step-3 quantity), so it is a considered design, not an accident.
- **The proof (`derived-math`):**
  - `sampling_method.md` §"Stage 1: Hierarchical Initial Conditions Generation", step 3 (quoted): "Sample inner semi-major axis $a_{\rm inner}\sim U(0.1,0.3)$, set $a_{\rm outer}=\mathcal{R}\,a_{\rm inner}$." Step 4 (quoted): "$r_{\rm inner}=a_{\rm inner}\bigl(1-e_{\rm inner}\cos M_{\rm inner}\bigr)$" with "$e_{\rm inner},e_{\rm outer}\sim U(0,0.3)$". Hence $r_{\rm inner} \in [0.7, 1.3]\,a_{\rm inner} = [0.07,\ 0.39]$ raw ($G=1$) units. The hierarchy ratio is drawn "$\mathcal{R}\sim U(\max(3,\mathrm{min\_ratio}),10)$", so $\mathcal{R} \ge 3$ and the minimum pairwise separation is the inner-binary separation: $s_{\min} \approx r_{\rm inner}$ (the step-8 $\mathcal{N}(0,0.01)$ perturbation shifts components by $\sim\pm0.03$ at most).
  - `ctl_instruction.md` Step 3 item 1 (quoted): "$s_{\min} \;=\; \min_{1\le i<j\le 3} \lVert \mathbf r'_i - \mathbf r'_j \rVert$" — primed (scaled) coordinates — and §2.5 (quoted): "Compute all subsequent invariants (`E`, `s_min`, etc.) from the scaled `r'` and `v'`", with "`r_i' = r_i^g / D`", "`D ~ 4.6416`". So $s_{\min}^{\rm scaled} \in [0.07, 0.39]/4.6416 = [\,0.0151,\ 0.0840\,]$.
  - `ctl_instruction.md` invariant glossary (quoted): "Stage 0 imposes $s_{\min}>2$ (in code units) to avoid any incipient close approaches", and immediately below: "All data is normalized to dimensionless code units for training". The Stage 0, 1a, and 1b criteria bullets each read "$s_{\min} > 2$"; Stage 2's criteria are "Union of Stage 0 and Stage 1 criteria" applied to Set 2a — the gold reruns of the *same* hierarchical ICs.
  - $0.0840 < 2$: no hierarchical trajectory in the sampling envelope satisfies the criterion in scaled code units. Raw units do not rescue it either ($\max r_{\rm inner} \approx 0.39 \ll 2$), so no unit reading makes Stage 0 non-empty.
  - Empirical confirmation from the spec's own pages: the sample hierarchical IC in §"A Glimpse at the Data" has $\mathbf r_1 = (-0.9690, 0.0077, -0.0152)$, $\mathbf r_2 = (-0.6620, -0.0054, 0.0071)$, $\mathbf r_3 = (1.1354, -0.0016, 0.0029)$, giving pairwise distances $|r_1{-}r_2| \approx 0.308$, $|r_1{-}r_3| \approx 2.104$, $|r_2{-}r_3| \approx 1.797$ (recomputed during consolidation). $s_{\min}^{\rm raw} = 0.308$; $s_{\min}^{\rm scaled} \approx 0.066$. The spec's own exemplar fails the gate under every reading.
  - Compound consequence (recorded, not required for the proof): since virtually every hierarchical trajectory has $s_{\min}^{\rm scaled} < 0.5$, the entire "easiest" family satisfies Stage 6's catch-all ("$s_{\min} < 0.5$ **OR** $|E| < 0.01$") — the literal spec does not merely empty Stages 0–2, it re-classifies the most stable systems into the "near-collision and extreme cases" stage, inverting the curriculum.
- **How serious:** Serious. The milestone is explicitly "Stage-0-first"; `v2.0-build-plan.md` DATA-06 "flags an under-populated Stage 0 as a fatal-class risk", and Phase 39 is on the critical path to Phases 40–43.
- **Which file it points at:** a spec (`ctl_instruction.md`); the data-generation geometry it collides with is frozen (`sampling_method.md`), making "regenerate wider systems" a one-way door — the fix must be on the criterion side.
- **Stops the build?** must-fix-first. Phases 37–38 can technically start, but the build cannot pass Phase 39, and the plan's own rule routes a build-discovered spec defect to a spec decision before code proceeds.
- **Suggested fix (suggestion, not a decision):** PB-1 — make the threshold data-derived from the admitted-set `s_min` distribution (the spec's Stratification section opens with an author note proposing exactly this scan-first approach), with a scaled safety floor such as `s_min > 0.01` as the interim default; leave the other Stage-0 criteria ($E < -0.5$, $L/L_{\max} > 0.5$, $0.7 \le Q \le 1.3$) unchanged — they were checked and are well-posed against the sampling envelope.
- **Provenance:** GLM IR2-002 (sole discoverer; steelman and derivation verified). Consolidation extended the blast radius to Stages 1a/1b/2 and added the Stage-6 misclassification consequence.

### IR2-002 — Build-plan Phase 38 NET-04 specifies a superseded three-term L1/MAE loss where the locked specs require the five-term Huber catalog
- **What's wrong:** The Phase 38 success criterion describes the loss as "three-term (data L1/MAE + physics + IC)", contradicting the locked five-term objective with a Huber data contract — in a phase whose stated purpose is a spec-faithful rebuild.
- **Where:** `v2.0-build-plan.md` Phase 38 (phase summary and NET-04, success criterion 4); contradicted by `pinn_architecture.md` §3/§3.1 and `ctl_instruction.md` §"Loss Function Formulation".
- **The proof (`derived-math`):**
  - Build plan (quoted): "The three-term loss (data L1/MAE + physics + IC) evaluates in the shared dimensionless system (`t_τ ∈ [-1,1]`, `r' = r/D`, raw-mass `D ≈ 4.6416`) matching the locked spec loss contracts (NET-04)." The phase summary repeats "the three-term data+physics+IC loss".
  - `pinn_architecture.md` §3 (quoted): "The default Phase 19 training objective is: $L_{total} = L_{data} + \lambda_{IC} \cdot L_{IC} + \lambda_{phys} \cdot L_{phys}^{causal} + \lambda_E \cdot L_E + \lambda_L \cdot L_L$" — five terms. §3.1 (quoted): "The data fidelity loss uses a Huber contract on scaled projected positions … where $\delta_r = 1$ is the default Huber transition. **The previous MAE/L1 data-loss prose is replaced by this Huber contract.**" NET-04's wording is, verbatim, the formulation the spec records as superseded.
  - `ctl_instruction.md` §"Loss Function Formulation" (quoted): "$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{IC}}\,\mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{phys}}\,\mathcal{L}_{\mathrm{phys}}^{\mathrm{causal}} + \lambda_E\,\mathcal{L}_E + \lambda_L\,\mathcal{L}_L$" — the same five terms.
  - Set difference: build-plan loss set {L1/MAE data, physics, IC} vs locked set {Huber data, IC, causal physics, energy, angular momentum} — a changed data-loss functional form plus two absent regularizer modules.
- **How serious:** Serious. Calibrated precisely: (i) the Huber-vs-L1 mismatch changes the optimized objective at Stage 0 immediately; (ii) the absent $L_E$/$L_L$ modules contradict the same plan's TRAIN-03 ("PHYS-05 scheduled-weight module … `λ_E^max ≤ 1`"), which presupposes those terms exist, and invalidate every stage ≥ 2 where their scheduled weights become nonzero; (iii) a success criterion is the phase's acceptance test, so Phase 38 could "pass" while shipping the wrong objective. (Note: at Stage 0–1 the *spec-correct* loss also carries $\lambda_E^{max} = \lambda_L^{max} = 0$, so "the gate fails because energy is unpenalized" — one source report's rationale — does not distinguish the two losses in the slice; the defect stands on (i)–(iii).)
- **Which file it points at:** the build plan.
- **Stops the build?** must-fix-first — no point running Phases 40–43 against a wrong objective definition.
- **Suggested fix (suggestion, not a decision):** PB-2 Option A — rewrite NET-04 to the five-term catalog (Huber data $\delta_r{=}1$; IC squared-error; causal physics; energy Huber $\delta{=}1.0$; angular-momentum componentwise Huber $\delta{=}1.0$) with PHYS-05 scheduled weights, citing `pinn_architecture.md` §3/§4.1 and `ctl_instruction.md` "Loss Function Formulation".
- **Provenance:** ChatGPT IR2-001 and GLM IR2-001 (independent, converging, both quote-accurate). Severity rationale corrected per Part 0.2-i.

### IR2-003 — Build-plan Phase 39 DATA-05 inverts the locked data-fidelity/collocation contract
- **What's wrong:** DATA-05 maps "240 replay" to the data-fidelity point set and "16 lookahead" to the collocation set, and mandates 50/50 mixed sampling "on both" — misstating a contract in which replay/lookahead select *trajectories*, data-fidelity points come from all 256 trajectories' snapshots, collocation points are continuous samples from $[0,T]$, and 50/50 mixed sampling is retained for data-fidelity points only (deferred for collocation).
- **Where:** `v2.0-build-plan.md` Phase 39 DATA-05 (success criterion 4); contradicted by `ctl_instruction.md` §"Phase 2a … Mini-Batch Construction with Lookahead Sampling" (LOOP-01/02/03).
- **The proof (`derived-math`):**
  - Build plan (quoted): "The replay/lookahead batch constructor emits the two independent point sets — data-fidelity (240 replay, 8192 pts) vs collocation (16 lookahead with the `has_stage(k+1)` guard, 4096 pts) — with 50/50 uniform + acceleration-weighted time sampling on both, per LOOP-01/02/03 (DATA-05)."
  - `ctl_instruction.md` LOOP-01 (quoted): "**Replay set** `B_replay = 240` trajectories … **Look-ahead set** `B_lookahead = 16` trajectories drawn from stage $k+1$ … **Per-trajectory data-loss point count** `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` … `n_pts_cap = 32`." Both sets are *trajectory* sets feeding the data loss.
  - LOOP-02 (quoted): "1. **Data-fidelity points**: sampled from the discrete BRUTUS trajectory snapshots (the replay/lookahead trajectories above), used for the Huber data loss … 2. **Collocation points**: continuous samples from $[0,T]$ for the physics residual … and the energy residual (energy reuses the physics collocation set)." The 8192/4096 budgets are "provisional/example budgets".
  - LOOP-03 (quoted): "**Data-fidelity points — 50/50 retained** … **Collocation points — 50/50 deferred:** A mandatory 50/50 mixed continuous collocation sampler is **deferred** (B-08 / GAP-06); Phase 34 does not mandate it."
  - Arithmetic cross-check: the data-fidelity set draws from $240 + 16 = 256$ trajectories; $256 \times 32 = 8{,}192$ matches the stated budget, while the plan's own "240 replay, 8192 pts" pairing does not ($240 \times 32 = 7{,}680$) — the sentence is internally inconsistent as well as contract-inverting.
  - A literal implementation would evaluate the physics residual only at lookahead-trajectory snapshot times, defeating the continuous-domain residual that defines a PINN, and would impose on collocation a sampler the spec deliberately deferred.
- **How serious:** Serious.
- **Which file it points at:** the build plan.
- **Stops the build?** must-fix-first (adjudicated in Part 0.2-c: success criteria are the plan's acceptance tests; one source report rated this Minor on spec-authoritativeness grounds — the dissent is recorded there).
- **Suggested fix (suggestion, not a decision):** PB-3 Option A — reword DATA-05: 256-trajectory batch (240 replay + 16 lookahead, `has_stage(k+1)`-gated with the LOOP-01 edge-case policy); data-fidelity points from those trajectories' snapshots at `min(32, n_snapshots)` (~8,192, provisional); collocation continuous from $[0,T]$ (~4,096, provisional; energy reuses it); 50/50 mixed sampling on data-fidelity only.
- **Provenance:** ChatGPT IR2-002 (substance + severity) and GLM IR2-005 (substance + the 256-trajectory arithmetic); consolidated per 0.2-c.

### IR2-004 — The split contract never groups by `physical_key`, so base/gold twins of the same physical system can straddle train/val/test
- **What's wrong:** Neither the build plan's split criterion nor the locked specs state that all `record_key`s sharing a `physical_key` must land in the same split, even though the dataset verifiably contains base and gold realizations of the same ICs — a proven under-specification whose derivable consequence is optimistic held-out metrics.
- **Where:** `v2.0-build-plan.md` Phase 39 DATA-04; `ctl_instruction.md` Step 1 item 7 (key vocabulary) and §"Stage Transition Criteria" / §"Evaluation Metrics and Validation" (which consume held-out sets without defining split construction); `DATASET-CONTEXT.md` §"Dataset identity and variants".
- **The proof (`derived-math`):**
  - Build plan (quoted): "A deterministic, stage-stratified split manifest (~80/10/10) is written to the run folder; train shuffles per-epoch under a seeded RNG while val/test iterate in fixed order (DATA-04)." No grouping clause; consolidation confirmed by search that no split-construction or grouping contract exists anywhere in `ctl_instruction.md` (the spec only *consumes* "the held-out validation set (hold-out 10-20% of cumulative data per stage)" and a test set).
  - `ctl_instruction.md` Step 1 item 7 (quoted): "`record_key = (variant, fidelity, id)`; the physical IC is `physical_key = (variant, id)`" — the vocabulary exists precisely because multiple records realize one physical system, and the spec's blacklist contract already attaches exclusion semantics at `physical_key` granularity ("Blacklist semantics attach to `physical_key` and exclude every `record_key` beneath it").
  - `DATASET-CONTEXT.md` (quoted, `verified-empirically`): hierarchical gold = "Gold (high temporal resolution) reruns of the **same** hierarchical ICs"; standard gold = "Gold reruns of a subset of the standard ICs". `ctl_instruction.md` Stage 2 (quoted): the model refines "the high-resolution BRUTUS output of the *same* physical systems (with the same hierarhical IC files used for **Stage 0** and **Stage 1**)".
  - Derivation: a splitter operating over `record_key`s treats `(hierarchical, base, 0123)` and `(hierarchical, gold, 0123)` as independent items; stage-stratified splitting is computed *within* each stage with no cross-stage coordination, so the base record can be assigned to Stage-0 train while its gold twin is assigned to Stage-2 val/test. The same physical trajectory (at different temporal resolution) then sits on both sides of the generalization boundary the ACC-03 gate is meant to measure.
- **How serious:** Serious.
- **Which file it points at:** the build plan (an under-specified step; the specs are silent rather than wrong).
- **Stops the build?** handle-with-a-condition (adjudicated in Part 0.2-d; one source report rated must-fix-first). Condition: add the `physical_key` grouping invariant to DATA-04 before the Phase-39 manifest is written, or record an explicit owner waiver.
- **Suggested fix (suggestion, not a decision):** PB-4 Option A — partition by `physical_key`, expand to all associated `record_key`s, and assert at manifest-write time that no `physical_key` appears in more than one split.
- **Provenance:** ChatGPT IR2-003 (sole discoverer); missed by Gemini and GLM.

### IR2-005 — The `ctl_instruction.md` dataset table swaps the Set 1b and Set 2a file counts against Tier-1 verified counts
- **What's wrong:** The spec's dataset table assigns 4,857 files to Set 1b (Standard base) and 2,749 to Set 2a (Hierarchical gold); the verified on-disk counts are the reverse (standard base = 2,749; hierarchical gold = 4,857). The total (15,028) is right; the per-set roles are not, and the wrong figures have already propagated into ratified-document arithmetic.
- **Where:** `ctl_instruction.md` §"Existing Training Dataset" (the four-row table); against `DATASET-CONTEXT.md` §"Dataset identity and variants" (Tier 1, `verified-empirically`, re-confirmed 2026-07-07).
- **The proof (`derived-math` against a Tier-1 fact):**
  - Spec table (quoted): "Set 1a (4857) | Hierarchical | 1e-15 | 130 | 0.08"; "Set 1b (4857) | Standard | 1e-13 | 118 | 0.17"; "Set 2a (2749) | Hierarchical | 1e-13 | 130 | 0.01"; "Set 2b (2565) | Standard | 1e-13 | 130 | 0.01".
  - `DATASET-CONTEXT.md` (quoted): `brutus_hierarchical` 4,857; `brutus_hierarchical_gold_standard` 4,857; `brutus_standard_quasi_random` 2,749; `brutus_standard_quasi_random_gold_standard` 2,565. The IC-type × `dt_out` pairing is the load-bearing join: "Set 1b Standard @ dt 0.17" *is* the `brutus_standard_quasi_random` folder (verified default `dt_out = 0.17`), which holds 2,749 files, not 4,857; "Set 2a Hierarchical @ dt 0.01" *is* `brutus_hierarchical_gold_standard`, which holds 4,857, not 2,749.
  - Internal corroboration: the spec's own prose two paragraphs below states "Set 1b Standard, 4000" raw ICs were generated, and `DATASET-CONTEXT.md` verifies the standard ID range tops out at 3,998 with 1,250 gaps — a 4,857-file standard-base folder is arithmetically impossible from 4,000 raw ICs.
  - Propagation (verified in `trainex-r1a-resolution-doc.md`): the corpus estimate "4,857×127 + 4,857×61 + 5,314×1,003 = 6,243,058 snapshots × 88 B/176 B" ≈ 0.55 GB fp32 / 1.1 GB fp64 was computed "against the spec's dataset Table" — i.e., with the swapped roles. With verified roles and the Tier-1 snapshot medians (127 hierarchical-base / 61 standard-base / 1,003 gold): $4857{\times}127 + 2749{\times}61 + (4857{+}2565){\times}1003 = 616{,}839 + 167{,}689 + 7{,}444{,}266 = 8{,}228{,}794$ snapshots — **31.8 % more** — ≈ 0.72 GB fp32 / 1.45 GB fp64. Every residency verdict survives (still ~3 % of 24 GB), but the recorded figure in the ratified decision set and in `RATIFICATION.md` ("~0.55 GB fp32") is stale. trainex-r1a's own register item R-5 noticed a sheet↔spec labeling drift but resolved it by trusting the spec table — the layer this finding corrects.
- **How serious:** Serious (a locked spec contradicting a Tier-1 verified fact).
- **Which file it points at:** a spec (`ctl_instruction.md`) / the data.
- **Stops the build?** handle-with-a-condition — Phase 39's Thrust-A scan measures true counts from disk regardless; the condition is correcting the table (and noting the trainex arithmetic) so no later phase quotes the stale figures.
- **Suggested fix (suggestion, not a decision):** PB-5 Option A — swap the two count cells and append a one-line correction note to the trainex-r1a memory arithmetic (≈8.23 M snapshots; ≈0.72 GB fp32).
- **Provenance:** ChatGPT IR2-004 and GLM IR2-003 (independent, converging); GLM's propagation analysis adopted with its snapshot totals corrected by 100 (7,444,266 / 8,228,794).

### IR2-006 — Build-plan Phase 39 DATA-02 summarizes the Step-1A admission gate incompletely
- **What's wrong:** DATA-02's success criterion names only the completeness clause (`final_timestep ≥ 9.5`) and a "NaN/Inf filter", omitting the gate family's *only reject gate* (the conservation clause) and the blacklist, quarantine, physical-invariant, and grid-consistency clauses.
- **Where:** `v2.0-build-plan.md` Phase 39 DATA-02 (success criterion 2); against `ctl_instruction.md` §"Step 1A — Trajectory Admission Gate".
- **The proof (quoted text):**
  - Build plan (quoted): "The Step-1A admission gate (`final_timestep ≥ 9.5`) and NaN/Inf filter run at load with logged admitted/rejected/quarantined/dropped counts, and a `data_version_hash` mismatch is a hard refusal, never a silent proceed (DATA-02, DATA-03)."
  - `ctl_instruction.md` Step 1A defines seven clauses: (1) identity & blacklist (fail-closed, "Missing blacklist file = hard init failure"); (2) data-remediation quarantine; (3) structural integrity; (4) completeness; (5) conservation gate — "REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`)", described in the same file's quality-metric subsection as "the Step-1A conservation gate (clause 5, the family's only reject gate)"; (6) physical-invariant gates; (7) grid-consistency (WARN). The plan's parenthetical covers clause 4 and part of clause 3.
- **How serious:** Minor. The plan does say "the Step-1A admission gate" (invoking the whole family) and logs a "quarantined" category, and the spec is authoritative — but a non-expert builder reading only DATA-02 could ship a completeness-plus-finite check that admits high-drift trajectories the conservation gate exists to exclude.
- **Which file it points at:** the build plan.
- **Suggested fix (suggestion, not a decision):** reword DATA-02 to "the full Step-1A admission gate (clauses 1–7, incl. the conservation reject gate `eps_H ≤ 1e-5` and fail-closed blacklist)" with the same logging language.
- **Provenance:** GLM IR2-004 (sole discoverer).

### IR2-007 — The Step-3 `L_norm` code snippet silently ε-floors exactly the degenerate case the same section's contract says must carry a diagnostic flag
- **What's wrong:** The normative prose mandates raw un-clipped `L_norm` storage with a mandatory diagnostic flag for nonfinite/near-degenerate `L_max`, and authorizes no global clamp — but the accompanying snippet computes `v_char = sqrt(2|E|/M_total + eps)` and returns `L / (L_max + eps)`, silently regularizing the very regime the flag is for.
- **Where:** `ctl_instruction.md` §"Step 3: Necessary Calculations of Invariants" (Phase 33 CURR-02/CURR-04 contract block and the `compute_L_norm` listing directly beneath it).
- **The proof (quoted text + `derived-math`):**
  - Prose definition (quoted): "$v_{\mathrm{char}} = \sqrt{\frac{2\,\lvert E \rvert}{M_{\mathrm{tot}}}}$ … $L_{\max} = M_{\mathrm{tot}}\,r_{\mathrm{char}}\,v_{\mathrm{char}}$ … $L_{\mathrm{norm}} = \frac{L}{L_{\max}}$."
  - Contract (quoted): "the recorded $L_{\mathrm{norm}}$ MUST carry a **diagnostic flag** rather than being silently clamped or stored as `inf` / `nan`" and "**No global clamp is authorized**" — with the stated rationale that Stage 6 ("$s_{\min} < 0.5$ OR $|E| < 0.01$") "is precisely the regime where $|E|$ is small, so a global clamp would erase exactly the diagnostic signal".
  - Snippet (quoted): "`v_char = np.sqrt(2 * np.abs(E) / M_total + eps)`" and "`return L / (L_max + eps)`" with `eps=1e-10`.
  - Derivation: adding `eps` inside the square root redefines $v_{\rm char}$ whenever $2|E|/M_{\rm tot} \lesssim$ `eps` (the small-$|E|$ Stage-6 regime the contract singles out), and the `+ eps` denominator converts an undefined/near-degenerate $L_{\rm norm}$ into a plausible finite number with no flag — the snippet's own trailing comment ("Callers MUST attach a diagnostic flag when L_max is nonfinite or near-degenerate") cannot be honored, because the function has already erased the signal it tells callers to detect.
- **How serious:** Minor — `L_norm` is staging/diagnostic metadata, not an `IC13` slot, and an implementer following the prose gets it right; but a builder copying the snippet ships silent regularization inside a locked spec.
- **Which file it points at:** a spec (`ctl_instruction.md`).
- **Suggested fix (suggestion, not a decision):** replace the snippet with the exact formula plus an explicit branch: if `L_max` is nonfinite or below a named numerical floor, emit `(value=None, flag=degenerate_Lmax)` rather than a manufactured finite value.
- **Provenance:** ChatGPT IR2-005 (sole discoverer; GLM marked Step 3 audited-clean — a verified miss).

### IR2-008 — Step-1A clause 2 still presents the 70-file DATA-05 quarantine as pending, though its own closing condition is Tier-1-verified as satisfied
- **What's wrong:** The spec's quarantine clause reads as an active pending state ("until rerun validation … passes"), while the Tier-1 baseline records that the rerun validation passed on 2026-06-11 and "All quarantines are lifted" — stale presentation that could lead an implementer without `DATASET-CONTEXT.md` to exclude 70 currently-valid files.
- **Where:** `ctl_instruction.md` Step 1A clause 2; against `DATASET-CONTEXT.md` §"Mass-consistency remediation (the 'DATA-05' event)".
- **The proof (quoted text):**
  - Spec (quoted): "The 70 `brutus_hierarchical` base outputs flagged by DATA-05 (IDs 0005-0059, 0061-0075) are quarantined from training, metrics, and PIPE-07 use **until rerun validation from the current canonical ICs passes**. The quarantine list is configuration, not code."
  - `DATASET-CONTEXT.md` (quoted, `verified-empirically`): "Remediation (2026-06-11, executed and validated): all 70 reruns … passed validation gates"; "post-swap re-probe shows **0 mismatches across all 15,028 pairs**. All quarantines are lifted."; and the explicit audit instruction that "any figure that treats the 70-file quarantine as open … predates this remediation."
  - Adjudication (Part 0.2-e): because the clause is conditional and the condition is met, this is stale-text drift, not a live contradiction — the correct implementation state is an empty quarantine list, which the clause's "configuration, not code" design supports.
- **How serious:** Minor.
- **Which file it points at:** a spec (`ctl_instruction.md`) / the data.
- **Suggested fix (suggestion, not a decision):** convert clause 2 to a historical note ("the DATA-05 quarantine was closed by the validated 2026-06-11 remediation; the quarantine-list configuration is empty in the verified baseline and re-opens only if a future validation run fails"), preserving the mechanism.
- **Provenance:** ChatGPT IR2-006, with the framing softened per 0.2-e.

---

## Part 4 — Spec check-everything table (consolidated)

Consolidation rule: where any source report's *verified* problem touches a heading, the problem verdict wins; `audited-clean` is retained only where at least one report examined the heading falsifiably and no verified problem contradicts it. Rejected findings (Part 0.2) do not mark headings.

### `ctl_instruction.md` (27 headings)

| Line | Level | Heading | Consolidated verdict |
|---|---|---|---|
| 9 | H1 | Important Note | skimmed-only — meta-pointer to the (unattached) `PINN_architecture_plan.tex`; no contract content. |
| 17 | H1 | Characterizing and Organizing the Multi-Fidelity Simulation Data | audited-clean — introductory framing. |
| 19 | H2 | Existing Training Dataset | **see problem IR2-005** — Set 1b / Set 2a counts swapped vs Tier-1 facts. |
| 44 | H2 | Multi-Fidelity Dataset and Physical Invariants | audited-clean — invariant glossary consistent with Step 3 definitions (E, Q, s_min, L_norm). |
| 107 | H2 | Multi-Stage Data Stratification by Difficulty (Revised …virial ratio…) | **see problem IR2-001** — `s_min > 2` unsatisfiable (Stages 0, 1a, 1b; Stage 2 via union). Stage 3–4 percentile gating, Stage 4a/4b τ_L bands, and the Stage-6 catch-all are internally well-posed given the Step-3 definitions (τ_L estimator finality is owner-pending — not a defect). |
| 336 | H1 | A Glimpse at the Data | audited-clean — file-format description matches `DATASET-CONTEXT.md`; its sample IC serves as empirical confirmation inside IR2-001. |
| 408 | H1 | Phase 1 - Data Preparation and Stratification | audited-clean — section header. |
| 414 | H2 | Step 1: Parse Raw Simulation Data | audited-clean — parser, ID-resolution (`record_key`, non-dense IDs), footer-default handling, and HDF5 storage contracts match the verified dataset facts. |
| 526 | H2 | Step 1A — Trajectory Admission Gate | **see problem IR2-008** (clause-2 stale quarantine framing). Clauses 1 and 3–7 audited-clean, including the fail-closed blacklist contract and the clause-5 conservation gate (`SCS > −5` reject; direction consistent with trainex B-8); training-time blacklist consumption is an open question → SL-6. |
| 772 | H2 | Step 2: Unified Preprocessing Pipeline | audited-clean — order (parse → mass gates → COM/boost → canonical ordering → rotation gauge → global scaling → assertions) sound; global constants `T=10`, `D≈4.6416`, `V=D/T` single-sourced (this is what refutes rejected finding 0.2-g). |
| 1097 | H2 | Step 3: Necessary Calculations of Invariants | **see problem IR2-007** (`L_norm` snippet vs contract). All other invariant formulas (E, Q, s_min, I_norm, shape invariants, Rosenstein τ_L baseline) re-derived clean; `ε_inv = 10⁻¹⁰` in V only; PHYS-03 anti-pattern correctly stated. |
| 1444 | H2 | Step 4: Formulating the Input Vector | audited-clean — 14D `[τ, IC₁₃]`, τ = 2u−1, raw-mass slots, per-slot tanh normalization with `E_scale = |median(E)| + 1e-8`; matches `pinn_architecture.md` §5.2 exactly. |
| 1580 | H2 | Step 5: Curriculum Stage Assignment | **see problem IR2-001** (stage populations inherit the defective criteria). The gold-counterpart / 184-missing-ID contract matches Tier-1 facts; data-driven adaptive assignment is owner-pending EDA — not a defect. |
| 1647 | H1 | Phase 2 - The Definitive CTL-PINN Training Loop | audited-clean — data flow (14D in → 9D head → COM projection → losses) correct. |
| 1677 | H2 | Overview: The Two-Phase Optimization Strategy | audited-clean — Adam→L-BFGS, plateau handoff, complete Adam reset, frozen-λ during L-BFGS. |
| 1722 | H2 | Loss Function Formulation | audited-clean — five-term assembly matches `pinn_architecture.md` §3; LOSS-01..04 contracts internally consistent. (The build plan contradicts this heading → IR2-002.) |
| 1768 | H2 | Phase 2a: Adam-driven Exploration | audited-clean — initialization, LR schedule, LOOP-01/02/03 batch contracts, C_stage clipping table, termination criterion all coherent. (The build plan misstates LOOP-01/02/03 → IR2-003.) |
| 1877 | H2 | Phase 2b: High-Precision L-BFGS Refinement | audited-clean — full-batch L-BFGS stages 0–2 / sL-BFGS 3–6; the accumulate-in-closure interpretation (trainex D5-a) → SL-3. |
| 1902 | H2 | Stage Transition Criteria | audited-clean — ADVANCE/RECOVER/HALT-REVIEW machine well-specified; fallback advancement rejected; numeric thresholds provisional per the owner carve-outs (not defects). |
| 1979 | H2 | Consolidated Hyperparameter Schedule | audited-clean — no duplicate definitions; C_stage canonically deferred to `pinn_architecture.md` §4.4. |
| 1992 | H2 | Implementation Notes | audited-clean — Hydra double-naming is a documented drift (concordance row 19), superseded by ratified B-9 single-keyed-YAML; not a defect. |
| 2021 | H1 | Advanced Considerations and Best Practices | audited-clean — section header. |
| 2023 | H2 | Evaluation Metrics and Validation | audited-clean as conceptual guidance — conservation/L tracking, Lyapunov-horizon, statistical metrics; the operational binary gate lives in the build plan (achievability → SL-10; τ_L estimator → out-of-scope OS-1). |
| 2097 | H1 | Reproducibility Note (Ignore Now and Come Back Later): | audited-clean — non-operative; second Hydra naming, same concordance row 19. |
| 2130 | H1 | Supplementary Figures | skimmed-only — two unrendered TikZ placeholders; no contract content. |
| 2136 | H1 | Source Issues / Notes for Future Reconciliation | audited-clean — meta-section. |
| 2140 | H2 | SI-CTL-001: Input-vector dimensionality inconsistency | audited-clean — resolved; the 14D contract is consistent across both specs. |

### `pinn_architecture.md` (25 headings)

| Line | Level | Heading | Consolidated verdict |
|---|---|---|---|
| 6 | H1 | A Definitive Implementation Blueprint … | audited-clean — title/abstract. |
| 8 | H1 | 1. Foundational Architectural Principles | audited-clean — co-design rationale consistent with Sitzmann et al. (2020). |
| 105 | H1 | 2. The SQR-SkipResNet-SIREN Backbone | audited-clean — section header. |
| 113 | H2 | 2.1 The Sinusoidal Activation (SIREN) | audited-clean — derivative-fidelity properties correctly stated. |
| 149 | H2 | 2.2 A Principled Initialization Scheme for SIREN Layers | audited-clean — `first_omega_0 = 30` (finalized, not deferred), `hidden_omega_0 = 1`, init bounds match Sitzmann et al. exactly. |
| 190 | H2 | 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation | audited-clean — odd-layer skip with `p=2` power and `LayerNorm(elementwise_affine=False, eps=1e-5)`; the author's LayerNorm addition is transparently documented. |
| 248 | H2 | 2.4 Finalized Architectural Hyperparameters | audited-clean — Table 1 (12×256, SIREN ω₀ pair, skip cadence, linear output) internally consistent with §2.1–2.3 and with build-plan NET-01. |
| 268 | H1 | 3. The Multi-Component Loss Function | audited-clean — five-term default objective; the term inventory this heading defines is what build-plan NET-04 contradicts (IR2-002). |
| 292 | H2 | 3.1 Data Fidelity Term (L_data) | audited-clean — Huber δ_r = 1 on scaled projected positions; explicitly supersedes MAE/L1 (the IR2-002 proof text). |
| 362 | H2 | 3.2 Physics Residual Term (L_physics) | audited-clean — matched-Plummer force with `ε_train = 1e-5`, raw-mass convention, causal weighting `w_n` (owner-ratified Option A), componentwise-AD requirement (PHYS-02). |
| 473 | H2 | 3.3 Initial Condition Anchor Loss (L_IC) | audited-clean — squared-error at u=0 with `λ_IC = 1, β_v = 1`; deliberate non-Huber choice justified. |
| 497 | H2 | 3.4 Soft Energy Conservation Regularizer (L_E) | audited-clean — matched-Plummer Hamiltonian with the **same** `ε_train = 1e-5` as the residual (numerator and H₀ alike); `ε_H = 1e-4·S_H` denominator floor; dual-ε (`ε_inv = 1e-10`) explicitly separated. This heading refutes rejected finding 0.2-b; the residual train-vs-validation-ε doubt → SL-5. |
| 611 | H2 | 3.5 Angular Momentum Conservation Loss (L_L) | audited-clean — componentwise Huber on `(L_θ − L_0)/L_scale`, `ε_L = 1e-8` numerical floor distinct from softening. |
| 627 | H1 | 4. Advanced Training and Optimization Strategy | audited-clean — section header. |
| 633 | H2 | 4.1 Loss Balancing via Warmup Schedule (PHYS-05) | audited-clean — warmup, per-stage `λ^max` (0 at stages 0–1; ≤ 1 throughout), frozen-λ during L-BFGS, mandated instrumentation before any control law. This heading (with §3.2) refutes rejected finding 0.2-f; loss-dynamics monitoring → SL-4. |
| 684 | H2 | 4.2 Optional ALM Ablation (P2) | audited-clean — OFF by default; scalar-conservation only; consistent with the pseudo-ALM rejection in `ctl_instruction.md`. |
| 707 | H2 | 4.3 Two-Phase Optimization | audited-clean — defers schedule to `ctl_instruction.md`; no duplicate definition. |
| 724 | H2 | 4.4 Adaptive Gradient Clipping | audited-clean — `clip = C_stage · median(history)`, Adam-only; deferred execution constants are explicitly routed to FUT (not defects). |
| 774 | H1 | 5. Inference and Trajectory Generation | audited-clean — section header. |
| 779 | H2 | 5.1 Generating a Trajectory | audited-clean — u-leaf vs τ-leaf chain factors (×2, ×4) correctly stated. |
| 801 | H2 | 5.2 Output Layer and Kinematic Consistency via AD | audited-clean — 14D input contract, 9D head, hard COM projection on ordered raw pre-tanh masses, PHYS-02 componentwise-AD contract with worked test. |
| 847 | H2 | 5.3 Output Frame and File Format | audited-clean — COM frame; CSV inference output; HDF5 remains the training-input store (different roles, no conflict). Optional nicety: echo the global constants (D, T, V) in output metadata — recorded as a note, not a problem (see 0.2-g). |
| 994 | H2 | References | skimmed-only — bibliography. |
| 1014 | H1 | 10. Numerical Acceptance Checks | audited-clean — five probes well-formed; probe scripts referenced but unattached (noted); fp32 achievability of the §10.3 `1e-6` tolerance is the D1-p carve-out → SL-1, not a defect. |
| 1043 | H2 | Source Issues / Notes for Future Reconciliation | audited-clean — SI-PINN-002/003 meta-notes; SI-PINN-003 (batch construction) confirmed resolved in favor of `ctl_instruction.md` as canonical. |

### `sampling_method.md` (12 headings)

| Line | Level | Heading | Consolidated verdict |
|---|---|---|---|
| 1 | H1 | A Unified Pipeline for Generating High-Fidelity Three-Body Initial Conditions | audited-clean — including the honest critical-update note that quasi-random sampling-time size scaling distorts virial ratio by s³ (one-way door → out-of-scope OS-4). |
| 5 | H2 | Overview of the Data Generation Pipeline | audited-clean. |
| 20 | H2 | Stage 1: Hierarchical Initial Conditions Generation | audited-clean *as a frozen historical record* — and the geometry source for the IR2-001 derivation (`a_inner ∼ U(0.1, 0.3)`, `R ≥ 3`). |
| 83 | H2 | Stage 2: Enhanced Quasi-Random Sampling | audited-clean — section header. |
| 86 | H2 | 1. Core Sampling Methodology | audited-clean — unit-ball placement, `p₃ = −(p₁+p₂)`. |
| 168 | H2 | 2. Enhancements to the Sampling Algorithm | audited-clean — velocity sampling; collision-avoidance `ε = 0.05`. |
| 200 | H2 | Stage 3: Pre-Screening of Generated ICs for Short-Term Stability | audited-clean — section header. |
| 203 | H2 | 3. The Pre-Screening Rationale | audited-clean — the coarse pre-screen (1 % energy, 0.01 min distance) is intentionally looser than Step-1A; a feature, not a conflict. |
| 224 | H2 | 4. Pre-Screening Criteria | audited-clean — five criteria well-defined; `MIN_DISTANCE_THRESHOLD = 0.01` is the anchor for PB-1 Option B. |
| 246 | H2 | 5. A Coordinated Strategy for Minimum Distance | audited-clean — the three distinct min-distance parameters are clearly disambiguated. |
| 264 | H2 | 6. Execution and Final Quality Control | audited-clean — final QC `|ΔE/E| < 1e-4` looser than Step-1A's `1e-5`: the admission gate is deliberately stricter downstream. |
| 279 | H2 | Source Issues / Notes for Future Reconciliation | audited-clean — "No source-level issues identified during Phase 15 audit." |

---

## Part 5 — Numbers cross-check (consolidated)

"absent" = the spec does not state the element; absence is data. GLM's concordance was adopted as the base (its cell contents verified); the one substantive divergence between reports — row 17 — is resolved against the sources.

| # | Shared element | `ctl_instruction.md` | `pinn_architecture.md` | `sampling_method.md` | Match verdict |
|---|---|---|---|---|---|
| 1 | Network input `[τ, IC₁₃]` | 14D `[τ, IC₁₃]` (Step 4 network-input contract) | 14D `[τ, IC₁₃]` (§5.2) | absent | **MATCH** — single source of truth Step 4; §5.2 cross-references it. |
| 2 | τ definition & AD contract | `τ = 2u−1, u = t/T`; autograd leaf `u` (Step 4) | same; PHYS-02 canonical leaf `u`, conditional ×2/×4 chain factors for τ (§5.2, §5.1) | absent | **MATCH** — PHYS-02 single-sourced in §5.2. |
| 3 | IC₁₃ slot order & mass encoding | `[m₁,m₂,m₃,ρₓ,λₓ,λᵧ,ρ̇ₓ,ρ̇ᵧ,ρ̇_z,λ̇ₓ,λ̇ᵧ,λ̇_z,E]`, raw ordered masses (Step 4) | same (§5.2) | masses normalized to `M_tot = 3` at generation (historical) | **MATCH** — mass-fraction alternative explicitly rejected (Step 2.5 PHYS-01). |
| 4 | Trajectory horizon T | `T = t_max = 10` (§2.5) | `T = t_max` (Table 2) | prescreen `t_max = 1.0` is the Leapfrog window, a different quantity | **MATCH** — single value T = 10. |
| 5 | G convention | `G = 1` (§2.5) | `G = 1` (§3.2, Table 2) | implicit in Keplerian formulas | **MATCH**. |
| 6 | Characteristic length D | `D = (G·T²)^(1/3) ≈ 4.6416`, defined once, globally (§2.5) | same (§3.2, Table 2) | absent (its own sampling-time scale is a distinct historical quantity) | **MATCH** — rejected `D ≈ 6.694` appears nowhere. |
| 7 | Input normalization | per-slot `tanh((z−μ)/(σ+1e-8))`; energy `tanh(E/E_scale)`, `E_scale = |median(E)|+1e-8` (Step 4) | same (§5.2) | absent | **MATCH**. |
| 8 | Output head & COM projection | 9D position head + hard mass-weighted COM projection (Phase-2 data flow) | canonical definition (§5.3): projection on ordered raw pre-tanh mass metadata, before any loss/metric | absent | **MATCH** — single source §5.3. |
| 9 | Softening ε (train) & validation ε | `ε_inv = 1e-10` in Step-3 invariants and the Step-1A gate; `ε_train = 1e-5` by cross-reference to the PHYS-03/§3.4 contracts | `ε_train = 1e-5` in force **and** Hamiltonian (§3.2, §3.4); dual-ε separation explicitly documented | sampling collision `ε = 0.05` is unrelated | **MATCH** — intentional dual-ε; matching of force↔Hamiltonian softening is exact (see 0.2-b). |
| 10 | Energy-drift screening gate | Step-1A clause 5: `eps_H = max_t\|(H(t)−H(0))/H(0)\|`, `SCS = log₁₀(eps_H)`, REJECT if `SCS > −5`; glyph collision with the training `eps_H` explicitly called out | §3.4 `ε_H = 1e-4·S_H` is a *different quantity, same glyph* — the spec flags this itself | absent | **MATCH** — deliberate glyph-collision, documented on both sides; gate direction consistent with trainex B-8 (smaller passes). |
| 11 | Hidden architecture | defers to `pinn_architecture.md` (Important Note) | 12×256, `first_ω₀ = 30` / `hidden_ω₀ = 1`, skip power p = 2, `LayerNorm(elementwise_affine=False)` on odd layers (§2.4 Table 1) | absent | **MATCH** — single source §2.4; matches build-plan NET-01. |
| 12 | Loss inventory & schedules | five-term assembly + LOSS-01..04 (Loss Function Formulation) | five-term components + PHYS-05 warmup, per-stage `λ^max` (§3, §4.1) | absent | **MATCH between specs** — the build plan contradicts it (IR2-002). |
| 13 | Energy-regularizer denominator floor | `ε_H = 1e-4·S_H` by cross-reference | `ε_H = 1e-4·S_H`, `S_H = median_train(K0+Uabs0)` in float64 (§3.4) | absent | **MATCH**. |
| 14 | Batch construction | canonical: 240 replay + 16 lookahead = 256 trajectories; `n_pts = min(32, n_snapshots)`; independent data/collocation point sets; 8192/4096 provisional budgets (Phase 2a, LOOP-01/02/03) | defers to `ctl_instruction.md` (SI-PINN-003 resolution); §3.1 listing marked illustrative | absent | **MATCH between specs** — the build plan misstates it (IR2-003). |
| 15 | Curriculum stage count & transition thresholds | stages 0–6; ADVANCE/RECOVER/HALT machine; thresholds provisional | defers to `ctl_instruction.md` | absent | **MATCH** — but the Stage 0/1 `s_min` criterion is defective on the data side (IR2-001). |
| 16 | Adam → L-BFGS boundary | plateau handoff `d(log₁₀ L_phys)/d(epoch) > −5e-3` for 50 epochs; full-batch L-BFGS stages 0–2, sL-BFGS 3–6 | defers (§4.3); no-clip / frozen-λ during L-BFGS consistent | absent | **MATCH** — accumulate-in-closure interpretation is trainex D5-a → SL-3. |
| 17 | Per-variant `dt_out` / tolerance / counts vs `DATASET-CONTEXT.md` | `dt_out`/tol values per set match the verified folder defaults; **file counts for Set 1b and Set 2a are swapped** | absent | generation background only | **MISMATCH — see IR2-005.** (One source report marked this row MATCH; refuted by the Tier-1 table.) |
| 18 | Output frame & file format | HDF5 canonical training-input store (Step 1/2.6) | COM-frame CSV inference output `time,x1,…,z3` (§5.3) | absent | **MATCH** — different roles (input store vs inference export); no contradiction. |
| 19 | *(extension)* Hydra YAML config stack | named twice: under "Implementation Notes" (unmarked) and under "Reproducibility Note (Ignore Now…)" | absent | absent | **DRIFT, resolved** — double-definition risk (trainex R-4); superseded by ratified B-9 single-keyed-YAML, which the build plan implements (CTRL-01). Recorded for the concordance; not a Part-3 problem. |

---

## Part 6 — Build-plan problem-hunt (consolidated)

Scope: `v2.0-build-plan.md` Phases 37–43 (42 requirements: ENV=4, NET=5, DATA=6, TRAIN=7, CTRL=8, OPS=6, ACC=6), `trainex-r1a-resolution-doc.md` D1–D7 / B-1..B-11, and the §5 first-run recipe. Depth per the stopping-rule: only defects that would invalidate a result, block the build, force a spec-unfreeze, or derail a later phase. Owner carve-outs (D1-p, D4-a ceiling, D4-c/R-2 budgets and thresholds, B-5 field list, R-1 guard thresholds) were respected by the consolidated hunt and are not flagged.

### 6.1 Found problems

| Location | Finding |
|---|---|
| Phase 38 NET-04 (and the phase summary line) | Superseded three-term L1/MAE loss vs the locked five-term Huber catalog — **IR2-002** (must-fix-first). |
| Phase 39 DATA-05 | Data-fidelity/collocation roles inverted; 50/50 wrongly mandated on collocation; "240 replay, 8192 pts" internally inconsistent — **IR2-003** (must-fix-first). |
| Phase 39 DATA-04 | Split manifest lacks the `physical_key` grouping invariant — **IR2-004** (handle-with-a-condition). |
| Phase 39 DATA-06 dependency | Not a plan defect, but the phase's "Stage 0 populated enough to train" goal is unreachable under the literal spec criteria — **IR2-001** (spec-side must-fix surfaced through the plan's own grounding). |
| Phase 39 DATA-02 | Incomplete Step-1A gate summary — **IR2-006** (Minor). |

### 6.2 "Checked this, found nothing" register

The register merges the two verified source registers (GLM's, the most complete, plus ChatGPT's); entries from the third report that could not be grounded were dropped rather than carried.

| Phase / decision | What was checked | Why it is sound |
|---|---|---|
| Phase 37 ENV-01..04 | One-command Miniforge/PyTorch-2.12+MPS setup; environment fingerprint; §10.3 dual-arm probe (fp32-MPS, `PYTORCH_ENABLE_MPS_FALLBACK` unset + fp64-CPU reference, both AD patterns timed); single precision/device switch | Matches B-6 fingerprint fields and the D1-p carve-out exactly: the probe produces evidence, the owner decides; the fp64-CPU branch is the in-framework escape (U-9). |
| Phase 38 NET-01/02/03/05 | 14→256×12→9 architecture with SIREN ω₀ pair and odd-layer skip+LayerNorm; COM projection before any loss; PHYS-02 chain factors + fp64-CPU gradcheck + residual-on-ground-truth; single-trajectory overfit | All match `pinn_architecture.md` §2.4/§5.2/§5.3/§3.2/§10 verbatim; only NET-04 (the loss wording) is defective. |
| Phase 39 DATA-01/03/06 | In-memory fp32 admitted-set preload, `num_workers=0`, 0.7 watermark, `n_snapshots`/`dt_out` metadata; `data_version_hash` hard refusal; Thrust-A stage-population scan with fatal-class Stage-0 flag | Match trainex D3-C and the spec's loader contracts; hash *production* remains an upstream open item → SL-7; the corrected corpus size (≈0.72 GB fp32, IR2-005) still lands comfortably in-memory, so the D3 residency verdict is unchanged. |
| Phase 40 TRAIN-01..07 | Outer/inner controller loop; two-phase Adam→L-BFGS closure with accumulate-in-closure, frozen-λ, no L-BFGS clipping; PHYS-05 scheduled-weight module with serialized state; collocation sampler interface with adaptive hook; merged median clipping with the C_stage table; ADVANCE/RECOVER/HALT machine with `recover.retries: 0` seam and no fallback advancement; sL-BFGS preflight refusal | All seven match `ctl_instruction.md` Phase 2, `pinn_architecture.md` §4, and trainex D5-a/b/c, D4-c, D7-b; the preflight refusal correctly converts U-7 into a typed stop; convergence-equivalence of accumulate-in-closure → SL-3. |
| Phase 41 CTRL-01..08 | Single keyed YAML with frozen resolved copy; dual-trigger checkpointing with rolling-3/best/latest/anchor retention; atomic writes (tmp+fsync+rename, `weights_only`-clean, fallback scan); dual anchors + idempotent promotion + `curriculum.jsonl`; `--resume`/`--hold-stage` + fail-safe field-classified resume-diff; complete Adam reset at boundaries; Tier-1+2 guards + RECOVER + HALT/REVIEW + always-on `failure/` bundle; full seed/RNG record scoped to statistical equivalence | All eight match trainex D4-a/b/c/d, D6, D7-a/b/c/d, B-5, B-6, B-9, B-11; every ⚖ placeholder is built as a seam with a safe default, exactly as the carve-outs prescribe. |
| Phase 42 OPS-01..06 | Five entry points; `caffeinate -is` wrapper with SIGTERM ≡ one graceful Ctrl-C; widened JSONL field set (5 loss terms + total + λ vector + grad-norm + `w_n` stats + lr + s/step + ETA) + TensorBoard secondary + `status.json`/`mem:`/residual panel; `runs/<n>/` contract; written runbook | Match trainex B-2/B-6/B-10; `caffeinate -is` is the correct Apple-Silicon unattended-run choice (lid-close sleep cannot be overridden). |
| Phase 43 ACC-01..06 | Verify ladder ordering (device sanity → §10.3 probe → gradcheck → residual/§10 probes → overfit) gating real runs; ~5-min smoke test recording s/step; `evaluate` rendering the binary gate with the spec-settled direction (`ε_H > 1e-5` reject, smaller passes — B-8); `summary.md` honesty layer; 2–3-seed pilot calibrating ⚖ thresholds; go/adjust/rethink close | Match Step-1A clause 5 and trainex B-8/D6; the gate's *achievability* as a model criterion is an empirical question the pilot itself renders → SL-10. |
| trainex D1 / D2 / D3 | Framework (PyTorch 2.12 + MPS, fp64 branch = same code on CPU); JSONL-canonical tracking; D3-C in-memory adapter | Consistent with the specs and the single-machine Tier-1 constraint; the U-9 MPS-coverage uncertainty is explicitly held open for the probe (side-list, not defect). |
| trainex D4/D5/D6/D7, B-1..B-11 | All 21 decisions checked for spec contradiction, internal recipe consistency, and improper filling of owner-carved values | No decision contradicts a locked spec contract; the §5 first-run recipe composes (its three consolidation additions consume existing seams); B-8 is spec-settled; B-5's fail-safe default is a strict safety improvement. One stale figure found: the D3/U-1 corpus arithmetic inherits the spec-table swap — recorded under IR2-005, with the residency verdict unchanged. |
| §5 first-run recipe | Step composition setup → verify → configure → launch (caffeinate) → Stage-0 shape → resume/rollback → seed band | Coherent as written, conditional on PB-1..PB-3 landing first; every pick holds under both D1-p branches except the device line and GPU-monitoring rows, as the recipe itself states. |

---

## Part 7 — Side-list (empirical doubts & their tests)

Merged and de-duplicated across the three reports; each entry keeps the strongest formulation. These feed the verify ladder / Stage-0 pilot as extra things to watch.

**SL-1. MPS double-backward coverage and fp32 second-order-AD precision for this exact net** *(all three reports; Gemini's IR2-001 demoted here per 0.2-a)*
(a) Doubt: does PyTorch 2.12's MPS backend support second-order AD through this operation sequence (sin, affine-free LayerNorm, elementwise square, `d²r'/du²`) with acceptable numerical error in fp32, and is the §10.3 `1e-6` tolerance achievable on that arm? (b) Paper can't settle it: MPS kernel coverage is version-specific and undocumented for this composite; fp32 round-off through a double-backward chain is workload-dependent; trainex U-9 holds it open by design. (c) Test: the Phase 37 ENV-03 dual-arm probe with fallback unset, comparing componentwise accelerations against the fp64-CPU reference and timing both AD patterns. Bad result: a not-implemented crash, NaN/Inf, relative error beyond the owner's D1-p tolerance, or per-step cost incompatible with the smoke budget. (d) Confidence: owner-carved with a designed escape (fp64-CPU branch); high confidence the probe settles it either way.

**SL-2. Stage-0 (and Stage-1/2) populations after the IR2-001 repair** *(ChatGPT SL-2 + GLM SL-2)*
(a) Doubt: with the `s_min` criterion repaired, how many admitted hierarchical trajectories jointly satisfy the remaining criteria ($E < -0.5$, $L/L_{max} > 0.5$, $0.7 \le Q \le 1.3$), after blacklist exclusion and `physical_key`-grouped splitting? The spec sets no numeric floor for "populated enough". (b) Invariant distributions are not in the Tier-1 facts; only counts are. (c) Test: the Phase 39 DATA-06 Thrust-A scan under the repaired criteria. Bad result: a Stage-0 train split too small for a ~727 K-parameter model (the scan should also propose the numeric meaning of "under-populated" for owner ratification). (d) Confidence: medium — hierarchical sampling targets stable triples, so $E$ and $Q$ should pass broadly; $L/L_{max} > 0.5$ is the likely binding filter.

**SL-3. Accumulate-in-closure L-BFGS: convergence equivalence, memory watermark, and wall-time** *(GLM SL-3 + ChatGPT SL-5 + Gemini side-list 1, merged)*
(a) Doubt: trainex D5-a interprets the spec's "full-batch L-BFGS" as gradient accumulation inside the closure; is that convergence-equivalent for this net+loss, and do the closure's repeated forward passes fit the 24 GB watermark and an acceptable s/step? (b) Line-search behavior under accumulated gradients and real memory highs are empirical. (c) Test: on a ~32-trajectory Stage-0 sub-batch, run single-graph full-batch vs accumulate-in-closure to convergence; log final loss, line-search step sizes, `mem:` peaks, and wall-time in the first L-BFGS phase of the smoke/pilot. Bad result: accumulate-in-closure stalls (step size → 0) or converges materially higher; or swap pressure / watermark trips / per-step time incompatible with unattended runs. (d) Confidence: low-medium on equivalence (standard practice, unproven here); memory itself is low-risk given the ≈0.72 GB corpus and r1b's 2–7 GB steady-state estimate.

**SL-4. Multi-term loss dynamics: term domination and causal-weight underflow** *(ChatGPT SL-3 + GLM SL-4; absorbs the legitimate kernel of Gemini's rejected IR2-003)*
(a) Doubt: even with causal weighting, warmup, and per-stage caps, multi-component PINN losses can develop one-term-dominates dynamics; separately, $w_n = \exp(-\eta_c\sum \mathrm{stopgrad}(\bar R_m))$ can underflow for late times (the clip bound is deliberately deferred to FUT). (b) Depends on data, init, and hardware; the literature (Krishnapriyan et al. 2021; Wang et al. 2024) documents the failure modes but cannot predict this instance. (c) Test: the already-ratified instrumentation — per-term weighted losses, λ vector, grad-norm, and `w_n` statistics in every logged step — reviewed at the smoke test and pilot. Bad result: one term's gradient norm persistently eclipses the rest, or > ~50 % of `w_n` underflow to 0 over the trajectory's second half (which would also calibrate the deferred clip bound). (d) Confidence: medium; Stage 0's λ_E = λ_L = 0 makes the slice the mildest case.

**SL-5. Dual-ε divergence at close encounters (training `ε_train = 1e-5` vs validation `ε_inv = 1e-10`)** *(GLM SL-5; the salvageable kernel of Gemini's rejected IR2-002)*
(a) Doubt: minimizing drift of the matched-softened $H_{\epsilon_{train}}$ may not minimize drift of the validation $H_{\epsilon_{inv}}$ for trajectories with pair separations approaching $\epsilon_{train}$. (b) Depends on the admitted set's close-encounter statistics. (c) Test: for any post-slice chaotic-stage pilot, compute both drifts on held-out data and compare against the loss floor and the `1e-5` gate. Bad result: passes the training-side threshold while failing the validation gate. (d) Confidence: low for Stage 0 (no close encounters by construction), medium-high for stages 4–6 — a full-platform watch item, not a slice blocker.

**SL-6. Blacklist training-time consumption** *(GLM SL-6)*
(a) Doubt: `DATASET-CONTEXT.md` labels training-time blacklist consumption `claimed-unverified` (current Brutus runners don't load it), while `ctl_instruction.md` Step-1A clause 1 requires fail-closed DataLoader enforcement — and the build plan's DATA-02 summary omits it (IR2-006), so the builder may not implement it. (b) Whether Phase-39 code enforces the contract is a build-time fact. (c) Test: audit the Phase-39 loader for load-at-init, schema validation (exactly `hierarchical` and `standard` keys), `physical_key`-level exclusion, and the batch-time re-assertion; then verify the 65 IDs (2 + 63) are absent from emitted batches. Bad result: any blacklisted IC appears in a batch, or absence of the file does not hard-fail. (d) Confidence: medium-high that a spec-faithful implementation is unambiguous; the risk is omission, which the IR2-006 fix mitigates.

**SL-7. `data_version_hash` production** *(GLM SL-7)*
(a) Doubt: DATA-03's compare-and-refuse contract presupposes a produced hash; the production mechanism (v1.5 PIPE-XX) is referenced but unattached (trainex U-12). (b) The upstream mechanism's integration is unverifiable on paper. (c) Test: before Phase 39 completes, confirm the processed store carries a non-null, content-derived hash. Bad result: missing/constant hash — the refusal check is structurally a no-op. (d) Confidence: medium.

**SL-8. Temporal-sampling / Nyquist adequacy and SIREN aliasing between snapshots** *(ChatGPT SL-4 + GLM SL-8 + Gemini side-list 2, merged)*
(a) Doubt: standard-base trajectories (median 61 snapshots, `dt_out = 0.17`) sit near the Nyquist limit for tight-binary orbital frequencies, and a `first_ω₀ = 30` SIREN can represent frequencies the base grid cannot pin down — so the network could fit snapshots exactly while oscillating unphysically between them (base stages 3–4 concern; hierarchical-base at 127 snapshots is comfortable for the slice). (b) The per-stage frequency-content and SASD/IPR distributions aren't in the Tier-1 facts. (c) Test: during Phase 39, compute SASD/IPR (and an orbital-frequency vs Nyquist comparison) per stage; during the overfit probe and pilot, evaluate the trained model at ~10× the data's temporal resolution and inspect kinetic-energy profiles between snapshots. Bad result: a large flagged fraction in the base stages, or wild inter-snapshot kinetic-energy oscillation in the overfit probe. (d) Confidence: low for Stage 0, medium for stages 3–4; the deferred `dt_out`-aware collocation scaling (LOOP-06) is the designed future lever.

**SL-9. Lyapunov-time-aware evaluation remains underdetermined for the chaotic stages** *(ChatGPT SL-6; GLM OS-1/OS-2 folded in)*
(a) Doubt: the final τ_L estimator, its time-unit convention, fit window, and the Stage-4a/4b thresholds are owner-pending; the slice's ACC-03 binary gate is a documented proxy, not the spec's Lyapunov-horizon metric. Stage labels for stages 4–6 could shift materially under a different estimator. (b) Estimator sensitivity is an empirical property of the data. (c) Test (pre-Stage-4, out of slice scope): compare the Rosenstein baseline against a Benettin-style estimator on a stratified subset; bad result: stage assignments change for a non-trivial fraction. (d) Confidence: high that it is unresolved; low that it affects the Stage-0 slice.

**SL-10. Achievability of the `ε_H ≤ 1e-5` binary gate as a *model* acceptance criterion** *(added during consolidation — flagged as consolidator-originated, surfaced while adjudicating IR2-002's severity)*
(a) Doubt: the post-v1.3 gate was designed to screen Brutus data (observed drifts ~1e-16..1e-13); ACC-03 applies the same `ε_H ≤ 1e-5` bar to *PINN-predicted* trajectories on held-out ICs, at a stage where the energy regularizer's scheduled weight is 0. Whether any healthy Stage-0 model can clear a 1e-5 max-relative-drift bar is unknown and drives the go/adjust/rethink verdict. (b) No prior in the files bounds a PINN's achievable drift on this data; Breen et al.'s (non-PINN) precedent doesn't reach conservation at this tolerance. (c) Test: none extra needed — ACC-03/ACC-05 render it; the watch is interpretive: record the achieved `ε_H` distribution across the 2–3 seeds. Bad result: healthy loss/validation curves with `ε_H` orders of magnitude above 1e-5 — which would indicate the *gate calibration for models*, not the build, needs an owner decision. (d) Confidence: genuinely unknown; flagged so a gate failure is read diagnostically rather than as an automatic build failure.

### Out of scope / no cheap test now
- **OS-1. Quasi-random sampling-time size scaling distorts virial ratio by s³** (documented in `sampling_method.md`'s own critical-update note): a data-generation property of the frozen set; any remedy is a one-way door. *(ChatGPT)*
- **OS-2. Latent integration artifacts near singularities that passed the ε_H screen**: unfalsifiable without regeneration; treated as irreducible data noise. *(Gemini — its one retained contribution)*
- **OS-3. Final τ_L estimator selection** (D-33-07): not testable until the estimator is chosen; affects stages 4–6 only. *(GLM)*
- **OS-4. Propagating the IR2-005 correction into `trainex-r1a-resolution-doc.md` / `RATIFICATION.md` figures** (~0.55 → ~0.72 GB fp32): a spec-owner reconciliation action, not an empirical test. *(GLM)*

---

## Part 8 — Sources

Consolidated, date-stamped 2026-07-07. Literature entries were relied on by the ChatGPT and GLM reports; the consolidation verified each is used only for context/anchoring, never as the sole proof of a Part-3 problem (every admitted problem is `derived-math` against the attached files). Gemini's `[1]–[10]` citations could not be included: its report contains no reference list.

**Primary literature**
1. Breen, P. G., Foley, C. N., Boekholt, T., & Portegies Zwart, S. (2020). *Newton versus the machine: solving the chaotic three-body problem using deep neural networks.* MNRAS 494(2), 2465–2470. doi:10.1093/mnras/staa713 — RD-1 anchor (same Brutus lineage; final-state prediction on a restricted IC family, no PINN/curriculum — scope contrast for the viability question).
2. Krishnapriyan, A., Gholami, A., Zhe, S., Kirby, R., & Mahoney, M. W. (2021). *Characterizing possible failure modes in physics-informed neural networks.* NeurIPS 34. — RD-6 anchor (multi-scale loss pathologies; supports curriculum-regularization design and the SL-4 monitoring stance).
3. Wang, S., Sankaran, S., Wang, H., & Perdikaris, P. (2023/2024). *An Expert's Guide to Training Physics-Informed Neural Networks.* arXiv:2308.08468. — RD-6 anchor (causal weighting, clipping, balancing; the spec's `w_n` mechanism matches its causal-training recommendation).
4. Sitzmann, V., Martel, J. N. P., Bergman, A. W., Lindell, D. B., & Wetzstein, G. (2020). *Implicit Neural Representations with Periodic Activation Functions.* NeurIPS 33. — SIREN initialization anchor (`first_ω₀ = 30`, hidden bounds `U[−√(6/n)/ω₀, √(6/n)/ω₀]`; verified to match `pinn_architecture.md` §2.2/§2.4).

**Official documentation**
5. PyTorch, *MPS backend* notes (stable, PyTorch 2.x; target 2.12 per trainex D1). https://pytorch.org/docs/stable/notes/mps.html — MPS capability context for SL-1; coverage for this composite is explicitly a probe question (U-9), not a documented guarantee.
6. PyTorch, *Reproducibility* notes. https://pytorch.org/docs/stable/notes/randomness.html — grounds the D6 statistical-equivalence determinism policy (MPS nondeterministic under full seeding; deterministic mode's cost).
7. PyTorch, *torch.optim.LBFGS* documentation. https://pytorch.org/docs/stable/generated/torch.optim.LBFGS.html — closure-based, single-device constraint context for SL-3.

**Project files (the seven attached sources; all Part-3 quotes drawn from these)**
8. `ctl_instruction.md` — locked science spec (data, preprocessing, invariants, input vector, curriculum, loop, evaluation).
9. `pinn_architecture.md` — locked science spec (network, losses, AD contract, inference, §10 checks); frontmatter date 2026-03-21.
10. `sampling_method.md` — frozen data-generation record; dated June 15, 2025.
11. `v2.0-build-plan.md` — the build plan under audit; created 2026-07-06.
12. `trainex-r1a-resolution-doc.md` — ratified build decisions and §5 first-run recipe; 2026-07-05.
13. `RATIFICATION.md` — owner ratification and carve-out record; 2026-07-05.
14. `DATASET-CONTEXT.md` — Tier-1 verified dataset facts; created 2026-07-07 (counts re-confirmed 2026-07-07).

---

*Consolidation discipline statement.* Every problem admitted to Part 3 was re-proven against the attached files during consolidation (quotes re-extracted, derivations re-run, arithmetic re-computed); every rejected finding carries its refuting quote in Part 0; the sole locked-decision challenge (IR2-001) carries its steelman; no owner carve-out is flagged as a defect; and the one consolidator-originated side-list entry (SL-10) is explicitly labeled as such. The punch-list (PB-1..PB-5) is the minimum decision set gating the Serious findings; the owner disposes.
