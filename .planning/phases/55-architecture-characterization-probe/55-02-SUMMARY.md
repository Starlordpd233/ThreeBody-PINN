---
phase: 55-architecture-characterization-probe
plan: 02
subsystem: testing
tags: [pinn, verification, architecture-characterization, cli, evidence, inst-04]

requires:
  - phase: 55-architecture-characterization-probe
    provides: SweepCase, ArchitectureCharacterizationResult, DEFAULT_CASES, measure_case, run_sweep
affects: [56-contract-amendment-train-free-gate, 55-03, 55-04]

provides:
  - argparse main() with defaulted --precision/--device so zero-argument invocation reproduces the six audited rows
  - load_cases_config validate-before-construct JSON case-list parser
  - atomic non-overwriting evidence writer (raw.json + summary.md) with SC2 provenance
  - documented Phase-38 _EXCLUDE_SUFFIXES entry for the defaulted precision seam

actuals:
  tokens: 8465
  tasks: 3
  commits: 3
plan_head_before: 6d4f96998bae7ab5de0046c59aad57f43507d4d5

tech-stack:
  added: []
  patterns:
    - residual_probe argparse main(argv) with D-02 defaulted precision/device
    - atomic_write_text for evidence (tmp + fsync + os.replace + parent-dir fsync)
    - git_head plus bounded git-status dirty probe for SC2 tree-state provenance
    - validate-before-construct --cases-config (fixture_loader idiom)

key-files:
  created: []
  modified:
    - pinn/verification/architecture_characterization_probe.py
    - tests/phase55/test_architecture_characterization.py
    - tests/phase38/test_prohibitions.py
    - .planning/phases/55-architecture-characterization-probe/55-VALIDATION.md

key-decisions:
  - "D-02 CLI: --precision default float64, --device default cpu, not required"
  - "Exit code encodes measurement completion only, never a recipe verdict"
  - "Phase-39 _LEGACY entry not required: the probe does not parse the corpus"

patterns-established:
  - "Pattern: load_cases_config validates every JSON field before SweepCase construction; __post_init__ is the second net"
  - "Pattern: _new_run_dir exclusive UTC stamp plus suffix retry; both files go through atomic_write_text"
  - "Pattern: Phase-38 glob carve-out is one documented per-file exclusion, with non-precision guarantees re-homed in tests/phase55"

requirements-completed: [INST-04]

coverage:
  - id: D1
    description: Zero-argument module invocation reproduces the six audited DEFAULT_CASES rows at float64/CPU and exits 0
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_zero_argument_cli_reproduces_six_rows
        status: pass
    human_judgment: false
  - id: D2
    description: --cases-config drives an arbitrary case list; malformed entries raise ValueError naming the field before any run directory is allocated
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_cases_config_drives_arbitrary_case_list
        status: pass
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_malformed_cases_config_raises_value_error
        status: pass
    human_judgment: false
  - id: D3
    description: Each run writes atomic raw.json + summary.md into a non-overwriting UTC directory with the full SC2 provenance record
    requirement: INST-04
    verification:
      - kind: integration
        ref: tests/phase55/test_architecture_characterization.py#test_cli_writes_provenance_evidence
        status: pass
      - kind: integration
        ref: tests/phase55/test_architecture_characterization.py#test_cli_allocates_non_overwriting_run_dirs
        status: pass
    human_judgment: false
  - id: D4
    description: An evidence root inside simulation_data/ is rejected before any directory is created
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_evidence_root_inside_simulation_data_is_rejected
        status: pass
    human_judgment: false
  - id: D5
    description: main returns 0 on a completed measurement and non-zero only when the measurement did not complete; the evidence key set cannot grow a silent verdict field
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_cli_exit_code_is_not_a_recipe_verdict
        status: pass
    human_judgment: false
  - id: D6
    description: The probe is excluded from the Phase-38 prohibition glob by one documented _EXCLUDE_SUFFIXES entry; every other module's assertions are unchanged
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase38/test_prohibitions.py
        status: pass
    human_judgment: false

duration: 8min
completed: 2026-09-06
status: complete
---

# Phase 55 Plan 02: CLI, Config Surface, and Re-derivable Evidence Writer Summary

**Argparse CLI whose zero-argument invocation reproduces the six audited rows, a fail-closed `--cases-config` parser, and an atomic evidence writer that records command, git tree state, and full output without emitting a recipe verdict**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-06T03:19:34Z
- **Completed:** 2026-09-06T03:27:36Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- `python -m pinn.verification.architecture_characterization_probe` with no `--precision`/`--device` flags runs `DEFAULT_CASES` at float64/CPU, writes `raw.json` + `summary.md` into a freshly allocated UTC run directory, and exits 0.
- `--cases-config` JSON drives an arbitrary `(label, seed, masses, ic13_mode)` list through per-field validators; a malformed entry raises `ValueError` naming the field before any directory is created.
- `raw.json` top-level keys equal `EVIDENCE_TOP_LEVEL_KEYS` (`schema_version`, `provenance`, `configuration`, `cases`, `failure`). Provenance carries argv, command, git sha + availability, worktree dirty flag, Torch/NumPy versions, UTC timestamp, median convention, IC13 RNG scheme, and `resolve_causal_clip_facts`.
- `pinn/verification/architecture_characterization_probe.py` is in `tests/phase38/test_prohibitions.py` `_EXCLUDE_SUFFIXES` with a D-02 rationale comment. Phase 39's whole-`pinn` glob does not trip; no `_LEGACY` entry was added.

## Task Commits

Each task was committed atomically:

1. **Task 1: CLI entry point, case-config surface, and the re-derivable evidence writer** - `09c3c563` (feat)
2. **Task 2: Register the documented Phase-38 prohibition exclusion for the new probe** - `f68ddd47` (test)
3. **Task 3: CLI-contract, config-validation and evidence-provenance test coverage** - `6477099e` (test)

**Plan metadata:** pending this SUMMARY commit

## Files Created/Modified

- `pinn/verification/architecture_characterization_probe.py` - `main`, `load_cases_config`, evidence writer, provenance capture, CLI flags
- `tests/phase55/test_architecture_characterization.py` - CLI-subprocess, config-validation, provenance, non-verdict exit tests
- `tests/phase38/test_prohibitions.py` - documented `_EXCLUDE_SUFFIXES` entry
- `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md` - 55-01 and 55-02 Status rows flipped green

## Decisions Made

- Followed CONTEXT.md D-02: `--precision`/`--device` are defaulted, not required, so a zero-argument invocation is reachable.
- Exit code means "measurement completed" only. `failure` is `None` on success and `{type, message}` on exception; no threshold, health, or GATE-04 verdict field.
- Inspected `tests/phase39/test_prohibitions.py` `discover_pinn_modules` / `_LEGACY`. The probe has no corpus-path tokens, so no Phase-39 exclude entry was added.

## Deviations from Plan

### Auto-fixed Issues

None.

### Execution notes (non-blocking)

**1. [process] Task 1 TDD tests live in Task 3's files**
- **Found during:** Task 1
- **Issue:** Task 1 is `tdd="true"` but its `<files>` is only the probe module; the CLI tests are Task 3. The Task 1 `-k "cli or cases_config or evidence"` filter collected 0 tests (pytest exit 5) until Task 3 landed.
- **Fix:** Verified Task 1 with the plan's CLI assertions (`main([])` / `--evidence-root`, six-row `raw.json`, simulation_data rejection). Task 3 added the named tests; the same `-k` filter then passed 11 tests.
- **Impact:** None on shipped behavior. Matches 55-01's skip-guard analog.

**2. [process] Phase-38 spec-history tests remain pre-existing failures**
- **Found during:** Task 2
- **Issue:** `pytest tests/phase38/test_prohibitions.py -q` still fails `test_spec_byte_identity_endpoint_sha256` and `test_spec_history_no_touch_since_phase_base` (SCOPE-18 baseline vs later spec edits). These are the 55-01-documented archive failures, not caused by this plan.
- **Fix:** None. Baseline before Task 2 was the same two failures; after the exclusion, still those two. `test_no_precision_default_in_discovered_modules` and `test_no_v1_3_era_imports_in_discovered_modules` passed. Discovery no longer lists the new probe.

---

**Total deviations:** 2 documented process notes. No scope creep.
**Impact on plan:** Task 1 CLI assertions and Task 3 tests cover the same contract. Pre-existing Phase-38 spec SHA failures are unchanged.

## Issues Encountered

- `_discover_phase38_modules` tests `rel in _EXCLUDE_SUFFIXES` first, so the redundant inline four-path set did not need a matching edit.
- Tests never wrote under `.planning/phases/55-architecture-characterization-probe/evidence/` (directory absent; 55-04 owns the committed run).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for 55-03: 4096-bin / bin-mean helpers unit-tested against synthetic arrays only, with AST containment from `run_sweep`/`measure_case`/`main`.
- Do not implement those helpers in the default sweep path. Do not persist a real new-structure measurement as `R_ref`.
- Do not add 55-04 exact-value fixtures in this module yet.

## Self-Check: PASSED

- FOUND: `pinn/verification/architecture_characterization_probe.py`
- FOUND: `tests/phase55/test_architecture_characterization.py`
- FOUND: `tests/phase38/test_prohibitions.py`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-02-SUMMARY.md`
- FOUND: commit `09c3c563` feat(55-02): add probe CLI config and evidence writer
- FOUND: commit `f68ddd47` test(55-02): exclude characterization probe from phase38 glob
- FOUND: commit `6477099e` test(55-02): cover CLI config evidence and non-verdict exit
- FOUND: `.venv/bin/python -m pytest tests/phase55/ -q` — 39 passed

---
*Phase: 55-architecture-characterization-probe*
*Completed: 2026-09-06*
