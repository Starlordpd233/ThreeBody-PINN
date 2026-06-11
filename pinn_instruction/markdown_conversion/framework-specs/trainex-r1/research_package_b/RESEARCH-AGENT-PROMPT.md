# Trainex R1b Research Agent Prompt (runbook and operations knowledge)

**[User instructions — not part of the prompt]** Attach these 4 files to the external
agent's conversation, then paste everything below the horizontal rule as the prompt:

1. `research_package_b/RESEARCH-CONTEXT-MASTER.md` (this package's master)
2. `specs/2026-06-10-training-execution-design.md` (shared snapshots at the round root)
3. `specs/pinn_architecture.md`
4. `specs/ctl_instruction.md`

---

You are an external research agent for a computational-physics ML project: a
curriculum-trained physics-informed neural network (CTL-PINN) for the gravitational
three-body problem, trained on a single MacBook by a project owner who is not an expert
at model training. This is the **runbook-and-operations-knowledge half** of the project's
foundational research round: your findings become the raw material for the user's
step-by-step training runbook and verification surfaces. (A companion package covering
the core decisions — framework choice, tracking, compute strategy, checkpoint policy,
loop skeleton, determinism — is being researched separately; do not produce decision
menus or recommendations on those topics here.)

You have been given four files. You have NO access to the project's codebase or
repository — work only from these four files plus your own research of current primary
sources (official documentation, release notes, issue trackers, published benchmarks and
literature; not blog hearsay):

- `RESEARCH-CONTEXT-MASTER.md` — your entry point. It contains the orientation, the hard
  constraints, five research topics (K1–K5, with K4 feasibility and K5 trainer
  correctness as the two priorities), and the output contract your deliverable must
  satisfy. Read it first and follow it exactly.
- `2026-06-10-training-execution-design.md` — the training-execution reference design
  whose entry points and monitoring surfaces your findings feed. It is a quick-brainstorm
  baseline, not fixed structure — if a finding suggests structural change, record it as a
  decision-relevant observation rather than redesigning.
- `pinn_architecture.md` and `ctl_instruction.md` — the project's authoritative framework
  specs. For the feasibility topic, derive parameter counts, per-step cost structure, and
  curriculum-stage workload from them.

**Your task:** produce structured, cited findings for the five research topics in
`RESEARCH-CONTEXT-MASTER.md`:

- **K4 (priority) — training feasibility envelope:** order-of-magnitude
  wall-clock and memory-footprint estimates for one curriculum stage and a full
  curriculum run on the specified MacBook, per candidate framework, parameterized over
  any project-side facts you don't have — with an explicit list of the numbers the
  project must supply, and explicit flags for outcome ranges that would pressure the
  project's no-cloud constraint.
- **K5 (co-priority) — trainer-correctness verification ladder:** the validation ladder
  practitioners use before trusting a PINN trainer (PINNs fail silently with
  plausible-looking loss curves): AD-vs-finite-difference gradient checks,
  overfit-a-single-batch tests, known-solution fixtures (the three-body problem has
  exact references — Euler collinear, Lagrange equilateral, the figure-eight
  choreography; verify parameterizations from literature), and the ~5-minute smoke-test
  run as a first-class pre-flight step. Deliver as rung → what it catches → pass
  criterion → cost.
- **K1 — PINN training-health watchlist:** documented PINN and curriculum-training
  failure modes, mapped to the monitoring surfaces as signal → meaning → first response
  a non-expert can take.
- **K2 — unattended MacBook training operations:** current macOS-15-era practice for
  sleep prevention, lid-close behavior, terminal-survival, thermal throttling realities
  vs. folklore, power settings, and safe manual stop semantics — plus environment
  pinning and upgrade/re-validation discipline over the project's multi-year life.
- **K3 — runbook design patterns for non-expert operators:** evidence-based patterns
  from well-regarded operational documentation, mapped to the design's five entry
  points.

**Your deliverable:** a single self-contained markdown document satisfying the output
contract in `RESEARCH-CONTEXT-MASTER.md`. In brief: (1) cited, runbook-ready findings
per topic; (2) K4's parameterized estimates with the needed-numbers list and
constraint-pressure flags; (3) K5's verification ladder as a rung-by-rung table liftable
into the runbook's pre-flight section; (4) a "decision-relevant observations" section
listing any finding that implies a project decision — stated as evidence, not
adjudicated; (5) a claims-and-uncertainty register for anything unverifiable or
ambiguous.

Ground rules:

- Verify against current primary sources as of today; do not rely on memory; date-stamp
  your findings and estimates.
- Estimates you cannot ground must be parameterized ranges with stated assumptions —
  never single confident numbers pulled from intuition.
- Where the attached materials are silent or ambiguous, record the gap in the
  claims-and-uncertainty register rather than inventing an answer.
- Write for a non-expert maintainer: plain language, concrete commands and version
  numbers, everything at the mechanical surface — what the user types, what the user
  sees, what files appear.
