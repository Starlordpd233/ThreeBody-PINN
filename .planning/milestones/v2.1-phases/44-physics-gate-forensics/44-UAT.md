---
status: complete
phase: 44-physics-gate-forensics
source: [44-01-SUMMARY.md, 44-02-SUMMARY.md, 44-03-SUMMARY.md, 44-04-SUMMARY.md, 44-05-SUMMARY.md]
started: 2026-07-24T05:45:25Z
updated: 2026-07-24T05:45:25Z
---

## Current Test

[testing complete]

<!--
Phase 44 is a read-only forensics phase: its deliverables are analysis scripts, their
JSON outputs, a pinning manifest, and 44-DIAGNOSIS.md. There is no application under test
and no user-observable UI to click. Per the established approach for trainex acceptance
phases, the verifier runs the semantic/contract checks directly rather than asking the
user to eyeball each. Every result below was agent-verified against the live artifacts,
not hand-confirmed.
-->

## Tests

### 1. Re-derivability — all analysis outputs regenerate byte-identical from pinned inputs (SC-5, D-02)
expected: Re-running the four retained scripts against the pinned inputs reproduces the committed outputs byte-for-byte; the manifest confirms all input hashes still match.
result: pass
source: automated
evidence: |
  Re-ran with ~/miniforge3/envs/pinn-train/bin/python3 (Python 3.11.15, numpy 2.4.6):
  - diag01/eps_h_distribution.json  SHA-256 036e8c40… (unchanged, byte-identical)
  - diag02/loss_decomposition.json  SHA-256 3e644b44… (unchanged, byte-identical)
  - diag03/seed_band.json           SHA-256 3c93be40… (unchanged, byte-identical)
  - build_manifest.py → "15 inputs pinned; all_match=True; git_head_available=True"
  All script self-check (fail-closed) assertions passed. Every input in the CONTEXT
  canonical-refs list is present.
note: |
  manifest.json re-run differs ONLY in its `git_head` provenance stamp
  (8631576… → 4788efb4…), because HEAD advanced two commits (44-05 diagnosis +
  gap-44-01 resolution) after 44-04 was committed. All 15 input SHA-256 hashes are
  unchanged. This is expected, documented behavior (44-04-SUMMARY.md scopes byte-identity
  to "consecutive re-runs at this commit") and is NOT a re-derivability failure — no
  substantive number depends on git_head. Working tree restored to committed manifest.

### 2. DIAG-01 — per-trajectory ε_H distribution over all 1,500 held-out trajectories (SC-1)
expected: A full distribution derived solely from preserved metrics.json (evaluator not invoked), stating with numbers whether failure is uniform or tail-driven.
result: pass
source: automated
evidence: |
  Traced to evidence/diag01/eps_h_distribution.json: min 0.9741251227996501,
  median 2.232675867436938, mean 5.6221870977458295, max 237.2086056078468;
  n_exceeding 1500/1500, frac_exceeding 1.0. Pre-registered verdict (min > 1e-5 strict)
  → UNIFORM failure with heavy right tail. Neither variant nor fidelity separates the
  population (no ≥10× median gap). Script reads only metrics.json — no evaluator call
  (SCOPE-22 respected).

### 3. DIAG-02 — five-term loss decomposition + warmup-spike attribution + PHYS-05 interaction (SC-2)
expected: Per-step, per-term decomposition across stage0-smoke + seeds 41/42/43 identifying the dominant term, attributing each warmup spike, accounting for PHYS-05 scheduled weights.
result: pass
source: automated
evidence: |
  Traced to evidence/diag02/loss_decomposition.json. Warmup spikes (each its own event):
  smoke 194/4.61e9, seed41 123/6.08e9, seed42 100/3.73e9, seed43 169/3.83e9 — loss_phys
  dominant in every spike (seed42 dominant_share_of_total 0.999982…), grad_norm ~5–7e13,
  all finite. PHYS-05: lambda_phys first ≥1.0 at step 31 in all four runs; lambda_l ≡ 0.0
  at all 300 steps in all four runs (asserted). loss_phys dominates raw AND λ-weighted
  cumulative views (no flip). stage0-smoke reported as a separate fourth trace.

### 4. DIAG-03 — three-seed band: budget-limited descent vs recipe instability + Phase-38 control (SC-3)
expected: Per-seed validation trends and spreads with cited evidence, distinguishing budget-limited descent from recipe instability, citing the Phase 38 overfit rung as the machinery-integrity control.
result: pass
source: automated
evidence: |
  Traced to evidence/diag03/seed_band.json. First-vs-last trend: seed41/seed42 improving,
  seed43 worsening → 1/3 worsened. Explicitly DISAGREES with 43-CALIBRATION's "2/3 worsened"
  and attributes the difference to the direction definition (last-window step200→300 vs
  first-vs-last step100→300), adjudicating neither. Final-loss relative span
  3.8224247683129153 reproduces 43-CALIBRATION exactly (cross_check matches_within_1e-9_rel
  true). Held-out splits: smoke == seed42 (identical SHA-256); seed41, seed43 diverge —
  caveat stated that cross-seed magnitude spans different populations. Phase 38 rung cited
  (ratio 1097.6107, ≥1e3 PASS) flagged CITATION-NOT-COMPUTATION, never re-run (SCOPE-23).

### 5. DIAG-04 — 44-DIAGNOSIS.md ranks ≥4 causes, abstains from remedy, routes source-silent call (SC-4)
expected: The report ranks ≥4 candidate causes each with supporting AND contradicting evidence citations, explicitly abstains from remedy selection, and routes any source-silent adjudication to a gap register.
result: pass
source: automated
evidence: |
  44-DIAGNOSIS.md: pre-registered evidence-support rubric stated BEFORE the table; 5 ranked
  causes (population-scale generalization Strong; loss-term imbalance / optimization-warmup /
  normalization-scale Moderate declared tie, alphabetical; insufficient budget Weak). Each
  row carries supporting evidence + contradicting evidence (or an explicit-none sentence,
  per the rubric header) + a proposed-but-never-executed discriminating test. Remedy
  abstinence stated up front and in §7. Both gate criteria addressed (ε_H and aggregate SCS).
  [FACT]/[HYP] separation applied inline for PKG-11. Source-silent call routed to GAP-44-01.
note: |
  Candidate 1 (Strong) uses the rubric's permitted "no contradicting evidence identified"
  form rather than a contradicting citation. Accepted: the DIAGNOSIS rubric and CONTEXT D-13
  both permit "(or explicit none)", and candidate 1 is the genuinely uncontradicted strongest
  cause (uniform failure + proven single-trajectory competence). Honest evidencing, not a gap.

### 6. GAP-44-01 governance — surfaced not decided; owner-resolved; consistent across registers
expected: The max-vs-mean gate-statistic question (D-07, MUST-SURFACE) is recorded as a STOP-protocol gap with the full 11-field schema, resolved by owner instruction (not by an agent), and reflected consistently across the phase register, the milestone index, and the diagnosis.
result: pass
source: automated
evidence: |
  GAP-44-01 in 44-GAPS.md carries the full STOP schema and RESOLVED-WITH-INSTRUCTION
  (owner option A, 2026-07-23, AskUserQuestion): worst-case max IS the gate statistic,
  headline max = 237.2086056078468, verdict-neutral. v2.1-GAPS.md (created on this first
  gap, standing trigger) row + Resolved-gaps section agree. 44-DIAGNOSIS.md §2 table, §6,
  §7, and the GAP-44-01 section designate max as THE gate number with this grounding;
  mean (5.6222) and median (2.2327) remain quoted as distribution facts, not gate numbers.
  Spec codification deferred (SCOPE-24). The gap was surfaced by the phase and decided by
  the owner — correct STOP-protocol handling.

### 7. Scope compliance — read-only forensics; no evaluator, no training, no spec edits, phase-dir writes only
expected: The phase runs no evaluator (SCOPE-22), no training (SCOPE-23), edits no framework spec (SCOPE-24), does no Stage-1/PLAT work (SCOPE-25), selects no remedy (SCOPE-26), and writes only under the phase directory.
result: pass
source: automated
evidence: |
  Re-running all four scripts left the working tree byte-identical to session start:
  0 changes under runs/, pinn/, or pinn_instruction/. Scripts read metrics.json,
  train.log.jsonl, validation.jsonl, splits.json, 43-CALIBRATION.md, 38-VERIFICATION.md,
  and the specs read-only; write only under evidence/. 44-DIAGNOSIS.md §7 states each
  scope boundary and remedy abstinence explicitly. Discriminating tests are proposals for
  owner authorization only — none executed.

## Summary

total: 7
passed: 7
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — all contract checks passed; GAP-44-01 is RESOLVED-WITH-INSTRUCTION, not an open UAT gap]
