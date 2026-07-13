---
phase: 39
slug: data-ingestion-stage-0-population-scan
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-07-13
---

# Phase 39 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` in the `pinn-train` environment |
| **Config file** | none — discovery-based; Wave 0 creates `tests/phase39/` |
| **Quick run command** | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v` |
| **Full suite command** | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -p 'test_*.py' -v` |
| **Estimated runtime** | ~30 seconds for the dataset-free Phase 39 suite; the full-corpus gate is excluded |

---

## Sampling Rate

- **After every task commit:** Run the task's targeted `tests.phase39` module plus `tests.phase39.test_prohibitions`.
- **After every plan wave:** Run `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v`.
- **Before `/gsd-verify-work`:** Run the full repository suite and the real-corpus Phase 39 scan gate.
- **Max feedback latency:** 30 seconds for normal task-level feedback; the real-corpus scan is a final phase gate only.

---

## Per-Task Verification Map

The task IDs below are reconciled one-for-one with all final PLAN tasks.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 39-01-01 | 01 | 0 | DATA-01..06 | T-39-01 / T-39-03 | Deferred tests specify shared types plus sole base-Set-1a classifier and zero numeric gold labels without production ownership | contract | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_stages -v` | ✅ W0 planned | ⬜ pending |
| 39-01-02 | 01 | 0 | DATA-01..06 | T-39-01 / T-39-06 | Synthetic corpus/blacklist fixtures and source-mutation guards exist before production code | fixture/security | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-01-03 | 01 | 0 | DATA-01..06 | T-39-01..T-39-06 | All Phase-39 suites collect with only localized missing-production-symbol skips during Wave 0 | scaffold | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v` | ✅ W0 planned | ⬜ pending |
| 39-02-01 | 02 | 1 | DATA-01 / DATA-03 | T-39-01 / T-39-05 | Frozen types, parser containment, footer/measured dt_out provenance, and version outcomes | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-02-02 | 02 | 1 | DATA-01 / DATA-02 / DATA-04 / DATA-05 / DATA-06 | T-39-02 | Preprocessing/Lmax/normalization plus sole stages.py classifier: base Set 1a numeric, all gold UNASSIGNED, zero numeric gold | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_stages -v` | ✅ W0 planned | ⬜ pending |
| 39-02-03 | 02 | 1 | DATA-02 | T-39-02 / T-39-03 | Seven admission clauses and GAP-39-04/05 boundaries fail closed | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-03-01 | 03 | 2 | DATA-01..03 | T-39-01 / T-39-03 / T-39-05 | First pass calls only stages.py before residency and hard-fails unless gold_numeric_stage_count is zero | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission -v` | ✅ W0 planned | ⬜ pending |
| 39-03-02 | 03 | 2 | DATA-01..03 | T-39-02 | Second pass normalizes/materializes fp32 and serves base-only numeric StageQuery pools with all gold UNASSIGNED | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter -v` | ✅ W0 planned | ⬜ pending |
| 39-03-03 | 03 | 2 | DATA-01..03 | T-39-01..T-39-06 | Sole-reader/sole-classifier, zero-gold, disk independence, two-pass, logs, and prohibitions integrate | integration/security | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-04-01 | 04 | 3 | DATA-04 | T-39-04 / T-39-08 | StageIndex/split use persisted base labels, gold UNASSIGNED/missing, zero numeric gold, and no physical-key leakage | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_splits -v` | ✅ W0 planned | ⬜ pending |
| 39-04-02 | 04 | 3 | DATA-04 | T-39-04 / T-39-08 | Canonical manifest is byte-stable, atomic, and records allocation provenance | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_splits -v` | ✅ W0 planned | ⬜ pending |
| 39-05-01 | 05 | 4 | DATA-05 | T-39-02 / T-39-10 | Replay/lookahead are base Set 1a only and hard-fail blacklist, gold, or non-Set1a bypass | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v` | ✅ W0 planned | ⬜ pending |
| 39-05-02 | 05 | 4 | DATA-05 | T-39-02 / T-39-11 | FixedBatch preserves normalized inputs/two point sets while final assembly enforces zero gold numeric members | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v` | ✅ W0 planned | ⬜ pending |
| 39-06-01 | 06 | 4 | DATA-06 | T-39-02 / T-39-12 | Report consumes sole-classifier base labels, asserts gold_numeric_stage_count=0, and enforces 239/240 | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v` | ✅ W0 planned | ⬜ pending |
| 39-06-02 | 06 | 4 | DATA-06 | T-39-04 / T-39-12 | CLI writes atomic evidence with base-only numeric labels and explicit zero-gold count | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v` | ✅ W0 planned | ⬜ pending |
| 39-07-01 | 07 | 5 | DATA-01..06 | T-39-01..T-39-06 | Dataset-free and repository-suite PASS markers are retained and inspected | regression/evidence | `bash -c 'set -euo pipefail; log=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/dataset-free.log; test -s "$log"; rg -q "^phase39_suite=PASS$" "$log"; rg -q "^repository_suite=PASS$" "$log"'` | ✅ prior rows | ⬜ pending |
| 39-07-02 | 07 | 5 | DATA-01..06 | T-39-01..T-39-06 | Real report is byte-identical and explicitly inspected for gold_numeric_stage_count=0 | dataset-backed/evidence | `bash -c 'set -euo pipefail; e=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close; cmp /tmp/phase39-real-scan/stage_population.json "$e/stage_population.json"; rg -q "gold_numeric_stage_count=0" "$e/scan.log"'` | ✅ prior rows | ⬜ pending |
| 39-07-03 | 07 | 5 | DATA-01..06 | T-39-01..T-39-12 | Reader/classifier audit and real base-only replay/lookahead prove zero gold plus source/evidence integrity | audit/evidence | `bash -c 'set -euo pipefail; v=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/verification.log; rg -q "^classifier_audit=PASS$" "$v"; rg -q "^gold_numeric_stage_count=0$" "$v"; rg -q "^real_stage0_gold_keys=0$" "$v"'` | ✅ prior rows | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Plan 39-01 owns `tests/phase39/__init__.py` and `tests/phase39/_fixtures.py` — deterministic tiny IC/Brutus/blacklist trees under `TemporaryDirectory`.
- [x] Plan 39-01 owns `tests/phase39/test_adapter.py` — deferred frozen types, footer/dt_out, Lmax, normalization, residency, accessors, memory, and version contracts.
- [x] Plan 39-01 owns `tests/phase39/test_admission.py` — DATA-02 clauses, GAP-39-04 near-zero boundary, and GAP-39-05 whole-record quarantine accounting.
- [x] Plan 39-01 owns `tests/phase39/test_stages.py` — sole stages.py classifier, base Set 1a Stage 0/collapsed-1, all gold UNASSIGNED, and `gold_numeric_stage_count == 0`.
- [x] Plan 39-01 owns `tests/phase39/test_splits.py` — base-label/gold-UNASSIGNED signatures, leakage, ordering, byte determinism, and Hamilton apportionment.
- [x] Plan 39-01 owns `tests/phase39/test_batches.py` — base-only replay/lookahead, zero gold, normalized input, two point sets, and blacklist defense.
- [x] Plan 39-01 owns `tests/phase39/test_stage_scan.py` — GAP-39-03/08 base-only report, zero-gold invariant, and fatal mechanics.
- [x] Plan 39-01 owns `tests/phase39/test_prohibitions.py` — exact-reader and sole-classifier allowlists, v1 ban, read-only corpus, containment, and global-default ban.

---

## Manual-Only Verifications

All phase behaviors have automated verification. The external 6.3 GB corpus
scan is intentionally a final automated phase gate rather than a per-task check.
Its report and logs must still be inspected as committed execution evidence.

---

## Threat References

| Ref | Threat | Required control |
|-----|--------|------------------|
| T-39-01 | Configured-root path traversal or symlink escape | Resolve every scanned path and require containment beneath the read-only corpus root. |
| T-39-02 | Malformed, oversized, or non-finite numeric text | Validate structure incrementally, fail closed, and keep `num_workers=0`. |
| T-39-03 | Missing or corrupt blacklist | Reject initialization; never substitute an empty blacklist. |
| T-39-04 | Partial or nondeterministic split-manifest write | Use canonical serialization and atomic replacement inside the run folder. |
| T-39-05 | Ignored version mismatch | Hard-refuse mismatch; emit the typed deferral only when canonical metadata is absent. |
| T-39-06 | Test or scan mutation of the source corpus | Open the corpus read-only; use temporary roots for synthetic tests; audit write targets. |

---

## Validation Sign-Off

- [x] Every final PLAN task maps to exactly one row above.
- [x] All tasks have `<automated>` verification and explicit Wave 0 dependencies where applicable.
- [x] Sampling continuity: every task has automated verification.
- [x] Wave 0 owns all currently missing test files.
- [x] No watch-mode flags are used.
- [x] Normal task feedback latency remains below 30 seconds.
- [x] The final gate runs the full repository suite and real-corpus scan separately.
- [x] DATA-06 tests cite GAP-39-03/08 and prove sole-classifier base Set 1a labels, all-gold UNASSIGNED, and no second predicate.
- [x] DATA-01/02/04/05 tests cite GAP-39-04..08 and enforce all five rulings exactly.
- [x] `nyquist_compliant: true` and `wave_0_complete: true` are set after the 18-task reconciliation.

**Approval:** validation map reconciled to all 18 final tasks
