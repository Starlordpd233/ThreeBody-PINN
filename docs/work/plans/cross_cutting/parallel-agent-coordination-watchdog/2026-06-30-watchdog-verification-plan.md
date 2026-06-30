---
status: active
purpose: implementation-plan
created: 2026-06-30
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when gates G0-G4 all PASS with committed evidence and the dogfood
  capstone has run (the watchdog is verified for global within-project
  deployment), OR when superseded by a revised verification plan. Re-open on any
  change to the wd-* tools, lib/wd-common.sh, SKILL.md, install-global.sh, or the
  Claude Code harness behaviors named in the strategy doc (background Bash
  re-entry, CronCreate/CronList, skill discovery).
---

# Cross-Session Watchdog — Verification Implementation Plan

> **For agentic workers (Agent B):** REQUIRED SUB-SKILL: use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the automated tests and live-rehearsal protocols that take the
cross-session watchdog from "logic + one live path proven" to "verified for
global within-project deployment," gated by G0-G4 + a dogfood capstone.

**Architecture:** This plan **verifies; it does not modify** the watchdog. Every
task creates *new* artifacts only — tests under `tests/watchdog/`, evidence files
under `tools/watchdog/evidence/`, and one running checklist. Automated tiers
(T0-T2) are characterization/contract tests of already-shipped tools: write the
test, run it, expect **PASS** (green = that cell verified). A **RED** result is a
**finding** about the tool, surfaced to the tool-owner — never a cue to edit
`wd-*`, `wd-common.sh`, `SKILL.md`, or `install-global.sh` (those belong to the
global-packaging track). Live tiers (T3, parts of T4, capstone) are operator
protocols whose deliverable is a committed evidence file.

**Tech Stack:** Bash tools (`tools/watchdog/wd-*` + `lib/wd-common.sh`); Python
`unittest` tests (stdlib only, run under `pytest`); git worktrees; `tmux` (real,
for one live tier; stubbed in unit tests); Claude Code harness (background `Bash`
re-entry, `CronCreate`/`CronList`) for live tiers.

**Source of truth & spec:** the approved strategy doc
`docs/work/designs/cross_cutting/parallel-agent-coordination-watchdog/2026-06-30-watchdog-verification-strategy.md`.
Read it first — this plan operationalizes its §4 tiers and §5 gates.

---

## Status update vs. the approved design (read before starting)

Three facts changed between the strategy doc and this plan; none alters the gate
semantics, all are grounded in files read on 2026-06-30:

1. **The global packaging has landed.** `tools/watchdog/install-global.sh` now
   deploys a **real** canonical skill at `~/.claude/skills/cross-session-watchdog/`
   (with `bin/` holding the 8 `wd-*` + `lib/wd-common.sh`) and **absolute symlinks**
   into the `alt`/`free`/`max` profiles. It **regenerates** the deployed `SKILL.md`,
   rewriting the repo-relative prefix `tools/watchdog/` → `$HOME/.claude/skills/cross-session-watchdog/bin/`.
2. **The strategy's headline risk is therefore mitigated, not open.** Design §9's
   "`SKILL.md` hard-codes `tools/watchdog/…` relative paths" is now handled by the
   install-time path-rewrite. It converts into three cheap, automatable **packaging
   contract checks** (drift, rewrite correctness, symlink integrity) folded into
   **T0/G0** — they are static contract checks, so no gate is redefined.
3. **`SKILL.md` exists in two forms:** the repo **source**
   (`.claude/skills/cross-session-watchdog/SKILL.md`, repo-relative paths, the
   `install-global.sh` input) and the **deployed** canonical copy (`$HOME/.claude/…`,
   absolute paths). The wake-prompt and vocab contracts span both.

Current observed drift status (read 2026-06-30): repo `wd-arm` ≡ `~/.claude` bin
≡ `~/.claude-free` bin = **IDENTICAL**. So G0's drift check should currently pass.

---

## Global Constraints

Every task's requirements implicitly include this section.

- **Verify-not-modify.** Create only `tests/watchdog/*`, `tools/watchdog/evidence/*`,
  and `tools/watchdog/VERIFICATION-CHECKLIST.md`. **Never** edit `wd-*`,
  `lib/wd-common.sh`, `SKILL.md`, or `install-global.sh`. A RED test or a failed
  live run is a **finding**: STOP that cell, record it in the checklist's Findings
  section with severity, and surface it. Do not "fix" the tool inside this plan.
- **Test conventions** (match the existing 5 files exactly): stdlib `unittest`;
  module constants `ROOT = pathlib.Path(__file__).resolve().parents[2]`,
  `WD = ROOT/"tools"/"watchdog"`; strip `ISOLATED_KEYS` from the child env; isolate
  every test in a throwaway `git init` repo so the real repo's
  `.git/live-monitor/channels/` is never touched; self-contained per file (no
  `conftest.py`). Use the **Shared Test Preamble** (below) verbatim at the top of
  each new test file.
- **Git governance.** Commit with `scripts/agent-commit` (never raw `git commit`);
  it requires `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` and auto-appends the
  `Agent-Assisted-By:` trailer. Stage explicit owned paths only (never `git add -A`).
  Conventional messages: `test(governance): …` for tests, `evidence(governance): …`
  for live evidence, `verify(governance): …` for the final roll-up; include a body.
  Do **not** push (master is a local integration branch).
- **Fixed wake prompt is a byte constant.** Never interpolate channel-file bytes
  into a prompt anywhere.
- **Scope:** single machine; within-project (same repo, any branch/worktree).
  Cross-project handoff is **deferred** (design §8) and out of this plan.
- **Runner:** `python3 -m pytest tests/watchdog/ -v` (fallback:
  `python3 -m unittest discover -s tests/watchdog -v`). A potentially-hanging tool
  (`wd-arm` loops) is always invoked with `--timeout-secs` and/or a subprocess
  timeout in tests.
- **Executor tags:** `[AGENT]` = Agent B runs it unattended. `[HUMAN-IN-LOOP]` =
  Agent B scripts and drives it, but a human supplies the second live session /
  foreground tab / tmux pane and confirms the observed re-entry.

---

## Shared Test Preamble (use verbatim atop each new test file)

```python
import os
import pathlib
import re
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
COMMON = WD / "lib" / "wd-common.sh"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
ARM = WD / "wd-arm"
PUSH = WD / "wd-push"
DISARM = WD / "wd-disarm"
STATUS = WD / "wd-status"
INTEGRATE = WD / "wd-integrate"
GSD_PUBLISH = WD / "wd-gsd-publish"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)


def _clean_env(extra=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if extra:
        merged.update(extra)
    return merged


def run(args, cwd, env=None, timeout=60):
    return subprocess.run(
        [str(a) for a in args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        env=_clean_env(env),
        check=False,
        timeout=timeout,
    )


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
    )


def init_repo(path):
    # .resolve() collapses the macOS /var -> /private/var symlink so cwd-based
    # paths and git's realpath toplevel agree.
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    (path / "README.md").write_text("hello\n")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "-m", "init")
    return path


def first_token(proc):
    return proc.stdout.split()[0] if proc.stdout.strip() else ""
```

---

## Evidence-file template (use for every `[HUMAN-IN-LOOP]` deliverable)

Write to `tools/watchdog/evidence/<YYYY-MM-DD>-<slug>.md`. `<YYYY-MM-DD>` is the
real run date.

```markdown
# <Title> — Live Verification Evidence

- **Cell:** <T3.1 | T3.2 | …>   **Gate:** <G3 | G4 | capstone>
- **Date / operator:** <YYYY-MM-DD> / <who ran it>
- **Result:** PASS | FAIL
- **Wake latency:** <seconds from publish to B re-entry>
- **Observed re-entry mode:** <background-Bash-exit | cron-fire | tmux-injection>
- **Environment:** <macOS ver, Claude Code ver, tmux ver if used, profile, repo>

## Steps run (verbatim commands)
…

## Observed output (verbatim, including the wd-* result line B saw)
…

## Verdict & notes
PASS/FAIL justification; any deviation; any finding (with severity) and the
checklist row updated.
```

---

# Phase A — T0 static & packaging contracts → Gate **G0**  `[AGENT]`

Catches doc-vs-tool drift and global-packaging breakage — the most likely silent
failure as the skill is repackaged. Two new files.

### Task A0: Create the verification checklist scaffold

**Files:**
- Create: `tools/watchdog/VERIFICATION-CHECKLIST.md`

- [ ] **Step 1: Write the checklist**

```markdown
# Watchdog Verification Checklist

Tracks per-cell status for the 2026-06-30 verification plan. Update the row as
each task closes. Legend: ⬜ not started · 🟩 PASS · 🟥 FAIL(finding) · ⏭️ covered-elsewhere

## G0 — static & packaging contracts
- ⬜ A1 shellcheck clean
- ⬜ A2 wake-prompt consistency
- ⬜ A3 verdict/exit-code vocab in SKILL.md
- ⬜ A4 watch-loops restore set +e
- ⬜ A5 install drift (repo ↔ canonical bin)
- ⬜ A6 deployed SKILL.md path-rewrite
- ⬜ A7 alt-profile symlink integrity

## G1 — unit logic gaps
- ⬜ B1 concurrent claim race (exactly-once)
- ⬜ B2 non-git CWD fails safely  (also satisfies T4.4)
- ⬜ B3 resolver uses CWD not tool-home  (automatable core of T4.2)
- ⬜ B4 claim-dir accumulation + re-wake
- ⬜ B5 disarm tolerates dead pid

## G2 — multi-process integration
- ⬜ C1 N-consumer real-process race
- ⬜ C2 mixed arm+push race (tmux stub)
- ⬜ C3 disarm sentinel stands down running watcher (timing)
- ⬜ C4 SIGTERM-during-sleep → DISARMED (TERM trap)
- ⬜ C5 cross-worktree real linked worktrees (clean/already/conflict-abort)
- ⬜ C6 cross-repo channel isolation  (satisfies T4.3)

## G3 — live single-machine
- ⬜ D1 cross-worktree two-session handoff
- ⬜ D2 real PUSH (real tmux + idle claude pane)
- ⬜ D3 P2 cron under termination contract

## G4 — live global
- ⬜ E1 discovery/load in each profile
- ⬜ E2 foreign-project live within-project handoff
- ⬜ E3 fresh-agent instruction-following rehearsal
- (T4.3 → C6 · T4.4 → B2)

## Capstone
- ⬜ F1 dogfooded A→B run (B runs the watchdog suite)

## Findings (RED cells / live FAILs — surface, do not patch)
| id | cell | severity | summary | status |
|----|------|----------|---------|--------|
```

- [ ] **Step 2: Commit**

```bash
git add tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "test(governance): add watchdog verification checklist scaffold" \
    -m "Tracks per-cell PASS/FAIL for the 2026-06-30 verification plan."
```

---

### Task A1-A4: Tool↔doc contract tests

**Files:**
- Create: `tests/watchdog/test_contract.py`

**Interfaces:**
- Consumes: the Shared Test Preamble constants (`WD`, `ARM`, `PUSH`, `ROOT`).
- Produces: nothing for later tasks (leaf test file).

- [ ] **Step 1: Write the test file** (preamble, then these tests)

```python
# The fixed wake prompt — byte-exact single-line form (as in wd-push line ~94).
WAKE = (
    "Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result "
    "line; if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, "
    "stop and report."
)
REPO_SKILL = ROOT / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"
HOME_SKILL = pathlib.Path.home() / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"

# Verdict tokens the tools emit and the skill doc must name (grep-confirmed in
# wd-arm / wd-push / wd-check on 2026-06-30).
VERDICTS = ("WAKE", "ALREADY-CLAIMED", "PRODUCER-STALLED", "DISARMED", "PUSHED")


def _norm(s):
    # Collapse blockquote ('>') and comment ('#') markers + whitespace runs so a
    # line-wrapped SKILL.md blockquote / wd-arm comment compares equal to the
    # single-line shell constant. Semantic identity, not literal byte identity.
    return re.sub(r"\s+", " ", re.sub(r"[>#]", " ", s)).strip()


class ContractTests(unittest.TestCase):
    def test_a1_shellcheck_clean(self):
        sc = shutil.which("shellcheck")
        if sc is None:
            self.skipTest("shellcheck not installed")
        targets = [str(COMMON)] + [str(p) for p in sorted(WD.glob("wd-*"))]
        proc = subprocess.run([sc, "-S", "error", *targets],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0,
                         "shellcheck errors:\n" + proc.stdout + proc.stderr)

    def test_a2_wake_prompt_consistent(self):
        canon = _norm(WAKE)
        candidates = [PUSH, ARM, REPO_SKILL]
        if HOME_SKILL.exists():
            candidates.append(HOME_SKILL)
        carriers = [c for c in candidates if c.exists() and canon in _norm(c.read_text())]
        names = [c.name for c in carriers]
        # The injector (wd-push) and at least one SKILL.md must carry the prompt.
        self.assertIn("wd-push", names, f"wd-push lost the wake prompt; carriers={names}")
        self.assertTrue(any(c.name == "SKILL.md" for c in carriers),
                        f"no SKILL.md carries the wake prompt; carriers={names}")
        # wd-push carries the byte-exact single-line form.
        self.assertIn(WAKE, PUSH.read_text(), "wd-push prompt is not byte-exact")

    def test_a3_verdict_vocab(self):
        self.assertTrue(REPO_SKILL.exists(), f"missing {REPO_SKILL}")
        skill = REPO_SKILL.read_text()
        tools_text = "\n".join(p.read_text() for p in WD.glob("wd-*"))
        for token in VERDICTS:
            self.assertIn(token, skill, f"SKILL.md does not document verdict {token}")
            self.assertIn(token, tools_text, f"no tool emits verdict {token}")

    def test_a4_watch_loops_restore_set_plus_e(self):
        # wd-arm and wd-push run a long poll loop after sourcing wd-common.sh
        # (which sets -e); both must restore `set +e` so an expected non-zero
        # from wd-check does not kill the loop.
        for tool in (ARM, PUSH):
            text = tool.read_text()
            self.assertRegex(text, r"\n\s*set \+e\b",
                             f"{tool.name} does not restore 'set +e' after sourcing")
```

- [ ] **Step 2: Run**

Run: `python3 -m pytest tests/watchdog/test_contract.py -v`
Expected: **4 PASS** (`shellcheck` test may SKIP if not installed — that is
acceptable for G0; note it in the checklist).

- [ ] **Step 3: On RED, STOP and record a finding** (do not edit the tool/doc).
Add a row to the checklist Findings table with severity, then surface it. The
likely real finding is A4 if a tool used `wd-check || true` instead of `set +e`,
or A2/A3 if `SKILL.md` drifted from the tools.

- [ ] **Step 4: Update checklist rows A1-A4, commit**

```bash
git add tests/watchdog/test_contract.py tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tests/watchdog/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "test(governance): add watchdog T0 tool-doc contract checks" \
    -m "shellcheck, wake-prompt consistency, verdict vocab, set+e restoration."
```

---

### Task A5-A7: Global-packaging contract tests

**Files:**
- Create: `tests/watchdog/test_global_packaging.py`

These read the **real** `~/.claude` install read-only and `skipTest` when it is
absent, so the suite still runs on a machine without the global install.

- [ ] **Step 1: Write the test file** (preamble, then these tests)

```python
HOME = pathlib.Path.home()
CANON = HOME / ".claude" / "skills" / "cross-session-watchdog"
CANON_BIN = CANON / "bin"
REPO_SKILL = ROOT / ".claude" / "skills" / "cross-session-watchdog" / "SKILL.md"


class GlobalPackagingTests(unittest.TestCase):
    def setUp(self):
        if not CANON_BIN.exists():
            self.skipTest("global install absent; run tools/watchdog/install-global.sh")

    def test_a5_canonical_bin_matches_repo_source(self):
        for src in sorted(WD.glob("wd-*")):
            dst = CANON_BIN / src.name
            self.assertTrue(dst.exists(), f"canonical missing {dst}")
            self.assertEqual(src.read_bytes(), dst.read_bytes(),
                             f"DRIFT: {src.name} differs between repo and canonical bin")
        self.assertEqual((WD / "lib" / "wd-common.sh").read_bytes(),
                         (CANON_BIN / "lib" / "wd-common.sh").read_bytes(),
                         "DRIFT: wd-common.sh differs between repo and canonical")

    def test_a6_deployed_skill_paths_rewritten(self):
        skill = CANON / "SKILL.md"
        self.assertTrue(skill.exists(), f"missing deployed {skill}")
        text = skill.read_text()
        self.assertNotIn("tools/watchdog/", text,
                         "deployed SKILL.md still has repo-relative tools/watchdog/ paths")
        refs = set(re.findall(
            r"\$HOME/\.claude/skills/cross-session-watchdog/bin/(wd-[a-z-]+)", text))
        self.assertTrue(refs, "deployed SKILL.md references no bin/ tools (rewrite failed?)")
        for name in sorted(refs):
            p = CANON_BIN / name
            self.assertTrue(p.exists() and os.access(p, os.X_OK),
                            f"deployed SKILL.md references non-executable {p}")

    def test_a7_alt_profiles_symlink_to_canonical(self):
        checked = 0
        for profile in ("alt", "free", "max"):
            link = HOME / f".claude-{profile}" / "skills" / "cross-session-watchdog"
            if not link.exists():
                continue
            checked += 1
            self.assertTrue(link.is_symlink(), f"{link} is not a symlink")
            self.assertEqual(os.path.realpath(link), os.path.realpath(CANON),
                             f"{link} does not resolve to canonical {CANON}")
        if checked == 0:
            self.skipTest("no alt profiles present")
```

- [ ] **Step 2: Run**

Run: `python3 -m pytest tests/watchdog/test_global_packaging.py -v`
Expected: **3 PASS** (or SKIP if the global install is absent on this machine).

- [ ] **Step 3: On RED, STOP and record a finding.** A5 RED = the repo source
changed without re-running `install-global.sh` (drift) → finding for the
packaging-track owner: "re-run `tools/watchdog/install-global.sh`." A6 RED = the
path-rewrite is broken. A7 RED = a profile holds a real dir or a stale symlink.

- [ ] **Step 4: Update checklist rows A5-A7, commit**

```bash
git add tests/watchdog/test_global_packaging.py tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tests/watchdog/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "test(governance): add watchdog global-packaging contract checks" \
    -m "Asserts repo-canonical drift, SKILL.md path-rewrite, and alt-profile symlinks."
```

**Gate G0 closes when:** A1-A7 are 🟩 (or justified SKIP) with no open finding.

---

# Phase B — T1 unit logic gaps → Gate **G1**  `[AGENT]`

Keep the 28 existing tests; add the five cells they miss. One new file.

### Task B1-B5: Unit gap tests

**Files:**
- Create: `tests/watchdog/test_watchdog_unit_gaps.py`

**Interfaces:**
- Consumes: Shared Test Preamble (`ARM`, `PUBLISH`, `CHECK`, `DISARM`, `init_repo`,
  `run`, `git`, `first_token`).

- [ ] **Step 1: Write the test file** (preamble, then these tests)

```python
class UnitGapTests(unittest.TestCase):

    # T1-a — concurrent claim race at unit fidelity. The exactly-once claim is a
    # single atomic `mkdir claimed.<head>` shared by every wake path (identical
    # line in wd-arm and wd-push), so N racing wd-arm processes prove the primitive.
    def test_b1_concurrent_claim_exactly_once(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            self.assertEqual(
                run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"],
                    cwd=repo).returncode, 0)
            N = 4

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "15"],
                           cwd=repo, timeout=30)

            with concurrent.futures.ThreadPoolExecutor(max_workers=N) as ex:
                results = [f.result() for f in [ex.submit(arm_once) for _ in range(N)]]
            verdicts = [first_token(r) for r in results]
            self.assertEqual(verdicts.count("WAKE"), 1, f"not exactly one WAKE: {verdicts}")
            self.assertEqual(verdicts.count("ALREADY-CLAIMED"), N - 1, f"{verdicts}")
            claims = list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))
            self.assertEqual(len(claims), 1, f"expected one claim dir: {claims}")

    # T1-b — non-git CWD must fail safely (defined non-zero exit + a diagnostic),
    # not hang or dump a confusing trace. wd-check is one-shot (cannot hang).
    def test_b2_non_git_cwd_fails_safely(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run([CHECK, "--channel", "x"], cwd=d, timeout=20)
            self.assertNotEqual(proc.returncode, 0,
                                "wd-check unexpectedly succeeded outside a git repo")
            self.assertTrue((proc.stderr or proc.stdout).strip(),
                            "no diagnostic emitted outside a git repo")
            # FINDING gate (design T1-b / T4.4): a watchdog-identifiable message is
            # preferred over git's bare 'fatal: not a git repository'. If only the
            # bare git message appears, record a LOW-severity UX finding. PASS here
            # requires only: non-zero exit + some diagnostic + no hang.

    # T1-c — the resolver keys the channel to the CWD's repo, even when the tool is
    # invoked by absolute path from a different repo (the global-install case).
    def test_b3_resolver_uses_cwd_not_tool_home(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            pub = run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            self.assertEqual(pub.returncode, 0, pub.stderr)
            chan = repo / ".git" / "live-monitor" / "channels" / "c"
            self.assertTrue((chan / "done.json").exists(),
                            "done.json not under CWD repo's .git; resolver used tool home")
            chk = run([CHECK, "--channel", "c"], cwd=repo)
            self.assertEqual(first_token(chk), "WAKE",
                             f"rc={chk.returncode} out={chk.stdout!r} err={chk.stderr!r}")

    # T1-d — claim dirs accumulate one-per-distinct-head; a NEW head still wakes
    # despite prior claims (claims never block a future head). Documents the
    # housekeeping contract grounded in the per-head claim mechanism.
    def test_b4_claim_dirs_accumulate_and_rewake(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            seen = []
            for i in range(3):
                (repo / f"f{i}.txt").write_text("x\n")
                git(repo, "add", f"f{i}.txt")
                git(repo, "commit", "-q", "-m", f"c{i}")
                head = git(repo, "rev-parse", "HEAD").stdout.strip()
                run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", f"f{i}.txt"], cwd=repo)
                arm = run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "10"],
                          cwd=repo, timeout=20)
                self.assertEqual(first_token(arm), "WAKE",
                                 f"head {i}: out={arm.stdout!r} err={arm.stderr!r}")
                seen.append(head)
            dirs = sorted(p.name for p in chan.glob("claimed.*"))
            self.assertEqual(dirs, sorted(f"claimed.{h}" for h in seen),
                             "expected exactly one claimed.<head> per distinct head")

    # T1-e — disarm tolerates a dead pid (best-effort kill of a gone process) with
    # exit 0 and removes the record. The reused-pid hazard (kill could signal an
    # unrelated reborn pid) is a documented LOW nit, not exercised destructively.
    def test_b5_disarm_tolerates_dead_pid(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            chan.mkdir(parents=True)
            dead = 2**31 - 1  # out-of-range pid; kill -0 fails cleanly
            (chan / "armed.json").write_text(
                '{"kind":"watcher","channel":"c","armed_at":0,"ttl":null,'
                f'"armed_by":"x","pid":{dead}}}\n')
            dis = run([DISARM, "--channel", "c"], cwd=repo)
            self.assertEqual(dis.returncode, 0, dis.stderr)
            self.assertFalse((chan / "armed.json").exists(), "armed.json not removed")
```

- [ ] **Step 2: Run**

Run: `python3 -m pytest tests/watchdog/test_watchdog_unit_gaps.py -v`
Expected: **5 PASS**.

- [ ] **Step 3: Confirm the 28 existing tests still pass**

Run: `python3 -m pytest tests/watchdog/ -v`
Expected: **33 PASS** (28 + 5), plus the G0 file results.

- [ ] **Step 4: On RED, STOP and record a finding.** Most plausible: B2 (only the
bare git message → LOW UX finding) or B4 (if accumulation differs from the
documented contract → re-state the contract with the owner).

- [ ] **Step 5: Update checklist rows B1-B5, commit**

```bash
git add tests/watchdog/test_watchdog_unit_gaps.py tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tests/watchdog/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "test(governance): add watchdog T1 unit-gap tests" \
    -m "Concurrent claim, non-git guard, CWD resolver, claim housekeeping, dead-pid disarm."
```

**Gate G1 closes when:** 28 existing + B1-B5 green; no open finding.

---

# Phase C — T2 multi-process integration → Gate **G2**  `[AGENT]`

Real OS processes, real timing — still no Claude harness, so it runs in CI. One
new file.

### Task C1-C6: Multi-process tests

**Files:**
- Create: `tests/watchdog/test_watchdog_multiprocess.py`

- [ ] **Step 1: Write the test file** (preamble; include the `tmux` stub block below)

```python
# tmux stub (identical contract to tests/watchdog/test_push.py): logs each call
# to $TMUX_LOG, exits 0, honors TMUX_STUB_NO_PANE / TMUX_STUB_SEND_KEYS_FAIL.
TMUX_STUB = """#!/bin/sh
log="${TMUX_LOG:-/dev/null}"
printf '%s\\n' "$*" >> "$log"
cmd="${1:-}"
case "$cmd" in
  has-session|list-panes)
    [ -n "${TMUX_STUB_NO_PANE:-}" ] && exit 1
    exit 0
    ;;
  send-keys)
    [ -n "${TMUX_STUB_SEND_KEYS_FAIL:-}" ] && exit 1
    exit 0
    ;;
  *) exit 0 ;;
esac
"""


def _stub_tmux_on_path(d):
    bindir = pathlib.Path(d) / "stubbin"
    bindir.mkdir()
    tmux = bindir / "tmux"
    tmux.write_text(TMUX_STUB)
    tmux.chmod(0o755)
    return f"{bindir}:{os.environ['PATH']}"


def _popen_arm(repo, channel, poll, timeout):
    return subprocess.Popen(
        [str(ARM), "--channel", channel, "--poll-secs", str(poll),
         "--timeout-secs", str(timeout)],
        cwd=str(repo), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_clean_env(),
    )


class MultiProcessTests(unittest.TestCase):

    # C1 — N real consumer processes race one publish; exactly one wins.
    def test_c1_n_consumers_exactly_one(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            N = 6

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, timeout=40)

            with concurrent.futures.ThreadPoolExecutor(max_workers=N) as ex:
                res = [f.result() for f in [ex.submit(arm_once) for _ in range(N)]]
            v = [first_token(r) for r in res]
            self.assertEqual(v.count("WAKE"), 1, f"not exactly one WAKE: {v}")
            self.assertEqual(len(list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))), 1)

    # C2 — mixed wake paths (2 wd-arm + 1 wd-push) race one head; exactly one of
    # {WAKE, PUSHED}, the rest ALREADY-CLAIMED, exactly one claim dir.
    def test_c2_mixed_arm_push_exactly_one(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            stub_path = _stub_tmux_on_path(d)
            log = pathlib.Path(d) / "tmux.log"

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, timeout=40)

            def push_once():
                return run([PUSH, "--channel", "c", "--pane", "fake:0.0",
                            "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, env={"PATH": stub_path, "TMUX_LOG": str(log)}, timeout=40)

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
                fs = [ex.submit(arm_once), ex.submit(arm_once), ex.submit(push_once)]
                res = [f.result() for f in fs]
            v = [first_token(r) for r in res]
            winners = v.count("WAKE") + v.count("PUSHED")
            self.assertEqual(winners, 1, f"not exactly one winner: {v}")
            self.assertEqual(v.count("ALREADY-CLAIMED"), 2, f"{v}")
            self.assertEqual(len(list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))), 1)

    # C3 — disarm sentinel dropped mid-poll stands down a RUNNING watcher within a
    # couple of poll intervals (process-fidelity timing).
    def test_c3_disarm_sentinel_timing(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            proc = _popen_arm(repo, "c", poll=1, timeout=30)
            try:
                time.sleep(2)  # let it arm + enter the poll loop
                self.assertTrue((chan / "armed.json").exists(), "watcher did not arm")
                (chan / "disarm").write_text("")
                out, err = proc.communicate(timeout=10)
            finally:
                if proc.poll() is None:
                    proc.kill()
            self.assertEqual(proc.returncode, 0, err)
            self.assertEqual(out.strip(), "DISARMED", f"out={out!r} err={err!r}")

    # C4 — SIGTERM during the poll sleep stands down via the TERM trap (DISARMED,
    # exit 0), not a silent kill.
    def test_c4_sigterm_during_sleep_disarms(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            proc = _popen_arm(repo, "c", poll=5, timeout=30)
            try:
                time.sleep(2)  # now inside `sleep 5`
                proc.send_signal(signal.SIGTERM)
                out, err = proc.communicate(timeout=10)
            finally:
                if proc.poll() is None:
                    proc.kill()
            self.assertEqual(out.strip(), "DISARMED", f"out={out!r} err={err!r}")
            self.assertEqual(proc.returncode, 0)

    # C5 — cross-worktree with REAL linked worktrees: not-integrated -> STALE,
    # integrate -> WAKE; and conflict -> abort with a clean tree.
    # NOTE: if tests/watchdog/test_watchdog_xworktree.py already uses real
    # `git worktree add` for all four sub-cases, mark C5 ⏭️ covered-elsewhere and
    # skip this body (verify by reading that file first).
    def test_c5_cross_worktree_real(self):
        with tempfile.TemporaryDirectory() as d:
            main = init_repo(pathlib.Path(d) / "main")
            wt = pathlib.Path(d) / "wt"
            git(main, "branch", "consumer")
            self.assertEqual(git(main, "worktree", "add", "-q", str(wt), "consumer").returncode, 0)
            (main / "a.txt").write_text("A\n")
            git(main, "add", "a.txt")
            git(main, "commit", "-q", "-m", "A work")
            run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "a.txt"], cwd=main)
            pre = run([CHECK, "--channel", "c", "--require-integration"], cwd=wt)
            self.assertTrue(pre.stdout.strip().startswith("STALE"),
                            f"expected STALE before integrate: {pre.stdout!r}")
            integ = run([INTEGRATE, "--channel", "c"], cwd=wt)
            self.assertEqual(integ.returncode, 0, integ.stderr)
            post = run([CHECK, "--channel", "c", "--require-integration"], cwd=wt)
            self.assertEqual(first_token(post), "WAKE",
                             f"out={post.stdout!r} err={post.stderr!r}")
            self.assertEqual(git(wt, "status", "--porcelain").stdout.strip(), "",
                             "worktree left dirty after integrate")

    # C6 — channel isolation across two repos: a publish in repo-Y is invisible in
    # repo-Z (no cross-talk). Satisfies design T4.3 automatically.
    def test_c6_cross_repo_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            y = init_repo(pathlib.Path(d) / "Y")
            z = init_repo(pathlib.Path(d) / "Z")
            run([PUBLISH, "--channel", "shared", "--stage", "s", "--scope", "README.md"], cwd=y)
            in_y = run([CHECK, "--channel", "shared"], cwd=y)
            in_z = run([CHECK, "--channel", "shared"], cwd=z)
            self.assertEqual(first_token(in_y), "WAKE", f"Y should WAKE: {in_y.stdout!r}")
            self.assertNotEqual(first_token(in_z), "WAKE",
                                f"Z must NOT see Y's publish (cross-talk): {in_z.stdout!r}")
```

- [ ] **Step 2: Run**

Run: `python3 -m pytest tests/watchdog/test_watchdog_multiprocess.py -v`
Expected: **6 PASS** (C5 may be ⏭️ if covered by the existing xworktree file —
see the note in C5; confirm by reading `test_watchdog_xworktree.py` first).

- [ ] **Step 3: Full-suite regression**

Run: `python3 -m pytest tests/watchdog/ -v`
Expected: **39 PASS** (28 + 5 + 6), G0 packaging tests possibly SKIP.

- [ ] **Step 4: On RED, STOP and record a finding** (timing flakes: re-run once;
if persistently RED it is a real race/termination defect → finding).

- [ ] **Step 5: Update checklist rows C1-C6, commit**

```bash
git add tests/watchdog/test_watchdog_multiprocess.py tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tests/watchdog/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "test(governance): add watchdog T2 multi-process integration tests" \
    -m "Real-process race, mixed arm+push, disarm timing, SIGTERM trap, real worktree, isolation."
```

**Gate G2 closes when:** C1-C6 green (C5 may be ⏭️); no open finding.
**This is the end of the no-coordination automated work** — G0-G2 can be done
now, before any live session.

---

# Phase D — T3 live single-machine → Gate **G3**  `[HUMAN-IN-LOOP]`

Cells only the real Claude Code harness can exercise. Each deliverable is a
committed evidence file (use the template above). Agent B scripts and drives;
a human supplies the second session and confirms the observed re-entry.

### Task D1: Cross-worktree two-session live handoff (T3.1)

**Files:**
- Create: `tools/watchdog/evidence/<date>-xworktree-live-handoff.md`

- [ ] **Step 1: Set up two sessions.** Session A in the main worktree on `master`;
  Session B in a linked worktree on its own branch:
  `git worktree add -q .worktrees/wd-consumer -b wd-consumer master`.
- [ ] **Step 2: B arms (background) and ends its turn:**
  `tools/watchdog/wd-arm --channel xw-live --poll-secs 20 --timeout-secs 1800 --task-file <task.md>`
  (run via the Bash tool in the background). `<task.md>` instructs B to run
  `wd-integrate --channel xw-live` then `wd-check --channel xw-live --require-integration`
  then report the integrated head.
- [ ] **Step 3: A commits a trivial change in the main worktree, then publishes:**
  `tools/watchdog/wd-publish-done --channel xw-live --stage demo --scope "<path>"`.
- [ ] **Step 4: Observe** B re-enter unattended, integrate A's head, `wd-check`
  return `WAKE`, and begin the task. Record latency + re-entry mode.
- [ ] **Step 5: Disarm/cleanup:** `tools/watchdog/wd-disarm --channel xw-live`;
  remove the temp worktree if desired (`git worktree remove .worktrees/wd-consumer`).

**PASS:** B woke with no keystroke, `wd-integrate` succeeded, `wd-check
--require-integration` returned `WAKE`, B's branch then contained A's commit.

- [ ] **Step 6: Write evidence + commit**

```bash
git add tools/watchdog/evidence/<date>-xworktree-live-handoff.md tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tools/watchdog/evidence/:tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "evidence(governance): record cross-worktree live watchdog handoff" \
    -m "T3.1 / G3: B armed in a linked worktree woke, integrated A's head, and began its task."
```

### Task D2: Real PUSH — real tmux + idle claude pane (T3.2)

**Files:**
- Create: `tools/watchdog/evidence/<date>-real-push.md`

- [ ] **Step 1:** In real `tmux`, open a pane running an **idle** `claude` session
  as B (note the pane target, e.g. `wd:0.1`). Honor the soft precondition: the
  pane must sit at a clean idle prompt (`wd-push` injects blindly).
- [ ] **Step 2:** From the operator terminal (NOT B's pane), run:
  `tools/watchdog/wd-push --channel push-live --pane wd:0.1 --poll-secs 10 --timeout-secs 900`.
- [ ] **Step 3:** From A's session, commit + `wd-publish-done --channel push-live
  --stage demo --scope "<path>"`.
- [ ] **Step 4:** Observe the two-call `send-keys` shim inject the fixed wake
  prompt and B begin. Confirm `wd-push` printed `PUSHED <head>` exactly once.

**PASS:** B woke via injection exactly once; `claimed.<head>` present;
re-running `wd-push` prints `ALREADY-CLAIMED`. **Document** the unverifiable soft
precondition as an operator responsibility.

- [ ] **Step 5: Write evidence + commit** (`evidence(governance): record real-tmux PUSH wake`).

### Task D3: P2 durable cron under the termination contract (T3.3)

**Files:**
- Create: `tools/watchdog/evidence/<date>-p2-cron-contract.md`

- [ ] **Step 1:** Arm P2 only with explicit **"yes, durable"** + a TTL. Verify the
  job is on disk in **both** `CronList` **and** `.claude/scheduled_tasks.json`
  immediately (refuse to call the arm complete otherwise).
- [ ] **Step 2:** Confirm the wake prompt's FIRST action on fire checks the
  `disarm` sentinel + TTL, and that **disarm-on-success** `CronDelete`s the job and
  removes `armed.json` before doing anything else.
- [ ] **Step 3:** Verify **TTL self-termination** fires (let a short TTL lapse;
  the job deletes itself) and that the **foreground-tab caveat** is surfaced at arm.
- [ ] **Step 4:** Run `wd-disarm --all` and confirm it removes the arm; `wd-status`
  shows nothing live.

**PASS:** job verified on disk; disarm-on-success and TTL-self-terminate both
observed; foreground caveat surfaced; no stranded cron after the run.

- [ ] **Step 5: Write evidence + commit** (`evidence(governance): record P2 cron under termination contract`).

**Gate G3 closes when:** D1-D3 each PASS with committed evidence.

---

# Phase E — T4 live global-scope → Gate **G4**  `[HUMAN-IN-LOOP]`

The layer the user is most worried about. Two of T4's cells are already automated
(**T4.3 → C6**, **T4.4 → B2**); the three live cells below remain.

### Task E1: Discovery / load in each profile (T4.1)

**Files:**
- Create: `tools/watchdog/evidence/<date>-global-discovery.md`

- [ ] **Step 1:** For each profile that exists (`~/.claude`, `~/.claude-alt`,
  `~/.claude-free`, `~/.claude-max`), start a Claude Code session and confirm the
  `cross-session-watchdog` skill is **surfaced and loadable** (its SKILL.md loads;
  the `$HOME/.claude/.../bin/` tool paths resolve to executables).
- [ ] **Step 2:** From an **arbitrary project directory** (not `3_body_problem`),
  confirm the skill still loads and `~/.claude/skills/cross-session-watchdog/bin/wd-status`
  runs (exit 0). This is the static counterpart to A7, proven live.

**PASS:** skill loads in every present profile and from a foreign CWD; tools run.

- [ ] **Step 3: Write evidence + commit** (`evidence(governance): record global skill discovery across profiles`).

### Task E2: Foreign-project live within-project handoff (T4.2, load-bearing)

**Files:**
- Create: `tools/watchdog/evidence/<date>-foreign-project-resolution.md`

- [ ] **Step 1:** Pick a real project **Y ≠ `3_body_problem`** that is a git repo.
  Two sessions, both in Y. (B3 already proved the resolver keys to CWD; this proves
  it end-to-end under the real global install.)
- [ ] **Step 2:** B (in Y) arms with absolute tool path:
  `~/.claude/skills/cross-session-watchdog/bin/wd-arm --channel fp-live --poll-secs 20 --timeout-secs 900 --task-file <task.md>`.
- [ ] **Step 3:** A (in Y) commits, then
  `~/.claude/skills/cross-session-watchdog/bin/wd-publish-done --channel fp-live --stage demo --scope "<path>"`.
- [ ] **Step 4:** Confirm the channel resolved under **Y's** `.git/live-monitor/…`
  and B woke + ran the task. If this fails, **global deployment is not real** —
  highest-severity finding.

**PASS:** a within-project handoff completes in a project other than
`3_body_problem`, using the installed absolute tool paths.

- [ ] **Step 5: Write evidence + commit** (`evidence(governance): record foreign-project within-project handoff`).

### Task E3: Fresh-agent instruction-following rehearsal (T4.5, highest-value)

**Files:**
- Create: `tools/watchdog/evidence/<date>-agent-rehearsal.md`

- [ ] **Step 1:** Start a **fresh** agent with **only** the global skill text — no
  this-repo context, no this-conversation history. Give it a plain task: "use the
  cross-session-watchdog to hand off from A to B" with a trivial unit of work.
- [ ] **Step 2:** Let it drive the full A→B handoff from the SKILL.md alone.
  Observe whether it picks the right tools, uses the **fixed wake prompt
  verbatim** (no interpolation), arms/integrates/checks in the right order, and
  surfaces the P2 gating if it reaches for durability.
- [ ] **Step 3:** Record every place the agent **misread** the skill (wrong path,
  wrong order, interpolated the prompt, skipped `wd-integrate`). Each is a
  **SKILL.md wording finding** — the skill *as an agent reads it*, which no logic
  test can catch.

**PASS:** the fresh agent completes a correct A→B handoff using only the skill
text; any misread is logged as a finding (severity by impact).

- [ ] **Step 4: Write evidence + commit** (`evidence(governance): record fresh-agent watchdog rehearsal`).

**Gate G4 closes when:** E1-E3 PASS (E2 and E3 mandatory) **and** C6 + B2 are
green (the automated T4.3/T4.4 halves).

---

# Phase F — Capstone & final verdict  `[HUMAN-IN-LOOP]`

### Task F1: Dogfooded A→B acceptance run

**Files:**
- Create: `tools/watchdog/evidence/<date>-dogfood-capstone.md`

Only after G0-G4 are green. One real A→B handoff, wired through the watchdog
itself, where **B's armed task is "run the full watchdog test suite"**
(`python3 -m pytest tests/watchdog/ -v`). This doubles as the acceptance demo.
It is a capstone, **not** a substitute for the deterministic tiers — a watchdog
bug must not be able to hide its own failure, which is why G0-G2 stand alone.

- [ ] **Step 1:** B arms with a task file whose body is "run `python3 -m pytest
  tests/watchdog/ -v` and report the pass count."
- [ ] **Step 2:** A makes a trivial commit and publishes done.
- [ ] **Step 3:** B wakes unattended, runs the suite, reports all-green.
- [ ] **Step 4: Write evidence + commit** (`evidence(governance): record dogfooded watchdog acceptance run`).

### Task F2: Final roll-up

- [ ] **Step 1:** Mark every checklist row 🟩 (or ⏭️ with justification). Ensure the
  Findings table is either empty or every row resolved/accepted by the user.
- [ ] **Step 2:** Add a one-paragraph verdict to the checklist: "Watchdog verified
  for global within-project deployment as of `<date>`; gates G0-G4 + capstone all
  green; open findings: `<none | list>`."
- [ ] **Step 3: Commit**

```bash
git add tools/watchdog/VERIFICATION-CHECKLIST.md
GIT_AGENT_ID="<your-agent-id>" GIT_AGENT_OWNED_PATHS="tools/watchdog/VERIFICATION-CHECKLIST.md" \
  scripts/agent-commit -m "verify(governance): close watchdog global within-project verification" \
    -m "All gates G0-G4 and the dogfood capstone PASS with committed evidence."
```

---

# Deferred — cross-project handoff (design §8 / T5)  `[NOT STARTED]`

Out of scope for this plan. Building it requires a **user decision** that this
plan must not pre-empt: **signal-only** handoff vs **fetch-then-integrate** (design
§8 lays out both, with the machine-global mailbox relocation). Do **not** start
T5 until the user chooses. When they do, it becomes its own brainstorming → plan
cycle, gated separately from G0-G4.

---

## Self-Review (completed by the plan author)

- **Spec coverage:** every design §4 cell maps to a task — T0→A1-A7 (+packaging),
  T1-a..e→B1-B5, T2→C1-C5, T4.3→C6, T4.4→B2, T3.1-3.3→D1-D3, T4.1/4.2/4.5→E1-E3,
  capstone→F1, §8→Deferred. Gates G0-G4 map to phase boundaries unchanged.
- **Placeholder scan:** no "TBD/TODO"; every automated step carries runnable code
  and an exact command + expected output; live steps carry exact `wd-*` commands
  and an evidence template (date is a legitimate runtime value, not a placeholder).
- **Type/name consistency:** shared helpers (`run`, `git`, `init_repo`,
  `first_token`, constants `ARM/PUSH/CHECK/PUBLISH/DISARM/INTEGRATE`) are defined
  once in the preamble and used unchanged in every task; channel/flag names match
  the tools' actual interfaces as read on 2026-06-30.
- **Grounding:** test code matches the existing suite's conventions
  (`test_watchdog_mvp.py`, `test_push.py`); commit flow matches `scripts/agent-commit`;
  packaging contracts match `install-global.sh`; the `set +e`/wake-prompt
  assertions match `wd-arm`/`wd-push` as read. No tool is modified.
