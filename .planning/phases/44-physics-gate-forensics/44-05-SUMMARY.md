---
phase: 44-physics-gate-forensics
plan: 05
wave: 3
requirements: [DIAG-04]
status: complete
---

# 44-05 Summary — 44-DIAGNOSIS.md (ranked, remedy-abstinent diagnosis)

## Objective
Produce the hypothesis-ranked, evidence-cited diagnosis report that explicitly
abstains from selecting a remedy (DIAG-04) — Phase 45's trainex-r2 centerpiece.

## What was built
- `44-DIAGNOSIS.md` — the diagnosis report.

## Key content (verified)
- **Both gate criteria addressed:** ε_H (1500/1500 exceed `1e-5`, uniform failure)
  and aggregate SCS (`2.3751…` vs `-5.0`); states no per-trajectory SCS exists
  in the preserved artifact, without speculating why.
- **Pre-registered ranking rubric** (evidence-support; Strong/Moderate/Weak;
  alphabetical tie-break) stated BEFORE the table.
- **5 ranked candidate causes** (≥4 required): population-scale generalization
  shortfall (Strong); loss-term imbalance, optimization/warmup pathology,
  normalization/data-scale mismatch (Moderate tie, declared); insufficient
  budget (Weak). Each row carries supporting evidence + contradicting evidence
  (or the explicit "none" sentence) + a proposed-but-never-executed
  discriminating test.
- **Verified-fact vs agent-hypothesis** separated inline throughout (`[FACT]` /
  `[HYP]`), for PKG-11.
- **GAP-44-01** referenced (max 237.21 and mean 5.62 both quoted; neither
  designated as the gate statistic). Verdict-neutral (FAIL under any aggregate).
- **Remedy abstinence** stated up front and in §7; no remedy recommended.

## Verification
- Watchdog verify gate `test -s …/44-DIAGNOSIS.md` passes.
- **Pre-shipping re-run (D-02):** all three diag outputs byte-unchanged vs
  committed; 15/15 manifest input hashes match the live tree; `manifest.json`
  `cross_check.all_match: true`, `git_head = 8631576…`.
- Every cited number traces to a diag output field or a cited file.

## Deviations
None. The plan executed as specified.
