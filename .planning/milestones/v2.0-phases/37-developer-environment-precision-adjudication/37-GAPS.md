# Phase 37 Gap Register

Owner-routed decisions and source-silent gaps surfaced during Phase 37
execution. Each entry uses the v2.0 build-analog STOP protocol fields
(requirements-completed surface; semantic decisions are owner-carved, not
invented). Add new gaps below; do not edit a `RESOLVED`/`DEFERRED` entry's
verbatim record after the fact.

---

## GAP-37-01 — D1-p precision branch not recorded (owner DEFERRED)

- **Decision point:** Which D1-p branch does the owner record — `fp32-MPS` or
  `fp64-CPU` — for the v2.0 build's production precision default?
- **Where in artifact:**
  - `.planning/phases/37-developer-environment-precision-adjudication/37-05-SUMMARY.md` (Owner D1-p Checkpoint section)
  - `.planning/phases/37-developer-environment-precision-adjudication/evidence/precision/20260712T150406Z/{raw.json,summary.md}` (the evidence the owner adjudicates from)
- **Task context:** Plan 37-05, the terminal blocking `checkpoint:decision`
  task. Plan 37-05 task 37-05-01 (the on-device dual-arm run + validate) is
  complete and committed (`a65e78c`).
- **Classification:** cross-phase reframing — D1-p is an owner-carved decision
  (RATIFICATION.md 2026-07-05, lines 36-40). v2.0 REQUIREMENTS.md SCOPE-19
  states owner-carved decisions are "built as seams, not invented"; the agent
  surfaces evidence, it does not pick the value.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md:36-40` — explicitly carves D1-p out: "adjudicated by running the §10.3 probe … as the first build act. Every ratified pick holds under both branches." Does NOT pick a branch.
  - `trainex-r1a-resolution-doc.md:12,26,204` — "D1-p (precision, fp32 vs fp64) is not decided anywhere in this document"; "Not decided — owner-carved; all picks hold under both branches"; "leaves D1-p (fp32 vs fp64) to the owner's separate adjudication".
  - `trainex-r1a-resolution-doc.md:178` — the §5 first-run recipe shows `device: mps, precision: float32`, but line 198 carries the explicit caveat "Every pick holds unchanged under D1-p branch (ii) except the device line" — i.e. the recipe line is an *example*, not a pick.
  - `trainex-r1a-resolution-doc.md:161` (R-6) — "the dual-arm scheme is a tolerance ruling the owner must ratify as part of D1-p — not decided here."
  - `.planning/REQUIREMENTS.md` ENV-03/ENV-04 — "The precision verdict is surfaced, not chosen by the agent."
- **Mathematical / engineering grounding:** both branches run the same code
  path through `pinn.runtime.resolve_runtime` (the ENV-04 seam). The §10.3
  probe is a scalar-leaf, single-trajectory fixture; on it, fp32-MPS and
  fp64-CPU both reproduce the analytical derivative to 0.00e+00 aggregate
  relative error. The fixture has no catastrophic-cancellation terms, so it
  does not distinguish the branches on correctness. Timing on this fixture
  (fp64-CPU ~5–6× faster per AD evaluation in median wall-clock) is NOT
  representative of the production Stage-0 residual workload, which the
  Phase-43 smoke test + pilot will measure. The decision therefore cannot be
  inferred from the probe evidence alone — it depends on the production
  workload's precision sensitivity (R-6), which is outside Phase 37's scope.
- **Agent was tempted to:** record `fp32-MPS` on the strength of the §5
  recipe's example line. Did NOT — the resolution explicitly disclaims that
  line as branch-dependent (line 198), and R-6 makes the tolerance ruling an
  owner ratification.
- **What the user needs to decide:**
  - **A. `fp32-MPS`** — record fp32-MPS as the D1-p branch. Phase 38 defaults to `precision=float32, device=mps`. The fp64-CPU arm remains available via the same resolver as the in-framework escape hatch.
  - **B. `fp64-CPU`** — record fp64-CPU as the D1-p branch. Phase 38 defaults to `precision=float64, device=cpu`. The fp32-MPS arm remains available via the same resolver.
  - **C. continue to defer** — leave D1-p and Phase 38 blocked; the retained evidence is reusable, no re-run required when the owner records a branch.
- **Confidence of impact:** HIGH — Phase 38 (`pinn/` model rebuild, FUT-01) is
  blocked at the D1-p seam until the owner records A or B. ENV-03 cannot close
  without the owner's verdict.
- **Status:** `RESOLVED-WITH-INSTRUCTION` (2026-07-12). History: first
  `DEFERRED` earlier the same day (owner instruction: *"i picked the wrong
  option. let's defer that and we'll decide on this later."* — the owner
  retracted an initial fp32-MPS selection; recorded verbatim per the plan's
  `<resume-signal>` contract), then resolved in a later session the same day.
- **Resolution note:** RESOLVED-WITH-INSTRUCTION on 2026-07-12. The owner
  recorded **Option A — fp32-MPS** as the D1-p branch. Verbatim owner
  instruction: *"okay let's close out the gap now. I think we will remain with
  the entire training happening on the MacBook Pro with M5 chip. Let's carry
  on with that choice and decision for now. If later we do want to split the
  workload to the Lenovo, then we can do that later if the benefit we'll gain
  is actually sufficent enough to offset the work and extra time we put in to
  setup the lenovo."* Because both branches run entirely on the M5 Pro, the
  agent asked one explicit branch-naming confirmation; the owner selected
  **"fp32-MPS"** from {fp32-MPS, fp64-CPU, keep deferred}. Per R-6, the
  selected option's text stated that recording fp32-MPS also ratifies the
  dual-arm tolerance scheme (fp64-CPU as reference arm; fp32-MPS accepted
  within ~1e-4 of it), so that tolerance ruling is recorded as part of this
  resolution. Effects: the v2.0 production precision default is
  `precision=float32, device=mps`; the fp64-CPU arm remains the in-framework
  escape hatch via the same resolver (ENV-04); **Phase 38 (NET) is
  UNBLOCKED**; ENV-03 is closable. Per CTX-14 no code changed now —
  `pinn/runtime.py` deliberately encodes no default and no training config
  file exists yet; the first training config (Phase 40/41 YAML per the §5
  recipe) consumes this recorded default. The retained dual-arm evidence
  (`evidence/precision/20260712T150406Z/`) required no re-run. The owner
  additionally ruled that training remains single-machine on the M5 Pro; any
  Lenovo/multi-machine split is a later cost-benefit question outside v2.0
  scope.

---
