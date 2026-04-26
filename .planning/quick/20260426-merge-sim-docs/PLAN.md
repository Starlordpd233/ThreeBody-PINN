# Quick Task: Merge simulation_data Documentation

## Description
Combine `simulation_data/Documentation/DATASET_DOCUMENTATION.md` and `README.md` into a single comprehensive `README.md`, then remove the old `DATASET_DOCUMENTATION.md`. Update cross-references in project root files.

## Verified Findings
- All file counts, disk usage, prescreening indices, footer schemas, and parameter distributions match documentation.
- One correction: `problematic_ics_blacklist.json` has 63 standard IDs (not 64).

## Steps
1. Write merged `simulation_data/Documentation/README.md` using `DATASET_DOCUMENTATION.md` as backbone, folding in unique elements from old `README.md`.
2. Delete `simulation_data/Documentation/DATASET_DOCUMENTATION.md`.
3. Update references in root project files (`README.md`, `CLAUDE.md`, `AGENTS.md`, `ANTIGRAVITY.md`, `GEMINI.md`) to point to `simulation_data/Documentation/README.md`.
4. Verify merged file completeness.
