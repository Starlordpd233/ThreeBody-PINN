---
phase: 21-acceptance-checks-and-handoff
status: issues_found
depth: deep
reviewed_at: 2026-06-08
files_reviewed: 8
findings:
  critical: 0
  warning: 0
  info: 3
  total: 3
verdict: "Phase 21 correctly, accurately, and completely executed. No blocking findings. 3 Info-level observations."
scope:
  - .planning/phases/21-acceptance-checks-and-handoff/probes/probe_scaling.py
  - .planning/phases/21-acceptance-checks-and-handoff/probes/probe_com.py
  - .planning/phases/21-acceptance-checks-and-handoff/probes/probe_ad.py
  - .planning/phases/21-acceptance-checks-and-handoff/probes/probe_force_energy.py
  - .planning/phases/21-acceptance-checks-and-handoff/probes/probe_loss_stability.py
  - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  - pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md
---

# Phase 21 Code Review — Acceptance Checks and Handoff (deep)

## Verdict

**Phase 21 is correctly, accurately, and completely executed and finished.** All five
disposable validation probes execute against the v1.4 framework specs, exit 0, and
reproduce their committed stdout evidence **byte-for-byte**. All six SHA-256 evidence
hashes match `21-PROBE-RESULTS.md`. The §10 acceptance-check definitions match the probes
and pass criteria. The SI-* ledger reconciliation and the Phase 22 handoff are fully
grounded in the Phase 16 issue ledger. No open STOP-protocol gaps. The phase's own strict
full suite passes (`SUITE_EXIT=0`). Working tree is clean for all Phase 21 paths.

No Critical or Warning findings. Three Info-level observations are recorded below; none
block closure.

## Verification Performed (independent re-execution)

| Check | Method | Result |
|---|---|---|
| Probe execution | Fresh re-run of all 5 probes with `.venv/bin/python` (Python 3.12.13) | All exit 0; PASS |
| Evidence authenticity | Diff fresh stdout vs committed `evidence/*.stdout.txt` | Byte-for-byte identical (incl. deterministic loss-stability values) |
| Evidence integrity | Recompute SHA-256 of 6 evidence files vs `21-PROBE-RESULTS.md` | 6/6 match |
| §10 spec fidelity | Compare §10.1–10.5 pass criteria/data/commands vs probe behavior | Consistent |
| Force-energy physics | Hand-derive −∂V/∂xᵢ vs manual Plummer accel | Correct (rel_err 1.62e-16) |
| SI reconciliation | Inspect retired SI-CTL-001→B-03, SI-SSR-001→M5; preserved entries | Correct |
| SI-PINN-001 no-fabrication | `git grep` whole tree | Exists only in planning/working notes, never a framework-spec SI entry — correctly NOT synthesized |
| Handoff grounding | Cross-check Fixed/Deferred vs `16-ISSUE-LEDGER.md` | 19 VERIFIED + M6/M7 DEFERRED — exact match |
| STOP gaps | `21-GAPS.md` `open_gaps: 0` + retroactive grounding audit | No open gaps; 6 ungrounded temptations correctly resisted |
| Closure shape | All 11 required GSD artifacts + 2 summaries present | Complete |
| Commit state | `git status` for phase paths | All committed (2f952cf, 87c84f5) |
| Strict full suite | `21-VALIDATION.md` suite | ALL PASS |

## Requirement Coverage

- **VER-01** (numeric acceptance checks): PASS — §10.1–10.5 each name pass criterion, input data, executing command.
- **VER-03** (validation handoff): PASS — `21-HANDOFF.md` classifies Fixed/Intentionally-Unchanged/Deferred, M6/M7 explicit.
- **VER-04** (checks executed against specs, not `pinn/`): PASS — probes implement spec contracts; raw stdout + hashes recorded.
- **VER-05** (closing loop): SATISFIED via the `16-ISSUE-LEDGER.md` phase-exit gate (VERIFIED/DEFERRED only). See CR-02.
- **VER-06** (SI ledger reconciliation): PASS — resolved entries retired with back-refs; unrelated entries preserved.

## Findings

### CR-01 (Info) — Scaling probe is near-tautological

`probes/probe_scaling.py` validates `D=(G·T²)^(1/3)` self-consistency by checking
`G·T²/D³ == 1` and an acceleration round-trip `(D/T²)·2·T²/D == 2`. Both are algebraic
identities given `D³ ≡ G·T²`; they can only fail through floating-point roundoff (observed
metric `2.22e-16` ≈ machine epsilon). This is the weakest of the five probes — it confirms
the scaling *convention* closes dimensionally but cannot discriminate a wrong exponent
against an independent reference. It is nonetheless a legitimate improvement over the
pre-repair `T=1`/`D=1` tautology and is adequate for a spec-self-consistency check.
**Action: none required.** Optional future hardening: validate against an independently
computed physical quantity rather than the inverse transform.

### CR-02 (Info) — VER-05 not itemized in 21-VERIFICATION.md coverage table

`21-VERIFICATION.md` frontmatter and the Requirement Coverage table enumerate VER-01,
VER-03, VER-04, VER-06 but omit VER-05. VER-05 is substantively satisfied — plan
`21-01-PLAN.md` carries it (`requirements: [VER-01, VER-04, VER-05]`), `ROADMAP.md` frames
it as "(+ VER-05 closing loop)", and the `16-ISSUE-LEDGER.md` phase-exit gate enforces it.
This is a documentation-completeness nit, not a correctness gap. **Action: optional** — add
a VER-05 row to the coverage table noting the ledger gate as its evidence.

**Follow-up:** Addressed after this review by adding `VER-05` to the `21-VERIFICATION.md`
frontmatter and Requirement Coverage table, with the Phase 16 ledger phase-exit gate as
evidence.

### CR-03 (Info) — Loss-stability probe architecture is representative, not locked

`probes/probe_loss_stability.py` applies the skip+`norm(x).pow(2)` branch on hidden layers
of odd `layer_number` (counting from 2). The production layer parity/indexing is not locked
until FUT-01 builds from spec, and §10.5's pass criterion is only finiteness (no NaN/Inf),
which is met. CONTEXT D-21-04 and the code comments label it "representative." The large but
finite `physics ≈ 2.0e8` is expected for an untrained random SIREN and is explicitly
acknowledged in `21-VERIFICATION.md`. **Action: none required** — behavior matches the
stated acceptance contract.

## Notes

- Live `pinn/` implementation files were not used as grounding evidence (2026-05-19
  directive upheld); `21-CODE-DIVERGENCE.md` correctly forward-points FUT-01 implications.
- The "repair" pass (commit 87c84f5) successfully replaced the prior ungrounded PASS claims
  with re-derivable captured evidence — independently confirmed here.
