#!/usr/bin/env python3
"""Advisory cross-worktree claims board (one JSON file per claim).

Claims live under $(git rev-parse --git-common-dir)/agent-claims/ so every
worktree shares them. One file per claim means concurrent agents add and drop
claims without corrupting a shared file. Expiry is time-based (each edit-hook is
a short-lived process, so there is no persistent agent PID to test) plus
explicit release.

Identity ("who") is resolved as: AGENT_CLAIM_WHO (set by the edit hook to the
Claude session id) > GIT_AGENT_ID > pid:<ppid>.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

EXPIRY_SECONDS = int(os.environ.get("AGENT_CLAIM_EXPIRY", str(2 * 60 * 60)))


def claims_dir():
    common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    if not os.path.isabs(common):
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        common = os.path.join(root, common)
    path = os.path.join(common, "agent-claims")
    os.makedirs(path, exist_ok=True)
    return path


def claim_file(area):
    key = hashlib.sha1(area.encode("utf-8")).hexdigest()[:16]
    return os.path.join(claims_dir(), key)


def agent_id():
    return (
        os.environ.get("AGENT_CLAIM_WHO")
        or os.environ.get("GIT_AGENT_ID")
        or f"pid:{os.getppid()}"
    )


def load(path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def expired(entry):
    return entry is None or (time.time() - entry.get("when", 0)) > EXPIRY_SECONDS


def sweep():
    directory = claims_dir()
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        if name.endswith(".tmp") or expired(load(full)):
            try:
                os.remove(full)
            except OSError:
                pass


def holder(area):
    """Return the entry if a *different* live agent holds `area`, else None."""
    entry = load(claim_file(area))
    if expired(entry) or entry.get("who") == agent_id():
        return None
    return entry


def claim(area, why=""):
    sweep()
    if holder(area) is not None:
        return 0  # held by someone else; advisory, do not clobber
    path = claim_file(area)
    entry = {"who": agent_id(), "area": area, "why": why, "when": int(time.time())}
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(entry, handle)
    os.replace(tmp, path)
    return 0


def release(area):
    path = claim_file(area)
    entry = load(path)
    if entry is not None and entry.get("who") == agent_id():
        try:
            os.remove(path)
        except OSError:
            pass
    return 0


def check(area):
    sweep()
    other = holder(area)
    if other is None:
        return 0
    when = time.strftime("%H:%M", time.localtime(other.get("when", 0)))
    print(f"claim conflict: '{area}' is held by {other.get('who')} since {when}", file=sys.stderr)
    return 3


def list_claims():
    sweep()
    directory = claims_dir()
    for name in sorted(os.listdir(directory)):
        entry = load(os.path.join(directory, name))
        if entry is not None:
            print(f"{entry.get('who')}\t{entry.get('area')}\t{entry.get('why', '')}")
    return 0


def main(argv):
    if not argv:
        print("usage: agent_claims.py {claim|release|check|list} [area] [why]", file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    if command == "list":
        return list_claims()
    if not rest:
        print(f"git policy: '{command}' needs an <area>", file=sys.stderr)
        return 2
    if command == "claim":
        return claim(rest[0], rest[1] if len(rest) > 1 else "")
    if command == "release":
        return release(rest[0])
    if command == "check":
        return check(rest[0])
    print(f"unknown command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
