# Phase 36: Acceptance Checks, Re-verification & Handoff - Context

**Gathered:** 2026-06-30
**Refreshed:** 2026-06-30 (`$gsd-discuss-phase 36 --all --auto --analyze`) - re-grounded against the post-Phase-35 codebase after the SPEC re-grounding: SI universe corrected to four IDs (added `SI-DQA-003`), the ROADMAP/REQUIREMENTS traceability reconciliation now flagged in scope (grounded by `34-VERIFICATION.md:102`), and the `D-05`/`D-06` closure path made explicit. No locked SPEC requirement changed.
**Status:** Ready for planning
**Mode:** `$gsd-discuss-phase 36 --all --auto --analyze` - all gray areas auto-selected and recommended implementation defaults chosen; trade-off rationale logged in `36-DISCUSSION-LOG.md`. Per the standing user instruction (and D-36-16), this run stops before plan-phase starts - auto-advance is intentionally suppressed.

<domain>
## Phase Boundary

Phase 36 delivers the v1.6 closure packet: a Phase 36-owned acceptance-check manifest, fresh disposable probe evidence, terminal ledger/SI verification, and a FUT-01/FUT-04 handoff for the curriculum/training-loop milestone.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `36-SPEC.md` for full requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `36-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Create Phase 36 closure artifacts under `.planning/phases/36-acceptance-checks-re-verification-handoff/`.
- Create `36-ACCEPTANCE-MANIFEST.md` as the Phase 36-owned contract check inventory.
- Execute fresh disposable Phase 36 probes and record `36-PROBE-RESULTS.md` plus raw evidence hashes.
- Write `36-VERIFICATION.md` with traceability, manifest, probe, ledger, SI, and handoff checks.
- Verify and, if a Phase 36 plan explicitly permits it, update the Phase 32 issue ledger to terminal states.
- Reconcile the `.planning/REQUIREMENTS.md` traceability Status column and the `.planning/ROADMAP.md` progress table to ledger-terminal values (R6; user-confirmed scope, see D-36-17).
- Reconcile current `SI-*` entries relevant to curriculum/training-loop closure inside `36-HANDOFF.md`.
- Write `36-HANDOFF.md` with fixed/unchanged/deferred findings and FUT-01/FUT-04 dispositions.
- Use prior Phase 21 and Phase 29 closure patterns as precedent for probe results, evidence hashes, SI reconciliation, and handoff structure.

**Out of scope (from SPEC.md):**
- Implementing DataLoader, training-loop, ALM, causal-window, gradient-clipping, or model code - v1.6 is specwork-only; implementation is FUT-01/FUT-04.
- Using live `pinn/` code as grounding or probe target - `pinn/` is explicitly non-grounding for v1.6.
- Re-opening v1.4/v1.5 locked conventions - SCOPE-12 makes them hard constraints unless a STOP gap is explicitly resolved.
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, or `stage-strat-revision.md` - SCOPE-08/SCOPE-09 keep them frozen/read-only.
- Re-deciding semantic physics/training-loop gaps without source grounding - STOP protocol governs any source-silent semantic/process-schema choice.
- Folding unrelated user-owned working-tree changes into Phase 36 commits (currently `AGENTS.md`; the earlier dirty Phase 35 plan/review edits are now committed) - those changes are user-owned unless separately authorized.
- Starting planning during this spec/discuss run - the user explicitly requested stopping before plan-phase starts.

</spec_lock>

<decisions>
## Implementation Decisions

### Closure Packet Topology
- **D-36-01:** Use a four-artifact Phase 36 closure packet: `36-ACCEPTANCE-MANIFEST.md`, `36-PROBE-RESULTS.md`, `36-VERIFICATION.md`, and `36-HANDOFF.md`.
- **D-36-02:** Put raw probe output under a Phase 36 evidence directory and record SHA-256 hashes in `36-PROBE-RESULTS.md`, following the Phase 21 closure pattern.
- **D-36-03:** Keep SI reconciliation inside `36-HANDOFF.md` rather than creating a separate SI report, because the SPEC locked the closure-packet shape and downstream agents should have one handoff source.

### Probe Execution Strategy
- **D-36-04:** Prefer small, disposable spec-consistency and formula-sanity probes over replaying every historical Phase 33-35 command. Cite prior phase verification as provenance, but make Phase 36 evidence fresh.
- **D-36-05:** Model probes after the repository's manual accumulator style: deterministic commands, PASS/FAIL labels, explicit stderr/stdout capture, and nonzero exit when required closure checks fail.
- **D-36-06:** The planner must include a protected-path check proving probes do not execute against or modify live `pinn/` production code.

### Ledger and SI Closure
- **D-36-07:** Treat all in-scope Phase 32 ledger rows as requiring terminal state. Current known blocker shape: `D-05` and `D-06` are still `PENDING` (owned by Phase 32; their owner verdicts are already `RESOLVED-WITH-INSTRUCTION` in `32-GAPS.md`, and downstream transcription was Phase 33/35-owned — both now complete). Recommended closure path: a Phase 36 plan verifies that the locked `D-05`/`D-06` verdicts are correctly transcribed in their downstream spec sections (Phase 33 CURR-05 geometric `s_min` gate; Phase 35 loss-side matched-Plummer references) and, if clean, promotes both to `VERIFIED` via an explicit owned-path ledger edit; if transcription is missing or divergent, Phase 36 records `BLOCKED` and routes back rather than promoting. This is fail-closed and consistent with the SPEC's "verify and, if a plan permits, update the ledger to terminal" boundary — it is NOT a re-litigation of the locked verdicts.
- **D-36-08:** Parse ledger status fresh during verification and report exact counts. Do not trust stale summaries or manually edited counts.
- **D-36-09:** Reconcile every current framework-spec `SI-*` hit from `ctl_instruction.md` and `pinn_architecture.md`. A fresh `rg -n "SI-[A-Z]+-[0-9]+"` returns **four** distinct IDs: `SI-CTL-001` (resolved, Phase 17/B-03), `SI-PINN-002` (documented-for-future), `SI-PINN-003` (resolved, Phase 34; canonical contract in `ctl_instruction.md`, pointer in `pinn_architecture.md`), and `SI-DQA-003` (`ctl_instruction.md:548`, inline conservation/SCS-gate citation, "locked post-v1.3", data-quality lineage). The earlier three-ID list omitted `SI-DQA-003`; the reconciliation table must cover all four, and the mechanical acceptance check is the fresh grep over both specs (SPEC Requirement 4 / VER-18).
- **D-36-10:** A resolved/retired SI row needs a phase/commit back-reference; a preserved row needs a written reason and downstream owner. No row may be assumed irrelevant.
- **D-36-17:** Reconciling the stale `.planning/REQUIREMENTS.md` traceability Status column and the `.planning/ROADMAP.md` progress table to their true terminal values is **in Phase 36's scope** — grounded by `34-VERIFICATION.md:102` ("ROADMAP reconciliation is deferred to Phase 36"; Phase 34 SCOPE-13 did not permit it then). Concretely: `LOOP-04`/`LOOP-07`/`LOOP-08` read `Pending` but are `VERIFIED`/`SATISFIED` in the ledger / `34-VERIFICATION.md`, and the ROADMAP progress table still shows Phase 34 "In Progress 1/5" and is dated 2026-06-23. The 32/32 traceability audit (R6/VER-14) is about the mapping; flipping these stale status flags to match the ledger is the closure-time reconciliation. **RESOLVED — user confirmed in scope 2026-06-30 ("yes and add it"); now codified in SPEC Requirement 6 (in-scope bullet + acceptance criterion + manual-edit constraint + fabricated-completion prohibition).** The plan therefore adds `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` to Phase 36's owned paths. Perform these edits **manually** (the gsd-tools state/roadmap mutating verbs emit malformed output in this repo), require each flipped flag to match a terminal Phase 32 ledger row, and diff before committing.
- **D-36-18:** `SI-DQA-003`'s disposition (retire-with-back-reference vs preserve-with-reason) is **not decided here** — it is a STOP-protocol-governed Issue-03-relevance judgment resolved during Phase 36 execution. Non-binding lean: preserve with reason (a data-quality/conservation-gate citation, locked post-v1.3, outside the curriculum/training-loop Issue-03 surface), but the executing plan must make the call against sources and, if genuinely source-silent, surface a STOP gap rather than invent the disposition.

### Handoff and Trainex Routing
- **D-36-11:** `36-HANDOFF.md` must classify each ledger row exactly once as fixed, intentionally unchanged, or deferred.
- **D-36-12:** FUT-01/FUT-04 handoff sections should route implementation-shaped findings to downstream work without implementing them in Phase 36.
- **D-36-13:** Fold `.planning/todos/pending/trainex-r1-research-handoff.md` only as a handoff input: mention it in the FUT/trainex routing section, but do not execute trainex research or user-facing external research tasks in Phase 36.

### Git and Workflow Hygiene
- **D-36-14:** Plan tasks must use explicit owned paths and `scripts/agent-commit`; broad staging is forbidden.
- **D-36-15:** Unrelated user-owned working-tree changes must be excluded from Phase 36 commits unless separately authorized. As of this refresh the only dirty file is `AGENTS.md` (the earlier Phase 35 plan/review edits are now committed); stage explicit owned paths only.
- **D-36-16:** This discuss run intentionally stops before planning. Do not invoke `$gsd-plan-phase` from the discuss auto-advance hook.

### the agent's Discretion

The planner may choose the exact number and grouping of Phase 36 plan files, the names of individual probe scripts, and whether the manifest is generated by a helper script or authored as markdown, as long as every locked acceptance criterion in `36-SPEC.md` is mechanically verifiable and the closure packet stays fail-closed.

### Folded Todos

- `.planning/todos/pending/trainex-r1-research-handoff.md` - Folded as a FUT/trainex handoff input only. It concerns review and external handoff of trainex-r1 research sub-packages; Phase 36 should reference it when writing FUT-01/FUT-04 routing, not execute the research package workflow.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase Requirements
- `.planning/phases/36-acceptance-checks-re-verification-handoff/36-SPEC.md` - Locked Phase 36 requirements, boundaries, acceptance criteria, edge coverage, prohibitions, and ambiguity report.
- `.planning/ROADMAP.md` - v1.6 roadmap; Phase 36 goal and dependency on Phases 32-35.
- `.planning/REQUIREMENTS.md` - `VER-13` through `VER-18`, SCOPE-12 through SCOPE-15, and 32/32 v1.6 traceability.
- `.planning/STATE.md` - Current position, v1.6 phase summary, and blockers/concerns.
- `AGENTS.md` - STOP protocol, v1.6 source hierarchy, specwork-only boundary, branch/worktree rules, and commit protocol.

### Ledger, Gaps, and Verification Sources
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` - Stable v1.6 issue ledger; Phase 36 terminal-state gate subject.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` - Phase 32 source-silent decisions consumed by downstream phases.
- `.planning/milestones/v1.6-GAPS.md` - Milestone-wide gap index; update if Phase 36 opens or resolves STOP gaps.
- `.planning/phases/33-curriculum-stage-contracts/33-VERIFICATION.md` - Phase 33 CURR closure evidence and ledger transitions.
- `.planning/phases/34-training-loop-batch-construction-contracts/34-VERIFICATION.md` - Phase 34 LOOP closure evidence and ledger transitions; line 102 explicitly defers ROADMAP/traceability reconciliation to Phase 36 (source for D-36-17).
- `.planning/phases/35-loss-energy-weight-contracts/35-VERIFICATION.md` - Phase 35 LOSS closure evidence and ledger transitions.

### Framework Specs and SI Metadata
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - CTL methodology, curriculum/training-loop contracts, and current `SI-CTL-001`, `SI-PINN-003` (canonical batch-construction contract), and `SI-DQA-003` (`:548` conservation-gate citation) source-issue metadata.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - PINN architecture, loss/training contracts, and current `SI-PINN-002` / `SI-PINN-003` source-issue metadata (the `SI-PINN-003` entry points to the canonical `ctl_instruction.md` contract).
- `pinn_instruction/issues/03-curriculum-and-training-loop.md` - Non-authoritative issue doc; useful for issue IDs and historical claims, not sufficient grounding by itself.
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` - Candidate verdict source for v1.6; not automatically authoritative.

### Closure Precedents
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-PROBE-RESULTS.md` - Probe result summary pattern with raw evidence hashes.
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-HANDOFF.md` - v1.4 handoff and SI reconciliation precedent, if present in the archived milestone.
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-VERIFICATION.md` - Requirement coverage pattern for closure verification.
- `.planning/milestones/v1.5-phases/29-acceptance-checks-reverification-handoff/29-VERIFICATION.md` - v1.5 acceptance/reverification handoff precedent, if present in the archived milestone.

### Handoff Inputs
- `.planning/todos/pending/trainex-r1-research-handoff.md` - Folded todo for FUT/trainex handoff routing only.
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` - External research workflow referenced by the folded trainex todo; do not execute during Phase 36 unless separately requested.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/agent-commit`: required commit wrapper for agent-authored commits; enforces `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`.
- `tests/test_phase12_validation.py`: manual content-integrity accumulator pattern (`PASS`/`FAIL`, result counts, explicit error list) suitable for Phase 36 disposable probe scripts.
- `tests/git_policy/test_git_policy.py`: `unittest` precedent for deterministic policy checks if a small Python test is preferable.
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/`: archived pattern for raw probe evidence files and hashes.

### Established Patterns
- Active phase artifacts live under `.planning/phases/{phase}-{slug}/`; archived milestone precedents live under `.planning/milestones/vX.Y-phases/`.
- Verification-before-closure: ledger rows change to terminal only after source-token/probe checks record PASS.
- Protected-path guards are expected around frozen/read-only files, live `pinn/`, and unrelated dirty files.
- There is no project-wide test runner; Phase 36 should use explicit commands captured in verification artifacts.

### Integration Points
- Phase 36 consumes Phase 32's ledger and gap registers, Phase 33/34/35 verification reports, and framework-spec `SI-*` sections.
- Phase 36 may update the Phase 32 ledger and framework-spec SI metadata only if the plan explicitly scopes those files and the STOP protocol does not block the decision.
- Phase 36 should hand off implementation-shaped items to FUT-01/FUT-04 and trainex, not implement or research them.

</code_context>

<specifics>
## Specific Ideas

- The closure manifest should be the planner's main organizing artifact: every probe, evidence file, ledger check, SI row, and handoff table should trace back to it.
- Treat `D-05` and `D-06` as visible current-state risks. They may be resolved before or during Phase 36 planning, but Phase 36 cannot close while they are still `PENDING` (see D-36-07 for the verify-and-promote-else-`BLOCKED` path).
- Stale closure-state to reconcile (D-36-17): `LOOP-04`/`LOOP-07`/`LOOP-08` show `Pending` in `REQUIREMENTS.md` though Phase 34 closed them `VERIFIED`/`SATISFIED`, and the `ROADMAP.md` progress table still reads Phase 34 "In Progress 1/5" (dated 2026-06-23). The traceability audit should surface these and the closure plan should flip them — manually — to match the ledger.
- The SI universe is four IDs, not three; `SI-DQA-003` was the previously-missed hit (D-36-09). Its disposition is STOP-governed and deferred to execution (D-36-18).
- The user explicitly requested stopping before planning starts in this run, so auto-mode's usual plan-phase dispatch is intentionally suppressed.

</specifics>

<deferred>
## Deferred Ideas

- Executing trainex-r1 external research handoff remains outside Phase 36; Phase 36 only records the FUT/trainex routing obligation.
- Training-loop/DataLoader/ALM implementation, adaptive-stage EDA, Stage-0 pilot calibration, and data regeneration remain FUT-01/FUT-04/FUT.

</deferred>

---

*Phase: 36-acceptance-checks-re-verification-handoff*
*Context gathered: 2026-06-30; refreshed 2026-06-30 (post-SPEC re-grounding — SI four-ID universe, ROADMAP/REQUIREMENTS reconciliation D-36-17, D-05/D-06 closure path D-36-07)*
