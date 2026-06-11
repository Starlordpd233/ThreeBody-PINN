---
phase: 24
slug: empirical-dataset-verification-and-correction-addendum
status: ready
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-10
---

# Phase 24 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **Phase nature:** Phase 24 IS the validation phase — its disposable probes ARE the acceptance
> checks (VER-09 model). There is no pytest/unittest harness; each probe is a self-contained
> script that prints `{value, command, dataset_path, date}` and writes nothing into
> `simulation_data/`. "Green" = the probe runs under `.venv/bin/python` and emits the recorded
> value into the verified-facts register. Source: 24-RESEARCH.md §"Validation Architecture".

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Disposable probe scripts under `probes/` (no pytest/unittest harness) |
| **Config file** | none — each probe is self-contained (D-01) |
| **Quick run command** | `.venv/bin/python probes/dataNN_*.py` (single probe) |
| **Full suite command** | run all six probes, capture stdout under `probes/outputs/` |
| **Estimated runtime** | ~5–60 s per probe; DATA-05 full-population mass sweep is the longest (first-block parse, still well under a minute on pilot timing) |

**Interpreter constraint (HARD):** every probe MUST be invoked as `.venv/bin/python` — it is the
only interpreter with numpy 2.2.0; system `python3` (homebrew 3.14.5) has NO numpy and DATA-05's
`np.allclose(rtol=1e-15)` aborts under it (24-RESEARCH.md Pitfall 1, VERIFIED in-session). The
DATA-01/03/06 probes need only stdlib but standardize on `.venv/bin/python` to kill the
split-interpreter footgun.

---

## Sampling Rate

- **After every probe authored:** run it once under `.venv/bin/python`, confirm it prints a value + command + dataset path + date, capture stdout under `probes/outputs/`.
- **After every plan wave:** confirm every CLM row owned by that wave has a `confirmed` / `corrected` / `unverified` verdict recorded in `24-VERIFIED-FACTS.md` with its probe citation (D-02/D-08).
- **Before phase exit:** all six probes have run; CLM-01..12 each carry a verdict; the addendum (or nil-addendum) is committed; the ledger seed exists at the stable path with the full finding inventory at PENDING.
- **Max feedback latency:** < 60 s (single probe run).

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 24-01-01 | 01 | 1 | DATA-01 | T-24-DS | Probe reads-only; never writes inside `simulation_data/` | probe | `.venv/bin/python probes/data01_id_gaps.py` | ❌ W0 | ⬜ pending |
| 24-01-02 | 01 | 1 | DATA-02, DATA-03 | T-24-DS | Probe reads-only; grep sweep confined to `simulation_data/Scripts/` + `Validation/` | probe | `.venv/bin/python probes/data02_blacklist.py`; `.venv/bin/python probes/data03_gold_gap.py` | ❌ W0 | ⬜ pending |
| 24-01-03 | 01 | 1 | DATA-01, DATA-02, DATA-03 | T-24-FACT | Register row carries probe command + dataset path + verdict (no issue-doc-sourced fact) | register | `grep -c 'CLM-0[123]' 24-VERIFIED-FACTS.md` ≥ 5 | ❌ W0 | ⬜ pending |
| 24-02-01 | 02 | 2 | DATA-04 | T-24-DS | Footer probe reads-only; "no footer" population characterized per D-07, not "partial footer" | probe | `.venv/bin/python probes/data04_footers.py` | ❌ W0 | ⬜ pending |
| 24-02-02 | 02 | 2 | DATA-05 | T-24-DS | `np.allclose(rtol=1e-15)` under `.venv/bin/python`; D-16 cluster check before verdict | probe | `.venv/bin/python probes/data05_mass_drift.py` | ❌ W0 | ⬜ pending |
| 24-02-03 | 02 | 2 | DATA-06 | T-24-DS | Distribution recorded (min/median/mode/max + modal counts), not a single example (D-09) | probe | `.venv/bin/python probes/data06_snapshots.py` | ❌ W0 | ⬜ pending |
| 24-02-04 | 02 | 2 | DATA-04, DATA-05, DATA-06 | T-24-FACT | Every register row has a verdict + probe citation; prose-sweep CLM-14+ rows added | register | `grep -c 'CLM-' 24-VERIFIED-FACTS.md` ≥ 12 | ❌ W0 | ⬜ pending |
| 24-03-01 | 04 | 1 | DATA-07 | T-24-GATE | Four OPEN WR decisions presented verbatim; NOT decided by the agent | checkpoint | human-check (AskUserQuestion gate) | n/a | ⬜ pending |
| 24-04-01 | 03 | 3 | DATA-07 | T-24-PKG | Addendum is a NEW sibling file; delivered package files byte-stable | addendum | `git diff --quiet -- '<research_package>/RESEARCH-CONTEXT-MASTER.md'` exits 0 | ❌ W0 | ⬜ pending |
| 24-04-02 | 03 | 3 | DATA-07 | T-24-FACT | Ledger seed has full inventory at PENDING; verified-facts annex linked at stable path | ledger | `grep -c 'PENDING' 24-ISSUE-LEDGER.md` ≥ 18 | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Note on Task IDs: plan 24-04 (WR user-gate) is Wave 1 and runs in parallel with plan 24-01; plan 24-03 (addendum + ledger) is Wave 3 and depends on both 24-02 and 24-04. The map above lists tasks by their owning plan.*

---

## Wave 0 Requirements

- [ ] `probes/data01_id_gaps.py` — DATA-01 ID-gap probe (pilot logic VERIFIED in 24-RESEARCH.md §Pattern 1)
- [ ] `probes/data02_blacklist.py` (+ grep sweep) — DATA-02 blacklist count + consumption map
- [ ] `probes/data03_gold_gap.py` — DATA-03 set-diff gold gap
- [ ] `probes/data04_footers.py` — DATA-04 footer schema + no-footer populations
- [ ] `probes/data05_mass_drift.py` — DATA-05 mass-drift, MUST run under `.venv/bin/python`
- [ ] `probes/data06_snapshots.py` — DATA-06 snapshot + final-timestep distributions
- [ ] `probes/outputs/` — captured stdout, committed
- [ ] `24-VERIFIED-FACTS.md` — verified-facts register (CLM/DATA-keyed)
- [ ] `24-ISSUE-LEDGER.md` — instantiated from v1.4 `16-ISSUE-LEDGER.md` schema (NOT redesigned)
- [ ] No framework install needed (numpy already present in `.venv` — VERIFIED)

*The pilot probe logic is verified in 24-RESEARCH.md (§Patterns 1–3); Wave 0 commits the disposable scripts and registers the outputs.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Four OPEN WR-01..04 decisions (CLM-05 split-vs-amend, WR-01 new-CLM-row, WR-02/03 channel, interim-vs-consolidated) | DATA-07 | Governance STOP protocol — schema + coordination decisions the agent must NOT invent; require user input | Present the four options exactly as 24-DISCUSSION-LOG.md §"Open Decisions — WR-01..04 Carry-In" frames them; record the user's answers before addendum assembly |
| DATA-01 nominal-range convention (if source-silent) | DATA-01 | Semantic STOP gap — the nominal-range basis ([0..3998] → 1,250 vs [0..3999] → 1,251) is not self-evidently grounded | If `ic_generation/` provenance does not ground the nominal range, STOP and surface a gap in `24-GAPS.md` + `v1.5-GAPS.md`; do not pick a convention |
| DATA-05 hierarchical mass baseline (if mismatches cluster + provenance ambiguous) | DATA-05 | Semantic STOP gap (D-16) — what Brutus actually consumed for perturbed hierarchical ICs may be ambiguous | If hierarchical mismatches cluster and `ic_generation/` provenance is ambiguous, STOP and surface a gap; do not pick a baseline |
| README contradiction → correction proposal (if any probe contradicts `simulation_data/Documentation/`) | DATA-01..06 | D-11 — dataset-doc edits require user sign-off, never autonomous | Record the contradiction in the register; propose the README correction to the user; do not apply autonomously |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify (probe command / grep gate) or are explicit human-check checkpoints (WR gate, STOP gaps)
- [x] Sampling continuity: every probe task has its own `.venv/bin/python` run; no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (six probe scripts + register + ledger seed)
- [x] No watch-mode flags (probes are one-shot scripts)
- [x] Feedback latency < 60 s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-06-10
