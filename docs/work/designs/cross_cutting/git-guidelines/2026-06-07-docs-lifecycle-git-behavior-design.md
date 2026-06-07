---
status: active
purpose: design
created: 2026-06-07
milestone: cross_cutting
phase: git-guidelines
retirement_trigger: guideline edits applied across all governance surfaces and accepted
---

# Docs Lifecycle Git Behavior — Design

Committed to its canonical home under `docs/work/designs/` per `docs/README.md`.
It records the design for three sets of additions to the project Git policy and how they
propagate across every agent-governance surface.

## Problem

1. A prior plan-split execution conflated a pre-existing uncommitted remediation with the
   split transformation in a single commit, destroying the clean baseline needed to verify
   byte-for-byte preservation after the fact. The verification claim survived only as prose
   in a commit message, not as re-derivable committed evidence.
2. The `docs/` directory became messy because agents running the recurring
   plan -> review -> fix-plan -> remediation loop had no Git commit behavior rules for that
   loop: no execution-provenance marker, no report retention discipline, and no separation
   between "what a reviewer found" and "what a reviewer changed."

## Scope

Three additions to the canonical Git policy, propagated to all governance surfaces:

- **Addition A — Baseline Before Transformation** (general).
- **Addition B — Auditable Verification Claims** (general).
- **Part 2 — `docs/` Plan-Review-Fix lifecycle** (docs-specific commit behavior).

Out of scope: the `docs/` *file* lifecycle (retention, naming, archive, deletion, closeout).
That is already owned by `docs/README.md`. This design defers to it and only adds the Git
*commit-behavior* layer, cross-referencing where the two meet.

## Decisions (resolved with user)

- **Execution marker form:** extend the `docs/README.md` frontmatter schema with
  execution-provenance keys rather than a separate blockquote stamp. One metadata block per
  file. Legacy plans without frontmatter use the short top-note `docs/README.md` already permits.
- **Marker fields:** `executed_at` carries date **and time with timezone**; agent/model
  identity is NOT recorded in the file stamp (it belongs in the mandatory commit attribution
  trailer, not the document body).
- **Report retention:** defer entirely to `docs/README.md`. Do **not** use `previous_reports/`
  (banned by `docs/README.md`). Superseding marks the old report `status: superseded` in
  frontmatter; archive/deletion follows the README's approval-gated lifecycle.
- **ANTIGRAVITY.md:** full parity — mirror the entire Git Commit Protocol block (it currently
  has none).
- **Spec location:** `docs_temp/` staging (untracked, uncommitted).

## Part 1 — General additions (already applied to docs/git-guidelines.md and AGENTS.md)

### A. Baseline Before Transformation

Before a bulk or mechanical transformation on a file that already carries uncommitted changes
(split, reformat, large find-and-replace), first commit or stash the pre-existing changes as
their own atomic unit. Never fold unrelated prior edits into the transformation commit:
conflating two logically distinct changes destroys the clean pre-transformation baseline that
later content-preservation checks depend on.

### B. Auditable Verification Claims

When a commit asserts a verifiable invariant (byte-for-byte preservation, hash match, line or
unit counts), record the supporting evidence durably, not in ephemeral locations such as
`/tmp`. Commit the per-unit hashes or counts alongside the change, or reference them from a
committed path, so a later reviewer can re-derive the claim from committed state instead of
trusting the commit message alone.

## Part 2 — `docs/` Plan-Review-Fix lifecycle (new section in docs/git-guidelines.md)

Governs Git behavior for the iterative loop run on implementation plans and review reports
under `docs/`: plan execution -> independent review -> fix-plan -> remediation. **Rules attach
to the action performed, not to which agent performs it.** One agent may perform several
actions; each follows its own rule and gets its own commit. File retention, naming, archive,
and review closeout are governed by `docs/README.md`; this section governs only commit behavior.

### A. Executing a plan

- Commit the executed work as normal typed commits by domain.
- Record execution provenance in the plan file's frontmatter (see `docs/README.md` schema):
  `execution_status`, `executed_at` (date + time + timezone), `review_status: pending`.
  Legacy plans without frontmatter use the short top-note `docs/README.md` permits.
- **Close each pass with a dedicated commit** that updates those frontmatter keys and carries
  trailers `Plan-Execution: first-pass` and `Plan-Source: <plan path>`, plus the mandatory
  `Agent-Assisted-By:` / `Co-Authored-By:` trailer. This commit is separate from the work
  commits (it touches the plan file, a different path/domain than the executed work).
- Re-executing after remediation uses `execution_status: remediation-pass-N-complete` and
  trailer `Plan-Execution: remediation-pass-N`.
- Do not fold pre-existing uncommitted changes into execution commits (Part 1 A).

### B. Reviewing an execution and writing a report

- A review report is committed and kept — never deleted-and-recreated. Type `verify(<scope>)`
  when it judges whether execution was correct, complete, and accurate; `docs(<scope>)` only
  for non-finding narrative notes. A body is required for `verify`.
- Naming and location follow `docs/README.md` (dated filename; `docs/work/reviews/...` in the
  target structure, or the existing legacy path only when completing already-started work).
- Superseding an older report sets its frontmatter `status: superseded` in an atomic commit;
  the new report is its own commit. Any archive move or deletion follows the README's
  approval-gated lifecycle (finding-by-finding closeout) and is committed atomically when approved.
- If the reviewing agent also finishes or fixes work, the report is committed **separately**
  from the fixes — findings in one commit, changes in their own atomic commits. Never combine
  a review report with the fixes it motivates.
- After review, update the plan's frontmatter `review_status: reviewed` with a pointer to the report.

### C. Authoring a fix / remediation plan

- A plan written to address review findings is its own `plan(<scope>)` commit, separate from
  any execution or report commit. Location follows `docs/README.md`.
- When later executed, it follows section A with a `remediation-pass-N` marker.

### D. Applying fixes

- Apply fixes as normal typed commits by domain, separate from the report that identified them
  and the plan that scheduled them.

## Part 3 — docs/README.md frontmatter schema extension

Add three optional execution-provenance keys to the "Lifecycle Metadata" block, set by the
Part 2 marker rule:

- `execution_status`: `not-executed` (default; may be omitted) | `first-pass-complete` |
  `remediation-pass-N-complete`
- `executed_at`: timestamp of the latest execution pass, date + time + timezone
- `review_status`: `none` (default) | `pending` | `reviewed`

These describe execution provenance and are orthogonal to the retention `status` key
(`active`/`consumed`/`superseded`/`archived`/`retained`). Add a short "Commit behavior"
pointer in `docs/README.md` to `docs/git-guidelines.md` for the commit-side rules.

## Part 4 — Governance-surface propagation

| Surface | Action |
|---|---|
| `docs/git-guidelines.md` | Canonical. Part 1 (A, B) applied; add Part 2 section. |
| `AGENTS.md` | Condensed mirror. Part 1 applied; add docs-lifecycle bullets. |
| `CLAUDE.md` | Symlink -> `AGENTS.md`. Covered automatically; no separate edit. |
| `GEMINI.md` | Symlink -> `AGENTS.md`. Covered automatically; no separate edit. |
| `ANTIGRAVITY.md` | Separate regular file with no git protocol. Add full-parity protocol block (Part 1 + Part 2 summary + pointer to canonical). |
| `docs/README.md` | Add Part 3 frontmatter keys + a commit-behavior cross-ref pointer. |
| `.planning/codebase/CONVENTIONS.md` | Descriptive map, currently stale (says `commit-msg` not installed). Not a rule surface; leave for codebase-map regeneration. |
| Enforcement (`scripts/git_policy/`, `.githooks/`) | No change. New rules are behavioral, not hook-enforceable. Verified custom trailers and `verify` type are not rejected by the existing validators. |
| Project memory | Not used. Claude-local, per-user, uncommitted; invisible to Gemini/Antigravity/Cursor, so unsuitable for shared enforceable policy. |

## Enforcement compatibility (verified)

- `validate_commit_msg.py` has no trailer allowlist; it only *requires* an
  `Agent-Assisted-By:`/`Co-Authored-By:` trailer on agent commits. Custom `Plan-Execution:` /
  `Plan-Source:` trailers pass through.
- `validate_staged_paths.py` does not map commit types to paths, so `verify(<scope>)` on a
  report under `docs/` is accepted; it only blocks scratch artifacts and >10 MiB blobs.
