# Requirements: Three-Body Physics-Informed LLM v1.6

**Defined:** 2026-06-17
**Core Value:** The curriculum-staging and training-loop framework contracts are evidence-backed, internally consistent with the locked v1.4 (doc-01) and v1.5 (doc-02) conventions, and verified with disposable acceptance probes before any training-loop implementation depends on them.

**Current workflow state:** v1.4 shipped 2026-06-09 (merged to master). v1.5 (doc-02 data-pipeline/validation) is **closure-ready** — its `--no-ff` merge to master and `/gsd-complete-milestone` archival are user-owned and in progress. v1.6 is being initialized on branch `milestone/v1.6` (worktree at `../3_body_problem-v1.6`, cut from the v1.5 deliverable tip `88aa1e4f`); it will be rebased onto the completed `master` once v1.5 closes. v1.6 targets `pinn_instruction/issues/03-curriculum-and-training-loop.md`.

## Source treatment policy

The issue doc (`pinn_instruction/issues/03-curriculum-and-training-loop.md`) is **NOT authoritative** — it consolidates the 2026-04-27 audit (Sections 6–7), the Causal Training Mismatch blueprint, the stage-assignment methodology, and `next steps.txt` fragments, and it carries known tensions (e.g., `D = 6.694` against the v1.5-locked raw-mass `D ≈ 4.6416`). Every finding is verified before any fix is applied.

**No resolution doc exists at milestone start.** The user produces one via external multi-AI research (the External Research Workflow), working from an agent-prepared research package (PKG-05..08). The resulting doc — expected under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/` — becomes the **candidate verdict source** with the same standing `ctl_pinn_resolution.md` had in v1.4 and `02-resolution-doc.md` had in v1.5: default verdict source, transcribed unless evidence shows a position fails, never authoritative. Adjudication phases gate on its arrival.

**Specwork only (user-confirmed 2026-06-17).** v1.6 settles the curriculum/training-loop **framework-spec contracts** in `ctl_instruction.md` and `pinn_architecture.md`. It does NOT implement training-loop code. The verbatim audit "Section 6 — Unified Batch Construction" pseudocode is transcribed as a **normative spec contract**, not executed; the production `training_step`, DataLoader, and ALM implementation are FUT-01/FUT-04 (the trainex track).

**Locked v1.4 + v1.5 outcomes are hard-constraint grounding** (SCOPE-12): the 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), the PHYS-01 raw-mass D convention (`D = (G·T²)^(1/3) ≈ 4.6416`; `D = 6.694` was rejected by v1.5 Phase 25 EVID-10), and the v1.5 DataLoader/stage-query/validation-metric data-side contracts (PIPE-01..10, VAL-01..04).

**Live code in `pinn/` is NOT grounding** (directive 2026-05-19, persists). Issue-03's "Canonical" citations of `data-processing-pipeline-full.py` and `basic_architecture.py` are overridden; live-code references stay confined to forward-pointing FUT-01/FUT-04 hand-off documents.

**STOP protocol applies in full** (AGENTS.md "CRITICAL GOVERNANCE"): source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in phase-local `NN-GAPS.md` registers and the milestone index `.planning/milestones/v1.6-GAPS.md`; nothing is invented.

## v1.6 Requirements

### Research Package and External Resolution

- [ ] **PKG-05**: The research package delivers a complete annotated document list for the user's external research agent — every document needed to adjudicate the issue-03 findings, each with a role annotation. If the list would exceed ~5 files or the necessary context is scattered across fragments, the fragments are consolidated into a single context file (framework specs passed intact, never consolidated) and the consolidation is surfaced to the user before assembly.
- [ ] **PKG-06**: The package frames the research questions: each contested or unverified finding is posed as an explicit neutral question, with the locked v1.4 conventions AND v1.5 data-pipeline/validation outcomes listed as hard constraints the research must respect (SCOPE-12). The three human-approval decisions — **D-04** (causal training mode: per-time-step / global+ALM / time-windowed hybrid), **D-05** (s_min frame), **D-06** (epsilon strategy) — and the known cross-milestone conflict (`D = 6.694` vs the v1.5-locked `D ≈ 4.6416`) are posed without being settled.
- [ ] **PKG-07**: The package presents dataset/empirical figures as explicitly-marked **"claimed, unverified"** issue-doc values wherever empirical verification has not been performed. Figures already verified by v1.5 (e.g., the 184 standard IDs without gold, the ~2,565 quasi-random gold count, per-variant snapshot/`dt_out` distributions) are stated as verified with their v1.5 citation. No unverified figure is presented as fact.
- [ ] **PKG-08**: The curriculum-relevant research reports cited by issue-03 — `review-of-framework.md` and `stage-strat-revision.md` (under `framework-revisions/`) — are characterized read-only: provenance, content map, and relation to the doc-03 findings, reported to the user. No edits to these files (SCOPE-09 analog).

### Adjudication (continuing v1.4 EVID-01..05 / v1.5 EVID-06..10)

- [x] **EVID-11**: For each issue-03 finding selected for remediation, the agent records direct evidence — issue-doc citation, resolution-doc verdict (once landed), current framework-spec evidence, and (where relevant) v1.5-verified dataset evidence — before editing. Evidence packets cite line ranges, not whole files.
- [x] **EVID-12**: Each finding receives an explicit verdict from the fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — with reasoning recorded in the evidence packet.
- [x] **EVID-13**: False positives in either source are documented as intentional non-changes, including why the current convention remains valid and which source(s) misread it (e.g., M6's L_norm clamp under the v1.4 Jacobi IC₁₃, which no longer carries L_norm as an IC slot).
- [x] **EVID-14**: Every accepted finding has a before/after evidence note naming the changed spec section, the contract it now enforces, and the verification step that confirms the fix.
- [x] **EVID-15**: When sources conflict — issue doc vs resolution doc vs v1.4/v1.5-locked conventions vs first principles — the agent performs root-cause adjudication: reads all positions, verifies each against specs and first principles, names the root-cause ambiguity, locks the convention, and records which source was right, which wrong, and why. Findings requiring adjudication (not pre-resolved here): **D-04** causal training mode (Option A / B / C); **D-06** epsilon strategy (`1e-5` everywhere / dual-context `1e-10`+`1e-5` / `1e-10` everywhere, cross-linked to the doc-01 dual-context discussion); **D-05** s_min frame (unsoftened stage gate + softened loss vs softened everywhere); the **`D = 6.694` vs v1.5-locked `D ≈ 4.6416`** conflict (reconciled with v1.5 Phase 25 EVID-10 as the hard constraint); and the **M14** dual gradient-clipping divergence.

### Curriculum-Stage Contracts (spec-side; FUT implements)

- [x] **CURR-01**: Framework specs define the data-driven adaptive stage-assignment methodology contract (dataset EDA → PCA + K-means + quantile thresholds augmenting the static theoretical anchors; the per-stage population safeguard — its value (5% / >10% / adaptive) owner-pending the FUT admitted-set EDA per GAP-33-01, not locked here) per the issue-03 "Data-Driven Adaptive Stage Assignment" section. The actual EDA run over the dataset is FUT (SCOPE-15).
- [x] **CURR-02**: Framework specs define the `tau_L` and `L_max` computation contracts — `L_max = M_total · r_char · v_char` (the characteristic angular-momentum scale, not a proven global maximum, per GAP-33-02); `tau_L = 1/λ_max` via the current Rosenstein-style revisable baseline estimator, with the shadow-trajectory `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10` method and the fast PCA+Rosenstein batch approximation not normatively adopted, and the estimator, time units, and thresholds owner-pending per GAP-33-02 — with the D value reconciled against the v1.5-locked convention (EVID-15). M7 (`tau_L` excluded from the IC vector by design) is recorded.
- [x] **CURR-03**: Framework specs define the dual-path stage-transition state machine — **ADVANCE** (only on the approved success gate: training plateau, validation stability, stage-dependent physics-residual `ε_phys` and energy-drift `ε_energy`), **RECOVER** (NaN/Inf rollback with bounded retry), and **HALT/REVIEW** (max-epoch or stagnation, with explicit owner authorization required for any degraded advancement) — as a curriculum contract. The issue-doc "fallback Path B advancement" framing is rejected; max-epoch/stagnation route to HALT/REVIEW and NaN/Inf route to RECOVER, not to advancement. Thresholds are marked **provisional pending the FUT Stage-0 pilot calibration** (D5-05 claimed-unverified; D-33-09). Transcribed in Plan 33-03; AC-CURR-03 verified by Plan 33-04.
- [x] **CURR-04**: Framework specs define the Stage 0–6 inventory and gating contract (per-stage definitions, criteria, cumulative replay, Stage-6 catch-all, storing raw un-clipped `L_norm` as metadata plus the mandatory nonfinite / near-degenerate `L_max` guard — the M6 `np.clip(L_norm, 0, 1)` stage-gate is not locked and is owner-pending per GAP-33-03, and no global clamp is authorized) consistent with v1.5-verified dataset facts; stage trajectory counts are cited as v1.5-verified or marked "claimed" where not yet grounded.
- [x] **CURR-05**: Framework specs define the s_min frame for the curriculum **stage gate** — unsoftened geometric `s_min` for the Stage-6 collision gate (detect true close encounters, raw value logged for diagnostics) — per the D-05 adjudication (GAP-32-02 Option A); the issue-doc `max(s_min, eps_soft)` phrasing is rejected per PHYS-03, and loss-side matched-Plummer softening (`epsilon_train = 1e-5`) is owned by Phase 35 (LOSS), with dual-context epsilon (`epsilon_inv = 1e-10` offline / `epsilon_train = 1e-5` training; GAP-32-03 Option A) transcribed alongside. Transcribed in Plan 33-03; AC-CURR-05 verified by Plan 33-04.

### Training-Loop and Batch-Construction Contracts (spec-side; FUT-01/FUT-04 implement)

- [x] **LOOP-01**: Framework specs define the replay/lookahead batch-construction contract (`B_replay = 240` from `D_≤k` + `B_lookahead = 16` from `D_{k+1}`, with the `has_stage(k+1)` guard) per B-07 / audit Section 6 — as a DataLoader/training design contract; the structure is reconciled with the D-04 causal-mode verdict (a windowed mode excludes future-window trajectories). Implementation is FUT-01.
- [x] **LOOP-02**: Framework specs define the two-independent-point-set contract — data-fidelity points (8192 from Brutus snapshots, L1/MAE loss) kept separate from collocation points (4096 from `[0,T]`, physics + energy loss), even when they share trajectory IDs — per B-08.
- [x] **LOOP-03**: Framework specs define the mixed time-sampling contract (50% uniform + 50% acceleration-weighted) applied to **both** data-fidelity and collocation point sets, per audit Section 6.1 (P3-3).
- [ ] **LOOP-04**: Framework specs define the merged gradient-clipping contract — `clip_value = C_stage · median(grad_norm_history)` with the per-stage `C_table` (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0) and a rolling window — per M14.
- [x] **LOOP-05**: Framework specs define the ALM parameter-update contract — `λ_p`/`μ_p` RMSprop-style moving-average update executed under `torch.no_grad()`, with the `μ_p` clamp `[1e-4, 100]` — per the audit ALM specification and the MINOR clamping finding.
- [x] **LOOP-06**: Framework specs define the `dt_out`-aware collocation-scaling contract — `n_col ∝ dt_base / dt_out` (audit M16 line-163 verbatim direction; the inverse form is an explicit future methodology change, not transcribed) — **realizing the v1.5 SCOPE-11 / PIPE-08 forward-reference** that left collocation-scaling to the doc-03 milestone.
- [ ] **LOOP-07**: Framework specs define the training-side use of the v1.5 metrics left provisional — **IPR** as the ALM convergence / noise-floor (v1.5 VAL-03 forward-reference; the provisional `1e-3` threshold confirmed or recalibrated) and **PSC** for replay-buffer governance (v1.5 VAL-04 forward-reference; the provisional grid/normalization/SCR confirmed or recalibrated).
- [ ] **LOOP-08**: Framework specs define the **SASD** training-side collocation-weighting use (v1.5 VAL-02 explicitly deferred "training-side collocation weighting" to the doc-03 milestone with a recorded forward-reference).

### Loss and Energy-Weight Contracts (spec-side; FUT implements)

- [x] **LOSS-01**: Framework specs carry the loss-component scaling contract — `L_data`, `L_physics`, `L_energy` all evaluated in the same dimensionless coordinate system (`t_τ ∈ [-1,1]`, `r' = r/D`), with the AD chain-rule factors (`d²r'/du² = 4·d²r'/dτ²`, `dr'/du = 2·dr'/dτ`) cross-linked to their canonical doc-01 location — per NS-18.
- [x] **LOSS-02**: Framework specs define the capped-hybrid energy-loss-weight schedule — `λ_E(k) = min(10^(k-3), cap[k])` with `cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}`, the adaptive `0.5×` reduction when energy is already well-conserved, and the dominance safeguard (`λ_E·L_energy > 10·L_data` → warn/reduce) — per M15.
- [x] **LOSS-03**: Framework specs define the Huber-δ calibration contract for the normalized-energy loss — δ selected from empirical `|ΔH|` quantiles with a `0.01–0.1` starting range, recorded per stage — per NS-13.
- [x] **LOSS-04**: Framework specs define the causal-training-mode contract per the **D-04** verdict — the chosen mode's batch-windowing, ALM locality, and loss-weighting structure; if Option C (time-windowed causal-ALM hybrid) is adjudicated, the overlapping-window partitioning, hard convergence gating, and state-propagation contract. The blueprint's Option-C recommendation is preserved unless the verdict downgrades it as an explicit, recorded human decision.

### Verification and Handoff (continuing v1.4 VER-01..06 / v1.5 VER-07..12)

- [ ] **VER-13**: Every v1.6 contract has a numerically-defined acceptance check naming its pass criterion, the data or expression it runs on, and the command or function that executes it — not just prose.
- [ ] **VER-14**: The roadmap maps every v1.6 requirement to exactly one phase, beginning at Phase 30.
- [ ] **VER-15**: The acceptance checks are **executed** using disposable probes — spec-consistency probes plus small formula-sanity probes (e.g., `tau_L`/`L_max`/`λ_E(k)`/clip-value behaviour on a documented sample) — each producing recorded pass/fail evidence. A failing check blocks phase completion and routes back to the originating phase; v1.6 does not ship while any required check fails. Probes never touch `pinn/` production code.
- [ ] **VER-16**: Every fix closes through the iterative re-verification loop: the issue ledger tracks each finding through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`; after each batch of edits, previously `VERIFIED` findings the batch could have regressed are re-verified and demoted on regression. The ledger lives at a stable path under the milestone's adjudication phase directory; nothing closes until all in-scope findings are `VERIFIED` or explicitly `DEFERRED` with a written blocker.
- [ ] **VER-17**: The milestone handoff identifies which findings were fixed, which were intentionally left unchanged, and which were deferred; FUT-01 (rebuild) and FUT-04 (resume training-loop implementation) divergence records are updated for every training-loop-implementation-shaped finding.
- [ ] **VER-18**: The remaining framework-spec Source-Issue (`SI-*`) entries relevant to curriculum and the training loop are reviewed for issue-03 relevance — each retired with a back-reference to the resolving phase/commit or preserved with a written reason. None is assumed resolved or assumed irrelevant.

## Future Requirements

Continuing from v1.4/v1.5 (see `.planning/milestones/v1.4-REQUIREMENTS.md` / `v1.5-REQUIREMENTS.md` for full text):

- **FUT-01**: Rebuild `pinn/` implementation code from the settled framework specs (now including the v1.6 curriculum/training-loop contracts).
- **FUT-02**: Recompute curriculum statistics and stage thresholds (the adaptive-assignment EDA run + stage-population calibration) after the contracts are finalized.
- **FUT-03**: Package useful disposable validation probes into reusable scripts under `pinn/validation/`.
- **FUT-04**: Resume PINN training-loop implementation (batch constructor, DataLoader stage queries, ALM, causal-mode mechanics, Stage-0 pilot calibration) after the framework specs are coherent.
- **FUT-05**: Adjudicate the author comments preserved by v1.4 Phase 22 (`22-COMMENT-HANDOFF.md`).

## Cross-Project Documentation Requirements

- **REQ-DOC-01** (cross-project): Markdown framework specs are the authoritative design documents during active work; LaTeX sources are publication/archive derivatives synced only at the final publication stage. (Full text in `.planning/milestones/v1.4-REQUIREMENTS.md`.)

## Scope Boundaries

| Scope | Status |
|-------|--------|
| **SCOPE-12** Locked v1.4 + v1.5 outcomes as grounding | **In scope as hard-constraint grounding** — the 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), the raw-mass `D ≈ 4.6416` convention (`D = 6.694` rejected by v1.5 Phase 25 EVID-10), and the v1.5 DataLoader/stage-query/validation-metric contracts (PIPE-01..10, VAL-01..04). v1.6 reconciles issue-03 against these; it does not re-open them absent new first-principles evidence surfaced through EVID-15. |
| **SCOPE-13** Spec-edit targets | **`ctl_instruction.md` + `pinn_architecture.md` only.** Curriculum staging, batch construction, stage transitions, loss scaling, and `tau_L`/`L_max` land in `ctl_instruction.md`; gradient clipping and training-strategy items in `pinn_architecture.md`. |
| **SCOPE-14** Training-loop code | **Out of scope — FUT-01/FUT-04 (trainex).** v1.6 transcribes the verbatim audit "Section 6" batch-construction pseudocode and the `training_step` structure as **normative spec contracts**; it does not implement the DataLoader, batch constructor, ALM update, or causal-window mechanics. |
| **SCOPE-15** Empirical EDA / Stage-0 pilot | **Out of scope — FUT/trainex.** The adaptive-stage-assignment EDA run over the dataset and the Stage-0 pilot threshold calibration are FUT. v1.6 specifies the methodology contracts and may run only **disposable formula-sanity probes** (e.g., `tau_L`/`L_max`/`λ_E` on a small sample) to test the contracts before locking. |
| **SCOPE-08** `sampling_method.md` (carried) | **Frozen by default** (user directive 2026-06-10) — the completed instruction file for the finished `simulation_data/` generation; revised ONLY on explicit user instruction triggered by verified data-feasibility issues. |
| **SCOPE-09** Read-only research reports (carried/extended) | **Read-only in v1.6** — `data_quality_assessment.md` (v1.5 carry) plus the curriculum-relevant `review-of-framework.md` and `stage-strat-revision.md` are characterized (PKG-08), never edited. They are research reports in `framework-revisions/`, not authoritative specs. |
| **SCOPE-10** `pinn/` live code (carried) | **Out of scope and NOT grounding** — the 2026-05-19 directive persists. Issue-03's "Canonical" citations of `data-processing-pipeline-full.py` and `basic_architecture.py` are overridden. Live-code references permitted only in forward-pointing FUT-01/FUT-04 hand-off documents. |

## Out of Scope

| Feature | Reason |
|---------|--------|
| Training-loop / DataLoader / ALM **implementation** | v1.6 settles design contracts; implementation is FUT-01/FUT-04 (trainex track). |
| Adaptive-stage-assignment EDA run + Stage-0 pilot calibration | Requires running over the dataset / a training run; FUT (SCOPE-15). |
| Brutus integrator changes | Issue-03 concerns curriculum and the training loop, not the validated C++ integrator. |
| Re-opening v1.4/v1.5 locked conventions | Hard-constraint grounding (SCOPE-12); only EVID-15 may revisit one with new first-principles evidence, surfaced as a gap. |
| Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md` | SCOPE-08 / SCOPE-09. |
| Data regeneration | Only via explicit user directive after verified data-feasibility findings; not assumed by any v1.6 fix. |
| LLM fine-tuning prep | Deferred until framework and data contracts are stable. |

## Traceability

Filled by roadmap creation (`.planning/ROADMAP.md`). Every v1.6 requirement maps to exactly one phase (satisfies VER-14), beginning at Phase 30. The Research Package Assembly phase (PKG-05..08) is first and ungated; its delivery opens the external resolution-doc gate. The Resolution Doc Readiness Verification phase (Phase 31, the v1.5 Phase 24.5 analog; operational, 0 requirement IDs) gates the adjudication phases. Phase 32 (EVID) stands up the ledger and adjudicates the headline conflicts before the contract phases transcribe verdicts; Phases 33 (CURR), 34 (LOOP), 35 (LOSS) carry the contracts; Phase 36 (VER) executes acceptance checks and writes the handoff.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PKG-05 | Phase 30 | Pending |
| PKG-06 | Phase 30 | Pending |
| PKG-07 | Phase 30 | Pending |
| PKG-08 | Phase 30 | Pending |
| EVID-11 | Phase 32 | Complete |
| EVID-12 | Phase 32 | Complete |
| EVID-13 | Phase 32 | Complete |
| EVID-14 | Phase 32 | Complete |
| EVID-15 | Phase 32 | Complete |
| CURR-01 | Phase 33 | Complete |
| CURR-02 | Phase 33 | Complete |
| CURR-03 | Phase 33 | Complete |
| CURR-04 | Phase 33 | Complete |
| CURR-05 | Phase 33 | Complete |
| LOOP-01 | Phase 34 | Complete |
| LOOP-02 | Phase 34 | Complete |
| LOOP-03 | Phase 34 | Complete |
| LOOP-04 | Phase 34 | Pending |
| LOOP-05 | Phase 34 | Complete |
| LOOP-06 | Phase 34 | Complete |
| LOOP-07 | Phase 34 | Pending |
| LOOP-08 | Phase 34 | Pending |
| LOSS-01 | Phase 35 | Complete |
| LOSS-02 | Phase 35 | Complete |
| LOSS-03 | Phase 35 | Complete |
| LOSS-04 | Phase 35 | Complete |
| VER-13 | Phase 36 | Pending |
| VER-14 | Phase 36 | Pending |
| VER-15 | Phase 36 | Pending |
| VER-16 | Phase 36 | Pending |
| VER-17 | Phase 36 | Pending |
| VER-18 | Phase 36 | Pending |

**Coverage:**

- v1.6 requirements: 32 total (4 PKG + 5 EVID + 5 CURR + 8 LOOP + 4 LOSS + 6 VER)
- Mapped to phases: **32/32** (Phase 30: 4 PKG; Phase 31: operational, 0 IDs; Phase 32: 5 EVID; Phase 33: 5 CURR; Phase 34: 8 LOOP; Phase 35: 4 LOSS; Phase 36: 6 VER). No orphans; no duplicates.
- Cross-project requirements: REQ-DOC-01 (not counted in v1.6 total)
- SCOPE-08 through SCOPE-15 are scope-boundary annotations, not numbered requirements.

---
*Requirements defined: 2026-06-17 (v1.6 milestone initialization, `/gsd-new-milestone`). Traceability table filled by roadmap creation 2026-06-17 (`.planning/ROADMAP.md`, Phases 30–36): 32/32 mapped, beginning at Phase 30, satisfying VER-14. Authored in the `milestone/v1.6` worktree off the v1.5 deliverable tip `88aa1e4f`.*
