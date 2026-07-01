---
phase: 36
slug: acceptance-checks-re-verification-handoff
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-01
---

# Phase 36 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution. Derived from
> `36-RESEARCH.md` §Validation Architecture. Phase 36 is specwork-only: "tests" are
> deterministic **disposable probes** (Phase 21/29 pattern), not a unit framework.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None project-wide; `python3` + `bash` deterministic accumulator probes. Local precedents: `tests/test_phase12_validation.py` (PASS/FAIL accumulator), `tests/git_policy/test_git_policy.py` (`unittest`). |
| **Config file** | none — explicit commands captured in `36-PROBE-RESULTS.md` |
| **Quick run command** | `bash .planning/phases/36-acceptance-checks-re-verification-handoff/run-ac-suite.sh` (illustrative; the planner may name the driver/probes) |
| **Full suite command** | same driver — re-runs every probe, exits nonzero on any required FAIL |
| **Estimated runtime** | ~seconds (closure has no time-series behavior; probes are deterministic file/token/count checks) |

---

## Sampling Rate

- **After every task commit:** run the affected manifest row's probe line.
- **After every plan wave (ledger promote, status reconcile):** re-run the full AC suite + protected-path guard + ledger-freshness SHA-256 check.
- **Before `/gsd-verify-work`:** full suite green + ledger terminal + SI grep clean + 32/32 traceability audit pass.
- **Max feedback latency:** ~seconds.

**Sampling-rate adequacy:** closure has no time-series to under-sample; the risk is *missing a
contract*, mitigated by deriving manifest rows from the enumerated v1.6 contract IDs (32-row
traceability + Phase 32 ledger) so coverage is exhaustive, not sampled.

---

## Per-Task Verification Map

> Finalized by the planner against `36-ACCEPTANCE-MANIFEST.md` rows. Each phase requirement below
> maps to a deterministic probe; rows are keyed to the manifest, one PASS/FAIL/SKIP each in
> `36-PROBE-RESULTS.md`.

| Requirement | Observable that proves it | Check type | Automated Command (illustrative) | Status |
|-------------|---------------------------|------------|----------------------------------|--------|
| VER-13 | Every manifest contract row has non-empty pass criterion + data/expression + command | manifest audit | `python3` parse of `36-ACCEPTANCE-MANIFEST.md` | ⬜ pending |
| VER-15 | Each manifest row → one PASS/FAIL/SKIP with hashed evidence; no `pinn/` touch | probe run + guard | `run-ac-suite.sh`; `grep -lE 'pinn/' probes/*` empty | ⬜ pending |
| VER-16 | Ledger counts match a fresh parse; 0 nonterminal in-scope rows | ledger audit | `python3` parse of `32-ISSUE-LEDGER.md` | ⬜ pending |
| VER-18 | Fresh SI grep ⊆ handoff SI table | grep diff | `rg -n "SI-[A-Z]+-[0-9]+"` vs `36-HANDOFF.md` table | ⬜ pending |
| VER-17 | Each ledger row appears once across fixed/unchanged/deferred | handoff audit | `python3` set check | ⬜ pending |
| VER-14 | Exactly 32 rows, one phase each; post-reconciliation no flag contradicts terminal state | traceability audit | `python3` parse of traceability table | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `36-ACCEPTANCE-MANIFEST.md` — aggregates the R1 source map (VER-13)
- [ ] `probes/` disposable scripts + `run-ac-suite.sh` driver (VER-15)
- [ ] `evidence/` raw stdout/stderr + SHA-256 (VER-15)
- [ ] ledger-audit + traceability-audit + handoff-audit probes (VER-16/14/17)
- [ ] SI-grep diff probe (VER-18)
- [ ] protected-path guard probe (D-36-06 / Prohibition 1)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `REQUIREMENTS.md` / `ROADMAP.md` status reconciliation | VER-14 (R6) | GSD state/roadmap mutating verbs emit malformed output in this repo (SPEC Constraint; `36-RESEARCH.md` §Don't Hand-Roll) — flips are manual, diff-reviewed edits | Apply each flip only where a matching terminal anchor exists (ledger row **OR** terminal phase-VERIFICATION/completion record per the resolved R6 rule, GAP-36-01/02); `git diff` review before commit; a companion probe re-parses the tables to confirm no flag contradicts its terminal anchor |
| SI-DQA-003 / SI-PINN-002 preserve disposition | VER-18 (R4) | Issue-03-relevance is a STOP-governed judgment (D-36-18); source-silent → STOP gap, not a probe | Adjudicate against sources; a `checkpoint:human-verify` may gate the *preserve* dispositions (Phase 29 D-08 precedent) |

---

## Validation Sign-Off

- [ ] Every manifest row has a probe with an automated command or an explicit Manual-Only entry
- [ ] Sampling continuity: no required contract left without a PASS/FAIL/SKIP row
- [ ] Wave 0 covers all MISSING references (manifest, probes, evidence, guards)
- [ ] No watch-mode flags
- [ ] Fail-closed gate holds: any missing field / required FAIL / nonterminal ledger row / uncited SI / count mismatch / traceability ≠ 32 / protected-path diff → BLOCKED
- [ ] `nyquist_compliant: true` set in frontmatter after Wave 0 lands

**Approval:** pending
