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
