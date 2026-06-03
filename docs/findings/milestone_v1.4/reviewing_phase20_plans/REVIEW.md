# Phase 20 Planning Artifacts — Document Review

**Reviewed:** 2026-06-03
**Review type:** ce-doc-review (interactive mode)
**Document type:** plan
**Reviewers:** ce-coherence-reviewer, ce-feasibility-reviewer

## Summary

Applied **2 fixes**. **1 proposed fix** needs confirmation. **1 FYI observation**.

## Applied Fixes

- **20-CONTEXT.md, 20-RESEARCH.md, 20-GAPS.md** — Disambiguated "D-02" references: Phase 20 decision D-02 (SIREN/omega0 contract) collided with issue-doc finding D-02 (I_norm naming). All references to the I_norm issue now read "the I_norm naming issue (issue-doc D-02)" to prevent implementer confusion. (coherence, anchor 100)
- **20-03-PLAN.md §Interfaces** — Split the D-04 citation to separately credit D-04 (M5 STOP-protocol adjudication) and D-05 (ARCH-04 separation from M5). Previously the ARCH-04 separation clause was incorrectly attributed to D-04, which only covers M5/I_3. (coherence, anchor 100)

## Proposed Fixes

### [P2] 20-04 has implicit dependency on 20-02 via shared `pinn_architecture.md` not declared
**Section:** 20-04-PLAN.md frontmatter and Architecture section
**Why:** 20-04 lists `pinn_architecture.md` in `files_modified` but only declares `depends_on: ["20-03"]`. 20-02 (Wave 2, `autonomous: true`) also edits `pinn_architecture.md`. If an executor runs autonomous Wave 2 plans in parallel — or in the wrong order — the editor touching `pinn_architecture.md` first will shift line numbers or cause a git merge conflict for the other. Both 20-02 and 20-04 are `autonomous: true` and Wave 2, making parallel dispatch a real possibility. The plan's Architecture prose explains the `ctl_instruction.md` dependency on 20-03 but is silent about `pinn_architecture.md` coordination with 20-01 and 20-02.
**Suggested fix:** In 20-04-PLAN.md frontmatter, change `depends_on` from `["20-03"]` to `["20-03", "20-02"]`. In the Architecture section, add: "This plan also touches `pinn_architecture.md` (input-normalization cross-reference); it runs in wave 2 after 20-02 to avoid concurrent edits on that file."
**Reviewer:** feasibility, confidence 75

## FYI Observations

### [P3] 20-01 and 20-03 both modify `16-ISSUE-LEDGER.md` in Wave 1 without inter-dependency
**Section:** 20-01-PLAN.md and 20-03-PLAN.md frontmatter
**Why:** Both Wave 1 plans touch `16-ISSUE-LEDGER.md` (different rows: B-01/B-10 vs M5) and declare `depends_on: []`. While 20-03 is `autonomous: false` (M5 EVID-05 adjudication requires human attention), making parallel autonomous dispatch impossible, the coordination requirement is unacknowledged. A human executing both plans in the same working tree needs to sequence git commits: commit 20-01's ledger change before starting 20-03's ledger edit, or risk merge conflicts. This is a minor operational note — the executor can serialize manually.
**Reviewer:** feasibility, confidence 50

## Residual Risks

1. **ROADMAP.md "unless" carve-out vs D-02 no-scheduler contract.** The ROADMAP.md Phase 20 entry (line 209) states the SIREN criterion as "no epochwise omega0 scheduler **unless a reparameterized runtime mechanism is specified**" — the word "unless" introduces a carve-out not reflected in the Phase 20 decision D-02 contract, which states no scheduler under any condition. A future reader could interpret the carve-out as permitting a different approach. (coherence)

2. **20-03 defer-with-blocker cascades to 20-04.** 20-04 depends on 20-03. If 20-03's M5 verdict is `defer-with-blocker`, the semantic dependency (M5 was supposed to define a Locked Convention) is unsatisfied even though 20-03 formally "completes." The plans do not specify whether `depends_on` means "must complete successfully" or "must complete in any status." (feasibility)

3. **Evidence packet creation risk.** All six evidence packets (B-01, B-10, M5, M8, M9, M10) are currently missing on disk. Phase 20 must create them from `_TEMPLATE.md` during execution. The residual risk is executor error during packet creation (e.g., filling EVID-05-required sections into non-EVID-05 findings), mitigated by the template's explicit section-level annotations. (feasibility)

4. **Line-number drift.** The `ctl_instruction.md` line references in 20-RESEARCH.md will shift when 20-03 edits the file. Each plan's threat model explicitly warns against using line numbers and instructs `rg`-based search. The remaining risk is that an executor ignores this warning and searches by stale line numbers. (feasibility)

5. **20-05 placeholder visibility.** ARCH-04 remains blocked by GAP-20-01 with a non-executable placeholder plan. Phase exit must account for ARCH-04 as blocked/deferred — the plan set cannot silently claim ARCH-04 closure. (coherence, from initial reading)

## Deferred Questions

1. **Dependency semantics for blocked plans:** If 20-03's M5 verdict is `defer-with-blocker` (no `ctl_instruction.md` edits committed), does 20-04 proceed or halt? Technically 20-03 completes with a deferred status and no file changes, so 20-04 could proceed safely. But the semantic dependency (20-03 was supposed to define a Locked Convention) is unsatisfied. The executor must interpret whether `depends_on` means "must complete successfully" or "must complete in any status." (feasibility)

## Coverage

| Reviewer | Findings | Route |
|----------|----------|-------|
| coherence | 2 | Both safe_auto/100 → applied silently |
| feasibility | 2 | 1 gated_auto/75 (proposed fix), 1 manual/50 (FYI) |

Dropped: 0
Chains: 0 root(s) with 0 dependents

---

## Applied Fix Details

### Fix 1: D-02 identifier disambiguation
**Files edited:** `20-CONTEXT.md:71`, `20-RESEARCH.md:173`, `20-GAPS.md:29,31,34,36`
**Before:** `D-02 / ARCH-04` or bare `D-02` used to refer to the I_norm naming issue
**After:** `the I_norm naming issue (issue-doc D-02) / ARCH-04` — distinguishes the issue-doc finding number from Phase 20 decision D-02 (SIREN/omega0)

### Fix 2: D-04 → D-05 citation split in 20-03 interfaces
**File edited:** `20-03-PLAN.md:69`
**Before:** Single line attributing both M5 adjudication rules AND ARCH-04 separation to D-04
**After:** Split into two lines — D-04 for M5 adjudication, D-05 for ARCH-04 separation

---

*Review complete*
