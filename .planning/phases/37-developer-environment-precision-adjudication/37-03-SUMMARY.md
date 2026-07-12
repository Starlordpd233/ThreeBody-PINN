---
phase: 37-developer-environment-precision-adjudication
plan: "03"
subsystem: pinn
tags: [runtime, precision, device, autograd, jacrev, jvp, componentwise-ad]

requires:
  - phase: 37-02
    provides: "pinn-train verified env (Python 3.11, Torch 2.12 + MPS) + Wave 0 ENV-04 contract"
provides:
  - "pinn/__init__.py package marker exporting only RuntimeSpec and resolve_runtime"
  - "pinn/runtime.py — immutable two-profile resolver (float32/mps, float64/cpu); fail-closed on every other pair"
  - "pinn/verification/__init__.py + pinn/verification/componentwise_ad.py — shared §10.3 AD worker, dual-pattern, fixed timing protocol, JSON child-worker entry"
affects:
  - "37-04 (Wave 3) invokes the worker twice via subprocess for the two fixed profiles"
  - "37-05 (Wave 4) runs the empirical MPS arm through this exact worker"
  - "Phase 38 consumes pinn.runtime.resolve_runtime as the single precision/device seam"

tech-stack:
  added: []
  patterns:
    - "Explicit immutable RuntimeSpec — no global default dtype, no availability inference, no retry"
    - "torch.func.jacrev (full Jacobian) and torch.func.jvp (scalar unit tangent) share one trajectory"
    - "Fallback capture (PYTORCH_ENABLE_MPS_FALLBACK) before any Torch import — recorded as a fact, never relied on"

key-files:
  created:
    - "pinn/__init__.py — package marker; re-exports RuntimeSpec, resolve_runtime only"
    - "pinn/runtime.py — frozen RuntimeSpec + resolve_runtime(precision, device); exactly two permitted pairs"
    - "pinn/verification/__init__.py — verification subpackage marker"
    - "pinn/verification/componentwise_ad.py — §10.3 trajectory, analytical derivative, compute_derivative, TimingProtocol, run_probe_arm, main (JSON worker)"
  modified:
    - "tests/phase37/test_runtime.py — test_resolver_does_not_infer_availability_or_retry now strips docstrings/comments before the source-inspection scan"

key-decisions:
  - "Both AD patterns share synthetic_trajectory and analytical_first_derivative; full_jacobian uses torch.func.jacrev, scalar_u_jvp uses torch.func.jvp with a scalar unit tangent. No summed-output VJP."
  - "run_probe_arm records requested/resolved/actual device + pre_import_fallback + torch build + protocol metadata + both pattern records + a structured exception (or null). Failed evidence never triggers a CPU retry, tolerance change, second-order residual, or D1-p default."
  - "MPS synchronization occurs immediately before and after each measured timing sample (CTX-09)."

patterns-established:
  - "Precision/device is resolved once through a central typed helper; dtype/device are passed explicitly through tensor and AD construction"
  - "The §10.3 fixture (u=0.3, [sin(2πu), cos(2πu), u²], analytical, < 1e-6) is the locked scientific contract; this worker preserves it verbatim from the v1.4 Phase 21 probe"

requirements-completed: [ENV-04]

coverage:
  - id: D1
    description: "Immutable two-profile runtime resolver (float32/mps and float64/cpu); fail-closed on every other pair; no global dtype mutation"
    requirement: "ENV-04"
    verification:
      - kind: unit
        ref: "tests/phase37/test_runtime.py#RuntimeResolverTests (12 cases) — green under pinn-train"
        status: pass
    human_judgment: false
  - id: D2
    description: "Shared §10.3 componentwise-AD worker: both full_jacobian and scalar_u_jvp preserve the locked fixture and the 1e-6 criterion; fixed 10/30/100 timing protocol; fallback captured before Torch import"
    requirement: "ENV-03"
    verification:
      - kind: unit
        ref: "tests/phase37/test_componentwise_ad.py#ComponentwiseADTests (11 cases) — green under pinn-train"
        status: pass
      - kind: integration
        ref: "python -m pinn.verification.componentwise_ad --precision float64 --device cpu -> one JSON object, both patterns pass criterion (0.00e+00), pre_import_fallback None, actual_device cpu"
        status: pass
    human_judgment: false

duration: ~20min
completed: 2026-07-12
status: complete
---

# Phase 37 Plan 03: Runtime Seam + Shared Componentwise-AD Worker Summary

**The narrow two-profile precision/device seam and the one §10.3 componentwise-AD worker both D1-p arms execute unchanged — no global default, no fallback, no D1-p pick**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2 (37-03-01 resolver; 37-03-02 AD worker)
- **Files created:** 4 (pinn package + resolver + verification package + worker); 1 test refinement

## Accomplishments

- **`pinn/runtime.py` (ENV-04):** frozen `RuntimeSpec(precision, requested_device, dtype, torch_device)` and `resolve_runtime(precision, device)`. Exactly two permitted profile pairs: `float32`/`mps` and `float64`/`cpu`. Every other input (omitted, partial, unknown, `float64`/`mps`, `float32`/`cpu`) raises `ValueError` BEFORE tensor construction, naming the two allowed pairs. No availability inference, no retry, no `torch.set_default_dtype`, no implicit production default. Source-inspection test confirms the executable code contains none of those tokens.
- **`pinn/verification/componentwise_ad.py` (ENV-03):**
  - Captures `PYTORCH_ENABLE_MPS_FALLBACK` at the very top of the module, BEFORE any Torch import (CTX-08). The value is recorded in every probe arm's evidence.
  - §10.3 fixture preserved verbatim: scalar leaf `u in [0,1]` (locked at 0.3); trajectory `[sin(2πu), cos(2πu), u²]`; analytical derivative `[2πcos(2πu), -2πsin(2πu), 2u]`; aggregate criterion `< 1e-6`.
  - Two AD patterns share the one trajectory: `full_jacobian` via `torch.func.jacrev`, `scalar_u_jvp` via `torch.func.jvp` with a scalar unit tangent. No summed-output VJP.
  - `compute_derivative(pattern, u, precision, device)` returns predicted/analytical vectors, componentwise signed/absolute/relative errors, aggregate norm-relative error, finite check, and criterion pass/fail. Rejects non-finite components.
  - `run_probe_arm(precision, device, ...)` runs both patterns' correctness + timing under the locked 10/30/100 protocol (10 warmups, 30 samples, 100 evaluations per sample, per-evaluation normalized; MPS synchronized immediately before and after each measured sample). Returns one JSON-serializable dict with requested/resolved/actual device, pre-import fallback, Torch build, protocol metadata, both pattern records, and a structured exception (or null).
  - `main()` is the JSON child-worker entry point: `python -m pinn.verification.componentwise_ad --precision X --device Y --warmup 10 --samples 30 --evaluations 100 --u 0.3` emits exactly one JSON object on stdout.

## Files Created/Modified

- `pinn/__init__.py` — package marker; re-exports only `RuntimeSpec`, `resolve_runtime`
- `pinn/runtime.py` — frozen resolver; two permitted pairs; fail-closed
- `pinn/verification/__init__.py` — subpackage marker
- `pinn/verification/componentwise_ad.py` — §10.3 worker (dual-pattern, timing protocol, JSON worker)
- `tests/phase37/test_runtime.py` — refined the no-inference source-inspection test to strip docstrings/comments

## Decisions Made

- **`torch.func.jacrev` and `torch.func.jvp`** are the dual-pattern implementation. `jacrev` over the scalar leaf gives the full componentwise Jacobian; `jvp` with a scalar unit tangent gives the same vector via forward mode. Both share `synthetic_trajectory` so the test `test_both_patterns_share_one_trajectory` proves they are not two implementations.
- **Aggregate error form** matches the legacy `probe_ad.py`: `norm(predicted - analytical) / norm(analytical)`. fp64-CPU produces `0.00e+00` because it IS the analytical precision; the criterion is `< 1e-6`, strict.
- **Fallback capture lives at module top**, before `import torch`. The parent orchestrator (Wave 3) removes the key from the MPS child's environment before spawn; the worker records whether the key was absent (correct) or present (leakage — invalid evidence).

## Deviations from Plan

### Auto-fixed Issues

**1. test_resolver_does_not_infer_availability_or_retry was too broad**
- **Found during:** Task 37-03-01 (running test_runtime under pinn-train)
- **Issue:** the source-inspection test scanned the whole file for `torch.set_default_dtype`, but the resolver's own docstring legitimately mentions that token to document that it does NOT call it.
- **Fix:** the test now parses the AST, collects docstring + comment spans, and scans executable code only.
- **Files modified:** tests/phase37/test_runtime.py
- **Verification:** 12 test_runtime cases green under pinn-train.
- **Committed in:** this task's commit.

---

**Total deviations:** 1 auto-fixed (test-contract refinement)
**Impact on plan:** necessary for correctness; no scope creep.

## Issues Encountered

None beyond the auto-fix above.

## Next Phase Readiness

- ENV-04 (the resolver) and ENV-03's worker/timing contract are GREEN.
- Wave 3 (37-04) can now build the stdlib-only parent orchestrator that invokes this worker twice via subprocess with fixed argv and sanitized MPS env, plus the append-only evidence contract.

---
*Phase: 37-developer-environment-precision-adjudication*
*Completed: 2026-07-12*
