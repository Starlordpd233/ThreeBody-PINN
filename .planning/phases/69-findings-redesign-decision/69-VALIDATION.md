---
phase: "69"
slug: "findings-redesign-decision"
status: draft
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-08"
---

Planning verification passed on 2026-11-08. The independent checker accepted
all three plan structures, three requirements, 12 decisions, 14 resolved edges
and three judgment prohibitions. Its research-status blocker was corrected
with explicit planning dispositions and independently rechecked. The canonical
failure-direction probe checked 17 commands with no findings. The path probe
reported `not_applicable`, not proof that the proposed checks already run.
The post-planning coverage gate passed all 15 requirement/decision items.
Plans 69-01 and 69-02 are complete. The findings and reviewed packet are ready
for the reserved owner checkpoint in Plan 69-03.

# Phase 69 validation strategy

## Test infrastructure

Use the existing standard-library unittest framework. The reporting verifier
is phase-specific and reads committed evidence without training or corpus access.
No dependency installation is needed.

- Quick command after evidence changes: `<home>/miniforge3/envs/pinn-train/bin/python -B .planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py all`
- Focused suite before each wave closes: `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase69 -t .`
- Existing integration check: `<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.diagnostic_phase67 audit-phase --json`

The verifier and test paths now exist. The parent reran the 31 focused tests
successfully in 16.206 seconds and the combined verifier returned every success
marker. This is implementation validation, not approval of an owner decision.
The task map below follows the three serial plans, 69-01 through 69-03.
Run checks after each substantive evidence/report change and at the final state.
Record observed latency during execution rather than asserting a duration now.

## Per-task verification map

All commands run from the trainex repository root. The interpreter in every
Python command is `<home>/miniforge3/envs/pinn-train/bin/python -B`.
The checker path is
`.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py`.
New commands become usable only after their implementing task completes.

| Plan/task | Wave | Requirement | Automated verification | Observable rejection signal | Judgment or checkpoint | Current status |
|---|---|---|---|---|---|---|
| 69-01.1, matched 1632/42 tracer | 1 | VERD-01 | `-m unittest tests.phase69.test_verifier_phase69.SourceTracerTests`; checker `sources` | Nonzero exit, zero tests, accepted corrupt digest/case, or missing `PHASE69-SOURCES-OK` | Historical publication registration differs legitimately from later pins | Passed, 31-test focused suite |
| 69-01.2, complete inventory and cost | 1 | VERD-01 | `-m unittest tests.phase69.test_verifier_phase69.IdentityAndCostTests`; checker `sources` and `cost` | Nonzero exit, accepted swapped identity/duplicate expense/missing-as-zero, or missing success marker | Preserve all registered readings and explicit unknown-cost coverage | Passed, 31-test focused suite |
| 69-01.3, dynamic mapping and focused suite | 1 | VER-23 | `-m unittest discover -s tests/phase69 -t .`; checker `all`; existing `-m pinn.verification.diagnostic_phase67 audit-phase --json` | Nonzero exit, zero tests, missing constituent/`PHASE69-ALL-OK`, nonempty problems, or invalid mapping accepted | Mapping is separate from satisfaction | Passed, 31-test focused suite |
| 69-02.1, findings and linked detail | 2 | VERD-01 | Checker `all` | Nonzero exit or missing constituent/`PHASE69-ALL-OK` | Review every conclusion, adverse result, prediction, recipe limit and cost claim against sources | Passed, 63 fit rows, 15 contrasts, 12 yardstick rows and 131 ledger activities checked |
| 69-02.2, reviewed closing packet | 2 | VERD-01, VERD-02 | Checker `all`; `shasum -a 256` on findings, evidence detail, accounting and evidence JSON | Nonzero exit, missing success/hash line, or digest differs from packet entry | Record all three scientific/authority prohibition judgments; keep choices pending | Passed, four component digests and three judgments recorded in 69-CHECKPOINT.md |
| 69-03.1, actual owner checkpoint | 3 | VERD-02 | Checker `all`; five-file hash check including checkpoint | Nonzero exit, missing success/hash line, or presented packet changed | `checkpoint:human-verify`, `gate="blocking-human"`; actual reply or explicit owner-open instruction required | Pending owner checkpoint |
| 69-03.2, verbatim ruling and handoff | 3 | VERD-02 | Checker `all` | Nonzero exit or missing constituent/`PHASE69-ALL-OK` | Compare actual owner words character for character; inspect authority, open choices and handoff obligations | Pending owner checkpoint |
| 69-03.3, final live reread | 3 | VER-23 | Checker `traceability` and `all`; `-m unittest discover -s tests/phase69 -t .` | Nonzero exit, zero tests, empty/unequal IDs, mapping anomalies, missing phase, missing success marker or stale final source hashes | Confirm actual reply/open disposition and recorded prohibition judgments | Pending final state |

Dependency order is `69-01 -> 69-02 -> 69-03`. Every task has an automated
command and an adjacent `fails_when` in its plan. All 14 SPEC edge rows are
lifted into plan truths; the three prohibitions retain `verification: judgment`.
The owner checkpoint cannot be auto-approved or replaced by test output.
Re-run final traceability after any approved requirement/mapping change and
after final Git coordination. Derive the count dynamically; 13 is orientation.

## Wave 0 requirements

- Create the small phase-specific verifier and focused tests before relying on
  its checks. Cover shuffled case/row order, duplicate or missing identities,
  empty inventories, missing phases, duplicate control accounting, unknown
  duration and altered source digest. Do not test for mere prose presence.
- Keep scientific interpretation and owner decisions outside automatic approval.

## Manual-only verification

- Review causal limits, prediction fidelity, completeness of adverse results,
  one-page readability and every scientific/authority prohibition from SPEC.
- Present the completed packet before asking the owner for v2.6 direction and
  trainex-r5 commission/question. Bind the reply to that packet's exact identity.
- Missing or partial replies remain pending or explicitly open. They cannot be
  discharged by a passing reporting test or preparatory approval.

## Validation sign-off

- [x] Final checked plans have per-task automated commands and failure signals.
- [x] Focused false-evidence tests pass and the checker rejects invalid inputs.
- [x] Source/result/cost checks pass on the packet prepared for presentation.
- [ ] Final live traceability check passes after any owner-approved changes.
- [x] Scientific judgment review is recorded against actual findings.
- [ ] Owner checkpoint is answered or choices explicitly left open by the owner.
- [ ] Observed runtimes and final validation status are recorded.

Planning and execution commits follow the repository's atomic task-end policy.
This draft does not assert phase completion or owner approval.
