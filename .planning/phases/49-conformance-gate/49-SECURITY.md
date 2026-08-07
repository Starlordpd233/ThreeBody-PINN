---
phase: 49
slug: conformance-gate
status: verified
# threats_open counts OPEN threats at or above workflow.security_block_on.
threats_open: 0
asvs_level: 1
block_on: high
register_authored_at_plan_time: true
created: 2026-08-07
---

# Phase 49 — Security

> ASVS L1 verification of the threat registers authored in Plans 49-01 through
> 49-06. This internal training-pipeline phase adds no network, authentication,
> external-service, or dependency-install surface.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| operator YAML → configuration | Untyped operator configuration enters fail-closed dataclass parsing | scheduler caps, invariant window, run settings |
| controller state → guards | Per-step causal statistics enter the conformance guard path | `w_n_stats`, collocation count, physics-evaluated flag |
| persisted checkpoint → resume | Serialized state is restored into live invariant-B state | schema version, high-water mark, last-advance step |
| committed register → preflight | Register bytes become run caveats and eligibility evidence | divergence entries, proof-test references, waivers |
| census producers → verdict | Runtime producer values satisfy the manifest used by preflight | resident/batch/model/collocation/anchor/loss facts |
| persisted preflight → summary | Validated artifact bytes become the terminal run record | checks, findings, divergences, eligibility inputs |
| owner ruling → shipped state | The owner checkpoint becomes enforced configuration and register state | `N = 500`, closed `INV-B-N-UNSET` entry |

---

## Threat Register

The historical plans reused phase-level IDs such as `T-49-01`. This aggregate
qualifies each reference with its plan number to preserve every authored row
without rewriting the source plans or conflating different components.

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| 49-01/T-49-01 | Repudiation | table assertion / preflight checks | high | mitigate | D-16 pass/trip matrix in `test_gate01_table.py`, including artifact-first refusal | closed |
| 49-01/T-49-03 | Tampering | `preflight.json` path and bytes | medium | mitigate | fixed filename under `run_dir`, atomic writer, fail-closed loader and integrity tests | closed |
| 49-02/T-49-01 | Repudiation | invariant A/B and missing-stat guards | high | mitigate | every guard has a driving HALT test; missing stats on a physics step also HALT | closed |
| 49-02/T-49-04 | Information Disclosure / integrity | `InvariantsConfig` parsing | low | mitigate | strict type/domain validation, dotted unknown-key refusal, null-shape regression suite | closed |
| 49-03/T-49-01 | Repudiation | invariant-B resume continuity | high | mitigate | boundary-exact checkpoint/resume test proves the stall window is not re-armed | closed |
| 49-03/T-49-05 | Tampering | stale or foreign checkpoint payload | medium | mitigate | schema-v2 enforcement and missing/malformed invariant-state refusal tests | closed |
| 49-04/T-49-01 | Repudiation | census/preflight checks | high | mitigate | placeholder, disagreement, instrumentation, and refusal-ordering trip tests | closed |
| 49-04/T-49-02 | Tampering | register entry claims closed after regression | high | mitigate | loader resolves proof nodes and the meta-test executes every closed proof | closed |
| 49-04/T-49-03 | Tampering | register/preflight path and bytes | medium | mitigate | fixed paths, atomic serialization, exact schema validation, non-finite refusal | closed |
| 49-05/T-49-01 | Repudiation | `eval01_precondition_i` projection | high | mitigate | both eligibility truth directions and every malformed/absent failure mode are trip-tested | closed |
| 49-05/T-49-02 | Tampering | conformance block content | medium | mitigate | summary projects the validated preflight payload verbatim; forgery tests fail closed | closed |
| 49-06/T-49-01 | Repudiation | end-to-end gate composition | high | mitigate | synthetic production-`main()` seam observes run-start, boundary, guards, and summary | closed |
| 49-06/T-49-06 | Elevation of Privilege | invariant-B window-selection authority | high | mitigate | owner ruling is recorded verbatim as `N = 500`; config, register, proof, and UAT agree | closed |

*Status: open · closed · open below threshold (non-blocking).*

---

## Accepted Risks Log

No accepted risks. Every authored threat uses the `mitigate` disposition and
has executable or recorded-authority evidence.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-07 | 13 | 13 | 0 | Codex GPT-5, ASVS L1 short-circuit audit |

Evidence: `.venv/bin/python -m pytest -q tests/phase49` reported 176 passed in
13.26s on the final code tree. The agent-automated UAT independently re-ran the
owner-window, launch/refusal, config, controlled-failure, resume-history, and
producer-contract slices with 68 focused passing cases in total.

---

## Sign-Off

- [x] All threats have a disposition.
- [x] Accepted risks documented (none).
- [x] `threats_open: 0` confirmed at the configured `high` threshold.
- [x] `status: verified` set in frontmatter.

**Approval:** verified 2026-08-07
