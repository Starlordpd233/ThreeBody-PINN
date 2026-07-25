---
status: active
purpose: runbook
created: 2026-06-11
milestone: untracked
phase: cross-cutting
retirement_trigger: superseded by a revised ERW runbook
---

# External Research Workflow (ERW)

**ERW** is this project's named workflow for delegating research-grade decisions to
external research agents: the agent in this repo **gathers context and builds a
package**, the **user hands it off** to one or more external AIs, and the returned
**research report becomes a guiding source** under channel-specific standing rules. The
in-repo agent transcribes and packages; it never adjudicates science itself.

Distilled 2026-06-11 from the issue-01/issue-02 resolution rounds (specwork channel) and
the trainex-r1 foundational round (build-design channel). Worked examples:
`pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`,
`pinn_instruction/markdown_conversion/framework-specs/trainex-r1/`, and
`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` (the open-book
worked example — see "Access modes").

**Revised 2026-07-24: two access modes added** (closed-book and open-book), on owner
instruction after the trainex-r2 round. Rules 1–2 are now mode-conditional and Rules
16–20 are new. Rationale in "Access modes" below.

## When to invoke ERW

Any decision that requires scientific justification, adjudication-grade analysis, or a
researched recommendation — framework choices, physics adjudications, methodology
trade-offs. Two channels with different standing:

| Channel | Examples | Package location | Standing of the report |
|---|---|---|---|
| **specwork** (spec adjudication) | issue-doc resolutions | `framework-revisions/research_reports/<NN-issue-slug>/` | **Candidate verdict source** — transcribed unless evidence shows a position fails; never authoritative; full verification protocol applies |
| **build-design** (e.g., trainex) | framework pick, runbook research | `framework-specs/<track>-<round>/` (e.g., `trainex-r1/`) | **Options menus + findings, not verdicts** — the user fills a decision sheet; the picks (recorded as Key Decisions) are the decisions; report is NOT a grounding source for spec adjudication |

**Channel separation is absolute:** evidence that feeds a specwork adjudication (e.g.,
precision-contract evidence) must never be folded into a build-design package — route it
as a separate EDL-style support brief through the specwork channel. (ERW ≠ EDL: the
Empirical Decision Loop at `.planning/research/edl/` supports empirically consequential
source-silent gaps, possibly with probes; ERW is the handoff relay. An EDL brief MAY be
delivered via ERW, but the gap register remains the blocking record.)

## Access modes (two routes) — added 2026-07-24

Channel sets the **standing** of the returned report. Access mode sets its **evidence
base**. The two axes are independent: either channel may run in either mode, and the mode
must be declared explicitly in the master frontmatter, the prompt, and the delivery note.

| | **Route A — closed-book** | **Route B — open-book** |
|---|---|---|
| Agent sees | attached files only | attachments **plus read-only repository access** |
| Use when | the question is conceptual — literature, methodology trade-offs, standard practice, how to frame a decision. No project fact is in dispute. | the question depends on what the code, data, configs, or run artifacts **actually do** |
| Evidence labels | package-derived facts + agent analysis | adds a distinct **repo-verified** label (`[FACT-W]`-style) with file:line citations |
| Repo paths in uploads | **forbidden** (Rule 1) | **expected** — the agent can resolve them |
| Premise challenge | limited to internal consistency of the package | **mandated** — the agent must test the package's own premises against the repository |
| Receiving-end burden | none beyond normal channel protocol | **every repo-derived claim independently verified in-repo before use** (Rule 19) |

**Why Route B exists (the trainex-r2 lesson, 2026-07-24).** The trainex-r2 package was
built Route A — "you have no codebase access" — and asked six questions about how to
re-tune a training recipe after a physics-gate failure. The owner overrode the clause and
granted read-only repository access. The agent then found that the executed run diverged
from the locked spec in five respects, including a causal-weighting collapse that made
the entire question set's premise false. All five were independently confirmed. Had the
round run strictly Route A, it would have returned a polished, internally consistent
resolution doc pointing in the wrong direction, and the false premise would have been
carried into the next milestone's scope. **A closed-book agent cannot tell you that your
question is wrong.**

**Default:** if any question references a project artifact — a run, a config, a code
path, a dataset — use **Route B**. Reserve Route A for questions that are purely
conceptual. When in doubt, Route B: its only real cost is the verification pass, and that
pass is cheap relative to acting on an unverified premise.

**Usage pattern — the premise-audit pass.** Route B may be commissioned specifically to
attack an existing package's premises rather than to answer its questions: same
attachments, plus repository access, with the mandate "tell me which of these stated
premises does not hold." Useful when a Route A round has already returned and its answers
depend on premises nobody verified.

## The workflow

```
0. MODE       pick Route A (closed-book) or Route B (open-book); declare it everywhere
1. GATHER     identify grounding sources; classify hard constraints vs baseline intent
2. PACKAGE    snapshot sources (commit-pinned) + write master, prompt, delivery note
3. HANDOFF    user attaches files + pastes prompt to external agent(s), in parallel
4. RESULTS    land per naming convention; optional multi-AI consolidation
4b. VERIFY    Route B only, mandatory: per-claim in-repo verification report (Rule 19)
5. USE        report becomes guiding source per channel standing; decisions recorded
```

## Files every package round creates

```
<round-root>/                          e.g. trainex-r1/
  DELIVERY-NOTE.md                     user-facing routing — NEVER uploaded
  specs/                               ONE shared snapshot set for the whole round
  research_package[_a|_b]/             one per sub-package (split rounds) or just one
    RESEARCH-CONTEXT-MASTER.md         the uploaded entry point
    RESEARCH-AGENT-PROMPT.md           paste-ready prompt + user attach-list header
  research_results/[r1a|r1b/]<agent>-resolution.md     (created at delivery time)
  <round>-resolution-doc.md            consolidated output (lands later)
```

- **RESEARCH-CONTEXT-MASTER.md** (uploaded): declared `access_mode` (Rule 16);
  orientation; manifest of companion files (*by bare filename* under Route A);
  source-treatment notes; hard-constraints-vs-baseline tiering; framed questions; output
  contract. Under Route B it also carries the premise-challenge mandate, the read-only
  bars, and the repo-derived evidence label. This is the agent's single entry point.
- **RESEARCH-AGENT-PROMPT.md** (paste-ready): a user-facing header above a horizontal
  rule listing exactly which files to attach; below the rule, the verbatim prompt.
  **A package without its prompt is incomplete — always ship them together.**
- **DELIVERY-NOTE.md** (user-only): all repo paths, gate context, result landing paths,
  consolidation join points, standing of the eventual report. The ONLY file where repo
  routing lives.
- **`specs/` snapshots**: verbatim copies of the grounding documents, pinned to a commit
  hash recorded in the master's frontmatter (`source_baseline`).

## Rules (each learned the hard way — do not relearn them)

### Self-containment of uploads — **Route A only** (see "Access modes")
1. **ZERO repo paths in any authored upload (masters and prompts).** A closed-book agent
   has no codebase access; refer to companion files by bare filename only. Never say
   "the `specs/` bundle" — directory structure is lost at upload. Exception
   (2026-06-11, trainex-r1): `specs/` snapshots are verbatim pins and may retain
   internal cross-references — never scrub them (that breaks commit-pin fidelity).
   Instead, the master instructs the agent to treat any unattached reference as
   unavailable and log it in the claims register if it matters.
2. Tell the agent explicitly: "you are working from attached files only" and enumerate
   the files in a manifest table with per-file treatment instructions.

   **Under Route B, Rules 1–2 invert:** repo paths in the master are *expected*, since
   the agent can resolve them, and the "attached files only" instruction must NOT appear
   — it directly contradicts the mandate in Rule 17. A Route B master still ships the
   attachments and still pins them, because they frame the questions and fix the
   baseline; the repository is an additional evidence source, not a replacement for the
   package. Package audits that check "zero repo-path markers" apply to Route A packages
   only.

### Storage (2026-06-11)
3. **One shared `specs/` snapshot set per round, at the round root — never duplicated
   per sub-package.** The attach-lists in each prompt's header and the delivery note do
   the routing; duplicate files buy nothing.
4. Snapshot only what the questions actually need; prefer pointing multiple sub-packages
   at the same snapshots.

### Provenance and freshness
5. Pin snapshots to a commit hash in the master frontmatter. If a source document is
   edited after packaging (e.g., a standing note is added), **refresh the snapshot** so
   the package stays internally consistent.

### Source grading
6. Classify every shipped source as **hard constraint** (facts, explicit user decisions,
   governance) vs **baseline design intent** (brainstorm-quality output — default
   starting point, challengeable only via explicit option-vs-baseline proposals). If a
   source is a quick-brainstorm baseline, say so in the package AND in the source doc
   itself (standing note), and include a **baseline critique mandate**.

### Output contracts (by channel)
7. **Build-design packages** (user picks): options menus (2–4 options, mechanical-surface
   trade-offs, cross-decision interactions, suggested default clearly marked); a
   **one-way vs two-way door classification** on every suggested default and deviation; a
   fill-in **decision sheet** (decision | options | suggested default | door type | your
   pick); a **composed first-run recipe** as a cross-menu coherence check; "what the
   runbook inherits"; claims-and-uncertainty register. Prompt must say: *suggest
   defaults; never decide.*
8. **Knowledge packages**: cited findings framed for direct reuse (signal → meaning →
   first response; rung → what it catches → pass criterion → cost); **parameterized
   estimates** with an explicit list of project-side numbers needed (never confident
   invented numbers); a **decision-relevant observations** section (observations, not
   adjudications); claims register.
9. All packages: where attached materials are silent or ambiguous, the agent records the
   gap in the claims register — never invents. (STOP-protocol culture extends to
   external agents via the prompt.)

### Scoping and splitting
10. Foundational rounds are scoped BIG (everything worth settling early, so later rounds
    only tune within fixed structure) — but **split into parallel sub-packages by output
    contract once a round exceeds ~6–7 work items** (single-prompt agents lose per-topic
    depth; multi-AI fan-out does not reliably compensate). Sub-packages share the round's
    DELIVERY-NOTE and `specs/`.
11. Record **consolidation join points** in the delivery note (which findings feed which
    menus) so the halves merge deliberately, not accidentally.

### Attachment cap (2026-07-07)
15. **Maximum 5 uploaded attachments per sub-package.** From 2026-07-07 onward,
    the package sent to each external research agent contains at most **5 attached
    files** per sub-package. This is a hard cap; exceeding it requires explicit
    user override. Files that are never uploaded to the agent — `DELIVERY-NOTE.md`
    (user-only routing), `research_results/` (created at delivery), the eventual
    `<round>-resolution-doc.md` (consolidated output) — are routing / provenance
    / outputs and do not count. **`specs/` snapshots DO count when uploaded**:
    bundle them into a single `framework-specs-bundle.md` so the bundle is 1
    attachment, not N. If a round's input set would exceed 5, **bundle — do not
    split into more attachments** (Rule 4 already prefers shared snapshots). The
    cap applies per sub-package, so a split round (e.g. `research_package_a/` +
    `research_package_b/`) may ship 5 attachments to each external agent
    independently.

### Access mode (2026-07-24)
16. **Declare the mode explicitly** in the master frontmatter (`access_mode: closed-book`
    or `open-book`), in the prompt body, and in the delivery note. An undeclared mode is
    a package defect: the agent's behavior, the evidence labels, and the receiving-end
    verification burden all depend on it.
17. **Route B carries a premise-challenge mandate, and it is not optional.** The prompt
    must instruct the agent to test the package's own stated premises against the
    repository and to report contradictions as **first-class findings reported up front**,
    not as per-question footnotes. Phrase it as a duty, not a permission: an agent that
    finds a false premise and buries it has failed the round. The trainex-r2 report's
    "source-verification findings that bear on multiple questions" section, placed ahead
    of the per-question answers, is the shape to ask for.
18. **Route B is read-only, and the prompt must say so in the imperative.** No file
    edited, no training run, no evaluation invoked, no command with side effects, no
    commit. On this project the standing bars (no held-out evaluation without owner
    policy, no new training runs, no framework-spec edits, no remedy selection) apply to
    external agents exactly as they apply to in-repo agents, and the prompt must
    enumerate them. Discriminating experiments are **proposed** as owner-gated options,
    never performed.
19. **Every repo-derived claim is verified in-repo before use, and the verification is
    recorded.** A Route B report's repo claims arrive as checkable assertions, not as
    established facts — they carry a file:line citation precisely so they can be
    re-derived independently. Produce a verification report under
    `docs/work/reviews/` with a per-claim verdict before any claim informs a decision,
    a roadmap, or a spec edit. This is a required step of the round, not a discretionary
    extra. Worked example:
    `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`.
20. **Pin the tree the agent saw.** Record in the delivery note how access was granted
    (which worktree, which branch) and the commit the working tree was at during the
    engagement. Open-book file:line citations are only re-derivable against that state;
    without the pin they rot silently as the tree moves. The attachment `source_baseline`
    pin does not cover this — it pins the snapshots, not the live tree.

### Naming
12. Rounds: `<track>-rN` (e.g., `trainex-r1`, `trainex-r2`); sub-packages
    `research_package_a/_b`; results `<agent>-resolution.md` under
    `research_results/[rNa|rNb/]`; consolidated `<round>-resolution-doc.md`.
    Issue-doc rounds keep the `<NN-issue-slug>` convention.

### Afterwards
13. Build-design: the user fills the decision sheet; picks are recorded as project Key
    Decisions; downstream rounds and the runbook draft proceed from picks + findings.
    Specwork: the resolution doc enters the adjudication machinery as candidate verdict
    source under the milestone's verification protocol.
14. The package directory is the durable record: keep master, prompt, delivery note,
    snapshots, results, and resolution together under the round root.

## Handoff quick reference (user steps)

1. Open the round's `DELIVERY-NOTE.md` — it names every sub-package and its attach list.
2. Per sub-package: open `RESEARCH-AGENT-PROMPT.md`, attach the files listed in its
   header (individually — no folders), paste everything below the horizontal rule.
3. Repeat across external agents (multi-AI fan-out), sub-packages in parallel.
4. Save each result as `<agent>-resolution.md` in the round's `research_results/`
   (per-sub-package subfolder if split).
5. Consolidate (issue-02 bundle tooling reusable) → `<round>-resolution-doc.md`; check
   the delivery note's join points; fill in the decision sheet where one exists.
6. **Route B only:** before consolidating or acting, have the in-repo agent produce the
   per-claim verification report (Rule 19). Repo-derived claims are checkable assertions
   until verified — the report's own file:line citations exist so you can hold it to that.
   If a verified claim contradicts a package premise, re-frame the round before using its
   answers; a false premise invalidates the answers built on it, however well-reasoned.
