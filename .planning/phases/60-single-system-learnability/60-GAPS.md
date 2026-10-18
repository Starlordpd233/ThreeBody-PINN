# Phase 60 Gap Register

Phase-local register under the STOP protocol, as applied to v2.4. Under that
rule (ROADMAP "Delegation and gaps"), a source-silent decision is recorded with
every field and may be resolved under the owner's delegation (2026-10-07,
re-confirmed 2026-10-09) **unless** it would move a locked value, spend the
evaluation or pre-empt the verdict. Those go to the owner. Milestone index:
`.planning/milestones/v2.4-GAPS.md`.

Every gap below surfaced during Phase-60 planning, in `60-RESEARCH.md`
(2026-10-18: Finding A and Open Questions OQ-1..OQ-12). Each was recorded
before any Phase-60 code ran, and all thirteen are resolved under the
delegation. **GAP-60-09 resolves only the procedure.** If a G2 confirmation run
ends below Tier 1, the phase stops and the owner decides what that means.

## In plain language

| Gap | What it decides | Outcome |
|---|---|---|
| 01 | How the amendment check compares text, and where the checkpoint ④ paragraph goes | Whitespace-only comparison, with the files edited to match. The paragraph goes in Owner Checkpoint 4 |
| 02 | How Phase 59's checker keeps passing after the scorer fix | One allowed new scorer hash, a re-check of the baselines on a copy, and a refreshed file index |
| 03 | Whether harness arms clip large gradient steps | Yes: every arm, with the trainer's own clipper, during Adam only |
| 04 | How the speed-measuring run before each arm works | 500 steps for data-only arms and 50 for physics arms, all timed, with nothing else running |
| 05 | When the L-BFGS polish counts as "improving", and which state it hands back | The polish's own objective decides, and the last iterate is the polish state |
| 06 | What happens if training blows up (NaN) | Adam stops at the last good state, which is scored and polished. No restart |
| 07 | Which states get the CPU double-precision cross-check | Both scored states of every real arm |
| 08 | How the weights are saved so git keeps them | One `.weights` file per state, with its hash in the record |
| 09 | **What it means if the G2 confirmation run fails** | **The phase stops and the owner decides. Nothing is assumed** |
| 10 | Which reference scale the probes use after an owner continue | The one re-measured at the approved setting |
| 11 | Whether the owner may approve a setting not on the sweep grid | Yes. The record says whether it was swept |
| 12 | The energy-term scale for the two probe physics arms | The value the trainer computed once and saved |
| 13 | The input-scaling statistics for the probes | The same Stage-0 statistics every arm uses |

---

## GAP-60-01: the amendment check's text comparison and the checkpoint ④ paragraph's home

- **Decision point.** SPEC Requirement 1 says the six amendment paragraphs
  must match `REQUIREMENTS.md` and `ROADMAP.md` "after collapsing whitespace".
  Two things are open:
  - whether the comparison ignores markdown emphasis;
  - which section holds the "Checkpoint ④ continue" paragraph.
- **Where in artifact.**
  - `60-SPEC.md`: Requirement 1 and `## Amendment text`.
  - `.planning/REQUIREMENTS.md`: the SCOPE-39 row (:319), FEAS-09
    (:187-195), the SCOPE-44 row (:324) and Owner Checkpoint 4 (:337-340).
  - Found by the orchestrator's containment script and `60-RESEARCH.md`
    Finding A.
- **Task context.** Planning SPEC Requirement 1. The spec commit `e74e44d3`
  already applied most of the amendment.
- **Classification.** Operational coordination.
- **Source silence.**
  - The SPEC's edge row (encoding/R3) says "exact after collapsing whitespace"
    and says nothing about markdown.
  - Five of the six paragraph labels name a target: the SCOPE-39 row, FEAS-04,
    roadmap success criterion 3, FEAS-09 and the SCOPE-44 row. "Checkpoint ④
    continue" names none.
- **Grounding.**
  - **Today's state:**
    - SCOPE-39 matches only if the two `**` markers in its table cell are
      dropped.
    - FEAS-04 and roadmap criterion 3 match exactly.
    - FEAS-09 has 1 of 3 sentences verbatim.
    - SCOPE-44 has 0 of 1: its condition is a clause inside a longer
      sentence.
    - Checkpoint ④ continue has 1 of 3. The rest of its content is spread and
      reworded across the FEAS-03 rescue bullet, Owner Checkpoint 4 and the
      exits table.
  - Stripping markdown would also strip the backticks inside the checkpoint
    paragraph itself, so a looser rule would weaken the check.
  - The roadmap sentence appears twice in `ROADMAP.md`, at the end of the Gate
    G2 paragraph and in success criterion 3. Containment must therefore be
    checked inside each paragraph's own section, not by counting matches in
    the file.
- **Agent was tempted to.** Strip markdown on both sides so the current text
  passes. Rejected, because it weakens the SPEC's exactness rule.
- **Options.**
  - A: collapse whitespace (after NFC) only, and edit the files so that each
    paragraph appears verbatim in its section.
  - B: also ignore `**` and backticks.
  - C: accept the near-matches as they stand.
- **Confidence of impact.** LOW. Only wording changes; no number moves.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - **Comparison:** `" ".join(unicodedata.normalize("NFC", text).split())` on
    both sides, inside the paragraph's designated section.
  - **Edits:**
    - Delete the two `**` markers in the SCOPE-39 cell.
    - Make the FEAS-09 body contain its three sentences as one contiguous run.
    - Add the stand-alone SCOPE-44 sentence.
    - Insert the three "Checkpoint ④ continue" sentences, contiguous, in Owner
      Checkpoint 4.
    - Keep the existing explanatory sentences.
  - **Test:** a committed test parses the paragraphs from `60-SPEC.md` itself.
    It also proves that the scorecard SHA-256 is unchanged (`f4b17688…444b`).
  - **Ordering:** the amendment commit comes before any real-arm record.

## GAP-60-02: keeping Phase 59's checker green after the scorer fix

- **Decision point.** D-09 allows exactly one successor SHA-256 for
  `feasibility_scorer.py`. That alone does not keep Phase 59 verifiable,
  because two more checks break.
- **Where in artifact.**
  - `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py`:
    `_check_result` (:434-440), `_rederive`, and `cmd_final` (:911-943).
  - `pinn/verification/baselines.py`: `PRODUCER_MODULES` (:82-91) and the
    `--check` byte comparison (:666-681).
  - `evidence/manifest.json`.
- **Task context.** Planning the D-09 verifier change (`60-RESEARCH.md`
  Finding F).
- **Classification.** Operational coordination.
- **Source silence.** D-09 (`60-CONTEXT.md`) names only the successor hash. It
  mentions neither of the two checks that break:
  - **The baselines re-derivation.** It re-renders payloads that embed the
    live scorer digest, then byte-compares them with the committed files.
  - **`manifest.json`.** It hashes the verifier file itself.
- **Grounding.**
  - **What fails after the edit:**
    - `baselines --check` prints `BASELINES-CHECK-DIFF`, purely because the
      embedded digest changed.
    - The all-area manifest check fails with "changed file
      verify_phase59_evidence.py".
  - Editing `baselines.py` to avoid the first failure would change its own
    pinned digest. That is a second successor, which D-09 forbids.
  - A same-length digest substitution in a temporary copy of the committed
    `baselines/` files leaves every other byte identical. Re-deriving against
    that copy therefore still tests that the baselines reproduce under the new
    scorer.
- **Agent was tempted to.** Skip the baselines re-derivation inside `final`.
  Rejected, because it would stop checking that the baselines reproduce.
- **Options.**
  - A: re-derive `baselines --check` against a temporary copy in which the old
    digest is replaced by the successor. Rewrite the manifest after the
    verifier edit, and re-run `final` detached.
  - B: skip the baselines re-derivation, with a documented exception.
  - C: edit `baselines.py`, which makes a second successor.
- **Confidence of impact.** MEDIUM. Without a fix, Phase 59's `final` check
  stays red at HEAD.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - **The successor record:** `evidence/scorer-successor.json`, tracked and
    clean. It names one path, its predecessor digest `cd5019a2…870b` and its
    successor digest.
  - **The verifier:**
    - `_check_result` accepts that one pair only. Every other producer digest
      is checked as before.
    - A record that names a second path or a second successor is refused.
    - `_rederive("baselines")` runs
      `python -B -m pinn.verification.baselines --check --evidence-root <temporary copy>`.
  - **The manifest** is rewritten with `manifest --area all --write`. The
    executor diffs it and confirms that only the verifier's entry and
    `produced_at_head` changed.
  - **If the substituted re-derivation still differs,** the fix changed CPU
    float64 numbers. Stop and report. Never fall back to option B.
  - **Running `final`:** `verify_phase59_evidence.py final` (about 644 s) runs
    detached, with its output retained, and never alongside a timing run or
    an arm.
  - Phase 59's evidence is not re-run.

## GAP-60-03: gradient clipping in harness arms

- **Decision point.** Whether harness arms clip the gradient on each Adam
  step, and at which stage multiplier.
- **Where in artifact.**
  - The harness Adam step, in modules not yet written.
  - `pinn/training/grad_clip.py`: `GradClipper` and `DEFAULT_C_STAGE_TABLE`
    (:89-97).
  - `pinn/training/controllers.py:2092`.
- **Task context.** Planning the harness Adam loop (`60-RESEARCH.md` OQ-3).
- **Classification.** Semantic.
- **Source silence.**
  - D-01 lists the learning rate, the cosine, the Adam constants and the
    warmup, but not clipping.
  - The Phase 38 probe did not clip.
  - The SPEC is silent.
- **Grounding.**
  - **The ratified recipe includes clipping in the Adam step:**
    - `ctl_instruction.md:1782`, step 4: "Adam-only median-based global
      gradient clip".
    - `pinn_architecture.md` §4.4 (:775): "The merged clipping mechanism is
      **locked**: during Adam epochs only, …".
    - No clipping during L-BFGS (`ctl_instruction.md:1786`).
  - **The multiplier:**
    - The Stage 0–1 multiplier `C_stage` has the locked range 7–10 (the
      `ctl_instruction.md` `C_stage` table).
    - The trainer uses 8.5, the provisional midpoint, and generation 7 ran
      with it.
    - Stages 4–6 use 3.0.
  - **Physics arms:** SCOPE-41 and D-01 forbid them from changing the ratified
    recipe, so they must clip.
  - **Data-only arms:** these are not a recipe run. D-04, however, already
    gave them Rung 2's Stage-0 schedule, so that a data-only failure is not an
    artifact of different optimizer settings. The same reasoning applies to
    clipping.
  - The median clip binds only on a step whose norm exceeds `C_stage` times
    the recent median norm.
- **Agent was tempted to.** Leave data-only arms unclipped, as the Phase 38
  probe did, as the "purest" ceiling.
- **Options.**
  - A: clip every Adam step in every arm with the trainer's `GradClipper`, at
    the arm's stage: 0 for data-only and Stage-0 arms, 4 and 6 for probe Rung
    2b.
  - B: clip physics arms only.
  - C: no clipping.
- **Confidence of impact.** MEDIUM. Clipping touches every Rung-1 arm and
  therefore Gate G2, although a median clip rarely binds in smooth training.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
  Reported to the owner, who can veto it before the run protocol is committed.
- **Resolution note.**
  - Use `GradClipper` with the trainer's table (stage 0: 8.5; stages 4 and 6:
    3.0) and median floor `1e-6`.
  - Clip during Adam only.
  - Record the stage, the multiplier and the arm's count of clipped steps.
  - Checkpoint the clipper state for resume.
  - A non-finite clip outcome is GAP-60-06's divergence case.

## GAP-60-04: the timing run

- **Decision point.** How many steps the pre-arm timing run takes, what it
  times, and how it is kept from disturbing the arm.
- **Where in artifact.**
  - The run protocol and the launcher.
  - `feasibility_scorecard.steps_budget` (:779-799; `timing_steps >= 50`).
- **Task context.** Planning D-02 (the budget comes from the timing run) and
  the run protocol (`60-RESEARCH.md` OQ-9).
- **Classification.** Process-artifact schema.
- **Source silence.**
  - The scorecard fixes only a 50-step minimum (`timing_run_min_steps`).
  - CONTEXT says "at least 50 steps of the exact arm configuration,
    immediately before the arm", with the weights discarded.
- **Grounding.**
  - The budget is `floor(3 h ÷ (wall ÷ steps))`. Anything that inflates the
    measured seconds per step therefore shrinks the experiment.
  - MPS has a first-step overhead. On a data-only step of tens of
    milliseconds, that overhead could dominate a 50-step run.
  - A physics step takes about 12 s (generation 7: 12.2–12.9 s per step), so
    50 physics steps already take about 10 minutes.
- **Agent was tempted to.** Exclude the first steps from the timing.
- **Options.**
  - A: 500 steps for data-only arms and 50 for physics arms, with every step
    timed, warm-up included.
  - B: 50 steps everywhere.
  - C: time only the steps after a warm-up.
- **Confidence of impact.** LOW. It sets each arm's step count, not any
  threshold.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - **Configuration:** every timing run uses the exact arm configuration (the
    same record, loss arm, `first_omega_0`, stage, batch, chunking and
    clipper). It runs immediately before its arm and times all its steps.
  - **Fresh start:** the arm then starts from its own seed-42 initialization
    and RNG streams, unaffected by the timing run.
  - **Isolation:** no other heavy job runs during a timing run or an arm.
  - **One per arm:** every arm has its own timing run, including each sweep
    setting, the confirmation and each probe arm. D-02 sizes the budget from
    "that arm's timing-run seconds per step".
  - **What is kept:** the timing weights are discarded and not committed. The
    timing wall time and step count go in the arm record.

## GAP-60-05: what the polish's "improvement" means and which state it returns

- **Decision point.** The frozen polish stops "after 5 outer calls without
  improvement" or at 25% of Adam's wall time. Three things are undefined:
  - what "improvement" is measured on;
  - which iterate is "the polish state";
  - exactly which time counts as Adam's.
- **Where in artifact.**
  - `feasibility_scorecard_v1.json`, `lbfgs_polish` (:398-409).
  - `feasibility_scorecard.polish_should_stop` (:868-888) and `better_state`
    (:894-906).
- **Task context.** Planning the polish loop (`60-RESEARCH.md` OQ-4).
- **Classification.** Semantic.
- **Source silence.** None of the scorecard, `polish_should_stop` or the SPEC
  defines improvement or the polish state. SPEC Requirement 8 says only
  "Adam's running time is the sum across segments, not calendar time that
  includes the interruption".
- **Grounding.**
  - Using the scored position error `E` to stop the polish, or to pick a best
    iterate, would feed the graded answer into a training decision.
  - For physics arms, that would contaminate Rung 2's "learns from the
    physics" reading.
  - L-BFGS minimizes its own objective, so the objective is the natural
    measure of progress.
- **Agent was tempted to.** Keep the best-scoring iterate.
- **Options.**
  - **Improvement:**
    - A: the full-batch objective returned by the closure, strictly below the
      best so far. The starting value is the objective at the Adam result.
    - B: the scored `E`.
  - **Polish state:** the final iterate, or the best iterate.
  - **Adam time:** the whole Adam phase (steps plus readings) summed across
    segments without interruptions, or the step time only.
- **Confidence of impact.** LOW to MEDIUM. It changes when the polish stops.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; improvement
  A, final iterate, whole Adam phase).
- **Resolution note.**
  - **One outer call** is one `LBFGS.step(closure)` with the frozen
    `max_iter` 50, history 10 and strong Wolfe.
  - **After each outer call:**
    - Compare its objective with the best so far. A strictly lower value
      resets the counter; otherwise the counter goes up.
    - Then call `polish_should_stop`.
  - **The polish state** is the iterate after the last outer call.
  - **Non-finite values:** if an outer call returns a non-finite objective or
    leaves non-finite parameters, the polish stops. The polish state is then
    the parameters from before that call.
  - **`E`** may be logged at each outer call for the trace, but it never
    steers the polish.
  - **Physics arms** freeze the collocation rows, causal weights and loss
    weights at the handoff (`57-RULING.md:112-124`).

## GAP-60-06: divergence

- **Decision point.** What an arm does if its loss or gradient becomes
  non-finite during Adam.
- **Where in artifact.** The harness Adam step. Compare
  `controllers.py:2131-2162`, where the trainer skips the step and returns
  RECOVER.
- **Task context.** Planning the Adam loop (`60-RESEARCH.md` OQ-6 and
  Pitfall 16).
- **Classification.** Semantic.
- **Source silence.**
  - The SPEC forbids a silent restart and makes the first completed run the
    result.
  - The scorecard's budget rule covers complete, extend and inconclusive. It
    does not cover divergence.
  - The trainer's recovery path is not part of the harness. CONTEXT says the
    harness does not enter the production loop.
- **Grounding.**
  - SIREN networks at a high `first_omega_0` can be unstable, and 480 is on
    the sweep grid, so the case is plausible.
  - Stepping on a non-finite gradient turns the parameters into NaN and loses
    the last good state.
  - A stop-for-owner rule would stall the sweep on an expected outcome.
- **Agent was tempted to.** Mark a diverged arm Tier 0 without scoring it.
- **Options.**
  - A: stop Adam at the last finite state and score it as the Adam state. Run
    the polish if its weights are finite, and let `better_state` choose.
  - B: Tier 0, unscored.
  - C: stop for the owner.
- **Confidence of impact.** MEDIUM. A diverged sweep arm decides that
  setting's tier.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - Check the loss and the clip outcome before `optimizer.step()`, as the
    trainer does.
  - On a non-finite value, skip that step and end the Adam phase. Record
    `diverged_at_step` and the budget outcome `diverged`.
  - `budget_outcome` is not called for a diverged arm, because no reading
    exists at the budget step. No reading is invented.
  - The arm's result enters G2 at its tier, like any other arm.
  - There is no restart.

## GAP-60-07: scope of the CPU float64 cross-check

- **Decision point.** Which scored states get the CPU float64 re-score that
  SPEC Requirement 3 requires.
- **Where in artifact.** SPEC Requirement 3 and the harness scoring step.
- **Task context.** Planning SPEC Requirement 3 (`60-RESEARCH.md` OQ-11).
- **Classification.** Operational coordination.
- **Source silence.** SPEC Requirement 3 requires the cross-check "beside the
  official score", and a stop when the tier or the counts boolean differs. It
  does not say whether interim cadence readings are included.
- **Grounding.** Only the two scored states, Adam and polish, enter
  `better_state`, the tier and `counts`. Cadence readings feed only the budget
  rule.
- **Agent was tempted to.** Cross-check only the better state.
- **Options.**
  - A: both scored states of every real arm.
  - B: the better state only.
  - C: every reading.
- **Confidence of impact.** LOW.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - Cross-check both scored states of every real arm.
  - Any difference in tier or in the counts boolean raises a dedicated
    owner-routed stop. The harness never takes the better of the two scores
    (SPEC prohibition).
  - Cadence readings are MPS-only.

## GAP-60-08: the weights file format

- **Decision point.** How each scored state's weights are written so that
  plain git keeps them (D-10).
- **Where in artifact.**
  - `.gitignore:146-158` ignores `*.pt`, `*.pth`, `*.npz`, `*.npy`, `*.ckpt`
    and `*.pkl`.
  - `scripts/git_policy/validate_staged_paths.py:9-27` blocks `runs/`,
    `tmp/`, `outputs/` and `scratch/`, and refuses blobs over 10 MiB.
- **Task context.** Planning D-10 (`60-RESEARCH.md` OQ-10 and Pitfall 7).
- **Classification.** Operational coordination.
- **Source silence.** D-10 says plain git, not LFS. It does not give the
  format or the path.
- **Grounding.**
  - Force-added ignored files are what milestone archival drops (v2.3 memory
    note).
  - The network has 795,657 parameters, so a float32 state is about
    3.04 MiB, under the 10 MiB limit.
  - D-10's planning figures assumed about 2.8 MiB per state. The corrected
    totals are about 49 MiB on the stop path (8 arms) and about 115 MiB on
    the full continue path (19 arms).
- **Agent was tempted to.** Force-add `.pt` files.
- **Options.**
  - A: `adam.weights` and `polish.weights` (`torch.save` of a CPU float32
    state dict) under `evidence/arms/<arm-id>/`.
  - B: force-add `.pt` files.
- **Confidence of impact.** LOW.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - Each record carries the file's SHA-256 and a canonical per-tensor digest
    (name, dtype, shape and bytes, in sorted-name order).
  - Loads use `torch.load(..., weights_only=True)`.
  - Resume checkpoints and timing weights stay under the ignored `runs/` tree.

## GAP-60-09: a G2 confirmation run that ends below Tier 1

- **Decision point.** What it means when the confirmation run ends below
  Tier 1 on the confirmation system. The confirmation run uses the highest
  sweep setting that reached Tier 1.
- **Where in artifact.**
  - SPEC Requirement 6.
  - `REQUIREMENTS.md` FEAS-03 (:124-126).
  - `feasibility_scorecard.decision_verdict` (:718-776).
- **Task context.** Planning the G2 sweep (`60-RESEARCH.md` OQ-5).
- **Classification.** Semantic. Its substance could pre-empt the verdict.
- **Source silence.**
  - FEAS-03 says the sweep runs "on one failing system, and a configuration
    that reaches Tier 1 there is confirmed on a second failing system". It
    then lists only "no rescue" and "rescue".
  - SPEC Requirement 6 says "a confirmed rescue raises the frozen
    `OwnerRouted`" and "zero Tier ≥ 1 settings means no confirmation and no
    rescue".
  - None of these says what a failed confirmation means. `decision_verdict`
    raises only for `sweep_rescued=True`.
- **Grounding.** Either reading decides the verdict's path, which the
  delegation does not cover:
  - Calling it "no rescue" sends the milestone to RETHINK-REPRESENTATION and
    skips Phases 61–63.
  - Calling it a rescue puts a setting that failed on a second system in
    front of the owner.
- **Agent was tempted to.** Read it as "no rescue", because the confirmation
  is part of the rescue's definition.
- **Options.**
  - A: no rescue (the RETHINK-REPRESENTATION path).
  - B: rescue (checkpoint ④).
  - C: stop and let the owner decide if it happens (Owner Checkpoint ③,
    SCOPE-42).
- **Confidence of impact.** HIGH if it occurs. It needs three things: G2
  fires, a sweep setting reaches Tier 1, and the confirmation fails.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation), for the
  procedure only (option C), because the procedure decides nothing.
  - The meaning is OWNER-ROUTED if the case occurs.
  - The owner may pre-answer A or B before the run protocol is committed.
- **Resolution note.**
  - The run protocol pre-registers the stop.
  - On a failed confirmation, the harness writes the sweep curve and the
    confirmation record and raises an owner-routed stop. It then runs or
    skips nothing further.
  - `decision_verdict` is not called until the owner answers.

## GAP-60-10: which `R_ref` the probe physics arms use after an owner continue

- **Decision point.** D-08 says probe physics arms "reuse the committed
  Stage-0 `R_ref`". After an owner continue at a `first_omega_0` other than
  30, does that mean the committed ω = 30 value, or the value D-07 re-measures
  at the approved setting?
- **Where in artifact.**
  - `60-CONTEXT.md`: D-07 and D-08.
  - `pinn_architecture.md:454`: the invalidation list.
  - `pinn/verification/artifacts/r_ref_stage0.json`.
- **Task context.** Planning the continue branch (`60-RESEARCH.md` OQ-2).
- **Classification.** Semantic.
- **Source silence.** D-08 was written for the probes against the ω = 30
  reference. It does not address a continue at another setting.
- **Grounding.**
  - The ratified rule says to re-measure `R_ref` and re-run GATE-04 "after
    any change to `first_omega_0`" (`pinn_architecture.md:454`). D-07 applies
    that rule before any physics arm on a continue.
  - D-08's own reason for reuse is that "none of the invalidation triggers …
    change" for the probes. That holds only relative to the reference measured
    at the arm's own setting.
  - Applying the ω = 30 value at another setting would use a reference that
    the ratified rule declares invalid.
- **Agent was tempted to.** Read D-08 literally, as the ω = 30 file.
- **Options.**
  - (i) The committed ω = 30 value in every case.
  - (ii) The Stage-0 reference in force: the committed ω = 30 value when the
    ladder runs at 30, and the D-07 re-measured value after a continue.
- **Confidence of impact.** MEDIUM. It scales the physics term in the two
  probe Rung-2b arms, which do not gate.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option ii).
- **Resolution note.**
  - Each probe record says "Stage-0 reference in force, applied unchanged",
    and names the artifact path and SHA-256.
  - The D-07 re-measure writes to a Phase 60 evidence path. It never
    overwrites `r_ref_stage0.json`.
  - The checkpoint ④ question says that a continue includes the re-measure and
    the GATE-04 re-run, and that a GATE-04 fail stops for the owner.

## GAP-60-11: an approved setting that is not on the sweep grid

- **Decision point.** Whether a continue-path arm may run at an
  owner-approved `first_omega_0` that the sweep did not run.
- **Where in artifact.** `60-CONTEXT.md` D-11 and the SPEC amendment
  "Checkpoint ④ continue".
- **Task context.** Planning the ruling-file loader (`60-RESEARCH.md` OQ-12).
- **Classification.** Semantic (low).
- **Source silence.** D-11 and the amendment say the ruling names "the
  approved `first_omega_0`". Neither restricts it to the grid.
- **Grounding.** The approval is the owner's decision under checkpoint ④. The
  harness's job is to refuse any value the ruling does not name.
- **Agent was tempted to.** Refuse values off the grid.
- **Options.**
  - A: accept any finite positive value the ruling names. Record whether it is
    on the grid and whether it equals the confirmed setting.
  - B: grid values only.
- **Confidence of impact.** LOW.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - D-07 runs at the named value.
  - Every continue-path record cites the ruling file's SHA-256 and states
    `on_grid` and `equals_confirmed`.

## GAP-60-12: the energy-term scale for the probe physics arms

- **Decision point.** Which `S_H` sets the energy floor `ε_H = 1e-4 · S_H` in
  the probe Rung-2b arms. At stages 4 and 6 the energy and angular-momentum
  weights are 1.0, so the term is active.
- **Where in artifact.**
  - `pinn_architecture.md:567-575`.
  - `pinn/constants.py:92-94`: `PHYS05_LAMBDA_E_MAX` and
    `PHYS05_LAMBDA_L_MAX`.
  - `runs/stage0-v23g7-seed42/training_metadata.json`.
- **Task context.** Planning probe Rung 2b (`60-RESEARCH.md` OQ-7).
- **Classification.** Semantic.
- **Source silence.** Neither the SPEC nor CONTEXT mentions `S_H`. Stage-0
  arms never evaluate the energy term, because its weight is 0 at stage 0.
- **Grounding.**
  - The spec computes `S_H` "once in float64 … over the training split" and
    persists it, together with `ε_H`, in the training metadata. It is not a
    per-stage value.
  - The persisted generation-7 values are `s_h = 22.321729071058996` and
    `eps_h = 0.0022321729071058997`.
- **Agent was tempted to.** Recompute `S_H` over the probes' own stages.
- **Options.**
  - A: reuse the persisted value.
  - B: recompute, which would create a number that no ratified rule owns.
- **Confidence of impact.** LOW. The probes do not gate.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.** Probe records state the `S_H` and `ε_H` values and
  their source file.

## GAP-60-13: the input-scaling statistics for the probes

- **Decision point.** Which IC13 normalizer the standard-variant probe
  systems use.
- **Where in artifact.**
  - `pinn/verification/production_reference.py`:
    `recover_normalizer_from_checkpoint`.
  - `59-GAPS.md`: GAP-59-06.
  - `evidence/audit/reader_acceptance.json:90`:
    `stats_sha256 77526e53…79f6`.
- **Task context.** Planning the probe arms (`60-RESEARCH.md` OQ-8).
- **Classification.** Semantic (low).
- **Source silence.** The SPEC and CONTEXT name the probe records but not
  their normalizer.
- **Grounding.**
  - IC13 uses one dataset-wide normalizer, under the IC13 contract.
  - The trainer's statistics are recovered from the retained generation-7
    checkpoint (GAP-59-06).
  - IC13 normalization is on the `R_ref` invalidation list, so a different
    normalizer would itself require a re-measure.
- **Agent was tempted to.** Nothing else; the gap is recorded for
  completeness.
- **Options.**
  - A: reuse the recovered statistics for every arm.
  - B: compute new statistics.
- **Confidence of impact.** LOW.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-18, delegation; option A).
- **Resolution note.**
  - Every record carries the statistics digest, and a mismatch fails closed.
  - The `production_reference` fallback normalizer is never used silently.
