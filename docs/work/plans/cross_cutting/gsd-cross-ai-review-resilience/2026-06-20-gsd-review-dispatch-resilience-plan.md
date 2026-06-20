---
status: active
purpose: implementation-plan
created: 2026-06-20
milestone: untracked
phase: cross-cutting
retirement_trigger: GSD cross-AI review dispatch is hardened so every selected reviewer either returns a real review or degrades to a labeled non-fatal stub within a bounded time, verified by a re-runnable doctor/self-test; or the dispatch is upstreamed into @opengsd/gsd-core.
---

# GSD Cross-AI Review Dispatch — Resilience Remediation Plan

## 1. Goal

Make `/gsd-review` and `/gsd-plan-review-convergence` (and the `gsd-autonomous` paths that
wrap them) **reliably dispatch every selected external AI reviewer**, so that each reviewer
either (a) returns a real review, or (b) degrades to a clearly-labeled, non-fatal stub
**within a bounded time** — never silently stalls the whole run, never spawns nothing, never
produces an empty `REVIEWS.md` section with no explanation.

Success is verifiable: a pre-flight **doctor** check reports per-reviewer PASS/FAIL/TIMEOUT
*before* the expensive run, and a real run of `--all` completes with every selected reviewer
accounted for.

> **This document is the plan, not the edit.** No skill files are modified by this artifact.
> See §8 (Concurrency) — `review.md` is being edited by another agent right now and is
> off-limits.

## 2. Scope — what actually dispatches external CLIs

Two user-facing skills, one shared dispatch engine, one downstream consumer:

| Skill (what you type) | Thin wrapper | Real logic | Role |
|---|---|---|---|
| `/gsd-review` | `skills/gsd-review/SKILL.md` | `gsd-core/workflows/review.md` (869 lines) | **The dispatch engine.** Detects CLIs, builds prompt, invokes each reviewer, writes `REVIEWS.md`. |
| `/gsd-plan-review-convergence` | `skills/gsd-plan-review-convergence/SKILL.md` | `gsd-core/workflows/plan-review-convergence.md` (381 lines) | Loop: plan → spawn an **Agent** that runs `gsd-review` → parse counts → replan → repeat. **Does not dispatch CLIs itself** — it delegates to `review.md` inside a subagent. |
| `/gsd-autonomous --converge`/`--cross-ai` | `skills/gsd-autonomous/SKILL.md` | `gsd-core/workflows/autonomous.md` | Calls `gsd-plan-review-convergence` per phase (`autonomous.md:371,388,409`). Inherits all of its fragility; adds none of its own. |

**All CLI dispatch funnels through `review.md`.** That is the single file whose robustness
determines whether reviewers spawn. `next.md` and `reapply-patches.md` mention the CLI names
but do **not** dispatch reviews. (`coderabbit` also appears in `code-review.md`/`ship.md`, a
different "review the git diff" path; `coderabbit` is not installed here, so it is out of
primary scope.)

### Dispatch flow (plain language)

1. You run `/gsd-review --phase N --all` (or convergence, which spawns a subagent that does the same).
2. The agent reads `review.md` and **hand-translates ~15 prose Bash blocks into real Bash tool calls** — one cluster per reviewer.
3. It resolves the `gsd-tools.cjs` "shim" (a Node helper used for every `config-get`), detects which CLIs exist, builds the prompt to `/tmp/gsd-review-prompt-<phase>.md`.
4. It invokes each selected reviewer **sequentially** (to avoid rate limits), each writing to `/tmp/gsd-review-<slug>-<phase>.md`.
5. It concatenates the per-reviewer files into `NN-REVIEWS.md` and commits.

The fragility is concentrated in steps 2–4: the dispatch is **agent-interpreted prose**, not a
deterministic program, and the per-reviewer blocks are **unevenly hardened**.

## 3. Failure taxonomy (evidence-backed)

Severity: 🔴 confirmed on this machine · 🟠 latent/structural · 🟡 environmental.

### F1 🔴 — `gsd-tools` shim cannot find this machine's config home
`review.md:17` (and `plan-review-convergence.md:59`) resolve the shim through a long
`elif` chain. The chain probes `$RUNTIME_DIR`/git-toplevel/`pwd`, then `.claude/`, `.codex/`,
`command -v gsd-tools`, then **`$HOME/.claude-max-max/`** (a directory that does not exist),
then a dozen other tool dirs — but **never plain `$HOME/.claude-max/`**, which is where the
shim actually lives (`~/.claude-max/gsd-core/bin/gsd-tools.cjs`, confirmed present).
- Reproduced conditions: `RUNTIME_DIR` **unset**, `gsd-tools` **not on PATH**, `CLAUDE_CONFIG_DIR=~/.claude-max` (set but **unused** by the chain).
- Consequence: if the skill runner does not inject `RUNTIME_DIR`, the chain falls through to `echo "ERROR: gsd-tools.cjs not found" >&2; exit 1` — **aborting the entire review before any CLI spawns**. Even when it does not hard-abort, every `gsd_run query config-get …` returns empty, so all model/host/budget config silently reverts to defaults.
- Matches memory note: *"gsd-tools shim auto-detect misses ~/.claude-max."*
- **Fix:** make `$CLAUDE_CONFIG_DIR/gsd-core/bin/gsd-tools.cjs` the **first** branch; add an explicit `$HOME/.claude-max/` branch; treat `.claude-max-max` as the typo it is (F3).

### F2 🔴 — `claude` is shadowed by a shell function; native `--claude` never hits the real binary
`type claude` resolves to a function: `claude () { _claude_profiles_ccp pro "$@" }` (from the
zsh snapshot the Bash tool sources). The native Claude block at `review.md:337-339`
(`cat … | claude -p -`) therefore invokes the **CCP `pro` wrapper**, not the real Claude CLI.
- The CCP map (`config-defaults.manifest.json:99`) already maps slug `claude → profile pro`, and the dispatch rule says a mapped slug "overrides the native `--claude` binary path." So *when the shim resolves*, `--claude` is correctly routed through `ccp pro`. **But when F1 fires** (shim fails → `CCP_MAP` empty), dispatch falls back to the native block → the wrapper function → ambiguous behavior with `-p -`.
- Matches memory note: *"claude (call real binary, not the CCP wrapper fn)."*
- **Fix:** never rely on the bare name `claude` resolving to a binary. Route `--claude` through CCP explicitly (map already supports it), and if a native binary path is ever needed, resolve it with `command claude` / an absolute path so a shell function can never shadow it.

### F3 🔴 — `.claude-max-max` systemic substitution artifact (~90 files)
The literal string `claude-max-max` appears in **~90 gsd-core files** (`review.md` ×1 at the
shim; `plan-review-convergence.md` ×4, including its `<required_reading>` at lines 12–14). This
is not a typo in one place — it is a global `claude → claude-max` rewrite applied **on top of an
already-`.claude-max` path**, producing the doubled `claude-max-max`. `~/.claude-max-max` does
not exist.
- Consequence for the review path: poisons the F1 shim fallback branch, and makes convergence's `@$HOME/.claude-max-max/gsd-core/references/{revision-loop,gates,agent-contracts}.md` includes **silently fail to load** (the loop runs without its own contract guidance). Across the other ~85 files it mostly suppresses `@`-include guidance (quality degradation, not hard failure), which is why daily GSD still "works."
- **Fix:** scope decision required — see **Open Question Q1**.

### F4 🟠 — Uneven per-reviewer hardening (the core structural defect)
The other agent has been hardening `review.md` reviewer-by-reviewer, but coverage is asymmetric.
A robust reviewer block has **four** properties; a fragile one is missing some:

| Reviewer | Killable single proc | Hard watchdog timeout | stderr captured | empty/whitespace guard | Verdict |
|---|:--:|:--:|:--:|:--:|---|
| CCP profiles (`review.md:297-318`) | ✅ `< file` | ✅ `CCP_TIMEOUT=300` | ✅ `.err` | ✅ | **Robust** |
| OpenCode (`:367-385`) | ✅ `< file` | ✅ `OPENCODE_TIMEOUT=180` | ❌ `/dev/null` | ✅ | Good (stderr hidden) |
| Antigravity/agy (`:409-515`) | n/a (arg) | ✅ `--print-timeout 300s` | ✅ (transcript) | ✅ 3-layer | **Robust** |
| Ollama/LM Studio/llama.cpp (`:517-701`) | n/a (HTTP) | ✅ `curl --max-time 120` | n/a | ✅ | **Robust** |
| Codex (`:343-357`) | ⚠️ `cat \|` pipe | ❌ **none** | ✅ `.err` | ✅ | Fragile (no timeout) |
| Cursor (`:395-407`) | n/a (arg) | ❌ **none** | ✅ `.err` | ✅ | Fragile (no timeout) |
| **Gemini** (`:326-332`) | ❌ `cat \|` pipe | ❌ **none** | ❌ `/dev/null` | ❌ **none** | **Fragile** |
| **Native Claude** (`:334-341`) | ❌ `cat \|` pipe | ❌ **none** | ❌ `/dev/null` | ❌ **none** | **Fragile** + F2 |
| **Qwen** (`:387-393`) | ❌ `cat \|` pipe | ❌ **none** | ❌ `/dev/null` | ✅ | **Fragile** (no timeout) |
| CodeRabbit (`:359-365`) | n/a | ❌ relies on Bash-tool `timeout:360000` | ❌ `/dev/null` | implicit | Fragile (not installed here) |

The reviewers with **no watchdog** are the stall vector: because dispatch is **sequential**,
any one of Gemini / native-Claude / Codex / Qwen / Cursor hanging (init stall, keychain prompt,
auth wait, network) **sticks the entire run** — exactly the "stalls and gets stuck midway"
symptom. The `cat prompt | cli` pipeline form compounds it: the watchdog-kill pattern can only
kill a single PID, not a pipeline (the robust blocks deliberately use `cli - < file`).

### F5 🟠 — Bash-tool 600 s ceiling vs. sequential multi-reviewer dispatch
When convergence spawns the review Agent, that Agent runs dispatch through the **Bash tool**,
whose timeout defaults to 120 s and **maxes at 600 s**. Today's in-script watchdogs are
180–300 s **per reviewer**, run sequentially.
- If the agent puts all reviewers in **one** Bash call: worst case ≈ N×300 s (6 reviewers ≈ 1800 s) → the Bash tool **hard-kills at 600 s**, truncating later reviewers and **orphaning** the background `sleep`/watchdog processes.
- If it puts each reviewer in its **own** Bash call but forgets to raise that call's `timeout` above the in-script watchdog → the tool kills before the watchdog reaps.
- `review.md` only tells the agent the right Bash-tool timeout for **one** reviewer (CodeRabbit: "Use `timeout: 360000`"). For all others the agent guesses.
- **Fix:** the dispatch must declare a **total wall-clock budget** and either chunk reviewers so no single Bash call can exceed ~570 s, or move the whole sequence into one committed script invoked by exactly one Bash call with a known timeout (see §5, P3).

### F6 🟠 — Silent failures: stderr → `/dev/null` and `{phase}` placeholder drift
- The codex block's own comment (`review.md:345-347`, issue #1115) documents that suppressing stderr turned a flag error into "a silent empty review." The **same anti-pattern still exists** for Gemini, native-Claude, Qwen, OpenCode (`2>/dev/null`). Any failure there is undiagnosable.
- The blocks use a mix of literal `{phase}`, `${PHASE}`, `${PHASE_ARG}`, `${PHASE_DIR}`. The literal `{phase}` is a template the agent must substitute consistently across *write path* and *read path*. If a reviewer writes `…-gemini-7.md` but assembly reads `…-gemini-{phase}.md`, the section is blank with no error. Inconsistent naming is a real "produced no output" source.

### F7 🟡 — Antigravity (`agy`) headless auth returns null
`agy` is installed but returns null output under headless auth (memory note). The 3-layer
fallback (`review.md:409-515`) already makes this **non-fatal** — it degrades to a stub and
cannot hang or corrupt. So F7 is "never produces a real review," an **environment/auth** matter,
arguably out of scope for the skill. The doctor (§6) will surface it as `agy: FAIL (auth)` so it
is at least visible, and the user can drop `--agy` from routine runs.

### F8 🟠 — No pre-flight visibility
There is no way to know a reviewer is broken until a multi-minute real run half-completes. The
user's lived experience ("so many examples") is this discovery cost paid repeatedly. The single
highest-value user-facing fix is a cheap pre-flight (§6).

## 4. Target invariant — the uniform reviewer contract

Every reviewer block (CLI or HTTP) MUST satisfy all of:

1. **Single killable process** — `cli - < /tmp/prompt` (redirect), never `cat /tmp/prompt | cli` (pipeline). The watchdog kills a PID.
2. **Hard watchdog timeout** — background-launch + `( sleep "$T"; kill -TERM "$pid"; sleep 3; kill -KILL "$pid" )` (macOS ships no `timeout`/`gtimeout`). One per reviewer, env-overridable, sane default (≈180–300 s).
3. **stderr captured** to `/tmp/gsd-review-<slug>-<phase>.err` — never `/dev/null`.
4. **Empty/whitespace guard** — if output is zero-byte or whitespace-only, write a labeled stub (`"<slug> failed/timed out — stderr:"` + tail of `.err`) so a dead reviewer becomes a visible non-fatal section.
5. **Non-fatal isolation** — one reviewer's failure never aborts the others.
6. **Bash-tool-timeout alignment** — the caller sets the Bash tool `timeout` ≥ the block's worst case; the sequence as a whole respects the 600 s ceiling (chunk or script).

The robust reference implementations already in the file (CCP `:297-318`, OpenCode `:367-385`)
are the template to copy to the fragile reviewers.

## 5. Remediation phases

> Ownership is explicit because `review.md` is being edited concurrently (§8). "Mine" =
> files this plan may safely change; "Coordinate" = needs the other agent to land first.

### P1 — Doctor / self-test harness  *(mine; highest leverage; build first)*
Add a `--doctor` (a.k.a. `--self-test`) mode that, for each **selected** reviewer, sends a
trivial prompt ("Reply with the single word READY") with a short timeout (~20–30 s) and prints:

```
GSD ► REVIEW DOCTOR — phase N (reviewers: gemini, codex, qwen, claude-glm, agy)
  gemini       PASS   2.1s
  codex        PASS   3.4s
  qwen         PASS   2.8s
  claude-glm   FAIL   0.4s   (ccp profile glm: auth/keychain)
  agy          TIMEOUT 30s   (headless auth → null; drop --agy or re-auth)
```

This is **also the test harness** for every other phase (re-run after each fix). It turns
"silent stall at minute 8" into "claude-glm FAIL in 0.4 s, up front." Implementation lives in a
committed helper so it survives prose drift. Ship P1 before touching dispatch.

### P2 — Config-dir + shadow robustness  *(mine; does not require the other agent)*
- **Shim (F1/F3):** replace the brittle detect chain in the files I own with a `$CLAUDE_CONFIG_DIR`-first resolver; add explicit `$HOME/.claude-max/` branch; drop reliance on `.claude-max-max`.
- **Claude shadow (F2):** route `--claude` through CCP explicitly; if any native path remains, force `command claude`/absolute path.
- **Convergence required-reading (F3):** fix `plan-review-convergence.md:12-14` to `$CLAUDE_CONFIG_DIR` (this file is **not** the one under active edit — verify mtime before touching).

### P3 — Dispatch determinism  *(coordinate — overlaps review.md)*
The durable fix for F4/F5/F6 is to **extract dispatch from prose into one committed script**
(`gsd-review-dispatch.sh` or `.cjs`) that applies the §4 contract uniformly to every reviewer
and owns its own wall-clock budget. The skill's job shrinks to: build the prompt, call the
script once with the selected flags, assemble `REVIEWS.md`. **This overlaps `review.md`**, so it
must be sequenced **after** the other agent lands, or co-designed with them. Interim fallback if
extraction is rejected: copy the CCP/OpenCode watchdog template onto the five fragile reviewer
blocks in place (still review.md — still needs coordination).

### P4 — Systemic typo + update survival  *(needs user decision — Q1/Q2)*
- The ~85 non-review files carrying `.claude-max-max` (F3) — fix globally, root-cause the installer, or leave. **Q1.**
- Any in-place edit to `~/.claude-max` is **clobbered by `gsd update`** (memory: *"edits live in ~/.claude-max, protect from gsd update"*). Decide where the fix lives so it survives. **Q2.**

## 6. Verification strategy

1. **P1 doctor** is the primary gate: `/gsd-review --phase N --all --doctor` must show a PASS/FAIL/TIMEOUT line for **every** selected reviewer within ~30 s each. No hang, no blank.
2. **Bounded real run:** `/gsd-review --phase N --gemini --codex --qwen` completes and `NN-REVIEWS.md` has a non-empty section *or a labeled stub* for each — never a silent blank.
3. **Stall injection:** point one reviewer at an unreachable host / bad profile; confirm it degrades to a stub within its timeout and the **others still complete**.
4. **Convergence smoke:** one cycle of `/gsd-plan-review-convergence N --codex` returns a valid `CYCLE_SUMMARY:` line (proves the Agent→review→parse path survives).
5. **Ceiling check (F5):** time `--all`; confirm no single Bash call approaches 600 s and no orphan `sleep`/CLI processes remain (`pgrep -f 'gsd-review'` clean afterward).

## 7. Hypothesis (what is most likely biting the user)

The recurring "nothing spawned / stuck midway / no output" is dominated by **F1** (shim abort
or silent config loss), **F4 on the un-watchdogged reviewers** (one sequential stall freezes the
batch), and **F5** (Bash 600 s truncation on `--all`). F2 specifically corrupts `--claude`. The
P1 doctor will make all of these immediately visible; P2 eliminates F1/F2 for the paths I own.

## 8. Concurrency & safety constraints

- **`review.md` is under active edit by another agent** (mtime 22:30, minutes before this
  investigation; the file shows in-flight per-reviewer hardening with `#1115`/`#687` notes).
  **Do not edit `review.md`.** `~/.claude-max` is **not** a git repo — there is no merge; last
  writer wins, and a blind overwrite destroys their work. P2's convergence edit and P1's helper
  do not touch `review.md`; P3 does and must be sequenced/coordinated.
- **Back up before any edit:** `~/.claude-max` is untracked. Snapshot affected files (e.g. to
  `~/.claude-max/backups/`) before changing them so a bad edit or a `gsd update` is recoverable.
- **`gsd update` clobber:** see Q2.
- **No commit** is made by this plan; the artifact is informational until the user picks a path.
- **Governance:** this is tooling work in `~/.claude-max`, outside the 3-body PINN
  spec-adjudication domain, so the v1.6 STOP/grounding protocol does not apply. The repo
  `docs/` conventions govern only *where this artifact lives*.

## 9. Open questions (consequential forks — must decide before P3/P4)

- **Q1 — Scope of the config-dir / `.claude-max-max` fix.** (A) Narrow: only the review
  dispatch path. (B) Global: `.claude-max-max → .claude-max` across all ~90 files. (C)
  Root-cause the installer substitution so updates stop re-introducing it. Different blast radii.
- **Q2 — Update survival.** In-place edit + a documented reapply step (there is a
  `reapply-patches.md` workflow) / relocate the fix to an update-safe location / upstream into
  `@opengsd/gsd-core`.
- **Q3 — Dispatch shape.** Extract dispatch into a committed script now (best durability,
  overlaps `review.md`, needs coordination) / wait for the other agent to finish then extract /
  keep prose and just copy the watchdog template onto the five fragile reviewers.

## Appendix — investigation evidence (re-derivable)

- Skills: `~/.claude-max/skills/gsd-review/SKILL.md`, `…/gsd-plan-review-convergence/SKILL.md` (active set is `~/.claude-max`, the session's `CLAUDE_CONFIG_DIR`).
- Engine: `~/.claude-max/gsd-core/workflows/review.md` (869 ln), `…/plan-review-convergence.md` (381 ln).
- CCP map: `~/.claude-max/gsd-core/bin/shared/config-defaults.manifest.json:97-116` (16 slugs).
- `type claude` → `claude () { _claude_profiles_ccp pro "$@" }` (F2).
- `RUNTIME_DIR` unset · `CLAUDE_CONFIG_DIR=~/.claude-max` · `gsd-tools` not on PATH · `~/.claude-max/gsd-core/bin/gsd-tools.cjs` present · `~/.claude-max-max` absent (F1/F3).
- Installed: gemini, codex, opencode, qwen, cursor-agent, agy, ccp. Missing: coderabbit, ollama.
- `.claude-max-max` present in ~90 gsd-core files (F3).
- `autonomous.md:371,388,409` call `gsd-plan-review-convergence`.

## 10. Decisions locked (2026-06-20, user)

- **Architecture = own skills, new names.** Build `/xreview` (+ later `/xconverge`) under
  `~/.claude-max/skills/`, named **without** the `gsd-` prefix so GSD update/sync can never
  overwrite or delete them (`sync-skills.md:103` — "entries that do not start with `gsd-` are
  never touched"; `update.md:250-253` — non-`gsd-` custom items preserved). They carry the
  hardened dispatch themselves and do **not** depend on the broken `review.md`, so F1/F2/F3
  cannot affect them.
- **Drift-check requirement (user).** Each invocation compares the fork against the official GSD
  review files and **flags** (non-fatal) when the official versions have changed since the fork's
  recorded baseline — so we stay aware of upstream changes worth porting. Baseline stored at
  `~/.claude-max/skills/xreview/.sync-baseline.json` (per-file SHA-256 + GSD VERSION). Exposed as
  `xreview --check-sync` and run automatically at the start of every dispatch.
- **`.claude-max-max` = installer-baked, not agent corruption (confirmed).** Untouched typo'd
  files match their manifest hashes; `gsd-tools.cjs` has zero occurrences. Therefore: a clean
  reinstall **reproduces** the typo (ruled out — destructive *and* ineffective); an in-place
  global sweep is correct but reverts on the next `gsd update`. **Chosen route:** one-time global
  sweep (`claude-max-max → claude-max` across the ~90 `.md` files) **plus a post-update repair
  hook** so it survives updates. Requires a backup checkpoint first (untracked files).
- **Dispatch design = delegated to agent judgment (user).** Implement the §4 uniform reviewer
  contract as a single committed script (`dispatch.sh`) the skill calls once; add the §6 `--doctor`
  pre-flight. Installed reviewers here: gemini, codex, qwen, opencode, cursor-agent, agy, ccp
  profiles. `--claude` routed through `ccp pro` (F2: bare `claude` is a shell-function wrapper).
- **Naming default:** `/xreview`, `/xconverge` (rename trivially if desired).

## 11. Build status (2026-06-20)

**`/xreview` built and validated.** Files under `~/.claude-max/skills/xreview/`:
`SKILL.md` (thin wrapper), `dispatch.sh` (the hardened engine), `.sync-baseline.json` (drift
baseline). Non-`gsd-` name → update-proof. Skill is discoverable/invocable. `--check-sync` and
`--doctor` validated; `bash -n` clean.

`--doctor --all` results — each reviewer bounded to 25 s; **no orphan processes left afterward
(watchdog reaps cleanly)**:
- **PASS:** qwen, opencode, agy, claude (via `ccp pro`).
- **TIMEOUT** (slow init, *bounded not hung* — fine under the 240 s real-review budget): codex,
  cursor. Use `--doctor-timeout 60` to confirm them.
- **FAIL:** gemini — **environment, not dispatch**: Google retired free-tier Gemini Code Assist
  for the CLI (`IneligibleTierError … migrate to Antigravity`). Drop `--gemini` or migrate auth.
  (Separately: ~25 `~/.gemini/agents/gsd-*.md` fail to load — "Invalid tool name" — a distinct
  GSD↔gemini breakage.)

Contract proven: codex/cursor, which would previously hang the sequential batch, were killed at
their timeout and the run continued; failures captured to `.err` and surfaced; nothing orphaned.

**Remaining work:**
1. `/xconverge` — fork of `gsd-plan-review-convergence` whose loop calls `xreview` instead of the
   broken `gsd-review`; reuses the official loop + CYCLE_SUMMARY contract.
2. Global `.claude-max-max` sweep (installer-baked; reverts on each `gsd update`) **+ a
   post-update repair hook** for durability.
