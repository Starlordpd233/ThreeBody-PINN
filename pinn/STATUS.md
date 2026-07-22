# CTL-PINN Forward Status

**Milestone:** v2.0 Stage-0 training viability slice  
**Status:** Awaiting owner `go` / `adjust` / `rethink` decision  
**Held-out gate:** `FAIL` (`eps_H = 237.2086056078468`, `SCS = 2.3751304405952904`)

This handoff separates what is shipped, what remains an explicit seam or
placeholder, and what is deferred. It does not implement Stage 1 or any
PLAT-01..07 work.

## Shipped slice

| Area | Shipped state | Evidence / entry point |
| --- | --- | --- |
| Environment and precision | MPS/float32 production runtime with fp64/CPU reference path and recorded fingerprints | Phase 37; `pinn/runtime.py` |
| Network and physics core | 14D `[tau, IC13]` SQR-SkipResNet-SIREN, mass-weighted COM projection, AD residuals, five-term loss catalog | Phase 38; `pinn/network.py`; `pinn/physics_residual.py`; `pinn/loss_catalog.py` |
| Real data path | Fail-closed admitted-data adapter, deterministic physical-key split manifest, Stage-0 batching and population scan | Phase 39; `pinn/data/` |
| Stage-0 training | Adam to full-batch L-BFGS controller path, scheduled weights, clipping, stage-exit dispositions | Phase 40; `pinn/training/controllers.py` |
| Operations | YAML config, atomic checkpoints, exact resume, guards, signals, status/summary artifacts, operator runbook | Phases 41–42; `pinn/train.py`; `pinn/training/` |
| Verification | Five-rung preflight ladder, duration gate, real interrupt/resume smoke, three-seed pilot | Phase 43; `pinn/verify.py`; Phase-43 smoke/pilot evidence |
| Held-out evaluation | One-time receipt-bound evaluator over the persisted test split; production summary refresh | `pinn/evaluate.py`; `runs/stage0-pilot-seed42/evaluation/` |

GAP-38-01 is closed: its real admitted-trajectory residual and overfit evidence
was supplied under owner Option B and recorded as `RESOLVED-WITH-INSTRUCTION`
in `.planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-GAPS.md`.

## Seams and placeholders

| Seam / placeholder | Current state | Forward constraint |
| --- | --- | --- |
| `recover.retries` | Owner-ratified conservative value `0`; config seam is live | Any nonzero policy needs new evidence and owner ratification |
| Guard thresholds | Owner-ratified for this Stage-0 slice: loss `1e11`, disk `0.05`, memory `0.7` | Do not generalize across stages/hardware without calibration |
| D4-a wall-clock checkpoint | Owner-ratified `120 s` | Checkpoint safety bound, not a convergence or abort threshold |
| B-5 resume classification | Current 34-field registry ratified unchanged; unclassified fields refuse | Extend only with explicit identity/operational classification |
| Owner acceptance threshold | Sole post-v1.3 physics gate remains `eps_H <= 1e-5` / `SCS <= -5` | Current held-out result is `FAIL`; never infer viability from validation alone |
| Stochastic L-BFGS | Typed refusal for unsupported stages | No stages 3–6 implementation in v2.0 |
| RAD collocation | Interface seam only | No adaptive-density strategy shipped |
| Tier-3 remediation | Not implemented | No automatic LR or optimizer rescue |
| Streaming residency | In-memory Stage-0 only | No out-of-core cumulative-stage path |
| Auto-revert | Manual rollback/hold-stage only | No automatic divergence-quality revert |

## Deferred platform inventory

| Requirement | Deferred work | Status |
| --- | --- | --- |
| PLAT-01 | End-to-end Stages 1–6 curriculum with cumulative replay | Deferred pending owner verdict |
| PLAT-02 | Stochastic L-BFGS for stages 3–6 | Deferred; typed refusal remains active |
| PLAT-03 | Streaming/out-of-core data residency | Deferred |
| PLAT-04 | Divergence-quality automatic revert | Deferred |
| PLAT-05 | RAD-style adaptive collocation densities | Deferred; hook only |
| PLAT-06 | Tier-3 automatic learning-rate remediation | Deferred |
| PLAT-07 | Automatic loss-weight dominance rebalancing | Deferred; seam remains empty |

## Acceptance handoff

The complete owner evidence draft is
`.planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`.
The evaluator invocation budget is exhausted: two failed attempts and the one
final completed invocation are all documented there. No further held-out
evaluation is authorized under the current policy.

