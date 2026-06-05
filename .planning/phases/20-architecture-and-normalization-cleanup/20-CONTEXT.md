# Phase 20: Architecture and Normalization Cleanup - Context

**Gathered:** 2026-06-03
**Status:** Ready for research and planning, except `ARCH-04` dependent edits/proof are blocked by `GAP-20-01`.

<domain>
## Phase Boundary

Phase 20 removes architecture and normalization ambiguity from the v1.4 framework specs without changing the preserved SQR-SkipResNet-SIREN backbone unnecessarily. Work is limited to framework-spec and planning/proof artifacts. Live `pinn/` implementation files are not grounding sources and are not edit targets.

Actual Phase 20 artifacts live in `.planning/phases/20-architecture-and-normalization-cleanup/`. The existing `.planning/phases/20-5-sampling-coordinate-allocation/` directory is Phase 20.5 and must remain untouched by actual Phase 20 work.

</domain>

<decisions>
## Implementation Decisions

### D-01: Phase 16 Evidence Protocol Applies First

Every Phase 20 spec edit must be evidence-gated. If a Phase 16 ledger row exists but its packet file is missing, Phase 20 creates/fills that packet according to the Phase 16 evidence workflow before editing. Evidence packets remain under `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/`; Phase 20 artifacts cite/link them and record proof trails.

### D-02: SIREN / `omega0` Contract (`ARCH-01`, `AC-ARCH-01`)

Phase 20 must create/fill or consult `evidence/B-01.md` and `evidence/B-10.md` before editing SIREN surfaces. Active SIREN wording should converge on:

- `first_omega_0 = 30`
- `hidden_omega_0 = 1`
- standard SIREN initialization
- hidden-layer bounds divided by `hidden_omega_0`, not multiplied by it
- no epochwise or optimizer-step `omega0` scheduler
- any `omega0` retuning is only a stage-boundary ablation with fresh initialization, not mutation inside a run

The executor must reconcile every active/normative SIREN/init/frequency surface in `pinn_architecture.md`: scheduler section/listing, hidden-layer formula wording, hyperparameter tables, architecture summary tables, and nearby implementer-facing prose. Historical/provenance text may remain only if clearly non-normative.

Closure proof for `AC-ARCH-01` requires completed B-01/B-10 packets, ledger verdicts, a targeted post-edit surface audit, and a negative search/audit showing no active scheduler guidance remains.

### D-03: LayerNorm Contract (`ARCH-02`, `AC-ARCH-02`)

LayerNorm cleanup is evidence-gated through `evidence/M8.md`. After M8 records a grounded verdict, active wording should state the source-backed contract only if that verdict supports it:

- LayerNorm is a project-specific/author modification used as a skip-path stabilizer.
- It is not original SQR-SkipResNet paper content.
- It applies on the skip/power branch only if supported by the source-backed architecture contract.
- The default is `elementwise_affine=False`.
- Affine LayerNorm or LayerNorm removal are optional future ablations, not the Phase 20 default contract.

The executor must reconcile every active/normative LayerNorm surface in `pinn_architecture.md`: architecture prose, skip/power-branch descriptions, hyperparameter tables, summary tables, attribution statements, default statements, and future-ablation wording.

Closure proof for `AC-ARCH-02` requires the M8 packet, ledger verdict, post-edit surface audit, confirmation of project-specific attribution and `elementwise_affine=False`, and a negative audit showing no contradictory attribution, branch-scope, or affine-default text remains.

### D-04: M5 / `I_3` Is Contested (`ARCH-03`, `AC-ARCH-03`)

M5 is a STOP-protocol adjudication task. Phase 20 must create/fill or consult `evidence/M5.md`, cite both primary sources side by side, compare each source's `I_3` definition, raw range, and normalization/input mapping, and only then run a short first-principles geometry/algebra range check for the ratio-form quantity it actually addresses if that check is genuinely short and uncontroversial.

The allowed verdict set is the full Phase 16 evidence enum:

- `accept-resolution`
- `accept-issue-doc`
- `accept-third-position`
- `reject-both-as-unsupported`
- `defer-with-blocker`

No `I_3` wording may be edited until M5 records a grounded verdict. If no verdict can be grounded without semantic judgment, Phase 20 must record a gap and stop dependent work for user instruction.

`AC-ARCH-03` closes only after the M5 verdict plus post-edit audit of every active `I_3` range/mapping surface and a negative audit showing no contradictory active `I_3` range/mapping remains.

### D-05: Raw vs Bounded `I_norm` Is Separate From M5 (`ARCH-04`)

`ARCH-04` distinguishes the raw inertia descriptor from the tanh-squashed network input. It is related by theme to M5 but is not closed by the M5 / `I_3` verdict.

Phase 20 verified no clear Phase 16 ledger row, evidence packet, or AC/proof vehicle for the `I_norm` naming issue (issue-doc D-02, distinct from 20-CONTEXT D-02 SIREN) / `ARCH-04`. This is recorded as `GAP-20-01` in `20-GAPS.md` and the milestone-wide gap index. Dependent `ARCH-04` edits/proof are blocked until the user chooses the vehicle. Do not invent `D-02.md`, `ARCH-04.md`, or attach `ARCH-04` to M5 by convenience.

If the gap is resolved and source support is confirmed, the intended naming contract is:

- `I_norm_raw` for the raw physics/metadata descriptor
- `I_norm_in = tanh(I_norm_raw)` for the bounded network-facing value

### D-06: Energy/Mass Support Ranges (`ARCH-05`, `AC-ARCH-05`)

Support-range cleanup is evidence-gated through two separate Phase 16 rows:

- M9 / `evidence/M9.md`: energy normalization realized support
- M10 / `evidence/M10.md`: mass normalization realized support

After M9 and M10 record grounded verdicts, wording should frame documented energy and mass normalization ranges as dataset/domain occupancy facts rather than normalizer defects, only if those verdicts support that framing. The spec should distinguish network input range available by formula from range actually occupied by this dataset, without treating one-sided or asymmetric realized support as universal physics bounds or normalizer defects.

**Vocabulary clarification (user decision 2026-06-03):** "Realized support" is planning/acceptance shorthand — it labels the ARCH-05 objective in this context, the Phase 16 ledger, and the Phase 20 roadmap success criterion. It is NOT a new technical term for the framework spec itself. Spec prose should use the issue doc's language or plain descriptive wording:
- **M9:** `E_norm` occupies `[-1, 0)` for the documented bound-system dataset; the positive side of the tanh input range is unused; this is acceptable for SIREN and not a normalizer correctness failure.
- **M10:** The hierarchical-mass `m_norm` range is asymmetric; that asymmetry carries mass hierarchy information and is not a centering/correctness failure.
- If extra clarification is needed, use plain prose like "dataset-occupied range under the documented data-generation regimes," not a formal new vocabulary label.

The executor must reconcile every active support-range surface that could imply an invalid normalizer: CTL/spec normalization tables, nearby prose explaining `E_norm` / `m_norm`, Phase 20 proof summaries, M9/M10 before/after notes, and ledger/handoff annotations if they summarize closure evidence. Cite issue docs as sources, but do not rewrite primary source issue docs unless the workflow explicitly treats a planning/proof annotation as editable.

M9 and M10 remain separate evidence/verdict records. Because both share `AC-ARCH-05`, a combined post-edit support-range audit may prove shared closure after both verdicts are recorded.

### D-07: EDL Use Is Narrow

EDL is only for source-silent empirical questions after a STOP-protocol gap is found. It is not used for ordinary evidence adjudication, source-backed documentation cleanup, short first-principles checks, or M5's Phase 16 / EVID-05 path. If EDL is used, it is support only; `20-GAPS.md` plus the milestone index remain the authoritative blocker, and final resolution still requires user instruction.

### D-08: Research Artifact Shape

`20-RESEARCH.md` should be an implementation-ready evidence map. It must map `ARCH-01` through `ARCH-05` to requirements, acceptance criteria, ledger rows, evidence packet paths, source anchors, target spec surfaces, STOP/gap triggers, EVID-05 applicability, and proof/audit requirements. It must not become a broad architecture redesign or empirical ablation study unless a logged STOP/EDL gap requires support.

### D-09: "Realized Support" Is Planning Shorthand, Not Spec Vocabulary

Named restatement of the existing D-06 vocabulary clarification, recorded as a labeled decision for traceability (review reports referenced it by label). "Realized support" remains planning/acceptance shorthand only: it labels the ARCH-05 objective in Phase 20 context, the Phase 16 ledger, and the roadmap success criterion, but it is not a new technical term for the framework specs; spec prose uses issue-doc language or plain descriptive wording. Source of record: 20-CONTEXT D-06 "Vocabulary clarification (user decision 2026-06-03)"; see also `20-DISCUSSION-LOG.md` Deep Review Decision D-09.

### D-10: I_3 Derivation Lives in Research Until Source Definitions Match

The ratio-form `I_3` derivation belongs in `20-RESEARCH.md` as a conditional lemma. A Phase 20 executor may consult it only after comparing the source definitions, ranges, and mappings in M5. If the issue doc uses a genuinely different `I_3` object, the ratio-form lemma must not be treated as verdict evidence for that object. Source: `20-DISCUSSION-LOG.md` Deep Review Decision D-10.

### D-11: 20-04 Autonomy Requires a Mechanical Grounding Gate

Plan 20-04 may remain `autonomous: true` because M9/M10 are not EVID-05 contested and D-11 records a deterministic safe default for ungrounded numeric ranges: record a `20-GAPS.md` entry, halt the affected Task 2 work, and surface the decision to the user. D-06 is the source for spec-safe plain descriptive wording when numeric support ranges are not explicitly grounded; if even qualitative/plain-language framing cannot be grounded, use the D-11 STOP path before editing. Sources: `20-DISCUSSION-LOG.md` Deep Review Decision D-11 for autonomy/safe-default handling; `20-CONTEXT.md` D-06 for issue-doc/plain-language support wording.

</decisions>

<execution_coordination>
## Execution Coordination Rules

- `20-02` and `20-03` both write `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`. If the plans are implemented with parallel workers, their ledger-write tasks must be serialized: one worker must complete and commit its ledger update before the other begins its ledger update.
- `20-04` depends on both `20-02` and `20-03`; treat it as wave 3 for execution ordering even if older review notes describe it as wave 2.
- Phase 20 may execute the non-ARCH-04 plans while `GAP-20-01` is open, but the milestone must not be marked fully complete while `ARCH-04` remains OPEN. Full closure requires `GAP-20-01` to be `RESOLVED-WITH-INSTRUCTION` or `DEFERRED` by user instruction. Phase 20 may report ARCH-01/02/03/05 closed with ARCH-04 blocked; a downstream phase that "Depends on Phase 20" may proceed on the four closed ACs but must treat ARCH-04 as an explicit open carry-forward, not silently satisfied.
</execution_coordination>

<canonical_refs>
## Canonical References

Downstream agents MUST read these before planning or implementing.

### Phase Scope and Requirements

- `.planning/ROADMAP.md:202-216` - Phase 20 goal, dependencies, requirements, and success criteria.
- `.planning/REQUIREMENTS.md:45-51` - `ARCH-01` through `ARCH-05`.
- `.planning/phases/20-architecture-and-normalization-cleanup/20-GAPS.md` - open process-artifact schema gap for `ARCH-04`.

### Evidence Workflow

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:17-38` - Phase 16 ledger status table.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:64-70` - B-01 / `AC-ARCH-01` notes.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:279-285` - M5 / `AC-ARCH-03` notes.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:320-324` - M8 / `AC-ARCH-02` notes.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` - packet format for newly created Phase 20 evidence packets.

### Primary Issue 01 Sources

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` - candidate verdict source for v1.4.
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` - issue doc to adjudicate against the resolution doc.

### Active Framework Specs

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - SIREN, LayerNorm, architecture summary, energy regularizer, and related active architecture surfaces.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - `I_3`, `I_norm`, `E_norm`, `m_norm`, and CTL normalization surfaces.

### Dataset Support

- `simulation_data/Documentation/README.md` - dataset mass regimes, IC support, and realized data-generation documentation for `ARCH-05`.

</canonical_refs>

<code_context>
## Existing Spec Insights

### Current Active Surfaces to Audit

- `pinn_architecture.md:172` still contains an `update_omega0` listing.
- `pinn_architecture.md:195`, `:269-270`, and `:945-947` contain active SIREN frequency/init surfaces.
- `pinn_architecture.md:214-228`, `:237-268`, and `:938-941` contain active LayerNorm attribution/default surfaces.
- `ctl_instruction.md:644-768` contains active invariant and `I_norm` / `I_3` surfaces.
- `ctl_instruction.md:1000-1032` contains active network-facing normalization prose/table surfaces.
- `pinn_architecture.md:773` repeats final network input normalization details and should be checked for support-range consistency if touched.

### Tooling Hazard

Current GSD `find-phase 20` / `init.phase-op 20` resolves to `.planning/phases/20-5-sampling-coordinate-allocation`, which is Phase 20.5. Phase 20 planning must use explicit paths under `.planning/phases/20-architecture-and-normalization-cleanup/` until the routing hazard is fixed.

</code_context>

<specifics>
## Specific Ideas

- Evidence packets for B-01, B-10, M5, M8, M9, and M10 are expected to be created/fillable by Phase 20 because the ledger reserves them even if the files are currently absent.
- Do not create an `ARCH-04` evidence vehicle without user instruction; use `GAP-20-01`.
- Phase 21 may consume or re-check Phase 20 proof artifacts, but Phase 20 owns closure proof for `AC-ARCH-01`, `AC-ARCH-02`, `AC-ARCH-03`, and `AC-ARCH-05`.

</specifics>

<deferred>
## Deferred Ideas

- Empirical ablation design for `omega0`, LayerNorm affine/removal, `I_norm` saturation, or new support ranges is out of Phase 20 unless a STOP/EDL gap explicitly opens that research path.
- Phase 20.5 Sampling Coordinate Allocation remains separate and pending after actual Phase 20.

</deferred>
