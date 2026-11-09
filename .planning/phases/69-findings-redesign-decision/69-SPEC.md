# Phase 69: Findings & Redesign Decision specification

**Created:** 2026-11-08
**Ambiguity score:** 0.060, gate at or below 0.20
**Requirements:** 3 locked, VERD-01, VERD-02 and VER-23

## Goal

Give the owner an evidence-backed account of what v2.5 established about
v2.4's failure, including what remains open, and a decision packet for the
v2.6 direction and whether to commission trainex-r5.

## Background

Phases 65 through 68 have completed their registered work. Phase 65
reproduced the adjacent-time hidden-state association on the seven v2.4
networks. That reproduction establishes neither information loss nor a
causal mechanism. Phase 66's smaller-network control achieved Tier 1 on
the main case, a second system and a second seed. Its depth, width and
first-layer frequency all changed, so it is not a depth-only result.

Phase 67 completed the depth, rate, input and window ladders. The rate
1e-3 contrast confirmed worsening relative to the 1e-4 control. Other
contrasts remained unsettled or ambiguous under their registered rules.
Importantly, the locked 12-layer, width-256, first-frequency-30 control
at constant-rate Adam 1e-4 achieved settled Tier 1 position fits: E =
0.040691019043637484 on 1632/42, 0.09549573839491703 on 851/42 and
0.03491785615016659 on 1632/41. These results are in
`.planning/phases/67-design-settings-ladders/evidence/exp03/review.json`.
They do not establish physics accuracy or new-IC generalization.

The historical v2.4 data-only runs used a cosine schedule starting at
1e-3, clipping and a subsequent polish. The successful diagnostic control
used constant-rate Adam 1e-4 without clipping or polish. This is an
observed recipe difference to reconcile, not a controlled attribution of
the historical failure to any one setting. Other relevant differences
and equivalences still need checking against the committed sources.

Phase 68's known-answer audit established a finite-difference measurement
problem and the inability of energy conservation alone to establish
position accuracy. The owner selected C-7 A, autograd velocities, and
left C-2, C-4, C-5 and C-6 open for separate discussion. Amendments are
routed to v2.6. The measurement defect does not explain a network learning
mean positions in a data-only fit.

The missing deliverable is the milestone-wide synthesis, followed by the
owner's closing choices and a fresh traceability check.

### Owner direction

After asking whether additional diagnostics would be useful, the owner
accepted the recommendation to keep Phase 68 closed, proceed with Phase
69, compare the existing failed and successful recipes first, and consider
a focused diagnostic only if the remaining uncertainty could change the
redesign decision. The reply on 2026-11-08 was:

```owner-quote
Okay, let's proceed with your recommendation then and continue the discussion for Phase 69.
```

This authorizes the evidence-first preparation and qualified findings. It
does not choose the final v2.6 design, commission trainex-r5, authorize a
new training campaign or settle the deferred pass bars. Technical review
proceeds under PROJECT.md's standing 2026-10-28 delegation.

## Requirements

1. **VERD-01:** Produce a one-page, plain-language findings page that classifies each suspect and the probe's lead as confirmed, refuted or open from committed evidence, reconciles the failed v2.4 recipe with the successful locked-network controls, and links the measured compute cost and every SCOPE-49 disposition.
   - Current: Committed phase findings, predictions, run records, reviews,
     owner rulings and the yardstick audit exist. They have not been
     synthesized into the Phase 69 findings page. No single setting has
     been established as the cause of v2.4's failure.
   - Target: The main page states the answer and its limits in plain
     language, with each suspect and the original probe lead accounted
     for. Linked detail places the observed numbers beside the committed
     predictions, separates the training-settings and physics-term halves
     of the pipeline suspect, and compares the failed v2.4 recipe with
     the successful locked-network controls. It reports supported redesign
     directions as recommendations, the measured v2.5 machine hours with
     their accounting basis, and all SCOPE-49 proposals and dispositions.
   - Acceptance: Every empirical claim resolves to an identified committed
     run record or table and its relevant prediction. The reconciliation
     distinguishes verified differences, verified equivalences and open
     comparability questions; it does not treat different recipes as an
     isolated-factor experiment. Scientific uncertainty is explicitly open.
     Missing or conflicting evidence is identified and does not become an
     invented result. Cost subtotals are reproducible without double
     counting, with missing durations and mixed measurement bases stated.
     The physics half remains open unless cited evidence actually tests it.

2. **VERD-02:** After the findings, present evidence-backed v2.6 directions and the conditional need for a focused diagnostic, then record the owner's redesign and trainex-r5 decisions verbatim, with any choice left open explicitly recorded.
   - Current: The roadmap reserves the closing decision to the owner.
     The accepted recommendation fixes the evidence-first sequence but
     selects no final redesign and commissions no external research.
   - Target: A decision packet explains the practical consequences of the
     supported directions. It first uses the recipe reconciliation, then
     states whether an unresolved question could change the recommendation.
     If a new diagnostic is recommended, it identifies that question, how
     different answers would affect the decision and the required scope
     or resource authorization. The owner decides the v2.6 direction and
     whether to commission trainex-r5, including its question.
   - Acceptance: The completed findings precede the owner checkpoint.
     The reply is preserved verbatim, tied to the evidence presented,
     and each reserved choice has an answer or an explicit open status.
     A missing reply is pending, not agreement. The packet preserves
     order A: redesign research is the normal trainex-r5 route; diagnosis
     research is conditional on the original lead being refuted, not
     merely on one rate contrast being labelled refuted. Further work
     remains a proposal until the applicable owner instruction is recorded.

3. **VER-23:** Re-verify at phase close that every final v2.5 requirement maps to exactly one phase, with no orphan or duplicate mapping and with any approved SCOPE-49 change included.
   - Current: REQUIREMENTS.md maps 13 requirements to Phases 65 through
     69. That creation-time mapping is not the required closing check.
   - Target: A closing check derives the final requirement IDs from the
     active requirements and compares them with the final phase mappings,
     accounting for any owner-approved additions or routing changes.
   - Acceptance: The requirement-ID set equals the mapping-ID set; every
     ID has exactly one mapped phase; every referenced phase exists; and
     the check reports the final counts, orphan IDs and duplicate IDs.
     Requirement satisfaction and phase mapping remain separate facts.
     A stale hardcoded count or an empty inventory cannot pass.

## Boundaries

**In scope:**

- The one-page findings, with linked supporting evidence and exact sources.
- Read-only reconciliation of existing v2.4 and v2.5 records and the code
  revisions those records identify, including successful locked controls.
- Measured v2.5 compute accounting and the SCOPE-49 disposition history.
- Evidence-backed options, a conditional diagnostic recommendation and
  the owner's closing decision record, including explicit open choices.
- Final requirement-to-phase traceability and the v2.6 handoff.

**Out of scope:**

- New training, retries, continuation of frozen arms, or another general
  sweep. A focused follow-up requires its own prospective proposal,
  authorization, budget and pre-registration before execution.
- Architectural redesign, rebuilding, physics-pipeline repairs, framework
  amendments or moving locked values. These belong to authorized v2.6 work.
- Reopening Phase 68's C-7 ruling or deciding its deferred pass bars by
  inference. C-2 and C-4 through C-6 remain open until owner instruction.
- Assembling or conducting trainex-r5. This phase records whether and why
  the owner commissions it; any package is subsequent work.
- A graded run, new validation/test access or spending the preserved
  held-out evaluation. SCOPE-45 remains in force.

## Constraints

- Preserve SCOPE-45 through SCOPE-49 and all historical prediction pages,
  reading rules, evidence, scorecard values and panel definitions.
- Report the registered labels from exact evidence. Display rounding must
  not turn an unsettled or ambiguous contrast into a confirming result.
- Keep the original probe association, the rate-improvement hypothesis,
  observed recipe differences and a historical causal explanation distinct.
- Use empirical implementation records to characterize what actually ran.
  Do not use live code to invent a framework-spec decision or silently
  treat today's implementation as the historical code revision.
- Label single-orbit data-only fitting separately from physics learning,
  conservation, full-Stage-0 performance and new-IC generalization.
- Carry forward the known physics-pipeline items by name: the single-anchor
  physics calculation, IC reduction over selected slots, IC/physics gradient
  imbalance and unreachable production L-BFGS stage. Do not confuse that
  production-stage finding with the diagnostic polish that v2.4 ran.
- Any proposed new compute remains on this Mac and subject to the existing
  resource and power governance. This specification authorizes no run.

## Acceptance criteria

- [ ] All three suspects and the original probe lead have a cited status;
  the pipeline suspect has separate training-settings and physics entries.
- [ ] Every experiment's prediction, observed numbers, registered reading
  and replication limits are accessible from the concise findings page.
- [ ] The successful locked-network controls are reported alongside the
  historical failures, with recipe differences and unresolved comparability
  limits, rather than a claim that only a smaller network can fit.
- [ ] Existing tier and confirmation labels are preserved at numeric
  boundaries; exact source values remain available behind rounded displays.
- [ ] Repeated numeric values from different cases, seeds, windows or
  measurement routes remain distinct, with those identities visible.
- [ ] An empty confirmation set is reported without inventing a positive
  result; missing or conflicting sources are identified rather than filled in.
- [ ] The findings lead with the plain-language answer, followed by the
  suspect statuses and cited detail, without implying an unregistered ranking.
- [ ] Cost accounting gives reproducible v2.5 subtotals, units, included
  activities, measurement bases and unknown durations, counts each attempt
  once and distinguishes v2.4 context from v2.5 expenditure.
- [ ] Every SCOPE-49 proposal has its actual disposition and authority;
  the EXP-03 continue ruling is not presented as a scope amendment.
- [ ] Evidence revisions are identified by committed paths and revisions
  or digests. An updated packet is not silently substituted for one the
  owner previously answered; prior rulings remain auditable on rerun.
- [ ] Any proposed diagnostic names a remaining decision-relevant question,
  the consequences of its possible answers and the required authorization;
  it is not launched merely because this recommendation was accepted.
- [ ] The owner is presented the findings before the closing checkpoint;
  both the v2.6 direction and trainex-r5 choice/question have a verbatim
  answer or explicit open status. Silence remains pending.
- [ ] Repeated or partial owner replies preserve the original wording;
  a later explicit revision is recorded with its context and does not erase
  an earlier ruling. Technical paraphrases remain separate from quotations.
- [ ] The closing traceability check reports equal, non-empty requirement
  and mapping ID sets, one phase per ID, valid referenced phases and the
  final counts, independent of row order and requirement completion status.
- [ ] If approved requirements or mappings change before close, the
  traceability check is rerun against that final state.
- [ ] The findings MUST NOT claim causality, architectural impossibility,
  physics success or generalization beyond the cited evidence.
- [ ] The findings MUST NOT omit unfavourable or unsettled results or
  present incomplete cost accounting as all machine use.
- [ ] The record MUST NOT turn a recommendation or preparatory approval
  into an owner redesign choice, research commission, run authorization,
  pass-bar change, specification amendment or evaluation spend.

## Edge Coverage

**Coverage:** 14/14 applicable edges resolved, 0 unresolved.

The canonical edge probe ran on the three requirement statements above,
with authored shapes reflecting their text, collection, numeric-reporting
and publication behavior. All 14 proposed rows were considered. Resolution
below is under the owner's standing technical delegation, not an invented
set of owner menu selections. Each row has verification `explicit` through
the acceptance criteria above; no new numerical reading rule is introduced.

| Requirement | Category | Status | Resolution |
|---|---|---|---|
| VERD-01 | boundary | resolved | Inherit exact scorer/review labels at their boundaries; never classify from rounded display values. |
| VERD-01 | adjacency | resolved | Equal numbers do not merge distinct system, seed, window or metric-route identities. |
| VERD-01 | empty | resolved | Empty confirming sets remain empty; missing/conflicting sources are visible and supply no fabricated result. |
| VERD-01 | encoding | resolved | Keep exact source values, IDs, units and revisions accessible; Unicode mathematical notation changes no evidence value. |
| VERD-01 | ordering | resolved | Plain-language answer first, then statuses and linked detail; no unregistered performance ranking. |
| VERD-01 | precision | resolved | Re-derive cost sums from recorded values, label incompatible bases and unknown durations, and round only for display. |
| VERD-01 | concurrency | resolved | Cite a committed evidence revision; a changed packet cannot silently inherit a prior answer. Recheck final sources before publication. |
| VERD-02 | empty | resolved | Missing or partial replies leave the unanswered choice pending or explicitly open; silence is not approval. |
| VERD-02 | encoding | resolved | Preserve the owner's reply verbatim; keep any technical interpretation separate. |
| VERD-02 | idempotency | resolved | Rerunning evidence checks does not mint a new owner answer or erase prior rulings. |
| VERD-02 | concurrency | resolved | Tie each ruling to the evidence presented and preserve context when the owner explicitly revises a choice. |
| VER-23 | adjacency | resolved | Detect duplicate requirement IDs or multiple mapped phases; never deduplicate silently to obtain coverage. |
| VER-23 | empty | resolved | Empty inventories, unmapped IDs and non-existent phases fail the closing check. |
| VER-23 | ordering | resolved | Compare ID sets and multiplicity independently of Markdown row order; rerun after approved changes. |

## Prohibitions

**Coverage:** 3/3 applicable prohibitions resolved, 0 unresolved.

The recall pass considered causal overstatement, selective reporting,
scope inflation, invented authority and evidence/accounting omissions.
Routine file handling and mapping correctness remain acceptance/edge
checks. The three retained prohibitions concern scientific transparency
and the owner's decision authority. They require judgment review rather
than fabricated mechanical test descriptors.

| Prohibition | Requirement | Status | Verification |
|---|---|---|---|
| MUST NOT strengthen association or a limited fit into an unsupported causal, capacity, physics or generalization claim. | VERD-01 | resolved | judgment: inspect each conclusion against its prediction, run/table and stated scope. |
| MUST NOT hide unfavourable/unsettled evidence or describe incomplete recorded costs as total machine use. | VERD-01 | resolved | judgment: compare the synthesis with all registered experiment reviews and the accounting coverage. |
| MUST NOT manufacture an owner decision or work authorization from silence, a recommendation or this preparatory approval. | VERD-02 | resolved | judgment: compare every reserved action with the verbatim instruction and the evidence it answered. |

## Ambiguity report

| Dimension | Score | Minimum | Status | Basis |
|---|---|---|---|---|
| Goal clarity | 0.95 | 0.75 | met | Qualified findings and a closing decision packet, with no invented single cause. |
| Boundary clarity | 0.95 | 0.70 | met | Existing-record reconciliation now; follow-up launches and redesign require separate authority. |
| Constraint clarity | 0.95 | 0.65 | met | Existing scientific, split, resource and owner-checkpoint governance carries forward. |
| Acceptance criteria | 0.90 | 0.70 | met | Sources, uncertainty, costs, owner choices and final mapping have explicit checks. |
| Ambiguity | 0.060 | at most 0.20 | met | 1 - (0.35 x 0.95 + 0.25 x 0.95 + 0.20 x 0.95 + 0.20 x 0.90). |

## Interview log

| Round | Perspective | Question or clarification | Decision locked |
|---|---|---|---|
| Initial assessment | Researcher | What is already specified by the roadmap and requirements? | Scores 0.85/0.90/0.95/0.75, ambiguity 0.1375; no artifact written before the owner answered. |
| 1 | Researcher and boundary keeper | Should the close require stronger causal confirmation? The owner asked for the agent's assessment of the value of further diagnostics. | Agent recommended closing Phase 68, proceeding with qualified Phase 69 findings and reconciling the failed/successful recipes before proposing more compute. |
| 1, follow-up | Simplifier and failure analyst | Does useful evidence remain available without another broad campaign? | Owner accepted the recommendation verbatim above; further diagnostics are conditional and not pre-authorized. Updated scores 0.95/0.95/0.95/0.90, ambiguity 0.060. |
| Completeness probes | Technical delegation | Resolve the 14 edge proposals and three scientific/authority prohibitions. | Explicit acceptance checks and judgment reviews above; no additional owner scientific interview or numeric default. |

## Grounding

- `.planning/ROADMAP.md`, diagnosis discipline and Phase 69.
- `.planning/REQUIREMENTS.md`, VERD-01, VERD-02, VER-23 and SCOPE-45 through SCOPE-49.
- `.planning/PROJECT.md`, Current Milestone and Context, standing delegation.
- `.planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md`.
- `.planning/phases/66-small-network-control/66-RESULT.md`.
- `.planning/phases/67-design-settings-ladders/67-FINDINGS.md` and `67-CLOSEOUT.md`.
- `.planning/phases/67-design-settings-ladders/evidence/exp03/review.json`.
- `.planning/phases/60-single-system-learnability/evidence/arms/r1-1632/record.json`.
- `.planning/phases/68-yardstick/68-AUDIT.md` and `68-CHECKPOINT-2-RULING.md`.
- Owner instruction in this session, 2026-11-08, quoted above.

---

*Phase: 69-findings-redesign-decision*
*Next step: discuss-phase implementation decisions, then research and planning.*
