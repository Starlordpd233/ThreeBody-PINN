---
plan: "45-01"
phase: 45-trainex-r2-erw-package-assembly
status: complete
completed: 2026-07-24
wave: 1
requirement: PKG-09
---

# 45-01 Summary — trainex-r2 package skeleton, diagnosis snapshot, evidence bundles

## What was built

The trainex-r2 ERW package tree (D-01 single sub-package) plus the PKG-09
commit-pinned snapshot substrate: a byte-identical diagnosis snapshot and the
two cap-compliant upload bundles. Pure assembly/curation — no analysis,
evaluation, training, spec edit, or remedy selection (SCOPE-22..26).

## source_baseline (phase-wide provenance pin — D-07)

`source_baseline = 9b1f0e7a4735df1c54867530cfd1f13b390e1514`

Captured as repo HEAD immediately before any Wave-1 commit (all snapshot
sources are committed at this HEAD). Recorded identically in both bundle
frontmatters; reused verbatim by Plans 45-02 (master) and 45-03 (delivery note).

## Diagnosis snapshot — byte-identical (D-08)

`44-DIAGNOSIS.md` copied verbatim from Phase 44 into `research_package/`.
Internal citations retained (nothing scrubbed — ERW Rule 1 verbatim-snapshot
exemption). Verified `diff -q` clean and SHA-256 identical:

- source `.planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md`
- snapshot `research_package/44-DIAGNOSIS.md`
- **SHA-256 (both):** `466000bc874011f5298738ef01b8cb13e364bae895218fd95eaf3f385cf77236`

## Complementary diagnosis evidence pin (D-07 — do NOT overwrite)

The diagnosis carries its own deeper evidence pin in its §8 provenance and
`evidence/manifest.json`: `git_head = 8631576dc5d8f76d1d0b301895ec5014161941cc`,
15 inputs by SHA-256, `cross_check.all_match: true`. This is complementary to
`source_baseline` (package baseline vs diagnosis evidence tree) and must be
surfaced in the master, never overwritten.

## Files created (upload-slot map)

| Path (under `framework-specs/trainex-r2/`) | Upload slot | Created by |
|---|---|---|
| `research_package/44-DIAGNOSIS.md` (verbatim) | attachment 2 | 45-01 |
| `specs/framework-specs-bundle.md` | attachment 3 | 45-01 |
| `research_package/run-evidence-bundle.md` | attachment 4 | 45-01 |
| `research_results/.gitkeep` (empty landing dir) | never | 45-01 |

Attachment 1 (RESEARCH-CONTEXT-MASTER.md) lands in Plan 45-02. The paste-ready
prompt and DELIVERY-NOTE.md land in 45-03 (never uploaded). Total uploads = 4
of at most 5 (ERW Rule 15).

## Self-Check: PASSED

- Task 1 automated gate: `test -d specs && test -d research_package && test -f
  research_results/.gitkeep && diff -q diagnosis == 0 && ! resolution-doc.md &&
  ! research_package_a` — PASS.
- Task 2 automated gate (framework-specs-bundle.md): 6 `^Source:
  (ctl_instruction|pinn_architecture)\.md` lines (≥5); `eps_H`, `PHYS-05`,
  `source_baseline` present; **zero** banned repo-path markers — PASS.
- Task 3 automated gate (run-evidence-bundle.md): `237.2086`, `Source:
  43-CALIBRATION.md`, `Source: 43-VERDICT.md`, `grad_norm`, `budget` present;
  258 lines (≤600); `source_baseline` present; **zero** banned repo-path
  markers — PASS.
- SCOPE-24: `git status --short` shows `ctl_instruction.md` and
  `pinn_architecture.md` unmodified (read-only excerpt sources).

## Notes for downstream plans

- Bundles use bare-filename + line-range citations and a top-of-file
  path-abbreviation note (D-11). The Phase-35 provenance annotations inside the
  spec text were condensed to their **normative content** (retain / reject /
  defer) with the internal evidence-packet path abbreviated — no number,
  formula, threshold, or normative decision was altered.
- The run-evidence verdict section retains the full exhausted-evaluator-budget
  record (Attempts 1/2/3) — this is the SCOPE-22 grounding for 45-02's Q5
  evaluation-policy question.
- The framework-specs bundle flags (Excerpt 5) that under PHYS-05, Stage 0
  (`k ∈ {0,1}`) sets `lambda_E^max = lambda_L^max = 0` — directly relevant to
  45-02's Q2/Q3 framing.
