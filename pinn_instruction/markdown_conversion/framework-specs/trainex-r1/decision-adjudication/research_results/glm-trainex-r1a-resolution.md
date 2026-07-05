# Trainex R1a — Decision-Adjudication Resolution (CTL-PINN Training Execution)

**Standing:** Recommendation for the project owner to ratify. This is a build-design round, not a science-spec adjudication; the science specs (`ctl_instruction.md`, `pinn_architecture.md`) are locked constraints.
**Scope decided:** D1, D2, D3, D4-a/b/c/d, D5-a/b/c, D6, D7-a/b/c/d, and baseline items B-1, B-2, B-3, B-4, B-5, B-6, B-9, B-10, B-11.
**Out of scope (transparency):** D1-p (precision branch — owner-carved, another channel); B-8 (ε_H gate direction — spec-settled by `ctl_instruction.md` lines 559–565: REJECT if `eps_H > 1e-5`, smaller passes); B-7 (cosmetic doc edit); B-12 (split-policy tension routed to v1.5/PH-5).
**Lens:** Every decision is tagged **Needed-now** (required for the Stage-0 viability slice, or a one-way door that must be right from the start) or **Deferrable** (safely postponed until the slice proves the approach), per `postspec-r1-direction-assessment.md`.
**Method:** STORM four-phase (multi-perspective scan → contradiction map → synthesis → peer review), with every claim grounded in the 8 attached sources. Working records for Phases 1, 2, 4 are in the appendices.

---

## Decision rows

### D1 — ML framework (the spine)

**Recommendation:** **D1-A — PyTorch 2.12 + MPS backend.** Endorse the suggested default.

**Endorse or override:** Endorse. PyTorch is the only candidate that simultaneously (a) runs on the GPU you bought, (b) ships the L-BFGS the science spec mandates (`ctl_instruction.md` Phase 2b), (c) matches the spec's own illustrative AD code (`pinn_architecture.md` §5.3.1 PHYS-02 listing uses `torch.func.jacrev` + `vmap`), and (d) maximizes searchable help for a non-expert. MLX is structurally blocked by **no L-BFGS** (F11 — `mlx.optimizers` ships SGD/Adam/AdamW/etc. but no L-BFGS); the spec's two-phase regime would require a non-expert to hand-implement L-BFGS with Wolfe line search and a stochastic variant — exactly the numerical-optimizer code they should not own. JAX is CPU-only on this machine because `jax-metal` is effectively unmaintained (F12, r1b DRO-1) and the community `jax-mps` replacement is alpha; the highest-friction maintainer-skill cost.

**Confidence:** **High.** Biggest uncertainty: whether every kernel in this net's double-backward graph has an MPS implementation (register U-9) — must be proven on-device by running the spec's §10.3 componentwise-AD probe with `PYTORCH_ENABLE_MPS_FALLBACK` *unset* before any long run. Also note the MPS-specific `torch.func.jacfwd` `as_strided` bug on `torch.cat`/`torch.stack` (pytorch#152701, fixed in 2.7.1+); pin PyTorch ≥ 2.7.1 (current stable 2.12.x per F1) and prefer a `jacrev`-based second-order path.

**Holds under both D1-p branches:**
- *Branch (i) fp32 residuals suffice:* `device="mps"`, float32 end-to-end in the training loop, with the fp64 islands the spec already requires (preprocessing/invariants, one-time `S_H` constant) kept on CPU.
- *Branch (ii) fp64 required for residuals:* the 15 GPU cores are off the table on every candidate — this is hardware (F3, F10, F12), not a framework choice. Use the same PyTorch codebase with `device="cpu"`, `torch.set_default_dtype(torch.float64)`; one framework, one runbook, one checkpoint format; cost is slower steps (R1b duration question, not estimated here).

**Consistency:** Determinates D2 (TensorBoard first-party), D3 (MPS allocator + `num_workers=0` simplification), D5 (native `torch.optim.LBFGS(line_search_fn="strong_wolfe")` available in-box), D6 (`torch.mps.manual_seed` + `get_rng_state`/`set_rng_state` per F5).

**Timing:** **Needed-now.** One-way door — every other decision, the runbook, and all run artifacts inherit the framework; reversing later is a rewrite.

**Nature:** Research-settled, with one empirical gate (U-9 — the §10.3 AD probe).

---

### D2 — Experiment tracking and the monitoring surface

**Recommendation:** **D2-A — TensorBoard as the secondary view, with the committed JSONL log as the canonical record, plus D2-B's one plotting script for end-of-run PNGs.** Endorse the suggested default.

**Endorse or override:** Endorse. The JSONL-canonical rule (decision sheet's framing) is the load-bearing design point: if `runs/<name>/logs/train.log.jsonl` remains the source of truth and any dashboard is only a *view* of it, the tracker choice becomes a cheap two-way experiment. TensorBoard is first-party for PyTorch (D1-A), matches the spec's own implementation note (`ctl_instruction.md` Implementation Notes line 2005), and has the lowest learning curve (one command, one URL). D2-D (W&B offline) is disqualified: offline mode is *capture only* — viewing the dashboard requires `wandb sync` to W&B's servers (F14), which contradicts the no-cloud hard constraint. D2-C (MLflow local) is heavier than a single-user project needs and its 3.x release energy is aimed at LLM observability (F15).

**Confidence:** **High.** Biggest uncertainty: whether TB event files become awkward to re-parse if relied on as primary record. Mitigated by homing `tb/` inside `runs/<name>/` (B-6) and keeping JSONL canonical.

**Consistency:** Depends on D1-A (first-party `torch.utils.tensorboard.SummaryWriter`). The "one plotting script" inherits from D2-B for end-of-run PNGs in `summary.md` — useful when TB is not running.

**Timing:** **Needed-now** for JSONL-canonical (it is the watchlist's data source per r1b K1). TensorBoard secondary view is **deferrable but free** — adopt from day 1.

**Nature:** Research-settled.

---

### D3 — Compute utilization on 24 GB unified memory (in-memory vs streaming)

**Recommendation:** **D3-C — auto-selector with `auto` defaulting to in-memory fp32 preload (D3-A behavior at expected sizes), `num_workers=0`, watermark 0.7, and the memory log line.** Endorse the suggested default.

**Endorse or override:** Endorse, but reconcile an internal contradiction (see SD-3 below). The chatgpt-pro-resolution's §6.7 recommended D3 "Option C — chunked HDF5 streaming with bounded stage-local cache" tagged **one-way door**; the decision sheet's D3-C auto→in-memory is tagged **two-way door** for residency. The sheet's framing is the more honest one given U-1 (snapshots-per-trajectory unknown): r1b §1.6 finds total expected training memory **2–7 GB, comfortably inside 24 GB** for the typical case, so in-memory preload is the simplest path for the Stage-0 slice; but r1b D-7 also flags that **full-batch L-BFGS at stage 2** (single full-batch second-derivative graph over millions of points) exceeds 24 GB without accumulation. The adapter interface must support both modes from day 1.

**Reconciliation (SD-3):** The **adapter interface** ("batches by index, fixed shapes") is one-way — downstream loop code assumes it. The **residency policy** (ram/mmap/auto) is two-way — a config flip. Adopt the sheet's nuanced door split, not the chatgpt-pro-resolution's stricter one-way framing.

**Confidence:** **Medium.** Biggest uncertainty: U-1 — once `S̄` (snapshots/trajectory) is known, the in-memory threshold (~6–8 GB fp32 per the sheet, traceable to r1b's 2–7 GB figure) may need to flip to mmap at stage 2 even for the thin slice's later probing. The one-way adapter interface protects against this.

**Consistency:** Depends on D1-A (MPS allocator with `torch.mps.set_per_process_memory_fraction(0.7)` per F5, `current_allocated_memory`/`recommended_max_memory` per F5). Memory-pressure log line `mem: X/16.8 GB (mps)` per 1,000 steps feeds r1b K1 watchlist.

**Timing:** **Needed-now** for the adapter interface (one-way); the auto/mmap flip is **deferrable**.

**Nature:** Research-settled for the interface; **empirical** for the threshold (U-1 measurement needed).

---

### D4-a — Checkpoint cadence & retention

**Recommendation:** **D4-B — rolling window (K=3) + best + stage anchors + `latest.pt` as copy.** Endorse the suggested default, with one adjustment: add a wall-clock fallback cadence (~15–30 min) **conditional on the smoke-test measurement** showing `t_step ≥ ~1 s`.

**Endorse or override:** Endorse with the conditional addition. r1b §1.8 shows the design's default `checkpoint_every = 1000` means 100 s of lost work at `t_step = 0.1 s` but **83 minutes** at 5 s/step — the design's step-only cadence is unsafe across r1b's full feasibility envelope. For the Stage-0 slice's first run, step-based at 1000 is fine (the smoke test measures `t_step` before any long run); add wall-clock if the smoke test lands in r1b's amber band. Disk math trivial: ~9 MB/checkpoint × (3 rolling + best + ≤7 stage anchors + latest) ≈ 110 MB per run.

**Confidence:** **High.** Biggest uncertainty: whether to ship wall-clock cadence from day 1 or after the smoke test. Recommendation: ship step-based + stage-event checkpoints from day 1; add wall-clock only if smoke-test shows `t_step ≥ 1 s`.

**Consistency:** Pairs with D7-A's stage anchors (excluded from rolling deletion). The atomic-write protocol of D4-b makes the `latest.pt` copy meaningful.

**Timing:** **Needed-now** (cadence + retention shape); wall-clock fallback is conditional on the smoke-test measurement.

**Nature:** Research-settled, with one empirical input (`t_step` from r1b K5 rung 6).

---

### D4-b — Corruption safety

**Recommendation:** **Adopt atomic writes (`*.pt.tmp` → `flush` + `fsync` → `os.rename`) + fallback scan + the `weights_only` rule.** Endorse the suggested default.

**Endorse or override:** Endorse. Free; required to make D7-A's stage anchors trustworthy; protects against mid-write power loss (costs at most one cadence interval). The `weights_only` rule (F8): store only `state_dict()`s, tensors, ints/floats/strings — never optimizer *objects*, never raw NumPy RNG tuples (convert to tensors/bytes). Then `torch.load(path)` works under the 2.6+ default with no `add_safe_globals` incantations in the runbook.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Required by D7-A's boundary anchors and D4-c's emergency-checkpoint guard.

**Timing:** **Needed-now** (free; adopt from day 1).

**Nature:** Research-settled.

---

### D4-c — Auto-guard tier

**Recommendation:** **Tier 1 + Tier 2 on by default; Tier 3 deferred post-R1b.** Endorse the suggested default, with one spec-alignment caveat (SD-2 below).

**Endorse or override:** Endorse with the caveat. Tier 1 (NaN/Inf auto-stop, loss-explosion kill, disk-floor) is the unattended-run minimum. Tier 2 (memory-watermark, heartbeat) catches leak-shaped growth before macOS swaps. Tier 3 (auto-LR-cut, auto-rollback-and-retry) needs R1b's signal definitions first.

**Spec-drift finding (SD-2):** The current spec's Phase 33 CURR-03 (`ctl_instruction.md` lines 1915–1988) defines a 3-state curriculum machine: **ADVANCE / RECOVER / HALT-REVIEW**. RECOVER = automatic rollback-and-retry on NaN/Inf with bounded retry budget. The decision sheet's D4 Tier 1 NaN guard (stop-and-preserve) does not account for RECOVER. **Reconciliation:** RECOVER is the loop-internal, spec-mandated mechanism (always-on, even for the Stage-0 slice); the D4 Tier 1 NaN guard is the *fallback* when RECOVER's retry budget is exhausted → HALT/REVIEW, or when NaN happens outside RECOVER's scope (e.g., during L-BFGS line search). The D4 Tier 3 "auto-rollback-and-retry" is therefore partially superseded by the spec's RECOVER for the NaN/Inf case; remaining Tier 3 (auto-LR-cut on loss explosion) is still deferred. **Owner/spec-author confirmation needed** on the exact RECOVER↔Tier-1-guard boundary.

**Confidence:** **Medium.** Biggest uncertainty: the exact boundary between spec's RECOVER and D4 Tier 1 guard — needs spec-author clarification. The ⚖ thresholds themselves (loss-explosion multiple, disk-floor GB, memory-watermark ratio, consecutive-logs count) are not given numbers in r1b — leave as Stage-2 placeholders per §3.

**Consistency:** Consumes the same closure/seam structure as D5-B. The guard hook points inside the loop (post-loss check, pre-checkpoint check, heartbeat write) are mildly one-way — build the skeleton with these three seams now even if some guards start disabled.

**Timing:** **Needed-now** for the three guard seams (one-way, retrofittable only with rework); Tier 1+2 toggles on by default; Tier 3 deferred.

**Nature:** Research-settled for tier structure; spec-alignment needs owner call; ⚖ thresholds are Stage-2 empirical.

---

### D4-d — Failure diagnostic bundle

**Recommendation:** **Always on.** Endorse the suggested default.

**Endorse or override:** Endorse. Additive files (`runs/<name>/failure/` containing `traceback.txt`, `env.txt`, `config-frozen.yaml` + SHA-256, `log-tail.txt`, `state.json`, `memory.txt`, dataset hash pointer); nothing else depends on them. The runbook step becomes literally *"zip `runs/<name>/failure/` and ask for help"* — exactly the operator pattern r1b K3 §5.2 endorses (SRE playbook evidence: pre-written responses beat improvisation ≈3× MTTR improvement).

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D4-c's guard stop message `GUARD: <reason> — run stopped`.

**Timing:** **Needed-now** (free; additive).

**Nature:** Research-settled.

---

### D5-a — Loop shape

**Recommendation:** **D5-B — two-phase, closure-shaped, accumulate-in-closure.** Endorse the suggested default.

**Endorse or override:** Endorse. The spec mandates two-phase Adam→L-BFGS per stage (`ctl_instruction.md` Phase 2 / 2b). D5-A (single-phase Adam only) **cannot express the spec's Phase 2b** — the sheet's own conflict warning; choosing it is a conscious descoping against the locked spec, defensible only as a sequencing choice, with retrofit cost when Phase 2b arrives. The closure-based loop is required because PyTorch's `torch.optim.LBFGS` calls the closure multiple times per `step()` for the line search. **Accumulate-in-closure is the structural answer to the 24 GB wall** (r1b D-7): a single full-dataset second-order graph would not fit; accumulation keeps peak memory at one-batch scale at the cost of closure wall-time.

**Confidence:** **High.** Biggest uncertainty: wall-time of accumulate-in-closure full-batch L-BFGS — r1b flags this as a duration question (R1b dependency, not estimated).

**Consistency:** The closure is exactly the seam D4's guards (post-loss check) and D7's boundary logic want. D5-C (pluggable phases) is over-abstraction for the first build; the pluggability needed for sL-BFGS is delivered by D5-B's phase-flag structure (Adam phase / L-BFGS phase / future sL-BFGS phase).

**Timing:** **Needed-now** (one-way door; it IS the skeleton; R2 tunes inside it).

**Nature:** Research-settled.

---

### D5-b — Collocation infrastructure

**Recommendation:** **D5-E — sampler interface with `uniform` + spec's acceleration-weighted `adaptive` behind a config key, including the stateful-hook signature.** Endorse the suggested default.

**Endorse or override:** Endorse. The spec already requires structurally: per-step sampling of `n_col` points in `u∈[0,1]` with at least two strategies (uniform and acceleration-weighted adaptive) plus the data-batch side's 50% uniform / 50% acceleration-weighted time-point sampling and replay/lookahead composition (`ctl_instruction.md` Mini-Batch Construction). D5-D (fixed uniform hard-coded) under-builds relative to the spec. D5-F (residual-pool now) is beyond spec; the stateful-hook signature (sampler may receive `(model, last_residuals)`) costs nothing today and is the one-way part — the pool machinery itself is bolt-on later.

**Confidence:** **High.** No real uncertainty.

**Consistency:** The interface signature is one-way (callable contract the loop is written against); strategies and densities inside it are two-way config.

**Timing:** **Needed-now** for the interface signature (one-way); strategy selections and numeric densities are **deferrable** (R2 territory).

**Nature:** Research-settled for the interface; **empirical** for densities (R2).

---

### D5-c — Loss-weight machinery

**Recommendation:** **D5-H — scheduled-weights module (`WeightSchedule`: inputs (stage k, phase, step-in-phase) → λ vector; logs all λ values every `log_freq`; serialized into checkpoints) + empty I-seam for adaptive rebalancing.** Endorse the suggested default.

**Endorse or override:** Endorse. The spec's PHYS-05 schedule is **not static**: `λ_phys`, `λ_E`, `λ_L` warm up linearly over `I_warm = min(2000, 0.1·N_Adam,k)` steps, with per-stage `λ^max` tables, frozen during L-BFGS, re-warmed at every stage boundary, plus per-batch causal weights with stopgrad and an underflow clip (`ctl_instruction.md` Phase 35 / `pinn_architecture.md` §4.1 PHYS-05). D5-G (static weights) **does not satisfy the spec** — the sheet's own finding. D5-I (adaptive rebalancing) is beyond spec; the empty seam (no-op callable site after backward) is nearly free.

**Confidence:** **High.** No real uncertainty. (Note: the causal-weight underflow clip bound is U-6 — spec explicitly declines to choose; surface at implementation with a logged rationale.)

**Consistency:** Loop + checkpoints + logs depend on the weight-module interface (one-way); values inside are two-way.

**Timing:** **Needed-now** for the module interface (one-way); values are **deferrable** (R2).

**Nature:** Research-settled for the interface; clip bound is **empirical** (U-6).

---

### D6 — Reproducibility and determinism policy

**Recommendation:** **D6-B + C — accepted-variance with a defined seed policy, plus a strict-mode debug switch.** Endorse the suggested default.

**Endorse or override:** Endorse. PyTorch's official position (F6): bitwise reproducibility is **not guaranteed** across releases, commits, platforms, or CPU↔GPU. On **MPS specifically**, an open issue (F7, #97236) documents non-identical training results *despite* full seeding and `torch.use_deterministic_algorithms(True)`, while the identical script is bit-reproducible on CPU; the deterministic-algorithms flag carries a measured ~7× slowdown on MPS (F7, #122394). D6-A (strict always) pays the price without securing the property — honest only as CPU-mode. D6-B+C: every run sets and records the full seed set (Python `random`, NumPy, `torch.manual_seed`, `torch.mps.manual_seed` per F5, config `seed:` field echoed into `status.json` and checkpoints, RNG states checkpointed for exact-resume continuity); no deterministic-algorithms flag; the policy *names* the residual (two same-seed MPS runs may differ slightly). The comparison protocol: judge runs on validation metrics at fixed checkpoints, and treat differences smaller than the seed-to-seed band as noise — establish the band once by running the Stage-0 pilot 2–3× with different seeds. D6-C adds a `determinism: strict` config that flips to CPU device + deterministic algorithms + `warn_only=True` for bisecting weird behavior on a small problem.

This re-scopes §5.7's "give a colleague the `runs/` folder ⇒ reproduce" to what the platform supports: *re-run to statistically equivalent results from the recorded config+seed; exact-continuation from any checkpoint; not bitwise re-creation of a from-scratch run* (F6/F7). See B-11.

**Confidence:** **High.** Biggest uncertainty: the seed-band calibration protocol needs the 2–3 pilot repeats — cheap, but adds a step to the runbook.

**Consistency:** The seed-and-RNG block inside the checkpoint/config schema is one-way-ish (part of the artifact contract every later run compares against) — include from run #1. Pairs with D4-b's `weights_only` rule (NumPy RNG state stored as tensors/bytes).

**Timing:** **Needed-now** for the seed/RNG schema (one-way-ish); strict-mode debug switch is **deferrable but cheap** — include from day 1.

**Nature:** Research-settled.

---

### D7-a — Boundary checkpoints

**Recommendation:** **D7-A — dual anchors (`stage-{k}-final.pt` + `stage-{k+1}-init.pt`), both excluded from D4's rolling deletion.** Endorse the suggested default.

**Endorse or override:** Endorse. The spec says "Save model checkpoints after each stage completion" (`ctl_instruction.md` Implementation Notes line 2009) — D7-A makes that checkpoint *distinguishable* and adds the post-init twin so a boundary crash is unambiguous. D7-B (single cadence checkpoint at the boundary) is indistinguishable in archaeology and gives no clean rollback target. For the thin Stage-0 slice: stage 0 alone may not promote during the viability probe, but the anchor mechanics must be right from day 1 because they are one-way (artifact contract; runbook and resume logic depend on them).

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D4-b's atomic writes and D7-d's `curriculum.jsonl`.

**Timing:** **Needed-now** (one-way artifact contract).

**Nature:** Research-settled.

---

### D7-b — Optimizer state at boundary

**Recommendation:** **Spec-mandated full reset (construct a new `torch.optim.Adam(...)` at stage start; state starts empty; nothing to "clear").** Endorse — this is not a real choice.

**Endorse or override:** Endorse (not a real choice — spec mandates). The spec says "**Critical**: Completely reset Adam's internal state (momentum buffers)…" (`ctl_instruction.md` line 1791). L-BFGS state never crosses a boundary (each stage's Phase 2b builds its own history). The "partial-carry experiment flag" is offered as a later two-way addition but is a scientific deviation; not for first build.

**Confidence:** **High.** Not a real choice.

**Consistency:** Mechanics verified per candidate (PyTorch = new `Adam`; MLX = new `optim.Adam`; JAX/Optax = re-`init` pytree).

**Timing:** **Needed-now** (spec mandate).

**Nature:** Spec-settled.

---

### D7-c — Rollback policy

**Recommendation:** **D7-C — manual, one documented command (`python -m pinn.train --config <same.yaml> --resume runs/<name>/checkpoints/stage-{k}-final.pt --hold-stage`) now; D7-D (auto-revert guard) deferred post-R1b.** Endorse the suggested default, with one spec-alignment caveat.

**Endorse or override:** Endorse with the caveat. The `--hold-stage` flag is essential: without it, promotion criteria would immediately re-fire since they were just met. D7-D needs R1b's divergence-after-transition signal, which r1b does **not** specify (no ⚖ number given — leave as Stage-2 placeholder).

**Spec-alignment caveat (SD-2):** The spec's RECOVER state (Phase 33 CURR-03, lines 1969–1976) is automatic rollback-and-retry for transient NaN/Inf with bounded retry budget — distinct from D7-D's "auto-revert guard on post-promotion divergence signal." RECOVER is spec-mandated and should be implemented from day 1 (it is the loop-internal mechanism that fires *before* D4 Tier 1's NaN guard); D7-D (the broader auto-revert guard) is deferred. **Owner/spec-author confirmation needed** on RECOVER↔D7-D boundary.

**Confidence:** **Medium.** Biggest uncertainty: the boundary between spec's RECOVER (always-on, NaN/Inf only) and D7-D (broader divergence signal, deferred) — needs spec-author confirmation. The ⚖ thresholds are not given numbers in r1b — Stage-2 placeholder.

**Consistency:** D7-C's manual command consumes D7-A's `stage-{k}-final.pt` anchor and D7-d's `curriculum.jsonl`. D7-D would consume D4's guard seams.

**Timing:** **Needed-now** for manual rollback command + spec's RECOVER; D7-D **deferrable**.

**Nature:** Research-settled for manual; spec-mandated for RECOVER; D7-D needs **empirical** signal (R1b ⚖ undefined).

---

### D7-d — Mid-promotion crash handling

**Recommendation:** **Idempotent, ordered promotion + `curriculum.jsonl` journal.** Endorse the suggested default.

**Endorse or override:** Endorse. Make promotion idempotent and ordered: (1) write `stage-{k}-final.pt` (atomic, D4-b); (2) append a promotion record to `runs/<name>/curriculum.jsonl` (`{from:k, to:k+1, step, criteria_snapshot}`); (3) construct new optimizer + schedule; (4) write `stage-{k+1}-init.pt`. On resume, the loop trusts the *checkpoint's* stage/phase fields and reconciles against `curriculum.jsonl`: a final-anchor without its init-twin ⇒ the crash hit mid-promotion ⇒ redo (3)–(4) deterministically. User-visible invariant: **resuming never re-asks "what stage am I in?" — the checkpoint knows.**

**Confidence:** **High.** No real uncertainty.

**Consistency:** Extends D4's resume invariants (additive); gives the runbook's curriculum-progression summary its data source. Pairs with D7-A's anchors.

**Timing:** **Needed-now** (one-way artifact contract).

**Nature:** Research-settled.

---

### B-1 — PH-7 first-trial optimizer default

**Recommendation:** **Replace baseline PH-7 (Adam, LR 1e-3, exp decay 0.95/500) with the spec's stage-0 schedule (per-stage `1e-3 × 0.7^k`, cosine annealing, two-phase Adam→L-BFGS, adaptive median clipping).** Endorse the suggested default.

**Endorse or override:** Endorse. Baseline PH-7's PhysicsNeMo-derived default would have the first run **silently off-spec**. The specs own the science; PH-7's default as written is a descoping, not a research-settled default. The only genuine cross-document conflict found in the sheet's pairwise check is B-1 vs baseline PH-7.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D5-a (the loop shape that expresses this schedule). The table in `ctl_instruction.md` "Consolidated Hyperparameter Schedule" (lines 1992–1996) is the source of truth.

**Timing:** **Needed-now** (else first run is off-spec).

**Nature:** Research-settled (spec mandate).

---

### B-2 — Committed log fields

**Recommendation:** **Widen the committed log-line fields from 3 terms (data/physics/IC) to the spec's 5 terms (data, IC, phys-causal, E, L) + total + current λ vector + grad-norm.** Endorse the suggested default.

**Endorse or override:** Endorse. The spec's named monitoring set is 5 terms + scheduled λ values + gradient-norm/clip events + conservation metrics (`ctl_instruction.md` Implementation Notes lines 2005–2007). The energy and angular-momentum drift terms are exactly the silent-failure detectors r1b K1 §3.2 relies on — they MUST be visible in the live log and dashboard. r1b DRO-5 / D-9 explicitly recommend this widening, plus a per-time-bin physics-residual panel and causal-weight statistics (min/mean `w_n`, fraction > 0.5) — the latter two are cheap dashboard additions for Stage-0 instrumentation.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Additive JSONL/log keys (consumers tolerate new keys). Pairs with D2's JSONL-canonical rule.

**Timing:** **Needed-now** (needed for r1b K1 watchlist from the first run).

**Nature:** Research-settled.

---

### B-3 — Name controller components (CurriculumController / RunController)

**Recommendation:** **Name `CurriculumController` (owns stage/phase, `curriculum.jsonl`, D7 promotion procedure) and `RunController` (owns guards, `status.json`, Ctrl-C/bundle handling of D4) as explicit components within Subsystem 3.** Endorse the suggested default.

**Endorse or override:** Endorse. The three-subsystem + verification split is sound and kept; this is structure-naming, not re-architecture. Gives the runbook nouns for "what stopped my run" — the operator can say "the RunController's NaN guard fired" or "the CurriculumController's RECOVER retry budget exhausted" rather than "training stopped."

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D4 (RunController) and D7 (CurriculumController).

**Timing:** **Needed-now** (free; adopt before runbook is written, but trivially two-way).

**Nature:** Research-settled (internal structure naming).

---

### B-4 — Extend placeholder inventory (PH-1..10)

**Recommendation:** **Extend the inventory per §8 B-4.** Endorse the suggested default.

**Endorse or override:** Endorse. The baseline's PH-1..PH-10 list omits early-settling execution decisions now exposed by D1–D7: precision policy (D1-p), reproducibility/determinism (D6), checkpoint cadence/retention/corruption (D4), unattended auto-guards (D4), stage-boundary mechanics (D7), collocation *infrastructure* distinct from PH-6's *strategy* (D5.2), **sL-BFGS implementation ownership** (D5.1 — custom in every framework; no PH covers who builds it), **validation-evaluation cadence** (U-5), config schema versioning (B-5).

**Confidence:** **High.** No real uncertainty.

**Consistency:** Documentation housekeeping; pairs with B-1 (retiring PH-2/PH-3/PH-4 as "open trainex decisions" since the specs own them).

**Timing:** **Deferrable** (documentation) but free.

**Nature:** Research-settled.

---

### B-5 — Resume config-diff rule

**Recommendation:** **Field-classified diff — identity fields (architecture, data version, split seed, curriculum definition, loss/schedule contracts) refuse resume; operational fields (`max_steps`, `log_freq`, guard toggles, tracker settings) resume with a logged `CONFIG CHANGE:` line.** Endorse the suggested default.

**Endorse or override:** Endorse. Baseline "different config ⇒ hard error" is too blunt — fixing a typo in a comment or extending `max_steps` bricks resume. The frozen `config.yaml` copy plus the diff log preserves provenance.

**Confidence:** **High.** Biggest uncertainty: the exact field classification list — owner should ratify before first real run.

**Consistency:** The field classification becomes part of the config schema people rely on; pairs with B-9 (single-YAML keyed structure).

**Timing:** **Needed-now** (one-way soft; settle before run #1).

**Nature:** Research-settled with **owner-ratification** of the field list.

---

### B-6 — `runs/<name>/` additive member list

**Recommendation:** **Adopt the additive member list: `tb/`, `checkpoints/stage-*-{final,init}.pt`, `curriculum.jsonl`, `failure/` bundle, seed record in `status.json`, `data-manifest.json`.** Endorse the suggested default, plus r1b D-12's environment fingerprint addition.

**Endorse or override:** Endorse with the r1b D-12 addition. Adding is free now; *removing or renaming* members later breaks the runbook. r1b D-12 additionally recommends including the environment fingerprint (`sw_vers`, `python -V`, framework version/build, lockfile hash) in `runs/<name>/` for the "give a colleague the folder" promise to hold and to make K2's upgrade re-validation diffable.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D2 (TB events inside `runs/<name>/tb/`), D4-d (`failure/` bundle), D6 (seed record in `status.json`), D7 (stage anchors + `curriculum.jsonl`).

**Timing:** **Needed-now** (one-way soft; adopt before runbook).

**Nature:** Research-settled.

---

### B-9 — Config approach (single YAML vs Hydra three-file stack)

**Recommendation:** **Keep baseline single-YAML-per-run + frozen copy, but structure its top-level keys as `stage:`, `opt:`, `loss:`, `run:` — capturing the spec's separation inside one file and making a later Hydra migration mechanical.** Endorse the suggested default.

**Endorse or override:** Endorse. `ctl_instruction.md` names a Hydra `stage/opt/loss.yaml` stack under a heading the spec itself marks "**Ignore Now** and Come Back Later" — treated as deferred guidance, not a binding science contract (decision sheet's correct reading). Baseline single-YAML + frozen copy = one file to read, no new tool, perfect fit for the operator profile. Hydra = composition/overrides/sweeps power the project doesn't yet need, plus a dependency and concept set. The key-structure hedge preserves a later Hydra migration path.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with B-5 (field classification lives in this schema). The frozen `config.yaml` is part of the run-folder contract (B-6).

**Timing:** **Needed-now** (key structure is the hedge; settle before first real run).

**Nature:** Research-settled.

---

### B-10 — Sleep-prevention wrapper

**Recommendation:** **`caffeinate -is python -m pinn.train …` (not `-d`).** Endorse the suggested default.

**Endorse or override:** Endorse. r1b K2 §4.1 (findings-1) and K2.1 (findings-2) both confirm: `-d` prevents *display* sleep (unnecessary for a terminal run, wastes power); `-i` (idle system sleep) + `-s` (system sleep on AC power) is the right pair; the assertion ends automatically when training exits. r1b DRO-2 also corrects baseline §5.4's "lid close → training continues when lid reopens" — on Apple Silicon + macOS 15+, closing the lid forces hardware-level sleep that **neither `caffeinate` nor `sudo pmset -a disablesleep 1` can override**; only clamshell mode (external display + power + keyboard/mouse) or lid-open works. Final lid/sleep/thermal doctrine is R1b's lane — but the launch-command shape is R1a surface, and `-is` is unambiguously better than `-d`.

**Confidence:** **High.** No real uncertainty on the flag; final ops doctrine (lid, thermal, High Power Mode) is R1b.

**Consistency:** Pairs with D4 (RunController respects SIGTERM ≡ single Ctrl-C per r1b D-10, so tmux-detached runs are stoppable gracefully).

**Timing:** **Needed-now** (free; correct from day 1).

**Nature:** Research-settled for the flag; final ops doctrine is R1b.

---

### B-11 — Reproducibility wording

**Recommendation:** **Re-scope §5.7's "give a colleague the folder ⇒ reproduce" to "re-run to statistical equivalence + exact checkpoint continuation" per D6's F6/F7 findings.** Endorse the suggested default.

**Endorse or override:** Endorse. PyTorch explicitly does not promise reproducibility across releases/platforms (F6); MPS-specific determinism is weaker still (F7). The runbook and the next doc revision should re-scope the folder hand-off promise to what the platform supports. Pairs with D6's seed-band comparison protocol.

**Confidence:** **High.** No real uncertainty.

**Consistency:** Pairs with D6 (accepted-variance policy) and B-6 (environment fingerprint in run folder).

**Timing:** **Deferrable** (doc/runbook text) but should accompany the runbook.

**Nature:** Research-settled.

---

## Composed first-run recipe (coherence check)

A short end-to-end description of the resulting first run, as a check that the picks compose.

**One-time setup.** Miniforge3 install → conda env `pinn-train` (Python 3.11) → `pip install torch tensorboard pyyaml numpy h5py` (torch 2.12.x wheel includes MPS, F1) → verify: `python -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"` → expected `2.12.x True`.

**First build acts (before any long run).** Run the spec's §10 acceptance probes on-device — especially §10.3 componentwise-AD probe and §10.5 loss-stability dry run — in float32 on `mps` with `PYTORCH_ENABLE_MPS_FALLBACK` *unset* so any unimplemented op in the double-backward graph fails loudly (F4; U-9). This simultaneously certifies the AD contract AND feeds the precision adjudication (D1-p). Layer in r1b K5 rungs 0–3 (environment, AD-vs-finite-difference, componentwise shape, force-energy) — these are the spec's §10 probes re-cast for the trainer's exact code path. Then run r1b K5 rung 6 (the ~5-minute smoke test: stage-0 subset, `n_col=256`, ~300 steps, `checkpoint_every=100`) — measures `s/step`, feeds r1b K4 forecast, verifies the full mechanical surface (`runs/<name>/` directory appears, loss lines print with all five terms finite, one Ctrl-C produces a graceful checkpoint, `--resume` continues from it).

**Configure (one YAML per run, keyed per B-9):**

```yaml
run:   { name: first-run, seed: 1234, device: mps, precision: float32,
         max_steps: 100000, log_freq: 100, checkpoint_every: 1000,
         guards: {nan: true, loss_explosion: true, disk_floor: true,
                  memory_watermark: true} }      # thresholds ⚖ pending R1b
stage: { start: 0, data_version: <from v1.5 PIPE-XX>, residency: auto }
opt:   { schedule: ctl-phase2, stage0_lr: 1.0e-3, anneal: cosine,
         lbfgs: {history: 10, line_search: strong_wolfe, max_iter: 20} }  # B-1/D5-B
loss:  { weights: phys05-warmup, collocation: {strategy: uniform, n_col: 2048} }  # D5-H/E
```

**Launch:**

```bash
cd <project-root> && conda activate pinn-train
caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml
```

**What you watch.** Startup sequence (device line — now also `mem cap: 16.8 GB (0.7×)`; data line; `Stage 0 of 7`), then one line per 100 steps showing **five** loss terms + total + lr + λ vector + s/step + ETA (B-2), and every 1,000 steps a `mem:` line (D3). Secondary: `tensorboard --logdir runs/` → http://localhost:6006 (D2). Mac-side: Activity Monitor GPU > 0%, swap flat (baseline §5.5 kept — but see r1b D-11: don't trust the 60–95% GPU band for this dispatch-heavy workload; compare against the smoke test's recorded baseline).

**Stage-0 shape under the defaults.** Adam phase with PHYS-05 warmup → plateau handoff (log-slope > −5e-3 for 50 epochs) → full-batch L-BFGS via accumulate-in-closure (D5-B) → spec's RECOVER state on NaN/Inf (auto-rollback-retry, bounded budget) → 4 promotion criteria evaluated at the validation cadence (**value needed — U-5**) → on promotion: `stage-0-final.pt`, `curriculum.jsonl` record, fresh Adam, re-warmed λ, `stage-1-init.pt` (D7). Stop anytime: Ctrl-C once = graceful checkpoint (baseline kept). Guard stop: `GUARD: <reason>` + `failure/` bundle (D4).

**Resume:**

```bash
caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml \
    --resume runs/first-run/checkpoints/latest.pt
```

**Pairwise coherence.** (1) B-1 vs PH-7 — resolved by adopting the spec schedule. (2) D5-B full-batch L-BFGS vs 24 GB — resolved structurally by accumulate-in-closure; residual risk is wall-time (R1b duration question). (3) D2 TensorBoard vs B-6 folder contract — resolved by homing `tb/` inside `runs/<name>/`. (4) D6 accepted-variance vs §6.2 run comparison — resolved by the seed-band protocol (2–3× stage-0 pilot repeats). (5) D4 guards + spec's RECOVER + D7 promotion — all consume the same closure/seam structure of D5-B; RECOVER is loop-internal, D4 Tier 1 is fallback, D7 manual rollback is operator-initiated. (6) Expected run duration — not estimated here; R1b's feasibility lane (explicit join).

---

## What the runbook inherits (needed-now set, concrete defaults/instructions)

The subset of recommended picks that lands in the non-expert operator's first runbook:

**Command shapes.**
- Setup: Miniforge3 install → `conda create -n pinn-train python=3.11` → `pip install torch tensorboard pyyaml numpy h5py` → verify MPS available.
- Launch: `caffeinate -is python -m pinn.train --config configs/runs/<name>.yaml` (lid MUST stay open per r1b DRO-2; on Apple Silicon, lid-close forces sleep that `caffeinate` cannot override).
- Resume: same + `--resume runs/<name>/checkpoints/latest.pt`.
- Rollback: same + `--resume runs/<name>/checkpoints/stage-{k}-final.pt --hold-stage`.
- Monitor: `tensorboard --logdir runs/` → http://localhost:6006.
- Pre-flight (DO-CONFIRM gate, r1b K3 §5.2): trainer-printed block (ladder rungs green, hashes match, AC power connected, caffeinate active) before every run > 30 min; re-run after any upgrade (r1b DRO-4).

**Checkpoint artifact format.** Single `.pt` per checkpoint containing only state_dicts/tensors/scalars (loads under `torch.load` defaults, F8); names `step-XXXXXX.pt`, `latest.pt` (copy), `best.pt`, `stage-{k}-final.pt`, `stage-{k+1}-init.pt`, `emergency-*.pt`; `*.pt.tmp` is documented crash debris.

**Run-folder contract (B-6 superset of baseline §5.7).** `config.yaml` (frozen), `checkpoints/`, `logs/train.log{,.jsonl}`, `tb/`, `curriculum.jsonl`, `status.json` (heartbeat timestamp + seed record + guard state), `summary.{md,json}`, `failure/` (only on failure), `data-manifest.json`, plus r1b D-12's environment fingerprint (`sw_vers`, `python -V`, framework version/build, lockfile hash).

**Monitoring vocabulary.** The five loss terms + λ vector + grad-norm in every log line (B-2); `GUARD: <reason>` stop messages; the heartbeat rule ("status.json older than 10 min while the process lives ⇒ hung"); the `mem:` line and the 0.7 watermark meaning; r1b K1 watchlist (signal → likely meaning → first response).

**Comparison doctrine (D6).** Runs are compared on validation metrics outside the calibrated seed-band (2–3× stage-0 pilot repeats with different seeds); the folder hand-off promise is re-scoped to statistical-equivalence + exact checkpoint continuation (B-11).

**Sleep/thermal (B-10, r1b K2).** `caffeinate -is` (not `-d`); lid open + AC power for the whole run; hard flat surface, ventilated; Energy Mode = Automatic (or High Power for multi-day runs); `pmset -g assertions` to confirm caffeinate active.

**Hard-constraint pressure flags (carry in the runbook).** (1) Full-batch L-BFGS naïvely violates the 24 GB reality — the runbook must carry the accumulate-in-closure assumption and its wall-time consequence (R1b duration lane). (2) Under D1-p branch (ii), every GPU-related instruction (device line, GPU 60–95% health check, MPS error rows) becomes inapplicable — the runbook forks on the adjudication outcome. (3) Determinism limits (F6/F7) cap what any runbook may promise about reproduction. (4) The unattended-run premise is only as good as the sleep wrapper and guards — final lid/sleep/thermal doctrine is R1b's, and the runbook should not be finalized before that consolidation.

**R1b joins inherited as placeholders.** Guard thresholds ⚖; divergence-after-transition signal (enables D7-D); run-duration/feasibility numbers; health-watchlist wording for the "what you watch" sections; sL-BFGS implementation (U-7 — custom in every framework; not needed until stage 3 approaches).

**Deferrable set (NOT in the first runbook).** Hydra three-file config (B-9 keeps single-YAML keyed); sL-BFGS implementation (U-7); D7-D auto-revert guard (needs R1b signal); Tier 3 auto-remediation beyond spec's RECOVER; full 7-stage curriculum buildout (only stage 0 + lookahead glance at stage 1); hardened long-horizon evaluation harness; bitwise reproducibility provenance (spec itself defers — "Ignore Now, Come Back Later"); active-learning Phase 3.

---

## Claims-and-uncertainty register

Every place the attached materials were silent/ambiguous, every project-side number needed but not in the files, every assumption made. **No invented facts or numbers.**

### Project-side unknowns (numbers needed but not in attached files)

| ID | Item | Status / what's needed |
|---|---|---|
| U-1 | Snapshots per trajectory (`S̄`) / integration horizon per dataset set — controls the D3 in-memory verdict | Not in attached files. Project must supply `S̄` or `t_max` per set + cumulative per-stage sizes. D3-C's adapter is parameterized to absorb any answer. r1b §1.6 brackets total training memory at 2–7 GB typical, low-GB worst case, "comfortably inside 24 GB" — but stage-2 full-batch L-BFGS is the real risk. |
| U-2 | M5 Pro–specific MPS performance characteristics (step times, thermal envelope under sustained second-order AD) | No primary-source benchmark data for this SoC located (r1b C-9). Smoke test (r1b K5 rung 6) measures `t_step` directly and collapses r1b K4's 30×-wide envelope. |
| U-5 | Validation-evaluation cadence — the spec's promotion criteria consume `L_val(i)` but neither document says how often validation runs | Must become a config knob; numeric value is R2 territory; the *existence* of the knob is a D5 skeleton fact (adopted). |
| U-6 | Causal-weight underflow clip bound | Spec explicitly declines to choose and instructs surfacing a gap if execution needs one — it will (exp of large negative sums). Gap surfaced; value to be set at implementation with a logged rationale. |
| U-7 | Stochastic L-BFGS provenance and algorithm — "batch 32, curvature interval 10" matches research variants, but the spec cites no reference implementation; none of the three frameworks ships one (F11/F13; torch's LBFGS is deterministic-objective) | Custom-implementation ownership is unassigned (B-4). Needs either a scheduling decision by the owner or spec-level renegotiation (out of this round's authority). Not needed until stage 3 approaches — deferrable for the Stage-0 slice. |
| U-9 | Whether every kernel in this network's double-backward graph has an MPS implementation (sin/linear/LayerNorm backward-of-backward, `jacfwd`/`jacrev` interactions) | Not provable from documentation — op-coverage surface is a moving list (F4). Adjudicated empirically by running the spec's §10.3 probe with fallback disabled (first build act). |
| U-12 | `data_version_hash` production/verification mechanism | The check is committed baseline; the hash's source is v1.5 PIPE-XX's; the adapter implements "compare and refuse," nothing more. |
| U-15 | Expected run durations / first-run feasibility | Explicit R1b dependency. r1b K4 §1.4 gives a parameterized envelope (0.7 h optimistic to 52 days worst credible), not a number — `t_step` measurement from the smoke test collapses it. |

### ⚖ thresholds the r1b files do NOT actually give numbers for (Stage-2 placeholders)

| Decision | Threshold | Status |
|---|---|---|
| D4-c Tier 1 | Loss-explosion kill switch: ⚖-multiple of trailing median for ⚖ consecutive logs | r1b gives no numbers — Stage-2 placeholder. |
| D4-c Tier 1 | Disk-floor guard: ⚖ GB free | r1b gives no number — Stage-2 placeholder. |
| D4-c Tier 2 | Memory-watermark guard: ⚖ × D3 cap for ⚖ consecutive logs | r1b gives no numbers — Stage-2 placeholder. |
| D4-c Tier 2 | Heartbeat/hang detection | Sheet specifies 10 min, traceable to baseline §5.8 + r1b K1 ("Step number frozen ≥ 5 min"). 10 min is a sheet consolidation; r1b does not directly state "10 min." |
| D7-c D7-D | Auto-revert divergence signal: ⚖ steps post-promotion, divergence magnitude | r1b gives no numbers — Stage-2 placeholder. D7-D itself deferred. |
| D3 | Memory watermark (0.7 vs 0.8) | Sheet's 0.7 is a sensible default; r1b does not specify — leave configurable. |

### Spec-drift findings (current specs contradict or postdate the decision sheet)

| ID | Finding | Reconciliation |
|---|---|---|
| **SD-1** (resolves U-14) | SI-PINN-003 (batch construction inconsistency) is now **RESOLVED** per current spec — Phase 34 designated `ctl_instruction.md` as the canonical batch-construction home (`pinn_architecture.md` SI-PINN-003 entry, line 3215–3219). The decision sheet's U-14 still flags this as open. | The spec is reconciled; the trainer's batch assembly follows the CTL composition (replay+lookahead). U-14 can be closed. |
| **SD-2** | Spec's Phase 33 CURR-03 (`ctl_instruction.md` lines 1915–1988) defines a 3-state curriculum machine: **ADVANCE / RECOVER / HALT-REVIEW**. RECOVER = automatic rollback-and-retry on NaN/Inf with bounded retry budget. The decision sheet's D4 Tier 1 NaN guard (stop-and-preserve) and D7-c manual rollback do not account for RECOVER. | RECOVER is loop-internal, spec-mandated, always-on (even for the Stage-0 slice). D4 Tier 1 NaN guard is the *fallback* when RECOVER's retry budget is exhausted → HALT/REVIEW. D7-c manual rollback remains the operator-initiated path. D4 Tier 3 "auto-rollback-and-retry" is partially superseded by RECOVER for NaN/Inf. **Owner/spec-author confirmation needed** on the exact RECOVER↔Tier-1-guard boundary. |
| **SD-3** | The chatgpt-pro-resolution's D3 suggested default (Option C, chunked HDF5 streaming, ONE-WAY door) contradicts the decision sheet's D3-C (auto→in-memory, TWO-WAY door for residency). | The sheet's framing is more honest given U-1. **Adopt the sheet's nuanced door split:** adapter interface is one-way (loop code assumes it); residency policy is two-way (config flip). |

### Other gaps / assumptions

- **Hardware spec mismatch (r1b C-14 / D-1).** Project docs say "16 CPU / 15 GPU" M5 Pro; Apple's published M5 Pro base is 15-CPU/16-GPU (configurable to 18/20), 24/48 GB, 307 GB/s. Does not change any estimate; flagged for correctness. **Owner should confirm actual hardware.**
- **D1-p (precision branch).** Out of scope per §3; recommendations hold under both branches. Under branch (ii), every GPU-related instruction (device line, GPU 60–95% health check, MPS error rows) becomes inapplicable; the runbook forks on the adjudication outcome.
- **B-8 (ε_H gate direction).** Spec-settled per §3. `ctl_instruction.md` lines 559–565 unambiguous: REJECT if `eps_H > 1e-5` (smaller passes); `eps_H = 0 → SCS = -inf → Excellent`; bands Excellent ≤ -10, Acceptable (-10,-6], Marginal (-6,-5], Reject > -5. The baseline design doc's §6.3 inverted-looking example (`ε_H: 8.2e-6 (required: > 1e-5) → FAIL`) is a display typo in a non-authoritative doc (r1b C-12), not a contradiction in the locked metric. Implement the gate as smaller-passes.
- **Validation-gate `eps_H` vs training-loss `eps_H`.** `ctl_instruction.md` lines 572–574 explicitly distinguishes them — same glyph, different quantity. Validation-gate `eps_H` (gate threshold 1e-5, smaller passes) ≠ training-loss `eps_H = 1e-4 * S_H` (energy denominator floor, `pinn_architecture.md` §3.4). Don't conflate.
- **Spec's HYDRA three-file stack.** Named in `ctl_instruction.md` (Phase 18 Implementation Notes) under a heading the spec itself marks "Ignore Now and Come Back Later" — deferred guidance, not a binding science contract. NOT a spec drift; the sheet's B-9 reading is correct.
- **Referenced-but-unattached materials.** `sampling_method.md` (frozen data-generation spec, out of scope for build decisions per §1), `PINN_architecture_plan.tex`, the §10 probe scripts under `.planning/...`, `simulation_data/`, v1.5 PIPE-XX format, SCS/SASD/IPR/PSC metric definitions (gate consumes SCS; only its threshold is in the attached design). Treated as unavailable per §3; the verification layer cannot fully specify `metrics.json` until the metric definitions arrive.
- **PyTorch `torch.func.jacfwd` MPS bug.** Through PyTorch 2.7.0, `torch.func.jacfwd` raises `RuntimeError: as_strided_tensorimpl does not work with MPS` for any traced function containing `torch.cat`/`torch.stack`/`torch.vstack` (pytorch#152701) — and a SIREN backbone with skip connections is exactly that concat-bearing case. On MPS prefer a `jacrev`-based second-order path (`jacfwd(jacrev(...))` for the Hessian route); pin PyTorch ≥ 2.7.1/2.8 where the bug is fixed (current stable 2.12.x per F1).
- **D-4 (forward-mode AD cost lever, r1b).** Because the differentiation variable `u` is a scalar, jvp-based forward(-over-forward) AD computes all 9 first/second derivative components in O(1) passes vs 9 reverse passes for the spec's named patterns — an order-of-magnitude cost lever. PHYS-02's "Equivalent full-Jacobian method" clause (`pinn_architecture.md` §5.3.1 line 3080) appears to admit it. Not a decision — an implementation strategy available inside D5-B/E that the spec permits.

---

## Standing restatement

This is a **recommendation for the owner to ratify**, not a science-spec verdict. **D1-p** (numerical precision branch) was left to the owner (another channel); **B-8** (ε_H gate direction) was left to the spec (settled unambiguously by `ctl_instruction.md` lines 559–565: smaller passes). Every claim above is grounded in the 8 attached source files; where the materials were silent, the gap is recorded in the claims-and-uncertainty register rather than invented. The owner makes the final call on every row.

---

# Appendix A — Phase 1: Multi-Perspective Scan (working record)

Six domain-recast perspectives, each reasoning only from the attached files, each grounding every claim with a filename citation.

### 1. The Apple-Silicon ML practitioner

**Core position (2 sentences).** MPS is the only mature GPU path on this machine for second-order AD, but it has sharp, specific edges the decision sheet handles correctly: no fp64 at all (F3), op-coverage gaps that fail loudly (F4), a `torch.func.jacfwd` `as_strided` bug on `torch.cat`/`stack` through 2.7.0 (pytorch#152701), `torch.mps.set_per_process_memory_fraction(0.7)` for OOM control (F5). The sheet's D1-A default and D3 watermark-0.7 are the right calls; MLX's lack of L-BFGS (F11) and JAX-Metal's effective abandonment (F12) make them non-viable for this spec.

**Strongest grounded evidence.** F3/F4/F5/F10/F11/F12 in `trainex-r1a-options-and-decisions.md` §0; pytorch#152701 cited in §D3.1; `trainex-r1b-findings.md` §1.5 (MPS double-backward gaps tracked op-by-op, fail loudly per op).

**One thing only this perspective would flag.** The MPS `as_strided` bug specifically bites SIREN-with-skip-connections architectures because of the concat in the skip path — and this project's SQR-SkipResNet-SIREN (`pinn_architecture.md` Table 2) is exactly that case. Pin PyTorch ≥ 2.7.1 and prefer `jacrev`-based second-order paths on MPS; the §10.3 probe with fallback disabled is the verification instrument.

### 2. The PINN & numerical-methods researcher

**Core position (2 sentences).** The specs are unusually prescriptive — `pinn_architecture.md` PHYS-02 §5.3.1 forbids the sum-trick VJP and mandates all 9 componentwise derivatives, lists three acceptable patterns (`jacrev`+`vmap`, explicit loop, "equivalent full-Jacobian method"), and pins `epsilon_train = 1e-5` matched-Plummer softening; `ctl_instruction.md` Phase 2/2b mandates two-phase Adam→L-BFGS with full-batch early / sL-BFGS late, "Critical" Adam-state reset at each stage, PHYS-05 scheduled loss weights, plateau-driven handoff (log-slope > −5×10⁻³ for 50 epochs), and a 4-criterion stage-advance gate. Any framework/loop that cannot express these is off-spec; the sheet's D5-B/E/H combo is the minimum skeleton that does.

**Strongest grounded evidence.** `pinn_architecture.md` §5.3.1 PHYS-02 contract (lines 3047–3116) + §10 acceptance probes (lines 3173–3198); `ctl_instruction.md` Phase 2 / 2b / Stage Transition Criteria / Consolidated Hyperparameter Schedule (lines 1684–1996).

**One thing only this perspective would flag.** The spec's "equivalent full-Jacobian method" clause (line 3080) **admits forward-over-forward AD**, which for a scalar autodiff leaf `u` computes all 9 first/second derivative components in O(1) passes vs 9 reverse passes — an order-of-magnitude cost lever (r1b D-4, §1.2 κ table). The skeleton (D5-E sampler interface) should not preclude a stateful `jvp`-based sampler path; the §10.3 probe certifies whichever AD pattern is chosen.

### 3. The adversarial build reviewer

**Core position (2 sentences).** The suggested defaults are mostly right but three will fail on first run if not adjusted: (a) PH-7's baseline optimizer default would silently run off-spec (B-1); (b) the 3-term log line cannot show the energy/L drift that the watchlist depends on (B-2 / r1b DRO-5); (c) the D4 Tier 1 NaN guard duplicates the spec's RECOVER state without acknowledging it (SD-2). The chatgpt-pro-resolution's D3 streaming-first stance is over-engineered for the Stage-0 slice where r1b §1.6 says memory is 2–7 GB comfortably.

**Strongest grounded evidence.** `trainex-r1a-options-and-decisions.md` §8 B-1/B-2; `trainex-r1b-findings.md` §1.6 (memory figure) and §3.2 (watchlist depends on 5-term logging); `ctl_instruction.md` Phase 33 CURR-03 (lines 1915–1988, RECOVER state).

**One thing only this perspective would flag.** The decision sheet's D7-c "manual rollback only" and D4-c "Tier 1 NaN guard stops" together read as if NaN handling is operator-mediated — but the spec's RECOVER state is automatic rollback-and-retry with bounded budget, fired *before* any operator action. The trainer must implement RECOVER from day 1 (spec-mandated), with D4 Tier 1 as the fallback when RECOVER's budget is exhausted. This is a spec-drift finding (SD-2), not a sheet error to silently fix.

### 4. The cost-&-effort economist

**Core position (2 sentences).** For one non-expert on one machine, the true costs are developer-hours, maintenance burden, and the cognitive load of the runbook — not peak FLOPs. The cheapest path that still works AND protects the one-way doors is: PyTorch (largest searchable help, no custom L-BFGS to maintain), in-memory preload for stage 0 (r1b §1.6 says it fits), TensorBoard + JSONL-canonical (swap-trackers-later is free), and the thinnest loop shape that still expresses the spec (D5-B not D5-C).

**Strongest grounded evidence.** `trainex-r1a-options-and-decisions.md` §0 F11 (MLX no L-BFGS) and F12 (JAX-Metal unmaintained) — both imply significant custom-implementation or maintenance tax; `trainex-r1b-findings.md` §1.6 (memory fits); `postspec-r1-direction-assessment.md` §7 (what NOT to work on yet — deferring full platform, Hydra sweeps, polished runbook).

**One thing only this perspective would flag.** The sL-BFGS gap (U-7) is the single largest hidden implementation cost lurking past stage 2 — no framework ships the spec's "batch 32, curvature interval 10" variant, and the spec cites no reference. For the Stage-0 slice this is deferrable, but the owner should consciously schedule either implementation work or spec-level renegotiation before stage 3 approaches; it is not free.

### 5. The operations-experience lens (r1b-grounded)

**Core position (2 sentences).** The r1b findings document a 5-minute smoke test that doubles as both the K5 correctness gate AND the K4 measurement instrument (r1b DRO-9 / D-5), a 7-rung correctness ladder (K5), a PINN health watchlist mapping signals to non-expert first responses (K1), and the lid-close-does-not-survive-sleep reality (K2 / DRO-2). The decision sheet's defaults compose cleanly with these — D4-d's failure bundle is the runbook's "zip and ask for help" pattern; D6's seed-band calibration is 2–3× stage-0 pilot repeats; B-10's `caffeinate -is` is r1b DRO-3.

**Strongest grounded evidence.** `trainex-r1b-findings.md` §2 (K5 ladder), §3 (K1 watchlist), §4 (K2 lid/sleep/thermal); `trainex-r1b-findings-2.md` K5.1 (ladder table), K2.1 (caffeinate flag pattern), Decision-Relevant Observations DRO-1 through DRO-9.

**One thing only this perspective would flag.** The "GPU utilization 60–95%" health band in baseline §6.1 is unreliable for this workload (r1b D-11) — a 0.73 M-parameter, dispatch-heavy double-backward workload can be healthy at much lower GPU residency. The runbook should compare against the smoke test's recorded baseline, not an absolute band; otherwise the operator will panic at 30% GPU and stop a healthy run.

### 6. The non-expert operator / runbook advocate

**Core position (2 sentences).** The operator can read code and follow a runbook but is not a Python developer — every command must be paste-verbatim with expected output (r1b K3 §5.2 READ-DO pattern), every error must be name → meaning → action (r1b K3 §5.2 flat error table), every decision juncture must have one default action. The decision sheet's `caffeinate -is python -m pinn.train --config <yaml>` launch, `--resume <ckpt>` resume, and `failure/` bundle all yield the simplest operation with the best-typed failures and the most searchable tools.

**Strongest grounded evidence.** `trainex-r1b-findings.md` §5 (K3 patterns), §3.2 (signal → meaning → action watchlist); `trainex-r1b-findings-2.md` K3.1 (Diátaxis mapping), K3.2 (SRE playbook patterns), K3.3 (read-do vs do-confirm checklists); `2026-06-10-training-execution-design.md` §5 (entry points).

**One thing only this perspective would flag.** The decision sheet's B-9 single-YAML-with-keyed-stage/opt/loss/run is exactly right for this operator — Hydra would add a dependency, a concept set (defaults lists, sweeps, overrides), and a new class of error (composition failures) that the operator cannot diagnose. Keep the single YAML; the key-structure hedge preserves the migration path if Hydra's power is ever actually needed.

---

# Appendix B — Phase 2: Contradiction & Consistency Map (working record)

### 1. Per-decision conflicts

| Decision | Conflict | Resolution |
|---|---|---|
| **D3 door classification** | chatgpt-pro-resolution §6.7 says ONE-WAY (streaming-first); decision sheet D3-C says TWO-WAY for residency. | Reconcile (SD-3): adapter interface is one-way; residency policy is two-way. Adopt the sheet's nuanced split — the chatgpt-pro-resolution's stricter stance over-engineers for the Stage-0 slice where r1b §1.6 says memory fits. |
| **D4-c vs spec's RECOVER** | Decision sheet D4 Tier 1 NaN guard stops-and-preserves; spec's Phase 33 CURR-03 RECOVER auto-rolls-back-and-retries. | Reconcile (SD-2): RECOVER is loop-internal, spec-mandated, fires first; D4 Tier 1 is fallback when RECOVER budget exhausted → HALT/REVIEW. Owner/spec-author confirmation needed on boundary. |
| **D7-c vs spec's RECOVER** | Decision sheet D7-c "manual rollback only"; spec's RECOVER is automatic for NaN/Inf. | Reconcile (SD-2): RECOVER handles transient NaN/Inf automatically; D7-c manual rollback handles operator-initiated stage retreat; D7-D (deferred) handles broader post-promotion divergence. Three distinct mechanisms, not duplicates. |
| **B-9 config approach** | `ctl_instruction.md` names Hydra three-file stack; baseline is single YAML. | Both documents agree: the Hydra stack is under a heading the spec itself marks "Ignore Now, Come Back Later." Not a real conflict — the sheet's B-9 reading is correct. |
| **B-1 optimizer default** | Baseline PH-7 (Adam, LR 1e-3, exp decay 0.95/500) vs spec (1e-3 × 0.7^k, cosine, two-phase with L-BFGS). | Real cross-document conflict. Specs own the science; replace PH-7 with spec schedule. The only genuine spec-vs-baseline conflict found. |
| **B-8 ε_H gate direction** | Baseline §6.3 example reads inverted (`ε_H: 8.2e-6 (required: > 1e-5) → FAIL`); plain-English gloss says "smaller is better." | Display typo in non-authoritative doc (r1b C-12). Spec (`ctl_instruction.md` 559–565) unambiguous: smaller passes. Out of scope per §3. |

### 2. Strongest vs weakest grounding

- **Strongest:** D1 (F1–F15 verified capability baseline, all primary-source-cited); D6 (F6/F7 PyTorch official reproducibility doctrine + open MPS issue); B-10 (r1b K2 §4.1 + K2.1 both confirm `-is` over `-d`); B-1 (spec's own Consolidated Hyperparameter Schedule table).
- **Weakest:** D4-c thresholds (⚖ values not in r1b, left as Stage-2 placeholders); D7-c D7-D signal (R1b has not specified a divergence-after-transition metric); D3 in-memory threshold (depends on U-1, an unknown).

### 3. The resolving question

For the biggest contradiction (SD-2: D4/D7 vs spec's RECOVER), the one question that would settle it: **does the spec's Phase 33 CURR-03 RECOVER state subsume the D4 Tier 1 NaN guard, or do they operate at different layers (RECOVER = curriculum-state-machine-internal; D4 Tier 1 = trainer-process-internal fallback)?** Settled by: **a spec reading** (the spec says RECOVER "rolls back to the last well-formed checkpoint and retries" — curriculum-level; D4 Tier 1 "save emergency-nan checkpoint, exit non-zero" — process-level; these compose, they don't duplicate) — but **owner/spec-author confirmation** is still warranted given the severity.

### 4. Unanimous agreement = robust picks

All six perspectives agree on: **D1-A PyTorch+MPS** (only viable framework for this spec on this machine); **D5-B two-phase closure loop** (spec mandate, no real alternative); **D6-B+C accepted-variance** (F6/F7 makes strict-mode dishonest on MPS); **B-1 replace PH-7 with spec schedule** (specs own the science); **B-2 widen log fields** (watchlist depends on it); **B-10 `caffeinate -is`** (r1b K2 is unambiguous); **B-11 re-scope reproducibility wording** (F6/F7 makes the over-claim dishonest). These are the high-confidence, low-risk recommendations.

### 5. Blind spots and drift

- **Blind spot:** No perspective could ground a number for the D4-c ⚖ thresholds (loss-explosion multiple, disk-floor GB, memory-watermark ratio, consecutive-logs count) — r1b gives no numbers. Registered as Stage-2 placeholders, not invented.
- **Blind spot:** No perspective could ground a number for D7-D's divergence-after-transition signal — r1b gives none. D7-D deferred; signal is Stage-2.
- **Spec-drift (SD-1):** SI-PINN-003 (batch construction) is now resolved per current spec; the sheet's U-14 is stale. Recorded.
- **Spec-drift (SD-2):** Spec's Phase 33 CURR-03 RECOVER state not reflected in sheet's D4/D7. Recorded.
- **Spec-drift (SD-3):** Internal contradiction between chatgpt-pro-resolution's D3 (streaming-first, one-way) and decision sheet's D3-C (auto→in-memory, two-way). Reconciled.

---

# Appendix C — Phase 4: Peer Review / Self-Critique (working record)

### 1. Confidence audit

| Decision | Confidence | Honesty check | Owner-look flag? |
|---|---|---|---|
| D1 | High | Grounded in F1–F15; U-9 is the one empirical gate | No |
| D2 | High | JSONL-canonical rule makes it two-way | No |
| D3 | Medium | U-1 unknown; adapter interface one-way protects | Yes — U-1 measurement needed before stage 2 |
| D4-a | High | Conditional wall-clock addition tied to smoke-test | No |
| D4-b | High | Free, well-grounded | No |
| D4-c | Medium | SD-2 spec-drift; ⚖ thresholds undefined | Yes — owner/spec-author on RECOVER boundary |
| D4-d | High | Free, additive | No |
| D5-a | High | Spec mandate | No |
| D5-b | High | Spec mandate | No |
| D5-c | High | Spec mandate; U-6 clip bound is implementation-time | No |
| D6 | High | F6/F7 well-grounded | No |
| D7-a | High | Spec-aligned | No |
| D7-b | High | Spec mandate (not a real choice) | No |
| D7-c | Medium | SD-2 spec-drift; D7-D deferred | Yes — owner/spec-author on RECOVER boundary |
| D7-d | High | Clean artifact contract | No |
| B-1 | High | Spec mandate | No |
| B-2 | High | Spec mandate + watchlist dependency | No |
| B-3 | High | Free, two-way | No |
| B-4 | High | Documentation | No |
| B-5 | High | Field list needs owner ratification | Yes — owner ratifies field classification list |
| B-6 | High | Free, additive; r1b D-12 addition | No |
| B-9 | High | Spec's "Ignore Now" heading makes Hydra deferred | No |
| B-10 | High | r1b unambiguous | No |
| B-11 | High | F6/F7 unambiguous | No |

### 2. Weakest link

The recommendation I am least confident in is **D4-c (auto-guard tier)**, specifically the SD-2 spec-drift reconciliation. Exactly what would settle it: a **spec-author clarification** on whether RECOVER (Phase 33 CURR-03) subsumes the D4 Tier 1 NaN guard or operates at a different layer. My reconciliation (RECOVER is curriculum-state-machine-internal and fires first; D4 Tier 1 is trainer-process-internal fallback when RECOVER's retry budget is exhausted) is the most natural reading of the spec text — but the spec does not explicitly say "and then the trainer's external NaN guard fires" — so owner/spec-author confirmation is warranted.

D1-p precision and B-8 gate direction are NOT weakest-link candidates — both are explicitly out of scope per §3 (D1-p is owner-carved; B-8 is spec-settled).

### 3. Bias check

Did one perspective dominate? The non-expert operator perspective (Perspective 6) and the operations lens (Perspective 5) are the most heavily represented in the recommendations, which is appropriate given the hard constraint that this is a non-expert operator on a single machine. However, I checked each one-way door (D1 framework, D5 loop shape, D7 artifact contract, D6 seed schema, B-5 config schema, B-6 run-folder contract) against the practitioner and economist perspectives to confirm the simplest-for-operator choice did not override a one-way door. No row needed rebalancing — the one-way doors (D1-A, D5-B/E/H, D7-A/d, D6 seed schema, B-5 field-classified, B-6 additive members) are all endorsed by multiple perspectives, not just the operator's.

The adversarial reviewer's spec-drift findings (SD-1, SD-2, SD-3) were incorporated rather than overridden by the operator-simplicity lens — D4-c and D7-c were adjusted to acknowledge RECOVER, not simplified to ignore it.

### 4. Missing angle

A potential **seventh** decision-relevant perspective: **the future-maintenance / project-handover lens** — the person who inherits this codebase 1–2 years from now (possibly a different non-expert, possibly the owner returning after a gap). This lens would emphasize: code readability over cleverness, environment lockfile durability (r1b K2.3's "archive the actual wheels because lockfile pins don't survive yanked packages"), schema versioning (`run_schema_version` and `checkpoint_schema_version` from chatgpt-pro-resolution's B4), and the run-folder-as-documentation property. Re-running affected decisions through this lens:

- **D2 (TensorBoard):** unchanged — TB event files are widely readable; JSONL is human-inspectable.
- **D6 (accepted-variance):** unchanged — recording the seed set + RNG states in checkpoints is exactly what future-handover needs.
- **B-6 (run-folder contract):** strengthened — r1b D-12's environment fingerprint addition is essential for handover.
- **B-9 (single YAML):** unchanged — the keyed structure is more readable than Hydra defaults lists for a returning non-expert.

No recommendations changed by adding this lens; it reinforces existing picks.

### 5. Overall honesty grade

If a Stanford professor reviewed this resolution: **A−**. Decisive (one option per decision, no waffling), honest (confidence levels tagged, biggest uncertainty per row stated, ⚖ thresholds left as Stage-2 placeholders rather than invented), coherent across decisions (the framework choice constrains tracking/data/loop options cleanly; the spec's RECOVER state reconciles with D4/D7), and free of invented facts or numbers. The biggest weakness a rigorous reviewer would flag: the SD-2 spec-drift finding (RECOVER vs D4 Tier 1) is **flagged for owner/spec-author confirmation** rather than resolved with finality — but that is the honest move given the spec text's ambiguity on the boundary. The reviewer would also note that the D3 door classification (SD-3) required reconciling an internal contradiction in the source bundle, which is resolved rather than papered over. Final fix: none required; the claims-and-uncertainty register is complete and the standing restatement is explicit that this is a recommendation for ratification, not a verdict.

---

*End of resolution. Phase 1–4 working records appended for transparency per §6 footnote.*
