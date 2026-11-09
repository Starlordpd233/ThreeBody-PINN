---
status: active
purpose: review-findings
created: 2026-06-25
milestone: untracked
phase: two-machine-git-sync
retirement_trigger: revised plan adopted and two-machine sync verified stable on both machines; all findings closed out finding-by-finding
---

# Two-Machine Git Sync Plan — Audit Report

**Date:** 2026-06-25
**Reviewer:** Claude (Opus 4.8), specwork worktree
**Subject:** `PLAN (2).md` — "Two-Machine Git Sync And Setup Plan" (Codex-authored)
**Subject path:** `<home>/Downloads/PLAN (2).md`
**Revised artifact:** same file, rewritten in place (see §7)
**Audit lens:** fitness for **flawless execution by an autonomous agent** that has no human intuition, across three dimensions — Logical Integrity (LI), Execution Clarity (EC), and Operational Resilience (OR).

---

## 1. Scope and method

The plan was audited against the repository's **actual state** (read-only `git` inspection of all worktrees, branches, hooks, and remotes) and against the **governing docs** (`AGENTS.md` / `CLAUDE.md`, `docs/git-guidelines.md`, `.githooks/pre-push`, and the existing `docs/runbooks/migration/exact-state-mac-migration.md`). Every factual premise in the plan was checked against ground truth rather than taken on faith — several did not hold.

## 2. Verdict

The plan's **direction is sound**: GitHub for tracked history, a small archive for ignored runtime state, bulky payloads out-of-band, policy-compliant commits. But **as written it would not execute flawlessly autonomously.** Four **P0** defects would cause a context-free executor to halt, capture only part of the work, or — most dangerously — leave the second machine in a **wrong-but-unflagged** state (a 285-commit-stale `master`, and two entirely-missed worktrees). The revised plan in §7 resolves every P0/P1 and most P2 findings; three items in §8 remain open for user confirmation.

## 3. Repository ground truth (verified 2026-06-25)

- **Three worktrees on three branches:** `/…/3_body_problem` → `master`; `.worktrees/specwork` → `milestone/v1.6`; `.worktrees/trainex` → `track/trainex`.
- `master`: **285 ahead** of `origin/master` (stale `b8b39a44`), **protected**.
- `milestone/v1.6`: **protected**, **no upstream** (never pushed), **has uncommitted work** (7 untracked phase-34 files + a modified `STATE.md`).
- `track/trainex`: **not protected**, **no upstream** (never pushed), **has uncommitted work** (2 untracked r1 files).
- Protected-ref enforcement (`.githooks/pre-push`): direct pushes to `refs/heads/master | main | milestone/*` are blocked.
- Remote: `https://github.com/Starlordpd233/ThreeBodyProblem.git` (private).
- **No Git LFS** in use (`.gitattributes` has zero `filter=lfs` entries).
- `CLAUDE.md` is a **symlink → `AGENTS.md`** (relevant to §6).

## 4. Decisions incorporated (from user, this session)

1. **Scenario:** ongoing two-machine sync (not a one-time migration).
2. **Existing runbook:** reuse `exact-state-mac-migration.md` as a **reference** for archive mechanics; do not duplicate it; build for the continuous-workflow case it does not cover.
3. **Protected branches:** mirror branch + local fast-forward.
4. **Scope:** capture all three worktrees and reproduce the `.worktrees/` layout.
5. **Assumption pending confirmation:** maintain persistent `sync/*` mirror branches long-term (preserves the protected-branch guardrail). Carried into the revised plan as an explicit, flagged assumption.

## 5. Prioritized findings

| ID | Pri | Dim | Finding | Status |
|----|-----|-----|---------|--------|
| P0-1 | P0 | LI/OR | Archive **creation** is undefined — only restore is described | Addressed in revision |
| P0-2 | P0 | LI/EC | "Handoff branch from current state" — source branch/worktree unspecified | Addressed in revision |
| P0-3 | P0 | LI | Receiver never reconciles local `master` → silent 285-commit-stale `master` | Addressed in revision |
| P0-4 | P0 | LI | Two of three worktrees/branches never captured or recreated | Addressed in revision |
| P1-1 | P1 | LI | `milestone/v1.6` is protected — "push workstream branch every commit" is impossible | Addressed in revision |
| P1-2 | P1 | EC | `agent-commit` `GIT_AGENT_ID` / `OWNED_PATHS` values unspecified | Addressed in revision |
| P1-3 | P1 | OR | Clone-into-existing-path precondition unchecked | Addressed in revision |
| P1-4 | P1 | LI/OR | `.venv` portability (path/Python) unhandled, no fallback | Addressed in revision |
| P1-5 | P1 | OR | Secrets audit too narrow (misses modified tracked `.claude/settings.json`) | Addressed in revision |
| P2-1 | P2 | EC | Undefined criteria: "relevance", "logical groups", "PR or leave branch" | Addressed in revision |
| P2-2 | P2 | EC/OR | Hardcoded branch date + no idempotency / rerun guidance | Addressed in revision |
| P2-3 | P2 | OR | Verification checks existence, not content; checksum step has no producer | Addressed in revision |
| P2-4 | P2 | OR | "Stop on divergence" underspecified for an autonomous agent | Addressed in revision |
| P2-5 | P2 | LI | Push-after-every-commit collides with concurrent multi-agent pushes | Addressed in revision |
| P3-1 | P3 | LI | Git-LFS prerequisite is dead weight (repo uses no LFS) | Addressed in revision |
| P3-2 | P3 | EC | "Read AGENTS.md" without noting the `CLAUDE.md` symlink | Addressed in revision |

### P0 — Blocking (failure or silent wrong-state)

**P0-1 · Archive creation is undefined — only restore is specified · LI/OR.**
*Evidence:* The "Ignored State Plan" and Machine-B prompt step 8 tell the receiver to "restore the ignored runtime archive … following the committed manifest/checksum instructions," but **no source-side step builds that archive**, picks a format/tool, generates the manifest or checksums, or names a transfer channel. "Test and Verification" even asserts an "archive checksum check" with nothing producing the checksums.
*Why an autonomous agent fails:* the source agent finishes having produced no archive; the receiver reaches step 8 with nothing to restore and either halts or fabricates a procedure. The entire ignored-state half of the sync silently does not happen.
*Resolution:* revised Part 1 Task 4 fully specifies the build (tar+zstd, `age`-encrypted, explicit include/exclude borrowed from the migration runbook), manifest + `SHA256SUMS`, a `requirements-machineA.txt` `.venv` fallback, and an explicit transfer channel; the receiver verifies checksums **before** extracting.

**P0-2 · "Handoff branch from current state" — source unspecified · LI/EC.**
*Evidence:* three worktrees exist on three branches; "create a handoff branch from current state" never says which.
*Why an autonomous agent fails:* a literal executor cuts the branch from whatever worktree it is invoked in, capturing one line of history and silently dropping the other two tracks.
*Resolution:* the revision drops the single-handoff-branch framing and publishes all three branches explicitly (Tasks 1–3).

**P0-3 · Receiver never reconciles `master` → silent stale master · LI.**
*Evidence:* `master` is 285 ahead of a stale `origin/master` and is protected; Machine-B prompt step 5 only `git switch`es to the handoff branch and never fast-forwards local `master`.
*Why an autonomous agent fails:* the second machine's `master` stays 285 commits behind, and **no checkpoint detects it** — the agent reports success on a wrong state.
*Resolution:* revised Machine-B step 6 fast-forwards local `master` from the `sync/master` mirror **locally** (the hook gates pushes only), then verifies `git rev-parse` equals the recorded source tip.

**P0-4 · Two of three worktrees/branches never captured or recreated · LI.**
*Evidence:* `milestone/v1.6` and `track/trainex` have no upstream (never pushed) and each holds uncommitted work; the plan pushes one handoff branch and never recreates the `.worktrees/` layout.
*Why an autonomous agent fails:* the second machine cannot continue specwork or trainex; their unpushed commits and dirty files never arrive.
*Resolution:* the revision captures all three worktrees' dirty work (Task 2), publishes `track/trainex` directly and `master`/`milestone/v1.6` via mirrors (Task 3), and recreates the worktree layout on Machine B (step 7).

### P1 — High

**P1-1 · `milestone/v1.6` is protected — "push the active workstream branch every commit" is impossible · LI.** The active specwork branch matches the `milestone/*` block; the cadence step is rejected by the hook and an agent may loop, fail, or attempt a forbidden `--no-verify` bypass. *Resolution:* route `milestone/v1.6` through the non-protected `sync/milestone-v1.6` mirror and scope the cadence to non-protected branches.

**P1-2 · `agent-commit` identifiers unspecified · EC.** Governance forbids broad staging and requires explicit owned paths, yet no values are given. *Resolution:* Task 2 supplies a concrete `GIT_AGENT_ID` and per-group `GIT_AGENT_OWNED_PATHS` examples and forbids blanket staging.

**P1-3 · Clone-into-existing-path unchecked · OR.** On an established second machine the target path may already exist; `git clone` aborts and the runbook stalls. *Resolution:* Machine-B step 0 adds an absent/empty-path precondition with a STOP.

**P1-4 · `.venv` portability unhandled · LI/OR.** The plan restores `.venv` with an unstated same-path + same-Python assumption and no fallback; a mismatch yields a broken interpreter with no diagnostic. The migration runbook already solved this and is not referenced. *Resolution:* generate `requirements-machineA.txt`; Machine-B step 9 rebuilds `.venv` when path/version differ, with an import smoke test.

**P1-5 · Secrets audit too narrow · OR.** Only `settings.local.json` is audited, but the master worktree has a **modified tracked** `.claude/settings.json` plus newly-committed `.planning/`/`.claude/` files headed for a push, where secrets are hard to expunge. *Resolution:* Task 2 audits every staged file (tracked `settings.json` included), excludes and surfaces secret-bearing content rather than committing it.

### P2 — Medium

**P2-1 · Undefined decision criteria · EC** — "audit for relevance", "commit in logical groups", "open a PR or leave the branch" give an autonomous agent no rule. *Resolution:* concrete grouping criteria and a default (leave the mirror as the pickup point; no PR).

**P2-2 · Hardcoded branch date + no idempotency · EC/OR** — `…2026-06-24` mismatches the execution date and re-runs create divergent branches. *Resolution:* stable mirror names (`sync/master`, `sync/milestone-v1.6`) and rerun-safe push semantics.

**P2-3 · Verification checks existence, not content · OR** — `git ls-remote --heads` confirms a branch exists, not its tip; the receiver checksum check has no producer (ties to P0-1). *Resolution:* compare tip hashes to recorded source tips; verify checksums before extract.

**P2-4 · "Stop on divergence" underspecified · OR** — *Resolution:* "STOP" is defined = halt, surface, never auto-merge/rebase/force.

**P2-5 · Push-after-every-commit vs. concurrent agents · LI** — same-branch pushes from two agents cause non-fast-forward churn. *Resolution:* scope the cadence and add explicit non-ff handling (STOP + surface).

### P3 — Minor

**P3-1 · Git-LFS prerequisite is dead weight · LI** — repo has zero `filter=lfs` entries. *Resolution:* removed from prerequisites.
**P3-2 · "Read AGENTS.md" without the symlink note · EC** — *Resolution:* the revised prompt notes `CLAUDE.md` is a symlink to `AGENTS.md`, so Claude-based executors are covered.

## 6. Cleared (non-issue, checked for rigor)

**`AGENTS.md` vs `CLAUDE.md` drift — NOT a problem.** `CLAUDE.md` is a symlink to `AGENTS.md`; revising `AGENTS.md` updates both. The plan's choice to edit `AGENTS.md` only is correct and complete.

## 7. Revised plan — what changed

Rewritten in place at `<home>/Downloads/PLAN (2).md`. Major changes:

- Replaced the single "handoff branch" with **explicit per-branch publication of all three worktrees** — `track/trainex` directly, `master`/`milestone/v1.6` via `sync/*` mirrors.
- Added **receiver-side local fast-forward** of `master`/`milestone/v1.6` from the mirrors (fixes the silent stale-master defect) with tip-hash verification.
- Added **worktree-layout recreation** on Machine B.
- **Fully specified the archive build** (format, include/exclude, manifest, `SHA256SUMS`, `.venv` requirements fallback, explicit transfer channel) — not just restore.
- Captured **all three worktrees'** uncommitted work with a concrete `agent-commit` invocation and a **broadened secrets audit**.
- Added **preconditions** (clone path), **error handling** (protected/non-ff rejections, `--ff-only` failures), idempotency, a **content-level verification matrix**, and a **rollback** section.
- Removed the Git-LFS prerequisite; noted the `CLAUDE.md`→`AGENTS.md` symlink.
- Scoped the **push-after-every-commit cadence to non-protected branches** so it never contradicts the protected-ref hook; defined what "STOP" means for an autonomous executor.

## 8. Residual risk / to confirm (remain `open`)

- **Persistent-mirror assumption** — the revision maintains `sync/master` and `sync/milestone-v1.6` long-term. Confirm, or choose the alternative (move active work onto non-protected feature branches and reserve `master`/`milestone/*` for integration).
- **Archive transfer channel** — the revision names an encrypted external drive as the default; confirm the actual secure channel.
- **Policy edit** — the scoped push-cadence change to `git-guidelines.md` / `AGENTS.md` is described as **follow-on work**, not performed here; it must land as its own atomic, policy-compliant commit.

## 9. Closeout (docs lifecycle)

All P0/P1/P2/P3 findings are **addressed-in-revision** (each maps to a resolution in the revised plan). The three §8 items are **`open`** pending user confirmation. Per `docs/README.md`, this report stays `active` until the revised plan is adopted and the sync is verified stable on both machines, at which point finding-by-finding closeout can proceed.
