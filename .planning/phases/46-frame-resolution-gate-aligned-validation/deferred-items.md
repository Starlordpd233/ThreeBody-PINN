# Phase 46 deferred items

Out-of-scope discoveries logged during execution. Per the executor scope-boundary
rule, pre-existing failures in unrelated files are recorded here, never fixed
inline by a later plan.

## DI-46-04-01 — `tests/phase43` pre-existing failures (12)

- **Found during:** Plan 46-04 phase-wide verification sweep (2026-07-26).
- **Observed:** 12 failed / 186 passed in `tests/phase43` under the confirmed
  interpreter: `DurationGateLaunchTests` (2), `HonestyGuardTests` (1),
  `PilotCalibrationEvidenceTests` (2), `VerdictGroundingTests` (7).
- **Cause (two environmental classes, both pre-existing):**
  1. `DurationGateLaunchTests` — the ACC-02 timing calibration is a run artifact
     present in the main checkout, not this worktree (already documented by
     plan 46-01's SUMMARY).
  2. Verdict/calibration/grounding tests — `FileNotFoundError` for
     `.planning/phases/43-verification-stage-0-pilot-acceptance/*`; the v2.0
     milestone artifacts now live under
     `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/`
     after milestone archival, so these test paths are stale.
- **Coupling with 46-04:** none — no `tests/phase43` module imports
  `pinn.verification.target_frame_probe` (grep-verified); the failure set is
  identical before and after this plan's diff.
- **Disposition:** deferred. Remediation belongs to a phase-43 test-path repair
  (point the artifact paths at the archived milestone location or skip when the
  v2.0 archive is absent), not to Phase 46.

## DI-46-05-01 — `tests/watchdog/test_global_packaging.py` pre-existing failures (2)

- **Found during:** Plan 46-05 phase-wide verification sweep (2026-07-27).
- **Observed:** 2 failed in `tests/watchdog/test_global_packaging.py` under the
  confirmed interpreter: `GlobalPackagingTests::test_a5_canonical_bin_matches_repo_source`
  and `test_a6_deployed_skill_paths_rewritten`.
- **Cause (environmental, pre-existing):** the tests compare the repo's
  `scripts/watchdog/` source against the live canonical global deploy
  (`~/.claude` bin/skills). `wd-arm` differs between repo and canonical bin
  (DRIFT assertion) — the repo source was updated by watchdog work outside this
  phase (the standalone-extraction effort) without a redeploy. The failure set
  is identical with and without this plan's diff, which adds two files under
  `tests/phase46/` and touches nothing else.
- **Coupling with 46-05:** none — no `tests/phase46` module imports or
  references watchdog packaging; the drift is in `scripts/watchdog/` vs the
  global deploy location.
- **Disposition:** deferred. Remediation belongs to the watchdog
  redeploy/extraction track (regenerate the canonical deploy from the repo
  source), not to Phase 46. The 12 pre-existing `tests/phase43` failures
  (DI-46-04-01) are unchanged: same 12 tests, zero new phase43 failures.
