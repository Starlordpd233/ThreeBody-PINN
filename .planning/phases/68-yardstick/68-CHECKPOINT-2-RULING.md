---
phase: 68-yardstick
milestone: v2.5
created: 2026-11-08
status: ratified
authority: owner, checkpoint 2 (YARD-02, YARD-03)
audit_commit: 605d7ad6e10eb96ebfca09f19db1d6a629636254
audit_sha256: 4b82c21918ba578c9f889cc21f1a93494d12aaa60940b2dac5ef073318922fe4
packet_commit: 20c1964ba0f7dbf174c356f9185a5390ebc1e3fa
gap_ref: .planning/phases/59-read-only-baseline-scorecard/59-GAPS.md#gap-59-08--the-production-energy-check-fails-even-a-perfect-answer-owner-routed
---

# Phase 68 — Owner Checkpoint 2 Ruling

## 1. Authority and Boundary

This document records the project owner's binding ruling at Checkpoint 2 of Phase 68 ("Yardstick"). It directly resolves **C-7** (closing `GAP-59-08` with instruction) and records the owner's explicit disposition on companion rows **C-2, C-4, C-5, and C-6**.

- **Authority:** The project owner (under YARD-02 and YARD-03 governance).
- **Audit Grounding:** Committed Phase 68 yardstick audit evidence `605d7ad6e10eb96ebfca09f19db1d6a629636254` (`SHA-256: 4b82c21918...`), which established that numerical ground truth (Brutus) fails the production finite-difference gate ($\text{eps}_H \approx 0.0238$ on gold, $0.379$ on base) while constant predictors pass ($\text{eps}_H = 0.0$).
- **Packet Reference:** Committed decision packet `20c1964ba0f7dbf174c356f9185a5390ebc1e3fa` in [`.planning/phases/68-yardstick/68-CHECKPOINT-2.md`](file://<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/68-yardstick/68-CHECKPOINT-2.md).
- **Gap Backlink:** Resolves [GAP-59-08](file://<home>/Desktop/3_body_problem/.worktrees/trainex/.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md) in the Phase 59 Gap Register.
- **Scope Boundary:** Phase 68 does not edit framework specifications, train models, or spend the preserved evaluation. Required specification amendments and code modifications are routed to milestone `v2.6`.

---

## 2. The Owner's Verbatim Reply

```owner-quote
C-7: A. Leave C-2, C-4, C-5 and C-6 open for separate discussion.
```

---

## 3. Recorded Answers and Practical Consequences

| ID | Item | Owner Ruling | Status | Disposition & Practical Consequences |
|---|---|:---:|:---:|---|
| **C-7** | Velocity measurement for energy check (`GAP-59-08`) | **Option A** | **RESOLVED-WITH-INSTRUCTION** | **Use autograd velocities in evaluator and validation gate.**<br>• Eliminates the $O(\Delta t^2)$ finite-difference truncation error that artificially failed Brutus ground truth.<br>• Aligns validation energy checks with the continuous derivative $\mathbf{v}(t) = \frac{\partial \mathbf{r}}{\partial t}$ and the FEAS-01 scorecard convention.<br>• Resolves `GAP-59-08` in `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`.<br>• Formal clarifying amendment to `pinn_architecture.md` §10.6 is routed to milestone v2.6. |
| **C-2** | Definition of Done (PoC target) | Open | **OPEN** | Deferred for separate discussion per owner instruction. Proposed Level 6 Stage-0 PoC remains pending. |
| **C-4** | Stage-0 position pass bar ($E$) | Open | **OPEN** | Deferred for separate discussion per owner instruction. Proposed Tier 1 ($E \le 0.1$) and formula/copy beating remain pending. |
| **C-5** | Stage-0 energy pass bar ($\text{eps}_H$) | Open | **OPEN** | Deferred for separate discussion per owner instruction. With C-7 resolved to Option A, C-5 will evaluate autograd velocities when decided. |
| **C-6** | The $10^{-5}$ held-out pass bar | Open | **OPEN** | Deferred for separate discussion per owner instruction. Existing locked text in `pinn_architecture.md` §10.6 remains untouched in Phase 68. |

---

## 4. Milestone v2.6 Amendment and Implementation Routing Table

Per YARD-02 and YARD-03, this ruling routes actionable implementation and specification items to milestone `v2.6`:

| Route ID | Target Document / File | Action Required | Source Authority |
|---|---|---|---|
| `ROUT-68-01` | `pinn_architecture.md` §10.6 | Formally clarify that neural network trajectory predictions evaluate energy error $\text{eps}_H$ using instantaneous velocities obtained via automatic differentiation ($\mathbf{v}_{\text{autograd}} = \partial \mathbf{r}_{\text{pred}} / \partial t$), rather than numerical finite differences on discrete position outputs. | Owner Checkpoint 2 ruling: C-7 Option A |
| `ROUT-68-02` | `pinn/training/validation_gate.py` | Add autograd velocity support to validation gate execution for continuous neural network trajectory predictions, preserving gradient tracking with respect to input coordinate $t$ during validation passes. | Owner Checkpoint 2 ruling: C-7 Option A |
| `ROUT-68-03` | `pinn/evaluate.py` | Enable autograd velocity computation in the evaluation harness when scoring continuous model trajectories, matching the FEAS-01 explicit-velocity scoring standard. | Owner Checkpoint 2 ruling: C-7 Option A |
| `ROUT-68-04` | Milestone v2.6 Planning | Conduct dedicated discussion with project owner to rule on C-2, C-4, C-5, and C-6 before establishing production pass bars or spending preserved evaluation data. | Owner Checkpoint 2 ruling: Companion rows open |
