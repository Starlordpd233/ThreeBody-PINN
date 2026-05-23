# Phase 19 Plan Review - Codex

**Date:** 2026-05-22  
**Reviewer:** Codex inline review via `gsd-plan-review-convergence` gate discipline  
**Scope:** `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md` through `19-04-PLAN.md`

## Summary

CYCLE_SUMMARY: current_high=6

## Current HIGH Concerns

- `19-01` and `19-02` are marked parallel even though both mutate the same ledger and Issue Doc files.
- `19-01` would write an incorrect B-02 dimensional-analysis statement saying the issue-doc value `6.694` corresponds to `M_tot=1`.
- `19-02` reintroduces a free `G'` coefficient in the scaled force/potential formulas, weakening the raw-mass nondimensionalization lock.
- `19-02` does not explicitly rewrite `pinn_architecture.md` §3.1 from L1/MAE data loss to the resolution-doc Huber default.
- `19-01`/`19-02` omit the causal-weight exponent clipping stated by the resolution doc.
- `19-04` can mark findings `VERIFIED` with a verification artifact that merely contains strings, not necessarily passing structural checks.

## Reviewed Materials

- Phase plans: `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md`, `19-02-PLAN.md`, `19-03-PLAN.md`, `19-04-PLAN.md`.
- Phase context: `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md`.
- Requirements and roadmap: `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`.
- Candidate verdict source: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`.
- Issue source: `pinn_instruction/issues/01-architecture-and-physics-foundations.md`.
- Current target specs: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`.
- Ledger and precedents: `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`, `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md`, `.planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md`.

## Findings

### HIGH-01: Wave-1 parallelism is unsafe because the plans share mutable files

`19-01` says it runs in parallel with `19-02` because they touch different files (`19-01-PLAN.md:49`). `19-02` repeats the same claim (`19-02-PLAN.md:55`). That is only true for the two framework-spec files. Both plans list and later edit `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` and `pinn_instruction/issues/01-architecture-and-physics-foundations.md` (`19-01-PLAN.md:8`, `19-01-PLAN.md:12`, `19-01-PLAN.md:13`, `19-02-PLAN.md:8`, `19-02-PLAN.md:13`, `19-02-PLAN.md:14`).

Why it matters: if the executor actually runs Wave 1 in parallel, the ledger and Issue Doc row appends can race, conflict, or commit stale state. This directly affects VER-05 lifecycle integrity because the ledger is the closure authority (`16-ISSUE-LEDGER.md:44`, `16-ISSUE-LEDGER.md:48`, `16-ISSUE-LEDGER.md:54`).

Recommended fix: keep the spec edits parallel only if necessary, but serialize every task that touches the shared ledger or Issue Doc. The simplest repair is to move all five Issue Doc annotations and all ledger state transitions into a single follow-up task after both Wave-1 spec edits land.

### HIGH-02: B-02 evidence text has a mass-scale error

`19-01` instructs `B-02.md` §5 to say: "The issue doc's 6.694 value corresponds to M_tot=1 (in natural units) and mass fractions" (`19-01-PLAN.md:163`). That is not correct as written. The issue doc computes `D = (G * M_tot * T^2)^(1/3) = (3 * 100)^(1/3) = 6.694` (`01-architecture-and-physics-foundations.md:72`), so the physical total mass used in that value is `M_tot=3`, not `1`.

Mathematically, the mass-fraction convention makes the dimensionless masses sum to one, but the characteristic scale still contains the physical `M_tot`: the resolution doc shows `D=(GM_tot T^2)^(1/3)` implies `GT^2/D^3 = 1/M_tot` (`ctl_pinn_resolution.md:180`, `ctl_pinn_resolution.md:191`), producing mass fractions `m_j/M_tot` in the scaled equation (`ctl_pinn_resolution.md:197`, `ctl_pinn_resolution.md:204`). The raw-mass convention instead forces `D^3=GT^2` (`ctl_pinn_resolution.md:165`, `ctl_pinn_resolution.md:175`).

Recommended fix: replace that sentence with: "The issue doc's `6.694` value corresponds to a mass-fraction rewrite using the physical total mass `M_tot=3`; in that rewritten dimensionless equation the mass fractions sum to one. That is a different convention from the raw-mass v1.4 contract."

### HIGH-03: `G'` in the scaled Plummer formulas reopens the scaling convention

`19-02` defines the Plummer force as `F_ij = G' · m_j · (...) / r_safe^3` and says `G'` is the dimensionless gravitational constant (`19-02-PLAN.md:288`, `19-02-PLAN.md:290`). It similarly includes `G'` in the potential (`19-02-PLAN.md:298`).

The resolution doc's raw-mass nondimensionalization chooses `D^3=GT^2` precisely so the scaled residual coefficient is one (`ctl_pinn_resolution.md:161`, `ctl_pinn_resolution.md:175`). Its final acceleration formula contains no `G'` factor (`ctl_pinn_resolution.md:759`, `ctl_pinn_resolution.md:763`), and its Hamiltonian likewise omits `G'` (`ctl_pinn_resolution.md:765`, `ctl_pinn_resolution.md:769`).

Why it matters: an unqualified `G'` invites an implementation to carry a second gravitational constant through a system where the scaling convention has already absorbed it. That would be a spec ambiguity in the core PHYS-01/PHYS-03 contract.

Recommended fix: remove `G'` from the snippets, or explicitly state once that `G' = 1` after the Phase 19 raw-mass nondimensionalization and must not be independently tuned.

### HIGH-04: `L_data` Huber default is not explicitly applied to §3.1

The resolution doc changes the data loss default to Huber with `δ_r=1` (`ctl_pinn_resolution.md:845`, `ctl_pinn_resolution.md:860`). The current `pinn_architecture.md` §3.1 still says the data fidelity loss is L1/MAE (`pinn_architecture.md:331`, `pinn_architecture.md:340`).

`19-02` mentions Huber only inside the new total-loss term list (`19-02-PLAN.md:352`), and `19-03` checks the summary table lists `L_data (Huber)` (`19-03-PLAN.md:109`, `19-03-PLAN.md:149`). Neither plan explicitly rewrites the existing §3.1 prose and formula where the contradiction originates.

Why it matters: after execution, the spec could simultaneously say §3.1 data loss is L1 and the total-loss summary says Huber. That violates PHYS-05's goal of a coherent loss contract.

Recommended fix: add a `19-02` task item to rewrite §3.1 to Huber on projected, gauge-frame positions with `δ_r=1`, preserving L1 only as an allowed ablation if that is intended. Add a verification check for the §3.1 formula/prose, not just the summary table.

### HIGH-05: Causal-weight clipping from the resolution doc is omitted

The resolution doc states that causal residual weights use `η_c=1` with clipping of the exponent to avoid underflow (`ctl_pinn_resolution.md:915`, `ctl_pinn_resolution.md:921`). Phase context preserves this detail in D-10 (`19-CONTEXT.md:209`, `19-CONTEXT.md:211`).

The replacement blocks in `19-01` and `19-02` include the exponential weighting and `stopgrad`, but not exponent clipping (`19-01-PLAN.md:293`, `19-01-PLAN.md:295`, `19-02-PLAN.md:354`, `19-02-PLAN.md:355`).

Why it matters: without clipping, later collocation weights can underflow to zero on high-residual trajectories, silently removing later-time residual pressure. That is a numerical-stability contract, not just prose.

Recommended fix: add an explicit default clipping clause to both total-loss replacement blocks and the verification regexes, e.g. "clip the exponent before `exp` to avoid underflow; the exact numeric clamp is Phase 21 VER-01/VER-04 scope unless already locked."

### HIGH-06: `19-04` closure checks can pass without real structural verification

`19-04` instructs the executor to create `19-VERIFICATION.md`, run each AC check, and record PASS/FAIL (`19-04-PLAN.md:222`). But the automated close command only checks that the file exists and contains at least one match for `PASS|AC-PHYS-01|...` (`19-04-PLAN.md:343`). That regex does not require every AC to have a PASS row. It would pass on a file containing a single AC name.

Several embedded checks are also non-executable as written:

- Checks that "should return 0 matches" are plain positive `rg` commands, not `! rg` assertions (`19-04-PLAN.md:264`, `19-04-PLAN.md:268`, `19-04-PLAN.md:276`, `19-04-PLAN.md:280`, `19-04-PLAN.md:288`, `19-04-PLAN.md:298`).
- The final no-stale-status regex uses escaped pipes inconsistently and is unlikely to test the intended alternatives cleanly (`19-04-PLAN.md:343`).
- The final guard after summary creation says to rerun Task 2's automated command (`19-04-PLAN.md:397`), but that command still does not rerun the structural AC commands.

Why it matters: Phase 19's final task advances all five findings to `VERIFIED` (`19-04-PLAN.md:301`, `19-04-PLAN.md:303`). The ledger rules say `VERIFIED` requires a passing acceptance check (`16-ISSUE-LEDGER.md:48`). A string-presence check is not enough to support that state transition.

Recommended fix: make `19-04` run an executable verification script or a single `bash -lc` block with one assertion per AC marker, one assertion per expected absence, and explicit `PASS: AC-PHYS-NN` rows generated only after each command succeeds. The final guard should require all six `PASS: AC-PHYS-NN` lines and no `FAIL`.

### MEDIUM-01: Verification regexes are brittle against the exact planned math notation

Many verification commands search ASCII spellings that the required snippets do not necessarily contain. Examples:

- `19-01` checks `epsilon_inv.*10.*-10`, while its snippet uses `ε_inv = 10⁻¹⁰` (`19-01-PLAN.md:247`, `19-01-PLAN.md:318`).
- `19-02` checks `epsilon_train.*10.*-5`, `Delta.*H_n.*H_epsilon`, `chain-rule factors.*tau`, and `2.*dr.*d.*tau`, while the snippets use `ε_train = 10⁻⁵`, `ΔH_n`, `H_ε`, and Greek `τ` (`19-02-PLAN.md:286`, `19-02-PLAN.md:312`, `19-02-PLAN.md:387`, `19-02-PLAN.md:453`).
- `19-04` repeats mixed ASCII/Unicode checks, but `10.*-5` still will not match `10⁻⁵` (`19-04-PLAN.md:255`, `19-04-PLAN.md:257`).

Recommended fix: either require ASCII aliases in the spec text alongside the math symbols, or update the checks to match TeX/Unicode forms intentionally. Avoid relying on one giant regex where a missed glyph causes a false failure.

### MEDIUM-02: `19-03` logs read-only cross-reference defects instead of blocking closure

`19-03` says that if `ctl_instruction.md` cross-references are wrong or missing, the executor should note the gap but not edit `ctl_instruction.md` and continue (`19-03-PLAN.md:190`, `19-03-PLAN.md:195`). The same plan's success criteria require cross-references to be validated (`19-03-PLAN.md:214`, `19-03-PLAN.md:216`), and `19-04` later verifies all findings.

Recommended fix: distinguish "read-only ownership" from "continue anyway." If a `ctl_instruction.md` cross-reference is wrong, `19-03` should fail the phase handoff and route back to `19-01` or a dedicated repair task before `19-04` can mark findings `VERIFIED`.

### LOW-01: Context D-19 contains an internal schema wording inconsistency, but the plan chose the better precedent

`19-CONTEXT.md` says D-19 mirrors `17/18-CODE-DIVERGENCE.md` (`19-CONTEXT.md:76`, `19-CONTEXT.md:347`), but one sentence describes the columns as `Surface | Live code (pinn/) | Spec target (Phase 19) | FUT-01 priority | Notes` (`19-CONTEXT.md:349`). The actual Phase 17 and Phase 18 divergence files use `Surface | Live code (file:line) | Spec target (...) | FUT-01 item | FUT-01 priority` (`17-CODE-DIVERGENCE.md:7`, `18-CODE-DIVERGENCE.md:7`), and `19-04` correctly follows that precedent (`19-04-PLAN.md:153`, `19-04-PLAN.md:156`).

Recommended fix: no Phase 19 plan change needed. Optionally clean up `19-CONTEXT.md:349` later so future agents do not reopen this as a schema dispute.

## Missed Gap Assessment

I did not find a new semantic physics gap that needs the STOP protocol. The main physics choices are grounded:

- Raw-mass scaling is explicitly grounded by the resolution doc's derivation (`ctl_pinn_resolution.md:137`, `ctl_pinn_resolution.md:175`) and user-locked D-01 (`19-CONTEXT.md:56`, `19-CONTEXT.md:59`).
- Plummer training/static split is explicitly grounded by resolution §7.1-7.2 (`ctl_pinn_resolution.md:743`, `ctl_pinn_resolution.md:797`) and user-locked D-02/D-06 (`19-CONTEXT.md:59`, `19-CONTEXT.md:63`).
- AD componentwise derivatives are grounded by resolution §6.4 (`ctl_pinn_resolution.md:721`, `ctl_pinn_resolution.md:737`) and PHYS-02 (`REQUIREMENTS.md:37`).
- ALM restriction is grounded by resolution §8.8 (`ctl_pinn_resolution.md:1011`, `ctl_pinn_resolution.md:1039`) and user-locked D-05 (`19-CONTEXT.md:62`).
- M4's reframing is grounded by resolution §10.4 (`ctl_pinn_resolution.md:1160`, `ctl_pinn_resolution.md:1175`) and user-locked D-03/D-11 (`19-CONTEXT.md:60`, `19-CONTEXT.md:68`).

The review did find process and execution defects that should be fixed before execution. They are not source-silence gaps: the source materials answer the intended behavior, and the plans simply fail to preserve it in a few places.

## Suggested Repair Order

1. Fix the Wave-1 dependency model first; this prevents ledger and Issue Doc corruption.
2. Correct the B-02 `M_tot` sentence and remove or pin `G'=1` in the Plummer snippets.
3. Add the missing `L_data` §3.1 rewrite and causal exponent clipping clauses.
4. Replace the brittle verification regexes with explicit structural assertions.
5. Tighten `19-04` so `VERIFIED` transitions only happen after executable checks pass.
