---
phase: 43-verification-stage-0-pilot-acceptance
plan: 12
subsystem: repository-acceptance
tags: [acc-02, acc-04, unittest, duration-gate, legacy-fixtures]
status: complete
requires:
  - phase: 43-06
    provides: "real 300-step smoke, interrupt/resume, checkpoint, and timing evidence"
  - phase: 43-09
    provides: "effective-runtime duration authorization and fail-closed marker validation"
  - phase: 43-10
    provides: "canonical once-only held-out evaluation enforcement"
  - phase: 43-11
    provides: "typed receipt-grounded verdict validation"
provides:
  - "Repository-wide compatibility with the ACC-01 duration gate across legacy Phase 41/42 launch fixtures"
  - "Precise Phase 39 corpus-reader detection without a bare .txt false positive"
  - "Green 1,036-test repository discovery evidence and formal ACC-02/ACC-04 completion"
affects: [phase-43-verification, milestone-v2.0-acceptance]
tech-stack:
  added: []
  patterns:
    - "Legacy launch tests authorize through persisted production calibration or the production smoke exemption"
    - "Generic text files imply corpus access only when paired with a corpus prefix or txt glob"
key-files:
  created:
    - .planning/phases/43-verification-stage-0-pilot-acceptance/43-12-SUMMARY.md
  modified:
    - tests/phase41/_fixtures.py
    - tests/phase41/test_train_entrypoint.py
    - tests/phase42/_fixtures.py
    - tests/phase39/test_prohibitions.py
    - .planning/REQUIREMENTS.md
key-decisions:
  - "Keep Phase 41 launches non-smoke and provision a real cpu/float64 calibration, including the strict-CPU override case."
  - "Use the production smoke exemption for Phase 42 operator-mechanics fixtures, but force strict-CPU configs back onto the calibrated non-smoke path."
  - "Preserve the Phase 39 reader allowlist exactly and narrow only the generic .txt detector signal."
patterns-established:
  - "Explicit run.smoke false in Phase 43 continues to exercise the production refusal matrix despite Phase 42 legacy defaults."
requirements-completed: [ACC-02, ACC-04]
coverage:
  - id: D1
    description: "Phase 41 and Phase 42 launch fixtures satisfy the real duration gate without changing its 1800-second boundary or refusal assertions."
    requirement: ACC-02
    verification:
      - kind: unit
        ref: "python -m unittest discover -s tests/phase41 -v (193 tests)"
        status: pass
      - kind: unit
        ref: "python -m unittest discover -s tests/phase42 -v (38 tests)"
        status: pass
      - kind: unit
        ref: "python -m unittest tests.phase43.test_verify_gate -v (18 tests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The Phase 39 sole-reader audit ignores non-corpus README.txt writes while retaining positive detection of corpus prefixes and txt globs."
    requirement: ACC-02
    verification:
      - kind: unit
        ref: "python -m unittest discover -s tests/phase39 -v (264 tests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "ACC-02 and ACC-04 are formally complete only after the complete repository suite passed and retained acceptance artifacts were inspected."
    requirement: ACC-04
    verification:
      - kind: integration
        ref: "python -m unittest discover -s tests -v (1,036 tests, exit 0)"
        status: pass
      - kind: other
        ref: "runs/stage0-smoke and runs/stage0-pilot-seed42/summary.md"
        status: pass
    human_judgment: false
duration: 18min-from-first-task-commit
completed: 2026-07-22
---

# Phase 43 Plan 12: Repository Acceptance Closure Summary

**Legacy launch fixtures now satisfy the unchanged duration gate, the corpus-reader audit retains its prohibition without false-flagging diagnostic text writes, and all 1,036 repository tests authorize ACC-02/ACC-04 completion.**

## Performance

- **Duration:** 18 min from first task commit to closeout; initial instruction/evidence loading was not separately timestamped
- **First task commit:** 2026-07-23T02:14:33Z
- **Completed:** 2026-07-23T02:32:17Z (Task 3), followed by summary closeout
- **Tasks:** 3
- **Files modified:** 5 task artifacts; 1 summary created

## Accomplishments

- Added a Phase 41 fixture helper that persists a real current-fingerprint `cpu/float64` timing calibration before the non-smoke launch harness runs, including the strict-CPU override case.
- Made Phase 42 operator-mechanics configs use the production smoke exemption while preserving explicit non-smoke and strict-CPU duration-gate coverage; honesty and redaction tests remained byte-identical.
- Replaced the Phase 39 bare `.txt` reader signal with corpus prefixes or an actual `.txt` glob signal while leaving `ALLOWED_CORPUS_READERS` unchanged.
- Observed a complete 1,036-test repository discovery run exit 0, then and only then marked ACC-02 and ACC-04 Complete in both requirement checkboxes and traceability rows.

## Task Commits

Each task was committed atomically:

1. **Task 1: Repair Phase 41 fresh-launch fixtures** — `c6c65bc3` (`fix`)
2. **Task 2: Repair Phase 42 fixtures and Phase 39 detector** — `9d30cd72` (`fix`)
3. **Task 3: Verify repository green and resolve ACC-02/ACC-04** — `f88cb4a6` (`evidence`)

**Plan metadata:** this summary closeout commit (`docs(43-12): complete repository acceptance plan`).

## Files Created/Modified

- `tests/phase41/_fixtures.py` — production-writer timing calibration helper for isolated legacy launches.
- `tests/phase41/test_train_entrypoint.py` — provisions the matching calibration in the common harness setup.
- `tests/phase42/_fixtures.py` — marks operator-mechanics fixtures as smoke while retaining non-smoke strict-CPU behavior.
- `tests/phase39/test_prohibitions.py` — narrows generic text detection to real corpus-glob behavior and adds positive/negative controls.
- `.planning/REQUIREMENTS.md` — records ACC-02 and ACC-04 Complete after the repository gate passed; 42/42 mapping is unchanged.
- `.planning/phases/43-verification-stage-0-pilot-acceptance/43-12-SUMMARY.md` — records execution and verification evidence.

## Decisions Made

- Used the real calibration writer for Phase 41 rather than smoke mode because `StrictCpuOverrideTests` must still prove the effective `cpu/float64` authorization path.
- Used smoke mode for Phase 42 because those tests exercise run lifecycle, signals, summaries, honesty, and redaction rather than duration; explicit `smoke: false` remains authoritative for Phase 43 gate tests.
- Did not add `pinn/training/guards.py` to a non-corpus exception set. Requiring a corpus prefix or `.txt` glob removes the false positive without expanding the exact reader allowlist.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The first Phase 43 gate-backstop run exposed that the new Phase 42 smoke default also reached a strict-CPU in-process test. The fixture was refined before commit so `strict_cpu_determinism: true` without an explicit smoke choice remains non-smoke; the test's existing `cpu/float64` calibration then exercised the intended gate and all 18 tests passed.
- The full verbose discovery command's final `tail -20` contained buffered test probe diagnostics after unittest's summary. `set -o pipefail` preserved the authoritative exit status (0), and a separate read-only discovery load counted exactly 1,036 tests.

## Verification

- `~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase41 -v` — **193/193 pass**, 39.352 s.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase42 -v` — **38/38 pass**, 270.095 s.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -v` — **264/264 pass**, 2.187 s.
- `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_gate -v` — **18/18 pass**, 6.597 s; includes strict-CPU fingerprinting, missing-calibration refusal, exact-1800 acceptance, and over-limit authorization cases.
- `set -o pipefail; ~/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -v 2>&1 | tail -20` — **PASS, exit 0**, therefore 0 failures and 0 errors.
- Read-only `unittest.defaultTestLoader.discover('tests').countTestCases()` — **1,036 discovered tests**.
- `shasum -a 256 tests/phase42/test_honesty_layer.py tests/phase42/test_redaction.py` — unchanged at `4d7cb6da…` and `ddbbd744…` before/after repair.
- `rg -n '_DURATION_GATE_LIMIT_S = 1800\.0|forecast > _DURATION_GATE_LIMIT_S' pinn/train.py` — unchanged production boundary and strict comparison found at lines 409 and 472.
- `rg -n 'ACC-02|ACC-04|Mapped to phases: \*\*42/42\*\*' .planning/REQUIREMENTS.md` — both checkboxes and traceability rows Complete; coverage remains 42/42.
- `git diff --check` on every task-owned diff — **PASS**.

## Acceptance Evidence

- `runs/stage0-smoke` is finished at 300 steps with checkpoints at 100, 158, 200, and 300, retained interrupt/resume evidence, and a final measured `0.11570179534756522 s/step` (`ACC-02`).
- `runs/stage0-pilot-seed42/summary.md` records final losses, validation, curriculum, a 1,500-trajectory held-out FAIL preview, comparison guidance, and all three honesty statements (`ACC-04`).
- No held-out evaluator command was run and no real acceptance evidence was mutated.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 43-12 is complete and all Phase 43 plan summaries are present.
- ACC-01 through ACC-06 now all read Complete in `.planning/REQUIREMENTS.md`.
- The parent orchestrator remains the sole writer for the already-dirty `.planning/STATE.md` and `.planning/ROADMAP.md`; this executor did not modify or commit either path.

## Known Stubs

- `.planning/REQUIREMENTS.md:17-24,62,73,92` contains pre-existing milestone language about owner-calibrated placeholder seams. These lines were not introduced or changed by Plan 43-12 and do not block its fixture-repair or acceptance-status goal; the active owner values and ACC-05 evidence are handled by prior Phase 43 plans.

## Threat Flags

None. Plan 43-12 changes only tests, requirement status, and this summary; it adds no endpoint, auth path, file-access trust boundary, or schema mutation.

## Self-Check: PASSED

- All five task-modified files and this summary exist on disk.
- Commits `c6c65bc3`, `9d30cd72`, and `f88cb4a6` exist in Git history and contain only declared owned paths.
- The full suite exited 0 with 1,036 discovered tests; targeted Phase 39/41/42 and Phase 43 duration-gate suites all passed.
- The production duration-gate files and Phase 42 honesty/redaction assertions were not modified.
- No plan-owned task change remains uncommitted; only this summary awaits its dedicated closeout commit.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-22*
