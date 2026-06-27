---
status: active
purpose: verification-report
created: 2026-06-27
milestone: untracked
phase: cross-cutting
retirement_trigger: >
  Retire when Phase 2 (MVP build) lands and the watchdog's first end-to-end handoff
  is demonstrated. Phase 1 evidence + this verification remain valid for as long as
  Claude Code's harness primitives (`Bash` background re-entry, `CronCreate`) behave as
  observed in 2026-06-26; re-verify after any harness upgrade that touches either.
---

# Phase 1 Verification — Cross-Session Watchdog

Verifies that Phase 1 of
`docs/work/plans/cross_cutting/parallel-agent-coordination-watchdog/2026-06-26-cross-session-watchdog-implementation-plan.md`
is genuinely complete against its own acceptance criteria.

## Phase 1 deliverable (per the plan)

> *"Prove unattended idle-wake in a real two-terminal TUI; pick the primary wake path."*

Phase overview row: `Build now? yes | Gate: manual test PASS`.

## Acceptance criteria

1. P1 background-watcher re-entry demonstrated in a real idle TUI.
2. P2 durable-cron re-entry demonstrated in a real idle TUI (or honestly deferred with rationale).
3. Evidence file committed with PASS/FAIL + latencies + observed re-entry mode.
4. Primary wake path chosen and recorded.
5. Termination-guarantee requirement captured in the plan (Phase 4) given the
   recurring-timer drain risk surfaced by the P2 test.

## Verification matrix

| Criterion | Evidence | Verdict |
|---|---|---|
| 1. P1 demonstrated | `65105313` test(governance): record unattended idle-wake results and re-home PTY proof — first commit on this work. Re-entry observed: terminal 1 printed `WOKE` with no human keystroke after `/tmp/wd_wake_demo` appeared. | **MET** |
| 2. P2 demonstrated | `9513d00` evidence(governance): record P2 cron wake PASS with caveats and discoveries. Re-entry observed: consumer session printed `WOKE-CRON` repeatedly, every minute, with no human keystroke. Foreground-required caveat recorded. | **MET** |
| 3. Evidence committed | `tools/watchdog/evidence/2026-06-26-idle-wake-results.md` on disk at `master` `9513d00`. Frontmatter compliant with docs conventions; PASS/FAIL + latencies + re-entry mode recorded for both P1 and P2; "Discoveries" section added with the 3 findings as Phase 4 regression targets. | **MET** |
| 4. Primary path chosen | Evidence file's "Decision (Phase 1 Step 4 gate)" records: **P1 primary** (low latency, inherently drain-safe); P2 fallback gated on Phase 4 termination contract; PUSH (tmux) optional accelerator. Plan's Phase 1 decision-gate bullet updated to reflect the same. | **MET** |
| 5. Termination contract in plan | `130f7c5` plan(docs): add guaranteed-termination contract to Phase 4 and capture P2 risk findings. New "Termination guarantee (hard requirement — discovered 2026-06-26)" subsection specifies the 5 layers (disarm-on-success, self-termination TTL+disarm flag, external `wd-disarm`, `wd-status`, conservative defaults). Phase 1 decision gate gates P2 on this. Risks / scope guard captured. | **MET** |

## Honesty notes (gaps and how they were closed)

- **Phase 1 Step 1 (re-home PTY proof) was not run.** `/tmp/wd_pty_proof.py` was absent
  at session resume; it was never copied into `tools/watchdog/`. The plan checkbox was
  updated to `[x]` with a one-line deferral note explaining that the PTY proof pertains
  to the PUSH path (Phase 5, optional) and will be regenerated only if/when Phase 5 is
  taken up. The deferral is documented and does not gate Phase 1's deliverable
  (PULL wake), since the PUSH proof is not on the PULL critical path.
- **P2's "durable" came out session-only on first two arming attempts** through a
  `claude` agent on the user's behalf, despite the `durable: true` flag. Discovered
  during the test, recorded as a MEDIUM-severity finding in the evidence file's
  "Discoveries" section and the plan's Risks block. The arming skill for Phase 4 must
  verify persistence on disk after arming.

## Commits on `master` (local, no push)

- `65105313` test(governance): record unattended idle-wake results and re-home PTY proof
  (Phase 1 first commit — recorded P1 PASS; PTY proof was already absent at that time).
- `9513d00` evidence(governance): record P2 cron wake PASS with caveats and discoveries
  (P2 result + Discoveries + Decision gate update).
- `130f7c5` plan(docs): add guaranteed-termination contract to Phase 4 and capture P2
  risk findings (Phase 4 termination contract + Risks / scope guard + Phase 1 Step 1
  deferral + Phase 1 decision gate update).

All three commits used `scripts/agent-commit` with `GIT_AGENT_ID=watchdog-build` and
explicit `GIT_AGENT_OWNED_PATHS`; no unrelated `M` files or untracked items were staged.
`65105313` was never amended.

## Conclusion

**Phase 1 is complete.** The deliverable is met; the evidence is on disk and reflects
what actually happened; the primary path is chosen; the drain risk surfaced by P2 is
captured as a hard Phase 4 requirement, not left as an open finding. The next step is
Phase 2 (MVP build: `wd-common.sh`, `wd-publish-done`, `wd-check`, `wd-arm`,
`tests/watchdog/test_watchdog_mvp.py`).