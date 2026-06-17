---
phase: 28
phase_name: "Validation Metrics Contracts"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 8
  lessons: 5
  patterns: 5
  surprises: 3
missing_artifacts: []
---

## Decisions

### GAP-28-01 RESOLVED-WITH-INSTRUCTION Option A — SASD canonical contract uses both-endpoint max
The SASD evidence packet surfaced a genuine fork between the DQA/issue-doc literal left-endpoint `t_i` and the resolution doc's candidate `max_{t in {t_i, t_{i+1}}}`. The user selected Option A after EDL empirical support showed both-endpoint evaluation adds zero extra flags vs left-endpoint across all four tiers (`cross-only-both = 0`, including the non-saturated hier_gold at 73%), confirming the "strictly dominates at no cost" rationale. Canonical SASD formula landed in `ctl_instruction.md` Step-1A `Data-side quality-metric contracts` as `dt_i * max_b max_{t in {t_i, t_{i+1}}} (||a_b|| / max(||v_b||, 1e-12))`, trajectory score `max_i SASD_i`, threshold 0.5 (provisional), flag-for-resampling (NOT auto-reject).

**Rationale:** Closed the final/right-endpoint blind spot at zero admitted-set cost; satisfies v1.5 governance that semantic spec forks require user sign-off, with EDL as support-only artifact.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-01 resolution note); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Resolution Addendum, P2-1)

---

### GAP-28-02 RESOLVED-WITH-INSTRUCTION Option A — IPR canonical contract pins raw G=1 units
The IPR evidence packet surfaced a raw-vs-scaled unit fork with ~464x gate impact (`D^2/T^4` under the locked `r = Dr', t = Tu` scale transform). The EDL gold-flag-rate calibration tripwire proved inconclusive (both raw-1e-3 and scaled-1e-3 flag ~100% of the clean admitted-set proxy because IPR is dominated by close-encounter under-resolution), so the units pin was decided on grounded convention-consistency: the data pipeline computes energy/conservation in raw `G = 1` units (`simulation_data/Scripts/metrics_calculation/`, a SCOPE-06/07 grounding source). Canonical data-side IPR is raw; landed in `ctl_instruction.md` Step-1A (Hermite/PCHIP-prohibited construction, `eps_inv = 1e-10`, stacked residual, dual-epsilon `IPR_train` separation) plus a `pinn_architecture.md` §3.4 visibility note.

**Rationale:** Convention-consistency with the pipeline's existing conservation-units choice, matching the resolution doc's primary raw argument without requiring the tripwire to discharge.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-02 resolution note); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md` (RESUMED banner, SUPERSEDED key-decision)

---

### GAP-28-03 user-DEFERRED Option D then later Option A — PSC composition: defer first, then adopt dedup-prefer-gold + equal-record weighting
The PSC evidence packet surfaced a population/weighting composition fork. Initial outcome was Option D (defer) because PSC's pooled population was entangled with unsettled gold-completeness work (184 base-only standard systems; pending missing-67 / OI-7b re-simulations). After gold completeness settled as final *in shape* (117 validatable + 67 permanent `gold_counterpart=absent`), the entanglement blocker discharged because the composition rule is promotion-invariant ("prefer gold when present" reads identically before and after the 117 promote). User ratified Option A: dedup-prefer-gold (one record per `physical_key`) + equal-record `1/N_t` weighting, on coverage-diagnostic + MNAR-censoring grounds — the `1/N_t` weighting holds the 67 low-snapshot chaotic-tail base trajectories at full per-trajectory weight rather than suppressing them ~16x.

**Rationale:** Two-stage resolution preserves STOP-protocol integrity at first park and then ratifies a consolidator-original synthesis only after the upstream entanglement resolves. PSC remains report-only (no reject authority).

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-03 resolution note, two-stage history); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md` (CLOSED banner)

---

### VAL-01 transcribed as locked-verdict (not re-adjudicated)
The SCS canonical contract was treated as transcription of the locked accept-resolution verdict (D-03), not re-adjudication. The Step-1A conservation gate was reconciled into the canonical form `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, REJECT if `SCS > -5`, with band table, tie rule, near-zero `|H(0)|` quarantine + Plummer `eps = 1e-10`, and per-trajectory storage rules preserved. Issue-doc ratio thresholds `1e-6`/`1e-8` were rejected by name (not canonical), with explicit cite of `scs-thresholds.md` and dual-`eps_H` symbol hygiene against `pinn_architecture.md` training `eps_H = 1e-4*S_H`.

**Rationale:** Avoids re-opening a resolved Q-C1 fork; keeps the substantive commit within the four 28-01 owned paths (ctl_instruction.md, 24-ISSUE-LEDGER.md, scs-thresholds.md, 28-01-SUMMARY.md).

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md` (Decisions Made, AC-VAL-01, key-decisions)

---

### AC-VAL-01 recorded inline rather than as a new committed script
The pre/post-edit discriminating AC-VAL-01 check (formula, band_table_and_tie, quarantine_and_plummer, ratio_thresholds_rejected, scs_packet_citation, invariance_and_symbol_hygiene) is captured inline in the 28-01 SUMMARY, with the rerunnable Python heredoc preserved in the artifact. Pre-edit RESULT: FAIL (ratio_thresholds_rejected, scs_packet_citation, invariance_and_symbol_hygiene); post-edit RESULT: PASS.

**Rationale:** Avoids adding a fifth owned file beyond the plan's same-commit scope; preserves re-derivability in the SUMMARY itself.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md` (AC-VAL-01 section)

---

### PIPE-09 `compute_globals` region byte-stable after SCS edit (no regression)
Extraction via `awk '/Normative compute_globals contract/{f=1} /^### 2.6/{f=0} f'` returned identical SHA-256 `816589102aea99f2878991bda9cee351db08e8d2cd5c64fbe725c551a825b986` at HEAD baseline and after the SCS edit. The `D=6.694` ledger row remains VERIFIED.

**Rationale:** Phase 27 PIPE-09 raw-mass D convention feeds the SCS definition directly; byte-for-byte regression check is the cheapest available proof that the SCS reconciliation did not perturb the upstream invariant.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md` (PIPE-09 Regression Re-Check); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Test 2)

---

### Phase 28 closes at 3/4 with VAL-04 (PSC) explicitly user-DEFERRED
Phase 28 closes with three of four canonical data-side contracts landed and structurally correct (SCS/SASD/IPR; 26/26 re-check assertions), and VAL-04 (PSC) explicitly user-DEFERRED with a recorded forward-dependency on the post-promotion first-run PSC/SCR sanity check at the FUT-01 dataset-finalization gate. The `0.5` SASD flag and `1e-3` IPR flag are landed as provisional; recalibration is a hard dependency for doc-03/FUT-01.

**Rationale:** Distinguishes "deferred by user choice with documented forward trigger" (valid terminal state) from "open gap blocking phase closure"; PSC is report-only and design-open, so the deferred state is appropriate rather than blocking.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Verdict, Pass 2); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md` (CLOSED banner)

---

### EDL empirical study used as support-only artifact (not grounding) for all three STOP forks
The EDL empirical decision-support brief at `.planning/research/edl/phase28-validation-metrics/FINDINGS.md` informed the user's choices on GAP-28-01/02/03 but never substituted for user sign-off. Per v1.5 governance (CLAUDE.md "Empirical Decision Loop support"), EDL briefs are support artifacts, not grounding sources — they do not authorize a probe, a numeric default, or a framework-spec edit without user instruction. This boundary held: the SASD 0.5 / IPR 1e-3 thresholds land as provisional with admitted-set recalibration deferred to doc-03/FUT-01, not as authoritative numbers.

**Rationale:** Prevents EDL from silently becoming a back-door authority for spec-engineering or physics-adjudication calls; the user attested in session they personally chose both-endpoint SASD, raw-units IPR, and Option-D PSC defer.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Resolution Addendum, P2-6); `<home>/Desktop/3_body_problem/CLAUDE.md` (Empirical Decision Loop support section)

---

## Lessons

### STOP-protocol integrity held: zero framework-spec files touched in the three park commits
The strongest available evidence the STOP protocol worked in Phase 28 is negative: park commits `2f7681d3` (SASD), `aea67477` (IPR), `f7c68e65` (PSC) each touch ZERO framework-spec files. The `### ... Data-side quality-metric contracts` heading was absent from `ctl_instruction.md` (only a prose forward-pointer naming the future subsection existed, added by SCS) until the user-instructed resume landed the SASD/IPR/PSC clauses. This is what "do not invent content where sources are silent" looks like in commit-history terms.

**Context:** When a metric forks on a semantic axis (endpoint convention, unit pin, population composition), the agent must produce the evidence packet, raise the gap, and stop — not silently choose one side and transcribe it as if the source had settled it.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Test 3: STOP-protocol integrity); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (each GAP's "Where in artifact" + "Task context")

---

### Dimensionful metrics must bind threshold values to explicit units before spec transcription
The IPR raw-vs-scaled fork surfaced because `IPR > 1e-3` looks unitless but the same number means different things in raw `G=1` arrays vs scaled normalized coordinates — a ~464x difference under the locked scale transform. The DQA's "Load and Normalize" wording left the placement ambiguous, and the resolution doc itself preserved scaled-units dissent. A dimension check (`acceleration-squared residual`) is necessary but not sufficient: it proves the unit pin is *consequential*, not that the source picked one side.

**Context:** Any validation metric whose threshold is a bare number, where the source does not pin units, is a STOP-candidate. The agent must surface, not infer — even when the dimension analysis is clear.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-02 Source silence, Mathematical/engineering grounding); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md` (key-decisions)

---

### Both-endpoint max is monotone ≥ left-only; monotone doesn't mean zero-cost in general
The both-endpoint SASD evaluation is mathematically monotone relative to left-only (`max(left,right) >= left`), so it cannot un-flag a trajectory already flagged by the DQA-literal form. On the empirical admitted set, it adds zero extra flags across all four tiers (`cross-only-both = 0`, including non-saturated hier_gold at 73%). But that is a dataset-specific result — the monotonicity guarantees strict conservative expansion, not zero-cost. Future datasets with different snapshot distributions could see flag growth that the EDL study did not observe.

**Context:** Monotone-extension arguments justify the conservative choice when the empirical cost is zero on the current data, but the justification must rest on the empirical finding, not the monotonicity alone.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-01 Mathematical/engineering grounding, resolution note); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (P2-2)

---

### Two-stage gap resolution is valid: park now, ratify later when upstream settles
GAP-28-03 (PSC composition) was initially resolved as Option D (defer) because PSC's pooled population was entangled with unsettled gold-completeness work. After the 117 promote + 67 permanent `gold_counterpart=absent` partition settled as final in shape, the user reopened and ratified Option A (adopt the composed convention) — the blocker discharged because the composition rule is promotion-invariant. This is a different pattern from "I changed my mind": the upstream state changed, the policy that was blocked by that state became ratifiable, and the gap register's resolution note records both stages.

**Context:** Defer (Option D) is not a permanent state. When a gap is parked behind upstream work and that work resolves, re-open the gap with a fresh resolution note that names the new basis. The fact that the composition is promotion-invariant is the technical reason a re-open is valid, not just an editorial cleanup.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-03 resolution note, two-stage history); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md` (CLOSED banner)

---

### Documentation-integrity follow-up: parked-state bodies contradicted their own resolution banners
The Pass-1 parked-state bodies in `28-UAT.md` and `28-02/03/04-SUMMARY.md` carried phrases like "GAP-28-01 is OPEN", "Phase 28 cannot close", "DEFERRED / No spec edit landed", and stale counters 9/3/6/0 — which directly contradicted the resolution banners above them ("RESUMED 2026-06-16 — GAP-28-01 RESOLVED-WITH-INSTRUCTION", "CLOSED 2026-06-16 — GAP-28-03 user-DEFERRED"). The Pass-2 reconciliation added SUPERSEDED markers + explicit "parked narrative retained below" framing to make the historical record non-misleading while preserving it as the STOP record.

**Context:** When a SUMMARY's lead banner says RESOLVED but its body says OPEN, the body becomes a misreading hazard. Resolved-with-instruction phases need both the resolution banner AND a clear "this body section is the historical first-park STOP record, NOT current state" marker.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Findings F1 doc-integrity MAJOR); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-02-SUMMARY.md`, `28-03-SUMMARY.md`, `28-04-SUMMARY.md` (SUPERSEDED key-decisions)

---

## Patterns

### Packet-before-edit enforcement for validation metric forks
Every Phase 28 plan (28-02 SASD, 28-03 IPR, 28-04 PSC) followed the same flow: author the EVID-06 packet from the Phase 25 schema → register the ID-to-filename map row in `evidence/README.md` → record the verdict (`defer-with-blocker` because the fork is unsettled) → park the spec edit → raise the STOP gap → block the phase-closure. The packet lives under `25-.../evidence/` and is the durable record; the gap is the live blocker; the SUMMARY is the plan outcome. This packet-before-edit pattern makes it cheap to resume work after user instruction, because the spec text is pre-shaped in the packet's before/after note and the AC-VAL-N check is pre-defined in 28-SPEC.md.

**When to use:** When a phase owns multiple metric/contract forks and the v1.5 governance requires user sign-off on each. Authoring the packet is fast (~4-5 min per metric), and it gives the user a concrete artifact to ratify.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-02-SUMMARY.md`, `28-03-SUMMARY.md`, `28-04-SUMMARY.md` (each: key-files created = `evidence/<metric>.md`, key-files modified = `evidence/README.md` + `24-ISSUE-LEDGER.md` + `28-GAPS.md` + `v1.5-GAPS.md`)

---

### Defer-with-blocker ledger status blocks phase closure while the corresponding STOP gap is OPEN
For Phase 28 validation metric forks, DEFERRED ledger status does not close the phase while the corresponding STOP gap remains OPEN. The transition log records `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` for resolved rows, and `PENDING -> IN_PROGRESS -> DEFERRED` for parked rows. The DEFERRED row carries the packet link, the owning GAP-NN-XX, and the `defer-with-blocker` verdict, so the ledger is self-describing for downstream phases (Phase 29 acceptance, FUT-01 build) that need to know which contracts are canonical.

**When to use:** Whenever a phase owns a metric/contract ledger and a parallel gap register. Bind the two: every DEFERRED row must cite its owning gap ID, and the gap resolution note must reference the row's terminal state.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-02-SUMMARY.md` (key-decision, Decisions Made); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (Test 7: Issue-ledger VAL rows at terminal lifecycle states)

---

### Inline structural acceptance checks recorded in SUMMARY (not new files)
The Phase 28 pattern is: an AC-VAL-N check is a pre-defined assertion set in `28-SPEC.md` (per D-07 reservation, satisfying the process-artifact-schema rule), the result is captured inline in the plan SUMMARY (pre-edit FAIL → post-edit PASS with concrete output), and the rerunnable command is preserved as a heredoc in the artifact. No new committed script is created; the check is re-derivable by anyone reading the SUMMARY.

**When to use:** When a plan owns a small set of structural assertions (6-10 checks) and committing a separate validator script would be scope creep. The SUMMARY's inline check is enough as long as it carries a concrete before/after and a copy-pasteable command.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md` (AC-VAL-01, Decisions Made); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (P2-1 "26/26 re-check assertions")

---

### Two-phase pending-SHA backfill for ledger provenance
Each Phase 28 plan landed the substantive content in one commit (`bd31dcd8` SCS, `2f7681d3` SASD, `aea67477` IPR, `f7c68e65` PSC) with a pending-SHA transition log entry, then a follow-up `verify(28-0N): backfill commit sha` commit backfills the real SHA into the evidence packet's status log and the SUMMARY. This pattern works because the substantive work and the provenance-record update are not the same change — folding them into one commit means the agent must know its own SHA before writing the artifact, which is impossible at edit time.

**When to use:** When a SUMMARY, evidence packet, or ledger row must cite its own commit SHA but the SHA is only known after `git commit` runs. Author the artifact with a `[pending — will be backfilled in verify(<scope>)]` placeholder, commit, capture the SHA, commit the backfill separately.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-01-SUMMARY.md`, `28-02-SUMMARY.md`, `28-03-SUMMARY.md`, `28-04-SUMMARY.md` (each: "Provenance backfill: expected follow-up commit verify(28-0N): backfill commit sha")

---

### Dual-epsilon visibility note for spec/architecture separation
When a validation metric has a training-side analogue (e.g., IPR train `eps_train = 1e-5` vs data-side `eps_inv = 1e-10`), the spec lands the metric in `ctl_instruction.md` with a `IPR_train` separation clause, and `pinn_architecture.md` §3.4 carries a visibility note (`ε_train=1e-5` vs `ε_inv=1e-10`, "must not be conflated", "does not alter" the locked PHYS-04/HC-4 invariants). This makes the dual-epsilon distinction discoverable from both the spec and the architecture doc, without introducing a new spec file or a cross-cutting doc.

**When to use:** When a data-side validation metric has a training-side analogue whose threshold differs by orders of magnitude. The spec owns the canonical threshold; the architecture doc owns the "you may see this number in the model, here's what it means" note.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md` (key-decisions, RESUMED banner: "pinn_architecture.md §3.4 dual-epsilon note"); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (P2-1)

---

## Surprises

### IPR gold-flag-rate tripwire proved inconclusive because IPR is dominated by close-encounter under-resolution
The EDL study intended to use the gold-flag-rate calibration tripwire (the clean admitted-set proxy) to disambiguate raw vs scaled IPR units. Both `raw-1e-3` and `scaled-1e-3` flag ~100% of the admitted set because IPR — an acceleration-squared residual — is dominated by close-encounter under-resolution regardless of unit convention. The tripwire that should have settled the units fork empirically was instead saturated by the underlying physics. The user fell back to convention-consistency (the pipeline computes energy in raw `G=1` units) as the secondary argument.

**Impact:** A well-designed empirical disambiguator can saturate on the very phenomenon the metric is designed to measure. When that happens, the unit pin has to be argued from convention-consistency, not from empirical calibration. This is a structural risk for any dimensionful validation metric calibrated against a saturated proxy.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-02 resolution note); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md` (RESUMED banner: "the EDL gold-flag-rate tripwire was inconclusive")

---

### Both-endpoint SASD adds zero extra flags across all four tiers on the current admitted set
The empirical cost of the conservative (both-endpoint) SASD evaluation was zero on the current admitted set: `cross-only-both = 0` for all four tiers, including the non-saturated hier_gold at 73%. This was not a designed property of the algorithm — it was an empirical finding that the admitted set's snapshot distribution does not exhibit final-endpoint spikes that left-only evaluation would miss. The monotonicity of `max(left, right) >= left` guarantees the conservative form is a superset, not a subset; the empirical finding is the *size* of the superset is zero on the current data.

**Impact:** Conservative extensions that are monotone do not always pay their conservatism in flag growth. The empirical cost can be zero on the current data and non-zero on a future dataset with different snapshot distribution. Future datasets with more close-encounter tails or more variable-cadence simulations could see the flag set grow non-trivially.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-01 resolution note); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-UAT.md` (P2-2)

---

### PSC's 1/N_t weighting is the opposite of hiding the censored region
The PSC composition decision landed at equal-record `1/N_t` weighting on coverage-diagnostic + MNAR-censoring grounds: the `1/N_t` weighting holds the 67 low-snapshot chaotic-tail base trajectories at full per-trajectory weight rather than suppressing them ~16x under naive all-snapshot pooling. This is a counterintuitive choice — equal-record weighting in a snapshot-resolution-imbalanced dataset usually *under-weights* the high-resolution gold-backed ICs, which looks like a bias introduction. The reason it is correct here is that the 67 low-snapshot trajectories are the MNAR-censored region (chaotic tail), and suppressing them would hide the very diagnostic signal PSC is supposed to surface.

**Impact:** Equal-record weighting is not a universal "fairness" axiom; it is the right choice when the under-weighted group is the diagnostically interesting one. The agent was tempted to weight by snapshot count to avoid the apparent bias, but the resolution doc's coverage-diagnostic argument is that the bias is the feature, not a bug. The 67 vs 117 partition and the `gold_counterpart=absent` marker are the load-bearing facts.

**Source:** `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-GAPS.md` (GAP-28-03 resolution note, "MNAR-censoring grounds"); `<home>/Desktop/3_body_problem/.planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md` (CLOSED banner: "post-promotion pool at the FUT-01 dataset-finalization gate")

---
