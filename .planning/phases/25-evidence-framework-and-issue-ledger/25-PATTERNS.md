# Phase 25: Evidence Framework and Issue Ledger - Pattern Map

**Mapped:** 2026-06-11
**Files analyzed:** 6 (2 machinery, 3 EVID-10 records, 1 in-place ledger re-issue)
**Analogs found:** 6 / 6 (all exact — every artifact instantiates a committed v1.4 Phase 16 precedent)

> This is a documentation/adjudication phase: zero code, zero framework-spec edits (CONTEXT D-02). "Patterns" here are Markdown artifact structures, heading conventions, citation formats, and lifecycle-rule wording. Every new artifact is an adaptation of a committed v1.4 precedent or an in-place edit of a Phase 24 deliverable. The planner's job is fidelity to existing structure, not redesign (RESEARCH "Don't Hand-Roll").

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `evidence/_TEMPLATE.md` | config (schema) | transform (copy-source) | `16-.../evidence/_TEMPLATE.md` | exact (adapt per D-04) |
| `evidence/README.md` | config (protocol) | transform (governance doc) | `16-.../evidence/README.md` | exact (adapt per D-03/D-05) |
| `evidence/scs-thresholds.md` | model (EVID-10 record) | transform (adjudication) | `16-.../evidence/B-09.md` (conflict packet) | role-match |
| `evidence/compute-globals-D.md` | model (EVID-10 record) | transform (adjudication) | `16-.../evidence/B-02.md` (D-formula conflict) | exact (same conflict family) |
| `evidence/m11-m12-severity.md` | model (EVID-10 record) | transform (adjudication) | `16-.../evidence/M5.md` / B-02 structure | role-match |
| `24-ISSUE-LEDGER.md` (Lifecycle Rules block) | config (state index) | event-driven (status machine) | same file, v1.4 README §Regression/§Phase-Exit | exact (in-place re-issue) |

**ID→filename map (Claude's discretion, CONTEXT "Claude's Discretion" ID→filename note):** record in `evidence/README.md`. Recommended: `scs-thresholds.md` (ledger ID `SCS`), `compute-globals-D.md` (ledger ID `D=6.694`), `m11-m12-severity.md` (ledger IDs `M11`+`M12`). Filesystem-safe, greppable, one-file-per-conflict consistent with v1.4.

## Pattern Assignments

### `evidence/_TEMPLATE.md` (config schema, transform)

**Analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` — copy the markdown structure and prose exactly; apply only the D-04 substitutions.

**Canonical section count:** 12 `##` section headings plus the `#` title. The list below includes the title as item 1 and the 12 `##` headings as items 2-13. The new `### Dataset Evidence (§3b)` is a sub-block under `## Spec Evidence`; it does not add a new `##` section.

**Section structure to copy (analog lines 1-103), in order:**
1. Title `# Evidence Packet: <ID> - <Title>`
2. `## Header` — 9-row table (lines 3-15): ID, Title, Severity, Current Status, Current Verdict, Phase, Acceptance Check ID, Spec Sections Touched, Code Paths Touched
3. `## Source Positions` — side-by-side line-range table (lines 17-26)
4. `## Spec Evidence` (lines 28-34)
5. `## FUT-01 Hand-off Note` (lines 36-44) — retained unchanged, forward-pointing only
6. `## First-Principles Physics Check` (lines 46-50, HTML-comment-gated REQUIRED-for-conflict marker)
7. `## Verdict` (lines 52-62)
8. `## Root-Cause Framework Ambiguity` (lines 64-68, conflict-gated)
9. `## Locked Convention` (lines 70-74, conflict-gated)
10. `## Which Source Was Correct / Wrong` (lines 76-80, conflict-gated)
11. `## Before / After Spec Note` (lines 82-86)
12. `## Named Acceptance Check` (lines 88-92)
13. `## Status Transition Log` (lines 94-102)

**Header verdict-enum row (analog line 11) — copy verbatim (EVID-07, D-04 §6):**
```
| Current Verdict | `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` / `-` |
```

**Source Positions table (analog lines 21-26) — D-04 §2 substitutions (swap issue-01 paths for issue-02):**
```
| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `path §N Q-XX:Lx-Ly` | Summarize the resolution document claim. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `path:Lx-Ly` | Summarize the issue document claim. |
```
Keep the analog's closing line verbatim: "Do not add a primary-source field. Neither source is authoritative before adjudication." Both citations required even for uncontested verdicts (D-04 §2).

**Conditional-section HTML markers (analog lines 48, 66, 72, 78) — copy the pattern, re-key to EVID-10:**
```
<!-- REQUIRED for EVID-10: any finding whose ledger row says `Sources Disagree? = YES`. Optional otherwise. -->
```

**D-04 mandatory ADDITIONS (no v1.4 analog — the one genuinely new sub-block):**
- **New `### Dataset Evidence (§3b)` under `## Spec Evidence`** — DATA-xx / CLM-row citations from `24-VERIFIED-FACTS.md`, line-cited. This is EVID-06's fourth source; v1.4 packets had only three. Do not create a new `##` section for it.
- §10 `## Before / After Spec Note` doubles as the EVID-08 false-positive record: for intentional non-changes, name the spec section, confirm no edit, state why the current convention stands and which source misread it (analog line 86 already has the `accept-resolution as no-change` idiom — extend it).

---

### `evidence/README.md` (config protocol, transform)

**Analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` — adapt section-by-section; enum, lifecycle, regression, phase-exit carry over verbatim except phase numbers.

**Section structure to copy (analog lines 1-108), in order:**
1. `# Evidence Packet Protocol` + intro (lines 1-3)
2. `## Artifact Roles` table (lines 5-13) — re-point `../16-ISSUE-LEDGER.md` → `../../24-.../24-ISSUE-LEDGER.md`
3. `## Primary Sources` (lines 15-24) — swap issue-01 → issue-02 paths; keep "Neither source is authoritative" + "Live code in `pinn/` is NOT in the examination basis" verbatim (SCOPE-10)
4. `## Verdict Enum` table (lines 26-38) — **copy verbatim** (EVID-07 fixed set)
5. `## Status Lifecycle` table (lines 40-54) — **copy verbatim** (the `PENDING/IN_PROGRESS/FIX_APPLIED/VERIFIED/DEFERRED` machine)
6. `## EVID-05 Trigger Table` (lines 56-67) — **rename to EVID-10 Trigger Table**; replace the B-02/B-04/B-09/M5 rows with the v1.5 conflict rows (SCS, D=6.694, M11/M12)
7. `## Regression Policy` (lines 69-75) — copy verbatim except "Phases 17-22, including Phase 20.5" → "Phases 26-28"
8. `## Phase-Exit Rule` (lines 77-82) — copy verbatim except phase numbers
9. `## Acceptance Check IDs` (lines 84-93) — copy the `AC-{REQ-ID}[-{NN}]` policy; note Phase 25 mints NO new AC-IDs (D-13)
10. `## Packet Start Procedure` (lines 95-104) — copy the 7 steps; update step 4 to add the §3b dataset-evidence source; update step 7 ledger path
11. `## Explicit Non-Goals` (lines 105-107) — copy; this phase adds no linter/CI/spec-edit

**Verdict-enum table (analog lines 28-38) — copy verbatim:**
```
| Verdict | Meaning |
|---|---|
| `accept-resolution` | Accept the resolution document's position after independent verification. |
| `accept-issue-doc` | Accept the issue document's position after independent verification. |
| `accept-third-position` | Reject both source positions in favor of an independently justified convention. |
| `reject-both-as-unsupported` | Reject both source positions because neither survives evidence review. |
| `defer-with-blocker` | Defer because evidence is unavailable or a blocker prevents adjudication. |
```

**EVID-10 trigger table (replace analog lines 60-65 rows) — new rows:**
```
| Finding | Topic | Required Flag | Adjudication Requirement |
|---|---|---|---|
| SCS | SCS thresholds vs locked log-drift gate | YES - EVID-10 required | Resolve ratio thresholds (1e-6/1e-8) vs locked `SCS = log10(eps_H)` reject `SCS > -5` gate. |
| D=6.694 | compute_globals D convention | YES - EVID-10 required | Resolve mass-fraction `6.694` vs raw-mass PHYS-01 `D ~ 4.6416`. |
| M11/M12 | severity reclassifications | YES - EVID-10 required | Resolve MAJOR->BLOCKING reclassification against verified-facts arithmetic and process-classification grounds. |
```

**D-03 enforcement encoding to ADD (no verbatim v1.4 line — synthesize from §Regression + §Phase-Exit + Packet Start):**
- No spec edit in Phases 26-28 without a completed packet + verdict for the finding (packet-before-edit, EVID-06).
- Phase-exit gate permits only `VERIFIED` or `DEFERRED` for in-scope findings.
- Ledger status edits travel in the same commit as the underlying change.

**Claude's-discretion ADDITION:** ID→filename map subsection (no v1.4 analog — v1.4 IDs were already filesystem-safe).

---

### `evidence/compute-globals-D.md` (model EVID-10 record, transform)

**Analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-02.md` — **close analog.** Same conflict family: raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` (PHYS-01/HC-6, locked) vs mass-fraction `D = (G·M_tot·T²)^(1/3) = 6.694` (issue-doc). The v1.5 record transcribes the v1.4 verdict structure with issue-02/resolution-02 citations.

**Completed-conflict-packet structure to mirror (analog B-02.md, same 12 `##` headings plus title present):**
- Header with `Current Verdict | accept-resolution` and the status selected by the `GAP-25-02` user resolution (analog lines 9-15) — for Phase 25 the D=6.694 record lands the verdict but the fix remains owned by Phase 27 PIPE-09.
- Source Positions table with full path + line range in BOTH cells (analog lines 19-22) — the citation format is `path:Lx-Ly` for issue, `path §N Q-XX:Lx-Ly` for resolution.
- First-Principles Physics Check derives `G·T²/D³ = 1 ⇒ D³ = G·T²` (analog lines 63-97). For v1.5 this is a *confirmation* of the resolution doc's check, not original derivation (RESEARCH: transcribe-with-grounding).
- Verdict `accept-resolution` with reasoning linked to cited evidence (analog lines 99-106).
- Locked Convention in spec-edit-ready prose (analog lines 114-120) — D-02: stops here, NO edit; Phase 27 PIPE-09 lands it.

**Citation format (analog line 22) to copy:**
```
| `.../issues/01-architecture-and-physics-foundations.md:L72` | Issue doc B-02 frames ... proposes `D = (G * M_tot * T^2)^(1/3) = 6.694`. |
```
For v1.5: cite `02-data-pipeline-and-validation.md:235-275,289,306,317` (issue) and `02-resolution-doc.md §4.4 Q-B4:493-536` (resolution).

**v1.5-specific ADDITIONS over B-02 (from RESEARCH Conflict 2):**
- §3b Dataset evidence: cite `24-VERIFIED-FACTS.md` CLM-13 = PENDING/not-probed; the EVID-10 step formally ratifies CLM-13 (OI-11 caveat, D-15).
- Spec evidence must cite `ctl_instruction.md §2.5 line 598` which *explicitly rejects* the 6.694 form (re-verify line number at authoring; A1).
- Root-cause: issue-doc listing is internally inconsistent (mass-fraction D with raw-mass energies); arithmetic for 6.694 is correct but convention is rejected. `E_scale = 1e-8` canonicalization is a Phase 27 edit decision, NOT a Phase 25 verdict — record in prose only.

---

### `evidence/scs-thresholds.md` (model EVID-10 record, transform)

**Analog:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/B-09.md` (closest conflict packet by shape — a threshold/strategy conflict upholding a locked convention). Use B-02.md's section completeness as the structural template.

**Structure:** same completed-conflict layout as B-02.md: the 12 `##` headings plus title, with `### Dataset Evidence (§3b)` nested under `## Spec Evidence`.

**v1.5-specific content (RESEARCH Conflict 1):**
- Issue-doc position: ratio `SCS > 1e-6` reject / `< 1e-8` Stage 5 — `02-data-pipeline-and-validation.md:129-141`.
- Resolution verdict: accept locked gate verbatim, reject issue-doc numbers — `02-resolution-doc.md §5.1 Q-C1:543-574`.
- **Spec evidence special case:** the locked gate's *sole written home* is read-only `data_quality_assessment.md §3.1` (SI-DQA-003) — citable, NEVER editable (SCOPE-09). The record must note Phase 28 VAL-01 will create a canonical SCS contract in the editable specs (ctl) WITHOUT touching DQA — this is precisely why the root-cause record matters before the edit.
- Root-cause: `1e-6` = dqa Acceptable/Marginal band boundary mis-promoted to a reject gate; `1e-8` has no source anywhere in the package.
- Expected verdict `accept-resolution` (upholds locked gate).

---

### `evidence/m11-m12-severity.md` (model EVID-10 record, transform)

**Analog:** B-02.md structure; this record is partly a *process-classification* ruling rather than a physics conflict.

**v1.5-specific content (RESEARCH Conflict 3):**
- M12: BLOCKING claim falsified on verified arithmetic — `24-VERIFIED-FACTS.md` CLM-10 medians 61/127/1003 (std min 59) ⇒ 32 distinct points trivially feasible. Expected verdict `accept-third-position` / reject-issue-doc-as-posed. Cite `02-resolution-doc.md §4.1 Q-B1:385-422`.
- M11: the resolution doc explicitly *defers the reclassification TO Phase 25* (`§3.3 Q-A3:238`: "whether the MAJOR→BLOCKING reclassification stands is EVID-10's call"). Phase 25 makes this severity ruling explicitly, grounded on the data-integrity argument (resolution §3.3 part 2) — NOT architectural-harm narratives (flagged non-load-bearing). This is the one verdict the source routes to Phase 25.
- Cross-reference `02-resolution-doc.md §6 F-3 (line 740)` defect catalog as supporting evidence (cite in all three records).

---

### `24-ISSUE-LEDGER.md` Lifecycle Rules block (config state index, in-place re-issue)

**Analog:** the file's own §Lifecycle Rules (lines 71-81) + v1.4 README §Regression/§Phase-Exit. D-11 is a **mechanical correction of stale applicability text only.**

**KEEP VERBATIM (do not "improve" — Pitfall 6):**
- State machine: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` (line 73); `DEFERRED` absorbing with written blocker (line 75).
- Audit string: "FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check." (line 77).
- Batch definition: "A batch is one GSD plan (`NN-NN-PLAN.md`)." (line 79).
- Transitive-dependent re-verification + regression demotion to `IN_PROGRESS` (line 79).
- Phase-exit gate: only `VERIFIED`/`DEFERRED` for in-scope findings (line 81).

**CHANGE ONLY (the single stale token):**
```
"Phases 17-22, including Phase 20.5"  →  "Phases 26-28" (spec-edit phases) + Phase 29 (acceptance)
```
Occurs in the §Regression sentence (line 79). Note the change in the ledger's Notes section. Nothing else in the block changes.

**Operating edits (D-06) — pattern for status transitions during 26-28:** per-finding log entry format `date commit-audit-label status->status (actor/plan)` (B-02.md analog lines 146-150; ledger lines 100-101). Ledger status edit travels in the same commit as the underlying change (Pitfall 5). For Phase 25 verdict-only records, status wording is blocked on `GAP-25-02`.

## Shared Patterns

### Four-source EVID-06 citation (every packet)
**Source:** RESEARCH "Source Materials Map" + analog B-02.md §Source Positions/§Spec Evidence.
**Apply to:** all three EVID-10 records.
**Pattern:** cite all four sources by path + section/line range, never whole files:
1. Issue doc `pinn_instruction/issues/02-data-pipeline-and-validation.md:Lx-Ly`
2. Resolution doc `.../02-resolution-doc.md §N Q-XX:Lx-Ly`
3. Framework specs `ctl_instruction.md` / `pinn_architecture.md` / read-only `data_quality_assessment.md` line ranges
4. **NEW §3b** `24-VERIFIED-FACTS.md` CLM-row citations

### Directory-qualified IDs (ID-namespace collision guard)
**Source:** CONTEXT specifics; RESEARCH Runtime State Inventory.
**Apply to:** every cross-document citation in all records and README.
**Pattern:** issue-01 (v1.4) and issue-02 (v1.5) both reuse IDs like `B-06`. No path collision (separate `evidence/` dirs) but cite-time confusion is possible — always directory-qualify so a v1.5 packet is never confused with its v1.4 namesake.

### Status-edit-in-commit + transition-log format
**Source:** v1.4 README §Status Lifecycle (lines 52-54); B-02.md §Status Transition Log (lines 144-150).
**Apply to:** ledger + every record that changes status.
**Pattern:** `YYYY-MM-DD <pending-commit-sha> STATUS -> STATUS (Phase NN PXX by actor)` or an already-known durable audit label such as the existing ledger's `SEED_SHA`; mirror in ledger in the same commit. Do not claim the final commit's own SHA inside the commit contents, because amending a file to contain that SHA changes the SHA. Record the final short SHA in the plan summary / git history after commit.

### Candidate-source-is-not-the-verdict grounding
**Source:** CONTEXT D-09; RESEARCH Pitfall 2.
**Apply to:** all three EVID-10 records.
**Pattern:** the resolution doc is the *candidate* verdict source. Transcribe its verdict only after independent confirmation against spec lines + CLM rows + a short first-principles check (e.g., `D³ = GT²` ⇒ 4.6416; `32 ≤ 59` for M12). An outcome that would overturn a locked convention (PHYS-01/HC-5/HC-6) is a STOP gap in `25-GAPS.md`, never an autonomous verdict. Where the source is silent/hedged (Open Items register §756-779, OI-7) → `defer-with-blocker` or STOP gap, never invention.

## No Analog Found

None. Every Phase 25 artifact maps to a committed v1.4 Phase 16 precedent or an in-place edit of a Phase 24 deliverable. The only genuinely new *content* (not structure) is:
- The §3b Dataset-evidence section (no v1.4 analog — v1.4 had three sources, not four).
- The ID→filename map subsection in README (v1.4 IDs were already filesystem-safe).
Both attach to existing analog structures; no new schema is invented.

## Metadata

**Analog search scope:** `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/` (template, README, 19 completed packets); `.planning/phases/24-.../24-ISSUE-LEDGER.md` (seeded ledger).
**Files scanned:** 5 read directly (`_TEMPLATE.md`, `README.md`, `B-02.md`, ledger Lifecycle block, ledger finding table); 19 packet inventory listed.
**Pattern extraction date:** 2026-06-11
