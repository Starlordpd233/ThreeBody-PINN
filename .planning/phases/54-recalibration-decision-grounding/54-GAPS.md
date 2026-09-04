# Phase 54 Gap Register — Recalibration Decision Grounding

Phase-local STOP-protocol gap register for Phase 54 (milestone v2.3). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md STOP protocol. The milestone-wide index is
`.planning/milestones/v2.3-GAPS.md` (created by this phase on its first gap,
under the standing first-gap trigger).

Per D-10, this register carries **one anchor entry** covering both owner
checkpoints ① and ②. The packet itself is the surfacing instrument: the full
enumeration of what the assembled evidence cannot answer lives in the packet's
`## 7. What the assembled evidence cannot answer` section
(`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`),
and this entry points at it rather than duplicating it. (The alternative — one
record per recalibration sub-question — is flagged to the owner as 54-CONTEXT.md
Open Item 2 and can be expanded into per-surface records without rework.)

## GAP-54-01 — The causal-weight / SIREN-scale recalibration: which of the five decision surfaces change and to what, and which branch of checkpoint ① is taken to decide it

- **Decision point:** The recalibration decision VER-20 item (e) routes into v2.3: which of the five decision surfaces — `η_c` (the causal-weight exponent coefficient), the `R̄` normalization and its reference scale, `ω₀` / `first_omega_0` (the SIREN initialization scale), `N_t` / `n_col` (the collocation-point count), and the causal-exponent clip's declared semantics — change, and to what, and which branch of checkpoint ① (rule directly, or commission `trainex-r3`) is taken to decide it. No candidate is offered for any surface.

- **Where in artifact:** The packet at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`, sections `## 4. The confirmed mechanism and the coupled decision surfaces` and `## 7. What the assembled evidence cannot answer` (the enumeration this entry points at by heading; §7's content lands with plan 54-04); plus `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:28-51` item (e) as the routing authority.

- **Task context:** Phase 54, ERW-01 decision-packet assembly under SCOPE-34 (the recalibration decision is owner-ratified, never agent-decided).

- **Classification:** **semantic** — SCOPE-34's own text invokes the STOP protocol's semantic / MUST-surface class for every recalibration sub-question, and a different disposition changes what Phase 56 may write into the framework spec.

- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:435`, `:445`, `:181`, `:454`, `:461`, `:668-671` — fix the current values and their contract markers (the `w_n` formula and the `eta_c = 1` Phase 35 contract block, the fixed-at-30 `first_omega_0` sentence, the `n_col=4096` signature and its stated range, the clip's underflow-only purpose), but do not state any recalibrated value, form, normalization, or bound.
  - `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:28-51` — item (e) explicitly declares that the correct calibration is a research question rather than an engineering default, and routes the decision to the owner-governed channel.
  - The trainex-r2 round's output contract §7 clause 3 forbade that round from naming a remedy, so it carries no decision sheet, no options menu, and no marked default `[r2-QUAL]` (quoted verbatim in the packet's §0).
  - `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` — establishes the mechanism (the initialization-scale chain, the underflow bound, the floored weights) but ends at diagnosis; it names no recalibrated value.

- **Mathematical / engineering grounding:** `w_n` is an **exclusive** prefix sum over collocation points — `cumsum_excl[n] = Σ_{m<n} R̄_m.detach()`, implemented by right-shifting a `torch.cumsum` and prepending a zero (`pinn/loss_catalog.py:326-342`) — so the exponent at point *n* grows with the count of preceding points, and the spec's `n_col = 4096` (`pinn_architecture.md:454`) against the run's `collocation_count = 16` (`pinn/train.py:1033`) differs by the exact factor `4096 / 16 = 256`. The float32 exponential underflows once its argument exceeds the threshold transcribed in the audit (`2026-08-17-residual-frame-conformance-audit.md:127`), so an unnormalized `R̄` near 10¹⁰ saturates the weighting shut at step 0 rather than degrading it gradually — the observed 15-of-16 floored weights (`:121`). Consequence per surface: a changed `η_c` without an `N_t` disposition leaves the exponent magnitude undetermined (SPEC-06's joint-ratification requirement, roadmap SC-5); an `R̄` normalization without a stated reference scale leaves the formula's units undefined; a changed `first_omega_0` shifts the second-derivative magnitude the whole causal mechanism is calibrated against (`:181`); and the clip's numeric bound, if any, interacts with whichever of those changes (`:668-671`). Each surface therefore changes what Phase 56 may legally write into the framework spec, which is why none of them is agent-disposable.

- **Agent was tempted to:** No candidate was formed, and none is recorded: SCOPE-34 removes the choice from the agent's authority by construction, so the packet is written as the surfacing instrument and the enumeration of what remains undecided lives in the packet's §7 rather than in an agent-held preference.

- **What the user needs to decide:** Two checkpoints, in order. Checkpoint ①: the branch — rule directly, or commission `trainex-r3`. Checkpoint ②: the per-surface disposition, plus the SCOPE-38 re-ratification of each locked contract the pick amends. A ruling that does not dispose of `N_t` / `n_col` is incomplete under roadmap Success Criterion 5 and SPEC-06's joint-ratification requirement, and routes back to the owner. No candidate value is offered for any surface; the only options named are the two branches at ①.

- **Confidence of impact:** **HIGH** — Phase 56 (SPEC-01 + SPEC-06) may not open without checkpoint ② being discharged, and Phases 57 and 58 follow from it.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Checkpoint ① discharged 2026-08-21** — the owner selected `commission trainex-r3`, recorded verbatim in `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`. The gap stays `OPEN` because checkpoint ② — the per-surface disposition and its SCOPE-38 re-ratifications — is what closes it, and that awaits the round's delivery, its Rule-19 verification, and owner ratification. The ruling itself is recorded in `54-RULING.md`, not here — a ruling is not a gap (D-09).

  ERW-02 assembly (2026-08-21) widened what the round is asked to consider, without disposing of anything: item (e)'s **fourth remedy family** (redesign the curriculum mechanism so it does not require the two to agree at initialization) was transcribed verbatim into the packet's §4.3 after it was found absent from the five decision surfaces, and two further open items were added to the packet's §7 — the SQR-SkipResNet stack's contribution to the same second-derivative magnitude `first_omega_0` is credited with, and the absence of any statement of the source method's own calibration procedure. See the packet's §11 amendment record.

  **Premise adjudication (2026-09-03, plan `54-11`).** The two returned reports' premise
  challenges have been adjudicated against the packet premises they challenge, using the
  verdicts the ERW Rule-19 verification report already recorded as the only admissible
  evidence about any claim. Nineteen packet premises were adjudicated: three contradicted,
  eleven qualified, four intact and one unsettled; no answer the round returned is marked
  unusable. The round-level re-frame determination is `REFRAME-PARTIAL` and every enumerated
  surface carries the same value, recorded per surface in
  `.planning/phases/54-recalibration-decision-grounding/54-PREMISE-ADJUDICATION.md`. One
  further decision point falls **inside this record's own scope** and is therefore recorded
  here rather than given an identifier of its own: the two returned reports place a
  normalization of the residual in **different mechanical locations**, one changing only the
  weight vector and the other changing the outer loss's magnitude as well, and the
  verification report classifies that as an open cross-report difference whose resolution is
  the disposition of the surface itself, at checkpoint ②, on the consolidated sheet. Both
  positions are located by line in the verification report's cross-report adjudication and
  neither is reproduced, ranked or marked anywhere in this pass. **This gap stays `OPEN`**;
  nothing in the adjudication closes it, disposes of any surface, or touches the ruling
  record's checkpoint ② or its pre-declared completeness rule. Ten decision points that are
  **not** sub-questions of this record's decision point are filed below as `GAP-54-02` …
  `GAP-54-11` under D-17; the granularity choice is offered back rather than assumed, per
  54-CONTEXT.md Open Item 2.

  **Checkpoint ② discharged 2026-09-04 — RESOLVED-WITH-INSTRUCTION.** The owner
  expressly delegated the final checkpoint adjudication to the Codex primary
  agent with the instruction to use its best mathematical and scientific
  reasoning. The resulting owner-authorized ruling is recorded in
  `54-RULING.md`: `A1 + B2 (residual-wide) + C1 + D3 + E1`, with `eta_c = 1`, a
  fixed six-case-probe-derived `R_ref`, `first_omega_0 = 30`, `n_col = 4096`
  total per training batch aggregated into `M = 16` fixed equal-time bin means,
  and the underflow-only dtype guard retained with binding made observable.
  Block 1 is re-ratified in kind; Blocks 2 and 3 are explicitly not amended.
  This final paragraph supersedes this entry's earlier OPEN standing.

## GAP-54-02 — Whether the authorized decision-surface set is complete, given a verified-locus finding that the capacity attributed to an authorized surface sits outside the authorized set and an unsettled finding that a failure mode survives disposing of all five

- **Decision point:** Whether the authorized decision-surface set for the recalibration is widened, and if so by what process — given (i) a verified finding that the architectural section carrying the capacity the packet attributes to one authorized surface is not inside SCOPE-33's enumeration, and (ii) an unsettled finding that a failure mode survives disposing of all five enumerated surfaces as the packet scopes them. No surface is proposed, named or scoped by this record.

- **Where in artifact:** `.planning/phases/54-recalibration-decision-grounding/54-PREMISE-ADJUDICATION.md`, row `PREM-02` and its per-premise detail. Underlying loci: the packet's §4.3 surface enumeration at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md:151-193` with S3 at `:171`; the packet's own §7 `S3-adjacent` entry at `:311`; the fourth-remedy-family transcription and its correction note at `:211`, `:213`, `:215`; `.planning/REQUIREMENTS.md:118` (SCOPE-33); `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:204-261`. Verdicts: `PC-1f` (`CONFIRMED-NARROWER` on locus and scope, `NOT-VERIFIABLE-HERE` on the capacity attribution) and `PC-6c` (`NOT-VERIFIABLE-HERE`), with supporting routed rows `R-04` and `R-05`, all in `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md`.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating the open-book report's `PC-1` and `PC-6` against the packet's §4.3, under ERW Rule 17 and the runbook's handoff step 6.

- **Classification:** **cross-phase reframing** — it changes what Phase 56 may legally write into the framework spec and what the train-free gate Phase 56 wires must measure before Phase 57 may spend a Stage-0 run, and it changes what the authorized scope row admits as a surface.

- **Source silence:**
  - `.planning/REQUIREMENTS.md:118` (SCOPE-33) enumerates the authorized items as `52-VER-20-ROUTING-HANDOFF.md` (a)–(e) plus the coupled collocation-count disposition. Its enumeration does not reach `pinn_architecture.md` §2.3, and it states **no rule** for admitting a surface the evidence later identifies. Silence about the admission procedure, not about the current list.
  - `RESEARCH-CONTEXT-MASTER.md:311` — the packet's own §7 entry says in its own words that the evidence "does not establish how the two factors divide" the measured quantity and that "Whether the stack constitutes a surface of its own is not settled by anything in this package." The packet names the question and declines to answer it.
  - `RESEARCH-CONTEXT-MASTER.md:211`, `:213` transcribe the routing authority's fourth remedy family and record that all four families sit inside the milestone's spec-edit authorization; neither says whether a **surface** outside the five is thereby admitted. A family and a surface are different objects in this packet's own vocabulary.
  - `.planning/ROADMAP.md` Phase 56's success criteria govern what the amendment must record for the surfaces it touches and are silent on admitting a new one; Phase 55's criteria charter the probe's reported quantities and do not reach the gate's condition set.
  - `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` — the checkpoint-② surface table carries exactly the five, and its completeness rule concerns the collocation-count disposition rather than the set's extent.
  - The ERW Rule-19 verification report routes both halves of the finding as `NOT-VERIFIABLE-HERE` and names what would settle each; a routing target is not a result.

- **Mathematical / engineering grounding:** Two findings bear on the same question from opposite directions and neither is agent-disposable. **(i)** The capacity locus. `PC-1f` re-derives that `pinn_architecture.md` §2.3 occupies `:204`–`:261`, that SCOPE-33's enumeration does not reach it, and that the packet's §7 records the stack as an unsurfaced gap — all confirmed. The claim that the capacity *lives* there rests on a clean-room depth sweep routed at `R-05`. If it holds, one enumerated surface is being asked to carry a capacity that resides in an unenumerated one, and the arithmetic that decides whether that surface can reach its threshold would be measuring the wrong object. **(ii)** The surviving pathology. `PC-6c` asserts that a recipe repairing the weight vector while leaving the outer physics loss at its current magnitude would satisfy the train-free gate's three conditions and still train on the physics term alone. Its arithmetic inputs are separately confirmed at `PC-6a` (the median physics-to-data gradient-norm ratio over every retained record) and `PC-6b` (the binary32 round-to-nearest headroom, below which an addend leaves a running sum unchanged); the prediction itself is routed. The mechanical reason it cannot be dismissed is structural: GATE-04's three conditions, quoted at `CC-2` from `.planning/REQUIREMENTS.md:100`, are conditions on the **weight vector** — no weight pinned at the clamp floor, a vector carrying differential information, and the front index able to advance — and **none of them is a condition on the magnitude of the physics loss**. A weight-vector repair therefore satisfies the gate by construction while leaving a gradient-magnitude imbalance the gate does not measure. If that holds, the authorized surface set contains no surface addressing it, and the fail-closed gate that exists to protect the single remaining Stage-0 run would pass a recipe that cannot train — which is precisely the failure GATE-04 was written to prevent. Whether the set is widened is a **scope** decision: SCOPE-33 is an owner-ratified boundary and its enumeration is what Phase 56 may legally edit. An agent that answered it would have widened the owner's authorized scope by writing a sentence.

- **Agent was tempted to:** No surface was named, proposed or scoped, and the reason the temptation is nameable is recorded honestly rather than omitted: to read `RESEARCH-CONTEXT-MASTER.md:213`'s statement that all four remedy families sit inside the milestone's authorization as already admitting a mechanism-level surface, and to read the packet's §7 `S3-adjacent` entry as an implicit sixth surface. Either reading would have widened the enumeration by inference rather than by ratification, which is the same act SCOPE-34 removes from the agent by construction.

- **What the user needs to decide:** Whether the authorized decision-surface set is widened, and if so by what process. Framed at the governance level only; no value, form, bound, ordering or marked choice is named for anything. (A) Widen the authorized surface set, recorded as a SCOPE-33 amendment carrying its own re-ratification under SCOPE-38's discipline. (B) Decline to widen, recording why, and leave both findings on the record as unaddressed by the authorized set. (C) Defer the question to checkpoint ②, so it is decided together with the per-surface dispositions rather than ahead of them. (D) Commission the evidence that would settle whether the pathology survives — the verification report names what would settle each half — before deciding whether the set needs widening. The enumeration is the owner's to widen; this record hands the finding over and disposes of nothing. **Granularity:** this is recorded as a separate gap because it is not a sub-question of `GAP-54-01`'s decision point, which asks which of the five surfaces change and to what; the owner may instead fold it into `GAP-54-01` as a sub-entry (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **HIGH** — it changes what Phase 56 may legally write, what GATE-04 must measure, and therefore whether Phase 57 may spend the single preserved Stage-0 run against a recipe the gate cannot refuse.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option B, 2026-09-04 — do not widen the
  authorized surface set for this ruling.** Residual-wide `B2` addresses the
  established physics/data conditioning concern inside enumerated surface S2;
  `first_omega_0` and the power-skip stack remain unchanged, and the stack is a
  future ablation rather than a Phase-56 amendment surface. This does not claim
  the IC term or trajectory accuracy is solved; GATE-04 remains a train-free
  causal-mechanism gate and a passing run may still fail honestly under the
  milestone's declared terminal branch.

## GAP-54-03 — The packet describes the same reference probe two incompatible ways, and one decision surface's reference scale is calibrated against it

- **Decision point:** Which of two incompatible descriptions of the same reference probe, both reproduced verbatim in the packet, is the correct one — and consequently whether the relative-error datum they disagree about may be used as a converged-regime residual reference at all. No reference scale is named, proposed or ranked by this record.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, row `PREM-09` and its per-premise detail. Underlying loci: `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:109` and `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:83`, both reproduced verbatim in the round's closure-evidence bundle; the transcription as `F-12` at `RESEARCH-CONTEXT-MASTER.md:278` and as `M6` at `:139-141`; the audit's inference at `2026-08-17-residual-frame-conformance-audit.md:167`. Verdicts `CB-F1a`, `CB-F1b` and `CB-F1c`, all `CONFIRMED`, with cross-report points `X-03` (`RESOLVED-BY-EVIDENCE`) and `X-04`, in the verification report.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating the closed-book report's `Finding 1` against the packet's `F-12` and `M6`.

- **Classification:** **semantic** — a converged residual scale is what one whole decision surface is calibrated against, and a different disposition changes what Phase 56 may write for that surface.

- **Source silence:**
  - `2026-08-17-residual-frame-conformance-audit.md:109` describes finite-differencing a stored Brutus trajectory; `52-DIAG-05-REDERIVATION.md:83` describes a trained network against ground truth. Both are in the packet, **neither cites the other**, and nothing reconciles them.
  - The packet's §11 amendment record at `RESEARCH-CONTEXT-MASTER.md:412-429` carries sixteen entries and **none addresses the contradiction**. This is the load-bearing silence: for the packet's other internal contradiction the amendment record settles which reading is authoritative, and here it does not.
  - `RESEARCH-CONTEXT-MASTER.md:141` records that the packet "takes no position on whether it is a reference scale for anything" — the packet transcribes the datum and declines to give it a role.
  - `RESEARCH-CONTEXT-MASTER.md:299` (§7's S2 entry) records that the evidence does not pin whether a normalization is to be introduced, its form, or its reference scale.
  - `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` name no reference scale anywhere; `pinn_architecture.md:435` consumes the residual unnormalized and no normalization is specified anywhere in the spec.
  - The verification pass stopped deliberately short of settling it, recording that reading the probe's source in the tree "would have been adjudicating a premise, which is wave 4's authority."

- **Mathematical / engineering grounding:** The two descriptions license different inferences and only one of them can bear on the question the datum is used for. A consistency check that finite-differences a stored integrator trajectory measures whether the integrator's own output satisfies the force law: the quantity it bounds is a property of the trajectory data and the differencing stencil, and it says nothing about any network. A measurement on a trained network measures how small that network's residual becomes. Only the second could establish what a *converged* residual scale is, and the packet's `F-12` transcribes exactly that inference and tiers it as established evidence a reader may rely on. `CB-F1b` adds an independent dimensional point, confirmed: with the residual defined at `pinn_architecture.md:429` as the mean squared force-balance discrepancy over the three bodies, a **relative** acceleration error determines the residual only once multiplied by the squared acceleration norm it is relative to, so a dimensionless figure alone under-determines the residual by that squared scale. The consequence is that the packet's §5.2 question — against what reference scale a normalization would be defined — has exactly one candidate datum in the whole package, and that datum's provenance is described two incompatible ways with no authoritative reading available. Both returned reports independently concluded the gate cannot supply the normalizer, so no returned answer rests on the contradicted reading and the exposure is forward: any later use of the datum as a converged-scale reference inherits the contradiction. Choosing between the descriptions, or naming a reference scale, is a disposition of a decision surface and is reserved to the owner.

- **Agent was tempted to:** Read the probe's source in the repository and decide which description is right. Declined twice over: the verification report already recorded that doing so would be adjudicating a premise ahead of its authority, and — the second reason, which is this pass's own — even a correct reading of the probe would settle the *description* without settling whether the datum is a reference scale, which is the surface disposition SCOPE-34 removes from the agent by construction.

- **What the user needs to decide:** Which reading governs, and what follows for the datum's use. At the governance level, with no reference scale named: (A) the operative diagnosis's description is corrected to match the audit's; (B) the audit's description is corrected; (C) the datum is withdrawn from use as a converged-scale reference and both descriptions are kept as historical record; (D) the question is folded into checkpoint ②, since what serves as a reference scale for the residual is a disposition of one of the five surfaces. **Granularity:** recorded separately because the *description* question is not a sub-question of `GAP-54-01`'s decision point even though the *use* question is; the owner may fold it in (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **HIGH** — the package's only converged-regime datum is what one whole decision surface's question is framed around, and Phase 56 would cite whatever the ratification rests on.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option C, 2026-09-04.** Withdraw the
  disputed Gate-B datum from use as a converged-network residual reference. Keep
  both historical descriptions in their source records; neither is corrected by
  inference here. The ratified `R_ref` instead comes from the fixed six-case
  GATE-04 initialization probe defined in `54-RULING.md`.

## GAP-54-04 — The round's one scaling-law disagreement, which the delivery note's own join rule says must be settled before the menus downstream of it are trusted

- **Decision point:** Whether the round's single scaling-law disagreement is settled before the menus downstream of it are read, and by what. Neither position is endorsed, ranked or reproduced by this record, and no scaling law is asserted by it.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, rows `PREM-01`, `PREM-02` and `PREM-04`, and the surface-level determination for S3. Underlying loci: the two positions at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/claude-resolution.md:69-86` and `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/chatgpt-resolution.md:353-360`; the verification report's cross-report point `X-12` (`OPEN-DISPUTE`), its scaling-statement classification table, and the routed rows `R-04`, `R-05` and `CB-07`; the join rule at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/DELIVERY-NOTE.md:142`.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating `PC-1` against the packet's `F-02` and §4.3, where the disputed law is what the capacity argument runs through.

- **Classification:** **semantic** — it is a physics question about the locked architecture, and the delivery note's own join rule makes it the case that blocks trust in the menus downstream of it.

- **Source silence:** Neither measurement was made on this project's own model: one position is an explicitly conditional analytic model and the other a clean-room re-implementation built from the specification text, and **no artifact in this repository measures the response**. `pinn_architecture.md:181` fixes the locked initialization scale and is silent about any other. `RESEARCH-CONTEXT-MASTER.md:301` (§7's S3 entry) says in its own words that the evidence "does not pin anything about any other scale". `RESEARCH-CONTEXT-MASTER.md:311` records that the evidence does not establish how the two contributing factors divide the measured quantity. `DELIVERY-NOTE.md:142` states the obligation — two agents who disagree on the scaling laws have a physics dispute that must be settled before any menu is trusted — and names **no procedure and no authority** for settling it. The verification report classified all five scaling statements the round makes, found exactly one disagreement, located the menus downstream of it, and settled nothing about it.

- **Mathematical / engineering grounding:** The two positions are not two estimates of one measured quantity; they are two **models**, and both reports name the same mechanism while disagreeing about its magnitude under the locked stack. One derives the derivative scaling for a bare periodic first layer at fixed weights — the first and second derivatives carry one and two powers of the initialization frequency, and squaring the residual carries four — and retains it as an explicitly conditional heuristic, saying in its own text that it is neither a measured law nor a guaranteed bound for the specified stack. The other argues the law fails under the locked architecture for a structural reason: the first operation applied to the first hidden activation is a positively scale-invariant normalization followed by a square, so the power branch's value and its derivatives are independent of the amplitude the first-layer frequency imparts, and it measures a much weaker response in a clean-room sweep. The disagreement is consequential because the per-surface capacity accounting the round was required to produce is computed **through** this law, while the requirement side of that accounting is fixed by quantities re-derived from the tree — the clamp requirement and the front-advance requirement, both re-derived at `CC-7` from the retained log's median residual and the implementation's own floor resolver. Two laws that differ by roughly ten decades in what a large change on that surface buys give two different answers to whether the surface can reach its threshold **at all**, which is the difference between a lever and an irrelevance. That is why the join rule treats a scaling disagreement differently from a disagreement about a marked default: the second is resolvable on the merits, the first invalidates the arithmetic both sets of merits were computed with.

- **Agent was tempted to:** Prefer the clean-room sweep over the conditional analytic model, because a measurement reads as stronger than a heuristic. Neither was made on this project's own model, so the preference would have been aesthetic rather than evidential. The verification report recorded the same temptation and declined for the same reason; this pass does not overturn it and adds no view of its own.

- **What the user needs to decide:** Whether and how the dispute is settled before the menus downstream of it are read. At the governance level, with no law asserted and no menu reproduced: (A) the dispute is settled by an owner-authorized characterization on this project's own model before any menu downstream of it is read — naming the instrument Phase 55's INST-04 is chartered to build is routing, not authorizing; (B) the dispute is recorded and the affected menus are deferred at the consolidation; (C) the dispute is declared not to block, with the reason recorded; (D) the consolidation proceeds and each affected menu carries this gap's identifier, so the owner disposes of the dispute at checkpoint ② beside the surfaces it qualifies. **Granularity:** recorded separately because a dispute about a physical scaling law is not a sub-question of which surface changes and to what; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **HIGH** — the delivery note names this exact case as the one that invalidates downstream menus, and the verification report located those menus across both reports.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option C, 2026-09-04 — the scaling-law
  dispute does not block this ruling.** Both reports retain
  `first_omega_0 = 30`, even though their explanations differ, and neither
  supports an enumerated frequency reduction as a sufficient standalone repair.
  The selected frozen `R_ref` is measured on the actual initialized recipe, so
  the causal calibration does not rely on either disputed scaling exponent.
  Phase 55 may characterize the law as evidence, but its result cannot change the
  ratified frequency without a new owner decision.

## GAP-54-05 — The collocation budget's unit is fixed by no consulted source, while the pre-declared completeness rule makes disposing of the count mandatory

- **Decision point:** Whether the collocation budget is defined per batch or per trajectory — a distinction the ratification must make, because the joint-ratification requirement binds the count's disposition to the exponent coefficient's and the pre-declared completeness rule makes a count-silent ruling incomplete. No count and no unit is proposed, defaulted or ranked by this record.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, rows `PREM-07` and `PREM-08`, and the surface-level determination for S4. Underlying loci: `RESEARCH-CONTEXT-MASTER.md:147` (§4.2), `:179-185` (S4) and `:303` (§7's S4 entry); `pinn_architecture.md:454` and `:461`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1815` and `:1840`; `.planning/REQUIREMENTS.md:95` (SPEC-06); `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`'s completeness rule. Verdicts `CB-F4a` and `CB-F4c`, both `CONFIRMED`, with `CB-F4b` `CONFIRMED` for the multiplier arithmetic.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating the closed-book report's `Finding 4` against the packet's §4.2 and S4.

- **Classification:** **semantic** — the unit changes what the exponent magnitude is at any given coefficient, so it changes what Phase 56 may write as the count the calibration binds to and what re-check trigger the spec must carry.

- **Source silence:**
  - `pinn_architecture.md:454` gives the sampler signature's default and `:461` its stated range; **neither states a unit**.
  - `ctl_instruction.md:1815` sits in a section describing a batch of trajectories and `:1840` calls the collocation budget a provisional or example budget, verbatim; neither fixes the unit, and the provisional marking makes the number explicitly non-binding.
  - The three uploaded attachments: `CB-F4c`'s negative search over both specification blocks and the curriculum block carrying the batch construction returns nothing, recorded as `NEGATIVE-SEARCH-EMPTY` with its scope stated. The verification report adds, as a statement the finding itself does not make, that the silence **also holds of the specification files themselves at the pinned tree**.
  - `RESEARCH-CONTEXT-MASTER.md:147` computes the coupling without saying which unit either number carries, and `:303` records only that no source states a disposition of the count.
  - `.planning/REQUIREMENTS.md:95` (SPEC-06) and `54-RULING.md`'s completeness rule both require the count to be disposed of and **neither names a unit**.

- **Mathematical / engineering grounding:** The causal weight at a collocation point is the exponential of the negative coefficient times the **exclusive** prefix sum of the preceding detached residuals, so the exponent at the last point is proportional to the prefix **length**, which is one less than the count. Two consequences follow and only the second makes the unit a gap rather than a wording point. First, the multiplier between the two fixed counts is the endpoint-prefix ratio and not the cardinality ratio: `CB-F4b` derives both exactly from the packet's own exclusive-prefix definition, and the packet's own hedge at `RESEARCH-CONTEXT-MASTER.md:147` makes its figure defensible as an order of magnitude but not as the multiplier a joint ratification is scoped against. Second — and this is the gap — the two candidate units are **numerically confusable**: the cardinality ratio multiplied by the executed count equals the specified count exactly, `256 × 16 = 4096`, so a per-trajectory budget of one count and a per-batch budget of the other coincide in total while producing entirely different prefix lengths per weight vector and therefore entirely different exponent magnitudes at the same coefficient. A ratification that dispositions the count without stating its unit therefore leaves the exponent magnitude under-determined by exactly the factor the joint-ratification requirement exists to pin. That is the same structural defect the pre-declared completeness rule already names for a count-silent ruling, arriving one level down: the rule catches a ruling that omits the count, and this gap catches a ruling that states a count whose unit is undefined.

- **Agent was tempted to:** Read the curriculum document's batch-construction context as fixing the unit per batch. That section calls the budget provisional and describes the batch in the same breath, so inferring a unit from adjacency would have supplied a fact the source does not state — and would have supplied it for a quantity the joint-ratification requirement makes owner-ratifiable.

- **What the user needs to decide:** Whether and where the unit is settled. At the governance level; no count and no unit is named: (A) the ratification states the unit explicitly as part of the count's disposition, and the completeness rule is read to require it; (B) the unit is settled first, as a separate codification item, before the disposition is ratified; (C) the unit question is folded into `GAP-54-01` as a sub-entry of the count disposition; (D) the ratification is permitted to disposition the count without a unit, with the resulting under-determination recorded and accepted and the reason stated. **Granularity:** recorded separately under D-17 because it asks what a quantity means rather than what its value should be; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **HIGH** — the count's disposition is jointly ratifiable with the exponent coefficient's, and an undefined unit under-determines the exponent by the same factor the joint requirement exists to fix.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Resolved from prior owner instruction plus the
  owner-delegated checkpoint ruling, 2026-09-04.** The repository-wide trace found
  that GAP-39-12 already fixes `4096` as the total per training batch and chooses
  near-even quotas over selected trajectory slots; the Phase-54 negative search
  had consulted too narrow a source set. Ratified `D3` retains that total and
  identity weighting, and supersedes only GAP-39-12's independent full-domain
  time draws: a 256-slot batch contributes one point per slot to each of 16 fixed
  equal-`u` bins, each bin mean has exactly 256 rows, and the batch-global causal
  prefix has 16 terms. The deterministic 240-slot remainder policy is recorded
  in `54-RULING.md`. Empty bins are impossible; microbatching may not reset the
  aggregate or prefix. Any change to total, selected-slot unit, bin count, or
  allocation invalidates `R_ref` and requires a fresh GATE-04 pass.

## GAP-54-06 — The round's characterization does not distinguish the two optimizer phases, and two separate mechanisms differ between them

- **Decision point:** Whether the round's characterization of the causal mechanism, and the invariant defined on it, are stated separately for the two optimizer phases — the collocation set is re-drawn every step in one and held fixed for a segment in the other, and whether the causal weights are recomputed inside the second phase's line searches is settled nowhere. No remedy and no recipe element is proposed by this record.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, rows `PREM-07` and `PREM-16`, the per-premise detail for `PREM-07`, and the surface-level determination for S5. Underlying loci: the verification report's `PC-5b` and `D-2b`, both `UNSUPPORTED`, and `CB-F8a`, `CB-F8b`, `CB-F8c`, `CB-F8d`, all `CONFIRMED`, with cross-report point `X-19` `CORROBORATED`; `pinn_architecture.md:698`, `:741`, `:435`, `:445`; the open-book report's own gaps row `G-7`; the closed-book report's `Finding 8` at `chatgpt-resolution.md:88-92`. Two candidate rows the verification report proposed and did not file are folded here, because they are one decision point seen through two mechanisms.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating `PC-5` and the closed-book report's `Finding 8`, where a cited line resolved to the other optimizer phase and a second finding established a silence about that same phase.

- **Classification:** **semantic** — it bears on the semantics of the invariant a later owner checkpoint is chartered to re-ratify, and on whether a composed recipe containing a second-phase refinement can be ratified as coherent.

- **Source silence:**
  - Both loci cited for the per-step re-draw resolve, but the one the departure's stated consequence needs does not carry it: the cited line is the fixed-draw path of the second optimizer phase, which draws once and holds the set for the segment. Neither the returned report nor the package distinguishes the phases anywhere.
  - `pinn_architecture.md:698` freezes the loss multipliers during the second phase and `:741` states the two-phase handoff; `CB-F8a` confirms all three cited elements are present and **none addresses weight recomputation inside a line search**.
  - `CB-F8b` establishes the silence by negative search across both specification blocks covering the loss contract and the optimizer sections, recorded as `NEGATIVE-SEARCH-EMPTY` with its scope stated. The open-book report records the same silence independently at its own gaps row, and `X-19` records that agreement as entitled corroboration because it is a negative claim about attachments both agents read in full.
  - `RESEARCH-CONTEXT-MASTER.md:293-317` (§7) carries **no entry** for either mechanism.
  - `.planning/REQUIREMENTS.md:118` (SCOPE-33) authorizes the routing-handoff items plus the coupled count disposition and does not reach the optimizer contract, so whether this is even inside this milestone's editable set is part of what is being asked.

- **Mathematical / engineering grounding:** Two mechanisms differ between the phases and both are load-bearing. **(i)** The causal front index is defined per step as the largest index whose weight exceeds one half, and the invariant trips on the **high-water mark** of that index accumulated across steps. Under a per-step re-draw the index is computed over a different sampled time set every step, so it is not a persistent state and the high-water mark accumulates over draws that are not comparable; under a set held fixed for a segment it **is** a persistent state and the high-water mark means what the guard assumes it means. A guard ratified against one semantics does not automatically carry to the other, and the milestone's own third owner checkpoint is chartered precisely to re-ratify that window for the new dynamics rather than carry it over silently. **(ii)** Differentiating a weighted mean produces two terms, one through the residuals and one through the weights. Detaching the weights suppresses the second, which is correct and intended for a fixed weight vector. If the weights are nonetheless recomputed as functions of the trial parameters inside a line search, the vector supplied to the search is the gradient of a **different function** than the scalar the search compares, so the sufficient-decrease and curvature tests are evaluated on an inconsistent objective-and-gradient pair — the standard failure mode of a detached surrogate inside a search that assumes consistency. Both the returned finding and the verification row are careful to call this a conditional risk rather than a verified defect, and that care is warranted: the attachments are silent and no in-repository claim was made. What makes it a **decision** rather than a note is that a composed recipe containing a second-phase refinement cannot be ratified as coherent while the behaviour is undetermined, and one of the two returned recipes addresses it explicitly while the other does not.

- **Agent was tempted to:** Treat the mis-cited line as a typographical slip and verify the re-draw claim at the line that does carry it. That would have converted an `UNSUPPORTED` verdict into a confirmation and erased the per-phase distinction the mis-citation exposed — which is the only reason the distinction surfaced at all.

- **What the user needs to decide:** Whether the characterization and the invariant's semantics are stated per optimizer phase, and whether the second phase's weight behaviour is settled before a recipe containing it is ratified. At the governance level; no recipe element is named: (A) the departure and the invariant's semantics are re-stated per optimizer phase before any consolidation consumes them; (B) both are scoped to the phase the retained run characterized and the other is recorded as unexamined; (C) they are left as the round wrote them with this record attached; (D) the second-phase behaviour is settled first as a separate item, and whether it sits inside the authorized spec-edit set is decided with it. **Granularity:** recorded separately because it asks whether a characterization holds, not what any surface's value should be; the owner may fold it into `GAP-54-01`, or split it back into its two mechanisms, per 54-CONTEXT.md Open Item 2.

- **Confidence of impact:** **HIGH** — it bears directly on the invariant a later owner checkpoint is chartered to re-ratify, and on the coherence of any composed recipe that carries a second optimizer phase.

- **Status:** DEFERRED

- **Resolution note:** **DEFERRED by the owner-authorized checkpoint ruling on
  2026-09-04.** The two optimizer phases must be distinguished, but SCOPE-33 does
  not authorize checkpoint ② or Phase 56 to add an L-BFGS objective contract.
  The conditional detached-weight/line-search consistency risk therefore moves
  to Phase 57 owner checkpoint ③ and must be settled **before RUN-04 executes**;
  no current candidate behavior is silently selected. Independently, the
  checkpoint-② ruling establishes that a front measured on a resampled Adam
  training batch is diagnostic only, not persistent advancement evidence.
  Checkpoint ③ must bind invariant B to a fixed, pre-registered monitoring
  context or another explicitly ratified estimator that separates parameter
  improvement from resampling.

## GAP-54-07 — Whether the reported gradient-norm ratio establishes that the data term's gradient disappears, or only that the imbalance is severe

- **Decision point:** Whether the audit's inference from a global gradient-norm ratio to the complete disappearance of the data term's gradient may be relied on before per-component evidence exists, or whether its evidential status is downgraded, commissioned or withdrawn. No remedy and no surface disposition is proposed by this record.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, row `PREM-11`. Underlying loci: `2026-08-17-residual-frame-conformance-audit.md:132`, `:134` and `:169`, reproduced verbatim in the round's closure-evidence bundle and tiered as hard-constraint evidence at `RESEARCH-CONTEXT-MASTER.md:63`; `pinn_architecture.md:690`. Verdicts `PC-6a` `CONFIRMED`, `PC-6b` `CONFIRMED`, `PC-6c` `NOT-VERIFIABLE-HERE`, `CB-F6a` `CONFIRMED`, `CB-F6b` `CONFIRMED`, `CB-F6c` `CONFIRMED`, `CB-12` split `CONFIRMED` / `NOT-VERIFIABLE-HERE`, with cross-report point `X-17` `OPEN-DISPUTE`.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating the open-book report's `PC-6` and the closed-book report's `Finding 6` against the audit's §6a conclusion as the packet carries it.

- **Classification:** **semantic** — it changes what the operative diagnosis can be said to have established, and therefore what a Phase 56 amendment is entitled to cite as its evidential base.

- **Source silence:** **No retained artifact records per-component gradient statistics** for the data and physics terms over the accumulation; the search for one was run and returned nothing. `pinn_architecture.md:690` requires exactly that logging, but only before a future dominance control is adopted, so the specification anticipates the measurement and does not require it yet. The packet tiers the closure-evidence bundle as a hard constraint **for the evidence** while stating in the same sentence that the *reasoning* is testable under ERW Rule 17 (`RESEARCH-CONTEXT-MASTER.md:63`), so the packet neither settles the inference nor claims to. The verification report confirms both positions as stated and settles neither.

- **Mathematical / engineering grounding:** Floating-point addition acts componentwise, so a ratio of vector **norms** bounds no individual component: two vectors with disjoint support have an arbitrary norm ratio and lose nothing when added. That makes the objection unimpeachable as a statement about **warrant** — and it is important that it claims nothing more, because the objection does not assert that the data gradient survives, and the row that records it says so. On the other side the inference is plausible for aligned, dense gradients, and both of its inputs are confirmed independently: the median physics-to-data gradient-norm ratio computed over every record of the retained log, and the binary32 round-to-nearest headroom below which an addend leaves a running sum unchanged. The dispute is therefore about what the available evidence **proves**, not about what is likely, and it is settleable only by an instrumented measurement nobody has run. It is consequential for two reasons. It is the load-bearing step in one report's argument about where a normalization of the residual belongs — an argument that reaches a decision surface — and a diagnosis row relied on as established and later downgraded would move what the amendment is entitled to cite as its ground.

- **Agent was tempted to:** Resolve it in favour of the componentwise objection, which is mathematically unimpeachable as a statement about warrant. That would have been adjudicating between two returned positions rather than recording their entitlement, and it would also have **overstated** the objection, which explicitly does not claim the data gradient survives.

- **What the user needs to decide:** What evidential status the inference carries and whether it is relied on. At the governance level: (A) the componentwise statistics are commissioned before the inference is relied on; (B) the inference is retained with its evidential status downgraded and the downgrade recorded; (C) the inference is withdrawn from the diagnosis; (D) the question is deferred to checkpoint ② and disposed of alongside the surfaces the argument bears on. **Granularity:** recorded separately because it asks what a diagnosis establishes rather than what a surface should become; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **MEDIUM** — it changes what the diagnosis can be said to have established and what a later amendment may cite, not what any spec currently says.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option B, 2026-09-04.** Retain the
  verified conclusion that the physics/data gradient-norm imbalance is severe.
  Downgrade the componentwise-disappearance statement to unproven and do not rely
  on it in the amendment rationale; a ratio of global norms cannot establish
  componentwise rounding. Raw and normalized per-term gradient telemetry remains
  required so the proposed run can measure what actually survives.

## GAP-54-08 — The invariance a premise finding's scaling argument rests on is exact only in a limit, as implemented

- **Decision point:** Whether the mechanism by which one report's premise finding argues a scaling law is broken is carried forward as an exact property or as an approximation valid while a condition holds, and whether the difference is material to the argument built on it. No scaling law is asserted and no surface value is named by this record.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, row `PREM-04`. Underlying loci: the verification report's `PC-1d`, verdict `CONFIRMED-NARROWER`, and its per-claim section; the constructed operation and its stabiliser field, located at `pinn/network.py:117-118`, `:122` and `pinn/architecture_spec.py:66` by that verdict's own re-derivation; the finding at `claude-resolution.md:65-76`.

- **Task context:** Phase 54, plan `54-11`, Task 1 — adjudicating the open-book report's `PC-1` against the packet's `M2`, where the invariance is the step that carries the argument.

- **Classification:** **semantic** — it qualifies the mechanism the round's one scaling dispute is argued through, and the qualification bites hardest in the regime the capacity argument is about.

- **Source silence:** The finding asserts positive scale-invariance as a property of the operation. The operation as actually constructed carries a positive stabiliser, so the identity holds exactly only in the limit where that stabiliser vanishes. **No source in the package addresses the difference**: the packet's `M2` quotes the audit's scalar-gain account without reaching the invariance question, the specification's architecture sections fix the skip cadence and the power term and say nothing about their derivative-scale consequence (`RESEARCH-CONTEXT-MASTER.md:311` records exactly that silence), and neither returned report distinguishes the exact identity from its stabilised form. Live code is not a grounding source for a spec decision on this project, which is why the locus is cited as the object the finding describes rather than as authority.

- **Mathematical / engineering grounding:** The structural half of the finding re-derives more strongly than it was claimed: the first hidden layer is an odd skip block, the stack contains exactly six of them, and the power term is a locked specification field rather than an assumption. The narrowing is in the invariance clause. A layer normalization carrying a positive stabiliser in its denominator satisfies the amplitude-invariance identity only to the extent that the squared pre-activation scale dominates the stabiliser; for any positive stabiliser it is an approximation whose accuracy degrades precisely as the pre-activation scale collapses. That matters because the invariance is the **mechanism** by which the finding argues the naive power law fails: an approximate invariance still breaks the law, so the finding's direction survives intact, but "exact" and "accurate while a condition holds" are different premises. The condition weakens exactly in the small-amplitude regime that a large reduction of the initialization scale would enter — which is the regime the whole capacity argument is about. It therefore interacts with the round's one scaling-law disagreement rather than standing apart from it, and the two are recorded as separate decisions because their resolutions differ.

- **Agent was tempted to:** Record the finding as sharpened on the structural half and let the invariance clause pass, since the finding's direction survives either way. That would have let an exact-sounding premise travel into a consolidation whose capacity arithmetic is computed in the regime where the premise is weakest.

- **What the user needs to decide:** How the qualified mechanism travels. At the governance level: (A) the narrowing is recorded and carried into any consolidation that cites the mechanism; (B) the round is asked to re-state the clause; (C) the difference is judged immaterial and recorded as such, with a reason that addresses the small-amplitude regime; (D) it is folded into the scaling-law dispute and settled with it. **Granularity:** recorded separately from `GAP-54-04` because the two have different resolutions — one qualifies a mechanism, the other decides whether a dispute blocks; the owner may merge them or fold either into `GAP-54-01` (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **MEDIUM** — it qualifies a mechanism rather than a conclusion, and the mechanism is the one the round's single physics dispute is argued through.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option A, 2026-09-04.** Carry the
  finite-stabilizer qualification everywhere the LayerNorm mechanism is cited:
  positive-scale invariance is approximate while activation variance dominates
  the stabilizer and exact only in the zero-stabilizer limit. It is not used as a
  quantitative scaling law for the ratified recipe.

## GAP-54-09 — A headline derived figure is bounded at one end by a threshold the round stipulates and no source fixes

- **Decision point:** Whether a derived window figure that the round presents beside a fully repository-grounded traversal may be cited on the same footing, given that one of its two edges is a threshold the report stipulates as a judgement and that no source fixes. The stipulated quantity is located and deliberately not printed here; no value is proposed, defaulted or ranked.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, the candidate list entry `C-05` and the `UNDERSTANDING-TEST` row for it. Underlying loci: the verification report's `R-06`, verdict `CONFIRMED-NARROWER`, and its per-claim section; the report's own confidence cell, which concedes the edge is a judgement call; `CC-1`'s note that the specification's stage-transition thresholds are recorded as provisional pending a future calibration.

- **Task context:** Phase 54, plan `54-11`, Task 2 — assembling the candidate list from the verification report's proposed-and-not-filed rows and testing each for grounding.

- **Classification:** **semantic** — it governs whether a prominent capacity figure may be cited as evidence, and the capacity accounting is what a per-surface disposition is measured against.

- **Source silence:** The report supplies the edge as a judgement and its own confidence cell says so in as many words. **Nothing in the package fixes it**, and **no repository fact bears on it**: the verification report re-derived both arithmetic results exactly and could ground only the other figure's two endpoints. The specification's own stage-transition section, which anchors the comparison's other side, states in its own text that all its numeric thresholds are provisional pending a future calibration — so even the grounded endpoint is grounded in a value the spec marks as not yet calibrated, which is recorded here rather than glossed.

- **Mathematical / engineering grounding:** The round presents two decade-counts as a single comparison. One is bounded at both ends by quantities re-derived here from the tree — the retained log's median first residual at one end and the specification's physics-residual threshold at the other, both content-resolved — so it is a repository-grounded statement about how far the residual must travel. The other is bounded at one end by the implementation's own floor, re-derived, and at the other by a stipulated notion of when a causal weight is still informative, which no source fixes. Because both are logarithms of ratios, the derived width moves decade for decade as the stipulated edge moves: the verification report records the width at two neighbouring choices of that edge and they differ by a decade each way. The two numbers therefore do **not** carry the same evidential status even though the round presents them as one comparison, and the comparison is exactly what the per-surface capacity accounting reads. A figure whose width is set by a judgement, cited beside one whose width is set by measurements, invites a reader to treat both as measured.

- **Agent was tempted to:** Record the figure as plainly confirmed, because both arithmetic results reproduce exactly. That would have let a stipulation travel into a consolidation as a repository fact, which is the specific failure the split verdict exists to prevent.

- **What the user needs to decide:** How the figure may be cited. At the governance level, with the stipulated quantity located rather than named: (A) the figure travels with its stipulation recorded, as the verification report records it; (B) the stipulation is itself routed for disposition before the figure informs anything; (C) the figure is cited only in the direction the fully-grounded number supports; (D) the question is folded into checkpoint ② with the capacity accounting it feeds. **Granularity:** recorded separately because it governs how a figure may be cited rather than what any surface should be; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2).

- **Confidence of impact:** **MEDIUM** — it governs how a prominent figure may be cited, not what any surface should become; the figure is read by the capacity accounting a ratification would rest on.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option C, 2026-09-04.** Do not cite the
  stipulated 3.24-decade informative-window width as a measured fact or use it to
  set a value. Retain only the fully grounded directional conclusion that a fixed
  unnormalized exponential has finite dynamic range, and use the hard
  `log(2)` front threshold and dtype-derived normal-floor boundary where exact
  thresholds are needed.

## GAP-54-10 — A declared evidence label and the evidence's actual provenance disagree, in a taxonomy that makes the label decide entitlement

- **Decision point:** What a receiving pass does when a returned report's declared evidence label and the evidence's actual provenance disagree, given that the round's four-class independence taxonomy reads a claim's class off its label and reads the corroboration entitlement off the class.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, row `PREM-15` and the candidate entry `C-02`. Underlying loci: the open-book report's declared label vocabulary at `claude-resolution.md:35-38` and the labelled sentence at `:271-273`; the four-class taxonomy and the `LEDGER-PREFIX-CONTRACT` in `.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md`; the verification report's `PC-9a`, verdict `CONFIRMED-NARROWER`.

- **Task context:** Phase 54, plan `54-11`, Task 2 — reconciling the verification report's proposed candidate rows against the adjudication table.

- **Classification:** **process-artifact schema** — it asks how this pass's own machinery behaves in a case its schema does not cover, which the STOP protocol reserves to the owner rather than to the agent that runs the machinery.

- **Source silence:** The report declares its label vocabulary in its own opening and applies the package-derived label to a sentence that appears in **none** of the three attachments. **Nothing says what to do when a declared label and the provenance disagree**: not the report, not the intake record that fixed the taxonomy, not the identifier contract that governs how the two reports' vocabularies are handled side by side, not the ERW runbook, and not this project's own conventions. The intake record is explicit that neither vocabulary is translated into the other, which forecloses the obvious repair without supplying an alternative.

- **Mathematical / engineering grounding:** The taxonomy the intake record fixed makes agreement between the two reports mean different things in different classes: in one it is independent corroboration, in another it is evidence that the attachment relayed the tree faithfully and explicitly **not** a second reading of the tree. That entitlement is read off the claim's class, and the class is read off the declared label. A mislabelled row is therefore consumed under the wrong entitlement, and once the label is trusted the error is **invisible**: a consolidated statement would claim two-agent support for something one agent read in a file the other never held, and a reader checking the entitlement column would find it consistent. Here the divergence happens to run in the benign direction — the sentence was read in the live tree, which is the stronger provenance — but a rule that only works when the error runs one way is not a rule, and the taxonomy exists precisely because the overconfident direction is the one a careless consolidation takes.

- **Agent was tempted to:** Silently re-label the row to the class the evidence supports. That is a repair to a returned report's own declared vocabulary, made by the pass that consumes it, with no record that the report said something different.

- **What the user needs to decide:** What the receiving convention is. At the governance level: (A) the ledger records both the declared label and the provenance and downstream consumes the provenance, which is what the verification report does pending instruction; (B) the round is asked to re-label; (C) the divergence is recorded and the row is excluded from any cross-report agreement claim; (D) a standing convention is written for future rounds and applied to this one. **Granularity:** recorded separately because it is a question about this pass's own schema rather than about the recalibration; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2), though that record's decision point does not naturally contain it.

- **Confidence of impact:** **MEDIUM** — it affects one row's entitlement in a taxonomy built precisely to stop that entitlement being assumed, and it sets the convention every later row is read under.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option A, 2026-09-04.** Record both a
  returned report's declared evidence label and the independently established
  provenance; downstream entitlement follows the established provenance when
  they disagree. The Rule-19 verification report's treatment of this round is
  adopted. No returned report is rewritten.

## GAP-54-11 — The closed-book verification burden's provenance-bucket vocabulary has no value for a reproduction supplied whole

- **Decision point:** Whether the closed-book receiving burden's second provenance bucket covers a citation whose line number is accounted for by a reproduction that declares its range by reproducing a document in full, or by an attachment that **is** the cited file — or whether such citations belong in the third bucket, or in a fourth the vocabulary does not yet have.

- **Where in artifact:** `54-PREMISE-ADJUDICATION.md`, candidate entry `C-07` and its `UNDERSTANDING-TEST` row. Underlying loci: the verification report's `ANCHOR-PROVENANCE-TRIAGE`, the reading paragraph in its second bucket, and its proposed-and-not-filed candidate row on this question; the burden as derived under `BURDEN-CLOSED-BOOK` in `.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md`.

- **Task context:** Phase 54, plan `54-11`, Task 2 — assembling the candidate list from the verification report's proposed rows and routing those in surfacing classes.

- **Classification:** **process-artifact schema** — the bucket vocabulary is this pass's own instrument, and how it is read changes the counts every later document quotes from it.

- **Source silence:** The burden's second bucket is defined in terms of a range that a verbatim block in an attachment **declares** for a file. The ERW runbook does not contemplate a closed-book round whose uploads carry repository anchors **at all** — its access-mode comparison sets the closed-book receiving burden to "none beyond normal channel protocol", which is why the burden had to be derived rather than inherited — and neither the derived burden nor the plan that derived it says whether a declaration made by reproduction rather than by numeral satisfies the definition.

- **Mathematical / engineering grounding:** The three buckets partition every cited anchor by whether the attachments account for its line number: literally, by a checkable offset, or not at all. The third bucket's stated meaning is that the number "came from somewhere the attachments do not account for", and its purpose is to concentrate attention on genuinely unexplained citations. For both of the forms at issue the attachments account for the number **exactly** — by a fixed, checkable offset in one case and by an offset of zero in the other — so assigning them to the third bucket would report unaccounted-for anchors where none exists and would dilute the one bucket whose whole value is that it is normally empty. Assigning them to the second requires reading "declares a range" to include a declaration made by reproduction. **Nothing downstream turns on the choice in terms of verdicts** — every anchor is content-resolved against the pinned tree either way and no claim verdict depends on the bucket — but the published bucket counts do, and those counts are what a later document quotes as the round's provenance result. The verification report records the alternative counts under the strict-literal reading; they are not restated here because this pass did not derive them independently.

- **Agent was tempted to:** Apply the second-bucket reading silently, since it changes no verdict. The verification report recorded the same temptation and declined for the same reason; this pass does not overturn that and adds nothing to it.

- **What the user needs to decide:** Which reading the vocabulary carries. At the governance level: (A) the reading applied in the verification report is adopted and the burden's wording is amended to say so; (B) the strict-literal reading is adopted and the published counts are restated accordingly, as the verification report's own candidate row records them; (C) the bucket vocabulary gains a fourth value for a reproduction supplied whole. **Granularity:** recorded separately because it is a question about this pass's own instrument rather than about the recalibration; the owner may fold it into `GAP-54-01` (54-CONTEXT.md Open Item 2), though that record's decision point does not naturally contain it.

- **Confidence of impact:** **MEDIUM** — it changes published counts a later document quotes and changes no verdict.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** **Owner-authorized option A, 2026-09-04.** A document
  reproduced whole, or an attachment that is the cited file, is accounted-for
  reconstructed coverage with an offset of zero and belongs in bucket 2. The
  receiving burden's wording is read to include a range declared by whole-file
  reproduction; the verification report's published counts therefore stand.
