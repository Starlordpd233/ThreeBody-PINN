# Watchdog Verification Checklist

Tracks per-cell status for the 2026-06-30 verification plan. Update the row as
each task closes. Legend: ⬜ not started · 🟩 PASS · 🟥 FAIL(finding) · ⏭️ covered-elsewhere

## G0 — static & packaging contracts [COMPLETE - one finding F1]
- ⏭️ A1 shellcheck clean (SKIP: shellcheck not installed)
- 🟩 A2 wake-prompt consistency
- 🟥 A3 verdict/exit-code vocab in SKILL.md
- 🟩 A4 watch-loops restore set +e
- 🟩 A5 install drift (repo ↔ canonical bin)
- 🟩 A6 deployed SKILL.md path-rewrite
- 🟩 A7 alt-profile symlink integrity

## G1 — unit logic gaps [COMPLETE]
- 🟩 B1 concurrent claim race (exactly-once)
- 🟩 B2 non-git CWD fails safely  (also satisfies T4.4)
- 🟩 B3 resolver uses CWD not tool-home  (automatable core of T4.2)
- 🟩 B4 claim-dir accumulation + re-wake
- 🟩 B5 disarm tolerates dead pid

## G2 — multi-process integration [COMPLETE]
- 🟩 C1 N-consumer real-process race
- 🟩 C2 mixed arm+push race (tmux stub)
- 🟩 C3 disarm sentinel stands down running watcher (timing)
- 🟩 C4 SIGTERM-during-sleep → DISARMED (TERM trap)
- ⏭️ C5 cross-worktree real linked worktrees (clean/already/conflict-abort) [covered by test_watchdog_xworktree.py]
- 🟩 C6 cross-repo channel isolation  (satisfies T4.3)

## G3 — live single-machine
- ⬜ D1 cross-worktree two-session handoff
- ⬜ D2 real PUSH (real tmux + idle claude pane)
- ⬜ D3 P2 cron under termination contract

## G4 — live global
- ⬜ E1 discovery/load in each profile
- ⬜ E2 foreign-project live within-project handoff
- ⬜ E3 fresh-agent instruction-following rehearsal
- (T4.3 → C6 · T4.4 → B2)

## Capstone
- ⬜ F1 dogfooded A→B run (B runs the watchdog suite)

## Findings (RED cells / live FAILs — surface, do not patch)
| id | cell | severity | summary | status |
|----|------|----------|---------|--------|
| F1 | A3 | HIGH | SKILL.md does not document the PUSHED verdict emitted by wd-push | OPEN |