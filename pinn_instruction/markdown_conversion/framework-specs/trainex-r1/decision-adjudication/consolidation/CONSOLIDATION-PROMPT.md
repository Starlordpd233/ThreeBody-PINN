# Trainex r1a Decision-Adjudication — Consolidation Prompt (Stage 2)

**User instructions — not part of the prompt.** Attach: (a) the 2–3 Stage-1 resolution
reports; (b) `RESEARCH-CONTEXT-MASTER.md` plus the same 8 originals
(`trainex-r1a-options-and-decisions.md`, `chatgpt-pro-resolution.md`, `ctl_instruction.md`,
`pinn_architecture.md`, `2026-06-10-training-execution-design.md`,
`postspec-r1-direction-assessment.md`, `trainex-r1b-findings.md`,
`trainex-r1b-findings-2.md`). Paste everything below the horizontal rule. Run on one agent.
Save the output as `trainex-r1a-resolution-doc.md`.

---

You are the consolidation agent. You are given 2–3 independent decision-adjudication
reports (each named like `*-decide-resolution.md`) produced from the same brief, plus the
original source materials they were based on (`RESEARCH-CONTEXT-MASTER.md` and its
attachments).

Produce **one final resolution** — the ultimate recommended decision for each in-scope
build decision: D1, D2, D3, D4-a/b/c/d, D5-a/b/c, D6, D7-a/b/c/d, and B-1, B-2, B-3, B-4,
B-5, B-6, B-9, B-10, B-11. (B-7, B-8, and B-12 are out of scope — B-7 is a cosmetic doc edit,
B-8 is settled by the attached spec, and B-12 is a split-policy item routed to v1.5.)

For each decision:

- State the **final recommended pick.**
- **Agreement / divergence note:** did the source reports agree? If they diverged, say how,
  and justify which position you adopt — breaking ties with the attached specs and r1b
  findings, not by preference.
- **Confidence** (High / Medium / Low). Where the source reports diverged, or all expressed
  low confidence, **mark the row for the owner's closer look.**
- Carry through the **needed-now / deferrable** tag and any **owner-preference / empirical**
  flag.

Then, once for the report:

- a **composed first-run recipe** from the final set (a coherence check that the picks work
  together);
- **fill the ⚖ thresholds (a Stage-2 job):** for each guard/threshold left as a ⚖ placeholder
  in the decision sheet (loss-explosion multiple + consecutive-log window; disk-floor GB;
  memory-watermark multiple), take the value from the attached r1b findings where they give
  one, and record in the merged register any ⚖ threshold r1b does not actually specify — do
  not invent it;
- a **merged claims-and-uncertainty register** (unresolved gaps, project-side unknowns,
  assumptions);
- a one-line **standing restatement** — this is a recommendation the owner ratifies, not a
  science-spec verdict; the D1-p precision question was left to the owner, and the B-8 ε_H
  gate direction is settled by the attached spec (REJECT if `eps_H > 1e-5`, smaller passes),
  not an open item.

Follow the standing, scope, and hard constraints in `RESEARCH-CONTEXT-MASTER.md` exactly.
Be decisive but honest; where the sources are silent, record it — do not invent. You suggest
a decisive default for the owner to ratify; you never assert final authority — where the
source reports diverged on an owner-preference or empirical row, flag it for the owner rather
than deciding it.
