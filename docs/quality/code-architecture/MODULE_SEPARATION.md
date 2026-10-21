# Tavall Module Separation and Ownership Boundaries

> **Status:** Active
> **Authority:** Binding specialization of [Tavall Module Types](../MODULE_TYPES.md), [Code Architecture](../CODE_ARCHITECTURE.md), [DI and Orchestration](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md), and [Testing and Git](TESTING_AND_GIT.md).
> **Applies to:** New modules, repository extractions, SYSTEM/FEATURE composition, API ownership, packages, Gradle dependencies, runtime lifecycle, CI, and Tavall AI engineering-policy routing.
> **Rule:** Module classification, responsibility role, runtime owner, repository location, artifact identity, and package identity are **separate decisions**. Current checked-in producer contracts and accepted system design take precedence over illustrative trees.

## 1. Boundary Selection: Package Before Module

For each proposed split record: **capability**, current owner and consumers, non-goal, smallest viable boundary, reason a smaller boundary fails, composing parent/fan-in, runtime owner, dependency direction, and an observable end-to-end acceptance path.

Choose the lowest sufficient boundary:

1. Existing class or package when there is one cohesive owner and no independently managed lifecycle.
2. Internal component when behavior needs its own interfaces/tests but ships and operates together.
3. Separate source/build module when typed dependency enforcement, reuse, ownership, tests, independently selected provider/configuration, or lifecycle actually require it.
4. Separate repository when the module has meaningful independent change/release/ownership pressure; a repo is **not** evidence of a new runtime.
5. Independently deployed `RUNTIME` only when a separate executable/process/service lifecycle exists.
6. Platform/exposed capability only with real cross-product consumers and an owned semantic API; HTTP, CLI, MCP, or UI exposure alone does not make a platform.

Do **not** create a FEATURE simply because a domain has several classes, a storage backend exists, or a directory has a memorable name. Stateless NLEW handlers, records, policy helpers, and cohesive logic remain packages until independent enable/disable/reload, provider selection, failure isolation, configuration, or test ownership is demonstrated. Record the **future split trigger** without prebuilding it.

## 2. Six Independent Identity Axes

Every real module records the following independently in its README and module-scoped Progression:

| Axis | Required answer | Non-equivalence |
| --- | --- | --- |
| Primary type | One of `RUNTIME`, `APPLICATION`, `SYSTEM`, `FEATURE`, `API`, `TOOLING`, `TEST_SUITE` | `LIBRARY`/`PROVIDER`/`ADAPTER`/`INTEGRATION` are secondary roles, not primary types |
| Secondary roles | Zero or more actual roles | A `PROVIDER` role does not imply its own process |
| Runtime owner | `Self`, a named runtime module, or `None` | `SYSTEM`/`FEATURE` does not imply `RUNTIME` |
| Composition owner | Parent SYSTEM or actual consumer/aggregator; child FEATURES where they exist | A source tree root is not automatically a SYSTEM |
| Contract owner | Which producer/runtime owns each typed API and its compatibility | Importing an API does not transfer ownership |
| Artifact/repository/package | Gradle/artifact name, owning repo, Java package root | Moving to another repo does not grant new domain authority |

A `SYSTEM` owns aggregation, fan-in, lifecycle coordination and an explicit consumer-facing capability surface. A `FEATURE` is an independently controllable child where independently controlled behavior has been justified. `RUNTIME` owns its executable lifecycle, host registration, deployment and APIs exposed by that runtime. A runtime-neutral API is owned by the domain producer/system that defines it, not automatically by the first FEATURE or adapter to import it. A `TEST_SUITE` verifies production modules but is not another implementation owner.

Each source/build module has its own `.tavallci/ci.yaml` and one module-scoped `PROGRESSION` document; SYSTEM-level Progression aggregates, but never replaces, child module evidence. Do not infer deployed state from a design diagram or the presence of a module folder.

## 3. Contracts and Dependency Direction

Write and inspect a dependency graph **before** moving code. The default direction is consumer/feature/adapter → stable typed API → selected implementation through Tavall DI and the canonical module registry. No consumer should need the implementation module's internals.

- Use Tavall's existing interface-first (`I*`) contracts, typed request/result/key/config/event models and generated `DependencyAccess`. Do not introduce a second DI container, static service locator, ad-hoc global map or per-SYSTEM lifecycle registry.
- A FEATURE imports only approved APIs/capabilities; it must not reach a sibling FEATURE through its concrete packages or silently depend on a second provider implementation.
- A runtime adapter (Paper, Velocity, Spring/HTTP, Discord, CLI, MCP/WebMCP) translates at the host boundary. It does not own the reusable business/domain rules it exposes.
- A provider/integration wrapper owns vendor-specific configuration, invocation, error translation, lifecycle and dependencies under the canonical Tavall wrapper boundary. Domain code does not scatter raw vendor SDK imports.
- A `tavall-*-api` artifact is justified by actual callers, a contract/version boundary, or independently consumable capability. Do not manufacture APIs for every SYSTEM or FEATURE.
- Shared contracts have an explicit owner and import direction. Cyclic module dependencies, duplicate domain authority and a generic `core/common/util` dumping ground are rejected. Existing package hierarchy guidance remains binding; module type names do not mandate `system` or `feature` Java package prefixes.

When a change crosses repositories, update the contract producer before downstream consumers, migrate imports through the approved API, and prove all intended consumers still work against the exact accepted artifact/version. The original consumer's responsibilities must be removed, not merely copied.

## 4. SYSTEM, FEATURE, and Runtime Lifecycle

Record for every FEATURE: parent SYSTEM, owning runtime, required capabilities/API imports, optional provider selection, enabled/disabled desired state, observed state and generation, activation order, failure path, teardown order, and what survives reload. The canonical Tavall DI/module-lifecycle infrastructure owns transition mechanics.

- Disabling a parent SYSTEM denies its dependent FEATURES and its aggregate capability. It must **not** disable unrelated SYSTEMs or restart the owning RUNTIME.
- Disabling/reloading one FEATURE isolates that FEATURE and its declared dependents; unrelated siblings remain available. A removed dependency, stale generation, denied capability, or failed rebinding fails closed.
- Use generation-safe registration/unregistration. Replacement must retire prior listeners, scheduler work, cache/registry handles, dependency aliases and references. A failed activation rolls back both the loaded artifact **and** desired module configuration, leaving an observable terminal result.
- API compatibility, startup/shutdown ordering, host permissions, failover, and rollback belong to the actual owning RUNTIME and deployment system. Do not claim dynamic loading/reload support until the host passes an E2E test.
- The universal `tavall module` command is a **planned** central operator surface under Tavall CLI/`tavall-cd-cli`. Document intended permissions and contracts but do not state that an unsupported command already operates.

## 5. Concrete Separation Examples and Package Layout

The following examples distinguish **accepted ownership direction** from **verified current deployment**; confirm exact source and deployed composition in the owning repository before describing any edge as implemented.

```text
Filesystem:
  tavall-filesystem-api         API, byte/integrity contracts
  tavall-filesystem             SYSTEM, composition/fan-in
    tavall-filesystem-zfs       FEATURE; secondary PROVIDER
    tavall-filesystem-nfs       FEATURE; secondary PROVIDER
  tavall-filesystem-test-suite  TEST_SUITE, validation only
  Tavall Cloud                  consuming RUNTIME / placement authority

Redis: tavall-database owns Redis and DB-facing state; it is not a Filesystem backend.
NLEW: tavall-nlew owns reusable Node/Lane/Environment/Workspace contracts and
  domain behavior; Cloud owns concrete control/placement/execution. Stateless
  NLEW per-record handlers can remain packages, not automatic FEATURES.
Web: tavall-web owns generic web runtime/framework concerns; tavall-web-mc
  owns the Minecraft Web surface; tavall-mc keeps Minecraft gameplay authority.
MC anti-cheat: SYSTEM with independently justified FEATURES is a target
  composition design, not proof of present runtime linkage or a separate JAR.
```

Example **illustrative** internal layout; preserve existing approved `org.tavall.<domain>` roots and package conventions instead of renaming packages by taxonomy:

```text
<system-module>/
  src/main/java/org/tavall/<domain>/
    api/                  (only contracts actually owned here)
    service/              (domain orchestration and fan-in)
    handler/              (bounded behavior)
    runtime/              (host binding when genuinely owned here)
<feature-module>/
  src/main/java/org/tavall/<domain>/<capability>/
    service/
    handler/
    adapter/              (only where an adapter role really exists)
```

A SYSTEM may contain stateless domain policy without a FEATURE. A repository may contain several modules without containing multiple runtimes. A single final application/JAR may package independently reloadable modules without converting those modules into independent processes.

## 6. Migration and E2E Acceptance Checklist

Before coding: resolve current `tavall-docs` sections and producer source; classify every touched module; identify consumer/fan-in and ownership; map typed API imports; locate the actual DI registration and runtime host; list the concrete old responsibilities to remove; capture exact revision/PRs in the existing Tavall agent ledger/provenance.

During migration: keep one owning semantic contract, move implementation and tests together, update Gradle/composite project relationships and `.tavallci`, rewrite concrete consumers to APIs, retain required compatible contracts intentionally, and record actual lifecycle support rather than guessing.

Acceptance uses real classes and integration-first tests where practical:

1. **Static architecture**: canonical `tavall-test-suite-tools` inspects compiled production classes and test evidence; reject forbidden imports, dependency cycles, sibling implementation leaks, wrong package ownership and direct vendor imports outside wrappers.
2. **Composition**: bootstrap actual owning RUNTIME and Tavall DI; verify each declared SYSTEM/FEATURE is registered and reachable through the expected API/caller.
3. **Isolation**: disable/reload one FEATURE, prove unrelated siblings continue and stale references fail closed; disable SYSTEM and prove its aggregate is unavailable.
4. **Failure/rollback**: exercise unavailable dependency, failed startup, partial cleanup and rollback of artifact plus module state.
5. **End-to-end**: exercise real host surface (Paper/Velocity/Cloud/Web/CLI as relevant), runtime packaging, API compatibility, permission checks, restarts and observability. Validate on an exact source SHA and the actual target environment.
6. **Documentation/progression**: update each owning module README, module-scoped Progression and consumer migrations, report which tests ran and which did not; do not mistake design completion for deployed acceptance.

Route adjacent concerns to [Module Types](../MODULE_TYPES.md), [Namespaces and Package Rules](NAMESPACES_VARIABLES_AND_OOP.md), [DI](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md), [Interfaces and Abstractions](INTERFACES_AND_ABSTRACTIONS.md), [Testing](TESTING_AND_GIT.md), [CI/CD](../CI_CD.md), and [Git Workflow](../GIT_WORKFLOW.md). This chapter specializes separation decisions and **does not duplicate** those authorities.
