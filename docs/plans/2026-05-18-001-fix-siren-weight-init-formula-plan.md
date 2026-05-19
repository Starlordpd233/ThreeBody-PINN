---
title: "fix: Correct SIREN hidden-layer weight initialization formula in LaTeX Table 1"
type: fix
status: active
date: 2026-05-18
---

# Fix: Correct SIREN Hidden-Layer Weight Init Formula in LaTeX Table 1

## Summary

Fix a typo in Table 1 of the PINN architecture LaTeX source where the hidden-layer SIREN weight initialization formula is inverted — the `hidden_omega_0` parameter appears in the numerator instead of denominator, and the `sqrt(6/n_in)` term is missing its square root. The correct formula already exists in the prose description (same file), the blueprint summary table, the markdown conversion, and the Python implementation. This plan corrects the single LaTeX table row, regenerates the PDF, and cleans up the now-stale discrepancy note in the markdown conversion.

---

## Problem Frame

Table 1 in `sqr_skipresnet_siren_backbone.tex:139` reads `U[-hidden_omega_0 / (6 n_in), hidden_omega_0 / (6 n_in)]`. The correct SIREN-paper formula is `U[-sqrt(6/n_in) / hidden_omega_0, sqrt(6/n_in) / hidden_omega_0]`. For `n_in=256` and `hidden_omega_0=1`, the Table 1 formula produces a bound ~235× too small. The author already flagged this exact row with `\authcomment{I believe this formula for initialization is incorrect}`. Every other location in the repo — the prose description in the same file (line 54), the blueprint summary table, the Python implementation (`basic_architecture.py:37`), and the markdown conversion (line 279) — uses the correct formula. The fix is a purely typographical correction in the LaTeX table body.

---

## Requirements

- R1. The Table 1 "Weight Init. (Hidden)" row must carry the correct SIREN initialization formula: `U[-sqrt(6/n_in) / hidden_omega_0, sqrt(6/n_in) / hidden_omega_0]`
- R2. The resolved `\authcomment{}` on that row must be removed (it was a question, not content)
- R3. The compiled PDF must reflect the corrected formula
- R4. The markdown conversion must no longer document a discrepancy that has been fixed

---

## Scope Boundaries

- Only the LaTeX table row and its adjacent author comment are in scope
- The prose description (lines 54-55), blueprint summary table, Python implementation, and all other files already carry the correct formula — no changes needed there
- No changes to PINN architecture, training logic, or any runtime code

---

## Context & Research

### Relevant Code and Patterns

- **LaTeX source (wrong formula):** `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex:139`
- **LaTeX source (correct formula in prose):** same file, lines 54-55
- **LaTeX source (blueprint summary, correct):** `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/blueprint_summary.tex:21`
- **Python implementation (correct):** `pinn/basic_architecture.py:36-38` — `bound = np.sqrt(6 / self.in_features) / self.omega_0`
- **Markdown conversion (correct formula, stale issue note):** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:279` (correct table), lines 856-860 (SI-PINN-001 issue note to remove)

### External References

- Sitzmann et al. (2020), "Implicit Neural Representations with Periodic Activation Functions" (NeurIPS) — the authoritative SIREN initialization derivation

---

## Key Technical Decisions

- **Match the exact LaTeX formatting of the prose description:** Reuse the same `\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}` LaTeX from line 54 to ensure visual consistency in the compiled PDF
- **Remove, don't just comment out, the author comment:** The `\authcomment` macro call on the table row becomes stale once the formula is corrected — delete it entirely

---

## Implementation Units

### U1. Fix the formula in Table 1

**Goal:** Replace the incorrect formula in the Table 1 "Weight Init. (Hidden)" row with the correct SIREN-paper formula.

**Requirements:** R1

**Dependencies:** None

**Files:**
- Modify: `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex`

**Approach:**
- On line 139, replace `\mathrm{U}\left[-\frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}, \frac{\text{hidden\_omega\_0}}{6 n_{\text{in}}}\right]` with `\mathrm{U}\left[-\frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}, \frac{\sqrt{6/n_{\text{in}}}}{\text{hidden\_omega\_0}}\right]`
- This matches the formula in the prose description (line 54) and the standard SIREN paper

**Patterns to follow:**
- Same file, line 54 for the correct LaTeX rendering

**Verification:**
- The LaTeX formula in the table row identically matches the prose formula on line 54
- With `hidden_omega_0=1` and `n_in=256`, the formula evaluates to `U[-0.153, 0.153]`, matching the SIREN paper and the Python implementation

### U2. Remove the resolved author comment

**Goal:** Delete the stale `\authcomment{}` that questioned the formula, now that it has been corrected.

**Requirements:** R2

**Dependencies:** U1

**Files:**
- Modify: `pinn_instruction/original_latex/framework-specs/pinn-architecture/sections/sqr_skipresnet_siren_backbone.tex`

**Approach:**
- Remove the `\authcomment{I believe this formula for initialization is incorrect}` on line 140 (immediately after the corrected formula row)

**Verification:**
- Grep for `authcomment.*incorrect` in the file returns zero matches

### U3. Regenerate the PDF

**Goal:** Produce an updated PDF from the corrected LaTeX source.

**Requirements:** R3

**Dependencies:** U2

**Files:**
- Modify: `pinn_instruction/original_latex/framework-specs/pinn-architecture/main_pinn.pdf` (regenerated output)

**Approach:**
- Compile `main_pinn.tex` with `pdflatex` (or `latexmk`) to regenerate the PDF
- If LaTeX tooling is unavailable, note the command that should be run

**Verification:**
- Open the PDF and visually confirm the "Weight Init. (Hidden)" row in Table 1 shows the corrected formula with `sqrt(6/n_in) / hidden_omega_0`

### U4. Update the markdown conversion to remove stale discrepancy references

**Goal:** Remove all stale references to the corrected formula discrepancy from the markdown conversion, so it no longer documents an error that has been fixed.

**Requirements:** R4

**Dependencies:** U2

**Files:**
- Modify: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`

**Approach:**
- Remove lines 856-860 (the `### SI-PINN-001: Weight Init. (Hidden) formula discrepancy` entry) from the "Source Issues / Notes for Future Reconciliation" section
- Remove the inline rendered authcomment `**[I believe this formula for initialization is incorrect]**` on line 287 (immediately below the Table 1 row) — this is the converted form of the LaTeX authcomment being removed in U2
- In SI-PINN-002 (lines 862-870): remove item 3 (`"I believe this formula for initialization is incorrect"`), update the count from "4 author comments" to "3 author comments", and renumber remaining items
- The markdown table at line 279 already uses the correct formula, so no table edit is needed

**Verification:**
- Grep for `SI-PINN-001` in the markdown file returns zero matches
- Grep for `I believe this formula for initialization is incorrect` in the markdown file returns zero matches
- SI-PINN-002 shows 3 author comments (not 4) and none reference the removed formula comment
- The "Source Issues" section no longer references a weight init formula discrepancy

---

## System-Wide Impact

- **API surface parity:** None — this is a documentation-only fix; the Python implementation already uses the correct formula
- **Unchanged invariants:** No code, training behavior, or PINN architecture is changed

---

## Sources & References

- Origin: user report identifying the formula discrepancy in Table 1, confirmed by author `\authcomment{}`
- SIREN paper: Sitzmann et al. (2020), "Implicit Neural Representations with Periodic Activation Functions," NeurIPS
- Related code: `pinn/basic_architecture.py:36-38` (correct Python implementation)
- Related doc: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:856-860` (SI-PINN-001 issue note)
