---
plan_id: 22-02
title: pinn_architecture.md GFM Table Conversion + Math Normalization
executed: 2026-06-09
status: COMPLETED
detector_exit: 0
gap_22_03: RESOLVED-WITH-INSTRUCTION
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
- **Verification:** All cell content preserved byte-for-byte; Pandoc footnote markers in the converted tables were changed from `[^n]` to render-safe `[n]` form per the Stage-0 `unsupported` probe.
- **Commit:** `acb8aa8` "fix(22-02): convert Pandoc structures in pinn_architecture.md to GFM"

### Task 2: Math Normalization ✓
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
  - All 39 Pandoc footnote references/definitions converted from `[^n]`/`[^n]:` syntax to render-safe bracket-number/reference-list form (`[n]` plus `n.` references) per the Stage-0 probe
  - Heading `## Footnotes` renamed to `## References`

## GAP-22-03 Incident

After Task 2 completed, the detector reported 0 DEFINITE + 7 REVIEW findings (exit 1). All 7 REVIEW findings were D5/D6 code identifiers — PyTorch parameter names (`first_omega_0`, `elementwise_affine=False`, etc.) within the ±20-line oracle window of author comments. The plan's D-02/D-07 says "convert to `$…$` only when it is genuinely math (not a filename/code identifier)", so converting these to LaTeX would change their semantic meaning from code to math.

**Gap recorded in:**
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` (GAP-22-03)
- `.planning/milestones/v1.4-GAPS.md` (milestone-level index)

### User Resolution (Option A)

User instructed on 2026-06-09:

> Resolve GAP-22-03 with Option A. Do not modify D5's code-span scan (Option B would delete the detector's only backtick-math layer - it's what found the 94d8e79 conversions, and snake_case vs. subscript is mechanically inseparable, which is precisely why these are REVIEW). Do not convert (Option C).
>
> 1. Keep all 7 tokens as code (presentation-preservation, D-02/D-07).
> 2. Redefine G2 for the tiered detector: 0 DEFINITE + every REVIEW adjudicated. Document each of the 7 in 22-02-SUMMARY.md with {line, token, verdict: code-identifier-kept, rationale}.
> 3. Add a surfaced adjudication-allowlist to detect.mjs so adjudicated REVIEWS are reported as cleared and the tool exits honestly; regenerate 22-02-DETECTOR-BASELINE.txt.
> 4. Mark GAP-22-03 RESOLVED-WITH-INSTRUCTION in 22-GAPS.md and v1.4-GAPS.md; record that D5 stays intact and the same adjudication pattern is expected (correctly) in 22-03.

### Implementation

1. **All 7 tokens kept as code** (presentation-preservation per D-02/D-07). No modifications to `pinn_architecture.md`.
2. **Adjudication allowlist mechanism added to detect.mjs** (`--adjudications <path>` flag). Minimal, surgical addition — D1–D7 core logic unchanged. D5's code-span scan stays intact.
3. **Adjudication allowlist created** at `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` with all 7 entries.
4. **G2 redefined** for the tiered detector: **0 DEFINITE + every REVIEW either adjudicated or absent**.

### Adjudication Table (7 items)

| Line | Token | Layer | Verdict | Rationale |
|------|-------|-------|---------|-----------|
| 170 | `first_omega_0` | D5 | code-identifier-kept | SIREN initialization parameter name (PyTorch code identifier in backtick code span, not math) |
| 188 | `\text{xxx}` | D5 | code-identifier-kept | Placeholder literal inside Author Comment text (not math to render) |
| 236 | `elementwise_affine=False` | D5 | code-identifier-kept | torch.nn.LayerNorm keyword argument (Python code identifier, not math expression) |
| 238 | `elementwise_affine=True` | D5 | code-identifier-kept | torch.nn.LayerNorm keyword argument (Python code identifier, not math expression) |
| 259 | `elementwise_affine` | D6 | code-identifier-kept | PyTorch LayerNorm parameter name in hyperparameter table cell (code identifier in prose) |
| 260 | `first_omega_0` | D6 | code-identifier-kept | SIREN parameter name in hyperparameter table cell (code identifier in prose) |
| 261 | `hidden_omega_0` | D6 | code-identifier-kept | SIREN parameter name in hyperparameter table cell (code identifier in prose) |

### G2 Definition (tiered detector)

**G2 = 0 DEFINITE findings + every REVIEW finding is either adjudicated (matched in the allowlist) or absent.** Exit code 0 when satisfied. This replaces the prior "0 findings total" definition for plans that encounter code identifiers the plan's D-02/D-07 excludes from conversion.

### D5 Preservation Note

Option B (narrowing D5's code-span scan) was explicitly rejected. D5's backtick-math oracle scan is the detector's only code-span layer — it found the 94d8e79 conversions during Task 2. snake_case code identifiers vs. bare subscripts are mechanically inseparable at the D5/D6 layer, which is precisely why these are REVIEW tier (not DEFINITE). The adjudication allowlist preserves D5's recall while allowing honest exit-0 reporting for adjudicated items.

### Forward Reference: Plan 22-03

The same adjudication pattern is expected to apply to plan 22-03 (`ctl_instruction.md`), which likely contains the same PyTorch parameter names (`first_omega_0`, `elementwise_affine`, `hidden_omega_0`) within oracle windows. A separate adjudication allowlist will be created for 22-03 following the same pattern.

## Final Detector Status

```
DEFINITE findings: 0
REVIEW findings: 0
ADJUDICATED: 7 (cleared via allowlist)
SUPPRESSED: 14 (identifier-shape, surfaced for review)
Exit code: 0
```

## Files Modified

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — tables converted, math normalized
- `tools/spec-render-check/detect.mjs` — adjudication allowlist mechanism added (`--adjudications` flag)
- `tools/spec-render-check/README.md` — documented adjudication allowlist feature
- `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` — 7-item adjudication allowlist
- `.planning/phases/22-framework-spec-cleanup/22-02-DETECTOR-BASELINE.txt` — regenerated with adjudication
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` — GAP-22-03 marked RESOLVED-WITH-INSTRUCTION
- `.planning/milestones/v1.4-GAPS.md` — GAP-22-03 marked RESOLVED-WITH-INSTRUCTION

## Verification Artifacts

- Detector output: `22-02-DETECTOR-BASELINE.txt` (post-adjudication, exit 0)
- Adjudication allowlist: `tools/spec-render-check/adjudications/22-02-pinn-architecture.json`
- Selftest: PASS (G1) — regression fixtures reproduced, negative controls clean
- Table conversion script: `.planning/phases/22-framework-spec-cleanup/22-02-transform.mjs`
- Per-construct checkpoint evidence: table conversion captured in commit `acb8aa8`; reproducibility script retained at `.planning/phases/22-framework-spec-cleanup/22-02-transform.mjs`
