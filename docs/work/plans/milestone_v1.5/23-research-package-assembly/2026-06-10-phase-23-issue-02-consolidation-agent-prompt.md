---
status: active
purpose: other
created: 2026-06-10
milestone: v1.5
phase: 23-research-package-assembly
retirement_trigger: final resolution doc delivered under research_reports/02-data-pipeline-and-validation/ and v1.5 adjudication phases complete
---

# Consolidation Agent Prompt — Issue 02 (Data Pipeline and Validation) Final Resolution

## Operator notes (not part of the prompt)

- **Where this fits:** this is **Stage 2** of the v1.5 external research pipeline (same process
  that produced the v1.4 resolution doc). Stage 1 — the companion prompt
  `2026-06-10-phase-23-issue-02-external-research-agent-prompt.md` (same folder) — is sent
  verbatim to multiple independent research agents, each producing an individual research
  report. Stage 2 — this prompt — is sent to one final consolidation agent together with all
  Stage-1 reports. Its output is the final resolution doc.
- **What to attach (4 files; bundles live in
  `research_reports/02-data-pipeline-and-validation/consolidation_input/`):**
  1. `research_package/RESEARCH-CONTEXT-MASTER.md` — the consolidated research-context master
     holding the manifest, framed questions, CLM claims register, dataset context, and
     correction provenance. The consolidator must be able to verify report positions against
     the primary materials, not consolidate hearsay.
  2. `consolidation_input/specs-bundle.md` — all five `research_package/specs/` snapshot
     files, byte-verbatim in one file with `===== BEGIN FILE <name> =====` delimiters.
  3. `consolidation_input/research-results-bundle.md` — all eight Stage-1 reports,
     byte-verbatim in one file, anonymized as R1–R8 with `===== BEGIN REPORT R<n> =====`
     delimiters.
  4. `research_package/DATA-07-CORRECTION-ADDENDUM.md` — shipped 2026-06-11; attach up front.
     If a further Phase-24 correction update lands mid-task, forward it the moment it does —
     the prompt tells the agent how to treat it.
- **Anonymization:** the R-tag → report-file mapping lives only in
  `consolidation_input/BUNDLE-MANIFEST.md`, which is deliberately NOT uploaded; de-reference
  report provenance there after the output lands. (Repo-side note: report bodies are verbatim
  and may self-identify — see the manifest's self-ID scan column; byte sizes in the uploaded
  bundle header are also distinguishing, R4 notably so — the prompt's Independence ground rule
  is the mitigation.)
- **Revision note (2026-06-11):** attach list rebundled to 4 files; reports anonymized R1–R8;
  crosswalk section added; Output-contract conformance pass added to Method. Design:
  `docs/superpowers/specs/2026-06-11-issue02-research-results-consolidation-packaging-design.md`.
- **Where the output goes:** save the final document under
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`
  (suggested name in the v1.4 spirit: `data_pipeline_resolution.md`). Place the Stage-1
  individual reports in the same directory (v1.4 layout precedent: `ctl_pinn_resolution.md`
  beside the four model reports). **Only the Stage-2 output is the candidate verdict source**;
  the individual reports are supporting evidence, consulted during adjudication when the final
  doc's consolidation provenance records ambiguity.
- **Gate:** the final doc's arrival, together with Phase 24 completion, opens adjudication
  Phases 25–29.

---

<!-- PROMPT BEGINS — copy everything below this line into the consolidation agent session -->

# Consolidation Task: Produce the Final Resolution Document from Independent Research Reports

## Role

You are the final consolidation analyst for a computational-physics research project that trains
a physics-informed neural network on high-precision three-body gravitational simulation data.
Several independent research agents were each given the same self-contained research package and
the same instructions, and each produced a resolution report answering the same question set.
You have been given the package and all of those reports. Your job is to critically consolidate
them into the single, final resolution document the project will act on.

## Inputs

1. **The research package** — `RESEARCH-CONTEXT-MASTER.md` (its "Package Orientation And
   Manifest" section defines every file's role and authority level; its "Framed Research
   Questions" section is the complete question set; its "CLM Claims Register" and
   "Consolidated Dataset Context" sections carry the factual baseline) and the spec snapshots
   inside `specs-bundle.md` (five files, each delimited by `===== BEGIN FILE <name> =====` /
   `===== END FILE <name> =====` lines).
2. **The independent research reports** — eight, inside `research-results-bundle.md`,
   anonymized as `R1`–`R8` and each delimited by `===== BEGIN REPORT R<n> … =====` /
   `===== END REPORT R<n> =====` lines; the bundle header's Contents table enumerates them.
   Treat them as argued candidate positions, nothing more.
3. **A correction addendum** — empirically verified values for figures the package marked
   `claimed-unverified`, provided up front. An updated version may be forwarded mid-task.

Read in this order: the master's manifest section → its question set → every report in the
bundle in full (R1–R8) → then the master's "CLM Claims Register" and "Consolidated Dataset
Context" sections and the `specs-bundle.md` contents as adjudication requires.

## Report coverage and verdict crosswalk (navigation aid)

> Navigation aid only, transcribed from each report's decision matrix by the project.
> Non-authoritative: the full report text in the bundle prevails over this table. Do not
> treat it as evidence or as your agreement classification — perform Method step 2 yourself
> from the full text.

Legend (structure only; byte sizes are of the original report files):

- **R1** — 58 KB; `##` Cluster A/B/C resolutions, no per-question subheadings
- **R2** — 55 KB; bare `Resolutions` parent + `Step 1A` + `Pre-training` subsections
- **R3** — 70 KB; §3.x Q-A1..Q-A6, §4.x Q-B1..Q-B4, §5.x Q-C1..Q-C4
- **R4** — 126 KB; §3.x, §4.x, §5.x with long-form verdicts and constraint-anchored analysis
- **R5** — 16 KB; `## 1 Decision Matrix` + `## 2 Cluster A` with Q-A1..Q-A5 subsections only
- **R6** — 52 KB; issue-ID-keyed (B-/M-/D-); §3.1..§3.8 sections; Q-IDs absent
- **R7** — 57 KB; Q-ID-prefixed `###` subheadings; no §-numbers
- **R8** — 58 KB; Q-ID-prefixed `###` subheadings; no §-numbers

Cell forms: `<verdict gist> (<section>)` — full resolution section exists there;
`matrix-only (<section>)` — covered only as a decision-matrix row at that section;
`—` — not addressed anywhere in the report; `see <section>` — verdict too nuanced to
compress faithfully, read the section.

### Cluster A — Ingestion & Selection

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-A1 (B-06) | post-metrics admission gate; reject >=200 (Cluster A) | post-metrics eligibility gate; reject >=200 (Step 1A) | post-metrics admission gate; final_t>=9.5, n_snap>=2 (§3.1) | admission gate init; final_t>=9.5; reject >=200 (§3.1) | enforce final_t>=9.5; reject arbitrary snapshot bounds (Q-A1) | TrajectoryValidator at init; block causal firewalls (§3.1) | completeness gate; final_t>=9.5, n_snap>=2; reject >=200 (Q-A1) | resolution-aware gate; final_t>=9.5 + snap>=N_min(variant,stage) (Q-A1) |
| Q-A2 (B-11) | explicit scanned manifests; ID != index (Cluster A) | ID by physical/record keys; no array index (see Resolutions) | folder-scanned TrajectoryIndex; no dense array index (§3.2) | ID = (variant folder, zero-padded ID); scan-built (§3.2) | TrajectoryIndex mapping; no linear array indexing (Q-A2) | TrajectoryIndex mapping; resolve O(N) filter gaps (§3.2) | id_to_path dictionary from scan; no linear indexing (Q-A2) | TrajectoryIndex from scan; ID==index invalid (Q-A2) |
| Q-A3 (M11) | mandatory blacklist load; fail closed (Cluster A) | blacklist at trajectory level across fidelities (see Resolutions) | load+enforce blacklist at load; fail closed (§3.3) | blacklist load blocking; fail hard if missing (§3.3) | blacklist at init; loudly exclude listed IDs (Q-A3) | blacklist at training time; protect LayerNorm + SIREN (§3.3) | blacklist at init; log exclusions; fail-loud on batch (Q-A3) | blacklist at init; unconditional; RuntimeError on batch (Q-A3) |
| Q-A4 (M13) | no fallback stage; retain in low-fidelity pool (Cluster A) | no low-fidelity Stage-5 substitute; mark non-upgradable (see Resolutions) | STOP-gap; no silent low-fidelity substitution (§3.4) | no fallback under locked stages; keep in replay (§3.4) | STOP-gap; insufficient evidence to adjudicate (Q-A4) | low-fidelity fallback with metadata flags (§3.5) | STOP-gap; insufficient evidence to choose fallback (Q-A4) | STOP gap; three policy options; human adjudication (Q-A4) |
| Q-A5 (D7) | footers optional; folder defaults + provenance (Cluster A) | missing footers absent metadata; folder defaults (see Resolutions) | footers optional; folder defaults + provenance (§3.5) | footer present->parse; absent->folder defaults; provenance (§3.5) | folder defaults for missing footers; flag inferred (Q-A5) | infer tol=1e-13 incomplete footers; tol_confidence flag (§3.6) | folder-default fallback; provenance DIRECT/INFERRED_FOLDER_DEFAULT (Q-A5) | three-tier fallback; direct/folder/provenance flag (Q-A5) |
| Q-A6 (D-03) | HDF5 canonical; .npy derived cache only (Cluster A) | HDF5 canonical; .npy derived; JSON inspection-only (see Resolutions) | HDF5 canonical; .npy schema-equivalent; JSON inspection (§3.6) | HDF5 primary; .npy spec-compliant; JSON inspect-only (§3.6) | matrix-only (1 Decision Matrix) | — | HDF5 primary; .npy acceptable; JSON inspection (Q-A6) | HDF5 primary; .npy acceptable; JSON debug-only (Q-A6) |

### Cluster B — Sampling, Precision & Global Scale

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-B1 (M12) | n_pts = max(2, min(32, floor(0.5*N_t))) (Cluster B) | n_pts_eff = min(32, N_valid); reject 0.5*n_snapshots rule (see Resolutions) | n_pts = min(32, N_snap, max(2, floor(0.5*N_snap))) (§4.1) | n_pts = min(cap, n_snap) without replacement (§4.1) | matrix-only (1 Decision Matrix) | adaptive 0.5 * n_snapshot cap; prevent interpolation blindness (§3.4) | n_pts = min(32, int(0.5*n_snapshots)) (Q-B1) | n_pts = min(32, max(4, floor(0.5*n_snap))) (Q-B1) |
| Q-B2 | IC<->Brutus rtol=1e-15; Decimal on fail (Cluster B) | full-population IC<->Brutus t=0 mass scan (see Resolutions) | rtol=1e-15 atol=0; full scan; Decimal diagnosis (§4.2) | all IC-Brutus pairs; max abs delta_m < 1e-15 (§4.2) | matrix-only (1 Decision Matrix) | — | np.allclose rtol=1e-15; Decimal if >1% failure (Q-B2) | two-tier: 1000-pair statistical + float64/Decimal mode (Q-B2) |
| Q-B3 | float64 sufficient; Decimal for literal mass (Cluster B) | float64 metrics; Decimal for text-equivalence only (see Resolutions) | float64 metrics; Decimal mass audit only (§4.3) | float64 sufficient; Decimal escalation diagnostic only (§4.3) | matrix-only (1 Decision Matrix) | — | float64 sufficient; Decimal for mass check (Q-B3) | float64 sufficient; Decimal for mass consistency (Q-B3) |
| Q-B4 | D ~ 4.6416; reject D=6.694 (Cluster B) | D ~ 4.6416 locked; no D=6.694 (see Resolutions) | D ~ 4.6416; D=6.694 rejected (§4.4) | D = (G*T^2)^{1/3} ~ 4.6416; reject 6.694 (§4.4) | matrix-only (1 Decision Matrix) | — | D ~ 4.6416; D=6.694 requires rewrite (Q-B4) | parameterize D; default None->PHYS-01 D~4.6416; await EVID-10 (Q-B4) |

### Cluster C — Validation Metrics

| Question | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Q-C1 (SCS) | SCS = log10(eps_H); reject SCS >= -5 (Cluster C) | log-drift SCS; reject SCS >= -5; store raw + log (Pre-training) | SCS = log10(eps_H); reject SCS >= -5; raw ratio != gate (§5.1) | SCS=log10 eps_H; reject SCS >= -5 (§5.1) | matrix-only (1 Decision Matrix) | reject eps_H > 1e-5; SCS >= -5; 1e-6 diag-only (§3.8) | locked SCS > -5; ratio thresholds different (Q-C1) | SCS=log10(eps_H); four-tier; reject SCS > -5 locked (Q-C1) |
| Q-C2 (SASD) | local turning-angle proxy; flag max >= 0.5 (Cluster C) | curvature-resolution via perp acceleration; flag max >= 0.5 (Pre-training) | normalized-time SASD + validation acceleration; flag max >= 0.5 (§5.2) | SASD = delta t * max norm(a) / max norm(v); flag max >= 0.5 (§5.2) | matrix-only (1 Decision Matrix) | — | SASD = delta t * norm(a) / norm(v); flag max > 0.5; eps=1e-10 (Q-C2) | SASD = delta t * norm(a) / norm(v); robust turning-point; flag max > 0.5 (Q-C2) |
| Q-C3 (IPR) | cubic Hermite eps=1e-10; flag IPR >= 1e-3 (Cluster C) | cubic Hermite + static eps 1e-10 (Pre-training) | validation eps 1e-10 for IPR; flag IPR >= 1e-3 (§5.3) | cubic Hermite PCHIP; eps=1e-10; flag IPR >= 1e-3 (§5.3) | matrix-only (1 Decision Matrix) | — | cubic Hermite; static eps=1e-10; doc's 1e-5 conflict (Q-C3) | IPR = mean PCHIP residual; eps=1e-10; flag IPR > 1e-3 (Q-C3) |
| Q-C4 (PSC) | quantile-bin Shannon on invariant vector (Cluster C) | dedup trajectory-level grid; omit Q from proxy (Pre-training) | fixed projected phase-space entropy + Miller-Madow; diagnostic only (§5.4) | dataset-level Shannon entropy on (log d_min, log d_mid) (§5.4) | matrix-only (1 Decision Matrix) | — | Shannon entropy; 6D pairwise-distance/velocity binning (Q-C4) | Shannon entropy 2D (r_12, r_23) grid; normalized recommended (Q-C4) |

## What consolidation means here

- **Not a merge, not a vote, not a summary.** For every question you re-adjudicate: the reports
  supply competing argued positions; the package supplies the primary evidence; you decide on
  the merits.
- **Agreement is not correctness.** Independent agents can share the same blind spot. A
  unanimous position must still check out against the package materials and first principles
  before you adopt it.
- **A minority — or single-report — position prevails when its evidence is better.** Never
  decide by majority count.
- **Never average or split numeric differences.** Where reports recommend different values or
  procedures, adopt one on the merits, or report the question unresolved together with the
  discriminating test that would settle it.
- **You may reject all reports' positions** on a question and substitute your own, provided you
  flag it as consolidator-original and argue it fully from the package evidence.
- **Every question gets answered.** If a question was skipped or answered inadequately by every
  report, work it directly from the package yourself and flag that no report covered it.

## Ground rules

1. **The package and the reports are your complete input.** You have no access to the project's
   repository. Do not assume unstated facts. If a final answer genuinely requires information
   not present in any input, record it in an "Additional Input Needed" register naming the exact
   missing item — do not guess.
2. **Authority levels:** the package manifest's authority levels bind. The issue consolidation
   material in the package is NOT authoritative, and **neither are the research reports** — a
   statement is not correct because a report asserts it, however confidently.
3. **Claims discipline:** figures marked `claimed-unverified` in the master's "CLM Claims
   Register" section remain unconfirmed unless the correction addendum verifies them. Where the addendum contradicts a
   figure any report relied on, the addendum wins — re-evaluate every report position that
   depended on the contradicted figure. Where no addendum value exists, keep verdicts that turn
   on such a figure in explicit conditional form ("if the verified value is X, then …;
   otherwise …").
4. **Hard constraints are fixed.** The package lists locked project conventions as hard
   constraints. Any report recommendation that violates one must be rejected or flagged as an
   explicit constraint conflict — never adopted, and never silently softened to fit.
5. **Scope boundary:** the package marks certain topics as out of scope or deferred. If a report
   strayed beyond that boundary, exclude that content from the final document and note the
   exclusion; do not let report scope creep widen the final document's scope.
6. **Independence:** weigh arguments, not sources. Do not weight positions by which agent or
   model produced them, by report length, or by rhetorical confidence.

## Method

For each question in the master's "Framed Research Questions" section:

1. **Collect** each report's position on the question (including "not addressed"). The
   crosswalk section above may be used to locate positions quickly — never as a substitute
   for reading the report's full text.
2. **Classify agreement** — unanimous / majority–minority / fully split / single-report-only /
   unaddressed.
3. **Verify** the candidate positions against the package evidence and first principles; check
   citations actually support what they are cited for.
4. **Decide** — adopt one position, synthesize a defensible combination (only where the elements
   are genuinely compatible, not as a compromise), substitute a consolidator-original position,
   or declare the question unresolved with the discriminating test.
5. **Record provenance** — which positions were adopted, rejected, or merged, and why; preserve
   dissenting positions in summary rather than erasing them.

Before finalizing, run three passes:

- **Consistency pass:** check the final answers against one another and against the hard
  constraints; resolve or explicitly flag any conflict.
- **Completeness audit:** every question answered; every claim-dependent verdict conditional or
  addendum-grounded; every citation resolvable to an input you were actually given.
- **Output-contract conformance pass:** check the document against the Output specification
  below before returning — every specified section present, every per-question resolution
  carrying all seven required parts, and every final verdict specified to the transcription
  level a specification author could apply without further interpretation. This document is the
  candidate verdict source the project will act on; record any required part you cannot supply
  as an explicit Open items / Additional Input Needed entry rather than omitting it silently.

## Output specification

Produce **one** self-contained markdown document — the final resolution document:

- **Header:** title, date, and an inventory of inputs received: every package file and every
  report (reports identified by bundle tag R1–R8), plus whether a correction addendum was
  received.
- **§0 Scope and decision standard:** what you covered, what you excluded per the package's
  scope boundary, and the evidence standard you applied.
- **§1 Executive decision summary:** the complete set of final recommendations, in brief.
- **§2 Decision matrix:** one row per question — question ID, one-line final verdict,
  confidence, and agreement classification across the input reports.
- **§3+ Resolutions:** per-question sections following the grouping and identifiers used in
  the master's "Framed Research Questions" section. Each contains:
  1. **Final verdict / recommendation** — specified to the level that a specification author
     could transcribe it without further interpretation: exact definitions, formulas, threshold
     values, procedures, and edge-case behavior where applicable.
  2. **Reasoning** — the argument from evidence and first principles.
  3. **Evidence** — citations to package files (file + section) and, where used, external
     literature carried over from the reports, with full citations.
  4. **Confidence** — High / Medium / Low, plus the single most important factor that would
     change the answer.
  5. **Verification suggestion** — how the project could independently check the
     recommendation.
  6. **Proposed specification text** where the recommendation implies changing the provided
     specifications, anchored to the specific spec file and section it would modify.
  7. **Consolidation provenance** — each report's position in one line each; which was adopted,
     rejected, or merged and why; dissents preserved in summary.
- **Open items register:** every "insufficient evidence" and "Additional Input Needed" item,
  consolidated across the reports and your own analysis.
- **References:** full citations for all external sources relied on.

Formatting: plain markdown (no HTML); LaTeX notation for mathematics is fine; use the package's
question identifiers and claim identifiers verbatim as anchors throughout.

## Quality bar

Your output becomes the **candidate verdict source** for a formal adjudication process: every
recommendation will be independently re-verified against the project's specifications, dataset,
and first principles before anything is adopted, and nothing is accepted on authority. The
project will consult the individual reports again **only where your consolidation provenance
records ambiguity or a close call** — so make the provenance honest and complete rather than
presenting false unanimity. Write so a skeptical reviewer can check every claim you make.

<!-- PROMPT ENDS -->
