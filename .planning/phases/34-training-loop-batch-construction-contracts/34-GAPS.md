# Phase 34 Gap Register

STOP-protocol gaps surfaced during Phase 34 (Training-Loop & Batch-Construction Contracts).
Milestone index: `.planning/milestones/v1.6-GAPS.md`.

---

## GAP-34-01 - Batch edge-case policy for replay/lookahead batch construction

- **Decision point:** What deterministic policy should govern the batch edge cases for the LOOP-01 replay/lookahead contract: (a) final-stage behavior when `has_stage(k+1)` is false, (b) behavior when the next-stage lookahead pool has fewer than 16 eligible trajectories, and (c) the replacement / reservoir policy for the replay and lookahead sets?
- **Where in artifact:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, section **Mini-Batch Construction with Lookahead Sampling** (Phase 34 LOOP-01 contract).
- **Task context:** Plan 34-03 Task 1, transcribing the LOOP-01 replay/lookahead batch-construction contract.
- **Classification:** **semantic** — the selected edge policy changes the effective batch distribution, curriculum convergence, and whether the final stage trains correctly.
- **Source silence:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:36-39` (§1.4 B-07 `modified`) flags these edge cases as "must be made deterministic" but gives no policy; `03-final-resolution.md:223` (GAP-05) routes the decision to Phase 34 LOOP-01 but does not select a policy; `.planning/phases/34-training-loop-batch-construction-contracts/evidence/b-07-replay-lookahead-batching.md` lists the three owner-pending items in its "Locked Convention or Owner Route" section. No source selects a final-stage, undersized-pool, or replacement policy.
- **Mathematical / engineering grounding:** The 240/16 replay/lookahead split is a structural curriculum-learning invariant. The edge policies affect (1) whether the final stage can train at all without a look-ahead set, (2) whether an undersized next-stage pool changes the effective batch size or triggers substitution/sampling-with-replacement, and (3) whether trajectories are reused within or across batches, which changes the effective data distribution and optimizer convergence properties. These are not derivable from first principles or from the current dataset facts without admitted-set EDA.
- **Agent was tempted to:** fill the gap with common defaults: reuse the replay set for the final stage, pad an undersized lookahead pool by sampling with replacement, and sample replay without replacement across the epoch. That would silently convert a source-silent owner decision into a locked contract.
- **What the user needs to decide:**
  - **A.** Final stage trains on replay only; undersized lookahead is padded by sampling with replacement from the available pool; replay is sampled without replacement across the epoch.
  - **B.** Final stage trains on replay only; undersized lookahead reduces the batch size (or is padded from replay); replay uses a reservoir sampler.
  - **C.** Another explicit deterministic policy supplied by the owner.
- **Confidence of impact:** **HIGH** — the choice affects batch distribution, curriculum convergence, and whether the final stage trains correctly.
- **Status:** **OPEN**
- **Resolution note:**

---

*Phase: 34-training-loop-batch-construction-contracts*
*Register opened: 2026-06-25*
