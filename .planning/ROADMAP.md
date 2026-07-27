# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- ✅ **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (shipped 2026-07-02; 32/32 requirements, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED; FUT-01/FUT-04 routed to the trainex track; archived under [`milestones/v1.6-*`](milestones/))
- ✅ **v2.0 CTL-PINN Training Viability Slice** — Phases 37–43 (shipped 2026-07-23; the project's first **build** milestone / trainex track — Stage-0-first end-to-end training slice from the ratified trainex-r1a decisions; 42/42 requirements Complete; audit `tech_debt` with zero blockers; the sole held-out physics gate rendered an honest **FAIL** (`ε_H = 237.21` vs ≤ 1e-5) and the owner signed **`adjust`** — Stage-0 mechanical slice retained, PLAT-01..07 blocked, physics-gate investigation routed to the next milestone; archived under [`milestones/v2.0-*`](milestones/))
- ✅ **v2.1 Physics-Gate Investigation & trainex-r2 Research Package** — Phases 44–45 (shipped 2026-07-24; the separately governed investigation routed by the v2.0 `adjust` verdict — read-only forensics over the retained v2.0 artifacts + trainex-r2 ERW package delivery; 7/7 requirements, package audited PASS; a bounded conformance audit found the v2.0 pilot diverged from the locked specs in five verified respects, qualifying the Phase 44 diagnosis and seeding a conformance-first next milestone; archived under [roadmap](milestones/v2.1-ROADMAP.md), [requirements](milestones/v2.1-REQUIREMENTS.md), [gaps](milestones/v2.1-GAPS.md), [phase archive](milestones/v2.1-phases/))
- 🚧 **v2.2 Stage-0 Conformance Repair & Valid Re-Run** — Phases 46–52 (started 2026-07-25; repair the verified Stage-0 conformance divergences C-01..C-08, prove the repair with gate-aligned instrumentation and a preflight conformance gate, re-run Stage-0 across the three-seed band, and spend the single owner-authorized held-out evaluation on a conformant run — the first valid verdict on the *design*; 22 requirements across CONF/INST/GATE/TEST/RUN/EVAL/DIAG/VER; closes at the verdict + the re-derived diagnosis)
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

## 🚧 v2.2 Stage-0 Conformance Repair & Valid Re-Run (Executing)

**Milestone Goal:** Establish, for the first time, a **valid** test of the Stage-0 design: repair the verified conformance divergences, prove the repair with gate-aligned instrumentation and a preflight gate, re-run Stage-0 under the corrected recipe, and spend the one authorized held-out evaluation on a run that is actually the specified experiment. The milestone ends with a verdict on the *design* — which the v2.0 pilot never produced, because what it graded was not the design. **What this milestone deliberately does not do:** tune the recipe. If the conformant run still fails, that failure is the first real evidence about the design, and recipe adjudication (with the trainex-r2 resolution doc as a candidate verdict source) is v2.3.

**Granularity:** standard (7 phases, 22 requirements: CONF-01..07, INST-01..03, GATE-01..03, TEST-01..02, RUN-01..03, EVAL-01, DIAG-05, VER-19..20)
**Coverage:** 22/22 v2.2 requirements mapped (VER-19 verified at roadmap creation)
**Branch:** work continues in `.worktrees/trainex`; branch `milestone/v2.2` to be cut from the v2.1 deliverable tip at first phase execution (v2.0/v2.1 precedent — no branch op during setup). Per-plan atomic commits via `scripts/agent-commit`; no protected-branch push; master merge is user-controlled integration.

### Conformance discipline (applies to all phases)

- **Hard boundaries (SCOPE-27..32):** training runs authorized, **Stage-0 only** (no Stage-1+, no PLAT-01..07); **exactly ONE held-out evaluation**, gated on EVAL-01; **conformance-only iteration** — repairing divergences against the spec, never adjusting hyperparameters against observed results; **no framework-spec edits** (amendments accumulate in the VER-20 routing list); **the trainex-r2 report is NOT a grounding source** (only its independently verified `[FACT-W]` findings may be used); **charter-workstream coordination** — v2.2 owns the minimum gate (GATE-01..03), the concurrent verification-enforcement charter owns the general regime.
- **The evaluation policy (owner-ratified 2026-07-25, binding as EVAL-01):** *"One additional held-out evaluation is authorized for the corrected Stage-0 implementation, conditional on (i) preflight conformance passing with zero unwaived divergences, (ii) RG-02 resolved, and (iii) validation-side gate metrics recorded for the run being submitted. Any evaluation beyond this one requires a new owner decision. No evaluation may be spent on a run that has not passed (i)–(iii)."* The standing "do NOT re-run" (v2.0 audit W-1; exhausted-budget note) governs re-evaluating the **v2.0 seed-42 checkpoint** — protecting the v2.0 record and its receipt-based refusal path. It is *not* a prohibition on evaluating a future model: a corrected implementation is a new question, not a re-run.
- **Grounding (authoritative inputs):** the locked framework specs (`ctl_instruction.md`, `pinn_architecture.md` — v1.4/v1.5/v1.6); the five v2.1 gap rulings (2026-07-24, `.planning/milestones/v2.1-GAPS.md`); the conformance audit's verified defect inventory C-01..C-08 (`docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`) — whose "verified clean" section is equally load-bearing: do not re-audit the component math; the owner-ratified evaluation policy. **NOT grounding:** the trainex-r2 research report (SCOPE-31) — silently consulting its tuning analysis would re-contaminate the milestone with the false premise this effort exists to remove.
- **Owner checkpoints (blocking, never auto-decided):** ① GAP-45-01 `L_data` reduction (Phase 48 — presented with computed term magnitudes from the retained runs); ② N for invariant B (Phase 49 — the front-advance window); ③ scope decision if CONF-01 reveals a frame defect (Phase 46 — the branch point); ④ the go / adjust / rethink verdict (Phase 51).
- **Gap discipline:** any source-silent physics/spec adjudication call is recorded in the phase-local `NN-GAPS.md` and the milestone index `.planning/milestones/v2.2-GAPS.md` (created on first gap, standing trigger) and routed to the owner — never decided inline (the build-track analog of the STOP protocol). The S_H pipeline may surface dataset facts interacting with v1.5-locked contracts — route as gaps, do not adjudicate inline.

## Phases

**Phase Numbering:** integer phases 46–52 continue from v2.1's Phase 45 (numbering does not reset). Decimal phases reserved for urgent insertions.

- [ ] **Phase 46: Frame Resolution & Gate-Aligned Validation** — Settle RG-02 (raw positions vs `r' = r/D` training targets) via the train-free residual-on-stored-targets check — no training run — and add per-trajectory ε_H/SCS validation metrics via the existing `pinn.verification.gate_metrics` functions, so validation carries a conservation signal where none exists. **Branch point:** a wrong frame is a sixth, data-path divergence — surface as an owner scope decision, never absorbed silently. (CONF-01, INST-01)
- [ ] **Phase 47: S_H Pipeline** — A real preprocessing stage computing the dataset-wide statistic `S_H = median_train(K0 + Uabs0)` over the admitted set, persisted in training metadata with fail-closed validation (finite, strictly positive, per spec §3.4), and the `ε_H = 1e-4 · S_H` wiring with the prohibited `+1e-12` fallback floor removed. The largest single work item in the milestone. (CONF-02, CONF-03)
- [ ] **Phase 48: Loss-Math Conformance** — The loss math the trainer executes becomes the loss math the specs lock: `R̄ = (1/3)Σ_i‖f_i‖²`, the causal-exponent clip (invariant A, chosen against the corrected `R̄`), `λ_E^max → 0`, and the `L_data` reduction — plus per-term gradient-statistics logging, the two divergence-defending tests corrected in the same change, and assembly-boundary conformance tests. **Blocking owner checkpoint:** GAP-45-01 `L_data` reduction with computed term magnitudes. Ordering: CONF-04 before CONF-05. (CONF-04..07, INST-02, TEST-01, TEST-02)
- [ ] **Phase 49: Conformance Gate** — The minimum enforcement subset that protects the single look: preflight asserts the full PHYS-05 per-stage table at run start and every stage boundary; the placeholder census (every spec-required loss quantity resolves real or is explicitly owner-waived); runtime invariants A/B failing loud and early; the known-divergence register surfaced in the run record. **Owner checkpoint:** N for invariant B. Coordinated with the charter workstream per SCOPE-32. (GATE-01..03, INST-03)
- [ ] **Phase 50: Valid Stage-0 Re-Run** — Stage-0 runs end-to-end under the corrected recipe across the re-established three-seed band (v2.0 protocol, comparable runs). Training authorized (SCOPE-27). Iteration is conformance-only (SCOPE-29). (RUN-01, RUN-02)
- [ ] **Phase 51: The Authorized Evaluation** — The three EVAL-01 preconditions verified and recorded, the evaluator invoked **once**, and the owner's go / adjust / rethink verdict on the design rendered (the v2.0 ACC-06 pattern) — the first valid grade the design has ever received. (RUN-03, EVAL-01)
- [ ] **Phase 52: Diagnosis Re-Derivation & Handoff** — The GAP-44-02 obligation discharged: the Phase 44 diagnosis re-derived against the conformant run with an acceptance check; 22/22 traceability closed; the four-item spec-amendment routing list handed off for a later spec milestone. (DIAG-05, VER-19, VER-20)

## Phase Details

### Phase 46: Frame Resolution & Gate-Aligned Validation

**Goal**: The last remaining way the next run could be invalid is settled, and validation carries a conservation signal where none exists.
**Depends on**: v2.1 archive (complete). Ungated — first v2.2 phase.
**Requirements**: CONF-01, INST-01
**Plans:** 5/7 plans executed

Plans:
**Wave 1**

- [x] 46-01-PLAN.md — Wave-0 test scaffolding: `tests/phase46/` skip convention, StageIndex-shaped stub, dual-frame/degenerate/confound fixtures (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 46-02-PLAN.md — CONF-01 probe core: symmetric arms, numerics-only tolerance, confound discriminators, fail-closed 4-way verdict (wave 2)
- [x] 46-03-PLAN.md — INST-01 gate composition core: frame-explicit full-pool `gate_metrics` pass, atomic sidecar, compact JSONL fields (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 46-04-PLAN.md — CONF-01 evidence writer + manifest-parametric CLI, D-05 deterministic artifact, redaction/containment (wave 3)
- [x] 46-05-PLAN.md — INST-01 isolation + artifact test suites: evaluator-import isolation, mode restore, schema fail-closed, pointer discipline (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 46-06-PLAN.md — The single real-corpus evidence run, `46-VERDICT.md`, and D-08/D-09 branch routing (wave 4; `autonomous: false` — owner branch point)

**Wave 5** *(blocked on Wave 4 completion)*

- [ ] 46-07-PLAN.md — Frame ratification (`RATIFIED_VALIDATION_FRAME`), `train.py`/`summary.py` wiring, EVAL-01 precondition (iii) projection (wave 5; blocked until D-08 or owner-resolved D-09)

**Success Criteria** (what must be TRUE):

  1. RG-02 is settled by the train-free residual-on-stored-targets check — no training run — with the verdict (raw positions vs `r' = r/D`) and its evidence recorded (CONF-01).
  2. If the check shows the target frame *is* wrong, the finding is surfaced as an owner scope decision (a sixth divergence, data-path not loss-math) — Phases 47–48 grow accordingly and the scope change is never absorbed silently (CONF-01 branch point).
  3. Per-trajectory ε_H/SCS are computed on the validation split via the existing `pinn.verification.gate_metrics` functions and recorded per run; validation is no longer limited to `final_val_loss`/`step`/`trend` (INST-01).

### Phase 47: S_H Pipeline

**Goal**: The loss's energy scale is a real dataset statistic, not a per-anchor stand-in: `S_H` is computed over the admitted set and the spec's ε_H formula is wired end-to-end.
**Depends on**: Phase 46 — `K0`/`Uabs0` are frame-dependent (`H' = D·H`), so the frame must be settled before the median is computed.
**Requirements**: CONF-02, CONF-03
**Success Criteria** (what must be TRUE):

  1. A preprocessing stage computes `S_H = median_train(K0 + Uabs0)` over the admitted set and persists it in training metadata (CONF-02).
  2. `S_H` validation fails closed per spec §3.4: non-finite or `≤ 0` is a preprocessing/metadata validation failure (CONF-02).
  3. `ε_H = 1e-4 · S_H` is wired into the loss assembly and the §3.4-prohibited `+1e-12` additive fallback floor is removed (CONF-03).

### Phase 48: Loss-Math Conformance

**Goal**: The loss math the trainer executes is the loss math the specs lock — `R̄`, the causal clip, `λ_E^max`, and `L_data` all conform — and the test suite is corrected to defend conformance instead of divergence.
**Depends on**: Phase 47 (the `S_H`/`ε_H` path the loss assembly consumes).
**Requirements**: CONF-04, CONF-05, CONF-06, CONF-07, INST-02, TEST-01, TEST-02
**Blocking owner checkpoint**: the GAP-45-01 `L_data` reduction, surfaced with computed term magnitudes from the retained runs — the choice is made against numbers, never auto-decided.
**Ordering constraint**: CONF-04 before CONF-05 — the clip must be chosen against the corrected `R̄` (3× larger, underflows sooner).
**Success Criteria** (what must be TRUE):

  1. `R̄` is the locked `(1/3) Σ_i ‖f_i‖²` (CONF-04), and the causal-exponent clip satisfies invariant A (no causal weight exactly zero), chosen against the corrected `R̄` with the bound recorded in the plan and the run record (CONF-05).
  2. `λ_E^max` is reverted to the locked Stage-0 value `0` (CONF-06).
  3. The `L_data` component reduction is implemented per the owner ruling on GAP-45-01, obtained at the blocking checkpoint with computed term magnitudes presented (CONF-07).
  4. Per-term gradient statistics are logged — the Phase-35 contract's named precondition for any reweighting decision, finally satisfied (INST-02).
  5. The two divergence-defending tests are corrected in the same change as the code fix (TEST-01), and assembly-boundary conformance tests assert the values the loss *actually receives* equal the spec values for `R̄` and `ε_H` at minimum (TEST-02).

### Phase 49: Conformance Gate

**Goal**: A preflight + runtime gate exists that makes an invalid run structurally unable to spend the single look — the minimum enforcement subset, coordinated with the charter workstream.
**Depends on**: Phase 48 (the conformant loss assembly the gate asserts).
**Requirements**: GATE-01, GATE-02, GATE-03, INST-03
**Owner checkpoint**: N for invariant B (the front-advance window).
**Success Criteria** (what must be TRUE):

  1. Preflight asserts the full PHYS-05 per-stage table at run start and at every stage boundary — not merely the `≤1` cap (GATE-01, per GAP-45-03).
  2. The placeholder census passes or names explicit owner waivers: every spec-required quantity the loss consumes resolves to a real pipeline value — the check that would have caught the `S_H` gap (GATE-02).
  3. Runtime invariants fail loud and early: no causal weight exactly zero (invariant A); the causal front advances within the owner-ratified N steps (invariant B) (GATE-03).
  4. The known-divergence register is maintained and every open divergence is surfaced in the run record — a run carries its own caveats (INST-03).
  5. The SCOPE-32 coordination decision is recorded: charter deliverables consumed if they land, the minimum subset implemented otherwise — no duplicated regime.

### Phase 50: Valid Stage-0 Re-Run

**Goal**: Stage-0 runs end-to-end under the corrected recipe — the first run that is actually the specified experiment.
**Depends on**: Phase 49 (the gate must exist before Phase 51 spends the look).
**Requirements**: RUN-01, RUN-02
**Success Criteria** (what must be TRUE — the proposal's exit criteria):

  1. Preflight is clean with zero unwaived divergences at run start and across stage boundaries (RUN-01).
  2. Invariants A/B hold for a full run — no causal weight exactly zero, the causal front advances within N steps (RUN-01).
  3. Validation ε_H is recorded and characterized across three seeds, re-establishing the three-seed band matching the v2.0 protocol so the runs are comparable (RUN-02).
  4. Every iteration inside the phase is conformance-only — no hyperparameter adjusted against observed results (SCOPE-29).

### Phase 51: The Authorized Evaluation

**Goal**: The single authorized held-out evaluation is spent — once — on a run that passed every precondition, producing the first valid verdict on the design.
**Depends on**: Phase 50.
**Requirements**: RUN-03, EVAL-01
**Success Criteria** (what must be TRUE):

  1. The three EVAL-01 preconditions are verified and recorded before the evaluator is invoked: (i) preflight conformance passing with zero unwaived divergences, (ii) RG-02 resolved, (iii) validation-side gate metrics recorded for the run being submitted (EVAL-01).
  2. Before any held-out access, a dataset-free evaluator-assembly regression and a pre-invocation assertion prove that canonical predicted `r'` is paired with `u=t/T`, never raw native time; this discharges GAP-46-01 without adding a fourth EVAL-01 eligibility precondition (RUN-03).
  3. The evaluator is invoked exactly once; the invocation, its gating verification, and the receipt are recorded (RUN-03, SCOPE-28).
  4. The owner renders a go / adjust / rethink verdict on the design (the v2.0 ACC-06 pattern) — the first valid grade the design has ever received (RUN-03).

### Phase 52: Diagnosis Re-Derivation & Handoff

**Goal**: The milestone's obligations are closed: the Phase 44 diagnosis is re-derived against the conformant run, traceability is complete, and the spec-amendment routing list is handed off.
**Depends on**: Phase 51 (the conformant run and its evaluation).
**Requirements**: DIAG-05, VER-19, VER-20
**Success Criteria** (what must be TRUE):

  1. The Phase 44 diagnosis is re-derived from the conformant run with an acceptance check — recording either that the v2.0 failure is explained by conformance divergence (if Phase 51 passed) or the first evidence-grounded diagnosis of the *design* (if it failed) (DIAG-05, the GAP-44-02 obligation).
  2. Every requirement maps to exactly one phase and 22/22 coverage is verified at close (VER-19).
  3. The spec-amendment routing list is handed off with all four items: (a) the misleading "default" wording on `pinn_architecture.md` §4.1's `λ_phys^max` line, (b) a convention for marking locked-vs-default values inside a spec table, (c) the explicit `L_data` reduction as settled by CONF-07, (d) the aggregate gate statistic from GAP-44-01 (VER-20, SCOPE-30).

## Progress

**Execution Order:** 46 → 47 → 48 → 49 → 50 → 51 → 52 — strict dependency order (frame → S_H → loss math → gate → re-run → evaluation → handoff). The only branch is the Phase 46 CONF-01 branch point (frame defect ⇒ owner scope decision). No external research gate inside v2.2 (unlike v1.4–v1.6): the trainex-r2 resolution doc enters at v2.3, not here (SCOPE-31).

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 46. Frame Resolution & Gate-Aligned Validation | v2.2 | 5/7 | In Progress|  |
| 47. S_H Pipeline | v2.2 | 0/? | Not started | - |
| 48. Loss-Math Conformance | v2.2 | 0/? | Not started | - |
| 49. Conformance Gate | v2.2 | 0/? | Not started | - |
| 50. Valid Stage-0 Re-Run | v2.2 | 0/? | Not started | - |
| 51. The Authorized Evaluation | v2.2 | 0/? | Not started | - |
| 52. Diagnosis Re-Derivation & Handoff | v2.2 | 0/? | Not started | - |

---
*v2.2 created 2026-07-25 (`/gsd-new-milestone`, roadmap generated inline from the owner-ratified v2.2 roadmap proposal — v2.0/v2.1 precedent; no research spawn, since the milestone repairs existing code against already-locked specs and the proposal fully specifies the work). 7 phases (46–52) continuing numbering from v2.1's Phase 45; 22/22 requirements mapped (CONF-01→46, CONF-02/03→47, CONF-04..07+INST-02+TEST-01/02→48, GATE-01..03+INST-03→49, RUN-01/02→50, RUN-03+EVAL-01→51, DIAG-05+VER-19/20→52). Grounded in the locked framework specs, the five v2.1 gap rulings, the C-01..C-08 verified defect inventory, and the owner-ratified evaluation policy; scope boundaries SCOPE-27..32 are hard constraints. v2.1 archived under [`milestones/v2.1-*`](milestones/) (roadmap, requirements, gaps, phase dirs).*
