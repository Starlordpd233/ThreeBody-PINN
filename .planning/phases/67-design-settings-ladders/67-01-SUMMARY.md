---
phase: 67-design-settings-ladders
plan: "01"
subsystem: testing
tags: [pytorch, unittest, siren, diagnostic-harness, tdd, registry-dispatch]

requires:
  - phase: 66-small-network-control
    provides: the INST-08 fit harness, the AC/weekend launcher and the committed-registration door this plan extends
provides:
  - The phase67 variant registry with the EXP-02 raw-depth-2 declaration exp02-d2-w256-o30 (D-03) and its settings-side dispatch
  - read_phase67_record, the registration-bound Phase 67 run reader (value-free problems, scores only on a clean audit)
  - Typed phase67 window-endpoint admission (finite numbers excluding booleans, start exactly zero)
  - The tests/phase67 synthetic fixture contracts (_fixtures.py) reused by plans 67-02..67-16
affects: [67-02..67-16 expansion plans, 67-06 compatibility work, Phase 68 energy adjudication]

actuals:
  tokens: 16289
  tasks: 2
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Separate per-phase registry dispatch: the fit harness checks the frozen phase66 table first, then falls through to the phase67 catalog's phase67_registry — a historical catalog is never edited to admit new variants (D-12)"
    - "Reader reuses the launcher's own window/receipt constants, so gate and auditor cannot drift (66-REVIEW IN-02 applied to the new path)"
    - "Malformed run evidence becomes a value-free mechanical problem, never a traceback (66-REVIEW CR-02's accepted limitation, not inherited)"

key-files:
  created:
    - pinn/verification/diagnostic_phase67_catalog.py
    - pinn/verification/diagnostic_phase67_records.py
    - tests/phase67/__init__.py
    - tests/phase67/_fixtures.py
    - tests/phase67/test_tracer.py
    - tests/phase67/test_admission.py
    - tests/phase67/test_historical.py
  modified:
    - pinn/verification/diagnostic_fit.py

key-decisions:
  - "The phase67 registry dispatch lives in a new declaration-only catalog module (phase67_registry raises VariantRefused for unknown names; _named_registry wraps it as DiagnosticFitRefused), so diagnostic_phase66.py stays byte-identical and its digest-pinned registrations keep their recorded bytes."
  - "read_phase67_record reuses verify_fit_result as its record audit and adds only what that verifier does not read (receipt, attempt, layer rows, tier consistency, split opens); a receipt's weekend weekday is derived from its own local_time, not its self-declared isoweekday."
  - "setting_problems is returned empty on clean raw-path readings and reserved for the experiment-specific reading rules of later plans (67-05 and beyond); no scientific branch table lives in this reader."
  - "The phase67 window-endpoint strictness is scoped to settings naming the phase67 registry; Phase 65/66 registrations keep their existing check byte-for-byte (65-CLOSEOUT IN-01 applied as affected-use hardening, D-13)."
  - "The four Phase 66 live-digest failures in tests/phase66/test_pages.py are the planned D-12 transition (the edited diagnostic_fit.py retires live admission of the Phase 66 registrations) and are reported for the narrowly scoped compatibility work in 67-06, per this plan's task instruction; the run-commit identity assertions are retained in tests/phase67/test_historical.py."

patterns-established:
  - "Per-phase catalog module: declarations only, no harness imports, fresh register_variant copy, AST-checked import direction"
  - "Registration-bound reading: expectations derived from the registration, never from the record; scores gated behind a clean audit"

requirements-completed: []  # EXP-02..05 are the experiment requirements; the experiments run in plans 67-08..67-15 and the marks flip at the phase verification act, never by this tracer plan (shared-ID gate confirms 0/4 ready).

coverage:
  - id: D1
    description: "One synthetic registered Phase 67 raw-depth-2 fit end to end: committed admission, AC/weekend launch, constant-rate Adam, every-layer logging (input + h1 + h2), frozen scoring, exclusive marked publication, and a clean registration-bound reader reading"
    requirement: EXP-02
    verification:
      - kind: integration
        ref: "tests/phase67/test_tracer.py#Phase67TracerTests.test_the_ac_case_runs_one_synthetic_phase67_run_end_to_end"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_tracer.py#Phase67TracerTests.test_the_battery_case_refuses_before_anything_is_created"
        status: pass
    human_judgment: false
  - id: D2
    description: "The Phase 67 admission boundary: typed window endpoints, seed/cap/cadence/variant/registry refusals, catalog immutability and duplicate-name refusal, deterministic layer order, locked raw production parity, and non-TRAIN orbits refusing before any corpus open or optimizer construction"
    requirement: EXP-02
    verification:
      - kind: unit
        ref: "tests/phase67/test_admission.py#Phase67AdmissionTests.test_phase67_window_endpoints_are_typed_and_exact"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_admission.py#Phase67NonTrainBoundaryTests.test_a_non_train_orbit_refuses_before_any_corpus_open"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_admission.py#Phase67CatalogControlTests"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_admission.py#LockedRawParityTests.test_locked_raw_construction_is_bitwise_production"
        status: pass
    human_judgment: false
  - id: D3
    description: "Historical evidence preservation: the six unedited Phase 66 code pins byte-identical live, every Phase 66 run's registration/dependency identity holding at its recorded run commit, live new-run admission correctly refusing on the changed diagnostic_fit.py, and the 11 Phase 65 preserved evidence hashes unchanged"
    verification:
      - kind: integration
        ref: "tests/phase67/test_historical.py#HistoricalPhase66Tests"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_historical.py#PreservedPhase65EvidenceTests.test_phase65_evidence_hashes_are_unchanged"
        status: pass
      - kind: unit
        ref: "command:pinn-train python -B -c 'from pinn.verification.learnability_protocol import load_protocol; load_protocol(); print(PROTOCOL-OK)'"
        status: pass
    human_judgment: false
---

# Phase 67 Plan 01: Design & Settings Ladders Tracer Summary

**A registered synthetic raw-depth-2 Phase 67 fit (exp02-d2-w256-o30) traverses committed admission, the AC/weekend launcher, constant Adam, every-layer logging, frozen scoring, exclusive publication and the new registration-bound reader — with the admission, catalog and historical-evidence boundaries proven before any protected operation.**

## Performance

- **Duration:** 30 min (04:54–05:25 UTC, 2026-11-02)
- **Started:** 2026-11-02T04:54:33Z
- **Completed:** 2026-11-02T05:24:28Z
- **Tasks:** 2 of 2
- **Files modified:** 8 (2 new diagnostic modules, 1 harness edit, 5 new/1 rewritten test files)

## Accomplishments

- The Phase 67 registry exists as a fresh immutable `register_variant` copy (`locked-12`, then `exp02-d2-w256-o30` at 137,737 parameters vs the locked 795,657) with `phase67_registry(settings)` dispatch, and `diagnostic_fit._named_registry` resolves it without touching the frozen Phase 66 catalog — both sealed catalogs are pinned unchanged by tests.
- The tracer proved the complete registered path on synthetic data: committed CPU64 fixture registration → AC/weekend launch through the existing gate → 20-step constant-rate Adam fit with stride-3 loss trace → input/h1/h2 rows in every similarity entry → frozen scorer with both comparison rows and access attestation → intrinsically marked exclusive weights and record → `verify_fit_result` acceptance → a clean `read_phase67_record` reading whose scores appear only on request.
- `read_phase67_record` audits a run directory against its committed registration: value-free mechanical problems over the fit audit, the receipt (weekday derived from its own local time), the published attempt digest, every-layer rows, split opens and tier consistency — malformed evidence becomes a problem, never a traceback.
- Phase 67 window endpoints are now typed at admission (finite numbers excluding booleans, start exactly zero) while Phase 65/66 settings keep their byte-identical check; non-TRAIN orbits still refuse at the real Stage-0 seam before any corpus open.
- Phase 66's historical evidence is intact: its six unedited pins are byte-identical live, every run's identity holds at its recorded run commit, and live admission correctly refuses on the changed `diagnostic_fit.py` — the D-12 separation of historical provenance from run permission.

## Task Commits

1. **Task 67-01-01 RED: failing Phase 67 tracer** - `e0f06523` (test) — the registration refuses at the registry door (`unknown variant registry 'phase67'`), machine-verified `RED_EVIDENCE_OK` (target `test_the_ac_case_runs_one_synthetic_phase67_run_end_to_end`, 2 tests / 1 fail).
2. **Task 67-01-01 GREEN: catalog, dispatch, reader** - `8e2f4110` (feat) — `diagnostic_phase67_catalog.py`, `diagnostic_phase67_records.py`, the `_named_registry` dispatch; tracer 2 tests OK; tracer feedback gate re-verified end-to-end before expansion.
3. **Task 67-01-02 RED: admission and historical tests** - `086f7e3d` (test) — boundary battery plus `_fixtures.py` extraction; `RED_EVIDENCE_OK` (target `test_phase67_window_endpoints_are_typed_and_exact`).
4. **Task 67-01-02 RED correction** - `97f9ecde` (test) — the window/seed/cap/drift cases retargeted onto the phase67 door; RED re-verified against the implementation-free tree.
5. **Task 67-01-02 GREEN: typed window endpoints** - `b6e54c4d` (feat) — the phase67 branch of `validate_smoke_settings`.
6. **Non-TRAIN boundary coverage** - `7ea514fb` (test) — the withheld test-split key refuses through the real seam with zero reference loads and zero optimizer steps.

**Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_phase67_catalog.py` - EXP02_D2_VARIANT (D-03 declaration), PHASE67_REGISTRY, phase67_registry; imports declarations only
- `pinn/verification/diagnostic_phase67_records.py` - read_phase67_record, registered_layers, Phase67RecordRefused; reuses the launcher's constants
- `pinn/verification/diagnostic_fit.py` - phase67 registry dispatch in `_named_registry`; typed phase67 window endpoints in `validate_smoke_settings` (+42/-9 total)
- `tests/phase67/__init__.py`, `tests/phase67/_fixtures.py` - the package marker and shared synthetic seam (plain functions only)
- `tests/phase67/test_tracer.py` - the end-to-end tracer and battery control
- `tests/phase67/test_admission.py` - admission boundary, catalog controls, locked parity, non-TRAIN seam refusal
- `tests/phase67/test_historical.py` - Phase 66 run-commit identity, live refusal, Phase 65 preserved hashes

## Decisions Made

- The `setting_problems` list is returned empty on clean raw-path readings and reserved for the experiment-specific reading rules of later plans; this plan's reader deliberately owns no scientific branch table (D-13).
- The four Phase 66 `test_pages` live-digest failures are reported for 67-06 rather than edited here, exactly as the plan's task instruction directs; the run-commit assertions are retained (in `test_historical.py`) so historical provenance stays independently verifiable.
- Depth-2 parameter count pinned at 137,737 (CPU float64 seed-42 build) for the size record D-03 asks the report to state.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] RED-phase test defects corrected before GREEN**
- **Found during:** Task 67-01-02 RED
- **Issue:** Two test-authoring defects: (a) the window/seed/cap/drift refusal cases merged into the base Phase 65 settings, so they exercised the wrong door; (b) the pre-existing-attempt control asserted the CLI would mark a foreign claim incomplete, but the established Phase 65 contract deliberately refuses without touching another worker's running claim.
- **Fix:** Retargeted the cases through `phase67_settings(...)` (full Phase 67 settings), asserted the foreign claim is left untouched, discarded the premature implementation edit, and re-verified RED against the implementation-free tree (`RED_EVIDENCE_OK` again) before re-applying GREEN.
- **Files modified:** tests/phase67/test_admission.py
- **Verification:** corrected RED run 25 tests / 20 pass / 5 fail on the target; GREEN 25 (then 26) tests OK.
- **Committed in:** 97f9ecde

**2. [Rule 2 - Missing critical] Non-TRAIN boundary coverage added post-GREEN**
- **Found during:** Task 67-01-02 acceptance-criteria verification
- **Issue:** The must-have truth "non-TRAIN registrations refuse before a corpus open or optimizer construction" had no direct Phase 67-path test (the Stage-0 seam is Phase 65 code proven by its own suite, but the phase67 path through the CLI was unproven).
- **Fix:** Added `Phase67NonTrainBoundaryTests` driving a registration naming the withheld test-split key through the real orbit-spec/Stage-0/reference-loader seam: exit 2, zero reference loads, zero optimizer steps, attempt incomplete.
- **Files modified:** tests/phase67/test_admission.py
- **Verification:** 26 tests OK on the task verify command.
- **Committed in:** 7ea514fb

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical coverage)
**Impact on plan:** Both fixes tightened the plan's own acceptance criteria; no scope creep.

## Issues Encountered

- The four `tests/phase66/test_pages.py` live-digest tests now fail by design: this plan's mandated `diagnostic_fit.py` edit retires live admission of the Phase 66 registrations (D-12). Recorded here and routed to 67-06 per the plan's explicit instruction; phase66 discovery otherwise passes (99 tests, 4 failures, all this known transition). The last live passes were at `734cb7da` (recorded in `66-02-SUMMARY.md`).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The Phase 67 slice is runnable and tested through its reader on synthetic data; plans 67-02 onward (catalog/time features, windows, budgets, records) extend the registry and reader established here, reusing `tests/phase67/_fixtures.py`.
- The 67-06 compatibility work should convert the four Phase 66 live-pin assertions to run-commit anchors (mirroring `tests/phase67/test_historical.py`) so the phase66 discovery returns to green.
- No real metadata, timing or science run occurred in this plan; the held-out evaluation remains unspent.

## Self-Check: PASSED

All 7 created files exist on disk; all 6 production commits (`e0f06523`, `8e2f4110`, `086f7e3d`, `97f9ecde`, `b6e54c4d`, `7ea514fb`) exist in history; both task verify commands and the Phase 67 discovery (26 tests OK) re-run green at final HEAD; `git diff --check` clean over the plan range.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
