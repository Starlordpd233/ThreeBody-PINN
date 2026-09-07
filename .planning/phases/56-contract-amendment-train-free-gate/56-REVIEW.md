---
phase: 56-contract-amendment-train-free-gate
reviewed: 2026-09-07T00:00:00Z
depth: standard
files_reviewed: 9
files_reviewed_list:
  - pinn/verification/architecture_characterization_probe.py
  - pinn/verification/artifacts/r_ref_stage0.json
  - pinn/verification/gate04_train_free.py
  - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
  - tests/phase56/__init__.py
  - tests/phase56/fixtures/pre_amendment_baseline.json
  - tests/phase56/test_gate04_train_free.py
  - tests/phase56/test_spec_amendment_contract.py
  - tools/spec-render-check/adjudications/22-02-pinn-architecture.json
findings:
  critical: 1
  warning: 4
  info: 0
  total: 5
status: issues_found
---

# Phase 56: Code Review Report

**Reviewed:** 2026-09-07T00:00:00Z
**Depth:** standard
**Files Reviewed:** 9
**Status:** issues_found

## Summary

Reviewed the GATE-04 train-free gate implementation (`pinn/verification/gate04_train_free.py`, entirely new: 1087 lines), its supporting probe helper addition (`ratified_causal_weights` in `architecture_characterization_probe.py`), the regenerated `r_ref_stage0.json` reference artifact, the `pinn_architecture.md` §3.2/§2.2/§4.1 amendment blocks, the SC5 pre/post-amendment demonstration test suite, the spec-amendment content-match tests, and the render-oracle adjudication update.

Per the task brief, GAP-56-01 (condition (ii) always raising `NotImplementedError`) and GAP-56-02 (the untouched §2.4 table reconciliation) are owner-ruled-pending and are not treated as defects below — condition (ii)'s permanent `NotImplementedError` and its `UNRATIFIED`-tagged diagnostics are working as designed.

`tests/phase56/test_spec_amendment_contract.py` (13 tests, content-match/adjudication checks) was run directly and passes. The heavier `tests/phase56/test_gate04_train_free.py` end-to-end classes (`RunGateEndToEndTests`, `Gate04PreAmendmentDemonstrationTests`) run one or two full six-case `run_gate()` measurements each and did not finish inside the review window; the findings below were independently confirmed by direct code tracing and, for the two most consequential items, by reproducing the underlying arithmetic in an isolated Python calculation against the actual six-case data recorded in `r_ref_stage0.json`.

Two categories of defect were found: (1) a genuine data-safety gap — the CLI's `--r-ref-path` write target is never checked against the `simulation_data/`-protection guard that `--evidence-root` explicitly receives, and (2) several new-code correctness/robustness issues in the Phase 56 diff (an incorrect mathematical claim baked into a docstring and locked in by a test, a syntactically-invalid regeneration command in a committed fixture, a provenance field that is captured but never persisted, and a fragile double-measurement equality assertion that can turn a successfully completed gate run into a silent, contentless CLI failure).

## Critical Issues

### CR-01: `--r-ref-path` is never checked against the dataset-write guard, unlike `--evidence-root`

**File:** `pinn/verification/gate04_train_free.py:1020-1069` (see also `934`, `992-995`)
**Issue:** `main()` explicitly protects one CLI-supplied write target before doing any work:

```python
try:
    _reject_dataset_evidence_root(args.evidence_root)
except Exception as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 1
```

`_reject_dataset_evidence_root` (imported from the probe module) exists specifically to "prevent an untrusted evidence-root from writing into `simulation_data`" — and the module's own docstring for `main()` calls this out as a deliberate design property: *"a hostile path is refused before... any directory is created."*

But `--r-ref-path` (`_parse_args`, default `R_REF_ARTIFACT_PATH`) is a second, independent write target reaching the exact same `atomic_write_text` primitive (via `write_r_ref_artifact`, which creates parent directories with `mkdir(parents=True, exist_ok=True)` and then writes a file), and it is **never validated**:

```python
if args.cases_config is None and verdict_obj is not None and verdict_obj.cases:
    write_r_ref_artifact(verdict_obj, path=args.r_ref_path)
```

An operator (or a caller script, e.g. a future Phase 57 `RUN-04` integration) that passes `--r-ref-path simulation_data/<anything>` — by mistake, by a stale default, or by a copy/paste from `--evidence-root` — will have this tool silently create directories and write a governed JSON artifact inside the project's protected, empirically-verified `simulation_data/` tree, with no rejection at all. This is exactly the class of write this codebase's governance treats as sacrosanct (see `CLAUDE.md` / `docs/` conventions on `simulation_data/`), and the guard to prevent it already exists and is used for the sibling parameter — it is simply not applied here.

No test exercises `--r-ref-path` pointed at `simulation_data/`; `test_dataset_evidence_root_rejected_before_any_write` only covers `--evidence-root`.

**Fix:**
```python
try:
    _reject_dataset_evidence_root(args.evidence_root)
    _reject_dataset_evidence_root(args.r_ref_path)
except Exception as exc:  # noqa: BLE001 - reported to the operator, not raised
    print(f"error: {exc}", file=sys.stderr)
    return 1
```

## Warnings

### WR-01: `condition_iii_diagnostics`'s "cannot move at any magnitude" claim is mathematically incorrect

**File:** `pinn/verification/gate04_train_free.py:500-537` (docstring), locked in by `tests/phase56/test_gate04_train_free.py:412-416` (`test_docstring_states_both_structural_findings`)
**Issue:** The docstring asserts, as a structural/universal fact:

> "A reduction confined to bins `late_bin_start` onward cannot move `front_idx` at any magnitude, because the weight at bin `n` depends only on the exclusive prefix over bins `0..n-1`: nothing that happens at or after bin `n` can change it."

This conflates two different claims. The exclusive-prefix fact is true, but it only proves that the weight *at* index `late_bin_start` itself (which depends on bins `0..late_bin_start-1`, i.e. bins strictly before the perturbed range) is unaffected. Weights at indices `> late_bin_start` (e.g. index 9 when `late_bin_start = 8`) depend on prefixes that *include* the perturbed bins (index 9's weight sums bins `0..8`, which includes perturbed bin 8), so they are **not** structurally guaranteed unaffected. I confirmed this by replaying the exact recipe on case `"41"`'s real recorded `raw_bin_means`/`r_ref` from `r_ref_stage0.json`:

```
factor=1.0:  w[9]=0.000313
factor=0.0:  w[9]=0.001006   # weight DOES move in response to the "late-bin-only" perturbation
```

The reason `front_idx` nonetheless stays at 0 for all nine tested factors in all six audited cases is a **data-dependent** fact — the eight unperturbed early bins already sum to an exponent so deeply negative that even eliminating the entire perturbed tail's contribution cannot lift any later weight above 0.5 — not a mathematical necessity following from the prefix structure "at any magnitude" or for any `late_bin_start`. A future change to `late_bin_start` (the function's own parameter, validated for the full `[0, RATIFIED_N_BINS]` range) or to the recipe's residual magnitudes could violate this claim, and the incorrect justification gives no warning that it needs re-checking. The committed test enforces the presence of this wording, so a future correction of the docstring's reasoning would itself need a test change — the incorrect claim is now load-bearing documentation, not just a comment.

The diagnostic's *measured values* are correct (real calls into `ratified_causal_weights`, no shortcut); this finding is about the stated justification, which overstates what is actually guaranteed.

**Fix:** Rephrase the second structural finding to scope the guarantee correctly, e.g.: "Weight at bin `late_bin_start` itself is guaranteed unaffected (it depends only on bins `0..late_bin_start-1`); weights at later indices *can* respond to the late-bin perturbation in principle, but for these six cases the un-perturbed early-bin prefix already suppresses them far below 0.5, so no observed front-index change is a fact about the current residual magnitudes, not an algebraic guarantee for arbitrary `late_bin_start`." Then loosen `test_docstring_states_both_structural_findings` to match the corrected, narrower claim.

### WR-02: SC5 fixture's `regeneration_command` is not valid Python (`%%` instead of `%`)

**File:** `tests/phase56/fixtures/pre_amendment_baseline.json:11`
**Issue:** The frozen fixture's `_meta.regeneration_command` field documents the exact command used to regenerate it, but contains a copy/paste defect:

```
... 'ic13_rng_scheme': 'zero: %s; random_tanh: %s' %% (_IC13_RNG_SCHEME_ZERO, _IC13_RNG_SCHEME_RANDOM_TANH)}) ...
```

`%%` is not a valid Python operator; `compile()`-checking the embedded `python -c "..."` payload raises `SyntaxError: invalid syntax`. The sibling Phase 55 fixture this was adapted from (`tests/phase55/fixtures/six_case_baseline.json:11`) has the same line with a single `%`, confirming this is a transcription error introduced while adapting it for Phase 56, not an intentional escape. No test executes this string, so nothing currently catches it, but the field exists specifically so a future maintainer can regenerate this frozen comparison baseline — as written, running it verbatim fails immediately.

**Fix:** Replace `%%` with `%` in the stored command string (matching the Phase 55 fixture's working form), and re-serialize the JSON.

### WR-03: `_PRE_IMPORT_FALLBACK` is captured but never recorded — dead provenance capture, contradicting the module's own "provenance-complete" claim

**File:** `pinn/verification/gate04_train_free.py:28-32`
**Issue:** The module opens with the same pattern used by every sibling instrument in `pinn/verification/` (`gradcheck_probe.py`, `residual_probe.py`, `overfit_probe.py`, `componentwise_ad.py`):

```python
_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None
```

with the comment "This must precede Torch and pinn.runtime imports: it is the only reliable record of the fallback environment that existed before Torch initialization." In every one of those sibling modules, the captured value is subsequently written into the provenance/evidence dict (`"pre_import_fallback": _PRE_IMPORT_FALLBACK`). In `gate04_train_free.py` it is captured and then **never referenced again** — neither `_cli_provenance()` nor any other dict includes it. The module's own docstring for `main()` describes its output as a "provenance-complete evidence record," and this is precisely the kind of MPS-relevant fact that matters given the module explicitly supports `--device mps`. As written, the value is dead code that silently drops the one fact its own comment says is otherwise unrecoverable ("the only reliable record").

**Fix:** Add `"pre_import_fallback": _PRE_IMPORT_FALLBACK` to `_cli_provenance()`'s returned dict, matching the sibling modules' convention.

### WR-04: `write_r_ref_artifact`'s strict-equality re-derivation is a fragile double-measurement coupling that can turn a completed run into a silent CLI failure

**File:** `pinn/verification/gate04_train_free.py:722-786` (`run_gate`), `788-903` (`write_r_ref_artifact`), `1057-1069` (`main`)
**Issue:** `run_gate` computes `r_ref` via `compute_r_ref`, which internally measures each case's raw bin means once and returns them as `_per_case_means` — deliberately discarded (leading underscore, never passed onward). It then calls `evaluate_case` for every case, which **independently re-measures** the same case's raw bin means from scratch via a second, separate call to `_measure_raw_bin_means` (a fresh `build_network` + full forward/backward-mode `componentwise_du` pass). `write_r_ref_artifact` then asserts these two independently-computed values agree exactly:

```python
recomputed = float(np.median(concatenated))   # from evaluate_case's raw_bin_means
if verdict.r_ref != recomputed:               # verdict.r_ref came from compute_r_ref's own measurement
    raise ValueError(...)
```

On CPU/float64 this has apparently held in practice (the committed `r_ref_stage0.json` has `"valid": true`), but the module explicitly supports `--device mps` (`choices=("mps", "cpu")`) — Apple's Metal reduction kernels are not guaranteed to produce bit-identical results across two separate kernel launches of the same computation, and no committed test exercises this equality check on `--device mps` (`Gate04CLIDefaultRunTests` and `RunGateEndToEndTests` both run on the CPU default). If the two independent forward passes ever diverge by even one ULP, `write_r_ref_artifact` raises, and that exception is caught by `main()`'s **outer** `except Exception: return 1` — which is reached *after* `run_dir`/`raw.json` were already written but *before* any `print(line)` / `print(f"evidence=...")` runs. The net effect: a `run_gate()` call that legitimately computed a correct PASS (or BLOCK) verdict is reported to the operator as a bare exit code 1 with **no stdout at all**, directly contradicting the module's own documented exit-code contract ("the process exit code reports whether the tool COMPLETED... a rendered BLOCK verdict is... still exit 0").

**Fix:** Thread `compute_r_ref`'s already-computed `_per_case_means` into `evaluate_case` (or a lower-level helper) instead of re-measuring, so there is exactly one measurement per case and no equality assertion between two independent computations is needed; alternatively, if the double-measurement is intentional as a self-check, catch the specific `ValueError` from `write_r_ref_artifact` in `main()` separately from the write-path I/O errors, and still print the verdict line / evidence path before returning a distinct non-zero exit code, so a real verdict is never silently swallowed.

---

_Reviewed: 2026-09-07T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
