---
phase: 65-probe-on-the-record-fit-harness
plan: "01"
subsystem: testing
tags: [pinn, diagnostic-harness, pytorch, similarity-measurement, frozen-scorer, tdd]

requires:
  - phase: 60-single-system-learnability
    provides: INST-05 fixture data seam, data_only_loss, frozen score_network/score_trajectory, write_record_exclusive, weights_digest, 33 pinned module digests
  - phase: 59-read-only-baseline-scorecard
    provides: frozen FEAS-01 scorecard and two-Kepler comparison formula
provides:
  - DiagnosticVariant, build_variant, resolve_variant and the sealed locked-12 registry entry with register_variant/registry_names
  - measure_time_signal, the one shared centred-neighbour time-signal implementation for probe and fit logger
  - fit_diagnostic and log_similarity, the synthetic fit-to-score-to-record path with the inst08-diagnostic/v1 record schema
  - diagnostic_guard with the intrinsic inst08 marker, require_not_diagnostic typed refusal and the diagnostic readers
  - All four Phase 65 Wave 0 unittest modules (test_fit_short, test_contracts, test_probe, test_isolation)
affects: [65-02, 65-03, 65-04, 65-05, 65-06]

actuals:
  tokens: 26061   # chars/4 over the realized 65-01 diff (104245 chars, 2333 insertions)
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Diagnostic variants build the production network from copied validated ArchitectureSpec fields, never by relaxing the production locks"
    - "One shared measurement implementation (measure_time_signal) serves probe and logger, with hooks on the real forward cleaned up in finally"
    - "Intrinsic payload markers (artifact_kind/diagnostic/counted) make diagnostic artifacts refusable by content, independent of filename"

key-files:
  created:
    - pinn/verification/diagnostic_variants.py
    - pinn/verification/diagnostic_similarity.py
    - pinn/verification/diagnostic_fit.py
    - pinn/verification/diagnostic_guard.py
    - tests/phase65/__init__.py
    - tests/phase65/test_fit_short.py
    - tests/phase65/test_contracts.py
    - tests/phase65/test_probe.py
    - tests/phase65/test_isolation.py
  modified: []

key-decisions:
  - "The frozen two-Kepler formula's Newton solver does not converge on the synthetic fixture orbit; that RuntimeError is caught narrowly around two_kepler_prediction and recorded as a non-applicable comparison row (failure: solver_did_not_converge) carrying the frozen module's own message, so a formula failure never becomes a successful score"
  - "fit_diagnostic takes times_physical explicitly (defaulting to the score view's times) so physical time and normalized tau are recorded separately, per D-05"
  - "Unregistered DiagnosticVariant instances are allowed as explicit fixture inputs and recorded with registered: false; only the sealed registry names registered variants"
  - "The zero gold finite-difference rate denominator is unreachable behind the zero-target-variation refusal; both guards exist and the reachable one is tested"

patterns-established:
  - "Wave 0 modules refuse typed-and-early: variant resolution, step counts, sample validation and denominator checks all raise before an optimizer step or any publication"
  - "Comparison rows recompute through the frozen score_trajectory with velocity_source analytic for both matched predictors, mirroring baselines.py"

requirements-completed: []   # DIAG-09 and INST-08 span later Phase 65 plans; Wave 0 alone completes neither

coverage:
  - id: D1
    description: "One synthetic orbit completes the real model/loss/logger/scorer/diagnostic-record path end to end (two guarded constant-rate Adam steps, init+final similarity once each, frozen network score, constant and two-Kepler comparison rows, one exclusive record plus marked tensor payload)"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_fit_short.py#ShortFitTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_fit_short.py#RefusalTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Named-variant registry and contracts: sealed locked-12 entry, exact-ASCII identity, duplicate/unknown/malformed refusals, exact serialization round-trip, bitwise production parity same-runtime/same-weights (CPU64 always, MPS32 when available), 33 pinned digests against the committed protocol with missing-artifact refusal, direct frozen scorer calls"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_contracts.py#RegistryContractTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_contracts.py#ParityContractTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_contracts.py#FrozenSourceContractTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_contracts.py#FitRecordContractTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Synthetic measurement and artifact edges: reductions pinned against a direct cosine at the torch epsilon, deterministic layer order, separate physical/tau coordinates, finiteness and strictly-increasing time refusals before any forward, hook cleanup after a raised forward, and intrinsic marker survival under renaming, relocation, nesting and production-key laundering"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_probe.py#MeasurementSemanticsTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#MeasurementRefusalTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_isolation.py#DiagnosticEnvelopeTests"
        status: pass
    human_judgment: false

duration: 33 min
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 01: Probe on the Record & Fit Harness — Wave 0 Summary

**Synthetic diagnostic fit harness: named locked-12 variant through guarded constant-rate Adam, shared centred-neighbour similarity, frozen scorer with matched comparison rows, and intrinsically marked inst08 records — all four Wave 0 test modules in place before any corpus access.**

## Performance

- **Duration:** 33 min (02:46–03:19 UTC, 2026-10-29)
- **Started:** 2026-10-29T02:46:23Z
- **Completed:** 2026-10-29T03:19:16Z
- **Tasks:** 3 of 3
- **Files modified:** 9 created (4 modules, 5 test files incl. `tests/phase65/__init__.py`), 0 existing files edited
- **Full Phase 65 suite latency:** 58 tests in 1.124 s (unittest measure; ~1.8 s wall including interpreter start)

## Accomplishments

- One synthetic orbit (the Phase 60 tiny gold corpus, 24 points, float64 CPU, seed 42) traverses the complete path: named locked-12 variant → two finite constant-rate Adam steps (weights really change) → init and final similarity once each → frozen `score_network` (entire `ScoreResult.to_json_dict`) → window-mean constant (zero velocities) and two-Kepler comparison rows on identical times and body order → one exclusive canonical record plus an intrinsically marked tensor payload, readable by the diagnostic reader and refused by `require_not_diagnostic` after renames and relocation.
- The registry is sealed to exactly `locked-12` (depth 12, width 256, raw [tau, IC13], locked frequencies, lr 1e-4, window [0, 10]); `register_variant` extends a copy in registration order and refuses duplicates; serialization round-trips numerics exactly. The locked variant is bitwise the production network at the same seed (CPU float64 `torch.equal` on parameters and projected outputs with unequal raw masses, state copied in either direction; MPS float32 same-weights parity case skips only when that runtime is unavailable).
- All 33 `PINNED_MODULES` digests still match the committed Phase 60 protocol (`93486d240f12…`, revalidated by `load_protocol()` at HEAD); a missing pinned artifact is a typed refusal, and the fit record reuses the same source hashes. Frozen scorecard digest unchanged (`f4b17688…444b`).
- Measurement edges: value validation and strictly-increasing time checks happen before any hook or forward; samples are never sorted, merged or dropped; hooks never survive a raised forward; scripted-row tests pin the reductions to a direct `F.cosine_similarity` at the torch default epsilon.

## Task Commits

Each task followed RED → GREEN (TDD), each RED gate machine-verified `RED_EVIDENCE_OK` via `check tdd-red-evidence`:

1. **65-01-01 fit and score one synthetic orbit end to end (tracer)** — `6c728271` (test) + `b292c060` (feat)
2. **65-01-02 prove named-variant parity and frozen scoring contracts** — `22c88395` (test) + `ca319423` (feat)
3. **65-01-03 cover synthetic measurement and artifact edges** — `9b964004` (test) + `b548da0a` (feat)

Tracer feedback gate: the tracer `<verify>` re-ran end-to-end on the committed tree (19 tests, exit 0) before expansion continued.

**Plan metadata:** this commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_variants.py` — `DiagnosticVariant`, `build_variant`, `resolve_variant`, sealed `REGISTRY`, `register_variant`, `registry_names` (SHA-256 `ad8ed66c…5dfb`)
- `pinn/verification/diagnostic_similarity.py` — `measure_time_signal`, the shared centred-neighbour measurement (SHA-256 `e80079b6…4d7`)
- `pinn/verification/diagnostic_fit.py` — `fit_diagnostic`, `log_similarity`, `pinned_source_hashes`, canonical record and marked payload writers (SHA-256 `2e2c06eb…2ca`)
- `pinn/verification/diagnostic_guard.py` — intrinsic marker, `require_not_diagnostic`, `DiagnosticArtifactRefused`, diagnostic readers (SHA-256 `d8317042…a6c`)
- `tests/phase65/{__init__,test_fit_short,test_contracts,test_probe,test_isolation}.py` — 58 tests total

## Verification Commands and Outcomes

- `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_fit_short -v` → 19 tests OK (exit 0)
- `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_contracts -v` → 19 tests OK (exit 0)
- `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_probe tests.phase65.test_isolation -v` → 20 tests OK (exit 0)
- Full suite `… -m unittest discover -s tests/phase65 -p 'test_*.py' -v` → 58 tests OK, 1.124 s
- `git diff --check` → clean; `load_protocol()` at HEAD → all 33 pinned digests unchanged
- Sealed entry points never called: spies on `open_real_context`, `run_arm`, `admit_arm` recorded 0 calls during the class-level fit; no `runs/phase65` or diagnostic directory was created anywhere in the repository (all evidence roots were temporary directories)

## Decisions Made

- **Two-Kepler solver non-convergence on the synthetic fixture** (see Deviations): the frozen module's `RuntimeError` is caught only around the `two_kepler_prediction` call and recorded as a non-applicable row with the frozen message verbatim, distinct from `NotApplicable` (`failure: solver_did_not_converge` vs `not_applicable`). The frozen module itself was not modified.
- **Explicit physical times:** `fit_diagnostic` takes `times_physical` (default the score view's times, exact for the fixture where train and score share a grid) so the record carries physical time and tau separately, per D-05.
- **Registry identity surface:** unregistered `DiagnosticVariant` instances are fixture inputs recorded with `registered: false`; the sealed catalog holds only `locked-12`, and the Phase 66-67 ladders are not populated.
- **Rate-denominator guard:** the zero gold-FD-rate refusal is doubly guarded (unreachable behind the zero-target-variation refusal); the reachable denominator refusal is tested, the unreachable one retained defensively.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Frozen two-Kepler formula crashes the fit on the synthetic fixture orbit**
- **Found during:** Task 1 (65-01-01), first GREEN run
- **Issue:** the plan names only `NotApplicable` as the formula's non-result path, but the frozen Newton solver raises `RuntimeError("Kepler Newton solve did not converge")` on the fixture's near-radial synthetic geometry (verified: monotone residual whose Newton iteration oscillates), which crashed `fit_diagnostic` before any record.
- **Fix:** caught `RuntimeError` narrowly around the `two_kepler_prediction` call and recorded it as `{"comparison": "two_kepler", "applicable": false, "failure": "solver_did_not_converge", "reason": <frozen message verbatim>}` — fail-closed, never a successful score, distinguishable from `NotApplicable`.
- **Files modified:** `pinn/verification/diagnostic_fit.py`, `tests/phase65/test_fit_short.py`
- **Verification:** `test_comparison_rows_match_direct_recomputation_on_the_same_window` mirrors both exception paths against direct recomputation; all 58 tests pass.
- **Committed in:** `b292c060`

**2. [Rule 3 - Blocking] Created `tests/phase65/__init__.py`**
- **Found during:** Task 1 RED
- **Issue:** `python -m unittest tests.phase65.test_fit_short` needs the package marker (matching the phase59/phase60 convention); the plan's file list omits it.
- **Fix:** added the one-line package file in the RED commit.
- **Files modified:** `tests/phase65/__init__.py`
- **Verification:** all module-form verify commands run as written in the plan.
- **Committed in:** `6c728271`

---

**Total deviations:** 2 auto-fixed (1 bug adaptation, 1 blocking infrastructure)
**Impact on plan:** No scope creep; both fixes are local to this plan. No pinned file was touched (protocol revalidates at HEAD).

## TDD Gate Compliance

All three tasks committed a `test(65-01)` RED before their `feat(65-01)` GREEN, and each RED was machine-verified `RED_EVIDENCE_OK` (`check tdd-red-evidence`, target tests: the Wave 0 module-existence assertion, the missing `register_variant` symbol, and the absent non-increasing-times refusal). Task 2's parity tests passed already at RED time — regression coverage of Task 1's faithful `build_variant`, documented here rather than treated as an unexpected GREEN. Task 3's isolation tests likewise covered Task 1 guard behavior; its genuinely new behavior (non-finite/non-increasing time refusals) drove the RED.

## Issues Encountered

- `unittest` does not emit TAP, so RED evidence was captured through a small faithful TAP converter (a real in-process run reporting each test's actual outcome); the converter initially missed `subTest` failures and was fixed before use.
- Test-side corrections during GREEN: the shared fixture loader was a classmethod used from both class and instance contexts (attribute errors), the scripted-boundary stub needed a zero-multiple-of-the-leaf so the rate comparator had an autograd graph, the synthetic tau column needed the loader's `2t/T − 1` transform, and one scripted-omega expectation used 30.0 instead of the scripted 0.3. All are test bugs, not implementation changes.

## User Setup Required

None — no external service configuration; everything runs on the local `pinn-train` environment.

## Known Stubs

None — every delivered path is real; no placeholder, TODO or unwired data source remains in the four new modules.

## Next Phase Readiness

- Wave 0 is complete: all four `tests/phase65` targets exist and pass, so later Phase 65 plans can invoke them.
- Ready for Plan 65-02 (probe registration and the read-only reproduction): `measure_time_signal` is the shared implementation the probe must call, and the preserved originals' reductions are already transcribed and pinned by `test_probe`.
- Plan 65-03 will wire `require_not_diagnostic`/`DiagnosticArtifactRefused` into the production graded-run and evaluator entry points; the typed refusal is exported and content-tested, including relocation and production-key laundering.
- No blocker. The held-out evaluation remains unspent; no real corpus record was opened by this plan.

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*
