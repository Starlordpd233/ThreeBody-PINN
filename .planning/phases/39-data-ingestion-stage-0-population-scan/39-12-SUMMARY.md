---
phase: 39-data-ingestion-stage-0-population-scan
plan: 12
subsystem: DATA
tags: [evidence-integrity, scan-cli, fail-closed, dataset-free, T-39-13, T-39-08, T-39-10]
dependency_graph:
  requires: [39-11]
  provides: [39-13]
  affects: [pinn/data/stage_scan.py, tests/phase39/test_stage_scan.py]
tech_stack:
  added: [secrets, datetime.timezone]
  patterns: [fail-closed duck-typing probe, per-run freshness stamping, redacted evidence passthrough]
key_files:
  created: []
  modified:
    - pinn/data/stage_scan.py
    - tests/phase39/test_stage_scan.py
decisions:
  - "Retained `exit_code` as the internal parameter name (per the plan action's explicit signature) while renaming the emitted scan.log field to `scan_exit_code=`; the plan's acceptance grep `(^|[^_])exit_code=` is over-broad and catches the mandated param names — the emitted field is verified renamed by `test_cli_exit_code_field_renamed_to_scan_exit_code`."
  - "evidence_byte_identity rendered via `str(...).lower()` so the Python bool `True` emits as the ledger's lowercase `true`."
metrics:
  duration: ~4min
  completed: "2026-07-16"
  tasks: 2
  files: 2
  tests_added: 13
  tests_total_phase39: 264
status: complete
---

# Phase 39 Plan 12: Serialize Adapter Evidence and Freshness into scan.log Summary

One documented CLI invocation now writes a `scan.log` that carries every field
row 39-07-02 asserts — the adapter's redacted evidence projection (`mem:`,
`mem_ballpark`, blacklist counts, per-folder dispositions, `allow_partial_data_root`,
the redacted `GSD_DATA_ROOT=` marker), plus per-run freshness markers
(`run_timestamp`, `run_nonce`) and the renamed `scan_exit_code` / derived
`evidence_byte_identity` fields. A source that cannot produce evidence fails
loudly (`TypeError` naming `evidence_lines`) rather than silently writing an
evidence-poor scan.log — the exact failure mode that let this gap survive
Waves 4–6.

## What Changed

### `pinn/data/stage_scan.py`

- **`_source_evidence_lines(source)`** — new fail-closed probe beside
  `_materialize_records`. Duck-types `evidence_lines` off the source; if not
  callable, raises `TypeError` naming `evidence_lines` and stating the source
  must be an admitted-set adapter. Coerces the return to `tuple` and validates
  every element is a `str`. No `hasattr`-and-skip fallback — a silent
  evidence-poor scan.log is precisely the defect 39-VERIFICATION.md found.
- **`_scan_log`** — signature changed to
  `_scan_log(split_evidence, *, evidence_lines, report, exit_code, run_timestamp,
  run_nonce)`. Emits in exact order: `schema_version`, `run_timestamp`,
  `run_nonce`, every `evidence_lines` entry verbatim, the splits.json evidence
  block, the new `evidence_byte_identity=<true|false>` (derived from
  `split_evidence["byte_identity"]`, not hardcoded), then the readiness tail.
- **Readiness tail** — `exit_code=` renamed to `scan_exit_code=` for both the
  pending (`scan_exit_code=pending`) and final (`scan_exit_code={exit_code}`)
  paths, matching row 39-07-02's anchored `^scan_exit_code=[0-9]+$` regex and
  39-07-PLAN.md:110's `scan_exit_code ∈ {0,2}` contract.
- **`_write_scan_log`** — accepts and forwards `evidence_lines`, `run_timestamp`,
  `run_nonce` to `_scan_log`.
- **`main()`** — generates `run_timestamp` (ISO-8601 UTC `...Z` via
  `datetime.now(timezone.utc)`) and `run_nonce` (16-hex via `secrets.token_hex(8)`)
  once after the preflight validation and before adapter construction; computes
  `evidence_lines = _source_evidence_lines(source)` once after construction;
  passes all three to every `_write_scan_log` call site (pending + two final
  writes) so one run stamps one identity.

### `tests/phase39/test_stage_scan.py`

- **`_ReportSource.evidence_lines()`** — returns a realistic tuple mirroring the
  adapter's redacted projection (`GSD_DATA_ROOT=$GSD_DATA_ROOT source=...`, four
  `brutus_folder ... present=True`, `allow_partial_data_root=0`, blacklist
  counts, one `folder ...` line, `mem:`, `mem_ballpark`, `gold_numeric_stage_count`).
- **`StageScanCliContract`** — extended the full-pass assertion to check
  evidence passthrough, freshness markers, `scan_exit_code=0`,
  `evidence_byte_identity=true`, and privacy (no `root: ` line, no home prefix);
  updated the fatal-path assertion from `exit_code=2` to `scan_exit_code=2`;
  added `test_cli_stamps_one_run_timestamp_and_nonce_across_writes` (distinct
  nonces across runs), `test_cli_exit_code_field_renamed_to_scan_exit_code`
  (no bare `exit_code=` line), and `test_cli_fail_closed_source_without_evidence_lines`
  (TypeError on a source lacking `evidence_lines()`).
- **`ScanLogLedgerRowContract`** — new test class with the single authoritative
  `test_scan_log_satisfies_validation_row_39_07_02_field_contract`, driven by
  the module-level `_ROW_39_07_02_PATTERNS` tuple (deliberate duplicate of the
  ledger row's regex set, with a docstring note requiring lockstep updates).
  Asserts every pattern, both privacy conditions (no `root: ` line, no
  `str(Path.home())`), and the `mem:` fraction ≤ 0.7 watermark — all dataset-free.

## Verification

- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan` — 31/31 OK
- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py'` — 264/264 OK (baseline 251 + ~13 added; exceeds the 260 threshold)
- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -p 'test_*.py'` — 447/447 OK (exceeds the 443 threshold)
- `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_prohibitions tests.phase39.test_adapter` — 133/133 OK
- `git diff --exit-code -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — clean
- `test -z "$(git status --short -- simulation_data)"` — corpus untouched

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Python bool capitalization in `evidence_byte_identity`**
- **Found during:** GREEN phase test run
- **Issue:** `f"evidence_byte_identity={split_evidence['byte_identity']}"` rendered Python's `True` (capitalized), but row 39-07-02 and 39-07-PLAN.md:117 mandate the lowercase `true`.
- **Fix:** `f"evidence_byte_identity={str(split_evidence['byte_identity']).lower()}"`.
- **Files modified:** `pinn/data/stage_scan.py`
- **Commit:** aef5507b

**2. [Plan acceptance-criterion over-broad grep — documented, not auto-fixed]**
- **Found during:** acceptance-criteria verification
- **Issue:** The plan's acceptance criterion `grep -cE '(^|[^_])exit_code='` returns 4 (not 0) because it matches the plan-mandated `exit_code=` keyword parameter names in `_write_scan_log` call sites and the `exit_code` parameter itself. The plan action explicitly keeps `exit_code` as the parameter name ("Change `_scan_log`'s signature to `_scan_log(..., exit_code, ...)`") while renaming only the *emitted field* to `scan_exit_code=`. The grep proxy cannot distinguish internal parameter names from emitted fields.
- **Resolution:** The emitted field is verified renamed by `test_cli_exit_code_field_renamed_to_scan_exit_code` (asserts no line starts with `exit_code=` and `scan_exit_code=0` is present). The parameter name is retained per the plan action. No code change — the deviation is the acceptance criterion's over-broad proxy, not a code defect.
- **Files modified:** none (test assertion adjusted to check per-line, not substring)

## Known Stubs

None. All emitted scan.log fields are wired to real data sources (adapter `evidence_lines()`, `_split_file_evidence`, per-run freshness generation).

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| T-39-13 (mitigated) | pinn/data/stage_scan.py | `_source_evidence_lines` raises `TypeError` on a source without `evidence_lines()`; `ScanLogLedgerRowContract` fails dataset-free the moment a field stops being emitted |
| T-39-08 (mitigated) | pinn/data/stage_scan.py | One `run_timestamp` + one `run_nonce` per run, stamped before adapter construction and reused across all three writes; `scan_exit_code=pending` makes an aborted artifact fail the anchored numeric regex |
| T-39-10 (mitigated) | pinn/data/adapter.py → stage_scan.py | Redaction stays the adapter's fail-closed invariant; `stage_scan.py` adds no second redaction rule. `ScanLogLedgerRowContract` asserts the home prefix is absent from emitted bytes |

## Self-Check: PASSED

- `pinn/data/stage_scan.py` — modified, contains `_source_evidence_lines`, `scan_exit_code`, `secrets`, `timezone`
- `tests/phase39/test_stage_scan.py` — modified, contains `_ROW_39_07_02_PATTERNS`, `ScanLogLedgerRowContract`, `_ReportSource.evidence_lines()`
- Commit `aef5507b` exists on `milestone/v2.0`
- 264 phase39 tests pass; 447 total tests pass
