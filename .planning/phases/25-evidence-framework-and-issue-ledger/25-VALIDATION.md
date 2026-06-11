---
phase: 25
slug: evidence-framework-and-issue-ledger
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-11
---

# Phase 25 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> Phase 25 produces **no executable code and no acceptance-check execution** (AC execution
> is Phase 29, VER-09). "Validation" here is artifact-completeness verification — doc
> review against the EVID/VER requirement contracts plus git invariants — not a test suite.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — non-code phase. Verification is doc-completeness review + git invariants. |
| **Config file** | n/a |
| **Quick run command** | `git diff --check` (whitespace/conflict-marker invariant); `scripts/agent-commit` precondition (`GIT_AGENT_ID` set) |
| **Full suite command** | n/a — acceptance-check execution is Phase 29 (VER-09) |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `git diff --check`; confirm the task's artifact exists on disk with required sections (grep assertions from the task's acceptance criteria).
- **After every plan wave:** Re-read each artifact produced in the wave against its requirement row in the map below.
- **Before `/gsd-verify-work`:** Every row in the Per-Requirement Verification Map must be ✅.
- **Max feedback latency:** 60 seconds (doc review, no build step).

---

## Per-Requirement Verification Map

| Req ID | Behavior | Verification Type | How verified (Phase 25) | Artifact |
|--------|----------|-------------------|--------------------------|----------|
| EVID-06 | 4-source line-range citations per packet | doc review | each EVID-10 record cites issue doc + resolution doc + framework spec + DATA-xx with line ranges (never whole files) | the 3 EVID-10 records |
| EVID-07 | verdict from fixed enum | doc review | each record carries exactly one of `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` | the 3 EVID-10 records |
| EVID-08 | false positives documented as intentional non-changes | doc review | template false-positive section present; any no-change verdict names which source misread and why the convention stands | template + records |
| EVID-09 | before/after note per accepted finding | doc review | before/after section names changed spec section + contract enforced + verification step | template + records |
| EVID-10 | root-cause adjudication for the 3 known conflicts | doc review | each record names the root-cause ambiguity, which source was right/wrong, and the convention now locked | 3 EVID-10 records |
| VER-10 | ledger lifecycle + re-verification rule | doc review | Lifecycle Rules re-issued for Phases 26–29; `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` state machine, "fix applied ≠ closure", and batch regression re-verification present | 24-ISSUE-LEDGER.md |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `evidence/_TEMPLATE.md` — does not exist yet; create from v1.4 precedent (CONTEXT D-04)
- [ ] `evidence/README.md` — does not exist yet; create from v1.4 precedent (CONTEXT D-03/D-05)
- [ ] `25-GAPS.md` — create only on first STOP gap (do not pre-create)

*No test-framework install needed — non-code phase.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Citation line-range accuracy | EVID-06 | Line ranges reference prose in four source docs; correctness requires reading the cited spans | Open each cited file at the cited range; confirm the quoted/paraphrased claim appears within it |
| Verdict grounding faithfulness | EVID-07/10 | Whether a verdict transcribes vs invents requires comparing record text against the resolution doc's position | Diff each record's verdict + reasoning against the resolution-doc section mapped in `24.5-RESOLUTION-MAP.md` |

---

## Validation Sign-Off

- [ ] All tasks have doc-review verification or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without an artifact-existence/grep check
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
