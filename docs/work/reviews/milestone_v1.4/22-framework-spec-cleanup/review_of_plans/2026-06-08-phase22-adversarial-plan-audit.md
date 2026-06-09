---
phase: 22
review_type: adversarial-plan-audit
status: consumed
superseded_by: docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/2026-06-09-phase22-review-closeout-matrix.md
reviewed_artifacts:
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-01-PLAN.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-02-PLAN.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-03-PLAN.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-04-PLAN.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-05-PLAN.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-CONTEXT.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-RESEARCH.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-VALIDATION.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-GAPS.md
  - .planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-DISCUSSION-LOG.md
reviewer: Claude (adversarial document reviewer)
date: 2026-06-08
closed_out: 2026-06-09
severity_summary:
  critical: 1
  high: 5
  medium: 7
  low: 6
overall_verdict: PLANS-NEED-AMENDMENTS
closeout_verdict: ALL-19-FINDINGS-RESOLVED
---

# Phase 22 Adversarial Plan Audit

**Scope:** Stress-test all 5 execution plans (22-01 through 22-05) and supporting artifacts for flawless autonomous execution.

**Dimensions evaluated:**
1. **Logical Integrity** — critical errors, procedural gaps, flawed assumptions
2. **Execution Clarity** — ambiguities, grey areas, hidden consequences
3. **Operational Resilience** — missing checkpoints, fragile steps, inadequate error handling

**Verdict: PLANS-NEED-AMENDMENTS.** The wave structure, governance alignment, and ROADMAP coverage are strong. One critical issue (missing baseline reference) and five high-severity issues (autonomous STOP resolution, fragile verify commands, semantic judgments, commit cadence, census timing) require targeted plan amendments before execution.

---

## Executive Summary

The 5-plan, 4-wave pipeline is architecturally sound. Wave ordering is correct, dependencies are properly sequenced, negative controls are well-defined, and the two resolved gaps (GAP-22-01, GAP-22-02) are cleanly integrated. The plans collectively cover all 7 ROADMAP success criteria.

The risks cluster around three themes:

| Theme | Root Cause | Plans Affected |
|-------|-----------|----------------|
| **Missing git baseline** | No plan creates the pre-WS-A reference that 22-04/22-05 need | 22-01 (should create), 22-04, 22-05 (consume) |
| **Autonomous semantic judgment** | STOP protocol + redundant-fallback removal require judgment an autonomous agent shouldn't make | 22-02, 22-03 |
| **Fragile verification plumbing** | grep-based verify commands and unspecified interface contracts | 22-01, 22-02, 22-03, 22-04 |

---

## Findings by Severity

### CRITICAL — Must Fix Before Execution

#### C-01: Missing pre-WS-A git baseline reference

**Plans affected:** 22-04 Task 1, 22-05 Task 1
**Dimension:** Logical Integrity

**What's wrong:**

22-04 Task 1 requires a pre-WS-A census snapshot and says:

> "check out the `v1.4-pre-phase-22` tag or the WS-A base commit into a temp worktree, or pipe `git show <ref>:<path>` into the census."

No plan creates this tag or defines "the WS-A base commit." There is no symbolic ref, no tag, no commit hash anywhere in the 5-plan set. 22-05 Task 1 also needs "the WS-A base" for the G3 content-preservation audit.

Without this reference:
- 22-04 cannot reconstruct the pre-WS-A census → G3 comment-preservation audit is undefined
- 22-05 cannot compute the WS-A diff → G3 content-preservation audit is undefined
- Both plans fail at their first task

**Why it matters:** The entire verification chain (G3) depends on a defined baseline that doesn't exist. This is a hard blocker.

**Remediation:** Add a step to 22-01 (end of Task 3 or as a new Task 4):

```
Before any WS-A edit: run `git tag v1.4-pre-phase-22` (or `git tag phase-22-ws-a-base`)
at the Wave-0 completion commit. Record the tag name in 22-CONTEXT.md
and reference it in plans 22-04 and 22-05.
```

Also update 22-04 and 22-05 to reference the specific tag name instead of the vague "v1.4-pre-phase-22 tag or the WS-A base commit."

---

### HIGH — Should Fix Before Execution

#### H-01: Census snapshot should be captured in Wave 0, not reconstructed in Wave 2

**Plans affected:** 22-01, 22-04
**Dimension:** Logical Integrity

**What's wrong:**

The detector's `--census` mode is built in 22-01 (Wave 0). At that point, the three framework specs are unmodified. The pre-WS-A census could be captured trivially: run `--census`, write output to `22-COMMENT-CENSUS-PRE.md`, commit it.

Instead, the current design defers the snapshot to 22-04 (Wave 2, after WS-A edits), forcing git archaeology to reconstruct the baseline. This adds:
- A dependency on C-01 (the tag must exist)
- Risk of mis-reconstruction (wrong commit, wrong file version)
- Unnecessary complexity for an operation that could be trivial

**Remediation:** Add to 22-01 Task 3 (or as a new task):

```
After the detector self-test passes and before any WS-A work:
run `node tools/spec-render-check/detect.mjs --census` against all 3 specs
(live files = pre-WS-A state at this point).
Write the output to 22-COMMENT-CENSUS-PRE.md with per-comment text hashes.
Commit as part of the Wave-0 artifact set.
```

Then simplify 22-04 Task 1 to run `--census` against the current live (post-WS-A) files and diff against the already-committed pre-snapshot.

#### H-02: Autonomous STOP-protocol resolution is operationally undefined

**Plans affected:** 22-02 Task 2, 22-03 Task 2
**Dimension:** Logical Integrity

**What's wrong:**

Both plans say: "SURFACE the finding to the orchestrator under the STOP protocol and HALT that specific conversion." But neither defines what "HALT that specific conversion" means for an autonomous executor:

- Does the agent skip that conversion and continue? (Implied by the acceptance criteria's "EXCEPT any region explicitly HALTED under STOP")
- Does the agent abort the entire plan? (Possible reading of "HALT")
- Does the agent revert the conversion attempt? (Not mentioned)

The plans are `autonomous: true` — there is no interactive orchestrator to surface findings to. The agent must decide what to do inline. Without an explicit operational definition, an executor could:
- Abort the entire plan on the first ambiguous transcription (too aggressive)
- Apply the conversion anyway and violate governance (too permissive)
- Skip and continue but leave no record of what was skipped (the detector will flag it)

**Remediation:** Add to 22-02 and 22-03 (in both Task 2 descriptions):

```
STOP operational procedure for autonomous execution:
1. Do NOT apply the conversion. Leave the original ASCII text in place.
2. Record the finding in the task output with: section anchor, original text,
   proposed LaTeX conversion, and the ambiguity reason.
3. Continue to the next conversion in the task.
4. After the task completes, the detector will report the unconverted region
   as a residual finding — this is EXPECTED. In the task's done/success note,
   list all STOP-halted regions so 22-05 can reconcile them in VER-05.
```

#### H-03: Fragile grep-based verify commands

**Plans affected:** 22-02 Task 1, 22-03 Task 1
**Dimension:** Execution Clarity

**What's wrong:**

22-02 Task 1 verify command:
```bash
node tools/spec-render-check/detect.mjs pinn_architecture.md 2>&1 | \
  grep -ivE '^#' | grep -ciE 'fenced div|multiline table|: Table|separator row' | \
  grep -qx 0 && echo "structural-survivors=0"
```

This pipes detector output through grep searching for specific strings (`fenced div`, `multiline table`, etc.). If the detector uses different wording:
- "Pandoc div" instead of "fenced div" → **missed**
- "grid table" instead of "multiline table" → **missed**
- "caption" instead of ": Table" → **missed**

In ALL cases, grep finds 0 matches, count is 0, and the verify step passes — **even though findings exist**. This is a silent false-negative in the verification pipeline.

The same pattern appears in 22-03 Task 1 verify.

**Remediation:** Replace grep-based verify with exit-code-based verify:

```bash
node tools/spec-render-check/detect.mjs pinn_architecture.md; echo "exit=$?"
# Assert exit=0 for zero findings, OR manually inspect output
# for expected STOP-halted regions per H-02 remediation.
```

The acceptance criteria (textual description of what should be true) remain as-is — they are correct. Only the automated verify command needs fixing.

#### H-04: Redundant-fallback removal requires autonomous semantic judgment

**Plans affected:** 22-03 Task 2
**Dimension:** Execution Clarity

**What's wrong:**

22-03 Task 2 says:

> "remove the duplicate plaintext/backtick fallback PER-INSTANCE ON CONFIRMATION (D-07 / D7). If you are not certain a fallback is purely redundant (vs carrying distinct meaning), SURFACE rather than delete."

This requires the autonomous agent to determine whether a plaintext version of a formula is "purely redundant" vs. "carrying distinct meaning." Examples where this is ambiguous:

- Author wrote both backtick `L_data + λ_p·L_phys` AND LaTeX `$L_{data} + \lambda_p \cdot L_{phys}$` — is the backtick "redundant" or intended for readers who read raw markdown?
- Formula appears in both a code block (pseudocode context) and in LaTeX (math context) — complementary, not redundant?

The STOP protocol exists to prevent exactly this kind of autonomous semantic judgment. The "per-instance confirmation" instruction gives the agent permission to delete content it judges redundant — which is autonomous semantic deletion.

**Remediation:** Change 22-03 Task 2 to:

```
SURFACE all redundant-fallback candidates as STOP findings; do NOT remove any
fallback autonomously. Record each candidate with: section anchor, fallback text,
LaTeX equivalent, and the reason it appears redundant. The user decides whether
each is redundant during manual review (G4) or as a batch decision before 22-05.
```

This is consistent with the governance principle: Phase 22 does presentation-only
repairs. Removing "redundant" prose is a semantic deletion, not a presentation fix.

#### H-05: No explicit commit cadence or rollback procedure in WS-A plans

**Plans affected:** 22-02, 22-03
**Dimension:** Operational Resilience

**What's wrong:**

The RESEARCH doc and CLAUDE.md specify "commit at logical task boundaries; specs under `pinn_instruction/` → one atomic commit at task end." But the actual plans don't include explicit commit instructions. An autonomous executor might:
- Accumulate all changes across both tasks and commit once (larger blast radius if something is wrong)
- Not commit at all (no recovery point)
- Commit after every individual conversion (excessive granularity)

More critically, if a conversion batch introduces a regression (new detector finding), the plan says "revert any region to IN_PROGRESS in the ledger" but doesn't say how to revert the FILE. Options:
- `git checkout -- <file>` (loses ALL changes in that file)
- Manual undo of the last edit (hard to automate)
- Edit to fix the new finding (what the plan implies but doesn't state)

**Remediation:** Add to 22-02 and 22-03 (after each task's action section):

```
Commit protocol: After each task's acceptance criteria pass, stage ONLY the
modified spec file and commit with message:
  fix(22): <description of what was repaired> in <file>
Use scripts/agent-commit per CLAUDE.md git commit protocol.

Rollback procedure: If the detector reports a NEW finding after a conversion
batch that was not present before the batch:
1. Undo the last edit (reverse the specific Edit operation).
2. Re-run the detector to confirm the new finding is gone.
3. Record the regression in the task output.
4. Surface the problematic conversion as a STOP finding if the regression
   recurs on retry.
```

---

### MEDIUM — Should Fix Before or During Execution

#### M-01: Footnote probe requires Cursor visual inspection in an autonomous task

**Plans affected:** 22-01 Task 3
**Dimension:** Execution Clarity

22-01 Task 3 says to "ALSO record how the actual Cursor/VS Code Markdown Preview renders [^n]." But Tasks 2-3 are `type: auto` (no human checkpoint). An autonomous agent cannot open Cursor and visually inspect rendering.

The footnote probe result is critical — it determines whether 37 `[^n]` refs are defects. If the agent can't determine Cursor's rendering from the engine alone, it has no defined fallback.

**Remediation:** Add to 22-01 Task 3:

```
If the engine-only footnote test is unambiguous (markdown-it clearly renders or
clearly doesn't render the footnote), record the result. If ambiguous, record
the result as "AMBIGUOUS — requires human G4 confirmation" in 22-STAGE0-FOOTNOTE-
PROBE.md and proceed assuming footnotes are UNSUPPORTED (conservative: treats
them as survivor defects that WS-A will repair; if they actually work, G4 manual
review in 22-05 will catch the false positive).
```

#### M-02: Census text-hash requirement absent from detector spec

**Plans affected:** 22-01 Task 2, 22-04 Task 1
**Dimension:** Execution Clarity

22-04 requires "per-comment text hashes" for the before/after diff, but 22-01's detector spec only describes census output as `{form, file, section-or-anchor, matched-snippet, verbatim-text}` — no hash field.

**Remediation:** Add to 22-01 Task 2 census output spec: "emit `{form, file, section/anchor, matched-snippet, verbatim-text, text-hash}` where `text-hash = SHA-256(verbatim-text)` for deterministic comparison."

#### M-03: Equivalence-verification boundary is inherently ambiguous

**Plans affected:** 22-02 Task 2, 22-03 Task 2
**Dimension:** Execution Clarity

The boundary between "unambiguous conversion" and "ambiguous (STOP)" is itself a judgment. `L_total` → `$L_{total}$` is clear; `epsilon_H = 1e-4 * S_H` → `$\epsilon_H = 10^{-4} \cdot S_H$` involves stylistic choices (`*` → `\cdot`, `1e-4` → `10^{-4}`).

**Assessment:** Inherent limitation of the problem space. The plans already flag known-hard cases and the STOP protocol + G4 manual review provide safety nets. No plan amendment needed — but the orchestrator should expect STOP findings during WS-A execution and have a resolution workflow ready.

#### M-04: Missing .gitignore verification for node_modules

**Plans affected:** 22-01 Task 1
**Dimension:** Operational Resilience

22-01 claims "node_modules/ is git-ignored by the repo-root .gitignore (line 238)" but doesn't verify. If the pattern doesn't match `tools/spec-render-check/node_modules/`, the agent could commit node_modules.

**Remediation:** Add to 22-01 Task 1 (after install):

```
Verify: git check-ignore tools/spec-render-check/node_modules/
Must output the path. If not, add node_modules/ to .gitignore
(or the more specific tools/spec-render-check/node_modules/).
```

#### M-05: VER-05 ledger format unspecified

**Plans affected:** All plans that reference VER-05
**Dimension:** Operational Resilience

Every plan says "append finding-status transitions to 16-ISSUE-LEDGER.md" but none specify the format for Phase-22 entries.

**Remediation:** Add a format template to 22-01 verification section:

```
Phase-22 ledger entry format:
| P22-<file>-<N> | <region/section> | <D-layer> | <status> | <details> |
Status lifecycle: PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED (or DEFERRED)
```

#### M-06: ROADMAP not updated with plan count

**Plans affected:** ROADMAP.md
**Dimension:** Operational Resilience

ROADMAP Phase 22 still shows "**Plans:** 0 plans" with TBD placeholder. The 5 plans exist but aren't registered. `gsd-verify` may see "0 plans" and skip plan-level verification.

**Remediation:** Update ROADMAP Phase 22 Plans section:

```
Plans:
- [ ] 22-01: Wave 0 — Build render detector + footnote probe
- [ ] 22-02: Wave 1 — Repair pinn_architecture.md (G2)
- [ ] 22-03: Wave 1 — Repair ctl_instruction.md (G2)
- [ ] 22-04: Wave 2 — Author-comment census + FUT-05 handoff
- [ ] 22-05: Wave 3 — Final validation (G1–G4) + VER-05 reconciliation
```

#### M-07: Detector exit code conflicts with STOP-halted regions

**Plans affected:** 22-02, 22-03
**Dimension:** Operational Resilience

Plans say "detector exits 0 (G2), EXCEPT any region explicitly HALTED under STOP." But the detector has no STOP concept — it will exit non-zero if unconverted ASCII math remains.

This means: if any STOP findings exist, the verify commands WILL fail (detector exits non-zero), even though the plan considers this acceptable. The executor has no way to distinguish "legitimate STOP-halted findings" from "actual regression findings" in the exit code.

**Remediation:** Change acceptance criteria in 22-02/22-03 to:

```
`node tools/spec-render-check/detect.mjs <file>` exits 0, OR all residual
findings correspond exclusively to STOP-halted regions listed in the task output.
If the exit code is non-zero, the executor must manually verify that every
finding maps to a known STOP-halted region.
```

---

### LOW — Minor Improvements

#### L-01: CWD assumption not stated
All detector commands assume CWD = repo root. Add a note to 22-01: "All `node` commands are run from the repository root directory."

#### L-02: `min_lines: 200` for detect.mjs could encourage padding
Consider removing the code-size estimate or changing to a quality gate description ("the detector must implement all 6 layers + census + sanity gate + CLI flags").

#### L-03: Regression fixtures may need updating if detector changes
No plan covers fixture maintenance if the detector is updated during WS-A. Low risk — the detector should be stable after Wave 0.

#### L-04: Design doc section references could become stale
Plans reference `§5.1`, `§5.3` etc. from the design doc. If the design doc is edited, these break. Low risk — the design doc should be frozen for Phase 22.

#### L-05: VALIDATION.md still in draft state
Frontmatter says `status: draft` and `nyquist_compliant: false`. Plans reference it as authoritative context. Consider finalizing it before execution.

#### L-06: 22-04 artifacts section lists files that Task 1 creates
`22-COMMENT-CENSUS-PRE.md` appears in both the artifacts list and Task 1's output. Internally consistent but could confuse an executor reading top-down.

---

## Positive Observations

The following areas demonstrate strong plan quality:

1. **Gap resolution is exemplary.** GAP-22-01 and GAP-22-02 are both RESOLVED-WITH-INSTRUCTION with detailed resolution notes, user decisions recorded verbatim, and downstream consequences traced. This is exactly how the STOP protocol should work.

2. **Wave ordering is correct.** Wave 0 (detector) → Wave 1 (parallel repairs, different files) → Wave 2 (census/handoff) → Wave 3 (validation). Dependencies are properly declared. 22-02 and 22-03 can safely run in parallel.

3. **Threat model is consistent.** STRIDE analysis is properly inherited across plans. T-22-01 is tracked from creation (22-01) through consumption (22-02 through 22-05). No surface is left unexamined.

4. **Negative controls are well-chosen.** SI-PINN-002 meta-doc (must not be flagged as defect) and `sampling_method.md` (must stay 0-findings including not flagging its definition-list `:   ` lines) are specific, testable, and address real false-positive risks identified during design.

5. **ROADMAP success-criteria coverage is complete.** All 7 SCs map to specific plans: SC1 → 22-01, SC2 → 22-02/03, SC3 → 22-05, SC4 → 22-02/03, SC5 → 22-05, SC6 → 22-04, SC7 → all plans.

6. **Governance alignment is thorough.** The STOP protocol, no-live-code directive, presentation-only constraints, commit protocol requirements, and FUT-05 deferral boundary are consistently enforced across all 5 plans.

---

## Recommended Amendment Priority

| Priority | Finding | Effort | Impact |
|----------|---------|--------|--------|
| 1 | C-01: Create pre-WS-A git tag in 22-01 | Add 3 lines to 22-01 Task 3 | Unblocks 22-04, 22-05 |
| 2 | H-01: Move census snapshot to Wave 0 | Add task to 22-01, simplify 22-04 | Eliminates git archaeology risk |
| 3 | H-02: Define autonomous STOP procedure | Add paragraph to 22-02, 22-03 | Prevents plan abortion or governance violation |
| 4 | H-03: Fix fragile grep verify commands | Replace verify commands in 22-02, 22-03 | Prevents silent verification bypass |
| 5 | H-04: Remove autonomous fallback deletion | Change 22-03 Task 2 instruction | Prevents autonomous semantic deletion |
| 6 | H-05: Add commit cadence + rollback | Add paragraphs to 22-02, 22-03 | Enables clean recovery from regressions |
| 7 | M-01..M-07 | Minor additions across plans | Improves robustness |

**Estimated amendment effort:** ~30 minutes of targeted edits to the plan files. All amendments are additive (no restructuring needed).

---

## Conclusion

The Phase 22 plan set is well-architected with a clear wave structure, proper dependency sequencing, thorough governance, and complete ROADMAP coverage. The issues identified are concentrated in two areas: (1) the missing git baseline reference that underpins the entire verification chain, and (2) the boundary between autonomous and human-judgment work in the STOP-protocol and redundant-fallback handling. Both are straightforward to fix with targeted amendments to the existing plan text.

The plans are **ready for execution after the 6 high-priority amendments are applied.** The medium and low findings can be addressed during execution if needed.

---

*Reviewed by: Claude adversarial document reviewer*
*Date: 2026-06-08*
*Review type: Pre-execution adversarial audit for autonomous-agent consumption*
