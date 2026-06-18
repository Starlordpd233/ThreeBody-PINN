---
phase: 30
slug: research-package-assembly
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-18
---

# Phase 30 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **Phase nature:** documentation-assembly (specwork). This phase writes Markdown/text
> artifacts and takes read-only snapshots — it runs no code and ships no test framework.
> "Validation" here is **acceptance-check sweeps + hash verification**, not a unit-test
> suite. Source: `30-RESEARCH.md` § "Validation Architecture" / § "Acceptance Criteria".

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — documentation-assembly phase; no executable code produced |
| **Config file** | none |
| **Quick run command** | `grep -RInE '(pinn_instruction\|\.planning\|simulation_data\|framework-specs\|pinn/)' <package>/RESEARCH-CONTEXT-MASTER.md <package>/RESEARCH-AGENT-PROMPT.md` → expect zero hits (repo-path leak sweep, ERW rule 1 / D-05) |
| **Full suite command** | per-file SHA-256 compare vs source for every `specs/` snapshot + `git diff --quiet <read-only file>` for the two PKG-08 reports + coverage checklist sweep |
| **Estimated runtime** | ~seconds (greps + hashing) |

---

## Sampling Rate

- **After every task commit:** run the repo-path-leak grep on any authored upload touched, and `git diff --quiet` on any read-only source touched.
- **After every plan wave:** run the full acceptance-check sweep (path-leak grep + snapshot SHA-256 compare + read-only `git diff --quiet` + figure→CLM coverage sweep).
- **Before delivery (30-05):** every acceptance check below must pass.
- **Max feedback latency:** seconds.

---

## Per-Task Verification Map

> The planner derives per-task acceptance criteria into the PLAN.md files; the checks below
> are the standing acceptance sweeps each plan's tasks map onto (from `30-SPEC.md` AC and
> `30-RESEARCH.md` § Validation Architecture). Test Type is "doc-sweep" / "hash" — not unit.

| Check ID | Requirement | Verifies | Method | Pass criterion |
|----------|-------------|----------|--------|----------------|
| VC-01 | PKG-05/06 (uploads) | zero repo paths in any authored upload | `grep -RInE '(pinn_instruction\|\.planning\|simulation_data\|framework-specs\|pinn/)'` on master + prompt | zero hits |
| VC-02 | PKG-05 | `specs/` snapshots byte-for-byte intact | per-file SHA-256 in `30-SNAPSHOT-HASHES.txt` vs source-commit blob | hashes match |
| VC-03 | PKG-08 | the two reports unchanged (read-only) | `git diff --quiet <report>` after characterization | exit 0 |
| VC-04 | PKG-07 | every dataset/empirical figure registered | sweep: each numeric figure in the master references a `CLM-` ID | no unregistered figure |
| VC-05 | PKG-07 | no-in-milestone-verification boundary stated | inspect claims register for the D-17 boundary statement | present |
| VC-06 | PKG-06 | SCOPE-12 hard-constraints preamble verbatim | diff preamble vs the SCOPE-12 constraint list | exact match |
| VC-07 | PKG-06 | coverage ≥ selected finding set | checklist: B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12/13/18, D-04, D-05, D-06, `D=6.694` each has a question | all present |
| VC-08 | PKG-06 | D-04/D-05/D-06 + `D` conflict unsettled | inspect each — states both positions, presupposes no verdict | no presupposed resolution |
| VC-09 | delivery | `DELIVERY-NOTE.md` has landing path + gate semantics | inspect note | exact result-landing path + "Phases 32–36 gate on doc landing AND Phase 31" |
| VC-10 | delivery | gate-open recorded via gsd-tools only | STATE.md changed only through a handler (no direct Write/Edit) | no direct STATE.md edit in the diff |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky — all VC-* are ⬜ pending until execution.*

---

## Wave 0 Requirements

- Existing infrastructure covers all phase requirements — no test framework to install. The
  standing evidence artifact is `30-SNAPSHOT-HASHES.txt` (created in 30-01/30-03), plus the
  greppable acceptance sweeps above. No Wave-0 test stubs.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Consolidation plan ratified before assembly | PKG-05 (D-09) | A hard user checkpoint — the user must approve what consolidates vs ships standalone before snapshots are assembled | Present `30-CONSOLIDATION-PLAN.md` with its open inclusion calls; obtain a recorded sign-off block before 30-03 begins |
| Recovery-tag re-cut approved | constraint (CONTEXT line 145) | `git tag -f v1.6-pre-phase-30` is a destructive ref move requiring explicit user approval per the destructive-git governance | Surface the orphaned-tag state (tag → 85f72f88, not an ancestor of HEAD); obtain approval to re-cut, OR cut a fresh distinctly-named tag, before the first phase commit |

---

## Validation Sign-Off

- [ ] All tasks map to a VC-* acceptance check or a manual verification above
- [ ] Sampling continuity: no plan wave closes without its acceptance sweep run
- [ ] No Wave 0 test stubs needed (no framework)
- [ ] No watch-mode flags (N/A — no test runner)
- [ ] Feedback latency < ~10s (greps + hashing)
- [ ] `nyquist_compliant: true` set in frontmatter once the planner confirms every task carries a VC-* / manual mapping

**Approval:** pending
