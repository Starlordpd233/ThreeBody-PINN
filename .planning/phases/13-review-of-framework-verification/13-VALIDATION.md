---
phase: 13
slug: review-of-framework-verification
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-06
---

# Phase 13 — Validation Strategy

> Per-phase validation contract for Review-of-Framework Verification.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + python one-liners (`grep`, `wc`, `diff`, `python -c "..."`) |
| **Config file** | none — verification commands embedded in plan acceptance criteria |
| **Quick run command** | `bash .planning/phases/13-review-of-framework-verification/scoring_script.py` |
| **Full suite command** | per-plan `<automated>` blocks in PLAN files |
| **Estimated runtime** | < 10 seconds (file-existence and grep checks only) |

---

## Sampling Rate

- **After every task commit:** Run the matching grep / diff acceptance check from the task's `<automated>` block
- **After every plan wave:** Re-run the per-plan automated checks (report heading counts, PENDING tokens, section audit status)
- **Before `/gsd-verify-work`:** Full verification report must show 0 PENDING, 7 PASS audits, Overall Status: PASS
- **Max feedback latency:** < 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 13-01-01 | 01 | 1 | CAND-02, AUDIT-03, FIDEL-03, FIDEL-06 | — | N/A | shell | `grep -c "^## " verification_report.md` → 7 | ✅ | ✅ green |
| 13-01-01 | 01 | 1 | D-42 (provenance fields), D-47 (vacuous policy), D-48 (`[@refN]`) | — | N/A | shell | `grep -c "VACUOUS PASS" report` → 5; `grep -c "@refN" report` → ≥1 | ✅ | ✅ green |
| 13-02-01..02 | 02 | 2 | AUDIT-01, AUDIT-02, FIDEL-01, FIDEL-02, FIDEL-04, FIDEL-05 | — | N/A | shell | `grep -c "^### [1-7]" report` → 7; all PASS | ✅ | ✅ green |
| 13-02-01..02 | 02 | 2 | FIDEL-01 (formula checklists), FIDEL-04 (cell-by-cell tables) | — | N/A | manual | Section 2: 6-row formula checklist; Section 5: 3-row formula checklist; Section 3/7: cell-by-cell tables | ✅ | 🔵 manual |
| 13-03-01 | 03 | 3 | CLEAN-01 (D-43), CLEAN-03, CROSS-01 (D-17/D-18), CROSS-02 | — | N/A | shell | `test -f review_of_framework.md`; `git log --follow` shows rename history; `grep "PENDING" report` → ≤1 | ✅ | ✅ green |

*Status: ✅ green · 🔵 manual-only*

---

## Wave 0 Requirements

- [x] `scoring_script.py` — diff-score harness for candidate comparison (used in prior phases; Phase 13 is single-candidate)
- [x] Per-plan `<automated>` blocks define grep/acceptance criteria (7 heading checks, PENDING counts, section audit PASS counts)
- [x] No external framework install required — project uses shell + python for verification per Phases 10-12

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Formula semantic equivalence (Section 2: 6 display math; Section 5: 3 display math) | FIDEL-01 | LaTeX-to-markdown math rendering varies; symbolic equivalence cannot be checked by string diff | Compare each `align*`/`equation` block in source against the markdown's `$$...$$` block; confirm operator-by-operator equivalence |
| Table cell-by-cell accuracy (Section 3: 13-row input vector spec; Section 7: 6-row hyperparameter schedule) | FIDEL-04 | GFM pipe-table conversion from pandoc grid-table/multiline-table; cell content requires human verification | Open both markdown and LaTeX tables side-by-side. Verify each cell value matches including subscripts, inline math, and column headers |
| PyTorch code block verbatim fidelity (Section 5: `compute_kinematics` function, 113+ lines) | FIDEL-02 | Code block must preserve function signatures, comments (including `CRITICAL:` markers), and exact indentation | Compare `compute_kinematics` block in markdown against the `lstlisting` in LaTeX source line-by-line |
| 3-wave execution pattern (Plan 01 provenance → Plan 02 audit/fix → Plan 03 promotion) | CROSS-02 | Process verification, not code | Confirm 3 PLAN/SUMMARY files exist; verify `git log` shows commits from all 3 waves |

---

## Post-Execution Formatting Fixes (2026-05-06)

During validation, the following markdown rendering compatibility issues were identified and fixed in `review_of_framework.md` (Wave 2, 17 fixes total):

1. **Fixed escaped-dash list markers** — 54 `\-` artifacts replaced across all 7 sections (26 in Section 2, 3 in Section 4, 3 in Section 5, 15 in Section 6, 7 in Section 3)
2. **Fixed escaped prose brackets** — 23 `\[` / `\]` artifacts replaced (1 in Section 1, 6 in Section 3, 4 in Section 6)
3. **Converted pandoc grid-table to GFM pipe-table** — Section 3 (13-row input vector spec): removed 14 grid separators, 1 duplicate header, 2 continuation markers (RoF-13-02-07/08)
4. **Converted pandoc multiline-table to GFM pipe-table** — Section 7 (6-row hyperparameter schedule): removed 3 long-dash separators and inter-row blanks (RoF-13-02-17)
5. **De-hyphenated `con\-cerning`** → `concerning` in Section 1 (RoF-13-02-01)

---

## Validation Sign-Off

- [x] All tasks have automated verify or manual-only designation
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-05-06
