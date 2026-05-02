---
phase: 10
slug: ctl-instruction-verification
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-02
---

# Phase 10 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Shell checks and manual markdown review |
| **Config file** | none |
| **Quick run command** | `rg -n "CTL Candidate Comparison|Section Audit|Final Verification" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` |
| **Full suite command** | `rg -n "CAND-01|AUDIT-01|FIDEL-01|CLEAN-01|CROSS-01" .planning/phases/10-ctl-instruction-verification/*-PLAN.md` |
| **Estimated runtime** | ~5 seconds |

## Sampling Rate

- **After every task commit:** Run the plan task's grep/read checks.
- **After every plan wave:** Run the full suite command above plus the plan-specific verification block.
- **Before `$gsd-verify-work`:** Confirm final markdown, report, archive README, and conversion index all exist.
- **Max feedback latency:** 10 seconds for automated checks.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | CAND-01 | T-10-01 | N/A | docs | `rg -n "Overall score|Per-section score|Selected baseline" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` | yes | pending |
| 10-01-02 | 01 | 1 | CLEAN-01 | T-10-01 | N/A | docs | `test -f pinn_instruction/markdown_conversion/ctl_instruction.md` | yes | pending |
| 10-02-01 | 02 | 2 | AUDIT-01 | T-10-02 | N/A | docs | `rg -n "01_intro.tex|02_data_characterization.tex|03_data_glimpse.tex|04_phase1_data_prep.tex" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` | yes | pending |
| 10-02-02 | 02 | 2 | FIDEL-01 | T-10-02 | N/A | docs | `rg -n "Formula Checklist|BLOCKING|MAJOR|MINOR|INFO" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` | yes | pending |
| 10-03-01 | 03 | 3 | AUDIT-01 | T-10-03 | N/A | docs | `rg -n "05_phase2_training_loop.tex|06_advanced_considerations.tex|07_reproducibility.tex|appendix.tex" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` | yes | pending |
| 10-03-02 | 03 | 3 | CLEAN-02 | T-10-03 | N/A | docs | `test -f pinn_instruction/markdown_conversion/_archive/ctl-instruction/README.md` | yes | pending |
| 10-03-03 | 03 | 3 | CLEAN-03 | T-10-03 | N/A | docs | `rg -n "Zero open discrepancies|Fix Log|Source Issues" pinn_instruction/markdown_conversion/ctl_instruction_verification_report.md` | yes | pending |

## Wave 0 Requirements

Existing repository files cover all phase requirements. No test harness installation is needed.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Formula-by-formula fidelity | FIDEL-01 | Mathematical notation may be semantically wrong despite passing grep checks | Read each Formula Checklist row for sections 04 and 05 and compare against the cited LaTeX source line/location. |
| Human override of diff-score winner | CAND-01 | User explicitly allowed human inspection to override raw score | Verify the report documents raw ranking and any override rationale. |
| Source-issue appendix does not contaminate fidelity body | CROSS-01 | Requires judgment about document boundary | Confirm the final report states appended source issues are metadata excluded from fidelity comparison. |

## Validation Sign-Off

- [ ] All tasks have automated grep/read verification.
- [ ] Sampling continuity: no plan lacks verification.
- [ ] No watch-mode flags.
- [ ] Feedback latency < 10 seconds.
- [ ] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending

