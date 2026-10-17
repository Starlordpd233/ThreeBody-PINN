"""Phase 59 DIAG-07: JX-5, JX-2, JX-4 and JX-3 on generation 7.

Bootstrap runs before any pinn import. Every pinn import happens inside a
function. The runtime is the run's own ("float32", "mps"); the CPU float64
cross-check belongs to JX-1 and JX-10 only (D-36). MPS has no float64, so a
tensor is moved to the CPU before it is widened.
"""

from __future__ import annotations

import argparse
import gc
import sys
from pathlib import Path

import numpy as np

import diag07_common


RUNTIME = ("float32", "mps")
MICROBATCH = 256
SUBSET_STRIDE = 16
MIXED_CHUNK = 16
ODD_BLOCKS = (0, 2, 4, 6, 8, 10)
EXPECTED_MONITOR_ANCHOR = 28


class ToleranceFailure(RuntimeError):
    """A pre-registered check failed. The result is kept and not accepted."""


def _parse(argv):
    parser = argparse.ArgumentParser(description="Read-only JX-5, JX-2, JX-4 and JX-3.")
    parser.add_argument("--code-root", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument(
        "--experiment", choices=("jx5", "jx2", "jx4", "jx3", "all"), default="all",
    )
    parser.add_argument(
        "--evidence-root",
        default=str(Path(__file__).resolve().parent),
    )
    return parser.parse_args(argv)


_PLANNED = {
    "jx5": ("jx05", ["jx05.json"]),
    "jx2": ("jx02", ["jx02.json"]),
    "jx4": ("jx04", ["jx04.json"]),
    "jx3": ("jx03", ["jx03.json"]),
    "all": ("jx02_jx05", ["jx05.json", "jx02.json", "jx04.json", "jx03.json"]),
}


def _cpu64(tensor):
    """Detach, move to the CPU, then widen to float64 (MPS has no float64)."""
    import torch

    return tensor.detach().to("cpu").to(torch.float64)


def _summary(values) -> dict:
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    return {
        "n": int(array.size),
        "rms": float(np.sqrt(np.mean(array ** 2))),
        "median": float(np.median(array)),
        "max": float(np.max(array)),
    }


def _row_norms(tensor):
    """Per-row Frobenius norm of an (N, 3, 3) tensor as a float64 numpy array."""
    flat = _cpu64(tensor).reshape(tensor.shape[0], -1)
    return flat.pow(2).sum(dim=1).sqrt().numpy()


def subset_rows(n) -> np.ndarray:
    """Rows 0, 16, 32, ... below n of a time-sorted set."""
    return np.arange(0, int(n), SUBSET_STRIDE, dtype=np.int64)


def _input(u, ic13):
    """The trainer's 14-dim input [tau, IC13] with tau = 2u - 1."""
    import torch

    tau = (2.0 * u - 1.0).reshape(1)
    return torch.cat([tau, ic13.reshape(-1)], dim=0)


def ic_errors(anchor_ctx, *, dtype, device) -> dict:
    """IC losses and error norms of the anchor trajectory at u = 0."""
    import torch
    from pinn.loss_catalog import ic_anchor_loss
    from pinn.physics_residual import componentwise_du

    zero_u = torch.zeros((), dtype=dtype, device=device)
    with torch.no_grad():
        pred_r0 = anchor_ctx.traj(zero_u).reshape(3, 3)
    first, _second = componentwise_du(anchor_ctx.traj, zero_u)
    pred_v0 = first.reshape(3, 3).detach()
    l_r = ic_anchor_loss(
        pred_r0, anchor_ctx.true_r0, pred_v0, anchor_ctx.true_v0,
        beta_v=0.0, dtype=dtype, device=device,
    )
    l_ic = ic_anchor_loss(
        pred_r0, anchor_ctx.true_r0, pred_v0, anchor_ctx.true_v0,
        beta_v=1.0, dtype=dtype, device=device,
    )
    position = _cpu64(pred_r0 - anchor_ctx.true_r0.reshape(3, 3))
    velocity = _cpu64(pred_v0 - anchor_ctx.true_v0.reshape(3, 3))
    return {
        "l_r": float(_cpu64(l_r)),
        "l_v": float(_cpu64(l_ic - l_r)),
        "l_ic": float(_cpu64(l_ic)),
        "position_error_norm": float(torch.linalg.vector_norm(position)),
        "velocity_error_norm": float(torch.linalg.vector_norm(velocity)),
    }


def mixed_derivative_norms(model, ic13, masses, u_rows, *, dtype, device) -> np.ndarray:
    """Per-row Frobenius norm of d(dr'/du)/d(IC13), shape (9, 13) per row.

    The trainer's closure with IC13 as an argument: jacrev over u gives dr'/du,
    jacrev of that over IC13 gives the mixed derivative, vmapped over the rows.
    """
    import torch

    ic = torch.as_tensor(np.asarray(ic13, dtype=np.float64), dtype=dtype, device=device).reshape(-1)
    mass = torch.as_tensor(np.asarray(masses, dtype=np.float64), dtype=dtype, device=device).reshape(1, 3)

    def positions(u, ic_vector):
        return model(_input(u, ic_vector).unsqueeze(0), mass).reshape(-1)

    velocity = torch.func.jacrev(positions, argnums=0)
    mixed = torch.func.vmap(
        torch.func.jacrev(velocity, argnums=1), in_dims=(0, None),
    )
    u_all = np.asarray(u_rows, dtype=np.float64).reshape(-1)
    norms = []
    for start in range(0, int(u_all.size), MIXED_CHUNK):
        u_chunk = torch.as_tensor(u_all[start:start + MIXED_CHUNK], dtype=dtype, device=device)
        block = mixed(u_chunk, ic)
        norms.append(_cpu64(block).reshape(block.shape[0], -1).pow(2).sum(dim=1).sqrt().numpy())
        del block, u_chunk
        gc.collect(0)
    return np.concatenate(norms)


def _branch_values(model, ic13, u_rows, *, dtype, device):
    """Siren, skip and block outputs of each odd block, and their du-derivatives.

    Returns (values, derivatives), each shaped (rows, blocks, 3, width) with the
    third axis ordered siren, skip, block. x_prev is built from the model's own
    input_layer and preceding hidden_layers.
    """
    import torch

    ic = torch.as_tensor(np.asarray(ic13, dtype=np.float64), dtype=dtype, device=device).reshape(-1)

    def outputs(u):
        x = model.input_layer(_input(u, ic).unsqueeze(0))
        stacked = []
        for index, layer in enumerate(model.hidden_layers):
            if index in ODD_BLOCKS:
                siren = layer.siren(x)
                skip = layer.layernorm(x) ** layer.power_p
                block = layer(x)
                stacked.append(torch.stack([siren, skip, block], dim=0).reshape(3, -1))
                x = block
            else:
                x = layer(x)
            if index >= ODD_BLOCKS[-1]:
                break
        return torch.stack(stacked, dim=0)

    def tangent(u_scalar):
        # dy/du by reverse over reverse: the pullback v -> J^T v is a scalar linear
        # in v, so its gradient in v is J. Forward mode is not used because on MPS
        # it promotes Python scalars to the default float64, which MPS cannot hold.
        values, pullback = torch.func.vjp(outputs, u_scalar)
        return torch.func.grad(lambda v: pullback(v)[0])(torch.zeros_like(values))

    u = torch.as_tensor(np.asarray(u_rows, dtype=np.float64).reshape(-1), dtype=dtype, device=device)
    values = torch.func.vmap(outputs)(u)
    derivatives = torch.func.vmap(tangent)(u)
    return values, derivatives


def branch_scales(model, ic13, u_rows, *, dtype, device, return_values=False):
    """RMS of each odd block's SIREN and skip branch values and du-derivatives."""
    values, derivatives = _branch_values(model, ic13, u_rows, dtype=dtype, device=device)
    values64 = _cpu64(values)
    derivatives64 = _cpu64(derivatives)
    rows = []
    for position, layer_index in enumerate(ODD_BLOCKS):
        def rms(tensor, branch):
            return float(tensor[:, position, branch].pow(2).mean().sqrt())

        rows.append({
            "hidden_layer_index": layer_index,
            "layer_number": layer_index + 1,
            "siren_value_rms": rms(values64, 0),
            "skip_value_rms": rms(values64, 1),
            "block_value_rms": rms(values64, 2),
            "siren_du_rms": rms(derivatives64, 0),
            "skip_du_rms": rms(derivatives64, 1),
            "block_du_rms": rms(derivatives64, 2),
        })
    if return_values:
        return rows, values64, derivatives64
    return rows


def _component_rows(controller, anchor_ctx) -> dict:
    """r', v', a', the softened force and the residual per row, chunked."""
    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME
    from pinn.physics_residual import componentwise_du, softened_acceleration

    dtype, device = controller._dtype, controller._device
    times = anchor_ctx.collocation_times
    norms = {name: [] for name in ("r_prime", "v_prime", "a_prime", "force", "residual")}
    for start in range(0, int(times.shape[0]), MICROBATCH):
        chunk = times[start:start + MICROBATCH]
        u_leaf = torch.as_tensor(chunk / T_CHARACTERISTIC_TIME, dtype=dtype, device=device)
        first, second = componentwise_du(anchor_ctx.traj, u_leaf)
        positions = torch.func.vmap(lambda s: anchor_ctx.traj(s).reshape(-1))(u_leaf)
        positions = positions.reshape(-1, 3, 3)
        velocities = first.reshape(-1, 3, 3)
        accelerations = second.reshape(-1, 3, 3)
        force = softened_acceleration(positions, anchor_ctx.masses, dtype=dtype, device=device)
        residual = accelerations - force
        for name, tensor in (
            ("r_prime", positions), ("v_prime", velocities), ("a_prime", accelerations),
            ("force", force), ("residual", residual),
        ):
            norms[name].append(_row_norms(tensor))
        del first, second, positions, velocities, accelerations, force, residual, u_leaf
        controller._release_chunk_memory()
    return {name: _summary(np.concatenate(parts)) for name, parts in norms.items()}


def _bins(controller, anchor_ctx) -> dict:
    phys_details, _bin_counts = controller._adam_frozen_causal_weights(
        anchor_ctx, microbatch_size=MICROBATCH,
    )
    w_n = [float(value) for value in _cpu64(phys_details["w_n"]).tolist()]
    return {
        "raw_rbar": [float(value) for value in _cpu64(phys_details["raw_rbar"]).tolist()],
        "rtilde": [float(value) for value in _cpu64(phys_details["rbar"]).tolist()],
        "w_n": w_n,
        "r_ref": float(phys_details["r_ref"]),
        "front_idx": max([n for n, w in enumerate(w_n) if w > 0.5], default=-1),
    }


def fixture_anchor_context(controller, source, key, times):
    """The trainer's own anchor context for an arbitrary trajectory and times."""
    from types import SimpleNamespace

    batch = SimpleNamespace(
        replay_keys=(key,),
        lookahead_keys=(),
        data_points=SimpleNamespace(record_keys=(key,)),
        collocation_points=None,
    )
    return controller._build_anchor_context(
        source, batch, fixed_collocation_times=np.asarray(times, dtype=np.float64),
    )


def prefix_profile(controller, anchor_ctx) -> dict:
    """Bin means, causal weights, the prefix of normalized means and the front."""
    bins = _bins(controller, anchor_ctx)
    prefix = [0.0]
    for value in bins["rtilde"]:
        prefix.append(prefix[-1] + float(value))
    bins["prefix"] = prefix
    return bins


def physical_scale(gold_reference) -> float:
    """Mean over gold samples with t <= 10 of the body-averaged squared true force."""
    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME
    from pinn.physics_residual import softened_acceleration

    times = np.asarray(gold_reference.times, dtype=np.float64).reshape(-1)
    keep = times <= float(T_CHARACTERISTIC_TIME) + 1e-9
    positions = np.asarray(gold_reference.positions, dtype=np.float64)[keep]
    force = softened_acceleration(
        positions,
        np.asarray(gold_reference.masses, dtype=np.float64),
        dtype=torch.float64,
        device=torch.device("cpu"),
    )
    return float(((force ** 2).sum(dim=(-2, -1)) / 3.0).mean())


def physical_front(raw_rbar, scale, *, dtype, device) -> int:
    """The causal front with R_ref replaced by a physical scale."""
    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME
    from pinn.loss_catalog import causal_physics_loss

    n_bins = 16
    centres = (np.arange(n_bins) + 0.5) / n_bins * float(T_CHARACTERISTIC_TIME)
    _loss, details = causal_physics_loss(
        torch.as_tensor(np.asarray(raw_rbar, dtype=np.float64), dtype=dtype, device=device),
        r_ref=float(scale),
        times=torch.as_tensor(centres, dtype=dtype, device=device),
        dtype=dtype,
        device=device,
        return_details=True,
    )
    weights = [float(value) for value in _cpu64(details["w_n"]).tolist()]
    return max([n for n, w in enumerate(weights) if w > 0.5], default=-1)


def jx2_reading(frozen_900, frozen_951, draws_900, draws_951) -> str:
    """Parameter motion only if the frozen change exceeds both 20-draw ranges."""
    change = abs(float(frozen_951) - float(frozen_900))
    range_900 = float(np.max(draws_900) - np.min(draws_900))
    range_951 = float(np.max(draws_951) - np.min(draws_951))
    if change > range_900 and change > range_951:
        return "parameter motion"
    return "estimator noise not excluded"


def jx4_reading(front_0, front_951, fixture_rows) -> str:
    """The frozen JX-4 rule on the relative front and the fixtures' tiers."""
    if not int(front_951) > int(front_0):
        return "inconclusive"
    if all(int(row["tier_951"]) == 0 for row in fixture_rows):
        return "relative descent without useful accuracy"
    if any(
        int(row["tier_951"]) >= 1 and float(row["E_951"]) <= 0.9 * float(row["E_0"])
        for row in fixture_rows
    ):
        return "useful accuracy with relative descent"
    return "inconclusive"


def _network_trajectory(model, ic13, masses, times, *, dtype, device, microbatch_size):
    """feasibility_scorer.network_trajectory with an MPS-safe float64 widening.

    GAP-59-13: the scorer widens with one .to(device="cpu", dtype=float64) call,
    which MPS refuses. This copy differs only in moving to the CPU first. The
    scorer itself stays byte-unchanged because its SHA-256 is pinned by the
    committed Plan-07 results.
    """
    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME
    from pinn.physics_residual import componentwise_du
    from pinn.verification.feasibility_scorer import _trainer_closure

    time_array = np.asarray(times, dtype=np.float64).reshape(-1)
    u_all = time_array / float(T_CHARACTERISTIC_TIME)
    traj, flat_traj = _trainer_closure(model, ic13, masses, dtype=dtype, device=device)
    prior_training = bool(model.training)
    position_chunks, velocity_chunks, acceleration_chunks = [], [], []
    try:
        model.eval()
        for start in range(0, int(u_all.shape[0]), microbatch_size):
            u_chunk = torch.as_tensor(
                u_all[start : start + microbatch_size], dtype=dtype, device=device
            )
            positions = torch.func.vmap(flat_traj)(u_chunk)
            velocities = torch.func.vmap(torch.func.jacrev(flat_traj))(u_chunk)
            _first, second = componentwise_du(traj, u_chunk)
            position_chunks.append(_cpu64(positions).numpy().reshape(-1, 3, 3))
            velocity_chunks.append(_cpu64(velocities).numpy().reshape(-1, 3, 3))
            acceleration_chunks.append(_cpu64(second).numpy().reshape(-1, 3, 3))
            del positions, velocities, second, _first, u_chunk
            gc.collect(0)
    finally:
        if prior_training:
            model.train()
        else:
            model.eval()
    return (
        np.concatenate(position_chunks, axis=0),
        np.concatenate(velocity_chunks, axis=0),
        np.concatenate(acceleration_chunks, axis=0),
    )


def network_score(model, ic13, masses, ref_positions, inner_pair, times, *,
                  scorecard, dtype, device, grid, microbatch_size=MICROBATCH):
    """feasibility_scorer.score_network through the MPS-safe trajectory (GAP-59-13)."""
    from dataclasses import replace

    from pinn.verification.feasibility_scorer import (
        load_governed_r_ref,
        physics_residual_context,
        score_trajectory,
    )

    positions, velocities, accelerations = _network_trajectory(
        model, ic13, masses, times, dtype=dtype, device=device, microbatch_size=microbatch_size,
    )
    result = score_trajectory(
        positions, velocities, ref_positions, masses, inner_pair, times,
        velocity_source="autograd", scorecard=scorecard, grid=grid,
    )
    context = physics_residual_context(
        positions, accelerations, masses, r_ref=load_governed_r_ref(),
    )
    return replace(
        result,
        physics_residual_mean=context["mean"],
        physics_residual_max=context["max"],
    )


def _key_json(key) -> dict:
    return {"variant": key.variant, "fidelity": key.fidelity, "id": int(key.id)}


def _grads_clear(model) -> bool:
    clear = True
    for parameter in model.parameters():
        if parameter.grad is not None:
            clear = False
            parameter.grad = None
    return clear


class _Session:
    """One controller, the checkpoint provenance and the non-interference flags."""

    def __init__(self, args, sources, scorecard):
        self.args = args
        self.sources = sources
        self.scorecard = scorecard
        self.controller = diag07_common.build_controller(
            args.code_root, diag07_common.REPO_ROOT, diag07_common.SEED42,
            sources, RUNTIME,
        )
        self.flags = {"parameters": True, "grads": True, "files": True, "optimizer": True}
        self.checkpoints = []
        self._loaded = None

    @property
    def model(self):
        return self.controller.model

    def load(self, name):
        """Load one retention-pinned checkpoint into the controller."""
        path = diag07_common.REPO_ROOT / "runs" / diag07_common.SEED42 / "checkpoints" / name
        before = diag07_common.file_hashes([path])
        payload, info = diag07_common.load_registry_checkpoint(
            diag07_common.REPO_ROOT, diag07_common.SEED42, name, scorecard=self.scorecard,
        )
        self.controller.load_state_dict(payload)
        del payload
        if info not in self.checkpoints:
            self.checkpoints.append(info)
        self._loaded = (path, before, diag07_common.param_fingerprints(self.model))
        return info

    def release(self):
        """Check the loaded checkpoint left nothing behind."""
        path, before, fingerprints = self._loaded
        self.flags["parameters"] &= fingerprints == diag07_common.param_fingerprints(self.model)
        self.flags["grads"] &= _grads_clear(self.model)
        self.flags["files"] &= before == diag07_common.file_hashes([path])
        self.flags["optimizer"] &= self.controller._optimizer is None
        self._loaded = None

    def monitor_anchor(self):
        batch = self.controller._front_monitor_batch
        return self.controller._select_anchor_key(batch)

    def writes(self) -> int:
        return int(self.controller._checkpoint_store.write_attempts)

    def non_interference(self) -> dict:
        return {
            "parameters_unchanged": bool(self.flags["parameters"]),
            "grads_none": bool(self.flags["grads"]),
            "optimizer_constructed": bool(self.flags["optimizer"]),
            "checkpoint_writes": self.writes(),
            "runs_hashes_unchanged": bool(self.flags["files"]),
        }

    def interference_checks(self, prefix) -> list:
        return [
            {"name": f"{prefix}.{label}", "passed": bool(passed), "detail": "non-interference"}
            for label, passed in (
                ("parameters_unchanged", self.flags["parameters"]),
                ("grads_none", self.flags["grads"]),
                ("optimizer_not_built", self.flags["optimizer"]),
                ("checkpoint_writes", self.writes() == 0),
                ("runs_hashes_unchanged", self.flags["files"]),
            )
        ]


def _payload(experiment, plain, session, identity, results, reading, checks, command, data_root):
    from pinn.verification.evidence_io import redacted_command, ru_maxrss_bytes
    from pinn.verification.feasibility_scorecard import SCORECARD_SHA256

    diag07_common.assert_module_provenance(
        session.args.code_root, diag07_common.REPO_ROOT, identity["overlay_modules"],
    )
    failed = [item["name"] for item in checks if not item["passed"]]
    if failed:
        plain += " A pre-registered check failed, so this run is not accepted."
    return {
        "schema": "phase59-diag07-result/v1",
        "experiment": experiment,
        "plain_language": plain,
        "command": redacted_command(command, data_root=data_root),
        "code_identity": identity,
        "runtimes": [list(RUNTIME)],
        "checkpoints": list(session.checkpoints),
        "scorecard_sha256": SCORECARD_SHA256,
        "results": results,
        "reading": reading,
        "tolerance_checks": checks,
        "memory": {"ru_maxrss_bytes": ru_maxrss_bytes()},
        "non_interference": session.non_interference(),
        "files_opened": session.sources["attestation"].summary(),
        "producer_sha256": diag07_common.producer_hashes(Path(__file__).resolve()),
        "normalizer": session.sources["normalizer"],
    }, failed


def _run_jx5(session, identity, evidence_root, data_root, command):
    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME

    rules = session.scorecard.section("diag07")["jx5"]
    controller = session.controller
    dtype, device = controller._dtype, controller._device
    session.load(str(rules["checkpoint"]))
    anchor_key = session.monitor_anchor()
    anchor_ctx = controller._build_anchor_context(
        controller._train_source, controller._front_monitor_batch, None,
    )
    print(f"jx5 anchor {anchor_key.id} rows {anchor_ctx.collocation_times.shape[0]}", file=sys.stderr)
    components = _component_rows(controller, anchor_ctx)
    bins = _bins(controller, anchor_ctx)
    errors = ic_errors(anchor_ctx, dtype=dtype, device=device)
    rows = subset_rows(anchor_ctx.collocation_times.shape[0])
    u_rows = anchor_ctx.collocation_times[rows] / T_CHARACTERISTIC_TIME
    record = controller._train_source.get(anchor_key)
    with torch.no_grad():
        mixed = mixed_derivative_norms(
            controller.model, record.ic13, record.masses, u_rows, dtype=dtype, device=device,
        )
        branches = branch_scales(controller.model, record.ic13, u_rows, dtype=dtype, device=device)
    controller._release_chunk_memory()
    session.release()
    checks = [{
        "name": "jx5.monitor_anchor",
        "passed": int(anchor_key.id) == EXPECTED_MONITOR_ANCHOR,
        "detail": f"{anchor_key.id} vs {EXPECTED_MONITOR_ANCHOR}",
    }]
    checks.extend(session.interference_checks("jx5"))
    results = {
        "anchor": _key_json(anchor_key),
        "expected_anchor_id": EXPECTED_MONITOR_ANCHOR,
        "n_times": int(anchor_ctx.collocation_times.shape[0]),
        "row_norms": components,
        "rbar_bins": bins,
        "ic_errors": errors,
        "subset": {
            "rule": str(rules["subset"]),
            "n_rows": int(rows.size),
            "mixed_derivative_dv_d_ic13_norm": _summary(mixed),
            "mixed_derivative_dv_d_ic13_norm_per_row": [float(value) for value in mixed],
            "branch_scales": branches,
        },
    }
    worst = max(branches, key=lambda row: row["skip_du_rms"])
    plain = (
        "JX-5 recorded, at initialization and on the frozen monitor's trajectory, "
        "how large each quantity in the physics residual is. The network's "
        f"acceleration a' has an RMS of {components['a_prime']['rms']:.3e} against a "
        f"softened force of {components['force']['rms']:.3e}, so the residual's RMS is "
        f"{components['residual']['rms']:.3e}. The IC position and velocity errors are "
        f"{errors['position_error_norm']:.3e} and {errors['velocity_error_norm']:.3e}. "
        "Among the six skip blocks, the largest du-derivative of the skip branch is "
        f"{worst['skip_du_rms']:.3e} at hidden layer {worst['layer_number']} "
        f"(SIREN branch {worst['siren_du_rms']:.3e}). This is structural evidence "
        "only and is not a decision input (R-2)."
    )
    reading = {
        "question": "Where does the derivative scale come from at initialization?",
        "supports": "structural evidence only (R-2)",
        "falsifies": "none (descriptive)",
        "outcome": "recorded",
    }
    payload, failed = _payload(
        "JX-5", plain, session, identity, results, reading, checks, command, data_root,
    )
    diag07_common.write_result(evidence_root, "jx05.json", payload, data_root=data_root)
    return failed


_STEP_FILES = {
    0: "stage-0-init.pt",
    900: "best.pt",
    931: "step-000931.pt",
    941: "step-000941.pt",
    951: "step-000951.pt",
}
_PANELS_REL = Path(".planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json")


def _checkpoint_files(scorecard, steps) -> dict:
    """Map each frozen step to its file (D-29: 951 is step-000951.pt)."""
    registry = scorecard.section("diag07")["checkpoints"][diag07_common.SEED42]
    files = {}
    for step in steps:
        name = _STEP_FILES.get(int(step))
        if name is None or int(registry[name]) != int(step):
            raise ToleranceFailure(f"no registered checkpoint for step {step}")
        files[int(step)] = name
    return files


def _stratified(seed):
    from pinn.verification.architecture_characterization_probe import stratified_collocation_times

    times, _bins = stratified_collocation_times(
        n_bins=16, per_bin=256, rng=np.random.default_rng(int(seed)),
    )
    return times


def _check_anchor(session, checks, prefix):
    key = session.monitor_anchor()
    checks.append({
        "name": f"{prefix}.monitor_anchor",
        "passed": int(key.id) == EXPECTED_MONITOR_ANCHOR,
        "detail": f"{key.id} vs {EXPECTED_MONITOR_ANCHOR}",
    })
    return key


def _run_jx2(session, identity, evidence_root, data_root, command):
    rules = session.scorecard.section("diag07")["jx2"]
    files = _checkpoint_files(session.scorecard, rules["checkpoints"])
    seeds = [int(rules["draw_seed_base"]) + k for k in range(int(rules["draws"]))]
    draw_times = [_stratified(seed) for seed in seeds]
    controller = session.controller
    checks = []
    per_step = {}
    for step, name in files.items():
        info = session.load(name)
        frozen = diag07_common.monitor_fields(controller)
        key = _check_anchor(session, checks, f"jx2.{step}")
        prefixes, fronts = [], []
        for seed, times in zip(seeds, draw_times):
            ctx = fixture_anchor_context(controller, controller._train_source, key, times)
            profile = prefix_profile(controller, ctx)
            prefixes.append(profile["prefix"])
            fronts.append(profile["front_idx"])
            del ctx
            print(f"jx2 step {step} seed {seed} front {profile['front_idx']}", file=sys.stderr, flush=True)
        session.release()
        per_step[step] = {
            "file": name,
            "global_step": int(info["global_step"]),
            "frozen_front_idx": int(frozen["front_idx"]),
            "frozen_prefix": frozen["prefix"],
            "draw_seeds": seeds,
            "draw_prefixes": prefixes,
            "draw_front_idx": fronts,
        }
    statistic_bin = max(per_step[900]["frozen_front_idx"], per_step[951]["frozen_front_idx"])
    if statistic_bin < 0:
        raise ToleranceFailure("JX-2 statistic bin is undefined: both frozen fronts are -1")
    for record in per_step.values():
        values = [prefix[statistic_bin + 1] for prefix in record["draw_prefixes"]]
        counts = {}
        for front in record["draw_front_idx"]:
            counts[str(front)] = counts.get(str(front), 0) + 1
        record["frozen_statistic"] = float(record["frozen_prefix"][statistic_bin + 1])
        record["draws"] = {
            "values": [float(value) for value in values],
            "min": float(np.min(values)),
            "median": float(np.median(values)),
            "max": float(np.max(values)),
            "std": float(np.std(values)),
            "range": float(np.max(values) - np.min(values)),
            "front_idx_counts": dict(sorted(counts.items(), key=lambda item: int(item[0]))),
        }
    change = abs(per_step[951]["frozen_statistic"] - per_step[900]["frozen_statistic"])
    outcome = jx2_reading(
        per_step[900]["frozen_statistic"], per_step[951]["frozen_statistic"],
        per_step[900]["draws"]["values"], per_step[951]["draws"]["values"],
    )
    checks.extend(session.interference_checks("jx2"))
    results = {
        "trajectory": _key_json(key),
        "statistic": str(rules["statistic"]),
        "statistic_bin": int(statistic_bin),
        "frozen_change_900_to_951": float(change),
        "checkpoints": {str(step): record for step, record in per_step.items()},
    }
    plain = (
        "JX-2 asked whether the run's progress monitor moved between steps 900 and "
        "951 by more than its own sampling noise. On the monitor's own trajectory, "
        f"the prefix through bin {statistic_bin} changed by {change:.3e}, while 20 "
        "fresh draws of collocation times spread it over "
        f"{per_step[900]['draws']['range']:.3e} at step 900 and "
        f"{per_step[951]['draws']['range']:.3e} at step 951. Reading: {outcome}."
    )
    reading = {
        "question": "Is the monitor's movement from step 900 to 951 larger than its own estimator noise?",
        "supports": "parameter motion (J1.c, J5.a)",
        "falsifies": "parameter motion (J1.c, J5.a)",
        "outcome": outcome,
        "rule": str(rules["parameter_motion_if"]),
    }
    payload, failed = _payload(
        "JX-2", plain, session, identity, results, reading, checks, command, data_root,
    )
    diag07_common.write_result(evidence_root, "jx02.json", payload, data_root=data_root)
    return failed


def _run_jx4(session, identity, evidence_root, data_root, command):
    import hashlib
    import json

    import torch
    from pinn.constants import T_CHARACTERISTIC_TIME
    from pinn.data.types import RecordKey
    from pinn.verification.feasibility_scorecard import SCORECARD_SHA256
    from pinn.verification.production_reference import load_reference

    rules = session.scorecard.section("diag07")["jx4"]
    files = _checkpoint_files(session.scorecard, rules["checkpoints"])
    panels_path = diag07_common.REPO_ROOT / _PANELS_REL
    panels_bytes = panels_path.read_bytes()
    panels = json.loads(panels_bytes.decode("utf-8"))
    if panels.get("scorecard_sha256") != SCORECARD_SHA256:
        raise ToleranceFailure("panels.json scorecard_sha256 is not the frozen scorecard")
    singles = {int(row["percentile"]): int(row["id"]) for row in panels["singles"]}
    controller = session.controller
    dtype, device = controller._dtype, controller._device
    times = _stratified(rules["draw_seed"])
    checks = []
    fixtures = None
    references = {}
    rows = {}
    monitor = {}
    for step, name in files.items():
        session.load(name)
        anchor = _check_anchor(session, checks, f"jx4.{step}")
        if fixtures is None:
            fixtures = [
                ("panel_single_p10", RecordKey("hierarchical", "base", singles[10])),
                ("panel_single_p50", RecordKey("hierarchical", "base", singles[50])),
                ("panel_single_p90", RecordKey("hierarchical", "base", singles[90])),
                ("frozen_monitor_anchor", anchor),
            ]
            if [label for label, _key in fixtures] != list(rules["fixtures"]):
                raise ToleranceFailure("JX-4 fixture labels differ from the scorecard")
            for label, key in fixtures:
                gold = load_reference(
                    session.sources["reader"], RecordKey("hierarchical", "gold", int(key.id)),
                )
                keep = np.asarray(gold.times, dtype=np.float64) <= float(T_CHARACTERISTIC_TIME) + 1e-9
                references[label] = {
                    "times": np.asarray(gold.times, dtype=np.float64)[keep],
                    "positions": np.asarray(gold.positions, dtype=np.float64)[keep],
                    "inner_pair": tuple(gold.inner_pair),
                    "scale": physical_scale(gold),
                }
                del gold
        fields = diag07_common.monitor_fields(controller)
        monitor[step] = {
            "relative_front_idx": int(fields["front_idx"]),
            "raw_rbar": fields["raw_rbar"],
            "physical_front_idx": physical_front(
                fields["raw_rbar"], references["frozen_monitor_anchor"]["scale"],
                dtype=torch.float64, device=torch.device("cpu"),
            ),
        }
        for label, key in fixtures:
            reference = references[label]
            ctx = fixture_anchor_context(controller, controller._train_source, key, times)
            profile = prefix_profile(controller, ctx)
            errors = ic_errors(ctx, dtype=dtype, device=device)
            del ctx
            record = controller._train_source.get(key)
            score = network_score(
                controller.model, np.asarray(record.ic13, dtype=np.float64),
                np.asarray(record.masses, dtype=np.float64),
                reference["positions"], reference["inner_pair"], reference["times"],
                scorecard=session.scorecard, dtype=dtype, device=device, grid="gold",
            )
            controller._release_chunk_memory()
            rows.setdefault(label, {"record": _key_json(key), "physical_scale": reference["scale"]})
            rows[label][str(step)] = {
                "relative_front_idx": profile["front_idx"],
                "physical_front_idx": physical_front(
                    profile["raw_rbar"], reference["scale"],
                    dtype=torch.float64, device=torch.device("cpu"),
                ),
                "raw_rbar": profile["raw_rbar"],
                "rtilde": profile["rtilde"],
                "ic_errors": errors,
                "score": score.to_json_dict(),
            }
            print(
                f"jx4 step {step} {label} E {score.E:.3e} tier {score.tier} "
                f"front {profile['front_idx']}",
                file=sys.stderr, flush=True,
            )
        session.release()
    fixture_rows = [
        {
            "fixture": label,
            "tier_0": rows[label]["0"]["score"]["tier"],
            "tier_951": rows[label]["951"]["score"]["tier"],
            "E_0": rows[label]["0"]["score"]["E"],
            "E_951": rows[label]["951"]["score"]["E"],
        }
        for label, _key in fixtures
    ]
    front_0 = monitor[0]["relative_front_idx"]
    front_951 = monitor[951]["relative_front_idx"]
    outcome = jx4_reading(front_0, front_951, fixture_rows)
    checks.extend(session.interference_checks("jx4"))
    results = {
        "draw_seed": int(rules["draw_seed"]),
        "monitor": {str(step): value for step, value in monitor.items()},
        "fixtures": rows,
        "reading_inputs": {
            "front_0": front_0,
            "front_951": front_951,
            "fixture_rows": fixture_rows,
        },
    }
    tiers = ", ".join(f"{row['fixture']} tier {row['tier_951']}" for row in fixture_rows)
    plain = (
        "JX-4 compared the run's own relative progress signal with real orbit "
        f"accuracy. The monitor's front moved from {front_0} at step 0 to "
        f"{front_951} at step 951. At step 951 the fixtures score: {tiers}. "
        f"Reading: {outcome}. It informs the scale question of JD-3 only (R-2)."
    )
    reading = {
        "question": "Does the run's relative descent come with useful absolute accuracy?",
        "supports": "relative descent without useful accuracy",
        "falsifies": "useful accuracy with relative descent",
        "outcome": outcome,
        "informs": "JD-3 scale only",
    }
    payload, failed = _payload(
        "JX-4", plain, session, identity, results, reading, checks, command, data_root,
    )
    payload["panels_sha256"] = hashlib.sha256(panels_bytes).hexdigest()
    diag07_common.write_result(evidence_root, "jx04.json", payload, data_root=data_root)
    return failed


def main(argv=None) -> int:
    args = _parse(argv)
    command = list(sys.argv if argv is None else [sys.argv[0], *list(argv)])
    identity = diag07_common.bootstrap(args.code_root, diag07_common.REPO_ROOT)
    from pinn.verification.evidence_io import (
        FreezeNotEstablished,
        LaunchRefused,
        MemoryPreflightError,
        files_opened_record,
        provenance_record,
        write_json,
    )
    from pinn.verification.feasibility_scorecard import load_scorecard

    evidence_root = Path(args.evidence_root)
    evidence_root.mkdir(parents=True, exist_ok=True)
    data_root = Path(args.data_root)
    label, planned = _PLANNED[args.experiment]
    try:
        run_info = diag07_common.start_run(
            evidence_root, planned, label=label, command=command,
            required_bytes=6 * 1024 ** 3,
        )
    except FreezeNotEstablished as exc:
        print(f"DIAG07-FREEZE: {exc}")
        return 1
    except LaunchRefused as exc:
        text = str(exc)
        if not text.startswith("LAUNCH-REFUSED"):
            text = f"LAUNCH-REFUSED: {text}"
        print(text)
        return 6
    except MemoryPreflightError as exc:
        print(f"DIAG07-PREFLIGHT: {exc}")
        return 4
    try:
        scorecard = load_scorecard()
        sources = diag07_common.build_sources(
            diag07_common.REPO_ROOT, data_root, "explicit", scorecard,
        )
        session = _Session(args, sources, scorecard)
        runners = {"jx5": _run_jx5, "jx2": _run_jx2, "jx4": _run_jx4}
        order = ("jx5", "jx2", "jx4", "jx3")
        selected = order if args.experiment == "all" else (args.experiment,)
        failed = []
        for name in selected:
            if name not in runners:
                raise RuntimeError(f"{name} is not implemented yet")
            session.checkpoints = []
            failed.extend(runners[name](session, identity, evidence_root, data_root, command))
            gc.collect()
            if failed:
                break
        write_json(
            evidence_root / "files_opened_jx02_jx05.json",
            files_opened_record("jx02_jx05.py", sources["attestation"].summary()),
            data_root=data_root,
        )
        record = provenance_record(
            "jx02_jx05.py",
            command,
            data_root=data_root,
            data_root_source="explicit",
            utc_started=run_info["utc_started"],
            monotonic_started=run_info["monotonic_started"],
        )
        write_json(evidence_root / "provenance_jx02_jx05.json", record, data_root=data_root)
        diag07_common.write_summary(evidence_root, data_root=data_root)
        if failed:
            diag07_common.fail_run(run_info, "DIAG07-TOLERANCE-FAIL: " + failed[0])
            print("DIAG07-TOLERANCE-FAIL: " + failed[0])
            return 3
        diag07_common.finish_run(
            evidence_root, label, planned, command=command, run_info=run_info,
        )
        return 0
    except ToleranceFailure as exc:
        diag07_common.fail_run(run_info, f"DIAG07-TOLERANCE-FAIL: {exc}")
        print(f"DIAG07-TOLERANCE-FAIL: {exc}")
        return 3
    except Exception as exc:
        diag07_common.fail_run(run_info, f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    sys.exit(main())
