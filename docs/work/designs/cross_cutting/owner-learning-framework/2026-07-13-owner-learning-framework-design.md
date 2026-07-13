---
status: active
purpose: design
created: 2026-07-13
milestone: cross-cutting
phase: cross-cutting
retirement_trigger: framework is either ratified into governance (AGENTS.md / rule file) and a living LEARN notebook is started, OR explicitly abandoned by the owner; this design draft is then consumed/retired.
---
****
# Owner Learning Framework — Design Draft (with Sample Lesson 0)

**Owner note (verbatim, 2026-07-11):** *"Add one important rule: think about how the agent
can teach me valuable things while doing this project. Now that all the frameworks specs are
done, all the basic infrastructure's design is set, how can you make me learn? I'm just a high
school student; most math, physics, PINN, engineering and scientific and technical aspects here
are things I have no way to understand... Now I have the intention to learn while having the
agents do all the real work... We just have to be very careful as to how the agent is going to
structure its teaching and response so that a high school student can understand."*

## What this document is

This is a **design draft**, not a ratified rule. It records (1) the agreed shape of a teaching
framework for the project owner, (2) the owner's calibrated learning baseline, and (3) **one
real sample lesson** so the owner can judge whether the lessons are *reachable* before we commit
the framework to governance and start the LEARN notebook.

The owner's go/no-go criterion is reachability: **can a high school student with the stated
baseline read the sample lesson and actually answer its three teach-back questions?** If yes, we
ratify. If no, we redesign informed by the owner's reaction.

---

## 1. Owner baseline (calibrated 2026-07-13)

The owner is a high school student entering college. Self-described as a project orchestrator
who lacks the scientific knowledge to verify the agents' work. Concrete baseline, gathered from
the owner's own textbooks and coursework:

| Domain | Level | Source | Note |
|---|---|---|---|
| Single-variable calculus | AP Calculus BC | Finney et al., *Calculus: Graphical, Numerical, Algebraic* 5e (calc-BC.md) | Chain rule §4.1, Taylor series Ch. 10 — seen, rusty |
| Multivariable calculus | Coursework | Stewart, *Multivariable Calculus* 7e (multivariable-calculus.md) | Partial derivatives §14.3, gradients §14.6, multiple integrals Ch. 15 — seen, rusty |
| Differential equations | Coursework | Zill, *A First Course in Differential Equations* 12e (Differential-equations.md) | ODE solution methods, Laplace transforms — seen, rusty |
| Statistics | AP Statistics | TPS 5e (AP-statistics.md) | Least-squares regression §3.2, probability rules Ch. 5 — seen, rusty |
| Physics | AP Physics C: Mechanics + E&M | College Board CED | **Includes gravitation and orbital motion as a unit.** Taken ~2 years ago, rusty |
| Programming | Object-oriented Python | Senior-year CS coursework (`Comp_Sci/code/`) | Classes, hash tables, merge/quick sort, stacks/queues — built working projects; rusty from disuse |

**Key calibration insight.** The gap is *not* missing prerequisites. The owner has seen the
chain rule, partial derivatives, gradients, least-squares, ODEs, and orbital mechanics. The gap
is the **bridge**: how those existing pieces turn into a neural network that learns physics. That
bridge is roughly six foundational rungs, not years of new prerequisites. The single best-fit
external resource at this exact level is **3Blue1Brown's "Neural Networks" series** (4 videos,
~19 min each), which assumes approximately AP Calculus + a little linear algebra — i.e., this
owner.

## 2. Framework shape (agreed in grill session, 2026-07-13)

Four decisions, each resolved:

- **Goal (Q1): working competence.** The owner can explain a piece back, spot a gross error,
  read a loss curve, reason about a design tradeoff. Not passive literacy (too low), not
  scientific judgment (multi-year, out of scope). Working competence is the on-ramp to judgment
  over many phases.
- **Artifacts (Q2): B + C.** (B) One growing **LEARN notebook** in the repo that accumulates one
  entry per phase — the concept, plain-language explanation, curated external resource, and
  three-tier teach-back. (C) A **teaching-protocol rule** (in `AGENTS.md` or a rule file) that
  makes every future agent teach the same calibrated way. A short pointer in each phase close-out
  directs the owner to the new entry.
- **Lesson selection (Q3): hybrid — mapped arc, emergent picks.** A lightweight curriculum map
  (drafted before lesson 1) gives the owner the visible arc; each phase the agent picks the
  concept that is *both* in the map *and* most alive in what just shipped, deferring the rest to
  later phases or to named walls.
- **Verification (Q4): three-tier teach-back, recorded.** Each entry ends with three questions
  (recall / explain / apply), answered in the owner's own words and recorded in the notebook.
  The agent never grades; the act of explaining is the check. Wrong answers are valuable — they
  show where the owner was.

### 2.1 Curriculum map (draft, to be refined before lesson 1)

The map below is the *intended* arc. The actual per-phase pick follows the hybrid rule (in map
AND most alive in what shipped). Phases are v2.0 (trainex) phases.

| Lesson | Concept | Builds on (owner's prior) | Rough phase |
|---|---|---|---|
| 0 | A neural network is stacked regression | AP Stats §3.2 least-squares | sample (this doc) |
| 1 | "Learning" = tuning numbers to reduce error, which is your least-squares idea generalized | Lesson 0 + Stats | 38 (model) |
| 2 | The tuning is your chain rule, done automatically — that's "autograd" | Calc BC §4.1 chain rule | 38 (model) |
| 3 | What the N-body problem actually is, and why it's hard | AP-C Mechanics gravitation unit | 39 (data) |
| 4 | Loss = the error number; you've met its simplest form (sum of squared residuals) | Stats + Lessons 0–2 | 40 (training) |
| 5 | What makes it "physics-informed" (the PINN idea: part of the loss enforces an ODE) | Diff eq + Lesson 4 | 40 (training) |
| 6 | How you can tell a trained model is wrong (loss curves, residuals) | All prior | 43 (verify) |

That is seven lessons across seven phases — one per phase, in dependency order.

## 3. Feasibility guarantees (the owner's core constraint)

The owner's stated constraint: the knowledge is advanced and beyond current expertise, so
lessons must be *feasible enough to understand and respond to*. Five conditions, enforced by the
teaching-protocol rule, guarantee this:

1. **First sentence hooks prior knowledge.** Every lesson opens by naming something the owner
   has already seen (in calc, stats, physics, or CS coursework), with a specific section
   reference where possible. The new idea is *one* step from that hook.
2. **One new idea per lesson.** Walls are named, not scaled (see §4).
3. **Every term defined twice** — plain language on first use, then its formal version — so the
   bridge builds both directions.
4. **One curated resource at the owner's level** (chosen, not a menu). The lesson is designed so
   the ~10-minute resource and the lesson cover the *same* idea; the owner is never asked to
   leap past the resource.
5. **The three-tier teach-back stays inside the lesson's four walls.** No question tests outside
   knowledge. This is the feasibility guarantee: if all three questions are answerable from the
   lesson + the curated resource, reachability is bounded by design.

## 4. Wall-naming (the "do not scale" section)

Every lesson includes a `### What we are NOT teaching this phase` section. The project contains
concepts that are genuine walls at this stage (SIREN activations, Jacobi coordinates, the
five-term loss catalog, the mass-weighted COM projection head, autograd internals). Each wall is
*named* in one sentence, with its importance stated, and the rung the owner would climb to reach
it eventually is pointed at. The owner's note asked the agent to "inspire me and encourage me to
learn, but figure out an effective way." Naming the wall and pointing at the door is that way;
teaching through the wall is not.

## 5. The three-tier teach-back (verification)

Per entry, three questions in escalating cognitive demand:

1. **Recall** — pull one key fact from memory. Low friction, reactivates the lesson.
2. **Explain in your own words** — the Feynman core; restate the lesson's central idea without
   jargon.
3. **Apply to this project** — a transfer question tied to what just shipped; predicts a small
   change or reasons about a design choice.

Plus two low-cost mechanics: **prediction-before-reveal** in the lesson body (the owner guesses
before the explanation lands — wrong guesses are the most valuable outcome), and **spaced
callbacks** (lesson *N+2* or *N+3* opens with a one-line reactivation of an earlier concept).

## 6. Visual emphasis convention (owner preference, 2026-07-13)

Lessons use a deliberate emphasis hierarchy so the owner's eye is drawn to what matters most.
Frequency decreases as emphasis weight increases — the strongest form is rare, reserved for the
single load-bearing clause of a step.

| Form | Markdown | Frequency | Use |
|---|---|---|---|
| **Most often** — key phrase | `<mark>...</mark>` highlight | Many per step | The phrases that carry the meaning; if the owner skims, these are the spine. |
| *Italic* — new term | `*...*` | First use of each term | Pairs with the "defined twice" rule; marks "you are meeting this word." |
| **Bold** — label/keyword | `**...**` | As needed | Section labels, the name of a new term once introduced, structural keywords. |
| **Highlight + underline** — the one load-bearing clause per step | `<mark><u>...</u></mark>` | At most once per step | The single sentence the owner must take away; everything else is context. |

`<mark>` renders as a yellow highlight in GitHub, VS Code, Obsidian, and Typora. `<u>` underline
works in the same renderers. Both are HTML inside Markdown, which is widely supported but not
strict CommonMark — acceptable here because the owner reads in renderers that support both.

Rules of thumb:
- **`<mark>` is the workhorse.** When in doubt, highlight rather than bold.
- **`<mark><u>` is the climax.** If a step has one sentence the owner should remember in six
  months, that sentence gets both. If a step has no clear climax, it is probably two steps.
- Do not stack all four forms on one clause. The hierarchy only works if each tier stays distinct.

### 6.1 Markdown syntax governance

**Canonical lesson reader: Obsidian or Typora** (owner decision, 2026-07-13). Both render
LaTeX math natively via built-in MathJax, so proper math typesetting is the standard — no
portable-Markdown workarounds, no Unicode-substitution tricks.

- **Math uses LaTeX delimiters.** Inline math: `$w$`, `$b$`, `$f(x)$`, `$w_1 x_1 + \dots + w_n x_n + b$`. Display math (standalone equations): `$$f(x) = wx + b$$` on its own line.
- **Do NOT use Unicode glyphs as math.** No `₁`, `ₙ`, `·`, `…` as substitutes for real math — they render in the prose font with wrong baseline alignment and look wrong. Use `$w_1$`, `$\cdot$`, `$\dots$`.
- **HTML emphasis tags (`<mark>`, `<u>`) are permitted** — both render correctly in Obsidian and Typora.
- **GitHub web / VS Code preview caveat:** `$...$` does NOT render in GitHub web or plain VS Code preview (it shows literal dollar signs). If a lesson must be read in those renderers, the equations would need a code-span fallback. The owner has chosen Obsidian/Typora as the canonical reader, so this caveat does not apply to lesson documents.

Teach-back answers (including wrong ones and missed predictions) are recorded in the LEARN
notebook and committed, not kept private. Wrong answers are the most valuable record: they show
where the owner was, and a future agent teaching the owner benefits from seeing prior
misconceptions.

---
---

# Sample Lesson 0 — A neural network is stacked regression

> This is a real lesson, written to the five feasibility conditions above. The owner's job: read
> it, watch the ~10-minute resource, and try the three teach-back questions. The framework is
> ratified only if this lesson is reachable.

**Builds on:** AP Statistics §3.2 (Least-Squares Regression). TPS 5e.
**New idea (one):** a neural network is a stack of tiny regressions, which makes the combined
function flexible enough to approximate almost any input→output relationship.
**Curated resource (one):** 3Blue1Brown, *"But what is a neural network?"* (Chapter 1 of the
neural-networks series, 19 min): https://www.3blue1brown.com/lessons/neural-networks
**Phase this lesson maps to:** 38 (model) — it is the foundation under the SQR-SkipResNet-SIREN
network Phase 38 builds.

## Prediction (guess before you read on)

In your stats class you fit a *line* to data by least-squares: you slid the line around until
the total squared error was as small as possible. That line could only represent straight-line
relationships.

**Before you read further — predict:** *how would you modify the "fit a function to data" idea
so the function could bend and curve to fit really complicated data, like the trajectory of three
gravitating stars?* Take a real guess (one sentence). Wrong guesses are the point.

> **Your prediction:** One way we can make this happen is by adding specific functions inside the function to modify components of it to make the graph change in a certain way we want at a very specific point. By continuously fitting this curve to the true curve we want to mimic, this can fit well. Functions that activate at a certain point can do this. 

## The lesson

### Step 1 — The thing you already own: least-squares regression

From AP Stats §3.2. You have a scatterplot of points. You want a function $f(x)$ that fits them.
You choose the simplest possible shape — a line:

$$f(x) = wx + b$$

Here $w$ is the slope and $b$ is the intercept. (In ML these get new names: $w$ is a **weight**
and $b$ is a **bias** — same objects, new vocabulary.) "Fitting" the line means choosing the
numbers $w$ and $b$ to <mark>minimize the total squared error across all data points</mark>. That is the
least-squares regression you did on your TI-84.

So you already understand the whole shape of machine learning at its smallest scale:

> *A model is a function with some tunable numbers. **Learning means choosing those numbers to
> make the function fit the data.***

That is the entire idea. Everything else — neural networks, deep learning, PINNs — is just a
more flexible choice of function $f$ and a more careful choice of "fit."

### Step 2 — One tiny generalization: the "neuron"

A line $wx + b$ takes one input. Real data has many inputs (the 14-number input vector in Phase
38, for example). The smallest generalization is:

$$\text{output} = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b$$

This is still least-squares regression — just with multiple inputs. With several inputs at once
this is called *multiple regression* (you may have seen it briefly in stats; if not, it is just
"a line with more than one input," which the equation above shows). In ML this whole expression
is one **neuron**: <mark>it takes $n$ inputs, multiplies each by its own tunable weight, adds a bias,
and produces one number</mark>. ML people often write this sum as a **dot product** of two *vectors* —
a list of inputs $[x_1, \dots, x_n]$ and a list of weights $[w_1, \dots, w_n]$. If "dot product"
or "vector" is rusty, the 3Blue1Brown video reviews them visually.

There is one extra ingredient. A raw $w_1 x_1 + \dots + b$ is still a *linear* function (strictly,
*affine* — the bias $b$ shifts the line off the origin, but it still can't bend), and stacking
such functions only ever gives you another flat function — no bending. So we pass the result
through a small nonlinear function (called an **activation** — often a squashing curve like in the
video; this project actually uses a sine wave, which is a later wall). You do not need to know
its shape yet; for now, read "activation" as "a little bend inserted after the regression."
<mark><u>That bend is what lets the network curve.</u></mark>

### Step 3 — The new idea: stack them

Here is the whole neural-network idea in one sentence:

> **A neural network is a stack of these little regressions, where each layer's outputs feed the
> next layer's inputs, so the combined function can bend enough to approximate almost anything.**

That is it. Layer 1 is a handful of parallel neurons (each a tiny multiple regression with a
bend). Layer 2 takes all of layer 1's outputs as its inputs. Layer 3 takes layer 2's outputs. The
final layer produces the answer. Phase 38's network is "<mark>14 inputs → 12 hidden layers of 256
neurons each → 9 outputs</mark>" (per the locked spec `pinn_architecture.md`): twelve stacked layers
of regression-with-bends, wide and deep enough to approximate the three-body trajectory function.

Why does stacking make it flexible? Each layer recomputes its inputs as a different mixture of
the previous layer's outputs. Compose enough mixtures-with-bends and the overall function can —
*in principle* — approximate essentially any smooth shape on a bounded region, including the curve
of three stars orbiting each other. (This is the **Universal Approximation Theorem**. A footnote
for later: it says the capacity *exists*, not that we can always *find* the right weights — that
capacity-vs-learnability distinction is exactly what Lessons 1 and 2 unpack.) This potential
flexibility is the core reason we use neural networks for hard functions instead of plain
regression.

### Step 4 — "Learning" is the same *goal* as least-squares — but a different *method*

"Training" the network = choosing *all* the weights and biases (Phase 38's network has on the
order of **600,000** of them) to minimize the total error across the training data. The *goal*
is the same as choosing the slope and intercept of a least-squares line. <mark><u>But the *method*
differs, and the difference matters.</u></mark> Your TI-84 solves the linear case **directly** — there
is a one-shot formula (the normal equations) that spits out the best slope and intercept
instantly. A neural network's bend makes the error a function with **no one-shot formula for its
minimum**, so the weights have to be **nudged iteratively** toward a smaller and smaller error.
That iterative nudging — called *gradient descent*, with the nudging done automatically by
*autograd* — is exactly what Lessons 1 and 2 unpack. For now, hold the corrected shape:

> *Training = error-minimization, like least-squares in its **goal**. But because the network's
> bend destroys the one-shot formula, the **method** is iterative nudging rather than a direct
> solve.*

### Step 5 — Why this matters for this project

Phase 38 builds the network whose shape you just learned. The three-body problem has no
closed-form solution in elementary functions — unlike the two-body problem (Keplerian orbits,
which you met in AP Physics C), <mark>you cannot write down $x(t)$, $y(t)$, $z(t)$ for three
gravitating stars</mark>. (Mathematicians have found infinite-series solutions — Sundman, 1912 —
but they converge so slowly they are useless in practice; that impracticality, not a total
absence of solutions, is why we resort to numerical integration or, here, a learned
approximation.) So instead of solving the equations directly, this project trains a neural
network to *approximate* the trajectory function. The network is the flexible function; physics
(Lessons 3 and 5) is what makes the approximation trustworthy rather than just curve-fitting.

## Curated resource (please watch, ~19 min)

Grant Sanderson (3Blue1Brown), *"But what is a neural network?"* — Chapter 1 of the
neural-networks series.
URL: https://www.3blue1brown.com/lessons/neural-networks
YouTube: https://www.youtube.com/watch?v=aircAruvnKk

Why this one: it assumes approximately your exact level (AP Calculus + a little linear algebra),
it builds the same "neuron = small regression, network = stack" picture visually, and the
handwritten-digit example is the cleanest first encounter with a real network. Lessons 1 and 2
will lean on Chapters 2 and 3 of the same series. The next chapters introduce the one piece this
lesson deliberately postponed: *how* the weights get tuned (gradient descent + backpropagation =
your chain rule).

## What we are NOT teaching this phase (walls)

These appear in Phase 38's spec. They are real, they matter, and you do **not** need them yet.
Each is named so you know it exists; the on-ramp is noted.

- **SIREN activation function.** A specific choice of the "bend" in Step 2 (a sine function
  instead of the usual squashing). Phase 38 uses it because sine's derivatives stay well-behaved,
  which matters for the physics residual in later lessons. *On-ramp: not needed until Lesson 5
  (PINN); for now "activation = a bend" is enough.*
- **SQR-SkipResNet architecture (skip connections, residual blocks).** A particular way of
  wiring the stack so very deep networks can still train. *On-ramp: Lesson 2, after you meet
  gradient descent — skip connections solve a problem you haven't met yet, so naming it now would
  be noise.*
- **The 14-dim input `[τ, IC₁₃]` and 9-dim output.** These are project-specific choices (one
  time + 13 initial-condition numbers in; 3 positions × 3 bodies out). *On-ramp: Lesson 3, when
  you meet the N-body problem — the input/output shapes will then make physical sense.*
- **Autograd / `torch.func` / Jacobians.** How the chain rule is applied automatically. *On-ramp:
  Lesson 2 — this is literally your Calc BC chain rule, mechanized. Do not chase it now.*

## Teach-back (three questions)

Answer in your own words, in this document beneath each question. The agent does not grade.
Wrong answers are useful — record them honestly.

### Q1 — Recall
Name, in your own words, the operations a neuron performs on its inputs, in order — and say
which one is responsible for letting the network bend.

> **Your answer:** uses the input, multiples by the weight and adds the bias, and produces the output

### Q2 — Explain
A classmate who has not seen this lesson asks you: "I did least-squares regression in stats. What
is a neural network, compared to that?" Answer in 2–3 sentences. Do not use the words "gradient"
or "backpropagation" (you haven't met them yet — that is deliberate).

> **Your answer:** A neural network is doing something very similar to LSR. It's aimed at minimizing loss, or a loss function that we want to define. The ultimate goal is to think of it as to "fit" something genuinely and universally true so that we can continue improving our model/function to fit that grdoung-truth. And the way we achieve that is by choosing the parameters' values inside the neural network, like how you adjust the slope and y-intercept in the linear equation for a function. 

### Q3 — Apply to this project
Phase 38's network has **12 hidden layers** of 256 neurons each. Suppose someone proposed
instead: one hidden layer of 10 neurons. Without knowing any ML theory beyond this lesson,
reason about the tradeoff — what would the smaller network likely be worse at, and why? (Hint:
think about Step 3, "stacking makes it flexible.")

> **Your answer:** more neurons and more layers give more curated and accurate final answer because more fitting was executed during each layer. With more neuron stacked within one layer, we gain a little bit of flexibility in tuning the specifc numbers: the more weights and biases we can tune and change, the more accurate we can make the fit to be. Now scale that one layer to many more layers, we gain even more accuracy. But what's the tradeoff? Is the accuracy simply going to increase infinitely without bound? I don't think so.

---

## Owner go/no-go (to fill in after reading)

- [ ] I could read the lesson without getting lost. Where I lost the thread (if anywhere):
  _
- [ ] I watched the 3Blue1Brown chapter and it covered the same idea.
- [ ] I could attempt all three teach-back questions using only the lesson + the video.
- [ ] The "walls" section felt like honest signposting, not noise.

**Verdict:** _ GO (the framework is feasible — ratify into governance and start the LEARN
notebook) / NO-GO (redesign needed — what specifically was unreachable: _ )

---

## Adversarial review log (Step C of the accuracy pipeline)

**Reviewer:** fresh adversarial subagent (no drafting involvement), 2026-07-13.
**Scope:** Sample Lesson 0 only.
**Verdict:** FIXABLE-IN-PASS — 1 CRITICAL (1 root cause appearing twice), 4 MAJOR, 5 MINOR.

All findings below were applied as surgical edits to this document before the owner's GO/NO-GO
decision. This log records what was found and fixed, in the spirit of transparency over the
appearance of infallibility.

| ID | Sev | Finding | Resolution |
|---|---|---|---|
| F1 | CRITICAL | Lesson said Phase 38's network has **3** hidden layers; locked spec `pinn_architecture.md` Table 2 says **12** (6 SQR-SkipResNet blocks × 2). A factual error about the owner's own project. | Fixed in Step 3 and Q3: corrected to 12 hidden layers. |
| F2 | MAJOR | "Tens of thousands" of parameters understates; true count ~661,000 for the 12×256 architecture. | Fixed in Step 4: "on the order of 600,000." |
| F3 | MAJOR | "No closed-form solution" for the three-body problem is technically false (Sundman 1912 gave a convergent series; it is just impractically slow). | Fixed in Step 5: qualified to "no closed-form solution in elementary functions," with the Sundman note. |
| F4 | MAJOR | Universality claim overstated: dropped the "continuous on a bounded domain" qualifier and presented capacity as learnability (the classic beginner misconception). | Fixed in Step 3: added "in principle," named the Universal Approximation Theorem, and deferred the capacity-vs-learnability distinction to Lessons 1–2. |
| F5 | MAJOR | "Training is the same action as least-squares" hid the closed-form-vs-iterative distinction. The owner's own Q2 answer showed this slip already happening. | Fixed in Step 4: separated *goal* (same: minimize error) from *method* (different: one-shot formula vs. iterative nudging). |
| F6 | MINOR | "Linear" used where "affine" is meant. | Fixed in Step 2: parenthetical "(strictly, affine)". |
| F7 | MINOR | "Multiple regression" hook may exceed AP Stats coverage (TPS 5e §3.2 is simple regression). | Fixed in Step 2: softened to "you may have seen it briefly; if not, it is just 'a line with more than one input.'" |
| F8 | MINOR | Dot products / vectors used implicitly but never anchored; the 3B1B video leans on them. | Fixed in Step 2: one sentence naming dot product + vector, pointing to the video's visual review. |
| F9 | MINOR | "Squashing function" inconsistent with this project's SIREN/sine activation (sine is not squashing). | Fixed in Step 2: generalized to "nonlinear function" with the squashing/sine distinction noted as a wall. |
| Q1 | MINOR | Q1 phrasing let the owner skip the activation in their answer (the load-bearing ingredient). | Fixed: Q1 now asks which operation lets the network bend. |
| Q3 | — | Q3 inherited the F1 layer-count error. | Fixed with F1. |

**What this review validated.** The conceptual spine of the lesson was sound — no finding
required restructuring. The pipeline caught one factual error about the owner's own project
before it could be committed to memory, plus four wording qualifications that would mislead a
careful reader. This is the system working as designed on its first run.

