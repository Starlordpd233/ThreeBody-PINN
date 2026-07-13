"""Phase 38 / NET-03 — PHYS-02 componentwise-AD physics-residual test contract.

Wave 3 contract (RED-first). Every production symbol is imported inside the
test methods through a PER-SYMBOL deferred import, so this suite SKIPs cleanly
(never ERRORs) before ``pinn/physics_residual.py`` lands, and turns green at
task 38-03-03.

Grounding (authoritative framework specs only — CTX-17 bans the v1.3-era
``pinn/`` files as a source):

  * ``pinn_architecture.md`` §5.3.1 (PHYS-02): the canonical autograd leaf is
    ``u = t/T``; ``v' = dr'/du`` and ``a' = d^2 r'/du^2`` are taken w.r.t. ``u``
    with NO chain factor (the 2x / 4x factors apply ONLY to a direct
    ``tau = 2u - 1`` leaf). All nine ``dr'_{i,alpha}/du`` are required; the
    summed-output VJP ``torch.autograd.grad(r.sum(), u)`` is FORBIDDEN.
    Worked example: ``r'(u) = [sin(2*pi*u), cos(2*pi*u), u**2]`` with
    ``dr'/du   = [ 2*pi*cos(2*pi*u), -2*pi*sin(2*pi*u), 2*u]``
    ``d2r'/du2 = [-4*pi^2*sin(2*pi*u), -4*pi^2*cos(2*pi*u), 2]``.
  * ``pinn_architecture.md`` §3.2: softened Newtonian force
    ``r_safe = sqrt(||r'_j - r'_i||^2 + eps_train^2)``, ``eps_train = 1e-5``,
    ``F_ij = m_j (r'_j - r'_i) / r_safe^3``, residual ``f_i = a'_i - sum_j F_ij``;
    RAW masses, ``G = 1`` absorbed into ``D``.
  * ``pinn/constants.py`` ``EPS_SOFT`` — the single home of ``eps_soft = 1e-5``.

Batch-dimension contract (38-03 plan, cycle-2 finding #6): the batch axis is
``N_t`` and is the LEADING dimension. ``physics_residual`` takes ``(N_t, 3, 3)``
positions with a ``(N_t,)`` u leaf and returns ``(N_t, 3, 3)``;
``componentwise_du`` maps a ``(N_t,)`` leaf to ``(N_t, 9)`` derivatives.

Edge R3 (planner assumption): gradcheck inputs are kept well above the
softening floor so the fp64 finite-difference check is well conditioned; the
residual is fail-loud on non-finite components rather than emitting evidence.
"""

import importlib
import math
import unittest

RESIDUAL_MODULE = "pinn.physics_residual"
CONSTANTS_MODULE = "pinn.constants"

# fp64-CPU gradcheck tolerances (double precision; documented per the plan).
GRADCHECK_EPS = 1e-6
GRADCHECK_ATOL = 1e-5
GRADCHECK_RTOL = 1e-3

# Symbolic-oracle tolerance for the §5.3.1 worked example under fp64.
SYMBOLIC_TOL = 1e-9


def _load_torch():
    """Import torch; skip cleanly if it is not installed."""
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - environment guard
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


def _require(symbol_name, module_name=RESIDUAL_MODULE):
    """Per-symbol deferred import. SkipTest if the module OR symbol is absent."""
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise unittest.SkipTest(f"{module_name} not implemented yet: {exc}")
    if not hasattr(module, symbol_name):
        raise unittest.SkipTest(f"{module_name}.{symbol_name} not implemented yet")
    return getattr(module, symbol_name)


def _mps_available(torch):
    return bool(torch.backends.mps.is_available())


# ---------------------------------------------------------------------------
# Fixtures — closed-form trajectories with symbolic derivatives (§5.3.1).
# ---------------------------------------------------------------------------

def _worked_example(torch):
    """r'(u) = [sin(2 pi u), cos(2 pi u), u^2] (the §5.3.1 one-body example)."""

    def traj(u):
        two_pi = torch.as_tensor(2 * math.pi, dtype=u.dtype, device=u.device)
        two_pi_u = u * two_pi
        return torch.stack([torch.sin(two_pi_u), torch.cos(two_pi_u), u * u])

    return traj


def _worked_example_symbolic(u):
    """Symbolic (dr'/du, d^2r'/du^2) of the §5.3.1 worked example at scalar u."""
    tp = 2 * math.pi
    first = [tp * math.cos(tp * u), -tp * math.sin(tp * u), 2.0 * u]
    second = [-(tp ** 2) * math.sin(tp * u), -(tp ** 2) * math.cos(tp * u), 2.0]
    return first, second


def _tau_leaf_trajectory(torch):
    """A trajectory whose forward computes ``tau = 2u - 1`` INTERNALLY.

    r'(u) = [sin(tau), tau^2, tau^3] with tau = 2u - 1. Differentiating on the
    u leaf must yield dr'/du = 2 * dr'/dtau AUTOMATICALLY (autograd propagates
    the tau = 2u - 1 relation from inside the forward) — the implementation
    must NOT apply a manual 2x / 4x factor on top of that (§5.3.1).
    """

    def traj(u):
        two = torch.as_tensor(2.0, dtype=u.dtype, device=u.device)
        one = torch.as_tensor(1.0, dtype=u.dtype, device=u.device)
        tau = two * u - one
        return torch.stack([torch.sin(tau), tau * tau, tau * tau * tau])

    return traj


def _tau_leaf_symbolic(u):
    """d/dtau and d2/dtau2 of [sin(tau), tau^2, tau^3] at tau = 2u - 1."""
    tau = 2.0 * u - 1.0
    d_tau = [math.cos(tau), 2.0 * tau, 3.0 * tau ** 2]
    d2_tau = [-math.sin(tau), 2.0, 6.0 * tau]
    return d_tau, d2_tau


def _three_body_positions(torch, dtype, device):
    """A well-separated 3-body geometry (all pairwise gaps >> eps_soft)."""
    return torch.tensor(
        [
            [1.0, 0.0, 0.0],
            [-0.5, 0.8, 0.1],
            [-0.3, -0.9, -0.2],
        ],
        dtype=dtype,
        device=device,
    )


def _reference_softened_acceleration(positions, masses, eps_soft):
    """Pure-Python §3.2 oracle: a_i = sum_{j != i} m_j (r_j - r_i) / r_safe^3."""
    n = len(positions)
    out = []
    for i in range(n):
        acc = [0.0, 0.0, 0.0]
        for j in range(n):
            if i == j:
                continue
            d = [positions[j][k] - positions[i][k] for k in range(3)]
            sq = sum(c * c for c in d)
            r_safe = math.sqrt(sq + eps_soft ** 2)
            factor = masses[j] / (r_safe ** 3)
            for k in range(3):
                acc[k] += factor * d[k]
        out.append(acc)
    return out


def _param_trajectory(torch, theta):
    """Smooth 3-body trajectory r'(u; theta), well above the softening floor.

    Closes over the parameter tensor ``theta`` (3, 3) so the residual is a
    differentiable function of theta — this is the training-relevant gradient
    path (params -> double-AD residual) that gradcheck exercises.
    """
    offsets = torch.tensor(
        [
            [2.0, 0.0, 0.0],
            [-2.0, 0.5, 0.0],
            [0.0, -3.0, 1.5],
        ],
        dtype=theta.dtype,
        device=theta.device,
    )

    def traj(u):
        two_pi = torch.as_tensor(2 * math.pi, dtype=u.dtype, device=u.device)
        w = u * two_pi
        base = torch.stack([
            torch.stack([torch.sin(w), torch.cos(w), u * u]),
            torch.stack([torch.cos(w), torch.sin(w), u]),
            torch.stack([u * u * u, torch.sin(w), torch.cos(w)]),
        ])
        return base * theta + offsets

    return traj


class ComponentwiseDerivativeTests(unittest.TestCase):
    """§5.3.1 — componentwise dr'/du and d^2 r'/du^2 on the canonical u leaf."""

    def test_worked_example_matches_symbolic_derivatives(self):
        torch = _load_torch()
        componentwise_du = _require("componentwise_du")
        u_value = 0.3
        u = torch.tensor(u_value, dtype=torch.float64, device="cpu")
        first, second = componentwise_du(_worked_example(torch), u)
        exp_first, exp_second = _worked_example_symbolic(u_value)
        got_first = [float(x) for x in first.reshape(-1)]
        got_second = [float(x) for x in second.reshape(-1)]
        self.assertEqual(len(got_first), 3)
        self.assertEqual(len(got_second), 3)
        for got, exp in zip(got_first, exp_first):
            self.assertAlmostEqual(got, exp, delta=SYMBOLIC_TOL)
        for got, exp in zip(got_second, exp_second):
            self.assertAlmostEqual(got, exp, delta=SYMBOLIC_TOL)

    def test_u_leaf_carries_no_manual_chain_factor(self):
        """The tau = 2u - 1 relation is propagated by autograd, not by hand.

        For a forward that computes tau internally, dr'/du must equal
        2 * dr'/dtau and d2r'/du2 must equal 4 * d2r'/dtau2 — obtained purely
        from autograd on the u leaf. A module that ALSO multiplied by 2 / 4
        would overshoot by exactly that factor and fail here.
        """
        torch = _load_torch()
        componentwise_du = _require("componentwise_du")
        u_value = 0.42
        u = torch.tensor(u_value, dtype=torch.float64, device="cpu")
        first, second = componentwise_du(_tau_leaf_trajectory(torch), u)
        d_tau, d2_tau = _tau_leaf_symbolic(u_value)
        got_first = [float(x) for x in first.reshape(-1)]
        got_second = [float(x) for x in second.reshape(-1)]
        for got, exp in zip(got_first, d_tau):
            self.assertAlmostEqual(got, 2.0 * exp, delta=SYMBOLIC_TOL)
        for got, exp in zip(got_second, d2_tau):
            self.assertAlmostEqual(got, 4.0 * exp, delta=SYMBOLIC_TOL)

    def test_componentwise_du_is_not_a_summed_output_vjp(self):
        """Each of the nine derivatives is distinct — an all-ones covector VJP
        would collapse them into one number per leaf. The componentwise result
        must match per-component autograd exactly."""
        torch = _load_torch()
        componentwise_du = _require("componentwise_du")
        u_value = 0.17
        traj = _param_trajectory(
            torch, torch.ones(3, 3, dtype=torch.float64, device="cpu"))
        u = torch.tensor(u_value, dtype=torch.float64, device="cpu")
        first, _second = componentwise_du(traj, u)
        flat = first.reshape(-1)
        self.assertEqual(flat.numel(), 9)

        # Independent per-component autograd oracle (explicit loop; never .sum()).
        u_leaf = torch.tensor(u_value, dtype=torch.float64, device="cpu",
                              requires_grad=True)
        out = traj(u_leaf).reshape(-1)
        for k in range(9):
            grad_k = torch.autograd.grad(out[k], u_leaf, retain_graph=True)[0]
            self.assertAlmostEqual(float(flat[k]), float(grad_k),
                                   delta=SYMBOLIC_TOL)

        # A summed-output VJP would equal the SUM of the nine; assert the
        # componentwise vector is not degenerate (the nine differ).
        values = [float(x) for x in flat]
        self.assertGreater(len(set(round(v, 9) for v in values)), 1)

    def test_batched_leaf_returns_nine_derivatives_per_time_point(self):
        """Batch contract: a (N_t,) leaf -> (N_t, 9) first/second derivatives."""
        torch = _load_torch()
        componentwise_du = _require("componentwise_du")
        n_t = 5
        u = torch.linspace(0.1, 0.9, n_t, dtype=torch.float64, device="cpu")
        traj = _param_trajectory(
            torch, torch.ones(3, 3, dtype=torch.float64, device="cpu"))
        first, second = componentwise_du(traj, u)
        self.assertEqual(tuple(first.reshape(n_t, -1).shape), (n_t, 9))
        self.assertEqual(tuple(second.reshape(n_t, -1).shape), (n_t, 9))
        # Row n must equal the scalar-leaf derivative at u[n].
        row = first.reshape(n_t, -1)[2]
        scalar_first, _ = componentwise_du(
            traj, torch.tensor(float(u[2]), dtype=torch.float64, device="cpu"))
        for got, exp in zip(row.reshape(-1), scalar_first.reshape(-1)):
            self.assertAlmostEqual(float(got), float(exp), delta=SYMBOLIC_TOL)


class SoftenedAccelerationTests(unittest.TestCase):
    """§3.2 — softened Newtonian force sum with raw masses and G = 1."""

    def test_matches_hand_computed_equal_mass_geometry(self):
        torch = _load_torch()
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        pos = _three_body_positions(torch, dtype, device)
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        got = softened_acceleration(pos, masses, eps_soft=eps_soft,
                                    dtype=dtype, device=device)
        expected = _reference_softened_acceleration(
            pos.tolist(), [1.0, 1.0, 1.0], eps_soft)
        self.assertEqual(tuple(got.shape), (3, 3))
        for i in range(3):
            for k in range(3):
                self.assertAlmostEqual(float(got[i][k]), expected[i][k],
                                       delta=1e-10)

    def test_matches_hand_computed_unequal_mass_geometry(self):
        """Unequal (hierarchical-style) RAW masses — an equal-mass fixture alone
        would mask a wrong (mass-dropped) force sum."""
        torch = _load_torch()
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        pos = _three_body_positions(torch, dtype, device)
        raw = [0.105, 0.897, 2.377]
        masses = torch.tensor(raw, dtype=dtype, device=device)
        got = softened_acceleration(pos, masses, eps_soft=eps_soft,
                                    dtype=dtype, device=device)
        expected = _reference_softened_acceleration(pos.tolist(), raw, eps_soft)
        for i in range(3):
            for k in range(3):
                self.assertAlmostEqual(float(got[i][k]), expected[i][k],
                                       delta=1e-10)

    def test_batched_positions_preserve_leading_time_axis(self):
        torch = _load_torch()
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        single = _three_body_positions(torch, dtype, device)
        batched = torch.stack([single, single * 1.5, single * 0.75])
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        got = softened_acceleration(batched, masses, eps_soft=eps_soft,
                                    dtype=dtype, device=device)
        self.assertEqual(tuple(got.shape), (3, 3, 3))
        first = softened_acceleration(single, masses, eps_soft=eps_soft,
                                      dtype=dtype, device=device)
        for i in range(3):
            for k in range(3):
                self.assertAlmostEqual(float(got[0][i][k]), float(first[i][k]),
                                       delta=1e-12)

    def test_softening_uses_the_squared_norm_not_the_distance(self):
        """PHYS-03: r_safe = sqrt(||d||^2 + eps^2). The anti-pattern
        ``||d|| + eps`` is prohibited and gives a measurably different value at
        a separation comparable to eps_soft."""
        torch = _load_torch()
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        # Bodies 0 and 1 separated by exactly eps_soft along x.
        pos = torch.tensor(
            [
                [0.0, 0.0, 0.0],
                [eps_soft, 0.0, 0.0],
                [5.0, 0.0, 0.0],
            ],
            dtype=dtype, device=device)
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        got = softened_acceleration(pos, masses, eps_soft=eps_soft,
                                    dtype=dtype, device=device)
        additive_on_norm = _reference_softened_acceleration(
            pos.tolist(), [1.0, 1.0, 1.0], eps_soft)  # squared-norm oracle
        self.assertAlmostEqual(float(got[0][0]), additive_on_norm[0][0],
                               delta=1e-6)
        # The prohibited (||d|| + eps) form would give |d| / (2 eps)^3 for the
        # 0-1 pair; the correct softened form gives eps / (sqrt(2) eps)^3.
        prohibited = eps_soft / ((eps_soft + eps_soft) ** 3)
        correct = eps_soft / ((math.sqrt(2.0) * eps_soft) ** 3)
        self.assertNotAlmostEqual(prohibited, correct, delta=1e-3 * abs(correct))
        # The 0-1 contribution dominates; the implementation must match the
        # squared-norm (correct) value, not the prohibited one.
        self.assertLess(abs(float(got[0][0]) - additive_on_norm[0][0]),
                        abs(float(got[0][0]) - prohibited))

    def test_non_finite_position_raises(self):
        torch = _load_torch()
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        pos = _three_body_positions(torch, dtype, device).clone()
        pos[1][1] = float("nan")
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        with self.assertRaises(ValueError):
            softened_acceleration(pos, masses, eps_soft=eps_soft,
                                  dtype=dtype, device=device)


class PhysicsResidualTests(unittest.TestCase):
    """The full PHYS-02 residual f_i = a'_i - sum_{j != i} F_ij."""

    def test_residual_is_zero_on_an_exact_newtonian_two_body_free_fall(self):
        """A trajectory that is NOT a solution has a non-zero residual; a
        trajectory built to satisfy a' = softened force has a ~zero residual.

        We construct the check the other way round: take a synthetic trajectory,
        compute the residual, and verify it equals (a' - softened_acceleration)
        component-for-component against the two building blocks. This pins the
        residual's definition without inventing a closed-form solution."""
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        componentwise_du = _require("componentwise_du")
        softened_acceleration = _require("softened_acceleration")
        eps_soft = _require("EPS_SOFT", CONSTANTS_MODULE)
        dtype, device = torch.float64, torch.device("cpu")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        n_t = 4
        u = torch.linspace(0.05, 0.95, n_t, dtype=dtype, device=device)
        masses = torch.tensor([1.0, 0.897, 2.377], dtype=dtype, device=device)

        residual = physics_residual(traj, u, masses, dtype=dtype, device=device)
        self.assertEqual(tuple(residual.shape), (n_t, 3, 3))

        _first, second = componentwise_du(traj, u)
        accel = second.reshape(n_t, 3, 3)
        positions = torch.stack([traj(u[n]) for n in range(n_t)])
        force = softened_acceleration(positions.detach(), masses,
                                      eps_soft=eps_soft,
                                      dtype=dtype, device=device)
        expected = accel.detach() - force
        for n in range(n_t):
            for i in range(3):
                for k in range(3):
                    self.assertAlmostEqual(float(residual[n][i][k]),
                                           float(expected[n][i][k]),
                                           delta=1e-8)

    def test_batch_dimension_contract(self):
        """(N_t, 3, 3) positions + (N_t,) u leaf -> (N_t, 3, 3) residual."""
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        for n_t in (1, 7):
            u = torch.linspace(0.1, 0.9, n_t, dtype=dtype, device=device)
            res = physics_residual(traj, u, masses, dtype=dtype, device=device)
            self.assertEqual(tuple(res.shape), (n_t, 3, 3))

    def test_positions_tensor_path_matches_callable_path(self):
        """The residual accepts a graph-connected (N_t, 3, 3) positions tensor
        as well as a callable model; both must agree (batch contract seam)."""
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        masses = torch.tensor([1.0, 0.5, 1.5], dtype=dtype, device=device)
        n_t = 3
        u_leaf = torch.linspace(0.2, 0.8, n_t, dtype=dtype, device=device,
                                requires_grad=True)
        positions = torch.stack([traj(u_leaf[n]) for n in range(n_t)])
        from_tensor = physics_residual(positions, u_leaf, masses,
                                       dtype=dtype, device=device)
        u_plain = u_leaf.detach()
        from_callable = physics_residual(traj, u_plain, masses,
                                         dtype=dtype, device=device)
        self.assertEqual(tuple(from_tensor.shape), (n_t, 3, 3))
        for n in range(n_t):
            for i in range(3):
                for k in range(3):
                    self.assertAlmostEqual(float(from_tensor[n][i][k]),
                                           float(from_callable[n][i][k]),
                                           delta=1e-8)

    def test_gradcheck_fp64_cpu(self):
        """torch.autograd.gradcheck on the residual under fp64-CPU.

        Inputs are kept well above the softening floor (edge R3) so the finite-
        difference check is well conditioned. The gradient path exercised is the
        training-relevant one: parameters -> double-AD residual.
        """
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        masses = torch.tensor([1.0, 0.897, 2.377], dtype=dtype, device=device)
        n_t = 2
        u = torch.linspace(0.25, 0.75, n_t, dtype=dtype, device=device)
        theta = torch.full((3, 3), 0.5, dtype=dtype, device=device,
                           requires_grad=True)

        def f(theta_in):
            traj = _param_trajectory(torch, theta_in)
            return physics_residual(traj, u, masses, dtype=dtype, device=device)

        self.assertTrue(torch.autograd.gradcheck(
            f, (theta,), eps=GRADCHECK_EPS, atol=GRADCHECK_ATOL,
            rtol=GRADCHECK_RTOL))

    def test_non_finite_leaf_raises(self):
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        u = torch.tensor([0.1, float("nan")], dtype=dtype, device=device)
        with self.assertRaises(ValueError):
            physics_residual(traj, u, masses, dtype=dtype, device=device)

    def test_non_finite_positions_raise(self):
        torch = _load_torch()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        u = torch.tensor([0.3], dtype=dtype, device=device, requires_grad=True)
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        positions = torch.stack([traj(u[0])])
        bad = positions.clone()
        bad = bad + torch.tensor(
            [[[float("inf"), 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]],
            dtype=dtype, device=device)
        with self.assertRaises(ValueError):
            physics_residual(bad, u, masses, dtype=dtype, device=device)


class PrecisionAgnosticTests(unittest.TestCase):
    """The identical code path runs under fp32-MPS (guarded) — no hard-coded
    precision/device anywhere in the module (CTX-14 / ENV-04)."""

    def test_runs_under_fp32_mps(self):
        torch = _load_torch()
        if not _mps_available(torch):
            raise unittest.SkipTest("MPS not available on this host")
        physics_residual = _require("physics_residual")
        dtype, device = torch.float32, torch.device("mps")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        masses = torch.tensor([1.0, 0.897, 2.377], dtype=dtype, device=device)
        n_t = 3
        u = torch.linspace(0.2, 0.8, n_t, dtype=dtype, device=device)
        res = physics_residual(traj, u, masses, dtype=dtype, device=device)
        self.assertEqual(tuple(res.shape), (n_t, 3, 3))
        self.assertEqual(res.device.type, "mps")
        self.assertEqual(res.dtype, torch.float32)
        self.assertTrue(bool(torch.isfinite(res).all()))

    def test_module_does_not_mutate_global_default_dtype(self):
        torch = _load_torch()
        before = torch.get_default_dtype()
        physics_residual = _require("physics_residual")
        dtype, device = torch.float64, torch.device("cpu")
        theta = torch.ones(3, 3, dtype=dtype, device=device)
        traj = _param_trajectory(torch, theta)
        masses = torch.tensor([1.0, 1.0, 1.0], dtype=dtype, device=device)
        u = torch.tensor([0.4], dtype=dtype, device=device)
        physics_residual(traj, u, masses, dtype=dtype, device=device)
        self.assertEqual(torch.get_default_dtype(), before)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
