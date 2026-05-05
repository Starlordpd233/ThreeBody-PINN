# PINN Architecture Candidate Archive

## Candidate provenance

The authoritative PINN-Architecture markdown for Phase 12 is `../../pinn_architecture.md`. Selection rationale and final verification details are documented in `../../verification_reports/pinn_architecture_verification_report.md`.

| Archived file | Original path | Score/rank | Disposition | Reason |
|---|---|---|---|---|
| `pinn_architecture_v2.md` | `pinn_instruction/markdown_conversion/pinn_architecture_v2.md` | 0.8241 F1 / rank 3 | Archived unselected candidate | Consistently lower F1 and recall across all 7 sections compared to both top-level and pandoc candidates. Clear content loss relative to other candidates. |
| `PINN_architecture_plan.md` | `pinn_instruction/markdown_conversion/pandoc_conversion/PINN_architecture_plan.md` | 0.9257 F1 / raw rank 1, selected rank 2 | Archived unselected candidate | Narrow raw F1 lead (0.9257 vs 0.9203) was overridden because the top-level candidate had slightly better recall (0.9124 vs 0.9103) and was already at the canonical target path. Both within 0.5% of each other. Per D-02 override. |

**Phase context:** Phase 12 — PINN-Architecture Verification (v1.3 Markdown Conversion)
**Date archived:** 2026-05-05
**Selected baseline:** `pinn_architecture.md` (top-level) — F1=0.9203, Recall=0.9124
**Verification report:** `pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md`
