---
status: consumed
purpose: other
created: 2026-06-05
milestone: untracked
phase: git-guidelines
retirement_trigger: milestone complete; superseded by subsequent work
---

# Git Commit Convention Design

**Date**: 2026-06-05
**Status**: Draft — pending user review
**Approach**: Layered Agent Integration (Approach 3)
**Audience**: AI agents (primary committers), user (reviewer/approver)

---

## Context

### Problem Statement

This project has 496 commits over 5.5 months, predominantly authored by AI agents. A forensic analysis surfaced 10 ranked issues:

1. **Scope fragmentation** — 125 distinct scopes, 3+ formats for the same phase (HIGH)
2. **25.8% of subjects exceed 72 chars** — worst is 203 chars (HIGH)
3. **`docs` type is 68.8% of commits** — meaningless as a classifier (MEDIUM-HIGH)
4. **42.1% lack a body** — problematic for auditability (MEDIUM)
5. **Co-Authored-By inconsistent** (37-41%) with 6 model variants (MEDIUM)
6. **Review report add-then-delete churn** (MEDIUM)
7. **Non-atomic cross-domain commits** (LOW)

### Why Now

- Phase 20 introduced project-specific types (`spec`, `evidence`, `verify`, `plan`) organically
- No written commit policy exists — conventions emerged implicitly from agent behavior
- The project is entering deeper execution phases where auditability matters more

### Design Decision

Approach 3 (Layered Agent Integration) was selected because:
- The primary audience is AI agents — rules must be structured and machine-parseable
- Convention violations spike during agent burst sessions
- Decision trees and fixed enumerations work better for agents than prose guidelines

---

## Design

### A. Commit Message Format

```
<type>(<scope>): <imperative-description>

[optional body — 72 char wrap]

[optional footer(s)]
```

**Subject line rules (hard):**

| Rule | Detail |
|------|--------|
| Max length | 72 characters (stretch to 80 if unavoidable; never more) |
| Mood | Imperative: "add", "fix", "record" — never "added", "fixed", "recording" |
| Capitalization | Capitalize first letter after the colon+space |
| Punctuation | No trailing period |
| Formatting | No backticks, quotes, or markdown in the subject |
| Semicolons | No semicolons joining unrelated ideas — split into separate commits |

**Body rules:**

- **Required for**: `spec`, `evidence`, `verify`, `plan` types; any multi-file commit; any governance change; any commit touching `pinn_instruction/`
- **Optional for**: single-file mechanical changes (gitignore, typo fix), trivial `chore` commits
- **Content**: explain **why**, not what (the diff shows what)
- **Spec changes**: reference the grounding source (resolution doc section, issue doc section, user decision)
- **Formatting**: wrap at 72 characters; use bullet lists for multi-point changes

**Footer:**

- `Co-Authored-By:` trailer for all AI-assisted commits
- No other standardized footers required

**Good example:**

```
spec(20): document energy/mass normalization as dataset occupancy facts

ARCH-05: edits to ctl_instruction.md §3.4, bounded by resolution doc §7.2
verdict and Phase 16 D-02-NORM evidence packet. No live-code touches.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

**Bad examples (from actual history):**

```
❌ docs: added a finidng file for addressing sobol sequence ambiguity
   (no type prefix convention, typo, past tense, no scope)

❌ refactor: Consolidate PINN instruction LaTeX sources and generated markdown
   into new `original_latex` and `markdown_conversion` directories...
   (203 chars, backticks in subject, no scope, no body)

❌ wip: milestone v1.3 complete -- pause handoff created
   (wip is not a valid type, oxymoronic "wip" + "complete")
```

### B. Type Taxonomy

#### Type Selection Decision Tree

```
What did this commit do?
│
├─ Edited a framework spec in pinn_instruction/ → spec(N)
├─ Created/updated an evidence packet → evidence(N)
├─ Recorded an audit or verification result → verify(N)
├─ Created/updated an execution plan → plan(N)
│
├─ Added new feature/code → feat(N)
├─ Fixed a bug in code → fix(N)
├─ Restructured code without behavior change → refactor(N)
├─ Added or corrected tests → test(N)
│
├─ Updated planning state, ROADMAP, governance docs → docs(N)
├─ Updated README, docs/ non-spec content → docs(N)
├─ Cleanup, deletion, archival → docs(N) or chore
│
├─ Updated .gitignore, config, dependencies → chore
├─ Updated CI/CD, GitHub Actions → ci
│
└─ None of the above? → Is this a coherent logical change?
   If yes, pick the closest type. If no, split the commit.
```

#### Project-Specific Types

| Type | Meaning | Scope | Body |
|------|---------|-------|------|
| `spec` | Edits to framework specs (`pinn_instruction/`) | Required: phase number | Required: must cite grounding source |
| `evidence` | Creates/updates evidence packets | Required: phase number | Required: must cite sources consulted |
| `verify` | Records audit/verification results | Required: phase number | Required: must state pass/fail and what was checked |
| `plan` | Creates/updates execution plans in `.planning/phases/` | Required: phase number | Recommended |

#### Standard Types

| Type | Meaning | Scope | Body |
|------|---------|-------|------|
| `feat` | New feature or significant code addition | Recommended | Recommended |
| `fix` | Bug fix in code | Recommended | Recommended |
| `refactor` | Code restructuring without behavior change | Recommended | Optional |
| `test` | Adding or correcting tests | Recommended | Optional |
| `docs` | Documentation, planning state, governance | Recommended | When non-trivial |
| `chore` | Maintenance, config, gitignore | Optional | Optional |
| `ci` | CI/CD configuration changes | Optional | Optional |
| `revert` | Reverting a prior commit | Optional | Required: reference reverted hash |

#### Prohibited Types

| Type | Why | Instead |
|------|-----|---------|
| `wip` | WIP means work isn't complete | Commit complete logical steps only |
| `phase` | Ambiguous | Use `plan(N)` or `docs(N)` |
| Ad-hoc types | Not in the enumeration | Pick the closest standard or project-specific type |

#### `docs` Restriction

After this guideline takes effect, `docs` is restricted to:
- Planning state updates (STATE.md, ROADMAP.md)
- Governance document edits (AGENTS.md, CLAUDE.md, .claude/rules/)
- README updates
- General documentation in `docs/`
- Bulk cleanup/deletion/archival
- Any documentation change that doesn't fit `spec`, `evidence`, `verify`, or `plan`

**Not for**: spec edits → `spec`. Evidence → `evidence`. Verification → `verify`. Plans → `plan`.

### C. Scope Convention

#### Three Scope Categories — No Others

| Category | Format | When to use |
|----------|--------|-------------|
| Phase number | `(N)` or `(N-MM)` | During phase execution (default) |
| Domain | Fixed list below | Cross-cutting or non-phase-specific |
| None | Omit `()` | Truly repo-wide changes |

#### Phase Number Scope Rules

- **Format**: `(N)` for phase overall, `(N-MM)` for a specific plan/sub-task
- **N is always two digits**: `(17)`, `(18)`, `(19)`, `(20)` — never `(7)` or `(2)`
- **MM is always two digits**: `(20-01)`, `(20-02)`, `(20-05)`
- **No variants**: Never `(phase-20)`, `(20.5)`, `(phase-20-5)`

#### Domain Scope Enumeration (fixed)

| Scope | Meaning |
|-------|---------|
| `(governance)` | AGENTS.md, CLAUDE.md, .claude/rules/, governance policies |
| `(planning)` | Cross-phase planning: ROADMAP.md, STATE.md, PROJECT.md, REQUIREMENTS.md |
| `(pinn)` | PINN code changes in `pinn/` |
| `(brutus)` | C++ integrator changes in `brutus_Newton-main/` |
| `(pipeline)` | Simulation pipeline changes in `simulation_data/` |
| `(spec)` | Cross-phase spec work not tied to a specific phase |
| `(docs)` | General documentation in `docs/` not tied to a phase |
| `(ref)` | Changes to `reference-code/` |

#### Scope Decision Tree

```
Is this commit part of an active phase execution?
├─ Yes → Phase number scope: (N) or (N-MM)
└─ No → Does it touch one specific domain?
    ├─ Yes → Matching domain scope from fixed list
    └─ No → Is it truly repo-wide?
        ├─ Yes → No scope
        └─ No → Pick the closest domain scope
```

#### Prohibited Scopes

- Session-specific: `(quick-260320-ssi)`, `(EDL)`
- Line numbers: `(line 655)`
- Math expressions: `(1e-4*S_H, user instruction)`
- Model names: `(claude,gemini)`
- Decision IDs: `(D-58)` — belongs in the body
- Any scope not in the phase-number or domain enumeration

### D. AI Attribution

**Rule**: All AI-assisted commits MUST include a `Co-Authored-By:` trailer.

- Use whatever Claude Code generates by default — do not remove or modify it
- The model version in the trailer is useful for forensic tracking — keep it
- For commits where the agent was heavily involved but the user made the final edit: still include the trailer if the agent wrote or suggested any part of the changes
- For purely human-authored commits: no trailer needed

### E. Atomicity & Commit Cadence

**One logical change per commit. Every commit leaves the project in a coherent state.**

**Split when:**
- Subject line cannot concisely describe all changes
- Bundles unrelated features, fixes, or doc updates
- Mixes refactoring with behavior changes
- Touches files in unrelated domains with no causal link

**Combine when:**
- Changes are meaningless without each other
- Changes are causally linked (spec edit + planning-state update)

**Cross-domain commits:**
- Allowed when changes are causally linked
- Scope follows the primary change; mention cross-domain impact in body
- Not allowed when changes are independent

**Cadence:**
- Commit at logical task boundaries
- One commit per plan task or sub-task during phase execution
- No `wip` commits
- No bundling multiple plan tasks unless causally linked

### F. Prohibited Patterns

| Pattern | Why | Instead |
|---------|-----|---------|
| `wip:` commits | Work isn't complete | Commit complete logical steps only |
| Past-tense subjects | "Fixed", "Added" | Imperative: "Fix", "Add" |
| No type prefix | `added a finding file` | Always start with `type(scope):` |
| Ad-hoc scopes | `(quick-260320-ssi)` | Phase number or domain scope |
| Backticks in subject | `` `original_latex` `` | Plain text in subject; detail in body |
| Subject > 80 chars | Truncated in git log | Shorten subject; move detail to body |
| Semicolons joining ideas | `fix(X): do A; also do B` | Split into two commits |
| Lowercase first letter | `docs(20): update plan` | Capitalize: `docs(20): Update plan` |

### G. Gray Areas

#### G1. Review Reports

Review reports in `docs/findings/` should be **committed and kept**, not deleted.
- If superseded: add a "Superseded by..." note at top or move to `docs/findings/archive/`
- Do NOT delete and re-create — this creates churn
- If purely temporary agent working notes: don't commit at all

#### G2. Worktree Agent Merges

- Squash worktree commits if they are fine-grained execution steps
- If the worktree produced a coherent deliverable, merge with a descriptive conventional commit
- The worktree agent ID never appears in the scope

#### G3. Consolidation / Sync Commits

- Use `docs(planning)` scope
- Body must list every change with before/after values
- Hold intentional-level items for user confirmation

#### G4. Evidence → Spec → Verify Sequence

The three-commit pattern is correct:
1. `evidence(N)`: Record the adjudication verdict
2. `spec(N)`: Apply the spec edit
3. `verify(N)`: Confirm the edit passes audits

### H. Tag Strategy

| Category | Format | Example | Type |
|----------|--------|---------|------|
| Milestone completion | `vMAJOR.MINOR.PATCH` | `v1.4.0` | Annotated |
| Phase checkpoint | `vMAJOR.MINOR.PATCH-pre-phase-N` | `v1.4-pre-phase-20` | Annotated |
| Recovery point | `recovery/<context>-<date>` | `recovery/delete-v13-audit-20260521` | Lightweight |
| Baseline | `baseline-<date>` | `baseline-2025-12-20` | Lightweight |

**When to tag:**
- Before each phase: `v1.4-pre-phase-N`
- At milestone completion: `v1.4.0`
- Before destructive operations: `recovery/<context>-<date>`

### I. Branch Lifecycle

| Branch type | Format | Lifecycle |
|-------------|--------|-----------|
| Milestone | `milestone/v1.N` | Long-lived; merge to master at completion |
| Backup | `backup/<context>-<date>` | Convert to tag within 14 days, then delete branch |
| Worktree agent | Auto-generated | Auto-cleaned; must not persist |

### J. Document Structure

**AGENTS.md "Commit Convention" section** (~80-100 lines, always loaded):
- Format rule
- Type decision tree (compact)
- Scope rules
- Subject line rules
- Body requirements
- Co-Authored-By requirement
- Atomicity principle
- Prohibited patterns table

**`.claude/rules/commit-convention.md`** (reference, loaded when relevant):
- Full type definitions with examples
- Complete scope enumeration
- Good/bad commit examples from actual history
- Tag strategy
- Branch lifecycle
- Gray-area guidance
- Enforcement options
- Pre-convention history acknowledgment

### K. Enforcement

Guidelines-only for now. AI agents follow written instructions; the organic convention is already followed ~86% of the time.

Optional future tooling:
- `.gitmessage` template for manual commit message guidance
- `commit-msg` shell hook for regex validation (opt-in, not installed by default)

---

## Implementation Plan

The implementation consists of two deliverables:

1. **AGENTS.md section**: Add a "Commit Convention" section to AGENTS.md
2. **Reference doc**: Create `.claude/rules/commit-convention.md` with the full reference

Both are documentation changes — no code, no tooling, no hooks.

## Pre-Convention History

Commits before approximately 2026-03-16 (the first ~100 commits) do not follow these conventions. They use lowercase, past tense, no type prefix, and no scope. This historical era exists and should not be used as precedent for future commits.

## Sources

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Chris Beams — How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- [Atlassian — Git Commit Tutorial](https://www.atlassian.com/git/tutorials/saving-changes/git-commit)
- [Good Enough Practices in Scientific Computing (Wilson et al.)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5480810/)
- [Conventional Commits for Research — GitHub Discussion #194225](https://github.com/orgs/community/discussions/194225)
- [Fabio Rehm — AI Agent Co-Authored-By debate](https://fabiorehm.com/blog/2026/03/02/our-coding-agent-commits-deserve-better-than-co-authored-by/)
- [git-cliff — Changelog Generator](https://git-cliff.org/)
- [commitlint — Lint Commit Messages](https://github.com/conventional-changelog/commitlint)
