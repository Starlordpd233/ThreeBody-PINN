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
