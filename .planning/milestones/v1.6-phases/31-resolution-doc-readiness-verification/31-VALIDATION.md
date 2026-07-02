---
phase: 31
slug: resolution-doc-readiness-verification
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-20
---

# Phase 31 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Phase 31 produces **markdown deliverables, not code** — so "tests" are structural / derivability
> assertions over the two files plus a git-diff invariant and one reviewer judgment pass. There is
> no test framework (the v1.5 24.5 analog used none either). Source: `31-RESEARCH.md` §Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — documentation-verification phase. Checks are shell one-liners (`grep`/`wc`/`sed`/`git`) + a reviewer judgment pass. |
| **Config file** | none |
| **Quick run command** | the structural `grep`/`wc` assertions for whichever deliverable a task wrote (below) |
| **Full suite command** | the full set (all greps + the `git diff --name-only` invariant + the verdict-derivability judgment) run at plan close before `/gsd-verify-work` |
| **Estimated runtime** | ~5 seconds (shell assertions) + reviewer pass |

---

## Sampling Rate

- **After every task commit:** Run the structural `grep` assertions for the deliverable that task produced.
- **At plan close (phase gate):** Run the full check set green; perform the verdict-derivability judgment pass.
- **Before `/gsd-verify-work`:** Full set green + the `git diff` zero-edit invariant confirmed.
- **Max feedback latency:** ~5 seconds (shell) — the judgment pass is manual.

---

## Per-Task Verification Map

> Task IDs are assigned by the planner (`31-01-PLAN.md`). The check → deliverable mapping is fixed here;
> the planner binds each check to the task that produces its deliverable.

| Check | Deliverable | Wave | Behavior asserted | Test Type | Automated Command (illustrative) | File Exists | Status |
|-------|-------------|------|-------------------|-----------|----------------------------------|-------------|--------|
| Map row-count = 18 | `31-RESOLUTION-MAP.md` §2 | 1 | The finding→section mapping covers exactly the 18 selected findings (SPEC R3) | structural | count mapping-table body rows → expect 18 | ❌ W0 | ⬜ pending |
| Report sections present | `31-READINESS-REPORT.md` | 1 | All 8 sections present (exec verdict, pre-exec gate, 4 checks, gap list, fix instructions, re-check protocol, gate decision, acceptance check) | structural | `grep -nE "^#{1,3} " 31-READINESS-REPORT.md` asserts each heading | ❌ W0 | ⬜ pending |
| Map sub-sections present | `31-RESOLUTION-MAP.md` | 1 | Identity + §1 index + §2 mapping + §3 citation guide + §4 verdict-direction + §5 out-of-scope + §6 carry-forward | structural | `grep -nE "^#{1,3} "` asserts each; assert a `…03-final-resolution.md:START–END` example string | ❌ W0 | ⬜ pending |
| Citation example resolves | `31-RESOLUTION-MAP.md` §3 | 1 | The `…:START–END` example lands inside the cited section of the committed doc | structural | `sed -n 'START,ENDp'` the range; confirm it falls in the named section | ❌ W0 | ⬜ pending |
| Verdict derivable | `31-READINESS-REPORT.md` §1 | 1 | Exec-summary verdict matches the SPEC R7 precedence applied to the four check tables (no rubber-stamp) | judgment | reviewer re-derives the verdict from the tables | ❌ W0 | ⬜ pending |
| Zero spec/pinn/doc edits | Phase 31 commit | 1 | The commit edits nothing it must not (SPEC R8 acceptance) | invariant | `git diff --name-only <commit>` shows zero `ctl_instruction.md` / `pinn_architecture.md` / `03-final-resolution.md` / `pinn/**` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `31-READINESS-REPORT.md` — does not exist yet (produced by the report task).
- [ ] `31-RESOLUTION-MAP.md` — does not exist yet (produced by the map task).
- [ ] No test framework to install — assertions are shell one-liners + a reviewer judgment pass (the 24.5 analog used none).

*Existing infrastructure (shell + git + the verified 24.5 analog as the template) covers all phase checks.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Verdict derivability | SPEC R7 | The gate verdict is a reasoned consolidation of four check tables; correctness is a judgment, not a string match | Re-derive `READY`/`READY-WITH-CAVEATS`/`NOT-READY` from the four check tables by the fixed precedence; confirm it matches the exec summary |
| No invented coverage/verdict | SPEC R8 / STOP protocol | "Silence reported as a gap, never filled" is a semantic property no grep can prove | Reviewer confirms every `silent`/`partial` row is a gap and no finding carries an inferred verdict |

---

## Validation Sign-Off

- [x] All checks have an automated structural assertion or a named manual judgment pass
- [x] Sampling continuity: every deliverable has at least one structural assertion
- [x] Wave 0 covers the two not-yet-written deliverables
- [x] No watch-mode flags
- [x] Feedback latency < 5s (shell assertions)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
