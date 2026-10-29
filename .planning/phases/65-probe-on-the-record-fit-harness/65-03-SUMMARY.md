---
phase: 65-probe-on-the-record-fit-harness
plan: "03"
subsystem: testing
tags: [pinn, diagnostic-harness, entry-point-isolation, checkpoint-store, resume-routing, tdd]

requires:
  - phase: 65-probe-on-the-record-fit-harness
    provides: require_not_diagnostic/DiagnosticArtifactRefused with intrinsic-marker survival under renaming, relocation and CTX-53 key laundering
  - phase: 60-single-system-learnability
    provides: the production evaluate_run/train.main/checkpoint-store/resume contracts this plan wires the guard into (outside the 33 pinned modules)
provides:
  - evaluate_run refuses INST-08 records and marked weight envelopes by content after the canonical-frame precondition and before config/manifest load, the evaluation claim or any data-adapter construction, translated into the existing CheckpointOwnershipError convention
  - require_resume_not_diagnostic, the read-only early graded-resume admission (explicit file / directory / literal latest) that never constructs a checkpoint store
  - DiagnosticCheckpointRefused (a NoValidCheckpointError subclass) plus marker refusals on load_latest, fallback_scan, load_checkpoint, the structural validator and load_resume_target's returned-payload boundary
  - train.main rejects diagnostic resumes before run_dir.mkdir, data/model/optimizer setup or any training effect
affects: [65-04, 65-05, 65-06]

actuals:
  tokens: 10977   # chars/4 over the realized task diff (43907 chars, 740 insertions, 71 deletions)
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Early admission mirrors routing, not filenames: the guard resolves exactly what load_resume_target would select (explicit file, or latest.pt/fallback order over the run's own checkpoints dir) and refuses the marked selection instead of falling through to an older ordinary file"
    - "Marker refusal before structural check: every load route raises DiagnosticCheckpointRefused outside any corrupt-file except, so a diagnostic refusal can never become a corrupt-file skip or silent fallback"
    - "One marker predicate, one selection implementation: carries_diagnostic_marker lives in diagnostic_guard, fallback_candidates/peek_latest_selection live in checkpoint.py, and the store methods delegate — no duplicated ordering or marker logic"

key-files:
  created: []
  modified:
    - pinn/verification/diagnostic_guard.py
    - pinn/evaluate.py
    - pinn/train.py
    - pinn/training/checkpoint.py
    - pinn/training/resume.py
    - tests/phase65/test_isolation.py

key-decisions:
  - "The evaluator translates the guard's DiagnosticArtifactRefused into its existing public CheckpointOwnershipError convention (message names the diagnostic marker and the file), so the four public refusal types and main()'s nonzero CLI behavior are unchanged; the checkpoint side likewise surfaces DiagnosticCheckpointRefused as a NoValidCheckpointError subclass"
  - "The evaluate guard sits after the prior-attempt/receipt check and before the frozen config/manifest load: strictly earlier than the required manifest/claim boundary, while ownership, output-guard and rerun refusals keep their existing precedence for non-diagnostic files (Phase 43/60 evaluator behavior byte-identical)"
  - "The early resume admission is read-only and mirrors load_resume_target exactly, including its directory form routing to the run's OWN store root (load_latest), so a marked file inside a supplied-but-ignored directory never refuses a resume that would legitimately load"
  - "checkpoint.py owns the selection seam (fallback_candidates/peek_latest_selection module-level, methods delegate) and imports the marker predicate from diagnostic_guard at module level; diagnostic_guard reaches back for the selection only via a deferred in-function import — the repo's established cycle-avoidance pattern — honouring the plan's checkpoint-to-guard key link"

patterns-established:
  - "Zero-effect entry proofs: relocated negative cases sit beside fully valid provenance with a nonempty test split, spy the claim/manifest/adapter/stage-index/corpus seams, and snapshot the run tree; a same-layout ordinary control completes the real flow so missing config, empty split or ownership can never be the refusal reason"
  - "Selection-order preservation is tested in both directions: a marked newest candidate refuses over an older ordinary file, while an ordinary newer candidate still wins over a marked older one"

requirements-completed: []   # INST-08 spans later Phase 65 plans; production-entry isolation alone does not complete it

coverage:
  - id: D1
    description: "evaluate_run refuses native and relocated INST-08 records and marked weight envelopes — including a laundered envelope carrying every CTX-53 key — beside valid config.yaml/splits.json with a nonempty test split, with zero claim/manifest/adapter/stage-index calls, zero corpus opens and an unchanged run tree; an ordinary production checkpoint clears the guard and evaluates"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_isolation.py#EvaluateEntryIsolationTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "train.main rejects diagnostic explicit-file, directory and literal-latest resumes (renamed JSON records and relocated weights included) before run creation or data/model/optimizer setup, while an ordinary latest resume preserves the production route into normal setup; the read-only admission never creates the checkpoints directory"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_isolation.py#GradedEntryIsolationTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_isolation.py#EarlyResumeAdmissionTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "No checkpoint load route ever returns a diagnostic envelope: load_latest (corrupt-handler non-swallowing), fallback_scan, load_checkpoint and load_resume_target's returned-payload boundary all raise the NoValidCheckpointError-compatible DiagnosticCheckpointRefused for marked payloads with every CTX-53 key present, and ordinary production payloads keep their load behavior and candidate ordering"
    requirement: INST-08
    verification:
      - kind: unit
        ref: "tests/phase65/test_isolation.py#CheckpointRouteIsolationTests"
        status: pass
    human_judgment: false

duration: 31 min
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 03: Probe on the Record & Fit Harness — Production-Entry Isolation Summary

**Diagnostic isolation now holds at the real production entry points: evaluate_run refuses INST-08 artifacts by content before the one-time evaluation claim, train.main rejects diagnostic explicit/directory/latest resumes before run creation, and no checkpoint load route (load_latest, fallback_scan, load_checkpoint, load_resume_target) can ever return a marked envelope.**

## Performance

- **Duration:** about 31 min (2026-10-29 17:26–17:57 UTC)
- **Started:** 2026-10-29T17:26:19Z
- **Completed:** 2026-10-29T17:57:00Z
- **Tasks:** 2 of 2
- **Files modified:** 6 (5 production/test files edited, 0 created; plus this SUMMARY)
- **Verify latency:** the plan's two-module verify command runs 77 tests in 1.6 s; the full Phase 65 suite runs 108 tests in 2.2 s

## Accomplishments

- `evaluate_run` places `require_not_diagnostic` after the canonical-frame precondition and the prior-attempt/receipt check, and before the frozen config/manifest load, the exclusive evaluation claim, data-adapter construction or any corpus access. The refusal is translated into the evaluator's existing public `CheckpointOwnershipError` convention with a message naming the diagnostic marker, so the one-time evaluation budget can never be spent on a diagnostic artifact — including a renamed JSON record or a tensor envelope carrying all seven CTX-53 production keys around the marker, relocated beside valid `config.yaml`/`splits.json` with a nonempty test split.
- `train.main` runs the new read-only `require_resume_not_diagnostic` admission over the existing run-name/root resolution and before `run_dir.mkdir`: diagnostic explicit-file, directory and literal `latest` resumes exit nonzero with a diagnostic message and zero run-directory side effects, verified with spies on `_resolve_runtime_spec`, `_build_sources`, `build_network` and `RunController` plus unchanged-tree snapshots. The admission never constructs `TorchSaveCheckpointStore` (its constructor creates directories), and an absent checkpoints directory stays absent.
- Every checkpoint load route refuses marked payloads by content: `DiagnosticCheckpointRefused` (a `NoValidCheckpointError` subclass, so existing callers, `assertRaises(NoValidCheckpointError)` tests and the CLI nonzero convention keep working) is raised on `load_latest` (outside the corrupt-file handler, so a marked `latest.pt` can never be swallowed into a fallback), `fallback_scan` (a marked newest candidate refuses instead of falling through to an older ordinary file), `load_checkpoint` (marker before the structural test, so key absence cannot supply the refusal) and `load_resume_target`'s returned-payload boundary (defense against a store that failed to check). `_is_structurally_valid` also refuses marked payloads, making the invariant total for direct validator callers.
- Selection and ordering for valid production files are preserved exactly: `fallback_candidates`/`peek_latest_selection` are the single module-level implementation the store methods delegate to, `load_latest` keeps its exact semantics (unreadable `latest.pt` falls back; empty store still raises `EmptyCheckpointStore`), and the ordinary-newer-over-marked-older ordering case is pinned by test.

## Task Commits

Each task followed RED → GREEN (TDD); each RED machine-verified `RED_EVIDENCE_OK` via `check tdd-red-evidence`:

1. **65-03-01 reject relocated diagnostic input before evaluation ownership** — `e887ac24` (test) + `14529e8a` (feat)
2. **65-03-02 reject diagnostic graded resumes on all load routes** — `bcbf762c` (test) + `6449a2ec` (feat)

**Plan metadata:** this commit (docs).

## Files Created/Modified

- `pinn/evaluate.py` — content guard + typed translation before config/manifest/claim (21 net lines)
- `pinn/train.py` — early resume admission before `run_dir.mkdir` (+19)
- `pinn/training/checkpoint.py` — `DiagnosticCheckpointRefused`, public `carries_diagnostic_marker` reuse, module-level `fallback_candidates`/`peek_latest_selection`, marker refusals on every load route and in the structural validator
- `pinn/training/resume.py` — `load_resume_target` returned-payload boundary
- `pinn/verification/diagnostic_guard.py` — public `carries_diagnostic_marker` predicate and `require_resume_not_diagnostic` early admission
- `tests/phase65/test_isolation.py` — `EvaluateEntryIsolationTests`, `EarlyResumeAdmissionTests`, `GradedEntryIsolationTests`, `CheckpointRouteIsolationTests` (+474 lines across the two RED commits)

## Verification Commands and Outcomes

- Task 1 verify: `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_isolation -v` → 23 tests OK (exit 0)
- Task 2 verify: `… -m unittest tests.phase65.test_isolation tests.phase65.test_contracts -v` → 77 tests OK (exit 0)
- Plan-level: `… -m unittest discover -s tests/phase65 -p 'test_*.py'` → 108 tests OK, 2.193 s; `git diff --check` → clean
- Production-diff review: the only behavior change in `pinn/` is early diagnostic rejection; the canonical-frame precondition remains the first evaluator precondition, ownership/output/rerun checks keep their precedence, and `load_latest`/`fallback_scan`/`load_checkpoint` semantics for unmarked payloads are unchanged (delegation refactor only)
- Frozen-surface recheck: `load_protocol()` revalidates all 33 `PINNED_MODULES` digests (PROTOCOL-OK); `pinn/verification/split_allowlist.py` and `pinn/verification/learnability_data.py` untouched; no pinned file edited
- Regression on every touched seam: `tests.phase41.test_checkpoint` + `tests.phase41.test_resume` → 78 OK; `tests.phase41.test_train_entrypoint` (real end-to-end resumes) → 26 OK in 54 s; `tests.phase60.test_refusals` + `tests.phase57.test_gate_and_evaluation` → 32 OK; `tests.phase43` evaluate suites → 28 OK; `tests.phase40.test_checkpoint` + `tests.phase41.test_controllers_ext` → OK
- No real corpus record was opened beyond the TinyCorpus fixture under temporary roots; no `runs/` tree was created in the repository; the held-out evaluation remains unspent (every evaluation in the suite ran inside a temporary run layout)

## Decisions Made

- **Translation conventions:** the evaluator raises its existing `CheckpointOwnershipError` (message names the diagnostic marker); the store routes raise `DiagnosticCheckpointRefused(NoValidCheckpointError)`. Both keep the existing public exception and nonzero-CLI conventions in use, as the plan requires, while the message makes every refusal specifically diagnostic.
- **Guard placement in `evaluate_run`:** after the prior-attempt check, before `load_config` — strictly earlier than the required manifest/claim boundary, with all pre-existing refusals keeping their precedence for non-diagnostic files.
- **Directory-resume mirroring:** `load_resume_target` routes a directory argument to the run's OWN store root (`load_latest`), so the early admission checks the run's checkpoints directory, not the supplied directory's contents — never refusing a legitimate resume because of files the production route would never read.
- **Module layout:** `checkpoint.py` imports the marker predicate from `diagnostic_guard` at module level (the plan's checkpoint→guard key link); `diagnostic_guard`'s admission reaches checkpoint's selection helpers through a deferred in-function import (the repo's established cycle-avoidance pattern, mirroring `pinn.train`), so neither module import cycle exists at load time.

## Deviations from Plan

None - plan executed exactly as written.

## TDD Gate Compliance

Both tasks committed a `test(65-03)` RED before their `feat(65-03)` GREEN (`e887ac24` → `14529e8a`; `bcbf762c` → `6449a2ec`), and each RED was machine-verified `RED_EVIDENCE_OK` at commit time (records at `/tmp/phase65_t1_red_record.json` and `/tmp/phase65_t2_red_record.json`, built from a faithful in-process unittest→TAP converter; target tests `EvaluateEntryIsolationTests.test_native_relocated_weights_are_refused_before_any_effect`, 23 tests/3 fail, and `GradedEntryIsolationTests.test_an_explicit_marked_file_resume_is_refused_before_run_creation`, 44 tests/17 fail). The Task 2 control tests (ordinary production payloads loading, the ordinary-latest main() route) passed already at RED time — regression coverage of preserved production behavior, documented here rather than treated as an unexpected GREEN. No REFACTOR commit: the final implementation needed no post-GREEN cleanup.

## Issues Encountered

- `tests/phase49/test_gate03_resume.py` fails to IMPORT (`ModuleNotFoundError: No module named 'pytest'`) in the `pinn-train` environment — a pre-existing environmental gap, unrelated to this diff and outside every plan verify command; not fixed (scope boundary). All other suites in the same run pass.

## User Setup Required

None — no external service configuration; everything runs on the local `pinn-train` environment.

## Known Stubs

None — every delivered path is real; no placeholder, TODO or unwired data source remains.

## Next Phase Readiness

- INST-08(d) is proved at the actual production entry points: relocation beside valid provenance, production-key laundering and every resume routing form are refused by content, with zero evaluation/data/training side effects and the frozen evaluation unspent.
- Plans 65-04 onward (probe registration, the read-only seven-arm reproduction, the real-orbit fit) can rely on this isolation: any INST-08 record or marked weights envelope they produce is intrinsically refused by `evaluate_run`, `train.main` and all checkpoint load routes.
- No blocker. INST-08 and DIAG-09 stay open (later plans own their completion).

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*

## Self-Check: PASSED

All seven key files exist on disk; all five plan commits (`e887ac24`, `14529e8a`, `bcbf762c`, `6449a2ec`, `039d78ab`) are in history; the RED/GATE sequence is present for both tasks (two `test(65-03)` REDs, two `feat(65-03)` GREENs); both verify commands exit 0 at the final tree (23 and 77 tests).
