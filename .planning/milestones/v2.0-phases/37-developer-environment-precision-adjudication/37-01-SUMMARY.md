---
phase: 37-developer-environment-precision-adjudication
plan: "01"
subsystem: testing
tags: [unittest, stdlib, hermetic, env-contract, ad-contract, precision-contract]

requires: []
provides:
  - "Six stdlib-only tests/phase37 modules encoding the executable contracts for ENV-01..04 and CTX-01..14"
  - "Hermetic bootstrap fixture (fake uname/sw_vers/conda/curl/shasum/bash) with temporary HOME and prefixes"
  - "Lock-boundary contract proving seed is the only first-lock route and default setup fails closed without a lock"
  - "CTX-06 fingerprint schema/allowlist, secret-canary exclusion, and exclusive non-overwrite contract"
  - "ENV-04 two-profile resolver contract with global-dtype-immutability and no-availability-inference guards"
  - "ENV-03 §10.3 componentwise-AD scientific contract preserving u=0.3, analytical derivatives, and the 1e-6 criterion for both full_jacobian and scalar_u_jvp"
  - "Dual-arm precision orchestrator contract for subprocess isolation, structured failure retention, and verdict-free rendering"
affects:
  - "37-02 (Wave 1) turns the bootstrap/lock/fingerprint contracts green"
  - "37-03 (Wave 2) turns the runtime and AD-worker contracts green"
  - "37-04 (Wave 3) turns the orchestrator/evidence contracts green"
  - "37-05 (Wave 4) runs the validated dual-arm evidence and stops for owner D1-p"

tech-stack:
  added: []
  patterns:
    - "Stdlib-only hermetic subprocess tests with fixture-owned fake tools and temporary HOME/prefixes"
    - "Production-target imports kept inside test methods so py_compile is the only Wave 0 green condition"
    - "Source-inspection tests for forbidden behaviors (shell=True, global dtype mutation, availability inference)"

key-files:
  created:
    - "tests/phase37/__init__.py — package marker and Wave 0 contract preamble"
    - "tests/phase37/test_setup_contract.py — bootstrap state machine + lock boundary (CTX-01..05)"
    - "tests/phase37/test_environment_fingerprint.py — fingerprint schema/hashing/secrecy/non-overwrite (CTX-06/07)"
    - "tests/phase37/test_runtime.py — two-profile resolver and no-global-default (CTX-12..14)"
    - "tests/phase37/test_componentwise_ad.py — §10.3 fixture and 10/30/100 timing protocol (CTX-08..10)"
    - "tests/phase37/test_precision_orchestrator.py — dual-arm isolation, structured failure, verdict-free (CTX-08/10/11/13/14)"
  modified: []

key-decisions:
  - "Wave 0 produces no production code, package install, environment, or evidence — only the executable contract that later waves satisfy"
  - "Non-stdlib imports (torch, production modules) live inside test methods and skip cleanly when the production target is absent, so module compilation is the only Wave 0 green condition"
  - "The §10.3 fixture (u=0.3, [sin(2pi u), cos(2pi u), u^2], analytical [2pi cos(2pi u), -2pi sin(2pi u), 2u], aggregate < 1e-6) is preserved verbatim from the v1.4 Phase 21 probe"

patterns-established:
  - "Hermetic bootstrap fixture: fake uname/sw_vers/conda/curl/shasum/bash under a fixture PATH, with isolated HOME and owned prefixes; never contacts network or host conda"
  - "Source-inspection tests assert forbidden behaviors are absent (shell=True, torch.set_default_dtype, is_available, retry, --profile selector) — structural guards that do not require the production code to run"

requirements-completed: []

coverage:
  - id: D1
    description: "Six tests/phase37 modules compile with host python3 using stdlib-only module-level imports"
    requirement: "ENV-01"
    verification:
      - kind: unit
        ref: "python3 -m py_compile tests/phase37/{__init__,test_setup_contract,test_environment_fingerprint,test_runtime,test_componentwise_ad,test_precision_orchestrator}.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "tests/phase37 discovery runs cleanly on host python3 (no errors); production-target tests skip pending later waves"
    requirement: "ENV-01"
    verification:
      - kind: unit
        ref: "python3 -m unittest discover -s tests/phase37 -p 'test_*.py' → 55 tests, 0 errors, 0 failures, 50 skipped"
        status: pass
    human_judgment: false

duration: ~25min
completed: 2026-07-12
status: complete
---

# Phase 37 Plan 01: Wave 0 Verification Contract Summary

**Six stdlib-only `tests/phase37/` modules encoding the executable ENV-01..04 / CTX-01..14 contracts before any host mutation, package install, or empirical MPS run**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 (37-01-01 bootstrap/lock/fingerprint; 37-01-02 runtime/AD/orchestrator)
- **Files created:** 6 (package marker + 5 test modules)

## Accomplishments

- Hermetic bootstrap fixture (`_make_fixture_repo`) with fake `uname`, `sw_vers`, `conda`, `curl`, `shasum`, `bash` under a fixture-owned PATH plus isolated HOME, install prefix, and target prefix. Wave 0 never contacts a network, host conda, a real installer, or MPS.
- `BootstrapContractTests` (8 cases) covers Darwin/arm64 rejection before download, occupied/incompatible prefix refusal without deletion or update, no shell-startup mutation, and the explicit activation handoff.
- `TestLockBoundary` (4 cases) proves the three lock states stay separated: explicit `--seed` creates only a disposable task-owned prefix and removes it; default setup fails before target creation when the committed lock is absent and never dispatches seed or refresh; ordinary setup preserves YAML/lock bytes.
- `EnvironmentFingerprintTests` (7 cases) asserts the CTX-06 field allowlist, deterministic sorted-key canonical JSON with final newline, byte-exact lock SHA-256, Markdown derived from the same object, secret-canary exclusion under every key, `--check-only` writes nothing, and exclusive non-overwriting run IDs.
- `RuntimeResolverTests` (12 cases) locks the exact two-profile matrix (`float32/mps`, `float64/cpu`), frozen `RuntimeSpec`, fail-closed on every other pair (including the cross-pairs `float64/mps` and `float32/cpu`), no global-dtype mutation, and source-inspection guards forbidding availability inference, retry, and `torch.set_default_dtype`.
- `ComponentwiseADTests` (11 cases) preserves the §10.3 fixture (`u=0.3`, `[sin(2πu), cos(2πu), u²]`, analytical `[2πcos(2πu), -2πsin(2πu), 2u]`, aggregate `< 1e-6`), requires both `full_jacobian` and `scalar_u_jvp` to share the trajectory and return the analytical vector, the locked 10/30/100 timing protocol, six summary statistics plus raw samples, and fallback capture before any Torch import.
- `PrecisionOrchestratorTests` (15 cases) locks subprocess isolation through one fixed-argv worker module (no shell, no profile selector, no in-process Torch import), removal of `PYTORCH_ENABLE_MPS_FALLBACK` from the MPS child env, structured arm records for timeout/signal/malformed-JSON/device-mismatch/fallback-leakage, exclusive atomic non-overwriting evidence, byte-identical deterministic rendering, and the verdict-free contract — the fixed `Owner decision required; no D1-p verdict is recorded by this report.` statement plus forbidden words (`winner`, `recommend`, `faster`, `preferred`, …).

## Files Created/Modified

- `tests/phase37/__init__.py` — package marker and Wave 0 contract preamble
- `tests/phase37/test_setup_contract.py` — `BootstrapContractTests` + `TestLockBoundary` (CTX-01..05)
- `tests/phase37/test_environment_fingerprint.py` — `EnvironmentFingerprintTests` (CTX-06/07, T-37-04)
- `tests/phase37/test_runtime.py` — `RuntimeResolverTests` (CTX-12..14, T-37-05)
- `tests/phase37/test_componentwise_ad.py` — `ComponentwiseADTests` (CTX-08..10, T-37-06)
- `tests/phase37/test_precision_orchestrator.py` — `PrecisionOrchestratorTests` (CTX-08/10/11/13/14, T-37-07)

## Decisions Made

- Kept `import torch` and all production-module imports inside test methods (per the plan's `<action>` text), and added a `_load_torch()` helper that skips cleanly when torch is absent — so the Wave 0 suite is RED-only-on-missing-targets rather than RED-on-missing-torch-dependency. An `ImportError` from a missing dependency is an environment failure, not a production-target miss.
- Used AST-based verification that module-level imports are stdlib-only, and that non-stdlib imports are confined to function bodies.
- No production code, package install, environment, or evidence run was created. The suite cannot turn an invalid arm or an absent owner record into a precision choice.

## Deviations from Plan

None — plan executed exactly as written. The plan's `<verify>` block specified `py_compile` as the Wave 0 green condition; additionally ran the full `unittest discover` to confirm clean skips (50 of 55 tests skip pending later-wave targets; 5 host-state bootstrap tests pass).

## Issues Encountered

None.

## Next Phase Readiness

- Wave 0 is GREEN: all six modules compile and the discovery suite runs without errors.
- Wave 1 (37-02) can now implement `setup.sh`, `scripts/refresh-environment-lock.sh`, `scripts/lib/conda_bootstrap.sh`, `scripts/verify_environment.py`, `environment.yml`, and `requirements-lock.txt` against the contracts in `test_setup_contract.py` and `test_environment_fingerprint.py`. Wave 1 begins with a blocking human-verify checkpoint (PyPI package-identity review) and then performs a real Miniforge/PyTorch seed install on the M5 Pro — both are out of Wave 0 scope.

---
*Phase: 37-developer-environment-precision-adjudication*
*Completed: 2026-07-12*
