---
phase: 67-design-settings-ladders
plan: "06"
subsystem: testing
tags: [pytorch, unittest, diagnostic-harness, tdd, cli-contract, power-gate, process-supervision, provenance]

requires:
  - phase: 67-design-settings-ladders (67-01)
    provides: the phase67 registry dispatch, the admission door, read_phase67_record and the tests/phase67 synthetic fixtures
  - phase: 67-design-settings-ladders (67-02)
    provides: PHASE67_ARMS/phase67_variant and the encoded input declarations the run matrices resolve
  - phase: 67-design-settings-ladders (67-03)
    provides: the window-evidence/baseline conventions the metadata capture reuses through same_window_expectations
  - phase: 67-design-settings-ladders (67-04)
    provides: PHASE67_BUDGET_RULE, phase67_budget and the registered cadence functions every row schedule declares
  - phase: 67-design-settings-ladders (67-05)
    provides: read_phase67_run_directory, phase67_contrast/confirmation, PHASE67_CASES and the control-arm resolver the review consumes
provides:
  - The thirteen Phase 67 CLI commands (prepare-design through audit-phase) on the established `-B -m pinn.verification.diagnostic_phase67` entry point, with exact paths, flags and refusal contracts for plans 67-08..67-16
  - phase67_design / phase67_run_matrix / admit_phase67_metadata_registration / capture_phase67_metadata / launch_phase67_row / audit_phase67 and the six new schemas (phase67-design/v1, -metadata-registration/v1, -metadata/v1, -run-matrix/v1, -budget/v1, -review/v1)
  - require_remaining_window + weekend_closing_utc in diagnostic_power — the full-cap remaining-window admission (Sunday 22:00 America/Chicago closing instant, DST-exact UTC arithmetic, exact now+cap equality admitted, the next instant refused)
  - The bounded outer supervisor (_run_outer_supervised) — a spawned child owning its process group, SIGTERM-then-SIGKILL to the whole group on cap expiry, the attempt preserved incomplete, nothing published, no retry
  - The encoded logger-parity receipt branch in the fit admission (null aggregate frequency beside pinned per-harmonic metadata admits; half-encoded hybrids refuse)
affects: [67-07 (compatibility gate and harness freeze over these commands), 67-08..67-15 (experiment execution invoking them), 67-16 (phase audit), Phase 68 energy adjudication]

actuals:
  tokens: 57720
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Injectable supervisor seam: every real operation runs as supervised(target, args, timeout=cap) — an inline in-process supervisor for synthetic tests, a spawn-based process-group-owning child for real work, one queue-appended payload contract"
    - "Gate evidence rides the receipt: the capture receipt records the closing instant, remaining allowance and gate moment so the remaining-window admission is recheckable from committed bytes alone"
    - "Read-only verification doors validate what the machine can run: check-matrix settings-validates every row through the run door's validate_smoke_settings, so a registration naming an unavailable runtime refuses at matrix-check time"

key-files:
  created:
    - pinn/verification/diagnostic_phase67_execution.py
    - tests/phase67/test_pages.py
    - tests/phase67/test_workflow.py
    - tests/phase67/test_isolation.py
  modified:
    - pinn/verification/diagnostic_phase67.py
    - pinn/verification/diagnostic_phase67_catalog.py
    - pinn/verification/diagnostic_fit.py
    - pinn/verification/diagnostic_power.py
    - tests/phase67/test_admission.py
    - tests/phase67/test_catalog.py
    - tests/phase67/test_historical.py

key-decisions:
  - "The remaining-window admission is a power-gate primitive, not launcher folklore: weekend_closing_utc derives the Sunday 22:00 closing instant from the receipt's own aware weekend instant on the Chicago wall clock (Saturday derives the next day's, Sunday the same day's, so a DST transition inside the weekend is exact) and require_remaining_window compares aware UTC instants — exact equality admits, the next representable instant refuses, for both the 900-second metadata/timing and 3540-second science caps."
  - "The outer supervisor's monotonic timer starts at the spawn, before power/admission, and the registered cap covers every overhead — data load, baseline scoring, publication — not just fit time; a cap expiry stops the child's whole process group (the fixed-argv caffeinate/fit descendants join it) and preserves the attempt explicitly incomplete (wall_cap_expired) with nothing published, never a rename, resume or retry."
  - "The deadline a synthetic test fires may be earlier than the registered cap (the same supervised-stop mechanism at fixture scale), because the spawned child re-admits the registration against the unpatched rule module — a rule patch cannot cross the spawn boundary, so the fixture keeps the real 900-second cap and fires the stop early instead."
  "check-matrix settings-validates each row through validate_smoke_settings (the run door's settings half) after the metadata-only identity door, so an mps-declaring registration on a machine without MPS refuses at matrix-check time — before any launch — while check-matrix stays corpus-free and value-free."
  - "The encoded (D-05) logger-parity receipt now admits as a measurement: null aggregate median/max beside an explicit false applicability, a reason, the pinned per-harmonic cycles, the harmonic list and the internal dimension (14 + 2·harmonics); a half-null hybrid, a manufactured applicability or a non-numeric cycle still refuses — the 67-05 recorded adapter item."
  - "The D-12 live-pin transition grows to its fourth file: task 2's diagnostic_power.py edit joins diagnostic_fit/variants/similarity in EDITED_PINS, with run-commit historical provenance still verifying and live new-run admission still refusing on the changed dependency."
  - "Malformed command input and audit problems return controlled exit 2 through one bounded handler — never a clean status, never an unhandled traceback; markers print only after verified completion."

patterns-established:
  - "Command tables with exclusive first-write evidence: every artifact family is written exactly once (the first completed capture/run is the evidence; a second never replaces it), and dependent commands refuse before creating any downstream file"
  - "Cost-only budget discipline at the command layer: budget consumes only the committed timing rows' cost fields, writes the immutable science prediction page separately, and changing timing scores cannot alter the budget, science settings or prediction text (proven by test)"

requirements-completed: []  # EXP-02..05 are declared by every 67-0N plan; the experiments run in 67-08..67-15 and the marks flip at the phase verification act (shared-ID gate: siblings also declare them), matching the 67-01..05 convention.

coverage:
  - id: D1
    description: "The thirteen Phase 67 commands and their exact path/flag/refusal contracts operating end to end on a synthetic fixture repo: frozen design and metadata registration, gated metadata-only capture, exact case-major matrices with committed registrations, single-row launches, the cost-only budget with immutable pages, the review with matched contrasts and conditional SCOPE-49 authority, and the read-only audit"
    requirement: EXP-02
    verification:
      - kind: integration
        ref: "tests/phase67/test_workflow.py#WorkflowChainTests.test_audit_phase_reports_every_experiment_read_only"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_workflow.py#CommandContractTests.test_unknown_commands_experiments_kinds_cases_arms_and_flags_refuse"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_workflow.py#CommandContractTests.test_a_pending_proposal_blocks_only_the_dependent_experiment"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_pages.py#DesignPageTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The real-operation boundaries: battery/weekday/late-Sunday/disk/dirty-freeze refusals before any protected work, the full-cap remaining-window admission at its exact 900/3540 second boundaries with DST-exact UTC arithmetic, the outer supervisor deadline through publication with process-group descendant cleanup and exclusive no-retry claims, the Stage-0 loader routing, and the encoded parity-receipt branch"
    requirement: EXP-02
    verification:
      - kind: unit
        ref: "tests/phase67/test_isolation.py#RemainingWindowTests.test_exact_now_plus_cap_equality_is_admitted_for_both_caps"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_isolation.py#RemainingWindowTests.test_the_arithmetic_is_dst_exact_across_the_transition"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_isolation.py#GateOrderingTests.test_03_a_late_sunday_without_the_full_allowance_refuses"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_isolation.py#CaptureDeadlineTests.test_a_cap_expired_capture_publishes_nothing_and_stays_incomplete"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_isolation.py#CaptureDeadlineTests.test_the_outer_supervisor_owns_the_worker_process_group"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_isolation.py#LaunchGateTests.test_02_an_mps_registration_refuses_when_mps_is_unavailable"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_isolation.py#GateOrderingTests.test_06_a_good_capture_records_the_remaining_window_evidence"
        status: pass
    human_judgment: false

duration: 104 min
completed: 2026-11-02
status: complete
---

# Phase 67 Plan 06: Design & Settings Ladders — Execution & Page Commands Summary

**The thirteen Phase 67 CLI commands (design, gated metadata capture, exact matrices, single-row launches, cost-only budget, review with conditional owner authority, audit) plus the real-operation gates every command admits through: the DST-exact full-cap remaining-window admission, a process-group-owning outer supervisor whose cap covers every overhead, and the encoded parity-receipt branch — all proven on synthetic data with no real launch.**

## Performance

- **Duration:** 104 min across two executor sessions (22:02–23:46 UTC, 2026-11-02; resumed mid-task-2 after a usage-limit interruption)
- **Started:** 2026-11-02T22:02:05Z
- **Completed:** 2026-11-02T23:46:00Z
- **Tasks:** 2 of 2
- **Files:** 4 created, 7 modified

## Accomplishments

- All thirteen commands run end to end on one temporary fixture repository through the established CLI entry point: `prepare-design` freezes the complete scientific design (suspect predictions, variants, repeat cases, contrasts, cadence formula, budget arithmetic, no-continuation policy and 67-05's reading branches), `capture-metadata` performs the registered gated metadata-only capture for both panel systems, `register-timing`/`budget` write the exact case-major matrices and registrations (15/15/18/12 rows per experiment at full arm order; the fixture-scale arm table proves the exact Cartesian product), `launch-row` launches exactly one row, `review` writes the result page with every E/tier/layer/checkpoint value and matched contrasts, and `audit-phase` audits all four experiments read-only (default marker or pure `--json`).
- The dependency chronology is enforced before any downstream file exists: every dependent command refuses (exit 2, no file) until its prerequisite is committed — the design before the capture, the committed metadata record before the timing registrations, every timing row before the budget, the committed budget before the science matrix, all science rows before the review, and a prior experiment's committed review before any dependent experiment's launch. A pending SCOPE-49 proposal blocks only the dependent experiment, never a universal gate.
- The budget is cost-only and the pages are immutable: `budget` consumes only the committed timing rows' cost fields through 67-04's `phase67_budget`, writes `budget.json`, the budget page, the separate science prediction page and the science registrations, and the timing prediction page stays unchanged — score independence is proven by a test that changes timing scores and asserts the budget, science settings and prediction text cannot move.
- The remaining-window admission (launch_window_contract) exists as a tested power primitive: the Sunday 22:00 America/Chicago closing instant derived from the receipt's own aware weekend instant (wall-clock construction, UTC duration arithmetic), exact now+cap equality admitted and the next representable instant refused for both 900 and 3540 seconds, DST-exact across the fall-back transition, with the closing instant, remaining allowance and gate moment recorded in the capture receipt for independent rechecking.
- Real operations run inside one bounded outer supervisor: the monotonic timer starts before power/admission, the spawned child owns its process group (caffeinate/fit descendants join it), a cap expiry SIGTERMs then SIGKILLs the whole group with no surviving descendant (proven by a ps -g sweep), the attempt stays explicitly incomplete and nothing is published — no erase, resume, rename or retry; the writable-space check against the registered byte bound runs before any claim; battery, weekday, late Sunday, dirty freeze and duplicate-output refusals all land before any protected work exists.
- The encoded (D-05) logger-parity receipt admits as a measurement through the fit admission — the 67-05 recorded adapter item — while half-encoded hybrids, manufactured applicability flags and non-numeric cycles still refuse; check-matrix now settings-validates every row so a registration naming an unavailable mps runtime refuses before any launch; malformed input returns controlled exit 2, never a traceback.

## Task Commits

1. **Task 67-06-01 RED: failing page, matrix and workflow command tests** - `f9bc3ce6` (test) — 9 tests / 13 failures-errors on the missing execution adapter; `RED_EVIDENCE_OK` (target `test_the_execution_adapter_exposes_the_declared_helpers`).
2. **Task 67-06-01 GREEN: the design, matrix, budget and review commands** - `f9552947` (feat) — the 2553-line execution adapter, the page builders and catalog extensions; task verify 31 tests OK.
3. **Task 67-06-02 RED: failing real metadata and launch isolation tests** - `f2f0aa8c` (test) — 18 tests / 21 failures-errors on the missing `require_remaining_window`; `RED_EVIDENCE_OK` (target `test_exact_now_plus_cap_equality_is_admitted_for_both_caps`).
4. **Task 67-06-02 GREEN: the real-operation gates** - `469f6e26` (feat) — the remaining-window admission, the outer supervisor, the disk bound, the receipt evidence, the encoded receipt branch and the check-matrix settings gate; task verify 33 tests OK.

**Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_phase67_execution.py` - created: the thirteen commands, the six schemas, the exclusive writers, the metadata capture and launch bodies, the outer supervisor, the gates and the audit
- `pinn/verification/diagnostic_phase67.py` - the CLI main dispatch (capture/launch supervisor plumbing, controlled exit-2 handler) and the page/review helpers
- `pinn/verification/diagnostic_phase67_catalog.py` - the EXP-05 window-variant materialization support the run matrix resolves
- `pinn/verification/diagnostic_fit.py` - `_receipt_is_a_measurement` admits the encoded receipt shape (null aggregate frequency beside pinned per-harmonic metadata)
- `pinn/verification/diagnostic_power.py` - `weekend_closing_utc` and `require_remaining_window` (the full-cap remaining-window admission)
- `tests/phase67/test_pages.py` - created: the design/page/metadata-registration contract tests
- `tests/phase67/test_workflow.py` - created: the complete synthetic chain, the command refusal contracts, the score-independence and conditional-blocking tests
- `tests/phase67/test_isolation.py` - created: the remaining-window boundaries, the gate ordering, the deadline/supervisor ownership, the launch gates and the encoded receipt tests
- `tests/phase67/test_admission.py`, `tests/phase67/test_catalog.py` - small adjustments to the shared fixtures the new commands admit through
- `tests/phase67/test_historical.py` - the D-12 EDITED_PINS transition set gains `diagnostic_power.py`

## Decisions Made

- The remaining-window admission returns its evidence (cap, closing instant, remaining allowance) rather than a bare pass, so the receipt can record it and any reader rechecks `closing_utc − checked_utc ≥ cap_seconds` from committed bytes alone.
- The supervisor seam is one injected function `supervised(target, args, *, timeout)`; the real implementation appends the queue to the spawned args, and an inline in-process implementation serves every synthetic test — the child re-groups only when actually spawned (`_become_process_group_leader` checks the multiprocessing process name so an inline supervisor never re-groups the host process).
- A synthetic deadline fires the same supervised stop early (6 s) over the real registered 900-second cap, because the spawned child re-admits against the unpatched rule module — the deadline mechanism is value-independent, and the registered-cap propagation is proven separately (launch-row passes its registered cap to the supervisor, asserted at 900.0).
- check-matrix validates row settings through `validate_smoke_settings` in addition to the metadata-only identity door, making "the committed registrations admit" true at settings level — an unavailable-runtime registration refuses at matrix-check time on the machine that would launch it.
- The workflow fixture's `inline_supervisor` and the production `_run_outer_supervised` share one payload contract (`("exited", payload)` / `("timeout", None)`), so every synthetic workflow exercises the same refusal/completion plumbing the real path uses.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The inherited supervisor seam had the wrong signature**
- **Found during:** Task 67-06-02 resume (the interrupted executor's uncommitted GREEN work)
- **Issue:** `_run_outer_supervised(operation, *, timeout)` did not accept the `(target, args, *, timeout)` convention both callers and the `inline_supervisor` fixture use; every real-supervisor call raised TypeError before any work, and the deadline test failed with a missing attempt file.
- **Fix:** Signature `(operation, args=(), *, timeout, ...)` with the queue appended to the spawned args; added `_become_process_group_leader()` so an in-process inline supervisor never re-groups the host process.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py
- **Verification:** CaptureDeadlineTests 2 tests OK; task-2 verify 33 tests OK.
- **Committed in:** 469f6e26

**2. [Rule 3 - Blocking] The committed RED deadline test could not pass at the real cap**
- **Found during:** Task 67-06-02 resume
- **Issue:** The RED test asserts elapsed < 20 s while the registration's metadata cap is the real 900-second rule; no production behavior satisfies both, and shrinking the rule via mock cannot work — the spawned child re-admits the registration against the unpatched rule module and refuses the cap mismatch.
- **Fix:** The deadline test wraps the real supervisor with an early 6-second deadline over the unchanged 900-second registered cap (the same supervised-stop mechanism at fixture scale); the registered-cap propagation is asserted separately in LaunchGateTests.test_01.
- **Files modified:** tests/phase67/test_isolation.py
- **Verification:** CaptureDeadlineTests 2 tests OK.
- **Committed in:** 469f6e26

**3. [Rule 3 - Blocking] The mps gate needed both a real fixture and a production home**
- **Found during:** Task 67-06-02 resume
- **Issue:** The RED test expected check-matrix to refuse when MPS is unavailable, but (a) the fixture's cpu runtime meant no registration named mps, so nothing could refuse, and (b) check-matrix only ran the metadata-only identity door (`check_fit_registration`), which never validates runtime availability.
- **Fix:** The test plants a genuine mps-declaring committed registration and asserts the refusal names MPS; check-matrix now settings-validates every row through `validate_smoke_settings` (the run door's settings half), so an unavailable-runtime registration refuses at matrix-check time.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py, tests/phase67/test_isolation.py
- **Verification:** LaunchGateTests 2 tests OK; the full workflow chain (cpu rows) still passes 31 tests OK.
- **Committed in:** 469f6e26

**4. [Rule 3 - Blocking] The D-12 live-pin transition set gained the edited power gate**
- **Found during:** Task 67-06-02 plan-level verification (phase67 discovery)
- **Issue:** Task 2's `diagnostic_power.py` edit diverged the fourth Phase 66 live pin; the four `test_historical` live-digest assertions failed (run-commit provenance and the live-admission refusal still held).
- **Fix:** Extended `EDITED_PINS` with `pinn/verification/diagnostic_power.py` and its comment, exactly the 67-02 convention. This file is outside task 2's declared list — recorded here rather than silently absorbed.
- **Files modified:** tests/phase67/test_historical.py
- **Verification:** phase67 discovery 233 tests OK.
- **Committed in:** 469f6e26

---

**Total deviations:** 4 auto-fixed (1 bug, 3 blocking)
**Impact on plan:** All four were the minimal changes needed to make the plan's own RED contracts satisfiable and to keep the recorded D-12 transition truthful; no scope creep. The resume itself re-verified the task-2 RED state against the implementation-free tree (HEAD, 18 tests / 21 failures-errors, target failing on the missing `require_remaining_window`) before completing GREEN.

## Issues Encountered

- The prior executor was interrupted by a usage limit mid-task-2; this session inherited three committed gates and an uncommitted partial GREEN diff, reviewed it against the plan's action/acceptance criteria, fixed the supervisor seam and two fixture defects (deviations 1-3), and completed the GREEN.
- phase66 discovery stays at its known D-12 live-pin transition state (99 tests, 6 failures — the four `test_pages` live-digest tests plus the Phase 65 smoke pins on `diagnostic_variants.py`/`diagnostic_similarity.py`); this plan edits no file beyond the already-transitioned set except `diagnostic_power.py`, whose transition is recorded (deviation 4). phase65 discovery is 204 OK and phase67 discovery is 233 OK at final HEAD.
- The `gsd-tools` mutating state/roadmap verbs are not used for the tracking updates (they corrupt this checkout's STATE.md/ROADMAP.md); the hand-edit convention recorded in prior plans' docs commits is followed here too.

## Known Stubs

None - every command, gate and receipt branch is implemented and tested; the `evidence/harness-freeze.json` the registrations pin is supplied by synthetic fixtures in tests and is produced and committed by 67-07 in production, exactly as the plan's artifact table specifies.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 5 is complete, unblocking Wave 6: 67-07 owns the final Phase 65/66/67 compatibility gate and the committed production `evidence/harness-freeze.json` these registrations pin, before any prospective registration or real launch.
- The four experiment plans 67-08..67-15 have concrete, tested commands with exact paths and flags; the EXP-05 lap variants materialize from the committed metadata through the catalog support registered here, and the conditional SCOPE-49/ruling contract is executable end to end on synthetic evidence.
- No real power check, metadata, timing or science run occurred in this plan; the held-out evaluation remains unspent.

## Self-Check: PASSED

All four created files exist on disk; all four production commits (`f9bc3ce6`, `f9552947`, `f2f0aa8c`, `469f6e26`) exist in history with both TDD gate sequences ordered (test → feat per task); both task verify commands re-ran green at final HEAD (31 and 33 tests OK), the Phase 67 discovery is 233 tests OK, phase65 is 204 OK and phase66 shows only its six known D-12 transition failures; `git diff --check` is clean over the plan range `f9bc3ce6^..469f6e26`.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
