---
status: consumed
purpose: implementation-plan
created: 2026-06-21
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when the watchdog is built and landed — i.e. the `.live-monitor/` spine (L1),
  the done-signal + staleness gate (L2), the wake mechanism, and the `.claude/skills/`
  watchdog skill all exist and pass an end-to-end producer->consumer test, AND the
  user has run the manual two-terminal PUSH confirmation in Section 8. Until then this
  is the live build plan for the parked Part B watchdog.
---

# Cross-Session Watchdog — Build Plan

> **Superseded 2026-06-26** by
> [`2026-06-26-cross-session-watchdog-implementation-plan.md`](2026-06-26-cross-session-watchdog-implementation-plan.md)
> in this same folder. That rewrite is the executable plan of record; this document is
> retained as the feasibility/rationale predecessor (`status: consumed`).

> **Companion to the design.** The architecture lives in Part B (Sections B1–B8) of
> `docs/work/designs/cross_cutting/parallel-agent-coordination/2026-06-17-parallel-agent-coordination-design.md`.
> That design is `status: consumed`, but the supersession covered only **Part A** (the
> worktree/Git guidelines, now built and landed). **Part B — the watchdog — was parked,
> nothing built.** This document is the plan to build it. It does **not** build it.

## 0. What this delivers, in one paragraph

Two Claude Code sessions run in separate terminal tabs. **Agent A** does a unit of work
(e.g. a GSD phase). **Agent B** sits idle in its own tab, pre-armed by the user with a
short prompt: *"wait for the watchdog; start your task once Agent A is done."* When A
finishes, B must **start working on its own, unattended** — no human keystroke. The two
sessions typically run in **separate git worktrees** (this project runs one worktree per
track), so the watchdog must work **across worktrees** — a hard requirement (set 2026-06-22)
that shapes the channel and gate design (§4, §5). This plan
specifies the files, the signal, and the wake mechanism that make that happen, plus the
one last-mile question (`does a keystroke injected into B's terminal actually submit?`)
that only the user's manual two-terminal test can close.

---

## 1. The core decision: PULL-primary, PUSH-secondary

The original design left **gap #2137** open: *"the wake command must target a specific
session, not just any poller."* That gap only exists under a **PUSH** mental model — an
external watchdog process reaching into B's terminal and typing for it. This plan reframes
the primary path as **PULL**, which dissolves #2137 by construction, and keeps PUSH as an
optional low-latency add-on.

| | **PULL (primary)** | **PUSH (secondary)** |
|---|---|---|
| Who watches | **Agent B watches from inside its own session** | An external local watchdog process |
| Wake mechanism | B's own background watcher completes / B's own cron fires → the harness re-enters B's conversation | `tmux send-keys -t <B-pane>` injects the prompt |
| How "target the right session" is solved | **By construction** — the watcher lives *inside* the session it must wake | By **pane address** — B is launched as a named tmux pane; `-t agentB` is the address |
| Setup required of B | none beyond the arming prompt | B must be **launched inside tmux** |
| Latency | seconds (background watcher) to one poll interval (cron) | sub-second |
| Last-mile risk | low — re-entry is a native harness behavior | **the open question:** does send-keys make the TUI *submit*? (user tests manually) |

**Why PULL is primary.** It needs no multiplexer wrapper, no separate watchdog daemon, and
no machine-specific terminal automation. The "activate the idle session" step is a *native*
harness behavior (a background task finishing, or a scheduled prompt firing, re-enters the
conversation), so there is no cross-process stdin injection to get right. It is also the
path this session validated empirically (Section 7).

**Why keep PUSH at all.** It is the lowest-latency kick and the closest match to the user's
original mental model. It is worth supporting as an *opt-in accelerator* for users who
already run their sessions inside tmux — but it is not required for the system to work.

---

## 2. Gap #2137, resolved on both paths

The linchpin question — *"how does the wake reach the **one specific** idle Agent B and not
some other poller?"* — is answered differently per path, and both are now concrete:

- **PULL.** The watcher is registered *from within B's own session* (B arms a background
  watcher or a cron during its idle turn). When it fires, the harness re-enters **that
  session's** conversation, because that is the session that owns the watcher. There is no
  global "any poller" — the watcher and the target are the same process. #2137 does not
  arise.
- **PUSH.** B is launched as a **named** tmux session/pane (`tmux new -s agentB`). The
  watchdog addresses it explicitly: `tmux send-keys -t agentB '<prompt>' Enter`. The pane
  name *is* the specific-session address. #2137 is resolved by tmux's addressing model.

Either way, "target a specific session" is no longer an open research question; it is a
property of where the watcher is registered (PULL) or how B is launched (PUSH).

---

## 3. Harness primitives — what each one can and cannot do

Grounded against the loaded tool schemas and the platform facts established this session.
This table prevents picking the wrong primitive during the build.

| Primitive | What it does | Role in this build |
|---|---|---|
| **Background `Bash` (`run_in_background`) + `until`-loop** | Runs detached; on completion the harness **re-enters the agent's conversation** with the result | **PULL wake (P1, default).** B arms a watcher that blocks until the done-signal file appears, then exits → B is re-entered and proceeds. Validated this session (Section 7). |
| **`CronCreate`** | Fires a prompt **into the idle REPL** (not mid-query); 7-day expiry; `durable` flag persists across sessions | **PULL wake (P2, durable fallback).** A recurring cron fires "check the channel; proceed if a fresh gated done exists, else stay idle" into idle B. Survives long idle gaps and restarts. |
| **`tmux send-keys`** | Writes keystrokes into a pane's PTY master that tmux owns | **PUSH wake (P3, opt-in). Confirmed working** (user manual test, 2026-06-22). External watchdog injects the prompt into B's named pane; requires B under tmux. **Submit needs `Enter` as a *separate* `send-keys` call** — text and Enter in one call do not submit (the TUI absorbs the trailing Enter as a newline in the input box). |
| **`Monitor`** | Streams stdout-line events into chat | Optional: surfacing the watcher's progress to the human; **not** a wake mechanism by itself. |
| **`RemoteTrigger`** | claude.ai **cloud** routines API | **Not usable** — it is not a local-terminal activator. |
| **`PushNotification`** | Notifies the **human** | **Not usable** for unattended auto-invoke — it wakes a person, not an agent. |
| **`ScheduleWakeup`** | Self-paces a `/loop` in the *same* session | Not cross-session; not a wake for B from A. |
| **computer-use MCP** | Mouse/keyboard control of the desktop | **Cannot type into terminals** — terminals are tier "click" (typing/keypress blocked). Cannot be the injector. |

**Platform constraint that forces the tmux requirement for PUSH.** Injecting keystrokes
into a terminal the injector does **not** own would need the `TIOCSTI` ioctl, which is
**removed/restricted on modern macOS and Linux**. The only supported way for an external
process to drive an interactive terminal program is to own the PTY it runs on — which is
exactly what a multiplexer (tmux) provides. Hence: **PUSH requires B launched under tmux.**

---

## 4. The signal — what "Agent A is done" means (cross-worktree)

The design's L1/L2 model, **adapted for the cross-worktree requirement**. The design was
written assuming one shared worktree (it says so explicitly); this project runs one worktree
per track, so the channel and the gate must be redefined to span worktrees. The anchor is
unchanged; the channel location and the gate (§5 step 5) are the adaptations.

- **Anchor = the Git commit (design B2).** A unit of work is done when its atomic
  completion commit lands (for GSD: the `verify(NN)` phase-close commit). The commit SHA is a
  *global* anchor: all linked worktrees share one object store, so A's commit is visible from
  B's worktree regardless of branch (verified 2026-06-22 — `cat-file -e` resolves a
  cross-worktree HEAD). A commit is durable, ordered, and unambiguous — unlike
  `.planning/STATE.md`, which is structurally noisy and must **not** be used as a done signal.
- **Channel = a shared `live-monitor/` spine in the git common dir (cross-worktree fix).**
  Channels live under `<git-common-dir>/live-monitor/channels/<name>/messages/`, where the
  root is `git rev-parse --git-common-dir` — the single physical `.git` directory shared by
  every linked worktree (verified identical from all three live worktrees). Append-only,
  **atomic publish** (write temp file, then `rename`), per-consumer cursors so B reads only new
  messages. Because it lives inside `.git/`, it is outside every working tree and needs **no
  `.gitignore` entry**. (The design's working-tree-relative `.live-monitor/` would give each
  worktree a *private* channel — the cross-worktree break this fixes.)
- **Done message = `{ stage, head, producer, producer_ref, scope, ts }`.** `head` is the
  commit SHA at publish time (the anchor); `producer_ref` is A's branch (so B can detect
  whether A advanced past `head` within `scope`); `scope` is the path set the done covers. A
  publishes only when `scope` is committed and clean in its own worktree (a publish-time
  invariant the message asserts).

---

## 5. Build steps

Ordered so each step is independently testable. Nothing here is built yet.

### L1 — shared `live-monitor/` spine (in the git common dir)
1. **L0 lock primitive.** Reuse the `mkdir`-lock pattern already in `scripts/agent-commit`
   (atomic create; trap-cleanup on exit). No new primitive.
2. **Channel layout.** `<git-common-dir>/live-monitor/channels/<name>/messages/`, where the
   root is resolved at runtime by `git rev-parse --git-common-dir` (**not** a
   working-tree-relative path — that is what made the channel per-worktree). Publish = write
   `*.tmp`, then `rename` to a monotonic `NNNN.json`. Consumers keep a cursor file. No
   `.gitignore` entry needed (inside `.git/`).
3. **`lm-publish` / `lm-check`.** Two small scripts; **both resolve the channel root via
   `git rev-parse --git-common-dir`** so every worktree shares one channel. Publish a message;
   report new messages since the cursor as **IDLE** / **WAKE**. (The design's 90-second cron
   drives `lm-check`; here the wake mechanism in L2 subsumes that.)

### L2 — done-signal + consumer-side staleness gate (the new core, redefined for cross-worktree)
4. **Producer side (`lm-publish done`).** Agent A, on completing its unit, publishes the
   `done` message with its current HEAD as `head` and its branch as `producer_ref`. A
   publishes only when `scope` is committed and clean in its worktree.
5. **Consumer staleness gate (cross-worktree).** The design's B6 gate assumed A and B share
   one branch ("is `done.head` an ancestor of *my* HEAD?"). Across worktrees on different
   branches that ancestry is `false` even when A is genuinely done (verified 2026-06-22:
   specwork HEAD is not an ancestor of trainex HEAD), so the gate is redefined against the
   shared object store and A's own ref. B runs all three before acting:
   - **Reachability** — `git rev-parse --verify --quiet <done.head>^{commit}` succeeds: A's
     commit really exists in the shared store. (Replaces "ancestry to B's HEAD.")
   - **Producer-stability** — `git rev-list <done.head>..<done.producer_ref> -- <done.scope>`
     is empty: A's branch has no further `scope`-touching commits after the anchor. (Replaces
     same-branch committed-drift.)
   - **Producer-cleanliness** — the publish-time clean invariant holds; B may re-verify with
     `git -C <A-worktree> status --porcelain -- <done.scope>` if the message carries A's
     worktree path. (Replaces uncommitted-drift.)
   Wake only if all three pass — the honest guarantee (the mechanism cannot stop a willful
   producer from working past `done`, but B will not start on a stale done).
   - **Optional integration variant.** If B needs A's *content present in its own line* (not
     just "A finished"), additionally require
     `git merge-base --is-ancestor <done.head> <B-integration-ref>`. Whether to require this is
     a per-consumer choice — **surface, do not hardcode**; it changes the handoff from "A is
     done" to "A's work is merged into B's branch."

### Wake mechanism (the part the design left open)
6. **P1 — background watcher (default).** B's arming prompt installs a background `Bash`
   `until`-loop: block until `lm-check` reports **WAKE** for the channel, then exit. On exit
   the harness re-enters B's conversation; B runs the staleness gate (step 5) and, if it
   passes, begins its task. No timeout, or a long one (idle gaps can be hours — see
   Section 7's window lesson).
7. **P2 — durable cron (long-idle / restart-safe fallback).** Register a `durable`
   `CronCreate` that fires every N minutes into idle B: *"run `lm-check`+gate; if WAKE,
   begin task; else reply IDLE and do nothing."* Use when B may be idle past a background
   task's life or across a restart.
8. **P3 — tmux PUSH (opt-in accelerator).** When B is launched under tmux
   (`tmux new -s agentB`), an external watchdog loop running `lm-check`, on WAKE, issues the
   prompt **as two calls** (confirmed required, 2026-06-22):
   ```bash
   tmux send-keys -t agentB '<begin prompt>'   # type the text
   tmux send-keys -t agentB Enter              # submit as a separate keystroke
   ```
   A single `send-keys '<prompt>' Enter` does **not** submit — the TUI treats the trailing
   Enter as a newline inside the input box. A small delay (e.g. `sleep 0.2`) between the two
   calls is a cheap robustness hedge. Lowest latency; requires the tmux wrapper.

### L3 — GSD adapter (optional, project-specific)
9. **Adapter file** maps GSD onto the generic core (design B7): GSD phase → `stage`; the
   `verify(NN)` commit → `done.head`; phase-scope paths → `done.scope`. The core skill stays
   generic; GSD lives only in the adapter.

### Packaging
10. **Skill at `.claude/skills/` (locked decision 3).** One portable skill exposing
    `arm-consumer` (B side: install watcher P1/P2, register channel + scope + gate) and
    `publish-done` (A side). The GSD adapter ships as a separate file the skill can load.

---

## 6. End-to-end test (to run when building — not now)

1. Two sessions, shared repo. B: `arm-consumer --channel demo --scope <paths>`.
2. A: do trivial work, commit, `publish-done --channel demo`.
3. Expect: B's background watcher exits → B re-enters → staleness gate passes → B prints a
   "starting now" line and begins. Latency target: seconds.
4. Negative test: publish `done`, then commit a further change inside `scope` → B's gate
   must **fail** (committed-drift) and B must **stay idle**.

---

## 7. Empirical evidence gathered this session

| Test | Method | Result |
|---|---|---|
| **PULL detection** | Self-contained demo: consumer background-watches a signal file; producer touches it after 3s | **PASS** — `PULL_DETECTED after 3s`; harness re-entered the consumer on watcher completion. Validates P1. |
| **PTY keystroke injection (PUSH OS-primitive)** | `/tmp/wd_pty_proof.py`: parent opens a PTY, spawns an idle interactive child on the slave, then as an external writer `os.write`s `137\n` to the master | **PASS** — idle child responded `RESULT=1507` (137×11), proving it *acted* on injected keystrokes, not just echoed. This is the exact primitive `tmux send-keys` is built on. |
| **`screen`-based PUSH** | screen `-X stuff` transport + real-claude injection | **Environment-blocked, not a mechanism signal** — the only multiplexer present is `screen 4.00.03 (FAU, 23-Oct-06)`, a 2006 build that cannot reliably create/drive sessions; the sandbox also blocks PTY/session creation. Failures attributed to the tool/sandbox, not the approach. |
| **`tmux send-keys` → real claude TUI (the last mile)** | User manual two-terminal test (Section 8): idle `claude` in a named tmux pane; external `tmux send-keys` from a second terminal | **PASS** (2026-06-22) — the injected prompt submitted and Claude responded, with **no keystroke in B's tab**, *provided the `Enter` is sent as a separate `send-keys` call*. Combined `'<text>' Enter` appears in the box but does not submit. PUSH (P3) is cleared for build with the two-call shim. |

**Interpretation.** PULL is validated end-to-end. The PUSH *mechanism* (external writer →
keystrokes → idle interactive program acts) is validated at the OS-primitive layer via the
PTY proof. The **one** thing not provable on this machine is whether `tmux send-keys`
specifically makes the **claude TUI submit** (Enter/bracketed-paste handling) — because tmux
is not installed and `screen` is too old. That is precisely the slice the user reserved for
the manual two-terminal test (Section 8). The division of labor is clean: the mechanism
foundation is proven here; the last mile is the user's to confirm. **That confirmation
landed 2026-06-22: PASS, with the two-call `Enter` shim** (see the evidence row above and
§8). PUSH is therefore feasible end-to-end; nothing about the watchdog is now unproven.

> Reproducer for the PTY proof (dependency-free; run with the sandbox disabled, since PTY
> creation is sandbox-blocked):
>
> ```text
> python3 /tmp/wd_pty_proof.py
> # child is idle (READY), blocked on stdin — modeling an idle Agent B
> # injected "137\n" into PTY master; child emitted: '137\nRESULT=1507'
> # PTY_INJECTION_PASS: external write to a PTY master drove an already-idle
> #   interactive child (137 -> 1507)
> ```
>
> When building, move this proof into the repo (e.g. under `tools/`) so the claim is
> re-derivable from committed state rather than `/tmp`.

---

## 8. The user's manual confirmation — the definitive PUSH test

The user owns this test. It confirms the only unproven slice: that a keystroke injected by
an external process makes a **real idle `claude` TUI** submit and start working.

```bash
# 1. install tmux (needed for the PUSH path and for this test)
brew install tmux

# 2. launch Agent B inside a named tmux session, then arm it with the short prompt
tmux new -s agentB
#   inside: start `claude`, and tell it: "wait for the watchdog; when it injects
#   a prompt saying Agent A is done, begin your task."  Then leave it idle.

# 3. from ANOTHER terminal, simulate the watchdog firing the wake (TWO calls — see Outcome):
tmux send-keys -t agentB 'Agent A is done — begin your task now.'   # type the text
tmux send-keys -t agentB Enter                                       # submit separately

# PASS = the idle Agent B receives the line, submits it, and starts working
#        with no human keystroke in B's tab.
```

If this PASSES, P3 (the PUSH accelerator) is fully cleared for build. If it does **not**
submit reliably (e.g. the TUI needs a separate Enter, or bracketed paste interferes), PULL
(P1/P2) remains the primary path and the system still works — PUSH simply stays unsupported
or gains a tmux-specific Enter-handling shim. **The system does not depend on this test
passing; it only determines whether the optional accelerator ships.**

**Outcome (2026-06-22): PASS.** The injected prompt submitted and Claude responded with no
keystroke in B's tab — *but only when `Enter` is sent as a separate `send-keys` call*. The
combined `tmux send-keys -t agentB '<text>' Enter` placed the text in the input box without
submitting (the TUI absorbed the trailing Enter as a newline). The canonical PUSH wake
command is therefore the **two-call** form:

```bash
tmux send-keys -t agentB '<begin prompt>'   # text
tmux send-keys -t agentB Enter              # submit (separate keystroke)
```

PUSH (P3) is cleared for build with this shim baked into the wake command.

---

## 9. Risks, limitations, scope

- **Honest guarantee (design B5).** The mechanism cannot mechanically stop a willful
  producer from working *after* publishing `done`. The achievable guarantee is unambiguous
  publish + consumer-side staleness detection. Accepted.
- **Long idle gaps.** A background watcher (P1) lives only as long as the session process;
  truly long idle (hours/restart) needs the durable cron (P2). Note P2's ceilings (from the
  `CronCreate` contract): durable crons **auto-expire after 7 days** and fire with up to
  ~15 min jitter — so a >7-day idle outlives even P2, and P2 latency is not exact.
- **Staleness-gate scope precision.** The gate is only as good as `done.scope`. A too-broad
  scope causes false "stale"; too-narrow misses real drift. Adapter (L3) must set scope from
  the actual phase paths.
- **PUSH portability.** P3 works only where B is launched under tmux; it is explicitly an
  opt-in accelerator, never a requirement.
- **Dependency on Part A.** The done-anchor trusts atomic, owned-path commits — Part A's
  discipline (now landed). Weaker commit hygiene makes the gate noisy.
- **Cross-worktree assumptions (2026-06-22 requirement).** The shared channel and the
  redefined gate assume A and B are **linked worktrees of the same repo** — one git common
  dir, one object store (verified). They do **not** span separate clones or machines; that is
  out of scope. Producer-stability/cleanliness assume A commits its unit before publishing
  `done` and does not later rewrite or force-push `producer_ref`.

### Open items to resolve before build (2026-06-22 review)

Recorded so they are not lost. Several are design sub-decisions to settle at build start, not
agent calls to make now:

- **Task payload contract (gap).** The wake transfers *control* to B, but nothing yet defines
  *what B does* — where B's task is specified and how it re-derives it after a cron fire or a
  long idle. Decide: arming-prompt-only, or a task-spec file the `done`/wake message points to.
- **Exactly-once guard (gap).** If both P1 (watcher) and P2 (cron) are armed, or a second
  `done` lands, B can double-start. Add a single-consumption claim/lock (e.g. B writes a
  `claimed/<msg-id>` marker under the channel via the L0 lock before acting).
- **Producer-liveness / dead-A timeout (gap).** P1's `until`-loop has no timeout; if A
  crashes, B blocks forever. Add a bounded timeout that surfaces "A appears stalled" rather
  than hanging silently.
- **P1 idle-wake grounding.** The real basis for "idle B wakes" is the tool contract
  (background `Bash` "re-invokes you when it exits"; `ScheduleWakeup`/`Monitor` notes), not the
  single `PULL_DETECTED after 3s` run (which did not isolate the no-human case). Add an
  explicit idle test to §6: arm B, type nothing, confirm B still wakes.
- **Evidence re-derivability.** Move `/tmp/wd_pty_proof.py` into `tools/` at build start so the
  PUSH proof is re-derivable from committed state, not `/tmp`.
- **Authority hygiene.** When building, re-home design Part B as `active` (or add a forward
  pointer) so a `status: consumed` doc is not the sole architecture record. Keep the injected
  wake prompt a fixed constant — never interpolate channel-file contents into `send-keys`.

---

## 10. Scope guard — this plan builds nothing

Per the governing instruction for this session: the feasibility test is run and this plan is
written; **the tool is not built here.** Building L1/L2/the wake mechanism/the skill begins
only on explicit user go-ahead, and the PUSH accelerator (P3) waits on the Section 8 manual
confirmation.
