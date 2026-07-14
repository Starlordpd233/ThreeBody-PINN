# Learning Curriculum

## Evidence states

- **queued** — selected as a likely future capability but not yet taught.
- **introduced** — encountered in an orientation or lesson; no mastery claim.
- **practicing** — attempted, but correction or more application is still needed.
- **demonstrated** — used correctly in an explanation or application without copying lesson wording.
- **retained** — retrieved and applied correctly after delay.

## Dependency map and queue

| ID | Capability | Depends on | State at workspace creation | Evidence or next action |
|---|---|---|---|---|
| O0 | Map regression to a layered neural network | AP Statistics least-squares | introduced | Historical sample in the source design; three corrected re-attempts remain pending. |
| U1 | Distinguish representation, optimization, and generalization from evidence | O0 vocabulary only | queued | First deep unit; repairs “more layers means more fitting and accuracy.” |
| U2 | Derive one gradient update and explain what autograd records | U1 | queued | Start only after U1's three-way distinction is at least demonstrated or deliberately deferred. |
| U3 | Translate three-body state and scaling into model inputs and outputs | algebra, mechanics | queued | Independent of project phase numbering. |
| U4 | Derive one physics residual from a second-order ODE | U2, U3 | queued | No implementation detail until the mathematical residual is understood. |
| U5 | Interpret training, validation, and physical-consistency evidence | U1, U4 | queued | Reuses U1 rather than reteaching capacity versus achieved performance. |
| U6 | Explain curriculum stages, checkpoints, recovery, and reproducibility evidence | U1, U5 | queued | Final item in the provisional sequence, not a promised endpoint. |

## Active unit

No unit is active until Unit 0001 is source-checked and released. The executor changes U1 from `queued` to `introduced` at that release; the learner's attempt then determines whether it becomes `practicing` or `demonstrated`.

## Review queue

No delayed review is due at workspace creation. A demonstrated capability receives:

1. a short reactivation at the next learning session;
2. a contrast or application question after at least one later unit; and
3. a longer-delay check, normally 1–4 weeks later, chosen from observed difficulty.

Failed retrieval returns a capability to `practicing`; it does not erase the prior attempt.

## Topic nominations from work

None recorded. A nomination is a pointer to a useful example, never an automatic lesson or a phase gate.
