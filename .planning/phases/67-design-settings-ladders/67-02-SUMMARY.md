---
phase: 67-design-settings-ladders
plan: "02"
subsystem: testing
tags: [pytorch, unittest, siren, diagnostic-harness, tdd, fourier-features, catalog, census-metadata]

requires:
  - phase: 66-small-network-control
    provides: the EXP-01 backbone settings (depth 1, width 384, first omega 1000) and the frozen harness whose paths this plan extends
  - phase: 67-design-settings-ladders (67-01)
    provides: the phase67 registry dispatch, the exp02-d2 declaration, the registration-bound reader and the tests/phase67 synthetic fixtures
provides:
  - The exact 17-name Phase 67 ladder registry (D-03 depth arms d2/d4/d6/d8/d12, D-04 rate arms lr1e-3..lr1e-5, D-05 input arms locked/exp01 x raw/f1/f12) with deterministic parameter counts and the PHASE67_ARMS + phase67_variant arm resolver
  - DiagnosticTimeFeatures / DiagnosticTimeFeatureNetwork — the internal differentiable Fourier encoder (public raw14 contract, 14/16/18 internal dimensions, persistent frequency/harmonics buffers, inherited COM forward) and the tau_ic13_fourier1 / tau_ic13_fourier12 declarations
  - Census-bound encoded frequency resolution: f = N_in/10 from the committed Phase 59 row, with phase67_registry rejecting an orbit that disagrees with the encoded declaration it names (T-67-04)
  - The truthful shared logger: encoded measurements carry frequency_applicability/reason, pinned feature frequencies, harmonics and internal dimension with null aggregate bandwidth; strict raw-tau monotonicity before any hook (WR-06); raw JSON byte-shape preserved
affects: [67-03..67-16 (windows, budgets, execution adapter, experiments), 67-06 compatibility work, Phase 68 energy adjudication]

actuals:
  tokens: 25094
  tasks: 2
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Feature-only constructor dispatch: build_variant routes encoded declarations to the diagnostic subclass while the raw branch stays byte-identical production construction (D-12 lock)"
    - "Registered metadata is the only frequency source: encoded variants pin f = N_in/10 from the committed census row, and the registry dispatch re-resolves it from the settings' orbit, refusing disagreement"
    - "Applicability-labelled diagnostics: an aggregate that does not describe the complete encoded input is emitted null with an explicit reason plus the registered per-harmonic metadata, never a misleading number"

key-files:
  created:
    - pinn/verification/diagnostic_time_features.py
    - tests/phase67/test_time_features.py
    - tests/phase67/test_catalog.py
  modified:
    - pinn/verification/diagnostic_variants.py
    - pinn/verification/diagnostic_phase67_catalog.py
    - pinn/verification/diagnostic_similarity.py
    - tests/phase67/test_admission.py
    - tests/phase67/test_historical.py

key-decisions:
  - "The encoded exp04 arms pin the MAIN comparison system's census row (1632, N_in = 10.471994061054543, f = N_in/T = 1.0471994061054543 cycles per physical time unit) per D-09; repeat-system (851) variants are materialized later as fresh orbit-specific registrations through register_variant, never by editing a declaration — which is exactly what phase67_registry's census-agreement check enforces."
  - "The encoder owns the unit conversion once: the phase coefficient is pi * (f * T) per harmonic, realized as tensor math from the persistent frequency_cycles buffer, so pi*N_in*(tau+1) and 2*pi*f*t are the same construction; malformed raw14 widths, boolean/nonfinite/nonpositive frequencies and non-ascending harmonics refuse before any tensor is built."
  - "The shared measurement detects an encoded model through its encoder attribute (isinstance DiagnosticTimeFeatures), keeps the raw path's fields byte-shape (proven against a committed Phase 66 record's similarity entries) and adds the five encoded metadata fields only on encoded models — diagnostic_fit._receipt_is_a_measurement still requires finite median/max numbers, so the encoded parity-receipt branch belongs to 67-06's adapter work."
  - "The phase67 historical suite's EDITED_PINS transition set was extended (diagnostic_variants.py, diagnostic_similarity.py now live-diverge from the Phase 66/65 recorded pins by design) and the admission suite's registry-order pin now anchors the head and tail of the 17-name order; the run-commit-anchored identity assertions are unchanged. The frozen tests/phase66 suite was left untouched per the 67-01 convention: its live-pin failures (now 6) are the planned D-12 transition routed to 67-06."

patterns-established:
  - "Per-arm declaration tables: PHASE67_ARMS maps experiment -> arm id -> declaration, so execution plans expand their case-major products from one source of truth"
  - "Applicability fields over silent reinterpretation: a diagnostic that changes meaning under an intervention is labelled inapplicable with a reason and replaced by the registered metadata"

requirements-completed: []  # EXP-02..04 are declared here but the experiments run in 67-08..67-15; the requirement marks flip at the phase verification act, per the phase convention (shared-ID gate: siblings 67-08..67-13 also declare them).

coverage:
  - id: D1
    description: "The exact declared ladders and their construction: the 17-name registration order, every D-03 depth field and D-04 rate, the six D-05 arms on the two actual backbones, deterministic parameter counts, the arm resolver, census-pinned frequencies, census-orbit agreement/refusal, and bitwise raw production parity with global-RNG preservation"
    requirement: EXP-02
    verification:
      - kind: unit
        ref: "tests/phase67/test_catalog.py#Phase67LadderCatalogTests.test_the_phase67_registry_holds_the_exact_declared_ladders_in_order"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_catalog.py#Phase67LadderCatalogTests.test_parameter_counts_are_exact_and_deterministic"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_catalog.py#Phase67FrequencyResolutionTests.test_an_encoded_declaration_refuses_a_disagreeing_orbit"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_catalog.py#RawParityAndRNGTests.test_the_raw_locked_arms_build_the_production_class_bitwise"
        status: pass
    human_judgment: false
  - id: D2
    description: "The internal Fourier time-feature models (D-05): public raw14 contract with COM projection, 14/16/18 internal dimensions, ordered harmonic pairs after raw tau and IC13, the pi*N_in*(tau+1) phase identity, analytic first and second raw-tau derivatives, persistent buffers surviving state_dict round-trips, fan-in bound 1/internal_dim, seeded determinism without shared mutable state, and the frozen scorer's vmap(jacrev) AD path through the encoded model"
    requirement: EXP-04
    verification:
      - kind: unit
        ref: "tests/phase67/test_time_features.py#FourierEncoderTests.test_first_and_second_raw_tau_derivatives_match_the_harmonics"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_time_features.py#DiagnosticNetworkTests.test_encoded_models_keep_the_public_raw_contract_and_com"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_time_features.py#DiagnosticNetworkTests.test_the_frozen_scorer_differentiates_the_encoded_model"
        status: pass
    human_judgment: false
  - id: D3
    description: "The truthful shared logger for encoded inputs and all layer depths (D-11/D-13): null aggregate bandwidth with frequency_applicability false and a reason, pinned feature frequencies/harmonics/internal dimension on both backbones and both designs, raw fields byte-shape against a committed Phase 66 record, every layer logged once in order at depths 2/12 and on the EXP-01 backbone, hook cleanup on success and forced failure, and strict raw-tau monotonicity refusals before any forward"
    requirement: EXP-04
    verification:
      - kind: unit
        ref: "tests/phase67/test_time_features.py#EncodedLoggerTests.test_encoded_measurements_mark_the_aggregate_bandwidth_inapplicable"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_time_features.py#SimilarityCaptureTests.test_every_layer_is_logged_exactly_once_in_order_at_depths_2_and_12"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_time_features.py#SimilarityCaptureTests.test_non_increasing_raw_tau_refuses_before_any_forward"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_catalog.py#RawLoggerShapeTests.test_raw_similarity_entries_match_the_committed_record_shape"
        status: pass
    human_judgment: false
---

# Phase 67 Plan 02: Design & Settings Ladders — Ladders and Time Features Summary

**The declared depth (2/4/6/8/12), rate (1e-3..1e-5) and time-input (raw/fundamental/fundamental+second-harmonic on both required backbones) interventions are constructible and differentiable through the existing public raw14 diagnostic path, with census-pinned encoded frequencies and an applicability-truthful shared logger.**

## Performance

- **Duration:** 20 min (05:41–06:01 UTC, 2026-11-02)
- **Started:** 2026-11-02T05:41:41Z
- **Completed:** 2026-11-02T06:01:00Z
- **Tasks:** 2 of 2
- **Files modified:** 8 (1 new encoder module, 3 extended harness modules, 4 test files)

## Accomplishments

- The Phase 67 registry now declares the exact ladders in one registration order (17 names): D-03's depth arms at the locked width/frequencies/rate/window (137,737 to 795,657 parameters, so the report can state the size change that accompanies depth), D-04's five constant-Adam rates on the locked depth-12 network, and D-05's six input arms on the locked and actual EXP-01 backbones — with `PHASE67_ARMS`/`phase67_variant` as the single arm-resolution source for the execution plans.
- `DiagnosticTimeFeatureNetwork` builds the production layer stack from a copied spec whose internal input dimension is 16 or 18 (fan-in bound `1/internal_dim`, reported beside the count), encodes ordered harmonic sin/cos pairs inside the model after raw tau and IC13 with phase `pi*N_in*(tau+1)`, keeps the public raw14 contract and the inherited mass-weighted COM forward, and owns persistent `frequency_cycles`/`harmonics` buffers that survive state_dict round-trips — the frozen scorer's `vmap(jacrev)` path and the analytic first/second raw-tau derivatives are proven, with no detach, NumPy hop or external preprocessing.
- Encoded frequencies resolve only from validated committed metadata: the exp04 arms pin the main system's committed census row (`f = N_in/10`), and `phase67_registry` re-resolves the frequency from the settings' orbit, refusing disagreement (a 1632-pinned declaration can never run mis-encoded on 851), unknown variants, and malformed census documents.
- The shared `measure_time_signal` is truthful for every declared input family: encoded measurements emit null aggregate bandwidth with `frequency_applicability` false, an explicit reason, and the encoder's pinned per-harmonic physical frequencies, harmonic list and internal dimension; raw records keep their historical JSON shape (proven against a committed Phase 66 record's similarity entries); a non-increasing raw tau column now refuses before any hook (WR-06); and every layer is logged exactly once in order at depths 2 and 12 and on the EXP-01 backbone, with hooks removed on success and on a forced forward failure.
- Raw production construction is untouched: the raw ladder arms build the production class bitwise from the locked spec, construction never touches the global RNG, and parallel encoded builds share no mutable frequency or RNG state.

## Task Commits

1. **Task 67-02-01 RED: failing ladder catalog and time-feature tests** - `d5d9003a` (test) — target `test_the_phase67_registry_holds_the_exact_declared_ladders_in_order` fails on the missing 15 ladder arms; machine-verified `RED_EVIDENCE_OK` (33 tests, 3 regression controls passing).
2. **Task 67-02-01 GREEN: exact ladders and internal Fourier models** - `4ee7909d` (feat) — `diagnostic_time_features.py`, the variant declarations and dispatch, the catalog arms, census resolution; 35 tests OK; also carries the two sibling-pin updates and the task-1 test-defect fixes.
3. **Task 67-02-02 RED: failing encoded-logger truthfulness tests** - `a658a7a1` (test) — target `test_encoded_measurements_mark_the_aggregate_bandwidth_inapplicable` fails `None is not False`; machine-verified `RED_EVIDENCE_OK` (48 tests, 4 planned failures).
4. **Task 67-02-02 GREEN: truthful encoded logger** - `e906ad54` (feat) — the `diagnostic_similarity.py` encoded metadata and raw-tau monotonicity; 48 tests OK.
5. **REFACTOR: optional annotations** - `f4be10d7` (refactor) — `| None` annotations for the None-defaulted metadata fields; no behavior change.
6. **Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_time_features.py` - DiagnosticTimeFeatures (ordered harmonic encoder, phase identity, buffers, refusals) and DiagnosticTimeFeatureNetwork (production class over the copied 16/18-dim spec, COM forward)
- `pinn/verification/diagnostic_variants.py` - `tau_ic13_fourier1`/`tau_ic13_fourier12` support, the optional validated `feature_frequency` (emitted in JSON only for encoded declarations), feature-only `build_variant` dispatch
- `pinn/verification/diagnostic_phase67_catalog.py` - the 15 new ladder declarations, `PHASE67_ARMS`, `phase67_variant`, the census constants/readers and the census-agreement check in `phase67_registry`
- `pinn/verification/diagnostic_similarity.py` - encoded applicability metadata, null aggregate bandwidth, raw-tau strict-increase refusal
- `tests/phase67/test_catalog.py` - exact order/fields/counts, census pinning and resolution, arm resolver, raw parity and RNG, committed raw-shape fixture
- `tests/phase67/test_time_features.py` - encoder layout/identity/derivatives/buffers/refusals, model contract/COM/bounds/scorer AD, encoded logger metadata, layer capture and hook cleanup
- `tests/phase67/test_admission.py`, `tests/phase67/test_historical.py` - sibling pins extended for the mandated catalog growth and the D-12 edited-pins transition

## Decisions Made

- The exp04 encoded arms pin system 1632's census row (the D-09 main comparison system); the 851 confirmation variants are fresh orbit-specific registrations materialized by later plans — `phase67_registry`'s census check is exactly what forces that discipline.
- The raw aggregate bandwidth stays on the raw path unchanged; encoded models get `frequency_applicability`/`frequency_reason`/`feature_frequency_cycles`/`feature_harmonics`/`internal_input_dimension` appended after the historical keys, so no consumer can mistake the nulls for a bandwidth claim (T-67-06).
- No similarity pass bar was added; the adjacent-time cosine remains associated evidence (D-02), now stated in the module contract.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Three test-authoring defects corrected during task 67-02-01 GREEN**
- **Found during:** Task 67-02-01 GREEN
- **Issue:** (a) the exp04 arm table was keyed by registry name while the assertions looked up bare arm ids (`KeyError: 'locked-raw'`); (b) `assertIs` compared two equal-but-distinct string objects; (c) a test expected `phase67_registry(None)` to refuse, but `None` is the sealed Phase 65 default by the 67-01 contract.
- **Fix:** key by the arm-id suffix, use `assertEqual` for strings, and assert `None` selects the sealed registry.
- **Files modified:** tests/phase67/test_catalog.py
- **Verification:** the task verify command moved from 2 failures + 1 error to 35 tests OK.
- **Committed in:** 4ee7909d

**2. [Rule 3 - Blocking] Sibling phase67 pins extended for the mandated catalog growth**
- **Found during:** Task 67-02-01 acceptance verification
- **Issue:** `tests/phase67/test_admission.py` pinned the two-entry registry order and `tests/phase67/test_historical.py` named a single edited pin; this plan's mandated 15-arm extension and harness edits invalidated both, though neither file is in the plan's `files_modified`.
- **Fix:** the admission pin now anchors the head (`locked-12`, `exp02-d2-w256-o30`) and tail (`exp04-exp01-f12`) of the 17-name order with the full order pinned in `test_catalog.py`; the historical `EDITED_PIN` became the `EDITED_PINS` transition set (fit, variants, similarity) with an any-edited-dependency refusal assertion. Run-commit identity assertions unchanged.
- **Files modified:** tests/phase67/test_admission.py, tests/phase67/test_historical.py
- **Verification:** phase67 discovery 61 then 72 tests OK across both tasks.
- **Committed in:** 4ee7909d (and e906ad54's gate)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking)
**Impact on plan:** Both fixes preserve the sibling tests' purposes under the mandated extension; no scope creep. The phase66 live-pin growth is a planned consequence, not a deviation (below).

## Issues Encountered

- phase66 discovery now reports 99 tests / 6 failures: the four known `test_pages` live-digest failures plus the same-class Phase 65 smoke pin on `diagnostic_variants.py` and `diagnostic_similarity.py` (the two files this plan mandates editing). This is the planned D-12 transition (historical registrations pin recorded bytes; live admission is already retired), left untouched per the 67-01 convention and routed to 67-06. phase65 stays 204 OK and phase67 discovery is 72 OK.
- Integration note for 67-06: `diagnostic_fit._receipt_is_a_measurement` still requires finite `first_layer_frequency` median/max numbers, so an encoded registration's logger-parity receipt (null medians, applicability fields) needs the encoded branch in 67-06's adapter work before the first encoded registration.

## Known Stubs

None - every declared arm is fully constructible and differentiable; no placeholder values or unwired paths were introduced.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- 67-03 (windows) is unblocked and independent; 67-04/67-05/67-06 can build on `PHASE67_ARMS`, `phase67_variant` and the census-resolution pattern (`census_feature_frequency` is the precedent for lap-window resolution from validated committed metadata).
- The encoded parity-receipt branch (above) and the repeat-system (851) variant materialization belong to 67-06/67-12, exactly as their plans direct.
- No real metadata, timing or training ran in this plan; the held-out evaluation remains unspent.

## Self-Check: PASSED

All 4 created files exist on disk; all 5 production commits (`d5d9003a`, `4ee7909d`, `a658a7a1`, `e906ad54`, `f4be10d7`) exist in history; both TDD gate sequences are present and ordered (test → feat per task, plus one refactor); both task verify commands re-ran green at final HEAD (48 tests OK) and the Phase 67 discovery is 72 tests OK; `git diff --check` clean over the plan range.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
