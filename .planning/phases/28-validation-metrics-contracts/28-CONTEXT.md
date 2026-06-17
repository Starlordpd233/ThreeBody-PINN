# Phase 28: Validation-Metrics Contracts - Context

**Gathered:** 2026-06-14
**Status:** Ready for planning
**Mode:** `--auto --all` - all gray areas auto-selected; recommended defaults chosen by Claude per explicit user instruction ("auto choose the default recommended options for all discussion questions and stop before the planning phase"). Auto-advance to plan-phase is intentionally suppressed. Decisions below are implementation/process defaults only; the locked requirements live in `28-SPEC.md`, the SCS verdict in `25-.../evidence/scs-thresholds.md`, the seeded metric rows in `24-ISSUE-LEDGER.md`, and the metric definitions in the read-only `data_quality_assessment.md`. **v1.5 STOP protocol applies in full — the un-adjudicated metric forks (Q-C2 SASD endpoints, Q-C3 IPR units, Q-C4 PSC composition) are NOT decided here.**

<domain>
## Phase Boundary

`ctl_instruction.md` / `pinn_architecture.md` carry one canonical, data-side contract for each of the four validation metrics, threshold-aligned to the locked post-v1.3 gate and the v1.4 physics outcomes, with all training-loop usage deferred to doc-03:

1. **VAL-01 / SCS** (Symplectic Conservation Score; Q-C1) - one canonical definition + threshold aligned to the locked post-v1.3 gate (`\epsilon_H > 10^{-5}` / `SCS > -5`); the issue-02 ratio thresholds (`1e-6`/`1e-8`) are rejected, not transcribed. **Already adjudicated** by the Phase 25 EVID-10 record `scs-thresholds.md` (verdict `accept-resolution`).
2. **VAL-02 / SASD** (Stiffness-Aware Sampling Density; Q-C2) - formula, data-side computation contract, low-resolution floor-effect caveat; training-side collocation weighting (M16) deferred to doc-03. **No verdict/packet yet** - Phase 28 authors them.
3. **VAL-03 / IPR** (Interpolation Physics Residual, dual-epsilon; Q-C3) - formula, dual-epsilon consistency with the v1.4 PHYS-03 outcome; ALM noise-floor role deferred to doc-03. **No verdict/packet yet** - Phase 28 authors them.
4. **VAL-04 / PSC** (Phase Space Coverage Entropy; Q-C4) - formula, data-side computation contract; replay-governance use deferred to doc-03. **No verdict/packet yet** - Phase 28 authors them.

**In-scope ledger rows:** SCS, SASD, IPR, PSC (all `PENDING` in `24-ISSUE-LEDGER.md`; SCS carries an assigned `accept-resolution` verdict). Previously verified Phase 26/27 rows are rechecked only where a Phase 28 edit touches shared spec sections - notably the Phase 27 PIPE-09 `compute_globals` global-scale contract that feeds the SCS definition.

**Not this phase:** FUT-01 code / live `pinn/` edits; doc-03 training-loop usage of any metric (SASD-weighted collocation/M16, IPR-as-ALM-noise-floor, PSC-governed replay; OI-10); edits to read-only `data_quality_assessment.md` (SCOPE-09); edits to frozen `sampling_method.md` (SCOPE-08); re-opening the locked Phase 27 PIPE-09 scale convention; milestone-wide acceptance-suite execution, ledger close, SI-ledger reconcile, and FUT-01 handoff (Phase 29).

**Governance:** v1.5 STOP protocol applies in full. The SCS verdict is locked and transcribed, not re-opened. For SASD/IPR/PSC the resolution doc is a **candidate verdict source, not authority**; where it flagged a fork for sign-off (Q-C2/C3/C4) and the dataset + first-principles evidence does not settle it, the executor STOPs the dependent work and records the gap in `28-GAPS.md` plus `.planning/milestones/v1.5-GAPS.md`. Source-silent semantic / process-schema / cross-phase decisions are never invented.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**4 requirements are locked.** See `28-SPEC.md` for full requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `28-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Adjudicate and land framework-spec contracts for VAL-01, VAL-02, VAL-03, and VAL-04 (SCS, SASD, IPR, PSC) - data-side definitions only.
- Consume the read-only DQA metric texts, issue-02 (non-authoritative), the consolidated resolution doc (candidate), the on-disk dataset / `simulation_data/Scripts/`, and Phase 25 evidence packets / EVID-10 records as grounding before any spec edit.
- Resolve the issue-02 ratio-based SCS thresholds through the EVID-10 record (already `accept-resolution`), not by transcription of the ratios.
- Record doc-03 forward-references for every deferred training-loop usage.
- Update the Phase 24 issue-ledger VAL rows per the Phase 25 lifecycle; define/execute per-finding acceptance checks (AC-VAL-01..04) before marking rows `VERIFIED`.
- Re-verify previously verified Phase 26/27 findings only where a Phase 28 edit could regress a shared spec section.

**Out of scope (from SPEC.md):**
- Training-loop usage of any metric (M16 collocation, ALM noise-floor, replay governance) - doc-03.
- FUT-01 DataLoader implementation or live `pinn/` code changes.
- Edits to `data_quality_assessment.md` (read-only) or `sampling_method.md` (frozen).
- Re-opening the Phase 27 PIPE-09 global-scale convention.
- Milestone-wide acceptance execution, ledger close, SI-ledger reconcile, and handoff - Phase 29.

</spec_lock>

<decisions>
## Implementation Decisions

### Spec-edit strategy and boundaries
- **D-01 - Locked inputs before edits:** Planning starts from `28-SPEC.md`, the seeded `24-ISSUE-LEDGER.md` VAL rows (SCS/SASD/IPR/PSC), the Phase 25 evidence machinery + `evidence/scs-thresholds.md`, `24-VERIFIED-FACTS.md`, and the read-only DQA metric definitions. The resolution doc remains a candidate verdict source, not authority; issue-02 is non-authoritative.
- **D-02 - Placement:** `ctl_instruction.md` is the primary home for all four metric contracts. `pinn_architecture.md` is touched only where architecture-facing metric wording must be visible to FUT-01 (the ledger Spec-Section column lists `ctl_instruction.md; pinn_architecture.md` for SASD/IPR/PSC). For SCS, the canonical contract is transcribed into `ctl_instruction.md`; the read-only DQA remains the cited written home of the locked gate (SCOPE-09 - cited, never edited). No other spec target is in scope.
- **D-03 - SCS is transcription, not re-adjudication:** VAL-01/SCS is already adjudicated - Phase 25 authored `evidence/scs-thresholds.md` with verdict `accept-resolution` (adopt the locked post-v1.3 log-drift gate `\epsilon_H > 10^{-5}` / `SCS > -5`; reject the issue-02 ratio thresholds `1e-6`/`1e-8`). Phase 28 transcribes and verifies that verdict into `ctl_instruction.md`, rejecting the ratio thresholds by name; it does NOT reopen the gate. (Mirrors Phase 27 D-03 for M12/D.)
- **D-04 - SASD/IPR/PSC require evidence packets + fork adjudication BEFORE edits (STOP-protocol critical):** VAL-02/03/04 have no verdict and no evidence packet yet (ledger Verdict/Packet = `—`). Phase 28 MUST author an EVID-06 evidence packet for each (copy `_TEMPLATE.md` per the evidence README ID->Filename map) before any spec edit, adjudicating each against the dataset, the read-only DQA definition, first-principles physics, and the resolution doc as a candidate. The resolution doc itself FLAGS three forks - Q-C2 (SASD both-endpoints vs left-endpoint, "flagged for sign-off"), Q-C3 (IPR raw vs scaled units, ~464x gate impact, "the consequential one"), Q-C4 (PSC dedup+weighting composition "present in neither input"). Where the evidence settles a fork, lock it in the packet; where the resolution doc requested sign-off or the evidence cannot settle it, **STOP and surface to the user** - do NOT adopt the resolution doc's choice on its authority alone. This is a MUST-surface protection; it is NOT auto-picked despite `--auto`.
- **D-05 - Deferral wording:** doc-03 training-loop consumers - SASD-weighted collocation (M16), IPR-as-ALM-noise-floor, PSC-governed curriculum replay - get factual forward-references only. If a proposed edit needs a policy for those consumers, stop and surface the gap rather than choosing. (Mirrors Phase 27 D-04.)

### Evidence and ledger workflow
- **D-06 - Use the existing evidence system:** Reuse Phase 25's evidence README protocol, `_TEMPLATE.md`, verdict enum, EVID-10 trigger table, and ID->Filename map. `evidence/scs-thresholds.md` is the authoritative process input for SCS; SASD/IPR/PSC packets are authored under `25-.../evidence/` per the map. EVID-06's four sources (current specs, dataset annex `24-VERIFIED-FACTS.md`, first-principles physics, and the candidate sources) apply to every packet.
- **D-07 - No new AC-IDs:** Use the seeded acceptance checks only - AC-VAL-01, AC-VAL-02, AC-VAL-03, AC-VAL-04 (reserved by Phase 25 D-13; names already in the ledger). Phase 28 cites the AC-ID each fix targets; runnable pass criteria/commands/fixtures are built and executed by Phase 29 (VER-07/09). A missing or ambiguous packet mapping is a process-schema STOP gap, not a license to mint a new schema. (Mirrors Phase 27 D-06.)
- **D-08 - EVID-10 only where sources disagree:** The ledger marks SCS as EVID-10-required (sources disagree - record already authored by Phase 25); SASD/IPR/PSC as sources-agree (NO), so no EVID-10 conflict packet is mandated - a standard EVID-06 packet suffices. If Phase 28 discovers any new resolution-doc-vs-issue-doc (or vs locked-convention / vs dataset) conflict, that triggers EVID-10 and its conflict-adjudication sections (evidence README).
- **D-09 - Ledger lifecycle + same-commit wiring:** Each VAL row moves `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` (or explicit `DEFERRED`). Ledger status, evidence links, spec edits, and acceptance-check results travel in the same logical plan commit. SCS begins `PENDING` with its verdict already assigned (adjudicated-but-unfixed).

### Acceptance checks and regression surface
- **D-10 - AC-VAL default shapes (structural):** Per `28-SPEC.md` Acceptance Criteria - AC-VAL-01 (one SCS definition + locked gate, ratio thresholds not canonical, EVID-10 backing); AC-VAL-02 (SASD formula + data-side computation + floor-effect caveat + doc-03 forward-ref); AC-VAL-03 (IPR formula + dual-epsilon consistency with PHYS-03 + doc-03 forward-ref); AC-VAL-04 (PSC formula + data-side computation + doc-03 forward-ref). Pass criteria are structural (does the contract contain the required elements?); they do NOT encode the contested fork values, which are settled inside the evidence packets.
- **D-11 - Regression discipline:** Re-verify the Phase 27 PIPE-09 `compute_globals` global-scale contract that feeds the SCS definition, plus any shared `ctl_instruction.md` / `pinn_architecture.md` sections a Phase 28 edit touches. Previously verified Phase 26/27 rows are rechecked only when an edit touches their text.

### Planning order and batching
- **D-12 - Recommended order:** SCS first (lowest-risk transcription of a locked verdict; depends only on the already-locked PIPE-09 scale), then SASD -> IPR -> PSC (each gated on authoring its evidence packet first). The planner may batch adjacent metric contracts only if acceptance checks and ledger transitions stay reviewable and no un-surfaced fork blocks the batch. (Mirrors Phase 27 D-13.)

### Autonomous execution and STOP recovery (D-13..D-16 carried forward from Phase 27 D-15..D-18; D-17..D-18 added in Phase 28 from the plan audit)
- **D-13 - Autonomous-STOP operationalization:** Under `autonomous: true`, a STOP gap (e.g., an unresolvable Q-C2/C3/C4 fork) neither silently resolves nor proceeds. The affected plan PARKS at the gap, records a full STOP entry in `28-GAPS.md` + `.planning/milestones/v1.5-GAPS.md`, and the phase-exit gate blocks while any in-scope gap is OPEN. Independent plans/waves may proceed. Grounding: CLAUDE.md STOP protocol step 5; Phase 27 D-15.
  - **Park-bookkeeping (the first park MUST do all of):** (1) create `28-GAPS.md` from the STOP-protocol schema if it does not yet exist (no task assumes it pre-exists — it is created on-demand at first park); (2) add a `## Phase 28` section + the gap row to `.planning/milestones/v1.5-GAPS.md`; (3) update that file's frontmatter counters in the SAME edit — increment `total_gaps` and `open_gaps` and set `last_updated` (and, if the user later defers the gap, move the count to `deferred_gaps`). A gap entry without the counter update is an incomplete STOP record. Grounding: Phase 28 plan audit O2.
  - **`DEFERRED` row-status vs Phase-28 close are two different gates (do NOT conflate):** the evidence README Phase-Exit Rule permits a row to sit at `DEFERRED` instead of `IN_PROGRESS`/`FIX_APPLIED` at exit — that is the *row-status* gate. It does NOT by itself permit Phase-28 closure. A row that is `DEFERRED` *with its STOP gap still `OPEN`* means the fork is still awaiting user instruction; Phase-28 close additionally requires every in-scope VAL gap to be `RESOLVED-WITH-INSTRUCTION` or explicitly user-`DEFERRED`. An autonomous executor MUST NOT read "the row is `DEFERRED`, and `DEFERRED` is an allowed exit state" as license to close the phase over an `OPEN` gap. Grounding: CLAUDE.md STOP protocol step 5; evidence README Phase-Exit Rule; Phase 28 plan audit C1.
- **D-14 - STOP-recovery contract:** If a STOP fires mid-wave after a ledger row advanced past `PENDING`, do NOT revert the row (revert is destructive, needs user approval). Leave it at its current status, record the halt in `28-GAPS.md`, and let the gap's resolution note carry the resume path. Grounding: CLAUDE.md destructive-op policy; Phase 27 D-16.
- **D-15 - Owned-paths self-audit:** `scripts/agent-commit` enforces only a non-empty `GIT_AGENT_OWNED_PATHS`; the hook does not cross-check staged vs owned paths. Each executor MUST self-audit `git diff --cached --name-only` before committing and stage only its plan's explicit owned paths. Grounding: Phase 27 D-17.
- **D-16 - Re-locate edit sites by content, not line number:** `ctl_instruction.md` line anchors drift as edits land; locate every edit target by section heading + content marker (`grep -n`), not by a cited line number. Grounding: Phase 27 D-18.
- **D-17 - Cross-plan subsection substrate (`Data-side quality-metric contracts`) — normative heading + idempotent create-if-absent:** SASD/IPR/PSC (28-02/03/04) all live in ONE shared `ctl_instruction.md` subsection. To make cross-plan re-location and the AC self-checks deterministic, the subsection heading is **NORMATIVE** — the fixed string `Data-side quality-metric contracts` (an optional trailing `(SASD, IPR, PSC)` enumerator is allowed, but the core string MUST be present and unchanged). This narrows the "Claude's Discretion" heading freedom for THIS one subsection only, because 28-02/03/04 and their AC checks re-locate it by that literal string (`grep -n 'Data-side quality-metric contracts'`). Subsection creation is **idempotent and order-independent across a park:** each of 28-02/03/04 must *locate-or-create* the subsection (if absent, CREATE it immediately after the Step-1A gate using the normative heading and the same placement rule) and then **append** its own clause; a parked predecessor therefore does NOT block an independent successor whose own fork settles, and a predecessor resuming after un-park finds the subsection already present and appends into it. The plan that first creates the subsection also adds the cross-reference back to the Step-1A SCS conservation gate (binding the four validation metrics into one family). Grounding: closes the wave-park substrate hole (Phase 28 plan audit L1/L3); append-only regression discipline (D-11); STOP park-independence (D-13).
- **D-18 - Pre-execution environment (operational; confirm before an unattended run):** (a) The four plans' `<execution_context>` `@`-includes point at `$HOME/.claude-max-max/gsd-core/...`. This path is inherited verbatim from Phase 27 (which executed successfully under the `.claude-max-max` CCP profile); it is a *profile selection*, not a typo, and resolves under the executing profile even though it is absent under other local profiles (e.g. `.claude-alt`, the profile that authored this audit). Confirm the executing profile mounts `gsd-core` before an unattended autonomous run; do NOT blind-edit the include path — changing it risks breaking execution under the intended profile. (b) A MUST-surface park halts awaiting user instruction; under an unattended wave run there may be no live channel, so a parked plan can idle on a `DEFERRED`+`OPEN` row — when any Q-C2/C3/C4 fork is plausible, the run should be watched so the surfaced gap is seen. Grounding: Phase 28 plan audit O1/O4; CLAUDE.md STOP protocol step 5.

### Claude's Discretion
- Exact heading names and placement within `ctl_instruction.md` / `pinn_architecture.md`, so long as canonical references and before/after notes keep placement auditable — EXCEPT the shared `Data-side quality-metric contracts` subsection heading, which is normative (fixed string) per D-17 because 28-02/03/04 and their AC checks re-locate it by that literal string.
- Whether acceptance checks are inline commands or small disposable scripts under the Phase 28 directory (built/executed in Phase 29 regardless).
- Exact plan count and wave grouping, constrained by D-04 / D-07 / D-09 / D-12.
- The SASD/IPR/PSC evidence-packet filenames, per the evidence README ID->Filename map.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements and protocol
- `.planning/phases/28-validation-metrics-contracts/28-SPEC.md` - locked requirements, boundaries, constraints, and acceptance criteria for VAL-01/02/03/04. Locked requirements - MUST read before planning.
- `.planning/REQUIREMENTS.md` - VAL-01..04; SCOPE-06/07 dataset and scripts grounding; SCOPE-08 frozen `sampling_method.md`; SCOPE-09 read-only `data_quality_assessment.md`; SCOPE-10 live `pinn/` ban; SCOPE-11 doc-03 boundary.
- `.planning/ROADMAP.md` - Phase 28 goal/success criteria and v1.5 phase ordering (depends on Phase 27 PIPE-09).
- `AGENTS.md` / `CLAUDE.md` - v1.5 STOP protocol, grounding hierarchy, Git and commit governance.

### Ledger and verified dataset facts
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` - seeded VAL rows (SCS/SASD/IPR/PSC) with Verdict, Sources-Disagree, Evidence-Packet, Acceptance-Check (AC-VAL-01..04), Spec-Section, and per-finding subsections; status lifecycle.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` - dataset-evidence annex (EVID-06's fourth source) for floor-effect / dual-epsilon / coverage grounding.

### Phase 25 evidence machinery and packets
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` - evidence-packet protocol, verdict enum, EVID-10 trigger table, ID->Filename map, lifecycle, and the no-new-AC-ID discipline (D-13; AC-VAL-01..04 reserved).
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md` - evidence-packet schema for the SASD/IPR/PSC packets Phase 28 authors.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md` - SCS EVID-10 record: verdict `accept-resolution` (locked log-drift gate; reject ratio thresholds). Authoritative input for VAL-01.
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md` - Phase 25 decisions for evidence, ledger, EVID-10, and status lifecycle.

### Metric definitions and candidate verdict sources
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` - read-only; the sole written home of the locked SCS gate and the SASD/IPR/PSC definitions. Cite, never edit (SCOPE-09).
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` - candidate verdict source; Q-C1 (SCS), Q-C2 (SASD), Q-C3 (IPR), Q-C4 (PSC), with the three flagged forks. Not authoritative.
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` - non-authoritative issue doc; source-position and rejected-claim citations (ratio thresholds).
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` / `24.5-READINESS-REPORT.md` - resolution-doc line map and readiness caveats / open-item dispositions (carry OI caveats forward).

### Framework spec targets and commit machinery
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - primary Phase 28 edit target.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - secondary edit target for architecture-facing metric wording.
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-CONTEXT.md` - immediate predecessor; PIPE-09 global-scale contract feeding SCS, and the D-15..D-18 autonomous/STOP machinery carried forward here.
- `scripts/agent-commit` + `docs/git-guidelines.md` - mandatory commit wrapper and commit/owned-path/hook policy.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 25 evidence-packet system under `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/` (README, `_TEMPLATE.md`, `scs-thresholds.md`) - reuse, do not redesign.
- `24-ISSUE-LEDGER.md` seeded VAL rows + `24-VERIFIED-FACTS.md` dataset annex - status index and evidence source.
- `scripts/agent-commit` and `.githooks` - enforced commit path.

### Established Patterns
- v1.5 spec-edit phases keep framework changes in `ctl_instruction.md` / `pinn_architecture.md`, with ledger and evidence updates committed atomically (same-commit wiring).
- Adjudicated-but-unfixed rows (verdict assigned, fix owned downstream) start the owning phase at `PENDING` with the verdict already filled (SCS).
- Acceptance checks use seeded AC IDs; phases cite pass intent but do not mint new identifiers or build runnable checks (that is Phase 29).
- Live `pinn/` code appears only in FUT-01 forward-handoff language, never as grounding.

### Integration Points
- Phase 28 metric contracts feed Phase 29 acceptance-suite execution (VER-07/09) and FUT-01 DataLoader implementation.
- SCS consumes the Phase 27 PIPE-09 raw-mass global-scale (`compute_globals`) contract - regression-check it.
- Each metric's training-loop usage (SASD collocation/M16, IPR ALM-noise-floor, PSC replay) feeds doc-03; Phase 28 records only the forward interface.

</code_context>

<specifics>
## Specific Ideas

- Authoritative metric titles (from the seeded ledger): SCS = Symplectic Conservation Score; SASD = Stiffness-Aware Sampling Density; IPR = Interpolation Physics Residual; PSC = Phase Space Coverage Entropy.
- SCS verdict is already `accept-resolution` (Phase 25): locked log-drift gate `\epsilon_H > 10^{-5}` / `SCS > -5`; issue-02 ratio thresholds (`1e-6`/`1e-8`) rejected. VAL-01 transcribes this into `ctl_instruction.md`; the DQA stays the read-only home of the gate.
- The resolution doc's three flagged forks are the decision risk for VAL-02/03/04: Q-C2 SASD endpoints (sign-off), Q-C3 IPR units (raw vs scaled, ~464x gate impact - the consequential one), Q-C4 PSC composition (synthesis present in neither input, with a verification run specified). None are decided here; each is adjudicated with evidence and surfaced for sign-off if unsettled.
- Ledger marks SASD/IPR/PSC "Sources Disagree = NO" - a standard EVID-06 packet (not an EVID-10 conflict packet) is the default, unless Phase 28 discovers a new conflict.
- IPR's dual-epsilon must stay consistent with the v1.4 PHYS-03 softening outcome; SCS consumes the v1.4 raw-mass PHYS-01 scale via Phase 27 PIPE-09.

</specifics>

<deferred>
## Deferred Ideas

- Training-loop usage of all four metrics - doc-03: SASD-weighted collocation (M16), IPR-as-ALM-noise-floor, PSC-governed curriculum replay (OI-10).
- Full acceptance-suite build/execution, SI-ledger reconciliation, and FUT-01 handoff - Phase 29 (VER-07/08/09/11/12).
- DataLoader implementation in live `pinn/` code - FUT-01.
- Standard-gold missing-counterpart rerun completion remains separate operational work from Phase 28 spec discussion.

### Reviewed Todos (not folded)
None - the single pending todo had no relevance match to Phase 28 (todo.match-phase returned 0 matches).

</deferred>

---

*Phase: 28-validation-metrics-contracts*
*Context gathered: 2026-06-14*
