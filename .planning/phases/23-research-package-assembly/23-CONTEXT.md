# Phase 23: Research Package Assembly - Context

**Gathered:** 2026-06-10
**Status:** Ready for planning
**Mode:** `--auto --all --batch --analyze` — all gray areas auto-selected; recommended options chosen by Claude and logged in `23-DISCUSSION-LOG.md`. The user did not interactively ratify these; they are grounded in REQUIREMENTS.md / ROADMAP.md / PROJECT.md wherever possible and marked Claude's discretion otherwise.

<domain>
## Phase Boundary

Deliver the external-research handoff package for issue 02: (1) a complete annotated document list — every document needed to adjudicate the issue-02 findings, with role annotations and scattered fragments consolidated into a single context file (PKG-01); (2) framed research questions — each contested or unverified finding posed as an explicit, neutral question with the locked v1.4 conventions as hard constraints and the doc-03 boundary stated (PKG-02); (3) every dataset figure marked "claimed, unverified" unless a prior grounded source verified it (PKG-03); (4) a read-only characterization of `data_quality_assessment.md` reported to the user (PKG-04). On delivery, the external resolution-doc gate opens and the user's multi-AI research begins.

**Not this phase:** empirical verification of any dataset claim (Phase 24); any adjudication, verdicts, or framework-spec edits (Phases 25–28); any edit to `data_quality_assessment.md` (SCOPE-09) or `sampling_method.md` (SCOPE-08); any `pinn/` reference as grounding (SCOPE-10).

**Governance:** v1.5 runs under the full STOP protocol (AGENTS.md "CRITICAL GOVERNANCE", v1.5 applicability section). Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `23-GAPS.md` + `.planning/milestones/v1.5-GAPS.md`, never invented.

</domain>

<decisions>
## Implementation Decisions

### Package location & delivery form
- **D-01:** Package lives at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/` — co-located with where the resolution doc is expected to land, mirroring the v1.4 layout (`research_reports/01-*/` holds research inputs and outputs together).
- **D-02:** The package is **self-contained**: snapshot copies of every included document (the user's external AI agents have no repo access). A manifest/README in the package records, per file, its role annotation, canonical source path, and the source commit hash, so the snapshot is traceable and the research state is pinned.
- **D-03:** Framework specs (`ctl_instruction.md`, `pinn_architecture.md`, and — if included — `sampling_method.md`) are copied byte-for-byte intact. They are NEVER consolidated, excerpted, or summarized in the package (PKG-01 hard rule).

### Document list (candidate inventory + criteria; final list locked at execution)
- **D-04:** Inclusion criterion: a document enters the list iff at least one issue-02 finding needs it for adjudication (PKG-01: "every document needed to adjudicate the issue-02 findings"). Final list is locked during execution AFTER the PKG-04 DQA characterization (which informs inclusion) and AFTER the consolidation plan is surfaced to the user (see D-07).
- **D-05:** Candidate inventory:
  - `pinn_instruction/issues/02-data-pipeline-and-validation.md` — the adjudication subject. Required.
  - `framework-specs/ctl_instruction.md`, `framework-specs/pinn_architecture.md` — intact; the only spec-edit targets; carry the locked v1.4 conventions.
  - `framework-specs/sampling_method.md` — intact; annotated FROZEN (SCOPE-08): historical record of how the dataset was generated; not a revision target.
  - `framework-revisions/data_quality_assessment.md` — inclusion decided by the PKG-04 characterization outcome; if included, annotated "research report, not authoritative spec" (SCOPE-09).
  - Consolidated context file (one file) for scattered fragments: `simulation_data/Documentation/README.md` content relevant to the findings, `standard_quasi_random_ids_not_in_gold.md`, a summary of `problematic_ics_blacklist.json`, and relevant excerpts of `simulation_data/Scripts/` provenance code (e.g., `calculate_metrics.py`, prescreening thresholds, runner parameter blocks) — each fragment labeled with its source path.
- **D-06:** `pinn/` live code is EXCLUDED from the package. The package explicitly states, as a hard constraint to the external research, that issue-02's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden (directive 2026-05-19; SCOPE-10) and the framework specs are the source of truth. Issue-01 is NOT included (resolved by v1.4; its outcomes travel as the locked-constraints block + the intact specs). Issue-03 is NOT included (doc-03 boundary; the boundary statement covers it).
- **D-07:** The candidate list is ≥6 deliverable files, so the PKG-01 consolidation rule fires. **Hard execution checkpoint: the consolidation plan (what gets consolidated, what stays standalone) is surfaced to the user BEFORE assembly.** This is a requirement (PKG-01), not a courtesy. Plans must model this as a user gate.

### Research-question framing (PKG-02)
- **D-08:** One questions document, structured as per-finding explicit questions grouped by downstream contract cluster: (a) ingestion & selection (B-06, B-11, M11, M13, D7, D-03 format, G1–G5 as applicable), (b) sampling / precision / global-scale (M12, precision handling, footer/mass-drift protocol, `compute_globals` D=6.694), (c) validation metrics (SCS, SASD, IPR, PSC definitions and thresholds). Grouping mirrors Phases 26–28 so the resolution doc maps onto adjudication phases.
- **D-09:** Neutral framing rule: each question presents the issue-doc position, the current framework-spec position, and the relevant dataset facts (via CLM IDs, D-11) — and never presupposes the issue doc's "Recommended Resolutions". The package instructs the external research that BOTH the issue doc and its recommendations are non-authoritative and may contain errors, citing the known seed conflict (ratio-based SCS thresholds `> 1e-6` / `< 1e-8` vs the locked post-v1.3 gate `ε_H > 10⁻⁵` / `SCS > −5`).
- **D-10:** A shared hard-constraints preamble lists the locked v1.4 conventions verbatim from PKG-02: 14D input contract, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening outcome, post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), PHYS-01 D convention — plus the doc-03 scope boundary (M16 collocation-scaling, G6 causal-training, and training-loop usage of SCS/SASD/IPR/PSC are EXCLUDED from the research scope, each noted as deferred with a forward-reference).

### Claims register (PKG-03 + Phase 24 handoff)
- **D-11:** The package contains a dedicated claims table with stable IDs (`CLM-01`, `CLM-02`, …): every dataset figure stated anywhere in the package gets a row with value, source citation, and status `claimed-unverified` (issue-doc value) or `verified` (with the grounding citation). All inline figure mentions in package prose reference their CLM ID.
- **D-12:** The claims table IS the "delivered package's claim list" that Phase 24 consumes as its verification checklist (ROADMAP Phase 24 dependency), and the DATA-07 correction addendum is keyed by CLM IDs. The table must therefore enumerate at minimum the figures named in DATA-01..06: 1,250/4,000 standard and 143/5,000 hierarchical ID gaps; 65 blacklist IDs; 184 standard IDs without gold; 2,565 vs 2,749 folder counts; 219 minimal standard-gold footers; ~59/~125/~1000 snapshot counts; `final_timestep >= 9.5` prevalence; folder-default tolerance/dt values.
- **D-13:** Conservative verified-status rule: only `simulation_data/Documentation/` files and prior-phase probe evidence (committed v1.4 artifacts) count as "prior grounded source" for marking a figure verified. `.planning/codebase/*.md` maps (analysis dated 2026-04-27) do NOT count. When in doubt, mark `claimed-unverified` — PKG-03's floor is "no unverified figure is presented as fact", and over-marking as claimed is harmless (Phase 24 verifies everything anyway).

### DQA characterization (PKG-04)
- **D-14:** Deliverable is a standalone phase artifact `.planning/phases/23-research-package-assembly/23-DQA-CHARACTERIZATION.md` covering: provenance (git origin/history of the file), a section-by-section content map, its relation to the not-yet-performed dataset↔framework compatibility verification (what it covers, what remains unverified), and a package-inclusion recommendation. Zero edits to `data_quality_assessment.md`.
- **D-15:** Sequencing: the characterization completes BEFORE the document list is finalized (roadmap success criterion 1: it "directly informs which documents the list includes") — so DQA characterization is an early task, before package assembly.

### Gate-opening record & handoff
- **D-16:** Delivery = package committed + a delivery note to the user stating: how to use the package for external multi-AI research; that the resolution doc must land under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`; that v1.4's `ctl_pinn_resolution.md` is a format precedent (suggestion only — the resolution doc is the user's product, no required schema); and that Phase 24 runs in parallel immediately and will forward a DATA-07 correction addendum for any package-stated claim that verification contradicts.
- **D-17:** The gate-open state is recorded in STATE.md via gsd-tools state handlers only (no direct Write/Edit to STATE.md), per universal anti-pattern 15 and roadmap success criterion 5.

### Claude's Discretion
- Exact file names inside the package (manifest/README name, questions-doc name, claims-table placement as standalone file vs section of the manifest) — presentation-only; keep names self-describing and kebab/snake-consistent with the repo.
- Which `simulation_data/Scripts/` excerpts enter the consolidated context file — judged per-finding during execution, within the D-04 criterion, and shown to the user at the D-07 consolidation checkpoint.
- Whether `sampling_method.md` ships in the package — recommended YES (the findings concern the dataset it generated) but final call rides the D-07 user checkpoint alongside the DQA inclusion decision.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/REQUIREMENTS.md` — PKG-01..04 (this phase's four requirements, verbatim), source-treatment policy, SCOPE-06..11 boundaries.
- `.planning/ROADMAP.md` §"Phase 23: Research Package Assembly" — goal, the five success criteria, gate semantics; §"Source treatment & STOP protocol" — applies to every task.
- `AGENTS.md` / `CLAUDE.md` §"CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones" — STOP protocol with v1.5 substitutions (gap registers: `23-GAPS.md` phase-local, `.planning/milestones/v1.5-GAPS.md` milestone index — neither exists yet; create on first gap).

### Adjudication subject
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — the issue doc (364 lines; NON-authoritative). Findings: D-03 (§Decisions Requiring Human Approval), BLOCKING B-06/B-11, MAJOR M11/M12/M13/D7, severity-reclassification ledger, MINOR items, G1–G6 (§Pipeline Validation Gaps), validation-threshold clarifications, SCS/SASD/IPR/PSC (§Validation Metrics as Live Training Parameters), h5-vs-txt/json (§File Format), footer/mass-drift + precision + global-scale (§Brutus Output Handling), §Open Decisions, §Recommended Resolutions (must NOT be presented as settled), §Dataset Inventory, §DataLoader Requirements, §References.

### Package contents (candidate inventory — D-05)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — spec-edit target; intact copy.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — spec-edit target; intact copy.
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — FROZEN (SCOPE-08); intact copy if included.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — PKG-04 characterization subject (328 lines; read-only, SCOPE-09).
- `simulation_data/Documentation/README.md` — canonical dataset spec ("Canonical" per issue-02 References; do not duplicate content into other repo docs — consolidation-file fragments cite it).
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — grounded gold-gap record (184 IDs).
- `simulation_data/Documentation/problematic_ics_blacklist.json` — blacklist (65-ID count is a CLAIM until DATA-02).
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` — provenance grounding (SCOPE-07) for metrics-related excerpts.

### Precedents
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/` — v1.4 layout precedent: `ctl_pinn_resolution.md` (resolution-doc format precedent) + 4 individual model reports.
- `.planning/research/edl/EDL-19-01-epsilon-H.md` + `.planning/research/edl/README.md` — prior user-led external-research brief format (non-canonical support workflow; structural inspiration only).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- v1.4 research-reports directory structure (`research_reports/01-*/`) — the layout the package directory mirrors (D-01).
- EDL brief format (`EDL-19-01`) — prior art for packaging context for user-led external research: decision statement, candidate options, constraints, what-the-research-must-answer.
- `scripts/agent-commit` — mandatory commit path (project Git Commit Protocol); one atomic commit per plan.

### Established Patterns
- Phase artifacts named `NN-*.md` in `.planning/phases/NN-slug/` (DQA characterization → `23-DQA-CHARACTERIZATION.md`).
- STATE.md mutations only via gsd-tools handlers.
- Pre-phase tag `v1.5-pre-phase-23` cut from `milestone/v1.5` HEAD before Phase 23 commits (STATE.md pending todo; cut at `cf16484` during discuss session).

### Integration Points
- Phase 24 consumes the CLM claims table as its verification checklist; the DATA-07 addendum keys off CLM IDs (D-12).
- Phases 25–29 gate on the resolution doc landing at `research_reports/02-data-pipeline-and-validation/` AND Phase 24 completion — the delivery note (D-16) must state this path exactly.
- The questions-doc grouping (D-08) mirrors the Phase 26 / 27 / 28 contract clusters so the resolution doc maps onto adjudication phases.

</code_context>

<specifics>
## Specific Ideas

- The package must be consumable by repo-blind external AI agents: self-contained copies, no repo-relative references that dangle outside the package (D-02).
- The known seed conflict (ratio-based SCS thresholds vs locked log-based gate) is the worked example of why the issue doc is non-authoritative — cite it explicitly in the package's source-treatment preamble (D-09).
- Dataset figures appearing in THIS planning context (e.g., 2,565/2,749/4,857 counts, 184 gold-gap IDs, 65 blacklist IDs) are themselves claims pending Phase 24 verification, except where `simulation_data/Documentation/` already grounds them (D-13 rule applies during assembly).

</specifics>

<deferred>
## Deferred Ideas

- Prescribing a required schema for the user's resolution doc — rejected for Phase 23 (the doc is the user's product); only a format-precedent pointer ships (D-16). If adjudication phases later need a minimum structure, that is a Phase 25 concern.
- Any empirical probe (counting files, parsing footers) — Phase 24 territory; Phase 23 states claims only.
- M16 collocation-scaling, G6 causal-training, training-loop metric usage — doc-03 milestone (SCOPE-11); appear in the package only as stated exclusions.

</deferred>

---

*Phase: 23-Research Package Assembly*
*Context gathered: 2026-06-10*
