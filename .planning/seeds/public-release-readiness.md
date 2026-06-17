---
title: Public-release readiness — considerations to revisit before making the repo public
planted_date: 2026-06-12
trigger_condition: >
  User decides to make the repository public (or to publish an accompanying paper /
  dataset). At that point this seed becomes a dedicated readiness-audit phase or
  cross-cutting work item; until then it is a mindfulness checklist, deliberately NOT
  an executed audit (user directive 2026-06-12: "worry briefly and not too much").
---

# Seed: Public-Release Readiness

The repo may eventually go public. These are the dimensions to think through *at release
time*, with project-specific observations grounded as of 2026-06-12 (commit-era
`c17e23ed`+). Ongoing-work habits that keep release cheap are in the companion memory
note; this seed is the release-time checklist.

## 1. Replicability — could someone else reproduce the training result?

The strongest current asset is the project's own discipline: commit-pinned research
packages, the `runs/<name>/` reproducibility contract ("give a colleague the runs/
folder"), the verified-facts registers, and the DATA-05 quarantine trail all serve
external replicators directly. Gaps to close at release:

- **Data**: the bulky `simulation_data/` payloads likely cannot ship in git (the
  migration runbook already treats them as separate). Decide: publish dataset via an
  archive (Zenodo/HF) with hashes, or document the regeneration path end-to-end
  (`sampling_method.md` → `ic_generation/` → prescreening → Brutus runners → metrics).
  Note Brutus arbitrary-precision builds are machine-sensitive; the gold-standard runner
  is Mac-specific.
- **Environment**: exact package pins + framework version (trainex r1b K2 covers
  pinning discipline; carry it into the published runbook).
- **Determinism**: publish the seed/variance policy from trainex r1a D6 — without it,
  "replicate the result" is ill-defined on Apple-Silicon backends.
- **Quarantines and anomalies**: the issue ledger and DATA-xx registers should ship —
  they are the honest provenance trail (which outputs are valid, which 70 are
  quarantined, why).
- **Single-machine bias**: results are tied to one M5 Pro; state hardware assumptions
  plainly rather than implying portability.

## 2. Copyright / licensing — the biggest concrete gap found

- **No root LICENSE and no CITATION.cff exist** (verified 2026-06-12). Public without a
  license = all-rights-reserved; nobody can legally use it. Pick licenses deliberately
  (code vs docs/specs may differ, e.g., MIT/Apache-2.0 + CC-BY).
- **Vendored third-party code**: `brutus_Newton-main/` (has its own LICENSE) and
  `reference-code/reference_NNs/` contains FULL vendored copies of at least GravNN,
  PINA, PyTorch-LBFGS, deepxde, hamiltonian-nn, neural-symplectic-integrator — each
  with its own license. At release: verify each license permits redistribution, keep
  the license files intact, and consider replacing vendored copies with pinned
  references/submodules where redistribution is awkward.
- **`paper_templates/`**: journal/LaTeX templates — check their redistribution terms.
- **External AI research outputs** (`research_results/*-resolution.md`): generally the
  user owns provider outputs, but confirm per provider terms at release; also check
  quoted literature in issue docs stays within fair use.

## 3. Privacy

- Git history publishes author name/email on every commit — conscious acceptance, or
  history rewrite (drastic; avoid unless necessary).
- **16 tracked files embed `<home>/...` absolute paths** (verified
  2026-06-12) — harmless but identifying; sweep at release (and prefer relative paths
  in new work).
- No tracked `.DS_Store` or `settings.local.json` (verified). Re-scan at release,
  including full git history for secrets/tokens (gitleaks/trufflehog) — the repo has
  never needed credentials, but scan anyway; backup branches and recovery tags count.

## 4. Repo hygiene

- `.planning/`, gap registers, discussion logs, and agent-governance files (CLAUDE.md,
  `.claude/rules/`) are an unusual but legitimate publishable artifact — decide
  deliberately whether the internal process trail is part of the public story or gets
  pruned. Pruning docs/ requires the docs/README.md audit-and-approval lifecycle.
- Legacy docs folders mid-cleanup (`docs/superpowers/`, `docs/plans/`, ...) should be
  resolved before strangers navigate them.
- Large-file check across history (simulation outputs, knowledge-graph artifacts) —
  consider whether history needs thinning before the repo is cloneable at sane cost.
- A public-facing root README (what this project is, how to navigate, how to replicate)
  does not exist yet — the current entry points are agent-governance docs.

## 5. Safety

Low risk: classical N-body physics + PINN training has no meaningful dual-use surface.
Two small items: published runbooks should not present destructive commands (resets,
`rm`, force-push recovery procedures) without their guard context; and the
agent-governance docs reference security-testing boilerplate that is fine but should
read sensibly to outsiders.

## When triggered, the first action

Spin up a dedicated readiness pass (cross-cutting work item or phase): license decision
first (it gates everything), then the third-party license audit, then the
privacy/hygiene sweeps, then the replicability packaging (README, CITATION, dataset
archive, environment pins). Each dimension above becomes a checklist section; none of it
is done implicitly.
