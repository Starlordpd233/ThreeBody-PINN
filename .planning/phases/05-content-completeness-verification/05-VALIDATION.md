---
phase: 05
slug: content-completeness-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python pytest (if installed) or standalone script execution |
| **Config file** | none — standalone scripts |
| **Quick run command** | `python pinn_instruction/original_latex/verification/verify_content.py --structure data-quality-assessment` |
| **Full suite command** | `python pinn_instruction/original_latex/verification/verify_content.py --all` |
| **Estimated runtime** | ~5 seconds per structure (~25 seconds total) |

---

## Sampling Rate

- **After every task commit:** Run verify_content.py on the structure just modified
- **After every plan wave:** Run `verify_content.py --all`
- **Before `/gsd:verify-work`:** Full suite must show "no differences found" for all 5 structures
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | CONT-01 | integration | `python verify_content.py --structure data-quality-assessment` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | CONT-01 | integration | `python verify_content.py --structure ctl-instruction` | ❌ W0 | ⬜ pending |
| 05-01-03 | 01 | 1 | CONT-01 | integration | `python verify_content.py --structure pinn-architecture` | ❌ W0 | ⬜ pending |
| 05-01-04 | 01 | 1 | CONT-01 | integration | `python verify_content.py --structure review_of_framework` | ❌ W0 | ⬜ pending |
| 05-01-05 | 01 | 1 | CONT-01 | integration | `python verify_content.py --structure stage_strat_revision` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | CONT-02 | integration | `python verify_content.py --all 2>&1 | grep -A5 "DROPPED"` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 1 | CONT-03 | integration | `python verify_content.py --all 2>&1 | grep -A5 "EXTRANEOUS"` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `pinn_instruction/original_latex/verification/verify_content.py` — main verification script
- [ ] `pinn_instruction/original_latex/verification/` — output directory for reports

*Note: No test framework required — standalone Python script using difflib*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Report readability | CONT-01 | Human judgment of output clarity | Open generated .md report and verify structure/wording matches expectations |
| Whitespace normalization correctness | CONT-01 | Visual inspection of edge cases | Compare original vs modular side-by-side for known tricky files |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending