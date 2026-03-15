  Phase 0 — Preflight + Backup: GOOD TO GO                                                                 
                  
  No issues. Clean-state check without forced commit, disk space validation, rsync with parity check.

  Phase 1 — Pre-existing Bug Fixes: GOOD (minor gap)

  All 7 fixes are correctly identified. The logging.py fix (Path(__file__).resolve().parent.parent /
  "logs") is elegant — works both pre and post migration.

  Gap: The phase describes WHAT to fix but not the exact code changes. For example, it says "Fix
  ic_patterns / brutus_patterns" but doesn't give the old→new values
  (ic_standard_quasi_random_{num:04d}.txt → ic_standard_{num:04d}.txt). An executor needs the original
  plan's Task 6 details or must derive them from the codebase.

  Phase 2 — .gitignore + Data Migration: GOOD TO GO

  Gitignore committed before moves, data-only target dirs created (no collision targets), guarded moves
  without error suppression. Clean separation from tracked files.

  Phase 3 — Tracked Moves: GOOD TO GO (one minor note)

  Every git mv source verified as tracked. Gitignored sources (brutus_metrics/, brutus_output/) correctly
  use mv + git add. Tracked analysis_output copy/ handled properly with git mv.

  Note: missing_results_report_20250716_230528.txt moved to audit_reports/ will remain untracked due to the
   broad simulation_data/**/*.txt ignore rule. This matches its previous gitignored status and is
  acceptable, but worth documenting.

  Phase 4 — Path Rewrites: NEEDS EXPANSION (significant gap)

  This is the one phase that isn't ready for execution. It handles 30+ files with precise line-level edits
  but delegates all specifics to "the migration mapping already documented in the original plan" without:

  1. Including or linking to the original plan (cozy-snuggling-hoare.md Task 7)
  2. Calling out the single most critical change: config.py:16 — base_dir must change from parent.parent to
   parent.parent.parent (the package moved from depth-2 to depth-3)
  3. Listing other critical config.py changes:
    - Line 94: self.base_dir / "dataset_readiness_checks" / "reports" → self.base_dir / "Validation" /
  "dataset_readiness_checks" / "reports"
    - Line 134: self.base_dir / "brutus_metrics" → self.base_dir / "Data" / "metrics"
    - Line 139: self.base_dir / "problematic_ics_blacklist.json" → self.base_dir / "Documentation" /
  "problematic_ics_blacklist.json"
    - Lines 44-57: All final_stage_ic_datasets → Data/ic_final, all brutus_output → Data/brutus_output
  4. Listing the other high-priority files beyond the 5 mentioned (e.g.,
  run_brutus_hierarchical_only_mac_gold_standard.py, stage2_prescreening_revised_auto.py,
  FINAL_ic_generator_enhanced.py)

  Recommendation: Either inline the original plan's Task 7 mapping table into Phase 4, or add an explicit
  reference: "See cozy-snuggling-hoare.md Tasks 7a-7x for line-level changes."

  Phase 5 — Verification + Cutover: GOOD (one minor note)

  Tests all 4 variants, includes __init__.py fallback, pattern-based gitignore cleanup.

  Note: The __init__.py for Validation/ should ideally be created proactively in Phase 3.1 rather than as a
   side effect during verification in Phase 5.2. If created in 5.2, it gets committed in 5.6 (git add -A),
  which works but is less clean.

  ---
  Summary

  ┌──────────────────┬────────────────┬───────────────────────────────────────────────────────────────┐
  │      Phase       │    Verdict     │                         Action Needed                         │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 0 - Preflight    │ GOOD TO GO     │ None                                                          │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 1 - Bug Fixes    │ Good (minor    │ Add exact code changes for standalone execution               │
  │                  │ gap)           │                                                               │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 2 - Data         │ GOOD TO GO     │ None                                                          │
  │ Migration        │                │                                                               │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 3 - Tracked      │ GOOD TO GO     │ Document .txt ignore behavior in audit_reports/               │
  │ Moves            │                │                                                               │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 4 - Path         │ NEEDS WORK     │ Inline or link the line-level mapping; call out config.py     │
  │ Rewrites         │                │ base_dir change                                               │
  ├──────────────────┼────────────────┼───────────────────────────────────────────────────────────────┤
  │ 5 - Verification │ Good (minor)   │ Create __init__.py in Phase 3 instead of Phase 5              │
  └──────────────────┴────────────────┴───────────────────────────────────────────────────────────────┘

  Bottom line: Phase 4 is the only blocker. The other 5 phases are ready to execute.