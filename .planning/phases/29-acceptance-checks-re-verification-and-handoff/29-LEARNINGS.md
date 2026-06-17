---
phase: 29
phase_name: "Acceptance Checks, Re-verification, and Hand-off"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 8
  lessons: 5
  patterns: 4
  surprises: 3
missing_artifacts: []
---

# Phase 29 Learnings: Acceptance Checks, Re-verification, and Hand-off

## Decisions

### GAP-29-01 RESOLVED-WITH-INSTRUCTION Option A — Reconcile Planning Layer Only, Defer Promotion
The gold-completeness reconciliation scope decision (whether Phase 29 promotes the 117 validated standard-gold reruns and applies the 184 → 67 framework-spec/AC/dataset cascade, or reconciles only the planning/governance/ledger layer) was surfaced as a STOP-protocol gap (`29-GAPS.md` GAP-29-01, classification: semantic + cross-phase reframing) and resolved with user instruction selecting **Option A**: Phase 29 reconciles only the planning/governance/ledger layer to the 117-validated / 67-permanent-absent / 0-promoted fact; the dataset promotion and 184→67 cascade are NOT performed in Phase 29 and remain DEFERRED to the FUT-01 dataset-finalization gate as FO-1. An embedded sub-decision ruled promote=yes at the FUT-01 gate (as one atomic transaction), with two additions: re-derive the gold-hole count from parsed `not_in_gold.md` content (blacklist-contract anti-hardcode rule) and back up the 117 staged outputs + `run_manifest.json` to the separate simulation-payload set.

**Rationale:** Mutation of the canonical `simulation_data/` gold dataset and editing of LOCKED M13 / AC-PIPE-05 rulings at the terminal milestone would create irreversible spec drift; Option A keeps the planning layer consistent with the locked 117-validated / 67-permanent / 0-promoted fact while preserving a single, auditable corrective transaction at the FUT-01 gate.

**Source:** 29-01-SUMMARY.md:STOP-Guard Status; 29-GAPS.md:GAP-29-01; 29-HANDOFF.md:§2 (Intentionally Unchanged)

---

### Ledger PSC Row Reframed (D-06) Without Touching Adjacent Rows
The PSC row (line 37) of `24-ISSUE-LEDGER.md` was edited in place to reframe the superseded "wait for gold completion" blocker as the D-06 framing (PSC clause LANDED; dedup-prefer-gold + `1/N_t` composition ratified, GAP-28-03; AC-VAL-04 numeric calibration awaits the post-promotion pool at FUT-01 FO-2). `git diff` confirmed the change is confined to line 37; M13/G4 rows and their OI-7b-partial notes are byte-identical (D-01a). Row-status enumeration: `NONTERMINAL []`, `COUNTS 18 1`.

**Rationale:** The PSC row's blocker text was stale relative to the committed PSC landing (D-01) and the GAP-28-03 composition ratification; re-scoping the blocker preserves the terminal state (still `DEFERRED`) while making the blocker text match the current decision context — without disturbing adjacent LOCKED rulings.

**Source:** 29-01-SUMMARY.md:What Was Built — Task 1

---

### AC-PIPE-08 Folded Into M12/G5 Family Under G5 — No Standalone Ledger Row
AC-PIPE-08 has no standalone ledger row; it was re-run inside the M12/G5 family and noted under G5 (13 ledger-mapped result lines, all 14 probe IDs exercised).

**Rationale:** AC-PIPE-08 is structurally a child of the M12/G5 acceptance lineage; introducing a new ledger row would expand the terminal ledger to 20 rows and break the 18 VERIFIED + 1 DEFERRED shape the G3 gate audits. Folding it under G5 keeps the audit surface consistent.

**Source:** 29-01-SUMMARY.md:frontmatter decisions

---

### ROADMAP Stale Framing Reconciled in Both Occurrences (Not Just the Progress Row)
The plan action named the Phase-28 Progress row, but the Task 3 verify required zero occurrences anywhere of "VAL-04/PSC user-deferred"; the second occurrence (the Phase-28 milestone bullet) carried the identical stale framing. Both were reconciled to PSC-landed (Phase-28 Progress row 3/4 → 4/4; the Phase-28 milestone bullet; Phase-29 row → In progress (1/2); footer date 2026-06-14 → 2026-06-17).

**Rationale:** Stale framing in any single location of a governance document is enough to mislead a downstream consumer; the verify-check contract demands zero stale occurrences, so the second edit is part of the same D-01 planning-layer reconciliation, not scope creep.

**Source:** 29-01-SUMMARY.md:Deviations from Plan — item 3

---

### D-08 STOP-Checkpoint Resolution: SI-PINN-002 Preserve-with-Reason (User-Approved)
The SI-PINN-002 disposition (the 3rd author comment "batch construction not consistent with the CTL instruction plan") is source-silent on whether the landed M12 mini-batch contract discharges it. Per the STOP protocol this was surfaced as a `checkpoint:human-verify` STOP point — not silently decided. The user **APPROVED preserve-with-reason** on 2026-06-17, explicitly declining to mark the comment retired-by-M12. SI-PINN-002 was NOT silently marked retired-by-M12; it is preserved-with-written-reason and carried to FUT-05. This matches the v1.4 `21-HANDOFF.md` "Preserved untouched" pattern.

**Rationale:** Source-silent semantic decisions must be surfaced (D-09); silent retirement-by-M12 would have collapsed a forward architecture-side author-comment into a data-pipeline verdict without grounding, and the user explicitly retained forward scope for FUT-05.

**Source:** 29-02-SUMMARY.md:Decisions Made; 29-HANDOFF.md:§4 (SI Metadata Reconciliation) + D-08 checkpoint resolution

---

### G1-G8 Closure Gate Transcribed Verbatim — No G9+ Invented
The eight G1-G8 closure conditions, their numeric pass criteria, and their route-back-on-fail targets are transcribed verbatim from `29-RESEARCH.md` §Milestone-Closure Gate. No gate condition's pass criterion or route-back target was invented; no G9+ added. The closure rule: v1.5 closes only when G1-G8 all pass; any G1/G2/G3 FAIL routes the specific finding back to its originating phase (26/27/28) per VER-09.

**Rationale:** The gate is a closure contract; any invented pass criterion or silent relaxation would let a future executor clear a finding the milestone does not actually discharge. Transcribing verbatim keeps the gate's authority at the source and lets the route-back-on-fail column carry its full VER-09 routing meaning.

**Source:** 29-02-SUMMARY.md:Decisions Made; 29-HANDOFF.md:§6 (Milestone-Closure Gate)

---

### Two-Artifact FUT-01 Handoff: `29-HANDOFF.md` + `29-CODE-DIVERGENCE.md` (D-09)
The FUT-01 handoff is split into two artifacts: `29-HANDOFF.md` (this milestone's closure record, authored in Phase 29 Plan 02) and `29-CODE-DIVERGENCE.md` (FO-1 gold promotion + 184→67 cascade + FO-2 PSC/SCR numeric calibration, committed earlier). `29-HANDOFF.md` references the divergence doc by line, never duplicating its content (the FO-1 gold-completeness reconciliation table, the stale-record inventory, the FO-2 PSC/SCR plan).

**Rationale:** A single handoff that mixed closure narrative and forward-mutation obligations would conflate the two scopes and make the v1.5 closure record harder to audit; two artifacts keep the closure record read-only-friendly and the forward obligations machine-actionable at the FUT-01 gate.

**Source:** 29-02-SUMMARY.md:frontmatter patterns; 29-HANDOFF.md:header

---

### Gold-Hole Count Re-Derivation Rule (Blacklist-Contract Anti-Hardcode)
The embedded GAP-29-01 sub-decision explicitly ruled that the 67 gold-hole count is **re-derived from parsed `not_in_gold.md` content** rather than re-hardcoded — applying the blacklist-contract anti-hardcode rule at the FUT-01 promotion step.

**Rationale:** The existing 184/67 ratio is itself a derived quantity; hardcoding 67 in the FUT-01 cascade would freeze a number that the parsed set-difference already produces authoritatively, and any future change to `not_in_gold.md` would silently invalidate the hardcoded value.

**Source:** 29-GAPS.md:GAP-29-01 Resolution note — embedded sub-decision (a)

---

## Lessons

### Probe Negative-Control Line-Scoping Must Match Wrapped Clause Layout
First suite run failed two checks (AC-PIPE-02, AC-PIPE-03, AC-VAL-02): the asserted phrases ("NO code path may compute a path…", "not a contract constant", "9-component aggregation is rejected") are line-wrapped in `ctl_instruction.md`, so multi-line `grep` scoping missed them. Fixed by asserting the single-line token that actually carries each phrase.

**Context:** The clauses do contain the assertions; only the probe's regex scoping was at fault. The fix happened before the Task 2 commit, but it highlights a class of failure: positive-assertion + negative-control probes that rely on text-spanning multi-line patterns are fragile against the very line-wrapping that human authors of spec files will introduce.

**Source:** 29-01-SUMMARY.md:Deviations from Plan — item 1

---

### `pinn/`-in-Docstring Trips the VER-09 Reference Check
The VER-09 "no probe references `pinn/`" check tripped on a docstring phrase ("touches no pinn/ code") in `ac-pipe-05.py`. Reworded to "production model code" (the `pinn_*` spec paths in other probes use underscores and never match `pinn/`).

**Context:** The literal substring `pinn/` is forbidden inside probes under VER-09 / SCOPE-10, even in comments and docstrings; the underscore convention `pinn_*` for spec file basenames sidesteps the substring match entirely.

**Source:** 29-01-SUMMARY.md:Deviations from Plan — item 2

---

### Stale Records Must Be Documented, Never Silent — Even When Out of Scope
Per the locked GAP-29-01 Option-A ruling, Phase 29 leaves the gold-completeness records stale (`not_in_gold.md` at 184, `AC-PIPE-05` at 184/184, runner `EXPECTED_ID_COUNT` at 184, `ctl_instruction.md` Step 5 gold note "backlog expected empty", Set-2b / issue-02 counts at 2,565), but documents the staleness in `29-CODE-DIVERGENCE.md` as the stale-record inventory — never silent. The disposition is `KNOWN-STALE` rather than `VERIFIED` or `DEFERRED` — a third planning-layer category that records the decision context without pretending the records are up to date.

**Context:** Without the documented inventory, a downstream reader of `not_in_gold.md` could not tell whether the 184 count is the current truth or a known-stale figure awaiting FUT-01; the inventory carries the planning-layer disposition that the records themselves cannot.

**Source:** 29-HANDOFF.md:§2 (Intentionally Unchanged) — KNOWN-STALE gold records paragraph; 29-CODE-DIVERGENCE.md (referenced, not duplicated)

---

### GSD `update-plan-progress` Has a Known State-Verb Regression (Phase 29)
`gsd-tools query roadmap.update-plan-progress 29` overwrote the descriptive ROADMAP status cell with a malformed value (bare `In Progress|`, dropping the descriptive text and the completion-date column) and pre-flagged 29-01 as done while counting `summary_count: 1`. The change was reverted (`git checkout -- .planning/ROADMAP.md`) and the ROADMAP Phase 29 progress row was edited manually instead. STATE.md was likewise edited manually.

**Context:** The GSD tooling's ROADMAP progress writer is not yet trustworthy for milestone-closure rows; manual edits are required to keep the descriptive status text and the date column intact. The regression is on the tool side, not in the data the tool operates on.

**Source:** 29-02-SUMMARY.md:Issues Encountered

---

### SI-PINN-003 Correctly NOT Folded Into the VER-12 Table
The adjacent `pinn_architecture.md` batch-construction-inconsistency SI entry (the SI block immediately after `SI-PINN-002`) is **not** in the VER-12 review list and is deliberately not folded into the §4 disposition table; it remains an FUT-05 item. The `21-HANDOFF.md` precedent table covers only entries the current milestone review actually names.

**Context:** Folding adjacent-but-out-of-scope SI entries into the milestone's reconciliation table would expand the table's authority beyond the issue-02 data-pipeline scope the v1.5 milestone actually resolves, and would risk retiring a forward architecture-side item on a data-pipeline verdict.

**Source:** 29-HANDOFF.md:§4 (SI Metadata Reconciliation) — adjacent-entry note

---

## Patterns

### Anti-Hardcode Derived Count: Set-Difference Probe Computes Its Own Expected
`ac-pipe-05.py` is a Python set-difference probe over `simulation_data/` (base 2,749 − gold 2,565 == the 184 `not_in_gold.md` IDs, exact intersection): **PASS @184/184** with 0 promoted (D-01/D-03), the count derived from parsed sets. No literal 184/67 in source. The probe accepts the actual on-disk state as authoritative rather than asserting a hard-coded expected number.

**When to use:** Whenever an acceptance check asserts a count or ratio that is itself derivable from the file system or repository state being checked. The pattern makes the probe resilient to dataset changes (gold promotion, blacklist updates) without re-writing the probe.

**Source:** 29-01-SUMMARY.md:What Was Built — Task 2; frontmatter tech-stack patterns

---

### Planning-Layer Disposition Recording: Don't Edit Read-Only / Frozen SI-Home Files
SI/staleness dispositions are recorded in `29-HANDOFF.md` §2 and §4, never by editing the read-only or frozen SI-home files (`data_quality_assessment.md:318-328` under SCOPE-09, `pinn_architecture.md:996-1004` for SI-PINN-002, `sampling_method.md` under SCOPE-08, `simulation_data/` under dataset-mutation scope). The handoff carries the audit-trail entries; the home files stay untouched.

**When to use:** When a milestone closure needs to record an SI disposition, a stale-record inventory, or a deferred-to-forward obligation that affects a file outside the milestone's edit scope. The planning layer becomes the audit-trail carrier; the home file's read-only/frozen status is preserved.

**Source:** 29-02-SUMMARY.md:frontmatter patterns; 29-HANDOFF.md:header + §2 + §4

---

### Closure Gate With Per-Condition Route-Back-on-Fail Targets
The G1-G8 milestone-closure gate assigns each gate condition both a numeric pass criterion AND a route-back-on-fail target (the originating spec-edit phase for G1/G2/G3; the owning phase for non-terminal rows in G3; roadmap revision for G6 mismatch; STOP for G8 governance violation). The route-back column lets a failing check block closure and surface the specific remediation path without a follow-up planning cycle.

**When to use:** When defining a milestone-closure contract that must distinguish a passing milestone from a milestone with a latent failure. Each gate condition should name (a) what numeric pass looks like, and (b) where the failure goes for remediation.

**Source:** 29-02-SUMMARY.md:frontmatter patterns-established; 29-HANDOFF.md:§6 (G1-G8 table)

---

### Re-Run As Fresh Disposable Phase-29 Probes (Don't Reuse the Original Runners)
11 new probes (`ac-pipe-01/02/03/06/07/10.sh`, `ac-pipe-05.py`, `ac-val-01/02/03/04.sh`) + `run-ac-suite.sh` were authored; the 3 persisted Phase-27 probes (`ac-pipe-04/08/09.sh`) were re-run in place. The new probes live in the phase-29 directory and have the same positive-assertion + negative-control grep structure, but they assert the LANDED spec text rather than re-running a different mechanism.

**When to use:** When a terminal acceptance-checks phase needs fresh evidence rather than relying on the original phase's run. The pattern keeps the original probes intact (auditable) and the new probes as the closure evidence.

**Source:** 29-01-SUMMARY.md:What Was Built — Task 2; key-files created

---

## Surprises

### `gsd-tools query roadmap.update-plan-progress` Wrote a Malformed Status Cell
The GSD ROADMAP-update tool's state-verb writer is broken in a way that drops the descriptive status text and the completion-date column and pre-flags 29-01 as done while reporting `summary_count: 1`. The fix required `git checkout -- .planning/ROADMAP.md` and a manual edit. STATE.md needed a manual edit too. This is the same GSD tooling that the v1.5 milestone uses to advance its own progress row, so the regression is on the path the milestone itself relies on.

**Impact:** Every Phase 29 ROADMAP advance had to be hand-edited instead of tool-driven, and a future milestone using `update-plan-progress` on a closure row will likely see the same regression — the `STATE.md` lag pattern from prior GSD state (`.planning/STATE.md` lags reality after a phase boundary) compounds with this tool-side defect.

**Source:** 29-02-SUMMARY.md:Issues Encountered

---

### AC-PIPE-05's 184/184 Internally Consistent Only Because the 117 Are Unpromoted
The AC-PIPE-05 set-difference probe asserts `{standard IDs} − {gold IDs} == standard_quasi_random_ids_not_in_gold.md`, currently **184/184 and VERIFIED**. The specs are internally consistent *at 184* only because the 117 successes are **unpromoted** (gold = 2,565; 0 promoted). Promotion changes `{gold}` by +117, which forces a coupled, largely-irreversible cascade: `not_in_gold.md` 184 → 67 → `AC-PIPE-05` must assert 67/67 (else it fails) → runner `EXPECTED_ID_COUNT` 184 → 67 → Set-2b / issue-02 counts 2,565 → 2,682 → M13/GAP-26-01 packet records OI-7b partial. The probe's current PASS state is therefore not a stable equilibrium — it is a snapshot of the planning layer's current reconciled state.

**Impact:** The probe cannot be re-run as-is after FUT-01 FO-1; the cascade is a one-shot atomic transaction, and the probe's expected assertion target moves with the cascade. This concentrates the gold-completeness decision into a single moment in the FUT-01 gate rather than letting it drift through incremental re-runs.

**Source:** 29-GAPS.md:GAP-29-01 — Mathematical / engineering grounding; 29-01-SUMMARY.md:STOP-Guard Status

---

### AC-VAL-04 Splits Structural-PASS From Numeric-DEFERRED In the Same Suite Run
`ac-val-04.sh` asserts only the landed PSC clause structure and prints the numeric-DEFER line — it computes no PSC value. The full 13-check suite therefore reports 12 PASS + 1 split (AC-VAL-04 structural PASS / numeric DEFERRED), exit 0, rather than 13 PASS or 1 FAIL. The split is encoded into G1 as a recognized shape.

**Impact:** A future executor reading `bash run-ac-suite.sh` for a pass/fail count cannot use a naive `grep -c PASS` to discover suite status — the count must distinguish the structural-PASS / numeric-DEFERRED shape. The gate G1 explicitly enumerates "12 PASS + 1 split" as the pass criterion, which means the suite's output grammar has effectively been promoted to a contract.

**Source:** 29-01-SUMMARY.md:Verification; 29-HANDOFF.md:§6 G1
