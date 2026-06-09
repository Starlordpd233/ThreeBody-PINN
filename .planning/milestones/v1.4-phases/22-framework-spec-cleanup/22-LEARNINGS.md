---
phase: 22
phase_name: "Framework Spec Cleanup"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 7
  lessons: 7
  patterns: 5
  surprises: 3
missing_artifacts:
  - "22-UAT.md"
---

# Phase 22 Learnings: Framework Spec Cleanup

## Decisions

### Footnotes Classified as `unsupported` in Cursor Markdown Preview
Cursor Markdown Preview renders `[^probe1]` and `[^n]:` footnote syntax as literal text, not as superscript links or footnote lists. All 37 footnote refs and 17 defs in `pinn_architecture.md` must be converted to render-safe bracket-number/reference-list form.

**Rationale:** Empirical probe (Stage-0 footnote probe) confirmed via user screenshot that the target renderer does not support standard Pandoc/GitHub footnote syntax.
**Source:** 22-01-SUMMARY.md

---

### G2 Gate Redefined as Tiered (0 DEFINITE + All REVIEW Adjudicated)
G2 was changed from "0 findings total" to "0 DEFINITE findings + every REVIEW finding is either adjudicated via allowlist or absent." This allows exit-0 when code identifiers are legitimately kept unconverted.

**Rationale:** Code identifiers (PyTorch parameter names, filenames) are mechanically inseparable from bare subscripts at the D5/D6 layer. The adjudication allowlist preserves detector recall while allowing honest exit-0 reporting.
**Source:** 22-02-SUMMARY.md

---

### D5 Detector Code-Span Scan NOT Narrowed Despite False Positives
Option B (narrowing D5's backtick-math oracle scan to reduce code-identifier false positives) was explicitly rejected.

**Rationale:** D5 is the detector's only code-span layer — it found the actual math conversions during execution. snake_case code identifiers vs. bare subscripts are mechanically inseparable, which is why these are REVIEW tier. Adjudication allowlists preserve recall without narrowing.
**Source:** 22-02-SUMMARY.md

---

### Author Comments Deferred to FUT-05, Inventory-Only in Phase 22
Phase 22 performs NO basis classification, NO adjudication, NO keep/remove/revise verdict, and NO deletion of author comments. Only an inventory (`22-COMMENT-HANDOFF.md`) is produced.

**Rationale:** GAP-22-01 was resolved with explicit user instruction to defer all author-comment adjudication to FUT-05.
**Source:** 22-04-SUMMARY.md

---

### Plan 22-05 Is the Sole VER-05 Ledger Reconciler for Phase 22
WS-A plans (22-02, 22-03) record per-plan summaries but do NOT directly write to the shared `16-ISSUE-LEDGER.md`. Plan 22-05 reconciles the shared ledger once, after Wave 1 and Wave 2 artifacts are stable.

**Rationale:** Prevents race conditions from multiple plans writing to a shared ledger file during parallel execution.
**Source:** 22-05-PLAN.md

---

### Redundant Fallback Surfacing via Task 3 Checkpoint (No Autonomous Deletion)
Redundant plaintext/backtick fallback candidates in `ctl_instruction.md` are surfaced for human/STOP disposition via a dedicated Task 3 checkpoint. None are deleted autonomously by the agent.

**Rationale:** Governance requirement — deletion of content that may be intentional author redundancy requires human disposition, not agent inference.
**Source:** 22-03-SUMMARY.md

---

### Adjudication Allowlists Stored as Per-Plan JSON Files
Code-identifier adjudications are recorded in JSON files under `tools/spec-render-check/adjudications/` (e.g., `22-02-pinn-architecture.json`, `22-03-ctl-instruction.json`), auto-loaded by `detect.mjs --all`.

**Rationale:** Deterministic, machine-verifiable, and composable — downstream plans load committed allowlists rather than re-adjudicating.
**Source:** 22-02-SUMMARY.md, 22-03-SUMMARY.md

---

## Lessons

### KaTeX Plugin ESM/CJS Interop Requires Defensive Resolution
The `@vscode/markdown-it-katex` plugin's export is double-wrapped; a naive `md.use(plugin)` silently fails to register, so KaTeX never runs and the detector either flags ALL valid math or passes a broken file.

**Context:** The sanity gate now checks `.default`, `.default.default`, and direct callable resolution before any layer runs. This was design test-fix #1 and the #1 pitfall.
**Source:** 22-01-PLAN.md

---

### Code Identifiers and Bare Subscripts Are Mechanically Inseparable at Detector Layer
snake_case code identifiers (e.g., `first_omega_0`, `elementwise_affine`) match the same patterns as bare mathematical subscripts. The detector cannot distinguish them mechanically.

**Context:** This is why D5/D6 findings involving code-like tokens are REVIEW tier (not DEFINITE), and why adjudication allowlists rather than detector narrowing is the correct resolution.
**Source:** 22-02-SUMMARY.md

---

### D5 Code-Identifier Pattern Recurses Predictably Across Specs
GAP-22-03's code-identifier pattern (7 PyTorch parameter names in `pinn_architecture.md`) recurred exactly as expected as 10 code identifiers in `ctl_instruction.md`. All adjudicated via the same `code-identifier-kept` verdict.

**Context:** Cross-referencing specs inherits the code-identifier findings from the referenced spec, plus its own parameter names.
**Source:** 22-03-SUMMARY.md

---

### Line Numbers Drift During Edits — Reports Must Use Anchor+Snippet
Every detector layer and the census re-derive positions against live file bytes at execution time. Reports use section/anchor + matched snippet, never hardcoded line numbers.

**Context:** Phase 22 involves multiple sequential edits to the same files. Line numbers shift with each edit.
**Source:** 22-01-PLAN.md

---

### Programmatic Table Conversion via Column Separator Detection Works for Pandoc Multiline Tables
Pandoc multiline tables (which have no GFM equivalent) were successfully converted using column separator detection and cell-boundary parsing, preserving all cell content byte-for-byte including footnote references.

**Context:** 2 tables in `pinn_architecture.md` (12×12 and 13×3) converted this way.
**Source:** 22-02-SUMMARY.md

---

### Author-Comment Preservation Is Provable via Stable Hash IDs
The census assigns each comment a stable `COMMENT_HASH` id that is reproducible across PRE and POST runs. Bijection matching by hash proves 0 lost, 0 semantically changed — even when surrounding prose was syntax-normalized.

**Context:** 26 comments tracked through WS-A; 3 carried D-05 wrapper repairs where surrounding prose changed but the comment clause itself was byte-identical.
**Source:** 22-04-SUMMARY.md

---

### Shared Ledger Writes Must Be Serialized Across Parallel Plans
Multiple plans executing in the same wave cannot safely write to a shared ledger file. The pattern is: per-plan summaries → single reconciler plan writes to shared ledger.

**Context:** Applied to `16-ISSUE-LEDGER.md` — WS-A plans (22-02, 22-03) record locally; 22-05 reconciles once.
**Source:** 22-05-PLAN.md

---

## Patterns

### Sanity Gate Before Detector Layers
Construct the rendering engine, register plugins, render a known-good inline AND block math expression, and assert correct output before any detection layer runs. Abort with exit 2 if the engine is broken.

**When to use:** Any time a rendering-based detection tool depends on a plugin chain that may silently fail to load (ESM/CJS interop, version mismatches).
**Source:** 22-01-PLAN.md, 22-01-SUMMARY.md

---

### D4 Survivor Scan via Complete-by-Construction
Render with the real engine, then scan the *rendered visible text* for control-markup that must never survive literally (`$$`, `\command`, `:::`, `[^n]`, `{.attr}`, Pandoc table rows, `: Table …` captions). This enumerates "markup that must never appear literally" rather than a fixed defect list — catching unknown-unknowns.

**When to use:** When validating that a Markdown→HTML conversion pipeline has fully consumed all non-standard syntax.
**Source:** 22-01-PLAN.md

---

### Tiered Detector with Adjudication Allowlists
Use a tiered severity model (DEFINITE / REVIEW / SUPPRESSED / ADJUDICATED). When the detector has known inseparable false positives (code identifiers vs. bare subscripts), keep detector recall at maximum and resolve via per-plan JSON allowlists that `--all` auto-loads.

**When to use:** When a static analysis detector has categories of findings that are mechanically indistinguishable but semantically different, and the false positives are predictable and enumerable.
**Source:** 22-02-SUMMARY.md, 22-05-PLAN.md

---

### Census-Based Content Preservation Verification
Take a PRE census (stable hash per tracked item) before edits, a POST census after edits, and diff by hash. Proves bijection: 0 lost, 0 semantically changed. Works for author comments, footnotes, any tracked structural element.

**When to use:** Any bulk-editing operation where content preservation is a correctness invariant — especially when surrounding syntax changes but specific clauses must remain byte-identical.
**Source:** 22-01-SUMMARY.md, 22-04-SUMMARY.md

---

### Wave-Structured Phase with Single-Reconciler Phase Gate
Split phase work into waves: Wave 0 (tool + baseline), Wave 1 (parallel per-file edits), Wave 2 (cross-cutting concerns), Wave 3 (phase gate: full suite re-run + ledger reconciliation + manual review). The final wave is the sole writer to shared state.

**When to use:** Multi-file spec cleanup or migration phases where parallel execution is needed but shared artifacts (ledgers, cross-file invariants) must be reconciled atomically.
**Source:** 22-05-PLAN.md

---

## Surprises

### `\text{xxx}` Inside an Author Comment Flagged as Math by D5
The detector's backtick-math oracle flagged `\text{xxx}` — a placeholder literal inside an Author Comment's verbatim text — as a REVIEW finding. It was adjudicated as `code-identifier-kept` (not math to render).

**Impact:** Demonstrates that even "obviously not math" tokens inside author-metadata contexts can trigger detector layers. The adjudication allowlist approach handles this gracefully without narrowing the detector.
**Source:** 22-02-SUMMARY.md

---

### Phase 22 Had 3 STOP Gaps, All Resolved Without Blocking the Phase
GAP-22-01 (author-comment adjudication scope), GAP-22-02 (redundant fallback deletion authority), GAP-22-03 (code-identifier vs. bare-subscript inseparability) were all surfaced and resolved with explicit user instruction — none blocked the phase because dependency-scoped blocking allowed independent work to continue.

**Impact:** Validates the dependency-scoped blocking model from the STOP protocol: gaps block only dependent work, not the entire phase.
**Source:** 22-05-SUMMARY.md

---

### G4 Visual Backstop Remains PENDING-USER-REVIEW After All Automated Gates Pass
Even with G1/G2/G3 all passing, the manual Cursor/VS Code render review (G4 visual backstop) could not be automated and remains PENDING-USER-REVIEW. A written checklist was produced in `22-RENDER-REVIEW.md` for the user.

**Impact:** The phase's automated verdict is conditional — it passes on the automated proxy but explicitly requires the human visual backstop to close. This is by design, not a deficiency.
**Source:** 22-05-SUMMARY.md, 22-VERIFICATION.md
