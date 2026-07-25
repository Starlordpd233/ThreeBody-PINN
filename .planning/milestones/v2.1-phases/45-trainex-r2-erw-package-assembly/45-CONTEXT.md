# Phase 45: trainex-r2 ERW Package Assembly - Context

**Gathered:** 2026-07-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 45 delivers the **trainex-r2 External Research Workflow (ERW) package** under
`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`, following the canonical ERW
runbook. The package hands the training-recipe questions raised by the v2.0 Stage-0 pilot failure to
external research agents so their returned resolution doc can serve as a **candidate verdict source**
for the next milestone's owner-adjudicated remedy selection.

It is an **assembly / packaging** phase, not an analysis phase — Phase 44 already produced the
forensic diagnosis (`44-DIAGNOSIS.md`). Phase 45 curates, snapshots, and frames; it does not
re-analyze, evaluate, train, edit specs, or choose a remedy.

Three deliverable strands (PKG-09/10/11):

1. **PKG-09** — the package structure: annotated document list with **commit-pinned snapshots**
   (44-DIAGNOSIS.md, held-out receipt/metrics excerpts, 43-CALIBRATION.md / 43-VERDICT.md, the
   relevant locked spec sections, run-evidence excerpts), assembled per the ERW runbook.
2. **PKG-10** — **neutrally framed research questions** (no recommended answer): training budget/steps,
   warmup + learning-rate schedule, loss weighting/balancing, Stage-0 curriculum pacing, and the
   evaluation-policy question.
3. **PKG-11** — a **claims register** separating v2.0-verified facts (cited) from unverified agent
   hypotheses (the DIAG-04 rankings), plus a **delivery note** recording contents, provenance (commit
   pins), and the expected return format.

**Hard boundaries (SCOPE-22..26, owner-signed — carried from Phase 44):** no held-out evaluation, no
training runs, no framework-spec edits (specs are snapshot read-only into the package), no
PLAT-01..07 / Stage-1 work, no remedy selection. Delivery **opens the external research gate and
closes the v2.1 milestone**; the returning resolution doc gates the NEXT milestone, not this one.

</domain>

<decisions>
## Implementation Decisions

Discussion ran `--all --auto`: all gray areas auto-selected, the recommended option taken for each and
logged (owner delegated selection to agent judgement this session). See `45-DISCUSSION-LOG.md` for the
per-question log and alternatives considered. Every decision below is a **structural / presentation /
process** choice grounded in the ERW runbook, the PKG-09..11 requirements, and Phase 44 precedent —
none is a physics or spec adjudication, so none is a STOP-protocol gap. The single genuinely
owner-routed item (the two carried-forward todos, D-13) is handled by locking the *process* (surface
to owner), never the content.

### Package structure

- **D-01:** **Single sub-package**, not a split. PKG-10 names exactly **5** research questions; ERW
  Rule 10 splits only when a round exceeds ~6–7 work items. The five questions share one coherent
  output contract and one centerpiece (44-DIAGNOSIS.md), so a single package keeps them mutually
  consistent. Files (ERW "files every round creates"): `trainex-r2/DELIVERY-NOTE.md` (user-only),
  `trainex-r2/specs/` (shared snapshot set), `trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md`,
  `trainex-r2/research_package/RESEARCH-AGENT-PROMPT.md`, `trainex-r2/research_results/` (created at
  delivery), `trainex-r2/trainex-r2-resolution-doc.md` (lands later).

- **D-02:** **Attachment cap = 5 uploaded files (ERW Rule 15, 2026-07-07, hard cap).** Because it is a
  single sub-package the cap applies once. Recommended concrete layout — **4 uploaded attachments
  (1 slot headroom)**:
  1. `RESEARCH-CONTEXT-MASTER.md` — the agent's single entry point (orientation, per-file manifest by
     bare filename, hard-constraint-vs-baseline source tiering, the 5 framed questions, the output
     contract, **and the claims register folded in as a section**).
  2. `44-DIAGNOSIS.md` — the forensics centerpiece (verbatim snapshot, commit-pinned).
  3. `framework-specs-bundle.md` — **one** bundle of the relevant locked spec sections (Stage-0
     recipe, loss catalog, PHYS-05 scheduled weights, two-sided gate definition) excerpted from
     `ctl_instruction.md` + `pinn_architecture.md`. Specs count against the cap when uploaded, so
     bundle to one file (Rule 15) — never ship N spec files.
  4. `run-evidence-bundle.md` — **one** bundle of run-evidence excerpts: the evaluation
     receipt + metrics summary (ε_H distribution facts), 43-CALIBRATION.md excerpts, 43-VERDICT.md
     excerpts (the audited exhausted-evaluator budget), and the DIAG-02 warmup-spike /
     loss-decomposition excerpts.
  The planner may adjust bundle *boundaries* on evidence, but **must not exceed 5 uploads** and must
  bundle rather than split (Rule 15 + Rule 4). Files that never upload — `DELIVERY-NOTE.md`,
  `research_results/`, `trainex-r2-resolution-doc.md` — do not count.

- **D-03:** **Claims register lives as a section inside `RESEARCH-CONTEXT-MASTER.md`** (guaranteed
  seen — the master is the agent's single entry point) **and** as a standalone
  `research_package/CLAIMS-REGISTER.md` in the package dir for the durable record (not uploaded,
  saves an attachment slot). This satisfies PKG-11 "the package carries a claims register" without
  spending a cap slot.

### Output contract and channel standing

- **D-04:** **Specwork-style neutral framing — no recommended answer**, despite the package living
  under the build-design track path `framework-specs/trainex-r2/`. Grounding: PKG-10 mandates "no
  recommended answer, v1.5/v1.6 precedent"; PKG-11 mandates return as "one consolidated resolution
  doc as candidate verdict source." trainex-r2 is **remedy-adjudication research routed to a future
  governed adjudication milestone** (SCOPE-26), not framework selection. Therefore the master/prompt
  use neutral framed questions, the STOP-culture "record gaps, never invent" mandate for the external
  agent, and instruct the agent **not** to recommend a remedy. The prompt must **not** carry the
  build-design instruction "suggest defaults; never decide" (that contract is for user-picks rounds
  like trainex-r1); it instead says: *answer with reasoning and cited evidence, frame the trade-offs,
  do not assume a house preference, and record any gap where the attached materials are silent.*
  This resolves the apparent build-design-vs-specwork tension explicitly — it is **grounded, not a
  gap**.

### The five research questions (PKG-10)

- **D-05:** Pose **exactly the five PKG-10 areas**, each neutrally, each cross-linked to the
  corresponding DIAG-04 candidate cause as **[HYP] context** (never as a steer):
  1. **Training budget / steps** — ↔ DIAG-04 candidate 5 (Weak) and its confound with the
     population-scale candidate 1 (300 steps; validation trends still moving; Phase 38 reached a
     single-trajectory floor in 176 steps).
  2. **Warmup + learning-rate schedule** — ↔ candidate 3 (Moderate): the finite `loss_phys` warmup
     spikes (3.7e9–6.1e9) with `grad_norm ≈ 5–7e13`, seed42 spiking at peak `lr = 7.5e-4`.
  3. **Loss weighting / balancing** — ↔ candidate 2 (Moderate): `loss_phys` carries ≈99.998–99.999%
     of every spike and dominates cumulative raw + weighted; `lambda_l = 0` at all 300 steps. **The
     normalization / data-scale candidate 4** (≈10 orders separating `loss_phys ≈ 1e9` from
     `loss_data ≈ 0.1`) is posed as a **sub-facet within this question**, keeping the count at the
     five named PKG-10 areas.
  4. **Stage-0 curriculum pacing** — ↔ the Stage-0 recipe: how stage / `front_idx` progression and
     scheduled-weight ramps interact within the 300-step budget.
  5. **Evaluation-policy question** — what evidence and governance a future held-out evaluation would
     require **given the exhausted budget** (SCOPE-22 context: two failed attempts + one completed
     FAIL, all audited in 43-VERDICT.md). This is a governance/methodology question, not a request
     to run the evaluator.
- **D-06:** Each question carries the matching **discriminating-test proposal from DIAG-04 §6** as a
  *proposed research direction only* — owner-authorization-gated, **never executed** (SCOPE-23). The
  package poses them as questions; it does not run them.

### Provenance and snapshots (PKG-09)

- **D-07:** **Commit-pin every snapshot.** Record a single `source_baseline` = the repo HEAD at
  package assembly in the master frontmatter (ERW Rule 5). All sources (44-DIAGNOSIS.md, its evidence
  tree, 43-CALIBRATION/43-VERDICT, the specs) are already committed by assembly time, so one
  assembly-HEAD pin covers them. Preserve the diagnosis's own deeper evidence pin
  (`evidence/manifest.json`, `git_head = 8631576…`) — note it in the master rather than overwriting
  it; the two pins are complementary (package baseline vs diagnosis evidence tree).
- **D-08:** Snapshots are **verbatim copies** of the grounding documents. Per ERW Rule 1, `specs/`
  snapshots may retain internal cross-references — **do not scrub them** (that breaks commit-pin
  fidelity); the master instructs the agent to treat any unattached reference as unavailable and log
  it in the claims register if it matters. Excerpting for the bundles (D-02 items 3–4) is by
  section, faithfully quoted with a source-path + line-range citation for each excerpt.

### Claims register construction (PKG-11)

- **D-09:** **Build the claims register by lifting the `[FACT]` / `[HYP]` tags already in
  44-DIAGNOSIS.md** (the diagnosis was written in the v1.4/v1.5/v1.6 house style precisely so the
  register is a direct lift). `[FACT]` rows = v2.0-verified numbers with citations (the ε_H
  distribution, the five-term loss decomposition, the seed-band trends, the spreads that reproduce
  43-CALIBRATION within 1e-9). `[HYP]` rows = the **DIAG-04 candidate-cause rankings**, explicitly
  labeled "agent analysis — **not** established fact." GAP-44-01's resolution (worst-case max IS the
  gate statistic, owner option A 2026-07-23) is recorded as a **verified/owner-instructed fact**, with
  its verdict-neutrality noted.

### Delivery note (PKG-11)

- **D-10:** `DELIVERY-NOTE.md` (user-only, **never uploaded**) records: the package contents +
  per-attachment upload list honoring the 5-cap; provenance (the commit pins); the **expected return
  format** — individual reports → one consolidated resolution doc as candidate verdict source, per the
  v1.4/v1.5/v1.6 precedent; result landing paths (`research_results/<agent>-resolution.md`;
  consolidated `trainex-r2-resolution-doc.md`); the standing of the eventual report (candidate verdict
  source for the **next** milestone's remedy adjudication — SCOPE-26); and the two carried-forward-todo
  owner questions (D-13). It is the ONLY file where repo paths live. Structure follows the trainex-r1
  DELIVERY-NOTE, adapted to a single sub-package.

### Self-containment of uploads (ERW Rules 1–2)

- **D-11:** **Zero repo paths in any authored upload** (master, prompt, bundles). The external agent
  has no codebase access — refer to companion files by **bare filename** only, never "the `specs/`
  bundle" or any directory reference. The prompt's header lists exactly which files to attach
  (individually, no folders); the body says explicitly "you are working from the attached files only."
- **D-12:** **Source grading is mandatory:** classify every shipped source as **hard constraint**
  (v2.0-verified facts, owner decisions incl. GAP-44-01, governance, locked specs) vs **baseline
  design intent**. For trainex-r2 there is little pure "brainstorm baseline" — the inputs are locked
  facts and the diagnosis — but the tiering section still states this explicitly so the agent treats
  the DIAG-04 rankings as challengeable hypotheses rather than settled findings.

### Carried-forward todos — OWNER decision, surfaced not decided (Success Criterion 4)

- **D-13 (SURFACE, do not decide):** Both pending todos are **in Phase 45 scope as owner-decision
  items**. Phase 45 Success Criterion 4 and SCOPE-26 make them "decided by the owner, not the agent."
  During assembly, **Agent C surfaces them to the owner as package-scope questions and does NOT decide
  their inclusion or content** — this explicitly overrides the `--auto` score≥0.4 auto-fold, because a
  locked success criterion is the more specific constraint:
  - **`trainex-r1-research-handoff`** ("Review and hand off the trainex-r1 sub-packages r1a + r1b") —
    the owner decides whether/how the trainex-r1 **r1b** runbook-operations findings relate to or feed
    the trainex-r2 package. (r1b's K-series findings partly overlap the training-recipe questions.)
  - **`d-06-static-epsilon-sensitivity-check`** ("confirm dual-context is safe on the admitted set") —
    the owner decides whether the static-`eps_soft` sensitivity check is **included as a trainex-r2
    research question** (it is a spec-side question and a candidate ERW question).
  The recommended default is to present both as clearly-framed A/B/C owner questions in the assembly
  hand-off; the agent records the owner's answer, never pre-fills it.

### Governance

- **D-14:** SCOPE-22..26 hold throughout assembly: no evaluation (SCOPE-22), no training (SCOPE-23),
  no framework-spec edits — specs enter the package as **read-only verbatim snapshots** (SCOPE-24),
  no Stage-1 / PLAT-01..07 work (SCOPE-25), no remedy chosen — the questions stay neutral (SCOPE-26).
  Any source-silent adjudication call encountered during assembly is a STOP-protocol gap → recorded in
  `.planning/phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` and indexed in
  `.planning/milestones/v2.1-GAPS.md`, never decided.
- **D-15:** Commits go through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`
  set; explicit owned paths only, never blanket staging. The docs/ lifecycle does not apply here — the
  package lives under `pinn_instruction/…/trainex-r2/`, not `docs/work/`.

### Claude's Discretion

`--auto` selected the recommended option for every area without user prompting, so all decisions above
are Claude-selected defaults. They are **implementation-mechanics** choices (single vs split, bundle
layout under the 5-cap, where the claims register lives, how to pin provenance, how to frame the five
questions) and are safe for the planner to adjust on evidence — **with two non-discretionary
exceptions**: **D-04** (neutral no-recommendation output contract is required by PKG-10) and **D-13**
(the two todos are owner-decided, surfaced not decided, per Success Criterion 4). Neither may be
overridden by the planner or executor.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (researcher, planner, executor) MUST read these before planning or implementing.**

### The ERW method (drives the whole package)
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — canonical ERW runbook.
  Read in full: the "files every round creates" layout, the self-containment/upload rules (Rules 1–2),
  the storage/shared-snapshot rules (Rules 3–4), provenance/commit-pin (Rule 5), source grading
  (Rule 6), output contracts by channel (Rules 7–9), scoping/splitting (Rules 10–11), and especially
  **Rule 15 — the max-5-attachments-per-sub-package hard cap** (lines 134–147).

### Phase scope, requirements, and hard boundaries
- `.planning/REQUIREMENTS.md` — **PKG-09, PKG-10, PKG-11** verbatim, plus **SCOPE-22..26** (owner-signed
  hard constraints). Read SCOPE-22..26 before proposing any task.
- `.planning/ROADMAP.md` §"Phase 45: trainex-r2 ERW Package Assembly" (goal, 5 success criteria) and
  §"Investigation discipline (applies to both phases)".
- `CLAUDE.md` — STOP protocol (gap classification; "never invent where sources are silent"), the git
  commit protocol, and the v2.1 governance context.

### The centerpiece and its evidence (PKG-09 inputs)
- `.planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md` — the hypothesis-ranked, `[FACT]`/`[HYP]`-
  tagged diagnosis. **Package centerpiece**; the claims register (PKG-11) lifts its tags directly.
- `.planning/phases/44-physics-gate-forensics/evidence/manifest.json` — the pinned evidence tree
  (`git_head = 8631576…`, 15 inputs by SHA-256); source of the diagnosis's re-derivability claim.
- `.planning/phases/44-physics-gate-forensics/evidence/diag01|diag02|diag03/` — the per-diag script
  outputs behind the quoted numbers.

### Run-evidence and verdict inputs (PKG-09 inputs)
- `runs/stage0-pilot-seed42/evaluation/metrics.json` — the sole gate rendering (per-trajectory ε_H
  array; two-sided verdict FAIL). Excerpt into `run-evidence-bundle.md`.
- `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` and `.../metrics.md` — receipt /
  human-readable summary of that rendering.
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` — the
  owner-signed `adjust` verdict; the audited exhausted-evaluator budget (SCOPE-22 grounding for the
  evaluation-policy question).
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` —
  per-seed calibration, the "2/3 seeds worsened" claim, the spreads DIAG-03 reproduced.
- `runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}/logs/train.log.jsonl` — per-step training
  records behind DIAG-02's warmup-spike / loss-decomposition excerpts.

### Locked specs to snapshot (read-only — SCOPE-24 forbids editing)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Stage-0 recipe,
  curriculum staging, loss catalog, PHYS-05 scheduled weights, and the two-sided gate definition
  (`ctl_instruction.md:567-572`). Excerpt the relevant sections into `framework-specs-bundle.md`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — architecture, AD
  contract, output head (context for the physics-residual / normalization sub-facet of question 3).

### Precedent (structure to mirror)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/DELIVERY-NOTE.md` — the delivery-note
  structure to adapt (single sub-package instead of split).
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/` and
  `.../research_package_b/` — `RESEARCH-CONTEXT-MASTER.md` + `RESEARCH-AGENT-PROMPT.md` shape reference.
- The v1.5 specwork precedent for neutral framed questions:
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`.

### Gap registers
- `.planning/milestones/v2.1-GAPS.md` — milestone gap index (currently: GAP-44-01 RESOLVED; no open
  gaps).
- `.planning/phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` — **to be created on the first
  Phase 45 gap** under the standing trigger.

### The two carried-forward todos (D-13 — owner-decided)
- `.planning/todos/trainex-r1-research-handoff.md` (or the todo store the `todo.match-phase` query
  reads) — the r1b-handoff owner question.
- `.planning/todos/d-06-static-epsilon-sensitivity-check.md` — the static-`eps_soft` inclusion owner
  question. (Confirm exact paths via `gsd-tools query todo.match-phase 45`.)

</canonical_refs>

<code_context>
## Existing Code Insights

This is a documentation-assembly phase — "reusable assets" are prior artifacts and templates, not code.

### Reusable Assets
- **44-DIAGNOSIS.md is upload-ready.** It was authored for two audiences (owner + external
  researchers), carries inline `[FACT]`/`[HYP]` tags, and cites every number to a retained artifact a
  stranger can follow. It snapshots into the package essentially verbatim (PKG-09) and its tags become
  the claims register (PKG-11) with minimal transformation.
- **trainex-r1 package** provides the exact file skeleton (`RESEARCH-CONTEXT-MASTER.md`,
  `RESEARCH-AGENT-PROMPT.md`, `DELIVERY-NOTE.md`, `specs/`, `research_results/`) and the delivery-note
  routing pattern — adapt from split (a/b) to single.
- **Phase 44 evidence tree** already pins its inputs by SHA-256 + git_head; the package can cite that
  pin rather than re-deriving provenance.

### Established Patterns
- **ERW Rule 15 bundling** is the load-bearing constraint: specs and multi-file evidence must be
  bundled to single attachments to stay ≤5 uploads. Design the package around the cap from the start,
  not as an afterthought.
- **House style: `[FACT]` vs `[HYP]` separation** (v1.4/v1.5/v1.6) is already applied in the
  diagnosis; keep it visible in the master and claims register.
- **Neutral-question framing** (specwork v1.5/v1.6): question → what evidence bears on it → what a
  complete answer specifies; no recommended answer; STOP-culture gap instruction to the agent.

### Integration Points
- Phase 45 writes under `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` (the
  deliverable) and `.planning/phases/45-trainex-r2-erw-package-assembly/` (phase artifacts:
  PLAN/SUMMARY/GAPS/VERIFICATION, and any evidence of the assembly). It **reads** `runs/`,
  `.planning/phases/44-*`, `.planning/milestones/v2.0-*`, the framework specs, and the trainex-r1
  package. It edits **none** of them (snapshots are copies).
- Delivery closes the v2.1 milestone; the returning resolution doc gates the next milestone.

</code_context>

<specifics>
## Specific Ideas

- The package is written for an **external agent with zero repo access** — the single hardest rule to
  honor is D-11 (no repo paths in uploads; bare filenames only). A reviewer should grep the authored
  uploads for `/`, `.planning`, `runs/`, and `framework-specs/` before delivery.
- The **evaluation-policy question (PKG-10 #5)** is subtle: it asks what a *future* held-out evaluation
  would require given the budget is exhausted — it must not read as a request to run the evaluator now
  (SCOPE-22). Frame it as governance/evidence design.
- The DIAG-04 rankings are **hypotheses, not findings** — the package must present them as challengeable
  agent analysis so the external agent does not treat "population-scale generalization shortfall" as a
  settled conclusion and skip the alternatives.
- GAP-44-01's resolution (worst-case max IS the gate statistic) is **verdict-neutral** (1500/1500 fail
  under any aggregate); the claims register should say so, so the framing does not overstate the
  headline magnitude's significance.

</specifics>

<deferred>
## Deferred Ideas

- **Choosing / recommending any remedy** — SCOPE-26; the questions stay neutral, the owner adjudicates
  from the returned resolution doc in a later milestone.
- **Running any discriminating test** from DIAG-04 §6 — SCOPE-23; they are posed as research questions
  only.
- **A new held-out evaluation** — SCOPE-22; the evaluation-policy question *asks about* a future
  evaluation's requirements; it does not perform one.
- **Framework-spec edits** implied by the diagnosis — SCOPE-24; snapshots are read-only.
- **Consolidation of returned results** into `trainex-r2-resolution-doc.md` — happens at *delivery
  time* (after external research returns), outside this phase; the delivery note only records the join
  points and expected format.

### Reviewed Todos (surfaced to owner, NOT auto-folded)

Both pending todos matched Phase 45 at relevance 0.6 (≥ the 0.4 `--auto` fold threshold), but per
Success Criterion 4 they are **owner-decided, surfaced at assembly** — see **D-13**. They are recorded
here as in-scope owner questions, not as agent-folded scope:

- **`trainex-r1-research-handoff`** — owner decides the r1b ↔ trainex-r2 relationship at assembly.
- **`d-06-static-epsilon-sensitivity-check`** — owner decides inclusion as a trainex-r2 research
  question at assembly.

</deferred>

---

*Phase: 45-trainex-r2-erw-package-assembly*
*Context gathered: 2026-07-23*
</content>
</invoke>
