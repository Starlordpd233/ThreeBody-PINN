# Integrity R1 Research Agent Prompt (framework integrity audit)

**[User instructions — not part of the prompt]** Attach these 6 files to the external
agent's conversation (individually — no folders), then paste everything below the
horizontal rule as the prompt:

1. `research_package/RESEARCH-CONTEXT-MASTER.md` (this package's master)
2. `specs/ctl_instruction.md` (shared snapshots at the round root)
3. `specs/pinn_architecture.md`
4. `specs/sampling_method.md`
5. `research_package/DATASET-CONTEXT.md`
6. `research_package/KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md`

---

You are an external research agent performing a **disruption-first integrity audit** for
a computational-physics ML project: a curriculum-trained physics-informed neural network
(CTL-PINN) that learns gravitational three-body trajectories from a frozen dataset of
high-precision N-body simulations, to be trained on a single MacBook by a project owner
who is not an expert at model training. The project is about to build its training stack
against three framework specification documents. Your job is to audit those three specs
**as a whole** — coherence, buildability, mathematical and physical correctness,
scientific soundness, and load-bearing assumptions — and surface everything that would
force disruptive change later, while change is still cheap.

You have been given six files. You have NO access to the project's repository or
dataset — work only from these six files plus your own research of current primary
sources (peer-reviewed literature, official documentation; not blog hearsay):

- `RESEARCH-CONTEXT-MASTER.md` — your entry point. It contains the orientation, the
  three-tier source treatment (fixed facts / locked decisions-of-record / fully
  reviewable content), the locked-decision challenge protocol, eight review dimensions
  (RD-1..RD-8) with named sub-checks, and the output contract your deliverable must
  satisfy — including the severity rubric, the per-heading coverage matrix you must
  fill, the constants concordance table you must complete, and the required section
  order. Read it first and follow it exactly.
- `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md` — the three
  framework specs. These are the audit subjects. `sampling_method.md` documents the
  *completed, frozen* data-generation work — audit it for what it implies about the
  data and for cross-spec contradictions, not as an active design to improve.
- `DATASET-CONTEXT.md` — consolidated dataset context: verified facts about the current
  training-data folders, stale-figure corrections, and the staged missing-184
  standard-gold rerun status, each entry carrying a per-fact status label. This is your
  only dataset evidence.
- `KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md` — three embedded project documents (known
  critiques and candidate verdicts, each behind an authority banner stating its exact,
  non-authoritative standing) plus the register of the project's in-flight work. Read
  it **last**, after you have formed your own view of the specs. If your platform
  ingests all attachments at once and a read order cannot be honored, that is expected —
  the binding requirement is the novelty classification below, not the read order.

**Your task:** work through all eight review dimensions in the master, in order of
disruption priority — RD-1 fundamental viability red-team (with the named literature
anchors and beyond); RD-2 cross-spec coherence (seam hunt, single-source-of-truth
analysis, cross-reference validity, authority hierarchy); RD-3 buildability gap audit
(walk the pipeline end-to-end as an implementing agent forbidden to invent; tensor
shapes, hyperparameter scope, reproducibility closure, failure-mode behavior,
determinism boundary); RD-4 mathematical and physics correctness (re-derive, dimension-
check, conservation-form and softening consistency, autodiff round-off); RD-5 ambiguity
audit; RD-6 scientific soundness vs current literature (steelman before criticizing);
RD-7 data–framework compatibility against `DATASET-CONTEXT.md`; RD-8 load-bearing
assumptions and risk register (door classification, compound failures, mitigation-cost
ranking). Every dimension produces findings, a coverage statement, and an explicit
"checked, found nothing" register — negative results are valued and required.

High-priority stress questions to keep in view throughout the audit:

- Does the framework remain mathematically and physically coherent under the actual
  dataset realities in `DATASET-CONTEXT.md`: non-contiguous IDs, variable snapshot
  counts, absent footers, folder-level parameter defaults, missing/staged gold
  counterparts, and blacklist semantics?
- Does the HDF5 processed-data contract preserve all identities and provenance needed
  for physics and curriculum logic: `record_key`, `physical_key`, source hashes,
  fidelity, per-trajectory parameters, `dt_out`, and stage labels?
- Are dimensionless scaling, mass handling, time normalization, COM projection,
  automatic differentiation, Plummer softening, and validation-epsilon choices mutually
  consistent across the specs?
- Are SCS, SASD, IPR, and PSC definitions mathematically meaningful and threshold-
  aligned with the locked post-v1.3 screening gate, especially where embedded known
  issues contain pre-adjudication or conflicting formulations?
- Is the curriculum / multi-fidelity story buildable when standard-gold coverage is
  incomplete in the current live folders and only staged for the missing 184 IDs?
- Can the entire approach plausibly train and be verified on the stated single
  Apple-Silicon laptop constraint, without relying on unstated cloud, cluster, or
  future-data assumptions?

Ground rules:

- **Severity discipline.** Every finding carries exactly one severity from the master's
  rubric: S1 (invalidates/re-scopes the core approach), S2 (builder cannot proceed /
  specs contradict), S3 (rework-likely / violates cited best practice), S4 (hygiene —
  compressed into a single appendix). Rank §1 Top Disruptions severity-first.
- **Novelty classification on every finding** — `novel` / `confirms-known` /
  `contradicts-known` / `against-in-flight-edit` (see the bundle's in-flight register).
  This is mandatory; it is how the project distinguishes your independent analysis from
  echoes of its own known issues. Findings overlapping in-flight topics are still
  wanted — tag them, don't drop them.
- **Evidence classes on every finding** — `quoted-textual` / `derived-math` /
  `literature-cited` / `judgment`. Quote verbatim with file + heading wherever a finding
  turns on what a document says.
- **Locked decisions are challengeable only via the protocol**: high evidence bar
  (math or literature, not judgment alone), explicit steelman of the locked decision
  first, and a `locked-decision challenge` flag on the finding.
- **Tier-1 facts are fixed**: the verified dataset baseline and any
  `verified-empirically` entries in `DATASET-CONTEXT.md` are facts; the only current
  data-change exception is the explicitly labeled `active-staged-remediation` path for
  the 184 missing standard-gold outputs; training is single-machine.
- **Never invent.** Where the attached materials are silent, ambiguous, or insufficient,
  record the gap in the §7 open-items register; where you must assume to proceed, state
  the assumption inside the finding. Treat any file referenced but not attached as
  unavailable.
- **Verify externals.** Literature and library-behavior claims must cite current primary
  sources, date-stamped as of your research date.
- **Anti-padding.** Do not manufacture findings; thoroughness is demonstrated by the
  coverage matrix (every H1/H2 of every spec gets a verdict), not by volume.

**Your deliverable:** a single self-contained markdown document satisfying the output
contract in `RESEARCH-CONTEXT-MASTER.md`, in this exact section order: Header (with the
file inventory you received); §0 scope and decision standard; §1 Top Disruptions (the
5–10 most disruptive findings, ranked); §2 decision matrix (ID | severity | novelty |
door | one-line verdict); §3 coverage matrix (a verdict for every enumerated H1/H2:
`audited-clean` / `findings: INT-NNN…` / `skimmed-only` + reason); §4 constants and
contracts concordance (complete and extend the seeded table; mismatches and
double-definitions become findings); §5 resolutions by dimension (RD-1..RD-8, each with
coverage statement, findings in the full schema — stable `INT-NNN` ID, severity, blast
radius, door type, novelty, evidence class, candidate resolution direction,
verification suggestion, confidence — and a negative-results register); §6 consolidated
minimum-decision-list (the smallest set of project-owner decisions to make the specs
build-ready, each as a question with options A/B/C, trade-offs, recommendation,
confidence); §7 open items register; References.

Quality bar: this audit's standing in the project is a findings register feeding human
triage — it decides nothing by itself, so do not soften findings out of deference and do
not dress recommendations as decisions. Steelman the design before concluding against
it; show your work on every re-derivation; make every "clean" verdict falsifiable by
saying what you checked. Write for a technically strong reader who is not an ML-training
expert: plain language, defined symbols, concrete citations.
