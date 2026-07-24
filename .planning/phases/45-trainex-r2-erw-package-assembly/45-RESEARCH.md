# Phase 45: trainex-r2 ERW Package Assembly - Research

**Researched:** 2026-07-24
**Domain:** Documentation/process assembly — External Research Workflow (ERW) package construction (this project's internal packaging methodology; not a software/library domain)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Discussion ran `--all --auto`: all gray areas auto-selected, the recommended option taken for each and
logged (owner delegated selection to agent judgement this session). See `45-DISCUSSION-LOG.md` for the
per-question log and alternatives considered. Every decision below is a **structural / presentation /
process** choice grounded in the ERW runbook, the PKG-09..11 requirements, and Phase 44 precedent —
none is a physics or spec adjudication, so none is a STOP-protocol gap. The single genuinely
owner-routed item (the two carried-forward todos, D-13) is handled by locking the *process* (surface
to owner), never the content.

#### Package structure

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

#### Output contract and channel standing

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

#### The five research questions (PKG-10)

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

#### Provenance and snapshots (PKG-09)

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

#### Claims register construction (PKG-11)

- **D-09:** **Build the claims register by lifting the `[FACT]` / `[HYP]` tags already in
  44-DIAGNOSIS.md** (the diagnosis was written in the v1.4/v1.5/v1.6 house style precisely so the
  register is a direct lift). `[FACT]` rows = v2.0-verified numbers with citations (the ε_H
  distribution, the five-term loss decomposition, the seed-band trends, the spreads that reproduce
  43-CALIBRATION within 1e-9). `[HYP]` rows = the **DIAG-04 candidate-cause rankings**, explicitly
  labeled "agent analysis — **not** established fact." GAP-44-01's resolution (worst-case max IS the
  gate statistic, owner option A 2026-07-23) is recorded as a **verified/owner-instructed fact**, with
  its verdict-neutrality noted.

#### Delivery note (PKG-11)

- **D-10:** `DELIVERY-NOTE.md` (user-only, **never uploaded**) records: the package contents +
  per-attachment upload list honoring the 5-cap; provenance (the commit pins); the **expected return
  format** — individual reports → one consolidated resolution doc as candidate verdict source, per the
  v1.4/v1.5/v1.6 precedent; result landing paths (`research_results/<agent>-resolution.md`;
  consolidated `trainex-r2-resolution-doc.md`); the standing of the eventual report (candidate verdict
  source for the **next** milestone's remedy adjudication — SCOPE-26); and the two carried-forward-todo
  owner questions (D-13). It is the ONLY file where repo paths live. Structure follows the trainex-r1
  DELIVERY-NOTE, adapted to a single sub-package.

#### Self-containment of uploads (ERW Rules 1–2)

- **D-11:** **Zero repo paths in any authored upload** (master, prompt, bundles). The external agent
  has no codebase access — refer to companion files by **bare filename** only, never "the `specs/`
  bundle" or any directory reference. The prompt's header lists exactly which files to attach
  (individually, no folders); the body says explicitly "you are working from the attached files only."
- **D-12:** **Source grading is mandatory:** classify every shipped source as **hard constraint**
  (v2.0-verified facts, owner decisions incl. GAP-44-01, governance, locked specs) vs **baseline
  design intent**. For trainex-r2 there is little pure "brainstorm baseline" — the inputs are locked
  facts and the diagnosis — but the tiering section still states this explicitly so the agent treats
  the DIAG-04 rankings as challengeable hypotheses rather than settled findings.

#### Carried-forward todos — OWNER decision, surfaced not decided (Success Criterion 4)

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

#### Governance

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

### Deferred Ideas (OUT OF SCOPE)

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

#### Reviewed Todos (surfaced to owner, NOT auto-folded)

Both pending todos matched Phase 45 at relevance 0.6 (≥ the 0.4 `--auto` fold threshold), but per
Success Criterion 4 they are **owner-decided, surfaced at assembly** — see **D-13**. They are recorded
here as in-scope owner questions, not as agent-folded scope:

- **`trainex-r1-research-handoff`** — owner decides the r1b ↔ trainex-r2 relationship at assembly.
- **`d-06-static-epsilon-sensitivity-check`** — owner decides inclusion as a trainex-r2 research
  question at assembly.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PKG-09 | Package assembled per canonical ERW runbook under `framework-specs/trainex-r2/`: curated annotated document list with commit-pinned snapshots (44-DIAGNOSIS.md, receipt/metrics, 43-CALIBRATION/43-VERDICT, locked spec sections, run-evidence excerpts) | ERW Rule-to-requirement mapping table (below); recommended file tree; Rule 5/D-07 commit-pin mechanics; Rule 15/D-02 cap-compliant 4-upload bundle plan; exact spec-section line anchors located in `ctl_instruction.md`/`pinn_architecture.md` |
| PKG-10 | Neutrally framed research questions (no recommended answer) covering budget/steps, warmup+LR schedule, loss weighting, Stage-0 pacing, evaluation-policy | v1.5 issue-02 Q-cluster precedent structure (position/spec-position/facts/question); 44-DIAGNOSIS.md's own [FACT]/[HYP] citations mapped to each of the 5 D-05 areas; worked neutral-framing template (Common Pitfalls + Code Examples) |
| PKG-11 | Claims register separating verified facts from hypotheses (DIAG-04 rankings); delivery note recording contents, provenance, expected return format | Full inventory of 44-DIAGNOSIS.md's [FACT] and [HYP] tagged claims (Code Examples); v1.5 CLM-register precedent format; trainex-r1 DELIVERY-NOTE.md structure to mirror; D-13 A/B/C todo-framing starting menu |

</phase_requirements>

## Summary

Phase 45 is a pure documentation-assembly phase with **no external software stack** — the "technology"
here is this project's own ERW (External Research Workflow) methodology, documented in
`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`, plus two directly-reusable
precedents already in the repo: the **trainex-r1** package (the file-skeleton and delivery-note
pattern to mirror, adapted from split to single sub-package) and the **v1.5 issue-02 specwork package**
(the neutral-question-framing and claims-register pattern to mirror, since D-04 locks trainex-r2 into
specwork-style output despite living under the build-design `framework-specs/` path). The centerpiece
input, `44-DIAGNOSIS.md`, was deliberately authored in the v1.4/v1.5/v1.6 `[FACT]`/`[HYP]` house style
specifically so Phase 45's claims register is a **direct lift**, not new authorship.

The single hardest constraint to satisfy correctly is **ERW Rule 15's 5-attachment-per-sub-package hard
cap** (2026-07-07): CONTEXT.md's D-02 already lays out a compliant 4-upload layout (master, diagnosis,
one spec bundle, one run-evidence bundle) with one slot of headroom, but the planner must not let scope
creep (e.g., separate spec files, a separate claims-register upload) blow the cap. The second
highest-risk area is **not** technical at all — it is governance discipline: every DIAG-04
candidate-cause ranking must be visibly tagged as agent hypothesis, not fact, in every place it appears
in the package, and the five questions must be framed so that "what a complete answer specifies" never
slides into "what the answer probably is" (D-04, SCOPE-26). A third, easy-to-miss nuance this research
surfaced: ERW Rule 1's self-containment requirement (zero repo paths) applies to **authored** content
(the master, the prompt, the two bundles) but explicitly **does not** apply to verbatim snapshots — so
`44-DIAGNOSIS.md`, uploaded as-is, correctly retains its own internal `.planning/`, `evidence/`, and
`runs/` citations, and must **not** be scrubbed (that would break D-08's commit-pin fidelity guarantee).

**Primary recommendation:** Mirror the trainex-r1 file skeleton exactly, but collapse `research_package_a/`
+ `research_package_b/` into a single `research_package/`; build `RESEARCH-CONTEXT-MASTER.md` using the
v1.5 issue-02 master's five-part shape (orientation → framed questions → claims register → hard-constraint
tiering → output contract) rather than the trainex-r1 master's build-design shape (decision menus → door
classification → decision sheet); and treat 44-DIAGNOSIS.md's own `[FACT]`/`[HYP]` tags as the claims
register's row-by-row source material rather than re-deriving them.

## Architectural Responsibility Map

This is a documentation-assembly phase, not a multi-tier software system — the table below maps
capabilities to **process roles** (who/what owns each responsibility in the ERW handoff) rather than
Browser/API/DB tiers, since that is the meaningful boundary structure for this domain.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Document curation & selection (what enters the package) | In-Repo Assembly (Phase 45 agent) | — | Only the assembly agent has repo access to decide what evidence is relevant |
| Commit-pinning provenance (`source_baseline`) | In-Repo Assembly | Repo-only Routing (DELIVERY-NOTE.md) | Recorded in master frontmatter (agent-visible) and detailed for the user in the routing note |
| Self-contained framing (master, prompt, bundles) | Authored-Upload Content | In-Repo Assembly | Zero-repo-path content written by the assembly agent, consumed by an agent with no codebase access |
| Verbatim citation fidelity (44-DIAGNOSIS.md, spec excerpts) | Snapshot-Verbatim Content | — | Must **not** be scrubbed of internal cross-references (ERW Rule 1 exception, D-08) |
| Claims separation (`[FACT]` vs `[HYP]`) | Authored-Upload Content (master section) | Repo-only Routing (standalone `CLAIMS-REGISTER.md`) | Dual-location per D-03: uploaded copy folded into the master, durable copy kept in-repo, neither costs an attachment slot |
| Neutral question framing (no recommended answer) | Authored-Upload Content | — | Specwork-style; zero steer toward any of the DIAG-04 candidates |
| **Answering the five research questions** | **External Research Agent** | — | Explicitly **out of Phase 45's scope** (SCOPE-26, D-04) — the researcher, not the assembler, produces the answer |
| D-13 owner-decision surfacing (the two carried-forward todos) | Repo-only Routing (DELIVERY-NOTE.md) | Owner/User | Agent surfaces the A/B/C question; owner decides; content never enters the uploaded package |
| Result consolidation → `trainex-r2-resolution-doc.md` | Owner/User (post-delivery) | External Research Agent(s) | Happens after Phase 45 closes, at handoff/delivery time — outside this phase's scope |
| Self-containment verification (pre-delivery grep audit) | In-Repo Assembly | — | A reviewer step gating delivery, not an external-agent-facing artifact |

## Standard Stack

**Not applicable in the conventional software sense.** This phase installs no libraries, frameworks,
or services. The "stack" is entirely this project's own documented process:

- The **ERW runbook** (`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`) —
  the methodology and its 15 numbered rules. [CITED: docs/runbooks/external-research/2026-06-11-external-research-workflow.md]
- The **trainex-r1 package** — the file-skeleton and delivery-note precedent to mirror.
  [CITED: pinn_instruction/markdown_conversion/framework-specs/trainex-r1/]
- The **v1.5 issue-02 specwork package** — the neutral-question-framing and claims-register precedent.
  [CITED: pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/]
- The **v1.4/v1.5/v1.6 house style** (`[FACT]`/`[HYP]` inline tagging) already applied verbatim in
  `44-DIAGNOSIS.md`. [CITED: .planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md]

No package installation, no version pinning of software, and no "Package Legitimacy Audit" applies —
see below.

## Package Legitimacy Audit

**Not applicable.** Phase 45 installs no external packages of any kind (npm, PyPI, crates, or
otherwise) — it is a pure markdown/documentation curation and copying task. The Package Legitimacy Gate
protocol is skipped for this phase; no packages require registry verification, and the planner should
not include a package-legitimacy verification step.

## Architecture Patterns

### System Flow Diagram

```
Phase 44 (complete)                    Phase 45 (this phase)
┌─────────────────┐                    ┌───────────────────────────────────────────┐
│ 44-DIAGNOSIS.md  │──── snapshot ─────▶│ research_package/44-DIAGNOSIS.md            │
│ (FACT/HYP tagged)│      (verbatim,    │   (verbatim, retains internal repo paths — │
│                  │       D-08)        │    NOT scrubbed, D-08 exception)           │
└─────────────────┘                    │                                             │
                                        │  ┌───────────────────────────────────────┐  │
ctl_instruction.md   ── excerpt by ───▶│  │ specs/framework-specs-bundle.md        │  │
pinn_architecture.md    section (D-08) │  │  (bare-filename + line-range citations │  │
(locked specs)                         │  │   only — never a directory path)       │  │
                                        │  └───────────────────────────────────────┘  │
runs/.../metrics.json                  │  ┌───────────────────────────────────────┐  │
43-CALIBRATION.md   ── excerpt by ───▶ │  │ research_package/run-evidence-        │  │
43-VERDICT.md           section (D-08) │  │  bundle.md                             │  │
                                        │  └───────────────────────────────────────┘  │
                                        │                                             │
                                        │  ┌───────────────────────────────────────┐  │
44-DIAGNOSIS.md's        ── lift ─────▶│  │ RESEARCH-CONTEXT-MASTER.md             │  │
[FACT]/[HYP] tags        (D-09)        │  │  §Claims Register (folded in, D-03)    │  │
                                        │  │  §5 Framed Questions (D-05)            │  │
                                        │  │  §Hard-constraint-vs-baseline (D-12)   │  │
                                        │  └───────────────────────────────────────┘  │
                                        │                    +                        │
                                        │  ┌───────────────────────────────────────┐  │
                                        │  │ CLAIMS-REGISTER.md (standalone,        │  │
                                        │  │  NOT uploaded — durable record, D-03)  │  │
                                        │  └───────────────────────────────────────┘  │
                                        │                                             │
                                        │  DELIVERY-NOTE.md (user-only, never        │
                                        │   uploaded) — routes handoff + D-13 owner  │
                                        │   A/B/C questions                          │
                                        └───────────────────────────────────────────┘
                                                        │
                                          user attaches 4 files + pastes
                                          RESEARCH-AGENT-PROMPT.md body
                                                        ▼
                                        ┌───────────────────────────────────────────┐
                                        │  External Research Agent(s)                │
                                        │  → answers the 5 neutral questions          │
                                        │  → research_results/<agent>-resolution.md   │
                                        └───────────────────────────────────────────┘
                                                        │  (post-delivery,
                                                        │   OUTSIDE Phase 45 scope)
                                                        ▼
                                        trainex-r2-resolution-doc.md
                                        (candidate verdict source for the NEXT
                                         milestone's owner-adjudicated remedy)
```

### Recommended Project Structure

```
pinn_instruction/markdown_conversion/framework-specs/trainex-r2/
├── DELIVERY-NOTE.md                       # user-only, NEVER uploaded; D-10; frontmatter: title/package_for/role/status/created
├── specs/
│   └── framework-specs-bundle.md          # excerpted spec sections (gate def, loss catalog, PHYS-05, Stage-0 recipe); uploaded attachment #3
├── research_package/
│   ├── RESEARCH-CONTEXT-MASTER.md         # uploaded attachment #1 — single entry point, includes claims-register section (D-03)
│   ├── RESEARCH-AGENT-PROMPT.md           # paste-ready; NOT an upload — its body is pasted as text below a horizontal rule
│   ├── 44-DIAGNOSIS.md                    # uploaded attachment #2 — verbatim snapshot, commit-pinned (D-07/D-08)
│   ├── run-evidence-bundle.md             # uploaded attachment #4 — metrics/receipt + 43-CALIBRATION + 43-VERDICT excerpts
│   └── CLAIMS-REGISTER.md                 # standalone durable record, NOT uploaded (D-03)
├── research_results/                      # created at delivery time (post-Phase-45)
│   └── <agent>-resolution.md
└── trainex-r2-resolution-doc.md           # consolidated output, lands later (post-Phase-45)
```

This gives exactly **4 uploaded attachments** (master, diagnosis, one spec bundle, one evidence bundle)
against the 5-cap, matching D-02's recommended layout with one slot of headroom. `specs/` holds the
excerpted spec bundle (keeping it a literal "spec snapshot" per ERW's own `specs/` definition and
preserving Rule 3's "one shared specs/ directory at round root" convention for any future trainex-r3+
round); the diagnosis, run-evidence bundle, and claims register — which are evidence/verdict artifacts,
not framework specs — live in `research_package/` alongside the master and prompt. This placement is
**Claude's-discretion territory** per CONTEXT.md's own delegation (see Open Questions below) — safe for
the planner to adjust, as long as the 4-upload count and bundling discipline are preserved.

### Pattern 1: Single sub-package, mirrored from trainex-r1's split precedent

**What:** trainex-r1 split into `research_package_a/` (decisions) and `research_package_b/` (knowledge)
because it had ~14 combined work items (D1–D7 + K1–K5), exceeding ERW Rule 10's ~6-7-item split
threshold. trainex-r2 has exactly 5 questions — under threshold — so D-01 locks a **single**
`research_package/`.
**When to use:** Any future trainex round should re-check its item count against the ~6-7 threshold
before defaulting to a split; do not split out of habit because the mirrored precedent (trainex-r1) is
split.
**Example:** [CITED: pinn_instruction/markdown_conversion/framework-specs/trainex-r1/DELIVERY-NOTE.md:18-22]
> "R1 is delivered as two parallel sub-packages with different output contracts (decision 2026-06-11: a
> single ~10-item package would cost per-topic depth in single-prompt research agents)"

### Pattern 2: Bundling to stay under the 5-attachment cap (Rule 15)

**What:** Rule 15 (2026-07-07) hard-caps uploads at 5 per sub-package; `specs/` snapshots **count**
when uploaded, so multiple spec files must be compiled into **one** bundle file rather than uploaded
individually.
**When to use:** Whenever a package's source material spans more files than the remaining attachment
budget allows.
**Example (adapted for trainex-r2):**
```
# framework-specs-bundle.md — excerpted sections, each citing its bare-filename source

## Two-sided physics-conservation gate definition
Source: ctl_instruction.md:567-572
> `eps_H = max_t |(H(t) - H(0)) / H(0)|`, `SCS = log10(eps_H)`.
> REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`). ...

## Loss Balancing via Warmup Schedule (PHYS-05)
Source: pinn_architecture.md §4.1 (line 633)
> [excerpt of the warmup-schedule contract text]

## Data Fidelity / Physics Residual / Soft Energy / Angular Momentum loss terms
Source: pinn_architecture.md §3.1 (line 292), §3.2 (line 362), §3.4 (line 497), §3.5 (line 611)
> [excerpts]

## Stage 0 definition and Stage 0-1 curriculum recipe
Source: ctl_instruction.md (Stage 0 definition ~line 138; Stage 0-1 recipe table ~line 2003)
> [excerpts]
```
Every citation is `bare-filename.md:line-range` or `bare-filename.md §N.N` — never the full repo path
(`pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`). This satisfies both D-08's
"source-path + line-range citation for each excerpt" requirement and D-11's "zero repo paths" rule
simultaneously (see Common Pitfalls #7).

### Pattern 3: Claims-register construction by direct tag lift (not re-derivation)

**What:** `44-DIAGNOSIS.md` already marks every claim `[FACT]` or `[HYP]` inline. D-09 requires
building PKG-11's claims register by **lifting** these tags, not re-assessing each number's status from
scratch.
**When to use:** Any time a source document already carries a verified/hypothesis distinction in the
project's house style.
**Example:** see Code Examples below for the concrete row-by-row inventory extracted from
`44-DIAGNOSIS.md`.

### Pattern 4: Neutral question framing (v1.5 issue-02 Q-cluster shape)

**What:** The v1.5 issue-02 package poses every contested finding as: (i) the non-authoritative source
position, (ii) the framework-spec position (or "spec is silent"), (iii) the relevant grounded facts by
claim-ID, (iv) a **question** that does not presuppose a resolution.
**When to use:** trainex-r2's five questions should follow the same shape, substituted for this
package's actual inputs (no "issue doc" exists here — substitute the relevant DIAG-04 candidate-cause
context, tagged `[HYP]`, in place of the issue-doc position slot).
**Example (adapted skeleton for Question 1 — training budget/steps):**
```
### Q1 — Training budget / steps

- **What DIAG-04 evidence bears on this:** [FACT] all four runs (smoke, seed41/42/43) completed
  300/300 finite steps; [FACT] per-seed validation trends are still moving at step 300 (2 of 3
  seeds trend differently depending on window definition — 44-DIAGNOSIS.md §4); [FACT] the Phase 38
  single-trajectory overfit control reached its floor in 176 steps (44-DIAGNOSIS.md §1, §4).
  [HYP, context only — not a steer] this report's DIAG-04 ranks "insufficient Stage-0 training
  budget" as candidate #5, Weak support, explicitly because budget and population-scale are
  confounded and cannot be separated by the retained evidence alone (44-DIAGNOSIS.md §6).
- **What the framework spec says:** [cite the Stage-0/curriculum step-budget contract in
  `ctl_instruction.md`, or state "spec is silent on a minimum Stage-0 step count" if that is what
  the excerpt shows].
- **What a complete answer specifies:** a training-budget recommendation (or a governance framework
  for deriving one) that explicitly addresses the budget/population-scale confound noted above —
  i.e., a reasoned position on whether the observed uniform 1500/1500 failure would plausibly
  resolve with more steps at the same population scale, and what evidence would distinguish that
  from a capacity/generalization limit. [Never state a specific recommended step count — that is
  the external agent's deliverable, not this package's.]
- **Question:** What Stage-0 training budget (step count, or a governing rule for determining one)
  is appropriate given the retained evidence, and how would the answer's reasoning distinguish a
  "needs more steps" explanation from a "needs a different recipe at this budget" explanation?
```
This shape can be reused for all five D-05 areas, substituting each question's own [FACT] citations
(see the DIAG-04 candidate-cause mapping already locked in D-05) and its own spec section.

### Anti-Patterns to Avoid

- **Re-deriving fact/hypothesis status from scratch:** 44-DIAGNOSIS.md's tags are the ground truth for
  this distinction (D-09) — do not independently re-judge whether a DIAG-01..03 number is "verified."
- **Treating the build-design output contract (options + suggested defaults + decision sheet) as the
  default because trainex-r1 used it:** D-04 explicitly locks the specwork-style neutral contract for
  trainex-r2 — the directory path (`framework-specs/`) does not determine the output contract; the
  package's *purpose* (remedy-adjudication research vs. user-picks research) does.
- **Uploading spec files individually:** violates Rule 15's bundling requirement the instant a second
  spec file is attached.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Package file/directory skeleton | A new ad-hoc layout | The ERW "files every round creates" skeleton (runbook lines 51-62), single-package-adapted from trainex-r1 | Reinventing risks missing the `DELIVERY-NOTE`/`specs/`/`research_results/`/`<round>-resolution-doc.md` conventions that future rounds (a hypothetical trainex-r3) and any consolidation tooling expect |
| Attachment-count bookkeeping | A custom cap-tracking scheme | ERW Rule 15's explicit exemption list (`DELIVERY-NOTE.md`, `research_results/`, the resolution doc, and the pasted prompt never count) + D-02's 4-file layout | Miscounting risks either silently exceeding the hard cap or wasting the one headroom slot the planner has to work with |
| Claims tagging vocabulary | A new fact/hypothesis taxonomy | The existing `[FACT]`/`[HYP]` tags already in `44-DIAGNOSIS.md` (v1.4/v1.5/v1.6 house style) | 44-DIAGNOSIS.md was deliberately authored in this style "precisely so the register is a direct lift" (D-09) — inventing a new taxonomy forces re-deriving verified/hypothesis status from scratch and risks disagreeing with Phase 44's own classification |
| Neutral-question document shape | A bespoke Q&A format | The v1.5 issue-02 Q-cluster pattern (position / spec-position / facts / question) | Already proven and precedent-consistent; naturally satisfies Rule 9's "record gaps, never invent" culture because each block ends in an open question, not an assertion |
| Self-containment auditing | Manual eyeballing only | A grep-based pre-delivery check for repo-path markers, scoped to **authored** files only (Common Pitfalls #1, #7) | Manual review misses subtle path leaks; but the check must exclude the verbatim-snapshot exemption or it will "fail" on fully compliant content |

**Key insight:** Nearly everything Phase 45 needs already exists in the repo in a form built for exactly
this purpose — 44-DIAGNOSIS.md was written *for* this package (its own closing line says so:
"This report is Phase 45's trainex-r2 centerpiece"), the ERW runbook was written *from* the trainex-r1 +
issue-02 rounds' hard-won lessons, and the v1.5 precedent already solved "how do you neutrally frame a
question without presupposing its answer." The task is curation and precedent-mirroring, not invention.

## Common Pitfalls

### Pitfall 1: Scrubbing 44-DIAGNOSIS.md's internal repo-path citations
**What goes wrong:** Applying D-11's "zero repo paths in any authored upload" rule to the diagnosis
snapshot itself, stripping its `evidence/diag01/eps_h_distribution.json`, `.planning/phases/44-*`, and
`43-VERDICT.md:27-49`-style citations.
**Why it happens:** D-11 and D-08 look contradictory at a skim (one says "zero repo paths," the other
snapshots a document full of them).
**How to avoid:** D-11 applies to files **authored by Phase 45** (the master, the prompt, and the two
excerpt bundles). D-08 explicitly exempts **verbatim snapshots** (`specs/` content and, by the same
logic, `44-DIAGNOSIS.md` itself, which is uploaded as a snapshot per D-02 item 2): "do not scrub them —
that breaks commit-pin fidelity." The master instructs the external agent to treat any reference to a
file *not* among the 4 attachments as unavailable.
**Warning signs:** If the uploaded `44-DIAGNOSIS.md` differs at all from the Phase-44 original (beyond a
frontmatter note), fidelity has been broken.

### Pitfall 2: Miscounting the 5-attachment cap
**What goes wrong:** Treating `RESEARCH-AGENT-PROMPT.md` as a 5th uploaded file (it is **pasted as
text** below a horizontal rule, never attached — see the ERW runbook's "files every round creates" and
the trainex-r1 precedent's own delivery instructions), or counting `DELIVERY-NOTE.md` /
`research_results/` / the resolution doc against the cap.
**Why it happens:** Skimming Rule 15 without noting its explicit exemption list.
**How to avoid:** Only master + diagnosis + 2 bundles = 4 uploads. The prompt's *header* names which
files to attach; its *body* (below the rule) is pasted directly into the external agent's conversation.
**Warning signs:** A package manifest or delivery note that lists more than 4 items under "files to
attach."

### Pitfall 3: Restating DIAG-04 rankings as settled fact
**What goes wrong:** Package prose reads "the population-scale generalization shortfall causes the
failure" instead of "candidate 1, ranked Strong by this report's agent analysis, is one of five
candidates."
**Why it happens:** DIAG-04's own prose is confident and well-evidenced-sounding even though every
ranking-related sentence in `44-DIAGNOSIS.md` is explicitly tagged `[HYP]`.
**How to avoid:** Every DIAG-04 candidate-cause mention anywhere in the package must carry explicit
"agent analysis, not established fact" framing (D-09, D-12) — this applies inside the claims register,
inside each question block, and inside the master's hard-constraint-vs-baseline tiering section.
**Warning signs:** Any question block that reads as though it already knows the cause, rather than
posing the cause as one candidate among several.

### Pitfall 4: Drifting into a recommended answer via "what a complete answer specifies"
**What goes wrong:** PKG-10's neutral-framing requirement is violated by slipping a preferred
number/schedule/value into the description of what a complete answer looks like.
**Why it happens:** It is natural to want to help the external agent by suggesting a ballpark or
direction.
**How to avoid:** Describe only the **structure** of a complete answer (e.g., "a numeric budget with
justification addressing the budget/population confound noted in candidate 5's contradiction column")
— never a value, direction, or preference. See the worked Q1 template above for the correct register.
**Warning signs:** Any sentence in the package that could be paraphrased as "the answer is probably X."

### Pitfall 5: Splitting the package into sub-packages out of habit
**What goes wrong:** Creating `research_package_a/` + `research_package_b/` because that is what the
mirrored trainex-r1 precedent did.
**Why it happens:** trainex-r1 is the explicitly-designated structure to mirror, and it is split.
**How to avoid:** D-01 is explicit — 5 questions is under Rule 10's ~6-7-item split threshold; single
`research_package/` only. The precedent to mirror is the *file skeleton and delivery-note pattern*, not
the split decision itself.
**Warning signs:** Any directory named `research_package_a/` or `_b/` under `trainex-r2/`.

### Pitfall 6: Pre-deciding the D-13 todos instead of surfacing them
**What goes wrong:** The assembly agent silently picks an outcome for the r1b-relationship question or
the d-06-inclusion question (e.g., states "r1b is unrelated to trainex-r2" as a conclusion) instead of
posing it to the owner.
**Why it happens:** `--auto` discussion mode auto-selected the recommended option everywhere else in
this phase's decisions, creating momentum to do the same here.
**How to avoid:** D-13 explicitly overrides the auto-fold — both items are Success-Criterion-4-locked
as owner-surfaced, never agent-decided, "even though" they scored above the 0.4 auto-fold threshold.
**Warning signs:** `DELIVERY-NOTE.md` states a conclusion about either todo instead of presenting an
A/B/C question with the owner's pick left blank (see the starting menu in Open Questions below).

### Pitfall 7: Directory-prefixed citations inside authored excerpt bundles
**What goes wrong:** An excerpt citation in `framework-specs-bundle.md` or `run-evidence-bundle.md`
reads "Source: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, lines
567-572" instead of "Source: `ctl_instruction.md:567-572`."
**Why it happens:** D-08 requires "a source-path + line-range citation for each excerpt," which sounds
like it wants a full repo-relative path.
**How to avoid:** "Source-path" in D-08 should be read as **bare filename**, consistent with D-11's
absolute "zero repo paths, refer to companion files by bare filename only" rule — the two decisions are
compatible only under this reading. Cite `ctl_instruction.md:567-572`, never the
`pinn_instruction/.../framework-specs/...` prefix. (Flagged for planner confirmation in Open Questions
— this is this research's own interpretive reconciliation of D-08 and D-11, not a verbatim CONTEXT.md
statement.)
**Warning signs:** Any citation string containing a `/` that is not part of a filename extension or a
line-range separator.

### Pitfall 8: Stale snapshot after a late spec/evidence edit
**What goes wrong:** Someone edits `ctl_instruction.md`, or re-runs a Phase-44 diag script, between
assembly and actual handoff to the external agent, and the package's snapshot silently drifts from
`source_baseline`.
**Why it happens:** Assembly (this phase, committed) and delivery (the user's handoff action) are not
guaranteed to be simultaneous.
**How to avoid:** ERW Rule 5: "If a source document is edited after packaging... refresh the snapshot."
44-DIAGNOSIS.md itself models the right discipline — it records a "pre-shipping re-run" step
immediately before commit, confirming all three diag scripts were byte-unchanged and all 15/15 manifest
hashes still matched. The planner should include an equivalent pre-delivery diff/re-check step in the
phase's acceptance criteria.
**Warning signs:** A gap between the package's `source_baseline` commit and the repo's current HEAD at
the moment of actual handoff.

## Code Examples

These are markdown/documentation templates (this phase's domain), not software code, but follow the
same "verified pattern from source" discipline.

### RESEARCH-CONTEXT-MASTER.md frontmatter (mirrors the trainex-r1a precedent)
```yaml
---
title: Trainex R2 Research Context Master — Stage-0 Physics-Gate Training-Recipe Questions
package_for: trainex-r2 (single sub-package)
role: research-context entry point (orientation, hard-constraint-vs-baseline tiering, 5 framed
  questions, claims register, output contract)
status: active
created: <assembly date>
source_baseline: <repo HEAD sha at package assembly, D-07>
self_contained: true
---
```
Source: pattern adapted from
`pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/RESEARCH-CONTEXT-MASTER.md:1-9`.

### Per-file manifest table (bare filenames only, D-11)
```markdown
| File | Role | How to treat it |
|---|---|---|
| `44-DIAGNOSIS.md` | The forensics centerpiece — verbatim snapshot of Phase 44's diagnosis | [FACT]-tagged content is established; [HYP]-tagged content (§5-6, the ranked candidates) is agent
  analysis, not settled — see the Claims Register section below |
| `framework-specs-bundle.md` | Excerpted, locked spec sections (gate definition, loss catalog,
  PHYS-05 schedule, Stage-0 recipe) | Authoritative — these are locked v1.4/v1.6 conventions, not open
  to challenge |
| `run-evidence-bundle.md` | Excerpted run evidence (metrics/receipt, 43-CALIBRATION, 43-VERDICT) | Authoritative record of what the retained evaluation artifacts show |
```
Source: table shape from
`pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/RESEARCH-CONTEXT-MASTER.md:45-49`.

### Claims register rows — direct inventory lifted from 44-DIAGNOSIS.md

**`[FACT]` rows (verified, cite 44-DIAGNOSIS.md section + underlying evidence file):**
- Gate FAIL: `eps_H = 237.2086056078468` vs reject threshold `1e-5`; `SCS = 2.3751304405952904` vs
  reject threshold `-5.0` — 44-DIAGNOSIS.md §1, §2; `runs/stage0-pilot-seed42/evaluation/metrics.json`
- Uniform, population-wide failure: **1500/1500** held-out trajectories exceed `1e-5`; `min =
  0.9741251227996501` — 44-DIAGNOSIS.md §1, §2.1; `evidence/diag01/eps_h_distribution.json`
- Full ε_H distribution (min/p25/p50/p75/p90/p99/max/mean) — 44-DIAGNOSIS.md §2.1
- Phase 38 machinery-integrity control: single-trajectory overfit `L0/Lf = 1097.6107…`, PASS, 176
  steps — 44-DIAGNOSIS.md §1, §4 (citation only, never re-run — SCOPE-23)
- Per-run warmup-spike table (spike step / total / dominant term / share / grad_norm / lr) for smoke,
  seed41, seed42, seed43 — 44-DIAGNOSIS.md §3; `evidence/diag02/loss_decomposition.json`
- `lambda_phys` reaches 1.0 at step 31 in all four runs; `lambda_l == 0.0` at all 300 steps in all four
  runs — 44-DIAGNOSIS.md §3
- `loss_phys` dominates cumulative view under both raw and λ-weighted aggregation, every run — 44-DIAGNOSIS.md §3
- All four runs finished 300/300 finite steps — 44-DIAGNOSIS.md §3
- Per-seed validation trend (first-vs-last): seed41 improving, seed42 improving, seed43 worsening (1 of
  3) — DISAGREES with 43-CALIBRATION's "2/3 worsened" purely due to differing trend-window definitions,
  neither adjudicated — 44-DIAGNOSIS.md §4
- Final-loss spread reproduces 43-CALIBRATION exactly (relative span `3.8224247683129153`, matches
  within 1e-9) — 44-DIAGNOSIS.md §4
- Held-out splits diverge across seeds (smoke/seed42 byte-identical SHA-256; seed41/seed43 differ) — 44-DIAGNOSIS.md §4
- GAP-44-01 resolution: worst-case max IS the gate statistic (owner instruction, option A, 2026-07-23);
  verdict-neutral because 1500/1500 fail under any aggregate — 44-DIAGNOSIS.md §GAP-44-01

**`[HYP]` rows (agent analysis — NOT established fact, cite 44-DIAGNOSIS.md §5-6):**
- Candidate 1 — Population-scale generalization shortfall — **Strong** support
- Candidate 2 (tie) — Loss-term imbalance (`loss_phys` dominance, `lambda_l = 0`) — **Moderate** support
- Candidate 3 (tie) — Optimization/warmup pathology — **Moderate** support
- Candidate 4 (tie) — Normalization/data-scale mismatch — **Moderate** support
- Candidate 5 — Insufficient Stage-0 training budget — **Weak** support
- The tie-breaking rationale and the closing interpretive paragraph of §1 ("the gate failure therefore
  emerges at population scale... not from a machine that cannot fit a trajectory") — both explicitly
  `[HYP]`

A suggested (non-locked, planner-discretion) ID scheme: `F-01..` for facts, `H-01..` for hypotheses,
referencing the 44-DIAGNOSIS.md section number — see Open Questions #3.

### RESEARCH-AGENT-PROMPT.md header pattern (files-to-attach + pasted body)
```markdown
**[User instructions — not part of the prompt]** Attach these 4 individual files to the external
agent's conversation, then paste everything below the horizontal rule as the prompt:

1. `RESEARCH-CONTEXT-MASTER.md`
2. `44-DIAGNOSIS.md`
3. `framework-specs-bundle.md`
4. `run-evidence-bundle.md`

---

[prompt body — pasted as text, not uploaded as a file]
```
Source: `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/RESEARCH-AGENT-PROMPT.md:1-11`.

### Self-containment pre-delivery check (D-11 verification)
```sh
# Scope: AUTHORED files only (master, prompt, bundles) — NOT 44-DIAGNOSIS.md (exempt, D-08).
grep -n -E '(\.planning|runs/|framework-specs/|pinn_instruction/)' \
  trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md \
  trainex-r2/research_package/RESEARCH-AGENT-PROMPT.md \
  trainex-r2/specs/framework-specs-bundle.md \
  trainex-r2/research_package/run-evidence-bundle.md
# Expect zero matches. A bare "/" alone is too broad a filter (legitimate in prose, e.g.
# "1500/1500", "τ = 2u − 1", or an external doc URL) — grep for the specific repo-path markers above.
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Split sub-packages (`research_package_a/`+`_b/`) as the default round pattern | Single sub-package by default; split only when a round exceeds ~6-7 work items (Rule 10) | trainex-r1 established the split (2026-06-11); the ERW runbook later codified the explicit threshold | trainex-r2's 5 questions stay under threshold — a single package is the *correct* structure, not a shortcut |
| No formal attachment limit | Hard 5-attachment-per-sub-package cap (Rule 15), with an explicit exemption list for routing/output files | 2026-07-07 | Directly shapes trainex-r2's 4-upload layout with 1 slot of headroom; any 5th uploaded file requires explicit user override |
| Build-design output contract (options menu + suggested defaults + door classification + decision sheet) assumed for any package under `framework-specs/<track>-<round>/` | D-04 explicitly carves out specwork-style neutral framing for trainex-r2 despite the build-design directory path | Locked 2026-07-23 (Phase 45 `45-CONTEXT.md` D-04) | The directory path alone does **not** determine output contract — the package's *purpose* (remedy-adjudication research routed to a future governed milestone, SCOPE-26) does |

**Deprecated/outdated:** None — this is an actively evolving internal methodology (the runbook itself is
frontmatter-tagged `status: active`, `retirement_trigger: superseded by a revised ERW runbook`); there is
no external library-versioning concern.

## Assumptions Log

All factual claims in this research were verified directly by reading the cited repository files
(CONTEXT.md, REQUIREMENTS.md, ROADMAP.md, the ERW runbook, `44-DIAGNOSIS.md`, the trainex-r1 package,
the v1.5 issue-02 package, the two pending todos, `.planning/config.json`, and the relevant spec-section
line numbers via `grep`). No `[ASSUMED]`-tagged (unverified, training-knowledge-only) claims appear in
this document.

One **interpretive reconciliation** (not a factual claim) is worth flagging for planner confirmation
rather than treating as locked: Pitfall #7's reading that D-08's "source-path" citation requirement
means *bare filename*, not a full repo-relative path — this is this research's own resolution of an
apparent tension between D-08 and D-11, not a verbatim CONTEXT.md statement. It is the only reading that
avoids contradiction, but the planner should confirm it explicitly rather than inherit it silently.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|----------------|
| — | (none — see interpretive note above, tracked as Open Question #2, not as an unverified claim) | — | — |

**This table is empty of `[ASSUMED]` rows:** all claims in this research were verified against
repository sources or cited from the locked CONTEXT.md — no user confirmation is needed on factual
grounds. The one open interpretive call is tracked below as Open Question #2.

## Open Questions

1. **Where should `framework-specs-bundle.md` physically live — `specs/` or `research_package/`?**
   - What we know: D-01 lists "`trainex-r2/specs/` (shared snapshot set)" as a top-level round
     artifact; D-02 identifies the bundle as an uploaded attachment; D-08 describes bundle excerpting
     without pinning a directory.
   - What's unclear: CONTEXT.md does not pin the exact subdirectory for the bundle file itself.
   - Recommendation: place `framework-specs-bundle.md` inside `specs/` (keeps it literally a "spec
     snapshot" per ERW's own definition, and preserves Rule 3's "one shared `specs/` directory at round
     root" convention for reuse by any future trainex-r3+ round). Place `44-DIAGNOSIS.md`,
     `run-evidence-bundle.md`, and `CLAIMS-REGISTER.md` in `research_package/` — they are
     evidence/verdict artifacts, not framework specs. This is explicitly Claude's-discretion territory
     per CONTEXT.md's own delegation (bundle *boundaries* are planner-adjustable) — safe to change.

2. **Does D-08's "source-path + line-range citation" mean bare-filename+line, or a fuller path?**
   - What we know: D-11 mandates bare-filename-only references to companion files, absolutely.
   - What's unclear: D-08's phrase "source-path" is not itself defined precisely.
   - Recommendation: read "source-path" as "bare filename + line-range" (e.g. `ctl_instruction.md:567-572`)
     — the only reading that does not create an internal contradiction between D-08 and D-11. See
     Pitfall #7. This is a process-mechanics interpretation, not a physics/training-recipe call, so it
     is safe for the planner to confirm or adjust without triggering the STOP protocol.

3. **Exact ID/naming scheme for claims-register rows.**
   - What we know: PKG-11/D-09 requires separating `[FACT]` rows from `[HYP]` rows, lifted from
     44-DIAGNOSIS.md's inline tags.
   - What's unclear: CONTEXT.md does not mandate a stable-ID scheme. The v1.5 precedent used `CLM-##`,
     but that scheme is specific to *dataset-count* claims and doesn't fit trainex-r2's mix of
     distribution statistics, per-run tables, and ranked hypotheses as cleanly.
   - Recommendation: a simple two-prefix scheme (`F-01..` for facts, `H-01..` for hypotheses),
     cross-referencing the 44-DIAGNOSIS.md section number, is sufficient — a presentation-only planner
     choice, not a locked decision.

4. **D-13 A/B/C framing content for the two carried-forward todos** (surface, do not decide — locked by
   Success Criterion 4). A starting menu for the planner to refine (content only, owner decides):
   - **`trainex-r1-research-handoff` (r1b relationship):**
     (A) r1b's K-series findings are independent of trainex-r2's training-recipe questions — no
     linkage needed; (B) some r1b findings (e.g., K1's divergence-after-transition health signals) are
     directly relevant context for trainex-r2's warmup/LR and Stage-0-pacing questions and should be
     referenced; (C) r1b handoff should complete first, as a soft precondition on trainex-r2 delivery.
   - **`d-06-static-epsilon-sensitivity-check` (inclusion):**
     (A) include as a 6th trainex-r2 question — note this would require an explicit owner override of
     D-05's locked "exactly the five PKG-10 areas"; (B) do not include — it is explicitly scoped to
     "once the data + processing pipeline exists" (FUT-01/trainex), which does not yet exist; keep it a
     separate, later-triggered verification item; (C) mention it in the package as related-but-out-of-scope
     context, without posing it as a question.
   - These are presented in `DELIVERY-NOTE.md` (never uploaded) per D-10; the assembly agent records the
     owner's pick, never pre-selects one.

5. **43-CALIBRATION.md / 43-VERDICT.md excerpt boundaries within `run-evidence-bundle.md`.**
   - What we know: both files are short (92 and 125 lines respectively) [VERIFIED: `wc -l`
     `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md`,
     `43-VERDICT.md`]; D-02 item 4 calls for "43-CALIBRATION.md excerpts, 43-VERDICT.md excerpts."
   - What's unclear: whether to excerpt specific sections or include both compact files close to in
     full.
   - Recommendation: given both files are well under 150 lines combined, full inclusion (or
     near-full, trimming only administrative sections like "Ratification record" / "Owner sign-off"
     boilerplate) inside `run-evidence-bundle.md` is likely simpler and lower-risk than fine-grained
     section-by-section excerpting — flag for planner confirmation since D-08 technically calls for
     "by section" excerpting.

## Environment Availability

**Skipped.** This phase has no external tool, service, or runtime dependencies beyond `git` (for
commit-pinning, D-07) and standard POSIX text tools (`grep`, `diff`, `cp`) for the self-containment
check and pre-delivery drift verification (Pitfall #8) — all confirmed available in this environment
during this research session (used directly above). There is nothing to audit for availability/fallback
in the sense this section exists for (databases, SDKs, cloud services).

## Security Domain

Most standard ASVS categories do not apply to a documentation-assembly phase (no authentication, no
session management, no application-layer input validation of user-submitted data, no cryptography). The
one genuinely applicable concern is **information disclosure / data exposure** — the package is handed
to an external, non-project party with no repository access, so leaking internal governance context
(commit hashes beyond the intended provenance pin, unrelated `.planning/` gap-register content,
directory structure) would be a disclosure the D-11 self-containment rule is specifically designed to
prevent. This is best treated as a data-handling control folded into the phase's acceptance criteria
(the self-containment grep audit, Pitfall #1/#7), not a formal ASVS gate.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-------------------|
| V2 Authentication | No | N/A — no application, no login surface |
| V3 Session Management | No | N/A |
| V4 Access Control | No | N/A |
| V5 Input Validation | Loosely (data-exposure sense only) | The self-containment grep audit (D-11) functions as an output-sanitization control on authored uploads |
| V6 Cryptography | No | N/A |

### Known Threat Patterns for this domain

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|-----------------------|
| Internal-governance / repo-structure leakage into an externally-shared document | Information Disclosure | D-11 self-containment rule (bare-filename-only references) + pre-delivery grep audit (Pitfall #1/#7), scoped correctly to exclude the D-08-exempt verbatim snapshots |
| Presenting unverified hypothesis as settled fact to an external, non-adjudicating party | (Not classic STRIDE — governance/integrity risk specific to this project's STOP protocol) | D-09/D-12 `[FACT]`/`[HYP]` tagging discipline carried through every package artifact (Pitfall #3) |

## Sources

### Primary (HIGH confidence — read directly, this session)
- `.planning/phases/45-trainex-r2-erw-package-assembly/45-CONTEXT.md` — locked D-01..D-15 decisions
- `.planning/REQUIREMENTS.md` — PKG-09/10/11 verbatim, SCOPE-22..26
- `.planning/ROADMAP.md` — Phase 45 goal + 5 success criteria, investigation discipline
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — canonical ERW runbook, read in full
- `.planning/phases/44-physics-gate-forensics/44-DIAGNOSIS.md` — read in full; [FACT]/[HYP] inventory extracted
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/DELIVERY-NOTE.md` — read in full
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/RESEARCH-CONTEXT-MASTER.md` — read in full
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/research_package_a/RESEARCH-AGENT-PROMPT.md` — read in full
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/RESEARCH-CONTEXT-MASTER.md` — sectioned read (headers + Framed Research Questions + CLM Claims Register)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/DELIVERY-NOTE.md` — read in full
- `.planning/todos/pending/trainex-r1-research-handoff.md`, `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md` — read in full
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_architecture.md` — grepped for gate-definition, loss-catalog, PHYS-05, and Stage-0 section line anchors
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`, `43-CALIBRATION.md` — size/section-header verified
- `.planning/config.json` — verified `nyquist_validation: true`, no `security_enforcement` override present

### Secondary
- None — no web/external research was invoked; this domain is entirely internal repo process/governance,
  confirmed by `gsd-tools query init.phase-op 45` returning all external-search providers (`brave_search`,
  `firecrawl`, `exa_search`) as `false` for this project, consistent with no external technology stack to
  research.

### Tertiary
- None.

## Metadata

**Confidence breakdown:**
- Package structure / ERW mechanics: HIGH — directly read the canonical runbook, both precedent
  packages in full or by targeted section, and the locked CONTEXT.md decisions.
- Claims-register construction: HIGH — directly extracted the full [FACT]/[HYP] inventory from
  44-DIAGNOSIS.md itself.
- Neutral-question framing: HIGH — directly read the v1.5 issue-02 precedent's actual question blocks
  and claims-register format.
- Spec-section line anchors (for bundle excerpting): MEDIUM — located via `grep` (exact line numbers
  confirmed), but the planner/executor should re-confirm exact excerpt boundaries when actually building
  `framework-specs-bundle.md`, since section content itself was not read in full (only anchor lines).
- D-08/D-11 citation-format reconciliation (bare-filename-only in bundle citations): MEDIUM — this
  research's own interpretive resolution of an apparent tension, not a verbatim CONTEXT.md statement;
  flagged explicitly in Open Questions #2 for planner confirmation.

**Research date:** 2026-07-24
**Valid until:** No expiry in the conventional sense — this research is grounded in fixed, already-committed
repository artifacts (44-DIAGNOSIS.md, the ERW runbook, the trainex-r1/v1.5 precedents) that will not
drift during Phase 45's execution window. Re-validate only if any cited source document is edited before
planning begins (re-run the relevant `grep`/`wc -l` checks).
