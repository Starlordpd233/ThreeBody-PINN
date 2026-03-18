---
phase: 01-code-rewrites-and-validation
verified: 2026-03-18T23:15:00Z
status: passed
score: 8/8 must-haves verified
re_verification: true
  previous_status: gaps_found
  previous_score: 7/8
  gaps_closed:
    - "Gold IC filename pattern for hierarchical_gold fixed in config.py line 64"
  gaps_remaining: []

---

# Phase 01: Code Rewrites and Validation Verification Report

**Phase Goal:** Every active script, validation tool, and documentation file must correctly resolve IC paths after consolidation. Gold IC variants use base folders with _gold_ filename patterns. Standard_gold validation handles 184-ID subset gap gracefully.

**Verified:** 2026-03-18T23:15:00Z
**Status:** passed (all gaps closed)
**Score:** 8/8 must-haves verified

## Re-Verification Summary

**Previous gap closed:** PATH-05 - hierarchical_gold IC pattern in config.py

**Fix verified:** Commit 6e31300 changed line 64 from `ic_hierarchical_gold_{num:04d}.txt` to `ic_hierarchical_{num:04d}.txt`, matching actual files in ic_hierarchical/ folder (4857 files).

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Gold IC directories point to base folders, not _for_gold_standard folders | VERIFIED | config.py lines 44, 48, 52, 56 all point to base folders |
| 2 | Filename patterns match actual files in base folders | VERIFIED | hierarchical_gold: ic_hierarchical_{num:04d}.txt (4857 files); standard_gold: ic_standard_{num:04d}.txt |
| 3 | All path references resolve to existing directories | VERIFIED | All referenced directories exist on disk |
| 4 | Debug scripts reference base IC folders | VERIFIED | grep returns zero matches for _for_gold_standard in Scripts folder |
| 5 | Stage 1/2 scripts use IC_RAW_DIR env var | VERIFIED | Present in 4 scripts: ic_generation_utils.py, stage2_prescreening, prescreening_utils.py, example_incremental_workflow.py |
| 6 | Missing IC_RAW_DIR produces clear error | VERIFIED | RuntimeError with export example in all scripts |
| 7 | correspondence.py excludes 184 IDs for standard_gold | VERIFIED | load_standard_gold_exclusions() returns 184 IDs from markdown file |
| 8 | Validation for standard_gold has zero false FAILs | VERIFIED | Exclusion list properly filters out 184 non-gold ICs |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `config.py` | Updated gold IC directory paths | VERIFIED | Lines 44, 48, 52, 56 point to base folders |
| `config.py` | Correct hierarchical_gold pattern | VERIFIED | Line 64: ic_hierarchical_{num:04d}.txt (FIXED) |
| `config.py` | Correct standard_gold pattern | VERIFIED | Line 66: ic_standard_{num:04d}.txt |
| `naming.py` | Legacy path comments | VERIFIED | Lines 172, 174 have "Legacy path - Phase 3 deletion" comments |
| `run_brutus_hierarchical_only_mac_gold_standard.py` | Updated IC_DIR | VERIFIED | Line 34 points to ic_hierarchical (base folder) |
| Debug scripts (5 files) | Base IC folder references | VERIFIED | grep -rn "_for_gold_standard" in Scripts returns 0 matches |
| `ic_generation_utils.py` | IC_RAW_DIR env var | VERIFIED | Lines 595-607 implement env var with error handling |
| `stage2_prescreening_revised_auto.py` | IC_RAW_DIR env var | VERIFIED | Lines 38-56 implement env var |
| `prescreening_utils.py` | IC_RAW_DIR env var | VERIFIED | Lines 212-220 implement env var |
| `correspondence.py` | load_standard_gold_exclusions() | VERIFIED | Function loads and parses 184 IDs |
| `standard_quasi_random_ids_not_in_gold.md` | 184-ID exclusion list | VERIFIED | File exists with 184 IDs documented |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| config.py dataset_variants | Actual IC folders | get_ic_dir() | WIRED | Returns correct path to base folders |
| naming.py directory_mapping | config.py variant names | map_directory_to_variant() | WIRED | Returns correct variant strings |
| correspondence.py | standard_quasi_random_ids_not_in_gold.md | load_standard_gold_exclusions() | WIRED | Function parses markdown file |
| is_blacklisted() | 184-ID exclusion set | file_number in excluded_ids | WIRED | Standard_gold correctly checks exclusions |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| PATH-01 | 01-01 | run_brutus_hierarchical_only_mac_gold_standard.py IC_DIR | SATISFIED | Line 34 points to ic_hierarchical |
| PATH-02 | 01-01 | config.py gold ic_dir entries | SATISFIED | All gold variants point to base folders |
| PATH-03 | 01-01 | naming.py folder-to-name mappings | SATISFIED | Legacy comments present at lines 172, 174 |
| PATH-04 | 01-02 | Debug scripts reference base paths | SATISFIED | Zero _for_gold_standard references in Scripts |
| PATH-05 | 01-01 | Gold IC filename patterns | SATISFIED | hierarchical_gold: ic_hierarchical_*.txt; standard_gold: ic_standard_*.txt |
| PATH-06 | 01-02 | IC_RAW_DIR env var in Stage 1/2 | SATISFIED | Present in 4 scripts |
| VALD-01 | 01-03 | correspondence.py handles 184 gap | SATISFIED | Exclusion loading returns 184 IDs |
| VALD-02 | 01-03 | Exclusion list file exists | SATISFIED | 184 IDs documented |

### Anti-Patterns Found

None. All patterns resolved.

### Human Verification Required

None required. All automated checks pass.

---

## Gaps Summary

All 8 must-haves verified. Phase goal achieved.

---

_Verified: 2026-03-18T23:15:00Z_
_Verifier: Claude (gsd-verifier)_