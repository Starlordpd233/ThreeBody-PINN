# Phase 53: Narrow Spec Codification - Pattern Map

**Mapped:** 2026-08-19
**Files analyzed:** 1 modified file, 4 edit sites (plus conditional gap-register creation only if a STOP fires — RESEARCH resolved the one candidate: no gap expected)
**Analogs found:** 4 / 5 pattern classes (the convention preamble has no in-file analog — see "No Analog Found")

**Phase shape note:** this is a spec-text transcription phase. No code files are created or modified; `pinn/` is read-only conformance context (CONF-07 Complete). The standard role/data-flow vocabulary is adapted: each "unit of work" below is an **edit site** in the sole target file, classified by spec-text role and edit mechanics. All line anchors are current as of worktree HEAD `7f9902d2` on `milestone/v2.3` and were verified by direct Read on 2026-08-19 (RESEARCH.md same-session verification; this map re-verified every quoted range).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — **Edit Site A**: §3.1 `L_data` formula + prose + contract block (`:292`-`:360`) | spec-formula correction | static text transcription | The site's own existing `$$…$$` formula (`:303`) + adjacent LOSS-01 contract block (`:310`) | exact (in-place) |
| same file — **Edit Site B**: §4.1 PHYS-05 warmup bullets (`:658`-`:665`) + marker application + contract block | spec-value marking + contract block | static text transcription | LOSS-02 contract block (`:667`) + guard block (`:669`), immediately below the site | exact (in-place) |
| same file — **Edit Site C**: new `### 10.6` subsection inserted between `:1039` and `:1041` | spec-subsection insertion | static text transcription | `### 10.1`-`### 10.5` subsections (`:1016`-`:1039`) | exact for header/structure; partial for body form (existing five are probe-style; §10.6 is a gate-definition — see assignment) |
| same file — **Edit Site D**: new unnumbered convention preamble after title (`:6`), before `# 1.` (`:8`) | spec-preamble insertion | static text transcription | **None exists** — no conventions/how-to-read section in the file (verified by structure grep, RESEARCH Edit Site D) | none — see "No Analog Found" |
| `.planning/phases/53-narrow-spec-codification/53-GAPS.md` + `.planning/milestones/v2.3-GAPS.md` | gap register | static text | **Conditional only** — created solely if a STOP-protocol gap fires. RESEARCH measured the one candidate (ε_H within-trajectory reduction) as DEFINED; no gap is authored at map time. If needed, copy the register format from `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` | n/a (conditional) |

**Read-only files (do not edit):** `ctl_instruction.md` (D-02/D-04), `pinn/loss_catalog.py` (CONF-07 confirmation only), `sampling_method.md` (frozen), `data_quality_assessment.md` (read-only).

## Pattern Assignments

### Edit Site A — §3.1 `L_data` (SPEC-04 / D-03): formula correction + prose + contract block

**Analog:** the site itself — `pinn_architecture.md:292-360` (all excerpts below read verbatim 2026-08-19).

**Pattern A-1: Displayed-math syntax (`$$…$$` on its own line, blank lines fore and aft)** — current formula at `:300-:305`:

```markdown
The data fidelity loss uses a Huber contract on scaled projected
positions:

$$L_{data} = \frac{1}{N_t} \sum_n \sum_i \operatorname{Huber}_{\delta_r}(r_{\theta,i}'(u_n) - r_i'(u_n))$$

Author Comment: again, the syntax is broken
```

Copy: display math fenced by `$$…$$` on its own line; `\operatorname{Huber}_{\delta_r}` operator spelling; `L_{data}` glyph style (RESEARCH Assumption A3). The corrected formula keeps this syntax exactly — only the normalization and summation indices change (`1/(N_t \, N_b \, d)` with triple sum, per RESEARCH Code Examples). **Never** backtick-wrapped ASCII math here: the site sits wholly inside the `:305` author flag's D5/D6 ±20-line render-check window (`:285-:325`), RESEARCH Pitfall 2.

**Pattern A-2: Preserved author comment — edit around, never remove** — `:305` (standalone-line form):

```markdown
Author Comment: again, the syntax is broken
```

The comment stays on its own line, byte-identical. The corrected formula replaces `:303` above it; new prose goes after `:307-:308`. Preservation is gate-asserted: `grep -c 'Author Comment' pinn_architecture.md` must remain `8` (instances at `:103, :188, :249, :282, :286, :305, :542, :699`). A second, inline form exists at `:699` — `(Author Comment: this syntax is not ideal …)` inside a bullet — not near Site A but covered by the same count assertion. SCOPE-33 does not authorize comment removal (CONTEXT Deferred Ideas).

**Pattern A-3: Contract block, single-paragraph form (D-06 template source)** — LOSS-01 block at `:310`, immediately below the edit site:

```markdown
> **Phase 35 contract: loss scaling and units (LOSS-01; NS-18 modified; AC-LOSS-01; grounded by the resolution doc §1.14 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md`).** `pinn_architecture.md` is the canonical component-math home for data, physics, energy, and angular-momentum terms; `ctl_instruction.md` owns total-loss assembly and methodology cross-references by stable section heading plus AC ID. The component contract uses dimensionless `u=t/T` and `r'=r/D`, projected scaled positions for Huber data loss, ordered raw mass metadata where COM/force terms require masses, matched `epsilon_train = 1e-5` for force and Hamiltonian terms, separate data-fidelity snapshot points from physics/energy collocation points, the IC anchor, the angular-momentum regularizer, and no linear-momentum / no-linear-momentum-loss term.
```

Form to copy: line-start `>` blockquote; bold head `> **Phase NN contract: <topic> (<IDs>; grounded by <paths>).**`; dense provenance in the head; normative body in the same paragraph. Phase 53's D-06 substitution: the GAP ruling occupies the AC-ID slot (no new `AC-*` IDs minted). Site A's applied head (RESEARCH, D-06 form):

```
> **Phase 53 contract: L_data component reduction (SPEC-04; GAP-45-01 owner ruling 2026-07-31, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).**
```

Body must carry the magnitude pair `0.1539..0.1630` (mean) vs `1.3852..1.4673` (sum, exactly 9×) per CONTEXT Specifics, and the SCOPE-38 defensibility clause (reduction was genuinely undetermined by LOSS-01 — resolves an ambiguity, does not amend a contract-marked value; RESEARCH Edit Site A "SCOPE-38 defensibility evidence"). Use the **archived** milestone paths, not the pre-archive `.planning/phases/44-...` / `45-...` citations in the v2.1 index (RESEARCH Contract-Block Census note).

**Pattern A-4: Symbol-legend continuation (where the new reduction prose integrates)** — `:307-:323`:

```markdown
where $\delta_r = 1$ is the default Huber transition. The previous
MAE/L1 data-loss prose is replaced by this Huber contract.

…

where:

- $u_n = t_n/T$ is the normalized physics time coordinate

- $r'_{\theta,i}(u_n)$ is the network's predicted **scaled
  position** vector (the direct output of the network)
```

The new reduction sentence (mean over time, bodies, and spatial components; equivalently `1/(9 N_t)` at `N_b = 3, d = 3`) belongs in this prose neighborhood, in words/`$…$` inline math. **Do not reword `:307`** ("where `$\delta_r = 1$` is the default Huber transition") — it is D-01 un-swept inventory item #2; editing it while touching §3.1 is a listed anti-pattern.

---

### Edit Site B — §4.1 PHYS-05 warmup block (SPEC-02 / SPEC-03 / D-01 / D-02): marker application + contract block

**Analog:** `pinn_architecture.md:655-704` (read verbatim 2026-08-19), plus the SCOPE-38 exclusion zone `:645-:650` (verbatim capture in RESEARCH Edit Site B, verified same session).

**Pattern B-1: Current edit target — bulleted LaTeX values (the structural fact behind D-02)** — `:658-:665`:

```markdown
The warmup schedule is:

- $I_{warm} = min(2000, 0.1 \cdot N_{Adam,k})$
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  default $\lambda_{phys}^{max}(k) = 1$
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$
- $\lambda_E(k, i)$ and $\lambda_L(k, i)$ warm up linearly with
  $i/I_{warm}$
```

The PHYS-05 values are bulleted LaTeX, **not a markdown table** — a Status column is structurally impossible; the value-attached inline `**[LOCKED]**` marker is the only form that works (D-02). Mark exactly `:661-:663` (the ruled per-stage `λ^max(k)` values); the warmup-form bullets `:660` and `:664-:665` stay unmarked (RESEARCH Open Question 2 — minimal-marking reading; planner discretion). SPEC-02's reword = remove the word "default" from the `λ_phys^{max}(k) = 1` bullet and append the marker. Applied form (RESEARCH Code Examples):

```markdown
- $\lambda_{phys}(k, i) = \lambda_{phys}^{max}(k) \cdot min(1, i/I_{warm})$,
  $\lambda_{phys}^{max}(k) = 1$ **[LOCKED]**
- $\lambda_E^{max}(k) = \lambda_L^{max}(k) = \{0 \text{ for } k \in \{0,1\}; 10^{k-4} \text{ for } k \in \{2,3,4\}; 1 \text{ for } k \in \{5,6\}\}$ **[LOCKED]**
```

**Pattern B-2: Contract block placed immediately after the text it binds** — LOSS-02 at `:667` (the insertion model: Phase 53's block lands after `:665`, before `:667`):

```markdown
> **Phase 35 contract: energy-loss weights (LOSS-02; M15 rejected as issue-doc replacement; AC-LOSS-02; grounded by the resolution doc §1.9 and `.planning/phases/35-loss-energy-weight-contracts/evidence/m15-energy-weight-schedule.md`).** Retain the PHYS-05 warmup schedule above with `lambda_E^max <= 1` and scheduled conservation weights at or below one. The issue-doc cap-table replacement and stale high-energy-weight premise are rejected, not adopted as a locked schedule. Before any future control law, log weighted losses, scheduled weights, and gradient statistics; automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists.
```

Site B's applied head (RESEARCH, D-06 form — one block covers both SPEC-02 and SPEC-03 since SC-2 couples them):

```
> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03; GAP-45-03 owner ruling 2026-07-24, option A; grounded by .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md).**
```

**Pattern B-3: Guard block (secondary house form — do not imitate for Phase 53)** — `:669`:

```markdown
> **Phase 35 guard: source precedence and deferred values (LOSS-02 / LOSS-03 / LOSS-04; AC-LOSS-02 / AC-LOSS-03 / AC-LOSS-04).** The Phase 35 evidence packets supersede issue-doc replacement proposals for this component catalog: …
```

There are exactly 2 guard blocks across both specs (census: 9 anchored contract + 1 guard in `pinn_architecture.md`; 17 anchored + 2 indented contract + 1 guard in `ctl_instruction.md`). Phase 53 mints **contract** blocks only (D-06); the guard form is documented here so the planner does not confuse the two.

**Pattern B-4: SCOPE-38 exclusion zone — the do-not-touch lines** — `:645-:650` (verbatim per RESEARCH Edit Site B), 8–13 lines above the edit target, inside the same subsection:

```markdown
- $L_{phys}^{causal}$: Physics residual with causal weighting
  $w_n = exp(-\eta_c \sum_{m<n} stopgrad(\bar R_m))$, $w_1 = 1$,
  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
  causal exponent to avoid underflow, but do not choose a numeric
  clipping bound in Phase 19; surface a gap if one is needed.
  The causal exponent clip is required only to avoid underflow.
```

Plan must carry an explicit excluded-lines list (`:639-:656` where-block, especially `:645-:650`) and the SC-5 negative diff assertion: `git diff -U0 -- pinn_architecture.md | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow'` → **empty** (RESEARCH Pitfall 1, Validation Architecture). Note `:647`'s `$\eta_c = 1$ default` keeps the word "default" **unmarked** under D-01 (SCOPE-38-marked, Phase-56-coupled; RESEARCH SCOPE-38 Adjacency "§4.1-internal hazard"). Also unmarked per D-01: `:641-:644` `$\delta_r = 1$` / `$\lambda_{IC} = 1$` defaults — inventory items #3.

---

### Edit Site C — new `### 10.6` Held-Out Physics-Gate subsection (SPEC-05 / D-04 / D-05)

**Analog:** `pinn_architecture.md:1014-1041` (read verbatim 2026-08-19).

**Pattern C-1: §10 subsection style (H3, numbered, titled)** — shortest full exemplar, `### 10.1` at `:1016-:1019`:

```markdown
### 10.1 Scaling Consistency
- **Pass Criterion**: Output variables computed via the length scaling $D = (G T^2)^{1/3}$ must match physical dimensions with `relative_error < 1e-10`.
- **Input Data**: Preprocessed network inputs.
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_scaling.py`
```

All five existing subsections (`### 10.1` Scaling Consistency `:1016`; `### 10.2` COM Invariance `:1021`; `### 10.3` Componentwise AD `:1026`; `### 10.4` Force-Energy Consistency `:1031`; `### 10.5` Loss Stability Dry Run `:1036`) are H3-level under the `# 10.` H1 (`:1014`), each carrying `- **Pass Criterion**` / `- **Input Data**` / `- **Execution**` bullets. **Style correction to CONTEXT D-04:** the new subsection is `### 10.6 <Title>` (H3), not `## 10.6` — match house style (RESEARCH Edit Site C).

**Form latitude (documented):** §10.6 is a gate-*definition* contract, not a probe — matching the three-bullet form exactly is optional (RESEARCH Edit Site C). A contract block per D-06 is **mandatory**. If a multi-paragraph block is needed, the `:353-:355` exemplar shows the continuation form (`>` on each line, italic `*Note (…)*` second paragraph):

```markdown
> **Phase 34 contract: batch-construction reconciliation (SI-PINN-003; ctl canonical; AC-LOOP-02; grounded by the resolution doc §1.5 claim matrix B07-04 and `ctl_instruction.md` Mini-Batch Construction).**
>
> *Note (PIPE-04): `points_per_trajectory=32` and `N_data = batch_size * points_per_trajectory` are code defaults/illustrations only, not the spec contract. …*
```

**Pattern C-2: Insertion point and file-end boundary** — `:1039-:1045`:

```markdown
- **Execution**: `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_loss_stability.py`

---

## Source Issues / Notes for Future Reconciliation

These notes are metadata for future reconciliation. They are not part of the faithful converted body and are excluded from fidelity comparison per D-19.
```

Insert §10.6 between `:1039` (end of §10.5) and the `---` separator at `:1041` — inside the faithful converted body, before the D-19 metadata section. File ends at `:1064`.

Site C's applied contract head (RESEARCH, D-06 form):

```
> **Phase 53 contract: held-out physics-gate aggregate statistic (SPEC-05; GAP-44-01 owner ruling 2026-07-23, option A; grounded by .planning/milestones/v2.1-phases/44-physics-gate-forensics/44-GAPS.md).**
```

Mandatory content per D-05: max over held-out trajectories of per-trajectory `ε_H` **as already defined** (cite `ctl_instruction.md`'s locked conservation-gate definition — `eps_H = max_t |(H(t) - H(0)) / H(0)|` at `ctl_instruction.md:567` — do **not** restate the within-trajectory reduction; cross-reference by stable section heading per the `:310` precedent); fail-if-any-exceeds-`1e-5`; `SCS = log10(max ε_H)`; mean/median explicitly non-gating distribution facts. Mandatory disambiguation sentence per D-04: §10.6 is distinct from the per-stage curriculum ADVANCE gate (`ctl_instruction.md:1939` region). Contract block should also carry the one-clause placement reasoning (GAP-44-01's "codifying into `ctl_instruction.md` … remains available" was availability language; D-04 is the locked placement) so a later reader does not re-litigate (RESEARCH Ruling Texts, GAP-44-01 placement note; Pitfall 4). Skeleton in RESEARCH Code Examples.

---

### Edit Site D — convention preamble after title (SPEC-03 / D-02)

**Analog:** none — see "No Analog Found" below. The placement context (read verbatim 2026-08-19) is:

**Pattern D-1: Document head structure (insertion slot)** — `:1-:8`:

```markdown
---
author: Starlordpd233
date: 2026-03-21
---

# A Definitive Implementation Blueprint for a Hybrid SQR-SkipResNet-SIREN PINN with Soft Conservation Regularization for $\mathrm{N}$-Body Dynamics

# 1. Foundational Architectural Principles: A Co-Designed Approach for Chaotic Systems
```

The preamble inserts between the title (`:6`) and `# 1.` (`:8`) — RESEARCH Edit Site D candidate (a), recommended. Constraints on the inserted text (all mechanical, from RESEARCH Pitfalls 2/3/5):

- **~15 lines max**, and all added lines must land above post-edit line 83 (first author flag at `:103`; D5/D6 window opens at `:83`).
- **No backtick-wrapped ASCII math** anywhere in the preamble; ASCII-only; no emoji (D-02 — `**[LOCKED]**` / `**[DEFAULT]**`, never `🔒`; the repo polices render fidelity via `tools/spec-render-check/`).
- **Defines markers as attaching to a *value*, not a table row** (D-02); states governance over both framework specs while making zero marker edits in `ctl_instruction.md`; states markers are status annotations, **not preserved author comments** (Pitfall 5 — SI-PINN-002 at `:1050` records author comments were once rendered as bold bracketed text `**[...]**`, visually identical to the D-02 marker; the convention text must draw this distinction explicitly).
- **Line-shift side effect the plan must own:** inserting after `:6` shifts every later line down, breaking the 7 line-keyed adjudicated render-check entries at `:170-:261` (`22-02-pinn-architecture.json`). RESEARCH Pitfall 3 preferred option: update the allowlist's seven line numbers in the same commit (mechanical, in-scope companion edit) so the oracle gate stays green. Decide in plan; do not discover at verify time.

## Shared Patterns

### S1: House contract block (applies to all four edits)
**Source:** `pinn_architecture.md:310` (LOSS-01) and `:667` (LOSS-02), quoted in full above; multi-paragraph variant at `:353-:355`.
**Census (RESEARCH, grep-verified 2026-08-19):** 9 anchored contract blocks in `pinn_architecture.md` (`:310, :353, :424, :537, :625, :667, :686, :726, :890`) + 1 guard (`:669`); 17 anchored + 2 indented contract + 1 guard in `ctl_instruction.md`. 26 line-start contract blocks total — unambiguous house pattern.
**D-06 form:** `> **Phase 53 contract: <topic> (<SPEC-NN>; <GAP-ID> owner ruling <date>, option <X>; grounded by <full relative archived path>).**` — GAP citation in the AC-ID slot; mint no new `AC-*` IDs; carry date, option letter, and archived grounding path in every block.

### S2: Render-oracle discipline (applies to all four edits)
**Source:** `tools/spec-render-check/` (Phase 22 D-08/G1/G2 house gate; baseline captured in RESEARCH Validation Architecture: exit 1, 0 DEFINITE / 12 REVIEW / 7 ADJUDICATED / 14 SUPPRESSED).
**Rules:** `$$…$$` display math on its own lines (mid-line `$$` is a D4 DEFINITE); inline math `$…$`; ASCII-only additions; no new backtick-ASCII-math inside D5/D6 author-flag windows (±20 lines around each of the 8 comment lines). Post-edit gate: 0 DEFINITE and REVIEW token set ⊆ the 12-token baseline (line numbers may shift; tokens must not grow).

### S3: Author-comment preservation (applies to Sites A and B by proximity; asserted phase-wide)
**Source:** SI-PINN-002, `pinn_architecture.md:1047-:1054`; instances at `:103, :188, :249, :282, :286, :305, :542, :699`.
**Rule:** edit around all `Author Comment:` lines; never remove or reword. Gate: `grep -c 'Author Comment' pinn_architecture.md` = `8` at every commit.

### S4: SCOPE-38 byte-identity (applies to all four edits; the SC-5 defense)
**Source:** RESEARCH SCOPE-38 Adjacency Check — markers: `η_c` (`:414, :424, :646-:647`), `first_omega_0` (`:167, :170, :260, :983`), clip underflow-only purpose (`:648, :650`).
**Rule:** no edit touches a marker line. Negative diff assertion at every commit: `git diff -U0 -- pinn_architecture.md | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow'` → empty. Scope guard: `git status --short` shows changes only in `pinn_architecture.md` + `.planning/phases/53-*`; `git diff --stat -- pinn/ tests/ simulation_data/ ctl_instruction.md` → empty.

### S5: D-01 un-swept inventory (the routed deliverable accompanying Site B)
**Source:** RESEARCH D-01 Un-Swept Inventory (7 items, all line-verified): §2.4 Table 1 "Recommended Value" header + `first_omega_0 | 30` row (`:253, :260` → Phase 56); `δ_r = 1` default prose (`:307`); §4.1 where-block defaults (`:641-:644`); `η_c = 1` default (`:647`); §3.2 `n_col` recommended ranges (`:433, :440`); Table 2 under `## 5.3` (`:976-:992` — cite as "Table 2", not "§9"; sections 6–9 do not exist as headers, RESEARCH numbering-anomaly note); §3.1 Loss Integration Note (`:357-:360`). The inventory records these as intentionally unmarked with per-item reasoning; it does not mark them.

## No Analog Found

| File / Site | Role | Data Flow | Reason |
|---|---|---|---|
| Edit Site D — convention preamble | spec-preamble | static text | No conventions/how-to-read/notation section exists anywhere in `pinn_architecture.md` (structure grep, RESEARCH Edit Site D: file goes frontmatter `:1-4` → title `:6` → `# 1.` `:8`; the file's only "convention" hit is inline prose at `:390`, "The raw-mass nondimensionalization convention absorbs `G`" — a sentence, not a declaration block). Planner should compose the ~15-line subsection from D-02's locked content + Pattern D-1's mechanical constraints; no style exemplar to copy. This was an explicit, verified finding of RESEARCH, not a search gap. |
| §10.6 body form (partial) | spec-subsection body | static text | All five existing §10.x subsections are probe-style (Pass Criterion / Input Data / Execution). §10.6 is a gate-*definition* contract — no probe exists for it (SCOPE-35's single-look budget is unspent; Phase 53 defines the statistic, runs no evaluation). RESEARCH Edit Site C explicitly grants form latitude; the H3 header style and mandatory contract block still come from Pattern C-1 / S1. |

## Metadata

**Analog search scope:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (targeted Reads at `:1-:60`, `:292-:361`, `:655-:704`, `:1010-:1064`; convention/notation grep across the full file); `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (read-only, via RESEARCH's verified captures); ruling texts and census via `53-RESEARCH.md` (all marked VERIFIED by direct Read same session).
**Files scanned:** 2 spec files + 5 planning artifacts (via RESEARCH); 4 targeted ranges read directly for this map.
**Early stopping:** analog search stopped at the 5 pattern classes named in the phase shape — all in-file exemplars identified; no broader sweep needed for a single-file transcription phase.
**Line-anchor corrections carried from RESEARCH (use these, not CONTEXT's):** §3.1 formula `:303` (CONTEXT said `:304`); author comment `:305` (said `:306`); LOSS-01 block starts `:310` (said `:307`); GAP-45-03 milestone-index row `:15` (said `:12`); "§9 Definitive Specification table" is **Table 2 under `## 5.3`** at `:976-:992`.
**Pattern extraction date:** 2026-08-19
