# Phase 50 Pre-Registration Record

**Dated:** 2026-08-12
**Status:** Fixed BEFORE any graded run exists

Every rule stated below is fixed, in writing, before the first Phase-50 graded
run (`runs/stage0-rerun-seed41`, `runs/stage0-rerun-seed42`,
`runs/stage0-rerun-seed43`) exists. No metric from any run — Phase-50 graded,
Phase-50 smoke, or any prior milestone's run — may influence any rule in this
record. This is the same discipline `44-DIAGNOSIS.md` uses for its D-05
uniform-vs-tail criterion and its ranking rubric (`.planning/milestones/
v2.1-phases/44-physics-gate-forensics/44-DIAGNOSIS.md` lines 77-79, 127-140):
state the criterion before any number exists that could bias it. The proof
that this record precedes every graded number is not this date — dates are
mutable labels — it is that this record's commit is an ancestor, in `git log`,
of the commit that opens the first Phase-50 graded run's band generation
(D-07/D-29). This record transcribes locked `50-CONTEXT.md` decisions
(D-07..D-12, D-19..D-21, D-30); it does not re-decide them.

## (1) Submission candidate: seed 42

The run offered to Phase 51 for the single authorized EVAL-01 evaluation is
**`runs/stage0-rerun-seed42`**. Grounding: v2.0 spent its single held-out look
on seed 42, so seed 42's held-out test population is the same physical
population on which `eps_h = 237.2086056078468` was measured
(`runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`). Evaluating
the same population against the conformant recipe makes the new number
directly comparable to the v2.0 number and gives Phase 52's DIAG-05
re-derivation its strongest available basis. No metric, from any run, may
influence this choice (`50-CONTEXT.md` D-08).

## (2) Checkpoint rule: `checkpoints/best.pt`

`pinn/evaluate.py` takes an explicit `--checkpoint` argument, so *which*
checkpoint is evaluated is a real decision, and it is pre-registered here
rather than picked in Phase 51 after validation curves are visible. The rule
is the v2.0 rule: `runs/<run>/checkpoints/best.pt`
(`runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`
`checkpoint_path: "runs/stage0-pilot-seed42/checkpoints/best.pt"`). `best.pt`
is selected by the run's own in-flight retention policy (`store.save_best`,
triggered on every validation improvement inside `pinn/train.py`'s
`checkpoint_hook`) — an automatic rule that predates every Phase-50 number,
not a human reading a chart afterwards (`50-CONTEXT.md` D-09).

## (3) Fallback order: 42 -> 41 -> 43, fired ONLY on structural ineligibility

If the seed-42 run is **structurally ineligible**, the candidate moves to
seed 41, then to seed 43, in that fixed order. Ineligibility is exactly one
of these four conditions (transcribed verbatim from `50-CONTEXT.md` D-10):

1. `eval01_precondition_i` is false.
2. A guard or invariant HALT (subject to the transient-retry carve-out in
   section (7) below).
3. The run's `disposition` is anything other than `finished`.
4. Validation gate metrics are absent (`eval01_precondition_iii` false, or no
   independently-validated production `validation_gate` sidecar).

The fallback fires **only** on eligibility — **never** on a metric's value.
An eligible seed-42 run that looks scientifically bad (a high `eps_h`, a
worsening validation trend, a large SCS) is still the submission. This is the
protection EVAL-01 precondition (i) exists to give, and pre-registering the
fallback order in writing before any number exists is what keeps a bad-looking
number from being quietly routed around.

**For the owner-selected retry policy, eligibility is defined at the final
in-band attempt**: an archived HALT caused solely by a documented/remediated
disk-pressure or external-memory transient does not permanently disqualify a
later successful fresh attempt of the same logical run — see section (7).
Every scientific, invariant, loss-explosion, non-finite, intrinsic-memory, or
unknown-cause HALT is terminal and never reaches selection, regardless of any
later attempt.

**Failure/HALT fallback is dormant under D-20/D-30.** The existence of the
42->41->43 fallback order is NOT permission to launch the remaining seeds
after a scientific or conformance terminal (an invariant-B HALT, a
loss-explosion guard trip, a non-finite loss/gradient/parameter state, or an
unknown numerical failure). Those are owner checkpoints (`50-CONTEXT.md`
D-20/D-21/D-30), not eligibility events this record authorizes an agent to
route around. The fallback becomes usable for a seed disqualified by one of
those terminal causes only if the owner resolves that specific checkpoint by
explicitly authorizing continuation, and the affected plan and its acceptance
criteria are amended, before any further launch. Absent that owner action, a
scientific or conformance terminal on seed 42 (or 41) stops the phase at the
D-11 owner checkpoint below — it does not fall through to the next seed.

## (4) No eligible seed is an owner checkpoint, not a workaround

If none of the three runs is eligible, Phase 50 does not manufacture a
candidate, relax a precondition, or waive a register entry. It records the
state, writes the gap, and routes to the owner; Phase 51 does not open. This
is the protection EVAL-01 precondition (i) exists to give, and it only works
if the agent is willing to end the phase without a candidate (`50-CONTEXT.md`
D-11).

## (5) Split reproduction — verified, not assumed

Each graded run's `splits.json` sha256 is compared against the retained v2.0
pilot baseline, pinned here so the check is re-derivable without
recomputation (`50-CONTEXT.md` D-12):

| seed | v2.0 `splits.json` sha256 |
|---|---|
| 41 | `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86` |
| 42 | `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903` |
| 43 | `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172` |

The seed-42 digest is independently corroborated: it is byte-equal to
`splits_sha256` inside the v2.0 evaluation receipt
(`runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`), so it is the
identity `eps_h = 237.2086056078468` was actually measured against. An exact
match on a graded run proves the held-out population is unchanged since v2.0.
A mismatch is not a failure but a mandatory qualification — the admitted
population moved (the CONF-02 admission-path change is the expected
candidate), the v2.0 comparison is no longer like-for-like, and that fact must
travel into Phase 51 and Phase 52. Either outcome is recorded; neither is a
licence to adjust anything.

## (6) Identity pins: `source_config_sha256` vs `frozen_config_sha256`

Following the v2.0 evaluation receipt's three-identity pinning pattern
(`checkpoint_sha256` / `config_sha256` / `splits_sha256`), this record pins
one identity now and defines — without filling — the identities that can only
exist after a run:

- **`source_config_sha256`** (pinned now, in the JSON block below): the
  sha256 of the exact bytes of the **committed input YAML**,
  `configs/stage0-rerun-seed42.yaml`, computed with `shasum -a 256` against
  the file as it stands at this record's own commit:
  `72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097`.
- **`frozen_config_sha256`** (NOT pinned here — deliberately absent from this
  record): the sha256 of the fully resolved, defaults-filled, stable-sort
  `runs/<candidate>/config.yaml` bytes that `freeze_resolved_config` writes at
  launch. This is a DIFFERENT artifact from the committed source YAML above —
  it carries every field the dataclass defaults fill in (e.g.
  `stage.replay_count`, `opt.adam_betas`, `run.checkpoint.failure_keep`) that
  the source YAML leaves unset. `source_config_sha256` and
  `frozen_config_sha256` **MUST NOT be compared to each other** — they hash
  different byte streams by construction, and Phase 51 must never treat
  "different hash" between them as a corruption signal.

This pre-registration blob is kept **immutable** after its own commit: no
mutable hash slot (a checkpoint hash, a frozen-config hash, a terminal
artifact hash) is filled in here, now or later, because a record that could
still be edited after a run exists is not a pre-registration. Instead, **plan
50-03 writes a separate candidate execution receipt**, keyed to this record's
own `pre_registration_commit`, recording the source config hash (repeated),
the frozen config hash, the reproduced `splits.json` hash, the selected
`best.pt` hash, and the terminal artifact hashes of the selected candidate
run. Phase 51 must exact-match that receipt before spending the authorized
evaluation. What is pre-registered here is the **checkpoint-selection RULE**
(`checkpoints/best.pt`, `best.pt`'s own in-flight retention policy) — not its
future bytes, which do not exist yet.

## (7) Recovery / attempt policy (owner-selected, this revision)

A fresh transient retry is allowed **at most once per logical run name within
one band generation**, and only after a failure has been **positively
identified** as transient disk pressure or transient external memory
pressure — with no code, config, corpus, threshold, or seed change accompanying
the retry. Loss explosion, non-finite loss/gradient/parameter state, and
unknown numerical failure are explicitly **excluded** from this transient
class; an intrinsic or unexplained numerical failure is evidence, not a
transient, and is never blind-retried — it stops and is surfaced per D-30.
Memory watermark pressure alone is an insufficient positive identification:
independent facts must show external (non-Phase-50) GPU/memory work was
present and has since been removed; absent that corroboration the failure is
classified intrinsic/unknown and the run stops.

**Before a retry**, the canonical `runs/<run_name>/` directory is moved
atomically to a unique `runs/<run_name>-attempt-<NN>-<disposition>-<UTC>/`
archive. The archive's path and its terminal artifact hashes are recorded in
the run ledger (`evidence/run-ledger.md`). An attempt directory is **never
deleted or overwritten**. The retry then launches the **unchanged committed
config** at the **same git head** — the archive-then-relaunch mechanism
recreates the canonical `runs/<run_name>/` directory from a clean state, so a
failed attempt and its successful canonical retry never collapse into one
ambiguous record.

**Invariant-B HALTs are excluded from this transient-retry class.** An
invariant-B HALT keeps `50-CONTEXT.md` D-20's owner-checkpoint treatment
unchanged and is never auto-retried under this section — it routes to the
owner exactly as D-20 requires, independent of any disk/memory finding.

**Calibration-expiry refresh and a new-generation relaunch are distinct
protocol causes, not transient retries** in the sense above — but a failed
*refresh* attempt still receives, at most, one transient retry within its own
generation, under the identical positive-identification and archive-first
rules. A stale (>24h) calibration is refreshed via the same archive-before-
rerun mechanism, applied to the smoke run plus the superseded calibration
JSON, without invalidating the already-graded seeds — but only while the full
generation identity (git head, the committed config set, the corpus
snapshot, the environment snapshot, and the runtime fingerprints) is
unchanged. Any code, config, corpus, or environment repair or drift closes the
current generation terminally and opens a new one, which restarts the full
smoke-then-band sequence from step zero (`50-CONTEXT.md` D-17); external state
can open a new generation even when `git rev-parse HEAD` does not change.

For this band, this owner-selected evidence-preserving fresh-attempt rule
**supersedes** the operator runbook's ordinary disk/memory resume response —
under this policy a failed attempt is archived and restarted from step zero,
it is never resumed.

**Phase 50 admits no `--resume` path, under any circumstance.** The current
checkpoint format restores the model, the optimizer, the scheduled-weight
state, the gradient clipper, the curriculum/controller counters, the main run
RNG, and the invariant-B state — but it does **not** checkpoint the separate
`CollocationSampler` RNG stream. Step alignment alone is therefore
insufficient to prove the resumed run would draw the same collocation times
as an uninterrupted run, so no resumed attempt can be proven to continue the
same optimization trajectory. Every interruption — of any cause, transient or
not — therefore closes **terminally**. Any later continuation requires an
owner-approved amended plan and a fresh full generation launched from step
zero. `resume_allowed: false` and `missing_state: [collocation_sampler_rng]`
in the JSON block below encode exactly this.

---

## Machine-readable selection policy and generation binding

The block below is the single fenced, machine-readable JSON policy this
record carries, tagged `schema: phase50-pre-registration/v2`. It contains two
nested objects. `selection_policy` encodes — not merely repeats in prose —
the primary seed, the fixed candidate order, the checkpoint-relative path
rule, the four (positive-form) eligibility facts, the
`prior_authorized_transient_halt_disqualifies` flag, the allowed transient
causes, the terminal cause classes, the once-per-logical-run-per-generation
retry ceiling, and the `resume_allowed`/`missing_state` pair. Its own hash,
`selection_policy_sha256`, is the sha256 of the canonical compact
(`sort_keys=True, separators=(",", ":")`) JSON serialization of the
`selection_policy` object alone (not including the hash field itself), so any
future byte-level change to the policy is self-detecting. `generation_binding`
separately carries the three D-12 expected split hashes, `source_config_sha256`
(section (6) above), the sorted `committed_config_sha256_by_path` mapping over
all four Phase-50 config repo paths — computed as the sha256 of each file's
exact bytes destined for the Task-3 wave-1 commit — and `committed_config_set_sha256`,
the sha256 of that mapping's own compact sorted JSON. Plan 50-02 must
reproduce both the per-path map and the aggregate from
`git show <this-record's-commit>:<path>` for each of the four config paths
before it opens a band generation; a mismatch means the committed bytes moved
between this record's commit and generation-open, and generation-open must
refuse. `generation_binding` also carries `required_launch_flags:
["--stage-0-only"]`, `forbidden_launch_flags: ["--resume"]`, and a nullable
`parent_pre_registration_commit`. The original revision set that field to
`null` (Phase 50's first pre-registration). The generation-3 amendment below
sets it to the prior pre-registration revision recorded as generation 2's
ancestor in the run ledger.

On a later D-19 conformance-repair rerun (a new band generation after a
terminal closeout), only `generation_binding` is updated to the new commit's
identities; the `selection_policy` object and its `selection_policy_sha256`
must remain byte-identical. This JSON block is the **only** selection-policy
input plan 50-03 parses when it extracts the band; the prose above supplies
rationale and is not itself a second, independently mutable rule surface.

## Generation-3 amendment (2026-08-15)

This is a D-19 conformance-repair amendment after generation 2 closed
terminally. Reason: GAP-50-02 Option A (2026-08-13) — `_run_validation` now
evaluates the entire held-out Stage-<=k validation pool, matching
`compute_validation_gate` and the spec's "held-out validation set". The
Task-3 repair commit `312f3080ab50e35be18ba87c9f0618866265b227` is the new
source identity; register entry `C-09` records the closed divergence.
Generation 3 must open at a head strictly after that commit.

`selection_policy` and `selection_policy_sha256` are byte-identical to the
prior revision (recomputed as the sha256 of the canonical compact
serialization of `selection_policy` alone and required equal). The four
config hashes, the aggregate `committed_config_set_sha256`,
`source_config_sha256`, and the three `expected_splits_sha256` values were
re-derived from `git show HEAD:<path>` / `git show 312f3080:<path>` and
matched the stored values — they were not copied forward by assumption.
`required_launch_flags` stays `["--stage-0-only"]` and
`forbidden_launch_flags` stays `["--resume"]`. `parent_pre_registration_commit`
moves from `null` to `abd5f8d9bc44c31abb58194e86806ea6aa39a649` (generation
2's `pre_registration_commit` in `evidence/run-ledger.md`).

No config byte, split, seed, threshold, or hyperparameter changed between
generation 2 and generation 3. Only the source identity and this
generation-binding parent pointer changed.

```json
{
  "generation_binding": {
    "committed_config_set_sha256": "e6e1fd53f93ec0b3059ff2da8eb9d27b92546b3d74fd7bffdbd0a11373a4e078",
    "committed_config_sha256_by_path": {
      "configs/stage0-rerun-seed41.yaml": "90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073",
      "configs/stage0-rerun-seed42.yaml": "72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097",
      "configs/stage0-rerun-seed43.yaml": "1c2336d8342198a417a129d3e70e7ce53609b1d28aff3fd021a92f8bd20360e6",
      "configs/stage0-rerun-smoke.yaml": "a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a"
    },
    "expected_splits_sha256": {
      "41": "c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86",
      "42": "5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903",
      "43": "a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172"
    },
    "forbidden_launch_flags": [
      "--resume"
    ],
    "parent_pre_registration_commit": "abd5f8d9bc44c31abb58194e86806ea6aa39a649",
    "required_launch_flags": [
      "--stage-0-only"
    ],
    "source_config_sha256": "72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097"
  },
  "schema": "phase50-pre-registration/v2",
  "selection_policy": {
    "allowed_transient_causes": [
      "disk_pressure",
      "external_memory_pressure"
    ],
    "candidate_order": [
      42,
      41,
      43
    ],
    "checkpoint_relative_path": "checkpoints/best.pt",
    "eligibility_facts": [
      "eval01_precondition_i == true",
      "final-attempt guard/invariant rule satisfied: no unresolved guard or invariant HALT at the final in-band attempt (an archived, positively-identified transient disk/external-memory HALT does not disqualify a later successful fresh attempt in the same generation; every scientific/invariant/loss-explosion/non-finite/intrinsic-memory/unknown HALT is terminal)",
      "final_process_disposition == 'finished' AND ledger_disposition == 'finished'",
      "eval01_precondition_iii == true AND independent production validation_gate sidecar validation passes"
    ],
    "missing_state": [
      "collocation_sampler_rng"
    ],
    "primary_seed": 42,
    "prior_authorized_transient_halt_disqualifies": false,
    "resume_allowed": false,
    "retry_ceiling": "at most one fresh transient retry per logical run name per band generation",
    "terminal_cause_classes": [
      "scientific",
      "invariant",
      "loss_explosion",
      "non_finite",
      "intrinsic_memory",
      "unknown"
    ]
  },
  "selection_policy_sha256": "c634aaac74aee5ef123b848bcb3816a09d90c5a9a24123adb598796ccef9873b"
}
```
