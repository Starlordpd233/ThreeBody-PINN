---
phase: "67"
slug: "design-settings-ladders"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-08"
---

# Phase 67 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Registration to local data/model construction | Caller-controlled declarations must pass committed TRAIN-only admission before any open or optimizer contact | Stage-0 TRAIN gold records (access counts attested per run) |
| Launch gate → fit worker | `diagnostic_power.launch` mediates every real run: pmset AC read, America/Chicago window (with the three one-shot owner amendments, each self-expiring), whole-launch cap fit, exclusive `power-gate.json` receipt, fixed-argv caffeinate child | Launch authorization (power, window, registration identity) |
| Committed pages/registrations → reader | The reading rule, budget, review and audit read only committed, hash-pinned artifacts; admission refuses untracked, dirty or digest-changed artifacts; the 41-file harness freeze is verified at every gate | Experiment evidence (records, attempts, receipts, registrations, pages) |
| Owner → SCOPE-47/49 checkpoints | The owner's answer crosses as a verbatim, never-parsed quote bound to result/review digests | Scope-continuation authority (EXP-03 refutation ruling) |

---

## Threat Register

All 60 plan-authored threats (disposition `mitigate` in every authoring plan) consolidate to 33 distinct mechanisms below; every plan threat ID is cited in its row. Status `closed` = the named mitigation is implemented and exercised by the green committed suites and gates cited in the evidence basis.

| Threat IDs (plan/ID) | Category | Component | Severity | Disposition | Mitigation (plan-authored) | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| 01/T-67-01 | Tampering | Phase 67 admission | high | mitigate | Bind exact declared settings and current dependencies before any open or optimizer. | closed |
| 01/T-67-02 | Information disclosure | TRAIN reader | high | mitigate | Retain Stage-0 TRAIN-only validation and zero-held-out-open tripwires. | closed |
| 01/T-67-03 | Repudiation | Historical evidence | medium | mitigate | Verify recorded bytes at the recorded run commit and keep fresh pins separate. | closed |
| 02/T-67-04 | Tampering | Feature declarations | high | mitigate | Reject malformed, boolean, nonfinite, nonpositive or orbit-mismatched frequencies before construction. | closed |
| 02/T-67-05 | Elevation of privilege | Production locks | high | mitigate | Preserve ArchitectureSpec/network bytes and prove raw seeded parity. | closed |
| 02/T-67-06 | Repudiation | Encoded logger | medium | mitigate | Explicit applicability fields and registered frequency/coordinate metadata prevent misleading bandwidth claims. | closed |
| 03/T-67-08 | Tampering | Prefix metadata | high | mitigate | Preserve first-crossing bracket, exact time/mask hashes and independent synthetic checks. | closed |
| 03/T-67-09 | Repudiation | Baseline expectations | medium | mitigate | Record both independent frozen-scoring paths and explicit formula nonapplicability. | closed |
| 04/T-67-10 | Tampering | Budget input | high | mitigate | Require all exact timing identities and finite disjoint costs, then compute N without scientific metrics. | closed |
| 04/T-67-11 | Denial of service | Checkpoints and publication | high | mitigate | Include all costs, reserve25% target headroom, retain under-hour refusal and supervised whole-run cap. | closed |
| 05/T-67-12 | Tampering | Record/receipt/attempt reader | high | mitigate | Shape/type/finite validation, exact registration matching and digest checks precede any scientific branch. | closed |
| 05/T-67-13 | Information disclosure | Record-supplied paths | high | mitigate | Contain registration paths and local weight filenames before open. | closed |
| 05/T-67-14 | Spoofing | Power and access evidence | high | mitigate | Require independent access attestation and aware-instant-derived weekend/AC receipt checks. | closed |
| 05/T-67-15 | Repudiation | Confirmation | medium | mitigate | Persist every declared paired contrast and all three cases, with exact thresholds and nonconfirmation reasons. | closed |
| 06/T-67-15 | Tampering | Page/registration workflow | high | mitigate | Exact design/metadata/budget hashes and Git ancestry precede each dependent operation. | closed |
| 06/T-67-16 | Information disclosure | Metadata capture | high | mitigate | Reuse TRAIN-only reader and independent attestation, with pre-open tripwire tests. | closed |
| 06/T-67-17 | Denial of service | Real operation supervisor | high | mitigate | Start cap before admission, bound publication, terminate owned descendants and preserve incomplete attempts. | closed |
| 06/T-67-18 | Elevation of privilege | Dependent launch | high | mitigate | Require prior committed review and explicit resolution of any reserved owner proposal. | closed |
| 07/T-67-07-FREEZE | Tampering | Harness-freeze manifest | high | mitigate | Record exact current implementation/frozen-artifact digests and commit before real registrations. | closed |
| 07/T-67-07-HISTORY | Repudiation | Historical compatibility | medium | mitigate | Preserve evidence hashes and run-commit ancestry separately from live admission pins. | closed |
| 08/T-67-08-A; 10/T-67-10-A; 12/T-67-12-A; 14/T-67-14-A | Information disclosure | Metadata and timing loader | high | mitigate | TRAIN-only pre-open checks, access counts and independent zero-held-out attestation. | closed |
| 08/T-67-08-B; 10/T-67-10-B; 12/T-67-12-B; 14/T-67-14-B | Tampering | Design, matrix and budget | high | mitigate | Committed design/dependency/grid digests and complete exact row checks before launch. | closed |
| 08/T-67-08-C; 10/T-67-10-C; 12/T-67-12-C; 14/T-67-14-C | Denial of service | Local compute | high | mitigate | Serial900-second supervised attempts, current weekend AC gate and cost-only common science projection. | closed |
| 08/T-67-08-D; 10/T-67-10-D; 12/T-67-12-D; 14/T-67-14-D | Repudiation | Prospective chronology | medium | mitigate | Commit design, metadata, matrix and each evidence row in that order with explicit owned paths. | closed |
| 09/T-67-09-A; 11/T-67-11-A; 13/T-67-13-A; 15/T-67-15-A | Information disclosure | Science reader | high | mitigate | Preserve TRAIN-only pre-open admission and zero-held-out access attestations. | closed |
| 09/T-67-09-B; 11/T-67-11-B; 13/T-67-13-B; 15/T-67-15-B | Denial of service | Local launch | high | mitigate | Serial3540-second whole-launch supervision and fresh weekend AC eligibility. | closed |
| 09/T-67-09-C; 11/T-67-11-C; 13/T-67-13-C; 15/T-67-15-C | Tampering | Matrix and result | high | mitigate | Freeze digests/settings before science, check every row and commit evidence before review. | closed |
| 09/T-67-09-D; 11/T-67-11-D; 13/T-67-13-D; 15/T-67-15-D | Elevation of privilege | Reserved disposition | high | mitigate | check-review requires a committed factual owner ruling only when the recorded proposal requires one. | closed |
| 09/T-67-09-E; 11/T-67-11-E; 13/T-67-13-E; 15/T-67-15-E | Repudiation | Confirmation | medium | mitigate | Publish all contrasts/repeats and exact prospective unsettled/effect thresholds with costs. | closed |
| 16/T-67-16-CLOSE-A | Tampering | Evidence index | high | mitigate | Independently re-run the read-only full audit and compare its JSON with the saved index. | closed |
| 16/T-67-16-CLOSE-B | Elevation of privilege | Scope disposition | high | mitigate | Require four closed committed reviews and factual hash-bound rulings only for actual reserved changes. | closed |
| 16/T-67-16-CLOSE-C | Information disclosure | Audit readers | high | mitigate | Use contained diagnostic evidence only; no corpus or held-out access is authorized by closeout. | closed |
| 16/T-67-16-CLOSE-D | Repudiation | Scientific findings/cost | medium | mitigate | Cite all main/repeat records and preserve actual successful/failed machine time in committed state. | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-67-SC | supply chain (standing) | No package installation or upgrade occurred in the phase (no dependency-touching commit in the phase range); the run environment stayed the pinned pinn-train interpreter audited in 66-RESEARCH.md | Owner (standing delegation, 66-CONTEXT D-01) | 2026-11-08 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-08 | 60 | 60 | 0 | ZCode orchestrator (gsd-secure-phase, State B, ASVS L1 short-circuit) |

Evidence basis: every mitigation mechanism above is implemented in the committed harness and exercised by the green suites at the phase tail (tests/phase67 260 OK across 13 modules with zero skips; tests/phase66 101 OK; tests/phase65 204 OK). The gate stack re-verified live at the final HEAD this session: check-design/check-metadata/check-matrix (timing+science)/check-budget for exp02+exp03, check-budget/check-matrix/check-review for exp04+exp05, `PHASE67-AUDIT-OK` re-run twice (67-16 and the orchestrator spot-check), and the live launch gate reading `POWER-OK` inside the weekend window. Every real launch of the phase (~65 timing probes + 45 science rows) wrote an exclusive power-gate receipt recording AC Power, the window and the amendment-era closing instant before its attempt claim; every row passed check-row (scores hidden) with its whole-launch wall inside the registered cap; the exp03 refutation crossed to EXP-04 only through the committed digest-bound owner ruling, and `check-review` re-confirmed `PHASE67-REVIEW-OK` after each freeze re-pin. The re-pin convention (ed93f359/179efd80/88d17045 and the in-plan fixes) kept historical run records verifiable at their introducing commits throughout.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-08
