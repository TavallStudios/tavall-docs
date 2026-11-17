# Tavall Studios CI/CD

> **Status:** Active
> **Authority:** Binding for Tavall Continuous Integration, Continuous Delivery, validation evidence, artifact promotion, and CI execution boundaries
> **Applies to:** All Tavall repositories, contributors, automation, AI-assisted development, CI callers, and deployment workflows
> **NLEW authority:** [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md)
> **Versioning authority:** [VERSIONING.md](VERSIONING.md)

Tavall CI is intentionally simple. It is one Tavall CI system with one shared Gradle orchestration/composition layer. Repositories remain separate repositories and are materialized into separate workspace folders. Cross-repository development is composed from those exact-source workspaces. Containers are optional execution boundaries, not the default CI architecture.

Do not turn CI into a mandatory Node -> Lane -> Environment -> Workspace -> Executor pipeline. NLEW objects are Cloud capabilities and ownership/context objects. Tavall CI may use those capabilities where appropriate, but they are not CI stages.

## Canonical model

```text
GitHub event / Tavall CLI / operator / bot
                    |
                    v
                Tavall CI
                    |
                    v
        exact-source materialization
                    |
                    v
             CI workspace root
        +-----------+-----------+
        |           |           |
        v           v           v
      repo A      repo B      repo C
    exact SHA    exact SHA    exact SHA
        \           |           /
         \          |          /
          +---------+---------+
                    |
                    v
       one Tavall CI Gradle system
   composite builds / source substitution
                    |
                    v
        build / test / validation
                    |
                    v
          evidence + artifacts
```

The workspace diagram is logical. Physical paths are provider/materialization details and do not become repository, build, service, Lane, Environment, Workspace, or Executor identity.

## Core rules

1. Tavall has **one CI system**.
2. Tavall CI has **one Gradle orchestration/composition system** for Gradle repositories.
3. Each repository remains a normal independent Gradle repository with its own project tree.
4. Each repository participating in one candidate is materialized at an exact source identity into its **own workspace folder**.
5. Cross-repository source development uses Gradle composite builds / `includeBuild(...)` / explicit dependency substitution against those exact workspaces.
6. Repositories are not flattened into a synthetic monorepo and modules are not copied between repositories to make CI work.
7. Containers are **optional**. A job may run directly on an authorized execution provider or inside an explicitly selected supported container boundary when isolation or reproducibility requires it.
8. Container choice does not change source identity, dependency identity, build identity, workspace ownership, or artifact identity.
9. Lane, Environment, Workspace, Executor, Node, and service objects are not mandatory CI stages.
10. GitHub is source/review/event/check presentation. GitHub Actions is not Tavall CI compute.

## Ownership

### Repositories

Each repository owns its actual Gradle project:

- `settings.gradle` / `settings.gradle.kts`;
- `build.gradle` / `build.gradle.kts`;
- modules and `include(...)` topology;
- dependency intent;
- wrapper and repository-specific Gradle behavior;
- lockfiles and version catalogs where used;
- source-owned build/test tasks and scripts;
- module and repository `.tavallci` definitions.

A repository does not surrender its Gradle structure to Tavall CI.

### Tavall CI

`TavallStudios/tavall-ci` owns the shared CI system:

- parsing repository/module `.tavallci` definitions;
- resolving exact source;
- materializing one isolated repository workspace folder per exact source;
- composing cross-repository development candidates;
- the shared Gradle planning/orchestration layer;
- dependency substitution and exact-source aggregation;
- approved build/dependency policy;
- build, dependency-resolution, and artifact identities;
- typed execution planning;
- validation/evidence collection;
- immutable artifact publication;
- delivery validation, promotion policy, and rollback policy.

Tavall CI must not duplicate Tavall Cloud's node, provider, NLEW, scheduling, runtime-placement, or service-lifecycle systems.

### Tavall Cloud / execution providers

Cloud or another approved local execution provider supplies compute and capabilities requested by Tavall CI. This may include Java, Gradle runtime support, caches, native tools, networking, or optional container isolation.

The execution provider answers **where/how the planned work runs**. It does not define the CI build graph.

Lane, Node, and Executor policy may be attached when a CI task requires it. A registered service Environment is not a source/build context and must never be created to run CI.

## Verification ladder: traditional CI is the last resort

Tavall verifies a change with the cheapest rung that gives the required guarantee. Because Tavall modules own one SYSTEM, FEATURE or clearly scoped issue each, a change is verified at the module level, not the repository level. Traditional Tavall CI runs only when no earlier rung can give the guarantee.

| Rung | Command | Guarantee | Scope |
| --- | --- | --- | --- |
| L0 Compile | `tavall ci compile` | Changed module compiles with javac/JDT; public API (ABI) unchanged or the change is explicit | Every change; changed module plus direct dependents only when its ABI changed |
| L1 Architecture | `tavall ca` | Tavall architecture rules hold for every changed class (boundaries, DI, naming, anti-patterns) | Every change; compiled production classes of the changed module |
| L2 Module behaviour | `tavall-module-test --worktree <worktree> --module :<gradle-path> [--tests <filter>]` | Edge cases of that SYSTEM/FEATURE (`<Class>SimulationTest`, contract tests) | Requested module only |
| L3 Reload proof | `tavall module reload <id>` on the DEVELOPMENT runtime | Wiring, configuration, lifecycle and live routes of the reloaded generation are ready | Runtime-facing modules |
| L4 Traditional CI | Tavall CI on the affected-module graph | Composed build, immutable artifact and evidence | Only the cases below |

The canonical `tavall-module-test` executable is `/srv/dev-storage/.ai/plugins/Tavall/agents/tavall-orchestrator/tools/module-test/tavall-module-test`. It composes the exact source pins in the checkout's `.tavallci/ci.yaml`, resolves plugins and dependencies from the pinned local Maven mirror and approved local caches, and runs only the requested module's `test` task (including `compileTestJava`). It emits a typed result with test counts and the report path. Public repositories are removed from resolution; the tool does not run repository-wide `check` or traditional CI.

Merging into a staging root or working branch needs, at the exact head SHA:

- L0 compile PASS;
- the changed module's own tests (L2);
- a real end-to-end run of the change (L3: `tavall module reload` proof, or running the changed runtime, CLI command or tool as a user would);
- a PR comment that starts with `TAVALL-VERIFIED <sha7>` and lists the module tests run and the end-to-end run with its result.

Traditional CI (L4) is required only for:

- promotion of a staging root to `main` (this is where build, `.tavallci`, `.tavallcd`, dependency-lock and Gradle settings changes are fully verified);
- database migrations, SQL and security/authentication code, on any branch.

When L4 runs it builds only the affected-module graph (changed modules plus modules whose compile classpath includes a changed ABI), never the whole repository by default. Every other change is accepted on L0–L3 evidence recorded against the exact source SHA.

## Workspace model

A multi-repository candidate is laid out as separate repository workspaces under one CI run/materialization root.

Example:

```text
<ci-run-root>/
└── repos/
    ├── tavall-mc/                    # exact SHA A
    ├── tavall-minecraft-framework/   # exact SHA B
    ├── tavall-java-tools/            # exact SHA C
    └── <shared-dependency>/             # exact SHA, only when declared
```

Rules:

- one repository = one repository workspace folder;
- the folder contains that repository's normal source tree;
- exact repository + exact Git SHA is the source identity;
- workspace folder names/paths are materialization details, not source identity;
- neighboring folders are not dependencies merely because they exist;
- Tavall CI explicitly selects and wires participating repositories;
- duplicate/conflicting exact sources for the same repository fail closed;
- mutable leftovers from a previous run are not dependency authority.

A single-repository build is simply the same model with one repository workspace.

## One Gradle system

"One Gradle system" means Tavall CI has one shared Gradle planning/composition model rather than each workflow inventing a private dependency/bootstrap mechanism.

For one repository:

```text
Tavall CI
  -> repository workspace
  -> repository's normal Gradle project
  -> requested typed Gradle tasks
```

For several repositories:

```text
Tavall CI
  -> repo workspace A
  -> repo workspace B
  -> repo workspace C
  -> exact-source composite
       includeBuild(A/B/C as required)
       explicit dependency substitution
  -> requested typed Gradle tasks
```

The shared system owns cross-repository composition and resolution evidence. Each repository still owns its internal Gradle module graph.

Internal development dependencies use exact source or an explicitly selected immutable Tavall artifact. Do not use Maven Local, arbitrary sibling directories, floating mutable snapshots, or a host user's accidental Gradle state as dependency authority.

Each Gradle project keeps its own build cache and configuration cache keyed by project identity; the former unified shared cache is retired. Immutable dependency downloads (the pinned Maven mirror) may be shared read-only. Source workspaces, outputs that require isolation, and run-specific evidence remain attributable to the CI run.

## `.tavallci`

CI intent lives with source.

```text
<repository>/
├── .tavallci/ci.yaml                 # optional repository aggregate
├── module-a/.tavallci/ci.yaml        # module-owned CI
└── module-b/.tavallci/ci.yaml        # module-owned CI
```

Module CI definitions own module checks. A root definition may aggregate them but must not become a stale second copy of every module's build logic.

`.tavallci` may request typed Gradle work, source-controlled scripts, test harnesses, exact-source repository dependencies, immutable artifacts, tools, and additional approved execution capabilities.

**Temporary organization-wide policy (2026-10-28):** Do not declare the Tavall architecture-test plugin, `architectureTest` tasks, task-facing ArchUnit tools, or architecture-only `architecture`/`architecture-tests` checks. They remain suspended until the replacement suite is set up. Keep regular compilation, unit/contract/behavior, integration, runtime, quality, E2E, artifact, and Tavall CI checks that the repository owns.

This suspension changes architecture-test sources and execution entries only. Preserve any existing repository-root `.tavallci/` and `.tavallcd/` directories and their user metadata; do not remove either directory as cleanup.

A typed Gradle check may declare up to 32 `gradleProperties` string entries for its primary build. Each entry is passed as a separate `-Pname=value` argument, preserving spaces and punctuation as part of one value. Property names are bounded identifiers; values are non-empty single-line text up to 4096 characters. Shell checks cannot set Gradle properties. `includeInAll: false` keeps a named check out of the default profile while allowing an explicit request for that check.

Gradle properties do not select or replace exact source inputs. Tavall CI rejects CI-owned `org.gradle.*`, `tavallCi*`, `tavallSource*`, `tavallDependency*`, `tavallArtifact*`, and `tavallBuildPolicy*` properties. A property name supplied by exact-source version or plugin metadata is also reserved and cannot be set by a check.

## Typed execution

Gradle is a first-class typed Tavall CI execution path. Shell remains available for source-owned scripts and work that is not naturally Gradle work. Additional adapters may exist without creating separate CI systems.

The execution type describes how a planned step runs. It does not create a new source/build identity model.

## Optional containerization

Containerization is optional.

```text
CI step
├── direct/provider-native execution
└── optional selected container boundary
```

Use a container only when the task needs that isolation/runtime boundary. Do not wrap every build in a container merely because containers exist.

The exact supported container-type vocabulary belongs to the execution/provider contract. CI documentation must not invent an enum that has not been canonically defined.

Regardless of execution boundary, the candidate remains the same exact repository workspaces and the same Tavall CI build/dependency graph.

## NLEW relationship

NLEW is not the CI pipeline.

Incorrect:

```text
CI -> Lane -> Environment -> Workspace -> Executor -> build
```

Also incorrect:

```text
CI -> Lane -> Executor -> Workspace -> build
```

Correct relationship:

```text
Tavall CI plan
    |
    v
approved execution capability
    |
    +--> selects Node/placement when required
    +--> runs on the existing shared Executor by default
    +--> carries Lane policy when the source workflow requires it
    +--> materializes exact sources in an operation-scoped Workspace
    +--> may target an existing service Environment for runtime integration checks
    +--> may use an optional container boundary
```

A CI job never creates or owns a service Environment. These are execution/context choices around the CI plan, not a mandatory ordered NLEW chain.

## Exact source and cross-repository candidates

Every participating repository is identified independently:

```text
repository A + exact Git SHA A
repository B + exact Git SHA B
repository C + exact Git SHA C
```

Tavall CI records the resolved source set and dependency-resolution identity. A source-head change creates a new candidate and requires fresh evidence.

Cross-repository development should validate source together before fake intermediate releases are published.

## GitHub boundary

GitHub owns source control, pull requests, review, merge history, events, and check presentation.

Typical integration:

```text
GitHub event
  -> Tavall GitHub Bot
  -> typed Tavall CI request
  -> Tavall CI execution
  -> typed evidence
  -> GitHub Check
```

No GitHub Actions workflow/job is Tavall CI compute, scheduler, deployment runner, artifact authority, or promotion authority.

`tavall-github-runner` is a GitHub caller identity only: it submits typed exact-source requests to Tavall CI and does not host CI compute. Tavall CI uses the existing shared Tavall Cloud Executor for builds and tests; the caller identity is not a separate runner host, Executor, or GitHub Actions runtime.

Direct Tavall CLI/API/operator requests may invoke the same Tavall CI system without GitHub.

### Bounded Console execution

ChatGPT MCP Console and retained CLI/CONTROL execution entrypoints submit an authorized command process to the existing shared SYSTEM Executor. CONTROL owns orchestration and authorization; the Executor enforces configured permission identity and invocation isolation. A command is not a request to create an Executor, sandbox, namespace, container, or service Environment. When source work requires bounded materialization, an operation Workspace scopes its state/output and a Lane retains exact-source/repository authority. Those relationships remain individually optional for commands that do not materialize source; registered service Environments own deployed runtimes.

Sequential commands reuse the configured durable Executor with distinct invocation IDs. A busy/unavailable Executor returns a bounded result without provisioning fallback or elevated permissions. Process timeout/cancellation preserves the shared Executor. Nonzero command exits are command failures, separate from authorization rejection, timeout, cancellation, and unverified provider/transport failure. HOME and working-directory selection follow the authorized invocation context. Artifacts remain scoped to their source invocation.

## Evidence and artifacts

Evidence binds to the exact candidate actually executed. It should include enough identity to reconstruct:

- participating repositories and exact SHAs;
- resolved `.tavallci` definition set;
- build/dependency policy identity;
- resolved cross-repository composition;
- requested execution profile;
- execution/provider information relevant to reproducibility;
- test/validation results;
- produced artifact identities and digests.

Execution details such as a temporary host path or optional container instance are evidence/provenance, not source identity.

An immutable package release manifest records its Maven coordinates, channel, exact artifact identity/digest, and durable CI-evidence reference. The evidence must resolve to the candidate's exact source and show `REQUIRED_ALL` plus `ACCEPTED_MAIN` before `ReleaseIndex` publication. The package index resolves through Tavall's existing SHA-256 artifact store; it has no GitHub API dependency. A generated Maven file-repository view is a consumer projection over those immutable objects, not a second artifact authority or build system. The manifest remains the rollback target, and the view is regenerated from it.

## CD boundary

Module-aware deployment distinguishes immutable artifact selection, the target's versioned desired module profile, and observed runtime module state. A build module is not automatically hot-loadable; the runtime/registry must prove support for load/unload/reload and generation-safe cleanup. For the accepted SYSTEM/FEATURE split, target-specific profile composition, Paper/Velocity single-JAR constraints and host acceptance, read [Module Separation and Ownership Boundaries](code-architecture/MODULE_SEPARATION.md#7-module-aware-cicd-profiles-and-host-loading) alongside this CD policy. Pure Tavall DI module-profile resolution does not itself perform runtime mutation.

CI builds and validates immutable artifacts. CD promotes the already validated artifact rather than rebuilding a supposedly equivalent one for each target.

```text
exact source workspaces
  -> build/test
  -> immutable artifact + digest
  -> delivery validation
  -> deployment target
  -> readiness
  -> explicit promotion/authorization
```

`.tavallcd` is deployment/service-local configuration for deployable services/runtimes. It is not a required source-repository container around ordinary CI and pure libraries do not need deployment state merely to build.

When `.tavallcd/` exists, keep its directory and existing metadata during architecture-test suspension; deployment configuration ownership is unchanged.

### Deployment and Runtime Ownership

Service/Environment ownership and deployment topology are governed by Cloud/NLEW authority, not by the CI workspace layout.

## Final rules

- One Tavall CI system.
- One shared Tavall CI Gradle orchestration/composition system.
- Normal independent Gradle repositories remain normal independent Gradle repositories.
- Separate workspace folder per participating repository.
- Exact source for every repository in a candidate.
- Cross-repo development through explicit Gradle composite/source substitution or immutable artifacts.
- No synthetic monorepo requirement.
- No Maven Local or accidental sibling-workspace dependency authority.
- Containers are optional execution boundaries.
- Do not invent container enums that have not been canonically defined.
- NLEW is available to CI; NLEW is not the CI pipeline.
- GitHub Actions is not Tavall CI compute.
- Build once, record immutable identity/digest, and promote that artifact unchanged.
- Verify with the cheapest sufficient rung (L0 compile, L1 `tavall ca`, L2 module tests, L3 `tavall module reload`); traditional CI is the last resort and runs on the affected-module graph only.
- Per-project Gradle caches; no unified shared build cache.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | 2026-11-16 11:16 PM PST | [PR #155](https://github.com/TavallStudios/tavall-docs/pull/155), orchestrator lane `orchestrator/20261105/modtest-20261116`; promotion to main pending. |
| Notion | `TEMPORARY_DRIFT` | [Tavall Studios CI/CD](https://app.notion.com/p/3e838458ddfd81c9aee9f9240c86b231) | 2026-11-16 11:16 PM PST | Synced with the L2 ladder candidate in PR #155; GitHub main promotion pending. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-16 11:16 PM PST | Notion | `UPDATED` | Tavall Studios CI/CD | Existing CI/CD Notion twin | [PR #155](https://github.com/TavallStudios/tavall-docs/pull/155) | Added the exact L2 module-test command and staging verification ladder; GitHub main promotion pending. |
| 2026-11-17 01:09 AM UTC | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | Same path | [PR #155](https://github.com/TavallStudios/tavall-docs/pull/155) | L2 now names the exact `tavall-module-test` command and its module-only guarantee. |
| 2026-11-16 09:20 AM UTC | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | Same path | [Issue #131](https://github.com/TavallStudios/tavall-docs/issues/131) | Owner P0: staging merges use compile + module tests + real e2e (TAVALL-VERIFIED comment); traditional CI only at promotion to main and for migrations/SQL/security. |
| 2026-11-16 02:45 AM UTC | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | Same path | [Issue #131](https://github.com/TavallStudios/tavall-docs/issues/131) | Owner P0: verification ladder, traditional CI as last resort on the affected-module graph, per-project Gradle caches. Notion twin not updated. |
| 2026-11-14 10:26 PM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | Same path | [PR #130](https://github.com/TavallStudios/tavall-docs/pull/130) | Documented CI evidence and immutable local package publication. Notion reconciliation remains pending because the connector failed. |

</details>
