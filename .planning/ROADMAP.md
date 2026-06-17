# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- 🚧 **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (in progress; planning)
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

---

## 🚧 v1.6 Resolving 03 Curriculum and Training Loop (Planning)

**Milestone Goal:** Critically examine each finding in `pinn_instruction/issues/03-curriculum-and-training-loop.md` — treating the issue doc as non-authoritative — against the user-produced external resolution doc (once it lands), the locked v1.4 (doc-01) and v1.5 (doc-02) conventions, the framework specs, and first principles; adjudicate the curriculum-staging and training-loop findings; apply evidence-backed edits limited to `ctl_instruction.md` and `pinn_architecture.md`; and verify each fix with disposable acceptance probes before closing. v1.6 settles the curriculum/training-loop **design contracts**; it does NOT implement training-loop code, run the adaptive-assignment EDA, or run the Stage-0 pilot calibration — those remain FUT-01/FUT-04 (the trainex track).

**Granularity:** standard
**Coverage:** 32/32 v1.6 requirements mapped (Phases 30–36; the readiness-verification phase 31 is operational and carries 0 requirement IDs)
**Branch:** `milestone/v1.6` (isolated worktree at `../3_body_problem-v1.6`, cut from the v1.5 deliverable tip `88aa1e4f`; rebased onto the completed `master` once v1.5's `--no-ff` merge + `/gsd-complete-milestone` land); tag `v1.6-pre-phase-NN` from branch HEAD before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.

### Source treatment & STOP protocol (applies to every phase)

- **Neither source is authoritative.** The issue doc (`03-curriculum-and-training-loop.md`) consolidates the 2026-04-27 audit (Sections 6–7), the Causal Training Mismatch blueprint, the stage-assignment methodology, and `next steps.txt` fragments, and carries known tensions (seed: `D = 6.694` against the v1.5-locked raw-mass `D ≈ 4.6416`; the issue doc's "Canonical" citations of `pinn/` live code). The forthcoming resolution doc is the **candidate verdict source** — same standing `ctl_pinn_resolution.md` had in v1.4 and `02-resolution-doc.md` had in v1.5 — transcribed unless evidence shows a position fails, never authoritative.
- **Grounding for v1.6 (SCOPE-12, hard-constraint):** the locked v1.4 framework-spec outcomes (14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, the PHYS-01 raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` with `D = 6.694` rejected by v1.5 Phase 25 EVID-10), the v1.5 DataLoader/stage-query/validation-metric data-side contracts (PIPE-01..10, VAL-01..04), v1.5-verified dataset facts, dataset documentation, prior user decisions, and short uncontroversial first-principles derivations. **`pinn/` live code is NOT grounding** (SCOPE-10) — issue-03's "Canonical" citations of `data-processing-pipeline-full.py` / `basic_architecture.py` are overridden; live-code references stay confined to forward-pointing FUT-01/FUT-04 hand-off documents.
- **Frozen / read-only spec targets (SCOPE-13):** edits land in `ctl_instruction.md` and `pinn_architecture.md` ONLY (curriculum staging, batch construction, stage transitions, loss scaling, and `tau_L`/`L_max` → `ctl_instruction.md`; gradient clipping and training-strategy items → `pinn_architecture.md`). `sampling_method.md` is frozen by default (SCOPE-08); `data_quality_assessment.md` (v1.5 carry) plus the curriculum-relevant `review-of-framework.md` and `stage-strat-revision.md` are read-only and only characterized (SCOPE-09).
- **Specwork only (SCOPE-14/15):** v1.6 transcribes the verbatim audit "Section 6" batch-construction pseudocode and the `training_step` structure as **normative spec contracts**; it does not implement the DataLoader, batch constructor, ALM update, or causal-window mechanics. The adaptive-stage-assignment EDA run over the dataset and the Stage-0 pilot threshold calibration are FUT; v1.6 may run only **disposable formula-sanity probes** to test contracts before locking.
- **STOP protocol in full** (AGENTS.md "CRITICAL GOVERNANCE"; v1.6 is a "similar adjudication milestone"): source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in phase-local `NN-GAPS.md` registers and the milestone index `.planning/milestones/v1.6-GAPS.md`; nothing is invented where sources are silent.

### Verification protocol (applies to every adjudication phase, 32–36)

Every selected finding follows the v1.4/v1.5-style loop:

1. **Adjudicate** — record an evidence packet (issue-doc citation by line range, resolution-doc verdict, current framework-spec evidence, and where relevant v1.5-verified dataset evidence) and an explicit verdict from `{accept-resolution, accept-issue-doc, accept-third-position, reject-both-as-unsupported, defer-with-blocker}`. Where sources conflict, perform root-cause adjudication (EVID-15) before editing.
2. **Fix** — apply the framework-spec edit to `ctl_instruction.md` / `pinn_architecture.md` only.
3. **Verify** — run the finding's numerically-defined acceptance check via a disposable probe (spec-consistency probe or small formula-sanity probe — e.g., `tau_L`/`L_max`/`λ_E(k)`/clip-value behaviour on a documented sample); probes never touch `pinn/`.
4. **Re-verify after every batch** — re-run the acceptance check on every previously `VERIFIED` finding the new batch could have regressed; any regression reverts that finding to `IN_PROGRESS`.
5. **Ledger discipline** — each finding moves `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (or `DEFERRED` with a written blocker) in the issue ledger held at a stable path under the Phase 32 (evidence-framework) directory. "Fix applied" is **not** closure; "the acceptance check passed" is. No phase exits with an in-scope finding still open.

## Phases

**Phase Numbering:**

- Integer phases (30, 31, …): planned v1.6 work, continuing from v1.5's Phase 29. Numbering does **not** reset.
- Decimal phases (e.g., 32.1): reserved for inserted checkpoints or urgent insertions (marked INSERTED), placed between their surrounding integers.

- [ ] **Phase 30: Research Package Assembly** — Assemble the annotated issue-03 document list and framed research questions (dataset figures marked "claimed, unverified" unless v1.5-verified; the three human-approval decisions D-04/D-05/D-06 and the `D = 6.694` conflict posed neutrally), plus a read-only characterization of `review-of-framework.md` and `stage-strat-revision.md`, then hand off for the user's external multi-AI research. First v1.6 phase, ungated; its delivery opens the external resolution-doc gate.

> ⛔ **External gate — resolution doc.** On Phase 30 delivery, the **USER** begins external multi-AI research (the ERW: multiple independent agents each produce a report from the package; one consolidation agent produces the resolution doc) and delivers it to `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`. The gate opens here, when package delivery starts the user's research. **Phase 31** (Resolution Doc Readiness Verification) verifies the consolidated resolution doc is ready before adjudication begins. Phases 32–36 (all adjudication and spec-edit work) **cannot start** until Phase 31 passes (which requires the consolidated doc landing). The doc is the candidate verdict source, not authoritative.

- [ ] **Phase 31: Resolution Doc Readiness Verification** — Verify the consolidated resolution doc covers every selected issue-03 finding, contains zero contradictions of v1.5-verified dataset facts, and respects all locked v1.4 + v1.5 conventions; produce a readiness report and a quick-reference resolution-doc map. Operational (0 requirement IDs; the v1.5 Phase 24.5 analog). Gates on the consolidated resolution doc landing; Phases 32–36 gate on this passing.

- [ ] **Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication** — Stand up the adjudication machinery (evidence packets, verdict set, false-positive/before-after notes) and the re-verification ledger, then perform root-cause adjudication of the headline conflicts before any spec edit lands: D-04 (causal training mode A/B/C), D-06 (epsilon strategy), D-05 (s_min frame), the M14 dual gradient-clipping divergence, and the cross-milestone `D = 6.694` vs the v1.5-locked `D ≈ 4.6416`.

- [ ] **Phase 33: Curriculum-Stage Contracts** — Transcribe the adjudicated curriculum-stage contracts into `ctl_instruction.md`: data-driven adaptive stage assignment, `tau_L`/`L_max` formulas, dual-path stage-transition criteria, the Stage 0–6 inventory/gating (incl. the M6 `L_norm` clamp guard), and the s_min stage-gate frame (per the D-05 verdict).

- [ ] **Phase 34: Training-Loop & Batch-Construction Contracts** — Transcribe the adjudicated training-loop contracts as normative spec contracts: replay/lookahead batch construction (B-07), two-independent-point-set separation (B-08), mixed time sampling, merged gradient clipping (M14), the ALM update + `μ_p` clamp, `dt_out`-aware collocation scaling (realizing v1.5 SCOPE-11), and the training-side use of SASD/IPR/PSC that v1.5 left provisional.

- [ ] **Phase 35: Loss & Energy-Weight Contracts** — Transcribe the adjudicated loss contracts: the loss-component scaling contract (NS-18), the capped-hybrid `λ_E` schedule (M15), the Huber-δ calibration (NS-13), and the causal-training-mode contract per the D-04 verdict (Option-C recommendation preserved unless downgraded by explicit human decision).

- [ ] **Phase 36: Acceptance Checks, Re-verification & Handoff** — Execute every contract's numerically-defined acceptance check via disposable probes, close the issue ledger to terminal state, reconcile the curriculum/training-loop `SI-*` entries, and write the FUT-01/FUT-04 handoff. Confirms 32/32 traceability (VER-14).

## Phase Details

### Phase 30: Research Package Assembly

**Goal**: Deliver a complete, framed research package for the user's external multi-AI research (ERW) — annotated document list, framed questions, and a read-only characterization of the two curriculum-relevant research reports — ready to hand off; on delivery, the milestone enters the external resolution-doc gate. The package is the milestone critical path (starting the external research gates all downstream adjudication), so it precedes adjudication and presents unverified dataset figures explicitly as issue-doc values marked "claimed, unverified".
**Depends on**: Nothing (first v1.6 phase; runs on `milestone/v1.6`). No external gate; no dependency on verification.
**Requirements**: PKG-05, PKG-06, PKG-07, PKG-08
**Success Criteria** (what must be TRUE):

  1. The package includes a complete annotated document list — every document needed to adjudicate the issue-03 findings, each with a role annotation; if the list would exceed ~5 files or context is scattered across fragments, the fragments are consolidated into a single context file (framework specs passed intact, never consolidated) and the consolidation is surfaced to the user before assembly (PKG-05).
  2. Each contested or unverified finding is posed as an explicit neutral research question, with the locked v1.4 conventions AND v1.5 data-pipeline/validation outcomes listed as hard constraints the research must respect (SCOPE-12); the three human-approval decisions — D-04 (causal training mode: per-time-step / global+ALM / time-windowed hybrid), D-05 (s_min frame), D-06 (epsilon strategy) — and the known cross-milestone `D = 6.694` vs `D ≈ 4.6416` conflict are posed without being settled (PKG-06).
  3. Every dataset/empirical figure stated in the package is explicitly marked "claimed, unverified" (the issue-doc value) unless already verified by v1.5 — figures verified by v1.5 (e.g., the 184 standard IDs without gold, the ~2,565 quasi-random gold count, per-variant snapshot/`dt_out` distributions) are stated as verified with their v1.5 citation; no unverified figure is presented as fact (PKG-07).
  4. `review-of-framework.md` and `stage-strat-revision.md` are characterized read-only (provenance, content map, and relation to the doc-03 findings), reported to the user with zero edits to either file (SCOPE-09 analog; PKG-08).
  5. The package is handed to the user, and the milestone records that the external resolution-doc gate is now open (user ERW research starts) and that adjudication Phases 32–36 gate on the consolidated resolution doc landing under `framework-revisions/research_reports/03-curriculum-and-training-loop/` and Phase 31 passing.
**Plans**: TBD
**UI hint**: no

### Phase 31: Resolution Doc Readiness Verification

**Goal**: Verify the consolidated resolution doc (from the user's external ERW research) is ready for use as the candidate verdict source in Phases 32–36. Produce a readiness report with pass/fail per check and fix instructions for any gap, plus a quick-reference map so downstream phases know where the resolution doc is, what each section covers, and how to cite it. (The v1.5 Phase 24.5 analog; given the next whole number rather than a decimal because it is a planned milestone phase, not an urgent insertion.)
**Depends on**: Phase 30 delivery **and the consolidated resolution doc landing** (external gate). Cannot start until the doc is present.
**Requirements**: Operational (supports EVID-11..15, CURR-01..05, LOOP-01..08, LOSS-01..04, VER-13..18); no new requirement IDs.
**Success Criteria** (what must be TRUE):

  1. Every issue-03 finding selected for remediation (B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, the human-approval decisions D-04/D-05/D-06, and the `D = 6.694` conflict) maps to a resolution-doc section (covered or partial; silent entries are flagged as gaps).
  2. The resolution doc shows no unexplained contradictions of v1.5-verified dataset facts or of the locked v1.4 + v1.5 conventions (SCOPE-12); scope observations — recommendations to change a locked convention — are recorded but are not failures.
  3. A resolution-doc quick-reference map exists providing enough information for Phase 32 to begin evidence-packet construction without reading the full resolution doc first.
  4. If any check fails, specific fix instructions are routed to the external consolidation agent via the readiness report, and Phases 32–36 remain blocked until the fix lands and re-check passes.
**Plans**: TBD
**UI hint**: no

### Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication

**Goal**: The adjudication machinery — evidence packets, verdict set, false-positive and before/after notes, root-cause conflict adjudication, and the re-verification ledger — is established, and the known cross-source conflicts are adjudicated at root cause before any spec edit lands. The contract phases (33–35) transcribe the verdicts this phase records.
**Depends on**: Phase 31 (resolution doc readiness verification). Cannot start until Phase 31 passes.
**Requirements**: EVID-11, EVID-12, EVID-13, EVID-14, EVID-15
**Success Criteria** (what must be TRUE):

  1. Each issue-03 finding selected for remediation has an evidence packet citing line ranges (never whole files) from the issue doc, the resolution-doc verdict, current framework-spec evidence, and (where relevant) v1.5-verified dataset evidence (EVID-11). *(Phase 32 authors packets/verdicts for the headline conflicts; packets for the remaining findings may be authored by the owning contract phase 33–35 immediately before its spec edits, recorded as a STOP-resolved split if the source materials do not pre-specify the split.)*
  2. Every selected finding carries an explicit verdict from the fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — with recorded reasoning (EVID-12).
  3. False positives in either source are documented as intentional non-changes naming why the current convention stands and which source(s) misread it (e.g., M6's `L_norm` clamp under the v1.4 Jacobi IC₁₃, which no longer carries `L_norm` as an IC slot — EVID-13), and every accepted finding carries a before/after note naming the changed spec section, the contract it now enforces, and the verification step (EVID-14).
  4. The headline conflicts are adjudicated at root cause (EVID-15) — D-04 causal training mode (Option A/B/C), D-06 epsilon strategy (`1e-5` everywhere / dual-context / `1e-10` everywhere), D-05 s_min frame, the M14 dual gradient-clipping divergence, and the `D = 6.694` vs v1.5-locked `D ≈ 4.6416` conflict (reconciled with v1.5 Phase 25 EVID-10 as the hard constraint) — each naming the root-cause ambiguity, which source was right and which wrong, and the convention now locked; the corresponding spec edits land in the contract phases (33–35).
  5. The issue ledger exists at its stable path under this (Phase 32, evidence-framework) directory, tracking every in-scope finding through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, with the explicit rule that "fix applied" is not closure and that each edit batch re-verifies previously `VERIFIED` findings it could have regressed.
**Plans**: TBD
**UI hint**: no

### Phase 33: Curriculum-Stage Contracts

**Goal**: `ctl_instruction.md` states one coherent set of curriculum-stage contracts — adaptive stage assignment, `tau_L`/`L_max` computation, dual-path stage transitions, the Stage 0–6 inventory/gating, and the s_min stage-gate frame — each grounded in the Phase 32 verdicts, the v1.5-verified dataset facts, and the locked v1.4/v1.5 conventions. Each contract is a spec contract; the EDA run and Stage-0 pilot calibration that would parameterize it are FUT (SCOPE-15).
**Depends on**: Phase 32 (consumes the evidence framework, the adjudicated verdicts, and the seeded ledger).
**Requirements**: CURR-01, CURR-02, CURR-03, CURR-04, CURR-05
**Success Criteria** (what must be TRUE):

  1. The data-driven adaptive stage-assignment methodology contract is defined (dataset EDA → PCA + K-means + quantile thresholds augmenting the static theoretical anchors; the >10%-per-stage population safeguard), with the actual EDA run explicitly marked FUT (SCOPE-15; CURR-01).
  2. The `tau_L` and `L_max` computation contracts are defined — `L_max = M_total · r_char · v_char`; `tau_L = 1/λ_max` via shadow-trajectory divergence with the split `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`, plus the fast PCA+Rosenstein batch approximation for ~15K trajectories — with the D value reconciled against the v1.5-locked convention (EVID-15) and M7 (`tau_L` excluded from the IC vector by design) recorded (CURR-02).
  3. The dual-path stage-transition criteria contract is defined — strict Path A (training plateau, validation stability, stage-dependent `ε_phys` and `ε_energy`) and fallback Path B (max-epochs, stagnation, NaN/Inf rollback) — with thresholds marked **provisional pending the FUT Stage-0 pilot calibration** (D5; CURR-03).
  4. The Stage 0–6 inventory and gating contract is defined (per-stage definitions, criteria, cumulative replay, Stage-6 catch-all, the M6 `np.clip(L_norm, 0, 1)` guard used in stage gating), consistent with v1.5-verified dataset facts; stage trajectory counts are cited as v1.5-verified or marked "claimed" where not yet grounded (CURR-04).
  5. The s_min frame for the curriculum **stage gate** is defined — unsoftened geometric `s_min` for the Stage-6 collision gate — per the D-05 adjudication; the loss-side softened `max(s_min, eps_soft)` is owned by LOSS (Phase 35), and the unsoftened value is always logged for diagnostics (CURR-05).
**Plans**: TBD
**UI hint**: no

### Phase 34: Training-Loop & Batch-Construction Contracts

**Goal**: `ctl_instruction.md` / `pinn_architecture.md` carry the training-loop and batch-construction contracts as normative spec contracts — replay/lookahead batch construction, two independent point sets, mixed time sampling, merged gradient clipping, the ALM update with `μ_p` clamp, `dt_out`-aware collocation scaling, and the training-side use of the v1.5-provisional metrics — each reconciled with the Phase 32 verdicts and the locked v1.4/v1.5 conventions. Implementation is FUT-01/FUT-04 (SCOPE-14).
**Depends on**: Phase 32 (verdicts + ledger). Sequenced after Phase 33 to manage shared spec sections and regressions; the D-04 causal-mode verdict from Phase 32 constrains LOOP-01.
**Requirements**: LOOP-01, LOOP-02, LOOP-03, LOOP-04, LOOP-05, LOOP-06, LOOP-07, LOOP-08
**Success Criteria** (what must be TRUE):

  1. The replay/lookahead batch-construction contract is defined (`B_replay = 240` from `D_≤k` + `B_lookahead = 16` from `D_{k+1}`, with the `has_stage(k+1)` guard) per B-07 / audit Section 6, reconciled with the D-04 causal-mode verdict (a windowed mode excludes future-window trajectories); implementation marked FUT-01 (LOOP-01).
  2. The two-independent-point-set contract is defined — data-fidelity points (8192 from Brutus snapshots, L1/MAE loss) kept separate from collocation points (4096 from `[0,T]`, physics + energy loss), even when they share trajectory IDs — per B-08 (LOOP-02); and the mixed time-sampling contract (50% uniform + 50% acceleration-weighted) is applied to **both** point sets per audit Section 6.1 (LOOP-03).
  3. The merged gradient-clipping contract is defined — `clip_value = C_stage · median(grad_norm_history)` with the per-stage `C_table` (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0) and a rolling window — per M14 (LOOP-04); and the ALM parameter-update contract is defined — `λ_p`/`μ_p` RMSprop-style moving-average update under `torch.no_grad()`, with the `μ_p` clamp `[1e-4, 100]` — per the audit ALM specification and the MINOR clamping finding (LOOP-05).
  4. The `dt_out`-aware collocation-scaling contract is defined — `n_col ∝ dt_base / dt_out` (audit M16 line-163 verbatim direction; the inverse form is an explicit future methodology change, not transcribed) — **realizing the v1.5 SCOPE-11 / PIPE-08 forward-reference** (LOOP-06).
  5. The training-side use of the v1.5-provisional metrics is defined — IPR as the ALM convergence / noise-floor (v1.5 VAL-03 forward-reference; provisional `1e-3` confirmed or recalibrated) and PSC for replay-buffer governance (v1.5 VAL-04 forward-reference; provisional grid/normalization/SCR confirmed or recalibrated) per LOOP-07, plus SASD training-side collocation-weighting (v1.5 VAL-02 deferral) per LOOP-08.
**Plans**: TBD
**UI hint**: no

### Phase 35: Loss & Energy-Weight Contracts

**Goal**: `ctl_instruction.md` carries the loss-component, energy-weight, Huber-δ, and causal-training-mode contracts — the loss scaling contract, the capped-hybrid `λ_E` schedule, the Huber-δ calibration, and the D-04 causal-mode contract — each reconciled with the Phase 32 verdicts and the locked v1.4/v1.5 conventions.
**Depends on**: Phase 34 (shares loss/energy spec sections; the LOOP collocation/point-set contracts feed the loss-component scaling contract; the D-04 verdict from Phase 32 shapes LOSS-04).
**Requirements**: LOSS-01, LOSS-02, LOSS-03, LOSS-04
**Success Criteria** (what must be TRUE):

  1. The loss-component scaling contract is defined — `L_data`, `L_physics`, `L_energy` all evaluated in the same dimensionless coordinate system (`t_τ ∈ [-1,1]`, `r' = r/D`), with the AD chain-rule factors (`d²r'/du² = 4·d²r'/dτ²`, `dr'/du = 2·dr'/dτ`) cross-linked to their canonical doc-01 location — per NS-18 (LOSS-01).
  2. The capped-hybrid energy-loss-weight schedule is defined — `λ_E(k) = min(10^(k-3), cap[k])` with `cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}`, the adaptive `0.5×` reduction when energy is already well-conserved, and the dominance safeguard (`λ_E·L_energy > 10·L_data` → warn/reduce) — per M15 (LOSS-02).
  3. The Huber-δ calibration contract for the normalized-energy loss is defined — δ selected from empirical `|ΔH|` quantiles with a `0.01–0.1` starting range, recorded per stage — per NS-13 (LOSS-03).
  4. The causal-training-mode contract is defined per the D-04 verdict — the chosen mode's batch-windowing, ALM locality, and loss-weighting structure; if Option C (time-windowed causal-ALM hybrid) is adjudicated, the overlapping-window partitioning, hard convergence gating, and state-propagation contract — with the blueprint's Option-C recommendation preserved unless the verdict downgrades it as an explicit, recorded human decision (LOSS-04).
**Plans**: TBD
**UI hint**: no

### Phase 36: Acceptance Checks, Re-verification & Handoff

**Goal**: Every v1.6 contract has an executed, numerically-defined acceptance check; the issue ledger closes to terminal state; the curriculum/training-loop `SI-*` entries are reconciled; and the handoff records what was fixed, left unchanged, and deferred, with FUT-01 (rebuild) and FUT-04 (training-loop) divergence updated.
**Depends on**: Phases 32–35 (all adjudication and spec edits complete).
**Requirements**: VER-13, VER-14, VER-15, VER-16, VER-17, VER-18
**Success Criteria** (what must be TRUE):

  1. Every v1.6 contract has a numerically-defined acceptance check naming its pass criterion, the data or expression it runs on, and the command or function that executes it — not just prose (VER-13).
  2. The acceptance checks are **executed** with disposable spec-consistency and small formula-sanity probes (e.g., `tau_L`/`L_max`/`λ_E(k)`/clip-value behaviour on a documented sample), each producing recorded pass/fail evidence; a failing check blocks phase completion and routes back to the originating phase, and no probe touches `pinn/` production code (VER-15).
  3. Every fix closes through the iterative re-verification loop: the issue ledger reaches terminal state — all in-scope findings `VERIFIED` or explicitly `DEFERRED` with a written blocker — with previously `VERIFIED` findings re-verified and demoted on regression after each edit batch (VER-16).
  4. The milestone handoff identifies which findings were fixed, which were intentionally left unchanged, and which were deferred; FUT-01 and FUT-04 divergence records are updated for every training-loop-implementation-shaped finding (VER-17); and the remaining curriculum/training-loop `SI-*` entries are each reviewed for issue-03 relevance and either retired with a back-reference to the resolving phase/commit or preserved with a written reason — none assumed resolved or assumed irrelevant (VER-18).
  5. Roadmap traceability is confirmed at closure: all 32 v1.6 requirements map to exactly one phase, beginning at Phase 30 (VER-14).
**Plans**: TBD
**UI hint**: no

## Progress

**Execution Order:** 30 → ⛔gate opens (user ERW research starts) → 31 readiness check → 32 (evidence + conflict adjudication) → 33 (curriculum) → 34 (training-loop) → 35 (loss) → 36 (acceptance + handoff).

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 30. Research Package Assembly | v1.6 | 0/0 | Not started | - |
| 31. Resolution Doc Readiness Verification | v1.6 | 0/0 | Not started | - |
| 32. Evidence Framework, Issue Ledger & Conflict Adjudication | v1.6 | 0/0 | Not started | - |
| 33. Curriculum-Stage Contracts | v1.6 | 0/0 | Not started | - |
| 34. Training-Loop & Batch-Construction Contracts | v1.6 | 0/0 | Not started | - |
| 35. Loss & Energy-Weight Contracts | v1.6 | 0/0 | Not started | - |
| 36. Acceptance Checks, Re-verification & Handoff | v1.6 | 0/0 | Not started | - |

---
*Last updated: 2026-06-17 — v1.6 roadmap created (`/gsd-new-project` roadmapper). 7 phases (30–36), standard granularity, continuing numbering from v1.5's Phase 29. 32/32 v1.6 requirements mapped (PKG=4, EVID=5, CURR=5, LOOP=8, LOSS=4, VER=6); Phase 31 readiness verification is operational (0 IDs). Package-first → readiness-gate → conflict-adjudication-then-contracts → acceptance/handoff ordering mirrors v1.5. Authored in the `milestone/v1.6` worktree off the v1.5 deliverable tip `88aa1e4f`.*
