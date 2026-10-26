---
phase: 64-feasibility-verdict
plan: 01
subsystem: verification
tags: [verifier, fail-closed, sealed-handoff, frozen-paths, traceability, ver-22, feas-06, decision-rule]

requires:
  - phase: 60-single-system-learnability
    provides: "the sealed stop-handoff.json (SHA-256 7ed8223c), the seven arm records, g2-outcome.json, sweep-curve.json, skip-records.json, run-protocol.json module_sha256"
  - phase: 59-read-only-baseline-scorecard
    provides: "scorecard-freeze.json, 59-SCORECARD.md and the frozen feasibility scorecard the decision rule reads"

provides:
  - "verify_phase64_verdict.py: fail-closed verifier with the inputs, frozen and traceability modes (three more modes land in 64-02 to 64-04)"
  - "inputs: the sealed handoff's bytes, schema, null owner fields and nine citations, the seven arms that ran and the ones that did not, and the pre-registered label re-derived by the frozen decision_verdict"
  - "frozen: 33 pinned modules, 8 sealed files and 4 frozen trees unchanged since the phase base 1ebb1d9b, with no uncommitted or untracked change in 45 pathspecs"
  - "traceability: the VER-22 check, 24 of 24 requirements mapped one phase each across REQUIREMENTS, ROADMAP and PROJECT"
  - "tests/phase64/test_verifier_phase64.py: 60 tests, real-worktree smokes plus synthetic negative controls for every mode"

actuals:
  tokens: 17321
  tasks: 3
  commits: 3
  plan_head_before: f61ed73c2f3f371f504edf6fa73b263560a7c927

tech-stack:
  added: []
  patterns:
    - "Fail-closed verifier whose every mode re-derives from committed bytes: no pre-registered output is rewritten and no number is typed by hand"
    - "One summation helper (ordered_sum, a left-to-right += loop) for the one exact float comparison, because builtin sum() changed meaning in CPython 3.12"
    - "Frozen path list derived at run time from run-protocol.json module_sha256, with only the sealed files and trees named in code and a literal 45-pathspec count"
    - "One git call per check with 45 separate argv items after '--', never a shell string, plus an argument-count self-test"

key-files:
  created:
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/__init__.py
    - tests/phase64/test_verifier_phase64.py
  modified: []

key-decisions:
  - "ordered_sum is a left-to-right += loop from 0.0: it reproduces the sealed total 22.37828873402778, while math.fsum and a sorted order land one ulp below and builtin sum() matches only on CPython 3.9 and 3.11"
  - "The 33 pinned module paths are read from run-protocol.json module_sha256 at run time; the verifier hard-codes only the 8 sealed files and 4 frozen trees, and EXPECTED_PATHSPEC_COUNT is the literal 45, never derived from the lists it checks"
  - "The module-level torch/pinn import guard applies to the verifier; the shell=True, eval, exec and torch.load(weights_only=True) guards glob every *.py under the Phase 64 evidence directory so later producers are covered automatically"
  - "inputs fails closed on sweep-curve.json outcome != 'no_rescue' and on g2-outcome.json panel_systems != [1632, 851, 4658] before re-deriving the label, so a silently changed input cannot reach the rule"
  - "traceability prints only its enumerated lines in a fixed order (defined, table, roadmap, per-phase 59 to 64, status labels sorted, TRACEABILITY-OK last), so two runs on the same files are byte-identical"

patterns-established:
  - "Sealed-input verification: pin the handoff digest, re-check every citation, recompute the tier vector and the sweep outcome, then call the frozen rule and compare the whole returned dict"
  - "Frozen-tree verification: diff 45 pathspecs against the phase base and status them with --untracked-files=all, so committed, uncommitted and untracked changes all fail"
  - "Registry recount: exact-string ID sets from definitions, table and roadmap, with every stated count parsed as an integer and compared with =="

requirements-completed: [FEAS-06, VER-22]

coverage:
  - id: D1
    description: "inputs re-derives the pre-registered label RETHINK-REPRESENTATION from the sealed handoff and the frozen decision rule, with all nine citations and the seven-arm layout checked"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#InputsRealTests,InputsSyntheticTests,OrderedSumTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py inputs -> INPUTS-OK"
        status: pass
    human_judgment: false
  - id: D2
    description: "frozen proves the 33 pinned modules, 8 sealed files and 4 frozen trees are unchanged since 1ebb1d9b, with no uncommitted or untracked change in 45 pathspecs"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#FrozenRealTests,FrozenSyntheticTests,FrozenArgvTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py frozen -> FROZEN-OK"
        status: pass
    human_judgment: false
  - id: D3
    description: "traceability recounts VER-22 from the current registries: 24 definitions, 24 table rows, 24 roadmap IDs, one phase each in 59 to 64, every stated count equal"
    requirement: "VER-22"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#TraceabilityRealTests,TraceabilityPureTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py traceability -> TRACEABILITY-OK"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-10-25
status: complete
---

# Phase 64 Plan 01: Verifier Foundation, Frozen Paths and VER-22 Summary

**The Phase 64 verifier exists and its three no-new-document checks pass on the real tree: the sealed handoff re-derives RETHINK-REPRESENTATION through the frozen decision rule, nothing frozen has moved since the phase base, and all 24 v2.4 requirements trace to exactly one phase.**

In plain language: before anything is written for the owner, a small checking program now proves three things from files already in the repository. The result the pre-registered rule gave is recomputed by that same rule and matches the saved hand-off, including every file it cites. None of the frozen code, specs or Phase 59/60 evidence has changed, and nothing uncommitted or untracked sits in those trees. And every one of the 24 requirements belongs to exactly one phase, with every stated count in REQUIREMENTS, ROADMAP and PROJECT equal to the recount. The remaining Phase 64 checks are added to the same program by later plans.

## Performance

- **Duration:** about 15 min
- **Started:** 2026-10-25T23:00:46-05:00 (`f61ed73c`, "mark phase 64 executing")
- **Completed:** 2026-10-26T04:15Z
- **Tasks:** 3
- **Commits:** 3
- **Files created:** 3 (`verify_phase64_verdict.py`, `tests/phase64/__init__.py`, `tests/phase64/test_verifier_phase64.py`)

## Accomplishments

- **Task 1 — inputs (tracer, TDD):** `verify_phase64_verdict.py` with the sealed handoff check. It pins `stop-handoff.json` to SHA-256 `7ed8223c…`, requires schema `phase60-stop-handoff/v1` with `owner_answer` and `verdict_note` null, re-checks all nine `{path, sha256}` citations against disk, requires exactly the seven arm directories and no later-rung arm, `continue/`, `rescue.json` or `60-CHECKPOINT-4-RULING.md`, recomputes the three Rung-1 tiers and the sweep outcome, and re-derives the verdict by calling the frozen `decision_verdict` — the whole returned dict must equal the recorded one. The wall-hours total goes through `ordered_sum`, the left-to-right `+=` loop that reproduces the sealed `22.37828873402778` on every interpreter.
- **Task 2 — frozen:** 33 pinned modules (read at run time from `run-protocol.json` `module_sha256`), 8 sealed files and 4 frozen trees, diffed against the phase base `1ebb1d9b` and statused with `--untracked-files=all` over 45 pathspecs. `frozen_pathspecs` builds the list once and fails closed on a wrong part count, a count other than the literal 45, an empty or padded entry, or a duplicate; both git calls receive 45 separate argv items after `--`.
- **Task 3 — traceability (VER-22):** `traceability_report` recounts the definitions, the Traceability table and the six ROADMAP Phase 59 to 64 `**Requirements**:` lines, requires one set with each ID in exactly one phase and the table phase equal to the roadmap phase, and checks every stated count as an exact integer. The real registries read `defined 24`, `table 24`, `roadmap 24`, `per-phase 59:5 60:4 61:8 62:2 63:2 64:3`, status `Complete 7` / `Complete (recorded as skipped: no rescue) 2` / `Pending 15`.

## Task Commits

Each task was committed atomically through `scripts/agent-commit`:

1. **Task 1: the verifier and its inputs check** — `54079da3` (`feat`)
2. **Task 2: the frozen path check** — `8fb4d63c` (`feat`)
3. **Task 3: the traceability check for VER-22** — `927e82b6` (`feat`)

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase64.test_verifier_phase64 -v` | Ran 60 tests in 13.3 s, `OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py inputs` | `INPUTS-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py frozen` | `frozen paths pinned=33 sealed=8 trees=4`, `FROZEN-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py traceability` | `TRACEABILITY-OK` last, exit 0 |
| `python -B .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py final` | `RECORDS-OK`, `G2-OK`, `PHASE60-EVIDENCE-OK`, exit 0 (2 s) |
| `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen` | `SCORECARD-FROZEN-OK`, exit 0 (2 s) |
| `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py guardrails` | `GUARDRAILS-OK`, exit 0 (2 s) |

Mutant checks (each reintroduced by hand, caught by a test, then restored):

- Task 1: the wall-hours comparison disabled (`if False and total != stored_total`) — caught by `test_changed_wall_hours_fails`.
- Task 2: `--untracked-files=all` dropped from the status call — caught by `FrozenArgvTests.test_git_calls_receive_45_separate_argv_items`.
- Task 3: `TRACEABLE_PHASES` widened to include Phase 65 — caught by `TraceabilityRealTests` (a Phase 65 section is then required and absent).

## Files Created

- `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py` — the fail-closed verifier: `VerifyError`, `fail`, `sha256_file`, `repo_path`, `load_json`, `_git`, `is_ancestor`, `is_tracked`, `is_clean`, `ordered_sum`, `frozen_pathspecs`, `traceability_report`, the six input/g2 helpers, `cmd_inputs`, `cmd_frozen`, `cmd_traceability`, `COMMANDS`, `build_parser`, `main`. `torch` and `pinn` are imported inside the mode that needs them, never at module scope.
- `tests/phase64/__init__.py` — the Phase 64 test package.
- `tests/phase64/test_verifier_phase64.py` — 60 tests: `VerifierModuleTests`, `InputsRealTests`, `InputsSyntheticTests`, `FrozenRealTests`, `FrozenSyntheticTests`, `FrozenArgvTests`, `TraceabilityRealTests`, `TraceabilityPureTests`, `OrderedSumTests`, `StaticGuardTests`.

## Decisions Made

- **`ordered_sum`, not `sum` or `fsum`.** The seven wall-hour values sum to `22.37828873402778` only with a left-to-right `+=` loop from `0.0`; `math.fsum` and any sorted order land one ulp below on every interpreter, and builtin `sum()` matches only on CPython 3.9 and 3.11 because 3.12 changed it to compensated summation. `OrderedSumTests` pins both facts, including `ordered_sum([1e16, 1.0, -1e16]) == 0.0` against `math.fsum(...) == 1.0`.
- **One source for the pinned list.** The 33 paths come from `run-protocol.json` `module_sha256` at run time, so no second committed list can drift. Only the 8 sealed files and 4 frozen trees are named in code, and the total is the literal 45.
- **Guards that cover later producers.** The module-level import guard applies to the verifier alone (later Phase 64 scripts will import torch at module scope legitimately); the `shell=True` / `eval` / `exec` / `torch.load(weights_only=True)` guards glob every `*.py` under the Phase 64 evidence directory.
- **Fail closed before the rule runs.** `inputs` rejects a sweep outcome other than `no_rescue` and a `panel_systems` other than `[1632, 851, 4658]` with a clear message, so a changed input cannot reach `decision_verdict` as a different-but-plausible label.
- **Deterministic traceability report.** IDs are sorted as strings in the returned dict and the printed lines follow one fixed order, so two runs are byte-identical (asserted by `test_two_runs_are_byte_identical`).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `rescue.relative_to(REPO_ROOT)` raised on a temporary root (Task 1)**
- **Found during:** Task 1, by `InputsSyntheticTests`
- **Issue:** `REPO_ROOT` can be an unresolved alias of the resolved directory (a `tempfile` path under `/var` resolves through `/private/var`), so subtracting it from a resolved `rglob` hit raised `ValueError`.
- **Fix:** Build the repo-relative name from the `P60_EVIDENCE_REL` constant and `rescue.relative_to(evidence_dir)` instead.
- **Files modified:** `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py`
- **Commit:** `54079da3`

**2. [Rule 1 - Bug] An empty `**Requirements**:` line was reported as missing (Task 3)**
- **Found during:** Task 3, by `test_empty_requirements_line_fails`
- **Issue:** The line pattern required a space after the colon, so `**Requirements**:` matched nothing and failed with "found 0" instead of the must-have's "lists no requirement ID". Both fail closed, but the message hid the real defect.
- **Fix:** `REQUIREMENTS_LINE` now accepts zero or more spaces/tabs after the colon, so a present-but-empty line reaches the empty-ID branch.
- **Files modified:** `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py`
- **Commit:** `927e82b6`

### Test-structure refinement

**3. The uncommitted-`pinn/` control is split in two (Task 2)**
- **Found during:** Task 2, first run of the synthetic fixture
- **Issue:** An uncommitted edit to a *pinned* module fails at the pinned-module clean check before the tree-level status check, so one test could not prove the status gate itself.
- **Fix:** `test_uncommitted_edit_to_pinned_module_fails` asserts the pinned-module message; `test_uncommitted_edit_under_pinn_tree_fails` edits a tracked file under `pinn/` that no pin names, so only `git status` can catch it. Both fail closed.
- **Commit:** `8fb4d63c`

## Known Stubs

None. No placeholder, hardcoded empty value or unwired component was introduced; every mode reads committed files and every branch either prints its token or fails closed.

## Threat Flags

None beyond the plan's threat model. The modes add no network endpoint, no write path and no new trust boundary: they read committed files, resolve paths through `repo_path` (containment plus symlink refusal), and pass git arguments as lists, never through a shell.

## Notes

- `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` were not modified and no state, roadmap or requirements verb was run: the orchestrator owns STATE/ROADMAP, and 64-07 Task 2 performs the binding VER-22 run after the last registry edit.
- `git diff --quiet HEAD -- .planning/REQUIREMENTS.md .planning/ROADMAP.md .planning/PROJECT.md` exits 0 after Task 3, so the traceability run read the committed registries.
- `git status --porcelain -- .planning/phases/60-single-system-learnability pinn .planning/phases/59-read-only-baseline-scorecard/evidence pinn_instruction/markdown_conversion/framework-specs` prints nothing after the plan, so nothing sealed or pinned was touched.
- Pre-existing user-owned changes in the working tree (`.planning/config.json`, `.agents/`, `.gsd/`, `docs/work/...`, `phase-40-plan-04-grok.md`, and others) were left alone and never staged.

## Next Phase Readiness

- The verifier foundation is in place: 64-02 to 64-04 add their modes to the same `COMMANDS` table, and the static guards already cover any new `*.py` under the Phase 64 evidence directory.
- `inputs`, `frozen` and `traceability` all pass on the real tree; the wave gate is green (`PHASE60-EVIDENCE-OK`, `SCORECARD-FROZEN-OK`, `GUARDRAILS-OK`, `FROZEN-OK`, 60 tests).
- The binding VER-22 run remains 64-07 Task 2, after the last registry edit; this plan's run is a real smoke, not the closeout.

## Self-Check: PASSED

- Files: verifier, tests package, test module and this SUMMARY all exist.
- Commits: 54079da3, 8fb4d63c and 927e82b6 all present on milestone/v2.4.
- Ledger: 3 commits measured from f61ed73c.
