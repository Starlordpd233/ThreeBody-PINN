---
phase: 55-architecture-characterization-probe
plan: 04
subsystem: testing
tags: [pinn, verification, architecture-characterization, exact-value-fixture, evidence, inst-04]

requires:
  - phase: 55-architecture-characterization-probe
    provides: SweepCase, ArchitectureCharacterizationResult, DEFAULT_CASES, measure_case, run_sweep, main
affects: [56-contract-amendment-train-free-gate]

provides:
  - tests/phase55/fixtures/six_case_baseline.json D-01 tier-2 six-row exact-value baseline with _meta provenance
  - test_exact_value_fixture plus fail-first and sha256 immutability tests
  - one committed zero-argument evidence run under evidence/probe/20260906T035209Z
  - audit §6b decade-resolution cross-check recorded here

actuals:
  tokens: 10721
  tasks: 3
  commits: 4
plan_head_before: 59b983c25c34de281d2a38a85fc2e1968a652b03

tech-stack:
  added: []
  patterns:
    - residual_probe JSON serialization (sort_keys, indent=2) for a committed numeric fixture
    - read-only per-field comparison at a recorded relative tolerance
    - session-scoped sha256 autouse so the suite cannot heal its own baseline

key-files:
  created:
    - tests/phase55/fixtures/six_case_baseline.json
    - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json
    - .planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md
  modified:
    - tests/phase55/test_architecture_characterization.py
    - .planning/phases/55-architecture-characterization-probe/55-VALIDATION.md

key-decisions:
  - "D-01 tier 2: pin the full six-row output at relative_tolerance=1e-9; regenerate only by explicit operator action"
  - "SC2 agreement is decade/order-of-magnitude, not bit-for-bit, because the original ad-hoc sampling scheme is unrecoverable (RESEARCH.md A1)"
  - "Committed evidence run records git_worktree_dirty=true honestly; user-owned dirty paths were not cleaned"

patterns-established:
  - "Pattern: fixture _meta carries regeneration command, runtime, torch/numpy versions, median convention, IC13 RNG scheme, and tolerance"
  - "Pattern: comparison failure names case, field, both values, and recorded-versus-running dependency versions"

requirements-completed: [INST-04]

coverage:
  - id: D1
    description: Committed six-row exact-value fixture with _meta provenance is compared field-for-field at 1e-9
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_exact_value_fixture
        status: pass
    human_judgment: false
  - id: D2
    description: Perturbing a copy of the baseline fails the comparison; the on-disk sha256 is unchanged across the suite
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_fixture_comparison_fails_on_a_perturbed_baseline
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_fixture_file_is_never_written_by_the_suite
        status: pass
    human_judgment: false
  - id: D3
    description: One committed zero-argument CLI evidence run records command, git tree state, and the full six-row output
    requirement: INST-04
    verification:
      - kind: other
        ref: .venv/bin/python -m pinn.verification.architecture_characterization_probe
        status: pass
    human_judgment: false
  - id: D4
    description: Reproduction matches the 2026-08-17 audit §6b table at decade resolution with front_idx=0 and R̄ in the 10^10 decade
    requirement: INST-04
    verification:
      - kind: other
        ref: 55-04-SUMMARY.md audit cross-check table
        status: pass
    human_judgment: false

duration: 21min
completed: 2026-09-06
status: complete
---

# Phase 55 Plan 04: Exact-Value Fixture and Re-derivable Evidence Run Summary

**Pinned six-row float64/CPU initialization baseline compared at 1e-9, proven unable to rewrite itself, plus one committed zero-argument CLI run that reproduces the 2026-08-17 audit §6b table at decade resolution**

## Performance

- **Duration:** 21 min
- **Started:** 2026-09-06T03:45:10Z
- **Completed:** 2026-09-06T04:06:00Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- `tests/phase55/fixtures/six_case_baseline.json` holds the full six-row `run_sweep()` output (identity, six medians, causal weights, front_idx, runtime fields) plus `_meta` naming the regeneration command, UTC generation time, precision/device/`n_col`, Torch 2.12.0, NumPy 2.2.0, `MEDIAN_CONVENTION`, the IC13 RNG scheme, `relative_tolerance=1e-9`, and the explicit-operator-only purpose.
- `test_exact_value_fixture` recomputes the shared module-scoped sweep and compares every listed field at the fixture's own tolerance. A 1.01× perturbation of median `R̄` raises; the on-disk sha256 `65edebc78d334c76e532a15d75bb6ca70ee4a3094f68b66804ad12d4372bc474` is unchanged across `pytest tests/phase55/`.
- One committed evidence run at `evidence/probe/20260906T035209Z/` was produced by `.venv/bin/python -m pinn.verification.architecture_characterization_probe` with no extra flags (`n_col=16`, float64/CPU). `raw.json` records `argv=[]`, command, git sha `2b1a4fd1490bba817639485063888b49a365b90d`, `git_available=true`, and `git_worktree_dirty=true`.
- No 4096-structure measurement was run and nothing is presented as `R_ref`. The 55-03 helpers remain unreachable from the default sweep.

## Task Commits

Each task was committed atomically:

1. **Task 1: Generate and commit the Tier-2 exact-value baseline** - `d5bd6f5b` (test)
2. **Task 2 RED: Add failing exact-value fixture tests** - `f5c68155` (test)
3. **Task 2 GREEN: Compare exact-value fixture without self-heal** - `2b1a4fd1` (test)
4. **Task 3: Produce, commit and audit-cross-check the reproduction run** - `912c3193` (evidence)

**Plan metadata:** pending this SUMMARY commit

## Files Created/Modified

- `tests/phase55/fixtures/six_case_baseline.json` - D-01 tier-2 baseline; read-only by the suite
- `tests/phase55/test_architecture_characterization.py` - `FIXTURE_PATH`, `_load_fixture`, `_compare_case_to_fixture`, three Tier-2 tests, session sha256 autouse
- `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json` - SC2 provenance + six full result records
- `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md` - human-readable §6b-layout table
- `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md` - `wave_0_complete: true`; 55-04-T2, 55-04-T3, and `all` rows green

## Decisions Made

- Relative tolerance is `1e-9` because the arm is deterministic (fixed seed, float64, CPU, no training). A future failure should first compare recorded vs running Torch/NumPy versions.
- `requirements-lock.txt` currently pins Torch 2.12.1 and NumPy 2.4.6 while this checkout runs 2.12.0 and 2.2.0. That drift predates Phase 55 and is not resolved here; it is why `_meta` stores the generating versions.
- The evidence dirty flag is `true` because user-owned modified/untracked paths (`.planning/config.json`, docs work artifacts, `.agents/`, `.gsd/`, `.planning/tmp/`, and others listed in the executor prompt) were left untouched. The flag is honest rather than suppressed.

## Audit §6b cross-check (ROADMAP SC2)

Source: `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` §6b versus committed `evidence/probe/20260906T035209Z/summary.md`. Agreement is asserted at decade / order-of-magnitude resolution (RESEARCH.md A1): the original ad-hoc collocation-sampling scheme was never written to the repository.

| seed / IC | ‖r′‖ audit / repro | ‖v′‖ audit / repro | ‖a′‖ audit / repro | ‖F_grav‖ audit / repro | min sep audit / repro | `R̄` audit / repro | `front_idx` audit / repro |
|---|---|---|---|---|---|---|---|
| 41, m=(1,1,1), IC13=0 | 1.28 / 1.085 | 310 / 251.8 | 2.03×10⁵ / 1.975×10⁵ | 2.17 / 3.131 | 0.91 / 0.784 | 1.37×10¹⁰ / 1.301×10¹⁰ | 0 / 0 |
| 42 | 1.13 / 1.009 | 331 / 313.5 | 2.72×10⁵ / 2.411×10⁵ | 3.29 / 4.41 | 0.67 / 0.6072 | 2.46×10¹⁰ / 1.938×10¹⁰ | 0 / 0 |
| 43 | 0.97 / 0.8298 | 251 / 297.9 | 2.20×10⁵ / 2.078×10⁵ | 3.24 / 5.913 | 0.72 / 0.5815 | 1.62×10¹⁰ / 1.440×10¹⁰ | 0 / 0 |
| 0 | 0.91 / 0.9759 | 281 / 301.8 | 2.79×10⁵ / 2.040×10⁵ | 5.94 / 5.803 | 0.50 / 0.5542 | 2.60×10¹⁰ / 1.387×10¹⁰ | 0 / 0 |
| 7 | 0.85 / 1.083 | 290 / 239.4 | 1.94×10⁵ / 2.027×10⁵ | 5.89 / 3.616 | 0.51 / 0.6767 | 1.25×10¹⁰ / 1.370×10¹⁰ | 0 / 0 |
| 41, m=(1,0.8,0.6), random tanh IC13 | 0.95 / 1.124 | 231 / 327.4 | 2.28×10⁵ / 1.917×10⁵ | 2.85 / 2.807 | 0.72 / 0.7188 | 1.74×10¹⁰ / 1.224×10¹⁰ | 0 / 0 |

ROADMAP SC2 claims, observed:

1. **`front_idx == 0` in every row.** Observed: `[0, 0, 0, 0, 0, 0]`.
2. **Median `R̄` in the 10^10 decade in every row.** Observed: `1.224×10¹⁰` … `1.938×10¹⁰`, all inside `1e9 < R̄ < 1e11`.
3. **The other five columns stay inside the audit's own decade.** Every audit/repro pair is within a factor of 0.53–1.83 (all well inside 10×). Two `‖r′‖` rows (seed 7: 0.85 vs 1.083; variable-mass: 0.95 vs 1.124) straddle `floor(log10)=0` at the 1.0 boundary; both remain O(1), matching the audit table's own `‖r′‖` span of 0.85–1.28. No column is outside order-of-magnitude agreement, so the claim is not widened.

## Deviations from Plan

None - plan executed exactly as written.

### Execution notes (non-blocking)

**1. [process] Task 2 used a RED then GREEN commit pair**
- **Found during:** Task 2 (`tdd="true"`)
- **Issue:** Helpers were absent, so the new tests failed with `NameError: _load_fixture`.
- **Fix:** RED commit `f5c68155`, then GREEN helpers and validation-row flip in `2b1a4fd1`.
- **Impact:** Required by task-level TDD; no production-code change.

**2. [process] Full-suite before/after uses the 55-01 failure count as before**
- **Found during:** Task 3
- **Issue:** A second 10-minute `pytest tests/ -q` before Task 1 would have duplicated an expensive command whose production inputs this plan does not change (`pinn/` untouched).
- **Fix:** After-run retained at `/tmp/gsd-55-04-full-pytest/` (started 2026-09-06T03:54:16Z, elapsed 601s, exit 1): `51 failed, 1629 passed, 3 skipped`. 55-01 recorded `51 failed, 1611 passed, 3 skipped`. Failure count unchanged; passed +18 from Phase 55 tests. Zero `tests/phase55/` failures. The 14 STATE.md phase43/watchdog failures remain inside the 51; the rest are archived-milestone / spec-history tests (`phase38` spec SHA, `phase47`, `phase49`, `phase50`).
- **Impact:** Matches the plan's "no failure beyond the documented pre-existing set" intent.

---

**Total deviations:** 0 auto-fixed. 2 documented process notes.
**Impact on plan:** None on shipped behavior.

## Issues Encountered

- Zero-argument CLI records `argv=[]` and `command="python -m pinn.verification.architecture_characterization_probe"`. The plan's `bool(pr.get('argv'))` snippet is False for an empty list; the plan `<verify>` assertion `pr.get('argv') is not None` is the correct SC2 check and passed.
- `REQUIREMENTS.md` INST-04 checkbox is not flipped. This plan copies `[INST-04]` into `requirements-completed` per the SUMMARY contract; the checkbox remains a phase-verification act, matching 55-01..03.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 55 plans 1–4 are executed. Ready for `/gsd-verify-work 55`.
- Phase 56 remains closed until that verification. Do not wire the 55-03 4096 helpers into the default sweep. Do not treat this 16-point `R̄` as `R_ref`.

## Self-Check: PASSED

- FOUND: `tests/phase55/fixtures/six_case_baseline.json`
- FOUND: `tests/phase55/test_architecture_characterization.py`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md`
- FOUND: `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json`
- FOUND: `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/summary.md`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-04-SUMMARY.md`
- FOUND: commit `d5bd6f5b` test(55-04): pin six-row exact-value baseline fixture
- FOUND: commit `f5c68155` test(55-04): add failing exact-value fixture tests
- FOUND: commit `2b1a4fd1` test(55-04): compare exact-value fixture without self-heal
- FOUND: commit `912c3193` evidence(55-04): record zero-argument six-row reproduction
- FOUND: `.venv/bin/python -m pytest tests/phase55/ -q` — 46 passed
- FOUND: fixture sha256 `65edebc78d334c76e532a15d75bb6ca70ee4a3094f68b66804ad12d4372bc474` unchanged after the phase55 suite
- FOUND: exactly one evidence directory `20260906T035209Z` with `raw.json` and `summary.md`

---
*Phase: 55-architecture-characterization-probe*
*Completed: 2026-09-06*
