---
phase: 29-acceptance-checks-re-verification-and-handoff
plan: 01
subsystem: verification-governance
tags: [acceptance-checks, issue-ledger, traceability, roadmap-reconcile, ver-07, ver-08, ver-09]
requires:
  - 24-ISSUE-LEDGER.md (19-row Status Table; PSC row)
  - ctl_instruction.md / pinn_architecture.md (landed v1.5 contracts)
  - simulation_data/ (base + gold ID sets; not_in_gold.md)
  - 29-CODE-DIVERGENCE.md (FO-1 gold table, FO-2 PSC numeric defer)
provides:
  - 29-UAT.md (executed AC evidence surface; 13-check table + ledger audit + traceability)
  - run-ac-suite.sh + 11 disposable AC probes (fresh Phase-29 re-run)
  - reframed ledger PSC-row blocker (D-06); reconciled ROADMAP Progress row
affects:
  - 29-02-PLAN (29-HANDOFF.md + G1-G8 closure gate consume this evidence surface)
tech-stack:
  added: [bash+grep spec-consistency probes, python3 set-difference dataset probe]
  patterns: [positive-assertion + negative-control grep probe; anti-hardcode derived count]
key-files:
  created:
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/29-UAT.md
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/run-ac-suite.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-01.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-02.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-03.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-05.py
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-06.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-07.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-pipe-10.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-val-01.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-val-02.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-val-03.sh
    - .planning/phases/29-acceptance-checks-re-verification-and-handoff/ac-val-04.sh
  modified:
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
    - .planning/ROADMAP.md
decisions:
  - "AC-PIPE-08 has no standalone ledger row; re-run inside the M12/G5 family and noted under G5 (13 ledger-mapped result lines, all 14 probe IDs exercised)"
  - "ROADMAP reconcile touched both stale 'VAL-04/PSC user-deferred' occurrences (Progress row + Phase-28 milestone bullet) — the Task 3 verify requires zero anywhere; both are the same PSC-landed reconciliation, grounded by the committed PSC landing (D-01)"
metrics:
  duration: ~13 minutes
  tasks: 3
  files_created: 13
  files_modified: 2
  completed: 2026-06-17
---

# Phase 29 Plan 01: Acceptance-Suite Re-run, Ledger Audit, and Traceability Summary

Re-executed the full 13-check v1.5 acceptance suite as fresh disposable Phase-29 probes
(12 PASS + AC-VAL-04 structural-PASS/numeric-DEFERRED), audited the 19-row issue ledger to its
terminal state (18 VERIFIED + 1 DEFERRED), confirmed 36/36 roadmap traceability, reframed the
stale PSC-row blocker (D-06), and reconciled the stale ROADMAP Progress records to PSC-landed —
producing `29-UAT.md`, the executed evidence surface Plan 02's handoff + closure gate consume.

## What Was Built

**Task 1 — Ledger PSC-row reframe (D-06).** Edited only the PSC row (line 37) of the
`24-ISSUE-LEDGER.md` Status Table: still `DEFERRED`, but the superseded "wait for gold completion"
blocker is replaced by the D-06 framing (PSC clause LANDED; dedup-prefer-gold + `1/N_t`
composition ratified, GAP-28-03; AC-VAL-04 numeric calibration awaits the post-promotion pool at
FUT-01 FO-2). `git diff` confirmed the change is confined to line 37 — M13/G4 rows and their
OI-7b-partial notes are byte-identical (D-01a). Row-status enumeration: `NONTERMINAL []`,
`COUNTS 18 1`.

**Task 2 — Disposable AC suite (VER-07/09).** Authored 11 new probes
(`ac-pipe-01/02/03/06/07/10.sh`, `ac-pipe-05.py`, `ac-val-01/02/03/04.sh`) + `run-ac-suite.sh`,
and re-ran the 3 persisted Phase-27 probes (`ac-pipe-04/08/09.sh`) in place. Grep probes use the
established positive-assertion + negative-control pattern, transcribing landed `ctl_instruction.md`
clauses (no invented assertions). `ac-pipe-05.py` is a Python set-difference probe over
`simulation_data/` (base 2,749 − gold 2,565 == the 184 `not_in_gold.md` IDs, exact intersection):
**PASS @184/184** with 0 promoted (D-01/D-03), the count derived from parsed sets (no hard-coded
184/67). `ac-val-04.sh` asserts only the landed PSC clause structure and prints the numeric-DEFER
line — it computes no PSC value. `bash run-ac-suite.sh` exits 0: 12 PASS + AC-VAL-04 split. No
probe references `pinn/` (VER-09 / SCOPE-10); no spec or dataset file mutated.

**Task 3 — 29-UAT.md + ROADMAP reconcile (VER-07/08/09, D-01/D-05).** Authored `29-UAT.md`: the
14-row AC execution table (13 ledger-mapped; AC-PIPE-08 noted under G5), the 19-row ledger audit
(method = per-ROW Status field, not token count), a one-line REFERENCE to the
`29-CODE-DIVERGENCE.md` FO-1 gold table (not duplicated), and the 36/36 traceability confirmation
(Phase 29 = VER-07/08/09/11/12). Reconciled `ROADMAP.md`: Phase-28 Progress row 3/4 → 4/4 and the
Phase-28 milestone bullet (both VAL-04/PSC user-deferred → LANDED), Phase-29 row → In progress
(1/2), footer date 2026-06-14 → 2026-06-17.

## Verification

- `bash run-ac-suite.sh` → 13 result lines (12 PASS + AC-VAL-04 STRUCTURAL PASS / NUMERIC
  DEFERRED), exit 0.
- `python3 ac-pipe-05.py` → `AC-PIPE-05 PASS 184/184` (base=2749 gold=2565 not_in_gold=184
  promoted=0); no hard-coded expected count; no literal 184/67 in source.
- Ledger audit: `NONTERMINAL []`, `COUNTS 18 1` (18 VERIFIED + 1 DEFERRED, 0 non-terminal).
- `grep -lE 'pinn/'` over all probes → empty.
- `git status` of `not_in_gold.md` / `ctl_instruction.md` / `pinn_architecture.md` → unmodified.
- 29-UAT.md content + ROADMAP reconcile assertions → all pass (all 14 AC IDs present, gold-table
  referenced not duplicated, 184/184, 36/36, 18 VERIFIED / 1 DEFERRED, AC-VAL-04 split;
  0 'VAL-04/PSC user-deferred', footer date updated).

## Deviations from Plan

**1. [Rule 3 — Blocking] Probe negative-control line-scoping (AC-PIPE-02, AC-PIPE-03, AC-VAL-02).**
First suite run failed two checks; the asserted phrases ("NO code path may compute a path…",
"not a contract constant", "9-component aggregation is rejected") are line-wrapped in
`ctl_instruction.md`, so my multi-line `grep` scoping missed them. Fixed by asserting the
single-line token that actually carries each phrase. The clauses do contain the assertions; only
the probe's regex scoping was corrected. Re-run: 12 PASS + AC-VAL-04 split. (Fixed before the
Task 2 commit.)

**2. [Rule 3 — Blocking] `ac-pipe-05.py` docstring contained the literal `pinn/`.** The VER-09
"no probe references `pinn/`" check tripped on a docstring phrase ("touches no pinn/ code").
Reworded to "production model code" (the `pinn_*` spec paths in other probes use underscores and
never match `pinn/`). (Fixed before the Task 2 commit.)

**3. [Scope clarification, not a STOP] ROADMAP edit touched two occurrences of
"VAL-04/PSC user-deferred".** The plan action named the Progress row, but the Task 3 verify
requires zero occurrences anywhere; the second occurrence (the Phase-28 milestone bullet) carries
the identical stale framing. Both were reconciled to the PSC-landed state — the same D-01
planning-layer reconciliation, grounded by the committed PSC landing. Not a source-silent
decision (no STOP).

## STOP-Guard Status

No STOP-protocol trip. AC-PIPE-05 returned 184/184 as expected under D-01/D-03 (dataset
unmodified); the landed PSC clause was located for AC-VAL-04; the PSC reframe touched only the
PSC ledger row (M13/G4 byte-identical, D-01a); no PSC composition content was invented (only the
ratified dedup-prefer-gold + `1/N_t` rule transcribed); no gold promotion, no edit to
`not_in_gold.md` / `EXPECTED_ID_COUNT` / any AC count to 67 (all carried to FUT-01 FO-1); no
`pinn/` touch, no spec edit, no frozen/read-only-file edit.

## Self-Check: PASSED

All 13 created files present on disk; all 3 per-task commits (490b58d4, 3cf84861, bf0ec71e)
present in `git log`; `run-ac-suite.sh` exits 0.
