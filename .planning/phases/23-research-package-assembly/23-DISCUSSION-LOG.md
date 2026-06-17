# Phase 23: Research Package Assembly - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-10
**Phase:** 23-Research Package Assembly
**Areas discussed:** Package location & delivery form; Document-list inventory & inclusion criteria; Question framing & structure; Claims register & Phase 24 handoff; DQA characterization deliverable; Gate-opening record & handoff mechanics
**Mode:** `--auto --all --batch --analyze` — no interactive prompts; Claude selected the recommended option per area and logged trade-off analyses below. The user can override any selection by editing `23-CONTEXT.md` before planning/execution.

---

## Package location & delivery form

| Option | Description | Selected |
|--------|-------------|----------|
| `research_reports/02-data-pipeline-and-validation/research_package/` | Co-located with where the resolution doc lands; mirrors v1.4 layout (`research_reports/01-*/` holds inputs + outputs) | ✓ |
| `.planning/phases/23-*/` | Keeps GSD artifacts together, but buries a user-facing deliverable in internal planning | |
| `.planning/research/` | EDL-brief precedent, but EDL is explicitly non-canonical support; this is the milestone-critical-path deliverable | |

**Auto-selected:** research_package/ subdir under the expected resolution-doc directory; self-contained snapshot copies with per-file source path + commit hash in a manifest (external AI agents are repo-blind).
**Notes:** Snapshot duplication is deliberate — the research state is pinned; specs do not change during the gate window (spec edits start Phase 26, gated on the doc).

---

## Document-list inventory & inclusion criteria

| Option | Description | Selected |
|--------|-------------|----------|
| Candidate inventory + criteria now; final list at execution | Respects PKG-04 sequencing (DQA characterization informs the list) and the PKG-01 user checkpoint before assembly | ✓ |
| Lock the final list now | Pre-empts the mandated user surfacing and the DQA characterization | |

**Auto-selected:** candidate inventory (issue doc; ctl_instruction.md + pinn_architecture.md intact; sampling_method.md intact marked FROZEN; data_quality_assessment.md pending PKG-04; one consolidated context file for dataset-doc + script fragments). `pinn/` excluded with the override stated as a hard constraint. Issue-01/issue-03 excluded (v1.4 outcomes travel as constraints + intact specs; doc-03 boundary statement covers issue-03).
**Notes:** ≥6 deliverable files → PKG-01 consolidation rule fires → consolidation plan MUST be surfaced to the user before assembly (hard execution checkpoint, modeled in plans as a user gate).

---

## Question framing & structure

| Option | Description | Selected |
|--------|-------------|----------|
| Per-finding questions grouped by contract cluster | Matches PKG-02 ("each finding posed as an explicit question"); grouping mirrors Phases 26–28; splittable across AI sessions | ✓ |
| One mega-prompt | Single artifact but buries findings; shallow-coverage risk | |
| Per-document questions | Mismatch — findings span documents | |

**Auto-selected:** per-finding neutral questions in three clusters (ingestion & selection / sampling-precision-global-scale / validation metrics), shared hard-constraints preamble (the PKG-02 locked-conventions list verbatim), doc-03 exclusions stated per-question and in the preamble.
**Notes:** Explicit instruction to external research that the issue doc AND its "Recommended Resolutions" are non-authoritative, citing the SCS-threshold seed conflict as the worked example.

---

## Claims register & Phase 24 handoff

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated claims table with stable CLM-NN IDs | Enumerable; Phase 24 consumes it as the verification checklist; DATA-07 addendum keys off the IDs | ✓ |
| Inline "claimed, unverified" tags only | Satisfies PKG-03 prose-wise but gives Phase 24 no enumerable claim list (roadmap dependency) | |

**Auto-selected:** claims table + inline CLM references. Conservative verified-status rule: only `simulation_data/Documentation/` files and committed prior-phase probe evidence count as prior grounding; `.planning/codebase/*` maps (2026-04-27) do not; doubt → claimed-unverified.

---

## DQA characterization deliverable

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone `23-DQA-CHARACTERIZATION.md` in the phase dir | Follows NN-artifact convention; committed; reported to user in delivery summary | ✓ |
| Section inside the package | Mixes an internal report-to-user with the external research artifact | |
| docs/findings/ | Convention drift — phase deliverables live in phase dirs | |

**Auto-selected:** standalone phase artifact, sequenced before document-list finalization (roadmap success criterion 1). Zero edits to the DQA file (SCOPE-09).

---

## Gate-opening record & handoff mechanics

| Option | Description | Selected |
|--------|-------------|----------|
| Delivery note + STATE.md gate record via gsd-tools | States the exact resolution-doc landing path, the v1.4 format precedent (suggestion only), and Phase 24 parallelism | ✓ |
| Required resolution-doc schema | Oversteps — the doc is the user's product; PKG requirements don't ask for it | |

**Auto-selected:** delivery note + state-managed gate record (no direct STATE.md writes).

---

## Claude's Discretion

- Exact file names inside the package (manifest, questions doc, claims-table placement) — presentation-only.
- Which `simulation_data/Scripts/` excerpts enter the consolidated context file — per-finding judgment within the inclusion criterion, shown at the consolidation checkpoint.
- `sampling_method.md` inclusion — recommended yes; final call at the consolidation user checkpoint.

## Deferred Ideas

- Required schema for the user's resolution doc — Phase 25 concern if adjudication needs a minimum structure.
- Any empirical dataset probe — Phase 24.
- M16 / G6 / training-loop metric usage — doc-03 milestone (SCOPE-11); package states the exclusions only.
