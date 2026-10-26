---
schema_version: phase64-verdict/v1
status: awaiting-owner
gate: not-run
evaluation: preserved-unspent
verdict: RETHINK-REPRESENTATION
representation_limit_qualifier: false
owner_decision: pending
owner_decision_date: pending
agent_recommendation: change-course
handoff_citation: .planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json
handoff_sha256: 7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5
numbers_sha256: 632e02b21d1ee132f844e5c9592578d5ce32bb31b9673ccb76dc84556511cafa
figure_sha256: d9754afaf0aefdf2c4b3f27dfc97b6cac06e4bac4adb63b5b5447efdd69a7695
charter_citation: .planning/phases/64-feasibility-verdict/64-CHARTER.md
ruling_citation: pending
ruling_sha256: pending
---

**Audience:** the project owner, a first-year student; no specialist background assumed.

**What this page rests on.** The sealed stop handoff, `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json`, SHA-256 `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5`. The number manifest, `evidence/numbers.json`, SHA-256 `632e02b21d1ee132f844e5c9592578d5ce32bb31b9673ccb76dc84556511cafa`. Every number below is taken from that manifest and re-derived by `evidence/verify_phase64_verdict.py`; none is typed by hand.

**Status.** `awaiting-owner`. The agent's recommendation is `change-course`. The owner's decision is recorded at checkpoint ①, below, and is still pending.

## In plain language

This page answers one question: can this project work? It reports what the experiments found, what the rule agreed in advance says about that, and what the owner is asked to decide. It trains nothing and it does not spend the held-out exam.

1. **The network did not reproduce any of the three orbits.** Each experiment is a *Rung*: one exam on the project's ladder. Rung 1 is the easiest, training the network on a real orbit together with the correct answer and then asking it to reproduce that same orbit. Three systems (1632, 851 and 4658) were each trained once, for 2.573 to 5.693 hours. All three ended at **Tier 0**. A *tier* is the scorecard's grade for a prediction, and Tier 1 is the lowest passing grade. Tier 1 needs **E**, the worst position error over the window as a fraction of the system's size, to be at most 0.1 (10%). The three runs ended with E of 1.1574, 1.2375 and 1.1432, about 11 to 12 times the Tier-1 line. The **valid horizon** is the fraction of the window before the error first exceeds 1% (or 10%); it was 0.0 at both limits on all three, meaning the prediction was outside both limits at the first scored time. **eps_h** is the largest relative energy drift along the predicted path: Tier 2 needs E at most 0.01 and eps_h at most 10⁻³; Tier 3 needs E at most 0.01 and eps_h at most 10⁻⁵.
2. **Gate G2 fired, and the pre-agreed sweep rescued nothing.** *Gate G2* is the stop rule agreed before any result: it fires when two or more of the three systems end below Tier 1, and all three did. The *settings sweep* is the one rescue the rule allows: four other values of the network's first-layer frequency setting, `first_omega_0` (60, 120, 240 and 480), on one failing system, 1632, where the project had locked the value 30. All four also ended at Tier 0, with E between 1.1539 and 1.1575. A rescue needed one of them to reach Tier 1; none did, so nothing was confirmed on system 851 and the owner was not called to the checkpoint that asks whether to continue at a new setting.
3. **The frozen rule's output is RETHINK-REPRESENTATION.** Given only "G2 fired and the sweep rescued nothing", the decision rule frozen in Phase 59 returns that label. It is the rule's output, not a Phase 64 judgement, and this page does not amend it.
4. **The evidence beside the label.** The trained networks behave as *time-constant predictors*: each returns essentially each body's average position and nothing that moves, with E of 1.1538, 1.2337 and 1.1396 on the three systems on the CPU in double precision (re-derived (CPU float64)), and an output that moves by only 0.0030 to 0.0034 of the real orbit's own variation about its mean. Their accuracy curves levelled off early: E fell by a factor of 25 to 48 in the first 5% of training (the decision context rounds this to 25- to 50-fold), then settled at 1.14 to 1.24, about 11 to 12 times the Tier-1 limit. Two comparison points frame the result: the *two-Kepler formula*, a no-learning baseline that places each body on the two-body orbit implied by its initial state, and the *nearest-neighbour copy*, which repeats the closest training orbit instead of predicting. Both are scored in the same physical units in `## Comparison points`.
5. **What was not run is not called failed.** Rung 2, which would ask whether the network can learn an orbit from the physics alone, is recorded with the reason "no rescue"; the two hard-stage probes are recorded the same way; Phases 61 to 63 are "skipped at G2, not failed"; Level 3 of the readiness ladder is "not tested (skipped at G2)"; and the control has no readout branch because Phase 63 was skipped at G2.
6. **What it cost.** 22.378 hours of arm wall time: 11.108 hours for Rung 1 and 11.270 hours for the sweep. One single-orbit experiment costs 2.573 to 3.046 hours for an unextended arm and 5.693 hours for the arm that earned its doubling. All computation runs on this Mac (standing owner rule, `PROJECT.md` Constraints, reaffirmed 2026-10-25).

The rule and the evidence sit side by side. Neither column is softened, and neither is allowed to overwrite the other.

| What the pre-registered rule says | What the evidence shows |
|---|---|
| **RETHINK-REPRESENTATION**, for "G2 fired and the sweep rescued nothing". The label is quoted exactly as the sealed handoff records it; it is not amended, softened or relabelled. | Every trained network learned only each body's average position: it is a time-constant predictor, with E of 1.1538, 1.2337 and 1.1396 on the three systems (re-derived (CPU float64)). Its accuracy curves levelled off early: E fell by a factor of 25 to 48 in the first 5% of training (about 25- to 50-fold as the decision context puts it), then settled at 1.14 to 1.24, about 11 to 12 times the Tier-1 limit. The sweep varied only `first_omega_0`; each arm's step budget followed its own measured speed under the pre-registered rule (the Budget row of `60-RUN-PROTOCOL.md`), 842,770 to 994,807 steps across the four sweep arms, so `first_omega_0` was the only setting chosen. The records cannot yet tell a design limit from a limit of the fixed training recipe. |

At checkpoint ① the owner is asked one question: continue on this path, change course (the agent's recommendation), or stop. If the project continues, the next milestone is v2.5, committed only to its name and its first phase, the trainex-r5 research round.

The cost of reaching the next level cannot be estimated from this evidence; `### Cost to the next level` under `## Cost on this Mac` states why, and what would measure it (GAP-64-03).

## The result under the pre-registered rule

The sealed handoff records the frozen rule's output as a small dictionary. Quoted exactly as recorded:

| Field | Recorded value |
|---|---|
| `verdict` | `RETHINK-REPRESENTATION` |
| `reason` | `G2 fired and the sweep rescued nothing` |
| `qualifier` | `false` |

The rule was given only those inputs. Re-running the frozen `decision_verdict` on the committed inputs returns the same dictionary — the `inputs` mode prints INPUTS-OK — so the label is reproducible from the sealed files rather than recalled from memory. Nothing pre-registered changes and the label is not amended; amending it after seeing the result would need a formal amendment with the owner's sign-off (SCOPE-42, SCOPE-43).

**The qualifier field, plainly.** `representation_limit_qualifier` is reported exactly as recorded: `false`. Here `false` means "not evaluated on this branch", not "the condition failed": the frozen rule returns `false` on the G2 path without evaluating the qualifier, and it refuses a Rung 1 comparison input on that path. The amendment's text applies the qualifier whatever the branch, so the two do not conflict in substance. On the committed numbers the qualifier's condition holds anyway: Rung 1 is Tier 0 on all three systems, and its E is below the two-Kepler formula's only on system 4658, 1 of 3. This page does not recompute or change the field.
