# Trainex r1a Decision-Adjudication — Research Agent Prompt

**User instructions — not part of the prompt.** Attach these files to the external agent
conversation (individually — no folders), then paste everything below the horizontal rule.
Run this same package on **2–3 agents in parallel**.

1. `RESEARCH-CONTEXT-MASTER.md`
2. `trainex-r1a-options-and-decisions.md`
3. `chatgpt-pro-resolution.md`
4. `ctl_instruction.md`
5. `pinn_architecture.md`
6. `2026-06-10-training-execution-design.md`
7. `postspec-r1-direction-assessment.md`
8. `trainex-r1b-findings.md`
9. `trainex-r1b-findings-2.md`

Request one polished, PDF-ready Markdown report.

---

You are an external research agent helping finalize the build-execution decisions for a
curriculum-trained physics-informed neural network (CTL-PINN) that will be built and run by
a non-expert on a single Apple-Silicon laptop.

**Read `RESEARCH-CONTEXT-MASTER.md` first and follow it exactly** — it defines your task,
the standing of your report, the files you have, what to decide and what to leave alone,
the "thin first step" lens, and the output contract.

In short: a prior research round already produced a decision sheet
(`trainex-r1a-options-and-decisions.md`, with deeper rationale in
`chatgpt-pro-resolution.md`) enumerating roughly twenty build decisions, each with options
and a suggested default. **Adjudicate it:** for each in-scope decision, recommend one
option — endorsing or overriding the suggested default — with reasoning, a confidence
level, cross-decision consistency, and a needed-now / deferrable tag. Respect the attached
science specs (`ctl_instruction.md`, `pinn_architecture.md`) as hard constraints, and flag
anything in the decision sheet they now contradict. Do **not** decide the carved-out
precision item — D1-p (numerical precision, fp32 vs fp64) — treat it as context and keep your
recommendations valid under both precision branches. (**B-8**, the ε_H acceptance-gate
direction, was previously carved out as an open question but is now settled by the attached
spec — `ctl_instruction.md` defines it as REJECT if `eps_H > 1e-5`, smaller passes; treat it
as a fixed constraint, not something to adjudicate. The sheet's **B-7** (cosmetic doc edit)
and **B-12** (split-policy tension routed to v1.5) are likewise out of scope — do not
adjudicate them.) You **suggest** decisive defaults for the owner to ratify; you never hold
final authority — where a row is really an owner preference or an empirical (probe-needed)
matter, flag it rather than deciding it. Where the attached files are silent or ambiguous,
record the gap; never invent.

Produce one decisive, honest, human-readable resolution following the output contract in
the context master.
