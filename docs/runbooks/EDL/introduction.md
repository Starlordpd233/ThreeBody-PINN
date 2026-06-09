# Empirical Decision Loop in the Three-Body Problem Project

## 1. Project Context

This repository is developing an end-to-end three-body trajectory-learning system. Its broad pipeline includes:

1. Generating high-precision three-body simulations.
2. Validating and preprocessing those trajectories.
3. Constructing physically meaningful model inputs and targets.
4. Training a physics-informed neural network.
5. Eventually preparing downstream language-model training workflows.

The project is currently not in the final implementation stage. It is still establishing and correcting the framework design.

The active and upcoming work is organized around three thematic issue documents:

- **Issue 01:** architecture and physics foundations.
- **Issue 02:** data pipeline and validation.
- **Issue 03:** curriculum and training loop.

The current v1.4 milestone addresses Issue 01. The next two major milestones are expected to address Issues 02 and 03.

During this period, the primary deliverables are authoritative Markdown framework specifications:

- `pinn_architecture.md`
- `ctl_instruction.md`
- `sampling_method.md`

These specifications describe what the future system must do. The existing `pinn/` implementation is based on an older framework version and is not authoritative for current design decisions. A future milestone, presently identified as `FUT-01`, will rebuild or align the implementation from the revised specifications.

This creates a deliberate separation:

```text
Current stage:
research → adjudication → specification → validation

Later stage:
implementation → training → evaluation → research iteration
```

## 2. The Problem EDL Addresses

Some framework questions can be settled through:

- explicit source material;
- short first-principles derivations;
- dimensional analysis;
- established physics;
- or straightforward engineering constraints.

Other questions cannot.

For example, theory may determine the form of a loss function without determining:

- the denominator floor;
- the clipping threshold;
- the loss weight;
- the Huber transition value;
- the initialization constant;
- the curriculum threshold;
- or the most stable normalization choice.

Choosing such values merely because they are common would introduce arbitrary assumptions into an authoritative specification. On the other hand, building the entire production system to investigate every uncertain value would be wasteful and might postpone important decisions until too late.

EDL was created to occupy the middle ground:

```text
Not enough evidence to choose safely
                  ↓
Do not invent a value
                  ↓
Do not build the whole system
                  ↓
Run or prepare the smallest useful empirical investigation
                  ↓
Use the result as decision support
```

EDL therefore complements theoretical reasoning. It does not replace it.

## 3. What EDL Means

**EDL** stands for **Empirical Decision Loop**.

It is a structured method for using narrowly scoped research or experiments to inform framework-design decisions that cannot be settled confidently from source documents and first principles alone.

An EDL investigation should:

1. Identify one concrete uncertainty.
2. Explain why existing sources do not resolve it.
3. Enumerate the plausible alternatives.
4. State the consequences of each alternative.
5. Determine whether an inexpensive experiment could distinguish them.
6. Define the measurements and interpretation rules before execution.
7. Run only the smallest experiment capable of producing useful evidence.
8. Record the result and its limitations.
9. Let the user make or approve the resulting design decision.

An EDL result is evidence. It is not automatically a framework decision.

## 4. Why EDL First Appeared

The current EDL methodology originated during Phase 19.

The energy-drift loss required a denominator floor, `epsilon_H`. The available sources defined the formula and named the symbol, but did not specify its value. An agent could easily have inserted a familiar constant such as `1e-8`, but that would not have been grounded.

This became:

- the canonical gap `GAP-19-01`;
- the research-support item `EDL-19-01`;
- and eventually a user-resolved scale-relative rule.

The final contract was:

```text
epsilon_H = 1e-4 * S_H
```

with no fallback floor and validation requiring `S_H` to be finite and strictly positive.

This example established several important principles:

- familiar defaults are not automatically justified;
- framework decisions require traceable provenance;
- EDL artifacts remain non-canonical;
- the user retains decision authority;
- closed decisions remain closed unless the user explicitly initiates new adjudication.

The existing EDL materials are located in:

```text
.planning/research/edl/
├── README.md
├── INDEX.md
├── EDL-19-01-epsilon-H.md
└── EDL-19-01-resolution.md
```

## 5. Current EDL Authority

The current EDL methodology is explicitly marked `canonical: false`.

It does not override:

- `AGENTS.md`;
- milestone requirements;
- framework specifications;
- phase plans;
- phase gap registers;
- or direct user instructions.

For source-silent decisions, the phase-local gap register remains the authoritative governance record. It determines:

- what work is blocked;
- what independent work may continue;
- whether the phase may close;
- and how the decision was ultimately resolved.

The current authority chain is:

```text
Gap register
    ↓
EDL research brief
    ↓
Optional user-authorized probe
    ↓
Decision evidence
    ↓
User instruction
    ↓
Canonical specification update
```

The EDL brief or probe cannot independently change a framework specification.

## 6. EDL During Framework Revision

The first proposed use of EDL occurs while Issues 01–03 are being adjudicated.

In this role, EDL helps when:

- a decision is empirically consequential;
- the designated sources are silent or ambiguous;
- first principles narrow the options but do not select one;
- and a relatively inexpensive investigation could materially inform the choice.

Candidate subjects include:

- loss normalization and denominator floors;
- Huber thresholds;
- clipping bounds;
- SIREN initialization parameters;
- LayerNorm configuration;
- curriculum-stage thresholds;
- sampling allocations;
- preprocessing tolerances;
- and stage-transition criteria.

The probe ladder moves from cheapest to most expensive:

1. Analytic fixture.
2. Existing-dataset scan.
3. Perturbation or sensitivity test.
4. Surrogate training test.
5. Minimal real-training ablation.

The investigation should stop as soon as it has enough evidence for the specific decision. Exhaustive optimization is not the objective.

## 7. Existing Validation Probes Are Different

Phase 21 already executed five disposable probes:

- scaling consistency;
- center-of-mass invariance;
- componentwise automatic differentiation;
- force-energy consistency;
- loss-stability dry run.

These are not decision EDL probes.

Their question is:

> Does this already-specified contract appear internally consistent and minimally implementable?

An EDL decision probe asks:

> Which contract should we select?

This distinction is important:

| Mechanism | Timing | Purpose |
|---|---|---|
| First-principles adjudication | Before specification | Determine what physics and logic require |
| EDL decision probe | Before contract finalization | Compare unresolved empirical alternatives |
| Validation probe | After contract selection | Test self-consistency and basic implementability |
| Full training experiment | During implementation/research | Measure actual system performance |

Passing Phase 21 proves that several isolated contracts can be executed consistently. It does not prove that the complete framework will train successfully as an integrated system.

## 8. Proposed Pre-Build Role

The second proposed EDL role would occur after the framework-spec revision milestones but before serious full-scale implementation and training.

At that point, the project would possess a mostly complete design but would not yet want to commit substantial resources to the final build.

The proposed activity would construct a small-scale, end-to-end realization of the specifications. Its purpose would be to answer questions such as:

- Can the preprocessing, model, losses, automatic differentiation, and curriculum logic connect coherently?
- Can a small dataset move through the complete pipeline?
- Can a reduced model complete a short training run?
- Are gradients finite and reasonably scaled?
- Do stage transitions execute?
- Are specified metrics computable?
- Do different contracts interact in unexpected ways?
- Does the design impose impractical memory or runtime requirements?
- Are any instructions too ambiguous to implement consistently?

This is best understood as a **framework integration preflight**.

It is larger than a normal one-decision EDL probe but smaller than production implementation.

```text
Isolated specification checks
             ↓
Small integrated preflight
             ↓
Full implementation
             ↓
Production-scale training
```

## 9. Authority of the Preflight

The preflight should not automatically reopen completed EDL decisions or previously approved contracts.

Those decisions were examined, resolved, and closed for a reason. A small prototype should not be granted authority to overrule them merely because one limited run behaved unexpectedly.

A preflight failure might instead indicate:

- an implementation defect;
- an incorrectly translated specification;
- an unstated integration requirement;
- a missing operational detail;
- an empirical calibration task already intended for later work;
- a limitation of the small-scale fixture;
- or a genuinely new problem not covered by the earlier decision.

The eventual methodology must define how these categories are distinguished. However, the preflight itself should produce evidence and findings, not autonomous contract revisions.

Any change to an authoritative specification would still require a separate, explicit user-approved process.

## 10. What EDL Should Not Become

EDL should not become:

- a substitute for physics;
- a justification for arbitrary trial and error;
- an unrestricted hyperparameter search;
- a way to bypass source-silence governance;
- a second production codebase;
- an excuse to implement the full system prematurely;
- or a claim that success on a tiny fixture guarantees success at scale.

EDL is particularly unsuitable when:

- the answer follows directly from a short derivation;
- the question is purely presentational;
- the existing sources explicitly settle it;
- no meaningful small proxy exists;
- or only full-scale training can answer the question.

## 11. Principal Risks

A future EDL design must control several risks:

- **False confidence:** A tiny successful run does not prove large-scale convergence.
- **Prototype drift:** Experimental code may accidentally become production architecture.
- **Fixture overfitting:** A design may work only on easy or synthetic trajectories.
- **Metric ambiguity:** Results become subjective when decision rules are not defined beforehand.
- **Scale dependence:** Thresholds calibrated on a small subset may not generalize.
- **Experiment sprawl:** Too many open-ended ablations can stall specification work.
- **Authority confusion:** Experimental findings may be mistaken for canonical decisions.
- **Reproducibility failure:** Results are weak if seeds, data, environment, and commands are not retained.

## 12. Current State

The repository currently has:

- a coherent draft methodology for decision-level EDL;
- a central EDL registry;
- one resolved EDL case;
- canonical gap-governance integration;
- five executed specification-validation probes;
- detailed implementation-divergence handoffs for `FUT-01`;
- explicit empirical recommendations in Issues 02 and 03.

It does not yet have:

- a generalized EDL execution harness;
- a standard decision-record schema for completed probes;
- a formal framework-integration preflight;
- a policy for interpreting preflight failures;
- a resource budget for experiments;
- or a roadmap milestone dedicated to small-scale end-to-end verification.

## 13. Central Design Question

The discussion is therefore not simply:

> Should this project use experiments?

It already does.

The real design problem is:

> How should the project organize multiple levels of empirical evidence so that experiments improve framework quality without overriding theoretical reasoning, closed decisions, source-of-truth governance, or the separation between design and production implementation?

A likely conceptual structure is:

```text
Layer 1: Theoretical and source-based adjudication
Layer 2: Decision-level EDL for unresolved empirical choices
Layer 3: Contract-level disposable validation probes
Layer 4: Small-scale framework integration preflight
Layer 5: Full implementation and research-scale training
```

The next discussion should determine whether Layers 2 and 4 should share one EDL methodology or be governed as separate but related workflows.