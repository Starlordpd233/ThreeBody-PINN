---
phase: 64-feasibility-verdict
plan: 07
subsystem: feasibility-verdict
tags: [owner-ruling, sign-off, requirements, roadmap, state, traceability, final-check]
requires:
  - 64-06 (the committed checkpoint ① ruling: V-1 change-course, C-1 to C-14 open)
  - 64-05 (the charter and its ruling mode)
  - 64-04 (the verdict)
provides:
  - "64-VERDICT.md: owner-signed, with the sign-off block and the ruling citation"
  - "64-CHARTER.md: owner-decided, every Owner cell copied from the ruling"
  - "FEAS-06, FEAS-10 and VER-22 ticked with Complete status cells"
  - "verify_phase64_verdict.py final mode and its completeness check"
affects:
  - v2.5 (reads PROJECT.md, the requirement statuses and the ruling)
tech-stack:
  added: []
  patterns:
    - apply only what the committed ruling records, and prove the only-if direction
    - synthetic fixtures rebuild their pre-ruling state from the committed files
    - aggregate check whose last line is the single success token
key-files:
  created:
    - .planning/phases/64-feasibility-verdict/64-07-SUMMARY.md
  modified:
    - .planning/phases/64-feasibility-verdict/64-VERDICT.md
    - .planning/phases/64-feasibility-verdict/64-CHARTER.md
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/test_verifier_phase64.py
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
decisions:
  - "PROJECT.md is not touched: C-12 and C-13 are open, so its title, What This Is, Core Value and Model line stay byte-identical to the phase base 1ebb1d9b."
  - "The twelve skipped-phase status cells are not touched: C-14 is open, so they stay Pending with unticked boxes and no label (GAP-64-01 stays OPEN)."
  - "No spec, amendment or gap register is edited: C-6 and C-7 are open, so the 10^-5 bar is neither retained nor replaced and GAP-59-08 stays OPEN."
  - "final reads PROJECT.md and REQUIREMENTS.md at HEAD, the same state the ruling mode judges, and its completeness step checks the if-direction ruling leaves out (an approval recorded but not applied fails)."
  - "The synthetic charter and verdict fixtures rebuild their pre-ruling state from the committed files, so every negative control still differs from the real document by exactly its mutation."
metrics:
  duration: 62 min
  completed: 2026-10-26
status: complete
actuals:
  tokens: 11874
  tasks: 3
  commits: 3
  plan_head_before: 36dfc2c0db1d178dfade9e70d59dcb62ad31ebe2
---

# Phase 64 Plan 07: The owner's answers applied, VER-22's binding check and the final check

## One-liner

The committed checkpoint ① ruling is carried out and nothing more: the verdict signs off on `change-course`, the charter's fifteen Owner cells copy the ruling's recorded answers, the three Phase 64 requirements are ticked against a re-counted 24, and one `final` command proves the whole phase with `PHASE64-VERDICT-OK` as its last line.

## The decisive fact this plan rested on

`.planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md` (SHA-256 `b0a80c114d1ddc7994c7e02abdd8105f7ae418c776981cf109951bb8f31fac82`) records **V-1 = `change-course`** and **C-1 to C-14 = `open`**. The owner replied "let's change course" and addressed no charter row, so every C row is open, not approved. Under the plan's own rules an open row authorises no edit, so the only content changes are the verdict's sign-off and the charter's Owner column.

## Task 1 — applied and unchanged, row by row

| Row | Recorded answer | What was applied |
|---|---|---|
| V-1 | `change-course` | `64-VERDICT.md` front matter (`status: owner-signed`, `owner_decision: change-course`, `owner_decision_date: 2026-10-26`, `ruling_citation`, `ruling_sha256`) and its `## Owner sign-off` block; the charter's V-1 Owner cell |
| C-1 to C-14 | `open` | The charter's Owner cell copies `open`; **no other file changes for any of them** |

Left as they were, because the row is open:

| Row | Target | State |
|---|---|---|
| C-6 | the `10⁻⁵` held-out bar | untouched; the sign-off states the bar is neither retained nor replaced |
| C-7 | GAP-59-08 and how ε_H is measured | untouched; the sign-off states it stays undecided and GAP-59-08 stays open |
| C-12 | PROJECT.md title, What This Is, Core Value | byte-identical to the phase base `1ebb1d9b` |
| C-13 | PROJECT.md Model constraint | byte-identical to the phase base `1ebb1d9b` |
| C-14 | the twelve skipped-phase status cells | `Pending`, checkboxes unticked, no label |

The sign-off block follows the 43-VERDICT.md shape: Decision, Date, Meaning (the charter page's own consequence for change course: v2.5 opens with the trainex-r5 research round, open-book and diagnosis first, and runs no new long training until it explains the time-constant output), Items left open (all fourteen, listed), the open rows carried as open, and the Record (the ruling's path and SHA-256).

One test was replaced: `CharterRealTests::test_real_page_has_empty_owner_cells` asserted the pre-checkpoint state and is false by design once the Owner column is filled. It is now `test_real_page_owner_cells_match_the_ruling`: every Owner cell must be non-empty and must equal `parse_ruling(ruling)["answers"][row]`. The synthetic fixtures (`CharterCase`, `VerdictCase`, `RulingCase`) rebuild the pre-ruling charter and verdict from the committed files, so all 261 surviving controls still differ from the real document by exactly their mutation.

## Task 2 — the records and VER-22's binding count

- `REQUIREMENTS.md`: only the FEAS-06, FEAS-10 and VER-22 checkboxes and their three Traceability cells change, to `Complete`. Six lines of diff, no requirement text moved (`tests.phase60.test_amendment`, 21 tests, `OK`).
- `ROADMAP.md`: the Phase 64 list item is ticked with `(completed 2026-10-26, verdict RETHINK-REPRESENTATION; owner decision: change-course)`, all seven plan items are ticked, and the Progress row reads `64. Feasibility Verdict | 7/7 | Complete | 2026-10-26`.
- `STATE.md`: the Current Position block reads Phase 64 complete, a `### Decisions from Phase 64 (2026-10-26)` entry records the verdict, the decision, what stays open and who owns the next steps, and the counters are counted from the three v2.4 phase directories:

| Directory | PLAN | SUMMARY |
|---|---|---|
| `.planning/phases/59-read-only-baseline-scorecard` | 10 | 10 |
| `.planning/phases/60-single-system-learnability` | 23 | 23 |
| `.planning/phases/64-feasibility-verdict` | 7 | 6 (+1, this plan's own) |

`progress.total_plans` 40, `progress.completed_plans` 40, `progress.percent` 100. `status`, `stopped_at`, `last_updated`, `last_activity_desc`, `state_head` and `completed_phases` were left to the orchestrator, and no gsd-tools state, roadmap or requirements mutating verb was run.

VER-22's binding check, run on the final text after the last registry edit:

```
defined 24
table 24
roadmap 24
per-phase 59:5 60:4 61:8 62:2 63:2 64:3
status Complete 10
status Complete (recorded as skipped: no rescue) 2
status Pending 12
TRACEABILITY-OK
```

That certifies mapping completeness — every v2.4 requirement in exactly one phase, no orphans and no duplicates. It does **not** certify that any requirement is satisfied; VER-21's lineage lesson is that a passing count shows no orphans, not no gaps.

## Task 3 — the final check

`cmd_final` runs `inputs`, `frozen`, `traceability`, `numbers`, `derive`, `figure`, `rules`, `charter` and `ruling` in that order, then the completeness check, then prints `PHASE64-VERDICT-OK` as its very last line. `_timed(name, action)` prints one `elapsed <name> <seconds>` line per step. `final` includes `derive` and `figure` (the dataset is present on this Mac); the modes' own unit tests skip with a stated reason when it is absent.

The completeness check is the if-direction the `ruling` mode leaves out:

1. every Owner cell is filled and equals the ruling's recorded answer for its row;
2. the charter is `owner-decided` and cites the ruling;
3. the verdict is `owner-signed`, with V-1's token, the ruling's created date, its path and its SHA-256;
4. every approved PROJECT.md rewrite is applied and every unapproved one is absent;
5. C-14's label is applied, or the cells are left `Pending`, and the checkboxes stay unticked;
6. FEAS-06, FEAS-10 and VER-22 are ticked with `Complete` cells;
7. GAP-64-03 option A's criterion-3 reconciliation: the verdict's `### Cost to the next level` subsection, inside `## Cost on this Mac`, states "not estimable from this evidence" and cites `GAP-64-03`.

Real run on the committed tree (exit 0):

```
INPUTS-OK
elapsed inputs 0.458
frozen paths pinned=33 sealed=8 trees=4
FROZEN-OK
elapsed frozen 0.492
defined 24
table 24
roadmap 24
per-phase 59:5 60:4 61:8 62:2 63:2 64:3
status Complete 10
status Complete (recorded as skipped: no rescue) 2
status Pending 12
TRACEABILITY-OK
elapsed traceability 0.003
entries 365
NUMBERS-OK
elapsed numbers 0.794
cpu entries 136
DERIVE-OK
elapsed derive 4.623
figure times 1001
FIGURE-OK
elapsed figure 1.309
RULES-OK
elapsed rules 0.009
CHARTER-OK
elapsed charter 0.023
RULING-OK
elapsed ruling 0.150
elapsed completeness 0.056
PHASE64-VERDICT-OK
```

Hand mutant before the tests were written: emptying the V-1 Owner cell in the parser's output exits 1 with `verify_phase64_verdict FAIL-CLOSED: the charter row V-1 has an empty Owner cell` and prints no `PHASE64-VERDICT-OK`.

`FinalRealTests` (3 tests) checks the registration, the aggregate token last and exactly once, the nine tokens in order, and each token followed by its own `elapsed <mode>` line. `FinalCompletenessTests` (9 tests) patches all nine modes to pass, so each case can fail only in the completeness step, and asserts exit 1 without the aggregate token for: an approved C-12 that is not applied, one empty Owner cell, a verdict still `awaiting-owner`, an `owner_decision` that differs from V-1, an unticked FEAS-10, a `Complete` cell left `Pending`, C-14 approved but the cells still `Pending`, and the cost subsection without its `GAP-64-03` citation.

## Verification

| Command | Output |
|---|---|
| `verify_phase64_verdict.py ruling` | `RULING-OK` |
| `verify_phase64_verdict.py charter` | `CHARTER-OK` |
| `verify_phase64_verdict.py rules` | `RULES-OK` |
| `verify_phase64_verdict.py numbers` | `entries 365` / `NUMBERS-OK` |
| `verify_phase64_verdict.py traceability` | counts above, `TRACEABILITY-OK` |
| `verify_phase64_verdict.py final` | the block above, `PHASE64-VERDICT-OK` last |
| `verify_phase64_verdict.py frozen` | `frozen paths pinned=33 sealed=8 trees=4` / `FROZEN-OK` |
| `python -B -m unittest tests.phase64.test_verifier_phase64 -v` | `Ran 285 tests in 97.734s` / `OK` |
| `python -B -m unittest tests.phase60.test_amendment` | `Ran 21 tests in 2.064s` / `OK` |
| `python -B -m unittest tests.phase60.test_verifier_phase60` | `Ran 32 tests in 6.031s` / `OK` |
| `verify_phase60_evidence.py final` | `PROTOCOL-OK`, `PREFLIGHT-OK`, `RECORDS-OK`, `G2-OK`, `PHASE60-EVIDENCE-OK` |
| Phase 59 `scorecard-frozen` / `guardrails` | `SCORECARD-FROZEN-OK` / `GUARDRAILS-OK` |
| `git diff --quiet 1ebb1d9b -- .planning/PROJECT.md pinn_instruction` | exit 0, `PROJECT-AND-SPECS-UNTOUCHED` |
| `git show --name-only --format= 5a447624` | exactly `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md` |

The twelve skipped-phase rows still read `Pending` with unticked boxes: `CONF-10`, `CONF-11`, `INST-06`, `INST-07`, `SPEC-07`, `SPEC-08`, `SPEC-09`, `SPEC-10` (Phase 61), `GATE-05`, `FEAS-05` (Phase 62), `RUN-06`, `DIAG-08` (Phase 63) — checked one by one, 12 of 12 unticked.

## Deviations from the plan

1. **[Rule 1 — stale test expectations] The traceability tests pinned the pre-close status counts.** `TraceabilityRealTests.EXPECTED`, `TraceabilityPureTests.test_real_files_report_24` and `test_phase_outside_range_fails` asserted `status Complete 7` / `status Pending 15` and anchored on `| FEAS-06 | Phase 64 | Pending |`. Ticking the three Phase 64 requirements makes those false by design; they now read `Complete 10` / `Pending 12` and anchor on the `Complete` cell. No verifier logic changed for them.
2. **[process] The plan's Task 3 prescribes "run it on the real tree first, then write the tests", so the task did not follow the RED-first order its `tdd="true"` flag normally implies.** The real run and the hand mutant came first, then `FinalRealTests` and `FinalCompletenessTests`; no failing test was ever committed as RED.
3. **[Rule 1 — fixture precondition build] The `FinalCompletenessTests` fixture commits twice.** The first commit holds the phase base's `PROJECT.md`, the second the current tree; without the first, a future approved C-12 rewrite would make the fixture's base wrong. `commit()` skips an empty commit so the second is a no-op while `PROJECT.md` is unchanged.

## Observations for the orchestrator

- **The verdict's body still carries its pre-checkpoint status sentence.** Line 29 of `64-VERDICT.md` reads "**Status.** `awaiting-owner`. The agent's recommendation is `change-course`. The owner's decision is recorded at checkpoint ①, below, and is still pending." The plan's Task 1 says "Change nothing else" and the orchestrator's instruction says no other wording changes, so it was left exactly as it was; the front matter, the sign-off block, `ROADMAP.md` and `STATE.md` all state the signed state. A one-line follow-up edit is the owner's or the orchestrator's call.
- Three commits, one per task: `707a608e`, `5a447624`, `fee0223d`.
- `actuals.tokens` is chars/4 over the realized diff of this plan's seven files (47,494 bytes), not a harness token count, so it is comparable with the plan's 60,000 estimate.

## For the orchestrator

- **C-7 is `open`.** `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md` GAP-59-08 therefore **stays OPEN**: no amendment was written, no evaluator or gate was changed, and the sign-off makes no claim that the `10⁻⁵` bar was retained or replaced. There is no resolution to record in the gap register.
- **C-14 is `open`.** `.planning/phases/64-feasibility-verdict/64-GAPS.md` GAP-64-01 therefore **stays OPEN**: the twelve skipped-phase requirements keep `Pending` and unticked checkboxes, and **no label was applied** to the traceability table. There is no resolution to record in the gap register.
- This plan wrote no gap register, no spec, no amendment and no PROJECT.md edit. `git diff 1ebb1d9b -- .planning/PROJECT.md pinn_instruction` is empty.
- STATE's orchestrator-owned keys (`status`, `stopped_at`, `last_updated`, `last_activity_desc`, `state_head`, `completed_phases`) were left untouched. `/gsd-complete-milestone`, any merge of `milestone/v2.4` into master, any push and the GitHub backup remain the owner's or a separate agent's.

## Self-Check: PASSED

- `64-VERDICT.md`, `64-CHARTER.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, the verifier and the test file all exist and are committed.
- Commits `707a608e` (`docs(64-07): apply the owner answers from checkpoint 1`), `5a447624` (`docs(planning): close phase 64`) and `fee0223d` (`feat(64-07): add the final phase 64 check`) are in `git log 36dfc2c0..HEAD`.
- `RULING-OK`, `CHARTER-OK`, `RULES-OK`, `NUMBERS-OK`, `TRACEABILITY-OK` and `PHASE64-VERDICT-OK` were run and seen on the committed tree; the unit suite is 285 tests, `OK`.
- PROJECT.md, `pinn_instruction/` and the twelve skipped-phase status cells are unchanged: `git diff --quiet 1ebb1d9b -- .planning/PROJECT.md pinn_instruction` exits 0 and all twelve rows still read `Pending`.
