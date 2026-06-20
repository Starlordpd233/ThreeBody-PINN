# Phase 31: Resolution Doc Readiness Verification — Specification

**Created:** 2026-06-20
**Ambiguity score:** 0.09 (gate: ≤ 0.20)
**Requirements:** 8 locked
**Branch:** `milestone/v1.6` (specwork worktree)

## Goal

Produce a pass/fail readiness verdict on the landed issue-03 resolution doc
(`03-final-resolution.md`) — confirming all **18 selected findings** are covered, **zero**
v1.5-verified dataset facts are contradicted, and **zero** locked v1.4/v1.5 conventions are
violated — plus a standalone quick-reference map, so that Phases 32–36 are either **unblocked**
(`READY` / `READY-WITH-CAVEATS`) or **held** with routed fix instructions (`NOT-READY`). Phase 31
verifies and maps the candidate verdict source; it adjudicates nothing.

## Background

Phase 31 is the operational readiness gate between the external research and the adjudication
phases — the **v1.5 Phase 24.5 analog** (operational, 0 requirement IDs). Grounded in the
`milestone/v1.6` specwork worktree:

- **The subject has landed.** The consolidated resolution doc is present at
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
  (282 lines, 48,049 bytes). It has a citable structure: §0 adjudication method; §1.1–§1.18 one
  subsection per finding with verdict tags (`surface_to_user` for the three human-approval
  decisions D-04/D-05/D-06; `modified` / `accepted` / `rejected` / `defer` for the rest); §2 claim
  matrix; §3 disagreement register; §4 gap register; §5 source-coverage checklist; §6
  non-independent-input note; §7 deliverable index.
- **Phase 30 is COMPLETE** (5/5 plans, `30-VERIFICATION.md` PASSED); the external resolution-doc
  gate opened on its delivery.
- **The deliverable shapes are fixed by the analog:** `24.5-READINESS-REPORT.md` (exec-summary
  verdict, pre-exec gate, four checks, gap list, fix instructions, re-check protocol, gate
  decision) and `24.5-RESOLUTION-MAP.md` (section index, finding→section mapping, citation guide,
  verdict-direction preview, out-of-scope forward refs, open-items carry-forward). Phase 31
  produces the v1.6 equivalents: `31-READINESS-REPORT.md` and `31-RESOLUTION-MAP.md`.
- **One structural difference from v1.5:** v1.6 has **no Phase-24 analog** — no in-milestone
  empirical verification phase. The "v1.5-verified dataset facts" the consistency check runs
  against are the **archived v1.5** register
  `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`
  (CLM-01..13 + DATA-05), the only in-repo verified-facts source. The issue ledger is built later
  (Phase 32), so the crosswalk uses the ROADMAP-enumerated selected-finding set, not a pre-built
  ledger.

## Requirements

1. **Pre-execution gate**: Before any check runs, both gate conditions are confirmed and recorded.
   - Current: No gate check exists; the doc has landed and Phase 30 is COMPLETE-verified.
   - Target: A recorded two-condition pre-exec gate at the top of the readiness report —
     (a) the canonical resolution doc `research_result/03-final-resolution.md` exists, is
     non-empty, and is not a stub/placeholder; (b) Phase 30 is COMPLETE in STATE.md. If either
     fails, STOP and surface to the user; do not proceed with partial artifacts. If the doc-03
     directory holds more than one candidate doc, `research_result/03-final-resolution.md` is the
     canonical subject (per the DELIVERY-NOTE landing path); other files are ignored.
   - Acceptance: The readiness report records both gate conditions as PASS with evidence (path +
     byte count for (a); STATE Phase-30-complete citation for (b)); a stub/empty doc or a missing
     Phase-30-complete marker yields a STOP, not a partial run.

2. **Presence and structural check**: The resolution doc is a single coherent, line-range-citable
   document covering each major topic area.
   - Current: The doc has a §0–§7 structure with §1.1–§1.18 per-finding subsections.
   - Target: A `PASS` / `FAIL` result on: the doc exists, is non-empty, and is a single coherent
     document (not a raw concatenation of independent agent outputs); has numbered/labeled
     sections citable by line range (Phase 32 evidence packets require line-range citations per
     EVID-11); and has identifiable sections for the four v1.6 topic areas — curriculum-stage,
     training-loop/batch-construction, loss/energy, and the human-approval decisions.
   - Acceptance: The readiness report records the Task-1 result as `PASS` or `FAIL` with the
     section inventory as evidence; a doc that is a raw concatenation (e.g. duplicate/competing
     top-level section numbering, an unresolved §6-flagged non-independence that breaks coherence)
     is recorded `FAIL` with the reason.

3. **Finding-coverage crosswalk**: Every finding in the selected set maps to a resolution-doc
   section with an explicit coverage status.
   - Current: No crosswalk exists; the doc covers the findings across §1.1–§1.18.
   - Target: A crosswalk table mapping each of the **18 selected findings** — the 15 ROADMAP-SC1
     findings (B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12, NS-13, NS-18, D-04, D-05, D-06,
     `D = 6.694`) **plus** the 3 extras the contract phases consume (adaptive stage assignment
     §1.15 → CURR-01; `L_max`/`tau_L` formulas §1.17 → CURR-02; ALM `mu_p` clamp §1.18 → LOOP-05)
     — to its resolution-doc section(s), with coverage status `covered` / `partial` / `silent`.
     Matching is by finding **identity**, not literal heading text (e.g. the doc's
     "componentwise automatic differentiation" §1.12 = NS-12; "Causal-training mode" §1.1 = D-04);
     a finding may map to more than one section and a section may cover more than one finding —
     the crosswalk records the actual mapping rather than assuming 1:1. A `surface_to_user` verdict
     (the three human-approval decisions) is recorded `covered` as a routed human-approval decision;
     a `defer` verdict is recorded `covered`-with-routing — **neither is `silent`**. A
     section that exists but states no actual position is `partial`.
   - Acceptance: The crosswalk maps all 18 findings to a section + coverage status; every `partial`
     or `silent` row is flagged as a gap; `surface_to_user` / `defer` rows are recorded as
     covered-with-caveat, not gaps; no selected finding is omitted from the table.

4. **Dataset-figure consistency check**: The doc contradicts no v1.5-verified dataset fact.
   - Current: No consistency check exists; v1.6 has no in-milestone verification phase.
   - Target: For each dataset figure the doc states that maps to a row in the archived v1.5
     `24-VERIFIED-FACTS.md` register, record `consistent? yes/no`. A figure that **contradicts** a
     verified fact fails the check; a figure that agrees within the verified fact's stated
     rounding/precision (e.g. doc `~2,565` vs verified `~2,565`) is consistent; a figure v1.5
     **never verified** is recorded as an unverified ("claimed") caveat flagged for FUT — **not a
     failure**. If the doc states no figure that maps to a verified fact, the check passes
     vacuously (0 contradictions), recorded explicitly.
   - Acceptance: The consistency table lists each doc figure that maps to a verified fact with a
     `consistent? yes/no` verdict applying the within-stated-precision rule; the check passes iff
     0 contradictions; non-contradicting unverified figures are listed as caveats, not failures;
     a zero-mapped-figure outcome is recorded as a vacuous pass.

5. **Locked-convention compliance**: The doc commits zero violations of the locked v1.4 + v1.5
   conventions (SCOPE-12).
   - Current: No compliance check exists; the doc §1.16 upholds raw-mass `D ≈ 4.6416` and rejects
     `6.694`.
   - Target: A compliance table over the locked conventions — 14D input `[τ, IC₁₃]`, Jacobi IC₁₃,
     mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, post-v1.3 SCS gate
     (`ε_H > 10⁻⁵` / `SCS > −5`), PHYS-01 raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` (`D = 6.694`
     rejected), and the v1.5 data-side contracts PIPE-01..10 / VAL-01..04 — each marked
     `compliant? yes/no`. A recommendation to **change** a locked convention is a recorded **scope
     observation** (surfaced to the user, not a failure); a silent assumption that **breaches** one
     is a **violation**. Phase 31 confirms compliance only; it does **not** re-adjudicate the
     `D = 6.694` conflict (that is Phase 32 / EVID-15).
   - Acceptance: The compliance table marks each convention `compliant? yes/no`; the check passes
     iff 0 violations; any scope observation is recorded separately and surfaced to the user
     (never counted as a failure and never silently auto-passed); no re-adjudication of any locked
     convention appears in the Phase 31 artifacts.

6. **Resolution-doc quick-reference map**: A standalone `31-RESOLUTION-MAP.md` lets Phase 32 begin
   evidence-packet construction without reading the full resolution doc first.
   - Current: No map exists; Phase 32 would otherwise reverse-engineer the doc's organization.
   - Target: `31-RESOLUTION-MAP.md` containing — a section index (with line ranges); the
     finding→section mapping over all 18 findings (from R3); a citation guide giving the verbatim
     file path, §/finding-ID anchors, and a concrete line-range example for EVID-11; a one-word
     verdict-direction preview per finding; out-of-scope / forward-reference notes; and an
     open-items carry-forward drawn from the doc's own §4 gap register and §6 non-independent-input
     note. Line ranges are anchored to the committed revision (byte count + date); §/finding-ID
     anchors are stable across re-pagination, line numbers are not.
   - Acceptance: `31-RESOLUTION-MAP.md` exists with every listed sub-section present; the
     finding→section mapping covers all 18 findings; the citation guide gives a concrete
     `…/03-final-resolution.md:START–END` example and names the revision the line numbers anchor to.

7. **Readiness report and gate decision**: A `31-READINESS-REPORT.md` consolidates the checks into
   one gate verdict with fix-routing.
   - Current: No report exists.
   - Target: `31-READINESS-REPORT.md` carrying — an executive-summary verdict from
     `READY` / `READY-WITH-CAVEATS` / `NOT-READY`; the four check results (R2–R5); a gap list; fix
     instructions (if any gap); a re-check protocol; and the gate decision. The verdict follows a
     fixed precedence: **any** `NOT-READY` trigger — a `silent` finding, a contradiction of a
     v1.5-verified fact, or a locked-convention violation — yields `NOT-READY` regardless of how
     many checks pass; absent any trigger, **any** caveat (`surface_to_user` / `defer` rows,
     non-contradicting unverified figures, scope observations, the §6 non-independence note) yields
     `READY-WITH-CAVEATS`; an all-clean result yields `READY`. If `NOT-READY`, specific fix
     instructions are routed to the external consolidation agent via the report and Phases 32–36
     remain blocked until the fix lands and an **affected-only** re-check passes (re-run only the
     checks the change could affect; refresh the map's line ranges on re-pagination).
   - Acceptance: The report carries the exec-summary verdict, the four check results, the gap list,
     fix instructions for every gap (if any), the re-check protocol, and the gate decision; the
     verdict is derivable from the check tables by the stated precedence; the STATE/ROADMAP gate
     state is updated to reflect the outcome (via gsd-tools handlers, not direct STATE edits).

8. **Phase boundary and governance**: Phase 31 produces only the two reports and crosses no
   adjudication or edit boundary.
   - Current: No Phase 31 artifacts exist.
   - Target: Phase 31 adjudicates nothing, assigns no finding verdict, edits no framework spec
     (`ctl_instruction.md` / `pinn_architecture.md`), edits no resolution doc, touches no `pinn/`
     file, and invents no coverage or verdict where the doc is silent — a `silent` finding is
     always reported as a gap, never filled. Source-silent semantic / process-schema / cross-phase
     decisions encountered during execution are surfaced as STOP-protocol gaps in
     `31-GAPS.md` + the milestone index `.planning/milestones/v1.6-GAPS.md` (create on first gap),
     never invented.
   - Acceptance: `git diff` for the Phase 31 commit shows zero changes to `ctl_instruction.md`,
     `pinn_architecture.md`, the resolution doc, or any `pinn/` path; no finding carries a Phase 31
     verdict (coverage status only); every selected finding the doc is silent on appears as a gap
     row, never as an inferred verdict.

## Boundaries

**In scope:**
- The two deliverables: `31-READINESS-REPORT.md` and `31-RESOLUTION-MAP.md`.
- The pre-execution gate (doc-present-and-canonical + Phase-30-complete).
- The four readiness checks: presence/structural; finding-coverage crosswalk (18 findings);
  dataset-figure consistency vs the archived v1.5 verified-facts register; locked v1.4 + v1.5
  convention compliance.
- The gate decision (`READY` / `READY-WITH-CAVEATS` / `NOT-READY`) with fix-routing and an
  affected-only re-check protocol.
- The STATE/ROADMAP gate-state update reflecting the outcome (via gsd-tools handlers).

**Out of scope:**
- **Adjudication, verdicts, evidence packets, root-cause conflict resolution** — Phases 32–36;
  Phase 31 checks coverage/consistency, it does not assign verdicts. The doc's three
  `surface_to_user` decisions (D-04/D-05/D-06) are confirmed-present-and-flagged here and
  **adjudicated in Phase 32 (EVID-15)**, not decided in Phase 31.
- **Editing `ctl_instruction.md` / `pinn_architecture.md`** — the spec-edit phases are 33–35.
- **Editing or re-writing the resolution doc** — it is the user's external product; Phase 31 only
  reads and maps it, and (if `NOT-READY`) routes fix instructions to the consolidation agent.
- **Empirical verification of any dataset figure** — v1.6 has no Phase-24 analog; figures are
  checked only for *contradiction* of already-v1.5-verified facts, never re-measured. Re-measuring
  is FUT (FUT-01/02/04).
- **Re-opening or re-adjudicating any locked v1.4/v1.5 convention** (e.g. `D = 6.694`) — SCOPE-12
  hard constraint; only Phase 32 EVID-15 may revisit one, and only with new first-principles
  evidence surfaced as a gap.
- **Running formula-sanity probes against `pinn/`** — SCOPE-15 probes belong to the contract /
  acceptance phases (33–36); Phase 31 reads documents only.

## Constraints

- **Candidate-verdict-source standing.** The resolution doc is the candidate verdict source, NOT
  authoritative — the same standing `ctl_pinn_resolution.md` held in v1.4 and `02-resolution-doc.md`
  held in v1.5. Phase 31 verifies its *readiness*, never ratifies its verdicts.
- **SCOPE-12 hard constraints** (the locked v1.4 + v1.5 outcomes) are fixed inputs to the
  compliance check and are never re-opened by this phase.
- **Verified-facts source** is the archived v1.5 register
  `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`
  — there is no in-milestone v1.6 verification phase.
- **STOP protocol in full** (adjudication milestone): source-silent semantic / process-schema /
  cross-phase decisions are surfaced as gaps in `31-GAPS.md` + `.planning/milestones/v1.6-GAPS.md`
  (created on first gap), never invented.
- **STATE.md is mutated only via gsd-tools handlers** (no direct Write/Edit), per the project
  anti-pattern.
- **One atomic commit per plan via `scripts/agent-commit`** (`GIT_AGENT_ID` +
  `GIT_AGENT_OWNED_PATHS`; `.githooks` active); no commit touches `pinn/` or the framework specs.

## Acceptance Criteria

- [ ] The pre-exec gate records both conditions PASS (doc present, non-empty, canonical =
      `research_result/03-final-resolution.md`; Phase 30 COMPLETE); a stub/empty doc or missing
      completion marker STOPs instead of running partially.
- [ ] The presence/structural check records `PASS` or `FAIL` with a section inventory; a raw
      concatenation is recorded `FAIL`.
- [ ] The crosswalk maps all **18** selected findings (15 SC1 + adaptive stage assignment +
      `L_max`/`tau_L` + ALM `mu_p` clamp) to a section with `covered` / `partial` / `silent`;
      matching is by finding identity; `surface_to_user` / `defer` are `covered`-with-caveat, never
      `silent`; every `partial` / `silent` is flagged as a gap; no selected finding is omitted.
- [ ] The consistency check lists each doc figure mapping to a v1.5-verified fact with
      `consistent? yes/no` under the within-stated-precision rule; passes iff 0 contradictions;
      non-contradicting unverified figures are caveats; a zero-mapped outcome is a recorded vacuous
      pass.
- [ ] The convention-compliance check marks each locked v1.4/v1.5 convention `compliant? yes/no`;
      passes iff 0 violations; scope observations are recorded and surfaced, never counted as
      failures; no locked convention is re-adjudicated.
- [ ] `31-RESOLUTION-MAP.md` exists with a section index (line ranges), the 18-finding
      finding→section mapping, a citation guide with a concrete line-range example anchored to the
      committed revision, a per-finding verdict-direction preview, and an open-items carry-forward.
- [ ] `31-READINESS-REPORT.md` exists with an exec-summary verdict
      (`READY`/`READY-WITH-CAVEATS`/`NOT-READY`), the four check results, gap list, fix
      instructions for any gap, a re-check protocol, and the gate decision — the verdict derivable
      from the check tables by the stated precedence.
- [ ] On `NOT-READY`, fix instructions are routed to the external consolidation agent and
      Phases 32–36 stay blocked until the fix lands and an affected-only re-check passes.
- [ ] `git diff` for the Phase 31 commit shows zero changes to `ctl_instruction.md`,
      `pinn_architecture.md`, the resolution doc, or any `pinn/` path; no finding carries a Phase 31
      verdict.

## Edge Coverage

**Coverage:** 9/9 applicable edges resolved · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| adjacency (alias) | R3 | ✅ covered | Crosswalk matches by finding **identity**, not literal heading text — doc titles reconciled to selected-set keys (e.g. "componentwise automatic differentiation" §1.12 = NS-12; "Causal-training mode" §1.1 = D-04). → R3 acceptance. |
| adjacency (mapping) | R3 | ✅ covered | A finding may map to >1 section and a section may cover >1 finding; the crosswalk records the actual mapping, not an assumed 1:1. → R3 acceptance. |
| empty (position-less) | R3 | ✅ covered | A section that exists but states no actual position is `partial` (a gap), not `covered`. → R3 acceptance. |
| precision (approx figure) | R4 | ✅ covered | **User decision:** a figure agreeing within the verified fact's stated rounding/precision (e.g. `~2,565`) is consistent; only a materially different value is a contradiction. → R4 acceptance. |
| empty (no mapped figures) | R4 | ✅ covered | If the doc states no figure mapping to a verified fact, the check passes vacuously (0 contradictions), recorded explicitly. → R4 acceptance. |
| boundary (recommends vs violates) | R5 | ✅ covered | A recommendation to change a locked convention is a recorded **scope observation** (surfaced, not a failure); a silent breach is a **violation** (NOT-READY trigger). Grounded in ROADMAP SC2 + v1.5 24.5 Task 4. → R5 acceptance. |
| empty (stub / multi-doc) | R1 | ✅ covered | **User decision:** canonical subject = `research_result/03-final-resolution.md`; a stub/empty/header-only doc FAILS the gate and STOPs; extra candidate docs are ignored. → R1 acceptance. |
| idempotency (re-delivery) | R6, R7 | ✅ covered | On re-delivery, the map's line ranges are refreshed and only affected checks re-run; §/finding-ID anchors are stable, line numbers are not. → R6/R7 acceptance. |
| boundary (mixed-outcome gate) | R7 | ✅ covered | A single NOT-READY trigger (silent / contradiction / violation) dominates regardless of passing checks; absent any trigger, any caveat → READY-WITH-CAVEATS; all-clean → READY. → R7 acceptance. |
| ordering | R2 | ⛔ dismissed | A verification report has no output-ordering contract — sections are authored, not algorithmically ordered. |
| idempotency / concurrency | R4, R6 | ⛔ dismissed | Phase 31 is a single-pass, single-agent read; no concurrent execution or repeated-run state to guarantee (re-delivery is covered separately above). |
| precision (own output) | R8 | ⛔ dismissed | Phase 31 emits no numeric output with a rounding contract of its own; the only precision concern (figure agreement) is covered under R4. |

## Prohibitions (must-NOT)

**Coverage:** 7/7 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT adjudicate, settle, or assign a verdict to any finding — including the D-04/D-05/D-06 human-approval decisions; verdicts are Phase 32. | R3, R8 | resolved | judgment — a reviewer confirms the two reports carry coverage status only, no verdict/decision text. |
| MUST NOT edit any framework spec (`ctl_instruction.md` / `pinn_architecture.md`), the resolution doc, or any `pinn/` file. | R8 | resolved | test — `git diff` for the Phase 31 commit shows zero changes to those paths. |
| MUST NOT invent coverage or a verdict where the doc is silent — a `silent` finding is reported as a gap, never filled. | R3, R8 | resolved | judgment — every `silent` selected finding appears as a gap row, never as an inferred verdict. |
| MUST NOT present a "claimed, unverified" figure as a verified fact, and MUST NOT fail the figure check on a non-contradicting unverified figure. | R4 | resolved | judgment — unverified figures appear as caveats with no verified citation; the check fails only on contradictions. |
| MUST NOT declare `READY` / `READY-WITH-CAVEATS` while a NOT-READY trigger (silent finding, verified-fact contradiction, or locked-convention violation) is present — no rubber-stamp; every verdict is backed by the check tables. | R7 | resolved | judgment — the exec-summary verdict is re-derivable from the four check tables by the stated precedence. |
| MUST NOT re-open or re-adjudicate a locked v1.4/v1.5 convention (e.g. the `D = 6.694` conflict) — confirm compliance only; re-adjudication is Phase 32 EVID-15. | R5 | resolved | judgment — no Phase 31 artifact contains a re-adjudication of any SCOPE-12 convention. |
| MUST NOT silently drop any of the 18 selected findings from the crosswalk — a finding not checked is recorded, never omitted. | R3 | resolved | test — the crosswalk table row count over the selected set = 18. |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                                 |
|--------------------|-------|------|--------|-----------------------------------------------------------------------|
| Goal Clarity       | 0.92  | 0.75 | ✓      | One precise outcome; deliverables fixed by the v1.5 24.5 analog; subject doc already landed |
| Boundary Clarity   | 0.92  | 0.70 | ✓      | Crosswalk set locked at 18 (SC1+3); no-adjudication / no-edit perimeter explicit; surface/defer handling locked |
| Constraint Clarity | 0.90  | 0.65 | ✓      | Verified-facts source = archived v1.5 register; SCOPE-12 verbatim; STOP protocol; figure-check = contradiction-only |
| Acceptance Criteria | 0.90 | 0.70 | ✓      | 9 pass/fail criteria; gate-verdict precedence pinned; edge + prohibition probes resolved |
| **Ambiguity**      | 0.09  | ≤0.20| ✓      | Gate passed; remaining open items are execution-level (exact report markdown, line-range capture) |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption). No dimension is below minimum.

## Interview Log

| Round | Perspective     | Question summary                                          | Decision locked                                                                 |
|-------|-----------------|----------------------------------------------------------|---------------------------------------------------------------------------------|
| 1     | Boundary Keeper | Which finding set must the coverage crosswalk check?     | SC1's 15 **plus** the 3 extras (adaptive stage assignment §1.15, `L_max`/`tau_L` §1.17, ALM `mu_p` clamp §1.18) = **18** |
| 1     | Researcher      | Figure-consistency semantics with no Phase-24 analog?    | Contradiction-only fails; an unverified-but-non-contradicting figure is a caveat (flagged FUT), not a failure |
| 1     | Failure Analyst | How to treat the doc's `surface_to_user` / `defer` verdicts? | Caveats, not failures — `surface_to_user` routed to Phase 32 (EVID-15); `defer` = covered-with-routing (v1.5 M13 precedent) |
| 1.5   | Edge probe      | What counts as a figure "contradiction" for approx values? | Match within the verified fact's stated precision; only a materially different value contradicts |
| 1.5   | Edge probe      | Behavior on a stub doc or multiple candidate docs?       | Canonical = `research_result/03-final-resolution.md`; stub/empty FAILs the gate; extra candidates ignored |

---

*Phase: 31-resolution-doc-readiness-verification*
*Spec created: 2026-06-20*
*Next step: /gsd-discuss-phase 31 — implementation decisions (exact report/map markdown, line-range capture method, the four-check task order)*
