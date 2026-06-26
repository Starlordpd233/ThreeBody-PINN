#!/usr/bin/env python3
"""Advisory presence registry: one JSON file per live top-level session.

Sits on top of the claims board (agent_claims.py) and shares its git
common-dir location so every worktree sees the same roster. A presence file
records liveness (pid, last_heartbeat) and intent (task_summary); a session's
*write set* is derived from the claims board, never duplicated here.

Identity is the Claude session id. Hooks read it from their stdin payload; agent
Bash-tool calls read it from CLAUDE_CODE_SESSION_ID, which the SessionStart hook
seeds into CLAUDE_ENV_FILE (it is not assumed to pre-exist). The join key with the
claims board is "session:<session_id>" -- exactly what claim_guard.py writes as
AGENT_CLAIM_WHO.

Advisory only: every entry point fails open and the CLI always exits 0. The one
hard backstop against silent overwrite is the commit-time owned-paths net in
scripts/agent-commit, not this module.
"""
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_claims  # noqa: E402

FRESH_SECONDS = 120
_SAFE_SID = re.compile(r"^[A-Za-z0-9._-]+$")


def _stale_floor():
    return int(os.environ.get("AGENT_PRESENCE_STALE", str(20 * 60)))


def presence_dir():
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
    path = os.path.join(common, "agent-presence")
    os.makedirs(path, exist_ok=True)
    return path


def _safe_session_id(session_id):
    if not session_id:
        return None
    session_id = str(session_id).strip()
    return session_id if _SAFE_SID.match(session_id) else None


def presence_file(session_id):
    sid = _safe_session_id(session_id)
    if sid is None:
        return None
    return os.path.join(presence_dir(), f"{sid}.json")


def who_key(session_id):
    return f"session:{session_id}"


def _session_from_env():
    return _safe_session_id(os.environ.get("CLAUDE_CODE_SESSION_ID"))


def _session_from_stdin():
    # Only read a piped payload; never block on an interactive tty.
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return None
        payload = json.load(sys.stdin)
    except Exception:
        return None
    return _safe_session_id(payload.get("session_id"))


def _pid_alive(pid):
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 1:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True   # exists, owned by another user
    except OSError:
        return False


def _atomic_write(path, obj):
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(obj, handle)
    os.replace(tmp, path)


def _git_context():
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
    except Exception:
        return "?", "?"
    worktree = os.path.basename(root) or "?"
    try:
        branch = subprocess.run(
            ["git", "-C", root, "symbolic-ref", "--short", "HEAD"],
            text=True, capture_output=True, check=True,
        ).stdout.strip() or "DETACHED"
    except Exception:
        branch = "DETACHED"
    return worktree, branch


def _load_or_init(session_id):
    path = presence_file(session_id)
    entry = agent_claims.load(path) if path else None
    if entry is None:
        now = int(time.time())
        entry = {
            "session_id": session_id,
            "pid": None,
            "worktree": "?",
            "branch": "?",
            "start_time": now,
            "task_summary": None,
            "last_heartbeat": now,
        }
    return entry


def sweep_presence():
    directory = presence_dir()
    now = int(time.time())
    floor = _stale_floor()
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        if name.endswith(".tmp"):
            try:
                os.remove(full)
            except OSError:
                pass
            continue
        entry = agent_claims.load(full)
        if entry is None:
            continue
        pid = entry.get("pid")
        if pid and _pid_alive(pid):
            continue                # trusted-live: keep regardless of heartbeat age
        # Absent, dead, OR untrusted pid (e.g. the transient SessionStart shell
        # captured by getppid()): do NOT reap on sight -- fall through to the
        # heartbeat-stale floor (design reaping table row 3). register/announce/
        # heartbeat keep last_heartbeat fresh, so an active session is never reaped.
        reap = (now - entry.get("last_heartbeat", 0)) > floor
        if reap:
            sid = entry.get("session_id")
            if sid:
                agent_claims.release_by_who(who_key(sid))
            try:
                os.remove(full)
            except OSError:
                pass


def register(session_id=None, pid=None):
    session_id = _safe_session_id(session_id) or _session_from_env()
    if session_id is None:
        return ""   # no identity -> no presence; stay silent
    sweep_presence()
    entry = _load_or_init(session_id)
    worktree, branch = _git_context()
    entry["session_id"] = session_id
    entry["pid"] = int(pid) if pid is not None else os.getppid()
    entry["worktree"] = worktree
    entry["branch"] = branch
    entry["last_heartbeat"] = int(time.time())
    _atomic_write(presence_file(session_id), entry)
    return list_roster(exclude=session_id)


def heartbeat(session_id):
    sid = _safe_session_id(session_id)
    if sid is None:
        return 0
    path = presence_file(sid)
    entry = agent_claims.load(path) if path else None
    if entry is None:
        return 0   # no registered presence -> nothing to bump (fail-safe)
    entry["last_heartbeat"] = int(time.time())
    _atomic_write(path, entry)
    return 0


def _format_line(entry, areas, now, my_worktree=None):
    sid = (entry.get("session_id") or "????")[:4]
    worktree = entry.get("worktree") or "?"
    branch = entry.get("branch") or "?"
    summary = entry.get("task_summary") or "(no task announced)"
    age = now - entry.get("last_heartbeat", now)
    heart = "fresh" if age < FRESH_SECONDS else f"{age // 60}m"
    writes = ", ".join(areas) if areas else "none"
    # Cross-worktree peers are visible but marked (design roster format).
    mark = "" if (my_worktree is None or worktree == my_worktree) else "  [cross-worktree]"
    return (f"  [{sid}] {worktree} / {branch}{mark} — \"{summary}\"\n"
            f"         writes: {writes}   ♥ {heart}")


def list_roster(exclude=None):
    sweep_presence()
    if exclude is None:
        exclude = _session_from_env()
    directory = presence_dir()
    now = int(time.time())
    my_worktree, _ = _git_context()
    lines = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        entry = agent_claims.load(os.path.join(directory, name))
        if entry is None:
            continue
        sid = entry.get("session_id")
        if sid and sid == exclude:
            continue
        areas = agent_claims.claims_for_who(who_key(sid)) if sid else []
        lines.append(_format_line(entry, areas, now, my_worktree))
    if not lines:
        return "Active sessions (excluding yours): none"
    return "Active sessions (excluding yours):\n" + "\n".join(lines)


def main(argv):
    pass


if __name__ == "__main__":
    main(sys.argv)
