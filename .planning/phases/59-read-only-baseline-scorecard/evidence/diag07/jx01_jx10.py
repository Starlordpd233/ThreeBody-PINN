"""Phase 59 DIAG-07: JX-10 and the executed half of JX-1 on generation 7.

Bootstrap runs before any pinn import. Checkpoint monitor hashes are raw
float32 bytes, so a float64 runtime loads at float32 and is promoted after
the trainer's own restore checks.
"""

from __future__ import annotations

import argparse
import gc
import sys
from decimal import Decimal
from pathlib import Path

import diag07_common


class ToleranceFailure(RuntimeError):
    """A frozen DIAG-07 tolerance failed. The result is kept and not accepted."""


def _parse(argv):
    parser = argparse.ArgumentParser(description="Read-only JX-10 and JX-1.")
    parser.add_argument("--code-root", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument(
        "--experiment", choices=("jx10", "jx1", "all"), default="all",
    )
    parser.add_argument("--runtimes", default="mps,cpu")
    parser.add_argument(
        "--evidence-root",
        default=str(Path(__file__).resolve().parent),
    )
    return parser.parse_args(argv)


def _runtime_pairs(spec: str):
    mapping = {"mps": ("float32", "mps"), "cpu": ("float64", "cpu")}
    pairs = []
    for name in spec.split(","):
        key = name.strip()
        if not key:
            continue
        if key not in mapping:
            raise RuntimeError(f"unknown runtime {key}")
        pairs.append((key, mapping[key]))
    return pairs


def _planned(experiment: str):
    if experiment == "jx10":
        return "jx10", ["jx10.json"]
    if experiment == "jx1":
        return "jx01", ["jx01.json", "g1.json"]
    return "jx01_jx10", ["jx10.json", "jx01.json", "g1.json"]


def _promote(controller, dtype, device) -> None:
    import torch
    from pinn.data.types import DataFidelityPoints, FixedBatch, PhysicsCollocationPoints

    controller._model.to(dtype=dtype, device=device)
    controller._dtype = dtype
    controller._device = device
    batch = controller._front_monitor_batch
    if batch is None:
        return

    def cast(value):
        if torch.is_tensor(value) and value.is_floating_point():
            return value.detach().to(dtype=dtype, device=device)
        return value

    data = batch.data_points
    collocation = batch.collocation_points
    controller._front_monitor_batch = FixedBatch(
        data_points=DataFidelityPoints(
            tau_ic13=cast(data.tau_ic13),
            masses=cast(data.masses),
            targets=cast(data.targets),
            times=cast(data.times),
            record_keys=data.record_keys,
            snapshot_indices=data.snapshot_indices,
            sampling_kinds=data.sampling_kinds,
        ),
        collocation_points=PhysicsCollocationPoints(
            times=cast(collocation.times),
            tau_ic13=cast(collocation.tau_ic13),
            masses=cast(collocation.masses),
            record_keys=collocation.record_keys,
        ),
        replay_keys=batch.replay_keys,
        lookahead_keys=batch.lookahead_keys,
    )


def _load_into(controller, payload, pair) -> None:
    import torch

    precision, device_name = pair
    if precision == "float64":
        controller._model.to(dtype=torch.float32, device=torch.device("cpu"))
        controller._dtype = torch.float32
        controller._device = torch.device("cpu")
        controller.load_state_dict(payload)
        _promote(controller, torch.float64, torch.device("cpu"))
        return
    controller.load_state_dict(payload)


def _grads_clear(model) -> bool:
    clear = True
    for parameter in model.parameters():
        if parameter.grad is not None:
            clear = False
            parameter.grad = None
    return clear


def _relative_ok(actual, expected, rel) -> bool:
    actual = float(actual)
    expected = float(expected)
    scale = abs(expected)
    if scale == 0.0:
        return abs(actual) <= float(rel)
    return abs(actual - expected) <= float(rel) * scale


def _rounded_within(actual, expected, bound) -> bool:
    """GAP-59-11: compare 4-decimal copies in exact decimal units.

    The repr of a float is its shortest decimal string, so Decimal(repr(x))
    recovers the rounded value. Doubles cannot hold 2.0539 or 2.0538 exactly,
    so their binary difference can land a hair over 1e-4 when the decimal
    difference is exactly one step. The bound is inclusive: one step passes
    and two fail.
    """
    gap = abs(Decimal(repr(float(actual))) - Decimal(repr(float(expected))))
    return gap <= Decimal(repr(float(bound)))


def _checkpoint_names(scorecard):
    diag = scorecard.section("diag07")
    seed_files = [str(name) for name in diag["jx10"]["seed42_reproduction"]]
    smoke_by_step = {
        int(step): name
        for name, step in diag["checkpoints"][diag07_common.SMOKE].items()
    }
    smoke_files = []
    for step in diag["jx10"]["smoke_checkpoints"]:
        smoke_files.append(str(smoke_by_step[int(step)]))
    return seed_files, smoke_files


def _measure_run(controller, repo_root, run, names, scorecard, pair, checks, flags):
    rows = {}
    provenance = []
    for name in names:
        path = repo_root / "runs" / run / "checkpoints" / name
        before = diag07_common.file_hashes([path])
        payload, info = diag07_common.load_registry_checkpoint(
            repo_root, run, name, scorecard=scorecard,
        )
        _load_into(controller, payload, pair)
        fingerprints = diag07_common.param_fingerprints(controller.model)
        fields = diag07_common.monitor_fields(controller)
        unchanged = fingerprints == diag07_common.param_fingerprints(controller.model)
        grads_none = _grads_clear(controller.model)
        after = diag07_common.file_hashes([path])
        flags["parameters"] &= unchanged
        flags["grads"] &= grads_none
        flags["files"] &= before == after
        flags["optimizer"] &= controller._optimizer is None
        rows[name] = fields
        provenance.append(info)
        print(f"{run} {name} front {fields['front_idx']}", file=sys.stderr)
    return rows, provenance


def _compare_packet(rows, scorecard, checks) -> bool:
    diag = scorecard.section("diag07")
    tolerances = diag["tolerances"]
    packet = diag["jx10"]["phase58_packet"]
    supports = True
    rounded_abs = float(tolerances["phase58_packet_rounded_abs"])
    raw_rel = float(tolerances["phase58_packet_raw_rbar_bin0_rel"])
    if tolerances["phase58_packet_front_idx"] != "exact":
        raise RuntimeError("phase58 front tolerance is not exact")
    for name, expected in packet.items():
        fields = rows[name]
        front_ok = int(fields["front_idx"]) == int(expected["front_idx"])
        checks.append({
            "name": f"phase58.{name}.front_idx",
            "passed": front_ok,
            "detail": f"{fields['front_idx']} vs {expected['front_idx']}",
        })
        supports &= front_ok
        for key in (
            "prefix_through_front",
            "prefix_to_cross_next",
            "rtilde_median_all_bins",
        ):
            actual = fields["rounded"][key]
            ok = _rounded_within(actual, expected[key], rounded_abs)
            checks.append({
                "name": f"phase58.{name}.{key}",
                "passed": ok,
                "detail": f"{actual} vs {expected[key]}",
            })
            supports &= ok
        actual_bins = fields["rounded"]["rtilde_bins_0_5"]
        bins_ok = len(actual_bins) == len(expected["rtilde_bins_0_5"]) and all(
            _rounded_within(got, want, rounded_abs)
            for got, want in zip(actual_bins, expected["rtilde_bins_0_5"])
        )
        checks.append({
            "name": f"phase58.{name}.rtilde_bins_0_5",
            "passed": bins_ok,
            "detail": "rounded absolute tolerance",
        })
        supports &= bins_ok
        raw_ok = _relative_ok(
            fields["raw_rbar_bin0"], expected["raw_rbar_bin0"], raw_rel,
        )
        checks.append({
            "name": f"phase58.{name}.raw_rbar_bin0",
            "passed": raw_ok,
            "detail": "relative tolerance",
        })
        supports &= raw_ok
    return supports


def _compare_smoke(rows, scorecard, checks) -> bool:
    expected = int(scorecard.section("diag07")["jx10"]["smoke_expected_front"])
    supports = True
    for name, fields in rows.items():
        ok = int(fields["front_idx"]) == expected
        checks.append({
            "name": f"smoke.{name}.front_idx",
            "passed": ok,
            "detail": f"{fields['front_idx']} vs {expected}",
        })
        supports &= ok
    return supports


def _compare_cpu(mps_rows, cpu_rows, scorecard, checks, label) -> None:
    tolerances = scorecard.section("diag07")["tolerances"]
    if tolerances["cpu_vs_mps_front_idx"] != "exact":
        raise RuntimeError("cpu front tolerance is not exact")
    rel = float(tolerances["cpu_vs_mps_rtilde_and_prefix_rel"])
    for name, cpu_fields in cpu_rows.items():
        mps_fields = mps_rows[name]
        front_ok = int(cpu_fields["front_idx"]) == int(mps_fields["front_idx"])
        checks.append({
            "name": f"{label}.{name}.cpu_front",
            "passed": front_ok,
            "detail": f"{cpu_fields['front_idx']} vs {mps_fields['front_idx']}",
        })
        vector_ok = True
        for key in ("rtilde", "prefix"):
            left = cpu_fields[key]
            right = mps_fields[key]
            if len(left) != len(right) or any(
                not _relative_ok(got, want, rel) for got, want in zip(left, right)
            ):
                vector_ok = False
        checks.append({
            "name": f"{label}.{name}.cpu_rtilde_prefix",
            "passed": vector_ok,
            "detail": "relative tolerance",
        })


def _json_fields(fields) -> dict:
    return {
        "front_idx": fields["front_idx"],
        "rtilde": fields["rtilde"],
        "raw_rbar": fields["raw_rbar"],
        "prefix": fields["prefix"],
        "prefix_through_front": fields["prefix_through_front"],
        "prefix_to_cross_next": fields["prefix_to_cross_next"],
        "rtilde_bins_0_5": fields["rtilde_bins_0_5"],
        "raw_rbar_bin0": fields["raw_rbar_bin0"],
        "rtilde_median_all_bins": fields["rtilde_median_all_bins"],
        "w_min": fields["w_min"],
        "w_mean": fields["w_mean"],
        "w_max": fields["w_max"],
        "rounded": fields["rounded"],
    }


def _run_jx10(args, identity, sources, scorecard, evidence_root, data_root, command):
    from pinn.verification.evidence_io import redacted_command, ru_maxrss_bytes
    from pinn.verification.feasibility_scorecard import SCORECARD_SHA256

    seed_files, smoke_files = _checkpoint_names(scorecard)
    results = {}
    checkpoints = []
    checks = []
    flags = {"parameters": True, "grads": True, "files": True, "optimizer": True}
    writes = 0
    for key, pair in _runtime_pairs(args.runtimes):
        seed = diag07_common.build_controller(
            args.code_root, diag07_common.REPO_ROOT, diag07_common.SEED42,
            sources, pair,
        )
        smoke = diag07_common.build_controller(
            args.code_root, diag07_common.REPO_ROOT, diag07_common.SMOKE,
            sources, pair,
        )
        seed_rows, seed_info = _measure_run(
            seed, diag07_common.REPO_ROOT, diag07_common.SEED42, seed_files,
            scorecard, pair, checks, flags,
        )
        smoke_rows, smoke_info = _measure_run(
            smoke, diag07_common.REPO_ROOT, diag07_common.SMOKE, smoke_files,
            scorecard, pair, checks, flags,
        )
        writes += seed._checkpoint_store.write_attempts
        writes += smoke._checkpoint_store.write_attempts
        results[key] = {
            diag07_common.SEED42: {name: _json_fields(fields) for name, fields in seed_rows.items()},
            diag07_common.SMOKE: {name: _json_fields(fields) for name, fields in smoke_rows.items()},
        }
        if key == "mps":
            checkpoints.extend(seed_info)
            checkpoints.extend(smoke_info)
            mps_seed, mps_smoke = seed_rows, smoke_rows
        else:
            _compare_cpu(mps_seed, seed_rows, scorecard, checks, "seed42")
            _compare_cpu(mps_smoke, smoke_rows, scorecard, checks, "smoke")
        del seed, smoke
        gc.collect()
    if "mps" not in results:
        raise RuntimeError("JX-10 requires the mps runtime")
    supports = _compare_packet(
        results["mps"][diag07_common.SEED42], scorecard, checks,
    )
    supports = _compare_smoke(
        results["mps"][diag07_common.SMOKE], scorecard, checks,
    ) and supports
    for label, passed in (
        ("parameters_unchanged", flags["parameters"]),
        ("grads_none", flags["grads"]),
        ("optimizer_not_built", flags["optimizer"]),
        ("checkpoint_writes", writes == 0),
        ("runs_hashes_unchanged", flags["files"]),
    ):
        checks.append({"name": label, "passed": bool(passed), "detail": "non-interference"})
    outcome = "supports" if supports else "falsifies"
    if outcome == "supports":
        plain = (
            "The frozen monitor reproduces the recorded Phase 58 values, and "
            "the smoke front is 0 at steps 100, 200 and 300. That reading "
            "supports C-F14 and F-H2b."
        )
    else:
        plain = (
            "The frozen monitor does not reproduce the recorded Phase 58 "
            "values, or the smoke front is not 0 at steps 100, 200 and 300. "
            "That reading falsifies C-F14 and F-H2b."
        )
    failed = [item["name"] for item in checks if not item["passed"]]
    if failed:
        plain += " A frozen tolerance check failed, so this run is not accepted."
    diag07_common.assert_module_provenance(
        args.code_root, diag07_common.REPO_ROOT, identity["overlay_modules"],
    )
    payload = {
        "schema": "phase59-diag07-result/v1",
        "experiment": "JX-10",
        "plain_language": plain,
        "command": redacted_command(command, data_root=data_root),
        "code_identity": identity,
        "runtimes": [list(pair) for _key, pair in _runtime_pairs(args.runtimes)],
        "checkpoints": checkpoints,
        "scorecard_sha256": SCORECARD_SHA256,
        "results": results,
        "reading": {
            "question": (
                "Does the frozen monitor reproduce the recorded values, and "
                "was the smoke's step-93 front-1 transient (front 0 at steps "
                "100, 200, 300)?"
            ),
            "supports": "C-F14, F-H2b, C-07 numeric",
            "falsifies": "C-F14, F-H2b, C-07 numeric",
            "outcome": outcome,
        },
        "tolerance_checks": checks,
        "memory": {"ru_maxrss_bytes": ru_maxrss_bytes()},
        "non_interference": {
            "parameters_unchanged": bool(flags["parameters"]),
            "grads_none": bool(flags["grads"]),
            "optimizer_constructed": bool(flags["optimizer"]),
            "checkpoint_writes": int(writes),
            "runs_hashes_unchanged": bool(flags["files"]),
        },
        "files_opened": sources["attestation"].summary(),
        "producer_sha256": diag07_common.producer_hashes(Path(__file__).resolve()),
        "normalizer": sources["normalizer"],
    }
    diag07_common.write_result(
        evidence_root, "jx10.json", payload, data_root=data_root,
    )
    return outcome, failed


_TERMS = ("data", "ic", "phys", "energy", "angmom")
_LAMBDA = {
    "data": "lambda_data",
    "ic": "lambda_ic",
    "phys": "lambda_phys",
    "energy": "lambda_e",
    "angmom": "lambda_l",
}
# Plan 59-07: the primary shares of the five terms sum to 1 within 1e-6.
_PRIMARY_SUM_TOLERANCE = 1e-6


def _vector_norm(vector) -> float:
    import torch

    return float(torch.linalg.vector_norm(vector))


def _weight(weights, term) -> float:
    return float(getattr(weights, _LAMBDA[term]))


def _jx1_steps(scorecard):
    steps = [int(step) for step in scorecard.section("diag07")["jx1"]["checkpoints"]]
    files = {
        int(step): str(name)
        for step, name in scorecard.section("gate_g1")["checkpoint_files"].items()
    }
    missing = [step for step in steps if step not in files]
    if missing:
        raise RuntimeError(f"gate_g1.checkpoint_files has no file for steps {missing}")
    return steps, files


def _trainer_cross_check(controller, batch, anchor_ctx, weights, vectors, microbatch, rel):
    """Compare the driver's vectors with the trainer's own microbatched step.

    The trainer path is backward only. Its populated .grad is read and then set
    back to None, so no gradient survives the measurement.
    """
    import torch

    parameters = tuple(p for p in controller.model.parameters() if p.requires_grad)
    for parameter in parameters:
        parameter.grad = None
    terms, stats = controller._run_adam_step_microbatched(
        batch, anchor_ctx, weights, parameters,
        microbatch_size=microbatch, want_diagnostics=True,
    )
    populated = torch.cat([
        (parameter.grad if parameter.grad is not None else torch.zeros_like(parameter))
        .detach().reshape(-1).to(device="cpu", dtype=torch.float64)
        for parameter in parameters
    ])
    for parameter in parameters:
        parameter.grad = None
    norms = {}
    for term in _TERMS:
        driver = _vector_norm(vectors[term])
        trainer = float(stats[f"grad_norm_raw_{term}"])
        norms[term] = {
            "driver": driver,
            "trainer": trainer,
            "passed": _relative_ok(driver, trainer, rel),
        }
    difference = _vector_norm(populated - vectors["total_weighted"])
    reference = _vector_norm(populated)
    return {
        "norms": norms,
        "grad_difference_over_norm": difference / reference if reference else None,
        "grad_passed": difference <= float(rel) * reference,
        "losses": {
            name: float(getattr(terms, name))
            for name in ("data", "ic", "phys", "energy", "angmom", "total")
        },
    }


def _measure_jx1(controller, repo_root, steps, files, scorecard, pair, microbatch,
                 rel, label, checks, flags):
    from pinn.verification.feasibility_scorecard import jx1_reading

    diag = scorecard.section("diag07")
    records = {}
    provenance = []
    for step in steps:
        name = files[step]
        path = repo_root / "runs" / diag07_common.SEED42 / "checkpoints" / name
        before = diag07_common.file_hashes([path])
        payload, info = diag07_common.load_registry_checkpoint(
            repo_root, diag07_common.SEED42, name, scorecard=scorecard,
        )
        moments = None
        if payload.get("optimizer") is not None:
            moments = diag07_common.flatten_optimizer_state(payload, controller.model)
        _load_into(controller, payload, pair)
        global_step = int(payload["counters"]["global_step"])
        if global_step != step:
            raise RuntimeError(f"{name} global_step {global_step} != {step}")
        fingerprints = diag07_common.param_fingerprints(controller.model)
        batch = controller._front_monitor_batch
        anchor_ctx = controller._build_anchor_context(
            controller._train_source, batch, None,
        )
        weights = controller.scheduled_weights.current(global_step)
        vectors = diag07_common.per_term_gradients(
            controller, batch, anchor_ctx, weights, microbatch_size=microbatch,
        )
        flags["grads"] &= _grads_clear(controller.model)
        cross = _trainer_cross_check(
            controller, batch, anchor_ctx, weights, vectors, microbatch, rel,
        )
        raw = {term: _vector_norm(vectors[term]) for term in _TERMS}
        record = {
            "file": name,
            "global_step": global_step,
            "weights": {term: _weight(weights, term) for term in _TERMS},
            "grad_norm_raw": raw,
            "grad_norm_weighted": {term: _weight(weights, term) * raw[term] for term in _TERMS},
            "total_weighted_norm": _vector_norm(vectors["total_weighted"]),
            "cosines": {
                f"{left}_{right}": diag07_common.cosine(vectors[left], vectors[right])
                for left, right in diag["jx1"]["cosine_pairs"]
            },
            "ic_split": {
                "position_norm": _vector_norm(vectors["ic_position"]),
                "velocity_norm": _vector_norm(vectors["ic_velocity"]),
            },
            "trainer_cross_check": cross,
        }
        prefix = f"jx1.{label}.{step}"
        for term in _TERMS:
            checks.append({
                "name": f"{prefix}.{term}.driver_vs_trainer_norm",
                "passed": cross["norms"][term]["passed"],
                "detail": f"{cross['norms'][term]['driver']} vs {cross['norms'][term]['trainer']}",
            })
        checks.append({
            "name": f"{prefix}.driver_vs_trainer_grad",
            "passed": cross["grad_passed"],
            "detail": f"difference over norm {cross['grad_difference_over_norm']}",
        })
        if moments is None:
            record["shares"] = "not computable: no stored moments"
        else:
            exp_avg, exp_avg_sq, adam_step = moments
            beta1, beta2 = (float(value) for value in controller._config.opt.adam_betas)
            eps = float(controller._config.opt.adam_eps)
            weighted = {term: _weight(weights, term) * vectors[term] for term in _TERMS}
            shares = diag07_common.preconditioned_shares(
                weighted, vectors["total_weighted"], exp_avg, exp_avg_sq, adam_step,
                beta1=beta1, beta2=beta2, eps=eps,
            )
            group = payload["optimizer"]["param_groups"][0]
            record["shares"] = {
                "adam_step": adam_step,
                "beta1": beta1,
                "beta2": beta2,
                "eps": eps,
                "primary": shares["primary"],
                "secondary": shares["secondary"],
                "primary_sum": shares["primary_sum"],
                "reading": jx1_reading(shares["primary"]["phys"], scorecard=scorecard),
            }
            checks.append({
                "name": f"{prefix}.primary_sum",
                "passed": abs(shares["primary_sum"] - 1.0) <= _PRIMARY_SUM_TOLERANCE,
                "detail": f"{shares['primary_sum']}",
            })
            checks.append({
                "name": f"{prefix}.adam_hyperparameters_match_checkpoint",
                "passed": (
                    tuple(float(value) for value in group["betas"]) == (beta1, beta2)
                    and float(group["eps"]) == eps
                ),
                "detail": f"{tuple(group['betas'])} {group['eps']}",
            })
        flags["parameters"] &= fingerprints == diag07_common.param_fingerprints(controller.model)
        flags["grads"] &= _grads_clear(controller.model)
        flags["files"] &= before == diag07_common.file_hashes([path])
        flags["optimizer"] &= controller._optimizer is None
        records[step] = record
        provenance.append(info)
        del vectors
        print(
            f"{label} jx1 step {step} phys primary share "
            + (
                f"{record['shares']['primary']['phys']:.6e}"
                if isinstance(record["shares"], dict) else "n/a"
            ),
            file=sys.stderr,
        )
    return records, provenance


def _compare_jx1_cpu(mps_records, cpu_records, scorecard, checks) -> None:
    tolerances = scorecard.section("diag07")["tolerances"]
    norm_rel = float(tolerances["cpu_vs_mps_grad_norm_rel"])
    share_rel = float(tolerances["cpu_vs_mps_share_rel"])
    share_abs = float(tolerances["cpu_vs_mps_share_abs_floor"])
    for step, cpu in cpu_records.items():
        mps = mps_records[step]
        norms_ok = all(
            _relative_ok(cpu["grad_norm_raw"][term], mps["grad_norm_raw"][term], norm_rel)
            for term in _TERMS
        )
        checks.append({
            "name": f"jx1.cpu_vs_mps.{step}.grad_norms",
            "passed": norms_ok,
            "detail": "relative tolerance",
        })
        if isinstance(mps["shares"], dict):
            shares_ok = isinstance(cpu["shares"], dict) and all(
                abs(cpu["shares"][kind][term] - mps["shares"][kind][term])
                <= max(share_abs, share_rel * abs(mps["shares"][kind][term]))
                for kind in ("primary", "secondary")
                for term in _TERMS
            )
            checks.append({
                "name": f"jx1.cpu_vs_mps.{step}.shares",
                "passed": shares_ok,
                "detail": "relative or absolute-floor tolerance",
            })


def _jx1_plain(results_mps, gate_steps, readings) -> str:
    pieces = [
        f"at step {step} the physics term supplied "
        f"{results_mps[step]['shares']['primary']['phys']:.3e} of the "
        f"Adam-preconditioned update direction ({readings[str(step)]})"
        for step in gate_steps
    ]
    return (
        "JX-1 measured how strongly each part of the loss pushed generation 7's "
        "network and what share of the actual Adam update the physics term "
        "received: " + "; ".join(pieces) + ". At step 0 no Adam moments are "
        "stored, so no share is computable there. A share of 1e-4 or less reads "
        "as physics being a passenger, and 1e-2 or more reads that claim as "
        "overstated."
    )


def _g1_plain(gate, g1, shares) -> str:
    steps = [int(step) for step in gate["checkpoints"]]
    measured = " and ".join(f"{shares[step]:.3e} at step {step}" for step in steps)
    threshold = float(gate["threshold"])
    if g1["fires"] is None:
        return (
            f"Gate G1 is not determinable: a physics share was not finite. "
            f"Outcome: {g1['outcome']}."
        )
    if g1["fires"]:
        return (
            f"Gate G1 fired. The physics term supplied {measured} of the Adam update, "
            f"at or above the {threshold:g} threshold. Outcome: {g1['outcome']}. "
            "The conformance-first premise of Phase 61 is re-examined before "
            "Phase 61 opens. Phase 59 itself is unaffected."
        )
    return (
        f"Gate G1 did not fire. The physics term supplied {measured} of the Adam "
        f"update, below the {threshold:g} threshold at both checkpoints. "
        f"Outcome: {g1['outcome']}."
    )


def _run_jx1(args, identity, sources, scorecard, evidence_root, data_root, command):
    import hashlib

    from pinn.verification.evidence_io import redacted_command, ru_maxrss_bytes, write_json
    from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, g1_fires

    steps, files = _jx1_steps(scorecard)
    diag = scorecard.section("diag07")
    rel = float(diag["tolerances"]["driver_vs_trainer_grad_norm_rel"])
    microbatch = int(diag["microbatch_size"])
    results = {}
    checkpoints = []
    checks = []
    flags = {"parameters": True, "grads": True, "files": True, "optimizer": True}
    writes = 0
    for key, pair in _runtime_pairs(args.runtimes):
        controller = diag07_common.build_controller(
            args.code_root, diag07_common.REPO_ROOT, diag07_common.SEED42,
            sources, pair,
        )
        records, provenance = _measure_jx1(
            controller, diag07_common.REPO_ROOT, steps, files, scorecard, pair,
            microbatch, rel, key, checks, flags,
        )
        writes += controller._checkpoint_store.write_attempts
        results[key] = records
        if key == "mps":
            checkpoints.extend(provenance)
        del controller
        gc.collect()
    if "mps" not in results:
        raise RuntimeError("JX-1 requires the mps runtime")
    if "cpu" in results:
        _compare_jx1_cpu(results["mps"], results["cpu"], scorecard, checks)

    gate = scorecard.section("gate_g1")
    gate_steps = [int(step) for step in gate["checkpoints"]]
    mps_primary = {
        step: results["mps"][step]["shares"]["primary"]["phys"] for step in gate_steps
    }
    mps_g1 = g1_fires(mps_primary, scorecard=scorecard)
    checks.append({
        "name": "jx1.g1_determinable",
        "passed": mps_g1["fires"] is not None,
        "detail": str(mps_g1["outcome"]),
    })
    cpu_primary = None
    cpu_g1 = None
    if "cpu" in results:
        cpu_primary = {
            step: results["cpu"][step]["shares"]["primary"]["phys"] for step in gate_steps
        }
        cpu_g1 = g1_fires(cpu_primary, scorecard=scorecard)
        checks.append({
            "name": "jx1.g1_outcome_cpu_vs_mps",
            "passed": (
                cpu_g1["fires"] == mps_g1["fires"]
                and cpu_g1["outcome"] == mps_g1["outcome"]
            ),
            "detail": f"{cpu_g1['outcome']} vs {mps_g1['outcome']}",
        })
    for label, passed in (
        ("parameters_unchanged", flags["parameters"]),
        ("grads_none", flags["grads"]),
        ("optimizer_not_built", flags["optimizer"]),
        ("checkpoint_writes", writes == 0),
        ("runs_hashes_unchanged", flags["files"]),
    ):
        checks.append({"name": f"jx1.{label}", "passed": bool(passed), "detail": "non-interference"})
    failed = [item["name"] for item in checks if not item["passed"]]

    readings = {str(step): results["mps"][step]["shares"]["reading"] for step in gate_steps}
    plain = _jx1_plain(results["mps"], gate_steps, readings)
    if failed:
        plain += " A frozen tolerance check failed, so this run is not accepted."
    diag07_common.assert_module_provenance(
        args.code_root, diag07_common.REPO_ROOT, identity["overlay_modules"],
    )
    payload = {
        "schema": "phase59-diag07-result/v1",
        "experiment": "JX-1",
        "plain_language": plain,
        "command": redacted_command(command, data_root=data_root),
        "code_identity": identity,
        "runtimes": [list(pair) for _key, pair in _runtime_pairs(args.runtimes)],
        "checkpoints": checkpoints,
        "scorecard_sha256": SCORECARD_SHA256,
        "results": {
            key: {str(step): record for step, record in records.items()}
            for key, records in results.items()
        },
        "reading": {
            "question": "Was physics a passenger in generation 7's Adam update?",
            "supports": "PC-2 (physics was a passenger)",
            "falsifies": "PC-2",
            "outcome": "; ".join(f"{step}: {readings[str(step)]}" for step in gate_steps),
            "outcome_by_checkpoint": readings,
        },
        "tolerance_checks": checks,
        "memory": {"ru_maxrss_bytes": ru_maxrss_bytes()},
        "non_interference": {
            "parameters_unchanged": bool(flags["parameters"]),
            "grads_none": bool(flags["grads"]),
            "optimizer_constructed": bool(flags["optimizer"]),
            "checkpoint_writes": int(writes),
            "runs_hashes_unchanged": bool(flags["files"]),
        },
        "files_opened": sources["attestation"].summary(),
        "producer_sha256": diag07_common.producer_hashes(Path(__file__).resolve()),
        "normalizer": sources["normalizer"],
    }
    diag07_common.write_result(evidence_root, "jx01.json", payload, data_root=data_root)
    source_sha256 = hashlib.sha256((Path(evidence_root) / "jx01.json").read_bytes()).hexdigest()
    g1_plain = _g1_plain(gate, mps_g1, mps_primary)
    if failed:
        g1_plain += " A frozen tolerance check failed, so this run is not accepted."
    record = {
        "schema": "phase59-gate-g1/v1",
        "plain_language": g1_plain,
        "scorecard_sha256": SCORECARD_SHA256,
        "threshold": float(gate["threshold"]),
        "checkpoints": gate_steps,
        "primary_share": {str(step): mps_primary[step] for step in gate_steps},
        "secondary_share": {
            str(step): results["mps"][step]["shares"]["secondary"]["phys"]
            for step in gate_steps
        },
        "fires": mps_g1["fires"],
        "outcome": mps_g1["outcome"],
        "source_sha256": source_sha256,
        "producer_sha256": diag07_common.producer_hashes(Path(__file__).resolve()),
    }
    if cpu_g1 is not None:
        record["cpu_primary_share"] = {str(step): cpu_primary[step] for step in gate_steps}
        record["cpu_outcome"] = cpu_g1["outcome"]
    write_json(Path(evidence_root) / "g1.json", record, data_root=data_root)
    return failed


def main(argv=None) -> int:
    args = _parse(argv)
    command = list(sys.argv if argv is None else [sys.argv[0], *list(argv)])
    identity = diag07_common.bootstrap(
        args.code_root, diag07_common.REPO_ROOT,
    )
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
    label, planned = _planned(args.experiment)
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
        print(
            "normalizer "
            + str(sources["normalizer"]["source"])
            + " deviation "
            + str(sources["normalizer"]["deviation"]).lower(),
            file=sys.stderr,
        )
        failed = []
        if args.experiment in ("jx10", "all"):
            _outcome, failed_jx10 = _run_jx10(
                args, identity, sources, scorecard, evidence_root, data_root, command,
            )
            failed.extend(failed_jx10)
        if args.experiment in ("jx1", "all") and not failed:
            failed.extend(_run_jx1(
                args, identity, sources, scorecard, evidence_root, data_root, command,
            ))
        write_json(
            evidence_root / "files_opened_jx01_jx10.json",
            files_opened_record("jx01_jx10.py", sources["attestation"].summary()),
            data_root=data_root,
        )
        record = provenance_record(
            "jx01_jx10.py",
            command,
            data_root=data_root,
            data_root_source="explicit",
            utc_started=run_info["utc_started"],
            monotonic_started=run_info["monotonic_started"],
        )
        write_json(
            evidence_root / "provenance_jx01_jx10.json", record, data_root=data_root,
        )
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
