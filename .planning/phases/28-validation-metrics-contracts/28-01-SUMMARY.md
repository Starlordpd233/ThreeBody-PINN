---
phase: 28-validation-metrics-contracts
plan: 01
subsystem: validation-metrics
tags: [scs, validation-gate, ctl, evidence-ledger]
requires:
  - phase: 27-sampling-precision-and-global-scale-contracts
    provides: PIPE-09 raw-mass compute_globals convention consumed by SCS invariance
provides:
  - canonical SCS validation-gate contract in ctl_instruction.md Step-1A
  - AC-VAL-01 structural verification result
  - SCS ledger row VERIFIED with evidence-packet transition log
affects: [phase-28, phase-29, fut-01, ctl_instruction]
tech-stack:
  added: []
  patterns:
    - inline structural acceptance check recorded in SUMMARY
    - two-phase pending-SHA backfill for ledger provenance
key-files:
  created:
    - .planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md
key-decisions:
  - "VAL-01 was treated as transcription of the locked accept-resolution verdict, not re-adjudication."
  - "AC-VAL-01 is recorded inline rather than as a new file so the substantive commit stays within the four 28-01 owned paths."
patterns-established:
  - "Validation metric contracts cite their evidence packet and keep rejected issue-doc numbers in rejection-only context."
requirements-completed: [VAL-01]
duration: 6 min
completed: 2026-06-16
---

# Phase 28 Plan 01: SCS Contract Summary

**Canonical SCS validation-gate contract reconciled into CTL Step-1A with evidence-backed threshold disposal and PIPE-09 regression proof**

## Performance

- **Duration:** 6 min
- **Started:** 2026-06-16T03:52:00Z
- **Completed:** 2026-06-16T03:57:52Z
- **Tasks:** 3/3 complete
- **Files modified:** 4

## Accomplishments

- Reconciled the existing Step-1A conservation gate into the canonical SCS contract: `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, REJECT if `SCS > -5`, with the tie, band-table, near-zero-`|H(0)|`, `eps_H = 0`, Plummer `eps = 1e-10`, and per-trajectory storage rules preserved.
- Added the Phase 28 commentary required by the locked verdict: raw/scaled invariance (`H' = D*H`), dual-`eps_H` symbol hygiene against `pinn_architecture.md` training `eps_H = 1e-4*S_H`, explicit rejection of issue-02 `1e-6`/`1e-8`, and citation of `scs-thresholds.md`.
- Advanced the SCS issue-ledger row and `scs-thresholds.md` status log through `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, then backfilled the substantive commit SHA.
- Verified the PIPE-09 `compute_globals` region remained byte-identical after the SCS edit.

## Task Commits

1. **Task 1: Verify locked SCS verdict and author AC-VAL-01** - `bd31dcd` (spec)
2. **Task 2: Reconcile canonical SCS contract into CTL** - `bd31dcd` (spec)
3. **Task 3: PIPE-09 re-check and ledger/evidence close** - `bd31dcd` (spec)

**Provenance backfill:** expected follow-up commit `verify(28-01): backfill commit sha`.

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Reconciled the Step-1A SCS clause and added invariance, symbol-hygiene, ratio-threshold rejection, EVID-10 citation, OI-2 deferral, and companion-metric forward pointer.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` - Moved SCS to VERIFIED, updated the Spec Section cell to the CTL Step-1A canonical home with DQA retained as read-only/historical home, and appended transition-log entries.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md` - Appended the matching Phase 28 VAL-01 transition-log entries.
- `.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md` - Captured AC-VAL-01, PIPE-09, and closeout evidence.

## Decisions Made

- VAL-01 remained a locked-verdict transcription. No new Q-C1 fork or STOP gap surfaced while reconciling the sources.
- The AC-VAL-01 check is kept inline here, not as a new committed script, to avoid adding a fifth owned file beyond the plan's same-commit scope.

## AC-VAL-01

Pre-edit discriminating run against `HEAD`/current CTL before the SCS reconciliation:

```text
PASS: formula
PASS: band_table_and_tie
PASS: quarantine_and_plummer
FAIL: ratio_thresholds_rejected
FAIL: scs_packet_citation
FAIL: invariance_and_symbol_hygiene
RESULT: FAIL (ratio_thresholds_rejected, scs_packet_citation, invariance_and_symbol_hygiene)
```

Post-edit run against the reconciled `ctl_instruction.md`:

```text
PASS: formula
PASS: band_table_and_tie
PASS: quarantine_and_plummer
PASS: ratio_thresholds_rejected
PASS: scs_packet_citation
PASS: invariance_and_symbol_hygiene
RESULT: PASS
```

Rerunnable command:

```bash
python3 - <<'PY'
from pathlib import Path
import re, sys
path = Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md')
text = path.read_text()
m = re.search(r'5\. Conservation gate[\s\S]*?(?=\n6\. Physical invariant gates)', text)
if not m:
    print('FAIL: Step-1A SCS conservation-gate clause not found')
    sys.exit(1)
block = m.group(0)
checks = [
    ('formula', 'SCS = log10(eps_H)' in block and 'SCS > -5' in block and 'eps_H > 1e-5' in block),
    ('band_table_and_tie', all(s in block for s in ['Excellent <= -10', 'Acceptable (-10,-6]', 'Marginal (-6,-5]', 'Reject > -5', 'SCS = -5']) and re.search(r'SCS = -5[^.]*Marginal', block) is not None),
    ('quarantine_and_plummer', all(s in block for s in ['eps = 1e-10', '|H(0)|', 'QUARANTINE'])),
    ('ratio_thresholds_rejected', all(s in block for s in ['1e-6','1e-8']) and all(re.search(r'.{0,100}'+re.escape(s)+r'.{0,140}', block, re.I|re.S) and re.search(r'(reject|rejected|mis-promoted|unsourced|not transcribed)', re.search(r'.{0,100}'+re.escape(s)+r'.{0,140}', block, re.I|re.S).group(0), re.I) for s in ['1e-6','1e-8'])),
    ('scs_packet_citation', 'scs-thresholds.md' in block),
    ('invariance_and_symbol_hygiene', all(s in block for s in ["H' = D*H", '1e-4', 'S_H']) and re.search(r'distinct|different', block, re.I) is not None),
]
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f'{"PASS" if ok else "FAIL"}: {name}')
if failed:
    print('RESULT: FAIL (' + ', '.join(failed) + ')')
    sys.exit(1)
print('RESULT: PASS')
PY
```

## PIPE-09 Regression Re-Check

Extraction command:

```bash
awk '/Normative `compute_globals` contract/{f=1} /^### 2\.6/{f=0} f' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

Hashes:

```text
HEAD baseline: 816589102aea99f2878991bda9cee351db08e8d2cd5c64fbe725c551a825b986
worktree after SCS edit: 816589102aea99f2878991bda9cee351db08e8d2cd5c64fbe725c551a825b986
```

Result: PIPE-09 `compute_globals` region byte-stable; no regression. The `D=6.694` ledger row remains VERIFIED.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Self-Check: PASSED

- AC-VAL-01 passed all six structural assertions plus the ratio-threshold negative control.
- PIPE-09 `compute_globals` extraction matched `HEAD` byte-for-byte at SHA-256 `816589102aea99f2878991bda9cee351db08e8d2cd5c64fbe725c551a825b986`.
- `data_quality_assessment.md` was not modified.
- SCS issue-ledger row is VERIFIED with AC-VAL-01, `scs-thresholds.md`, CTL Step-1A, DQA historical-home, and 2026-06-16 provenance.
- `scs-thresholds.md` transition log carries the Phase 28 Plan 01 transitions with substantive commit `bd31dcd`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 28-02. The Step-1A SCS gate now contains the forward pointer to the later `Data-side quality-metric contracts` subsection; 28-02 should create that subsection if still absent and add the SASD reciprocal back-reference.

---
*Phase: 28-validation-metrics-contracts*
*Completed: 2026-06-16*
