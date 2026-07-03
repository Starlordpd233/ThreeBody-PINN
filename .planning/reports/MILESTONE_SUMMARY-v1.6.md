# Milestone v1.6 — Project Summary

**Generated:** 2026-07-02
**Purpose:** Team onboarding and project review
**Milestone:** v1.6 Resolving 03 Curriculum and Training Loop
**Branch:** `milestone/v1.6` (cut from v1.5 deliverable tip `88aa1e4f`)
**Audit Verdict:** *Pending — `/gsd-audit-milestone` running in parallel watchdog (Agent A).* Pre-audit confidence: PASS — Phase 36 closure gate satisfied (26/26 acceptance probes, 18/18 ledger VERIFIED, 32/32 traceability, 0 STOP gaps, 0 open gaps). 11/11 independent UAT checks pass per `36-UAT.md`.

---

## 1. Project Overview

### What This Is

A three-body physics simulation + Physics-Informed Neural Network (PINN) training stack. The Brutus C++ integrator produces high-precision ground-truth trajectories; the Python pipeline generates initial conditions, runs hierarchical Brutus simulations, and computes per-IC metrics; the CTL-PINN trains on those trajectories under a curriculum that progressively exposes it to harder dynamics. The framework specs (`pinn_instruction/markdown_conversion/framework-specs/`) are the authoritative design documents; `pinn/` is v1.3-era live code carried forward, scheduled for a spec-driven rebuild in the trainex track.

### v1.6 Goal

Critically examine each finding in `pinn_instruction/issues/03-curriculum-and-training-loop.md` — treating the issue doc as non-authoritative — against the user-produced external resolution doc, the locked v1.4 (doc-01) and v1.5 (doc-02) conventions, the framework specs, and first principles; adjudicate the curriculum-staging and training-loop findings; apply evidence-backed edits limited to `ctl_instruction.md` and `pinn_architecture.md`; and verify each fix with disposable acceptance probes before closing.

**Coverage:** 32/32 v1.6 requirements mapped (Phases 30–36; the readiness-verification Phase 31 is operational with 0 requirement IDs).
**Granularity:** standard (Phase 31 deliberately given a whole number, not a `.5` decimal, because it was planned at milestone initialization, not an urgent insertion — v1.5's Phase 24.5 analog).

### What v1.6 Delivered

- **Curriculum-stage spec contracts** (CURR-01..05) in `ctl_instruction.md`: data-driven adaptive stage assignment methodology, `tau_L`/`L_max` computation with `D ≈ 4.6416` (the v1.5-locked raw-mass convention), dual-path stage-transition state machine, Stage 0–6 inventory + gating, and the unsoftened `s_min` stage-gate frame.
- **Training-loop spec contracts** (LOOP-01..08): replay/lookahead batch construction (`B_replay = 240` + `B_lookahead = 16`), two-independent-point-set separation (data-fidelity 8192 / collocation 4096), 50/50 mixed time sampling, merged gradient clipping (`C_stage · median(grad_norm_history)`, `C_table = [8.5, 8.5, 5, 5, 3, 3, 3]`), `dt_out`-aware collocation scaling (forward-direction only), ALM update with `μ_p` clamp `[1e-4, 100]`, and the training-side use of IPR/PSC/SASD that v1.5 left provisional.
- **Loss-function spec contracts** (LOSS-01..04): loss-component scaling in dimensionless coordinates, capped-hybrid `λ_E(k) = min(10^(k-3), cap[k])` schedule (`cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}`), Huber-δ calibration, and the causal-training-mode contract per D-04 Option A.
- **Adjudication machinery** (EVID-11..15): evidence-packet template, fixed verdict enum, false-positive notes, before/after evidence, and root-cause adjudication of the five headline conflicts (D-04, D-05, D-06, M14, `D = 6.694` vs `D ≈ 4.6416`).
- **Acceptance suite** (VER-13..18): 26 numerically-defined acceptance probes covering every v1.6 contract, each producing recorded pass/fail evidence. Re-run 2026-07-02T00:39:33Z shows **26/26 PASS** plus a 1/1 companion traceability probe.
- **Issue ledger closure** (VER-16): 18/18 in-scope findings reach terminal `VERIFIED` state under freshness-checked write; previously VERIFIED findings re-verified after each edit batch; nothing closes via advisory; cycle-4 HIGH-B partition discipline enforces "every ledger finding classified exactly once across Fixed / Intentionally Unchanged / Deferred".
- **SI metadata reconciliation** (VER-18): all four `SI-*` entries (SI-CTL-001, SI-PINN-002, SI-PINN-003, SI-DQA-003) reviewed for issue-03 relevance; each retired-with-back-reference or preserved-with-written-reason-and-owner; none assumed resolved or assumed irrelevant.

### Where v1.6 Stops

v1.6 is **specwork-only** (user-confirmed 2026-06-17). The verbatim audit "Section 6 — Unified Batch Construction" pseudocode is transcribed as a **normative spec contract**, not executed. Training-loop implementation, the adaptive-stage-assignment EDA run over the dataset, and the Stage-0 pilot threshold calibration are FUT — they route to the **trainex track** (`.worktrees/trainex` on branch `track/trainex`), not into v1.6 specwork. The trainex track owns:

- **FUT-01** (rebuild from specs): componentwise AD, gradient-clipping mechanism, batch constructor / DataLoader, ALM update + μ_p clamp activation, causal-mode mechanics.
- **FUT-04** (resume training-loop impl + calibration): adaptive-stage EDA, Stage-0 pilot calibration, Huber-δ calibration, IPR/PSC/SASD numeric confirmation, dt_out collocation scaling, epsilon train-vs-validate sensitivity.

`pinn/` live code was **not** edited during v1.6 (SCOPE-10); the protected-path guard (`git diff` over `pinn/` and frozen specs is empty) confirms it. `pinn/STATUS.md` (FUT-01 target) is the only place `pinn/` references are permitted post-v1.6, and only as forward-pointing hand-off.

---

## 2. Architecture & Technical Decisions

### Governance Decisions (user directives that frame v1.6)

| Decision | Description | Why |
|----------|-------------|-----|
| **Issue doc is non-authoritative** | `pinn_instruction/issues/03-curriculum-and-training-loop.md` consolidates the 2026-04-27 audit (Sections 6–7), the Causal Training Mismatch blueprint, the stage-assignment methodology, and `next steps.txt`. It carries known tensions (`D = 6.694` against v1.5-locked raw-mass `D ≈ 4.6416`; "Canonical" citations of `pinn/` live code). | Adjudication milestones treat the issue doc as a finding-list, never as authority. |
| **Resolution doc is the candidate verdict source** | The user-produced consolidated doc landed at `framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` (commit `49fb7958`). Same standing `ctl_pinn_resolution.md` had in v1.4 and `02-resolution-doc.md` had in v1.5: transcribed unless evidence shows a position fails, never authoritative. | Phases 32–36 gate on Phase 31 (READINESS VERIFICATION) PASS; phase 31 gates on the consolidated doc landing. |
| **SCOPE-12 hard-constraint grounding** | v1.4 (14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`, raw-mass `D ≈ 4.6416`) + v1.5 PIPE-01..10 / VAL-01..04 data-side contracts are hard constraints. `pinn/` live code is NOT grounding (directive 2026-05-19, persists). | v1.6 reconciles issue-03 against these; it does not re-open them absent new first-principles evidence surfaced through EVID-15. |
| **SCOPE-13 spec-edit perimeter** | Edits land in `ctl_instruction.md` and `pinn_architecture.md` ONLY. Curriculum staging, batch construction, stage transitions, loss scaling, and `tau_L`/`L_max` → `ctl_instruction.md`; gradient clipping and training-strategy items → `pinn_architecture.md`. `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md`, `review-of-framework.md`, `stage-strat-revision.md` read-only (SCOPE-09). | Specwork is bounded by file; frozen files cannot be silently re-opened. |
| **SCOPE-14/15 implementation is FUT** | Training-loop code, the adaptive-stage-assignment EDA run, and the Stage-0 pilot calibration are FUT-01/FUT-04 (trainex track). v1.6 transcribes verbatim audit pseudocode as normative spec contracts; it may run only disposable formula-sanity probes (e.g., `tau_L`/`L_max`/`λ_E`) to test contracts before locking. | Specwork-only milestone; "reality pipeline" lives in a separate track. |
| **STOP protocol in full** | Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in phase-local `NN-GAPS.md` registers and the milestone index `.planning/milestones/v1.6-GAPS.md`. Nothing is invented where sources are silent. | v1.6 is a "similar adjudication milestone" per AGENTS.md governance; user does not trust silent invention. |
| **SI preservation discipline** | Curriculum/training-loop `SI-*` entries reviewed for issue-03 relevance: each retired-with-back-reference or preserved-with-written-reason-and-owner; none assumed resolved or assumed irrelevant. | Avoids silent retirement (preserves the v1.4 / v1.5 preserve-with-reason precedent set by D-08 SI-PINN-002). |

### Process / Tooling Decisions

| Decision | Description | Why | Phase |
|----------|-------------|-----|-------|
| **Per-phase preflight tag** | Tag `v1.6-pre-phase-NN` from branch HEAD before each phase begins. | Recovery point for any destructive operation; audit-trail of phase boundaries (D-09 GUARD discipline). | 30, 31, 32, 33, 34, 35, 36 |
| **`scripts/agent-commit` wrapper** | All atomic commits go through the wrapper; agents set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; explicit-path staging only. | Concurrent-sessions safety; ownership prevents agent races. | all |
| **Two-stage external research pipeline** | Stage 1: generic prompt + self-contained research package → 8 independent research agents. Stage 2: 8 reports (anonymized R1–R8) + package → 1 consolidation agent. | Reduces anchoring; reproducibility; byte-verifiable; explicit. | 30 |
| **Phase 31 readiness gate (whole-number, not `.5`)** | Lightweight readiness verification that the consolidated resolution doc is fit for adjudication before Phases 32–36 commit to it. | v1.4 retrospective insight: a missing gate let consolidation defects propagate into 5 phases of adjudication work. | 31 |
| **Evidence-packet template with fixed verdict enum** | `evidence/{id}.md` with `## Verdict` section; verdict enum `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker`. | Audit trail for adjudication; later phases can re-derive the verdict. Thin-pointer packets allowed for findings whose verdict predates the packet system. | 32 |
| **Ledger as canonical verification artifact** | The 18-row `32-ISSUE-LEDGER.md` (PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED) is the verification record. Per-phase VERIFICATION.md is the per-phase verification surface; the ledger is the cross-phase one. | State machine preserved verbatim; lets Phase 32 own records while 33-35 own the fixes; Phase 36 owns closure. | 32, 33, 34, 35, 36 |
| **Freshness-checked ledger promotion** | Each promotion PENDING → VERIFIED includes a freshness hash (post-write SHA-256) of the ledger file. `36-LEDGER-CLOSURE.md` recorded `184cb56f…` for the final state. | Detects concurrent writes; prevents stale-cache demotions; audit trail for verifier independence. | 36 |
| **Protected-path guard** | A disposable probe asserts `git diff` over `pinn/` and frozen specs is empty. | SCOPE-10 enforcement; prevents accidental `pinn/` edits during spec-only phases. | 36 |
| **Cycle-4 HIGH-B partition discipline** | Each ledger finding classified exactly once across Fixed / Intentionally Unchanged / Deferred tables. Prevents double-counting. | Avoids reconciliation ambiguity; partition is auditable. | 36 |
| **D-36-17 terminal-anchor definition extension** | PKG-05..08 flip Complete on the Phase 30 completion record (pre-ledger family); LOOP-07/08 flip Complete on `34-VERIFICATION.md` SATISFIED anchor (provisional carry-forward). D-36-17 amended to "terminal ledger row OR terminal phase-VERIFICATION record." | Reconciled R6 traceability under the rule "each flipped flag must match a terminal anchor"; pre-ledger families get phase-completion anchors. | 36 |
| **Owner-driven gap resolutions** | All 10 milestone gaps are RESOLVED-WITH-INSTRUCTION (user picks A/B/C via AskUserQuestion at the relevant SPEC/UAT gate). | STOP protocol requires the user, not the agent, to settle source-silent decisions. | 32, 33, 34, 35, 36 |

### Adjudication Decisions (resolved gaps)

| Gap | Decision | Why | Phase |
|-----|----------|-----|-------|
| **GAP-32-01** (D-04) | Owner ratified **Option A** at the Phase 35 SPEC gate: retain current per-time causal weighting baseline (`w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `w_1 = 1`, `η_c = 1`); preserve dense-residual pseudo-ALM rejection; defer numeric causal-exponent clip bound to FUT. | v1.3 live code already implements Option A correctly per GAP-32-01 consumption; future clip-bound work lives in trainex. | 32 → 35 |
| **GAP-32-02** (D-05) | Owner ratified **Option A**: unsoftened geometric `s_min` stage gate + matched-Plummer (`ε_train = 1e-5`) softening in training residual/energy only; issue-doc `max(s_min, ε)` phrasing rejected per PHYS-03. | Resolves SCS-gate / Plummer physics consistency; loss-side softening owned by Phase 35. | 32 → 33 |
| **GAP-32-03** (D-06) | Owner ratified dual-context (**Option A; = issue-doc Option B**): offline invariants/validation keep `ε_inv = 1e-10` (consistent with v1.5-locked IPR GAP-28-02); training keeps `ε_train = 1e-5`; Option C rejected. | Preserves v1.5 SCOPE-12 hard constraint; close-encounter sensitivity check logged as FUT-04. | 32 → 33 |
| **GAP-33-01** | Owner ratified packet-first / defer-floor (§1.15; ADAPT-04/07): `CURR-01` specifies the offline-EDA methodology + stable `record_key` labels within the existing multi-fidelity topology; the 5% / >10% / adaptive population floor is owner-pending the FUT admitted-set EDA (SCOPE-15). | Roadmap `>10%` phrasing superseded; not locked. | 33 |
| **GAP-33-02** | Owner ratified keep-Rosenstein-baseline / defer (§1.17; TAUL-01/03): `CURR-02` transcribes the grounded `L_max` characteristic-scale formula + `D ≈ 4.6416` + M7; the `tau_L` estimator stays Rosenstein-baseline-revisable with method/units/thresholds owner-pending. | Roadmap shadow + PCA/Rosenstein phrasing not normatively adopted. | 33 |
| **GAP-33-03** | Owner ratified raw-only / defer-clip (§1.6; M6-02/03, DGR-07): `CURR-04` stores raw `L_norm` metadata + the mandatory degenerate-`L_max` guard; no global clamp authorized (M6-01 rejected); the `np.clip` stage-gate is owner-pending admitted-set evidence. | Roadmap `np.clip` gate phrasing superseded. | 33 |
| **GAP-34-01** | Owner ratified **Option A** at Phase 34 UAT: final stage trains replay-only; undersized look-ahead (<16) padded by sampling with replacement (batch size fixed at 240+16); replay sampled without replacement across the epoch. | Edges covered; values inherit the LOOP-01 `provisional` tag. | 34 |
| **GAP-35-01** | Owner adopted a **refined de-duplication**: `ctl_instruction.md` LOSS-04 callout now points to `pinn_architecture.md` **Physics Residual Term** as the single canonical home and cites only `w_1 = 1` / `η_c = 1`; the `w_n = exp(...)` body is no longer restated in the assembly file. | Phase-35-authored content; aligned to LOSS-03 pointer pattern; Option B's locked-content cost premise was obsolete. | 35 |
| **GAP-36-01** | Owner selected **Option A**: flip PKG-05..08 → `Complete`, anchored on the Phase 30 completion record (5/5, 2026-06-18); the terminal-anchor definition extends to phase-completion records for pre-ledger families. | Pre-ledger families (PKG was complete before Phase 32 ledger existed) need a non-ledger anchor. | 36 |
| **GAP-36-02** | Owner selected **Option A**: flip LOOP-07/08 → `Complete`, anchored on `34-VERIFICATION.md` SATISFIED/VERIFIED (`:118-119`); **D-36-17 amended** to "terminal ledger row OR terminal phase-VERIFICATION record." | LOOP-07/08 are provisional carry-forwards (no dedicated ledger row); VERIFICATION anchor is the right closure surface. | 36 |

---

## 3. Phases Delivered

| # | Phase | Status | Plans | One-Liner |
|---|-------|--------|-------|-----------|
| **30** | Research Package Assembly | complete (5/5) | 5 | PKG-08 reports characterized read-only; PKG-07 claims register seeded; 5 consolidation artifacts assembled (FRAMEWORK-SPECS-BUNDLE 3200 lines, byte-pinned); 5/5 plans 2026-06-18. |
| **31** | Resolution Doc Readiness Verification | complete (1/1) | 1 | READY-WITH-CAVEATS gate; 18/18 finding coverage; 0 contradictions; 0 HC violations; resolution doc 820 lines / 157,460 bytes; Phases 32–36 unblocked 2026-06-20. |
| **32** | Evidence Framework, Issue Ledger & Conflict Adjudication | complete (4/4) | 4 | Evidence-packet template + verdict enum + 32-ISSUE-LEDGER.md operating protocol; 5 EVID-15 headline conflicts adjudicated at root cause (D-04, D-05, D-06, M14, D-CONFLICT); cycle-4 HIGH-B partition discipline; D-09/D-10 GUARD discipline honored. |
| **33** | Curriculum-Stage Contracts | complete (4/4) | 4 | CURR-01..05 transcribed into `ctl_instruction.md`: adaptive stage assignment methodology, `tau_L`/`L_max` (`D ≈ 4.6416`), dual-path state machine (ADVANCE/RECOVER/HALT/REVIEW), Stage 0–6 inventory + degenerate-`L_max` guard, unsoftened `s_min` stage gate (D-05 Option A). |
| **34** | Training-Loop & Batch-Construction Contracts | complete (5/5) | 5 | LOOP-01..08 transcribed: replay/lookahead (`240+16`), two-independent-point-set (8192/4096), mixed time sampling (50/50), merged gradient clipping (`C_table [8.5,8.5,5,5,3,3,3]`), ALM μ_p clamp `[1e-4,100]`, `dt_out` collocation scaling (forward-only), IPR/PSC/SASD training-side use. |
| **35** | Loss & Energy-Weight Contracts | complete (4/4) | 4 | LOSS-01..04 transcribed: dimensionless-coordinate loss scaling + AD chain-rule factors, capped-hybrid `λ_E` schedule, Huber-δ `0.01–0.1` starting range, D-04 Option A causal-mode contract. GAP-35-01 refined de-duplication applied. |
| **36** | Acceptance Checks, Re-verification & Handoff | complete (5/5) | 5 | 26/26 acceptance probes PASS + 1/1 companion traceability probe PASS; ledger terminal 18/18 VERIFIED; D-05/D-06 promoted under freshness-checked write (post-write SHA-256 `184cb56f…`); SI table reconciled (4/4 retired-with-back-ref or preserve-with-reason); 36-HANDOFF.md + 36-CODE-DIVERGENCE.md; 32/32 traceability per VER-14. |

**Total:** 7 phases, 28 plans, 32/32 requirements satisfied, 0 open gaps, 0 STOP gaps, 18/18 ledger VERIFIED, 26/26 acceptance probes PASS, 11/11 UAT independent checks pass.

---

## 4. Requirements Coverage

All 32 v1.6 requirements are `Complete` per the Phase 36 R6 reconciliation (each flip citing its specific terminal anchor — see `.planning/REQUIREMENTS.md` traceability table):

| Coverage Block | Count | Phase | Status |
|----------------|-------|-------|--------|
| **PKG** (Research Package) | 4 (PKG-05..08) | 30 | ✅ Complete (anchored on Phase 30 completion record 5/5, 2026-06-18) |
| **EVID** (Adjudication) | 5 (EVID-11..15) | 32 | ✅ Complete |
| **CURR** (Curriculum) | 5 (CURR-01..05) | 33 | ✅ Complete |
| **LOOP** (Training-Loop) | 8 (LOOP-01..08) | 34 | ✅ Complete (LOOP-07/08 anchored on `34-VERIFICATION.md` SATISFIED/VERIFIED; provisional carry-forward) |
| **LOSS** (Loss) | 4 (LOSS-01..04) | 35 | ✅ Complete |
| **VER** (Verification) | 6 (VER-13..18) | 36 | ✅ Complete |
| **Total** | **32/32** | 30–36 | ✅ Complete |

**Audit verdict:** *Pending `/gsd-audit-milestone` (Agent A).* Pre-audit confidence PASS — all VER-13..18 must-haves satisfied; protected-path guard PASS; no advisory closures; cycle-4 HIGH-B partition holds; UAT 11/11 independent.

**Cross-project requirements:** REQ-DOC-01 (Markdown specs authoritative during active work; LaTeX sources publication/archive derivatives) — carried from v1.4, still in force.

**Future Requirements (not in v1.6 total):** FUT-01 (rebuild `pinn/` from settled framework specs), FUT-02 (recompute curriculum statistics after contract finalization), FUT-03 (package validation probes), FUT-04 (resume training-loop implementation), FUT-05 (adjudicate v1.4 Phase 22 author comments).

---

## 5. Key Decisions Log

The full gap index is in `.planning/milestones/v1.6-GAPS.md` (10 gaps, 0 open, 10 RESOLVED-WITH-INSTRUCTION). The most consequential decisions:

| ID | Phase | Decision | Impact |
|----|-------|----------|--------|
| **D-04** (GAP-32-01) | 32 → 35 | Causal training mode: Option A — per-time causal weighting (`w_n = exp(-η_c · Σ stopgrad)`, `w_1 = 1`, `η_c = 1`); dense-residual pseudo-ALM rejected; scalar ALM deferred P2; numeric causal-exponent clip bound deferred to FUT. | LOSS-04 contract; FUT-01 causal-mode mechanics. |
| **D-05** (GAP-32-02) | 32 → 33 | s_min frame: unsoftened geometric `s_min` stage gate + matched-Plummer (`ε_train = 1e-5`) softening in training residual/energy only. Issue-doc `max(s_min, ε)` phrasing rejected per PHYS-03. | CURR-05 contract; preserves SCS-gate / Plummer physics consistency. |
| **D-06** (GAP-32-03) | 32 → 33 | Epsilon strategy: dual-context (`ε_inv = 1e-10` offline invariants / `ε_train = 1e-5` training). Option C (`1e-10` everywhere) rejected. Close-encounter mismatch sensitivity check routed to FUT-04. | Spec convention for training residual/energy; preserves v1.5-locked IPR hard constraint. |
| **D-CONFLICT** (EVID-15) | 32 | `D = 6.694` vs v1.5-locked raw-mass `D ≈ 4.6416`: reconciled with v1.5 Phase 25 EVID-10 as the hard constraint. Issue-doc `D = 6.694` figure rejected. | Locks the CURR-02 `D` value; resolves cross-milestone conflict. |
| **M14** (EVID-15) | 32 → 34 | Gradient clipping divergence: `clip_value = C_stage · median(grad_norm_history)` with per-stage `C_table` (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0) and rolling window. | LOOP-04 contract; M14 sub-items (bootstrap floor, exact early-stage C, lower floor, history reset) routed to FUT-01. |
| **GAP-35-01** | 35 | Causal-weight formula single-home discipline: `ctl_instruction.md` LOSS-04 callout points to `pinn_architecture.md` Physics Residual Term; `w_n = exp(...)` body not restated. | Aligned to LOSS-03 pointer pattern; prevents drift kernel in two files. |
| **GAP-34-01** | 34 | Batch edge cases: final stage trains replay-only; undersized look-ahead (<16) padded by replacement sampling; replay sampled without replacement across epoch. | LOOP-01 `provisional` tag inherited; clears Phase 34 §8 closure gate. |
| **GAP-33-01/02/03** | 33 | Owner-pending population floor / `tau_L` estimator / `L_norm` clip; packet-first / defer-floor / raw-only. | CURR-01/02/04 contracts carry forward as methodology + open evidence needs. |
| **GAP-36-01/02** | 36 | R6 reconciliation terminal-anchor extension: PKG flips on Phase 30 completion record; LOOP-07/08 flip on `34-VERIFICATION.md` SATISFIED anchor. D-36-17 amended. | 32/32 traceability closed; pre-ledger families + provisional carry-forwards have correct anchors. |
| **VER-18 SI table** | 36 | SI-CTL-001 / SI-PINN-002 / SI-PINN-003 / SI-DQA-003 each retired-with-back-reference or preserve-with-written-reason-and-owner. | VER-18 must-have satisfied; no `SI-*` assumed resolved or irrelevant. |

---

## 6. Tech Debt & Deferred Items

### Deferred to FUT-01 (rebuild from specs)

Per `36-CODE-DIVERGENCE.md`. Owner: trainex team. Implementation target: `pinn/STATUS.md`.

| Item | Spec anchor | Forward obligation |
|------|-------------|--------------------|
| **Componentwise AD executable strategy** (NS-12 / AC-LOSS-01-AD) | `pinn_architecture.md` + `ctl_instruction.md` LOSS-01 | Canonical `u = t/T` autograd leaf; summed-output VJP rejected; executable memory/loop strategy is FUT work. |
| **Gradient-clipping mechanism realization** (M14 / AC-LOOP-04) | `pinn_architecture.md` §4.4 + `ctl_instruction.md` (C-schedule 7-10/5/3) | `clip_value = C_stage · torch.median(...)` mechanism; sub-items (bootstrap floor, exact early-stage C, lower floor, history reset) routed by the M14 packet. |
| **Batch constructor / DataLoader** (B-07 / B-08 / LOOP-01..03) | `ctl_instruction.md` LOOP section | `B_replay = 240`, `B_lookahead = 16`, `has_stage(k+1)` guard; two independent point sets (data-fidelity 8192 vs collocation 4096); mixed time sampling 50/50. |
| **ALM update + μ_p clamp** (LOOP-05) | `pinn_architecture.md` §4.2 | Optional / deferred ALM body; `[1e-4, 100]` clamp conditional only; dense-residual ALM rejected from default loop. |
| **Causal-mode mechanics** (D-04 / LOSS-04) | `pinn_architecture.md:424` + `ctl_instruction.md:1749,1803` | D-04 Option A; dense-residual pseudo-ALM rejected; scalar ALM deferred P2; causal exponent clip bound to be removed from live code. |

### Deferred to FUT-04 (training-loop impl + calibration)

Per `36-CODE-DIVERGENCE.md` and `36-HANDOFF.md`. Owner: trainex team. Calibration target: admitted-set evidence + Stage-0 pilot.

| Item | Spec anchor | Forward obligation |
|------|-------------|--------------------|
| **Adaptive-stage EDA + population floor** (CURR-01 / GAP-33-01) | `ctl_instruction.md` CURR-01 | Decide 5% / >10% / adaptive population floor from admitted-set EDA. |
| **Stage-0 pilot threshold calibration** (CURR-03 / D5-05) | `ctl_instruction.md` CURR-03 | Numeric thresholds for 4-criterion ADVANCE (training-loss plateau, validation-stability, physics-residual, energy-conservation) require FUT Stage-0 pilot. |
| **tau_L estimator / units selection** (GAP-33-02) | `ctl_instruction.md` CURR-02 | Owner-pending; Rosenstein-baseline-revisable, not yet locked. |
| **Huber-δ empirical / median-scaled calibration** (NS-13 / AC-LOSS-03) | `pinn_architecture.md:537` + `ctl_instruction.md:1741` | `delta_E = 1.0` baseline retained; empirical / median-scaled calibration deferred until admitted-set evidence exists. |
| **dt_out collocation scaling** (M16 / AC-LOOP-06) | `ctl_instruction.md:1819-1823` | Realized-as-deferred; candidate direction only; not implemented unless a future measurement motivates it. Inverse form NOT adopted. |
| **IPR / PSC / SASD training-side numeric confirmation** (LOOP-07 / LOOP-08) | `ctl_instruction.md` LOOP-07/08 | Provisional carry-forward with v1.5 VAL-02/03/04 forward-references; confirm or recalibrate. |
| **Epsilon train-vs-validate sensitivity** (D-06 caveat) | `ctl_instruction.md:287-303` | Confirm close-encounter mismatch negligible on admitted set (dual-context option). |
| **M16 / NS-13 defer-with-blocker** | (ledger rows) | Realized-as-deferred; AC-LOOP-06 / AC-LOSS-03 probe PASS verifies deferred state is the correct transcription. |
| **ALM μ_p clamp activation gate** | `pinn_architecture.md` LOOP-05 | Conditional clamp activation deferred; default-loop ALM update stays optional. |

### Non-Blocking Tech Debt (Working-Tree Observations)

| Item | Severity | Location | Recommended Action |
|------|----------|----------|--------------------|
| Uncommitted `consumer-task.md` and `consumer-task-backup2.md` in Phase 36 dir | INFO | `.planning/phases/36-acceptance-checks-re-verification-handoff/` | Untracked files left over from the watchdog chain; commit-or-clean during milestone closure. |
| Uncommitted `M AGENTS.md` working-tree edit | INFO | `AGENTS.md` | Not a v1.6 deliverable; review before `gsd-complete-milestone` (likely Phase 35 or 36 cross-reference update). |
| `v1.6-MILESTONE-AUDIT.md` not yet written | INFO | `.planning/` | Agent A (`/gsd-audit-milestone`) producing in parallel; will land before `/gsd-complete-milestone`. |

### Lessons Learned (for v1.7 and trainex handoff)

- **Two-stage ERW pipeline scales**: 8 anonymized research reports → 1 consolidation agent produced a resolution doc that survived READINESS verification (18/18 finding coverage, 0 contradictions, 0 HC violations). Same pipeline works for future Issue-04/05/06 candidates.
- **Whole-number readiness gates (Phase 31, not Phase 24.5) avoid the "urgent insertion" framing**: deliberately inserted at milestone init, not retrofitted. Same approach should apply to future milestones.
- **D-36-17 terminal-anchor extension was necessary and should have been anticipated**: pre-ledger families (PKG complete before Phase 32 ledger existed) and provisional carry-forwards (LOOP-07/08 with no dedicated ledger row) both needed non-ledger anchors. v1.7 should bake this into the R6 rule from phase 0.
- **Cycle-4 HIGH-B partition discipline is essential**: each ledger finding classified exactly once across Fixed / Intentionally Unchanged / Deferred. Without the discipline, double-counting risks silently under-reporting what was actually decided.
- **Freshness-checked ledger promotion is cheap and strong**: post-write SHA-256 recorded once per promotion; verifier can re-derive the ledger state from the committed hash. Same pattern should apply to trainex side artifacts.
- **Owner-driven gap resolution cadence**: every v1.6 gap was surfaced at the right SPEC/UAT gate (Phase 32 SPEC, Phase 34 UAT, Phase 35 SPEC, Phase 36 SPEC) with AskUserQuestion options. The cadence is auditable in `32-DISCUSSION-LOG.md` / `33-DISCUSSION-LOG.md` / `34-DISCUSSION-LOG.md` / `35-DISCUSSION-LOG.md` / `36-DISCUSSION-LOG.md`.

---

## 7. Getting Started

### Repository Layout (v1.6-relevant)

```
3_body_problem/
├── pinn_instruction/
│   ├── issues/03-curriculum-and-training-loop.md             # Issue doc (non-authoritative; consolidated 2026-04-27 audit + blueprint + fragments)
│   ├── markdown_conversion/
│   │   ├── framework-specs/                                  # Spec-edit perimeter
│   │   │   ├── ctl_instruction.md                            # EDITED in v1.6 (CURR-01..05, LOOP-01..08, LOSS-01..04; LOSS-04 refined per GAP-35-01)
│   │   │   ├── pinn_architecture.md                          # EDITED in v1.6 (ALM μ_p clamp; gradient-clipping mechanism; LOSS-04 canonical home)
│   │   │   ├── sampling_method.md                            # FROZEN (SCOPE-08)
│   │   │   ├── data_quality_assessment.md                    # READ-ONLY (SCOPE-09; v1.5 carry)
│   │   │   ├── review-of-framework.md                        # READ-ONLY (SCOPE-09; characterized in PKG-08, no edits)
│   │   │   ├── stage-strat-revision.md                       # READ-ONLY (SCOPE-09; characterized in PKG-08, no edits)
│   │   │   ├── postspec-r1/                                  # Phase 30 byte-pinned snapshot (FRAMEWORK-SPECS-BUNDLE 3200 lines)
│   │   │   └── trainex-r1/                                   # Phase 30 package copy (folded as trainex routing input only, D-36-13)
│   │   └── framework-revisions/research_reports/03-curriculum-and-training-loop/
│   │       └── research_result/03-final-resolution.md        # User-produced candidate verdict source (commit 49fb7958)
├── simulation_data/                                          # On-disk dataset + scripts (SCOPE-05 carveout)
│   ├── Data/                                                 # Brutus outputs (base + gold)
│   ├── Documentation/                                        # Dataset README, blacklists, ID lists
│   ├── Scripts/                                              # ic_generation/, metrics_calculation/, Validation/, brutus_runners/
│   ├── Data/forensic/                                        # Quarantined invalid outputs (carried from v1.5 DATA-05)
│   └── Validation/                                           # Prescreening artifacts (carried from v1.5)
├── pinn/                                                     # v1.3-era live code — NOT grounding; reference only for FUT-01
│   ├── basic_architecture.py                                 # (NOT modified in v1.6; protected-path guard PASS)
│   └── data-processing-pipeline-full.py                      # (NOT modified in v1.6; protected-path guard PASS)
├── .planning/
│   ├── ROADMAP.md                                            # v1.6 milestone + 7 phases (30–36)
│   ├── REQUIREMENTS.md                                       # 32 v1.6 requirements (PKG 4 + EVID 5 + CURR 5 + LOOP 8 + LOSS 4 + VER 6)
│   ├── STATE.md                                              # current_phase=36, last_activity=2026-07-02, completion-line to be added
│   ├── PROJECT.md                                            # What This Is, core value, requirements overview
│   ├── MILESTONES.md                                         # Per-milestone one-line summaries (v1.0–v1.5 shipped)
│   ├── milestones/
│   │   ├── v1.6-GAPS.md                                      # 10 gaps, 0 open, 10 RESOLVED-WITH-INSTRUCTION
│   │   ├── v1.6-MILESTONE-AUDIT.md                           # (Agent A producing; will land before /gsd-complete-milestone)
│   │   ├── v1.6-REQUIREMENTS.md                              # (carried from current REQUIREMENTS.md at /gsd-complete-milestone)
│   │   └── v1.6-ROADMAP.md                                   # (carried from current ROADMAP.md at /gsd-complete-milestone)
│   ├── phases/                                               # 7 v1.6 phase directories
│   │   ├── 30-research-package-assembly/                     # 30-CONSOLIDATION-PLAN, 5 SUMMARYs, research_package/, evidence/
│   │   ├── 31-resolution-doc-readiness-verification/         # 31-VERIFICATION, 31-READINESS-REPORT, 31-RESOLUTION-MAP
│   │   ├── 32-evidence-framework-issue-ledger-conflict-adjudication/
│   │   │   ├── 32-ISSUE-LEDGER.md                            # 18 rows, 18 VERIFIED (post-write SHA-256 184cb56f…)
│   │   │   ├── 32-VERIFICATION.md
│   │   │   ├── evidence/                                     # 18 evidence packets (one per ledger row)
│   │   │   └── 32-GAPS.md
│   │   ├── 33-curriculum-stage-contracts/                    # 4 SUMMARYs, 33-VERIFICATION, evidence/ (AC-CURR-01..05)
│   │   ├── 34-training-loop-batch-construction-contracts/    # 5 SUMMARYs, 34-VERIFICATION, evidence/ (AC-LOOP-01..08)
│   │   ├── 35-loss-energy-weight-contracts/                  # 4 SUMMARYs, 35-VERIFICATION, evidence/ (AC-LOSS-01..04)
│   │   └── 36-acceptance-checks-re-verification-handoff/     # 5 SUMMARYs, 36-VERIFICATION, 36-ACCEPTANCE-MANIFEST,
│   │                                                          #   36-PROBE-RESULTS, 36-LEDGER-CLOSURE, 36-HANDOFF, 36-CODE-DIVERGENCE,
│   │                                                          #   36-GAPS, evidence/, probes/, run-ac-suite.sh
│   ├── reports/                                              # Milestone summaries (for team onboarding)
│   │   ├── MILESTONE_SUMMARY-v1.4.md
│   │   ├── MILESTONE_SUMMARY-v1.5.md
│   │   └── MILESTONE_SUMMARY-v1.6.md                         # THIS FILE
│   ├── todos/pending/trainex-r1-research-handoff.md          # Routing obligation only (D-36-13; not executed in v1.6)
│   └── config.json                                           # Project config
├── docs/                                                     # Lifecycle-managed project docs (runbooks, designs, reviews)
└── tools/                                                    # Verification tooling (spec-render-check detector suite)
```

### Where to Look First (by role)

| Role | Start here |
|------|-----------|
| **New contributor wanting to understand v1.6** | This document (sections 1, 3, 6, 7) |
| **Spec engineer auditing v1.6 changes** | `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` + each row's `evidence/{id}.md` |
| **Trainer starting FUT-04** | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-HANDOFF.md` (FUT-04 section) + `36-CODE-DIVERGENCE.md` (FUT-04 section) |
| **Implementer starting FUT-01** | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-CODE-DIVERGENCE.md` (FUT-01 section) + `ctl_instruction.md` + `pinn_architecture.md` |
| **Auditor running `/gsd-audit-milestone` (Agent A)** | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-VERIFICATION.md` + `36-PROBE-RESULTS.md` + `.planning/REQUIREMENTS.md` traceability table |
| **User picking up next milestone** | `.planning/STATE.md` (current_phase=36, last_activity=2026-07-02) → `/gsd-complete-milestone` then `/gsd-new-milestone` |

### Common Commands

| Purpose | Command |
|---------|---------|
| Check current branch + working tree | `git status --short --branch` |
| List v1.6 phase preflight tags | `git tag -l 'v1.6-pre-*' \| sort -V` |
| See milestone gap index | `head -8 .planning/milestones/v1.6-GAPS.md` |
| See milestone audit verdict (when Agent A lands) | `head -5 .planning/v1.6-MILESTONE-AUDIT.md` |
| See milestone handoff structure | `grep -E '^## (Evidence Used\|1\. Fixed\|2\. Intentionally Unchanged\|3\. Deferred\|4\. SI\|5\. FUT-01\|6\. Milestone)' .planning/phases/36-acceptance-checks-re-verification-handoff/36-HANDOFF.md` |
| See FUT-01 forward obligations | `grep -E '^(FO-1\|FO-2\|## )' .planning/phases/36-acceptance-checks-re-verification-handoff/36-CODE-DIVERGENCE.md` |
| Run all 26 acceptance probes | `bash .planning/phases/36-acceptance-checks-re-verification-handoff/run-ac-suite.sh` |
| Run the 1 companion traceability probe | `python3 .planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-traceability.py` |
| See v1.6 commit timeline | `git log --oneline --grep='v1.6' \| tail -10` (latest); `git log --oneline --reverse --grep='v1.6' \| head -10` (earliest) |
| Verify protected-path guard | `git diff --stat v1.6-pre-phase-30..HEAD -- pinn/ pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn_instruction/markdown_conversion/framework-specs/data_quality_assessment.md pinn_instruction/markdown_conversion/framework-specs/review-of-framework.md pinn_instruction/markdown_conversion/framework-specs/stage-strat-revision.md` (must be empty) |

### Validation Evidence

- **Ledger:** `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` — 18 rows, 18 `VERIFIED`, 0 `PENDING` (post-write SHA-256 `184cb56ff62caba140e9f35e9ddd857cd924d56354eed49f6de7d4144b5a7e10`).
- **Acceptance probes:** `.planning/phases/36-acceptance-checks-re-verification-handoff/36-PROBE-RESULTS.md` — re-run 2026-07-02T00:39:33Z, **26/26 PASS**.
- **Companion traceability probe:** `.planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-traceability.py` — 1/1 PASS.
- **Phase 36 UAT:** `.planning/phases/36-acceptance-checks-re-verification-handoff/36-UAT.md` — 11/11 independent checks pass.
- **Protected-path guard:** `git diff` over `pinn/` + frozen specs is empty (per `run-ac-suite.sh` probe).
- **Handoff:** `.planning/phases/36-acceptance-checks-re-verification-handoff/36-HANDOFF.md` (sections: Evidence Used, SI Reconciliation, Fixed, Intentionally Unchanged, Deferred, FUT-01, FUT-04, Consumption Notes, Milestone-Closure Gate).

---

## Stats

- **Timeline:** 2026-06-18 (Phase 30 first commit) → 2026-07-02 (Phase 36 closure) — **14 days** (start tag `v1.6-pre-phase-30` dated 2026-06-18T14:33:56+08:00; HEAD `1ba34d96` dated 2026-07-02T17:29:03+08:00)
- **Phases:** 7 / 7 complete (100%)
- **Plans:** 28 / 28 (Phase 30: 5, Phase 31: 1, Phase 32: 4, Phase 33: 4, Phase 34: 5, Phase 35: 4, Phase 36: 5)
- **Requirements:** 32 / 32 satisfied (100%)
- **Gaps:** 10 total — 0 open, 10 RESOLVED-WITH-INSTRUCTION, 0 deferred
- **Ledger:** 18 / 18 VERIFIED, 0 PENDING, 0 IN_PROGRESS, 0 FIX_APPLIED
- **Acceptance probes:** 26 / 26 PASS (re-run 2026-07-02T00:39:33Z)
- **Companion traceability probe:** 1 / 1 PASS
- **UAT independent checks:** 11 / 11 pass
- **Commits:** 184 (`v1.6-pre-phase-30..HEAD`, all on `milestone/v1.6`)
- **Files changed:** 312 (+60,265 / −328) since `v1.6-pre-phase-30` (includes pre-pinned framework spec bundles, framework-revisions research_reports, trainex-r1 specs, git-policy scripts + tests; spec-only deltas on `ctl_instruction.md` +392 and `pinn_architecture.md` +71)
- **Contributors:** 1 (Starlordpd233)

---

*Generated 2026-07-02 by `/gsd-milestone-summary v1.6` (Agent B in the closure-chain watchdog: Agent A → `/gsd-audit-milestone`, this Agent B → `/gsd-milestone-summary`, Agent C → `/gsd-extract-learnings`).*