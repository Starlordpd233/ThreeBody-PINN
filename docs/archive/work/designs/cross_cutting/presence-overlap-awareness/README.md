# Archived — Presence & Overlap Awareness design

## What
`2026-06-22-presence-overlap-awareness-design.md` — the design document for the advisory
presence/overlap-awareness registry: the two-layer model (mechanical hook lifecycle +
agent-driven semantic reasoning), the presence-registry schema, the liveness/reaping
policy, the presence↔claims integration, the graduated-autonomy overlap protocol, and the
pre-build verification gate.

## Why archived (not deleted)
The design's `retirement_trigger` is satisfied: the Presence & Overlap Awareness system is
implemented and its operating contract is folded into `docs/git-guidelines.md` (section
"Presence & overlap awareness (advisory)"). The document is retained rather than deleted
because it preserves the original design rationale and the four-item pre-build
verification gate, which remain the reference for why the live system is shaped the way it
is. Reference audit on 2026-06-27 found a single inbound reference (the companion plan's
archive README), updated to point here.

## Consumed / superseded by
- **Live system:** `scripts/git_policy/agent_presence.py`, `scripts/agent-presence`, and
  the `claim_guard.py` / `session_banner.sh` / `.claude/settings.json` hook wiring.
- **Operating contract:** `docs/git-guidelines.md` → section
  "Presence & overlap awareness (advisory)".
- **Companion implementation plan (also archived):**
  `docs/archive/work/plans/cross_cutting/presence-overlap-awareness/2026-06-22-presence-overlap-awareness-implementation-plan.md`.

## Note on the archived snapshot
This file is a frozen historical snapshot. Its in-body relative links (e.g. to the
`parallel-agent-coordination` design) reflect the document's original active location
under `docs/work/designs/cross_cutting/presence-overlap-awareness/` and are intentionally
left unmodified; the link targets themselves remain under `docs/work/designs/` and
`docs/work/plans/`.

## Retention
Retained as historical provenance. Revisit if the presence system is revised or folded
into the consolidated parallel-agent-coordination (watchdog) effort.
