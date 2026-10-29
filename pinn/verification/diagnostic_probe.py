"""Phase 65 (DIAG-09): the read-only historical probe runner and its registration.

D-02 through D-07 put the 2026-10-27 exploratory probe on the record before any
rerun: the original scripts, their scoped numerical output and the exact
reproduction rule are committed first (Plan 65-04), and only a committed-clean
registration admits any later data or weight access (Plan 65-05 performs the
real seven-arm reproduction; this plan runs nothing real).

Reproduction is defined by exact formatter equality: every registered
historical numeric field reproduces when the freshly measured value renders, under
the field's original formatter, to the preserved token — never a widened
tolerance. Each token's exact rounding cell (the first and last representable
doubles that render to it, with the excluded ``nextafter`` neighbours) is
recorded in the registration and cross-checked against the formatter, so the
acceptance interval is provably the original one, including signed zero, ties
and ``.3g``'s omitted trailing zeros. The measurement itself is the one shared
``measure_time_signal`` implementation — probe and fit logger never run a
second reduction (D-05).

Reading rule (immutable after observation): every registered available
historical numeric field reproduces or is marked ``not_reproduced``. All
required fields reproduced keeps the exploratory association on record
(``retained``); any failed required comparison withdraws the lead and yields a
SCOPE-49 proposal for the owner; fields the shared measurement cannot produce
and figures whose original source is absent are reported separately — never a
fabricated failure or a fabricated success. Individual deep-layer values that
the original all-arm output never printed are recorded as ``new_measurement``
entries, not invented historical targets. Low cosine is association only; it
never claims causality, information loss or a capacity bound (D-07).

The runner is probe-only: an interlock refuses optimizer construction and
steps for the whole run, attempted steps are counted (zero on any complete
run), and the model's parameter tensors are digested before and after every
measurement so any mutation is a refusal. Attempts are claimed exclusively and
never replaced; an interrupted attempt stays explicitly incomplete and no
result exists without a complete one; there is no automatic numerical retry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import OrderedDict
from collections.abc import Mapping
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import torch

from pinn.verification.diagnostic_guard import (
    REGISTRATION_SCHEMA,
    DiagnosticRegistrationRefused,
    require_committed_registration,
)
from pinn.verification.diagnostic_similarity import measure_time_signal

__all__ = [
    "PROBE_REGISTRATION_SCHEMA",
    "PROBE_RESULT_SCHEMA",
    "PROBE_ATTEMPT_SCHEMA",
    "ProbeRefused",
    "RegistrationRefused",
    "AttemptExists",
    "ProbeInterlockRefused",
    "RegistrationError",
    "render",
    "derive_cell",
    "compare_field",
    "evaluate_reading_rule",
    "new_measurement_entry",
    "optimizer_interlock",
    "load_registration",
    "check_registration",
    "run_probe",
    "verify_result",
    "default_model_factory",
    "default_probe_loader",
    "main",
]

PROBE_REGISTRATION_SCHEMA = REGISTRATION_SCHEMA
PROBE_RESULT_SCHEMA = "phase65-probe-result/v1"
PROBE_ATTEMPT_SCHEMA = "phase65-probe-attempt/v1"
LOGGER_PARITY_POINT = "probe-logger-parity"
_DEEP_LAYERS = tuple(f"h{index}" for index in range(3, 13))


class ProbeRefused(RuntimeError):
    """The probe refuses before or during the run; nothing is published."""


class RegistrationRefused(ProbeRefused):
    """The registration does not admit the run (see the shared guard)."""


class AttemptExists(ProbeRefused):
    """An attempt or result already exists; the first is never replaced."""


class ProbeInterlockRefused(ProbeRefused):
    """An optimizer path or a parameter mutation was refused by the interlock."""


class RegistrationError(ValueError):
    """The registration document itself is malformed."""


# --------------------------------------------------------------------------
# Exact formatter rounding cells
# --------------------------------------------------------------------------


def render(value, formatter):
    """The historical formatter applied to one value (e.g. ``".3g"``)."""
    return format(float(value), formatter)


def derive_cell(formatter, token):
    """The exact rounding cell of ``token`` under the original ``formatter``.

    Returns the first and last representable doubles that render to the token
    (both included in the cell), plus the first excluded neighbour on each
    side. The cell is the original formatter's exact preimage of the token —
    never a tolerance widened by counting visible digits — so signed zero,
    decimal-midpoint ties and ``.3g``'s omitted trailing zeros are handled by
    construction. The boundary is found by exponential search for an outside
    float followed by bisection over the float grid, which stays logarithmic
    even for cells that reach toward zero, where the per-ulp double density
    would make a linear walk unbounded.
    """
    token = str(token)
    anchor = float(token)
    if render(anchor, formatter) != token:
        raise RegistrationError(
            f"token {token!r} is not the {formatter} rendering of its float value"
        )

    def inside(value):
        return math.isfinite(value) and render(value, formatter) == token

    def boundary(known_inside, direction):
        """The extreme inside float adjacent to the outside in ``direction``."""
        step = 1.0
        outside = known_inside + direction * step
        while inside(outside) or outside == known_inside:
            step *= 2.0
            outside = known_inside + direction * step
        low, high = (outside, known_inside) if direction < 0 else (known_inside, outside)
        while True:
            middle = (low + high) / 2.0
            if middle <= low or middle >= high:
                break
            if inside(middle):
                if direction < 0:
                    high = middle
                else:
                    low = middle
            else:
                if direction < 0:
                    low = middle
                else:
                    high = middle
        return high if direction < 0 else low

    lo = boundary(anchor, -1.0)
    hi = boundary(anchor, +1.0)
    return {
        "lo": lo,
        "hi": hi,
        "lo_included": True,
        "hi_included": True,
        "excluded_below": math.nextafter(lo, -math.inf),
        "excluded_above": math.nextafter(hi, math.inf),
    }


def compare_field(expected, measured_value):
    """One registered field's verdict by exact formatter equality.

    When the registration records the field's rounding cell, the derived cell
    must match it exactly (a recorded cell that disagrees with the formatter is
    tampering, not a tolerance). The measured value reproduces exactly when it
    renders to the preserved token; both cell endpoints are inclusive.
    """
    formatter = expected.get("formatter")
    token = expected.get("token")
    if not formatter or token is None:
        raise RegistrationError(
            f"a registered field needs a formatter and a token; got {expected!r}"
        )
    cell = derive_cell(formatter, token)
    recorded = expected.get("cell")
    if isinstance(recorded, Mapping):
        for key, endpoint in (("lo_hex", cell["lo"]), ("hi_hex", cell["hi"])):
            if key in recorded and float.fromhex(str(recorded[key])) != endpoint:
                raise RegistrationError(
                    f"the recorded rounding cell for token {token!r} disagrees with "
                    f"the {formatter} formatter; refusing the tampered cell"
                )
    rendered = render(measured_value, formatter)
    return {
        "status": "reproduced" if rendered == token else "not_reproduced",
        "measured": float(measured_value),
        "rendered": rendered,
        "token": token,
        "formatter": formatter,
    }


# --------------------------------------------------------------------------
# The reading rule
# --------------------------------------------------------------------------


def evaluate_reading_rule(entries):
    """Apply the registered reading rule to one run's field verdicts.

    ``retained`` requires every available required field to reproduce; any
    failed required comparison ``withdraws`` the lead and proposes the SCOPE-49
    roadmap change. Preserved-only fields (no shared-measurement definition)
    and provenance limitations are reported separately and never flip the
    verdict; ``new_measurement`` entries carry raw values and deltas without a
    historical target.
    """
    failed = [
        entry["field_id"]
        for entry in entries
        if entry.get("availability") == "measured" and entry.get("status") != "reproduced"
    ]
    not_measured = [
        entry["field_id"] for entry in entries if entry.get("availability") == "preserved_only"
    ]
    limitations = [
        entry["field_id"]
        for entry in entries
        if entry.get("availability") == "provenance_limitation"
    ]
    new_measurements = [
        entry["field_id"] for entry in entries if entry.get("status") == "new_measurement"
    ]
    required = [entry for entry in entries if entry.get("availability") == "measured"]
    return {
        "verdict": "withdrawn" if failed else "retained",
        "scope49_proposal": bool(failed),
        "failed_required": failed,
        "not_measured": not_measured,
        "provenance_limitations": limitations,
        "new_measurements": new_measurements,
        "required_count": len(required),
        "reproduced_count": sum(
            1 for entry in required if entry.get("status") == "reproduced"
        ),
    }


def new_measurement_entry(row_id, layer, value, *, deep_min_token=None, deep_max_token=None):
    """Record one individual deep-layer value as a NEW measurement (D-03).

    The original all-arm output printed only the h3..h12 min/max range, so an
    individual layer value has no historical target: it is retained with its
    raw value and its deltas to the registered range, never compared against an
    invented figure.
    """
    entry = {
        "field_id": f"{row_id}/{layer}",
        "status": "new_measurement",
        "layer": layer,
        "value": float(value),
    }
    deltas = {}
    if deep_min_token is not None:
        deltas["to_deep_min"] = float(value) - float(deep_min_token)
    if deep_max_token is not None:
        deltas["to_deep_max"] = float(value) - float(deep_max_token)
    if deltas:
        entry["delta"] = deltas
    return entry


# --------------------------------------------------------------------------
# The probe-only optimizer interlock
# --------------------------------------------------------------------------


@contextmanager
def optimizer_interlock():
    """Refuse optimizer construction and steps for the duration of the probe.

    Every ``torch.optim`` optimizer constructs through ``Optimizer.__init__``,
    so refusing it closes every construction path; each concrete optimizer
    defines its own ``step`` (the base method is never the one dispatched), so
    the interlock also refuses ``step`` on ``Optimizer`` and every loaded
    subclass. The context yields a counter of attempted (always refused) steps
    for the run record.
    """
    from torch.optim import Optimizer

    attempted = {"steps": 0}
    step_owners = [Optimizer]
    stack = list(Optimizer.__subclasses__())
    while stack:
        subclass = stack.pop()
        stack.extend(subclass.__subclasses__())
        if "step" in vars(subclass):
            step_owners.append(subclass)
    original_step_by_owner = [(owner, owner.__dict__.get("step")) for owner in step_owners]
    original_init = Optimizer.__init__

    def _refuse_init(_self, *args, **kwargs):
        raise ProbeInterlockRefused(
            "the diagnostic probe takes no optimizer step; optimizer construction refused"
        )

    def _refuse_step(_self, *args, **kwargs):
        attempted["steps"] += 1
        raise ProbeInterlockRefused(
            "the diagnostic probe takes no optimizer step; optimizer step refused"
        )

    Optimizer.__init__ = _refuse_init
    for owner, _original in original_step_by_owner:
        owner.step = _refuse_step
    try:
        yield attempted
    finally:
        Optimizer.__init__ = original_init
        for owner, original_step in original_step_by_owner:
            if original_step is None:
                del owner.step
            else:
                owner.step = original_step


def _parameter_digest(model):
    """A SHA-256 over the model's parameter tensors, compared around measurements."""
    digest = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        data = tensor.detach().cpu().contiguous()
        digest.update(name.encode("utf-8"))
        digest.update(str(tuple(data.shape)).encode("utf-8"))
        digest.update(str(data.dtype).encode("utf-8"))
        digest.update(data.numpy().tobytes())
    return digest.hexdigest()


# --------------------------------------------------------------------------
# Registration document
# --------------------------------------------------------------------------


def load_registration(registration_path):
    """Load and schema-check the registration document (read-only)."""
    path = Path(registration_path)
    if not path.is_file():
        raise RegistrationError(f"the registration file is missing: {path}")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise RegistrationError(f"the registration is not valid JSON: {exc}") from exc
    if not isinstance(doc, Mapping) or doc.get("schema") != PROBE_REGISTRATION_SCHEMA:
        raise RegistrationError(f"not a {PROBE_REGISTRATION_SCHEMA} registration")
    return doc


def _resolve_repo(repo_root, path):
    if repo_root is not None:
        return Path(repo_root).resolve()
    probe = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(Path(path).resolve().parent if Path(path).exists() else Path.cwd()),
        capture_output=True, text=True, check=False,
    )
    if probe.returncode == 0 and probe.stdout.strip():
        return Path(probe.stdout.strip()).resolve()
    return Path.cwd().resolve()


def _repo_relative(root, path):
    candidate = Path(path)
    if not candidate.is_absolute():
        return candidate.as_posix()
    try:
        return candidate.resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise RegistrationError("the path lies outside the repository") from exc


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _registration_text_entries(doc):
    """(relative path, recorded sha) for every enumerated text artifact."""
    entries = []
    page = doc.get("page")
    if isinstance(page, Mapping):
        entries.append((page["path"], page["sha256"]))
    source = doc.get("source")
    if isinstance(source, Mapping):
        for key in ("manifest", "stdout"):
            entry = source.get(key)
            if isinstance(entry, Mapping):
                entries.append((entry["path"], entry["sha256"]))
        for entry in source.get("scripts") or []:
            if isinstance(entry, Mapping):
                entries.append((entry["path"], entry["sha256"]))
    for entry in doc.get("code_dependencies") or []:
        if isinstance(entry, Mapping):
            entries.append((entry["path"], entry["sha256"]))
    for entry in doc.get("frozen") or []:
        if isinstance(entry, Mapping):
            entries.append((entry["path"], entry["sha256"]))
    for arm in doc.get("arms") or []:
        record = arm.get("record") if isinstance(arm, Mapping) else None
        if isinstance(record, Mapping):
            entries.append((record["path"], record["sha256"]))
    return entries


def check_registration(registration_path, *, repo_root=None):
    """Read-only committed-identity report — zero corpus or weight opens.

    Verifies the committed-clean admission (weight digests deliberately
    deferred to the run path), resolves the registration commit (the commit
    that introduced the expectations file, which must be an ancestor of HEAD)
    and reports the artifact digests. No probe result or attempt is created.
    """
    root = _resolve_repo(repo_root, registration_path)
    path = Path(registration_path)
    if not path.is_absolute():
        path = root / path
    relative = _repo_relative(root, path)
    doc = load_registration(path)
    require_committed_registration(path, repo_root=root, weight_digests=False)
    probe = subprocess.run(
        ["git", "log", "-n1", "--format=%H", "--diff-filter=A", "--", relative],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    if probe.returncode != 0 or not probe.stdout.strip():
        raise RegistrationRefused("the registration file has no introducing commit")
    commit = probe.stdout.strip().splitlines()[0]
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=str(root), capture_output=True, text=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RegistrationRefused(
            f"the registration commit {commit} is not an ancestor of HEAD"
        )
    artifacts = [
        {"path": relative_path, "sha256": _sha256_file(root / relative_path)}
        for relative_path, _recorded in _registration_text_entries(doc)
    ]
    artifacts.append({"path": relative, "sha256": _sha256_file(path)})
    return {
        "committed": True,
        "registration_commit": commit,
        "schema": doc["schema"],
        "artifacts": artifacts,
        "weight_digests": "deferred to the run admission",
    }


# --------------------------------------------------------------------------
# Measurement-to-field mapping (one shared implementation, never a copy)
# --------------------------------------------------------------------------


def _layer_row(measurement, name):
    for row in measurement.layers:
        if row.name == name:
            return row
    raise ProbeRefused(f"the measurement has no layer {name!r}")


def _deep_rows(measurement):
    return [row for row in measurement.layers if row.name in _DEEP_LAYERS]


FIELD_EXTRACTORS = {
    "frequency_median": lambda measurement: measurement.frequency_median,
    "frequency_max": lambda measurement: measurement.frequency_max,
    "adj_input": lambda measurement: _layer_row(measurement, "input").adjacent_cosine_mean,
    "out_move": lambda measurement: measurement.output_movement,
    "rate_ratio": lambda measurement: measurement.output_rate_ratio,
    "deep_min": lambda measurement: min(row.adjacent_cosine_mean for row in _deep_rows(measurement)),
    "deep_max": lambda measurement: max(row.adjacent_cosine_mean for row in _deep_rows(measurement)),
}
for _index in range(1, 13):
    FIELD_EXTRACTORS[f"adj_h{_index}"] = (
        lambda name: lambda measurement: _layer_row(measurement, name).adjacent_cosine_mean
    )(f"h{_index}")


# --------------------------------------------------------------------------
# Default seams (never exercised by this plan's synthetic suite)
# --------------------------------------------------------------------------


def _load_state_weights(weights_path, recorded_sha256):
    """Hash-before-load: the recorded digest must agree before deserialization."""
    from pinn.verification.diagnostic_guard import DiagnosticRegistrationRefused

    disk = _sha256_file(weights_path)
    if disk != recorded_sha256:
        raise DiagnosticRegistrationRefused(
            f"weights SHA-256 {disk} != recorded {recorded_sha256} for {weights_path}"
        )
    weights = torch.load(weights_path, map_location="cpu", weights_only=True)
    if not isinstance(weights, Mapping):
        raise ProbeRefused(f"the weights file {weights_path} is not a state mapping")
    return OrderedDict(
        (name, tensor.detach().cpu().to(torch.float64)) for name, tensor in weights.items()
    )


def default_model_factory(first_omega_0, state, weights_entry):
    """Build the CPU float64 seed-42 reconstruction; load recorded states last.

    The reconstruction is labelled a reconstruction: CPU float64 seed-42
    initialization is NOT the historical MPS float32 training initialization
    (D-04). A recorded state is deserialized only after its committed record
    and weight SHA-256 agree, with ``weights_only=True`` and a CPU map
    location.
    """
    from pinn.architecture_spec import ArchitectureSpec
    from pinn.network import build_network
    from pinn.verification.diagnostic_architecture import build_network_with_first_omega
    from pinn.verification.learnability_arms import SEED

    device = torch.device("cpu")
    if abs(float(first_omega_0) - 30.0) < 1e-9:
        model = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=device)
    else:
        model = build_network_with_first_omega(
            float(first_omega_0), seed=SEED, dtype=torch.float64, device=device
        )
    if weights_entry is not None:
        state_dict = _load_state_weights(weights_entry["path"], weights_entry["sha256"])
        model.load_state_dict(state_dict)
    return model


def default_probe_loader(repo_root, *, scorecard=None):
    """The guarded-seam data loader: Stage-0 TRAIN admission before every open."""
    from pinn.verification.diagnostic_data import (
        load_diagnostic_data,
        open_diagnostic_context,
    )
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.learnability_arms import arm_spec

    context = open_diagnostic_context(repo_root=Path(repo_root))
    card = scorecard if scorecard is not None else load_scorecard()
    cache = {}
    attestations = {}

    def loader(arm_id):
        if arm_id not in cache:
            arm = load_diagnostic_data(
                arm_spec(arm_id), context, scorecard=card,
                dtype=torch.float64, device=torch.device("cpu"),
            )
            train_summary = arm.records["train"]
            attestations[arm_id] = {
                "record_key": train_summary["record_key"],
                "split": train_summary["split"],
                "n_within_window": train_summary["n_within_window"],
                "requested_window": train_summary["requested_window"],
                "source": "the Stage-0 guarded seam records split and stage on every open",
            }
            cache[arm_id] = (
                arm.data_points.tau_ic13,
                arm.data_points.masses,
                arm.data_points.targets,
                arm.records["train"]["times_physical"],
            )
        return cache[arm_id]

    loader.attestations = attestations
    return loader


# --------------------------------------------------------------------------
# The read-only run
# --------------------------------------------------------------------------


def _exclusive_write(path, payload):
    """Create ``path`` exactly once (O_CREAT | O_EXCL); never replace."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        descriptor = os.open(path, flags, 0o644)
    except FileExistsError as exc:
        raise AttemptExists(
            f"{path.name} already exists; the first result is the result and a "
            "second run never replaces it (no automatic retry)"
        ) from exc
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def _git_head(root):
    probe = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, check=False
    )
    if probe.returncode != 0:
        raise ProbeRefused("the run needs a git commit to record as its run commit")
    return probe.stdout.strip()


def _write_attempt(output_dir, doc, root, registration_relative, result_path):
    attempt = {
        "schema": PROBE_ATTEMPT_SCHEMA,
        "status": "incomplete",
        "registration": {
            "path": registration_relative,
            "sha256": _sha256_file(root / registration_relative),
        },
        "run_commit": _git_head(root),
        "result_path": Path(result_path).as_posix(),
        "no_automatic_retry": True,
        "note": "a claim, not an outcome; the outcome is reproduction.json",
    }
    payload = (json.dumps(attempt, indent=2) + "\n").encode("utf-8")
    _exclusive_write(Path(output_dir) / "attempt.json", payload)
    return attempt


def _measure_row(model, tensors):
    """One shared-implementation measurement with the parameter digest guard."""
    tau_ic13, masses, targets, times = tensors
    before = _parameter_digest(model)
    measurement = measure_time_signal(model, tau_ic13, masses, targets, times)
    after = _parameter_digest(model)
    if before != after:
        raise ProbeInterlockRefused(
            "the model's parameter tensors changed during measurement; refusing"
        )
    return measurement, before, after


def _compare_registered(row_fields, measurement, field_prefix):
    verdicts = []
    for name, expected in row_fields.items():
        availability = expected.get("availability", "measured")
        if availability != "measured":
            # A preserved-only field has no shared-measurement definition (and
            # a second reduction is forbidden): it is recorded for the reading
            # rule to report separately, never compared and never fabricated.
            verdicts.append({
                "field_id": f"{field_prefix}/{name}",
                "availability": availability,
                "token": expected.get("token"),
                "formatter": expected.get("formatter"),
                "reason": expected.get("reason", "no shared measurement implementation"),
            })
            continue
        extractor = FIELD_EXTRACTORS.get(name)
        if extractor is None:
            raise RegistrationError(f"no shared measurement is registered for {name!r}")
        value = extractor(measurement)
        verdict = compare_field(expected, value)
        verdicts.append({
            "field_id": f"{field_prefix}/{name}",
            "availability": availability,
            **verdict,
        })
    return verdicts


def _new_measurement_rows(row, measurement, field_prefix):
    entries = []
    deep_min = row["fields"].get("deep_min", {}).get("token")
    deep_max = row["fields"].get("deep_max", {}).get("token")
    for row_ in measurement.layers:
        field_name = f"adj_{row_.name}"
        if row_.name not in _DEEP_LAYERS or field_name in row["fields"]:
            continue
        entries.append(
            new_measurement_entry(
                field_prefix, row_.name, row_.adjacent_cosine_mean,
                deep_min_token=deep_min, deep_max_token=deep_max,
            )
        )
    return entries


def _validate_probe_spec(doc):
    probe_spec = doc.get("probe")
    if not isinstance(probe_spec, Mapping):
        raise RegistrationError("the registration names no probe section")
    registered_ids = [arm.get("arm_id") for arm in doc["arms"]]
    rows_by_arm = {}
    for entry in probe_spec.get("arms") or []:
        rows_by_arm[entry["arm_id"]] = entry
    missing = [arm_id for arm_id in registered_ids if arm_id not in rows_by_arm]
    if missing:
        raise RegistrationError(f"the probe section is missing rows for arms: {missing}")
    return probe_spec, rows_by_arm


def run_probe(
    registration_path,
    *,
    repo_root=None,
    output_dir,
    result_path=None,
    data_loader=None,
    model_factory=None,
):
    """Run the read-only historical probe under the committed registration.

    Admission (``require_committed_registration`` with weight digests) happens
    BEFORE any data resolution, weight deserialization or attempt creation.
    The attempt is claimed exclusively; an interrupted or exceptional attempt
    stays explicitly incomplete and never publishes a result; a complete run
    writes an exclusive result (even when figures fail) plus
    ``reproduction.stdout.txt`` beside it. No optimizer can be constructed or
    stepped, attempted steps are counted, and parameter digests are compared
    around every measurement.
    """
    root = _resolve_repo(repo_root, registration_path)
    path = Path(registration_path)
    if not path.is_absolute():
        path = root / path
    registration_relative = _repo_relative(root, path)
    doc = load_registration(path)
    require_committed_registration(path, repo_root=root, weight_digests=True)
    probe_spec, rows_by_arm = _validate_probe_spec(doc)
    output_dir = Path(output_dir)
    result_path = Path(result_path) if result_path is not None else output_dir / "reproduction.json"
    attempt = _write_attempt(output_dir, doc, root, registration_relative, result_path)

    loader = data_loader if data_loader is not None else default_probe_loader(root)
    build_model = model_factory if model_factory is not None else default_model_factory
    loaded = {}

    def cached_loader(arm_id):
        if arm_id not in loaded:
            loaded[arm_id] = loader(arm_id)
        return loaded[arm_id]

    verdicts = []
    new_measurements = []
    arm_records = []
    parity_entry = None
    parity_block = None
    digest_pairs = []
    try:
        with optimizer_interlock() as attempted:
            models = {}
            for arm in doc["arms"]:
                arm_id = arm["arm_id"]
                tensors = cached_loader(arm_id)
                entry = rows_by_arm[arm_id]
                arm_digests = {}
                for row in entry["rows"]:
                    state = row["state"]
                    if state == "init":
                        weights_entry = None
                    else:
                        weights_entry = arm["weights"].get(state)
                        if weights_entry is None:
                            raise RegistrationError(
                                f"row state {state!r} for {arm_id} names no committed weights"
                            )
                    cache_key = (arm_id, state)
                    if cache_key not in models:
                        models[cache_key] = build_model(
                            arm.get("first_omega_0", 30.0), state, weights_entry
                        )
                    measurement, before, after = _measure_row(models[cache_key], tensors)
                    arm_digests[state] = (before, after)
                    prefix = f"{arm_id}/{state}"
                    verdicts.extend(
                        _compare_registered(row["fields"], measurement, prefix)
                    )
                    if entry.get("new_measurements", row.get("new_measurements", False)):
                        new_measurements.extend(
                            _new_measurement_rows(row, measurement, prefix)
                        )
                    arm_records.append({
                        "arm_id": arm_id,
                        "state": state,
                        "rows": [
                            {"name": row.name, "order": row.order,
                             "adjacent_cosine_mean": row.adjacent_cosine_mean}
                            for row in measurement.layers
                        ],
                        "first_layer_frequency": {
                            "median": measurement.frequency_median,
                            "max": measurement.frequency_max,
                        },
                        "output_movement": measurement.output_movement,
                        "output_rate_ratio": measurement.output_rate_ratio,
                    })
                supplement = (probe_spec.get("supplement") or {})
                if supplement.get("arm_id") == arm_id:
                    for state, supplement_entry in supplement.get("states", {}).items():
                        weights_entry = arm["weights"].get(state)
                        if weights_entry is None:
                            raise RegistrationError(
                                f"supplement state {state!r} names no committed weights"
                            )
                        cache_key = (arm_id, state)
                        if cache_key not in models:
                            models[cache_key] = build_model(
                                arm.get("first_omega_0", 30.0), state, weights_entry
                            )
                        measurement, before, after = _measure_row(models[cache_key], tensors)
                        arm_digests.setdefault(state, (before, after))
                        verdicts.extend(
                            _compare_registered(
                                supplement_entry.get("fields", {}),
                                measurement,
                                f"supplement/{state}",
                            )
                        )
                        if supplement_entry.get("new_measurements", True):
                            new_measurements.extend(
                                _new_measurement_rows(
                                    {"fields": supplement_entry.get("fields", {})},
                                    measurement,
                                    f"supplement/{state}",
                                )
                            )
                for pair in arm_digests.values():
                    digest_pairs.append({"before": pair[0], "after": pair[1]})
            parity_spec = probe_spec.get("logger_parity")
            if isinstance(parity_spec, Mapping):
                from pinn.verification.diagnostic_fit import log_similarity

                parity_arm = parity_spec["arm_id"]
                parity_state = parity_spec["state"]
                arm = next(a for a in doc["arms"] if a["arm_id"] == parity_arm)
                weights_entry = arm["weights"].get(parity_state)
                if weights_entry is None:
                    raise RegistrationError(
                        f"the logger-parity state {parity_state!r} names no committed weights"
                    )
                tensors = cached_loader(parity_arm)
                cache_key = (parity_arm, parity_state)
                if cache_key not in models:
                    models[cache_key] = build_model(
                        arm.get("first_omega_0", 30.0), parity_state, weights_entry
                    )
                tau_ic13, masses, targets, times = tensors
                parity_entry = log_similarity(
                    models[cache_key],
                    SimpleNamespace(tau_ic13=tau_ic13, masses=masses, targets=targets),
                    times,
                    step=-1,
                    point=LOGGER_PARITY_POINT,
                )
                parity_block = {
                    "arm_id": parity_arm,
                    "state": parity_state,
                    "without_updates": True,
                    "entry": parity_entry,
                }
    except BaseException:
        # The attempt stays explicitly incomplete; no result exists or is replaced.
        raise

    reading_rule = evaluate_reading_rule(verdicts)
    # A run-level aggregate over every measurement's digest pair: the two
    # hashes agree exactly when every model's parameters were unchanged from
    # before to after its measurement.
    aggregate_before = hashlib.sha256(
        "".join(pair["before"] for pair in digest_pairs).encode("utf-8")
    ).hexdigest() if digest_pairs else ""
    aggregate_after = hashlib.sha256(
        "".join(pair["after"] for pair in digest_pairs).encode("utf-8")
    ).hexdigest() if digest_pairs else ""
    result = {
        "schema": PROBE_RESULT_SCHEMA,
        "status": "complete",
        "registration": {
            "path": registration_relative,
            "sha256": _sha256_file(root / registration_relative),
        },
        "run_commit": attempt["run_commit"],
        "attempt": {
            "path": (output_dir / "attempt.json").as_posix(),
            "status": "incomplete-claim (the result is this file)",
        },
        "reading_rule": reading_rule,
        "field_verdicts": verdicts,
        "new_measurements": new_measurements,
        "arms": arm_records,
        "logger_parity": parity_block,
        "access": {
            "requested_arms": [arm["arm_id"] for arm in doc["arms"]],
            "attestations": dict(getattr(loader, "attestations", {})),
            "note": "actual split/stage accesses are attested by the guarded seam's per-record summaries",
        },
        "interlock": {
            "attempted_steps": attempted["steps"],
            "parameter_digest_before": aggregate_before,
            "parameter_digest_after": aggregate_after,
            "parameter_digest_pairs": digest_pairs,
            "match": all(pair["before"] == pair["after"] for pair in digest_pairs),
            "no_optimizer_path": True,
        },
        "no_retry": True,
    }
    _exclusive_write(result_path, (json.dumps(result, indent=2) + "\n").encode("utf-8"))
    _exclusive_write(
        result_path.parent / "reproduction.stdout.txt",
        _render_stdout(result).encode("utf-8"),
    )
    return result


def _render_stdout(result):
    """The human-readable rendering written beside reproduction.json."""
    lines = [
        "DIAG-09 reproduction (registered rule: exact formatter equality)",
        f"run commit: {result['run_commit']}",
        f"reading rule: {result['reading_rule']['verdict']}"
        + (" (SCOPE-49 proposal)" if result["reading_rule"]["scope49_proposal"] else ""),
        "",
    ]
    for arm in result["arms"]:
        lines.append(
            f"{arm['arm_id']:<15}{arm['state']:<8}"
            f"cyc {arm['first_layer_frequency']['median']:.2f} "
            f"move {arm['output_movement']:.4f} "
            f"rate {arm['output_rate_ratio']:.3g}"
        )
    lines.append("")
    for verdict in result["field_verdicts"]:
        lines.append(
            f"{verdict['field_id']}: measured {verdict['measured']:.6g} rendered "
            f"{verdict['rendered']} vs token {verdict['token']} -> {verdict['status']}"
        )
    for entry in result["new_measurements"]:
        lines.append(
            f"{entry['field_id']}: new measurement {entry['value']:.6g} "
            f"(deltas: {entry.get('delta', {})})"
        )
    if result["reading_rule"]["not_measured"]:
        lines.append("")
        lines.append(
            "preserved, not measured by the shared implementation: "
            + ", ".join(result["reading_rule"]["not_measured"])
        )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Result verification
# --------------------------------------------------------------------------


def verify_result(result_path, *, repo_root=None, logger_parity_path=None):
    """Verify a probe result: complete outcome, correct branch, run-commit deps.

    The reading rule is recomputed from the per-field verdicts, so a recorded
    verdict that contradicts its own fields is refused. Historical code
    dependencies are verified against the RECORDED RUN COMMIT (the bytes that
    actually ran), not against later source bytes: a legitimate later change to
    a dependency never invalidates an old result, while a result claiming a
    commit where the dependencies did not match is refused.
    """
    root = _resolve_repo(repo_root, result_path)
    path = Path(result_path)
    if not path.is_absolute():
        path = root / path
    try:
        result = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise RegistrationError(f"the result is not valid JSON: {exc}") from exc
    if not isinstance(result, Mapping) or result.get("schema") != PROBE_RESULT_SCHEMA:
        raise RegistrationError(f"not a {PROBE_RESULT_SCHEMA} result")
    if result.get("status") != "complete":
        raise ProbeRefused(
            "an interrupted attempt never verifies; only a complete result does"
        )
    recomputed = evaluate_reading_rule(result.get("field_verdicts") or [])
    recorded_rule = result.get("reading_rule") or {}
    if recomputed["verdict"] != recorded_rule.get("verdict") \
            or recomputed["scope49_proposal"] != recorded_rule.get("scope49_proposal"):
        raise ProbeRefused(
            "the recorded reading-rule verdict contradicts the recorded field verdicts"
        )
    registration_relative = (result.get("registration") or {}).get("path")
    registration_recorded = (result.get("registration") or {}).get("sha256")
    if not registration_relative or not registration_recorded:
        raise RegistrationError("the result does not record its registration")
    registration_file = root / registration_relative
    if _sha256_file(registration_file) != registration_recorded:
        raise ProbeRefused("the registration bytes changed since the run")
    run_commit = result.get("run_commit")
    if not run_commit:
        raise ProbeRefused("the result does not record its run commit")

    doc = load_registration(registration_file)
    dependencies = doc.get("code_dependencies") or []
    for entry in dependencies:
        show = subprocess.run(
            ["git", "show", f"{run_commit}:{entry['path']}"],
            cwd=str(root), capture_output=True, check=False,
        )
        if show.returncode != 0:
            raise ProbeRefused(
                f"the run commit {run_commit} has no {entry['path']}; the result "
                "cannot be tied to the code that ran"
            )
        digest = hashlib.sha256(show.stdout).hexdigest()
        if digest != entry["sha256"]:
            raise ProbeRefused(
                f"code dependency {entry['path']} differs at the run commit "
                f"({digest} != {entry['sha256']})"
            )
    if logger_parity_path is not None:
        parity_file = Path(logger_parity_path)
        if not parity_file.is_absolute():
            parity_file = root / parity_file
        recorded = (result.get("logger_parity") or {}).get("entry")
        if recorded is None:
            raise ProbeRefused("the result records no logger-parity entry to compare")
        try:
            expected = json.loads(parity_file.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise RegistrationError(f"the logger-parity record is not valid JSON: {exc}") from exc
        if expected != recorded:
            raise ProbeRefused(
                "the supplied logger-parity record does not match the result's recorded entry"
            )
    return {
        "verified": True,
        "run_commit": run_commit,
        "verdict": recomputed["verdict"],
        "dependencies_checked": [entry["path"] for entry in dependencies],
    }


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------


def main(argv=None, *, repo_root=None):
    """The probe CLI: check-registration / run / verify-result."""
    parser = argparse.ArgumentParser(
        prog="diagnostic_probe",
        description="Read-only DIAG-09 probe: registration, run and verification gates.",
    )
    commands = parser.add_subparsers(dest="command")
    check = commands.add_parser("check-registration")
    check.add_argument("--registration", required=False)
    run = commands.add_parser("run")
    run.add_argument("--registration", required=False)
    run.add_argument("--result", required=False)
    run.add_argument("--output", required=False)
    verify = commands.add_parser("verify-result")
    verify.add_argument("--result", required=False)
    verify.add_argument("--logger-parity", default=None)
    args = parser.parse_args(argv)

    required = {
        "check-registration": ["registration"],
        "run": ["registration", "result", "output"],
        "verify-result": ["result"],
    }.get(args.command)
    if args.command is None or required is None:
        print("PROBE-REFUSED: choose check-registration, run or verify-result", file=sys.stderr)
        return 2
    missing = [f"--{name}" for name in required if getattr(args, name) is None]
    if missing:
        print(f"PROBE-REFUSED: missing required flags: {', '.join(missing)}", file=sys.stderr)
        return 2
    try:
        if args.command == "check-registration":
            report = check_registration(args.registration, repo_root=repo_root)
            print(
                f"CHECK-REGISTRATION-OK registration-commit={report['registration_commit']}"
            )
            for artifact in report["artifacts"]:
                print(f"  {artifact['sha256']}  {artifact['path']}")
            return 0
        if args.command == "run":
            result = run_probe(
                args.registration,
                repo_root=repo_root,
                output_dir=args.output,
                result_path=args.result,
            )
            print(
                f"PROBE-RUN-COMPLETE verdict={result['reading_rule']['verdict']} "
                f"result={args.result}"
            )
            return 0
        verify_result(
            args.result,
            repo_root=repo_root,
            logger_parity_path=args.logger_parity,
        )
        print("VERIFY-RESULT-OK")
        return 0
    except (ProbeRefused, DiagnosticRegistrationRefused, RegistrationError) as exc:
        print(f"PROBE-REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
