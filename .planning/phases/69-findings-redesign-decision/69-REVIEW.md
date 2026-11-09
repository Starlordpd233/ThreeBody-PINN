---
phase: 69-findings-redesign-decision
reviewed: 2026-11-09T04:16:00Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - .planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py
  - tests/phase69/test_verifier_phase69.py
findings:
  critical: 4
  warning: 3
  info: 0
  total: 7
status: issues_found
remediation_status: resolved
open_findings: 0
---

# Phase 69 code review

**Reviewed:** 2026-11-09T04:16:00Z  
**Depth:** standard  
**Files reviewed:** 2  
**Status:** issues_found

## Summary

This report covers the verifier and tests introduced in `0f53ab64061a1998e2df2a082149f087ee6c4b03`. The traceability check accepted an unrelated milestone and malformed mappings in memory. The evidence builder accepted an endpoint with a different configured window from its registration. The accounting builder refused a valid incomplete attempt with no result file. The checked live inputs contained none of these mutations. All three EXP-03 control records matched their publication bytes, and the cited diagnostic implementation files matched their original registration digests. The existing 31-test result came from the execution workflow. This review used focused read-only probes.

## Narrative Findings (AI reviewer)

### Critical issues

### CR-01: Bind the Phase 69 success marker to v2.5

**Severity:** BLOCKER  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:609-635`

**Issue.** The checker accepts whichever milestone is named at the start of REQUIREMENTS.md and finds a matching roadmap heading. Replacing `v2.5` with `v9.9` in copies of both live files returned `valid=True`, `milestone=v9.9` and 13 definitions. A subsequent milestone with internally consistent planning files could therefore yield the Phase 69 success marker. VER-23 requires the final v2.5 mapping.

**Fix.** Require the active title and roadmap heading to identify `v2.5`. Continue deriving requirement IDs, phase numbers and counts dynamically. Add a test with consistent non-v2.5 inputs and require failure.

### CR-02: Reject hidden duplicates and malformed rows in the live mapping

**Severity:** BLOCKER  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:598-629`

**Issue.** The definition and row patterns accept only column-zero entries, treat fenced examples as active Markdown and read only the first two table cells. In separate in-memory copies of the live inputs, the checker returned `valid=True` and 13 definitions after adding a two-space-indented duplicate DIAG-09 definition, adding a two-space-indented duplicate DIAG-09 mapping row, adding a `Phase 66` cell to its mapping row, or moving the actual DIAG-09 definition inside a fenced `md` block. The same parser misses real multiplicity and counts quoted examples as definitions.

**Fix.** Exclude fenced code before locating active headings and entries. Account for Markdown indentation in both inventories. Validate the table header and require exactly the declared columns and a single phase cell for every data row. Add one regression fixture for each reproduced mutation.

### CR-03: Check registered window and metric route before joining review labels

**Severity:** BLOCKER  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:196-225,513-528`

**Issue.** The full identity index is discarded before the review join. The replacement lookup keys by `(case, arm)` and accepts a review label if E and tier match. `fit_row` also skips the physical window in the original registration. Changing only `record["orbit"]["window"]["configured_length"]` to `9.0` on the main EXP-03 control produced a row labelled `settled` under the unchanged 0–10 registration and review. The committed inventory comparison catches a mutation against an unchanged inventory. The derivation still accepts the conflicting evidence when rebuilding that inventory.

**Fix.** Check each scored row against the as-captured registration's window and the registered endpoint metric route before joining. Require exactly one row for each review case, arm, window, state and metric route. Preserve distinct source rows and fail when the review has insufficient identity to select one. Add a one-field window mutation fixture and an ambiguous route fixture.

### CR-04: Keep incomplete attempts that have no published result

**Severity:** BLOCKER  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:410-445`

**Issue.** The code opens the adjacent `record.json` for every non-probe attempt before looking at its status. The diagnostic producer writes the claim first and marks it incomplete if data setup or the worker fails before result publication (`pinn/verification/diagnostic_fit.py:1533-1591`). An in-memory fixture with a valid `incomplete` claim, a two-second UTC interval and no tracked result aborted `build_cost` at the missing record. The existing partial-attempt test calls `summarize_activities` after the stage that drops this supported record shape. The plan requires retaining failed and partial attempts.

**Fix.** Look for the result in the tracked census and validate it when present. Require it for a `published` claim. For a claim-only incomplete attempt, preserve the claim's identity and UTC interval, mark its fit wall unknown with a reason and omit it from the published count. Test this through `build_cost`, with a paired test that a published claim lacking its result still fails.

### Warnings

### WR-01: Validate a timestamp even when its partner is missing

**Severity:** WARNING  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:353-364`

**Issue.** The early return treats malformed supplied data as unknown whenever the other endpoint is absent. `utc_interval("not a timestamp", None)` returned `None`. This hides a corrupt value inside an otherwise legitimate partial record.

**Fix.** Parse and validate each non-null UTC endpoint first. Return `None` if either validated endpoint is absent. Test both combinations of one absent value and one malformed value.

### WR-02: Hash the exact live planning bytes

**Severity:** WARNING  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:675-689`

**Issue.** `Path.read_text()` normalizes line endings. The resulting report hashes the decoded and re-encoded text, so a CRLF checkout has a different on-disk SHA-256 from the reported source identity. This was reproduced in memory with the live REQUIREMENTS.md bytes converted to CRLF. Plan 69-03 uses those hashes to bind the capture to the final live sources.

**Fix.** Read each source once with `read_bytes()`. Hash those bytes and decode the same buffer for parsing. Add a CRLF fixture whose reported digest matches `hashlib.sha256` over the fixture bytes.

### WR-03: Reject conflicting duplicate keys in the inventory JSON

**Severity:** WARNING  
**File:** `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py:591-595,693-705`

**Issue.** `json.loads` silently keeps the last value for a repeated key. An inventory containing an altered `sources` object followed by the expected `sources` object decoded as the expected object alone. The comparison can therefore accept an ambiguous inventory and another reader can see different evidence.

**Fix.** Use an `object_pairs_hook` that rejects repeated keys while loading the inventory. Test a duplicate top-level key and a duplicate nested evidence field with the expected value last.

## Closeout remediation, 2026-11-08

The original findings above apply to `0f53ab64061a1998e2df2a082149f087ee6c4b03`.
All seven were addressed in the Phase 69 closeout. The recorded experiment and
accounting values still reproduce from the same committed evidence.

| Finding | Change and check |
|---|---|
| CR-01 | Restrict the check to the active v2.5 milestone while deriving IDs and counts from the live files. The retitled milestone fixture fails. |
| CR-02 | Count indented definitions and table rows, exclude fenced examples and validate the mapping columns. Fixtures reject hidden duplicates, fenced entries, an extra phase column and an altered header. |
| CR-03 | Verify original registration window bounds and configured length, enforce the diagnostic metric route and reject multiple scored rows for a review case and arm. Mutating a window or the velocity route causes rejection. |
| CR-04 | Retain an incomplete claim without a published record, with unavailable duration fields unknown. A published claim missing its result fails. |
| WR-01 | Parse each supplied UTC endpoint. Tests reject malformed input even with the other endpoint absent. |
| WR-02 | Read exact source bytes and normalize line endings only for Markdown parsing. The CRLF fixture verifies both raw SHA-256 values and a fresh read after editing. |
| WR-03 | Reject duplicate inventory JSON keys at any depth. Both top-level and nested duplicate fixtures fail. |

The rejection fixtures exposed the original behavior before the changes.
After the fixes, all 39 Phase 69 tests passed. The full `verify_phase69.py all`
reconstruction passed, with the checked source and cost inventory unchanged.
