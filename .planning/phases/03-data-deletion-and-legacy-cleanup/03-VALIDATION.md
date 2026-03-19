---
phase: 3
slug: data-deletion-and-legacy-cleanup
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-19
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — all validation via shell existence checks |
| **Config file** | None |
| **Quick run command** | Shell checks (see Per-Task Verification Map) |
| **Full suite command** | Run all 7 shell checks sequentially |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run all 7 shell checks
- **After every plan wave:** Run all 7 shell checks (all fast < 1 second)
- **Before `/gsd:verify-work`:** All 7 checks must pass
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | DEL-01 | smoke | `test ! -d simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard && echo PASS` | N/A (shell) | ⬜ pending |
| 03-01-02 | 01 | 1 | DEL-02 | smoke | `test ! -d simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard && echo PASS` | N/A (shell) | ⬜ pending |
| 03-01-03 | 01 | 1 | DEL-03 | smoke | `test ! -d simulation_data/Data/ic_raw && echo PASS` | N/A (shell) | ⬜ pending |
| 03-02-01 | 02 | 1 | CLN-01 | smoke | `test ! -d paper_templates/old_templates && echo PASS` | N/A (shell) | ⬜ pending |
| 03-02-02 | 02 | 1 | CLN-02 | smoke | `test ! -d brutus_simulation_documentation && echo PASS` | N/A (shell) | ⬜ pending |
| 03-02-03 | 02 | 1 | CLN-03 | smoke | `test $(find . -type d -name "__pycache__" -not -path "./.venv/*" -not -path "./.git/*" -not -path "./reference-code/*" \| wc -l) -eq 0 && echo PASS` | N/A (shell) | ⬜ pending |
| 03-02-04 | 02 | 1 | CLN-04 | smoke | `test $(find . \( -name "*.synctex.gz" -o -name "*.aux" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" \) -not -path "./.venv/*" -not -path "./.git/*" \| wc -l) -eq 0 && echo PASS` | N/A (shell) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. All validation is via shell existence checks — no test framework needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| naming.py legacy lines removed | DEL-01/02 (code cleanup) | Code edit verification | `grep -n '_for_gold_standard' simulation_data/Validation/dataset_readiness_checks/utils/naming.py` should return no matches |
| analysis/utils.py ic_raw refs fixed | DEL-03 (code cleanup) | Code edit verification | `grep -n 'ic_raw' simulation_data/Validation/analysis/utils.py` should return no matches |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 1s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
