# Tavall Studios CI/CD

> **Status:** Active
> **Document Type:** Technical / Organization Policy
> **Authority:** Binding for Tavall Continuous Integration, Continuous Delivery, validation evidence, artifact promotion, and CI execution boundaries
> **Applies to:** All Tavall repositories, modules, contributors, automation, AI-assisted development, CI callers, and deployment workflows
> **Notion Counterpart:** [Tavall Studios CI/CD](https://app.notion.com/p/3e838458ddfd81c9aee9f9240c86b231)
> **Versioning Authority:** [VERSIONING.md](VERSIONING.md)

This document defines the organization-wide CI/CD contract. Repository and module documentation may specialize it, but may not silently weaken exact-source, evidence, module-local CI-definition, artifact, staging, or promotion requirements.

[Git workflow and staging ancestry](GIT_WORKFLOW.md) remain owned by `GIT_WORKFLOW.md`. Version numbering, identity, artifact channels, and release identity remain owned by `VERSIONING.md`.

## Purpose

Tavall CI/CD exists to make the path from source to production explicit, reproducible, attributable, and impossible to fake merely by leaving a green icon somewhere visible.

The required properties are:

- Exact-source validation.
- Module-owned and repository-owned build/test definitions.
- Tavall-owned execution.
- Typed durable evidence.
- Explicit version/build/dependency identity.
- Immutable artifacts.
- Production-equivalent staging.
- Explicit production authorization.
- Safe promotion and rollback.
- Clear ownership between Tavall CI, Tavall Cloud, GitHub, repositories, and modules.

## Ownership

### Tavall CI

`TavallStudios/tavall-ci` owns reusable CI/CD semantics.

Tavall CI owns:

- CI orchestration.
- `.tavallci` definition parsing, validation, mutation, and planning.
- Exact-source candidate composition.
- Cross-repository source aggregation.
- Source, build-policy, dependency-resolution, artifact, channel, and release identity semantics.
- Dependency validation.
- Build orchestration.
- Typed CI checks.
- Failure classification.
- Architecture-test orchestration.
- CI evidence.
- Immutable artifact identity and publication.
- Delivery validation.
- Production authorization state.
- Promotion policy.
- Rollback policy.

Tavall CI does not own node placement, service processes, Docker, Kubernetes, runtime routing, infrastructure storage, or Cloud scheduling.

### Repositories and Modules

Repositories own their aggregate build/test topology. Modules own the build/test definition for the source they contain.

**Every Tavall source/build module ships its own `.tavallci/` directory with a canonical `.tavallci/ci.yaml`.**

A repository root may additionally ship `.tavallci/` for repository-wide and aggregate validation. The root definition does not replace module-local CI ownership.

Examples of module-owned validation include:

- Gradle tasks.
- Unit and behavior tests.
- Integration tests.
- Runtime acceptance.
- Required Architecture Tests.
- Module-specific verification.
- Bounded module-owned scripts.

Tavall CI orchestrates those definitions. It does not maintain a second hard-coded build graph for every module.

### Gradle and Build Tools

Gradle ownership follows the same boundary:

- Repositories/modules own `settings.gradle(.kts)`, `build.gradle(.kts)`, project topology, dependency intent, lockfiles, version catalogs, and repository-specific tasks.
- Tavall CI owns approved build policy, exact-source composition, typed Gradle planning, build-platform identity, resolution evidence, and artifact identity.
- Tavall Cloud Executors own execution placement, Java/Gradle provisioning, filesystem isolation, and cache access.

Java 25 is the Tavall default. Gradle repositories use the committed Wrapper and approved platform Gradle version through `./gradlew`; CI must not depend on whichever host `gradle` binary happened to win `PATH` roulette.

Tavall internal dependency composition uses exact source builds or immutable Tavall artifacts. Maven Local, floating sibling workspaces, mutable snapshot selection, and GitHub Packages are not silent internal dependency authorities.

### Tavall Cloud

Tavall Cloud owns infrastructure and execution capabilities:

- DEVELOPMENT lanes and environments.
- Exact-source materialization.
- Executors.
- Nodes.
- Tavall Console execution.
- Storage.
- Deployment.
- Service lifecycle.
- Scaling.
- Runtime placement.
- Routing.
- Docker/Kubernetes providers.
- Runtime recovery.

Reusable callers access Cloud capabilities through `tavall-cloud-api`.

`tavall-cloud-api` is a generic Cloud capability boundary. It must not become another home for Tavall CI policy.

### Tavall GitHub Bot

`TavallStudios/tavall-github-bot` owns GitHub integration:

- GitHub App authentication.
- GitHub event ingestion and normalization.
- Repository, branch, and pull-request discovery.
- Exact-head reconciliation.
- Stale-head fencing.
- Fork/foreign-head trust checks.
- Requesting CI work from Tavall CI.
- Publishing Tavall CI evidence as GitHub Checks.
- GitHub-facing reconciliation and recovery.

The GitHub Bot is a CI caller/evidence projector, not a CI scheduler or CI policy owner.

### GitHub

GitHub is the authoritative surface for:

- Source control.
- Pull requests.
- Review.
- Merge history.
- GitHub events.
- Check presentation.

GitHub-hosted Actions are not Tavall's primary CI/CD compute plane. Tavall builds, tests, architecture checks, integration tests, runtime validation, and deployment validation run on Tavall/local infrastructure unless a narrower documented exception requires another provider.

## Repository and Module CI Definitions

CI definitions live with the source they validate.

The canonical shape is:

```text
<repository>/
├── .tavallci/
│   └── ci.yaml
├── module-a/
│   ├── .tavallci/
│   │   ├── ci.yaml
│   │   └── scripts/
│   └── ...
├── module-b/
│   ├── .tavallci/
│   │   └── ci.yaml
│   └── ...
└── ...
```

The repository root definition is optional when no repository-wide aggregation is needed. The module definition is required for every Tavall source/build module.

A `.tavallci` definition is ordinary source-controlled configuration. It may define typed work such as:

- Gradle tasks.
- Repository or module verification.
- Architecture checks.
- Behavior tests.
- Integration tests.
- Runtime acceptance.
- Required aggregate checks.
- Additional tools.
- Immutable dependencies.
- Bounded source-controlled scripts.

### `.tavallci` Rules

- Every source/build module has `.tavallci/ci.yaml`.
- A repository root may additionally have `.tavallci/ci.yaml` for aggregate/repository checks.
- Root aggregation composes module validation; it does not erase or duplicate module-owned definitions.
- CI definitions are reviewed with the source they affect.
- Tavall CI reads and validates the definitions from the exact source candidate.
- Tavall CI must not require an opaque database copy to determine canonical CI policy.
- Missing dependencies or versions fail closed.
- Module-specific validation remains module-owned.
- CI configuration must not silently invent missing dependencies or versions.
- Provider metadata may identify where source events came from, but CI identities and execution semantics do not require GitHub APIs.
- A neighboring checkout, stale executor directory, or floating workspace is never an implicit dependency.
- Changing `.tavallci` changes source state and requires fresh exact-source evidence.

Where a module needs stable bounded scripts, they should live with its CI definition when practical:

```text
module-a/
└── .tavallci/
    ├── ci.yaml
    └── scripts/
        └── runtime-acceptance.sh
```

Repository-level entrypoints such as `scripts/ci/run` may remain when they are the deliberate aggregate/application boundary, but they must ultimately resolve the exact repository/module CI graph rather than maintain a stale copy of it.

## CI Dependencies and Workflow Inputs

A workflow may require more than source code.

Dependencies may include:

- Another exact-source repository.
- Another exact-source module.
- An immutable Tavall artifact.
- An approved released library.
- A tool.
- A test harness.
- An MCP or bounded execution capability.
- Repository-specific workflow support.

These inputs must be declared through `.tavallci` or another explicit typed dependency boundary.

CI dependencies must be reproducible. Do not depend on:

- An arbitrary mutable directory.
- Whichever tool version happens to be installed first in `PATH`.
- A floating development checkout.
- An undocumented agent state.
- A stale executor workspace left over from another job.
- A floating `SNAPSHOT` as a cross-repository source selector.

Reusable workflows may be distributed independently, but executions must resolve exact required inputs before becoming valid evidence.

For Gradle composites, Tavall CI includes only resolved exact-source builds and applies declared module substitutions. A candidate never includes a neighboring directory merely because it exists.

## Exact Source

Authoritative CI is bound to immutable source.

At minimum, an execution identifies:

```text
repository
exact Git SHA
resolved repository/module .tavallci definitions
execution profile
execution origin
```

A source-head change creates a new CI identity. Evidence from one source revision must not be reused for another.

For GitHub-triggered work:

1. GitHub Bot resolves the exact pull-request or branch head.
2. Tavall CI accepts work for that exact source.
3. The execution provider materializes that exact source.
4. Tavall CI resolves the `.tavallci` graph from that materialization.
5. Validation verifies the source fence before meaningful execution.
6. Evidence binds to that exact source and definition set.
7. GitHub publication verifies that the result still belongs to the current source.

Stale source fails closed.

## Versioning and Build Identity

The binding Tavall versioning model lives in [VERSIONING.md](VERSIONING.md).

CI/CD must preserve the distinction between:

- Source identity.
- Build-policy identity.
- Dependency-resolution identity.
- Build identity.
- Artifact version and artifact channel.
- Artifact identity/digest.
- Release identity.

These are different facts and must not be collapsed into one generic version string.

A source SHA is not a release. A release is not a dependency graph. A dependency graph is not a build policy. An artifact version string is not an artifact digest.

`SNAPSHOT` is a valid development artifact channel/version suffix. It must not be used as the protocol for choosing another repository's current development source.

## Cross-Repository Validation

Tavall CI may compose several repositories into one development candidate.

```text
tavall-project-novus @ exact SHA
tavall-minecraft-framework @ exact SHA
tavall-mc-paper @ exact SHA
                |
                v
       exact CI candidate
```

Each participating repository has one unambiguous exact source identity.

Tavall CI may use:

- Source aggregation.
- Gradle composite builds.
- Explicit dependency substitution.
- Immutable internal artifacts where source composition is not appropriate.

This validates dependent changes together without publishing fake intermediate releases. Materialization paths are execution details and do not define candidate identity. Duplicate/conflicting sources for the same repository fail closed.

## Execution

Tavall CI decides what work is required. Tavall Cloud decides where authorized work executes.

```text
repository / GitHub event
        |
        v
    Tavall CI
        |
        v
  tavall-cloud-api
        |
        v
 Tavall Cloud BUILD
        |
        v
 environment executor
        |
        v
 repository + module .tavallci graph
```

Executors may provide Java, Gradle, Docker, Testcontainers, Node, native tools, private artifact access, and repository/module-specific testing capabilities.

Completed executor work, metadata, logs, and evidence remain attributable to the exact source, environment, lane, executor, and job lineage that produced them.

## CI Origins

CI may be requested through trusted surfaces such as:

```text
github-bot
chatgpt
codex
manual
scheduler
```

These are execution origins, not separate CI systems. Every origin uses the same CI semantics and may not redefine source identity, repository/module CI policy, artifact identity, required checks, or promotion policy.

Arbitrary console execution is not automatically CI evidence.

## Architecture Tests

Canonical Tavall Architecture Tests are part of the required validation graph where applicable.

Architecture Tests inspect the real production classes/source roots of the repository/module being validated.

Do not:

- Copy architecture rules into each module.
- Test a fake replacement implementation.
- Treat the existence of test source as proof it ran.
- Replace canonical architecture validation with a weaker approximation.

The canonical implementation belongs to `TavallStudios/Tavall-Architecture-Tests`. Tavall CI orchestrates it against the actual candidate source.

## Evidence

CI success requires typed durable evidence identifying, where applicable:

- Repository.
- Exact source SHA.
- Cross-repository candidate identity.
- Resolved `.tavallci` definition set.
- Build-policy identity.
- Dependency-resolution identity.
- Java/Gradle versions.
- Commands/tasks executed.
- Typed checks.
- Check results.
- Artifact versions/channels/digests.
- Executor identity.
- Environment identity.
- Runtime identity.
- Durable log/storage references.
- Final result and failure classification.

Infrastructure failure is not source failure. A missing dependency is not a failed unit test. A timeout is not a compilation error. A stale source is not successful execution.

Failure classification must preserve those distinctions.

## GitHub Checks

GitHub Checks present Tavall CI evidence. They do not replace it.

Canonical check families may include:

```text
tavall-ci/dependencies
tavall-ci/architecture
tavall-ci/behavior
tavall-ci/integration
tavall-ci/runtime
tavall-ci/quality
tavall-ci/required/all
```

A GitHub-specific aggregate may be published when it represents real Tavall CI execution.

PR bookkeeping and automated review are not executable CI Checks. AI review may contribute review evidence; it does not become human approval merely because the model sounded stern.

## Immutable Artifacts

Artifacts intended for delivery are immutable.

Artifact identity binds the built output to source, version/channel, digest, storage reference, and evidence as defined by [VERSIONING.md](VERSIONING.md).

At minimum, promoted evidence makes it possible to determine:

```text
source
build identity
artifact version/channel
artifact digest
CI evidence
```

Changing the bytes creates a different artifact identity.

STAGING and PRODUCTION consume the immutable artifact validated by CI. They do not independently rebuild the source and then hope the bytes have developed a sense of professional responsibility.

```text
validated artifact
      |
      +--> STAGING
      |
      +--> PRODUCTION
```

## Continuous Delivery

Continuous Delivery begins with an already validated candidate.

Tavall CI owns delivery and promotion semantics. A delivery candidate binds:

- Exact source.
- Build identity.
- Immutable artifact identity.
- Artifact digest.
- Required CI evidence.
- Deployment target.
- Validation requirements.
- Rollback requirements.

Deployment intent belongs to deployable logical service/runtime templates in Tavall Cloud's service template registry. The source repository does not own `.tavallcd`; a repository/module may produce no service, one service, or several independently deployed runtimes. Pure libraries need no CD definition.

The service/runtime template may attach `.tavallcd/cd.yaml`, which binds service/runtime identity, artifact selector, required CI checks, allowed environments, readiness requirements, promotion gates, rollback expectations, runtime flags, and production traffic mode.

Tavall CI freezes deployment configuration identity into delivery evidence alongside exact source/build/dependency/artifact identity. Tavall Cloud carries that candidate through deployment, readiness, promotion, and rollback evidence.

## DEVELOPMENT, STAGING, and PRODUCTION

### DEVELOPMENT

DEVELOPMENT is the normal engineering execution surface. It may use exact-source workspaces, cross-repository composition, environment executors, development services, integration infrastructure, and production-shaped tests with appropriately isolated/protected data.

### STAGING

STAGING validates the production-equivalent immutable candidate intended for production. Required checks may include startup, readiness, architecture, integration, persistence, runtime behavior, deployment, networking, upgrades, and rollback.

A development test passing does not prove the production-shaped deployment path works.

### PRODUCTION

PRODUCTION receives an explicitly authorized candidate.

These are separate states:

```text
merge to main
CI success
artifact creation
staging success
production authorization
production deployment
```

One does not imply all the others. `main` is production source truth, but reaching `main` does not mean production services have already changed.

## Staging Ancestry

Git/PR integration topology is defined by [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

CI validates the actual source composition at every integration tier whose source changed.

```text
feature PR
    |
    v
Sub-Staging
    |
    v
Repository Staging
    |
    v
main
```

A child PR passing CI does not prove the composed Sub-Staging or Repository Staging head passes. Changed integration state requires its own exact-head evidence.

## Production Authorization

Production promotion requires accountable authorization naming the exact candidate being promoted.

A changed artifact, source revision, delivery definition, or invalidated required check requires new authorization when previous authorization no longer represents the candidate.

Automation may prepare candidates, run validation, produce evidence, deploy to staging, and prepare promotion. Automation must not invent human production approval.

## Deployment and Runtime Ownership

Tavall Cloud owns deployment mechanics and resulting runtime state, including artifact materialization, service placement/process lifecycle, A/B handling, health observation, routing, degradation handling, infrastructure failover, and rollback execution.

Tavall CI owns whether a candidate is valid and authorized for promotion. Requested deployment state is not evidence of successful deployment; observed runtime state must agree.

## Rollback

Production-capable delivery paths identify:

- Known-good candidate.
- Artifact to restore.
- Compatibility requirements.
- Required readiness validation.
- State/migration restrictions.
- Conditions where automatic rollback is unsafe.

Rollback does not mean blindly reversing databases or persistent state. Application, data, and infrastructure rollback may have different safety rules.

## Validation Rules

Before CI evidence is accepted:

- The source identity matches the requested source.
- Required module `.tavallci` definitions exist and are valid.
- Root aggregation, when present, resolves the module graph rather than replacing it.
- Required dependencies resolve explicitly.
- The selected executor satisfies required capabilities.
- Required checks actually execute.
- Architecture Tests run against real production source.
- Evidence identifies the execution that produced it.
- Artifact hashes correspond to produced artifacts.
- Stale source invalidates acceptance.
- Provider/infrastructure failure is not reported as source success/failure.
- Integration tiers are revalidated after composition changes.
- Deployment acceptance verifies observed state rather than requested state.

## Anti-Patterns

### Root-Only CI Definition for a Multi-Module Repository

Bad:

```text
repo/.tavallci/ci.yaml
module-a/   # no .tavallci
module-b/   # no .tavallci
```

Why?

The root becomes a second hard-coded model of module validation and module CI cannot travel independently with module source.

Good:

```text
repo/.tavallci/ci.yaml          # optional aggregate
module-a/.tavallci/ci.yaml      # required module definition
module-b/.tavallci/ci.yaml      # required module definition
```

### GitHub Actions as the CI Platform

GitHub may request/display CI, but hosted Actions must not become the hidden primary Tavall build/test/deployment authority.

### CI Policy in Tavall Cloud

Cloud is the infrastructure provider. Moving check taxonomy, build identity, or promotion policy back into Cloud recreates the retired Cloud CI/CD architecture under a new name.

### Hard-Coded Central Build Graph

Tavall CI must not require central Java changes whenever a module adds/removes a repository-owned test. The exact `.tavallci` graph is the source-controlled authority.

### Stale Evidence

Do not publish evidence from SHA A as current after the reviewed head moves to SHA B.

### Rebuilding During Promotion

Do not independently rebuild for CI, STAGING, and PRODUCTION. Promote the exact immutable artifact already validated.

### Floating Development Dependencies

Do not select `latest SNAPSHOT` as another repository's current development source. Use exact source or an approved immutable release/artifact.

## Final Rules Summary

- `tavall-docs` owns organization-wide CI/CD and versioning policy.
- `tavall-ci` owns reusable CI/CD semantics and implementation contracts.
- Every Tavall source/build module ships `.tavallci/ci.yaml`.
- Repository-root `.tavallci` may aggregate modules but cannot replace module-local definitions.
- CI definitions are source-controlled and exact-source resolved.
- CI is exact-source fenced.
- Cross-repository development uses exact-source composition, not floating snapshots.
- Tavall Cloud owns execution/deployment infrastructure, not CI policy.
- Tavall GitHub Bot owns GitHub event/head reconciliation and evidence projection, not CI scheduling policy.
- Architecture Tests inspect real production source.
- Evidence records what actually ran.
- Infrastructure failure and source failure remain distinct.
- Delivery uses immutable artifacts.
- STAGING validates the candidate intended for production.
- Production requires accountable authorization.
- Merge, CI success, artifact creation, staging, authorization, and deployment remain separate states.
- Every changed staging composition receives its own exact-head validation.

## Delegated Documents

- [VERSIONING.md](VERSIONING.md) — organization-wide source/build/artifact/release versioning and identity policy.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) — branch/PR/staging ancestry.
- `TavallStudios/tavall-ci/docs/architecture/IDENTITIES.md` — Tavall CI implementation identity model.
- `TavallStudios/tavall-ci/docs/architecture/SOURCE_AGGREGATION.md` — exact-source aggregate mechanics.
- `TavallStudios/tavall-ci/docs/architecture/EVIDENCE.md` — typed evidence contract.
- `TavallStudios/tavall-ci/docs/architecture/CD.md` — delivery/promotion implementation contract.
- `TavallStudios/tavall-ci/docs/architecture/GITHUB_BOT_INTEGRATION.md` — GitHub caller/evidence projection boundary.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `1:1` | `TavallStudios/tavall-docs/docs/quality/CI_CD.md` | 2026-09-27 2:46 PM PDT | Docs sync branch `docs/ci-versioning-notion-sync-20260927`. |
| Notion | `1:1` | `Tavall / Platform & Infrastructure / Tavall Studios CI/CD` | 2026-09-27 2:46 PM PDT | Notion counterpart `3e838458-ddfd-81c9-aee9-f9240c86b231`. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 2:46 PM PDT | GitHub + Notion | `RECONCILED` | Canonical CI/CD 1:1 pair | GitHub-only `CI_CD.md` plus split Notion CI pages | Current documentation reconciliation | Made module-local `.tavallci` ownership explicit and delegated organization-wide versioning to `VERSIONING.md`. |

</details>
