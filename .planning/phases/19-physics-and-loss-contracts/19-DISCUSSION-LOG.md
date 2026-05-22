# Phase 19: Physics and Loss Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `19-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-05-22
**Phase:** 19 - Physics and Loss Contracts
**Areas discussed:** Area 1 (B-02 / PHYS-01 D-formula EVID-05); Area 2 (B-09 / PHYS-03 softening EVID-05 + simulation_data check); Area 3 (M4 / PHYS-06 constraint-counting + Phase 16 ledger reclassification); Area 4 (PHYS-02 AD contract + PHYS-04 HNN-reframing + PHYS-05 ALM restructure + total-loss replacement); Area 5 (Process — plans, AC naming, CODE-DIVERGENCE, Issue Doc annotation, simulation_data role)
**Mode:** `gsd-discuss-phase 19 --all ultrathink` — default-mode interactive discussion with `--all` auto-select of all 5 areas

---

## Area 1: B-02 / PHYS-01 D-formula adjudication

### Q1: B-02 verdict framing

| Option | Description | Selected |
|--------|-------------|----------|
| 1. `accept-resolution` + explicit false-positive on issue doc | Resolution doc §3.1–3.2 dimensional-analysis proof forces D=(GT²)^(1/3) under raw-mass framework. Issue doc's 6.694 valid only under a mass-fraction framework rewrite the issue doc did not also propose. EVID-05 §9: resolution correct on dimensional grounds; issue doc correct only conditionally on an undeclared framework switch. | ✓ |
| 2. `accept-resolution` + neutral note on issue doc | Same verdict with non-judgmental language: "both proposals are internally consistent for their respective frameworks; we adopt raw masses." Avoids calling the issue doc wrong; downside is leaving the door open for future re-litigation. | |
| 3. `accept-third-position` with explicit raw-mass framework lock | Add a "Governing Mathematical Convention" subsection per resolution §3.1 that names raw-mass as locked, then derives D=(GT²)^(1/3) as a consequence. Stronger framework commitment but extra spec text. | |

**User's choice:** Option 1 (rejected the multiple-choice frame; provided a richer answer that combines Option 1's verdict with Option 3's explicit-framework-lock posture in the spec edit, plus established a new milestone-wide governance convention).

**Notes:**

> Verdict: accept-resolution. Resolution doc §3.1–3.2 provides a complete dimensional-analysis proof. Issue doc's B-02 claim that D should be 6.694 is only valid under a mass-fraction convention requiring rewriting every residual, Hamiltonian, COM, and invariant formula. The framework uses raw masses everywhere, so D=(GT²)^(1/3) is mathematically forced. Issue doc B-02 was wrong to frame this as a formula error — it was proposing an unstated convention change without accounting for downstream consistency.

> Governance context (NEW milestone-wide convention):
> - Resolution doc is the designated default verdict source per directive 2026-05-18: "adopted as the default verdict source — the agent transcribes its positions into framework-spec edits unless EVID-05 surfaces concrete evidence that the position fails."
> - Issue Docs (all of them under pinn_instruction/issues/) exist ONLY to identify issues. They are NOT source of truth for solutions. They are a historical record of what was found during audit. Do NOT rewrite or revise Issue Doc content.
> - For B-02 specifically: append a single-line adjudication annotation to the Issue Doc's B-02 table row. Format: `**Adjudicated Phase 19:** \`accept-resolution\`. See \`evidence/B-02.md\`.` Original row text stays intact.

---

## Area 2: B-09 / PHYS-03 softening adjudication

### Q1: B-09 verdict framing + softening functional form

(Prefaced by a `simulation_data/` inspection finding: `simulation_data/` uses NO force-softening anywhere — its `epsilon = 0.05` is an IC minimum-separation rejection threshold; Brutus is arbitrary-precision; metrics use unsoftened separations. PHYS-03's "simulation_data epsilon usage" clause refers to a quantity that does not exist as force softening.)

(Also surfaced during preparation: current spec uses additive softening `1/(||r||+ε)`; resolution doc §10.7 prescribes Plummer-sqrt `1/sqrt(||r||²+ε²)`.)

| Option | Description | Selected |
|--------|-------------|----------|
| 1. `accept-resolution` + change to Plummer-sqrt | Verdict accept-resolution. Lock ε_train=1e-5 (matched training pair), ε_inv=1e-10 (static invariants). Change form additive → Plummer per resolution §10.7 in both residual AND energy regularizer. Anti-pattern warning: "Do not mix `(||r||+ε)⁻³` with `(||r||+ε)⁻¹` or with the Plummer form; chosen pair MUST appear identically in residual and Hamiltonian." | ✓ |
| 2. `accept-resolution` + keep current additive form | Same numeric strategy; deviate from resolution §10.7 to keep additive form. Requires positive evidence to defend. | |
| 3. `accept-third-position` | Compose both: matched pair within training (resolution framing) + dual-context separation (issue doc framing) as orthogonal. Change to Plummer. Slightly stronger positive framing of issue doc. | |

**User's choice:** Option 1, with refinements.

**Notes:**

> B-09 / PHYS-03 = accept-resolution.
> Sub-decision 1: Issue doc's "5 orders of magnitude mismatch" framing is not the final defect. simulation_data has no force-softening epsilon to match; its epsilon=0.05 is an IC minimum-separation rejection threshold. Keep the dual-context split: ε_train = 1e-5, ε_inv = 1e-10, s_min unsoftened.
> Sub-decision 2: Change specs from additive 1/(||r||+ε) to matched Plummer 1/sqrt(||r||²+ε²) everywhere the softened training Hamiltonian/residual is defined. Residual and Hamiltonian use the same r_safe; do not mix additive and Plummer; do not mix unmatched (||r||+eps)^-3 force with (||r||+eps)^-1 potential.
> Evidence §9 (Which Source Was Correct/Wrong): credit issue doc as partly correct on separating static-invariant ε from training-time softening, but wrong/overstated on mismatch framing and incomplete on functional form. Resolution doc correct on final contract.

### Q2: Static-invariant V form (additive vs Plummer-sqrt)

Surfaced because Q1's wording "everywhere the softened training Hamiltonian/residual is defined" left ambiguous whether the offline static `V` in `ctl_instruction.md` Step 3 also changes form.

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Change to Plummer-sqrt (matches resolution §7.2) | Apply form change to static V too. One softening shape across the framework; Plummer everywhere with ε differing by context (ε_inv=1e-10 static, ε_train=1e-5 training). Matches resolution §7.2 verbatim. No functional difference at ε_inv=1e-10. | ✓ |
| 2. Keep additive in static V; Plummer only in training | Deliberate two-form spec: static V additive, training Plummer. Minimizes spec churn. Internally consistent (user's matched-pair rule applies within a context). | |
| 3. Defer to plan-phase / executor | Treat as planner discretion. Risk: re-litigation during execution. | |

**User's choice:** Option 1.

**Notes:**

> Static-invariant V should also change from additive to Plummer-sqrt. Record under the same `accept-resolution` verdict, NOT `accept-third-position`. Resolution §7.2 explicitly specifies V_{ε_inv} = -Σ m_i m_j / sqrt(||r_i' - r_j'||² + ε_inv²) with ε_inv=1e-10, while training uses the same Plummer shape with ε_train=1e-5. Locked convention: one softening functional form across the framework, Plummer everywhere; ε value differs by context; s_min unsoftened.

> Practical-note correction: additive vs Plummer at ε_inv=1e-10, r≥0.05 is negligible but NOT ~1e-20 between the two forms. Additive has first-order relative bias ~ε/r = 2e-9 at r=0.05; Plummer's bias from Newtonian is ~ε²/(2r²) = 2e-18. Does not affect verdict; math should be recorded accurately.

### Q3: "More questions or next area?" check

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Move to M4 / PHYS-06 | Keep EVID-05 clustered. | ✓ |
| 2. More questions on B-09 | Reopen if sub-decision missed. | |
| 3. Skip to Process (Area 5) | Lock plans/scaffold first. | |

**User's choice:** Option 1.

**Notes:**

> One note for the planner punchlist: treat cited line numbers as anchors, not the full edit set. The executor should `rg` for all old additive forms and old symbols (`epsilon_soft`, bare `varepsilon`, `(||r|| + eps)`) and update related prose/listings too, including numerical notes and anti-pattern wording. Adopting `epsilon_train` / `epsilon_inv` is fine as mechanical cleanup because it matches the resolution-doc convention and reduces ambiguity.

> Do not mark B-09 VERIFIED until AC-PHYS-03 is actually applied/passed; for now it is discussion-locked / ready for planning. Identify any real source gap if encountered.

---

## Area 3: M4 / PHYS-06 constraint-counting replacement + Phase 16 ledger reclassification

### Q1: M4 verdict + Phase 16 ledger `Sources Disagree?` correction

(Prefaced by surfacing a Phase 16 ledger inconsistency: ledger M4 row shows `Sources Disagree? = NO` but REQUIREMENTS.md PHYS-06 says "EVID-05 adjudication of M4" required, and actual source positions disagree — issue doc keeps the counting framing with arithmetic correction; resolution doc rejects counting altogether. Per CRITICAL GOVERNANCE STOP protocol, surfaced as a process-artifact gap.)

| Option | Description | Selected |
|--------|-------------|----------|
| 1. `accept-resolution` + amend Phase 16 ledger row + full EVID-05 packet | Verdict accept-resolution. Replace ctl_instruction.md:914-915 with resolution §10.4 reconstructive-gauge-fixed-encoding prose. Amend Phase 16 ledger M4 row: `Sources Disagree? NO → YES — EVID-05 required` with audit note. Issue Doc M4 row gets standard annotation per the new convention. EVID-05 packet evidence/M4.md carries full §5/§7/§8/§9. | ✓ |
| 2. `accept-resolution` + keep ledger NO + lightweight packet | Same verdict and spec edit; don't amend ledger; skip EVID-05 sections. Lowest churn; downside: ledger contradicts PHYS-06 requirement language. | |
| 3. `accept-third-position` | Hybrid: reconstructive-encoding framing primary, but include corroborating dimension-accounting check (18-DOF - 3 COM - 3 P - 3 SO(3) = 9 reduced DOF). Amend ledger. Gives issue doc partial credit on math while keeping resolution framing dominant. | |

**User's choice:** Option 1.

**Notes:**

> M4 / PHYS-06 verdict = accept-resolution. Use the resolution doc framing as the spec replacement: IC13 is a redundant but reconstructive fixed-gauge initial-state encoding, not a constraint-counting proof. The issue doc gets correctness credit for the arithmetic correction (18 − 3 COM − 3 P − 3 SO(3) = 9), but that belongs in the EVID-05 packet's dimension-accounting / correctness-assignment sections, not in the replacement spec prose.

> Also amend the Phase 16 ledger M4 row from `Sources Disagree? = NO` to `YES — EVID-05 required`, with an audit note that Phase 19 reclassified it because PHYS-06 explicitly requires EVID-05 and the source positions actually disagree. This is a factual ledger correction after surfacing the discrepancy, not a new schema invention.

> Do not use accept-third-position: the final contract is explicitly the resolution doc's position. Mark M4 discussion-locked / ready for planning, but not verified until AC-PHYS-06 is actually applied and passed.

---

## Area 4: PHYS-02 AD chain-rule + PHYS-04 HNN→regularizer + PHYS-05 ALM restructure + total-loss replacement

### Q1: PHYS-02 AD contract placement and worked synthetic-trajectory test format

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Primary in pinn_architecture.md; ctl side cross-ref only; math + Python listing | Most natural home is pinn_architecture.md (Phase 17 forward-referenced §5.x area). Carries: three-layer separation + chain-rule factors (math); anti-pattern warning naming forbidden `torch.autograd.grad(r.sum(), u, ...)` + acceptable patterns (jacrev+vmap / explicit loop); worked synthetic-trajectory test as math + short Python listing. ctl_instruction.md:962 retargets to cross-reference. Single source of truth. | ✓ |
| 2. Split — ctl carries math contract; pinn carries code test | Two-file split; cleaner what/how separation; cost of two cross-references to keep in sync. | |
| 3. Math-only in both files; no Python listing | Avoid Python listing entirely; cleanest separation from code; downside: anti-pattern easier to misread without code form. | |

**User's choice:** Option 1.

**Notes:**

> PHYS-02 canonical content lives in pinn_architecture.md; ctl_instruction.md should carry only a cross-reference. Use math + a short Python listing because the requirement asks for a worked synthetic-trajectory test, and the resolution/issue docs already discuss concrete PyTorch AD anti-patterns. Keep the listing illustrative/spec-level, not a FUT-01 implementation harness.

> Guardrails:
> - Canonical leaf is u=t/T. If differentiating w.r.t. u, velocities/accelerations are direct componentwise dr'/du and d²r'/du². The 2x/4x chain factors apply ONLY to a code path differentiating directly w.r.t. tau=2u-1.
> - Use the PHYS-02 requirement's synthetic trajectory exactly: r'(u) = [sin(2πu), cos(2πu), u²]. Do not substitute the resolution doc's simpler tau³ smoke test. Exact executable tolerance belongs to Phase 21 VER-04 / AC-PHYS-02, not this prose spec unless already locked elsewhere.

> Single source of truth in pinn_architecture.md avoids duplicate math drifting between files.

### Q2: PHYS-04 + PHYS-05 + total-loss rewrite scope

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Full replacement per resolution §10.6-10.8 + §8.3-8.8 | B-07 = accept-resolution; B-08 = accept-resolution. Wholesale replace pinn_architecture.md §3.2-3.3 + §4.1 (and ctl_instruction.md total-loss block) with resolution-doc contract. Add L_IC (§8.3) and L_L (§8.6). L_phys uses causal weighting (§8.4) with stopgrad. L_E framed as soft conservation regularizer using matched-Plummer H_ε (NOT HNN). Remove ALL pseudo-ALM from default; add P2-ablation appendix. HNN-flavored prose rewritten throughout. | ✓ |
| 2. Targeted patches per §10.6-10.8 only; keep surrounding prose | Same verdicts; only patch specific formulas and section titles; leave wider HNN framing intact with annotation. Lower-churn; leaves contradictory framing visible in same file. | |
| 3. Phased rewrite — P02 formulas, P03 prose cleanup | Same verdicts and final state; split rewrite across two plans for review safety. Adds one plan vs Phase 17/18's 3-plan precedent. | (accepted as plan-structuring decomposition) |

**User's choice:** Option 1 (with Option 3 accepted as the plan-decomposition structure — see Area 5).

**Notes:**

> B-07 / PHYS-04 = accept-resolution. B-08 / PHYS-05 = accept-resolution. Full resolution-doc replacement, not formula-only patch. Current HNN and pseudo-ALM claims are spread through title/intro, §3 loss overview, ALM implementation block, HNN energy section, §4.1, summary table, and ctl_instruction.md total-loss block. Leaving any of that as active prose would contradict PHYS-04/05.

> Default contract: L_total = L_data + λ_IC L_IC + λ_phys L_phys_causal + λ_E L_E + λ_L L_L.

> Guardrails:
> - L_E is a soft conservation regularizer using the analytic matched-Plummer Hamiltonian. It is not an HNN, because the model predicts positions; it does not parameterize a Hamiltonian.
> - L_IC is mandatory and anchors both position and velocity at u=0.
> - L_phys uses causal weights with stopgrad by default.
> - L_L is componentwise Huber on relative angular-momentum drift; ε_L=1e-8 is only a numerical-stability scale, not force softening.
> - Remove pseudo-ALM from default training. Optional ALM is P2 only, scalar conservation constraints only (c_E and c_{L,α}), never dense ODE residual, never dual updates during L-BFGS, updates only between Adam epochs or deterministic refinement passes.
> - Replace the old λ_E-only schedule with the resolution §8.7 λ_phys/λ_E/λ_L warmup schedule where the loss schedule is discussed.

> Option 3 is acceptable only as an execution-plan decomposition. The accepted contract is still Option 1, and AC-PHYS-04/05 should not be marked passed until the final coherent rewrite is in place across both pinn_architecture.md and ctl_instruction.md.

> One nuance: keep "Hamiltonian" where it means the analytic energy function H_ε; remove "HNN-style" and any claim that the architecture is an HNN.

### Q3: "More questions or next area?" check

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Move to Process (Area 5) | All substantive PHYS verdicts locked. Remaining = process scaffolding. | ✓ |
| 2. More questions on Area 4 | Reopen if sub-decision missed. | |
| 3. Move to write_context now and defer process | Skip Area 5; planner handles. Risk: planner re-litigates locked-elsewhere decisions. | |

**User's choice:** Option 1.

---

## Area 5: Process — plans, AC naming, CODE-DIVERGENCE, Issue Doc annotation scope, simulation_data role

### Q1: Plan decomposition

| Option | Description | Selected |
|--------|-------------|----------|
| 1. 4 plans — split pinn_architecture.md rewrite | P01 (Wave 1, parallel with P02): ctl_instruction.md edits + EVID-05 ctl-side adjudications. P02 (Wave 1, parallel): pinn_architecture.md formula/contract changes. P03 (Wave 2, blocked on P02): pinn_architecture.md prose cleanup + cross-references. P04 (Wave 3, blocked on Waves 1-2): 19-CODE-DIVERGENCE.md + evidence packets + ledger transitions + Issue Doc annotations + Phase 16 M4-row amendment + AC-PHYS-02 reservation. | ✓ |
| 2. 3 plans — mirror Phase 17/18 | P01 ctl; P02 pinn (one big plan); P03 evidence + cleanup. Matches precedent; risk: P02 is the largest single plan in v1.4 so far. | |
| 3. Defer plan count to planner | Let gsd-plan-phase decide. Lowest user input now; risk planner makes different review-safety call. | |

**User's choice:** Option 1.

**Notes:**

> Proceed with Option 1: use the 4-plan decomposition. Treat this as review-safety process decomposition, not a semantic physics decision. Keep P02 focused on pinn_architecture.md formula/contract changes, and P03 blocked on P02 for HNN/prose cleanup and cross-reference validation.

> Approve reserving AC-PHYS-02 only as AC naming continuity, mirroring Phase 17 GAP-17-02; do not invent pass criteria beyond Phase 21 VER-01. Apply Issue Doc annotations forward for all Phase 19 findings, including `Not contested` markers for B-07/B-08, but do not retroactively backfill Phase 17/18 unless separately instructed. For B-09 evidence §5, use the structured simulation_data verification subsection, citing inspected files and implications, without treating simulation_data as grounding for new v1.4 spec decisions.

> If any semantic, schema, or cross-phase reframing choice is not directly grounded in locked Phase 16/17/18 precedent or cited source material, stop and surface it as a gap.

### Q2: "Ready for context or explore more?" check

| Option | Description | Selected |
|--------|-------------|----------|
| 1. I'm ready for context | Write 19-CONTEXT.md and proceed. | ✓ |
| 2. Explore more gray areas | Reopen for warmup-schedule λ values, HNN terminology specifics, M4 prose wording, ALM appendix placement, ε_L symbolic vs numeric. | |
| 3. Surface a remaining structural concern first | Flag cross-phase coupling (Phase 20.5 sampling_method.md — no overlap; Phase 20 ARCH — no overlap; Phase 21 VER-04 — AC-PHYS handoff). | |

**User's choice:** Option 1.

---

## Claude's Discretion

The user explicitly designated these as Claude's-discretion territory during the discussion:

- Exact section-break placement of the new "Governing Mathematical Convention" anchor in `ctl_instruction.md` Step 2.5 (per resolution §10.1).
- Exact wording of the M4 replacement prose's Phase 17/18 cross-reference clause (D-11) — must be unambiguous about which downstream phase locks the referenced concept; specific phrasing flexible.
- Markdown formatting choice for the Plummer formula presentation in `pinn_architecture.md` §3.2-3.3 (math display vs inline; current spec uses display blocks — keep).
- Whether the worked synthetic-trajectory Python listing uses `torch.func.jacrev + vmap` or an explicit per-component loop (D-08); either is acceptable, planner picks the cleaner diff against current spec style.
- Exact placement of the "Optional ALM ablation (P2)" appendix within `pinn_architecture.md` §4 (after the default-contract sections; planner finalizes).
- Evidence-packet section ordering within the Phase 16 `_TEMPLATE.md` 12-section schema (Phase 17/18 precedent: follow template ordering).
- Whether `evidence/B-07.md` / `evidence/B-08.md` use a Markdown table or list for source-position quotes (both findings are non-EVID-05, so §5/§7/§8/§9 carry `Not contested` markers either way).
- Adopting `epsilon_train` / `epsilon_inv` symbol naming as mechanical cleanup (user noted: "fine as mechanical cleanup because it matches the resolution-doc convention and reduces ambiguity").
- `r_safe` notation reuse where the Plummer denominator formula recurs.

---

## Deferred Ideas

Items raised during discussion and explicitly deferred per the user's instruction (or by Phase 17/18 precedent):

- **Phase 17 / Phase 18 Issue Doc retroactive back-fill** with the D-14 adjudication-annotation convention — surfaced as a follow-on question (B-03/B-04/B-06/M1/M2 for Phase 17; B-05/M3 for Phase 18). User instruction (D-15): "do not retroactively backfill Phase 17/18 unless separately instructed." Held for future authorization.
- **Numeric AC-PHYS-NN pass criteria + executable probes** — Phase 21 VER-01 / VER-04 scope per Phase 16 D-13. Phase 19 reserves AC names only.
- **SCOPE-05 formalization in `REQUIREMENTS.md`** — Phase 20.5's job. Phase 19 relies on Phase 18 D-10 + the D-17 user-directive distinction directly.
- **`pinn/` code rebuild** — FUT-01. Phase 19 records divergence in `19-CODE-DIVERGENCE.md` only.
- **SI-PINN-001 / SI-CTL-001 retirement** — Phase 21 VER-06.
- **Causal-weighting alternative weighting contracts** — PHYS-05's "or otherwise justified" wording leaves room; Phase 19 locks causal-with-stopgrad as default.
- **L_phys hyperparameter ablations** (η_c, lookahead fraction, replay fraction beyond defaults) — Phase 21 disposable probes or post-v1.4 training-tuning.
- **`pinn/STATUS.md` archival marker** — Phase 21 handoff per Phase 17 D-15.

No scope-creep ideas surfaced during this discussion; user redirected the one back-fill question explicitly to deferred.
