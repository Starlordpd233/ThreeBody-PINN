# Codebase Concerns & Risks Audit

**Original Analysis Date:** 2026-04-27
**Last Refreshed:** 2026-06-10
**Scope:** Full repository audit for technical debt, architecture risks, security, data quality, and process issues.
**Severity Scale:** BLOCKER > CRITICAL > MAJOR > MINOR > INFO

> **How to read the status annotations (2026-06-10 refresh).**
> This audit is a hand-curated base with stable finding IDs (B-#, C-#, M-#, D-#, Q-#, P-#, S-#). The 2026-06-10 refresh did **not** regenerate findings or drop any. It updated each finding's **status line** against planning artifacts and framework specs.
>
> **Governance rule applied (STOP protocol):** A physics/spec finding is marked "spec-resolved" **only** where a planning artifact or framework spec **explicitly** says so — citing the artifact. The agent did **not** re-derive any physics or judge correctness on its own. Where v1.4 locked a convention that differs from this audit's originally-proposed fix, the status records that the convention was *adjudicated and locked* (see the cited evidence packet) — **not** that this audit's proposed number was "right." The live `pinn/` code is v1.3-era, **not** spec-authoritative, and slated for the FUT-01 rewrite; a code↔spec divergence is itself a tracked concern, never a resolution.
>
> **Milestone context:** v1.4 ("Resolving 01 Architecture and Physics Foundations," Phases 16–22) **shipped 2026-06-09** and merged to master — it constructed/repaired the framework specs and closed 32/32 requirements and 25/25 STOP gaps (`.planning/MILESTONES.md`, `.planning/milestones/v1.4-REQUIREMENTS.md`, `.planning/milestones/v1.4-GAPS.md`). v1.5 ("Resolving 02 Data Pipeline and Validation," Phases 23–29) is **IN PROGRESS** on branch `milestone/v1.5`, currently at Phase 23 (research-package assembly); **no resolution doc exists yet** and adjudication phases have not started (`.planning/REQUIREMENTS.md`).

---

## Executive Summary

This is a research / spec-engineering codebase. The simulation data pipeline functions and produces valid Brutus outputs. The PINN/ML layer has **not been built** — there is no training loop, no LLM integration, and no end-to-end pipeline connecting simulation data to model training (`PROJECT.md`: "architecture exists, training does not").

The 2026-04-27 pre-implementation audit identified **11 critical blockers** plus supporting findings. The v1.4 milestone addressed the **architecture & physics foundations** (Issue 01) by **constructing authoritative framework specifications** at `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` and `pinn_architecture.md`, locking the contested conventions through the EVID-05 adjudication and STOP-gap protocols. The **data-pipeline and curriculum findings** (Issues 02 and 03) are **not yet resolved**: Issue 02 is the subject of the in-progress v1.5 milestone (no resolution doc yet), and Issue 03 (curriculum/training-loop) has no dedicated milestone.

**Crucial nuance for every spec finding below:** v1.4 resolved the **spec/documentation** side. It did **not** touch the live `pinn/` implementation (FUT-01 owns that). So the original "code is wrong" half of each blocker generally **remains open as a code↔spec divergence** until FUT-01.

**Overall Readiness:** Framework specs for Issue 01 are locked and verified. Data-pipeline contracts (Issue 02) are mid-verification. No training code may be written until the data contracts land and FUT-01 aligns the code.

---

## 1. BLOCKER: Critical Technical Issues

### B-1: Characteristic Length D — Convention Adjudicated in Spec; Code Divergence Remains

**What (original):** `pinn/data-processing-pipeline-full.py:142` computes `self.D = np.cbrt(self.G * self.T_max**2)` (≈4.64); this audit originally argued the correct value must include `M_tot=3` → 6.694.

**Status as of 2026-06-10:** Spec side **adjudicated and locked** by v1.4. The D formula was an explicit EVID-05 conflict ("B-02 D formula", `.planning/milestones/v1.4-REQUIREMENTS.md` EVID-05), resolved under **PHYS-01** (Phase 19, Complete): the framework specs "lock the raw-mass nondimensionalization convention and retain `D=(G*T^2)^(1/3)` unless a full mass-fraction rewrite is explicitly chosen later." The adjudication record lives in the Phase 16 evidence packet / issue ledger (`.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`).
**Governance note:** the locked convention is **not** necessarily this audit's originally-proposed 6.694 fix — consult the evidence packet for the adjudicated definition; do not assume this finding's original number was endorsed. The **live-code value remains a code↔spec divergence** for FUT-01.

**Severity:** BLOCKER (spec contract locked; code alignment deferred to FUT-01)

### B-2: AD Chain-Rule Factor — Derivative Contract Locked in Spec; Code Divergence Remains

**What (original):** Time normalization (τ = 2t/T − 1) requires chain-rule conversion of AD derivatives (factor 2 for velocity, 4 for acceleration); `pinn/basic_architecture.py` did not implement them, so kinetic energy and residual accelerations were wrong by 4×.

**Status as of 2026-06-10:** Spec side **resolved** by **PHYS-02** (Phase 19, Complete, `.planning/milestones/v1.4-REQUIREMENTS.md`): framework specs "define the normalized-time derivative contract, naming the autograd leaf explicitly (`u=t/T` or `tau=2u-1`) and specifying the chain-rule factors when the leaf differs from `u`," require **componentwise** derivatives (not `grad_outputs=torch.ones_like(...)`), and include the synthetic-trajectory worked example `r'(u)=[sin(2πu),cos(2πu),u²]`. This contract was **executed** as acceptance probe §10.3 under VER-04 (Phase 21, Complete). The **live-code 4× bug remains a code↔spec divergence** for FUT-01.

**Severity:** BLOCKER (spec contract locked; code alignment deferred to FUT-01)

### B-3: No Training Loop Exists

**What:** `pinn/basic_architecture.py` defines the SQR-SkipResNet-SIREN model only — no training loop, loss implementation, data loading, optimizer, or evaluation. `pinn/data-processing-pipeline-full.py` has stage assignment and batch construction but no training loop.

**Status as of 2026-06-10:** **Still open.** Confirmed by `PROJECT.md` ("Data pipeline: get PINN training loop working end-to-end (architecture exists, training does not)") and explicitly deferred to **FUT-01** ("Update existing `pinn/` implementation code and build the broader PINN training loop after framework-spec reconciliation is complete," `.planning/milestones/v1.4-REQUIREMENTS.md`). v1.4 deliberately built no code.

**Severity:** BLOCKER

### B-4: SIREN Init Formula — Spec Stated Consistently in v1.4; Doc Corruption Fixed

**What (original):** The PINN doc (`main_pinn.pdf` Table 1) specified hidden-layer init `U[-ω₀√(6/n), ω₀√(6/n)]` (multiplies by ω₀ → variance explosion), while code at `pinn/basic_architecture.py:37` correctly divides by ω₀.

**Status as of 2026-06-10:** Spec side **resolved** by **ARCH-01** (Phase 20, Complete): "SIREN initialization and frequency settings are stated consistently, with no epochwise `omega0` scheduler unless a reparameterized runtime mechanism is specified" (`.planning/milestones/v1.4-REQUIREMENTS.md`). A residual corruption in the very same weight-init table (`pinn_architecture.md:263`, `designe`→`designed` + fused Value/Rationale cell) was caught by the Phase 22 content-equivalence audit and **fixed in commit `bf841f6`** (GAP-22-04, `.planning/milestones/v1.4-GAPS.md`). Authoritative spec is now `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (no longer `main_pinn.pdf`).

**Severity:** BLOCKER → spec-resolved (documentation); historical, retained for traceability.

### B-5: Input Vector Dimensionality — Canonical 14D Locked in Spec

**What (original):** LaTeX docs claimed 12D/13D/14D simultaneously; code produces a 13-component IC (+ time = 14D); CTL described 11D. No authoritative count existed.

**Status as of 2026-06-10:** Spec side **resolved** by **IO-01/IO-02/IO-04** (Phase 17, Complete, `.planning/milestones/v1.4-REQUIREMENTS.md`): framework specs state one canonical input contract `14D = [tau, IC_13]`; define the 13-component Jacobi-state IC vector in one consistent order (ordered raw mass slots, Jacobi positions/velocities, energy, per-slot normalization); and remove or label-as-historical any obsolete 11D/12D/ambiguous wording. The **live-code IC composition remains a code↔spec divergence** for FUT-01 (the spec's Jacobi IC₁₃ differs from the v1.3 code's vector).

**Severity:** BLOCKER (spec contract locked; code alignment deferred to FUT-01)

---

## 2. CRITICAL: Architecture & Physics Issues

### C-1: Softening Parameter Mismatch — Strategy Adjudicated in Spec

**What (original):** CTL used ε = 1e-10 for static invariants; PINN used ε_soft = 1e-5 for dynamic loss; pipeline code at `pinn/data-processing-pipeline-full.py:594` used 1e-10. Curriculum sorting and training physics disagreed.

**Status as of 2026-06-10:** Spec side **resolved** by **PHYS-03** (Phase 19, Complete): framework specs "use a matched softened force/potential pair for physics residuals and energy regularization, with any offline invariant epsilon kept separate from training-time numerical softening," with the value "locked only after EVID-05 adjudication" — and "B-09 softening strategy" is one of the named EVID-05 conflicts (`.planning/milestones/v1.4-REQUIREMENTS.md` EVID-05/PHYS-03). The matched force/energy pair was exercised by acceptance probe §10.4 (VER-04, Phase 21).
**Governance note:** the locked value/strategy is whatever the evidence packet recorded — not necessarily this audit's originally-suggested ε = 1e-8. The **live-code ε remains a code↔spec divergence** for FUT-01.

**Severity:** CRITICAL (spec contract locked; code alignment deferred to FUT-01)

### C-2: COM Frame Inconsistency — Preprocessing Order Locked in Spec

**What (original):** Standard ICs have exact COM=0; hierarchical ICs carry a Gaussian-perturbation COM offset (median |COM|≈9e-3). Pipeline `verify_com_frame()` (`pinn/data-processing-pipeline-full.py:534-551`) only warns; no mass-consistency check between IC and Brutus COM scripts.

**Status as of 2026-06-10:** Spec side **resolved** by **FRAME-01/FRAME-02/FRAME-03** and **IO-03** (Phases 17–18, Complete, `.planning/milestones/v1.4-REQUIREMENTS.md`): one preprocessing order is locked (COM recentering → zero-momentum boost → canonical ordering → canonical rotation gauge → scaling); COM/total-momentum assertions are stated for preprocessed samples and model outputs; the hierarchical post-perturbation COM offset is reconciled with the sampling spec; and a **mass-weighted COM projection on the raw 9D position head** is required before any loss consumes the output. COM invariance was exercised by acceptance probe §10.2 (VER-04, Phase 21). The **live-code "warn-only" behavior remains a code↔spec divergence** for FUT-01.

**Severity:** CRITICAL (spec contract locked; code alignment deferred to FUT-01)

### C-3: Non-Contiguous IDs Break Curriculum Mapping

**What:** Standard dataset has ~31% ID gaps, hierarchical ~2.9%. Stage assignment in `pinn/data-processing-pipeline-full.py:991-1020` iterates a trajectory list and assigns in-place without an `id_to_path` map; list-index access can map wrong IDs.

**Status as of 2026-06-10:** **Tracked; not resolved.** This is a data-pipeline (Issue 02) concern. v1.5 is verifying the underlying ID-gap claims empirically (**DATA-01**: "ID-gap claims are verified against the on-disk dataset … with recorded counts and the counting method," `.planning/REQUIREMENTS.md`) but the milestone is at Phase 23 (research-package assembly) with **no resolution doc and no adjudication yet**. The pipeline fix itself (build `id_to_path` / `TrajectoryIndex`) belongs to FUT-01 code work, not yet performed.

**Severity:** CRITICAL

### C-4: Missing Stage 4-to-5 Validation Gate

**What:** `calculate_metrics.py` emits metrics for all Brutus files including partial/errored runs; the only validity signal (`final_timestep >= 9.5`) runs once at Stage 3; no snapshot-count minimum is enforced for Lyapunov-dependent stages.

**Status as of 2026-06-10:** **Tracked; not resolved.** Data-pipeline/validation (Issue 02) territory under in-progress v1.5; no resolution doc yet (`.planning/REQUIREMENTS.md`). The `TrajectoryValidator` gate is unbuilt (FUT-01).

**Severity:** CRITICAL

### C-5: Stage Transition Criteria Theoretically Unattainable

**What:** CTL requires monotonically-decreasing validation loss for stage advancement; with ~7,600 ICs and Adam, strict monotonicity is unattainable, blocking curriculum progression.

**Status as of 2026-06-10:** **Tracked; not resolved.** This is a curriculum/training-loop concern (Issue 03, `pinn_instruction/issues/03-curriculum-and-training-loop.md`). **No milestone has been opened for Issue 03**; v1.4 covered Issue 01 and v1.5 covers Issue 02 only. The planning artifacts are silent on a fix.

**Severity:** CRITICAL

### C-6: Energy Loss Weight Schedule Risks Late-Stage Destabilization

**What:** CTL Table 3 specifies λ_E = 1000 at Stage 6, potentially drowning the physics residual and turning the loss into a pure energy-conservation optimizer.

**Status as of 2026-06-10:** **Tracked; not resolved.** Curriculum/training-loop (Issue 03) — no milestone opened. Note: v1.4 PHYS-04/05/06 and the §10.5 loss-stability dry-run touched loss-balancing *semantics* at the spec level, but the **stage-wise λ_E schedule magnitude** is curriculum content not adjudicated in v1.4; planning artifacts do not record a fix.

**Severity:** CRITICAL

---

## 3. MAJOR: Technical Debt

### M-1: No Dependency Management

**What:** No `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, or `environment.yml`. A `.venv/` exists (Python 3.12.2) with no reproducibility manifest. `.gitignore` excludes `.venv/`.

**Status as of 2026-06-10:** **Still open — re-verified.** A repo scan on 2026-06-10 found none of the manifest files; `.venv/` is present. No planning artifact has addressed dependency pinning (FUT-01 territory).

**Fix:** Generate a pinned `requirements.txt` from the active `.venv/`.

**Severity:** MAJOR

### M-2: Dual Data Pipeline — Two Competing Implementations

**What:** `pinn/data-processing-pipeline-full.py` (monolithic, ~1,650 lines) vs. `pinn/data-handling/` (modular, partial). Both contain parsing, invariants, stage assignment, batch construction; the modular package copies rather than shares logic.

**Status as of 2026-06-10:** **Tracked; not resolved.** Both are v1.3-era live code, frozen as non-grounding for v1.4/v1.5; consolidation is FUT-01 scope. No planning artifact has reconciled them.

**Severity:** MAJOR

### M-3: 2,847-Line `next steps.txt` — Mostly Superseded

**What:** `pinn_instruction/issues/archive/next steps.txt` (128KB) is ~80% superseded by the 2026-04-27 audit.

**Status as of 2026-06-10:** **Resolved/archived** — consolidated under the v1.2 Phase 9 issues-consolidation work (`.planning/MILESTONES.md` v1.2) and the v1.4 Phase 22 author-comment census; the file lives in `archive/` and is retained for provenance only.

**Severity:** MAJOR → INFO (archived)

### M-4: Hardcoded Machine-Specific Paths in Brutus Makefile

**What:** `brutus_Newton-main/makefile` hardcodes `BREW_PREFIX = /opt/homebrew`, `HOME_DIR = <home>`, `MPRLIB = $(HOME_DIR)/src/mpreal`.

**Status as of 2026-06-10:** **Still open.** Outside v1.4/v1.5 scope; no planning artifact addresses it.

**Severity:** MAJOR

### M-5: No Reproducibility — Missing Seeds and Random State

**What:** IC generation uses scrambled Sobol sequences (`simulation_data/Scripts/ic_generation/ic_generation_utils.py`) with no fixed seed in the runner scripts.

**Status as of 2026-06-10:** **Tracked.** v1.5's empirical-verification scope (e.g. SAMP/DATA requirements, `.planning/REQUIREMENTS.md`) characterizes the existing dataset but treats `sampling_method.md` and the generated data as **frozen** (the dataset will not be regenerated, per the 2026-06-10 `sampling_method.md` freeze directive). The seed gap remains a documented reproducibility limit of the historical dataset rather than an active fix target.

**Severity:** MAJOR

### M-6: Blacklist Not Enforced in PINN Pipeline

**What:** `simulation_data/Documentation/problematic_ics_blacklist.json` (65 IDs) is enforced by the Brutus runners but NOT loaded by `pinn/data-processing-pipeline-full.py`.

**Status as of 2026-06-10:** **Tracked; under empirical re-verification in v1.5.** **DATA-02** verifies the blacklist — locates `problematic_ics_blacklist.json`, confirms/corrects the 65-ID claim, and records consumption status "within grounding limits: `simulation_data/Scripts/` runners are grounding; `pinn/` is not" (`.planning/REQUIREMENTS.md`). The pipeline enforcement fix is FUT-01.

**Severity:** MAJOR

### M-7: Pickle Used for Batch Serialization

**What:** `pinn/data-processing-pipeline-full.py:1585-1586`, `pinn/data-handling/scripts/prepare_training_data.py:193-194`, and `pinn/data-handling/core/parsing.py:407,442` use pickle for batch files.

**Status as of 2026-06-10:** **Still open.** Live-code serialization choice; FUT-01 territory. No planning artifact addresses it.

**Severity:** MAJOR

### M-8: Thin Test Coverage (governance/phase tests now exist; pipeline tests do not)

**What (original):** Only `simulation_data/Data/testing_data/test_pipeline.py` existed; no tests for `pinn/`, IC generation, parsing, invariants, or stage assignment.

**Status as of 2026-06-10:** **Partially changed — keep open for pipeline code.** A top-level `tests/` directory now exists, but it holds **governance/process and phase-acceptance** tests, not data-pipeline unit tests: `tests/git_policy/test_git_policy.py`, `tests/test_phase12_validation.py`, and a compiled `tests/__pycache__/test_v1_4_acceptance.cpython-312.pyc` (v1.4 acceptance probes). v1.4's VER-04 disposable probes validated the **specs**, explicitly **not** the v1.3-era code. So there is **still no unit-test coverage for `pinn/` data-pipeline logic** (D computation, COM verification, invariants, stage assignment). The regression-catching gap that would have flagged the D bug remains.

**Severity:** MAJOR

### M-9: 1650-Line Monolithic Data Pipeline

**What:** `pinn/data-processing-pipeline-full.py` (~1,650 lines, ~30 functions/classes) mixes parsing, scaling, invariants, stage assignment, batch construction, and I/O.

**Status as of 2026-06-10:** **Still open.** Live-code structure; FUT-01 modularization target. No planning artifact addresses it.

**Severity:** MAJOR

---

## 4. MAJOR: Documentation Gaps & Inconsistencies

### D-1: Input Vector Orientation Encoding — Adjudicated/Reframed in Spec

**What (original):** Two competing proposals for the 13-component IC: 2026-04-27 audit's 5 trig values vs. Causal_Trainingmismatch's 3 shape invariants + 2 direction cosines. Both 14D total but different IC composition.

**Status as of 2026-06-10:** Spec side **resolved/reframed** by **IO-02** (Phase 17, Complete): the framework specs define the IC vector as a **Jacobi-state** vector and declare that "**shape invariants and orientation summaries are metadata only, not final network IC slots**" (`.planning/milestones/v1.4-REQUIREMENTS.md` IO-02). The orientation conflict was an EVID-05 item ("B-04 input-vector orientation slots") and its Source-Issue entry was retired under VER-06 (`SI-PINN-001 ↔ B-04`). The adjudication record is in the Phase 16/17 evidence packet.

**Severity:** MAJOR → spec-resolved (reframed); retained for traceability.

### D-2: I_norm Definition — Raw vs. Bounded Names Separated in Spec

**What (original):** CTL text defines I_norm = tr(I)/(M·r_char²); some old code listings applied `tanh()`, risking double-normalization. Current pipeline does not apply `tanh`.

**Status as of 2026-06-10:** Spec side **resolved** by **ARCH-04** (Phase 20, Complete): "`I_norm` uses separate names for the raw inertia descriptor and the tanh-squashed network input" (`.planning/milestones/v1.4-REQUIREMENTS.md`). The evidence/proof vehicle was added via GAP-20-01 (Phase 16 ledger row `D-02-NORM`, `AC-ARCH-04`, `evidence/D-02-NORM.md`, `ctl_instruction.md`; `.planning/milestones/v1.4-GAPS.md`).

**Severity:** MAJOR → spec-resolved; retained for traceability.

### D-3: Standard Gold Standard Provenance Unknown

**What:** No runner targets `brutus_output/brutus_standard_quasi_random_gold_standard/`; its 2,565 files were produced externally (184 fewer than the base standard IC folder).

**Status as of 2026-06-10:** **Tracked; under empirical scope in v1.5.** Gold-standard provenance/coverage is part of the dataset characterization v1.5 performs against the on-disk data (SCOPE-06/07; DATA-series requirements, `.planning/REQUIREMENTS.md`). Not yet adjudicated.

**Severity:** MAJOR

### D-4: PINN vs. LLM Direction — Clarified in PROJECT.md

**What (original):** Unclear whether the project targets PINN or LLM; `PROJECT.md` stated the relationship was TBD.

**Status as of 2026-06-10:** **Largely clarified.** `PROJECT.md` now frames the project as a **Physics-Informed LLM**: it generates Brutus data and "uses that data to fine-tune a language model (Qwen 3.5 2B)," with the SQR-SkipResNet-SIREN PINN architecture as an existing component and data integrity feeding "everything downstream (PINN or LLM training)." The near-term roadmap is data pipeline → PINN training loop → LLM fine-tuning. The **PINN→LLM bridge mechanics remain future work**, but the strategic direction is no longer "TBD."

**Severity:** MAJOR → MINOR (direction clarified; bridge still future).

### D-5: Author-Flagged Uncertainties in Framework Specs — Census Deferred to FUT-05

**What (original):** CTL/PINN docs contained author-flagged uncertainties (originally mis-counted as "28 `\authcomment`").

**Status as of 2026-06-10:** **Tracked; adjudication deferred by explicit user decision.** v1.4 Phase 22 **censused and preserved verbatim** every author-flagged comment (any form/format), retiring the "28 `\authcomment`" mis-census (GAP-22-02), and **deferred per-comment disposition** to new requirement **FUT-05** via `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md` (GAP-22-01; `.planning/milestones/v1.4-GAPS.md`, `.planning/milestones/v1.4-REQUIREMENTS.md` FUT-05). The comments are catalogued, not yet resolved.

**Severity:** MAJOR → tracked under FUT-05.

---

## 5. MODERATE: Data Quality Risks

> All Q-# findings concern the on-disk dataset (`simulation_data/`), which is **frozen** and is **grounding** for v1.5 (SCOPE-06/07). v1.5 empirically re-verifies several of these claims; until those verifications complete and a resolution doc lands, they remain **tracked**.

### Q-1: 184 Standard IDs Missing Gold Counterpart

**What:** 184 standard quasi-random IDs lack a gold-standard Brutus output (`simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`); Stage 5 needs gold data.

**Status as of 2026-06-10:** **Tracked.** Part of v1.5 dataset characterization; Stage-5 fallback handling is FUT-01.

**Severity:** MODERATE

### Q-2: Brutus Footer Schema Heterogeneity

**What:** Result footers come in 3 schemas (full / no-eta / minimal); 219 minimal-footer files in the standard gold folder. Parsers must handle optional fields with folder-default fallback (`simulation_data/Documentation/README.md`).

**Status as of 2026-06-10:** **Tracked.** Empirical-verification scope in v1.5.

**Severity:** MODERATE

### Q-3: 31.2% Gap Rate in Standard Dataset

**What:** ~1,250 gaps in 4,000 standard IDs.

**Status as of 2026-06-10:** **Under direct empirical verification in v1.5** — **DATA-01** verifies the exact claim "1,250 gaps / 4,000 standard quasi-random; 143 / 5,000 hierarchical" against the on-disk dataset with recorded counts and method (`.planning/REQUIREMENTS.md`). Counting not yet executed (Phase 23 precedes verification per PKG-03). Linked to C-3 (pipeline handling, FUT-01).

**Severity:** MODERATE

### Q-4: Brutus Timeout Produces Orphaned Partial Outputs

**What:** 3000s timeout; failed sims have partial output deleted and IC moved to `problematic_ics/`; no resume mechanism.

**Status as of 2026-06-10:** **Tracked; historical.** Pertains to the frozen data-generation pipeline; no active fix (dataset is frozen).

**Severity:** MODERATE

### Q-5: Parameter Heterogeneity Within Dataset Folders

**What:** Mixed tolerance/word-length values within a single output folder (`simulation_data/Documentation/README.md`).

**Status as of 2026-06-10:** **Tracked.** Part of v1.5 dataset characterization (per-file parameter tracking).

**Severity:** MODERATE

---

## 6. MODERATE: Process & Workflow Issues

### P-1: Issues Consolidation Complete; v1.4 Shipped, v1.5 In Progress

**What (original):** Tracked Phase 9 (issues consolidation) status.

**Status as of 2026-06-10 (updated phase state):**
- v1.2 Phase 9 consolidated 7 issue reports into 3 thematic docs (`pinn_instruction/issues/01..03-*.md`) — Complete.
- **v1.4 (Phases 16–22) SHIPPED 2026-06-09** and merged to master: 8 phases, 26 plans, 65 tasks; 32/32 requirements and 25/25 STOP gaps closed (`.planning/MILESTONES.md`, `.planning/milestones/v1.4-MILESTONE-AUDIT.md`).
- **v1.5 (Phases 23–29) IN PROGRESS** on branch `milestone/v1.5`, currently Phase 23 (research-package assembly); resolution doc not yet produced (`.planning/REQUIREMENTS.md`).

**Severity:** INFO

### P-2: Modified But Uncommitted Documentation

**What (original):** `simulation_data/Documentation/README.md` was modified-but-unstaged in the working tree.

**Status as of 2026-06-10:** **Stale — original instance cleared.** `git status` on 2026-06-10 shows the working tree carries only `.planning/config.json` (modified) and `.planning/phases/23-research-package-assembly/23-PATTERNS.md` (untracked) — both active v1.5 planning artifacts, not the README. The README drift this finding flagged is no longer present.

**Severity:** MINOR → resolved (this instance).

### P-3: No Test/Build CI (AI-triage workflows now exist; local hooks enforced)

**What (original):** No GitHub Actions, no test automation, linting, or build verification.

**Status as of 2026-06-10:** **Partially changed — keep open for test/build CI.** GitHub Actions now exist but are **AI bot workflows only**: `.github/workflows/` contains `gemini-dispatch.yml`, `gemini-invoke.yml`, `gemini-review.yml`, `gemini-scheduled-triage.yml`, `gemini-triage.yml` (Gemini review/triage automation). There is still **no test-execution, lint, or build-verification CI**. Local commit governance is enforced via `.githooks/` (`commit-msg`, `pre-commit`, `pre-push`, `pre-rebase`, `post-checkout`, `post-commit`, `post-merge`) per the Git Commit Protocol. So: governance automation strong; quality/test CI absent.

**Severity:** MINOR

### P-4: Reference Code is Loaded with TODOs

**What:** `reference-code/` (~387MB) holds external NN reference implementations (GravNN, PINA, PyTorch source) with 30+ TODO/FIXME/HACK comments — not project-owned.

**Status as of 2026-06-10:** **Still open (low impact).** No planning artifact addresses extraction to a submodule.

**Severity:** MINOR

---

## 7. MINOR: Scaling & Portability

### S-1: Brutus Build Depends on System-Specific Libraries

**What:** Brutus needs GMP, MPFR, and the `mpreal` header at specific paths, unvendored and unversioned.

**Status as of 2026-06-10:** **Still open.** Unchanged.

**Severity:** MINOR

### S-2: Large Data Directories Excluded from Git But Not Documented

**What:** `.gitignore` excludes `simulation_data/Data/` (~6.2GB); raw ICs externalized via `IC_RAW_DIR`. A fresh clone has no simulation data.

**Status as of 2026-06-10:** **Still open.** Note the new-Mac migration runbook (`docs/runbooks/migration/exact-state-mac-migration.md`) now documents restoring local state excluding bulky payloads, partially mitigating onboarding confusion. A dedicated SETUP.md is still absent.

**Severity:** MINOR

### S-3: Single M2 Mac Development Constraint

**What:** All development on one Apple-Silicon Mac; Brutus makefile assumes ARM64 + Homebrew at `/opt/homebrew`; no x86_64 Linux testing.

**Status as of 2026-06-10:** **Still open.** Unchanged.

**Severity:** MINOR

---

## 8. Security

### No Secrets Detected

- No `.env` files; no API keys, tokens, or credentials in tracked code.
- `.gitignore` covers `.venv/`, `gha-creds-*.json`, and data directories.
- No cloud credentials or database passwords. Pipeline is offline.

**Status as of 2026-06-10:** Unchanged. (Note: `.github/workflows/gemini-*.yml` invoke an external AI service via GitHub Actions; verify any associated secrets are stored in GitHub Actions secrets, not committed — not audited here.)

### Unsafe Deserialization

- `pickle.dump/load` in `pinn/data-processing-pipeline-full.py` and `pinn/data-handling/core/parsing.py` (see M-7); `np.load(allow_pickle=True)` in `pinn/data-handling/core/parsing.py:411,468`. Low risk (self-produced data) but violates best practice. Unchanged.

### Path Traversal

- File paths built from numeric IDs and predefined directories; no user-supplied path components found. Low risk, not formally validated. Unchanged.

---

## 9. Pre-Implementation Audit: 11 Blockers Status (Refreshed 2026-06-10)

From the 2026-04-27 audit (`three_body_pinn_pre-implementation_audit_2026-04-27.md`). The table now distinguishes **Spec** status (resolved by v1.4 framework-spec construction) from **Code** status (v1.3-era live `pinn/` code, untouched — FUT-01). **Spec status changes below are grounded in `.planning/milestones/v1.4-REQUIREMENTS.md` and `.planning/milestones/v1.4-GAPS.md`; no physics was re-derived to assign them.**

| # | Blocker | Spec status (v1.4) | Code status (FUT-01) | Grounding |
|---|---------|--------------------|----------------------|-----------|
| B-01 | SIREN hidden-layer init formula | RESOLVED | already correct in code | ARCH-01; GAP-22-04 (`bf841f6`) |
| B-02 | Characteristic length D convention | ADJUDICATED & LOCKED | divergent | PHYS-01; EVID-05 |
| B-03 | Input vector 12/13/14D conflict | RESOLVED (14D=[τ,IC₁₃]) | divergent | IO-01/02/04 |
| B-04 | Orientation/trig encodings in CTL | RESOLVED (metadata-only) | divergent | IO-02; VER-06 (SI-PINN-001) |
| B-05 | COM frame violation (hierarchical) | RESOLVED | warn-only in code | FRAME-01/02/03, IO-03 |
| B-06 | Missing Stage 4→5 validation gate | NOT in v1.4 scope (Issue 02/03) | not built | tracked (C-4) |
| B-07 | Replay/lookahead batch split | NOT in v1.4 scope (Issue 03) | basic replay only | tracked |
| B-08 | Data-fidelity vs collocation conflated | NOT in v1.4 scope (Issue 03) | not built | tracked |
| B-09 | Softening mismatch ε strategy | ADJUDICATED & LOCKED | divergent | PHYS-03; EVID-05 |
| B-10 | Dynamic ω₀ scheduling no-op | RESOLVED (no scheduler unless reparameterized) | n/a | ARCH-01 |
| B-11 | Non-contiguous IDs not handled | under empirical verify (v1.5) | not built | DATA-01 (C-3) |

**Resolution status (2026-06-10):** **Spec side:** 7 of 11 resolved or adjudicated-and-locked by v1.4 (B-01, B-02, B-03, B-04, B-05, B-09, B-10); B-11 under empirical verification in v1.5; B-06/B-07/B-08 belong to the not-yet-opened Issue-03 (curriculum/training-loop) work. **Code side:** 0 of 11 aligned — the live `pinn/` implementation was deliberately untouched and is owned by FUT-01.

---

## 10. Dependency & Environment Risks

### No Pinned Dependencies

Inferred from `.venv/` (no manifest exists as of 2026-06-10): Python 3.12.2; PyTorch (`pinn/basic_architecture.py`); NumPy/SciPy/pandas across the pipeline. No version information recorded anywhere. See M-1.

### External Library Risk

- `mpreal` (MPFR C++ header), GMP, MPFR — system libraries, version-dependent, installed separately.
- Brutus uses C++11 — compiler-default-evolution compatibility risk.

Unchanged from prior audit.

---

## 11. Summary: What Blocks Implementation

### Resolved at the spec level by v1.4 (code alignment still owed to FUT-01)

- D convention (B-1/B-02 → PHYS-01), AD derivative contract (B-2/B-02 → PHYS-02), input vector 14D (B-5/B-03 → IO-01/02/04), orientation encoding (D-1/B-04 → IO-02), COM frame (C-2/B-05 → FRAME-01/02/03, IO-03), softening strategy (C-1/B-09 → PHYS-03), SIREN init doc (B-4/B-01 → ARCH-01), I_norm naming (D-2 → ARCH-04). All verified by the §10.1–§10.5 acceptance probes under VER-04/VER-05 (Phase 21).

### Still blocking (in priority order)

1. **Land the Issue-02 resolution doc + adjudicate (v1.5).** Data-pipeline/validation contracts (C-3, C-4, M-6, Q-1..Q-5) gate on it. Currently at Phase 23; no resolution doc yet.
2. **Open and resolve Issue-03 (curriculum/training-loop).** C-5 (stage transition criteria), C-6 (λ_E schedule), B-07, B-08 — no milestone exists.
3. **FUT-01 code rewrite/alignment.** Build the training loop (B-3) and align the live `pinn/` code to the v1.4 specs: D value, AD chain-rule factors, COM transform, Jacobi IC₁₃, softening ε, `TrajectoryIndex`/`TrajectoryValidator`, blacklist enforcement (M-6), pickle→HDF5 (M-7), modularization (M-2/M-9).
4. **FUT-02.** Recompute curriculum statistics/stage thresholds after preprocessing+physics contracts finalize.
5. **FUT-05.** Adjudicate the preserved author comments (`22-COMMENT-HANDOFF.md`).
6. **Infra debt (parallelizable).** `requirements.txt` (M-1), pipeline unit tests (M-8), test/build CI (P-3), Brutus makefile portability (M-4), data-acquisition docs (S-2).

---

*Concerns audit base: 2026-04-27. Refreshed: 2026-06-10 (status-only update against v1.4 completion records and v1.5 in-progress artifacts; no findings dropped; no physics re-adjudicated).*
*Next review: After the Issue-02 resolution doc lands and v1.5 adjudication phases (25–29) execute.*
