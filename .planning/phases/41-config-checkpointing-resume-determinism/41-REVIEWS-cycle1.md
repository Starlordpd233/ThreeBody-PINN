---
phase: 41
reviewers: [codex, grok, claude-max, claude-kimi]
rerun_reviewers: [claude-max, claude-kimi, grok]
reviewed_at: 2026-07-18T05:31:30Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T052528Z-62777
merged_existing_reviews: true
---

# Cross-AI Plan Review — Phase 41

## codex Review



## Summary

Phase 41 is well decomposed and largely aligned with CTRL-01..08. The main risk is cross-plan contract drift: checkpoint payload shape, frozen config contents, strict-CPU runtime behavior, and resume identity classification are not yet specified tightly enough to guarantee the end-to-end resume/determinism goal. All requested plan/support files inspected were readable.

## Strengths

- Good dependency ordering: config/atomic scaffold first, checkpoint and guard modules in parallel, controller wiring next, `pinn.train` last.
- Strong edge coverage around atomic writes, corrupt checkpoint fallback, coincident checkpoint triggers, idempotent promotion, and guard trips.
- Good governance discipline around owner-carved values: wall-clock ceiling, guard thresholds, and B-5 field lists are kept provisional.
- The plans correctly identify `RunController` as the central seam for mid-stage checkpointing and exact RNG continuation.

## Concerns tagged HIGH / MEDIUM / LOW

- **HIGH:** Checkpoint payload shape is inconsistent across plans. `41-02` requires CTX-53 top-level keys like `model`, `optimizer`, `curriculum`, `rng`, `counters`, `config_identity`, `schema_version`, but the existing `CurriculumController` payload is `tag/stage/run_controller`, and `41-04` mostly adds keys inside `RunController.state_dict()`. Without one assigned payload builder, real checkpoints may fail the store’s own fallback validation.

- **HIGH:** CTRL-08 says the frozen `config.yaml` and every checkpoint carry all four RNG streams, but `41-01` defines `config.yaml` as a `TrainingConfig`-only resolved copy that must re-parse equal to `TrainingConfig`. Those two contracts conflict unless the plan defines a serializable RNG section, an ignored metadata envelope, or a separate artifact.

- **HIGH:** The strict-CPU switch may not actually force CPU. `41-03` says `apply_strict_cpu_determinism()` resolves `float64/cpu`, but `41-05` then resolves runtime from `config.run.precision/device`; if the config remains `float32/mps`, the model can still build on MPS.

- **HIGH:** Resume config diff cannot both name changed fields and enforce unclassified-field refusal from only a stored digest. `41-05` passes only `checkpoint_config_identity`, so it can detect mismatch but not identify which field changed. It also omits several CTX-57 identity classes from the explicit payload list, including dataset version/hash, split policy, curriculum/stage definitions beyond `max_epochs`, and loss-catalog structure.

- **MEDIUM:** Nested YAML validation needs a recursive contract. `41-01` specifies unknown-key diffing for top-level `run/stage/opt/loss`, but newly introduced nested surfaces like `run.guards.*` and `run.checkpoint.*` need the same dotted-path `ConfigKeyError` behavior.

- **MEDIUM:** Adam reset at `stage-{k+1}-init.pt` is only clearly safe when `stage_factory` swaps in a fresh controller. The no-factory path can retain the old `self._optimizer` unless the plan explicitly clears it before saving the init anchor.

## Suggestions

- Add a single `build_checkpoint_payload(...)` owner, probably in `controllers.py` or a small checkpoint-payload helper, and require all rolling/latest/anchor saves to use it.
- Resolve the frozen-config RNG contract before implementation: either extend the YAML envelope deliberately or move full RNG recording to checkpoints plus a separate run-start state artifact.
- Make strict CPU return or produce the actual `RuntimeSpec` used by `pinn.train`, or have `pinn.train` override/reject incompatible precision/device when strict mode is enabled.
- Store enough resume metadata to compare old vs incoming classifications, not just a digest; add a classification-coverage test over every resolved config/identity field.
- Add recursive YAML unknown-key tests for nested config sections.

## Overall Risk

**HIGH** until the cross-plan contracts above are tightened. The plans are strong, but the current mismatches can let isolated unit tests pass while the Phase 41 end-to-end resume/determinism contract fails.

---

## grok Review

I'll review Phase 41 by reading the five plan files first, then spot-check CONTEXT/SPEC/requirements only where needed to validate concerns.Spot-checking SPEC/CONTEXT and a few live symbols to validate the higher-risk plan concerns.I have enough evidence for the highest-impact findings. Writing the concise review.# Phase 41 Plan Review — Config, Checkpointing, Resume & Determinism

**Plans reviewed:** `41-01` … `41-05`  
**Spot-checked:** `41-SPEC.md`, `41-CONTEXT.md` (CTX-50–64), `ROADMAP.md`, live `checkpoint.py` / `controllers.py` / phase40 tests  
**Git context:** `milestone/v2.0` worktree `trainex` (not edited)

---

## 1. Summary

The five-plan decomposition matches the phase goal well: foundation (config + atomic I/O) → parallel store/guards/determinism → controller mid-stage hooks → composition root (`pinn.train`). Governance is strong (⚖ provisional seams, no invented owner values, Phase 42/43 boundary held, threat models present). The central architecture insight (Pattern 4: mid-stage hooks must live inside `RunController`) is correctly owned by `41-04`.

The plans will **not** reliably deliver CTRL-05 fail-safe resume and CTRL-03/08 end-to-end until several **cross-plan payload and wiring holes** are closed: CTX-53 payload composition is split inconsistently across plans, the unclassified-field refuse rule is not implementable from identity-digest alone, and `41-04` store-method calls break the “phase40 stays green with naive store” claim.

---

## 2. Strengths

- **Clear wave graph:** `01 → (02 ∥ 03) → 04 → 05` matches real dependencies; parallel wave-2 work is actually independent.
- **Falsifiability floor:** Option A `python -m pinn.train` + tiny synthetic Stage-0 loop is the right way to make CTRL-01/02/05/08 testable.
- **Governance discipline:** D4-a / R-1 / B-5 stay ⚖; seed fan-out and memory-signal choices are explicit assumptions, not silent inventions.
- **Security-conscious store design:** `yaml.safe_load` only, `weights_only=True` at every load site + prohibition test, atomic write + crash injection, fallback schema validation (Pitfall 4).
- **Correct restore-vs-reseed distinction** and repro honesty layer (CTX-64) are first-class, tested contracts.
- **Protocol preservation intent** for the Phase-40 seam is right; dual-trigger coincidence guard and rolling/anchor retention match SPEC acceptance.

---

## 3. Concerns

### HIGH

1. **CTX-53 payload composition is incomplete and inconsistent across plans**  
   Live `_checkpoint_payload` is still `{tag, stage, run_controller: state_dict}`.  
   - `41-02` fallback validation requires top-level `model`, `optimizer`, `curriculum`, `rng`, `counters`, `config_identity`, `schema_version`.  
   - `41-04` mid-stage saves use `self.state_dict()` (component keys under the controller, not a full CTX-53 envelope).  
   - `41-05` resume expects `config_identity` on the checkpoint.  
   **Nobody owns a single “compose CTX-53 payload” function** that every save path (boundary, rolling, best/latest) must use. Without that, fallback scan, resume refuse, and RNG-everywhere acceptance diverge or fail.

2. **CTRL-05 unclassified → refuse is underspecified / digest-only fail-open risk**  
   CTX-57/SPEC require refuse on **unclassified** field changes, not only identity digest mismatch.  
   `41-05` stores/compares a **sha256 of identity fields**. Operational changes correctly leave that digest unchanged — but so do **unclassified** fields outside the identity payload. Digest equality alone **cannot** implement fail-safe refuse. Field-level classification (and likely a stored resolved-config snapshot or full config diff) must be specified, or the prohibition is not testable as written.

3. **Identity payload under-covers the CTX-57 Conservative line**  
   `build_identity_payload` covers seed/precision/device/max_epochs/guards + partial `ArchitectureSpec` + `D`/`eps_soft`/`T`. CTX-57 also lists IC-vector/dataset hash, loss-catalog structure, curriculum/stage definitions, split policy, LayerNorm, etc. Either expand the payload to match the locked identity line, or explicitly document a ⚖-reduced proposal with owner ratification before claiming Conservative-line compliance.

4. **`41-04` + phase40 regression conflict**  
   Phase40 tests construct `TorchSaveCheckpointStore` and drive ADVANCE/RECOVER/HALT.  
   `41-04` adds unconditional `promote()` / `record_disposition()` calls on `checkpoint_store`. Those methods are **not** on the Protocol and **not** on the naive store. Claiming “hooks default None ⇒ phase40 byte-for-byte green” does not cover this: **CurriculumController changes are not optional**. Need no-op methods on the naive/empty path, Protocol extension, or duck-typed optional calls — plan does not choose one.

5. **strict-CPU switch vs `resolve_runtime` order in `pinn.train` (`41-05`)**  
   Plan applies `apply_strict_cpu_determinism` (resolve `float64`/`cpu` side effects) then still `resolve_runtime(config.run.precision, config.run.device)` which may rebuild on `float32`/`mps`. Unless train.py **overrides device/dtype from the strict path**, the switch is a false safety. Wiring must force network build onto the escape-hatch pair when the flag is on.

### MEDIUM

6. **RNG in frozen `config.yaml` vs CTRL-01 re-parse equality**  
   SPEC/CTX-62 require four RNG streams in the frozen config **and** every checkpoint. `41-01` freezes a `TrainingConfig` YAML that re-parses equal; tensors / bit-generator state do not fit that contract. Need an explicit format (sidecar, base64 section, seed-only-at-start + checkpoint-only mid-run) and which test owns it — currently `41-01` and `41-05` pull opposite directions.

7. **Nested YAML mapping for `run.guards` / checkpoint cadence**  
   Pattern-1 `_map_section` is described for flat section dataclasses. Nested frozen dataclasses under `run` need recursive mapping, defaults, and unknown-key dotted paths (`run.guards.disk_floor`). Under-specified; easy silent default or KeyError miss.

8. **`best.pt` write path unwired**  
   Store supports “validation improvement → best.pt”; no plan owns a validation signal or caller. Retention “never delete best” can be tested with a hand-planted file, but the retention **class** is only half-delivered.

9. **Hard-coded 24 GB unified-memory denominator (`41-03`)**  
   Threshold is ⚖ from config; capacity is a machine constant. Wrong on non–M5 Pro / CI CPU hosts; MPS APIs may be absent off-device. Need injectable total-memory (or skip/degrade path) for tests and honesty.

10. **`TorchSaveCheckpointStore` rename/replace risk**  
    `41-02` “replace the naive body” vs phase40 tests that import the class name. If the class is removed/renamed without an alias, the whole phase40 suite fails before any controller extension.

11. **Ledger path vs store root**  
    Store roots at `runs/<name>/checkpoints/`; ledger is `runs/<name>/curriculum.jsonl`. Easy off-by-directory bug; plans mention both but do not pin parent-run-dir ownership.

### LOW

12. **Step-0 dual-trigger:** `step % N == 0` usually fires at 0 — intentional? Document “checkpoint every N including 0” or use `step > 0 and step % N == 0`.

13. **“163/163” / “byte-for-byte” wording** is brittle; prefer “phase40 suite green” after additive changes.

14. **`latest.pt` full copy** doubles write I/O each checkpoint — acceptable for M5 Pro slice, but worth noting for disk-floor interaction with frequent N.

15. **Statistical-equivalence fresh-run test** in SPEC (tolerance seam at Phase 43) is only weakly reflected in `41-05` (mostly exact-continuation vs reseed). Fine if deferred, but mark as out-of-phase so AC isn’t overclaimed.

---

## 4. Suggestions

1. **Add a single owned composer** (e.g. `compose_checkpoint_payload(controller, …) → CTX-53 dict`) in `41-04` or shared helper; require all save paths (anchor, rolling, best, latest) to use it. Align fallback required-key list with that composer.

2. **Specify resume diff algorithm in two steps:** (a) classify every differing field vs `IDENTITY_FIELDS` / `OPERATIONAL_FIELDS`; (b) refuse if any identity or unclassified differs; only then compare digests as a fast path / integrity check. Store enough snapshot data (full resolved config dict under a plain key, or hash + field map) to make unclassified detection real.

3. **Reconcile identity coverage with CTX-57** before execute: either expand `build_identity_payload` or shrink the claimed “Conservative line” with an explicit ⚖ proposal note in CONTEXT.

4. **Regression strategy for `41-04`:** give production + naive stores `record_disposition` / `promote` / `save_anchor` (naive: no-ops / pass-through), or guard calls with `hasattr` / Protocol-optional methods — and keep `TorchSaveCheckpointStore` name or a thin alias for phase40 imports.

5. **strict-CPU path:** when flag is true, force `precision="float64"`, `device="cpu"` for `resolve_runtime` + `build_network` (and record that in frozen config / identity), not only global torch flags.

6. **RNG freeze contract:** freeze seed + maybe initial stream dump once at run start in a non-TrainingConfig artifact if needed; assert mid-run streams primarily on checkpoints. Adjust `41-05` AC wording to match.

7. **Nested config mapper tests:** unknown key under `run.guards.*`, partial nested section, defaults for nested ⚖ fields.

8. **Memory guard testability:** inject `memory_total_bytes` / signal callable; default 24 GB only as ⚖ platform default with provenance.

---

## 5. Overall Risk

**HIGH**

Rationale: Wave structure, threat models, and requirement coverage are strong enough that execution can succeed, but three load-bearing contracts — **CTX-53 payload shape**, **unclassified fail-safe resume**, and **phase40-compatible store/controller extension** — are currently underspecified or mutually inconsistent. Those are not polish items; they sit on the critical path for CTRL-03/05/08. Fix those before autonomous execute, or expect rework mid-wave-3/4.

---

## claude-max Review

I have read all five plans, the SPEC, and the CONTEXT, and spot-checked the plans' code-level claims against the live tree (all referenced symbols/line ranges and PyYAML 6.0.3 confirmed present; no existing `runs/` path handling exists). Here is the review.

---

# Phase 41 Plan Review — Config, Checkpointing, Resume & Determinism

## 1. Summary

Five plans decompose Phase 41 into a clean wave graph: 41‑01 (config + `atomic_io` + test scaffold) → 41‑02 (checkpoint store) ‖ 41‑03 (guards + determinism) → 41‑04 (controllers wiring) → 41‑05 (resume + `pinn.train` driver). File ownership is disjoint per plan, the change to `controllers.py` is strictly additive behind a Phase‑40 163/163 regression gate, and every owner‑carved value ships as a ⚖ provisional seam surfaced through `provisional_fields()`. The plans are unusually disciplined on scope boundaries and governance. My substantive concerns are integration seams *between* plans — chiefly who assembles the full checkpoint payload — plus an undefined run‑folder identity, not defects within any single plan.

Files read: all five `41-0N-PLAN.md`, `41-SPEC.md`, `41-CONTEXT.md`; concerns verified against the live `pinn/training/*.py`. Did not need PROJECT/REQUIREMENTS/ROADMAP/RESEARCH in full; all files readable.

## 2. Strengths

- **Boundary discipline (41↔42↔43).** Minimal step log only; canonical JSONL/TensorBoard, `summary.*`, `status.json`, and ⚖‑seam *calibration* explicitly deferred. The rationale (avoid a later widen/refactor of OPS‑03) is sound and consistently applied.
- **Governance hygiene.** Every D4‑a/R‑1/B‑5 value is provisional, registered, and enforced by prohibition tests; no ratified numeric is minted. This matches the project's strong "surface, don't invent" culture.
- **Security posture.** `yaml.safe_load` exclusively, `weights_only=True` at every load site with an `inspect.getsource` counter test, atomic tmp+fsync+`os.replace`+dir‑fsync, disk‑floor‑safe tiered `failure/` bundle, retention bounding disk. Per‑plan STRIDE registers are concrete.
- **Reuse‑first.** Promotes the verified 3‑site atomic‑write idiom into one primitive rather than a 4th copy; reuses `state_dict`/`resolve_runtime`/`StageExitMachine` seams instead of re‑implementing.
- **Correctness subtlety handled well.** The restore‑vs‑reseed distinction (exact continuation ≠ statistically‑equivalent restart) is identified and tested as two *distinct* invariants — a common determinism bug avoided by design.

## 3. Concerns

### HIGH
None that block planning outright, but concern **M1** is close to high — it can produce a runtime failure if not closed before 41‑04/41‑05 execute.

### MEDIUM

- **[M1] Full CTX‑53 payload composition is unassigned.** `RunController.state_dict()` returns `model/scheduled_weights/clipper` and, after 41‑04, `optimizer/rng/counters` — but **not** `curriculum`, `config_identity`, or `schema_version`. Yet 41‑04 Task 2 has the mid‑stage checkpoint hook "save a rolling checkpoint from `self.state_dict()`", and 41‑02's `fallback_scan` **rejects** any checkpoint missing those exact keys (its structural‑validity gate lists `config_identity`, `curriculum`, `schema_version`). As written, mid‑stage rolling checkpoints would lack `config_identity`/`schema_version`/`curriculum` → they fail `fallback_scan` on a corrupt `latest.pt` (yielding a false `NoValidCheckpointError` despite valid rollings), and `--resume` has no identity digest to compare. No plan clearly owns wrapping `state_dict()` with the run‑level keys + `CurriculumController` state at each save site. Assign this explicitly (a payload‑assembler in 41‑04 or injection in the store), and add a test that a *mid‑stage rolling* checkpoint is structurally complete.

- **[M2] Run‑folder `<name>` derivation and collision behavior undefined.** All plans write `runs/<name>/config.yaml`, `checkpoints/`, `curriculum.jsonl`, but neither CONTEXT nor any plan defines where `<name>` originates (config field? CLI arg? config hash?) or what happens if `runs/<name>/` already exists. A fresh launch into an existing folder could clobber a prior run's frozen config and checkpoints — a data‑integrity risk. Design‑doc §5.7 is cited but never pinned into a 41‑05 task.

- **[M3] Adam‑reset anchor sourcing is imprecise.** CTRL‑06 depends on `stage-{k+1}-init.pt` being serialized when `self._optimizer is None` (post stage‑factory swap). But the ADVANCE branch saves *both* anchors at the boundary; if the init anchor is serialized from the outgoing (stage‑k) controller, it carries stale Adam moments. 41‑04 Task 3 asserts the guarantee but leaves the save‑ordering vs the controller swap loose. Nail down which controller's state feeds the init anchor.

- **[M4] Seed fan‑out is a consequential decision made in a plan assumption.** 41‑05 fans `run.seed` into `ArchitectureSpec.seed`, and that seed is part of the identity digest that gates *every* resume and defines the D6 seed‑band semantics. CONTEXT does not resolve this (RESEARCH OQ1). The plan flags it ("do not silently diverge"), which is good, but unlike D4‑a/R‑1/B‑5 it is not surfaced as a ratifiable ⚖ seam. Given its blast radius (changing it later invalidates all prior checkpoints' digests), recommend surfacing for owner confirmation rather than adopting inline.

### LOW

- **[L1] `weights_only` prohibition guard is brittle.** The `count("torch.load")==count("weights_only=True")` check breaks on string/comment occurrences and cannot see cross‑module loads; 41‑01's scaffold also references a store class name 41‑02 chooses "at discretion" — a name drift makes the guard silently `SkipTest` forever. Real coverage lives in 41‑02's `test_checkpoint`, so this is belt‑and‑suspenders, but the class‑name coordination should be explicit.
- **[L2] Wall‑clock ceiling across resume undefined.** If `counters.wall_clock_baseline` is restored from an old checkpoint, `elapsed = now − baseline` could fire the ceiling immediately after resume. Harmless (one extra checkpoint) but the intended semantics (per‑session vs cumulative) should be stated.
- **[L3] Terminal‑stage knowledge for `promote()` beyond‑terminal refusal.** The generic store must know the terminal stage index to refuse promotion‑beyond‑terminal; it references `check_stage_preflight` but has no obvious handle to it in a Stage‑0‑only slice. Specify how the max stage reaches the store.
- **[L4] "per‑step" vs "per‑epoch" terminology.** Requirements say guards/checkpoints run "every step"; the wiring fires "once per epoch." Fine if step≡epoch in this full‑batch loop, but state the equivalence — L‑BFGS epochs run multiple closure evaluations, so "which iteration does the guard observe" should be unambiguous.

## 4. Suggestions

1. **Close M1 first:** add an explicit payload‑assembler (merge `RunController.state_dict()` + `CurriculumController` curriculum state + `config_identity` + `schema_version`) owned by one plan (41‑04 is the natural home, consumed by 41‑02's store and 41‑05's driver), and add a 41‑05 assertion that a *mid‑stage rolling* checkpoint passes the store's own structural validation.
2. **Pin the run‑folder contract (M2)** into a 41‑05 task: define `<name>` source and an explicit exists‑already policy (fail‑closed unless `--resume` targets that folder).
3. **Make the init‑anchor save‑order explicit (M3)** in 41‑04 Task 3 (e.g., "init anchor is serialized from the entered stage's fresh controller, after `self._optimizer` is reset/None"), and let the `AdamResetCompositionTests` assert the anchor payload's `optimizer` key is `None`.
4. **Surface the seed fan‑out (M4)** as a ⚖ decision line (like B‑5) so the owner ratifies single‑seed‑fanout vs two independent seeds before run #1, since it defines the identity digest.

## 5. Overall Risk

**MEDIUM.** The plans are well‑structured, security‑aware, and governance‑clean, with accurate grounding in the live code. Risk is concentrated in cross‑plan integration seams — the unassigned full‑payload composition (M1) and the undefined run‑folder identity (M2) — that are cheap to close now and expensive to discover at end‑to‑end execution (41‑05) or first real run. Resolve M1–M3 before executing Wave 3/4; M4 is a governance surface, not a build blocker.

---

## claude-kimi Review

Execution error
---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- status: preserved from existing REVIEWS.md

### grok
- reviewer=grok
- exit_code=0
- elapsed_seconds=104
- timeout_seconds=360
- watchdog=not_triggered
- command=grok --no-auto-update --no-memory --no-subagents --disable-web-search --permission-mode plan --output-format json -m grok-4.5 --prompt-file /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260718T052528Z-62777/xreview-prompt-41.md 
- grok_json_parse=ok
- grok_raw_stdout_bytes=13950
- stdout_bytes=10078
- stderr_bytes=0

### claude-max
- reviewer=claude-max
- exit_code=0
- elapsed_seconds=289
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-max --model claude-opus-4-8 -p - 
- stdout_bytes=8472
- stderr_bytes=0

### claude-kimi
- reviewer=claude-kimi
- exit_code=143
- elapsed_seconds=361
- timeout_seconds=360
- watchdog=triggered
- timeout_after_seconds=360
- command=ccp kimi -p - 
- stdout_bytes=15
- stderr_bytes=192
