# Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication - Specification

**Created:** 2026-06-21
**Ambiguity score:** 0.09 (gate: <= 0.20)
**Requirements:** 7 locked

## Goal

Phase 32 establishes the v1.6 adjudication machinery and records root-cause verdicts for the five headline conflicts before any Phase 33-35 framework-spec edit may land.

## Background

v1.6 is the curriculum-and-training-loop adjudication milestone for `pinn_instruction/issues/03-curriculum-and-training-loop.md`. Phases 30 and 31 are complete: Phase 30 delivered the research package and opened the external-resolution gate, and Phase 31 verified the consolidated resolution doc as READY-WITH-CAVEATS with downstream ownership for the remaining caveats.

The current roadmap defines Phase 32 as the evidence-framework phase. Its deliverables are evidence-packet machinery, a stable issue ledger, and root-cause adjudication of D-04 causal-training mode, D-05 `s_min` frame, D-06 epsilon strategy, M14 gradient clipping, and the `D = 6.694` versus v1.5-locked `D ~= 4.6416` conflict. The contract-edit phases consume Phase 32's verdicts: Phase 33 owns curriculum-stage contracts, Phase 34 owns training-loop and batch-construction contracts, Phase 35 owns loss and energy-weight contracts, and Phase 36 owns acceptance execution and handoff.

The Phase 31 resolution map is the navigation contract for the consolidated resolution doc. It maps D-04 to `03-final-resolution.md` section 1.1, D-05 to section 1.2, D-06 to section 1.3, M14 to section 1.8, and the locked `D` conflict to section 1.16. The same map records D-04/D-05/D-06 as `surface_to_user`, M14 as `modified`, and the `D` conflict as `accepted` for `4.6416` and `rejected` for `6.694`.

The v1.5 Phase 25 evidence framework is the closest precedent: it used a packet template, a protocol README, a stable issue ledger, a fixed five-value verdict enum, and a rule that `FIX_APPLIED` is not closure. Phase 32 adapts that machinery for issue-03 and v1.6's SCOPE-12/SCOPE-13/SCOPE-14/SCOPE-15 constraints. Phase 32 does not edit `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, `stage-strat-revision.md`, or `pinn/`.

## Requirements

1. **Phase scaffold and zero-edit boundary**: Phase 32 creates its phase-local adjudication artifacts under `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/` while preserving unrelated user-owned work and making no framework-spec edits.
   - Current: The v1.6 roadmap and requirements define Phase 32, but no Phase 32 artifact directory or `32-SPEC.md` existed before this spec-phase run.
   - Target: The phase directory contains this SPEC and later Phase 32 artifacts; any execution artifacts are limited to `.planning/phases/32-*` and milestone gap/index files when STOP protocol requires them.
   - Acceptance: `git diff --name-only` for the spec-phase commit contains only `32-SPEC.md`; later Phase 32 execution diffs contain no `pinn_instruction/markdown_conversion/framework-specs/*.md`, read-only report edits, or `pinn/` production-code edits.

2. **Evidence-packet schema and protocol**: Phase 32 adapts the v1.5 Phase 25 evidence-packet template and protocol for issue-03.
   - Current: v1.5 has an archived `_TEMPLATE.md` and protocol README for issue-02; issue-03 has no active v1.6 packet schema yet.
   - Target: Phase 32 defines a v1.6 packet template and protocol with the fixed verdict enum (`accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`), line-range citation rules, SCOPE-12 grounding, SCOPE-13 edit-target boundaries, no-live-code grounding, and issue-03 source paths.
   - Acceptance: The template/protocol artifacts exist, name issue-03 sources and the final resolution doc, preserve the five verdict values exactly, require line-range citations rather than whole-file citations, and explicitly ban `pinn/` live code as grounding evidence.

3. **Stable issue ledger**: Phase 32 creates a stable issue ledger seeded with every selected issue-03 finding and the v1.6 lifecycle rules.
   - Current: The roadmap says the ledger lives under Phase 32, but no Phase 32 ledger exists.
   - Target: The ledger lists every selected finding used by Phases 32-36, including at minimum B-07, B-08, M6, M7, M14, M15, M16, D-04, D-05, D-06, NS-12, NS-13, NS-18, the `D = 6.694` conflict, and any Phase 31 caveat rows carried into downstream work.
   - Acceptance: The ledger has exactly the statuses `PENDING`, `IN_PROGRESS`, `FIX_APPLIED`, `VERIFIED`, and `DEFERRED`; each row has an owner phase, evidence-packet field, verdict field, acceptance-check field, dependents field, and transition log; no row may close at `FIX_APPLIED`.

4. **Headline-conflict evidence packets**: Phase 32 authors root-cause evidence packets and verdict records for D-04, D-05, D-06, M14, and the `D = 6.694` conflict before downstream spec edits begin.
   - Current: Phase 31 mapped the resolution-doc sections and caveats, but the Phase 32 EVID-15 records do not yet exist.
   - Target: The five headline conflicts each have an evidence packet citing issue-doc lines, resolution-doc lines, current-spec evidence, v1.4/v1.5 locked conventions, and first-principles or dataset evidence where relevant.
   - Acceptance: Each packet contains side-by-side source positions, a verdict from the fixed enum or a `defer-with-blocker`, a root-cause ambiguity section, a locked-convention/non-change or before-after note, a consumer phase, and a named acceptance-check handoff.

5. **STOP-safe owner-decision handling**: Phase 32 surfaces source-silent owner decisions and locked-convention overturn attempts instead of selecting semantic defaults in auto mode.
   - Current: D-04, D-05, and D-06 are `surface_to_user` decisions in the Phase 31 map; the consolidated resolution doc states positions and options but does not make the owner selection.
   - Target: If no prior user instruction resolves D-04/D-05/D-06 at Phase 32 execution time, the affected packet records `defer-with-blocker` or an OPEN STOP-gap entry with all required fields, and dependent Phase 33-35 work remains blocked only where it depends on the unresolved choice.
   - Acceptance: The Phase 32 artifacts contain no autonomous selection of causal-training mode, `s_min` gate frame, or static epsilon strategy unless backed by explicit user instruction, a prior locked decision, or first-principles evidence sufficient under AGENTS.md; any unresolved owner decision is present in `32-GAPS.md` and `.planning/milestones/v1.6-GAPS.md`.

6. **Before/after and downstream routing**: Phase 32 records what downstream contract phases must do with each adjudicated finding without performing those edits itself.
   - Current: The roadmap assigns contract transcription to Phases 33-35 and acceptance execution to Phase 36, but Phase 32 still needs the records those phases consume.
   - Target: Every accepted, deferred, or unresolved finding has a before/after or intentional non-change note naming the relevant spec section, owning downstream phase, acceptance-check identity, and regression dependents.
   - Acceptance: Phase 32 artifacts can be used by Phase 33, 34, 35, and 36 without re-asking what the finding is, why it was accepted or deferred, or which artifact consumes it; no Phase 32 artifact instructs a downstream phase to treat an unresolved STOP decision as resolved.

7. **Structural verification of Phase 32 artifacts**: Phase 32 defines and runs deterministic checks for the machinery and headline records.
   - Current: No Phase 32 validation commands or checks exist.
   - Target: Phase 32 includes a validation artifact or verification section with deterministic checks for template sections, protocol lifecycle values, ledger row coverage, evidence-packet links, verdict coverage for the five headline conflicts, no forbidden spec edits, and no unresolved `FIX_APPLIED` rows.
   - Acceptance: The checks run successfully before Phase 32 closes; failures identify the artifact and invariant that failed, and Phase 32 remains open until all in-scope machinery and headline-conflict records satisfy their structural checks or are explicitly deferred with blockers.

## Boundaries

**In scope:**

- Create Phase 32 spec/discussion/plan-input artifacts under `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/`.
- Adapt the v1.5 evidence-packet template and protocol to issue-03 / v1.6.
- Create the Phase 32 issue ledger stable path and lifecycle rules.
- Author evidence packets and verdict records for D-04, D-05, D-06, M14, and the `D = 6.694` conflict.
- Record STOP/gap entries for source-silent semantic decisions or locked-convention overturn attempts.
- Define deterministic checks for Phase 32 artifacts.
- Route downstream work to Phases 33-36 without doing the contract edits here.

**Out of scope:**

- Editing `ctl_instruction.md` or `pinn_architecture.md` - contract transcription belongs to Phases 33-35.
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md` - frozen/read-only by scope policy.
- Editing or using `pinn/` live code as grounding - live code is non-authoritative and FUT-only.
- Implementing DataLoader, training loop, ALM, causal windows, or gradient clipping code - FUT-01/FUT-04.
- Running adaptive-stage EDA, Stage-0 pilot calibration, or dataset regeneration - FUT/SCOPE-15.
- Running plan-phase or creating `32-*-PLAN.md` during this spec/discussion workflow - user requested stop before planning starts.
- Resolving D-04/D-05/D-06 by assumption - these are semantic owner decisions unless explicit grounding exists.

## Constraints

- Work happens in `<home>/Desktop/3_body_problem/.worktrees/specwork` on branch `milestone/v1.6`.
- Existing unrelated modification to `docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md` is user-owned and must not be staged or rewritten by Phase 32.
- Phase 32 follows AGENTS.md STOP protocol for v1.6 adjudication milestones.
- Evidence packets cite line ranges, not whole files.
- The resolution doc is a candidate verdict source, not authority; independent grounding is required before a verdict.
- Locked v1.4/v1.5 conventions are hard constraints unless a STOP-worthy first-principles conflict is surfaced and resolved by user instruction.
- `FIX_APPLIED` is never terminal; closure requires `VERIFIED` or `DEFERRED`.
- GSD helper `gsd-tools.cjs` is currently unavailable in this environment because its packaged `package.json` dependency is missing; manual workflow execution must preserve the same artifacts and checks.

## Acceptance Criteria

- [ ] `32-SPEC.md` exists and locks Phase 32 requirements, boundaries, constraints, acceptance criteria, edge coverage, prohibitions, and ambiguity report.
- [ ] Phase 32 execution creates issue-03 evidence-packet template/protocol artifacts with the five fixed verdict values and line-range citation requirement.
- [ ] Phase 32 execution creates a stable issue ledger under the Phase 32 directory with all selected findings, lifecycle statuses, owner phases, evidence-packet links, verdict fields, and transition logs.
- [ ] Evidence packets exist for D-04, D-05, D-06, M14, and the `D = 6.694` conflict, each with source positions, root-cause ambiguity, verdict/defer status, and downstream routing.
- [ ] D-04/D-05/D-06 are not resolved by autonomous assumption; if no explicit instruction exists, corresponding STOP/gap entries are recorded and dependent downstream work is blocked.
- [ ] Phase 32 artifacts contain no edits to framework specs, read-only reports, or `pinn/` production code.
- [ ] Structural verification commands for the Phase 32 artifacts pass, or every failure is converted into a written blocker before the phase can close.
- [ ] Spec-phase and discussion-phase work stops before any Phase 32 planning artifact is created.

## Edge Coverage

**Coverage:** 26/26 applicable edges resolved - 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| idempotency | R1 | backstop | Re-running spec/discussion must update or preserve Phase 32 artifacts without duplicating sections; verify with path-level diff review. |
| concurrency | R1 | covered | Worktree and dirty-file constraints require preserving unrelated user-owned work and staging explicit paths only. |
| adjacency | R2 | covered | Template/protocol adaptation must distinguish issue-doc, resolution-doc, current-spec, and locked-convention evidence instead of merging adjacent source roles. |
| empty | R2 | covered | Template/protocol fails if required sections, verdict enum values, or source-path entries are absent. |
| encoding | R2 | covered | Verdict values and lifecycle states are literal ASCII tokens and must match exactly. |
| ordering | R2 | covered | Protocol section order and packet-start procedure follow the established Phase 25 precedent. |
| adjacency | R3 | covered | Ledger rows for closely related findings remain distinct unless an explicit close-with-parent relationship is recorded. |
| empty | R3 | covered | Empty or unseeded ledger is invalid; selected findings must be present before downstream phases consume it. |
| ordering | R3 | covered | Ledger preserves deterministic finding order by issue/phase grouping so re-verification dependencies are reviewable. |
| idempotency | R3 | backstop | Re-running ledger generation must not reset nonterminal transition logs; structural checks review duplicate headings and status tokens. |
| concurrency | R3 | covered | Ledger edits happen in the same commit as packets/status changes that they mirror. |
| adjacency | R4 | covered | D-04/D-05/D-06/M14/D-conflict packets are separate records with separate verdict/defer states. |
| empty | R4 | covered | Missing packet for any headline conflict blocks Phase 32 closure. |
| encoding | R4 | covered | `D = 6.694`, `D ~= 4.6416`, verdict tokens, and finding IDs must be represented consistently for search and verification. |
| ordering | R4 | covered | Headline packets are produced before Phase 33-35 spec edits consume their verdicts. |
| idempotency | R5 | covered | STOP/gap entries must not be silently overwritten by later auto-mode reruns; resolution notes require explicit instruction. |
| concurrency | R5 | covered | Dependency-scoped blocking allows independent records to proceed while affected downstream work remains halted. |
| adjacency | R6 | covered | Accepted, deferred, unresolved, and intentional non-change cases have distinct routing notes. |
| empty | R6 | covered | Every headline record must name a consumer phase or blocker. |
| ordering | R6 | covered | Before/after/non-change notes precede downstream transcription and Phase 36 acceptance execution. |
| idempotency | R6 | backstop | Re-runs must preserve prior transition history; verifier checks transition-log presence. |
| concurrency | R6 | covered | Dependent re-verification policy prevents a later edit batch from silently invalidating previously verified rows. |
| adjacency | R7 | covered | Checks distinguish schema, ledger, packet, verdict, and forbidden-edit invariants. |
| empty | R7 | covered | A missing validation artifact or empty check list blocks closure. |
| ordering | R7 | covered | Checks run after artifact creation and before Phase 32 closure. |
| concurrency | R7 | covered | `git diff --name-only` and explicit staging checks prevent unrelated dirty work from entering the commit. |

## Prohibitions (must-NOT)

**Coverage:** 7/7 applicable prohibitions resolved - 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT edit `ctl_instruction.md` or `pinn_architecture.md` during Phase 32. | R1, R6 | resolved / test | `git diff --name-only` must show no framework-spec path for the Phase 32 machinery/spec commits. |
| MUST NOT edit `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md`. | R1 | resolved / test | Same forbidden-path diff check; these files are frozen/read-only by scope. |
| MUST NOT use `pinn/` live code as grounding evidence. | R2, R4 | resolved / judgment | Template/protocol must label any live-code mention as FUT handoff only, never evidence. |
| MUST NOT treat the resolution doc as authoritative. | R2, R4 | resolved / judgment | Protocol and packets must require independent grounding before accepting a resolution-doc position. |
| MUST NOT silently select D-04, D-05, or D-06 in auto mode. | R5 | resolved / judgment | If no explicit user decision exists, packets/gaps must remain unresolved or `defer-with-blocker`; reviewer checks gap register and packet verdicts. |
| MUST NOT close any finding at `FIX_APPLIED`. | R3, R7 | resolved / test | Ledger lifecycle check fails if any in-scope terminal row is `FIX_APPLIED`. |
| MUST NOT create Phase 32 planning artifacts during this spec/discussion run. | R7 | resolved / test | Before final response, verify no `32-*-PLAN.md` exists. |

## Ambiguity Report

| Dimension | Score | Min | Status | Notes |
|-----------|-------|-----|--------|-------|
| Goal Clarity | 0.94 | 0.75 | met | Roadmap explicitly names machinery, ledger, and headline conflicts. |
| Boundary Clarity | 0.92 | 0.70 | met | Zero framework-spec edits; contract edits routed to Phases 33-35; acceptance to Phase 36. |
| Constraint Clarity | 0.88 | 0.65 | met | SCOPE-12 through SCOPE-15, no-live-code rule, STOP protocol, and worktree constraints are explicit. |
| Acceptance Criteria | 0.90 | 0.70 | met | Pass/fail artifact and structural verification criteria are defined. |
| **Ambiguity** | 0.09 | <=0.20 | met | Gate passed after auto exploration and edge/prohibition probes. |

Status: met = dimension meets the workflow minimum; no dimension is below minimum.

## Interview Log

Auto mode was requested (`--auto`), so the workflow did not stop for interactive questions. The following decisions were auto-selected from repository context, with STOP-protocol limits preserved.

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | What exists today for Phase 32? | Roadmap/requirements exist in the v1.6 specwork worktree; Phase 30/31 artifacts and final resolution doc exist; Phase 32 artifacts do not. |
| 1 | Researcher | What is the delta? | Create Phase 32 machinery and headline conflict records; do not edit framework specs. |
| 2 | Simplifier | What is the irreducible core? | Evidence template/protocol, issue ledger, five headline conflict packets/verdicts, STOP/gap handling, structural checks. |
| 3 | Boundary Keeper | What is explicitly excluded? | Framework-spec edits, production code, data regeneration, EDA/pilot calibration, and plan-phase artifacts. |
| 4 | Failure Analyst | What would make this phase invalid? | Silent D-04/D-05/D-06 default selection, treating the resolution doc as authority, missing ledger lifecycle, forbidden spec edits, or closing at `FIX_APPLIED`. |
| 5 | Seed Closer | What ambiguity remains? | Only execution-time owner decisions remain; the spec requires surfacing them rather than resolving them here. |

---

*Phase: 32-evidence-framework-issue-ledger-conflict-adjudication*
*Spec created: 2026-06-21*
*Next step: $gsd-discuss-phase 32 --auto - implementation decisions (how to build what is specified above)*
