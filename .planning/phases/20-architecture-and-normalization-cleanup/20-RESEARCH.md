# Phase 20 Research - Architecture and Normalization Cleanup

**Created:** 2026-06-03
**Purpose:** Implementation-ready evidence map for planning Phase 20. This is a routing table for evidence-led edits and closure proof, not a broad architecture redesign study.

## Executive Summary

Phase 20 should execute as evidence-first spec cleanup:

- Reserved Phase 16 evidence packets for `ARCH-01`, `ARCH-02`, `ARCH-03`, and `ARCH-05` are missing on disk and should be created/filled from the Phase 16 template during execution.
- `ARCH-04` has no clear Phase 16 evidence/proof vehicle; `GAP-20-01` is open and blocks only `ARCH-04` dependent edits/proof.
- Phase 20 should not edit live `pinn/` implementation code.
- Phase 20 should leave closure proof for `AC-ARCH-01`, `AC-ARCH-02`, `AC-ARCH-03`, and `AC-ARCH-05`; Phase 21 may re-check that evidence, but should not be the first proof point.

## Current Packet State

Checked 2026-06-03:

| Packet | Ledger status | File state | Handling |
|--------|---------------|------------|----------|
| `evidence/B-01.md` | Reserved, Phase 20 PENDING | missing | Create/fill from `_TEMPLATE.md` before SIREN edits. |
| `evidence/B-10.md` | Reserved, Phase 20 PENDING | missing | Create/fill from `_TEMPLATE.md` before SIREN edits. |
| `evidence/M5.md` | Reserved, Phase 20 PENDING, EVID-05 required | missing | Create/fill from `_TEMPLATE.md`; contested adjudication before `I_3` edits. |
| `evidence/M8.md` | Reserved, Phase 20 PENDING | missing | Create/fill from `_TEMPLATE.md` before LayerNorm edits. |
| `evidence/M9.md` | Reserved, Phase 20 PENDING | missing | Create/fill from `_TEMPLATE.md` before energy support edits. |
| `evidence/M10.md` | Reserved, Phase 20 PENDING | missing | Create/fill from `_TEMPLATE.md` before mass support edits. |
| `evidence/D-02.md` / `evidence/ARCH-04.md` | Not found in ledger | missing | Example names only; no authorized packet exists. Do not create without user instruction; see `GAP-20-01`. |

## Route Map by Requirement

| Requirement | Acceptance / proof vehicle | Ledger row(s) | Evidence packet(s) | EVID-05? | Status |
|-------------|----------------------------|---------------|--------------------|----------|--------|
| `ARCH-01` SIREN init/frequency | `AC-ARCH-01` | B-01, B-10 | `evidence/B-01.md`, `evidence/B-10.md` | No | Ready to plan packet creation and edits. |
| `ARCH-02` LayerNorm attribution/default | `AC-ARCH-02` | M8 | `evidence/M8.md` | No | Ready to plan packet creation and edits. |
| `ARCH-03` `I_3` range/mapping | `AC-ARCH-03` | M5 | `evidence/M5.md` | Yes | Ready to plan adjudication-gated task; edits blocked until verdict. |
| `ARCH-04` raw vs bounded `I_norm` naming | Missing / unresolved | none found | none found | Unknown | Blocked by `GAP-20-01`. |
| `ARCH-05` energy/mass realized support | `AC-ARCH-05` | M9, M10 | `evidence/M9.md`, `evidence/M10.md` | No | Ready to plan packet creation and edits. |

## ARCH-01 - SIREN Initialization and Frequency

### Requirement and Success Criterion

- `.planning/REQUIREMENTS.md:47` requires consistent SIREN initialization and frequency settings, with no epochwise `omega0` scheduler unless a reparameterized runtime mechanism is specified.
- `.planning/ROADMAP.md:209` requires the reader to find consistent SIREN initialization and frequency settings with no epochwise or optimizer-step `omega0` scheduler; `omega0` retuning is only a stage-boundary ablation with fresh initialization.

### Ledger / Evidence Route

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:19` reserves B-01 with `evidence/B-01.md`, `AC-ARCH-01`, and `pinn_architecture.md`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:28` reserves B-10 with `evidence/B-10.md`, `AC-ARCH-01`, and `pinn_architecture.md`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:64-70` notes that B-01 and B-10 share `AC-ARCH-01`.

### Source Anchors

- Resolution: `ctl_pinn_resolution.md:106` fixes `first_omega_0=30`, `hidden_omega_0=1`, standard SIREN initialization, and removal of epochwise scheduling.
- Resolution: `ctl_pinn_resolution.md:126`, `:659-660`, `:685`, and `:1227-1234` reiterate fixed settings and scheduler deletion / stage-boundary ablation framing.
- Issue doc: `01-architecture-and-physics-foundations.md:71` flags B-01; `:77` / `:257-263` are the known B-10 dynamic-scheduling anchors from prior research and should be re-located by the executor.

### Target Spec Surfaces

Search and audit every active/normative SIREN/init/frequency surface in `pinn_architecture.md`, including:

- `pinn_architecture.md:172` - `update_omega0` listing.
- `pinn_architecture.md:195` - hidden `omega0` prose.
- `pinn_architecture.md:269-270` - hyperparameter table entries.
- `pinn_architecture.md:945-947` - architecture summary initialization table.
- Any nearby prose that tells implementers how `omega0` behaves.

### STOP / Gap Triggers

- If B-01/B-10 source review finds source silence or contradiction beyond the known fixed contract, stop the dependent edit and record a gap.
- Do not invent a reparameterized runtime mechanism.
- Do not edit live `pinn/` implementation code.

### Closure Proof

Phase 20 must leave:

- Completed `evidence/B-01.md` and `evidence/B-10.md`.
- Ledger verdict/status updates.
- Post-edit audit of all active SIREN/init/frequency surfaces.
- Confirmation of `first_omega_0=30`, `hidden_omega_0=1`, standard SIREN initialization, hidden-layer bounds divided by `hidden_omega_0`, no in-run scheduler.
- Negative audit showing no active scheduler guidance remains.

## ARCH-02 - LayerNorm Attribution and Affine Default

### Requirement and Success Criterion

- `.planning/REQUIREMENTS.md:48` requires LayerNorm to be documented as a project-specific stabilizer with a consistent affine/non-affine default.
- `.planning/ROADMAP.md:210` requires the reader to see that same contract.

### Ledger / Evidence Route

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:36` reserves M8 with `evidence/M8.md`, `AC-ARCH-02`, and `pinn_architecture.md`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:320-324` records the M8 packet/check anchors.

### Source Anchors

- Resolution: `ctl_pinn_resolution.md:127` keeps skip-path LayerNorm with default `elementwise_affine=False` and ablation if needed.
- Resolution: `ctl_pinn_resolution.md:663-664` states skip-path-only LayerNorm and false affine default.
- Issue doc: LayerNorm attribution/default anchors should be re-located in `01-architecture-and-physics-foundations.md` during M8 packet creation; prior research identified this as an attribution problem rather than original SQR-SkipResNet content.

### Target Spec Surfaces

Audit every active LayerNorm surface in `pinn_architecture.md`, including:

- `pinn_architecture.md:214-228` - skip-path / power-branch formula and prose.
- `pinn_architecture.md:237-268` - LayerNorm rationale through the hyperparameter default currently showing `elementwise_affine=True`.
- `pinn_architecture.md:938-941` - architecture summary and LayerNorm default.
- Any active future-ablation wording.

### STOP / Gap Triggers

- If M8 cannot ground the branch scope or default without empirical judgment, record a gap before editing.
- EDL is only relevant if Phase 20 tries to decide empirical usefulness or a required ablation protocol.

### Closure Proof

Phase 20 must leave:

- Completed `evidence/M8.md`.
- Ledger verdict/status update.
- Post-edit audit of active LayerNorm surfaces.
- Confirmation of project-specific/author attribution, skip-path stabilizer framing, `elementwise_affine=False`, and optional future ablation framing.
- Negative audit showing no contradictory attribution, branch-scope, or affine-default text remains.

## ARCH-03 - `I_3` Range and Mapping

### Requirement and Success Criterion

- `.planning/REQUIREMENTS.md:49` requires `I_3` normalization to map the documented triangle-shape range to `[-1, 1]`.
- `.planning/ROADMAP.md:211` requires the reader to verify the same.

### Ledger / Evidence Route

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:33` reserves M5 with `evidence/M5.md`, marks sources disagree, and requires EVID-05.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:279-285` confirms M5 is contested and tied to `AC-ARCH-03`.

### Source Anchors

- Resolution: `ctl_pinn_resolution.md:128`, `:608`, `:614`, and `:620` state the candidate `I_3` definition/range/mapping.
- Issue doc: the executor must cite the issue-doc `I_3` definition/range/mapping position side by side; prior research identified the issue doc as using sorted mutual distances with an `I_max` mapping, which must be compared against the resolution/current-spec ratio-form `I_3` before any range derivation is treated as verdict evidence.
- Current spec: `ctl_instruction.md:758-768` contains active `I_3` definition/range text.

### Target Spec Surfaces

Audit all active `I_3` range/mapping surfaces in `ctl_instruction.md` and any cross-references in `pinn_architecture.md` if discovered by search.

### STOP / Gap Triggers

- M5 must use EVID-05.
- Allowed verdicts are `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker`.
- If source review plus short first-principles range checking cannot ground a verdict without semantic judgment, record a gap and stop dependent `I_3` edits.

### Closure Proof

Phase 20 must leave:

- Completed `evidence/M5.md`.
- EVID-05 verdict and ledger/status transition.
- Post-edit audit showing all active `I_3` range/mapping surfaces match the selected verdict.
- Negative audit showing no contradictory active `I_3` range/mapping remains.

## ARCH-04 - Raw vs Bounded `I_norm` Naming

### Requirement and Success Criterion

- `.planning/REQUIREMENTS.md:50` requires separate names for raw inertia descriptor and tanh-squashed network input.
- `.planning/ROADMAP.md:212` requires the reader to distinguish the raw inertia descriptor from the tanh-squashed network input value.

### Current State

No clear Phase 16 ledger row, evidence packet, or AC/proof vehicle was found for the `I_norm` naming issue (issue-doc D-02, distinct from 20-CONTEXT D-02 SIREN) / `ARCH-04`.

- The Phase 16 ledger reserves B-01/B-10/M5/M8/M9/M10 for Phase 20, but no issue-doc D-02 or `ARCH-04` row.
- `ctl_pinn_resolution.md:626-627` and `:1435-1443` contain the expected raw/bounded naming anchors.
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md:42-62` documents D-02 as routine documentation cleanup.
- `ctl_instruction.md:644`, `:667`, `:738-755`, and `:1000-1032` contain active metadata/input-normalization surfaces that should be audited once the proof vehicle is resolved.

### STOP / Gap Triggers

`GAP-20-01` is open. Do not edit `ARCH-04` surfaces or close `ARCH-04` until the user chooses the evidence/proof vehicle.

### Closure Proof

Blocked. Once resolved, proof should show active text consistently distinguishes `I_norm_raw` from `I_norm_in`, confirms `I_norm_in = tanh(I_norm_raw)` only if supported, and negatively audits for raw/bounded conflation.

## ARCH-05 - Energy and Mass Realized Support

### Requirement and Success Criterion

- `.planning/REQUIREMENTS.md:51` requires energy and mass normalization support ranges to be documented as realized dataset support, not normalizer defects when asymmetric or mostly negative.
- `.planning/ROADMAP.md:213` requires the reader to see the same.

### Ledger / Evidence Route

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:37` reserves M9 with `evidence/M9.md`, `AC-ARCH-05`, and `ctl_instruction.md`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md:38` reserves M10 with `evidence/M10.md`, `AC-ARCH-05`, and `ctl_instruction.md`.

### Source Anchors

- Dataset docs: `simulation_data/Documentation/README.md:245` states standard IC masses are exactly `1.0` and hierarchical masses vary but normalize to total mass near 3.
- Dataset docs: `simulation_data/Documentation/README.md:317-324` summarize total mass support for standard and hierarchical regimes.
- Dataset docs: `simulation_data/Documentation/README.md:423-443` describe energy-error and prescreening thresholds; use only as dataset-support evidence, not as permission to invent normalization ranges.
- Current spec: `ctl_instruction.md:1019-1032` contains active network-facing normalization prose/table; `pinn_architecture.md:773` repeats input normalization details.

### Target Framing

After M9/M10 record grounded verdicts, and only if those verdicts support realized-support framing:

- Energy and mass ranges describe realized support of current dataset/data-generation regimes.
- They are not universal physics bounds.
- They are not normalizer defects.
- The spec distinguishes formula-available input range from dataset-occupied range.
- Numeric ranges must be grounded in cited sources/dataset documentation or replaced with qualitative realized-support wording.

### STOP / Gap Triggers

- If M9/M10 cannot ground numeric support ranges, do not invent them.
- If changing normalization design or deriving new empirical ranges becomes necessary, record a gap. EDL may support only that empirical question.

### Closure Proof

Phase 20 must leave:

- Completed `evidence/M9.md` and `evidence/M10.md`.
- Separate ledger verdicts/status transitions for M9 and M10.
- Combined support-range audit after both verdicts.
- Confirmation that active energy/mass support-range wording converges on realized dataset support.
- Negative audit showing no active text frames one-sided energy support or asymmetric/degenerate mass support as an invalid normalizer.

## Planning Implications

Recommended plan structure:

1. Evidence packet setup: create missing B-01, B-10, M5, M8, M9, M10 packets from `_TEMPLATE.md`; do not create an `ARCH-04` packet without user instruction.
2. SIREN edits and audits in `pinn_architecture.md` after B-01/B-10 verdicts.
3. LayerNorm edits and audits in `pinn_architecture.md` after 20-01 and the M8 verdict.
4. M5 adjudication and `I_3` edits only after a grounded EVID-05 verdict.
5. Support-range edits and combined audit in `ctl_instruction.md` after M9/M10 verdicts. Treat `pinn_architecture.md` as a read-only consistency audit surface unless a separate plan explicitly owns that edit.
6. `ARCH-04` stays blocked by `GAP-20-01` unless the user resolves the proof vehicle before planning/execution.
