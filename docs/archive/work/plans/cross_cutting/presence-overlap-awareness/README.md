# Archived — Presence & Overlap Awareness implementation plan

## What
`2026-06-22-presence-overlap-awareness-implementation-plan.md` — the implementation
plan for the advisory presence/overlap-awareness registry built on top of the claims
board (per-session presence files, board-derived write sets, SessionStart/PreToolUse/Stop
hook wiring, and the agent-facing operating contract).

## Why archived (not deleted)
The plan was fully executed (2026-06-26) and verified at runtime, and it carries
provenance worth preserving: the Post-execution review record and the user's 2026-06-26
confirmation of the cross-worktree weighting (Open Decision #2). Deleting it would lose
that decision trail. Reference audit on 2026-06-26 found no remaining references to the
file (full path, basename, or stem), so it is no longer active work.

## Consumed / superseded by
- **Live system:** `scripts/git_policy/agent_presence.py`, `scripts/agent-presence`, and
  the `claim_guard.py` / `session_banner.sh` / `.claude/settings.json` hook wiring
  (commits `1c5cdf9b`..`80a2679b`; review reconciliation `3d4834e2`).
- **Operating contract:** merged into `docs/git-guidelines.md` → section
  "Presence & overlap awareness (advisory)".
- **Companion design (also archived 2026-06-27):** `docs/archive/work/designs/cross_cutting/presence-overlap-awareness/2026-06-22-presence-overlap-awareness-design.md`.

## Retention
Retained as historical provenance. Revisit if the presence system is revised or folded
into the consolidated parallel-agent-coordination (watchdog) effort.
