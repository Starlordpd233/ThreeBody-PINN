# Evidence Packet: NS-12 - Componentwise Automatic Differentiation

## Header

| Field | Value |
|---|---|
| ID | `NS-12` |
| Title | Componentwise automatic differentiation |
| Severity | `MAJOR` |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 35` |
| Owner Phase | `Phase 35` |
| Consumer Phase | `Phase 36` |
| Acceptance Check ID | `AC-LOSS-01-AD` |
| Spec Sections Touched | `ctl_instruction.md` loss scaling and AD cross-link; `pinn_architecture.md` PHYS-02 derivative contract |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

Neither source is authoritative. The issue doc is a non-authoritative conflict source, and the final resolution doc is a candidate verdict source consumed under the Phase 32 evidence protocol.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:108`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:164`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:167` | Non-authoritative issue source | The issue doc asks for concrete componentwise AD rather than differentiating a summed 9D output proxy, and its loss-scaling contract points to component-wise accelerations and canonical AD chain-rule factors. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `03-final-resolution.md:68-70` (§1.12 NS-12); `03-final-resolution.md:152-154` (NS12-01..03); `03-final-resolution.md:231` (GAP-13) | Candidate verdict source, not authority | §1.12 records an `accepted` verdict: PHYS-02 already requires coordinatewise first and second derivatives and forbids the summed-output VJP. The all-ones-covector snippet is rejected, while executable batched implementation/performance details remain FUT work. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:57`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:92`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:151`; `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:210` | Navigation / line-map aid | Maps NS-12 to §1.12 lines 68-71, marks it covered, records the accepted disposition, and routes executable AD implementation/memory strategy to FUT-01 via GAP-13. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:817-825` states that velocities and accelerations are derived from projected positions with componentwise AD with respect to normalized physics time `u=t/T`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:876-893` defines the normalized-time derivative contract, canonical autograd leaf `u=t/T`, and conditional `tau` chain-rule factors.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:895-907` explicitly requires componentwise derivatives and forbids `torch.autograd.grad(r.sum(), u, create_graph=True)` because it computes a vector-Jacobian product against an all-ones covector rather than nine individual derivatives.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1519-1528` defines the network input relation `tau = 2u - 1`, `u=t/T`, and points normalized-time derivative details to `pinn_architecture.md` PHYS-02.

No framework spec is edited by this packet.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:16` and `.planning/REQUIREMENTS.md:92-95` define SCOPE-12 through SCOPE-15: locked v1.4/v1.5 outcomes are hard constraints; v1.6 spec edits are limited to `ctl_instruction.md` and `pinn_architecture.md`; training-loop code and empirical EDA remain FUT.
- `.claude/rules/pinn-reference.md:14-16` locks the architecture/input contract: input is `[tau, IC13]`, `tau = 2u - 1`, and autograd leaf `u = t/T`; output is 9D positions with the COM projection head.
- `.planning/phases/35-loss-energy-weight-contracts/35-SPEC.md:18-24` and `.planning/phases/35-loss-energy-weight-contracts/35-CONTEXT.md:101-109` make the NS-12 AD boundary part of LOSS-01 / NS-18 packet-before-edit evidence.

No dataset evidence is needed for this packet because the current framework spec already states the derivative contract and the candidate resolution accepts it.

## FUT Hand-off Note

- FUT path / note: FUT-01/FUT-04 may choose a performant batched implementation pattern, memory strategy, and executable PHYS-02 tests. Live `pinn/` code is NOT grounding evidence and is not cited here.
- Not FUT-applicable: This packet records the spec-side componentwise AD verdict only.

## First-Principles or Engineering Check

1. **Jacobian shape:** A 9D projected position output needs nine coordinate derivatives with respect to `u`; summing the output before differentiation collapses the Jacobian with an all-ones covector and loses coordinate identity.
2. **Physics residual correctness:** Newton residual and Hamiltonian terms require velocity and acceleration per body and coordinate, so a summed-output VJP cannot supply the necessary componentwise kinematics.
3. **Implementation boundary:** The spec can require full componentwise derivatives without choosing `jacrev`, explicit loops, batching layout, or memory strategy; those executable details remain FUT under GAP-13.

## Verdict

Verdict: `accept-resolution` (resolution-doc NS-12 position: `accepted`)

Explicit user instruction: None beyond the Phase 35 SPEC/CONTEXT lock.

Reasoning:

- The candidate resolution doc §1.12 accepts the current PHYS-02 componentwise-AD contract and rejects the summed-output VJP anti-pattern.
- NS12-01 and NS12-02 are grounded in the current framework spec; NS12-03 explicitly defers executable implementation/performance details.
- The current specs already carry the componentwise derivative and `u`/`tau` boundary; later Phase 35 edits should cross-link and status-tag this contract without using live `pinn/` code.

## Root-Cause Ambiguity

The issue doc observed that source documents lacked concrete implementation detail. The current framework spec already resolved the semantic AD requirement, but executable batching/performance strategy remains outside the specwork phase. The root ambiguity is implementation specificity, not the derivative contract.

## Locked Convention or Owner Route

Locked for Phase 35 transcription:

```text
NS-12 / AC-LOSS-01-AD:
- Derive velocity and acceleration from projected positions using componentwise AD.
- Use the canonical autograd leaf u=t/T unless a specific path differentiates with respect to tau.
- Forbid the summed-output VJP / all-ones-covector anti-pattern.
- Leave batched implementation and performance details to FUT-01/FUT-04.
```

## Which Source Was Correct / Wrong

- Issue doc: correct that a summed-output proxy is not sufficient and that implementation detail remains FUT; not needed as a replacement for the existing PHYS-02 semantic contract.
- Resolution doc: correct in accepting PHYS-02 and deferring executable details.
- Current specs: correct semantic contract; later Phase 35 edits should add LOSS cross-links and AC status without duplicating the PHYS-02 body.

## Before / After or Intentional Non-Change Note

**Before:** `pinn_architecture.md:876-907` already defines componentwise normalized-time AD, `u=t/T`, conditional `tau` factors, and the forbidden summed-output VJP; `ctl_instruction.md:1519-1528` already points to PHYS-02.

**After:** Phase 35 spec-edit plans should add LOSS-01 / AC-LOSS-01-AD status-tagged references while leaving implementation/memory strategy as FUT work.

## Named Acceptance Check

AC-LOSS-01-AD

Planned pass criterion: the edited framework specs expose `NS-12`, `AC-LOSS-01-AD`, `accepted`, componentwise AD, the canonical `u=t/T` autograd leaf, and the rejection of summed-output VJP; no executable implementation detail is locked in v1.6.

Owning phase: Phase 35, with Phase 36 final structural/acceptance verification.

## STOP / Gap Handling

No STOP gap opened. The semantic AD requirement is explicitly grounded by `03-final-resolution.md:68-70`, `03-final-resolution.md:152-154`, and current PHYS-02 spec evidence. The missing executable implementation strategy is already deferred to GAP-13, so no new source-silent decision is invented.

## Status Transition Log

```text
2026-06-29 pending-commit PENDING -> IN_PROGRESS (Phase 35 Plan 35-01 Task 2 by codex-gsd-executor-35-01; packet authored, NS-12 accept-resolution consumed)
```
