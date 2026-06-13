---
phase: 27
slug: sampling-precision-and-global-scale-contracts
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-13
---

# Phase 27 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **Phase nature:** spec-adjudication / transcription. Deliverables are Markdown
> framework-spec edits (`ctl_instruction.md`, `pinn_architecture.md`) + ledger
> transitions + evidence-packet links — NOT runtime code. The **acceptance-check
> assertions (AC-PIPE-04/07/08/09) ARE the sampling mechanism.** The "signal" for each
> contract is (1) the locked verdict present in the edited spec, (2) the rejected form
> absent as an operative rule (negative control), (3) the evidence-packet / dataset-fact
> citation present, (4) the ledger transition recorded. Source: `27-RESEARCH.md`
> "Validation Architecture".

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Spec-string assertions (`grep` / `grep -E`) over edited Markdown + re-derivable dataset probes (`.venv/bin/python .../probes/*.py`) |
| **Config file** | none — checks are inline commands or small disposable scripts under `.planning/phases/27-sampling-precision-and-global-scale-contracts/` (Codex discretion per CONTEXT) |
| **Quick run command** | per-AC `grep` block against `ctl_instruction.md` / `pinn_architecture.md` for the finding just edited |
| **Full suite command** | AC-PIPE-04 + AC-PIPE-07 + AC-PIPE-08 + AC-PIPE-09 + regression AC-PIPE-01 + AC-PIPE-06 |
| **Estimated runtime** | ~10 seconds (grep); ~1–3 min if the optional dataset probes are re-run |

---

## Sampling Rate

- **After every task commit:** Run the finding's own AC `grep` block (positive: verdict present; negative-control: rejected form appears ONLY in rejection context).
- **After every plan wave:** Run the finding's AC + any shared-section regression AC (AC-PIPE-01 for B-06 overlap; AC-PIPE-06 for D7 footer overlap).
- **Before `/gsd-verify-work`:** All four AC + both regression AC green; all touched ledger rows at `VERIFIED` / `DEFERRED`; same-commit discipline confirmed.
- **Max feedback latency:** ~30 seconds (grep-only); dataset probe cross-checks are corroborating, not blocking.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| PIPE-04 M12 | (M12/G5) | 1 | PIPE-04 | T-27-SPEC-DRIFT | spec states `min(n_pts_cap, n_snapshots)`, no `0.5×`, DATA-06 cited | spec-string + dataset-fact | `grep -E 'min\(n_pts_cap, n_snapshots' ctl_instruction.md` + `data06_snapshots.py` | ❌ W0 | ⬜ pending |
| PIPE-07 precision | (precision) | 2 | PIPE-07 | T-27-SPEC-DRIFT | float64 sufficiency + Decimal-as-classifier + staleness | spec-string + dataset-fact | `grep -i 'float64\|decimal.Decimal\|stale' ctl_instruction.md` + `data05_mass_drift.py` | ❌ W0 | ⬜ pending |
| PIPE-08 stage-query | (stage-query) | 2 | PIPE-08 | T-27-SPEC-DRIFT | stage-query signatures + `dt_out`/`n_snapshots` metadata + doc-03 ref | spec-string | `grep 'sample_replay(n, max_stage)\|sample_lookahead(n, stage)' ctl_instruction.md` | ❌ W0 | ⬜ pending |
| PIPE-09 compute_globals | (compute_globals) | 3 | PIPE-09 | T-27-SPEC-DRIFT | raw-mass `D≈4.6416` canonical; `6.694`/`M_tot_ref` rejected by name; `E_scale +1e-8` | spec-string + dimensional | `grep '6.694\|M_tot_ref\|1e-8' ctl §2.5` (rejected forms ONLY in rejection context) | ❌ W0 | ⬜ pending |
| AC-PIPE-01 regression | (M12/G5) | 1 | PIPE-01 (Ph26) | T-27-REGRESS | B-06 admission gate unchanged | spec-string | `grep '## Step 1A — Trajectory Admission Gate' ctl_instruction.md` (no `>= 200` floor) | ✅ (Ph26) | ⬜ pending |
| AC-PIPE-06 regression | (precision) | 2 | PIPE-06 (Ph26) | T-27-REGRESS | D7 footer/`param_provenance` provenance intact | spec-string | `grep 'param_provenance' ctl_instruction.md` (footer all-or-nothing + folder defaults) | ✅ (Ph26) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Threat refs are process-integrity (this phase has no runtime attack surface): T-27-SPEC-DRIFT = paraphrasing a locked verdict into something subtly different / citing the wrong or missing packet; T-27-REGRESS = silently regressing a Phase 26 contract in shared spec text.*

---

## Wave 0 Requirements

- [ ] Author runnable pass-criteria (inline `grep` blocks or disposable scripts under `.planning/phases/27-.../`) for AC-PIPE-04 / AC-PIPE-07 / AC-PIPE-08 / AC-PIPE-09 — the seeded AC-IDs exist; the runnable criteria are Phase 27's to define (evidence/README.md:113). NO new AC-IDs (D-06).
- [ ] Author/confirm the regression `grep` blocks for AC-PIPE-01 (B-06) and AC-PIPE-06 (D7) per CONTEXT D-14.
- [ ] Confirm the Phase 24 probes (`probes/data05_mass_drift.py`, `probes/data06_snapshots.py`) still run against current dataset state (corroborating cross-checks).

*No test-framework install needed — `grep` + existing `.venv` python probes.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Transcription fidelity — edited spec prose matches the locked verdict's *meaning*, not just the grep tokens | PIPE-04/07/08/09 | A grep confirms tokens are present but cannot confirm the surrounding prose faithfully states the locked convention without drift | Reviewer diffs the edited spec paragraph against the named packet anchor (e.g. `m11-m12-severity.md:105-113`) and confirms semantic equivalence |

*Remaining behaviors have automated (grep + dataset-probe) verification.*

---

## Validation Sign-Off

- [ ] All four contracts have an automated AC `grep` block (+ dataset probe where applicable) or a Wave-0 dependency to author it
- [ ] Sampling continuity: no contract edited without its AC + any shared-section regression AC run in the same wave
- [ ] Wave 0 covers all MISSING AC pass-criteria (the four AC blocks + two regression blocks)
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s (grep)
- [ ] `nyquist_compliant: true` set in frontmatter (after Wave 0 authors the AC blocks)

**Approval:** pending
