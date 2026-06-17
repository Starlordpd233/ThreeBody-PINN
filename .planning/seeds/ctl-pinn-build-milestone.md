---
title: CTL-PINN build milestone (FUT-01 code rewrite ∥ training pipeline ∥ user runbook)
planted_date: 2026-06-11
trigger_condition: >
  ALL of: (1) v1.5 milestone complete (data-side contracts settled, spec edits to
  ctl_instruction.md / pinn_architecture.md applied); (2) doc-03 milestone resolved or
  user explicitly waives waiting on it (it owns training-loop usage of SCS/SASD/IPR/PSC,
  M16 collocation scaling, G6 causal training per SCOPE-11); (3) trainex-r1 resolutions
  (r1a decisions/structure + r1b runbook/ops knowledge) delivered AND the user's D1–D7
  decision-sheet picks recorded.
---

# Seed: CTL-PINN Build Milestone

The future milestone that builds the actual system. Three streams developed in parallel
with each other (user decision 2026-06-11, confirming design doc Section 10):

1. **FUT-01 — `pinn/` package rewrite from specs.** The scientific side: network,
   loss formulation, curriculum state machine, all implemented from the post-v1.5
   (and post-doc-03) framework specs. v1.3-era live code is NOT a grounding source;
   it gets replaced wholesale.
2. **Training pipeline (FUT-04 territory).** The mechanical side: dev environment,
   data ingestion (per v1.5 PIPE-XX contracts), training loop shell, verification
   layer — per the training-execution reference design.
3. **User runbook.** The non-expert-facing step-by-step workflow (setup → configure →
   launch → monitor → resume), promoted from Section 5 of the reference design once
   trainex-r1 fixes the framework and the real commands/error surfaces exist; the r1
   K1–K3 findings (health watchlist, unattended-Mac ops, runbook patterns) seed it.

## Starting inputs when triggered

- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`
  (baseline reference design from a quick 2026-06-10 brainstorm — per its 2026-06-11
  standing note a simplified starting point, NOT fundamental trainex structure;
  placeholders PH-1..PH-10 marked; subject to r1 baseline-critique revisions)
- Trainex-r1 resolution docs (r1a + r1b) + filled decision sheet (from `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/`)
- v1.5-revised framework specs (`ctl_instruction.md`, `pinn_architecture.md`)
- doc-03 outcomes (training-loop contracts)
- `.planning/notes/training-execution-parallel-work-boundary.md` (the boundary decision)

## First action when triggered

Per design doc Section 10: a fresh brainstorm/planning session producing the build plan,
with this seed and the design doc as inputs. Do NOT skip straight to code — the design
doc deliberately produced no implementation plan, and the placeholder resolutions
need to be folded into the plan first. Remaining research handoffs after trainex-r1
(which covers PH-1/PH-8/PH-9/PH-10, the structural slices of PH-7/PH-6, determinism
policy, stage-boundary mechanics, feasibility envelope, the trainer-correctness
verification ladder, and runbook research): trainex-r2 (numeric tuning of
PH-7 optimizer/LR and PH-6 collocation inside the r1a-picked skeleton) before the first
real training run; PH-5 split policy once v1.5 data contracts and dataset statistics are
in hand.
