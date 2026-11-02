"""Phase 67: the registration-bound diagnostic run reader.

``read_phase67_record`` reads one Phase 67 run directory against its committed
fit registration: the registration is admitted through the existing
committed-registration door (metadata-only, before any corpus access), its
settings must name the Phase 67 registry, and the run's record, weights,
power-gate receipt and attempt claim are audited into value-free
``mechanical_problems`` and ``setting_problems`` lists beside the registered
identity — the reader derives its expectations from the registration, never
from the record. Frozen scores are exposed only when ``include_scores`` is
requested AND the audit is clean.

``read_phase67_run_directory`` (plan 67-05, D-12/D-13) is the science
reading: the registration must additionally declare the registered Phase 67
checkpoint schedule and commit its window metadata (the retained grid's
endpoint, sample count and both sha256 digests) and independently recomputed
same-window baselines, and the run directory is validated in a strict staged
order — JSON/object/list/scalar shapes, then identity/settings against the
declared matrix row, then the evidence links (record/weights/receipt/attempt
digests, contained local weight basenames, symlink checks before any open),
then the numeric and scientific fields (every layer row exactly once in
order, finite cosines in [-1, 1], output movement and rate, strictly
increasing actual physical and raw-tau coordinates against the committed grid
digests, raw frequency evidence or the registered encoded nonapplicability
and feature metadata, the frozen E/tier consistency of the endpoint and every
checkpoint, the same-window baselines with formula nonapplicability retained,
the access evidence with at least one TRAIN read, the aware receipt and
attempt instants with the weekday derived from the receipt's own instant, the
AC first line, the checked-before-start-before-end order, the launch-to-end
wall inside the registered cap, and the cap fitting the derived Sunday 22:00
closing instant exactly at the boundary). The reading carries the identity,
actual coordinates, layer trace, checkpoint steps, the observed fit and the
final-quarter ``unsettled`` flag; scores appear only after a clean audit, so
a malformed record never yields an accuracy direction. Command wrappers in
67-06 translate the problem lists to exit 2.

The reader owns no scientific branch table: the EXP-02..05 confirmation rules
live in ``diagnostic_phase67`` (plan 67-05 task 2) and consume only
mechanically clean readings. This module imports the fit harness lazily
(inside the readers), so the catalog module the harness imports at module
level never sees a cycle. The window and receipt constants come from the
launcher itself, so the gate and the auditor cannot drift apart.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
from collections.abc import Mapping
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from pinn.verification.diagnostic_phase67_catalog import (
    PHASE67_ARMS,
    PHASE67_REGISTRY_NAME,
)
from pinn.verification.diagnostic_power import (
    AC_SOURCE,
    RECEIPT_SCHEMA,
    WINDOW_SUNDAY_LAST_HOUR,
    WINDOW_TIMEZONE,
    power_source,
)

__all__ = [
    "Phase67RecordRefused",
    "read_phase67_record",
    "read_phase67_run_directory",
    "registered_layers",
]

# Value-free mechanical problem strings: none embeds a score value, so a
# caller can print the problems without exposing an unread score.
_PROBLEM_FIT_AUDIT = "the result fails the registration-bound fit verification"
_PROBLEM_RECORD_UNREADABLE = "the record is not a readable diagnostic record"
_PROBLEM_LAYERS = (
    "the similarity log does not carry exactly the registered layers in order"
)
_PROBLEM_TIER = "the recorded scorecard grade disagrees with the network error"
_PROBLEM_ACCESS = "the record carries no access evidence"
_PROBLEM_SPLITS = "a validation or test split was opened"
_PROBLEM_RECEIPT_MISSING = "the power-gate receipt is missing"
_PROBLEM_RECEIPT_UNREADABLE = "the power-gate receipt is not a readable JSON object"
_PROBLEM_RECEIPT_SCHEMA = "the receipt schema is not the launcher's power-gate schema"
_PROBLEM_RECEIPT_SOURCE = "the receipt does not record AC Power"
_PROBLEM_RECEIPT_WINDOW = "the receipt window is outside the weekend window"
_PROBLEM_TIMESTAMPS = (
    "a receipt or attempt timestamp is missing or not timezone-aware ISO 8601"
)
_PROBLEM_RECEIPT_LATE = "the receipt was written after the attempt started"
_PROBLEM_ATTEMPT_MISSING = "the attempt claim is missing"
_PROBLEM_ATTEMPT_UNREADABLE = "the attempt claim is not a readable JSON object"
_PROBLEM_ATTEMPT_STATUS = "the attempt is not published"
_PROBLEM_ATTEMPT_DIGEST = (
    "the attempt's record digest disagrees with the record bytes"
)

# Plan 67-05 task 67-05-01: the science reading's staged problems (value-free;
# none embeds a score, so a caller can print the lists without exposing an
# unread score).
_PROBLEM_SCHEDULE = (
    "the recorded checkpoint schedule is not the registered Phase 67 schedule"
)
_PROBLEM_COSINE = "a layer row carries an unusable adjacent-time cosine"
_PROBLEM_MOVEMENT = "a similarity entry carries an unusable output movement or rate"
_PROBLEM_COORDINATES = (
    "the recorded time coordinates are not finite and strictly increasing"
)
_PROBLEM_GRID = "the recorded grid disagrees with the committed window metadata"
_PROBLEM_BASELINE = (
    "the recorded same-window baselines disagree with the committed expectations"
)
_PROBLEM_RAW_FREQUENCY = "a raw-input run carries no finite first-layer frequency"
_PROBLEM_ENCODED_FREQUENCY = (
    "an encoded run's frequency evidence is not the registered nonapplicability "
    "and feature metadata"
)
_PROBLEM_TRAIN_ACCESS = "the record attests no TRAIN access"
_PROBLEM_UNSAFE_PATH = "a record-named file resolves outside the run directory"
_PROBLEM_SYMLINK = "the run evidence replaces a file with a symbolic link"
_PROBLEM_ATTEMPT_ORDER = (
    "the attempt does not start after the receipt or end after its start"
)
_PROBLEM_ATTEMPT_CAP = "the attempt's whole-run cap disagrees with the registration"
_PROBLEM_ATTEMPT_STEPS = "the attempt's completed steps disagree with the record"
_PROBLEM_LAUNCH_WALL = (
    "the launch-to-end wall exceeds the registered whole-launch cap"
)
_PROBLEM_SUNDAY_CAP = (
    "the registered whole-launch cap does not fit before the Sunday 22:00 "
    "closing instant"
)
_PROBLEM_AC_FIRST_LINE = "the receipt's recorded pmset first line does not name AC Power"
_PROBLEM_IMPROVEMENT = (
    "the recorded score checkpoints cannot settle the final-quarter improvement"
)

# Setting problems: the run's registered identity disagrees with the declared
# matrix row (the caller's committed experiment/arm/case identity).
_SETTING_EXPERIMENT = "the matrix row names no known Phase 67 experiment"
_SETTING_ARM = "the run's variant is not the matrix row's arm"
_SETTING_CASE = "the matrix row names no registered case role"
_SETTING_ORBIT = "the run's orbit is not the matrix row's orbit"
_SETTING_SEED = "the run's seed is not the matrix row's seed"

#: The three D-09 confirmation case roles a matrix row may name.
_CASE_ROLES = ("main", "repeat-system", "repeat-seed")

#: The registered EXP-05 window arm names (D-06); their variant declarations
#: arrive with the window registration plans, so only the names bind here.
_EXP05_WINDOW_ARMS = ("lap1", "lap2", "lap5", "lap10")


def _finite_number(value):
    """A finite float excluding booleans, or ``None``."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _strictly_increasing(values):
    """Every value finite and the sequence strictly increasing."""
    if not isinstance(values, list) or not values:
        return False
    numbers = [_finite_number(value) for value in values]
    if any(number is None for number in numbers):
        return False
    return all(
        left < right for left, right in zip(numbers, numbers[1:])
    )


def _float64_digest(values):
    """The 67-03 windows evidence digest convention over plain Python floats."""
    packed = struct.pack(
        f"<{len(values)}d", *[float(value) for value in values]
    )
    return hashlib.sha256(packed).hexdigest()


def _sunday_closing(local):
    """That weekend's Sunday 22:00 ``WINDOW_TIMEZONE`` closing instant.

    ``local`` is the receipt's own aware instant in the window timezone. A
    Saturday derives the next day's 22:00; a Sunday derives the same day's
    22:00; any other weekday has no closing instant (the window check is what
    flags it). Wall-clock construction keeps DST transitions exact.
    """
    if local.isoweekday() == 6:
        day = local.date() + timedelta(days=1)
    elif local.isoweekday() == 7:
        day = local.date()
    else:
        return None
    return datetime(
        day.year, day.month, day.day,
        int(WINDOW_SUNDAY_LAST_HOUR), 0, 0,
        tzinfo=ZoneInfo(WINDOW_TIMEZONE),
    )


def _tier_consistent(score, card):
    """A score row's frozen E/tier/eps_h consistency, shape-guarded."""
    from pinn.verification.feasibility_scorecard import tier_of

    if not isinstance(score, Mapping):
        return False
    e_value = _finite_number(score.get("E"))
    eps = _finite_number(score.get("eps_h"))
    tier = score.get("tier")
    if e_value is None or e_value < 0.0 or eps is None:
        return False
    if isinstance(tier, bool) or not isinstance(tier, int):
        return False
    try:
        return int(tier) == int(tier_of(e_value, eps, scorecard=card))
    except Exception:
        return False


def _improvement_unsettled(checkpoints):
    """The reading's ``unsettled`` field: the canonical registered rule.

    ``phase67_improvement_check`` (plan 67-05 task 2) is the single
    implementation of the final-quarter improvement rule — strictly greater
    than the five-percent threshold leaves the endpoint unsettled, exactly
    five percent is settled, and a zero reference is settled either way. The
    reader maps its verdict onto the reading's flag, and a refusal (a
    negative, non-finite or malformed checkpoint E, a wrong count or
    non-increasing steps) becomes ``None``: the reading records the
    improvement problem instead of guessing a settlement.
    """
    from pinn.verification.diagnostic_phase67 import phase67_improvement_check

    try:
        return not phase67_improvement_check(checkpoints)["settled"]
    except (ValueError, TypeError):
        return None


def _matrix_row_problems(row, settings, variant):
    """The setting problems of a declared matrix row against the run."""
    problems = []
    experiment = row["experiment"]
    if experiment not in PHASE67_ARMS and experiment != "exp05":
        problems.append(_SETTING_EXPERIMENT)
    elif experiment in PHASE67_ARMS:
        declaration = PHASE67_ARMS[experiment].get(row["arm"])
        if declaration is None or declaration.name != variant.name:
            problems.append(_SETTING_ARM)
    elif row["arm"] not in _EXP05_WINDOW_ARMS:
        # The exp05 variant declarations arrive with the window registration
        # plans; until then only the registered arm names bind.
        problems.append(_SETTING_ARM)
    if row["case"] not in _CASE_ROLES:
        problems.append(_SETTING_CASE)
    if row["orbit_key"] != settings["orbit_key"]:
        problems.append(_SETTING_ORBIT)
    if row["seed"] != int(settings["seed"]):
        problems.append(_SETTING_SEED)
    return problems


def _validate_matrix_row(expected_case):
    """One well-formed declared matrix row, or ``ValueError``."""
    if not isinstance(expected_case, Mapping):
        raise ValueError(
            f"the declared matrix row must be a mapping; got {expected_case!r}"
        )
    for field in ("experiment", "arm", "case", "orbit_key"):
        value = expected_case.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"the matrix row {field} must be non-empty text; got {value!r}"
            )
    seed = expected_case.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError(f"the matrix row seed must be an integer; got {seed!r}")
    return {
        "experiment": expected_case["experiment"],
        "arm": expected_case["arm"],
        "case": expected_case["case"],
        "orbit_key": expected_case["orbit_key"],
        "seed": int(seed),
    }


class Phase67RecordRefused(RuntimeError):
    """The Phase 67 reader cannot read this run directory at all."""


def registered_layers(depth):
    """The layer rows a fit at ``depth`` hidden layers logs, in order.

    The shared similarity logger hooks the input layer as ``input`` and each
    hidden layer as ``h1``..``h{depth}``; the order is the hook order, so a
    registered depth fixes the expected row names deterministically.
    """
    count = int(depth)
    if count < 1:
        raise ValueError(f"a diagnostic depth is at least 1; got {depth!r}")
    return ["input"] + [f"h{order}" for order in range(1, count + 1)]


def _read_json_object(path):
    """The parsed JSON object at ``path``, or ``None`` when unreadable."""
    try:
        payload = json.loads(Path(path).read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _aware_datetime(value):
    """The timezone-aware datetime in ``value``, or ``None``."""
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return None
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        return None
    return moment


def _receipt_window_ok(window):
    """The receipt's window block, audited on its own local time.

    The declared ``isoweekday`` must agree with the weekday the recorded
    ``local_time`` itself carries (a self-declared weekday is not evidence),
    and the Chicago local time must sit inside the owner's weekend window.
    """
    if not isinstance(window, Mapping):
        return False
    declared = window.get("isoweekday")
    if isinstance(declared, bool) or not isinstance(declared, int):
        return False
    if window.get("timezone") != WINDOW_TIMEZONE:
        return False
    moment = _aware_datetime(window.get("local_time"))
    if moment is None:
        return False
    try:
        local = moment.astimezone(ZoneInfo(WINDOW_TIMEZONE))
    except (ValueError, OSError):
        return False
    if local.isoweekday() != declared:
        return False
    return local.isoweekday() == 6 or (
        local.isoweekday() == 7 and local.hour < WINDOW_SUNDAY_LAST_HOUR
    )


def _split_opens(record):
    """``(opens, access_present)`` from the record's own access evidence.

    Fail-closed: a record whose access block is missing cannot attest
    TRAIN-only access, so the caller flags it separately from any counted
    validation or test split open.
    """
    access = record.get("access")
    if not isinstance(access, Mapping):
        return 0, False
    total = 0
    blocks = [access.get("reads"), access.get("attestation")]
    attestation = access.get("attestation")
    if isinstance(attestation, Mapping):
        blocks.append(attestation.get("opened"))
    for block in blocks:
        if not isinstance(block, Mapping):
            continue
        for key in ("validation", "test", "test_split_opened", "test_split_opens"):
            value = block.get(key, 0)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            total += int(value)
    return total, True


def _tier1_max():
    """The frozen scorecard's Tier-1 E limit, read from the scorecard itself."""
    from pinn.verification.diagnostic_phase66 import tier1_e_max
    from pinn.verification.feasibility_scorecard import load_scorecard

    return tier1_e_max(load_scorecard())


def read_phase67_record(registration_path, run_dir, *, repo_root, include_scores=False):
    """One Phase 67 run directory read against its committed registration.

    The registration is admitted first (committed-clean artifacts, settings
    against the registry, the logger-parity receipt — all metadata-only, no
    corpus opens), and its settings must name the Phase 67 registry; anything
    else is a typed refusal, as is a run directory with no ``record.json``.
    The record is then audited through the existing registration-bound
    ``verify_fit_result`` plus the receipt, attempt, layer-row, split and
    tier-consistency checks into value-free problem lists. Returns the
    registered identity (registration citation, variant, orbit key, seed,
    runtime, physical window and the expected layer rows) with
    ``mechanical_problems`` and ``setting_problems``; ``setting_problems`` is
    reserved for the experiment-specific reading rules of later plans, so it
    is empty on every clean raw-path reading today. With ``include_scores``
    the frozen network score and both comparison rows are added — only when
    the audit is clean, otherwise a typed refusal.
    """
    from pinn.verification.diagnostic_fit import (
        RECORD_NAME,
        DiagnosticFitRefused,
        require_committed_smoke_registration,
        validate_smoke_settings,
        verify_fit_result,
    )
    from pinn.verification.diagnostic_guard import (
        DiagnosticArtifactRefused,
        DiagnosticRegistrationRefused,
    )

    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    settings, variant, _orbit_key, _runtime_pair = validate_smoke_settings(doc)
    if settings.get("variant_registry") != PHASE67_REGISTRY_NAME:
        raise Phase67RecordRefused(
            "the Phase 67 reader reads phase67 registrations only; the settings "
            f"name variant_registry {settings.get('variant_registry')!r}"
        )
    registration_file = Path(registration_path)
    if not registration_file.is_absolute():
        registration_file = root / registration_file
    try:
        registration_relative = registration_file.resolve().relative_to(root).as_posix()
    except ValueError:
        registration_relative = registration_file.as_posix()
    directory = Path(run_dir)
    if not directory.is_absolute():
        directory = root / directory
    record_path = directory / RECORD_NAME
    if not record_path.is_file():
        raise Phase67RecordRefused(
            f"the run directory carries no {RECORD_NAME}: {directory}"
        )

    layers = registered_layers(variant.depth)
    identity = {
        "registration": {
            "path": registration_relative,
            "sha256": hashlib.sha256(registration_file.read_bytes()).hexdigest(),
        },
        "variant": {**variant.to_json_dict(), "registry": PHASE67_REGISTRY_NAME},
        "orbit_key": settings["orbit_key"],
        "seed": int(settings["seed"]),
        "runtime": dict(settings["runtime"]),
        "physical_window": dict(settings["physical_window"]),
        "layers": layers,
    }
    mechanical: list[str] = []

    # 1) The registration-bound record audit: identity, cadence, steps,
    #    optimizer policy, window, weights bytes and pinned sources.
    try:
        verify_fit_result(registration_path, record_path, repo_root=root)
    except (
        DiagnosticFitRefused,
        DiagnosticRegistrationRefused,
        DiagnosticArtifactRefused,
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    ):
        mechanical.append(_PROBLEM_FIT_AUDIT)

    # 2) The record's own shape-guarded checks (never a traceback).
    record_raw = record_path.read_bytes()
    try:
        record = json.loads(record_raw.decode("utf-8"))
        if not isinstance(record, dict):
            raise ValueError("not an object")
    except (UnicodeDecodeError, ValueError):
        record = None
        mechanical.append(_PROBLEM_RECORD_UNREADABLE)
    if isinstance(record, dict):
        entries = (record.get("similarity") or {}).get("entries")
        if not isinstance(entries, list) or not entries or any(
            not isinstance(entry, dict)
            or [layer.get("name") for layer in (entry.get("layers") or [])] != layers
            for entry in entries
        ):
            mechanical.append(_PROBLEM_LAYERS)
        network = (record.get("scores") or {}).get("network")
        if not isinstance(network, dict):
            network = {}
            mechanical.append(_PROBLEM_TIER)
        else:
            e_value = network.get("E")
            tier_value = network.get("tier")
            e_number = (
                not isinstance(e_value, bool)
                and isinstance(e_value, (int, float))
                and math.isfinite(float(e_value))
            )
            tier_int = not isinstance(tier_value, bool) and isinstance(tier_value, int)
            if not (e_number and tier_int):
                mechanical.append(_PROBLEM_TIER)
            else:
                try:
                    limit = _tier1_max()
                except Exception:
                    limit = None
                    mechanical.append(_PROBLEM_TIER)
                if limit is not None and (
                    (float(e_value) <= limit and tier_value < 1)
                    or (float(e_value) > limit and tier_value != 0)
                ):
                    mechanical.append(_PROBLEM_TIER)
        opens, access_present = _split_opens(record)
        if not access_present:
            mechanical.append(_PROBLEM_ACCESS)
        elif opens:
            mechanical.append(_PROBLEM_SPLITS)
    else:
        mechanical.append(_PROBLEM_LAYERS)
        mechanical.append(_PROBLEM_TIER)
        mechanical.append(_PROBLEM_ACCESS)

    # 3) The launcher receipt: AC power inside the owner's weekend window.
    receipt = _read_json_object(directory / "power-gate.json")
    receipt_path = directory / "power-gate.json"
    if not receipt_path.is_file():
        mechanical.append(_PROBLEM_RECEIPT_MISSING)
    elif receipt is None:
        mechanical.append(_PROBLEM_RECEIPT_UNREADABLE)
    else:
        if receipt.get("schema") != RECEIPT_SCHEMA:
            mechanical.append(_PROBLEM_RECEIPT_SCHEMA)
        if receipt.get("power_source") != AC_SOURCE:
            mechanical.append(_PROBLEM_RECEIPT_SOURCE)
        if not _receipt_window_ok(receipt.get("window")):
            mechanical.append(_PROBLEM_RECEIPT_WINDOW)

    # 4) The exclusive attempt claim: published, digest-faithful, not preceded
    #    by its own receipt.
    attempt = _read_json_object(directory / "attempt.json")
    attempt_path = directory / "attempt.json"
    if not attempt_path.is_file():
        mechanical.append(_PROBLEM_ATTEMPT_MISSING)
    elif attempt is None:
        mechanical.append(_PROBLEM_ATTEMPT_UNREADABLE)
    else:
        if attempt.get("status") != "published":
            mechanical.append(_PROBLEM_ATTEMPT_STATUS)
        if attempt.get("record_sha256") != hashlib.sha256(record_raw).hexdigest():
            mechanical.append(_PROBLEM_ATTEMPT_DIGEST)

    if receipt is not None and attempt is not None:
        checked = _aware_datetime(receipt.get("checked_utc"))
        started = _aware_datetime(attempt.get("started_utc"))
        if checked is None or started is None:
            mechanical.append(_PROBLEM_TIMESTAMPS)
        elif checked > started:
            mechanical.append(_PROBLEM_RECEIPT_LATE)

    reading = {
        **identity,
        "mechanical_problems": mechanical,
        "setting_problems": [],
    }
    if include_scores:
        if mechanical or reading["setting_problems"]:
            raise Phase67RecordRefused(
                "the Phase 67 reader exposes scores only after a clean audit; "
                f"this reading carries {len(mechanical)} mechanical problems"
            )
        if not isinstance(record, dict):
            raise Phase67RecordRefused(_PROBLEM_RECORD_UNREADABLE)
        reading["scores"] = {
            "network": (record.get("scores") or {}).get("network") or {},
            "comparisons": list(record.get("comparisons") or []),
        }
    return reading


# --------------------------------------------------------------------------
# Plan 67-05 task 67-05-01: the science reading over one run directory.
# --------------------------------------------------------------------------


def _committed_window_metadata(doc):
    """The registration's committed window metadata and baselines, or refusal.

    A Phase 67 science registration commits both blocks beside its settings:
    the retained grid's first/last timestamp, sample count and the physical
    and normalized-tau sha256 digests (the 67-03 evidence convention), and
    the independently recomputed same-window baseline expectations with the
    two-Kepler formula's nonapplicability retained rather than a manufactured
    score. Anything missing or malformed is a typed refusal before any run
    evidence is read.
    """
    metadata = doc.get("window_metadata")
    baselines = doc.get("window_baselines")
    if not isinstance(metadata, Mapping) or not isinstance(baselines, Mapping):
        raise Phase67RecordRefused(
            "the Phase 67 science reading requires the registration's "
            "committed window metadata and same-window baselines"
        )
    for field in ("first_time", "last_time"):
        if _finite_number(metadata.get(field)) is None:
            raise Phase67RecordRefused(
                f"the committed window metadata {field} must be a finite number"
            )
    count = metadata.get("sample_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise Phase67RecordRefused(
            "the committed window metadata sample_count must be a positive integer"
        )
    for field in ("physical_times_sha256", "normalized_tau_sha256"):
        digest = metadata.get(field)
        if not isinstance(digest, str) or len(digest) != 64:
            raise Phase67RecordRefused(
                f"the committed window metadata {field} must be a sha256 digest"
            )
    constant = baselines.get("window_mean_constant")
    if not isinstance(constant, Mapping) or _finite_number(constant.get("E")) is None:
        raise Phase67RecordRefused(
            "the committed baselines carry no finite window-mean-constant E"
        )
    kepler = baselines.get("two_kepler")
    if not isinstance(kepler, Mapping) or not isinstance(
        kepler.get("applicable"), bool
    ):
        raise Phase67RecordRefused(
            "the committed baselines carry no two-Kepler applicability"
        )
    if kepler["applicable"] and _finite_number(kepler.get("E")) is None:
        raise Phase67RecordRefused(
            "the committed two-Kepler baseline names no finite E"
        )
    return metadata, baselines


def _layer_shape_problems(record, layers):
    """Layer rows, cosines, movement, rate and coordinates, per entry."""
    problems = []
    similarity = record.get("similarity")
    entries = similarity.get("entries") if isinstance(similarity, Mapping) else None
    if not isinstance(entries, list) or not entries:
        return [_PROBLEM_LAYERS], None
    orders = list(range(len(layers)))
    grids = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            return [_PROBLEM_LAYERS], []
        rows = entry.get("layers")
        if not isinstance(rows, list) or any(
            not isinstance(row, Mapping) for row in rows
        ):
            return [_PROBLEM_LAYERS], []
        if [row.get("name") for row in rows] != layers or [
            row.get("order") for row in rows
        ] != orders:
            problems.append(_PROBLEM_LAYERS)
        for row in rows:
            cosine = _finite_number(row.get("adjacent_cosine_mean"))
            if cosine is None or not -1.0 <= cosine <= 1.0:
                problems.append(_PROBLEM_COSINE)
        movement = entry.get("output_movement")
        rate = entry.get("output_rate_ratio")
        movement_value = (
            _finite_number(movement.get("value")) if isinstance(movement, Mapping) else None
        )
        rate_value = (
            _finite_number(rate.get("value")) if isinstance(rate, Mapping) else None
        )
        if movement_value is None or movement_value < 0.0 \
                or rate_value is None or rate_value < 0.0:
            problems.append(_PROBLEM_MOVEMENT)
        times_ok = _strictly_increasing(entry.get("times_physical"))
        tau_ok = _strictly_increasing(entry.get("tau_values"))
        if not times_ok or not tau_ok:
            problems.append(_PROBLEM_COORDINATES)
            continue
        grids.append((
            list(entry["times_physical"]),
            list(entry["tau_values"]),
        ))
    # De-duplicate while keeping the deterministic discovery order.
    return sorted(set(problems)), grids


def _grid_problems(grids, metadata):
    """Every entry's actual retained grid against the committed metadata."""
    if not grids:
        return [_PROBLEM_GRID]
    problems = []
    for times, tau in grids:
        if _float64_digest(times) != metadata["physical_times_sha256"] \
                or _float64_digest(tau) != metadata["normalized_tau_sha256"]:
            problems.append(_PROBLEM_GRID)
        if float(times[0]) != float(metadata["first_time"]) \
                or float(times[-1]) != float(metadata["last_time"]) \
                or len(times) != int(metadata["sample_count"]):
            problems.append(_PROBLEM_GRID)
    return sorted(set(problems))


def _frequency_problems(record, variant):
    """Raw frequency evidence, or the registered encoded nonapplicability."""
    entries = (record.get("similarity") or {}).get("entries")
    if not isinstance(entries, list):
        return []
    raw = variant.time_features == "raw_tau_ic13"
    harmonics = {
        "tau_ic13_fourier1": (1,),
        "tau_ic13_fourier12": (1, 2),
    }.get(variant.time_features)
    problems = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        block = entry.get("first_layer_frequency")
        if raw:
            values = (
                _finite_number(block.get("median")),
                _finite_number(block.get("max")),
            ) if isinstance(block, Mapping) else (None, None)
            if any(value is None or value < 0.0 for value in values):
                problems.append(_PROBLEM_RAW_FREQUENCY)
            continue
        if harmonics is None:
            continue
        applicable = entry.get("frequency_applicability")
        reason = entry.get("frequency_reason")
        cycles = entry.get("feature_frequency_cycles")
        emitted = entry.get("feature_harmonics")
        dimension = entry.get("internal_input_dimension")
        expected_cycles = [
            int(k) * float(variant.feature_frequency) for k in harmonics
        ]
        median_max_null = (
            isinstance(block, Mapping)
            and block.get("median") is None
            and block.get("max") is None
        )
        if (
            applicable is not False
            or not isinstance(reason, str)
            or not reason
            or cycles != expected_cycles
            or emitted != list(harmonics)
            or isinstance(dimension, bool)
            or not isinstance(dimension, int)
            or dimension != 14 + 2 * len(harmonics)
            or not median_max_null
        ):
            problems.append(_PROBLEM_ENCODED_FREQUENCY)
    return problems


def _baseline_problems(record, baselines):
    """The recorded same-window comparisons against the committed rows."""
    rows = record.get("comparisons")
    if not isinstance(rows, list):
        return [_PROBLEM_BASELINE]
    by_name = {
        row.get("comparison"): row
        for row in rows
        if isinstance(row, Mapping)
    }
    constant = by_name.get("window_mean_constant")
    constant_score = (
        (constant.get("score") or {}) if isinstance(constant, Mapping) else {}
    )
    committed_constant = baselines["window_mean_constant"]["E"]
    if _finite_number(constant_score.get("E")) is None \
            or float(constant_score["E"]) != float(committed_constant):
        return [_PROBLEM_BASELINE]
    kepler = by_name.get("two_kepler")
    committed_kepler = baselines["two_kepler"]
    if not isinstance(kepler, Mapping) \
            or bool(kepler.get("applicable", False)) is not bool(
                committed_kepler["applicable"]
            ):
        return [_PROBLEM_BASELINE]
    if committed_kepler["applicable"]:
        score = kepler.get("score")
        e_value = (
            _finite_number(score.get("E")) if isinstance(score, Mapping) else None
        )
        if e_value is None or e_value != float(committed_kepler["E"]):
            return [_PROBLEM_BASELINE]
    elif (
        kepler.get("failure") != committed_kepler.get("failure")
        or kepler.get("reason") != committed_kepler.get("reason")
    ):
        return [_PROBLEM_BASELINE]
    return []


def _access_problems(record):
    """TRAIN-only access evidence; absent evidence never stands for zero."""
    access = record.get("access")
    if not isinstance(access, Mapping):
        return [_PROBLEM_ACCESS]
    problems = []
    reads = access.get("reads")
    train = reads.get("train") if isinstance(reads, Mapping) else None
    if (
        isinstance(train, bool) or not isinstance(train, int) or train < 1
    ):
        problems.append(_PROBLEM_TRAIN_ACCESS)
    if access.get("attestation") is None:
        problems.append(_PROBLEM_ACCESS)
    opens, _present = _split_opens(record)
    if opens:
        problems.append(_PROBLEM_SPLITS)
    return problems


def _run_directory_shape_problems(directory, record_name):
    """Symlink problems over the run directory's own evidence files."""
    problems = []
    for name in (record_name, "power-gate.json", "attempt.json"):
        path = directory / name
        if path.is_symlink():
            problems.append(_PROBLEM_SYMLINK)
    return problems


def read_phase67_run_directory(
    registration_path, run_dir, *, repo_root, expected_case=None, include_scores=False
):
    """One Phase 67 run directory read as science evidence.

    The registration is admitted through the committed-registration door and
    must name the Phase 67 registry, declare the registered checkpoint
    schedule and commit its window metadata and same-window baselines;
    anything else is a typed refusal, as is a run directory with no
    ``record.json``. The record, weights, receipt and attempt are then
    validated in the staged order described in the module docstring into
    value-free ``mechanical_problems`` beside the ``setting_problems`` of the
    declared matrix row (``expected_case``: experiment/arm/case/orbit/seed).
    Returns the registered identity, the actual coordinates, the layer trace,
    the checkpoint steps, the observed fit and the final-quarter ``unsettled``
    flag; with ``include_scores`` the frozen endpoint score and both
    comparison rows are added — only after a clean audit, otherwise a typed
    refusal, so a malformed record never yields an accuracy direction.
    """
    from pinn.verification.diagnostic_fit import (
        RECORD_NAME,
        DiagnosticFitRefused,
        require_committed_smoke_registration,
        validate_smoke_settings,
        verify_fit_result,
    )
    from pinn.verification.diagnostic_guard import (
        DiagnosticArtifactRefused,
        DiagnosticRegistrationRefused,
    )
    from pinn.verification.feasibility_scorecard import load_scorecard

    root, doc = require_committed_smoke_registration(
        registration_path, repo_root=repo_root
    )
    settings, variant, _orbit_key, _runtime_pair = validate_smoke_settings(doc)
    if settings.get("variant_registry") != PHASE67_REGISTRY_NAME:
        raise Phase67RecordRefused(
            "the Phase 67 reader reads phase67 registrations only; the settings "
            f"name variant_registry {settings.get('variant_registry')!r}"
        )
    if settings.get("score_cadence") is None:
        raise Phase67RecordRefused(
            "the Phase 67 science reading requires a registration with the "
            "registered score cadence; this registration declares none"
        )
    metadata, baselines = _committed_window_metadata(doc)
    row = (
        _validate_matrix_row(expected_case) if expected_case is not None else None
    )
    registration_file = Path(registration_path)
    if not registration_file.is_absolute():
        registration_file = root / registration_file
    try:
        registration_relative = registration_file.resolve().relative_to(root).as_posix()
    except ValueError:
        registration_relative = registration_file.as_posix()
    directory = Path(run_dir)
    if not directory.is_absolute():
        directory = root / directory
    directory = directory.resolve()
    record_path = directory / RECORD_NAME
    if not record_path.is_file():
        raise Phase67RecordRefused(
            f"the run directory carries no {RECORD_NAME}: {directory}"
        )

    layers = registered_layers(variant.depth)
    identity = {
        "registration": {
            "path": registration_relative,
            "sha256": hashlib.sha256(registration_file.read_bytes()).hexdigest(),
        },
        "variant": {**variant.to_json_dict(), "registry": PHASE67_REGISTRY_NAME},
        "orbit_key": settings["orbit_key"],
        "seed": int(settings["seed"]),
        "runtime": dict(settings["runtime"]),
        "physical_window": dict(settings["physical_window"]),
        "layers": layers,
    }
    if row is not None:
        identity["experiment"] = row["experiment"]
        identity["arm"] = row["arm"]
        identity["case"] = row["case"]
    mechanical: list[str] = []
    setting: list[str] = []
    if row is not None:
        setting.extend(_matrix_row_problems(row, settings, variant))

    # Evidence-link stage: the directory's own files are regular files (never
    # symlinks), and the record's weight reference stays a contained local
    # basename BEFORE the fit verifier opens anything (T-67-13).
    mechanical.extend(_run_directory_shape_problems(directory, RECORD_NAME))
    record_raw = record_path.read_bytes()
    try:
        record = json.loads(record_raw.decode("utf-8"))
        if not isinstance(record, dict):
            raise ValueError("not an object")
    except (UnicodeDecodeError, ValueError):
        record = None

    weights_unsafe = False
    weights_block = (
        record.get("weights") if isinstance(record, dict) else None
    )
    if isinstance(weights_block, Mapping):
        name = weights_block.get("file")
        if not isinstance(name, str) or not name \
                or Path(name).name != name or "/" in name:
            weights_unsafe = True
            mechanical.append(_PROBLEM_UNSAFE_PATH)
        else:
            weights_file = directory / name
            if weights_file.is_symlink():
                weights_unsafe = True
                mechanical.append(_PROBLEM_SYMLINK)
            elif weights_file.resolve().parent != directory:
                weights_unsafe = True
                mechanical.append(_PROBLEM_UNSAFE_PATH)
    if weights_unsafe:
        # Nothing outside the run directory is opened on an unsafe
        # reference: the fit verifier is skipped rather than aimed through
        # the record's own path (T-67-13).
        mechanical.append(_PROBLEM_FIT_AUDIT)

    # 1) The registration-bound record audit: identity, cadence, schedule,
    #    steps, optimizer policy, window, weights bytes and pinned sources.
    if not weights_unsafe:
        try:
            verify_fit_result(registration_path, record_path, repo_root=root)
        except (
            DiagnosticFitRefused,
            DiagnosticRegistrationRefused,
            DiagnosticArtifactRefused,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ):
            mechanical.append(_PROBLEM_FIT_AUDIT)

    # 2) The staged shape, grid, frequency, baseline, score and access checks.
    grids: list = []
    layer_trace: list = []
    checkpoint_steps: list = []
    observed_fit = False
    unsettled = None
    if not isinstance(record, dict):
        mechanical.extend([
            _PROBLEM_RECORD_UNREADABLE, _PROBLEM_LAYERS, _PROBLEM_TIER,
            _PROBLEM_ACCESS, _PROBLEM_SCHEDULE, _PROBLEM_IMPROVEMENT,
            _PROBLEM_GRID, _PROBLEM_BASELINE,
        ])
    else:
        shape_problems, grids = _layer_shape_problems(record, layers)
        mechanical.extend(shape_problems)
        mechanical.extend(_grid_problems(grids, metadata))
        mechanical.extend(_frequency_problems(record, variant))
        mechanical.extend(_baseline_problems(record, baselines))
        mechanical.extend(_access_problems(record))
        similarity = record.get("similarity")
        entries = (
            similarity.get("entries") if isinstance(similarity, Mapping) else None
        )
        if isinstance(entries, list):
            layer_trace = [
                {
                    "step": entry.get("step"),
                    "layers": [dict(row) for row in entry.get("layers") or []],
                }
                for entry in entries
                if isinstance(entry, Mapping)
            ]
        # The registered schedule, re-derived from the module functions.
        steps_setting = int(settings["optimizer_steps"])
        from pinn.verification.diagnostic_phase67 import (
            phase67_cadence,
            phase67_score_cadence,
        )

        cadence_ok = (
            isinstance(similarity, Mapping)
            and similarity.get("cadence") == phase67_cadence(steps_setting)
        )
        checkpoints = record.get("score_checkpoints")
        if isinstance(checkpoints, list) and all(
            isinstance(entry, Mapping) for entry in checkpoints
        ):
            checkpoint_steps = [entry.get("step") for entry in checkpoints]
        schedule_ok = (
            checkpoint_steps == phase67_score_cadence(steps_setting)
        )
        if not cadence_ok or not schedule_ok:
            mechanical.append(_PROBLEM_SCHEDULE)
        # The frozen E/tier consistency of the endpoint and every checkpoint.
        try:
            card = load_scorecard()
        except Exception:
            card = None
        network = (record.get("scores") or {}).get("network")
        if card is None or not _tier_consistent(network, card):
            mechanical.append(_PROBLEM_TIER)
        else:
            observed_fit = _finite_number(network.get("E")) is not None
        if isinstance(checkpoints, list):
            for checkpoint in checkpoints:
                if not (
                    isinstance(checkpoint, Mapping)
                    and card is not None
                    and _tier_consistent(checkpoint.get("score"), card)
                ):
                    mechanical.append(_PROBLEM_TIER)
        # The final-quarter improvement rule over the three checkpoints.
        unsettled = _improvement_unsettled(checkpoints)
        if unsettled is None:
            mechanical.append(_PROBLEM_IMPROVEMENT)

    # 3) The launcher receipt: AC power inside the owner's weekend window,
    #    audited on its own local time and first line.
    receipt = _read_json_object(directory / "power-gate.json")
    receipt_path = directory / "power-gate.json"
    if not receipt_path.is_file():
        mechanical.append(_PROBLEM_RECEIPT_MISSING)
    elif receipt is None:
        mechanical.append(_PROBLEM_RECEIPT_UNREADABLE)
    else:
        if receipt.get("schema") != RECEIPT_SCHEMA:
            mechanical.append(_PROBLEM_RECEIPT_SCHEMA)
        if receipt.get("power_source") != AC_SOURCE:
            mechanical.append(_PROBLEM_RECEIPT_SOURCE)
        if not _receipt_window_ok(receipt.get("window")):
            mechanical.append(_PROBLEM_RECEIPT_WINDOW)
        first_line = receipt.get("pmset_first_line")
        if not isinstance(first_line, str) \
                or power_source(first_line) != AC_SOURCE:
            mechanical.append(_PROBLEM_AC_FIRST_LINE)

    # 4) The exclusive attempt claim: published, digest-faithful, capped and
    #    completed exactly as the record states.
    attempt = _read_json_object(directory / "attempt.json")
    attempt_path = directory / "attempt.json"
    if not attempt_path.is_file():
        mechanical.append(_PROBLEM_ATTEMPT_MISSING)
    elif attempt is None:
        mechanical.append(_PROBLEM_ATTEMPT_UNREADABLE)
    else:
        if attempt.get("status") != "published":
            mechanical.append(_PROBLEM_ATTEMPT_STATUS)
        if attempt.get("record_sha256") != hashlib.sha256(record_raw).hexdigest():
            mechanical.append(_PROBLEM_ATTEMPT_DIGEST)
        cap = _finite_number(settings.get("whole_run_cap_seconds"))
        attempt_cap = _finite_number(attempt.get("whole_run_cap_seconds"))
        if cap is None or attempt_cap is None or attempt_cap != cap:
            mechanical.append(_PROBLEM_ATTEMPT_CAP)
        completed = attempt.get("completed_steps")
        recorded_completed = (
            (record.get("steps") or {}).get("completed")
            if isinstance(record, dict) else None
        )
        if isinstance(completed, bool) or not isinstance(completed, int) \
                or completed != recorded_completed:
            mechanical.append(_PROBLEM_ATTEMPT_STEPS)

    # 5) The aware instants: checked before start before end, the
    #    launch-to-end wall inside the registered cap, and the cap fitting
    #    the Sunday 22:00 closing instant derived from the receipt itself.
    if receipt is not None and attempt is not None:
        checked = _aware_datetime(receipt.get("checked_utc"))
        started = _aware_datetime(attempt.get("started_utc"))
        ended = _aware_datetime(attempt.get("ended_utc"))
        cap = _finite_number(settings.get("whole_run_cap_seconds"))
        if checked is None or started is None or ended is None or cap is None:
            mechanical.append(_PROBLEM_TIMESTAMPS)
        else:
            if checked > started:
                mechanical.append(_PROBLEM_RECEIPT_LATE)
            if started > ended:
                mechanical.append(_PROBLEM_ATTEMPT_ORDER)
            if (ended - checked).total_seconds() > cap:
                mechanical.append(_PROBLEM_LAUNCH_WALL)
            window = receipt.get("window")
            moment = (
                _aware_datetime(window.get("local_time"))
                if isinstance(window, Mapping) else None
            )
            if moment is not None:
                try:
                    local = moment.astimezone(ZoneInfo(WINDOW_TIMEZONE))
                except (ValueError, OSError):
                    local = None
                if local is not None:
                    closing = _sunday_closing(local)
                    if closing is not None and local + timedelta(
                        seconds=cap
                    ) > closing:
                        mechanical.append(_PROBLEM_SUNDAY_CAP)

    # De-duplicate the mechanical list, keeping the deterministic order.
    mechanical = list(dict.fromkeys(mechanical))
    reading = {
        "identity": identity,
        "mechanical_problems": mechanical,
        "setting_problems": setting,
        "actual_coordinates": (
            {"physical": grids[-1][0], "raw_tau": grids[-1][1]}
            if grids else {}
        ),
        "layer_trace": layer_trace,
        "checkpoint_steps": checkpoint_steps,
        "observed_fit": observed_fit,
        "unsettled": unsettled,
    }
    if include_scores:
        if mechanical or setting:
            raise Phase67RecordRefused(
                "the Phase 67 reader exposes scores only after a clean audit; "
                f"this reading carries {len(mechanical)} mechanical and "
                f"{len(setting)} setting problems"
            )
        if not isinstance(record, dict):
            raise Phase67RecordRefused(_PROBLEM_RECORD_UNREADABLE)
        reading["scores"] = {
            "network": (record.get("scores") or {}).get("network") or {},
            "comparisons": list(record.get("comparisons") or []),
        }
    return reading
