# Phase 53: Narrow Spec Codification - Research

**Researched:** 2026-08-19
**Domain:** Framework-spec text transcription (documentation-only phase; no code)
**Confidence:** HIGH — every load-bearing claim verified by direct `Read` of the source-of-truth file this session; no external stack involved

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Apply the convention to §4.1's PHYS-05 values ONLY. Do not sweep the rest of the file. Record the un-swept tables as a routed inventory. (Reversible — a later phase extends the sweep by adding markers.)
- **D-02:** Notation is an inline ASCII marker — `**[LOCKED]**` / `**[DEFAULT]**` — declared in one short dedicated subsection, and defined as attaching to a *value*, not to a table row. ASCII, not emoji (render-fidelity + greppable). The convention states it governs both framework specs, but **zero marker edits in `ctl_instruction.md`**. (Costly to reverse once adopted.)
- **D-03:** Correct the displayed `L_data` formula, add the prose sentence, AND land a contract block. Not prose-only. The formula must be corrected to the explicit triple sum with `1/(N_t · N_b · d)` normalization (equivalently `1/(9 N_t)` at `N_b = 3, d = 3`). This phase changes no code. The edit must state the SCOPE-38 reasoning (resolves an ambiguity; does not amend a contract-marked value). (Reversible.)
- **D-04:** New `## 10.6` subsection in `pinn_architecture.md` §10 Numerical Acceptance Checks. Do NOT place it at `ctl_instruction.md:1939` (that is the per-stage curriculum ADVANCE gate — a different object). Include one disambiguating sentence stating §10.6 is distinct from the per-stage ADVANCE gate. (Reversible.)
- **D-05:** Write the statistic as max over held-out *trajectories*, and do not define the within-trajectory reduction. §10.6 states: max over held-out trajectories of the per-trajectory `ε_H` **as already defined**; fail-if-any-exceeds-`1e-5`; `SCS = log10(max ε_H)`; mean and median are explicitly **non-gating** distribution facts. If the within-trajectory axis is found undefined in the spec, it is a **gap to route**, not a Phase 53 invention. (Reversible.)
- **D-06:** Use the house contract-block pattern with the requirement ID plus the originating GAP ruling. Mint no new `AC-*` IDs. Form: `> **Phase 53 contract: <topic> (<SPEC-NN>; <GAP-ID> owner ruling <date>, option <X>; grounded by <full relative path>).**` (Reversible.)

**Delegation of authority (verbatim boundary):** Owner instruction 2026-08-19 — *"run all the areas worth discussing yourself by choosing the best option automatically following your best judgement and logical reasoning grounded in the mathematics, physics, and codebase. no need to ask the user for their input unless the decision is very important and can create a bigger impact later."* This delegates Phase 53's wording/placement questions only. SCOPE-34's "never agent-decided" rule still binds the recalibration decision (`η_c` / normalization / SIREN-scale / `N_t`) — Phase 54/56 content, not delegated.

**Open Items for Owner Visibility (non-blocking, recorded in CONTEXT):** (1) §2.4's "Recommended Value" header stays wrong after Phase 53 — routed to Phase 56 as first item of the D-01 inventory; (2) correcting a displayed formula (D-03) is a larger edit than "reword" — flagged for owner review at phase close; (3) `ε_H`'s within-trajectory reduction may be undefined — **measured this session: DEFINED (see below); no new gap required.**

### Claude's Discretion
- Plan decomposition (one plan or several across SPEC-02..05; SPEC-02 and SPEC-03 are coupled — land together or in fixed order).
- Commit granularity within `scripts/agent-commit` discipline.
- Exact section number if `## 10.6` collides with concurrent work.
- Exact prose wording, provided every ruling's date, option letter, and source path are carried.

### Deferred Ideas (OUT OF SCOPE)
- Sweeping the locked/default convention across §2.4 and §9 (deferred by D-01; GAP-45-03 explicitly left generalization undecided).
- A cross-reference from `ctl_instruction.md` to the new §10.6.
- Removing the stray preserved author comments (`:249`, `:305`) — SCOPE-33 does not authorize it.
- A preflight/CI test asserting spec markers against the PHYS-05 preflight assertion (tooling work, outside spec-text scope).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SPEC-02 | Reword `pinn_architecture.md` §4.1's `λ_phys^max` line to state the PHYS-05 per-stage table is **locked**, not defaulted; cite GAP-45-03. | Current line quoted verbatim below (Edit Site B); GAP-45-03 ruling text quoted verbatim (index row + full record consequences 1–5). |
| SPEC-03 | Add a spec convention for marking locked-vs-default values **inside a table**; §4.1's PHYS-05 table is marked under it. | D-02 form fixed (`**[LOCKED]**` / `**[DEFAULT]**`, value-attached); placement candidates inventoried (Edit Site D); structural proof that a Status column is impossible at this site (values are LaTeX bullets, not a markdown table). |
| SPEC-04 | Make the `L_data` reduction explicit in spec prose — mean over time, bodies, and spatial components (GAP-45-01 option A, 2026-07-31). | Current formula + author comment + LOSS-01 block quoted verbatim (Edit Site A); GAP-45-01 full record quoted (9× evidence, executable contract sentence); conformance confirmation from `pinn/loss_catalog.py:246-262` quoted. |
| SPEC-05 | Codify the held-out physics gate's aggregate statistic: worst-case max, not mean/median (GAP-44-01, 2026-07-23). | §10 structure enumerated (§10.1–§10.5, insertion point confirmed); GAP-44-01 full record quoted (max = 237.2086056078468, SCS = log10(max)); ADVANCE-gate distinction evidence quoted from `ctl_instruction.md:1922-1976`. |
</phase_requirements>

## Summary

Phase 53 transcribes four already-ratified owner rulings into `pinn_architecture.md`. Every fact needed to plan it is in-repo and was verified byte-for-byte this session: the four edit sites' current text, the three GAP ruling texts, the house contract-block pattern, the SCOPE-38 marker locations, and the render-check baseline. The phase touches exactly one file; `ctl_instruction.md` is read-only; `pinn/` is untouched (CONF-07 already Complete — shipped code already implements the `L_data` mean reduction the spec text will now state).

Three findings materially shape the plan. **First**, the §4.1 edit site sits 8–13 lines below two SCOPE-38 contract markers (`η_c = 1` at `:646-647`, the clip's underflow-only purpose at `:648-650`) inside the same subsection — the edit must be scoped to the warmup bullets `:658-665` and the plan must carry an explicit excluded-lines list so Success Criterion 5 is defensible on inspection. **Second**, the open question CONTEXT D-05 flagged — whether `ε_H`'s within-trajectory reduction is defined — resolves as **DEFINED**: `ctl_instruction.md:567` locks per-trajectory `eps_H = max_t |(H(t) - H(0)) / H(0)|`, and the Phase 44 gap record confirms that is the held-out gate's per-trajectory object. No new gap is authored; §10.6 references the existing definition rather than restating it. **Third**, the §3.1 edit site lies entirely inside the render-checker's ±20-line D5/D6 author-flag window (`:285-:325` around the `:305` flag), so any backtick-wrapped ASCII math added there generates new REVIEW findings — the corrected formula must go in `$$…$$` display math.

**Primary recommendation:** Three strictly-sequential edits to one file, planned as either one plan with ordered tasks or three single-task plans — (1) convention subsection + PHYS-05 marking (SPEC-02+SPEC-03 land together per SC-2), (2) §3.1 `L_data` formula correction + prose + contract block (SPEC-04), (3) `### 10.6` held-out-gate subsection (SPEC-05) — each gated by the render oracle and the SCOPE-38 byte-identity diff assertion in the Validation Architecture below.

## Project Constraints (from CLAUDE.md)

Directives binding this phase, extracted from `CLAUDE.md` and repo rules:

- **STOP protocol in full force.** Phase 53 is inside an adjudication-style milestone. Any wording question the four rulings do not answer is routed as a gap (create `53-GAPS.md` + `.planning/milestones/v2.3-GAPS.md` under the standing trigger), never decided inline (SC-5).
- **`pinn/` live code is NOT a grounding source.** It is read-only conformance context here (CONF-07 confirmation only). No spec value may be derived from it.
- **Spec-edit targets:** `pinn_architecture.md` only this phase; `ctl_instruction.md` read-only (D-02/D-04); `sampling_method.md` frozen; `data_quality_assessment.md` read-only.
- **Preserved author comments are not cleanup targets.** Eight `Author Comment` instances exist in `pinn_architecture.md` (`:103, :188, :249, :282, :286, :305, :542, :699`); SCOPE-33 does not authorize removing them. Edit around them.
- **Commit protocol:** `scripts/agent-commit` only; `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` set; stage explicit paths (the spec file + phase artifacts), never blanket staging; message `<type>(<scope>): <subject>` — here `spec(53): …`; body required (touches framework specs + `.planning/`); `Agent-Assisted-By:` trailer required.
- **Branch/worktree:** all work in `.worktrees/trainex` on `milestone/v2.3` (verified this session: `git worktree list`); no direct push from `milestone/*`.
- **REQUIREMENTS.md checkboxes** (SPEC-02..05) are flipped at phase close/verification, not by the executor — house precedent recorded in STATE.md (CONF-09/CONF-02/RUN-01/RUN-02).

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Normative statement of the four rulings | Framework-spec docs (`pinn_architecture.md`) | `ctl_instruction.md` (read-only distinction evidence) | SCOPE-33 authorizes narrow spec edits; D-02/D-04 fix the file |
| Ruling provenance / grounding | `.planning` gap registers (44-GAPS, 45-GAPS) | Milestone index `v2.1-GAPS.md`; VER-20 handoff | STOP-protocol registers are authoritative resolution records |
| Render fidelity of edited spec | `tools/spec-render-check` oracle | Committed adjudication allowlists | Phase 22 D-08/G1/G2 house gate; same KaTeX engine as Cursor preview |
| Edit verification | Textual assertions (grep / `git diff` byte-identity) | Render oracle | Docs-only phase — no runtime behavior exists to test |
| Code conformance of `L_data` reduction | None this phase | `pinn/loss_catalog.py` (read-only confirmation) | CONF-07 Complete in v2.2; D-03 changes spec only |

## Edit Site Inventory (verbatim current text)

All quotes below were captured by direct `Read` this session. Line numbers are current as of worktree HEAD `7f9902d2` on `milestone/v2.3`.

### Edit Site A — §3.1 `L_data` (SPEC-04 / D-3)

`pinn_architecture.md:292-310` [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:292-310]:

```
292  ## 3.1 Data Fidelity Term ($\mathcal{L}_{\text{data}}$): Anchoring to Ground Truth
...
300  The data fidelity loss uses a Huber contract on scaled projected
301  positions:
302
303  $$L_{data} = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$
304
305  Author Comment: again, the syntax is broken
306
307  where $\delta_r = 1$ is the default Huber transition. The previous
308  MAE/L1 data-loss prose is replaced by this Huber contract.
309
310  > **Phase 35 contract: loss scaling and units (LOSS-01; NS-18 modified; AC-LOSS-01; grounded by the resolution doc §1.14 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`).** `pinn_architecture.md` is the canonical component-math home for data, physics, energy, and angular-momentum terms; `ctl_instruction.md` owns total-loss assembly and methodology cross-references by stable section heading plus AC ID. The component contract uses dimensionless `u=t/T` and `r'=r/D`, projected scaled positions for Huber data loss, ordered raw mass metadata where COM/force terms require masses, matched `epsilon_train = 1e-5` for force and Hamiltonian terms, separate data-fidelity snapshot points from physics/energy collocation points, the IC anchor, the angular-momentum regularizer, and no linear-momentum / no-linear-momentum-loss term.
```

The symbol legend follows at `:312-323` (`$u_n = t_n/T$`, `$r'_{\theta,i}(u_n)$`, `$r'_i(u_n)$`, `$N_t$`); batch construction at `:325-347`; a second contract block (Phase 34 / SI-PINN-003 + PIPE-04 note) at `:353-355`; "Loss Integration Note" at `:357-360` (*"The data term is unweighted in the default objective."*).

**Citation corrections vs CONTEXT.md** (immaterial to content, material to plan anchors): the formula is at **`:303`** (CONTEXT said `:304`); the author comment at **`:305`** (said `:306`); the LOSS-01 contract block starts at **`:310`** (said `:307` — `:307` is the `δ_r` prose).

**SCOPE-38 defensibility evidence for D-03** (must be restated in the edit's contract block): GAP-45-01's source-silence record [VERIFIED: .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md:45-54] — *"The §3.1 Phase 35 LOSS-01 contract note specifies units, frames, and which file owns the component math; it does not state the reduction."* The reduction was genuinely undetermined; correcting it resolves an ambiguity rather than superseding a ruling. Also: every neighboring term states its reduction explicitly (`L_IC` `(1/3)Σ`, `L_L` `(1/(3N_t))ΣΣ`, `L_phys` `(1/N_t)Σ`, `L_E` `(1/N)Σ`) — `L_data` is the only under-specified term (45-GAPS.md:36-40).

### Edit Site B — §4.1 PHYS-05 warmup block (SPEC-02 / SPEC-03 / D-01 / D-02)

`pinn_architecture.md:633-669` [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:633-669]. The where-block `:639-656` contains the SCOPE-38-marked `L_phys` bullet — **DO NOT TOUCH**:

```
645  - $L_{phys}^{causal}$: Physics residual with causal weighting
646    $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
647    $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
648    causal exponent to avoid underflow, but do not choose a numeric
649    clipping bound in Phase 19; surface a gap if one is needed.
650    The causal exponent clip is required only to avoid underflow.
```

The edit target — warmup schedule bullets `:658-665`:

```
658  The warmup schedule is:
659
660  - $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
661  - $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
662    default $\lambda_{phys}^{max}(k) = 1$
663  - $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$
664  - $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with
665    $i/I_{warm}$
```

Existing Phase 35 blocks immediately below: LOSS-02 contract at `:667`, guard at `:669` (both quoted in the census below). Optimizer-phase semantics prose at `:671-678`; section ends at `:683` (`## 4.2` starts `:684`).

**Structural fact for D-02:** the PHYS-05 values are bulleted LaTeX (`:660-665`), not a markdown table — a Status column is structurally impossible here; the value-attached inline marker is the only form that works. Also in §4.1's where-block, two further "default" wordings stay unmarked under D-01: `$\delta_r = 1$ default` (`:641-642`) and `$\lambda_{IC} = 1$ default` (`:643-644`).

### Edit Site C — §10 Numerical Acceptance Checks (SPEC-05 / D-04 / D-05)

`pinn_architecture.md:1014-1041` [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:1014-1064]. Existing subsections, all `###`-level under the `# 10.` H1:

| Subsection | Title | Lines |
|---|---|---|
| `### 10.1` | Scaling Consistency | `:1016-1019` |
| `### 10.2` | COM Invariance | `:1021-1024` |
| `### 10.3` | Componentwise AD on Synthetic Trajectory | `:1026-1029` |
| `### 10.4` | Force-Energy Consistency | `:1031-1034` |
| `### 10.5` | Loss Stability Dry Run | `:1036-1039` |

Section body ends at `:1039`; `---` separator at `:1041`; `## Source Issues / Notes for Future Reconciliation` at `:1043` (SI-PINN-002 `:1047`, SI-PINN-003 `:1056`); file ends `:1064` (*"End of faithful converted body. Source Issues section above is metadata excluded from fidelity comparison (D-19)."*).

**Insertion point:** new subsection between `:1039` and `:1041`, keeping it inside the faithful converted body. **Style correction to D-04's shorthand:** existing subsections use `### 10.N` (H3), so the new subsection should be `### 10.6 <Title>` — CONTEXT's "`## 10.6`" was informal; match house style. Each existing subsection carries `- **Pass Criterion**` / `- **Input Data**` / `- **Execution**` bullets; §10.6 is a gate-*definition* contract rather than a probe, so matching the three-bullet form exactly is optional — but a contract block per D-06 is mandatory.

### Edit Site D — new convention subsection (SPEC-03 / D-02)

**No existing conventions / how-to-read section exists** [VERIFIED: structure grep of `pinn_architecture.md` — headers at `:6` (title), `# 1.` `:8`, `# 2.` `:105`, `# 3.` `:268`, `# 4.` `:627`, `# 5.` `:774`, `## References` `:994`, `# 10.` `:1014`, `## Source Issues` `:1043`]. The document goes YAML frontmatter (`:1-4`) → title (`:6`) → `# 1.` narrative (`:8`). Candidates:

| Candidate | Verdict | Rationale |
|---|---|---|
| **(a) Unnumbered preamble immediately after the title (`:6`), before `# 1.` (`:8`)** | **Recommended** | File-wide scope matching D-02's "governs both framework specs"; zero renumbering; additive diff; outside every D5/D6 author-flag window (nearest flag `:103`, window ends `:123` — a preamble at `:7-:30`… note: keep it short so it stays above `:83`; see Pitfall 2) |
| (b) Inside `## Source Issues` (`:1043+`) | Rejected | That section is metadata *excluded from fidelity comparison* (D-19, `:1045`); a normative convention does not belong in a metadata section |
| (c) Inside §4.1 adjacent to the application site | Rejected | Understates the convention's two-file authority; §4.1 is already dense and adjacent to SCOPE-38 markers |
| (d) New numbered section | Rejected | The file's numbering is already anomalous (no §6–§9 exist; §10 follows §5 + References); a new number invites confusion |

**Recommendation (a)**, with a mechanical guard: the first author flag is at `:103` (D5/D6 window `:83-:123`); the preamble plus frontmatter shift must keep all added lines above line 83 of the post-edit file — trivially satisfied by a ~15-line subsection — and must contain no backtick-wrapped ASCII math regardless.

**Numbering anomaly to note in the plan:** sections 6–9 do not exist as headers. CONTEXT D-01's "§9's 'Definitive Specification' table (`:978-:992`)" refers to **Table 2 under `## 5.3`** (`:976-992`) [VERIFIED: pinn_architecture.md:976-992 — header row at `:978`: `| **Component** | **Definitive Specification** | **Justification** |`]. Plans should cite it as "Table 2 (`:976-:992`)" to avoid implying a §9 exists.

## Ruling Texts (verbatim)

### GAP-45-03 — PHYS-05 table locked (SPEC-02 / SPEC-03 authority)

Milestone index row [VERIFIED: .planning/milestones/v2.1-GAPS.md:15] — note CONTEXT cited `:12`; the row is at **`:15`** (`:12` is GAP-44-02):

> "| GAP-45-03 | 45 | process-artifact schema | RESOLVED-WITH-INSTRUCTION | Owner instruction 2026-07-24 (option A): **the per-stage `λ^max(k)` values are locked** — the full PHYS-05 table binds, not just the warmup form plus the `≤1` cap. Preflight asserts the entire table at run start and every stage boundary; overriding any value is a violation; the misleading "default" wording on the adjacent `λ_phys^max` line is routed to a spec-editing milestone. Generalization to other spec tables NOT decided. Full record: `45-GAPS.md`. |"

Full-record resolution note [VERIFIED: .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md:317-341], consequences 4–5 are the direct SPEC-02/03 authorities:

> "**Option A — the per-stage `λ^max(k)` values are locked.** The full PHYS-05 table binds, not merely the warmup form plus the `≤1` cap; the `10^(k−4)` ramp is a designed decision about how conservation pressure enters the curriculum, not a placeholder default. Consequences, all owner-authorized by this ruling: … 4. The "default" wording on the adjacent `λ_phys^max(k) = 1` line in `pinn_architecture.md` §4.1 is now known to be misleading relative to this ruling. Correcting that wording is a **spec edit** and therefore out of scope here (SCOPE-24, and v2.1 edits no spec); it is routed to a spec-editing milestone. Recorded so the ambiguity is not re-litigated. 5. Generalization beyond PHYS-05 was **not** decided: this ruling settles the PHYS-05 table's lock granularity. Whether framework-spec tables carry locked per-row values *by default* remains unstated, and a spec convention for marking locked-vs-default within a table is still absent. Flagged for the spec-editing milestone rather than assumed."

Consequence 5 is the explicit owner withholding that D-01 honors: a sweep would reverse a standing ruling.

### GAP-45-01 — `L_data` reduction (SPEC-04 authority)

Milestone index row [VERIFIED: .planning/milestones/v2.1-GAPS.md:13]:

> "| GAP-45-01 | 45 | semantic | RESOLVED-WITH-INSTRUCTION | Initial owner instruction 2026-07-24 (option C) deferred the `L_data` component reduction to the next conformance-fix phase with a pre-re-run condition. **Final owner ruling 2026-07-31 at the Phase 48 checkpoint: option A, mean over time, bodies, and spatial components.** Both readings were presented against retained-run magnitudes: mean `0.1539..0.1630`; sum `1.3852..1.4673` (exactly 9×). The retained runs were non-conformant and lacked per-term gradient statistics, so the selection rests on the owner-ratified per-coordinate convention, not on those runs or on live-code precedent. The later VER-20 spec amendment must make the reduction explicit. Full record: `45-GAPS.md`. |"

Full-record final resolution [VERIFIED: .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md:114-128]:

> "**Final resolution 2026-07-31 (Phase 48 owner checkpoint): Option A — mean over all components.** Phase 48 presented both readings against the retained Stage-0 runs. The implemented per-coordinate mean produced run-average `L_data = 0.1539..0.1630`; the sum-over-components reading produced exactly 9× those values, `1.3852..1.4673`. The retained runs were non-conformant and lacked per-term gradient statistics, so these magnitudes did not establish intent. The orchestrator recommended Option A because a per-coordinate Huber mean keeps `delta_r = 1` coordinate-local, remains invariant to tensor cardinality, and avoids encoding a body/component-count multiplier inside the one term whose coefficient is fixed at 1. The owner replied `proceed` after the explicit recommendation and ratification request. The executable contract is therefore `mean(Huber(residual), axes=(time, body, spatial_component))`. The spec formula still requires an explicit reduction amendment through VER-20; no framework-spec edit is authorized in v2.2."

Arithmetic cross-check: 9 × 0.1539 = 1.3851 ≈ 1.3852; 9 × 0.1630 = 1.467 ≈ 1.4673; 9 = 3 bodies × 3 spatial components. The current formula (`:303`) normalizes by `1/N_t` only — mean over time, sum over bodies, components undefined — i.e., it computes 9× the ratified quantity under the implicit-sum reading.

### GAP-44-01 — held-out gate aggregate statistic (SPEC-05 authority)

Milestone index row [VERIFIED: .planning/milestones/v2.1-GAPS.md:11]:

> "| GAP-44-01 | 44 | semantic | RESOLVED-WITH-INSTRUCTION | Owner instruction 2026-07-23 (option A): the held-out physics-gate `eps_H` headline is the **worst-case max** — the gate fails if ANY trajectory exceeds `1e-5`, headline `max = 237.2086056078468` (confirms the evaluator's rendering; consistent with `SCS = log10(max)`). Verdict-neutral (100% of trajectories fail individually). `44-DIAGNOSIS.md` designates max as the gate number; mean/median stay quoted as distribution facts. Full record: `.planning/phases/44-physics-gate-forensics/44-GAPS.md`. |"

Full-record resolution note [VERIFIED: .planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md:111-124]:

> "Owner instruction 2026-07-23 (interactive session, AskUserQuestion): **Option A — the worst-case max is the spec-intended gate statistic.** The held-out physics gate fails if ANY trajectory's `eps_H` exceeds `1e-5`, and the headline is `max(per_trajectory.eps_h) = 237.2086056078468` — confirming the evaluator's rendering, consistent with the per-trajectory reject rule applied set-wide, 43-VERDICT's citation, and the preserved aggregate `SCS = log10(max)`. Applied: `44-DIAGNOSIS.md` (GAP-44-01 section, §2 gate table, §7) updated to designate max as THE gate number with this grounding; mean (5.6222) and median (2.2327) remain quoted as distribution facts, not gate numbers; `v2.1-GAPS.md` row updated. Codifying the aggregate-statistic wording into `ctl_instruction.md` is NOT done here (SCOPE-24 — Phase 44 edits no spec); it remains available to a later spec-editing milestone if the owner wants the gate definition to state it explicitly."

Supporting distribution facts (44-GAPS.md:14-18, :33-36, :74-77): mean = 5.622187097745829, median = 2.232675867436938, min per-trajectory `eps_h` = 0.9741251227996501 (already ~5 orders above `1e-5`; 1500/1500 trajectories fail individually — the aggregate choice is verdict-neutral).

**Placement note for the plan's traceability:** the GAP-44-01 resolution note contemplates codification *"into `ctl_instruction.md`"* as non-binding availability language ("it remains available … if the owner wants"). D-04 (locked, under the 2026-08-19 delegation of placement questions) overrides with a correctness finding — the only "held-out" hit in either spec is the per-stage ADVANCE gate at `ctl_instruction.md:1939`, a different object. The §10.6 contract block should carry this one clause of placement reasoning so a later reader does not re-litigate it.

### VER-20 routing handoff, items (a)–(d) (the routing authority)

[VERIFIED: .planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:9-26]:

> "**(a) Misleading "default" wording on `pinn_architecture.md` §4.1's `λ_phys^max` line.** The line reads as though the value is a tunable default; GAP-45-03 ratified that the full PHYS-05 per-stage table is locked, not defaulted. Needs rewording to state the table binds.
>
> **(b) Convention for marking locked-vs-default values inside a spec table.** No existing spec convention distinguishes a locked constant from an illustrative default within the same table. GAP-45-03's ruling exposed the gap; item (a) is one instance of a systemic wording problem.
>
> **(c) Explicit `L_data` reduction, settled by CONF-07.** GAP-45-01 resolved (2026-07-31, Phase 48 checkpoint): mean over time, bodies, and spatial components. The spec should state this explicitly rather than leaving it inferable from code.
>
> **(d) Aggregate gate statistic from GAP-44-01.** The held-out physics gate's headline statistic (worst-case max, not mean or median) was owner-ruled 2026-07-23 but is not codified in the spec."

Disposition (`:61-66`): items (a)–(d) are *"narrow wording/codification fixes with no open research question."*

## Contract-Block Census (the house pattern Phase 53 must match)

Exact counts this session (patterns: `^> \*\*Phase [0-9]* contract:` anchored; `> \*\*Phase [0-9]* contract:` anywhere; `^> \*\*Phase [0-9]* guard:`):

| File | Anchored contract blocks | Indented contract blocks | Guard blocks |
|---|---|---|---|
| `pinn_architecture.md` | **9** (`:310, :353, :424, :537, :625, :667, :686, :726, :890`) | 0 | **1** (`:669`) |
| `ctl_instruction.md` | **17** | **2** (`:1182, :1333`) | **1** (`:1771`) |

[VERIFIED: grep counts this session]. CONTEXT's "9 in pinn_architecture.md + 18 in ctl_instruction.md + 2 guard blocks" and D-06's "26 contract blocks and 2 guard blocks" reconcile as: 26 = 9 + 17 **line-start** blocks; the indented pair in `ctl_instruction.md` brings that file's true total to **19**, not 18. The pattern's dominance is unaffected; plans should quote the exact census (9 / 17+2 / 2) rather than CONTEXT's rounded figures.

**Exemplar 1** — `pinn_architecture.md:667` (Phase 35 / LOSS-02) [VERIFIED: pinn_architecture.md:667]:

> "> **Phase 35 contract: energy-loss weights (LOSS-02; M15 rejected as issue-doc replacement; AC-LOSS-02; grounded by the resolution doc §1.9 and `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md`).** Retain the PHYS-05 warmup schedule above with `lambda_E^max <= 1` and scheduled conservation weights at or below one. The issue-doc cap-table replacement and stale high-energy-weight premise are rejected, not adopted as a locked schedule. Before any future control law, log weighted losses, scheduled weights, and gradient statistics; automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists."

**Exemplar 2** — `pinn_architecture.md:310` (Phase 35 / LOSS-01): quoted in full at Edit Site A above.

**D-06 form applied** (GAP citation substitutes for the AC-ID slot; no new AC IDs minted):

- SPEC-02/03 site: `> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03; GAP-45-03 owner ruling 2026-07-24, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).**`
- SPEC-04 site: `> **Phase 53 contract: L_data component reduction (SPEC-04; GAP-45-01 owner ruling 2026-07-31, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).**` — plus the magnitude pair `0.1539..0.1630` vs `1.3852..1.4673` in the block body (CONTEXT specifics: *"Cite those numbers in the edit's contract block — they are what makes the ruling legible to a later reader"*).
- SPEC-05 site: `> **Phase 53 contract: held-out physics-gate aggregate statistic (SPEC-05; GAP-44-01 owner ruling 2026-07-23, option A; grounded by .planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md).**`

Use the **archived** milestone paths above; the v2.1 index's inline `Full record:` citations point at the pre-archive `.planning/phases/44-...` / `.planning/phases/45-...` paths, which no longer resolve (CONTEXT canonical_refs verified the archived paths 2026-08-19; directory listing re-verified this session).

## ε_H Within-Trajectory Reduction — Measurement (agenda item 4)

**Verdict: DEFINED. No routed gap is authored.**

The locked per-trajectory definition [VERIFIED: pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:565-577]:

> "5. Conservation gate (locked post-v1.3; SI-DQA-003). With H evaluated in float64 using Plummer softening `eps = 1e-10` in V:
> `eps_H = max_t |(H(t) - H(0)) / H(0)|`, `SCS = log10(eps_H)`.
> REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`). `SCS = -5` exactly is
> Marginal: admitted, flagged for review. …"

The within-trajectory reduction is **`max_t` — maximum over time** (`:567`). That this is the same per-trajectory object the held-out physics gate consumes is confirmed by the Phase 44 gap record [VERIFIED: 44-GAPS.md:47-52 (source silence) and :67-69 (grounding)]:

> "`ctl_instruction.md:567-572` defines per-trajectory `eps_H = max_t |(H(t) - H(0)) / H(0)|` and the per-trajectory reject rule `eps_H > 1e-5` (equivalently `SCS > -5`). It does NOT define the aggregate held-out statistic over the 1,500 test trajectories (max vs mean vs median vs fraction-failing)."
> "Per-trajectory `eps_H` is the max over time of the relative Hamiltonian drift — a worst-case-over-time measure for one trajectory."

So: the **across-trajectory** aggregate was the silent axis (ruled by GAP-44-01: worst-case max); the **within-trajectory** reduction was and is locked (max over time, post-v1.3 / EVID-10 lineage, listed among the prior locked decisions v2.3 does not reopen — REQUIREMENTS.md:70-75). D-05's instruction lands cleanly: §10.6 writes the aggregate over per-trajectory `ε_H` "as already defined" — cite `ctl_instruction.md`'s locked definition rather than restating or altering it.

**Two disambiguation hazards §10.6 must steer around** (measurement only, no resolution proposed):

1. `ctl_instruction.md:578-580` — *"This validation-gate `eps_H` is distinct from the training-loss `eps_H = 1e-4*S_H` in `pinn_architecture.md` §3.4: same glyph, different quantity."* The glyph `ε_H` names two different quantities; §10.6 must make clear it speaks of the **validation-gate** `ε_H`.
2. `ctl_instruction.md:1971-1976` — the ADVANCE gate's energy-conservation check (criterion 4 of 4) uses **final value** (`t_final`) and **mean over trajectories** with the *training-loss* denominator `epsilon_H = 1e-4 * S_H` and threshold `ε_energy = 10⁻⁴`. This is the per-stage curriculum gate (D-04's conflation target), a different metric with a different reduction on both axes. D-04's required disambiguating sentence covers `ctl_instruction.md:1939`; the plan should also ensure no reader maps §10.6's max-over-trajectories onto `:1976`'s mean-over-trajectories form.

SCOPE-35 (REQUIREMENTS.md:116) budgets exactly one held-out evaluation; nothing in Phase 53 spends or touches it — §10.6 is a definition of the statistic, not an evaluation.

## SCOPE-38 Adjacency Check (agenda item 5)

The three owner-ratified contract markers and every occurrence in `pinn_architecture.md` [VERIFIED: grep this session; quoted lines from Reads above]:

| Marker | Occurrences | Nearest edit site | Distance / verdict |
|---|---|---|---|
| `η_c` (`eta_c`) | `:414` (§3.2 formula `w_n = exp(−η_c Σ …)`); `:424` (LOSS-04 contract block, `eta_c = 1`); `:646-647` (§4.1 `L_phys` bullet, `$\eta_c = 1$ default`) | §4.1 warmup bullets `:658-665` | **`:646-647` is 11 lines above `:661` — inside the same subsection, outside the edit block.** Edit must be scoped to `:658-665` (plus contract-block insertion after `:665`/before `:667`); `:645-650` excluded |
| `first_omega_0` | `:167` (§2.2 lock: "`first_omega_0` is fixed at `30` and is not scheduled during training"); `:170`; `:260` (§2.4 table row); `:983` (Table 2 row); (`:130/:132/:156` math context) | §10.6 insertion (`:1039-1041`) | `:983` is ~56 lines above the insertion point; §2.2/§2.4 are Phase 56 territory — untouched |
| Clip underflow-only purpose | `:648` ("Clip the causal exponent to avoid underflow…"), `:650` ("The causal exponent clip is required only to avoid underflow.") — **only** in §4.1's `L_phys` bullet | §4.1 warmup bullets `:658-665` | Same bullet as `η_c`; excluded with it |

**Conclusion:** no edit site contains or touches a SCOPE-38 marker line, *provided* the §4.1 edit is scoped to the warmup bullets and the new contract block. The plan should carry an explicit excluded-lines list (`:639-656` where-block, especially `:645-650`) and the negative diff assertion from the Validation Architecture below, so SC-5 is defensible on inspection rather than by claim.

**§4.1-internal hazard the CONTEXT did not enumerate:** `$\eta_c = 1$ default` at `:647` carries the word "default" *and* is a SCOPE-38-marked value Phase 56 may amend. Under D-01 (PHYS-05 values only) it stays unmarked — stamping it `[LOCKED]` would couple Phase 53 to the recalibration outcome, the exact failure D-01's §2.4 reasoning warns against. The D-01 un-swept inventory should list it explicitly with that reasoning.

## D-01 Un-Swept Inventory (seed for the routed deliverable)

"Default"/"recommended" wordings that intentionally remain unmarked after Phase 53 [all VERIFIED by grep/Read this session]:

| # | Location | Text | Why un-swept |
|---|---|---|---|
| 1 | `:253` + `:260` | §2.4 Table 1 header "**Recommended Value**"; row `first_omega_0 \| 30` | CONTEXT Open Item 1 — routed to Phase 56; SCOPE-38-amendable value |
| 2 | `:307` | §3.1 "where `$\delta_r = 1$` is the default Huber transition" | Adjacent to Edit Site A; not a VER-20 item; do not reword while editing §3.1 |
| 3 | `:641-644` | §4.1 where-block `$\delta_r = 1$` default; `$\lambda_{IC} = 1$` default | D-01 scopes to PHYS-05 values only |
| 4 | `:647` | §4.1 `$\eta_c = 1$` default | SCOPE-38-marked; Phase-56-coupled (hazard above) |
| 5 | `:433, :440` | §3.2 `n_col=4096` / "recommended: 2048-4096" | SPEC-06 territory (Phase 56) |
| 6 | `:978-992` | Table 2 "Definitive Specification" (mixes locked `epsilon_train=1e-5` with defaults `δ_r=1`, `λ_IC=1`) | CONTEXT D-01: ~15 fresh adjudications no ruling covers |
| 7 | `:357-360` | §3.1 Loss Integration Note "unweighted in the default objective" | "default" modifies the objective formulation, not a table value |

## Standard Stack

No runtime libraries — this phase's "stack" is the repo's own spec-tooling.

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `tools/spec-render-check/detect.mjs` | committed; deps pinned `markdown-it@14.2.0`, `@vscode/markdown-it-katex@1.1.2`, `katex@0.16.47` | Render-fidelity oracle for framework specs (same KaTeX engine as the Cursor/VS Code preview) | Phase 22 D-08/G1/G2 house gate [CITED: tools/spec-render-check/README.md] |
| `git diff` / `grep -F` | system | Byte-identity and literal-string assertions | Only verification surface a docs-only phase has |
| `scripts/agent-commit` | repo | Governed commit path | CLAUDE.md mandatory |

**Environment setup (one-time per worktree):** `node_modules/` for the detector is git-ignored; restore with `cd tools/spec-render-check && npm ci` (10 packages, committed lockfile; done this session — baseline below is reproducible).

## Package Legitimacy Audit

**Not applicable — Phase 53 installs no packages.** The only npm surface is restoring the render-checker's *pre-existing* pinned dependencies via `npm ci` from the committed `package-lock.json`. Those three packages were supply-chain-vetted in Phase 22 (T-22-01: canonical repos, exact names, MIT licenses, `--save-exact`) [CITED: tools/spec-render-check/README.md:10-35]. No new dependency is introduced; no `postinstall` surface changes.

## Architecture Patterns

### Pattern 1: House contract block
**What:** A `> **Phase NN contract: <topic> (<REQ-ID>; <disposition>; <AC-ID>; grounded by <paths>).**` blockquote immediately adjacent to the text it binds, recording provenance densely (requirement, ruling, acceptance check, grounding path). 26 line-start instances + 2 guard blocks across the two specs.
**When to use:** Every Phase 53 edit lands one (D-06), with the GAP citation in the AC-ID slot.
**Example:** Exemplars at `:310` and `:667`, quoted above.

### Pattern 2: Converted-from-LaTeX Markdown discipline
**What:** Specs are pandoc-converted Markdown headed for a deferred LaTeX sync; display math in `$$…$$` on its own lines (mid-line `$$` is a D4 DEFINITE finding); inline math `$…$`; preserved author comments are load-bearing metadata tracked in Source Issues (SI-PINN-002).
**When to use:** All four edits. ASCII-only additions; no emoji (D-02); no new backtick-ASCII-math inside author-flag windows.

### Anti-Patterns to Avoid
- **Sweeping markers beyond PHYS-05:** reverses GAP-45-03's explicit withholding (consequence 5). D-01.
- **A markdown-table Status column:** structurally impossible at the one application site (values are LaTeX bullets). D-02.
- **Prose-only `L_data` fix:** leaves the displayed formula computing 9× the ratified quantity; fails SC-3. D-03.
- **Placing the gate statistic at `ctl_instruction.md:1939`:** conflates the terminal held-out physics gate with the per-stage ADVANCE gate. D-04.
- **Redefining per-trajectory `ε_H` inside §10.6:** the within-trajectory reduction is already locked (`max_t`, CT `:567`); restating it risks divergence. D-05.
- **Minting new `AC-*` IDs at discuss/plan time:** the AC namespace is reserved for acceptance checks defined by phase plans; authority here is the GAP rulings. D-06.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Render fidelity of edited spec | Eyeballing Markdown / a new linter | `node tools/spec-render-check/detect.mjs <file>` (with committed allowlists) | Same KaTeX engine as the target previewer; six detector layers; committed adjudication state |
| Provenance format for ratified rulings | A new callout syntax or footnote scheme | The `> **Phase NN contract:**` blockquote (D-06 form) | 28-instance house pattern; VER-21 traceability stays clean |
| Unanswered wording questions | Reasonable-looking inline choices | `53-GAPS.md` + `v2.3-GAPS.md` under the STOP protocol | SC-5; the milestone's entire governance model |
| Post-edit diff review | Manual re-read | `git diff -U0` scoped greps (Validation Architecture) | Byte-identity on SCOPE-38 markers is the SC-5 defense |

**Key insight:** this phase's risk is entirely transcription fidelity and scope discipline — every needed artifact (rulings, patterns, gates) already exists in-repo; the only way to fail is to invent or to touch what is marked.

## Common Pitfalls

### Pitfall 1: Editing §4.1 past the warmup bullets
**What goes wrong:** the §4.1 reword bleeds into the `L_phys` bullet `:645-650`, altering `η_c = 1` or the clip's underflow-only sentence — a SCOPE-38 amendment without re-ratification.
**Why it happens:** the markers live in the same subsection, 8–13 lines above the target lines.
**How to avoid:** plan scopes the edit to `:658-665` + contract-block insertion; verification runs the marker-line byte-identity diff.
**Warning signs:** `git diff -U0` shows any `-`/`+` line containing `eta_c` or `underflow`.

### Pitfall 2: New REVIEW findings from the D5/D6 author-flag windows
**What goes wrong:** the render oracle emits new REVIEW findings post-edit even with zero DEFINITEs.
**Why it happens:** D5/D6 scan ±20 lines around every author marker; the §3.1 edit site sits wholly inside the `:305` flag's window (`:285-:325`); §4.2 findings (`:686-695`) sit in the `:699` flag's window (`:679-719`).
**How to avoid:** write the corrected `L_data` formula in `$$…$$` display math and the reduction prose in words/`$…$` — never backtick-wrapped ASCII math — inside that window; keep the convention preamble above line 83 post-edit (before the `:103` flag's window opens).
**Warning signs:** `detect.mjs` output gains `§3-1-…` REVIEW lines absent from the baseline below.

### Pitfall 3: Breaking the adjudication allowlist by line shifts
**What goes wrong:** previously-adjudicated findings reappear as unadjudicated REVIEWs.
**Why it happens:** allowlist matching is file + **1-based line number** + token; edits shift lines.
**How to avoid:** all 7 adjudicated entries are at `:170-261`, above the first edit site (`:292`); keep the convention preamble at the title (adds lines above `:103`? — no: inserting after `:6` shifts `:170+` down!). **Correction:** a title-level preamble *does* shift the adjudicated lines. Mitigation options: (a) place the convention subsection after `# 1.`'s prose… also shifts; (b) accept the shift and re-derive the allowlist — out of scope; (c) **preferred:** place the convention subsection anywhere and note that the 7 adjudicated entries will shift uniformly; the gate is then *content-based* (same 7 tokens adjudicated at shifted lines no longer match → they surface as REVIEW). Re-deriving `22-02-pinn-architecture.json` line numbers is a mechanical, seven-entry update the plan may include as a task — it is an existing committed artifact keyed to line numbers, and Phase 53's edits legitimately move them. Decide in plan: either update the allowlist in the same commit (recommended; keeps the oracle gate green) or gate on content-diff of findings.
**Warning signs:** post-edit run shows `first_omega_0`/`elementwise_affine` REVIEWs at §2 lines.

### Pitfall 4: Treating GAP-44-01's resolution-note file mention as binding
**What goes wrong:** planner "corrects" D-04 by moving §10.6 content into `ctl_instruction.md`.
**Why it happens:** the resolution note says codification "into `ctl_instruction.md` … remains available."
**How to avoid:** that sentence is availability language ("if the owner wants"), not a ruling on file choice; D-04 is the locked placement decision under the 2026-08-19 delegation, grounded in the ADVANCE-gate conflation finding. The §10.6 contract block carries the one-sentence placement reasoning.

### Pitfall 5: `**[LOCKED]**` mistaken for a preserved author comment
**What goes wrong:** SI-PINN-002 records that author comments were once rendered "as bold bracketed text (`**[...]**`)" — visually identical to the D-02 marker.
**How to avoid:** the convention subsection explicitly defines the two markers and their value-attached semantics; current author comments are plain `Author Comment:` prose (`:103` etc.), so no live collision exists — but the convention text should say markers are status annotations, not preserved comments.

## Code Examples

Verified patterns from the sources read this session (edit *templates* — exact wording is planner discretion under CONTEXT, but dates/options/paths are load-bearing):

### SPEC-02/03 — marker application at §4.1 (`:661-663` region)
```markdown
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  $\lambda_{phys}^{max}(k) = 1$ **[LOCKED]**
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$ **[LOCKED]**
```
Followed by the D-06 contract block (form above). The word "default" attached to `λ_phys^{max}` is removed — that removal *is* SPEC-02.

### SPEC-04 — corrected formula (display math, per Pitfall 2)
```markdown
$$L_{data} = \frac{1}{N_t \, N_b \, d} \sum_{n} \sum_{i} \sum_{c} \operatorname{Huber}_{\delta_r}(r_{\theta,i,c}'(u_n) - r_{i,c}'(u_n))$$
```
plus prose stating the reduction is the **mean over time, bodies, and spatial components** (equivalently `1/(9 N_t)` at `N_b = 3, d = 3`), the ruling citation, and the preserved author comment left untouched on its own line.

### SPEC-05 — `### 10.6` skeleton
```markdown
### 10.6 Held-Out Physics-Gate Aggregate Statistic

> **Phase 53 contract: … (SPEC-05; GAP-44-01 owner ruling 2026-07-23, option A; grounded by .planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md).** …

- The held-out physics gate's headline statistic is the **worst-case max** over held-out trajectories of the per-trajectory validation-gate `eps_H` (as already defined, max over time, ctl_instruction.md conservation gate).
- The gate fails if ANY held-out trajectory's `eps_H` exceeds `1e-5`; `SCS = log10(max eps_H)`.
- Mean and median over trajectories are **non-gating** distribution facts.
- This gate is distinct from the per-stage curriculum ADVANCE gate (`ctl_instruction.md` Stage Transition Criteria).
```

## State of the Art

House-pattern evolution only (no external state-of-the-art applies to a transcription phase):

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Lock status implicit in prose ("default" wording) | Value-attached `**[LOCKED]**` / `**[DEFAULT]**` markers (this phase) | Phase 53 | First stated convention; GAP-45-03 consequence 5 discharged |
| Aggregate gate statistic lived only in gap registers | Codified in §10.6 (this phase) | Phase 53 | GAP-44-01's "remains available to a later spec-editing milestone" discharged |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The file-targeted render command (not `--all`) is the correct phase gate; `--all` was not re-run this session | Validation Architecture | Low — file-targeted is the tighter, phase-scoped gate; `--all` adds only the other two specs, which Phase 53 does not edit |
| A2 | No in-repo tooling other than the render oracle parses `pinn_architecture.md` headings/anchors, so a title-level preamble is structurally safe | Edit Site D | Low — only `tools/spec-render-check` was found to consume the file; its anchor reporting is diagnostic, not load-bearing |
| A3 | The corrected formula keeps the existing `L_{data}` glyph style and `Huber_{\delta_r}` operator spelling | Code Examples | Trivial — glyph choice is presentation, not substance; reversible |

## Open Questions

1. **Does §10.6 restate or cite the per-trajectory `ε_H` definition?**
   - What we know: within-trajectory reduction is DEFINED (`max_t`, CT `:567`); D-05 says "as already defined."
   - What's unclear: nothing substantive — only whether the subsection quotes the formula or cites the section.
   - Recommendation: cite by section name (the file already cross-references `ctl_instruction.md` by stable heading per the `:310` contract); planner decides exact wording. Not a gap.

2. **Do the warmup-form bullets (`:660`, `:664-665`) also receive markers?**
   - What we know: GAP-45-03 locks "the full PHYS-05 table" — the per-stage `λ^max(k)` values (`:661-663`); LOSS-02 (`:667`) already retains the whole warmup schedule.
   - What's unclear: whether D-01's "PHYS-05 values" extends to `I_warm` and the linear-warmup form.
   - Recommendation: mark exactly `:661-663` (the ruled values); the contract block states the surrounding schedule is retained per LOSS-02. Minimal-marking reading is the defensible one. Planner discretion, not a gap.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| node | spec-render-check | ✓ | v24.16.0 | — |
| npm | `npm ci` dep restore | ✓ | 11.13.0 | — |
| spec-render-check deps | render gate | ✓ (installed this session via `npm ci`; git-ignored) | lockfile-pinned | re-run `npm ci` |
| git | diff assertions, commit | ✓ | — | — |
| python / pinn env | — | not required | — | phase runs no code |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none.

## Validation Architecture

This phase's validation is **textual**, not runtime. `workflow.nyquist_validation: true` in `.planning/config.json`; satisfied by the assertion architecture below (no pytest/unittest target exists for prose, and none is introduced).

### Test Framework
| Property | Value |
|----------|-------|
| Framework | none — grep/diff/render-oracle assertions (shell) |
| Config file | none |
| Quick run command | `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| Full suite command | the same, plus the per-edit grep assertions and the SCOPE-38 diff assertion below |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SPEC-02 | `λ_phys^max` line states locked, cites GAP-45-03 | textual assertion | `sed -n '633,690p' pinn_architecture.md \| grep -F '**[LOCKED]**'` and `grep -F 'GAP-45-03'` present; `grep -F 'default $\lambda_{phys}^{max}(k) = 1$'` absent | ✅ (post-edit) |
| SPEC-03 | convention subsection defines both markers; PHYS-05 marked | textual assertion | `grep -c -F '**[LOCKED]**'` ≥ 3 (definition + 2 applications); `grep -F '**[DEFAULT]**'` defined; subsection states two-file governance | ✅ (post-edit) |
| SPEC-04 | reduction explicit; ruling + magnitudes cited | textual assertion | `grep -F 'mean over time, bodies, and spatial components'`; `grep -F 'GAP-45-01'` + `2026-07-31`; `grep -F '0.1539..0.1630'` and `grep -F '1.3852..1.4673'`; formula line carries `N_t \, N_b \, d` or `9 N_t` | ✅ (post-edit) |
| SPEC-05 | §10.6 states worst-case max, disambiguated | textual assertion | `grep -F '### 10.6'`; `grep -F 'worst-case'` and `grep -F 'max'`; `grep -F '1e-5'`; `grep -F 'GAP-44-01'` + `2026-07-23`; mean/median named non-gating; ADVANCE-gate disambiguation sentence present | ✅ (post-edit) |
| SC-5 / SCOPE-38 | markers byte-identical; no contract-marked value changed | negative diff assertion | `git diff -U0 -- pinn_architecture.md \| grep -E '^[+-]' \| grep -E 'eta_c\|first_omega_0\|underflow'` → **empty** | ✅ |
| Scope guard | only authorized files change | diff-scope assertion | `git status --short` shows changes only in `pinn_instruction/.../pinn_architecture.md` + `.planning/phases/53-*`; `git diff --stat -- pinn/ tests/ simulation_data/ ctl_instruction.md` → empty | ✅ |
| Author-comment preservation | 8 preserved comments intact | count assertion | `grep -c 'Author Comment' pinn_architecture.md` = `8` (baseline: `:103,:188,:249,:282,:286,:305,:542,:699`) | ✅ |
| Render fidelity | no new findings | oracle | baseline below; post-edit: 0 DEFINITE + no new REVIEW tokens | ✅ |

### Render-oracle baseline (captured this session, pre-edit)

Command: `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
Result: **exit 1** — `0 DEFINITE, 12 REVIEW, 7 ADJUDICATED, 14 SUPPRESSED`. The 12 REVIEWs are all D5 backtick-math near author flags: `§3.4` lines 537/544 (`delta_E = 1.0`, `ctl_instruction.md`, `IPR_train`) and `§4.2` lines 686-695 (`mu_p`, `torch.no_grad()`, `lambda_p`, `[1e-4, 100]`). The 7 adjudicated: lines 170, 188, 236, 238, 259, 260, 261 (`first_omega_0`, `\text{xxx}`, `elementwise_affine…`).

**Post-edit gate:** exit code ≤ 1 with 0 DEFINITE and the REVIEW token set ⊆ the baseline's 12 tokens (line numbers will shift; tokens must not grow). If the plan updates `22-02-pinn-architecture.json` line numbers for the 7 shifted adjudications (Pitfall 3), exit 0 is achievable — that update is a mechanical, in-scope companion edit to the same commit.

### Sampling Rate
- **Per task commit:** the grep assertions for the task's edit + the SCOPE-38 negative diff + `grep -c 'Author Comment'` = 8.
- **Per wave merge / phase gate:** full assertion set + render oracle + scope guard.
- **Phase gate:** all green before `/gsd-verify-work`.

### Wave 0 Gaps
- None — no test framework, fixtures, or config are needed; every assertion above runs against the post-edit file with committed tooling (render deps restorable via `npm ci`).

### No-runtime-change declaration
Phase 53 modifies no code. Verification: `git status --short -- pinn/ tests/ simulation_data/` empty at every commit; the phase's full diff is `pinn_architecture.md` + `.planning/phases/53-*` artifacts.

## Security Domain

`security_enforcement` is absent from `.planning/config.json` → treated as enabled; assessed honestly for a docs-only phase.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | — (no runtime surface) |
| V3 Session Management | no | — |
| V4 Access Control | no | — |
| V5 Input Validation | no | no user input is processed; edits are static prose |
| V6 Cryptography | no | — |

### Known Threat Patterns for this phase's actual surface
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Supply-chain via tooling deps | Tampering | `npm ci` from committed lockfile only; pinned exact versions; Phase 22 T-22-01 vetting; no new packages |
| Governance-record drift (spec says what was not ruled) | Repudiation | Every edit carries a D-06 contract block citing the ruling's date, option letter, and archived path; SC-5 negative diff on SCOPE-38 markers |

## Sources

All claims are in-repo and verified by direct `Read`/grep this session. The `research-plan` seam was not exercised: this phase has no library/docs/web questions — its entire domain is repository text. No package names are asserted (nothing installed), so no `[ASSUMED]`-tagged packages exist.

### Primary (HIGH confidence — direct file reads)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — Read at `:1-60, :149-273, :292-361, :405-469, :627-701, :960-1064`; structure/census greps (contract blocks, guard blocks, `eta_c`, `omega_0`, `underflow`, `lambda_phys`, `Author Comment`)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Read at `:550-594` (SCS gate), `:1900-1989` (ADVANCE gate); contract-block census greps
- `.planning/milestones/v2.1-GAPS.md` — full read (all five gap rows + obligations)
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` — full read
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md` — full read (GAP-44-01/44-02 records)
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` — Read at `:20-131` (GAP-45-01), `:235-344` (GAP-45-03)
- `.planning/REQUIREMENTS.md:60-129` (SPEC-01..06, SCOPE-33..38, owner checkpoints); `.planning/ROADMAP.md:56-78,155-167` (Phase 53 block + execution order); `.planning/STATE.md` (session continuity + house precedents)
- `.planning/phases/53-narrow-spec-codification/53-CONTEXT.md` — full read (D-01..D-06)
- `tools/spec-render-check/README.md` — full read; baseline detector run this session (exit 1, 0 DEFINITE / 12 REVIEW / 7 ADJUDICATED / 14 SUPPRESSED)
- `pinn/loss_catalog.py:240-269` — read-only CONF-07 conformance confirmation (NOT grounding; quoted below)

### Conformance confirmation (read-only; not grounding)
`pinn/loss_catalog.py:246-262` [VERIFIED: pinn/loss_catalog.py:246-262] — `data_huber_loss` docstring: *"GAP-45-01 / D-01 ratifies the scalar reduction as ``sum(Huber) / (9 * N_t)`` for the resident ``(N_t, 3, 3)`` tensor. The mean below is intentionally retained unchanged (D-03): it is exactly that reduction, with no compensating factor of nine."*; body `:262`: `return _huber(residual, HUBER_DELTA_DATA, dtype=dtype, device=device).mean()`. Code already conforms to the ruling; D-03 edits spec text only. (GAP-45-01's "Where in artifact" cites stale lines `:173-188`; current location is `:246-262` — another instance of line drift; plans must always re-derive line anchors.)

## Metadata

**Confidence breakdown:**
- Edit sites & ruling texts: HIGH — every quote captured by direct Read this session; line anchors corrected where CONTEXT drifted (§3.1 formula `:303`; author comment `:305`; GAP-45-03 index row `:15`)
- Architecture/patterns: HIGH — 28-instance house pattern census with exact grep reproduction
- Pitfalls: HIGH — render-window hazard and allowlist line-shift hazard both derived from the tool's committed README + a live baseline run
- ε_H measurement: HIGH for DEFINED (CT `:567` + 44-GAPS confirmation); residual ambiguity about *which file's prose* §10.6 cites is planner discretion, not a gap

**Research date:** 2026-08-19
**Valid until:** 2026-09-18 (stable — all sources are committed repo artifacts; invalidate early if `pinn_architecture.md` is edited by a concurrent phase, esp. Phase 56's §2.2/§3.2 work, which would shift every line anchor herein)
