#!/usr/bin/env python3
"""Rerun the 184 missing standard quasi-random gold Brutus outputs.

This runner deliberately targets the documented standard-gold folder defaults:

    brutus 1e-13 130 0 10 0.01 3 ic_standard_XXXX.txt

It stages outputs first and only promotes validated files when --promote is
requested. It never moves, deletes, or rewrites IC files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import median


REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_PATH = REPO_ROOT / "simulation_data" / "Documentation" / "standard_quasi_random_ids_not_in_gold.md"
BRUTUS_BIN = REPO_ROOT / "brutus_Newton-main" / "brutus"
IC_DIR = REPO_ROOT / "simulation_data" / "Data" / "ic_final" / "ic_standard_quasi_random"
STAGING_DIR = REPO_ROOT / "simulation_data" / "Data" / "rerun_staging" / "standard_gold_missing_184"
STAGING_OUTPUT_DIR = STAGING_DIR / "outputs"
FINAL_OUTPUT_DIR = (
    REPO_ROOT
    / "simulation_data"
    / "Data"
    / "brutus_output"
    / "brutus_standard_quasi_random_gold_standard"
)
MANIFEST_PATH = STAGING_DIR / "run_manifest.json"
VALIDATION_SUMMARY_PATH = STAGING_DIR / "validation_summary.json"

PARAMS = {
    "tolerance": "1e-13",
    "word_length": "130",
    "t_begin": "0",
    "t_end": "10",
    "dt_out": "0.01",
    "n_particles": "3",
}
EXPECTED_FOOTER = {
    "tol": "1e-13",
    "Lw": "130",
    "N": "3",
    "dt": 0.01,
    "eta": 0.277971,
    "min_final_time": 10.0,
    "nominal_footer_t_end": 10.01,
}
EXPECTED_ID_COUNT = 184
DEFAULT_TIMEOUT_SECONDS = 3000
DEFAULT_STALL_SECONDS = 3600.0
DEFAULT_STALL_CHECK_SECONDS = 30.0
TIME_TOLERANCE = 1e-6
ETA_TOLERANCE = 1e-6
SNAPSHOT_VALUE_TOLERANCE = 1e-12

ID_RE = re.compile(r"\b\d{4}\b")
FOOTER_RE = re.compile(r"(\w+)=\s*([^\s]+)")
TIMESTEP_RE = re.compile(r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s+3(?:\s|$)")


class ValidationResult:
    def __init__(self, ok: bool, errors: list[str], footer: dict[str, str], final_time: float | None):
        self.ok = ok
        self.errors = errors
        self.footer = footer
        self.final_time = final_time

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "footer": self.footer,
            "final_time": self.final_time,
        }


class OutputProgress:
    def __init__(
        self,
        exists: bool,
        snapshot_count: int,
        final_time: float | None,
        idle_seconds: float | None,
        size: int,
    ):
        self.exists = exists
        self.snapshot_count = snapshot_count
        self.final_time = final_time
        self.idle_seconds = idle_seconds
        self.size = size

    exists: bool
    snapshot_count: int
    final_time: float | None
    idle_seconds: float | None
    size: int


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print preflight and command contract only")
    parser.add_argument("--limit", type=int, help="Run only the first N selected IDs")
    parser.add_argument("--workers", type=int, default=default_worker_count(), help="Concurrent Brutus workers")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Per-simulation timeout in seconds",
    )
    parser.add_argument(
        "--stall-seconds",
        type=float,
        default=DEFAULT_STALL_SECONDS,
        help=(
            "Skip a live Brutus run if its staged output has no new simulated "
            "timestep for this many real seconds; use 0 to disable"
        ),
    )
    parser.add_argument(
        "--stall-check-seconds",
        type=float,
        default=DEFAULT_STALL_CHECK_SECONDS,
        help="How often to check live output progress for stall detection",
    )
    parser.add_argument("--resume", action="store_true", help="Skip staged outputs that already validate")
    parser.add_argument("--validate-only", action="store_true", help="Validate staged outputs without running Brutus")
    parser.add_argument("--promote", action="store_true", help="Copy validated staged outputs to final output folder")
    return parser.parse_args(argv)


def default_worker_count() -> int:
    cpu_count = os.cpu_count() or 1
    return min(4, max(1, cpu_count // 3))


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_missing_ids(doc_path: Path = DOC_PATH) -> list[str]:
    text = doc_path.read_text()
    blocks = re.findall(r"```(?:text)?\n(.*?)```", text, flags=re.DOTALL)
    search_text = "\n".join(blocks) if blocks else text
    ids = ID_RE.findall(search_text)
    if len(ids) != EXPECTED_ID_COUNT:
        raise ValueError(f"Expected {EXPECTED_ID_COUNT} missing standard-gold IDs, found {len(ids)}")
    if len(set(ids)) != len(ids):
        raise ValueError("Missing standard-gold ID list contains duplicates")
    return ids


def ic_path_for_id(id_str: str) -> Path:
    return IC_DIR / f"ic_standard_{id_str}.txt"


def staged_output_path_for_id(id_str: str, output_dir: Path = STAGING_OUTPUT_DIR) -> Path:
    return output_dir / f"brutus_standard_{id_str}.txt"


def final_output_path_for_id(id_str: str, output_dir: Path = FINAL_OUTPUT_DIR) -> Path:
    return output_dir / f"brutus_standard_{id_str}.txt"


def build_brutus_command(brutus_bin: Path, ic_path: Path) -> list[str]:
    return [
        str(brutus_bin),
        PARAMS["tolerance"],
        PARAMS["word_length"],
        PARAMS["t_begin"],
        PARAMS["t_end"],
        PARAMS["dt_out"],
        PARAMS["n_particles"],
        str(ic_path),
    ]


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    with path.open() as f:
        return json.load(f)


def save_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp_path.replace(path)


def should_skip_for_resume(id_str: str, manifest: dict[str, dict[str, object]]) -> bool:
    entry = manifest.get(id_str)
    if not entry:
        return False
    validation = entry.get("validation")
    return entry.get("status") == "success" and isinstance(validation, dict) and validation.get("ok") is True


def read_ic_rows(ic_path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in ic_path.read_text().splitlines():
        parts = line.strip().split()
        if len(parts) == 7:
            rows.append([float(part) for part in parts])
    if len(rows) != 3:
        raise ValueError(f"Expected 3 IC rows with 7 columns in {ic_path}, found {len(rows)}")
    return rows


def parse_footer(line: str) -> dict[str, str]:
    if not line.startswith("Result:"):
        return {}
    footer = {match.group(1): match.group(2) for match in FOOTER_RE.finditer(line)}
    filename_match = re.search(r"filename=\s+(.*?)\s+N=", line)
    if filename_match:
        footer["filename"] = filename_match.group(1)
    return footer


def parse_snapshots(lines: list[str]) -> tuple[list[tuple[float, list[list[float]]]], float | None]:
    snapshots: list[tuple[float, list[list[float]]]] = []
    final_time: float | None = None
    i = 0
    while i < len(lines):
        match = TIMESTEP_RE.match(lines[i])
        if not match:
            i += 1
            continue
        time_value = float(match.group(1))
        body_rows: list[list[float]] = []
        for offset in range(1, 4):
            if i + offset >= len(lines):
                break
            parts = lines[i + offset].strip().split()
            if len(parts) != 7:
                break
            try:
                body_rows.append([float(part) for part in parts])
            except ValueError:
                break
        if len(body_rows) == 3:
            snapshots.append((time_value, body_rows))
            final_time = time_value
            i += 4
        else:
            i += 1
    return snapshots, final_time


def read_output_progress(output_path: Path, now: float | None = None) -> OutputProgress:
    if now is None:
        now = time.time()
    if not output_path.exists():
        return OutputProgress(False, 0, None, None, 0)

    stat = output_path.stat()
    lines = output_path.read_text(errors="replace").splitlines()
    snapshots, final_time = parse_snapshots(lines)
    return OutputProgress(
        True,
        len(snapshots),
        final_time,
        now - stat.st_mtime,
        stat.st_size,
    )


def stall_reason(progress: OutputProgress, stall_seconds: float) -> str | None:
    if stall_seconds <= 0 or not progress.exists or progress.idle_seconds is None:
        return None
    if progress.final_time is not None and progress.final_time >= EXPECTED_FOOTER["min_final_time"]:
        return None
    if progress.idle_seconds < stall_seconds:
        return None
    if progress.final_time is None:
        return f"no valid timestep after {progress.idle_seconds:.1f}s"
    return f"no new timestep for {progress.idle_seconds:.1f}s at t={progress.final_time:.12g}"


def stop_process(process: subprocess.Popen[object], grace_seconds: float = 10.0) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def nearly_equal(left: float, right: float, tolerance: float) -> bool:
    return abs(left - right) <= tolerance


def validate_first_snapshot(ic_rows: list[list[float]], snapshots: list[tuple[float, list[list[float]]]]) -> list[str]:
    if not snapshots:
        return ["No valid Brutus snapshots found"]
    first_time, first_rows = snapshots[0]
    errors: list[str] = []
    if not nearly_equal(first_time, 0.0, TIME_TOLERANCE):
        errors.append(f"First snapshot time is {first_time}, expected 0")
    for row_idx, (ic_row, out_row) in enumerate(zip(ic_rows, first_rows), start=1):
        for col_idx, (ic_value, out_value) in enumerate(zip(ic_row, out_row), start=1):
            if not nearly_equal(ic_value, out_value, SNAPSHOT_VALUE_TOLERANCE):
                errors.append(
                    f"First snapshot mismatch row {row_idx} col {col_idx}: output {out_value} != IC {ic_value}"
                )
    return errors


def validate_footer_contract(footer: dict[str, str]) -> list[str]:
    errors: list[str] = []
    required = ["N", "t_begin", "t_end", "dt", "eta", "tol", "Lw", "t_cpu"]
    for key in required:
        if key not in footer:
            errors.append(f"Footer missing {key}")
    if errors:
        return errors

    if footer["N"] != EXPECTED_FOOTER["N"]:
        errors.append(f"Footer N={footer['N']}, expected {EXPECTED_FOOTER['N']}")
    if footer["tol"] != EXPECTED_FOOTER["tol"]:
        errors.append(f"Footer tol={footer['tol']}, expected {EXPECTED_FOOTER['tol']}")
    if footer["Lw"] != EXPECTED_FOOTER["Lw"]:
        errors.append(f"Footer Lw={footer['Lw']}, expected {EXPECTED_FOOTER['Lw']}")
    if not nearly_equal(float(footer["dt"]), EXPECTED_FOOTER["dt"], TIME_TOLERANCE):
        errors.append(f"Footer dt={footer['dt']}, expected {EXPECTED_FOOTER['dt']}")
    if not nearly_equal(float(footer["eta"]), EXPECTED_FOOTER["eta"], ETA_TOLERANCE):
        errors.append(f"Footer eta={footer['eta']}, expected {EXPECTED_FOOTER['eta']}")
    if float(footer["t_end"]) < EXPECTED_FOOTER["min_final_time"]:
        errors.append(f"Footer t_end={footer['t_end']}, expected at least {EXPECTED_FOOTER['min_final_time']}")
    if not (10.0 <= float(footer["t_end"]) <= 10.02):
        errors.append(f"Footer t_end={footer['t_end']} is outside expected standard-gold range [10.0, 10.02]")
    return errors


def validate_output(output_path: Path, ic_path: Path) -> ValidationResult:
    errors: list[str] = []
    if not output_path.exists():
        return ValidationResult(False, [f"Output missing: {output_path}"], {}, None)
    if output_path.stat().st_size == 0:
        return ValidationResult(False, [f"Output empty: {output_path}"], {}, None)
    if not ic_path.exists():
        return ValidationResult(False, [f"IC missing: {ic_path}"], {}, None)

    lines = output_path.read_text(errors="replace").splitlines()
    footer_line = next((line for line in reversed(lines) if line.startswith("Result:")), None)
    if footer_line is None:
        return ValidationResult(False, ["Missing full Result: footer"], {}, None)

    footer = parse_footer(footer_line)
    snapshots, final_time = parse_snapshots(lines)
    try:
        ic_rows = read_ic_rows(ic_path)
    except ValueError as exc:
        return ValidationResult(False, [str(exc)], footer, final_time)

    errors.extend(validate_footer_contract(footer))
    errors.extend(validate_first_snapshot(ic_rows, snapshots))
    if final_time is None:
        errors.append("No final timestep found")
    elif final_time < EXPECTED_FOOTER["min_final_time"]:
        errors.append(f"Final timestep {final_time} is below {EXPECTED_FOOTER['min_final_time']}")

    return ValidationResult(not errors, errors, footer, final_time)


def preflight(ids: list[str], brutus_bin: Path = BRUTUS_BIN) -> list[str]:
    errors: list[str] = []
    if not brutus_bin.exists():
        errors.append(f"Brutus binary missing: {brutus_bin}")
    elif not os.access(brutus_bin, os.X_OK):
        errors.append(f"Brutus binary is not executable: {brutus_bin}")
    missing_ics = [ic_path_for_id(id_str) for id_str in ids if not ic_path_for_id(id_str).exists()]
    if missing_ics:
        errors.append(f"Missing {len(missing_ics)} IC files; first missing: {missing_ics[0]}")
    existing_final = [final_output_path_for_id(id_str) for id_str in ids if final_output_path_for_id(id_str).exists()]
    if existing_final:
        errors.append(f"{len(existing_final)} final gold outputs already exist; first existing: {existing_final[0]}")
    return errors


def print_preflight(ids: list[str], args: argparse.Namespace) -> None:
    print("=== Standard-Gold Missing 184 Brutus Rerun Preflight ===")
    print(f"Repository: {REPO_ROOT}")
    print(f"IDs: {len(ids)} ({ids[0]} ... {ids[-1]})")
    print(f"Brutus binary: {BRUTUS_BIN}")
    print(f"Input IC directory: {IC_DIR}")
    print(f"Staging output directory: {STAGING_OUTPUT_DIR}")
    print(f"Final output directory: {FINAL_OUTPUT_DIR}")
    print(f"Workers: {args.workers}")
    print(f"Timeout seconds: {args.timeout_seconds}")
    print(f"Stall seconds: {args.stall_seconds:g} (0 disables live timestep-progress checks)")
    print(f"Stall check seconds: {args.stall_check_seconds:g}")
    print(f"Parameter contract: {' '.join(build_brutus_command(Path('brutus_Newton-main/brutus'), Path('<ic_standard_XXXX.txt>')))}")
    print("Expected footer: tol=1e-13 Lw=130 dt=0.01 eta~=0.277971 t_end~=10.01")


def command_metadata(command: list[str], ic_path: Path, output_path: Path) -> dict[str, object]:
    return {
        "command": command,
        "params": PARAMS,
        "brutus_bin": str(BRUTUS_BIN),
        "brutus_bin_sha256": sha256_file(BRUTUS_BIN) if BRUTUS_BIN.exists() else None,
        "ic_path": str(ic_path),
        "ic_sha256": sha256_file(ic_path) if ic_path.exists() else None,
        "output_path": str(output_path),
    }


def run_one(
    id_str: str,
    timeout_seconds: int,
    stall_seconds: float = DEFAULT_STALL_SECONDS,
    stall_check_seconds: float = DEFAULT_STALL_CHECK_SECONDS,
    state: DashboardState | None = None,
) -> dict[str, object]:
    ic_path = ic_path_for_id(id_str)
    output_path = staged_output_path_for_id(id_str)
    command = build_brutus_command(BRUTUS_BIN, ic_path)
    start = time.time()
    status = "success"
    reason = ""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if state is not None:
        with state.lock:
            state.counts["queued"] -= 1
            state.counts["running"] += 1
            state.active[id_str] = start

    with output_path.open("w") as out:
        process = subprocess.Popen(command, stdout=out, stderr=subprocess.STDOUT)
        while True:
            return_code = process.poll()
            if return_code is not None:
                if return_code != 0:
                    status = "failed"
                    reason = f"exit code {return_code}"
                break

            now = time.time()
            if now - start >= timeout_seconds:
                status = "timeout"
                reason = f"timeout {timeout_seconds}s"
                stop_process(process)
                break

            progress = read_output_progress(output_path, now=now)
            reason_if_stalled = stall_reason(progress, stall_seconds)
            if reason_if_stalled is not None:
                status = "stalled"
                reason = reason_if_stalled
                stop_process(process)
                break

            sleep_seconds = max(0.05, stall_check_seconds)
            if timeout_seconds > 0:
                sleep_seconds = min(sleep_seconds, max(0.05, timeout_seconds - (now - start)))
            time.sleep(sleep_seconds)

    duration = time.time() - start
    validation = validate_output(output_path, ic_path)
    if status == "success" and not validation.ok:
        status = "failed"
        reason = "; ".join(validation.errors)

    result = command_metadata(command, ic_path, output_path)
    result.update(
        {
            "id": id_str,
            "status": status,
            "reason": reason,
            "start": start,
            "end": start + duration,
            "duration": duration,
            "validation": validation.to_dict(),
            "output_sha256": sha256_file(output_path) if output_path.exists() else None,
        }
    )
    return result


class DashboardState:
    def __init__(self, total: int, timeout_seconds: int, stall_seconds: float):
        self.total = total
        self.completed = 0
        self.counts = {
            "queued": total,
            "running": 0,
            "success": 0,
            "failed": 0,
            "timeout": 0,
            "stalled": 0,
            "skipped": 0,
        }
        self.active: dict[str, float] = {}
        self.durations: list[float] = []
        self.recent: list[str] = []
        self.start = time.time()
        self.timeout_seconds = timeout_seconds
        self.stall_seconds = stall_seconds
        self.done = False
        self.lock = threading.Lock()


def dashboard_loop(state: DashboardState) -> None:
    while True:
        with state.lock:
            done = state.done
            snapshot = {
                "completed": state.completed,
                "counts": dict(state.counts),
                "active": dict(state.active),
                "durations": list(state.durations),
                "recent": list(state.recent),
                "elapsed": time.time() - state.start,
                "timeout_seconds": state.timeout_seconds,
                "stall_seconds": state.stall_seconds,
            }
        if sys.stdout.isatty():
            print_dashboard(snapshot, state.total)
        if done:
            break
        time.sleep(1)


def print_dashboard(snapshot: dict[str, object], total: int) -> None:
    sys.stdout.write("\033[2J\033[H")
    elapsed = snapshot["elapsed"]
    counts = snapshot["counts"]
    active = snapshot["active"]
    durations = snapshot["durations"]
    remaining = total - snapshot["completed"]
    active_count = max(1, len(active))
    eta = "N/A"
    if durations:
        eta = f"{(remaining * median(durations)) / active_count:.1f}s"
    print("=== Missing 184 Standard-Gold Brutus Rerun Dashboard ===")
    print("Params: 1e-13 130 0 10 0.01 3")
    stall_text = "disabled" if snapshot["stall_seconds"] <= 0 else f"{snapshot['stall_seconds']:g}s"
    print(f"Timeout: {snapshot['timeout_seconds']}s | Stall: {stall_text} without timestep progress")
    print(f"Staging: {repo_relative(STAGING_OUTPUT_DIR)}")
    print(f"Progress: {snapshot['completed']}/{total} | Elapsed: {elapsed:.1f}s | ETA: {eta}")
    print(
        "Counts: "
        + " ".join(f"{key}={value}" for key, value in counts.items())
    )
    if active:
        print("Active:")
        now = time.time()
        for id_str, start in sorted(active.items()):
            print(f"  {id_str}: {now - start:.1f}s")
    if snapshot["recent"]:
        print("Recent:")
        for item in snapshot["recent"][-8:]:
            print(f"  {item}")
    sys.stdout.flush()


def validate_ids(ids: list[str], output_dir: Path = STAGING_OUTPUT_DIR) -> dict[str, object]:
    details: dict[str, object] = {}
    summary = {"total": len(ids), "passes": 0, "failures": 0, "details": details}
    for id_str in ids:
        result = validate_output(staged_output_path_for_id(id_str, output_dir), ic_path_for_id(id_str))
        details[id_str] = result.to_dict()
        if result.ok:
            summary["passes"] += 1
        else:
            summary["failures"] += 1
    return summary


def promote_outputs(ids: list[str], staging_output_dir: Path = STAGING_OUTPUT_DIR, final_output_dir: Path = FINAL_OUTPUT_DIR) -> list[Path]:
    final_output_dir.mkdir(parents=True, exist_ok=True)
    promoted: list[Path] = []
    for id_str in ids:
        source = staging_output_dir / f"brutus_standard_{id_str}.txt"
        target = final_output_dir / f"brutus_standard_{id_str}.txt"
        if not source.exists():
            raise FileNotFoundError(f"Staged output missing: {source}")
        if target.exists():
            raise FileExistsError(f"Refusing to overwrite existing final output: {target}")
        shutil.copy2(source, target)
        promoted.append(target)
    return promoted


def select_ids(ids: list[str], limit: int | None) -> list[str]:
    if limit is None:
        return ids
    if limit < 1:
        raise ValueError("--limit must be >= 1")
    return ids[:limit]


def run_batch(ids: list[str], args: argparse.Namespace) -> dict[str, dict[str, object]]:
    manifest = load_manifest()
    selected = select_ids(ids, args.limit)
    STAGING_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.resume:
        pending: list[str] = []
        skipped = 0
        for id_str in selected:
            if should_skip_for_resume(id_str, manifest) and validate_output(
                staged_output_path_for_id(id_str), ic_path_for_id(id_str)
            ).ok:
                skipped += 1
            else:
                pending.append(id_str)
    else:
        pending = selected
        skipped = 0

    state = DashboardState(len(selected), args.timeout_seconds, args.stall_seconds)
    state.counts["queued"] = len(pending)
    state.counts["skipped"] = skipped
    state.completed = skipped
    dashboard = threading.Thread(target=dashboard_loop, args=(state,), daemon=True)
    dashboard.start()

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {}
            for id_str in pending:
                futures[
                    pool.submit(
                        run_one,
                        id_str,
                        args.timeout_seconds,
                        args.stall_seconds,
                        args.stall_check_seconds,
                        state,
                    )
                ] = id_str

            for future in as_completed(futures):
                id_str = futures[future]
                result = future.result()
                manifest[id_str] = result
                save_json(MANIFEST_PATH, manifest)
                status = str(result["status"])
                with state.lock:
                    state.counts["running"] -= 1
                    state.counts[status] = state.counts.get(status, 0) + 1
                    state.completed += 1
                    state.active.pop(id_str, None)
                    if "duration" in result:
                        state.durations.append(float(result["duration"]))
                    state.recent.append(f"{id_str}: {status} ({float(result.get('duration', 0)):.1f}s)")
    finally:
        with state.lock:
            state.done = True
        dashboard.join()

    return manifest


def write_validation_summary(ids: list[str]) -> dict[str, object]:
    summary = validate_ids(ids)
    save_json(VALIDATION_SUMMARY_PATH, summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        ids = parse_missing_ids()
        selected = select_ids(ids, args.limit)
        print_preflight(selected, args)

        errors = preflight(selected)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 2

        if args.dry_run:
            print("Dry run complete; no simulations launched.")
            return 0

        if args.validate_only:
            summary = write_validation_summary(selected)
            print(f"Validation summary written to {repo_relative(VALIDATION_SUMMARY_PATH)}")
            print(f"Passes: {summary['passes']} Failures: {summary['failures']}")
            return 0 if summary["failures"] == 0 else 1

        if args.promote:
            summary = write_validation_summary(selected)
            if summary["failures"]:
                print(f"Refusing promotion: {summary['failures']} staged outputs failed validation", file=sys.stderr)
                return 1
            promoted = promote_outputs(selected)
            print(f"Promoted {len(promoted)} outputs to {repo_relative(FINAL_OUTPUT_DIR)}")
            return 0

        run_batch(ids, args)
        summary = write_validation_summary(selected)
        print(f"Manifest written to {repo_relative(MANIFEST_PATH)}")
        print(f"Validation summary written to {repo_relative(VALIDATION_SUMMARY_PATH)}")
        print(f"Passes: {summary['passes']} Failures: {summary['failures']}")
        return 0 if summary["failures"] == 0 else 1
    except KeyboardInterrupt:
        print("\nInterrupted by user; partial staged outputs remain for inspection or rerun.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
