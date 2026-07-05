# Trainex R1a — Decision-Adjudication Resolution (STORM round)

**Date:** 2026-07-04 · **Channel:** build-design (recommendation only; the project owner ratifies)
**Sources:** the eight original documents, delivered inside four consolidated bundles (`r1a-decision-materials.md`, `framework-specs.md`, `context-baseline-strategy.md`, `r1b-findings.md`). Citations below use the **original filenames** per the source-discipline contract.
**Method:** four-phase STORM (multi-perspective scan → contradiction map → synthesis → peer review), executed with every claim grounded in the attached files only. The Phase 1–2 working record and the Phase 4 self-critique are appended (Appendices A–C); the report below is the deliverable.

---

## 0. How to read this resolution

Each in-scope decision gets one block: **Recommendation · Endorse/Override · Confidence (+ biggest uncertainty) · Consistency · Timing · Nature.** "Endorse/Override" is judged against the *suggested default in `trainex-r1a-options-and-decisions.md`* (the operative decision sheet); where the deeper `chatgpt-pro-resolution.md` disagreed with its own distilled sheet, that intra-prior-round tension is adjudicated explicitly. Per the mandate: **D1-p (precision) is not decided here** — every recommendation is stated to hold under both branches — and **B-8 (ε_H gate direction) is treated as spec-settled** (`ctl_instruction.md` conservation gate: REJECT if `eps_H > 1e-5`; smaller passes; `eps_H = 0 → Excellent`).

**Three findings shape the whole resolution** (details in the per-decision blocks and Appendix B):

1. **The specs have moved since the decision sheet was written (2026-06-12).** The attached `ctl_instruction.md` (v1.6 baseline) now contains Phase 33–35 contracts the sheet never saw: the **ADVANCE / RECOVER / HALT-REVIEW stage-transition state machine** (CURR-03), the **canonical replay/lookahead batch contract with resolved edge cases** (LOOP-01, closing SI-PINN-003), verified **snapshot-count medians** (61 / 127 / 1003), and loader-metadata requirements (LOOP-06). These close two of the sheet's register items (U-3, U-14), partially close a third (U-1), and force one substantive amendment (D4-c).
2. **The sheet's one under-argued row is checkpoint cadence.** Its own companion evidence (`trainex-r1b-findings.md` §1.8, `trainex-r1b-findings-2.md` DRO-6) argues for a wall-clock-bounded cadence; the sheet "kept" the step-1000 baseline without engaging that evidence. Overridden (D4-a).
3. **Everything else composes.** The endorsed set is coherent: PyTorch's closure-shaped two-phase loop (D5-a) is the single structural seam that D4's guards, D7's idempotent promotion, the spec's RECOVER path, and the full-batch-L-BFGS memory answer all hang off. The JSONL-canonical rule (D2) is what makes the tracker a two-way door. The 5-minute smoke test (r1b rung 6) is what makes durations, cadence values, and the seed band measurable instead of guessed.

**⚖ thresholds are left as placeholders** per the round contract (Stage-2 fills them); the claims register (§5) records exactly which ⚖ values the r1b files do and do not supply numbers for.

---

## 1. Resolution summary

| # | Decision | Recommendation | Verdict vs sheet default | Conf. | Timing |
|---|---|---|---|---|---|
| D1 | ML framework | **PyTorch 2.12 + MPS** (fp64 branch: same code, `device="cpu"`) | **Endorse** | High | Needed now (one-way) |
| D1-p | Precision branch | *Not decided (owner-carved).* All picks hold under both branches | n/a | n/a | — |
| D2 | Tracker / monitor | **TensorBoard as view; JSONL log canonical; one plot script** | **Endorse** | High | Needed now (JSONL+TB); plot script deferrable |
| D3 | Data residency | **Auto-selector defaulting to in-memory fp32; `num_workers=0`; watermark 0.7 (knob)** — adapter also exposes `n_snapshots`/`dt_out` metadata (spec drift) | **Endorse (amended)** | High (structure) / Medium (auto lands in-RAM) | Adapter interface needed now; policy two-way |
| D4-a | Cadence & retention | **Rolling-3 + best + anchors + latest-copy; dual trigger: every 1000 steps *or* wall-clock ceiling, whichever first** | **Override (amend cadence)** | High (structure); ceiling value open | Needed now |
| D4-b | Corruption safety | **Atomic tmp+fsync+rename; `weights_only`-clean contents** | **Endorse** | High | Needed now |
| D4-c | Auto-guard tier | **Tier 1+2 on; three loop seams built now; ADD spec-mandated RECOVER seam (retry budget default 0) and HALT/REVIEW guard (provisional thresholds)** | **Endorse (spec-drift amendment)** | Medium | Seams needed now; toggles two-way |
| D4-d | Diagnostic bundle | **Always on** (+ one-line README: "attach this folder when asking for help") | **Endorse** | High | Needed now |
| D5-a | Loop shape | **Two-phase closure loop, accumulate-in-closure; preflight refuses stages requiring sL-BFGS until one exists** | **Endorse (one guard added)** | High | Needed now (one-way) |
| D5-b | Collocation infra | **Sampler interface (uniform + spec adaptive), stateful-hook signature** | **Endorse** | High | Interface needed now (one-way) |
| D5-c | Loss-weight machinery | **Scheduled-weights module + empty rebalance seam** | **Endorse** | High | Interface needed now (one-way) |
| D6 | Determinism policy | **Accepted-variance + full seed/RNG record + strict-CPU debug switch; seed band calibrated by 2–3 stage-0 pilot repeats** | **Endorse** | High (policy); band is empirical | Seed schema needed now |
| D7-a | Boundary checkpoints | **Dual anchors (`stage-k-final` + `stage-(k+1)-init`)** | **Endorse** | High | Needed now (one-way) |
| D7-b | Optimizer at boundary | **Complete Adam reset (spec-mandated); no partial-carry support** | **Endorse** | High | n/a (spec) |
| D7-c | Rollback policy | **Manual `--resume … --hold-stage` now; auto-revert (D) only after R1b signal exists** | **Endorse** | Medium | C needed now; D deferrable |
| D7-d | Mid-promotion crash | **Idempotent ordered promotion + `curriculum.jsonl`** — extended to also record RECOVER/HALT dispositions | **Endorse (amended)** | High | Needed now (one-way) |
| B-1 | PH-7 optimizer default | **Replace with `ctl_instruction.md` Phase-2 stage-0 schedule** | **Endorse** | High | Needed now |
| B-2 | Committed log fields | **Widen to 5 terms + λ vector + grad-norm; add causal-weight stats (scalars) now; per-time-bin residual panel early** | **Endorse (extended per r1b D-9)** | High | Needed now (scalars); panel deferrable |
| B-3 | Controller naming | **Name `CurriculumController` / `RunController`** | **Endorse** | Medium | Free at skeleton-writing time (two-way) |
| B-4 | Placeholder inventory | **Extend per sheet + add RECOVER/HALT mechanics, wall-clock cadence, validation-cadence knob** | **Endorse (extended)** | High | Deferrable (docs) |
| B-5 | Resume config-diff rule | **Field-classified diff; unclassified fields default to identity (refuse)** | **Endorse (fail-safe added)** | Medium | Needed now (settle before run #1) |
| B-6 | Run-folder members | **Adopt additive list + environment fingerprint (`sw_vers`, `python -V`, framework build, lockfile hash)** | **Endorse (extended per r1b D-12)** | High | Needed now (before runbook) |
| B-8 | ε_H gate direction | *Spec-settled: smaller passes.* Implement as such; fix the design-doc §6.3 display slip cosmetically | n/a (closed) | — | — |
| B-9 | Config approach | **Single YAML keyed `stage/opt/loss/run`; frozen resolved copy in the run folder** | **Endorse** | Medium | Needed now (schema) |
| B-10 | Sleep wrapper | **`caffeinate -is <cmd>`; lid-open + AC rule; trainer treats SIGTERM like one Ctrl-C** | **Endorse (r1b doctrine folded in)** | High | Needed now |
| B-11 | Reproducibility wording | **Re-scope to statistical equivalence + exact checkpoint continuation** | **Endorse** | High | Doctrine now; doc edit deferrable |

---

## 2. Per-decision resolutions

### D1 — ML framework

**Recommendation:** **D1-A — PyTorch 2.12 + MPS backend**, float32 in the training loop under branch (i); the identical code on `device="cpu"` with `torch.set_default_dtype(torch.float64)` under branch (ii) — i.e., the sheet's (ii)-1. First build act in either branch: run the spec's §10 acceptance probes on the training device with `PYTORCH_ENABLE_MPS_FALLBACK` **unset**, so any missing kernel in the double-backward graph fails loudly.

**Endorse or override:** **Endorse.** Both prior documents converge here (`trainex-r1a-options-and-decisions.md` D1; `chatgpt-pro-resolution.md` §4.5), and every Phase-1 perspective independently lands on it. PyTorch is the only candidate that simultaneously (a) uses the GPU this machine has, (b) ships the L-BFGS the science spec mandates (`torch.optim.LBFGS` with strong-Wolfe line search — `ctl_instruction.md` Phase 2b requires L-BFGS; MLX ships none, F11), (c) matches the spec's own illustrative AD code and §10 probes (`pinn_architecture.md` PHYS-02 lists `torch.func.jacrev`+`vmap` as an acceptable pattern), and (d) minimizes searchable-help friction for a non-expert. MLX's structural blocker (no L-BFGS) and JAX's honest hardware picture (jax-metal effectively dead per F12 and r1b DRO-1/D-2; "JAX on this Mac" means CPU) are grounded in both r1a's verified capability baseline and r1b's independent verification.

**Confidence:** **High.** Biggest uncertainty: **U-9** — whether every kernel in *this* network's double-backward graph (SIREN sin, LayerNorm, the SQR skip path, the COM projection) has an MPS implementation. Not provable from documentation; the §10.3 componentwise-AD probe with fallback disabled is the adjudication instrument, and the fp64-CPU branch is the in-framework escape if it fails.

**Consistency:** Anchors everything else: first-party TensorBoard writer (D2), `torch.optim.LBFGS` closures (D5-a), `torch.save`/`torch.load` with the `weights_only` rule (D4-b), `torch.mps` memory/RNG API (D3, D6). One practical note from the sheet stands: through PyTorch 2.7.0, `torch.func.jacfwd` broke on MPS for concat-bearing traced functions (as_strided bug, fixed ≥2.7.1); at 2.12 this is past, but the probe should exercise the AD pattern the trainer will actually use — and per r1b D-4, scalar-`u` forward-mode (`jacfwd`/jvp-based) is the ~order-of-magnitude cost lever the probe should also time, since PHYS-02's "equivalent full-Jacobian method" clause admits it.

**Timing:** **Needed now** — one-way door; code, checkpoints, runbook, and all R2 numbers inherit it.

**Nature:** Research-settled at the framework level; the *device* consequence is carved to the owner's precision adjudication (D1-p), which the §10 probes feed empirically.

---

### D2 — Experiment tracking and the monitoring surface

**Recommendation:** **TensorBoard as the secondary view**, with `runs/<name>/logs/train.log.jsonl` as the **canonical record**, TB event files homed inside `runs/<name>/tb/`, and one small plotting script for end-of-run PNGs in `summary.md`.

**Endorse or override:** **Endorse.** Both prior documents agree in substance (the depth report phrases it "JSONL/CSV canonical + TensorBoard as optional local view"). The spec's own Implementation Notes name TensorBoard for logging the five loss terms, scheduled weights, gradient statistics, and conservation metrics (`ctl_instruction.md`), so this is also the least-surprise pick. W&B-offline stays disqualified for a no-cloud project (viewing requires `wandb sync` or self-hosting, F14); MLflow adds a second metadata store a single-user project doesn't need (F15).

**Confidence:** **High.** Biggest uncertainty: none material — the JSONL-canonical rule is precisely what makes this a cheap experiment.

**Consistency:** The JSONL-canonical rule is the hinge that keeps this a two-way door (§9 of the sheet, conditional door classification). It also feeds B-2 (the widened field set is the JSONL schema), B-6 (`tb/` inside the folder contract), and D6 (comparison happens on validation metrics in the record, not on TB pixels).

**Timing:** **Needed now** for the JSONL log and the TB writer (both trivial and spec-named); the end-of-run plotting script is **deferrable** (the slice can read TB and the log tail).

**Nature:** Research-settled.

---

### D3 — Data residency and compute utilization under 24 GB

**Recommendation:** **D3-C's selector with `auto` defaulting to full in-memory float32 preload** (fp64 parse → fp32 cast at the adapter boundary, honoring the offline-fp64 contracts), `num_workers=0`, `torch.mps.set_per_process_memory_fraction(0.7)` at startup (0.7-vs-0.8 is a knob whose final value joins the Stage-2 consolidation), and a `mem:` log line each 1,000 steps. **Two amendments from the current specs:** (1) the adapter must expose `n_snapshots(traj)` and `dt_out(traj)` as metadata (`ctl_instruction.md` LOOP-06 requires the loader to keep these exposed); (2) the adapter loads only the **admitted** set — the Step-1A admission gate (blacklist, DATA-05 quarantine, structural/completeness/conservation clauses) "runs at DataLoader init" per `ctl_instruction.md`, so the adapter is where its admitted/rejected/quarantined counts get logged.

**Endorse or override:** **Endorse the sheet; explicitly overrule the depth report's divergent default.** `chatgpt-pro-resolution.md` §6.7 suggested streaming-first (chunked HDF5 + bounded cache + a `doctor` benchmark harness). That was the one real intra-prior-round contradiction on D3, and the evidence now favors the sheet's side: the current `ctl_instruction.md` supplies verified snapshot-count **medians** (61 standard-base / 127 hierarchical-base / 1003 gold — LOOP-01 note), from which the full 15,028-trajectory corpus works out to roughly **6.2 M snapshots ≈ 0.55 GB in fp32 / 1.1 GB in fp64** (derived arithmetic: `N_traj × S̄_median × 88 B or 176 B`, sets per the spec's Table: 4,857 hierarchical-base, 4,857 standard-base, 2,749 + 2,565 gold). That is far below the sheet's own ~6–8 GB streaming threshold, and r1b independently estimated total steady-state training memory at 2–7 GB, "comfortably inside 24 GB" (§1.6). The mediating fact remains that the adapter's "batches by index" interface hides residency entirely, so the auto-selector keeps the depth report's concern covered as a config flip if per-stage cumulative bytes ever surprise. Streaming's cost — reintroducing DataLoader worker processes, the most common PyTorch beginner failure class — is exactly what the operator constraint says to avoid. (Registered: the medians are population medians, not per-file guarantees; the completeness gate's `final_timestep ≥ 9.5` bounds the horizon below but not above. Also registered: the sheet's §3.1 swapped which sets are gold — it put 4,857 in `hierarchical_gold` where the spec's Table assigns 2,749 to Set 2a — making its worst-case bracketing conservative; cosmetic, direction-safe.)

**Confidence:** **High** on the structure (selector + adapter seam), **Medium** that `auto` lands in-memory for every cumulative stage — the remaining project-side number is exact per-stage cumulative bytes (U-1, now only *partially* closed by the medians).

**Consistency:** `num_workers=0` composes with D5-a (batch assembly on CPU, forward/backward on MPS, no worker pickling); the 0.7 watermark makes the trainer OOM itself catchably rather than swap the OS, which is what D4-c's memory guard watches; the metadata exposure (LOOP-06) is a forward interface for the deferred collocation-density question, costing nothing now.

**Timing:** Adapter batch-interface (and the metadata fields) **needed now** (mild one-way — it is the baseline's own committed seam); residency policy **two-way**.

**Nature:** Partly **empirical** — the auto threshold consumes project-supplied per-stage byte counts; flag for the owner only if a stage's measured bytes approach the threshold.

---

### D4-a — Checkpoint cadence and retention

**Recommendation:** **B-retention** exactly as the sheet defines it (rolling `K=3` `step-XXXXXX.pt`, plus `best.pt`, plus D7's stage anchors excluded from deletion, plus `latest.pt` as a *copy*), **but with a dual cadence trigger: checkpoint every `checkpoint_every=1000` steps *or* every wall-clock ceiling, whichever comes first.** The ceiling's exact value is left open (r1b grounds a robust range of "e.g., every 15–30 min", §1.8; the specific number is an owner/Stage-2 pick informed by the smoke-test's measured s/step).

**Endorse or override:** **Override the cadence, endorse the retention.** This is the sheet's weakest row: it "kept" the baseline's step-1000 default while its own companion evidence argued against a pure step cadence — `trainex-r1b-findings.md` §1.8 shows worst-case lost work is `checkpoint_every × t_step`, which is 100 s at 0.1 s/step but **83 minutes at 5 s/step**, inside the credible envelope since t_step is unknown across a ~30× range; `trainex-r1b-findings-2.md` DRO-6 states the recommendation directly ("checkpoint cadence should consider wall-clock, not only steps"); and `chatgpt-pro-resolution.md` §7.4/7.9 independently chose a wall-clock+event hybrid. Three grounded voices against an unexamined "kept" — the override is low-risk (a config addition) and protects the unattended-run premise.

**Confidence:** **High** on the structure; the ceiling value is the open piece and is deliberately not invented here.

**Consistency:** Disk math stays trivial (~9 MB per checkpoint per the sheet's §0 arithmetic); the wall-clock trigger uses the same atomic write path (D4-b) and the same pre-write disk check (D4-c).

**Timing:** **Needed now** (cheap; the unattended premise depends on it).

**Nature:** The ceiling value is **owner preference informed by an empirical number** (measured t_step from the smoke test).

---

### D4-b — Corruption safety

**Recommendation:** **Adopt** as specified: serialize to `*.pt.tmp`, `flush`+`fsync`, `os.rename`, then update `latest.pt`; on resume, fall back to the newest readable `step-*.pt` and say so; checkpoints contain only state_dicts/tensors/plain scalars so `torch.load` works under the 2.6+ `weights_only=True` default (F8). Optional cheap addition borrowed from the depth report: record each checkpoint's checksum in `status.json`/`curriculum.jsonl` so resume can detect truncation explicitly — additive, adopt if it costs a line.

**Endorse or override:** **Endorse.** Unanimous across perspectives and both prior documents; the `weights_only` rule is what keeps the runbook free of `add_safe_globals` incantations.

**Confidence:** **High.** No material uncertainty.

**Consistency:** The atomic path is shared by ordinary, wall-clock, guard-emergency, and stage-anchor writes (D4-a/c, D7).

**Timing:** **Needed now** (free to adopt early, expensive to retrofit trust into).

**Nature:** Research-settled.

---

### D4-c — Auto-guards for unattended runs

**Recommendation:** **Tier 1 + Tier 2 on by default** (NaN/Inf stop, loss-explosion kill switch, disk-floor guard, memory-watermark guard, heartbeat file), with the three loop seams (post-loss check, pre-checkpoint check, heartbeat write) built into the skeleton from day one — **plus a spec-drift amendment the sheet could not have known about:**

The current `ctl_instruction.md` (Phase 33, CURR-03) defines the stage-exit decision as a **three-disposition state machine — ADVANCE, RECOVER, HALT/REVIEW**. RECOVER is *in-loop behavior the spec itself mandates*: "If training produces NaN or Inf gradients … the loop rolls back to the last well-formed checkpoint and retries with a bounded retry budget," with retry limits provisional pending Stage-0 pilot calibration; exhaustion routes to HALT/REVIEW, never to advancement. HALT/REVIEW likewise requires the loop to **halt and surface the stage for owner review** when a per-stage max-epoch budget or a stagnation window trips (values provisional). Two consequences:

1. The sheet's Tier-3 rationale ("auto-remediation … turns the trainer into an agent making science-adjacent decisions the spec assigns to operator+spec contracts") is now **partially contradicted by the spec**: bounded rollback-and-retry on non-finite gradients is spec-assigned *loop* behavior, not operator improvisation. The correct reconciliation: build the **RECOVER seam now** — the NaN/Inf guard's action gains a config'd `recover.retries` whose **default is 0** (behaving exactly like the sheet's Tier-1 stop-and-preserve) until the Stage-0 pilot calibrates a budget. Auto-LR-mutation and other Tier-3 remediation remain excluded — the spec mandates rollback-retry, nothing more.
2. Add a **HALT/REVIEW guard family**: per-stage max-epoch and validation-stagnation halts, thresholds provisional per the spec's own text (the issue-doc epoch tables are explicitly claimed-unverified). For the Stage-0 slice these can start as generous placeholders or disabled — but the seam exists and `curriculum.jsonl` records the disposition (see D7-d).

**⚖ thresholds stay placeholders** per the round contract. For the record (Phase-2 blind-spot audit): the r1b files supply **no number** for the loss-explosion multiple or its consecutive-log count, **no fixed number** for the disk floor (the depth report argues it should be formula-based: temp file + retained file + reserve), and **no number** for the memory-watermark multiple/consecutive count. The heartbeat rule's "10 min" is the sheet's own runbook proposal. All registered (§5).

**Endorse or override:** **Endorse the tiers and seams; amend for CURR-03.**

**Confidence:** **Medium** — the tiers themselves are high-confidence, but the RECOVER instantiation depends on a spec whose thresholds are self-declared provisional, and the ⚖ values are unfilled.

**Consistency:** Every guard consumes D5-a's closure/seam structure (no second mechanism); guard stops share D4-b's atomic write and D4-d's bundle; RECOVER's "last well-formed checkpoint" is exactly what B-retention + anchors guarantee exists.

**Timing:** **Seams needed now** (retrofitting hooks into a live loop is the rework case, per the sheet's own door analysis); toggles and thresholds **two-way**.

**Nature:** Threshold values are **empirical/Stage-2** (⚖) and the RECOVER retry budget is **owner-ratified after the Stage-0 pilot** (the spec says so explicitly).

---

### D4-d — On-failure diagnostic bundle

**Recommendation:** **Always on**, with the sheet's checklist (traceback, env, frozen config + SHA-256, log tail, state.json, memory readings, data-hash pointer), plus the depth report's one-line `README.md` ("Attach this directory when asking for help") — it makes the runbook step literal.

**Endorse or override:** **Endorse.**

**Confidence:** **High.**

**Consistency:** Written by guard stops (D4-c), uncaught exceptions, and HALT/REVIEW; contains the environment fingerprint B-6 adds to the folder contract.

**Timing:** **Needed now** (cheap, and the non-expert's help loop depends on it).

**Nature:** Research-settled.

---

### D5-a — Training-loop skeleton: loop shape

**Recommendation:** **D5-B — two-phase, closure-shaped loop** (Adam step-per-batch; L-BFGS driven by a `closure()` that recomputes the loss; "full-batch" realized as **gradient accumulation inside the closure**, keeping peak memory at one-batch scale). Phase flags honor the spec's frozen-λ and no-clipping rules during L-BFGS. **One guard added from the depth report:** preflight **refuses to enter any stage whose spec-mandated optimizer is sL-BFGS** (stages 3–6) until a concrete implementation is selected and validated — this converts the U-7 gap from a silent science deviation into a typed stop.

**Endorse or override:** **Endorse** (the added preflight guard is additive, not a shape change). The controlling facts are spec-side and unambiguous: `ctl_instruction.md` Phase 2 mandates Adam→L-BFGS per stage with a plateau handoff, complete Adam reset per stage, per-stage LR ladder `1e-3 × 0.7^k` with cosine annealing, adaptive median clipping (Adam only), scheduled weights with re-warm, and replay+lookahead batches. D5-A cannot express Phase 2b (a conscious descope at best); D5-C's pluggable-phase abstraction buys generality the spec's *fixed* phase order doesn't need — and the depth report's own Option B ("small state machine") is substantively D5-B plus the named seams already adopted here. The accumulate-in-closure move is the structural answer to r1b's D-7 flag (a literal full-batch second-order graph over the cumulative stage-2 set, gold included, would exceed 24 GB); its residual cost is closure wall-time, an R1b-lane duration question, not memory.

**Consistency:** The closure is the **hidden connection of this whole resolution**: it is the one seam that D4-c's guards hook (post-loss check), D7-d's promotion consumes (a defined safe point), the spec's RECOVER path needs (loss construction as a callable that can be re-entered after rollback), and the L-BFGS memory answer lives in. Batch assembly inside the loop follows the now-canonical LOOP-01/02/03 contracts (240 replay + 16 lookahead with the three resolved edge cases; data vs collocation point sets kept role-separate even in one concatenated forward pass; 50/50 Gumbel-top-k data-point sampling retained).

**Confidence:** **High.** Biggest uncertainty: closure wall-time for full-batch phases (durations are the R1b/U-15 lane; the smoke test measures the Adam side, and the first L-BFGS phase should be watched).

**Timing:** **Needed now** — the loop shape *is* the skeleton; one-way.

**Nature:** Research-settled (spec-mandated structure). sL-BFGS implementation ownership (U-7) remains an **owner scheduling decision or spec-level renegotiation** — out of the slice's path (stages 0–2 are full-batch) but registered.

---

### D5-b — Collocation infrastructure

**Recommendation:** **D5-E — sampler interface** `sampler(stage, step) → u_col` with `uniform` and the spec's acceleration-weighted `adaptive` shipped behind `collocation.strategy`, and the **stateful-hook signature** (a sampler *may* receive `(model, last_residuals)`) defined now, pool machinery later.

**Endorse or override:** **Endorse.** Current-spec check: Phase 34 LOOP-03 explicitly **defers** a mandatory 50/50 mixed continuous collocation sampler and says "the current uniform/adaptive collocation choices remain usable" — so E is exactly spec-aligned; F's residual-pool machinery (RAD) remains not-called-for, and the near-free hook signature is the hedge. LOOP-06 defers dt_out-aware collocation scaling to FUT while requiring the metadata exposure D3 already adopted.

**Confidence:** **High.** Biggest uncertainty: none structural; `n_col`'s value is R2's (the spec's 4,096 is a provisional/example budget per LOOP-02).

**Consistency:** Uniform default for the slice; the interface signature is the one-way part; strategies and densities are config.

**Timing:** Interface **needed now** (one-way); strategy contents two-way.

**Nature:** Research-settled.

---

### D5-c — Loss-weighting machinery

**Recommendation:** **D5-H — a `WeightSchedule` module** (inputs: stage, phase, step-in-phase → λ vector; logged every `log_freq`; serialized into checkpoints so resume restores mid-warmup state exactly), **plus the empty D5-I rebalance seam** (a no-op callable site after backward).

**Endorse or override:** **Endorse.** The spec settles the plumbing question: weights are scheduled (PHYS-05 warmup `I_warm = min(2000, 0.1·N_Adam,k)`, per-stage `λ^max` tables with `λ_E^max ≤ 1` per LOSS-02), frozen during L-BFGS, re-warmed at every boundary. Static weights (G) fail the spec. Notably, LOSS-02 also *strengthens the case for the empty seam staying empty*: "automatic dominance reweighting is **deferred** until measured weighted-loss/gradient evidence exists" — and it mandates the very instrumentation B-2 adopts ("training instrumentation must log weighted losses, scheduled weights, and gradient statistics" before any future control law).

**Confidence:** **High.** Biggest uncertainty: the causal-weight underflow clip bound, which the spec explicitly declines to choose (U-6) — set at implementation with a logged rationale, exactly as the sheet routes it.

**Consistency:** Checkpoint serialization of schedule state is what makes D7's re-warm-on-promotion and resume-mid-warmup exact; the λ logging feeds B-2 and the K1 watchlist's "confirm the warmup actually ramped" response.

**Timing:** Interface **needed now** (one-way); values two-way.

**Nature:** Research-settled; U-6's bound is a logged implementation choice.

---

### D6 — Reproducibility and determinism policy

**Recommendation:** **B + C** — accepted-variance with a fully recorded seed set (Python/NumPy/`torch.manual_seed`/`torch.mps.manual_seed`, split seed, shuffle seeds; echoed into config, `status.json`, and checkpoints; RNG states checkpointed for exact-resume continuity), no `use_deterministic_algorithms` in production, **plus** a `determinism: strict` debug switch that flips to CPU + deterministic algorithms + `warn_only=True` for bisecting on a small problem. Comparison doctrine: judge runs on validation metrics at fixed checkpoints against a **seed-to-seed band** calibrated once by running the short stage-0 pilot 2–3× with different seeds.

**Endorse or override:** **Endorse.** The ground truth is verified and sobering: PyTorch's official doctrine disclaims cross-platform/CPU-vs-GPU bitwise reproducibility (F6), and MPS specifically has an open issue showing non-identical training *despite* full seeding and the deterministic flag, which itself carries a measured ~7× slowdown example (F7) — strict-always would pay the price without securing the property. The depth report's two-tier framing (deterministic CPU acceptance lane + provenance-complete accelerator lane + ≥3 paired seeds for consequential A/Bs) is substantively the same policy: its acceptance lane maps onto the r1b ladder's rung-2 fp64-CPU checks and the strict debug switch; its paired-seed floor is the seed-band protocol with an explicit count. Adopt the band; if a comparison is ever load-bearing, the depth report's "three paired seeds, report all values plus median and range" is the grounded floor.

**Confidence:** **High** on the policy. Biggest uncertainty: the band itself is **empirical** — until the pilot repeats run, "better than my last run" has no calibrated meaning on this hardware.

**Consistency:** The seed/RNG block in the config+checkpoint schema is the mildly one-way part (artifact contract from run #1); B-11's re-scoped wording is this policy's documentation face; r1b's golden-smoke re-validation (K2 §4.4) consumes the same fixed-seed smoke config.

**Timing:** Seed/RNG schema **needed now**; band calibration piggybacks on the stage-0 pilot (cheap, effectively needed-now once comparisons start).

**Nature:** Policy is research-settled; the band is **empirical**; the confirmatory seed count for future A/Bs is an **owner** call informed by measured durations.

---

### D7-a — Boundary checkpoint guarantee

**Recommendation:** **D7-A — dual distinguishable anchors**: `stage-{k}-final.pt` (rollback target) and `stage-{k+1}-init.pt` (weights carried, fresh optimizer, re-warmed schedule state, advanced stage field), both excluded from rolling deletion.

**Endorse or override:** **Endorse.** The spec's implementation note requires a checkpoint at each stage completion; A makes it distinguishable and adds the post-init twin so a boundary crash is unambiguous. The depth report's transactional variant reaches the same crash semantics with heavier machinery (journal hashes, immutable IDs, a `rollback` CLI that branches run identity) — adjudicated under D7-d.

**Confidence:** **High.** No material uncertainty.

**Consistency:** Anchor names are artifact contract (one-way); they are what RECOVER's "last well-formed checkpoint" and D7-c's rollback command point at.

**Timing:** **Needed now** (one-way naming; the slice may cross its first boundary if stage-0 criteria fire).

**Nature:** Research-settled.

---

### D7-b — Optimizer state at the transition

**Recommendation:** **Spec-mandated complete Adam reset** (construct a new `torch.optim.Adam` at stage start); L-BFGS history never crosses a boundary; the skeleton does **not** support partial carry (a later two-way experiment flag if the owner ever wants it).

**Endorse or override:** **Endorse.** Not genuinely open — `ctl_instruction.md` marks the complete reset "Critical." Both prior documents and the depth report's §10.5 agree partial carry is a scientific deviation outside this round's authority.

**Confidence:** **High.** · **Consistency:** the reset is step (5) of D7-d's ordered promotion. · **Timing:** needed now. · **Nature:** spec-fixed (n/a).

---

### D7-c — Rollback policy when a fresh stage goes bad

**Recommendation:** **D7-C now** — manual, one documented command: `--resume runs/<name>/checkpoints/stage-{k}-final.pt --hold-stage` (the `--hold-stage` flag prevents just-met promotion criteria from immediately re-firing). **D7-D (auto-revert on post-promotion divergence) is specced only after Stage-2 consolidation**, off by default.

**Endorse or override:** **Endorse**, with one clarifying distinction the CURR-03 drift makes necessary: the spec's **RECOVER** covers *numerical* failure (NaN/Inf → bounded rollback-retry; handled at D4-c) and is **not** the same thing as D7-D's *divergence-quality* auto-revert. The latter's trigger signal is genuinely absent from the r1b files — the K1 watchlist gives only the qualitative guidance that a stage-boundary loss jump is *scheduled and normal* and that per-term curves should resume a downward trend "within ~2,000 steps" (a watch heuristic, not a guard threshold). With no validated signal, an auto-revert can reject valid hard-stage behavior (the depth report's own §10.4 warning). Manual-with-a-one-liner is the honest default.

**Confidence:** **Medium** — C is safe, but the boundary between "spec-mandated RECOVER" and "deferred D" depends on a divergence-signal definition that does not yet exist.

**Consistency:** Uses D7-a's anchor and D7-d's records; the runbook inherits the exact command shape.

**Timing:** C's command **needed now** (documentation + the `--hold-stage` flag); D **deferrable**.

**Nature:** D's signal is **empirical (Stage-2/R1b join)**; enabling it is then an **owner** policy call.

---

### D7-d — Resume across a boundary / death mid-promotion

**Recommendation:** **Adopt the idempotent, ordered promotion**: (1) write `stage-{k}-final.pt` atomically; (2) append a promotion record to `runs/<name>/curriculum.jsonl` (`{from, to, step, criteria_snapshot}`); (3) construct new optimizer + schedule; (4) write `stage-{k+1}-init.pt`. On resume, trust the checkpoint's stage/phase fields and reconcile against `curriculum.jsonl`; a final-anchor without its init-twin means the crash hit mid-promotion — redo (3)–(4) deterministically. **One amendment for CURR-03:** `curriculum.jsonl` records **all three dispositions**, not just promotions — RECOVER events (`{disposition: recover, retry_n, restored_checkpoint, step}`) and HALT/REVIEW events (`{disposition: halt, trigger, step}`) — so the spec's state machine has its audit trail and the operator's "what stopped my run?" has one file to read.

**Endorse or override:** **Endorse (amended).** This is the deliberate middle path between the sheet and the depth report's full transactional journal (PREPARED/COMMITTED records, source/target hashes, rollback-as-new-run-identity). The heavyweight version's *crash semantics* are fully captured by the ordered write + jsonl reconciliation; its *branching lineage and checksum schema* are platform engineering the viability-slice lens (`postspec-r1-direction-assessment.md`: a hardened platform is the *output* of a successful slice, not its prerequisite) says to defer. The user-visible invariant is kept verbatim: **resuming never re-asks "what stage am I in?" — the checkpoint knows.**

**Confidence:** **High.** Biggest uncertainty: none structural; the criteria_snapshot's exact contents firm up when the validation cadence (U-5) gets its knob value.

**Consistency:** Extends D4's resume invariants additively; gives §6.2's curriculum-progression summary its data source; the disposition records are what B-3's `CurriculumController` owns.

**Timing:** **Needed now** — anchor names, stage/phase checkpoint fields, and `curriculum.jsonl` are the one-way artifact contract.

**Nature:** Research-settled.

---

### B-1 — PH-7 first-trial optimizer default

**Recommendation:** **Replace** the baseline's PhysicsNeMo-derived default (Adam 1e-3, exponential 0.95/500) with "the `ctl_instruction.md` Phase-2 schedule, stage-0 values": LR `1e-3 × 0.7^k`, cosine annealing, two-phase with L-BFGS (history 10, strong-Wolfe, max_iter 20), curriculum-aware median clipping (C = 7–10 for stages 0–1 per the locked AC-LOOP-04 table, exact early-stage value deferred by the spec itself), no clipping during L-BFGS.

**Endorse or override:** **Endorse.** The specs own the science; keeping the baseline default would have the first run silently off-spec. This was the only genuine cross-document conflict the sheet found, and its resolution is clean. · **Confidence:** **High.** · **Consistency:** the config values live inside D5-a's loop shape; B-9's `opt:` key holds them. · **Timing:** **Needed now.** · **Nature:** spec-conformance (research-settled).

### B-2 — Committed monitoring fields

**Recommendation:** **Widen** the committed log line and `summary.md` to the five loss terms (data, IC, phys-causal, E, L) + total + current λ vector + grad-norm/clip events — and, per r1b D-9, **add two watchlist-enabling surfaces**: (a) causal-weight statistics (min/mean w_n, fraction > 0.5) as scalars at `log_freq` — **now** (they are the only way to see causal-weight collapse, r1b's silent-freeze failure mode); (b) a per-time-bin physics-residual panel at validation cadence — **early** (it is the propagation-failure detector; without it a slice can look healthy while the solution never leaves the IC).

**Endorse or override:** **Endorse (extended).** The spec's Implementation Notes and LOSS-02's instrumentation mandate both require this set; the r1b extension is what makes two of the K1 watchlist's highest-value rows *observable at all*. · **Confidence:** **High.** · **Consistency:** the JSONL schema tolerates additive keys (D2's two-way condition); λ logging comes from D5-c's module. · **Timing:** five terms + λ + grad-norm + w_n scalars **needed now**; the residual panel **deferrable to early** (before the first long unattended run). · **Nature:** research-settled.

### B-3 — Name the controller components

**Recommendation:** **Name them**: within Subsystem 3, `CurriculumController` (stage/phase, `curriculum.jsonl`, the D7 promotion procedure, and now the CURR-03 dispositions) and `RunController` (guards, `status.json`, Ctrl-C/SIGTERM/bundle handling). Structure-naming only; the plain-script style stays.

**Endorse or override:** **Endorse.** · **Confidence:** **Medium** (it is a taste-adjacent internal-naming call; the value is giving the runbook nouns for "what stopped my run"). · **Consistency:** the two names are exactly where the CURR-03 amendment and D4's guards live, which strengthens the case beyond the sheet's original argument. · **Timing:** free if adopted at skeleton-writing time (i.e., now); two-way regardless. · **Nature:** mild owner preference.

### B-4 — Extend the placeholder inventory

**Recommendation:** **Extend** per the sheet (precision policy, determinism policy, checkpoint policy, guards, boundary mechanics, collocation infrastructure vs strategy, sL-BFGS ownership, validation-evaluation cadence, config schema versioning) **plus three items this round adds**: RECOVER/HALT-REVIEW mechanics and their provisional thresholds (CURR-03); the wall-clock checkpoint ceiling; and the two D-9 monitoring surfaces.

**Endorse or override:** **Endorse (extended).** · **Confidence:** **High.** · **Timing:** deferrable (documentation) — but the *validation-cadence knob's existence* is a needed-now D5 skeleton fact, adopted there. · **Nature:** documentation.

### B-5 — Resume config-diff rule

**Recommendation:** **Field-classified diff**: identity fields (architecture, data version, split seed, curriculum definition, loss/schedule contracts) → any diff refuses resume; operational fields (`max_steps`, `log_freq`, guard toggles, tracker settings, the wall-clock ceiling) → resume with a logged `CONFIG CHANGE:` line. **Fail-safe amendment:** any field not explicitly classified defaults to **identity** (refuse) — so a misclassification or a schema addition fails safe rather than silently resuming across a semantic change.

**Endorse or override:** **Endorse (fail-safe added).** The blunt rule bricks resume on a `max_steps` extension — exactly the operation a long run needs. · **Confidence:** **Medium** — the classification itself is judgment applied before the schema fully exists; the default-to-identity rule is the mitigation. · **Consistency:** becomes part of B-9's schema; the frozen config copy + diff log preserves provenance. · **Timing:** **Needed now** (soft one-way: settle before run #1). · **Nature:** partially **owner** — which fields count as identity encodes risk tolerance; the proposed split is the recommendation, the ratification is the owner's.

### B-6 — `runs/<name>/` folder-contract additions

**Recommendation:** **Adopt** the additive member list (`tb/`, `checkpoints/stage-*-{final,init}.pt`, `curriculum.jsonl`, `failure/`, seed record in `status.json`, `data-manifest.json`) **plus the r1b D-12 environment fingerprint**: record `sw_vers`, `python -V`, framework version/build string, and the lockfile hash into every run folder at launch — without it the "give a colleague the folder" promise (even re-scoped per B-11) doesn't hold, and K2's upgrade re-validation has nothing to diff against.

**Endorse or override:** **Endorse (extended).** · **Confidence:** **High.** · **Consistency:** the fingerprint is also what D4-d's bundle copies; the final member list is the runbook's vocabulary. · **Timing:** **Needed now** (adding is free now; renaming later breaks the runbook — adopt the final list before the runbook is written). · **Nature:** research-settled.

### B-9 — Config approach

**Recommendation:** **Single YAML per run, top-level keys structured `stage:` / `opt:` / `loss:` / `run:`**, with the frozen resolved copy in the run folder (the baseline already commits this — it is the property worth preserving from the spec's Hydra note, per r1b D-14).

**Endorse or override:** **Endorse**, with one honesty note the sheet under-weighted: Hydra appears **twice** in `ctl_instruction.md` — once under the heading the spec itself marks "**Ignore Now** and Come Back Later" (the sheet's basis for treating it as deferred), but also in the **Implementation Notes** bullet ("Reproducibility: Drive runs from a three-level Hydra YAML configuration"), which carries no such marker. The strategy assessment independently defers reproducibility provenance ("the spec itself marks 'ignore now, come back later'"), and the keyed-single-YAML structure makes a later Hydra migration mechanical — so the recommendation stands — but the duplication is an ambiguity the spec owners should reconcile, registered below.

**Confidence:** **Medium** (because of that ambiguity; the engineering case is otherwise strong for the operator profile). · **Consistency:** the key structure is the Hydra hedge; B-5's field classes and B-1's values live inside it. · **Timing:** **Needed now** (the schema is what everything reads). · **Nature:** partly **owner preference** (tooling taste), research-supported.

### B-10 — Sleep-prevention wrapper

**Recommendation:** **`caffeinate -is python -m pinn.train …`** (idle + system sleep prevention scoped to the process), **plus the r1b K2 doctrine now available at this consolidation**: lid **open** and AC power for the whole run (lid-close sleeps Apple-Silicon laptops regardless of `caffeinate`; recovery is checkpoint-resume, not wake-and-hope — DRO-2, D-10); the "prevent automatic sleeping on power adapter" setting on; and the trainer treats **SIGTERM like a single Ctrl-C** so detached runs stop gracefully.

**Endorse or override:** **Endorse (doctrine folded in).** The sheet flagged final ops doctrine as R1b's lane; the r1b files are attached, so the join is executed here rather than left dangling. · **Confidence:** **High.** · **Timing:** **Needed now** (launch-command shape + two runbook sentences). · **Nature:** research-settled.

### B-11 — Reproducibility wording

**Recommendation:** **Re-scope** §5.7's promise to: *re-run to statistically equivalent results from the recorded config+seed; exact continuation from any checkpoint; not bitwise re-creation of a from-scratch run.*

**Endorse or override:** **Endorse.** Directly grounded in F6/F7 and D6's policy. · **Confidence:** **High.** · **Timing:** the **doctrine** is needed now (never make the bitwise promise); the doc edit itself is deferrable to the next revision. · **Nature:** research-settled.

---

## 3. Composed first-run recipe (coherence check)

The picks compose into this end-to-end first run — a coherence check, not the runbook.

**Step 0 — the upstream prerequisite this round cannot skip past:** the strategy assessment's **Thrust A data scan** (bin the 15,028 admitted trajectories by the difficulty invariants; count the stage populations, Stage 0 above all). It needs almost no training machinery and can reshape everything below — an under-populated Stage 0 is a named fatal-class risk (`postspec-r1-direction-assessment.md` §8). It also produces the per-stage cumulative byte counts that settle D3's `auto` verdict.

**Setup (once):** Miniforge + `conda create -n pinn-train python=3.11` + `pip install torch tensorboard pyyaml numpy h5py`; export the lockfile pair (`environment.yml` + explicit spec / `pip freeze`) per r1b K2; verify `torch.backends.mps.is_available()`.

**Pre-flight (before any run longer than 30 minutes — r1b ladder):** rungs 0–3 as a `verify` script — device sanity; the §10.3 componentwise-AD probe **on MPS, fp32, with `PYTORCH_ENABLE_MPS_FALLBACK` unset** (plus the fp64-CPU reference arm; this simultaneously certifies the AD contract and feeds the owner's D1-p adjudication); fp64-CPU gradcheck; residual-on-ground-truth + the remaining §10 probes. Then rung 4 (single-trajectory overfit) and rung 6 (the **5-minute smoke test**: ~32 stage-0 trajectories, ~300 steps — it verifies the whole mechanical surface, exercises Ctrl-C/resume, and **records s/step**, collapsing the 30×-wide duration envelope into a forecast).

**Configure** — one keyed YAML (B-9), e.g.:

```yaml
run:   { name: first-run, seed: 1234, device: mps, precision: float32,
         max_steps: 100000, log_freq: 100,
         checkpoint_every: 1000, checkpoint_wallclock_min: <owner: r1b range 15-30>,
         guards: { nan: true, loss_explosion: true, disk_floor: true,
                   memory_watermark: true, halt_review: placeholder },   # thresholds ⚖ pending Stage 2
         recover: { retries: 0 } }                                       # CURR-03 seam; budget pending pilot
stage: { start: 0, data_version: <from v1.5 PIPE-XX>, residency: auto }  # D3-C
opt:   { schedule: ctl-phase2, stage0_lr: 1.0e-3, anneal: cosine,
         lbfgs: { history: 10, line_search: strong_wolfe, max_iter: 20 } }
loss:  { weights: phys05-warmup, collocation: { strategy: uniform, n_col: 2048 } }
```

**Launch:** `caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml` — lid open, AC power, hard flat surface. The startup prints device + `mem cap` line, admission-gate counts (admitted/rejected/quarantined — Step 1A), data line, environment fingerprint, `Stage 0 of 7`, then one line per 100 steps with **five loss terms + total + lr + λ vector + grad-norm + w_n stats + s/step + ETA**, a `mem:` line each 1,000 steps, and a `status.json` heartbeat. Secondary view: `tensorboard --logdir runs/`.

**Stage-0 shape:** Adam with PHYS-05 warmup → plateau handoff → full-batch L-BFGS via accumulate-in-closure → the four ADVANCE criteria at the validation cadence (**knob exists; value U-5**) → on promotion: `stage-0-final.pt`, `curriculum.jsonl` record, fresh Adam, re-warmed λ, `stage-1-init.pt`. NaN/Inf → RECOVER seam with `retries: 0` ⇒ emergency checkpoint + `GUARD: non-finite loss` + `failure/` bundle (identical to Tier-1 stop until the pilot calibrates a budget). Max-epoch/stagnation → `HALT: <trigger>` for owner review (placeholder thresholds). Ctrl-C once (or SIGTERM) = graceful checkpoint.

**Resume / rollback:** `--resume runs/first-run/checkpoints/latest.pt`; after a bad promotion, `--resume …/stage-0-final.pt --hold-stage`. Resuming never asks what stage it is in.

**Pilot for the seed band (D6):** repeat the short stage-0 pilot 2–3× with different seeds; record the spread in `summary.md`'s comparison hint.

**Pairwise conflict check:** all six of the sheet's §11 checks still pass under the amendments; the three new elements (wall-clock trigger, RECOVER seam, HALT guard) consume existing seams (atomic writes, the closure, `curriculum.jsonl`) and introduce no second mechanism. Durations remain deliberately un-estimated — the smoke test measures them (r1b D-5/DRO-9).

---

## 4. What the runbook inherits

**Needed-now set (concrete defaults for the first runbook):**

- **Commands:** the Setup block; pre-flight = `verify` script (rungs 0–3) + smoke test; launch = `caffeinate -is python -m pinn.train --config <yaml>`; resume = `+ --resume <ckpt>`; rollback = `+ --resume …/stage-{k}-final.pt --hold-stage`; monitor = `tensorboard --logdir runs/`.
- **Ops rules:** lid open + AC for the whole run; one Ctrl-C or SIGTERM = graceful stop; `*.pt.tmp` after a crash is documented debris; "status.json older than 10 min while the process lives ⇒ hung"; never resume past a NaN without restoring; freeze macOS/framework versions mid-project, re-run rungs 0–3 + golden smoke after any upgrade.
- **Artifacts:** single-`.pt` checkpoints containing only state_dicts/tensors/scalars; names `step-XXXXXX.pt`, `latest.pt` (copy), `best.pt`, `stage-{k}-{final,init}.pt`, `emergency-*.pt`; folder contract = frozen config, `checkpoints/`, `logs/train.log{,.jsonl}` (canonical), `tb/`, `curriculum.jsonl` (all dispositions), `status.json` (heartbeat + seeds + guard state), `summary.{md,json}`, `failure/` (+README), `data-manifest.json`, environment fingerprint.
- **Monitoring vocabulary:** five terms + λ + grad-norm + w_n stats per log line; `GUARD:` / `HALT:` stop messages; the `mem:` line and what the 0.7 cap means; "a loss jump at a stage boundary is scheduled and normal — read the per-term curves."
- **Comparison doctrine:** validation metrics outside the calibrated seed band; folder promise re-scoped per B-11.
- **Failure reporting:** "zip `runs/<name>/failure/` and ask for help."

**Deferrable set (do not write into the first runbook):** tracker swaps; residency `mmap` mode; D7-D auto-revert; RECOVER retry budgets > 0; Tier-3 remediation; the residual-vs-time dashboard panel (early, but after the slice runs); sL-BFGS anything (stages 3–6 are preflight-refused until an implementation exists); Hydra migration; periodic-archive retention; the end-of-run PNG script; tmux (introduce as one optional sub-step only when runs exceed a workday, per r1b).

**Placeholders the runbook must carry, never invent:** all ⚖ guard thresholds; the wall-clock ceiling value; RECOVER retry budget; HALT max-epoch/stagnation windows; the validation cadence value; the divergence-after-transition signal; run durations (smoke test supplies per-run forecasts).

---

## 5. Claims-and-uncertainty register

Every silence, ambiguity, needed-but-absent number, and assumption. Sheet register IDs are carried forward with status updates; new items are R-numbered.

| ID | Item | Status |
|---|---|---|
| U-1 | Snapshots per trajectory / per-stage cumulative bytes (controls D3's in-memory verdict) | **Partially closed by the current spec**: `ctl_instruction.md` LOOP-01 supplies verified snapshot-count **medians** (61 standard-base / 127 hierarchical-base / 1003 gold; "population medians, not hard per-file guarantees") and Step-1A's completeness gate bounds `t_max ≥ 9.5`. Derived corpus estimate ≈ 0.55 GB fp32 / 1.1 GB fp64 — supports in-memory. **Still open:** exact per-stage cumulative bytes (stage populations come from the Thrust-A scan); the medians' spread. |
| U-2 / U-15 | M5-class step times, thermal envelope, run durations | Open; no benchmark near this workload exists in the sources (r1b C-9/C-6). The rung-6 smoke test is the designated measurement; durations are deliberately not estimated here. |
| U-3 | ε_H gate direction | **Closed** (spec-settled smaller-passes; design-doc §6.3 slip is cosmetic, fold with B-7 which is out of this round's decide set). |
| U-4 | Split-policy tension (global 80/10/10 vs per-stage cumulative 10–20% hold-out) | Open; routed to v1.5/PH-5 (B-12, out of decide set). The stage-stratified-global-split reading remains the compatible one. |
| U-5 | Validation-evaluation cadence | **Still open in the current spec** — the ADVANCE criteria consume `L_val(i)` but no document states how often validation runs. The knob's existence is adopted (D5 skeleton fact); its value is R2/owner. |
| U-6 | Causal-weight underflow clip bound | Open by the spec's explicit instruction (LOSS-04: "no numeric clipping bound is selected … deferred to FUT"). Set at implementation with a logged rationale. |
| U-7 | Stochastic L-BFGS algorithm/ownership | Open. No framework ships it (F11/F13; torch LBFGS assumes a consistent objective). Preflight-refusal guard adopted (D5-a) so the gap cannot be crossed silently. Owner must schedule the implementation or renegotiate at spec level before stage 3. |
| U-8 / U-10 | MLX fp64-CPU op coverage; MLX/Metal determinism | Moot under the D1 pick; carried unchanged. |
| U-9 | MPS double-backward kernel coverage for this net | Open until the §10.3 probe runs on-device with fallback disabled (first build act). |
| U-11 | Referenced-but-unattached materials | **Updated:** the SCS gate and the SASD/IPR/PSC data-side metric contracts are now present in the attached `ctl_instruction.md` (partially closing the sheet's claim that metric definitions were unavailable). Still unattached: `sampling_method.md` (frozen data-generation spec — out of scope per the mandate), the Phase 18 FRAME-01 preprocessing doc, v1.5 PIPE-XX format/hash mechanism, and the §10 probe scripts under `.planning/…`. Treated as unavailable; nothing above depends on their contents. |
| U-12 | `data_version_hash` production mechanism | Open (v1.5 PIPE-XX); the adapter implements compare-and-refuse only. |
| U-13 | TensorBoard release pin | Open; pin at install time (`pip show tensorboard`). |
| U-14 | SI-PINN-003 batch-construction inconsistency | **Closed by the current spec** (Phase 34: `ctl_instruction.md` Mini-Batch Construction is canonical; `pinn_architecture.md` §3.1 now points to it). |
| R-1 | **⚖ guard thresholds the r1b files do not number** (Stage-2 fills; recorded per the round contract): loss-explosion multiple and consecutive-log count — **no number in r1b**; disk-floor GB — **no fixed number** (depth report argues formula-based: temp + retained + reserve); memory-watermark multiple and consecutive count — **no number**; post-promotion divergence signal — **qualitative only** (per-term curves resume downward "within ~2,000 steps" is a watch heuristic, not a guard trigger). r1b **does** ground: the wall-clock cadence range ("e.g., every 15–30 min", §1.8), the heartbeat concept (the 10-min value is the sheet's own proposal), and the twice-daily monitoring rhythm for day-scale runs. | Open (Stage 2). |
| R-2 | **RECOVER retry budget; HALT/REVIEW max-epoch table and stagnation window** | Provisional **by the spec's own declaration** (CURR-03: "provisional pending FUT Stage-0 pilot calibration"; the issue-doc epoch tables are claimed-unverified and not transcribed as locked). Seams built now; `recover.retries: 0` and placeholder HALT values until the pilot. |
| R-3 | **Hardware confirmation** | Both r1b files flag that no shipping M5 Pro matches the project docs' "16 CPU / 15 GPU" (Apple's lineup: 15/16 base or 18/20; 24 or 48 GB). Does not change any recommendation (the ~24 GB constraint is honored as stated), but the owner should confirm the actual part — especially 24 vs 48 GB — before Stage-2 threshold setting. |
| R-4 | **Hydra ambiguity in the spec** | `ctl_instruction.md` names the three-file Hydra stack both under the "Ignore Now and Come Back Later" heading **and** in the Implementation Notes (unmarked). B-9's keyed-single-YAML hedge is recommended regardless; the duplication is for the spec owners to reconcile (also r1b D-14). |
| R-5 | **Sheet's D3 set-labeling slip** | The sheet's §3.1 decomposition swaps which sets are gold (it lists 4,857 as `hierarchical_gold`; the spec's Table 1 assigns 2,749 to Set 2a hierarchical @ dt 0.01, 4,857 to Set 1b standard @ 0.17). Total 15,028 unchanged; the sheet's memory bracketing was conservative (overestimated the gold count). Cosmetic; noted so Stage-2 arithmetic uses the spec's table. |
| R-6 | **fp32 achievability of the §10.3 tolerance** | The spec's `relative_error < 1e-6` may be marginal for fp32 second derivatives on GPU (r1b C-6); the proposed dual-arm scheme (fp64-CPU reference; fp32-device within ~1e-4 of it) is a **tolerance ruling the owner must ratify** as part of the D1-p adjudication — not decided here. |
| R-7 | **Assumptions made** | (a) The four consolidated bundles faithfully contain the eight originals (asserted by their headers; content-consistent throughout). (b) The r1a sheet is the operative "prior suggested default"; the depth report is used for depth and its divergences adjudicated explicitly (D3, D4-a, D7-d). (c) `RESEARCH-CONTEXT-MASTER.md` (also present in the bundle) is superseded as instruction by the current prompt and used only as context. (d) Where the two r1b files differ in secondary numbers (e.g., segment counting 7–9), the ranges are carried, not resolved. |

**The frontier question** (single biggest open uncertainty, flagged for the owner): **does the fp32/MPS arm pass the §10 probes — especially 10.3 componentwise-AD and 10.4 force–energy — at a tolerance the owner ratifies, and what s/step does the smoke test measure?** Those two cheap measurements jointly decide the D1-p branch (owner-carved), the real duration envelope, the D3 auto verdict at later stages, and the value of every ⚖ threshold. Nothing else in this resolution moves as much on so little effort.

---

## 6. Standing restatement

This document is a **recommendation for the project owner to ratify — not a science-spec verdict**: it adjudicates build-design choices only, treats `ctl_instruction.md` and `pinn_architecture.md` as fixed constraints, leaves **D1-p (fp32 vs fp64)** to the owner's separate adjudication (every pick above holds under both branches), and treats **B-8** as settled by the spec (smaller ε_H passes).

---
---

## Appendix A — Phase 1: the multi-perspective scan (working record)

Six perspectives, each reasoning only from the attached files. Format: core position · strongest grounded evidence · the one thing no other perspective would flag.

**1. The Apple-Silicon ML practitioner.** *Core:* MPS is the only real GPU on this machine and its failure surface is op-gaps, fallback cliffs, and weak determinism — PyTorch is the least-surprising way to live with that; nothing gives you fp64 on this GPU, full stop. *Evidence:* `trainex-r1a-options-and-decisions.md` §0 F3–F8 (fp64 hard error; `PYTORCH_ENABLE_MPS_FALLBACK` semantics; `torch.mps` memory/RNG API; `weights_only` default; MPS nondeterminism issue + ~7× deterministic-flag slowdown); r1b §1.5 (double-backward per-op gap history; "the AD probe must run on the MPS device"). *Unique flag:* run the §10.3 probe with fallback **unset** so gaps fail loudly, and don't trust GPU-utilization bands — a 0.73 M-parameter dispatch-heavy workload can be healthy at low residency (r1b D-11); also `pin_memory` is a CUDA concept, leave it off, and `num_workers=0` deletes the most common beginner failure class.

**2. The PINN & numerical-methods researcher.** *Core:* the specs mandate the loop's shape — two-phase Adam→L-BFGS with complete Adam reset, five scheduled loss terms with re-warm, replay 240/16 with resolved edge cases, componentwise AD on the `u` leaf, hard COM projection before any loss — a skeleton that can't express these is off-spec regardless of how nice it is to operate. *Evidence:* `ctl_instruction.md` Phase 2a/2b, PHYS-05 semantics, LOOP-01/02/03, AC-LOOP-04; `pinn_architecture.md` PHYS-02 (forbidden sum-trick; acceptable patterns), §10 probes. *Unique flag — the spec-drift findings:* (i) Phase 33's ADVANCE/RECOVER/HALT-REVIEW machine postdates the sheet and makes bounded rollback-retry *spec-assigned loop behavior* (amends D4-c/D7); (ii) SI-PINN-003 is now RESOLVED (closes U-14); (iii) B-8 settled; (iv) LOOP-06 requires loader metadata exposure (amends D3); (v) Hydra appears in the un-marked Implementation Notes too (R-4); (vi) LOSS-02 mandates the B-2 instrumentation and defers auto-reweighting (vindicates the empty D5-I seam).

**3. The adversarial build reviewer.** *Core:* the suggested defaults mostly survive attack, with one clean kill: the sheet kept step-1000 cadence against its own companion evidence. *Evidence:* r1b §1.8 (83 min lost work at 5 s/step), DRO-6, depth report §7.4/7.9. *Other attacks and outcomes:* D1-A could die on a missing double-backward kernel (mitigated: probe-first + in-framework CPU branch); D3 in-memory could be wrong at later cumulative stages (mitigated: two-way selector + spec medians now bounding the corpus ≈ 0.55 GB fp32); B-5's field classification could misclassify (mitigated: default-to-identity fail-safe); D6's pilot repeats cost wall-clock (acceptable: the pilot is short by construction). *Unique flag:* the depth report's transactional D7 is over-build for a one-person slice — its crash semantics survive in the ordered-promotion + jsonl form at a fraction of the machinery; adopt the semantics, not the schema.

**4. The cost-&-effort economist.** *Core:* the binding budget is one non-expert's developer-hours and complexity, then wall-clock — memory is a measured non-issue at expected sizes (r1b §1.6: 2–7 GB total). The cheapest still-correct path is PyTorch + single keyed YAML + in-memory data + a plain closure loop with seams + JSONL/TB; the expensive traps are Hydra, MLflow, the checksum/branching journal, RAD machinery, and above all a hand-written sL-BFGS. *Evidence:* r1a menus' cost notes; r1b §1.6, K4. *Unique flag:* the κ (implementation-efficiency) spread ~15× is **larger than the device spread** (r1b §1.8) — and scalar-`u` forward-mode AD is the order-of-magnitude lever PHYS-02's "equivalent full-Jacobian" clause admits (r1b D-4): time both AD patterns in the probe before any long run.

**5. The operations-experience lens.** *Core:* PINN trainers fail *silently* — smooth curves over garbage physics — so the ladder (rungs 0–6) is the mechanical substitute for expert eyeballs, and the 5-minute smoke test is simultaneously the feasibility instrument (D-5/DRO-9). *Evidence:* r1b K5 ladder, K1 watchlist (five failure families incl. causal-weight collapse and propagation failure), K2 (lid/caffeinate/SIGTERM corrections D-10/DRO-2/3; environment pinning + golden-smoke re-validation), D-9 (two missing dashboard surfaces), D-11/D-12. *Unique flag:* the ⚖ audit — r1b **does not** number the loss-explosion, disk-floor, or memory-watermark thresholds, nor a post-promotion divergence trigger (R-1); and the hardware core counts in the project docs match no shipping M5 Pro (R-3).

**6. The non-expert operator / runbook advocate.** *Core:* fewest concepts, best-typed failures, one folder that is the whole record; every stop is a named `GUARD:`/`HALT:` line plus a zip-and-ask-for-help bundle. *Evidence:* baseline design §5 (five entry points, mental model, error table); r1b K3 (READ-DO vs DO-CONFIRM; verbatim-command-with-expected-output; flat symptom tables; "the run directory is the report"). *Unique flag:* D7-d's invariant — *resuming never re-asks what stage am I in* — is the single most operator-protective property in the whole sheet; and the watchlist's first row ("a boundary loss jump is scheduled and normal") must be in the runbook or the operator will panic at every promotion. Per-decision nulls declared: this perspective has nothing distinct to add on D5-b/D5-c internals (interfaces are invisible to the operator) beyond "log what the watchlist needs."

*(Coverage note: all 24 decide-set rows were touched by at least two perspectives; rows where a perspective had nothing distinct to add — e.g., the economist on B-11, the practitioner on B-3 — were left unpadded per the phase contract.)*

## Appendix B — Phase 2: contradiction & consistency map

**1. Per-decision conflicts.**
- **D3 residency:** depth report (streaming-first HDF5 + doctor benchmarks) vs sheet (auto→in-memory, workers=0) vs r1b (2–7 GB expectation, but parameterized on then-unknown S̄; stage-2 full-batch flag D-7). — Resolved for the sheet: the current spec's medians bound the corpus ≈ 0.55 GB fp32; the selector keeps streaming one config flip away; accumulate-in-closure answers D-7.
- **D4 cadence:** sheet (step-1000 kept) vs r1b §1.8/DRO-6 + depth report (wall-clock-aware). — Resolved against the sheet (override).
- **D4-c guard philosophy:** sheet ("auto-remediation = Tier-3, science-adjacent, operator's job") vs current spec CURR-03 (RECOVER is mandated loop behavior). — Resolved by the spec: seam now, retries=0 until the pilot.
- **D7 weight:** depth report (transactional journal, hashes, branch-on-rollback) vs sheet (ordered promotion + jsonl). — Resolved for the sheet's lighter form under the viability-slice lens; semantics preserved, disposition records added.
- **D5 shape:** depth report Option B (state machine) vs sheet D5-B (closure loop). — Substantively convergent; D5-B + the adopted seams ≡ the small state machine without the abstraction layer.
- **D6 shape:** depth report two-tier + 3 paired seeds vs sheet B+C + 2–3 pilot repeats. — Convergent; mapped onto each other.
- **B-9:** spec's Hydra mentions vs baseline single-YAML. — Keyed-YAML hedge; ambiguity registered (R-4).

**2. Strongest vs weakest grounding.** Strongest on the contradicted rows: the operations lens (r1b) on D4-a (an arithmetic consequence of an unknown t_step) and the researcher on D4-c (verbatim spec text). Weakest: the depth report's D3 streaming-first — its "the dataset is not the only large object" concern is real but generic, while the sheet+spec side now has numbers (medians) and the r1b memory decomposition; and its D7 transactional schema, which is grounded in sound engineering but not in any attached constraint that demands that weight for a single-user slice.

**3. The resolving question per biggest contradiction.** D3: *what are the per-stage cumulative bytes?* — **empirical**, supplied by the Thrust-A scan (the medians already answer the corpus-level question). D4-a: *what is t_step?* — **empirical** (smoke test); the ceiling value is then an **owner** pick. D4-c: *what retry budget / HALT thresholds?* — **empirical via the Stage-0 pilot, then owner-ratified** (the spec says exactly this).

**4. Unanimous agreements (the robust picks).** D1-A PyTorch; JSONL-canonical; probe-first with fallback disabled; atomic writes + `weights_only` contents; the five-term log widening; spec optimizer schedule as first default; dual stage anchors + complete Adam reset; `caffeinate -is` + lid-open; re-scoped reproducibility promise; single-folder record with environment fingerprint. These carry High confidence with least owner attention needed.

**5. Blind spots, drift, and ⚖ audit.** No in-scope decision was left ungrounded by all six perspectives; the items *no perspective could ground in the sources* are exactly the register's open numbers: the validation cadence (U-5), the ⚖ thresholds r1b never numbers (R-1), sL-BFGS's algorithm (U-7), and per-stage byte counts (U-1 residual). Spec-drift list (options/claims the current specs now contradict or amend): the sheet's Tier-3 framing of rollback-retry (CURR-03); the sheet's open U-3/U-14 (now closed); the sheet's "S̄ unknown" (medians now in-spec); the sheet's D3 set labels (R-5); the baseline's `caffeinate -d`, lid-close optimism, 3-term log line, "CUDA out of memory" row, blunt resume rule, and bitwise-reproduce promise (all already targeted by B-rows). The most valuable cross-cutting finding: **the two cheapest actions in the whole program — the Thrust-A data scan and the 5-minute smoke test — collapse more registered uncertainty (U-1, U-2/15, D3 auto, D4-a ceiling, the seed band) than any decision on this sheet.**

## Appendix C — Phase 4: peer review (self-critique)

**1. Confidence audit.** The High ratings on D1, D2, D4-b/d, D5-a/b/c, D6-policy, D7-a/b/d, B-1/2/6/10/11 rest on unanimous-perspective agreement plus verbatim spec or verified-capability grounding — honest. Rows deliberately held at Medium and **marked for the owner's closer look:** D4-c (spec thresholds self-declared provisional; ⚖ unfilled), D7-c (no divergence signal exists), B-5 (classification judgment; mitigated by fail-safe), B-9 (R-4 ambiguity), B-3 (taste), and D3's auto-lands-in-RAM sub-claim (median-based, not guaranteed per-stage). Independent agents would plausibly diverge on D7's weight class and B-9 — both flagged.

**2. Weakest link.** The **D4-c RECOVER instantiation**: it rests on reading CURR-03's provisional state machine as binding *structure* with non-binding *values*. If the owner reads RECOVER as itself deferred, the amendment reduces gracefully to the sheet's Tier-1 (the retries=0 default makes the two behaviorally identical today) — the cost of being wrong is one config key. What would settle it: an owner ruling on CURR-03's standing for the slice, plus the Stage-0 pilot's calibration run. (Per the mandate, D1-p and B-8 are not candidates here.)

**3. Bias check.** The operator/economist lenses dominated the D7 and B-9 weight calls — deliberately, because the strategy assessment's viability-slice lens licenses exactly that bias, and the one-way doors those lenses might have endangered (anchor names, jsonl, seed schema, closure shape, adapter interface) were all kept. Conversely, the researcher's spec-purism was allowed to override the operator's simplicity exactly once (the RECOVER/HALT seams), which is the right direction of deference. No row was found where simplicity overrode a flagged one-way door.

**4. Missing angle.** Considered a seventh perspective — **the data-pipeline owner (v1.5/PIPE-XX)** — since three joins land on them (data_version hash, admission-gate manifests, split policy U-4). Re-running the affected rows (D3, B-5 identity fields, B-6 data-manifest) through that lens changed no conclusion: every touchpoint is already behind the adapter seam or registered as their lane. Not added.

**5. Overall honesty grade.** Decisive (one recommendation per row), coherent (the closure-seam consistency thread holds across D4/D5/D7; the recipe composes without a second mechanism), and free of invented numbers — every quantity is either cited, derived arithmetic from cited spec values (flagged as such), or an explicit placeholder. Residual weaknesses a rigorous reviewer would name: the CURR-03 reading (mitigated as above), the derived 0.55 GB figure's reliance on medians (caveated), and the fact that four Medium rows push real decisions to the owner — which is by design, since they are genuinely owner/empirical in nature. Fixes from this review were applied before finalizing (the fail-safe on B-5, the RECOVER/D7-D distinction, and the ⚖ audit's explicit "no number in r1b" list). Register and standing restatement finalized above.

*— End of resolution.*
