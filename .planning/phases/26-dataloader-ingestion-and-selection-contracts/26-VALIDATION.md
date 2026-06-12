---
phase: 26
slug: dataloader-ingestion-and-selection-contracts
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-12
---

# Phase 26 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> Phase 26 produces **no executable code** — it authors evidence packets and spec edits.
> Unlike Phase 25, Phase 26 DOES execute per-finding acceptance checks via disposable
> probes (D-14: each AC-PIPE check is defined numerically per VER-07 AND run before the
> finding's ledger row moves to `VERIFIED`). "Validation" here is therefore two-layer:
> doc-completeness review (packets, spec edits, ledger discipline) plus probe execution
> with re-derivable command + output capture (D-15). The full acceptance suite build and
> re-execution remain Phase 29 (VER-09).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — non-code phase. Verification is doc-completeness review + git invariants + disposable probes (spec-consistency greps and dataset probes reusing Phase 24 commands). |
| **Config file** | n/a |
| **Quick run command** | `git diff --check`; `test -x scripts/agent-commit`; `test -n "$GIT_AGENT_ID"` and `test -n "$GIT_AGENT_OWNED_PATHS"` before file mutation |
| **Full suite command** | n/a — full acceptance-suite execution is Phase 29 (VER-09); Phase 26 runs per-finding probes at adjudication time |
| **Estimated runtime** | ~5 seconds (git invariants); probes vary, all < 60s (filesystem scans / grep assertions over `simulation_data/` and specs) |

---

## Sampling Rate

- **After every task commit:** Run `git diff --check`; confirm the task's artifact exists on disk with required sections (grep assertions plus structural checks below).
- **After every plan wave:** Re-read each packet/spec edit produced in the wave against its requirement row in the map below; re-verify previously `VERIFIED` findings sharing edited spec sections or `Dependents` links (D-08 regression discipline — regression demotes to `IN_PROGRESS`).
- **Before `/gsd-verify-work`:** Every row in the Per-Requirement Verification Map must be ✅ or carry an explicit `DEFERRED`/STOP-gap disposition.
- **Max feedback latency:** 60 seconds (doc review + short probes, no build step).

---

## Per-Requirement Verification Map

| Req ID | Finding | Behavior | Verification Type | How verified (Phase 26) | Artifact |
|--------|---------|----------|-------------------|--------------------------|----------|
| PIPE-01 | B-06 | Stage 4→5 admission gate contract (final-timestamp threshold, stage-dependent snapshot minimums via locked M12 rule citation, rejection logging) | doc review + probe | packet defines AC-PIPE-01 numerically (pass criterion, data, exact command); probe executed and output captured in packet; spec edit cites locked M12 rule, never re-adjudicates it (D-02) | B-06 packet + `ctl_instruction.md` edit |
| PIPE-02 | B-11 | `id_to_path` from filesystem scan; trajectory ID ≠ array index invariant stated explicitly | doc review + probe | packet defines AC-PIPE-02; probe executed (e.g., scan-based ID/path demonstration on `simulation_data/`); invariant text present in spec edit | B-11 packet + spec edit |
| PIPE-03 | M11 | Blacklist exclusion: load at init, exclude, log count, fail loudly on blacklisted ID in batch; grounded in DATA-02 | doc review + probe | M11's existing packet `evidence/m11-m12-severity.md` EXTENDED (D-06), never duplicated; M12 content untouched; AC-PIPE-03 defined + executed; DATA-02 row cited not re-derived | extended M11 packet + spec edit |
| PIPE-05 | M13 | Stage-5 gold-existence check + fallback policy; source-silent/conflicting fallback → STOP gap, never invented | doc review (+ probe only if verdict grounded) | packet authored from full read of §3.4 Q-A4 + OI-7; either (a) no-fallback verdict adopted with grounding shown, or (b) `GAP-26-NN` recorded with all STOP-protocol fields and work halted (D-12) | M13 packet + (spec edit XOR gap entry) |
| PIPE-06 | D7 | Footer precedence, folder-default fallback, `tol_confidence` (`direct`/`inferred`), footer-as-metadata-only (completeness gate never depends on footer) | doc review + probe | packet defines AC-PIPE-06; OI-6 (no-footer probe-coverage gap) and OI-9 (DATA-05 rerun note) propagated into packet (D-13); probe executed | D7 packet + spec edit |
| PIPE-10 | D-03 | Format decision (HDF5 vs `.npy`/`.npz` vs txt/json) presented to USER with verified evidence; user-locked choice recorded in specs | doc review + user gate | dedicated `autonomous: false` plan; evidence presentation cites DATA-06 + dataset-scale facts; resolution-doc §3.6 Q-A6 position presented as candidate only; NO auto-selection under any mode (D-11); user choice recorded in `ctl_instruction.md` + packet + ledger in one commit | D-03 packet + user-gated spec edit |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Synthesis rows G1→B-06, G2→B-11, G3→M11, G4→M13 close with their parents; closure annotated in per-finding ledger notes (D-07) — verified as part of each parent's row.*

---

## Structural Checks

- [ ] Each new packet (B-06, B-11, M13, D7, D-03) is copied from `evidence/_TEMPLATE.md` and keeps the 12 `##` heading names; `### Dataset Evidence (§3b)` cites `24-VERIFIED-FACTS.md` rows, never re-derives.
- [ ] `evidence/README.md` ID→filename map updated in the same commit that adds each packet (D-05).
- [ ] M11 extension nests under existing sections of `m11-m12-severity.md`; `git diff` shows no M12-content modifications (D-06).
- [ ] Ledger status edits + Evidence-Packet links travel in the same commit as the underlying change (D-08); transition log entries follow `date commit-audit-label status→status (actor/plan)`.
- [ ] Every probe's command + output captured re-derivably in its packet (D-15); any probe scripts live under the phase directory, never under `pinn/`.
- [ ] Zero edits outside `ctl_instruction.md` / `pinn_architecture.md` (D-04): `git diff --stat` per plan shows only those two spec files plus `.planning/` artifacts.
- [ ] All citations directory-qualified (v1.4/issue-01 also had a "B-06" — namespace caution from CONTEXT.md).
- [ ] AC-IDs restricted to reserved AC-PIPE-01/02/03/05/06/10 — no new AC-IDs minted.

---

## Wave 0 Requirements

- [ ] Tag `v1.5-pre-phase-26` cut from `milestone/v1.5` HEAD at execution start (D-10).
- [ ] `scripts/agent-commit` executable and `GIT_AGENT_ID` / `GIT_AGENT_OWNED_PATHS` set before any file mutation (each plan preflights this).
- [ ] Phase 25 machinery present: `evidence/README.md`, `evidence/_TEMPLATE.md`, `evidence/m11-m12-severity.md`.
- [ ] Ledger present with the ten in-scope rows at `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md`.
- [ ] `26-GAPS.md` created on first STOP gap (not pre-created); `.planning/milestones/v1.5-GAPS.md` updated in step with it.

*No test-framework install needed — non-code phase.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Citation line-range accuracy | EVID-06 discipline (all packets) | Line ranges reference prose in source docs; correctness requires reading the cited spans | Open each cited file at the cited range; confirm the claim appears within it; search for claim text if line drift suspected, repair or fire STOP gap |
| Verdict grounding faithfulness | PIPE-01/02/03/05/06 | Whether a verdict transcribes vs invents requires comparing packet text against resolution-doc §3 Cluster A positions | Diff each packet's verdict + reasoning against the Q-A section mapped in `24.5-RESOLUTION-MAP.md` §3 |
| M13 STOP-gap disposition | PIPE-05 / D-12 | Whether OI-7's "defeater" disposes of the roadmap's STOP-gap expectation is a judgment call against success criterion 4 wording | Read packet §on Q-A4 + OI-7; confirm either grounded verdict or correctly-fielded `GAP-26-NN`; no third path |
| D-03 user-gate integrity | PIPE-10 / D-11 | Confirming the user actually decided (not auto-selected) requires checking the plan's interaction record | Confirm the plan is `autonomous: false`, the choice is recorded as user-issued, and the same commit carries spec + packet + ledger updates |
| Caveat propagation completeness | D-13 | OI-6/OI-7/OI-8/OI-9 routing spans multiple packets | Enumerate the four OI notes; confirm OI-6→D7, OI-7→M13, OI-8→M11 §4 hand-off note only, OI-9→wherever D7 footer evidence touches rerun files |

---

## Validation Sign-Off

- [ ] All tasks have doc-review/probe verification or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without an artifact-existence/grep check
- [ ] Wave 0 covers all MISSING references and open gap gates
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
