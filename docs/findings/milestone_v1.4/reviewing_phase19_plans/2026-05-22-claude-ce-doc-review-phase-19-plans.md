# Phase 19 Plans — Multi-Persona Document Review

**Reviewer:** Claude Opus 4.7 via `compound-engineering:ce-doc-review` skill
**Date:** 2026-05-22
**Branch:** `milestone/v1.4`
**Targets reviewed:**
- `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-03-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-04-PLAN.md`
- `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md` (grounding source)
- `.planning/phases/19-physics-and-loss-contracts/19-DISCUSSION-LOG.md` (audit trail)

**Reviewing personas dispatched (4):**
1. `ce-coherence-reviewer` (always-on) — internal consistency, terminology drift, ambiguity
2. `ce-feasibility-reviewer` (always-on) — execution reality, regex robustness, wave coordination
3. `ce-scope-guardian-reviewer` — multi-requirement / multi-priority document with future-work deferrals
4. `ce-adversarial-document-reviewer` — high-stakes physics/math domain, contested EVID-05 findings, new abstractions

**Findings synthesized:** 24 distinct findings after dedup and cross-persona promotion.

---

## Headline

The plans **correctly transcribe a mathematically sound resolution doc** on the major calls (raw-mass dimensional analysis, matched Plummer pair, pseudo-ALM rejection, AD leaf semantics). The 19 LOCKED decisions in `19-CONTEXT.md` are coherent and well-grounded. **The problems concentrate in three areas:**

1. **Verify-command rigor** — Multiple regex patterns are tautological or cannot detect what they're supposed to. `! rg "lambda_p.*L_phys.*mu_p.*L_phys"` never matches the actual LaTeX text; `! rg "epsilon_soft|eps_soft"` is ASCII-only while the live file uses `\epsilon_{\text{soft}}`.
2. **Process-artifact mechanics** — Markdown table-row annotation (D-14) is structurally underspecified; cross-reference section numbers between specs are unstable across waves; Wave-1 parallel ledger writes collide; commit-before-verify ordering creates partial-success states.
3. **Audit-record fidelity** — `ε_H = 10⁻⁸` is silently invented (CRITICAL GOVERNANCE STOP protocol violation); B-09 §5's "additive softening force" derivation is mathematically wrong; M4 §5/§9 overstates the issue doc's arithmetic correctness on a convention-dependent count.

**Most important missed gap** (per user's explicit ask about gaps the plans should have documented):
**`ε_H = 10⁻⁸` should have been surfaced as a `19-GAPS.md` entry per the STOP protocol.** The resolution doc defines the symbol but not the value; the plans pick `10⁻⁸` by analogy with `ε_L`. This is the textbook case the project's CRITICAL GOVERNANCE rule exists to prevent.

**Most important physics correctness concern:**
**B-09 §5's additive-softening force derivation is wrong.** The plan rejects a strawman formulation (`F ∝ r/(r+ε)³`) that doesn't exist in any standard softening literature. The actual additive force law is `r̂/(r+ε)²`. The locked verdict (Plummer is correct) is unaffected, but the evidence packet contains false physics that will mislead future readers.

---

## Coverage

| Persona | Status | Findings |
|---|---|---|
| ce-coherence-reviewer | ✅ completed | 14 findings (C1–C14) |
| ce-feasibility-reviewer | ✅ completed | 17 findings (F1–F17) |
| ce-scope-guardian-reviewer | ✅ completed | 13 findings (S1–S13) |
| ce-adversarial-document-reviewer | ✅ completed | 12 findings (A1–A12) |

**Document classification:** `plan` (frontmatter `type: execute`, task-structured, file paths, implementation units)
**Origin:** `19-CONTEXT.md` (validated upstream — 19 LOCKED decisions, 0 OPEN gaps)

---

# Findings by Severity

## 🔴 MUST_FIX — Critical Issues (8)

### M1. Cross-reference §-number instability across waves
**Cross-persona agreement:** F5, F10, F11, S1, S9, S11 (Feasibility + Scope-Guardian)
**Classification:** operational + mechanical
**Confidence:** high

**Evidence.** Plan 19-01 Task 2 (lines 282–286) commits the following into `ctl_instruction.md`:
> `where each term is defined in pinn_architecture.md §3 (see §3.1 L_data, §3.2 L_phys, §3.3 L_E, §3.4 L_L, §3.5 L_IC). ... see pinn_architecture.md §5.x (PHYS-02).`

Plan 19-02 Task 2 (lines 323, 335) creates the new subsections with literal `### 3.x` placeholders that the executor must resolve at run time. The current `pinn_architecture.md` has §3.1 (L_data), §3.2 (Physics Residual), §3.3 (HNN Energy Regularizer). After 19-02 inserts L_IC and L_L, the actual section numbers depend on executor ordering choices that the plan does not constrain.

Plan 19-03 Task 2 (line 195) is explicitly forbidden to edit `ctl_instruction.md`:
> "Read ctl_instruction.md to verify; if any cross-reference is wrong or missing, note it but do NOT edit ctl_instruction.md (it was committed in 19-01). Instead, log any cross-reference gap found and continue."

Plan 19-04 Task 2 verifies cross-references via `rg -n "pinn_architecture.md.*PHYS-02" ctl_instruction.md` — a permissive substring match that passes whether or not the section number is correct.

**Why it matters.** Phase 19 can exit with known-broken cross-references and `VERIFIED` ledger statuses, simply because the structural check is too loose to detect the mismatch. This also violates the `CLAUDE.md` STOP protocol's "log and continue" prohibition.

**Suggested fix.** Choose one:
- (a) **Section-agnostic prose in 19-01:** Replace `§3.1 L_data, §3.2 L_phys, §3.3 L_E, §3.4 L_L, §3.5 L_IC` with `the §3 subsections (L_data, L_IC, L_phys^causal, L_E, L_L)`. Replace `§5.x` with `the AD contract subsection in §5`.
- (b) **Move retargeting to P03:** Have P03 (which runs after P02 finalizes numbers) write the `ctl_instruction.md:962` cross-reference. P01 then leaves a `TODO(P03)` marker.
- (c) **HTML anchors:** P02 writes `<a id="phys-02-ad-contract"></a>` etc. and P01 references the anchors.

Option (a) is the cleanest and lowest-risk.

---

### M2. D-14 "append one line to table row" breaks Markdown tables
**Persona:** Feasibility (F1)
**Classification:** process-artifact schema
**Confidence:** high

**Evidence.** The Issue Doc rows at `pinn_instruction/issues/01-architecture-and-physics-foundations.md:72, 76, 86` are single-line GFM table rows. Example B-02:
```
| B-02 | **BLOCKING** | Characteristic length D has the same wrong formula... | ... | ... |
```

Plan 19-01 Task 3 (line 354) instructs:
> "append exactly ONE line to the B-02 table row (line 72 area, at the end of the row or in the adjacent cell)"

And the annotation is given as a separate code-fenced line:
```
**Adjudicated Phase 19:** `accept-resolution`. See `evidence/B-02.md`.
```

Inserting a newline inside a Markdown table row breaks the table — GFM/Pandoc parsers terminate the table at the blank or non-pipe line. The executor faces an undefined choice between:
- (a) Breaking the table (and parser).
- (b) Appending inside the last cell (ambiguous given trailing pipe).
- (c) Creating a new row (changes table semantics).
- (d) Appending as prose below the table (departs from "append to the table row" instruction).

Verifier regex `rg "Adjudicated Phase 19.*accept-resolution.*evidence/B-02"` passes whether the annotation is inside the cell, in a broken-table fragment, or in a paragraph below.

**Why it matters.** Phase 17/18/19 issue-doc edits could silently corrupt the table format if D-14 is treated as "any of these is fine." The convention is supposed to become milestone-wide.

**Suggested fix.** Lock one option in `19-CONTEXT.md` D-14 (and propagate to all plans):
- **Option A (recommended):** HTML comment immediately below the row — `<!-- Adjudicated Phase 19: accept-resolution. See evidence/B-02.md -->`. Doesn't break the table; greppable; invisible in rendered Markdown.
- **Option B:** Add a new dedicated `Adjudication` column to the Issue Doc table (one-time schema change applied to all rows; uncontested rows get blank or `--`).
- **Option C:** Append inside the last cell with HTML break `<br>` — `| ... | last cell text<br>**Adjudicated Phase 19:** ... |`.

Add a `pandoc --dry-run` table-parse check to the P04 structural verification.

---

### M3. Negated pseudo-ALM regex `! rg "lambda_p.*L_phys.*mu_p.*L_phys"` is a tautology
**Persona:** Feasibility (F2)
**Classification:** process-artifact (verify-command bug)
**Confidence:** high

**Evidence.** The forbidden-match pattern appears in:
- Plan 19-01 Task 2 verify (line 318)
- Plan 19-02 Task 2 verify (line 453)
- Plan 19-04 AC-PHYS-05 (line 279)

The actual existing pseudo-ALM in `ctl_instruction.md:1095`:
```latex
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_{p}\mathcal{L}_{\text{physics}} + \frac{\mu_{p}}{2}\mathcal{L}_{\text{physics}}^{2} + \lambda_{E}(k)\mathcal{L}_{\text{energy}}
```

The literal token `L_phys` never appears in the file. So `! rg ... lambda_p.*L_phys.*mu_p` passes trivially whether the ALM block is removed or left intact. **The structural check is non-functional.**

**Suggested fix.** Replace with LaTeX-aware patterns:
```bash
! rg -n '\\lambda_\{p\}.*\\mathcal\{L\}_\{\\text\{physics\}\}.*\\mu_\{p\}' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
! rg -n '\\frac\{\\mu_\{p\}\}\{2\}' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
! rg -n '\\mathcal\{L\}_\{\\text\{physics\}\}\^\{2\}' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

Or simpler: search for any occurrence of `\lambda_{p}` and `\mu_{p}` in the same file.

---

### M4. Symbol rename grep cannot detect surviving LaTeX symbols
**Persona:** Feasibility + Coherence (F3, C2)
**Classification:** process-artifact (verify-command bug)
**Confidence:** high

**Evidence.** Plan 19-01 Task 2 verify and Plan 19-02 Task 2 verify both use:
```
! rg -n "epsilon_soft|eps_soft"
```

The actual existing symbols are:
- `\epsilon_{\text{soft}}` in `pinn_architecture.md:416, 428, 549, 600, 613` (LaTeX subscript with `\text`)
- Bare `\varepsilon = 10^{-10}` in `ctl_instruction.md:669` (no subscript at all)

Neither is caught by `epsilon_soft|eps_soft`. Only `epsilon_soft = 1e-5` in the Python listing at `pinn_architecture.md:600` is caught (a single occurrence).

**Why it matters.** A half-finished rename will pass the negated grep. D-18 specifies a comprehensive symbol-family migration that the verify cannot enforce.

**Suggested fix.** Expand verify:
```bash
! rg -n '\\epsilon_\{\\text\{soft\}\}|\\epsilon_\{soft\}|epsilon_soft|eps_soft' \
   pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
   pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md

# The static-V bare varepsilon should be replaced with \epsilon_{\text{inv}}
! rg -n '\\varepsilon\s*=\s*10\^\{-10\}' \
   pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```

Plus positive count checks: `\epsilon_{\text{train}}` should appear ≥ 3 times in `pinn_architecture.md` (residual, Hamiltonian, Python listing).

---

### M5. Wave-1 parallel ledger writes collide on `16-ISSUE-LEDGER.md`
**Persona:** Feasibility (F4)
**Classification:** operational
**Confidence:** high

**Evidence.** Both P01 and P02 declare `wave: 1, depends_on: []` and both touch `16-ISSUE-LEDGER.md`:
- P01 Task 1: B-02 + M4 rows → IN_PROGRESS + M4 row reclassification + per-finding subsection audit note
- P02 Task 1: B-07 + B-08 + B-09 rows → IN_PROGRESS
- P01 Task 3: B-02 + M4 rows → FIX_APPLIED
- P02 Task 3: B-07 + B-08 + B-09 rows → FIX_APPLIED
- P04 Task 2: all five rows → VERIFIED + AC-PHYS-01..06 reservation block

Both Wave-1 plans run in parallel per `19-CONTEXT.md` D-12. No merge strategy is specified.

**Why it matters.** If both plans run as separate workers, the second worker's commit will hit a git conflict on the ledger file. Adjacent table rows merge cleanly only sometimes — the lifecycle-rules / phase-exit-gate sections near the bottom of the ledger are also touched, increasing conflict likelihood.

**Suggested fix.** Choose one:
- (a) **Serialize ledger commits:** P02 Task 1 waits for P01 Task 1's ledger commit. Downgrade D-12 from "parallel" to "spec files in parallel, ledger interleaved." Add `depends_on_artifact: ["16-ISSUE-LEDGER.md after 19-01-task-1"]` to P02.
- (b) **Per-plan delta files:** P01 writes `19-01-LEDGER-DELTA.md`; P02 writes `19-02-LEDGER-DELTA.md`. P04 Task 2 merges all deltas into the canonical ledger as part of closure.
- (c) **Squash-merge per plan:** Each plan's 3 commits squash to 1 at plan boundary; ledger conflicts can then be resolved at squash time.

---

### M6. PHYS-02 forward-reference dangles between Wave-1 commits
**Persona:** Feasibility (F5)
**Classification:** operational
**Confidence:** high

**Evidence.** Plan 19-01 Task 2 retargets `ctl_instruction.md:962` to point at `pinn_architecture.md §5.x (PHYS-02)`. Plan 19-02 Task 2 (which runs in parallel) creates `### 5.x Normalized-Time Derivative Contract (PHYS-02)`. Both commits land independently in Wave 1.

- If P02 fails or stalls between Task 1 and Task 2: ctl spec contains a dangling cross-reference to a section that does not yet exist.
- "§5.x" is a literal placeholder; P02's executor must invent a real section number. If they call it `§5.4`, the cross-reference in ctl says `§5.x`, not `§5.4`.

**Why it matters.** Compounds with M1. P04's verify regex `rg "pinn_architecture.md.*PHYS-02" ctl_instruction.md` passes on the literal string regardless.

**Suggested fix.**
- (a) Move the ctl:962 retargeting from P01 Task 2 to P03 Task 2 (which runs after P02 has chosen real section numbers). P03's "do NOT edit ctl_instruction.md" restriction becomes "only edit the cross-references at lines 962 and total-loss block."
- (b) Reverse wave assignment: P02 first, P01 after. Breaks the "different files → parallel" optimization.

Option (a) is cleanest.

---

### M7. `ε_H = 10⁻⁸` is silently invented — CRITICAL GOVERNANCE violation
**Persona:** Adversarial (A1)
**Classification:** **semantic — must surface per STOP protocol**
**Confidence:** high (verified by direct quote of resolution doc)

**Evidence.** Plan 19-02 Task 2 (line 314) writes:
> `ΔH_n = (H_ε(r_θ'(u_n), v_θ'(u_n)) - H_ε(r_0', v_0')) / (|H_ε(r_0', v_0')| + ε_H), ε_H = 10⁻⁸ is a numerical stability scale`

Resolution doc `ctl_pinn_resolution.md` §8.5 defines `ε_H` symbolically as a denominator floor but **never assigns a numerical value**. (Search-verified: no `ε_H = 10⁻⁸` text exists in the resolution doc.) The plan picks `10⁻⁸` by silent analogy with `ε_L = 10⁻⁸`.

**Why it matters (physics).** For marginally-bound ICs (E_total → 0, parabolic or weakly hyperbolic configurations), `|H₀|` after softening with `ε_train = 10⁻⁵` is bounded away from zero only by softening contributions on the order of `ε_train²/2 ≈ 5·10⁻¹¹`. The denominator becomes `max(|H₀|, ε_H)`. With `ε_H = 10⁻⁸` chosen as floor, any absolute drift `ΔH ~ 10⁻⁵` produces `ΔH_n ~ 10³` — entirely outside the Huber linear regime (δ=1.0), saturating the gradient and effectively turning off energy-conservation learning for these ICs.

**Why it matters (governance).** Per the project `CLAUDE.md` STOP protocol:
> "**Semantic** (mass encoding raw vs fraction, physics derivations the source hedged on, permutation-invariance handling, any sub-flavor the source punted on): **MUST surface**, never invent."

The agent's articulation should have been:
> "The resolution doc gives `ε_H` as a symbol but no numerical value. I am tempted to pick `10⁻⁸` by analogy with `ε_L`. This is **semantic** — the choice affects gradient behavior near low-energy ICs. **MUST surface.**"

This gap was not raised. Instead the value was silently invented.

**Suggested fix.** Open a `19-GAPS.md` entry following the STOP-protocol gap template:
- **Decision point:** Numerical value of `ε_H` in the L_E relative-drift denominator `(|H_ε(r_0', v_0')| + ε_H)`.
- **Classification:** Semantic.
- **Source silence:** `ctl_pinn_resolution.md` §8.5 defines `ε_H` symbolically only (no numerical value).
- **Mathematical grounding:** For marginal-energy ICs with `|H₀| ≲ ε_H`, the relative drift `ΔH_n = ΔH/(|H₀|+ε_H)` becomes pathological. Different choices of `ε_H` shift the IC-class boundary where this happens.
- **Agent was tempted to:** Pick `ε_H = 10⁻⁸` by analogy with `ε_L`. Rationale: same "numerical-stability scale" purpose.
- **What the user needs to decide:** Adjudicate `ε_H` value.
  - Option A: `ε_H = 10⁻⁸` (analogy with `ε_L`)
  - Option B: `ε_H = 10⁻⁶` (one-order safety margin over `ε_train²`)
  - Option C: Use absolute-drift fallback for `|H₀| < threshold` ICs; relative for others
  - Option D: Filter dataset to exclude `|H₀| < some_floor` ICs (couples to Phase 18 D-10 sampling)
- **Confidence of impact:** HIGH (gradient behavior in production training).
- **Status:** OPEN.

---

### M8. B-09 §5 additive-softening force derivation is mathematically wrong
**Persona:** Adversarial (A2)
**Classification:** semantic — false physics in audit record
**Confidence:** high (rigorously checked)

**Evidence.** Plan 19-02 Task 1 (line 231) specifies B-09 §5 prose:
> "Plummer softening r_safe = sqrt(||r||² + ε²) preserves the force/potential matched pair: F = -∇V where V ∝ 1/r_safe and F ∝ r/r_safe³. Additive softening (||r|| + ε) does NOT give a matched pair because -∇(1/(||r||+ε)) = r/(||r||·(||r||+ε)²) ≠ r/(||r||+ε)³ in general."

**Verification.** Let V_add = -1/(r+ε), where r = ||r||. Then:
- ∂V_add/∂r_α = (1/(r+ε)²) · (∂r/∂r_α) = (r_α/r) / (r+ε)²
- ∇V_add = r̂/(r+ε)², where r̂ = r/r
- F_add = -∇V_add = -r̂/(r+ε)² = **-r/(r·(r+ε)²)**

The plan correctly writes this on the LHS of its inequality. But the RHS `r/(||r||+ε)³` (cubic denominator) is **not** what any "additive softening" formulation yields. The factor of cube comes from differentiating Newtonian `1/r³` (the unsoftened force law), not from any softened potential.

**Standard alternatives in the literature:**
- Plummer: `V = -1/√(r²+ε²)` ⟹ `F = -r/(r²+ε²)^(3/2)` ✓ matched
- Hernquist / spline softening: piecewise polynomial; matched by construction
- *Unmatched additive:* unsoftened force `r/r³` paired with softened potential `-1/(r+ε)`. **Energy non-conservation by construction.** This is likely what the pre-Phase-19 spec actually had.

The plan's strawman `r/(r+ε)³` corresponds to no published softening method.

**Why it matters.** The B-09 evidence packet becomes the permanent audit record explaining why Plummer was chosen over additive. If it cites a non-existent "additive force law" as the rejected alternative, future FUT-01 implementers will be confused about what was actually rejected. The locked verdict (Plummer) is unaffected; the audit record is what's broken.

**Suggested fix.** Rewrite B-09 §5's "Additive softening does NOT give a matched pair" paragraph to:

> Plummer V_ε = -1/r_safe with r_safe = √(r²+ε²) yields F = -∇V_ε = -r/r_safe³ exactly. This is a matched gradient pair derived from a single r_safe definition.
>
> The pre-Phase-19 spec used additive forms (||r||+ε) for potentials. The force derived from V_add = -1/(||r||+ε) is F_add = -r̂/(||r||+ε)² = -r/(||r||·(||r||+ε)²) — algebraically valid but with a non-Newtonian r→0 limit and a denominator that mixes ||r|| with (||r||+ε), making the force-potential relationship harder to inspect and verify.
>
> Worse, the pre-Phase-19 spec paired this additive potential with an unsoftened-Newtonian force expression in the residual (or a mismatched cubic-denominator force in some sections), breaking the F = -∇V identity and thus breaking energy conservation by construction.
>
> Plummer is preferred because (a) the gradient pair is automatic and algebraically clean from a single r_safe definition, and (b) the matched pair is closed-form and well-behaved at r→0.

---

## 🟡 SHOULD_FIX — Significant Issues (10)

### S1. Divergence schema mismatch (19-04 Task 1 vs CONTEXT D-19) — `safe_auto`-eligible
**Persona:** Coherence (C1)
**Confidence:** high

CONTEXT D-19 (line 349): `Surface | Live code (pinn/) | Spec target (Phase 19) | FUT-01 priority (non-binding hint) | Notes`
Plan 19-04 Task 1 (line 156): `Surface | Live code (file:line) | Spec target (Phase 19 decision) | FUT-01 item | FUT-01 priority`

The two specifications differ in column-3 wording, column-4 name, and column-5 name. D-19 is authoritative.

**Suggested fix.** Update 19-04-PLAN.md Task 1 line 156 to use D-19's schema verbatim.

---

### S2. Python `jacrev` listing has functional errors — `safe_auto`-eligible
**Persona:** Scope-Guardian (S2)
**Confidence:** high

Plan 19-02 Task 2 (lines 416–434):
```python
def model_single(u_scalar, ic13):
    return net(torch.cat([2*u_scalar - 1, ic13]))  # tau = 2u-1

J = jacrev(model_single)(u, ic13)  # shape (9, 1) -> 9 derivatives
```

Two errors:
- `torch.cat([2*u_scalar - 1, ic13])` fails at runtime: `2*u_scalar - 1` is 0-D scalar; `ic13` is 1-D. Needs `(2*u_scalar - 1).unsqueeze(0)`.
- `jacrev(f)(u_scalar, ic13)` returns shape `(9,)` for scalar input, not `(9, 1)`. Comment is wrong.

**Why it matters.** Spec-illustrative listings get copied. A wrong listing in the AD-correctness contract section undermines the anti-pattern warning it accompanies.

**Suggested fix.**
```python
def model_single(u_scalar, ic13):
    """Single-trajectory forward pass. u_scalar: shape (); ic13: shape (13,)."""
    tau = (2*u_scalar - 1).unsqueeze(0)  # shape (1,)
    return net(torch.cat([tau, ic13]))

# dr'/du for all 9 output components:
J = jacrev(model_single)(u_scalar, ic13)  # shape (9,) — 9 partial derivatives dr'_k/du
```

---

### S3. AC-PHYS-04 structural check (HNN sweep) not in automated verify block
**Persona:** Feasibility (F9)
**Confidence:** high

Plan 19-04 Task 2 AC-PHYS-04 section (lines 266–274):
```bash
# HNN-style framing removed
rg -n "HNN-style|HNN architecture|borrowing.*benefit.*HNN|Hamiltonian Neural Network" pinn_architecture.md
# (should return 0 matches)
```

No `!` prefix. The full `<automated>` verify block at lines 342–344 only checks for the verification file's existence and `PASS` markers — it does **not** include the negated HNN sweep. P04 can transition findings to VERIFIED while HNN language survives.

**Suggested fix.** Move the HNN sweep into the `<automated>` block as a chained `&& !` clause:
```bash
&& ! rg -q "HNN-style|HNN architecture|borrowing.*benefit.*HNN|Hamiltonian Neural Network" \
       pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```

---

### S4. Plan 19-04 final negated regex is malformed
**Persona:** Feasibility (F8)
**Confidence:** high

Plan 19-04 Task 2 `<verify>` last segment:
```
! rg -n "^\\| B-02 .*IN_PROGRESS\|^| B-02 .*FIX_APPLIED\|^| B-07 .*IN_PROGRESS\|^| ..."
```

The mixed `\|^|` reads as: literal pipe `\|`, then `^` (line-start anchor mid-pattern), then `|` (alternation). The alternation immediately after `^` reads as an empty alternative, which matches blank lines, returning matches and tripping `!`. **The negated check likely fails on every run.**

**Suggested fix.**
```bash
! rg -n '^\| (B-02|B-07|B-08|B-09|M4) .*(IN_PROGRESS|FIX_APPLIED)' \
     .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md
```

---

### S5. L_E / L_L denominator degeneracy at marginal ICs
**Persona:** Adversarial (A5)
**Classification:** semantic — silent failure mode
**Confidence:** high

`ΔH_n` denominator: `|H_ε(r_0', v_0')| + ε_H`. `L_L` scale: `||L_0'|| + ε_L`.

- **Energy degeneracy:** For parabolic IC (E_total = 0 exactly), `|H₀'|` after softening is bounded only by `ε_train²/2 ≈ 5·10⁻¹¹`. Denominator collapses to `max(ε_H, |H₀'|)` ≈ `10⁻⁸`. Any absolute drift `ΔH ~ 10⁻⁵` blows ΔH_n to 10³, saturating Huber.
- **Angular-momentum degeneracy:** For aligned-collinear ICs (all three bodies on a line through COM), `||L_0'|| → 0`, L_scale → `ε_L = 10⁻⁸`, same explosion.

The IC distribution from `simulation_data` is filtered by `epsilon = 0.05` minimum separation (per D-17) but not by minimum `|E|` or `|L|`. Both pathological IC classes are admissible.

**Why it matters.** With λ_E = λ_L = 1 in stages k ≥ 4, low-|H₀| or near-aligned ICs will dominate gradient through saturation effects or contribute nothing via gradient-clip masking. Either way the contract is silently broken for orbit classes the dataset contains.

**Suggested fix.** Add a one-line note in the L_E / L_L documentation in `pinn_architecture.md`:
> "The relative-drift formulation assumes `|H₀| ≳ 10⁻³` and `||L₀|| ≳ 10⁻³` in dimensionless units (typical for bound non-marginal ICs). Marginally-bound or near-aligned ICs may require either curriculum-stage exclusion or absolute-drift fallback. Deferred to Phase 21 VER-01 distribution sanity check."

Or surface as a `19-GAPS.md` entry for user adjudication.

---

### S6. η_c = 1 causal weight does not scale with collocation density N_t
**Persona:** Adversarial (A4)
**Classification:** semantic
**Confidence:** medium-high

Plan 19-02 Task 2 (line 354): `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m)), w_1 = 1, η_c = 1 default`.

For N_t = 100 collocation points and R̄ ~ 1 early in training, `w_N_t ~ e⁻¹⁰⁰ ≈ 10⁻⁴⁴`. Effective vanishing. For N_t = 10, `w_N_t ~ 4·10⁻⁵` — small but recoverable. Same η_c=1 over different N_t produces very different effective horizons.

Standard solutions in the literature (Wang–Sankaran–Perdikaris): scale η_c ~ 1/N_t or normalize R̄ by N_t. The plan adopts neither.

**Suggested fix.** Add a note in the L_phys^causal section:
> "η_c = 1 assumes per-stage collocation densities O(10²) consistent with curriculum staging defined in Phase 20. Larger N_t may require η_c → η_c/N_t or analogous normalization (deferred to Phase 21 VER-01 numeric tuning)."

---

### S7. M4 §5/§9 overstates "9 is correct" — constraint count is convention-dependent
**Persona:** Adversarial (A3)
**Classification:** semantic — audit-record fidelity
**Confidence:** high (literature cross-checked)

Plan 19-01 Task 1 (line 171): M4 §5 prose:
> "Constraints: 3 COM position + 3 COM momentum + 3 SO(3) rotation = 9 constraints, yielding a 9-dimensional reduced phase space (not 8). The issue doc's arithmetic is correct."

Plan 19-01 Task 1 (line 174): M4 §9 prose:
> "issue doc arithmetically correct on counting (9, not 8)"

**The constraint count is convention-dependent:**
- 18 = full phase space (positions + momenta, 9+9) ✓
- 18 − 3(P) − 3(X_COM) − 3(L) = 9 ← the plan's count (translations + rotation generators)
- 18 − 10(full Galilean: 3 translations + 3 boosts + 3 rotations + 1 time-translation) = 8 ← Marchal (1990) convention, and likely what the pre-Phase-19 spec used
- 18 − 3(COM only) − 3(momentum only) = 12

Both 8 and 9 are defensible under different conventions. The plan's confident assertion "9 is uniquely correct, 8 is wrong" is overstated and will mislead future readers.

**Note:** The locked verdict (D-03) is correct — constraint counting is the wrong justification altogether. That decision is sound. The problem is the audit-record text's confidence.

**Suggested fix.** Rewrite M4 §5:

> Reduced phase-space dimension is convention-dependent. Counting only configuration-space DOF: 9 − 3(COM) = 6. Counting full phase space and quotienting by translations + momenta + rotation generators: 18 − 3 − 3 − 3 = 9 (the issue doc's count). Quotienting by the full 10-dim Galilean group including boosts and time-translation/energy: 18 − 10 = 8 (Marchal 1990 convention; likely the source of the pre-spec's "8"). Both 8 and 9 are defensible.
>
> The deeper point per resolution doc §10.4 is that constraint counting is the wrong justification altogether. The IC13 validity comes from being a reconstructive gauge-fixed encoding (Phase 17 IO-02 + Phase 18 FRAME-01), not from DOF arithmetic.

And rewrite M4 §9:
> "Both source positions are partially correct depending on the constraint-counting convention chosen; both are wrong on relevance under Jacobi-state IC13. Resolution doc correct on rejecting the framing altogether."

---

### S8. Numerical defaults lack provenance citations in evidence packets
**Persona:** Adversarial (A6)
**Confidence:** high

Of ~10 numerical defaults the plans encode:
- **Grounded in resolution doc** (verified): `ε_train = 10⁻⁵` (§7.1:750), `ε_inv = 10⁻¹⁰` (§7.2:791), `ε_L = 10⁻⁸` (§8.6:952), `η_c = 1` (§8.4:918), `δ = 1.0` Huber (§8.5:934), `δ_r = 1` (§8.2:860), `β_v = 1` (§8.3:883), `λ_IC = 1` and ablation `[0.1, 10]` (§8.7:1006–1009), `I_warm = min(2000, 0.1·N_Adam,k)` (§8.7:969), warmup schedule (§8.7:985–991).
- **Not grounded:** `ε_H` (see M7).

The plans cite line numbers only for `ε_train`, `ε_inv`, `ε_L`. The other defaults are transcribed on faith.

**Suggested fix.** Add a "Numerical defaults provenance" subsection to B-07, B-08, B-09 packets:
```
ε_train = 10⁻⁵: resolution §7.1 line 750
ε_inv = 10⁻¹⁰: resolution §7.2 line 791
ε_L = 10⁻⁸: resolution §8.6 line 952
ε_H = 10⁻⁸: NOT GROUNDED — see 19-GAPS.md
η_c = 1: resolution §8.4 line 918
δ = 1.0 (Huber): resolution §8.5 line 934
δ_r = 1: resolution §8.2 line 860
β_v = 1: resolution §8.3 line 883
λ_IC = 1: resolution §8.7 lines 1006-1009
I_warm: resolution §8.7 line 969
Warmup schedule {0,0,10⁻²,10⁻¹,1,1,1}: resolution §8.7 lines 985-991
```

---

### S9. 19-03 Task 2 violates STOP protocol with "log and continue"
**Persona:** Feasibility + Scope-Guardian (F11, S9) — overlaps M1
**Confidence:** high

Plan 19-03 Task 2 (line 195): "log any cross-reference gap found and continue."

Per `CLAUDE.md` CRITICAL GOVERNANCE STOP protocol, detected gaps must stop affected work and surface to user. "Log and continue" is not a permitted classification.

**Suggested fix.** Either:
- (a) Make P03 empowered to fix mechanical cross-reference errors (M1 fix path).
- (b) Make detected cross-reference gaps a STOP-protocol event: record in `19-GAPS.md`, halt P04, wait for instruction.
- (c) Eliminate the gap by adopting M1's section-agnostic prose approach in P01.

Option (c) is cleanest.

---

### S10. Commit-before-verify ordering creates partial-success states
**Persona:** Feasibility (F6)
**Confidence:** high

Plans 19-01, 19-02, 19-03 each have tasks that:
1. Make spec edits (in-place)
2. Commit
3. Run `<verify>` (after commit)

If verify fails at step 3, the bad edit is already on the branch. No rollback recipe documented anywhere.

**Suggested fix.**
- (a) Restructure each Task's `<action>` to: `make edits → verify → commit` (verify gates commit).
- (b) Add a top-level "Failure Recovery" section to each plan: `git revert HEAD && reopen task` with explicit recovery commands.

---

### S11. "Or equivalent" hedge for M4 replacement target
**Persona:** Feasibility (F7)
**Confidence:** high

Plan 19-01 Task 2 PHYS-06 action:
> Replace the sentence at `ctl_instruction.md:914-915` (the text `"13 constraints for an 8-dimensional reduced phase space ensure over-determination and uniqueness"` or equivalent)

The live text (verified): "The 13 constraints for an 8-dimensional reduced phase space ensure over-determination and uniqueness." — capital "The", in item 1 of an enumerated Injectivity list across lines 913–915.

**Structural ambiguity:** Replace the trailing sentence of the Injectivity bullet? The whole bullet? Insert as new subsection? The plan's replacement block `"**IC13 Validity (locked Phase 19, PHYS-06):** ..."` doesn't fit naturally as the tail of "Injectivity."

**Suggested fix.** Specify in 19-01 Task 2:
> "Replace the last sentence of item 1 (Injectivity), starting with 'The 13 constraints' and ending with 'uniqueness.', with the IC13 Validity block as a standalone paragraph between item 1 and item 2 of the enumerated list."

Or lift the IC13 Validity block out of the enumerated list and place it as a new subsection above "#### Mathematical Guarantees" (line 908).

---

## 🔵 CONSIDER — Worth Addressing (7)

### Co1. D ≈ 4.6416 assumes hidden T = 10 in natural units
**Persona:** Adversarial (A7)
**Confidence:** medium

`(G·T²)^(1/3) = 4.6416` requires `G·T² ≈ 100`. Most likely interpretation: G=1 natural units, T=10 (matches `simulation_data` standard 3BP dataset convention). The spec never names T's value.

**Suggested fix.** In ctl_instruction.md Governing Mathematical Convention block, state explicitly:
> "In G=1 natural units with the dataset convention T = 10 (see `simulation_data/Documentation/README.md`), D = (1 · 100)^(1/3) ≈ 4.6416. Both G and T are dimensionless choices of this framework; D is derived."

---

### Co2. Linear momentum conservation silent in loss contract
**Persona:** Scope-Guardian (S10)
**Confidence:** medium

L_total has L_E (energy) and L_L (angular momentum) but no L_P (linear momentum). Reason: COM projection head (Phase 17 D-02) enforces total linear momentum = 0 at every output time step by construction.

**Suggested fix.** Add one sentence to L_total documentation:
> "Linear momentum conservation is not enforced via a dedicated loss term because the COM projection head (§2.x, Phase 17 D-02) enforces total linear momentum = 0 by construction at every output time step. A dedicated L_P term would be redundant."

---

### Co3. L_IC,v vs IC13 velocity slot redundancy
**Persona:** Adversarial (A9)
**Confidence:** medium

L_IC,v = MSE(v_θ'(0), v_0') forces the AD-derived initial velocity to match v_0' (reconstructable from IC13's Jacobi velocity slots). β_v = 1 weights v and r anchors equally, but MSE on velocity (units of D/T) and on position (units of D) have different scales.

**Suggested fix.** Add a note to L_IC documentation:
> "β_v = 1 assumes scaled-velocity v' = dr'/du is O(1) in the natural problem scale; if dataset distribution shows |v'| ≫ |r'| typically, β_v may need rescaling. Phase 21 should sanity-check empirically."

---

### Co4. B-09 "category error" framing partially strawmans the issue doc
**Persona:** Adversarial (A10)
**Confidence:** medium

The issue doc's "5 orders of magnitude mismatch" may admit two readings: (a) PINN-internal ε_train vs ε_inv (the rebutted reading), or (b) simulation_data ε=0 vs PINN ε_train=10⁻⁵ (a valid model-vs-data bias concern). The plan addresses (a) cleanly but treats (b) as nonexistent.

**Suggested fix.** Soften B-09 §9 to:
> "The issue doc's 5-orders framing admits two readings: (a) PINN-internal static vs training ε (a category error — different purposes), and (b) simulation_data ε=0 vs PINN ε_train=10⁻⁵ (a valid model-vs-data bias concern). Reading (b) is addressed by noting that Plummer's relative bias ε²/(2r²) ~ 5·10⁻¹⁹ at ε_train=10⁻⁵, r ≥ 0.05 is far below dataset noise; the gap is real but acceptable."

---

### Co5. No rollback recipe
**Persona:** Feasibility (F13)

For a 4-plan dependency chain (P03 blocked on P02; P04 blocked on Waves 1-2), a verify failure in P02 Task 2 (the largest single edit in v1.4) leaves the working tree in an unknown partial state, and P03 cannot start.

**Suggested fix.** Add a "Failure Recovery" section to each plan or to `19-CONTEXT.md`:
- If P01 Task N fails: `git reset --hard <P01-Task-(N-1)>` and re-run P01 from Task N.
- If P02 Task N fails: same.
- If P03 Task N fails: `git reset --hard <Wave-1-tip>` and re-run P03.
- Reverting requires user confirmation per `CLAUDE.md` destructive-op protocol.

---

### Co6. simulation_data anchor pre-flight not enforced
**Persona:** Feasibility (F12)

B-09 §5 cites specific line ranges (`ic_generation_utils.py:60-81, 223, 261, 572`). I spot-checked at this review; all are correct. But no plan task verifies the anchors pre-execution, and `simulation_data` could shift line numbers via unrelated edits.

**Suggested fix.** Add to P02 Task 1 `<read_first>`:
```bash
# Verify cited line anchors are still valid
rg -n "def __init__\(self, epsilon: float = 0.05" simulation_data/Scripts/ic_generation/ic_generation_utils.py
rg -n "self.epsilon = epsilon" simulation_data/Scripts/ic_generation/ic_generation_utils.py
# Surface gap if anchors differ from cited line numbers
```

---

### Co7. B-02 §5 prose introduces opaque `M_scale`
**Persona:** Adversarial (A8)

The plan's B-02 §5 introduces `M_scale` parameter without grounding it. The resolution doc §3.1 has a cleaner direct-substitution derivation.

**Suggested fix.** Replace the M_scale construction with the resolution doc's direct substitution. (Full text in adversarial finding A8.)

---

## ℹ️ FYI — Observations (6)

- **Fy1. Title `"...with Hamiltonian Regularization"` — keep or change?** (F16) D-09 nuance ambiguous: is "Hamiltonian Regularization" an architectural-HNN claim (forbidden) or a reference to the analytic H_ε function (allowed)? Currently P03 doesn't tell the executor which way to read this.

- **Fy2. `19-VERIFICATION.md` schema unspecified.** (F17) P04 Task 2 creates the file without a template. The verify regex passes if `PASS` appears once and each AC-PHYS-NN name appears once — extremely permissive.

- **Fy3. Explicit-loop AD pattern is correctness-fragile under batching.** (A11) The spec illustrative `for k in range(9): torch.autograd.grad(r_prime[k], u)[0]` is correct for scalar u but ambiguous for batched u (B, 1). Phase 21 VER-04 should add a batched-case correctness probe.

- **Fy4. Unicode equation equivalence not enforced.** (F14) The cross-file total-loss text-match check uses a permissive regex that tolerates Unicode/ASCII variation but doesn't enforce character-level identity between the two specs.

- **Fy5. Cross-phase decision-ID references not robust to renumbering.** (A12) M4 replacement prose hard-cites "Phase 17 (IO-02) and Phase 18 (FRAME-01)." If Phase 17/18 decisions are later renumbered, the audit chain breaks silently.

- **Fy6. Numerical precision (float32 vs float64) silent.** (S13) The resolution doc references float64 for parsing; loss-term and AD-leaf precision is unspecified. May couple to Phase 20 ARCH-01..05.

---

# Recommended Routing of Findings

Per the project's CRITICAL GOVERNANCE STOP protocol, findings classified as **semantic** that the plans silently invented should be surfaced as `19-GAPS.md` entries before any plan execution begins. The mechanical/operational findings should be patched into the plans themselves.

## Recommended actions before Wave 1 starts:

### A. Surface as `19-GAPS.md` entries (per STOP protocol):
1. **M7** — `ε_H = 10⁻⁸` ungrounded numerical default
2. **S5** — L_E / L_L degeneracy at marginal ICs (could be note vs gap, user's call)

### B. Patch into plan files (mechanical, no governance question):
3. **M3, M4, S3, S4** — Verify-command regex fixes (LaTeX-aware patterns)
4. **S1** — 19-04 schema alignment with D-19
5. **S2** — Python `jacrev` listing corrections
6. **M5** — Wave-1 ledger serialization strategy
7. **M6** — Move ctl:962 retargeting from P01 to P03
8. **M1, S9, S11** — Section-agnostic cross-references; M4 replacement boundary
9. **S10, Co5** — Failure-recovery section per plan

### C. Improve audit-record text (semantic but non-governance):
10. **M8** — Rewrite B-09 §5 additive-force derivation
11. **S7** — Rewrite M4 §5/§9 to acknowledge convention-dependence of 8 vs 9
12. **S8** — Add numerical-defaults provenance subsection
13. **Co1** — Pin D's hidden T-value
14. **Co4** — Soften B-09 §9 "category error" framing

### D. Apply during P02/P03 execution:
15. **M2** — Lock D-14 annotation format (HTML comment recommended)
16. **S6** — Add η_c scaling note
17. **Co2** — Add linear-momentum-via-COM-projection note to L_total
18. **Co3** — Add β_v scaling note
19. **Co6** — Add simulation_data anchor pre-flight check
20. **Co7** — Tighten B-02 §5 derivation
21. **Fy1** — Decide title fate

### E. Leave for Phase 21 / future awareness:
22. **Fy2** — `19-VERIFICATION.md` schema (define template in Phase 21)
23. **Fy3** — Batched AD correctness probe (Phase 21 VER-04)
24. **Fy4, Fy5, Fy6** — Robustness observations

---

# Summary

| Severity | Count | Most critical |
|---|---|---|
| **MUST_FIX** | 8 | M7 (ε_H STOP-protocol violation); M8 (B-09 wrong derivation); M1 (cross-ref instability) |
| **SHOULD_FIX** | 10 | S5 (marginal-IC degeneracy); S7 (M4 convention overclaim); S3/S4 (verify-block bugs) |
| **CONSIDER** | 7 | Co1, Co2, Co3, Co4 (audit-record polish) |
| **FYI** | 6 | Fy1 (title decision) |

**Overall assessment:** The plans are competent and largely correct in their decision transcription. The locked decisions in 19-CONTEXT are sound. The plans will fail at execution time due to a small number of high-impact regex bugs (M3, M4, S3, S4) and undecided process-artifact mechanics (M1, M2, M5, M6). One semantic issue (M7) is a CRITICAL GOVERNANCE STOP-protocol violation that must be surfaced before execution. Two audit-record issues (M8, S7) embed misleading or wrong physics in permanent evidence packets and should be fixed before P04 closure.

**Minimum bar before execution:** Address M1, M2, M3, M4, M5, M6, M7, M8 (the 8 must_fix). Should-fix items can be addressed during execution or in follow-up commits if execution discipline is tight.

---

**End of review.**

*Generated by `compound-engineering:ce-doc-review` skill with 4 parallel persona agents (coherence, feasibility, scope-guardian, adversarial). Round 1 — no prior decisions.*
