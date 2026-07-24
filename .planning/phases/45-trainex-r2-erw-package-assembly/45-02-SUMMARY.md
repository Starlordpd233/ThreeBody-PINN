---
plan: "45-02"
phase: 45-trainex-r2-erw-package-assembly
status: complete
completed: 2026-07-24
wave: 2
requirement: PKG-09, PKG-10, PKG-11
---

# 45-02 Summary — claims register and research-context master

## What was built

The intellectual core of the trainex-r2 package: the standalone PKG-11 claims
register (D-03/D-09) and the PKG-10/PKG-09 `RESEARCH-CONTEXT-MASTER.md` — the
external agent's single entry point with the 4-attachment manifest, source
tiering (D-12), five neutrally framed questions (D-04/D-05/D-06), the folded-in
claims register (D-03), dual provenance pins (D-07), and the specwork-style
neutral output contract (D-04).

## source_baseline (matches 45-01)

`source_baseline = 9b1f0e7a4735df1c54867530cfd1f13b390e1514` — identical to the
45-01 bundles (confirmed). Complementary diagnosis evidence pin
`8631576dc5d8f76d1d0b301895ec5014161941cc` surfaced in the master §6.

## Claims-register reconciliation (D-09 direct lift)

- **23 `[FACT]` inline tags → 16 `F-` rows (F-01..F-16)**, with merges:
  gate-FAIL numbers (§1/§2/GAP-44-01) → F-01/F-05/F-15; distribution statistics
  (§1/§2.1) → F-02/F-03; Phase-38 overfit control (§1/§4) → F-06; §8
  provenance → F-16.
- **7 `[HYP]` inline tags → 8 `H-` rows (H-01..H-08)**: §1 emergence → H-01;
  §5 rubric → H-02; the §6 interpretation tags + 5 candidate-table rows →
  H-03..H-07 + tie-rationale H-08.
- GAP-44-01 recorded as **owner-instructed (option A, 2026-07-23)** and
  **verdict-neutral** (F-15). No claim was re-judged or newly adjudicated.

## Row-count sync (standalone vs master folded section)

| | standalone CLAIMS-REGISTER.md | master folded section |
|---|---|---|
| F- rows | 16 | 16 |
| H- rows | 8 | 8 |

Match confirmed — the master folds the register verbatim (D-03).

## Per-question neutrality attestation (acceptance criterion 7, manual)

Each "what a complete answer specifies" block describes the **structure** of an
adequate answer and states **no** value, schedule, direction, or preferred
candidate:

- **Q1 (budget/steps):** "a reasoned budget rule that addresses the
  budget/population-scale confound" — no step count stated.
- **Q2 (warmup/LR):** "a warmup/LR-schedule design with stated rationale and
  the per-step diagnostics" — no schedule stated.
- **Q3 (loss weighting):** "a loss-weighting/balancing approach … with the
  weighted-loss/gradient evidence that would justify it" — no weights stated;
  the candidate-4 normalization/data-scale sub-facet is kept **inside** Q3
  (count stays at five).
- **Q4 (curriculum pacing):** "how stage/front_idx progression and the PHYS-05
  ramps should interact within the 300-step budget" — the 300-step figure is the
  verified fact F-10, not a recommendation; no pacing scheme stated.
- **Q5 (evaluation policy):** framed as future-evaluation governance **only**;
  no request to evaluate now; no numeric acceptance bands beyond the locked spec.

Every DIAG-04 candidate mention is `[HYP]`-labeled; every discriminating-test
mention is marked proposal-only / owner-authorization-gated (D-06, SCOPE-23).
Q3 contains the candidate-4 sub-facet; Q5 is governance-only (acceptance
criteria 1 and 4).

## Self-Check: PASSED

- Task 1 gate: 16 F- rows (≥12), 8 H- rows (≥7); `GAP-44-01`,
  `not established fact`, `verdict-neutral`, `source_baseline` present; zero
  banned repo-path markers.
- Task 2 gate: exactly 5 `Q[1-5]` headings; `source_baseline`, the diagnosis
  evidence pin `8631576…`, `attached files only`, `not recommend`,
  `not established fact` present; 16 F-/8 H- folded; **negative grep for
  `suggest defaults` passes** (the build-design directive is absent — D-04);
  zero banned repo-path markers.
- `git status --short` shows only the two new files (no spec/seed edits).

## Notes for downstream plans

- The master's output contract (§7) is the specwork neutral contract (D-04),
  explicitly **without** Rule 7's build-design default-suggestion directive —
  45-03's paste-ready prompt must carry this same contract verbatim.
- The four attachment filenames are fixed: RESEARCH-CONTEXT-MASTER.md,
  44-DIAGNOSIS.md, framework-specs-bundle.md, run-evidence-bundle.md — 45-03's
  prompt header and delivery-note upload list must name exactly these four.
- The two D-13 carried-forward todos are **not** pre-answered here; they surface
  at the 45-04 owner checkpoint.
