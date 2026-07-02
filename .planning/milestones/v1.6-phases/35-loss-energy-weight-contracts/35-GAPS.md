# Phase 35 Gap Register

STOP-protocol gaps surfaced during Phase 35 (Loss & Energy-Weight Contracts).
Milestone index: `.planning/milestones/v1.6-GAPS.md`.

---

## GAP-35-01 - D-35-05 no-duplication reach over the pre-existing causal-weight formula in ctl_instruction.md

- **Decision point:** Does Phase 35's D-35-05 "zero duplicated normative body text" contract require de-duplicating the causal-weight formula `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))` (the LOSS-04 / GAP-32-01 Option-A baseline), which **already appears in both** `pinn_architecture.md` (component-math home) **and** `ctl_instruction.md` (a Phase-34 D-34-15 assembly statement)? Concretely: must plan 35-03 convert the `ctl_instruction.md` occurrence into a stable pointer to `pinn_architecture.md` (and 35-04 enforce a single-home check on it), or is the assembly-context occurrence exempt from D-35-05?
- **Where in artifact:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (~L1743, Phase-34 D-34-15 causal-weight assembly statement) vs `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (causal-weight component-math occurrences, ~L412/L638). Surfaced while selecting the A3 deterministic no-duplication sentinel for plan 35-04 and the LOSS-04 transcription/pointer in plan 35-03.
- **Task context:** Phase 35 `--reviews` replan (gsd-planner, Mode=reviews) — incorporating cross-AI finding M1 (claude-glm: "no automated no-duplication verifier — D-35-05 is unmet"). The planner surfaced this rather than free-handing an edit to Phase-34-locked content.
- **Classification:** **semantic** (with a **cross-phase** dimension) — whether a pre-existing Phase-34-verified formula body must be removed/converted touches both the *scope* of D-35-05 and *Phase-34-locked* assembly content (D-34-15).
- **Source silence:** `35-CONTEXT.md` D-35-05 requires "zero duplicated normative body text" and "a verifier that proves no duplication" but does **not** enumerate the pre-existing causal-weight occurrence or instruct editing the `ctl_instruction.md` line. `35-03-PLAN.md` Task 2 ("point to pinn for the causal weight formula") and Task 3 acceptance ("component formula bodies are not duplicated from pinn_architecture.md") *imply* the ctl occurrence should be a pointer, but **no source explicitly instructs deleting/converting** the existing ctl formula body. `v1.6-GAPS.md` GAP-32-01 (RESOLVED, Option A) ratifies the causal-weight baseline as LOSS-04 content but is silent on **where** it lives or on de-duplication. The ctl occurrence is Phase-34 D-34-15 assembly content; **no Phase 35 source authorizes editing Phase-34-locked assembly statements**.
- **Mathematical / engineering grounding:** The D-35-05 canonical-home split assigns component-math formula *bodies* to `pinn_architecture.md` and training/assembly *methodology* to `ctl_instruction.md`; a normative formula body duplicated across both homes is the precise spec-drift vector D-35-05 targets (the two copies can silently diverge under later edits). The causal-weight `w_n` body is a component-math object, so under a strict reading its only home is `pinn_architecture.md` and any `ctl_instruction.md` occurrence should be a pointer. But the ctl occurrence may be a legitimate **assembly-context citation** (showing how the weight enters the staged loss assembly), in which case a short formula reference is methodology, not a duplicated component body. The component-body-vs-assembly-citation distinction is a spec-engineering judgment with no first-principles answer, and resolving it by editing the ctl line mutates Phase-34-verified content — itself a STOP-gated action.
- **Agent was tempted to:** (gsd-planner) enforce a single-home check on the causal-weight formula and instruct 35-03 to convert the `ctl_instruction.md` occurrence to a pointer — which would have free-handed both a deletion of Phase-34-locked content and a semantic interpretation of D-35-05's reach. Instead the planner used the **energy-Huber `L_E` body** (already single-home in `pinn_architecture.md`; "tagged, not rewritten" by Phase 35) as the deterministic no-duplication sentinel, leaving the causal-weight case to 35-03's existing pointer actions + the manual no-duplication review.
- **What the user needs to decide:**
  - **A. Accept as-is (no further plan change).** The A3 energy-Huber sentinel + 35-03's existing pointer guidance + the manual no-duplication review govern the causal-weight case; the pre-existing `ctl_instruction.md` occurrence is left untouched by Phase 35. Plans are already in this state and are executable.
  - **B. De-duplicate.** Add an explicit 35-03 instruction to convert the `ctl_instruction.md` causal-weight formula body into a stable pointer to the `pinn_architecture.md` causal-weight section, and add a second deterministic single-home sentinel on the causal-weight body (`exp(-eta_c ...)`). Mechanically enforces D-35-05 for this formula but **edits Phase-34 (D-34-15) assembly content**.
  - **C. Exempt with carve-out.** Treat the `ctl_instruction.md` occurrence as legitimate assembly-context citation and explicitly EXEMPT it from D-35-05 in 35-03/35-04, documenting the carve-out (assembly-context references are not "duplicated normative bodies").
- **Confidence of impact:** **MEDIUM** — the plans are safe and executable under Option A (the deterministic verifier uses a grounded, single-home sentinel); the decision affects only whether Phase 35 additionally de-duplicates a pre-existing causal-weight occurrence and how strictly D-35-05 is mechanically enforced for that one formula. No data, scope, or safety exposure under any option.
- **Status:** **RESOLVED-WITH-INSTRUCTION**
- **Resolution note:** Resolved by **owner instruction on 2026-06-29** (this session, after reviewing the Option-B review findings below and a git-grounded re-evaluation). Adopted a **refined de-duplication** that realizes Option B's drift-elimination intent at Option A's cost: the `ctl_instruction.md` LOSS-04 callout now points to the `pinn_architecture.md` **Physics Residual Term** as the single canonical home and cites only the `w_1 = 1` / `eta_c = 1` parameters — the `w_n = exp(...)` formula body is no longer restated in the assembly file (LOSS-04 aligned to the existing LOSS-03 pointer pattern). The only remaining `ctl_instruction.md` occurrence was **Phase-35-authored** content (commit `83f82219`), **not** Phase-34-locked D-34-15 content, so no locked-content gate was traversed and no Option-C carve-out was created. A causal-weight single-home sentinel (`exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))` resolves to `pinn_architecture.md` only) was added beside the energy-Huber sentinel in the D-35-05 verification. This entry **supersedes** the earlier "owner-ratified Option A at the execution-readiness gate" note, which was not owner-grounded. See **Resolution reconciliation** below for why the Option-B recommendation was not adopted wholesale.


# Agent Analysis of Gap

Final Independent Evaluation: GAP-35-01

1. Verdict

Option B — full de-duplication — is the best resolution on the merits.

The ctl_instruction.md causal-weight callout should be converted to a pure pointer referencing pinn_architecture.md §3.2 as the single canonical home. The no-duplication verifier should be extended to cover the causal-weight formula body (in addition to the energy-Huber sentinel). The D-34-15 gate should be traversed with owner authorization — it exists to enable exactly this kind of justified, scoped, authorizable change.

If the process overhead of reopening a completed Phase 35 is judged disproportionate by the owner, Option A is an acceptable fallback — but only with the verifier extension applied immediately (not deferred). Option C is rejected outright.

2. Core Judgment: Is the ctl callout duplicated normative body?

Yes. The formula body w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m)) with w_1 = 1, eta_c = 1 is normative content — it defines a computation that downstream implementation must execute. It currently resides in two files. D-35-05 states "zero duplicated normative body text" — the word "zero" is not qualified by assembly context, attribution quality, phase provenance, or formula length.

The attribution line ("pinn_architecture.md remains the component-math home") is a social mitigation, not a structural prevention. D-35-05 anticipates and explicitly rejects this approach: "a bidirectional arrow alone does not stop drift." The attribution is a unidirectional arrow — weaker than what the rule already declares insufficient. The rule's designers understood that attribution decays; they chose to eliminate the decay surface entirely.

The practical drift risk is genuinely low for this specific formula. But D-35-05 was designed as a structural rule, not a risk-calibrated one — it prohibits duplication categorically because humans (and agents) are bad at calibrating which duplications are "safe." The SI-PINN-003 disaster that motivated D-35-05 was presumably also "low risk" when the first duplicate was written.

3. Drift Analysis

Concrete desync scenario: A future phase adjusts eta_c from 1 to 0.5 in pinn_architecture.md §3.2. The editor updates the canonical home. The ctl_instruction.md callout still reads eta_c = 1. A downstream implementer reading ctl_instruction.md (the assembly document — where they'd naturally look for total-loss assembly details) sees the stale default and implements the wrong value. The attribution text says pinn_architecture.md is authoritative — but the implementer doesn't follow the pointer because the formula is right there in front of them.

Does the attribution mitigate this? Partially. A careful reader who notices the discrepancy will follow the attribution. But D-35-05's philosophy is that discrepancies should not exist for readers to notice. The rule eliminates the conflict surface; attribution only labels which side of the conflict wins.

Does the energy-Huber sentinel satisfy D-35-05's intent for causal-weight? No. A sentinel on formula X proves the verifier mechanism works. It does not verify formula Y. The sentinel's value is in demonstrating the tooling exists; its limitation is that it doesn't cover the formula in question. Extending the verifier to cover causal-weight (regardless of which option is chosen) is a necessary supplement — but a verifier detects drift after the fact, while de-duplication prevents it entirely. D-35-05 demands both: "single canonical home per value/formula + a pointer, plus a verifier that proves no duplication."

The drift risk is low but non-zero, and low-probability/high-impact events are exactly what structural rules protect against. The formula will likely be edited in future phases (eta_c tuning, clipping bounds, stopgrad semantics). Each edit is a drift opportunity that de-duplication eliminates permanently.

4. Cost/Benefit

┌────────────────────┬─────────────────────────┬──────────────────────────────┬─────────────────────────────────────────┐
│     Dimension      │  Option A (status quo)  │      Option B (de-dup)       │           Option C (carveout)           │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ Drift prevention   │ None (attribution only) │ Complete (single copy)       │ None (label only)                       │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ One-time cost      │ Zero                    │ Owner gate + 1-line edit +   │ Policy amendment + verifier changes     │
│                    │                         │ re-verify                    │                                         │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ Ongoing cost       │ Low (trust attribution) │ Zero (problem eliminated)    │ High (carveout must be learned,         │
│                    │                         │                              │ applied, defended)                      │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ Governance clarity │ Poor (implicit          │ Best (rule enforced)         │ Worst (interpretive trigger)            │
│                    │ exception)              │                              │                                         │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ Precedent          │ Grandfathering is       │ D-35-05 means what it says   │ Carveouts are the resolution mechanism  │
│                    │ acceptable              │                              │                                         │
├────────────────────┼─────────────────────────┼──────────────────────────────┼─────────────────────────────────────────┤
│ STOP protocol      │ Preserved               │ Preserved                    │ Degraded (adds semantic classification) │
│ integrity          │                         │                              │                                         │
└────────────────────┴─────────────────────────┴──────────────────────────────┴─────────────────────────────────────────┘

The key finding from the adversarial review is that Option C is strictly worse than both alternatives. Both adversarial agents independently converged on this: carveouts are governance debt. They create an interpretive classification burden ("is this an assembly-context citation or a duplicated body?") that undermines the STOP protocol's binary trigger. They establish a precedent factory where each new borderline case argues for its own exemption. They add ongoing cognitive load for every future agent without reducing the actual drift risk.

Option B's one-time cost is small: a one-line pointer edit through the D-34-15 gate (which exists for exactly this purpose), a verifier extension, and a phase re-verification. The ongoing benefit — permanent elimination of a drift vector for a training-critical formula — compounds across all future phases.

Option A's ongoing cost is also small in practice, given the strong attribution and low practical drift risk. But it leaves the structural vulnerability in place, and it establishes the wrong precedent: that D-35-05's "zero" can be satisfied by "one, with good attribution."

5. Flip Conditions

I would flip to Option A if:
- Phase 36 is already deeply in progress with a hard dependency on Phase 35 being "complete," making re-verification cascading rather than contained
- The owner explicitly weighs the process overhead and decides the marginal hygiene gain doesn't justify reopening
- The verifier is extended to cover causal-weight (making drift detectable even if not prevented)

I would flip to Option C if:
- The project had an existing, well-defined taxonomy of citation types with established boundaries (it doesn't)
- Multiple similar cases already existed, making individual de-duplication impractical (only one case exists)
- The attribution were weak or missing (it's strong — but this actually argues FOR de-duplication, not against it, since a strong attribution makes the pointer conversion natural)

Neither condition holds. C remains rejected.

6. Missed Options

Two additional resolutions emerged during analysis that are lighter-weight than B but stronger than A:

Option E (verifier-only): Don't change any text. Extend the no-duplication verifier to cover both the energy-Huber body AND the causal-weight body (and ideally all formula bodies with known cross-file occurrences). Any future drift is caught immediately by automation. This is the lightest touch — zero text changes, zero governance changes, but the detection gap is closed. The weakness: detection is not prevention. A failing verifier means the drift already happened and needs cleanup.

Option F (grammatical subordination): Reword the ctl callout so the formula is grammatically subordinated to the pointer. Instead of a standalone display formula with an attribution appendix, write: "The per-time causal weighting follows the recurrence defined in pinn_architecture.md §3.2 (w_1 = 1; w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m)) for n>1; eta_c = 1)." The sentence structure makes pinn_architecture.md the grammatical subject and the formula a parenthetical restatement. This preserves readability while making the reference relationship primary rather than secondary. The weakness: the formula text is still present, so drift risk is reduced but not eliminated. This is lighter than B (no locked-content policy question — it's a wording improvement, not a structural edit) but heavier than E.

Recommendation if B is rejected: Apply E + F together — reword for grammatical subordination AND extend the verifier. This provides both a social mitigation (clearer reference relationship) and a technical detection mechanism (automated drift catching), without reopening the locked-content question.

7. Confidence

HIGH. The analysis rests on well-defined governance rules with explicit text (D-35-05's "zero," D-34-15's gate semantics), a clear factual situation (simple formula, strong attribution, two-file occurrence), and rigorous adversarial testing (both alternative positions were argued by specialized review agents and their strongest points incorporated). The only uncertainty is the owner's willingness to authorize the D-34-15 gate — a procedural judgment, not a technical one.

---
Summary

┌─────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────┐
│                      Question                       │                              Answer                              │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ Is A the best resolution?                           │ No. B is better on the merits.                                   │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ Is the ctl callout duplicated normative body?       │ Yes. Attribution doesn't change this.                            │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ Does the energy-Huber sentinel protect              │ No. Different formula, different check.                          │
│ causal-weight?                                      │                                                                  │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ Is C a good compromise?                             │ No. Carveouts are governance debt — both adversarial agents      │
│                                                     │ agree.                                                           │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ What if B is too expensive?                         │ Apply E+F: verifier extension + grammatical subordination.       │
├─────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ Confidence                                          │ High.                                                            │
└─────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┘
---

## Resolution reconciliation (2026-06-29)

The Option-B recommendation in **Agent Analysis of Gap** (above) was evaluated against the **live repository**, not just this gap text, and was **not adopted wholesale** for two grounded reasons:

1. **Its load-bearing cost premise is obsolete.** B was costed as "edit Phase-34-locked D-34-15 content + reopen for a locked edit." Git history shows Phase 35 already converted the pre-existing (Phase-19-era) inline causal formula to a pointer in commit `83f82219`; the only remaining `ctl_instruction.md` occurrence was the **Phase-35-authored** LOSS-04 callout. De-duplicating it is a Phase-35-local edit — no locked-content gate.
2. **The "zero means zero" reading overreads D-35-05.** The causal-weight formula already appears three times **inside** `pinn_architecture.md` (the §3.2 display, the LOSS-04 callout, and the §4.1 PHYS-05 catalog) under the accepted verdict-callout/catalog convention. D-35-05 governs a single canonical *authoritative* home + pointer **across the two specs**, not literal single-occurrence.

The adopted resolution honors B's **valid kernel** — the cross-file formula body could drift, and the energy-Huber sentinel did not cover causal-weight — via the lighter, project-consistent callout rewording plus a dedicated causal-weight single-home sentinel, at no locked-content cost and without the Option-C carve-out the review itself rejected. (The "both adversarial agents agree" claim in the analysis is uncorroborated by any artifact in the repo and was not relied upon.)

---

*Phase: 35-loss-energy-weight-contracts*
*Register opened: 2026-06-28*
