---
lesson_id: "0001"
title: Capacity is not accuracy
format: deep-unit
capability_state: introduced
created: 2026-07-14
source_design: docs/work/designs/cross_cutting/owner-learning-framework/2026-07-13-owner-learning-framework-design.md
---

# Unit 0001 — Capacity is not accuracy

**Expected acquisition time:** 25–45 minutes, plus your independent response.

**Capability target:** Given observations about a model, distinguish evidence about representation, optimization, and generalization—and state what the evidence still does not establish.

> In this title, “accuracy” means achieved model performance in ordinary language. This project predicts continuous trajectories, so the precise terms in the unit are *training loss*, *held-out performance*, and *physical consistency*.

## Cold retrieval — answer before reading on

These two prompts reactivate Orientation 0. Answer from memory before continuing; your answers are diagnostic and will be preserved.

1. Without reopening Orientation 0: after a neuron forms its weighted sum and adds its bias, what operation comes next, and why does it matter?
2. In Orientation 0 you wrote that more layers “give more accuracy because more fitting is executed during each layer.” From memory now — name **one thing** a larger network definitely provides, and **one thing** it does **not** by itself guarantee.

Commit to an answer for both before reading on. These are diagnostic predictions, not a test you can fail: the value is in committing first, then comparing your prediction to the formal statement as you read §2–§3. Your exact wording will be preserved either way.

## 1. The intuition, then retire it

Suppose you face a mechanical job. Three very different facts matter:

- **The toolbox** — does it even contain a tool capable of this job?
- **Your ability to pick the right tool and use it well** — given the toolbox, do you actually select and drive the right tool?
- **Success on a new job** — when the next job is slightly different, does the work still hold?

Map these to three separate questions about a neural network:

- **Representation** — is the model class rich enough, relative to *this* target, to contain a function capable of the required mapping?
- **Optimization** — did the training process find a sufficiently good member of that class?
- **Generalization** — does the fitted function work on relevant cases that did not determine its parameters?

The toolbox analogy gets you to the shape of the distinction. Then retire it. Networks are not toolboxes, training is not a mechanic, and stretching the picture will start to mislead. Keep the three questions; drop the analogy.

## 2. The formal statement

Let a model class be a set of candidate functions

$$\mathcal{F} = \{f_\theta\}$$

indexed by parameters $\theta$. Training selects one fitted member $f_{\hat\theta} \in \mathcal{F}$ by adjusting **all** parameters $\theta$ jointly under one objective — no layer is fitted separately; the whole network is one composed function whose every weight and bias is tuned together. Define:

- training loss $L_{\mathrm{train}}(f)$ — average error over the examples whose parameters the fit was allowed to see;
- unseen / validation loss $L_{\mathrm{unseen}}(f)$ — average error over relevant examples that did *not* choose $\hat\theta$.

Now the three questions become precise:

- **Capacity** describes the richness of the class $\mathcal{F}$. The target-relative **representation** question asks whether a sufficiently good function for *this* task exists *somewhere* in $\mathcal{F}$.
- **Optimization** asks whether the training procedure finds useful parameters $\hat\theta$ — a good-enough member of the class, not just any member.
- **Generalization** asks how $f_{\hat\theta}$ behaves on relevant evidence that did *not* choose $\hat\theta$.

## 3. A logical gate, not an additive decomposition

It is tempting to write something like “total error = representation error + optimization error + generalization error.” Resist that. The three are not independent additive pieces. They are a sequence of gating questions:

```text
good-enough function exists in the model class?
                  ↓
training finds a good-enough member of that class?
                  ↓
fitted member works on relevant unseen cases?
```

Each question only becomes informative once the previous one is at least approximately satisfied. If no good function exists in the class, asking whether training “found the optimum” is beside the point. If training never fit the seen examples, held-out performance is not yet the right thing to measure.

<mark><u>Increasing capacity changes what the model class *could* represent; it does not by itself choose good parameters or supply unseen evidence.</u></mark>

That single sentence is the load-bearing claim of this unit.

## 4. A complete algebraic example: when the class cannot represent the target

Take the target $y = x^2$ sampled at three points: $x \in \{-1, 0, 1\}$, so $y \in \{1, 0, 1\}$.

Try to fit these points with an affine model $f(x) = wx + b$. Matching the two outer points requires:

$$
-w + b = 1, \qquad w + b = 1
$$

Add the two equations: $2b = 2$, so $b = 1$. Subtract the first from the second: $2w = 0$, so $w = 0$. The affine fit is forced to be $f(x) = 1$ everywhere, which gives $f(0) = 1$. But the target requires $f(0) = 0$.

Therefore **no parameter choice in the affine class** can fit all three points. This is a *representational* limitation of the class $\{wx + b\}$ on this target, not a statement about how hard the class is to optimize.

A richer class that contains $f(x) = x^2$ — for instance quadratics $ax^2 + bx + c$ — removes this limitation: $a=1, b=0, c=0$ fits all three points exactly.

Two walls around this example:

- This proves a limitation of *this affine class* on *these points*. It is not a universal diagnostic procedure that you can run on every neural network.
- A richer class makes a correct fit *possible*, not *inevitable*. Knowing the class contains a good function says nothing about whether training finds it.

## 5. Optimization and generalization counterexamples

**Optimization contrast.** Same architecture, same training data, same objective. Two runs (different initialization, different learning-rate schedule, or different optimizer) end at very different training losses — one a hundred times lower than the other. The high-loss run is evidence of an *optimization* problem, because the better run demonstrates that *the same class can fit the training objective more closely*. Note we are not claiming random seeds are the only possible cause; any controlled change to the training procedure that leaves the class fixed is a valid contrast.

**Generalization contrast.** A fitted model reaches very low training loss while held-out loss stays high or keeps rising across several evaluations. Improvement on seen evidence accompanied by deterioration on unseen evidence is evidence of a *generalization gap*. It is not evidence that “another layer would fix it” — another layer is a statement about capacity, which is a different question.

**Empirical counterexample (Zhang et al., 2017).** In their experiments, high-capacity networks could fit *randomly assigned* labels on standard image datasets essentially perfectly. That demonstrates two things, stated at their honest strength: high capacity and near-zero training error are *insufficient* evidence of useful generalization; the network class was expressive enough to memorize arbitrary labels. It does *not* establish that large networks never generalize — many of the same architectures generalize well on real structure. The lesson is about what the evidence fails to prove, not a blanket claim against capacity.

These claims draw on [Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 5 §5.2](https://www.deeplearningbook.org/contents/ml.html) (capacity, under/overfitting), [Ch. 8 §8.1](https://www.deeplearningbook.org/contents/optimization.html) (learning vs. pure optimization), and [Zhang et al., arXiv:1611.03530](https://arxiv.org/abs/1611.03530) (random-label memorization).

## 6. Guided practice — pause and classify

Read each case, pause, and classify it as evidence of a **representation**, **optimization**, or **generalization** issue. Then check your reasoning below.

| Case | Observation |
|---|---|
| A | An exact least-squares fit of an affine model cannot match the three $x^2$ points, while a quadratic model matches all three exactly. |
| B | Two runs use the same network, data, and objective; one reaches training loss 100 times lower than the other. |
| C | Training loss keeps falling while held-out loss rises for several evaluations. |

### Check your reasoning

- **A** most directly supports a **representation** diagnosis for the affine class. The contrast with the quadratic model shows the affine class could not contain a good-enough function for this target. It does not prove that quadratics would generalize, only that the affine limitation is representational.
- **B** supports an **optimization** diagnosis for the worse run, because the better run shows the *same class* can fit the training objective more closely. It does not yet tell you anything about held-out performance.
- **C** supports a **generalization** problem, because improvement on seen evidence accompanies deterioration on unseen evidence. It does not by itself tell you whether the class is too rich or the training is flawed.

Each of these is an *evidence-supported* diagnosis. It is not proof that no second problem coexists — a model can be hard to optimize *and* generalize poorly.

## 7. Project transfer

Consider this claim, which you will evaluate in your independent attempt:

> “The project network is much larger than a one-layer network, and its training loss is low. Therefore its three-body trajectories are accurate.”

For context (from the authoritative [PINN architecture spec](../pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md), not legacy code): the project backbone is a SQR-SkipResNet with SIREN sinusoidal activations, **12 hidden layers of 256 neurons each** — genuinely much larger than a one-layer affine map. The factual premise about size is real. The question is what that premise *supports* and what it does *not*.

## Independent attempt — stop here

Answer all four from memory. Do not copy lesson phrasing. Naming uncertainty is allowed and expected; say what you do not yet know.

1. **Explain:** In your own words, distinguish representation, optimization, and generalization *without* using the toolbox analogy.
2. **Diagnose:** Classify Cases A, B, and C from §6. For each, cite the specific observation that supports your classification, and name one conclusion the observation does *not* establish.
3. **Transfer:** Respond to the project claim in §7 in 3–5 sentences. State what the larger network and low training loss *do* support. Then name at least three categories of evidence still needed before you would trust the three-body trajectories.
4. **Correct the old model:** Rewrite this statement so it is technically sound: *“More neurons and layers give more accuracy because more fitting is executed during each layer.”* Preserve whatever is correct in the original; do not replace it with “bigger is bad.”

When you finish:

- answer from memory rather than copying lesson phrases;
- uncertainty is allowed and should be named explicitly;
- stop after the four responses and return them to the teaching agent;
- your original response will be preserved verbatim, diagnosed without a grade, and followed by one corrected re-attempt where needed.

Do not read past this section until you have written your four responses. Nothing below the checkpoint gives away the answers.

## Review hook

> “A very large model achieves almost zero training loss. From memory, draw the three-question diagnostic and name the additional observation you would seek at each step.”

This review hook is **not due yet**. It becomes due at the next learning session only after the current correction cycle closes.

## Walls for this unit

The following are deliberately deferred because they do not improve the target capability (distinguishing representation, optimization, and generalization from evidence) at this stage:

- **Proofs of universal approximation.** A theorem that a sufficiently wide network can approximate continuous functions does not teach you to diagnose evidence on a fitted model; deferred.
- **VC dimension, Rademacher complexity, formal generalization bounds.** These formalize generalization but require statistical-learning machinery that would bury the three-question distinction; deferred.
- **Double descent and modern scaling-law subtleties.** Important for large-model behavior, but they complicate the basic gate before the gate is intuitive; deferred.
- **Optimizer mechanics, gradients, and autograd.** These explain *how* optimization proceeds and are the subject of Unit 0002; deferred.
- **Full PINN validation and physics-residual design.** These supply the *physical-consistency* evidence category named in transfer, and belong to Units 0004–0005; deferred.

## Sources

- [Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 5 — “Machine Learning Basics” §5.2](https://www.deeplearningbook.org/contents/ml.html) — capacity, underfitting, overfitting, generalization.
- [Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 8 — “Optimization for Training Deep Models” §8.1](https://www.deeplearningbook.org/contents/optimization.html) — learning differs from pure optimization.
- [Zhang et al., “Understanding deep learning requires rethinking generalization,” arXiv:1611.03530](https://arxiv.org/abs/1611.03530) — high-capacity networks can fit random labels.
- [PINN architecture specification (local, authoritative)](../pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md) — project architecture facts used in §7.

## Attempt and feedback history

No Unit 0001 attempt is recorded yet. The learner completes the independent attempt in conversation; the teaching agent appends it here verbatim before giving diagnostic feedback.
