"""Phase 38 / NET-01 — SQR-SkipResNet-SIREN backbone structure test contract.

Wave 2 contract. Tests import ``pinn.network`` inside test methods via
PER-SYMBOL deferred imports, so the suite SKIPs cleanly (never ERRORs) before
``pinn/network.py`` lands at task 38-02-03.

Grounding:
  * pinn_architecture.md §2.1 (SIREN sine activation sin(omega_0 (W x + b))).
  * pinn_architecture.md §2.2 (principled init: first layer
    U[-1/n_in, 1/n_in]; hidden layers U[-sqrt(6/n_in)/hidden_omega_0, +...];
    line 983 fixes the exact bounds).
  * pinn_architecture.md §2.3 (odd-layer update
    x^(l) = f_sr^(l)(x^(l-1)) + (LayerNorm(x^(l-1)))^p; even-layer plain
    SIREN block; p = 2).
  * pinn_architecture.md §2.4 Table 1 (depth 12, width 256, LayerNorm
    elementwise_affine=False eps=1e-5 odd layers only, first_omega_0=30,
    hidden_omega_0=1, linear output).
  * .claude/rules/pinn-reference.md (locked 14-dim input [tau, IC13],
    9-dim output).

The SIREN principled-init STATISTICS test operationalizes the "consistent with
a uniform init" clause into three concrete checks that jointly REJECT any
Kaiming/Xavier NORMAL substitute (cycle-1 HIGH #4 / cycle-3 MEDIUM #5):
  (i)   every pooled sample within the bound (max_abs <= b)
  (ii)  pooled empirical variance within +/-20% of the uniform variance b^2/3
  (iii) pooled max-abs reaches the bound (>= 0.9*b)
A normal narrow enough to satisfy (i) has variance << b^2/3 (fails ii); a
normal with variance ~ b^2/3 puts ~8% of samples beyond b (fails i).
"""

import ast
import importlib
import math
import pathlib
import re
import unittest

NETWORK_MODULE = "pinn.network"
ARCH_SPEC_MODULE = "pinn.architecture_spec"
RUNTIME_MODULE = "pinn.runtime"


def _load_torch():
    try:
        import torch
    except ImportError as exc:
        raise unittest.SkipTest(f"torch not installed: {exc}")
    return torch


def _load_runtime():
    try:
        return importlib.import_module(RUNTIME_MODULE)
    except ImportError as exc:
        raise unittest.SkipTest(f"{RUNTIME_MODULE} not implemented: {exc}")


def _require(symbol_name, module_name):
    """Per-symbol deferred import; SkipTest if module OR symbol is absent."""
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise unittest.SkipTest(f"{module_name} not implemented yet: {exc}")
    if not hasattr(module, symbol_name):
        raise unittest.SkipTest(
            f"{module_name}.{symbol_name} not implemented yet")
    return getattr(module, symbol_name)


def _build(torch, seed=0):
    build_network = _require("build_network", NETWORK_MODULE)
    ArchitectureSpec = _require("ArchitectureSpec", ARCH_SPEC_MODULE)
    runtime = _load_runtime()
    spec = runtime.resolve_runtime("float64", "cpu")
    model = build_network(ArchitectureSpec(seed=seed),
                          dtype=spec.dtype, device=spec.torch_device)
    return model, spec


class TopologyTests(unittest.TestCase):
    """§2.4 Table 1 — exact layer counts, dims, SIREN omega, LayerNorm shape."""

    def test_input_layer_is_14_to_256(self):
        torch = _load_torch()
        model, _ = _build(torch)
        input_layer = model.input_layer
        self.assertEqual(input_layer.in_features, 14)
        self.assertEqual(input_layer.out_features, 256)

    def test_hidden_layers_are_12_of_256_to_256(self):
        torch = _load_torch()
        model, _ = _build(torch)
        hidden = model.hidden_layers
        self.assertEqual(len(hidden), 12)
        for layer in hidden:
            # Every hidden layer carries a SIREN sublayer with 256->256.
            sirens = self._collect_siren_sublayers(layer, torch)
            self.assertEqual(len(sirens), 1,
                             "each hidden layer must contain exactly one "
                             "SIREN block")
            siren = sirens[0]
            self.assertEqual(siren.in_features, 256)
            self.assertEqual(siren.out_features, 256)

    def _collect_siren_sublayers(self, module, torch):
        # A SIREN block exposes omega_0 and in_features/out_features. Return
        # all such sublayers within this hidden-layer module.
        found = []
        stack = [module]
        seen = set()
        while stack:
            m = stack.pop()
            if id(m) in seen:
                continue
            seen.add(id(m))
            if hasattr(m, "omega_0") and hasattr(m, "in_features"):
                found.append(m)
            for child in m.children():
                stack.append(child)
        return found

    def test_output_layer_is_256_to_9_linear(self):
        torch = _load_torch()
        model, _ = _build(torch)
        out = model.output_layer
        self.assertEqual(out.in_features, 256)
        self.assertEqual(out.out_features, 9)
        # Linear head: forward must NOT apply any activation (output ~ linear
        # projection of its input). We assert the head's weight shape and that
        # the forward is a pure affine map by checking there is no nonlinearity
        # attribute registered.
        self.assertFalse(hasattr(out, "activation"),
                         "output head must be linear (no activation)")

    def test_siren_first_omega_0_is_30(self):
        torch = _load_torch()
        model, _ = _build(torch)
        self.assertAlmostEqual(float(model.input_layer.omega_0), 30.0,
                               places=6)

    def test_siren_hidden_omega_0_is_1(self):
        torch = _load_torch()
        model, _ = _build(torch)
        for layer in model.hidden_layers:
            for siren in self._collect_siren_sublayers(layer, torch):
                self.assertAlmostEqual(float(siren.omega_0), 1.0, places=6,
                                       msg="hidden SIREN omega_0 must be 1.0")

    def test_layernorm_count_and_attributes(self):
        torch = _load_torch()
        model, _ = _build(torch)
        layernorms = [m for m in model.modules() if isinstance(m, torch.nn.LayerNorm)]
        # 6 odd hidden layers (1,3,5,7,9,11) each contribute one LayerNorm.
        self.assertEqual(len(layernorms), 6,
                         "exactly 6 LayerNorm modules (one per odd layer)")
        for ln in layernorms:
            self.assertFalse(ln.elementwise_affine,
                             "LayerNorm must have elementwise_affine=False (ARCH-02)")
            self.assertAlmostEqual(float(ln.eps), 1e-5, places=12,
                                   msg="LayerNorm eps must be 1e-5")
            self.assertEqual(ln.normalized_shape, (256,))

    def test_layernorm_only_on_odd_layers(self):
        torch = _load_torch()
        model, _ = _build(torch)
        # Even hidden layers must contain NO LayerNorm; odd layers must contain
        # exactly one. Hidden layers are 1-indexed: index 0 -> layer 1 (odd).
        for idx, layer in enumerate(model.hidden_layers):
            layer_num = idx + 1
            lns = [m for m in layer.modules() if isinstance(m, torch.nn.LayerNorm)]
            if layer_num % 2 == 1:
                self.assertEqual(len(lns), 1,
                                 f"odd layer {layer_num} must have one LayerNorm")
            else:
                self.assertEqual(len(lns), 0,
                                 f"even layer {layer_num} must have NO LayerNorm")

    def test_odd_layer_update_equals_siren_plus_layernorm_squared(self):
        torch = _load_torch()
        model, _ = _build(torch)
        # First odd hidden layer (layer 1).
        block = model.hidden_layers[0]
        layernorms = [m for m in block.modules() if isinstance(m, torch.nn.LayerNorm)]
        self.assertEqual(len(layernorms), 1)
        siren = self._collect_siren_sublayers(block, torch)[0]
        layernorm = layernorms[0]
        p = int(model.power_p)
        self.assertEqual(p, 2)
        x_prev = torch.randn(4, 256, dtype=siren.weight.dtype,
                             device=siren.weight.device)
        expected = siren(x_prev) + layernorm(x_prev) ** p
        actual = block(x_prev)
        self.assertTrue(torch.allclose(actual, expected, atol=1e-12, rtol=0),
                        "odd-layer update must equal "
                        "SIREN_block(x_prev) + (LayerNorm(x_prev))**2")

    def test_even_layer_is_plain_siren_block(self):
        torch = _load_torch()
        model, _ = _build(torch)
        # First even hidden layer (layer 2) — plain SIREN, no skip/LayerNorm.
        block = model.hidden_layers[1]
        siren = self._collect_siren_sublayers(block, torch)
        # Even layer IS the SIREN block itself (no wrapper skip).
        self.assertGreaterEqual(len(siren), 1)
        x_prev = torch.randn(4, 256, dtype=siren[0].weight.dtype,
                             device=siren[0].weight.device)
        expected = siren[0](x_prev)
        actual = block(x_prev)
        self.assertTrue(torch.allclose(actual, expected, atol=1e-12, rtol=0),
                        "even-layer output must equal its plain SIREN block")


class DeterminismAndSideEffectsTests(unittest.TestCase):
    """NET-01 AC #3 / edge R1 — deterministic seeded build, no side effects."""

    def test_same_seed_gives_identical_state_dict(self):
        torch = _load_torch()
        m1, _ = _build(torch, seed=7)
        m2, _ = _build(torch, seed=7)
        sd1 = m1.state_dict()
        sd2 = m2.state_dict()
        self.assertEqual(set(sd1.keys()), set(sd2.keys()))
        for key in sd1:
            self.assertTrue(torch.equal(sd1[key], sd2[key]),
                            f"param {key!r} differs between same-seed builds")

    def test_different_seed_gives_different_state_dict(self):
        torch = _load_torch()
        m1, _ = _build(torch, seed=1)
        m2, _ = _build(torch, seed=2)
        sd1 = m1.state_dict()
        sd2 = m2.state_dict()
        # At least one parameter must differ.
        any_diff = any(not torch.equal(sd1[k], sd2[k]) for k in sd1)
        self.assertTrue(any_diff, "different seeds must yield different params")

    def test_build_does_not_mutate_global_default_dtype(self):
        torch = _load_torch()
        _require("build_network", NETWORK_MODULE)
        _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        ArchitectureSpec = _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        build_network = _require("build_network", NETWORK_MODULE)
        before = torch.get_default_dtype()
        try:
            build_network(ArchitectureSpec(),
                          dtype=spec.dtype, device=spec.torch_device)
        finally:
            after = torch.get_default_dtype()
        self.assertEqual(before, after,
                         "build_network mutated the global default dtype")

    def test_build_does_not_mutate_global_rng(self):
        torch = _load_torch()
        _require("build_network", NETWORK_MODULE)
        _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        ArchitectureSpec = _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        build_network = _require("build_network", NETWORK_MODULE)
        before = torch.get_rng_state()
        try:
            build_network(ArchitectureSpec(),
                          dtype=spec.dtype, device=spec.torch_device)
        finally:
            after = torch.get_rng_state()
        self.assertTrue(torch.equal(before, after),
                        "build_network mutated the global CPU RNG state")

    def test_build_writes_no_files(self):
        torch = _load_torch()
        _require("build_network", NETWORK_MODULE)
        _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float64", "cpu")
        ArchitectureSpec = _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        build_network = _require("build_network", NETWORK_MODULE)
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                build_network(ArchitectureSpec(),
                              dtype=spec.dtype, device=spec.torch_device)
                written = list(pathlib.Path(tmp).rglob("*"))
            finally:
                os.chdir(cwd)
        written_files = [p for p in written if p.is_file()]
        self.assertEqual(written_files, [],
                         "build_network wrote files (side effect): "
                         f"{[str(p) for p in written_files]}")


class ForwardPrecisionTests(unittest.TestCase):
    """NET-01 AC #2 — forward through the SAME code path under both branches."""

    def test_forward_returns_shape_9_fp64_cpu(self):
        torch = _load_torch()
        model, spec = _build(torch)
        tau_ic13 = torch.randn(14, dtype=spec.dtype, device=spec.torch_device)
        masses = torch.as_tensor((0.1, 1.0, 2.4),
                                 dtype=spec.dtype, device=spec.torch_device)
        out = model.forward(tau_ic13, masses)
        self.assertEqual(tuple(out.shape), (9,))
        self.assertTrue(torch.isfinite(out).all().item())

    def test_forward_returns_shape_9_batched_fp64_cpu(self):
        torch = _load_torch()
        model, spec = _build(torch)
        n = 6
        tau_ic13 = torch.randn(n, 14, dtype=spec.dtype, device=spec.torch_device)
        masses = torch.as_tensor((0.1, 1.0, 2.4),
                                 dtype=spec.dtype, device=spec.torch_device)
        out = model.forward(tau_ic13, masses)
        self.assertEqual(tuple(out.shape), (n, 9))
        self.assertTrue(torch.isfinite(out).all().item())

    def test_forward_returns_shape_9_fp32_mps(self):
        torch = _load_torch()
        if not torch.backends.mps.is_available():
            self.skipTest("MPS unavailable")
        build_network = _require("build_network", NETWORK_MODULE)
        ArchitectureSpec = _require("ArchitectureSpec", ARCH_SPEC_MODULE)
        runtime = _load_runtime()
        spec = runtime.resolve_runtime("float32", "mps")
        model = build_network(ArchitectureSpec(),
                              dtype=spec.dtype, device=spec.torch_device)
        tau_ic13 = torch.randn(14, dtype=spec.dtype, device=spec.torch_device)
        masses = torch.as_tensor((0.1, 1.0, 2.4),
                                 dtype=spec.dtype, device=spec.torch_device)
        out = model.forward(tau_ic13, masses)
        self.assertEqual(tuple(out.shape), (9,))
        self.assertTrue(torch.isfinite(out).all().item())


class SirenInitStatisticsTests(unittest.TestCase):
    """§2.2 / :983 — principled SIREN init is UNIFORM, not normal.

    Three concrete checks over pooled per-layer weights (b = per-layer bound)
    jointly reject any Kaiming/Xavier NORMAL substitute:
      (i)   max_abs(w) <= b            (every sample within the bound)
      (ii)  0.8 * b^2/3 <= var(w) <= 1.2 * b^2/3  (uniform variance band)
      (iii) max_abs(w) >= 0.9 * b      (the bound is actually reached)
    """

    SEEDS = (0, 1, 2, 3)

    def _pool_first_layer_weights(self, torch):
        weights = []
        for seed in self.SEEDS:
            model, _ = _build(torch, seed=seed)
            weights.append(model.input_layer.weight.detach().to("cpu").to(torch.float64))
        return torch.cat([w.reshape(-1) for w in weights], dim=0)

    def _pool_hidden_layer_weights(self, torch):
        weights = []
        for seed in self.SEEDS:
            model, _ = _build(torch, seed=seed)
            # First even hidden layer (layer 2) is a plain SIREN block whose
            # weight is directly accessible.
            layer = model.hidden_layers[1]
            w = self._extract_weight(layer)
            weights.append(w.detach().to("cpu").to(torch.float64))
        return torch.cat([w.reshape(-1) for w in weights], dim=0)

    def _extract_weight(self, layer):
        # The even hidden layer is itself a SIREN layer exposing .weight.
        return layer.weight

    def test_first_layer_weights_within_uniform_bound(self):
        torch = _load_torch()
        w = self._pool_first_layer_weights(torch)
        n_in = 14
        b = 1.0 / n_in
        self.assertLessEqual(float(w.abs().max()), b,
                             f"first-layer |w| must be within U[-1/{n_in}, 1/{n_in}]")

    def test_first_layer_weights_uniform_variance(self):
        torch = _load_torch()
        w = self._pool_first_layer_weights(torch)
        n_in = 14
        b = 1.0 / n_in
        var_uniform = (b ** 2) / 3.0
        var_emp = float(torch.var(w, unbiased=False))
        self.assertGreaterEqual(var_emp, 0.8 * var_uniform,
                                "first-layer var below 0.8*b^2/3 (not uniform?)")
        self.assertLessEqual(var_emp, 1.2 * var_uniform,
                             "first-layer var above 1.2*b^2/3 (not uniform?)")

    def test_first_layer_weights_reach_bound(self):
        torch = _load_torch()
        w = self._pool_first_layer_weights(torch)
        n_in = 14
        b = 1.0 / n_in
        self.assertGreaterEqual(float(w.abs().max()), 0.9 * b,
                                "first-layer max-abs must reach >= 0.9*b")

    def test_hidden_layer_weights_within_uniform_bound(self):
        torch = _load_torch()
        w = self._pool_hidden_layer_weights(torch)
        n_in = 256
        hidden_omega_0 = 1.0
        b = math.sqrt(6.0 / n_in) / hidden_omega_0
        self.assertLessEqual(
            float(w.abs().max()), b,
            f"hidden |w| must be within U[-sqrt(6/{n_in})/{hidden_omega_0}, +...]")

    def test_hidden_layer_weights_uniform_variance(self):
        torch = _load_torch()
        w = self._pool_hidden_layer_weights(torch)
        n_in = 256
        hidden_omega_0 = 1.0
        b = math.sqrt(6.0 / n_in) / hidden_omega_0
        var_uniform = (b ** 2) / 3.0
        var_emp = float(torch.var(w, unbiased=False))
        self.assertGreaterEqual(var_emp, 0.8 * var_uniform,
                                "hidden var below 0.8*b^2/3 (not uniform?)")
        self.assertLessEqual(var_emp, 1.2 * var_uniform,
                             "hidden var above 1.2*b^2/3 (not uniform?)")

    def test_hidden_layer_weights_reach_bound(self):
        torch = _load_torch()
        w = self._pool_hidden_layer_weights(torch)
        n_in = 256
        hidden_omega_0 = 1.0
        b = math.sqrt(6.0 / n_in) / hidden_omega_0
        self.assertGreaterEqual(float(w.abs().max()), 0.9 * b,
                                "hidden max-abs must reach >= 0.9*b")


class SourceInspectionTests(unittest.TestCase):
    """CTX-14 / ENV-04 — no precision/device default, no availability probe,
    no v1.3-era import. Technique: tests/phase37/test_runtime.py:139-183
    (AST executable-code inspection, stripping docstrings/comments)."""

    def _executable_source(self, path):
        source = path.read_text()
        tree = ast.parse(source, filename=str(path))
        docstring_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef, ast.Module)):
                doc = ast.get_docstring(node, clean=False)
                if doc and node.body and isinstance(node.body[0], ast.Expr):
                    expr = node.body[0]
                    if hasattr(expr, "lineno") and hasattr(expr, "end_lineno"):
                        for ln in range(expr.lineno,
                                        (expr.end_lineno or expr.lineno) + 1):
                            docstring_lines.add(ln)
        executable_lines = []
        for ln, line in enumerate(source.splitlines(), 1):
            if ln in docstring_lines:
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            executable_lines.append(stripped)
        return "\n".join(executable_lines)

    def test_network_has_no_precision_default_or_availability_probe(self):
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        network_py = repo_root / "pinn" / "network.py"
        if not network_py.exists():
            self.skipTest("pinn/network.py not implemented yet")
        executable = self._executable_source(network_py)
        self.assertNotIn("torch.set_default_dtype", executable,
                         "network.py mutates the global default dtype")
        self.assertNotIn("is_available", executable,
                         "network.py performs an availability probe")
        self.assertFalse(re.search(r"\bretry\b", executable, re.IGNORECASE),
                         "network.py implements a retry loop")

    def test_com_projection_has_no_precision_default_or_availability_probe(self):
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        com_py = repo_root / "pinn" / "com_projection.py"
        if not com_py.exists():
            self.skipTest("pinn/com_projection.py not implemented yet")
        executable = self._executable_source(com_py)
        self.assertNotIn("torch.set_default_dtype", executable,
                         "com_projection.py mutates the global default dtype")
        self.assertNotIn("is_available", executable,
                         "com_projection.py performs an availability probe")

    def test_no_module_imports_v13_era_files(self):
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        banned = ("basic_architecture", "data-processing-pipeline-full",
                  "data-handling")
        for rel in ("pinn/network.py", "pinn/com_projection.py"):
            path = repo_root / rel
            if not path.exists():
                continue
            executable = self._executable_source(path)
            for name in banned:
                self.assertNotIn(name, executable,
                                 f"{rel} imports banned v1.3-era module {name}")


if __name__ == "__main__":
    unittest.main()
