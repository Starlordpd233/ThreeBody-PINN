---
phase: 02
slug: documentation-updates
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-03-19
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual verification (grep-based) |
| **Config file** | None |
| **Quick run command** | `grep -r "for_gold_standard" simulation_data/Documentation/ CLAUDE.md GEMINI.md QWEN.md ANTIGRAVITY.md README.md` |
| **Full suite command** | Multiple grep checks (see Per-Task Verification Map) |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Verify changed file manually
- **After every plan wave:** Run grep checks on all documentation
- **Before `/gsd:verify-work`:** All grep checks must return 0 for gold IC folder references
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | DOCS-01 | grep | `grep -c "ic_hierarchical_for_gold_standard" simulation_data/Documentation/DATASET_DOCUMENTATION.md` (expect 0) | N/A | ⬜ pending |
| 02-01-02 | 01 | 1 | DOCS-01 | grep | `grep -c "ic_standard_quasi_random_for_gold_standard" simulation_data/Documentation/DATASET_DOCUMENTATION.md` (expect 0) | N/A | ⬜ pending |
| 02-01-03 | 01 | 1 | DOCS-01 | grep | `grep -c "IC_RAW_DIR" simulation_data/Documentation/DATASET_DOCUMENTATION.md` (expect ≥1) | N/A | ⬜ pending |
| 02-02-01 | 02 | 1 | DOCS-02 | grep | `grep -c "for_gold_standard" simulation_data/Documentation/README.md` (expect 0) | N/A | ⬜ pending |
| 02-02-02 | 02 | 1 | DOCS-03 | grep | `grep -c "for_gold_standard" README.md` (expect 0) | N/A | ⬜ pending |
| 02-03-01 | 03 | 1 | DOCS-04 | diff | `diff <(grep -A 30 "### 3.2 Dataset" CLAUDE.md) <(grep -A 30 "### 3.2 Dataset" GEMINI.md)` (expect empty) | N/A | ⬜ pending |
| 02-03-02 | 03 | 1 | DOCS-04 | diff | `diff <(grep -A 30 "### 3.2 Dataset" CLAUDE.md) <(grep -A 30 "### 3.2 Dataset" QWEN.md)` (expect empty) | N/A | ⬜ pending |
| 02-03-03 | 03 | 1 | DOCS-04 | diff | `diff <(grep -A 30 "### 3.2 Dataset" CLAUDE.md) <(grep -A 30 "### 3.2 Dataset" ANTIGRAVITY.md)` (expect empty) | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements — manual grep verification only.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ic_raw externalization explanation clarity | DOCS-01 | Subjective quality | Read updated DATASET_DOCUMENTATION.md, verify IC_RAW_DIR env var explanation includes example export command |
| 184-ID subset explanation clarity | DOCS-01 | Subjective quality | Read updated DATASET_DOCUMENTATION.md, verify it references the exclusion list file and explains the subset relationship |
| Gold Brutus outputs distinction note | DOCS-01 | Subjective quality | Read updated DATASET_DOCUMENTATION.md, verify it clarifies gold outputs still exist while gold IC inputs were removed |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending