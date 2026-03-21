---
phase: 08
slug: compilability-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-22
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib (subprocess, re) |
| **Config file** | none — Wave 0 installs nothing |
| **Quick run command** | `python pinn_instruction/original_latex/verification/verify_compile.py --structure data-quality-assess` |
| **Full suite command** | `python pinn_instruction/original_latex/verification/verify_compile.py` |
| **Estimated runtime** | ~60 seconds (5 structures × ~12s each) |

---

## Sampling Rate

- **After every task commit:** Run `python verify_compile.py --structure <name>` for the structure modified
- **After every plan wave:** Run `python verify_compile.py` (all structures)
- **Before `/gsd:verify-work`:** Full run must show 5/5 PASS
- **Max feedback latency:** 120 seconds (compilation timeout per structure)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | COMP-01 | integration | `python verify_compile.py` | ❌ W0 | ⬜ pending |
| 08-01-02 | 01 | 1 | COMP-02 | integration | `python verify_compile.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `pinn_instruction/original_latex/verification/verify_compile.py` — main script
- [ ] `pinn_instruction/original_latex/verification/tmp/` — temp directory for aux files

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| PDF visual inspection | COMP-01 | Compilation success ≠ visual correctness | Open each PDF and verify no obvious rendering issues |

*Note: The primary verification (0 errors) is fully automated. Manual inspection is optional for visual confirmation.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending