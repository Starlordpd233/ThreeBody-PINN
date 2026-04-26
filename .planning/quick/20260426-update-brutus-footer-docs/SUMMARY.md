---
quick_id: 20260426-update-brutus-footer-docs
description: Update documentation that still claims Brutus output files are missing Result: footers
status: complete
completed: 2026-04-26
---

# Quick Task Summary: Update Brutus footer documentation

## Outcome

Updated 6 documentation files to reflect that all 15,028 Brutus output files contain a `Result:` footer (verified live on 2026-04-26). The remaining issue is schema variation (some footers omit `eta`; a small subset omits both `eta` and `tol`), not absence.

## Files Changed

| File | Change |
|---|---|
| `CLAUDE.md` | Replaced dead audit folder ref with current audit reports path; rewrote "Result footer inconsistency" bullet as "schema variation" |
| `AGENTS.md` | Same as CLAUDE.md |
| `GEMINI.md` | Same as CLAUDE.md |
| `ANTIGRAVITY.md` | Same as CLAUDE.md |
| `.planning/codebase/CONCERNS.md` | Rewrote "Missing Result Footers" subsection as "Result Footer Schema Variation (resolved as of 2026-04-26)" with history note |
| `.planning/codebase/TESTING.md` | Tightened wording so it describes audit detection capability, not current breakage |

## Files Intentionally NOT Modified

- `simulation_data/Documentation/README.md` — already accurate (updated 2026-03-09).
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md` — already accurate.
- `simulation_data/Validation/audit_reports/footer_audit_20251224_*.md` — historical point-in-time records.
- `simulation_data/Validation/audit_reports/missing_results_report_20250716_230528.txt` — historical point-in-time record.

## Verification

```
grep -rn -i --include="*.md" -E "(missing in many files|missing.*Result.*footer)" \
  CLAUDE.md AGENTS.md GEMINI.md ANTIGRAVITY.md .planning/codebase/
# → only the new historical-context line in CONCERNS.md (correct — describes the past)

grep -rn "check missing results line" \
  CLAUDE.md AGENTS.md GEMINI.md ANTIGRAVITY.md .planning/codebase/
# → 0 matches

git diff --name-only -- simulation_data/Validation/audit_reports/
# → 0 files (historical records preserved)
```

## Notes

- The gsd-sdk binary installed (v0.1.0) does not implement the `query` subcommand expected by the gsd-quick workflow, so this task was executed in a manual hybrid: the workflow's structure (PLAN.md, atomic commits, SUMMARY.md, STATE.md row) was followed, but planner/executor agent spawns were skipped given the trivial scope (text edits in 6 files).
