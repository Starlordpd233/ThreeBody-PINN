# Trainex R1a — Stage-2 Consolidated Resolution (Final Recommended Decision Set)

**Date:** 2026-07-05 · **Channel:** build-design (recommendation only; the project owner ratifies)
**Consolidates:** `chatgpt-trainex-r1a-resolution.md` ("ChatGPT report"), `fable-trainex-r1a-adjudication-resolution.md` ("Fable report"), `glm-trainex-r1a-resolution.md` ("GLM report"), checked against the original sources (decision sheet `trainex-r1a-options-and-decisions.md`, depth report `chatgpt-pro-resolution.md`, specs `ctl_instruction.md` / `pinn_architecture.md`, baseline design, strategy assessment, and both r1b findings files).
**Tie-break rule used:** where the three reports diverged, the divergence was adjudicated against the attached specs and r1b findings — never by preference. Every tie-break below names its grounding. Where a diverged row is genuinely an owner-preference or empirical matter, it is **flagged for the owner** rather than decided.

---

## 0. How to read this consolidation

- "Sources agree/diverge" is judged against the three reports' recommendations for each row of the decision sheet (`trainex-r1a-options-and-decisions.md` §10), which all three treated as the operative prior default.
- **D1-p (precision, fp32 vs fp64)** is not decided anywhere in this document: every pick below holds under both branches (branch (i): PyTorch on `mps`, fp32 loop; branch (ii): identical code on `cpu`, fp64), per the round mandate.
- **B-8 (ε_H gate direction)** is settled by the attached spec, not adjudicated: `ctl_instruction.md` conservation gate — `eps_H = max_t |(H(t) − H(0))/H(0)|`, **REJECT if `eps_H > 1e-5`** (smaller passes), `eps_H = 0 → SCS = −inf → Excellent`. The baseline design doc's §6.3 inverted-looking example is a display slip (r1b C-12), fixed cosmetically with B-7. Note the glyph collision the spec itself calls out: this validation-gate `eps_H` is distinct from the training-loss denominator floor `eps_H = 1e-4·S_H` in `pinn_architecture.md` §3.4.
- **B-7** (cosmetic doc edit) and **B-12** (split-policy tension, routed to v1.5/PH-5; register U-4) are out of scope per the mandate.
- **⚖ thresholds** are filled in §3 only where the r1b files actually give a value; where they do not, the gap is recorded in the merged register (§4) — no value is invented.

One consolidation-level finding shapes several rows and is worth stating once: **the attached specs postdate the decision sheet (2026-06-12) and contain Phase 33–35 contracts the sheet never saw.** Two of the three reports (Fable, GLM) independently found the load-bearing drift — the ADVANCE / RECOVER / HALT-REVIEW stage-exit state machine (CURR-03), the canonical replay/lookahead batch contract closing SI-PINN-003 (LOOP-01/02/03), the loader-metadata requirement (LOOP-06), and the instrumentation mandate in LOSS-02. The Fable report additionally found that the spec now supplies **verified snapshot-count medians (61 standard-base / 127 hierarchical-base / 1003 gold)**, which partially closes the sheet's biggest open number (U-1). All of these were re-verified against `ctl_instruction.md` during this consolidation and are adopted below.

---

## 1. Final resolution summary

| # | Decision | Final recommended pick | Sources | Conf. | Timing |
|---|---|---|---|---|---|
| D1 | ML framework | **PyTorch 2.12 + MPS** (branch (ii): same code, `device="cpu"`, fp64) | Unanimous endorse | High | Needed now (one-way) |
| D1-p | Precision branch | *Not decided — owner-carved; all picks hold under both branches* | n/a | n/a | — |
| D2 | Tracker / monitor | **JSONL log canonical; TensorBoard as secondary view in `runs/<name>/tb/`; one end-of-run plot script** | Unanimous endorse | High | Needed now (plot script deferrable) |
| D3 | Data residency | **D3-C auto-selector defaulting to full in-memory fp32 preload (D3-A behavior); `num_workers=0`; watermark 0.7 knob; `mem:` log line; + adapter exposes `n_snapshots`/`dt_out` metadata (LOOP-06) and loads only the Step-1A admitted set** | 2 endorse-C / 1 override-to-A; substance converges on in-memory | High (interface + Stage-0 in-memory) / Medium (auto stays in-RAM at later cumulative stages) | Adapter interface needed now; residency two-way |
| D4-a | Checkpoint cadence & retention | **Retention: rolling-3 + `best.pt` + stage anchors + `latest.pt` copy (endorse). Cadence: OVERRIDE — dual trigger, every 1000 steps *or* a wall-clock ceiling, whichever first; ceiling value open (r1b range "e.g. 15–30 min")** | Diverged (endorse / conditional add / dual-trigger override) → **owner look: ceiling value** | High (structure); ceiling open | Needed now |
| D4-b | Corruption safety | **Atomic tmp+fsync+rename; fallback scan; `weights_only`-clean checkpoint contents** | Unanimous endorse | High | Needed now |
| D4-c | Auto-guard tier | **Tier 1+2 on; three loop seams built now; + spec-drift amendment: RECOVER seam (default `recover.retries: 0`) and HALT/REVIEW guard family (placeholder thresholds); Tier-3 auto-LR remediation still excluded; ⚖ values left as placeholders** | Tiers unanimous; CURR-03 amendment in 2 of 3 → **owner look: RECOVER↔guard boundary + retry budget after pilot** | Medium | Seams needed now; toggles two-way |
| D4-d | Diagnostic bundle | **Always on (+ one-line README in `failure/`)** | Unanimous endorse | High | Needed now |
| D5-a | Loop shape | **D5-B two-phase closure loop; full-batch as accumulate-in-closure; + preflight refuses sL-BFGS stages (3–6) until an implementation exists** | Unanimous endorse (guard added by one report; adopted as additive) | High | Needed now (one-way) |
| D5-b | Collocation infrastructure | **D5-E sampler interface (uniform + spec adaptive) with the stateful-hook signature** | Unanimous endorse | High | Interface needed now (one-way) |
| D5-c | Loss-weight machinery | **D5-H scheduled-weights module (checkpointed state) + empty rebalance seam** | Unanimous endorse | High | Interface needed now (one-way) |
| D6 | Determinism policy | **B+C: accepted-variance + full seed/RNG record in config+checkpoints + strict-CPU debug switch; seed band calibrated by 2–3 stage-0 pilot repeats** | Unanimous endorse | High (policy); band empirical; margin is owner preference | Seed schema needed now |
| D7-a | Boundary checkpoints | **Dual anchors `stage-{k}-final.pt` + `stage-{k+1}-init.pt`, excluded from rolling deletion** | Unanimous endorse | High | Needed now (one-way) |
| D7-b | Optimizer at boundary | **Complete Adam reset (spec "Critical"); no partial-carry support** | Unanimous endorse | High | n/a (spec-fixed) |
| D7-c | Rollback policy | **Manual `--resume …/stage-{k}-final.pt --hold-stage` now; D7-D auto-revert deferred until a divergence signal exists (Stage-2/R1b join); RECOVER (NaN/Inf) is a distinct, spec-side mechanism handled at D4-c** | Unanimous on C-now/D-later; boundary clarification in 2 of 3 → **owner note: RECOVER↔D7-D boundary** | Medium | C needed now; D deferrable |
| D7-d | Mid-promotion crash | **Idempotent ordered promotion + `curriculum.jsonl`; extended to record all three CURR-03 dispositions (promotion / RECOVER / HALT)** | Unanimous endorse (extension in 1 of 3; adopted as additive) | High | Needed now (one-way) |
| B-1 | PH-7 optimizer default | **Replace with the `ctl_instruction.md` Phase-2 stage-0 schedule** | Unanimous endorse | High | Needed now |
| B-2 | Committed log fields | **Widen to 5 terms + total + λ vector + grad-norm; + causal-weight `w_n` stats as scalars now; per-time-bin residual panel early (r1b D-9/DRO-5)** | Unanimous endorse (+extension in 2 of 3, adopted) | High | Needed now (panel deferrable-to-early) |
| B-3 | Controller naming | **Name `CurriculumController` / `RunController`** | Unanimous endorse | Medium (taste-adjacent) | Free at skeleton time (two-way); mild owner preference |
| B-4 | Placeholder inventory | **Extend per sheet + RECOVER/HALT mechanics, wall-clock cadence ceiling, validation-cadence knob, D-9 surfaces** | Unanimous endorse (+extensions) | High | Deferrable (docs); the validation-cadence knob's *existence* is needed-now (D5 fact) |
| B-5 | Resume config-diff rule | **Field-classified diff; unclassified fields default to identity (refuse) — fail-safe** | Unanimous endorse (fail-safe in 1 of 3; adopted) → **owner ratifies the field list** | Medium | Needed now (settle before run #1) |
| B-6 | Run-folder members | **Adopt additive list + environment fingerprint (`sw_vers`, `python -V`, framework build, lockfile hash) per r1b D-12** | Unanimous endorse (+D-12 in 2 of 3, adopted) | High | Needed now (before runbook) |
| B-9 | Config approach | **Single YAML keyed `stage/opt/loss/run`; frozen resolved copy in the run folder** | Unanimous endorse → **owner attention: R-4 spec ambiguity (Hydra named twice, once unmarked)** | High for the slice; partly owner tooling preference | Needed now (schema) |
| B-10 | Sleep wrapper | **`caffeinate -is <cmd>`; lid-open + AC rule; SIGTERM treated as one Ctrl-C** | Unanimous endorse (+r1b doctrine folded in) | High | Needed now |
| B-11 | Reproducibility wording | **Re-scope to statistical equivalence + exact checkpoint continuation** | Unanimous endorse | High | Doctrine now; doc edit deferrable |
| B-8 | ε_H gate direction | *Spec-settled: smaller passes (see §0). Implement as such; fix the design-doc §6.3 slip with B-7* | n/a (closed) | — | — |

---

## 2. Per-decision consolidation notes

Only the substance needed to justify each final pick, its agreement/divergence adjudication, and its flags. All three reports converged on the large majority of rows; divergences and amendments are adjudicated explicitly.

### D1 — ML framework → **PyTorch 2.12 + MPS** (fp64 branch: same code on CPU)
**Agreement:** unanimous endorse, on the same grounds: the only candidate that (a) uses this machine's GPU, (b) ships the spec-mandated L-BFGS (`torch.optim.LBFGS`, strong-Wolfe; MLX ships none — F11), (c) matches the spec's own illustrative AD patterns and §10 probes (PHYS-02), and (d) minimizes searchable-help friction. JAX's supported path on this machine is CPU-only (jax-metal effectively unmaintained — F12, r1b DRO-1/D-2). **Confidence: High.** Biggest shared uncertainty: U-9 (MPS double-backward kernel coverage for this exact net) — adjudicated empirically by the §10.3 probe run on-device with `PYTORCH_ENABLE_MPS_FALLBACK` **unset** as the first build act; the fp64-CPU branch is the in-framework escape. Two reports carry the sheet's practical note (jacfwd `as_strided` MPS bug through 2.7.0, past at 2.12; prefer/verify the actual AD pattern), and two carry r1b D-4 (scalar-`u` forward-mode AD is an order-of-magnitude cost lever the PHYS-02 "equivalent full-Jacobian" clause admits — time both patterns in the probe). **Timing:** needed now (one-way). **Nature:** research-settled at the framework level; the device consequence is the owner's D1-p call.

### D2 — Tracking/monitoring → **JSONL canonical + TensorBoard view + one plot script**
**Agreement:** unanimous endorse. The JSONL-as-source-of-truth rule is what keeps the tracker a two-way door; TensorBoard is spec-named (`ctl_instruction.md` Implementation Notes) and first-party for D1; W&B-offline stays disqualified for a no-cloud project (F14); MLflow adds a second metadata store (F15). TB events homed in `runs/<name>/tb/` (B-6). **Confidence: High. Timing:** needed now (JSONL + TB writer); the end-of-run PNG script is deferrable. **Nature:** research-settled.

### D3 — Data residency → **D3-C auto-selector defaulting to in-memory fp32 preload, `num_workers=0`, watermark 0.7, `mem:` line; + two spec amendments**
**Divergence and adjudication:** Fable and GLM endorse the sheet's D3-C; ChatGPT overrides to plain D3-A (in-RAM only, streaming deferred) on thin-slice grounds. The *behavior for the Stage-0 slice is identical in all three* — full in-memory fp32 preload, no worker processes — so the only real delta is whether the residency selector (a config key) exists. Tie-break by the attached specs and r1b: (1) the current `ctl_instruction.md` supplies verified snapshot-count medians (61/127/1003; "population medians, not hard per-file guarantees"), from which the whole 15,028-trajectory corpus is ≈ 6.2 M snapshots ≈ **0.55 GB fp32 / 1.1 GB fp64** (Fable's derived arithmetic, re-verified here against the spec's dataset Table: base sets 4,857 + 4,857; gold sets 2,749 + 2,565) — far below the sheet's ~6–8 GB streaming threshold; (2) r1b independently estimates total steady-state training memory at 2–7 GB, "comfortably inside 24 GB" (§1.6), and calls memory "a monitoring nicety" (K4.2); (3) the stage-2 full-batch L-BFGS risk r1b flags (D-7) is an autograd-graph question answered by D5-a's accumulate-in-closure, not a dataset-residency question. So streaming-first (the depth report's §6.7 stance) is over-build, and the selector — the sheet's own two-way hedge, essentially free — is kept in case per-stage cumulative bytes ever surprise. ChatGPT's substantive point (simplest possible Stage-0 data path) is fully preserved. Adopted amendments (Fable, spec-grounded): the adapter exposes `n_snapshots(traj)`/`dt_out(traj)` metadata (LOOP-06 requires it) and loads only the **admitted** set, logging Step-1A's admitted/rejected/quarantined counts. **Confidence:** High on the interface and the Stage-0 in-memory verdict; Medium that `auto` lands in-RAM for every later cumulative stage (per-stage bytes come from the strategy doc's Thrust-A scan). **Timing:** adapter interface (+ metadata fields) needed now (mild one-way, the baseline's own seam); residency policy two-way. **Nature:** partly empirical (per-stage bytes); the residual auto-vs-plain-A choice is a trivial config matter the owner can ratify with the set.

### D4-a — Cadence & retention → **retention endorsed; cadence OVERRIDDEN to a dual trigger (steps or wall-clock, whichever first)**
**Divergence and adjudication:** all three endorse B-retention (rolling-3 + best + anchors + latest-copy; ~110 MB/run disk math). On cadence they split three ways: ChatGPT endorses step-1000 as-is (cadence "empirical"); GLM endorses with a *conditional* wall-clock addition (add if the smoke test shows t_step ≳ 1 s); Fable overrides to an unconditional dual trigger. Tie-break by r1b's own words (§1.8): worst-case lost work is `checkpoint_every × t_step` — 100 s at 0.1 s/step but **83 minutes at 5 s/step**, inside the credible envelope since t_step is unknown across a ~30× range; "a wall-clock-based cadence (e.g., every 15–30 min) is **robust across the whole envelope**; a step-based default is only safe after t_step is measured" — plus DRO-6 and the depth report's independent §7.4/7.9 hybrid. The dual trigger is the reading that is robust *before* measurement and costs one config key; if t_step turns out small, the wall-clock trigger simply rarely fires first (GLM's condition is thereby subsumed). This is the one sheet default all evidence sources argue against; the sheet "kept" it without engaging its own companion evidence. **Confidence:** High on structure. **⚠ Owner look:** the ceiling *value* is an owner pick informed by the smoke-test's measured s/step; r1b grounds only the "e.g. 15–30 min" range — not filled here. **Timing:** needed now. **Nature:** structure research-settled; ceiling value owner+empirical.

### D4-b — Corruption safety → **adopt (atomic writes + fallback scan + `weights_only`-clean contents)**
**Agreement:** unanimous. Free robustness; keeps the runbook free of `add_safe_globals` incantations (F8); shared by ordinary, wall-clock, guard-emergency, and anchor writes. Optional cheap addition (depth report, via Fable): record checkpoint checksums in `status.json`/`curriculum.jsonl` if it costs a line. **Confidence: High. Timing:** needed now. **Nature:** research-settled.

### D4-c — Auto-guards → **Tier 1+2 on; three seams built now; + RECOVER seam (retries default 0) and HALT/REVIEW guard family; Tier-3 remediation still excluded; ⚖ placeholders**
**Divergence and adjudication:** the tiers, seams, and ⚖-as-placeholders are unanimous. Fable and GLM both found the spec-drift the sheet could not have known: `ctl_instruction.md` Phase 33 (CURR-03) defines the stage-exit decision as **ADVANCE / RECOVER / HALT-REVIEW**, where RECOVER — "rolls back to the last well-formed checkpoint and retries with a bounded retry budget" on NaN/Inf — is *spec-assigned loop behavior*, partially contradicting the sheet's Tier-3 framing ("auto-rollback-and-retry = science-adjacent, operator's job"). ChatGPT registered only the adjacent fact (fallback advancement rejected) and missed the RECOVER implication. The two findings differ in instantiation: GLM says RECOVER should be "always-on from day 1" but names no budget and flags the boundary for the owner; Fable builds the RECOVER *seam* now with `recover.retries: 0` as the default — behaviorally identical to the sheet's Tier-1 stop-and-preserve until the Stage-0 pilot calibrates a budget (the spec itself declares retry limits "provisional pending Stage-0 pilot calibration"). **Consolidated:** Fable's instantiation, because it implements the spec's *structure* without inventing its *provisional values* — exactly the round's discipline — and degrades gracefully to the sheet's Tier-1 if the owner reads RECOVER as deferred for the slice. Also adopted: the HALT/REVIEW guard family (per-stage max-epoch / stagnation halts) with placeholder or disabled thresholds, and `curriculum.jsonl` disposition records (D7-d). Tier-3 auto-LR mutation remains excluded — the spec mandates rollback-retry, nothing more. **Confidence: Medium** (all three said Medium). **⚠ Owner look:** (a) confirm the RECOVER↔external-guard boundary reading; (b) ratify the retry budget and HALT thresholds after the Stage-0 pilot. **Timing:** seams needed now; toggles/thresholds two-way. **Nature:** ⚖ values empirical/Stage-2; RECOVER budget owner-ratified post-pilot.

### D4-d — Failure diagnostic bundle → **always on** (+ one-line README)
**Agreement:** unanimous. The runbook step becomes literally "zip `runs/<name>/failure/` and ask for help" (r1b K3's pre-decided evidence package). **Confidence: High. Timing:** needed now. **Nature:** research-settled.

### D5-a — Loop shape → **D5-B two-phase closure loop; accumulate-in-closure; + preflight refusal of sL-BFGS stages**
**Agreement:** unanimous endorse. Spec-mandated structure (Adam→L-BFGS per stage, plateau handoff, complete Adam reset, frozen-λ and no-clip during L-BFGS); the closure is the single seam D4's guards, D7-d's promotion, and the spec's RECOVER all hang off; accumulate-in-closure is the structural answer to r1b D-7 (a literal full-batch second-order graph over the cumulative stage-2 set would exceed 24 GB). The depth report's "small state machine" is substantively D5-B plus the seams already adopted. Adopted addition (Fable, additive): preflight refuses to enter stages 3–6 until a concrete sL-BFGS implementation exists — converting U-7 from a silent science deviation into a typed stop (out of the slice's path regardless; stages 0–2 are full-batch). **Confidence: High.** Biggest uncertainty: closure wall-time for full-batch phases (R1b duration lane; watch the first L-BFGS phase). **Timing:** needed now (one-way). **Nature:** research-settled; sL-BFGS ownership (U-7) remains an owner scheduling / spec-renegotiation item.

### D5-b — Collocation infrastructure → **D5-E sampler interface with the stateful-hook signature**
**Agreement:** unanimous. Spec-aligned: LOOP-03 explicitly defers a mandatory 50/50 continuous collocation sampler ("the current uniform/adaptive collocation choices remain usable"); the near-free `(model, last_residuals)` hook signature is the hedge for later RAD-style machinery. `n_col` is a provisional/example budget (LOOP-02) — R2's number. **Confidence: High. Timing:** interface needed now (one-way); strategies/densities two-way. **Nature:** research-settled (densities empirical/R2).

### D5-c — Loss-weight machinery → **D5-H scheduled-weights module + empty rebalance seam**
**Agreement:** unanimous. PHYS-05 makes weights scheduled (warmup `I_warm = min(2000, 0.1·N_Adam,k)`, per-stage λ^max with `λ_E^max ≤ 1`, frozen during L-BFGS, re-warmed at boundaries); static weights fail the spec. LOSS-02 both mandates the very instrumentation B-2 adopts and defers automatic dominance reweighting — vindicating the empty seam staying empty. Module state serialized into checkpoints so resume restores mid-warmup exactly. **Confidence: High.** U-6 (causal-weight underflow clip bound) is left open by the spec's explicit instruction; set at implementation with a logged rationale. **Timing:** interface needed now (one-way). **Nature:** research-settled.

### D6 — Determinism → **accepted-variance + full seed/RNG record + strict-CPU debug switch; pilot-calibrated seed band**
**Agreement:** unanimous. Grounded in F6 (official PyTorch doctrine) and F7 (MPS nondeterminism despite full seeding + ~7× deterministic-flag slowdown): strict-always would pay the cost without securing the property. The depth report's two-tier framing maps onto B+C (CPU acceptance lane ≡ the strict debug switch + r1b's fp64-CPU ladder rungs; "≥3 paired seeds for consequential A/Bs" ≡ the seed-band protocol with an explicit count — adopt as the floor for load-bearing comparisons). **Confidence: High** on policy; the band itself is **empirical** (2–3 stage-0 pilot repeats); the confirmatory seed count for future A/Bs is an **owner** call at the margin. **Timing:** seed/RNG block in config+checkpoint schema needed now (mild one-way).

### D7-a — Boundary checkpoints → **dual anchors, excluded from deletion**
**Agreement:** unanimous. Makes the spec's "checkpoint at each stage completion" distinguishable and gives boundary crashes an unambiguous twin. **Confidence: High. Timing:** needed now (one-way naming). **Nature:** research-settled.

### D7-b — Optimizer at boundary → **complete Adam reset (spec-mandated); no partial carry**
**Agreement:** unanimous; not genuinely open (`ctl_instruction.md`: "**Critical**: Completely reset Adam's internal state"). L-BFGS history never crosses a boundary. **Confidence: High. Nature:** spec-fixed.

### D7-c — Rollback → **manual `--hold-stage` command now; D7-D auto-revert deferred**
**Agreement:** unanimous on C-now / D-later. Adopted clarification (Fable + GLM): the spec's RECOVER covers *numerical* failure (NaN/Inf; handled at D4-c) and is **not** D7-D's *divergence-quality* auto-revert, whose trigger signal is genuinely absent from r1b (the K1 watchlist's "per-term curves resume a downward trend within ~2,000 steps" is a watch heuristic, not a guard trigger); with no validated signal, auto-revert can reject valid hard-stage behavior. **Confidence: Medium** (2 of 3). **⚠ Owner note:** the RECOVER↔D7-D boundary reading, same as D4-c. **Timing:** C's command needed now; D deferrable. **Nature:** D's signal empirical (Stage-2/R1b join); enabling it is then an owner policy call.

### D7-d — Mid-promotion crash → **idempotent ordered promotion + `curriculum.jsonl`, recording all three dispositions**
**Agreement:** unanimous on the ordered write + jsonl reconciliation ("resuming never re-asks what stage am I in"). The depth report's heavier transactional journal (hashes, branch-on-rollback) reaches the same crash semantics; under the viability-slice lens its extra machinery is deferred (adjudicated identically by Fable and GLM; ChatGPT concurs by endorsing the sheet's lighter form). Adopted extension (Fable, additive): `curriculum.jsonl` records RECOVER and HALT/REVIEW events too, giving CURR-03 its audit trail and the operator one file for "what stopped my run." **Confidence: High. Timing:** needed now (one-way artifact contract).

### B-1 → **replace PH-7's default with the spec's stage-0 schedule.** Unanimous; keeping the baseline default would run the first trial silently off-spec (LR `1e-3 × 0.7^k`, cosine, two-phase, curriculum-aware median clipping C = 7–10 at stages 0–1 with the exact early-stage value left open by the spec itself, no clipping during L-BFGS). **High · Needed now · spec-conformance.**

### B-2 → **widen to 5 terms + total + λ vector + grad-norm; + `w_n` stats now; per-time-bin residual panel early.** Unanimous on the widening (spec Implementation Notes + LOSS-02 mandate + r1b DRO-5); the r1b D-9 extension (causal-weight statistics; residual-vs-time panel) is what makes causal-weight collapse and propagation failure — two of the watchlist's highest-value silent failures — observable at all; adopted by two reports and consistent with the third's "add watchlist signals as soon as practical." **High · scalars needed now; panel early (before the first long unattended run).**

### B-3 → **name `CurriculumController` / `RunController`.** Unanimous adopt; confidence labels split (Medium/Medium/High) — consolidated **Medium**: taste-adjacent internal naming whose value is giving the runbook nouns, strengthened now that CURR-03 dispositions and the guards have owners. **Free at skeleton-writing time · two-way · mild owner preference.**

### B-4 → **extend the placeholder inventory** per the sheet, plus this round's additions (RECOVER/HALT mechanics + provisional thresholds; the wall-clock ceiling; the D-9 monitoring surfaces). Unanimous. **High · deferrable as documentation** — except the validation-cadence knob's *existence*, a needed-now D5 skeleton fact (U-5).

### B-5 → **field-classified resume diff, with unclassified-fields-default-to-identity fail-safe.** Unanimous on classification; the fail-safe (Fable) is adopted as a strict safety improvement (misclassification or schema additions fail safe rather than silently resuming across a semantic change). **Medium** (classification is judgment applied before the schema fully exists). **⚠ Owner ratifies the identity/operational field list before run #1. Needed now (soft one-way).** Nature: partly owner — the identity list encodes risk tolerance.

### B-6 → **adopt the additive run-folder list + the r1b D-12 environment fingerprint** (`sw_vers`, `python -V`, framework version/build, lockfile hash) — without it the (re-scoped) "give a colleague the folder" promise doesn't hold and upgrade re-validation has nothing to diff. Unanimous (+2 of 3 on D-12; adopted). **High · needed now (adopt the final member list before the runbook is written).**

### B-9 → **single YAML keyed `stage/opt/loss/run`, frozen resolved copy in the run folder.** Unanimous. Consolidation honesty note (Fable, verified here): Hydra appears **twice** in `ctl_instruction.md` — under the "Ignore Now and Come Back Later" heading *and* in the Implementation Notes bullet, which carries no such marker (also r1b D-14). The engineering conclusion stands regardless — the strategy assessment defers reproducibility provenance, the keyed structure makes a later Hydra migration mechanical, and the load-bearing property (resolved config frozen into the run folder) is preserved — but the duplication is a spec-owner reconciliation item (register R-4). **High for the slice · needed now (schema) · partly owner tooling preference. ⚠ Owner attention: R-4.**

### B-10 → **`caffeinate -is <cmd>`; lid open + AC for the whole run; SIGTERM ≡ one Ctrl-C.** Unanimous, grounded in both r1b files (K2 §4.1 / K2.1, DRO-2/3, D-10): `-d` prevents only display sleep; on Apple Silicon + macOS 15+, lid-close forces sleep that neither `caffeinate` nor `pmset disablesleep` overrides — recovery is checkpoint-resume, not wake-and-hope. **High · needed now.**

### B-11 → **re-scope the reproducibility promise** to "re-run to statistical equivalence from recorded config+seed; exact continuation from any checkpoint; not bitwise re-creation." Unanimous (F6/F7). **High · doctrine now; doc edit deferrable.**

---

## 3. ⚖ thresholds — the Stage-2 fill

Per the round contract: take values from the attached r1b findings where they give one; record every ⚖ the r1b files do **not** specify. All three source reports independently audited this and agree; re-verified here by direct search of both r1b files.

| ⚖ item (decision sheet) | r1b value? | Stage-2 disposition |
|---|---|---|
| Loss-explosion kill switch: multiple of trailing median + consecutive-log window (D4-c Tier 1) | **No number anywhere in r1b** | **Remains a placeholder** — register R-1. Do not invent; calibrate against the Stage-0 pilot's observed loss variance. |
| Disk-floor guard: GB free (D4-c Tier 1) | **No fixed number in r1b** (the depth report argues a *formula-based* floor — temp file + retained files + reserve — a shape, not a value) | **Remains a placeholder** — register R-1. The formula shape is a reasonable implementation basis; its reserve constant is still a project pick. |
| Memory-watermark guard: multiple of the D3 cap + consecutive-log window (D4-c Tier 2) | **No number in r1b** (r1b's memory analysis explicitly calls memory "a monitoring nicety, not the feasibility question") | **Remains a placeholder** — register R-1. Related but distinct: the D3 watermark *fraction* 0.7 is the sheet's default knob, also not an r1b value. |

Adjacent values the r1b files **do** ground (recorded so Stage-2 doesn't confuse them with the ⚖ slots): the wall-clock checkpoint cadence range "e.g., every 15–30 min" (§1.8 — used for D4-a's ceiling *range*, value still an owner pick); the hang heuristic "step number frozen ≥ 5 min" (K1 watchlist) — note the sheet's 10-minute `status.json` heartbeat rule is the sheet's own runbook proposal, not an r1b number; and the smoke test's role as the instrument that converts the whole duration envelope, and hence these calibrations, from parameterized to measured (D-5/DRO-9).

---

## 4. Merged claims-and-uncertainty register

Carried from the sheet with status updates; new items R-numbered. Nothing here is asserted as fact; every open number stays open.

| ID | Item | Merged status |
|---|---|---|
| U-1 | Snapshots/trajectory; per-stage cumulative bytes (controls D3) | **Partially closed by the attached spec** (found by the Fable report; verified here): `ctl_instruction.md` supplies verified snapshot-count medians — 61 standard-base / 127 hierarchical-base / 1003 gold ("population medians, not hard per-file guarantees") — and Step-1A's completeness gate bounds `final_timestep ≥ 9.5`. Derived corpus estimate ≈ 6.2 M snapshots ≈ **0.55 GB fp32 / 1.1 GB fp64** (using the spec's dataset Table set assignments). Supports in-memory. **Still open:** exact per-stage cumulative bytes (stage populations from the Thrust-A scan); the medians' spread. The ChatGPT and GLM reports carried U-1 as fully open — superseded. |
| U-2 / U-15 | M5-class step times, thermal envelope, run durations | Open; no near-workload benchmark exists in the sources (r1b C-9). The rung-6 smoke test is the designated measurement; durations deliberately not estimated. |
| U-3 | ε_H gate direction | **Closed** (spec-settled smaller-passes; design-doc §6.3 slip is cosmetic → B-7, out of scope). |
| U-4 | Split-policy tension (global 80/10/10 vs per-stage cumulative 10–20% hold-out) | Open; routed to v1.5/PH-5 (B-12, out of scope). Stage-stratified global split remains the compatible reading. |
| U-5 | Validation-evaluation cadence | **Still open in the current spec** — the ADVANCE criteria consume `L_val(i)` but no document states how often validation runs. Knob's existence adopted (D5 skeleton fact); value is R2/owner. |
| U-6 | Causal-weight underflow clip bound | Open by the spec's explicit deferral (LOSS-04). Set at implementation with a logged rationale. |
| U-7 | Stochastic L-BFGS algorithm/ownership | Open; no framework ships it (F11/F13; torch's LBFGS assumes a consistent objective). Preflight-refusal guard adopted (D5-a) so the gap cannot be crossed silently; owner must schedule implementation or renegotiate at spec level before stage 3. |
| U-8 / U-10 | MLX fp64-CPU coverage; MLX/Metal determinism | Moot under the D1 pick; carried unchanged. |
| U-9 | MPS double-backward kernel coverage for this net | Open until the §10.3 probe runs on-device with fallback **unset** (first build act). |
| U-11 | Referenced-but-unattached materials | Updated: the SCS gate and SASD/IPR/PSC contracts are now present in the attached `ctl_instruction.md`. Still unattached: `sampling_method.md` (out of scope), the Phase-18 FRAME-01 preprocessing doc, v1.5 PIPE-XX format/hash mechanism, the §10 probe scripts. Treated as unavailable; nothing above depends on them. |
| U-12 | `data_version_hash` production mechanism | Open (v1.5 PIPE-XX); the adapter implements compare-and-refuse only. |
| U-13 | TensorBoard release pin | Open; pin at install time. |
| U-14 | SI-PINN-003 batch-construction inconsistency | **Closed by the current spec** (Phase 34: `ctl_instruction.md` Mini-Batch Construction is canonical). Found independently by the Fable and GLM reports. |
| R-1 | **⚖ guard thresholds r1b does not number** | Loss-explosion multiple + window; disk-floor GB; memory-watermark multiple + window; post-promotion divergence signal (qualitative watch heuristic only). All remain Stage-2 placeholders — see §3. |
| R-2 | RECOVER retry budget; HALT/REVIEW max-epoch table and stagnation window | Provisional **by the spec's own declaration** (CURR-03; issue-doc epoch tables claimed-unverified). Seams built now; `recover.retries: 0` and placeholder HALT values until the Stage-0 pilot; then owner-ratified. |
| R-3 | Hardware confirmation | Both r1b files flag that no shipping M5 Pro matches the project docs' "16 CPU / 15 GPU" (Apple: 15/16 base or 18/20; 24 or 48 GB). Changes no recommendation (~24 GB honored as stated), but the owner should confirm the actual part — especially 24 vs 48 GB — before Stage-2 threshold setting. |
| R-4 | Hydra ambiguity in the spec | Named both under "Ignore Now and Come Back Later" **and** in the unmarked Implementation Notes (also r1b D-14). Keyed-single-YAML hedge recommended regardless; spec owners should reconcile the duplication. |
| R-5 | Decision sheet's D3 set-labeling slip | The sheet's §3.1 swaps which sets are gold (it lists 4,857 as `hierarchical_gold`; the spec's Table assigns 2,749 to Set 2a hierarchical @ dt 0.01, and 4,857 to Set 1b standard @ 0.17). Total 15,028 unchanged; the sheet's memory bracketing was conservative. Cosmetic; Stage-2 arithmetic here uses the spec's Table. (Found by the Fable report; verified.) |
| R-6 | fp32 achievability of the §10.3 tolerance | The spec's `relative_error < 1e-6` may be marginal for fp32 second derivatives on GPU (r1b C-6). The dual-arm scheme (fp64-CPU reference; fp32-device within ~1e-4 of it) is a **tolerance ruling the owner must ratify** as part of D1-p — not decided here. |
| R-7 | Divergence-derived owner items | (a) D4-a wall-clock ceiling value (owner pick in r1b's 15–30 min range, informed by measured s/step); (b) D4-c/D7-c RECOVER↔guard boundary reading + post-pilot retry budget; (c) B-5 identity/operational field list; (d) B-9 tooling taste + R-4; (e) D3's later-stage residency check once per-stage bytes exist. |
| R-8 | Assumptions | The four consolidated bundles faithfully contain the eight originals (asserted by their headers; content-consistent). The decision sheet is the operative prior default; the depth report's divergences (D3 residency, D4 cadence, D5 shape, D6 shape, D7 weight) were adjudicated explicitly. Where the two r1b files differ in secondary numbers (e.g., 7-vs-9 curriculum segments), ranges are carried, not resolved. |

---

## 5. Composed first-run recipe (coherence check that the final set works together)

**Step 0 — before any training code:** run the strategy assessment's **Thrust-A data scan** (bin the admitted trajectories by the difficulty invariants; count stage populations, Stage 0 above all). Almost no machinery; supplies the per-stage cumulative byte counts that settle D3's `auto` verdict and flags the fatal-class risk of an under-populated Stage 0.

**Setup (once):** Miniforge3 → `conda create -n pinn-train python=3.11` → `pip install torch tensorboard pyyaml numpy h5py` → verify `torch.backends.mps.is_available()` → export the environment pair (loose `environment.yml` + lockfile / `pip freeze`) per r1b K2.3.

**Pre-flight (r1b ladder; no run > 30 min without it green):** rungs 0–3 as a `verify` script — device sanity; the **§10.3 componentwise-AD probe on `mps`/fp32 with `PYTORCH_ENABLE_MPS_FALLBACK` unset**, plus the fp64-CPU reference arm (this simultaneously certifies the AD contract, times both AD patterns per r1b D-4, and feeds the owner's D1-p adjudication); fp64-CPU gradcheck; residual-on-ground-truth + the remaining §10 probes. Then rung 4 (single-trajectory overfit) and rung 6 — the **~5-minute smoke test** (≈32 stage-0 trajectories, ~300 steps, checkpoint_every=100): verifies the whole mechanical surface, exercises Ctrl-C/resume, and **records s/step**, collapsing the ~30×-wide duration envelope into a per-run forecast and informing the D4-a ceiling.

**Configure** — one keyed YAML (B-9):

```yaml
run:   { name: first-run, seed: 1234, device: mps, precision: float32,
         max_steps: 100000, log_freq: 100,
         checkpoint_every: 1000, checkpoint_wallclock_min: <owner pick; r1b range 15-30>,
         guards: { nan: true, loss_explosion: true, disk_floor: true,
                   memory_watermark: true, halt_review: placeholder },  # ⚖ values pending (see §3)
         recover: { retries: 0 } }                                      # CURR-03 seam; budget pending pilot
stage: { start: 0, data_version: <from v1.5 PIPE-XX>, residency: auto } # D3-C
opt:   { schedule: ctl-phase2, stage0_lr: 1.0e-3, anneal: cosine,
         lbfgs: { history: 10, line_search: strong_wolfe, max_iter: 20 } }  # B-1 / D5-a
loss:  { weights: phys05-warmup, collocation: { strategy: uniform, n_col: 2048 } }  # D5-c / D5-b
```

**Launch:** `caffeinate -is python -m pinn.train --config configs/runs/first-run.yaml` — lid open, AC power, hard flat surface (B-10). Startup prints: device + `mem cap: … (0.7×)`; Step-1A admission counts (admitted/rejected/quarantined); data + residency line; environment fingerprint; `Stage 0 of 7`. Then one line per 100 steps with **five loss terms + total + lr + λ vector + grad-norm + w_n stats + s/step + ETA** (B-2), a `mem:` line each 1,000 steps (D3), and a `status.json` heartbeat. Secondary view: `tensorboard --logdir runs/` (D2). Mac-side: Activity Monitor swap flat; GPU% judged against the smoke-test baseline, not an absolute band (r1b D-11).

**Stage-0 shape:** Adam with PHYS-05 warmup → plateau handoff → full-batch L-BFGS via accumulate-in-closure (D5-a) → four ADVANCE criteria at the validation cadence (knob exists; value = U-5) → on promotion: `stage-0-final.pt`, `curriculum.jsonl` promotion record, fresh Adam, re-warmed λ, `stage-1-init.pt` (D7). NaN/Inf → the RECOVER seam at `retries: 0` ⇒ emergency checkpoint + `GUARD: non-finite loss` + `failure/` bundle (identical to Tier-1 stop until the pilot calibrates a budget). Max-epoch/stagnation → `HALT: <trigger>` for owner review (placeholder thresholds). One Ctrl-C or SIGTERM = graceful checkpoint.

**Resume / rollback:** `--resume runs/first-run/checkpoints/latest.pt`; after a bad promotion, `--resume …/stage-0-final.pt --hold-stage`. Resuming never re-asks what stage it is in (D7-d).

**Seed band (D6):** repeat the short stage-0 pilot 2–3× with different seeds; record the spread in `summary.md`.

**Coherence check:** the sheet's six pairwise checks still pass; the three consolidation additions (wall-clock trigger, RECOVER seam, HALT guard) consume existing seams (atomic writes, the closure, `curriculum.jsonl`) and introduce no second mechanism; durations remain deliberately un-estimated — the smoke test measures them. Every pick holds unchanged under D1-p branch (ii) except the device line, the GPU-side monitoring rows, and the watermark call, exactly as the sheet's conditional describes.

---

## 6. Standing restatement

This consolidated set is a **recommendation for the project owner to ratify — not a science-spec verdict**: it treats `ctl_instruction.md` and `pinn_architecture.md` as fixed constraints, leaves **D1-p (fp32 vs fp64)** to the owner's separate adjudication (every pick holds under both branches), and treats **B-8** as settled by the attached spec (REJECT if `eps_H > 1e-5`; smaller passes) rather than as an open item.

---

## 7. Ranking of the three individual reports

**Method.** Each report was audited on the same checklist, and every load-bearing claim that *could* be verified against the attached originals *was* re-verified during this consolidation (file and section anchors given below so the audit is repeatable). The checklist: (1) **research quality** — did the report actually re-derive its conclusions from the attached sources, including the brief's explicit instruction to check whether the *current* specs postdate and contradict the decision sheet, and did it adjudicate the known intra-prior-round divergences (sheet vs depth report)? (2) **accuracy** — are its mathematical, physical, and engineering statements correct where checkable, and are its citations real and verifiable? (3) **rigor/reliability** — scope compliance (D1-p and B-8 untouched; ⚖ left as placeholders per the Stage-1 contract), source discipline (no invented numbers), honesty of the claims register, and internal consistency of the recommended set. All three reports were directionally sound and converged on the same core defaults; the ranking below is about verification depth and error rate, not about which "side" they took.

### 7.1 Verified findings and errors, per report

**Fable report — verified positives (each re-checked against the originals):**
- Found the **CURR-03 spec drift** (ADVANCE/RECOVER/HALT-REVIEW postdating the sheet) and gave the cleanest operationalization (`recover.retries: 0` — spec structure without inventing the spec's own provisional values). *(Verified against `ctl_instruction.md` Stage Transition Criteria.)*
- Found the **SI-PINN-003 closure** (U-14 stale). *(Verified: `pinn_architecture.md` Source Issues, "RESOLVED — reconciled by Phase 34.")*
- **Unique:** found the **snapshot-count medians (61/127/1003)** in the attached spec, partially closing U-1, and computed the corpus at ≈6.2 M snapshots ≈ **0.55 GB fp32 / 1.1 GB fp64** — the arithmetic was independently re-computed here and is exactly right (4,857×127 + 4,857×61 + 5,314×1,003 = 6,243,058 snapshots × 88 B/176 B), and it materially strengthens the D3 verdict. The other two reports carried U-1 as fully open, which the attached spec contradicts.
- **Unique:** caught the **decision sheet's own set-labeling slip** (R-5: the sheet lists 4,857 as `hierarchical_gold`; the spec's dataset Table assigns 2,749 to Set 2a hierarchical @ dt 0.01 and 4,857 to Set 1b standard @ 0.17). *(Verified against the spec's Table; correctly labeled cosmetic/direction-safe.)*
- **Unique:** caught the **Hydra duplication** (R-4: the three-file stack is named both under the "Ignore Now and Come Back Later" heading and, unmarked, in the Implementation Notes — meaning the sheet's B-9 rationale was slightly overstated). *(Verified at both locations in `ctl_instruction.md`.)*
- The only report to execute the **D4-a cadence override** on the evidence: it identified that the sheet "kept" step-1000 against its own companion evidence, citing r1b §1.8's arithmetic (100 s lost at 0.1 s/step vs **83 min at 5 s/step**), DRO-6, and the depth report's §7.4/7.9 — all three citations verified verbatim.
- The most precise **⚖ audit**: itemizes exactly which values r1b does and does not supply, including correctly attributing the 10-min heartbeat to the sheet itself and the "15–30 min" range to r1b §1.8.
- Adjudicated **every** sheet-vs-depth-report divergence explicitly (D3, D4-a, D5 shape, D6 shape, D7 weight), with each side's grounding named.
- Physics/engineering statements spot-checked (LOOP-01 240/16 with edge cases; LOOP-03 collocation deferral; LOOP-06 metadata; LOSS-02 instrumentation mandate; Step-1A gate at DataLoader init; `final_timestep ≥ 9.5` horizon bound; r1b D-4 forward-mode lever; rung-6 smoke parameters) — all accurate.

**Fable report — weaknesses:** it goes furthest beyond the sheet (sL-BFGS preflight refusal, disposition records, B-5 fail-safe); all additions are additive, argued, and inside build-design authority, but they are new engineering an owner must still ratify. It is also the densest read. No factual error was found in it during this audit; its one derived number (0.55 GB) is properly caveated as median-based.

**GLM report — verified positives:**
- Independently found **SD-2 (CURR-03/RECOVER)** and **SD-1 (SI-PINN-003 closed)** — the two biggest drift items — with **precise line citations that check out** on spot verification (e.g., the "Critical" Adam reset, the Consolidated Hyperparameter Schedule, the conservation gate, CURR-03's span, PHYS-02 and §10 probe locations).
- **Unique framing:** explicitly named the intra-prior-round **D3 door contradiction (SD-3)** between the depth report (streaming-first, one-way) and the sheet (auto→in-memory, two-way), and reconciled it correctly (interface one-way / residency two-way).
- Clean, complete output contract; per-row owner-look flags; an explicit "⚖ thresholds r1b does NOT give numbers for" table with correct provenance notes (10-min heartbeat is a sheet consolidation; 0.7 watermark is a sheet default); correctly distinguished the validation-gate `eps_H` from the training-loss `eps_H = 1e-4·S_H` glyph collision.
- Physics/engineering statements accurate wherever checkable; no invented numbers.

**GLM report — verified errors/gaps:**
- **Missed the snapshot medians:** its register states U-1 is "Not in attached files" — contradicted by the attached `ctl_instruction.md` (verified medians 61/127/1003 in the batch-construction contract). A material miss, since it is exactly the "current specs may postdate the sheet" check the brief mandates, and it bears directly on GLM's own Medium-confidence D3 row.
- **Hydra location error:** its register asserts the Hydra stack is named "under a heading the spec itself marks 'Ignore Now and Come Back Later'" and attributes it to "(Phase 18 Implementation Notes)" — the Implementation Notes mention is *not* under that heading and carries no Phase-18 tag; the report concluded "NOT a spec drift," missing the duplication (R-4). Minor, but a checkable inaccuracy.
- One conceptual slip: conflates r1b D-4's jvp-based *AD pattern* with a "jvp-based sampler path" under D5-E (the collocation sampler has nothing to do with the AD mode).
- Mild over-confidence in places (e.g., B-3 rated High/"research-settled" for what is internal-naming taste; the sheet, and the other two reports, treat it as a preference).
- Its RECOVER instantiation ("always-on from day 1") is left without an executable budget — honest (flagged for the owner) but less operational than the retries=0 form.

**ChatGPT report — verified positives:**
- Directionally sound on every row; converges with the others on the unanimous core; the one override it makes (D3 → plain in-RAM) is reasoned from the strategy lens, names the settling measurement, and is honestly ranked as its own least-confident call.
- Disciplined about ⚖: explicitly leaves all guard thresholds blank and enumerates the missing ones — no invented numbers anywhere.
- Correct standing restatement; correct handling of D1-p (holds under both branches) and B-8; correctly registers the spec's rejection of "fallback advancement," so it did read at least part of the Phase-33 material.
- Useful self-audit (identifies the over-weighting risk of the simplicity lens and keeps the one-way doors).

**ChatGPT report — verified errors/gaps:**
- **No usable citations:** every citation is a broken machine token ("fileciteturn0file2"-style) naming no file or section. The brief's source-discipline clause asks for attached-filename citations; as delivered, none of its claims can be traced, which is a direct reliability cost for a report whose job is adjudication.
- **Shallowest spec verification:** it performed no systematic current-spec diff. It missed the RECOVER/CURR-03 implication for D4-c/D7-c (despite quoting the adjacent fallback-advancement fact), the SI-PINN-003 closure, the snapshot medians, the sheet's set-label slip, and the Hydra duplication — i.e., every drift finding the other reports surfaced.
- **One checkable factual error:** "the Hydra stack appears *only* in a deferrable 'ignore now and come back later' note" — false; it also appears, unmarked, in the Implementation Notes.
- **Did not engage the one row where the sheet contradicts its own evidence base:** it endorses D4-a's step-1000 cadence without addressing r1b §1.8/DRO-6 — the wall-clock evidence both other reports engaged.
- Its D3 override rationale leans on "the measurements required … are explicitly still unknown," which the attached spec had already partially narrowed (the medians) — an information gap of its own making.
- Very few concrete numbers or spec quotations anywhere: a low error surface, but also low verification value; several rows are argued generically ("the attached materials say…") rather than from named contracts.

### 7.2 Ranking

| Rank | Report | Research quality | Math/physics/engineering accuracy | Rigor & reliability |
|---|---|---|---|---|
| **1** | **Fable report** | Deepest: full current-spec diff (5+ verified drift findings, 3 unique), every prior-round divergence adjudicated, r1b evidence actually consumed (cadence override) | All checkable statements and all derived arithmetic verified correct; caught and corrected a source's own numerical labeling error against the spec | Tightest scope/⚖ discipline; most precise register (statuses per item, an explicit "what r1b does/doesn't number" audit); no factual errors found |
| **2** | **GLM report** | Strong: found the two biggest drift items independently, with accurate line-level citations; named and resolved the D3 door contradiction | Accurate wherever checkable, but one location/attribution error (Hydra) and one conceptual conflation (jvp/sampler); missed the medians its own D3 confidence depended on | Very good: honest ⚖ table, per-row owner flags, no invented numbers; a stale U-1 entry and a couple of over-confident labels are the reliability deductions |
| **3** | **ChatGPT report** | Sound synthesis of the prior round, but essentially no independent verification against the current specs or the r1b numbers; missed all drift findings | No mathematical claims to fault — because it makes almost none; one checkable factual error ("Hydra appears only…"); abstraction substitutes for verification | Good scope/⚖ discipline and an honest register, but unverifiable citations and generic grounding make its conclusions the hardest to trust without redoing the work |

**Bottom line.** The gap between #1 and #2 is moderate: both did the job the brief actually asked for — adjudication *against the attached current sources* — and both caught the load-bearing spec drift; Fable adds three unique verified catches (medians/U-1, the set-label slip, the Hydra duplication), the only evidence-driven cadence override, and a spotless error record, while GLM carries two small checkable inaccuracies and one material miss. The gap between #2 and #3 is larger and is about method, not conclusions: the ChatGPT report's recommendations are largely correct because the prior round's defaults were largely correct, but it demonstrably did not re-verify them — no traceable citations, no current-spec diff, no engagement with the r1b evidence on the one row where that evidence overturns the sheet — so as an *independent adjudication* it adds the least assurance. If its picks are adopted, it should be on the strength of the other two reports' verification, not its own.

**Transparency note on this ranking.** Every claim above that credits or faults a report is tied to a named artifact (file, section, or number) that was re-checked during this consolidation, so the owner can audit the ranking independently rather than take it on trust: the medians and dataset Table in `ctl_instruction.md`; the CURR-03 text; the SI-PINN-003 resolution note in `pinn_architecture.md`; the two Hydra locations; r1b §1.8/DRO-6; and the r1b files' absence of the three ⚖ numbers.

*— End of consolidated resolution.*
