# Phase 45: trainex-r2 ERW Package Assembly - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `45-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-07-23
**Phase:** 45-trainex-r2-erw-package-assembly
**Mode:** `--all --auto` — all gray areas auto-selected; recommended option taken for each without user
prompting (owner delegated selection to agent judgement this session). Single pass (auto-mode cap).
**Areas discussed:** Package structure, Attachment set (5-cap), Claims-register location, Output
contract / channel standing, Research-question framing, Provenance / commit-pin, Claims-register
construction, Delivery note, Upload self-containment, Carried-forward todos.

---

## Package structure (single vs split sub-package)

| Option | Description | Selected |
|--------|-------------|----------|
| Single sub-package | One `research_package/` with one master + prompt; five questions share one output contract and one centerpiece | ✓ |
| Split (a/b) | Two parallel sub-packages by output contract (trainex-r1 precedent) | |

**Auto-selected:** Single. **Rationale:** PKG-10 names exactly 5 questions; ERW Rule 10 splits only
above ~6–7 work items. → D-01.

---

## Attachment set under the 5-cap (ERW Rule 15)

| Option | Description | Selected |
|--------|-------------|----------|
| 4 bundled uploads | master + 44-DIAGNOSIS + framework-specs-bundle + run-evidence-bundle (1 slot headroom) | ✓ |
| One file per source | ships >5 individual attachments — violates the hard cap | |
| Split into more attachments to fit | prohibited by Rule 15 ("bundle — do not split into more attachments") | |

**Auto-selected:** 4 bundled uploads. **Rationale:** Rule 15 hard cap = 5; specs count when uploaded,
so bundle to one; evidence bundled to one. → D-02.

---

## Claims-register location

| Option | Description | Selected |
|--------|-------------|----------|
| Section in master + standalone file (not uploaded) | guaranteed seen by the agent; costs no cap slot | ✓ |
| Separate 5th upload | prominent but spends a cap slot | |

**Auto-selected:** In master + standalone. → D-03.

---

## Output contract / channel standing (build-design vs specwork)

| Option | Description | Selected |
|--------|-------------|----------|
| Specwork-style neutral (no recommended answer) | framed questions → candidate verdict source | ✓ |
| Build-design (options menus + decision sheet, "suggest defaults; never decide") | trainex-r1 contract | |

**Auto-selected:** Specwork-style neutral. **Rationale:** PKG-10 mandates "no recommended answer,
v1.5/v1.6 precedent"; PKG-11 returns a candidate verdict source. Despite the build-design directory
path, the output contract is specwork. **Non-discretionary** (grounded in PKG-10). → D-04.

---

## Research-question framing (PKG-10)

| Option | Description | Selected |
|--------|-------------|----------|
| Exactly 5 PKG-10 areas, cross-linked to DIAG-04 candidates as [HYP] context | budget/steps; warmup+LR; loss weighting (with normalization sub-facet); Stage-0 pacing; evaluation-policy | ✓ |
| Expand to a question per DIAG-04 candidate (6+) | would exceed the named PKG-10 set and invite a split | |

**Auto-selected:** Exactly 5, normalization/data-scale folded as a sub-facet of loss weighting. → D-05,
D-06.

---

## Provenance / commit-pin (ERW Rule 5)

| Option | Description | Selected |
|--------|-------------|----------|
| Single `source_baseline` = assembly-time HEAD | all sources already committed by then; preserve the diagnosis's own evidence git_head as a complementary note | ✓ |
| Per-source pins | more granular but redundant since all land in one history | |

**Auto-selected:** Single assembly-HEAD baseline. → D-07, D-08.

---

## Claims-register construction (PKG-11)

| Option | Description | Selected |
|--------|-------------|----------|
| Lift the [FACT]/[HYP] tags already in 44-DIAGNOSIS.md | facts = cited v2.0 numbers; hyps = DIAG-04 rankings, labeled agent analysis | ✓ |
| Re-derive a fresh register | needless rework; diagnosis was authored for this lift | |

**Auto-selected:** Direct lift. → D-09.

---

## Delivery note (PKG-11)

| Option | Description | Selected |
|--------|-------------|----------|
| trainex-r1 DELIVERY-NOTE structure, adapted to single package | contents, provenance, return format (reports → consolidated resolution doc), landing paths, standing, todo questions | ✓ |

**Auto-selected:** trainex-r1 structure adapted. → D-10.

---

## Upload self-containment (ERW Rules 1–2)

| Option | Description | Selected |
|--------|-------------|----------|
| Zero repo paths in uploads; bare filenames; "attached files only" | reviewer greps uploads for `/`, `.planning`, `runs/` before delivery | ✓ |

**Auto-selected:** Self-contained uploads. → D-11, D-12.

---

## Carried-forward todos (Success Criterion 4)

| Option | Description | Selected |
|--------|-------------|----------|
| Surface to owner as package-scope questions at assembly; agent does not decide | overrides the `--auto` score≥0.4 auto-fold | ✓ |
| Auto-fold into scope (score 0.6 ≥ 0.4) | would contradict the locked success criterion — REJECTED | |

**Auto-selected:** Surface, do not decide. **Non-discretionary** (Success Criterion 4 + SCOPE-26). → D-13.

---

## Claude's Discretion

All decisions were auto-selected under `--auto` (owner delegated selection to agent judgement).
Every decision is a structural / presentation / process choice, safe for the planner to refine on
evidence — **except D-04** (neutral no-recommendation contract, required by PKG-10) and **D-13** (the
two todos are owner-decided, surfaced not decided, per Success Criterion 4). Neither is discretionary.

## Deferred Ideas

- Remedy selection / recommendation (SCOPE-26 — owner-adjudicated later).
- Running any discriminating test (SCOPE-23 — posed as questions only).
- A new held-out evaluation (SCOPE-22 — the evaluation-policy question asks about a future one).
- Framework-spec edits (SCOPE-24 — snapshots are read-only).
- Consolidation of returned results (happens at delivery, after external research returns).
</content>
