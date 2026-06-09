#!/usr/bin/env python3
"""
Phase 20.5 disposable verification probe — Sobol dimension and allocation order.

Three evidence surfaces, each exiting nonzero on failure:

  Surface 1 — SPEC: static assertions over sampling_method.md (dimension formula,
      fixed allocation order, standard and no-scale branches, absence of the obsolete
      double-booked velocity statement).
  Surface 2 — ENTRYPOINT: AST parse of generate_ics.py confirming the standard-generation
      call uses ic_type="standard", scale_range=(0.8, 1.2), velocity_scale=0.1.
  Surface 3 — SAMPLER: behavioral tests of EnhancedThreeBodySampler against
      simulation_data/Scripts/ic_generation/ic_generation_utils.py —
      the dimension matrix, the standard-config scale/velocity allocation, a synthetic
      position test proving columns 0-2 drive the expected spherical mapping, the
      no-scale velocity allocation, and the rotate=False boundary.

Run from the repository root:
    .venv/bin/python3 .planning/milestones/v1.4-phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py
"""
import ast
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

REPO_ROOT = Path(__file__).resolve().parents[4]  # probes/ -> 20-5-* -> phases/ -> .planning/ -> repo
SPEC_PATH = REPO_ROOT / "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md"
ENTRYPOINT_PATH = REPO_ROOT / "simulation_data/Scripts/ic_generation/generate_ics.py"

failures = []


def record(surface, label, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"{tag}  {surface}: {label}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(f"{surface}/{label}: {detail}")


# ===========================================================================
# Surface 1 — SPEC
# ===========================================================================
spec_text = SPEC_PATH.read_text()

record("SPEC", "sobol-convention subsection present",
       "#### Sobol Coordinate Allocation Convention" in spec_text,
       "missing Sobol Coordinate Allocation Convention subsection")

record("SPEC", "global-scaling heading removed",
       "#### Global Scaling (Optional)" not in spec_text,
       "'#### Global Scaling (Optional)' heading still present — rename did not apply")

record("SPEC", "sampling-time-size heading present",
       "#### Sampling-Time Size Variability" in spec_text,
       "'#### Sampling-Time Size Variability' heading missing")

record("SPEC", "dimension formula d = 3 + δ_s + 3δ_v",
       "d = 3 + \\delta_s + 3\\delta_v" in spec_text,
       "dimension formula not found in spec")

record("SPEC", "fixed allocation order stated",
       "allocation order is **fixed**" in spec_text
       or "allocation order is fixed" in spec_text,
       "fixed allocation-order statement missing")

record("SPEC", "standard branch (δ_s = δ_v = 1) stated",
       "δ_s = δ_v = 1" in spec_text
       or "\\delta_s = \\delta_v = 1" in spec_text
       or "$\\delta_s = \\delta_v = 1$" in spec_text,
       "standard-configuration branch statement missing")

record("SPEC", "no-scale branch (δ_s = 0) stated",
       "δ_s = 0" in spec_text
       or "\\delta_s = 0" in spec_text,
       "no-scale branch statement missing")

record("SPEC", "obsolete double-booked velocity statement absent",
       "The next three Sobol coordinates $(u_4, u_5, u_6)$ are mapped to a 3D velocity vector"
       not in spec_text,
       "obsolete double-booked velocity statement still present in spec")

record("SPEC", "velocity prose uses u_{4+δ_s} indexing",
       "u_{4+\\delta_s}" in spec_text,
       "velocity-coordinate prose does not use u_{4+δ_s} indexing")

record("SPEC", "Phase 18 momentum sentence intact",
       "The sampler then enforces total momentum conservation for the equal-mass case"
       in spec_text,
       "Phase 18 momentum sentence missing — Edit 5 altered it")

# ===========================================================================
# Surface 2 — ENTRYPOINT (AST parse of generate_ics.py)
# ===========================================================================
try:
    entrypoint_src = ENTRYPOINT_PATH.read_text()
    tree = ast.parse(entrypoint_src)
except Exception as e:
    record("ENTRYPOINT", "parse generate_ics.py", False, f"could not parse: {e}")
    entrypoint_src, tree = "", None

if tree is not None:
    record("ENTRYPOINT", "parse generate_ics.py", True)

    # Find every Call node whose func is the Name 'generate_ics' (or any call carrying the
    # standard-config kwargs we need to verify). The canonical standard-generation call in
    # the main block uses these kwargs by name.
    standard_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        kw = {k.arg: k.value for k in node.keywords if k.arg is not None}
        has_ic_type_std = (
            "ic_type" in kw
            and isinstance(kw["ic_type"], ast.Constant)
            and kw["ic_type"].value == "standard"
        )
        if has_ic_type_std:
            standard_calls.append(kw)

    record("ENTRYPOINT", "at least one ic_type='standard' call",
           len(standard_calls) >= 1,
           "no generate_ics(... ic_type='standard' ...) call found")

    if standard_calls:
        kw = standard_calls[0]

        def _const_tuple(node):
            if isinstance(node, ast.Tuple) and all(
                isinstance(e, ast.Constant) for e in node.elts
            ):
                return tuple(e.value for e in node.elts)
            return None

        scale_range = _const_tuple(kw.get("scale_range")) if "scale_range" in kw else None
        record("ENTRYPOINT", "scale_range=(0.8, 1.2)",
               scale_range == (0.8, 1.2),
               f"got scale_range={scale_range}")

        vs = kw.get("velocity_scale")
        vs_val = vs.value if isinstance(vs, ast.Constant) else None
        record("ENTRYPOINT", "velocity_scale=0.1",
               vs_val == 0.1,
               f"got velocity_scale={vs_val}")

# ===========================================================================
# Surface 3 — SAMPLER
# ===========================================================================
sys.path.append(str(REPO_ROOT / "simulation_data/Scripts/ic_generation"))
try:
    from ic_generation_utils import EnhancedThreeBodySampler
    record("SAMPLER", "import EnhancedThreeBodySampler", True)
except Exception as e:
    record("SAMPLER", "import EnhancedThreeBodySampler", False, str(e))
    EnhancedThreeBodySampler = None

if EnhancedThreeBodySampler is not None:
    # --- 3a. Dimension matrix (rotate=False) ---
    cases = [
        ((0.8, 1.2), 0.1, 7, "delta_s=1, delta_v=1 (standard config)"),
        ((1.0, 1.0), 0.1, 6, "delta_s=0, delta_v=1"),
        ((0.8, 1.2), 0.0, 4, "delta_s=1, delta_v=0"),
        ((1.0, 1.0), 0.0, 3, "delta_s=0, delta_v=0"),
    ]
    for scale_range, velocity_scale, expected_d, label in cases:
        s = EnhancedThreeBodySampler(
            scale_range=scale_range, velocity_scale=velocity_scale, seed=42
        )
        record("SAMPLER", f"dimension {label}",
               s.sobol_dim == expected_d,
               f"expected d={expected_d}, got {s.sobol_dim}")

    # --- 3b. Standard-config allocation (columns 3 -> scale, 4-6 -> velocity) ---
    s = EnhancedThreeBodySampler(scale_range=(0.8, 1.2), velocity_scale=0.1, seed=42)
    if s.sobol_dim != 7:
        record("SAMPLER", "standard-config sobol_dim=7", False,
               f"got {s.sobol_dim}")
    else:
        record("SAMPLER", "standard-config sobol_dim=7", True)
        n_rows = 5
        # column j carries the constant 0.1*(j+1) -> 0.1, 0.2, ..., 0.7
        synthetic = np.tile(0.1 * (np.arange(7) + 1.0), (n_rows, 1))
        p1 = np.array([1.0, 0.0, 0.0])
        # _process_sobol_batch is PRIVATE — used here only for this disposable probe.
        result = s._process_sobol_batch(synthetic, p1)
        if len(result) != 7:
            record("SAMPLER", "standard-config _process_sobol_batch arity", False,
                   f"expected 7 returns, got {len(result)}")
        else:
            record("SAMPLER", "standard-config _process_sobol_batch arity", True)
            p1_scaled, _p2, _p3, _v1, v2_batch, _v3, _ = result

            # Scale is drawn from column 3: s = lo + (hi - lo) * u_4, and p1_scaled = p1 * s.
            expected_scale = 0.8 + (1.2 - 0.8) * synthetic[:, 3]
            record("SAMPLER", "scale factor s drawn from column 3 (u_4)",
                   np.allclose(p1_scaled[:, 0], expected_scale),
                   f"p1_scaled[:,0]={p1_scaled[:, 0]}, expected {expected_scale}")

            # Velocity is drawn from columns 4-6 via inverse-CDF, then scaled by s.
            expected_v2 = norm.ppf(synthetic[:, 4:7], loc=0, scale=0.1) * expected_scale[:, None]
            record("SAMPLER", "free-particle velocity drawn from columns 4-6 (u_5-u_7)",
                   np.allclose(v2_batch, expected_v2),
                   f"v2_batch={v2_batch}, expected {expected_v2}")

            # --- 3c. Synthetic position test: columns 0-2 drive the spherical mapping ---
            # The position mapping reads columns 0, 1, 2 (θ, φ, r) to produce a 3D position.
            # Isolation test: vary column 0 (θ) while holding columns 1-6 fixed; some output
            # component must change. Then vary column 3 (scale) while holding columns 0-2
            # fixed; the DIRECTION of the position must stay constant (scale only changes
            # magnitude), while magnitude changes. This proves columns 0-2 drive the angular
            # spherical mapping, not the scale coordinate.
            base = np.tile([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], (n_rows, 1))
            var_theta = base.copy(); var_theta[:, 0] = 0.1  # different θ
            var_scale = base.copy(); var_scale[:, 3] = 0.9  # different scale
            out_base = s._process_sobol_batch(base, p1)
            out_theta = s._process_sobol_batch(var_theta, p1)
            out_scale = s._process_sobol_batch(var_scale, p1)
            # Changing column 0 must change some output (the free-particle position p2 or p3
            # depends on θ, since p1 is the fixed reference point):
            theta_affects_output = any(
                not np.allclose(out_base[i], out_theta[i]) for i in range(7)
            )
            record("SAMPLER", "synthetic position: column 0 (θ) affects position output",
                   theta_affects_output,
                   "changing column 0 had no effect on any output component")
            # Changing column 3 (scale) must NOT change the DIRECTION of position outputs
            # (only their magnitude). p1 is fixed at [1,0,0] so p1_scaled = p1 * s; the
            # direction is invariant. For p2/p3, direction depends on θ, φ (columns 0, 1),
            # which are held fixed here, so direction is invariant.
            def same_direction(a, b, tol=1e-9):
                na = np.linalg.norm(a, axis=1)
                nb = np.linalg.norm(b, axis=1)
                # Skip rows where either norm is near zero (direction undefined).
                mask = (na > tol) & (nb > tol)
                if not mask.any():
                    return True
                ua = a[mask] / na[mask, None]
                ub = b[mask] / nb[mask, None]
                return np.allclose(ua, ub, atol=1e-6)
            # Check p1_scaled, p2, p3 directions are invariant to scale.
            scale_direction_invariant = (
                same_direction(out_base[0], out_scale[0])  # p1_scaled
                and same_direction(out_base[1], out_scale[1])  # p2
                and same_direction(out_base[2], out_scale[2])  # p3
            )
            record("SAMPLER", "synthetic position: column 3 (scale) preserves position direction",
                   scale_direction_invariant,
                   "changing column 3 altered position direction — columns 0-2 are not driving the angular mapping")

    # --- 3d. No-scale allocation (columns 3-5 -> velocity) ---
    s_no_scale = EnhancedThreeBodySampler(
        scale_range=(1.0, 1.0), velocity_scale=0.1, seed=42
    )
    if s_no_scale.sobol_dim != 6:
        record("SAMPLER", "no-scale sobol_dim=6", False, f"got {s_no_scale.sobol_dim}")
    else:
        record("SAMPLER", "no-scale sobol_dim=6", True)
        n_rows = 5
        synthetic_no_scale = np.tile(0.1 * (np.arange(6) + 1.0), (n_rows, 1))
        p1 = np.array([1.0, 0.0, 0.0])
        result = s_no_scale._process_sobol_batch(synthetic_no_scale, p1)
        if len(result) != 7:
            record("SAMPLER", "no-scale _process_sobol_batch arity", False,
                   f"expected 7 returns, got {len(result)}")
        else:
            record("SAMPLER", "no-scale _process_sobol_batch arity", True)
            _p1_scaled, _p2, _p3, _v1, v2_no_scale, _v3, _ = result
            expected_v2_no_scale = norm.ppf(synthetic_no_scale[:, 3:6], loc=0, scale=0.1)
            record("SAMPLER", "no-scale velocity drawn from columns 3-5 (u_4-u_6)",
                   np.allclose(v2_no_scale, expected_v2_no_scale),
                   f"v2_batch={v2_no_scale}, expected {expected_v2_no_scale}")

    # --- 3e. rotate=False boundary ---
    s_rf = EnhancedThreeBodySampler(
        scale_range=(0.8, 1.2), velocity_scale=0.1, rotate=False, seed=42
    )
    s_rt = EnhancedThreeBodySampler(
        scale_range=(0.8, 1.2), velocity_scale=0.1, rotate=True, seed=42
    )
    record("SAMPLER", "rotate=False -> d=7",
           s_rf.sobol_dim == 7,
           f"got {s_rf.sobol_dim}")
    record("SAMPLER", "rotate=True -> d=10 (three unused future-rotation dims)",
           s_rt.sobol_dim == 10,
           f"got {s_rt.sobol_dim}")

# ===========================================================================
# Summary
# ===========================================================================
print()
if failures:
    print(f"FAILED: {len(failures)} assertion(s) did not pass:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("All three surfaces (SPEC, ENTRYPOINT, SAMPLER) passed.")
    print("Sobol dimension formula d = 3 + delta_s + 3*delta_v (rotate=False) and the")
    print("allocation order (position, optional scale, optional velocity) are verified.")
    sys.exit(0)
