# Directory Restructuring Master Plan (Corrected)

## Scope
Restructure `3_Body_Problem/` into `simulation_data/` with a phased workflow that separates:
1. Pre-existing bug fixes
2. Migration mechanics
3. Path rewrites + docs
4. Verification + final cutover

This corrected plan explicitly addresses execution bugs identified in `findings.md` and `review.md`.

## Plan Bundle

Execution is split across phase documents:

1. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-0-preflight-backup.md`
2. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-1-preexisting-bugfixes.md`
3. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-2-gitignore-and-data-migration.md`
4. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-3-tracked-moves-and-structure.md`
5. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-4-path-rewrites-and-docs.md`
6. `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-5-verification-and-cutover.md`

Use `<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/README.md` as the operator checklist.

---

## Issue Resolution Matrix

### Resolved Critical Failures

1. **`git mv` on ignored/untracked files**
- Fixed by replacing those operations with `mv + git add` in Phase 3 for:
  - files sourced from `3_Body_Problem/brutus_metrics/`
  - files sourced from `3_Body_Problem/brutus_output/check missing results line/`

2. **Destination-collision risk from pre-created directories**
- Fixed by not pre-creating whole-directory `git mv` targets:
  - `simulation_data/Scripts/debug/renaming`
  - `simulation_data/Validation/dataset_readiness_checks`
  - `simulation_data/Validation/prescreening/utilities`

3. **Contradictory backup commit flow**
- Fixed by using clean-state check + tag snapshot (no forced extra commit when no changes exist).

4. **Broken logging path fix (`Validation/Validation/...`)**
- Corrected to:
```python
self.log_dir = Path(__file__).resolve().parent.parent / "logs"
```
which is valid before and after migration.

### Resolved High/Significant Issues

5. **Missing staging before commit**
- Every phase commit now includes explicit `git add -A`.

6. **References to deleted docs (`plan.md`, `dataset_readiness_checks_b73004bc.plan.md`)**
- Removed from docs-update scope.

7. **Brittle `.gitignore` cleanup by fixed line numbers**
- Replaced with pattern-based cleanup (`^3_Body_Problem/`) in final cutover.

8. **Tracked `analysis_output copy/` treated as untracked**
- Fixed with Git-aware handling in Phase 3 (`git mv`), no blind `rm -rf`.

9. **Verification too narrow (single variant)**
- Expanded to all four variants: `hierarchical`, `hierarchical_gold`, `standard`, `standard_gold`.

10. **Silent move failures masked by `2>/dev/null`**
- Removed suppression; replaced with guarded checks.

11. **No backup disk-space precheck**
- Added explicit free-space validation before `rsync`.

12. **Phase 4 underspecified (path rewrites)**
- Expanded with full line-level change tables for all 30+ files, organized by priority.
- `config.py` `base_dir` change (`parent.parent` → `parent.parent.parent`) explicitly called out as highest-priority edit.

13. **Phase 1 lacked exact code changes**
- Expanded with old→new tables for each fix.

14. **`Validation/__init__.py` created reactively in verification**
- Moved to proactive creation in Phase 3.1.

15. **`--modules` CLI argument silently discarded**
- `run_validation()` in `validator.py` created a fresh `ValidationConfig()`, ignoring `enabled_modules` set via CLI.
- Fixed by adding `modules` parameter to `run_validation()` in Phase 1 Step 8.

16. **Metrics filename pattern mismatch (`standard_0000.json` vs `metrics_standard_0000.json`)**
- `validator.py:226` constructed filenames without the `metrics_` prefix.
- Fixed in Phase 1 Step 9.

17. **Metrics JSON key schema mismatch**
- `modules/metrics.py` expected flat keys (`final_energy_error`, `momentum_drift`) but actual JSON uses nested structure (`conservation.energy.relative_error`, etc.).
- Fixed in Phase 1 Step 10 to match actual schema.

18. **Phase 5.1 grep false positives from plan files**
- The stale-reference scan had no `--glob '!docs/plans/*'` exclusion, causing 172 false positives from plan documents that intentionally contain `3_Body_Problem` references.
- Fixed by adding `--glob '!docs/plans/*'` exclusion to Phase 5.1 and Phase 4.12.

19. **Phase 1 Step 6 missing `import os`**
- The proposed fix for `compare_thresholds.py` used `os.path.exists()` without importing `os`.
- Fixed by adding `import os` to the proposed code snippet.

20. **Completeness scans miss `.txt` files**
- Phase 4.12 scanned `--type py` only; Phase 5.1 scanned `--type py --type tex --type md`. Neither covered `.txt` files like `parsing.txt` which Phase 4 explicitly rewrites.
- Fixed by adding `--type txt` to Phase 4.12 and Phase 5.1 scan scope.

---

## Execution Guardrails

- Run phases in strict order.
- Do not combine phase commits.
- Stop on first unexpected `git status` change.
- If a command differs from observed repo reality, update the phase doc before proceeding.
- Keep `3_Body_Problem` ignore rules until the old tree is fully removed.

---

## Notes on Design Choices

- `simulation_data/` remains the migration root for Data, Scripts, Validation, and Documentation to preserve existing migration intent.
- `problematic_ics/` stays under `Documentation/` in this revision for compatibility with already-planned path rewrites.
- If stricter semantics are preferred later, a follow-up migration can move runtime operational artifacts to `Data/`.

---

## Success Criteria

Migration is complete only when:
1. All phases pass exit criteria.
2. Code + docs contain no active stale `3_Body_Problem` references.
3. Validation runs for all four variants without import/path errors.
4. `3_Body_Problem/` is removed (or blocked with explicit diagnostic output).
5. `.gitignore` contains only `simulation_data` rules for migrated paths.
