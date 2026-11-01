---
phase: "66"
slug: "small-network-control"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-01"
---

# Phase 66 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Launch gate → fit worker | `diagnostic_power.launch` mediates every real run: pmset power read, America/Chicago weekend window, exclusive `power-gate.json` receipt, fixed-argv caffeinate child | Launch authorization (AC power, window, registration identity) |
| Registration → data seam | A run may open only what its committed registration declares: one Stage-0 TRAIN gold record through the unchanged guarded seam | Stage-0 training record (access counts audited by check-run) |
| Committed pages/registrations → reader | The reading rule and review read only committed, hash-pinned artifacts; admission refuses untracked, dirty, or changed artifacts | Experiment evidence (record.json, pages, registrations) |
| Owner → checkpoint ① | The owner's answer crosses as a verbatim, never-parsed quote | SCOPE-49 plan-change authority |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-66-01 | Tampering | validate_smoke_settings registry lookup | high | mitigate | Closed REGISTRIES table; byte-agreeing variant block; refusals before data/optimizer contact proven by Phase66AdmissionTests (tests/phase66 green) | closed |
| T-66-02 | Tampering | Phase 65 smoke registration and evidence | high | mitigate | No Phase 65 file edited — git log on the Phase 65 directory empty since phase start; HistoricalPhase65Tests check the four unedited digests and 11 preserved hashes (green) | closed |
| T-66-03 | Elevation of privilege | diagnostic_power.launch argv | medium | mitigate | Absolute binary paths, fixed argv list, no shell, repo-root confinement; exact-argv assertions in test_tracer/test_power (green); reviewer traced argv construction clean | closed |
| T-66-04 | Spoofing | power-source parse and launch window | medium | mitigate | Positive first-line match only; every unrecognized reading, error or timeout refuses before any receipt or child; weekend window enforced in code (test_power, 22 tests, green); live POWER-OK agreed with pmset | closed |
| T-66-05 | Information disclosure | power-gate.json | low | mitigate | Repo-relative paths only; write_record_exclusive home-directory redaction guard; receipts on disk verified free of absolute/home paths | closed |
| T-66-06 | Denial of service | record size and run cap | high | mitigate | exp01_budget time-bound N with stride ceil(N/10,000) and 14-entry cadence; ceiling guard independent of N; all four records ~0.56–1.3 MiB against the 10 MiB commit policy; caps held (600/1957/1734/2034 s); MAX_BLOB_BYTES unchanged | closed |
| T-66-07 | Repudiation | reading rule at its edges, still-improving runs | medium | mitigate | One tested pure function per rule with boundary tests at 0.1, both band edges, non-finite values and the 0.01 growth edge (test_reading_rule, 20 tests, green); unsettled never confirmed, routes to owner | closed |
| T-66-08 | Tampering | a run that did not test the registered network | high | mitigate | read_exp01_record/read_run_directory refuse on any mechanical problem and route to owner; check-run EXP01-CHECK-OK with empty problem lists re-run live on all three committed records by the verifier | closed |
| T-66-09 | Elevation of privilege | Stage-0 data access per run | high | mitigate | Unchanged guarded seam admits only the registered train-split stage-0 gold record; check-run audited one train open, zero validation opens, test_split_opened 0 on every record (re-run live) | closed |
| T-66-10 | Denial of service | launch conditions (battery, window, cap, session kill, burned directory) | medium | mitigate | Gate refuses on battery/outside window creating nothing; detached session after a passing survival test; supervised caps ended every run; run-state table never relaunches a published/live attempt; single pre-registered retry unused | closed |
| T-66-11 | Repudiation | a run launched outside the gate or window | medium | mitigate | Every directory holds a receipt recording AC Power and the window, preceding its attempt claim; check-run checks both (re-run live on all records) | closed |
| T-66-12 | Denial of service | concurrent heavy jobs perturbing a run | low | mitigate | One run at a time, no suites during runs; receipt records load average | closed |
| T-66-13 | Spoofing | the owner's checkpoint ① answer | high | mitigate | One gate="blocking-human" checkpoint, never auto-selected; owner message kept verbatim in a never-parsed owner-quote block (RULING-OK re-run live); CP1-EXP01 = accept | closed |
| T-66-14 | Repudiation | the scientific claim of the result | medium | mitigate | Branch/confirmation/route derive only from diagnostic_phase66 review over committed directories; RESULT-PAGE-OK compares the page against a fresh review (re-run live); all 22 evidence-index SHA-256s match | closed |
| T-66-15 | Tampering | diagnostic records reused as graded evidence | medium | mitigate | Records stay intrinsically marked inst08-diagnostic; graded/evaluator entry points refuse them (Phase 65, unchanged); held-out evaluation unspent | closed |
| T-66-16 | Information disclosure | the timing run's score | low | mitigate | check-run prints no score (tested); the timing score was never read in any plan; verifier used check-run only | closed |
| T-66-17 | Repudiation | a non-Tier-1 result read as a pipeline defect | high | mitigate | Frozen timing page committed before the timing run (git ancestry 4eab280b → a564ea35); near only for settled runs with passed setting checks; TimingPageTests verbatim sections (green) | closed |
| T-66-18 | Tampering | pages and registrations | high | mitigate | Admission refuses untracked/dirty/changed artifacts; page digests pinned; ORDER-OK evidence-order ancestry re-run live by the verifier | closed |
| T-66-SC | Tampering | package installs | low | accept | No package installed or upgraded; torch/numpy pre-existing in the pinned environment (66-RESEARCH.md Package Legitimacy Audit: not applicable) | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-66-SC | T-66-SC | No package installation occurs in this phase; dependencies are pre-existing in the pinned pinn-train environment, so the supply-chain surface is empty | Owner (standing delegation, 66-CONTEXT D-01) | 2026-11-01 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-01 | 19 | 19 | 0 | ZCode orchestrator (gsd-secure-phase, State B, ASVS L1 short-circuit) |

Evidence basis: all 18 mitigate-dispositions are test-backed by the green suites (tests/phase65 204 OK; tests/phase66 99 OK) and re-verified live by 66-VERIFICATION.md (VERIFY-RESULT-OK, EXP01-CHECK-OK, ORDER-OK, RESULT-PAGE-OK, RULING-OK, budget reproduction, 22/22 SHA-256 matches, Phase 65 directory untouched). Advisory findings in 66-REVIEW.md (2 critical / 4 warning / 4 info) are reader-robustness edges on malformed-evidence shapes outside the committed evidence; they are documented known-accepted debt in 66-VERIFICATION.md against the frozen harness and are not open threats against this phase's evidence.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-01
