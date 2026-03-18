---
phase: 01
slug: code-rewrites-and-validation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — manual grep-based verification |
| **Config file** | None |
| **Quick run command** | N/A |
| **Full suite command** | See success criteria commands below |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run grep verification for modified files
- **After every plan wave:** Run all 4 success criteria grep commands
- **Before `/gsd:verify-work`:** All grep commands return zero matches
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | PATH-01 | grep | `grep -n "ic_hierarchical_for_gold_standard" run_brutus_hierarchical_only_mac_gold_standard.py` | ✅ | ⬜ pending |
| 01-01-02 | 01 | 1 | PATH-02 | grep | `grep -n "ic_dir.*_for_gold_standard" config.py` | ✅ | ⬜ pending |
| 01-01-03 | 01 | 1 | PATH-03 | grep | `grep -n "_for_gold_standard" naming.py` | ✅ | ⬜ pending |
| 01-02-01 | 02 | 1 | PATH-04 | grep | `grep -rn "_for_gold_standard" Scripts/debug/` | ✅ | ⬜ pending |
| 01-02-02 | 02 | 1 | PATH-05 | grep | `grep -n "ic_.*_gold_" config.py` | ✅ | ⬜ pending |
| 01-03-01 | 03 | 2 | PATH-06 | grep | `grep -n "IC_RAW_DIR\|ic_raw" Scripts/ic_generation/*.py Validation/prescreening/*.py` | ✅ | ⬜ pending |
| 01-04-01 | 04 | 2 | VALD-01 | script | `python -m dataset_readiness_checks.modules.correspondence standard_gold` | ✅ | ⬜ pending |
| 01-04-02 | 04 | 2 | VALD-02 | file | `test -f simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] No test framework needed — verification uses grep commands and script execution

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| IC_RAW_DIR error message | PATH-06 | Requires runtime execution | Run IC gen script without IC_RAW_DIR env var; verify clear error with export example |
| correspondence.py 184-ID exclusion | VALD-01 | Requires runtime execution | Run `python -m dataset_readiness_checks.modules.correspondence standard_gold`; verify summary shows "184 IDs excluded" |

---

## Success Criteria Commands

```bash
# Criterion 1: No gold IC folder references
grep -r "ic_hierarchical_for_gold_standard\|ic_standard_quasi_random_for_gold_standard" \
  simulation_data/Scripts/ simulation_data/Validation/ --include="*.py"

# Criterion 2: No gold IC filename patterns
grep -r "ic_hierarchical_gold_\|ic_standard_gold_" \
  simulation_data/Scripts/ simulation_data/Validation/ --include="*.py"

# Criterion 3: IC_RAW_DIR usage in Stage 1/2 scripts
grep -n "IC_RAW_DIR" simulation_data/Scripts/ic_generation/*.py \
  simulation_data/Validation/prescreening/*.py

# Criterion 4: Correspondence validation handles 184-ID gap
python -m simulation_data.Validation.dataset_readiness_checks.modules.correspondence standard_gold
```

---

## Validation Sign-Off

- [x] All tasks have verification commands defined
- [x] Sampling continuity: each wave has verification coverage
- [x] Wave 0 covers all MISSING references (N/A — grep-based)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter (after Wave 0 verification)

**Approval:** pending