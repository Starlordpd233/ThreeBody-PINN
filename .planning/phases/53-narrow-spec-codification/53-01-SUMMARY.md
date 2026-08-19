---
phase: 53-narrow-spec-codification
plan: 01
subsystem: spec
tags: [framework-specs, adjudication, ver-20, scope-38, render-oracle]

requires:
  - phase: 45-trainex-r2-erw-package-assembly
    provides: GAP-45-03 (PHYS-05 table locked) and GAP-45-01 (L_data mean reduction) owner rulings
  - phase: 44-physics-gate-forensics
    provides: GAP-44-01 (held-out physics-gate worst-case max) owner ruling
  - phase: 52-diagnosis-re-derivation-handoff
    provides: VER-20 routing handoff items (a)-(d)
provides:
  - Locked-vs-default value-attached marker convention ([LOCKED] / [DEFAULT]) declared in pinn_architecture.md
  - PHYS-05 per-stage lambda^max(k) values marked locked in section 4.1, with the misleading "default" wording removed
  - Explicit L_data mean reduction (formula + prose) in section 3.1
  - New subsection 10.6 defining the held-out physics-gate aggregate statistic
  - 53-UNSWEPT-INVENTORY.md — the D-01 routed inventory of 7 deliberately unmarked wordings
affects: [phase-56-contract-amendment, phase-58-traceability-close]

actuals:
  tokens: 3910
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Value-attached ASCII status markers (**[LOCKED]** / **[DEFAULT]**) as a spec-wide convention"
    - "Phase NN contract blockquote citing a GAP ruling (id + date + option letter + archived grounding path) instead of minting a new AC-* id"

key-files:
  created:
    - .planning/phases/53-narrow-spec-codification/53-UNSWEPT-INVENTORY.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
    - tools/spec-render-check/adjudications/22-02-pinn-architecture.json

key-decisions:
  - "Contract-block heads render symbols as inline math rather than bare text (deviation from the plan's verbatim head string) because bare multi-char subscripts trip the render oracle's D3 rule; all load-bearing citation content is unchanged."
  - "The warmup-form symbol is named in words rather than as a symbol in the section 4.1 contract block, satisfying both the render oracle and the SPEC-02 numeric-preservation gate."
---

# Phase 53 Plan 01 — Summary

Transcribed four already-ratified owner rulings into
`pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`,
the only framework spec this phase edited. Every edit is a transcription; no
value or formula carrying an owner-ratified contract marker was changed.

## Commits

| # | SHA | Subject | Requirements |
|---|-----|---------|--------------|
| 1 (tracer) | `a2bc4fd0ebb0b75476264af04edb83f8d288606a` | `spec(53): add locked-vs-default marker convention and mark PHYS-05 table locked` | SPEC-02, SPEC-03 |
| 2 | `6f11a097f10b3e284e582fef44a2ebd9bcd3f526` | `spec(53): state L_data mean reduction per GAP-45-01 ruling` | SPEC-04 |
| 3 | `3e9f94daa2658c94a71b1f1ca313f4a86e8d5b11` | `spec(53): codify held-out physics-gate max statistic per GAP-44-01` | SPEC-05 |

## Preamble line count and adjudication re-key

The convention preamble inserted **N = 14** lines (13 content lines plus one
trailing blank) immediately after the title and before `# 1.`, so it sits well
above the first author-flag render window.

All 7 entries in `tools/spec-render-check/adjudications/22-02-pinn-architecture.json`
were re-keyed by exactly **+14** in the same commit as the insertion:

| Before | 170 | 188 | 236 | 238 | 259 | 260 | 261 |
|--------|-----|-----|-----|-----|-----|-----|-----|
| After  | 184 | 202 | 250 | 252 | 273 | 274 | 275 |

Tasks 2 and 3 edited only regions below line 261, so no further re-key was needed.

## Render-oracle counts

| Run | Exit | DEFINITE | REVIEW | ADJUDICATED | SUPPRESSED |
|-----|------|----------|--------|-------------|------------|
| Baseline (pre-edit) | 1 | 0 | 12 | 7 | 14 |
| Final (post-Task 3) | 1 | 0 | 12 | 7 | 14 |

The REVIEW token set on the final tree is **identical** to the baseline's
12 tokens (line numbers shifted; tokens did not grow), verified by a
line-number-stripped diff of the two runs. The gate required exit ≤ 1,
0 DEFINITE, 7 ADJUDICATED, and REVIEW ⊆ baseline — all met.

Two iterations were needed to reach that state, both against the same oracle
rule (D3, bare multi-character subscript outside math):

1. Task 1's contract block originally named the warmup-iteration symbol in
   plain text, adding a 13th REVIEW. The symbol is now named in words. It could
   not simply be wrapped in inline math, because the braced form matches the
   SPEC-02 numeric-preservation gate's regex and would have broken the
   pre/post numeric multiset equality.
2. Task 2's contract-block head carried the loss symbol as bare text, adding a
   13th REVIEW. It is now inline math. See the deviation note below.

## Gate results

- **SCOPE-38 negative diff** — empty on every one of the three commits, checked
  individually with `git show -U0 <sha> -- <spec> | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow'`.
- **SPEC-02 numeric preservation** — the multiset of numeric tokens on the edited
  λ bullets is identical pre/post; the section 4.1 edit is status wording only.
- **Author-note preservation** — `grep -c 'Author Comment'` returns **8** on the
  final tree and at every commit; the note beneath the section 3.1 formula is
  byte-identical.
- **Scope guard** — zero diff in `pinn/`, `tests/`, `simulation_data/`, and
  `ctl_instruction.md`. The phase's full diff touches exactly three files:
  the spec (40 lines changed), the adjudication JSON (14), and the new
  inventory (32).
- **Citation fidelity (manual row)** — each of the three `> **Phase 53 contract:`
  blocks was read back and cross-checked against its archived GAP record:
  GAP-45-03 "Owner instruction 2026-07-24 … Option A"
  (`45-GAPS.md:317`), GAP-45-01 "Final resolution 2026-07-31 (Phase 48 owner
  checkpoint): Option A" (`45-GAPS.md:114`), GAP-44-01 "Owner instruction
  2026-07-23 … Option A" (`44-GAPS.md:111`). Both cited archived paths resolve.

## Gap files

**None created.** No STOP fired. The one anticipated candidate — whether
`ε_H`'s *within-trajectory* reduction is undefined (53-CONTEXT.md Open Item 3) —
was checked directly and is **DEFINED**: `ctl_instruction.md:565-567` states
`eps_H = max_t |(H(t) - H(0)) / H(0)|`, `SCS = log10(eps_H)` inside the locked
conservation gate. Subsection 10.6 therefore cites that definition by section
name and defines only the aggregate across trajectories, per D-05. Neither
`53-GAPS.md` nor `.planning/milestones/v2.3-GAPS.md` exists.

## Deviations

1. **Contract-block head symbol rendering (Task 2).** The plan specified the
   verbatim head `> **Phase 53 contract: L_data component reduction (SPEC-04; …)`.
   Written as bare text, `L_data` trips the render oracle's D3 rule and adds a
   13th REVIEW finding, violating the phase's own REVIEW ⊆ baseline gate. The
   head now renders the symbol as inline math. RESEARCH records that head
   wording is planner discretion while "dates/options/paths are load-bearing";
   all load-bearing content — requirement id, gap id, date, option letter,
   archived grounding path — is unchanged. Classified mechanical /
   presentation-only under the CLAUDE.md STOP protocol, so recorded rather than
   surfaced as a gap.
2. **Warmup symbol named in words (Task 1).** Same D3 cause, but inline math was
   unavailable as a fix because the braced symbol matches the SPEC-02 numeric
   gate's regex. The contract block says "the warmup-iteration count and the
   linear ramp" instead. No content lost; the warmup form's retention under the
   Phase 35 LOSS-02 contract is still stated.
3. **Execution mode.** Executed inline and sequentially on this working tree
   rather than via worktree-isolated executor subagents. `gsd-tools worktree
   base-check` returned `shouldDegrade: true` / `head-diverged-from-fork`
   (HEAD `bb221ae9` on `milestone/v2.3` vs `origin/HEAD` `b8b39a44`), which forces
   `ISOLATION=none` under the #683 auto-degrade; a STOP-protocol phase also keeps
   gap ownership with the parent agent. The plan is a single strictly-sequential
   plan, so no parallelism was available to lose.

## Open Items for Owner Visibility

Carried forward from 53-CONTEXT.md for review at phase close:

1. **§2.4's "Recommended Value" header stays wrong after Phase 53.** The spec now
   carries a declared LOCKED/DEFAULT convention while `pinn_architecture.md`
   still labels `first_omega_0 = 30` a "Recommended Value" — a value §2.2 locks
   and that Phase 56 may amend under SCOPE-38. This is deliberate: marking it
   here would couple this phase to the recalibration outcome and destroy the
   independence that is Phase 53's reason to exist. **Routed to Phase 56**, first
   item of the D-01 inventory.
2. **Correcting a displayed formula (D-03) is a larger edit than "reword".** The
   section 3.1 data-fidelity formula was changed, not merely annotated, because
   Success Criterion 3 cannot otherwise be met — a reader following the old
   `1/N_t` double sum would compute 9× the ratified quantity. Judged in-scope
   because the reduction was never contract-marked (the adjacent LOSS-01 block
   fixes scaling, units, and component-math ownership but not the reduction).
   **Flagged for owner review at phase close.**

## Requirements

SPEC-02, SPEC-03, SPEC-04, SPEC-05 are all discharged in the spec text. Per
house precedent (CONF-09 / CONF-02 / RUN-01 / RUN-02), the executor did **not**
flip their checkboxes in `.planning/REQUIREMENTS.md` — that is a
phase-close/verification act.
