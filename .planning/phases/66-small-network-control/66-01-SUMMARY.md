---
phase: 66-small-network-control
plan: 01
subsystem: pinn-verification
tags: [exp01, diagnostic-harness, variant-registry, ac-power-gate, loss-trace-stride, tdd]
requires:
  - phase: 65-probe-on-the-record-fit-harness
    provides: "the INST-08 fit harness (diagnostic_fit/variants/guard/data/similarity), the sealed locked-12 registry, the committed-registration admission and the 204-test phase65 suite"
provides:
  - "diagnostic_phase66.py: EXP01_VARIANT (exp01-d1-w384-o1000), PHASE66_REGISTRY, the closed REGISTRIES name table, NEAR_BAND, tier1_e_max, classify_exp01"
  - "diagnostic_power.py: fail-closed first-line pmset AC gate, PowerRefused before any receipt or run, the exclusive power-gate.json receipt, and the fixed-argv caffeinate launch of the fit CLI"
  - "the six-site diagnostic_fit.py extension: registration-declared variant_registry lookup, registry fields on the record with the verify check, and the registration-declared loss_trace_stride (Site F) that thins only the recorded trace"
  - "tests/phase66 package: tracer, catalog, admission, records and historical contracts (30 tests)"
affects: [66-02, 66-03, 66-04, 66-05, phase-67]
actuals:
  tokens: 15350
  tasks: 2
  commits: 3
tech-stack:
  added: []
  patterns:
    - "registration-declared named-registry lookup over a closed MappingProxyType table, with absent/null selecting the sealed catalog"
    - "fail-closed positive parse of the pmset first line before any side effect"
    - "record-size bounded at its source: a registration-declared loss-trace stride thins only the recorded trace"
key-files:
  created:
    - pinn/verification/diagnostic_phase66.py
    - pinn/verification/diagnostic_power.py
    - tests/phase66/__init__.py
    - tests/phase66/test_tracer.py
    - tests/phase66/test_catalog.py
    - tests/phase66/test_admission.py
    - tests/phase66/test_records.py
    - tests/phase66/test_historical.py
  modified:
    - pinn/verification/diagnostic_fit.py
key-decisions:
  - "Decision 1 (carried from the plan): the digest-pinned diagnostic_fit.py is edited at exactly the six declared sites (A-E plus the loss-trace stride F), and the Phase 65 smoke registration becomes historical; the other four smoke-pinned modules stay byte-identical and the identity is anchored at the smoke-record commit 84128fe2, not the registration's introducing commit"
  - "Decision 2 (carried from the plan): reuse-condition stance — WR-01 is a precondition for graded use only; WR-02/WR-05 govern probe registrations; WR-03/WR-04 stay deferred (verify-result runs only on records this harness wrote at registered paths); WR-06 not triggered (same loader and time transform); IN-01 not triggered (schema literal unchanged, new keys validated strictly)"
  - "The tracer's launcher passes the resolved ABSOLUTE registration and output paths in the child argv (cwd-independent, so the in-process test and the detached run resolve identically) while the receipt holds repo-relative paths only, keeping the redaction guard satisfied"
  - "fit_diagnostic resolves the named registry and validates the stride before the model is built, so a bad value refuses before any data access or optimizer work, not at record-assembly time"
requirements-completed: []
coverage:
  - id: D1
    description: "A committed phase66 registration admitting through the unchanged door, run end to end on synthetic data: AC gate, registry-aware admission, fit, thinned loss record, verify_fit_result and classify_exp01"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_tracer.py#Phase66TracerTests.test_the_ac_case_runs_one_synthetic_exp01_run_end_to_end"
        status: pass
      - kind: unit
        ref: "tests/phase66/test_tracer.py#Phase66TracerTests.test_the_battery_case_refuses_before_anything_is_created"
        status: pass
    human_judgment: false
  - id: D2
    description: "The sealed catalog and every Phase 65 refusal intact: sealed locked-12 registry, all admission refusals with the EXP-01 variant, cap/MPS/policy/stride matrices"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_catalog.py#Phase66CatalogTests"
        status: pass
      - kind: unit
        ref: "tests/phase66/test_admission.py#Phase66AdmissionTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Record and verification contracts: registry fields, input/h1 rows, scores and comparisons, stride-thinned trace equal to the full fit at the registered steps, verify refusals"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_records.py#Phase66RecordTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Phase 65 evidence byte-identical: four unedited pin digests, the smoke identity at the record commit, the 11 preserved hashes, and the live smoke refusal recorded"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_historical.py#HistoricalPhase65Tests"
        status: pass
      - kind: cli
        ref: "diagnostic_fit check-registration on the smoke registration (exit 2, names only pinn/verification/diagnostic_fit.py)"
        status: pass
    human_judgment: false
duration: 18min
completed: 2026-11-01
status: complete
---

# Phase 66: Small-Network Control — Plan 01 Summary

**EXP-01's 1-hidden-layer 384-wide network (first_omega_0 1000) is admitted through the unchanged Phase 65 admission door from a separate sealed-registry copy, launched behind a fail-closed AC-power gate, recorded with a bounded loss-trace stride, and verified end to end on synthetic data, with every Phase 65 refusal, digest and evidence file intact.**

## Performance
- **Duration:** about 18 minutes (16:33Z–16:51Z)
- **Started:** 2026-11-01T16:33:07Z (PLAN_START_SHA `c919194d5496847ad4b62e88cb0d75b3b0144580`)
- **Completed:** 2026-11-01T16:51Z
- **Tasks:** 2 of 2
- **Files modified:** 9 (8 created, 1 modified)

## Accomplishments
- `pinn/verification/diagnostic_phase66.py`: `EXP01_VARIANT` (depth 1, width 384, `first_omega_0` 1000.0, locked rate/window/hidden frequency — D-04, D-05, D-06; 157,065 parameters against the locked 795,657), `PHASE66_REGISTRY = register_variant(EXP01_VARIANT, into=REGISTRY)`, the closed `REGISTRIES` table, `NEAR_BAND = 0.05` (D-09), `tier1_e_max` (read from the frozen scorecard, never retyped) and `classify_exp01`.
- `pinn/verification/diagnostic_power.py`: fail-closed `power_source`/`require_ac_power` (anchored first-line match; OSError, timeout, nonzero exit or any non-`AC Power` source refuses before anything is created), the exclusive canonical redacted `power-gate.json` receipt (repo-relative paths, load average, no interpreter path), and `launch`/`main` composing `caffeinate -is <interpreter> -B -m pinn.verification.diagnostic_fit run` as a fixed-argv child with no shell and the repository root as cwd.
- The `diagnostic_fit.py` extension, confined to the six declared sites: A the `REGISTRIES` import; B the `_named_registry` helper and the registry-aware `validate_smoke_settings` lookup (absent/null keeps the sealed catalog; unknown or non-string names refuse before any access); C the `variant_registry` keyword and record fields (`registered` is membership in the selected registry, `registry` holds the name); D the `run_registered_smoke` pass-through; E the `verify_fit_result` registry check; F the `loss_trace_stride` (admitted in settings, validated before the model is built, thinning only the recorded trace while every in-memory count is unchanged, passed through by `run_registered_smoke`, and re-checked by `verify_fit_result` for stride, trace length and last entry).
- The `tests/phase66/` package (30 tests): the end-to-end tracer with shared helpers, the catalog contract, the full admission matrix, the record/verify contracts, and the Phase 65 preservation and historical-identity checks.

## Task Commits
1. **Task 66-01-01 RED: failing phase 66 tracer** - `ca4147cc` (test) — tests/phase66/__init__.py + test_tracer.py; observed failure: `unknown diagnostic variant 'exp01-d1-w384-o1000'; registered: ['locked-12']` at the admission door (unittest exit 1, RED evidence verdict `RED_EVIDENCE_OK`, reason `target_test_failed`, machine-verified via `check tdd-red-evidence`).
2. **Task 66-01-01 GREEN: harness commit** - `332bd963` (feat) — the two new modules and the six-site `diagnostic_fit.py` edit. **This is the harness commit that first changed `diagnostic_fit.py`** (`4884a1a5a2d0f0356ff142b5bb2ba6b438bdf5e11dd8425f1ec73493c4e7b273` live), after which the Phase 65 smoke registration is historical.
3. **Task 66-01-02: contract modules** - `32e7409d` (test) — the four contract modules; no `diagnostic_fit.py` site needed a change.

## Files Created/Modified
- `pinn/verification/diagnostic_phase66.py` - the EXP-01 catalog, registry copy, name table and reading rule (new)
- `pinn/verification/diagnostic_power.py` - the AC-power launch gate, receipt and launcher (new)
- `pinn/verification/diagnostic_fit.py` - the six-site registry/stride extension (modified; all other lines unchanged)
- `tests/phase66/__init__.py`, `test_tracer.py`, `test_catalog.py`, `test_admission.py`, `test_records.py`, `test_historical.py` - the phase 66 package (new)

## Pre-edit and post-edit Phase 65 smoke checks

Last live passes before the harness edit (HEAD `c919194d5496847ad4b62e88cb0d75b3b0144580`, 2026-11-01T16:33:12Z, metadata-only; no corpus, no weights):

- `check-registration --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json` → `CHECK-REGISTRATION-OK registration-commit=ac4358cbe61159c0a4663c9e719f19a43182edfb` (exit 0)
- `verify-result --registration …smoke-registration.json --result …1632-smoke/record.json` → `VERIFY-RESULT-OK` (exit 0)

Post-edit refusals (HEAD `32e7409dcc2fc5856e82398a447b1fd40ad8f465`, 2026-11-01T16:48:36Z):

- `check-registration` → `FIT-REFUSED: registration artifact changed since it was committed: pinn/verification/diagnostic_fit.py (4884a1a5a2d0f0356ff142b5bb2ba6b438bdf5e11dd8425f1ec73493c4e7b273 != b00e45b460b8d60ee9dfabf9a1e74f09828f83e798d324947cabed5bea34c2cd)` (exit 2)
- `verify-result` → the same `FIT-REFUSED` line (exit 2)

Both refusals name only `pinn/verification/diagnostic_fit.py` — the guard working as designed, with every other pinned digest still agreeing.

## Phase 65 smoke registration: historical from 332bd963

From the feat(66-01) harness commit `332bd963` the Phase 65 smoke registration (`.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json`, bytes `ba54e8124a33bb8b172256c6c7150b1f37e3dde1c52c682635bc49e169140d8e`) no longer admits against the live tree, exactly as `65-CLOSEOUT.md` lines 86–89 anticipate ("If their implementation touches a pinned dependency, it must use a fresh registration; historical smoke evidence stays unchanged"). Its historical identity is proven by `tests/phase66/test_historical.py` at the commit that added the smoke record (found by `--diff-filter=A`, not hard-coded): all five code-dependency digests (including `diagnostic_fit.py` at `b00e45b4…`) and the registration bytes (`ba54e812…`, the record's `registration.sha256`) hold at that anchor, and the record still verifies against the committed bytes. The smoke's last live pass and first live refusal are quoted above. No Phase 65 artifact was edited, re-pinned or re-committed (`git status --porcelain` on the phase 65 directory is empty at every commit).

The only other Phase 65 registration that pins `pinn/verification/diagnostic_fit.py` is the probe registration `evidence/probe/expectations.json` (its code_dependencies entry for that file pins `2e2c06eb5bb294e37147e76505db9d9288778d201bcd460e69d5e0ff5e7c52ca` — the digest the plan names, listed 4th of five in the document). Its live check already refused before Phase 66 (`65-CLOSEOUT.md` line 109: PROBE-REFUSED, exit 2, live fit dependency differs), so it was already historical; it stays historical, and this plan neither runs nor changes that check.

**Decision carried (plan "Decisions this plan carries", decision 1):** the digest-pinned `diagnostic_fit.py` is edited because the registry lookup lives in `validate_smoke_settings`, which every admission path reaches; the non-editing alternatives (a ~300-line clone of the admission/supervision/verification code, or rebinding module globals across the spawn boundary) are worse. Confined to about 45 lines across the six sites, with the safeguards that the other four smoke-pinned modules stay byte-identical and the 11 Phase 65 evidence files stay unchanged.

**Reuse-condition stance (decision 2):** WR-01 is a precondition for graded use only (D-11). WR-02 and WR-05 govern new probe registrations; Phase 66 registers fits. WR-03 and WR-04 stay deferred: Phase 66 runs `verify-result` only on records its own harness wrote at its own registered paths, and a traceback there is a failure, never a success. WR-06 is not triggered (same loader and time transform). IN-01 is not triggered: the schema literal stays `phase65-fit-registration/v1`, the window endpoints stay numeric, and the two new keys (`variant_registry`, `loss_trace_stride`) are validated strictly.

**The four unedited digests (live == smoke registration's code_dependencies):**

| Module | SHA-256 |
|---|---|
| `pinn/verification/diagnostic_guard.py` | `8dd577a263c28bf7886a0795336ac613fe3fde7c8ebf424fcd6eaf2e80fef540` |
| `pinn/verification/diagnostic_data.py` | `47b9d99dd991c2a899cb8a4308273643c1d98ea591b851546373e44bcf429836` |
| `pinn/verification/diagnostic_variants.py` | `ad8ed66c43a8d6edbef15e794f4f06af194a99729acd103428c25bd6cd0c5dfb` |
| `pinn/verification/diagnostic_similarity.py` | `e80079b62485f04c7c42a513913ef392d7201eea625ff496bae432d0c440d4b7` |

## Decisions Made
- The launcher passes the resolved absolute registration and output paths in the child argv (cwd-independent, so the in-process test and the detached production run resolve identically); the receipt holds repo-relative paths only, which is what the redaction guard requires.
- `fit_diagnostic` resolves the named registry and validates the loss-trace stride immediately after the steps/warmup validation, before the model is built — the fail-closed reading of Sites C and F (a bad value then refuses before any data access, optimizer work or weights write, not at record-assembly time).
- `phase66_settings` builds the EXP-01 variant block through the sealed Phase 65 `DiagnosticVariant` class rather than importing the Phase 66 catalog, so the RED run fails at the sealed-catalog door exactly as the plan predicts; admission's byte-agreement loop ties the block to `EXP01_VARIANT`, and `test_catalog` pins the same fields.
- The unused `VariantRefused` import (whose only use was the replaced `try/resolve_variant/except`) was removed with Site B.

## Deviations from Plan
- **[Tracer detail] The tracer AC test needed the VerifyResultTests access-attestation shim** — **Found during:** Task 66-01-01 GREEN. **Issue:** the fixture context carries no attestation summary and its reader has no `access_summary`, so `verify_fit_result` refused the published record ("carries no access attestation; no Stage-0 access summary"). **Fix:** the AC case applies the exact `VerifyResultTests.setUp` shim (a summary-capable attestation and a Stage-0 style reader summary) before launching; no harness file changed. **Files modified:** tests/phase66/test_tracer.py. **Verification:** tracer OK; verify returns verified. **Committed-in:** `332bd963`.
- **[Test bug] `test_the_loss_trace_stride_matrix` popped a key `phase66_settings` never sets** — **Found during:** Task 66-01-02. **Issue:** KeyError on `absent.pop("loss_trace_stride")`. **Fix:** use the settings as built (the key is absent by construction). **Files modified:** tests/phase66/test_admission.py. **Verification:** 28 tests OK. **Committed-in:** `32e7409d`.

No harness site changed after the GREEN commit: `git diff 332bd963..32e7409d -- pinn/` is empty, so the plan's `test(66-01)` subject applied (not `fix(66-01)`), and the harness commit named in the SUMMARY is the GREEN commit `332bd963`.

## Issues Encountered
- The tracer's argv assertion initially compared unresolved temp paths (`/var/folders/...`) against the launcher's resolved forms (`/private/var/...`); the test now asserts the resolved absolute paths. Resolved inside Task 66-01-01 GREEN, committed in `332bd963`.
- The pre-existing PyTorch `float(loss)` UserWarning at `diagnostic_fit.py:681` appears in the Phase 65 suite as before (recorded at `65-CLOSEOUT.md` lines 116–118); pre-existing, untouched.

## Verification (measured)
- `tests.phase66.test_tracer -v`: 2 tests, OK (AC case and battery case both in the listing); re-run on the committed tree before expansion (tracer gate).
- `tests.phase66` four contract modules `-v`: 28 tests, OK in 12.106 s (27 passed immediately; the one error was the test bug fixed above).
- `unittest discover -s tests/phase65 -t .`: **204 tests, OK** — 34.970 s after Task 1, 31.060 s after Task 2 (the 204 of `65-CLOSEOUT.md` line 105).
- `unittest discover -s tests/phase66 -t .`: 30 tests, OK in 12.484 s (under the 30 s expectation).
- `load_protocol()`: `PROTOCOL-OK` (all 33 pinned digests unchanged; `diagnostic_fit.py` is not one of them).
- `CATALOG-OK` inline assertion (sealed `REGISTRY` exactly `['locked-12']`; `PHASE66_REGISTRY` `['locked-12', 'exp01-d1-w384-o1000']`; `REGISTRIES` `['phase66']`).
- Post-edit smoke compound check: check-registration exits 2 naming only `pinn/verification/diagnostic_fit.py`; verify-result exits 2 with the same refusal.
- `git diff c919194d..HEAD -- diagnostic_guard.py diagnostic_data.py diagnostic_variants.py diagnostic_similarity.py` empty; `git diff --check` clean at every commit.

## Next Phase Readiness
- Plan 66-02 can build directly on the committed harness: `EXP01_VARIANT`, `REGISTRIES`, `classify_exp01`/`tier1_e_max`, `diagnostic_power.launch/main` (Plan 66-02 adds the `check` subcommand, the output-exists and admission prechecks and the full refusal matrix), and the Site F stride contract (`settings.loss_trace_stride`, ceil-to-10,000 per plan 66-02). The `tests/phase66` helpers (`phase66_settings`, `phase66_fixture_registration`, `patch_data_seam`, `inline_supervisor`, `fake_pmset`) are importable by name.
- **Freeze rule now in force:** any further edit to `pinn/verification/diagnostic_fit.py`, `diagnostic_phase66.py` or `diagnostic_power.py` after the first Phase 66 registration is written retires that registration's live admission and forces a fresh registration. Finish all harness work (Plan 66-02) before the first page/registration pair.
- The Phase 65 smoke registration is historical from `332bd963`; Phase 66 runs use fresh committed registrations (D-11). The held-out evaluation remains unspent; no real orbit was opened and no MPS work ran in this plan.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01*
