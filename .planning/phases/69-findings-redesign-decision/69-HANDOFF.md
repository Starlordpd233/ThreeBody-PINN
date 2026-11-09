# v2.6 handoff from Phase 69

The owner chose **A**. Keep the current architecture as the supervised fit
control while addressing the training recipe and physics pipeline. The owner
also commissioned **trainex-r5** to research that redesign. The dated replies
and exact evidence they address are recorded in the [owner ruling](69-RULING.md).

## Starting point for the redesign

The locked architecture’s diagnostic controls reached settled Tier 1 on two
systems and a second seed. The historical failures used a different optimizer
schedule, clipping, diagnostic polish, update budget and scored state. The
historical cause and exact initial state equivalence remain open. Use the
successful supervised fit as the reference when checking the repaired recipe.
Then follow the existing ladder through one orbit from physics, the 16-system
family and full Stage 0. Generalization and physics learning are still to be
demonstrated. [Findings](69-FINDINGS.md) · [Recipe comparison](69-EVIDENCE.md#recipe-comparability) · [Future requirements](../../REQUIREMENTS.md#future-requirements-v26-and-beyond)

If a limitation persists after the relevant pipeline checks, compare any
representation candidate with the control using matched data, recipe, budget
and scoring. The locked fit gives the redesign a comparison point. The
diagnostic optimizer and score are evidence for that comparison. Production
settings and pass bars are separate v2.6 decisions. [Decision packet](69-CHECKPOINT.md)

## Commissioned research

Open v2.6 with the trainex-r5 redesign review under order A. The owner
authorized the question presented in the closing packet:

> How should v2.6 retain the demonstrated single-orbit position fit while
> repairing the physics training and energy measurement, and what evidence
> should trigger a representation change before expanding to the 16-system
> family?

Ask the review to identify checks that distinguish a recipe or physics failure
from a representation limitation. DIAG-09 retained the original association.
The refuted rate-improvement hypothesis concerns the tested EXP-03 rates.
The commission is for redesign research. Package assembly and research belong
to the next milestone’s workflow. [Order A](../../PROJECT.md) · [Owner ruling](69-RULING.md)

## Yardstick and physics work carried forward

| Item | Handoff |
|---|---|
| C-7 A and GAP-59-08 | The owner resolved the velocity measurement choice. Route autograd velocities to the validation gate and evaluator, and clarify `pinn_architecture.md` §10.6. The known-answer comparison shows finite-difference error on both tested grids. A static predictor still conserves its own energy, so position accuracy needs a separate criterion. |
| C-2, C-4, C-5 and C-6 | Remain open for separate owner discussion on the proof-of-concept target, Stage 0 position and energy bars, and the held-out bar. |
| C-11 | Route the `ctl_instruction.md` evaluation-section rewrite to v2.6, in line with the bars when settled. |
| Single-anchor physics | Verify and address physics calculated on one trajectory per step. |
| IC reduction | Verify and address the IC term’s reduction over the selected slots. |
| IC and physics gradient imbalance | Investigate the earlier recorded IC gradient at roughly 10⁴ to 10⁶ times the physics gradient. |
| Production L-BFGS | Address the unreachable production stage. The historical Phase 60 diagnostic polish was executed in a separate recipe. |

Sources for these routes are the [Phase 68 owner ruling](../68-yardstick/68-CHECKPOINT-2-RULING.md), [yardstick evidence](69-EVIDENCE.md#yardstick-and-current-owner-ruling) and [future requirements](../../REQUIREMENTS.md#future-requirements-v26-and-beyond).

Stage 1+ and PLAT-01 through PLAT-07 remain blocked. The single held-out
evaluation remains unspent. The next milestone’s empirical plans need their
own scope, predictions and resource decisions. [Scope boundaries](../../REQUIREMENTS.md#scope-boundaries-owner-direction-2026-10-27-hard-constraints)
