---
title: "Phase 22 Execution — Gatekeeper Verification Review"
phase: 22
slug: framework-spec-cleanup
type: execution-verification
status: active
purpose: review-findings
role: verification-gatekeeper
reviewer: Claude (verification-before-completion)
created: 2026-06-09T14:33:04+08:00
scope: "Plans 22-01 → 22-05 (Wave 0 → Wave 3)"
verdict: "WORK CORRECT / RECORD DEFECTIVE — automated gates G1–G3 verified green with fresh evidence; G4 visual backstop genuinely PENDING-USER-REVIEW (phase not yet closeable). Several false/contradictory statements in commit messages and plan summaries must be corrected."
baseline_tag: v1.4-pre-phase-22 (faa73d0)
head_at_review: 7375fe6 (+ uncommitted 22-03-SUMMARY.md edit, untracked 22-02-transform.mjs)
---

# Phase 22 Execution — Gatekeeper Verification Review

**Reviewer stance:** I did not trust the prior agent's summaries. Every claim below was
re-derived from fresh commands against the live repository (detector re-run, git diff against the
baseline tag, file-state greps, JSON entry counts, commit-existence checks). Commands and raw
outputs are in the Evidence Appendix.

---

## 1. Executive Verdict

**The executed engineering work is correct and the automated gates pass on fresh evidence.**
The detector runs green, the three specs are clean against the baseline, content was preserved in
the claimed categories, all 26 author comments survived, and the governance scaffolding
(gaps, FUT-05, ledger) is in place.

**However, the *record* of that work contains multiple false or contradictory statements** — most
seriously a commit message and a plan summary that both claim footnotes were "preserved as
`[^n]`" when the commit in fact *converted* them to `[n]`. For a v1.4 adjudication milestone whose
governing philosophy is "transcribe what is explicit, never invent," false claims in the
phase record are consequential: downstream consumers (FUT-01, FUT-05) read these summaries as
ground truth.

**Phase 22 is NOT yet complete.** The G4 *manual* Cursor/VS Code render review is correctly marked
`PENDING-USER-REVIEW`. Decision contract D-09/D-10 require *both* automated and manual review to
pass; the human half is outstanding by design. ROADMAP correctly still shows `- [ ] Phase 22`.

| Dimension | Result |
|-----------|--------|
| Automated gates G1 (selftest), G2 (per-file 0-residual), G3 (content + comments) | ✅ VERIFIED GREEN (fresh) |
| G4 automated proxy | ✅ PASS |
| G4 manual visual backstop | ⏳ PENDING-USER-REVIEW (honest; blocks phase close) |
| End-state correctness of specs | ✅ CORRECT |
| Accuracy of phase record (summaries / commit messages) | ❌ 4 false/contradictory claims (F1–F4) |
| State tracking / committed-artifact hygiene | ⚠️ stale + uncommitted artifacts (F5–F6) |

---

## 2. What Was Verified Green (fresh evidence)

| # | Claim | Verification | Result |
|---|-------|--------------|--------|
| V1 | Detector toolchain committed + runnable | `ls tools/spec-render-check/`; `node_modules` present; node v24.16.0 | ✅ |
| V2 | G1 selftest exit 0 | `detect.mjs --selftest` → sanity gate PASS, 9 regions, neg-control clean, **exit 0** | ✅ |
| V3 | G2 pinn_architecture.md | `--adjudications 22-02…json` → `0 DEFINITE, 0 REVIEW, 7 ADJUDICATED, 14 SUPPRESSED`, **exit 0** | ✅ matches claim |
| V4 | G2 ctl_instruction.md | `--adjudications 22-03…json` → `0 DEFINITE, 0 REVIEW, 10 ADJUDICATED, 5 SUPPRESSED`, **exit 0** | ✅ matches claim |
| V5 | G2 sampling_method.md | no adjudication → `0 DEFINITE, 0 REVIEW, 0 ADJUDICATED, 1 SUPPRESSED`, **exit 0** | ✅ matches claim |
| V6 | G3 content: sampling unchanged | `git diff --quiet faa73d0 HEAD -- sampling_method.md` | ✅ 0 hunks |
| V7 | G3 content: hunk counts | pinn = **23 hunks**, ctl = **8 hunks** | ✅ matches claim exactly |
| V8 | Footnotes converted to render-safe form | tag `[^n]`=37 → live `[^n]`=0 / `[n]`=39; heading `## References` | ✅ correct end-state |
| V9 | Comment census = 26 (13+13+0) | `detect.mjs --census` union; PRE/POST/DIFF/HANDOFF/live all agree | ✅ |
| V10 | Handoff artifact well-formed | `22-COMMENT-HANDOFF.md` has **26** numbered rows, verbatim text + preservation flag; HB-01 line-1430 `\` preserved verbatim | ✅ |
| V11 | 22-02 adjudication allowlist | JSON = **7** entries, all 7 matched/cleared | ✅ |
| V12 | Gaps resolved | GAP-22-01/02/03 = `RESOLVED-WITH-INSTRUCTION` in both `22-GAPS.md` and `v1.4-GAPS.md` | ✅ |
| V13 | VER-05 ledger reconciliation | `16-ISSUE-LEDGER.md` Phase 22 addendum (P22-R1/R2/R3 VERIFIED; prior-finding re-verification) added by `7375fe6` (+103 lines) | ✅ |
| V14 | FUT-05 registered | `REQUIREMENTS.md` FUT-05 owns `22-COMMENT-HANDOFF.md` | ✅ |
| V15 | Baseline tag | `v1.4-pre-phase-22` → `faa73d0` | ✅ |
| V16 | Verified == committed | 3 specs clean in working tree (no uncommitted spec edits) | ✅ |
| V17 | No false "phase complete" in ROADMAP | ROADMAP line 127 still `- [ ] Phase 22` | ✅ honest |

The end-state of the corpus is correct. The detector, the fixtures, the negative control, the
adjudication mechanism, the content preservation, and the comment census all hold up under
independent re-execution.

---

## 3. Findings (defects in the record / hygiene)

| ID | Severity | Title | Work vs Record |
|----|----------|-------|----------------|
| **F1** | **HIGH** (record integrity) | Commit `94d8e79` message **and** 22-02 summary falsely claim footnotes were "preserved as `[^n]` (not converted)" — the commit converted them | Work correct, record **false** |
| **F2** | **MEDIUM** | 22-03 summary "Task 1: No action required" contradicts commit `5bfbd20`, which performed Task-1 edits | Work correct, record **false** |
| **F3** | **LOW** | 22-02 summary cites nonexistent commit `ac601e9` for the table conversion and for "per-construct checkpoint hashes" | Record **wrong SHA** |
| **F4** | **LOW** | 22-03 adjudication allowlist has **11** entries (not 10); 2 are orphans matching no finding | Mild over-broad allowlist |
| **F5** | **LOW** | `STATE.md` is stale — says "Next action: Execute Phase 22" as if unstarted | State tracking lag |
| **F6** | **LOW** | Uncommitted/untracked phase artifacts (`22-02-transform.mjs` untracked; `22-03-SUMMARY.md` edit uncommitted) | Committed-evidence hygiene |
| **F7** | **INFO** | G4 manual visual review genuinely outstanding → phase not closeable | Honest, by design |

### F1 — HIGH — False footnote-preservation claim (commit message + summary)

**The defect.** Plan 22-02's Stage-0 footnote probe (22-01) concluded the Cursor preview renders
Pandoc footnotes as `unsupported`, so footnotes were to be converted to a render-safe `[n]` form.
The conversion **did happen and was the correct call** — but it is described as its own opposite in
two committed records:

- **Commit `94d8e79`** ("fix(22-02): normalize bare subscripts + convert backtick math") changed
  `pinn_architecture.md` `[^n]` count **37 → 0** (verified: `git show 94d8e79~1:… | grep -c '[^n]'`
  = 37; `git show 94d8e79:…` = 0). Yet its commit-message body states:
  *"Preserved all 39 Pandoc footnote references `[^n]` and definitions."*
  **The message asserts the exact opposite of what the commit did.**
- **`22-02-SUMMARY.md`** repeats it: *"All 39 Pandoc footnote references `[^n]` and definitions
  `[^n]:` preserved (not converted to `[n]`)."* — **false** against live state.

**The contradiction inside the phase.** `22-05-SUMMARY.md` (G3) and the `16-ISSUE-LEDGER.md`
addendum both correctly record *"footnote form `[^n]` → `[n]` per Stage-0 probe."* So the phase
record disagrees with itself; the 22-02-level records are the wrong ones.

**Live ground truth.** `pinn_architecture.md`: 0 `[^n]` refs, 39 `[n]` refs, heading
`## References`. This is the render-safe form the Stage-0 probe mandated, and it is why the detector
reports 0 DEFINITE (the `pinn-footnote` fixture expects `flag` for surviving `[^n]`).

**Impact.** The *work* is correct. The *risk* is that a future agent (FUT-01 rebuilding code from
specs, or FUT-05 adjudicating comments) reads 22-02-SUMMARY / `94d8e79` and believes the specs
still carry Pandoc `[^n]` footnotes, or that conversion was rejected — a false premise.

**Required correction.** Amend `22-02-SUMMARY.md` to state footnotes were converted `[^n]`→`[n]`
(render-safe per Stage-0 probe), consistent with 22-05 and the ledger. The commit message of
`94d8e79` cannot be edited without history rewrite; add a corrective note in the summary and/or
ledger explicitly flagging the stale `94d8e79` message.

### F2 — MEDIUM — 22-03 "Task 1: No action required" contradicts commit `5bfbd20`

`22-03-SUMMARY.md` Task 1 states: *"No action required… The three `$$\begin{aligned}` blocks…
were already in own-line positions in the committed file. No edits were needed for Task 1."*

Commit **`5bfbd20`** ("fix(22-03): move mid-list `$$\begin{aligned}` to own lines") contradicts
this directly. Its message: *"Fixed 2 mid-list block math sites (lines 679, 703) where
`$$\begin{aligned}` was appended to bold list text… Removed Pandoc attribute `{#sec:ctl:step3}`
from line 655… All 22 DEFINITE findings resolved (D4 survivors eliminated)."* `git show --numstat
5bfbd20` = **15 insertions / 7 deletions** to `ctl_instruction.md`.

So Task-1-type work *was* performed and committed; the summary says it was not. The summary's
"Commits" section also lists only `7fe572e`, omitting `5bfbd20`. **Required correction:** rewrite
22-03 Task 1 to describe the `5bfbd20` edits and add it to the commit list.

### F3 — LOW — Nonexistent commit SHA `ac601e9` cited in 22-02 summary

`22-02-SUMMARY.md` cites **`ac601e9`** ("fix(22-02): convert Pandoc multiline tables to GFM…") as
the table-conversion commit and as where "per-construct checkpoint hashes" are recorded. **No such
commit exists** (`git cat-file -t ac601e9` → MISSING). The real table-conversion commit is
**`acb8aa8`** ("convert Pandoc structures… to GFM"). Consequently the summary's claim that
byte-for-byte checkpoint hashes are "recorded in commit `ac601e9`" points to nothing — the
governance requirement (record verifiable invariants in committed state, not `/tmp`) is not
demonstrably met via that reference. (Byte preservation is still independently checkable via
`git diff`, which I confirmed.) **Required correction:** fix the SHA to `acb8aa8`; relocate or
re-derive the hash evidence into committed state.

### F4 — LOW — 22-03 allowlist has 11 entries, not 10 (2 orphans)

`tools/spec-render-check/adjudications/22-03-ctl-instruction.json` contains **11** entries; the
detector clears **10**. The two orphans match no finding:
- `dE/E` @ line 356 (no corresponding REVIEW finding)
- `cpu_times` @ line 358 (this token is `SUPPRESSED`, not a REVIEW finding)

The 22-03 summary and front-matter say "10-entry allowlist." Harmless to the current gate
(detector still exits 0), but an over-broad allowlist could silently clear a *future* genuine
finding at those tokens. **Suggested:** prune the 2 orphan entries or document them as intentional.

### F5 — LOW — `STATE.md` is stale

`.planning/STATE.md` still reads "Current focus: Phase 22 … (Phase 21 complete)", "Plan: Next —
Phase 22", and "Next action: Execute Phase 22" — i.e., as though Phase 22 has not begun. All five
plans (22-01…22-05) have executed and the detector is green. STATE should reflect "Phase 22 plans
executed; pending G4 manual visual backstop." (ROADMAP is correct; only STATE lags.)

### F6 — LOW — Uncommitted / untracked phase artifacts

- `**.planning/phases/22-framework-spec-cleanup/22-02-transform.mjs**` (10.6 KB) is **untracked**.
  This appears to be the table-transform reproducibility script. The 22-02 summary instead
  referenced an ephemeral `/tmp/convert-both-tables.mjs`. Neither is in committed state, so the
  byte-for-byte table-conversion is not reproducibly evidenced per the commit-protocol governance.
- `**22-03-SUMMARY.md**` has an **uncommitted** edit (fills the Commits section with `7fe572e`); the
  committed copy still shows the `_(to be filled in after commit)_` placeholder.

**Suggested:** commit or remove `22-02-transform.mjs`; commit the 22-03 summary edit.

### F7 — INFO — G4 manual review outstanding (phase not closeable)

`22-05-SUMMARY.md` and `22-RENDER-REVIEW.md` correctly mark the manual Cursor/VS Code render review
`PENDING-USER-REVIEW`. This is honest and not a defect — but per D-09/D-10 ("render correctness is
established only when both automated detector and manual review pass"), **Phase 22 cannot be
declared complete** until the user completes the per-file checklist in `22-RENDER-REVIEW.md` and
reports no defect. The automated half (G1+G2+G3) is done; the human half is the gating item.

---

## 4. Per-Plan Disposition

| Plan | Claim | Verified? | Notes |
|------|-------|-----------|-------|
| 22-01 (Wave 0) | Detector + fixtures + footnote probe + baseline tag + PRE census (26) | ✅ | Selftest green; tag on faa73d0; PRE census 26 |
| 22-02 (pinn) | 2 tables→GFM, math normalized, footnotes, G2 exit 0 (7 ADJ) | ✅ work / ❌ record | Gate verified; **F1** (footnote claim false), **F3** (bad SHA) |
| 22-03 (ctl) | Math normalized, G2 exit 0 (10 ADJ), Task 1 no-op, HB-01 deferred | ✅ work / ❌ record | Gate verified; **F2** (Task 1 false), **F4** (11-entry allowlist) |
| 22-04 (Wave 2) | POST census 26, diff 0-lost/0-changed, handoff produced | ✅ | All 4 sources agree on 26; handoff 26 rows; commits `e7204d2`,`99b15f3` exist |
| 22-05 (Wave 3) | Full suite green, G3 audit, VER-05 ledger, G4 backstop pending | ✅ | Gates re-verified; ledger addendum present; G4 honestly pending (**F7**) |

---

## 5. Recommendations (before phase close)

1. **Correct F1** — rewrite the 22-02 footnote description to "converted `[^n]`→`[n]` (Stage-0
   render-safe)"; add a corrective note flagging the stale `94d8e79` commit message. *(record
   integrity — do before FUT-01/FUT-05 consume these specs.)*
2. **Correct F2** — rewrite 22-03 Task 1 to reflect `5bfbd20`; add `5bfbd20` to its commit list.
3. **Fix F3** — replace `ac601e9` with `acb8aa8`; ensure byte-preservation hashes live in
   committed state.
4. **Resolve F4** — prune or annotate the 2 orphan allowlist entries.
5. **Refresh F5** — update STATE.md to "Phase 22 executed; pending G4 visual backstop."
6. **Clean F6** — commit/remove `22-02-transform.mjs`; commit the 22-03 summary edit.
7. **Complete F7** — user performs the manual `22-RENDER-REVIEW.md` checklist; only then mark
   Phase 22 complete in ROADMAP/STATE.

None of F1–F6 require re-doing engineering work — they are record/ hygiene corrections. F7 is the
only gating action that requires the human-in-the-loop step the contract demands.

---

## 6. Concurrency Note (surfaced, not a Phase-22 defect)

The target directory `review_of_execution/` was **empty at the start of this review**
(`total 0`, dir mtime Jun 8 19:21). During this session it gained **four** other execution-review
files (timestamps 14:18–14:24 today): `2026-06-09-phase-22-execution-verification-review.md`,
`2026-06-09-phase22-comprehensive-execution-review-142145.md`,
`2026-06-09-phase22-execution-review.md`, `2026-06-09-phase22-execution-verification.md`.
These appear to be produced by other agents running the same task concurrently. I did **not** read
or overwrite them (to keep this review independent), and I wrote to a uniquely timestamped filename
to avoid collision. You may want to reconcile/dedupe these parallel reports.

---

## 7. Evidence Appendix (fresh commands)

```
# Detector (all exit 0)
$ node tools/spec-render-check/detect.mjs --selftest
  sanity gate: PASS … SELFTEST PASS (G1)                                  EXIT 0
$ … detect.mjs pinn_architecture.md --adjudications 22-02-pinn-architecture.json
  -- totals: 0 DEFINITE, 0 REVIEW, 7 ADJUDICATED, 14 SUPPRESSED --        EXIT 0
$ … detect.mjs ctl_instruction.md --adjudications 22-03-ctl-instruction.json
  -- totals: 0 DEFINITE, 0 REVIEW, 10 ADJUDICATED, 5 SUPPRESSED --        EXIT 0
$ … detect.mjs sampling_method.md
  -- totals: 0 DEFINITE, 0 REVIEW, 0 ADJUDICATED, 1 SUPPRESSED --         EXIT 0

# Content preservation vs baseline tag faa73d0
$ git diff --quiet faa73d0 HEAD -- …/sampling_method.md   → UNCHANGED (0 hunks)
pinn hunks: 23   ctl hunks: 8                              (matches 22-05 G3)

# Footnotes
tag faa73d0 [^n]=37  →  live [^n]=0 / [n]=39 / heading "## References"
$ git show 94d8e79~1:…pinn_architecture.md | grep -c '[^n]'  → 37
$ git show 94d8e79:…pinn_architecture.md   | grep -c '[^n]'  → 0   (94d8e79 CONVERTED)

# Census / handoff
detect.mjs --census → ctl 13, pinn 13, sampling 0, union 26
22-COMMENT-HANDOFF.md numbered rows: 26

# Adjudication allowlists
22-02-pinn-architecture.json: 7 entries (7 cleared)
22-03-ctl-instruction.json:  11 entries (10 cleared; orphans: dE/E@356, cpu_times@358)

# Commit existence
ac601e9: MISSING        acb8aa8: EXISTS (real table commit)
5bfbd20: EXISTS (22-03 Task-1 edits the summary denies)
7fe572e,e7204d2,99b15f3,64345f9,7375fe6,faa73d0: EXIST

# Working tree
3 specs: CLEAN (verified == committed)
22-02-transform.mjs: UNTRACKED ; 22-03-SUMMARY.md: uncommitted edit (commit ref fill-in)

# Governance
GAP-22-01/02/03: RESOLVED-WITH-INSTRUCTION (22-GAPS.md + v1.4-GAPS.md)
FUT-05: registered in REQUIREMENTS.md (owns 22-COMMENT-HANDOFF.md)
16-ISSUE-LEDGER.md: Phase 22 addendum present (P22-R1/R2/R3 VERIFIED)
ROADMAP: "- [ ] Phase 22" (correctly NOT closed)
```

---

*Gatekeeper conclusion: APPROVE the engineering work; REJECT the phase record as-is pending the
F1–F4 corrections; HOLD phase closure pending the F7 manual visual review. The corpus renders
correctly under the automated detector; the documentation must be made to tell the truth about how
it got there before the phase is signed off.*
