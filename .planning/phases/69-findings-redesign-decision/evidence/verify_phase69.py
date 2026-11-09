"""Check Phase 69 evidence without training, rescoring or dataset access."""

import argparse
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]
PHASE = ".planning/phases/69-findings-redesign-decision"
INVENTORY = ROOT / PHASE / "evidence/69-evidence.json"
BASELINE = "0f91709000a442507e0eb2b9616f474a81525333"
OLD_CODE = "a686d26e00f7c1e8ba54bb2d3e1cd730a3404a69"
P60 = ".planning/phases/60-single-system-learnability"
P65 = ".planning/phases/65-probe-on-the-record-fit-harness"
P66 = ".planning/phases/66-small-network-control"
P67 = ".planning/phases/67-design-settings-ladders"
P68 = ".planning/phases/68-yardstick"
# The v2.5 close archived the live requirements and roadmap; check the v2.5 archives.
REQUIREMENTS_REL = ".planning/milestones/v2.5-REQUIREMENTS.md"
ROADMAP_REL = ".planning/milestones/v2.5-ROADMAP.md"
CASES = {
    "main-1632-s42": (1632, 42, "main"),
    "repeat-851-s42": (851, 42, "repeat-system"),
    "repeat-1632-s41": (1632, 41, "repeat-seed"),
}
CONTROL_PUBLICATIONS = {
    "main-1632-s42": "df40671e2e07a95b65efc102cabc59e22ca8dc59",
    "repeat-851-s42": "23df087ccb13dfb3123809024dcd554e24c5b954",
    "repeat-1632-s41": "623f8df6641eebdbbfdda811e4f13c3002b1c14f",
}
CODE_PATHS = {
    "pinn/network.py", "pinn/architecture_spec.py", "pinn/data/preprocessing.py",
    "pinn/verification/production_reference.py", "pinn/verification/learnability_data.py",
    "pinn/verification/learnability_losses.py", "pinn/verification/learnability_run.py",
    "pinn/loss_catalog.py", "pinn/verification/diagnostic_variants.py",
    "pinn/verification/diagnostic_data.py", "pinn/verification/diagnostic_fit.py",
}


class VerifyError(RuntimeError):
    """Missing, conflicting or altered evidence cannot pass verification."""


def fail(message):
    raise VerifyError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def evidence_path(path):
    """Allow named evidence/code files, never corpus files or weight loading."""
    supplied = PurePosixPath(path)
    if supplied.is_absolute() or ".." in supplied.parts or str(supplied) != path:
        fail(f"source path escapes or is not repository-relative: {path!r}")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        fail(f"source path escapes the repository: {path!r}")
    prefixes = (P60 + "/", P65 + "/", P66 + "/", P67 + "/", P68 + "/")
    if not (path.startswith(prefixes) or path in CODE_PATHS) or supplied.suffix not in (".json", ".md", ".py", ".txt"):
        fail(f"source path is outside named evidence/code: {path!r}")
    return path


def git_bytes(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        fail(f"committed object unavailable: {' '.join(args)}")
    return result.stdout


def read_source(path, revision, digest=None):
    evidence_path(path)
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        fail(f"source revision must be a full commit ID: {revision!r}")
    data = git_bytes("show", f"{revision}:{path}")
    if digest is not None and sha256(data) != digest:
        fail(f"source digest differs: {path}@{revision}")
    return data


class Sources:
    def __init__(self):
        self.raw = {}

    def read(self, path, revision=BASELINE, digest=None):
        key = (path, revision)
        if key not in self.raw:
            self.raw[key] = read_source(path, revision)
        data = self.raw[key]
        if digest is not None and sha256(data) != digest:
            fail(f"source digest differs: {path}@{revision}")
        return data

    def json(self, path, revision=BASELINE, digest=None, *, decimals=False):
        try:
            return json.loads(self.read(path, revision, digest), parse_float=Decimal if decimals else float)
        except (ValueError, UnicodeError) as exc:
            fail(f"unreadable source JSON: {path}: {exc}")

    def rows(self):
        return [
            {"path": path, "revision": revision, "sha256": sha256(data)}
            for (path, revision), data in sorted(self.raw.items())
        ]

    def publication(self, path):
        evidence_path(path)
        revision = git_bytes("log", "-1", "--diff-filter=A", "--format=%H", BASELINE, "--", path).decode().strip()
        if not revision:
            fail(f"source has no publication commit: {path}")
        return revision


def tracked_paths(*prefixes):
    return git_bytes("ls-tree", "-r", "--name-only", BASELINE, "--", *prefixes).decode().splitlines()


def publication_registration(record, publication, sources):
    reference = record["registration"]
    return sources.json(reference["path"], publication, reference["sha256"])


def metric_route(score):
    return {key: score[key] for key in ("grid", "frame", "velocity_source")}


def matched_comparison(case, old, control, review, sources):
    if case not in CASES:
        fail(f"unknown case: {case}")
    system, seed, role = CASES[case]
    if old["system_id"] != system or old["seed"] != seed or control["seed"] != seed:
        fail(f"case/system/seed mismatch: {case}")
    if control["orbit"]["train"]["record_key"].split("/")[-1] != str(system):
        fail(f"case/record system mismatch: {case}")
    if old["code"]["git_head"] != OLD_CODE:
        fail(f"historical implementation revision differs: {case}")
    score = control["scores"]["network"]
    observed = review["contrasts"]["lr1e-3"]["cases"][role]
    if observed["observed_fit"]["control"] != {"E": score["E"], "tier": score["tier"]}:
        fail(f"review/endpoint mismatch: {case}")
    publication = CONTROL_PUBLICATIONS[case]
    publication_registration(control, publication, sources)
    current_registration = sources.read(control["registration"]["path"])
    return {
        "system": system, "seed": seed, "case": case,
        "historical": {
            "arm": old["arm_id"], "record": f"{P60}/evidence/arms/{old['arm_id']}/record.json",
            "execution_revision": old["code"]["git_head"],
            "adam_E": old["states"]["adam"]["score_gold"]["E"],
            "polish_E": old["states"]["polish"]["score_gold"]["E"],
            "official_E": old["result"]["E"], "tier": old["result"]["tier"],
            "state": old["better_state"],
            "metric_route": metric_route(old["states"][old["better_state"]]["score_gold"]),
        },
        "control": {
            "experiment": "exp03", "case": case, "system": system, "seed": seed,
            "arm": "lr1e-4", "state": "registered-endpoint", "E": score["E"],
            "tier": score["tier"], "settled": observed["endpoint_status"]["control"] == "settled",
            "endpoint_status": observed["endpoint_status"]["control"],
            "metric_route": metric_route(score),
            "record": f"{P67}/evidence/exp03/science/{case}/lr1e-4/record.json",
            "prediction": f"{P67}/67-EXP03-PREDICTION.md",
            "review": f"{P67}/evidence/exp03/review.json",
            "publication_revision": publication,
            "captured_registration_sha256": control["registration"]["sha256"],
            "current_registration_sha256": sha256(current_registration),
            "current_registration_matches_capture": sha256(current_registration) == control["registration"]["sha256"],
        },
    }


def index_cases(rows):
    """Keep equal-valued cases distinct and reject duplicate identities."""
    indexed = {}
    for row in rows:
        if row["case"] not in CASES:
            fail(f"unknown case identity: {row['case']}")
        key = (row["experiment"], row["case"], row["system"], row["seed"],
               row["arm"], json.dumps(row["window"], sort_keys=True), row["state"],
               json.dumps(row["metric_route"], sort_keys=True))
        if key in indexed:
            fail(f"duplicate/conflicting case identity: {key}")
        system, seed, role = CASES[row["case"]]
        if (row["system"], row["seed"], row["role"]) != (system, seed, role):
            fail(f"case identity mismatch: {row['case']}")
        indexed[key] = row
    return indexed


def fit_row(sources, path, experiment, case, arm):
    record = sources.json(path)
    system, seed, role = CASES[case]
    if record["seed"] != seed or record["orbit"]["train"]["record_key"].split("/")[-1] != str(system):
        fail(f"record/case mismatch: {path}")
    publication = sources.publication(path)
    registration = publication_registration(record, publication, sources)
    settings = registration["settings"]
    if settings["seed"] != seed or settings["orbit_key"] != record["orbit"]["train"]["record_key"]:
        fail(f"registration/case mismatch: {path}")
    if settings["variant"]["name"] != record["variant"]["name"]:
        fail(f"registration/arm mismatch: {path}")
    window = record["orbit"]["window"]
    bounds = settings["physical_window"]
    if (window["configured_length"] != settings["variant"]["window_length"]
            or not bounds["t_start"] <= window["t_start"] <= window["t_end"] <= bounds["t_end"]):
        fail(f"registration/window mismatch: {path}")
    if experiment != "exp01":
        expected = {"experiment": experiment, "case": case, "arm": arm, "kind": "science"}
        if any(registration["phase67_row"][key] != value for key, value in expected.items()):
            fail(f"registration row identity mismatch: {path}")
    sources.read(registration["page"]["path"], publication, registration["page"]["sha256"])
    score = record["scores"]["network"]
    route = metric_route(score)
    if route != {"grid": "gold", "frame": "r_prime_u", "velocity_source": "autograd"}:
        fail(f"unexpected diagnostic metric route: {path}")
    if "score_checkpoints" in record and record["score_checkpoints"][-1]["score"] != score:
        fail(f"recorded endpoint score differs: {path}")
    return {
        "experiment": experiment, "case": case, "system": system, "seed": seed,
        "role": role, "arm": arm, "state": "registered-endpoint", "score": score,
        "metric_route": route, "window": window,
        "record": path, "publication_revision": publication,
        "registration": record["registration"], "prediction": registration["page"]["path"],
        "variant": record["variant"], "steps": record["steps"],
        "comparison_scores": record["comparisons"],
        "score_checkpoints": record.get("score_checkpoints"),
        "similarity_reference": path + "#/similarity/entries",
    }


def recipe_comparison(sources, old_records, controls):
    """Describe the recorded recipes; no factor is assigned causal priority."""
    main = controls["main-1632-s42"]
    shared = old_records[1632]["module_sha256"]
    for old in old_records.values():
        if old["module_sha256"] != shared:
            fail("historical module maps disagree")
    for control in controls.values():
        if control["source_sha256"] != shared:
            fail("historical/control frozen module maps disagree")
    # Read implementation at the recorded historical/publication revisions.
    code_paths = ("pinn/network.py", "pinn/architecture_spec.py", "pinn/data/preprocessing.py",
                  "pinn/verification/production_reference.py", "pinn/verification/learnability_data.py",
                  "pinn/verification/learnability_losses.py", "pinn/verification/learnability_run.py",
                  "pinn/loss_catalog.py")
    for path in code_paths:
        sources.read(path, OLD_CODE, shared[path])
        sources.read(path, CONTROL_PUBLICATIONS["main-1632-s42"], shared[path])
    for path in ("pinn/verification/diagnostic_variants.py", "pinn/verification/diagnostic_data.py",
                 "pinn/verification/diagnostic_fit.py"):
        sources.read(path, CONTROL_PUBLICATIONS["main-1632-s42"])
    pins = {}
    for system, old in old_records.items():
        control = controls["main-1632-s42" if system == 1632 else "repeat-851-s42"]
        for route in ("train", "score"):
            if old["records"][route]["windowed_sha256"] != control["orbit"][route]["windowed_sha256"]:
                fail(f"actual {system} {route} window digests differ")
            if old["records"][route]["n_within_t"] != control["orbit"][route]["n_within_window"]:
                fail(f"actual {system} {route} sample counts differ")
        pins[str(system)] = {
            "window_sha256": old["records"]["train"]["windowed_sha256"],
            "samples": old["records"]["train"]["n_within_t"],
        }
    references = [f"{P60}/evidence/arms/r1-{system}/record.json" for system in old_records]
    references += [f"{P67}/evidence/exp03/science/{case}/lr1e-4/record.json" for case in controls]

    def aspect(name, status, facts, citations):
        return {"aspect": name, "status": status, "facts": facts, "citations": citations}

    old_main = old_records[1632]
    pub = CONTROL_PUBLICATIONS["main-1632-s42"]
    code = lambda path, anchor: f"{path}@{anchor}"
    return {
        "scope": "retrospective recipe comparison; no isolated historical cause, physics success or generalization",
        "module_sha256": shared, "module_count": len(shared),
        "statistics_sha256": old_main["normalizer"]["stats_sha256"], "matched_windows": pins,
        "aspects": [
            aspect("architecture", "checked-equivalent",
                   {key: main["variant"][key] for key in ("depth", "width", "first_omega_0", "hidden_omega_0", "time_features")},
                   references + [code("pinn/network.py", OLD_CODE), code("pinn/architecture_spec.py", pub)]),
            aspect("initialization construction", "checked-equivalent",
                   "Same production class, seeded construction and nominal seed 42; new builder uses a local generator.",
                   [code("pinn/verification/learnability_run.py:321-331", OLD_CODE),
                    code("pinn/verification/diagnostic_variants.py:245-274", pub)]),
            aspect("archived initial tensors", "source-unresolved",
                   "Same-seed construction does not prove archived initial-tensor identity.", references),
            aspect("input and targets", "checked-equivalent",
                   "raw_tau_ic13; globally fixed characteristic time; residency-cast float32 times; identical target/time window hashes",
                   references + [code("pinn/verification/learnability_data.py:256-275", OLD_CODE),
                                 code("pinn/verification/diagnostic_data.py:543-563", pub)]),
            aspect("body order, gauge and normalization", "checked-equivalent",
                   "Unchanged production preprocessing/reference/residency sources, ordered raw masses, same required statistics digest; recovery versus rehydration is operational.",
                   references + [code("pinn/verification/learnability_data.py:123-165", OLD_CODE),
                                 code("pinn/verification/diagnostic_data.py:324-427", pub)]),
            aspect("grid, window and samples", "checked-equivalent", pins,
                   references + [code("pinn/verification/learnability_data.py:183-194", OLD_CODE),
                                 code("pinn/verification/diagnostic_data.py:446-459", pub)]),
            aspect("window boundary implementation", "checked-different",
                   "Historical upper bound uses 1e-9 tolerance; diagnostic mask uses exact 0 <= t <= window. Actual gold samples agree.",
                   [code("pinn/verification/learnability_data.py:183-194", OLD_CODE),
                    code("pinn/verification/diagnostic_data.py:446-459", pub)]),
            aspect("loss and reduction", "checked-equivalent",
                   "Same data_only_loss and Huber implementation, sum(Huber)/(9*N_t); every retained point on every update; no physics term.",
                   [code("pinn/verification/learnability_losses.py:479-491", OLD_CODE),
                    code("pinn/loss_catalog.py:260-276", pub)]),
            aspect("Adam and schedule", "checked-different", {
                "historical": {str(k): v["schedule"] for k, v in old_records.items()},
                "diagnostic": main["optimizer"],
            }, references),
            aspect("clipping and diagnostic polish", "checked-different", {
                "historical_clipping": {str(k): v["clip"] for k, v in old_records.items()},
                "historical_polish_calls": {str(k): v["states"]["polish"]["outer_calls"] for k, v in old_records.items()},
                "diagnostic_clipping": None, "diagnostic_polish": main["optimizer"]["polish"],
                "limit": "Executed Phase 60 diagnostic polish is distinct from the unreachable production L-BFGS stage.",
            }, references + [main["registration"]["path"] + "@" + pub]),
            aspect("precision and device", "checked-equivalent", {
                "historical": {str(k): v["runtime"] for k, v in old_records.items()},
                "diagnostic": main["runtime"],
            }, references),
            aspect("historical runtime, kernels and determinism", "source-unresolved",
                   "Recorded MPS/float32 does not establish exact historical kernel or determinism state.", references),
            aspect("update budget", "checked-different", {
                "historical": {str(k): v["budget"]["budget_steps"] for k, v in old_records.items()},
                "diagnostic": {case: v["steps"] for case, v in controls.items()},
            }, references),
            aspect("scored-state selection", "checked-different", {
                "historical": {str(k): v["better_state"] for k, v in old_records.items()},
                "diagnostic": "registered endpoint, not best intermediate checkpoint; gold/r_prime_u/autograd",
            }, references + [code("pinn/verification/diagnostic_fit.py:1098-1108", pub)]),
        ],
    }


def owner_quote(text):
    blocks = re.findall(r"```owner-quote\n(.*?)\n```", text, re.S)
    if len(blocks) != 1 or not blocks[0].strip():
        fail("owner ruling requires its one recorded nonempty quotation")
    return blocks[0]


def duration(value, what):
    if value is None:
        return None
    if isinstance(value, bool):
        fail(f"invalid duration: {what}")
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        fail(f"invalid duration: {what}")
    if not number.is_finite() or number < 0:
        fail(f"invalid or negative duration: {what}")
    return number


def utc_interval(start, end):
    try:
        left, right = (datetime.fromisoformat(value) if value is not None else None for value in (start, end))
    except (TypeError, ValueError):
        fail("invalid UTC timestamps")
    if any(time.utcoffset() is None or time.utcoffset().total_seconds() != 0
           for time in (left, right) if time is not None):
        fail("timestamps must explicitly use UTC")
    if left is None or right is None:
        return None
    delta = right - left
    seconds = Decimal(delta.days * 86400 + delta.seconds) + Decimal(delta.microseconds) / 1000000
    return duration(seconds, "UTC interval")


def summarize_activities(rows):
    """Repeated references count once; different attempts cannot share an identity."""
    by_path, by_identity = {}, {}
    for row in rows:
        path = row["attempt"]
        identity = (row["registration"]["path"], row["registration"]["sha256"], row["run_id"])
        if path in by_path:
            if row != by_path[path]:
                fail(f"conflicting duplicate attempt: {path}")
            continue
        if identity in by_identity:
            fail(f"duplicate attempt identity at different paths: {path}")
        by_path[path], by_identity[identity] = row, path
    subtotals = {}
    for row in by_path.values():
        path = row["attempt"]
        activity = row["activity"]
        totals = subtotals.setdefault(activity, {"attempts": 0, "published_attempts": 0,
                                               "timed_attempts": 0, "utc_seconds": Decimal(0),
                                               "fit_wall_records": 0, "fit_wall_seconds": Decimal(0),
                                               "unknown_utc_attempts": 0})
        totals["attempts"] += 1
        totals["published_attempts"] += row["status"] == "published"
        utc = duration(row["utc_seconds"], path)
        fit = duration(row["fit_wall_seconds"], path)
        if utc is None:
            totals["unknown_utc_attempts"] += 1
        else:
            totals["timed_attempts"] += 1
            totals["utc_seconds"] += utc
        if fit is not None:
            totals["fit_wall_records"] += 1
            totals["fit_wall_seconds"] += fit
    fields = ("attempts", "published_attempts", "timed_attempts", "utc_seconds", "fit_wall_records", "fit_wall_seconds", "unknown_utc_attempts")
    total = {key: sum((row[key] for row in subtotals.values()), Decimal(0) if key.endswith("seconds") else 0) for key in fields}
    # The historical probe claim is an outcome-linked probe, not a failed fit.
    attempt_totals = {key: total[key] - subtotals.get("phase65-probe", {}).get(key, 0) for key in fields}
    for row in [*subtotals.values(), total, attempt_totals]:
        row["utc_seconds"] = str(row["utc_seconds"]) if row["timed_attempts"] else None
        row["fit_wall_seconds"] = str(row["fit_wall_seconds"]) if row["fit_wall_records"] else None
    return {**attempt_totals, "activity_subtotals": dict(sorted(subtotals.items())),
            "unique_activity_records": len(by_path), "unknown_probe_activities": subtotals.get("phase65-probe", {}).get("attempts", 0)}


def build_cost():
    sources = Sources()
    paths = tracked_paths(f"{P65}/evidence", f"{P66}/evidence", f"{P67}/evidence")
    tracked = set(paths)
    rows = []
    for path in paths:
        if not path.endswith("/attempt.json"):
            continue
        attempt = sources.json(path)
        unknown_reason = None
        if path.startswith(P65) and "/probe/" in path:
            record_path = attempt["result_path"]
            record = sources.json(record_path)
            activity = "phase65-probe"
            unknown_reason = "Probe publication has no timed attempt interval; incomplete is a claim, not a separate failed fit."
        else:
            if attempt.get("output", "record.json") != "record.json":
                fail(f"attempt output is not its local record: {path}")
            record_path = str(PurePosixPath(path).with_name("record.json"))
            if record_path in tracked:
                record = sources.json(record_path, digest=attempt.get("record_sha256"), decimals=True)
            elif attempt["status"] in {"incomplete", "failed"} and attempt.get("record_sha256") is None:
                record_path = None
                record = {}
                unknown_reason = "No result was published. Unrecorded duration fields remain unknown."
            else:
                fail(f"attempt is missing its required result: {path}")
            if record.get("registration") is not None and record["registration"] != attempt["registration"]:
                fail(f"attempt/record registration mismatch: {path}")
            if path.startswith(P65):
                activity = "phase65-smoke"
            elif path.startswith(P66):
                activity = "phase66-timing" if "/timing/" in path else "phase66-science"
            else:
                activity = "phase67-" + ("metadata" if "/metadata/" in path else "timing" if "/timing/" in path else "science")
        utc = utc_interval(attempt.get("started_utc"), attempt.get("ended_utc"))
        fit = duration(record.get("timing", {}).get("total_wall_seconds"), path)
        rows.append({
            "attempt": path, "record": record_path, "activity": activity,
            "registration": attempt["registration"], "run_id": record.get("run_id", record_path or path),
            "status": attempt["status"], "record_status": record.get("status"),
            "started_utc": attempt.get("started_utc"), "ended_utc": attempt.get("ended_utc"),
            "utc_seconds": None if utc is None else str(utc),
            "fit_wall_seconds": None if fit is None else str(fit),
            "unknown_reason": unknown_reason,
            "below_timestamp_resolution": utc == 0 if utc is not None else None,
        })
    summary = summarize_activities(rows)
    yard_path = f"{P68}/evidence/yardstick-audit.json"
    yard = sources.json(yard_path, decimals=True)["provenance"]
    yard_utc = utc_interval(yard["utc_started"], yard["utc_finished"])
    yard_elapsed = duration(yard["elapsed_seconds"], "yardstick capture elapsed_seconds")
    yardstick = {"activity": "phase68-yardstick-capture", "record": yard_path,
                "utc_started": yard["utc_started"], "utc_finished": yard["utc_finished"],
                "utc_seconds": str(yard_utc), "elapsed_seconds": str(yard_elapsed),
                "basis": "One recorded audit capture; UTC interval and elapsed_seconds are alternative views of this same activity."}
    unknowns = [
        {"activity": "phase65-receipt-admission-refusal", "duration_seconds": None, "training_attempt_created": False, "source": f"{P65}/65-06-SUMMARY.md:154-164"},
        {"activity": "phase67-battery-gate-refusal", "duration_seconds": None, "training_attempt_created": False, "source": f"{P67}/67-08-SUMMARY.md:203"},
        {"activity": "phase67-exp05-post-receipt-pre-attempt-variant-refusal", "duration_seconds": None, "training_attempt_created": False, "source": f"{P67}/67-14-SUMMARY.md:136-157"},
        {"activity": "development/tests/operator time and unrecorded activity", "duration_seconds": None, "source": "not measured by these attempt or capture records"},
    ]
    for path in (f"{P65}/65-06-SUMMARY.md", f"{P65}/65-CLOSEOUT.md", f"{P67}/67-08-SUMMARY.md", f"{P67}/67-14-SUMMARY.md"):
        sources.read(path)
    return {
        "summary": summary, "activities": rows, "yardstick_capture": yardstick,
        "named_activity_utc_subtotal": {"timed_activities": summary["timed_attempts"] + 1,
                                       "utc_seconds": str(Decimal(summary["utc_seconds"] or "0") + yard_utc)},
        "unknown_costs": unknowns,
        "coverage": "Recorded Phase 65-67 attempts plus one Phase 68 capture; not all Mac use. Attempt UTC timestamps have one-second resolution, including below-resolution zero intervals.",
        "non_additive_views": "Fit-wall and UTC intervals are alternatives; optimizer/logging/scoring segments are inside fit walls. Yardstick elapsed and UTC views are alternatives.",
        "excluded_context": "v2.4 costs remain outside every v2.5 subtotal",
        "source_rows": sources.rows(),
    }


def build_sources():
    sources = Sources()
    old_records = {system: sources.json(f"{P60}/evidence/arms/r1-{system}/record.json") for system in (1632, 851)}
    controls = {case: sources.json(f"{P67}/evidence/exp03/science/{case}/lr1e-4/record.json") for case in CASES}
    reviews = {exp: sources.json(f"{P67}/evidence/{exp}/review.json") for exp in ("exp02", "exp03", "exp04", "exp05")}
    comparisons = [matched_comparison(case, old_records[system], controls[case], reviews["exp03"], sources)
                   for case, (system, seed, _role) in CASES.items() if seed == 42]
    probe = sources.json(f"{P65}/evidence/probe/reproduction.json")
    sources.read(probe["registration"]["path"], probe["run_commit"], probe["registration"]["sha256"])
    experiments = {"DIAG-09": {
        "prediction": f"{P65}/65-PROBE-PREDICTION.md", "record": f"{P65}/evidence/probe/reproduction.json",
        "reading": probe["reading_rule"],
        "new_measurement_entries": len(probe["new_measurements"]),
        "historical_summary_defect": "reading_rule.new_measurements is zero while 130 top-level entries exist; preserved under 65-CLOSEOUT.md",
        "limit": "Reproduction of already-seen association; CPU64 initialization reconstruction differs from historical MPS32 initial state. Causality remains open.",
    }}
    result66 = sources.read(f"{P66}/66-RESULT.md").decode()
    match = re.search(r"EXP01-REVIEW confirmation=([\w-]+) route=([\w.-]+)", result66)
    if not match:
        fail("EXP-01 recorded review line absent")
    rows66 = [fit_row(sources, f"{P66}/evidence/exp01/{case}/record.json", "exp01", case, "exp01-d1-w384-o1000") for case in CASES]
    index_cases(rows66)
    experiments["EXP-01"] = {
        "prediction": f"{P66}/66-PREDICTION.md", "review": f"{P66}/66-RESULT.md",
        "confirmation": match[1], "route": match[2], "arms": rows66,
        "limit": "One-orbit data-only supervised position fits; depth, width and first frequency changed together. No physics or new-IC generalization claim.",
    }
    paths = tracked_paths(f"{P67}/evidence")
    for exp, review in reviews.items():
        prediction = f"{P67}/67-{exp.upper()}-PREDICTION.md"
        sources.read(prediction)
        design = sources.json(f"{P67}/evidence/{exp}/design.json")
        rows = []
        for path in paths:
            if path.startswith(f"{P67}/evidence/{exp}/science/") and path.endswith("/record.json"):
                _prefix, case, arm, _filename = path.rsplit("/", 3)
                rows.append(fit_row(sources, path, exp, case, arm))
        index_cases(rows)
        lookup = {(row["case"], row["arm"]): row for row in rows}
        if len(lookup) != len(rows):
            fail(f"review has multiple scored rows for one case and arm: {exp}")
        contrasts = {}
        for arm, contrast in review["contrasts"].items():
            cases = {}
            for case, (_system, _seed, role) in CASES.items():
                cell = contrast["cases"][role]
                for side, named_arm in (("arm", arm), ("control", contrast["control"])):
                    row = lookup[(case, named_arm)]
                    expected = {"E": row["score"]["E"], "tier": row["score"]["tier"]}
                    if cell["observed_fit"][side] != expected:
                        fail(f"review case/arm score mismatch: {exp}/{case}/{named_arm}")
                    status = cell["endpoint_status"][side]
                    if "endpoint_status" in row and row["endpoint_status"] != status:
                        fail(f"conflicting endpoint labels: {exp}/{case}/{named_arm}")
                    row["endpoint_status"] = status
                cases[case] = cell
            contrasts[arm] = {key: contrast[key] for key in ("arm", "control", "confirmation", "reasons", "scope_disposition")}
            contrasts[arm]["cases"] = cases
        experiments[exp.upper().replace("EXP", "EXP-")] = {
            "prediction": prediction, "review": f"{P67}/evidence/{exp}/review.json",
            "hypothesis": design["hypothesis"], "confounds": design["confounds"],
            "prediction_table": design["prediction_table"], "reading_rule": design["reading_rule"],
            "predictions_comparison": review["predictions_comparison"],
            "confirmed": review["confirmation"]["confirmed"], "unconfirmed": review["confirmation"]["unconfirmed"],
            "contrasts": contrasts, "arms": rows, "budget_steps": review["budget_steps"],
            "scope49_disposition": review["scope49_disposition"], "proposed_change": review["proposed_change"],
            "dependent_launch_allowed": review["dependent_launch_allowed"],
            "limit": "Registered three-case rule; unsettled and ambiguous results remain unconfirmed; no arm continuation.",
        }
    yardstick = sources.json(f"{P68}/evidence/yardstick-audit.json")
    ruling68 = sources.read(f"{P68}/68-CHECKPOINT-2-RULING.md").decode()
    experiments["YARD-01"] = {
        "record": f"{P68}/evidence/yardstick-audit.json", "rows": yardstick["rows"],
        "aggregates": yardstick["aggregates"], "coverage": yardstick["coverage"],
        "limit": "Finite-difference measurement defect; energy conservation alone does not establish position accuracy or explain a data-only fitting failure.",
    }
    experiments["YARD-02"] = {"ruling": f"{P68}/68-CHECKPOINT-2-RULING.md", "owner_words_verbatim": owner_quote(ruling68), "C-7": "A; autograd amendment routed to v2.6"}
    experiments["YARD-03"] = {"ruling": f"{P68}/68-CHECKPOINT-2-RULING.md", "owner_words_verbatim": owner_quote(ruling68), "open": ["C-2", "C-4", "C-5", "C-6"], "C-11": "evaluation-text rewrite routed to v2.6"}
    ruling66 = sources.read(f"{P66}/66-CHECKPOINT-1-RULING.md").decode()
    if sha256(sources.read(f"{P66}/66-RESULT.md")) not in ruling66:
        fail("EXP-01 ruling does not bind the result digest")
    ruling67 = sources.json(f"{P67}/67-EXP03-RULING.md")
    for entry in ruling67["reviewed_artifacts"].values():
        sources.read(entry["path"], BASELINE, entry["sha256"])
    if ruling67["proposal"] != reviews["exp03"]["proposed_change"] or sha256(json.dumps(ruling67["proposal"], sort_keys=True).encode()) != ruling67["proposal_sha256"]:
        fail("EXP-03 proposal digest differs")
    index = sources.json(f"{P67}/67-EVIDENCE-INDEX.json")
    dispositions = [
        {"event": "DIAG-09", "proposal": False, "disposition": "retained; no pivot", "authority": f"{P65}/65-FINDINGS.md"},
        {"event": "EXP-01", "disposition": match[2], "owner_words_verbatim": owner_quote(ruling66), "authority": f"{P66}/66-CHECKPOINT-1-RULING.md"},
    ]
    dispositions += [{"event": exp.upper().replace("EXP", "EXP-"), **{key: review[key] for key in ("scope49_disposition", "proposed_change", "dependent_launch_allowed")}, "audit_disposition": index["experiments"][exp]["scope"], "authority": f"{P67}/evidence/{exp}/review.json"} for exp, review in reviews.items()]
    dispositions.append({"event": "EXP-03 owner continuation", "ruling": ruling67, "authority": f"{P67}/67-EXP03-RULING.md", "amendment": False})
    resources = []
    for revision in ("73bcbc748e74e0a563f1730348d53955fe92b054", "179efd809193d3980776ed4dc04bd6aa58e6f71e", "88d17045167c960f2981187b7444725fe32715a2"):
        message = git_bytes("show", "-s", "--format=%B", revision).decode()
        resources.append({"revision": revision, "commit_message": message, "message_sha256": sha256(message.encode()), "kind": "historical resource window ruling; no Phase 69 run authorization"})
    for path in (f"{P65}/65-PROBE-PREDICTION.md", f"{P65}/65-FINDINGS.md", f"{P65}/65-CLOSEOUT.md",
                 f"{P66}/66-PREDICTION.md", f"{P67}/67-CLOSEOUT.md", f"{P67}/67-FINDINGS.md", f"{P68}/68-AUDIT.md"):
        sources.read(path)
    recipe = recipe_comparison(sources, old_records, controls)
    return {
        "baseline_revision": BASELINE, "source_rows": sources.rows(),
        "matched_comparisons": comparisons,
        "additional_control": next(row for row in experiments["EXP-03"]["arms"]
                                   if row["case"] == "repeat-1632-s41" and row["arm"] == "lr1e-4"),
        "additional_control_limit": "1632/41 is a second seed on the main system, with no matched historical run here; it is not a second physical system.",
        "experiments": experiments, "recipe": recipe, "dispositions": dispositions,
        "resource_rulings": resources,
        "historical_narrative_discrepancy": {
            "source": f"{P67}/67-FINDINGS.md:139-154,193-205",
            "issue": "Historical narrative swaps repeat columns; raw keyed reviews are retained here and historical page remains unchanged.",
            "correct_lr1e-3_effects": {case: reviews["exp03"]["contrasts"]["lr1e-3"]["cases"][role]["relative_E_effect"] for case, (_system, _seed, role) in CASES.items()},
        },
    }


def unique_json_object(pairs):
    values = {}
    for key, value in pairs:
        if key in values:
            fail(f"duplicate inventory JSON key: {key!r}")
        values[key] = value
    return values


def load_inventory():
    try:
        return json.loads(INVENTORY.read_bytes(), object_pairs_hook=unique_json_object)
    except (OSError, ValueError) as exc:
        fail(f"unreadable Phase 69 inventory: {exc}")


def markdown_section(text, title_pattern, level=2):
    matches = list(re.finditer(r"^" + "#" * level + r" " + title_pattern + r"[ \t]*$", text, re.M))
    if len(matches) != 1:
        fail(f"expected one {title_pattern} section, found {len(matches)}")
    start = matches[0].end()
    following = re.search(r"^#{1," + str(level) + r"} ", text[start:], re.M)
    return text[start:start + following.start()] if following else text[start:]


def active_markdown(text):
    """Keep rendered lines, excluding backtick and tilde fenced examples."""
    visible = []
    opener = None
    for line in text.splitlines():
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opener is not None:
            if fence and fence[1][0] == opener[0] and len(fence[1]) >= len(opener) and not fence[2].strip():
                opener = None
        elif fence:
            opener = fence[1]
        else:
            visible.append(line)
    return "\n".join(visible)


def traceability_report(requirements_text, roadmap_text, phase_exists):
    """Check active mappings independently of completion and row order."""
    requirements = active_markdown(requirements_text)
    roadmap = active_markdown(roadmap_text)
    active = re.match(r"# Requirements: (v\d+\.\d+)\b", requirements)
    if not active:
        fail("active requirements milestone title is missing")
    milestone = active[1]
    if milestone != "v2.5":
        fail(f"Phase 69 checks v2.5 traceability, found {milestone}")
    # A later top-level archive title cannot contribute active definitions/rows.
    tail = re.search(r"^# ", requirements[active.end():], re.M)
    if tail:
        requirements = requirements[:active.end() + tail.start()]
    definitions = markdown_section(requirements, re.escape(milestone) + r" Requirements")
    defined = re.findall(r"^[ \t]*[-+*][ \t]+\[[ xX]\][ \t]+\*\*([A-Z][A-Z0-9]*-\d+)\*\*", definitions, re.M)
    table = markdown_section(requirements, "Traceability")
    table_pairs = []
    malformed = []
    has_header = False
    for line in table.splitlines():
        columns = [cell.strip() for cell in line.strip().removeprefix("|").removesuffix("|").split("|")]
        if columns == ["Requirement", "Phase", "Status"]:
            if has_header:
                malformed.append(line)
            has_header = True
            continue
        if not re.fullmatch(r"[A-Z][A-Z0-9]*-\d+", columns[0]):
            continue
        if len(columns) != 3 or not has_header:
            malformed.append(line)
            continue
        phase = re.fullmatch(r"Phase (\d+(?:\.\d+)?)", columns[1])
        if phase is None:
            malformed.append(line)
        else:
            table_pairs.append((columns[0], phase[1]))
    if not has_header:
        fail("expected Requirement, Phase and Status columns in traceability table")
    milestones = list(re.finditer(r"^## [^\n]*\b(v\d+\.\d+)\b[^\n]*$", roadmap, re.M))
    headings = [heading for heading in milestones if heading[1] == milestone]
    if len(headings) != 1:
        fail(f"expected one active {milestone} roadmap heading")
    start = headings[0].start()
    end = next((heading.start() for heading in milestones if heading.start() > start), len(roadmap))
    detail = markdown_section(roadmap[start:end], "Phase Details")
    phase_headings = list(re.finditer(r"^### Phase (\d+(?:\.\d+)?):[^\n]*$", detail, re.M))
    roadmap_pairs, phase_ids = [], []
    for index, heading in enumerate(phase_headings):
        phase = heading[1]
        phase_ids.append(phase)
        end = phase_headings[index + 1].start() if index + 1 < len(phase_headings) else len(detail)
        body = detail[heading.end():end]
        lines = re.findall(r"^\*\*Requirements\*\*:[ \t]*(.*)$", body, re.M)
        if len(lines) != 1:
            fail(f"Phase {phase} must have exactly one Requirements line")
        identifiers = re.findall(r"\b[A-Z][A-Z0-9]*-\d+\b", lines[0])
        if not identifiers:
            fail(f"Phase {phase} lists no requirement IDs")
        roadmap_pairs += [(identifier, phase) for identifier in identifiers]
    table_ids = [identifier for identifier, _ in table_pairs]
    roadmap_ids = [identifier for identifier, _ in roadmap_pairs]
    duplicates = lambda values: sorted(key for key, count in Counter(values).items() if count > 1)
    duplicate_ids = {"definitions": duplicates(defined), "table": duplicates(table_ids),
                     "roadmap": duplicates(roadmap_ids), "phase_sections": duplicates(phase_ids)}
    defined_set = set(defined)
    orphan_ids = {"table": sorted(defined_set - set(table_ids)), "roadmap": sorted(defined_set - set(roadmap_ids))}
    extra_ids = {"table": sorted(set(table_ids) - defined_set), "roadmap": sorted(set(roadmap_ids) - defined_set)}
    table_mapping, roadmap_mapping = dict(table_pairs), dict(roadmap_pairs)
    conflicts = [{"id": identifier, "table_phase": table_mapping[identifier], "roadmap_phase": roadmap_mapping[identifier]}
                 for identifier in sorted(set(table_ids) & set(roadmap_ids))
                 if table_mapping[identifier] != roadmap_mapping[identifier]]
    mapped_phases = sorted(set(phase_ids) | {phase for _, phase in table_pairs}, key=lambda value: tuple(map(int, value.split("."))))
    missing_phases = [phase for phase in mapped_phases if not phase_exists(phase)]
    valid = bool(defined and table_pairs and roadmap_pairs) and not (
        any(duplicate_ids.values()) or any(orphan_ids.values()) or any(extra_ids.values())
        or conflicts or malformed or missing_phases
    )
    report = {
        "valid": valid, "milestone": milestone,
        "definition_count": len(defined), "table_count": len(table_pairs), "roadmap_count": len(roadmap_pairs),
        "definition_ids": sorted(defined), "table_ids": sorted(table_ids), "roadmap_ids": sorted(roadmap_ids),
        "mapped_phases": mapped_phases, "mappings": dict(sorted(table_mapping.items())),
        "orphan_ids": orphan_ids, "extra_ids": extra_ids, "duplicate_ids": duplicate_ids,
        "conflicts": conflicts, "missing_phases": missing_phases, "malformed_rows": malformed,
        "requirements_sha256": sha256(requirements_text.encode()), "roadmap_sha256": sha256(roadmap_text.encode()),
        "scope": "Mapping validity only; no requirement satisfaction or closing owner decision is inferred.",
    }
    if not valid:
        fail("invalid active traceability: " + json.dumps(report, sort_keys=True))
    return report


def check_traceability():
    # Always read current files, including when all runs after historical checks.
    requirements = (ROOT / REQUIREMENTS_REL).read_bytes().decode("utf-8")
    roadmap = (ROOT / ROADMAP_REL).read_bytes().decode("utf-8")
    phase_exists = lambda phase: any(path.is_dir() for path in (ROOT / ".planning/phases").glob(phase + "-*"))
    print(json.dumps(traceability_report(requirements, roadmap, phase_exists), indent=2))
    print("PHASE69-TRACEABILITY-OK")


def check_sources():
    actual = build_sources()
    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(load_inventory()["sources"], sort_keys=True, allow_nan=False):
        fail("source inventory differs from pinned committed evidence")
    print(json.dumps({"source_count": len(actual["source_rows"]),
                      "matched_comparisons": actual["matched_comparisons"]}, indent=2))
    print("PHASE69-SOURCES-OK")


def check_cost():
    actual = build_cost()
    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(load_inventory()["cost"], sort_keys=True, allow_nan=False):
        fail("cost inventory differs from unique committed activities")
    print(json.dumps({**actual["summary"], "named_activity_utc_subtotal": actual["named_activity_utc_subtotal"],
                      "yardstick_capture": actual["yardstick_capture"]}, indent=2))
    print("PHASE69-COST-OK")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("sources", "cost", "traceability", "all"))
    args = parser.parse_args(argv)
    try:
        if args.command == "sources":
            check_sources()
        elif args.command == "cost":
            check_cost()
        elif args.command == "traceability":
            check_traceability()
        elif args.command == "all":
            check_sources()
            check_cost()
            check_traceability()
            print("PHASE69-ALL-OK")
    except (VerifyError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"PHASE69-FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
