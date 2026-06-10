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
- **What to attach:**
  1. The full `research_package/` (same set as Stage 1: `README.md`,
     `framed-research-questions.md`, `claims-table.md`, `consolidated-context.md`, all of
     `specs/`). The consolidator must be able to verify report positions against the primary
     materials, not consolidate hearsay.
  2. Every Stage-1 individual research report.
  3. The Phase 24 DATA-07 correction addendum, if it has shipped by then. If it has not, forward
     it mid-task the moment it does — the prompt tells the agent how to treat it.
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

1. **The research package** — `README.md` (the manifest; it defines every file's role and
   authority level), `framed-research-questions.md` (the complete question set),
   `claims-table.md`, `consolidated-context.md`, and the files under `specs/`.
2. **The independent research reports** — one per agent. Treat them as argued candidate
   positions, nothing more.
3. **Possibly a correction addendum** — empirically verified values for figures the package
   marked `claimed-unverified`. It may be provided up front or forwarded mid-task.

Read in this order: package manifest → question set → every report in full → then
`claims-table.md`, `specs/`, and `consolidated-context.md` as adjudication requires.

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
3. **Claims discipline:** figures marked `claimed-unverified` in `claims-table.md` remain
   unconfirmed unless the correction addendum verifies them. Where the addendum contradicts a
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

For each question in `framed-research-questions.md`:

1. **Collect** each report's position on the question (including "not addressed").
2. **Classify agreement** — unanimous / majority–minority / fully split / single-report-only /
   unaddressed.
3. **Verify** the candidate positions against the package evidence and first principles; check
   citations actually support what they are cited for.
4. **Decide** — adopt one position, synthesize a defensible combination (only where the elements
   are genuinely compatible, not as a compromise), substitute a consolidator-original position,
   or declare the question unresolved with the discriminating test.
5. **Record provenance** — which positions were adopted, rejected, or merged, and why; preserve
   dissenting positions in summary rather than erasing them.

Before finalizing, run two passes:

- **Consistency pass:** check the final answers against one another and against the hard
  constraints; resolve or explicitly flag any conflict.
- **Completeness audit:** every question answered; every claim-dependent verdict conditional or
  addendum-grounded; every citation resolvable to an input you were actually given.

## Output specification

Produce **one** self-contained markdown document — the final resolution document:

- **Header:** title, date, and an inventory of inputs received: every package file and every
  report (identified by filename or label), plus whether a correction addendum was received.
- **§0 Scope and decision standard:** what you covered, what you excluded per the package's
  scope boundary, and the evidence standard you applied.
- **§1 Executive decision summary:** the complete set of final recommendations, in brief.
- **§2 Decision matrix:** one row per question — question ID, one-line final verdict,
  confidence, and agreement classification across the input reports.
- **§3+ Resolutions:** per-question sections following the grouping and identifiers used in
  `framed-research-questions.md`. Each contains:
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
