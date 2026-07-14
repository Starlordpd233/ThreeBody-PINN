---
status: active
purpose: design
created: 2026-07-13
updated: 2026-07-14
milestone: cross-cutting
phase: cross-cutting
retirement_trigger: revised framework is ratified into governance and absorbed into the independent learning workspace, or explicitly abandoned by the owner
---
****
# Owner Learning Framework — Revised Design (with Sample Orientation 0)

**Owner note (verbatim, 2026-07-11):** *"Add one important rule: think about how the agent
can teach me valuable things while doing this project. Now that all the frameworks specs are
done, all the basic infrastructure's design is set, how can you make me learn? I'm just a high
school student; most math, physics, PINN, engineering and scientific and technical aspects here
are things I have no way to understand... Now I have the intention to learn while having the
agents do all the real work... We just have to be very careful as to how the agent is going to
structure its teaching and response so that a high school student can understand."*

## What this document is

This is the revised design for an **independent owner-learning system**. It records the owner's
learning mission, the distinction between fast project execution and durable learning, the
contracts for orientation and deep learning, and one sample orientation that proved the material
can be made reachable.

The design was revised after the first sample exposed two truths:

1. Project work advances too quickly for one lesson per GSD phase to be a useful cadence.
2. A broad introductory lesson can be valuable without being the depth standard for real
   learning.

The framework therefore separates **work progress** from **learning progress**. GSD phases may
suggest useful topics, but they do not schedule lessons, determine prerequisites, or wait for the
owner to complete a learning unit.

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

## 2. Two independent tracks

### 2.1 Work track

The work track contains GSD phases, implementation, research adjudication, verification, and
shipping. It moves at the pace required by the project. Learning is never a prerequisite for
starting or closing a work phase unless the owner explicitly makes one particular decision a
learning gate.

At a useful work boundary, an agent may add a **topic nomination** to the learning queue. A
nomination is only a pointer: “this concept became concrete in the work.” It does not create a
lesson automatically and does not outrank prerequisites, a misconception that needs repair, or a
review that is already due.

### 2.2 Learning track

The learning track has its own mission, curriculum, active unit, and review schedule. Its pace is
set by:

1. prerequisite order;
2. the owner's stated interests and available time;
3. misconceptions revealed by prior attempts;
4. concepts due for retrieval practice; and
5. usefulness toward the owner's working-competence goal.

Current project work is a rich source of examples, but **work relevance is a tie-breaker, not the
clock**.

## 3. Learning goal: useful working competence

The goal remains **working competence**. The owner should increasingly be able to:

- explain an important mechanism without relying on agent wording;
- perform a small derivation, calculation, inspection, or debugging move;
- distinguish a plausible claim from a grossly incorrect one;
- interpret project evidence such as a loss curve, residual, data split, or validation result;
  and
- reason about a bounded design tradeoff while clearly naming what remains unknown.

Coverage is not learning. Reading a lesson changes a concept's state to **introduced**, not
learned. A concept becomes **demonstrated** only after a correct explanation or application, and
**retained** only after successful delayed retrieval.

## 4. Two teaching formats

### 4.1 Orientation

An orientation creates a map of unfamiliar territory. It may introduce several concepts at a
very shallow level so the owner can see how they relate, recognize the vocabulary, and choose
where to go deeper.

An orientation:

- may contain several new ideas;
- explicitly marks every explanation as introductory;
- makes no mastery or depth claim;
- ends with questions that reveal interest and misconceptions; and
- normally takes about 15–30 minutes, including one curated resource.

Sample Lesson 0 is an orientation. Its breadth is intentional and acceptable. It is not the
template for the depth of later units.

### 4.2 Deep learning unit

A deep unit develops **one useful capability**, not necessarily one vocabulary term. Several
supporting concepts may appear when they are necessary to build that capability. A difficult
capability may span multiple short sessions rather than being compressed into one oversized
lesson.

Examples of valid capability targets:

- derive one gradient update from the chain rule and explain what autograd records;
- inspect a train/validation split and detect trajectory leakage;
- derive a PINN residual from one second-order ODE;
- compare underfitting, overfitting, and optimization failure using evidence; or
- read a five-term loss report and identify which physical constraint is failing.

“Know what autograd is” is too shallow. “Understand neural networks” is too broad. A capability
must end in something observable that the owner can do.

Provisional timeboxes keep the system usable without sacrificing depth:

- **acquisition session:** roughly 25–45 minutes;
- **practice or correction session:** roughly 10–20 minutes;
- **spaced review:** roughly 5–10 minutes.

These are defaults, not quotas. When depth needs more time, split the unit at a meaningful
capability boundary.

## 5. Selecting what to learn next

The curriculum is a dependency map plus a small priority queue, not a copy of the GSD roadmap.
Before starting a unit, the agent recommends one next capability and explains why it is ready.
The owner may choose another topic.

Priority order:

1. repair an important active misconception;
2. complete a prerequisite for the current learning goal;
3. perform a due retrieval review;
4. pursue the owner's current question or curiosity;
5. use a newly concrete project example; and
6. explore an optional adjacent topic.

The initial candidate sequence after Orientation 0 is deliberately provisional:

1. **Capacity is not accuracy:** distinguish representation, optimization, and generalization.
2. **Gradient descent and autograd:** connect iterative fitting to the chain rule.
3. **Three-body state and scaling:** turn positions, masses, initial conditions, and time into a
   model input/output contract.
4. **Physics residuals:** derive how an ODE becomes a PINN loss term.
5. **Training evidence:** distinguish loss reduction, overfitting, physical validity, and held-out
   performance.
6. **Curriculum and reproducibility:** understand stages, checkpoints, recovery, and why a run can
   or cannot be trusted.

This sequence may change when learning records show a different prerequisite or the owner chooses
a different goal. No item is assigned to a phase number.

## 6. Deep-unit contract

Every deep unit must include:

1. **Capability target** — one sentence describing what the owner will be able to do.
2. **Prior-knowledge bridge** — the exact calculus, statistics, physics, programming, or earlier
   learning concept being reused.
3. **Source grounding** — at least one high-trust primary or authoritative source; project-specific
   claims cite the authoritative spec or recorded evidence.
4. **Explanation in layers** — intuition first, then the formal statement, then a worked example.
5. **Guided practice** — one partially scaffolded example with immediate feedback.
6. **Independent attempt** — recall, explanation, and application without copying lesson wording.
7. **Diagnostic feedback and corrected re-attempt** — the loop in §7.
8. **Transfer** — one small project or novel example that differs from the worked example.
9. **Review hook** — a compact prompt scheduled for later retrieval.
10. **Named walls** — adjacent ideas that are intentionally deferred and why.

The old “one new idea per lesson” rule is retired. The replacement is stricter where it matters:
**one useful capability per deep unit, with only the supporting concepts needed to acquire it**.

## 7. Feedback, correction, and retention

Teach-back remains low-stakes, but it is no longer feedback-free. The agent does not assign a
number or letter grade. It must diagnose the attempt accurately.

For each independent response, the agent:

1. preserves the owner's original answer verbatim;
2. identifies what is correct;
3. classifies the remainder as incomplete, imprecise, or a misconception;
4. explains the smallest correction needed, preferably with a counterexample;
5. asks for one corrected re-attempt in the owner's own words; and
6. records what future teaching should assume only after the correction is demonstrated.

The original answer is never overwritten. A learning record may state that a misconception was
corrected only after the re-attempt supplies evidence.

Retrieval is scheduled by learning time, not work time:

- a short reactivation at the next learning session;
- an application or contrast question after at least one later session; and
- a longer-delay check when the concept becomes a prerequisite or after roughly one to four
  weeks.

Exact intervals are adjusted from observed difficulty. A failed delayed retrieval returns the
concept to **practicing**; it is useful evidence, not failure of the learner.

## 8. Learning workspace and records

The implemented framework should live in a bounded `learning/` workspace, separate from GSD and
framework-spec artifacts:

```text
learning/
  MISSION.md             # why the owner is learning and observable success criteria
  CURRICULUM.md          # dependency map, queue, active unit, and due reviews
  RESOURCES.md           # small annotated set of trusted sources
  NOTES.md               # stable teaching preferences and constraints
  lessons/               # orientations and deep units, numbered independently of phases
  learning-records/      # demonstrated understanding and corrected misconceptions only
  reference/             # compressed glossaries, derivations, and checklists
```

Markdown remains canonical because the owner reads in Obsidian or Typora. Interactive HTML may be
added when it materially improves practice, but it is not required for ordinary lessons.

The workspace deliberately avoids one ever-growing LEARN notebook. Lessons hold the teaching and
the full attempt/feedback trail; learning records stay compact and record only durable changes in
what future sessions may assume.

## 9. Accuracy and source-grounding pipeline

The first sample's adversarial review caught real errors, but requiring a separate reviewer for
every small lesson would slow the system unnecessarily. Review depth is risk-based.

Every lesson receives:

1. **source pass** — factual claims checked against the annotated resource set;
2. **project-truth pass** — project-specific claims checked against authoritative specs, evidence,
   or current implementation as appropriate;
3. **pedagogy pass** — capability, prerequisite, depth, walls, and likely misconceptions checked;
4. **answer-key pass** — prompts tested against explicit expected reasoning before the owner sees
   them; and
5. **correction log** — any post-release correction recorded without silently rewriting the
   learner's historical attempt.

Use an independent adversarial review when the unit is mathematically subtle, scientifically
contested, safety-sensitive, or foundational enough that a misconception would contaminate later
units. Routine reviews need not pay that cost.

If a prompt changes after the owner answered it, the old prompt remains attached to the old
answer and the revised prompt requires a fresh attempt.

## 10. Visual emphasis convention (owner preference, 2026-07-13)

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

### 10.1 Markdown syntax governance

**Canonical lesson reader: Obsidian or Typora** (owner decision, 2026-07-13). Both render
LaTeX math natively via built-in MathJax, so proper math typesetting is the standard — no
portable-Markdown workarounds, no Unicode-substitution tricks.

- **Math uses LaTeX delimiters.** Inline math: `$w$`, `$b$`, `$f(x)$`, `$w_1 x_1 + \dots + w_n x_n + b$`. Display math (standalone equations): `$$f(x) = wx + b$$` on its own line.
- **Do NOT use Unicode glyphs as math.** No `₁`, `ₙ`, `·`, `…` as substitutes for real math — they render in the prose font with wrong baseline alignment and look wrong. Use `$w_1$`, `$\cdot$`, `$\dots$`.
- **HTML emphasis tags (`<mark>`, `<u>`) are permitted** — both render correctly in Obsidian and Typora.
- **GitHub web / VS Code preview caveat:** `$...$` does NOT render in GitHub web or plain VS Code preview (it shows literal dollar signs). If a lesson must be read in those renderers, the equations would need a code-span fallback. The owner has chosen Obsidian/Typora as the canonical reader, so this caveat does not apply to lesson documents.

Teach-back answers, feedback, and corrected re-attempts are recorded in the relevant lesson file.
Compact learning records are written only when the owner demonstrates non-trivial understanding,
corrects a misconception, establishes meaningful prior knowledge, or changes the mission.

## 11. Evidence behind the learning mechanics

The framework's learning claims are grounded in a small set of high-trust sources:

- [Chi et al. (1989), “Self-Explanations”](https://doi.org/10.1207/s15516709cog1302_1) — supports
  asking the learner to explain mechanisms and monitor gaps rather than only reread explanations.
- [Karpicke and Blunt (2011), “Retrieval Practice Produces More Learning”](https://doi.org/10.1126/science.1199327)
  — supports independent retrieval and transfer questions rather than familiarity checks alone.
- [Butler and Roediger (2008), corrective feedback after testing](https://pubmed.ncbi.nlm.nih.gov/18491500/)
  — supports diagnosing and correcting errors rather than merely preserving an attempt.
- [Cepeda et al. (2006), distributed-practice synthesis](https://doi.org/10.1037/0033-2909.132.3.354)
  — supports revisiting concepts after delay instead of treating immediate fluency as retention.
- [U.S. Institute of Education Sciences practice guide](https://ies.ed.gov/ncee/wwc/practiceguide/1)
  — integrates retrieval, deep explanatory questions, spacing, worked examples, and monitoring of
  what is and is not yet known.

---
---

# Sample Orientation 0 — A neural network grows from the regression idea

> This is a real **orientation**, preserved as the reachability prototype that motivated the
> revised framework. It intentionally introduces several ideas at shallow depth. Its job is to
> provide a map and expose promising directions or misconceptions—not to demonstrate deep
> learning or ratify the complete learning system.

**Builds on:** AP Statistics §3.2 (Least-Squares Regression). TPS 5e.
**Orientation map:** a neural network generalizes the tunable-function idea from regression by
composing affine transformations with nonlinear activations and tuning the whole composition
together.
**Curated resource (one):** 3Blue1Brown, *"But what is a neural network?"* (Chapter 1 of the
neural-networks series, 19 min): https://www.3blue1brown.com/lessons/neural-networks
**Project anchor:** the SQR-SkipResNet-SIREN model built during Phase 38 supplies a concrete
example, but the orientation is not scheduled by or owned by that phase.

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

So you already understand one important starting point for machine learning:

> *A model is a function with some tunable numbers. **Learning means choosing those numbers to
> reduce a defined objective.***

In least-squares regression, that objective measures data fit. Neural networks use more flexible
functions, and PINNs use objectives that can combine data fit with physical constraints. The
deeper questions—what the objective guarantees, how the parameters are adjusted, and whether the
result generalizes—belong to later deep units.

### Step 2 — One tiny generalization: the "neuron"

A line $wx + b$ takes one input. Real data has many inputs (the 14-number input vector in Phase
38, for example). The smallest generalization is:

$$\text{output} = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b$$

This has the same affine form used by multiple regression, just with several inputs. (You may
have seen multiple regression briefly in stats; if not, it is “a line with more than one input,”
which the equation above shows.) In ML this expression is the **pre-activation** part of one
**neuron**: <mark>it takes $n$ inputs, multiplies each by its own tunable weight, adds a bias, and
produces one number</mark>. ML people often write this sum as a **dot product** of two *vectors* —
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

> **A neural network composes layers of affine transformations and nonlinear activations, where
> each layer's outputs feed the next layer's inputs and the whole composition is trained
> together.**

Layer 1 is a handful of parallel neurons (each an affine calculation followed by a nonlinear
activation). Layer 2 takes all of layer 1's outputs as its inputs. Layer 3 takes layer 2's outputs.
The final layer produces the answer. <mark>No layer performs its own separate fit to the target;
the parameters across all layers are adjusted jointly by one training objective.</mark> Phase 38's
network is "<mark>14 inputs → 12 hidden layers of 256 neurons each → 9 outputs</mark>" (per the
locked spec `pinn_architecture.md`): twelve stacked layers of affine transformations and
activations, designed with enough capacity to approximate the three-body trajectory function.

Why does stacking make it flexible? Each layer recomputes its inputs as a different mixture of
the previous layer's outputs. Compose enough mixtures-with-bends and the overall function can —
*in principle* — approximate essentially any smooth shape on a bounded region, including the curve
of three stars orbiting each other. (This is the **Universal Approximation Theorem**. A footnote
for later: it says the capacity *exists*, not that we can always *find* the right weights or that
the fitted model will generalize — the capacity-vs-optimization-vs-generalization distinction is
the first recommended deep unit.) This potential flexibility is the core reason we use neural
networks for hard functions instead of plain regression. More depth or width can increase
capacity, but it does not guarantee better accuracy.

### Step 4 — "Learning" is the same *goal* as least-squares — but a different *method*

"Training" the network = choosing *all* the weights and biases jointly (Phase 38's network has on the
order of **600,000** of them) to minimize the total error across the training data. The *goal*
is the same as choosing the slope and intercept of a least-squares line. <mark><u>But the *method*
differs, and the difference matters.</u></mark> Your TI-84 solves the linear case **directly** — there
is a one-shot formula (the normal equations) that spits out the best slope and intercept
instantly. A neural network's bend makes the error a function with **no one-shot formula for its
minimum**, so the weights have to be **nudged iteratively** toward a smaller and smaller error.
That iterative nudging — called *gradient descent*, with derivatives supplied automatically by
*autograd* — is a later deep-learning sequence. For now, hold the corrected shape:

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
network to *approximate* the trajectory function. The network is the flexible function; later
deep units examine how physics constraints help and what evidence is still required before the
approximation can be trusted.

## Curated resource (please watch, ~19 min)

Grant Sanderson (3Blue1Brown), *"But what is a neural network?"* — Chapter 1 of the
neural-networks series.
URL: https://www.3blue1brown.com/lessons/neural-networks
YouTube: https://www.youtube.com/watch?v=aircAruvnKk

Why this one: it assumes approximately your exact level (AP Calculus + a little linear algebra),
visually connects simple neurons into a network, and uses handwritten digits as a clean first
encounter with a real model. Later deep units may use Chapters 2 and 3 when they teach how the
weights are tuned through gradient descent and backpropagation.

## What we are NOT teaching in this orientation (walls)

These appear in Phase 38's spec. They are real, they matter, and you do **not** need them yet.
Each is named so you know it exists; the on-ramp is noted.

- **SIREN activation function.** A specific choice of the "bend" in Step 2 (a sine function
  instead of the usual squashing). Its smooth derivatives matter when a PINN differentiates the
  network output. *On-ramp: a later deep unit on activations and physics residuals; for now
  "activation adds nonlinearity" is enough.*
- **SQR-SkipResNet architecture (skip connections, residual blocks).** A particular way of
  wiring the stack so very deep networks can still train. *On-ramp: after the deep unit on
  gradient descent; skip connections solve a problem you have not yet studied.*
- **The 14-dim input `[τ, IC₁₃]` and 9-dim output.** These are project-specific choices (one
  time + 13 initial-condition numbers in; 3 positions × 3 bodies out). *On-ramp: the deep unit
  on three-body state and scaling.*
- **Autograd / `torch.func` / Jacobians.** How the chain rule is applied automatically. *On-ramp:
  the gradient-descent and autograd sequence—your Calc BC chain rule, mechanized.*

## Orientation teach-back and diagnostic follow-up

These answers were captured under the original feedback-free protocol. The 2026-07-14 revision
preserves them and adds the diagnostic feedback that should have followed. Corrected re-attempts
remain optional until the owner resumes this learning track; they do not block project work.

### Q1 — Recall
Name, in your own words, the operations a neuron performs on its inputs, in order — and say
which one is responsible for letting the network bend.

> **Your answer:** uses the input, multiples by the weight and adds the bias, and produces the output

> **Diagnostic feedback (2026-07-14):** Incomplete. You correctly named the weighted combination
> and bias. The missing operation is the nonlinear activation applied afterward; that activation
> is what prevents a stack of affine transformations from collapsing into another affine
> transformation. The wording of Q1 was strengthened after your original answer, so the revised
> prompt requires a fresh attempt rather than being judged retroactively.
>
> **Corrected re-attempt:** _pending when this learning track resumes_

### Q2 — Explain
A classmate who has not seen this lesson asks you: "I did least-squares regression in stats. What
is a neural network, compared to that?" Answer in 2–3 sentences. Do not use the words "gradient"
or "backpropagation" (you haven't met them yet — that is deliberate).

> **Your answer:** A neural network is doing something very similar to LSR. It's aimed at minimizing loss, or a loss function that we want to define. The ultimate goal is to think of it as to "fit" something genuinely and universally true so that we can continue improving our model/function to fit that grdoung-truth. And the way we achieve that is by choosing the parameters' values inside the neural network, like how you adjust the slope and y-intercept in the linear equation for a function.

> **Diagnostic feedback (2026-07-14):** Partly correct. The parameter-tuning analogy and the
> objective-minimization goal are good. The phrase “genuinely and universally true” is the key
> misconception: minimizing a chosen objective does not guarantee truth or generalization. A
> network may fit the training evidence and still fail on unseen cases or violate important
> physics. Its layers are also tuned jointly, not as separate regressions.
>
> **Corrected re-attempt:** _pending when this learning track resumes_

### Q3 — Apply to this project
Phase 38's network has **12 hidden layers** of 256 neurons each. Suppose someone proposed
instead: one hidden layer of 10 neurons. Without knowing any ML theory beyond this lesson,
reason about the tradeoff — what would the smaller network likely be worse at, and why? (Hint:
think about Step 3, "stacking makes it flexible.")

> **Your answer:** more neurons and more layers give more curated and accurate final answer because more fitting was executed during each layer. With more neuron stacked within one layer, we gain a little bit of flexibility in tuning the specifc numbers: the more weights and biases we can tune and change, the more accurate we can make the fit to be. Now scale that one layer to many more layers, we gain even more accuracy. But what's the tradeoff? Is the accuracy simply going to increase infinitely without bound? I don't think so.

> **Diagnostic feedback (2026-07-14):** Partly correct. You correctly identified that more
> parameters can provide more representational capacity, and you correctly doubted that accuracy
> rises without bound. The correction is that each layer does not perform another fit. All layers
> form one function and are optimized together. A tiny network may underfit a complex trajectory;
> a larger network may represent it better, but can also cost more, optimize poorly, or overfit.
> Capacity is therefore not the same as achieved accuracy.
>
> **Corrected re-attempt:** _pending when this learning track resumes_

---

## Orientation verdict and framework status

**Orientation reachability: GO.** On 2026-07-14 the owner clarified that the amount and breadth
of content in this sample are acceptable because every idea is introduced only at a very shallow
level. This validates orientation as a format.

**Depth verdict: not applicable.** The sample was not intended to represent the depth of real
learning. Actual learning must go far enough to produce useful understanding and retention,
which is now the purpose of deep units.

**Framework status: revised design, active.** Reachability of one orientation does not by itself
validate diagnostic feedback, transfer, or delayed retention. Those mechanisms must be exercised
when the independent learning workspace begins.

---

## Historical adversarial content-review log (2026-07-13)

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
| F4 | MAJOR | Universality claim overstated: dropped the "continuous on a bounded domain" qualifier and presented capacity as learnability (the classic beginner misconception). | Fixed in Step 3: added "in principle," named the Universal Approximation Theorem, and routed capacity vs optimization vs generalization to the first recommended deep unit. |
| F5 | MAJOR | "Training is the same action as least-squares" hid the closed-form-vs-iterative distinction. The owner's own Q2 answer showed this slip already happening. | Fixed in Step 4: separated *goal* (same: minimize error) from *method* (different: one-shot formula vs. iterative nudging). |
| F6 | MINOR | "Linear" used where "affine" is meant. | Fixed in Step 2: parenthetical "(strictly, affine)". |
| F7 | MINOR | "Multiple regression" hook may exceed AP Stats coverage (TPS 5e §3.2 is simple regression). | Fixed in Step 2: softened to "you may have seen it briefly; if not, it is just 'a line with more than one input.'" |
| F8 | MINOR | Dot products / vectors used implicitly but never anchored; the 3B1B video leans on them. | Fixed in Step 2: one sentence naming dot product + vector, pointing to the video's visual review. |
| F9 | MINOR | "Squashing function" inconsistent with this project's SIREN/sine activation (sine is not squashing). | Fixed in Step 2: generalized to "nonlinear function" with the squashing/sine distinction noted as a wall. |
| Q1 | MINOR | Q1 phrasing let the owner skip the activation in their answer (the load-bearing ingredient). | The prompt was strengthened, but the original response was not re-attempted. The revised framework now preserves the mismatch and requires a fresh attempt. |
| Q3 | — | Q3 inherited the F1 layer-count error. | Fixed with F1. |

**What this review validated.** Independent content review was valuable: it caught one factual
error about the owner's own project and several misleading qualifications. It did **not** validate
the learning system, and the missing feedback/re-attempt after Q1 is evidence for the revised
contract in §7 and §9.
