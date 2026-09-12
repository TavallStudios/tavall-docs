# Tavall Studios Code Architecture

> **Status:** Active  
> **Authority:** Binding shared architecture root for Tavall Studios and projects that consume `tavall-docs`  
> **Applies to:** Production modules, contributors, automation, generated code, reviews, and AI-assisted development

This document owns **cross-project architecture invariants and topic routing**. It is intentionally not the full implementation manual for every pattern.

Detailed chapters under [`docs/quality/code-architecture/`](code-architecture/) are **binding specializations** for the topics they own. When a topic has a delegated chapter, the summary in this file is not a substitute for reading that chapter.

Project Novus is used frequently as production evidence because it exercises many Tavall systems in one codebase. Those examples demonstrate shared rules; they do not make this document Project Novus-only.

## Purpose

Tavall architecture optimizes for:

- clear ownership;
- small coherent classes;
- typed data flow;
- stable lifecycle behavior;
- reuse of Tavall infrastructure;
- testable boundaries;
- honest failure and recovery semantics.

Decorative abstraction is not architecture. A class is not improved merely by acquiring an interface, builder, repository, or vaguely important suffix.

## Required Reading and Delegation

Before changing architecture:

1. Read this file for shared invariants and topic routing.
2. Read **every delegated chapter relevant to the code being touched**.
3. Read repository/module `AGENTS.md`, architecture tests, and local design rules.
4. Read the current checked-in Tavall tool/module contracts used by the implementation.
5. Inspect the current lifecycle/composition owner and production behavior before designing a replacement.

A change may require several delegated chapters. A Handler using Tavall DI, Cache, and persistence must not read only `HANDLERS.md`; it also requires the DI and state/persistence chapters that own those boundaries.

### Required Topic Routing

| Topic being changed | Required delegated chapter |
| --- | --- |
| Packages, class names, fields, locals, OOP, DRY, type safety | [Namespaces, Variables, OOP, DRY, and Type Safety](code-architecture/NAMESPACES_VARIABLES_AND_OOP.md) |
| Class roles and suffix responsibilities | [Classes](code-architecture/CLASSES.md) |
| Method naming, shape, parameters, locals, data/cache/database method ownership | [Methods](code-architecture/METHODS.md) |
| Interfaces, abstraction, substitution boundaries | [Interfaces and Abstractions](code-architecture/INTERFACES_AND_ABSTRACTIONS.md) |
| Tavall DI, dependency access, default consumers, orchestration, cleanup | [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md) |
| Handler/DataHandler/MetaDataHandler behavior | [Handlers](code-architecture/HANDLERS.md) |
| Builders and construction-only behavior | [Builders](code-architecture/BUILDERS.md) |
| Requests, results, resolvers, formatters | [Requests, Results, Resolvers, and Formatters](code-architecture/REQUESTS_RESULTS_RESOLVERS_AND_FORMATTERS.md) |
| Routers and delegation | [Routers and Delegation](code-architecture/ROUTERS_AND_DELEGATION.md) |
| Registry, Cache, Redis, operation state, durable-state classification | [Registries, Caches, and Persistence](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md) |
| Application-owned mutable maps/sets/keyed collections | [Application-Owned Mutable Maps](code-architecture/APPLICATION_OWNED_MUTABLE_MAPS.md) |
| Tavall Database entity persistence and `*Repository` migration | [Entity Persistence](code-architecture/ENTITY_PERSISTENCE.md) |
| Validation, fallbacks, prohibited patterns, direct Thread ownership | [Validation, Fallbacks, and Anti-Patterns](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md) |
| Utilities and pure/static boundaries | [Utilities](code-architecture/UTILITIES.md) |
| Effect/animation sequences and timing ownership | [Effect Sequences](code-architecture/EFFECT_SEQUENCES.md) |
| Test structure and Git-facing architecture expectations | [Testing and Git](code-architecture/TESTING_AND_GIT.md) and [Git Workflow](GIT_WORKFLOW.md) |

### Conflict Rule

A delegated chapter may specialize a shared invariant for its topic, but it must not silently contradict this root document.

If a direct conflict is discovered:

1. treat it as a documentation defect;
2. follow the root invariant until the conflict is reconciled;
3. inspect current architecture tests and owning module contracts before changing behavior;
4. fix the conflicting documentation in the same coherent work when practical.

Do not choose whichever paragraph is more convenient and call that architecture.

##### Why

Routing must happen before enough detail exists for a reader or agent to stop early. The root explains what must remain true; delegated chapters explain how that invariant applies to the specific pattern being changed.

Architecture review is required for a new persistence/cache authority, lifecycle owner, global registry, cross-module dependency, distributed fallback, reflective/static dependency lookup, direct thread/executor ownership, or a class with more than four managed dependencies.

## Shared Invariants

The sections below are **cross-cutting summaries**. Follow their delegated chapters for detailed pattern rules, examples, exceptions, and review criteria.

## Package Ownership and Class Roles

Packages describe domain ownership and role. Avoid broad new buckets such as `util`, `misc`, `common`, or `manager`; platform-specific code stays in its platform boundary and product/mode-specific code stays with its owner.

Common roles include Handler, Service, Orchestrator, Router, Resolver, Registry, Cache, Builder, Mapper, Serializer, Reader, Writer, Publisher, Consumer, Listener, Bootstrap, Runtime, and Timer. The suffix must describe actual ownership rather than decorate an implementation after the fact.

Detailed rules: [Namespaces and Class Names](code-architecture/NAMESPACES_VARIABLES_AND_OOP.md#namespaces-and-class-names) and [Class Roles](code-architecture/CLASSES.md).

### Prohibited `*Repository` Production Type Name

**New Tavall-owned production classes, interfaces, records, enums, or other declared types whose simple name ends in `Repository` are prohibited.** Existing `*Repository` types are migration debt only; the debt set may shrink but must not grow.

Do not evade the rule with `RepositoryImpl`, `RepositoryAdapter`, `RepositoryStore`, or another name whose purpose is preserving the same application repository layer. Third-party APIs may expose externally owned Repository types when unavoidable at an integration boundary.

Detailed migration and persistence rules: [Entity Persistence](code-architecture/ENTITY_PERSISTENCE.md#repository-name-prohibition).

##### Why

`Repository` repeatedly became a generic wrapper that preserved obsolete persistence mechanics. The prohibition forces real behavior to state its actual responsibility while Tavall Database owns ordinary durable persistence.

## Interfaces and Abstractions

Use an interface for a real contract/substitution boundary such as a Tavall DI alias, module boundary, platform adapter, provider strategy, external system boundary, or testable policy family. Do not create an interface merely because a concrete class exists, and do not recreate `I*Repository` as a persistence seam.

Detailed rules: [Interfaces and Abstractions](code-architecture/INTERFACES_AND_ABSTRACTIONS.md).

## Dependency Injection

`tavall-di` is the default Tavall runtime composition system unless a narrower repository explicitly defines another composition boundary.

Ordinary managed behavior declares Tavall-managed collaborators through `DependencyAccess<...>` and the generated typed access surface. It does not constructor-inject those managed application dependencies, add static service locators, or own manual composition trees. More than four managed dependencies is a design-review signal, not a hard cap.

Detailed registration, generated access, alias identity, default-consumer, orchestration, and cleanup rules: [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md).

## Builders, Handlers, Services, Orchestrators, and Routers

- **Builder:** constructs typed output only.
- **Handler:** owns one focused behavior/operation family.
- **Service:** provides one cohesive reusable domain capability.
- **Orchestrator:** owns ordered cross-boundary workflow/lifecycle coordination.
- **Router:** selects and delegates without becoming the implementation.
- **Listener/command/controller:** adapts external input/output and delegates reusable domain behavior.

Detailed rules: [Builders](code-architecture/BUILDERS.md), [Handlers](code-architecture/HANDLERS.md), [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md#orchestration-pattern), and [Routers and Delegation](code-architecture/ROUTERS_AND_DELEGATION.md).

## Typed Data, Requests, Results, Keys, and Local Types

Prefer typed immutable values where value semantics fit. `*Request` carries operation input, `*Result` represents expected outcomes, `*Data`/`*State` carries named values, `*MetaData` represents derived/display-ready values, and stable keys use typed identities rather than raw strings.

Production Java local variables under `src/main/java` use explicit declared types; Java `var` is prohibited there. Tests, fixtures, generated source, and tooling may define narrower rules independently.

Detailed rules and Bad/Good examples: [Namespaces, Variables, OOP, DRY, and Type Safety](code-architecture/NAMESPACES_VARIABLES_AND_OOP.md#local-variables), [Methods](code-architecture/METHODS.md), and [Requests, Results, Resolvers, and Formatters](code-architecture/REQUESTS_RESULTS_RESOLVERS_AND_FORMATTERS.md).

##### Why

Tavall uses visible types as architecture documentation. Explicit type boundaries make API and domain changes visible during review and refactoring.

## Validation and Mutation Ordering

Validate before mutation. A normal multi-step mutation is:

```text
validate
  -> resolve required dependencies
  -> authorize/check invariants
  -> commit through the authoritative durable boundary
  -> update/invalidate caches and registries
  -> publish typed events/projections
  -> return typed result
```

A different order must document authority, partial-failure behavior, retry ownership, and reconciliation.

Detailed validation/fallback rules: [Validation, Fallbacks, and Anti-Patterns](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md).

## Concurrency and Operation State

Ordinary off-thread application work routes through Tavall concurrency; platform-affine mutation routes through the owning platform scheduler. Ordinary feature code does not create worker threads or private executors merely to obtain concurrency.

The current checked-in [`AsyncTask`](https://github.com/TavallStudios/TavallMonoRepo/blob/8d3891ec9620e008405f9367b80b0e5c7bd0ab34/tavall-java-tools/tavall-concurrency/src/main/java/org/tavall/internal/utils/concurrent/AsyncTask.java) uses a virtual-thread-per-task executor and exposes `CompletableFuture` completion. Retain an explicitly typed `CompletableFuture<T>` only when completion is part of the caller's contract.

Direct Thread construction is limited to canonical concurrency infrastructure or a JVM/platform/integration API that structurally requires a Thread object, with an explicit reason and lifecycle owner.

Detailed Bad/Good examples and exceptions: [Direct Thread Ownership Pattern](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md#direct-thread-ownership-pattern).

Planned `ThreadRegistry` and CPU/core-aware inspection/accounting work is tracked in [TavallMonoRepo issue #7](https://github.com/TavallStudios/TavallMonoRepo/issues/7). It is planned infrastructure, not current behavior.

##### Why

Centralized concurrency keeps virtual-thread policy, lifecycle, diagnostics, and future resource balancing behind one owner.

## Tavall Database and Durable Persistence

For Tavall applications using PostgreSQL/JPA, Tavall Database owns persistence runtime mechanics and the entity model. Application architecture consumes the entity classes and persistence contract defined by the checked-in `tavall-database` version.

Shared application documentation does **not** freeze a concrete Tavall Database accessor. Application code does not recreate EntityManager/factory lifecycle, transaction callbacks, JDBC transaction wrappers, duplicate persistence runtimes, or a new application `*Repository` layer.

When required durable behavior is missing, extend `tavall-database` upstream instead of recreating persistence ownership downstream.

Detailed binding rules: [Entity Persistence](code-architecture/ENTITY_PERSISTENCE.md).

##### Why

Persistence ownership is stable even when Tavall Database's concrete API evolves. The module that implements and tests persistence owns that API.

## Runtime, Cached, Distributed, and Keyed State

Classify state by semantics before choosing a collection or class name:

- durable application truth -> Tavall Database entity model/current contract;
- disposable/reloadable/expiring/stale-able fast state -> Tavall Cache;
- runtime identity/definitions/providers/sessions -> Tavall Registry;
- distributed coordination/projections -> owning Redis/distributed boundary;
- in-flight futures/tasks/retries/cancellation -> dedicated typed operation/runtime owner;
- bounded method-local transforms -> local collection that never escapes;
- immutable snapshots/values -> typed immutable data.

Application-owned mutable maps/sets are prohibited by default. Registry/Cache/database/distributed/operation infrastructure may own mutable maps internally according to their own lifecycle contracts.

Detailed rules: [Registries, Caches, and Persistence](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md) and [Application-Owned Mutable Maps](code-architecture/APPLICATION_OWNED_MUTABLE_MAPS.md).

## Cross-Storage Mutation

For PostgreSQL-authoritative state, the normal order is:

```text
validate
  -> commit through the current Tavall Database entity contract
  -> update/invalidate Redis/cache/registry projections
  -> publish typed result/event
```

Any alternative documents source of truth, idempotency, durable commit boundary, retry ownership, partial-failure visibility, restoration, reconciliation, audit, and rollback.

Detailed state/recovery rules: [Registries, Caches, and Persistence](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md#cross-storage-mutation).

## Platform Boundaries

Platform adapters remain thin. Paper, Velocity, web, Discord, Cloud, and other platform objects/lifecycle mechanics stay in their owning modules. Listeners/controllers/commands adapt typed input/output and do not absorb durable persistence or reusable domain rules.

## Lifecycle and Cleanup

Every long-lived object has an owner. Define creation, registration, replacement, close semantics, partial-startup cleanup, unload behavior, async draining/cancellation, and reverse-order teardown where applicable.

Do not leave generation-owned caches, listeners, tasks, registries, threads, classloaders, database contexts, or subscriptions reachable after unload.

Detailed DI/runtime cleanup rules: [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md#lifecycle-and-cleanup).

## Error Handling

Expected rejections use typed results. Infrastructure failures propagate operation-specific failures. Fallbacks have an owner/reason, remain observable, never report success for a failed required durable write, and define recovery/reconciliation.

Detailed fallback rules: [Validation, Fallbacks, and Anti-Patterns](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md#fallback-pattern).

## Testing

Test real behavior at the narrowest meaningful boundary and report exactly what ran and what remains untested. Unit, integration, simulation, and E2E boundaries should match the contract being exercised rather than merely maximize test count.

Detailed testing rules: [Testing and Git](code-architecture/TESTING_AND_GIT.md). Repository workflow and review requirements remain owned by [Git Workflow](GIT_WORKFLOW.md).

## Architecture Review Checklist

Before accepting a change, confirm:

- [ ] This root document and every relevant delegated chapter were read.
- [ ] Repository/module instructions and current Tavall tool contracts were inspected where relevant.
- [ ] Owner/module/package and class/method roles are correct.
- [ ] No new Tavall-owned production type ends in `Repository`; migration debt does not grow.
- [ ] Interfaces represent real contract/substitution boundaries.
- [ ] Tavall-managed dependencies resolve through Tavall DI rather than constructor/static-locator ownership.
- [ ] Builders construct typed output; Handler/Service/Orchestrator/Router responsibilities remain distinct.
- [ ] Production Java locals use explicit declared types rather than `var`.
- [ ] Off-thread application work uses Tavall concurrency/owning platform schedulers rather than direct worker-thread ownership.
- [ ] Durable persistence follows Tavall Database's checked-in entity contract without shared docs freezing a concrete accessor.
- [ ] Runtime keyed state is Registry/Cache/distributed/typed operation state rather than consumer-owned mutable maps.
- [ ] Cross-storage authority, ordering, recovery, and reconciliation are explicit.
- [ ] Async/lifecycle cleanup is explicit.
- [ ] Requests/results/keys/state are typed and validation precedes mutation.
- [ ] Tests exercise real contracts and meaningful failure/cleanup paths.
- [ ] Current architecture tests pass or pre-existing migration debt is explicitly baselined and cannot grow.
