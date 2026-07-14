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
