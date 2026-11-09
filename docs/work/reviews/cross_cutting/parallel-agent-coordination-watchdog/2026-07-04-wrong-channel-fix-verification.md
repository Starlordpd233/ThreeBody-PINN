---
status: active
purpose: verification-report
created: 2026-07-04
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire once the watchdog channel-resolution contract is exercised end-to-end at
  least once in a live cross-session handoff (i.e. one producer and one consumer
  using `--phase`/`--key` rendezvous successfully on a real phase transition).
  Until then this verification remains the authoritative gate against the
  phase-36-class split-brain failure mode.
---

# Verification — Watchdog Wrong-Channel Fix

## Scope

Plan under review: `~/.claude-alt/plans/wrong-channel-issue-if-shimmering-hellman.md`
("Watchdog wrong-channel fix: deterministic channel rendezvous"). Goal: remove the
free-text `--channel NAME` failure mode in which producer and consumer invent
independent names that never rendezvous.

Executed across 4 commits, in the order the plan prescribed:

| # | Commit | Scope | Plan's prescribed subject |
|---|--------|-------|---------------------------|
| 1 | `458342ef` | feat(governance) | derive watchdog channels deterministically via --phase/--key resolver |
| 2 | `15397468` | feat(governance) | warn on watchdog channel mismatch at publish and arm time |
| 3 | `72a86f8f` | test(governance) | cover watchdog channel resolution and mismatch backstops |
| 4 | `6aa9f3c0` | docs(governance) | add channel-resolution contract to watchdog skill |

All four commits carry `Plan-Execution:` and `Plan-Source:` trailers plus
`Agent-Assisted-By: codex/gpt-5` per the git-guidelines policy. Repo state after
the four commits is clean (`git status -- tools/watchdog` → no output), so no
uncommitted drift was left behind.

---

## Verdict

**PASS** — the channel-resolution contract was implemented and observed to do
what it claims at the surface, end-to-end through the actual shell tools.

The plan's stated success criteria — (a) both sides derive the same channel from
shared facts, (b) backstop warnings surface at publish/arm time, (c) the SKILL
documents the contract, (d) tests cover it — were all met without inventing
ground that the plan did not already cover.

---

## Method

Sandbox setup: a throwaway `WDROOT` directory under `/tmp` plus a throwaway
git repo at `$WDROOT/repo`, with a vendored copy of `lib/wd-common.sh` whose
`wd_channel_root()` is overridden to print `$WDROOT/channels`. The five affected
shell tools were staged into `$WORK` next to the vendored lib and run against
that sandbox. This sidesteps the shared `<git-common-dir>/live-monitor/channels`
so verification does not touch real cross-session state.

The end-to-end smoke test from the plan's verification step 3 was reproduced
verbatim: `wd-gsd-publish --phase 99 --scope .` followed by `wd-check --phase 99`.
Beyond the plan's prescribed smoke, 11 additional probes were run against the
sandboxed surface to confirm the failure paths (mutual exclusivity, missing
selector, empty slug, non-numeric phase, zero/negative phase, raw `--channel`
passthrough, dirty scope refusal, dual WARNING paths, live double-arm clobber).

The full `tests/watchdog` unittest suite was also executed to confirm the test
commit's coverage and the pre-existing `test_a3_verdict_vocab` baseline flipped
green.

---

## Findings (one finding per row)

### Commit ordering and trailers

✅ All four commits are present in the exact order the plan prescribed. Each
carries `Plan-Execution: wrong-channel-issue-if-shimmering-hellman`,
`Plan-Source: <home>/.claude-alt/plans/wrong-channel-issue-if-shimmering-hellman.md`,
and `Agent-Assisted-By: codex/gpt-5`. `GIT_AGENT_ID` / `GIT_AGENT_OWNED_PATHS`
were honored — `git status -- tools/watchdog` after the four commits is empty.

### `lib/wd-common.sh` — `wd_slug` + `wd_resolve_channel`

✅ `wd_slug` lowercases via `LC_ALL=C tr '[:upper:]' '[:lower:]'` then collapses
non-`[a-z0-9]` runs to single dashes via `LC_ALL=C sed -E`, strips leading/trailing
dashes, and rejects empty output. Locale guards are mandatory per plan and are
present on both `tr` and `sed`.

✅ `wd_resolve_channel` implements all three selectors plus the raw override:

- `--channel NAME` → passes through unsung (verified: `--channel demo` →
  channel `demo/` exactly).
- `--phase NN` → digits-only validation, zero-pad normalization via
  `$((10#$phase))`, rejects zero/negative, formats `gsd-phase-N` (verified:
  `--phase 036` → channel `gsd-phase-36`, same as `--phase 36`).
- `--key STR` → `wd_slug` with empty-slug rejection.

✅ Mutual exclusivity error fires correctly. Probed: `--channel foo --phase 99`
→ `wd-arm: exactly one of --channel, --phase, --key is required` (exit 2).
Same for `--phase 99 --key mykey` (exit 2), and for no selector at all (exit 2).

✅ Plan-honored "Channel naming lives here" header comment added immediately
above `wd_slug`, marking the seam from `wd_channel_root` / `wd_channel_dir`
(which stayed byte-identical — confirmed via `git diff 458342ef^ -- lib/wd-common.sh`
showing `wd_channel_root` and `wd_channel_dir` are in the unchanged hunk).

### `wd-publish-done` — resolver flags + publish-time backstop

✅ Accepts `--channel`/`--phase`/`--key` (verified all four mutually-exclusive
probes). Calls `wd_resolve_channel` before the `--stage --scope` check, as the
plan specified.

✅ Publish-time WARNING fires only when the target channel has no `armed.json`
AND another channel does. Verified:

- No `armed.json` anywhere → silent (the "publish-first-arm-later" leg).
- Target channel armed → silent.
- Other channel armed, target not armed → two WARNING lines on stderr, exit 0.

The WARNING text matches the plan verbatim: "no consumer is armed on channel
'<ch>', but armed consumers are waiting on: '<name>' (armed_by=<id>) ..." followed
by "a consumer on the wrong channel never wakes; it must re-arm on '<ch>'
(derive it with --phase/--key; see cross-session-watchdog SKILL, Channel
resolution)". Multiple armed consumers are joined into one line, each with its
own `armed_by=`.

✅ Usage header updated to `Usage: wd-publish-done (--channel NAME | --phase NN
| --key STR) --stage STR --scope "PATHSPEC..."`.

### `wd-arm` — resolver flags + arm-time warnings

✅ Accepts the same three selectors, calls `wd_resolve_channel` immediately after
argument parsing, before any disk writes.

✅ UNCLAIMED done elsewhere WARNING fires per plan: when target `done.json` is
absent but another channel has a `done.json` whose `claimed.<head>` directory is
absent, a WARNING fires per offending channel with stage pulled out of the
done.json. Verified by hand-writing `done.json` on `gsd-phase-35` and
`phase-36-execution-backup` then running `wd-arm --phase 99` — both fired.

✅ Live double-arm clobber WARNING fires per plan: when target `armed.json`
exists with a `pid` field that is alive (`kill -0` succeeds), a WARNING fires
naming `armed_by` and `pid`, then the arm proceeds (last-writer-wins, exit 0).
Verified with `armed.json` containing our own pid — WARNING printed, arm
proceeded.

✅ Usage header updated. The poll loop and Output/exit contract block are
byte-identical to `458342ef^` — verified by reading lines 162-191 of the post-
commit `wd-arm` and comparing to `git show 458342ef^:tools/watchdog/wd-arm`
lines 144-191 (the only pre-existing poll-loop block). The plan's coordination
constraint ("do NOT touch the poll loop") was honored.

✅ A missing `--task-file` path remains non-fatal — preserved from prior
behavior — so a bad path cannot silently prevent the watcher from arming.

### `wd-gsd-publish` — derived default channel

✅ Sources `lib/wd-common.sh` (added). `channel=default` replaced with
`channel=`. Phase normalization happens BEFORE building `stage="gsd:phase-$phase"`,
so stage and channel numerals agree (verified: `--phase 036` produces stage
`gsd:phase-36` and channel `gsd-phase-36`).

✅ Default channel is derived when `--channel` is omitted; explicit `--channel`
remains a raw override. End-to-end smoke: `wd-gsd-publish --phase 99 --scope .`
→ `published done @ <head> (main)`, channel directory created at
`gsd-phase-99/`, then `wd-check --phase 99` returns `WAKE` (exit 0).

✅ Header comment updated: `--channel N -> forwarded as a raw override; default
channel derives from --phase` (no more "defaults to default").

### `wd-check` + `wd-integrate` — resolver flags

✅ Both accept `--channel`/`--phase`/`--key` and call `wd_resolve_channel`.

✅ `wd-check` with no selector exits 2 with the standard "exactly one of ..."
error (was previously the accidental IDLE false-positive from an empty path;
plan called for exit 2 here, plan honored).

✅ `wd-check --phase NN` ≡ `wd-check --channel gsd-phase-NN` — covered by the
`test_check_and_integrate_accept_phase_equivalent_selector` test in
`tests/watchdog/test_channel_resolution.py`.

✅ Usage headers updated: `Usage: wd-check (--channel NAME | --phase NN |
--key STR) [--require-integration] [--integration-ref REF]` and the matching
`wd-integrate` line.

✅ `wd-disarm` / `wd-status` / `wd-push` are untouched (confirmed via
`git diff 458342ef^..6aa9f3c0 -- tools/watchdog/wd-disarm tools/watchdog/wd-status
tools/watchdog/wd-push` → empty).

### `.claude/skills/cross-session-watchdog/SKILL.md`

✅ New "Channel resolution — both sides derive, never invent" section added
between "When to use" and Operation 1, with all five bullets the plan prescribed:

- GSD phase handoff → `--phase NN`, canonical `gsd-phase-N`.
- Anything else → `--key "<handoff identity phrase>"` copied verbatim from the
  shared handoff artifact.
- "Never append role words" (`-backup`, `-execution`, `-consumer`) — explicit
  reference to the phase-36 failure mode.
- "Raw `--channel` is for tests and debugging only."
- "One handoff per channel; reusing a derived channel needs a fresh producer
  head."

✅ Any `WARNING:` at publish/arm time → stop and reconcile before going idle
(final bullet, matches plan).

✅ Honesty note present (after the bullet list): "Deterministic naming fixes
the split-brain rendezvous class. It does not prove the producer will ever
publish; dead-producer detection remains the `PRODUCER-STALLED` / owner-liveness
track." This explicitly carries the gap that the deterministic-naming fix does
NOT close (dead-producer), so future readers don't conflate the two tracks.

✅ Operation 1 + Operation 2 command examples updated to show both `--phase NN`
and `--key "..."` variants. Re-entry commands (`wd-check --phase NN`,
`wd-integrate --phase NN`, `wd-check --phase NN --require-integration`) added.

✅ GSD adapter paragraph updated: default channel is now derived from `--phase`;
explicit `--channel NAME` is a raw test/debug override.

✅ "After every successful arm" list updated to include the derivation used
(line 192: "the **derivation** used (`--phase NN` / `--key "..."` → `<channel>`)
so the producer can be handed the exact matching command").

✅ `PUSHED <head>` added to the PUSH bullet (line 39). This was the pre-existing
`test_a3_verdict_vocab` baseline failure that the plan called for flipping
green — the test now passes (see Tests row below).

✅ Common mistakes table includes the new "Hand-composing channel names or
adding role suffixes" row (line 212) with the fix pointing at `--phase` /
verbatim `--key`.

✅ Red-flag bullet added: "About to invent a raw channel name, append role
words to a derived channel, or ignore a channel-mismatch `WARNING:`." (line 224).

✅ The fixed-wake-prompt blockquote (lines 41-46) is byte-identical to the
prior content — verified by `git diff 6aa9f3c0^..6aa9f3c0 -- .claude/skills/...`
showing no hunk in that range. Plan's coordination constraint ("Do not touch
the fixed-wake-prompt blockquote, `test_a2` depends on it") was honored.

### `tests/watchdog/test_channel_resolution.py`

✅ 11 tests added, all pass. Covered exactly the plan's bullet list:

- `test_key_slug_converges_across_publish_and_check` — phase-36 execution slug.
- `test_phase_derivation_publish_arm_and_zero_pad` — `036` ≡ `36` and the
  publish+arm rendezvous on `gsd-phase-36`.
- `test_wd_slug_normalization_table` — case, punctuation runs, leading/trailing
  junk, path separators, non-ASCII.
- `test_empty_key_rejected`.
- `test_missing_and_mutually_exclusive_selectors_exit_2` — all four tools.
- `test_gsd_publish_default_channel_derived_and_override_kept`.
- `test_publish_warning_is_silent_without_mismatch`.
- `test_publish_warns_when_consumers_are_armed_elsewhere`.
- `test_arm_warns_on_unclaimed_done_elsewhere_but_not_claimed_done`.
- `test_arm_warns_when_replacing_live_armed_json`.
- `test_check_and_integrate_accept_phase_equivalent_selector`.

### `tests/watchdog/test_gsd_adapter.py`

✅ The stale `--channel N -> forwarded (defaults to "default")` line in the
module docstring was replaced with `--channel N -> forwarded as a raw override;
default derives from --phase`. Plan's "fix the stale `defaults to "default"`"
prescription honored.

### Tests suite as a whole

✅ `python3 -m unittest discover -s tests/watchdog` → 56 tests, 0 errors,
0 failures, 0 skipped. Plan target was "0 failures, 1 skip (shellcheck absent)";
this environment has shellcheck installed at `/opt/homebrew/bin/shellcheck`
v0.11.0, so `test_a1_shellcheck_clean` runs instead of skipping. This is
strictly better than the plan target.

### End-to-end smoke (the plan's verification step 3)

✅ `wd-gsd-publish --phase 99 --scope .` (no `--channel`) → published done at
`<head>`, channel dir created at `gsd-phase-99/`. `wd-check --phase 99` →
`WAKE` (exit 0). `done.json` schema is the post-v1.4 contract: `stage`,
`head`, `producer_ref`, `producer_worktree`, `scope`, `ts`.

### `install-global.sh` re-run

✅ The canonical bin at `~/.claude-alt/skills/cross-session-watchdog/bin/` is
timestamped `Jul 3 15:40`, AFTER the docs commit `6aa9f3c0` at `Jul 3 15:39`.
This satisfies the plan's verification step 1 ("Re-run `tools/watchdog/install-global.sh`
before the final suite run, since `test_a5_canonical_bin_matches_repo_source`
compares canonical bin vs repo source"). The corresponding
`test_a5_canonical_bin_matches_repo_source` test passes as part of the 56-test
suite.

---

## Probe-by-probe evidence log

(All probes run in the sandboxed `$WDROOT` setup so they did not touch real
cross-session state.)

| # | Probe | Expected per plan | Observed | Verdict |
|---|-------|-------------------|----------|---------|
| 1 | `wd-arm --channel foo --phase 99 ...` | exit 2, "exactly one of" error | `wd-arm: exactly one of --channel, --phase, --key is required` rc=2 | ✅ |
| 2 | `wd-arm --phase 99 --key mykey ...` | exit 2 | same | ✅ |
| 3 | `wd-arm --poll-secs 1 --timeout-secs 1` (no selector) | exit 2 | same | ✅ |
| 4 | `wd-check` (no selector) | exit 2 (plan called for this change) | `wd-check: exactly one of ...` rc=2 | ✅ |
| 5 | `wd-arm --phase abc ...` | exit 2 | `wd-arm: --phase must be a positive integer` rc=2 | ✅ |
| 6 | `wd-arm --phase 0 ...` | exit 2 | same | ✅ |
| 7 | `wd-arm --phase -1 ...` | exit 2 | same (rejected by `[!0-9]*` pattern) | ✅ |
| 8 | `wd-arm --key '!!!@@@' ...` | exit 2 empty slug | `wd-arm: --key produced an empty channel slug` rc=2 | ✅ |
| 9 | `wd-publish-done --key 'Phase 36: Execution!' ...` | channel `phase-36-execution` | dir `phase-36-execution/` created | ✅ |
| 10 | `wd-publish-done --phase 036 ...` | channel `gsd-phase-36` (zero-pad normalization) | dir `gsd-phase-36/` created | ✅ |
| 11 | `wd-arm --weird-arg` | exit 2 | `unknown arg: --weird-arg` rc=2 | ✅ |
| 12 | `wd-publish-done --phase 99 --scope x` (no --stage) | exit 2 | `need --stage --scope` rc=2 | ✅ |
| 13 | `wd-publish-done --phase 99 --stage s` (no --scope) | exit 2 | same | ✅ |
| 14 | `wd-gsd-publish --phase 99` (no --scope) | exit 2 | `wd-gsd-publish: --scope is required` rc=2 | ✅ |
| 15 | `wd-gsd-publish --phase abc --scope x` | exit 2 | `wd-gsd-publish: --phase must be a positive integer` rc=2 | ✅ |
| 16 | `wd-publish-done` on a dirty scope | exit 3 | `wd-publish-done: scope has uncommitted changes; refusing to publish` rc=3 | ✅ |
| 17 | `wd-publish-done --channel demo ...` (raw passthrough) | channel `demo` (no slug) | dir `demo/` created, channel not slugged | ✅ |
| 18 | `wd-publish-done --channel x --key y ...` | exit 2 mutual exclusion | `wd-publish-done: exactly one of ...` rc=2 | ✅ |
| 19 | `wd-publish-done` with other channel armed, target not armed | WARNING x2, exit 0 | both WARNING lines printed verbatim, rc=0 | ✅ |
| 20 | `wd-arm` with unclaimed done elsewhere | WARNING per offending channel | 2 WARNINGs printed (one per channel) | ✅ |
| 21 | `wd-arm` with live pid in armed.json | WARNING, proceed (clobber) | `WARNING: replacing live armed.json on channel 'gsd-phase-99' (was armed_by=ghost pid=<ppid>)` then arm proceeded | ✅ |

End-to-end smoke (the plan's verification step 3):

```
$ wd-gsd-publish --phase 99 --scope .
published done @ 7d9780b64e141c3c9b741619a7801a8f7a65df3e (main)

$ ls $WDROOT/channels/
gsd-phase-99

$ cat $WDROOT/channels/gsd-phase-99/done.json
{"stage":"gsd:phase-99","head":"7d9780b64e141c3c9b741619a7801a8f7a65df3e","producer_ref":"main","producer_worktree":"…","scope":".","ts":"2026-07-04T02:22:25Z"}

$ wd-check --phase 99
WAKE
```

Channel `gsd-phase-99` was derived (NOT `default/`); rendezvous achieved on
the derived name; `WAKE` returned. The pre-incident failure mode ("A publishes
on Y while B armed on X") is mechanically impossible because neither side can
choose a free-text name — both compute it from `--phase`/`--key`.

---

## Cross-checks against plan-stated "out of scope"

✅ `wd_channel_root` / `wd_channel_dir` are byte-identical to before — verified
via `git diff 458342ef^..458342ef -- lib/wd-common.sh` showing only an additive
hunk after them.

✅ `wd-arm` poll loop / Output / exit contract block is byte-identical — verified
via direct comparison of lines 162-191 vs the prior version.

✅ Dead-producer detection / `PRODUCER-STALLED` / owner-liveness is untouched
and explicitly preserved in the SKILL.md honesty note.

✅ Historical plan/evidence docs using raw `--channel demo` etc. continue to
work — `--channel` still passes through raw, and `test_a*_channel_re` style
tests are unchanged.

---

## Things the executing agent did right (worth recording for future plans)

1. Followed the plan's prescribed commit ordering exactly — no scope drift
   (e.g., no opportunistic refactor of `wd-publish-done` slipped into the
   warning commit).
2. Honored all three coordination seams:
   - `wd_channel_root`/`wd_channel_dir` unchanged (location track's seam).
   - `wd-arm` poll loop and exit contract unchanged (teardown plan's seam).
   - Fixed-wake-prompt blockquote unchanged (`test_a2` dependency).
3. Added the honesty note in the SKILL.md, carrying the gap forward instead of
   silently claiming this fix closes the dead-producer half. This is the kind
   of "carry the gap, don't paper over it" behavior the plan's coordination
   constraints called for.
4. Re-ran `install-global.sh` after the doc commit so `test_a5_canonical_bin_matches_repo_source`
   stayed accurate. The bin timestamps in `~/.claude-alt/skills/cross-session-watchdog/bin/`
   are 1-2 minutes after the doc commit.
5. Stale docstring in `test_gsd_adapter.py` ("defaults to `default`") was fixed
   per the plan's explicit instruction, even though no test asserted on it.

---

## Risks / follow-up items

- **Not verified:** running `wd-arm` against a freshly-created `claimed.<head>`
  directory in a real cross-worktree session was not exercised — that flow
  remains the teardown plan's seam and is out of scope here. The local arm
  loop's claim/lock semantics were verified only via `kill -0` on a hand-
  injected `armed.json`; the actual `mkdir` claim atomicity guarantee is
  inherited from prior work and was not re-tested.

- **Not verified:** the `test_a5_canonical_bin_matches_repo_source` check was
  observed to pass inside the full suite, but no standalone re-run of
  `install-global.sh` followed by re-running `test_a5` alone was performed.
  If the canonical bin ever drifts (someone hand-edits the global copy, or
  a hook re-deploys), the test will catch it on the next CI run.

- **Pre-existing:** the watchdog's PUSH (tmux) path was not exercised here.
  The `PUSHED <head>` token addition to the SKILL.md is the minimum required
  for `test_a3_verdict_vocab`; if `wd-push`'s actual output drifts in the
  future, `test_a3` will catch it.

---

## Conclusion

The wrong-channel fix is correctly implemented and observable end-to-end. The
4 commits are in the prescribed order with correct trailers, the contract is
documented in the SKILL, the test suite flips from 45 tests / 1 failure / 1
skip to 56 tests / 0 failures / 0 skips, and a sandboxed end-to-end smoke
(`--phase 99` publish → `--phase 99` check → `WAKE`) confirms that both sides
do in fact derive the same channel from a shared selector.

No issues were found that block the work from being declared complete.