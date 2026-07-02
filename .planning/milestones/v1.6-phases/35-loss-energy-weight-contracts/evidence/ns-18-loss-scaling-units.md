# Evidence Packet: NS-18 - Loss Scaling and Units

## Header

| Field | Value |
|---|---|
| ID | `NS-18` |
| Title | Loss scaling and units |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 35` |
| Owner Phase | `Phase 35` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOSS-01` |
| Spec Sections Touched | `ctl_instruction.md` loss scaling and total-loss assembly; `pinn_architecture.md` component loss math |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The issue doc is a non-authoritative conflict source, and the final resolution doc is a candidate verdict source consumed under the Phase 32 evidence protocol.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:110`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:159-167`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:366-379` | Non-authoritative issue source | The issue doc asks for an explicit scaling contract across `L_data`, `L_physics`, and `L_energy`, proposes L1/MAE for data, states physics and energy use collocation points with `epsilon_soft=1e-5`, and gives unconditional `tau`-based chain factors. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:76-78` (§1.14 NS-18); `03-final-resolution.md:158-161` (NS18-01..04); `03-final-resolution.md:195` (DGR-06 context) | Candidate verdict source, not authority | §1.14 records a `modified` verdict: confirm the current dimensionless contract, use projected scaled positions for data, componentwise normalized-time derivatives for physics, matched `epsilon_train = 1e-5` in physics and energy, raw masses, shared physics/energy collocation set, IC anchor, angular-momentum regularizer, no linear-momentum loss, Huber data loss instead of issue-doc L1/MAE, and `2`/`4` factors only for a `tau`-leaf path. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:59`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:94`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:153` | Navigation / line-map aid | Maps NS-18 to §1.14 lines 76-79, marks it covered, and records the modified disposition: dimensionless contract confirmed, issue L1/MAE replaced by spec Huber, and matched `epsilon_train` / raw-mass conventions retained. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:300-308` defines Huber data loss on scaled projected positions and replaces the previous MAE/L1 prose.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:493-531` defines the soft energy regularizer and its `delta = 1.0` Huber transition.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:590-603` states that positions, velocities, and initial energy use the same dimensionless unit system, that physics and energy use the same `epsilon_train = 1e-5`, and that the same collocation points are used for physics and energy loss.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:625-656` defines the total loss catalog, including no dedicated linear-momentum term and the PHYS-05 warmup schedule.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:876-893` defines canonical `u=t/T` derivatives and conditional `tau` chain-rule factors.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1689-1715` lists the training data flow and named loss components; `ctl_instruction.md:1722-1751` assembles the total loss by reference to `pinn_architecture.md`.
- `.planning/phases/34-training-loop-batch-construction-contracts/evidence/b-08-data-vs-collocation-points.md:51-56` and `b-08-data-vs-collocation-points.md:77-88` record the two logical point sets and that energy reuses the physics collocation set.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `.planning/REQUIREMENTS.md:92-95` define SCOPE-12 through SCOPE-15: locked v1.4/v1.5 outcomes are hard constraints; v1.6 spec edits are limited to `ctl_instruction.md` and `pinn_architecture.md`; training-loop code and empirical EDA remain FUT.
- `.claude/rules/pinn-reference.md:14-16` locks the architecture/input contract: input is `[tau, IC13]`, `tau = 2u - 1`, autograd leaf `u = t/T`, and output is 9D positions with the COM projection head.
- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md:18-24` states the Phase 35 target for LOSS-01: modified NS-18 verdict, no-linear-momentum-loss statement, shared physics/energy collocation set, and the `tau` versus `u` derivative-factor distinction.
- `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md:101-109` records D-35-06 with the same target state and warns not to contradict Phase 34 LOOP-02/03.

No additional dataset evidence is required for this packet because it transcribes the current dimensionless spec contract and Phase 34 point-set split.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may implement the training loop using these spec contracts after Phase 35/36 verification. Live `pinn/` code is NOT grounding evidence and is not cited here.
- Not FUT-applicable: This packet records the evidence and spec transcription target only.

## First-Principles or Engineering Check

1. **Dimensional consistency:** Data, physics, and energy terms must be evaluated in the same nondimensional coordinate system; mixing unscaled positions with scaled derivatives would make loss magnitudes and residuals physically incomparable.
2. **Autograd leaf boundary:** If the autograd leaf is `u=t/T`, then derivatives are already with respect to normalized physics time and no `2`/`4` factors are applied. Those factors are only the chain rule for a path differentiating directly with respect to `tau = 2u - 1`.
3. **Point-set compatibility:** Phase 34 separates data-fidelity snapshot points from continuous collocation points; NS-18 must preserve that split while recording that energy reuses the physics collocation set.
4. **Momentum redundancy:** The COM projection head and zero-momentum output contract make a separate linear-momentum loss redundant; the packet therefore records a no linear-momentum loss statement instead of inventing `L_P`.

## Verdict

Verdict: `accept-resolution` (resolution-doc NS-18 position: `modified`)

Explicit user instruction: None beyond the Phase 35 SPEC/CONTEXT lock.

Reasoning:

- The candidate resolution doc §1.14 confirms the current dimensionless contract while modifying the issue-doc framing: Huber replaces L1/MAE, chain factors are conditional on a `tau` leaf, and energy shares the physics collocation set.
- NS18-01, NS18-02, NS18-03, and NS18-04 are grounded by current framework spec sections for component math, softening, raw masses, AD, and loss catalog boundaries.
- The Phase 34 B-08 packet already locks the two-point-set separation, so this packet preserves data-vs-collocation independence and does not merge loss roles.

## Root-Cause Ambiguity

The issue doc correctly asked for a unified loss-scaling contract but mixed in stale L1/MAE data-loss wording and unconditional `tau` chain factors. The current specs already use Huber data loss, componentwise `u` derivatives, matched Plummer softening, and separate point-set roles. The ambiguity is resolved by transcribing the modified verdict rather than the issue-doc literal proposal.

## Locked Convention or Owner Route

Locked for Phase 35 transcription:

```text
NS-18 / LOSS-01:
- Use projected scaled positions for Huber data loss.
- Use componentwise normalized-time derivatives for physics and energy.
- Use matched epsilon_train = 1e-5 in physics and energy.
- Use raw masses where the physics/COM contracts require raw mass metadata.
- Keep data-fidelity points separate from physics/energy collocation points.
- Energy reuses the physics collocation set.
- Preserve IC anchor and angular-momentum regularizer.
- Record no linear-momentum loss / no-linear-momentum-loss: separate L_P is redundant.
- Apply 2 and 4 chain-rule factors only when differentiating with respect to tau;
  if u=t/T is the autograd leaf, no chain-rule factor is applied.
```

## Which Source Was Correct / Wrong

- Issue doc: correct that an explicit scaling contract is needed; wrong or stale where it asserts L1/MAE data loss or unconditional `tau` factors.
- Resolution doc: correct in confirming the dimensionless current contract and modifying the issue-doc framing.
- Current specs: mostly correct baseline math; later Phase 35 edits should add LOSS-01 status tags and cross-references without duplicating component formulas into `ctl_instruction.md`.
- Phase 34 B-08 packet: correct point-set split; NS-18 must preserve it.

## Before / After or Intentional Non-Change Note

**Before:** `pinn_architecture.md` already carries Huber data loss, componentwise AD, matched energy softening, shared physics/energy collocation points, no separate linear-momentum loss, and conditional `tau` factors, while `ctl_instruction.md` assembles loss terms by reference. These are not yet tagged as the Phase 35 NS-18 / LOSS-01 `modified` verdict.

**After:** Phase 35 spec-edit plans should add LOSS-01 callouts and bidirectional cross-references while keeping component math canonical in `pinn_architecture.md` and methodology/assembly canonical in `ctl_instruction.md`. The issue-doc L1/MAE and unconditional chain-factor language must remain superseded.

## Named Acceptance Check

AC-LOSS-01

Planned pass criterion: the edited framework specs expose `LOSS-01`, `NS-18`, `modified`, Huber data loss, matched `epsilon_train = 1e-5`, raw masses, shared physics/energy collocation set, IC anchor, angular-momentum regularizer, no linear-momentum loss, and the `u=t/T` versus `tau` chain-factor distinction without contradicting Phase 34 LOOP-02/03.

Owning phase: Phase 35, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap opened. The required target fields are explicitly grounded by `03-final-resolution.md:76-78`, `03-final-resolution.md:158-161`, current framework-spec evidence, `.claude/rules/pinn-reference.md:14-16`, and the Phase 34 B-08 packet's point-set separation. Deferred executable training implementation remains FUT and is not invented here.

## Status Transition Log

```text
2026-06-29 pending-commit PENDING -> IN_PROGRESS (Phase 35 Plan 35-01 Task 2 by codex-gsd-executor-35-01; packet authored, NS-18 accept-resolution consumed)
```
