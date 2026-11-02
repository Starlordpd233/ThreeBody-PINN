"""Phase 67 (plans 67-08..67-16): the execution and page command adapter.

This module owns the narrow orchestration the four experiment plans invoke
without scientific improvisation (plan 67-06, D-07/D-10/D-12/D-13):

* :func:`phase67_design` — the frozen scientific design block one experiment
  commits before any real operation: every declared arm and case, the
  prospective hypothesis prediction with the flat, opposite, unsettled and
  mechanical alternatives recorded equally, the registered schedule numbers,
  the cost-only budget rule, the scope branch table and the confound record.
* :func:`phase67_run_matrix` — the exact case-major Cartesian product of the
  declared cases and arms, with orbit-aware variant names, the committed
  metadata digest and the exact registration/output paths.
* :func:`admit_phase67_metadata_registration` /
  :func:`capture_phase67_metadata` — the committed metadata registration
  door and the gated metadata-only capture (no optimizer, no model).
* :func:`launch_phase67_row` — one registered row through the existing
  AC/weekend power launcher, never a batch or retry loop.
* :func:`audit_phase` — the read-only evidence, chronology, scope and hash
  audit of all four experiments.

Every command is a small function here; the CLI entry point is
``python -B -m pinn.verification.diagnostic_phase67`` (the pure module's
``main``, which imports this adapter lazily so the pure module never gains a
harness import). The execution-heavy modules (the fit, the power gate, the
data seam, the readers) are imported inside the functions that need them.

All outputs live inside the phase directory; unknown options, experiments,
kinds, cases and arms refuse with exit 2 and no downstream file. The
evidence ``harness-freeze.json`` is 67-07's committed artifact; synthetic
fixtures supply their own temporary freeze manifest, and until the
production freeze exists every phase67 command refuses real work.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.verification.diagnostic_phase67 import (
    CONFIRMATION_LABELS,
    GAP_59_08_NOTE,
    PHASE67_CASES,
    SIMILARITY_NOTE,
    phase67_budget,
    phase67_cadence,
    phase67_confirmation,
    phase67_contrast,
    phase67_control_arm,
    phase67_loss_trace_stride,
    phase67_score_cadence,
)
from pinn.verification import diagnostic_phase67 as _core67


def _rule():
    """The registered budget rule, read through its owning module.

    Every phase67 command derives its schedule numbers from the one
    registered rule object; reading it through the source module (never a
    bound copy) keeps one source of truth.
    """
    return _core67.PHASE67_BUDGET_RULE
from pinn.verification.diagnostic_phase67_catalog import (
    CENSUS_N_IN_1632,
    CENSUS_N_IN_851,
    CENSUS_PANELS_RELATIVE_PATH,
    PHASE67_REGISTRY_NAME,
    register_exp05_window_variants,
)
from pinn.verification.diagnostic_variants import DiagnosticVariant

__all__ = [
    "ARM_ORDER",
    "BUDGET_SCHEMA",
    "CASES",
    "DEFAULT_RUNTIME",
    "DESIGN_SCHEMA",
    "EXPERIMENTS",
    "EXPERIMENT_CHAIN",
    "HARNESS_FREEZE_SCHEMA",
    "METADATA_ATTEMPT_SCHEMA",
    "METADATA_REGISTRATION_SCHEMA",
    "METADATA_SCHEMA",
    "Phase67CommandRefused",
    "REVIEW_SCHEMA",
    "RUN_MATRIX_SCHEMA",
    "admit_phase67_metadata_registration",
    "audit_phase67",
    "budget_page",
    "capture_phase67_metadata",
    "check_budget",
    "check_design",
    "check_matrix",
    "check_metadata",
    "check_review",
    "check_row",
    "launch_phase67_row",
    "phase67_cost_rows",
    "phase67_design",
    "phase67_prior_experiment_allowed",
    "phase67_run_matrix",
    "phase67_scope_disposition",
    "prediction_page",
    "prepare_design",
    "register_timing",
    "result_page",
    "timing_prediction_page",
    "verify_harness_freeze",
    "write_budget",
    "write_review",
]

# --------------------------------------------------------------------------
# The registered experiment surface (the plan's exact bindings).
# --------------------------------------------------------------------------

DESIGN_SCHEMA = "phase67-design/v1"
METADATA_REGISTRATION_SCHEMA = "phase67-metadata-registration/v1"
METADATA_SCHEMA = "phase67-metadata/v1"
METADATA_ATTEMPT_SCHEMA = "phase67-metadata-attempt/v1"
RUN_MATRIX_SCHEMA = "phase67-run-matrix/v1"
BUDGET_SCHEMA = "phase67-budget/v1"
REVIEW_SCHEMA = "phase67-review/v1"
RULING_NAME_TEMPLATE = "67-EXPxx-RULING.md"
HARNESS_FREEZE_SCHEMA = "phase67-harness-freeze/v1"

#: The four experiments and the review chain order (D-10: each result is
#: reviewed before the work its result could invalidate continues).
EXPERIMENTS = ("exp02", "exp03", "exp04", "exp05")
EXPERIMENT_CHAIN = ("exp02", "exp03", "exp04", "exp05")

#: The three D-09 confirmation cases every matrix repeats on.
CASES = (
    ("main-1632-s42", "hierarchical/gold/1632", 42),
    ("repeat-851-s42", "hierarchical/gold/851", 42),
    ("repeat-1632-s41", "hierarchical/gold/1632", 41),
)

#: The exact arm order per experiment (the plan's declared ladders; exp05's
#: arms are the D-06 lap counts whose variants materialize after metadata).
ARM_ORDER = {
    "exp02": ("d2", "d4", "d6", "d8", "d12"),
    "exp03": ("lr1e-3", "lr3e-4", "lr1e-4", "lr3e-5", "lr1e-5"),
    "exp04": (
        "locked-raw", "locked-f1", "locked-f12",
        "exp01-raw", "exp01-f1", "exp01-f12",
    ),
    "exp05": ("lap1", "lap2", "lap5", "lap10"),
}

#: The registered run runtime (MPS float32, D-07); synthetic fixtures patch
#: this module attribute to their CPU float64 seam.
DEFAULT_RUNTIME = {"dtype": "float32", "device": "mps"}

#: The default phase directory (relative to the repository root).
PHASE_DIR_RELATIVE = ".planning/phases/67-design-settings-ladders"

#: The committed Phase 65 smoke registration whose provenance blocks (the
#: logger-parity receipt, the probe context, the frozen scorer artifacts and
#: the pinned protocol) the phase67 row registrations copy verbatim.
PROVENANCE_REGISTRATION_REL = (
    ".planning/phases/65-probe-on-the-record-fit-harness/"
    "evidence/fit/smoke-registration.json"
)

#: The harness files every phase67 row registration pins at their current
#: committed bytes ("Require current harness-freeze pins in all new
#: registrations"; the freeze manifest itself is pinned separately).
PHASE67_DEPENDENCIES = (
    "pinn/verification/diagnostic_fit.py",
    "pinn/verification/diagnostic_guard.py",
    "pinn/verification/diagnostic_data.py",
    "pinn/verification/diagnostic_variants.py",
    "pinn/verification/diagnostic_similarity.py",
    "pinn/verification/diagnostic_power.py",
    "pinn/verification/diagnostic_phase66.py",
    "pinn/verification/diagnostic_time_features.py",
    "pinn/verification/diagnostic_phase67.py",
    "pinn/verification/diagnostic_phase67_catalog.py",
    "pinn/verification/diagnostic_phase67_records.py",
    "pinn/verification/diagnostic_phase67_windows.py",
    "pinn/verification/diagnostic_phase67_execution.py",
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class Phase67CommandRefused(RuntimeError):
    """A phase67 command precondition does not hold; nothing downstream."""


def _require(condition, message):
    if not condition:
        raise Phase67CommandRefused(message)


def _finite(value, what):
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(float(value)):
        raise Phase67CommandRefused(f"{what} must be a finite number; got {value!r}")
    return float(value)


# --------------------------------------------------------------------------
# Repository, phase-directory and committed-provenance primitives.
# --------------------------------------------------------------------------


def _repo_root(repo_root=None):
    if repo_root is not None:
        return Path(repo_root).resolve()
    probe = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
    )
    if probe.returncode == 0 and probe.stdout.strip():
        return Path(probe.stdout.strip()).resolve()
    raise Phase67CommandRefused(
        "the phase67 commands run inside the experiment repository; no "
        "repository root was found or given"
    )


def _phase_directory(phase_dir, root):
    if phase_dir is None:
        path = root / PHASE_DIR_RELATIVE
    else:
        path = Path(phase_dir)
        if not path.is_absolute():
            path = root / path
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise Phase67CommandRefused(
            "all phase67 outputs live inside the phase directory; "
            f"{path} resolves outside the repository"
        ) from exc
    return path


def _relative(root, path):
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True, check=False
    )


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _tracked_and_clean(root, relative_path):
    if _git(root, "ls-files", "--error-unmatch", "--", relative_path).returncode != 0:
        return False
    status = _git(root, "status", "--porcelain", "--", relative_path)
    return status.returncode == 0 and status.stdout.strip() == ""


def _introducing_commit(root, relative_path):
    probe = _git(
        root, "log", "-n1", "--format=%H", "--diff-filter=A", "--", relative_path
    )
    if probe.returncode != 0 or not probe.stdout.strip():
        return None
    return probe.stdout.strip().splitlines()[0]


def _require_committed(root, relative_path, what):
    _require(
        _tracked_and_clean(root, relative_path),
        f"the {what} is untracked or dirty: {relative_path}",
    )


def _entry(path, digest):
    return {"path": path, "sha256": digest}


def verify_harness_freeze(root, phase_dir):
    """The committed harness freeze, verified current (67-07's artifact).

    The freeze manifest must be committed clean, carry the phase67 schema and
    a non-empty pinned-file list, and every pinned file must be tracked,
    clean and digest-exact at its current bytes. Until 67-07 commits the
    production freeze this refuses, so no phase67 registration or launch can
    precede the compatibility gate.
    """
    freeze_rel = _relative(root, phase_dir / "evidence/harness-freeze.json")
    path = root / freeze_rel
    _require(path.is_file(), f"the harness freeze manifest is missing: {freeze_rel}")
    _require_committed(root, freeze_rel, "harness freeze manifest")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(
            f"the harness freeze manifest is not readable JSON: {exc}"
        ) from exc
    _require(
        isinstance(doc, Mapping) and doc.get("schema") == HARNESS_FREEZE_SCHEMA,
        f"the harness freeze manifest must be schema {HARNESS_FREEZE_SCHEMA!r}",
    )
    files = doc.get("files")
    _require(
        isinstance(files, list) and files,
        "the harness freeze manifest names no pinned files",
    )
    for index, pinned in enumerate(files):
        _require(
            isinstance(pinned, Mapping) and isinstance(pinned.get("path"), str)
            and isinstance(pinned.get("sha256"), str),
            f"the freeze entry {index} must name a path and a sha256",
        )
        _require_committed(root, pinned["path"], f"frozen harness file")
        on_disk = _sha256_file(root / pinned["path"])
        _require(
            on_disk == pinned["sha256"],
            f"the frozen harness file changed since the freeze: {pinned['path']} "
            f"({on_disk} != {pinned['sha256']})",
        )
    return doc


def _fenced_block(page_text, info_string):
    """The single fenced block named by ``info_string`` (66-02's contract)."""
    pattern = re.compile(
        r"^```(?P<info>[^\n`]*)\n(?P<body>.*?)^```[ \t]*$",
        re.MULTILINE | re.DOTALL,
    )
    matches = [
        fence.group("body")
        for fence in pattern.finditer(page_text)
        if fence.group("info").split()[-1:] == [info_string]
    ]
    if len(matches) != 1:
        raise Phase67CommandRefused(
            f"the page must carry exactly one fenced {info_string!r} block; "
            f"found {len(matches)}"
        )
    return matches[0]


def _exclusive_json_write(path, payload):
    """The canonical exclusive evidence write (one file, created once)."""
    from pinn.verification.learnability_arms import (
        FirstResultExists,
        write_record_exclusive,
    )

    if Path(path).exists():
        raise Phase67CommandRefused(
            f"the artifact already exists and is never replaced: {Path(path).name}"
        )
    try:
        write_record_exclusive(Path(path), payload)
    except FirstResultExists as exc:
        raise Phase67CommandRefused(str(exc)) from exc


def _exclusive_text_write(path, text):
    """One exclusive page write (the same create-once contract, raw text)."""
    import os

    destination = Path(path)
    if destination.exists():
        raise Phase67CommandRefused(
            f"the page already exists and is never replaced: {destination.name}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
        )
    except FileExistsError as exc:
        raise Phase67CommandRefused(
            f"the page already exists and is never replaced: {destination.name}"
        ) from exc
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(text.encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())


def _canonical_json(payload):
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


# --------------------------------------------------------------------------
# The frozen design block (D-10: committed before any real operation).
# --------------------------------------------------------------------------

#: The depth-associated parameter changes (67-02's pinned deterministic
#: counts) the report states beside the depth ladder (D-03).
_DEPTH_PARAMETER_COUNTS = {
    "d2": 137737, "d4": 269321, "d6": 400905, "d8": 532489, "d12": 795657,
}

_HYPOTHESES = {
    "exp02": {
        "name": "depth",
        "statement": (
            "the locked 12-layer depth contributes to the time-constant "
            "failure; a shallower network at the same locked width, input, "
            "frequencies, rate and window fits the orbit better"
        ),
        "prediction": (
            "shallower depth improves the one-orbit fit: each shallower arm's "
            "E is below the d12 control's on all three registered cases "
            "under the registered effect rule"
        ),
    },
    "exp03": {
        "name": "rate",
        "statement": (
            "the locked 1e-4 constant Adam rate is mis-set for this task; a "
            "different constant rate fits the same locked network better"
        ),
        "prediction": (
            "learning-rate sensitivity: the fit's E changes across the rate "
            "ladder against the lr1e-4 control on the registered cases"
        ),
    },
    "exp04": {
        "name": "input",
        "statement": (
            "the raw [tau, IC13] input under-resolves the orbit's inner "
            "motion; an input carrying the census-frequency harmonics fits "
            "better without changing the backbone"
        ),
        "prediction": (
            "the encoded harmonic input improves the fit: each encoded arm's "
            "E is below its own backbone's raw control's on all three "
            "registered cases"
        ),
    },
    "exp05": {
        "name": "window",
        "statement": (
            "the full [0, 10] window is harder than the orbit's early "
            "motion; a shorter exact signed-lap prefix fits better at the "
            "locked settings"
        ),
        "prediction": (
            "a shorter window improves the fit: each shorter prefix arm's E "
            "is below the lap10 control's on all three registered cases"
        ),
    },
}


def phase67_scope_disposition(confirmation):
    """The registered SCOPE-49 disposition of one confirmation label.

    Within-scope registered branches (confirmed-improvement, ambiguous,
    unsettled) record a technical ruling and continue under D-01; a refuted
    lead (confirmed-worsening) or an out-of-rule result
    (inconclusive-mechanical) raises a concrete owner proposal under
    SCOPE-49/SCOPE-47 and blocks the dependent experiment's launches.
    """
    if confirmation == "confirmed-improvement":
        return {
            "scope49_disposition": "none",
            "dependent_launch_allowed": True,
            "reason": "the hypothesis-supported branch is a registered "
                      "technical ruling; continue under D-01",
        }
    if confirmation in ("ambiguous", "unsettled"):
        return {
            "scope49_disposition": "none",
            "dependent_launch_allowed": True,
            "reason": f"the {confirmation} branch is registered and equally "
                      "recorded; no continuation runs (the no-continuation "
                      "policy) and no scope change is proposed",
        }
    if confirmation == "confirmed-worsening":
        return {
            "scope49_disposition": "proposal-pending",
            "dependent_launch_allowed": False,
            "reason": "a refuted lead: the registered hypothesis is "
                      "contradicted on all three cases, so a concrete owner "
                      "proposal under SCOPE-49 is recorded before dependent "
                      "work continues",
        }
    if confirmation == "inconclusive-mechanical":
        return {
            "scope49_disposition": "proposal-pending",
            "dependent_launch_allowed": False,
            "reason": "an out-of-rule result routes to the owner under "
                      "SCOPE-47; dependent work waits for the ruling",
        }
    raise Phase67CommandRefused(
        f"unknown confirmation label {confirmation!r}; the registered labels "
        f"are {list(CONFIRMATION_LABELS)}"
    )


def _variant_table(experiment):
    """The design's per-arm declaration table (orbit-aware where needed)."""
    from pinn.verification.diagnostic_phase67_catalog import phase67_arm_variant

    arms = ARM_ORDER[experiment]
    if experiment == "exp05":
        return [
            {
                "arm": arm,
                "selection": "first_lap_prefixes",
                "lap_count": int(arm.removeprefix("lap")),
                "window_source": "the committed metadata capture's exact "
                                 "first-crossing endpoint",
            }
            for arm in arms
        ]
    orbits = sorted({orbit for _case, orbit, _seed in CASES})
    return [
        {
            "arm": arm,
            "declarations": {
                orbit: phase67_arm_variant(experiment, arm, orbit).to_json_dict()
                for orbit in orbits
            },
        }
        for arm in arms
    ]


def _prediction_table(experiment):
    """Every arm's hypothesis prediction and its alternatives, equally."""
    arms = ARM_ORDER[experiment]
    control = arms[-1]
    phrase = {
        "exp02": "shallower depth",
        "exp03": "learning-rate sensitivity",
        "exp04": "encoded harmonic",
        "exp05": "shorter window",
    }[experiment]
    table = {}
    for arm in arms:
        if arm == control:
            table[arm] = {
                "hypothesis": (
                    f"the control arm {control!r} defines the contrast "
                    "reference; the hypothesis predicts "
                    f"{phrase} against it"
                ),
                "flat": "no effect against the control inside the registered rule",
                "opposite": "the control fits at least as well as every arm",
                "unsettled": "the endpoint is still improving when its budget ends",
                "mechanical": "the run's evidence is mechanically unusable",
            }
            continue
        table[arm] = {
            "hypothesis": (
                f"under the hypothesis, {phrase} improves the fit: this arm's "
                "E is below the control's on all three registered cases "
                "under the registered effect rule"
            ),
            "flat": (
                "no effect against the control inside the registered rule; "
                "the hypothesis is not supported on this arm"
            ),
            "opposite": (
                "this arm fits worse than the control; the hypothesis is "
                "contradicted on this arm"
            ),
            "unsettled": (
                "the endpoint is still improving when its budget ends; the "
                "no-continuation policy records it and extends nothing"
            ),
            "mechanical": (
                "this arm's evidence is mechanically unusable; it reads "
                "nothing about the hypothesis"
            ),
        }
    return table


def phase67_design(experiment):
    """The frozen design block of one experiment (JSON-normal, D-10).

    Everything a prediction page freezes before any real operation: the
    hypothesis with its prospective prediction, every arm's alternative
    branches recorded equally, the exact arm/case tables with orbit-aware
    variants, the registered schedule and budget numbers, the reading and
    scope rules, the no-continuation policy, the positive-control note and
    the confound record.
    """
    _require(experiment in ARM_ORDER,
             f"unknown Phase 67 experiment {experiment!r}; known: "
             f"{list(ARM_ORDER)}")
    rule = dict(_rule())
    timing_steps = int(rule["timing_steps"])
    timing = {
        "optimizer_steps": timing_steps,
        "warmup_steps": int(rule["timing_warmup"]),
        "measured_steps": int(rule["timing_measured"]),
        "similarity_cadence": phase67_cadence(timing_steps),
        "score_cadence": phase67_score_cadence(timing_steps),
        "loss_trace_stride": phase67_loss_trace_stride(timing_steps),
        "cap_seconds": float(rule["timing_cap_seconds"]),
    }
    arms = ARM_ORDER[experiment]
    design = {
        "schema": DESIGN_SCHEMA,
        "experiment": experiment,
        "title": f"EXP-{experiment[-2:].upper()} "
                 + {
                     "exp02": "depth ladder",
                     "exp03": "learning-rate ladder",
                     "exp04": "time-input designs",
                     "exp05": "signed-lap window ladder",
                 }[experiment],
        "hypothesis": dict(_HYPOTHESES[experiment]),
        "alternative_branches": ["flat", "opposite", "unsettled", "mechanical"],
        "prediction_table": _prediction_table(experiment),
        "variants": _variant_table(experiment),
        "cases": [
            {"case": case, "orbit_key": orbit, "seed": seed}
            for case, orbit, seed in CASES
        ],
        "controls": {
            arm: phase67_control_arm(experiment, arm) for arm in arms
        },
        "control_arm": arms[-1],
        "schedule": {
            "timing": timing,
            "science": {
                "cap_seconds": float(rule["cap_seconds"]),
                "optimizer_steps": "the phase67_budget common N, frozen at "
                                   "budget time before any science run",
                "formula": "phase67_cadence/phase67_score_cadence/"
                           "phase67_loss_trace_stride at the budget's N",
            },
        },
        "budget_rule": rule,
        "reading_rule": {
            "improvement": "(E_at_3N/4 - E_at_N)/E_at_3N/4 strictly greater "
                           "than five percent leaves the endpoint unsettled",
            "effect": "a case qualifies through a matching tier change or a "
                      "relative E effect of at least twenty percent",
            "confirmation": "all three registered cases qualifying in one "
                            "direction with settled, clean endpoints",
            "confirmation_labels": list(CONFIRMATION_LABELS),
            "descriptive": {
                "adjacent_time_similarity": SIMILARITY_NOTE,
                "gap_59_08": GAP_59_08_NOTE,
                "loss": "context only",
            },
        },
        "scope_branches": {
            label: phase67_scope_disposition(label)
            for label in CONFIRMATION_LABELS
        },
        "no_continuation": (
            "no branch extends, retries or re-sizes any run after its score "
            "is read; an unsettled endpoint is recorded as unsettled"
        ),
        "positive_control_note": (
            "Phase 66 (EXP-01) remains a multi-setting positive control "
            "(D-02): its confirmed Tier-1 fit refutes only 'too small' and "
            "identifies no single enabling setting"
        ),
        "metadata_algorithm": {
            "reader": "pinn.verification.diagnostic_data.Stage0TrainingReader",
            "normalizer": "the retained Phase 59 recorded normalizer; never refit",
            "baselines": "same_window_expectations (67-03) per window: the "
                         "window-mean constant and the two-Kepler comparison, "
                         "independently cross-checked",
            "frequency": f"N_in from the committed Phase 59 panels row; "
                         f"f = N_in/{float(T_CHARACTERISTIC_TIME):g} cycles "
                         "per physical time unit on both backbones",
            "harmonics": {"f1": [1], "f12": [1, 2]},
            "harmonic_phase_increment": "max adjacent 2*pi*k*f*dt per "
                                        "harmonic k; strictly below pi or "
                                        "EXP-04 timing refuses without retuning",
            "byte_bound": int(rule["size_fraction"] * int(rule["size_limit_bytes"])),
            "cap_seconds": float(rule["timing_cap_seconds"]),
        },
        "confounds": _confounds(experiment),
    }
    if experiment == "exp05":
        design["window_selection"] = {
            "algorithm": "first_lap_prefixes",
            "lap_counts": [int(arm.removeprefix("lap")) for arm in arms],
            "note": "the exact first-crossing gold sample is the endpoint; no "
                    "interpolation and no tau rescaling (D-06)",
        }
    return design


def _confounds(experiment):
    """The confound record each experiment's report states beside its arms."""
    if experiment == "exp02":
        return {
            "depth_parameter_counts": dict(_DEPTH_PARAMETER_COUNTS),
            "note": "the size change that accompanies depth is recorded, not "
                    "controlled away (D-03)",
        }
    if experiment == "exp03":
        return {
            "equal_updates": "every arm runs the same common update count N "
                             "from the shared cost-only budget (D-08)",
        }
    if experiment == "exp04":
        return {
            "encoded": {
                "fan_in": "the first layer's fan-in bound is 1/internal_dim "
                          "(16 for f1, 18 for f12) on both backbones",
                "frequency": "f = N_in/10 from the committed census row, with "
                             "harmonics 1 or 1 and 2 on both backbones",
                "input_design_not_omega": "the encoded arms change the input "
                                          "design, not first_omega_0 (D-05)",
            },
        }
    return {
        "window_only": "the window changes and nothing else: locked depth, "
                       "width, frequencies, rate and global tau normalization",
    }


# --------------------------------------------------------------------------
# The page builders (deterministic text; the design block rides verbatim).
# --------------------------------------------------------------------------


def timing_prediction_page(design):
    """The timing prediction page: the frozen design before any real run."""
    block = json.dumps(design, indent=2, sort_keys=True)
    lines = [
        f"# {design['title']} — Timing Prediction",
        "",
        "The frozen scientific design, committed before any real timing or",
        "experiment run for this experiment (D-10).",
        "No rule is re-set after a result is seen.",
        "",
        "## 1. The frozen design",
        "",
        "```json phase67-design",
        block,
        "```",
        "",
        "## 2. Predictions and their alternatives",
        "",
        "Every arm's hypothesis prediction and the flat, opposite, unsettled",
        "and mechanical alternatives are recorded equally in the design block",
        "above; the review reads the observed branch against this table.",
        "",
    ]
    for arm, branches in design["prediction_table"].items():
        lines.append(f"- `{arm}` — {branches['hypothesis']}")
    lines += [
        "",
        "## 3. The timing run",
        "",
        f"The registered timing run is {design['schedule']['timing']['optimizer_steps']}",
        f"steps ({design['schedule']['timing']['warmup_steps']} warmup,",
        f"{design['schedule']['timing']['measured_steps']} measured) at the five",
        "normalized similarity events and three frozen-score checkpoints of",
        f"the registered schedule, under the",
        f"{design['schedule']['timing']['cap_seconds']:g}-second whole-launch cap.",
        "One row launches at a time; no retry, no batch loop.",
        "",
        "## 4. The budget",
        "",
        "The cost-only common-update budget (67-04) consumes only the timing",
        "rows' measured cost fields and freezes the science update count",
        "before any science registration exists.",
        "",
        "## 5. Harness provenance",
        "",
        "The committed harness freeze manifest pins every harness file at its",
        "current bytes; every registration this page admits pins the freeze.",
        "",
    ]
    return "\n".join(lines)


def budget_page(design, budget):
    """The budget page: the measured cost summary, never a score."""
    lines = [
        f"# {design['title']} — Budget",
        "",
        "The cost-only common-update budget derived from every committed",
        "timing row of this experiment (67-04's phase67_budget). No score,",
        "loss, tier or cosine value is read or appears here.",
        "",
        "```json phase67-budget",
        json.dumps(budget, indent=2, sort_keys=True),
        "```",
        "",
        f"- common optimizer steps: {budget['common_optimizer_steps']}",
        f"- warmup steps: {budget['warmup_steps']}",
        f"- whole-run cap: {budget['whole_run_cap_seconds']:g} seconds",
        "",
        "The science registrations are frozen from this budget before any",
        "science run; the timing prediction page is unchanged by this page.",
        "",
    ]
    return "\n".join(lines)


def prediction_page(design, budget):
    """The immutable science prediction page, frozen before science."""
    lines = [
        f"# {design['title']} — Prediction",
        "",
        "The complete pre-registered prediction: the frozen design, the",
        "measured budget and the exact science registrations. This page is",
        "written once by the budget step and frozen before science; the",
        "review reads every result against it.",
        "",
        "```json phase67-design",
        json.dumps(design, indent=2, sort_keys=True),
        "```",
        "",
        "```json phase67-budget",
        json.dumps(budget, indent=2, sort_keys=True),
        "```",
        "",
        f"The science runs are frozen at {budget['common_optimizer_steps']}",
        f"common optimizer steps ({budget['warmup_steps']} warmup) under the",
        f"{budget['whole_run_cap_seconds']:g}-second cap: the exact",
        "case-major science matrix beside this page carries every registered",
        "row. No rule is re-set after a result is seen.",
        "",
    ]
    return "\n".join(lines)


def result_page(experiment, review):
    """The result page: every value, contrast and the scope disposition."""
    lines = [
        f"# Phase 67 Experiment Result — EXP-{experiment[-2:].upper()}",
        "",
        "The review's complete reading: every endpoint's frozen values, the",
        "matched contrasts, the prediction and roadmap comparison, and the",
        "SCOPE-49 disposition. GAP-59-08 stays explicit: E is the frozen",
        "scorecard's position-error score; no energy bar is adjudicated here.",
        "",
        "```json phase67-review",
        json.dumps(review, indent=2, sort_keys=True),
        "```",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# The exact run matrices.
# --------------------------------------------------------------------------


def _metadata_windows(experiment, metadata, arm):
    """The window list one (experiment, arm) pair runs, per orbit."""
    _require(
        isinstance(metadata, Mapping)
        and metadata.get("schema") == METADATA_SCHEMA,
        "the metadata record must be a phase67-metadata/v1 mapping",
    )
    _require(
        metadata.get("experiment") == experiment,
        f"the committed metadata record belongs to experiment "
        f"{metadata.get('experiment')!r}, not {experiment!r}",
    )
    orbits = metadata.get("orbits")
    _require(isinstance(orbits, Mapping) and orbits,
             "the metadata record names no orbit evidence")
    window_name = "full" if experiment != "exp05" else arm
    windows = {}
    for case, orbit_key, _seed in CASES:
        block = orbits.get(orbit_key)
        _require(
            isinstance(block, Mapping),
            f"the metadata record names no evidence for orbit {orbit_key!r}",
        )
        window = (block.get("windows") or {}).get(window_name)
        _require(
            isinstance(window, Mapping),
            f"the metadata record names no {window_name!r} window for orbit "
            f"{orbit_key!r}",
        )
        for field in ("t_end", "first_time", "last_time", "sample_count",
                      "physical_times_sha256", "normalized_tau_sha256"):
            _require(field in window,
                     f"the {window_name!r} window of {orbit_key!r} names no {field}")
        baselines = window.get("baselines")
        _require(
            isinstance(baselines, Mapping)
            and isinstance(baselines.get("window_mean_constant"), Mapping)
            and isinstance(baselines.get("two_kepler"), Mapping),
            f"the {window_name!r} window of {orbit_key!r} names no baseline pair",
        )
        windows[case] = window
    return windows


def phase67_run_matrix(experiment, kind, *, metadata, metadata_sha=None,
                       science_steps=None, phase_dir=None, repo_root=None):
    """The exact case-major Cartesian product rows of one experiment/kind.

    Every declared case in the registered order crossed with every declared
    arm in the plan's arm order, each row carrying its orbit-aware variant
    name, the committed metadata digest binding it to the window evidence it
    depends on, its exact physical window and its exact registration and
    output paths inside the phase directory. ``kind`` is ``timing`` (the
    registered timing scale) or ``science`` (the frozen budget scale;
    ``science_steps`` names the budget's common N, and without it the
    schedule fields defer to the budget).
    """
    _require(experiment in ARM_ORDER,
             f"unknown Phase 67 experiment {experiment!r}; known: {list(ARM_ORDER)}")
    _require(kind in ("timing", "science"),
             f"unknown matrix kind {kind!r}; known: timing, science")
    _require(
        isinstance(metadata, Mapping)
        and metadata.get("schema") == METADATA_SCHEMA,
        "the metadata record must be a phase67-metadata/v1 mapping",
    )
    rule = _rule()
    if kind == "timing":
        steps = int(rule["timing_steps"])
        warmup = int(rule["timing_warmup"])
        cap = float(rule["timing_cap_seconds"])
    else:
        _require(
            science_steps is None or (
                not isinstance(science_steps, bool)
                and isinstance(science_steps, int)
                and science_steps > 0
            ),
            f"the science steps must be a positive integer; got {science_steps!r}",
        )
        steps = science_steps
        warmup = int(rule["warmup_steps"])
        cap = float(rule["cap_seconds"])
    digest = metadata_sha if metadata_sha is not None else metadata.get("sha256")
    _require(
        isinstance(digest, str) and _HEX64.fullmatch(digest) is not None,
        "the matrix rows need the committed metadata record's sha256",
    )
    from pinn.verification.diagnostic_phase67_catalog import phase67_arm_variant

    rows = []
    for case, orbit_key, seed in CASES:
        for arm in ARM_ORDER[experiment]:
            window = _metadata_windows(experiment, metadata, arm)[case]
            t_end = _finite(window["t_end"],
                            f"the {arm} window endpoint of {orbit_key!r}")
            if experiment == "exp05":
                variant_name = f"exp05-{arm}-{orbit_key.rsplit('/', 1)[-1]}"
            else:
                variant_name = phase67_arm_variant(
                    experiment, arm, orbit_key
                ).name
            schedule = {
                "optimizer_steps": steps,
                "warmup_steps": warmup,
                "measured_steps": None if steps is None else steps - warmup,
                "similarity_cadence": (
                    None if steps is None else phase67_cadence(steps)
                ),
                "score_cadence": (
                    None if steps is None else phase67_score_cadence(steps)
                ),
                "loss_trace_stride": (
                    None if steps is None else phase67_loss_trace_stride(steps)
                ),
                "cap_seconds": cap,
            }
            rows.append({
                "experiment": experiment,
                "kind": kind,
                "case": case,
                "arm": arm,
                "orbit_key": orbit_key,
                "seed": seed,
                "variant_name": variant_name,
                "t_end": t_end,
                "metadata_sha256": digest,
                "physical_window": {"t_start": 0.0, "t_end": t_end},
                "registration_path": (
                    f"evidence/{experiment}/{kind}/{case}/{arm}/registration.json"
                ),
                "output_path": (
                    f"evidence/{experiment}/{kind}/{case}/{arm}/record.json"
                ),
                "schedule": schedule,
            })
    return rows


def _write_matrix(experiment, kind, rows, *, metadata_sha, path, science_steps=None):
    rule = _rule()
    payload = {
        "schema": RUN_MATRIX_SCHEMA,
        "experiment": experiment,
        "kind": kind,
        "metadata_sha256": metadata_sha,
        "schedule": {
            "optimizer_steps": (
                int(rule["timing_steps"]) if kind == "timing" else science_steps
            ),
            "cap_seconds": (
                float(rule["timing_cap_seconds"]) if kind == "timing"
                else float(rule["cap_seconds"])
            ),
        },
        "rows": rows,
    }
    _exclusive_json_write(path, payload)
    return payload


def _load_matrix(experiment, kind, *, phase_dir):
    path = phase_dir / f"evidence/{experiment}/{kind}-matrix.json"
    _require(path.is_file(),
             f"the {kind} matrix is missing: evidence/{experiment}/{kind}-matrix.json")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(f"the {kind} matrix is not readable JSON: {exc}")
    _require(isinstance(doc, Mapping) and doc.get("schema") == RUN_MATRIX_SCHEMA,
             f"the {kind} matrix must be schema {RUN_MATRIX_SCHEMA!r}")
    _require(doc.get("experiment") == experiment and doc.get("kind") == kind,
             "the committed matrix belongs to another experiment or kind")
    return path, doc


def _committed_metadata_record(experiment, *, root, phase_dir):
    directory = phase_dir / f"evidence/{experiment}/metadata"
    record_path = directory / "record.json"
    _require(record_path.is_file(),
             f"the metadata capture record is missing for {experiment!r}; run "
             "capture-metadata and commit it first")
    rel = _relative(root, record_path)
    _require_committed(root, rel, "metadata capture record")
    try:
        doc = json.loads(record_path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(
            f"the metadata capture record is not readable JSON: {exc}"
        ) from exc
    _require(isinstance(doc, Mapping) and doc.get("schema") == METADATA_SCHEMA,
             f"the metadata capture record must be schema {METADATA_SCHEMA!r}")
    _require(doc.get("experiment") == experiment,
             f"the committed metadata record belongs to experiment "
             f"{doc.get('experiment')!r}")
    _require(doc.get("status") == "complete",
             "the committed metadata capture is not complete")
    return record_path, doc, _sha256_file(record_path)


def _materialize_exp05_variants(metadata):
    """Register the exp05 lap variants from the committed metadata record."""
    from pinn.verification.diagnostic_phase67_catalog import (
        EXP02_D12_VARIANT,
    )

    reference = EXP02_D12_VARIANT
    declarations = []
    for orbit_key, block in metadata["orbits"].items():
        orbit_id = orbit_key.rsplit("/", 1)[-1]
        for arm in ARM_ORDER["exp05"]:
            window = (block.get("windows") or {}).get(arm)
            if not isinstance(window, Mapping):
                continue
            declarations.append(DiagnosticVariant(
                name=f"exp05-{arm}-{orbit_id}",
                time_features=reference.time_features,
                depth=reference.depth,
                width=reference.width,
                learning_rate=reference.learning_rate,
                window_length=float(window["t_end"]),
                first_omega_0=reference.first_omega_0,
                hidden_omega_0=reference.hidden_omega_0,
            ))
    if declarations:
        register_exp05_window_variants(declarations)


# --------------------------------------------------------------------------
# The metadata registration and the gated metadata-only capture.
# --------------------------------------------------------------------------

_METADATA_ALGORITHM_KEYS = (
    "reader", "normalizer", "baselines", "frequency", "harmonics",
    "harmonic_phase_increment", "byte_bound", "cap_seconds",
)


def admit_phase67_metadata_registration(registration_path, *, repo_root=None):
    """Admit the committed metadata registration before any capture.

    The registration file must be committed clean, carry the
    phase67-metadata-registration schema, and pin the frozen design, the
    prediction page and the harness freeze at their current committed bytes;
    its orbits must be exactly the two registered panel systems and its
    algorithm block must name the committed metadata algorithm. Reuses the
    guard's provenance primitives (tracked-clean + digest-exact + an
    introducing commit that is an ancestor of HEAD).
    """
    root = _repo_root(repo_root)
    path = Path(registration_path)
    if not path.is_absolute():
        path = root / path
    _require(path.is_file(), f"the metadata registration is missing: {path.name}")
    rel = _relative(root, path)
    _require_committed(root, rel, "metadata registration")
    introducing = _introducing_commit(root, rel)
    _require(introducing is not None,
             "the metadata registration has no introducing commit")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(
            f"the metadata registration is not readable JSON: {exc}"
        ) from exc
    _require(isinstance(doc, Mapping)
             and doc.get("schema") == METADATA_REGISTRATION_SCHEMA,
             f"the metadata registration must be schema "
             f"{METADATA_REGISTRATION_SCHEMA!r}")
    for field in ("design", "page", "harness_freeze"):
        entry = doc.get(field)
        _require(
            isinstance(entry, Mapping) and isinstance(entry.get("path"), str)
            and isinstance(entry.get("sha256"), str),
            f"the metadata registration names no {field} entry",
        )
        _require_committed(root, entry["path"], f"metadata registration {field}")
        _require(
            _sha256_file(root / entry["path"]) == entry["sha256"],
            f"the pinned {field} changed since the registration was committed: "
            f"{entry['path']}",
        )
    _require(doc.get("orbits") == ["hierarchical/gold/1632", "hierarchical/gold/851"],
             "the metadata registration must name exactly the two registered "
             "panel systems 1632 and 851")
    algorithm = doc.get("algorithm")
    _require(isinstance(algorithm, Mapping)
             and all(key in algorithm for key in _METADATA_ALGORITHM_KEYS),
             "the metadata registration names no complete algorithm block")
    cap = algorithm.get("cap_seconds")
    _require(
        not isinstance(cap, bool) and isinstance(cap, (int, float))
        and float(cap) == float(_rule()["timing_cap_seconds"]),
        "the metadata registration's whole-launch cap must equal the "
        "registered 900-second metadata cap",
    )
    verify_harness_freeze(root, _phase_directory(None, root))
    return root, doc


def _window_evidence(data, scorecard, *, prefix=None):
    """One window's grid evidence and independently checked baselines."""
    from pinn.verification.diagnostic_phase67_windows import (
        same_window_expectations,
    )

    evidence = same_window_expectations(data, scorecard=scorecard, prefix=prefix)
    kepler = evidence["two_kepler"]
    harness = kepler["harness"]
    applicable = bool(harness.get("applicable", False))
    # The retained tau digest convention is the RECORDED train grid's tau
    # column (the residency-cast times the fit actually trains and logs),
    # exactly the 67-05 reader's `_committed_metadata` convention — not the
    # score view's exact float64 re-derivation.
    import numpy as np

    tau_column = getattr(getattr(data, "data_points", None), "tau_ic13", None)
    if tau_column is not None:
        tau_values = np.asarray(
            tau_column.detach().cpu().numpy()[:, 0], dtype=np.float64
        ).reshape(-1)
        tau_sha = hashlib.sha256(
            np.ascontiguousarray(tau_values, dtype=np.float64).tobytes()
        ).hexdigest()
    else:
        tau_sha = evidence["normalized_tau_sha256"]
    return {
        "first_time": evidence["window"]["first_time"],
        "last_time": evidence["window"]["last_time"],
        "sample_count": evidence["window"]["sample_count"],
        "physical_times_sha256": evidence["physical_times_sha256"],
        "normalized_tau_sha256": tau_sha,
        "t_end": float(evidence["window"]["last_time"]),
        "baselines": {
            "window_mean_constant": {
                "E": float(evidence["constant"]["harness"]["score"]["E"]),
            },
            "two_kepler": (
                {"applicable": True,
                 "E": float(harness["score"]["E"])} if applicable
                else {
                    "applicable": False,
                    "failure": harness.get("failure"),
                    "reason": harness.get("reason"),
                }
            ),
        },
        "gap_59_08": evidence["gap_59_08"],
    }


def _phase_increments(times, frequency):
    """The max adjacent harmonic-phase increment per harmonic k in (1, 2)."""
    import numpy as np

    values = np.asarray(times, dtype=np.float64).reshape(-1)
    _require(values.size >= 2, "a window needs at least two samples")
    delta = float(np.max(np.diff(values)))
    return {
        f"harmonic_{k}": 2.0 * math.pi * k * float(frequency) * delta
        for k in (1, 2)
    }


def capture_phase67_metadata(
    experiment, *, repo_root=None, phase_dir=None, load_orbit=None,
    load_reference=None, read_power=None, now=None,
):
    """The registered gated metadata-only capture for both panel systems.

    Admits the committed metadata registration, gates on AC power inside the
    owner's weekend window, claims the output exclusively, then — in this
    command only — loads the registered TRAIN gold records through the
    injected/default orbit loader, derives the exact grid evidence and the
    independently checked same-window baselines for every used window, and
    records the census frequency and harmonic-phase evidence. No optimizer
    and no model is ever constructed. The record and attempt are published
    only after every window's evidence exists; any refusal leaves the
    attempt explicitly incomplete and publishes nothing.
    """
    from pinn.verification.diagnostic_power import (
        PowerRefused,
        require_ac_power,
        require_weekend_window,
    )
    from pinn.verification.feasibility_scorecard import load_scorecard

    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    registration = phase / f"evidence/{experiment}/metadata-registration.json"
    _admit_root, doc = admit_phase67_metadata_registration(
        registration, repo_root=root
    )
    try:
        first_line = require_ac_power(read_power=read_power)
        local = require_weekend_window(now)
    except PowerRefused as exc:
        raise Phase67CommandRefused(str(exc)) from exc
    directory = phase / f"evidence/{experiment}/metadata"
    record_path = directory / "record.json"
    attempt_path = directory / "attempt.json"
    receipt_path = directory / "power-gate.json"
    if record_path.exists():
        raise Phase67CommandRefused(
            "a metadata capture record already exists; the first completed "
            "capture is the evidence and a second never replaces it"
        )
    directory.mkdir(parents=True, exist_ok=True)
    _exclusive_json_write(attempt_path, {
        "schema": METADATA_ATTEMPT_SCHEMA,
        "status": "running",
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registration": _entry(
            _relative(root, registration), _sha256_file(registration)
        ),
        "whole_run_cap_seconds": float(
            doc["algorithm"]["cap_seconds"]
        ),
    })
    try:
        loader = load_orbit if load_orbit is not None else _default_load_orbit
        reference_loader = (
            load_reference if load_reference is not None else _default_load_reference
        )
        scorecard = load_scorecard()
        orbits = {}
        for orbit_key in doc["orbits"]:
            data = loader(orbit_key, float(scorecard.section("scoring_grid")["t_max"]))
            windows = {"full": _window_evidence(data, scorecard)}
            if experiment == "exp05":
                from pinn.verification.diagnostic_phase67_windows import (
                    first_lap_prefixes,
                )

                reference = reference_loader(orbit_key)
                census_n_in = _census_n_in(orbit_key)
                prefixes = first_lap_prefixes(
                    reference, census_n_in=census_n_in, scorecard=scorecard,
                )
                by_laps = {
                    int(prefix["requested_laps"]): prefix for prefix in prefixes
                }
                for arm in ARM_ORDER["exp05"]:
                    laps = int(arm.removeprefix("lap"))
                    prefix = by_laps[laps]
                    window_data = loader(orbit_key, float(prefix["requested_endpoint"]))
                    windows[arm] = _window_evidence(
                        window_data, scorecard, prefix=prefix
                    )
            full_times = _window_times(loader, orbit_key, scorecard)
            n_in = _census_n_in(orbit_key)
            frequency = n_in / float(T_CHARACTERISTIC_TIME)
            orbits[orbit_key] = {
                "census": {
                    "N_in": n_in,
                    "panels_path": CENSUS_PANELS_RELATIVE_PATH,
                },
                "frequency": {
                    "f_cycles_per_physical_unit": frequency,
                    "harmonics": {"f1": [1], "f12": [1, 2]},
                },
                "max_adjacent_phase_increment_rad": _phase_increments(
                    full_times, frequency
                ),
                "windows": windows,
            }
        record = {
            "schema": METADATA_SCHEMA,
            "experiment": experiment,
            "status": "complete",
            "registration": _entry(
                _relative(root, registration), _sha256_file(registration)
            ),
            "harness_freeze": doc["harness_freeze"],
            "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "window": {
                "timezone": "America/Chicago",
                "local_time": local.isoformat(timespec="seconds"),
                "isoweekday": int(local.isoweekday()),
            },
            "orbits": orbits,
            "access": {
                "reads": {"train": len(orbits)},
                "note": "metadata-only TRAIN gold reads for the registered "
                        "orbits; no model is constructed and no training "
                        "step runs",
            },
            "algorithm": dict(doc["algorithm"]),
        }
        receipt = {
            "schema": "phase66-power-gate/v1",
            "checked_utc": record["checked_utc"],
            "power_source": "AC Power",
            "pmset_first_line": first_line,
            "registration": _relative(root, registration),
            "output": _relative(root, record_path),
            "window": record["window"],
            "metadata_only": True,
        }
        _exclusive_json_write(record_path, record)
        _exclusive_json_write(receipt_path, receipt)
    except BaseException as exc:
        payload = json.loads(attempt_path.read_bytes().decode("utf-8"))
        payload["status"] = "incomplete"
        payload["ended_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        payload["reason"] = f"{type(exc).__name__}: {exc}"
        attempt_path.write_bytes(_canonical_json(payload).encode("utf-8"))
        raise
    payload = json.loads(attempt_path.read_bytes().decode("utf-8"))
    payload["status"] = "published"
    payload["ended_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload["record_sha256"] = _sha256_file(record_path)
    attempt_path.write_bytes(_canonical_json(payload).encode("utf-8"))
    return record


def _census_n_in(orbit_key):
    from pinn.verification.diagnostic_phase67_catalog import census_n_in

    try:
        orbit_id = int(orbit_key.rsplit("/", 1)[-1])
    except ValueError as exc:
        raise Phase67CommandRefused(
            f"the orbit key names no integer id: {orbit_key!r}"
        ) from exc
    try:
        return census_n_in(orbit_id)
    except Exception as exc:  # VariantRefused and friends: fail closed
        raise Phase67CommandRefused(
            f"the committed census holds no validated N_in for {orbit_key!r}: {exc}"
        ) from exc


def _window_times(loader, orbit_key, scorecard):
    """The full-window physical times of one orbit (for phase increments)."""
    import numpy as np

    data = loader(orbit_key, float(scorecard.section("scoring_grid")["t_max"]))
    times = np.asarray(data.score.times, dtype=np.float64).reshape(-1)
    return [float(value) for value in times.tolist()]


def _default_load_orbit(orbit_key, window_length):
    """The real registered metadata loader (plan 67-06 task 2)."""
    from pinn.verification.diagnostic_data import (
        load_diagnostic_data,
        one_orbit_spec,
        open_diagnostic_context,
    )
    from pinn.verification.feasibility_scorecard import load_scorecard
    from pinn.verification.diagnostic_fit import _parse_orbit_key

    context = open_diagnostic_context(repo_root=None)
    spec = one_orbit_spec(_parse_orbit_key(orbit_key))
    return load_diagnostic_data(
        spec, context, scorecard=load_scorecard(), dtype=torch_dtype(),
        device=torch_device(), window_length=float(window_length),
    )


def _default_load_reference(orbit_key):
    """The real raw gold reference for the EXP-05 prefix selection."""
    from pinn.verification.diagnostic_data import (
        open_diagnostic_context,
    )
    from pinn.verification.production_reference import load_reference
    from pinn.verification.diagnostic_fit import _parse_orbit_key

    context = open_diagnostic_context(repo_root=None)
    return load_reference(context.reader, _parse_orbit_key(orbit_key))


def torch_dtype():
    import torch

    return {"float64": torch.float64, "float32": torch.float32}[
        DEFAULT_RUNTIME["dtype"]
    ]


def torch_device():
    import torch

    return torch.device(DEFAULT_RUNTIME["device"])


# --------------------------------------------------------------------------
# Registrations, cost rows and the budget.
# --------------------------------------------------------------------------


def _row_settings(experiment, kind, row, *, steps, cap):
    """One row's validated smoke settings block."""
    from pinn.verification.diagnostic_phase67_catalog import phase67_arm_variant

    declaration = phase67_arm_variant(experiment, row["arm"], row["orbit_key"])
    return {
        "variant": declaration.to_json_dict(),
        "variant_registry": PHASE67_REGISTRY_NAME,
        "seed": int(row["seed"]),
        "runtime": dict(DEFAULT_RUNTIME),
        "orbit_key": row["orbit_key"],
        "orbit_note": f"the registered {row['case']} case",
        "physical_window": dict(row["physical_window"]),
        "optimizer_steps": int(steps),
        "warmup_steps": int(_rule()["warmup_steps"] if kind == "science"
                            else _rule()["timing_warmup"]),
        "measured_steps": int(steps - (
            _rule()["warmup_steps"] if kind == "science"
            else _rule()["timing_warmup"]
        )),
        "similarity_cadence": phase67_cadence(steps),
        "score_cadence": phase67_score_cadence(steps),
        "loss_trace_stride": phase67_loss_trace_stride(steps),
        "whole_run_cap_seconds": float(cap),
        "optimizer": {
            "kind": "adam_constant_rate",
            "lr": float(declaration.learning_rate),
            "scheduler": None, "clipping": None, "physics_term": None,
            "polish": None,
        },
        "loss": {"kind": "data_only"},
        "timing_definitions": (
            "synchronized completed-work segments around setup, warmup, "
            "measured updates, per-event logging/scoring and publication"
        ),
        "reading_rule": {
            "mechanical_pass": "every registered step and event completes "
                               "finite and the audit is clean",
            "incomplete": "an interrupted or over-cap attempt stays "
                          "incomplete and is never a result",
            "out_of_branch": "the phase67 contrast and confirmation rules "
                             "read the branch; no threshold is re-set here",
            "branch_rule": "phase67_contrast/phase67_confirmation (67-05)",
        },
    }


def _provenance_blocks(root, provenance_registration):
    """The copied provenance blocks of a committed fit registration."""
    path = root / provenance_registration
    _require(path.is_file(),
             f"the provenance registration is missing: {provenance_registration}")
    try:
        doc = json.loads(path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(
            f"the provenance registration is not readable JSON: {exc}"
        ) from exc
    blocks = {}
    for key in ("logger_parity", "context", "frozen", "pinned"):
        if key in doc:
            blocks[key] = doc[key]
    _require("logger_parity" in blocks,
             "the provenance registration names no logger_parity block")
    return blocks


def _write_row_registrations(experiment, kind, rows, *, root, phase_dir,
                             metadata, page_rel, provenance_registration=None,
                             dependencies=None):
    """Write every row registration beside its future evidence."""
    provenance_registration = (
        provenance_registration or PROVENANCE_REGISTRATION_REL
    )
    blocks = _provenance_blocks(root, provenance_registration)
    dependencies = list(dependencies or PHASE67_DEPENDENCIES)
    for dependency in dependencies:
        _require((root / dependency).is_file(),
                 f"the pinned harness file is missing: {dependency}")
    freeze_rel = _relative(root, phase_dir / "evidence/harness-freeze.json")
    page_repo_rel = _relative(root, phase_dir / page_rel)
    page_sha = _sha256_file(root / page_repo_rel)
    for row in rows:
        window = _metadata_windows(experiment, metadata, row["arm"])[row["case"]]
        steps = row["schedule"]["optimizer_steps"]
        _require(steps is not None,
                 "the science registrations need the budget's frozen step count")
        settings = _row_settings(experiment, kind, row, steps=steps,
                                 cap=row["schedule"]["cap_seconds"])
        doc = {
            "schema": "phase65-fit-registration/v1",
            "title": (
                f"EXP-{experiment[-2:].upper()} {kind} row "
                f"{row['case']}/{row['arm']}"
            ),
            "committed_before": "the first real optimizer step of this row",
            "page": _entry(page_repo_rel, page_sha),
            "settings": settings,
            **blocks,
            "code_dependencies": [
                _entry(dependency, _sha256_file(root / dependency))
                for dependency in dependencies
            ],
            "harness_freeze": _entry(
                freeze_rel, _sha256_file(root / freeze_rel)
            ),
            "window_metadata": {
                "first_time": window["first_time"],
                "last_time": window["last_time"],
                "sample_count": window["sample_count"],
                "physical_times_sha256": window["physical_times_sha256"],
                "normalized_tau_sha256": window["normalized_tau_sha256"],
            },
            "window_baselines": dict(window["baselines"]),
            "phase67_row": {
                "experiment": experiment, "kind": kind, "case": row["case"],
                "arm": row["arm"], "metadata_sha256": row["metadata_sha256"],
            },
        }
        registration = phase_dir / row["registration_path"]
        registration.parent.mkdir(parents=True, exist_ok=True)
        _exclusive_json_write(registration, doc)
    # The EXP-05 lap variants materialize from the committed metadata.
    if experiment == "exp05":
        _materialize_exp05_variants(metadata)


def phase67_cost_rows(entries):
    """The validated cost-only rows of one experiment's timing records.

    ``entries`` are ``(identity, record, receipt, attempt, record_bytes,]
    weights_bytes])`` tuples — one per committed timing row. Only cost
    fields are read (status, steps, timing, event ledgers and the
    launch-to-end wall); no score, loss, tier or cosine value is extracted,
    so changed scientific values cannot alter a budget (T-67-10).
    """
    from pinn.verification.diagnostic_phase66 import launch_wall_seconds

    rows = []
    for entry in entries:
        identity, record, receipt, attempt, record_bytes = entry[:5]
        weights_bytes = entry[5] if len(entry) > 5 else 1
        _require(isinstance(record, Mapping),
                 "a timing record must be a mapping")
        _require(record.get("status") == "complete",
                 "an incomplete timing record cannot size the budget")
        steps = record.get("steps") or {}
        timing = record.get("timing") or {}
        events = (timing.get("events") or {})
        logging_events = events.get("logging")
        scoring_events = events.get("scoring")
        publication = events.get("publication_io")
        _require(
            isinstance(logging_events, list) and len(logging_events) == int(
                _rule()["similarity_events"]
            ),
            "a timing record's logging ledger is missing or malformed",
        )
        _require(
            isinstance(scoring_events, list) and len(scoring_events) == int(
                _rule()["score_events"]
            ),
            "a timing record's scoring ledger is missing or malformed",
        )
        _require(
            isinstance(publication, list) and publication
            and isinstance(publication[0], Mapping)
            and isinstance(publication[0].get("seconds"), (int, float)),
            "a timing record's publication ledger is missing or malformed",
        )
        rule = _rule()
        for field, expected in (
            ("requested", int(rule["timing_steps"])),
            ("warmup", int(rule["timing_warmup"])),
            ("measured", int(rule["timing_measured"])),
        ):
            value = steps.get(field)
            _require(
                not isinstance(value, bool) and isinstance(value, int)
                and value == expected,
                f"a timing record's steps.{field} is {value!r}; the "
                f"registered timing scale names {expected}",
            )
        launch_wall = launch_wall_seconds(receipt, attempt)
        rows.append({
            "identity": dict(identity),
            "timing": {
                "optimizer_steps": steps.get("requested"),
                "warmup_steps": steps.get("warmup"),
                "measured_steps": steps.get("measured"),
                "seconds_per_step": timing.get("seconds_per_step"),
                "warmup_seconds": timing.get("warmup_seconds"),
                "measured_seconds": timing.get("measured_seconds"),
            },
            "logger_event_seconds": [
                float(event["seconds"]) for event in logging_events
            ],
            "scorer_event_seconds": [
                float(event["seconds"]) for event in scoring_events
            ],
            "publication_io_seconds": float(publication[0]["seconds"]),
            "launch_wall_seconds": float(launch_wall),
            "record_bytes": int(record_bytes),
            "weights_bytes": int(weights_bytes),
        })
    return rows


def _row_run_dir(phase_dir, row):
    return (phase_dir / row["registration_path"]).parent


def _collect_timing_rows(experiment, *, root, phase_dir):
    """Every committed timing row's cost entry, keyed by its identity."""
    _path, matrix = _load_matrix(experiment, "timing", phase_dir=phase_dir)
    rel = _relative(root, _path)
    _require_committed(root, rel, "timing matrix")
    entries = []
    identities = []
    for row in matrix["rows"]:
        directory = _row_run_dir(phase_dir, row)
        record_path = directory / "record.json"
        _require(record_path.is_file(),
                 f"the timing row {row['case']}/{row['arm']} has no record")
        _require_committed(root, _relative(root, record_path),
                           f"timing record of {row['case']}/{row['arm']}")
        record = json.loads(record_path.read_bytes().decode("utf-8"))
        receipt = json.loads(
            (directory / "power-gate.json").read_bytes().decode("utf-8")
        )
        attempt = json.loads(
            (directory / "attempt.json").read_bytes().decode("utf-8")
        )
        _require(attempt.get("status") == "published",
                 f"the timing attempt of {row['case']}/{row['arm']} is not "
                 "published")
        weights = directory / "diagnostic.weights"
        _require(weights.is_file(),
                 f"the timing row {row['case']}/{row['arm']} has no weights")
        identity = {
            "experiment": row["experiment"], "arm": row["arm"],
            "orbit_key": row["orbit_key"], "seed": row["seed"],
            "window": row["t_end"],
        }
        entries.append((
            identity, record, receipt, attempt,
            len(record_path.read_bytes()), len(weights.read_bytes()),
        ))
        identities.append(identity)
    return matrix, entries, identities


def _budget_artifacts(experiment):
    return {
        "budget": f"evidence/{experiment}/budget.json",
        "budget_page": f"67-EXP{experiment[-2:].upper()}-BUDGET.md",
        "prediction_page": f"67-EXP{experiment[-2:].upper()}-PREDICTION.md",
        "science_matrix": f"evidence/{experiment}/science-matrix.json",
        "result_page": f"67-EXP{experiment[-2:].upper()}-RESULT.md",
        "review": f"evidence/{experiment}/review.json",
        "timing_page": f"67-EXP{experiment[-2:].upper()}-TIMING-PREDICTION.md",
        "design": f"evidence/{experiment}/design.json",
        "metadata_registration": f"evidence/{experiment}/metadata-registration.json",
        "metadata_record": f"evidence/{experiment}/metadata/record.json",
        "timing_matrix": f"evidence/{experiment}/timing-matrix.json",
        "ruling": f"67-EXP{experiment[-2:].upper()}-RULING.md",
    }


def write_budget(experiment, *, repo_root=None, phase_dir=None,
                 provenance_registration=None, dependencies=None):
    """Derive the cost-only budget and freeze the science registrations.

    Requires every timing row committed and published; consumes only their
    cost fields through :func:`phase67_cost_rows` and 67-04's
    ``phase67_budget``; writes the budget document, the budget page, the
    immutable science prediction page, the science matrix and every science
    registration. The earlier timing prediction page is never touched.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    _record_path, metadata, metadata_sha = _committed_metadata_record(
        experiment, root=root, phase_dir=phase
    )
    _matrix, entries, identities = _collect_timing_rows(
        experiment, root=root, phase_dir=phase
    )
    verify_harness_freeze(root, phase)
    budget_core = phase67_budget(
        [dict(
            identity=row["identity"],
            timing=dict(row["timing"]),
            logger_event_seconds=list(row["logger_event_seconds"]),
            scorer_event_seconds=list(row["scorer_event_seconds"]),
            publication_io_seconds=row["publication_io_seconds"],
            launch_wall_seconds=row["launch_wall_seconds"],
            record_bytes=row["record_bytes"],
            weights_bytes=row["weights_bytes"],
        ) for row in phase67_cost_rows(entries)],
        expected_identities=identities,
    )
    steps = int(budget_core["common_optimizer_steps"])
    science_rows = phase67_run_matrix(
        experiment, "science", metadata=metadata, metadata_sha=metadata_sha,
        science_steps=steps,
    )
    budget = {
        "schema": BUDGET_SCHEMA,
        "experiment": experiment,
        "timing_evidence": {
            "rows": [
                {"path": _relative(root, phase / row["output_path"]),
                 "sha256": _sha256_file(root / _relative(root, phase / row["output_path"]))}
                for row in _matrix["rows"]
            ],
        },
        "whole_run_cap_seconds": float(_rule()["cap_seconds"]),
        **budget_core,
    }
    design = phase67_design(experiment)
    _exclusive_json_write(phase / artifacts["budget"], budget)
    _exclusive_text_write(
        phase / artifacts["budget_page"], budget_page(design, budget)
    )
    _exclusive_text_write(
        phase / artifacts["prediction_page"], prediction_page(design, budget)
    )
    _write_matrix(
        experiment, "science", science_rows, metadata_sha=metadata_sha,
        path=phase / artifacts["science_matrix"], science_steps=steps,
    )
    _write_row_registrations(
        experiment, "science", science_rows, root=root, phase_dir=phase,
        metadata=metadata, page_rel=artifacts["prediction_page"],
        provenance_registration=provenance_registration,
        dependencies=dependencies,
    )
    return budget


def _has_number(text, number):
    token = repr(number)
    pattern = re.compile(r"(?<![0-9.])" + re.escape(token) + r"(?!\.?[0-9])")
    return pattern.search(text) is not None


# --------------------------------------------------------------------------
# Launch, review and audit (the remaining table commands live below).
# --------------------------------------------------------------------------


def phase67_prior_experiment_allowed(experiment, *, phase_dir, repo_root):
    """Whether a pending owner proposal blocks this experiment's launches.

    Only a committed review of an EARLIER experiment in the chain carrying a
    pending SCOPE-49 proposal (or ``dependent_launch_allowed`` false) blocks;
    the experiment's own review never blocks its own remaining rows.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    for prior in EXPERIMENT_CHAIN:
        if prior == experiment:
            return True
        review_path = phase / _budget_artifacts(prior)["review"]
        if not review_path.is_file():
            continue
        try:
            review = json.loads(review_path.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise Phase67CommandRefused(
                f"the committed review of {prior!r} is not readable JSON"
            )
        if review.get("scope49_disposition") == "proposal-pending" or \
                review.get("dependent_launch_allowed") is False:
            return False
    return True


def launch_phase67_row(
    experiment, kind, case, arm, *, repo_root=None, phase_dir=None,
    read_power=None, run=None, now=None, supervisor=None,
):
    """Launch exactly one registered row through the existing power gate.

    Requires the exact committed matrix row, its committed-clean
    registration, the committed prerequisite of its kind (the metadata
    record for timing; the committed budget for science) and every earlier
    experiment's committed review allowing the dependent launch, then
    delegates to ``diagnostic_power.launch`` with a fixed argv — one row per
    call, never a retry or a batch loop.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    _require(experiment in ARM_ORDER,
             f"unknown Phase 67 experiment {experiment!r}")
    _require(kind in ("timing", "science"), f"unknown matrix kind {kind!r}")
    _path, matrix = _load_matrix(experiment, kind, phase_dir=phase)
    _require_committed(root, _relative(root, _path), f"{kind} matrix")
    rows = [row for row in matrix["rows"]
            if row["case"] == case and row["arm"] == arm]
    _require(len(rows) == 1,
             f"the {kind} matrix names no exact row for case {case!r} arm "
             f"{arm!r}")
    row = rows[0]
    registration = phase / row["registration_path"]
    output = phase / row["output_path"]
    _require(registration.is_file(),
             f"the row registration is missing: {row['registration_path']}")
    _require_committed(root, _relative(root, registration),
                       f"{kind} row registration")
    if kind == "timing":
        _committed_metadata_record(experiment, root=root, phase_dir=phase)
    else:
        budget_path = phase / _budget_artifacts(experiment)["budget"]
        _require(budget_path.is_file(), "the committed budget is required "
                                        "before any science row launches")
        _require_committed(root, _relative(root, budget_path), "budget")
    for prior in EXPERIMENT_CHAIN:
        if prior == experiment:
            break
        review_path = phase / _budget_artifacts(prior)["review"]
        _require(
            review_path.is_file(),
            f"the prior experiment {prior!r} has no committed review; each "
            "result is reviewed before dependent work continues (D-10)",
        )
        _require_committed(root, _relative(root, review_path),
                           f"review of {prior!r}")
    _require(
        phase67_prior_experiment_allowed(experiment, phase_dir=phase, repo_root=root),
        "a pending SCOPE-49 owner proposal blocks the dependent experiment's "
        "launches",
    )
    _require(
        not output.exists(),
        f"an output record already exists at {_relative(root, output)}; the "
        "first completed run is the result and a second run never replaces it",
    )
    from pinn.verification.diagnostic_power import (
        PowerRefused,
        launch as power_launch,
    )

    try:
        return power_launch(
            registration, output, repo_root=root,
            read_power=read_power, run=run, now=now,
        )
    except PowerRefused as exc:
        raise Phase67CommandRefused(str(exc)) from exc


def check_row(experiment, kind, case, arm, *, repo_root=None, phase_dir=None):
    """One row's strict reading; no scientific score value is printed."""
    from pinn.verification.diagnostic_phase67_records import (
        read_phase67_run_directory,
    )

    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    _path, matrix = _load_matrix(experiment, kind, phase_dir=phase)
    rows = [row for row in matrix["rows"]
            if row["case"] == case and row["arm"] == arm]
    _require(len(rows) == 1,
             f"the {kind} matrix names no exact row for case {case!r} arm {arm!r}")
    row = rows[0]
    registration = phase / row["registration_path"]
    run_dir = _row_run_dir(phase, row)
    reading = read_phase67_run_directory(
        registration, run_dir, repo_root=root, expected_case={
            "experiment": row["experiment"], "arm": row["arm"],
            "case": _case_role(row["case"]), "orbit_key": row["orbit_key"],
            "seed": row["seed"],
        },
    )
    problems = reading["mechanical_problems"] + reading["setting_problems"]
    if problems:
        raise Phase67CommandRefused(
            "the row carries problems: " + "; ".join(problems)
        )
    return {
        "case": row["case"], "arm": row["arm"], "kind": kind,
        "problems": [],
        "checkpoint_steps": reading["checkpoint_steps"],
        "unsettled": reading["unsettled"],
    }


def _case_role(case_id):
    return {
        "main-1632-s42": "main",
        "repeat-851-s42": "repeat-system",
        "repeat-1632-s41": "repeat-seed",
    }[case_id]


def write_review(experiment, *, repo_root=None, phase_dir=None):
    """Review every science row against the committed predictions.

    Requires every science row committed and mechanically clean; reads each
    through the registration-bound science reader (scores only after the
    clean audit), runs the declared contrasts and the experiment
    confirmation (67-05), compares every result to the committed
    predictions and the roadmap in plain language, and records the SCOPE-49
    disposition — a refuted lead or an out-of-rule result raises a concrete
    owner proposal and blocks the dependent experiment's launches.
    """
    from pinn.verification.diagnostic_phase67_records import (
        read_phase67_run_directory,
    )

    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    _path, matrix = _load_matrix(experiment, "science", phase_dir=phase)
    _require_committed(root, _relative(root, _path), "science matrix")
    budget = json.loads(
        (phase / artifacts["budget"]).read_bytes().decode("utf-8")
    )
    _require_committed(root, _relative(root, phase / artifacts["budget"]), "budget")
    design = phase67_design(experiment)
    arms = list(ARM_ORDER[experiment])
    readings = {}
    for row in matrix["rows"]:
        registration = phase / row["registration_path"]
        run_dir = _row_run_dir(phase, row)
        _require_committed(root, _relative(root, registration),
                           f"science registration of {row['case']}/{row['arm']}")
        readings[(row["case"], row["arm"])] = read_phase67_run_directory(
            registration, run_dir, repo_root=root,
            expected_case={
                "experiment": row["experiment"], "arm": row["arm"],
                "case": _case_role(row["case"]), "orbit_key": row["orbit_key"],
                "seed": row["seed"],
            },
            include_scores=True,
        )
    contrasts = {}
    predictions_comparison = {}
    pending = False
    for arm in arms:
        if phase67_control_arm(experiment, arm) == arm:
            continue
        arm_readings = {}
        for case_id, _orbit, _seed in CASES:
            arm_readings[_case_role(case_id)] = {
                "arm": readings[(case_id, arm)],
                "control": readings[(case_id, arms[-1])],
            }
        contrast = phase67_contrast(experiment, arm, arm_readings)
        disposition = phase67_scope_disposition(contrast["confirmation"])
        contrast["scope_disposition"] = disposition
        contrasts[arm] = contrast
        predictions_comparison[arm] = {
            "registered_hypothesis": design["prediction_table"][arm]["hypothesis"],
            "observed_confirmation": contrast["confirmation"],
            "observed_disposition": disposition["scope49_disposition"],
            "case_directions": {
                role: case["direction"] for role, case in contrast["cases"].items()
            },
        }
        if not disposition["dependent_launch_allowed"]:
            pending = True
    confirmation = phase67_confirmation(
        experiment,
        [contrasts[arm] for arm in contrasts],
        declared_arms=arms,
    )
    review = {
        "schema": REVIEW_SCHEMA,
        "experiment": experiment,
        "contrasts": contrasts,
        "confirmation": confirmation,
        "predictions_comparison": predictions_comparison,
        "roadmap_comparison": (
            "each contrast's confirmation label is read against the committed "
            "prediction table; the roadmap's next experiment proceeds only "
            "when this review allows the dependent launch"
        ),
        "scope49_disposition": "proposal-pending" if pending else "none",
        "dependent_launch_allowed": not pending,
        "proposed_change": (
            "a refuted lead or an out-of-rule result was observed; the owner "
            "decides under SCOPE-49 whether the remaining experiments run, "
            "change or stop"
            if pending else None
        ),
        "gap_59_08": GAP_59_08_NOTE,
        "budget_steps": budget["common_optimizer_steps"],
    }
    _exclusive_json_write(phase / artifacts["review"], review)
    _exclusive_text_write(
        phase / artifacts["result_page"], result_page(experiment, review),
    )
    return review


def _verify_ruling(experiment, review, *, root, phase_dir):
    """The optional owner ruling over a pending proposal (SCOPE-49)."""
    artifacts = _budget_artifacts(experiment)
    ruling_path = phase_dir / artifacts["ruling"]
    _require(ruling_path.is_file(),
             f"a pending SCOPE-49 proposal requires the committed owner "
             f"ruling {artifacts['ruling']}")
    rel = _relative(root, ruling_path)
    _require_committed(root, rel, "owner ruling")
    review_rel = _relative(root, phase_dir / artifacts["review"])
    result_rel = _relative(root, phase_dir / artifacts["result_page"])
    review_commit = _introducing_commit(root, review_rel)
    result_commit = _introducing_commit(root, result_rel)
    ruling_commit = _introducing_commit(root, rel)
    _require(ruling_commit is not None and review_commit is not None
             and result_commit is not None,
             "the reviewed artifacts and the ruling must all be committed")
    _require(
        _git(root, "merge-base", "--is-ancestor", review_commit,
             ruling_commit).returncode == 0
        and _git(root, "merge-base", "--is-ancestor", result_commit,
                 ruling_commit).returncode == 0,
        "the ruling must be committed after the reviewed artifacts",
    )
    try:
        ruling = json.loads(ruling_path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise Phase67CommandRefused(
            f"the owner ruling is not readable JSON: {exc}"
        ) from exc
    _require(isinstance(ruling, Mapping),
             "the owner ruling must be a JSON object")
    for field in ("review_sha256", "result_page_sha256", "proposal_sha256"):
        value = ruling.get(field)
        _require(isinstance(value, str) and _HEX64.fullmatch(value) is not None,
                 f"the owner ruling names no {field} digest")
    _require(
        ruling["review_sha256"] == _sha256_file(root / review_rel),
        "the ruling's review digest is stale",
    )
    _require(
        ruling["result_page_sha256"] == _sha256_file(root / result_rel),
        "the ruling's result-page digest is stale",
    )
    proposal = review.get("proposed_change")
    proposal_digest = hashlib.sha256(
        json.dumps(proposal, sort_keys=True).encode("utf-8")
    ).hexdigest()
    _require(
        ruling["proposal_sha256"] == proposal_digest,
        "the ruling's proposal digest does not match the reviewed proposal",
    )
    disposition = ruling.get("disposition")
    _require(
        disposition in ("authorized", "hold", "changed-scope"),
        f"the ruling's disposition must be an explicit authorized, hold or "
        f"changed-scope verdict; got {disposition!r}",
    )
    _require(
        disposition != "hold",
        "the owner ruled hold; the dependent launch stays blocked",
    )
    allowed = ruling.get("allowed_dependent_work")
    _require(
        isinstance(allowed, list) and allowed
        and all(isinstance(item, str) and item for item in allowed),
        "the ruling names no exact scope of dependent work allowed",
    )
    _require(
        any(experiment in item or item.endswith("*") for item in allowed),
        f"the ruling's allowed dependent work does not cover {experiment!r}",
    )
    words = ruling.get("owner_words_verbatim")
    _require(
        isinstance(words, str) and words.strip(),
        "the ruling records no verbatim owner words",
    )
    return ruling


def check_review(experiment, *, repo_root=None, phase_dir=None, admit_for=None):
    """Committed result/review agreement and the conditional scope authority.

    ``PHASE67-REVIEW-OK`` is printed only when the next dependent launch is
    allowed: a pending proposal requires the committed owner ruling (after
    the reviewed artifacts, digest-faithful, explicit, scope-matching and
    never a hold).
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    review_path = phase / artifacts["review"]
    _require(review_path.is_file(), "the review is missing")
    rel = _relative(root, review_path)
    _require_committed(root, rel, "review")
    review = json.loads(review_path.read_bytes().decode("utf-8"))
    _require(isinstance(review, Mapping)
             and review.get("schema") == REVIEW_SCHEMA,
             f"the review must be schema {REVIEW_SCHEMA!r}")
    result_path = phase / artifacts["result_page"]
    _require(result_path.is_file(), "the result page is missing")
    _require_committed(root, _relative(root, result_path), "result page")
    page = result_path.read_text()
    _require(
        json.dumps(review, indent=2, sort_keys=True) in page,
        "the committed result page does not embed the committed review",
    )
    if review.get("scope49_disposition") == "proposal-pending" or \
            review.get("dependent_launch_allowed") is False:
        _verify_ruling(experiment, review, root=root, phase_dir=phase)
        return {"allowed": True, "ruled": True}
    _require(review.get("dependent_launch_allowed") is True,
             "the review names no dependent-launch decision")
    return {"allowed": True, "ruled": False}


def audit_phase67(*, repo_root=None, phase_dir=None):
    """The plan's declared audit helper name (see :func:`audit_phase`)."""
    return audit_phase(repo_root=repo_root, phase_dir=phase_dir)


def audit_phase(*, repo_root=None, phase_dir=None):
    """The read-only evidence, chronology, scope and hash audit.

    Summarizes every experiment's committed artifacts, their introducing
    chronology, the scope status (a pending proposal without a committed
    ruling flags the audit) and the harness-freeze agreement. Writes
    nothing.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    problems = []
    experiments = {}
    try:
        verify_harness_freeze(root, phase)
        freeze_ok = True
    except Phase67CommandRefused as exc:
        freeze_ok = False
        problems.append(f"harness freeze: {exc}")
    for experiment in EXPERIMENTS:
        artifacts = _budget_artifacts(experiment)
        state = {"freeze_verified": freeze_ok}
        for name, rel in artifacts.items():
            path = phase / rel
            committed = (
                path.is_file() and _tracked_and_clean(root, _relative(root, path))
            )
            state[name] = "committed" if committed else (
                "present-uncommitted" if path.is_file() else "absent"
            )
        review_path = phase / artifacts["review"]
        scope = "none"
        if review_path.is_file():
            try:
                review = json.loads(review_path.read_bytes().decode("utf-8"))
                if review.get("scope49_disposition") == "proposal-pending":
                    ruling = phase / artifacts["ruling"]
                    scope = "proposal-ruled" if (
                        ruling.is_file()
                        and _tracked_and_clean(root, _relative(root, ruling))
                    ) else "proposal-pending"
            except (UnicodeDecodeError, ValueError):
                scope = "review-unreadable"
                problems.append(f"{experiment}: the review is not readable JSON")
        state["scope"] = scope
        if scope == "proposal-pending":
            problems.append(
                f"{experiment}: a pending SCOPE-49 proposal has no committed "
                "owner ruling"
            )
        experiments[experiment] = state
    status = "PHASE67-AUDIT-OK" if not problems else "PHASE67-AUDIT-PROBLEMS"
    return {"status": status, "problems": problems, "experiments": experiments}


# --------------------------------------------------------------------------
# The remaining table commands: design, metadata and matrix writing/checks.
# --------------------------------------------------------------------------


def prepare_design(experiment, *, repo_root=None, phase_dir=None):
    """Exclusively create the design, its page and the metadata registration.

    No corpus access: the three artifacts freeze the full scientific design,
    the reading branches and the metadata algorithm before any real
    operation, and the metadata registration pins the design, the page and
    the committed harness freeze.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    freeze = verify_harness_freeze(root, phase)
    design = phase67_design(experiment)
    design_path = phase / artifacts["design"]
    page_path = phase / artifacts["timing_page"]
    registration_path = phase / artifacts["metadata_registration"]
    _exclusive_json_write(design_path, design)
    _exclusive_text_write(page_path, timing_prediction_page(design))
    freeze_rel = _relative(root, phase / "evidence/harness-freeze.json")
    _exclusive_json_write(registration_path, {
        "schema": METADATA_REGISTRATION_SCHEMA,
        "title": f"EXP-{experiment[-2:].upper()} metadata registration",
        "experiment": experiment,
        "committed_before": "any real metadata, timing or science operation",
        "design": _entry(
            _relative(root, design_path), _sha256_file(design_path)
        ),
        "page": _entry(_relative(root, page_path), _sha256_file(page_path)),
        "harness_freeze": _entry(
            freeze_rel, _sha256_file(root / freeze_rel)
        ),
        "orbits": ["hierarchical/gold/1632", "hierarchical/gold/851"],
        "algorithm": dict(design["metadata_algorithm"]),
    })
    return {
        "design": _relative(root, design_path),
        "page": _relative(root, page_path),
        "metadata_registration": _relative(root, registration_path),
        "freeze_files": len(freeze["files"]),
    }


def check_design(experiment, *, repo_root=None, phase_dir=None):
    """Read-only verification of the committed design trio."""
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    design_path = phase / artifacts["design"]
    page_path = phase / artifacts["timing_page"]
    registration_path = phase / artifacts["metadata_registration"]
    for name, path in (("design", design_path), ("page", page_path),
                       ("metadata registration", registration_path)):
        _require(path.is_file(), f"the {name} is missing for {experiment!r}")
        _require_committed(root, _relative(root, path), name)
    design = json.loads(design_path.read_bytes().decode("utf-8"))
    _require(isinstance(design, Mapping) and design.get("schema") == DESIGN_SCHEMA,
             f"the design must be schema {DESIGN_SCHEMA!r}")
    page = page_path.read_text()
    embedded = _fenced_block(page, "phase67-design")
    _require(
        json.loads(embedded) == design,
        "the committed page's design block disagrees with the committed design",
    )
    registration = json.loads(registration_path.read_bytes().decode("utf-8"))
    _require(
        registration.get("design", {}).get("sha256")
        == _sha256_file(design_path),
        "the metadata registration's design digest is stale",
    )
    _require(
        registration.get("page", {}).get("sha256") == _sha256_file(page_path),
        "the metadata registration's page digest is stale",
    )
    verify_harness_freeze(root, phase)
    return {"design": design["experiment"], "problems": []}


def check_metadata(experiment, *, repo_root=None, phase_dir=None):
    """Audit the committed capture and its registered sources."""
    from pinn.verification.diagnostic_power import power_source

    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    admit_phase67_metadata_registration(
        phase / artifacts["metadata_registration"], repo_root=root
    )
    record_path, record, _sha = _committed_metadata_record(
        experiment, root=root, phase_dir=phase
    )
    directory = record_path.parent
    attempt_path = directory / "attempt.json"
    receipt_path = directory / "power-gate.json"
    for name, path in (("attempt", attempt_path), ("receipt", receipt_path)):
        _require(path.is_file(), f"the metadata {name} is missing")
        _require_committed(root, _relative(root, path), f"metadata {name}")
    attempt = json.loads(attempt_path.read_bytes().decode("utf-8"))
    _require(attempt.get("status") == "published",
             "the metadata attempt is not published")
    _require(
        attempt.get("record_sha256") == _sha256_file(record_path),
        "the metadata attempt's record digest disagrees with the record bytes",
    )
    receipt = json.loads(receipt_path.read_bytes().decode("utf-8"))
    _require(receipt.get("power_source") == "AC Power",
             "the metadata receipt does not record AC Power")
    _require(
        power_source(str(receipt.get("pmset_first_line", ""))) == "AC Power",
        "the metadata receipt's pmset first line does not name AC Power",
    )
    window = receipt.get("window")
    _require(
        isinstance(window, Mapping)
        and window.get("timezone") == "America/Chicago"
        and window.get("isoweekday") in (6, 7),
        "the metadata receipt's window is outside the owner's weekend window",
    )
    reads = (record.get("access") or {}).get("reads") or {}
    _require(
        isinstance(reads, Mapping) and reads.get("train", 0) >= 2,
        "the metadata record attests fewer than two TRAIN reads",
    )
    problems = []
    for orbit_key, block in record["orbits"].items():
        increments = block.get("max_adjacent_phase_increment_rad") or {}
        for harmonic, value in increments.items():
            _finite(value, f"the {harmonic} increment of {orbit_key!r}")
        for window_name, window_block in (block.get("windows") or {}).items():
            _require(
                isinstance(window_block, Mapping)
                and isinstance(window_block.get("physical_times_sha256"), str)
                and isinstance(window_block.get("baselines"), Mapping),
                f"the {window_name!r} window of {orbit_key!r} is malformed",
            )
    verify_harness_freeze(root, phase)
    if problems:
        raise Phase67CommandRefused("; ".join(problems))
    return {"experiment": experiment, "orbits": sorted(record["orbits"]),
            "problems": []}


def register_timing(experiment, *, repo_root=None, phase_dir=None,
                    provenance_registration=None, dependencies=None):
    """Write the exact timing matrix and every timing registration.

    Requires the committed metadata capture (whose window evidence binds
    every registration's metadata blocks) and the verified harness freeze;
    the EXP-04 timing registrations refuse unless the committed maximum
    adjacent harmonic-phase increment is strictly below pi.
    """
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    _record_path, metadata, metadata_sha = _committed_metadata_record(
        experiment, root=root, phase_dir=phase
    )
    if experiment == "exp04":
        for orbit_key, block in metadata["orbits"].items():
            increments = block.get("max_adjacent_phase_increment_rad") or {}
            worst = max(
                (float(value) for value in increments.values()), default=math.inf
            )
            _require(
                math.isfinite(worst) and worst < math.pi,
                f"the maximum adjacent harmonic-phase increment of {orbit_key!r} "
                f"({worst!r}) is not strictly below pi; EXP-04 timing refuses "
                "without retuning",
            )
    rows = phase67_run_matrix(
        experiment, "timing", metadata=metadata, metadata_sha=metadata_sha,
    )
    _write_matrix(
        experiment, "timing", rows, metadata_sha=metadata_sha,
        path=phase / artifacts["timing_matrix"],
    )
    _write_row_registrations(
        experiment, "timing", rows, root=root, phase_dir=phase,
        metadata=metadata, page_rel=artifacts["timing_page"],
        provenance_registration=provenance_registration,
        dependencies=dependencies,
    )
    return {"rows": len(rows), "matrix": artifacts["timing_matrix"]}


def check_matrix(experiment, kind, *, repo_root=None, phase_dir=None):
    """Verify the complete ordered row set and its committed registrations.

    The committed matrix must equal the exact current Cartesian product of
    the declared cases and arms; every registration must be committed clean
    and admit metadata-only through the fit door with settings agreeing
    with its row; the harness freeze must be current. No corpus is opened
    and no scientific value is printed.
    """
    from pinn.verification.diagnostic_fit import (
        DiagnosticFitRefused,
        check_fit_registration,
    )
    from pinn.verification.diagnostic_guard import DiagnosticRegistrationRefused

    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    path, matrix = _load_matrix(experiment, kind, phase_dir=phase)
    _require_committed(root, _relative(root, path), f"{kind} matrix")
    _record_path, metadata, metadata_sha = _committed_metadata_record(
        experiment, root=root, phase_dir=phase
    )
    science_steps = None
    if kind == "science":
        budget_path = phase / _budget_artifacts(experiment)["budget"]
        _require(budget_path.is_file(),
                 "the science matrix check requires the committed budget")
        _require_committed(root, _relative(root, budget_path), "budget")
        budget = json.loads(budget_path.read_bytes().decode("utf-8"))
        science_steps = int(budget["common_optimizer_steps"])
    expected = phase67_run_matrix(
        experiment, kind, metadata=metadata, metadata_sha=metadata_sha,
        science_steps=science_steps,
    )
    _require(matrix["rows"] == expected,
             "the committed matrix is not the exact current Cartesian "
             "product of the declared cases and arms")
    for row in expected:
        registration = phase / row["registration_path"]
        _require(registration.is_file(),
                 f"the row registration is missing: {row['registration_path']}")
        _require_committed(root, _relative(root, registration),
                           f"{kind} row registration")
        try:
            check_fit_registration(registration, repo_root=root)
        except (DiagnosticFitRefused, DiagnosticRegistrationRefused) as exc:
            raise Phase67CommandRefused(
                f"the registration of {row['case']}/{row['arm']} does not "
                f"admit: {exc}"
            ) from exc
        doc = json.loads(registration.read_bytes().decode("utf-8"))
        settings = doc["settings"]
        _require(
            settings["variant"]["name"] == row["variant_name"]
            and settings["orbit_key"] == row["orbit_key"]
            and settings["seed"] == row["seed"]
            and settings["physical_window"] == row["physical_window"]
            and settings["similarity_cadence"] == row["schedule"]["similarity_cadence"]
            and settings["score_cadence"] == row["schedule"]["score_cadence"]
            and settings["whole_run_cap_seconds"] == row["schedule"]["cap_seconds"],
            f"the registration of {row['case']}/{row['arm']} disagrees with "
            "its matrix row",
        )
    verify_harness_freeze(root, phase)
    return {"experiment": experiment, "kind": kind, "rows": len(expected),
            "problems": []}


def check_budget(experiment, *, repo_root=None, phase_dir=None):
    """Verify cost provenance, arithmetic, pages, matrices and chronology."""
    root = _repo_root(repo_root)
    phase = _phase_directory(phase_dir, root)
    artifacts = _budget_artifacts(experiment)
    budget_path = phase / artifacts["budget"]
    _require(budget_path.is_file(), "the budget is missing")
    _require_committed(root, _relative(root, budget_path), "budget")
    budget = json.loads(budget_path.read_bytes().decode("utf-8"))
    _require(budget.get("schema") == BUDGET_SCHEMA,
             f"the budget must be schema {BUDGET_SCHEMA!r}")
    _matrix, entries, identities = _collect_timing_rows(
        experiment, root=root, phase_dir=phase
    )
    recomputed = phase67_budget(
        phase67_cost_rows(entries), expected_identities=identities,
    )
    for key in recomputed:
        _require(
            budget.get(key) == recomputed[key],
            f"the committed budget's {key} disagrees with the recomputation "
            "from the committed timing rows",
        )
    steps = int(budget["common_optimizer_steps"])
    for name in ("budget_page", "prediction_page", "science_matrix"):
        path = phase / artifacts[name]
        _require(path.is_file(), f"the budget's {name} is missing")
        _require_committed(root, _relative(root, path), f"budget {name}")
    budget_page_text = (phase / artifacts["budget_page"]).read_text()
    prediction_text = (phase / artifacts["prediction_page"]).read_text()
    for page in (budget_page_text, prediction_text):
        for number in (steps, budget["warmup_steps"],
                       budget["whole_run_cap_seconds"]):
            _require(_has_number(page, number),
                     f"a budget page omits the frozen number {number!r}")
    for entry in budget["timing_evidence"]["rows"]:
        _require(
            _sha256_file(root / entry["path"]) == entry["sha256"],
            f"the budget's timing-evidence digest is stale: {entry['path']}",
        )
    _path, science_matrix = _load_matrix(experiment, "science", phase_dir=phase)
    _require(
        science_matrix["rows"] and all(
            row["schedule"]["optimizer_steps"] == steps
            for row in science_matrix["rows"]
        ),
        "the science matrix is not frozen at the budget's common step count",
    )
    budget_commit = _introducing_commit(root, _relative(root, budget_path))
    for row in _matrix["rows"]:
        record_commit = _introducing_commit(
            root, _relative(root, phase / row["output_path"])
        )
        _require(
            record_commit is not None and budget_commit is not None
            and _git(root, "merge-base", "--is-ancestor", record_commit,
                     budget_commit).returncode == 0,
            f"the timing record of {row['case']}/{row['arm']} was not "
            "committed before the budget",
        )
    verify_harness_freeze(root, phase)
    return {"steps": steps, "problems": []}
