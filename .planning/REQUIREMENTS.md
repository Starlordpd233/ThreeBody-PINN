# Requirements: v2.2 Stage-0 Conformance Repair & Valid Re-Run

**Defined:** 2026-07-25
**Core value:** A *valid* test of the Stage-0 design — repair the verified conformance divergences, prove the repair with gate-aligned instrumentation and a preflight gate, re-run Stage-0 under the corrected recipe, and spend the one authorized held-out evaluation on a run that is actually the specified experiment — never tuning the recipe against observed results.
**Total:** 24 requirements (9 CONF + 3 INST + 3 GATE + 2 TEST + 3 RUN + 1 EVAL + 1 DIAG + 2 VER) + scope boundaries SCOPE-27..32.

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

- [x] **CONF-01**: Resolve RG-02: settle whether training targets are raw positions or `r' = r/D`, via the train-free residual-on-stored-targets check. No training run. **Branch point:** if the target frame *is* wrong, that is a sixth divergence and a data-path defect rather than a loss-math one — surface as an owner scope decision, never absorbed silently. [RG-02; proposal Phase 46] *(The 2026-07-27 real-corpus run returned `VERDICT_AMBIGUOUS`; the branch point fired and produced CONF-08. **Closed 2026-07-28 by owner ruling on GAP-46-06 option B, NOT by a clean machine verdict.** The post-repair re-probe returned rule-5 `VERDICT_NON_FRAME_DIVERGENCE`: rule 4 was unreachable by construction once CONF-08 landed, because it requires byte-identity against the parsed file-order array that the authorized repair deliberately removed. The owner exercised the D-09 branch on the recorded arm evidence — scaled arm median 0.9894 with 1605/1651 separated versus raw arm 0.0802249 against controls at 0.0802262, a factor of 12.3 — and ratified the operational raw/native frame `("r_raw", "t_native", "ordered_raw")`. **Anywhere CONF-01 is cited as satisfying EVAL-01 precondition (ii), this qualification MUST travel with it: RG-02 is settled by owner instruction on measured evidence, not by a `VERDICT_TARGETS_ARE_RAW` token.** See GAP-46-06.)*
- [x] **CONF-02**: Build the `S_H` pipeline: `S_H = median_train(K0 + Uabs0)` over the admitted set, persisted in training metadata. `S_H` must be finite and strictly positive; non-finite or `≤ 0` is a preprocessing/metadata validation failure that fails closed (spec §3.4). [spec §3.4; conformance audit]
- [x] **CONF-03**: Wire `ε_H = 1e-4 · S_H` into the loss assembly and remove the `+1e-12` additive fallback floor, which §3.4 explicitly prohibits. [spec §3.4]
- [x] **CONF-04**: Correct `R̄` to the locked `(1/3) Σ_i ‖f_i‖²` (from the implemented `(1/9)Σ`). [locked loss contract; conformance audit]
- [x] **CONF-05**: Implement a causal-exponent clip satisfying invariant A (no causal weight may be exactly zero), **chosen against the corrected `R̄`** — which is 3× larger and underflows sooner. Record the chosen bound in the plan and the run record. [GAP-45-04 owner ruling: invariant mandated, number deferred to the implementer with a recording obligation]
- [x] **CONF-06**: Revert `λ_E^max` to the locked Stage-0 value `0`. [GAP-45-02 owner ruling: λ_E provenance unrecoverable, treated as drift]
- [x] **CONF-07**: Implement the `L_data` component reduction per the owner ruling on GAP-45-01. [GAP-45-01: deferred with a pre-re-run condition; blocking owner checkpoint at Phase 48, presented with computed term magnitudes from the retained runs]
- [x] **CONF-08**: Repair the sixth (data-path) divergence and re-verify CONF-01. The resident trajectory surface pairs `pre.masses_ordered` (`pinn/data/adapter.py:865`) with the un-permuted, un-gauged `parsed_brutus.positions` (`:863`), so mass index *i* does not address body *i* — measured at 1651/1651 trajectories, permutation `(2,0,1)`×1547 and `(0,2,1)`×104, identity never. Repair covers **exactly** the two measured transforms: apply `pre.permutation` (`pinn/data/preprocessing.py:188-189`) and the COM-recentre/boost gauge (`:186`) to the resident position and velocity series. The `D` scaling is **excluded** — it is the raw-vs-scaled question CONF-01 exists to answer, and pre-applying it would decide the verdict by construction. Rotation gauge (`:195`) enters only if the re-probe measures it as the new `first_diverging_step`. Then re-run the CONF-01 probe unchanged over the same GAP-46-02 1,651-trajectory population and record the verdict. [GAP-46-04 + GAP-46-05 owner rulings 2026-07-27; conformance audit sixth divergence] *(Complete 2026-07-28 via plans 46-08 and 46-09. The repair is exact: `stepwise_attribution.plus_permutation = 0.0` for 1651/1651 trajectories, so resident positions and `masses_ordered` address the same canonical bodies. `D` scaling and the rotation gauge were not applied, as specified. The unchanged probe was re-run once over the same 1,651-trajectory population and its verdict recorded in `46-VERDICT-POSTREPAIR.md`.)*

- [x] **CONF-09**: Complete the residency transform to the locked canonical contract. Move the resident position and velocity series (`pinn/data/adapter.py:864-865`) from `pre.r_com_ordered` / `pre.v_com_ordered` to `pre.r_gauge` / `pre.v_gauge` — the rotation-gauged, `D`/`V`-scaled output `preprocess_trajectory` already computes and currently exports only to the probe. Re-ratify `RATIFIED_VALIDATION_FRAME` to `(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED, MASS_CONVENTION_ORDERED_RAW)` in the same change, as `pinn/training/validation_gate.py:526-528` requires, and correct in that same change any test encoding the current resident pairing. **Sequenced ahead of CONF-02** — `S_H` is frame-dependent (`H' = D·H`), so building it first means rebuilding it. [GAP-46-07 owner ruling 2026-07-28, option A] *(Repairs three defects in one move, because every anchor target derives from the residents. **Scale:** the training path pairs raw residents with `u = t/T`, a pairing `COHERENT_FRAME_PAIRS` does not admit, so `residual = (T²−1)·a(r)` on a perfect trajectory — `L_phys` has no zero and is minimized at zero gravity. **Velocity:** autograd returns `d/du` while the resident series is `dr/dt`, so `K_model = T²·K_raw` against `U_model = U_raw` — unit-inconsistent, absorbable by no single constant. **Rotation:** `IC₁₃` is built from `r0_gauge`/`v0_gauge` and is exactly rotation-gauge-invariant while the targets are equivariant, so the regression target is not a function of the network input. Under the swap, `dr'/du = (T/D)·v_rot = v_gauge` exactly, `h0` and `l0` become the scaled-frame invariants their loss terms expect, and `IC₁₃` already lives in this frame. Two further conformance gains: `HUBER_DELTA_DATA = 1.0` is locked for scaled positions (`loss_catalog.py:174-183`) and `EPS_SOFT = 1e-5` is a scaled-frame softening per `softened_acceleration`'s input contract — both currently applied to raw positions. Gate metrics are unchanged in value: `ε_H` is a relative drift, invariant under uniform `H → D·H`. **Not** a CONF-01 pre-emption: CONF-08 excluded the `D` scaling so the measurement could be made, it was made, and this applies its answer. **Not** recipe tuning under SCOPE-29: magnitudes move because the frame becomes the locked one, not because a hyperparameter was fitted to an observed result. Evidence and derivations: `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`.)*

### Instrumentation (INST) — Phases 46, 48, 49

- [x] **INST-01**: Gate-aligned validation metrics: per-trajectory `ε_H`/`SCS` on the validation split, via the existing `pinn.verification.gate_metrics` functions. Currently validation records only `final_val_loss`, `step`, `trend` — no conservation signal at all. [conformance audit; EVAL-01 precondition (iii)] *(Frame-independent components shipped in plans 46-03/46-05; the production wiring landed 2026-07-28 in Plan 46-07. Verified end-to-end on a real run, not inferred: each validation event publishes a sidecar carrying 240 per-trajectory `{record_key, eps_h, scs}` rows plus the ratified frame block, the eight `gate_*` keys merge into `validation.jsonl`, and `summary.json` projects them alongside `eval01_precondition_iii`. `gate_status` and `gate_verdict` remain distinct states, so instrumentation failure never renders as a metric PASS.)*
- [x] **INST-02**: Log per-term gradient statistics — the precondition the locked Phase-35 contract names for any reweighting decision, never satisfied. [Phase-35 loss/energy-weight contract]
- [ ] **INST-03**: Maintain the known-divergence register; the run record surfaces every open divergence so a run carries its own caveats. [conformance audit]

### Minimum Enforcement (GATE) — Phase 49

- [ ] **GATE-01**: Preflight asserts the **full** PHYS-05 per-stage table at run start and at every stage boundary (per GAP-45-03), not merely the `≤1` cap. [GAP-45-03 owner ruling: per-stage PHYS-05 values are locked]
- [ ] **GATE-02**: Preflight placeholder census: every spec-required quantity the loss consumes resolves to a real pipeline value, or is explicitly owner-waived for that run. This is the check that would have caught the `S_H` gap. [conformance audit]
- [ ] **GATE-03**: Runtime invariants: no causal weight exactly zero (invariant A); the causal front advances within N steps (invariant B — N is an owner checkpoint). Fail loud, fail early. [GAP-45-04; N owner checkpoint at Phase 49]

### Test-Suite Correction (TEST) — Phase 48

- [x] **TEST-01**: Correct the two tests that currently defend divergences (C-08), in the same change as the code fix, or CI fails the fix. [conformance audit C-08]
- [x] **TEST-02**: Add assembly-boundary conformance tests: given known inputs, assert the value the loss *actually receives* equals the spec value — for `R̄` and `ε_H` at minimum. The existing tests cover the components, which are already correct. [conformance audit]

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
| CONF-02 | Phase 47 | Complete |
| CONF-03 | Phase 47 | Complete |
| CONF-04 | Phase 48 | Complete |
| CONF-05 | Phase 48 | Complete |
| CONF-06 | Phase 48 | Complete |
| CONF-07 | Phase 48 | Complete |
| CONF-08 | Phase 46 | Complete |
| CONF-09 | Phase 47 | Complete |
| INST-01 | Phase 46 | Complete |
| INST-02 | Phase 48 | Complete |
| INST-03 | Phase 49 | Gaps Found |
| GATE-01 | Phase 49 | Gaps Found |
| GATE-02 | Phase 49 | Gaps Found |
| GATE-03 | Phase 49 | Gaps Found |
| TEST-01 | Phase 48 | Complete |
| TEST-02 | Phase 48 | Complete |
| RUN-01 | Phase 50 | Pending |
| RUN-02 | Phase 50 | Pending |
| RUN-03 | Phase 51 | Pending |
| EVAL-01 | Phase 51 | Pending |
| DIAG-05 | Phase 52 | Pending |
| VER-19 | Phase 52 | Pending |
| VER-20 | Phase 52 | Pending |

**Coverage:** 24/24 mapped (Phase 46: CONF-01, CONF-08, INST-01 · Phase 47: CONF-09, CONF-02, CONF-03 — in that order · Phase 48: CONF-04..07, INST-02, TEST-01, TEST-02 · Phase 49: GATE-01..03, INST-03 · Phase 50: RUN-01, RUN-02 · Phase 51: RUN-03, EVAL-01 · Phase 52: DIAG-05, VER-19, VER-20). No orphans; no duplicates. SCOPE-27..32 are scope-boundary annotations, not numbered requirements (v2.0 SCOPE-16..21 precedent). CONF/INST/GATE/TEST/RUN/EVAL are new categories beginning at 01; DIAG continues from v2.1's DIAG-04; VER continues from v1.6's VER-18; SCOPE continues from v2.1's SCOPE-26.

**Amendment 2026-07-27 (GAP-46-05, owner instruction).** CONF-08 was added to Phase 46 and the milestone moved 22 → 23 requirements after the CONF-01 branch point fired: the real-corpus probe returned `VERDICT_AMBIGUOUS` on a 100%-prevalent mass↔position permutation and COM/boost gauge divergence. GAP-46-04 first routed that repair to Phases 47/48; because Phase 47 is gated on Phase 46 (`ROADMAP.md:103`) while Plan 46-07 was gated on the repair, the routing deadlocked the milestone at its first phase. GAP-46-05 moves the **minimum** repair and its re-probe into Phase 46 as CONF-08. In the same amendment, CONF-01 and INST-01 reverted from Complete to Pending: CONF-01 mandates "Resolve RG-02" and RG-02 is measurably unresolved (this sits directly under EVAL-01 precondition (ii)), and INST-01's production wiring is the unexecuted Plan 46-07. VER-19 is re-verified against 23/23 at Phase 52 close, not carried forward from the roadmap-creation check.

**Amendment 2026-07-28 (GAP-46-06, owner instruction).** Phase 46's three requirements — CONF-01, CONF-08, INST-01 — moved to Complete, re-derived as 3/23 Complete and 20/23 Pending rather than carried forward. CONF-08 closed on plans 46-08/46-09; INST-01 closed on plan 46-07 and was verified by inspecting a real run's artifacts, not by a passing plan. CONF-01 closed by owner ruling on GAP-46-06 option B: the post-repair probe returned rule-5 `VERDICT_NON_FRAME_DIVERGENCE` because CONF-08's authorized repair made rule 4's byte-identity condition unreachable, so no clean token was obtainable; the owner exercised the D-09 branch on the measured arm evidence and ratified `("r_raw", "t_native", "ordered_raw")`. **The CONF-01 bullet carries a mandatory qualification that must travel with any citation of it under EVAL-01 precondition (ii).** Phase 51 must read that qualification before treating precondition (ii) as satisfied — a `Complete` checkbox is not the evidence.

**Amendment 2026-07-28 (GAP-46-07, owner instruction).** **CONF-09** added to Phase 47, sequenced **ahead of CONF-02**; the milestone moves 23 → 24 requirements and coverage is re-derived as 24/24 rather than carried forward. An independent verification of the six-claim conformance handoff (report under `docs/work/reviews/cross_cutting/stage0-conformance-audit/`) confirmed all six divergences and surfaced a seventh, unrouted one: CONF-08 excluded the rotation gauge and the `D`/`V` scaling by design, and GAP-46-06 then ratified the resulting intermediate as the **validation** observation frame — neither ruling reached the **training** path, which pairs unrotated, unscaled residents with `u = t/T`. Coverage read `23/23 mapped` with no orphans throughout, which is precisely why a *missing* requirement was invisible to it; the scale half was already measured in committed CONF-01 evidence (the `scaled_hypothesis` arm **is** the training frame, median 0.98936 over 1,651 trajectories against the probe's own analytic `(T²−1)/T² ≈ 0.99`) and had simply never been inferred. **Supersedes in part** GAP-46-06's ratified `("r_raw", "t_native", "ordered_raw")` frame, whose own constant declares this staleness condition; **CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged.** Separately measured and recorded so it is not mis-assumed later: the frame error is **not** the cause of the observed causal-front collapse — at step 1 the model is at initialization, so `R̄₀ = 5.32e+09` is identical under any target-frame repair, and the cause is the absent CONF-05 clip — but it does impose an asymptotic `R̄` floor of median `8.36e+05`, `1122×` above underflow on 25/25 real trajectories, so the front could never advance at convergence either. **CONF-05's bound is therefore chosen after both CONF-04 and CONF-09**; a clip applied to an unrepaired frame yields a run that looks healthy and is just as invalid.

---
*Requirements defined: 2026-07-25 via `/gsd-new-milestone`, transcribed from the owner-ratified v2.2 roadmap proposal.*
*Last updated: 2026-07-28 — CONF-09 added to Phase 47 per GAP-46-07 (owner option A); milestone 23 → 24 requirements.*
