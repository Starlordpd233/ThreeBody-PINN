# Adopt GAP-19-01 / EDL-19-01 Resolution — Updated Execution Plan

> **Skill expectation:** Use `superpowers:executing-plans` task-by-task. This is a documentation/planning update only; do not edit runtime code unless a referenced plan already authorizes that edit.

## Summary

Adopt the user instruction resolving `GAP-19-01` for the energy-drift denominator floor `epsilon_H`, while preserving the repository's canonical/non-canonical governance boundary.

The canonical resolution is recorded in:

1. `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md`
2. `.planning/milestones/v1.4-GAPS.md`
3. `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`

The EDL files under `.planning/research/edl/` remain research-support artifacts. They may point to the canonical decision, but they must not become the decision record.

## Review Adjudication

Applied from the reviews:

- Do **not** add `RESOLVED-WITH-INSTRUCTION` frontmatter to `.planning/research/edl/EDL-19-01-resolution.md`.
- Separate canonical decision records from non-canonical research-support updates.
- Make the `19-CONTEXT.md` `D-20` text explicit.
- Replace negative verification guards that merely ban numeric defaults with positive guards asserting the selected contract.
- Make the evidence-packet §6.5 provenance-table template update explicit.
- Make the `19-03-PLAN.md` and `19-04-PLAN.md` updates concrete.
- Include an explicit no-change verification for `19-01-PLAN.md`.

Post-review revision sweep (R0-R10):

- Record the `1e-12`-drop provenance so a later auditor does not flag the canonical contract as spec drift against `EDL-19-01-resolution.md` (R0).
- Fix the evidence-packet verification path from phase-19 to phase-16 evidence directory (R1).
- Invert the symbolic-row provenance-table guard in `19-02-PLAN.md` and `19-04-PLAN.md` from asserting the OPEN row to asserting the resolved row (R2).
- Delete stale `epsilon_H = 10` negative guards and standardize contract notation to `1e-4 * S_H` (ASCII) / `1e-4 · S_H` (unicode tables) — never `10^-4` (R3).
- Add `v1.4-GAPS.md` frontmatter counter updates (`open_gaps: 0`, `resolved_gaps: 17`) (R4).
- Add Step 0 to Pre-Flight: commit pre-existing dirty files (B-07/B-08 routing corrections) before the `epsilon_H` work (R5).
- Warn about the `\epsilon_H` name collision with the SCS-gate quantity in `STATE.md` and `PROJECT.md`; add SCS-gate guard to verification (R6).
- Use existing EDL taxonomy status `RESOLVED-WITH-INSTRUCTION` instead of the invented `RESOLVED-BY-CANONICAL-RECORD` (R7).
- Complete `19-GAPS.md` edits: frontmatter `last_updated`, `governance` string, and body text resolution markers (R8).
- Reframe §5 (`19-03-PLAN.md`) as net-new content addition, not updating an existing vague instruction (R9).
- Tighten verification: per-file assertions instead of one OR-joined cross-file grep; add counter, date, and SCS-gate checks (R10).

Decision after re-review:

- Use `epsilon_H = 1e-4 * S_H` without `max(..., 1e-12)`.
- Treat non-finite or non-positive `S_H` as an invalid preprocessing/metadata state that must fail validation, not as a condition to silently mask with a hard-coded absolute floor.

Amendment provenance:

- `epsilon_H = 1e-4 * S_H` is a deliberate amendment to `EDL-19-01-resolution.md` (which states `max(1e-4 * S_H, 1e-12)`). The `1e-12` backstop is dropped per user instruction 2026-05-26: it is numerically inert at float32 (machine eps ~1.2e-7), and a near-zero/non-finite `S_H` must fail validation rather than be masked. The resolution doc remains non-canonical research support.

Date policy:

- Use the actual local execution date in changed files. This handoff uses `2026-05-26`. If the executor's repository policy requires a different already-recorded decision date, use that date consistently across all touched artifacts.

## Final Contract

Define:

```text
S_H = median_train(K0 + Uabs0)
```

computed once in `float64` after final COM/zero-momentum/gauge/scaling preprocessing over the training split.

Use the matched-Plummer components with `epsilon_train = 1e-5`:

```text
K0 = 0.5 * sum_i m_i ||v0_i'||^2

Uabs0 = sum_{i<k} m_i m_k /
        sqrt(||r0_i' - r0_k'||^2 + epsilon_train^2)
```

Bind:

```text
epsilon_H = 1e-4 * S_H
```

Validation requirement:

```text
S_H must be finite and strictly positive.
If S_H <= 0 or S_H is non-finite, fail preprocessing or metadata validation.
Do not substitute a fallback numeric floor.
```

Use `epsilon_H` only in the energy-drift denominator:

```text
|H0| + epsilon_H
```

Persist both metadata keys:

```text
S_H
epsilon_H
```

Do not tie `epsilon_H` to `epsilon_train`, `epsilon_inv`, or `epsilon_L`.

Phase 21 validates activation behavior only:

```text
Pr(|H0| < epsilon_H)
quantiles of |H0| / S_H
```

Phase 21 does not reselect `epsilon_H` unless a new user instruction opens a replacement gap.

## Rationale To Preserve In Canonical Text

Near-zero `H0` is physically meaningful for marginally bound trajectories; it is not merely a numerical artifact. However, strict relative drift normalization is ill-conditioned near zero. The dataset-scale floor preserves relative energy drift for typical bound systems while converting near-zero-`H0` samples to a controlled absolute Hamiltonian scale.

`Huber(delta=1)` caps per-sample loss contributions, but it does not remove denominator-driven gradient and sample-weighting effects. The denominator floor is therefore still part of the loss contract.

The removed `max(..., 1e-12)` term is intentionally not retained. For valid training data with non-zero masses and finite separations, `S_H = median_train(K0 + Uabs0)` is strictly positive. A zero or non-finite `S_H` indicates an invalid data or preprocessing state and should fail fast.

## Pre-Flight Guardrails

### Step 0 — Commit pre-existing unrelated changes

The working tree has unrelated dirty files from a prior session (B-07/B-08 annotation routing corrections, D-14/D-15 fixes). These must be committed BEFORE the `epsilon_H` work so each commit is logically clean.

1. Review the unrelated diffs:

```bash
git diff -- .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md \
            .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md \
            .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md \
            .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
```

2. Confirm the diffs touch ONLY B-07/B-08 annotation routing and D-14/D-15 corrections — nothing touching `D-07`, `D-20`, or `epsilon_H`.
3. Commit them as their own atomic commit:

```bash
git add .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
git commit -m "docs(19): correct B-07/B-08 annotation routing and D-14/D-15 corrections"
```

4. Do **not** stage untracked unrelated files (`EDL-19-01-resolution.md`, `18-UAT.md`, `reviewing_19_context.md`, or any `docs/findings/` files).
5. After this commit, the working tree should be clean except for files this plan will modify.

Then proceed with the Pre-Flight checks below.

Before editing, run:

```bash
git status --short --branch
git worktree list
```

Rules:

- Preserve unrelated dirty files.
- Do not edit `pinn/`.
- Documentation paths under `pinn_instruction/` may be edited only if already authorized by the Phase 19 plan task being executed.
- Keep historical review artifacts under `docs/findings/...` unchanged.
- Make two sequential atomic commits after verification (Step 0 routing corrections, then epsilon_H resolution).

## Canonical Decision-Record Updates

### 1. `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md`

Update `GAP-19-01` from open to resolved.

#### Frontmatter counter updates

```yaml
open_gaps: 0
resolved_gaps: 1
```

#### Frontmatter `last_updated`

Change `last_updated: 2026-05-24` to the resolution date (`2026-05-26`).

#### Frontmatter `governance` string

Replace the current governance string:

```yaml
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block (STOP protocol + math/engineering grounding requirement + no-live-code directive). GAP-19-01 is OPEN; dependent Phase 19 P02 work must not assign a numeric epsilon_H default until user instruction resolves it."
```

with:

```yaml
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block (STOP protocol + math/engineering grounding requirement + no-live-code directive). GAP-19-01 is RESOLVED-WITH-INSTRUCTION; epsilon_H = 1e-4 * S_H per user instruction 2026-05-26. See D-20 in 19-CONTEXT.md."
```

#### Gap status

Set the gap status line from `**OPEN**` to:

```text
**RESOLVED-WITH-INSTRUCTION**
```

#### Resolution note

Add a resolution note equivalent to:

```text
Resolution date: 2026-05-26
Resolution authority: User instruction for GAP-19-01 / EDL-19-01
Decision: Adopt Option C, scale-relative denominator floor.
Contract: epsilon_H = 1e-4 * S_H, where S_H = median_train(K0 + Uabs0), computed once in float64 after final preprocessing over the training split using the matched-Plummer Hamiltonian components with epsilon_train = 1e-5.
Validation: S_H must be finite and strictly positive; invalid S_H fails preprocessing/metadata validation. No fallback absolute floor is used.
Scope: epsilon_H is used only in the L_E denominator |H0| + epsilon_H. Persist S_H and epsilon_H in training metadata. Phase 21 reports activation behavior only and does not choose epsilon_H from scratch.
Amendment provenance: epsilon_H = 1e-4 * S_H is a deliberate amendment to EDL-19-01-resolution.md (which states max(1e-4*S_H, 1e-12)). The 1e-12 backstop is dropped per user instruction 2026-05-26: it is numerically inert at float32 (machine eps ~1.2e-7), and a near-zero/non-finite S_H must fail validation rather than be masked. The resolution doc remains non-canonical research support.
```

#### Body text updates (keep original text for provenance, append resolution markers)

In the "What the user needs to decide" block (options a-d), append to the block header:

```text
**RESOLVED** — User selected a variant of option (c): scale-relative rule. See resolution note above.
```

In the Notes section, replace or annotate the existing text:

- "Until resolved, plan text must not preserve or rely on a numeric `epsilon_H` default" → annotate: "**RESOLVED** — epsilon_H is now bound as `1e-4 * S_H`."
- "Phase 19 completion requires either user resolution or explicit deferral" → annotate: "**RESOLVED** — user instruction received 2026-05-26."

Keep the original decision-point text, source-silence citations, and agent-temptation text for provenance. Do not delete historical content.

### 2. `.planning/milestones/v1.4-GAPS.md`

Update the milestone index entry for `GAP-19-01`:

```text
Status: RESOLVED-WITH-INSTRUCTION
Resolution: epsilon_H = 1e-4 * S_H, with S_H = median_train(K0 + Uabs0), computed once in float64 after final preprocessing. See 19-GAPS.md for the canonical contract.
```

Remove active blocker language for this gap.

#### Frontmatter counter updates

The current frontmatter is `total_gaps: 17 / open_gaps: 1 / resolved_gaps: 16`. Update:

```yaml
open_gaps: 0
resolved_gaps: 17
```

Also update `last_updated` to the resolution date.

#### Row format

Match the file's established single-column resolution format:

```text
RESOLVED-WITH-INSTRUCTION: epsilon_H = 1e-4 * S_H; S_H = median_train(K0 + Uabs0). Canonical contract in 19-GAPS.md.
```

### 3. `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`

Add the following locked decision. Use the repository's existing decision formatting, but preserve this content.

```markdown
### D-20 — `epsilon_H` energy-drift denominator floor for `L_E`

**Status:** LOCKED
**Authority:** User instruction resolving `GAP-19-01` / `EDL-19-01`
**Date:** 2026-05-26

**Decision:** Use a dataset-scale Hamiltonian floor:

```text
epsilon_H = 1e-4 * S_H
```

where:

```text
S_H = median_train(K0 + Uabs0)
```

computed once in `float64` after final COM/zero-momentum/gauge/scaling preprocessing over the training split.

The components are:

```text
K0 = 0.5 * sum_i m_i ||v0_i'||^2

Uabs0 = sum_{i<k} m_i m_k /
        sqrt(||r0_i' - r0_k'||^2 + epsilon_train^2)
```

with `epsilon_train = 1e-5` and the same matched-Plummer Hamiltonian convention used by the training loss.

`S_H` must be finite and strictly positive. If `S_H <= 0` or is non-finite, preprocessing or metadata validation must fail rather than applying a fallback numeric floor.

Use `epsilon_H` only in the energy-drift denominator:

```text
|H0| + epsilon_H
```

Persist both `S_H` and `epsilon_H` in training metadata. Do not tie `epsilon_H` to `epsilon_train`, `epsilon_inv`, or `epsilon_L`.

Phase 21 validates activation behavior only by reporting:

```text
Pr(|H0| < epsilon_H)
quantiles of |H0| / S_H
```

Phase 21 must not reselect `epsilon_H` unless a new user instruction opens a replacement gap.

**Rationale:** Near-zero `H0` is physically meaningful for marginally bound trajectories, but strict relative normalization is ill-conditioned near zero. The dataset-scale floor preserves relative drift for typical bound systems while converting near-zero-`H0` samples to a controlled absolute Hamiltonian scale. `Huber(delta=1)` caps loss values but does not remove denominator-driven gradient/sample weighting.

**Amendment provenance:** `epsilon_H = 1e-4 * S_H` is a deliberate amendment to `EDL-19-01-resolution.md` (which states `max(1e-4·S_H, 1e-12)`). The `1e-12` backstop is dropped per user instruction 2026-05-26: it is numerically inert at float32 (machine eps ~1.2e-7), and a near-zero/non-finite `S_H` must fail validation rather than be masked. The resolution doc remains non-canonical research support.
```

Then update existing `D-07` or related `L_E` language:

- Replace `epsilon_H` symbolic wording with a reference to `D-20`.
- Keep the formula shape for `Delta H_n` and `L_E` unchanged except for the concrete denominator-floor contract.
- Update Phase 21 scope language to activation-rate reporting only.

## Execution-Plan Updates

### 4. `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md`

Update the task that edits the `pinn_architecture.md` loss section.

Required content:

- Replace symbolic `epsilon_H` instructions with `epsilon_H = 1e-4 * S_H`.
- Define `S_H = median_train(K0 + Uabs0)` exactly as in the final contract.
- Require `S_H` and `epsilon_H` to be persisted in training metadata.
- Require validation failure for `S_H <= 0` or non-finite `S_H`.
- State that `epsilon_H` is used only in `|H0| + epsilon_H`.
- State that Phase 21 only reports activation behavior.

#### Evidence packet §6.5 provenance-table template

In the §6.5 Numerical Defaults Provenance table template, replace the symbolic row:

```markdown
| `ε_H` | symbolic | `GAP-19-01` | OPEN — see `19-GAPS.md` |
```

with:

```markdown
| `ε_H` | `1e-4 · S_H`; `S_H = median_train(K0 + Uabs0)` | User instruction resolving `GAP-19-01`; canonical record in `19-GAPS.md` | RESOLVED-WITH-INSTRUCTION |
```

If `B-07.md`, `B-08.md`, or `B-09.md` already exist in the working tree, update their §6.5 rows directly as well. If they do not exist yet, updating the template in `19-02-PLAN.md` is sufficient.

#### Symbolic-row guard inversion (existing packets and verification)

In both `19-02-PLAN.md` and `19-04-PLAN.md`, there are positive guards asserting the OPEN symbolic row exists in evidence-packet §6.5 provenance tables:

```bash
rg -n "\| \`ε_H\` \| symbolic \| \`GAP-19-01\`" "$packet"
```

After resolution, this asserts a row that no longer exists. Replace with the resolved-row assertion:

```bash
rg -n "\| \`ε_H\` \| \`1e-4 · S_H\`" "$packet"
```

Apply this change in both `19-02-PLAN.md` (~line 316) and `19-04-PLAN.md` (~line 496).

#### Verification guards in `19-02-PLAN.md`

Replace guards that only reject invented numeric defaults, such as:

```bash
! rg -n "epsilon_H\s*=\s*10" "$ARCH"
```

with positive assertions that the selected contract appears:

```bash
rg -n "epsilon_H\s*=\s*1e-4\s*\*\s*S_H|ε_H\s*=\s*1e-4\s*·\s*S_H" "$ARCH"
rg -n "S_H.*median.*K0.*Uabs0|S_H.*median_train.*K0.*Uabs0" "$ARCH"
rg -n "S_H.*finite.*positive|S_H.*strictly positive|S_H.*validation" "$ARCH"
rg -n "training metadata.*S_H|S_H.*training metadata" "$ARCH"
rg -n "training metadata.*epsilon_H|epsilon_H.*training metadata" "$ARCH"
```

**Notation standard:** Use `1e-4 * S_H` (ASCII) in code blocks and grep patterns. Use `1e-4 · S_H` (unicode) only in markdown table cells. Never emit `10^-4`.

Also assert that the discarded fallback is not part of the live architecture contract:

```bash
! rg -n "epsilon_H\s*=\s*max|ε_H\s*=\s*max|max\(1e-4.*S_H.*1e-12" "$ARCH"
```

Do not globally ban every occurrence of `1e-12` in EDL research-support files, because historical candidate discussions may still mention it. Ban it only when it appears as part of the live `epsilon_H` contract.

### 5. `.planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md`

Add new review checks (net-new content). `19-03-PLAN.md` currently has 0 `epsilon_H` references; this is not updating an existing vague instruction but adding concrete verification checks that did not previously exist.

Add or update checks requiring the Phase 19 review to verify:

```text
- `pinn_architecture.md` contains the concrete `epsilon_H = 1e-4 * S_H` contract.
- `S_H = median_train(K0 + Uabs0)` is defined with matched-Plummer components and `epsilon_train = 1e-5`.
- `S_H` is computed once in float64 after final preprocessing over the training split.
- `S_H` and `epsilon_H` are persisted in training metadata.
- `S_H <= 0` or non-finite `S_H` is a validation failure.
- No live Phase 19 artifact leaves `epsilon_H` symbolic.
- No live architecture contract uses `epsilon_H = max(..., 1e-12)`.
```

Add FUT-01 divergence coverage for training metadata:

```text
FUT-01 must flag divergence if executable training metadata omits `S_H` or `epsilon_H`, computes `S_H` from a different split/preprocessing stage, uses a per-minibatch `S_H`, uses a fixed numeric `epsilon_H`, or uses a max/fallback floor not present in the canonical contract.
```

### 6. `.planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md`

Update final closure and handoff checks:

```text
- Phase 19 closure may treat `GAP-19-01` as resolved once `19-GAPS.md`, `v1.4-GAPS.md`, and `19-CONTEXT.md` carry the canonical decision.
- Phase 21 handoff must validate only denominator activation behavior: `Pr(|H0| < epsilon_H)` and quantiles of `|H0| / S_H`.
- Phase 21 must not reopen epsilon selection unless a new gap is created by user instruction.
- Any final grep/acceptance guard expecting symbolic `epsilon_H` must be removed or inverted.
```

Add a final check that the closure plan does not still describe `GAP-19-01` as open or blocking.

#### Symbolic-row guard inversion

See §4 above. The symbolic-row positive guard in `19-04-PLAN.md` (~line 496) must also be inverted from asserting `| ε_H | symbolic | GAP-19-01` to asserting `| ε_H | 1e-4 · S_H`. Apply the same change described in §4's "Symbolic-row guard inversion" subsection.

### 7. `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md`

No content update is expected if this file delegates `L_E` details to `pinn_architecture.md` and contains no `epsilon_H` contract.

Verify explicitly:

```bash
rg -n "epsilon_H|ε_H" .planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md || true
```

If the command returns no matches, make no edit. If it returns matches, inspect and update only if the text leaves `epsilon_H` symbolic or contradicts `D-20`.

## Status-Tracking Updates

### 8. `.planning/STATE.md`

Update active status text so `GAP-19-01` / `EDL-19-01` is no longer described as open or blocking.

Required wording:

```text
GAP-19-01 resolved by user instruction: epsilon_H = 1e-4 * S_H, with S_H = median_train(K0 + Uabs0). Phase 21 validates activation behavior only.
```

#### SCS-gate name collision warning

`STATE.md` uses `\epsilon_H` at line 117 for a **different** quantity — the post-v1.3 SCS raw-Hamiltonian-drift data-ingestion gate (`\epsilon_H > 10^{-5}` / `SCS > -5`). This is unrelated to the `L_E` denominator floor resolved by GAP-19-01.

**Edit ONLY:**
- Line 157 (the "Phase 19 cannot close" blocker sentence) — replace with resolved wording.
- Line 124 (the EDL support workflow note) — update to reflect resolution.

**Do NOT edit:**
- Line 117 (SCS-gate `\epsilon_H`).

Add this verification guard:

```bash
! git diff -- .planning/STATE.md | rg -q "^-.*epsilon_H > 10"
```

### 9. `.planning/PROJECT.md`

Update milestone or project-level status text consistently with `STATE.md`:

```text
EDL-19-01 no longer blocks Phase 19 loss-contract closure; the canonical resolution is recorded in 19-GAPS.md and D-20 of 19-CONTEXT.md.
```

#### SCS-gate name collision warning

`PROJECT.md` uses `\epsilon_H` at lines 42 and 155 for the SCS raw-Hamiltonian-drift data-ingestion gate — a different quantity from the `L_E` denominator floor.

**Edit ONLY:**
- Line 184 (the active-status footer) — update to reflect GAP-19-01 resolution.

**Do NOT edit:**
- Line 42 (SCS-gate milestone completion marker).
- Line 155 (SCS-gate Key Decision log row).
- Line 160 (EDL support workflow Key Decision — historical record, do not rewrite).

The same SCS-gate guard from §8 applies:

```bash
! git diff -- .planning/PROJECT.md | rg -q "^-.*epsilon_H > 10"
```

## Non-Canonical Research-Support Updates

### 10. `.planning/research/edl/EDL-19-01-resolution.md`

Do **not** add `RESOLVED-WITH-INSTRUCTION` frontmatter.

Do **not** treat this file as the canonical decision record.

Preferred action: leave this file unchanged. If a pointer is necessary, add only a short non-canonical note that says:

```markdown
> Non-canonical note: `GAP-19-01` was resolved by user instruction on 2026-05-26. The canonical record is `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md`; this file remains research input only.
```

### 11. `.planning/research/edl/EDL-19-01-epsilon-H.md`

Keep `canonical: false`.

Add a prominent note near the top:

```markdown
> Resolution pointer: `GAP-19-01` was resolved by user instruction on 2026-05-26. The canonical resolution is recorded in `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md` and locked as `D-20` in `19-CONTEXT.md`. This EDL brief remains a non-canonical research-support artifact.
```

If changing the frontmatter status, use the existing EDL taxonomy status `RESOLVED-WITH-INSTRUCTION` (defined in `.planning/research/edl/INDEX.md:17` and `README.md:338`). Do **not** use `RESOLVED-BY-CANONICAL-RECORD` — that status is not in the EDL taxonomy and inventing it would be a process-artifact-schema invention.

```yaml
status: RESOLVED-WITH-INSTRUCTION
canonical: false
```

This does not make the EDL brief canonical; `19-GAPS.md` remains the authoritative gap record.

### 12. `.planning/research/edl/INDEX.md`

Update the `EDL-19-01` row or entry to say:

```text
Resolved per canonical `19-GAPS.md`; support brief retained for research provenance. Contract: epsilon_H = 1e-4 * S_H, S_H = median_train(K0 + Uabs0).
```

Do not make the EDL index the canonical source of the decision.

### 13. `.planning/research/edl/README.md`

If the README has an active/open EDL list, update it to indicate that `EDL-19-01` is closed as a support item because the canonical gap is resolved.

Required wording:

```text
EDL-19-01 is no longer an open research dependency; see the canonical `GAP-19-01` resolution in `19-GAPS.md`.
```

## Verification Plan

Run from the repository root.

### Pre- and post-edit status

```bash
git status --short --branch
git worktree list
```

After editing, confirm no `pinn/` files changed:

```bash
! git diff --name-only -- pinn/ | rg .
```

### Canonical resolution present — per-file assertions

Each file must independently match. A missing edit in one file must not be masked by a match in another.

**19-GAPS.md:**

```bash
rg -n "RESOLVED-WITH-INSTRUCTION" .planning/phases/19-physics-and-loss-contracts/19-GAPS.md
rg -n "epsilon_H\s*=\s*1e-4\s*\*\s*S_H|ε_H\s*=\s*1e-4\s*·\s*S_H" .planning/phases/19-physics-and-loss-contracts/19-GAPS.md
rg -n "open_gaps: 0" .planning/phases/19-physics-and-loss-contracts/19-GAPS.md
rg -n "last_updated: 2026-05-26" .planning/phases/19-physics-and-loss-contracts/19-GAPS.md
```

**v1.4-GAPS.md:**

```bash
rg -n "RESOLVED-WITH-INSTRUCTION" .planning/milestones/v1.4-GAPS.md
rg -n "epsilon_H\s*=\s*1e-4\s*\*\s*S_H" .planning/milestones/v1.4-GAPS.md
rg -n "open_gaps: 0" .planning/milestones/v1.4-GAPS.md
rg -n "resolved_gaps: 17" .planning/milestones/v1.4-GAPS.md
```

**19-CONTEXT.md:**

```bash
rg -n "D-20" .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md
rg -n "epsilon_H\s*=\s*1e-4\s*\*\s*S_H" .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md
rg -n "LOCKED" .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md | tail -5
```

### Architecture/loss-plan contract present

Set `ARCH` to the `pinn_architecture.md` path used by `19-02-PLAN.md`, then run:

```bash
rg -n "epsilon_H\s*=\s*1e-4\s*\*\s*S_H|ε_H\s*=\s*1e-4\s*·\s*S_H" "$ARCH"
rg -n "S_H.*median.*K0.*Uabs0|S_H.*median_train.*K0.*Uabs0" "$ARCH"
rg -n "training metadata.*S_H|S_H.*training metadata" "$ARCH"
rg -n "training metadata.*epsilon_H|epsilon_H.*training metadata" "$ARCH"
rg -n "S_H.*finite.*positive|S_H.*strictly positive|S_H.*validation" "$ARCH"
```

### No live symbolic/open blocker remains

```bash
! rg -n "open_gaps: [1-9]|OPEN-RESEARCH-NEEDED|Phase 19 cannot close|epsilon_H.*symbolic|ε_H.*symbolic|unresolved in GAP-19-01" \
  .planning/STATE.md \
  .planning/PROJECT.md \
  .planning/phases/19-physics-and-loss-contracts \
  .planning/milestones/v1.4-GAPS.md
```

Allow `OPEN-RESEARCH-NEEDED` or symbolic-candidate wording to remain only in clearly non-canonical EDL research history if accompanied by a resolution pointer.

### Discarded fallback not used as live contract

```bash
! rg -n "epsilon_H\s*=\s*max|ε_H\s*=\s*max|max\(1e-4.*S_H.*1e-12" \
  .planning/phases/19-physics-and-loss-contracts \
  .planning/milestones/v1.4-GAPS.md \
  .planning/STATE.md \
  .planning/PROJECT.md
```

Do not globally search-fail on every `1e-12` occurrence in `.planning/research/edl/`, because historical candidate text may still mention it.

### Evidence packet template updated

```bash
rg -n "Numerical Defaults Provenance|1e-4 · S_H|median_train\(K0 \+ Uabs0\)|RESOLVED-WITH-INSTRUCTION" \
  .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md
```

If packet files exist (they are in the **phase-16** evidence directory):

```bash
for f in B-07.md B-08.md B-09.md; do
  pkt=".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/$f"
  if [ -f "$pkt" ]; then
    rg -n "1e-4 · S_H|median_train\(K0 \+ Uabs0\)|RESOLVED-WITH-INSTRUCTION" "$pkt"
  fi
done
```

### EDL canonical boundary preserved

```bash
! rg -n "RESOLVED-WITH-INSTRUCTION" .planning/research/edl/EDL-19-01-resolution.md
rg -n "canonical record|19-GAPS.md|D-20|non-canonical|support" \
  .planning/research/edl/EDL-19-01-epsilon-H.md \
  .planning/research/edl/INDEX.md
```

### SCS-gate epsilon_H untouched

```bash
! git diff -- .planning/STATE.md .planning/PROJECT.md | rg -q "^-.*epsilon_H > 10"
```

### EDL taxonomy compliance

```bash
! rg -n "RESOLVED-BY-CANONICAL-RECORD" .planning/research/edl/
rg -n "RESOLVED-WITH-INSTRUCTION" .planning/research/edl/INDEX.md
```

### Stale guards removed

```bash
! rg -n "epsilon_H\s*=\s*10\b" .planning/phases/19-physics-and-loss-contracts/19-0[24]-PLAN.md
```

### Formatting and diff hygiene

```bash
git diff --check
git diff --name-only
```

Review the diff manually for:

- no unrelated dirty-file changes (Step 0 committed them separately);
- no `pinn/` changes;
- no EDL research file claiming canonical authority;
- no live artifact still requiring `epsilon_H` to remain symbolic;
- consistent use of `epsilon_H = 1e-4 * S_H` (ASCII in code/grep) and `1e-4 · S_H` (unicode in tables only);
- no `10^-4` notation anywhere;
- SCS-gate `\epsilon_H` lines in STATE.md:117 and PROJECT.md:42,155 are unchanged;
- no invented EDL status (`RESOLVED-BY-CANONICAL-RECORD`).

## Commit

Use two sequential atomic commits.

### Commit 1: Pre-existing routing corrections (Step 0)

Already performed in Pre-Flight Step 0. If not yet done:

```bash
git add .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md \
        .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md

git commit -m "docs(19): correct B-07/B-08 annotation routing and D-14/D-15 corrections"
```

### Commit 2: epsilon_H resolution

```bash
git add .planning/phases/19-physics-and-loss-contracts/19-GAPS.md \
        .planning/milestones/v1.4-GAPS.md \
        .planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md \
        .planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md \
        .planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md \
        .planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md \
        .planning/STATE.md \
        .planning/PROJECT.md \
        .planning/research/edl/EDL-19-01-epsilon-H.md \
        .planning/research/edl/INDEX.md \
        .planning/research/edl/README.md

git commit -m "docs(19): resolve GAP-19-01 epsilon_H energy-drift floor (1e-4*S_H, user instruction)"
```

Do not add `.planning/research/edl/EDL-19-01-resolution.md` unless a non-canonical pointer note was intentionally added. Preferred action is to leave it unchanged.

### Commit hygiene check

Before committing, verify:

- Commit 1 diff touches ONLY B-07/B-08 routing and D-14/D-15 corrections — no `epsilon_H` or `D-20` changes.
- Commit 2 diff touches ONLY the epsilon_H resolution files listed above.
- No `pinn/` files in either commit.
- No untracked unrelated files staged (`EDL-19-01-resolution.md`, `18-UAT.md`, `reviewing_19_context.md`).

## Assumptions

- The user instruction resolves `GAP-19-01` and supersedes the prior open EDL research state.
- `S_H` is computed over the training split after the final canonical preprocessing pipeline, not per minibatch.
- Training data have non-zero masses and finite softened separations. If not, the dataset is invalid for this contract.
- EDL briefs are provenance/support artifacts, not canonical planning records.
- The exact Markdown heading syntax should follow the repository's existing style when applying the text above.
