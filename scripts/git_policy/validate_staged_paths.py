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

ALLOW_LARGE_PATTERNS = (
    "simulation_data/Documentation/*",
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
        if matches_any(path, BLOCKED_PATTERNS):
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
