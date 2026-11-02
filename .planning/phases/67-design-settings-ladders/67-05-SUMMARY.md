---
phase: 67-design-settings-ladders
plan: "05"
subsystem: testing
tags: [pytorch, unittest, diagnostic-harness, tdd, evidence-reader, contrast-rules, confirmation, staged-validation]

requires:
  - phase: 67-design-settings-ladders (67-01)
    provides: read_phase67_record, the phase67 registry dispatch, the admission door and the tests/phase67 synthetic fixtures this plan extends
  - phase: 67-design-settings-ladders (67-03)
    provides: the window-evidence digest conventions (physical/tau sha256 over the retained grid) the committed window metadata reuses
  - phase: 67-design-settings-ladders (67-04)
    provides: the registered checkpoint schedule every science registration declares and the reader re-derives
provides:
  - read_phase67_run_directory — the registration-bound Phase 67 science reading: staged shape, identity, evidence-link and numeric validation with value-free mechanical/setting problems, the declared matrix row, actual coordinates, layer trace, checkpoint steps, observed fit and the final-quarter unsettled flag
  - phase67_improvement_check — the exact 5 percent final-quarter improvement rule with the zero-reference rule and typed refusals
  - phase67_contrast / phase67_confirmation — the matched-contrast and three-case confirmation rules (direction, exact 20 percent relative effect, tier qualification, zero-control handling, distinct run identities, the five-label branch table, every declared noncontrol contrast persisted)
  - PHASE67_CASES (the D-09 role-to-orbit/seed bindings) and phase67_control_arm (d12, lr1e-4, own-backbone raw, lap10)
affects: [67-06 (command wrappers translating reader problems to exit 2, the encoded receipt branch), 67-07 (prediction/registration pages embedding the window metadata, baseline blocks and matrix rows), 67-08..67-15 (experiment execution and reading), Phase 68 energy adjudication]

actuals:
  tokens: 31400
  tasks: 2
  commits: 5

tech-stack:
  added: []
  patterns:
    - "Staged evidence reading: JSON/object/list/scalar shapes, then identity/settings against the declared matrix row, then evidence links (digests, contained basenames, symlinks before any open), then numeric/scientific fields — a malformed record becomes a value-free problem, never a traceback or a scientific reading"
    - "Committed metadata is the expectation source: the registration's window_metadata/window_baselines blocks (the 67-03 evidence shape) bind the grid digests, endpoint, sample count and same-window baselines the record must reproduce"
    - "One implementation per registered threshold: the reader's unsettled flag delegates to phase67_improvement_check, and the contrast derives everything else from the frozen scorecard tiers it is handed"

key-files:
  created:
    - tests/phase67/test_records.py
    - tests/phase67/test_reading_rule.py
  modified:
    - pinn/verification/diagnostic_phase67_records.py
    - pinn/verification/diagnostic_phase67.py
    - tests/phase65/test_fit_short.py

key-decisions:
  - "The science reading requires the registered checkpoint schedule and the committed window metadata and baseline blocks: a registration without either is a typed refusal before any run evidence is read. The metadata block shape (first/last time, sample count, both sha256 digests; constant E and two-Kepler applicability-or-failure) is this plan's contract for 67-07's pages, mirroring the 67-03 same_window_expectations evidence."
  - "The Sunday 22:00 closing instant is derived from the receipt's own aware window instant (Saturday derives the next day's 22:00, Sunday the same day's, wall-clock so DST is exact), and the registered whole-launch cap must fit the remaining allowance — exact equality admits and the next representable instant does not, as 67-06 specifies."
  - "An unsafe weight reference (non-basename, absolute, parent-relative, resolving outside the run directory, or a symlink) both records its own problem and skips the fit verifier entirely, so nothing outside the run directory is ever opened through a record-supplied path (T-67-13)."
  - "The matrix row is caller-declared (experiment/arm/case/orbit/seed) and mismatches become setting problems; the D-09 role-to-orbit/seed binding and the registered control arm are enforced in phase67_contrast, where the three cases meet — wrong-control and duplicate-identity refusals live there and are tested in test_reading_rule."
  - "The qualification rule is the plan's OR: a nonzero E direction qualifies through a matching tier change OR a relative E effect of at least twenty percent (exact 20 percent qualifies; an opposing tier change cannot veto the effect side). A zero control E retains the direction and flags the percentage inapplicable — only a matching tier change can then qualify, never a division by zero."
  - "The encoded (D-05) clean reading is proven on a real registered encoded run through a patched census seam (a fixture panels row for the synthetic orbit whose N_in pins the declaration's frequency), because the real encoded logger-parity receipt branch is 67-06's adapter work; the window (EXP-05) grid/baseline path is proven on the fixture's own grid, with the lap-arm names binding now and the lap registrations arriving with their plans."

patterns-established:
  - "Registration-committed expectations: run evidence is validated against metadata committed before the run, never against values the record supplies about itself"
  - "Per-entry grid binding: every similarity entry's coordinates must reproduce the committed digests, so one tampered entry cannot borrow another's grid"

requirements-completed: []  # EXP-02..05 are declared here but the experiments run in 67-08..67-15; the marks flip at the phase verification act (shared-ID gate: siblings also declare them), matching the 67-01..04 convention.

coverage:
  - id: D1
    description: "The registration-bound Phase 67 science reader: staged shape/identity/evidence/numeric validation, raw and encoded clean readings at real depths, grid and baseline binding, access and receipt/attempt audits with the Sunday 22:00 cap boundary, matrix-row setting problems, and scores only after a clean audit"
    requirement: EXP-02
    verification:
      - kind: integration
        ref: "tests/phase67/test_records.py#CleanReadingTests.test_a_clean_raw_run_reads_clean_with_the_full_reading_shape"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_records.py#EncodedReadingTests.test_an_encoded_run_reads_clean_at_every_registered_layer"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_records.py#ReceiptAndAttemptTests.test_the_cap_fits_the_sunday_closing_exactly_and_not_one_instant_later"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_records.py#HostileRecordShapeTests.test_unsafe_and_symlinked_weight_references_refuse"
        status: pass
    human_judgment: false
  - id: D2
    description: "The prospective contrast and confirmation rules: the exact 5 percent improvement boundary, the matched control arms, direction and exact 20 percent effect with tier qualification, zero-control handling, the three-case confirmation table (a favourable main run alone can never confirm), distinct run identities, and the experiment-level confirmation persisting every declared noncontrol contrast"
    requirement: EXP-02
    verification:
      - kind: unit
        ref: "tests/phase67/test_reading_rule.py#ContrastTests.test_an_exact_twenty_percent_effect_confirms_improvement"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_reading_rule.py#ImprovementTests.test_exact_five_percent_is_settled_and_the_next_instant_is_not"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_reading_rule.py#ContrastTests.test_one_unsettled_endpoint_blocks_confirmation"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_reading_rule.py#ConfirmationTests.test_every_declared_noncontrol_contrast_is_persisted"
        status: pass
    human_judgment: false

duration: 37 min
completed: 2026-11-02
status: complete
---

# Phase 67 Plan 05: Design & Settings Ladders — Evidence Reader & Reading Rules Summary

**A registration-bound science reader that turns every malformed or tampered Phase 67 run directory into value-free mechanical/setting problems (staged shape, matrix-row, digest, path, receipt, attempt and Sunday-22:00-cap audits; scores only after a clean audit), plus the prospective improvement, matched-contrast and three-case confirmation rules pinned at their exact 5 and 20 percent boundaries before any prediction page or real run exists.**

## Performance

- **Duration:** 37 min (20:15–20:52 UTC, 2026-11-02)
- **Started:** 2026-11-02T20:15:14Z
- **Completed:** 2026-11-02T20:52:00Z
- **Tasks:** 2 of 2
- **Files modified:** 5 (2 harness modules, 2 new test modules, 1 phase65 fixture helper)

## Accomplishments

- `read_phase67_run_directory` reads one Phase 67 run directory against its committed registration, registered checkpoint schedule, committed window metadata and same-window baselines, and declared matrix row: raw and encoded inputs at real depths read clean with exact identities, layer rows exactly once in order, finite cosines in [-1, 1], output movement and rate, strictly increasing actual physical/raw-tau coordinates that must reproduce the committed grid digests, endpoint and sample count, raw frequency evidence or the registered encoded nonapplicability and feature metadata, frozen E/tier/eps_h consistency of the endpoint and every checkpoint through the frozen scorecard, TRAIN-only access evidence (absent never stands for zero), contained weight basenames with symlink checks before anything is opened, the aware receipt (weekday derived from its own instant, AC first line) and the published attempt (digest, cap, completed steps, checked-before-start-before-end, launch wall inside the cap), and the derived Sunday 22:00 closing instant that the registered cap must fit exactly at the boundary.
- `phase67_improvement_check` implements the final-quarter rule exactly: `(E_at_3N/4 − E_at_N)/E_at_3N/4` strictly greater than five percent is unsettled, exactly five percent is settled, a zero reference is settled either way, and negative, non-finite, boolean or string E, wrong counts or non-increasing steps refuse.
- `phase67_contrast` runs one declared arm against its registered control (`d12`, `lr1e-4`, its own backbone's raw input, or `lap10`) on exactly the three D-09 cases: exact E direction (equal is a tie), the relative effect `abs(E_arm − E_control)/E_control` at the exact twenty-percent line (a zero control retains direction and flags the percentage inapplicable), tier qualification through the frozen scorecard ordering, per-case endpoint statuses and observed fits retained separately, and the deterministic confirmation table — all three cases qualifying in one direction with all six endpoints settled and clean confirms improvement or worsening; problematic endpoints are inconclusive-mechanical; unsettled endpoints block confirmation; ties, small effects and opposed directions are ambiguous with reasons. Duplicate run identities refuse (an interrupted or duplicate attempt never counts as an additional replicate), and every reading's orbit, seed, experiment and arm must match its registered case and control.
- `phase67_confirmation` persists every declared noncontrol contrast of an experiment (missing, duplicate, undeclared and control-arm contrasts refuse) with its nonconfirmation reasons, separating confirmed effects from ambiguous, unsettled and mechanically inconclusive ones — T-67-15's repudiation answer — while adjacent-time hidden-state similarity stays descriptive (no cosine threshold, no causal claim), loss stays context and GAP-59-08 stays explicit.
- Both TDD gates were machine-verified `RED_EVIDENCE_OK` (task 1: 24 tests, 87 errors on the missing reader; task 2: 21 tests, 21 errors on the missing contrast), and the reader's `unsettled` flag now delegates to the one canonical improvement implementation.

## Task Commits

1. **Task 67-05-01 RED: failing reader contract tests** - `36ba5210` (test) — 24 tests over hostile roots, nested blocks, numeric shapes, grid/baseline substitutions, unsafe paths, receipts, attempts and the Sunday boundary; `RED_EVIDENCE_OK` (target `test_a_clean_raw_run_reads_clean_with_the_full_reading_shape`).
2. **Task 67-05-01 GREEN: the science run reader** - `3e125e8b` (feat) — `read_phase67_run_directory` with the staged validation order; 24 tests OK.
3. **Task 67-05-02 RED: failing contrast and confirmation tests** - `05d5063a` (test) — 21 tests over the improvement boundary, controls, the effect line, the confirmation table and the experiment rollup; `RED_EVIDENCE_OK` (target `test_an_exact_twenty_percent_effect_confirms_improvement`).
4. **Task 67-05-02 GREEN: the reading rules** - `d8974f73` (feat) — the improvement check, contrast, confirmation and control-arm resolver, plus the reader's unsettled wiring to the canonical rule; 45 tests OK across both modules.

**Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_phase67_records.py` - `read_phase67_run_directory` with the staged problem surface, the committed window-metadata/baseline gate, per-entry grid binding, encoded feature-metadata validation, receipt/attempt/cap audits and the matrix-row setting problems; `read_phase67_record` (67-01) unchanged in behavior
- `pinn/verification/diagnostic_phase67.py` - `PHASE67_CASES`, `PHASE67_IMPROVEMENT_RULE`, `PHASE67_EFFECT_RULE`, `CONFIRMATION_LABELS`, the GAP/similarity notes, `phase67_control_arm`, `phase67_improvement_check`, `phase67_contrast`, `phase67_confirmation`
- `tests/phase67/test_records.py` - one real registered 100-step schedule run per class (raw and encoded through a patched census seam), the hostile-evidence matrix and the improvement-field boundary tests (24 tests)
- `tests/phase67/test_reading_rule.py` - the pure rule suites over synthetic readings (21 tests)
- `tests/phase65/test_fit_short.py` - the fixture registration builder's optional `doc_extra` merge for committed metadata blocks (backward compatible)

## Decisions Made

- The science reading's hard requirements (registered schedule; committed window metadata and baselines) are typed refusals at admission, so 67-07's pages must carry the metadata blocks this plan defines; a malformed record after admission is always a problem list, never a refusal, so 67-06's wrappers can translate every evidence defect to exit 2.
- Task 1's "wrong control" acceptance item is satisfied at the contrast layer (task 2): the reader validates the run against its declared row, and `phase67_contrast` refuses a control reading whose arm is not the registered control of the contrasted arm (`wrong_control` and the exp04 cross-backbone cases in `test_reading_rule`).
- The exact-boundary fixtures use dyadic values (20→19 for exactly five percent; 5→4 for exactly twenty percent) so the boundary comparisons are exact float64 arithmetic, and the nextafter neighbours prove strictness in both directions.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] The fixture registration builder gained a `doc_extra` parameter**
- **Found during:** Task 67-05-01 RED
- **Issue:** The reader requires registrations that commit window metadata and baseline blocks, but `_fit_registration_fixture` could not express any additional top-level block, so no test registration could carry them.
- **Fix:** Added an optional `doc_extra=None` parameter merged into the registration document before serialization; every earlier caller's document is unchanged (the parameter defaults to no merge).
- **Files modified:** tests/phase65/test_fit_short.py
- **Verification:** phase65 discovery 204 tests OK; phase67 discovery 184 OK.
- **Committed in:** 36ba5210

**2. [Rule 1 - Bug] Test-authoring corrections during GREEN**
- **Found during:** Task 67-05-01 GREEN
- **Issue:** Five RED-test defects surfaced once the reader existed: the raw-roots cases wrote hostile bytes to the receipt instead of the record; the nested-block case table derived its expected problem from the case name and misfiled three entries; the grid tamper broke coordinate monotonicity (exercising the coordinates problem instead of the digest); the symlink fixture unlinked a file that never existed; and the exact-boundary arithmetic was not dyadic (0.95 and 19/20 do not land exactly on the thresholds).
- **Fix:** Added a `record_bytes` parameter, made the case table carry its problem explicitly, moved the grid tampers to in-place perturbations that preserve ordering, created the symlink directly, and switched to 20→19 and 5→4 boundaries with nextafter neighbours.
- **Files modified:** tests/phase67/test_records.py, tests/phase67/test_reading_rule.py
- **Verification:** test_records 24 OK; test_reading_rule 21 OK.
- **Committed in:** 3e125e8b, d8974f73

**3. [Rule 3 - Blocking] The reader's improvement flag was wired to the canonical rule in task 2**
- **Issue:** Task 1's reader computed `unsettled` with a private copy of the five-percent rule so the reading contract was complete from task 1, but the plan's file lists put `phase67_improvement_check` in task 2 — leaving two implementations of the registered threshold at plan end.
- **Fix:** Task 2's GREEN replaced the private copy with a delegation to `phase67_improvement_check` (a two-line change to `diagnostic_phase67_records.py`, outside task 2's declared file list), so one implementation owns the boundary.
- **Files modified:** pinn/verification/diagnostic_phase67_records.py
- **Verification:** the task 2 verify command (both modules) re-ran green — test_records' improvement-boundary tests pin the delegated behavior at 45 tests OK.
- **Committed in:** d8974f73

---

**Total deviations:** 3 auto-fixed (1 bug, 2 blocking)
**Impact on plan:** All three were the minimal changes needed to express and then unify the plan's own contracts; no scope creep. The file-list extension in deviation 3 is recorded here rather than silently absorbed.

## Issues Encountered

- phase66 discovery stays at its known D-12 live-pin transition state (99 tests, 6 failures — the four `test_pages` live-digest tests plus the Phase 65 smoke pins on `diagnostic_variants.py`/`diagnostic_similarity.py`): this plan edits no file pinned by a Phase 66 registration, so the set is unchanged and still routed to 67-06 per the 67-01 convention. phase65 discovery is 204 OK and phase67 discovery is 184 OK at final HEAD.
- A real registered encoded run required patching the census panels seam for the synthetic orbit (the encoded declaration pins system 1632's frequency and the fixture orbit is id 0); this mirrors the established data-seam patching style and is the same census-agreement check the real door performs. The real encoded logger-parity receipt branch remains 67-06's adapter work, exactly as 67-02 recorded.

## Known Stubs

None - the reader and all three rule functions are fully implemented and tested; the EXP-05 lap-arm name binding is a registered rule constant whose variant declarations arrive with the window registration plans, and no placeholder value or unwired path was introduced.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 4 is complete, unblocking Wave 5 (67-06 compatibility work). The wrappers can translate every reader problem to exit 2, and the encoded parity-receipt branch is the remaining adapter item 67-06 already owns.
- 67-07's prediction and registration pages must embed the `window_metadata`/`window_baselines` blocks and per-run matrix rows this reader validates, and can cite `PHASE67_CASES`/`phase67_control_arm` as the single control-resolution source.
- No real corpus read, timing or training ran in this plan; the held-out evaluation remains unspent.

## Self-Check: PASSED

Both created test files exist on disk; all four production commits (`36ba5210`, `3e125e8b`, `05d5063a`, `d8974f73`) exist in history with both TDD gate sequences ordered (test → feat per task); both task verify commands re-ran green at final HEAD (24 and 45 tests OK), the Phase 67 discovery is 184 tests OK, phase65 is 204 OK and phase66 shows only its six known D-12 transition failures; `git diff --check` is clean over the plan range `36ba5210^..HEAD`.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
