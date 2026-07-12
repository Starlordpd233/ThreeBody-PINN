"""Phase 37 / ENV-03 — shared componentwise-AD worker (§10.3 fixture).

This module is the one scientific kernel both D1-p profiles (fp32-MPS and
fp64-CPU) execute unchanged. It preserves the authoritative ``pinn_architecture.md``
§10.3 contract and the legacy v1.4 Phase 21 ``probe_ad.py`` fixture semantics:

    * scalar leaf ``u in [0, 1]`` (locked at ``u = 0.3``)
    * trajectory ``r'(u) = [sin(2*pi*u), cos(2*pi*u), u**2]``
    * analytical first derivative ``[2*pi*cos(2*pi*u), -2*pi*sin(2*pi*u), 2*u]``
    * componentwise loop (per-component derivative, not a summed-output VJP)
    * aggregate criterion ``relative_error < 1e-6``

It extends the fixture with two AD patterns sharing the same trajectory:

    * ``full_jacobian``  — ``torch.func.jacrev`` over the scalar leaf
    * ``scalar_u_jvp``   — scalar unit tangent ``torch.func.jvp`` (forward mode)

and a fixed timing protocol (10 warmups, 30 samples, 100 evaluations per
sample, normalized per evaluation; MPS synchronized immediately before and
after each measured sample). The module is import-safe as a library and also
runnable as a JSON child worker via ``python -m pinn.verification.componentwise_ad``.

CTX-08 contract: the worker captures ``PYTORCH_ENABLE_MPS_FALLBACK`` BEFORE
importing Torch or ``pinn.runtime``. The orchestrator parent removes the
fallback key from the MPS child's environment before spawn; the worker records
whether the key was absent (correct) or present (fallback leakage — invalid
evidence).
"""

# CRITICAL ORDERING: read the fallback key from the environment BEFORE any
# Torch import. Torch reads PYTORCH_ENABLE_MPS_FALLBACK at import time; once
# Torch is loaded the pre-import value is no longer recoverable from os.environ
# reliably (the parent may have already scrubbed it). Capture it here, at the
# top of the module, with only stdlib imported.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK")
# Normalize: absent -> None; empty string -> None (treat as unset); any other
# value is the leaked fallback state.
if _PRE_IMPORT_FALLBACK is not None and _PRE_IMPORT_FALLBACK == "":
    _PRE_IMPORT_FALLBACK = None

# NOW it is safe to import Torch and the runtime resolver.
import argparse as _argparse
import json as _json
import math as _math
import sys as _sys
import time as _time
from dataclasses import dataclass as _dataclass

import torch as _torch

# Local import after fallback capture + Torch availability. ``pinn.runtime`` is
# the single explicit precision/device seam (no global default, no fallback).
from pinn.runtime import resolve_runtime as _resolve_runtime


# ---------------------------------------------------------------------------
# §10.3 fixture — the locked synthetic trajectory and its analytical derivative.
# ---------------------------------------------------------------------------

def synthetic_trajectory(u):
    """r'(u) = [sin(2*pi*u), cos(2*pi*u), u**2].

    ``u`` is a scalar Torch tensor (the autograd leaf). Returns a 3-vector.
    Both AD patterns share this one trajectory.

    Implementation note: the constants are wrapped as same-dtype/device tensors
    because the dual-number tangent representation inside ``torch.func.jvp``
    on MPS does not support Python-float × dual-tensor in either operand
    ordering. Tensor × tensor is correct on both CPU and MPS.
    """
    two_pi = _torch.as_tensor(2 * _math.pi, dtype=u.dtype, device=u.device)
    two = _torch.as_tensor(2.0, dtype=u.dtype, device=u.device)
    two_pi_u = u * two_pi
    return _torch.stack([_torch.sin(two_pi_u), _torch.cos(two_pi_u), u * u])


def analytical_first_derivative(u):
    """Analytical dr'/du = [2*pi*cos(2*pi*u), -2*pi*sin(2*pi*u), 2*u]."""
    two_pi = _torch.as_tensor(2 * _math.pi, dtype=u.dtype, device=u.device)
    neg_two_pi = _torch.as_tensor(-2 * _math.pi, dtype=u.dtype, device=u.device)
    two = _torch.as_tensor(2.0, dtype=u.dtype, device=u.device)
    two_pi_u = u * two_pi
    return _torch.stack([
        _torch.cos(two_pi_u) * two_pi,
        _torch.sin(two_pi_u) * neg_two_pi,
        u * two,
    ])


# ---------------------------------------------------------------------------
# Timing protocol — locked counts. The 10/30/100 workload is the research-
# derived deterministic protocol; do not invent a performance threshold.
# ---------------------------------------------------------------------------

@_dataclass(frozen=True)
class TimingProtocol:
    """Fixed measurement protocol (CTX-09).

    warmup_iterations: untimed warmup calls before sampling (deterministic).
    sample_count: number of raw timing samples.
    evaluations_per_sample: identical derivative evaluations per sample; each
        sample's elapsed time is normalized (divided) by this count.
    """

    warmup_iterations: int = 10
    sample_count: int = 30
    evaluations_per_sample: int = 100


# Aggregate correctness criterion (CTX-09).
AGGREGATE_CRITERION = 1e-6

# The two AD pattern IDs (CTX-09).
PATTERN_FULL_JACOBIAN = "full_jacobian"
PATTERN_SCALAR_U_JVP = "scalar_u_jvp"
_PATTERN_IDS = (PATTERN_FULL_JACOBIAN, PATTERN_SCALAR_U_JVP)


def _scalar_unit_tangent(u, requires_grad=False):
    """Construct a scalar leaf tensor for ``u`` on the resolved runtime."""
    if not _torch.is_tensor(u):
        u = _torch.tensor(float(u))
    return u.detach().clone().requires_grad_(True)


def _full_jacobian(u_scalar, dtype, device):
    """Full Jacobian of the 3-vector trajectory w.r.t. the scalar leaf.

    Uses ``torch.func.jacrev``. For a scalar input the Jacobian is the
    componentwise derivative vector.
    """
    def f(leaf):
        return synthetic_trajectory(leaf)

    u_leaf = _torch.tensor(float(u_scalar), dtype=dtype, device=device,
                           requires_grad=True)
    jac = _torch.func.jacrev(f)(u_leaf)
    return jac


def _scalar_u_jvp(u_scalar, dtype, device):
    """Scalar-unit-tangent forward-mode derivative via ``torch.func.jvp``.

    The tangent is a scalar unit (1.0) on the leaf ``u``; the primal is the
    trajectory; the JVP returns (primal, tangent) where tangent is the
    directional derivative = componentwise derivative for a scalar unit tangent.
    """
    def f(leaf):
        return synthetic_trajectory(leaf)

    u_leaf = _torch.tensor(float(u_scalar), dtype=dtype, device=device,
                           requires_grad=True)
    primal, tangent = _torch.func.jvp(
        f, (u_leaf,), (_torch.tensor(1.0, dtype=dtype, device=device),))
    return tangent


_PATTERN_IMPLEMENTATIONS = {
    PATTERN_FULL_JACOBIAN: _full_jacobian,
    PATTERN_SCALAR_U_JVP: _scalar_u_jvp,
}


def compute_derivative(pattern, u, precision, device):
    """Compute the componentwise derivative at scalar ``u`` for one AD pattern.

    Returns a dict carrying the predicted and analytical vectors, the
    componentwise signed/absolute/relative errors, the aggregate norm-relative
    error, finite/vector checks, and the strict criterion pass/fail. Raises on
    non-finite components (the caller treats that as invalid evidence).

    Args:
        pattern: ``"full_jacobian"`` or ``"scalar_u_jvp"``.
        u: scalar leaf value (the §10.3 fixture locks ``u = 0.3``).
        precision: ``"float32"`` or ``"float64"``.
        device: ``"mps"`` or ``"cpu"``.

    Returns:
        dict with keys: ``pattern``, ``u``, ``precision``, ``device``,
        ``predicted``, ``analytical``, ``signed_delta``, ``absolute_error``,
        ``relative_error``, ``aggregate_relative_error``, ``criterion``,
        ``finite``, ``passed``.
    """
    if pattern not in _PATTERN_IMPLEMENTATIONS:
        raise ValueError(f"unknown AD pattern {pattern!r}; expected {_PATTERN_IDS}")
    spec = _resolve_runtime(precision, device)  # raises on unsupported pair
    if not _torch.is_tensor(u):
        u_val = float(u)
    else:
        u_val = float(u.item())
    if not _math.isfinite(u_val):
        raise ValueError(f"non-finite scalar leaf u={u_val!r}; refusing to produce evidence")
    impl = _PATTERN_IMPLEMENTATIONS[pattern]
    predicted = impl(u_val, spec.dtype, spec.torch_device)
    analytical = analytical_first_derivative(
        _torch.tensor(u_val, dtype=spec.dtype, device=spec.torch_device)
    )
    # Flatten to 1-D CPU float64 lists for JSON evidence + signed/relative math.
    pred_list = [float(x) for x in predicted.detach().to("cpu").to(_torch.float64).flatten()]
    anal_list = [float(x) for x in analytical.detach().to("cpu").to(_torch.float64).flatten()]
    if len(pred_list) != 3 or len(anal_list) != 3:
        raise ValueError(f"trajectory must be 3-component; got pred={len(pred_list)}, anal={len(anal_list)}")
    if not all(_math.isfinite(x) for x in pred_list):
        raise ValueError(f"non-finite predicted component; refusing to produce evidence")
    signed_delta = [p - a for p, a in zip(pred_list, anal_list)]
    absolute_error = [abs(d) for d in signed_delta]
    relative_error = [abs(d) / max(abs(a), 1e-30) for d, a in zip(signed_delta, anal_list)]
    # Aggregate norm-relative error (matches the legacy probe_ad.py form).
    import math
    num = math.sqrt(sum(d * d for d in signed_delta))
    den = math.sqrt(sum(a * a for a in anal_list))
    aggregate = num / max(den, 1e-30)
    return {
        "pattern": pattern,
        "u": u_val,
        "precision": precision,
        "device": device,
        "predicted": pred_list,
        "analytical": anal_list,
        "signed_delta": signed_delta,
        "absolute_error": absolute_error,
        "relative_error": relative_error,
        "aggregate_relative_error": aggregate,
        "criterion": AGGREGATE_CRITERION,
        "finite": all(_math.isfinite(x) for x in pred_list + anal_list),
        "passed": aggregate < AGGREGATE_CRITERION,
    }


def _time_pattern(pattern, u_val, spec, protocol):
    """Time one AD pattern under the fixed protocol.

    Returns a dict with raw samples (ns, per-evaluation-normalized) and the
    six summary statistics (median, p25, p75, min, max, plus mean for context).
    MPS is synchronized immediately before and after each measured sample.
    """
    impl = _PATTERN_IMPLEMENTATIONS[pattern]
    # Warmup (untimed).
    for _ in range(protocol.warmup_iterations):
        impl(u_val, spec.dtype, spec.torch_device)
    _sync(spec)
    raw_samples_ns = []
    for _ in range(protocol.sample_count):
        _sync(spec)  # immediately before the measured block
        t0 = _time.perf_counter_ns()
        for _ in range(protocol.evaluations_per_sample):
            impl(u_val, spec.dtype, spec.torch_device)
        _sync(spec)  # immediately after the measured block
        t1 = _time.perf_counter_ns()
        # Normalize per evaluation.
        raw_samples_ns.append((t1 - t0) / protocol.evaluations_per_sample)
    stats = _summary_stats(raw_samples_ns)
    return {
        "raw_samples_ns": raw_samples_ns,
        "median": stats["median"],
        "p25": stats["p25"],
        "p75": stats["p75"],
        "min": stats["min"],
        "max": stats["max"],
        "mean": stats["mean"],
    }


def _sync(spec):
    """Synchronize the resolved device so timing reflects completed work."""
    if spec.torch_device.type == "mps":
        _torch.mps.synchronize()
    # CPU is synchronous already.


def _summary_stats(samples):
    """median / p25 / p75 / min / max / mean of a numeric sample list."""
    import statistics
    s = sorted(samples)
    n = len(s)
    if n == 0:
        return {"median": None, "p25": None, "p75": None, "min": None, "max": None, "mean": None}

    def _percentile(p):
        # Linear interpolation between closest ranks.
        if n == 1:
            return float(s[0])
        k = (n - 1) * p
        f = int(_math.floor(k))
        c = int(_math.ceil(k))
        if f == c:
            return float(s[f])
        return float(s[f] + (s[c] - s[f]) * (k - f))

    return {
        "median": statistics.median(samples),
        "p25": _percentile(0.25),
        "p75": _percentile(0.75),
        "min": float(min(samples)),
        "max": float(max(samples)),
        "mean": statistics.mean(samples),
    }


def run_probe_arm(precision, device, patterns=_PATTERN_IDS,
                  protocol=None, u=0.3):
    """Run one D1-p profile arm: both AD patterns' correctness + timing.

    Returns a single JSON-serializable dict carrying requested/resolved/actual
    device facts, the pre-import fallback fact, Torch build/configuration,
    protocol metadata, both pattern records (correctness + timing), and any
    structured exception (or null). Failed evidence never triggers a CPU retry,
    a tolerance change, a second-order residual, or a D1-p default.

    Args:
        precision: ``"float32"`` or ``"float64"``.
        device: ``"mps"`` or ``"cpu"``.
        patterns: ordered tuple of pattern IDs to run (default both).
        protocol: TimingProtocol instance (default TimingProtocol()).
        u: scalar leaf (default 0.3, the §10.3 fixture).

    Returns:
        dict with keys: ``profile``, ``precision``, ``requested_device``,
        ``resolved_device``, ``actual_device``, ``pre_import_fallback``,
        ``torch_build``, ``protocol``, ``u``, ``patterns``, ``exception``.
    """
    if protocol is None:
        protocol = TimingProtocol()
    exception = None
    pattern_records = {}
    spec = None
    try:
        spec = _resolve_runtime(precision, device)
        # Record the ACTUAL device after a no-op tensor allocation so a silent
        # CPU fallback (actual != requested) is observable.
        probe = _torch.tensor(0.0, dtype=spec.dtype, device=spec.torch_device)
        actual_device = probe.device.type
        for pattern in patterns:
            correctness = compute_derivative(pattern, u, precision, device)
            timing = _time_pattern(pattern, float(u), spec, protocol)
            pattern_records[pattern] = {**correctness, **timing}
    except Exception as exc:  # noqa: BLE001 — structured failure retention
        exception = {"type": type(exc).__name__, "message": str(exc)}
    return {
        "profile": f"{precision}-{device}",
        "precision": precision,
        "requested_device": device,
        "resolved_device": spec.torch_device.type if spec else None,
        "actual_device": actual_device if (exception is None and spec is not None) else None,
        "pre_import_fallback": _PRE_IMPORT_FALLBACK,
        "torch_build": {
            "version": _torch.__version__,
            "git_version": getattr(_torch.version, "git_version", None),
            "is_debug": bool(getattr(_torch.version, "is_debug", False)) if hasattr(_torch.version, "is_debug") else False,
            "mps_is_built": bool(_torch.backends.mps.is_built()),
        },
        "protocol": {
            "warmup_iterations": protocol.warmup_iterations,
            "sample_count": protocol.sample_count,
            "evaluations_per_sample": protocol.evaluations_per_sample,
        },
        "u": float(u),
        "patterns": pattern_records,
        "exception": exception,
    }


# ---------------------------------------------------------------------------
# JSON child-worker entry point. The orchestrator parent (Wave 3) invokes this
# module twice with fixed argv — once per profile — and reads exactly one JSON
# object from stdout.
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = _argparse.ArgumentParser(
        prog="python -m pinn.verification.componentwise_ad",
        description="Phase 37 componentwise-AD child worker (one JSON object on stdout).",
    )
    parser.add_argument("--precision", required=True, choices=("float32", "float64"))
    parser.add_argument("--device", required=True, choices=("mps", "cpu"))
    parser.add_argument("--warmup", type=int, default=TimingProtocol.warmup_iterations)
    parser.add_argument("--samples", type=int, default=TimingProtocol.sample_count)
    parser.add_argument("--evaluations", type=int, default=TimingProtocol.evaluations_per_sample)
    parser.add_argument("--u", type=float, default=0.3)
    args = parser.parse_args(argv)
    # Validate positive counts; reject non-positive CLI overrides.
    if args.warmup <= 0 or args.samples <= 0 or args.evaluations <= 0:
        print(_json.dumps({"error": "warmup/samples/evaluations must be positive"}))
        _sys.exit(2)
    protocol = TimingProtocol(warmup_iterations=args.warmup,
                              sample_count=args.samples,
                              evaluations_per_sample=args.evaluations)
    record = run_probe_arm(args.precision, args.device, protocol=protocol, u=args.u)
    _sys.stdout.write(_json.dumps(record, sort_keys=True))
    _sys.stdout.write("\n")
    _sys.stdout.flush()
    return 0


if __name__ == "__main__":
    _sys.exit(main())
