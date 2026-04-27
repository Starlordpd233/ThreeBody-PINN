# Phase 9: Issues Directory Consolidation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-27
**Phase:** 09-issues-directory-consolidation
**Areas discussed:** Theme split, Merge style, Originals disposition, Output location, Conflict resolution policy, Treatment of `next steps.txt`, Migration manifest format

---

## Theme split — how to reorganize the 7 files into thematic documents

| Option | Description | Selected |
|---|---|---|
| 3 docs by system layer | architecture-and-physics / data-pipeline-and-validation / curriculum-and-training-loop. Maps to likely future implementation phases. | ✓ |
| 3 docs by readiness status | blockers / open-design-decisions / implementation-roadmap. Kanban-style. | |
| 2 docs: comprehensive audit + design | Coarsest split using audit as spine of doc 1. | |
| 3 docs by source intent | findings-and-blockers / proposed-resolutions / open-questions. | |

**User's choice:** 3 docs by system layer (Recommended).

**Notes:** First pass the user said "I don't know what would be the best way to organize these 7 files" and asked Claude to research file content and propose options. After reading all 7 files (or skimming the largest), Claude presented 4 grouping options. User selected the system-layer split because it aligns with the three likely future implementation phases (data, architecture, training).

---

## Merge style — how content is carried into the new docs

| Option | Description | Selected |
|---|---|---|
| Synthesized rewrite | Fresh thematic docs that re-state findings, deduplicate, cross-link. | ✓ |
| Verbatim concatenation | Concatenate originals under thematic headers, paragraph-perfect fidelity. | |
| Hybrid: synthesized exec summary + verbatim appendix | Each new doc has rewritten intro + verbatim appendix. | |

**User's choice:** Synthesized rewrite (Recommended).

**Notes:** Source docs total ~245 KB. Target combined size of 80–120 KB through deduplication. Audit's structural skeleton (Exec Summary → Critical Issues → Inconsistencies → Ambiguities → Corrected Specs → Checklist) is reused as the spine for each thematic doc.

---

## Originals disposition — what happens to the 7 source files

| Option | Description | Selected |
|---|---|---|
| Move to `issues/archive/` | Move all 7 to archive subfolder; rely on MIGRATION.md for provenance. | ✓ |
| Delete (rely on git history) | Remove the 7 originals; git log + MIGRATION.md only. | |
| Keep in place with deprecation header | Prepend "SUPERSEDED BY <new doc>" header to each. | |

**User's choice:** Move to issues/archive/ (Recommended).

**Notes:** Use `git mv` to preserve history. No deprecation header injection — folder name + MIGRATION.md carry the signal.

---

## Output location — where the new thematic docs live

| Option | Description | Selected |
|---|---|---|
| Same `issues/` directory | Drop new docs in the same folder as originals (now archived). | ✓ |
| New `review-of-framework/audit/` subfolder | Stronger separation between historical issues and current audit. | |
| Promote to `review-of-framework/` root | Place at framework review root next to existing structure. | |

**User's choice:** Same issues/ directory (Recommended).

---

## Conflict resolution — handling contradictions between source files

| Option | Description | Selected |
|---|---|---|
| Surface as open decision | Both positions side-by-side under `[DECISION-NEEDED]` callout. | |
| Pick newer source's recommendation | Defer to most recent source (usually 2026-04-27 audit). | |
| Pick stronger physical/mathematical justification | Claude evaluates per-conflict, documents reasoning inline. | ✓ |

**User's choice:** Pick whichever has stronger physical/mathematical justification.

**Notes:** Two known live conflicts must be addressed by name in the new docs:
- Input vector orientation encoding: trig values (audit B-04, §5.3) vs shape invariants + direction cosines (Causal_Trainingmismatch). Recommended verdict: shape invariants + direction cosines (gimbal-lock argument is decisive for chaotic-scattering regimes).
- `s_min` softening for collision criterion: unsoftened raw separation vs `max(s_min, epsilon)` (audit D8).

The losing position is preserved under "Considered Alternatives" in the relevant thematic doc — not silently dropped.

---

## `next steps.txt` (128 KB, mostly superseded) — how to handle

| Option | Description | Selected |
|---|---|---|
| Cherry-pick unique content only | Extract content not covered by audit; archive the rest. | ✓ |
| Treat equally with the others | Pull all 19 issues even where they overlap with audit. | |
| Archive entirely with a pointer | Single-line MIGRATION.md note; lose unique deep dives. | |

**User's choice:** Cherry-pick unique content only (Recommended).

**Notes:** Verified-unique candidates to extract:
- "5 Orders of Magnitude Difference" softening analysis
- Issue 17: Global scale computation pseudo-code
- Issue 19: Normalization formulas verification table
- Issue 1 resolution: Lyapunov τ_L and L_max formulas
Each candidate must be checked for absence in the 2026-04-27 audit before extraction.

---

## Migration manifest — format of `archive/MIGRATION.md` (decision: lives at `issues/MIGRATION.md`, not inside archive/)

| Option | Description | Selected |
|---|---|---|
| Per-file map of where every section went | Detailed table per source file with destination doc(s) and "unique findings preserved" checklist. | ✓ |
| Short table mapping old→new file only | 7-row table; less detailed provenance. | |
| Just a README with paragraph note | Minimal; doesn't help reconstruct what went where. | |

**User's choice:** Per-file map of where every section went (Recommended).

**Notes:** Required to satisfy success criterion 2 ("No unique findings from the original files are lost in consolidation"). The "unique findings preserved" checklist is the auditable proof.

---

## Claude's Discretion

- Naming convention `01-`, `02-`, `03-` numbered prefix on the 3 new docs
- Adding `issues/README.md` as navigation anchor (≤ 50 lines)
- Section headings within each thematic doc (use audit subsections as a guide)
- Severity classification: reuse audit's BLOCKING / MAJOR / MINOR / INFO labels for cross-doc consistency
- Format choices for `[DECISION-NEEDED]` callouts (markdown blockquotes recommended)
- Whether to copy audit's §5 (Corrected Input Vector Spec) and §6 (Unified Batch Construction) verbatim into the relevant thematic docs (recommend: yes — they are reference specs that downstream phases will quote)

## Deferred Ideas

- Implementation of any audit finding (B-01 SIREN init, B-02 D-formula, B-05 unified COM transformer, B-09 epsilon unification, B-11 TrajectoryIndex, etc.) — future v1.2 phases 10+
- Updating LaTeX source documents to match consolidated findings — future LaTeX-revision phase
- Resolving the 12 author-flagged `\authcomment` items — future LaTeX-revision phase
- File format conversion h5 → txt/json — surfaced as `[DECISION-NEEDED]` in `02-...`, decided in future data-pipeline phase
- Re-running stage assignment for all ~15K trajectories — future data-pipeline phase
- Expanding `.planning/REQUIREMENTS.md` v1.2 requirements (CONSOL-01..CONSOL-03) — flagged for the planner, not this discussion
