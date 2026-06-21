# Evidence Packet: D-05 - s_min Frame Owner Decision

## Header

| Field | Value |
|---|---|
| ID | `D-05` |
| Title | `s_min` frame owner decision |
| Severity | owner-decision |
| Current Status | `DEFERRED` |
| Current Verdict | `defer-with-blocker` |
| Phase | Phase 32 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 33 `CURR-05`; Phase 35 loss-side references |
| Acceptance Check ID | `AC-EVID-15-D05` |
| Spec Sections Touched | None in Phase 32; future `ctl_instruction.md` curriculum stage gate and Phase 35 loss cross-references only after owner decision |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:42-63`; `03-curriculum-and-training-loop.md:412-418`; `03-curriculum-and-training-loop.md:520-528` | Non-authoritative issue source | Records D-05 as awaiting human approval, presents Option A as unsoftened `s_min` for the curriculum stage gate plus softened loss-side criterion, Option B as softened `max(s_min, epsilon)` everywhere, and Option C as an owner-defined hybrid or alternative convention. Later sections recommend keeping unsoftened gate diagnostics while applying softening only in training loss. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:28-31`; `03-final-resolution.md:111-113`; `03-final-resolution.md:191-193`; `03-final-resolution.md:221-222` | candidate verdict source, not authority | Section 1.2 is `surface_to_user`: it states the current baseline uses unsoftened geometric `s_min` for stage assignment and matched-Plummer pair distances in training residual and energy, but the owner must explicitly approve the geometric gate or define a softened gate. `SMIN-01..03` and `DGR-02/03` preserve both the grounded split and the unresolved owner decision. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:47-48`; `31-RESOLUTION-MAP.md:82-83`; `31-RESOLUTION-MAP.md:141-142`; `31-RESOLUTION-MAP.md:200-201` | Navigation / line-map aid | Maps D-05 to section 1.2, records coverage as routed human approval, previews unsoftened geometric `s_min` plus matched-Plummer loss/residual, and carries GAP-03 as the open gate-frame decision. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:207-211` | Readiness and caveat routing | Records C-02 as the D-05 caveat: geometric versus softened stage gate routed to Phase 32 EVID-15 and owner decision. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:237-244` defines Stage 6 near-collision criteria using `s_min < 0.5` as a curriculum-stage gate.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:897-929` says subsequent invariants, including `s_min`, are computed after global scaling from scaled positions and velocities, and preserves the Plummer-form invariant convention.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1056-1067` states that invariant computation uses Plummer softening only in `V`, while the geometric quantity `s_min` is computed from true pairwise separations with no softening; it also distinguishes static-invariant softening from training-time softening.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:359-400` defines the training physics residual with Plummer-softened distance and `epsilon_train = 1e-5`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:492-512` defines energy loss through the analytic matched-Plummer Hamiltonian using the same safe distance as the residual force term.

These lines support the grounded distinction between a geometric stage-gate quantity and matched-Plummer training residual/energy terms. They do not by themselves record owner approval of the final stage-gate frame.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:33-37` requires line-range evidence, fixed-set verdicts, and EVID-15 root-cause adjudication for D-05.
- `.planning/REQUIREMENTS.md:92-98` keeps PHYS-03 softening `eps_soft = 1e-5` and bans live `pinn/` grounding, while routing v1.6 to specwork only.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:48-52` requires D-05 to remain separate and deferred unless explicit prior user instruction resolves it.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-RESEARCH.md:132` identifies D-05 as high STOP risk because a gate-frame choice changes stage labels and downstream curriculum semantics.

No prior user decision or resolved gap entry in the loaded Phase 32 context chooses geometric gate, softened gate, or another final stage-gate frame.

## FUT Hand-off Note

- FUT path / note: Future training and data implementation should consume the eventual owner-selected gate-frame contract. This packet does not cite live `pinn/` code and does not use live code as grounding.
- Not FUT-applicable: Phase 32 creates evidence artifacts only.

## First-Principles or Engineering Check

The engineering distinction is between classification semantics and numerical regularization:

- A geometric `s_min` stage gate asks whether a trajectory actually approaches close physical separation. It is a curriculum-labeling criterion; softening it changes the boundary of the stage population and could move trajectories between stages.
- A matched-Plummer training residual or energy term regularizes a differentiable force/potential calculation so training remains finite near close encounters. It is a numerical-stability convention for loss evaluation, not proof that curriculum labels should use the same softened value.
- A softened stage gate could be defensible if the owner wants the curriculum to track the physics the network sees, but that would intentionally change stage-label semantics and any downstream counts/thresholds.

The sources ground the loss-side matched-Plummer distinction. They do not settle the owner preference for the stage-gate frame.

## Verdict

Verdict: defer-with-blocker

Explicit user instruction: None

Reasoning:

- The issue doc and candidate verdict source both preserve D-05 as an owner decision rather than a completed automatic fix.
- Current specs support an unsoftened geometric `s_min` baseline for invariants/stage criteria and a matched-Plummer training residual/energy convention, but the Phase 32 context requires explicit owner instruction before finalizing the gate frame.
- The packet may safely record the grounded loss-side matched-Plummer distinction, but it cannot approve the final stage-gate frame without a concrete prior instruction or a short first-principles proof that eliminates the owner choice. No such proof or instruction is present.

## Root-Cause Ambiguity

The ambiguity is a naming and context collision: `s_min` is used as a geometric curriculum-stage quantity, while close-encounter training losses use softened matched-Plummer pair distances. Source language that says "collision criterion" can refer to either curriculum staging or loss evaluation unless the artifact names the frame explicitly.

## Locked Convention or Owner Route

Owner route and blocker:

- Primary owner: Phase 33 `CURR-05`, because the selected frame defines the curriculum stage gate.
- Phase 35 consumer: loss-side references should preserve matched-Plummer residual/energy softening and avoid reinterpreting it as a stage-label rule.
- Blocker: the framework owner must explicitly choose unsoftened geometric stage gate or define a softened gate, including which epsilon it uses, before Phase 33 can transcribe `CURR-05`.

No downstream phase should treat the D-05 stage-gate frame as resolved from this packet alone.

## Which Source Was Correct / Wrong

- The issue doc is correct that D-05 requires explicit owner approval and correctly separates stage gate from training-loss criterion in its later recommended-resolution text.
- The candidate verdict source is correct that current evidence supports unsoftened geometric `s_min` as the current baseline and matched-Plummer distances in residual/energy.
- Neither source is sufficient to select the final stage-gate frame. The dissent and report-attribution columns are provenance, not votes.

## Before / After or Intentional Non-Change Note

Intentional Phase 32 non-change: no framework spec section is edited in this plan. The downstream "after" state is blocked until the owner selects the D-05 stage-gate frame. Phase 33 must not finalize `CURR-05` from this packet alone; Phase 35 may cite the matched-Plummer loss-side distinction but must not use it to infer the curriculum gate.

## Named Acceptance Check

`AC-EVID-15-D05`

Planned pass criterion: this packet must cite issue-doc D-05 decision, open-decision, considered-alternative ranges, final-resolution section 1.2, `SMIN-01..03`, `DGR-02/03`, and distinguish stage-gate frame from loss/residual softening while recording `defer-with-blocker` unless explicit owner instruction is cited.

Owning phase: Phase 32 for packet coverage; Phase 36 for final structural verification.

## STOP / Gap Handling

No STOP gap opened. The known D-05 owner routing is already specified by the Phase 32 plan and protocol, and this packet preserves it as `defer-with-blocker` without selecting geometric or softened stage gate. No new source-silent semantic question beyond that known owner route was encountered.

## Status Transition Log

```text
2026-06-21 pending-commit PENDING -> DEFERRED (Phase 32 Plan 32-03 Task 2 by codex-gsd-executor-32-03)
```
