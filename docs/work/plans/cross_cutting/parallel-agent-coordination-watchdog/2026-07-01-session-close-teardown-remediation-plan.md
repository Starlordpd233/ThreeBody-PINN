---
status: active
purpose: implementation-plan
created: 2026-07-01
milestone: untracked
phase: cross-cutting
execution_status: not-executed
review_status: pending
retirement_trigger: >
  Retire when the session-close teardown guarantee is implemented and landed —
  the wd-arm owner-liveness self-check, the bounded-TTL default, and the
  SessionEnd disarm wiring (or the user-approved subset), with tests and
  install-global.sh propagation — OR when superseded by a revised teardown plan.
  Re-open on any change to wd-arm/wd-push/lib/wd-common.sh, install-global.sh,
  the SessionEnd hook wiring, or Claude Code harness background-Bash lifecycle
  behavior.
---

# Cross-Session Watchdog — Session-Close Teardown Remediation Plan

## 1. Problem

The watchdog's consumer watcher (`wd-arm`) is a background shell poll-loop. The
skill's safety story assumes that when the arming Claude session goes away, the
watcher goes away with it. **It does not.** Closing the terminal tab, typing
`/quit`, or a hard kill of the session can leave the watcher running as an
orphan, polling indefinitely. With the watchdog installed globally and armed
across many projects, these orphans accumulate silently.

This plan specifies a teardown guarantee: **when the arming session ends — by any
exit path, including hard kills — its watcher terminates within a bounded time,
in every project the global skill reaches.** No code is changed by this
document; it is the reviewed plan of record for that work.

## 2. Evidence (measured 2026-07-01, this machine)

| # | Finding | How observed |
|---|---------|--------------|
| E1 | Bash-tool background processes are `setsid`'d into their **own session with no controlling terminal** (`STAT=Ss`, `tty=??`), as a direct child of the `claude` process. | Live `ps` of a real `run_in_background` marker: `PPID=<claude pid>`, `Ss`, `tty ??`. |
| E2 | A child **survives `kill -9` of its parent** and its live PPID **flips to `1`** (launchd). | Self-contained reparent experiment; child logged `live_ppid` before (real parent) and after (`1`), still alive. |
| E3 | **A real orphaned watcher was already running in the wild.** `wd-arm --channel phase-36-xconverge-to-execution`, `PPID=1`, `PGID=43928` (leader gone), age ~86 min, still polling every 20 s. Its arming session had already exited. | `wd-status` + `ps -p 43930`. |
| E4 | The orphan will only die because it was armed with `--timeout-secs 7200` (self-terminates at TTL). **`wd-arm --timeout-secs` defaults to `0` = poll forever.** | `wd-arm` source (`timeout=0`; the timeout branch is skipped when `0`). |
| E5 | **No `SessionEnd`/`Stop` hook runs `wd-disarm`.** The one `SessionEnd` hook on this profile runs `scripts/git_policy/presence_hook.sh deregister` only. | `settings.json` scan across profiles; `presence_hook.sh` contains no watchdog reference. |
| E6 | The verification strategy enumerates every "Termination" scenario (disarm sentinel, SIGTERM/TERM-trap, TTL, `wd-disarm --all`, `wd-status`) but **omits "the arming session ends."** Every tested teardown path requires an *external* signal; session-close signals nothing. | `2026-06-30-watchdog-verification-strategy.md` §3 "Termination" row. |

### Why closing the tab does not signal the watcher

Closing the terminal tab delivers `SIGHUP` down the terminal's own process chain
(`ghostty → login → zsh → claude`). Because the watcher lives in a **separate
session with no controlling terminal** (E1), that hangup never reaches it. The
watcher's death then depends entirely on whether the dying `claude` process
actively kills its children — which does not happen on a hard exit (tab close,
`kill -9`, crash, laptop force-quit). The watcher is reparented to launchd and
keeps polling (E2, E3). Once orphaned it is also **useless**: no live session
remains for the harness to re-enter on wake, so it is pure dead weight until its
TTL (if any) reaps it.

> Note on the term "drain-safe." SKILL.md calls P1 "inherently drain-safe." That
> is true only in the **quota** sense (no recurring API-consuming timer, unlike
> P2 cron). It is **not** a process-teardown guarantee. SKILL.md wording must be
> qualified (§5.4) so the claim is not read as "the process dies on session
> end."

## 3. Goal / success criteria

Let *S* be the Claude session that armed a watcher *W*.

1. **G-graceful:** `/quit` (or Ctrl-D) in *S* ⇒ *W* terminates promptly (≤ a few
   seconds), clean standdown, `armed.json` removed.
2. **G-tabclose:** closing *S*'s terminal tab ⇒ *W* terminates within ≤ one poll
   interval after the session process is gone.
3. **G-hardkill:** `kill -9` of the session / crash / force-quit ⇒ *W* terminates
   within ≤ one poll interval (this is the case hooks cannot cover).
4. **G-bounded:** even if 1–3 all fail, *W* self-terminates within a bounded,
   declared TTL — never "forever."
5. **G-global:** guarantees 1–4 hold in **every** project the global skill
   reaches, not just this repo, with no per-project setup.
6. **G-nonregress:** the wake path still works — a watcher whose session is alive
   is never stood down early; exactly-once claim, cross-worktree integrate, and
   `wd-push`/P2 parity are unchanged.

## 4. Design — defense in depth (three layers)

Ordered by robustness. Layer 1 is the centerpiece and is sufficient for
G-graceful/tabclose/hardkill on its own; Layers 2–3 add speed and a final bound.

### Layer 1 — owner-liveness self-check baked into `wd-arm` (centerpiece)

The watcher ties its own life to the arming session and stands down when the
session process is gone. This is the only layer that covers **hard kills**
(reparenting always happens) and it travels with the tool to every project
(G-global), so it needs no per-project wiring.

**Mechanism (recommended): snapshot the owner pid at arm, re-check each poll.**

At arm time, before the loop:

```sh
# The arming session's process that owns this background job. For the canonical
# run_in_background path this is wd-arm's parent (the harness job wrapper), whose
# lifetime tracks the session (confirmed by the E3 orphan structure: the wrapper
# died exactly when the session ended, leaving wd-arm at PPID 1).
owner_pid="${WD_OWNER_PID:-$PPID}"          # --owner-pid override for manual/tmux use
owner_start="$(ps -o lstart= -p "$owner_pid" 2>/dev/null || true)"  # PID-reuse guard
```

Add to the top of each poll iteration (before `wd-check`):

```sh
# Owner-liveness standdown: if the arming session process is gone (or its pid was
# reused by an unrelated process), stand down. Covers /quit, tab-close, and hard
# kills (kill -9/crash/force-quit) — all of which end the owner or orphan us.
cur_ppid="$(ps -o ppid= -p $$ 2>/dev/null | tr -d ' ')"
owner_now="$(ps -o lstart= -p "$owner_pid" 2>/dev/null || true)"
if [ "${cur_ppid:-1}" = 1 ] || [ -z "$owner_now" ] || [ "$owner_now" != "$owner_start" ]; then
  remove_armed_record
  echo "SESSION-GONE"
  exit 0
fi
```

- `cur_ppid == 1` ⇒ orphaned (reparented to launchd) ⇒ owner chain is gone.
  PID-reuse-proof.
- `owner_now` empty ⇒ owner pid no longer exists.
- `owner_now != owner_start` ⇒ owner pid was reused by a different process
  (start-time mismatch) ⇒ treat as gone. Removes the reused-pid hazard.
- New terminal verdict `SESSION-GONE` (exit 0), added to the vocabulary in
  `wd-arm` header, SKILL.md, and the T0 vocab-parity check.

**Design decisions to confirm (see §8):** (a) watch the direct parent pid
(simple; correct for the canonical path) vs. walk up to the `claude` node pid
(robust to wrapper lifetime, but process-name dependent); (b) keep or drop the
`lstart` reuse guard; (c) `--owner-pid`/`WD_OWNER_PID` override for the manual
`&` and tmux forms so they are not stood down early.

**Latency:** ≤ one `--poll-secs` interval. With the default 20 s poll, a
hard-killed session's watcher dies within ~20 s.

### Layer 2 — `SessionEnd` → `wd-disarm --all` (fast graceful path)

Wire `wd-disarm --all` to run on `SessionEnd` so `/quit` (and tab-close, if the
harness runs `SessionEnd` on `SIGHUP`) cleans up **immediately** rather than
waiting a poll interval. This reuses the proven `SessionEnd` hook slot already
used for presence-deregister.

- Option 2A: append a second hook command to the existing `SessionEnd` array.
- Option 2B: call `wd-disarm --all` from inside `presence_hook.sh deregister`.
- Must be non-fatal and fast (short `timeout`), best-effort, and resolve the
  tool by absolute path (`~/.claude/skills/cross-session-watchdog/bin/wd-disarm`)
  so it works from any project.

**Not sufficient alone:** `SessionEnd` is not guaranteed on `kill -9`, crash, or
force-quit (already noted in the global-presence-awareness design). Layer 2 is
the fast path; Layer 1 is the guarantee. This layer is also **profile-specific
wiring**, so it does not satisfy G-global by itself — another reason Layer 1
carries the guarantee.

### Layer 3 — bounded `--timeout-secs` default (final backstop)

Change `wd-arm` so a P1 arm can never poll forever:

- Option 3A: change the default `--timeout-secs` from `0` to a bounded value
  (e.g. 1800 s), so an arm without an explicit timeout still self-terminates.
- Option 3B (stricter): the **skill** refuses to arm P1 without an explicit
  `--timeout-secs`, and `0` (forever) is disallowed for unattended arms.

This caps the blast radius of any leak that somehow escapes Layers 1–2 to a known
duration (this is exactly what saved orphan E3). Applies equally to the P2 cron
TTL, which is already mandatory.

### Layer interaction

Independent and complementary: Layer 1 guarantees teardown on session death for
all exit modes; Layer 2 makes the common graceful case instant; Layer 3 bounds
the worst case unconditionally. Any one of the three prevents an *indefinite*
leak; together they give prompt teardown with a hard ceiling.

## 5. Scope of code changes (for review — not yet applied)

### 5.1 `tools/watchdog/wd-arm`
- Snapshot `owner_pid` (+ `owner_start`) at arm; add the owner-liveness standdown
  block to the poll loop; add `--owner-pid` flag / `WD_OWNER_PID` env.
- Add `SESSION-GONE` to the header's Output/exit contract.
- (Layer 3) change the `--timeout-secs` default or add the no-timeout guard.

### 5.2 `tools/watchdog/wd-push`
- Apply the **same** owner-liveness standdown to the external push-watcher loop
  for parity (it shares the `armed.json`/`disarm` lifecycle). Note: `wd-push`
  runs from the operator terminal, so "owner" there is the operator shell, not a
  claude session — confirm the intended owner semantics for PUSH (§8).

### 5.3 `SessionEnd` wiring (Layer 2) — profile settings and/or `presence_hook.sh`
- Add the best-effort `wd-disarm --all` call per Option 2A/2B.

### 5.4 `.claude/skills/cross-session-watchdog/SKILL.md`
- Document the `SESSION-GONE` verdict and the teardown guarantee.
- Qualify the "drain-safe" claim (quota, not process teardown).
- State the bounded-TTL default / requirement.

### 5.5 `tools/watchdog/install-global.sh`
- No structural change, but **must be re-run** after 5.1–5.4 to propagate the
  updated `wd-*` scripts and SKILL.md to the canonical
  `~/.claude/skills/cross-session-watchdog/` and the `alt`/`free`/`max` profile
  symlinks (E5 shows the global install is the surface that matters).

## 6. Tests to add (`tests/watchdog/`)

Extend the existing suite (mirrors the verification-strategy tiers):

- **T-own-1 (unit/process):** arm a watcher with `--owner-pid <pid-of-a-sleep>`;
  `kill -9` the sleep; assert the watcher prints `SESSION-GONE` and removes
  `armed.json` within one poll interval. Direct automated proof of G-hardkill.
- **T-own-2 (reuse guard):** owner pid dies and a new process takes the same pid;
  assert standdown still fires (start-time mismatch), no false "still alive."
- **T-own-3 (no false positive):** owner alive for several polls with no done
  marker ⇒ watcher keeps polling (G-nonregress); does not stand down early.
- **T-own-4 (orphan path):** parent exits so the watcher reparents to 1; assert
  `SESSION-GONE` via the `ppid==1` branch.
- **T-ttl-default:** arm with no `--timeout-secs`; assert it is bounded per the
  chosen Layer-3 option (not `0`/forever).
- **T-disarm-hook:** `SessionEnd` command invokes `wd-disarm --all` and it is
  idempotent/empty-safe (already covered for `wd-disarm`; assert the wiring).

Also add the missing **verification-strategy scenario**: a "Termination" row
"**owner session ends (graceful / tab-close / hard-kill)**" with these tests as
its cheapest-tier coverage, plus one live rehearsal (D-tier) using a throwaway
scratch session to confirm real harness behavior end-to-end.

## 7. Rollout

1. Land 5.1–5.4 on a feature/review branch (governance: not directly on a
   protected branch); atomic commits; watchdog commits use the **`governance`**
   scope (the commit-msg hook rejects a `watchdog` scope).
2. Run the watchdog test suite (`python3 -m unittest discover -s tests/watchdog`)
   — all green including the new tests.
3. Re-run `tools/watchdog/install-global.sh`; verify canonical + profile symlinks
   updated and `wd-status` exits 0 through each profile.
4. One live confirmation per exit mode (graceful `/quit`, tab-close, `kill -9`)
   using a throwaway channel; record evidence under `tools/watchdog/evidence/`.

## 8. Decisions to confirm before implementation

1. **Owner signal:** direct-parent pid (simple, correct for canonical path) vs.
   walk-up-to-`claude` pid (robust to wrapper lifetime, process-name dependent).
   *Recommendation: direct-parent pid + `ppid==1` orphan check + `lstart` reuse
   guard.*
2. **Layer 3 policy:** bounded default (3A) vs. mandatory explicit timeout (3B).
   *Recommendation: 3A with a conservative default (e.g. 1800 s), plus the skill
   surfacing the value at arm time.*
3. **SessionEnd wiring:** separate hook command (2A) vs. fold into
   `presence_hook.sh` (2B); and whether to wire it in all profiles or defer
   (since Layer 1 already gives the guarantee). *Recommendation: 2A, all
   profiles, as the fast path.*
4. **`wd-push` owner semantics:** what counts as the "owner" for the operator-run
   push-watcher, and whether it should stand down on operator-shell exit.
5. **PID-reuse guard:** keep the `lstart` start-time match (robust) or drop it
   (simpler). *Recommendation: keep.*

## 9. Non-goals

- P2 durable cron behavior (already gated, already has mandatory TTL + on-disk
  verification; only inherits the SKILL.md wording fix).
- The cross-project channel-resolution work (separate track).
- Killing or altering the existing orphan E3 (user chose to let its TTL reap it).

## 10. Risk / rollback

- **False-positive standdown** (watcher dies while its session is alive) would
  silently break a handoff. Mitigated by T-own-3 and the `--owner-pid` override;
  the `lstart` guard avoids reuse-driven flaps. This is the main risk and the
  reason for the recommended signal choice in §8.1.
- All changes are additive to shell scripts and one hook line; rollback is
  reverting the commits and re-running `install-global.sh`.
- No git history, dataset, or framework-spec surface is touched.

## 11. Related artifacts

- Design: `docs/work/designs/cross_cutting/parallel-agent-coordination-watchdog/2026-06-30-watchdog-verification-strategy.md` (§3 Termination row to extend).
- Plan of record: `.../2026-06-26-cross-session-watchdog-implementation-plan.md` ("Termination guarantee" section).
- Verification: `.../2026-06-30-watchdog-verification-plan.md`, `.../verification-steps.md`.
- Tools: `tools/watchdog/wd-arm`, `wd-push`, `wd-disarm`, `wd-status`, `lib/wd-common.sh`, `install-global.sh`.
- Skill: `.claude/skills/cross-session-watchdog/SKILL.md`.
- Memory: `cross-session-watchdog-design` (design location + status).
