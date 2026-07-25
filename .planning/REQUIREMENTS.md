# Requirements: v2.1 Physics-Gate Investigation & trainex-r2 Research Package

**Defined:** 2026-07-23
**Core value:** An evidence-grounded diagnosis of how (and plausibly why) the Stage-0 model fails the physics-conservation gate, packaged so the owner's external research (ERW) can adjudicate the remedy — without the agent inventing the remedy.
**Total:** 7 requirements (4 DIAG + 3 PKG) + scope boundaries SCOPE-22..26.

Routed by the v2.0 owner verdict `adjust` (2026-07-22, `milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`): retain the mechanical slice, block full-platform expansion, investigate the failed gate and non-convergent pilot behavior under separate governance.

## v2.1 Requirements

### Physics-Gate Forensics (DIAG) — Phase 44

- [x] **DIAG-01**: The per-trajectory ε_H distribution over all 1,500 held-out test trajectories is characterized from the **preserved** evaluation artifacts (`runs/stage0-pilot-seed42/evaluation/metrics.json` — the evaluator is NOT re-run): summary statistics (min/median/max/percentiles), uniform-vs-tail failure structure, and any correlation with recorded trajectory attributes available in the artifacts — all derived re-derivably (analysis scripts + outputs retained in phase evidence). [ACC-03 receipt; SCOPE-22]
- [x] **DIAG-02**: The five-term loss composition (data / IC / causal-physics / soft-energy / angular-momentum) is decomposed per-step across the retained smoke and pilot runs (`runs/stage0-smoke`, `runs/stage0-pilot-seed{41,42,43}`: `logs/train.log.jsonl`, `tb/`, `status.json`), identifying which terms dominate at which step ranges, the warmup-spike attribution (which term spikes to ~3.7e9), and the interaction with the PHYS-05 scheduled weights — read-only over existing artifacts. [Phase 43 evidence; PHYS-05]
- [x] **DIAG-03**: The three-seed band (41/42/43) is characterized to distinguish budget-limited-but-descending behavior from recipe instability: per-seed validation-trend direction (2/3 worsened per 43-CALIBRATION.md), final-loss/validation spreads, and step-window trend analysis — with the Phase 38 single-trajectory overfit rung cited as the machinery-integrity control (the network CAN fit one trajectory; failure emerges at population scale/budget). [43-CALIBRATION.md; 38-VERIFICATION.md]
- [x] **DIAG-04**: A hypothesis-ranked diagnosis report (`44-DIAGNOSIS.md`) ranks at least four candidate causes — insufficient training budget, loss-term imbalance, optimization/warmup pathology, normalization-or-data-scale issue (plus any the evidence surfaces) — each with cited supporting AND contradicting evidence from DIAG-01..03, and **explicitly abstains from selecting a remedy** (remedy selection is owner-routed through the trainex-r2 ERW round). Any source-silent physics-adjudication call encountered is surfaced as a STOP-protocol gap, never decided. [SCOPE-26; STOP protocol]

### trainex-r2 ERW Package Assembly (PKG) — Phase 45

- [x] **PKG-09**: The trainex-r2 research package is assembled per the canonical ERW runbook (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`) under `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`: curated annotated document list with commit-pinned snapshots — the 44-DIAGNOSIS.md forensics report, the held-out receipt/metrics artifacts, 43-CALIBRATION.md/43-VERDICT.md, the relevant locked spec sections (Stage-0 recipe, loss catalog, scheduled weights, gate definition), and run-evidence excerpts. [ERW runbook]
- [x] **PKG-10**: The package poses neutrally framed research questions — no recommended answer, v1.5/v1.6 precedent — covering at minimum: training budget/steps, warmup and learning-rate schedule, loss weighting/balancing, curriculum pacing for Stage 0, and the evaluation-policy question (what evidence and governance a future held-out evaluation would require, given the exhausted budget). [SCOPE-22; ERW precedent]
- [x] **PKG-11**: The package carries a claims register separating verified facts (v2.0-verified numbers with citations) from unverified claims/hypotheses (the DIAG-04 rankings, marked as agent analysis — not established fact), plus a delivery note recording package contents, provenance (commit pins), and the expected return format (individual reports → one consolidated resolution doc as candidate verdict source, per v1.4/v1.5/v1.6). [PKG-07/PKG-03 precedent]

## Scope Boundaries (from the owner-signed verdict — hard constraints)

- **SCOPE-22**: NO held-out evaluation. The evaluator budget is exhausted (two failed attempts + one completed FAIL, all audited in 43-VERDICT.md). Any future evaluation requires a new, explicitly changed owner policy and a separately governed evidence boundary. Nothing in v2.1 invokes `pinn.evaluate` or touches the held-out test split.
- **SCOPE-23**: NO new training runs. v2.1 is read-only over retained artifacts. If the forensics concludes a diagnostic run would be decisive, that is surfaced as a gap with a concrete proposal for owner authorization — never executed unilaterally.
- **SCOPE-24**: NO framework-spec edits. A diagnosis implicating a spec parameter (e.g. a loss weight or schedule) becomes an ERW research question, not an edit. Specs remain read-only inputs.
- **SCOPE-25**: NO PLAT-01..07 or Stage-1 work. The full-platform block from the verdict stands throughout v2.1.
- **SCOPE-26**: Remedy selection is owner-routed. The diagnosis report ranks hypotheses with evidence; the remedy is adjudicated by the owner from the trainex-r2 resolution doc in a later milestone. The STOP protocol applies to any source-silent adjudication call.

## Future Requirements (deferred beyond v2.1)

- Trainex-r2 resolution-doc readiness verification and adjudication (the post-return milestone, v1.5-Phase-24.5-style gate) — cannot start until the owner's external research delivers.
- Remedy implementation (training-recipe changes) per the adjudicated verdicts.
- New held-out evaluation policy + evidence boundary (owner-defined).
- PLAT-01..07 full-platform work — still gated on a future `go`.
- Carried forward, unlinked: `trainex-r1-research-handoff` todo (r1b tuning round — relationship to trainex-r2 to be confirmed by the owner at package assembly) and `d-06-static-epsilon-sensitivity-check` todo (spec-side; candidate ERW question, owner to confirm inclusion at Phase 45).

## Out of Scope

- Re-running or retrying the held-out evaluator (SCOPE-22) — irreversible policy boundary, not a technical limitation.
- Training, tuning, or "quick experiment" runs (SCOPE-23) — the verdict's investigation is evidence-first.
- Spec edits, `sampling_method.md` remains frozen, read-only reports remain read-only (SCOPE-24 + standing SCOPE-08/09).
- Selecting or recommending THE remedy (SCOPE-26) — ranking hypotheses is in scope; deciding is not.
- Performing the external research itself — ERW is owner-led; the agent assembles the package only.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DIAG-01 | Phase 44 | Complete |
| DIAG-02 | Phase 44 | Complete |
| DIAG-03 | Phase 44 | Complete |
| DIAG-04 | Phase 44 | Complete |
| PKG-09 | Phase 45 | Complete |
| PKG-10 | Phase 45 | Complete |
| PKG-11 | Phase 45 | Complete |

**Coverage:** 7/7 mapped (Phase 44: 4 DIAG; Phase 45: 3 PKG). No orphans; no duplicates. SCOPE-22..26 are scope-boundary annotations, not numbered requirements (v2.0 SCOPE-16..21 precedent). PKG numbering continues from v1.6's PKG-08.

---
*Defined 2026-07-23 (`/gsd-new-milestone`, requirements gathered inline from the v2.0 close-out context — the adjust verdict, the milestone audit, and the owner-endorsed two-phase investigation scope; research spawn skipped: the milestone analyzes internal artifacts and the ERW package is the research vehicle).*
