# Requirements: v2.2 Stage-0 Conformance Repair & Valid Re-Run

**Defined:** 2026-07-25
**Core value:** A *valid* test of the Stage-0 design — repair the verified conformance divergences, prove the repair with gate-aligned instrumentation and a preflight gate, re-run Stage-0 under the corrected recipe, and spend the one authorized held-out evaluation on a run that is actually the specified experiment — never tuning the recipe against observed results.
**Total:** 22 requirements (7 CONF + 3 INST + 3 GATE + 2 TEST + 3 RUN + 1 EVAL + 1 DIAG + 2 VER) + scope boundaries SCOPE-27..32.

**Source:** the owner-ratified v2.2 roadmap proposal (`docs/work/designs/cross_cutting/v2.2-milestone-proposal/2026-07-25-v2.2-roadmap-proposal.md`), consumed by `/gsd-new-milestone` on 2026-07-25. Requirement texts below are transcribed from that proposal.

## Evaluation Policy (owner-ratified 2026-07-25 — binding)

> One additional held-out evaluation is authorized for the corrected Stage-0
> implementation, conditional on (i) preflight conformance passing with zero
> unwaived divergences, (ii) RG-02 resolved, and (iii) validation-side gate metrics
> recorded for the run being submitted. Any evaluation beyond this one requires a
> new owner decision. No evaluation may be spent on a run that has not passed
> (i)–(iii).

This becomes requirement **EVAL-01** and scope boundary **SCOPE-28**.

**Related clarification, also load-bearing.** The standing "do NOT re-run" (v2.0 audit warning W-1; the exhausted-budget note) governs re-evaluating **the v2.0 seed-42 checkpoint**, protecting the integrity of the v2.0 record and its receipt-based refusal path. It is *not* a prohibition on evaluating a future model. A corrected implementation is a new question, not a re-run. Without this distinction stated here, v2.2 is impossible by construction.

## Grounding (authoritative inputs)

1. **The locked framework specs** (`ctl_instruction.md`, `pinn_architecture.md`) as completed by v1.4/v1.5/v1.6. Hard constraints.
2. **The five v2.1 gap rulings** (2026-07-24): GAP-45-03 per-stage PHYS-05 values are locked; GAP-45-02 λ_E provenance unrecoverable, treated as drift, reverts to 0; GAP-45-04 invariant mandated with the number deferred to the implementer; GAP-45-01 deferred with a pre-re-run condition; GAP-44-02 erratum plus mandatory re-derivation. Record: `.planning/milestones/v2.1-GAPS.md`.
3. **The conformance audit's verified defect inventory** C-01..C-08: `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`. Its "verified clean" section is equally load-bearing — do not re-audit the component math.
4. **The evaluation policy** above (new, owner-ratified 2026-07-25).

**NOT grounding:** the trainex-r2 research report (SCOPE-31).

## v2.2 Requirements

### Conformance Repair (CONF) — Phases 46–48

- [x] **CONF-01**: Resolve RG-02: settle whether training targets are raw positions or `r' = r/D`, via the train-free residual-on-stored-targets check. No training run. **Branch point:** if the target frame *is* wrong, that is a sixth divergence and a data-path defect rather than a loss-math one — surface as an owner scope decision, never absorbed silently. [RG-02; proposal Phase 46]
- [ ] **CONF-02**: Build the `S_H` pipeline: `S_H = median_train(K0 + Uabs0)` over the admitted set, persisted in training metadata. `S_H` must be finite and strictly positive; non-finite or `≤ 0` is a preprocessing/metadata validation failure that fails closed (spec §3.4). [spec §3.4; conformance audit]
- [ ] **CONF-03**: Wire `ε_H = 1e-4 · S_H` into the loss assembly and remove the `+1e-12` additive fallback floor, which §3.4 explicitly prohibits. [spec §3.4]
- [ ] **CONF-04**: Correct `R̄` to the locked `(1/3) Σ_i ‖f_i‖²` (from the implemented `(1/9)Σ`). [locked loss contract; conformance audit]
- [ ] **CONF-05**: Implement a causal-exponent clip satisfying invariant A (no causal weight may be exactly zero), **chosen against the corrected `R̄`** — which is 3× larger and underflows sooner. Record the chosen bound in the plan and the run record. [GAP-45-04 owner ruling: invariant mandated, number deferred to the implementer with a recording obligation]
- [ ] **CONF-06**: Revert `λ_E^max` to the locked Stage-0 value `0`. [GAP-45-02 owner ruling: λ_E provenance unrecoverable, treated as drift]
- [ ] **CONF-07**: Implement the `L_data` component reduction per the owner ruling on GAP-45-01. [GAP-45-01: deferred with a pre-re-run condition; blocking owner checkpoint at Phase 48, presented with computed term magnitudes from the retained runs]

### Instrumentation (INST) — Phases 46, 48, 49

- [x] **INST-01**: Gate-aligned validation metrics: per-trajectory `ε_H`/`SCS` on the validation split, via the existing `pinn.verification.gate_metrics` functions. Currently validation records only `final_val_loss`, `step`, `trend` — no conservation signal at all. [conformance audit; EVAL-01 precondition (iii)]
- [ ] **INST-02**: Log per-term gradient statistics — the precondition the locked Phase-35 contract names for any reweighting decision, never satisfied. [Phase-35 loss/energy-weight contract]
- [ ] **INST-03**: Maintain the known-divergence register; the run record surfaces every open divergence so a run carries its own caveats. [conformance audit]

### Minimum Enforcement (GATE) — Phase 49

- [ ] **GATE-01**: Preflight asserts the **full** PHYS-05 per-stage table at run start and at every stage boundary (per GAP-45-03), not merely the `≤1` cap. [GAP-45-03 owner ruling: per-stage PHYS-05 values are locked]
- [ ] **GATE-02**: Preflight placeholder census: every spec-required quantity the loss consumes resolves to a real pipeline value, or is explicitly owner-waived for that run. This is the check that would have caught the `S_H` gap. [conformance audit]
- [ ] **GATE-03**: Runtime invariants: no causal weight exactly zero (invariant A); the causal front advances within N steps (invariant B — N is an owner checkpoint). Fail loud, fail early. [GAP-45-04; N owner checkpoint at Phase 49]

### Test-Suite Correction (TEST) — Phase 48

- [ ] **TEST-01**: Correct the two tests that currently defend divergences (C-08), in the same change as the code fix, or CI fails the fix. [conformance audit C-08]
- [ ] **TEST-02**: Add assembly-boundary conformance tests: given known inputs, assert the value the loss *actually receives* equals the spec value — for `R̄` and `ε_H` at minimum. The existing tests cover the components, which are already correct. [conformance audit]

### Re-Run & the Authorized Evaluation (RUN / EVAL) — Phases 50–51

- [ ] **RUN-01**: Stage-0 re-run under the corrected recipe, with conformance-only iteration (SCOPE-29). [SCOPE-27 authorizes Stage-0 training]
- [ ] **RUN-02**: Re-establish the three-seed band, matching the v2.0 protocol so the runs are comparable. [v2.0 pilot protocol]
- [ ] **RUN-03**: Execute the single authorized held-out evaluation, gated on EVAL-01. Before any held-out access, prove with a dataset-free regression and pre-invocation assertion that the evaluator pairs canonical predicted `r'` with `u=t/T`; raw native time with scaled predictions is prohibited. [SCOPE-28; GAP-46-01 delegated ruling 2026-07-26]
- [ ] **EVAL-01**: The evaluation policy above, as a binding requirement with its three preconditions checked and recorded before the evaluator is invoked. [owner-ratified 2026-07-25]

### Diagnosis Re-Derivation & Traceability (DIAG / VER) — Phase 52

- [ ] **DIAG-05**: Re-derive the Phase 44 diagnosis from the conformant run, with an acceptance check — the GAP-44-02 mandated requirement on which Phase 44 was permitted to stay closed. [GAP-44-02 owner ruling: erratum plus mandatory re-derivation]
- [ ] **VER-19**: Requirement traceability: every requirement maps to exactly one phase. [roadmap coverage]
- [ ] **VER-20**: Hand off the spec-amendment routing list: (a) the misleading "default" wording on `pinn_architecture.md` §4.1's `λ_phys^max` line; (b) a convention for marking locked-vs-default values inside a spec table; (c) the explicit `L_data` reduction once CONF-07 is settled; (d) the aggregate gate statistic from GAP-44-01. [SCOPE-30 — spec prose is not edited in v2.2]

## Scope Boundaries (owner-ratified — hard constraints)

| ID | Boundary |
|----|----------|
| SCOPE-27 | **Training runs AUTHORIZED** — Stage-0 only. No Stage-1+, no PLAT-01..07 platform work. This is the boundary v2.1 could not cross. |
| SCOPE-28 | **Exactly ONE held-out evaluation**, gated on EVAL-01's three preconditions. Any further evaluation requires a new owner decision. |
| SCOPE-29 | **NO recipe tuning.** Iteration inside v2.2 is *conformance-only* — repairing divergences against the spec, never adjusting hyperparameters against observed results. This is what protects the single look; violating it re-creates the leakage the budget exists to prevent. |
| SCOPE-30 | **No framework-spec file edits.** Spec-text amendments accumulate in the VER-20 routing list for a later spec milestone. Decisions are recorded and implemented; spec prose is not touched. |
| SCOPE-31 | **The trainex-r2 report is not a grounding source for v2.2.** Its Q1–Q6 answers reason carefully about a recipe that did not run; its value here is limited to the `[FACT-W]` findings already independently verified. It enters at v2.3 as a premise-qualified candidate verdict source. Silently consulting its tuning analysis would re-contaminate the milestone with the false premise this whole effort exists to remove. |
| SCOPE-32 | **Coordination with the verification-enforcement workstream.** v2.2 owns the *minimum* gate needed to protect its single look (GATE-01..03). The concurrent charter workstream owns the general regime — normative-statement index, full CI integration, waiver policy, thresholds X/M. Neither duplicates the other; the charter is the authority on the general design. Charter: `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`. |

## Future Requirements (deferred beyond v2.2)

- **v2.3 recipe adjudication** — if the conformant run still fails, that failure is the first real evidence about the design; recipe adjudication follows with the trainex-r2 resolution doc as a premise-qualified candidate verdict source (SCOPE-29/31).
- **PLAT-01..07 platform expansion and Stage-1+ curriculum work** — blocked by the v2.0 `adjust` verdict and SCOPE-27; re-opens only on a go verdict after a valid evaluation.
- **The general verification-enforcement regime** — normative-statement index, full CI integration, waiver policy, thresholds X/M — owned by the concurrent charter workstream (SCOPE-32).
- **Carried-forward todos** (remain in `.planning/todos/pending/`, unlinked to v2.2 phases): `trainex-r1-research-handoff` (r1b tuning round), `d-06-static-epsilon-sensitivity-check` (spec-side sensitivity question).

## Out of Scope

| Exclusion | Reason |
|-----------|--------|
| Recipe tuning / hyperparameter adjustment against observed results | SCOPE-29 — conformance-only iteration protects the single look; tuning is v2.3 |
| Framework-spec file edits | SCOPE-30 — amendments accumulate in the VER-20 routing list for a later spec milestone |
| Stage-1+ work, PLAT-01..07 platform expansion | SCOPE-27 — Stage-0-only training authorization |
| Any held-out evaluation beyond the one authorized | SCOPE-28 — requires a new owner decision |
| The trainex-r2 report's tuning analysis as grounding | SCOPE-31 — it reasons about a recipe that did not run |
| Re-auditing the component math | The conformance audit's "verified clean" section is load-bearing — the divergences sit in assembly, wiring, and configuration seams |
| Re-running the v2.0 seed-42 checkpoint's evaluation | The v2.0 record and its receipt-based refusal path are protected (see the evaluation-policy clarification) |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CONF-01 | Phase 46 | Complete |
| CONF-02 | Phase 47 | Pending |
| CONF-03 | Phase 47 | Pending |
| CONF-04 | Phase 48 | Pending |
| CONF-05 | Phase 48 | Pending |
| CONF-06 | Phase 48 | Pending |
| CONF-07 | Phase 48 | Pending |
| INST-01 | Phase 46 | Complete |
| INST-02 | Phase 48 | Pending |
| INST-03 | Phase 49 | Pending |
| GATE-01 | Phase 49 | Pending |
| GATE-02 | Phase 49 | Pending |
| GATE-03 | Phase 49 | Pending |
| TEST-01 | Phase 48 | Pending |
| TEST-02 | Phase 48 | Pending |
| RUN-01 | Phase 50 | Pending |
| RUN-02 | Phase 50 | Pending |
| RUN-03 | Phase 51 | Pending |
| EVAL-01 | Phase 51 | Pending |
| DIAG-05 | Phase 52 | Pending |
| VER-19 | Phase 52 | Pending |
| VER-20 | Phase 52 | Pending |

**Coverage:** 22/22 mapped (Phase 46: CONF-01, INST-01 · Phase 47: CONF-02, CONF-03 · Phase 48: CONF-04..07, INST-02, TEST-01, TEST-02 · Phase 49: GATE-01..03, INST-03 · Phase 50: RUN-01, RUN-02 · Phase 51: RUN-03, EVAL-01 · Phase 52: DIAG-05, VER-19, VER-20). No orphans; no duplicates. SCOPE-27..32 are scope-boundary annotations, not numbered requirements (v2.0 SCOPE-16..21 precedent). CONF/INST/GATE/TEST/RUN/EVAL are new categories beginning at 01; DIAG continues from v2.1's DIAG-04; VER continues from v1.6's VER-18; SCOPE continues from v2.1's SCOPE-26.

---
*Requirements defined: 2026-07-25 via `/gsd-new-milestone`, transcribed from the owner-ratified v2.2 roadmap proposal.*
*Last updated: 2026-07-25 after initial definition*
