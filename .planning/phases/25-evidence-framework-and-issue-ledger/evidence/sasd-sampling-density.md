# Evidence Packet: SASD - Stiffness-Aware Sampling Density

## Header

| Field | Value |
|---|---|
| ID | `SASD` |
| Title | Stiffness-Aware Sampling Density endpoint and data-side contract |
| Severity | `MAJOR` |
| Current Status | `DEFERRED` |
| Current Verdict | `defer-with-blocker` |
| Phase | Phase 28 |
| Acceptance Check ID | `AC-VAL-02` |
| Spec Sections Touched | None yet - `ctl_instruction.md` Data-side quality-metric contracts subsection is parked pending GAP-28-01 |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§5.2 Q-C2:L575-L626` | Proposes per-interval SASD with per-body, both-endpoint max, analytic accelerations, raw/scaled invariance, flag-not-auto-reject semantics, floor-effect caveat, optional perpendicular diagnostic, and doc-03 training-use deferral. It explicitly names endpoints as a genuine fork: both-endpoint max is adopted as a candidate because it closes the final/right-endpoint blind spot, while CR-A's DQA-literal left endpoint is preserved as dissent and the project is asked to weigh the consolidation-generated argument. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `L143-L153` | Defines SASD as `SASD_i = dt_i * ||a(t_i)|| / ||v(t_i)||`, says high values flag low-resolution trajectories for resampling, and assigns collocation-weighting use to training. This source is non-authoritative and does not address right-endpoint evaluation or data-side clean-training disposition. |

Do not treat either primary source as authoritative before user resolution. The resolution doc supplies the stronger candidate implementation, but it also preserves the endpoint fork and asks for sign-off.

## Spec Evidence

- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:L138-L158` is the read-only written home of the SASD definition: local characteristic timescale `||v||/||a||`, left-endpoint formula `dt_i * ||a(t_i)|| / ||v(t_i)||`, and `SASD > 0.5` flag-for-resampling framing. It does not specify right-endpoint evaluation.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:L452-L458` establishes the data-side admission-gate pattern: parsed trajectories are screened before stage assignment, `compute_globals`, or training. This supports placing SASD as a data-side contract after Step-1A once the endpoint fork is resolved, but does not answer the endpoint choice.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` currently has no `Data-side quality-metric contracts` subsection and no SASD clause. No SASD spec edit has been made in this packet.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` remains untouched; architecture-facing visibility is deferred until the data-side SASD contract is authorized.

### Dataset Evidence (§3b)

- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:24` (`CLM-09`) records the folder-default `dt_out` context: standard base `dt_out=0.17`, hierarchical base `dt_out=0.08`, and gold variants `dt_out=0.01`.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:25` (`CLM-10`) records the snapshot-resolution context: standard base median 61, hierarchical base median 127, and gold medians 1003. These facts ground the low-resolution floor-effect concern but do not decide whether SASD should evaluate the left endpoint only or both endpoints.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live `pinn/` code is not a v1.5 evidence source and was not consulted for this verdict. FUT-01 will need to implement whichever SASD endpoint convention the user resolves, plus the associated metadata (`max SASD`, argmax interval, `v_floor_hit`, and disposition fields) after the framework specs are finalized.

## Verdict

`defer-with-blocker`

The packet cannot lock a SASD endpoint convention without user instruction. The evidence supports the following engineering facts:

- The DQA and issue doc state a left-endpoint formula.
- The resolution doc proposes a both-endpoint max and gives a first-principles rationale: the right endpoint can expose a spike at `t_{i+1}`, the final snapshot would otherwise never be evaluated, and `max(left,right) >= left`, so both-endpoint evaluation cannot un-flag any trajectory flagged by the DQA-literal form.
- The dataset facts show why low-resolution aliasing matters: base outputs have much coarser `dt_out` and far fewer snapshots than gold outputs.

Those facts do not decide the semantic policy fork. Choosing both endpoints would expand or preserve the flagged set and feed more records into resampling / clean-training exclusion; choosing the DQA-literal left endpoint would avoid expanding flags but knowingly leaves the final/right-endpoint blind spot. Because the candidate verdict source explicitly frames this as a genuine fork with preserved dissent and direct project sign-off, the STOP protocol applies. No SASD spec clause is landed until GAP-28-01 is resolved or explicitly deferred by the user.

## Before / After Spec Note

Before this packet: no canonical SASD contract existed in editable framework specs. DQA §3.2 and issue-02 carried a left-endpoint formula; the resolution doc carried a candidate both-endpoint completion.

After this packet: no framework-spec SASD edit has been made. The intended `ctl_instruction.md` `Data-side quality-metric contracts` subsection remains parked pending GAP-28-01.

## Named Acceptance Check

`AC-VAL-02`

Phase 28 Plan 02 owns AC-VAL-02, but its runnable structural check is parked with the spec edit. Once GAP-28-01 is resolved, AC-VAL-02 must verify the SASD clause, data-side computation contract, low-resolution floor-effect caveat, flag-not-auto-reject semantics, doc-03/M16 forward-reference, packet citation, and no training-loop policy text.

## Status Transition Log

```text
2026-06-16 <pending-28-02-sha> PENDING -> IN_PROGRESS (Phase 28 Plan 02; SASD EVID-06 packet opened and Q-C2 endpoint fork evaluated)
2026-06-16 <pending-28-02-sha> IN_PROGRESS -> DEFERRED (Phase 28 Plan 02; GAP-28-01 opened for SASD endpoint sign-off, no spec edit landed)
```
