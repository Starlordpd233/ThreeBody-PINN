---
phase: 35
reviewers: [agy, codex, opencode, cursor, claude-glm]
rerun_reviewers: [opencode]
reviewed_at: 2026-06-27T15:21:26Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260627T-xai-reasoning-35
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 35

## agy Review


# Phase 35 Plan Review

### 1. Summary
The Phase 35 plans are well-architected and properly sequenced across three waves. They successfully create the required evidence packets (35-01), inject the resulting loss component math (35-02) and assembly instructions (35-03) into their respective canonical specs, and perform a robust verification/ledger-closure pass (35-04). The plans strictly enforce the division of labor between component formulas and training assembly.

### 2. Strengths
*   **Dependency Ordering**: Excellent use of the wave architecture. Evidence creation (Wave 1) cleanly blocks spec edits (Wave 2), which in turn block verification and ledger closure (Wave 3).
*   **Canonical Boundary Enforced**: `pinn_architecture.md` is strictly limited to component math, while `ctl_instruction.md` is limited to assembly. The plans explicitly forbid duplicating formulas between them.
*   **Scope Containment**: 35-04 Task 3 utilizes a robust `git diff --name-only` guard to ensure live `pinn/` code, frozen specs, and read-only resolution documents are strictly untouched.
*   **Negative Invariants**: The plans extensively check for the absence of stale or uncommissioned mechanics (e.g., automatic dominance control, dense-residual ALM). 

### 3. Concerns
*   **HIGH - File Truncation Risk**: The automated `<verify>` scripts in 35-01, 35-02, 35-03, and 35-04 check for the *presence* of required tokens and the *absence* of forbidden tokens, but do not assert that original surrounding content is preserved. An AI could accidentally truncate `32-ISSUE-LEDGER.md` or the framework specs to just the newly written lines, and the automated checks would still pass.
*   **MEDIUM - Fragile Negative Checks**: The negative string matching in 35-02 and 35-03 is rigid. For example, `assert 'lambda_E = 1000' not in t` can be bypassed if the agent writes `lambda_E=1000` (without spaces). 
*   **LOW - GAP-32-01 Verification**: In 35-04 Task 1, the verification script only asserts that the string `'GAP-32-01'` is present in `35-VERIFICATION.md`. It does not actively read `32-GAPS.md` or `v1.6-GAPS.md` to programmatically confirm that the dual-register states match `RESOLVED-WITH-INSTRUCTION` and `Option A`, relying entirely on the agent's textual output.

### 4. Suggestions
*   **Add File Size Assertions**: Inject a simple line-count or file-size assertion into the verify scripts modifying large documents (e.g., `assert len(t.splitlines()) > 100` for the framework specs and ledger) to protect against accidental truncation.
*   **Use Flexible Regex for Negative Checks**: Update the strict string checks to handle whitespace variations (e.g., use `re.search(r'lambda_E\s*=\s*1000', text)` instead of exact string matching).
*   **Active GAP Validation**: Update the verify script in 35-04 Task 1 to actually read the gap registers and assert the required state, rather than just checking the verification artifact.

### 5. Overall Risk
**MEDIUM** (The flow and logic are solid, but the automated verification scripts lack safeguards against content truncation—a common AI editing failure mode).

---

## codex Review


## Summary

All four Phase 35 plan files were readable. The plan sequence is coherent and likely achieves the phase goal: evidence packets first, parallel spec edits second, verification and ledger closure last. Main residual risk is that some validation gates are weaker than the governance risk profile warrants.

## Strengths

- Clear dependency order: `35-01` precedes spec edits; `35-02` and `35-03` can run in parallel; `35-04` closes only after both.
- Strong scope boundary around specwork-only edits, with explicit bans on live `pinn/` code and frozen/read-only framework files.
- Good source-precedence handling: plans repeatedly guard against stale roadmap/requirements language.
- The canonical-home split between `pinn_architecture.md` and `ctl_instruction.md` is explicit and verified later.

## Concerns tagged HIGH / MEDIUM / LOW

- **MEDIUM:** Final changed-file validation is incomplete. [35-04-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/35-loss-energy-weight-contracts/35-04-PLAN.md:199) says `git diff --check` covers Phase 35 changed files, but the automated command at [line 206](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/35-loss-energy-weight-contracts/35-04-PLAN.md:206) omits evidence packets and `35-0N-SUMMARY.md` files, despite those being Phase outputs.

- **MEDIUM:** Several grounding checks are token-presence checks. [35-01-PLAN.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/35-loss-energy-weight-contracts/35-01-PLAN.md:161) requires line-range citations and STOP-gap discipline, but its automated checks mainly assert keywords. [35-VALIDATION.md](<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/35-loss-energy-weight-contracts/35-VALIDATION.md:23) also labels a token-existence check as the “Full suite command.”

- **LOW:** Plan metadata omits summary outputs from `files_modified`, while each plan creates a `35-0N-SUMMARY.md`. This may understate owned paths for execution, review, or commit hygiene.

## Suggestions

- Expand final `git diff --check` to include all Phase 35 outputs: evidence packets, summaries, verification, ledger, and both framework specs.
- Strengthen evidence-packet validators to assert required source paths, line-range citation patterns, verdict/status fields, and STOP-gap/milestone-gap handling.
- Either upgrade `35-VALIDATION.md`’s “Full suite command” to match the stronger negative checks in `35-04`, or rename it as a smoke check.
- Add a final allowed-path diff guard that compares actual changed files against the declared Phase 35 write set.

## Overall Risk (LOW/MEDIUM/HIGH)

**MEDIUM**. The plan architecture is sound, but validation precision should be tightened before execution closes the phase.

---

## opencode Review

**1. Summary**

Phase 35 plans correctly implement packet-before-edit discipline, canonical-home split (`pinn_architecture.md` for component math, `ctl_instruction.md` for methodology/assembly), STOP protocol, and ledger lifecycle for LOSS-01–04. Four evidence packets + ledger updates precede any spec edits; verification uses heavy structural/token/negative/protected-path checks. No live `pinn/` grounding or scope creep.

**2. Strengths**

- Rigorous wave/dependency ordering and `depends_on` declarations prevent edit-before-packet violations.
- Comprehensive acceptance criteria tied to exact tokens (`AC-LOSS-0[1-4]`, `modified`/`rejected`/`defer`, `delta_E = 1.0`, negative constructs) mirrored in automated `python -c` + `rg` verifiers.
- Explicit negative checks for every D-35-12 prohibition (cap table, `lambda_E=1000`, per-stage delta table, numeric clip, default dense-residual ALM, windowed Option C).
- Protected-path guards, `git diff --check`, and dual-register GAP-32-01 confirmation in final wave.
- Clear threat models and edge-coverage table (20/20) in 35-SPEC.md.

**3. Concerns**

- **MEDIUM**: Cross-phase mutation of `32-ISSUE-LEDGER.md` (and conditional `35-GAPS.md`/`v1.6-GAPS.md`) creates tight coupling; ledger-closure timing in 35-04 depends on prior waves succeeding without explicit rollback path if verification fails late.
- **LOW**: Token-based verification could theoretically be satisfied by misplaced comments; relies on human review of callout context.
- **LOW**: No explicit test of bidirectional stable-anchor cross-references beyond string presence.

**4. Suggestions**

Add one deterministic verification command in 35-04 that extracts and asserts exact blockquote callout structure (e.g. via `rg -A5 -B5 "AC-LOSS"`). Consider marking ledger rows `FIX_APPLIED` immediately after 35-02/03 before final verification wave.

**5. Overall Risk**

**LOW**

Plans achieve the phase goal with strong governance alignment. No missing critical edges, no destructive risk, no scope creep.

---

## cursor Review


_cursor failed: returned empty output, failed, or timed out._

Diagnostics:
- reviewer=cursor
- exit_code=1
- elapsed_seconds=19
- timeout_seconds=360
- watchdog=not_triggered
- command=cursor-agent -p --mode ask --trust --output-format text --model gpt-5.5-extra-high Read\ the\ file\ at\ /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260627T142131Z-45158/xreview-prompt-35.md\ in\ full\ and\ carry\ out\ the\ review\ request\ it\ contains.\ Output\ only\ the\ resulting\ markdown\ review.\ Do\ not\ edit\ any\ files. 
- stdout_bytes=0
- stderr_bytes=264

Artifacts:
- stdout: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260627T142131Z-45158/xreview-cursor-35.md
- stderr: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260627T142131Z-45158/xreview-cursor-35.err
- metadata: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260627T142131Z-45158/xreview-cursor-35.meta

Stderr excerpt:
```
ActionRequiredError: You've hit your usage limit You've saved $46 on API model usage this month with Pro Student. Switch to a different model or set a Spend Limit to continue with this model. Your usage limits will reset when your monthly cycle ends on 7/12/2026.

```

---

## claude-glm Review


I've read all four plans, the SPEC, and the CONTEXT. That's sufficient to evaluate intent, grounding, dependency ordering, scope, and verification rigor without loading the larger PROJECT/ROADMAP/REQUIREMENTS files (the CONTEXT already quotes the relevant SCOPE-12/13/14 constraints, and the dispatcher advises against loading everything by default). No files were edited.

---

# Phase 35 Plan Review

## 1. Summary

Phase 35 is v1.6 **specwork-only**: transcribe four settled loss contracts into `ctl_instruction.md` and `pinn_architecture.md` *by verdict status*, then close the Phase 32 ledger rows. The four contracts: **LOSS-01/NS-18+NS-12** (modified), **LOSS-02/M15** (rejected as replacement), **LOSS-03/NS-13** (defer), **LOSS-04/D-04** (RESOLVED-WITH-INSTRUCTION, Option A, resolving GAP-32-01).

Four plans, three waves: **35-01** authors one evidence packet per finding + advances ledger rows to `IN_PROGRESS`; **35-02** tags `pinn_architecture.md` (component math); **35-03** tags `ctl_instruction.md` (assembly); **35-04** verifies and closes rows to `VERIFIED`. No code, no destructive ops, STOP protocol explicitly armed.

## 2. Strengths

- **Grounding discipline is strong and consistent with v1.6 governance.** Packet-before-edit (D-35-09), explicit source precedence over the *stale* ROADMAP/REQUIREMENTS phrasing, live `pinn/` excluded as evidence, frozen specs fenced off.
- **Scope boundary is tight and actively enforced.** Only the two SCOPE-13 specs are edited; a protected-path `git diff` guard (35-04 T3) verifies `sampling_method.md`, read-only revision reports, the resolution doc, and `pinn/` are untouched.
- **The most dangerous fabrications are guarded by strict absence checks** — the cap table, `lambda_E = 1000`, a per-stage Huber table, and a numeric causal clip bound are all exact-string/regex "must not be present" assertions (no soft absolution).
- **Clean traceability.** Every requirement maps to plans → tasks → AC IDs → prohibitions, with a source-audit table per plan; STOP escalation is explicit and conditional (`35-GAPS.md` only if a real gap surfaces).

## 3. Concerns

### HIGH
None clearly reach HIGH. The worst numeric fabrications are caught by strict absence checks, and there is no path to data loss or scope breach.

### MEDIUM

- **M1. No automated no-duplication verifier — D-35-05 is unmet.** The CONTEXT explicitly demands *"a verifier that proves no duplication — a bidirectional arrow alone does not stop drift."* Yet every plan enforces the canonical-home split only through manual "review the new text" actions plus presence/absence *token* checks. No deterministic check compares the two files for duplicated normative body text. This is the phase's own flagged HIGH spec-drift risk; it should not rest on human judgment alone. (Closest item to HIGH.)

- **M2. Prohibition-check absolution logic is weakly discriminative.** The shared `ok(i)` helper (35-02/03/04 verify blocks) absolves a forbidden-pattern match if any of ` not `, ` no `, ` off `, `defer`, `reject` appears within ±2 lines. Generic negations are common enough that a construct introduced *as default* could be absolved by an unrelated nearby "not". The strictly-numeric prohibitions (cap table, `lambda_E=1000`, Huber table, clip bound) bypass `ok()` and are safe; the regex-guarded ones (Option-C/windowed, automatic dominance, dense-residual-as-default) rely on `ok()` and are the soft spot.

- **M3. Parallel wave-2 edits with bidirectional section-heading cross-references and no resolution check.** 35-02 and 35-03 are both wave 2, edit different files, and each must point to the other by "stable section heading + AC ID." If executed in parallel, a cross-reference can target a heading the sibling is still creating or has renamed. No task asserts that referenced headings/anchors actually exist in the target file.

### LOW

- **L1. `FIX_APPLIED` is never asserted.** D-35-10 specifies `IN_PROGRESS → FIX_APPLIED → VERIFIED`, but no plan sets or checks the row status at `FIX_APPLIED`; it survives only as a transition-log entry. Acceptable as transient, but the lifecycle is not verifiably traversed.
- **L2. Ledger-row checks assume a single-line, same-row token layout.** Task 3 (35-01) and 35-04 require status + packet path + AC ID + "Option A" all on the exact table-row line. If `32-ISSUE-LEDGER.md` stores any of these in a separate transition-log block, the check could fail (safe-fail) or pass spuriously. Executor reads the ledger first, so impact is low.
- **L3. Protected-path guard uses `git diff` (working-tree vs index).** A frozen file modified *and staged* before 35-04 would not appear in unstaged `git diff`. The agent-commit explicit-staging protocol makes this unlikely, but `git diff HEAD` would be stricter.
- **L4. Packet acceptance hard-codes resolution-doc finding IDs** (`DGR-09`, `GAP-14`, `NS18-01..04`, etc.) — brittle coupling to the doc's exact ID formatting. If the doc's IDs differ, the executor is forced between STOP and token-forcing. CONTEXT indicates the IDs are correct, so low risk.

## 4. Suggestions

1. **Add a deterministic no-duplication check (M1):** pick a sentinel normative formula (e.g. the causal-weight `w_n = exp(...)` body or the energy-Huber body) and assert it appears in exactly one of the two specs.
2. **Tighten `ok(i)` (M2):** restrict absolution tokens to the specific verdict markers actually used (`deferred`, `rejected`, `not part of the default`, `superseded`) and drop generic ` not `/` no `/` off ` — or require the absolution token on the *same* line as the match.
3. **Resolve the wave-2 hazard (M3):** either serialize 35-02 → 35-03, or add a post-edit check that every cross-referenced sibling section heading / AC anchor actually exists in the target file.
4. **Use `git diff HEAD` in the protected-path guard (L3)** to catch staged as well as unstaged modifications.

## 5. Overall Risk: **MEDIUM**

Intent, grounding, and scope are sound — the phase will almost certainly produce faithful edits with no scope creep or data-integrity exposure. The residual risk is **verification rigor, not design correctness**: the phase's two highest-priority guardrails (no-duplication and prohibition enforcement) lean on manual review and weakly-discriminative regex, and parallel wave-2 bidirectional cross-references have no resolution check. None of these is likely to cause loss or breach, but each could let a small spec inconsistency ship uncaught. All four suggested fixes are cheap and local to the verify blocks.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### agy
- status: preserved from existing REVIEWS.md

### codex
- status: preserved from existing REVIEWS.md

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=29
- timeout_seconds=360
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=2024
- stderr_bytes=598

### cursor
- status: preserved from existing REVIEWS.md

### claude-glm
- status: preserved from existing REVIEWS.md
