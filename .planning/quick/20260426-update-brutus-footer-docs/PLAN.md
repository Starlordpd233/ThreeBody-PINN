---
quick_id: 20260426-update-brutus-footer-docs
description: Update documentation that still claims Brutus output files are missing Result: footers
created: 2026-04-26
status: in-progress
---

# Quick Task: Update Brutus footer documentation

## Context

Live verification on 2026-04-26 confirmed all 15,028 Brutus output files contain a `Result:` footer line. A December 2025 audit (`simulation_data/Validation/audit_reports/footer_audit_20251224_170141.md`) had previously found 2,470 files missing footers and 3,273 with partial footers; those gaps were closed by `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`.

Several documentation files still describe footers as "missing in many files" or reference a dead audit folder path (`simulation_data/Data/brutus_output/check missing results line/`, which no longer exists). These need correction so downstream agents and readers don't act on stale assumptions.

## Already-Accurate Docs (do NOT touch)

- `simulation_data/Documentation/README.md` — already updated 2026-03-09 ("All Brutus output files contain a `Result:` footer, but the footer schema varies"). Uses "partial" to mean missing `eta` field, not missing energy fields. Counts match audit.
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md` — same updated content as README.md.
- `simulation_data/Validation/audit_reports/footer_audit_20251224_*.md` — historical point-in-time records; preserve as-is.
- `simulation_data/Validation/audit_reports/missing_results_report_20250716_230528.txt` — historical audit; preserve as-is.

## Files to Update

### Agent instruction files (4 — content differs slightly per file)

1. `CLAUDE.md`
   - Lines 261-262: Replace dead audit folder ref with current audit reports directory.
   - Line 270: Rewrite "Result footer inconsistency: Optional, missing in many files" → schema-variation language matching `simulation_data/Documentation/README.md`.
2. `AGENTS.md` — same two locations as CLAUDE.md.
3. `GEMINI.md` — same two locations as CLAUDE.md.
4. `ANTIGRAVITY.md` — lines 253-254 and 262.

### Codebase concern docs

5. `.planning/codebase/CONCERNS.md` — Lines 33-37: Rewrite "Missing Result Footers" subsection. Footer presence is no longer a concern; only schema variation matters. Reference current audit reports path.
6. `.planning/codebase/TESTING.md` — Line 26: Tighten wording so it doesn't imply footers are *currently* missing — describe what the audit script *can detect* rather than what is *currently broken*.

## Replacement Wording (canonical)

For the "Known Issues" bullet (CLAUDE.md / AGENTS.md / GEMINI.md / ANTIGRAVITY.md):

> **Result footer schema variation**: All files contain a `Result:` footer, but the schema varies — some omit `eta`, and a small subset of standard-quasi-random gold files omit both `eta` and `tol`. When `tol` is absent from the footer, fall back to folder defaults. See `simulation_data/Documentation/README.md` "Brutus Parameters by Variant" for per-folder schema counts.

For the "Provenance and Audit Files" bullet:

> - Footer audit reports:
>   - `simulation_data/Validation/audit_reports/` (most recent: `footer_audit_20251224_170141.md`)
>   - Audit/backfill script: `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`

## Commit Plan

- **Commit 1**: `docs: update agent files — Brutus footer state is schema-variation, not missing`
  - CLAUDE.md, AGENTS.md, GEMINI.md, ANTIGRAVITY.md
- **Commit 2**: `docs(planning): mark missing-footer concern as resolved (schema variation only)`
  - .planning/codebase/CONCERNS.md, .planning/codebase/TESTING.md
- **Commit 3**: `docs(quick-20260426): record footer-docs update task`
  - PLAN.md, SUMMARY.md, .planning/STATE.md

## Verification

After updates:
- `grep -rn -i --include="*.md" -E "(missing.*Result.*footer|Result.*footer.*missing|missing in many files)" CLAUDE.md AGENTS.md GEMINI.md ANTIGRAVITY.md .planning/codebase/` → 0 matches.
- `grep -rn "check missing results line" CLAUDE.md AGENTS.md GEMINI.md ANTIGRAVITY.md .planning/codebase/` → 0 matches.
- Historical audit reports under `simulation_data/Validation/audit_reports/` remain unchanged (`git diff` shows no edits there).
