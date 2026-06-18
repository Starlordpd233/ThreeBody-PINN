---
status: active
purpose: design
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  When approved and its decisions land in their canonical homes
  (docs/git-guidelines.md A4, project CLAUDE.md Git-governance recognition,
  .gitignore, scripts/agent-commit, and the new overlap-avoidance script/hook).
  At that point set status to consumed and point readers to those targets.
---

# Worktree Placement & Parallel-Agent Concurrency — Design

**Status: DESIGN ONLY.** No code, `.gitignore`, `scripts/agent-commit`, worktree, or hook
changes happen until the implementation plan derived from this doc is approved and executed.
This document records decisions and their rationale. It is written in plain language first;
implementation specifics are called out separately so a non-specialist can follow the design
without prior familiarity with git internals or Claude Code tooling.

## 0. What this doc is, and how it relates to the git guidelines

This is the **design** — it records what we decided and why, for making parallel-agent git
work smooth. It is the **input** that the canonical git guidelines will be updated *from*,
once approved. Concretely:

- This doc stays here as the design record.
- The decisions transfer into: `docs/git-guidelines.md` (the policy), project `CLAUDE.md`
  (a short recognition note), `.gitignore`, `scripts/agent-commit`, and a new overlap-avoidance
  script (+ optional hook).
- Once those land, this doc is marked `consumed`, and the git guidelines become the live
  authority for agents and clones.

So: the design **feeds** the git guidelines, but in two steps (design now, policy update during
implementation). The doc itself is not pasted into the guidelines.

**Relationship to prior work.** This refines the 2026-06-17 parallel-agent coordination draft.
It (a) **confirms per-track over per-milestone** isolation (the draft's Open Q#2), (b) **chooses
Option β** for the commit lock — a deliberate change from the draft's α recommendation, in order
to make concurrent commits smoother — and (c) **adds an overlap-avoidance dimension** (a shared
"I'm working on this" list plus an automatic warning) that the draft did not have.

## 1. The goal

Make parallel-agent git work **smooth** — fewer conflicts, less ambiguity, and lower cost when
agents discover overlapping work. This project is **agent-driven**: agents do the work and
commit, while the user opens several terminals (each already in a branch + folder) and spawns
agents inside them. Therefore every mechanism below must be one an **agent can follow
automatically** — not one that depends on the user remembering to run something.

## 2. The decisions

### 2.1 Where each stream of work lives (worktrees)

- Each active **stream** of work gets its own worktree folder at `.worktrees/<stream>/`
  (for example `.worktrees/specwork/`). The set of streams is **open**: `specwork` and
  `trainex` today; `edl` or others later — each new stream gets a worktree on demand.
- **EDL note:** EDL is currently a *workflow* under `.planning/research/edl/`, not yet a
  stream. It earns its own worktree only if/when it is run as parallel work.
- The **main repo folder stays on `master`** and holds finished/merged work. Cross-cutting
  housekeeping — governance docs, planning notes, CI config — **is** permitted on `master`;
  that is integration work, not stream work.
- **Lifecycle:** a worktree is created when a stream starts real work and **removed when the
  stream goes dormant** (not "on completion"). Streams persist across milestones — for example
  `specwork` spans v1.6 → v1.7 in the *same* worktree, just on a new branch.
- **Migration:** move the existing `~/Desktop/3_body_problem-v1.6` → `.worktrees/specwork` via
  `git worktree move` (verified feasible on git 2.54.0; the branch `milestone/v1.6` is unchanged
  by the move). Do this only when the v1.6 worktree is quiescent (no active session inside it).
- **Acknowledges the existing convention:** `.gitignore` already lists `.claude/worktrees/`
  (the folder Claude Code itself uses for its auto-managed worktrees). We use a **separate
  top-level `.worktrees/`** so our manual stream worktrees do not collide with the tool's
  auto-generated ones.
- **Sync cadence:** streams regularly **merge `master`** into their branch (merge, **not**
  rebase — we never rewrite history). This is the guard against drift, i.e. the 2026-05-13
  "agent worked the wrong branch for 5 days, work discarded" failure.

### 2.2 Telling terminals apart (navigation)

- The **status line** at the bottom of each terminal shows the stream name + milestone + phase,
  so the user can tell several tabs apart at a glance. No custom code — it reuses the existing
  GSD statusline plus the worktree folder name.
- **For agents:** the prevention layer is the **existing session-start rule** ("announce which
  branch/worktree you are on when you start"). We are **not** building a user-run launcher,
  because the project is agent-driven and the user does not drive commits. (A status line
  surfaces state *after* a terminal is open; the agent's own session-start check is what
  prevents mistakes at the source.)

### 2.3 Smoother commits (the commit lock)

- **Today:** two agents committing at the same instant → one fails and must retry.
- **Decision:** change `scripts/agent-commit` so the second agent **waits briefly, then
  commits** (bounded wait-and-retry) instead of failing fast. We call this **Option β**.
- **Why β over the draft's α (fail-fast) recommendation:** in an agent-driven repo with many
  concurrent commits, failing-and-retrying wastes agent effort; brief serialization is smoother.
  This is a **deliberate change** from the 2026-06-17 draft, which recommended α.
- **Safety details (so it cannot go wrong):**
  - The lock already covers staging + commit + hooks (it is held across the whole commit step),
    so this change does **not** open any new gap in what is protected.
  - It **polls for up to ~2 minutes**: if the other commit finishes in that window, this one
    proceeds; if still busy after ~2 minutes it reports clearly (and the agent can retry) rather
    than failing silently.
  - A lock is **reclaimed** only when **both** hold: its age exceeds **~5 minutes** *and* the
    holder's process no longer exists — so a real, live commit is never interrupted. The ~5-minute
    floor is well beyond any real commit (sub-second to a couple of minutes) and is overridable.
  - The lock stays **repo-wide** (every worktree shares it) because all worktrees share the same
    underlying git storage — serializing all commits is the safe choice and costs almost nothing.

### 2.4 Not editing each other's files — the shared list + automatic warning (NEW)

This is the main new piece, added because same-file overlap between agents is **regular**.

- **The idea:** a shared "I'm working on this" list — like a sign-up sheet on an office
  whiteboard — that every agent can see.
- **How it works for an agent:**
  - When an agent is about to edit a file someone else has already claimed, the system **warns
    it automatically**. The agent does not have to remember to check — this is the
    "guaranteed" guarantee.
  - Agents can also declare a broader area (a whole folder, a big rebuild) with one quick
    command, so others are warned *before* they start.
- **Self-cleaning:** entries fade away after about **2 hours**, or sooner if the holder's process
  is gone — so a crashed agent never blocks anyone, and forgetting to "un-claim" is harmless.
- **Second safety net (unchanged):** at commit time, an agent may only stage the paths it
  declared. So even if a warning were missed, two agents cannot silently overwrite each other —
  it is caught when they commit.
- **Why it is generic:** the list does not care about specific files. Any agent, any task,
  declares the area it is working in; the rule is always "do not overlap with someone already on
  the list." The same mechanism handles same-file clashes, same-folder work, and big cleanups.
- **Specifics (for the implementer; full detail deferred to the plan):**
  - The list is one text file, one line per claim: *who · what-area · why · when · process-id*.
  - It lives in the **shared git internals folder** — the one place every worktree can already
    see (the same shared spot the commit lock uses), so cross-worktree conflicts are caught too.
    In git terms: under `$(git rev-parse --git-common-dir)/agent-claims/`.
  - A small script `scripts/agent-claim <area>` declares and consults; `scripts/agent-release`
    removes an entry (optional — expiry handles it).
  - The **automatic warning** is a Claude Code hook that watches edit actions and checks the
    list. Whether it also auto-declares on first edit is an implementation choice for the plan.

### 2.5 Big files

- New worktrees do **not** copy the multi-GB simulation data. Untracked outputs live
  per-folder, so they simply do not appear in a fresh worktree; it carries only the smaller
  tracked files.
- **Size note (corrected):** `reference-code/` is ~387 MB **on disk**; the tracked subset is
  smaller. Either way it is modest, so we accept a **full tracked checkout** for now (no
  "sparse"/partial checkout), because partial checkouts risk hiding reference material an agent
  might need. We will revisit if a future stream needs neither.
- **Trainex (later):** if a stream needs the big data, **link to it from one place** instead of
  copying — and link **only the large output subfolders**, not the small tracked reference files
  (linking the whole `simulation_data/` folder would make git think the reference files were
  deleted).

### 2.6 Governance landing (deferred to the plan)

Once approved, the decisions land in: `docs/git-guidelines.md` A4 (stream unit, `.worktrees/`
placement, the overlap rule, the commit-lock behavior, merge-not-rebase), project `CLAUDE.md`
(a recognition note), `.gitignore` (the `.worktrees/` line), `scripts/agent-commit` (the β
behavior), and the new overlap-avoidance script (+ optional hook).

## 3. Open / deferred (explicit, not hidden)

- **EDL as a stream:** not yet; becomes one only if run as parallel work.
- **Trainex big-data link:** deferred to when trainex starts.
- **Automatic-warning hook mechanics:** the design says "warn on edit"; the exact hook wiring
  (and whether it also auto-declares on first edit) is an implementation choice for the plan.
- **Sparse checkout:** not now; revisit only if a future stream does not need `reference-code/`.

## 4. Risks accepted

- The automatic warning may occasionally false-alarm — acceptable because it only **warns**
  (never blocks); it costs a glance.
- The shared list is **advisory, not a hard block** — by design (hard blocks add friction). The
  commit-time net is the hard guarantee against silent loss.
- Disk-wide tools (backups, Finder) still see nested worktrees as duplicate bytes — accepted
  for the containment benefit.

## 5. How this lands — input to the implementation plan

The change set (for the later plan):
1. `.gitignore`: add `.worktrees/`.
2. Migrate the v1.6 worktree → `.worktrees/specwork` via `git worktree move`; verify
   `git worktree list`, branch unchanged, and that a commit inside lands on `milestone/v1.6`.
3. `scripts/agent-commit`: bounded wait-and-retry + reclaim-only-when-holder-is-gone; update
   its messages; update the git-guidelines lock prose to match.
4. New `scripts/agent-claim` / `scripts/agent-release` + the shared list location.
5. Optional: the automatic-warning hook.
6. Governance text: `docs/git-guidelines.md` A4 refinement + a recognition line in project
   `CLAUDE.md`.
7. Deferred: trainex big-data link; sparse checkout.

## 6. Verification (acceptance for the plan)

- **Migration:** `git worktree list` shows `.worktrees/specwork → milestone/v1.6`; the main
  worktree `git status` is clean (no `.worktrees/` noise); a commit inside `.worktrees/specwork`
  lands on `milestone/v1.6`.
- **Commit lock:** with the lock held, a second commit **waits then succeeds**; a lock whose
  holder process is gone is **reclaimed**; a live long commit is **not** interrupted.
- **Overlap avoidance:** agent A claims a file; agent B is **warned automatically** when it tries
  to edit that file; a claim fades after ~2h; at commit, an agent cannot stage paths it did not
  declare.
- **Status line:** in `.worktrees/specwork`, the status line shows `specwork` + `v1.6 · <phase>`
  with no code change.
