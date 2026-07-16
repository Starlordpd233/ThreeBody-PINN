---
phase: 39-data-ingestion-stage-0-population-scan
plan: 11
subsystem: pinn/data (adapter)
tags: [gap-closure, evidence-integrity, redaction, blacklist, DATA-01, DATA-02]
dependency_graph:
  requires: [39-03, 39-07, 39-10]
  provides: [evidence_lines, per-fidelity-blacklist-counts]
  affects: [39-12]
tech_stack:
  added: [EvidenceRedactionError, AdmittedSetAdapter.evidence_lines, data_root_source]
  patterns: [fail-closed redaction, verbatim-order projection, per-fidelity counters]
key-files:
  created: []
  modified:
    - pinn/data/adapter.py
    - pinn/data/__init__.py
    - tests/phase39/test_adapter.py
decisions:
  - "Redact at the projection, not at init_log: init_log is the in-process operator diagnostic (must retain resolved root per 39-03-PLAN.md:88); scan.log must not contain absolute paths (39-07-PLAN.md:29). A single seam with two consumers is the minimal structure that satisfies both."
  - "Fail-closed via host-agnostic needles (str(data_root), str(Path.home())) rather than a hardcoded host-path prefix, so the guard holds on any machine."
  - "Per-fidelity counters keyed by BRUTUS_FOLDER_TABLE fidelity (base/gold), not folder — the 39-03 contract is per fidelity, and four folders map to two fidelities."
  - "n_excluded incremented only when disposition != admit (defense-in-depth: a blacklisted record present on disk is never admitted)."
metrics:
  duration: ~12min
  completed: "2026-07-16"
  tasks: 2/2
  files: 3
  tests_added: 9
  tests_total_phase39: 260 (baseline 251)
  tests_total_full: 443 (baseline 434)
status: complete
---

# Phase 39 Plan 11: Adapter Evidence Projection Summary

Redacted evidence projection and per-fidelity blacklist logging added to `AdmittedSetAdapter`, closing the 39-VERIFICATION.md truth-7 evidence-integrity gap at the adapter source. A caller (Plan 39-12's `stage_scan.py` CLI) can now retain DATA-01 memory evidence and DATA-02 blacklist disposition evidence without leaking a host path.

## One-liner

`AdmittedSetAdapter.evidence_lines()` is a fail-closed, redacted, verbatim-order projection of `init_log` that replaces the absolute-root entry with the `$GSD_DATA_ROOT` placeholder; per-fidelity `n_present_on_disk`/`n_excluded` blacklist lines are derived from the file walk and emitted alongside the existing per-family lines.

## Tasks Executed

| Task | Name | Type | Commit | Files |
|------|------|------|--------|-------|
| 39-11-01 | Log per-fidelity blacklist presence and exclusion counts | auto (TDD) | d2300e2 | pinn/data/adapter.py, tests/phase39/test_adapter.py |
| 39-11-02 | Add the fail-closed redacted evidence projection | auto (TDD) | 08a4641 | pinn/data/adapter.py, pinn/data/__init__.py, tests/phase39/test_adapter.py |

## What Was Built

### Task 39-11-01 — Per-fidelity blacklist counts

- Replaced the fidelity-blind `blacklist_present` dict (keyed by folder, discarded) with two per-fidelity counters keyed by the fidelity component of `BRUTUS_FOLDER_TABLE[folder]` — `"base"` and `"gold"`.
- `n_present_on_disk` incremented when a found file's `record_key.physical_key` is in `self.blacklisted_physical_keys`.
- `n_excluded` incremented for that same fidelity when the record's `outcome.disposition` is not `"admit"`.
- Both counters initialized for every fidelity so a fidelity with zero blacklisted files still emits a `0` line.
- After the per-folder disposition loop, one sorted line per fidelity is appended: `blacklist {fidelity} n_present_on_disk={present} n_excluded={excluded}` (base before gold).
- The existing per-family `n_blacklist_entries` and `absent_ids` lines are byte-identical.
- 4 dataset-free tests added; existing per-family assertions unchanged.

### Task 39-11-02 — Redacted evidence projection

- `EvidenceRedactionError(ValueError)` module-level exception added to `pinn/data/adapter.py` and exported from `pinn/data/__init__.py`.
- `self.data_root_source` persisted in `_resolve_root` immediately before the existing `root: {resolved} source={source}` append (the `:764` line is byte-identical).
- `AdmittedSetAdapter.evidence_lines() -> tuple[str, ...]`: walks `self.init_log`, substitutes the single `root: ` entry with `GSD_DATA_ROOT=$GSD_DATA_ROOT source={self.data_root_source}` at the same position, passes every other entry through verbatim.
- Fail-closed guard: raises `EvidenceRedactionError` if any projected line contains `str(self.data_root)` or `str(Path.home())`, naming the offending field.
- 5 dataset-free tests added (placeholder replaces root, init_log retains absolute root, no host path in projection, DATA-01/DATA-02 payload carried, fail-closed guard on post-construction leak).

## Deviations from Plan

None — plan executed exactly as written. Both tasks followed the TDD RED/GREEN cycle; no Rule 1-4 deviations were triggered.

## Known Stubs

None. `evidence_lines()` is fully wired from `init_log` entries appended during `__init__`; no field is hardcoded or post-processed.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: information-disclosure-mitigated | pinn/data/adapter.py | T-39-10 mitigated at source: `evidence_lines()` replaces the absolute-root entry with the `$GSD_DATA_ROOT` placeholder and raises `EvidenceRedactionError` if `str(data_root)` or `str(Path.home())` survives. |
| threat_flag: tampering-mitigated | pinn/data/adapter.py | T-39-03 mitigated: `n_present_on_disk`/`n_excluded` derived from the actual file walk, never a README total or hardcoded count. |

## Verification

- `grep -c 'def evidence_lines' pinn/data/adapter.py` → 1 ✓
- `grep -c 'EvidenceRedactionError' pinn/data/adapter.py` → 4 ✓
- `$HOME/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phase39 -p 'test_*.py'` → 260 tests, OK (baseline 251; >= 255) ✓
- `$HOME/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests -p 'test_*.py'` → 443 tests, OK (baseline 434; >= 438) ✓
- `git diff --exit-code -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` → 0 ✓
- `test -z "$(git status --short -- simulation_data)"` → untouched ✓

## Self-Check: PASSED

- `pinn/data/adapter.py` — `evidence_lines`, `EvidenceRedactionError`, `data_root_source`, per-fidelity counters all present ✓
- `pinn/data/__init__.py` — `EvidenceRedactionError` exported ✓
- Commits d2300e2, 08a4641 exist on `milestone/v2.0` ✓
- 260 phase39 tests pass; 443 full-suite tests pass ✓
