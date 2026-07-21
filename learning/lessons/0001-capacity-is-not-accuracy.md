---
lesson_id: "0001"
title: Capacity is not accuracy
format: deep-unit
capability_state: practicing
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

Answer: the third thing is the final outcome or value of a neuron, and it provides the answer? I'm not sure if I'm getting what you're asking here. 

2. In Orientation 0 you wrote that more layers “give more accuracy because more fitting is executed during each layer.” From memory now — name **one thing** a larger network definitely provides, and **one thing** it does **not** by itself guarantee.

Answer: A larger network provides more flexibility. With more neurons and layers, we are able to better fit our model to a situation that we want, so that we can adjust the values for the weights and biases to better approach the final value that we want to achieve. I'm not sure what a larger network by itself does not guarantee. It could be that if we don't design a training loss function well, the gradient descent will not happen smoothly as we want? 

Commit to an answer for both before reading on. These are diagnostic predictions, not a test you can fail: the value is in committing first, then comparing your prediction to the formal statement as you read §2–§3. Your exact wording will be preserved either way.

## 1. The intuition, then retire it

Suppose you face a mechanical job. Three very different facts matter:

- **The toolbox** — does it even contain a tool capable of this job?
- **Your ability to pick the right tool and use it well** — given the toolbox, do you actually select and drive the right tool?
- **Success on a new job** — when the next job is slightly different, does the work still hold?

Map these to three separate questions about a neural network:

- **Representation** — is the model class rich enough, relative to *this* target, to contain a function capable of the required mapping? <mark>User: What's a model class?<mark>
- **Optimization** — did the training process find a sufficiently good member of that class?
- **Generalization** — does the fitted function work on relevant cases that did not determine its parameters?

The toolbox analogy gets you to the shape of the distinction. Then retire it. Networks are not toolboxes, training is not a mechanic, and stretching the picture will start to mislead. Keep the three questions; drop the analogy.

## 2. The formal statement

Let a model class be a set of candidate functions

$$\mathcal{F} = \{f_\theta\}$$

indexed by parameters $\theta$. Training selects one fitted member $f_{\hat\theta} \in \mathcal{F}$ by adjusting **all** parameters $\theta$ jointly under one objective — no layer is fitted separately; the whole network is one composed function whose every weight and bias is tuned together. Define:

- training loss $L_{\mathrm{train}}(f)$ — average error over the examples whose parameters the fit was allowed to see;
- unseen / validation loss $L_{\mathrm{unseen}}(f)$ — average error over relevant examples that did *not* choose $\hat\theta$. User: what do you mean relevant examples that did not choose ${\theta}$?

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

That single sentence is the load-bearing claim of this unit. User: my biggest confusion till now is: what do you mean by representation? How well the model class can fit a specific scenario? How many functions that are available to be chosen for modeling?

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
| A | An exact least-squares fit of an affine model cannot match the three $x^2$ points, while a quadratic model matches all three exactly. | representation
| B | Two runs use the same network, data, and objective; one reaches training loss 100 times lower than the other. | optimization
| C | Training loss keeps falling while held-out loss rises for several evaluations. | generalizations

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

Representation is basically how big and rich the model class is for a neural network. The more and richer the model class contains, perhaps with different functions and different tools that the neural network are equipped with (although currently I cannot name you any examples of what a model class contains inside, except the only thing I know is functions), the better the chances that the neural network can sue this strong representation capabilities to model and fit a specific requirement. optimization is about training, and it's what we try to continuously minimize the training less to find the best fitting parameters for a model class. Generalization is the ability of the neural network to extends its answers to anser questions that it has not yet seen before. This generalization capabilities are independent from optimization, and overfitting and underfitting are examples of this independence. 


2. **Diagnose:** Classify Cases A, B, and C from §6. For each, cite the specific observation that supports your classification, and name one conclusion the observation does *not* establish.
Already done this.

3. **Transfer:** Respond to the project claim in §7 in 3–5 sentences. State what the larger network and low training loss *do* support. Then name at least three categories of evidence still needed before you would trust the three-body trajectories.

The larger network and low training loss are good evidence to support that the model is indeed representative enough to learn to model different trajectories, and it is able to do so accurately because of the low training loss. But we still need to see its generalization abilities in order to fully be confident of whether or not it's a good model at predicting correct trajectories. Overfitting and underfitting could be problems. This is all I can say for this question for now.


4. **Correct the old model:** Rewrite this statement so it is technically sound: *“More neurons and layers give more accuracy because more fitting is executed during each layer.”* Preserve whatever is correct in the original; do not replace it with “bigger is bad.”

More neurons and layers give more accuracy because each layer takes the input from the previous layer, adds its own calculations, and produces a new result to be fed into the next layer, until the last layer. The training and loss minimizing happens at the same time for all layers. 


When you finish:

- answer from memory rather than copying lesson phrases;
- uncertainty is allowed and should be named explicitly;
- stop after the four responses and return them to the teaching agent;
- your original response will be preserved verbatim, diagnosed without a grade, and followed by one corrected re-attempt where needed.

Do not read past this section until you have written your four responses. Nothing below the checkpoint gives away the answers.

## Review hook

> “A very large model achieves almost zero training loss. From memory, draw the three-question diagnostic and name the additional observation you would seek at each step.”

This review hook is **not due yet**. It becomes due at the next learning session only after the current correction cycle closes.

User: I'm still a little confused at what the general "three-category" or three-perspsectives are. Representation, optimization, and generalization? But doesn't this question already contain the first two? 

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

### Initial independent attempt — 2026-07-19

The learner also wrote the cold-retrieval answers, three clarification questions ("what's a model class?", "what do you mean relevant examples that did not choose θ̂?", "what do you mean by representation?"), the Review-hook clarification, and the Case A/B/C classifications inline in the body of the lesson. Those inline annotations are preserved in place as the learner's working layer and are addressed under "Term clarifications" below.

#### Response 1 — Explain

> Representation is basically how big and rich the model class is for a neural network. The more and richer the model class contains, perhaps with different functions and different tools that the neural network are equipped with (although currently I cannot name you any examples of what a model class contains inside, except the only thing I know is functions), the better the chances that the neural network can sue this strong representation capabilities to model and fit a specific requirement. optimization is about training, and it's what we try to continuously minimize the training less to find the best fitting parameters for a model class. Generalization is the ability of the neural network to extends its answers to anser questions that it has not yet seen before. This generalization capabilities are independent from optimization, and overfitting and underfitting are examples of this independence.

**What is correct:**
- Representation correctly anchored to "how big and rich the model class is" — that is the right object (the class, not a fitted model).
- Optimization correctly anchored to training and to minimizing training loss to find parameters.
- Generalization correctly anchored to "questions it has not yet seen before."
- The instinct that generalization can fail independently of optimization (overfitting/underfitting) is the right instinct.

**Diagnosis: imprecise.** Two imprecisions, one load-bearing:
1. The phrase "use this strong representation capabilities to **model and fit** a specific requirement" slips from the class (representation) to the act of fitting a member (optimization). The class is the *menu*; fitting is *placing an order*. Richness of the menu does not fit anything — it only makes a good fit *possible*.
2. "best fitting parameters **for a model class**" — parameters belong to one fitted member $f_{\hat\theta}$, not to the class $\mathcal{F}$. The class has no parameters; it has candidates.
3. "generalization capabilities are independent from optimization" is mostly right but overstated as a universal: they can fail independently, and they can also fail together. The safe statement is "a model can be well-optimized and still generalize poorly" — one-directional, not a general independence claim.

**Smallest correction:** Replace "use this strong representation capabilities to model and fit" with "makes it *possible* that a good fitting function exists in the class — but representation alone does not do the fitting." Use the §4 algebraic example as the counterexample: the affine class could not represent $y=x^2$ at three points; the quadratic class could. The richer class made a correct fit *possible*, not *done*.

#### Response 2 — Diagnose

> Already done this.

(Refers to the inline classifications in §6: A = representation, B = optimization, C = generalization.)

**What is correct:** All three classifications are correct.
- A (affine cannot fit $x^2$ points; quadratic can) → representation ✓
- B (same network, one run 100× lower training loss) → optimization ✓
- C (training loss falls, held-out loss rises) → generalization ✓

**Diagnosis: incomplete.** The prompt asked for two things per case: (a) the classification, and (b) cite the observation that supports it AND name one conclusion the observation does *not* establish. You did (a) inline. You did not do (b) for any case.

**Smallest correction:** For each case, add one sentence of the form "Observation X supports this because __; it does *not* establish __." Example for Case B: "The 100×-lower-loss run supports an optimization diagnosis for the worse run because the same class demonstrably fits the training objective better; it does *not* establish anything about held-out performance for either run."

#### Response 3 — Transfer

> The larger network and low training loss are good evidence to support that the model is indeed representative enough to learn to model different trajectories, and it is able to do so accurately because of the low training loss. But we still need to see its generalization abilities in order to fully be confident of whether or not it's a good model at predicting correct trajectories. Overfitting and underfitting could be problems. This is all I can say for this question for now.

**What is correct:**
- "Larger network" supports representational capacity (richness of the class) — correct.
- "We still need to see its generalization abilities" — correct direction.
- Naming overfitting/underfitting as candidate problems — on-topic.

**Diagnosis: misconception (load-bearing).** The clause "it is able to do so **accurately because of the low training loss**" is the exact claim this unit exists to repair, now endorsed in your own words. Low training loss supports fit **to the training objective on the training cases**. It does **not** support accuracy on trajectories in general — which is a generalization claim. The project claim you were asked to push back on is precisely "low training loss → trajectories are accurate," and this response concedes that step.

The prompt also asked for **at least three categories of evidence still needed**. You named one (generalization). Three more categories from the unit that you did not reach:
- **Held-out trajectory performance** on a valid validation split — quantitatively, not just "we need to see generalization."
- **Physical-consistency evidence** (residual against the equations of motion) — does the fitted trajectory obey Newton's laws, not just fit training data?
- **Domain/edge-case coverage** — does the model handle close encounters, chaotic regimes, or initial conditions outside the training distribution?
- (Also valid: baseline comparison to a trusted integrator; reproducibility across seeds; uncertainty estimates.)

**Smallest correction (counterexample):** In [Zhang et al.](https://arxiv.org/abs/1611.03530), high-capacity networks fit *randomly assigned* labels with near-zero training loss. So near-zero training loss is possible even when there is no true input→output relationship to generalize. Therefore: low training loss is *consistent with* accuracy but does *not establish* it. The missing inferential step is "training loss → accuracy on training cases → accuracy on unseen trajectories," and the second arrow is the one low training loss cannot buy.

This is the **focused re-attempt** requested below.

#### Response 4 — Correct the old model

> More neurons and layers give more accuracy because each layer takes the input from the previous layer, adds its own calculations, and produces a new result to be fed into the next layer, until the last layer. The training and loss minimizing happens at the same time for all layers.

**What is correct:**
- "Training and loss minimizing happens at the same time for all layers" — this correctly kills the original statement's "each layer executes its own fit" error. Layers form one jointly-optimized function; this is the joint-optimization correction and it is exactly right.
- The description of the forward pass (each layer takes the previous layer's output) is mechanically correct.

**Diagnosis: imprecise.** The rewrite *adds* a correct clause but does not *revise* the false one. The sentence still begins "More neurons and layers give more accuracy because..." — which is the very guarantee the unit says cannot be made. More capacity makes better performance *possible*, not *guaranteed*. The original statement had two errors; you corrected one (per-layer fitting → joint fitting) and left the other (capacity → guaranteed accuracy) standing.

**Smallest correction:** Replace "give more accuracy" with "may make better performance *possible* by increasing the range of functions the network can represent; whether that performance is actually realized depends on optimization, and whether it holds beyond training cases depends on generalization."

#### Corrected re-attempt — *focused on the Response 3 misconception*

Your Response 3 endorsed the step "low training loss → trajectories are accurate." That is the same shape as the first clause of the statement in Response 4. Re-attempt **only this Transfer prompt**, in your own words:

> The project network has 12 hidden layers of 256 neurons, and its training loss is low. Re-state what those two facts *do* support, then re-state what they do *not* establish — using the Zhang et al. counterexample (networks that fit random labels with near-zero training loss) as the concrete reason the second arrow fails.

Aim for 3–5 sentences. Do not just rephrase the lesson — name the inferential step that low training loss cannot buy. After your re-attempt lands, the Response 4 first-clause fix and the Response 2 "what it doesn't establish" skill will follow naturally from the same distinction.

### Term clarifications (addressing inline questions)

You asked four questions inline. Brief answers, using only terms already in the lesson:

- **"What's a model class?"** — The set of candidate functions the network *could* be, before training chooses one. Written $\mathcal{F} = \{f_\theta\}$ in §2. Concretely: fix the architecture (12 layers, 256 neurons, SIREN activations) and you have fixed the class; every possible assignment of weights and biases is one member $f_\theta$ of that class. The class is the *menu*; one fitted network is one *item ordered from it*. (Your instinct in the inline note — "how many functions available" — is essentially right: the class is the collection of all members reachable by some parameter choice.)
- **"What do you mean relevant examples that did not choose $\hat\theta$?"** — Training adjusts $\hat\theta$ to reduce loss on the *training* examples; those examples "chose" $\hat\theta$ in the sense that they shaped it. Held-out examples are ones the training procedure never saw, so they did *not* shape $\hat\theta$. "Relevant" means: drawn from the same kind of problem you actually care about (here, three-body trajectories with similar regimes), not arbitrary random inputs.
- **"What do you mean by representation? How well the model class can fit a specific scenario? How many functions available?"** — Closer to the second. Representation is about whether a *sufficient* function exists somewhere in the class for *this* target — a yes/no richness question about the menu, not a measurement of how well any particular fitted member does. "How well a fitted model fits" is an *optimization/evaluation* question about one member, not a representation question about the class.
- **"The three-question perspectives — doesn't the Review hook already contain the first two?"** — The Review hook asks you to *re-derive the gating sequence from memory* and name the *additional observation you would seek at each step*. The three questions are not three coexisting labels; they are three sequential gates (§3): first ask whether a good function exists in the class; *only if yes* ask whether training finds one; *only if yes* ask whether it works on unseen cases. The Review hook tests whether you can reproduce that *sequence*, including what each step does not yet entitle you to conclude.
