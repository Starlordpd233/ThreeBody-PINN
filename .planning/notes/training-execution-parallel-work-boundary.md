---
title: Training-execution parallel-work boundary (gate-window decision)
date: 2026-06-11
context: gsd-explore advisory session on starting the CTL-PINN build alongside v1.5 adjudication
---

# Training-Execution Parallel-Work Boundary

User decision (2026-06-11, explore session): clarifies what "work on both stages
simultaneously" means for the CTL-PINN build effort relative to the in-flight v1.5
adjudication milestone.

## What "parallel" means

The reference design (`docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`,
Section 10) commits to the PINN code (scientific side, owned by framework specs) and the
training pipeline + user runbook (mechanical side) being built **in parallel with each
other** when the build effort begins. It does NOT mean building in parallel with v1.5
adjudication. The user confirmed this reading 2026-06-11: the runbook is developed
concurrently with the future build (or sequentially otherwise), not now.

## Workflow decision: external research handoff

Decisions requiring scientific justification, adjudication-grade analysis, or a researched
recommendation (framework choice, optimizer selection, collocation strategy, etc.) are
**handed off to external research agents**, mirroring the issue-doc research workflow:
research package → multiple external AI research passes → consolidation → resolution doc →
user delivers it back. The agent assembles packages and transcribes results; it does not
perform the adjudication itself. (User instruction 2026-06-11; consistent with the design
doc's own PH-1 entry, which defers framework choice to external research per STOP protocol.)

## Boundary table — what may start during the v1.5 gate window

| Build slice | Status | Gated on |
|---|---|---|
| Trainex-r1 foundational research round, split into two parallel sub-packages: r1a decisions & structure (D1 framework, D2 tracking, D3 compute + ingestion memory, D4 checkpoint policy + auto-guards + diagnostics, D5 loop-skeleton capabilities incl. loss-weighting machinery, D6 determinism policy, D7 stage-boundary mechanics, baseline critique) and r1b runbook & ops knowledge (K4 feasibility envelope + K5 correctness-verification ladder as co-priorities, K1 health watchlist, K2 unattended-Mac ops, K3 runbook patterns) | **STARTED 2026-06-11** (packages at `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a|b/`; build-decision packages live under `framework-specs/`, not `framework-revisions/research_reports/`, which is reserved for issue-doc adjudication) | Nothing — user hands off both in parallel when ready |
| GSD formalization of build milestone | **DONE** (seed: `.planning/seeds/ctl-pinn-build-milestone.md`) | — |
| Runbook v0 draft | Queued | Trainex-r1 resolution + user's decision-sheet picks landing (commands/error tables are framework-dependent; K1–K3 findings feed the draft) |
| Trainer mechanical scaffold (config schema, run dirs, logging, checkpoint/resume, CLI) | Deferred | v1.5 Phases 26–27 (data + precision contracts) settling; avoids live `pinn/` code mid-adjudication |
| Subsystem 2 — data ingestion | Blocked | v1.5 Phases 26–27 outputs (DataLoader ingestion/selection contracts are literally their deliverable) |
| Training-loop science (loss, curriculum, network) | Blocked | v1.5 Phases 28–29 spec edits AND future doc-03 milestone (training-loop metric usage, M16 collocation scaling, G6 causal training per SCOPE-11) |

## Rationale

The training-loop science has TWO upstream spec revisions pending (v1.5 and doc-03);
data ingestion has one (v1.5 Phases 26–27). Building those now invents ahead of
adjudication and guarantees rework. The trainex-r1 foundational round (framework choice plus the other
early-settling decisions and runbook research) is nearly independent of adjudication, and
its outputs unblock the remaining placeholders (PH-7/PH-6 in trainex-r2). One dependency
edge is flagged: v1.5 Phase 27 adjudicates precision contracts, so the r1 output contract
requires a conditional recommendation on the precision requirement. Per user direction
(2026-06-11), r1 was deliberately scoped BIG — every core design and runbook perspective
worth settling early (decisions D1–D7 as options menus the user picks from, knowledge
K1–K5 for the runbook, plus a baseline critique of the quick-brainstorm design doc) —
then split into two parallel sub-packages (r1a decisions/structure, r1b runbook/ops
knowledge) so single-prompt research agents keep per-topic depth. Later rounds tune
within the structure r1 fixes: trainex-r2 is pure numeric tuning inside the r1a-picked
skeleton.
