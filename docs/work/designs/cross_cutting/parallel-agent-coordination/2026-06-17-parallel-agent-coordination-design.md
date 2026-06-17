---
status: active
purpose: design
created: 2026-06-17
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  When the design is approved and its content is split into canonical homes
  (docs/git-guidelines.md, project CLAUDE.md Git-governance section, the watchdog
  skill under .claude/skills/, and the .live-monitor/ spine build). This file is a
  review draft; once approved content has landed in those targets, set status to
  consumed and point readers there.
---

# Parallel-Agent Coordination — Design Review (Draft, Not Applied)

**Status:** DESIGN ONLY. This document edits **nothing** in `docs/git-guidelines.md`,
project `CLAUDE.md`, the `.live-monitor/` spine, or any hook/script. It exists so the
design can be verified end to end before any critical change lands in the codebase.

**What this document captures:** everything produced this session across two related
systems for coordinating parallel Claude Code sessions on one repository:

- **Part A — Parallel-agent Git guidelines.** Three new guideline families that extend
  `docs/git-guidelines.md` and are recognized at the agent level in `CLAUDE.md`.
- **Part B — Cross-session watchdog.** A portable skill that lets one session signal
  "my work is done" so a dependent session can safely start. Design is captured here;
  build is **parked** pending Part A.

**How to read:** Sections 1–2 frame the shared problem. Part A (Sections A1–A7) is the
priority deliverable. Part B (Sections B1–B8) is documented for completeness but not
yet approved for build. Section 4 lists every decision the user has locked this session.
Section 5 lists open questions for the end-to-end review.

---

## 1. The Setting

- One repository: `<home>/Desktop/3_body_problem`, currently branch `milestone/v1.5`.
- Multiple Claude Code sessions run in **separate terminal tabs** against the same repo.
- A single commit lock (`scripts/agent-commit`) serializes writes today.
- In practice the repo uses **one shared worktree**; `docs/git-guidelines.md` already
  says to "prefer separate worktrees and branches" but this is not followed (Section A2).

## 2. The Two Failure Classes (Shared Root, Different Layers)

| Class | Question it answers | Layer | Part |
|---|---|---|---|
| **Structural** | "Can two agents touch overlapping work without colliding?" | Always-on Git behavior + isolation | A |
| **Temporal** | "Is agent A's work **done yet**, so agent B can start?" | On-demand coordination signal | B |

Both share **Git** as the governing layer: Part A defines the structural rules; Part B's
done-signal **anchors on Git commits**, which Part A makes reliable. This is why they are
presented together.

---

# PART A — Parallel-Agent Git Guidelines

> **Priority deliverable.** Generic (GSD appears as an example only). Lands in
> `docs/git-guidelines.md` (detail) + a concise recognition rule in project `CLAUDE.md`.

## A1. What Exists Today (verbatim)

The canonical policy is `docs/git-guidelines.md`. The relevant current sections:

**"Concurrent Agent Work" (`docs/git-guidelines.md:111-130`):**

```text
For Claude Code CCP or any multi-agent setup, prefer separate worktrees and
branches for independent agents. If agents share one worktree, they must still
declare disjoint owned paths and commit through `scripts/agent-commit`.

Rules for concurrent agents:
- Prefer one agent per worktree/branch for independent work.
- Declare owned paths before editing and before committing.
- Stage only owned paths.
- Re-run git status --short --branch, git diff --cached, and relevant
  unstaged diffs immediately before commit.
- If another agent commits first, re-check the branch and staged diff before committing.
- Never alter another agent's staged or unstaged work unless explicitly assigned.

`scripts/agent-commit` serializes commits with a repository-local lock. If the
lock is held, wait or retry after the other commit finishes.
```

**Worktree definition (`docs/git-guidelines.md:22-23`):**

```text
- Worktree: a separate checkout of the same repository, useful when multiple
  agents work at the same time.
```

**`scripts/agent-commit` lock behavior (`scripts/agent-commit:23-28`):**

```bash
lock_dir="$common_dir/agent-commit.lock"
if ! mkdir "$lock_dir" 2>/dev/null; then
  echo "git policy: another agent commit is in progress; retry after the lock clears: $lock_dir" >&2
  exit 1
fi
trap 'rmdir "$lock_dir" 2>/dev/null || true' EXIT
```

## A2. The Gap — Why the Existing Rule Is Ignored

Three concrete defects in the current text drive every conflict the user observed:

1. **"Worktrees and branches" treats them as interchangeable — they are not.**
   A branch is a commit pointer; a worktree is a separate **working directory**. Two agents
   on **different branches in the same worktree** are *not* isolated: a worktree holds exactly
   one checked-out state, so they clobber each other's checkout or must serialize. True
   parallel isolation requires **different worktrees** (independent working dirs, each on its
   own branch, sharing one `.git`). The current text's "branch per agent" advice is inert on a
   single-worktree repo.

2. **The repo runs one shared worktree.** `git worktree list` shows one entry. The rule says
   "prefer separate worktrees" but nothing operationalizes it, so it is never followed — which
   is exactly why the milestone-close quartet collided.

3. **The lock doc/code contract contradicts itself.** `docs/git-guidelines.md:128-129` promises
   the lock will **"wait or retry,"** but `scripts/agent-commit:24-27` **exits 1 (fail-fast)** on
   contention. An agent following the doc will not retry; an agent reading the code is surprised.

The three new guideline families below close these defects.

## A3. Family 1 — Conflict Taxonomy + Pre-Flight Dependency Check

**A3.1 Four conflict classes** (A has two sub-flavors):

| Class | Name | Example | Resolution |
|---|---|---|---|
| **A1** | Destructive overlap | Agent X deletes/moves a file agent Y is reading | **Must sequence.** No guideline can make this safe concurrently. |
| **A2** | Producer/consumer edge | `audit-milestone` *produces* the audit file `milestone-summary` *reads* | **Must sequence** by dependency order (audit → summary). |
| **B** | Shared-file concurrent edit | Two agents both mutate `.planning/STATE.md` | **Guidelines help:** append-only / single-mutator / accept the commit lock. |
| **C** | Incidental commit race | Two independent agents, disjoint files, both commit at once | **Retry** — the commit lock handles it; re-check and re-commit. |
| **D** | Read-during-write staleness | Agent B reads a file mid-edit by agent A | **Re-read** before acting; treat as stale. |

**A3.2 Pre-flight dependency check (the core rule).** Before starting concurrent work, each
agent declares three sets for its task:

- **R** — files/dirs it will **read** (and depend on being current).
- **W** — files/dirs it will **write/create**.
- **D** — files/dirs it will **delete or move**.

For every pair of concurrent agents, an overlap in **(W∪D) of one × (R∪W∪D) of the other**
forces sequencing (Classes A1/A2) or partitioning (Class B). Only fully disjoint sets may run
unsynchronized (Class C, retried on lock contention). This check is the mechanical answer to
"is this conflict GSD-sequential or genuinely parallelizable?" — the milestone-close quartet
is **A2/B across shared `.planning/` state**, so it is inherently sequential, not a race.

**A3.3 Example applied (GSD milestone-close quartet).** Required order is
`audit → (extract ∥ summary) → complete`. Three of four mutate `.planning/STATE.md`
(Class B surface); `complete-milestone` is destructive (`git rm .planning/REQUIREMENTS.md`,
archive moves) and reads everything the others wrote (Class A1/A2). The "conflict" the user
saw was the system working correctly — these must serialize. The guideline makes that explicit
instead of discovered at collision time.

## A4. Family 2 — Isolation Decision Rule (One Worktree per Active Track)

This is the user's proposed new guideline, judged and scoped this session.

**A4.1 Judgment: sound, with two corrections.**

- *Correction 1 — worktree, not branch.* For "undisturbed by other work," branches are
  necessary but **not sufficient**. Only **different worktrees** isolate working directories.
  The phrase "branch or worktree or whatever" collapses to **worktree**.

- *Correction 2 — scoped decision rule, not a blanket mandate.* A blanket "always isolate"
  would *hurt* this repo: coordinated tasks that share live state (sequential GSD phases, the
  milestone-close pipeline, gap-register/ROADMAP/STATE work) *must* coordinate and would merely
  diverge `STATE.md` (already fragile) in separate worktrees.

**A4.2 The rule.**

| Work type | Mechanism | Rationale |
|---|---|---|
| **Distinct, long-running unit** (new milestone; specwork vs trainex tracks; independent spike) | **Own worktree** | No live shared-state coupling → isolation removes edit friction entirely |
| **Coordinated, shared-state tasks within one unit** (sequential GSD phases; close-out pipeline; shared planning files) | **Shared worktree + owned-path partitioning + commit lock** | Must coordinate over live shared state; separate worktrees only diverge it |

**A4.3 Model: one worktree per active track.** The repo already has named tracks
(`specwork`, `trainex`) plus per-milestone work. Each **active track** gets its own worktree;
agents on the same track share it and partition owned paths; agents on different tracks never
touch each other's files. The user's "new milestone" trigger generalizes to "new/distinct track."

**A4.4 The five operational costs the rule must address** (without these, the rule is ignored
again — same fate as today's "prefer separate worktrees"):

1. **Shared planning state** (`.planning/STATE.md`, `ROADMAP`, `REQUIREMENTS`, gap registers)
   has a single home on the integration worktree. Track worktrees rebase it frequently; never
   let it diverge silently.
2. **Bulky payloads** (`simulation_data/`) are **shared via symlink, not duplicated** per
   worktree (the migration runbook already excludes these — make that explicit policy).
3. **Build/env state** (venv, `node_modules`, Brutus build) — shared or rebuilt, never copied.
4. **Integration cadence** — track worktrees rebase onto the integration branch regularly
   (daily / before completion) so merges stay small. This is the direct prevention for the
   2026-05-13 "5-day divergence, work discarded" incident the Git-governance section exists to stop.
5. **Lifecycle** — create the worktree on track start, remove it on completion (the
   `EnterWorktree`/`ExitWorktree` tooling already exists). No stale worktrees.

## A5. Family 3 — Reconcile the Commit-Lock Doc/Code Gap

`docs/git-guidelines.md:128-129` says the lock **waits or retries**; `scripts/agent-commit:24-27`
**fails fast (exit 1)** on contention. One of them must change so the contract an agent reads
matches the contract it executes. Two options (the user picks at apply time):

- **Option α (doc follows code):** rewrite the guideline to say the lock **fails fast**; the
  committing agent must re-check status, staged diff, and HEAD, then retry. This matches current
  behavior and the existing "if another agent commits first, re-check before committing" rule.
- **Option β (code follows doc):** add bounded retry-with-backoff to `scripts/agent-commit` so it
  waits briefly for the lock before failing. More convenient, but a retrying lock widens the
  TOCTOU window (the lock wraps only the commit write, not staging/editing).

**Recommendation: Option α** (doc follows code). It is honest about current behavior, requires
no code change, and keeps the lock's critical section minimal.

> Note: even Option α leaves a **known TOCTOU gap** — the lock wraps the commit write only, not
> staging or editing, and does not re-validate the staged set against post-lock HEAD. Family 1's
> pre-flight check (A3.2) and "re-check before committing" cover this at the behavioral layer;
> fully closing it mechanically is out of scope for these guidelines and would be a hook change.

## A6. Enforcement — Soft Now, Hard Hook Offered Later

Per the user's global CLAUDE.md, instruction files are **behavioral, not deterministic** — an
agent *can* still drift. "Follow STRICTLY" therefore has two layers:

- **Soft (do now):** a concise, prominent rule in project `CLAUDE.md`'s Git-governance section
  that names the trigger, the action (**worktree, not branch**), and the five operational costs,
  pointing to `docs/git-guidelines.md` for detail. This makes agents recognize and intend to
  follow it. Covers most cases. **User decision this session: soft now.**
- **Hard (offered later):** a hook or wrapper that actually blocks/redirects (e.g., detect "new
  track starting on the shared integration tree" and prompt). This makes "strictly" literally
  true. **User decision this session: hard hook offered later, not built now.**

## A7. Where Each Family Lands Upon Approval (the diff plan, not applied)

| Family | Target file | Nature |
|---|---|---|
| 1 — taxonomy + pre-flight check | `docs/git-guidelines.md` "Concurrent Agent Work" | New subsection |
| 2 — isolation rule + 5 costs | `docs/git-guidelines.md` "Concurrent Agent Work" + new "Worktree Isolation per Track" subsection | New subsection + tightened existing text ("worktree, not branch") |
| 3 — lock doc/code reconciliation | `docs/git-guidelines.md:128-129` (Option α) | Wording fix |
| Recognition pointer (all three) | project `CLAUDE.md` Git-governance section | Concise rule + pointer |

All generic; GSD is example-only. **Nothing in this Part is applied until the user approves
this review.**

---

# PART B — Cross-Session Watchdog

> **Design captured; build parked** pending Part A. The user reprioritized this session to do
> the Git guidelines first. The watchdog design below is reconstructed from this session's
> investigation (five subagents) and the prior Codex conversation that produced the spine.

## B1. Goal and the False-Positive Problem

A "watchdog" lets a **producer** session (agent A) signal "my work is done" so a **consumer**
session (agent B), which is waiting, can safely start dependent work.

The hard case is the GSD **plan** phase: the agent first writes planning-artifact files to disk,
then `gsd-plan-checker` runs a Check→Revise→Escalate loop (up to 3 iterations). So **"the plan
files exist on disk" is a false-positive done signal** — revision may still be in flight. The
watchdog needs a rigorous, unambiguous completion marker.

## B2. The Universal Phase-Done Signal Already Exists: the Git Commit

Investigation this session established the reliability ranking of GSD phase-done signals:

1. **(Most reliable) The atomic phase-completion commit.** GSD `execute-phase` closes a phase
   with one commit, e.g. `verify(NN): complete/close phase NN` (pattern seen as `verify(27)`,
   `verify(28)`), staging `ROADMAP.md`, `STATE.md`, `REQUIREMENTS.md`, and the phase
   `*-VERIFICATION.md`. A commit is durable, ordered, and unambiguous.
2. **The `ROADMAP.md` row `Complete` transition** — the most reliable *content* signal.
3. **Phase directory artifact set** — reliable but noisy mid-phase (files appear before done).
4. **(Unreliable) `.planning/STATE.md`.** Structurally noisy: the `stateReplaceFieldIfTemplate`
   invariant preserves stale prose, and `state.record-session` touches no status fields. Not a
   safe done signal.

**Conclusion:** the Git commit is already the universal, portable "this phase is done" signal.
The watchdog's job is to **bridge a commit into a wake-up another session can consume**, not to
re-derive done-ness from files.

## B3. Layered Architecture

| Layer | Responsibility | Status |
|---|---|---|
| **L0** | Atomic `mkdir`-lock primitive (same pattern `agent-commit` uses) | Pattern exists in repo |
| **L1** | The `.live-monitor/` channel spine — disk-backed message delivery | **Designed w/ Codex; not yet built** |
| **L2** | Done-signal + consumer-side staleness gate (the new core) | **Designed this session; not built** |
| **L3** | GSD adapter (optional, project-specific) | **Conceptual; not built** |
| **L4** | File-conflict guidelines = Part A of this document | **Designed; lands first** |

## B4. The `.live-monitor/` Spine (L1) — Design from the Codex Conversation

- Gitignored on-disk message channels under `.live-monitor/channels/<name>/messages/`.
- **Append-only**, **atomic publish** (write temp file, then `rename`), so a consumer never reads
  a half-written message.
- **Consumer cursors** so a polling session reads only new messages.
- **90-second cron** polls and runs `lm-check`, returning **IDLE** or **WAKE**.
- On-disk (not a network service) on purpose: survives across terminal tabs, no port/daemon.

**Confirmed user decision:** the done-signal lives in this gitignored spine (decision 1 = yes).

## B5. The Done-Signal (L2) — Producer/Consumer Model

**Producer (agent A)** publishes a **terminal `done` message** to a named channel on completion,
recording at minimum:

```text
{ stage, head, scope, producer, ts }
```

- `stage` — what was completed (e.g., "phase-29-execute").
- `head` — the Git commit SHA at publish time (the universal done anchor from B2).
- `scope` — the file/path scope this done covers.
- `producer` — which session published.
- `ts` — publish timestamp.

**Consumer (agent B)** polls the channel; on a `done` message it runs the **staleness gate**
(B6) before starting; if the gate fails it stays IDLE.

**Honest framing:** the mechanism **cannot mechanically prevent** a willful producer from doing
more work after publishing `done`. The achievable guarantee is **unambiguous publish +
consumer-side staleness detection**: B will not start on a stale or superseded done.

## B6. The Consumer-Side Staleness Gate (L2 core)

Before agent B acts on a `done` message, it checks three things against the message's
`{ head, scope }`:

1. **Ancestry check.** Is `done.head` an ancestor of the current integration HEAD? If not, the
   branch moved on — the done may be superseded.
2. **Committed-drift check.** Has anything in `done.scope` been committed *after* `done.head`?
   If yes, the work changed after the done was published → stale.
3. **Uncommitted-drift check.** Does the working tree carry uncommitted changes inside
   `done.scope`? If yes, someone is mid-edit → not safe to start.

Only when all three pass does the consumer wake. This is what makes "no more work after this
commit" *detectable* at B's start point.

## B7. GSD as an Adapter (L3) — Mechanical Surface

The core skill (L2) is **generic**: it knows only "publish/wait for a named stage, gated by a
commit-anchored staleness check." GSD specifics live in a **separate adapter file** that maps
GSD concepts onto the generic core:

- GSD phase → watchdog `stage`.
- The `verify(NN)` completion commit (B2) → the `done.head` anchor.
- GSD phase-scope paths → `done.scope`.

**Analogy (power plug):** the core skill is the socket; the GSD adapter is the country-specific
plug. Other workflows (non-GSD) get their own adapters. **Confirmed user decision:** the adapter
concept (explained this session) — and the scope is portable beyond GSD (decision scope = (b)).

## B8. Open Gaps and Build Status

- **Open gap (carry-over from Codex session, ref #2137):** the wake command must target a
  **specific Claude profile/session**, not just any polling session. Unresolved at design time.
- **Skill location:** `.claude/skills/` (confirmed user decision 4).
- **Build status: parked.** Part B is documented for completeness; it is **not approved for
  build** this session and will not be built until Part A lands and the user explicitly restarts
  the watchdog track.

---

## 3. How Part A and Part B Relate

- **Part A is structural and always-on.** It defines isolation (worktree per track) and conflict
  rules (taxonomy + pre-flight check) that govern *every* parallel interaction regardless of any
  watchdog.
- **Part B is temporal and on-demand.** It is wired only for explicit producer→consumer pairs
  that need a "done" signal.
- **Part B anchors on Part A.** The watchdog's `done.head` is a Git commit; Part A's rules
  (atomic logical-boundary commits, the `verify(NN)` completion commit convention, owned-path
  staging) are what make that commit a trustworthy done anchor. Weaker commit discipline would
  make the staleness gate noisy.
- **Order:** Part A first (it removes most friction on its own); Part B second (for the residual
  cases where a dependent session needs an explicit wake).

## 4. Decisions Locked This Session

| # | Decision | Source |
|---|---|---|
| 1 | Scope is **general-purpose / portable** beyond GSD (not GSD-only). | Msg 2 |
| 2 | Done-signal lives in the **gitignored `.live-monitor/` spine**. | Msg 2/4 |
| 3 | Skill location = **`.claude/skills/`**. | Msg 4 |
| 4 | Guidelines **extend `docs/git-guidelines.md`** (not a new file). | Msg 5 |
| 5 | **Enforce at agent level**: `CLAUDE.md` recognizes and follows the guideline strictly. | Msg 5 |
| 6 | Guidelines stay **generic** (GSD as example only). | Msg 5 |
| 7 | Isolation proposal judged: **sound, but worktree-not-branch, scoped rule, 5 costs**. | This turn |
| 8 | Enforcement: **soft (CLAUDE.md) now; hard hook offered later**. | This turn |
| 9 | **Do not edit `docs/git-guidelines.md` yet** — produce this review doc for verification first. | This turn |
| 10 | GSD-as-adapter concept **explained**; watchdog build remains parked. | Msg 4 + this turn |

## 5. Open Questions for the End-to-End Review

1. **Conflict taxonomy (A3):** are the four classes (A1/A2/B/C/D) and the R/W/D pre-flight check
   the right granularity, or should Class B (shared-file) be split further?
2. **Isolation rule (A4):** is "one worktree per active track" the right unit, or should it be
   per-milestone? (Today the repo effectively runs per-milestone in a single shared worktree.)
3. **The five operational costs (A4.4):** is the symlink-for-`simulation_data` policy acceptable,
   and is the rebase cadence (daily / before completion) right?
4. **Lock reconciliation (A5):** confirm **Option α (doc follows code, fail-fast)** vs Option β
   (code retries).
5. **Part B parking:** confirm the watchdog stays parked until Part A lands, and that gap #2137
   (wake must target a specific session) is acceptable to leave open in this design doc.

## 6. Glossary

- **Worktree** — a separate working-directory checkout of the same `.git`; the unit of true
  parallel isolation. Not the same as a branch.
- **Branch** — a commit pointer; necessary but not sufficient for isolation in a shared worktree.
- **Track** — a named long-running work stream (`specwork`, `trainex`, or a milestone); the unit
  to which a worktree is assigned under the isolation rule.
- **Producer / Consumer** — the session that completes work and publishes a `done` signal; the
  session that waits for that signal before starting dependent work.
- **Staleness gate** — the consumer-side 3-part check (ancestry / committed-drift /
  uncommitted-drift) against a `done` message's `{head, scope}`.
- **Pre-flight dependency check** — per-task R/W/D sets used to decide sequence vs partition vs
  allow-parallel for any pair of concurrent agents.
- **`.live-monitor/` spine** — the gitignored on-disk message channels the watchdog uses for
  producer→consumer signaling; designed with Codex, not yet built.
