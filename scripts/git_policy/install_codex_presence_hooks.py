#!/usr/bin/env python3
"""Idempotently install guarded Codex presence hooks into the global hooks file.

Target: ${CODEX_HOOKS_FILE:-$HOME/.codex/hooks.json}. Existing handlers from other
tools are preserved; our groups are tagged with a 'aps:' statusMessage prefix and
replaced on re-run. Commands resolve this repo at runtime from the git common-dir
and no-op cleanly in any other repo or outside a repo (global hooks fire machine-wide).
"""
import json
import os
import shutil
import sys

TAG = "aps:"


def guarded(rel, args, status):
    # `s` is the resolved script path; the final clause matches the Global-Constraints
    # guarded-command template verbatim (`exec python3 "$s"` / `exec "$s"`).
    runner = 'exec python3 "$s"' if rel.endswith(".py") else 'exec "$s"'
    cmd = (
        "sh -c '"
        'r="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" || exit 0; '
        'p="$(dirname "$r")"; '
        f's="$p/{rel}"; '
        '[ -f "$s" ] || exit 0; '
        + (f'{runner} {args}' if args else runner)
        + "'"
    )
    return {"type": "command", "command": cmd, "timeout": 5000, "statusMessage": TAG + status}


# GROUPS maps each Codex hook event to a LIST of (matcher, handler) groups so a single
# event (PreToolUse) can carry more than one of our groups (Task 7 appends the git-guard).
# matcher=None means "omit the matcher field" — which is how Codex's real global hooks
# (~/.codex/hooks.json, verified 2026-06-30) express catch-all SessionStart/Stop/PostToolUse
# firing. Do NOT use "startup|resume" for SessionStart: that is Claude-Code vocabulary and
# Codex SessionStart has no such sub-events, so it would never match and the register hook
# would silently never fire (success criterion 1 would fail with no error). PreToolUse MUST
# be restricted to apply_patch — the only Codex edit tool (probe F4) and the only payload
# shape codex_claim_guard.py can parse (tool_input.command). Edit/Write are Claude-Code tool
# names, not Codex, and the guard no-ops on them, so they are deliberately NOT in the matcher.
GROUPS = {
    "SessionStart": [(None, guarded("scripts/git_policy/presence_hook.sh", "register", "register presence"))],
    "PreToolUse": [("apply_patch", guarded("scripts/git_policy/codex_claim_guard.py", "", "auto-declare write area"))],
    "PostToolUse": [(None, guarded("scripts/git_policy/codex_presence_flush.py", "", "presence heartbeat / flush"))],
    "Stop": [(None, guarded("scripts/git_policy/presence_hook.sh", "deregister", "deregister presence"))],
}


def _strip_ours(groups):
    out = []
    for g in groups or []:
        kept = [h for h in g.get("hooks", []) if not h.get("statusMessage", "").startswith(TAG)]
        if kept:
            out.append({**g, "hooks": kept})
    return out


def install(doc):
    hooks = doc.setdefault("hooks", {})
    for event, our_groups in GROUPS.items():
        groups = _strip_ours(hooks.get(event))
        for matcher, handler in our_groups:
            entry = {"hooks": [handler]}
            if matcher is not None:
                entry["matcher"] = matcher  # omit the field entirely when None (Codex catch-all)
            groups.append(entry)
        hooks[event] = groups
    return doc


def main(argv):
    target = os.environ.get("CODEX_HOOKS_FILE") or os.path.expanduser("~/.codex/hooks.json")
    doc = {}
    if os.path.exists(target):
        try:
            with open(target) as fh:
                doc = json.load(fh)
        except ValueError:
            print(f"refusing to overwrite unparseable {target}", file=sys.stderr)
            return 1
    install(doc)
    if "--print" in argv:
        print(json.dumps(doc, indent=2))
        return 0
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if os.path.exists(target):
        shutil.copyfile(target, target + ".bak")  # back up the original before overwrite
    tmp = target + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2)
    os.replace(tmp, target)
    print(f"installed presence hooks into {target}; review/trust once via Codex /hooks if prompted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
