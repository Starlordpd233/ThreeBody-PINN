---
phase: 30
phase_name: "research-package-assembly"
project: "3-body-problem"
generated: "2026-07-02T04:56:08+00:00"
counts:
  decisions: 8
  lessons: 5
  patterns: 8
  surprises: 5
missing_artifacts: []
---

# Phase 30 Learnings: Research Package Assembly

## Decisions

### MULTI-COMPOSITION package form locked
**What was decided:** Lock the research package form as MULTI-COMPOSITION before assembly, preventing downstream plans (30-03, 30-04, 30-05) from re-litigating the package structure.
**Rationale:** Provides one settled architecture target for multiple authors; prevents package-structure drift during assembly; allows downstream plans to author against a stable foundation.
**Source:** 30-02-SUMMARY.md (tech tracking patterns)

### D-09 APPROVED record filled autonomously
**What was decided:** Ratify the D-09 gate using user's pre-authorized approve-as-proposed waivers, filled the APPROVED record autonomously without explicit user prompts.
**Rationale:** User pre-authorized safe defaults; reversible until 30-03; no need to interrupt workflow for approval; allows autonomous execution.
**Source:** 30-02-SUMMARY.md ("F16: FILLED record" verification)

### verified-facts-reference.md created as STANDALONE companion
**What was decided:** Create verified-facts-reference.md as a STANDALONE companion file solely owned by 30-03 Task 2, not folded into consolidated context.
**Rationale:** Prevents consolidation from forcing other companions to re-cite buried fragments; verified rows retain their v1.5 citations; provides clear single-owner provenance.
**Source:** 30-03-SUMMARY.md (F11 verification)

### source_baseline pinned to assembly-time HEAD, NOT recovery-tag
**What was decided:** Pin source_baseline to assembly-time HEAD (522cea7182bf3d0e3206d8faa75150e705b174f0), not to the recovery-tag (e841c958b1ae7b18c9cdaa40b9e2432ecf7cc870).
**Rationale:** Recovery tag trails HEAD by few commits; pinning to HEAD ensures snapshots match when created; provides more reliable baseline for downstream reproducibility.
**Source:** 30-03-SUMMARY.md (F7 verification, audit refresh note)

### Package form locked before D-09 gate
**What was decided:** Lock the MULTI-COMPOSITION package form in 30-02 before assembly, not re-litigated at the D-09 gate.
**Rationale:** Gives downstream plans a settled architectural target; prevents package-structure drift during assembly; explicit F3 decision up-front.
**Source:** 30-02-SUMMARY.md (F3)

### Inclusion calls resolved: minimal sim_data excerpts, standalone verified-facts-reference, ALM-μ_p-clamp question
**What was decided:** (a) Include minimal simulation_data/v1.5 excerpts in consolidated context, (b) keep verified-facts-reference.md standalone, (c) include the ALM-μ_p-clamp question in framed questions.
**Rationale:** Minimal excerpts preserve grounding while keeping context consolidated; standalone companion avoids fragment duplication; ALM-clamp inclusion preserves LOOP-05 coverage.
**Source:** 30-02-SUMMARY.md ("Inclusion calls" section)

### RESEARCH-CONTEXT-MASTER.md as single uploaded entry point
**What was decided:** Create RESEARCH-CONTEXT-MASTER.md as the single uploaded entry point with preamble + manifest + reading order, not as multiple files.
**Rationale:** Single entry point simplifies ERW multi-AI handoff; master lists all companions and ensures reading order; user-friendly RESEARCH-AGENT-PROMPT.md references master by bare filename.
**Source:** 30-05-SUMMARY.md (accomplishments)

### DELIVERY-NOTE.md at round root (repo-blind routing)
**What was decided:** Place DELIVERY-NOTE.md at the package round root (user-only, never uploaded) containing landing path and gate semantics.
**Rationale:** Zero repo paths in uploaded content; repo-blind for external research; routing isolated to DELIVERY-NOTE.md at round root.
**Source:** 30-05-SUMMARY.md (D03 plan)

---

## Lessons

### Recovery-tag staleness discovered and documented
**What was learned:** The existing tag v1.6-pre-phase-30 was orphaned (not an ancestor of HEAD), requiring a user decision before Phase 30 work could proceed.
**Context:** Task 1 required verification that the recovery tag pointed at HEAD; discovered the tag pointed to an old commit (85f72f88).
**Source:** 30-01-SUMMARY.md (Task 1)

### D-09 APPROVED record structure clarified
**What was learned:** The D-09 APPROVED record requires a FILLED block with status, authority, document list, resolved inclusion calls, and declined-findings slot — not just the literal string "APPROVED".
**Context:** Plan specified F16 filled requirement; automation learned that the APPROVED record structure includes specific fields (status, authority, document list, inclusion calls, declined-findings).
**Source:** 30-02-SUMMARY.md (Decisions Made section)

### Auto-fixed gsd-tools state-verb regression
**What was learned:** The gsd-tools state-verb (add-decision, add-blocker) regressed STATE.md counters (progress_plans, completed_plans) and frontmatter fields (status, stopped_at, last_activity) during gate-open recording.
**Context:** Task 3 discovered regression bug when recording gate-open state; required manual restoration of handler-induced regressions to maintain F2 invariant.
**Source:** 30-05-SUMMARY.md (Deviations from Plan → Auto-fixed Issues)

### Verified-facts-reference.md ownership pattern
**What was learned:** Standalone companion files with single ownership (verified-facts-reference.md owned solely by 30-03) prevent consolidation from fragmenting citation lines.
**Context:** 30-03 claimed sole ownership (F11); consolidation plan respected this; per D-09 inclusion call (b) the standalone form was pre-approved.
**Source:** 30-03-SUMMARY.md (key-decisions, verified-facts-reference.md created)

### Zero repo paths required for repo-blind ERW package
**What was learned:** Research package must have zero repo-path leaks in both the master file and RESEARCH-AGENT-PROMPT.md to ensure repo-blind external research.
**Context:** VC-01 verification required 0 hits; all uploaded files must be referenced by bare filename only.
**Source:** 30-05-SUMMARY.md (VC-01 verification, tech tracking patterns)

---

## Patterns

### Multi-companion ERW package with repo-blind uploads
**Description:** Research package ships as multiple companion files referenced by bare filename in a manifest, ensuring zero repo-path contamination in both the uploaded master and paste-ready prompt.
**When to use:** ERW research packages requiring repo-blind external research handoff; when documents must maintain repo-path integrity.
**Source:** 30-05-SUMMARY.md (tech tracking: "Multi-companion ERW package")

### Byte-for-byte cp snapshotting with dual provenance
**Description:** Package source files are copied byte-for-byte (`cp`) while recording BOTH content SHA-256 (byte-fidelity) and source commit (provenance) for each packaged snapshot.
**When to use:** When absolute provenance tracking is needed; verification requires both file identity AND git provenance.
**Source:** 30-03-SUMMARY.md (patterns: "byte-for-byte cp snapshotting", "content sha256 + source-commit dual provenance")

### Assembly-time HEAD pin for source_baseline
**Description:** Pin source_baseline to the assembly-time git HEAD (not a recovery tag) to ensure snapshots match the state when created.
**When to use:** When research package needs a reliable baseline for content re-derivation or snapshot refresh.
**Source:** 30-03-SUMMARY.md (F7 verification: "source_baseline = assembly-time HEAD")

### CLM-NN append-only claim-ID scheme
**Description:** Claims register uses stable, append-only CLM-NN IDs (CLM-01, CLM-02, ...) that never get renumbered, providing traceability for every figure.
**When to use:** When tracking dataset/empirical figures across phases; when reference IDs must be stable.
**Source:** 30-01-SUMMARY.md (key-decisions: "CLM-NN append-only claim-ID scheme")

### D-09 APPROVED record as FILLED block with multiple fields
**Description:** The D-09 user gate requires a FILLED APPROVED record with status, authority, document list, resolved inclusion calls, and declined-findings slot - not just the literal "APPROVED" string.
**When to use:** When hard user checkpoint gates require populated approval records with structured metadata; when validating gate completion.
**Source:** 30-02-SUMMARY.md (key-decisions: "F16: FILLED record")

### F12 self-containment cross-check for repo-blind packages
**Description:** Run bidirectional self-containment check verifying: (a) every shipped file appears in manifest, (b) every manifest reference resolves to a shipped file, (c) no dangling manifest/attach rows.
**When to use:** When validating package delivery; when ensuring repo-blind integrity for external research.
**Source:** 30-05-SUMMARY.md (Self-Check: PASSED)

### Three-inclusion-call resolution pattern
**Description:** D-09 gate resolved three inclusion calls autonomously: (a) minimal sim_data excerpts, (b) standalone verified-facts-reference, (c) include ALM-μ_p-clamp question — all cross-checked against 30-RESEARCH with zero conflicts.
**When to use:** When consolidating research materials; when multiple inclusion calls have dependencies or conflicts that need resolution.
**Source:** 30-02-SUMMARY.md (D-09 APPROVED record)

### Lock/open delineation for contested SCOPE-12 values
**Description:** Contested values (like D=6.694 vs D≈4.6416) carry LOCKED vs OPEN delineation blocks preventing re-opening locked SCOPE-12 hard constraints.
**When to use:** When framing neutral research questions with contested scientific parameters; when protecting hard constraint decisions from being re-posed.
**Source:** 30-04-SUMMARY.md (F5 locked/open delineation pattern)

---

## Surprises

### Recovery tag was orphaned, not ancestor of HEAD
**What was surprising:** The existing tag `v1.6-pre-phase-30` pointed to commit 85f72f88, which was not an ancestor of HEAD; required user decision to either re-cut tag or create fresh distinctly-named tag.
**Impact:** Added Task 1 human-approval checkpoint; required orchestrator pre-resolution before first Phase 30 commit; delayed workflow until resolved.
**Source:** 30-01-SUMMARY.md (Task 1 pre-flight, deviation note)

### Audit refresh required source_baseline update after path-only citation repair
**What was surprising:** After Phase 30 delivery, an audit refresh updated the package baseline from the assembly-time HEAD (522cea71) to a newer commit (3781d1a) due to a path-only citation repair in ctl_instruction.md.
**Impact:** The source_baseline pin in 30-SNAPSHOT-HASHES.txt was correct at assembly time, but the DELIVERY-NOTE.md reflected the refreshed baseline; milestone closure audit confirms both HEAD baselines are valid (one for assembly-time, one post-refresh).
**Source:** 30-03-SUMMARY.md (audit refresh note in body, F7 verification note)

### Orphaned recovery-tag pattern discovered
**What was surprising:** Recovery-tag pattern from v1.5 (tag on milestone branch then rebase) doesn't apply to v1.6 (tag on branch, orphaned after rebase).
**Impact:** Required adaptation of recovery-tag pre-flight workflow to handle orphaned tag scenario; new workflow asks for user decision on re-cut vs fresh tag.
**Source:** 30-01-SUMMARY.md (Task 1, deviation note)

### gsd-tools state-verb regression during gate recording
**What was surprising:** gsd-tools state handlers (add-decision, add-blocker) regressed STATE.md progress counters and frontmatter fields when recording gate-open state.
**Impact:** Required manual restoration of handler-induced regressions to maintain F2 "counters unchanged" invariant; net STATE change was only gate record + benign timestamp.
**Source:** 30-05-SUMMARY.md (Deviations from Plan → Auto-fixed Issues)

### Consolidation rule threshold (>5 files) triggered MULTI-COMPOSITION form
**What was surprising:** The PKG-05 consolidation rule fires when deliverable set exceeds ~5 files, requiring scattered fragments to be consolidated into ONE context file, but framework specs never consolidate (D-04).
**Impact:** Package form changed from v1.5 pattern to MULTI-COMPOSITION; consolidated-context.md contains only minimal excerpts, while framework specs ship as byte-for-byte snapshots.
**Source:** 30-02-SUMMARY.md (tech tracking: "PKG-05 consolidation rule")