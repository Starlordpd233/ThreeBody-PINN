---
status: active
purpose: runbook
created: 2026-06-10
milestone: v1.5
retirement_trigger: superseded by a later audit runbook revision
---

# Documentation Integrity Audit Runbook

Repeatable milestone-boundary integrity check of project-owned documentation.
Checklist-shaped by design (R12): criteria and pointers only — never duplicate
content from the audited docs into this runbook.

**Origin:** `docs/brainstorms/2026-06-10-doc-integrity-audit-requirements.md` (requirements R1–R13)
**Plan:** `docs/work/plans/cross_cutting/doc-integrity-audit/2026-06-10-doc-integrity-audit-plan.md`
**Reports:** `docs/work/reviews/cross_cutting/doc-integrity-audit/YYYY-MM-DD-doc-integrity-audit-drift-report.md`

## When to Run

- At each milestone boundary (after the closing milestone's spec/process changes land).
- On demand after a repo reorganization or any change that moves or renames doc-referenced paths.

## Doc Inventory

Point-in-time snapshot; docs created after a run are picked up at the next
re-run (update this table first — see Re-run Procedure step 1). `CLAUDE.md`
and `GEMINI.md` are symlinks to `AGENTS.md`, so 15 paths resolve to 13 real files.

| Doc | Class | Treatment | Last verified |
|---|---|---|---|
| `README.md` | 1 — root entry | direct fix | |
| `AGENTS.md` (targets of `CLAUDE.md`, `GEMINI.md` symlinks) | 1 — root entry | direct fix | |
| `ANTIGRAVITY.md` | 1 — root entry | direct fix | |
| `.claude/rules/repo-map.md` | 1 — agent rules | direct fix | |
| `.claude/rules/dataset-reference.md` | 1 — agent rules | direct fix | |
| `.claude/rules/pinn-reference.md` | 1 — agent rules | direct fix | |
| `docs/README.md` | 2 — process | direct fix | |
| `docs/git-guidelines.md` | 2 — process | direct fix | |
| `pinn_instruction/issues/README.md` | 2 — sub-area | direct fix | |
| `pinn_instruction/markdown_conversion/README.md` | 2 — sub-area | direct fix | |
| `tools/spec-render-check/README.md` | 2 — sub-area | direct fix | |
| `simulation_data/Documentation/README.md` | 3 — grounding | report-only, gated | |
| `simulation_data/Data/testing_data/README_TESTING.md` | 3 — grounding | report-only, gated | |

### Class definitions

- **Class 1 — root entry / agent rules.** Loaded into agent sessions; stale content misleads all future work. Drift is fixed directly.
- **Class 2 — process / sub-area.** Governs conventions and sub-area navigation. Drift is fixed directly.
- **Class 3 — grounding.** Feeds adjudication as a designated grounding source. Report-only: no edit without per-finding user sign-off.

### Excluded surfaces (R2)

Never edited by the audit; may be read to cross-check claims in in-scope docs:

- `.planning/` docs (PROJECT.md, ROADMAP.md, phase artifacts, EDL briefs)
- Framework specs (`ctl_instruction.md`, `pinn_architecture.md`) and issue docs
- `sampling_method.md` (frozen by default) and `data_quality_assessment.md` (read-only)
- Vendored third-party READMEs (`brutus_Newton-main/`, `reference-code/`)
- `pinn/` live code

## Verification Checklist

Run the tracks scaled by class. Every check must be recorded so the verdict is
re-derivable (claim, method, result).

### Track 1 — Mechanical checks (all docs; R3)

- [ ] Extract every referenced path, script, and file from the doc.
- [ ] Verify each referenced path exists on disk (`test -f` / `test -d` / `ls`).
- [ ] Resolve internal markdown cross-references (relative links, anchors).
- [ ] Record each broken reference as a finding with the doc line and the actual state on disk.

### Track 2 — Drift detection (Class 1–2 docs; R4)

- [ ] `git log -1 --format='%h %ad' -- <doc-path>` to get the last-touch commit.
- [ ] `git log <last-touch>..HEAD --stat` to enumerate repo changes since.
- [ ] Review the commits for changes that should have updated the doc: moved or renamed paths, new or removed scripts, structural or convention changes, new directories.
- [ ] Record each missed update as a finding citing the commit that introduced the change.

### Track 3 — Content verification (Class 3 docs; R5)

- [ ] Enumerate the doc's factual claims about the dataset (counts, schemas, parameters, paths, procedures).
- [ ] Spot-verify a sample against on-disk `simulation_data/` and `simulation_data/Scripts/`: directory listings, file counts, CSV headers, script argument signatures. Sampling-based, not exhaustive — the dataset is frozen.
- [ ] Record each check re-derivably: claim, verification method, result (verified / contradicted with evidence / not-verifiable with reason).

### Agent-entry consistency (R6)

- [ ] Read `AGENTS.md` and `ANTIGRAVITY.md` side by side; flag contradictory guidance.
- [ ] Verify `CLAUDE.md` and `GEMINI.md` are intact symlinks to `AGENTS.md` (`ls -la`).

## Verdicts and Reporting (R1, R13)

- Every inventory doc receives exactly one verdict: **verified-current** (with checks listed), **drift-found** (with itemized findings and evidence), or **not-verifiable** (with reason).
- The drift report is a dated, committed review artifact at the Reports path above, with frontmatter per `docs/README.md` (`purpose: review-findings`).
- The report commit is separate from any fix commits.

## Drift Handling

- **Class 1–2 (R7):** fix directly. Each fix traces to a report finding ID; commits are atomic and follow `docs/git-guidelines.md`. If a finding requires substantial rewriting rather than a targeted correction, flag it for user review instead of rewriting unilaterally.
- **Class 3 (R8, R9):** report-only. Where direct observation of on-disk data settles the correct content, propose a specific edit with evidence. Where it cannot, surface the finding as a question — never invent content. No grounding-doc edit without explicit user sign-off on that finding.
- **Adjudication coordination (R10):** if an adjudication milestone is in flight, flag any Class 3 finding that could affect its inputs before the consuming work product is finalized; if the audit cannot meet that deadline, notify the user to hold finalization.

## Re-run Procedure

1. **Refresh the inventory.** Add any new project-owned docs to the table with a class assignment; remove retired docs (per the `docs/README.md` lifecycle); confirm the symlink note still holds.
2. **Run the checklist.** Track 1 on all docs; Track 2 on Class 1–2; Track 3 on Class 3; agent-entry consistency check.
3. **Compose the drift report.** Dated filename at the Reports path; per-doc verdicts; commit the report on its own.
4. **Apply Class 1–2 fixes.** One commit per finding or logical group, referencing finding IDs; re-run the relevant Track 1 checks on fixed docs.
5. **Gate Class 3 findings.** Present each to the user with evidence; apply edits only after sign-off, each in its own commit.
6. **Stamp the inventory.** Fill the `Last verified` column with the audit date for every doc that received a verdict; commit the runbook update.
