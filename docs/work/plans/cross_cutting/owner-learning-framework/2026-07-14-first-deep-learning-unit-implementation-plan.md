---
status: active
purpose: implementation-plan
created: 2026-07-14
milestone: untracked
phase: cross-cutting
retirement_trigger: the standalone learning workspace and Unit 0001 have completed one learner attempt and correction cycle, execution provenance is recorded, and a reference audit permits retirement
execution_status: not-executed
review_status: none
---

# First Deep Learning Unit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Use the `teach` skill for the learner-facing files and feedback loop. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch implementation subagents unless the user explicitly authorizes them; the one required independent review in Task 4 is read-only.

**Goal:** Create the smallest complete standalone learning workspace and use it to teach one deep unit in which the owner can distinguish representation, optimization, and generalization when evaluating a neural network.

**Architecture:** Learning lives under root-level `learning/` and advances independently of GSD phases. Markdown files hold the mission, curriculum state, resources, teaching preferences, lesson, and compact reference; the lesson itself holds the complete learner-attempt and feedback history. Execution has a hard learner checkpoint: release the lesson, stop for an independent attempt, preserve that attempt verbatim, provide diagnostic feedback, and create a learning record only if a corrected re-attempt demonstrates understanding.

**Tech Stack:** Markdown rendered in Obsidian or Typora, LaTeX/MathJax, local authoritative project specifications, primary or authoritative ML sources, `rg`, `curl`, Git, and the repository's `scripts/agent-commit` wrapper. No new package, renderer, JavaScript, stylesheet, or build step.

## Source design

Implement this plan against:

- `docs/work/designs/cross_cutting/owner-learning-framework/2026-07-13-owner-learning-framework-design.md`
- especially §§2–10 and “Sample Orientation 0 — A neural network grows from the regression idea”

The accepted design overrides the generic `teach` skill in one intentional respect: lessons are canonical Markdown because the owner reads in Obsidian or Typora. HTML is reserved for a later lesson that genuinely needs interaction. Do not create `assets/` or duplicate the sample orientation merely to satisfy the skill's generic HTML default.

## Why Unit 0001 comes first

Orientation 0 revealed a load-bearing misconception: the owner associated additional layers with additional fitting and therefore with greater accuracy. The useful correction is not merely “bigger is not always better.” The owner needs three separate questions:

1. **Representation:** Is the model class rich enough, relative to this target, to contain a function capable of the required mapping?
2. **Optimization:** Did the training process find a sufficiently good member of that class?
3. **Generalization:** Does the fitted function work on relevant cases that did not determine its parameters?

Every later unit about loss curves, validation, physics residuals, architecture, or training decisions depends on this distinction. Unit 0001 is therefore both misconception repair and a prerequisite; it is not selected because Phase 39 is current.

## Definition of done

The first pass is complete only when all of the following are true:

1. `learning/` contains a concise mission, curriculum, annotated resources, stable teaching notes, one Markdown deep unit, and one reusable diagnostic reference.
2. Orientation 0 is registered as historical **exposure**, not copied into `learning/` and not claimed as demonstrated knowledge.
3. Unit 0001 teaches one observable capability: classify evidence as representational, optimization, or generalization evidence and state what the evidence does not establish.
4. The unit includes an algebraic worked example, guided classification practice with immediate feedback, a novel project-transfer prompt, and a delayed-review hook.
5. Every substantive technical claim is traceable to an annotated high-trust source; project-specific claims use the authoritative spec or recorded project evidence, never legacy live code under `pinn/`.
6. A fresh read-only reviewer passes the source, project-truth, pedagogy, answer-key, and misconception-risk checks before the lesson is released.
7. The owner completes an independent attempt. That attempt is preserved verbatim and receives diagnostic feedback followed by one corrected re-attempt.
8. `learning/learning-records/` is absent until the owner demonstrates non-trivial understanding. If the re-attempt remains incomplete, Unit 0001 ends this pass in `practicing` without a learning record.
9. Learning state and review scheduling are updated by learning events only. No Phase 39 or future GSD phase is blocked, delayed, or made a prerequisite.
10. The plan's execution provenance is closed in a separate commit after the learner interaction cycle.

## Global constraints

- **Worktree:** Execute on `master` in `<home>/Desktop/3_body_problem`. This is cross-cutting learning governance. Do not edit `.worktrees/trainex`, its `milestone/v2.0` branch, or Phase 39 artifacts.
- **Dirty-tree safety:** Start and pre-commit with `git status --short --branch`; preserve every unrelated modification and untracked file. Stage only files named by the active task.
- **Cadence separation:** Project work may nominate examples but never schedules or gates this lesson.
- **One capability:** Supporting ideas are allowed only when they help the owner distinguish representation, optimization, and generalization.
- **Depth:** Target 25–45 minutes for acquisition plus an independent response. Depth comes from a derivation, contrasts, evidence interpretation, transfer, and correction—not from adding more vocabulary.
- **Canonical reader:** Use Markdown with LaTeX delimiters for Obsidian/Typora. Use `<mark>` for key phrases and at most one `<mark><u>...</u></mark>` load-bearing clause per major explanatory step.
- **Terminology:** The title preserves “Capacity is not accuracy,” but the lesson must state that “accuracy” is colloquial here. For regression, prefer **achieved performance**, **training loss**, and **held-out performance**.
- **Evidence states:** Use `queued`, `introduced`, `practicing`, `demonstrated`, and `retained`. Reading can create only `introduced`; delayed successful retrieval is required for `retained`.
- **Learner ownership:** Never fabricate or pre-fill an owner answer. Never overwrite an old prompt, answer, feedback block, or re-attempt.
- **Runtime values are not authoring placeholders:** ISO dates and verbatim learner responses are supplied only when those events occur. Examples in this plan label those insertion points; no literal `YYYY-MM-DD` or bracketed learner-response marker may remain in an implemented learning file.
- **Feedback:** No number or letter grade. Identify correct parts, classify the gap as incomplete/imprecise/misconception, make the smallest correction—preferably with a counterexample—and request one re-attempt in the owner's own words.
- **Source discipline:** The lesson may simplify, but it may not turn a sufficient condition into a guarantee. Use “supports,” “suggests,” or “is most consistent with” when the presented evidence does not uniquely prove a diagnosis.
- **No premature learning record:** Merely covering material or receiving an initial answer never justifies a learning record.
- **No new tooling:** Do not introduce markdown plugins, a lesson generator, tests framework, front-end code, or an automated scheduler in this slice.
- **Commits:** Use explicit `git add` paths and `scripts/agent-commit` with actual `GIT_AGENT_ID` and exact `GIT_AGENT_OWNED_PATHS`. Never use raw `git commit` or broad staging.

## File map

| File | Action | Responsibility |
|---|---|---|
| `learning/MISSION.md` | Create | Concrete reason, observable success, constraints, and scope walls |
| `learning/CURRICULUM.md` | Create, then update | Dependency map, evidence state, active unit, and review triggers |
| `learning/RESOURCES.md` | Create | Small annotated high-trust source set |
| `learning/NOTES.md` | Create | Stable owner teaching preferences; not a session log |
| `learning/reference/capacity-optimization-generalization.md` | Create | Reusable diagnostic table and decision sequence |
| `learning/lessons/0001-capacity-is-not-accuracy.md` | Create, then update | Deep teaching, independent attempt, feedback, and re-attempt history |
| `learning/learning-records/0001-capacity-does-not-guarantee-performance.md` | Create conditionally during Task 7 | Evidence-backed learning record; absent if understanding is not yet demonstrated |
| `docs/work/plans/cross_cutting/owner-learning-framework/2026-07-14-first-deep-learning-unit-implementation-plan.md` | Update only at close | Execution provenance and lifecycle status |

Do not create a copy of Orientation 0, `learning/assets/`, an answer-key file, a session journal, or any Unit 0002 content.

---

### Task 1: Establish the learning compass and initial state

**Files:**

- Create: `learning/MISSION.md`
- Create: `learning/CURRICULUM.md`
- Create: `learning/NOTES.md`

**Interfaces:**

- Consumes: the accepted owner baseline and learning/work separation in the source design.
- Produces: the stable mission and state vocabulary used by all later lesson work.

- [ ] **Step 1: Verify branch, hooks, and ownership before writing**

Run:

```bash
git status --short --branch
git worktree list --porcelain
git config --get core.hooksPath
scripts/agent-claim learning
scripts/agent-claim docs/work/plans/cross_cutting/owner-learning-framework
```

Expected:

- current branch is `master`;
- `.worktrees/trainex` appears separately on `milestone/v2.0`;
- hook path is `.githooks` (otherwise run `scripts/setup-git-hooks.sh` before continuing);
- unrelated dirty paths remain untouched;
- claims succeed or only report the current executor's existing claims.

Set `GIT_AGENT_ID` in the shell to the actual executing agent, tool, and model. Do not use the plan author's identity.

- [ ] **Step 2: Create `learning/MISSION.md` with this exact mission**

```markdown
# Mission: Verify and reason about the three-body PINN project

## Why
Build enough mathematical, physical, and machine-learning working competence to judge important agent claims, interpret project evidence, and participate in bounded design decisions instead of relying on fluent-sounding explanations.

## Success looks like
- Explain an important model or physics mechanism in original words.
- Carry out a small derivation, calculation, evidence inspection, or debugging move.
- Distinguish a plausible project claim from one that the available evidence does not establish.
- Interpret a loss curve, residual, data split, or validation result and name what remains unknown.
- Make a bounded technical tradeoff while stating uncertainty and the evidence needed next.

## Constraints
- Project work and learning advance independently; neither waits for the other unless the owner explicitly creates a learning gate.
- Prefer one useful capability per deep unit, usually in a 25–45 minute acquisition session plus shorter practice and review.
- Reuse the owner's AP Calculus BC, multivariable calculus, differential equations, AP Statistics, AP Physics C, and Python background; expect the details to be rusty.
- Canonical lesson readers are Obsidian and Typora.
- Reading creates exposure, not mastery; demonstrated use and delayed retrieval are required before future lessons assume competence.

## Out of scope
- Completing a survey of all machine learning or mathematical physics before project work continues.
- Following the GSD roadmap as a lesson schedule.
- Learning legacy implementation details line by line.
- Treating model size, low training loss, or polished agent prose as proof of scientific validity.
```

- [ ] **Step 3: Create `learning/NOTES.md` with stable preferences only**

```markdown
# Teaching Notes

- The owner moves through project phases quickly, so learning cadence must remain independent of work cadence.
- Broad orientations are useful maps when every idea is explicitly shallow; deep units must produce one useful, observable capability.
- Prefer depth through a worked derivation, evidence interpretation, transfer, feedback, and later retrieval—not through vocabulary volume.
- Start from the owner's existing calculus, statistics, physics, and Python knowledge, but reactivate rusty prerequisites briefly.
- Use plain language before formal notation. Define a new term once intuitively and once precisely.
- Use Markdown, LaTeX math, `<mark>` for the conceptual spine, and `<mark><u>` only for a genuinely load-bearing clause.
- Preserve every learner attempt verbatim. Give diagnostic feedback without grades and ask for a corrected re-attempt.
- Do not record coverage as learning. Create learning records only from demonstrated understanding, corrected misconceptions, meaningful prior knowledge, or a mission change.
- Current project examples are welcome when they clarify a concept, but work relevance is a tie-breaker rather than the lesson clock.
```

- [ ] **Step 4: Create `learning/CURRICULUM.md` with explicit initial state**

Use this content:

```markdown
# Learning Curriculum

## Evidence states

- **queued** — selected as a likely future capability but not yet taught.
- **introduced** — encountered in an orientation or lesson; no mastery claim.
- **practicing** — attempted, but correction or more application is still needed.
- **demonstrated** — used correctly in an explanation or application without copying lesson wording.
- **retained** — retrieved and applied correctly after delay.

## Dependency map and queue

| ID | Capability | Depends on | State at workspace creation | Evidence or next action |
|---|---|---|---|---|
| O0 | Map regression to a layered neural network | AP Statistics least-squares | introduced | Historical sample in the source design; three corrected re-attempts remain pending. |
| U1 | Distinguish representation, optimization, and generalization from evidence | O0 vocabulary only | queued | First deep unit; repairs “more layers means more fitting and accuracy.” |
| U2 | Derive one gradient update and explain what autograd records | U1 | queued | Start only after U1's three-way distinction is at least demonstrated or deliberately deferred. |
| U3 | Translate three-body state and scaling into model inputs and outputs | algebra, mechanics | queued | Independent of project phase numbering. |
| U4 | Derive one physics residual from a second-order ODE | U2, U3 | queued | No implementation detail until the mathematical residual is understood. |
| U5 | Interpret training, validation, and physical-consistency evidence | U1, U4 | queued | Reuses U1 rather than reteaching capacity versus achieved performance. |
| U6 | Explain curriculum stages, checkpoints, recovery, and reproducibility evidence | U1, U5 | queued | Final item in the provisional sequence, not a promised endpoint. |

## Active unit

No unit is active until Unit 0001 is source-checked and released. The executor changes U1 from `queued` to `introduced` at that release; the learner's attempt then determines whether it becomes `practicing` or `demonstrated`.

## Review queue

No delayed review is due at workspace creation. A demonstrated capability receives:

1. a short reactivation at the next learning session;
2. a contrast or application question after at least one later unit; and
3. a longer-delay check, normally 1–4 weeks later, chosen from observed difficulty.

Failed retrieval returns a capability to `practicing`; it does not erase the prior attempt.

## Topic nominations from work

None recorded. A nomination is a pointer to a useful example, never an automatic lesson or a phase gate.
```

- [ ] **Step 5: Validate structure and the absence of premature records**

Run:

```bash
test -f learning/MISSION.md
test -f learning/CURRICULUM.md
test -f learning/NOTES.md
test ! -d learning/learning-records
rg -n '^## (Why|Success looks like|Constraints|Out of scope)$' learning/MISSION.md
rg -n '^## (Evidence states|Dependency map and queue|Active unit|Review queue|Topic nominations from work)$' learning/CURRICULUM.md
git diff --check -- learning/MISSION.md learning/CURRICULUM.md learning/NOTES.md
```

Expected: all commands exit `0`; the mission prints four section headings, the curriculum prints five, and `learning/learning-records/` does not exist.

- [ ] **Step 6: Commit the workspace foundation**

Before staging, run `git status --short --branch` and confirm only the three new learning files are in this task's write set.

```bash
git add learning/MISSION.md learning/CURRICULUM.md learning/NOTES.md
git diff --cached --check
git diff --cached --name-only
GIT_AGENT_OWNED_PATHS='learning/MISSION.md:learning/CURRICULUM.md:learning/NOTES.md' \
  scripts/agent-commit -m "docs(docs): establish owner learning workspace" \
  -m "Record the independent learning mission, evidence-state curriculum, and stable teaching preferences without coupling them to GSD phases."
```

Expected staged names before commit: exactly the three paths above. Expected commit result: one atomic documentation commit on `master` with the wrapper-added attribution trailer.

---

### Task 2: Curate the sources and reusable diagnostic reference

**Files:**

- Create: `learning/RESOURCES.md`
- Create: `learning/reference/capacity-optimization-generalization.md`

**Interfaces:**

- Produces: the source set that grounds Unit 0001 and the compact conceptual tool reused by Units 0002 and 0005.
- Does not produce: a lesson answer key or a learning record.

- [ ] **Step 1: Verify the three external technical sources**

Run:

```bash
for url in \
  https://www.deeplearningbook.org/contents/ml.html \
  https://www.deeplearningbook.org/contents/optimization.html \
  https://arxiv.org/abs/1611.03530
do
  curl -L --max-time 20 -s -o /dev/null -w '%{http_code} %{url_effective}\n' "$url"
done
```

Expected: HTTP `200` for all three. If a host is temporarily unavailable, do not replace it with an unreviewed blog; verify the title/claim through the publisher, arXiv record, or another primary host and annotate the alternate primary URL.

The source pass must confirm these exact uses:

- Goodfellow, Bengio, and Courville, *Deep Learning*, Chapter 5 §5.2: capacity, underfitting, and overfitting; use for the representation/generalization distinction.
- Goodfellow, Bengio, and Courville, Chapter 8 §8.1: learning differs from pure optimization; use for the optimization/generalization distinction.
- Zhang et al., “Understanding deep learning requires rethinking generalization,” arXiv:1611.03530: sufficiently expressive networks can fit random labels, so near-zero training error does not by itself establish generalization.

- [ ] **Step 2: Create `learning/RESOURCES.md`**

Use this annotated resource set:

```markdown
# Three-Body PINN Learning Resources

## Knowledge

- [Book chapter: “Machine Learning Basics” — Goodfellow, Bengio, and Courville](https://www.deeplearningbook.org/contents/ml.html)
  Foundational treatment of capacity, underfitting, overfitting, validation, and generalization. Use for: separating what a model class can represent from how a fitted model performs on unseen cases; Unit 0001 relies mainly on §5.2.
- [Book chapter: “Optimization for Training Deep Models” — Goodfellow, Bengio, and Courville](https://www.deeplearningbook.org/contents/optimization.html)
  Authoritative account of optimization in deep learning and why minimizing a training objective is not the whole learning problem. Use for: separating optimization evidence from generalization evidence; Unit 0001 relies mainly on §8.1.
- [Paper: “Understanding deep learning requires rethinking generalization” — Zhang et al.](https://arxiv.org/abs/1611.03530)
  Primary empirical counterexample showing that high-capacity neural networks can fit random labels. Use for: explaining why capacity and near-zero training error do not guarantee useful unseen performance.
- [Visual orientation: “But what is a neural network?” — 3Blue1Brown](https://www.3blue1brown.com/lessons/neural-networks)
  Accessible bridge from weighted sums and activations to layered networks. Use for: reactivating Orientation 0 vocabulary, not as the depth source for Unit 0001.
- [Local design: Owner Learning Framework](../docs/work/designs/cross_cutting/owner-learning-framework/2026-07-13-owner-learning-framework-design.md)
  Governs the independent learning cadence, deep-unit contract, feedback loop, retrieval schedule, and the preserved Orientation 0 attempts. Use for: teaching-process decisions.
- [Local specification: PINN architecture](../pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md)
  Authoritative project architecture contract. Use for: any Unit 0001 project-specific architecture statement; do not substitute legacy live code under `pinn/`.

## Wisdom (Communities)

No external community task is assigned in Unit 0001. The first transfer target is the owner's own project evidence. Revisit community-based critique only when the owner wants external practitioner feedback.

## Gaps

- Unit 0001 does not attempt a literature review of PINN-specific generalization. Curate that evidence when Unit 0005 begins; it is not needed to learn the representation/optimization/generalization distinction.
```

Check the relative local links from the `learning/` directory:

```bash
test -f docs/work/designs/cross_cutting/owner-learning-framework/2026-07-13-owner-learning-framework-design.md
test -f pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

- [ ] **Step 3: Create the reusable diagnostic reference**

Write `learning/reference/capacity-optimization-generalization.md` with the following substantive content. Use the project's visual-emphasis convention, but do not decorate every cell.

```markdown
# Diagnosing Model Failure: Three Different Questions

| Question | Name | Strongest simple evidence | What that evidence does not prove |
|---|---|---|---|
| Is the chosen model class rich enough, relative to this target, to contain a sufficiently good function? | **Representation** (target-relative use of capacity) | A more expressive class fits the same target substantially better under a trustworthy fitting procedure. | That training will find the good function, or that it will work on unseen cases. |
| Did training find a sufficiently good member of that class? | **Optimization** | The same architecture and data reach very different training losses under different runs or training procedures. | That low training loss will transfer beyond the training cases. |
| Does the fitted function work on relevant cases that did not determine its parameters? | **Generalization** | Performance on a valid held-out set, out-of-sample domain, or independent physical check. | That every deployment regime is covered or that the model is physically valid everywhere. |

<mark><u>Capacity belongs to a model class; training loss belongs to one fitted model on seen evidence; generalization belongs to its behavior on relevant unseen evidence.</u></mark>

## A disciplined diagnostic order

1. Ask whether the training evidence is already poor. If yes, representation and optimization are both candidates.
2. Compare controlled runs or model classes to separate “could not represent” from “training did not find.”
3. Only after fitting the training objective well, ask whether held-out and independent checks also succeed.
4. Name the conclusion at the strength supported by the evidence: “consistent with” is often more honest than “proves.”

## Important caution

The three failures are not mutually exclusive. A model can have inadequate capacity, be difficult to optimize, and generalize poorly at the same time. The framework separates the questions so the next experiment targets the right uncertainty; it is not a guarantee that one metric uniquely identifies one cause.

Capacity is the richness of a model class; representational adequacy asks whether that richness is useful for a particular target. Treating those phrases as related does not make them interchangeable in every theorem or experiment.
```

- [ ] **Step 4: Validate and commit the source foundation**

Run:

```bash
rg -n '^## (Knowledge|Wisdom \(Communities\)|Gaps)$' learning/RESOURCES.md
rg -n 'Representation / capacity|Optimization|Generalization|not mutually exclusive' learning/reference/capacity-optimization-generalization.md
git diff --check -- learning/RESOURCES.md learning/reference/capacity-optimization-generalization.md
git status --short --branch
git add learning/RESOURCES.md learning/reference/capacity-optimization-generalization.md
git diff --cached --check
git diff --cached --name-only
GIT_AGENT_OWNED_PATHS='learning/RESOURCES.md:learning/reference/capacity-optimization-generalization.md' \
  scripts/agent-commit -m "docs(docs): add first learning sources and diagnostic reference" \
  -m "Curate authoritative sources for capacity, optimization, and generalization and provide a reusable evidence-diagnosis reference."
```

Expected staged names before commit: exactly the two Task 2 files.

---

### Task 3: Author Unit 0001 through the independent checkpoint

**Files:**

- Create: `learning/lessons/0001-capacity-is-not-accuracy.md`
- Modify: `learning/CURRICULUM.md`

**Interfaces:**

- Consumes: `learning/MISSION.md`, `learning/NOTES.md`, `learning/RESOURCES.md`, the diagnostic reference, and the source design's preserved Orientation 0 answers.
- Produces: one draft deep unit. U1 remains `queued` until Task 4's review passes.

- [ ] **Step 1: Write lesson frontmatter and learning contract**

Use the actual execution date for `created`; do not leave a date token in the file.

```markdown
---
lesson_id: "0001"
title: Capacity is not accuracy
format: deep-unit
capability_state: introduced
created: YYYY-MM-DD
source_design: docs/work/designs/cross_cutting/owner-learning-framework/2026-07-13-owner-learning-framework-design.md
---

# Unit 0001 — Capacity is not accuracy

**Expected acquisition time:** 25–45 minutes, plus your independent response.

**Capability target:** Given observations about a model, distinguish evidence about representation, optimization, and generalization—and state what the evidence still does not establish.

> In this title, “accuracy” means achieved model performance in ordinary language. This project predicts continuous trajectories, so the precise terms in the unit are *training loss*, *held-out performance*, and *physical consistency*.
```

- [ ] **Step 2: Add a short cold retrieval from Orientation 0**

Before presenting new material, ask exactly these two prompts:

1. “Without reopening Orientation 0: after a neuron forms its weighted sum and adds its bias, what operation comes next, and why does it matter?”
2. “Your earlier answer correctly suspected that accuracy cannot increase without bound. In one sentence, predict what a larger network can guarantee and what it cannot guarantee.”

Explain that these predictions are diagnostic and will be preserved, but do not provide the answers until after the owner has committed to a response. The expected reasoning for the later answer-key pass is:

- a nonlinear activation follows the affine calculation and prevents a stack from collapsing to a single affine map;
- a larger model can increase representational capacity, but cannot guarantee that optimization finds a good function or that the fitted function generalizes.

- [ ] **Step 3: Teach the three-question framework in layers**

The explanation must use this order and these claims:

1. **Intuition:** A large toolbox, the ability to select the right tool, and success on a new job are three different facts. Map them to representation, optimization, and generalization, then retire the analogy rather than stretching it.
2. **Formal statement:** Introduce a model class $\mathcal{F} = \{f_\theta\}$, a fitted member $f_{\hat\theta}$, training loss $L_{\mathrm{train}}(f)$, and unseen or validation loss $L_{\mathrm{unseen}}(f)$. State:
   - capacity describes the richness of $\mathcal{F}$, while the target-relative representation question asks whether a sufficiently good function for this task exists in $\mathcal{F}$;
   - optimization asks whether the training procedure finds useful parameters $\hat\theta$;
   - generalization asks how $f_{\hat\theta}$ behaves on relevant evidence that did not choose $\hat\theta$.
3. **Logical gate:** Show a three-step flow rather than a false additive “error decomposition”:

   ```text
   good-enough function exists in the model class?
                     ↓
   training finds a good-enough member of that class?
                     ↓
   fitted member works on relevant unseen cases?
   ```

4. **Load-bearing sentence:** Use exactly one strongest emphasis in this section:

   ```markdown
   <mark><u>Increasing capacity changes what the model class could represent; it does not by itself choose good parameters or supply unseen evidence.</u></mark>
   ```

Do not describe the three failures as mutually exclusive or claim that one metric uniquely diagnoses them.

- [ ] **Step 4: Include one complete algebraic representation example**

Use the target $y=x^2$ at $x=-1,0,1$ and the affine class $f(x)=wx+b$.

Show the contradiction explicitly:

```math
-w+b=1, \qquad w+b=1
```

Adding the two equations gives $b=1$, and subtracting them gives $w=0$. That forces $f(0)=1$, but the target requires $f(0)=0$. Therefore no parameter choice in the affine class fits all three points. A quadratic class containing $f(x)=x^2$ removes this representational limitation.

State both walls:

- this proves a limitation of this affine class on these points, not a universal method for diagnosing every neural network;
- a richer class makes a correct fit possible, not inevitable.

- [ ] **Step 5: Add optimization and generalization counterexamples**

Use controlled contrasts rather than vague definitions:

- **Optimization contrast:** Same architecture, training data, and objective; two runs or training procedures end at very different training losses. The high-loss run is evidence of an optimization problem because another run demonstrates that the architecture can fit the training objective better. Do not claim that different random seeds are the only possible cause.
- **Generalization contrast:** A fitted model reaches very low training loss while held-out loss stays high or worsens. This is evidence of a generalization gap, not evidence that another layer would fix it.
- **Empirical counterexample:** Briefly summarize Zhang et al. without overclaiming: high-capacity networks in their experiments could fit random labels, demonstrating that capacity and near-zero training error alone are insufficient evidence of useful generalization.

Link the relevant claims inline to Goodfellow Chapter 5 §5.2, Chapter 8 §8.1, and Zhang et al. Do not quote a source at length.

- [ ] **Step 6: Add guided practice with immediate feedback**

Present these three cases first, asking the learner to pause and classify each. Then provide a clearly separated “Check your reasoning” block:

| Case | Observation |
|---|---|
| A | An exact least-squares fit of an affine model cannot match the three $x^2$ points, while a quadratic model matches all three exactly. |
| B | Two runs use the same network, data, and objective; one reaches training loss 100 times lower than the other. |
| C | Training loss keeps falling while held-out loss rises for several evaluations. |

The feedback must say:

- A most directly supports a **representation** diagnosis for the affine class.
- B supports an **optimization** diagnosis for the worse run, because the better run shows the same class can fit the training objective more closely.
- C supports a **generalization** problem, because improvement on seen evidence accompanies deterioration on unseen evidence.
- These are evidence-supported diagnoses, not proof that no second problem coexists.

- [ ] **Step 7: Add the project transfer and independent attempt**

Use this transfer claim:

> “The project network is much larger than a one-layer network, and its training loss is low. Therefore its three-body trajectories are accurate.”

Then create an `## Independent attempt — stop here` section with four numbered responses:

1. **Explain:** In original words, distinguish representation, optimization, and generalization without using the toolbox analogy.
2. **Diagnose:** Classify Cases A, B, and C. For each, cite the observation that supports the classification and name one conclusion the observation does not establish.
3. **Transfer:** Respond to the project claim in 3–5 sentences. State what the larger network and low training loss do support, then name at least three categories of evidence still needed before trusting the trajectories.
4. **Correct the old model:** Rewrite this statement so it is technically sound: “More neurons and layers give more accuracy because more fitting is executed during each layer.” Preserve the correct part rather than replacing the sentence with “bigger is bad.”

Immediately below, tell the owner:

- answer from memory rather than copying lesson phrases;
- uncertainty is allowed and should be named;
- stop after the four responses and return them to the teaching agent;
- the original response will be preserved, diagnosed without a grade, and followed by one corrected re-attempt where needed.

Do not put expected answers, hints that disclose the classification, or prewritten feedback below the independent attempt.

- [ ] **Step 8: Finish the lesson with review hook, walls, sources, and history state**

Add these sections after the independent checkpoint:

`## Review hook`:

> “A very large model achieves almost zero training loss. Draw the three-question diagnostic from memory and name the additional observation you would seek at each step.”

State that it is not due yet. It becomes due at the next learning session only after the current correction cycle.

`## Walls for this unit`:

- proofs of universal approximation;
- VC dimension, Rademacher complexity, and formal generalization bounds;
- double descent and modern scaling-law subtleties;
- optimizer mechanics, gradients, and autograd, reserved for Unit 0002;
- full PINN validation and physics-residual design, reserved for Units 0004–0005.

For each wall, give one sentence explaining that it is deferred because it does not improve the target capability yet.

`## Sources` must contain the three external sources and links from Task 2 plus the local architecture spec for any project-specific statement.

`## Attempt and feedback history` must initially contain only:

```markdown
No Unit 0001 attempt is recorded yet. The learner completes the independent attempt in conversation; the teaching agent appends it here verbatim before giving diagnostic feedback.
```

- [ ] **Step 9: Preserve the pre-release curriculum state**

Confirm that U1 remains `queued` while the lesson is a draft. Do not edit `learning/CURRICULUM.md` in Task 3. The review gate—not file creation—authorizes the `introduced` transition.

---

### Task 4: Review, repair, validate, and commit the releasable lesson

**Files:**

- Modify if findings require it: `learning/lessons/0001-capacity-is-not-accuracy.md`
- Modify if findings require it: `learning/reference/capacity-optimization-generalization.md`
- Modify if findings require it: `learning/RESOURCES.md`
- Modify: `learning/CURRICULUM.md`

**Interfaces:**

- Consumes: the answer-key contract below and the source design's five-pass review rule.
- Produces: a lesson safe to show the owner; no learner response is generated in this task.

- [ ] **Step 1: Run the executor's five-pass self-review**

Check each item explicitly:

1. **Source pass:** every capacity, optimization, and generalization claim maps to one of the three annotated sources; the Zhang example says “insufficient evidence,” not “large networks never generalize.”
2. **Project-truth pass:** any architecture fact is supported by `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`; no file under legacy `pinn/` is cited.
3. **Pedagogy pass:** the unit has one capability, the algebra is complete, guided practice differs from the worked example, independent practice differs from guided practice, and walls remove adjacent theory.
4. **Answer-key pass:** every independent prompt has a determinate expected-reasoning range shown below; no scenario silently requires information the owner has not been given.
5. **Correction-risk pass:** the prose never says each layer fits separately, more capacity means more accuracy, low training loss means truth, or one metric proves a unique root cause.

Expected reasoning range for the independent attempt:

- **Response 1:** representation is whether the class contains a sufficient function; optimization is whether training finds useful parameters; generalization is performance on relevant unseen evidence.
- **Response 2:** A representation, B optimization, C generalization; each answer must cite the observation and withhold a stronger unsupported conclusion.
- **Response 3:** size supports possible capacity and low training loss supports fit to the chosen training objective. Trust still needs, at minimum, valid held-out trajectory performance, physical-consistency or residual evidence, and coverage of the intended domain/edge cases. Baseline comparison, uncertainty, or reproducibility evidence are also valid additions.
- **Response 4:** more neurons/layers may increase capacity, but layers form one jointly optimized function; they do not perform separate fits, and increased capacity guarantees neither successful optimization nor generalization.

- [ ] **Step 2: Obtain one fresh independent adversarial review**

This unit is foundational, so the design's risk-based rule requires a second reader. Give a fresh reviewer only:

- the source design §§3–10;
- `learning/MISSION.md`;
- `learning/RESOURCES.md`;
- `learning/reference/capacity-optimization-generalization.md`;
- `learning/lessons/0001-capacity-is-not-accuracy.md`;
- the answer-key range above.

Ask the reviewer to return findings only—no file edits and no repo review artifact—under these severities:

- **BLOCKER:** factual error, ambiguous answer key, false guarantee, or exercise that cannot assess the target capability;
- **MAJOR:** scope overload, missing feedback opportunity, project-truth drift, or likely misconception left unaddressed;
- **MINOR:** wording, visual hierarchy, or citation placement.

The executor applies every BLOCKER and MAJOR finding before release. Apply MINOR findings only when they improve clarity without expanding scope. Rerun the affected review pass after each fix.

- [ ] **Step 3: Run mechanical validation**

Run:

```bash
lesson=learning/lessons/0001-capacity-is-not-accuracy.md
test -f "$lesson"
rg -n '^## (Independent attempt — stop here|Review hook|Walls for this unit|Sources|Attempt and feedback history)$' "$lesson"
rg -n 'Capability target|Representation|Optimization|Generalization|x\^2|training loss|held-out' "$lesson"
! rg -n '[₀₁₂₃₄₅₆₇₈₉]|[⋅]' "$lesson"
! rg -n 'each layer (fits|performs.*fit)|more (layers|neurons).*(guarantee|give).*accuracy|training loss.*proves' "$lesson"
test ! -d learning/learning-records
git diff --check -- "$lesson" learning/CURRICULUM.md learning/RESOURCES.md learning/reference/capacity-optimization-generalization.md
```

Expected: required headings and terms print; both negated `rg` checks and the no-learning-record check exit successfully; `git diff --check` is silent.

Review the lesson length:

```bash
wc -w "$lesson"
```

Target: roughly 1,800–2,800 words excluding the eventual attempt history. A result outside that range is a review signal, not an automatic failure: shorten repetition or split an overloaded explanation, but do not remove the derivation, practice, transfer, or walls to meet a number.

- [ ] **Step 4: Mark the reviewed unit `introduced`**

Only after Steps 1–3 pass, edit `learning/CURRICULUM.md`:

- change U1 from `queued` to `introduced`;
- replace its next action with “Lesson 0001 released; independent attempt pending.”;
- set `## Active unit` to Unit 0001 and state that reading alone does not advance it beyond `introduced`;
- leave delayed review unscheduled.

- [ ] **Step 5: Commit the reviewed pre-response lesson**

Before staging, run `git status --short --branch` and inspect touched unstaged diffs. Stage only files actually changed by Tasks 3–4:

```bash
git add learning/lessons/0001-capacity-is-not-accuracy.md learning/CURRICULUM.md
git diff --cached --check
git diff --cached --name-only
GIT_AGENT_OWNED_PATHS='learning/lessons/0001-capacity-is-not-accuracy.md:learning/CURRICULUM.md' \
  scripts/agent-commit -m "docs(docs): add first deep owner learning unit" \
  -m "Teach the representation, optimization, and generalization distinction through derivation, guided diagnosis, project transfer, and an independent learner checkpoint."
```

If review fixes also changed `learning/RESOURCES.md` or the diagnostic reference, include only the changed path(s) in both the explicit `git add` and `GIT_AGENT_OWNED_PATHS`, and list them in `git diff --cached --name-only` before committing.

---

### Task 5: Release the lesson and stop for the owner's independent attempt

**Files:** none until the owner responds.

**Interfaces:**

- Produces: learner-owned responses to four prompts.
- Blocks: Task 6 only. It does not block any GSD or Phase 39 work.

- [ ] **Step 1: Open and hand off the lesson**

On macOS, run:

```bash
open learning/lessons/0001-capacity-is-not-accuracy.md
```

Tell the owner, in one short message:

- the lesson is ready;
- the expected acquisition time is 25–45 minutes;
- answer the four independent prompts from memory;
- send the answers back together;
- Phase 39 remains independent and can continue.

- [ ] **Step 2: Stop**

Do not simulate an answer, write “likely feedback,” pre-create a learning record, or advance curriculum state. Wait for the owner's actual response.

---

### Task 6: Preserve the attempt, diagnose it, and request one corrected re-attempt

**Files:**

- Modify: `learning/lessons/0001-capacity-is-not-accuracy.md`
- Modify: `learning/CURRICULUM.md`

**Interfaces:**

- Consumes: the owner's four responses from Task 5.
- Produces: a verbatim attempt, diagnostic feedback, and only the necessary re-attempt prompts.

- [ ] **Step 1: Append the original attempt verbatim**

Replace the initial no-attempt sentence under `## Attempt and feedback history` with:

```markdown
### Initial independent attempt — YYYY-MM-DD

#### Response 1 — Explain
> [owner's exact response]

#### Response 2 — Diagnose
> [owner's exact response]

#### Response 3 — Transfer
> [owner's exact response]

#### Response 4 — Correct the old model
> [owner's exact response]
```

The bracketed lines above describe learner-owned insertion points; copy the actual response bytes there and remove the brackets. Correct no spelling, grammar, notation, or factual content inside the quote blocks.

- [ ] **Step 2: Add diagnostic feedback response by response**

For each response, append four labeled parts:

1. `**What is correct:**` the specific correct reasoning already present;
2. `**Diagnosis:**` exactly one of `complete`, `incomplete`, `imprecise`, or `misconception`, with a concise reason;
3. `**Smallest correction:**` the minimum missing distinction, preferably using one counterexample from the unit;
4. `**Corrected re-attempt:**` one focused prompt, but only when diagnosis is not `complete`.

Do not ask the owner to rewrite a complete answer. Do not bundle new theory into the feedback. If a response is wrong for multiple reasons, choose the first load-bearing error and ask one correction at a time.

- [ ] **Step 3: Update curriculum to reflect evidence honestly**

- Set `capability_state: practicing` in the lesson frontmatter and set U1 to `practicing` in the curriculum while the correction cycle is open.
- If all four initial responses are complete, ask one compact transfer confirmation that differs from the lesson; this is the Task 7 evidence that may advance the state to `demonstrated`.
- Otherwise state which distinction is being corrected and ask only the focused re-attempt needed for it.
- Keep the delayed review unscheduled until the corrected re-attempt arrives.
- Leave `learning/learning-records/` absent.

- [ ] **Step 4: Validate, commit, and ask for the re-attempt**

Run:

```bash
rg -n '^### Initial independent attempt|\*\*What is correct:\*\*|\*\*Diagnosis:\*\*|\*\*Smallest correction:\*\*|\*\*Corrected re-attempt:\*\*' learning/lessons/0001-capacity-is-not-accuracy.md
test ! -d learning/learning-records
git diff --check -- learning/lessons/0001-capacity-is-not-accuracy.md learning/CURRICULUM.md
git status --short --branch
git add learning/lessons/0001-capacity-is-not-accuracy.md learning/CURRICULUM.md
git diff --cached --check
GIT_AGENT_OWNED_PATHS='learning/lessons/0001-capacity-is-not-accuracy.md:learning/CURRICULUM.md' \
  scripts/agent-commit -m "docs(docs): record first learning attempt and feedback" \
  -m "Preserve the owner's independent responses, diagnose them without grading, and request only the corrections needed before recording demonstrated understanding."
```

Return only the focused corrected re-attempt prompt(s) to the owner, with enough context to answer without rereading the full lesson. Then stop again.

---

### Task 7: Evaluate the corrected re-attempt and schedule retention

**Files:**

- Modify: `learning/lessons/0001-capacity-is-not-accuracy.md`
- Modify: `learning/CURRICULUM.md`
- Create conditionally: `learning/learning-records/0001-capacity-does-not-guarantee-performance.md`

**Interfaces:**

- Consumes: the owner's corrected re-attempt from Task 6.
- Produces: either demonstrated state plus a learning record, or practicing state plus a defined next-session correction.

- [ ] **Step 1: Preserve and evaluate the corrected re-attempt**

Append the response verbatim under:

```markdown
### Corrected re-attempt — YYYY-MM-DD
```

Then record:

- which prior issue the re-attempt corrected;
- whether the owner can now distinguish all three questions and withhold unsupported conclusions;
- one sentence explaining the resulting state: `demonstrated` or `practicing`.

Set the lesson frontmatter `capability_state` to the same resulting state. The lesson and curriculum must never disagree.

Do not call the capability demonstrated merely because the owner repeats the three labels. Demonstration requires applying the distinction to evidence or correcting the project claim in original words.

- [ ] **Step 2A: If demonstrated, create the first learning record and review schedule**

Create `learning/learning-records/` lazily and write:

```markdown
# Capacity does not guarantee achieved performance

The owner distinguished representation, optimization, and generalization in original words and used the distinction to reject the claim that a larger network or low training loss alone proves accurate three-body trajectories. Future sessions may assume the three-question diagnostic, but not long-term retention.

## Evidence

See the initial attempt, diagnostic feedback, and corrected re-attempt in `../lessons/0001-capacity-is-not-accuracy.md`.

## Implications

Unit 0002 may build on the difference between “a good parameter setting exists” and “training finds it.” Unit 0005 must reactivate the full three-way distinction before interpreting validation evidence.
```

Update `learning/CURRICULUM.md`:

- set U1 to `demonstrated`;
- cite the learning record as evidence;
- queue the exact review-hook prompt for the next learning session;
- queue a contrast/application prompt after at least one later unit;
- choose the longer review date from observed difficulty: 14 days after a clean correction, 7 days after a correction that required a cue. Record the actual calendar date.

- [ ] **Step 2B: If not demonstrated, keep the evidence state honest**

Do not create `learning/learning-records/`. Keep U1 as `practicing` and add this next-learning-session action to `learning/CURRICULUM.md`:

> Rebuild the three-question diagnostic from a new two-model comparison before starting Unit 0002; use one new counterexample and do not repeat the Unit 0001 cases.

The first plan pass may still close: the system has correctly detected that more correction is needed. Unit 0002 remains queued rather than pretending the prerequisite is secure.

- [ ] **Step 3: Validate and commit the learner-state result**

For the demonstrated path:

```bash
test -f learning/learning-records/0001-capacity-does-not-guarantee-performance.md
rg -n 'demonstrated|next learning session|[0-9]{4}-[0-9]{2}-[0-9]{2}' learning/CURRICULUM.md
git diff --check -- learning/lessons/0001-capacity-is-not-accuracy.md learning/CURRICULUM.md learning/learning-records/0001-capacity-does-not-guarantee-performance.md
git status --short --branch
git add learning/lessons/0001-capacity-is-not-accuracy.md learning/CURRICULUM.md learning/learning-records/0001-capacity-does-not-guarantee-performance.md
git diff --cached --check
GIT_AGENT_OWNED_PATHS='learning/lessons/0001-capacity-is-not-accuracy.md:learning/CURRICULUM.md:learning/learning-records/0001-capacity-does-not-guarantee-performance.md' \
  scripts/agent-commit -m "docs(docs): record demonstrated capacity diagnosis" \
  -m "Preserve the corrected re-attempt, record demonstrated understanding, and schedule learning-time retrieval without coupling it to project phases."
```

For the practicing path, omit the learning-record path from the checks, staging, ownership, and commit; use subject `docs(docs): record capacity diagnosis practice state` and explain in the body that the capability remains practicing.

---

### Task 8: Close plan execution provenance

**Files:**

- Modify: `docs/work/plans/cross_cutting/owner-learning-framework/2026-07-14-first-deep-learning-unit-implementation-plan.md`

**Interfaces:**

- Consumes: completed Tasks 1–7 and the independent lesson review result.
- Produces: a lifecycle-compliant record that the first pass was executed, regardless of whether U1 ended `demonstrated` or honestly remained `practicing`.

- [ ] **Step 1: Update frontmatter and lifecycle state**

Change:

```yaml
status: consumed
execution_status: first-pass-complete
executed_at: YYYY-MM-DDTHH:MM:SS±HH:MM
review_status: reviewed
```

Use the actual local date, time, and timezone offset. Keep the plan in place; do not delete, move, or archive it without the separate audit and explicit approval required by `docs/README.md`.

- [ ] **Step 2: Run final scope and integrity checks**

Run:

```bash
git status --short --branch
git log --oneline --max-count=8
rg --files learning | sort
git diff --check
```

Verify:

- no Phase 39, `.planning/`, `.worktrees/trainex`, framework-spec, or legacy `pinn/` file was modified;
- the lesson contains the verbatim attempt, feedback, and re-attempt;
- U1 is either `demonstrated` with a learning record or `practicing` without one;
- all unrelated pre-existing worktree changes remain present and unstaged by this execution.

- [ ] **Step 3: Commit only the provenance update with required trailers**

```bash
git add docs/work/plans/cross_cutting/owner-learning-framework/2026-07-14-first-deep-learning-unit-implementation-plan.md
git diff --cached --check
git diff --cached --name-only
GIT_AGENT_OWNED_PATHS='docs/work/plans/cross_cutting/owner-learning-framework/2026-07-14-first-deep-learning-unit-implementation-plan.md' \
  scripts/agent-commit -m "docs(docs): record first learning unit execution" \
  -m "Close the first execution pass after the workspace, reviewed lesson, learner attempt, correction, and retention decision are recorded." \
  -m "Plan-Execution: first-pass" \
  -m "Plan-Source: docs/work/plans/cross_cutting/owner-learning-framework/2026-07-14-first-deep-learning-unit-implementation-plan.md"
```

Expected staged name: only this plan file. This commit is separate from every learner-facing work commit.

- [ ] **Step 4: Release advisory claims**

Run:

```bash
scripts/agent-release learning
scripts/agent-release docs/work/plans/cross_cutting/owner-learning-framework
```

Expected: both execution-owned claims are removed; this does not alter Git state.

## Executor handoff

Execute Tasks 1–4 in sequence, then Task 5 must return control to the owner. Resume Tasks 6–8 only from the owner's actual answers. The first educational success is not “six files exist”; it is that the system elicits evidence, responds to that evidence honestly, and carries the result into the next learning decision without slowing Phase 39.
