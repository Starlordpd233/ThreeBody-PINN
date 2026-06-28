---
status: active
purpose: implementation-plan
created: 2026-06-26
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when the watchdog MVP is built and landed — the signal+gate (wd-* tools),
  the proven wake path (Phase 1 decision), the same-worktree end-to-end test, and
  the cross-worktree integration step all exist and pass their committed tests.
  Supersedes 2026-06-21-cross-session-watchdog-build-plan.md.
---

# Cross-Session Watchdog — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This plan builds nothing until the user exits plan mode and gives the go-ahead; Phase 0 (a governed docs move) and Phase 1 (a manual two-terminal test) each carry their own approval gate.

**Goal:** Let one idle Claude Code session (Agent B) start working on its own, unattended, the moment a second session (Agent A) finishes a unit of work — primarily when A and B share one worktree, and secondarily across linked worktrees.

**Architecture:** A publishes a terminal `done` marker (atomic file) into a channel inside the shared git common dir; the marker is anchored on A's completion commit SHA. B watches that channel from *inside its own session* (a background `Bash` loop, later a durable cron), so when the watcher exits the harness re-enters B's conversation — the wake targets the right session by construction. Before acting, B runs a commit-anchored **staleness gate** and an atomic **exactly-once claim**. In the common same-worktree case B already has A's files; cross-worktree, B integrates A's commit first (user decision: B integrates; watchdog only signals).

**Tech Stack:** POSIX `bash`, `git` (worktrees, shared object store), the Claude Code harness primitives (background `Bash` re-entry, `CronCreate`, optional `tmux send-keys`), `python3`/`unittest` for committed tests (matches `tests/git_policy/`), packaged finally as a `.claude/skills/` skill.

---

## Context — why this plan exists

Three things prompted this rewrite:

1. **Two scattered plan folders.** The watchdog's work is split across `docs/work/plans/cross_cutting/parallel-agent-coordination/` (the **completed** Part-A worktree/concurrency plan, `status: consumed`) and `docs/work/plans/cross_cutting/cross-session-watchdog/` (the **active, unbuilt** watchdog plan). They are two phases of one design family, not the same task. Phase 0 consolidates them under the umbrella `parallel-agent-coordination/` topic. (After Phase 0 ran, the umbrella folder was renamed to `parallel-agent-coordination-watchdog/` on 2026-06-26 for quick identification; the original-name paths in the Phase 0 steps below reflect the commands as executed.)

2. **The prior plan was a feasibility/rationale doc, not an executable plan.** A final review (this session) found load-bearing gaps: the "primary" PULL wake path's unattended idle-wake was the *least*-demonstrated piece (PUSH was the only path proven in a real idle TUI); a producer-stability livelock; an incomplete `git rev-parse --git-common-dir` command; an unspecified exactly-once race; a missing task-payload contract; and no dead-producer timeout. This plan resolves each.

3. **Scope clarified by the user.** (a) The **common case is two agents in one worktree** — cross-worktree is a "keep it handy" capability, not the main path. (b) For cross-worktree dependent handoffs, **B integrates A's work itself**; the watchdog only certifies "A is done + reachable." (c) **De-risk first:** prove the wake mechanism before building the full stack.

The reframing matters: same-worktree, A's commit is already on B's HEAD and A's files are already in B's checkout, so the watchdog reduces to its essential core — *wake idle B when A's done-commit lands.* The cross-worktree channel/gate is the secondary mode.

---

## Global Constraints

Copied verbatim from project governance; every task inherits these.

- **Commits:** use `scripts/agent-commit` only — never raw `git commit`. Set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` (colon/newline-separated explicit paths). Stage explicit owned paths only — **no** `git add .`/`-A`/`-u`.
- **Branch:** this is cross-cutting work → perform in the **main worktree** (`<home>/Desktop/3_body_problem`) on `master`. Commit locally; **do not push** from `master`/`main`/`milestone/*`.
- **Commit messages:** `<type>(<scope>): <lowercase imperative subject>`; scopes here are `docs` (Phase 0 docs moves) and `governance` (the watchdog tooling/evidence — it is Part B of the parallel-agent-coordination/governance family; the commit-msg hook **rejects** a `watchdog` scope, allowing only `governance, planning, pinn, brutus, pipeline, spec, docs, ref` plus phase/task scopes). `plan`/`docs` commits require a body. Add an `Agent-Assisted-By:` trailer.
- **Docs moves (Phase 0):** require a reference audit + a written move proposal + **explicit user approval** before executing (docs/README.md §Reference Audit / §Cleanup Boundaries). Never move artifacts outside `docs/`.
- **Pre-existing uncommitted edits:** the old build plan currently carries uncommitted cross-worktree edits. Commit those as their **own** atomic unit before any supersession/transformation (git-guidelines: never fold pre-existing changes into a transformation commit).
- **Evidence re-derivability:** committed tests/proofs, not `/tmp`. Wake prompts are **fixed constants** — never interpolate channel-file contents into a prompt or `send-keys`.
- **Do not touch** unrelated working-tree changes (`.claude/settings.json`, `.planning/STATE.md`, the provider-config edit).

---

## Phase overview

| Phase | Deliverable | Build now? | Gate |
|---|---|---|---|
| **0** | Consolidate the two plan folders; file this plan; supersede the old one | yes | docs move-approval |
| **1** | Prove unattended idle-wake in a real two-terminal TUI; pick the primary wake path | yes | manual test PASS |
| **2** | MVP: signal + staleness gate + exactly-once + same-worktree end-to-end | yes | committed tests pass |
| **3** | Cross-worktree mode: gate variant + "B integrates A" step | yes | committed test passes |
| **4** | Durable cron wake + task-payload persistence + packaged skill | deferred until 1–3 land | — |
| **5** | Optional PUSH (tmux) accelerator + GSD adapter | opt-in, after 4 | — |

Phases 0–3 are specified to executable detail below. Phases 4–5 are forward outlines whose detail is intentionally deferred until the Phase 1 decision and the MVP results are known (per the de-risk-first decision); they are not placeholders for the active scope.

---

## Phase 0 — Consolidate the plan folders (governed docs move)

**Files:**
- Pre-existing edits: `docs/work/plans/cross_cutting/cross-session-watchdog/2026-06-21-cross-session-watchdog-build-plan.md` (commit as-is first)
- Create: `docs/work/plans/cross_cutting/parallel-agent-coordination/2026-06-26-cross-session-watchdog-implementation-plan.md` (this plan)
- Move + supersede: the old build plan into the umbrella folder, `status: consumed`
- Remove: the emptied `docs/work/plans/cross_cutting/cross-session-watchdog/` directory

- [ ] **Step 1: Commit the pre-existing uncommitted edits to the old plan as their own unit.**

```bash
cd <home>/Desktop/3_body_problem
GIT_AGENT_ID=watchdog-build \
GIT_AGENT_OWNED_PATHS='docs/work/plans/cross_cutting/cross-session-watchdog/' \
scripts/agent-commit -m "plan(docs): land cross-worktree edits to watchdog build plan" \
  -m "Commit the prior session's cross-worktree signal/gate edits before superseding."
```
Expected: one commit touching only the old build plan.

- [ ] **Step 2: Reference audit (required before any docs move).**

```bash
cd <home>/Desktop/3_body_problem
for q in cross-session-watchdog 2026-06-21-cross-session-watchdog-build-plan; do
  echo "== $q =="; rg --hidden --glob '!.git/*' -l "$q" || echo "(no refs)"
done
```
Expected: a list of every file referencing the old path/slug (the memory pointer, the presence-overlap docs, the design). Record it — these references get updated in Step 4.

- [ ] **Step 3: Write the move proposal and STOP for user approval.** Present: file, old path, new path, type=plan, reason (consolidation), the audit result, the list of references to update. Wait for explicit approval. Do not proceed without it.

- [ ] **Step 4: On approval — file this plan, move + supersede the old one, update references, remove the empty dir.**

```bash
cd <home>/Desktop/3_body_problem
DEST=docs/work/plans/cross_cutting/parallel-agent-coordination
# 4a. write THIS plan to $DEST/2026-06-26-cross-session-watchdog-implementation-plan.md
#     (apply the frontmatter from the top-of-file comment; drop the comment)
# 4b. move the old plan under the umbrella, set status: consumed + a superseded-by line
git mv docs/work/plans/cross_cutting/cross-session-watchdog/2026-06-21-cross-session-watchdog-build-plan.md "$DEST/"
#     then edit its frontmatter: status: consumed; add prose:
#     "Superseded 2026-06-26 by 2026-06-26-cross-session-watchdog-implementation-plan.md."
# 4c. update each reference found in Step 2 to the new path
# 4d. remove the now-empty directory
rmdir docs/work/plans/cross_cutting/cross-session-watchdog
```

- [ ] **Step 5: Verify and commit.**

```bash
cd <home>/Desktop/3_body_problem
ls docs/work/plans/cross_cutting/parallel-agent-coordination/   # 3 files; cross-session-watchdog/ gone
git diff --cached --stat
GIT_AGENT_ID=watchdog-build \
GIT_AGENT_OWNED_PATHS='docs/work/plans/cross_cutting/' \
scripts/agent-commit -m "docs(docs): consolidate watchdog plan under parallel-agent-coordination" \
  -m "Move the active watchdog plan into the umbrella topic, supersede the 2026-06-21 build plan, update references. Part-A plan (consumed) and the watchdog plans now share one topic slug."
```
Expected: `cross-session-watchdog/` no longer exists; all references resolve; the umbrella folder holds the consumed Part-A plan, the consumed old build plan, and this active plan.

---

## Phase 1 — Prove unattended idle-wake (the riskiest unknown)

The whole "primary" wake path rests on one unproven behavior: **does an idle `claude` session, sitting at the prompt with no human present, re-enter and act when its own background watcher exits (P1) or its own durable cron fires (P2)?** PUSH was already proven in a real idle TUI; this proves (or refutes) PULL and picks the primary path. Nothing downstream is built until this passes.

**Files:**
- Move: `/tmp/wd_pty_proof.py` → `tools/watchdog/wd-pty-proof.py` (re-derivable evidence)
- Create: `tools/watchdog/evidence/2026-06-26-idle-wake-results.md` (record PASS/FAIL)

- [x] **Step 1: Re-home the PTY proof so the existing evidence is committed.** *Done as deferral (2026-06-27):* `/tmp/wd_pty_proof.py` was absent at session resume; per the evidence file's Provenance section, the PTY proof pertains to the PUSH path (Phase 5, optional). It will be regenerated only if/when Phase 5 is taken up — no committed re-homing needed at this time.

- [ ] **Step 2: Manual idle-wake test — P1 background watcher.** In **terminal 1**, in the main worktree, launch `claude` and arm it (idle) with exactly: *"Run this in the background and do nothing else until it returns: `bash -c 'until test -f /tmp/wd_wake_demo; do sleep 2; done'`. When it returns, print WOKE and stop."* Walk away (no keystrokes in terminal 1). In **terminal 2**:

```bash
sleep 15 && : > /tmp/wd_wake_demo    # create the signal after B is confirmed idle
```
**PASS =** terminal 1 prints `WOKE` with no human keystroke. Record the exact latency and whether re-entry happened spontaneously vs. only after a later keystroke.

- [ ] **Step 3: Manual idle-wake test — P2 durable cron.** In terminal 1, arm idle `claude` to register a `durable` `CronCreate` firing every minute with the fixed prompt: *"If `/tmp/wd_wake_demo2` exists, print WOKE-CRON and stop; else do nothing."* Walk away. In terminal 2: `: > /tmp/wd_wake_demo2`. **PASS =** the next cron fire prints `WOKE-CRON` unattended. Note the fire latency and jitter.

- [ ] **Step 4: Record results and decide the primary path.** Write PASS/FAIL + latencies to the evidence file. **Decision gate:**
  - Both pass → **P1 primary** (low latency), **P2 durable fallback** — **but P2 may not be enabled as a wake path until the Phase 4 termination-guarantee contract (see "Termination guarantee" below) is shipped and tested.** Without those layers, a recurring `CronCreate` is a silent quota drain (see evidence file 2026-06-26-idle-wake-results.md, "Discoveries"); P1 is inherently drain-safe (one watcher, no recurring timer) and is the only path the MVP may rely on.
  - Only cron passes → **P2 primary**, conditional on the Phase 4 termination contract landing in the same change set as P2 activation.
  - Neither passes → **PULL is not viable unattended**; fall back to **PUSH (Phase 5) as the primary**, and the MVP's wake becomes tmux-based. (This is why Phase 5 stays specified even though it's "optional.")

- [ ] **Step 5: Commit evidence.**

```bash
cd <home>/Desktop/3_body_problem
rm -f /tmp/wd_wake_demo /tmp/wd_wake_demo2
GIT_AGENT_ID=watchdog-build \
GIT_AGENT_OWNED_PATHS='tools/watchdog/' \
scripts/agent-commit -m "test(governance): record unattended idle-wake results and re-home PTY proof" \
  -m "Manual two-terminal P1/P2 idle-wake evidence; selects the primary wake path for the MVP."
```

---

## Phase 2 — MVP: signal + gate + same-worktree handoff

Builds the essential core for the common (same-worktree) case. All scripts live under `tools/watchdog/`; tests under `tests/watchdog/` (python `unittest`, matching `tests/git_policy/`).

> *Executed 2026-06-28 (Phase 2 only).* MVP committed `f37469c4` (tools + `unittest`, all green); `wd-arm` missing-`--task-file` hardening in `dbca0af`. Same-worktree handoff confirmed end-to-end by the committed unittest **and** a two-tab live dry run — evidence: `tools/watchdog/evidence/2026-06-28-same-worktree-live-dryrun.md`. The Task 2.2/2.3 "commit a trivial change" smoke steps were instead verified in throwaway temp repos and against a clean tracked-file scope, to avoid junk commits on `master`. Phases 3–5 remain unexecuted, so the plan-level `execution_status` is intentionally left unset.

### Task 2.1 — Channel root resolver (absolute common-dir)

**Files:** Create `tools/watchdog/lib/wd-common.sh`.
**Interfaces:** Produces `wd_channel_root` and `wd_channel_dir NAME` → absolute paths under the shared git common dir.

- [x] **Step 1: Write the resolver** (normalizes the relative `.git` that the main worktree returns — the bug in the old plan; mirrors `scripts/agent-commit:16-21`).

```bash
#!/usr/bin/env bash
set -euo pipefail
wd_channel_root() {
  local repo_root common_dir
  repo_root="$(git rev-parse --show-toplevel)"
  common_dir="$(git rev-parse --git-common-dir)"
  case "$common_dir" in /*) : ;; *) common_dir="$repo_root/$common_dir" ;; esac
  printf '%s/live-monitor/channels' "$common_dir"
}
wd_channel_dir() { printf '%s/%s' "$(wd_channel_root)" "$1"; }
```

- [x] **Step 2: Verify it returns an identical absolute path from main and linked worktrees.**

```bash
( cd <home>/Desktop/3_body_problem && bash -c 'source tools/watchdog/lib/wd-common.sh; wd_channel_root' )
( cd <home>/Desktop/3_body_problem/.worktrees/specwork && bash -c 'source <home>/Desktop/3_body_problem/tools/watchdog/lib/wd-common.sh; wd_channel_root' )
```
Expected: both print `<home>/Desktop/3_body_problem/.git/live-monitor/channels`.

### Task 2.2 — Producer: `wd-publish-done`

**Files:** Create `tools/watchdog/wd-publish-done`.
**Interfaces:** Consumes `wd-common.sh`. Produces `<channel>/done.json` `{ stage, head, producer_ref, producer_worktree, scope, ts }`, written atomically (write-temp + `mv`), last-write-wins.

- [x] **Step 1: Write the publisher** (refuses to publish a dirty scope — the publish-time clean invariant).

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/wd-common.sh"
channel=; stage=; scope=
while [ $# -gt 0 ]; do case "$1" in
  --channel) channel=$2; shift 2;; --stage) stage=$2; shift 2;; --scope) scope=$2; shift 2;;
  *) echo "unknown arg: $1" >&2; exit 2;; esac; done
[ -n "$channel" ] && [ -n "$stage" ] && [ -n "$scope" ] || { echo "need --channel --stage --scope" >&2; exit 2; }
# shellcheck disable=SC2086  # scope is an intentional space-separated pathspec list
if [ -n "$(git status --porcelain -- $scope)" ]; then
  echo "wd-publish-done: scope has uncommitted changes; refusing to publish" >&2; exit 3
fi
dir="$(wd_channel_dir "$channel")"; mkdir -p "$dir"
head="$(git rev-parse HEAD)"; ref="$(git rev-parse --abbrev-ref HEAD)"
wt="$(git rev-parse --show-toplevel)"; ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
tmp="$dir/.done.json.tmp.$$"
printf '{"stage":"%s","head":"%s","producer_ref":"%s","producer_worktree":"%s","scope":"%s","ts":"%s"}\n' \
  "$stage" "$head" "$ref" "$wt" "$scope" "$ts" > "$tmp"
mv "$tmp" "$dir/done.json"
echo "published done @ $head ($ref)"
```

- [x] **Step 2: Smoke test** in the main worktree: commit a trivial change, then `tools/watchdog/wd-publish-done --channel demo --stage smoke --scope README.md`. Expected: `published done @ <sha>`; `cat .git/live-monitor/channels/demo/done.json` shows the fields.

### Task 2.3 — Consumer gate: `wd-check`

**Files:** Create `tools/watchdog/wd-check`.
**Interfaces:** Consumes `wd-common.sh` + `<channel>/done.json`. Prints one of `WAKE` | `IDLE` | `STALE:<reason>`; exits `0`/`10`/`20`.

- [x] **Step 1: Write the gate** (reachability → producer-stability → producer-cleanliness → optional integration). Newest-done-wins is automatic because `done.json` is overwritten atomically, dissolving the prior plan's livelock.

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/wd-common.sh"
channel=; require_integration=0; integration_ref=HEAD
while [ $# -gt 0 ]; do case "$1" in
  --channel) channel=$2; shift 2;; --require-integration) require_integration=1; shift;;
  --integration-ref) integration_ref=$2; shift 2;; *) echo "unknown arg: $1" >&2; exit 2;; esac; done
done_f="$(wd_channel_dir "$channel")/done.json"
[ -f "$done_f" ] || { echo IDLE; exit 10; }
jget() { sed -n 's/.*"'"$1"'":"\([^"]*\)".*/\1/p' "$done_f" | head -1; }
head="$(jget head)"; ref="$(jget producer_ref)"; wt="$(jget producer_worktree)"; scope="$(jget scope)"
git rev-parse --verify --quiet "${head}^{commit}" >/dev/null || { echo "STALE:unreachable"; exit 20; }
# shellcheck disable=SC2086
[ -z "$(git rev-list "${head}..${ref}" -- $scope 2>/dev/null)" ] || { echo "STALE:producer-advanced"; exit 20; }
# shellcheck disable=SC2086
if [ -d "$wt" ] && [ -n "$(git -C "$wt" status --porcelain -- $scope 2>/dev/null)" ]; then echo "STALE:producer-dirty"; exit 20; fi
if [ "$require_integration" = 1 ]; then
  git merge-base --is-ancestor "$head" "$integration_ref" || { echo "STALE:not-integrated"; exit 20; }
fi
echo WAKE; exit 0
```

- [x] **Step 2: Verify WAKE / STALE transitions by hand** (same-worktree): after Task 2.2's publish, `wd-check --channel demo` → `WAKE`. Then commit another change to `README.md` and re-run → `STALE:producer-advanced`. Re-publish → `WAKE` again.

### Task 2.4 — Consumer watcher + exactly-once claim + dead-A timeout: `wd-arm`

**Files:** Create `tools/watchdog/wd-arm`.
**Interfaces:** Consumes `wd-check`. The background body B runs; on exit prints `WAKE <head>` (claimed) / `ALREADY-CLAIMED <head>` / `PRODUCER-STALLED after Ns`. Exit `0`/`0`/`42`.

- [x] **Step 1: Write the watcher** (atomic `mkdir` claim keyed by head = the exactly-once guard shared by every wake path; bounded by an optional timeout = the dead-producer guard).

```bash
#!/usr/bin/env bash
set -uo pipefail
source "$(dirname "$0")/lib/wd-common.sh"
channel=; poll=20; timeout=0
while [ $# -gt 0 ]; do case "$1" in
  --channel) channel=$2; shift 2;; --poll-secs) poll=$2; shift 2;; --timeout-secs) timeout=$2; shift 2;;
  *) echo "unknown arg: $1" >&2; exit 2;; esac; done
dir="$(wd_channel_dir "$channel")"; here="$(dirname "$0")"; start="$(date +%s)"
while true; do
  st="$("$here/wd-check" --channel "$channel" || true)"
  if [ "${st%%:*}" = WAKE ]; then
    head="$(sed -n 's/.*"head":"\([^"]*\)".*/\1/p' "$dir/done.json" | head -1)"
    if mkdir "$dir/claimed.$head" 2>/dev/null; then echo "WAKE $head"; else echo "ALREADY-CLAIMED $head"; fi
    exit 0
  fi
  if [ "$timeout" -gt 0 ] && [ "$(( $(date +%s) - start ))" -ge "$timeout" ]; then
    echo "PRODUCER-STALLED after ${timeout}s"; exit 42
  fi
  sleep "$poll"
done
```

- [x] **Step 2: Persist the task payload at arm time** (F9 — so a woken B knows what to do even after a restart). The arming convention writes B's task to `<channel>/consumer-task.md`; the wake prompt is the **fixed constant**: *"Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result line; if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, stop and report."* Document this in the script header; never interpolate file contents into the prompt.

### Task 2.5 — Same-worktree end-to-end + negative tests (committed)

**Files:** Create `tests/watchdog/test_watchdog_mvp.py` (python `unittest`, shells out to the scripts in a throwaway temp git repo).

- [x] **Step 1: Write tests** covering: (a) publish→check returns `WAKE`; (b) producer-advanced → `STALE:producer-advanced`; (c) dirty scope → publish refused (exit 3); (d) `wd-arm` claims once — a second `wd-arm` on the same head returns `ALREADY-CLAIMED`; (e) `wd-arm --timeout-secs 1` with no done → `PRODUCER-STALLED` exit 42; (f) resolver returns an absolute path. Each test builds a temp repo with two commits and asserts stdout + exit code.

- [x] **Step 2: Run** `python3 -m unittest tests/watchdog/test_watchdog_mvp.py -v`. Expected: all pass.

- [x] **Step 3: Live same-worktree dry run** — two `claude` tabs in the main worktree: B arms `wd-arm --channel live` in the background + records its task; A commits + `wd-publish-done`. Expected: B re-enters (per Phase 1's proven path), claims, reads `consumer-task.md`, begins. Confirms the common-case path end-to-end.

- [x] **Step 4: Commit** the tools + tests.

```bash
cd <home>/Desktop/3_body_problem
GIT_AGENT_ID=watchdog-build \
GIT_AGENT_OWNED_PATHS='tools/watchdog/:tests/watchdog/' \
scripts/agent-commit -m "feat(governance): add watchdog signal, staleness gate, and exactly-once watcher (MVP)" \
  -m "wd-common/publish-done/check/arm + same-worktree end-to-end tests. Same-worktree handoff works; cross-worktree integration is Phase 3."
```

---

## Phase 3 — Cross-worktree support (secondary capability)

Same-worktree needs no integration (shared tree). Cross-worktree, B must pull A's commit into its own branch before starting (user decision: **B integrates; watchdog signals only**).

### Task 3.1 — Integration step + gate variant

**Files:** Create `tools/watchdog/wd-integrate`; the gate variant already exists (`wd-check --require-integration`).

- [ ] **Step 1: Write `wd-integrate`** — fast-forward-or-merge A's `done.head` into B's branch; on conflict, abort and surface (never leave a half-merge in an unattended path).

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/wd-common.sh"
channel=$2   # --channel NAME
done_f="$(wd_channel_dir "$channel")/done.json"
head="$(sed -n 's/.*"head":"\([^"]*\)".*/\1/p' "$done_f" | head -1)"
git merge-base --is-ancestor "$head" HEAD && { echo "already-integrated"; exit 0; }
if git merge --no-edit "$head"; then echo "integrated $head"; else
  git merge --abort; echo "CONFLICT integrating $head — manual merge required" >&2; exit 4
fi
```

- [ ] **Step 2: Wake sequence for cross-worktree** = `wd-arm` (WAKE) → `wd-integrate` → `wd-check --require-integration` (now passes) → begin. Document this ordering in the arm header.

### Task 3.2 — Cross-worktree end-to-end test (committed)

- [ ] **Step 1: Add `tests/watchdog/test_watchdog_xworktree.py`** — temp repo with two linked worktrees on different branches; A commits on its branch + publishes; assert `wd-check --require-integration` returns `STALE:not-integrated`, then `wd-integrate` succeeds, then it returns `WAKE`; and a conflicting B-edit makes `wd-integrate` exit 4 cleanly (no half-merge). Run with `python3 -m unittest`.

- [ ] **Step 2: Commit** (`feat(governance): add watchdog cross-worktree integration step and test`).

---

## Phase 4 — Durable wake + packaging (deferred until 0–3 land)

Forward outline; detail finalized after the Phase 1 decision.

- **P2 durable cron arming.** A `durable CronCreate` firing the fixed wake prompt into idle B every N minutes; B runs `wd-check` + claim. Survives restarts/long idle. Note the documented ceilings: 7-day auto-expiry, ≤15-min jitter — surface these to the user when arming. **P2 may only be enabled once the "Termination guarantee" contract below is implemented and committed** (see Step 4 of Phase 1: P2 is a fallback, not the primary, and is gated on the termination layers).
- **Packaged skill** at `.claude/skills/cross-session-watchdog/SKILL.md`, exposing `arm-consumer` (B: write task, install P1 watcher and/or P2 cron, register channel + scope + integration flag) and `publish-done` (A). The skill loads the GSD adapter (Phase 5) only when present.

### Termination guarantee (hard requirement — discovered 2026-06-26)

**Why this exists.** The P2 idle-wake test (see `tools/watchdog/evidence/2026-06-26-idle-wake-results.md`) confirmed that a recurring `CronCreate` wakes idle B correctly, but exposed a load-bearing risk: a recurring timer that fires every minute against an unattended session is a **silent quota drain** — usage accumulates even when no one is watching, and the user has no obvious place to look for "why is my usage going down?" The P1 background-watcher path is inherently drain-safe (one watcher process, no recurring timer) and is therefore the only MVP-eligible path. P2 may only ship if and when every layer below is in place.

**Constraint source:** user directive 2026-06-26, grounded in the observed drain behavior of the just-completed test.

**Five layers — every layer is required, no shortcuts:**

1. **Disarm-on-success.** When the watchdog's job is done (`wd-arm` returned `WAKE <head>` and B successfully claimed), the arming skill **must** delete the cron / kill the watcher as its first action after the wake prompt fires. No "leave it running in case I need to re-wake" — that is exactly the leak.
2. **Self-termination (TTL + disarm flag).** Every recurring timer the watchdog arms carries an explicit `--ttl` (or equivalent) bounding parameter. When the TTL expires, the wake prompt itself deletes the cron / kills the watcher before doing anything else. A separate **disarm flag** (e.g. `<channel>/disarm` sentinel in the channel dir, OR a sentinel file the wake prompt checks first) lets a finished handoff tell an in-flight timer to stand down on its very next fire. TTL is the backstop; disarm is the fast path.
3. **External kill-switch — `wd-disarm`.** A standalone script under `tools/watchdog/wd-disarm` that the user (or another agent) can invoke at any time to forcibly remove **every** watchdog-armed timer and watcher the tool can see, on every worktree it can reach. Must be idempotent and safe to call repeatedly. The arming step's documentation must call this out: *"if anything goes wrong, `wd-disarm` cleans up."*
4. **Visibility — `wd-status`.** A standalone script that lists every active watchdog timer + watcher across all reachable worktrees (channel name, what it watches, when it was armed, when its TTL expires, when it last fired, who armed it). Drain troubleshooting starts here: if the user thinks the watchdog is leaking, `wd-status` shows whether a timer is live and where.
5. **Conservative defaults.** No recurring timer may be armed with `durable: true` without the user **explicitly** opting in at arm time (default = `durable: false`, session-only, dies when the owner session ends). Cron frequency defaults to the longest interval the wake SLA permits, not the shortest. TTL defaults to a small multiple of the expected handoff duration — never "forever / 7 days" unless the user names a specific long-running handoff. Every deviation from a default is printed in the arming output so the user sees what they just authorized.

**Skill integration.** The packaged `arm-consumer` skill (Phase 4, second bullet) MUST refuse to arm P2 unless (a) the user typed an explicit "yes, durable" at the prompt, (b) a TTL was supplied, and (c) `wd-disarm` and `wd-status` exist on disk and pass their own smoke tests. The skill MUST print, after every successful arm: the channel, the TTL, when the TTL expires, the disarm command, and the status command.

**Verification.** A committed test under `tests/watchdog/test_termination.py` must cover at least: arming a recurring timer with a 2-second TTL and asserting the timer is gone at T+3s; arming and then calling `wd-disarm` and asserting the timer is gone immediately; `wd-status` reporting the timer while live and not reporting it after disarm. The full Phase 1 evidence file's "Discoveries" section is the regression target — re-running it after Phase 4 lands must show: arm → drains-while-idle → TTL-or-disarm removes the timer → no further firings → `wd-status` confirms empty.

**Out of scope for this contract:** the user's choice of how often a recurring timer may fire, the wake prompt text (still a fixed constant), and the choice of P2 vs PUSH as a backup wake path. Those remain user-driven.

## Phase 5 — Optional PUSH accelerator + GSD adapter (opt-in)

- **PUSH (tmux).** If the Phase 1 decision kept PULL primary, PUSH is a low-latency accelerator for users already in tmux: external watcher runs `wd-check`; on WAKE, the **two-call** shim (proven 2026-06-22) — `tmux send-keys -t agentB '<fixed prompt>'` then a separate `tmux send-keys -t agentB Enter`. Precondition checks: B is a named pane at a clean idle prompt; re-test after `claude` TUI upgrades. (tmux 3.6b is installed.) If Phase 1 found PULL non-viable, this becomes the primary path instead.
- **GSD adapter (L3).** Maps GSD onto the generic core: phase → `stage`; the `verify(NN)` commit → `done.head`; phase-scope paths → `scope`. Ships as a separate file; the core stays generic.

---

## Verification (end-to-end)

| What | How | Pass criteria |
|---|---|---|
| Idle-wake (the crux) | Phase 1 manual two-terminal, P1 & P2 | B acts unattended; primary path chosen and recorded |
| Resolver correctness | run from main + linked worktree | identical absolute path |
| Signal + gate | `python3 -m unittest tests/watchdog/test_watchdog_mvp.py` | WAKE/STALE/refuse-dirty all pass |
| Exactly-once | second `wd-arm` on same head | `ALREADY-CLAIMED`, no double-start |
| Dead-A timeout | `wd-arm --timeout-secs 1`, no done | `PRODUCER-STALLED` exit 42 |
| Same-worktree handoff | Phase 2 live dry run | B wakes, claims, begins its armed task |
| Cross-worktree | `test_watchdog_xworktree.py` + live | integrate→WAKE; conflict aborts cleanly |

## Risks, non-goals, scope guard

- **Honest guarantee:** the gate cannot stop a willful producer from working past `done`; it guarantees unambiguous publish + consumer-side staleness detection. Accepted.
- **Capability precondition:** both wake paths assume B's `claude` session has the scheduling/background tools (same launch profile). The arm step checks for them.
- **Recurring-timer drain (HIGH; captured 2026-06-26).** A `CronCreate` armed with `durable: true` and no termination contract is a silent quota drain against the owning session — observed in the P2 test. Mitigated by the Phase 4 termination-guarantee contract (disarm-on-success, self-termination TTL, external `wd-disarm`, visibility `wd-status`, conservative defaults) and by gating P2 activation on that contract landing.
- **macOS background-tab throttle (MEDIUM; captured 2026-06-26).** `CronCreate` does not fire reliably when the consumer session is in a backgrounded terminal tab on macOS — the timer pauses with the rest of the tab's process group. P2 therefore requires B's TUI to be foreground (or near-foreground) for the wake to fire in a timely manner. The arming skill warns the user about this; documented as a P2 capability precondition, not a bug to fix.
- **Agent-armed `durable: true` crons can come out session-only (MEDIUM; captured 2026-06-26).** When a `claude` agent invokes `CronCreate` on the user's behalf with `durable: true`, the job has been observed persisting as session-only (lives only in the agent's process memory, not in `.claude/scheduled_tasks.json`) on at least one path through the harness. The arming skill must therefore **verify persistence on disk** immediately after arming and refuse to consider the arm complete until `CronList` shows the job AND `.claude/scheduled_tasks.json` contains it; otherwise the wake is silently non-durable.
- **Out of scope:** separate clones or separate machines (the channel assumes one shared git common dir); auto-integration with no human (user chose B-integrates); rewriting/force-pushing `producer_ref` after publish.
- **Scope guard:** Phases 0–3 are the build. Phases 4–5 begin only after 0–3 land, the Phase 1 decision is recorded, AND the Phase 4 termination-guarantee contract lands before any P2 activation.

## Self-review (writing-plans checklist)

- **Coverage:** every prior-review finding maps to a task — F1→Phase 3 + Task 2.x reframing; F2→Phase 1 + decision gate; F4→Task 2.3 newest-done-wins; F5→Task 2.1; F6→Task 2.4 claim; F8→Task 2.4 timeout; F9→Task 2.4 Step 2; F11→Phase 0 (umbrella + supersede); F12→implicit (tmux noted installed in Phase 5).
- **No placeholders in the active scope (Phases 0–3):** every code step shows runnable code; every test step names the file and the assertions; Phases 4–5 are explicitly deferred-by-decision, not TODOs.
- **Type/name consistency:** `wd-common.sh`/`wd-publish-done`/`wd-check`/`wd-arm`/`wd-integrate`, `done.json` fields `{stage,head,producer_ref,producer_worktree,scope,ts}`, and the `WAKE`/`IDLE`/`STALE:*`/`ALREADY-CLAIMED`/`PRODUCER-STALLED` vocabulary are used consistently across tasks and tests.
