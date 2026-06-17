# Phase 29: Acceptance Checks, Re-verification, and Handoff - Context

**Gathered:** 2026-06-16
**Status:** Ready for planning — **paused for user review** before plan-phase (user choice, discuss-phase 2026-06-16)

<domain>
## Phase Boundary

Phase 29 closes v1.5 by producing named closure artifacts that (a) re-run the full
`AC-PIPE-*` / `AC-VAL-*` acceptance suite for confidence in the information and design,
(b) close the v1.5 issue ledger to terminal states, (c) reconcile the remaining `SI-*`
entries, (d) record the FUT-01 implementation handoff, and (e) reconcile the locked
184 → 67 standard-gold completeness outcome **at the planning/governance/ledger layer
only** — without promoting the 117 validated reruns into canonical gold and without
editing framework specs / AC counts. v1.5 remains spec-side; FUT-01 implements.

This is the **terminal** v1.5 phase. Requirements are locked by `29-SPEC.md` (ambiguity
0.08); this context captures the HOW, not the WHAT.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**5 requirements are locked.** See `29-SPEC.md` for full requirements, boundaries, and
acceptance criteria. Downstream agents MUST read `29-SPEC.md` before planning or
implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Create/maintain the Phase 29 closure artifacts: `29-SPEC.md`, `29-UAT.md`, `29-HANDOFF.md`, and one FUT-01 divergence/handoff artifact.
- Re-run the full applicable `AC-PIPE-*` / `AC-VAL-*` suite for confidence (commands/functions, data, pass criteria, results, evidence).
- Reconcile the v1.5 issue ledger to terminal states (`VERIFIED` or explicitly documented `DEFERRED`).
- Review and reconcile `SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002` per VER-12.
- Record the FUT-01 implementation handoff for DataLoader-, TrajectoryValidator-, TrajectoryIndex-, metric-, data-format-, and gold-counterpart-facing obligations.
- Reconcile the standard-gold 184 → 67 rerun outcome against stale repo planning/spec records before using gold-completeness language in PSC closure.

**Out of scope (from SPEC.md):**
- Production DataLoader / TrajectoryValidator / TrajectoryIndex / training-loop / live `pinn/` implementation — FUT-01 implements.
- Inventing or landing a canonical PSC/VAL-04 composition — PSC stays user-deferred unless the user explicitly resolves GAP-28-03.
- Retrying the 67 irreducible gold failures — they are permanent absent gold counterparts.
- Editing `sampling_method.md` or `data_quality_assessment.md` — SCOPE-08 / SCOPE-09 in force.
- Treating live `pinn/` code as grounding — SCOPE-10 in force.
- Maintaining LaTeX/PDF publication parity — deferred to later implementation/training stability.

</spec_lock>

<decisions>
## Implementation Decisions

### Gold-completeness reconciliation scope — **GAP-29-01 ruling** (the one surfaced fork)

- **D-01 (LOCKED 2026-06-16, Option A):** Phase 29 reconciles **only the
  planning / governance / ledger layer** to the locked **117 validated / 67 permanent
  `gold_counterpart=absent` / 0 promoted** fact (grounded by `29-SPEC.md` Background +
  the 2026-06-14 user ruling). It does **not** promote the 117 into canonical gold and
  does **not** edit framework specs or AC counts. The dataset promotion + the
  184 → 67 framework-spec/AC cascade is **DEFERRED to a separate explicit user ruling**
  (tracked as **GAP-29-01**).

  **IN scope under D-01 (Phase 29 performs):**
  - Issue-ledger gold rows (M13 / G4): keep `VERIFIED`, add a reconciliation note that OI-7b executed *partial* (117/184 validated, 67 permanent-absent, 0 promoted) and that promotion + count cascade is deferred.
  - `GAP-28-03` rationale: reframe (see D-06).
  - `GAP-26-01` forward-dependency note: record the partial OI-7b outcome (117 landed-but-unpromoted, 67 permanent-absent).
  - `STATE.md`: drop the "gold eventually-completable" framing → "gold final: 117 validatable + 67 permanent-absent; promotion deferred."
  - `29-UAT.md`: the gold-completeness reconciliation table + a stale-artifact inventory (each stale record named with its corrective action and `deferred → GAP-29-01` marker).

  **OUT of scope under D-01 (DEFERRED → GAP-29-01, NOT touched in Phase 29):**
  - Promote the 117 staged successes (gold stays 2,565, not 2,682).
  - `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` (stays 184).
  - `ctl_instruction.md` Step 5 gold-counterpart note ("backlog expected empty" stays, KNOWN-STALE).
  - Set-2b / issue-02 count fields (stay 2,565).
  - `AC-PIPE-05` assertion + runner `EXPECTED_ID_COUNT` (stay 184).

- **D-01a (LOCKED-ruling sensitivity):** The M13 / GAP-26-01 packet
  (`.planning/phases/25-.../evidence/m13-gold-counterpart.md`) factual-outcome update
  (record "OI-7b executed partial") is treated as planning-layer reconciliation
  **grounded by `29-SPEC.md`**; the LOCKED M13 *verdict* (Option B — re-simulate, no
  base→gold substitution) is **untouched**. If execution finds the packet edit reads as
  *re-adjudication* of the LOCKED verdict rather than recording its empirical outcome,
  **STOP and re-surface** per the STOP protocol — do not silently invent.

### Rerun evidence (Area 1)

- **D-02:** Re-run the **full** applicable `AC-PIPE-*` / `AC-VAL-*` suite (not a narrow
  terminal-state check), enumerated from the issue-ledger "Acceptance check:" rows +
  phase contracts. Each `29-UAT.md` row records: command/function, input data, pass
  criterion, result, evidence path. Probes are disposable (dataset + spec-consistency);
  **no probe touches `pinn/` production code** (VER-09 / SPEC Constraint).
- **D-03:** `AC-PIPE-05` (gold set-difference probe) reruns and is recorded **PASS at
  184/184** — internally consistent precisely because no promotion occurs under D-01.
  `29-UAT.md` notes it moves to 67/67 only if/when the deferred GAP-29-01 promotion lands.
- **D-04:** Acceptance checks whose owning contract is user-deferred (`AC-VAL-04` / PSC)
  are recorded **`DEFERRED`** with the exact blocker + decision record (GAP-28-03), never
  counted `PASS`.

### Gold / PSC reconciliation (Area 2)

- **D-05:** `29-UAT.md` carries the gold-completeness reconciliation table — 184
  attempted, 117 validated (staged, unpromoted), 67 permanent `gold_counterpart=absent`,
  0 promoted — with evidence paths and the disposition of the 67 holes per the
  2026-06-14 ruling (keep all 67 base trajectories; permanent Stage-5 holes; no
  base→gold substitution; no retry).
- **D-06:** PSC / VAL-04 stays **`DEFERRED`**. Blocker reframed from *"wait until the
  gold dataset is complete"* → *"gold completeness is settled as final (117 validatable +
  67 permanent-absent); PSC's data dependency is discharged; the dedup-prefer-gold +
  equal-record composition remains user-deferred pending explicit GAP-28-03 reopen."*
  The composition itself is **NOT invented** (STOP protocol).

### Ledger / SI closure (Area 3)

- **D-07:** Close `24-ISSUE-LEDGER.md` only when every in-scope row is `VERIFIED` or
  explicitly `DEFERRED`. `29-UAT.md` carries a status-count audit confirming **zero**
  `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` in-scope rows and naming each `DEFERRED` row +
  its blocker.
- **D-08:** Review `SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002` (VER-12): each
  **retired-with-backref** (to resolving phase/commit) or **preserved-with-written-reason**;
  none assumed resolved or assumed irrelevant. If any disposition turns out source-silent
  during execution, **surface per STOP protocol** — do not invent.

### FUT-01 handoff packaging (Area 4)

- **D-09:** Emit **two** artifacts mirroring v1.4 Phase 21:
  - `29-HANDOFF.md` — fixed / intentionally-unchanged / deferred findings + the three SI dispositions (mirror `21-HANDOFF.md`).
  - `29-CODE-DIVERGENCE.md` — the FUT-01 divergence artifact: every DataLoader, TrajectoryValidator, TrajectoryIndex, metric, data-format, and gold-counterpart implementation obligation to rebuild from settled specs (mirror `21-CODE-DIVERGENCE.md` structure). Live `pinn/` code appears ONLY as a divergence target, never as grounding (SCOPE-10).
- **D-10:** The GAP-29-01 deferred promotion + cascade is itself recorded as a forward
  obligation in `29-CODE-DIVERGENCE.md` (gold-counterpart handling + the 117-promotion
  decision), so it is not lost when v1.5 closes.

### Claude's Discretion

- Table-vs-prose formatting and section ordering within the named artifacts — mechanical;
  follow the v1.4 Phase 21 (`21-UAT.md` / `21-HANDOFF.md` / `21-CODE-DIVERGENCE.md`)
  precedent where one exists.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 29 spec, roadmap, requirements
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-SPEC.md` — LOCKED 5 requirements, boundaries, acceptance criteria. MUST read first.
- `.planning/ROADMAP.md` §"Phase 29" (≈ L282–294) — goal, depends-on, VER-07/08/09/11/12, five success criteria.
- `.planning/REQUIREMENTS.md` — VER-07/08/09/11/12 text (≈ L67–72); requirement→phase map (≈ L147–151); v1.5 distribution (≈ L157).

### Gold-completeness (Area 2 / GAP-29-01)
- `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-GAPS.md` — GAP-29-01 (gold promotion + cascade scope), RESOLVED-WITH-INSTRUCTION = Option A, with embedded DEFERRED action.
- `simulation_data/Data/rerun_staging/standard_gold_missing_184/` — staged 117-validated / 67-failed outputs + manifest (evidence for the reconciliation table).
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — the 184 not-in-gold list. **KNOWN-STALE under D-01** (corrective 184→67 edit deferred to GAP-29-01).
- `simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py` — rerun/promote runner (`EXPECTED_ID_COUNT=184`; `--validate-only` / `--promote`). Promotion deferred.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` Step 5 gold-counterpart note — **KNOWN-STALE** ("remediation backlog expected empty"); corrective edit deferred to GAP-29-01.
- Agent-memory `missing-67-gold-decision` (user ruling 2026-06-14) — 117/67, keep base, permanent Stage-5 holes, the 6-edit cascade list. (Not in-repo; the 29-SPEC Background restates the grounded facts.)

### Issue ledger / gaps / SI
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — full `AC-PIPE-*`/`AC-VAL-*` rows, M13/G4 gold rows, SI entries; the ledger-close target.
- `.planning/milestones/v1.5-GAPS.md` — milestone gap index (GAP-28-03 DEFERRED; GAP-29-01 added).
- `.planning/phases/28-validation-metrics-contracts/28-GAPS.md` — GAP-28-03 PSC deferral detail (blocker to reframe).
- `.planning/phases/26-dataloader-ingestion-and-selection-contracts/26-GAPS.md` — GAP-26-01 (M13, OI-7b forward dependency to reconcile).
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m13-gold-counterpart.md` — M13 packet (LOCKED verdict; D-01a sensitivity).

### FUT-01 handoff precedent (mirror these)
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-HANDOFF.md` — handoff structure precedent.
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/21-CODE-DIVERGENCE.md` — CODE-DIVERGENCE structure precedent.

### Governance
- `CLAUDE.md` — v1.5 STOP protocol (Phases 23–29); spec-edit targets `ctl_instruction.md` / `pinn_architecture.md` only; live-`pinn/` ban.
- `.planning/REQUIREMENTS.md` SCOPE-05..10 — data-generation carveout, empirical-observation grounding, frozen `sampling_method.md`, read-only `data_quality_assessment.md`, live-code ban.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `rerun_standard_gold_missing_184.py` (+ its test): already implements staging /
  `--validate-only` / `--promote` / stall-detection for the 184→117/67 outcome. FUT-01
  reuses it; **promotion deferred** under D-01. Evidence anchor for the reconciliation table.
- Prior-phase `AC-PIPE-*` / `AC-VAL-*` disposable probes — the rerun pattern for D-02.

### Established Patterns
- `NN-CODE-DIVERGENCE.md` + `NN-HANDOFF.md` (v1.4 Phases 17–21) — the FUT-01 handoff shape (D-09).
- Issue-ledger state machine + dated audit-entry convention (`24-ISSUE-LEDGER.md`) — the ledger-close shape (D-07).
- Phase-local `NN-GAPS.md` + `v1.5-GAPS.md` index — the STOP-gap recording shape (GAP-29-01).

### Integration Points
- `29-UAT.md` consumes the issue-ledger AC rows + the staging evidence.
- `29-HANDOFF.md` / `29-CODE-DIVERGENCE.md` consume the v1.5 ledger + framework specs (`ctl_instruction.md`, `pinn_architecture.md`).

</code_context>

<specifics>
## Specific Ideas

Locked user premises carried into Phase 29:
- The 184 standard-gold rerun has **already been attempted**; 117 validate, 67 are
  **permanent** absent gold counterparts (not a backlog).
- Phase 29 stays **spec-side** (Option A) — reconcile the planning layer, defer the
  dataset/framework-spec cascade.
- PSC/VAL-04 stays **DEFERRED** unless the user explicitly reopens GAP-28-03.
- FUT-01 handoff mirrors the **v1.4 Phase 21 two-artifact** pattern.

</specifics>

<deferred>
## Deferred Ideas

- **GAP-29-01 — gold promotion + 184→67 cascade (DEFERRED, separate explicit user
  ruling required).** Promote the 117 validated reruns into canonical gold (2,565 →
  2,682) and apply the cascade: `standard_quasi_random_ids_not_in_gold.md` 184→67;
  `ctl_instruction.md` Step 5 note; Set-2b / issue-02 counts; `AC-PIPE-05` + runner
  `EXPECTED_ID_COUNT` 184→67; M13/GAP-26-01 packet. Recorded as a FUT-01 forward
  obligation in `29-CODE-DIVERGENCE.md` (D-10) so it survives v1.5 closure.
- **PSC / VAL-04 composition** (dedup-prefer-gold + equal-record weighting) — user-deferred
  (GAP-28-03); revisit on explicit reopen after the gold reconciliation.

### Reviewed Todos (not folded)
- `.planning/todos/pending/trainex-r1-research-handoff.md` ("Review and hand off the
  trainex-r1 research sub-packages r1a + r1b") — **reviewed, not folded.** Belongs to the
  *trainex* (training-execution) track; v1.5 is *specwork*. Out of Phase 29 scope.

</deferred>

---

*Phase: 29-acceptance-checks-re-verification-and-handoff*
*Context gathered: 2026-06-16*
