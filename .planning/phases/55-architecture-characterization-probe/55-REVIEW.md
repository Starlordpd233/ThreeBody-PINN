---
phase: 55-architecture-characterization-probe
reviewed: 2026-09-06T04:22:04Z
depth: deep
files_reviewed: 5
files_reviewed_list:
  - pinn/verification/architecture_characterization_probe.py
  - tests/phase55/__init__.py
  - tests/phase55/test_architecture_characterization.py
  - tests/phase55/fixtures/six_case_baseline.json
  - tests/phase38/test_prohibitions.py
findings:
  critical: 0
  warning: 2
  info: 2
  total: 4
status: issues
---

# Phase 55: Code Review Report

**Reviewed:** 2026-09-06T04:22:04Z
**Depth:** deep
**Files Reviewed:** 5
**Status:** issues

## Narrative Findings (AI reviewer)

## Summary

Adversarial review of the Phase 55 architecture-characterization probe against the 55-01..04 must_haves/prohibitions, with call-chain tracing into `pinn/training/controllers.py`, `pinn/loss_catalog.py`, `pinn/physics_residual.py`, `pinn/runtime.py`, and the `residual_probe.py` analog.

The five review focus areas hold in the measurement path:

1. **SC3 derivation.** `measure_case` calls `componentwise_du`, `softened_acceleration`, and `causal_physics_loss(..., return_details=True)` and mirrors `controllers.py:639-694` for `traj` / `u_leaf` / `rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0` / `w_n` / `front_idx`. It does not import or call `physics_residual.physics_residual`. `test_derives_from_trainer_implementation` patches the three module bindings and asserts lock-step movement of `causal_weights`, `f_grav_norm_median`, and the derivative norms.
2. **D-03 containment.** `stratified_collocation_times` and `bin_mean_residuals` are not referenced from `run_sweep` / `measure_case` / `main`. The AST closure has a non-vacuity guard (`_ic13_for_case`), and the causal-point recorder asserts every default-path `causal_physics_loss` call receives `DEFAULT_N_COL=16` residuals.
3. **Fixture immutability.** The suite opens `six_case_baseline.json` read-only. Perturbation is in-memory (`copy.deepcopy`). A session-scoped sha256 autouse plus `test_fixture_file_is_never_written_by_the_suite` prevent self-heal. No production module references the fixture path.
4. **CLI exit-code non-verdict.** `main` returns `0` iff `run_sweep` completed; `failure` is `None` or `{type, message}`. Top-level evidence keys are a closed frozenset with no `passed` / threshold / GATE-04 field. The printed summary reports quantities only.
5. **Clamp floor derived, not literal.** `causal_clip_min_weight` is `resolve_causal_clip_facts(dtype, device)['causal_clip_min_weight']`. Tests derive the same key at runtime; executable test source has no `1.18e-38` / `2.225e-308` literals. The fixture stores the *measured* float64 value, which is the recorded output, not a copied floor definition.

Two warnings remain on the evidence-I/O boundary (silent write-failure swallow, and a `..`-path hole in the `simulation_data/` mkdir guard). Neither falsifies the six-row measurement.

## Warnings

### WR-01: Evidence-write exceptions are swallowed with a silent exit 1

**File:** `pinn/verification/architecture_characterization_probe.py:871-874`
**Issue:** After the measurement `try`/`except`, `main` wraps `_write_evidence` in a bare `except Exception: return 1`. Dataset-root rejection, permission errors, disk-full, and JSON serialization failures all become a silent non-zero exit: no stderr, no traceback, no printed summary. The sibling analog `residual_probe.main` lets write errors propagate. This also means a completed six-case sweep whose evidence write fails is indistinguishable from a measurement exception, and the `simulation_data/` guard (T-55-06) fails closed without telling the operator why. 55-02 required structured failure evidence for measurement errors, not a mute I/O path.
**Fix:** Surface the write error and keep the non-verdict exit contract:

```python
    try:
        run_dir = _write_evidence(raw, args.evidence_root)
    except Exception as exc:
        print(
            f"failed to write evidence: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1
```

Alternatively omit the inner `try` and let the exception propagate, matching `residual_probe.py`.

### WR-02: Dataset-root guard canonicalizes for the check, then mkdir uses the unresolved path

**File:** `pinn/verification/architecture_characterization_probe.py:604-626`
**Issue:** `_reject_dataset_evidence_root` tests `evidence_root.resolve().relative_to(dataset_root)`, but `_new_run_dir` then calls `candidate.mkdir(parents=True, exist_ok=False)` on the *unresolved* `evidence_root / name`. `Path.mkdir(parents=True)` creates each path component, including intermediates that `..` later walks out of. A probe against this exact pattern created `simulation_data/nested/` while the resolved target sat outside the dataset tree:

```text
evidence_root = simulation_data/nested/../../outside/evidence
resolve() -> outside/evidence          # guard allows
mkdir(parents=True) -> also creates simulation_data/nested/
```

T-55-06 claimed the resolve-and-refuse guard prevents any directory under `simulation_data/` before `_new_run_dir` creates anything. `test_evidence_root_inside_simulation_data_is_rejected` only covers a path that *resolves* inside the dataset, so this hole is untested. Harm is empty-directory creation rather than overwrite of corpus files, which is why this is a Warning rather than Critical — but it is a real bypass of the stated dataset-write prohibition.
**Fix:** Canonicalize once, then allocate:

```python
def _new_run_dir(evidence_root: Path) -> Path:
    evidence_root = Path(evidence_root).resolve()
    _reject_dataset_evidence_root(evidence_root)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for suffix in range(1000):
        name = run_id if suffix == 0 else f"{run_id}-{suffix:03d}"
        candidate = evidence_root / name
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise FileExistsError(
        f"could not allocate exclusive evidence directory under {evidence_root}"
    )
```

Add a regression test whose `--evidence-root` is `simulation_data/<seg>/../../<tmp>` and assert `simulation_data/<seg>` is not created.

## Info

### IN-01: `_PRE_IMPORT_FALLBACK` is captured and never recorded

**File:** `pinn/verification/architecture_characterization_probe.py:44`
**Issue:** The module copies `residual_probe.py`'s pre-Torch capture of `PYTORCH_ENABLE_MPS_FALLBACK`, but unlike `residual_probe`, `gradcheck_probe`, `overfit_probe`, and `componentwise_ad`, it never writes `pre_import_fallback` into provenance. The name is dead. Harmless on the default float64/CPU path; it is leftover analog copy-paste.
**Fix:** Either add `"pre_import_fallback": _PRE_IMPORT_FALLBACK` to `_provenance`, or delete the capture if Phase 55 provenance is intentionally CPU-only.

### IN-02: Argparse advertises precision/device pairs `resolve_runtime` rejects

**File:** `pinn/verification/architecture_characterization_probe.py:823-832`
**Issue:** `--precision` choices are `float32|float64` and `--device` choices are `mps|cpu`, independently. `pinn.runtime.resolve_runtime` accepts only `("float32", "mps")` and `("float64", "cpu")`. A plausible invocation `--precision float32` (default device `cpu`) therefore passes argparse, fails inside `main`'s measurement `try`, and is recorded as a generic incomplete measurement rather than a usage error. Fail-closed is correct; the CLI contract is just wider than the runtime contract.
**Fix:** Validate the pair in `_parse_args` (or restrict choices so the defaults remain the only zero-argument pair and the cross pairs error via `parser.error` before any sweep).

---

_Reviewed: 2026-09-06T04:22:04Z_
_Reviewer: Grok (gsd-code-reviewer)_
_Depth: deep_
