# Deletion Decisions -- v1.3 Closure Audit -- 2026-05-11

## Summary
- Files to DELETE: 14
- Files to KEEP: 3
- Files UNCERTAIN (escalated): 0

## Per-File Decision Table

| # | File | Directory | Verdict | Rationale | Embedded-forward? | Agent(s) consulted |
|---|------|-----------|---------|-----------|-------------------|---------------------|
| 1 | ctl_instruction_verification_report.md | verification_reports/ | KEEP | Automated F1/recall scoring (0.958 F1, per-section breakdown) and candidate comparison tables are computational evidence not manually reproducible. | NA (KEEP) | ctl_instruction agent |
| 2 | data_quality_assessment_verification_report.md | verification_reports/ | DELETE | All 11 Phase-11 fixes (DQA-00-001 through DQA-STRUCT-04) confirmed applied; all discrepancies resolved; SI-DQA entries preserved in markdown Source Issues block. | YES (MASTER-AUDIT-2026-05-11.md reconciliation table) | data_quality_assessment agent |
| 3 | pinn_architecture_verification_report.md | verification_reports/ | DELETE | Candidate-scoring metadata (F1 scores, inactive-content grep tables) is conversion-process history, not fidelity evidence; fidelity findings subsumed by later audits. | YES (MASTER-AUDIT-2026-05-11.md section 5.2) | pinn_architecture agent |
| 4 | review_of_framework_verification_report.md | verification_reports/ | KEEP | Contains unique detailed evidence of 17 Phase 13 pandoc-artifact fixes, vacuous policy checks, formula checklist, and cell-by-cell table/code block verification not replicated elsewhere. | Partially (formula verification embedded in closure audit) | review_of_framework agent |
| 5 | sampling_method_verification_report.md | verification_reports/ | DELETE | All 7 SM-15-* fix items verified as applied; per-section F1 scores are historical benchmarks superseded by closure audit. | YES (MASTER-AUDIT-2026-05-11.md section 5.2) | sampling_method agent |
| 6 | stage_strat_revision_verification_report.md | verification_reports/ | KEEP | Phase 14 verification report documents the pandoc conversion workflow, per-section audit results, and fix log (SSR-14-NN-NN IDs); historically significant for conversion provenance. | NA (KEEP) | stage_strat_revision agent |
| 7 | MASTER-AUDIT-v1.3.md | audit_2026-05-07/ | DELETE | Synthesizer final. All 10 cross-cutting patterns (P1-P10) status updated in MASTER-AUDIT-2026-05-11.md section 2. Prioritized fix waves (A/B/C/D) executed in Phase 15.1 and verified. Overturned milestone-complete claim (commit c1a7e3a) documented in section 6. No unique non-reproducible evidence. | YES (fully embedded in MASTER-AUDIT-2026-05-11.md) | All 6 per-pair agents + synthesizer |
| 8 | audit-ctl_instruction.md | audit_2026-05-07/ | DELETE | All 12 findings independently re-verified; no unique byte-level or computational evidence not reproducible from current sources. | YES (closure audit reconciliation table) | ctl_instruction agent |
| 9 | audit-data_quality_assessment.md | audit_2026-05-07/ | DELETE | All 3 MINOR findings (title bold, em-dash, table header bold) now RESOLVED; 2 INFO findings reconfirmed and carried forward. | YES (closure audit reconciliation table) | data_quality_assessment agent |
| 10 | audit-pinn_architecture.md | audit_2026-05-07/ | DELETE | All findings either resolved or re-documented in closure audit; no unique non-reproducible evidence remains. 235x computational proof embedded verbatim. | YES (closure audit Embedded Evidence section) | pinn_architecture agent |
| 11 | audit-review_of_framework.md | audit_2026-05-07/ | DELETE | All 8 findings reconciled and status updated; superseded by closure audit. | YES (closure audit reconciliation table) | review_of_framework agent |
| 12 | audit-sampling_method.md | audit_2026-05-07/ | DELETE | All 16 findings reconciled and resolved; per-expression math verification table (49 expressions) embedded as historical evidence in closure audit. | YES (closure audit Embedded Evidence section) | sampling_method agent |
| 13 | audit-stage_strat_revision.md | audit_2026-05-07/ | DELETE | All 16 findings reconciled in closure audit; pair-specific evidence fully incorporated. | YES (closure audit reconciliation table + Embedded Evidence) | stage_strat_revision agent |
| 14 | verification_final_report.md | previous_audits/ | DELETE | Synthesizer final. All 15 structural issues (VFR-1 through VFR-15) resolved. Both pairs (sampling_method, review_of_framework) fully reconciled in closure audits. No unique evidence not captured in later reports. | YES (MASTER-AUDIT-2026-05-11.md section 5.2) | sampling_method agent + review_of_framework agent + synthesizer |
| 15 | pinn_architecture_verification_report.md | previous_audits/ | DELETE | 235x computational proof embedded verbatim in closure audit Embedded Evidence section. Error 1-3 all resolved. Inherited inconsistency note superseded. | YES (closure audit Embedded Evidence section) | pinn_architecture agent |
| 16 | pinn_architecture_verification_report_2.md | previous_audits/ | DELETE | Findings C-1/C-2/C-3/M-1-M-4/N-1-N-3 all resolved. Physics-softening note subsumed by closure audit. No unique evidence beyond what is captured. | YES (closure audit reconciliation table) | pinn_architecture agent |
| 17 | stage_strat_revision.md | previous_audits/ | DELETE | All 6 issues (ISS-1 through ISS-6) reconciled in closure audit. Tab-byte fix verification and proposed-fix text captured in Embedded Evidence section. | YES (closure audit Embedded Evidence section) | stage_strat_revision agent |

**Self-check: 17 rows present. 14 DELETE + 3 KEEP + 0 UNCERTAIN = 17. OK.**

## Files Marked KEEP (with justification)

### 1. `pinn_instruction/markdown_conversion/verification_reports/ctl_instruction_verification_report.md`
**Justification:** Contains unique, non-reproducible computational evidence:
- Automated F1/recall scoring comparing 3 candidate markdown conversions (0.958, 0.890, 0.959 F1 scores)
- Per-section recall breakdown (Section 01: 1.000 through Appendix: 0.577)
- Excluded comment range documentation (5 ranges across source)
- Candidate selection rationale (pandoc candidate vs. selected target)
This data cannot be regenerated without re-running the full conversion pipeline with all 3 candidates.

### 2. `pinn_instruction/markdown_conversion/verification_reports/review_of_framework_verification_report.md`
**Justification:** Contains unique Phase 13 conversion provenance:
- 17 specific pandoc-artifact fixes applied (escaped brackets, list markers, prose brackets, table conversions, longtable artifacts)
- Vacuous policy checks (authcomment, comment blocks, inactive files, citations, bibliography)
- Per-equation formula verification checklist for all 15 equations
- Cell-by-cell verification of input vector table (14 rows x 5 columns) and hyperparameter table (6 rows x 5 columns)
- Code block line-for-line verification (44 lines)
This is the primary record of Phase 13 conversion work.

### 3. `pinn_instruction/markdown_conversion/verification_reports/stage_strat_revision_verification_report.md`
**Justification:** Contains unique Phase 14 conversion provenance:
- Pandoc conversion workflow documentation
- Per-section audit results
- Fix log with SSR-14-NN-NN identifier system
- Documented conversion decisions and tradeoffs
Historically significant as the primary record of the Phase 14 conversion pass.

## Embed-before-delete verification

Before marking `MASTER-AUDIT-v1.3.md` (file #7) as SAFE_TO_DELETE, the following content was verified as present in `MASTER-AUDIT-2026-05-11.md`:

| Required content | Location in MASTER-AUDIT-2026-05-11.md | Status |
|-----------------|---------------------------------------|--------|
| 10 cross-cutting patterns (P1-P10) | Section 2, "Legacy cross-cutting patterns" table | PRESENT -- all 10 patterns listed with current status |
| Prioritized fix list (Waves A-D) | Referenced in Section 5.3 (Phase 15.1 claims verification) and Section 6 (resolution path) | PRESENT -- Phase 15.1 execution evidence confirms all waves completed |
| Overturned milestone-complete claim (commit c1a7e3a) | Section 6, "Verdict: BLOCKED" with rationale | PRESENT -- explicitly states current state and what remains |

All three required elements are embedded. SAFE_TO_DELETE is valid.

## Conflict Resolution Notes

### MASTER-AUDIT-v1.3.md (file #7): Per-pair agent disagreement resolved
- 2 agents said UNCERTAIN (ctl_instruction, sampling_method): cited cross-pair synthesis content
- 2 agents said SAFE_TO_DELETE (pinn_architecture, review_of_framework)
- 2 agents said KEEP_AS_HISTORICAL (data_quality_assessment, stage_strat_revision)
- **Synthesizer resolution: SAFE_TO_DELETE.** The cross-pair synthesis patterns (P1-P10), prioritized fix waves, and overturned milestone claim are all embedded-forward in MASTER-AUDIT-2026-05-11.md. No unique non-reproducible evidence remains. The 2 KEEP_AS_HISTORICAL votes reflect a preference for archiving rather than a claim of unique evidence.

### verification_final_report.md (file #14): Synthesizer final
- Both per-pair agents with visibility (sampling_method, review_of_framework) said SAFE_TO_DELETE.
- **Synthesizer confirms: SAFE_TO_DELETE.** All 15 structural issues (VFR-1 through VFR-15) are resolved and documented in MASTER-AUDIT-2026-05-11.md section 5.2. No unique evidence remains.

## Deletion Command Preview

```bash
# Set A — verification_reports/ (3 files to delete)
rm "pinn_instruction/markdown_conversion/verification_reports/data_quality_assessment_verification_report.md"
rm "pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md"
rm "pinn_instruction/markdown_conversion/verification_reports/sampling_method_verification_report.md"

# Set B — audit_2026-05-07/ (7 files to delete)
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/MASTER-AUDIT-v1.3.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-ctl_instruction.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-data_quality_assessment.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-pinn_architecture.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-review_of_framework.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-sampling_method.md"
rm "docs/findings/reports_on_v1.3/audit_2026-05-07/audit-stage_strat_revision.md"

# Set C — previous_audits/ (4 files to delete)
rm "docs/findings/reports_on_v1.3/previous_audits/verification_final_report.md"
rm "docs/findings/reports_on_v1.3/previous_audits/pinn_architecture_verification_report.md"
rm "docs/findings/reports_on_v1.3/previous_audits/pinn_architecture_verification_report_2.md"
rm "docs/findings/reports_on_v1.3/previous_audits/stage_strat_revision.md"
```

**Total: 14 files to delete across 3 directories. 3 files to retain (KEEP).**

---

*Synthesized from deletion_verdicts YAML in 6 per-pair closure audits plus synthesizer review of 2 cross-pair historical reports. KEEP rationales verified against per-pair agent findings. All 17 candidate files have a row in the per-file decision table above.*
