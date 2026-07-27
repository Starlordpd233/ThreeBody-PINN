---
phase: 46-frame-resolution-gate-aligned-validation
plan: "05"
subsystem: testing
tags: [inst-01, isolation, non-interference, mode-restoration, sidecar, fail-closed, sentinels, pointer-discipline, d-12, d-15, d-16, d-17, d-18, d-20, d-23, d-24]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-01 stub fixtures (StubStageSource/StubModel/disjoint split pair) and 46-03 validation_gate module under test
provides:
  - tests/phase46/test_isolation.py (12 tests, zero skips) — D-16 dual enforcement, D-12/D-23 restoration, D-15/D-23 non-interference
  - tests/phase46/test_artifacts.py (18 tests, zero skips) — D-17 atomicity, D-18/D-20 fail-closed, sentinel retention, pointer discipline
affects: [46-07 wiring plan — these suites must stay green while it touches pinn/train.py and pinn/training/summary.py]

tech-stack:
  added: []
  patterns:
    - "AST-over-raw-source prohibition detectors (phase40 style) applied to the gate module: evaluator-import scan and handler-less-try mode-bracket pin"
    - "Fresh-subprocess sys.modules isolation check (transitive import graph, not just direct source)"
    - "Observations built exactly the production way: per-row SCS, aggregate, verdict, and thresholds all sourced from gate_metrics — no hand-set threshold or verdict"

key-files:
  created:
    - tests/phase46/test_isolation.py
    - tests/phase46/test_artifacts.py
  modified:
    - .planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md

key-decisions:
  - "Held-out isolation enforced twice (T-46-05-01): AST scan over raw source covering every import spelling (absolute, from-import, package-plus-name, relative) AND a fresh-subprocess sys.modules check"
  - "FrameConvention constructed INLINE in both suites (D-07 frame-independence); the wave-5 ratified-frame constant is never referenced — reaching for it through _require would vacuate the suites while exiting green (T-46-05-04)"
  - "Signature pinned exactly (model, validation_source, keyword-only stage/global_step/frame/dtype/device) so an interference-capable argument cannot be added silently (D-15)"
  - "Schema fail-closed loop enumerates the full 16-key top-level 46-03 schema list, never a hand-picked subset; nested frame/row/record_key shape pinned on the published payload"

patterns-established:
  - "Metric JSON legality predicate: finite number or one of the three quoted sentinels, bool rejected — asserted over every gate metric field"
  - "Instrumentation-failure vs metric-FAIL distinction pinned by paired tests: missing/truncated/corrupt sidecar raises, valid-FAIL observation still yields gate_status ok pointer fields"

requirements-completed: [INST-01]

coverage:
  - id: D1
    description: "Held-out isolation: no evaluator import in source (AST) or in a fresh interpreter's sys.modules (subprocess)"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_isolation.py#EvaluatorImportIsolationTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Prior-mode restoration from BOTH prior states, healthy and under an injected mid-population failure; handler-less try/finally bracket AST-pinned"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_isolation.py#ModeRestorationTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Non-interference: parameters bitwise-identical, no populated gradient, exact-signature pin, deterministic consecutive passes"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_isolation.py#NonInterferenceTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Validation-only driving: rows exactly the sorted validation key set, none from train; fixture-surface withheld-split identifiers re-asserted absent"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_isolation.py#ValidationOnlySourceTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "Atomic publication: valid final file, no temp residue, byte-identical re-publish, hostile step rejected before any write"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_artifacts.py#SidecarPublicationTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "Schema fail-closed over the full 16-key enumeration plus version/order/count/string-metric/row-subkey violations"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_artifacts.py#SchemaFailClosedTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "Non-finite retention: NaN/Infinity/-Infinity quoted sentinels under plain json.loads, schema-legal, FAIL verdict retained"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_artifacts.py#NonFiniteRetentionTests"
        status: pass
    human_judgment: false
  - id: D8
    description: "Pointer discipline: missing/truncated/corrupt sidecars refuse fields; valid sidecar returns exactly the eight gate_* keys; valid-FAIL yields ok status"
    requirement: INST-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_artifacts.py#PointerDisciplineTests"
        status: pass
    human_judgment: false

duration: ~58min
completed: 2026-07-27
status: complete
---

# Phase 46 Plan 05: Validation-Gate Isolation and Artifact Fail-Closed Contracts Summary

**INST-01 safety properties PROVEN as tests: held-out isolation enforced doubly (AST + fresh subprocess), prior-mode restoration from both states under failure, observation-only non-interference proven bitwise and structurally, and the persistence contract pinned — atomic, schema-fail-closed, sentinel-preserving, pointer-only-after-durable — all dataset-free (D-24)**

## Performance

- **Duration:** ~58 min (includes two full `tests/` sweeps at ~9 min each)
- **Started:** 2026-07-27T05:24:59Z
- **Completed:** 2026-07-27T06:22:42Z
- **Tasks:** 2
- **Files modified:** 2 created, 1 modified (deferred-items log)

## Accomplishments

- `tests/phase46/test_isolation.py` — **12 tests, zero skips**, four classes:
  - `EvaluatorImportIsolationTests` (D-16): AST scan of `pinn/training/validation_gate.py` raw source finds no `Import`/`ImportFrom` resolving to the held-out evaluator module in ANY spelling — `import pinn.evaluate[.x]`, `from pinn.evaluate[.x] import ...`, `from pinn import evaluate`, and the relative form `from .. import evaluate` (resolved against the containing package). The fresh-subprocess check (`sys.executable -c`, cwd = repo root) imports the gate and asserts no `pinn.evaluate[.x]` module is present in `sys.modules` — the transitive import graph stays clean, not just the direct source. Either detector alone would catch a direct import; together they also catch a lazy or transitive import (T-46-05-01).
  - `ModeRestorationTests` (D-12/D-23): prior mode restored after a healthy pass from BOTH prior states (train→train, eval→eval — strictly stronger than an unconditional `train()` restore) and under an injected mid-population failure (hook fires on call 2 of 3; the RuntimeError propagates unconverted AND the prior mode holds). The mode bracket is AST-pinned as a handler-less `try/finally` whose body reaches the bare `model(...)` call — a bare `try/finally` cannot swallow a signal; only an `except` handler can (the phase40 detector scoping rule).
  - `NonInterferenceTests` (D-15/D-23): around a gate pass over the tiny real CPU/float64 network (`tests/phase40/_fixtures.make_stub_model`), every parameter is bitwise-identical (`torch.equal`) and every `p.grad is None`. `inspect.signature(compute_validation_gate)` is pinned EXACTLY — `(model, validation_source, *, stage, global_step, frame, dtype, device)` with the last five keyword-only — plus a banned-token sweep (optimizer/scheduler/replay/checkpoint/early_stop/stage_machine/stage_exit/curriculum/controller/loss/grad/hook/callback/writer), so an interference-capable argument cannot be added silently. Two consecutive passes produce identical row keys, per-row metrics, aggregates, and verdict (deterministic and stateless).
  - `ValidationOnlySourceTests` (D-16/D-23): the gate driven by the validation member of the disjoint stub pair returns rows whose keys are EXACTLY the sorted validation key set (full-pool; the stub's descending insertion order makes the sort assertion non-vacuous), none from the train member, `split == "validation"`. The banned withheld-split identifier set from 46-01 acceptance criterion 3 (`test_source|make_test|test_index|held.?out`, case-insensitive) is re-asserted absent from `tests/phase46/_fixtures.py` source text — never by constructing the forbidden object (D-16).
- `tests/phase46/test_artifacts.py` — **18 tests, zero skips**, four classes:
  - `SidecarPublicationTests` (D-17): publish lands the final file at `sidecar_relative_path(step)`, parses, passes `validate_sidecar_payload`, and leaves NO `.tmp.` residue anywhere under the run dir (the `atomic_io` ordering: tmp+fsync → os.replace → dir fsync → finally-unlink); re-publish is byte-identical (idempotent atomic replace); a hostile step (negative, `True`, `False`) raises `ValueError` before any write, and a publish attempted with `global_step=-1` leaves the run dir empty.
  - `SchemaFailClosedTests` (D-18/D-20): the missing-key loop enumerates the FULL 16-key top-level schema list from the 46-03 SUMMARY (never a hand-picked subset — T-46-05-04), plus wrong `schema_version`, rows out of RecordKey order, row count disagreeing with `n_trajectories` (±1), non-sentinel string metrics (row `eps_h`/`scs` and both aggregates, including a numeric STRING, which is not a legal sentinel), and a dropped `record_key` sub-key. The published payload's complete shape (16 top-level, 4 `frame`, 3 row, 3 `record_key` keys) is pinned exactly.
  - `NonFiniteRetentionTests` (D-20): a NaN per-row `eps_h` (its SCS also NaN), a zero-`eps_h` row (derived SCS `-inf`), and an Inf aggregate publish successfully; the raw bytes contain all three quoted sentinels `"NaN"` / `"Infinity"` / `"-Infinity"`; plain `json.loads` (no custom decoder) shows the quoted forms with `0.0` surviving as a number; NO gate metric field is null and each is a finite number or one legal sentinel; the payload passes `validate_sidecar_payload` (sentinels are schema-legal); the FAIL verdict accompanies the non-finite aggregate with `gate_status == "ok"` and `n_nonfinite == 1`.
  - `PointerDisciplineTests` (D-17/D-20): `compact_validation_fields` on a run dir without the sidecar raises `ValidationGateUnavailable`; a sidecar truncated to half its bytes raises; a corrupted required key (verdict outside PASS/FAIL; dropped `rows`) raises; a valid sidecar returns EXACTLY the eight `gate_*` keys from the artifact table with `gate_sidecar` equal to the relative path and `gate_status == "ok"`. The instrumentation-failure vs metric-FAIL distinction is pinned: a valid-but-FAIL observation (worst-case `eps_h` 1.0) still yields `gate_status == "ok"` pointer fields carrying `gate_verdict == "FAIL"` — a metric FAIL is honest evidence, not an instrumentation failure; the two states are never conflated.

## Enforced isolation mechanisms (plan-required record)

1. **Static (AST over raw source).** `_import_nodes_targeting_evaluator` walks the parsed module and resolves every import spelling to an absolute dotted name, including relative `ImportFrom` levels against the containing package `pinn.training` (so `from .. import evaluate` is caught as `pinn` + `evaluate`). Guarded by `.is_file()` (phase40 named-module audit precedent); absence degrades to a localized skip via `_require`, never an ERROR.
2. **Dynamic (fresh subprocess).** A clean interpreter imports `pinn.training.validation_gate` and prints whether any module equal to or under `pinn.evaluate` is present in `sys.modules`; the test asserts `absent`. This catches anything the source scan cannot see — an import hidden behind a helper, a dynamic `importlib` call, or a transitive pull from `pinn/__init__.py`, `pinn.training/__init__.py`, or `pinn.verification/__init__` (all three inspected: none references the evaluator).

## Schema-key enumeration source (plan-required record)

The missing-key fail-closed loop enumerates the sixteen top-level keys recorded in the 46-03 SUMMARY's "Sidecar schema keys (D-18)" block — `schema_version, run_dir, sidecar_path, global_step, stage, split, frame, n_trajectories, rows, n_nonfinite, eps_h_reject_threshold, scs_reject_threshold, aggregate_eps_h, aggregate_scs, verdict, gate_status` — held as the suite-level `SCHEMA_REQUIRED_KEYS` constant with a comment citing that SUMMARY section. The list is hardcoded from the SUMMARY rather than imported from the module's private `_REQUIRED_TOP_KEYS`, so the test pins the schema independently of the validator's own table (a dropped key on either side fails loudly). `test_each_required_key_removed_raises` also asserts the list has exactly 16 entries, so an accidental shrink of the enumeration itself fails.

## 46-03 contract details the tests forced to be clarified (plan-required record)

1. **Validator scope vs documented nested schema.** `validate_sidecar_payload` enforces the 16 TOP-LEVEL required keys, the row `record_key` triple, row/aggregate metric legality, row ordering, row count, and verdict membership — it does NOT enumerate the four `frame{...}` sub-keys (a payload missing `frame.position_frame` passes validation). The missing-key loop therefore enumerates the 16 top-level keys (exactly the set the 46-03 SUMMARY's validator contract sentence calls "all required keys"), and the nested shape — `frame{position_frame, time_coord, mass_convention, conf01_evidence_ref}`, `rows[]{record_key{variant, fidelity, id}, eps_h, scs}` — is pinned on the PUBLISHED payload instead (`test_published_payload_shape_matches_documented_schema`), i.e., at the producer the 46-07 wiring consumes. No production change was made (this plan writes no production code); if a fail-closed `frame` sub-key check is ever wanted, that is a 46-03 contract amendment for a later plan, not a test-side invention.
2. **The Inf-aggregate shape is a serialization fixture, not an aggregate-path product.** `gate_metrics.aggregate_test_eps_h` maps ANY non-finite per-row value to a NaN aggregate (never ±Inf — verified in source), so the plan's "NaN per-row + Inf aggregate" observation cannot arise from the production aggregate path. The suite builds it directly: `make_observation([nan, 1e-6, 0.0])` then `dataclasses.replace(aggregate_eps_h=inf, aggregate_scs=gate_metrics.scs_from_eps_h(inf), verdict=gate_metrics.gate_verdict(inf))` — the SCS (NaN) and verdict (FAIL) remain gate_metrics-derived, never hand-set (D-06/D-13). The purpose is to exercise all three quoted sentinels in one published payload.
3. **`scs_from_eps_h` edge values confirmed and used as grounded sentinel sources:** non-finite or negative input → NaN; exactly `0.0` → `-inf`. The zero-`eps_h` row's `-inf` SCS is what exercises the `"-Infinity"` sentinel; `0.0` itself survives the round-trip as a JSON number, proving sentinels and legitimate zeros are not conflated.
4. **Sorted-row assertions are non-vacuous by fixture design:** the 46-01 validation stub inserts ids in DESCENDING order, so `records_at_or_below(0)` returns an order that differs from `sorted(...)`; the suite's `row_keys == sorted(validation_keys)` assertion genuinely exercises the module's sort.
5. **`compact_validation_fields` returns exactly the eight `gate_*` keys** (no extras): pinned by exact-set comparison against the artifact-table list, so a silently added ninth pointer field fails.

## Contract surfaces Plan 46-07 quotes verbatim

- `EXPECTED_GATE_FIELDS` — the eight compact `validation.jsonl` keys: `gate_schema_version, gate_eps_h, gate_scs, gate_verdict, gate_status, gate_n_trajectories, gate_n_nonfinite, gate_sidecar`.
- `SCHEMA_REQUIRED_KEYS` — the sixteen-key sidecar schema list (46-03 SUMMARY).
- The inline-frame construction rule: 46-07's own suite (`test_validation_wiring.py`) constructs test frames inline exactly as these suites do until `RATIFIED_VALIDATION_FRAME` exists — then the production constant becomes reachable WITHOUT vacuating suites (the T-46-05-04 lesson).
- The fail-closed pointer semantics the `_validation_summary` projection stands on: no durable schema-valid sidecar → `ValidationGateUnavailable` → no pointer fields, never a fabricated eligibility.

## Task Commits

Both tasks landed in one plan-prescribed commit:

1. **Tasks 1-2: test_isolation.py + test_artifacts.py** - `270e045` (test)

## Files Created/Modified

- `tests/phase46/test_isolation.py` — created (12 tests)
- `tests/phase46/test_artifacts.py` — created (18 tests)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md` — modified (DI-46-05-01 added)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-05-SUMMARY.md` — created (this file)

## Decisions Made

- **Dual isolation enforcement (AST + subprocess)** rather than either alone: a source scan cannot see transitive/dynamic imports; a subprocess check cannot attribute the source line. Together they make D-16 regression-proof in both directions (T-46-05-01).
- **Inline FrameConvention in both suites** (module-level constant built from the gate module's own constants): the properties are frame-independent (D-07), and the wave-5 ratified-frame constant does not exist at wave 3 — importing it through `_require` would produce vacuous green skips (T-46-05-04).
- **Real tiny network for the bitwise/determinism proofs** (`tests/phase40/_fixtures.make_stub_model`, CPU/float64): `StubModel` proves the mode-bracket semantics, but only a real parameterized network can prove parameters and gradients are untouched (D-15).
- **Hardcoded 16-key schema list from the 46-03 SUMMARY** rather than importing the module's private `_REQUIRED_TOP_KEYS`: an independent pin, so validator-side drift fails the test.
- **Observations built the production way:** per-row SCS via `scs_from_eps_h`, aggregate/verdict via `aggregate_gate_verdict`, thresholds via the `GATE_*_REJECT_THRESHOLD` constants — no test invents a threshold or verdict (D-06/D-13).

## Deviations from Plan

None — the plan executed exactly as written. No Rule 1/2/3 fixes were triggered; no package installs occur anywhere in Phase 46.

### Out-of-scope discoveries (logged, not fixed)

- **DI-46-05-01** — `tests/watchdog/test_global_packaging.py` 2 failures (`test_a5_canonical_bin_matches_repo_source`, `test_a6_deployed_skill_paths_rewritten`): live-deploy drift between the repo's `scripts/watchdog/wd-arm` and the canonical global bin, caused by watchdog extraction work outside this phase. Zero coupling with this plan's diff (two new files under `tests/phase46/` only). Logged to `deferred-items.md`; remediation belongs to the watchdog redeploy track.
- The 12 pre-existing `tests/phase43` failures (DI-46-04-01) are unchanged — same 12 tests, zero new phase43 failures.

## Issues Encountered

None blocking. The two full-repo verification sweeps (~9 min each) dominated the wall clock; both confirmed the pre-existing failure sets above and nothing new.

## Verification

- Task 1 verify: `pytest tests/phase46/test_isolation.py -x -q -rs` → **12 passed, 0 skipped**, exit 0, no skip token in output. (≥8 required.)
- Task 2 verify: `pytest tests/phase46/test_artifacts.py -x -q -rs` → **18 passed, 27 subtests passed, 0 skipped**, exit 0, no skip token. (≥12 required.)
- Phase sweep: `pytest tests/phase46/ -q` → **94 passed, 27 subtests passed**.
- Full sweep: `pytest tests/ -q` → **1252 passed, 3 skipped (pre-existing phase42 `pinn-train env not available`), 14 failed = 12 pre-existing phase43 (DI-46-04-01, unchanged) + 2 pre-existing watchdog packaging (DI-46-05-01, environmental live-deploy drift)**. `tests/phase37`–`phase42` stay green.
- Acceptance greps: `grep -c "simulation_data" tests/phase46/test_isolation.py` → 0; `grep -c "RATIFIED_VALIDATION_FRAME" tests/phase46/test_isolation.py` → 0; `grep -c "simulation_data\|runs/stage0" tests/phase46/test_artifacts.py` → 0; `grep -c "RATIFIED_VALIDATION_FRAME" tests/phase46/test_artifacts.py` → 0.
- `git status --short` shows additions only under `tests/phase46/` (this plan writes no production code); all pre-existing unrelated working-tree changes left untouched.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 46-06 (the single real-corpus CONF-01 evidence run) is unblocked on its own wave dependency (46-04 landed); this plan shares wave 3 and does not gate it.
- 46-07 (frame ratification + `train.py`/`summary.py` wiring) inherits these two suites as its regression net: the wiring must keep `tests/phase46/` green while adding `RATIFIED_VALIDATION_FRAME` and the hook. The inline-frame rule in these suites means they neither depend on nor conflict with the wave-5 constant.
- The `EXPECTED_GATE_FIELDS` eight-key list and the pointer-discipline semantics pinned here are exactly what 46-07's `validation.jsonl` emission and `_validation_summary` projection must satisfy.

## Self-Check: PASSED

- `tests/phase46/test_isolation.py` — FOUND (12 tests, green)
- `tests/phase46/test_artifacts.py` — FOUND (18 tests, green)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md` — FOUND (DI-46-05-01)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-05-SUMMARY.md` — FOUND (this file)
- Commit `270e045` — FOUND (`git log --oneline` verifies all four files in one atomic commit; no deletions)

---
*Phase: 46-frame-resolution-gate-aligned-validation*
*Plan: 05*
*Completed: 2026-07-27*
