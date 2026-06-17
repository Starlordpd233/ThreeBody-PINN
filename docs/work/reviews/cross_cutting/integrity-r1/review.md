I verified the package end-to-end against the live repo and the dataset on disk. Here is the assessment. I changed nothing.

Bottom line

The integrity-r1 package is in much better shape than your questions presuppose — it already anticipated all four of your concerns, and the parts I could verify empirically check out. The spec snapshots are the current framework (byte-identical, hash-confirmed), the dataset is already represented empirically rather than via sampling_method.md, and both the ongoing (issue-02) and next-milestone (issue-03) work are already embedded as context. There is one real defect worth fixing before you send, and one timing decision to make.

What I verified

┌────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         Check                          │                                                                       Result                                                                       │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Spec snapshots vs live framework specs (cmp)           │ IDENTICAL for all 3 (ctl / pinn_architecture / sampling)                                                                                           │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Snapshot SHA-256 vs the DELIVERY-NOTE's claimed hashes │ All 3 MATCH                                                                                                                                        │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Live spec history                                      │ Phase-26 contracts (b1852b0f..ab5f7f06) landed before the snapshot refresh; no Phase-27 edits have landed — so "no adopted spec edits yet" is true │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Dataset counts vs DATASET-CONTEXT.md                   │ Exact: 4,857 / 4,857 / 2,749 / 2,565 = 15,028                                                                                                      │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 184-rerun state                                        │ 60 of 184 staged under rerun_staging/.../outputs/, 0 promoted → "still 2,565, staged-not-promoted" is currently accurate                           │
├────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ctl §3 coverage enumeration in the master              │ STALE — see below                                                                                                                                  │
└────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

The one thing to fix before sending: a stale coverage map

When the ctl_instruction.md content snapshot was refreshed to post-Phase-26 HEAD earlier today, the master's §3 coverage-matrix enumeration was not regenerated to match it. Concretely:

- It claims 26 H1/H2 headings in ctl; the attached snapshot has 27.
- The new Phase-26 heading "Step 1A — Trajectory Admission Gate" (line 452) has no row in the enumeration.
- Every line number from "Step 2" onward is wrong by +40 to +218 lines (e.g., SI-CTL-001 is at line 1676, the table says 1456).

This matters because the master itself calls the coverage matrix "the audit's single most important defense against confident-sounding 40% coverage," and tells the agent "line numbers refer to the attached snapshots." The omitted heading is the newest load-bearing contract (the admission gate) — exactly what the audit should scrutinize, now at risk of escaping a coverage verdict. This is meta-drift, not spec drift: the audited text is current; the map of it is stale. (pinn_architecture.md = 25 and sampling_method.md = 12 are both correct — only ctl was refreshed, so only ctl's table went stale.) Fix is mechanical: regenerate the ctl sub-table to 27 rows with current line numbers.

The one time-sensitive thing: the 184-rerun is live

The rerun is actively producing (60/184 done) and none promoted yet, so the package is accurate right now. The active-staged-remediation label already protects the framing. The only decision: if a promotion lands in the middle of your multi-AI fan-out, the "2,565 / 184-missing" frame the agents reason against shifts underneath them. Recommendation: either freeze promotion until the audits return, or accept it (the label already tells agents not to count staged outputs). Low stakes; just be deliberate.

Your three "should we include…" questions — already answered by the package

1. Ongoing this-milestone work? Already in. The bundle's in-flight register marks Phase 26 landed / 27 planning / 28 pending, and 02-resolution-doc.md is embedded behind BANNER-2 ("candidate verdicts under adjudication"). The against-in-flight-edit novelty tag routes overlapping findings to the owning phase. This is the right model: audit the frozen snapshot, tag — don't drop — overlaps.
2. Next-milestone / next issue doc? Already in. 03-curriculum-and-training-loop.md is embedded behind BANNER-3 ("unadjudicated critiques; open issue doc for a future milestone"). So your "next two issue documents" (02 in adjudication, 03 upcoming) are both present, each correctly bannered for its maturity.
3. Attach the actual dataset rather than sampling_method.md? Already done — better than proposed. DATASET-CONTEXT.md is a curated, per-fact-labeled empirical transcription (verified-empirically / corrected-by-DATA-07 / active-staged-remediation), and I confirmed its counts against disk. Crucially, the package deliberately rejected attaching the raw simulation_data/Documentation/README.md because it re-imports the stale figures the curated file exists to police. Do not add the raw dataset docs back — that would reintroduce exactly the drift you're worried about. Your instinct was right and is already implemented.

So "does it reflect the entire framework?" — Yes for everything adopted: the 3 specs (audit subjects), the v1.4 locked decisions (carried as Tier-2 in the master), the SCS/SASD/IPR/PSC metrics (embedded DQA, BANNER-1), and the dataset (DATASET-CONTEXT). The only things absent are the not-yet-decided Phase-27/28 contracts and issue-03 resolutions — correctly absent, because a snapshot audit shouldn't audit decisions that don't exist yet.

In the research agent's shoes: the seams that actually carry the framework

Grounding in the math, these are where a disruptive finding most likely hides. The package already steers toward most of them; I note coverage and the one gap:

1. Normalized-time chain rule (silent 1/T bug). τ = 2u−1, u = t/T ⇒ d/dt = (2/T)·d/dτ, and acceleration carries (2/T)². Drop a T-power anywhere in the physics residual or energy terms and the dynamics are silently mis-scaled. Covered (RD-2 AD contract, RD-4).
2. Global nondimensionalization self-consistency. Raw-mass D=(G·T²)^⅓≈4.6416 (mass-fraction ≈6.694 rejected). With raw masses spanning a range, does a residual M^⅓ scale leak across trajectories under a single global D? Covered (RD-2, §4 row 6; this is Phase-27's "global-scale" topic → will be tagged against-in-flight-edit).
3. Dual-ε Plummer softening consistency. The energy-conservation loss must use the same softened Hamiltonian as the force it regularizes (ε_train=1e-5), while the SCS data gate uses ε=1e-10; softening breaks exact conservation of the unsoftened H. A mismatch penalizes an ε-artifact, not physics. Strongly covered (RD-4-iv, stress-Q3).
4. COM-projection × autodiff × frame. Conservation laws (L = Σ mᵢ rᵢ×vᵢ) must be computed in the same COM/nondimensional frame as the labels, post-projection. Covered (RD-4-iii, §4 row 8).
5. SCS conditioning at H(0)≈0. ε_H = max_t|(H(t)−H(0))/H(0)| divides by H(0); marginally-bound triples (H(0)→0) blow it up and reject good trajectories. Covered (already mid-adjudication via the resolution doc's near-zero-H(0) quarantine).
6. Sampling-rate vs SIREN frequency content — the under-exposed seam. Base trajectories have ~61 snapshots over the horizon; the SIREN's first_omega_0=30 can represent high-frequency features, and close encounters produce sharp velocity spikes. Can 61 samples support that frequency content without aliasing/overfitting on base-stage data, or does the curriculum depend on gold (~1003) for the high-frequency stages? The package gives the agent the snapshot distribution but does not pose the Nyquist/aliasing question explicitly. This is the single highest-value stress question to add.
7. Single-source-of-truth for D, T, ε, n_pts. Duplicated normative definitions across specs are drift risk — which is exactly why the §3/§4 scaffold must be clean (ties back to the finding above).

Recommended actions

1. Fix the ctl §3 coverage enumeration before sending (27 rows, current line numbers, add the Step-1A admission-gate row). Mechanical; restores the audit's primary QC mechanism. (I can do this on your word.)
2. Add one stress question on sampling-rate/Nyquist vs SIREN ω0 (seam 6). Cheap, high-leverage. (I can draft it.)
3. Decide the rerun-promotion timing for the fan-out window (freeze, or rely on the label). Your call; low stakes.
4. Do not attach raw dataset docs or not-yet-adopted resolutions — the curated context and the embed-with-banner model are the correct design.
5. (Optional, cosmetic) refresh the "GAP-27-01 open" line — it was resolved in 09e37f89; immaterial to the audit.