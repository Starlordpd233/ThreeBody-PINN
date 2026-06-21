---
status: active
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

> **Companion to the design.** The architecture lives in Part B (Sections B1–B8) of
> `docs/work/designs/cross_cutting/parallel-agent-coordination/2026-06-17-parallel-agent-coordination-design.md`.
> That design is `status: consumed`, but the supersession covered only **Part A** (the
> worktree/Git guidelines, now built and landed). **Part B — the watchdog — was parked,
> nothing built.** This document is the plan to build it. It does **not** build it.

## 0. What this delivers, in one paragraph

Two Claude Code sessions run in separate terminal tabs. **Agent A** does a unit of work
(e.g. a GSD phase). **Agent B** sits idle in its own tab, pre-armed by the user with a
short prompt: *"wait for the watchdog; start your task once Agent A is done."* When A
finishes, B must **start working on its own, unattended** — no human keystroke. This plan
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

## 4. The signal — what "Agent A is done" means (unchanged from design)

Reusing the design's L1/L2 model verbatim; this plan only operationalizes it.

- **Anchor = the Git commit (design B2).** A unit of work is done when its atomic
  completion commit lands (for GSD: the `verify(NN)` phase-close commit). A commit is
  durable, ordered, and unambiguous — unlike `.planning/STATE.md`, which is structurally
  noisy and must **not** be used as a done signal.
- **Channel = the gitignored `.live-monitor/` spine (design L1/B4).** On-disk message
  channels under `.live-monitor/channels/<name>/messages/`, append-only, **atomic publish**
  (write temp file, then `rename`), with per-consumer cursors so B reads only new messages.
- **Done message = `{ stage, head, scope, producer, ts }` (design B5).** `head` is the
  commit SHA at publish time (the anchor); `scope` is the path set the done covers.

---

## 5. Build steps

Ordered so each step is independently testable. Nothing here is built yet.

### L1 — `.live-monitor/` spine
1. **L0 lock primitive.** Reuse the `mkdir`-lock pattern already in `scripts/agent-commit`
   (atomic create; trap-cleanup on exit). No new primitive.
2. **Channel layout.** `.live-monitor/channels/<name>/messages/` (gitignored). Publish =
   write `*.tmp`, then `rename` to a monotonic `NNNN.json`. Consumers keep a cursor file.
3. **`lm-publish` / `lm-check`.** Two small scripts: publish a message; report new messages
   since the cursor as **IDLE** / **WAKE**. (The design's 90-second cron drives `lm-check`;
   here the wake mechanism in L2 subsumes that.)

### L2 — done-signal + consumer-side staleness gate (the new core)
4. **Producer side (`lm-publish done`).** Agent A, on completing its unit, publishes the
   `done` message with the current HEAD as `head`.
5. **Consumer staleness gate (design B6)** — B runs all three before acting:
   - **Ancestry** — is `done.head` an ancestor of current integration HEAD?
   - **Committed-drift** — was anything in `done.scope` committed *after* `done.head`?
   - **Uncommitted-drift** — does the working tree carry uncommitted changes in `done.scope`?
   Wake only if all three pass. This is what makes "no more work after this commit"
   *detectable* at B's start point — the honest guarantee (the mechanism cannot stop a
   willful producer from working past `done`, but B will not start on a stale done).

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

# 3. from ANOTHER terminal, simulate the watchdog firing the wake:
tmux send-keys -t agentB 'Agent A is done — begin your task now.' Enter

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
  truly long idle (hours/restart) needs the durable cron (P2). Both are specified.
- **Staleness-gate scope precision.** The gate is only as good as `done.scope`. A too-broad
  scope causes false "stale"; too-narrow misses real drift. Adapter (L3) must set scope from
  the actual phase paths.
- **PUSH portability.** P3 works only where B is launched under tmux; it is explicitly an
  opt-in accelerator, never a requirement.
- **Dependency on Part A.** The done-anchor trusts atomic, owned-path commits — Part A's
  discipline (now landed). Weaker commit hygiene makes the gate noisy.

---

## 10. Scope guard — this plan builds nothing

Per the governing instruction for this session: the feasibility test is run and this plan is
written; **the tool is not built here.** Building L1/L2/the wake mechanism/the skill begins
only on explicit user go-ahead, and the PUSH accelerator (P3) waits on the Section 8 manual
confirmation.
