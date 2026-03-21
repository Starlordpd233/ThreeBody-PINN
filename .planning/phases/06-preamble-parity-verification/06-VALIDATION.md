---
phase: 6
slug: preamble-parity-verification
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None (standalone Python scripts, built-ins only) |
| **Config file** | None — scripts are self-contained |
| **Quick run command** | `python pinn_instruction/original_latex/verification/verify_preamble.py --structure data-quality -v` |
| **Full suite command** | `python pinn_instruction/original_latex/verification/verify_preamble.py -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python pinn_instruction/original_latex/verification/verify_preamble.py --structure <name> -v`
- **After every plan wave:** Run `python pinn_instruction/original_latex/verification/verify_preamble.py -v` (all structures)
- **Before `/gsd:verify-work`:** Full suite must be green for all 5 structures
- **Max feedback latency:** ~5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 6-01-01 | 01 | 1 | PREAMB-01, PREAMB-02, PREAMB-03 | functional | `python pinn_instruction/original_latex/verification/verify_preamble.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `pinn_instruction/original_latex/verification/verify_preamble.py` — main verification script (create in Wave 1)
- [ ] Framework install: None needed — uses only Python built-ins

*Existing infrastructure covers all phase requirements once verify_preamble.py is created.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Visual inspection of mismatches flagged | PREAMB-03 | Human review to confirm package option diffs are real discrepancies | Run full suite, inspect MISMATCH lines in output |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
