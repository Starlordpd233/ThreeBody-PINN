# Phase 36: Acceptance Checks, Re-verification & Handoff — Research

**Researched:** 2026-06-30
**Domain:** GSD milestone-closure / verification process (v1.6 specwork closure; no external tech stack)
**Confidence:** HIGH (every claim traces to an in-repo artifact read this session)

## Summary

Phase 36 is the v1.6 closure packet. It does not transcribe contracts — Phases 33/34/35 already did that and recorded per-phase verification. Phase 36 (a) builds a Phase-36-owned acceptance-check manifest spanning every v1.6 contract, (b) executes fresh disposable probes (spec-consistency + small formula-sanity, never touching `pinn/`) with hashed evidence, (c) drives the Phase 32 issue ledger to terminal state, (d) reconciles the four framework-spec `SI-*` entries, (e) writes a fixed/unchanged/deferred handoff with FUT-01/FUT-04 divergence routing, and (f) reconciles the stale `REQUIREMENTS.md` Status column and `ROADMAP.md` progress table to ledger-terminal values.

The current state is well-characterized and stable: the Phase 32 ledger has **18 rows, 16 `VERIFIED`, 2 `PENDING` (`D-05`, `D-06`)**; `REQUIREMENTS.md` has **32 traceability rows, 13 `Pending` / 19 `Complete`** with `VER-13..18` Pending and `LOOP-04/07/08` stale-Pending; the SI universe is **4 IDs** (`SI-CTL-001`, `SI-PINN-002`, `SI-PINN-003`, `SI-DQA-003`); and the `ROADMAP.md` progress table still shows Phase 34 "In Progress 1/5" dated 2026-06-23 even though Phase 34 closed VERIFIED. The two `PENDING` ledger rows are a process-state lag, not an open decision: `D-05`/`D-06` verdicts are `RESOLVED-WITH-INSTRUCTION` in `32-GAPS.md` and `v1.6-GAPS.md`, and their downstream transcription (Phase 33 `CURR-05` + Phase 35 loss-side) is complete — so D-36-07's verify-and-promote-else-`BLOCKED` path applies.

**Primary recommendation:** Source every manifest pass-criterion from the **framework spec section + Phase 32 ledger verdict + the owning phase's `AC-*` verification record** — NOT from the literal `REQUIREMENTS.md`/`ROADMAP.md` description text, which is stale (it still describes the M15 cap table, the `8.5` clip constant, the M16 `n_col` formula, and D-04 Option-C preservation that the adjudicated verdicts rejected or deferred). Then run disposable probes against the transcribed contract, close the ledger fail-closed, and reconcile statuses by manual diff-reviewed edits.

## Architectural Responsibility Map

Phase 36 is a closure/verification phase, not a multi-tier app. The "tiers" are the planning artifacts that own each closure responsibility.

| Capability (Phase 36 requirement) | Primary Owner Artifact | Secondary | Rationale |
|---|---|---|---|
| Acceptance-check inventory (R1/VER-13) | `36-ACCEPTANCE-MANIFEST.md` | framework specs + ledger + 33/34/35-VERIFICATION | Manifest is the organizing spine; pass criteria already exist upstream |
| Fresh probe execution + evidence (R2/VER-15) | `36-PROBE-RESULTS.md` + `evidence/` + `probes/` | Phase 21/29 probe precedent | Disposable, hashed, fail-closed, never touches `pinn/` |
| Ledger terminal-state gate (R3/VER-16) | `36-VERIFICATION.md` ledger-state table | `32-ISSUE-LEDGER.md` (parsed fresh) | Fail-closed: any nonterminal in-scope row → BLOCKED |
| SI reconciliation (R4/VER-18) | `36-HANDOFF.md` SI table | `ctl_instruction.md` + `pinn_architecture.md` | Fresh grep is the mechanical acceptance check |
| Fixed/unchanged/deferred + FUT routing (R5/VER-17) | `36-HANDOFF.md` + `36-CODE-DIVERGENCE.md` | `21-/29-CODE-DIVERGENCE.md` precedent | Implementation-shaped findings route to FUT-01/FUT-04, never implemented |
| 32/32 traceability + status reconciliation (R6/VER-14) | `36-VERIFICATION.md` audit + manual edits to `REQUIREMENTS.md`/`ROADMAP.md` | `32-ISSUE-LEDGER.md` terminal state | Each flip must match a terminal ledger row; manual diff-reviewed |

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VER-13 | Every v1.6 contract has a numerically-defined acceptance check (pass criterion + data/expression + command/function) | R1 source map below: each contract already has an AC and a spec-section pass criterion; manifest aggregates them |
| VER-14 | Roadmap maps every v1.6 requirement to exactly one phase (32/32), beginning at Phase 30 | Traceability table read: 32 rows, 1 phase each; coverage block confirms 4+5+5+8+4+6=32 |
| VER-15 | Acceptance checks executed via disposable probes; failing check blocks completion; probes never touch `pinn/` | R2: Phase 21/29 probe precedent (driver script, hashed stdout, exit-0 gate); formula-sanity vs spec-consistency classification below |
| VER-16 | Iterative re-verification loop; ledger terminal (`VERIFIED`/`DEFERRED`+blocker) before close; demote on regression | R3: ledger state (16 VERIFIED, 2 PENDING=D-05/D-06) + D-36-07 verify-and-promote-else-BLOCKED path |
| VER-17 | Handoff identifies fixed/unchanged/deferred; FUT-01/FUT-04 divergence updated for implementation-shaped findings | R5: `21-`/`29-HANDOFF.md` + `CODE-DIVERGENCE.md` precedent; trainex-r1 todo routed as input only |
| VER-18 | Remaining curriculum/training-loop `SI-*` reviewed; each retired-with-backref or preserved-with-reason; none assumed | R4: fresh grep = 4 IDs; per-ID disposition evidence below; SI-DQA-003 STOP-governed (D-36-18) |

## User Constraints (from CONTEXT.md)

### Locked Decisions (36-CONTEXT.md)
- **D-36-01:** Four-artifact closure packet: `36-ACCEPTANCE-MANIFEST.md`, `36-PROBE-RESULTS.md`, `36-VERIFICATION.md`, `36-HANDOFF.md`.
- **D-36-02:** Raw probe output under a Phase 36 evidence directory; SHA-256 hashes recorded in `36-PROBE-RESULTS.md` (Phase 21 pattern).
- **D-36-03:** SI reconciliation lives inside `36-HANDOFF.md` (no separate SI report).
- **D-36-04:** Prefer small disposable spec-consistency + formula-sanity probes over replaying historical 33/34/35 commands; cite prior verification as provenance but make Phase 36 evidence fresh.
- **D-36-05:** Manual accumulator probe style: deterministic commands, PASS/FAIL labels, explicit stdout/stderr capture, nonzero exit on required-check failure.
- **D-36-06:** Plan must include a protected-path check proving probes neither execute against nor modify live `pinn/`.
- **D-36-07:** All in-scope ledger rows require terminal state. `D-05`/`D-06` are still `PENDING` but their verdicts are owner-ratified (`RESOLVED-WITH-INSTRUCTION`); recommended path: verify the locked verdicts are correctly transcribed downstream (Phase 33 `CURR-05` geometric `s_min` gate + `epsilon_inv=1e-10`; Phase 35 matched-Plummer loss-side) and, if clean, promote both to `VERIFIED` via explicit owned-path ledger edit; if divergent, record `BLOCKED` and route back. NOT a re-litigation of the verdicts.
- **D-36-08:** Parse ledger status fresh; report exact counts; do not trust stale summaries.
- **D-36-09:** Reconcile all four SI IDs (`SI-CTL-001`, `SI-PINN-002`, `SI-PINN-003`, `SI-DQA-003`); mechanical check = fresh grep over both specs.
- **D-36-10:** Resolved/retired SI row needs a phase/commit back-reference; preserved row needs a written reason + downstream owner; no row assumed irrelevant.
- **D-36-11:** `36-HANDOFF.md` classifies each ledger row exactly once as fixed / intentionally unchanged / deferred.
- **D-36-12:** FUT-01/FUT-04 sections route implementation-shaped findings downstream without implementing them.
- **D-36-13:** Fold `trainex-r1-research-handoff.md` only as a handoff-routing input; do NOT execute trainex/ERW research.
- **D-36-14:** Explicit owned paths + `scripts/agent-commit`; broad staging forbidden.
- **D-36-15:** Exclude unrelated user-owned dirty changes from Phase 36 commits.
- **D-36-16:** This discuss run stops before planning; do not auto-dispatch plan-phase.
- **D-36-17:** Reconciling the stale `REQUIREMENTS.md` Status column and `ROADMAP.md` progress table to ledger-terminal values is **in scope** (grounded by `34-VERIFICATION.md:102`). `LOOP-04/07/08` read `Pending` but are `VERIFIED`/`SATISFIED`; the ROADMAP table shows Phase 34 "In Progress 1/5" (2026-06-23). Edits are **manual** (the gsd-tools state/roadmap mutating verbs emit malformed output here); each flip must match a terminal ledger row; diff before commit; `ROADMAP.md` + `REQUIREMENTS.md` are Phase 36 owned paths.
- **D-36-18:** `SI-DQA-003`'s disposition (retire-with-backref vs preserve-with-reason) is **NOT decided here** — STOP-governed Issue-03-relevance judgment for execution. Non-binding lean: preserve-with-reason (conservation/SCS-gate citation, locked post-v1.3, outside the curriculum/training-loop surface); if genuinely source-silent, surface a STOP gap rather than invent.

### Claude's / Planner Discretion (36-CONTEXT.md)
The planner may choose the number/grouping of plan files, individual probe-script names, and whether the manifest is helper-generated or authored markdown — provided every locked acceptance criterion is mechanically verifiable and the packet stays fail-closed.

### Deferred Ideas (OUT OF SCOPE)
- Executing the trainex-r1 external research handoff (FUT/trainex).
- Training-loop/DataLoader/ALM implementation, adaptive-stage EDA, Stage-0 pilot calibration, data regeneration (FUT-01/FUT-04/FUT).

## Project Constraints (from CLAUDE.md / AGENTS.md)
- **STOP protocol in full** (v1.6 is a designated adjudication milestone): do not invent spec content, AC thresholds, numeric values, verdicts, or SI dispositions where sources are silent. Surface, never fill.
- **Specwork-only (SCOPE-13/14/15):** spec-edit targets are `ctl_instruction.md` + `pinn_architecture.md` only; `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md`/`review-of-framework.md`/`stage-strat-revision.md` read-only (SCOPE-09). Phase 36 does NOT edit framework specs (it verifies them) — its only spec-adjacent writes are the ledger and the `REQUIREMENTS.md`/`ROADMAP.md` status reconciliation.
- **`pinn/` is NOT grounding and never a probe target** (SCOPE-10). Issue-03 "Canonical" `pinn/` citations are overridden.
- **Commit policy:** `scripts/agent-commit` with `GIT_AGENT_ID` + explicit `GIT_AGENT_OWNED_PATHS`; no broad staging; `.planning/` / multi-file commits need a body + `Agent-Assisted-By` trailer; no push from `milestone/*`.
- **STATE.md** mutates only through GSD state handlers (do not hand-edit); `REQUIREMENTS.md`/`ROADMAP.md` reconciliation is hand-edited with reviewed diff (per 36-SPEC Constraints).

---

## R1 — Acceptance-Check Manifest Source Map (VER-13)

**Pass-criterion authority order (use this, not the stale requirement text):** (1) the transcribed framework-spec section; (2) the Phase 32 ledger row verdict; (3) the owning phase's `AC-*` verification record. The `REQUIREMENTS.md`/`ROADMAP.md` prose is stale for several rows and must not be the source (see Common Pitfalls).

Every v1.6 contract already has a located pass criterion. **No contract criterion was unlocatable** — the manifest is an aggregation task, not a discovery task.

| Contract (req) | AC ID | Pass criterion (adjudicated) | Spec location | Owning phase / evidence |
|---|---|---|---|---|
| CURR-01 adaptive stage assignment | AC-CURR-01 | Methodology tokens present (offline EDA → PCA + clustering + quantile; Stage-2 hierarchical-gold / Stage-5 quasi-random-gold); population safeguard owner-pending, NOT locked | `ctl_instruction.md:315-334,1632-1639` | Phase 33 / `evidence/adaptive-stage-assignment.md` |
| CURR-02 L_max/tau_L | AC-CURR-02-LMAX | `L_max = M_tot·r_char·v_char` characteristic scale; raw-mass `D ≈ 4.6416` active (`6.694` rejected provenance); Rosenstein revisable baseline; shadow/PCA shortcut NOT normative | `ctl_instruction.md:984-1003,1270-1273,1309-1335` | Phase 33 / `evidence/l-max-tau-l.md` |
| CURR-02 M7 tau_L exclusion | AC-CURR-02-M7 | `tau_L` is staging/eval metadata, outside IC13 by design | `ctl_instruction.md:1311-1340` | Phase 33 / `evidence/m7-tau-l-ic13-exclusion.md` |
| CURR-03 stage transitions | AC-CURR-03 | ADVANCE / RECOVER / HALT-REVIEW state machine anchored in `## Stage Transition Criteria`; thresholds provisional pending FUT Stage-0 pilot | `ctl_instruction.md:1836-1893` | Phase 33 / `evidence/d5-stage-transitions.md` |
| CURR-04 Stage 0-6 inventory | AC-CURR-04 | Raw un-clipped `L_norm` metadata + mandatory nonfinite/near-degenerate `L_max` guard; "No global clamp is authorized"; `np.clip` gate NOT locked | `ctl_instruction.md:1187-1211` | Phase 33 / `evidence/m6-l-norm-metadata.md` |
| CURR-05 s_min gate | AC-CURR-05 | Unsoftened geometric `s_min` stage gate; `max(s_min,eps)` rejected per PHYS-03; matched-Plummer loss-side owned by Phase 35; `epsilon_inv=1e-10` / `epsilon_train=1e-5` dual context | `ctl_instruction.md:287-303` | Phase 33 consumes Phase 32 `evidence/d-05-s-min-frame.md` |
| LOOP-01 replay/lookahead | AC-LOOP-01 | `B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` guard; provisional; edge-case policy (GAP-34-01 Option A) transcribed | `ctl_instruction.md:1787-1799` (canonical, SI-PINN-003) | Phase 34 / `evidence/b-07-replay-lookahead-batching.md` |
| LOOP-02/03 point sets + mixed sampling | AC-LOOP-02 | Two independent point sets (data-fidelity vs collocation, 8192/4096 provisional); data-fidelity 50/50 retained, collocation 50/50 deferred (NOT mandated) | `ctl_instruction.md:1801-1818` | Phase 34 / `evidence/b-08-data-vs-collocation-points.md` |
| LOOP-04 merged gradient clipping | AC-LOOP-04 | Mechanism `clip_value = C_stage·median(grad_norm_history)` canonical in pinn §4.4; C-schedule `7-10 / 5 / 3` canonical in ctl; **`8.5` absent both files**; bidirectional anchors | `pinn_architecture.md:714-728` + `ctl_instruction.md:1825-1849` | Phase 34 consumes Phase 32 `evidence/m14-gradient-clipping.md` |
| LOOP-05 ALM μ_p clamp | AC-LOOP-05 | ALM deferred/optional; dense-residual ALM rejected from default loss; `[1e-4,100]` clamp conditional only | `pinn_architecture.md:674` | Phase 34 / `evidence/alm-mu-p-clamp.md` |
| LOOP-06 dt_out collocation scaling | AC-LOOP-06 | Realized-as-deferred; candidate direction only; **no probe-able `n_col=...` formula**; inverse form NOT adopted | `ctl_instruction.md:1819-1823` | Phase 34 / `evidence/m16-dt-out-collocation-scaling.md` |
| LOOP-07 IPR/PSC training-side | (no ledger AC) | Provisional carry-forward; `IPR`/`PSC`/`provisional`/`VAL-03`/`VAL-04` tokens present | `ctl_instruction.md:770` | Phase 34 (provisional, no dedicated ledger row) |
| LOOP-08 SASD training-side | (no ledger AC) | Provisional carry-forward; `SASD`/`provisional`/`VAL-02` tokens present | `ctl_instruction.md:684` | Phase 34 (provisional, no dedicated ledger row) |
| LOSS-01 loss scaling | AC-LOSS-01 | Dimensionless `L_data`/`L_physics`/`L_energy`; AD chain factors `d²r'/du²=4·d²r'/dτ²`, `dr'/du=2·dr'/dτ`; no linear-momentum term | `pinn_architecture.md:310,890` + `ctl_instruction.md:1737` | Phase 35 / `evidence/ns-18-loss-scaling-units.md` |
| LOSS-01 componentwise AD | AC-LOSS-01-AD | Componentwise AD, canonical `u=t/T` leaf; summed-output VJP rejected | `pinn_architecture.md:310` (PHYS-02) | Phase 35 / `evidence/ns-12-componentwise-ad.md` |
| LOSS-02 energy-weight schedule | AC-LOSS-02 | **Adjudicated M15:** retain PHYS-05 `λ_E^max ≤ 1.0`; issue-doc cap-table replacement REJECTED; logging-first; dominance reweighting deferred | `pinn_architecture.md:667` + `ctl_instruction.md:1739` | Phase 35 / `evidence/m15-energy-weight-schedule.md` |
| LOSS-03 Huber-δ | AC-LOSS-03 | `delta_E=1.0` baseline retained; empirical/median-scaled calibration deferred; no per-stage δ table locked | `pinn_architecture.md:537` + `ctl_instruction.md:1741` | Phase 35 / `evidence/ns-13-energy-huber-delta.md` |
| LOSS-04 causal mode | AC-LOSS-04 | **D-04 Option A:** per-time causal weighting `w_n = exp(-η_c·Σ_{m<n} stopgrad(R̄_m))`, `w_1=1`, `η_c=1`; dense-residual pseudo-ALM rejected; scalar ALM deferred P2 | `pinn_architecture.md:424` + `ctl_instruction.md:1749,1803` | Phase 35 / D-04 ledger row + GAP-32-01 |
| Headline: D=6.694 conflict | AC-EVID-15-D-CONFLICT | `D ≈ 4.6416` active; `6.694` rejected provenance only | `ctl_instruction.md` (D≈4.6416 present, 6.694 absent from pinn) | Phase 32 / `evidence/d-6-694-conflict.md` |
| Headline: D-05 s_min frame | AC-EVID-15-D05 | Owner Option A (geometric gate + matched-Plummer loss-side) | consumed by CURR-05 | Phase 32 / `evidence/d-05-s-min-frame.md` (ledger PENDING → promote per D-36-07) |
| Headline: D-06 epsilon strategy | AC-EVID-15-D06 | Owner dual-context (`epsilon_inv=1e-10` / `epsilon_train=1e-5`) | consumed by CURR-05 static invariants | Phase 32 / `evidence/d-06-epsilon-strategy.md` (ledger PENDING → promote per D-36-07) |

**Manifest acceptance check (SPEC R1):** count entries against v1.6 contract IDs; every row must have non-empty `pass criterion`, `data/expression`, `command/function`; duplicate/missing contract IDs fail. Sort rows by requirement-family ID for stable diffing (Edge: ordering).

**LOOP-07/08 caveat:** these two have **no dedicated Phase 32 ledger row** (provisional carry-forwards). The manifest must still carry a row for each (pass criterion = provisional-token presence per `34-VERIFICATION.md` truths 6-7), but their evidence anchor is `34-VERIFICATION.md`, not the ledger. This interacts with R6 reconciliation — see Findings F2.

---

## R2 — Probe & Evidence Pattern (VER-15)

### Precedent structure (Phase 21 + Phase 29)
- **Evidence layout (Phase 21):** raw stdout per probe under `…/21-…/evidence/*.stdout.txt`; probe scripts under `…/probes/`; a `python_environment.stdout.txt` capture; **SHA-256 recorded for every file** in `21-PROBE-RESULTS.md`. Each probe section records Status, Command, Raw-stdout-evidence path, SHA-256, Observed metric, Pass criterion.
- **Driver + table (Phase 29):** `run-ac-suite.sh` re-runs all probes and exits 0; `29-ACCEPTANCE-EVIDENCE` AC table columns = `AC-ID | Asserts | Command/Function | Input data | Pass criterion | Result | Evidence path`. Probe types were grep spec-consistency probes (`ac-pipe-*.sh`, `ac-val-*.sh`) plus one dataset set-difference probe (`ac-pipe-05.py` → `PASS 184/184`, counts derived not hard-coded). A guard `grep -lE 'pinn/' ac-*` must return empty.
- **Recommended Phase 36 layout:** `36-ACCEPTANCE-MANIFEST.md` (static inventory) + `36-PROBE-RESULTS.md` (run record, one PASS/FAIL/SKIP per manifest row + hashes) + `evidence/` (hashed stdout/stderr) + `probes/` (disposable scripts). One driver (e.g. `run-ac-suite.sh`) exits nonzero if any required check fails (fail-closed, D-36-05).

### Probe classification (which contracts admit a formula-sanity probe vs spec-consistency only)

**Formula-sanity probes (small, disposable, documented sample — never `pinn/`):**
- **CURR-02 L_max / D:** numerically check `D = (G·T²)^(1/3) ≈ 4.6416` and `L_max = M_tot·r_char·v_char` on a documented toy sample; assert `D ≈ 4.6416` and `6.694` rejected. (`tau_L = 1/λ_max` estimator is owner-pending → structural only, not numeric.)
- **LOOP-04 clip-value behaviour:** evaluate `clip_value = C_stage·median(history)` on a synthetic gradient-norm history for the `7-10 / 5 / 3` C-schedule; assert monotone-by-stage and **`8.5` absent**.
- **LOSS-01 AD chain factors:** verify `d²r'/du² = 4·d²r'/dτ²` and `dr'/du = 2·dr'/dτ` symbolically/numerically on a synthetic trajectory (τ = 2u−1).
- **LOSS-02 λ_E schedule:** evaluate the **transcribed adjudicated** weight rule and assert PHYS-05 `λ_E^max ≤ 1.0` holds; assert the rejected `{0:1…6:500}` cap table and `λ_E = 1000` are NOT present (negative check). *Do not probe the stale cap-table formula.*

**Spec-consistency probes only (token/structure/negative checks):** CURR-01, CURR-03, CURR-04, CURR-05, M7, LOOP-01, LOOP-02/03, LOOP-05, LOOP-06 (deferred — assert no `n_col=` formula), LOOP-07, LOOP-08, LOSS-01-AD, LOSS-03, LOSS-04, and all SI rows + the D-conflict. These assert discriminating tokens are present in the transcribed contract (would fail against pre-phase boilerplate) and that rejected/forbidden strings are absent.

**Protected-path guard (D-36-06, mandatory):** a probe/guard proving (a) `grep -lE 'pinn/' probes/*` empty, and (b) `git diff --name-only` over `pinn/` + frozen/read-only specs empty for all Phase 36 commits. Phases 33/34/35/29 all ran this guard; replicate it.

---

## R3 — Ledger Terminal-State (VER-16)

**Fresh parse (this session) of `32-ISSUE-LEDGER.md`:** 18 rows. **16 `VERIFIED`, 2 `PENDING` (`D-05`, `D-06`).** Verdict mix: 14 `accept-resolution`, 3 `defer-with-blocker` (`M16`, `NS-13`, `ALM μ_p clamp` — each carries a written blocker), 1 (`D-04`) accept-resolution.

| Status | Count | Rows |
|---|---|---|
| VERIFIED | 16 | D-04, B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12, NS-13, NS-18, adaptive-stage-assignment, D=6.694, L_max/tau_L, ALM μ_p clamp |
| PENDING | 2 | **D-05, D-06** |

**The two PENDING rows are NOT an open decision.** Their owner verdicts are `RESOLVED-WITH-INSTRUCTION` in `32-GAPS.md` (GAP-32-02 Option A; GAP-32-03 dual-context) and mirrored in `v1.6-GAPS.md`. The ledger row stayed `PENDING` because downstream transcription was Phase 33/35-owned; both are now complete:
- D-05 → Phase 33 `CURR-05` transcribed unsoftened geometric `s_min` (`ctl_instruction.md:287-303`); Phase 35 owns matched-Plummer loss-side.
- D-06 → Phase 33 transcribed `epsilon_inv=1e-10` static invariants alongside `epsilon_train=1e-5`; Phase 35 preserves the loss-side lock.

**D-36-07 closure path (do NOT propose verdicts):** Phase 36 verifies the locked D-05/D-06 verdicts are correctly transcribed in those downstream sections and, if clean, **promotes both ledger rows `PENDING → VERIFIED` via an explicit owned-path ledger edit** (citing AC-EVID-15-D05 / -D06 + the CURR-05 token check). If transcription is missing or divergent, Phase 36 records **BLOCKED** and routes back rather than promoting. Fail-closed.

**Re-verify-after-batch / demote-on-regression mechanic (VER-16):** the ledger discipline (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, with re-verification of previously `VERIFIED` rows a batch could regress, demoting to `IN_PROGRESS` on regression) is the loop established in Phase 32 and operated by 34/35. Phase 36's own edits (D-05/D-06 promotion + any status reconciliation) are an "edit batch": after them, re-run the cross-file consistency suites the edit could have touched (it should not touch framework specs at all) and confirm no previously-VERIFIED contract regressed. Concurrency: pre-write SHA-256 freshness check on the ledger before writing (Phase 34 `ledger_post_34_01_sha256` precedent).

**Terminal-state acceptance (SPEC R3):** `36-VERIFICATION.md` ledger-state table counts must match a fresh parse; any `PENDING`/`IN_PROGRESS`/`FIX_APPLIED` in-scope row → record BLOCKED, not complete; every `DEFERRED` row needs an explicit blocker + handoff destination (the three `defer-with-blocker` rows already carry blockers routed to FUT).

---

## R4 — Source-Issue Reconciliation (VER-18)

**Fresh `rg -n "SI-[A-Z]+-[0-9]+"` over both framework specs (this session) = 4 distinct IDs:**

| SI ID | Location(s) | What the citation asserts | Candidate disposition EVIDENCE | Issue-03 relevance |
|---|---|---|---|---|
| `SI-CTL-001` | `ctl_instruction.md:2140` | Input-vector dimensionality inconsistency — "Resolved by v1.4 finding B-03. See Phase 17 input contract." | **Retire-with-back-reference** (already self-states resolved by v1.4 B-03 / Phase 17). Back-ref: v1.4 Phase 17. | Low — v1.4 (doc-01) input contract, not curriculum/training-loop |
| `SI-PINN-002` | `pinn_architecture.md:1047` | Three preserved author comments: (1) omega_0 dynamic scheduling detail, (2) hidden-layer detail, (3) batch-construction inconsistency — comment (3) **resolved under SI-PINN-003 by Phase 34**; (1)/(2) remain "documented for future reconciliation" | **Preserve-with-reason** lean: comments (1)/(2) are architecture (doc-01) author notes, outside the Issue-03 curriculum/training-loop surface; comment (3) retired with Phase 34 back-ref. **Precedent caution:** v1.5 Phase 29 treated the analogous SI-PINN-002 preserve-with-reason as a **D-08 STOP human-approval checkpoint** | Partial — only comment (3) is Issue-03; (1)/(2) are doc-01 |
| `SI-PINN-003` | `ctl_instruction.md:1793` (canonical) + `pinn_architecture.md:353,1053,1056,1059` | Batch-construction inconsistency with CTL plan — **RESOLVED by Phase 34**; `ctl_instruction.md` Mini-Batch Construction is canonical; `pinn_architecture.md §3.1` points to it; "is not consistent…" string removed | **Retire-with-back-reference** (Phase 34 / AC-LOOP-01/02; RESOLVED log present in pinn `:1056-1060`) | High — directly Issue-03 batch construction (LOOP-01/02) |
| `SI-DQA-003` | `ctl_instruction.md:548` | Inline citation on the conservation/SCS gate ("locked post-v1.3"): `SCS = log10(eps_H)`, REJECT if `SCS > -5`, Plummer `eps=1e-10` in V — data-quality lineage | **STOP-governed / D-36-18 — characterize, do NOT decide.** Non-binding lean: preserve-with-reason (data-quality/conservation-gate citation, locked post-v1.3, outside the curriculum/training-loop Issue-03 surface). If genuinely source-silent on Issue-03 relevance, surface a STOP gap. | Low/ambiguous — conservation-gate/data-quality, v1.5 (doc-02) lineage; SCS gate is SCOPE-12 hard constraint |

**Acceptance (SPEC R4):** a fresh grep must produce no entry absent from the `36-HANDOFF.md` SI table; no entry marked resolved/irrelevant without a citation or reason; rows ordered by spec path + line number. The fresh grep is the mechanical check — re-run it at handoff-write time against the same checked working-tree snapshot (concurrency edge).

**Important nuance:** v1.4 `21-HANDOFF.md` listed `SI-DQA-003` as living in `data_quality_assessment.md:324-327` and preserved-untouched. The current v1.6 grep finds `SI-DQA-003` as an **inline citation in `ctl_instruction.md:548`** (the transcribed conservation gate), a different surface. Reconcile against the current `ctl_instruction.md` occurrence, not the archived v1.4 location.

---

## R5 — Handoff + FUT Routing (VER-17)

**Handoff table shape (from `21-HANDOFF.md` / `29-HANDOFF.md`):**
1. Evidence Used
2. **Fixed** — in-scope findings `VERIFIED` in the ledger (one row per finding)
3. **Intentionally Unchanged** — false-positive / valid-existing-convention non-changes (e.g., M6 `L_norm` clamp under Jacobi IC₁₃; M15 cap-table rejection; M16/NS-13/ALM defers carried as deferred)
4. **Deferred** — `defer-with-blocker` rows with written blocker + downstream owner (M16, NS-13, ALM μ_p clamp; plus owner-pending FUT items: population floor GAP-33-01, tau_L estimator GAP-33-02, L_norm clip GAP-33-03, causal-exponent clip bound, epsilon train-vs-validate sensitivity)
5. **SI Metadata Reconciliation** (the R4 table — D-36-03 keeps it inside the handoff)
6. **FUT-01 / FUT-04 / Consumption Notes**

**Each ledger row appears exactly once across Fixed/Unchanged/Deferred (D-36-11 / Edge adjacency).** Empty outcome tables fail (the ledger has in-scope findings). Rows ordered by finding ID; FUT sections grouped by downstream owner.

**FUT divergence-record convention:** precedents are `21-CODE-DIVERGENCE.md` (v1.4, forward-pointing code-alignment hints) and `29-CODE-DIVERGENCE.md` (v1.5, FO-1/FO-2 forward obligations). Recommend a Phase 36 `36-CODE-DIVERGENCE.md` (forward-pointing only; `pinn/` references permitted ONLY here per SCOPE-10). The eventual `pinn/STATUS.md` is the FUT-01 target. Implementation-shaped findings to route there:
- **FUT-01 (rebuild from specs):** componentwise AD executable strategy (NS-12), gradient-clipping mechanism realization (M14), batch constructor / DataLoader (B-07/B-08/LOOP-01/02/03), ALM update + μ_p clamp (LOOP-05), causal-mode mechanics (D-04/LOSS-04).
- **FUT-04 (resume training-loop impl + calibration):** adaptive-stage EDA + population floor (CURR-01/GAP-33-01), Stage-0 pilot threshold calibration (CURR-03 thresholds, D5-05), tau_L estimator/units selection (GAP-33-02), Huber-δ empirical calibration (NS-13), dt_out collocation scaling (M16), IPR/PSC/SASD training-side numeric confirmation (LOOP-07/08), epsilon train-vs-validate sensitivity (D-06 caveat).
- **trainex-r1 todo (D-36-13):** `.planning/todos/pending/trainex-r1-research-handoff.md` is a **routing input only** — mention it in the FUT/trainex routing section (it concerns review/handoff of trainex-r1 r1a/r1b research sub-packages); do NOT execute the ERW workflow.

---

## R6 — Traceability + Status Reconciliation (VER-14)

**Traceability table (fresh read of `REQUIREMENTS.md`):** 32 rows, each mapped to exactly one phase, beginning at Phase 30. Coverage block: 4 PKG + 5 EVID + 5 CURR + 8 LOOP + 4 LOSS + 6 VER = 32. **32/32 mapping holds** (VER-14 audit: boundary count must be exactly 32; one phase per row; no duplicate/missing).

**Status column (fresh read): 13 `Pending` / 19 `Complete`.** The Pending set = PKG-05, PKG-06, PKG-07, PKG-08, LOOP-04, LOOP-07, LOOP-08, VER-13, VER-14, VER-15, VER-16, VER-17, VER-18.

**Stale rows to reconcile (D-36-17), grounded in `34-VERIFICATION.md:102`:**
- `LOOP-04` reads `Pending` but M14 is `VERIFIED` in the ledger and `34-VERIFICATION.md` records LOOP-04 SATISFIED. → flip to `Complete`, matched to the terminal M14 ledger row.
- `LOOP-07` / `LOOP-08` read `Pending` but `34-VERIFICATION.md` records them SATISFIED (provisional carry-forward). → flip to `Complete`, **but they have NO ledger row** — anchor = `34-VERIFICATION.md`, not the ledger (see Finding F2; the SPEC's "match a terminal ledger row" rule is literally unsatisfiable for these two).
- `VER-13..18` flip to `Complete` only after Phase 36's own terminal evidence lands (self-referential; flip at Phase 36 closure).

**ROADMAP.md staleness (fresh read):**
- Milestone line 11: "Phases 30–33 complete, Phase 34 next" — stale (35 complete; 36 next).
- Phase checklist: `- [ ] Phase 34` (line 76) and `- [ ] Phase 36` (line 80) unchecked; Phase 34 is actually complete (GAP-34-01 cleared by Plan 34-06; `34-VERIFICATION.md` status `passed`, gaps_remaining `[]`).
- Phase 34 Plans block: "1/5 plans executed", 34-02..05 unchecked — stale (all five consumed; LOOP rows VERIFIED via Plan 34-05).
- Progress table (line 249): Phase 34 "In Progress 1/5", Completed blank — stale.
- "Last updated: 2026-06-23" — stale.

**Reconciliation method (SPEC Constraints / D-36-17):** perform edits **manually** with a reviewed diff — the gsd-tools state/roadmap mutating verbs emit malformed output in this repo. Each flipped flag must match a terminal Phase 32 ledger row (except the no-ledger-row rows — see F2); add `.planning/ROADMAP.md` + `.planning/REQUIREMENTS.md` to Phase 36 owned paths; stage explicitly. **STATE.md still uses GSD state handlers** (do not hand-edit STATE.md). Idempotency: re-running reconciliation with no ledger change reproduces the same flags; a flip lacking a matching terminal ledger row fails (precision: integer-exact 32, no fractional count).

**Precedent:** v1.5 Phase 29 hit the identical situation — VER rows left `Pending`/unchecked because `REQUIREMENTS.md` was outside executor owned-paths; `29-VERIFICATION.md` "Reconciliation Recommendation" flipped the checkboxes + traceability rows + the ROADMAP milestone bullet as the post-verification step. v1.6 R6 codifies that as in-scope.

---

## Validation Architecture

> Nyquist validation enabled (no `workflow.nyquist_validation: false` found). Phase 36 is specwork-only: "tests" are deterministic disposable probes, not a unit framework.

### Test Framework
| Property | Value |
|---|---|
| Framework | None project-wide; `python3` + `bash` deterministic accumulator probes (Phase 21/29 pattern). `tests/test_phase12_validation.py` (PASS/FAIL accumulator) and `tests/git_policy/test_git_policy.py` (`unittest`) are local precedents. |
| Config file | none — explicit commands captured in `36-PROBE-RESULTS.md` |
| Quick run command | `bash .planning/phases/36-acceptance-checks-re-verification-handoff/run-ac-suite.sh` |
| Full suite command | same driver (re-runs every probe, exits nonzero on any required FAIL) |

### Phase Requirements → Observable → Check
| Req | Observable that proves it | Check type | Command (illustrative) | Exists? |
|---|---|---|---|---|
| VER-13 | Every contract row has non-empty pass criterion + data + command | manifest audit | `python3` parse of `36-ACCEPTANCE-MANIFEST.md` | ❌ Wave 0 |
| VER-15 | Each manifest row → one PASS/FAIL/SKIP with hashed evidence; no `pinn/` touch | probe run | `run-ac-suite.sh`; `grep -lE 'pinn/' probes/*` empty | ❌ Wave 0 |
| VER-16 | Ledger counts match fresh parse; 0 nonterminal in-scope rows | ledger audit | `python3` parse of `32-ISSUE-LEDGER.md` | ❌ Wave 0 |
| VER-18 | Fresh SI grep ⊆ handoff SI table | grep diff | `rg -n "SI-[A-Z]+-[0-9]+"` vs handoff table | ❌ Wave 0 |
| VER-17 | Each ledger row appears once across fixed/unchanged/deferred | handoff audit | `python3` set check | ❌ Wave 0 |
| VER-14 | Exactly 32 rows, one phase each, post-reconciliation no flag contradicts ledger | traceability audit | `python3` parse of traceability table | ❌ Wave 0 |

### Sampling Rate
- **Per probe / per manifest row:** the row's `run-ac-suite.sh` line.
- **Per Phase 36 batch (ledger promote, status reconcile):** re-run the full AC suite + protected-path guard + ledger freshness SHA check.
- **Phase gate:** full suite green + ledger terminal + SI grep clean + 32/32 audit pass before `/gsd-verify-work`.

### Sampling-rate adequacy
Closure has no time-series behavior to under-sample; the risk is *missing a contract*, mitigated by deriving manifest rows from the enumerated v1.6 contract IDs (32-row traceability + ledger) so coverage is exhaustive, not sampled.

### Fail-closed gate
Any of: missing manifest field, required probe FAIL/missing-evidence, nonterminal in-scope ledger row, uncited SI disposition, handoff row count mismatch, traceability ≠ 32, or any `pinn/`/framework-spec/frozen-file diff → record **BLOCKED**, route back to the originating phase, do not mark Phase 36 complete (SPEC Prohibition 2; Constraints "fail-closed").

### Wave 0 Gaps
- [ ] `36-ACCEPTANCE-MANIFEST.md` — covers VER-13 (aggregates the R1 source map)
- [ ] `probes/` disposable scripts + `run-ac-suite.sh` driver — covers VER-15
- [ ] `evidence/` raw stdout/stderr + SHA-256 — covers VER-15
- [ ] ledger-audit + traceability-audit + handoff-audit probes — VER-16/14/17
- [ ] SI-grep diff probe — VER-18
- [ ] protected-path guard probe — D-36-06 / Prohibition 1

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| AC table / probe-results schema | A new format | Phase 29 `ACCEPTANCE-EVIDENCE` columns + Phase 21 `PROBE-RESULTS` hash blocks | Locked precedents; downstream readers expect them |
| Evidence hashing | Ad-hoc | `sha256` per output file recorded in markdown (Phase 21/29) | Re-derivable invariant per commit policy |
| Ledger freshness under concurrency | Optimistic write | Pre-write SHA-256 equality check (Phase 34 `ledger_post_34_01_sha256`) | Parallel sessions edit `.planning/` |
| Status reconciliation | gsd-tools roadmap/state mutating verbs | Manual diff-reviewed edits (SPEC Constraint) | Those verbs emit malformed output in this repo |
| SI disposition where source-silent | Invent retire/preserve | STOP gap (D-36-18) | Adjudication-milestone governance |

## Common Pitfalls

### Pitfall 1: Sourcing pass criteria from stale REQUIREMENTS.md / ROADMAP text
**What goes wrong:** The manifest transcribes `λ_E(k)=min(10^(k-3),cap[k])` with `cap={0:1…6:500}` (LOSS-02), the `8.5` clip constant (LOOP-04), `n_col ∝ dt_base/dt_out` (LOOP-06), or D-04 Option-C preservation — all of which the **adjudicated verdicts rejected or deferred**. `35-VERIFICATION.md` and `34-VERIFICATION.md` explicitly flag this stale preview wording.
**How to avoid:** Pass criteria come from the framework-spec section + ledger verdict + `AC-*` record. Add negative checks (assert the rejected strings are absent).

### Pitfall 2: Treating D-05/D-06 PENDING as an unresolved decision
**What goes wrong:** Re-litigating the s_min/epsilon verdicts, or blocking on them as if owner input is missing.
**How to avoid:** They are `RESOLVED-WITH-INSTRUCTION`; the ledger lag is a transcription-state artifact. Follow D-36-07: verify transcription, promote-or-BLOCK. Do not propose new verdicts.

### Pitfall 3: Probing the wrong target
**What goes wrong:** A formula-sanity probe imports or executes `pinn/` code, or a probe targets a deferred contract (LOOP-06) that has no probe-able formula.
**How to avoid:** Probes are self-contained on documented toy samples; `grep -lE 'pinn/'` guard; deferred contracts (LOOP-06, LOSS-03 calibration, ALM, tau_L estimator) get spec-consistency/negative checks only.

### Pitfall 4: Absorbing unrelated dirty files
**What goes wrong:** Staging `AGENTS.md` (modified) or the untracked `36-PATTERNS.md` into a Phase 36 commit.
**How to avoid:** Explicit owned-path staging only (D-36-14/15). Current dirty set: `AGENTS.md` (modified) + `.planning/phases/36-…/36-PATTERNS.md` (untracked) — neither is Phase 36 closure output unless the plan explicitly owns it.

### Pitfall 5: SI grep snapshot drift
**What goes wrong:** The handoff SI table is built from one grep, then a later edit changes SI lines, so the table no longer matches.
**How to avoid:** Build the SI table and run the acceptance grep against the same checked working-tree snapshot (concurrency edge R4).

## Environment Availability
| Dependency | Required by | Available | Version | Fallback |
|---|---|---|---|---|
| `python3` | formula-sanity + audit probes | ✓ (used by 33/34/35 verification) | system | — |
| `bash` | driver `run-ac-suite.sh` | ✓ | system | — |
| `rg` (ripgrep) | SI grep / token checks | ✓ (used this session) | — | `grep -rn` |
| `sha256` (`shasum -a 256`) | evidence hashing | ✓ (Phase 21/29 used it) | — | `openssl dgst -sha256` |
| `scripts/agent-commit` | committing closure artifacts | ✓ | repo script | — |

No external packages installed → **no Package Legitimacy Audit required** (closure phase, repo-internal only).

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | `D = (G·T²)^(1/3) ≈ 4.6416` is numerically reproducible from the documented constants for a formula-sanity probe | R2 | LOW — value is the v1.5-locked convention; probe will confirm or surface a real discrepancy |
| A2 | A Phase 36 `36-CODE-DIVERGENCE.md` is the right FUT-divergence artifact name (vs folding FUT notes into `36-HANDOFF.md`) | R5 | LOW — both Phase 21 and Phase 29 used a `*-CODE-DIVERGENCE.md`; planner may choose |
| A3 | LOOP-07/LOOP-08 should be flipped `Pending → Complete` using `34-VERIFICATION.md` as the (non-ledger) anchor | R6 / F2 | MEDIUM — the locked rule says "match a terminal ledger row"; these have none (see Finding F2 — surfaced, not resolved) |

*All other claims are `[VERIFIED]` against an in-repo artifact read this session.*

## Sources

### Primary (HIGH — read directly this session)
- `36-SPEC.md`, `36-CONTEXT.md` (locked R1–R6, D-36-01..18)
- `32-ISSUE-LEDGER.md` (18 rows parsed), `32-GAPS.md` (GAP-32-01/02/03 resolutions), `.planning/milestones/v1.6-GAPS.md`
- `REQUIREMENTS.md` (32-row traceability, VER-13..18, SCOPE-12..15), `ROADMAP.md` (Phase 36 + protocol blocks + progress table), `STATE.md`
- `33-VERIFICATION.md`, `34-VERIFICATION.md` (line 102 reconciliation deferral), `35-VERIFICATION.md`
- `ctl_instruction.md` (SI-CTL-001:2140, SI-DQA-003:548, SI-PINN-003:1793), `pinn_architecture.md` (SI-PINN-002:1047, SI-PINN-003:1056) — fresh `rg` SI grep = 4 IDs
- Precedents: `21-PROBE-RESULTS.md`, `21-HANDOFF.md`, `29-VERIFICATION.md`; `36-PATTERNS.md` (prior-session precedent map)
- `.planning/todos/pending/trainex-r1-research-handoff.md` (FUT routing input)

### Secondary (MEDIUM)
- `AGENTS.md` / `CLAUDE.md` v1.6 STOP-protocol + commit governance

### Candidate verdict source (transcribe-unless-fails, NOT authoritative)
- `…/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` (cited via 32-GAPS line ranges; not re-adjudicated here)

## Metadata
**Confidence breakdown:**
- R1 manifest source map: HIGH — every contract's AC + spec line located in a verification file.
- R2 probe pattern: HIGH — Phase 21/29 precedents read directly.
- R3 ledger state: HIGH — fresh parse, 16/2 confirmed.
- R4 SI universe: HIGH — fresh grep = 4 IDs matching anchors.
- R5/R6 reconciliation: HIGH for the stale-row inventory; MEDIUM for the no-ledger-row reconciliation rule (Finding F2).

**Research date:** 2026-06-30
**Valid until:** ~7 days (active milestone; ledger/traceability mutate as Phase 36 executes)

---

## Findings for Orchestrator (potential STOP gaps)

> Returned for the orchestrator to log if it agrees — NOT written to any gap register by this research, and NOT resolved here.

**F1 — PKG-05..08 read `Pending` while Phase 30 is `Complete`; outside the D-36-17 ledger-anchored rule.** `REQUIREMENTS.md` shows PKG-05/06/07/08 = `Pending`, but `ROADMAP.md` marks Phase 30 Complete (5/5, 2026-06-18) and PKG has no Phase 32 ledger row (research-package work predates the ledger). D-36-17 scoped reconciliation to "ledger-terminal values" and the SPEC R6 "current" text enumerated only LOOP-04/07/08 + VER as stale — it did not mention PKG. **Decision needed:** does Phase 36's reconciliation also flip PKG-05..08 → `Complete` (anchored on Phase 30 completion evidence, not the ledger), or are they intentionally left as-is / out of scope? Classification: process-artifact-schema. Confidence of impact: MEDIUM (affects whether the "no v1.6 status flag contradicts terminal state" acceptance criterion is read as violated). Do not invent the flip.

**F2 — The locked reconciliation rule "each flipped flag must match a terminal Phase 32 ledger row" is unsatisfiable for LOOP-07 and LOOP-08.** Both are provisional carry-forwards with **no dedicated ledger row** (`34-VERIFICATION.md` truths 6-7: "no dedicated ledger row (provisional carry-forward)"), yet both read `Pending` and are SATISFIED in `34-VERIFICATION.md`. The literal D-36-17 / SPEC constraint cannot be met for them. **Decision needed:** is flipping LOOP-07/08 → `Complete` justified by `34-VERIFICATION.md` (SATISFIED) as the terminal anchor in lieu of a ledger row, or do they stay `Pending`? Classification: process-artifact-schema. Confidence of impact: MEDIUM (R6 acceptance + idempotency edge). Do not invent.

**F3 — `SI-DQA-003` disposition is STOP-governed (D-36-18) and deferred to execution.** Characterized only (R4): non-binding lean preserve-with-reason (conservation/SCS-gate citation, locked post-v1.3, outside the curriculum/training-loop Issue-03 surface). The executing plan must make the call against sources and, if genuinely source-silent on Issue-03 relevance, surface a STOP gap. Additionally, `SI-PINN-002`'s preserve decision is analogous to the v1.5 Phase 29 `SI-PINN-002` case, which required a **D-08 human-approval STOP checkpoint** — the planner should consider whether a `checkpoint:human-verify` is warranted for the SI-PINN-002 / SI-DQA-003 preserve dispositions. Classification: semantic / process-artifact-schema. Confidence of impact: MEDIUM. Do not invent.

**F4 (LOW / mechanical) — precedent path drift in 36-CONTEXT.md.** `36-CONTEXT.md` canonical_refs (line 115) cites the Phase 29 dir as `29-acceptance-checks-reverification-handoff`, but the on-disk path is `29-acceptance-checks-re-verification-and-handoff`. The planner needs the correct path to read the v1.5 closure precedent. Also: the current dirty/untracked set is `AGENTS.md` (modified) **plus** an untracked `36-PATTERNS.md` in the Phase 36 dir — the SPEC/CONTEXT stated "only dirty file is AGENTS.md," so the dirty-file exclusion guard (D-36-15) must account for `36-PATTERNS.md` too. Confidence of impact: LOW (mechanical/path correctness).
