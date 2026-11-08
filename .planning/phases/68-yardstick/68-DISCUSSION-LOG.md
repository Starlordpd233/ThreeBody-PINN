# Phase 68: Yardstick - Discussion log

This log records the choices considered. `68-CONTEXT.md` is the handoff for
research and planning.

**Date:** 2026-11-08
**Phase:** 68-yardstick
**Areas resolved:** corpus access, matched comparisons, gate coverage and
checkpoint order.

## Decision authority

The owner invoked `$gsd-discuss-phase 68` and asked to continue after the
initial orientation. In the spec interview the owner chose option 3, to
gather evidence before choosing the proof-of-concept target. The exact
answer is in `.planning/phases/68-yardstick/68-SPEC.md` under Owner direction.

The remaining choices for this discussion were technical and came within
the standing delegation in `.planning/PROJECT.md` (2026-10-28). The agent
scouted the existing scorer, readers and gate callers and recorded the
decisions below. The discussion required zero new owner questions. The
charter choices remain pending at checkpoint 2, after the audit.

## Choices considered

| Area | Alternatives considered | Disposition and reason |
|---|---|---|
| Record access | Open the corpus through the production bulk adapter, or read only the fixed panel through the Stage-0 TRAIN reader. | Reuse the per-record reader and existing attestation. Admission precedes corpus path resolution and includes the corresponding gold sibling. |
| Known answers | Reuse historical scores, or calculate both answers on each matching native window with the frozen scorer. | Calculate the reference and window-mean constant for the audit. Historical scores remain comparison evidence with their original grid and velocity source. |
| Energy measurement | Invoke the production evaluation entry point, reimplement its formula, or exercise the shared calculations on allowed inputs. | Use the actual shared calls and trace the frame, time and dtype used by each caller. Compare recorded and estimated velocities on the same gold samples to isolate the velocity route. |
| Verdicts | Treat a correct-answer failure as a failed audit, or record audit completeness and metric verdict separately. | Preserve every observed result, including a passing conservation score for a constant and any failing Brutus score. The discrepancy is evidence for the owner. |
| Decision timing | Choose a target and bars now, or commit the audit and present the charter choices afterward. | Carry forward the owner's option 3. Ask for C-7 after the audit and use its disposition in the bar discussion. C-6 and C-7 require their own explicit replies. |

## Planning discretion and deferred work

Research and planning own the precise audit entry point, evidence format
and checks. The native gold result and relevant published comparisons are
evidence to gather. The Phase 66 and 67 closeouts bound what can be said
about learning one orbit and the effects of the tested settings.

The D-06 static epsilon todo concerns admission and stage labels under
different softening values. Its keyword match does not fit the locked
audit. Keep it separate. Phase 69 retains the redesign and `trainex-r5`
choices. Authorized changes to the production contracts go to v2.6.
