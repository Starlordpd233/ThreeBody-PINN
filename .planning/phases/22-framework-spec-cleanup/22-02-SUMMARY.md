---
plan_id: 22-02
title: pinn_architecture.md GFM Table Conversion + Math Normalization
executed: 2026-06-09
status: BLOCKED
detector_exit: 1
blocker: GAP-22-03
---

# Plan 22-02 Execution Summary

## Objective
Convert all Pandoc multiline tables in `pinn_architecture.md` to GFM format and normalize all bare multi-character subscripts/superscripts to LaTeX math, achieving G2 (detector exit 0).

## Completed Work

### Task 1: Pandoc Multiline Table Conversion ✓
- **Tables converted:** 2/2
  - Architectural hyperparameters (12 data rows, 12 columns, 3 footnote references)
  - Consolidated implementation blueprint (13 data rows, 3 columns, 1 footnote reference)
- **Method:** Programmatic extraction using column separator detection and cell-boundary parsing
- **Verification:** All cell content preserved byte-for-byte, footnote references maintained as `[^n]`
- **Commit:** `ac601e9` "fix(22-02): convert Pandoc multiline tables to GFM in pinn_architecture.md"

### Task 2: Math Normalization (Partial) ✓
- **D3 bare subscripts fixed:** 23 instances → 0 instances
  - `$L_total$`, `$L_data$`, `$L_IC$`, `$L_phys$`, `$L_E$`, `$L_L$` → `$L_{total}$`, etc. (all loss functions)
  - `$epsilon_H$` → `$\epsilon_H$`
  - Inline math in table cells corrected
- **D5/D6 backtick-wrapped math fixed:** 3 instances
  - `` `ΔH_n` `` → `$\Delta H_n$`
  - `` `10^-5` `` (duplicate note) removed
  - `` `epsilon_H` `` → `$\epsilon_H$` (multiple instances)
- **Other fixes:**
  - Line 651-653: Collapsed multi-line math block to single line
  - All 39 Pandoc footnote references `[^n]` and definitions `[^n]:` preserved (not converted to `[n]`)
  - Heading `## Footnotes` renamed to `## References`

## Detector Status After Completed Work

```
DEFINITE findings: 0
REVIEW findings: 7 (all D5/D6 code identifiers)
Exit code: 1
```

### Remaining REVIEW Findings (Code Identifiers)

The detector's D5/D6 layers (backtick/prose math near author comments) flag 7 PyTorch parameter names because they're within the ±20-line oracle window of author comments:

1. L170: `first_omega_0`
2. L178: `hidden_omega_0`, `hidden_omega_0 = 1`
3. L188: `\text{xxx}` (in author comment text)
4. L236: `elementwise_affine=False`
5. L238: `elementwise_affine=True`
6. L259: `elementwise_affine=False`
7. L260: `first_omega_0`
8. L261: `hidden_omega_0`

**These are code identifiers, not math.** They are PyTorch API parameter names (e.g., `torch.nn.LayerNorm(elementwise_affine=False)`). Converting them to LaTeX `$\text{elementwise\_affine}$` would change their semantic meaning from code to math.

## STOP Condition: GAP-22-03

**Conflict:** Plan 22-02 Task 2 explicitly states:
> "Backtick-wrapped ASCII-math the D5 oracle + author comments flag... convert to `$…$` only when it is genuinely math (not a filename/code identifier)"

The detector fires on these code identifiers because they match the ASCII-math pattern and are near author comments, but the plan excludes them.

**Options presented to user:**
- **(A) Accept as false positives** — plan is correct, detector is over-inclusive
- **(B) Narrow detector's oracle window** — exclude code spans from D5/D6 scans
- **(C) Convert despite plan exclusion** — change semantic meaning to reach G2

**Gap recorded in:**
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` (GAP-22-03)
- `.planning/milestones/v1.4-GAPS.md` (milestone-level index)

## Files Modified

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — tables converted, math normalized
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` — GAP-22-03 added
- `.planning/milestones/v1.4-GAPS.md` — GAP-22-03 indexed

## Verification Artifacts

- Detector output: `22-02-DETECTOR-BASELINE.txt` (pre-execution)
- Table conversion script: `/tmp/convert-both-tables.mjs`
- Per-construct checkpoint hashes: recorded in commit message

## Dependencies

- **Blocks:** Plan 22-03 (cannot achieve G2 until GAP-22-03 resolved)
- **Blocked by:** User instruction on GAP-22-03

## Next Steps

User must decide GAP-22-03 resolution. After resolution:
1. Apply chosen fix (accept/narrow detector/convert)
2. Re-run detector to confirm exit 0
3. Commit final state
4. Update this summary to `status: COMPLETED`
