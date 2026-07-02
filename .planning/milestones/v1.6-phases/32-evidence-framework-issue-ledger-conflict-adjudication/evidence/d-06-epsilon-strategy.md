# Evidence Packet: D-06 - Epsilon Strategy Owner Decision

## Header

| Field | Value |
|---|---|
| ID | `D-06` |
| Title | Epsilon strategy owner decision |
| Severity | owner-decision |
| Current Status | `DEFERRED` |
| Current Verdict | `defer-with-blocker` |
| Phase | Phase 32 |
| Owner Phase | Phase 33 |
| Consumer Phase | Phase 33 static invariants; Phase 35 loss consistency |
| Acceptance Check ID | `AC-EVID-15-D06` |
| Spec Sections Touched | None in Phase 32; future static-invariant text and loss-side cross-references only after owner decision |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `pinn_instruction/issues/03-curriculum-and-training-loop.md:65-86` | Non-authoritative issue source | Records D-06 as awaiting human approval, frames Option A as `eps = 1e-5` everywhere, Option B as dual-context `eps = 1e-10` for static invariants and `eps_soft = 1e-5` for dynamic loss, and Option C as tightening everything to `1e-10`. It says the owner must weigh the scientific argument against the dual-context rationale. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md:32-35`; `03-final-resolution.md:114-118`; `03-final-resolution.md:193`; `03-final-resolution.md:222` | candidate verdict source, not authority | Section 1.3 states the loss-side value and form are locked: `epsilon_train = 1e-5`, matched-Plummer, identically in physics and energy. The open decision is only whether offline static/invariant context retains `epsilon_inv = 1e-10` or collapses to `1e-5`; "`1e-10` everywhere" is preserved as a recorded alternative but is not selectable without reopening the locked loss contract. `EPS-03`, `EPS-05`, `DGR-04`, and `GAP-04` preserve the owner-routed static choice and missing sensitivity evidence. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md:48-49`; `31-RESOLUTION-MAP.md:83-84`; `31-RESOLUTION-MAP.md:142-143`; `31-RESOLUTION-MAP.md:200-201` | Navigation / line-map aid | Maps D-06 to final-resolution section 1.3, records coverage as routed human approval, and carries GAP-04 as the static-epsilon owner selection. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md` | `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md:207-211` | Readiness and caveat routing | Records C-03 as the D-06 caveat: static `epsilon_inv = 1e-10` versus collapse to `1e-5`, routed to Phase 32 EVID-15 and owner decision. |

## Current Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:610-636` defines data-side IPR with validation softening `eps_inv = 1e-10`, and explicitly distinguishes it from training-time `epsilon_train = 1e-5`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1056-1067` defines static-invariant softening `epsilon_inv = 1e-10` only in potential energy `V`, keeps `s_min` unsoftened, and separates static-invariant softening from the training-time PHYS-03 residual and energy contracts.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:373-400` defines the training physics residual with Plummer-softened distance and `epsilon_train = 1e-5`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:492-537` defines the matched-Plummer energy regularizer, computes its scale with `epsilon_train = 1e-5`, and states that training-time softening is distinct from data-side validation softening `epsilon_inv = 1e-10`.

These lines are current-spec evidence, not Phase 32 edit authority. They show the present dual-context baseline and the already-locked loss-side `epsilon_train = 1e-5` convention.

## Locked Convention / Dataset Evidence

- `.planning/REQUIREMENTS.md:33-37` requires line-range evidence, fixed-set verdicts, and EVID-15 root-cause adjudication for D-06.
- `.planning/REQUIREMENTS.md:92-98` keeps PHYS-03 softening `eps_soft = 1e-5` as a locked hard constraint and bans live `pinn/` code grounding.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-CONTEXT.md:48-52` requires D-06 to remain separate and deferred unless explicit prior user instruction resolves it.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-RESEARCH.md:133` identifies D-06 as high STOP risk because selecting static epsilon changes invariant and stage semantics.

No prior user decision or resolved gap entry in the loaded Phase 32 context chooses whether the static/invariant context retains `epsilon_inv = 1e-10` or collapses to `1e-5`.

## FUT Hand-off Note

- FUT path / note: Future implementation must preserve the locked loss-side `epsilon_train = 1e-5` matched-Plummer contract unless a later owner instruction reopens it. Static-invariant behavior must consume the eventual owner-selected D-06 decision. This packet does not cite live `pinn/` code and does not use live code as grounding.
- Not FUT-applicable: Phase 32 creates evidence artifacts only.

## First-Principles or Engineering Check

The engineering distinction is between the differentiable training loss and offline/static diagnostics:

- The training physics residual and energy regularizer need one matched Plummer form with one `epsilon_train = 1e-5` so force and Hamiltonian terms are internally consistent and numerically regularized during optimization.
- Static invariant and data-side validation quantities are offline measurements. Keeping `epsilon_inv = 1e-10` preserves a near-unsoftened diagnostic; collapsing it to `1e-5` aligns the diagnostic with the training softening but changes the measured energy/IPR convention and may affect stage or quality gates.
- Option C, `1e-10` everywhere, conflicts with the locked loss-side `epsilon_train = 1e-5` contract unless the owner explicitly reopens that contract.

The sources therefore support recording the locked loss-side convention, but they do not provide sensitivity evidence or explicit owner instruction for the static/invariant choice.

## Verdict

Verdict: defer-with-blocker

Explicit user instruction: None

Reasoning:

- The issue doc explicitly marks D-06 as awaiting human approval and lists three strategies whose consequences cross invariant computation, stage assignment, physics residual loss, and energy loss.
- The candidate verdict source narrows the open decision: loss-side `epsilon_train = 1e-5` is locked, while the static/invariant context remains owner-routed.
- Current specs already display a dual-context baseline, but existing text is evidence of present state, not a grounded owner decision that Phase 32 may silently canonize.
- Under AGENTS.md and the Phase 32 protocol, Phase 32 may not choose between retaining `epsilon_inv = 1e-10` and collapsing static invariants to `1e-5` without explicit instruction or new grounding.

## Root-Cause Ambiguity

The ambiguity is an epsilon-context collision. The same "softening" word appears in static invariant calculations, validation diagnostics, physics residuals, and energy loss. The loaded sources lock the training loss form, but they preserve the static/invariant epsilon as an owner decision because changing it alters what offline measurements mean.

## Locked Convention or Owner Route

Owner route and blocker:

- Locked immediately: Phase 35 loss-side contracts retain `epsilon_train = 1e-5`, matched-Plummer, identically in physics residual and energy unless the owner explicitly reopens the loss contract.
- Primary owner for the open decision: Phase 33 static invariants, because the unresolved choice is whether offline invariant and data-side validation contexts retain `epsilon_inv = 1e-10` or collapse to `1e-5`.
- Phase 35 consumer: loss consistency text may cite this packet for the locked `epsilon_train = 1e-5` convention, but must not infer the static/invariant choice from the loss-side lock.
- Blocker: the framework owner must choose the static/invariant epsilon strategy or authorize a sensitivity study before Phase 33 transcribes final static-invariant behavior.

No downstream phase should treat the D-06 static epsilon choice as resolved from this packet alone.

## Which Source Was Correct / Wrong

- The issue doc is correct that D-06 spans multiple framework components and requires owner approval.
- The candidate verdict source is correct to narrow the unresolved choice to static/invariant context and to mark `epsilon_train = 1e-5` as locked on the loss side.
- Neither source supplies a final static/invariant owner selection. The resolution doc's report references are provenance, not votes, and no attached sensitivity study resolves `epsilon_inv = 1e-10` versus `1e-5` for offline measurements.

## Before / After or Intentional Non-Change Note

Intentional Phase 32 non-change: no framework spec section is edited in this plan. The downstream "after" state is blocked until the owner selects the static/invariant epsilon strategy. Phase 33 must not finalize static invariant behavior from this packet alone; Phase 35 may preserve the locked loss-side `epsilon_train = 1e-5` contract without resolving the static choice.

## Named Acceptance Check

`AC-EVID-15-D06`

Planned pass criterion: this packet must cite issue-doc D-06 options, final-resolution section 1.3, `EPS-01..05`, `DGR-04`, `GAP-04`, and current dual-epsilon spec text; record `defer-with-blocker`; preserve `epsilon_train = 1e-5` as locked for loss/residual/energy; and route the unresolved static `epsilon_inv = 1e-10` versus `1e-5` decision to downstream owner handling.

Owning phase: Phase 32 for packet coverage; Phase 36 for final structural verification.

## STOP / Gap Handling

No STOP gap opened. The known D-06 owner routing is already specified by the Phase 32 plan and protocol, and this packet preserves it as `defer-with-blocker` without selecting a static epsilon default. No new source-silent semantic question beyond that known owner route was encountered.

## Status Transition Log

```text
2026-06-21 pending-commit PENDING -> DEFERRED (Phase 32 Plan 32-03 Task 3 by codex-gsd-executor-32-03)
```
