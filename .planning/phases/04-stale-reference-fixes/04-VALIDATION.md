---
phase: 4
slug: stale-reference-fixes
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual verification via grep |
| **Config file** | none |
| **Quick run command** | `grep -rn 'FINAL_ic_generator_enhanced\|generate_enhanced_ics' --include='*.py' --include='*.md' . \| grep -v '.planning/'` |
| **Full suite command** | Quick run + `cd simulation_data/Scripts/ic_generation && python -c "from ic_generation_utils import continuation_enhanced_ic_generation; print('OK')"` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick grep sweep
- **After every plan wave:** Run full suite command
- **Before `/gsd:verify-work`:** Full suite must return zero hits and import must succeed
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | PATH-06 | smoke | `cd simulation_data/Scripts/ic_generation && python -c "from ic_generation_utils import continuation_enhanced_ic_generation; print('OK')"` | N/A (inline) | ⬜ pending |
| 04-01-02 | 01 | 1 | PATH-06 | grep | `grep -n 'ic_raw_datasets' simulation_data/Scripts/ic_generation/generate_ics.py` (expect empty) | N/A (inline) | ⬜ pending |
| 04-02-01 | 02 | 1 | DOCS-02 | grep | `grep -n 'FINAL_ic_generator_enhanced\|generate_enhanced_ics\|Data/ic_raw/' simulation_data/Documentation/README.md` (expect empty) | N/A (inline) | ⬜ pending |
| 04-02-02 | 02 | 1 | DOCS-04 | grep | `grep -n 'FINAL_ic_generator_enhanced\|generate_enhanced_ics\|_for_gold_standard' AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md` (expect empty) | N/A (inline) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No test framework needed — verification is grep-based.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| AGENTS.md Section 3.2 content matches CLAUDE.md | DOCS-04 | Structural content comparison, not simple grep | Diff AGENTS.md Section 3.2 against CLAUDE.md Section 3.2 — content must be identical |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
