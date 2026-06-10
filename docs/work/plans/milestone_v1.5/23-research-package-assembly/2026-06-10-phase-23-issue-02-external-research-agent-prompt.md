---
status: active
purpose: other
created: 2026-06-10
milestone: v1.5
phase: 23-research-package-assembly
retirement_trigger: resolution doc delivered under research_reports/02-data-pipeline-and-validation/ and v1.5 adjudication phases complete
---

# External Research Agent Prompt — Issue 02 (Data Pipeline and Validation) Resolution

## Operator notes (not part of the prompt)

- **When to send:** after Phase 23 delivers `research_package/` (Plan 23-05). The package is the
  agent's complete input; this prompt is only the generic wrapper that starts the task. It
  deliberately contains no research direction — all questions, constraints, claims, and context
  live in the package files.
- **What to attach:** every file in
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/`
  — `README.md` (manifest), `framed-research-questions.md`, `claims-table.md`,
  `consolidated-context.md`, and all files under `specs/`. (`DELIVERY-NOTE.md` is
  operator-facing; attaching it is harmless but not required.)
- **Mid-task addendum:** Phase 24 runs in parallel and produces the DATA-07 correction addendum
  for any package-stated claim that empirical verification contradicts (or a nil addendum if none
  is). Forward it to the in-flight research session as soon as it ships — the prompt already
  tells the agent to expect and incorporate it.
- **Where the output goes:** save the agent's final document under
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`.
  Its arrival, together with Phase 24 completion, opens adjudication Phases 25–29.
- **Reuse:** the prompt works verbatim for one agent or for several run in parallel (v1.4 ran
  four models and consolidated afterward). Whatever lands in the repo is the **candidate verdict
  source** — never authoritative; every recommendation is re-verified during adjudication.

---

<!-- PROMPT BEGINS — copy everything below this line into the research agent session -->

# Research Task: Resolution Document for a Data-Pipeline and Validation Issue Set

## Role

You are an independent senior research analyst engaged by a computational-physics research
project that trains a physics-informed neural network on high-precision three-body gravitational
simulation data. You have been given a self-contained research package. Your job is to
investigate the questions it poses and produce one resolution document with explicit,
fully specified recommendations.

## Task

1. Read the package in this order: `README.md` (the manifest — it defines every file's role and
   authority level), then `framed-research-questions.md` (the complete question set), then
   `claims-table.md`, then the files under `specs/` and `consolidated-context.md` as the
   questions require.
2. Investigate and answer **every** question in `framed-research-questions.md`. The question set
   is the complete and authoritative statement of what this task covers — nothing in this prompt
   adds to it or narrows it.
3. Produce a single, self-contained resolution document in markdown, per the output
   specification below.

## Ground rules

1. **The package is your complete input.** You have no access to the project's repository. Do
   not assume unstated facts about the codebase, dataset, or project history. If an answer
   genuinely requires information the package does not contain, record it in an "Additional
   Input Needed" register naming the exact missing item — do not guess.
2. **Respect the authority levels stated in the manifest.** In particular, the issue
   consolidation material included in the package is NOT authoritative: it may contain errors,
   and any recommendations embedded in it are candidate positions to be evaluated, not defaults
   to be transcribed. Nothing in the package is correct merely because it is written down.
3. **Claims discipline.** Figures marked `claimed-unverified` in `claims-table.md` are
   unconfirmed reports. Do not present them as established facts, and do not let a
   recommendation silently depend on one. Where a verdict turns on such a figure, state the
   dependency explicitly and give the conditional form ("if the verified value is X, then …;
   otherwise …"). A correction addendum with empirically verified values may be forwarded to you
   mid-task; when it arrives, incorporate it and revisit every answer that depended on an
   affected claim.
4. **Hard constraints are fixed.** The package lists locked project conventions as hard
   constraints. Treat them as boundary conditions: do not relitigate them, and do not propose
   anything that violates them. If your analysis suggests a question cannot be resolved without
   violating a constraint, flag that conflict explicitly as a finding instead of overriding the
   constraint.
5. **Scope boundary.** The package marks certain topics as out of scope or deferred to later
   work. Respect those boundaries exactly; do not answer beyond them.
6. **Independence.** Evaluate every position on evidence and first principles. Do not defer to
   any source — including the project's own documents — and do not be contrarian for its own
   sake. Agreeing with a presented position, rejecting all presented positions, or proposing a
   third position are all acceptable outcomes when justified.

## Method expectations

- Answer every question; no silent omissions or mergers. Where answers interact, cross-reference
  them and ensure they are mutually consistent.
- For each question, provide:
  1. **Verdict / recommendation** — specified to the level that a specification author could
     transcribe it without further interpretation: exact definitions, formulas, threshold
     values, procedures, and edge-case behavior where applicable.
  2. **Reasoning** — the argument from evidence and first principles.
  3. **Evidence** — citations to package files (file + section) and, where used, external
     literature or standard practice with full citations. Distinguish established results from
     your own judgment calls.
  4. **Confidence** — High / Medium / Low, plus the single most important factor that would
     change your answer.
  5. **Verification suggestion** — how the project could independently check your
     recommendation.
- Where a recommendation implies changing the provided specifications, include the proposed
  specification text (or a precise description of the change), anchored to the specific spec
  file and section it would modify.
- Where the evidence is insufficient to decide, say so explicitly and specify what evidence
  would resolve the question. An honest "insufficient evidence" with a discriminating test is
  more valuable than an arbitrary choice.
- You may use web search and published literature where available to you; cite everything you
  rely on.
- Before finalizing, run a consistency pass: check your recommendations against one another and
  against the hard constraints; resolve or explicitly flag any conflict you find.

## Output specification

Produce **one** self-contained markdown document:

- **Header:** title, date, and a one-line inventory of the package files you received (so input
  mismatches are detectable).
- **§0 Scope and decision standard:** what you covered, what you excluded per the package's
  scope boundary, and the evidence standard you applied.
- **§1 Executive decision summary:** the complete set of recommendations, in brief.
- **§2 Decision matrix:** one row per question — question ID, one-line verdict, confidence.
- **§3+ Resolutions:** per-question sections following the grouping and identifiers used in
  `framed-research-questions.md`, each containing the five elements listed under Method
  expectations (plus proposed specification text where applicable).
- **Open items register:** every "insufficient evidence" and "Additional Input Needed" item
  collected in one place.
- **References:** full citations for all external sources used.

Formatting: plain markdown (no HTML); LaTeX notation for mathematics is fine; use the package's
question identifiers and claim identifiers verbatim as anchors throughout.

## Quality bar

This document will serve as the **candidate verdict source** for a formal adjudication process:
every recommendation will be independently re-verified against the project's specifications,
dataset, and first principles before anything is adopted, and nothing is accepted on authority.
Write accordingly — precise citations, explicit assumptions, no unstated leaps — so that a
skeptical reviewer can check every claim you make.

<!-- PROMPT ENDS -->
