---
phase: 60-single-system-learnability
plan: 03
subsystem: requirements-amendment
tags: [scope-amendment, gap-60-01, containment-test, nfc-whitespace-collapse, spec-parser, frozen-scorecard]

requires:
  - phase: 60-single-system-learnability
    provides: "plan 60-01 created the tests/phase60 package; 60-SPEC.md holds the six amendment paragraphs (single source of truth); GAP-60-01 ruled option A"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard (SHA-256 f4b17688...444b), load_scorecard(), and verify_phase59_evidence.py scorecard-frozen"
provides:
  - "REQUIREMENTS.md carries the 2026-10-17 amendment word for word in SCOPE-39, FEAS-09, SCOPE-44 and Owner Checkpoint 4 (FEAS-04 and roadmap criterion 3 already did)"
  - "tests/phase60/test_amendment.py: 21 tests that parse the six paragraphs from 60-SPEC.md and check each inside its own section, plus the frozen-scorecard checks"
  - "The amendment commit dc3edac0e9ae737b42be276dd9b67e12b8ab8926, which precedes any real-arm record (Plan 60-13 pins it in the run protocol)"
affects: [60-10, 60-13, phase-64-handoff]

amendment_commit: dc3edac0e9ae737b42be276dd9b67e12b8ab8926

actuals:
  tokens: 4960
  tasks: 2
  commits: 1
plan_head_before: 2734f4c90b8690e62a667e9b8c5ea0d019a7c267

tech-stack:
  added: []
  patterns:
    - "Section-scoped containment: NFC plus whitespace collapse on both sides, no markdown stripping, tested inside one designated section and never in the whole file"
    - "Paragraphs parsed from the SPEC at test time, so the SPEC stays the single source of truth"
    - "Locators that raise on a missing or repeated anchor instead of choosing one"

key-files:
  created:
    - tests/phase60/test_amendment.py
  modified:
    - .planning/REQUIREMENTS.md

key-decisions:
  - "The one-word-change proof in LocatorSelfTests builds its section from each SPEC paragraph instead of mutating the real sections, so it means the same thing in the RED state (four paragraphs absent from the files) and the GREEN state"
  - "The circled digit U+2463 lives in the Checkpoint paragraph's label, not its body, so ParserTests assert it on the label key and assert the backtick spans (first_omega_0, pinn_architecture.md) on the body"
  - "Locators are bounded and strict: SourceMiss on zero or several anchors; the roadmap locator is limited to the Phase 60 heading, its Success Criteria line and the item-4 line, so the Gate G2 paragraph's copy of the sentence cannot satisfy criterion 3"
  - "Test identifiers avoid the substrings Error and FAILED so the plan's text-based fails_when checks cannot be tripped by verbose test names"

requirements-completed: [FEAS-04, FEAS-09]

coverage:
  - id: D1
    description: "The six SPEC amendment paragraphs are each contained, after NFC and whitespace collapse, in their own section of REQUIREMENTS.md or ROADMAP.md (four REQUIREMENTS.md edits: SCOPE-39 row, FEAS-09 opening line, SCOPE-44 row, Owner Checkpoint 4)"
    requirement: "FEAS-04, FEAS-09"
    verification:
      - kind: unit
        ref: "tests/phase60/test_amendment.py#ContainmentTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The check reads the SPEC itself and cannot pass vacuously: exactly six labels, section-bounded locators, a one-word change breaks containment, and the Gate G2 copy of the roadmap sentence is outside criterion 3"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_amendment.py#ParserTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_amendment.py#LocatorSelfTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The frozen scorecard is byte-unchanged (SHA-256 f4b17688...444b), load_scorecard() succeeds, and the Phase 59 scorecard-frozen command prints SCORECARD-FROZEN-OK; the amendment commit touches none of the frozen files or ROADMAP.md"
    verification:
      - kind: unit
        ref: "tests/phase60/test_amendment.py#ScorecardFrozenTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen"
        status: pass
      - kind: other
        ref: "git diff --quiet dc3edac0~1 dc3edac0 -- .planning/ROADMAP.md <four frozen files> (AMENDMENT-SCOPE-OK)"
        status: pass
    human_judgment: false
  - id: D4
    description: "The amendment is committed as one commit that touches exactly REQUIREMENTS.md and the test, and no real-arm record exists yet, so it precedes every real arm"
    verification:
      - kind: other
        ref: "git show --name-only --format= dc3edac0 (two paths) and find of record.json, evidence/arms and *.weights under the phase directory (none)"
        status: pass
    human_judgment: false

duration: 11min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 03: Scope amendment text and containment check Summary

**The Phase 60 scope amendment now sits in REQUIREMENTS.md word for word (SCOPE-39, FEAS-09, SCOPE-44, Owner Checkpoint 4) in one commit, `dc3edac0`, proven by a 21-test check that parses the six paragraphs from 60-SPEC.md and tests each inside its own section, with the frozen scorecard SHA-256 unchanged.**

In plain language: the written rules now say what the experiment will do (data-only arms train on the gold record they are graded on; Rung 2 and the probes are skipped, with one of two recorded reasons, when the ladder stops at Gate G2; on an owner continue the approved setting governs the remaining arms). A test now fails if the SPEC and the requirement files ever drift apart.

## Performance

- **Duration:** about 11 min
- **Started:** about 2026-10-20T01:03Z (not captured at spawn; the previous commit landed at 01:02:25Z, and the commit ledger was created at 01:06:26Z after the plan and SPEC were read)
- **Completed:** 2026-10-20T01:14Z
- **Tasks:** 2 (Task 1 tracer, Task 2 edits plus commit)
- **Files:** 2 (1 created: the test, 420 lines; 1 modified: `REQUIREMENTS.md`, 10 insertions and 5 deletions)
- **Measured:** `actuals.tokens` 4,960 is chars/4 over the realized diff (19,841 content characters). The plan's 45,000 was a low-confidence estimate; the figure is not rounded toward it.

## Accomplishments

- **Containment check.** `tests/phase60/test_amendment.py` parses the six bold-labelled paragraphs under `## Amendment text` in `60-SPEC.md` and asserts each is contained, after `unicodedata` NFC normalization and `" ".join(text.split())` on both sides with no markdown stripping, in its own section only: the SCOPE-39 row, the FEAS-04 entry, Phase 60 success criterion 3 of `ROADMAP.md`, the FEAS-09 entry, the SCOPE-44 row, and Owner Checkpoint 4.
- **Four edits to `REQUIREMENTS.md`, nothing else.** (1) SCOPE-39: the two `**` markers deleted. (2) FEAS-09: the opening line now holds the three amendment sentences as one run, followed by the kept explanatory sentence. (3) SCOPE-44: the clause no longer repeats the condition and the stand-alone sentence "The hard-stage probes run only if the ladder continues past G2." is in the row. (4) Owner Checkpoint 4: the three Checkpoint continue sentences are inserted contiguously after "Continue runs the remaining Phase 60 arms at the approved setting.", in the item's hard-wrap style.
- **Untouched by design.** `ROADMAP.md` (criterion 3 already carries its sentence), the FEAS-04 acceptance bullet, the FEAS-09 last acceptance bullet, `STATE.md`, and the four frozen scorecard files are byte-identical to HEAD. No requirement checkbox was ticked.
- **Frozen scorecard.** `ScorecardFrozenTests` check the file's SHA-256 against both the module constant and the literal `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`, `load_scorecard()`, and the Phase 59 `scorecard-frozen` command (prints `SCORECARD-FROZEN-OK`).

## Task Commits

1. **Task 1: Tracer, the containment test (RED on four paragraphs)** - not committed, by the plan's own instruction ("Task 2 commits the test with the edits"). Result recorded below.
2. **Task 2: Edit `REQUIREMENTS.md`, commit the amendment** - `dc3edac0e9ae737b42be276dd9b67e12b8ab8926` (spec): `spec(60-03): apply the phase 60 scope amendment text`. `git show --name-only --format=` lists exactly `.planning/REQUIREMENTS.md` and `tests/phase60/test_amendment.py`; the diff contains no deletions of files.

**Plan metadata:** the docs commit that follows this file.

### Task 1 RED result (before any `REQUIREMENTS.md` edit)

`python -B -m unittest tests.phase60.test_amendment -v`: **Ran 21 tests, FAILED (failures=4)**.

| Test | Result | Why |
|---|---|---|
| ContainmentTests: SCOPE-39 row | FAIL | contained once the two `**` markers are removed (marker count 2) |
| ContainmentTests: FEAS-09 entry | FAIL | 1 of 3 sentences present |
| ContainmentTests: SCOPE-44 row | FAIL | 0 of 1; the condition was a clause inside a longer sentence |
| ContainmentTests: Checkpoint continue | FAIL | 0 of 3 inside Owner Checkpoint 4 |
| ContainmentTests: FEAS-04 bullet, roadmap criterion 3 | ok | already verbatim |
| ParserTests (6), LocatorSelfTests (6), ScorecardFrozenTests (3) | ok | 15 tests |

GAP-60-01 counts the Checkpoint paragraph as "1 of 3" file-wide, because "Phase 60 does not edit `pinn_architecture.md`." already sits in the FEAS-03 rescue bullet. That is outside the designated section, so the section-scoped check correctly saw 0 of 3 and the edit inserted all three.

**Tracer feedback gate.** Auto mode was off (`workflow._auto_chain_active` false, `workflow.auto_advance` unset) and `human_verify_mode` was `end-of-phase`, with an automated-only verify. The Task 1 verify command was re-run: **Ran 15 tests, OK**, exit 0, none of `FAILED`, `Error` or `Ran 0 tests` in the output. "Tracer verified end-to-end, expanding."

## Files Created/Modified

- `tests/phase60/test_amendment.py` - `collapse`, `parse_amendment`, six section locators, `SECTIONS` registry, and the four test classes (`ParserTests` 6, `ContainmentTests` 6, `LocatorSelfTests` 6, `ScorecardFrozenTests` 3)
- `.planning/REQUIREMENTS.md` - the four amendment edits (lines 187, 319, 324 and the Owner Checkpoint 4 item)

## Decisions Made

- **One-word-change proof on synthetic sections.** The plan describes "a copy of a section with one word changed fails containment". Applied to the real sections it would be vacuous in the RED state, where four paragraphs are absent. The test builds a section around each SPEC paragraph, confirms containment, changes the middle word, and confirms containment breaks. It passes in both states. Real-file bounds are checked separately (each locator starts and ends where expected and excludes its neighbour's marker).
- **Circled digit on the label.** The plan says the Checkpoint body "keeps its backticks and the circled digit U+2463". The digit is in the label `Checkpoint ④ continue`, not the body. The test asserts U+2463 on the label and the backtick spans on the body.
- **Strict locators.** A locator raises `SourceMiss` (an `AssertionError` subclass) on zero or several anchors. The roadmap locator is bounded by the `### Phase 60:` heading, its `**Success Criteria**` line and the `  4. ` line, and a synthetic roadmap proves that another phase's items and a Gate G2 copy of the sentence are ignored.
- **Naming.** Test and class names avoid the substrings `Error` and `FAILED`, so the plan's text-scan `fails_when` checks cannot be tripped by verbose output.

## Deviations from Plan

None - plan executed exactly as written.

### Process notes

- **Co-author trailer.** The commit carries `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5 (same note as 60-01).
- **Execution-context paths.** The plan's `@~/.claude-max/gsd-core/...` includes do not exist; the executing profile's `~/.claude-alt/gsd-core/...` files were read instead (a known property of this profile, not a typo).
- **Branch namespace check.** The generic executor assertion that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The detached-HEAD check, the protected-branch check (`git.base-branch --is-protected` returned false) and the cwd-drift check all passed.
- **State files.** `STATE.md` and `ROADMAP.md` were not touched and no `gsd-tools` state or roadmap verb was run. `FEAS-04` and `FEAS-09` stay unticked: both IDs are shared with later plans (the runs), so their checkboxes belong to the orchestrator.
- **Ledger and tooling.** `.planning/WINDOWS.md` was not appended (no stubs, skipped tests or unrun verifies). The Sequentialthinking MCP named in `CLAUDE.md` is not available to this executor.
- **Expensive commands.** None. The longest command was the guard suites at 9.7 s; no run was repeated to reformat output. Complete outputs are retained outside the repository in `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/2c416048-3fb9-456b-b651-a4fa222c09a5/scratchpad/` (`task1-red-full.txt`, `task1-tracer-verify.txt`, `task2-green-full.txt`, `task2-guards-full.txt`, `task2-verify1-committed.txt`).

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_amendment -v` (RED, before edits) | Ran 21 tests, FAILED (failures=4): SCOPE-39, FEAS-09, SCOPE-44, Checkpoint continue |
| Task 1 verify: `... ParserTests LocatorSelfTests ScorecardFrozenTests -v` | Ran 15 tests, OK |
| `python -B -m unittest tests.phase60.test_amendment -v` (after edits, pre-commit) | Ran 21 tests, OK |
| Same, on the committed tree (Task 2 verify 1) | Ran 21 tests, OK; no `FAILED`, `Error` or `Ran 0 tests` |
| `C=$(git log -1 --format=%H --fixed-strings --grep='spec(60-03)') ... git diff --quiet "$C~1" "$C" -- ROADMAP.md <four frozen files>` (Task 2 verify 2) | `AMENDMENT-SCOPE-OK` (`C` = `dc3edac0e9ae737b42be276dd9b67e12b8ab8926`) |
| `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen` | `SCORECARD-FROZEN-OK` (about 2 s) |
| `shasum -a 256 pinn/verification/artifacts/feasibility_scorecard_v1.json` | `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b` (unchanged) |
| `tests.phase39.test_prohibitions` + four named `tests.phase38.test_prohibitions` tests + `tests.phase59.test_static_guards` + `tests.phase60.test_static_guards` | Ran 76 tests, OK, 0 FAIL, 0 ERROR (new test file trips no repo-wide scan) |
| `git diff --check` on `REQUIREMENTS.md`, the new file, and the staged set | clean |
| `git diff --quiet HEAD -- .planning/ROADMAP.md .planning/STATE.md <scorecard json and module>` (pre-commit) | unchanged |
| FEAS-04 bullet and FEAS-09 last acceptance bullet vs HEAD | byte-identical |

Task acceptance criteria re-run against the committed tree: all pass (Task 1: six labels found, exactly four ContainmentTests RED, ScorecardFrozenTests pass; Task 2: all 21 pass, commit touches exactly the two named paths, FEAS-04, FEAS-09 acceptance bullet and `ROADMAP.md` unchanged, hash recorded here).

## Known Stubs

None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-13** pins `amendment_commit: dc3edac0e9ae737b42be276dd9b67e12b8ab8926` in the run protocol; **Plan 60-10**'s runner admission refuses a real arm unless that commit is an ancestor of HEAD. No real-arm record exists yet (`record.json`, `evidence/arms` and `*.weights` are all absent under the phase directory).
- Later commit messages in this plan avoid the literal `spec(60-03)`, so the Task 2 verify's `git log -1 --grep` keeps resolving to the amendment commit.
- Open for the orchestrator: update `STATE.md` and `ROADMAP.md` by hand; leave the FEAS-04 and FEAS-09 checkboxes until the plans that run Rung 2 and the probes (or record them skipped) have finished.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- Created and modified files exist on disk (`tests/phase60/test_amendment.py`, `.planning/REQUIREMENTS.md`); commit `dc3edac0` exists and is the only commit in `2734f4c9..HEAD`.
- `git log --oneline --all --grep="60-03"` returns the amendment commit.
- Task acceptance criteria and the three plan-level verification bullets (module passes, `SCORECARD-FROZEN-OK`, commit touches only `REQUIREMENTS.md` and the test) re-run against the committed tree: all pass.
