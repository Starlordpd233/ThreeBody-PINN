---
phase: 39-data-ingestion-stage-0-population-scan
plan: 14
subsystem: DATA (validation ledger)
tags: [gap-closure, ledger-integrity, assertion-liveness, vacuous-pass, DATA-01, DATA-02, DATA-06, T-39-LC2, T-39-LC3, T-39-08]
dependency_graph:
  requires: [39-10, 39-13]
  provides: [live-status-assertion]
  affects: [39-VALIDATION.md row 39-10-02, 39-13-SUMMARY.md FINDING-1]
tech_stack:
  added: []
  patterns: [restoration-from-authoritative-text, differential broken-vs-fixed liveness proof, string-diff edit verification, observed-exit-only status]
key-files:
  created:
    - .planning/phases/39-data-ingestion-stage-0-population-scan/39-14-SUMMARY.md
  modified:
    - .planning/phases/39-data-ingestion-stage-0-population-scan/39-VALIDATION.md
decisions:
  - "The repair is a restoration, not a composition. The corrected awk body was taken from the authoritative command at 39-10-PLAN.md:115 and asserted character-for-character equal to it, rather than newly composed. No judgement about what the assertion 'should' say was exercised."
  - "39-13-PLAN.md:137's prohibition on modifying row 39-10-02's command was read as an anti-weakening rule ('do not modify row 39-10-02's command to add an exclusion ... widening a historical row's exclusion set would weaken it'). Restoring the brace strengthens the row, which is the opposite action, so the prohibition does not bar it. The exclusion set was asserted to remain exactly {39-10-02} to prove no weakening occurred under cover of the repair."
  - "The edit was verified by difflib SequenceMatcher opcodes over the pre- and post-edit command strings, not by eyeball. The proof is that exactly one opcode exists, it is an insert, and the inserted text is exactly '}' — mechanically excluding any other change hiding in a 693-character command."
  - "Liveness was proven differentially, running BOTH the broken and the corrected awk against the same forced-red scratch copy. A one-sided test (fixed awk fires) shows the fixed version works but not that the old version was defective; the differential shows the exact behavioural delta being bought."
  - "awk's stderr was discarded (2>/dev/null), never folded into the captured stdout. Capturing stderr makes the BROKEN awk appear to correctly report a failure (its syntax error lands on stderr), masking the vacuity. This mistake was made once during the original investigation and was deliberately not repeated."
  - "Row 39-13-02 was inspected and already carries the closing brace; the defect is isolated to row 39-10-02. No other row was touched."
  - "39-13-SUMMARY.md finding 2 (the inert `! rg -q` assertion) was left untouched per the plan's explicit out-of-scope instruction — it is a broader multi-row schema question, and its underlying criterion is independently confirmed satisfied."
metrics:
  duration: ~12min
  completed: "2026-07-16"
  tasks: 1/1
  files: 1 changed (1 character inserted)
  ledger_rows: 29/29 green
status: complete
---

# Phase 39 Plan 14: Restore Row 39-10-02's Assertion Liveness Summary

Row 39-10-02's status assertion can now fail. Its awk was missing one `}`, so awk aborted with a syntax error, wrote nothing to stdout, and the enclosing `test -z "$(awk ...)"` succeeded unconditionally — the row's central claim (every other row is green) was structurally incapable of being violated.

## One-liner

A one-character restoration from `39-10-PLAN.md:115` that converts row 39-10-02 from a vacuous pass into a live assertion, proven by running the broken and corrected awk side-by-side against the same forced-red ledger copy.

## Tasks Executed

| Task | Name | Type | Commit | Files |
|------|------|------|--------|-------|
| 39-14-01 | Restore row 39-10-02's awk closing brace | auto | `06130c6` | 39-VALIDATION.md |

## What Was Built

### The defect, reproduced before the repair

The row's awk program body opened an action block and never closed it:

```
... if (id != "39-10-02" && status != "✅ green") print id
```

Run against the real ledger, the broken awk exits **2** with empty stdout. Because command substitution discards the inner exit status, `test -z "$(awk ...)"` sees an empty string and succeeds. Every possible ledger state passed this row.

### The repair

One `}` inserted at offset 684 of a 693-character command, taken from the authoritative text at `39-10-PLAN.md:115`, which has always carried the brace:

```
-... print id" "$v")"'
+... print id}" "$v")"'
```

`git diff --word-diff` isolates the whole change to `-id"` → `+id}"`.

## Verification Performed

| Check | Method | Result |
|---|---|---|
| Edit is exactly one `}` insertion | `difflib.SequenceMatcher` opcodes over pre/post command strings; asserted single `insert` opcode of text `}` and `pre[:i] + "}" + pre[i:] == post` | PASS — 1 opcode: `('insert', 684, 684, 684, 685)` |
| awk body matches authoritative source | String equality of the extracted awk body vs `39-10-PLAN.md:115` | PASS — character-for-character |
| Exclusion set not widened | Count of `id !=` comparisons; extracted excluded ids | PASS — exactly 1, exactly `{39-10-02}` |
| Assertion is LIVE (differential, stderr NOT captured) | Broken vs corrected awk against the same scratch copy with `39-01-01` forced `❌ red` | PASS — broken: stdout `''` → `test -z` **passes** (vacuous); corrected: stdout `39-01-01` → `test -z` **fails** (fires correctly) |
| Real ledger clean | Corrected awk vs the real all-green ledger | PASS — exit 0, empty stdout |
| Row command end-to-end | Row 39-10-02's full command extracted verbatim from the ledger and `eval`'d | PASS — **exit 0**, observed |
| Row command fails on a red ledger | Same full command against the forced-red scratch copy | exit 1 — the row now genuinely fails when a row is not green |
| No status cell changed | SHA-256 of the row→status pair list, pre vs post | PASS — `65981c06…` identical, 29 rows, all `✅ green` |
| Scope | `git diff --name-only -- .planning/phases/` | PASS — only `39-VALIDATION.md` |
| Evidence untouched | `git status --short` on `evidence/` and `simulation_data` | PASS — clean |
| Whitespace | `git diff --check` | PASS — clean |

Command SHA-256: `67aed981daa841ec84c96b2da9c0f1f6e203139487eaf31cba903c4a9be26d54` (pre, 693 bytes) → `6f4c2a8ec42e0b34b947ecb77903e2659aa9e8996592c440804b0d5e6e96828c` (post, 694 bytes).

The scratch copy was written outside the repository and deleted afterward. No red status was ever written into the real ledger.

## Status Provenance

Row 39-10-02's `✅ green` is **retained from an observed exit**: its full command, extracted verbatim from the ledger cell, was `eval`'d against the real ledger and observed to exit 0 after the repair. The status was not carried forward on the strength of the pre-repair record — that record was worthless, since the row could not have failed.

## Deviations from Plan

None — plan executed exactly as written. No deviation rule was triggered.

## Known Stubs

None.

## Threat Flags

None. No new security-relevant surface: the change is a one-character edit to a planning-artifact assertion.

## Deliberately Out of Scope

- **39-13-SUMMARY.md finding 2** — the inert `! rg -q ...` hygiene assertion (bash exempts `!`-inverted commands from errexit, and the pattern self-matches). Affects several rows; a broader schema question; its underlying criterion is independently confirmed satisfied. Left for owner decision, per this plan's explicit instruction.
- **UAT Test 24 / phase completion** — gated on `/gsd-verify-work 39` re-running.

## What This Closes

`39-13-SUMMARY.md` FINDING-1 (HIGH), which recorded the defect but correctly declined to fix it under `39-13-PLAN.md:137`, and the execute-phase orchestrator's independent reproduction. The finding is now resolved rather than deferred.

## Self-Check: PASSED

- `39-14-SUMMARY.md` — FOUND
- `39-VALIDATION.md` modified, single-line diff — FOUND
- Commit hash — recorded in the Tasks Executed table
