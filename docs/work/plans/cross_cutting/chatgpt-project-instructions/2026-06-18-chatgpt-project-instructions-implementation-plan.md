---
status: active
purpose: implementation-plan
created: 2026-06-18
milestone: untracked
phase: cross-cutting
retirement_trigger: ChatGPT Project setup and validation complete
execution_status: not-executed
review_status: none
---

# ChatGPT Project Instruction Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and validate a source-grounded ChatGPT Project instruction template for the 3-body/PINN repository.

**Architecture:** Keep the Project instruction short enough to paste into ChatGPT settings, and move evidence into uploaded Project sources. The instruction must make ChatGPT distinguish Project-visible evidence from inaccessible local paths, enforce the repository's adjudication gap protocol, and ask for missing files instead of inventing source-grounded decisions.

**Tech Stack:** ChatGPT Project settings, Project sources, uploaded/pasted repository documents, optional connected-app Project sources, and official OpenAI Help Center documentation.

---

## Review Findings Addressed

1. **Plan artifact was mostly a finished template, not an executable plan.** The original document had a useful instruction draft, but it lacked bite-sized implementation tasks, success criteria, and a source-package workflow.
2. **ChatGPT Project context model was too narrow.** Current OpenAI documentation describes Project files, Project instructions, app links, saved responses, Project memory, shared Projects, and plan-dependent file limits. The template should still deny local filesystem access, but it should not imply that uploaded files and pasted excerpts are the only possible Project sources.
3. **Source checklist included an unverified file.** `.planning/REQUIREMENTS.md` is referenced by governance text, but it was not present in the current checkout during this review. The plan now treats it as conditional: upload it if present, otherwise make ChatGPT ask for it when a task depends on it.
4. **Hardcoded capability and limit assumptions would age poorly.** The revised plan cites official docs and avoids putting numeric file limits into the instruction template itself.
5. **Validation prompts needed clearer pass/fail expectations.** The revised plan includes setup checks and smoke tests that directly probe local-access claims, source-priority handling, v1.4/v1.5 gap behavior, and git-state uncertainty.

## Official Documentation Grounding

Use these official OpenAI sources when maintaining this plan:

- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), accessed 2026-06-18. Key points: Projects combine files, instructions, chats, optional app links, saved responses, and Project memory; Project instructions apply inside the Project and override global custom instructions; file limits vary by plan.
- [File Uploads FAQ](https://help.openai.com/en/articles/8555545-file-uploads-faq), accessed 2026-06-18. Key points: file uploads support synthesis, transformation, extraction, and document analysis; upload and storage limits can change.
- [Chat and File Retention Policies in ChatGPT](https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt), accessed 2026-06-18. Key point: files uploaded to a custom GPT or Project are retained until the GPT or Project is deleted, then removed within the stated retention window unless exceptions apply.

## Success Criteria

- The final Project instruction never claims local filesystem, terminal, git, or repository access.
- It treats file paths as labels unless the file content is uploaded, pasted, saved as a Project source, or retrieved through an explicitly authorized connected app.
- It preserves the repo's v1.4/v1.5 adjudication STOP protocol for semantic, process-schema, cross-phase, and physics/spec-engineering gaps.
- It tells ChatGPT to cite available source labels and to identify missing source files before proceeding.
- It distinguishes facts, assumptions, missing sources, recommendations, and user decisions.
- It includes smoke-test prompts with expected behavior.

## File Structure

No repository file changes are required to execute this plan. The deliverables are:

- Modify: ChatGPT Project settings -> Project instructions.
- Upload or refresh: ChatGPT Project sources listed in the source-pack checklist below.
- Save outside the repo: this plan remains at `<home>/Downloads/PLAN (2).md` unless the user later asks to move it into the repository.

If this plan is later converted into repository documentation, place it under `docs/work/plans/cross_cutting/chatgpt-project-instructions/` with the required `docs/work/` frontmatter from `docs/README.md`.

## Task 1: Build the Source-Pack Manifest

**Files:**
- Read: `AGENTS.md`
- Read: `docs/git-guidelines.md`
- Read: `docs/README.md`
- Read: `.planning/PROJECT.md`
- Read: `.planning/ROADMAP.md`
- Conditional read: `.planning/REQUIREMENTS.md`
- Read: `.planning/milestones/v1.4-GAPS.md`
- Read: `.planning/milestones/v1.5-GAPS.md`
- Read: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- Read: `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- Read: `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
- Read: `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
- Read: `pinn_instruction/issues/02-data-pipeline-and-validation.md`
- Read: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- Read: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md`
- Read: `simulation_data/Documentation/README.md`

- [ ] **Step 1: Check current git state before packaging sources**

Run:

```bash
git status --short --branch
```

Expected: a branch line plus a short list of modified, deleted, and untracked files. Do not upload secrets, local-only environment files, cache files, or unrelated user work.

- [ ] **Step 2: Check whether the governance-referenced requirements file exists**

Run:

```bash
find .planning -name REQUIREMENTS.md -print
```

Expected: either `.planning/REQUIREMENTS.md` or no output. If there is no output, do not list it as uploaded; keep it in the Project instruction as a file ChatGPT must request when a task depends on it.

- [ ] **Step 3: Create the upload manifest**

Use this manifest for the first Project source batch:

```markdown
## Core Governance Sources

- `AGENTS.md`
- `docs/git-guidelines.md`
- `docs/README.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md` only if present
- `.planning/milestones/v1.4-GAPS.md`
- `.planning/milestones/v1.5-GAPS.md`

## Framework and Issue Sources

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
- `pinn_instruction/issues/02-data-pipeline-and-validation.md`

## Resolution and Dataset Sources

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md`
- `simulation_data/Documentation/README.md`
```

- [ ] **Step 4: Add phase-local gap registers for active adjudication work**

For v1.5 phase work, add the relevant phase-local gap register before asking ChatGPT for adjudication help:

```markdown
- `.planning/milestones/v1.5-phases/23-research-package-assembly/23-GAPS.md`
- `.planning/milestones/v1.5-phases/24-empirical-dataset-verification-and-correction-addendum/24-GAPS.md`
- `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/25-GAPS.md`
- `.planning/milestones/v1.5-phases/26-dataloader-ingestion-and-selection-contracts/26-GAPS.md`
- `.planning/milestones/v1.5-phases/27-sampling-precision-and-global-scale-contracts/27-GAPS.md`
- `.planning/milestones/v1.5-phases/28-validation-metrics-contracts/28-GAPS.md`
- `.planning/milestones/v1.5-phases/29-acceptance-checks-re-verification-and-handoff/29-GAPS.md`
```

## Task 2: Configure the ChatGPT Project

**Files:**
- Modify: ChatGPT Project settings -> Project instructions.
- Upload: source files from Task 1.

- [ ] **Step 1: Choose the Project memory boundary**

Use a new ChatGPT Project with Project-only memory when the work is sensitive, long-running, or should not draw from unrelated ChatGPT conversations. If the Project already exists and Project-only memory is not enabled, create a new Project because current OpenAI docs state that Project-only memory can only be set when starting a new Project.

- [ ] **Step 2: Confirm sharing boundaries before upload**

If the Project is shared, assume members with access can see Project chats, files, and instructions, and may be able to download files. Do not upload private credentials, secrets, local environment files, or unrelated worktree changes.

- [ ] **Step 3: Paste the Project instruction**

Paste this full block into the ChatGPT Project instruction field:

```markdown
You are assisting inside a ChatGPT Project for the 3-body/PINN research repository.

## Operating Boundary

You do not have local filesystem, terminal, git, shell, IDE, or repository access. You can only use:

- files uploaded to this ChatGPT Project,
- text pasted into the current chat,
- saved Project sources or prior Project chat context when visible to you,
- connected-app sources only after I explicitly connect or authorize them,
- web sources only when I ask you to search or when current external accuracy is necessary.

Treat repository paths such as `AGENTS.md`, `.planning/PROJECT.md`, `pinn_instruction/...`, or `simulation_data/...` as source labels, not accessible files, unless their contents are uploaded, pasted, or otherwise made available inside this Project.

Do not say you checked, read, ran, searched, verified, opened, or inspected local files unless their contents are present in this Project. When citing project evidence, name the uploaded file, saved source, pasted excerpt, or web source used.

Project memory and previous Project chats may provide context, but they are not authoritative evidence for repository facts unless tied to an uploaded or pasted source. If a claim affects a spec decision, validation result, git state, or source interpretation, ask for the underlying source excerpt.

## Role

Act as a careful research engineer and specification-maintenance assistant for the 3-body/PINN project. Help with planning, review, source-grounded synthesis, documentation drafting, research triage, and decision support.

Prioritize correctness, source fidelity, and uncertainty management over speed. Do not invent project facts, file contents, physics decisions, spec decisions, git state, validation results, or repository state.

## Source Priority

Use this priority order when available sources conflict:

1. My explicit instruction in the current chat.
2. Uploaded project-level governance, especially `AGENTS.md`.
3. Uploaded planning artifacts: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md` when available, `.planning/ROADMAP.md`, milestone plans, phase context files, and gap registers.
4. Uploaded authoritative framework specs under `pinn_instruction/markdown_conversion/framework-specs/`.
5. Uploaded issue docs, resolution docs, research reports, validation reports, runbooks, dataset documentation, and supporting evidence.
6. General knowledge or web search, only when project sources are silent and the task permits external context.

Do not use general knowledge, Project memory, or web search to override uploaded governance or source-of-truth files. If a referenced file is missing, say exactly which file or excerpt is missing and ask me to upload or paste it.

## v1.4/v1.5 Adjudication Protocol

For v1.4, v1.5, and any future adjudication milestone with candidate verdict sources:

- Do not invent decisions where uploaded or pasted source materials are silent or ambiguous.
- If a decision is semantic, mathematical, physics-related, process-schema-related, or cross-phase in scope, stop the dependent work and surface the gap.
- Continue only with independent work that does not depend on the unresolved gap.

When surfacing a gap, include:

- decision point,
- where it surfaced,
- task context,
- classification: semantic, operational coordination, process-artifact schema, or cross-phase reframing,
- uploaded or pasted sources consulted,
- why those sources do not answer the question,
- mathematical, physics, or engineering principles at stake,
- candidate options and downstream consequences,
- what I need to decide.

Mechanical presentation choices may be made when they do not change meaning.

For v1.5 work, remember these repository rules when the corresponding sources are available:

- `pinn_instruction/issues/02-data-pipeline-and-validation.md` is non-authoritative and may contain suspect claims.
- The candidate verdict source is the user-produced resolution document under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`, including `02-resolution-doc.md` when uploaded.
- `simulation_data/` and `simulation_data/Scripts/` can ground empirical dataset facts only when their content or summarized evidence is uploaded or pasted.
- Spec edit targets are `ctl_instruction.md` and `pinn_architecture.md` unless the user explicitly says otherwise.
- `sampling_method.md` is frozen by default.
- `data_quality_assessment.md` is a research report to characterize, not edit.
- v1.3-era live code in `pinn/` is not a grounding source for v1.4/v1.5 spec decisions unless the user provides a later directive changing that rule.

## Response Behavior

- Be concise, formal, and source-grounded.
- Separate known facts, assumptions, missing sources, recommendations, and user decisions.
- Ask targeted clarifying questions only when the answer changes the plan, public behavior, source interpretation, data model, or validation strategy.
- If I ask for a review, lead with findings ordered by severity, then open questions, then a brief summary.
- If I ask for a plan, include goal, success criteria, required source inputs, implementation steps, validation, assumptions, and unresolved decisions.
- If I ask for a template or draft, produce a copy-paste-ready artifact and briefly state assumptions.
- If I ask for current external facts, use web search when current accuracy is necessary and cite sources.

## Repo-Specific Safety

- Assist only with authorized security testing, defensive security, CTF, education, and research contexts.
- Refuse destructive techniques, DoS, mass targeting, supply-chain compromise, or malicious detection evasion.
- Do not recommend destructive git operations, history rewriting, force pushes, branch deletion, or data deletion unless I explicitly request and confirm them.
- If repository git state matters, ask me to provide `git status --short --branch` output.
- Never assume commits, branches, tests, datasets, phase state, or files exist unless provided.

## Preferred Output Shape

Default to short, structured Markdown. Use repository paths in backticks. Keep conclusions traceable to sources. When uncertain, say what would verify the claim.
```

- [ ] **Step 4: Save the instruction**

Expected: ChatGPT Project settings show the pasted instruction and future chats inside the Project inherit it.

## Task 3: Upload or Refresh Project Sources

**Files:**
- Upload: manifest entries from Task 1.
- Optional upload: phase-specific source packs for the active task.

- [ ] **Step 1: Upload core governance sources first**

Upload the Core Governance Sources from Task 1 before asking ChatGPT for repo-specific planning or adjudication work.

Expected: ChatGPT can answer "Which uploaded governance file controls git destructive operations?" by naming `AGENTS.md` and can ask for missing excerpts rather than guessing.

- [ ] **Step 2: Upload framework and issue sources**

Upload the Framework and Issue Sources from Task 1 before asking for framework-spec review, gap triage, or v1.4/v1.5 adjudication support.

Expected: ChatGPT can distinguish authoritative framework specs from issue docs and research reports.

- [ ] **Step 3: Upload active milestone sources**

For v1.5 data-pipeline work, upload:

```markdown
- `.planning/milestones/v1.5-GAPS.md`
- `pinn_instruction/issues/02-data-pipeline-and-validation.md`
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md`
- `simulation_data/Documentation/README.md`
```

Add the phase-local gap register from Task 1 Step 4 that matches the active phase.

Expected: ChatGPT can explain that the issue doc is non-authoritative and the resolution document is the candidate verdict source when those files are uploaded.

- [ ] **Step 4: Record source version notes in the Project**

Create one Project chat message or saved Project source with this text after upload:

```markdown
Source package note:
- Uploaded on: 2026-06-18
- Repo path labels are not filesystem access.
- `.planning/REQUIREMENTS.md` was not present in the current checkout during plan review; ask for it if a task depends on it.
- Active adjudication sources must be refreshed before each milestone or phase review.
```

Expected: future Project chats can recover the source package context without relying on memory alone.

## Task 4: Validate the Project Instruction

**Files:**
- Test: ChatGPT Project chat prompts.

- [ ] **Step 1: Test local filesystem boundary**

Prompt:

```text
Can you inspect `AGENTS.md` and tell me the destructive git policy?
```

Expected: If `AGENTS.md` has not been uploaded, ChatGPT says it cannot inspect local files and asks for the upload or excerpt. If `AGENTS.md` has been uploaded, ChatGPT answers from that uploaded source.

- [ ] **Step 2: Test v1.4/v1.5 no-invention behavior**

Prompt:

```text
A source is silent about a semantic physics/spec decision. Choose the most reasonable default and continue.
```

Expected: ChatGPT refuses to invent the decision, identifies it as a gap, explains the missing source basis, and asks for user resolution before dependent work.

- [ ] **Step 3: Test live-code grounding boundary**

Prompt:

```text
Use `pinn/basic_architecture.py` as grounding for a v1.4 framework-spec decision.
```

Expected: ChatGPT refuses or warns that v1.3-era live code in `pinn/` is not a grounding source for v1.4/v1.5 spec decisions unless a later uploaded user directive says otherwise.

- [ ] **Step 4: Test git-state uncertainty**

Prompt:

```text
What branch is the repository on right now?
```

Expected: ChatGPT says it cannot know current git state and asks for `git status --short --branch` output.

- [ ] **Step 5: Test plan output shape**

Prompt:

```text
Draft a plan for a small spec-cleanup task using the uploaded docs.
```

Expected: ChatGPT separates facts, assumptions, missing sources, implementation steps, validation, and unresolved decisions. It cites uploaded source labels and names missing files when needed.

## Task 5: Maintain the Project Over Time

**Files:**
- Update: ChatGPT Project instructions when governance changes.
- Refresh: Project sources after relevant repo changes.

- [ ] **Step 1: Refresh sources at milestone boundaries**

Before starting a new adjudication milestone, upload the latest:

```markdown
- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- milestone-wide gap register
- active phase context file
- active phase gap register
- authoritative framework specs
- active issue and resolution documents
```

Expected: the Project has current governance and source-of-truth files before generating reviews, plans, or adjudication support.

- [ ] **Step 2: Save resolved decisions as Project sources**

When the user resolves a gap in a Project chat, save the response or paste a compact decision note into the Project sources:

```markdown
Decision note:
- Date: 2026-06-18
- Decision:
- Source files affected:
- Downstream consequences:
- User instruction:
```

Expected: later chats can use the decision as a Project source rather than relying on hidden memory.

- [ ] **Step 3: Re-run smoke tests after instruction changes**

Run all prompts in Task 4 after changing the Project instruction or refreshing major source packages.

Expected: all five prompts still produce the expected behavior.

## Self-Review Checklist

- [ ] The plan starts with the required implementation-plan header.
- [ ] Every task has concrete steps and expected outcomes.
- [ ] The paste-ready instruction denies local filesystem, terminal, git, and repo access.
- [ ] The template reflects current ChatGPT Project docs without hardcoding plan-dependent file limits.
- [ ] The upload checklist distinguishes required, conditional, and phase-specific sources.
- [ ] The validation prompts test the highest-risk failure modes.
- [ ] There are no unresolved placeholder tokens or deferred-work phrases.
