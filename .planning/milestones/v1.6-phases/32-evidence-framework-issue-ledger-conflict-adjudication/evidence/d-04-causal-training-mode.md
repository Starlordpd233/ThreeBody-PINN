# Evidence Packet: D-04 - Causal-Training Mode Owner Decision

## Header

| Field | Value |
|---|---|
| ID | `D-04` |
| Title | Causal-training mode owner decision |
| Severity | owner-decision |
| Current Status | `DEFERRED` |
| Current Verdict | `defer-with-blocker` |
| Phase | Phase 32 |
| Owner Phase | Phase 35 |
| Consumer Phase | Phase 35 `LOSS-04`; Phase 34 `LOOP-01` if batch-windowing changes |
| Acceptance Check ID | `AC-EVID-15-D04` |
| Spec Sections Touched | None in Phase 32; future `ctl_instruction.md` / `pinn_architecture.md` loss and batch-windowing sections only after owner decision |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:16-40`; `pinn_instruction/issues/03-curriculum-and-training-loop.md:383-410` | Non-authoritative issue source | Records D-04 as awaiting human approval, frames Option A per-time-step causal weighting, Option B global sampling plus ALM, and Option C time-windowed causal-ALM hybrid. It discloses that Option B accepts temporal-causality risk and that Option C rewrites DataLoader, batch construction, ALM state, checkpointing, and stage transitions. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:24-27`; `03-final-resolution.md:106-110`; `03-final-resolution.md:190`; `03-final-resolution.md:219-220` | candidate verdict source, not authority | Section 1.1 is `surface_to_user`: it rejects dense-residual pseudo-ALM, keeps ALM optional/scalar-only, and says the framework owner must still select the final mode. Claim rows `CAU-01..CAU-05` preserve current baseline facts, route `CAU-04` to owner selection, and defer the causal exponent clipping bound. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:46-47`; `31-RESOLUTION-MAP.md:81-82`; `31-RESOLUTION-MAP.md:140-142`; `31-RESOLUTION-MAP.md:198-200` | Navigation / line-map aid | Maps D-04 to section 1.1, records coverage as routed human approval, previews `surface_to_user`, and carries GAP-02 as the open owner selection for Phase 32 EVID-15. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:207-211`; `31-READINESS-REPORT.md:230-233` | Readiness and caveat routing | Records D-04 as non-blocking caveat C-01 whose owner must select Option A/B/C, routed to Phase 32 EVID-15 and downstream owner decision. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:359-416` defines the physics residual with sorted collocation times and default causal weights `w_n = exp(-eta_c * sum stopgrad(R_m))`, with the unweighted mean logged only as a diagnostic.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:671-681` keeps ALM outside the baseline training contract, permits it only as a P2 ablation for scalar conservation constraints, and forbids ALM on the dense ODE residual.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1554-1583` defines the default loss with `L_phys^causal`, documents causal weighting as the PHYS-05 default, requires an exponent clip without selecting the bound, and rejects the pseudo-ALM dense residual formulation.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1606-1619` gives the current mini-batch construction context that would be affected only if the selected causal mode changes batch windowing.

These lines are current-spec evidence, not a Phase 32 edit target.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:33-37` requires EVID-11/EVID-12/EVID-15 evidence, fixed-set verdicts, and root-cause adjudication before downstream contract edits.
- `.planning/REQUIREMENTS.md:92-98` makes locked v1.4/v1.5 outcomes hard-constraint grounding, limits spec edits to `ctl_instruction.md` and `pinn_architecture.md`, keeps training-loop code out of scope, and bans live `pinn/` code as grounding.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:48-52` requires separate D-04/D-05/D-06 packets and says D-04/D-05/D-06 must defer or open a STOP gap unless explicit prior user instruction resolves them.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-RESEARCH.md:131` identifies D-04 as high STOP risk because choosing Option A/B/C changes the training paradigm.

No prior user decision or resolved gap entry in the loaded Phase 32 context selects Option A, Option B, or Option C.

## FUT Hand-off Note

- FUT path / note: Future training-loop implementation in FUT-01/FUT-04 must consume the owner-selected D-04 mode after Phase 35 records it. This packet does not cite live `pinn/` code and does not use live code as grounding.
- Not FUT-applicable: Phase 32 is evidence/specwork only.

## First-Principles or Engineering Check

The engineering consequence is not a small parameter change; each option changes what information a loss term can see and how gradients are allowed to flow through time:

- Option A, per-time-step causal weighting, enforces an arrow-of-time loss ordering by suppressing later residual contributions until earlier residuals improve. It can protect causality but risks a causal firewall if an early stiff segment drives later weights near zero.
- Option B, global sampling plus ALM-style global view, gives the optimizer access to late-time residuals immediately. It is simpler and more global, but the issue source explicitly flags temporal-causality risk because late-time gradients can influence the model before early dynamics are resolved.
- Option C, time-windowed causal-ALM hybrid, changes both sampling and state management by adding causal windows, local constraint handling, hard window gates, and state propagation. That is a different training architecture, not a Markdown cleanup.

Because these options change batch visibility, loss weighting, convergence gates, and ALM locality, Phase 32 cannot infer the owner preference from source counts or convenience. The sources preserve a real owner choice rather than a hidden theorem.

## Verdict

Verdict: defer-with-blocker

Explicit user instruction: None

Reasoning:

- The issue doc explicitly marks D-04 as awaiting human approval and lists three mutually exclusive modes with different risks and implementation scope.
- The candidate verdict source is not authority and also records `surface_to_user`: it rejects dense-residual pseudo-ALM and records the current baseline, but it does not select the final mode.
- Current specs show causal weighting as the default and dense-residual ALM as rejected, but no loaded grounding source says the framework owner has decided to retain that default, remove it, or commission Option C.
- Under AGENTS.md and the Phase 32 protocol, broad cautionary prose is insufficient. A concrete prior user instruction is required before selecting Option A, Option B, or Option C.

## Root-Cause Ambiguity

The ambiguity is a training-mode contract gap between three concerns that the source bundle keeps separate: time-causal residual weighting, dense-residual ALM rejection, and possible time-windowed batch/state mechanics. The current specs define causal weighting and reject dense-residual ALM, while the issue doc and resolution doc preserve a final owner decision about whether that baseline remains the training mode or is replaced by a global or windowed design.

## Locked Convention or Owner Route

Owner route and blocker:

- Primary owner: Phase 35 `LOSS-04`, because the selected mode determines the loss weighting and causal-training contract.
- Secondary consumer: Phase 34 `LOOP-01` only if the owner selects a windowed mode or another mode that changes replay/lookahead batch-windowing.
- Blocker: the framework owner must choose one of the causal-training modes or explicitly instruct a different split before Phase 35 can transcribe `LOSS-04`.

No framework spec edit should treat D-04 as resolved until this blocker is cleared.

## Which Source Was Correct / Wrong

- The issue doc is correct that D-04 is an owner decision and that the choices have different downstream consequences.
- The candidate verdict source is correct to reject dense-residual pseudo-ALM and to surface the final mode selection to the owner.
- Neither source is sufficient to select the final causal-training mode. The resolution doc's report references are provenance, not votes.

## Before / After or Intentional Non-Change Note

Intentional Phase 32 non-change: no framework spec section is edited in this plan. The downstream "after" state is blocked until the owner selects the final D-04 mode. Phase 35 must not write a final causal-training-mode contract from this packet alone; Phase 34 must not rewrite batch-windowing unless the owner-selected mode requires it.

## Named Acceptance Check

`AC-EVID-15-D04`

Planned pass criterion: this packet must contain issue-doc and candidate-resolution line citations, exact parser fields `Verdict:` and `Explicit user instruction:`, a `defer-with-blocker` verdict unless an explicit instruction is cited, and downstream routing that does not treat Option A/B/C as resolved.

Owning phase: Phase 32 for packet coverage; Phase 36 for final structural verification.

## STOP / Gap Handling

No STOP gap opened. The known D-04 owner routing is already specified by the Phase 32 plan and protocol, and this packet preserves it as `defer-with-blocker` without selecting a default. No new source-silent semantic question beyond that known owner route was encountered.

## Status Transition Log

```text
2026-06-21 pending-commit PENDING -> DEFERRED (Phase 32 Plan 32-03 Task 1 by codex-gsd-executor-32-03)
```
