#!/usr/bin/env python3
import fnmatch
import json
import os
import subprocess
import sys


MAX_BLOB_BYTES = 10 * 1024 * 1024

BLOCKED_PATTERNS = (
    ".DS_Store",
    "*/.DS_Store",
    "__pycache__/*",
    "*/__pycache__/*",
    "*.pyc",
    "tmp/*",
    "*/tmp/*",
    "scratch/*",
    "*/scratch/*",
    "runs/*",
    "*/runs/*",
    "outputs/*",
    "*/outputs/*",
    "wandb/*",
    "*/wandb/*",
)

ALLOWED_BLOCKED_PATHS = {
    ".planning/tmp/docs-work-manifest.json",
    ".planning/tmp/verify-Phase-9-consistency.json",
    # Phase 57 band generation 1 (blocked smoke). runs/ stays blocked for
    # ordinary runtime output; these 18 exact paths are the artifacts the
    # committed Phase-57 run ledger addresses by sha256, so they are tracked
    # in place to keep those integrity claims verifiable. Owner ruling
    # 2026-09-09 on GAP-57-03. Exact paths only — never a runs/ wildcard.
    "runs/stage0-v23-smoke/checkpoints/ckpt-223666118608.pt",
    "runs/stage0-v23-smoke/checkpoints/failure-stage-0-step-0.pt",
    "runs/stage0-v23-smoke/checkpoints/latest.pt",
    "runs/stage0-v23-smoke/checkpoints/stage-0-init.pt",
    "runs/stage0-v23-smoke/config.yaml",
    "runs/stage0-v23-smoke/curriculum.jsonl",
    "runs/stage0-v23-smoke/failure/README.txt",
    "runs/stage0-v23-smoke/failure/trip.json",
    "runs/stage0-v23-smoke/logs/train.log",
    "runs/stage0-v23-smoke/logs/train.log.jsonl",
    "runs/stage0-v23-smoke/preflight.json",
    "runs/stage0-v23-smoke/run_start_rng.pt",
    "runs/stage0-v23-smoke/splits.json",
    "runs/stage0-v23-smoke/status.json",
    "runs/stage0-v23-smoke/summary.json",
    "runs/stage0-v23-smoke/summary.md",
    "runs/stage0-v23-smoke/tb/<host>.54461.0",
    "runs/stage0-v23-smoke/training_metadata.json",
    # GAP-57-06 option A (owner ruling 2026-09-27): retain the interrupted
    # generation-2 smoke in place. These are its 16 observed files only.
    "runs/stage0-v23g2-smoke/checkpoints/ckpt-61163069181.pt",
    "runs/stage0-v23g2-smoke/checkpoints/latest.pt",
    "runs/stage0-v23g2-smoke/checkpoints/stage-0-init.pt",
    "runs/stage0-v23g2-smoke/checkpoints/step-000031.pt",
    "runs/stage0-v23g2-smoke/config.yaml",
    "runs/stage0-v23g2-smoke/curriculum.jsonl",
    "runs/stage0-v23g2-smoke/logs/train.log",
    "runs/stage0-v23g2-smoke/logs/train.log.jsonl",
    "runs/stage0-v23g2-smoke/preflight.json",
    "runs/stage0-v23g2-smoke/run_start_rng.pt",
    "runs/stage0-v23g2-smoke/splits.json",
    "runs/stage0-v23g2-smoke/status.json",
    "runs/stage0-v23g2-smoke/summary.json",
    "runs/stage0-v23g2-smoke/summary.md",
    "runs/stage0-v23g2-smoke/tb/events.out.tfevents.1789304466.<host>.91780.0",
    "runs/stage0-v23g2-smoke/training_metadata.json",
    # GAP-57-11 option A: retain the 23 observed generation-5 smoke files.
    # Exact paths only; future run directories remain blocked.
    "runs/stage0-v23g5-smoke/checkpoints/best.pt",
    "runs/stage0-v23g5-smoke/checkpoints/ckpt-18887573397.pt",
    "runs/stage0-v23g5-smoke/checkpoints/latest.pt",
    "runs/stage0-v23g5-smoke/checkpoints/stage-0-init.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000100.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000200.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000300.pt",
    "runs/stage0-v23g5-smoke/config.yaml",
    "runs/stage0-v23g5-smoke/curriculum.jsonl",
    "runs/stage0-v23g5-smoke/logs/train.log",
    "runs/stage0-v23g5-smoke/logs/train.log.jsonl",
    "runs/stage0-v23g5-smoke/preflight.json",
    "runs/stage0-v23g5-smoke/run_start_rng.pt",
    "runs/stage0-v23g5-smoke/splits.json",
    "runs/stage0-v23g5-smoke/status.json",
    "runs/stage0-v23g5-smoke/summary.json",
    "runs/stage0-v23g5-smoke/summary.md",
    "runs/stage0-v23g5-smoke/tb/<host>.56068.0",
    "runs/stage0-v23g5-smoke/training_metadata.json",
    "runs/stage0-v23g5-smoke/validation.jsonl",
    "runs/stage0-v23g5-smoke/validation_gate/step-00000100.json",
    "runs/stage0-v23g5-smoke/validation_gate/step-00000200.json",
    "runs/stage0-v23g5-smoke/validation_gate/step-00000300.json",
}

ALLOW_LARGE_PATTERNS = (
    "simulation_data/Documentation/*",
    # Exact exceptions for the two preserved generation-2 checkpoints >10 MiB.
    "runs/stage0-v23g2-smoke/checkpoints/latest.pt",
    "runs/stage0-v23g2-smoke/checkpoints/step-000031.pt",
    # Exact >10 MiB exceptions for the retained generation-5 smoke.
    "runs/stage0-v23g5-smoke/checkpoints/best.pt",
    "runs/stage0-v23g5-smoke/checkpoints/latest.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000100.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000200.pt",
    "runs/stage0-v23g5-smoke/checkpoints/step-000300.pt",
)


def fail(message):
    print(f"git policy: {message}", file=sys.stderr)
    return 1


def staged_files():
    override = os.environ.get("GIT_POLICY_STAGED_FILES")
    if override is not None:
        return [line.strip() for line in override.splitlines() if line.strip()]
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def staged_sizes():
    override = os.environ.get("GIT_POLICY_STAGED_SIZES")
    if override:
        return {str(key): int(value) for key, value in json.loads(override).items()}
    sizes = {}
    for path in staged_files():
        result = subprocess.run(
            ["git", "cat-file", "-s", f":{path}"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            sizes[path] = int(result.stdout.strip())
    return sizes


def matches_any(path, patterns):
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def main():
    paths = staged_files()
    errors = []

    for path in paths:
        if path not in ALLOWED_BLOCKED_PATHS and matches_any(path, BLOCKED_PATTERNS):
            errors.append(f"generated or scratch artifact is staged: {path}")

    sizes = staged_sizes()
    for path, size in sizes.items():
        if size > MAX_BLOB_BYTES and not matches_any(path, ALLOW_LARGE_PATTERNS):
            errors.append(f"staged blob exceeds 10 MiB: {path}")

    if errors:
        for error in errors:
            print(f"git policy: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
