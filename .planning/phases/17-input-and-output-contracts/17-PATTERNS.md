# Phase 17: Input and Output Contracts - Pattern Map

**Mapped:** 2026-05-19
**Files analyzed:** 9 implementation targets
**Analogs found:** 9 / 9
**Scope:** Documentation/spec adjudication only. Do not edit `pinn/`; live-code references are FUT-01 hand-off references only, not v1.4 grounding evidence.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-03.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md` | documentation evidence packet | file-I/O + EVID-05 adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` + `16-ISSUE-LEDGER.md` B-04 subsection | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md` | documentation evidence packet | file-I/O + adjudication | `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` | exact |
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | framework spec | transform | same file Step 4 + `ctl_pinn_resolution.md` IC sections | exact self-edit |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | framework spec | transform | same file §§5.2-5.3 + `ctl_pinn_resolution.md` time/output sections | exact self-edit |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` | documentation ledger | event-driven + batch index | same file status table and per-finding notes | exact self-edit |
| `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md` | hand-off register | batch + file-I/O | `17-CONTEXT.md` D-14 table + `17-GAPS.md` GAP-17-04 resolution | role-match |

Workflow artifacts such as `17-01-PLAN.md`, `17-02-PLAN.md`, `17-03-PLAN.md`, summaries, and verification reports are planner/executor outputs, not implementation targets for this map. `17-VALIDATION.md` already exists and is a shared validation reference.

## Pattern Assignments

### Evidence Packets: `B-03.md`, `M1.md`, `M2.md` (documentation evidence packet, file-I/O + adjudication)

**Analog:** `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`

**Packet header pattern** (`_TEMPLATE.md` lines 1-15):
```markdown
# Evidence Packet: <ID> - <Title>

## Header

| Field | Value |
|---|---|
| ID | `<ID>` |
| Title | `<Title>` |
| Severity | `BLOCKING` / `MAJOR` / `MINOR` / `INFO` |
| Current Status | `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` / `VERIFIED` / `DEFERRED` |
| Current Verdict | `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` / `-` |
| Phase | `Phase NN` |
| Acceptance Check ID | `AC-<REQ-ID>` |
| Spec Sections Touched | List exact framework spec section names or `None` |
| Code Paths Touched | List exact code paths or `Not code-applicable` |
```

Copy this scaffold for `B-03`, `M1`, and `M2`. Use `AC-IO-01` for `B-03` and `M2`; use `AC-IO-02` for `M1`.

**Source-position pattern** (`_TEMPLATE.md` lines 17-26):
```markdown
## Source Positions

Add side-by-side line-range citations from both primary Issue 01 sources before selecting a verdict.

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` | `path:Lx-Ly` | Summarize the resolution document claim. |
| `pinn_instruction/issues/01-architecture-and-physics-foundations.md` | `path:Lx-Ly` | Summarize the issue document claim. |

Do not add a primary-source field. Neither source is authoritative before adjudication.
```

**FUT-01 hand-off pattern** (`_TEMPLATE.md` lines 36-44):
```markdown
## FUT-01 Hand-off Note (formerly "Code Evidence")

> **Note (v1.4 update 2026-05-19):** Live code in `pinn/` is NOT a v1.4 evidence source per user directive 2026-05-19. This section is repurposed for forward-pointing FUT-01 hand-off documentation only. Do NOT cite live code as a basis for a v1.4 verdict.

If this finding's new framework-spec contract diverges from the v1.3-era code and FUT-01 will need to rewrite something, summarize the divergence class and point readers to `17-CODE-DIVERGENCE.md` for exact `pinn/` file:line references. Do not duplicate live-code line references inside evidence packets.
```

**Non-contested section handling** (`17-GAPS.md` lines 336-338):
```markdown
| Evidence-packet subsection ordering for non-EVID-05 findings (B-03, B-06, M1, M2) | Per Phase 16 D-06 template; section 5/7/8/9 marked "Not contested" | `evidence/B-03.md` etc. |
```

Apply that rule to `B-03.md`, `M1.md`, and `M2.md`: keep the template headings, mark EVID-05-only sections as `Not contested`, and avoid deleting headings that validation expects.

---

### `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md` (documentation evidence packet, file-I/O + EVID-05 adjudication)

**Analog:** `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`
**Supplemental analog:** `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` B-04 subsection

**EVID-05 required sections** (`_TEMPLATE.md` lines 46-80):
```markdown
## First-Principles Physics Check

<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->

Name the physical law, dimensional argument, numerical comparison, or architecture invariant used to adjudicate the claim. Show enough work that the verdict can be reviewed without trusting either primary source.

## Verdict

Select exactly one verdict:

- `accept-resolution`
- `accept-issue-doc`
- `accept-third-position`
- `reject-both-as-unsupported`
- `defer-with-blocker`
```

Continue using the same template sections `Root-Cause Framework Ambiguity`, `Locked Convention`, and `Which Source Was Correct / Wrong` from lines 64-80. Do not skip these for `B-04`.

**Candidate-set pattern** (`16-ISSUE-LEDGER.md` lines 97-115):
```markdown
### B-04: Input vector composition and orientation slots

Evidence packet: evidence/B-04.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-IO-02

Shared acceptance check: AC-IO-02 also covers other IDs B-04 and M1.

EVID-05 candidate set (corrected 2026-05-18; see 16-CONTEXT.md Amendment 2026-05-18):
- Option A: trig encoding for 3 angles (issue doc §5.3 / recommended-A path)
- Option B: shape invariants + direction cosines (issue doc "Recommended Option B")
- Option C: reconstructive Jacobi-state IC₁₃ (resolution doc §5.2–5.4; rejects A and B)
- Option D: codify status quo — live code's `I₁, I₂, I₃ + θ₁, θ₂` hybrid (pinn/data-processing-pipeline-full.py:1062–1146)
```

Use Option D only as a labeled v1.3 status-quo / FUT-01 hand-off reference. It is not v1.4 grounding evidence under the 2026-05-19 live-code directive.

**Resolution-doc IC target excerpt** (`ctl_pinn_resolution.md` lines 512-530):
```markdown
### 5.3 Final `IC13` formula

The final network-facing IC vector is

$$
\boxed{
IC_{13}=
[m_1^{in},m_2^{in},m_3^{in},
\rho_x^{in},\lambda_x^{in},\lambda_y^{in},
\dot\rho_x^{in},\dot\rho_y^{in},\dot\rho_z^{in},
\dot\lambda_x^{in},\dot\lambda_y^{in},\dot\lambda_z^{in},
E^{in}]
}.
$$

The full model input is

$$
\boxed{x=[\tau,IC_{13}]\in\mathbb R^{14}}.
$$
```

**Normalization excerpt** (`ctl_pinn_resolution.md` lines 533-572):
```markdown
Mass channels must preserve absolute mass scale. Do not use mass fractions as the final input representation under raw-mass dynamics.

For each ordered mass channel, compute dataset statistics after canonical ordering:

$$
\mu_{m,i}=\operatorname{mean}_{traj}(m_i),\qquad
\sigma_{m,i}=\operatorname{std}_{traj}(m_i),
$$

and encode

$$
\boxed{m_i^{in}=\tanh\left(\frac{m_i-\mu_{m,i}}{\sigma_{m,i}+10^{-8}}\right)}.
$$
```

Also copy the Jacobi-coordinate and energy normalization pattern from `ctl_pinn_resolution.md` lines 550-572. Keep μ and σ symbolic; `17-GAPS.md` GAP-17-07 resolved that concrete values are populated downstream after preprocessing finalization.

---

### `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md` (documentation evidence packet, file-I/O + adjudication)

**Analog:** `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md`
**Supplemental analog:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §5.2-5.3

**Existing output-contract wording to reuse** (`pinn_architecture.md` lines 747-761):
```markdown
The final layer of the SQR-SkipResNet-SIREN network is a standard linear
layer without any activation function. This is crucial as it allows the
network's outputs---the predicted positions---to take on any real value
required by the physical system. The output is a 9-dimensional vector
representing the concatenated positions of the three bodies at a given
time $\mathrm{t}$:
$$\mathrm{r}_\theta(\mathrm{t}) = [\mathrm{r}_1(\mathrm{t}), \mathrm{r}_2(\mathrm{t}), \mathrm{r}_3(\mathrm{t})]$$

Crucially, the network does not predict velocities or accelerations
directly. Instead, these kinematic quantities are derived from the
position outputs using AD with respect to the time input, $t$.
```

**COM projection target excerpt** (`ctl_pinn_resolution.md` lines 687-719):
```markdown
### 6.3 Output projection

Let the raw network head produce

$$
\tilde r_\theta'\in\mathbb R^{3\times3}.
$$

Before data loss, physics residual, IC loss, conservation loss, or metrics, project to the mass-weighted COM frame:

$$
R_\theta'=\frac1M\sum_{i=1}^3m_i\tilde r_{\theta,i}',
$$

$$
r_{\theta,i}'=\tilde r_{\theta,i}'-R_\theta'.
$$
```

Add the projection paragraph immediately after the existing `Output Frame` subsection in `pinn_architecture.md` lines 771-779, matching the mechanical placement approved in `17-GAPS.md` line 339.

**Acceptance-check pattern** (`17-CONTEXT.md` line 150):
```markdown
`AC-IO-03`: output is 9D positions; COM projection head defined with formula in `pinn_architecture.md`; AD-derived velocities and accelerations defined; `ctl_instruction.md:879–880` no longer claims direct velocity output.
```

---

### `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (framework spec, transform)

**Analog:** same file Step 4 and Data Flow sections
**Target source:** `ctl_pinn_resolution.md` IC formula/normalization sections

**Current section shape to preserve** (`ctl_instruction.md` lines 669-676):
```markdown
## Step 4: Formulating the Input Vector: Canonical Ordering, Normalization, and Assembly

#### Scope.

Using the invariants and quantities computed in Step 3 (e.g., $E$, $Q$,
$s_{\min}$, $L_{\text{norm}}$, $I_{\text{norm}}$, $I_1$, $I_2$, $I_3$,
masses), this step applies canonical ordering, normalizes all components
to $[-1,1]$, and assembles the final 12D input vector for the PINN.
```

Keep the Step 4 heading and flow, but replace stale 12D / invariant-input wording with the Jacobi-state IC13 contract.

**Current stale block to replace** (`ctl_instruction.md` lines 790-811):
```markdown
3.  **Assemble the Final 12-Component Input Vector.** The complete input
    vector fed to the PINN is formed by concatenating the normalized
    time component $t'$ with the 13-component initial condition vector
    $\text{IC}$ (using normalized values from above):

...

    The 11-component IC is: $$\text{IC} = \begin{pmatrix}
        m_1^{\text{norm}}, m_2^{\text{norm}}, m_3^{\text{norm}} & \text{(normalized masses)} \\
...
$$\text{Input} = [t', \text{IC}] \text{, (12-dimensional input vector)}$$
```

Replace rather than patch around this block; it combines the 12D-vs-14D and 11-vs-13 contradictions that `AC-IO-01` and `AC-IO-02` cover.

**Target IC pattern** (`ctl_pinn_resolution.md` lines 467-510):
```markdown
After preprocessing, define scaled Jacobi state variables:

$$
\rho'=r_2'(0)-r_1'(0),
$$

$$
\lambda'=r_3'(0)-\frac{m_1r_1'(0)+m_2r_2'(0)}{m_1+m_2},
$$

The velocities remain fully 3D:

$$
\dot\rho'=(\dot\rho_x,\dot\rho_y,\dot\rho_z),
$$

That gives 12 IC scalars. The 13th scalar is $E^{in}$, retained as redundant but useful optimization/curriculum information.
```

**Metadata-only pattern** (`ctl_pinn_resolution.md` lines 576-588):
````markdown
The following quantities remain mandatory, but they are not the final network IC vector:

```text
E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L
```

They are used for:

- curriculum stage assignment;
- lookahead/replay sampling;
- diagnostics and validation;
- loss scaling and reporting;
- possible auxiliary-head or widened-input ablations.
````

Use this for obsolete invariant/metadata mentions: preserve as metadata only when needed, never as final network IC slots.

**Training-flow line to replace in P02** (`ctl_instruction.md` lines 876-883):
```markdown
1.  **Input**: The model receives a 12-dimensional input vector, which
    is a combination of the scalar time $t$ and the 11-component initial
    condition (IC) vector.

2.  **Network Prediction**: The network outputs the predicted positions
    $\mathbf{r}_i(t)$ and velocities $\mathbf{v}_i(t)$ for all three
    bodies at time $t$.
```

Replace with 14D `[tau, IC13]`, position-only output, and AD-derived velocities/accelerations. Do not edit the `Source Issues` metadata section for SI retirement in Phase 17; `ctl_instruction.md` lines 1210-1218 are deferred to Phase 21 VER-06.

---

### `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (framework spec, transform)

**Analog:** same file §§5.2-5.3
**Target source:** `ctl_pinn_resolution.md` time spaces and output projection

**Input/time target excerpt** (`ctl_pinn_resolution.md` lines 209-249):
````markdown
The final implementation distinguishes three spaces:

$$
(t,r,v)_{raw}
\rightarrow
(u,r',v')_{physics}
\rightarrow
(\tau,IC_{13})_{network},
$$

with

$$
u=t/T,\qquad \tau=2u-1.
$$

```python
# u is the autograd leaf.
u = torch.as_tensor(u, dtype=torch.float64).requires_grad_(True)
tau = 2.0 * u - 1.0
x = torch.cat([tau, ic13], dim=-1)
r_proj = model_projected(x, raw_masses)
```
````

Also copy the chain-rule distinction from `ctl_pinn_resolution.md` lines 237-249. Name `u` as the autograd leaf and forward-reference Phase 19 (PHYS-02) for the componentwise derivative test.

**Current stale architecture table row** (`pinn_architecture.md` lines 812-817):
```markdown
**Input Vector** A **14-dimensional vector** `[t, IC]`, where `t` is time normalized to $[-1,1]` and `IC` is a 13-component vector of initial conditions. The IC vector contains:
• 3 masses.
• 5 physical invariants.
• 5 values for 3 trigonometrically encoded angles.

**Output** A **9-dimensional position vector** `[r1(t), r2(t), r3(t)]` with a linear (no activation) final layer. Velocities (...) and accelerations (...) are derived via **Automatic Differentiation (AD)**.
```

Rewrite the input row to `14D = [tau, IC13]` and back-reference the primary `ctl_instruction.md` IC composition. Preserve the existing 9D position-only output statement, then add the hard COM projection target from `ctl_pinn_resolution.md` lines 687-719.

**Output frame insertion point** (`pinn_architecture.md` lines 771-787):
```markdown
## 5.3 Output Frame and File Format

For consistency and physical correctness, the output of the model must
be clearly defined.

- **Reference Frame:** The predicted positions, $r_{\theta}(t)$, are in
  the **Center of Mass (COM) frame**.

- **Output Definition:** The output at each network forward pass is
  strictly the positions of the three bodies at a single normalized
  input time $t'$; velocities and accelerations are derived via AD.
```

Insert the COM projection paragraph immediately after the reference-frame bullets, so the spec explains how the COM-frame guarantee is enforced.

---

### `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (documentation ledger, event-driven + batch index)

**Analog:** same file status table and per-finding notes

**Status table rows to update** (`16-ISSUE-LEDGER.md` lines 21-30):
```markdown
| B-03 | Input dimensionality | 17 | PENDING | - | NO | evidence/B-03.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | B-04, M1, M2 | 2026-05-16 |
| B-04 | Input vector composition and orientation slots | 17 | PENDING | - | YES - EVID-05 required | evidence/B-04.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | B-03, M1, M2 | 2026-05-16 |
| B-06 | 3D-vs-planar encoding and output contract | 17 | PENDING | - | NO | evidence/B-06.md | AC-IO-03 | pinn_architecture.md | - | 2026-05-16 |
| M1 | 11D IC versus 13D IC gap | 17 | PENDING | - | NO | evidence/M1.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-16 |
| M2 | Total dimension claims conflict | 17 | PENDING | - | NO | evidence/M2.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-16 |
```

Update these rows in the same commit as the packet/spec edit that changes each status. Do not create a separate Phase 17 status table.

**Lifecycle pattern** (`16-ISSUE-LEDGER.md` lines 44-54):
```markdown
The forward status path is exactly `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.

`DEFERRED` is an absorbing state and requires a written blocker. `FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check for the finding's AC-ID.

A batch is one GSD plan (`NN-NN-PLAN.md`). After every batch of spec or code edits in Phases 17-21, the executing agent re-runs each `VERIFIED` finding's acceptance check if that finding appears as a transitive dependent of any finding edited by the batch.
```

**Transition log pattern** (`16-ISSUE-LEDGER.md` lines 62-73):
```markdown
Status transition log entries must include date, commit short SHA, status transition, and actor / plan reference.

### B-01: SIREN hidden-layer initialization

Evidence packet: evidence/B-01.md

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
```

Use ASCII arrows in ledger updates. If no commit SHA exists yet during planning, the plan should require executor to fill the actual short SHA when it commits or use the workflow's accepted placeholder convention only if execution is uncommitted.

---

### `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md` (hand-off register, batch + file-I/O)

**Analog:** `17-CONTEXT.md` D-14 table
**Schema authority:** `17-GAPS.md` GAP-17-04 resolution

**Resolved schema pattern** (`17-GAPS.md` lines 174-205):
```markdown
### GAP-17-04: `17-CODE-DIVERGENCE.md` schema

- **Decision point**: What fields does `17-CODE-DIVERGENCE.md` contain per divergence entry, and how does it relate to the eventual `pinn/STATUS.md`?
...
- **Agent was tempted to**: Use 5-column Markdown table — Surface / Live code (file:line) / Spec target (Phase 17 decision) / FUT-01 item / FUT-01 priority (HIGH/MEDIUM/LOW).
...
- **Resolution note**: User authorized auto-advance on 2026-05-19. Apply option (a): use the 5-column Markdown schema: Surface / Live code (file:line) / Spec target (Phase 17 decision) / FUT-01 item / FUT-01 priority.
```

**Divergence table seed** (`17-CONTEXT.md` lines 155-166):
```markdown
| Surface | Live code (`pinn/`) | Spec target (Phase 17) | FUT-01 item |
|---------|----------------------|------------------------|-------------|
| IC vector composition | `(m_frac, E_norm, L_norm, Q_norm, s_min_norm, I₁_norm, I₂_norm, I₃, θ₁_norm, θ₂_norm, I_norm)` | Jacobi state (D-01/D-06) | Full rewrite of `pinn/data-processing-pipeline-full.py` IC-formulation block |
| Mass encoding | mass fractions | ordered raw masses, `tanh` over dataset statistics (D-07) | Replace mass-fraction logic in same block |
| COM projection head | absent | hard layer applied before every loss/metric (D-02) | Add COM-subtraction step; thread mass metadata through forward signature |
```

Add the resolved fifth column `FUT-01 priority`. The context recommends HIGH for mass-encoding and IC composition, LOW for docstring drift.

**Forward-pointing code references for divergence only** (`pinn/data-processing-pipeline-full.py` lines 1114-1146):
```python
# Mass fractions
m_total = np.sum(masses) + 1e-8
m_norm = 2 * (masses / m_total) - 1  # Array for all 3 masses

# Assemble IC vector
ic_vector = np.concatenate([
    m_norm,                    # 3 components
    [E_norm],                  # 1 component
    [L_norm],                  # 1 component (already in [0,1], map to [-1,1])
    [Q_norm],                  # 1 component
    [smin_norm],               # 1 component
    [I1_norm, I2_norm, I3],    # 3 components
    theta_norm,                # 2 components
    [I_norm_bounded]           # 1 component
])
```

**Architecture divergence reference** (`pinn/basic_architecture.py` lines 185-192):
```python
# Final linear layer to get position outputs
outputs = self.final_layer(x)

# Apply output transform if specified
if self._output_transform is not None:
    outputs = self._output_transform(inputs, outputs)
            
return outputs
```

Label every `pinn/` reference as "FUT-01 hand-off reference only; not v1.4 grounding evidence."

## Shared Patterns

### Evidence Protocol
**Source:** `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` lines 15-24
**Apply to:** all evidence packet files
```markdown
Every finding packet must cite both primary Issue 01 sources side by side before recording a verdict:

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`

Neither source is authoritative.
```

The same README now states live code is not in the v1.4 examination basis; use the template's FUT-01 section for code-path hand-offs only.

### STOP Protocol
**Source:** `AGENTS.md` lines 15-40; user pattern-mapping instruction
**Apply to:** all Phase 17 planning and execution
```markdown
For every phase in v1.4 ... do NOT invent content where source materials are silent or ambiguous. STOP the affected work, surface the gap with full context, and wait for user instruction.
```

This pattern-mapping step must not write gap-register entries directly. If planner/executor finds a new MUST-surface gap, it should return it to the parent workflow.

### Validation
**Source:** `.planning/phases/17-input-and-output-contracts/17-VALIDATION.md` lines 22-43
**Apply to:** P01, P02, P03 verification sections
```markdown
| **Quick run command** | `rg -n "14D|14-dimensional|\\[tau, IC_13\\]|IC_\\{13\\}|9D|9-dimensional|COM projection|mass-weighted COM|AD-derived" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
...
| 17-03-01 | 03 | 2 | IO-04, VER-05 | T-17-02 / T-17-03 | Obsolete contract wording is removed or historical-labeled, and every spec-vs-code mismatch is recorded for FUT-01 without editing `pinn/`. | negative doc-structure | `bash -lc 'test -f .planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md ... && ! rg -n "12D input vector|12-dimensional input vector|11-component IC|5 values for 3 trigonometrically encoded angles|outputs.*velocities" ...'` | ❌ W0 | ⬜ pending |
```

Use the existing `17-VALIDATION.md` commands rather than inventing numerical probes in Phase 17.

### Obsolete-Wording Cleanup
**Source:** `17-CONTEXT.md` D-13 and `17-RESEARCH.md` validation map
**Apply to:** P03 cleanup and final verification
```bash
rg -n "12D input vector|12-dimensional input vector|11-component IC|outputs.*velocities|5 values for 3 trigonometrically encoded angles" \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

P03 should classify every remaining match as authoritative new contract, historical-labeled metadata, or removed. Do not edit Source Issues sections for SI retirement in Phase 17.

### Scope Boundary
**Source:** `17-CONTEXT.md` lines 34-40 and 155-166
**Apply to:** all Phase 17 work
```markdown
Phase 17 does NOT:
- Edit any file in `pinn/`.
- Lock frame, gauge, scaling order, or COM preprocessing.
- Execute numerical acceptance probes.
```

`pinn/` divergences are recorded for FUT-01 only.

## No Analog Found

No target is without a usable analog. `17-CODE-DIVERGENCE.md` has no exact predecessor file, but `17-CONTEXT.md` D-14 and `17-GAPS.md` GAP-17-04 provide the resolved table schema and seed rows.

## Metadata

**Analog search scope:** `.planning/`, `pinn_instruction/`, and `pinn/` targeted hand-off ranges
**Files scanned:** 147 candidates via `rg --files`
**Strong analogs read:** 18 files or targeted source ranges
**Pattern extraction date:** 2026-05-19
**Dirty worktree note:** Existing unrelated changes were present before writing this file. This mapping step creates only `.planning/phases/17-input-and-output-contracts/17-PATTERNS.md`.
