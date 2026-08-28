---
phase: 54-recalibration-decision-grounding
plan: 06
subsystem: planning
tags: [erw, trainex-r3, reconciliation, erw-02]

# Dependency graph
requires:
  - phase: 54-recalibration-decision-grounding
    provides: plans 54-01 through 54-05 summarized; checkpoint ① discharged out of band
provides:
  - 54-RECONCILIATION.md ledger record of commits 11b4e0c1 and ad51968e
  - Checks R1 and R2 replacing the retired two-path tree-completeness guard
  - re-derived ERW-02 audit table and A-1 through A-10 verdicts
  - disk-derived ROADMAP / STATE / VALIDATION accounting; Bar G
affects: [54-07 handoff, Phase 56 still closed]

# Actuals
actuals:
  tokens: 8333
  tasks: 3
  commits: 1

key-files:
  created:
    - .planning/phases/54-recalibration-decision-grounding/54-RECONCILIATION.md
  modified:
    - .planning/ROADMAP.md
    - .planning/STATE.md
    - .planning/phases/54-recalibration-decision-grounding/54-VALIDATION.md
    - .planning/phases/54-recalibration-decision-grounding/54-RESEARCH.md
    - pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md
    - pinn_instruction/markdown_conversion/framework-specs/trainex-r3/DELIVERY-NOTE.md

key-decisions:
  - "This plan does not retroactively authorize commits 11b4e0c1 and ad51968e; it authorizes the reconciliation only."
  - "STATE.md updated by hand because gsd-tools mutating verbs emit malformed output in this checkout."
  - "Check R2 cannot falsify T-54-12 for 11b4e0c1; provenance for the three ERW-02 paths is the verbatim owner instruction at 54-RULING.md:19."
  - "Bar G gate printed BAR-G-CLEAN with G1-REGION=13; an empty region would have been BAR-G-CLEAN-NO-SURFACE-NAMED."
  - "Phase 54 remains in progress. GAP-54-01 stays OPEN. Checkpoint ② stays PENDING. Phase 56 stays closed. ERW-02 is partially discharged."

requirements-completed: []

coverage:
  - id: D1
    description: "Ledger reconciliation of the 2026-08-21 out-of-band assembly pass, Checks R1/R2, re-derived audit table, A-1..A-10, disk-derived accounting, Bar G"
    requirement: ERW-02
    verification:
      - kind: other
        ref: "54-RECONCILIATION.md; Check R1 MANIFEST-OK; Bar G BAR-G-CLEAN G1-REGION=13; empty-cell awk 0; AMENDMENTS-COVERED"
        status: pass
    human_judgment: true
    rationale: "ERW-02 is only partially discharged; delivery, Rule-19, Rule-12, and checkpoint ② remain owner-gated."

# Metrics
duration: 120min
completed: 2026-08-28
status: complete
---

# Phase 54 / Plan 06: Out-of-band ERW-02 assembly pass reconciled; tree-completeness guard retired; accounting derived from disk

**Commits `11b4e0c1` and `ad51968e` are recorded, not retroactively authorized. Checks R1/R2 replace the two-path guard. Every hand-run audit result was re-derived. ERW-02 is partially discharged. Phase 54 remains in progress.**

## Performance

- **Duration:** 120 min
- **Tasks:** 3
- **Files created:** 1 (`54-RECONCILIATION.md`) plus this summary
- **Files modified:** ROADMAP, STATE (by hand), VALIDATION, RESEARCH, master §3/§11, delivery-note attachment table

## What landed on 2026-08-21

Precondition (asserted before any file was written):

- `git merge-base --is-ancestor 11b4e0c1 HEAD` → exit 0
- `git merge-base --is-ancestor ad51968e HEAD` → exit 0

| Hash | Date | Subject |
|---|---|---|
| `11b4e0c12529efe993143c7dcd9eb08df9a213fd` | 2026-08-21 | docs(54): discharge checkpoint one and assemble the trainex-r3 package |
| `ad51968eaa37c246d0692bdd04c3ac381a4aa41e` | 2026-08-21 | docs(54): stamp the rule-20 live-tree pin for the trainex-r3 handoff |

Owner instruction (verbatim, `54-RULING.md:19`): *"let's do the r3 and assemble the research pacakge to be handed off to the external research agent. make sure that the information inlcuded in that package is accurate and faithful"*

## Verification Commands and Outputs

| Check | Output |
|---|---|
| Check R1 | `MANIFEST-OK` |
| Check R1 four-path fail-demo | `MANIFEST-FAIL` exit 1 |
| Check R2 | discharge=`2026-08-21`; DELIVERY-NOTE and master `2026-08-20`; prompt, v2.2 bundle, specs bundle `2026-08-21` |
| Bar A | empty (region 301 lines) |
| Bar A2 line count | 4 (region 28 lines) |
| Bar A2 occurrence count | 11 |
| Bar B | empty (region 421 lines; case-sensitive literal substring) |
| Bar D | empty |
| Bar E Task 2 (canonical two-path) | empty |
| Bar E Task 3 (narrowed to REQUIREMENTS.md) | empty — narrowing recorded with reason |
| Bar F | 0 |
| Snapshot fidelity | specs 10/10 identical; v2.2 3/3 identical; total 13 blocks, 0 mismatched |
| Snapshot fail-demo (source offset +1 line) | specs mismatched=10; v2.2 mismatched=3 |
| Pin consistency | five files, distinct_40hex=1 each, value `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` |
| Baseline currency | empty |
| Citations | 52 distinct `file:line` via `grep -oE '[A-Za-z0-9_./-]+\.(md\|py):[0-9]+' \| sort -u`; 52/52 resolve (packet had 49 with no command) |
| Attachments | 3 of at most 5 |
| Empty-cell awk | exit 0 |
| A-1..A-10 first-cell gate | `AMENDMENTS-COVERED` |
| Bar G `<automated>` | `RETAINED=1568 G1-REGION=13` then **`BAR-G-CLEAN`** (literal; not paraphrased) |
| Bar G fences | 54-06-PLAN.md 12 (even); 54-07-PLAN.md 6 (even) |
| Bar G preprocessing | raw 1647; retained 1568; removed 79 (fences, planner-discipline allow-comment, `<automated>` lines) |

**Bar G fail-demos (scratch copies):** G1 injected `the eta_c value is 1` prints the stripped line; G2 injected recommend/leading option prints that sentence; G3 injected cheaper/faster prints that sentence. Five-surface G1 injections all fire: `eta_c` / `Rbar`+normalization+reference scale / `first_omega_0` / `n_col` / `clip`. Real-text G1 remainder after token strip is empty.

**Check R2 limitation.** For the three ERW-02 artifacts the introducing commit is `11b4e0c1`, which also introduced `54-RULING.md`. Both sides of the comparison are that one day. R2 returns a result consistent with post-gate provenance without demonstrating it. Provenance evidence is the verbatim owner instruction at `54-RULING.md:19`.

## At-source repairs (new A- entries; A-1..A-10 row text unchanged)

- A-11: fifth `pinn_architecture.md` path added to §3 (A-6 stated four)
- A-12: Bar A2 §11 restated as 4 lines / 11 occurrences
- A-13: Check 6 over five files, not four
- A-14: citation count 49 → 52 with command
- A-15: delivery-note attachment table 13 → 10 for the specs bundle
- A-16: A-10's packet-side supersession superseded by this ledger record

## Accounting (derived, not copied)

Milestone-wide: `total_phases` 6 matches `grep -cE '^### Phase [0-9]'`. Counters are milestone-wide. Pre-existing `total_plans: 6` was consistent with disk on 2026-08-20; now 8 plan files and 6 summaries. STATE `progress`: total_plans=8, completed_plans=6, percent=17. ROADMAP Phase 54: 7 plans (5/7 complete); 54-01..05 checked against the recorded five-summary listing; 54-06/54-07 unchecked. ERW-02 is **partially discharged**. STATE edited by hand (no `gsd-tools` mutating verb).

Before→after (proof the edits landed): ROADMAP `ERW-02 is deliberately unplanned` 1→0; STATE the three case-insensitive phrases 1→0 each; VALIDATION `last task of this execution pass` 1→0.

## Outstanding on ERW-02

Delivery; ERW Rule-19 per-claim in-repo verification; ERW Rule-12 consolidation; owner checkpoint ②. `GAP-54-01` stays OPEN. Phase 56 stays closed. Phase 54 remains in progress. 54-07 follows.

## Self-Check: PASSED

- `54-RECONCILIATION.md` exists; `does not retroactively authorize` present; both full hashes present
- Checks R1/R2 recorded with commands, outputs, and demonstrated failure modes
- A-1 through A-10 present as first cells; empty-cell gate exit 0; R1 `\|\|` present in a table cell
- Bar G printed `BAR-G-CLEAN` with `G1-REGION=13`
- Plans 54-01 through 54-05, REQUIREMENTS.md, 54-RULING.md, and both gap registers byte-unchanged vs HEAD
