---
phase: 22
reviewers: [gemini, codex]
failed_reviewers:
  - reviewer: claude-alt
    reason: "401 authentication failure — external claude CLI requires interactive auth not available in headless /gsd-plan-phase context"
reviewed_at: 2026-06-08
plans_reviewed:
  - 22-01-PLAN.md
  - 22-02-PLAN.md
  - 22-03-PLAN.md
  - 22-04-PLAN.md
  - 22-05-PLAN.md
---

# Phase 22 — Cross-AI Plan Review

**Reviewers invoked:** gemini ✓, codex ✓, claude-alt ✗ (auth failure)
**Plans reviewed:** 22-01 (detector/Wave 0), 22-02 (ctl_instruction.md WS-A), 22-03 (pinn_architecture.md WS-A), 22-04 (WS-B census+preservation), 22-05 (final validation + VER-05 reconciliation)

---

## Convergent Findings (both reviewers flagged)

### C1 — Stage-0 footnote probe + detector D4 gate conflict [HIGH]

Both reviewers independently identified a tension between the **Stage-0 `[^n]` footnote probe** and the **detector D4 survivor scan**:

- **Codex [HIGH]:** "D4 unconditionally flags `[^n]`, while Plan 22-02 leaves footnotes unchanged if Cursor supports them. Because plain `markdown-it` treats footnotes as plugin syntax, the supported branch may never reach `--all` zero findings. The actual Cursor probe is also embedded in an automatic task rather than a blocking checkpoint. If unsupported, 'convert to a render-safe reference form' does not specify reference numbering, repeated references, anchors, backlinks, or definition preservation."
- **Gemini [LOW]:** "sampling_method.md is designated as the clean negative control. Since Phase 20.5 touched sampling_method.md, we must be absolutely certain that Phase 20.5 did not inadvertently introduce a defect."

**Orchestrator response:** The design doc §10 explicitly flagged this as a Stage-0 probe risk. The plans must be tightened so that: (1) the Stage-0 probe result **branches D4 behavior at runtime** (if Cursor renders `[^n]`, D4 suppresses that class; otherwise, it flags), and (2) the probe is a **blocking checkpoint** in Wave 0 before any WS-A repair runs, not an automatic task that can be silently skipped.

### C2 — WS-B preservation scope well-bounded in 22-04, but 22-03 has a deletion-on-confirmation contradiction

Both reviewers acknowledged WS-B is well-bounded, but codex found a specific contradiction:

- **Codex [HIGH]:** "Plan 22-03 is `autonomous: true` but permits deletion of redundant fallbacks and hard breaks 'per-instance on confirmation.' That confirmation is not represented by a human checkpoint."
- **Gemini [implicit]:** "22-04 rigidly enforces the WS-B reduction, explicitly banning any disposition or semantic classification, and strictly mapping out the 22-COMMENT-HANDOFF.md artifact."

**Orchestrator response:** 22-03's `autonomous: true` + "per-instance on confirmation" for deletion must be reconciled. Either: (a) downgrade 22-03 to `autonomous: false` and add a blocking human checkpoint for fallback/hard-break deletion, or (b) reclassify deletion as WS-A presentation-only (since the design doc §5.3 treats redundant-fallback removal as "once math renders, the plaintext/backtick duplicates the author flagged are removed per-instance on confirmation") and add an explicit human checkpoint in 22-03's task flow.

---

## Codex Review (full)

```markdown
## Summary

The plan set is **not execution-ready**. The broad phase decomposition is sound, but several HIGH-severity contradictions could make G2 impossible, violate the STOP protocol, or lose the pre-repair evidence needed for WS-B.

## Strengths

- Wave 0 is explicitly required before both WS-A repair plans.
- WS-B clearly preserves comments and defers adjudication to FUT-05.
- Automated G1–G3 and manual G4 gates are appropriately separated.
- The retired "28 `\authcomment`" count is not treated as canonical.
- Exact dependency pinning, a lockfile, negative controls, and plugin-load sanity checking are good foundations.
- No new `AC-*` names are introduced.

## Concerns

### HIGH — Footnote branches conflict with the detector

D4 unconditionally flags `[^n]`, while Plan 22-02 leaves footnotes unchanged if Cursor supports them. Because plain `markdown-it` treats footnotes as plugin syntax, the supported branch may never reach `--all` zero findings.

The actual Cursor probe is also embedded in an automatic task rather than a blocking checkpoint. If unsupported, "convert to a render-safe reference form" does not specify reference numbering, repeated references, anchors, backlinks, or definition preservation.

### HIGH — STOP-halted plans can incorrectly complete

Plans 22-02 and 22-03 allow "zero findings except STOP-halted regions" and then declare the task done. Governance requires the affected work to remain blocked until user resolution or explicit deferral.

Plan 22-05 likewise must not mark a finding `DEFERRED` merely because it has a written blocker; deferral requires recorded user instruction.

### HIGH — Autonomous deletion contradicts confirmation requirements

Plan 22-03 is `autonomous: true` but permits deletion of redundant fallbacks and hard breaks "per-instance on confirmation." That confirmation is not represented by a human checkpoint.

### HIGH — Pre-repair census evidence for WS-B

Plan 22-04 suggests piping `git show <ref>:<path>` into the census tool. If `detect.mjs --census` (built in 22-01) is not designed to read from `stdin`, this will fail. The alternative (temp worktree) is safer but introduces repository-state complexity.

## Suggestions

- Make the Stage-0 footnote probe a blocking Wave-0 checkpoint with explicit D4 branching logic.
- Reconcile 22-03 `autonomous: true` with "per-instance on confirmation" — either downgrade to `autonomous: false` or add a human checkpoint.
- Tighten STOP-halted completion: a task with STOP regions is NOT done; it's blocked.
- Specify the census stdin/worktree interface in 22-01 so 22-04's pre-repair snapshot is well-formed.

## Risk Assessment

**HIGH** — The plans are structurally sound but contain governance violations (STOP completion, autonomous deletion) and a detector-vs-plan conflict (footnote branches) that could block execution or produce incorrect results.
```

---

## Gemini Review (full)

```markdown
# Phase 22: Framework-Spec Cleanup — Plan Review

## Summary
The 5-plan suite provides a rigorous, highly-controlled approach to finalizing the framework specs for presentation. The dependency graph is structurally sound, pushing tooling and baseline probes to Wave 0, execution to Wave 1, census verification to Wave 2, and final integration checks to Wave 3.

## Strengths
- **Strict Dependency Ordering:** Wave 0 isolates the detector creation and Stage-0 probe. Wave 1 can then rely on a static, verified oracle. Wave 2 isolates the census diff, and Wave 3 enforces the final gates.
- **Npm Supply-Chain Threat Modeling:** The blocking human-verify checkpoint in `22-01` Task 1 effectively mitigates the risk of poisoned packages by forcing a registry verification before `--save-exact` installation.
- **Footnote Probe Contingency:** `22-01` explicitly tests the `[^n]` rendering capability of the target environment before `22-02` blindly replaces them. This prevents unnecessary structural changes if the renderer natively supports them.
- **Clear Scope Boundaries:** `22-04` rigidly enforces the WS-B reduction, explicitly banning any disposition or semantic classification, and strictly mapping out the `22-COMMENT-HANDOFF.md` artifact.

## Concerns

### 1. GFM Pipe Table Multiline Cell Limitations (22-02) [HIGH]
The plan states: "Where a multiline table cell spans multiple source lines, join into the single GFM cell that renders identically".
**Risk:** GFM pipe tables do not support block-level elements inside cells. If a Pandoc multiline table contains block math (`$$...$$`), multiple paragraphs, or lists, flattening it into a single line will break the parser or the math rendering.

### 2. Pre-WS-A Census Execution Input (22-04 & 22-01) [MEDIUM]
`22-04` Task 1 suggests piping `git show <ref>:<path>` into the census tool.
**Risk:** If `detect.mjs --census` (built in `22-01`) is not designed to read from `stdin`, this will fail. The alternative (temp worktree) is safer but introduces repository-state complexity.

### 3. "Clean" Spec Drift (22-01) [LOW]
`sampling_method.md` is designated as the clean negative control.
**Risk:** Since Phase 20.5 touched `sampling_method.md`, we must be absolutely certain that Phase 20.5 did not inadvertently introduce a defect.

### 4. Double-Wrap Sanity Gate Rigidity (22-01) [LOW]
The sanity gate checks `.default.default` for the `@vscode/markdown-it-katex` plugin.
**Risk:** If the package structure differs slightly based on the exact pinned version, the detector aborts. This is a "good" failure mode (failing safe), but might require manual intervention.

## Suggestions

- Clarify in 22-02 how block math in Pandoc multiline tables will be handled (extract to standalone `$$` blocks, or keep in tables if GFM supports it?).
- Specify the census tool's input interface (stdin vs file) in 22-01.
- Add a verification step in 22-01 to confirm `sampling_method.md` is still 0-findings after Phase 20.5.
- Document the double-wrap gate as a "known landmine" so the executor expects to potentially fix the import.

## Risk Assessment

**MEDIUM** — The plans are well-structured and respect the locked scope decisions. The main risks are in edge cases (block math in tables, stdin interface) and minor governance drift (clean-spec verification). These are addressable with targeted clarifications before execution.
```

---

## Orchestrator Next Steps

The reviews surfaced 4 actionable concerns. Before the plans are committed and sent to the checker, the orchestrator should:

1. **Fix the footnote probe (C1):** Tighten 22-01 so the Stage-0 probe is a **blocking Wave-0 checkpoint** (not an automatic task) and D4's behavior branches on the probe result at runtime.
2. **Fix 22-03 autonomous + deletion (C2):** Either downgrade 22-03 to `autonomous: false` or add an explicit human checkpoint for "per-instance on confirmation" deletion.
3. **Fix STOP-completion semantics (codex HIGH):** Tighten 22-02/22-03/22-05 so a task with STOP-halted regions is marked **blocked**, not done.
4. **Clarify census stdin interface (codex HIGH + gemini MEDIUM):** Specify in 22-01 that `detect.mjs --census` reads from a file path (not stdin), so 22-04's pre-repair snapshot is well-formed.
5. **Clarify GFM table math (gemini HIGH):** Specify in 22-02 how block math inside Pandoc multiline tables is handled (extract to standalone `$$` blocks, since GFM pipe tables don't support block-level elements).

These are targeted revisions, not a replan. The orchestrator should spawn the planner in **revision mode** with these 5 specific fixes, then re-run the checker.
