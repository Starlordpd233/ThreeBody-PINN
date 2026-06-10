# v1.4 Milestone Summary: Resolving 01 Architecture and Physics Foundations

**Milestone:** v1.4  
**Status:** Complete  
**Duration:** 2026-05-19 to 2026-06-09 (22 days)  
**Branch:** `milestone/v1.4` (cut from master 2026-05-19)  
**Commits:** 189 on milestone branch  

---

## 1. Overview

v1.4 resolved all adjudicable findings from Issue 01 (Architecture and Physics Foundations) in the CTL-PINN framework specifications. The milestone established an evidence-based adjudication workflow, locked 30 requirements across input/output contracts, frame/gauge preprocessing, physics/loss functions, architecture cleanup, and sampling coordinate allocation, and validated internal consistency via five disposable numerical probes.

**Core Achievement:** Three authoritative framework specifications (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`) now encode a unified, physically consistent PINN training contract. All v1.3-era code in `pinn/` is non-authoritative artifact; FUT-01 will rewrite the implementation from v1.4 specs.

**Governance Innovation:** Introduced the "resolution doc is candidate, not authority" policy. The agent transcribes positions from `ctl_pinn_resolution.md` only when they survive critical examination against both source documents and first-principles physics. Where sources are silent or ambiguous, the agent records gaps and halts until user instruction—never inventing.

---

## 2. Architecture and Deliverables

### 2.1 Framework Specifications (Authoritative)

| File | Lines | Scope |
|------|-------|-------|
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | 1458 | CTL methodology, input-vector formulation, curriculum staging, frame preprocessing, loss balancing |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | 1010 | Network architecture (SQR-SkipResNet-SIREN), AD contract, output head, §10 numerical acceptance checks |
| `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` | 281 | IC generation pipeline, Sobol coordinate allocation, hierarchical vs quasi-random sampling |

**Total:** 2749 lines across three files.

### 2.2 Key Contracts Locked

**Input/Output (Phase 17):**
- Canonical input: `14D = [tau, IC_13]` where `IC_13` is the Jacobi-state vector (ordered raw masses, Jacobi positions, Jacobi velocities, energy, per-slot normalization).
- Output: 9D position-only head with hard mass-weighted COM projection before any loss consumption. Velocities and accelerations derived via automatic differentiation, not predicted directly.
- Obsolete 11D/12D/ambiguous wording removed or labeled as source-issue metadata.

**Frame/Gauge (Phase 18):**
- Unified preprocessing contract: parse → mass-invariance check → COM recenter → zero-momentum boost → canonical ordering → rotation gauge → global scaling → assertions.
- Rotation gauge: dimensionless threshold `η_gauge = 1e-8`; sign-flip `e_y` to keep `λ_y ≥ 0` in fallback branch; ρ-degenerate trajectories rejected/quarantined.
- Frame invariants: preprocessed samples assert COM/total-momentum; model outputs assert mass-weighted COM projection using ordered raw mass metadata.
- 3D Cartesian output semantics preserved (rotation gauge fixes only initial orientation, not full trajectory).

**Physics/Loss (Phase 19):**
- Scaling: D-formula prose present; mass-fraction alternative documented as future-rewrite-only (AC-PHYS-01).
- AD contract: canonical leaf `u`, chain-rule factors, anti-pattern warning (AC-PHYS-02).
- Softening: Plummer in both sources; `ε_train=10⁻⁵`, `ε_inv=10⁻¹⁰`, `s_min` unsoftened (AC-PHYS-03).
- Energy loss: HNN-style framing removed; `L_E` reframed as soft conservation regularizer (AC-PHYS-04).
- Pseudo-ALM removed; P2-ablation appendix present (AC-PHYS-05).
- Constraint counting: `ctl_instruction.md` passage replaced (AC-PHYS-06).
- Causal physics loss: `L_{phys}^{causal}` with causal weights and `stopgrad`; normalized physics-time sampling `u ∈ [0, 1]`.

**Architecture Cleanup (Phase 20):**
- SIREN init: `first_omega_0=30`, `hidden_omega_0=1`, no in-run scheduler, hidden-layer bounds divided by `hidden_omega_0`.
- Energy/mass normalization: framed as realized dataset support only (M9/M10 evidence packets).
- FUT-01 handoff documents for M5 (I_3 ratio-form descriptor), M8 (elementwise_affine=False), B-01 (SIREN init already consistent).

**Sampling (Phase 20.5):**
- Sobol coordinate allocation locked to "Option A" (conditional `(δ_s, δ_v)` allocation matching existing dataset generation).
- No dataset regeneration required; spec matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py` behavior.
- `u_4` double-booking between scaling and velocity sampling resolved.

### 2.3 Evidence and Adjudication Infrastructure

**Phase 16 Deliverables:**
- Issue ledger: `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (21 findings: 19 in-scope, 2 deferred).
- Evidence packet template: `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`.
- Verdict enum: `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`.
- Status lifecycle: `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` (with regression revert policy).
- EVID-05 conflict-adjudication protocol for contested findings (B-02 D formula, B-04 input-vector orientation slots, B-09 softening strategy, M5 I_3 mapping).

**Traceability:** 30/30 v1.4 requirements mapped exactly once in `REQUIREMENTS.md` §Traceability (verified 2026-05-16).

### 2.4 Numerical Acceptance Suite (Phase 21)

**Five Disposable Probes** (all PASS, executed 2026-06-08):

| Check | Pass Criterion | Observed | Evidence |
|-------|----------------|----------|----------|
| 10.1 Scaling Consistency | `relative_error < 1e-10` | `max_relative_error = 2.22e-16` (3 non-unit scaling cases) | `probe_scaling.stdout.txt` |
| 10.2 COM Invariance | `abs(COM) < 1e-10` | `COM magnitude: 7.90e-17` | `probe_com.stdout.txt` |
| 10.3 Componentwise AD | `relative_error < 1e-6` | `relative_error: 0.00e+00` | `probe_ad.stdout.txt` |
| 10.4 Force-Energy Consistency | finite forward pass + finite loss scalars | all finite, no NaN/Inf | `probe_force_energy.stdout.txt` |
| 10.5 Loss Stability Dry Run | finite data/IC/physics/energy/angular losses | all finite | `probe_loss_stability.stdout.txt` |

**Probe Scripts:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/`  
**Raw Evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/` (SHA-256 hashes recorded)

### 2.5 Render Cleanup (Phase 22)

**Objective:** Normalize math rendering to LaTeX `$…$`/`$$…$$`, preserve all author comments, defer author-comment adjudication to FUT-05.

**Automated Gates:**
- G1 (selftest): PASS
- G2 (per-file 0-residual): PASS (0 DEFINITE, 0 REVIEW, 17 ADJUDICATED, 20 SUPPRESSED across three specs)
- G3 (content preservation): PASS (23 `pinn_architecture.md` hunks, 8 `ctl_instruction.md` hunks classified against allowed presentation-preserving categories; 26 PRE = 26 POST author comments, 0 lost)
- VER-05 (ledger): PASS (Phase 22 addendum records P22-R1/R2/R3 as VERIFIED, 0 OPEN STOP gaps)

**Manual Gate:**
- G4 (visual backstop): **APPROVED 2026-06-09** (checklist in `22-RENDER-REVIEW.md`)

**Detector Tool:** `tools/spec-render-check/detect.mjs` (Node.js, committed with adjudication allowlists)

**Handoff Artifacts:**
- `22-COMMENT-CENSUS-PRE.md`: 26 author comments before WS-A repair
- `22-COMMENT-CENSUS-POST.md`: 26 author comments after WS-A repair (0 lost, 0 gained)
- `22-COMMENT-DIFF.md`: per-comment classification (D-05 wrapper repairs recorded)
- `22-COMMENT-HANDOFF.md`: FUT-05 adjudication brief (inventory only, no adjudication performed)

---

## 3. Phases and Execution

| Phase | Focus | Plans | Status | Completed |
|-------|-------|-------|--------|-----------|
| 16 | Evidence framework, issue ledger, conflict adjudication | 3/3 | ✅ Complete | 2026-05-16 |
| 17 | Input and output contracts (incl. COM projection head) | 3/3 | ✅ Complete | 2026-05-20 |
| 18 | Frame and gauge contracts | 3/3 | ✅ Complete | 2026-05-21 |
| 19 | Physics and loss contracts (incl. M4 constraint counting) | 4/4 | ✅ Complete | 2026-05-30 |
| 20 | Architecture and normalization cleanup | 5/5 | ✅ Complete | 2026-06-05 |
| 20.5 | Sampling coordinate allocation (Sobol) | 1/1 | ✅ Complete | 2026-06-07 |
| 21 | Acceptance checks executed, SI-ledger reconciled, handoff | 2/2 | ✅ Complete | 2026-06-08 |
| 22 | Framework-spec render cleanup | 5/5 | ✅ Complete | 2026-06-09 |

**Total Plans:** 26 executed and complete

### Phase Dependencies

```
Phase 15.1 (v1.3 post-ship SCS gate correction)
    ↓
Phase 16 (Evidence framework)
    ↓
Phase 17 (Input/Output) → Phase 18 (Frame/Gauge) → Phase 19 (Physics/Loss)
                                                        ↓
                                                   Phase 20 (Architecture cleanup)
                                                        ↓
                                                   Phase 20.5 (Sampling allocation) [INSERTED]
                                                        ↓
                                                   Phase 21 (Acceptance checks + handoff)
                                                        ↓
                                                   Phase 22 (Render cleanup)
```

### Phase 20.5 Insertion

Phase 20.5 was inserted mid-milestone (2026-06-07) to address a Sobol coordinate-allocation ambiguity discovered during Phase 20 execution. The phase resolved the `u_4` double-booking between scaling and velocity sampling, locking "Option A" (conditional `(δ_s, δ_v)` allocation) as the canonical convention matching the existing dataset generator. No dataset regeneration was required.

---

## 4. Decisions and Governance

### 4.1 Standing Governance Rules

**Resolution Doc is Candidate, Not Authority**  
`ctl_pinn_resolution.md` is the most recent adjudication of Issue 01 and the default verdict source, but every claim must survive critical examination against `01-architecture-and-physics-foundations.md`, current framework specs, and first-principles physics before any spec edit. Live code in `pinn/` is NOT a grounding source (directive 2026-05-19).

**Agent Must Surface Gaps, Not Invent**  
Where source materials are silent or ambiguous, the agent records gaps in phase-local registers (`.planning/phases/NN-*/NN-GAPS.md`) and halts affected work until user instruction. The agent does NOT proceed past a non-grounded MUST-surface decision under any circumstance.

**Iterative Re-Verification Protocol**  
Architecture/physics fixes routinely need multiple attempts. The ledger pattern (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` with regression revert) prevents "fix applied" being mistaken for "issue closed." VER-04/VER-05 codify execute-then-re-verify using disposable validation probes.

**Empirical Decision Loop (EDL) Support**  
For source-silent decisions that are empirically consequential, the non-canonical EDL draft at `.planning/research/edl/README.md` provides research-support workflow. Phase gap registers remain authoritative blocking records. EDL briefs package context for user-led research; the agent does not perform that research or infer conclusions.

### 4.2 Key Decisions Made

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Resolution doc is NOT authoritative in v1.4 | The consolidated multi-AI resolution may contain errors never checked against current framework specs and first-principles physics. EVID-05 mandates critical examination of BOTH sources. | Active |
| Live code in `pinn/` is NOT a grounding source (2026-05-19) | v1.3-era code reflects a previous framework version; relying on it would silently bake in legacy conventions. FUT-01 rewrites code from v1.4 specs. | Active |
| Iterative re-verification protocol | Fixes need multiple attempts; ledger lifecycle prevents premature closure. | Active |
| `master_consolidation_report.md` demoted to supporting evidence | Resolution doc already consumed it; treating both as co-equal triples re-adjudication work. | Active |
| Agent must surface gaps, not invent | Cost of asking is small; cost of silent invention is irreparable spec drift across phases. | Active (v1.4 + standing for future adjudication milestones) |
| EDL support remains non-canonical (2026-05-24) | Some source-silent decisions are empirically consequential; EDL provides research-support workflow without authorizing conclusions. | Draft at `.planning/research/edl/README.md` |
| SCS/raw-drift gate correction (2026-05-15) | Keep SCS as base-10 log score, introduce raw drift `ε_H`, reject at `ε_H > 10⁻⁵` / `SCS > -5`. | Active |
| ε_H threshold (GAP-19-01, resolved 2026-05-24) | `ε_H = 1e-4 * S_H` with `S_H = median_train(K0 + Uabs0)`. Phase 21 validates activation behavior only. | Resolved via EDL |
| Rotation-gauge threshold (GAP-18-04, resolved 2026-05-21) | `η_gauge = 1e-8` as dimensionless relative threshold; `ε_ρ = ε_λ = η_gauge·D`, `ε_v = η_gauge·V`. | Resolved |
| Sobol allocation (Phase 20.5, 2026-06-07) | "Option A" conditional `(δ_s, δ_v)` allocation matching existing dataset generator. No regeneration. | Locked |
| Phase 22 author-comment adjudication deferred (GAP-22-01, 2026-06-08) | Phase 22 performs presentation-preserving render cleanup; author-comment substance adjudication deferred to FUT-05. | Deferred to FUT-05 |

### 4.3 Gap Resolution

**Total Gaps:** 23  
**Resolved:** 23 (100%)  
**Open:** 0  
**Deferred:** 0  

All gaps resolved via `RESOLVED-WITH-INSTRUCTION` (user provided explicit direction). No gaps remain open or deferred.

**Sample Resolutions:**
- GAP-17-01: AC-IO acceptance-check naming → reserve `AC-IO-01..04`, one per IO requirement
- GAP-18-04: Rotation-gauge epsilon thresholds → bind `η_gauge = 1e-8` dimensionless
- GAP-19-01: ε_H threshold → `ε_H = 1e-4 * S_H` (EDL-supported)
- GAP-20.5-01: Sobol allocation ambiguity → lock "Option A" matching data generator
- GAP-22-01: Author-comment adjudication scope → defer to FUT-05, Phase 22 does presentation only

Full gap register: `.planning/milestones/v1.4-GAPS.md`

---

## 5. Requirements and Verification

### 5.1 Requirements Fulfilled

**Total v1.4 Requirements:** 30 (all fulfilled)

**By Category:**

| Category | Count | Requirements |
|----------|-------|--------------|
| Evidence and Resolution Validation | 5 | EVID-01, EVID-02, EVID-03, EVID-04, EVID-05 |
| Input and Output Contracts | 4 | IO-01, IO-02, IO-03, IO-04 |
| Frame and Gauge Contracts | 4 | FRAME-01, FRAME-02, FRAME-03, FRAME-04 |
| Physics and Loss Contracts | 6 | PHYS-01, PHYS-02, PHYS-03, PHYS-04, PHYS-05, PHYS-06 |
| Architecture and Normalization Cleanup | 5 | ARCH-01, ARCH-02, ARCH-03, ARCH-04, ARCH-05 |
| Sampling Coordinate Allocation | 2 | SAMP-01, SAMP-02 |
| Verification and Handoff | 4 | VER-01, VER-03, VER-04, VER-06 |

**Cross-Project Documentation Requirement:**
- REQ-DOC-01: Markdown framework specs are authoritative during active project work; LaTeX sources are publication/archive derivatives. No milestone before final publication/archive syncs `.tex` to markdown.

### 5.2 Verification Protocol

**Applies to Every Phase:** adjudicate → fix → verify → re-verify after every batch → close only when the acceptance check passes.

**Per-Phase Verification Artifacts:**
- `NN-VERIFICATION.md`: Verdict (passed/failed), requirement coverage table, automated checks, notes, human verification required
- `NN-VALIDATION.md`: Test infrastructure, sampling rate, per-task verification map, validation sign-off
- `NN-UAT.md`: User acceptance tests (where applicable)

**Phase 21 Acceptance Suite:**
- Defined in `pinn_architecture.md` §10 (five subsections)
- Executed via disposable probes in `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/`
- Raw stdout evidence with SHA-256 hashes in `evidence/`
- All five probes PASS

### 5.3 Issue Ledger Reconciliation

**Total Findings:** 21  
**In-Scope:** 19  
**Deferred:** 2 (M6, M7 — "not adjudicable from supplied files")

**Terminal State (Phase 21):**
- 19 in-scope findings: all `VERIFIED` or `DEFERRED` with written blocker
- M6/M7: explicitly deferred (resolution doc declares "not adjudicable from supplied files")
- SI-ledger entries reconciled: every v1.4-resolved finding retires its corresponding `SI-*` with back-reference; entries outside Issue 01 preserved untouched

**Ledger Location:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`

---

## 6. Tech Debt and Deferrals

### 6.1 Explicit Deferrals

| Item | Reason | Revisit When |
|------|--------|--------------|
| M6, M7 from resolution doc | "Not adjudicable from supplied files" | Source material becomes available |
| Author-comment substance adjudication (Phase 22) | Phase 22 scoped to presentation-preserving render cleanup only | FUT-05 dedicated adjudication phase |
| LaTeX sync (REQ-DOC-01) | Markdown is authoritative during active work; LaTeX is publication derivative | Final publication/archive milestone |
| Code implementation alignment (FUT-01) | v1.4 constructs framework specs; code rewrite is separate milestone | FUT-01 milestone (from v1.4 specs) |

### 6.2 Known Divergences (FUT-01 Handoff)

**Forward-Pointing Handoff Documents:**
- `17-CODE-DIVERGENCE.md`: Input/output contract divergences (obsolete 11D/12D wording, direct velocity prediction)
- `18-CODE-DIVERGENCE.md`: Frame/gauge divergences (COM projection, rotation gauge)
- `19-CODE-DIVERGENCE.md`: Physics/loss divergences (causal loss, energy denominator floor)
- `20-CODE-DIVERGENCE.md`: Architecture divergences (M5 I_3 ratio-form, M8 elementwise_affine, B-01 SIREN init)
- `21-CODE-DIVERGENCE.md`: Acceptance-check divergences (Section 10 probes)

**Policy:** Live code in `pinn/` is NOT a grounding source during v1.4. Divergence documents record where v1.3-era code differs from v1.4 specs; FUT-01 rewrites code to match v1.4 specs.

### 6.3 Operational Notes

**Working Branch:** `milestone/v1.4` (cut from master 2026-05-19). Do NOT commit v1.4 spec edits to master. Before merge: `git merge --no-ff milestone/v1.4` to master.

**Phase 22 Completion Status:** Automated gates G1/G2/G3/VER-05 passed, and the user approved the manual G4 visual backstop on 2026-06-09. Checklist and approval record: `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-RENDER-REVIEW.md`.

---

## 7. Getting Started

### 7.1 For New Team Members

**Start Here:**
1. Read this summary (you are here)
2. Read `.planning/PROJECT.md` for project overview and current milestone context
3. Read `.planning/ROADMAP.md` for phase-by-phase details and verification protocols
4. Read `.planning/REQUIREMENTS.md` for full requirement traceability

**Framework Specs (Authoritative):**
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — CTL methodology, curriculum, frame preprocessing
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — Network architecture, AD contract, §10 acceptance checks
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — IC generation, Sobol allocation

**Evidence and Adjudication:**
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — Issue ledger with all 21 findings and verdicts
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` — Evidence packet template
- `.planning/milestones/v1.4-GAPS.md` — All 25 gaps with resolutions

**Acceptance Probes:**
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/` — Five disposable validation probes
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-PROBE-RESULTS.md` — Probe execution summary
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/` — Raw stdout with SHA-256 hashes

**Render Cleanup:**
- `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-RENDER-REVIEW.md` — Gate status and G4 visual backstop checklist
- `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md` — FUT-05 author-comment adjudication brief
- `tools/spec-render-check/detect.mjs` — Committed render detector (Node.js)

### 7.2 For Future Milestones

**FUT-01: Code Rewrite**  
Rewrite `pinn/` implementation from v1.4 framework specs. Start from `NN-CODE-DIVERGENCE.md` handoff documents to identify where v1.3 code diverges from v1.4 specs.

**FUT-05: Author-Comment Adjudication**  
Adjudicate author comments preserved in Phase 22. Start from `22-COMMENT-HANDOFF.md` for full inventory and context.

**Phase 22 G4 Visual Backstop**  
Approved by the user on 2026-06-09 after completing the manual visual review checklist in `22-RENDER-REVIEW.md`.

**Merge to Master**  
Completed on 2026-06-09 via merge commit `376adcc`.

### 7.3 Key Governance Rules

1. **Resolution doc is candidate, not authority.** Transcribe positions only when they survive critical examination.
2. **Agent must surface gaps, not invent.** Halt work where sources are silent; record gaps; wait for user instruction.
3. **Live code in `pinn/` is NOT a grounding source.** v1.3 code is artifact; FUT-01 rewrites from v1.4 specs.
4. **Iterative re-verification.** Fixes need multiple attempts; ledger lifecycle prevents premature closure.
5. **Commit at logical task boundaries.** Atomic commits for spec edits; use `scripts/agent-commit`; include `Agent-Assisted-By:` trailer.

---

## Appendix A: File Inventory

**Planning Artifacts:**
- `.planning/ROADMAP.md` — Phase-by-phase details and verification protocols
- `.planning/REQUIREMENTS.md` — 30 v1.4 requirements with traceability
- `.planning/PROJECT.md` — Project overview and current milestone context
- `.planning/STATE.md` — Current state and progress metrics
- `.planning/milestones/v1.4-GAPS.md` — All 25 gaps with resolutions

**Phase Directories:**
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/` — Evidence framework
- `.planning/milestones/v1.4-phases/17-input-and-output-contracts/` — Input/output contracts
- `.planning/milestones/v1.4-phases/18-frame-and-gauge-contracts/` — Frame/gauge contracts
- `.planning/milestones/v1.4-phases/19-physics-and-loss-contracts/` — Physics/loss contracts
- `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/` — Architecture cleanup
- `.planning/milestones/v1.4-phases/20.5-sampling-coordinate-allocation/` — Sobol allocation
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/` — Acceptance probes and handoff
- `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/` — Render cleanup

**Framework Specs:**
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (1458 lines)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (1010 lines)
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` (281 lines)

**Source Documents (Grounding Sources):**
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — Resolution doc (candidate verdict source)
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — Thematic issue doc

**Tools:**
- `tools/spec-render-check/detect.mjs` — Phase 22 render detector

---

## Appendix B: Metrics

| Metric | Value |
|--------|-------|
| Milestone duration | 22 days (2026-05-19 to 2026-06-09) |
| Commits on milestone branch | 189 |
| Phases executed | 8 (16, 17, 18, 19, 20, 20.5, 21, 22) |
| Plans executed | 26/26 complete |
| Requirements fulfilled | 30/30 |
| Gaps surfaced and resolved | 25/25 |
| Issue ledger findings | 21 total (19 in-scope, 2 deferred) |
| Framework spec lines | 2749 (across 3 files) |
| Acceptance probes | 5/5 PASS |
| Phase 22 gates | G1/G2/G3/VER-05 PASS; G4 approved |

---

**Generated:** 2026-06-09  
**Milestone Status:** Complete  
**Next Action:** Begin FUT-01 code rewrite
