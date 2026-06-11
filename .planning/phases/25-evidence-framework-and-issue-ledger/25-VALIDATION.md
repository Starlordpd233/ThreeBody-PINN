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
| **Quick run command** | `git diff --check` (whitespace/conflict-marker invariant); `test -x scripts/agent-commit`; `test -n "$GIT_AGENT_ID"` and `test -n "$GIT_AGENT_OWNED_PATHS"` before file mutation |
| **Full suite command** | n/a — acceptance-check execution is Phase 29 (VER-09) |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `git diff --check`; confirm the task's artifact exists on disk with required sections (grep assertions plus structural checks below).
- **After every plan wave:** Re-read each artifact produced in the wave against its requirement row in the map below; verify the `##` heading set matches the v1.4 template plus the required `### Dataset Evidence (§3b)` sub-block.
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

## Structural Checks

- [ ] `_TEMPLATE.md` has exactly the v1.4 title plus 12 `##` headings; `### Dataset Evidence (§3b)` exists under `## Spec Evidence` and is not a new `##` heading.
- [ ] Each EVID-10 record has the same 12 `##` heading names as `_TEMPLATE.md`; M11/M12 sub-parts are nested under existing sections.
- [ ] `evidence/README.md` places `### D-03 Downstream Enforcement` under `## Phase-Exit Rule`, after the copied v1.4 phase-exit language.
- [ ] Ledger relative links are computed from `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/` to `../25-evidence-framework-and-issue-ledger/evidence/{filename}`.
- [ ] D-14 negative path: if no shared contract is found, `git diff -- .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` shows no `Dependents:` changes for that row.
- [ ] Post-commit boundary: `git show --stat HEAD` lists every record file, `25-02-SUMMARY.md`, and `24-ISSUE-LEDGER.md` in the same commit for Plan 25-02.

---

## Wave 0 Requirements

- [ ] `GAP-25-01` resolved before Phase 25 execution starts; split vs literal/hybrid scope is user-confirmed.
- [ ] `24.5-READINESS-REPORT.md` exists and records READY or READY-WITH-CAVEATS; NOT-READY or missing report blocks execution.
- [ ] v1.4 precedent files exist: Phase 16 `_TEMPLATE.md`, `README.md`, and completed conflict packet `B-02.md`.
- [ ] `scripts/agent-commit` executable and `GIT_AGENT_ID` / `GIT_AGENT_OWNED_PATHS` set before any file mutation.
- [ ] `evidence/` directory is explicitly created with `mkdir -p` before writing `_TEMPLATE.md`.
- [ ] `25-GAPS.md` exists with open gaps; append future STOP gaps, do not overwrite.

*No test-framework install needed — non-code phase.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Citation line-range accuracy | EVID-06 | Line ranges reference prose in four source docs; correctness requires reading the cited spans | Open each cited file at the cited range; confirm the quoted/paraphrased claim appears within it |
| Verdict grounding faithfulness | EVID-07/10 | Whether a verdict transcribes vs invents requires comparing record text against the resolution doc's position | Diff each record's verdict + reasoning against the resolution-doc section mapped in `24.5-RESOLUTION-MAP.md` |
| Line-range drift repair | EVID-06/10 | Some cited line numbers came from resolution-doc self-cites and may shift | Search for the quoted claim text, not only the expected line number; update to the actual line range if found; if the claim cannot be found, fire a STOP gap |
| Readiness-caveat routing | D-15/D-16 | 24.5 caveats may affect only some records | Enumerate every readiness-report caveat; propagate those touching SCS/D=6.694/M11/M12 into the record, and explicitly carry unrelated caveats to the owning Phase 26-28 packet |

---

## Validation Sign-Off

- [ ] All tasks have doc-review verification or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without an artifact-existence/grep check
- [ ] Wave 0 covers all MISSING references and open Phase 25 gap gates
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
