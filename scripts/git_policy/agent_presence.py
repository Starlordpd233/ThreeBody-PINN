#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import time

import agent_claims


STALE_FLOOR_SEC = int(os.environ.get("AGENT_PRESENCE_STALE", "1200"))


def who_key(session_id):
    return f"session:{session_id}"


def presence_file(session_id):
    return os.path.join(agent_claims.claims_dir(), f"presence-{session_id}.json")


def _atomic_write(path, data):
    dir_name = os.path.dirname(path)
    try:
        fd, tmp = tempfile.mkstemp(dir=dir_name, prefix="presence-tmp-", suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
            f.flush()
            os.fsync(f.fileno())
        os.rename(tmp, path)
    except Exception as e:
        print(f"agent_presence: failed to write {path}: {e}", file=sys.stderr)


def _pid_is_alive(pid):
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # If we get a permission error, the process exists but is owned by someone else
        return True
    except Exception:
        return False


def register(session_id, pid=None):
    if not session_id:
        return ""

    path = presence_file(session_id)
    now = int(time.time())
    entry = agent_claims.load(path) or {}

    entry["session_id"] = session_id
    entry["pid"] = pid
    entry.setdefault("start_time", now)
    entry["last_heartbeat"] = now
    entry.setdefault("task_summary", None)

    _atomic_write(path, entry)
    return path


def sweep_presence():
    directory = agent_claims.claims_dir()
    now = int(time.time())
    
    for name in os.listdir(directory):
        if not name.startswith("presence-") or not name.endswith(".json"):
            continue
            
        full = os.path.join(directory, name)
        entry = agent_claims.load(full)
        if entry is None:
            continue
            
        pid = entry.get("pid")
        if _pid_is_alive(pid):
            continue
            
        last_heartbeat = entry.get("last_heartbeat", 0)
        if now - last_heartbeat > STALE_FLOOR_SEC:
            # Reaping dead session
            session_id = entry.get("session_id")
            if session_id:
                agent_claims.release_by_who(who_key(session_id))
            try:
                os.remove(full)
            except OSError:
                pass


def main(argv):
    pass


if __name__ == "__main__":
    main(sys.argv)
