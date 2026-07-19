---
status: active
purpose: design
created: 2026-07-19
milestone: "untracked"
phase: cross-cutting
retirement_trigger: implementation and verification artifacts absorb these decisions and a reference audit passes
---

# Agent Skill Lifecycle, Publication, and Hygiene Design

## Summary

Create one reversible maintenance system for standalone skills and plugin-provided skills across Codex, Claude Code/CCP, OpenCode, ZCode, and Grok. Google Antigravity is explicitly out of scope.

The system has one user-facing skill, `maintain-agent-skills`, backed by a deterministic driver. User-owned or explicitly adopted portable standalone skills use `~/.agents/skills` as their single physical global home. Each platform receives exactly one effective exposure through native discovery, a per-skill symlink, or—only when neither works—a hash-verified materialized projection. Manager-owned plugin, marketplace, bundled, and system skills remain under their owning managers and are represented in a consolidated off-prompt registry. Separately approved curated derivatives are complete pipeline-owned plugin packages.

The system covers two related workflows:

1. Publish, update, migrate, and verify standalone skills across platforms without duplicates.
2. Audit unused skills, propose cleanup, apply only approved changes, survive package updates, and either roll back to a verified recorded state or preserve later drift and stop `conflicted` for a separate resolution plan.

No migration may move only `SKILL.md`. A skill is the complete directory tree plus its declared dependencies and recorded execution context. Migration follows `copy -> verify -> switch -> retain`; it never destroys the only working copy.

## Goals

- Maintain one physical global home for portable standalone skills without adding another canonical skill store.
- Make a new or updated standalone skill discoverable on every selected platform through one repeatable `publish` -> approval -> `apply` workflow.
- Ensure each platform/profile consumer sees an invocation name exactly once across its complete discovery graph.
- Preserve full skill functionality, including scripts, references, assets, executable modes, symlinks, cross-skill dependencies, and stable external helpers.
- Inventory plugin and marketplace skills without taking ownership away from their package managers.
- Disable approved unused skills in update-resistant ways and measure the resulting context reduction.
- Make every mutation reviewable, atomic where practical, and recoverable through journaled, conflict-safe rollback.
- Keep the maintenance registry out of ordinary model context and load it only when maintenance is requested.

## Non-goals

- Physically relocate plugin or marketplace payloads into `~/.agents/skills`.
- Edit versioned plugin caches, bundled runtime trees, or package-manager staging directories.
- Publish or promote project-local skills. The first implementation inventories them only so their collisions are visible.
- Infer that a skill is unused merely because no invocation evidence was found.
- Automatically disable, delete, archive, or prune skills without an approved immutable plan.
- Run a background filesystem watcher. Publishing and reconciliation are explicit maintenance actions.
- Normalize unrelated platform configuration or plugin versions as a side effect.

## Baseline and motivation

The read-only 2026-07-18/19 inventory found:

- 15 standalone/project discovery roots in scope.
- 910 lexical skill entries resolving to 705 skill directories.
- 127 normalized frontmatter names.
- 210 directory-symlink entries.
- 77 same-realpath alias groups.
- 111 byte-identical-copy groups.
- 77 normalized names with divergent content.

These classes overlap and are not additive. They demonstrate that physical path count is not the same as effective skill count.

Two current Codex examples define required regression cases:

- `xconverge` is visible through both `~/.agents/skills` and `~/.codex/skills`, with byte-identical trees.
- `xreview` collides across those roots but has divergent content.

The July 17 `sync-gsd-fleet` incident established the same root cause for a previously repaired skill: Codex indexed the shared Agents root and an active profile-local root. The durable rule is therefore consumer-level uniqueness, not merely byte-level deduplication.

The active plugin inventory also shows why plugin skills cannot be flattened safely. Examples include skills coupled to plugin hooks, MCP services, sibling agents, executables, Node modules, dashboards, and plugin-root environment variables. Plugin managers own versioned paths and may replace or garbage-collect them during updates.

## Core concepts

### Consumer

A consumer is a platform plus the effective profile/configuration root used for one session. Multiple CCP aliases that resolve to the same `CLAUDE_CONFIG_DIR` are one consumer for global skill publication. Four Codex homes are separate profiles but share one global standalone root.

### Discovery graph

A discovery graph is every root, plugin registry, compatibility root, and project-local path that a consumer may scan in a specified working directory. Duplicate detection operates on this graph, not on an individual folder.

### Logical identity and invocation identity

The registry records two identities:

- Logical identity: ownership namespace plus skill name, such as `standalone/xreview` or `plugin/superpowers/brainstorming`.
- Invocation identity: the effective platform-visible name, including a plugin namespace where the platform uses one.

Version and content digest are attributes, not identity. The same basename under two plugin namespaces may be valid; two exposures with the same effective invocation name for one consumer are not.

### Ownership classes

Every discovered skill receives exactly one class:

- `user-standalone`: user-authored or explicitly adopted portable skill.
- `external-standalone`: plain skill installed or updated by an external installer. It remains installer-owned until an adoption plan transfers update authority.
- `profile-local`: deliberately unique to one platform profile.
- `project-local`: deliberately scoped to one project.
- `plugin-managed`: component of an installed plugin or marketplace package.
- `system-bundled`: shipped and owned by a platform/runtime.
- `curated-plugin`: complete pipeline-owned local plugin package derived from an upstream version.

Only user-owned or explicitly adopted standalone skills may be consolidated. Adoption requires a proven writer transfer: retarget, disable, or uninstall the previous updater so it cannot recreate the old exposure. If writer transfer cannot be proven, the skill remains external and in place. Plugin and bundled caches are read-only inventory sources.

## Governing invariants

1. **One effective exposure:** each `(consumer, working-directory scope, invocation name)` resolves to exactly one enabled entry.
2. **One writer:** every skill has one authoritative writer. Projections are disposable outputs and never synchronization peers.
3. **Whole-tree integrity:** a standalone skill moves as its complete directory tree plus a reviewed dependency/execution contract and successful functional probes, not as selected Markdown files.
4. **Plugin-root integrity:** plugin managers remain sole writers of plugin caches. A plugin-coupled skill is never extracted as a standalone skill.
5. **No silent conflict resolution:** divergent same-name entries block until the user selects a canonical outcome.
6. **Fail closed:** unknown roots, stale plans, broken links, unresolved dependencies, and unverifiable functional probes block mutation.
7. **Explicit approval:** only an immutable plan identifier may be applied.
8. **Reversibility:** every changed path and configuration fragment has a pre-change snapshot and verified rollback procedure.
9. **Update persistence:** supported configuration or a complete curated package expresses policy; cache edits never do.
10. **Low prompt cost:** registry and detailed inventory data remain off-prompt and are queried only by the maintenance workflow.
11. **Secret minimization:** discovery and recovery capture only fields the plan can change. Credentials, tokens, prompt contents, and unrelated configuration are neither copied into the registry nor written into reports.

## Filesystem architecture

```text
~/.agents/skills/
  <portable-standalone-skill>/         canonical global standalone trees
  maintain-agent-skills/               user-facing workflow and deterministic driver

~/.config/agent-skill-maintenance/
  registry.json                        ownership, topology, identities, targets
  policy.json                          keep/disable/curate decisions and usage window

~/.local/state/agent-skill-maintenance/
  lock                                 single-writer run lock
  runs/<run-id>/
    plan.json                          immutable approved operations and preconditions
    journal.jsonl                      durable write-ahead operation journal
    before.json                        resolved roots, config fragments, tree manifests
    after.json                         post-application inventory and verification
    backups/                           recoverable originals for changed paths
    verification.json                  checks, evidence, and limitations

~/.local/share/agent-skill-maintenance/
  curated-plugins/<platform>/<plugin>/ complete local plugin variants, when approved
```

The config and state directories do not contain discoverable skills. The curated-plugin area contains complete plugin packages, not a second standalone skill library. Configuration and state directories use owner-only permissions. Snapshots contain only the exact non-secret fields and paths the approved plan may mutate; encountering a secret-bearing or inseparable configuration structure blocks the operation rather than copying the whole file into recovery state.

## Platform adapter strategy

| Platform | Standalone publication | Duplicate guard | Plugin ownership |
|---|---|---|---|
| Codex profiles | Use `~/.agents/skills` natively | Never repeat a shared name under `~/.codex*/skills`; profile-local skills must have unique names | Codex plugin manager/cache |
| Claude Code / CCP | For Claude Code v2.1.203 or later, create one per-skill directory link in each distinct `CLAUDE_CONFIG_DIR/skills`; older or unverified versions remain blocked | Deduplicate CCP aliases by resolved config root; include project roots for project audits; verify Claude's same-target deduplication behavior instead of assuming it | Claude plugin registry and versioned cache |
| OpenCode | Use `~/.agents/skills` natively | Use one recorded managed launch contract that sets `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`; unmanaged launch surfaces remain unsupported and are reported | OpenCode/Bun plugin manager |
| ZCode | Use its supported external-skill symlink import | Verify the imported invocation once and reject a competing native copy | ZCode plugin manager/cache or complete vendored plugin root |
| Grok | Block publication until a version-pinned probe establishes how the installed release handles the same realpath through Agents and Claude roots | If the probe does not prove one deterministic exposure, the shared-home design is unsupported for that Grok version; do not publish a fallback that recreates the collision | Grok registry, installed checkout, and bundled manifest |

Platform adapters discover roots from authoritative configuration and manifests. They never rely on a broad recursive search for directories named `skills`. Inactive versions, staging trees, fixtures, documentation, and caches not selected by the active registry are excluded from effective visibility, though storage audits may report them separately.

Project-local roots participate in inventory and collision analysis for the selected working directory. Project-local publication and global promotion are deferred from the first implementation and require a later design.

## Registry model

The normalized registry records, at minimum:

- Platform, tool version, profile/account, config root, and working-directory scope.
- Discovery-root identifier, precedence, source of authority, and configuration hash.
- Lexical skill path, `SKILL.md` path, immediate link target, fully resolved realpath, device/inode, and broken-link state.
- Raw frontmatter name, normalized name, directory fallback name, plugin namespace, and effective invocation name.
- Ownership class, source manager, plugin/marketplace identifier, active version/commit, enabled state, and authoritative-selection evidence.
- `SKILL.md` SHA-256 and canonical whole-tree SHA-256.
- Tree manifest entries: relative path, type, mode/executable bit, size, file hash, symlink text, ownership, supported macOS flags/xattrs/ACL metadata, and hard-link identity.
- A versioned declarative dependency and execution-context contract: entrypoints, internal paths, cross-skill logical identities and invocation names, approved digest/version compatibility constraints, executables, interpreter/runtime constraints, working directory, environment-variable bindings, stable external paths, and plugin-root coupling. Each environment binding records required presence, sensitivity, provider/source, target binding, and a safe validation method—never a secret value.
- Target policy, projection method, usage evidence, cleanup decision, and last verification.
- Discovery-evidence level for each consumer: native machine-readable inventory, isolated invocation, manual UI confirmation, or static graph simulation.
- Scan timestamp, excluded roots, unreadable paths, and tool/configuration versions.

The registry is regenerated from sources of truth. Hand-edited policy is stored separately so a refresh cannot erase user decisions.

### Versioned tree-manifest digest

`tree-manifest-v1` uses one canonical JSON Lines serialization with fixed key order, LF line endings, and no insignificant whitespace. Eligible relative paths must be valid UTF-8 normalized to NFC, contain no `..` segment, and are sorted by their UTF-8 byte sequence. Each entry records the schema-defined fields for its type; file contents and supported metadata values are SHA-256 hashed, symlink text is recorded without dereferencing, and hard-linked entries share a stable manifest-local identity. Directories, files, and links are explicit entries. Unsupported file types, invalid path encodings, or functionality-relevant metadata the current user cannot capture and restore block migration.

The whole-tree digest is SHA-256 over the exact `tree-manifest-v1` byte stream. The implementation must ship test vectors so independent runs produce the same digest. A future manifest schema produces a different versioned digest and cannot be compared silently with v1.

## User-facing command surface

The `maintain-agent-skills` skill delegates to a deterministic driver with these operations:

| Command | Behavior |
|---|---|
| `audit` | Read-only discovery, normalization, usage evidence, dependency checks, duplicate classification, and projected context cost; persist a read-only audit snapshot |
| `publish <skill>` | Validate a staged standalone skill and create an immutable publication plan; never mutate live discovery directly |
| `propose <audit-id>` | Consume a current audit snapshot and create an immutable reorganization or cleanup plan without changing live state |
| `apply <plan-id>` | Revalidate preconditions and apply only the exact approved plan |
| `verify` | Check tree integrity, dependencies, platform discovery, functional probes, duplicates, and policy state |
| `refresh` | Re-resolve active versions and detect drift after tool/plugin/marketplace updates |
| `status` | Summarize inventory, outstanding conflicts, policies, and prior runs |
| `rollback <run-id>` | Restore the recorded manifest-equivalent pre-run state only when current targets still match `after.json`; otherwise preserve drift and stop conflicted |

`apply` never accepts an implicit latest plan. A plan is content-addressed and includes input configuration hashes; any intervening change makes it stale and forces a new proposal.

## Core workflows

### Audit and proposal

1. Re-resolve active manager/tool state, then acquire a read-only inventory snapshot without following arbitrary cache history.
2. Resolve platform versions, profiles, authoritative plugin selections, and discovery graphs.
3. Normalize identities and compute full-tree manifests.
4. Collect only invocation-event metadata from the preceding 30 days where logs permit it. Never persist prompt, response, or transcript content in the registry, audit report, or recovery state.
5. Report manual user invocation, main-agent automatic invocation, and subagent invocation separately.
6. Classify no-evidence results as `unknown`, never automatically as unused.
7. Classify duplicates as same-realpath exposure, identical independent copy, divergent same-name content, or namespace collision.
8. Calculate projected always-on metadata/context savings using tool-native cost output when available and a clearly labeled estimate otherwise.
9. Persist the audit report and its input digest. `audit` stops here.

`propose <audit-id>` consumes a still-current audit snapshot, records the requested keep/disable/curate/migrate decisions, and emits the immutable plan and approval digest. If manager state or any input digest changed, the audit is stale and must be rerun.

### Publishing or updating a standalone skill

1. Create and validate the complete skill in a non-discoverable staging directory outside every `skills/` root.
2. Require portable `name` and `description` metadata; treat platform-specific metadata as optional adapter behavior, not a reason to fork the core instructions silently.
3. Define global scope and an explicit target set. Reject project-local publication in the first implementation.
4. Scan every target consumer's full discovery graph and simulate the complete switch before writing.
5. Block any effective invocation collision or unresolved dependency.
6. Emit an immutable publication plan. `publish` stops here.
7. After approval, `apply <plan-id>` snapshots the canonical destination, every old exposure, and each exact non-secret configuration fragment.
8. Execute a journaled per-consumer switch batch: withdraw competing old exposures, atomically place the canonical tree, then create only necessary per-skill projections using relative links where supported.
9. Apply any required discovery-graph guard, such as the recorded OpenCode launch contract, and require affected consumers to restart/reload.
10. Verify discovery and every declared safe functional probe from each final lexical exposure.
11. Record hashes, link targets, discovery-evidence levels, results, and restart/reload completion.

An existing canonical tree is replaced only by an approved, journaled `apply <plan-id>` after staging, snapshotting, and preflight. Once that switch occurs, link-based consumers observe the update immediately. The pipeline still runs `verify` so a changed dependency or frontmatter contract cannot silently break another platform. Materialized fallback projections are rebuilt atomically from the new manifest.

### Adopting or migrating an existing standalone skill

Migration uses `copy -> verify -> switch -> retain`:

1. **Freeze and inventory:** identify every candidate copy, dependency, projection, and active consumer. Do not select a canonical copy by timestamp alone.
2. **Resolve divergence:** byte-identical copies may be proposed for consolidation. Divergent copies block until the user chooses or requests an explicit merge.
3. **Manifest the complete source:** record every file, directory, mode, executable bit, symlink, and hash.
4. **Declare dependencies and execution context:** create a versioned contract covering every supported entrypoint, internal path, runtime/interpreter, working directory, non-secret environment-variable binding metadata, cross-skill logical identity/invocation/digest constraints, executable, and stable external helper. Static analysis proposes and validates this contract; it does not claim to discover dynamic dependency closure completely.
5. **Plan writer-authority transfer and classify coupling:** prove that the previous updater can be retargeted, disabled, or uninstalled, but do not execute that change yet. If the transfer mechanism cannot be proven, do not adopt. If functionality depends on hooks, agents, MCP servers, binaries, or files outside a standalone skill tree, keep it with its plugin/package or migrate the complete dependency group under a separately approved design.
6. **Stage a copy:** copy the whole tree into a same-filesystem staging directory without rewriting references or dereferencing symlinks blindly.
7. **Verify the staged tree:** compare versioned manifests, validate frontmatter, check links, run existing tests, and run a safe probe for every declared entrypoint and helper class under the recorded execution context.
8. **Transfer, publish, and switch:** after staged verification passes, use a write-ahead journal to retarget/disable/uninstall the previous updater, recheck the simulated graph, and perform a per-consumer switch batch. Individual renames are atomic; the multi-path batch is crash-recoverable, not globally atomic.
9. **Retain originals:** move originals into the run recovery bundle. Do not delete recovery copies automatically.
10. **Verify behavior:** from each final lexical exposure, confirm invocation identity, supporting resources, executable behavior, and representative end-to-end skill use under the declared execution context.

A skill without a reviewed dependency/execution contract and required functional probes remains in place. It may be inventoried and planned, but it is not declared safely migrated. The guarantee is limited to the declared and verified behavior; if the behavior cannot be bounded credibly, migration is blocked.

### Cleaning unused standalone skills

1. Present usage evidence and confidence to the user.
2. Prefer disabling/hiding through supported platform policy when that preserves provenance.
3. For user-owned standalone skills requiring physical removal from discovery, move the whole tree into the recovery bundle and record the original path; never delete it during the initial cleanup.
4. Re-scan all affected consumers and measure the actual metadata/context change.
5. Preserve the canonical tree when only one platform is being excluded; adjust target policy and remove only that platform's projection.

### Cleaning plugin skills

1. Treat the active plugin root as the minimum ownership unit until dependency analysis proves otherwise.
2. Prefer supported whole-plugin disablement for wholly unused plugins.
3. Do not assume ordinary standalone skill overrides affect plugin skills.
4. For a mixed-use plugin, create a complete curated local plugin package only after approval.
5. Copy required plugin metadata, hooks, agents, MCP/LSP declarations, executables, shared resources, selected skill trees, and all transitive dependencies.
6. Disable the upstream plugin for that consumer before enabling the curated package, preventing duplicate namespace exposure.
7. Pin the upstream version/commit and record a reproducible derivation manifest.
8. Register and install the curated package only through a named platform adapter with an explicit upstream-disable, local-install, reload, namespace-verification, update, and rollback transaction.
9. Preserve upstream license/provenance requirements and verify that every runtime dependency is either bundled or declared.
10. After upstream updates, `refresh` reports changed inputs and requires review before rebuilding the curated package.

The pipeline never edits a manager-owned cache to remove a skill. This prevents package refresh from silently restoring an apparently disabled component.

The first implementation supports curated-package mutation only for default CCP Pro after its Claude adapter passes isolated update/reinstall tests. Other managers remain inventory-only or use supported whole-plugin enable/disable controls until a named curation adapter is designed and verified.

### Refresh after updates

1. Re-resolve tool versions, discovery roots, active plugin registries, versions, and commits. Every maintenance command performs this refresh preflight; protection is not continuous between commands.
2. Compare configuration and source hashes to the last verified state.
3. Detect new skills, removed skills, changed descriptions, changed dependency edges, restored projections, broken links, or policy drift.
4. Preserve user policy and produce a new proposal; do not reapply an old plan to changed inputs.
5. Rebuild a curated plugin only from its pinned/reviewed upstream version.
6. Verify that disabled plugins remain disabled and each invocation remains unique.

## Dependency-preserving migration contract

A release-blocking requirement governs every reorganization: do not migrate a skill unless its declared behavior and helpers remain functional from every final exposure.

Before a skill can migrate, the pipeline must establish:

- The complete skill tree is copied, including `scripts/`, `references/`, `assets/`, tests, metadata, hidden files required at runtime, and executable permissions.
- Every symlink is classified. Internal relative links must resolve within the staged tree. Stable external links must be recorded and tested. Broken, cyclic, cache-version, or manager-owned external links block migration.
- A reviewed declarative dependency/execution contract exists. Static reference analysis is evidence for that contract, not proof that dynamic imports, `PATH` lookups, conditional branches, shell initialization, or runtime configuration have all been discovered.
- Relative references from `SKILL.md`, scripts, manifests, and configuration still resolve after staging under both lexical-path and realpath behavior used by the target.
- Cross-skill calls are explicit dependency edges. The target must match the recorded logical identity, effective invocation name, and approved digest/version compatibility constraint, or the migration group must include it.
- Platform-specific environment variables and root placeholders are preserved or adapted deliberately. For each required variable, verify presence and the recorded provider-to-target binding with its safe validation method without storing or exposing the value.
- Existing tests run from the staged location. The plan also defines safe probes for each supported entrypoint and helper class, including required working directory, interpreter/runtime version, `PATH` assumptions, and environment-variable names.
- A plugin-coupled skill remains inside a complete plugin package. Apparent self-containment is not inferred from the absence of a single text reference.
- The original remains recoverable until post-switch verification passes on every selected consumer.

The driver must preserve the source tree rather than reconstructing it from parsed Markdown. Versioned full-tree manifests—not `SKILL.md` hashes alone—prove transfer integrity. Functional preservation is claimed only for the declared execution contract and passing probes; unbounded or dynamically unknowable behavior blocks migration.

## Failure handling and rollback

### Preconditions that block mutation

- Unknown or unexpected discovery/configuration root.
- Consumer/tool version outside the adapter's verified range.
- Stale plan input hash.
- Concurrent maintenance lock.
- Broken or cyclic link.
- Same invocation name with divergent content.
- Unresolved helper, cross-skill, plugin-root, or external dependency.
- Existing non-pipeline-owned destination.
- Active plugin version cannot be resolved authoritatively.
- Previous update writer cannot be retargeted, disabled, or uninstalled for adoption.
- Declarative dependency/execution contract or a required safe functional probe is absent for a migration.
- Unsupported file type, invalid path encoding, or functionality-relevant metadata cannot be captured and restored.
- A platform launch surface falls outside its recorded adapter contract.

### Atomicity

- Persist a write-ahead journal entry and fsync the journal before each mutation; record and fsync completion immediately afterward.
- Use explicit run states: `planned`, `prepared`, `applying`, `verifying`, `committed`, `rolling-back`, `rolled-back`, and `conflicted`.
- Write configuration through a temporary file, validate it, preserve supported metadata, fsync it and its parent directory, then atomically rename it.
- Stage directories on the destination filesystem and rename them into place.
- Create links at temporary names, verify their targets, then rename them into place.
- Recheck plan preconditions immediately before the first mutation.
- Treat only individual filesystem replacements as atomic. A multi-path or multi-consumer operation is a journaled sequence of idempotent steps.
- On startup, refuse new mutation while an incomplete run exists; recover it by replaying or rolling back from the last durable journal boundary.
- Stop on the first failure; do not continue to later consumers after partial failure. Fault-injection tests must cover termination between every journaled boundary.

### Rollback

Rollback first compares every current target against `after.json`. If a user, installer, tool, or another process changed any target after the run, rollback preserves the current state in a conflict bundle, marks the run `conflicted`, and stops for an explicit conflict-resolution plan. It never overwrites legitimate post-run changes merely because the earlier run once owned the path.

When current state still matches `after.json`, rollback restores only paths and exact non-secret configuration fragments owned by the recorded run. It restores contents, entry types, POSIX modes, symlink text, prior absence/presence, and the supported metadata recorded by the versioned manifest. A run is not reported as rolled back until the restored state is manifest-equivalent to its `before.json` contract and discovery has been re-verified.

Recovery bundles and conflict bundles use owner-only permissions and are retained until an explicit, separately approved pruning operation. The initial implementation does not include automatic backup deletion.

## Verification strategy

### Static validation

- Frontmatter names and directory names satisfy the portable Agent Skills subset.
- Complete tree manifests and hashes match staged/canonical sources.
- Executable bits and symlink targets are preserved.
- Relative paths and declared helper commands resolve.
- Plugin manifests reference only content present in the complete curated package.

### Discovery validation

- Each consumer lists the intended skill exactly once.
- A project working directory does not introduce an unreported collision.
- Disabled skills are absent from the model-visible catalog where the platform supports hiding.
- Plugin namespaces and enabled versions match authoritative manager state.
- OpenCode does not rescan Claude's copy of shared Agents skills.

Discovery evidence is adapter-specific:

- `native-inventory`: a stable machine-readable tool command reports the skill and source.
- `isolated-invocation`: a fresh isolated process/session successfully resolves and invokes the expected skill.
- `manual-ui`: the platform exposes only a GUI/TUI confirmation, recorded as a user checkpoint.
- `static-simulation`: the pipeline's discovery-graph model predicts visibility but has not received native confirmation.

Static simulation alone cannot close publication verification. Each target needs native inventory, isolated invocation, or explicit manual UI confirmation. Tool/runtime sessions that cache skills must be reloaded or restarted before final evidence is collected; an on-disk change is not claimed to alter already-running sessions retroactively.

### Functional validation

- Run the skill's own tests when present.
- Run every declared safe helper/script probe from each final lexical canonical/projection path and its recorded execution context.
- Forward-test `maintain-agent-skills` in isolated temporary homes using realistic audit, publish, conflict, and rollback requests.
- For migrated skills, run a representative invocation that exercises supporting resources, not merely skill listing.
- Never run destructive, paid, network-heavy, or production-affecting probes without separate authorization.

### Required regression fixtures

- `xconverge`: identical duplicate across shared and profile Codex roots.
- `xreview`: same name with divergent trees.
- Multiple CCP aliases resolving to one `~/.claude` home.
- Four Codex profiles consuming one shared Agents root.
- OpenCode discovering both Agents and Claude compatibility roots.
- Managed versus unmanaged OpenCode launch surfaces and required restart.
- ZCode link import and a competing native copy.
- Grok scanning the same canonical skill through Agents and Claude roots.
- Broken, cyclic, internal, stable-external, and cache-version symlinks.
- Skill-local script, cross-skill dependency, dynamic helper declaration, execution-context constraint, and plugin-root helper dependency.
- External installer update after successful writer transfer and a blocked adoption when transfer is impossible.
- Plugin update introducing a new or restored skill.
- Unsupported metadata/file types and `tree-manifest-v1` digest test vectors.
- Process termination between every journal boundary followed by idempotent recovery.
- Post-run user/tool drift causing conflict-safe rollback refusal.

## Rollout

1. **Build and fixture-test:** implement the registry, adapters, planner, full-tree manifest, dependency analysis, and rollback entirely against temporary homes.
2. **Publish the maintenance skill pilot:** expose `maintain-agent-skills` only to the current Codex environment and default CCP Pro home, then close discovery and functional verification for both.
3. **Read-only CCP Pro pilot:** audit the shared `~/.claude` cleanup unit and present a keep/disable/curate list. Do not apply cleanup in the audit run.
4. **Standalone duplicate pilot:** exercise identical and divergent conflict handling one skill at a time. Never merge divergent variants without instruction.
5. **Plugin hygiene pilot:** start with supported whole-plugin disablement; introduce a curated package only for an approved high-yield mixed-use plugin.
6. **Fleet expansion:** cover the remaining Claude homes, four Codex profiles, ZCode, and the managed OpenCode launch contract one consumer at a time. Add Grok only if its version-pinned overlapping-root probe proves deterministic single exposure; otherwise report it as unsupported rather than weakening the uniqueness invariant.
7. **Periodic maintenance:** run `refresh` after tool/plugin updates and a 30-day `audit` when the user requests cleanup.

Each stage has its own run ID and rollback boundary. A later stage does not begin while an earlier stage has unresolved verification failures.

## Success criteria

- `~/.agents/skills` is the sole physical global home for user-owned or explicitly adopted portable standalone skills managed by this pipeline.
- `maintain-agent-skills` is discoverable exactly once on every selected consumer.
- Publishing or updating a canonical skill requires no manual multi-root copying.
- The pipeline detects both current `xconverge` and `xreview` collision classes before mutation.
- Migrated skills retain manifest-equivalent complete trees and pass every declared dependency, execution-context, entrypoint, helper, and representative functional probe from each final exposure.
- Plugin managers remain sole writers of plugin/bundled caches.
- Every maintenance command and explicit `refresh` detects plugin/update drift against policy; no continuous protection is claimed between commands.
- No no-evidence skill is disabled without explicit user approval.
- Before/after results show the actual model-visible skill set and a measured context-cost change where native output exists, otherwise a clearly labeled estimate.
- Every applied run either restores its manifest-equivalent prior state when targets still match `after.json`, or preserves later drift and stops `conflicted` for a separate resolution plan. It can also recover from interruption at every journal boundary and re-verify discovery.
- No Google Antigravity paths, profiles, or policies are included.

## Authoritative references

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugin cache and file resolution](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)
- [Claude Code marketplaces and plugin seeds](https://code.claude.com/docs/en/plugin-marketplaces)
- [Codex standalone skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills)
- [Codex plugin structure and cache](https://learn.chatgpt.com/docs/build-plugins)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills/)
- [OpenCode Claude compatibility controls](https://opencode.ai/docs/rules/)
- [ZCode skills and symlink import](https://zcode.z.ai/en/docs/skill)
- [ZCode plugins](https://zcode.z.ai/en/docs/plugin)
- [Grok skills, plugins, and marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces)

Local implementation precedents to reuse carefully:

- `~/.agents/skills/sync-gsd-fleet/`: fleet discovery, dry-run, backup, and verification patterns.
- `~/.agents/.skill-lock.json`: upstream provenance and folder-hash pattern.
- `~/.codex/AGENTS.md`: shared Codex skill placement and duplicate-prevention policy.

The new system must not inherit `sync-gsd-fleet`'s copy-everywhere behavior, `xreview`'s any-root-can-be-source model, or validators that hash only selected files.
