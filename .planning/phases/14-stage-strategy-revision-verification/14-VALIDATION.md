---
phase: 14
slug: stage-strategy-revision-verification
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-06
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for Stage-Strategy-Revision Verification.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | shell + python one-liners (`grep`, `wc`, `diff`, `python -c "..."`) |
| **Config file** | none — verification commands embedded in plan acceptance criteria |
| **Quick run command** | per-plan `<automated>` blocks in PLAN files |
| **Full suite command** | per-plan `<automated>` blocks in PLAN files |
| **Estimated runtime** | < 10 seconds (file-existence and grep checks only) |

---

## Sampling Rate

- **After every task commit:** Run the matching grep / diff acceptance check from the task's `<automated>` block
- **After every plan wave:** Re-run the per-plan automated checks (report heading counts, PENDING tokens, section audit status)
- **Before `/gsd-verify-work`:** Full verification report must show 0 PENDING, 6 PASS audits, Overall Status: PASS
- **Max feedback latency:** < 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 14-01-01 | 01 | 1 | CAND-02, AUDIT-03, FIDEL-03, FIDEL-06 | T-14-01/T-14-02 | N/A | shell | `grep -c "^## " report` → 7; `grep -c "VACUOUS PASS" report` → 3 | ✅ | ✅ green |
| 14-01-01 | 01 | 1 | D-53 (provenance), D-58 (policy checks), D-59 (`[@refN]`) | T-14-03 | N/A | shell | `grep -c "ACTIVE" report` → ≥3; `grep -c "@refN" report` → ≥1 | ✅ | ✅ green |
| 14-02-01 | 02 | 2 | AUDIT-01, AUDIT-02, FIDEL-01, FIDEL-02, FIDEL-04, FIDEL-05 | T-14-04 through T-14-13 | N/A | shell | `grep -c "^### [1-3]" report` → 3; all PASS | ✅ | ✅ green |
| 14-02-02 | 02 | 2 | AUDIT-01, FIDEL-02, FIDEL-03 | — | N/A | shell | `grep -c "^### [4-6]" report` → 3; all PASS; `grep -c "^\\*\\*Status:\\*\\* PASS" report` → 6 | ✅ | ✅ green |
| 14-02-01 | 02 | 2 | FIDEL-01 (formula checklists), FIDEL-04 (cell-by-cell tables) | T-14-05/T-14-06 | N/A | manual | Section 2: 6-row formula + Physical Invariants table; Section 3: 2-row formula + 3 tables (11-col, 3-col, 5-col) | ✅ | 🔵 manual |
| 14-02-02 | 02 | 2 | FIDEL-03 (16 bibitems), FIDEL-02 (113-line code block) | T-14-09/T-14-10 | N/A | manual | Section 6: 16-row bibitem verification; Section 4: code block line-by-line | ✅ | 🔵 manual |
| 14-03-01 | 03 | 3 | CLEAN-01 (D-54), CLEAN-03, CROSS-01, CROSS-02, CAND-02 | T-14-14 through T-14-20 | N/A | shell | `test -f stage_strat_revision.md`; `grep -c "PENDING" report` → 0; `grep -c "COMPLETED" report` → ≥1 | ✅ | ✅ green |

*Status: ✅ green · 🔵 manual-only*

---

## Wave 0 Requirements

- [x] Per-plan `<automated>` blocks define grep/acceptance criteria (7 heading checks, PENDING counts, section audit PASS counts, promotion status)
- [x] All 6 Policy Checks (D-58) captured with live grep evidence in Wave 1: 3 VACUOUS PASS + 3 ACTIVE verified
- [x] No external framework install required — project uses shell + python for verification per Phases 10-13

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Formula semantic equivalence (Section 2: 6 display math; Section 3: 2 display math) | FIDEL-01 | LaTeX-to-markdown math rendering varies; symbolic equivalence cannot be checked by string diff | Compare each `align*`/`equation` block in source against the markdown's `$$...$$` block; confirm operator-by-operator equivalence |
| Table cell-by-cell accuracy (4 tables: Physical Invariants 3-col, DataFrame 11-col, Framework Comparison 3-col, Stage Definitions 5-col) | FIDEL-04 | Tables were reconstructed from MISSING/MANGLED source; cell content requires human verification | Open both markdown and LaTeX tables side-by-side. Verify each cell value matches including subscripts, inline math, and column headers |
| Bibliography item-by-item accuracy (16 `\bibitem` entries) | FIDEL-03 | Bibliography was reconstructed from a collapsed paragraph; URLs, access dates, and title text require human confirmation | Compare each numbered list item against the LaTeX source `bibliography.tex`; verify title, URL, access date for all 16 entries |
| 113-line Python code block verbatim fidelity (Section 4: `compute_kinematics` et al.) | FIDEL-02 | Code block must preserve function signatures, comments, and exact indentation; converted from indented to fenced | Compare fenced Python block in markdown against the `lstlisting` in LaTeX source line-by-line |
| 3-wave execution pattern (Plan 01 provenance → Plan 02 audit/fix → Plan 03 promotion) | CROSS-02 | Process verification, not code | Confirm 3 PLAN/SUMMARY files exist; verify `git log` shows commits from all 3 waves |

---

## Post-Execution Formatting Fixes (2026-05-06)

During validation, the following markdown rendering compatibility issues were identified and fixed in `stage_strat_revision.md` (Wave 2, 14 fixes total):

1. **Fixed escaped citation brackets** — 35 `\[N\]` artifacts replaced with `[N]` across sections 1-3 (section-scoped per D-20)
2. **Fixed escaped quotes** — 10 `\"` artifacts replaced with `"` across sections 1-3
3. **Reconstructed Table 2 (DataFrame, 11-col) from MISSING** — Source `algorithmic_workflow.tex:42-54` rebuilt as GFM pipe-table with 2 data rows (SSR-14-02-NN, BLOCKING)
4. **Rebuilt Table 4 (Stage Definitions, 5-col longtable) from MANGLED** — Source `algorithmic_workflow.tex:126-162` rebuilt as GFM pipe-table with 7 data rows (Stages 0-6); removed continuation marker (SSR-14-02-NN, BLOCKING)
5. **Reformatted bibliography from collapsed paragraph** — 16 `\bibitem` entries from `bibliography.tex` expanded as numbered list at lines 369-384 (SSR-14-02-14, BLOCKING)
6. **Cleaned pandoc reference attribute** — `reference-type="ref"` removed from `\ref{tab:final_stages}` reference; simplified to "Table 4"
7. **Converted Python code block** — 113-line indented block → fenced code block with `python` language tag
8. **Fixed heading hierarchy** — Promoted `\section`→`##`, `\subsection`→`###` per D-60 across all 6 sections
9. **Verified `\authcomment{}` rendering** — Bold text acceptable per D-58; no further action needed

---

## Validation Sign-Off

- [x] All tasks have automated verify or manual-only designation
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (Policy Checks D-58 captured 3 ACTIVE checks requiring verification)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-05-06
