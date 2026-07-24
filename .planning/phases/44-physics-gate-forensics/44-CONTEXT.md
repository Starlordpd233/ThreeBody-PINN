# Phase 44: Physics-Gate Forensics - Context

**Gathered:** 2026-07-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 44 delivers a **read-only, re-derivable forensic characterization** of how the Stage-0 CTL-PINN
model fails the physics-conservation gate, using **only artifacts v2.0 already produced**. It ends in
`44-DIAGNOSIS.md`: a hypothesis-ranked, evidence-cited diagnosis that **explicitly abstains from
selecting a remedy**.

Three quantifications plus a report:

1. **DIAG-01** — per-trajectory ε_H distribution over all 1,500 held-out trajectories, from the
   preserved `metrics.json` (the evaluator is **not** invoked).
2. **DIAG-02** — five-term loss decomposition per step across `stage0-smoke` and pilot seeds 41/42/43,
   including warmup-spike attribution and PHYS-05 scheduled-weight interaction.
3. **DIAG-03** — three-seed band characterization separating budget-limited descent from recipe
   instability, with the Phase 38 overfit rung as machinery-integrity control.
4. **DIAG-04** — the ranked diagnosis report itself.

**This phase does not fix anything.** Hard boundaries (SCOPE-22..26, owner-signed): no held-out
evaluation, no new training runs, no framework-spec edits, no PLAT-01..07/Stage-1 work, no remedy
selection. A diagnosis implicating a spec parameter becomes an ERW question for Phase 45 — never an edit.

</domain>

<decisions>
## Implementation Decisions

Discussion ran `--all --auto`: all gray areas auto-selected, recommended option taken for each and
logged. See `44-DISCUSSION-LOG.md` for alternatives considered.

### Evidence layout and re-derivability

- **D-01:** Analysis scripts, their outputs, and an input-pinning manifest live in
  `.planning/phases/44-physics-gate-forensics/evidence/`. Nothing is written under `pinn/` — the
  shipped code is read as the *factual record of what executed* and is not modified (SCOPE-24 spirit).
- **D-02:** Every number quoted in `44-DIAGNOSIS.md` must be regenerable by running a retained script
  against pinned inputs. Pin inputs by **SHA-256 of each artifact file plus the repo commit hash**;
  record them in the evidence manifest. This satisfies Phase 44 success criterion 5 and mirrors the
  v1.5 "re-derivable, recorded in committed state — not `/tmp`" rule.
- **D-03:** Scripts are plain Python 3 run against the repo as-is, no new dependencies. Determinism
  over cleverness: sorted inputs, explicit seeds where any sampling occurs (none expected).

### ε_H distribution analysis (DIAG-01)

- **D-04:** Report the **full distribution**, not just the headline number: min / percentiles
  (p25, p50, p75, p90, p99) / max, mean, and the fraction exceeding the `1e-5` reject threshold.
- **D-05:** **Pre-register the uniform-vs-tail criterion before computing it**, so the verdict is not
  post-hoc: failure is **uniform** when the *minimum* per-trajectory ε_H already exceeds the reject
  threshold (i.e. 100% of trajectories fail); tail structure is then reported separately as a
  magnitude-spread statement (max/median ratio, p99/median). Scouting indicates this criterion will
  resolve to "uniform failure carrying a heavy right tail" — see `<code_context>` — but the phase must
  derive it, not inherit it from this file.
- **D-06:** Break the distribution down by the **two trajectory attributes actually present** in the
  artifact — `variant` (hierarchical / standard) and `fidelity` (base / gold) — and report whether
  either separates the population. These are the only recorded attributes available; do not
  manufacture others.
- **D-07 (MUST SURFACE, do not decide):** Scouting established that the reported gate value
  `eps_h = 237.2086056078468` is **exactly the maximum** per-trajectory ε_H, not the mean
  (mean = 5.6222). Whether a worst-case max is the **spec-intended** gate statistic is a
  semantics question about the gate definition. Phase 44 **checks this against the locked spec and the
  Phase 43 evaluator record, and if the sources are silent or ambiguous, records a STOP-protocol gap**
  in `.planning/milestones/v2.1-GAPS.md` — it does **not** decide the intended statistic, and does not
  quietly re-report the mean as "the" gate number.

### Loss decomposition (DIAG-02)

- **D-08:** Report **both** raw per-term loss values **and** λ-weighted contributions for every step
  range. The PHYS-05 scheduled weights change during training, so term *dominance* can differ between
  the raw and weighted views — DIAG-02 explicitly requires the interaction with those scheduled
  weights, which needs both series.
- **D-09:** Attribute the warmup spike (~3.7e9) to specific term(s) by locating the spike step window
  in the JSONL and reporting which `loss_*` key carries the magnitude, alongside `grad_norm`, `lr`,
  and the `finite` / `nonfinite_keys` flags at those steps.
- **D-10:** `runs/stage0-smoke` is analysed as a fourth trace alongside the three pilot seeds, not
  folded into them — it is a different run configuration and is cited as such.

### Seed-band characterization (DIAG-03)

- **D-11:** Characterize all three pilot seeds (41/42/43) on per-seed validation-trend direction,
  final-loss and validation spreads, and step-window trend analysis. Anchor the trend claims to the
  numbers already recorded in `43-CALIBRATION.md` (2/3 seeds worsened) and state agreement or
  disagreement with them explicitly.
- **D-12:** Cite the Phase 38 single-trajectory overfit rung **from its existing verification record**
  as the machinery-integrity control — evidence that the network *can* fit one trajectory, so failure
  emerges at population scale/budget. It is **cited, never re-run** (SCOPE-23).

### Diagnosis report (DIAG-04)

- **D-13:** Rank **at least four** candidate causes on a fixed rubric, each carrying (a) supporting
  evidence citations, (b) **contradicting** evidence citations, and (c) the *discriminating test that
  would settle it*. Baseline candidates from REQUIREMENTS: insufficient training budget, loss-term
  imbalance, optimization/warmup pathology, normalization-or-data-scale issue — plus any the evidence
  surfaces.
- **D-14:** Discriminating tests are recorded as **proposals only**. Under SCOPE-23 a decisive
  diagnostic run may be *proposed for owner authorization* and must never be executed in this phase.
- **D-15:** The report states remedy-abstinence explicitly and in its own words — ranking hypotheses is
  in scope, choosing among them is not (SCOPE-26). Any source-silent physics-adjudication call goes to
  the gap register, not into the report as a decision.

### Governance

- **D-16:** `.planning/milestones/v2.1-GAPS.md` does not exist yet; it is created on the **first** gap
  under the standing trigger, and the phase-local register is
  `.planning/phases/44-physics-gate-forensics/44-GAPS.md`. D-07 is the most likely first entry.
- **D-17:** Commits go through `scripts/agent-commit` with `GIT_AGENT_ID` and
  `GIT_AGENT_OWNED_PATHS` set; explicit paths only, never blanket staging.

### Claude's Discretion

`--auto` mode selected the recommended option for every area without user prompting, so all decisions
above are Claude-selected defaults. They are **implementation-mechanics** choices (where scripts live,
how to pin inputs, which statistics to report, how to structure the ranking) and are safe for the
planner to adjust on evidence.

**One exception, which is not discretionary:** D-07 is a governance obligation, not a preference. The
max-vs-mean gate-statistic question must be surfaced, not resolved by any agent.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and hard boundaries
- `.planning/REQUIREMENTS.md` — DIAG-01..04 verbatim, plus **SCOPE-22..26** (the owner-signed hard
  constraints). Read SCOPE-22..26 before proposing any task.
- `.planning/ROADMAP.md` §"Phase 44: Physics-Gate Forensics" (goal, 5 success criteria) and
  §"Investigation discipline (applies to both phases)".
- `CLAUDE.md` — STOP protocol: classification of gaps and the "never invent where sources are silent"
  rule. Applies to this milestone per the ROADMAP's "STOP-protocol spirit" clause.

### The failure being diagnosed
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md` — the
  owner-signed `adjust` verdict that routed this investigation; also the audited record of the
  exhausted evaluator budget.
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CALIBRATION.md` —
  per-seed calibration, the "2/3 seeds worsened" claim, spreads. Primary DIAG-03 anchor.
- `.planning/milestones/v2.0-MILESTONE-AUDIT.md` — `tech_debt` status, warnings W-1..W-3
  (W-1 concerns missing `evaluation-attempt.json` provenance for seed-42; relevant to DIAG-01 framing).
- `pinn/STATUS.md` — forward handoff from v2.0; factual record of what shipped.

### Machinery-integrity control
- `.planning/milestones/v2.0-phases/38-pinn-model-rebuild-from-specs-fut-01/38-VERIFICATION.md` —
  the single-trajectory overfit rung (DIAG-03 control; cite only, never re-run).

### Retained evidence artifacts (read-only inputs)
- `runs/stage0-pilot-seed42/evaluation/metrics.json` — **sole gate rendering**; schema
  `phase43-evaluate-metrics/v1`; contains the 1,500-entry `per_trajectory` array. DIAG-01's only input.
- `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` — receipt/provenance for that rendering.
- `runs/stage0-pilot-seed42/evaluation/metrics.md` — human-readable summary of the same rendering.
- `runs/stage0-smoke/logs/train.log.jsonl`, `runs/stage0-pilot-seed{41,42,43}/logs/train.log.jsonl` —
  per-step training records (300 lines each). DIAG-02/03 primary input.
- `runs/stage0-smoke/tb/`, `runs/stage0-pilot-seed{41,42,43}/tb/` — TensorBoard event files.
- `runs/stage0-{smoke,pilot-seed41,pilot-seed42,pilot-seed43}/status.json` — run status records.

### Locked specs (read-only — SCOPE-24 forbids editing)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Stage-0 recipe,
  curriculum staging, loss catalog. Consult for the gate definition behind D-07.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — architecture, AD
  contract, output head.

### Downstream (Phase 45 — context only, not this phase's work)
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — canonical ERW runbook;
  `44-DIAGNOSIS.md` becomes the centerpiece of the trainex-r2 package.

### To be created
- `.planning/milestones/v2.1-GAPS.md` — milestone gap index; **does not exist yet**, created on first
  gap under the standing trigger.

</canonical_refs>

<code_context>
## Existing Code Insights

Findings below are from **scouting during discussion** — a shape check to confirm the requirements are
feasible against real artifacts. They are **not** the DIAG-01..03 analyses, and Phase 44 must derive
its own numbers through retained, re-derivable scripts (D-02) rather than citing this file.

### Reusable Assets

- **`metrics.json` carries full per-trajectory data.** Confirmed: `per_trajectory` is a 1,500-element
  array; each entry has `eps_h`, `id`, `variant`, `fidelity`. Top-level keys: `checkpoint`, `eps_h`,
  `eps_h_reject_threshold` (`1e-05`), `n_test_trajectories` (1500), `scs` (2.3751304405952904),
  `scs_reject_threshold` (`-5.0`), `run_dir`, `schema_version`, `timestamp`, `verdict` (`FAIL`).
  **DIAG-01 is fully feasible without re-running the evaluator** — this was the phase's main
  feasibility risk and it is cleared.
- **Training logs carry all five loss terms *and* their scheduled weights.** Each `event: "step"`
  record in `train.log.jsonl` has `loss_data`, `loss_ic`, `loss_phys`, `loss_energy`, `loss_angmom`
  (the five terms) plus `lambda_data`, `lambda_ic`, `lambda_phys`, `lambda_e`, `lambda_l` (PHYS-05
  scheduled weights), alongside `step`, `epoch`, `stage`, `phase`, `front_idx`, `lr`, `grad_norm`,
  `total`, `finite`, `nonfinite_keys`, `w_min`/`w_mean`/`w_max`, `s_per_step`, `eta_seconds`,
  `step_completed`. **DIAG-02 is fully feasible read-only**, including the raw-vs-weighted split (D-08).
- **All four required runs have complete artifact sets** — `stage0-smoke` and
  `stage0-pilot-seed{41,42,43}` each have `logs/train.log.jsonl` (300 lines), `tb/`, and `status.json`.

### Established Patterns

- **Phase 43 evidence convention:** the phase used numbered `43-NN-PLAN.md` / `43-NN-SUMMARY.md` pairs
  (10 plans). Plan files must follow `{padded_phase}-{NN}-PLAN.md` exactly — `44-01-PLAN.md`, etc.
- **Two extra run directories exist that the requirements do not name:** `runs/probe-run/` and
  `runs/stage0-smoke-diag/`. They are **not** in DIAG-02/03 scope as written. If the planner wants them
  used, that is a scope question for the owner, not a silent inclusion.

### Integration Points

- Phase 44 writes **only** under `.planning/phases/44-physics-gate-forensics/`. It reads `runs/`,
  `.planning/milestones/v2.0-*`, `pinn/`, and the framework specs. It writes to none of them.
- `44-DIAGNOSIS.md` is Phase 45's centerpiece input — its structure should survive being snapshotted
  and commit-pinned into the trainex-r2 package (PKG-09).

### Scouting observations the phase must independently re-derive

Recorded here so the planner can size the work honestly — **not** as established findings:

- `eps_h` (237.2086056078468) is **exactly equal to `max(per_trajectory.eps_h)`**; the mean is 5.6222
  and the median 2.234. The headline gate number is therefore a worst-case statistic. → D-07.
- Distribution shape observed: min 0.9741, p25 1.216, p50 2.234, p75 5.225, p90 11.22, p99 56.13,
  max 237.21.
- **1500/1500 trajectories exceed the `1e-5` reject threshold** — the *best* trajectory misses by
  roughly five orders of magnitude. This points to uniform, population-wide failure carrying a heavy
  right tail, rather than a tail-driven failure that a few bad trajectories dominate. It materially
  affects which hypotheses in DIAG-04 stay plausible, so DIAG-01 should be sequenced early.
- Attribute split available: `variant` = hierarchical 970 / standard 530; `fidelity` = base 759 /
  gold 741. Worst trajectory: `id 1414`, `variant standard`, `fidelity base`.

</code_context>

<specifics>
## Specific Ideas

- The diagnosis is written for **two audiences at once**: the owner (adjudicating the remedy) and the
  external trainex-r2 researchers (who will not have this repo's context). Every claim needs a citation
  a stranger can follow.
- Follow the v1.4/v1.5/v1.6 house style of separating **verified fact** from **agent hypothesis**
  inline — Phase 45's claims register (PKG-11) is built directly from that separation, so making it
  explicit in `44-DIAGNOSIS.md` saves rework.
- The gate is two-sided: `ε_H > 1e-5` **and** `SCS > -5`. Observed `SCS = 2.3751304405952904` against a
  `-5.0` reject threshold. The diagnosis should address both criteria, not ε_H alone.

</specifics>

<deferred>
## Deferred Ideas

- **Remedy design of any kind** (budget increases, loss re-weighting, warmup/LR schedule changes,
  curriculum re-pacing) — SCOPE-26, owner-routed via the trainex-r2 resolution doc in a later milestone.
- **Any decisive diagnostic training run** — SCOPE-23. May be *proposed* in `44-DIAGNOSIS.md` with a
  concrete design for owner authorization; never executed here.
- **A new held-out evaluation** — SCOPE-22, requires a new explicit owner policy. Phase 45 poses the
  evaluation-policy question (PKG-10); Phase 44 does not.
- **Spec edits implied by the diagnosis** — SCOPE-24. These become ERW research questions.
- **`runs/probe-run/` and `runs/stage0-smoke-diag/` analysis** — outside the named DIAG-02/03 artifact
  set; raise with the owner if the planner believes they are needed.

### Reviewed Todos (not folded)

Both pending todos matched Phase 44 at relevance 0.6, which under `--auto` would normally be
auto-folded (threshold 0.4). **Both were deliberately NOT folded** — ROADMAP.md and REQUIREMENTS.md
explicitly assign both to Phase 45, and an auto-fold would have contradicted a locked decision:

- **`trainex-r1-research-handoff`** — "Review and hand off the trainex-r1 research sub-packages
  (r1a + r1b)". Deferred to **Phase 45**: REQUIREMENTS.md Future Requirements and Phase 45 success
  criterion 4 make the r1b ↔ trainex-r2 relationship an **owner** decision at package assembly.
- **`d-06-static-epsilon-sensitivity-check`** — "D-06 static-epsilon sensitivity check (confirm
  dual-context is safe on the admitted set)". Deferred to **Phase 45**: it is a spec-side question and
  a candidate ERW question, with owner confirmation of inclusion due at assembly.

</deferred>

---

*Phase: 44-physics-gate-forensics*
*Context gathered: 2026-07-23*
