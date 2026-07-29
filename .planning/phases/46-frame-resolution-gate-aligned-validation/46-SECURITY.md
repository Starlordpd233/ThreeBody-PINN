---
phase: 46
slug: frame-resolution-gate-aligned-validation
status: verified
threats_open: 0
asvs_level: 1
created: 2026-07-29
---

# Phase 46 — Security

> ASVS-L1 verification of the threat registers authored in plans 46-01 through
> 46-09. The audit verifies the registered mitigations; it does not expand the
> plan-time threat model.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Test fixtures → production probe/gate | Synthetic fixtures define the ground truth for frame and isolation checks. | Synthetic trajectories, split keys, model outputs |
| Probe → corpus and split manifests | The train-free probe may read eligible train/validation records but must not materialize a withheld-split view. | Manifest membership, trajectory arrays |
| Corpus/manifests → committed evidence | Evidence grounds the frame verdict and must remain deterministic, attributable, contained, and host-path free. | Metrics, hashes, provenance |
| Evidence → verdict and owner ruling | Machine outcomes must be transcribed without rounding or semantic upgrade. | Verdict token, branch route, owner instruction |
| Repair → resident trajectory surface | The minimum repair must pair bodies correctly without silently applying rotation or global scaling. | Positions, velocities, masses |
| Validation event → sidecar/JSONL | A pointer is eligible only after a durable schema-valid sidecar exists. | Per-trajectory ε_H/SCS, frame metadata |
| Persisted validation → EVAL-01 eligibility | Metric failure and instrumentation failure must remain distinguishable. | Gate status, gate verdict, summary projection |
| Run/evidence roots → filesystem | User-influenced roots and step values must not escape their designated containment. | Relative paths, atomic files |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation and verification evidence | Status |
|-----------|----------|-----------|----------|-------------|--------------------------------------|--------|
| T-46-01-01 | Tampering | Dual-frame fixture | high | mitigate | Closed-form separability and matched-frame residual checks pass in `test_fixtures_selfcheck.py`. | closed |
| T-46-01-02 | Tampering | Stub source ordering | medium | mitigate | Fixture self-check proves insertion order differs from sorted order; downstream sorting checks are non-vacuous. | closed |
| T-46-01-03 | Elevation of Privilege | Fixture split surface | high | mitigate | Fixture source exposes no withheld/test constructor; isolation tests reassert the banned surface is absent. | closed |
| T-46-01-04 | Information Disclosure | Fixture data sources | low | accept | Fixtures are wholly synthetic and access no corpus or run artifact; accepted as no sensitive data crosses this boundary. | closed |
| T-46-02-01 | Tampering | Probe arm construction | high | mitigate | Symmetric hypothesis/control construction and mirror cases pass in `test_frame_probe.py`. | closed |
| T-46-02-02 | Tampering | Verdict classifier | high | mitigate | `test_frame_probe.py` exercises definite, ambiguous, and non-frame routes with fail-closed ordering. | closed |
| T-46-02-03 | Tampering | Numerical tolerance | high | mitigate | Tests pin the measured control-floor plus fp32-increment formula and exclude imported physics thresholds. | closed |
| T-46-02-04 | Information Disclosure / Elevation | Probe split exposure | medium | mitigate | Probe core accepts injected readers only; dataset-free tests and manifest assembly preserve train/validation-only access. | closed |
| T-46-02-05 | Denial of Service | Degenerate finite differences | low | mitigate | Non-finite, coincident, and single-snapshot fixtures fail closed without an unhandled exception. | closed |
| T-46-03-01 | Tampering | Sidecar publication | high | mitigate | Atomic publication, no-temp-residue, re-read, and schema validation pass in `test_artifacts.py`. | closed |
| T-46-03-02 | Tampering | Non-finite handling | high | mitigate | Quoted sentinel retention and honest FAIL behavior pass in `test_artifacts.py` and the autonomous UAT production-path check. | closed |
| T-46-03-03 | Tampering | Sidecar path containment | medium | mitigate | Fixed relative step path, integer validation, and hostile-step refusal are covered by sidecar tests. | closed |
| T-46-03-04 | Elevation of Privilege | Validation split isolation | high | mitigate | AST plus fresh-interpreter checks prove no evaluator import; rows are exactly validation keys. | closed |
| T-46-03-05 | Repudiation | Gate evidence re-derivability | medium | mitigate | Versioned schema, in-band thresholds, deterministic ordering, and byte-identical republish are tested. | closed |
| T-46-04-01 | Repudiation | Probe evidence provenance | high | mitigate | Payload includes repo, manifest, blacklist, frame, dtype/device, and tolerance provenance; deterministic rendering tests pass. | closed |
| T-46-04-02 | Information Disclosure | Committed probe evidence | medium | mitigate | Both committed evidence runs pass host-path scans; roots are represented by source labels. | closed |
| T-46-04-03 | Tampering | Evidence-root containment | high | mitigate | Evidence writer tests reject dataset/corpus roots, use atomic writes, and create non-overwriting UTC directories. | closed |
| T-46-04-04 | Elevation of Privilege | Manifest test membership | high | mitigate | Test partitions are physical-key exclusion sets only; no test `StageIndex` is constructed. | closed |
| T-46-04-05 | Tampering | Population drift | medium | mitigate | Population equality and empty-eligibility checks fail closed; CLI operational failure is nonzero. | closed |
| T-46-05-01 | Elevation of Privilege | Evaluator import isolation | high | mitigate | Static AST and fresh-subprocess `sys.modules` checks both pass. | closed |
| T-46-05-02 | Tampering | Eligibility semantics | high | mitigate | Missing, truncated, or corrupt sidecars cannot produce eligible pointer fields. | closed |
| T-46-05-03 | Tampering | FAIL rendered as PASS | high | mitigate | Sentinel tests and an autonomous non-conserving production-path run verify `gate_status: ok` can honestly coexist with `gate_verdict: FAIL`. | closed |
| T-46-05-04 | Repudiation | Vacuous-test risk | medium | mitigate | Full 16-key removal loop, both prior-mode variants, and zero-skip Phase 46 execution prevent subset/skip-to-green behavior. | closed |
| T-46-06-01 | Tampering | Pre-repair verdict grounding | high | mitigate | `46-VERDICT.md` matches committed `raw.json`: SHA-256 `3fa8251b…`, `VERDICT_AMBIGUOUS`, rule 6, D-09, 1,651 records. | closed |
| T-46-06-02 | Elevation of Privilege | D-09 scope boundary | high | mitigate | The pre-repair executor changed no `pinn/` file and routed the ambiguity through the recorded owner gap process. | closed |
| T-46-06-03 | Information Disclosure | Pre-repair evidence bytes | medium | mitigate | Host-path scan is clean and the payload records redacted source labels. | closed |
| T-46-06-04 | Repudiation | Population decision provenance | high | mitigate | The three retained manifest hashes and the 1,651-record intersection are embedded in committed evidence and verdict artifacts. | closed |
| T-46-06-05 | Denial of Service | Long-running corpus scan | low | accept | Expected runtime and operational exit semantics are documented; the finite one-run cost is accepted. | closed |
| T-46-07-01 | Elevation of Privilege | Frame ratification | high | mitigate | `RATIFIED_VALIDATION_FRAME` quotes GAP-46-06 option B and the post-repair evidence path; the machine verdict remains unchanged. | closed |
| T-46-07-02 | Tampering | Pointer-before-durable | high | mitigate | Production seam publishes then revalidates before returning fields; wiring and artifact tests pass. | closed |
| T-46-07-03 | Tampering | Eligibility/FAIL projection | high | mitigate | Six projection cases plus direct UAT generation prove schema-valid durability, sentinel passthrough, and fail-closed eligibility. | closed |
| T-46-07-04 | Denial of Service | Instrumentation failure | medium | mitigate | Empty/poisoned sources convert to `failed:` records without crashing and restore prior model mode. | closed |
| T-46-07-05 | Repudiation | Re-entry/idempotency | medium | mitigate | Single hook location, last-step deduplication, atomic same-path replacement, and deterministic last-record rendering are tested. | closed |
| T-46-08-01 | Elevation of Privilege | Repair overreach | high | mitigate | Pairing tests prove rotation and D/V scaling remain absent and the probe implementation is untouched. | closed |
| T-46-08-02 | Tampering | Duplicate transform math | high | mitigate | Adapter consumes `preprocess_trajectory` outputs; repair equations remain centralized in preprocessing. | closed |
| T-46-08-03 | Repudiation | Weakened regression suite | high | mitigate | Summary records the baseline triage; no new skip/xfail exists and all 114 Phase 46 tests pass with zero skips. | closed |
| T-46-08-04 | Tampering | Membership/accounting drift | medium | mitigate | Pairing regression tests pin membership, counts, and snapshot totals across the resident-source switch. | closed |
| T-46-08-05 | Information Disclosure | Repair test output | low | mitigate | Tests use fixtures and produce no new real-corpus artifact or host-specific path. | closed |
| T-46-09-01 | Tampering | Instrument/population drift | high | mitigate | Pre/post controls are byte-for-byte equal, the probe hash gate passed, and both runs use the same 1,651-record population. | closed |
| T-46-09-02 | Elevation of Privilege | Verdict rounding | high | mitigate | Committed output remains rule-5 `VERDICT_NON_FRAME_DIVERGENCE`; no clean token is substituted. | closed |
| T-46-09-03 | Elevation of Privilege | Re-run until clean | high | mitigate | Exactly one pre-repair and one authorized post-repair evidence directory exist and are separately attributable. | closed |
| T-46-09-04 | Tampering | Transform-to-force-verdict | high | mitigate | Post-repair evidence preserves the specified intermediate, reports `plus_permutation = 0.0` for 1,651/1,651, and routes the remaining result to GAP-46-06. | closed |
| T-46-09-05 | Repudiation | Pre-repair verdict mutation | medium | mitigate | Pre-repair artifact hash remains `3fa8251b…`; post-repair evidence is separate with SHA-256 `11b6690a…`. | closed |

*Status: open · closed · open — below high threshold (non-blocking)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-46-01 | T-46-01-04 | Synthetic fixtures contain no corpus, run, credential, or host data; residual disclosure exposure is negligible. | Phase 46 plan disposition | 2026-07-29 |
| R-46-02 | T-46-06-05 | The bounded train-free scan is intentionally minutes-scale, with documented liveness expectations and operational exit codes. | Phase 46 plan disposition | 2026-07-29 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-07-29 | 43 | 43 | 0 | Codex/GPT-5 autonomous ASVS-L1 audit |

Verification basis:

- `pytest tests/phase46/ -q -rs` → 114 passed, 27 subtests passed, zero skipped.
- `pytest tests/phase43/test_summary_enrichment.py -q -rs` → 5 passed.
- Direct pre/post evidence assertions verified schema, hashes, rule/route,
  population, byte-identical controls, and 1,651/1,651 exact pairing repair.
- A fresh temporary production-path run verified sidecar → JSONL → summary
  persistence with the ratified frame, all eight gate fields,
  `eval01_precondition_iii: true`, and an honest metric FAIL under successful
  instrumentation.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-07-29
