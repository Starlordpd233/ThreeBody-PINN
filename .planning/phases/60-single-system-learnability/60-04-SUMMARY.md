---
phase: 60-single-system-learnability
plan: 04
subsystem: testing
tags: [phase-59-verifier, d-09, gap-60-02, successor-digest, baselines-rederivation, manifest, evidence-reuse]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: verify_phase59_evidence.py, the ten result files that pin the scorer digest, the all-area manifest, the baselines --check re-derivation
  - phase: 60-single-system-learnability
    provides: "Plan 60-02's evidence/scorer-successor.json (phase60-scorer-successor/v1) and the fixed feasibility_scorer.py"
provides:
  - "verify_phase59_evidence.py: SCORER_REL / SCORER_SUCCESSOR_REL, _scorer_successor(), the single-successor branch in _check_result, and the digest-substituted baselines re-derivation (_substituted_baselines, _run_rederive, _rederive)"
  - "evidence/manifest.json rewritten after the verifier edit (verifier entry and produced_at_head only)"
  - "tests/phase60/test_verifier_successor.py: 34 synthetic-repo tests of the successor rule and the substituted re-derivation"
  - "Retained evidence that Phase 59 verifies end to end at HEAD 4df5d4a8 (PHASE59-EVIDENCE-OK, EXIT=0, 604 s), for Plan 60-22 to reuse"
affects: [60-22, 60-23]

actuals:
  tokens: 6215
  tasks: 3
  commits: 2
plan_head_before: 9448af2f83f553abe0e4c8f4dca6e816549c76dd

tech-stack:
  added: []
  patterns:
    - "A relaxation of an integrity check is a committed, tracked-and-clean record read at call time, exact key set, string fields only, one path hard-coded in the checker; the pair must match on both ends"
    - "Re-deriving against a same-length digest-substituted temporary copy, so the check still compares every other byte and the committed files are never written"
    - "Mutation check with a scratch harness that restores the file and compares its SHA-256 after every mutation"

key-files:
  created:
    - tests/phase60/test_verifier_successor.py
  modified:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/manifest.json

key-decisions:
  - "The record must have exactly the six v1 keys, all strings, schema phase60-scorer-successor/v1, path equal to the scorer path, two 64-character lowercase hex digests (fullmatch, so a trailing newline is refused). This is how 'a list of paths or of successors' and 'extra successor entries' are refused: any unknown key fails"
  - "The record is consulted only when a producer digest mismatches (and for the baselines re-derivation), so an absent or unneeded record changes nothing and a needed but untracked, dirty, staged-only, symlinked or malformed record fails closed"
  - "The substituted copy is made with shutil.copytree defaults (symlinks are followed into the copy, never recreated), so the write-back can only reach the copy"
  - "RED evidence is the retained unittest log, not 'check tdd-red-evidence': that verb parses Node TAP output and reports zero tests for Python unittest"

requirements-completed: [INST-05]

coverage:
  - id: D1
    description: "The Phase 59 result check accepts a producer-digest mismatch for exactly one path (the scorer) and only for the committed predecessor/successor pair, with a record that is tracked, clean and exactly the v1 shape; every other mismatch is refused as before"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_verifier_successor.py#SuccessorAcceptedTests, SuccessorRefusedTests, OtherProducerTests, AbsentRecordTests (25 + 1 tests)"
        status: pass
      - kind: other
        ref: "verify_phase59_evidence.py baselines --skip-rederive (BASELINES-OK) and diag07 --require all --skip-rederive (DIAG07-OK) on the real tree"
        status: pass
    human_judgment: false
  - id: D2
    description: "The baselines area re-derives against a temporary copy of the committed baselines/ files with only the predecessor digest replaced by the successor digest (same length), without writing the committed files and without a fallback to skipping"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_verifier_successor.py#SubstitutedRederiveTests, UnchangedRederiveTests, SubstitutionFailureTests"
        status: pass
      - kind: other
        ref: "verify_phase59_evidence.py baselines (re-derivation on): BASELINES-OK, EXIT=0, 61 s; log $HOME/.cache/3bp-phase60-logs/p59-baselines-60-04.log"
        status: pass
    human_judgment: false
  - id: D3
    description: "evidence/manifest.json is rewritten after the verifier edit and its diff shows only the verifier's entry (sha256, size_bytes) and produced_at_head"
    verification:
      - kind: other
        ref: "git diff --numstat on manifest.json before the commit (3 added, 3 deleted lines); verify_phase59_evidence.py manifest --area all prints MANIFEST-ALL-OK"
        status: pass
    human_judgment: false
  - id: D4
    description: "Phase 59 verifies end to end at the new HEAD with the scorer successor in place, and no Phase 59 evidence was regenerated"
    requirement: "INST-05"
    verification:
      - kind: other
        ref: "verify_phase59_evidence.py final, detached, HEAD 4df5d4a8: PHASE59-EVIDENCE-OK, ELAPSED=604, EXIT=0; log $HOME/.cache/3bp-phase60-logs/phase59-final-60-04.log"
        status: pass
      - kind: other
        ref: "git diff --quiet 0d0ec297 HEAD -- <baselines, diag07, census, survey, audit result directories> exits 0"
        status: pass
    human_judgment: false
  - id: D5
    description: "The twelve other hash-pinned Phase 59 producer modules, pinn/verification/baselines.py and the frozen scorecard files are byte-unchanged"
    verification:
      - kind: other
        ref: "git diff --quiet 0d0ec297 HEAD -- <the twelve modules, baselines.py, scorecard JSON and module, scorecard-freeze.json> exits 0"
        status: pass
    human_judgment: false

duration: 30min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 04: Phase 59 verifier accepts the one scorer successor Summary

**`verify_phase59_evidence.py` now accepts exactly one committed successor digest for `feasibility_scorer.py` (one path, one predecessor/successor pair, record tracked and clean) and re-derives the baselines against a same-length digest-substituted copy; the full Phase 59 check printed `PHASE59-EVIDENCE-OK` with `EXIT=0` at HEAD `4df5d4a8` in 604 s, with no Phase 59 evidence regenerated.**

## Performance

- **Duration:** about 30 min (1,812 s)
- **Started:** 2026-10-20T01:21:22Z
- **Completed:** 2026-10-20T01:51:34Z (approximate; the SUMMARY commit follows)
- **Tasks:** 3 (Task 1 tracer, Task 2, Task 3)
- **Files:** 2 modified, 1 created; 549 added lines, 9 removed; no file deleted

## Accomplishments

- **Successor rule (D-09, GAP-60-02 step 1).** `_check_result` skips a mismatch only when `_scorer_successor()` returns a record, the result key equals the record's path, the result's recorded digest equals `predecessor_sha256`, and the file's current digest equals `successor_sha256`. The record is read at call time relative to `REPO_ROOT` through `repo_path` (containment and symlink refusal), must be tracked and clean, and must have exactly the six v1 string keys. Everything else is compared exactly as before; with no record the behaviour is today's.
- **Digest-substituted re-derivation (GAP-60-02 step 2).** When a record exists, `_rederive("baselines")` copies the committed `baselines/` files (skipping `logs` and `__pycache__`) into a temporary directory, swaps the predecessor digest for the successor digest in every copied file (same length, checked), and runs `python -B -m pinn.verification.baselines --check --evidence-root <that directory>`. The committed files are never written, the directory is removed afterwards, and a differing or failed check fails the verifier. `pinn/verification/baselines.py` was not edited. **The substituted check passed, so the scorer fix did not change any CPU float64 baseline number and the GAP-60-02 stop condition did not trigger.**
- **Manifest (step 3).** `manifest --area all --write` at HEAD `ec8bd4e8` changed three lines: the verifier's `sha256` and `size_bytes`, and `produced_at_head`.
- **Final check (step 4).** `final` ran once, detached, at HEAD `4df5d4a8458c9acc09406d672088213d80c8ae82`, with nothing else heavy running.

## Digests

| | SHA-256 | Bytes |
|---|---|---|
| Scorer predecessor (pinned by the committed Phase 59 results) | `cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b` | 17,626 |
| Scorer successor (record and file on disk) | `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7` | 17,606 |
| Verifier before this plan | `faac504c1c96a1e61d8a4dfebebf07f636293438ccfcfae4aa9e31c16052bd5d` | 39,214 |
| Verifier after (committed in `ec8bd4e8`, listed in the manifest) | `82f5ddf44e80e2f227667efc701fe5119a9e69777547159b78b51d9c69e92620` | 43,392 |

## Phase 59 `final` at the new HEAD

- **Command:** `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final`, launched with `nohup sh -c` and polled; working directory the trainex worktree.
- **HEAD:** `4df5d4a8458c9acc09406d672088213d80c8ae82` (branch `milestone/v2.4`).
- **Result:** `PHASE59-EVIDENCE-OK`, `ELAPSED=604`, `EXIT=0`, started 2026-10-20T01:39:25Z. At Phase 59 close it took 644 s.
- **Log (outside the repository, not committed):** `$HOME/.cache/3bp-phase60-logs/phase59-final-60-04.log`, which is `<home>/.cache/3bp-phase60-logs/phase59-final-60-04.log`. First line `CMD=... HEAD=... CWD=...`, last two lines `ELAPSED=604` and `EXIT=0`.

| Step | Elapsed (s) |
|---|---|
| scorecard-frozen | 1.210 |
| audit | 4.438 (prints the owner-accepted `AUDIT-DEVIATION: GAP-59-10` line, as at Phase 59 close) |
| census | 54.003 |
| survey | 480.294 |
| baselines (substituted re-derivation inside `final`) | 60.355 |
| diag07 | 1.715 |
| guardrails | 1.097 |
| manifest (all) | 1.146 |
| phase59-files, findings | 0.007, 0.001 |

**For Plan 60-22 (reuse of this evidence).** The run is valid only while no input of `final` changes after `4df5d4a8`: the Phase 59 phase directory (evidence tree, the verifier, the manifest, `59-VALIDATION.md`, `59-FINDINGS.md`), the Phase 59 producer modules and the scorecard files, `tests/phase59`, `evidence/scorer-successor.json`, the retained generation-7 run files, and the `pinn` code and corpus that the census, survey and baselines re-derivations import and read. Plans 60-01 to 60-03 changed none of these; Phase 60's own new modules are not inputs.

## Red-green evidence

The tests were written first and run against the unedited verifier. The retained logs are in the session scratchpad (`red-run.log`, `red-run-final.log`).

- **Real tree before any edit:** `baselines --skip-rederive` exited 1 with `baselines.json producer_sha256 does not match pinn/verification/feasibility_scorer.py`; `diag07 --require all --skip-rederive` exited 1 with the same message for `g1.json`.
- **Synthetic tests before the edit (final test file, 33 tests):** `FAILED (failures=21, errors=5)`, 7 passing. The failures are assertions for the planned behaviour: for example `AssertionError: 1 != 0 : verify_phase59_evidence FAIL-CLOSED: census.json producer_sha256 does not match pinn/verification/feasibility_scorer.py` in `test_the_committed_record_makes_the_area_check_pass`, and `'scorer successor record is not tracked and clean' not found in ...` in the untracked, dirty and staged cases. The 5 errors are `AttributeError` on the not-yet-existing `_scorer_successor` (4) and `shutil` (1). The 7 that already passed are regression guards that must stay green (no-record strictness, an unchanged scorer, an unchanged command, other areas, a missing token, and the two mismatched-pair refusals).
- **After the edit:** the whole module, 34 tests (33 plus the same-digest-pair test added afterwards), `OK`, 0 skipped, with no `FAILED`, `Error` or `Ran 0 tests` in the verbose output.
- **Mutation check (13 mutations, scratch harness, verifier restored byte-identical after each, SHA-256 `82f5ddf4...2620` checked):** all 13 caught. They drop the path, predecessor or successor comparison, the tracked-and-clean check, the key-set check, the string-field check, the `fullmatch`, replace only the first digest occurrence, copy `logs`, substitute for every area, rewrite the committed file instead of the copy, drop `--evidence-root`, or ignore the record. The path comparison (M1) is caught only by `test_the_same_digest_pair_on_another_path_is_refused`.

## Task Commits

1. **Tasks 1 and 2: successor rule, substituted re-derivation and tests** - `ec8bd4e8` (fix). One commit by Task 2's explicit instruction ("Commit Tasks 1-2 as `fix(60-04): ...`"); the body names D-09, GAP-60-02 and both digests.
2. **Task 3: manifest** - `4df5d4a8` (evidence). The body lists the two changed fields and both old and new values.

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The tracer feedback gate ran after Task 1: not auto mode (`AUTO_CHAIN` false, `AUTO_CFG` unset), mode `end-of-phase`, and the verify block holds only `<automated>` entries, so the verification was re-run on the finished Task 1 tree before Task 2 started: the four Task 1 classes (25 tests, OK), `baselines --skip-rederive` printed `BASELINES-OK`, `diag07 --require all --skip-rederive` printed `DIAG07-OK`, and `tests.phase59.test_static_guards` ran 15 tests OK. `Tracer verified end-to-end - expanding.`

## Files Created/Modified

- `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` - the successor rule and the substituted baselines re-derivation (+93, -6 lines; imports `shutil` and `tempfile`, both inside the static guard's allowed roots)
- `.planning/phases/59-read-only-baseline-scorecard/evidence/manifest.json` - verifier entry and `produced_at_head` (+3, -3)
- `tests/phase60/test_verifier_successor.py` - 34 tests in 8 classes, reusing `AreaFixture`, `commit_all` and the helpers of `tests.phase59.test_evidence_verifier` (453 lines)

## Decisions Made

- **Exact key set.** The plan says a list of paths or of successors, or extra successor entries, must be refused. Requiring exactly the six v1 keys, all strings, refuses every such shape (a list in a field, or an extra `paths` or `successors` key) without guessing key names. Plan 60-02's own test already pins the real record to those six keys.
- **Lazy read of the record.** The record is consulted only on a mismatch and for the baselines re-derivation. A broken record therefore cannot break a tree that needs no relaxation, and a needed one cannot be bypassed.
- **Copy semantics.** `shutil.copytree` with its defaults, so a symlink inside `baselines/` would be copied as a regular file and the write-back can only touch the copy.
- **Length guard kept.** The plan asks for the length check after the swap. It cannot trigger for two 64-character digests, so it is a `fail(...)` guard rather than an `assert` (an `assert` would vanish under `python -O`).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical] The first test set could not tell the scorer path from another path**
- **Found during:** Task 1 (planning the mutation check)
- **Issue:** The second-producer test used a stub whose digests differ from the record's pair, so a verifier that dropped `relative == successor["path"]` would still pass every test. The research (Finding F, step 5) lists "same digest for a different path refused".
- **Fix:** Added `test_the_same_digest_pair_on_another_path_is_refused`, where the stub starts and ends with exactly the scorer's old and new bytes. The mutation run confirms it is the only test that catches the dropped path comparison.
- **Files modified:** `tests/phase60/test_verifier_successor.py`
- **Verification:** `OtherProducerTests` (3 tests OK); mutation M1 caught
- **Committed in:** `ec8bd4e8`

---

**Total deviations:** 1 auto-fixed (1 Rule 2)
**Impact on plan:** Strengthens the proof the plan asks for; no file outside the owned set changed and no frozen value moved.

### Process notes

- **One RED run for both tasks.** All tests, including Task 2's re-derivation classes, were written before the verifier edit, so Task 1's tracer gate ran the four Task 1 classes and the real-tree commands; the whole-module command of the Task 1 verify block became green only after Task 2, as it was always going to be.
- **Fixture reuse.** The tests import `AreaFixture`, `commit_all` and the small helpers from `tests.phase59.test_evidence_verifier` (`load_verifier`, `init_repo` and `run_main` are used through `AreaFixture`); nothing was copied and `tests/phase59` is byte-unchanged.
- **Commits carry `Claude Sonnet 5.5`** per the orchestrator's protocol; the plan text names Opus 5.5. The generic executor rule that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The cwd-drift and default-branch assertions ran before each commit.
- **Expensive commands, each run once.** `verify_phase59_evidence.py baselines` with re-derivation (61 s), `tests.phase59.test_evidence_verifier` (22 tests, 75.7 s, `OK`, 0 skipped) and `final` (604 s). Logs: `$HOME/.cache/3bp-phase60-logs/p59-baselines-60-04.log`, `p59-test-evidence-verifier-60-04.log`, `phase59-final-60-04.log`; each starts with the command, HEAD, working directory and (for the first two) the verifier SHA-256, and ends with `EXIT=` and, where measured, `ELAPSED=`. The evidence-verifier suite was not repeated after the manifest commit because its inputs (the verifier and the test modules) did not change after that run; the 34-test module (31 s), the 15-test static guard (6 s) and the 111-test closeout pass (50 s, `OK`, skipped=1, the designed opt-in `PlatformProbeTests`) are each under 60 s. The mutation harness (13 runs, 241 s in total, each run under 30 s) is retained in the scratchpad.
- **Log appeared empty until exit.** Python block-buffers stdout when redirected, so `final`'s log held only its first line for about ten minutes; progress was followed through the process table (`pinn.verification.dataset_survey --check` was the long child, 480 s).
- **Not touched.** `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` (INST-05 is declared by many plans in this phase, so the shared-ID gate leaves it to the orchestrator); `.planning/WINDOWS.md` was not appended (no stub, skipped test or unrun verify was added). The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_verifier_successor -v` (Task 1 and 2 verify 1, final tree) | Ran 34 tests in 31.4 s, OK |
| `verify_phase59_evidence.py baselines --skip-rederive` and `diag07 --require all --skip-rederive` (Task 1 verify 2) | `BASELINES-OK`, `DIAG07-OK`, 2 s each |
| `python -B -m unittest tests.phase59.test_static_guards` | Ran 15 tests, OK (before and after the edit) |
| `verify_phase59_evidence.py baselines` with re-derivation (Task 2) | `BASELINES-OK`, `EXIT=0`, 61 s, no `BASELINES-CHECK-DIFF` |
| `python -B -m unittest tests.phase59.test_evidence_verifier -v` (Task 2) | Ran 22 tests in 75.7 s, OK, 0 skipped |
| Task 2 retained-log gate (`grep '^BASELINES-OK'`, `'^EXIT=0 '`, `'^OK'`) | pass |
| `git diff --quiet HEAD -- pinn/verification/baselines.py .planning/phases/59-.../evidence/baselines` | exit 0 |
| `verify_phase59_evidence.py manifest --area all --write`, then `git diff --numstat` on `manifest.json` | 3 added, 3 deleted: verifier `sha256`, `size_bytes`, `produced_at_head` |
| Task 3 gate (`tail -n 1 log` is `EXIT=0`, `^PHASE59-EVIDENCE-OK`, `git diff --quiet HEAD -- manifest.json`) | pass |
| `verify_phase59_evidence.py final` (detached, HEAD `4df5d4a8`) | `PHASE59-EVIDENCE-OK`, `ELAPSED=604`, `EXIT=0`, no `FAIL-CLOSED` in the log |
| `git diff --quiet 0d0ec297 HEAD --` the baselines, diag07, census, survey and audit result directories | exit 0 |
| `git diff --quiet 0d0ec297 HEAD --` the twelve other pinned modules, `baselines.py`, scorecard JSON, `feasibility_scorecard.py`, `scorecard-freeze.json` | exit 0 |
| Closeout: `test_amendment`, `phase60.test_static_guards`, `test_scorer_mps`, `test_verifier_successor`, `phase59.test_static_guards` | Ran 111 tests in 50.5 s, OK (skipped=1) |
| `git diff --diff-filter=D --name-only HEAD~1 HEAD` after each commit | no deletions |

## Issues Encountered

None. Plan 60-02 had left `verify_phase59_evidence.py` red on the scorer's producer digest by design; this plan closes that. The two `tests.phase38.test_prohibitions` spec byte-identity failures recorded by Plans 60-01 and 60-02 are unrelated and were not run or touched.

## Known Stubs

None.

## Threat Flags

None. The edit adds no endpoint or auth path. The only new file access is a read of one fixed-path record through `repo_path` and a copy of committed evidence into a private (mode 0700) temporary directory that is removed afterwards. Threat register: T-60-08 mitigated (one path, one pair, string fields only, tracked and clean, `SuccessorRefusedTests`, `OtherProducerTests`, 13 of 13 mutations caught); T-60-05 mitigated (fixed relative path constant, `repo_path` containment and symlink refusal, `test_a_record_that_is_a_symlink_is_refused`); T-60-06 accepted (all logs live under `$HOME/.cache/3bp-phase60-logs`, none committed); T-60-SC accepted (no package installed).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 59 verifies at `4df5d4a8`; Plan 60-22 can cite `$HOME/.cache/3bp-phase60-logs/phase59-final-60-04.log` if no input listed above changes. If it must re-run, it has to be detached and alone, as here.
- Plan 60-23 depends on this plan and may now run its suites, including the real short training runs; no heavy job of this plan remains.
- No gap needs recording: GAP-60-02 option A worked as resolved and its stop condition (a differing substituted check) did not occur.
- The scorer successor record is now load-bearing for Phase 59 verification. Any later edit of `feasibility_scorer.py` fails both `SuccessorRecordTests` (Plan 60-02) and the Phase 59 verifier until a new record is committed.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All four files exist (`tests/phase60/test_verifier_successor.py`, the edited verifier, `manifest.json`, `evidence/scorer-successor.json`); commits `ec8bd4e8` and `4df5d4a8` exist and `git log --grep=60-04` returns them; the three retained logs exist and end in `EXIT=0`.
- Task acceptance criteria re-run on the final tree: the four behaviour classes and the three re-derivation classes pass (34 tests); the real-tree commands print `BASELINES-OK` and `DIAG07-OK`; the static guard passes; the baselines log shows `BASELINES-OK` and `EXIT=0`; the evidence-verifier log ends in `OK`; `baselines.py` and the committed baselines are unchanged against HEAD; the manifest commit changes only the verifier's digest, size and `produced_at_head`; the `final` log ends in `EXIT=0` with `PHASE59-EVIDENCE-OK`; no Phase 59 result file changed since `0d0ec297`.
