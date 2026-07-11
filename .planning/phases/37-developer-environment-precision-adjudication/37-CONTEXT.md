# Phase 37: Developer Environment & Precision Adjudication - Context

**Gathered:** 2026-07-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 37 delivers the reusable M5 Pro development substrate for the v2.0
viability slice: a fresh-Mac, one-command `pinn-train` setup; a reproducible
environment definition and fingerprint; one parameterized precision/device
seam; and recorded dual-arm componentwise-AD evidence for owner adjudication
of D1-p.

The phase does not rebuild the production PINN, ingest the admitted dataset,
run Stage 0, or select fp32 versus fp64. The owner records D1-p after reading
the probe evidence; dependent build work must not silently cross that
checkpoint.

</domain>

<decisions>
## Implementation Decisions

### Bootstrap Entry And Idempotence
- **CTX-01:** The canonical fresh-Mac command is a root-level `./setup.sh`.
  It may delegate to focused helpers, but it must not require Make, Python, or
  a pre-existing conda installation.
- **CTX-02:** Setup detects a compatible Miniforge installation and installs
  the arm64 distribution only when needed. It never replaces an existing
  conda installation silently, and its install prefix remains configurable.
- **CTX-03:** Setup creates or validates `pinn-train`, runs verification via
  the discovered conda executable or `conda run`, avoids editing shell startup
  files, and prints the explicit interactive activation command. A second run
  is a no-op validation pass rather than a destructive rebuild.
- **CTX-04:** The setup verification must include the locked package/runtime
  contract and `torch.backends.mps.is_available() == True`.

### Environment Provenance
- **CTX-05:** Keep a human-editable `environment.yml` and a fully pinned lock
  or `pip freeze` file under version control. Normal setup consumes and
  validates this pair; only an explicit refresh operation may rewrite the
  pinned file.
- **CTX-06:** Emit a canonical JSON environment fingerprint plus a concise
  human-readable rendering. It includes at least `sw_vers`, Python version,
  PyTorch version/build, and the pinned-lock SHA-256. Architecture and observed
  MPS availability are also recorded facts.
- **CTX-07:** Evidence runs are non-overwriting and timestamped. Preserve raw
  machine-readable output and an owner-readable Markdown summary together so
  the adjudication remains re-derivable.

### Dual-Arm AD Evidence
- **CTX-08:** One orchestration command launches isolated fp32-MPS and
  fp64-CPU child processes through the same parameterized probe path. The MPS
  child receives `PYTORCH_ENABLE_MPS_FALLBACK` removed from its environment,
  and every arm records requested and actual device.
- **CTX-09:** Preserve the authoritative synthetic trajectory on
  `u in [0, 1]`, the legacy `u = 0.3` fixture, analytical component
  derivatives, and `relative_error < 1e-6`. Add only deterministic warmup and
  repeat work needed to time the full-Jacobian and scalar-`u` forward-mode AD
  patterns; do not replace correctness with a timing-only benchmark.
- **CTX-10:** For every arm and AD pattern, record dtype, device, fallback
  state, framework build, workload and repetition counts, raw and summary
  timings, componentwise and aggregate errors, criterion pass/fail, and any
  exception. The report presents evidence and does not recommend a precision.
- **CTX-11:** Probe completion is an explicit owner checkpoint. Do not set a
  production precision default or begin dependent Phase 38 work until the
  owner records the D1-p choice.

### Precision And Device Seam
- **CTX-12:** Use the required `precision` and `device` config keys and resolve
  them once through a central typed helper. Pass dtype and device explicitly
  through tensor, model, and AD construction; avoid hidden global
  default-dtype mutation and scattered device checks.
- **CTX-13:** The same execution path supports the required fp32-MPS and
  fp64-CPU profiles. Validate combinations up front and fail clearly on an
  unsupported request such as fp64-MPS; never fall back silently.
- **CTX-14:** Before owner adjudication there is no implicit production
  precision default. Probe invocations select each arm explicitly. After the
  owner decides D1-p, one recorded config default may change without changing
  the implementation path.

### Agent Discretion
- Choose exact helper/module names and CLI spelling consistent with the
  repository after research maps the new `pinn/` package layout.
- Choose the pinned-lock mechanism (`pip freeze` or an equivalent platform
  lock) that most faithfully reproduces the mixed conda/pip environment.
- Choose deterministic timing warmup/repetition counts and summary statistics;
  record the raw counts and do not invent a performance threshold.
- Choose the exact JSON field names and evidence directory layout while
  preserving non-overwrite, machine readability, and an owner-readable
  Markdown result.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Milestone Scope And Requirements
- `.planning/ROADMAP.md` - v2.0 build discipline, verification protocol, and
  the Phase 37 goal and success criteria.
- `.planning/REQUIREMENTS.md` - ENV-01 through ENV-04, including the exact
  setup, fingerprint, dual-arm probe, and shared-path precision contracts.
- `.planning/PROJECT.md` - viability-slice boundary, M5 Pro constraint, and
  owner-carved decision doctrine.
- `.planning/STATE.md` - integrity-r2 clearance state, branch alignment record,
  and the explicit exclusion of the two matched legacy todos.

### Authoritative Build And Science Decisions
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` - owner-ratified D1 and the D1-p carve-out.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` - D1 rationale, B-6 fingerprint, and the composed first-run setup/pre-flight recipe.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` section 10.3 - synthetic trajectory, analytical AD criterion, and authoritative science contract.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - read-only framework-spec companion; do not edit it in this build phase.

### Clearance And Observation Evidence
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md` - ratified PB-1 through PB-5 dispositions and cleared Phase 37 gate.
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/research_results/MASTER-FINAL-RESOLUTION.md` - supporting audit source, especially SL-1; it is not authority over the clearance record.

### Existing Implementation Evidence
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py` - legacy `u = 0.3` componentwise-AD fixture to preserve and extend, not a complete Phase 37 dual-arm harness.
- `.planning/codebase/STACK.md` - current Python/PyTorch/MPS and platform inventory.
- `.planning/codebase/ARCHITECTURE.md` - spec-as-source-of-truth boundary and `pinn/` rebuild integration context.
- `.planning/codebase/TESTING.md` - established Python and scientific-probe validation patterns.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py` already implements the synthetic trajectory, analytical derivatives,
  componentwise autograd loop, and locked relative-error assertion. Reuse its
  fixture semantics while replacing its single CPU/fp64 process shape.
- `scripts/agent-commit` and the repository Git hooks provide the required
  atomic, owned-path commit path for phase execution.

### Established Patterns
- Framework specs define scientific behavior; build code implements them.
  Any newly discovered spec defect is surfaced and routed, not edited here.
- v1.3 `pinn/` code is reference-only and must not become the authority for
  the new precision or AD contract.
- Scientific verification uses executable probes with explicit numeric
  criteria, not prose-only acceptance.
- There is no existing production environment bootstrap, root Makefile, lock
  pair, or dual-arm MPS precision harness to preserve.

### Integration Points
- The setup entry point and environment pair sit at repository level so a
  fresh machine can invoke them before Python exists.
- The central precision/device resolver is the narrow contract later model,
  data, and training modules consume; Phase 37 should not pre-build those
  later modules.
- Phase 37 evidence feeds the owner D1-p record and the later pre-flight
  verification ladder. SL-1 is observed here but is not a gate by itself.

</code_context>

<specifics>
## Specific Ideas

- Keep the two probe arms visibly symmetric in code and output so the owner is
  comparing precision/device behavior rather than two implementations.
- Treat fallback state, actual device, and framework build as first-class
  evidence. A fast result reached through silent CPU fallback is invalid.
- Make the precision choice a small post-probe config change, not a refactor.

</specifics>

<deferred>
## Deferred Ideas

- Model architecture, losses, and production second-order residual code belong
  to Phase 38.
- Admitted-dataset scans and `s0` ratification belong to Phase 39.
- Stage-0 training, guard calibration, and the pilot belong to Phases 40-43.

### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` - explicitly recorded in
  `STATE.md` as a spec-side sensitivity question outside the v2.0 build phases;
  the keyword match to "dual" and "adjudication" was a false positive.
- `trainex-r1-research-handoff.md` - r1a is already ratified and consumed;
  the remaining r1b tuning round is a Future item, not Phase 37 work.

</deferred>

---

*Phase: 37-developer-environment-precision-adjudication*
*Context gathered: 2026-07-11*
