# Phase 4: Stale Reference Fixes - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix all stale code imports, documentation filename references, and agent instruction file drift caused by Phase 1 renames (`FINAL_ic_generator_enhanced.py` → `ic_generation_utils.py`, `generate_enhanced_ics.py` → `generate_ics.py`) and Phase 3 deletions (`_for_gold_standard` IC folders, `ic_raw/`). This is a gap closure phase — no new capabilities, only fixing references that were missed by phase-level verifiers.

</domain>

<decisions>
## Implementation Decisions

### QWEN.md Resolution
- Phase 2 Plan 03 claimed to update QWEN.md, but the file does not exist on the filesystem
- Investigate whether QWEN.md ever existed (check git history) — if it never existed, AGENTS.md is the actual 4th agent instruction file
- If QWEN.md never existed: update AGENTS.md Section 3.2 to match CLAUDE.md/GEMINI.md/ANTIGRAVITY.md
- If QWEN.md was deleted: determine if it should be recreated or if AGENTS.md replaces it
- Update DOCS-04 requirement description to reflect the actual set of agent files

### Stale Filename Scope
- Fix ALL stale references project-wide, not just the files explicitly flagged in the audit
- This includes: agent instruction files (all non-3.2 sections), root README.md, simulation_data/Documentation/README.md, test_pipeline.py, generate_ics.py, and any other file referencing old names
- Old names to replace: `FINAL_ic_generator_enhanced.py` → `ic_generation_utils.py`, `generate_enhanced_ics.py` → `generate_ics.py`
- Also fix stale `ic_raw` / `ic_raw_datasets` references in documentation and code comments

### test_pipeline.py Fix
- Fix the broken import: `from FINAL_ic_generator_enhanced import ...` → `from ic_generation_utils import ...`
- Check for any other stale references in the same file and fix them

### generate_ics.py Print Statement
- Fix `generate_ics.py:56` print statement that references `ic_raw_datasets/`
- Update to reflect the IC_RAW_DIR externalization pattern (e.g., `$IC_RAW_DIR/ic_hierarchical/`)

### simulation_data/Documentation/README.md Cleanup
- Fix lines 22-23, 25, 70, 272, 349-350 as identified by integration checker
- Update old filenames to new names
- Update Interaction Diagram to show IC_RAW_DIR instead of `Data/ic_raw/`
- Update Stage 2 Input reference

### AGENTS.md Section 3.2 Update
- Apply the same Section 3.2 content from CLAUDE.md/GEMINI.md/ANTIGRAVITY.md
- Must show: 2 IC folders, IC_RAW_DIR externalization note, no `_for_gold_standard` directories
- Also fix stale filenames in non-Section-3.2 areas (pipeline descriptions, command refs, key file tables)

### REQUIREMENTS.md Bookkeeping
- The 5 stale checkboxes (PATH-04, PATH-05, VALD-01, VALD-02) were already fixed during gap planning
- PATH-06 checkbox will be fixed after this phase completes
- Do NOT backfill SUMMARY frontmatter `requirements_completed` — that's non-blocking tech debt

### Claude's Discretion
- Exact ordering of file updates within the phase
- Whether to combine all filename updates into one task or split by file type (code vs docs)
- How to handle any additional stale references discovered during implementation

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Audit Report (defines gaps to close)
- `.planning/v1.0-MILESTONE-AUDIT.md` — Full audit with gap details, integration findings, and tech debt inventory. Section "Gap Details" has the specific lines and files to fix.

### Files to Fix (code)
- `simulation_data/Data/testing_data/test_pipeline.py` — Line 61: broken import `from FINAL_ic_generator_enhanced`. Line 69: `ic_raw` path reference.
- `simulation_data/Scripts/ic_generation/generate_ics.py` — Line 56: stale print referencing `ic_raw_datasets/`

### Files to Fix (documentation)
- `simulation_data/Documentation/README.md` — Lines 22-23, 25, 70, 272, 349-350: old filenames and unqualified `Data/ic_raw/` path
- `AGENTS.md` — Section 3.2: still lists 4 IC folders including deleted `_for_gold_standard` directories; non-3.2 sections have stale filenames
- `CLAUDE.md` — Lines 75, 169, 220, 281: stale IC generator filenames in non-3.2 sections
- `GEMINI.md` — Lines 75, 161, 212, 273: stale IC generator filenames in non-3.2 sections
- `ANTIGRAVITY.md` — Lines 67, 161, 212, 273: stale IC generator filenames in non-3.2 sections
- `README.md` (root) — Lines 77, 149: stale `generate_enhanced_ics.py` filename

### Reference (correct content to copy)
- `CLAUDE.md` Section 3.2 — The canonical Section 3.2 content that was applied to GEMINI.md and ANTIGRAVITY.md in Phase 2. Apply same to AGENTS.md.

### Prior Phase Context
- `.planning/phases/01-code-rewrites-and-validation/01-CONTEXT.md` — Phase 1 rename decisions
- `.planning/phases/02-documentation-updates/02-CONTEXT.md` — Phase 2 documentation scope and agent file decisions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- CLAUDE.md Section 3.2 content already exists as canonical template — copy to AGENTS.md
- Phase 2 established the pattern for identical Section 3.2 across agent files

### Established Patterns
- Agent instruction files share identical dataset inventory sections (Section 3.2)
- IC generator was renamed in Phase 1: FINAL_ic_generator_enhanced.py → ic_generation_utils.py, generate_enhanced_ics.py → generate_ics.py
- IC_RAW_DIR pattern: `os.environ.get('IC_RAW_DIR')` with RuntimeError on missing

### Integration Points
- test_pipeline.py imports from ic_generation_utils (the renamed module)
- generate_ics.py prints user-facing messages about output locations
- Agent instruction files guide AI agents on project structure and file locations
- README.md files are the primary human-facing documentation

</code_context>

<specifics>
## Specific Ideas

- The filename renames happened in Phase 1 but many files outside Phase 1's scope still reference the old names
- This is a sweep-and-fix phase — systematic grep for old names, replace with new names
- AGENTS.md may be the actual 4th agent file (not QWEN.md) — check git history to confirm

</specifics>

<deferred>
## Deferred Ideas

- SUMMARY frontmatter `requirements_completed` backfill — non-blocking bookkeeping, not worth a phase
- `paper_templates/mdpi_template/` residual `.bbl`/`.blg` files — out of CLN-04 scope, minor

</deferred>

---

*Phase: 04-stale-reference-fixes*
*Context gathered: 2026-03-19*
