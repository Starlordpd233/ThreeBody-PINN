---
status: archived
purpose: other
created: 2026-06-05
milestone: v1.4
phase: 20-review-remediation
retirement_trigger: milestone complete; superseded by subsequent work
---

Verdict: The remediation is directionally sound and unusually governance-aware — its STOP-protocol fidelity is its strongest feature. But it is not safe to execute verbatim: roughly six of its concrete edit/verify instructions are mis-anchored or self-contradicting against the real files, so a literal executor will either fail to find the anchor or fail its own verification gate. It also under-claims its coverage — the Self-Review Checklist asserts "every high-risk review finding has a task," which is false.

---
P1 — Will mis-execute as written (fix before running)

1. The verification gate forbids a string the remediation itself injects (partial AC).
Task 4 Step 7's replacement text ends with "Do not invent a partial AC status or a new ledger status" (plan line 329). But Task 4 Step 9 (line 347) and Task 7 Step 1 (line 473) both run ! rg -n "…|partial AC|HALF" 20-04-PLAN.md. After Step 7 lands, rg "partial AC" matches → ! inverts → the verification fails on a correctly-applied plan. The original 20-04 (line 228) contains no "partial AC". Fix: tighten the guard to the invented artifact, e.g. partial AC status: as a status token, or drop partial AC from the negative grep and rely on HALF.

2. The new I₃ negative-audit regex is vacuous (false-negative).
Task 3 Step 4 replaces 20-03 Task 3 Step 2 with rg -n "I_3.*raw.*\[-1, ?1\]|raw.*I_3.*\[-1, ?1\]|I_3.*formula.*\[-1, ?1\]". The actual offending line is I_3 = (d_short + d_mid - d_long) / (…) ∈ [-1, 1] (20-03 line 163) — it contains neither the literal word "raw" nor "formula", and the legit mapped-range prose (…mapped to $[-1,1]$ via $I_3^{\mathrm{in}}=6I_3-1$) doesn't either. So the regex matches nothing in either the defective or the corrected state — the AC-ARCH-03 negative audit becomes a no-op that always "passes." The intent (don't flag the mapped range) is right; the implementation guts the safety check. Fix: anchor on the assignment form, e.g. rg "I_3 *=.*\[-1, ?1\]", or exclude the superscript: rg "I_3[^^]*\[-1, ?1\]".

3. The new formula-change guard false-positives on the plan's own prose.
Task 4 Step 5 replaces the (admittedly broken) … | rg "tanh|E_scale" || true with git diff -- ctl_instruction.md | rg -n "^[+-].*(tanh|E_scale|mu|sigma|m_i)", Expected "no formula-line additions or removals." But Task 4 Step 4 adds prose containing tanh((m_i - mu)/(sigma+1e-8)) to that same file. The added + line matches the guard, so the gate flags the plan's own sanctioned prose. The Expected note hand-waves ("explanatory prose may mention formulas") but the command can't tell prose from formula. Fix: restrict to the actual normalization definition lines (e.g. grep for the table row or a code-fence marker), or assert the formula tokens are unchanged via git diff … | rg "^-.*tanh" (removals only).

4. 20-01 B-01/B-10 "split" misreads the real structure and would degrade it.
Task 5 Step 2 says "If Step 1 still bundles both packet bodies, split it into Step 1a/1b." In the real 20-01, B-01 is Steps 1–5 and B-10 is Step 6 — they're already separate steps, so the conditional never fires and R4's actual goal (HIGH-03: separate tasks for parallel dispatch) is unmet. If forced, the header-only Step 1a/1b collides with the existing Steps 2–6 (which already fill B-01's body and all of B-10), producing incoherent ordering. The instruction also conflates step-split (no parallelism) with the task-split the finding wanted. Fix: if the goal is parallel dispatch, split into Task 1a/Task 1b; otherwise drop the split and keep only the severity-rationale hardening (the real value buried here).

5. 20-04's contains: "realized" artifact check contradicts the remediation's own D-09.
20-04 frontmatter (line 28) verifies ctl_instruction.md contains: "realized". The remediation promotes D-09 to canonical ("realized support" is not spec vocabulary) and 20-04 Task 2 PRECONDITION already forbids putting "realized" in the spec. So a correctly-executed 20-04 (no "realized" in the spec) fails its own artifact gate — and making D-09 canonical turns this latent contradiction into an active one. The remediation never touches the frontmatter. Fix: change the artifact contains: to a plain-language token actually used in the prose (e.g. dataset-occupied or asymmetry carries), and reconcile the D-06 truth on line 21 that still says "framed as realized support."

6. Mis-anchored mass-range edit (Task 4 Step 3).
Step 3 says "In Task 1 Step 3, replace the Before/After sentence that includes approximately [-0.93, 0.585]." But 20-04 Task 1 Step 3 (line 135) has no numeric — [-0.93, 0.585] exists only in Task 2 Step 2 (line 183), which Step 4 already handles. A literal executor finds nothing to replace. Fix: re-point Step 3 at the asymmetry sentence in Task 1 Step 3 (no numeric), and let Step 4 own the numeric removal.

7. Coverage gap that falsifies the Self-Review Checklist.
Finding #24 (R5 H-003, HIGH) — 20-02 Task 3 Step 4 re-runs 20-01's exact omega scheduler rg pattern, so a false-negative in one is a false-negative in both — is not addressed. Yet the Self-Review Checklist (plan line 523) claims "every high-risk review finding has a task." Fix: add an orthogonal cross-check (broad schedul sweep + manual inspect) in 20-02, or down-scope the checklist claim.

---
P2 — Coherence drift and partial fixes

- Wave relabel leaves stale references. Task 4 Step 1 sets 20-04 wave: 3, but 20-03 line 44 still says "plan 20-04 … edits the same file in wave 2" and 20-04 line 51 prose says "after 20-02 and 20-03." Neither is updated → new contradiction.
- D-09 duplicates an already-grounded decision. Its content is verbatim the D-06 "Vocabulary clarification (user decision 2026-06-03)" block (20-CONTEXT lines 87–90). The new D-09 cites 20-DISCUSSION-LOG rather than the stronger D-06 grounding, and creates two canonical statements of the same rule. Fix: make D-09 a one-line pointer to D-06, or note the consolidation.
- 20-03 accept-resolution prose left in place + verify ambiguity. The remediation strengthens the fallback (good) but does not remove the pre-written ∈ [0, 1/3] / 6 I_3 − 1 prose in 20-03 Task 2 Steps 1–2 (Finding #14, R5 H-006 HIGH). Worse, Task 3 Step 6's verify says matches are "allowed only inside Task 1's accept-resolution example" — but those tokens also live in Task 2, so the check is ambiguous as written.
- 20-04 negative-audit (Task 3 Step 2) untouched. Finding #28 (pattern misses "incorrect/problem/flawed") isn't fixed — the remediation only rewrites Task 3 Step 1 (the positive audit).
- Phase-exit only half-resolved. The execution_coordination text addresses milestone-level completion, but Finding #20's real question — can Phase 20 "exit" / Phase 21 ("Depends on Phase 20") start with ARCH-04 blocked? — is not answered.
- Final commit omits the gap files. Task 7 Step 3 stages only the 7 plan files, but the Global STOP rules and Task 6 may write 20-GAPS.md / v1.4-GAPS.md; those changes would be left uncommitted.
- D-02 identifier collision (Finding #17, MEDIUM×2) not addressed — 20-CONTEXT D-02 (SIREN) vs issue-doc D-02 (I_norm) remains a latent naming hazard referenced across plans.

---
FYI / governance notes

- D-11 resolves a CRITICAL by assertion. The canonical D-11 the plan writes adds a "mechanical grounding gate" that is not in the cited 20-DISCswers R5's C-003 ("autonomous: true rests on a semantic judgment") by declaring the test mechanical. This is defensible (the test "does M10 citea v1.4-formula-grounded range? yes→use / no→qualitative-or-STOP" is fairly mechanical), but it's a judgment overriding a CRITICAL finding and ts its grounding. Worth a conscious user sign-off.
- 20-GAPS.md line 9 literally cites AGENTS.md (Finding #36) and last_updated: 2026-06-03 is stale (#35); both are out of the remediation's stated scope and left unfixed.
- M8 severity rationale asserts "Issue-doc M8 is MAJOR" as fact (Task 5 Step 5) — better phrased conditionally ("if the issue doc/ledger rates M8 MAJOR…"), though the embedded "keep or escalate if not source-grounded" self-check mitigates it.
- Unaddressed minors: #22 (SI-PINN-002 section-anchor), #25 (old_string exactness), #26 (lemma I₃=0 edge case), #29 (skill mismatch), #30 (E_sc in log), #44 (D-01 citation in 20-03/04).

What the remediation gets right (keep)

Strong STOP-protocol fidelity (refuses to invent the M5 verdict, the mass range, or an ARCH-04 vehicle; routes semantic gaps to both gap registers + user); correct do-not-modify scope (framework specs, evidence packets, 16-ISSUE-LEDGER, pinn/, Phase 20.5); the mass-range fix correctly diagnoses the v1.3-vs-v1.4 tanh formula root cause and defaults to qualitative wording (siding with R3/R5 over the lenient R1); ledger serialization by execution rule rather than by redefining evidence semantics; ARCH-04 block + 20-05 re-audit-after-20-03/04 preserved; the "stricter safe rule" meta-policy is governance-aligned.

---
The biggest theme: the remediation correctly diagnoses the report findings but several of its fixes recreate the defect class they target (vacurify gate that forbids its own output). I'd treat the seven P1 items as blocking before anyone executes this remediation.