---
status: active
purpose: design
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  When approved and its decisions land in their canonical homes
  (docs/git-guidelines.md A4, project CLAUDE.md Git-governance recognition,
  .gitignore, scripts/agent-commit, the new overlap-avoidance script/hook, and the
  session-start banner hook).
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
  (a short recognition note), `.gitignore`, `scripts/agent-commit`, a new overlap-avoidance
  script and its warn/auto-declare hook, and a session-start banner hook.
- Once those land, this doc is marked `consumed`, and the git guidelines become the live
  authority for agents and clones.

So: the design **feeds** the git guidelines, but in two steps (design now, policy update during
implementation). The doc itself is not pasted into the guidelines.

**Relationship to prior work.** This refines the 2026-06-17 parallel-agent coordination draft.
It (a) **confirms per-track over per-milestone** isolation (the draft's Open Q#2), (b) **chooses
Option β** for the commit lock — a deliberate change from the draft's α recommendation, in order
to make concurrent commits smoother — (c) **adds an overlap-avoidance dimension** (a shared
"I'm working on this" list plus automatic warn-and-claim) that the draft did not have, and
(d) **adds an enforced session-start banner** as an active navigation guard.

## 1. The goal

Make parallel-agent git work **smooth** — fewer conflicts, less ambiguity, and lower cost when
agents discover overlapping work. This project is **agent-driven**: agents do the work and
commit, while the user opens several terminals (each already in a branch + folder) and spawns
agents inside them. Therefore every mechanism below must be one an **agent can follow
automatically** — not one that depends on the user remembering to run something.

## 2. The decisions

### 2.1 Where each track of work lives (worktrees)

- Each active **track** of work gets its own worktree folder at `.worktrees/<track>/`
  (for example `.worktrees/specwork/`). The set of tracks is **open**: `specwork` and
  `trainex` today; `edl` or others later — each new track gets a worktree on demand.
  ("Track" is the project's established term — see `.claude/rules/repo-map.md` Track Aliases.)
- **EDL note:** EDL is currently a *workflow* under `.planning/research/edl/`, not yet a
  track. It earns its own worktree only if/when it is run as parallel work.
- The **main repo folder stays on `master`** and holds finished/merged work. Cross-cutting
  housekeeping — governance docs, planning notes, CI config — **is** permitted on `master`;
  that is integration work, not track work.
  - **Where milestone planning lives (boundary made explicit):** a milestone's *science* work
    **and its phase-planning** (`.planning/phases/NN/…` for that milestone) live in the owning
    track's worktree on the milestone branch; only **cross-cutting** coordination, governance,
    and CI live on `master`. This very design is cross-cutting, so it correctly lives on `master`.
- **Lifecycle:** a worktree is created when a track starts real work and **removed when the
  track goes dormant** — "dormant" meaning no active or planned sessions for it, a judgement the
  user makes (not automatic, and not "on completion"). Tracks persist across milestones — for
  example `specwork` spans v1.6 → v1.7 in the *same* worktree, just on a new branch.
- **Migration:** move the existing `~/Desktop/3_body_problem-v1.6` → `.worktrees/specwork` via
  `git worktree move` (verified feasible on git 2.54.0; the branch `milestone/v1.6` is unchanged
  by the move). Do this only when the v1.6 worktree is quiescent (no active session inside it).
- **Acknowledges the existing convention:** `.gitignore` already lists `.claude/worktrees/`
  (the folder Claude Code itself uses for its auto-managed worktrees). We use a **separate
  top-level `.worktrees/`** so our manual track worktrees do not collide with the tool's
  auto-generated ones.
- **Sync cadence:** tracks regularly **merge `master`** into their branch (merge, **not**
  rebase — we never rewrite history). This is the guard against drift, i.e. the 2026-05-13
  "agent worked the wrong branch for 5 days, work discarded" failure.

### 2.2 Telling terminals apart (navigation)

- **For the user (passive):** the **status line** at the bottom of each terminal shows the track
  name + milestone + phase, so the user can tell several tabs apart at a glance. No custom code —
  it reuses the existing GSD statusline plus the worktree folder name.
- **For agents (active, enforced):** a **SessionStart hook prints a one-line banner** at the top
  of every session stating the worktree and branch it is in — for example
  `worktree .worktrees/specwork → branch milestone/v1.6 · phase 30`. This is the **enforced,
  automatic** form of the existing "announce your branch at session start" rule: it fires on its
  own, so it does not depend on the agent remembering. It is deliberately minimal — a banner, not
  a launcher and not a branch-mapping system — to keep it simple and self-enforcing.
- **Why this is enough:** the per-track model already removes most of the 2026-05-13 risk
  structurally — each worktree folder is permanently bound to one branch, so an agent no longer
  switches branches inside a worktree (which is how that incident happened). The banner makes the
  "which terminal am I in?" question answer itself at the source; the merge-`master` sync cadence
  (§2.1) is the deeper guard against drift.

### 2.3 Smoother commits (the commit lock)

- **Today:** two agents committing at the same instant → one fails and must retry.
- **Decision:** change `scripts/agent-commit` so the second agent **waits briefly, then
  commits** (bounded wait-and-retry) instead of failing fast. We call this **Option β**.
- **Why β over the draft's α (fail-fast) recommendation:** in an agent-driven repo with many
  concurrent commits, failing-and-retrying wastes agent effort; brief serialization is smoother.
  This is a **deliberate change** from the 2026-06-17 draft, which recommended α.
- **Safety details (so it cannot go wrong):**
  - The lock covers **the commit itself and its hooks** — it is held across the `git commit`
    invocation inside `scripts/agent-commit`. Staging (`git add`) runs *before* that and is
    per-worktree; Option β changes only **whether a waiting agent retries or fails**, not what the
    lock covers, so it opens no new gap.
  - It **waits up to ~5 minutes** — comfortably longer than any real commit (at most a minute or
    two even with heavy hooks) — then reports clearly so the agent can retry, rather than failing
    silently. Poll and stale-floor use the **same ~5-minute figure**, so a waiter never gives up on
    a commit that is still legitimately in progress.
  - While waiting, it **reclaims the lock immediately if the holder's process is gone** (a dead
    holder's lock is safe to take at once). As a backstop for a lock whose holder cannot be
    identified, it also reclaims one older than ~5 minutes — so a real, live commit is never
    interrupted. The ~5-minute figure is overridable.
  - The lock stays **repo-wide** (every worktree shares it) because all worktrees share the same
    underlying git storage — serializing all commits is the safe choice and costs almost nothing.

### 2.4 Not editing each other's files — the shared list + automatic warning (NEW)

This is the main new piece, added because same-file overlap between agents is **regular**.

- **The idea:** a shared "I'm working on this" list — like a sign-up sheet on an office
  whiteboard — that every agent can see.
- **How it works for an agent:**
  - When an agent edits a file, the system **records that claim automatically and warns the agent
    if someone else already holds it** (auto-declare on first edit). The agent never has to
    remember to check *or* to claim — both happen on their own. This is the "guaranteed"
    guarantee, and it is what keeps the mechanism inside the §1 rule ("automatic, not 'remember to
    run something'").
  - Agents can also declare a broader area (a whole folder, a big rebuild) up front with one quick
    command (`scripts/agent-claim <area>`), so others are warned *before* they start.
- **Self-cleaning:** entries fade away after about **2 hours** (time-based: each edit-hook runs as
  a short-lived process, so unlike the commit lock there is no persistent agent process to test for
  liveness — expiry is by age plus explicit release) — so a crashed agent never blocks anyone, and
  forgetting to "un-claim" is harmless. A task that runs longer than ~2 hours simply re-claims on
  its next edit (the same hook refreshes it); the commit-time net below is the hard backstop
  regardless.
- **Second safety net (the hard guarantee — to be built):** at commit time, an agent may only
  stage the paths it declared via `GIT_AGENT_OWNED_PATHS`. So even if a warning were missed, two
  agents cannot silently overwrite each other — it is caught when they commit. *Note (verified
  2026-06-18): today the git-policy hooks block only **broad** `git add`; this per-path ownership
  check does **not** yet exist and is new work in the implementation plan — not pre-existing.*
- **Why it is generic:** the list does not care about specific files. Any agent, any task,
  declares the area it is working in; the rule is always "do not overlap with someone already on
  the list." The same mechanism handles same-file clashes, same-folder work, and big cleanups.
- **Specifics (for the implementer; full detail deferred to the plan):**
  - The list is a **directory of small files, one file per claim** (not one shared file), each
    recording *who · what-area · why · when · process-id*. One file per claim, created atomically,
    means concurrent agents add and drop claims without ever corrupting each other's entries — the
    same discipline the commit lock uses.
  - The directory lives in the **shared git internals folder** — the one place every worktree can
    already see (the same shared spot the commit lock uses), so cross-worktree conflicts are caught
    too. In git terms: under `$(git rev-parse --git-common-dir)/agent-claims/`.
  - A small script `scripts/agent-claim <area>` declares a broader area and consults the list;
    `scripts/agent-release` removes an entry (optional — expiry handles it).
  - The **automatic warning + auto-declare** is a Claude Code hook on edit actions: before an edit
    it warns if the file is already claimed by another agent, and otherwise records this agent's
    own claim. The exact hook event/config is the only piece deferred to the plan.

### 2.5 Big files

- New worktrees do **not** copy the multi-GB simulation data. Untracked outputs live
  per-folder, so they simply do not appear in a fresh worktree; it carries only the smaller
  tracked files.
- **Size note (corrected, measured 2026-06-18):** `reference-code/` is ~387 MB **on disk** but
  only **~104 MB tracked** (the rest is gitignored third-party code); the **whole tracked checkout
  is ~126 MB**, of which `reference-code/` is the bulk. That is modest, so we accept a **full
  tracked checkout** for now (no "sparse"/partial checkout), because partial checkouts risk hiding
  reference material an agent might need. We will revisit if a future track does not need it.
- **Trainex (later):** if a track needs the big data, **link to it from one place** instead of
  copying — and link **only the large output subfolders**, not the small tracked reference files
  (linking the whole `simulation_data/` folder would make git think the reference files were
  deleted).

### 2.6 Governance landing (deferred to the plan)

Once approved, the decisions land in: `docs/git-guidelines.md` A4 (track unit, `.worktrees/`
placement, the overlap rule, the commit-lock behavior, merge-not-rebase), project `CLAUDE.md`
(a recognition note), `.gitignore` (the `.worktrees/` line), `scripts/agent-commit` (the β
behavior), the new overlap-avoidance script with its warn/auto-declare hook, and the
session-start banner hook.

## 3. Open / deferred (explicit, not hidden)

- **EDL as a track:** not yet; becomes one only if run as parallel work.
- **Trainex big-data link:** deferred to when trainex starts.
- **Hook event/config:** auto-declare-on-edit (§2.4) and the session-start banner (§2.2) are
  **decided**; only the exact Claude Code hook event names and wiring are an implementation choice
  for the plan.
- **Sparse checkout:** not now; revisit only if a future track does not need `reference-code/`.
- **GSD workstreams/workspace:** GSD ships `gsd-workstreams`/`gsd-workspace` skills, but they are
  **not** managing worktrees in this repo today (no `.planning/workstreams` or `.planning/workspaces`).
  If they are later adopted to manage worktrees, reconcile this `.worktrees/<track>/` scheme with
  them then; there is no conflict now.

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
3. `scripts/agent-commit`: wait up to ~5 min then report + reclaim-when-holder-is-gone (with a
   ~5-min age backstop); update its messages; update the git-guidelines lock prose to match.
4. New `scripts/agent-claim` / `scripts/agent-release` + the per-claim files under
   `$(git rev-parse --git-common-dir)/agent-claims/`.
5. The **warn-on-edit + auto-declare hook** (the overlap guarantee — not optional).
6. The **session-start banner hook** (the active navigation guard, §2.2).
7. Governance text: `docs/git-guidelines.md` A4 refinement + a recognition line in project
   `CLAUDE.md`.
8. Deferred: trainex big-data link; sparse checkout.

## 6. Verification (acceptance for the plan)

- **Migration:** `git worktree list` shows `.worktrees/specwork → milestone/v1.6`; the main
  worktree `git status` is clean (no `.worktrees/` noise); a commit inside `.worktrees/specwork`
  lands on `milestone/v1.6`.
- **Commit lock:** with the lock held, a second commit **waits then succeeds**; a lock whose
  holder process is gone is **reclaimed**; a live long commit is **not** interrupted.
- **Overlap avoidance:** agent A edits a file and its claim is **recorded automatically**; agent B
  is **warned automatically** when it tries to edit that file; a claim fades after ~2h; at commit,
  an agent cannot stage paths it did not declare.
- **Navigation:** in `.worktrees/specwork`, the status line shows `specwork` + `v1.6 · <phase>`,
  and a new session prints the worktree+branch banner — both with no change to GSD's statusline code.
