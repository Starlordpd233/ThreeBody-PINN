---
phase: 43-verification-stage-0-pilot-acceptance
reviewed: 2026-07-22T12:52:06Z
depth: standard
files_reviewed: 26
files_reviewed_list:
  - configs/smoke.yaml
  - configs/stage0-example.yaml
  - pinn/STATUS.md
  - pinn/evaluate.py
  - pinn/train.py
  - pinn/training/config.py
  - pinn/training/config_yaml.py
  - pinn/training/controllers.py
  - pinn/training/summary.py
  - pinn/training/timing.py
  - pinn/verification/gate_metrics.py
  - pinn/verify.py
  - tests/phase43/__init__.py
  - tests/phase43/_fixtures.py
  - tests/phase43/test_evaluate_edge_cases.py
  - tests/phase43/test_evaluate_gate.py
  - tests/phase43/test_gate_boundary.py
  - tests/phase43/test_pilot_calibration.py
  - tests/phase43/test_real_data_smoke_config.py
  - tests/phase43/test_smoke.py
  - tests/phase43/test_summary_enrichment.py
  - tests/phase43/test_summary_honesty.py
  - tests/phase43/test_timing_calibration.py
  - tests/phase43/test_verdict_grounding.py
  - tests/phase43/test_verify_gate.py
  - tests/phase43/test_verify_ladder.py
findings:
  critical: 5
  warning: 3
  info: 0
  total: 8
status: issues_found
---

# Phase 43: Code Review Report

**Reviewed:** 2026-07-22T12:52:06Z  
**Depth:** standard  
**Files Reviewed:** 26  
**Status:** issues_found

## Summary

The Phase 43 acceptance machinery is not safe to ship. The one-time held-out evaluation can be replayed through another output directory and is not claimed before held-out access; the duration gate fingerprints the requested MPS/fp32 runtime even when training will actually run on strict CPU/fp64; and a forged five-entry verify marker with arbitrary rung names is accepted as green. The owner-verdict test also does not compare the verdict with the cited receipt, so it can approve an ungrounded `go` decision.

The focused Phase 43 regression slice passed 111 tests, but those tests do not exercise the reproduced bypasses. The already-disclosed full-suite result remains non-green at 24 failures and 10 errors.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01 [BLOCKER]: Alternate output directories bypass the single-evaluation rule

**File:** `pinn/evaluate.py:138-148,242-252`  
**Issue:** The evaluator permits any output directory beneath the runs root and checks for an existing receipt only inside that selected directory. It never binds evaluation authority to the owning run's canonical `evaluation/` directory or records a run-level claim. Consequently, the same run and held-out split can be evaluated repeatedly by invoking the evaluator with `evaluation-a`, `evaluation-b`, and so on. A direct counterexample completed two evaluations of one run with different output directories. Existing coverage only verifies refusal when the exact same output directory is reused (`tests/phase43/test_evaluate_gate.py:223-234`).

**Fix:** Require the resolved output to equal `<run_dir>/evaluation`, and store the attempt/receipt at a fixed run-owned path that the caller cannot redirect. Add a regression test proving that a second invocation with a different `--output` is refused.

### CR-02 [BLOCKER]: Held-out access is not claimed atomically before evaluation begins

**File:** `pinn/evaluate.py:246-334`  
**Issue:** Receipt absence is checked before evaluation, but the receipt is written only after the held-out corpus has been loaded, every model forward pass has completed, and metrics artifacts have been written. A crash or exception after held-out access but before line 334 leaves no durable evidence that the one allowed evaluation was consumed. Two concurrent evaluators can also both pass the existence check before either writes a receipt. The Phase 43 verdict itself records an MPS/fp64 crash after held-out processing without a corresponding receipt, demonstrating this is reachable rather than hypothetical.

**Fix:** Immediately before the first held-out read/forward pass, create a run-level attempt record with exclusive creation (`O_CREAT | O_EXCL`). Finalize that record into a success/failure receipt without erasing failed or abandoned attempts. Keep pre-access validation failures outside the claim, and add injected-failure and concurrent-process tests.

### CR-03 [BLOCKER]: The duration gate fingerprints a runtime different from the one training executes

**File:** `pinn/train.py:448-482`  
**Issue:** `_check_duration_gate` builds its fingerprint from `config.run.precision` and `config.run.device`. Only later does `_resolve_runtime_spec` apply `strict_cpu_determinism`, which forces CPU/fp64. Thus a configuration requesting MPS/fp32 with strict determinism checks MPS/fp32 calibration and verification artifacts, then actually launches CPU/fp64 training. A fast MPS calibration can authorize a CPU/fp64 run whose real forecast exceeds 30 minutes without a green CPU/fp64 ladder.

**Fix:** Resolve the effective runtime before the duration gate, use that same immutable runtime specification for calibration lookup, marker validation, and model construction, and add a regression asserting strict determinism fingerprints `device=cpu` and `precision=float64` regardless of requested values.

### CR-04 [BLOCKER]: A forged verify marker with arbitrary rung names is accepted as green

**File:** `pinn/verify.py:286-291,448-481`  
**Issue:** `ladder_is_green` checks only that there are five entries and every entry has a truthy `passed` value. Marker validation does not require the exact rung names, order, uniqueness, field types, or supported schema version. A marker containing five duplicate records named `not_a_rung`, all with `passed: true`, is accepted by both `ladder_is_green` and `marker_is_green_and_fresh`. This bypasses the safety gate for runs forecast above 30 minutes.

**Fix:** Validate the complete marker schema and require `[record["name"] for record in records] == list(LADDER)`, exact booleans, the current schema version, and expected fingerprint fields before accepting freshness. Add malformed, duplicate, reordered, missing, unknown-rung, and stale-schema tests.

### CR-05 [BLOCKER]: The owner verdict “grounding” test never reads the cited receipt

**File:** `tests/phase43/test_verdict_grounding.py:24-60`  
**Issue:** The test uses a hand-written frontmatter parser, checks only a few strings, and merely verifies that the receipt path text appears somewhere in the verdict. It never opens or parses the cited receipt, compares the receipt's gate/metrics/digests with the verdict, or validates the hashes claimed in the body. The document can therefore be changed to `gate: PASS`, `verdict: go`, and `owner_decision: go` while still citing a FAIL receipt, and the acceptance test will pass. The parser can also be bypassed by valid quoted YAML such as `gate: "FAIL"`, and the date regex accepts impossible calendar dates.

**Fix:** Parse frontmatter with `yaml.safe_load`, validate typed fields and the date with `date.fromisoformat`, resolve and load the cited receipt, and assert that gate result, metrics, model/config/data digests, and allowed owner decision agree with that receipt. Add receipt-mismatch, quoted-YAML, and invalid-date cases.

## Warnings

### WR-01 [WARNING]: The code fingerprint ignores dirty source changes

**File:** `pinn/verify.py:312-360`  
**Issue:** `current_fingerprint` represents code solely by Git HEAD. Editing tracked training or verification source without committing leaves HEAD unchanged, so a calibration and green marker produced before the edit remain “fresh” for materially different code. This undermines the marker's claimed code-binding and can authorize a long run against unverified local source.

**Fix:** Either fail closed when relevant tracked files are dirty or include a deterministic digest of the relevant tracked-file contents and paths in both the fingerprint and marker. Add a test that modifies a relevant file under the same HEAD and confirms freshness is rejected.

### WR-02 [WARNING]: Frozen relative data roots change meaning with the evaluator's working directory

**File:** `pinn/training/config_yaml.py:276-295`  
**Issue:** An explicit relative `data.root` is frozen unchanged. Training and evaluation subsequently resolve it against their current process working directory (`pinn/train.py:268-303`, `pinn/evaluate.py:254-264`). Evaluating the same frozen run from another directory can therefore fail to find the corpus or select a different corpus at the same relative path. Current fixtures use absolute roots and do not cover cross-directory replay.

**Fix:** Resolve `data.root` relative to the source configuration file (or another documented stable base), freeze the canonical absolute path, and use that frozen value everywhere. Add a test that launches and evaluates from different working directories.

### WR-03 [WARNING]: Phase-local green tests mask an unresolved repository-wide compatibility regression

**File:** `pinn/train.py:455-462`  
**Issue:** The new fail-closed timing-calibration requirement breaks older Phase 41/42 subprocess fixtures, contributing to the disclosed full-suite result of 24 failures and 10 errors. Phase 43 tests prove the new isolated behavior but do not migrate the shared launch fixtures or otherwise restore repository-wide compatibility. Shipping with the full suite non-green makes subsequent regressions indistinguishable from this known breakage.

**Fix:** Update the older launch fixtures to provision a real, matching timing calibration (or explicitly select smoke mode only where the test genuinely models a smoke run), repair the unrelated Phase 39 false-positive detector, and require the full repository suite to pass before closing the acceptance phase.

---

_Reviewed: 2026-07-22T12:52:06Z_  
_Reviewer: the agent (gsd-code-reviewer)_  
_Depth: standard_
