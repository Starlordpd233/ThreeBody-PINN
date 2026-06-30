---
status: active
purpose: design
created: 2026-06-30
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when the watchdog is verified for global within-project deployment (all
  gates G0–G4 PASS with committed evidence) AND the cross-project extension is
  either built+verified or formally declined. Re-open on any Claude Code harness
  upgrade touching background Bash re-entry, CronCreate/CronList, or skill
  discovery, or on any change to wd-common.sh path resolution or the global-scope
  packaging.
---

# Cross-Session Watchdog — Verification Strategy

## In plain terms (read this first)

The watchdog lets one idle Claude session (**Agent B**) start working the instant
another session (**Agent A**) finishes and says "done." We are about to make the
skill **global** — available in every CCP profile and every project, so you can
invoke it wherever you work. Before we trust it in real use, we need to prove it
works **under every scenario it claims to handle**, not just the one path that has
been demonstrated so far.

This document is the **plan for that proof**. It does three things:

1. **Inventories what is already proven** (so we don't re-test green things).
2. **Names every gap** and maps each to the **cheapest kind of test** that can
   actually exercise it — from instant automated checks up to live two-session
   rehearsals that a human has to watch.
3. **Defines the "ready to deploy" bar**: a short list of gates that must all be
   green, each backed by committed, re-runnable evidence.

Scope decision (locked 2026-06-30): we verify the watchdog working **inside
whatever project you use** (including across branches/worktrees of that one
project), at **global availability**, on a **single machine**. Handing off
**between two different projects** ("cross-project") is captured as a designed,
optional extension at the end — not part of the first "verified" verdict.

---

## 1. System under test (what we are verifying)

The watchdog is **8 small command-line tools** plus one shared helper, all under
`tools/watchdog/`, driven by the `cross-session-watchdog` skill
(`.claude/skills/cross-session-watchdog/SKILL.md`):

| Tool | Role | Key verdicts / exit codes |
|---|---|---|
| `wd-publish-done` | Producer A: "I'm finished" (writes `done.json`) | `published…`; refuses dirty scope → **3** |
| `wd-check` | Consumer staleness gate | `WAKE`(0) · `IDLE`(10) · `STALE:<why>`(20) |
| `wd-arm` | Consumer B: background watcher + exactly-once claim (P1) | `WAKE <head>`(0) · `ALREADY-CLAIMED`(0) · `PRODUCER-STALLED`(**42**) · `DISARMED`(0) |
| `wd-integrate` | Consumer B: merge A's head (cross-worktree) | `integrated`/`already-integrated`(0) · `CONFLICT`(**4**, aborts clean) · no-marker(10) |
| `wd-disarm` | External kill-switch (`--channel`/`--all`) | idempotent, exit 0 |
| `wd-status` | Read-only "what's armed" view | exit 0 |
| `wd-push` | External tmux PUSH accelerator | `PUSHED`(0) · `ALREADY-CLAIMED`(0) · `PRODUCER-STALLED`(42) · `DISARMED`(0) · tmux-missing(**5**) · pane-missing(**6**) · send-keys-failed(**7**, releases claim) |
| `wd-gsd-publish` | GSD adapter → `wd-publish-done` | `--phase NN` → `stage=gsd:phase-NN`; bad args → 2 |

**Rendezvous model.** State lives on disk at
`<git-common-dir>/live-monitor/channels/<channel>/` — files `done.json`,
`claimed.<head>`, `armed.json`, `disarm`, `consumer-task.md`. Because the channel
root is keyed to the **current repo's** git common dir, A and B share a mailbox
**iff they are in the same repo** (any branch/worktree). The exactly-once wake is
an atomic `mkdir claimed.<head>`; termination rides on `armed.json` + the `disarm`
sentinel + a `TERM` trap.

**Wake paths.** **P1** background watcher (`wd-arm`, default, drain-safe) · **PUSH**
external tmux injector (`wd-push`, optional) · **P2** durable cron (gated, fallback).

**The fixed wake prompt** (must be byte-identical wherever it appears):

> Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result line;
> if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, stop and report.

---

## 2. Coverage baseline — what is already proven

**Automated logic (28 tests, all green)** under `tests/watchdog/`:

- `test_watchdog_mvp.py` (8) — resolver→absolute path; publish→check WAKE;
  producer-advanced→STALE; dirty-scope refusal; claim-once; timeout→PRODUCER-STALLED;
  task-file persistence; missing-task-file still arms.
- `test_watchdog_xworktree.py` (4) — not-integrated→STALE; integrate→wake;
  already-integrated; conflict-aborts-clean.
- `test_termination.py` (5) — armed.json visible to status; disarm stands down a
  *running* watcher; TTL self-termination; idempotent/empty disarm; armed_by from env.
- `test_push.py` (7) — arg/precondition guards (exit 2/5/6); two-call send-keys shim
  exactly-once; second push→ALREADY-CLAIMED; disarm stands down push-watcher;
  send-keys failure releases claim→exit 7. **tmux is stubbed.**
- `test_gsd_adapter.py` (4) — phase→stage mapping + anchor; bad phase; missing scope;
  clean delegation.

**Live harness behavior (single machine, manual evidence committed):**

- **P1 background re-entry — PASS** (`evidence/2026-06-26-idle-wake-results.md`): an
  idle session woke itself when its background shell exited, no keystroke.
- **P2 durable cron — PASS with caveats** (same file): foreground-only on macOS;
  silent-drain risk → drove the Phase 4 termination contract.
- **Same-worktree two-tab end-to-end — PASS** (`evidence/2026-06-28-same-worktree-live-dryrun.md`):
  real `wd-arm`, real publish from a separate session, real unattended re-entry, claim, task run.

**What this means:** the *script logic* and the *P1 same-worktree live path* are
solid. The strategy below deliberately spends little effort re-proving these and
concentrates on the unproven cells (Section 4, tiers T3–T4).

---

## 3. The scenario space (so "all scenarios" is a checklist, not a vibe)

Degrees of freedom in the actual mechanism:

- **Topology:** same-worktree (SW) · cross-worktree (XW). *(cross-project = §8 extension.)*
- **Wake path:** P1 (pull) · PUSH (tmux) · P2 (cron).
- **Producer outcome:** clean done · dirty-scope (refuse, 3) · advanced-after-publish
  (STALE) · unreachable head (STALE) · never finishes (PRODUCER-STALLED, 42).
- **Claim outcome:** single winner · double-start race (two wake paths, one head) →
  exactly-once · PUSH send-keys TOCTOU → claim released → pull fallback (7).
- **Integration (XW only):** clean merge · already-integrated · conflict → abort, 4,
  tree clean.
- **Termination:** natural exit · disarm sentinel mid-poll · SIGTERM during sleep
  (TERM trap → DISARMED) · TTL self-terminate · `wd-disarm --all` idempotent ·
  `wd-status` visibility.
- **Deployment context:** C1 this repo, CWD=root · C2 a *foreign* project dir under
  the global skill · C3 a subdir of a repo · C4 a non-git dir · *(C5 cross-project = §8.)*
- **Multiplicity:** many channels at once · repeated arm→wake→re-arm cycles ·
  stale/orphaned `armed.json` with a dead-or-reused pid.

Every existing test/evidence item maps into this space; the empty cells are what
Section 4 targets.

---

## 4. The five-tier verification model

Cheapest, most-deterministic first. Each scenario is verified at the **cheapest tier
that can actually exercise it** — we do not push a thing to a live rehearsal if a
unit test proves it.

### T0 — Static / contract checks (automated, seconds)

Catches doc-vs-tool drift, which is the most likely silent breakage as the skill is
repackaged for global use.

- `shellcheck` all 8 tools + `lib/wd-common.sh`.
- Assert the **fixed wake prompt** is byte-identical across `wd-arm`, `wd-push`, and
  `SKILL.md`.
- Assert the verdict/exit-code vocabulary in `SKILL.md` matches what the tools emit.
- Assert the watch-loop scripts restore `set +e` after sourcing `wd-common.sh`
  (an `set -e` foot-gun here would kill the loop on an expected non-zero from `wd-check`).

**Acceptance G0:** all static checks pass; zero drift findings.

### T1 — Unit / logic (automated; the 28 + targeted additions)

Keep the 28. Add the logic cells they miss:

- **T1-a True concurrent claim race.** Spawn 2×`wd-arm` + 1×`wd-push` against one
  head simultaneously; assert **exactly one** `WAKE`/`PUSHED`, the rest
  `ALREADY-CLAIMED`, and **exactly one** `claimed.<head>` dir. (Today's claim tests
  are sequential.)
- **T1-b Non-git CWD.** Run each tool from a non-repo dir; assert a **defined,
  friendly** message + non-zero exit, **not** a raw `git rev-parse` stack trace.
  *(This is a likely real misuse once the skill is global — see C4.)*
- **T1-c Foreign-CWD, absolute tool path.** Invoke a tool by absolute path while CWD
  is a *different* repo; assert the channel resolves to **that CWD's** repo, not the
  tool's home. (Pins the resolver's correctness for global use.)
- **T1-d Cycle housekeeping.** arm→wake→re-arm across 3 successive heads; define and
  assert the expected `claimed.<head>` accumulation/cleanup behavior.
- **T1-e Dead/reused-pid disarm.** `wd-disarm` against an `armed.json` whose pid is
  gone (or reused by an unrelated process); assert no error and document the
  reused-pid hazard (best-effort `kill` could signal an unrelated process — low
  probability, surfaced honestly).

**Acceptance G1:** 28 existing + all new T1 tests green.

### T2 — Scripted multi-process integration (automated-ish; real processes, no harness)

Real OS processes, real timing, real filesystem — but no Claude harness, so it runs
in CI/unittest.

- Producer + **N** real consumers racing one publish (T1-a at process fidelity).
- `disarm` sentinel dropped mid-poll → `DISARMED` within one poll interval.
- `SIGTERM` delivered during the poll `sleep` → `DISARMED` via the TERM trap (not a
  silent kill).
- Cross-worktree with **real linked worktrees**: integrate clean / already / conflict-abort.

**Acceptance G2:** all T2 scripts green and re-runnable.

### T3 — Live harness, single machine (manual protocol + committed evidence)

The cells only the real Claude Code harness can exercise. Each needs a written step
protocol and a committed evidence file under `tools/watchdog/evidence/` recording
**PASS/FAIL + latency + observed re-entry mode + environment** (the established
`2026-06-26`/`2026-06-28` pattern).

- **T3.1 Cross-worktree two-session handoff [GAP].** B armed in a linked worktree on
  its own branch; A publishes from the main worktree; B wakes unattended, runs
  `wd-integrate` → `wd-check --require-integration` → begins. *(Only SW is live-proven.)*
- **T3.2 Real PUSH [GAP].** Real `tmux`, a real **idle claude** pane as B, `wd-push`
  from the operator terminal; assert the two-call send-keys shim wakes B exactly
  once. *(The old PTY proof is no longer on disk; stub tests don't cover real tmux.)*
- **T3.3 P2 cron under the Phase-4 termination contract [GAP].** Arm with explicit
  "yes, durable" + a TTL; verify the job on disk (**both** `CronList` **and**
  `.claude/scheduled_tasks.json`); confirm **disarm-on-success** deletes the job,
  **TTL self-termination** fires, and the **foreground caveat** is surfaced. *(The
  2026-06-26 P2 test predates this contract.)*
- **T3.4 Same-worktree P1 re-confirm.** Already PASS (2026-06-28); re-run **only**
  after a harness upgrade (see §7 re-validation), not as new work.

**Acceptance G3:** T3.1–T3.3 each PASS with committed evidence.

### T4 — Global-scope deployment (manual + automated mix) — the new frontier

This is the layer the user is actually worried about and the least covered today.
**Method-agnostic to however the other agent makes the tools global** — these tests
assert the *outcome* (an agent in any project can complete a handoff), not the
mechanism.

- **T4.1 Discovery.** In each CCP profile, and from an arbitrary project directory,
  the `cross-session-watchdog` skill is surfaced and loadable.
- **T4.2 Tool resolution from a foreign project [load-bearing].** An agent working in
  a project that is **not** `3_body_problem` can find and run the `wd-*` tools and
  complete a **within-project** handoff (A and B both in that project). If this fails,
  global deployment is not real. *(Directly tests the relative-path hazard:
  `SKILL.md` currently says `tools/watchdog/wd-arm`.)*
- **T4.3 Channel isolation.** A handoff in project-Y uses project-Y's mailbox; a
  concurrent handoff in project-Z does not cross-talk.
- **T4.4 Non-git-dir guard.** Invoking the workflow where there is no repo yields a
  clear refusal (pairs with T1-b), not a confusing failure.
- **T4.5 Instruction-following rehearsal [highest-value].** A **fresh** agent, given
  **only** the global skill text (no repo context, no this-conversation history),
  executes a full A→B handoff correctly. This catches `SKILL.md` path/anchoring/wording
  bugs that no logic test can see — the skill *as the agent reads it*, not the tools
  in isolation.

**Acceptance G4:** T4.1–T4.5 PASS, with T4.2 and T4.5 mandatory.

---

## 5. "Ready to deploy" — the gate

The watchdog is **verified for global within-project deployment** when **all** hold,
each backed by committed evidence:

| Gate | Tier | Bar |
|---|---|---|
| **G0** | T0 | Static/contract checks clean; zero drift |
| **G1** | T1 | 28 existing + new logic tests green |
| **G2** | T2 | Multi-process race / disarm / SIGTERM / XW integration green |
| **G3** | T3 | Cross-worktree-live, real-PUSH, P2-under-contract each PASS |
| **G4** | T4 | Discovery + foreign-project resolution + isolation + non-git guard + agent rehearsal PASS |

**Capstone (Approach C):** after G0–G4, one **dogfooded** end-to-end run — a real
A→B handoff, wired through the watchdog itself, where B's armed task is "run the
watchdog test suite." This doubles as the real-world acceptance demo. It is a
capstone, **not** a substitute for the deterministic tiers (a watchdog bug must not
be able to hide its own failure).

Cross-project (§8) is gated **separately** and only if it is built.

---

## 6. Execution model & sequencing

1. **Now (no dependency):** T0 + T1 + T2 — automatable, fast, closes the logic nits.
2. **When the global packaging lands** (coordinate with the agent doing it): T4.2 and
   T4.5 — the load-bearing global checks.
3. **In parallel with step 2** (single-machine harness runs): T3.1–T3.3.
4. **Capstone:** the dogfooded acceptance run.
5. **Later, optional:** the cross-project extension (§8) — design, then T5.

**Who does what.** Automated tiers (T0–T2) and the test code for T4.2–T4.4 can be
built and run by an agent. The **live** tiers (T3, T4.1, T4.5, capstone) need real
sessions: an agent can script and drive them, but a human supplies the second
session / the foreground tab / the tmux pane and confirms the observed re-entry.

---

## 7. Evidence & re-validation conventions

- **Automated tiers:** committed tests under `tests/watchdog/` (re-derivable proof of
  logic).
- **Live tiers:** committed evidence files under `tools/watchdog/evidence/`
  (`YYYY-MM-DD-<topic>.md`, with PASS/FAIL, latency, re-entry mode, environment) —
  matching the existing two evidence notes.
- **Status tracking:** this document's Section 4/5 tables are the per-tier checklist;
  a companion checklist file may track per-cell PASS/FAIL as runs complete.
- **Re-validation triggers (re-run T3 + T4):**
  - any Claude Code harness upgrade touching background `Bash` re-entry,
    `CronCreate`/`CronList`, or skill discovery;
  - any change to `wd-common.sh` path resolution;
  - the first landing of, or any later change to, the global-scope packaging.

---

## 8. Optional extension — cross-project handoff (designed, not yet in scope)

Captured per the 2026-06-30 scope decision so the idea is build-ready without
blocking the verification above.

**Goal.** Let Agent A in project **X** hand off to Agent B in project **Y** on the
**same machine**.

**Why it's a real change, not a config flag.** Two things are repo-keyed today:

1. **The mailbox** lives under the current repo's git common dir, so X and Y get
   *different* mailboxes and never see each other. Cross-project requires relocating
   the mailbox to a **machine-global root** (e.g.
   `${XDG_STATE_HOME:-$HOME/.local/state}/watchdog/channels/` or
   `~/.claude/watchdog/channels/`), selectable so within-project stays the default.
2. **Integration** relies on a shared git object store (that is *why* `wd-integrate`
   can merge A's head across worktrees). X and Y have **separate** object stores, so
   B does **not** have A's commit. Two honest options, both to be surfaced to the user
   at arm time:
   - **Signal-only handoff:** "A is done, B go" with **no** automatic git merge — B
     does not inherit A's committed files. Weaker guarantee, simplest.
   - **Fetch-then-integrate:** an optional `wd-fetch` step adds A's worktree as a
     temporary remote, fetches A's head, then integrates. Stronger, but more moving
     parts and new failure modes (auth, divergent histories).

**T5 verification sketch** (only if built): cross-project two-session live handoff;
signal-only correctness (and fetch-then-integrate, if chosen); isolation between
concurrent cross-project channels; and a **no-cross-talk** check proving cross-project
channels never collide with within-project ones.

---

## 9. Risks & open questions

- **Tool-location model is owned by the in-flight global work.** T4.2/T4.5 are
  method-agnostic, but the exact discovery test depends on where the tools physically
  land. **Coordinate before running T4.**
- **`SKILL.md` hard-codes `tools/watchdog/…` relative paths** — the most likely
  global-scope breakage; T4.2 and T4.5 exist primarily to catch it.
- **Reused-pid in `wd-disarm` best-effort `kill`** — low-probability safety nit
  (T1-e); surfaced, not yet mitigated.
- **PUSH soft precondition** ("pane must be at a clean idle claude prompt") is
  unverifiable by tooling and remains an operator responsibility; T3.2 documents it.
- **`claimed.<head>` housekeeping** over long-lived channels (T1-d) — define expected
  behavior before declaring G1.
