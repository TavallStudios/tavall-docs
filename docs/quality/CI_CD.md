# Tavall Studios CI/CD

> **Status:** Active
> **Authority:** Binding for Tavall Continuous Integration, Continuous Delivery, validation evidence, artifact promotion, and CI execution boundaries
> **Applies to:** All Tavall repositories, contributors, automation, AI-assisted development, CI callers, and deployment workflows

This document defines the required CI/CD architecture for Tavall projects.

[Git workflow and staging ancestry](GIT_WORKFLOW.md) remain owned by `GIT_WORKFLOW.md`. Repository and system documentation may define stricter validation or deployment requirements, but they may not create a competing CI/CD authority or silently weaken exact-source, evidence, or promotion requirements.

## Purpose

Tavall CI/CD exists to make the path from source to production explicit, reproducible, and attributable.

The goals are:

- Exact-source validation.
- Repository-owned build and test definitions.
- Tavall-owned execution.
- Typed and durable evidence.
- Immutable artifacts.
- Production-equivalent staging.
- Explicit production authorization.
- Safe promotion and rollback.
- Clear ownership between GitHub, Tavall CI, Tavall Cloud, and individual repositories.

A green icon beside a commit is not the architecture. It is a user interface representing evidence that must exist somewhere substantially less decorative.

## Ownership

CI/CD responsibilities are intentionally separated.

### Tavall CI

`TavallStudios/tavall-ci` owns reusable CI/CD semantics.

Tavall CI owns:

- CI orchestration.
- Repository CI-definition parsing and planning.
- Exact-source candidate composition.
- Cross-repository source aggregation.
- Source, release, build-policy, and dependency-resolution identities.
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

### Repository

Each repository owns its actual build and test graph.

Examples include:

- Gradle tasks.
- Test suites.
- Integration tests.
- Runtime acceptance scripts.
- Repository-specific verification.
- Required architecture checks.

Tavall CI orchestrates those definitions. It does not maintain a second hard-coded version of every repository's build.

### Gradle and Build Tools

Gradle ownership follows the same boundary:

- The repository owns `settings.gradle(.kts)`, `build.gradle(.kts)`, project topology, dependency intent, lockfiles, version catalogs, and repository-specific tasks.
- Tavall CI owns approved build policy, exact-source composition, typed Gradle planning, build-platform identity, resolution evidence, and artifact identity.
- The Tavall Cloud Executor owns execution placement, Java and Gradle provisioning, filesystem isolation, and cache access.

Java 25 is the Tavall default. Gradle repositories use the standard committed Wrapper and the approved platform Gradle version, currently 9.6.1, through `./gradlew`. CI must not depend on a host `gradle` command or an arbitrary user Gradle home.

The Executor provides the canonical equivalent of `/tavall/workspace`, `/tavall/dependencies`, and `/tavall/shared-tools/gradle`. Commands run from the exact-source repository root. Source dependencies are materialized at exact Git identities and record repository, commit, dependency role, and source tree digest. Shared Gradle download caches may be reused; job output and operation-specific Gradle state remain isolated per execution.

Tavall internal dependency composition uses exact source builds or immutable Tavall artifacts. Maven Local, floating sibling workspaces, mutable snapshots, and GitHub Packages are not internal dependency authorities. Gradle remains a typed Tavall CI executor; shell commands remain for work that needs a repository-owned script or non-Gradle tool.

### Tavall Cloud

Tavall Cloud owns infrastructure and execution capabilities.

This includes:

- DEVELOPMENT lanes and environments.
- Exact-source materialization.
- Executors.
- Nodes.
- Sandboxing.
- Tavall Console execution.
- Storage.
- Deployment.
- Service lifecycle.
- Scaling.
- Runtime placement.
- Routing.
- Docker and Kubernetes providers.

Reusable callers access Cloud capabilities through `tavall-cloud-api`.

`tavall-cloud-api` is a generic Cloud capability boundary. It must not become another home for Tavall CI policy.

The historical `tavall-cloud-ci` and `tavall-cloud-cd` implementations are retired as CI/CD authorities.

### Tavall GitHub Bot

`TavallStudios/tavall-github-bot` owns GitHub integration.

It is responsible for:

- GitHub App authentication.
- GitHub event ingestion and normalization.
- Repository and pull-request discovery.
- Exact-head reconciliation.
- Stale-head fencing.
- Fork and foreign-head trust checks.
- Requesting CI work from Tavall CI.
- Publishing Tavall CI evidence as GitHub Checks.
- GitHub-facing reconciliation and recovery.

The GitHub Bot is not a CI scheduler.

It must not define its own build graph, dependency policy, artifact rules, promotion rules, or Cloud scheduling behavior.

### GitHub

GitHub is the authoritative surface for:

- Source control.
- Pull requests.
- Review.
- Merge history.
- GitHub events.
- Check presentation.

GitHub-hosted Actions are not Tavall's primary CI/CD compute plane.

Tavall builds, tests, architecture checks, integration tests, runtime validation, and deployment validation run on Tavall/local infrastructure unless a narrower documented exception explicitly requires another provider.

## Repository CI Definitions

Repository CI definitions live with the repository source they validate.

The standard location is:

```text
.tavallci/
└── ci.yaml
```

A `.tavallci` definition is ordinary source-controlled configuration.

It may define typed work such as:

- Gradle tasks.
- Repository verification.
- Architecture checks.
- Behavior tests.
- Integration tests.
- Runtime acceptance.
- Required aggregate checks.
- Additional tools or immutable dependencies required by the workflow.

Rules:

- CI definitions are reviewed with the source they affect.
- CI definitions use typed executors or bounded repository-owned commands.
- Tavall CI reads and validates the definition.
- Tavall CI must not require an opaque database copy to determine the repository's canonical CI graph.
- CI configuration must not silently invent missing dependencies or versions.
- Repository-specific validation remains repository-owned.
- `SYSTEM` is the default resource mode unless an explicit platform policy selects another approved mode.
- Provider metadata may identify where source events came from, but CI identities and build execution do not require GitHub APIs.

Where a repository exposes stable CI scripts such as:

```text
scripts/ci/run
scripts/ci/verify
```

they remain repository-owned execution boundaries.

## CI Dependencies and Workflow Inputs

A workflow may require more than source code.

Dependencies may include:

- Another exact-source repository.
- An immutable Tavall artifact.
- An approved released library.
- A tool.
- A test harness.
- An MCP or other bounded execution capability.
- Repository-specific workflow support.

These inputs must be declared through the repository's CI definition or another explicit typed dependency boundary.

CI dependencies must be reproducible.

Do not depend on:

- An arbitrary mutable directory.
- Whichever tool version happens to be installed first in `PATH`.
- A floating development checkout.
- An undocumented agent state.
- A stale executor workspace left over from another job.

Reusable workflows and workflow dependencies may be distributed and hosted independently, but executions must resolve their exact required inputs before becoming valid evidence.

For Gradle composites, Tavall CI includes only resolved exact-source builds and applies declared module substitutions. A candidate never includes a neighboring directory just because it is present on an Executor.

## Exact Source

Authoritative CI is bound to immutable source.

At minimum, an execution must identify:

```text
repository
exact Git SHA
CI definition
execution profile
execution origin
```

A source-head change creates a new CI identity.

Evidence from one source revision must not be reused for another revision.

For GitHub-triggered work:

1. The GitHub Bot resolves the exact pull-request or branch head.
2. Tavall CI accepts work for that exact source.
3. The execution provider materializes that exact source.
4. Repository validation verifies the source fence before meaningful execution.
5. GitHub publication verifies that the result still belongs to the current source.

Stale source fails closed.

Do not run tests against one commit and publish success against another because both commits looked emotionally similar.

## CI Identities

Tavall CI separates identities that represent different things.

### Source Identity

The repository and exact Git revision.

```text
repository + exact Git SHA
```

### Release Identity

An explicitly approved immutable release identity.

Development source does not need a fake release number.

### Build Policy Identity

The exact Tavall build and CI policy used for the execution.

### Dependency Resolution Identity

The exact resolved dependency graph used by the build.

These identities must not be collapsed into one generic version string.

A Git SHA is not a release.

A release is not a dependency graph.

A dependency graph is not a build policy.

`SNAPSHOT` must not be used as the protocol for choosing another repository's current development source.

## Cross-Repository Validation

Tavall CI may compose several repositories into one development candidate.

Example:

```text
tavall-project-novus @ exact SHA
tavall-minecraft-framework @ exact SHA
tavall-mc-paper @ exact SHA
                |
                v
       exact CI candidate
```

Each participating repository must have one unambiguous exact source identity.

Tavall CI may use:

- Source aggregation.
- Gradle composite builds.
- Explicit dependency substitution.
- Immutable internal artifacts where source composition is not appropriate.

This allows dependent changes to be validated together without publishing fake intermediate releases.

Materialization paths are execution details. They do not define candidate identity.

Duplicate or conflicting sources for the same repository fail closed.

## Execution

Tavall CI decides what work is required.

Tavall Cloud decides where authorized work executes.

The normal boundary is:

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
repository CI graph
```

Executors may provide capabilities such as:

- Java.
- Gradle.
- Docker.
- Testcontainers.
- Node.
- Native system tools.
- Private artifact access.
- Repository-specific testing tools.

Executors belong to their environment and execution lineage.

Completed executor work, metadata, logs, and evidence must remain attributable to the environment, lane, source, and job that produced them.

An executor is not a random temporary folder with a CPU attached.

## CI Origins

CI may be requested through multiple trusted surfaces.

Examples include:

```text
github-bot
chatgpt
codex
manual
scheduler
```

These are execution origins, not separate CI systems.

Every origin uses the same CI semantics.

An origin must not redefine:

- Source identity.
- Repository CI policy.
- Artifact identity.
- Required checks.
- Promotion policy.

Trusted development tools may also have stronger raw execution capabilities, but arbitrary console execution is not automatically CI evidence.

## Architecture Tests

Canonical Tavall Architecture Tests are part of the required validation graph where applicable.

Architecture Tests must inspect the real production classes and source roots of the repository being validated.

Do not:

- Copy architecture rules into each repository.
- Test a fake replacement implementation.
- Treat the presence of architecture-test source files as proof that architecture tests ran.
- Replace canonical architecture validation with repository-specific approximations.

The canonical implementation belongs to `TavallStudios/Tavall-Architecture-Tests`.

Tavall CI orchestrates it against the source actually being built.

## Evidence

CI success requires evidence of what actually ran.

Evidence should identify, where applicable:

- Repository.
- Exact source SHA.
- Cross-repository candidate identity.
- CI definition.
- Build-policy identity.
- Dependency-resolution identity.
- Java version.
- Gradle version.
- Commands or tasks executed.
- Typed checks.
- Check results.
- Artifact digests.
- Executor identity.
- Environment identity.
- Runtime identity.
- Durable log or storage references.
- Final result and failure classification.

Infrastructure failure is not source failure.

A missing dependency is not a failed unit test.

A timeout is not a compilation error.

A stale source is not a successful execution.

Failure classification must preserve those distinctions.

## GitHub Checks

GitHub Checks present Tavall CI evidence.

They do not replace it.

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

PR bookkeeping and automated review are not executable CI Checks.

AI review may contribute review evidence. It does not become a human approval merely because a model used serious punctuation.

## Immutable Artifacts

Artifacts intended for delivery must be immutable.

An artifact identity binds the built output to its source and evidence.

At minimum, promoted artifact evidence must make it possible to determine:

```text
source
artifact
artifact digest
CI evidence
```

Changing the bytes produces a different artifact.

STAGING and PRODUCTION should consume the immutable artifact validated by CI.

Do not independently rebuild the source for every environment and then assume the outputs are equivalent.

The desired relationship is:

```text
validated artifact
      |
      +--> STAGING
      |
      +--> PRODUCTION
```

not:

```text
source
  |
  +--> rebuild A
  +--> rebuild B
  +--> rebuild C
```

Build once, identify it, validate it, and promote that identity.

## Continuous Delivery

Continuous Delivery begins with an already validated candidate.

Tavall CI owns delivery and promotion semantics.

A delivery candidate should bind:

- Exact source.
- Build identity.
- Immutable artifact.
- Artifact digest.
- Required CI evidence.
- Deployment target.
- Validation requirements.
- Rollback requirements.

Deployment intent belongs to a deployable logical service/runtime template in Tavall Cloud's existing service template registry. The source repository does not own `.tavallcd`; a repository may produce no service, one service, or several independently deployed runtimes. Pure libraries therefore need no CD definition.

The canonical service/runtime template leaf is `templates/services/<service-id>/`, with `.tavallcd/cd.yaml` attached to the template. It binds the logical `serviceId`, a distinct `runtimeId`, artifact selector, required CI checks, allowed environments, readiness requirement, promotion gates, rollback expectation, runtime flags, and production traffic mode. Provider-specific deployment configuration remains beneath Tavall Cloud CONTROL.

Tavall CI freezes the `.tavallcd` template identity and configuration digest into the delivery bundle alongside exact source identity, CI evidence, build-platform and dependency identity, and immutable artifact digest. Tavall Cloud carries that bundle through deployment generation, environment, runtime instance, readiness, promotion, and rollback evidence. A filesystem path or GitHub pull-request state is not release identity.

The deployment path remains the existing Tavall service flow through `tavall service deploy` and CONTROL. DEVELOPMENT and STAGING consume the frozen artifact and template configuration. PRODUCTION A/B uses two runtime slots beneath one stable logical service identity.

Production-relevant changes create a new delivery identity and invalidate authorization that no longer represents the candidate.

Tavall Cloud performs the authorized infrastructure operation.

It does not decide that an unvalidated candidate has somehow become production-ready.

## Development, Staging, and Production

### DEVELOPMENT

DEVELOPMENT is the normal engineering execution surface.

It may use:

- Exact-source workspaces.
- Cross-repository source composition.
- Environment executors.
- Development services.
- Integration infrastructure.
- Production-shaped test environments.

Tests that can mutate user or player data must use appropriately isolated or protected data boundaries.

### STAGING

STAGING validates production-equivalent artifacts and behavior.

Staging should use the immutable candidate intended for production rather than independently rebuilding its source.

Required checks depend on the system but may include:

- Startup.
- Readiness.
- Architecture.
- Integration.
- Persistence.
- Runtime behavior.
- Deployment.
- Networking.
- Upgrade behavior.
- Rollback behavior.

A development test passing does not prove the production-shaped deployment path works.

### PRODUCTION

PRODUCTION receives an explicitly authorized candidate.

These are separate events:

```text
merge to main
CI success
artifact creation
staging success
production authorization
production deployment
```

One does not imply all the others.

`main` is production source truth. Reaching `main` does not mean production services have already been changed.

## Staging Ancestry

Git and PR integration topology is defined by [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

CI must validate the actual source composition at every integration tier whose source changed.

Example:

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

A child PR passing CI does not prove that the composed Sub-Staging or repository Staging head passes.

Changed integration state requires its own exact-head evidence.

CI evidence and staging ancestry cooperate, but neither replaces the other.

## Production Authorization

Production promotion requires accountable authorization.

Authorization must identify the exact candidate being promoted.

A changed artifact, source revision, delivery definition, or invalidated required check requires new authorization when the previous authorization no longer represents the candidate.

Automation may:

- Prepare a candidate.
- Run validation.
- Produce evidence.
- Deploy to staging.
- Prepare promotion.

Automation must not invent human production approval.

## Deployment and Runtime Ownership

Tavall Cloud owns deployment mechanics and resulting runtime state.

This includes:

- Artifact materialization.
- Service placement.
- Service process lifecycle.
- Blue/green or A/B runtime handling.
- Health observation.
- Runtime routing.
- Degradation handling.
- Infrastructure failover.
- Rollback execution.

Tavall CI owns whether a candidate is valid and authorized for promotion.

Cloud owns whether and how that candidate is actually running.

Requested deployment state is not sufficient evidence of successful deployment. Observed runtime state must agree.

Detailed deployment, router, storage, and service-layout behavior belongs in Tavall Cloud documentation rather than being duplicated here.

## Rollback

Rollback is part of delivery design.

A production-capable delivery path should identify:

- The known-good candidate.
- The artifact to restore.
- Compatibility requirements.
- Required readiness validation.
- State or migration restrictions.
- Conditions where automatic rollback is unsafe.

Rollback does not mean blindly reversing databases or persistent state.

Application, data, and infrastructure rollback may have different safety rules.

## GitHub Actions

GitHub Actions may be used as a bounded integration or adapter where needed.

It must not become the hidden primary Tavall CI/CD implementation.

Do not move Tavall builds, integration tests, architecture validation, or deployment authority into hosted Actions merely because a YAML file can technically run them.

The primary Tavall execution plane remains Tavall/local infrastructure.

GitHub remains the SCM, review, event, and status surface.

## Validation Rules

Before CI evidence is accepted:

- The source identity must match the requested source.
- Required dependencies must resolve explicitly.
- The CI definition must be valid.
- The selected executor must satisfy required capabilities.
- Required repository checks must actually execute.
- Required Architecture Tests must run against production source.
- Evidence must identify the execution that produced it.
- Artifact hashes must correspond to the produced artifacts.
- A stale source must invalidate acceptance.
- Provider or infrastructure failure must not be reported as source success or source failure.
- Integration tiers must be validated after their composition changes.
- Deployment acceptance must verify observed state, not merely requested state.

## Anti-Patterns

### GitHub Actions as the CI Platform

Bad:

```text
GitHub PR
   |
   v
GitHub Actions
   |
   +--> build
   +--> integration tests
   +--> architecture tests
   +--> deployment
```

Why?

It moves Tavall execution authority back into an external hosted CI plane and bypasses the infrastructure built to perform that work.

GitHub should request and display CI, not secretly become CI.

### CI Policy in Tavall Cloud

Bad:

```text
Tavall Cloud
  -> decides required tests
  -> defines CI check semantics
  -> defines artifact promotion
```

Why?

Cloud is the infrastructure provider.

Making it own CI policy recreates the retired Cloud CI/CD architecture under a new class name, which is an impressively expensive way to return to where we started.

### Hard-Coded Repository Build Graph

Bad:

```text
Tavall CI:
if repo == "tavall-mc":
    run these twelve Gradle tasks
```

Why?

The repository owns its build graph.

CI should read the repository's current definition instead of requiring central code changes whenever the repository changes its tests.

### Stale Evidence

Bad:

```text
PR SHA A passed
PR moved to SHA B
publish SHA A result as current
```

Why?

The tested source no longer matches the reviewed source.

The result is stale.

### Rebuilding During Promotion

Bad:

```text
CI build
STAGING rebuild
PRODUCTION rebuild
```

Why?

Each rebuild may produce different bytes or dependency resolution.

Promote the immutable validated artifact instead.

### Floating Development Dependencies

Bad:

```text
dependency = latest SNAPSHOT
```

Why?

There is no exact source identity.

Use an exact source candidate or an approved immutable release.

## Final Rules Summary

- `tavall-docs` owns organization-wide CI/CD policy.
- `tavall-ci` owns reusable CI/CD semantics.
- Repositories own their CI definitions and build/test graphs.
- Tavall Cloud owns execution, deployment, storage, placement, routing, and runtime infrastructure.
- `tavall-cloud-api` is the generic boundary between CI and Cloud capabilities.
- Tavall GitHub Bot owns GitHub events, exact-head reconciliation, and Check publication.
- GitHub-hosted Actions are not Tavall's primary CI compute plane.
- CI definitions are source-controlled under `.tavallci`.
- CI is exact-source fenced.
- Cross-repository development uses exact-source composition, not floating `SNAPSHOT` selection.
- Architecture Tests run against the real production source.
- Evidence records what actually ran.
- Infrastructure failure and source failure remain distinct.
- Delivery uses immutable artifacts.
- STAGING validates the candidate intended for production.
- Production requires accountable authorization.
- Merge, CI success, artifact creation, staging, authorization, and deployment remain separate states.
- Every changed staging composition receives its own exact-head validation.
