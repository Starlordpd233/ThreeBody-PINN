---
status: consumed
purpose: review-findings
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  When the staged corrections are committed, the design and plan docs are marked
  consumed, the owned-paths enforcement wording is corrected to name the
  commit-msg validator, and any follow-up tests for the new scripts are added.
---

# Worktree Placement & Parallel-Agent Concurrency — Implementation Review

**Design:** `docs/work/designs/cross_cutting/parallel-agent-coordination/2026-06-18-worktree-placement-and-concurrency-design.md`  
**Plan:** `docs/work/plans/cross_cutting/parallel-agent-coordination/2026-06-18-worktree-placement-and-concurrency-plan.md`  
**Reviewer:** Claude Code verification gatekeeper  
**Date:** 2026-06-18

## Executive summary

The eight planned tasks are **functionally implemented** in the codebase, but the
implementation is **not fully committed**. A block of final corrections remains
**staged on `master`** and must be committed before the work is complete. In
addition, two lifecycle artifacts (the design doc and the implementation plan)
still carry `status: active` even though their own retirement triggers say they
should be `consumed` once the decisions land. Finally, there is a wording
inaccuracy in the staged governance text about which hook enforces the
owned-paths net.

| Criterion | Verdict | Evidence |
|-----------|---------|----------|
| `.worktrees/` ignored | Pass | `.gitignore` line 41 |
| v1.6 worktree migrated to `.worktrees/specwork` | Pass | `git worktree list` |
| `agent-commit` wait-and-retry lock | Pass | `scripts/agent-commit` lines 25–71; defaults 300s |
| `agent-claim` / `agent-release` board | Pass | `scripts/agent-claim`, `scripts/agent-release`, `scripts/git_policy/agent_claims.py` |
| Warn-on-edit / auto-declare hook | Pass | `.claude/settings.json` PreToolUse matcher + `scripts/git_policy/claim_guard.py` |
| Session-start banner hook | Pass | `.claude/settings.json` SessionStart hook + `scripts/session_banner.sh` |
| Governance text in `docs/git-guidelines.md` and `AGENTS.md` | **Partial** | Staged but uncommitted; one inaccurate enforcement claim |
| Design/plan marked `consumed` | **Fail** | Both still `status: active` |
| All changes committed to `master` | **Fail** | Six files staged, not committed |

## Verification methodology

All checks were run fresh in this session. Commands executed:

- `git status --short --branch` and `git worktree list` — state and worktree inventory.
- `python3 -m unittest tests.git_policy.test_git_policy -v` — existing policy test suite.
- Manual behavior probes for the claims board, claim guard, session banner, and
  commit-lock reclaim logic.
- Source-code read of `scripts/agent-commit`, `scripts/git_policy/agent_claims.py`,
  `scripts/git_policy/claim_guard.py`, `scripts/session_banner.sh`,
  `.claude/settings.json`, `docs/git-guidelines.md`, `AGENTS.md`, and the
  relevant git hooks.

## Detailed findings

### 1. `.gitignore` — PASS

`.gitignore` contains the expected rule at line 40–41:

```gitignore
# Manual per-track worktrees (see docs/git-guidelines.md A4)
.worktrees/
```

`git status --short` from the main repo shows no `.worktrees/` untracked noise.

### 2. Worktree migration — PASS

```text
$ git worktree list
<home>/Desktop/3_body_problem                     729c22ba [master]
<home>/Desktop/3_body_problem/.worktrees/specwork 01683da0 [milestone/v1.6]
```

The `specwork` worktree is on `milestone/v1.6`, matching the design. The main
repo remains on `master`.

### 3. Commit lock — PASS

`scripts/agent-commit` implements Option β exactly:

- Shared lock directory under `$(git rev-parse --git-common-dir)/agent-commit.lock`.
- Defaults: `AGENT_COMMIT_LOCK_TIMEOUT=300`, `AGENT_COMMIT_LOCK_STALE=300`.
- Reclaims only when the holder PID is gone **or** the lock exceeds the stale
  floor; atomic `mv` steal prevents two waiters from both reclaiming.
- Trap removes the lock on exit.

The logic was verified by source inspection. A full live commit test could not
be run cleanly because unrelated staged changes (see §6) caused the
owned-paths validator to reject a probe commit, which is itself evidence that
the hard owned-paths net is active.

### 4. Claims board — PASS

`scripts/agent-claim`, `scripts/agent-release`, and
`scripts/git_policy/agent_claims.py` exist and are executable. Manual test:

```text
$ GIT_AGENT_ID=A scripts/agent-claim simulation_data/foo.py "edit foo"
$ GIT_AGENT_ID=B python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py
claim conflict: 'simulation_data/foo.py' is held by A since 18:48
B sees exit=3
$ GIT_AGENT_ID=A python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py
A sees exit=0
$ GIT_AGENT_ID=A scripts/agent-release simulation_data/foo.py
$ GIT_AGENT_ID=B python3 scripts/git_policy/agent_claims.py check simulation_data/foo.py
after release exit=0
```

Expiry defaults to 7200s (`AGENT_CLAIM_EXPIRY`), matching the ~2-hour target.

### 5. Warn-on-edit / auto-declare hook — PASS

`scripts/git_policy/claim_guard.py` is registered in `.claude/settings.json`
under the `Edit|Write|MultiEdit` PreToolUse matcher. Manual probe:

```text
$ PAY='{"tool_input":{"file_path":".../simulation_data/bar.py"}}'
$ echo "$PAY" | GIT_AGENT_ID=A python3 scripts/git_policy/claim_guard.py; echo "A exit=$?"
A exit=0
$ echo "$PAY" | GIT_AGENT_ID=B python3 scripts/git_policy/claim_guard.py; echo "B exit=$?"
claim warning: 'simulation_data/bar.py' overlaps a claim held by A ...
B exit=0
```

The hook is advisory (always exits 0), as designed.

### 6. Session-start banner — PASS

`scripts/session_banner.sh` is registered in `.claude/settings.json` under
`SessionStart`. Running it directly:

```text
$ bash scripts/session_banner.sh
worktree 3_body_problem -> branch master  (<home>/Desktop/3_body_problem)
```

The session-start message appeared at the top of this Claude Code session.

### 7. Governance text — PARTIAL

The canonical policy updates are **present and correct in content** but **not
committed**. The staged diff adds:

- `docs/git-guidelines.md` §"Per-track worktrees and overlap avoidance":
  worktree placement, merge-not-rebase, commit-lock behavior, claims board, and
  owned-paths net.
- `AGENTS.md` concurrent-agents paragraph: a single recognition line pointing to
  `docs/git-guidelines.md`.

However, the staged `docs/git-guidelines.md` says the owned-paths net is
"enforced by the pre-commit validator". That is **incorrect**. The enforcement
lives in the **commit-msg** hook, which calls
`scripts/git_policy/validate_commit_msg.py` (`validate_agent_owned_paths`). The
staged change to `scripts/git_policy/validate_staged_paths.py` actually
**removes** the duplicate owned-paths check from the pre-commit hook, so the
canonical text must name the commit-msg validator instead.

The design doc itself correctly identifies the commit-msg hook as the
enforcement point; the guidelines drift from the design.

### 8. Design doc and plan still `status: active` — FAIL

Both frontmatter blocks still say `status: active`. Their own
`retirement_trigger` fields state they should become `consumed` once the
decisions land in their canonical homes. The decisions have landed (or are
staged to land), so the status should be updated and the files should point
readers to `docs/git-guidelines.md` and the shipped scripts.

### 9. Staged but uncommitted changes — FAIL

At the time of review, the following files are modified and staged on `master`
but not committed:

- `AGENTS.md`
- `docs/git-guidelines.md`
- `docs/work/designs/cross_cutting/parallel-agent-coordination/2026-06-18-worktree-placement-and-concurrency-design.md`
- `docs/work/plans/cross_cutting/parallel-agent-coordination/2026-06-18-worktree-placement-and-concurrency-plan.md`
- `scripts/git_policy/validate_staged_paths.py`

The prior agent's commit history contains commits for each task, but the final
policy corrections and doc reconciliations remain in the index. This means the
"live" `HEAD` version of the governance text still describes the old fail-fast
lock and omits the per-track worktree rules.

### 10. Test coverage gap

`tests/git_policy/test_git_policy.py` covers commit-message validation, staged
artifact blocking, and the Bash command guard. It does **not** cover:

- `agent-commit` lock acquisition, waiting, and reclaim.
- `agent_claims.py` claim / conflict / expiry / release behavior.
- `claim_guard.py` auto-declare and warn-on-edit behavior.
- `session_banner.sh` output.

The existing 27 tests pass:

```text
$ python3 -m unittest tests.git_policy.test_git_policy -v
Ran 27 tests in 0.663s
OK
```

## Recommendations

1. **Commit the staged block** as the final governance/closure commit, with the
   correct owned-paths wording fixed first.
2. **Correct `docs/git-guidelines.md`** so it says the owned-paths net is
   enforced by the **commit-msg validator** (`validate_commit_msg.py`), not the
   pre-commit validator.
3. **Mark the design doc and implementation plan `status: consumed`** and add a
   pointer to `docs/git-guidelines.md`.
4. **Add focused tests** for the new scripts to close the coverage gap:
   - Lock reclaim with a dead PID and a stale lock.
   - Waiter succeeds after a live holder releases the lock.
   - Claims board conflict, self-claim, release, and expiry.
   - Claim guard warning and auto-declare from a synthetic PreToolUse payload.
   - Session banner output regex.
5. **Verify the commit** with `git status --short --branch` showing a clean tree.

## Additional finding: worktree-specific Claude Code settings

The project ships its Claude Code hooks in the tracked `.claude/settings.json`.
Because each worktree checks out its branch's version of that file, hooks do not
automatically propagate to worktrees whose branches have not merged `master`:

- **Main repo (`master`):** `.claude/settings.json` contains the new
  `SessionStart` banner hook and the `Edit|Write|MultiEdit` PreToolUse claim
  guard. ✓
- **`.worktrees/specwork` (`milestone/v1.6`, HEAD `01683da0`):**
  `.claude/settings.json` is an older revision with **only** the Bash PreToolUse
  guard. It has **neither** the session-start banner **nor** the warn-on-edit
  claim guard. Verified by direct inspection of the file in the worktree.
- **Root cause:** `milestone/v1.6` has not yet merged the `master` commits that
  introduced the banner/claim hooks and the `scripts/session_banner.sh` script.
  `git merge-base --is-ancestor 6a720fe0 HEAD` in the specwork worktree returns
  false.

**Consequence:** agents working in `.worktrees/specwork` do **not** receive the
session-start banner or the automatic edit warnings/auto-declares. The hard
commit-time owned-paths net and the `agent-commit` lock still work because those
live in `scripts/` (shared git object database) and `core.hooksPath` points to
`.githooks`, but the two *Claude-Code-specific* soft guards are absent there
until the branch merges `master`.

## Risk assessment

- **HIGH**: The staged-but-uncommitted state means the canonical policy and
  design reconciliation are not durable in git history. A reset or accidental
  unstage would lose the corrections.
- **HIGH**: The specwork worktree is missing the new Claude Code hooks because
  `milestone/v1.6` has not merged `master`. The design's active navigation and
  overlap-warning guards are therefore not active for specwork agents yet.
- **MEDIUM**: The "pre-commit validator" wording in `docs/git-guidelines.md`
  will mislead agents about where the owned-paths check happens.
- **LOW**: Missing unit tests for the new scripts; the manual probes in this
  review provide interim confidence.
