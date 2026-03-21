---
phase: 07
slug: structure-fidelity-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 07 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None (standalone Python scripts) |
| **Config file** | None — scripts are self-contained |
| **Quick run command** | `python pinn_instruction/original_latex/verification/verify_structure.py --structure pinn-architecture -v` |
| **Full suite command** | `python pinn_instruction/original_latex/verification/verify_structure.py -v` |
| **Estimated runtime** | ~3 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python verify_structure.py --structure <name> -v`
- **After every plan wave:** Run `python verify_structure.py -v` (all structures)
- **Before `/gsd:verify-work`:** Full suite must be green (exit code 0)
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | STRUCT-01 | functional | `python verify_structure.py -v` | ❌ W0 | ⬜ pending |
| 07-01-02 | 01 | 1 | STRUCT-02 | functional | `python verify_structure.py -v` | ❌ W0 | ⬜ pending |
| 07-01-03 | 01 | 1 | STRUCT-03 | functional | `python verify_structure.py -v` | ❌ W0 | ⬜ pending |
| 07-01-04 | 01 | 1 | STRUCT-04 | functional | `python verify_structure.py -v` | ❌ W0 | ⬜ pending |
| 07-01-05 | 01 | 1 | STRUCT-05 | functional | `python verify_structure.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `pinn_instruction/original_latex/verification/verify_structure.py` — main verification script
- [ ] No framework install needed — uses only Python built-ins (re, pathlib, dataclasses, argparse, difflib, datetime)

*Existing infrastructure (verify_content.py, verify_preamble.py) provides reference patterns but verify_structure.py must be created.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Report readability check | All STRUCT | Human judgment | Open structure_verification_report.md and verify sections are readable and complete |

*All structural element verification is automated via the script.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending