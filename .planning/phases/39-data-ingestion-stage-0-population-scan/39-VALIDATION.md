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

- **After every task commit:** Run the task's exact `<verify><automated>` command from the map below. The whole-tree prohibition audit runs only in rows that list it and again at 39-07-03, avoiding a Wave-4 source-discovery race while Plans 05/06 write distinct modules.
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
| 39-01-03 | 01 | 0 | DATA-01..06 | T-39-01..T-39-06 | All suites collect; GAP-39-11 split-only `MISSING_BASE`, GAP-39-12 Option-C quotas, and DATA-06 full-count 239/240 plus full≥240/train<240 contracts are deferred explicitly | scaffold | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v` | ✅ W0 planned | ⬜ pending |
| 39-02-01 | 02 | 1 | DATA-01 / DATA-03 | T-39-01 / T-39-05 | Frozen types, parser containment, footer/measured dt_out provenance, version outcomes, and GAP-39-10 global-T/no-per-record-T contract | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-02-02 | 02 | 1 | DATA-01 / DATA-02 / DATA-04 / DATA-05 / DATA-06 | T-39-02 | Preprocessing/Lmax/normalization plus sole stages.py classifier: base Set 1a numeric, all gold UNASSIGNED, zero numeric gold | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_stages -v` | ✅ W0 planned | ⬜ pending |
| 39-02-03 | 02 | 1 | DATA-02 | T-39-02 / T-39-03 | Seven admission clauses and GAP-39-04/05 boundaries fail closed | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-02-04 | 02 | 1 | DATA-01 / DATA-06 | T-39-02 | Phase-local SPEC defect banners point at GAP-39-02/03/08 so literal verifiers read correct behavior as correct (HIGH-4) | artifact/spec | `bash -c 'set -euo pipefail; s=.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md; rg -q "GAP-39-03" "$s"; rg -q "GAP-39-08" "$s"; rg -q "GAP-39-02" "$s"; rg -q "routed build-discovered spec defect" "$s"; git diff --exit-code -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md'` | ✅ W0 planned | ⬜ pending |
| 39-03-01 | 03 | 2 | DATA-01..03 | T-39-01 / T-39-03 / T-39-05 | First pass calls only stages.py before residency and hard-fails unless gold_numeric_stage_count is zero | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission -v` | ✅ W0 planned | ⬜ pending |
| 39-03-02 | 03 | 2 | DATA-01..03 | T-39-02 | Second pass normalizes/materializes fp32 and serves base-only numeric StageQuery pools with all gold UNASSIGNED | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter -v` | ✅ W0 planned | ⬜ pending |
| 39-03-03 | 03 | 2 | DATA-01..03 | T-39-01..T-39-06 | Sole-reader/sole-classifier, zero-gold, disk independence, two-pass, logs, and prohibitions integrate | integration/security | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_adapter tests.phase39.test_admission tests.phase39.test_prohibitions -v` | ✅ W0 planned | ⬜ pending |
| 39-04-01 | 04 | 3 | DATA-04 | T-39-04 / T-39-08 | StageIndex/split use persisted base labels; GAP-39-11 gold-only groups use split-only `MISSING_BASE`, are assigned once, never enter numeric pools, and do not leak physical keys | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_splits -v` | ✅ W0 planned | ⬜ pending |
| 39-04-02 | 04 | 3 | DATA-04 | T-39-04 / T-39-08 | Canonical manifest is byte-stable, atomic, and records allocation provenance | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_splits -v` | ✅ W0 planned | ⬜ pending |
| 39-05-01 | 05 | 4 | DATA-05 | T-39-02 / T-39-10 | Replay/lookahead are base Set 1a only and hard-fail blacklist, gold, or non-Set1a bypass | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v` | ✅ W0 planned | ⬜ pending |
| 39-05-02 | 05 | 4 | DATA-05 | T-39-02 / T-39-11 | GAP-39-10 fixes global T=10/no FixedBatch.T; GAP-39-12 Option C gives q/r per-identity quotas (256→16 each; 240→17 each plus 16 seeded extras), independent times, reused energy points, and Phase-40 adaptive boundary | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v` | ✅ W0 planned | ⬜ pending |
| 39-06-01 | 06 | 4 | DATA-06 | T-39-02 / T-39-12 | Report consumes sole-classifier labels, asserts zero numeric gold, and binds fatal only to admitted/full 239/240; full≥240/train<240 is nonfatal while train remains diagnostic | unit | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v` | ✅ W0 planned | ⬜ pending |
| 39-06-02 | 06 | 4 | DATA-06 | T-39-04 / T-39-12 | CLI writes atomic report/manifest evidence, exits 2 only for admitted/full<240, exits 0 for admitted/full≥240 regardless of diagnostic train count | integration | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v` | ✅ W0 planned | ⬜ pending |
| 39-07-01 | 07 | 5 | DATA-01..06 | T-39-01..T-39-06 | Dataset-free/repository PASS and structured command results; explicit rg status handling treats rc=1 as no match, rc=0 as failure found, and rc≥2 as audit error under `set -euo pipefail` | regression/evidence | `bash -c 'set -euo pipefail; assert_absent() { local pattern=$1 file=$2 label=$3 rc; if rg -q -- "$pattern" "$file"; then echo "prohibited match found: $label" >&2; return 1; else rc=$?; if [ "$rc" -eq 1 ]; then return 0; fi; echo "rg absence audit failed for $label with status $rc" >&2; return "$rc"; fi; }; log=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/dataset-free.log; test -s "$log"; rg -q "^phase39_suite=PASS$" "$log"; rg -q "^repository_suite=PASS$" "$log"; rg -q "Ran [0-9]+ tests" "$log"; test -n "$(rg "^command_result=[A-Za-z0-9._-]+:exit=0$" "$log")"; if rg -q "^command_result=[A-Za-z0-9._-]+:exit=[1-9][0-9]*$" "$log"; then echo "nonzero command_result found" >&2; exit 1; else rc=$?; if [ "$rc" -ne 1 ]; then echo "rg command_result audit failed with status $rc" >&2; exit "$rc"; fi; fi; assert_absent "skipped Phase39 production symbol" "$log" "skipped Phase39 production symbol"'` | ✅ prior rows | ⬜ pending |
| 39-07-02 | 07 | 5 | DATA-01..06 | T-39-01..T-39-06 | Real report/manifest are retained byte-identically; full/admitted count is the only 0/2 exit operand; train count is retained diagnostic Phase-40 seam evidence | dataset-backed/evidence | **Run:** `GSD_DATA_ROOT=<simulation_data/Data> $HOME/miniforge3/envs/pinn-train/bin/python -m pinn.data.stage_scan --run-dir /tmp/phase39-real-scan`. **Exact task verify:** `bash -c 'set -euo pipefail; assert_absent() { local pattern=$1 file=$2 label=$3 rc; if rg -q -- "$pattern" "$file"; then echo "prohibited match found: $label" >&2; return 1; else rc=$?; if [ "$rc" -eq 1 ]; then return 0; fi; echo "rg absence audit failed for $label with status $rc" >&2; return "$rc"; fi; }; e=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close; test -z "${GSD_ALLOW_PARTIAL_DATA_ROOT:-}"; test -s "$e/scan.log"; test -s "$e/stage_population.json"; test -s "$e/splits.json"; rg -q "^allow_partial_data_root=0$" "$e/scan.log"; rg -q "^scan_exit_code=[0-9]+$" "$e/scan.log"; rg -q "^run_timestamp=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}" "$e/scan.log"; rg -q "^run_nonce=[0-9a-f]{16}$" "$e/scan.log"; rg -q "^stage0_train_split_count=[0-9]+$" "$e/scan.log"; rg -q "^stage0_full_split_count=[0-9]+$" "$e/scan.log"; rg -q "splits.json_sha256=[0-9a-f]{64}" "$e/scan.log"; rg -q "^evidence_byte_identity=true$" "$e/scan.log"; ec=$(rg -o "^scan_exit_code=[0-9]+$" "$e/scan.log" | cut -d= -f2); test "$ec" = "0" -o "$ec" = "2"; assert_absent "/Users/" "$e/scan.log" "personal path in scan.log"; assert_absent "/Users/" "$e/stage_population.json" "personal path in stage_population.json"; assert_absent "/Users/" "$e/splits.json" "personal path in splits.json"; rg -q "GSD_DATA_ROOT=" "$e/scan.log"; rg -q "gold_numeric_stage_count=0" "$e/scan.log"; rg -q "mem: [0-9]+ \([0-9]+\.[0-9]{6}\) watermark=0\.7" "$e/scan.log"; rg -q "mem_ballpark=[0-9]+" "$e/scan.log"; rg -q "n_blacklist_entries" "$e/scan.log"; rg -q "n_present_on_disk" "$e/scan.log"; ts=$(rg -o "^stage0_train_split_count=[0-9]+$" "$e/scan.log" | cut -d= -f2); fs=$(rg -o "^stage0_full_split_count=[0-9]+$" "$e/scan.log" | cut -d= -f2); test "$ts" -ge 0; if [ "$fs" -lt 240 ]; then test "$ec" = "2"; else test "$ec" = "0"; fi; $HOME/miniforge3/envs/pinn-train/bin/python -c "import json,re; log=open(\"$e/scan.log\").read(); m=re.search(r\"mem: [0-9]+ \\(([0-9]+\\.[0-9]{6})\\) watermark=0\\.7\",log); assert m and float(m.group(1)) <= 0.7; p=json.load(open(\"$e/stage_population.json\")); required={\"schema_version\",\"version_state\",\"admission\",\"stages\",\"s_min\",\"interim_s0\",\"fatal\",\"gold_numeric_stage_count\",\"stage0_full_split_count\",\"stage0_train_split_count\"}; assert required <= p.keys(); assert p[\"gold_numeric_stage_count\"] == 0; assert {\"0\",\"1\",\"UNASSIGNED\"} <= p[\"stages\"].keys(); s=json.load(open(\"$e/splits.json\")); assert s[\"algorithm\"]==\"group-signature-hamilton-v1\"; assert set(s.get(\"ratios\",{}).keys()) == {\"train\",\"validation\",\"test\"}"'` | ✅ prior rows | ⬜ pending |
| 39-07-03 | 07 | 5 | DATA-01..06 | T-39-01..T-39-12 | Reader/classifier/source audit; full count alone controls fatal/readiness; retained train count is diagnostic; full≥240/train<240 passes | audit/evidence | `bash -c 'set -euo pipefail; v=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/verification.log; e=.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close; test -s "$v"; test -s "$e/splits.json"; rg -q "^reader_audit=PASS$" "$v"; rg -q "^classifier_audit=PASS$" "$v"; rg -q "^report_invariants=PASS$" "$v"; rg -q "^manifest_evidence=PASS$" "$v"; rg -q "^gold_numeric_stage_count=0$" "$v"; rg -q "^spec_hashes_match=true$" "$v"; rg -q "^corpus_fingerprint_match=true$" "$v"; rg -q "^evidence_byte_identity=PASS$" "$v"; rg -q "^real_stage0_gold_keys=0$" "$v"; rg -q "^stage0_train_split_count=[0-9]+$" "$v"; rg -q "^stage0_train_split_gold_keys=0$" "$v"; rg -q "^stage0_full_split_count=[0-9]+$" "$v"; rg -q "^phase39_stage0_fatal=(true|false)$" "$v"; rg -q "^phase39_full_set_fatal=(true|false)$" "$v"; rg -q "^phase39_train_ready=(true|false)$" "$v"; rg -q "^phase39_status=(train-ready|executed-fatal-finding-owner-action-required)$" "$v"; rg -q "^phase38_preflight=PASS$" "$v"; if rg -q "^has_stage1=true$" "$v"; then rg -q "^real_stage1_lookahead=16$" "$v"; rg -q "^real_stage1_gold_keys=0$" "$v"; else rg -q "^has_stage1=false$" "$v"; fi; ts=$(rg -o "^stage0_train_split_count=[0-9]+$" "$v" | cut -d= -f2); fs=$(rg -o "^stage0_full_split_count=[0-9]+$" "$v" | cut -d= -f2); fl=$(rg -o "^phase39_stage0_fatal=(true|false)$" "$v" | cut -d= -f2); ff=$(rg -o "^phase39_full_set_fatal=(true|false)$" "$v" | cut -d= -f2); tr=$(rg -o "^phase39_train_ready=(true|false)$" "$v" | cut -d= -f2); test "$ts" -ge 0; if [ "$fs" -lt 240 ]; then rg -q "^real_stage0_replay=${fs}$" "$v"; [ "$ff" = "true" ]; [ "$fl" = "true" ]; [ "$tr" = "false" ]; rg -q "^phase39_status=executed-fatal-finding-owner-action-required$" "$v"; else rg -q "^real_stage0_replay=240$" "$v"; [ "$ff" = "false" ]; [ "$fl" = "false" ]; [ "$tr" = "true" ]; rg -q "^phase39_status=train-ready$" "$v"; fi; $HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_prohibitions tests.phase39.test_stages -v; $HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase38.test_prohibitions -v; git diff --check; git diff --exit-code -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md; test -z "$(git status --short -- simulation_data)"; if [ "$fl" = "true" ]; then exit 1; fi'` | ✅ prior rows | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] Plan 39-01 owns `tests/phase39/__init__.py` and `tests/phase39/_fixtures.py` — deterministic tiny IC/Brutus/blacklist trees under `TemporaryDirectory`.
- [x] Plan 39-01 owns `tests/phase39/test_adapter.py` — deferred frozen types, footer/dt_out, Lmax, normalization, residency, accessors, memory, and version contracts.
- [x] Plan 39-01 owns `tests/phase39/test_admission.py` — DATA-02 clauses, GAP-39-04 near-zero boundary, and GAP-39-05 whole-record quarantine accounting.
- [x] Plan 39-01 owns `tests/phase39/test_stages.py` — sole stages.py classifier, base Set 1a Stage 0/collapsed-1, all gold UNASSIGNED, and `gold_numeric_stage_count == 0`.
- [x] Plan 39-01 owns `tests/phase39/test_splits.py` — base-label/gold-UNASSIGNED signatures, GAP-39-11 split-only `MISSING_BASE`, leakage, ordering, byte determinism, and Hamilton apportionment.
- [x] Plan 39-01 owns `tests/phase39/test_batches.py` — base-only replay/lookahead, GAP-39-10 global T, GAP-39-12 Option-C quotas, zero gold, normalized input, two point sets, and blacklist defense.
- [x] Plan 39-01 owns `tests/phase39/test_stage_scan.py` — GAP-39-03/08 base-only report, zero-gold invariant, full/admitted 239/240 fatal mechanics, and full≥240/train<240 nonfatal regression.
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
| T-39-07 | Elevation via unauthorized reader or global-default mutation | AST exact-reader and global-state audits over discovered production modules (Plan 01). |
| T-39-08 | Repudiation of split seed/order provenance | Persist seed, ratios, algorithm, tie order, and signature quotas/counts/deviations (Plan 04). |
| T-39-09 | Information disclosure of absolute corpus paths | Canonical payload omits absolute roots; risk is local and tests enforce omission (Plan 04). |
| T-39-10 | Repudiation of batch randomness | Caller-owned local Generator and recorded sampled keys/indices; no global seed (Plan 05). |
| T-39-11 | Tampering via point-set aliasing/allocation drift | Separate frozen data/collocation fields and GAP-39-12 exact q/r quota tests with independent per-slot times (Plan 05). |
| T-39-12 | Repudiation of s0/fatal evidence | Persist interim input, exact sorted distribution, threshold/observed typed state; never mutate/ratify (Plan 06). |

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
- [x] GAP-39-10 global `T=10.0`, GAP-39-11 split-only `MISSING_BASE`, and GAP-39-12 Option-C quotient/remainder quotas are represented in task rows and Wave-0 contracts.
- [x] DATA-06 fatal/CLI/phase-close verification is bound only to the admitted/full Stage-0 count; `stage0_train_split_count` remains retained diagnostic Phase-40 seam evidence and full≥240/train<240 passes.
- [x] `nyquist_compliant: true` and `wave_0_complete: true` are set after the 19-task reconciliation (cycle-2 review incorporation added 39-02-04).

**Approval:** validation map reconciled to all 19 final tasks
