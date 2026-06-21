# Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication - Context

**Gathered:** 2026-06-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 32 builds the v1.6 adjudication machinery and records root-cause evidence for the headline issue-03 conflicts. It produces process/evidence artifacts only: evidence packet schema, protocol, stable issue ledger, headline conflict records, STOP/gap handling, and structural verification. It does not transcribe contract edits into framework specs; Phases 33-35 do that, and Phase 36 executes final acceptance checks and handoff.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**7 requirements are locked.** See `32-SPEC.md` for full requirements, boundaries, edge coverage, prohibitions, and acceptance criteria.

Downstream agents MUST read `32-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Create Phase 32 spec/discussion/plan-input artifacts under `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/`.
- Adapt the v1.5 evidence-packet template and protocol to issue-03 / v1.6.
- Create the Phase 32 issue ledger stable path and lifecycle rules.
- Author evidence packets and verdict records for D-04, D-05, D-06, M14, and the `D = 6.694` conflict.
- Record STOP/gap entries for source-silent semantic decisions or locked-convention overturn attempts.
- Define deterministic checks for Phase 32 artifacts.
- Route downstream work to Phases 33-36 without doing the contract edits here.

**Out of scope (from SPEC.md):**
- Editing `ctl_instruction.md` or `pinn_architecture.md`.
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md`.
- Editing or using `pinn/` live code as grounding.
- Implementing DataLoader, training loop, ALM, causal windows, or gradient clipping code.
- Running adaptive-stage EDA, Stage-0 pilot calibration, or dataset regeneration.
- Running plan-phase or creating `32-*-PLAN.md` during this spec/discussion workflow.
- Resolving D-04/D-05/D-06 by assumption.

</spec_lock>

<decisions>
## Implementation Decisions

### Artifact Topology
- **D-01:** Use the v1.5 Phase 25 pattern as the implementation baseline: a phase-local evidence directory, an evidence-packet template, a protocol README, a stable issue ledger, and later verification/validation artifacts in the Phase 32 directory.
- **D-02:** Keep Phase 32 artifacts process-local. The only acceptable cross-file planning mutations are STOP/gap register updates if a source-silent semantic decision is encountered.
- **D-03:** Do not update `.planning/STATE.md` directly in this discussion run because GSD's `gsd-tools.cjs` is currently failing and the existing `STATE.md` modification is user-owned.

### Headline Conflict Handling
- **D-04:** Create separate evidence packets for D-04 causal-training mode, D-05 `s_min` frame, D-06 epsilon strategy, M14 gradient clipping, and the `D = 6.694` conflict. Do not collapse these into one umbrella packet; each has different downstream owners and different STOP risk.
- **D-05:** Treat D-04/D-05/D-06 as owner-routed semantic decisions. If no explicit prior user instruction resolves one at Phase 32 execution time, the packet records `defer-with-blocker` or an OPEN STOP gap instead of selecting a default.
- **D-06:** Treat the `D = 6.694` conflict as constrained by v1.5 Phase 25 EVID-10 and SCOPE-12: `D = (G*T^2)^(1/3) ~= 4.6416` stands unless Phase 32 surfaces a genuine first-principles contradiction and obtains user instruction.
- **D-07:** Treat M14 as a split record: Phase 32 can lock the structural merge (`clip_value = C_stage * median(recent global gradient norms)`) if grounded, while bootstrap floor, early-stage exact `C`, and history-reset mechanics remain downstream/FUT if source-silent.

### Ledger and Verification
- **D-08:** Seed the ledger with every selected issue-03 finding consumed by Phases 32-36, not just the five headline conflicts. Headline packets are Phase 32-owned; remaining packets may be authored by owning contract phases immediately before their edits, matching the v1.5 split-reading precedent.
- **D-09:** Preserve the lifecycle invariant exactly: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` or `DEFERRED`; `FIX_APPLIED` is never terminal.
- **D-10:** Phase 32 must include deterministic structural checks for packet schema, protocol lifecycle, ledger row coverage, headline verdict/defer coverage, no forbidden spec edits, and absence of `32-*-PLAN.md` before this workflow stops.

### Planning Boundary
- **D-11:** Auto-advance is intentionally stopped after discussion because the user explicitly requested "stop before planning phase starts." No `32-*-PLAN.md` should exist at the end of this run.

### the agent's Discretion
- Exact packet filename slugs, as long as they are stable, grep-friendly, and mapped in the protocol.
- Exact Markdown table layout for the ledger, as long as required fields and lifecycle states are present.
- Exact shell commands used for structural checks, as long as they are deterministic and recorded.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase Requirements
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-SPEC.md` - Locked Phase 32 requirements, boundaries, acceptance criteria, edge coverage, prohibitions, and ambiguity report.
- `.planning/ROADMAP.md` - v1.6 roadmap; Phase 32 goal, dependencies, success criteria, verification protocol, and downstream phase boundaries.
- `.planning/REQUIREMENTS.md` - EVID-11 through EVID-15, SCOPE-12 through SCOPE-15, and v1.6 traceability.
- `.planning/PROJECT.md` - standing source-treatment, no-live-code, STOP, and current-milestone context.

### Issue-03 Sources
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` - Non-authoritative issue doc; source positions for D-04, D-05, D-06, M14, and `D = 6.694` claims.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` - Candidate verdict source; sections 1.1, 1.2, 1.3, 1.8, and 1.16 are the headline Phase 32 anchors.
- `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` - Quick-reference line map, status table, caveat routing, and downstream ownership.
- `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md` - READY-WITH-CAVEATS gate result and caveat list.

### Framework and Locked Conventions
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Current editable framework spec; Phase 32 may cite as current-spec evidence but must not edit.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - Current editable architecture spec; Phase 32 may cite as current-spec evidence but must not edit.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` - v1.5 EVID-10 precedent for the `D = 6.694` conflict and dimensional-analysis reasoning.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md` - Evidence-packet schema precedent.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md` - Protocol, verdict enum, lifecycle, regression policy, and packet-start precedent.

### Prior Phase Context
- `.planning/phases/30-research-package-assembly/30-CONTEXT.md` - Research package delivery and external gate-opening context.
- `.planning/phases/31-resolution-doc-readiness-verification/31-CONTEXT.md` - Readiness verification decisions and map-consumption guidance.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md`: closest packet-template precedent; adapt paths, source roles, and EVID numbering to v1.6.
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/README.md`: closest protocol precedent; adapt lifecycle, trigger table, packet-start procedure, and phase-exit rules.
- `scripts/agent-commit`: required commit wrapper for agent-authored commits, with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`.

### Established Patterns
- Planning artifacts live under `.planning/phases/{phase}-{slug}/` for active work and `.planning/milestones/vX.Y-phases/` for archived precedents.
- Evidence-first adjudication precedes spec edits; downstream contract phases cite packet records rather than re-deciding the source question.
- Live `pinn/` code is forward-handoff context only, never grounding evidence for v1.6 adjudication.
- STOP gaps are phase-local plus milestone-indexed; source-silent semantic choices do not become defaults.

### Integration Points
- Phase 33 consumes curriculum-stage verdicts and any D-05/D-06 outcomes that affect stage gates.
- Phase 34 consumes batch-construction, M14, ALM, and training-loop verdicts.
- Phase 35 consumes D-04, loss-scaling, energy-weight, and Huber-delta verdicts.
- Phase 36 consumes the ledger, packet links, verification commands, and unresolved/deferred blocker list.

</code_context>

<specifics>
## Specific Ideas

- The user asked for careful mathematical, physics, and engineering grounding. Phase 32 should explicitly articulate first-principles reasoning where it adjudicates, especially for dimensional analysis (`D`) and softening/gate distinctions.
- Auto-mode choices are conservative: select artifact/process defaults, but do not select semantic physics/training-mode outcomes that the sources route to the owner.

</specifics>

<deferred>
## Deferred Ideas

- Framework-spec contract transcription is deferred to Phases 33, 34, and 35.
- Runnable acceptance execution and milestone handoff are deferred to Phase 36.
- Training-loop/DataLoader/ALM implementation, adaptive-stage EDA, Stage-0 pilot calibration, and data regeneration remain FUT-01/FUT-04/FUT.

</deferred>

---

*Phase: 32-evidence-framework-issue-ledger-conflict-adjudication*
*Context gathered: 2026-06-21*
