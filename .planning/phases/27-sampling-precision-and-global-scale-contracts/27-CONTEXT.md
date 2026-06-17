# Phase 27: Sampling, Precision, and Global-Scale Contracts - Context

**Gathered:** 2026-06-13
**Status:** Ready for planning
**Mode:** `--all --auto` - all gray areas auto-selected; recommended defaults chosen by Codex per explicit user instruction. Auto-advance stops before planning starts. Decisions below are implementation/process defaults only; the locked physics and data contracts are in `27-SPEC.md`, Phase 25 evidence packets, and Phase 24 verified facts.

<domain>
## Phase Boundary

`ctl_instruction.md` / `pinn_architecture.md` state four remaining v1.5 data-side contracts before Phase 28 and FUT-01 depend on them:

1. **PIPE-04 / M12 + G5** - points-per-trajectory sampling uses `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, sampled without replacement, default cap 32, with `dt_out`/`n_snapshots` exposed as data-side metadata and M16 collocation-density policy deferred.
2. **PIPE-07 / DATA-05 precision** - float64 is sufficient for data-side metrics and invariants; `decimal.Decimal` is a future failed-mass-gate classifier only, not the normal parsing or metric path.
3. **PIPE-08 / stage-query interface** - the DataLoader exposes per-trajectory `dt_out` and `n_snapshots`, plus `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)`.
4. **PIPE-09 / `compute_globals`** - global scales preserve the v1.4 raw-mass PHYS-01 convention and reject the issue-doc `D = 6.694` / `M_tot_ref` convention as canonical.

**In-scope ledger rows:** M12, G5, footer, mass-drift, and D=6.694. G5 closes with M12 as a synthesis row. Previously verified Phase 26 rows are rechecked only when Phase 27 edits touch shared spec sections.

**Not this phase:** FUT-01 code, live `pinn/` implementation edits, doc-03 M16 collocation/training-loop policy, Phase 28 validation metrics, edits to frozen `sampling_method.md`, edits to read-only `data_quality_assessment.md`, or new processed-training-data format decisions.

**Governance:** v1.5 STOP protocol applies in full. If the planner/executor finds a source-silent semantic, process-schema, or cross-phase decision, stop the dependent work and record it in `27-GAPS.md` plus `.planning/milestones/v1.5-GAPS.md`. Do not fill white space in the specs.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**4 requirements are locked.** See `27-SPEC.md` for full requirements, boundaries, and acceptance criteria.

Downstream agents MUST read `27-SPEC.md` before planning or implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Adjudicate and land framework-spec contracts for PIPE-04, PIPE-07, PIPE-08, and PIPE-09.
- Consume Phase 24 verified facts and Phase 25 evidence packets as grounding sources before any spec edit.
- Update the Phase 24 issue ledger rows for M12, G5, mass-drift/footer precision, and D=6.694 according to the Phase 25 lifecycle rules.
- Define and execute per-finding acceptance checks AC-PIPE-04, AC-PIPE-07, AC-PIPE-08, and AC-PIPE-09 before marking rows `VERIFIED`.
- Re-verify previously verified Phase 26 findings only where a Phase 27 edit could regress their contracts.

**Out of scope (from SPEC.md):**
- FUT-01 DataLoader implementation or live `pinn/` code changes.
- doc-03 collocation-density, training-loop sampling, or M16 policy.
- Phase 28 validation metric definitions for SCS, SASD, IPR, and PSC.
- Changes to `sampling_method.md` unless explicitly instructed by the user.
- Edits to `data_quality_assessment.md`.
- New processed-training-data format decisions; HDF5 was user-locked in Phase 26.

</spec_lock>

<decisions>
## Implementation Decisions

### Spec-edit strategy and boundaries
- **D-01 - Locked inputs before edits:** Planning starts from `27-SPEC.md`, `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md`, Phase 24 verified facts/remediation artifacts, and Phase 25 evidence packets. The resolution doc remains a candidate verdict source, not authority.
- **D-02 - Placement:** `ctl_instruction.md` is the primary home for all four contracts. `pinn_architecture.md` is touched only where the data-side metadata/query interface or architecture-facing precision/global-scale wording needs to be visible to FUT-01. No other spec target is in scope.
- **D-03 - No re-adjudication of locked rulings:** M12's third-position sampling rule and PIPE-09's raw-mass `D` convention are already locked by Phase 25. Phase 27 transcribes and verifies them; it does not reopen the 0.5 factor, `D = 6.694`, `M_tot_ref`, or mass-fraction conventions.
- **D-04 - Deferral wording:** M16, training-loop sampling/collocation use, Phase 28 validation metrics, and FUT-01 code behavior get factual forward references only. If a proposed edit needs a policy for those downstream consumers, stop and surface the gap rather than choosing.

### Evidence and ledger workflow
- **D-05 - Use the existing evidence system:** The planner uses Phase 25's evidence README and template rules. Existing packets `m11-m12-severity.md` and `compute-globals-D.md` are authoritative process inputs for M12/G5 and D=6.694 respectively; DATA-05 precision consumes the Phase 24 rerun remediation/validation artifacts and ledger notes.
- **D-06 - No new AC IDs:** Use the seeded acceptance checks only: AC-PIPE-04, AC-PIPE-07, AC-PIPE-08, and AC-PIPE-09. If a required process artifact or packet mapping is missing or ambiguous, that is a process-schema STOP gap, not a license to invent a new schema.
- **D-07 - Ledger lifecycle:** Each touched row moves through the Phase 25 lifecycle (`PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, or explicit `DEFERRED`). Ledger status, evidence links, spec edits, and acceptance-check results travel in the same logical plan commit.
- **D-08 - G5 closes with M12:** G5 is a synthesis/data-side facet over M12 and M16-deferred metadata. It gets no separate evidence packet unless the existing Phase 25 protocol explicitly requires one; otherwise it closes with M12 and records the doc-03 M16 deferral.

### Acceptance checks and regression surface
- **D-09 - AC-PIPE-04 default shape:** Verify the specs state `min(n_pts_cap, n_snapshots)` without replacement, default cap 32, no `0.5 * n_snapshots` factor, DATA-06 grounding, and M16 deferral. Recheck any shared Phase 26 admission-gate text if edited.
- **D-10 - AC-PIPE-07 default shape:** Verify float64 sufficiency, Decimal-only-as-classifier wording, current IC masses canonical, old 70 base-hier artifacts rejected as stale rather than precision failures, and the future mass-gate failure condition.
- **D-11 - AC-PIPE-08 default shape:** Verify `dt_out` and `n_snapshots` metadata, footer/default provenance preservation from PIPE-06, and the two stage-query method signatures. Keep this data-side; no training-loop policy.
- **D-12 - AC-PIPE-09 default shape:** Verify raw-mass PHYS-01 `D = (G*T^2)^(1/3)` is canonical, `D = 6.694` / `M_tot_ref` are rejected by name as canonical pipeline instructions, `E_scale` floor handling follows the locked evidence packet, and Phase 28 SCS usage is left alone.

### Planning order and batching
- **D-13 - Recommended order:** Plan M12/G5 first, then precision, then stage-query metadata, then global-scale cleanup. This keeps snapshot/metadata contracts available before interface wording and leaves the more isolated `compute_globals` cleanup last. The planner may batch adjacent contracts only if the acceptance checks and ledger transitions remain reviewable.
- **D-14 - Regression discipline:** Any edit to sections touched by Phase 26 triggers targeted rechecks for previously verified rows sharing that text, especially B-06 admission, D7 footer provenance, and D-03 HDF5 wording if nearby text is moved.

### Autonomous execution and recovery (audit remediation 2026-06-13)

These three decisions operationalize the Phase 27 plan-audit findings F-06, F-09,
and F-21 (`docs/work/reviews/milestone_v1.5/27-sampling-precision-and-global-scale-contracts/2026-06-13-phase-27-plan-audit-report.md`).
They are **operational coordination** defaults derived from existing governance,
not new semantic or physics decisions; each cites its grounding.

- **D-15 - Autonomous-STOP operationalization (F-06):** Under `autonomous: true`, a
  STOP-protocol gap neither silently resolves nor proceeds. The affected plan **parks**
  at the gap, records a full STOP-protocol entry in `27-GAPS.md`, and the phase-exit gate
  blocks while any in-scope gap is OPEN. **Independent** plans/waves may proceed; the
  halted plan resumes only when the user resolves the gap. Grounding: `CLAUDE.md` STOP
  protocol step 5 ("halted work stays halted until the user provides instruction") and the
  explicit "There is no exception" clause govern. `autonomous: true` removes mid-run human
  checkpoints; it does not license inventing past a source-silent decision.
- **D-16 - STOP-recovery contract (F-09):** If a STOP/gap fires mid-wave after a ledger row
  has advanced past `PENDING` (the EVID-06 packet-before-edit gate), **do NOT revert** the
  row status — revert is a destructive operation requiring user approval. Leave the row at
  its current status (`IN_PROGRESS` or `FIX_APPLIED`), record the halt in `27-GAPS.md`, and
  let the gap's resolution note carry the resume path. The phase-exit gate will keep the
  phase open until the gap is resolved and the row reaches `VERIFIED`. Grounding:
  `CLAUDE.md` destructive-operation policy.
- **D-17 - Owned-paths is advisory, not hook-enforced (F-21):** `scripts/agent-commit`
  enforces only that `GIT_AGENT_OWNED_PATHS` is non-empty; `.githooks` →
  `validate_staged_paths.py` validates blocked patterns and blob size but does **not**
  cross-check staged paths against declared owned paths. Owned-paths discipline is therefore
  advisory: each executor MUST self-audit `git diff --cached --name-only` before committing
  and stage only its plan's explicit owned paths. Grounding: verified against
  `scripts/agent-commit` and `.githooks/validate_staged_paths.py` during the audit.
- **D-18 - Line anchors drift across waves; re-locate by content (F-19):** The fixed line
  numbers cited in plan `read_first` blocks (e.g. `1410-1430`, `800-825`, `744-774`,
  `~773`) are the line numbers AT PLAN-AUTHORING TIME. Wave 1 (Plan 27-01) inserts ~12-40 new
  lines into `ctl_instruction.md` (Mini-Batch transcription), so every later wave's ctl anchors
  shift by the insertion delta (already observed: the 27-04 `E_scale` "~line 773" anchor is
  actually `:771`). Executors MUST re-locate every edit target by **section heading and content
  marker** (e.g. `grep -n '## Mini-Batch Construction'`, `grep -n 'Per-trajectory data-loss
  point count'`, `grep -n 'Global-scale D'`), not by the cited line number. Each plan's
  pre-transcription content-marker verification (audit F-04) is the enforced form of this rule.

### Codex's Discretion
- Exact heading names and placement within `ctl_instruction.md` / `pinn_architecture.md`, so long as canonical references and before/after notes make the placement auditable.
- Whether acceptance checks are implemented as inline commands or small disposable scripts under the Phase 27 directory.
- Exact plan count and wave grouping, constrained by D-06/D-07/D-13.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements and protocol
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-SPEC.md` - locked requirements, boundaries, constraints, and acceptance criteria for PIPE-04/07/08/09.
- `.planning/REQUIREMENTS.md` - PIPE-04, PIPE-07, PIPE-08, PIPE-09; SCOPE-06/07 dataset and scripts grounding; SCOPE-08 frozen `sampling_method.md`; SCOPE-09 read-only `data_quality_assessment.md`; SCOPE-10 live `pinn/` ban.
- `.planning/ROADMAP.md` - Phase 27 milestone scope and v1.5 phase ordering.
- `AGENTS.md` / `CLAUDE.md` - v1.5 STOP protocol, grounding hierarchy, Git and commit governance.

### Ledger and verified dataset facts
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` - stable ledger rows for M12, G5, footer, mass-drift, and D=6.694; status lifecycle; row-specific notes.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` - DATA-05 and DATA-06 facts, including snapshot/`dt_out` distributions and mass-drift verdict inputs.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md` - user-resolved DATA-05 boundary and remediation record for the 70 stale base-hier outputs.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-VALIDATION.md` - validation evidence for the DATA-05 rerun remediation.

### Phase 25 evidence machinery and packets
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` - evidence-packet protocol, verdict enum, EVID-10 trigger rules, ID-to-filename map, lifecycle rules, and no-new-AC-ID discipline.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/_TEMPLATE.md` - evidence-packet schema if a grounded packet is required by the protocol.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md` - M12 verdict: `accept-third-position`; reject BLOCKING infeasibility and the 0.5 factor; locked data-side sampling rule.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` - PIPE-09 verdict: accept raw-mass PHYS-01 `D`, reject `D = 6.694` / `M_tot_ref`, capture `E_scale` floor and Plummer/additive-epsilon rules.
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md` - Phase 25 decisions for evidence, ledger, EVID-10, and status lifecycle.

### Candidate verdict sources and issue source
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` - candidate verdict source for issue-02; not authoritative.
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` - non-authoritative issue doc; useful for source-position and rejected-claim citations.
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` - line map and citation structure for the consolidated resolution doc.
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-READINESS-REPORT.md` - readiness caveats and open-item dispositions.

### Framework spec targets
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - primary Phase 27 edit target.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - secondary edit target for architecture-facing data-side contract wording.
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` - frozen by default; cite only as historical data-generation record unless user explicitly reopens it.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` - read-only; cite only, never edit.

### Commit machinery
- `scripts/agent-commit` - mandatory commit wrapper for agent commits.
- `docs/git-guidelines.md` - commit message, owned-path, hook, and verification policy.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 25 evidence packet system under `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/` - reuse rather than redesign.
- `24-ISSUE-LEDGER.md` and `24-VERIFIED-FACTS.md` - status index and dataset evidence for Phase 27 rows.
- DATA-05 rerun remediation/validation artifacts - precision and mass-gate evidence source.
- `scripts/agent-commit` and `.githooks` - enforced commit path and hook setup.

### Established Patterns
- v1.5 spec-edit phases keep framework changes in `ctl_instruction.md` / `pinn_architecture.md`, with ledger and evidence updates committed atomically.
- Synthesis rows close with parent findings unless the Phase 25 protocol explicitly says otherwise.
- Acceptance checks are named by seeded AC IDs; phases define pass criteria but do not mint new identifiers.
- Live `pinn/` code can appear only in FUT-01 forward handoff language, never as grounding.

### Integration Points
- Phase 27 spec edits feed Phase 28 validation metrics and Phase 29 acceptance-suite execution.
- `dt_out` / `n_snapshots` metadata and stage-query signatures feed FUT-01 DataLoader implementation and doc-03 M16 policy, but Phase 27 does not define the consuming training policy.
- PIPE-04 sampling text overlaps Phase 26 B-06 admission language; PIPE-07 precision text overlaps Phase 26 D7 footer provenance; edits there need targeted regression checks.

</code_context>

<specifics>
## Specific Ideas

- DATA-06 corrected snapshot medians are 61 standard-base, 127 hierarchical-base, and 1003 gold; the PIPE-04 sampling rule must cite those facts without turning medians into hard per-file guarantees.
- DATA-05 is resolved as stale base-hier artifacts requiring rerun from current ICs, not Decimal parsing. The 70-file remediation was validated before Phase 27 planning.
- The `compute_globals-D.md` packet explicitly frames `D = 6.694` as a convention migration, not a local formula correction.
- The stage-query method names are locked by SPEC: `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)`.

</specifics>

<deferred>
## Deferred Ideas

- M16 collocation-density and training-loop sampling policy - doc-03 milestone.
- SCS, SASD, IPR, and PSC validation-metric definitions - Phase 28.
- Full acceptance-suite build/execution, SI-ledger reconciliation, and final handoff - Phase 29.
- DataLoader implementation in live `pinn/` code - FUT-01.
- Standard-gold missing-counterpart rerun completion remains separate operational work from Phase 27 spec discussion.

</deferred>

---

*Phase: 27-Sampling, Precision, and Global-Scale Contracts*
*Context gathered: 2026-06-13*
