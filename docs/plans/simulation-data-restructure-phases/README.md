# Simulation Data Restructure — Phased Execution Bundle

This bundle replaces the monolithic migration workflow with independent, testable phases.

## Why this split exists

The original plan mixed three high-risk tracks in one pass:
1. Large filesystem migration of gitignored data
2. Pre-existing bug fixes unrelated to migration mechanics
3. Broad path rewrites across Python + documentation

This phased version reduces blast radius and resolves previously identified execution bugs:
- No `git mv` on ignored/untracked sources
- No pre-created destination collisions for whole-directory `git mv`
- No contradictory backup commit flow
- Correct `logging.py` path fix (no `Validation/Validation`)
- Every commit stage includes explicit `git add -A`
- `.gitignore` cleanup is pattern-based, not fixed-line-based
- Validation covers all 4 dataset variants

## Phase Order

1. `phase-0-preflight-backup.md`
2. `phase-1-preexisting-bugfixes.md`
3. `phase-2-gitignore-and-data-migration.md`
4. `phase-3-tracked-moves-and-structure.md`
5. `phase-4-path-rewrites-and-docs.md`
6. `phase-5-verification-and-cutover.md`

## Execution Rules

- Start each phase only after the previous phase passes its exit criteria.
- Keep one commit per phase (or clearly separated sub-commits inside a phase).
- Do not squash data migration + bugfix commits together.
- Stop immediately on unexpected `git status` output and investigate before continuing.
