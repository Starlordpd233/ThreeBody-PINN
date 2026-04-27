# Phase 9: Issues Directory Consolidation - Research

**Researched:** 2026-04-27
**Domain:** Documentation consolidation, technical audit synthesis, plain Markdown authoring
**Confidence:** HIGH

## Summary

This phase reorganizes 7 scattered issue/audit files (~246 KB total) in `pinn_instruction/original_latex/review-of-framework/issues/` into 3 thematic Markdown documents, plus supporting metadata files. The work is purely editorial: synthesized rewrite, deduplication, conflict resolution, and archival. No source code or LaTeX templates are modified.

The 7 source files span three technical layers: (1) network architecture and physics foundations, (2) data pipeline and validation, and (3) curriculum stratification and training loop mechanics. The 2026-04-27 comprehensive audit (38 KB) is the structural spine; the other 6 files either extend it with deeper analysis, contradict it on specific points, or are mostly superseded by it. The primary planning challenge is mapping every unique finding to the correct thematic bucket while resolving two live conflicts (input vector orientation encoding, frame for s_min) and cherry-picking only genuinely unique content from the oldest 128 KB dump.

**Primary recommendation:** Treat the audit as the canonical source for ~80% of content; use the Causal_Trainingmismatch blueprint for its physically-motivated input-vector alternative and Time-Windowed Causal-ALM Hybrid; use review.md for the AD chain-rule factor finding; use stage-assignment-issue.txt for the data-driven PCA/K-means methodology; cherry-pick 4 items from next steps.txt; archive everything else.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Documentation consolidation | Human / Agent | — | Pure editorial task; no runtime tier involvement |
| Content deduplication | Human / Agent | — | Requires reading and cross-referencing all 7 sources |
| Conflict resolution (trig vs shape invariants) | Human / Agent | — | Physical/mathematical judgment call per D-05 |
| Git history preservation | CLI (git mv) | — | Archive via `git mv` to preserve provenance |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| git | system | Archive originals via `git mv` | Preserves history; project convention from Phases 1-2 |
| plain Markdown | — | Output format | Project uses no MkDocs/Sphinx/MDX per CONTEXT.md |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `wc` / `ls` | system | Size verification | Confirm target size budget met |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Plain Markdown | MkDocs/Sphinx | Rejected: project explicitly uses plain Markdown only |
| `git mv` | `mv` + manual note | Rejected: loses file history; project convention is `git mv` |
| 3 thematic docs | 2 docs (merge data+training) | Rejected: training loop and data pipeline are distinct future implementation phases |

## Architecture Patterns

### System Architecture Diagram

```
7 source files ──read──> Content inventory ──> Deduplication analysis
     │                                              │
     v                                              v
Archive (git mv)                              Thematic mapping
     │                                              │
     v                                              v
issues/archive/          <──provenance──    3 synthesized .md docs
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    │                             │                             │
                    v                             v                             v
         01-architecture-and-physics      02-data-pipeline-and-       03-curriculum-and-training-loop
              -foundations.md                   validation.md
                    │                             │                             │
                    └─────────────────────────────┴─────────────────────────────┘
                                                  │
                                                  v
                                           MIGRATION.md (per-section provenance)
                                           README.md (navigation anchor)
```

### Recommended Project Structure (after consolidation)

```
pinn_instruction/original_latex/review-of-framework/issues/
├── archive/                                       # 7 originals, git-mv'd
│   ├── three_body_pinn_pre-implementation_audit_2026-04-27.md
│   ├── Causal_Trainingmismatch_resolution_blueprint.md
│   ├── Issue_on_data_validation_protocol_and_compatbility_with_project_context.md
│   ├── review.md
│   ├── stage-assignment-issue.txt
│   ├── next-step-for-data-processing-pipeline.txt
│   └── next steps.txt
├── 01-architecture-and-physics-foundations.md     # NEW
├── 02-data-pipeline-and-validation.md             # NEW
├── 03-curriculum-and-training-loop.md             # NEW
├── MIGRATION.md                                   # NEW
└── README.md                                      # NEW
```

### Pattern 1: Synthesized Rewrite (not Verbatim Concatenation)
**What:** Write fresh thematic docs that re-state findings clearly, deduplicate cross-source repetition, and cross-link between docs.
**When to use:** All 3 output documents.
**Example:** Audit Section 5 (Corrected Input Vector Spec) should be copied verbatim into `01-...` as it is a formal reference spec. Audit Section 6 (Unified Batch Construction) should be copied verbatim into `03-...`. Everything else should be synthesized.

### Pattern 2: Per-Section Provenance Tracking
**What:** `MIGRATION.md` records, for every major section heading in each of the 7 originals, which new doc absorbed it and whether it was synthesized, copied verbatim, or archived-only.
**When to use:** Required by D-09.
**Example:**
```markdown
## next steps.txt (archived)
| Original section | Destination doc(s) | Notes |
|---|---|---|
| Issue 1: Lyapunov tau_L / L_max | 03-curriculum-and-training-loop.md §Stage assignment | Resolved subsection extracted |
| 5 Orders of Magnitude Difference | 01-architecture-and-physics-foundations.md §Softening | Unique to this file |
| Issue 6: Batch construction | (covered by audit) | Not extracted; archived only |
```

### Pattern 3: Conflict Resolution with "Considered Alternatives"
**What:** When two sources contradict, pick the stronger position and document the loser under "Considered Alternatives."
**When to use:** Required by D-05 for two known live conflicts.
**Example:**
```markdown
### Input Vector Orientation Encoding
**Resolved position:** Shape invariants + direction cosines (Causal_Trainingmismatch)
**Rationale:** Trig encodings have gimbal-lock pathologies during chaotic scattering...

#### Considered Alternatives
- **Trig encoding [sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]**
  - Source: 2026-04-27 audit B-04, §5.3
  - Reason not chosen: Gimbal lock during late-stage chaotic events...
```

### Anti-Patterns to Avoid
- **Verbatim pasting without synthesis:** The 3 new docs combined must be smaller than the 7 originals (~80-120 KB target vs ~246 KB source). If >= 80% of source size, the rewrite failed.
- **Silent dropping of contradictory positions:** Per D-05, the losing position must be recorded, not erased.
- **Injecting deprecation headers into originals:** D-07 explicitly forbids this; the `archive/` folder name and `MIGRATION.md` carry the signal.
- **Duplicating dataset documentation:** `02-data-pipeline-and-validation.md` must cross-link to `simulation_data/Documentation/README.md`, not duplicate it.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Table of contents / navigation | Custom TOC generator | Manual README.md with markdown links | Plain Markdown; no tooling dependency |
| File size measurement | Custom script | `wc -c` | Simple, exact, already available |
| Git archival | `cp` + `rm` | `git mv` | Preserves history; project convention |
| Markdown linting | Custom linter | None needed | Plain Markdown only; no compliance requirement |

## Runtime State Inventory

This phase is documentation-only with no runtime state. All changes are to files tracked in git.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None | — |
| Live service config | None | — |
| OS-registered state | None | — |
| Secrets/env vars | None | — |
| Build artifacts | None | — |

## Common Pitfalls

### Pitfall 1: Underestimating `next steps.txt` Cherry-Pick Effort
**What goes wrong:** The 128 KB dump is mostly superseded, but the 4 unique items (5-OoM softening, global-scale computation, normalization verification table, Issue 1 resolution) are scattered across ~50 issue sections. A naive grep may miss them.
**Why it happens:** The file is an unindexed brain dump with no table of contents.
**How to avoid:** Use the explicit list from D-06 as a checklist. Verify each candidate is genuinely absent from the audit before extracting.
**Warning signs:** If `01-architecture-and-physics-foundations.md` has no "Softening" section, the 5-OoM analysis was missed.

### Pitfall 2: Overlapping Coverage Between Thematic Docs
**What goes wrong:** COM frame, softening, and input vector dimensionality are touched by all 3 source categories. If each doc repeats the full context, the target size budget is blown.
**Why it happens:** These are cross-cutting concerns.
**How to avoid:** Assign a canonical owner per topic (per D-01) and use brief cross-links in the other docs. Example: COM frame lives in `01-...`; `02-...` and `03-...` mention it in one sentence with a link.

### Pitfall 3: Missing Unique Findings from Smaller Files
**What goes wrong:** `review.md` (6 KB) and `Issue_on_data_validation_protocol...` (8 KB) are small but contain unique findings (AD chain-rule factor, causal Option-A-vs-B framing) that do not appear in the audit.
**Why it happens:** Temptation to focus on the large audit and blueprint files.
**How to avoid:** Explicitly check each of the 7 files against the content inventory table below before declaring consolidation complete.

### Pitfall 4: MIGRATION.md Becomes Unmaintainable
**What goes wrong:** Listing every subsection of the 128 KB dump creates a 50-row table that is itself unmaintainable.
**Why it happens:** Over-zealous provenance tracking.
**How to avoid:** Track at the "Issue N" or major section level, not per-paragraph. D-09 says "every major section heading," not every paragraph.

## Code Examples

No code implementation is in scope for this phase. The only "code" is Markdown authoring patterns.

### Verified Markdown Pattern: Decision-Needed Callout
```markdown
> **[DECISION-NEEDED]** Input vector composition (14-D content)
>
> Two competing proposals exist:
> 1. Trig encoding: 5 values for 3 angles (audit B-04)
> 2. Shape invariants + direction cosines: 3 + 2 = 5 values (Causal_Trainingmismatch)
>
> Current consolidated doc adopts position #2. Revisit before implementation.
```

### Verified Markdown Pattern: Severity Labels
```markdown
| ID | Severity | Finding |
|----|----------|---------|
| B-01 | BLOCKING | SIREN hidden-layer init formula multiplies by omega0 instead of dividing |
| M1 | MAJOR | Input vector: CTL assembles 11D IC; PINN expects 13D IC |
| D1 | MINOR | What exactly are the 3 angles for trigonometric encoding? |
```

## State of the Art

This phase is editorial, not technical implementation. No "old approach vs current approach" applies to the consolidation methodology itself. The findings being consolidated are state-of-the-art as of 2026-04-27.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The 2026-04-27 audit subsumes ~80% of `next steps.txt` | Summary / D-06 | If wrong, unique findings may be lost; mitigated by explicit cherry-pick checklist |
| A2 | Shape invariants + direction cosines is physically superior to trig encoding | Conflict resolution | If wrong, implementation phase may need to revert; mitigated by "Considered Alternatives" section |
| A3 | The 3 thematic docs can be kept under 120 KB combined | Standard Stack | If wrong, deduplication failed; planner should enforce size check |
| A4 | `git mv` preserves history through the archive move | Runtime State | If wrong, provenance is lost; standard git behavior |

## Open Questions

1. **Exact length of `next steps.txt` unique content**
   - What we know: 4 items are explicitly flagged as unique (5-OoM softening, global-scale computation, normalization verification, Issue 1 resolution)
   - What's unclear: Whether any other sections in the 128 KB dump contain genuinely unique analysis not in the audit
   - Recommendation: During implementation, grep each Issue N title against the audit before deciding to archive-only

2. **Whether to include the full "Synthesized Curriculum Training Protocol" from Causal_Trainingmismatch**
   - What we know: It is a 4-phase narrative (Static Pre-Screening -> IPR Bounding -> Causal-ALM Loop -> Refinement)
   - What's unclear: Whether this narrative duplicates audit Section 6 or extends it
   - Recommendation: Compare against audit Section 6 (Unified Batch Construction); if the narrative adds the causal-window gating mechanism not in the audit, include it in `03-...`

3. **Cross-doc Interaction Matrix**
   - What we know: Audit Section 8 has an 8-row interaction matrix
   - What's unclear: Whether to copy it verbatim into `README.md` or synthesize a smaller version
   - Recommendation: Per Claude's discretion, include a condensed version in `README.md`

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| git | Archiving originals | Yes | system | — |
| Markdown renderer | Verification (optional) | Yes | any | Visual inspection sufficient |
| `wc` | Size verification | Yes | system | — |

**Missing dependencies with no fallback:** None.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None (documentation-only phase) |
| Config file | none |
| Quick run command | `wc -c issues/01-*.md issues/02-*.md issues/03-*.md` |
| Full suite command | Manual review of MIGRATION.md completeness |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONSOL-01 | All 7 files read and merged into 2-3 thematic files | manual | Verify 3 new docs exist | N/A |
| CONSOL-02 | No unique findings lost | manual | Cross-check MIGRATION.md against content inventory | N/A |
| CONSOL-03 | Each doc has clear, distinct purpose | manual | Read opening paragraph of each doc | N/A |

### Sampling Rate
- **Per task commit:** Verify file exists and size is reasonable
- **Per wave merge:** Verify MIGRATION.md has an entry for every original file
- **Phase gate:** All 7 originals in `archive/`, all 5 new files in `issues/`, no orphaned content

### Wave 0 Gaps
- None — this phase has no test infrastructure gaps (it is editorial)

## Security Domain

Not applicable. This phase produces documentation only; no executable code, no network interfaces, no authentication, no cryptography.

## Sources

### Primary (HIGH confidence)
- `pinn_instruction/original_latex/review-of-framework/issues/three_body_pinn_pre-implementation_audit_2026-04-27.md` — Comprehensive audit (38 KB); structural spine. Read in full.
- `pinn_instruction/original_latex/review-of-framework/issues/Causal_Trainingmismatch_resolution_blueprint.md` — Architecture+training reconciliation (48 KB). Read in full.
- `09-CONTEXT.md` — Locked decisions, discretion areas, deferred ideas. Read in full.

### Secondary (MEDIUM confidence)
- `pinn_instruction/original_latex/review-of-framework/issues/Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` — Pre-agent validation gap analysis (8 KB). Read in full.
- `pinn_instruction/original_latex/review-of-framework/issues/review.md` — Scaling-contract review (6 KB). Read in full.
- `pinn_instruction/original_latex/review-of-framework/issues/stage-assignment-issue.txt` — Curriculum-stratification methodology (10 KB). Read in full.
- `pinn_instruction/original_latex/review-of-framework/issues/next-step-for-data-processing-pipeline.txt` — Mixed pipeline asks (6 KB). Read in full.

### Tertiary (LOW confidence — cherry-pick only)
- `pinn_instruction/original_latex/review-of-framework/issues/next steps.txt` — Oldest dump (128 KB, mostly superseded). Sampled at 500-line intervals to confirm structure; unique items identified per D-06 checklist.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no external dependencies, plain Markdown only
- Architecture: HIGH — output structure is fully specified in CONTEXT.md
- Pitfalls: MEDIUM — based on pattern recognition from prior consolidation phases in this project

**Research date:** 2026-04-27
**Valid until:** 2026-05-27 (documentation content is stable; only implementation findings may update)

---

## Appendix: Detailed Content Inventory

### File 1: `three_body_pinn_pre-implementation_audit_2026-04-27.md` (38 KB)
**Unique contributions:**
- Executive Summary with Top 3 Blocking Issues ranked
- 11 Critical Issues (B-01..B-11) with severity, location, root cause, impact, fix, evidence
- 16 Major Inconsistencies (M1..M16) in table format with resolution strategy
- 10 Design Ambiguities (D1..D10) with proposed experiment/decision path
- 28 Author-Flagged Uncertainties — resolution status table
- Section 5: Corrected 14-D Input Vector Specification (verbatim-copy quality)
- Section 6: Unified Batch Construction Specification (verbatim-copy quality)
- Section 7: Implementation Checklist (P0..P4)
- Section 8: Cross-Issue Interaction Matrix
- Section 9: Quantitative Impact Summary

**Thematic mapping:**
- `01-architecture-and-physics-foundations.md`: B-01, B-02, B-03, B-04, B-05, B-09, B-10, M1-M5, M8-M10, D1-D4, D6-D10, Section 5
- `02-data-pipeline-and-validation.md`: B-06, B-11, M11-M13, D7, parts of D4/D6
- `03-curriculum-and-training-loop.md`: B-07, B-08, M6-M7, M14-M16, D5, Section 6, Section 7 P3-P4

### File 2: `Causal_Trainingmismatch_resolution_blueprint.md` (48 KB)
**Unique contributions:**
- Time-Windowed Causal-ALM Hybrid architecture (4-phase narrative)
- **Input vector alternative:** Shape invariants (I1,I2,I3) + direction cosines (cos theta, sin theta) vs audit's trig encoding
- Dual-Context Epsilon Strategy (eps=1e-10 for static invariants, eps_soft=1e-5 for dynamic loss)
- SCS/SASD/IPR/PSC redesign as live training parameters (not just pre-training gates)
- Temporal resolution bridging argument (dt_out mandates per curriculum stage)
- Frame convention: aggressive automated Galilean boost mandate

**Thematic mapping:**
- `01-architecture-and-physics-foundations.md`: Input vector alternative, dual-epsilon strategy, frame convention
- `02-data-pipeline-and-validation.md`: SCS/SASD/IPR/PSC redesign, temporal resolution bridging
- `03-curriculum-and-training-loop.md`: Time-Windowed Causal-ALM Hybrid, 4-phase training narrative

**Key conflict with audit:** Input vector orientation encoding (trig vs shape invariants + direction cosines). Per D-05, resolve by physical/mathematical soundness.

### File 3: `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` (8 KB)
**Unique contributions:**
- Framing of the causal training mismatch as an explicit Option A vs Option B decision
- 6 gaps identified from initial README+validation PDF review
- Resolution table showing which gaps are resolved by PINN+CTL documents
- Recommended information package for the agent

**Thematic mapping:**
- `02-data-pipeline-and-validation.md`: Gap analysis, validation protocol critique
- `03-curriculum-and-training-loop.md`: Option A vs Option B causal training decision (flag as [DECISION-NEEDED])

### File 4: `review.md` (6 KB)
**Unique contributions:**
- AD chain-rule factor missing -> physics residual off by 4x, kinetic energy off by 4x
- Three-layer separation formalism: raw -> physics-scaled -> network-input
- Explicit derivative conversion rules: dr'/du = 2*dr'/dtau, d2r'/du2 = 4*d2r'/dtau2

**Thematic mapping:**
- `01-architecture-and-physics-foundations.md`: AD chain-rule factor, three-layer scaling contract

### File 5: `stage-assignment-issue.txt` (10 KB)
**Unique contributions:**
- Data-driven adaptive stage assignment methodology (PCA + K-means + quantiles)
- Python code snippets for EDA, clustering, and assignment
- Hybrid approach: physical metrics + empirical distributions
- Correlation analysis recommendation

**Thematic mapping:**
- `03-curriculum-and-training-loop.md`: Data-driven stage assignment, PCA/K-means methodology

### File 6: `next-step-for-data-processing-pipeline.txt` (6 KB)
**Unique contributions:**
- h5 -> txt/json format question (file format for processed data)
- I_norm text-vs-code inconsistency (text: raw tr(I)/(M r_char^2); code: tanh of that)
- 12 author-flagged `\authcomment` items in CTL document (list with line numbers)
- Grok's response on COM transformation timing (put after step 2 global scaling)

**Thematic mapping:**
- `02-data-pipeline-and-validation.md`: File format question [DECISION-NEEDED], I_norm inconsistency
- `01-architecture-and-physics-foundations.md`: I_norm definition resolution
- `03-curriculum-and-training-loop.md`: COM transformation order (Step 2 vs Step 2.5)

### File 7: `next steps.txt` (128 KB)
**Unique contributions (cherry-pick only per D-06):**
1. **"5 Orders of Magnitude Difference" softening analysis** (Issue 15) — deep dive into eps=1e-10 vs eps=1e-5 divergence
2. **"Issue 17: Global scale computation implementation"** — `compute_globals` parallelized pseudo-code over all ICs
3. **"Issue 19: Normalization formulas verification"** — comprehensive table of E_norm, s_min_norm, m_norm, Q_norm formulas with cross-document confirmation
4. **"Issue 1: Lyapunov time tau_L and L_max formula resolution"** — verified+resolving section with full Python implementation

**Everything else in this file is superseded by the 2026-04-27 audit.** Archive only.

**Thematic mapping:**
- `01-architecture-and-physics-foundations.md`: 5-OoM softening analysis
- `02-data-pipeline-and-validation.md`: Global scale computation, normalization formulas
- `03-curriculum-and-training-loop.md`: tau_L / L_max computation

---

## Appendix: Overlap/Deduplication Analysis

| Topic | Audit | Causal_Trainingmismatch | Other files | Canonical home |
|-------|-------|------------------------|-------------|----------------|
| SIREN init bug (B-01) | Full | Mentioned | — | `01-...` |
| D formula (B-02) | Full | Mentioned | next steps (Issue 9, 17) | `01-...` |
| Input vector 14-D (B-03/B-04) | Full (trig) | Full (shape+dir-cos) | — | `01-...` (with conflict resolution) |
| COM frame (B-05) | Full | Full | next-step (Grok response) | `01-...` |
| Batch construction (B-07/B-08) | Full (Section 6) | Mentioned | next steps (Issue 6) | `03-...` |
| Softening mismatch (B-09) | Full | Full (dual-context) | next steps (Issue 15) | `01-...` |
| Omega0 scheduling (B-10) | Full | Mentioned | next steps (Issue 4, 14) | `01-...` |
| Non-contiguous IDs (B-11) | Full | Mentioned | — | `02-...` |
| AD chain-rule factor | — | — | review.md (unique) | `01-...` |
| Causal Option A vs B | — | Full | Issue_on_data_validation (unique framing) | `03-...` |
| Data-driven stage assignment | — | — | stage-assignment-issue (unique) | `03-...` |
| SCS/SASD/IPR/PSC as live params | — | Full | — | `02-...` + `03-...` |
| h5 vs txt/json | — | — | next-step-for-data-processing (unique) | `02-...` [DECISION-NEEDED] |
| I_norm text-vs-code | — | — | next-step-for-data-processing (unique) | `01-...` |
| tau_L / L_max formulas | Partial (B-04, M7) | — | next steps (Issue 1, 16) (full code) | `03-...` |
| Normalization formulas table | Partial (Section 5) | — | next steps (Issue 19) (comprehensive) | `01-...` + `02-...` |

---

## Appendix: Recommended File Structure and Size Estimates

| File | Estimated Size | Rationale |
|------|---------------|-----------|
| `01-architecture-and-physics-foundations.md` | 30-40 KB | Audit Section 5 (verbatim) + B-01..B-05, B-09, B-10, M1-M5, M8-M10, D1-D4, D6-D10, review.md chain-rule, Causal_Trainingmismatch input-vector alternative, 5-OoM softening, I_norm resolution |
| `02-data-pipeline-and-validation.md` | 20-30 KB | B-06, B-11, M11-M13, D7, h5-vs-txt question, global scale computation, normalization formulas, SCS/SASD/IPR/PSC as live params (data side), temporal resolution bridging |
| `03-curriculum-and-training-loop.md` | 30-40 KB | Audit Section 6 (verbatim) + B-07, B-08, M6-M7, M14-M16, D5, Section 7 P3-P4, causal Option A vs B, Time-Windowed Causal-ALM Hybrid, data-driven stage assignment, tau_L/L_max code |
| `MIGRATION.md` | 5-8 KB | Per-file, per-section provenance map for 7 originals |
| `README.md` | 2-3 KB | Navigation anchor (<= 50 lines per D-11) |
| **Total new** | **87-121 KB** | Target: 80-120 KB (vs 246 KB source) |

---

## Appendix: Cross-Link Dependencies Between the 3 New Docs

| Topic | Canonical home | Referenced by |
|-------|---------------|---------------|
| 14-D input vector spec | `01-...` | `02-...` (data pipeline produces it), `03-...` (training consumes it) |
| COM frame transformation | `01-...` | `02-...` (validation must apply same transform) |
| Dual-epsilon strategy | `01-...` | `02-...` (validation uses static eps), `03-...` (training uses dynamic eps) |
| D = 6.694 | `01-...` | `02-...` (recompute stage assignments), `03-...` (stage thresholds in scaled units) |
| Replay/lookahead batch | `03-...` | `02-...` (DataLoader must support stage queries) |
| Stage assignment criteria | `03-...` | `02-...` (pipeline outputs stage labels) |
| TrajectoryValidator gate | `02-...` | `03-...` (training loop assumes validated data) |

---

## Appendix: Verification Strategy (How to Prove Consolidation Succeeded)

1. **Completeness check:** For each of the 7 originals, verify `MIGRATION.md` has an entry for every major section heading.
2. **Unique findings check:** Cross-reference the "Unique contributions" lists above against the 3 new docs. Every bullet must appear somewhere.
3. **Conflict resolution check:** Both live conflicts (input vector encoding, s_min frame) must have a "Considered Alternatives" subsection.
4. **Size check:** `wc -c` on the 3 new docs must total < 120 KB.
5. **Archive check:** All 7 originals must be in `issues/archive/` with git history preserved (`git log --follow` on one archived file should show pre-move history).
6. **No-duplicate check:** A grep for identical paragraphs (>5 lines) across the 3 new docs should return zero hits (synthesis, not concatenation).
7. **Decision callouts check:** All 4 [DECISION-NEEDED] items from D-12 must appear in the relevant docs.
