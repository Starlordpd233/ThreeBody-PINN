# Phase 69 closing decision

Prepared 2026-11-08. Owner response pending.

The locked architecture reached settled Tier 1 position fits on both tested
systems and a second seed under the diagnostic recipe. In the rate ladder, the
constant `1e-3` arm performed worse than the constant `1e-4` control in all
three cases. The historical failure involved a different schedule, clipping,
polish and update budget. A single historical cause remains open.
[Findings and supporting evidence](69-FINDINGS.md)

## v2.6 direction

**A. Keep the current architecture as the control and address training and
physics first (recommended).** Use the successful supervised fit as the
reference point for a staged redesign. In v2.6, confirm the supervised rung,
then test whether the repaired pipeline can learn one orbit from physics
before expanding to the 16-system family or full Stage 0. Preserve the
comparison points and scorecard. This keeps a demonstrated position fit
available while testing the part of the pipeline the diagnostics left open.
The diagnostic recipe is evidence for the control, not a production setting
decision. [Matched records and recipe comparison](69-EVIDENCE.md#recipe-comparability)

**B. Prioritize a representation redesign.** Compare a proposed architecture
with the successful locked control under the same data, optimizer policy,
budget and scoring. This may be worthwhile if the goal requires a capability
the existing architecture cannot demonstrate. Current depth, time-input and
window results leave that case open. A larger redesign adds a comparison to
the physics-pipeline work. [Registered ladder outcomes](69-EVIDENCE.md#how-to-read-the-ladders)

**Leave the direction open.** Record that disposition and retain both options
for later planning.

## Value of another diagnostic

The existing results are sufficient to recommend A and close the v2.5 evidence
synthesis. A repeat of the ladders or another measurement of the historical
hidden-state association would leave the main choice unchanged. The next
decision-changing question is whether the current architecture can reproduce
the supervised fit in the repaired pipeline and carry that progress into the
single-orbit physics rung. If the supervised control transfers and the physics
rung fails, inspect the physics objective and optimization before attributing
the failure to architecture. If the supervised control fails to transfer,
first isolate the changed recipe or data path. A matched representation
comparison becomes useful if the remaining failure could plausibly be relieved
by a change to the model while the pipeline and recipe are held fixed.

A focused historical comparison could isolate a recipe variable if the owner
makes that distinction a condition for choosing a redesign. It would hold the
data window, model, initial state, loss, budget, score route and endpoint rule
fixed, varying only the specific recipe element at issue. A result that
separates the recipes would support prioritizing that element. An inconclusive
result would leave the historical mechanism open. That comparison would need a
separate scope and resource decision, a prospective prediction and reading
rule, and a measured Mac budget. This packet recommends no new v2.5 experiment.
[Existing comparison and limits](69-EVIDENCE.md#recipe-comparability)

## trainex-r5 commission

**Commission a focused redesign review (recommended if choosing A).** Proposed
question:

> How should v2.6 retain the demonstrated single-orbit position fit while
> repairing the physics training and energy measurement, and what evidence
> should trigger a representation change before expanding to the 16-system
> family?

The deliverable would be a source-grounded design and discriminating checks
for the next rungs. Order A routes trainex-r5 to redesign research. DIAG-09
retained the original lead, while EXP-03 refuted a distinct rate-improvement
hypothesis within its ladder. [Milestone governance](../../PROJECT.md) · [Probe and rate results](69-EVIDENCE.md)

**Defer, decline or leave open.** Defer the commission if the owner wants the
v2.6 planning and pipeline review to establish a narrower research question
first. The v2.6 direction can be recorded separately.

| Reserved item | Status before presentation | Owner response needed |
|---|---|---|
| v2.6 direction | Pending | A, B, a different direction, or explicitly open |
| trainex-r5 commission | Pending | Commission, defer, decline, or explicitly open |
| trainex-r5 question | Pending, conditional on commission | Adopt the proposed question, give a different question, or explicitly leave it open |
| New diagnostic scope or resources | No new request in this packet | A subsequent proposal would require its own decision |

The 2026-11-08 proceed instruction approved comparison of the existing records
before deciding on further diagnostics. The two closing choices are reserved
for the owner after this evidence is presented. [Phase 69 scope](69-SPEC.md) · [VERD-02](../../REQUIREMENTS.md#findings-and-decision-verd)

## Obligations carried to v2.6

- C-7 A routes autograd velocities to the validation gate and evaluator and a
  clarification to `pinn_architecture.md` §10.6. GAP-59-08 is closed. The
  constant predictor still shows why energy conservation alone is insufficient.
- C-2 and C-4 through C-6 remain open for separate owner discussion. C-11
  routes the `ctl_instruction.md` evaluation-text rewrite to v2.6.
- The named physics-pipeline defects are the single-anchor physics calculation,
  IC loss reduction over selected slots, the recorded IC/physics gradient
  imbalance and the unreachable production L-BFGS stage. The production
  stage is distinct from the diagnostic polish executed in Phase 60.
- Stage 1+ and PLAT-01 through PLAT-07 remain blocked. The preserved held-out
  evaluation remains unspent.

[Phase 68 ruling](../68-yardstick/68-CHECKPOINT-2-RULING.md) · [Future requirements](../../REQUIREMENTS.md#future-requirements-v26-and-beyond) · [Historical recipe evidence](69-EVIDENCE.md#recipe-comparability)

## Packet identity

The evidence inventory was committed at `0f53ab64061a1998e2df2a082149f087ee6c4b03`.
The closing record will bind the owner’s words to this packet’s publication
revision and SHA-256 and to the component digests below.

| Component | SHA-256 |
|---|---|
| [69-FINDINGS.md](69-FINDINGS.md) | `6f923eae704b387d2c0a6dc4da0d37b41b90aca052541826a5496edb2afa99ad` |
| [69-EVIDENCE.md](69-EVIDENCE.md) | `b4a7cce32e949829710dca42642f090cf64f9c3f8de3b3bce422e7aaf8afcdd0` |
| [69-ACCOUNTING.md](69-ACCOUNTING.md) | `bc6cadcd20cb31a097a192cdd12f7d0508bda706824166cff244793eb8c314c8` |
| [evidence/69-evidence.json](evidence/69-evidence.json) | `0c54c45997665b19470b8a14a672d640ae28fe851b3542cbfa782c74345957f8` |

## Technical judgment review, 2026-11-08

| SPEC prohibition | Review of the packet |
|---|---|
| Scientific overclaim | Passed on judgment. Checked the matched historical records and the three locked controls against the registered endpoints. The findings limit learnability to supervised positions on those orbits, preserve the historical causal question and separate the original DIAG-09 association from the rate-improvement hypothesis. The yardstick comparison and control energy drift leave physics learning and generalization open. [Evidence](69-EVIDENCE.md) |
| Omission of adverse results or incomplete cost | Passed on judgment. The tables retain every registered arm and contrast, including empty confirmed sets, worse scores and unsettled or ambiguous endpoints. The case keys correct the older repeat-column error. The cost report distinguishes attempt and fit-wall bases, includes the yardstick capture and exposes unknown durations. [Evidence](69-EVIDENCE.md) · [Accounting](69-ACCOUNTING.md) |
| Inferred owner authority | Passed on judgment for the prepared packet. The direction and trainex-r5 commission/question remain pending. The Phase 68 ruling and EXP-03 continuation retain their original scope. The closing reply must come through Plan 69-03’s blocking human checkpoint. [Scope](69-SPEC.md) · [Closing plan](69-03-PLAN.md) |

The judgment review is distinct from the verifier’s reconstruction of values
and the hashes that identify these files. This packet is ready for the owner
decision.
