---
phase: 23
slug: research-package-assembly
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-10
---

# Phase 23 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Phase 23 ships **documents, not code** — there is no test framework, no pytest/runtime suite.
> The acceptance checks are structural completeness checks on the deliverables, executed by
> inspection (`diff`, `git hash-object`, `grep -c`, file-existence, `gsd-tools state json`) and,
> for the D-07 consolidation gate, by user sign-off.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — documentation-assembly phase; verification is checklist/grep/diff-based |
| **Config file** | none (no framework to install; Wave 0 not applicable) |
| **Quick run command** | per-task `<automated>` check (each is a `grep -c` / `diff -q` / `test -f` one-liner, runs in <2s) |
| **Full suite command** | run every task's `<automated>` check in sequence + `git diff --quiet -- pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` (and the frozen specs) |
| **Estimated runtime** | ~5 seconds total |

---

## Sampling Rate

- **After every task commit:** Run that task's `<automated>` check.
- **After every plan wave:** Re-run the wave's task checks plus `git hash-object` byte-identity on any snapshot created so far.
- **Before `/gsd-verify-work`:** Every task's acceptance check passes; `git diff --quiet` on `data_quality_assessment.md`, `sampling_method.md`, `ctl_instruction.md`, `pinn_architecture.md` (no spec edits this phase) exits 0.
- **Max feedback latency:** ~5 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 23-01-01 | 01 | 1 | PKG-04 | T-23-01-T | DQA byte-unchanged (read-only, SCOPE-09) | structural | `test -f 23-DQA-CHARACTERIZATION.md && git diff --quiet -- pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` | ✅ | ⬜ pending |
| 23-01-02 | 01 | 1 | PKG-03 | T-23-01-INT | No unverified figure stated as fact (D-13) | structural | `grep -cE '\|\s*CLM-[0-9]+' 23-CLAIMS-INVENTORY.md` (>=13) | ✅ | ⬜ pending |
| 23-01-03 | 01 | 1 | PKG-01 (prep) | T-23-01-I | No package dir created pre-gate | structural | `test -f 23-CONSOLIDATION-PLAN.md && test ! -d .../research_package` | ✅ | ⬜ pending |
| 23-02-01 | 02 | 2 | PKG-01 | T-23-02-E | User decides inclusion, agent records | manual + structural | `grep -c 'APPROVED' 23-CONSOLIDATION-PLAN.md` (>=1) | ✅ | ⬜ pending |
| 23-03-01 | 03 | 3 | PKG-01 | T-23-03-T | Specs byte-for-byte; no `pinn/` content | structural | `diff -q .../specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (exit 0) | ✅ | ⬜ pending |
| 23-03-02 | 03 | 3 | PKG-03 | T-23-03-INT | Package claims table = canonical register | structural | `grep -cE '\|\s*CLM-[0-9]+' .../research_package/claims-table.md` (== inventory count) | ✅ | ⬜ pending |
| 23-03-03 | 03 | 3 | PKG-01 (D-05) | T-23-03-I | Figures CLM-referenced; no `pinn/`/spec | structural | `grep -cE 'CLM-[0-9]+' .../research_package/consolidated-context.md` (>=1) + `grep -c 'data-processing-pipeline'` (==0) | ✅ | ⬜ pending |
| 23-04-01 | 04 | 4 | PKG-02 | T-23-04-INT | SCS gate cited to DQA only (Pitfall 1) | structural | `grep -cE '14D\|Jacobi\|COM\|PHYS-03\|SCS\|PHYS-01' .../framed-research-questions.md` (>=6) | ✅ | ⬜ pending |
| 23-04-02 | 04 | 4 | PKG-02 | T-23-04-E | No question presupposes a resolution | structural + manual | `grep -cE 'B-06\|B-11\|M11\|M12\|M13\|D7\|SCS\|SASD\|IPR\|PSC' .../framed-research-questions.md` (>=10) | ✅ | ⬜ pending |
| 23-05-01 | 05 | 5 | PKG-01 | T-23-05-I | Manifest self-contained, no dangling paths | structural | `grep -cE '[0-9a-f]{7,40}' .../research_package/README.md` (>= snapshot count) + `grep -cE '\]\(\.\./\|\]\(/Users\|\]\(pinn/' README.md` (==0) | ✅ | ⬜ pending |
| 23-05-02 | 05 | 5 | PKG-01 (D-16/D-17) | T-23-05-T | STATE mutated via handlers only | structural | `grep -c 'research_reports/02-data-pipeline-and-validation' .../DELIVERY-NOTE.md` (>=1) + `gsd-tools state json` shows gate decision + blocker | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* No test infrastructure is required for a
documentation-assembly phase — the "checks" above are inspection-based deliverable audits
(`diff`, `git hash-object`, `grep -c`, `test -f`, `gsd-tools state json`), not automated unit tests.
No framework install, no fixtures, no stubs.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-07 consolidation gate: user approves the final document list + the two inclusion calls | PKG-01 | The inclusion decisions (ship `sampling_method.md`? ship `data_quality_assessment.md`?) are reserved to the user by D-07; the agent records, does not decide | Present `23-CONSOLIDATION-PLAN.md`; user replies with one of the Plan 02 options; agent appends the APPROVED record (the `grep -c APPROVED` check then confirms it landed) |
| Every inline figure references a CLM ID (no bare figure stated as fact) | PKG-03 | Negative-space check — `grep` confirms CLM presence but a human scan confirms no figure was stated without one | Scan `framed-research-questions.md` and `consolidated-context.md` against the D-12 figure list; each numeric figure must carry a CLM-NN reference (Pitfall 3) |
| No issue-doc imperative ("Implement…/Use…") carried without a "the issue doc proposes" qualifier | PKG-02 | Tone/framing judgment not fully grep-expressible | Scan each question block in `framed-research-questions.md`; every proposal prefixed as non-authoritative (Pitfall 2) |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (every task carries a `grep`/`diff`/`test`/`gsd-tools` check; no framework/Wave 0 needed)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify (every task has one)
- [x] Wave 0 covers all MISSING references (none — no test infrastructure required)
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-06-10
