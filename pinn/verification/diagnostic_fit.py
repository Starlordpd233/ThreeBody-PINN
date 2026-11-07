"""Phase 65 (INST-08): the minute-scale diagnostic fit, score and record path.

``fit_diagnostic`` fits one named diagnostic variant on one already-loaded
Stage-0 training orbit with a constant-rate Adam policy — ``OptConfig``'s betas
and epsilon, the variant's learning rate, no physics term, no scheduler and no
polish — taking the existing data-only loss (INST-05's ``data_only_loss``)
directly, guarding the loss and gradients before every update, measuring the
shared time-signal similarity at a registered cadence (hooks and logging kept
outside the optimizer timing), scoring the fitted network with the frozen
FEAS-01 ``score_network``, recording the window-mean constant predictor (zero
velocities) and the two-Kepler comparison through the frozen
``score_trajectory`` on the same times and body order, and publishing one
canonical, exclusive record plus an intrinsically marked tensor payload.

Plan 65-06 adds the guarded real-data CLI around that core. A committed
fit registration (``phase65-fit-registration/v1``) is admitted through the
shared committed-registration gate BEFORE any data access or optimizer
construction; the admission also validates the bounded-run settings against
the sealed variant registry and requires a committed, run-commit-faithful
logger-parity receipt. The bounded run separates the first ``warmup_steps``
updates from the measured remainder, wraps every timing segment in the
existing MPS ``_synchronize`` helper with an injected monotonic clock, refuses
a requested whole-run cap at or above one hour, enforces the registered
whole-run deadline with a supervised worker and graceful termination, and
claims its output exclusively: repeated or parallel attempts refuse, and an
interrupted, over-cap or non-finite attempt stays explicitly incomplete and is
never published as a result.

The record and payload carry the ``inst08-diagnostic/v1`` identity
(``artifact_kind``/``diagnostic``/``counted``), variant identity and
configuration, seed, runtime, orbit/window identity, requested/warmup/measured
and completed steps, similarity cadence, synchronized timing basis, the full
frozen scorer output, comparison rows, the 33 pinned source hashes and the
reader's access counts. A bare state dict is never published as an INST-08
artifact. This module never calls the sealed Phase 60 entry points (``run_arm``,
``admit_arm``) or the real-corpus resolver; the real data path goes through
the Stage-0 training seam in ``diagnostic_data``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing
import os
import re
import signal
import subprocess
import sys
import time
from collections import OrderedDict
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.types import RecordKey
from pinn.training.atomic_io import atomic_write_torch
from pinn.training.config import OptConfig
from pinn.verification import evidence_io
from pinn.verification.diagnostic_data import (
    load_diagnostic_data,
    one_orbit_spec,
    open_diagnostic_context,
)
from pinn.verification.diagnostic_guard import (
    FIT_REGISTRATION_SCHEMA,
    REGISTRATION_SCHEMA,
    WEIGHTS_SCHEMA,
    DiagnosticRegistrationRefused,
    diagnostic_marker,
    read_diagnostic_record,
    read_diagnostic_weights,
    require_committed_registration,
)
from pinn.verification.diagnostic_phase66 import REGISTRIES
from pinn.verification.diagnostic_phase67 import (
    phase67_cadence,
    phase67_loss_trace_stride,
    phase67_score_cadence,
)
from pinn.verification.diagnostic_phase67_catalog import (
    PHASE67_REGISTRY_NAME,
    phase67_registry,
)
from pinn.verification.diagnostic_similarity import measure_time_signal
from pinn.verification.diagnostic_variants import (
    DiagnosticVariant,
    VariantRefused,
    build_variant,
    resolve_variant,
)
from pinn.verification.feasibility_scorecard import load_scorecard
from pinn.verification.feasibility_scorer import score_network, score_trajectory
from pinn.verification.learnability_arms import (
    SEED,
    FirstResultExists,
    write_record_exclusive,
)
from pinn.verification.learnability_losses import data_only_loss
from pinn.verification.learnability_protocol import PINNED_MODULES
from pinn.verification.learnability_run import _synchronize, weights_digest
from pinn.verification.two_kepler import NotApplicable, two_kepler_prediction

__all__ = [
    "ATTEMPT_SCHEMA",
    "DIAGNOSTIC_SCHEMA",
    "FIT_REGISTRATION_SCHEMA",
    "HOUR_SECONDS",
    "SMOKE_WEIGHTS_NAME",
    "TIMING_BASIS",
    "DiagnosticFitRefused",
    "check_fit_registration",
    "diagnostic_evidence_dir",
    "diagnostic_run_id",
    "fit_diagnostic",
    "load_fit_registration",
    "log_similarity",
    "main",
    "pinned_source_hashes",
    "require_committed_smoke_registration",
    "run_registered_smoke",
    "save_diagnostic_weights",
    "validate_smoke_settings",
    "verify_fit_result",
    "verify_logger_parity_receipt",
]

DIAGNOSTIC_SCHEMA = "inst08-diagnostic/v1"
RECORD_NAME = "record.json"
WEIGHTS_NAME = "weights.pt"
ATTEMPT_NAME = "attempt.json"
#: The CLI smoke run publishes its weights under the plan's declared name.
SMOKE_WEIGHTS_NAME = "diagnostic.weights"
ATTEMPT_SCHEMA = "phase65-fit-attempt/v1"
#: Any requested whole-run cap at or above one hour refuses before data access
#: until governed pause/resume and power compatibility is demonstrated (D-11).
HOUR_SECONDS = 3600.0
_RUN_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]*")

#: The measured wall time covers the constant-rate Adam steps only. Similarity
#: logging (hooks), frozen scoring, comparison predictors and artifact writes
#: are outside the measured window (D-11's timing basis).
TIMING_BASIS = (
    "optimizer steps only (constant-rate Adam); similarity logging, frozen "
    "scoring, comparisons and artifact writes excluded; monotonic clock"
)

#: The bounded run's basis: synchronized completed-work segments with an
#: explicit warmup/measured split (D-11). Formatted per run.
TIMING_BASIS_BOUNDED = (
    "optimizer steps only (constant-rate Adam), synchronized completed-work "
    "segments: the first {warmup} updates are warmup and the remaining "
    "{measured} provide the optimizer-rate measurement; similarity logging, "
    "frozen scoring, comparisons and artifact writes excluded; monotonic clock"
)
SECONDS_PER_STEP_BASIS = (
    "sum of the measured synchronized update durations divided by the "
    "{measured} measured steps; excludes the {warmup} warmup updates, "
    "similarity logging, scoring and artifact writes; a {measured}-step sample "
    "is not steady-state throughput for other configurations"
)

_DTYPES = {"float64": torch.float64, "float32": torch.float32}


class DiagnosticFitRefused(RuntimeError):
    """A diagnostic fit precondition does not hold; nothing runs or is published."""


def _resolve_runtime(runtime):
    """Map a named ``(dtype, device)`` pair to torch objects. No availability probe."""
    try:
        dtype_name, device_name = runtime
    except (TypeError, ValueError) as exc:
        raise DiagnosticFitRefused(
            f"runtime must be a (dtype, device) pair such as ('float64', 'cpu'); "
            f"got {runtime!r}"
        ) from exc
    if dtype_name not in _DTYPES:
        raise DiagnosticFitRefused(
            f"runtime dtype must be one of {sorted(_DTYPES)}; got {dtype_name!r}"
        )
    return _DTYPES[dtype_name], torch.device(device_name)


def pinned_source_hashes(*, repo_root=None):
    """The 33 pinned INST-05 module hashes, as the frozen protocol pins them.

    A pinned artifact that is missing is a refusal, not a regenerated baseline.
    """
    try:
        return dict(
            evidence_io.module_hashes(list(PINNED_MODULES), repo_root=repo_root)
        )
    except FileNotFoundError as exc:
        raise DiagnosticFitRefused(f"a pinned source artifact is missing: {exc}") from exc


def diagnostic_run_id(variant, data):
    """``<variant name>-<train record slug>``, a plain lowercase token."""
    key = data.records["train"]["record_key"]
    run_id = f"{variant.name}-{str(key).replace('/', '-')}"
    if _RUN_ID_RE.fullmatch(run_id) is None:
        raise DiagnosticFitRefused(
            f"the diagnostic run id must match [a-z0-9][a-z0-9-]*; got {run_id!r}"
        )
    return run_id


def diagnostic_evidence_dir(run_id, *, evidence_root):
    """``<evidence_root>/diagnostics/<run_id>``, refusing an id that could escape."""
    if not isinstance(run_id, str) or _RUN_ID_RE.fullmatch(run_id) is None:
        raise DiagnosticFitRefused(
            f"the diagnostic run id must match [a-z0-9][a-z0-9-]*; got {run_id!r}"
        )
    return Path(evidence_root) / "diagnostics" / run_id


def save_diagnostic_weights(path, model, *, variant, seed, runtime):
    """Save the CPU state dict inside the intrinsic diagnostic envelope.

    The payload is the marker block beside the plain ``state_dict``, so it
    loads with ``weights_only=True`` and can never be mistaken for a bare
    production state dict. Returns the file and tensor digests.
    """
    state = OrderedDict(
        (name, tensor.detach().cpu().clone())
        for name, tensor in model.state_dict().items()
    )
    payload = {
        **diagnostic_marker(schema=WEIGHTS_SCHEMA),
        "variant": variant.to_json_dict(),
        "seed": int(seed),
        "runtime": {"dtype": str(runtime[0]), "device": str(runtime[1])},
        "state_dict": state,
    }
    atomic_write_torch(path, payload)
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return {
        "file": Path(path).name,
        "sha256": digest,
        "tensor_digest": weights_digest(state),
        "schema": WEIGHTS_SCHEMA,
    }


def log_similarity(model, data_points, times_physical, *, step, point):
    """The fit logger's callable similarity entry.

    ``measure_time_signal`` is the sole measurement implementation: probe and
    logger share this one function (D-05), so the logger's trace is comparable
    with the DIAG-09 reproduction by construction.
    """
    measurement = measure_time_signal(
        model,
        data_points.tau_ic13,
        data_points.masses,
        data_points.targets,
        times_physical,
    )
    return {
        "step": int(step),
        "point": str(point),
        **measurement.to_json_dict(),
    }


# --------------------------------------------------------------------------
# Plan 65-06: the committed fit registration, its settings and the
# logger-parity receipt — all admitted before any data access.
# --------------------------------------------------------------------------


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _cites_registration_bytes(registration_file, root, cited):
    """True when the record cites this registration file's committed bytes.

    The citation must name the file's current on-disk sha256, or its exact
    bytes at a commit in HEAD's history — the as-captured citation of a run
    launched before a freeze-chain re-pin moved the live registration bytes
    (run evidence keeps its as-captured citations; each record's citation
    remains verifiable at its introducing commit). A digest that never
    existed at this path, or exists only uncommitted, is not a citation.
    """
    if not isinstance(cited, str):
        return False
    if cited == _sha256_file(registration_file):
        return True
    try:
        relative = registration_file.resolve().relative_to(
            Path(root).resolve()
        ).as_posix()
    except ValueError:
        return False
    probe = subprocess.run(
        ["git", "log", "--format=%H", "--", relative],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    if probe.returncode != 0:
        return False
    for commit in probe.stdout.splitlines():
        blob = subprocess.run(
            ["git", "show", f"{commit}:{relative}"],
            cwd=str(root), capture_output=True, check=False,
        )
        if blob.returncode == 0 and hashlib.sha256(blob.stdout).hexdigest() == cited:
            return True
    return False


def load_fit_registration(registration_path, *, repo_root=None):
    """Load and schema-check the fit registration document (read-only)."""
    path = Path(registration_path)
    if repo_root is not None and not path.is_absolute():
        path = Path(repo_root) / path
    if not path.is_file():
        raise DiagnosticFitRefused(f"the registration file is missing: {path.name}")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise DiagnosticFitRefused(f"the registration is not valid JSON: {exc}") from exc
    if not isinstance(doc, Mapping) or doc.get("schema") != FIT_REGISTRATION_SCHEMA:
        raise DiagnosticFitRefused(f"not a {FIT_REGISTRATION_SCHEMA} registration")
    return doc


def _parse_orbit_key(text):
    """``variant/fidelity/id`` to a structural ``RecordKey``; anything else refuses."""
    parts = str(text).split("/")
    if len(parts) != 3:
        raise DiagnosticFitRefused(
            f"the orbit key must be variant/fidelity/id; got {text!r}"
        )
    variant, fidelity, raw_id = parts
    try:
        record_id = int(raw_id)
    except ValueError as exc:
        raise DiagnosticFitRefused(
            f"the orbit key id must be an integer; got {raw_id!r}"
        ) from exc
    try:
        return RecordKey(variant, fidelity, record_id)
    except (TypeError, ValueError) as exc:
        raise DiagnosticFitRefused(
            f"the orbit key is not a record key: {text!r}"
        ) from exc


def _named_registry(name):
    """The registry a registration's ``variant_registry`` name selects.

    ``None`` — every Phase 65 registration — selects the sealed ``REGISTRY``
    object itself, so Phase 65 behaviour is unchanged. A string key of
    ``REGISTRIES`` selects that registry. ``phase67`` dispatches to the Phase
    67 catalog's registry through ``phase67_registry`` (a separate module, so
    the frozen Phase 66 catalog is never edited). Anything else refuses
    before any data access, optimizer construction or attempt claim.
    """
    if isinstance(name, str) and name in REGISTRIES:
        return REGISTRIES[name]
    try:
        return phase67_registry({"variant_registry": name})
    except VariantRefused as exc:
        raise DiagnosticFitRefused(
            f"unknown variant registry {name!r}; known registries: "
            f"{[*REGISTRIES, PHASE67_REGISTRY_NAME]}"
        ) from exc


def validate_smoke_settings(doc):
    """Validate the registration's settings block before any data access.

    The variant must be a registry entry with byte-agreeing fields, the
    runtime must be a named ``(dtype, device)`` pair whose device is actually
    available, the orbit key must parse structurally, the window must match
    the variant's, the step/warmup/measured counts and cadence must be
    mutually consistent, the whole-run cap must sit strictly below one hour,
    and the optimizer/loss policy must be the bounded smoke policy. Returns
    ``(settings, variant, orbit_key, (dtype, device))``.
    """
    settings = doc.get("settings")
    if not isinstance(settings, Mapping):
        raise DiagnosticFitRefused("the registration names no settings block")
    variant_block = settings.get("variant")
    if not isinstance(variant_block, Mapping) or not isinstance(variant_block.get("name"), str):
        raise DiagnosticFitRefused("the settings name no diagnostic variant")
    registry = _named_registry(settings.get("variant_registry"))
    variant_name = variant_block["name"]
    if variant_name not in registry:
        raise DiagnosticFitRefused(
            f"unknown diagnostic variant {variant_name!r}; registered: {list(registry)}"
        )
    variant = registry[variant_name]
    for field, value in variant.to_json_dict().items():
        if variant_block.get(field) != value:
            raise DiagnosticFitRefused(
                f"the registered variant field {field} is {value!r}; the settings "
                f"name {variant_block.get(field)!r}"
            )
    seed = settings.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise DiagnosticFitRefused(f"the settings seed must be an integer; got {seed!r}")
    runtime = settings.get("runtime")
    if not isinstance(runtime, Mapping) or runtime.get("dtype") not in _DTYPES \
            or runtime.get("device") not in ("cpu", "mps"):
        raise DiagnosticFitRefused(
            "the settings runtime must name a registered dtype and a cpu or mps device; "
            f"got {runtime!r}"
        )
    dtype, device = _resolve_runtime((runtime["dtype"], runtime["device"]))
    if device.type == "mps":
        mps_module = getattr(torch.backends, "mps", None)
        available = mps_module is not None and bool(torch.backends.mps.is_available())
        if not available:
            raise DiagnosticFitRefused(
                "the registration names the mps device, but MPS is not available "
                "on this machine; the registered smoke refuses rather than "
                "falling back to another device"
            )
    orbit_key = _parse_orbit_key(settings.get("orbit_key"))
    window = settings.get("physical_window")
    if not isinstance(window, Mapping):
        raise DiagnosticFitRefused("the settings name no physical window")
    if settings.get("variant_registry") == "phase67":
        # Phase 67 (65-CLOSEOUT IN-01's affected-use hardening): both window
        # endpoints must be finite numbers excluding booleans, and the start
        # exactly zero — never a boolean, numeric string, null or list that
        # merely survives a float coercion. Phase 65/66 registrations keep
        # their existing check byte-for-byte.
        for endpoint in ("t_start", "t_end"):
            value = window.get(endpoint)
            if isinstance(value, bool) or not isinstance(value, (int, float)) \
                    or not math.isfinite(float(value)):
                raise DiagnosticFitRefused(
                    f"the phase67 physical window {endpoint} must be a finite "
                    f"number excluding booleans; got {value!r}"
                )
        if float(window["t_start"]) != 0.0:
            raise DiagnosticFitRefused("the phase67 physical window must start at t = 0")
    elif float(window.get("t_start", float("nan"))) != 0.0:
        raise DiagnosticFitRefused("the physical window must start at t = 0")
    t_end = window.get("t_end")
    if isinstance(t_end, bool) or not isinstance(t_end, (int, float)) \
            or not math.isfinite(float(t_end)) or float(t_end) != float(variant.window_length):
        raise DiagnosticFitRefused(
            f"the physical window must end at the variant's window length "
            f"{variant.window_length!r}; got {t_end!r}"
        )
    steps = settings.get("optimizer_steps")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise DiagnosticFitRefused(
            f"the settings optimizer_steps must be a positive integer; got {steps!r}"
        )
    warmup = settings.get("warmup_steps")
    if isinstance(warmup, bool) or not isinstance(warmup, int) or not 0 <= warmup < steps:
        raise DiagnosticFitRefused(
            f"the settings warmup_steps must be an integer in [0, optimizer_steps); "
            f"got {warmup!r}"
        )
    if settings.get("measured_steps") != steps - warmup:
        raise DiagnosticFitRefused(
            f"the settings measured_steps must be optimizer_steps - warmup_steps "
            f"({steps - warmup}); got {settings.get('measured_steps')!r}"
        )
    cadence = settings.get("similarity_cadence")
    if not isinstance(cadence, list) or not cadence:
        raise DiagnosticFitRefused("the settings name no similarity cadence")
    if any(isinstance(c, bool) or not isinstance(c, int) for c in cadence):
        raise DiagnosticFitRefused("the similarity cadence must be a list of integers")
    if len(set(cadence)) != len(cadence) or cadence != sorted(cadence):
        raise DiagnosticFitRefused("the similarity cadence must be unique and in step order")
    if cadence[0] != 0 or cadence[-1] != steps:
        raise DiagnosticFitRefused(
            "the similarity cadence must start at step 0 and end at the final step"
        )
    if any(c < 0 or c > steps for c in cadence):
        raise DiagnosticFitRefused(
            "the similarity cadence steps must lie in [0, optimizer_steps]"
        )
    stride = settings.get("loss_trace_stride")
    if stride is not None and (
        isinstance(stride, bool) or not isinstance(stride, int)
        or not 1 <= stride <= steps
    ):
        raise DiagnosticFitRefused(
            "the loss-trace stride must be an integer from 1 to optimizer_steps"
        )
    # The Phase 67 checkpoint schedule (plan 67-04, D-08/D-10): a
    # registration that declares one must declare the exact registered
    # schedule — the five normalized similarity events, the three
    # frozen-score checkpoints and the bounded loss-trace stride — before
    # any data access or model construction. Older raw runs (any registry,
    # no score cadence) gain no new fields or events.
    score_cadence = settings.get("score_cadence")
    if score_cadence is not None:
        if settings.get("variant_registry") != PHASE67_REGISTRY_NAME:
            raise DiagnosticFitRefused(
                "score_cadence is a Phase 67 checkpoint-schedule setting; a "
                f"registration naming the {settings.get('variant_registry')!r} "
                "registry cannot declare it"
            )
        if not isinstance(score_cadence, list) or not score_cadence \
                or any(isinstance(c, bool) or not isinstance(c, int) for c in score_cadence):
            raise DiagnosticFitRefused(
                f"the score cadence must be a non-empty list of integers; got {score_cadence!r}"
            )
        try:
            expected_score = phase67_score_cadence(steps)
            expected_similarity = phase67_cadence(steps)
            expected_stride = phase67_loss_trace_stride(steps)
        except ValueError as exc:
            raise DiagnosticFitRefused(str(exc)) from exc
        if score_cadence != expected_score:
            raise DiagnosticFitRefused(
                "the registered score cadence must be the exact Phase 67 "
                f"schedule {expected_score} for {steps} steps; got {score_cadence!r}"
            )
        if cadence != expected_similarity:
            raise DiagnosticFitRefused(
                "a registration with a score cadence must declare the exact "
                f"normalized similarity schedule {expected_similarity} for "
                f"{steps} steps; got {cadence!r}"
            )
        if stride != expected_stride:
            raise DiagnosticFitRefused(
                "a registration with a score cadence must declare the bounded "
                f"loss-trace stride {expected_stride} for {steps} steps; got {stride!r}"
            )
    cap = settings.get("whole_run_cap_seconds")
    if isinstance(cap, bool) or not isinstance(cap, (int, float)) \
            or not math.isfinite(float(cap)) or not 0 < float(cap) < HOUR_SECONDS:
        raise DiagnosticFitRefused(
            f"the whole-run cap must be a finite number of seconds in "
            f"(0, {HOUR_SECONDS:.0f}); runs of an hour or more refuse until "
            f"governed pause/resume and power compatibility is demonstrated; "
            f"got {cap!r}"
        )
    optimizer = settings.get("optimizer")
    if not isinstance(optimizer, Mapping) or optimizer.get("kind") != "adam_constant_rate":
        raise DiagnosticFitRefused("the optimizer policy must be adam_constant_rate")
    if float(optimizer.get("lr", float("nan"))) != float(variant.learning_rate):
        raise DiagnosticFitRefused(
            "the optimizer policy rate must equal the variant's learning rate"
        )
    for key in ("scheduler", "clipping", "physics_term", "polish"):
        if optimizer.get(key) is not None:
            raise DiagnosticFitRefused(
                f"the bounded smoke policy must not set {key}; got {optimizer.get(key)!r}"
            )
    loss = settings.get("loss")
    if not isinstance(loss, Mapping) or loss.get("kind") != "data_only":
        raise DiagnosticFitRefused("the smoke loss policy must be data_only")
    if not settings.get("timing_definitions"):
        raise DiagnosticFitRefused("the settings name no timing definitions")
    reading_rule = settings.get("reading_rule")
    if not isinstance(reading_rule, Mapping):
        raise DiagnosticFitRefused("the settings name no reading rule")
    for key in ("mechanical_pass", "incomplete", "out_of_branch"):
        if not reading_rule.get(key):
            raise DiagnosticFitRefused(f"the reading rule names no {key} branch")
    return settings, variant, orbit_key, (dtype, device)


def _receipt_is_a_measurement(receipt):
    """A successful logger-parity receipt is an actual log_similarity entry.

    Two registered shapes admit (plan 67-06 task 2): the raw receipt, whose
    first-layer frequency carries finite median/max numbers, and the encoded
    receipt (the D-05 logger's truthful output), whose aggregate frequency is
    explicitly inapplicable — null median/max beside a false applicability
    flag, a reason, the pinned per-harmonic cycles, the harmonic list and the
    internal dimension. Anything else (a half-encoded hybrid, a manufactured
    applicability or a non-numeric frequency) refuses.
    """
    if not isinstance(receipt, Mapping):
        return False
    layers = receipt.get("layers")
    if not isinstance(layers, list) or not layers:
        return False
    for row in layers:
        if not isinstance(row, Mapping) or not isinstance(row.get("name"), str):
            return False
        value = row.get("adjacent_cosine_mean")
        if isinstance(value, bool) or not isinstance(value, (int, float)) \
                or not math.isfinite(float(value)):
            return False
    numbers = []
    frequency = receipt.get("first_layer_frequency")
    movement = receipt.get("output_movement")
    rate = receipt.get("output_rate_ratio")
    for block in (frequency, movement, rate):
        if not isinstance(block, Mapping):
            return False
    median, maximum = frequency.get("median"), frequency.get("max")
    raw_frequency = not any(
        value is None for value in (median, maximum)
    )
    if raw_frequency:
        numbers.extend((median, maximum))
    elif not (median is None and maximum is None):
        return False  # a half-null aggregate frequency is no registered shape
    numbers.extend((movement.get("value"), rate.get("value")))
    if any(isinstance(v, bool) or not isinstance(v, (int, float))
           or not math.isfinite(float(v)) for v in numbers):
        return False
    if not (isinstance(receipt.get("point"), str) and isinstance(receipt.get("step"), int)):
        return False
    # The raw receipt is complete at this point.
    if raw_frequency:
        return True
    # The encoded receipt: an explicitly inapplicable aggregate frequency
    # beside the encoder's pinned per-harmonic metadata.
    cycles = receipt.get("feature_frequency_cycles")
    harmonics = receipt.get("feature_harmonics")
    dimension = receipt.get("internal_input_dimension")
    if receipt.get("frequency_applicability") is not False:
        return False
    if not isinstance(receipt.get("frequency_reason"), str) \
            or not receipt["frequency_reason"]:
        return False
    if not isinstance(cycles, list) or not cycles \
            or any(isinstance(v, bool) or not isinstance(v, (int, float))
                   or not math.isfinite(float(v)) or float(v) <= 0.0
                   for v in cycles):
        return False
    if not isinstance(harmonics, list) or not harmonics \
            or any(isinstance(v, bool) or not isinstance(v, int)
                   for v in harmonics):
        return False
    if len(cycles) != len(harmonics):
        return False
    if isinstance(dimension, bool) or not isinstance(dimension, int):
        return False
    return dimension == 14 + 2 * len(harmonics)


def verify_logger_parity_receipt(doc, *, repo_root):
    """A successful committed receipt, faithful to its publication bytes.

    The D-10 receipt precedes any training trace: the registered receipt file
    must be a real ``log_similarity`` measurement, its recorded run commit
    must be an ancestor of HEAD, and its bytes at its own introducing commit
    must equal the committed bytes. (The receipt was materialized after the
    probe run from the run's own recorded logger entry — plan 65-05's
    receipt provenance — so its bytes exist only from that introducing commit
    onward; rewriting it afterwards is the tampering this check refuses.)
    The historical lead's reproduction branch is recorded in the registration
    and never required here: an independent fit runs regardless of the
    probe's verdict.
    """
    parity = doc.get("logger_parity")
    if not isinstance(parity, Mapping):
        raise DiagnosticFitRefused("the registration names no logger-parity receipt")
    receipt_entry = parity.get("receipt")
    if not isinstance(receipt_entry, Mapping) or not isinstance(receipt_entry.get("path"), str):
        raise DiagnosticFitRefused("the logger-parity receipt entry names no path")
    path = Path(repo_root) / receipt_entry["path"]
    if not path.is_file():
        raise DiagnosticFitRefused("the committed logger-parity receipt is missing")
    raw = path.read_bytes()
    try:
        receipt = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise DiagnosticFitRefused(
            f"the logger-parity receipt is not readable JSON: {exc}"
        ) from exc
    if not _receipt_is_a_measurement(receipt):
        raise DiagnosticFitRefused(
            "the committed logger-parity receipt is not a successful "
            "log_similarity measurement"
        )
    run_commit = parity.get("run_commit")
    if not isinstance(run_commit, str) or re.fullmatch(r"[0-9a-f]{40}", run_commit) is None:
        raise DiagnosticFitRefused(
            "the logger-parity receipt names no recorded 40-hex run commit"
        )

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(repo_root), capture_output=True, text=True, check=False
        )

    if git("merge-base", "--is-ancestor", run_commit, "HEAD").returncode != 0:
        raise DiagnosticFitRefused(
            f"the recorded logger-parity run commit {run_commit} is not an "
            "ancestor of HEAD"
        )
    introduced = git("log", "-n1", "--format=%H", "--diff-filter=A", "--", receipt_entry["path"])
    if introduced.returncode != 0 or not introduced.stdout.strip():
        raise DiagnosticFitRefused(
            "the logger-parity receipt has no introducing commit; it is not committed"
        )
    receipt_commit = introduced.stdout.strip().splitlines()[0]
    at_publication = git("show", f"{receipt_commit}:{receipt_entry['path']}")
    if at_publication.returncode != 0 or at_publication.stdout.encode("utf-8") != raw:
        raise DiagnosticFitRefused(
            "the committed logger-parity receipt differs from its bytes at its "
            f"introducing commit {receipt_commit}"
        )
    return receipt


def require_committed_smoke_registration(registration_path, *, repo_root=None):
    """Admit the committed-clean smoke registration BEFORE any data or optimizer.

    Runs the shared committed-registration admission (committed-clean
    artifacts with exact digests, a real ancestor introducing commit, and the
    pinned-protocol revalidation of the 33 frozen sources when present), then
    the fit-specific gates: the settings block against the sealed registry and
    the bounded-run rules, and the committed logger-parity receipt verified
    against its recorded run-commit bytes. Read-only: no corpus record is
    opened, no diagnostic weights are read and no attempt is claimed. Returns
    ``(repo_root, doc)``.
    """
    root = require_committed_registration(
        registration_path, repo_root=repo_root, weight_digests=False
    )
    doc = load_fit_registration(registration_path, repo_root=root)
    validate_smoke_settings(doc)
    verify_logger_parity_receipt(doc, repo_root=root)
    return root, doc


def _fit_artifact_paths(doc):
    """The registration's enumerated artifact paths, for the check report."""
    paths = []
    page = doc.get("page")
    if isinstance(page, Mapping):
        paths.append(page["path"])
    parity = doc.get("logger_parity")
    if isinstance(parity, Mapping) and isinstance(parity.get("receipt"), Mapping):
        paths.append(parity["receipt"]["path"])
    context = doc.get("context")
    if isinstance(context, Mapping) and isinstance(context.get("probe_result"), Mapping):
        paths.append(context["probe_result"]["path"])
    for entry in doc.get("code_dependencies") or []:
        if isinstance(entry, Mapping):
            paths.append(entry["path"])
    for entry in doc.get("frozen") or []:
        if isinstance(entry, Mapping):
            paths.append(entry["path"])
    return paths


def check_fit_registration(registration_path, *, repo_root=None):
    """Read-only committed-identity report — no corpus opens, no weight reads.

    Metadata-only: the shared committed-registration admission in its
    weight-deferred mode, the introducing commit (which must be an ancestor of
    HEAD) and the on-disk digests of the enumerated artifacts.
    """
    root = require_committed_registration(
        registration_path, repo_root=repo_root, weight_digests=False
    )
    path = Path(registration_path)
    if not path.is_absolute():
        path = root / path
    relative = path.resolve().relative_to(root).as_posix()
    doc = load_fit_registration(path, repo_root=root)
    probe = subprocess.run(
        ["git", "log", "-n1", "--format=%H", "--diff-filter=A", "--", relative],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    if probe.returncode != 0 or not probe.stdout.strip():
        raise DiagnosticFitRefused("the registration file has no introducing commit")
    commit = probe.stdout.strip().splitlines()[0]
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    if ancestor.returncode != 0:
        raise DiagnosticFitRefused(
            f"the registration commit {commit} is not an ancestor of HEAD"
        )
    artifacts = [
        {"path": artifact_path, "sha256": _sha256_file(root / artifact_path)}
        for artifact_path in _fit_artifact_paths(doc)
    ]
    artifacts.append({"path": relative, "sha256": _sha256_file(path)})
    return {
        "committed": True,
        "registration_commit": commit,
        "schema": doc["schema"],
        "artifacts": artifacts,
    }


def _validate_data_points(data_points):
    if data_points is None:
        raise DiagnosticFitRefused("the fit needs data points; got None")
    tau = getattr(data_points, "tau_ic13", None)
    masses = getattr(data_points, "masses", None)
    targets = getattr(data_points, "targets", None)
    if tau is None or masses is None or targets is None:
        raise DiagnosticFitRefused(
            "the fit needs tau_ic13, masses and targets; a field is None"
        )
    if not isinstance(tau, torch.Tensor) or tau.dim() != 2:
        raise DiagnosticFitRefused(
            f"tau_ic13 must be a 2-D tensor (N, 14); got {type(tau).__name__} "
            f"{tuple(getattr(tau, 'shape', ()))}"
        )
    count = int(tau.shape[0])
    if count < 2:
        raise DiagnosticFitRefused(
            f"at least two samples are needed for a diagnostic fit; got {count}"
        )


def _guarded_step(model, optimizer, data_points, *, dtype, device, step):
    """One constant-rate Adam step behind finiteness guards.

    A non-finite loss or gradient refuses before ``optimizer.step()`` — the
    diagnostic never updates on, or publishes, a non-finite quantity.
    """
    optimizer.zero_grad(set_to_none=True)
    loss = data_only_loss(model, data_points, dtype=dtype, device=device)
    value = float(loss)
    if not math.isfinite(value):
        raise DiagnosticFitRefused(
            f"the data-only loss is not finite before step {step}: {value!r}"
        )
    loss.backward()
    for parameter in model.parameters():
        if parameter.grad is not None and not bool(
            torch.isfinite(parameter.grad).all()
        ):
            raise DiagnosticFitRefused(
                f"a parameter gradient is not finite before step {step}; "
                "refusing the optimizer update"
            )
    optimizer.step()
    return float(loss.detach())


def _comparison_rows(data, *, scorecard):
    """The matched-window comparison rows through the frozen score_trajectory.

    Same times, same body order, same window as the network score. A formula
    ``NotApplicable`` result carries its existing reason; it never becomes a
    successful score.
    """
    view = data.score
    positions = np.asarray(view.positions, dtype=np.float64)
    times = np.asarray(view.times, dtype=np.float64)
    masses = np.asarray(data.masses, dtype=np.float64).reshape(3)
    inner_pair = tuple(int(slot) for slot in view.inner_pair)

    constant = np.broadcast_to(
        positions.mean(axis=0, keepdims=True), positions.shape
    ).copy()
    constant_score = score_trajectory(
        constant,
        np.zeros_like(constant),
        positions,
        masses,
        inner_pair,
        times,
        velocity_source="analytic",
        scorecard=scorecard,
        grid=view.grid,
    )
    constant_row = {
        "comparison": "window_mean_constant",
        "predictor": {
            "kind": "window_mean_constant",
            "velocities": "zero",
            "definition": "each body held at its time-mean position over the window",
        },
        "score": constant_score.to_json_dict(),
    }

    elapsed = (times - times[0]) / T_CHARACTERISTIC_TIME
    r0 = data.true_r0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    v0 = data.true_v0.detach().cpu().numpy().astype(np.float64).reshape(3, 3)
    try:
        predicted, predicted_v = two_kepler_prediction(r0, v0, masses, inner_pair, elapsed)
    except NotApplicable as exc:
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "not_applicable",
            "reason": exc.reason,
        }
    except RuntimeError as exc:
        # The frozen formula's own Newton solver failed on this window (its
        # message, verbatim). Like NotApplicable, it never becomes a score.
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": False,
            "failure": "solver_did_not_converge",
            "reason": str(exc),
        }
    else:
        kepler_score = score_trajectory(
            predicted,
            predicted_v,
            positions,
            masses,
            inner_pair,
            times,
            velocity_source="analytic",
            scorecard=scorecard,
            grid=view.grid,
        )
        kepler_row = {
            "comparison": "two_kepler",
            "applicable": True,
            "initial_state": "the train record's first in-window snapshot (true_r0, true_v0)",
            "score": kepler_score.to_json_dict(),
        }
    return [constant_row, kepler_row]


def _require_finite_checkpoint(score, *, step):
    """A recorded checkpoint must be a complete finite frozen score.

    The guard mirrors the loss guard: a checkpoint whose error columns are
    not all finite numbers is refused before it is recorded, and nothing is
    published (D-08/D-13 — a non-finite score never becomes evidence).
    """
    tier = getattr(score, "tier", None)
    if isinstance(tier, bool) or not isinstance(tier, int):
        raise DiagnosticFitRefused(
            f"the frozen score at step {step} carries no integer tier; the "
            "checkpoint is not recorded and nothing is published"
        )
    for name in ("E", "e_sys_max", "e_in_max", "eps_h"):
        value = getattr(score, name, None)
        if isinstance(value, bool) or not isinstance(value, (int, float)) \
                or not math.isfinite(float(value)):
            raise DiagnosticFitRefused(
                f"the frozen score at step {step} is not a complete finite "
                f"score ({name} = {value!r}); the checkpoint is not recorded "
                "and nothing is published"
            )


def fit_diagnostic(
    variant,
    data,
    *,
    context,
    scorecard,
    runtime=("float64", "cpu"),
    evidence_root=None,
    out_dir=None,
    steps,
    cadence=None,
    warmup_steps=0,
    deadline_seconds=None,
    times_physical=None,
    seed=SEED,
    repo_root=None,
    clock=time.monotonic,
    weights_name=WEIGHTS_NAME,
    run_phases=None,
    registration_provenance=None,
    logger_parity_provenance=None,
    run_context=None,
    variant_registry=None,
    loss_trace_stride=None,
    score_cadence=None,
):
    """Fit, measure, score and record one diagnostic variant on one orbit.

    ``data`` is an already-loaded ``ArmData`` (the synthetic fixture seam in
    tests; the Stage-0 training seam through ``run_registered_smoke``).
    ``times_physical`` are the physical times of the training samples,
    recorded beside their normalized tau; it defaults to the score view's
    times, which is exact when the train and score records share a grid.

    The bounded form (Plan 65-06): ``warmup_steps`` of the ``steps`` updates
    are warmup and the remaining measured updates provide the optimizer-rate
    measurement; ``cadence`` names the steps (0 and ``steps`` included) at
    which the shared similarity logger runs; ``deadline_seconds`` is the
    registered whole-run cap enforced between phases and updates with the
    injected clock; ``out_dir`` overrides the registry-derived evidence
    directory. Every timing segment is wrapped in the MPS ``_synchronize``
    helper, whose overhead and call count are recorded. Returns the canonical
    record; nothing is published unless every step completed finite.

    The registered Phase 67 checkpoint schedule (plan 67-04, D-08/D-10):
    ``score_cadence`` names the steps at which the frozen ``score_network``
    runs as mid-run checkpoints. Each scorer and logger event is then timed
    individually (synchronized, on the same monotonic basis, disjoint from
    the synchronized optimizer durations) inside the whole-run deadline,
    checkpoints are recorded only after complete finite scores, and the
    final checkpoint supplies the endpoint score — no fourth scoring call
    happens. Without a ``score_cadence`` the historical path is unchanged:
    no checkpoint, event or timing field is added.
    """
    resolved = resolve_variant(variant)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise DiagnosticFitRefused(f"steps must be a positive integer; got {steps!r}")
    if isinstance(warmup_steps, bool) or not isinstance(warmup_steps, int) \
            or not 0 <= warmup_steps < steps:
        raise DiagnosticFitRefused(
            f"warmup_steps must be an integer in [0, steps); got {warmup_steps!r}"
        )
    # The registry and the loss-trace stride are admitted before the model is
    # built: a bad value refuses before any data access or optimizer work.
    registry = _named_registry(variant_registry)
    if loss_trace_stride is not None and (
        isinstance(loss_trace_stride, bool) or not isinstance(loss_trace_stride, int)
        or not 1 <= loss_trace_stride <= int(steps)
    ):
        raise DiagnosticFitRefused(
            "the loss-trace stride must be an integer from 1 to optimizer_steps"
        )
    if cadence is None:
        cadence = [0, int(steps)]
    if not isinstance(cadence, list) or not cadence \
            or any(isinstance(c, bool) or not isinstance(c, int) for c in cadence):
        raise DiagnosticFitRefused(f"cadence must be a list of integers; got {cadence!r}")
    if len(set(cadence)) != len(cadence) or cadence != sorted(cadence):
        raise DiagnosticFitRefused("the cadence must be unique and in step order")
    if cadence[0] != 0 or cadence[-1] != int(steps):
        raise DiagnosticFitRefused("the cadence must start at step 0 and end at the final step")
    if any(c < 0 or c > int(steps) for c in cadence):
        raise DiagnosticFitRefused("the cadence steps must lie in [0, steps]")
    # The admitted schedule is checked before the model is built: a bad
    # score cadence refuses before any data access or optimizer work.
    score_set = None
    if score_cadence is not None:
        if not isinstance(score_cadence, list) or not score_cadence \
                or any(isinstance(c, bool) or not isinstance(c, int) for c in score_cadence):
            raise DiagnosticFitRefused(
                f"score_cadence must be a non-empty list of integers; got {score_cadence!r}"
            )
        if len(set(score_cadence)) != len(score_cadence) \
                or score_cadence != sorted(score_cadence):
            raise DiagnosticFitRefused(
                f"the score cadence must be unique and in step order; got {score_cadence!r}"
            )
        if any(c < 0 or c > int(steps) for c in score_cadence):
            raise DiagnosticFitRefused(
                f"the score cadence steps must lie in [0, steps]; got {score_cadence!r}"
            )
        if score_cadence[-1] != int(steps):
            raise DiagnosticFitRefused(
                "the score cadence must end at the final step so the endpoint "
                f"score is the final checkpoint; got {score_cadence!r}"
            )
        off_grid = [c for c in score_cadence if c not in set(cadence)]
        if off_grid:
            raise DiagnosticFitRefused(
                "every score cadence step must be a similarity cadence step; "
                f"got {score_cadence!r} against cadence {cadence!r}"
            )
        score_set = set(score_cadence)
    if deadline_seconds is not None:
        if isinstance(deadline_seconds, bool) or not isinstance(deadline_seconds, (int, float)) \
                or not math.isfinite(float(deadline_seconds)) \
                or not 0 < float(deadline_seconds) < HOUR_SECONDS:
            raise DiagnosticFitRefused(
                f"deadline_seconds must be a finite number of seconds in "
                f"(0, {HOUR_SECONDS:.0f}); got {deadline_seconds!r}"
            )
    if out_dir is None:
        if evidence_root is None:
            raise DiagnosticFitRefused("the fit needs an out_dir or an evidence_root")
        out_dir = diagnostic_evidence_dir(
            diagnostic_run_id(resolved, data), evidence_root=evidence_root
        )
    out_dir = Path(out_dir)
    record_path = out_dir / RECORD_NAME
    if record_path.exists():
        raise FirstResultExists(
            f"a diagnostic record already exists at {record_path.name}; the first "
            "completed run is the result and a second run never replaces it"
        )
    dtype, device = _resolve_runtime(runtime)
    _validate_data_points(getattr(data, "data_points", None))
    if times_physical is None:
        times_physical = data.score.times

    fit_started = clock()
    sync_overhead = 0.0
    sync_samples = 0

    def timed_sync():
        nonlocal sync_overhead, sync_samples
        mark = clock()
        _synchronize(device)
        sync_overhead += clock() - mark
        sync_samples += 1

    def check_deadline(what):
        if deadline_seconds is None:
            return
        elapsed = clock() - fit_started
        if elapsed >= float(deadline_seconds):
            raise DiagnosticFitRefused(
                f"the whole-run deadline ({float(deadline_seconds):g}s) expired "
                f"before {what} after {elapsed:.3f}s of completed work"
            )

    # Setup: the model and its constant-rate Adam policy, synchronized.
    check_deadline("setup")
    timed_sync()
    setup_started = clock()
    model = build_variant(resolved, seed=seed, dtype=dtype, device=device)
    options = OptConfig()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=float(resolved.learning_rate),
        betas=options.adam_betas,
        eps=options.adam_eps,
    )
    setup_seconds = clock() - setup_started

    # Initialization is logged once, before any step, outside the optimizer
    # timing (its seconds join the logging phase). On the registered Phase 67
    # schedule every logger and scorer event is timed individually as its own
    # synchronized completed-work segment, disjoint from the synchronized
    # optimizer durations, and each expensive event is deadline-checked
    # before and after (plan 67-04, D-08).
    scheduled = score_set is not None
    log_seconds = 0.0
    logging_events = []
    score_events = []
    score_checkpoints = []
    cadence_set = set(cadence)
    entries = []
    view = data.score

    def run_log_event(step, point):
        nonlocal log_seconds
        if scheduled:
            check_deadline(f"the similarity log at step {step}")
            timed_sync()
            log_started = clock()
            entry = log_similarity(
                model, data.data_points, times_physical, step=step, point=point
            )
            timed_sync()
        else:
            log_started = clock()
            entry = log_similarity(
                model, data.data_points, times_physical, step=step, point=point
            )
        event_seconds = clock() - log_started
        log_seconds += event_seconds
        if scheduled:
            logging_events.append({"step": int(step), "seconds": float(event_seconds)})
            check_deadline(f"the similarity log at step {step} completed")
        return entry

    if 0 in cadence_set:
        entries.append(run_log_event(0, "init"))

    losses = []
    warmup_seconds = 0.0
    measured_seconds = 0.0
    measured_count = 0
    loop_started = clock()
    for step in range(1, int(steps) + 1):
        check_deadline(f"optimizer step {step}")
        timed_sync()
        segment_started = clock()
        losses.append(
            _guarded_step(model, optimizer, data.data_points, dtype=dtype, device=device, step=step)
        )
        timed_sync()
        segment_seconds = clock() - segment_started
        if step <= int(warmup_steps):
            warmup_seconds += segment_seconds
        else:
            measured_seconds += segment_seconds
            measured_count += 1
        if step in cadence_set:
            point = "final" if step == int(steps) else f"step-{step}"
            entries.append(run_log_event(step, point))
        if score_set is not None and step in score_set:
            check_deadline(f"the frozen-score checkpoint at step {step}")
            timed_sync()
            event_started = clock()
            checkpoint_score = score_network(
                model,
                data.ic13,
                data.masses,
                view.positions,
                view.inner_pair,
                view.times,
                scorecard=scorecard,
                dtype=dtype,
                device=device,
                grid=view.grid,
            )
            timed_sync()
            event_seconds = clock() - event_started
            _require_finite_checkpoint(checkpoint_score, step=step)
            score_events.append({"step": int(step), "seconds": float(event_seconds)})
            score_checkpoints.append({
                "step": int(step),
                "score": checkpoint_score.to_json_dict(),
                "elapsed_seconds": float(clock() - fit_started),
            })
            check_deadline(f"the frozen-score checkpoint at step {step} completed")
    wall = clock() - loop_started

    comparisons_seconds = None
    if score_set is None:
        # Scoring happens outside the optimizer timing, synchronized, inside
        # the whole-run deadline.
        check_deadline("scoring")
        timed_sync()
        scoring_started = clock()
        score = score_network(
            model,
            data.ic13,
            data.masses,
            view.positions,
            view.inner_pair,
            view.times,
            scorecard=scorecard,
            dtype=dtype,
            device=device,
            grid=view.grid,
        )
        comparisons = _comparison_rows(data, scorecard=scorecard)
        scoring_seconds = clock() - scoring_started
        network_score_json = score.to_json_dict()
    else:
        # The endpoint score is the final frozen-score checkpoint: no fourth
        # scoring call happens. The frozen comparisons still run on the same
        # window, timed as their own synchronized segment.
        check_deadline("comparisons")
        timed_sync()
        comparisons_started = clock()
        comparisons = _comparison_rows(data, scorecard=scorecard)
        timed_sync()
        comparisons_seconds = clock() - comparisons_started
        scoring_seconds = (
            sum(event["seconds"] for event in score_events) + comparisons_seconds
        )
        network_score_json = score_checkpoints[-1]["score"]

    check_deadline("publish")
    publish_started = clock()
    out_dir.mkdir(parents=True, exist_ok=True)
    weights_block = save_diagnostic_weights(
        out_dir / weights_name, model, variant=resolved, seed=seed, runtime=runtime
    )
    times = np.asarray(times_physical, dtype=np.float64).reshape(-1)
    timing = {
        "basis": (
            TIMING_BASIS if int(warmup_steps) == 0
            else TIMING_BASIS_BOUNDED.format(warmup=int(warmup_steps), measured=measured_count)
        ),
        "steps": {
            "requested": int(steps),
            "warmup": int(warmup_steps),
            "measured": measured_count,
            "completed": len(losses),
        },
        "seconds_per_step": measured_seconds / measured_count,
        "seconds_per_step_basis": SECONDS_PER_STEP_BASIS.format(
            warmup=int(warmup_steps), measured=measured_count
        ),
        "measured_seconds": float(measured_seconds),
        "warmup_seconds": float(warmup_seconds),
        "wall_seconds": float(wall),
        "total_wall_seconds": None,
        "sync": {"sample_count": sync_samples, "overhead_seconds": float(sync_overhead)},
        "phases": {
            "setup_seconds": float(setup_seconds),
            "logging_seconds": float(log_seconds),
            "scoring_seconds": float(scoring_seconds),
            "publish_seconds": None,  # filled in after the record is assembled
            **(dict(run_phases) if run_phases else {}),
        },
        "completed_steps": len(losses),
    }
    if scheduled:
        # The disjoint per-event ledger (plan 67-04): each logger and scorer
        # event's own synchronized seconds, plus the publication I/O segment.
        timing["events"] = {
            "logging": logging_events,
            "scoring": score_events,
            "publication_io": [{"phase": "publish", "seconds": None}],
        }
        timing["phases"]["comparisons_seconds"] = float(comparisons_seconds)
    timing["total_wall_seconds"] = float(clock() - fit_started)
    timing["end_to_end_seconds_per_completed_step"] = (
        timing["total_wall_seconds"] / len(losses)
    )
    # Only the recorded loss trace is thinned: the full in-memory losses list,
    # and every count taken from it, are unchanged. A stride s keeps the loss
    # after every s-th step, then the final step's loss when the step count is
    # not a multiple of s.
    if loss_trace_stride is None:
        loss_trace = list(losses)
    else:
        loss_trace = [
            losses[index]
            for index in range(int(loss_trace_stride) - 1, len(losses), int(loss_trace_stride))
        ]
        if len(losses) % int(loss_trace_stride):
            loss_trace.append(losses[-1])
    loss_block = {"final": losses[-1], "trace": loss_trace}
    if loss_trace_stride is not None:
        loss_block["trace_stride"] = int(loss_trace_stride)
    record = {
        **diagnostic_marker(schema=DIAGNOSTIC_SCHEMA),
        "status": "complete",
        "run_id": diagnostic_run_id(resolved, data),
        "variant": {
            **resolved.to_json_dict(),
            "registered": resolved.name in registry,
            "registry": variant_registry,
        },
        "seed": int(seed),
        "runtime": {"dtype": str(runtime[0]), "device": str(runtime[1])},
        "orbit": {
            "train": data.records["train"],
            "score": data.records["score"],
            "beside": data.records["beside"],
            "window": {
                "t_start": float(times[0]),
                "t_end": float(times[-1]),
                "n_points": int(times.shape[0]),
                "configured_length": float(resolved.window_length),
                "basis": "physical times of the training samples",
            },
            "two_kepler_initial_state": (
                "the train record's first in-window snapshot (true_r0, true_v0)"
            ),
        },
        "steps": timing["steps"],
        "optimizer": {
            "kind": "adam_constant_rate",
            "lr": float(resolved.learning_rate),
            "betas": [float(beta) for beta in options.adam_betas],
            "eps": float(options.adam_eps),
            "scheduler": None,
            "physics_term": None,
            "polish": None,
        },
        "similarity": {"cadence": list(cadence), "entries": entries},
        **({"score_checkpoints": score_checkpoints} if scheduled else {}),
        "loss": loss_block,
        "timing": timing,
        "scores": {"network": network_score_json},
        "comparisons": comparisons,
        "weights": weights_block,
        "source_sha256": pinned_source_hashes(repo_root=repo_root),
        "access": {
            "reads": dict(context.reader.read_counts()),
            "attestation": (
                context.attestation.summary() if context.attestation is not None else None
            ),
            **(
                {"stage0": dict(context.reader.access_summary())}
                if hasattr(context.reader, "access_summary") else {}
            ),
        },
    }
    if registration_provenance is not None:
        record["registration"] = dict(registration_provenance)
    if logger_parity_provenance is not None:
        record["logger_parity"] = dict(logger_parity_provenance)
    if run_context is not None:
        record["context"] = dict(run_context)
    record["timing"]["phases"]["publish_seconds"] = float(clock() - publish_started)
    if scheduled:
        record["timing"]["events"]["publication_io"][0]["seconds"] = (
            record["timing"]["phases"]["publish_seconds"]
        )
        # The deadline is checked after the expensive publication work and
        # before the exclusive write, so an over-cap attempt never strands a
        # written record; the supervisor remains the hard stop (D-07/D-08).
        check_deadline("the publication of the record")
    write_record_exclusive(
        record_path, record,
        data_root=getattr(context.reader, "data_root", None),
    )
    return record


# --------------------------------------------------------------------------
# Plan 65-06: the admitted smoke run — exclusive attempt ownership, the
# supervised bounded worker, and result verification.
# --------------------------------------------------------------------------


def _claim_attempt(record_path, doc, *, registration_relative, registration_file):
    """Claim the output exclusively BEFORE any data access (T-65-19).

    The claim is an ``O_EXCL`` canonical JSON file beside the declared record:
    a second writer — a repeated or parallel attempt — refuses at the claim
    and never touches data or optimizer state. ``registration_relative`` is
    the repo-relative citation; ``registration_file`` is the path hashed.
    Returns the attempt path.
    """
    out_dir = Path(record_path).parent
    attempt_path = out_dir / ATTEMPT_NAME
    payload = {
        "schema": ATTEMPT_SCHEMA,
        "status": "running",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registration": {
            "path": Path(registration_relative).as_posix(),
            "sha256": _sha256_file(registration_file),
        },
        "output": Path(record_path).name,
        "whole_run_cap_seconds": float(doc["settings"]["whole_run_cap_seconds"]),
    }
    write_record_exclusive(attempt_path, payload)
    return attempt_path


def _mark_attempt(attempt_path, status, **fields):
    """Update the attempt claim in place; the claim itself is never removed."""
    path = Path(attempt_path)
    payload = json.loads(path.read_bytes().decode("utf-8"))
    payload["status"] = status
    payload["ended_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload.update(fields)
    evidence_io.write_json(path, payload)


def _ensure_incomplete_attempt(attempt_path, reason):
    """Mark the attempt incomplete; create the record of it if it is missing."""
    path = Path(attempt_path)
    if path.exists():
        _mark_attempt(path, "incomplete", reason=reason)
        return
    payload = {
        "schema": ATTEMPT_SCHEMA,
        "status": "incomplete",
        "reason": reason,
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ended_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pid": os.getpid(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    evidence_io.write_json(path, payload)


def run_registered_smoke(registration_path, output_path, *, repo_root=None, clock=time.monotonic):
    """Run exactly the admitted smoke: admission, claim, data, fit, publish.

    The committed-clean registration, its settings and the logger-parity
    receipt are re-verified here (the worker path re-executes the same gate
    the CLI ran), the record must not already exist, and the output is
    claimed exclusively BEFORE the Stage-0 training record is opened. Only
    the registered gold orbit, the recorded normalizer and the frozen scorer
    are used. A refusal after the claim — a deadline expiry, a non-finite
    update, an interruption — marks the attempt explicitly incomplete and
    publishes nothing; it is never retried, extended or resumed here.
    """
    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    settings, variant, orbit_key, (dtype, device) = validate_smoke_settings(doc)
    record_path = Path(output_path)
    if record_path.exists():
        raise FirstResultExists(
            f"a diagnostic record already exists at {record_path.name}; the first "
            "completed run is the result and a second run never replaces it"
        )
    parity = doc.get("logger_parity")
    receipt_entry = parity["receipt"]
    context_block = doc.get("context") or {}
    registration_file = Path(registration_path)
    if not registration_file.is_absolute():
        registration_file = root / registration_file
    try:
        registration_relative = registration_file.resolve().relative_to(root).as_posix()
    except ValueError:
        registration_relative = registration_file.as_posix()
    attempt_path = _claim_attempt(
        record_path, doc,
        registration_relative=registration_relative, registration_file=registration_file,
    )
    try:
        phase_started = clock()
        context = open_diagnostic_context(repo_root=root)
        scorecard = load_scorecard()
        spec = one_orbit_spec(orbit_key)
        data = load_diagnostic_data(
            spec, context, scorecard=scorecard, dtype=dtype, device=device,
            window_length=float(variant.window_length),
        )
        data_load_seconds = clock() - phase_started
        record = fit_diagnostic(
            variant,
            data,
            context=context,
            scorecard=scorecard,
            runtime=(settings["runtime"]["dtype"], settings["runtime"]["device"]),
            out_dir=record_path.parent,
            weights_name=SMOKE_WEIGHTS_NAME,
            steps=int(settings["optimizer_steps"]),
            warmup_steps=int(settings["warmup_steps"]),
            cadence=list(settings["similarity_cadence"]),
            deadline_seconds=float(settings["whole_run_cap_seconds"]),
            times_physical=None,
            seed=int(settings["seed"]),
            variant_registry=settings.get("variant_registry"),
            loss_trace_stride=settings.get("loss_trace_stride"),
            score_cadence=settings.get("score_cadence"),
            # The 33 pinned source digests describe the RUNNING implementation,
            # never the registration's repository (which may be a fixture).
            repo_root=None,
            clock=clock,
            run_phases={"data_load_seconds": float(data_load_seconds)},
            registration_provenance={
                "path": registration_relative,
                "sha256": _sha256_file(registration_file),
            },
            logger_parity_provenance={
                "receipt_path": str(receipt_entry["path"]),
                "receipt_sha256": str(receipt_entry["sha256"]),
                "run_commit": str(parity.get("run_commit")),
            },
            run_context={
                "probe_verdict": context_block.get("probe_verdict"),
                "probe_result_sha256": (
                    (context_block.get("probe_result") or {}).get("sha256")
                ),
                "note": (
                    "the probe's reproduction branch is recorded, not required; "
                    "the smoke proves mechanics and cost only"
                ),
            },
        )
    except BaseException as exc:  # refusal, deadline, interruption: stay incomplete
        _mark_attempt(attempt_path, "incomplete", reason=f"{type(exc).__name__}: {exc}")
        raise
    _mark_attempt(
        attempt_path,
        "published",
        record_sha256=_sha256_file(record_path),
        completed_steps=record["steps"]["completed"],
    )
    return {
        "status": "complete",
        "record_path": str(record_path),
        "completed_steps": record["steps"]["completed"],
        "seconds_per_step": record["timing"]["seconds_per_step"],
    }


class _WorkerTerminated(BaseException):
    """A supervised worker received a termination signal."""

    def __init__(self, signum):
        self.signum = int(signum)
        super().__init__(f"terminated by signal {signum}")


def _smoke_worker(registration_path, output_path, repo_root, queue):
    """The supervised worker body: admitted smoke, report via the queue.

    SIGTERM is converted into the incomplete path (graceful termination); the
    worker distinguishes its own refusals (``refused`` — nothing to mark) from
    failures after its claim (``incomplete`` — the attempt already says so).
    """
    previous_handler = None
    try:
        previous_handler = signal.signal(
            signal.SIGTERM, lambda signum, frame: (_ for _ in ()).throw(_WorkerTerminated(signum))
        )
    except (ValueError, OSError):
        previous_handler = None
    try:
        summary = run_registered_smoke(
            registration_path,
            output_path,
            repo_root=Path(repo_root) if repo_root else None,
        )
    except FirstResultExists as exc:
        queue.put({"status": "refused", "reason": str(exc)})
    except BaseException as exc:
        queue.put({"status": "incomplete", "reason": f"{type(exc).__name__}: {exc}"})
    else:
        queue.put({
            "status": "complete",
            "completed_steps": summary["completed_steps"],
            "seconds_per_step": summary["seconds_per_step"],
            "record_path": summary["record_path"],
        })
    finally:
        if previous_handler is not None:
            signal.signal(signal.SIGTERM, previous_handler)


def _drain_queue(queue):
    try:
        return queue.get(block=False)
    except Exception:  # empty, closed or cross-platform queue quirk: no payload
        return None


def _run_supervised(
    target,
    args,
    *,
    timeout,
    context_method="spawn",
    terminate_grace=10.0,
    kill_grace=5.0,
):
    """Run ``target(*args, queue)`` in a supervised child process.

    The child is joined with the whole-run timeout; a child that outlives it
    is terminated gracefully (SIGTERM, then SIGKILL as the last resort). The
    standard library only: no retry, no extension, no resume.
    """
    context = multiprocessing.get_context(context_method)
    queue = context.Queue()
    process = context.Process(target=target, args=(*args, queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join(terminate_grace)
        if process.is_alive():
            process.kill()
            process.join(kill_grace)
        return "timeout", None
    return "exited", _drain_queue(queue)


def verify_fit_result(registration_path, result_path, *, repo_root=None):
    """Verify an existing smoke result against its committed registration.

    No retraining and no corpus access: the committed registration is
    re-admitted (metadata-only), the result's identity, settings agreement,
    cadence, steps, optimizer policy, orbit and window, timing fields,
    weights bytes and tensor digest, frozen source digests and access
    evidence are checked against the committed bytes. Any disagreement is a
    typed refusal naming every problem found.
    """
    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    settings, variant, _orbit_key, _runtime_pair = validate_smoke_settings(doc)
    result_file = Path(result_path)
    if not result_file.is_absolute():
        result_file = root / result_file
    record = read_diagnostic_record(result_file)
    problems = []

    def check(condition, message):
        if not condition:
            problems.append(message)

    check(record.get("status") == "complete", "the result status is not complete")
    variant_block = record.get("variant") or {}
    check(
        variant_block.get("name") == settings["variant"]["name"],
        "the result's variant is not the registered variant",
    )
    for field, value in variant.to_json_dict().items():
        check(
            variant_block.get(field) == value,
            f"the result's variant field {field} disagrees with the registration",
        )
    check(
        variant_block.get("registry") == settings.get("variant_registry"),
        "the result's variant registry disagrees with the registration",
    )
    loss_block = record.get("loss") or {}
    trace = loss_block.get("trace")
    stride = settings.get("loss_trace_stride")
    if stride is None:
        check(
            loss_block.get("trace_stride") is None,
            "the result's loss block names a trace_stride the registration does not declare",
        )
        expected_trace_length = settings["optimizer_steps"]
    else:
        check(
            loss_block.get("trace_stride") == stride,
            "the result's loss trace_stride disagrees with the registration",
        )
        expected_trace_length = settings["optimizer_steps"] // stride + (
            1 if settings["optimizer_steps"] % stride else 0
        )
    check(
        isinstance(trace, list) and len(trace) == expected_trace_length,
        "the result's loss trace length disagrees with the registration",
    )
    check(
        isinstance(trace, list) and bool(trace) and trace[-1] == loss_block.get("final"),
        "the result's last loss trace entry disagrees with loss.final",
    )
    check(record.get("seed") == settings["seed"], "the result's seed disagrees with the registration")
    runtime = record.get("runtime") or {}
    check(
        runtime.get("dtype") == settings["runtime"]["dtype"]
        and runtime.get("device") == settings["runtime"]["device"],
        "the result's runtime disagrees with the registration",
    )
    steps_block = record.get("steps") or {}
    check(
        steps_block.get("requested") == settings["optimizer_steps"],
        "the result's requested steps disagree with the registration",
    )
    check(
        steps_block.get("warmup") == settings["warmup_steps"],
        "the result's warmup steps disagree with the registration",
    )
    check(
        steps_block.get("measured") == settings["measured_steps"],
        "the result's measured steps disagree with the registration",
    )
    check(
        steps_block.get("completed") == settings["optimizer_steps"],
        "the result did not complete the registered steps",
    )
    similarity = record.get("similarity") or {}
    check(
        similarity.get("cadence") == list(settings["similarity_cadence"]),
        "the result's similarity cadence disagrees with the registration",
    )
    entries = similarity.get("entries") or []
    check(
        [entry.get("step") for entry in entries] == list(settings["similarity_cadence"]),
        "the result's similarity entries are not exactly the registered cadence",
    )
    # The registered Phase 67 checkpoint schedule (plan 67-04): a
    # registration that declares one must see exactly its score checkpoints,
    # the endpoint score reused from the final checkpoint and the per-event
    # timing ledger; a registration without one must see none of them.
    score_cadence_setting = settings.get("score_cadence")
    if score_cadence_setting is not None:
        checkpoints = record.get("score_checkpoints")
        checkpoint_steps = (
            [entry.get("step") for entry in checkpoints if isinstance(entry, Mapping)]
            if isinstance(checkpoints, list) else None
        )
        check(
            checkpoint_steps == list(score_cadence_setting),
            "the result's score checkpoints disagree with the registered score cadence",
        )
        final_checkpoint = (
            checkpoints[-1]
            if isinstance(checkpoints, list) and checkpoints
            and isinstance(checkpoints[-1], Mapping) else None
        )
        check(
            final_checkpoint is not None
            and (record.get("scores") or {}).get("network")
            == final_checkpoint.get("score"),
            "the result's network score is not its final score checkpoint",
        )
        event_ledger = (record.get("timing") or {}).get("events") or {}
        check(
            isinstance(event_ledger.get("logging"), list)
            and isinstance(event_ledger.get("scoring"), list)
            and isinstance(event_ledger.get("publication_io"), list),
            "the result's timing is missing the per-event logging, scoring "
            "and publication seconds",
        )
    else:
        check(
            "score_checkpoints" not in record,
            "the result carries score checkpoints its registration does not declare",
        )
        check(
            "events" not in (record.get("timing") or {}),
            "the result's timing carries per-event seconds its registration "
            "does not declare",
        )
    optimizer = record.get("optimizer") or {}
    check(
        optimizer.get("kind") == "adam_constant_rate"
        and float(optimizer.get("lr", float("nan"))) == float(variant.learning_rate)
        and optimizer.get("scheduler") is None
        and optimizer.get("physics_term") is None
        and optimizer.get("polish") is None,
        "the result's optimizer policy disagrees with the registration",
    )
    orbit = record.get("orbit") or {}
    train = orbit.get("train") or {}
    check(
        train.get("record_key") == settings["orbit_key"],
        "the result's training orbit disagrees with the registration",
    )
    window = orbit.get("window") or {}
    check(
        float(window.get("configured_length", float("nan"))) == float(variant.window_length),
        "the result's window disagrees with the registration",
    )
    registration_file = Path(registration_path)
    if not registration_file.is_absolute():
        registration_file = root / registration_file
    registration_block = record.get("registration")
    check(
        isinstance(registration_block, Mapping)
        and _cites_registration_bytes(
            registration_file, root, registration_block.get("sha256")
        ),
        "the result does not cite the committed registration bytes",
    )
    parity_entry = (doc.get("logger_parity") or {}).get("receipt") or {}
    parity_block = record.get("logger_parity")
    check(
        isinstance(parity_block, Mapping)
        and parity_block.get("receipt_sha256") == parity_entry.get("sha256"),
        "the result does not cite the committed logger-parity receipt",
    )
    timing = record.get("timing") or {}
    for key in (
        "basis", "seconds_per_step", "seconds_per_step_basis", "measured_seconds",
        "warmup_seconds", "wall_seconds", "total_wall_seconds",
        "end_to_end_seconds_per_completed_step",
    ):
        check(key in timing, f"the result's timing block is missing {key}")
    sync_block = timing.get("sync") or {}
    check(
        "sample_count" in sync_block and "overhead_seconds" in sync_block,
        "the result's timing block is missing the synchronization record",
    )
    phases = timing.get("phases") or {}
    for key in ("setup_seconds", "logging_seconds", "scoring_seconds", "publish_seconds"):
        check(key in phases, f"the result's timing phases are missing {key}")
    network = (record.get("scores") or {}).get("network") or {}
    check("E" in network and "tier" in network, "the result carries no frozen network score")
    comparisons = {row.get("comparison"): row for row in record.get("comparisons") or []}
    check(
        "window_mean_constant" in comparisons
        and "score" in (comparisons.get("window_mean_constant") or {}),
        "the result carries no window-mean-constant comparison score",
    )
    check("two_kepler" in comparisons, "the result carries no two-Kepler comparison row")
    access = record.get("access") or {}
    reads = access.get("reads") or {}
    check(reads.get("validation", 0) == 0, "the result records validation-split reads")
    check(access.get("attestation") is not None, "the result carries no access attestation")
    check("stage0" in access, "the result carries no Stage-0 access summary")
    weights_block = record.get("weights") or {}
    weights_file = result_file.parent / str(weights_block.get("file", ""))
    check(weights_file.is_file(), "the result's weights file is missing beside it")
    if weights_file.is_file():
        digest = _sha256_file(weights_file)
        if digest == weights_block.get("sha256"):
            payload = read_diagnostic_weights(weights_file)
            check(
                weights_digest(payload["state_dict"]) == weights_block.get("tensor_digest"),
                "the result's weights tensor digest disagrees with the payload",
            )
        else:
            problems.append("the result's weights bytes disagree with the recorded digest")
    check(
        record.get("source_sha256") == pinned_source_hashes(),
        "the result's 33 pinned source digests disagree with the committed modules",
    )
    if problems:
        raise DiagnosticFitRefused(
            "the result disagrees with the committed registration: " + "; ".join(problems)
        )
    return {"verified": True, "result": result_file.as_posix(), "problems": []}


def _cmd_run(
    registration_path,
    output_path,
    *,
    repo_root=None,
    context_method="spawn",
    supervisor=None,
):
    """The ``run`` command: admission, supervised worker, exclusive reporting.

    The whole-run cap is enforced twice: the worker checks the deadline
    between phases and updates with its own clock, and the supervisor joins
    the child with the registered cap as the hard backstop, terminating
    gracefully and marking the attempt explicitly incomplete.
    """
    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    record_path = Path(output_path)
    if record_path.exists():
        raise FirstResultExists(
            f"a diagnostic record already exists at {record_path.name}; the first "
            "completed run is the result and a second run never replaces it"
        )
    cap = float(doc["settings"]["whole_run_cap_seconds"])
    attempt_path = record_path.parent / ATTEMPT_NAME
    if supervisor is None:
        def supervisor(target, args, *, timeout, **kwargs):
            return _run_supervised(
                target, args, timeout=timeout, context_method=context_method, **kwargs
            )
    try:
        status, payload = supervisor(
            _smoke_worker,
            (str(registration_path), str(record_path), str(root)),
            timeout=cap,
        )
    except BaseException as exc:  # supervisor interrupted: the attempt stays burned
        _ensure_incomplete_attempt(
            attempt_path, reason=f"{type(exc).__name__}: supervisor interrupted"
        )
        raise
    if status == "timeout" or payload is None or payload.get("status") != "complete":
        if status == "timeout":
            reason = "wall_cap_expired"
        elif payload is None:
            reason = "the supervised worker exited without reporting"
        else:
            reason = str(payload.get("reason", "unknown"))
            if payload.get("status") == "refused":
                print(f"FIT-REFUSED: {reason}", file=sys.stderr)
                return 2
        _ensure_incomplete_attempt(attempt_path, reason=reason)
        print(f"FIT-RUN-INCOMPLETE reason={reason}", file=sys.stderr)
        return 2
    print(
        f"FIT-RUN-COMPLETE status=complete "
        f"completed_steps={payload.get('completed_steps')} "
        f"seconds_per_step={payload.get('seconds_per_step')!r} "
        f"record={record_path}"
    )
    return 0


def main(argv=None, *, repo_root=None, context_method="spawn", supervisor=None):
    """The fit CLI: check-registration / run / verify-result.

    Exit codes: 0 ok, 2 refused or incomplete. ``check-registration`` is
    metadata-only and opens no corpus or weights; ``run`` admits one
    registration and one exclusive attempt; ``verify-result`` reads existing
    evidence without retraining.
    """
    parser = argparse.ArgumentParser(
        prog="diagnostic_fit",
        description=(
            "Bounded diagnostic fit: committed registration, synchronized "
            "timing, whole-run cap and exclusive result."
        ),
    )
    commands = parser.add_subparsers(dest="command")
    check = commands.add_parser("check-registration")
    check.add_argument("--registration", required=False)
    run = commands.add_parser("run")
    run.add_argument("--registration", required=False)
    run.add_argument("--output", required=False)
    verify = commands.add_parser("verify-result")
    verify.add_argument("--registration", required=False)
    verify.add_argument("--result", required=False)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse's own usage error carries exit code 2
        return int(exc.code) if isinstance(exc.code, int) else 2

    required = {
        "check-registration": ["registration"],
        "run": ["registration", "output"],
        "verify-result": ["registration", "result"],
    }.get(args.command)
    if required is None:
        print("FIT-REFUSED: choose check-registration, run or verify-result", file=sys.stderr)
        return 2
    missing = [f"--{name}" for name in required if getattr(args, name) is None]
    if missing:
        print(f"FIT-REFUSED: missing required flags: {', '.join(missing)}", file=sys.stderr)
        return 2
    try:
        if args.command == "check-registration":
            report = check_fit_registration(args.registration, repo_root=repo_root)
            print(f"CHECK-REGISTRATION-OK registration-commit={report['registration_commit']}")
            for artifact in report["artifacts"]:
                print(f"  {artifact['sha256']}  {artifact['path']}")
            return 0
        if args.command == "run":
            return _cmd_run(
                args.registration,
                args.output,
                repo_root=repo_root,
                context_method=context_method,
                supervisor=supervisor,
            )
        verify_fit_result(args.registration, args.result, repo_root=repo_root)
        print("VERIFY-RESULT-OK")
        return 0
    except (DiagnosticFitRefused, DiagnosticRegistrationRefused, FirstResultExists) as exc:
        print(f"FIT-REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
