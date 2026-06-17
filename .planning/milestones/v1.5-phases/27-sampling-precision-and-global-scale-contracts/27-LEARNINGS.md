---
phase: 27
phase_name: "Sampling Precision and Global Scale Contracts"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 8
  lessons: 5
  patterns: 5
  surprises: 2
missing_artifacts: []
---

## Decisions

### M12 points-per-trajectory sampling rule locked in ctl § Mini-Batch Construction
Phase 27-01 replaced the stale "50% uniform / 50% weighted" prose in `ctl_instruction.md` Mini-Batch Construction (~1417) with the locked M12 contract: `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, sampled **without replacement**, with the default cap 32 flagged as example/non-evidence-based, and DATA-06 medians (61/127/1003) cited as the empirical grounding. The M12 ledger row and the G5 synthesis row both advanced PENDING → VERIFIED in the same atomic ledger edit, and `ac-pipe-04.sh` was authored with 8 region-scoped assertions including a vacuous negative control confirming `0.5 * n_snapshots` never appears as an operative rule.

**Rationale:** The locked third-position sampling rule from `evidence/m11-m12-severity.md:107` (resolution-doc §4.3:481-489) was the binding source; verbatim transcription with packet citation and DATA-06 medians satisfied EVID-06:99 while preventing the F-22 vacuous-factor drift back into the spec.

**Source:** `27-01-SUMMARY.md` — Tasks Completed / Files Changed / Verification Results / Self-Check

---

### PIPE-07 float64-sufficiency / Decimal-as-classifier precision note added to ctl §2.1
Phase 27-02 appended a blockquote precision note to `ctl_instruction.md §2.1` after the existing 1e-15 mass-invariance gate (line 578) stating: float64 is the data-side precision contract for all validation metrics and invariants; `decimal.Decimal` is reserved **only** as the future IC↔Brutus t=0 mass-gate failure classifier; the 70 historical base-hier mismatches were stale artifacts (0.1–1.0 mass units), not a precision failure; a future mismatch is a **fail** condition (quarantine), not a trigger to switch to Decimal. Cites `24-DATA05-RERUN-VALIDATION.md` (70/70 PASS) as evidence-of-record. The existing §2.1 gate is preserved verbatim — additive clarification, not convention change.

**Rationale:** Distinguishes the routine parsing/metric path (float64) from the failure-classification path (Decimal), pinning the DATA-05 rerun verdict in the spec and preventing a future "switch everything to Decimal" reflex; preserves the existing gate to avoid regressing the D-02/D-04 boundary that precision is data-side only.

**Source:** `27-02-SUMMARY.md` — What Changed (1) / Deviations from Plan / Verification Results

---

### PIPE-08 stage-query interface placed under §2.6 metadata schema, not co-located with Mini-Batch
Phase 27-03 added a `#### Data-side stage-query interface` sub-section under `ctl_instruction.md §2.6` (adjacent to the `dt_out`/`n_snapshots` metadata fields it references) with locked signatures `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)`, data-side semantics (cumulative D_{≤k} / next-stage D_{k+1}), and a SCOPE-11 blockquote deferral to doc-03 for M16 collocation-scaling and training-loop policy. A one-line FUT-01 visibility note was added to `pinn_architecture.md §3.1`. AC-PIPE-08 was authored with 7/7 positive assertions plus a blockquote-scoped negative control that filters blockquote lines before checking for forbidden training-loop/collocation-density policy text.

**Rationale:** Placement under §2.6 avoids region-collision risk with the 27-01 Mini-Batch edits and keeps the interface adjacent to the metadata it references; the blockquote-scoped negative control enforces the SCOPE-11 boundary mechanically (the deferral note is a blockquote, so filter-then-check correctly excludes it from the forbidden-policy assertion).

**Source:** `27-03-SUMMARY.md` — Files Changed / Verification Results / Decisions Made (Placement F-02, A1 guard, Negative control scope)

---

### PIPE-09 normative compute_globals contract landed in ctl §2.5 with raw-mass D canonical
Phase 27-04 landed the normative `compute_globals` global-scale contract in `ctl_instruction.md §2.5`: raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` is canonical (HC-6 / PHYS-01); mass-fraction `D = (G·M_tot·T²)^(1/3) ≈ 6.694` and `M_tot_ref` are **rejected by name** with the explicit "No configuration parameter may select the mass-fraction form" line; `E_scale = |median(E)| + 10^{-8}` is canonicalized (2-of-3 editable-spec majority; `pinn_architecture.md §5.2` already matched); Plummer-vs-additive-ε (PHYS-03) rule restated with `ε_inv = 1e-10` preserved; admitted-set scope is post-Step-1A, post-blacklist, post-DATA-05-quarantine per GAP-27-02 Option A; SCS / Phase 28 untouched per D-14 dependents note.

**Rationale:** Locked D value unchanged (D-03); preserves the v1.4 raw-mass PHYS-01 convention, locks the convention migration (not a local formula correction) into §2.5, and uses the "rejected by name" wording to prevent silent re-introduction via a downstream configuration flag.

**Source:** `27-04-SUMMARY.md` — What was built / Artifacts produced / Phase-exit gate

---

### GAP-27-01 RESOLVED-WITH-INSTRUCTION Option C — thin pointer packet for PIPE-07 evidence
User selected Option C on 2026-06-13: Phase 27-02 authored a minimal `evidence/data05-precision.md` packet that (1) records the locked verdict, (2) names acceptance check AC-PIPE-07 (no new AC IDs), (3) carries the status-transition log, and (4) in its dataset-evidence section **cites** the Phase 24 artifacts (`24-DATA05-RERUN-REMEDIATION.md`, `24-DATA05-RERUN-VALIDATION.md`, the mass-drift/footer ledger rows) without re-deriving them. A corresponding ID→Filename map entry was added in the same commit. This satisfies EVID-06:99's "completed evidence packet + verdict" gate while honoring CONTEXT D-05's "consume, don't re-derive" — reconciling both readings.

**Rationale:** Re-home an already-grounded verdict into a thin pointer packet rather than either re-deriving a full packet (A) or skipping the packet entirely (B); preserves the per-finding-packet uniformity for the audit trail while avoiding duplication of the already-grounded Phase 24 evidence; sets the reusable precedent for future non-conflict spec-edit findings whose verdict predates the packet system.

**Source:** `27-GAPS.md` GAP-27-01 Resolution note; `27-02-SUMMARY.md` Decisions (transcribed verbatim, two-phase SHA backfill)

---

### GAP-27-02 RESOLVED-WITH-INSTRUCTION Option A — sign off compute_globals admitted-set scope
User follow-up on 2026-06-14 selected Option A: the `compute_globals` admitted-set scope (per-IC energies over the admitted set after Step-1A admission, blacklist exclusion, and DATA-05 quarantine) is approved as the locked convention and was transcribed into `ctl_instruction.md §2.5` as clean normative spec text. The "flagged for spec-author sign-off" caveat was **not** preserved in normative spec text; it remains only in this gap record and the evidence packet. All other PIPE-09 legs remain as already grounded; SCS/Phase 28 text remains untouched.

**Rationale:** The packet's explicit sign-off flag withheld final authority; landing the scope unflagged before sign-off would have blessed an unreviewed convention, violating the "do NOT invent content where source materials are silent/ambiguous" governance. Option A supplies the user instruction that GAP-27-02 surfaced; the audit trail (sign-off flag in packet, resolved entry in gap register) is preserved off-spec.

**Source:** `27-GAPS.md` GAP-27-02 Resolution note; `27-04-SUMMARY.md` Deviations

---

### Two-phase SHA backfill pattern (F-08) used for all four phase plans
All four Phase 27 plans used the two-phase SHA backfill pattern: the substantive spec-edit commit writes a `<pending-27-NN-sha>` placeholder into the evidence-packet transition log and the ledger row, then a separate `verify(27-NN)` provenance commit backfills the real SHA. Commit pair examples: `6e81d14f` + `da2149d` (M12/G5), `b6fe225d` + `70dd29b` (PIPE-07), `c647fc3` + `8fb87fa` (PIPE-08), `731c795e` + `95575fd9` (PIPE-09). For PIPE-07, the first entry's authoring SHA (`09e37f8`) was left intact per F-08.

**Rationale:** The substantive commit cannot know its own SHA at write time, and the transition log must record the SHA of the edit it describes; the two-phase pattern decouples the spec edit from the SHA backfill while keeping both in the same logical plan and a single ledger-evidence commit-pair.

**Source:** `27-01-SUMMARY.md` Commits; `27-02-SUMMARY.md` Decisions (F-08) / Commits; `27-03-SUMMARY.md` Tasks Completed; `27-04-SUMMARY.md` Commits

---

### Phase-exit gate uses F-13/F-16 to require all in-scope ledger rows at VERIFIED with no OPEN in-scope gap
Phase 27-04 closed only after all five in-scope ledger rows reached VERIFIED: M12 (line 26), G5 (line 33), mass-drift (line 41), footer (line 40), D=6.694 (line 39). `27-GAPS.md` has no OPEN in-scope gap (GAP-27-01 RESOLVED-WITH-INSTRUCTION 2026-06-13 Option C; GAP-27-02 RESOLVED-WITH-INSTRUCTION 2026-06-14 Option A). `27-VALIDATION.md` was flipped to `nyquist_compliant: true`, `wave_0_complete: true`, all rows green. The full AC suite (AC-PIPE-04, AC-PIPE-07 inline, AC-PIPE-08, AC-PIPE-09, AC-PIPE-01 regression, AC-PIPE-06 regression, AC-PIPE-10 conditional regression) was re-run 2026-06-14 with all PASS.

**Rationale:** The phase-exit gate is a hard precondition for handoff to Phase 28/29; F-13/F-16 keep any IN_PROGRESS/FIX_APPLIED row or any OPEN in-scope gap from being silently left behind when the next phase starts consuming the spec text.

**Source:** `27-04-SUMMARY.md` Phase-exit gate (F-13/F-16); Acceptance checks (full-suite re-run 2026-06-14)

---

## Lessons

### Re-locate edit targets by content marker, not by cited line number (D-18 / F-19)
The fixed line numbers cited in plan `read_first` blocks (e.g. `1410-1430`, `800-825`, `744-774`, `~773`) are the line numbers AT PLAN-AUTHORING TIME. Wave 1 (Plan 27-01) inserts ~12-40 new lines into `ctl_instruction.md` (Mini-Batch transcription), so every later wave's ctl anchors shift by the insertion delta — already observed: the 27-04 `E_scale` "~line 773" anchor is actually `:771`. Executors MUST re-locate every edit target by **section heading and content marker** (e.g. `grep -n '## Mini-Batch Construction'`, `grep -n 'Per-trajectory data-loss point count'`, `grep -n 'Global-scale D'`), not by the cited line number. Each plan's pre-transcription content-marker verification (audit F-04) is the enforced form of this rule.

**Context:** Surfaced by the Phase 27 plan audit (F-19) and codified as CONTEXT D-18; F-04 enforces a content-marker pre-check before transcription; without this rule, multi-wave phases drift the spec text into regions the next plan did not audit.

**Source:** `27-CONTEXT.md` D-18; `27-04-SUMMARY.md` Artifacts produced (`pinn_architecture.md §5.2` anchor already canonical)

---

### Autonomous-STOP operationalization parks affected plan, never silently resolves (D-15 / F-06)
Under `autonomous: true`, a STOP-protocol gap neither silently resolves nor proceeds. The affected plan **parks** at the gap, records a full STOP-protocol entry in `27-GAPS.md`, and the phase-exit gate blocks while any in-scope gap is OPEN. **Independent** plans/waves may proceed; the halted plan resumes only when the user resolves the gap. Grounding: `CLAUDE.md` STOP protocol step 5 ("halted work stays halted until the user provides instruction") and the explicit "There is no exception" clause govern. `autonomous: true` removes mid-run human checkpoints; it does **not** license inventing past a source-silent decision.

**Context:** Surfaced by the Phase 27 plan audit (F-06) and codified as CONTEXT D-15; demonstrated in 27-04 when GAP-27-02 gated the §2.5 normative consolidation until the 2026-06-14 user follow-up approved the admitted-set scope as Option A; the dependent plan parked at the gap, recorded the entry, and resumed on instruction.

**Source:** `27-CONTEXT.md` D-15; `27-GAPS.md` GAP-27-02 (parked 27-04 Task 2); `27-04-SUMMARY.md` Phase-exit gate

---

### STOP-recovery contract: never revert ledger row past PENDING after a mid-wave halt (D-16 / F-09)
If a STOP/gap fires mid-wave after a ledger row has advanced past `PENDING` (the EVID-06 packet-before-edit gate), **do NOT revert** the row status — revert is a destructive operation requiring user approval. Leave the row at its current status (`IN_PROGRESS` or `FIX_APPLIED`), record the halt in `27-GAPS.md`, and let the gap's resolution note carry the resume path. The phase-exit gate will keep the phase open until the gap is resolved and the row reaches `VERIFIED`. Grounding: `CLAUDE.md` destructive-operation policy.

**Context:** Codified as CONTEXT D-16 from audit F-09; the rule preserves the progress made before the halt and avoids destructive git operations on ledger state; the phase-exit gate (F-13/F-16) is the blocking mechanism, not a rewind.

**Source:** `27-CONTEXT.md` D-16

---

### Owned-paths discipline is advisory, not hook-enforced — self-audit before commit (D-17 / F-21)
`scripts/agent-commit` enforces only that `GIT_AGENT_OWNED_PATHS` is non-empty; `.githooks` → `validate_staged_paths.py` validates blocked patterns and blob size but does **not** cross-check staged paths against declared owned paths. Owned-paths discipline is therefore advisory: each executor MUST self-audit `git diff --cached --name-only` before committing and stage only its plan's explicit owned paths. Grounding: verified against `scripts/agent-commit` and `.githooks/validate_staged_paths.py` during the audit.

**Context:** Codified as CONTEXT D-17 from audit F-21; the lesson is that hook enforcement is a partial check, not a guarantee — agent behavior is the final layer; the practical mitigation is a `git diff --cached --name-only` self-audit step before invoking `scripts/agent-commit`.

**Source:** `27-CONTEXT.md` D-17

---

### Phase 27 stayed on the data-side boundary: precision/global-scale wording, no architecture/forward-policy invention
All four PIPE edits landed in `ctl_instruction.md` (primary) and `pinn_architecture.md` (secondary, only where the data-side metadata/query interface or architecture-facing precision/global-scale wording needs FUT-01 visibility). No edits to live `pinn/` code, no M16/training-loop/collocation-density policy invented (SCOPE-11 deferral to doc-03), no Phase 28 SCS/SASD/IPR/PSC metric definitions, no `sampling_method.md` edits, no `data_quality_assessment.md` edits, no new processed-training-data format decisions. The D-04 "deferral wording = factual forward references only" rule was honored throughout — whenever a proposed edit needed a policy for downstream consumers, the plan stopped and surfaced the gap rather than choosing.

**Context:** Honored throughout all four plans per D-02/D-04; the data-side boundary is the v1.5 specwork/trainex split: specwork lands the spec text, trainex/FUT-01 consumes it; crossing the boundary without user instruction is exactly the "do not invent" governance failure the STOP protocol guards against.

**Source:** `27-CONTEXT.md` D-02/D-04; all four SUMMARY files Deviations from Plan (None sections)

---

## Patterns

### Atomic ledger + spec + evidence + AC commit pattern (D-07)
Each touched ledger row moves through the Phase 25 lifecycle (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, or explicit `DEFERRED`). Ledger status, evidence links, spec edits, and acceptance-check results travel in the same logical plan commit (or commit-pair with the two-phase SHA backfill). Synthesis rows close with parent findings unless the Phase 25 protocol explicitly requires a separate packet (G5 closes-with-M12 by D-08). No new AC IDs are minted — the seeded AC-PIPE-04/07/08/09 are the only acceptance checks; if a required process artifact or packet mapping is missing or ambiguous, that is a process-schema STOP gap (D-06), not a license to invent a new schema.

**When to use:** Any v1.5 spec-edit phase that touches an in-scope ledger row, edits a framework spec, advances an evidence-packet transition, and runs an AC. The pattern preserves the audit chain (issue → evidence → spec → AC → ledger transition) as a single reviewable unit.

**Source:** `27-CONTEXT.md` D-06/D-07/D-08; all four SUMMARY files Commits / Verification Results

---

### Spec-string acceptance check (grep-based) with positive assertions + scoped negative control
Every AC script in Phase 27 is a region-scoped, grep-based positive-assertion suite plus a blockquote-scoped or context-scoped negative control. Examples: AC-PIPE-04 (8 region-scoped assertions + vacuous F-22 control confirming `0.5 * n_snapshots` never appears as an operative rule), AC-PIPE-07 (7 positive assertions + negative control confirming `decimal.Decimal` appears exactly once, in classifier context only), AC-PIPE-08 (7/7 positive assertions + blockquote-scoped negative control that filters blockquote lines before checking for forbidden training-loop/collocation-density policy text), AC-PIPE-09 (14 assertions: canonical-D + Plummer positive + 6.694/M_tot/E_scale/arch/SCS negative-controls + arch §5.2 consistency). The blockquote-scoping pattern is the right answer when a deferral note is blockquoted: filter-then-check correctly excludes it from the forbidden-policy assertion.

**When to use:** Any AC for a v1.5 spec-edit finding where the contract has both positive requirements (a value/convention must appear) and rejection requirements (a rejected convention must not appear, including in scope language). The negative control is what catches a future spec-edit that re-introduces a rejected convention (e.g. `D = 6.694`, `0.5 * n_snapshots`).

**Source:** `27-01-SUMMARY.md` Verification Results; `27-02-SUMMARY.md` AC-PIPE-07 / AC-PIPE-06 D7 Regression; `27-03-SUMMARY.md` AC-PIPE-08; `27-04-SUMMARY.md` AC-PIPE-09

---

### Regression discipline: re-run all shared-section ACs after every plan (D-14)
Any edit to sections touched by Phase 26 triggers targeted rechecks for previously verified rows sharing that text, especially B-06 admission, D7 footer provenance, and D-03 HDF5 wording if nearby text is moved. Phase 27-01 re-ran AC-PIPE-01 (B-06) and confirmed the B-06 region is byte-stable. Phase 27-02 re-ran AC-PIPE-06 (D7) and confirmed the footer/param_provenance text is preserved. Phase 27-03 re-ran AC-PIPE-06 and AC-PIPE-10 (conditional, for the stage-query placement decision) and confirmed byte-identical. The full-suite re-run on 2026-06-14 (after 27-04) covered AC-PIPE-01, AC-PIPE-04, AC-PIPE-06, AC-PIPE-07, AC-PIPE-08, AC-PIPE-09, AC-PIPE-10 conditional — all PASS.

**When to use:** Any v1.5 spec-edit phase where multiple plans touch the same framework spec; the regression AC set is the cost of multi-wave coordination; the discipline prevents Phase 26 contracts from being silently regressed by Phase 27 wording changes.

**Source:** `27-01-SUMMARY.md` AC-PIPE-01 Regression (B-06); `27-02-SUMMARY.md` AC-PIPE-06 D7 Regression; `27-03-SUMMARY.md` D7 regression (AC-PIPE-06); `27-04-SUMMARY.md` Acceptance checks (full-suite re-run 2026-06-14)

---

### Mechanical/operational choices noted in artifact, semantic/process choices surface as gap (D-09 / governance)
Mechanical/operational decisions (heading capitalization, exact heading names and placement within `ctl_instruction.md` / `pinn_architecture.md`, exact packet filename within the sanitization rule, exact plan count and wave grouping) are agent-discretion items per the CONTEXT "Codex's Discretion" section. They are noted in the plan/artifact and proceeded with. Semantic decisions (mass encoding raw vs fraction, the admitted-set scope sign-off, any sub-flavor the source punted on) **MUST surface** as a gap with full STOP-protocol fields, never invent. The pattern is: pre-classify the decision before transcribing; if classification is "mechanical" or "operational coordination," proceed with a minimal note; if "semantic" or "process-artifact schema" or "cross-phase reframing," stop and record the gap.

**When to use:** Every v1.5 spec-edit decision; the pre-classification step is what prevents the "I'll make a reasonable choice and note it" failure mode that the governance explicitly forbids.

**Source:** `27-CONTEXT.md` Codex's Discretion; `27-GAPS.md` GAP-27-01 (process-artifact schema), GAP-27-02 (semantic); `CLAUDE.md` governance

---

### Thin pointer packet pattern for non-conflict findings whose verdict predates the packet system (Option C)
When a non-conflict finding's verdict already lives in a prior-phase artifact (e.g. Phase 24 rerun remediation/validation) rather than an `evidence/{id}.md` packet, the thin pointer packet pattern records the locked verdict, names the acceptance check (no new AC IDs), carries the status-transition log, and **cites** the prior-phase artifacts in its dataset-evidence section without re-deriving them. A corresponding ID→Filename map entry is added in the same commit. This satisfies EVID-06:99's "completed evidence packet + verdict" gate while honoring the "consume, don't re-derive" rule; sets a reusable precedent for future non-EVID-10 findings whose verdict predates the packet system.

**When to use:** Any future non-conflict spec-edit finding whose verdict already lives in a Phase 24 (or prior-phase) artifact; PIPE-07 is the first such case in the v1.5 sequence (M12 and D=6.694 are EVID-10 packets; G5 closes-with-M12 by D-08; B-06/B-11/D7/M13/D-03 all have packets).

**Source:** `27-GAPS.md` GAP-27-01 Resolution note (Option C); `27-02-SUMMARY.md` What Changed (4) and Decisions (F-08)

---

## Surprises

### The 70 historical base-hier mass mismatches were stale artifacts, not a precision failure
DATA-05's 70/70 rerun validation reframes a candidate "we need Decimal everywhere" reflex into "the historical base-hier outputs were 0.1–1.0 mass units off because the ICs that generated them are stale; current ICs are canonical and float64 is sufficient." This is consequential: it pins the precision contract on a **remediation** boundary (rerun from current ICs) rather than a **computation** boundary (switch to Decimal), and it makes the future IC↔Brutus mass-gate failure a quarantine condition (fail, do not silently coerce). The reframing only became visible because Phase 24's GAP-24-01 was RESOLVED-WITH-INSTRUCTION and the 70/70 rerun was validated before Phase 27 planning — without that chain, the spec might have over-engineered the precision path.

**Impact:** Reorients the precision contract from "Decimal is the answer" to "float64 is the answer, Decimal is the failure classifier"; prevents a systemic over-engineering path and pins a precise quarantine semantics for future failures.

**Source:** `27-02-SUMMARY.md` What Changed (1); `27-GAPS.md` GAP-27-01 Resolution note; `27-CONTEXT.md` D-05 (DATA-05 precision consumes the Phase 24 rerun remediation/validation artifacts)

---

### SCS / Phase 28 was deliberately untouched across all four PIPE-09-adjacent edits
Despite the compute_globals contract landing in ctl §2.5 and the D-14 dependents note explicitly forbidding SCS changes, the temptation to "while I'm in the section, also touch SCS" was real and was resisted across all four plans. The D-03 "no re-adjudication of locked rulings" rule and the D-14 "regression discipline" rule both apply: SCS lives in Phase 28 territory, and any Phase 27 wording change to SCS-adjacent text would have silently expanded scope. The 27-04 SUMMARY's "SCS untouched per D-14 dependents note" and the AC-PIPE-09 negative controls (`SCS` exclusion from forbidden-text checks) make this a deliberate boundary, not an oversight.

**Impact:** Phase 27 lands a complete, scope-respecting §2.5 contract without bleeding into Phase 28 territory; the SCS untouched rule is enforced both by the plan author (no SCS edits) and by the AC negative controls (mechanical detection of any drift).

**Source:** `27-04-SUMMARY.md` Deviations / Threat Flags (None); AC-PIPE-09 negative controls; `27-CONTEXT.md` D-03/D-14
