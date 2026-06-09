# Phase 16: Evidence Framework and Issue Adjudication - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-15
**Phase:** 16-Evidence Framework and Issue Adjudication
**Mode:** `--all --auto` (all gray areas auto-selected; recommended option auto-picked per area in a single pass — no interactive AskUserQuestion calls)
**Areas discussed:** Ledger directory path, Ledger schema, Evidence packet location, Evidence packet template, Finding inventory, EVID-05 trigger and storage, VER-05 lifecycle and regression policy, Acceptance check naming, VER-02 traceability artifact, "Neither source authoritative" operationalization, Phase 16 deliverables list

---

## Ledger directory path reconciliation

| Option | Description | Selected |
|--------|-------------|----------|
| A | Canonical path is `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (matches actual phase slug). Update ROADMAP/REQUIREMENTS/PROJECT references to match. | ✓ |
| B | Honor the literal path `.planning/milestones/v1.4-phases/16-evidence-framework/` referenced in ROADMAP — create a second phase directory. | |
| C | Place the ledger at `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/ledger/16-ISSUE-LEDGER.md`. | |

**User's choice:** A (auto-selected, recommended).
**Notes:** Two phase directories for one phase produces silent drift. Reconcile by edits to the three upstream planning docs in the Phase 16 plan.

---

## Ledger schema and file layout

| Option | Description | Selected |
|--------|-------------|----------|
| A | Single Markdown file: status table at top + per-finding H3 subsections + YAML frontmatter for counts/traceability. | ✓ |
| B | YAML frontmatter + per-finding sections only (no status table). | |
| C | Per-finding JSON files + ISSUE-LEDGER.md summary table. | |

**User's choice:** A.
**Notes:** Status table is greppable and renders cleanly in markdown viewers; subsections hold prose that does not fit the table; frontmatter carries machine-readable counts. Matches existing planning-doc conventions.

---

## Evidence packet location and granularity

| Option | Description | Selected |
|--------|-------------|----------|
| A | One file per finding under `evidence/{finding-id}.md`. | ✓ |
| B | One consolidated `EVIDENCE-PACKETS.md` with all findings as subsections. | |
| C | Inside `16-ISSUE-LEDGER.md` per-finding subsections (no separate evidence/ directory). | |

**User's choice:** A.
**Notes:** Per-finding files isolate contested adjudications and avoid one giant file. Grep-friendly. Phase 9's pattern (thematic .md files + README.md + MIGRATION.md) supports the precedent.

---

## Evidence packet template (fixed schema)

| Option | Description | Selected |
|--------|-------------|----------|
| A | Fixed 12-section schema (header, both source positions, spec evidence, code evidence, first-principles check, verdict, root-cause, locked convention, source correctness, before/after note, acceptance check, transition log). EVID-05-specific sections marked conditional. | ✓ |
| B | Free-form prose with required headings only (verdict, evidence, rationale). | |
| C | YAML-frontmatter-only packets (table-style metadata). | |

**User's choice:** A.
**Notes:** A is strict enough to enforce EVID-01..05 without being so heavy it discourages packet creation. Conditional sections (first-principles check, root-cause ambiguity, locked convention, source correctness) are required only for EVID-05 contested findings to keep simple verdicts cheap to record.

---

## Initial finding inventory (seed for the ledger)

| Option | Description | Selected |
|--------|-------------|----------|
| A | Seed ledger with B-01..B-10 + B-11 (folded into B-05) + M1..M5, M8, M9, M10 active; M6, M7 DEFERRED with VER-03 blocker text. | ✓ |
| B | Seed ledger only with the four contested findings (B-02, B-04, B-09, M5); other findings added by Phases 17–21. | |
| C | Seed ledger with every finding ID mentioned anywhere in either source (broader net, more rows). | |

**User's choice:** A.
**Notes:** A matches REQUIREMENTS.md/ROADMAP.md scope, keeps Phases 17–21 working against a known surface, and respects VER-03's M6/M7 deferral. B-11 from the issue doc's cross-issue interactions is folded into B-05 (both COM/mass) with an explicit note rather than a separate row.

---

## EVID-05 trigger conditions and storage

| Option | Description | Selected |
|--------|-------------|----------|
| A | Trigger when (a) the two source docs give different verdicts OR (b) either source contradicts current framework-spec convention. Adjudication record lives inside the same per-finding evidence packet under conditional sections. | ✓ |
| B | Trigger only on explicit source-doc verdict disagreement; ignore spec contradictions. | |
| C | Always run full EVID-05 for every finding regardless of agreement (uniform but expensive). | |

**User's choice:** A.
**Notes:** Condition (b) catches cases where both source docs are wrong about a current spec convention — explicitly within the v1.4 "neither authoritative" rule. Single home for adjudication records (no separate ADJUDICATIONS.md).

---

## VER-05 status transitions and batch regression policy

| Option | Description | Selected |
|--------|-------------|----------|
| A | Strict enum `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` + `DEFERRED`. Each row carries `Dependents:` seeded from `ctl_pinn_resolution.md` §"Cross-Issue Interactions". After each batch, re-run acceptance checks for transitive dependents of edited findings. Phase exit blocks on any in-scope finding not at `VERIFIED`/`DEFERRED`. | ✓ |
| B | Same enum but re-run EVERY previously verified finding's check after every batch (safe but expensive). | |
| C | Heuristic regression detection via file/section diff (auto, but error-prone). | |

**User's choice:** A.
**Notes:** Explicit dependency map is cheap to maintain, transparent in review, and lets Phase 17–21 reviewers see at a glance what risks regressing. Phase 16 transcribes the cross-issue table; later phases append.

---

## Acceptance check naming policy

| Option | Description | Selected |
|--------|-------------|----------|
| A | Reserve `AC-{REQ-ID}[-{NN}]` names in Phase 16. Pass criteria + runnable command + data fixture defined in Phase 21 per VER-01. | ✓ |
| B | Define checks fully in Phase 16 (overlaps Phase 21/VER-01 scope). | |
| C | No naming in Phase 16; Phase 21 picks names freely. | |

**User's choice:** A.
**Notes:** Reserving names early lets Phases 17–20 cite a stable AC-ID in their packets and ledger rows. Definition stays in Phase 21 where it belongs.

---

## VER-02 traceability artifact

| Option | Description | Selected |
|--------|-------------|----------|
| A | No separate file. Ledger frontmatter carries the verification statement; REQUIREMENTS.md §Traceability remains source of truth. | ✓ |
| B | New `TRACEABILITY.md` duplicating the requirements→phase table. | |
| C | Embed verification statement inline in PROJECT.md "Validated". | |

**User's choice:** A.
**Notes:** Duplicating the table invites drift. The frontmatter statement plus a Phase 16 verification commit is enough evidence for VER-02 without creating two sources of truth.

---

## "Neither source authoritative" operationalization

| Option | Description | Selected |
|--------|-------------|----------|
| A | Evidence-packet template enforces side-by-side citation of BOTH source docs before any verdict; no "primary source" field in the template. `master_consolidation_report.md` and per-model reports are supporting evidence, cite-when-useful. | ✓ |
| B | Designate one source as "primary" per finding via a template field; agent justifies the choice. | |
| C | Loose convention only — no template enforcement. | |

**User's choice:** A.
**Notes:** Template-level enforcement makes the v1.4 milestone's central rule operational rather than aspirational. EVID-05 sections in the template hold the conflict-adjudication record when verdicts disagree.

---

## Phase 16 deliverables list

| Option | Description | Selected |
|--------|-------------|----------|
| A | Ledger + evidence/README.md + evidence/_TEMPLATE.md + 3 path-reconciliation doc edits + standard GSD artifacts. No spec/code edits, no adjudication records. | ✓ |
| B | Same as A but also includes seeded evidence packets for the four contested findings (B-02, B-04, B-09, M5) without verdicts — just source quotes preloaded. | |
| C | Same as A but also includes a draft of Phase 21's executable acceptance-check suite skeleton. | |

**User's choice:** A.
**Notes:** Seeding packets without verdicts (B) was tempting but blurs the line between Phase 16 (framework) and Phases 17–20 (apply framework). Adjudication and source-quote selection belong to the phase doing the work. C overlaps Phase 21.

---

## Claude's Discretion

- Exact column ordering in the ledger table within the columns defined in D-02.
- Exact YAML key ordering in the ledger frontmatter within the keys defined in D-03.
- Whether to use `<details>` collapse blocks for per-finding subsections in `16-ISSUE-LEDGER.md` if the file grows long.
- Subsection ordering within `evidence/_TEMPLATE.md` within the 12 required sections per D-06.
- Exact phrasing of the M6/M7 deferral blocker text (substance fixed by VER-03; wording flexible).

## Deferred Ideas

- Ledger linter / CI check validating verdict and status enums — future tooling, not v1.4 requirement.
- Auto-generated traceability table from REQUIREMENTS.md — defer until drift is shown to be a real problem.
- Cross-issue dependency graph visualization (e.g., graphviz) — `Dependents:` field is sufficient for VER-05.
- Physical migration of `master_consolidation_report.md` into a `supporting/` subdirectory to match its demoted status — out of Phase 16 scope.
- Acceptance check executable suite — Phase 21 (VER-01/VER-04) territory.
- Re-opening M6/M7 with new source material — explicitly deferred per VER-03; addendum allowed but no status change without milestone-level approval.

## Scope-creep redirects (none triggered)

No suggestions during this auto-pass would have expanded scope beyond Phase 16's framework deliverable. The four contested findings stayed flagged for downstream adjudication, not adjudicated here. Spec/code edits stayed out. Acceptance check definition stayed in Phase 21.
