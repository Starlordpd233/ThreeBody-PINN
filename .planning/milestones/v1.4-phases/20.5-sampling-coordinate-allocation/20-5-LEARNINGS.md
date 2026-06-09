---
phase: 20.5
phase_name: "Sampling Coordinate Allocation"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 3
  lessons: 4
  patterns: 6
  surprises: 2
missing_artifacts:
  - "20-5-VERIFICATION.md"
  - "20-5-UAT.md"
---

# Phase 20.5 Learnings: Sampling Coordinate Allocation

## Decisions

### Locked "Option A" Conditional (δ_s, δ_v) Sobol Coordinate Allocation
The Sobol coordinate allocation convention was locked as "Option A" — the conditional `(δ_s, δ_v)` allocation where `d = 3 + δ_s + 3δ_v`. This convention matches the existing standard quasi-random dataset's generation parameters.

**Rationale:** The existing dataset was generated under this convention; locking it avoids a costly dataset rebuild while ensuring spec/code alignment.
**Source:** 20-5-SUMMARY.md, 20-5-PLAN.md

---

### No Dataset Regeneration Required
The phase concluded that no dataset rebuild was needed because the spec edits were made to match the existing data-generator behavior, not the other way around.

**Rationale:** The conditional `(δ_s, δ_v)` convention locked as Option A is the one the standard quasi-random dataset was generated under, so the spec now accurately describes the existing data.
**Source:** 20-5-SUMMARY.md

---

### Scoped Provenance Claim (Not Blanket Historical-Provenance Certification)
The data-alignment handoff (`20-5-DATA-ALIGNMENT.md`) deliberately scopes its provenance claim: it certifies alignment of the spec, the documented generator configuration, and the current sampler behavior — but explicitly does NOT certify that a specific script revision produced every stored data file.

**Rationale:** No in-repository manifest proves the exact script revision for every stored data file. Claiming blanket historical provenance would overstate what can be verified. The scoped claim is honest about this limitation while still resolving the coordinate-allocation mismatch.
**Source:** 20-5-PLAN.md, 20-5-SUMMARY.md

---

## Lessons

### Phase 18 Already Reconciled the Velocity-Momentum Discrepancy
Phase 20.5's Task 8 verified that the velocity-momentum sampling discrepancy (a potential sub-conflict) no longer existed because Phase 18's FRAME-03 had already reconciled the spec prose to the code's symmetric `v1 = v3 = -v2/2` split. No separate finding document was created.

**Context:** This avoided creating a stale open-finding document for a conflict that had already been resolved upstream.
**Source:** 20-5-PLAN.md, 20-5-SUMMARY.md

---

### CLAUDE.md and GEMINI.md Are Symlinks to AGENTS.md
The root agent instruction files `CLAUDE.md` and `GEMINI.md` are symlinks pointing to `AGENTS.md`, while `ANTIGRAVITY.md` is a separate regular file. Edits must target `AGENTS.md` and `ANTIGRAVITY.md` directly — editing `CLAUDE.md`/`GEMINI.md` separately would be incorrect.

**Context:** This symlink topology is critical for governance propagation tasks. Editing the symlink target rather than the symlinks avoids duplicate or inconsistent edits.
**Source:** 20-5-PLAN.md

---

### GSD Phase-Number Tooling Has a Phase 20/20.5 Resolution Hazard
The `find-phase 20` and `init.phase-op 20` tools can resolve to the Phase 20.5 directory instead of the Phase 20 directory. This hazard is recorded in `v1.4-GAPS.md`.

**Context:** All Phase 20.5 work must use explicit file paths, never phase-number tooling. This is a known structural issue with dot-decimal phase numbering in the GSD toolchain.
**Source:** 20-5-PLAN.md

---

### Pre-Existing Gap Registers Can Be Verified Rather Than Recreated
Phase 20.5's gap register (`20-5-GAPS.md`) with GAP-20-5-01/02/03 had already been created and resolved (`RESOLVED-WITH-INSTRUCTION`) on 2026-05-19, before the phase execution began. Task 4 verified the existing register rather than recreating it.

**Context:** Gap resolution can precede phase execution. The phase plan correctly identified these as "verify pre-existing" rather than "create new."
**Source:** 20-5-PLAN.md, 20-5-SUMMARY.md

---

## Patterns

### Three-Surface Disposable Verification Probe
A verification probe that checks three independent surfaces — (1) static spec text, (2) entrypoint AST parse of the generator code, (3) sampler runtime behavior including a synthetic position test — where each surface exits nonzero on missing source anchor, malformed configuration, or allocation mismatch.

**When to use:** When spec↔code alignment must be verified with defense in depth: static text alone is insufficient if the code's runtime behavior diverges from its source structure, and AST alone is insufficient if configuration overrides change behavior.
**Source:** 20-5-PLAN.md

---

### Mandatory Per-Commit Gate (8-Step)
A structured commit gate requiring: (1) empty pre-stage index check, (2) unstaged diff review, (3) explicit-path-only staging, (4) staged-list confirmation against expected file set, (5) cached-diff inspection plus whitespace check, (6) re-running task verification against staged content, (7) commit via `scripts/agent-commit` with `GIT_AGENT_ID`, (8) post-commit confirmation that index is drained and HEAD matches expected files.

**When to use:** When working in risk-elevated paths (`.planning/`, `pinn_instruction/`) where commits must contain exactly their declared files and no pre-existing user staging may be silently captured.
**Source:** 20-5-PLAN.md

---

### Chained Part-Completion Gates Between Plan Parts
Each plan part file ends with a completion gate that verifies its tasks, expected commits, required artifacts, and empty staged index. The next part's precondition requires the prior part's gate to have passed.

**When to use:** When a plan is split across multiple part files that must execute in strict order, and each part's output is a precondition for the next. Prevents partial-execution drift.
**Source:** 20-5-PLAN.md

---

### State-Aware Plan Authoring with Re-Grounding
Plans authored before prior phases complete must be re-grounded against live state after those phases execute. Phase 20.5's plan was made state-aware on 2026-06-06 after Phases 17–20 executed, with Task 5 Edit 5 FROM/TO re-grounded to the Phase 18 momentum wording.

**When to use:** When a plan spans phases that are not yet complete at authoring time, and downstream spec wording may shift due to upstream phase edits.
**Source:** 20-5-PLAN.md

---

### Plan-Files-Committed Precondition
All plan files must be committed and the working tree clean with respect to them before Task 0 begins. Execution must never start from an uncommitted or stale plan revision.

**When to use:** When plan files are authored separately from execution, to ensure the executed plan matches the reviewed/committed plan.
**Source:** 20-5-PLAN.md

---

### Symlink-Aware Governance Propagation
When propagating governance rules to root instruction files, first determine the symlink topology (`ls -l AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md`), then edit only the real files (`AGENTS.md`, `ANTIGRAVITY.md`), never the symlinks (`CLAUDE.md`, `GEMINI.md`).

**When to use:** When a project uses symlinks to share instruction content across agent-specific filenames (e.g., `CLAUDE.md` → `AGENTS.md` for Claude Code, `GEMINI.md` → `AGENTS.md` for Gemini).
**Source:** 20-5-PLAN.md

---

## Surprises

### Velocity-Momentum Discrepancy Already Resolved by Phase 18
Phase 20.5 was initially scoped with a potential sub-conflict around velocity-momentum sampling. However, Task 8 verified that Phase 18's FRAME-03 had already reconciled the spec prose to the code's symmetric velocity split (`v1 = v3 = -v2/2`), making the sub-conflict non-existent. No finding document was created.

**Impact:** Task 8 became verification-only rather than producing a new finding. The plan correctly adapted by verifying the reconciliation rather than duplicating work.
**Source:** 20-5-PLAN.md, 20-5-SUMMARY.md

---

### Gap Register Pre-Dated Phase Execution by Weeks
The three Phase 20.5 gaps (GAP-20-5-01/02/03) were created and resolved on 2026-05-19 — nearly three weeks before the phase execution began on 2026-06-07. Task 4 verified the existing resolved state rather than creating new gaps.

**Impact:** The phase execution benefited from prior gap analysis done during the research/planning stage. The gap register served as an input to execution rather than an output.
**Source:** 20-5-PLAN.md, 20-5-SUMMARY.md
