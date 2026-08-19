---
phase: 53
slug: narrow-spec-codification
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-19
---

# Phase 53 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> This phase's validation is **textual**, not runtime — the phase edits one
> framework-spec Markdown file and writes no code.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — grep/diff/render-oracle assertions (shell) |
| **Config file** | none |
| **Quick run command** | `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| **Full suite command** | the same, plus the per-edit grep assertions and the SCOPE-38 negative-diff assertion in the map below |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** the grep assertions for that task's edit + the SCOPE-38 negative diff + `grep -c 'Author Comment' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` = `8`
- **After every plan wave:** full assertion set + render oracle + scope guard
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 53-01-01 | 01 | 1 | SPEC-03 | — | N/A | textual assertion | `grep -c -F '**[LOCKED]**' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` ≥ 3; `grep -F '**[DEFAULT]**'` defined in new convention subsection | ✅ (post-edit) | ⬜ pending |
| 53-01-02 | 01 | 1 | SPEC-02 | — | N/A | textual assertion | `sed -n '633,700p' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md \| grep -F '**[LOCKED]**'`; `grep -F 'GAP-45-03'` present; `grep -F 'default $\lambda_{phys}^{max}(k) = 1$'` absent | ✅ (post-edit) | ⬜ pending |
| 53-01-03 | 01 | 1 | SPEC-04 | — | N/A | textual assertion | `grep -F 'mean over time, bodies, and spatial components'`; `grep -F 'GAP-45-01'` + `2026-07-31`; `grep -F '0.1539..0.1630'`; corrected formula in `$$…$$` display math carrying `N_t \, N_b \, d` or `9 N_t` | ✅ (post-edit) | ⬜ pending |
| 53-01-04 | 01 | 1 | SPEC-05 | — | N/A | textual assertion | `grep -F '### 10.6'`; `grep -F 'worst-case'`; `grep -F 'GAP-44-01'` + `2026-07-23`; `grep -F '1e-5'`; mean/median named non-gating; ADVANCE-gate disambiguation sentence present | ✅ (post-edit) | ⬜ pending |
| 53-01-05 | 01 | 1 | SCOPE-33/34/38 (SC-5) | T-53-01 | Governance-record integrity: no contract-marked value changed | negative diff assertion | `git diff -U0 -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md \| grep -E '^[+-]' \| grep -E 'eta_c\|first_omega_0\|underflow'` → **empty** | ✅ | ⬜ pending |
| 53-01-06 | 01 | 1 | SCOPE-33 | T-53-01 | Only authorized files change | diff-scope assertion | `git diff --stat -- pinn/ tests/ simulation_data/ pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` → empty; `grep -c 'Author Comment' …/pinn_architecture.md` = `8` | ✅ | ⬜ pending |
| 53-01-07 | 01 | 1 | SPEC-02..05 (render) | — | N/A | render oracle | Quick run command above → exit ≤ 1, 0 DEFINITE, REVIEW token set ⊆ baseline 12 tokens (see RESEARCH.md); adjudication JSON line re-key permitted as mechanical companion edit | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Task IDs above assume a single-plan decomposition; if the planner splits, re-key the map to the emitted plan/task IDs at plan time.*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements — no test framework, fixtures, or config are introduced; every assertion runs against the post-edit file with committed tooling (render deps restorable via `npm ci` from the committed lockfile).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Contract blocks carry ruling date, option letter, and archived grounding path | SPEC-02..05 (D-06) | Citation fidelity is a human-judgment check on prose, not a string match | Read each new `> **Phase 53 contract:` block; confirm date + option letter + full relative path match the GAP record quoted in RESEARCH.md §2 |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
