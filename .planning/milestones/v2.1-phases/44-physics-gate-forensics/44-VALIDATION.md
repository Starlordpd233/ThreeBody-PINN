---
phase: 44
slug: physics-gate-forensics
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-23
---

# Phase 44 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `44-RESEARCH.md` § "Validation Architecture" (lines 360–402).

**Phase shape caveat.** Phase 44 produces **analysis artifacts** — Python scripts, their JSON/markdown
outputs, and a pinning manifest — not application code. There is no application under test and no
conventional test suite. Validation here means two things, and only these two:

1. Every number quoted in `44-DIAGNOSIS.md` can be **mechanically regenerated** from pinned inputs (D-02).
2. Each script **self-checks its own output shape and fails closed** before writing anything.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — no test framework is installed or needed; the embedded self-check assertions in each analysis script ARE the test surface |
| **Config file** | none |
| **Interpreter** | `~/miniforge3/envs/pinn-train/bin/python3` (Python 3.11.15, numpy 2.4.6, tensorboard 2.21.0) — **not** bare `python3` on PATH (system 3.14.6, which has neither package) |
| **Quick run command** | `~/miniforge3/envs/pinn-train/bin/python3 .planning/phases/44-physics-gate-forensics/evidence/<diag>/<script>.py` (each script asserts, then writes) |
| **Full suite command** | re-run all retained analysis scripts end-to-end against `evidence/manifest.json` and confirm every SHA-256 still matches |
| **Estimated runtime** | seconds — inputs are 4 × 300-line JSONL logs plus one 183 KB `metrics.json` |

---

## Sampling Rate

- **After every task commit:** run that task's script; its self-check assertions must pass (fail-closed).
- **After every plan wave:** re-run all scripts produced so far against `evidence/manifest.json`; every input SHA-256 must still match.
- **Before `/gsd-verify-work`:** every number cited in `44-DIAGNOSIS.md` must trace to a script output file, not a hand-transcribed value.
- **Max feedback latency:** < 30 seconds (all inputs are small, frozen, local files).

---

## Per-Task Verification Map

Seeded as draft — task IDs are assigned when `44-NN-PLAN.md` files are written. The planner MUST give
every analysis task an automated `<verify>` that runs the task's own script and exercises its assertions.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 44-NN-NN | NN | — | DIAG-01 | — | N/A | self-check | `<env python> evidence/diag01/<script>.py` | ❌ W0 | ⬜ pending |
| 44-NN-NN | NN | — | DIAG-02 | — | N/A | self-check | `<env python> evidence/diag02/<script>.py` | ❌ W0 | ⬜ pending |
| 44-NN-NN | NN | — | DIAG-03 | — | N/A | self-check | `<env python> evidence/diag03/<script>.py` | ❌ W0 | ⬜ pending |
| 44-NN-NN | NN | — | DIAG-04 | — | N/A | manual/review | citation trace (see Manual-Only below) | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `.planning/phases/44-physics-gate-forensics/evidence/` — evidence directory (D-01); does not exist yet
- [ ] `evidence/manifest.json` — input pinning manifest: SHA-256 of every input file + `git rev-parse HEAD` (D-02); created by the first analysis task
- [ ] No test framework install required — analysis scripts self-check

---

## Baseline self-check assertions

Every script that touches these inputs must embed the applicable assertions and halt on failure rather
than write an unverified number (source: `44-RESEARCH.md` §Validation Architecture):

```python
assert len(per_trajectory) == 1500
assert max(e["eps_h"] for e in per_trajectory) == metrics_json["eps_h"]   # re-verifies D-07's own premise every run
assert set().union(*(e.keys() for e in per_trajectory)) == {"eps_h", "fidelity", "id", "variant"}
assert len(train_log_records) == 300
assert {r["step"] for r in train_log_records} == set(range(1, 301))
```

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The D-07 gap entry faithfully represents the evidentiary trail | DIAG-04 | Semantics, not re-derivability — no script can validate whether `max` is the spec-intended gate statistic; sources are silent | Read the `44-GAPS.md` entry against `44-RESEARCH.md` §C; confirm every cited file:line quote is accurate and that the entry decides nothing |
| Ranked hypotheses are honestly evidenced | DIAG-04 | Causal correctness is unknowable in-phase; SCOPE-23 forbids the discriminating runs | Confirm each ranked cause carries supporting AND contradicting citations plus a named-but-unexecuted discriminating test |
| Remedy-abstinence is explicit | DIAG-04 | Prose obligation (SCOPE-26), not a computable property | Confirm `44-DIAGNOSIS.md` states abstinence in its own words and recommends no remedy |
| Seed-dependent-split caveat is stated | DIAG-03 | Cannot be quantified without re-partitioning/re-evaluating (out of scope) | Confirm DIAG-03 states that per-seed comparisons span *different* held-out populations |

---

## Explicitly NOT validatable in-phase

Carried from `44-RESEARCH.md` so the verifier does not later mistake these for gaps:

- Whether `max` is the spec-intended gate statistic (D-07) — routed to the gap register, not resolvable.
- Whether the DIAG-04 hypothesis ranking is causally correct — discriminating tests are proposed, never run (SCOPE-23).
- Whether TensorBoard `residuals/bin_*` series would change DIAG-02's conclusions — not computed in this phase.
- How much the seed-dependent split shifts the DIAG-03 interpretation — surfacing the caveat is in scope; quantifying it is not.

---

## Validation Sign-Off

- [ ] All analysis tasks have an automated `<verify>` that runs the script and exercises its assertions
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers the evidence dir + manifest
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
