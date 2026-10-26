---
phase: 64-feasibility-verdict
plan: 05
subsystem: feasibility-verdict
tags: [charter, ruling, verifier, checkpoint, owner-quote]
requires:
  - 64-04 (the verdict, the numbers manifest and the figure)
provides:
  - "64-CHARTER.md: the one page the owner answers, with fifteen appendices"
  - "verify_phase64_verdict.py charter mode (page, quotes, drafts, content)"
  - "verify_phase64_verdict.py ruling mode (format and only-if applied checks)"
affects:
  - 64-06 (writes the ruling this mode reads)
  - 64-07 (applies the ruling to the charter, verdict, PROJECT.md and REQUIREMENTS.md)
tech-stack:
  added: []
  patterns:
    - fail-closed CLI verifier with synthetic negative controls
    - byte-equal owner quotes in opaque owner-quote fences
    - only-if checks on applied owner-dependent edits
key-files:
  created:
    - .planning/phases/64-feasibility-verdict/64-CHARTER.md
  modified:
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/test_verifier_phase64.py
decisions:
  - "The page limit counts both markers: the real page is 25 lines of the 60 allowed."
  - "The ruling mode checks applied edits only-if, so 64-06 can pass it before 64-07 applies anything; a blanket approval's C-6/C-7 rule stays in 64-06 because the owner's quote is never parsed."
  - "A changed: row authorises any change to its PROJECT.md segments or REQUIREMENTS.md status cells, because the owner's restatement lives in the opaque quote and is never machine-read."
  - "The ruling parser blanks fenced blocks before reading headings and tables, and requires the owner-quote block to be its section's only visible content, so a quote that closes its fence early is refused rather than trusted."
  - "rules scans the charter, and the ruling whenever it exists, after stripping owner-quote fences, so the owner's own words are never policed."
metrics:
  duration: 35 min
  completed: 2026-10-26
status: complete
actuals:
  tokens: 29421
  tasks: 3
  commits: 3
  plan_head_before: 6843bc7a153705bc7da800cab776b17f4cfdc667
---

# Phase 64 Plan 05: The one-page charter and the checkpoint ① ruling check

## One-liner

A fifteen-row, pre-filled project charter (V-1 and C-1 to C-14) with its appendices, a `charter` mode that checks every row, quote, draft and number, and a `ruling` mode that refuses to pass until the owner answers and then admits only the edits the recorded answers authorise.

## What was built

### Task 1 — the page and its check (tracer)

`.planning/phases/64-feasibility-verdict/64-CHARTER.md` now holds the front matter (`phase64-charter/v1`, `awaiting-owner`, `ruling_citation: pending`), the Audience line, the plain-language lead, and the page between `<!-- page:begin -->` and `<!-- page:end -->`: a five-column table with exactly the fifteen rows V-1, C-1 to C-14 in order, every recommended answer pre-filled, every Owner cell empty, and the fixed `REPLY_RULE_C6_C7` sentence once. `cmd_charter` checks the markers, the 60-line limit, the header and separator, the row order and shape, the V-1 wording, the recorded rows, the option letters each row offers (C-6, C-8, C-12 and C-13 offer no C), C-5's conditionality on C-7, the reply note, and that no Owner cell is filled while no ruling exists.

### Task 2 — the appendices and their checks

Every appendix now carries its evidence, options and recommendation: the three owner-quote blocks (D-07 in C-1; D-06's latest and earlier statements as two separate blocks in C-9), the D-12 stop rule in plain text in C-10, GAP-59-08's floor values and options in C-7, the D-11 measured costs and the for-scale figure in C-9, the three frozen `ctl_instruction.md` anchors in C-11, the four PROJECT.md draft blocks in C-12 and C-13, and GAP-64-01's twelve IDs and three labels in C-14. `cmd_charter` now also checks the quotes byte-for-byte against 64-CONTEXT.md, the amendments document's owner's lean, the draft blocks' placement and non-emptiness, the per-section tokens, C-5's three conditional options, the C-14 IDs and labels, and the unticked checkboxes. `cmd_rules` scans the charter (and the ruling when present) for guarded Mac-cost wording, banned phrasings and the host home prefix after stripping owner-quote fences. `cmd_numbers` requires all 32 charter-required manifest entries to render in the charter.

### Task 3 — the ruling mode

`parse_ruling` reads the ruling's front matter, its three headings, the one owner-quote block, the fixed message-count sentence and the fifteen Recorded answers rows, validating each token against the options the charter's page row offers (V-1: continue/change-course/stop; C-1/C-3/C-11: recorded/open; the rest: an offered letter or open; any row: `changed: <restatement>`). `cmd_ruling` first requires the ruling to exist, be tracked and be clean; then `_check_ruling_applied` checks every applied owner-dependent edit only-if: a filled Owner cell, a set verdict `owner_decision`, `owner_decision_date` or `ruling_sha256`, a changed PROJECT.md segment under C-12 or C-13, and a non-Pending status among the twelve skipped-phase requirements. `project_segments` compares HEAD against `PHASE_BASE`; under A a changed segment must equal the charter's draft, under B or open it must stay at the base, and under `changed:` any change is allowed. `_check_ruling_commit_order` requires every commit after the phase base that touches PROJECT.md or REQUIREMENTS.md to descend from the ruling's adding commit.

## Verification

- `python -B -m unittest tests.phase64.test_verifier_phase64 -v` — **Ran 273 tests, OK**.
- `verify_phase64_verdict.py charter` — `CHARTER-OK`.
- `verify_phase64_verdict.py rules` — `RULES-OK`.
- `verify_phase64_verdict.py numbers` — `entries 365`, `NUMBERS-OK`.
- `verify_phase64_verdict.py frozen` — `frozen paths pinned=33 sealed=8 trees=4`, `FROZEN-OK`.
- `verify_phase64_verdict.py ruling` — exit 1, `FAIL-CLOSED: the ruling does not exist: .planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md`.
- `sed -n '/<!-- page:begin -->/,/<!-- page:end -->/p' 64-CHARTER.md | wc -l` — `25` (limit 60).
- `test ! -e .planning/phases/64-feasibility-verdict/64-CHECKPOINT-1-RULING.md && echo NO-RULING` — `NO-RULING`.
- `git diff --quiet HEAD -- .planning/PROJECT.md pinn_instruction && echo PROJECT-AND-SPECS-UNTOUCHED` — `PROJECT-AND-SPECS-UNTOUCHED`.
- `shasum -a 256 .planning/phases/64-feasibility-verdict/64-CHARTER.md` — `03b9016edea2aca965253260bd18eb1f84b46dcffde3de9a9faa580fada81bc6`.

Hand mutants, each applied, observed to fail the intended check, and reverted:

- Task 1: `PAGE_MAX_LINES = 61` made the 61-line control pass instead of fail.
- Task 2: changing `For now, the only device` to `For now the only device` in the C-9 quote made `charter` exit 1 with "the first C-9 owner quote is not byte-equal".
- Task 3: relaxing `len(words_blocks) != 1` to `< 1` made the two-owner-quote control pass instead of fail.

## Deviations from Plan

None — the plan executed as written. Two implementation choices are recorded under `decisions` above: the ruling parser's structural refusal of an early-closing quote, and `changed:` rows being unverifiable against the opaque quote.

## Auth gates

None.

## Known Stubs

None. Every value on the page is either a recorded owner answer, a pre-filled recommendation the owner may change, or a manifest-rendered number; every Owner cell is intentionally empty until checkpoint ①.

## Threat Flags

None beyond the plan's threat model. The charter introduces no executable surface; the ruling mode adds git read-only subprocess calls with fixed argv lists.

## Commits

| Commit | Subject |
|---|---|
| `b65e46d0` | `docs(64-05): write the one page charter and its check` |
| `04dadd6a` | `docs(64-05): complete the charter appendices and checks` |
| `47bea1e5` | `feat(64-05): add the checkpoint 1 ruling check` |

## Self-Check: PASSED

- `64-CHARTER.md` exists at `.planning/phases/64-feasibility-verdict/64-CHARTER.md`.
- `verify_phase64_verdict.py` exists and registers `charter` and `ruling`.
- `tests/phase64/test_verifier_phase64.py` exists and holds 273 passing tests.
- Commits `b65e46d0`, `04dadd6a` and `47bea1e5` are in `git log`.
- No ruling file exists, no Owner cell is filled, and PROJECT.md and `pinn_instruction/` are untouched at HEAD.
