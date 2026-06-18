# Post-Spec R1 Delivery Note

This file is user-only routing context for the `postspec-r1` External Research
Workflow package. Do not upload this file to the external research agent.

## Package Standing

- Channel: build-design / strategy advisory
- Report standing: options, findings, and recommendations only
- Not a candidate verdict source for framework-spec adjudication
- Final decisions remain with the project owner

## Source Baseline

- Baseline commit: `6a720fe0`
- Packaged on: 2026-06-18

Refresh the package if any source document changes before handoff.

## Package Root

```text
pinn_instruction/markdown_conversion/framework-specs/postspec-r1/
```

## Files

```text
pinn_instruction/markdown_conversion/framework-specs/postspec-r1/
  DELIVERY-NOTE.md
  research_package/
    RESEARCH-AGENT-PROMPT.md
    RESEARCH-CONTEXT-MASTER.md
    FRAMEWORK-SPECS-BUNDLE.md
```

## Handoff Instructions

1. Open `research_package/RESEARCH-AGENT-PROMPT.md`.
2. Attach exactly these two files to the external agent conversation:
   - `research_package/RESEARCH-CONTEXT-MASTER.md`
   - `research_package/FRAMEWORK-SPECS-BUNDLE.md`
3. Paste only the text below the horizontal rule in
   `RESEARCH-AGENT-PROMPT.md`.
4. Ask the external agent for one polished, PDF-ready Markdown report.
5. If the external agent can also export a PDF, request it as an optional
   companion output, not as the only source.

## Result Landing Path

Save returned reports under this round root using filenames like
`chatgpt-postspec-report.md`, `claude-postspec-report.md`, or another
agent-name-specific variant:

```text
pinn_instruction/markdown_conversion/framework-specs/postspec-r1/research_results/
```

If multiple agents are used, save each report separately. A later consolidation
document may be created after the user reviews the returned reports.

## Package Intent

This round asks for broad strategic direction after the recent spec-heavy work.
It should help decide whether the next major stage should be EDL-first,
Trainex-first, a hybrid, or a different path proposed by the external agent.

The package intentionally avoids asking for detailed implementation gates,
task-by-task planning, milestone checklists, or a full execution backlog.
