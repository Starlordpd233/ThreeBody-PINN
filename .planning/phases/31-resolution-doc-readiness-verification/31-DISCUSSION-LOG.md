# Phase 31: Resolution Doc Readiness Verification - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-20
**Phase:** 31-resolution-doc-readiness-verification
**Mode:** `--auto --all` — all gray areas auto-selected; Claude chose the recommended (grounded) option per question without interactive ratification. Every selected option is grounded in `31-SPEC.md` + the **verified** v1.5 Phase 24.5 analog; no source-silent semantic decision arose (STOP protocol recorded no gap).
**Areas discussed:** Plan decomposition, Report/map markdown, Line-range capture method, Four-check task order

---

## Plan decomposition

| Option | Description | Selected |
|--------|-------------|----------|
| Single plan, single wave (7 tasks) | One `31-01-PLAN.md` mirroring the analog `24.5-01-PLAN.md`; the four checks are independent reads of one doc | ✓ |
| Multiple plans / wave fan-out | Split the checks across parallel plans | |

**Auto-selected choice:** Single plan, single wave (D-01).
**Notes:** `[auto]` Phase 31 is a lightweight single-agent read-and-check pass with no probe authoring and no spec edits; the verified analog used a single 7-task plan. Wave parallelization adds coordination cost with no benefit. Grounded in `24.5-PLAN.md`.

---

## Report/map markdown (SPEC "Next step" item 1)

| Option | Description | Selected |
|--------|-------------|----------|
| Model on the verified v1.5 24.5 analog | Reuse `24.5-READINESS-REPORT.md` / `24.5-RESOLUTION-MAP.md` section structure, adapted to 18 findings + §0–§7 doc structure | ✓ |
| Invent a fresh report/map schema | Design new section layouts from the SPEC R6/R7 field lists alone | |

**Auto-selected choice:** Model on the verified analog (D-02, D-03, D-04, D-05).
**Notes:** `[auto]` The *schema* (which sections/fields/pass-criteria each deliverable carries) is already fixed by SPEC R6/R7 and the verified analog — so this settles rendering only, not a new process-artifact schema. Modeling on the user-accepted, `24.5-VERIFICATION.md`-PASSED precedent *grounds* the markdown rather than inventing it (governance-compliant). The gate-verdict precedence (D-05) is fixed by SPEC R7, not a discretion item. **Inventing a fresh schema was rejected** — it would be an un-grounded process-artifact-schema decision (MUST-surface under the STOP protocol) when a verified precedent exists.

---

## Line-range capture method (SPEC "Next step" item 2)

| Option | Description | Selected |
|--------|-------------|----------|
| Capture from committed doc, anchor to revision; §/ID anchors stable | `grep -n`/line-numbered read of §0–§7 / §1.1–§1.18 headers; record byte count + commit/date; §/finding-ID is the stable citation key | ✓ |
| Line numbers as the primary citation key | Cite by raw line number without a revision anchor | |

**Auto-selected choice:** Revision-anchored ranges with §/finding-ID as the stable key (D-06, D-07).
**Notes:** `[auto]` SPEC R6 fixes this: line ranges are anchored to the committed revision (byte count + date); §/finding-ID anchors survive re-pagination, line numbers do not. On `NOT-READY` re-delivery only the line ranges refresh (affected-only re-check). The exact grep/read mechanism is Claude's discretion. Grounded in `24.5-RESOLUTION-MAP.md` §3 citation guide.

---

## Four-check task order (SPEC "Next step" item 3)

| Option | Description | Selected |
|--------|-------------|----------|
| Dependency-ordered (analog 7-task sequence) | gate → structural → crosswalk → consistency → compliance → map → report → gate-decision | ✓ |
| Arbitrary / parallel check order | Run R2–R5 in any order or concurrently | |

**Auto-selected choice:** Dependency-ordered, matching the analog (D-08).
**Notes:** `[auto]` Order is derivable from data dependencies: the pre-exec gate STOPs before any check on a stub/empty doc or missing Phase-30 marker; R2 (structural) precedes R3–R5 because an incoherent doc makes the crosswalk meaningless; R3–R5 are independent and run in SPEC order; the map (R6) consumes the crosswalk (R3); the report (R7) consolidates R2–R5; the gate decision + STATE/ROADMAP update closes. Matches `24.5-PLAN.md` Tasks 1–7.

---

## Claude's Discretion

- Exact column headers, table-vs-bullet rendering, and heading capitalization **within** each deliverable's fixed section set (analog headers are the recommended default).
- The precise grep/read mechanism for line-range capture (any method yielding revision-anchored ranges).
- Whether per-check detail tables are inline under report §3 or in labeled subsections (recommended: inline, per the analog).

## Deferred Ideas

- Adjudicating D-04 / D-05 / D-06 and the `D = 6.694` conflict → Phase 32 (EVID-15); Phase 31 only confirms-present-and-flags.
- Re-measuring / empirically verifying any dataset figure → FUT / trainex (no Phase-24 analog in v1.6).
- Editing the resolution doc to close a gap → routed to the external consolidation agent; Phase 31 never edits the doc.
- **Reviewed-not-folded:** the trainex-r1 research-handoff todo (score 0.6) — cross-track (trainex build-design, not specwork/doc-03); auto-fold suppressed to preserve the locked phase boundary (same call Phase 30 made).
