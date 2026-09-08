# Tavall Studios Code Architecture

> **Status:** Active  
> **Authority:** Binding shared default for Tavall Studios and projects that consume `tavall-docs`  
> **Applies to:** Production modules, contributors, automation, generated code, reviews, and AI-assisted development

This document defines the required shared architecture for Tavall projects. Repository- and module-specific rules may strengthen it, but they must not silently weaken it.

Project Novus is used frequently as production evidence because it exercises many Tavall systems in one codebase. Those examples demonstrate shared rules; they do not make this document Project Novus-only.

Detailed chapters under [`docs/quality/code-architecture/`](code-architecture/) provide examples and specialized guidance. **When a detailed chapter conflicts with this file, this file wins.**

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

## Reading and Enforcement

Before changing architecture:

1. Read this file.
2. Read the relevant detailed chapter.
3. Read repository/module `AGENTS.md`, architecture tests, and local design rules.
4. Inspect the current lifecycle/composition owner.
5. Prefer current checked-in Tavall tool contracts over remembered API shapes.
6. When the rule concerns an existing Tavall tool, inspect that canonical tool's interfaces, implementation, tests, and owning docs before changing shared guidance.

Canonical Tavall tools own their own API shape, inheritance model, lifecycle semantics, supported low-level/framework surfaces, and naming vocabulary. Shared architecture may classify when a tool is used and may constrain ordinary application consumers, but it must not silently redesign the canonical tool itself. A desired redesign belongs in the owning tool first and in shared docs only after that change becomes the accepted tool contract.

Architecture review is required for a new persistence/cache authority, lifecycle owner, global registry, cross-module dependency, distributed fallback, reflective/static dependency lookup, direct thread/executor ownership, or a class with more than four managed dependencies.

## Package Ownership

Packages describe domain ownership and role.

Preferred shapes include:

```text
<domain>/data
<domain>/request
<domain>/result
<domain>/handler
<domain>/service
<domain>/orchestrator
<domain>/resolver
<domain>/router
<domain>/registry
<domain>/cache
<domain>/persistence
<domain>/event
<domain>/listener
<domain>/bootstrap
<domain>/runtime
<domain>/config
<domain>/builder
<domain>/mapper
<domain>/serializer
<domain>/reader
<domain>/writer
```

Do **not** introduce a new application `repository` package merely to preserve an older persistence abstraction.

Avoid broad new packages such as `util`, `misc`, `common`, or `manager`. Platform-specific code stays in its platform module. Product/mode-specific code stays with its owner.

## Naming and Class Roles

| Suffix | Role |
| --- | --- |
| `Handler` | Performs one focused domain behavior or owns one input/operation family. |
| `Service` | Provides one cohesive reusable domain capability. |
| `Orchestrator` | Coordinates focused collaborators across an ordered workflow/lifecycle. |
| `Router` | Selects and delegates to handlers. |
| `Resolver` | Derives one typed answer from explicit inputs. |
| `Registry` | Owns typed runtime lookup state. |
| `Cache` | Owns bounded, disposable, expiring, reloadable, or stale-able fast state. |
| `Builder` | Constructs typed values/definitions/requests/results/configuration. |
| `Mapper` | Converts representations. |
| `Serializer` | Converts typed data to serialized form. |
| `Reader` | Reads a source. |
| `Writer` | Writes a source. |
| `Publisher` | Publishes typed events/updates. |
| `Consumer` | Consumes queued/streamed/published data. |
| `Listener` | Adapts platform events into domain behavior. |
| `Bootstrap` | Owns startup/composition wiring. |
| `Runtime` | Owns a live generation or active-system lifecycle. |
| `Timer` | Owns actual time progression or timer state. |

### Prohibited `*Repository` Production Type Name

**New Tavall-owned production classes, interfaces, records, enums, or other declared types whose simple name ends in `Repository` are prohibited.**

Examples that must not be introduced:

```text
PlayerRepository
IPlayerRepository
PostgresPlayerRepository
MessageConfigRepository
AccountLinkRepository
```

Existing `*Repository` types are **migration debt only**. Their existence does not create an exception, template, naming precedent, or approved architecture boundary. Migration work should delete or rename them as their behavior moves to the correct owner. The allowed legacy set may only shrink.

Do not evade the rule with `RepositoryImpl`, `RepositoryAdapter`, `RepositoryStore`, or another name whose purpose is merely to recreate the same application repository layer. If behavior is real, name the actual capability it owns. If behavior is ordinary durable entity persistence, use Tavall Database as described below.

Third-party APIs may expose externally owned types named `Repository`. Tavall code may interact with those types at the integration boundary when unavoidable, but must not wrap them in a new Tavall-owned `*Repository` abstraction.

##### Why

`Repository` repeatedly became a default wrapper around whatever persistence API happened to exist that year. Banning the Tavall-owned production name removes that escape hatch and forces real behavior to state its actual responsibility.

Avoid `Manager` as well unless maintaining an external API that cannot be changed.

## Interfaces and Abstractions

Use an interface for a real contract/substitution boundary, including a Tavall DI alias, platform adapter, distributed/local strategy, module boundary, external provider, test fake, or policy family.

Do not create an interface merely because a concrete class exists. Do not invent `I*Repository` as a persistence seam. If a persistence-adjacent capability genuinely has behavior beyond entity persistence, name the capability itself, such as a writer, loader, resolver, history service, synchronization handler, or domain-specific gateway when that term truthfully describes an external boundary.

## Dependency Injection

`tavall-di` is the default Tavall runtime composition system unless a narrower repository explicitly defines another composition boundary.

Ordinary managed behavior:

- declares managed collaborators through `DependencyAccess<...>`;
- uses generated typed getters;
- captures `getInstance()` once when several dependencies are used;
- fails fast for missing required dependencies;
- does not use reflection for normal lookup;
- does not constructor-inject Tavall-managed application dependencies;
- does not add static service locators.

Constructors remain valid for immutable object state, configuration, builder inputs, and genuinely externally owned platform handles.

More than four managed dependencies is a design-review signal, not a hard cap. Keep direct access when the class is still cohesive, create a cohesive immutable domain bundle only when a real durable domain boundary exists, or split responsibilities when several behaviors/lifecycle phases have accumulated.

Managed concrete implementations use `@DelegatesTo` for interface aliases and preserve one metadata-owned object identity across aliases.

## Builders

Builders construct typed values. They do not become services, persistence workflows, registries, composition roots, or dependency containers.

A builder may own validation/defaulting required to construct its result. It must not perform persistence, cache mutation, authorization, managed registration, scheduling, or dependency lookup.

Do not use a builder to hide a long Tavall-managed constructor dependency list.

## Handlers, Services, Orchestrators, and Routers

- **Handler:** one focused behavior/operation family.
- **Service:** one cohesive reusable domain capability used by several consumers. Longevity is not the defining criterion.
- **Orchestrator:** ordered cross-boundary workflow/lifecycle coordination. It does not absorb collaborator rules or storage.
- **Router:** selects/delegates. It does not become the implementation or durable owner.
- **Listener/command/controller:** adapts external input and delegates; it does not acquire reusable domain rules merely because input arrived there first.

## Data, Requests, Results, Keys, and Local Types

Use typed immutable values when value semantics fit.

- `*Request` carries operation input.
- `*Result` represents expected outcomes.
- `*Data` / `*State` carries named values, not arbitrary mutable storage.
- `*MetaData` represents known derived/display-ready values.
- Typed keys represent registry/cache/message/timer/distributed identity.
- Production Java local variables use explicit declared types; `var` is prohibited under `src/main/java`.

Extensible metadata maps are allowed only at real dynamic integration/serialization edges. Core identity and behavior remain typed.

Detailed local-variable examples: [Namespaces, Variables, OOP, DRY, and Type Safety](code-architecture/NAMESPACES_VARIABLES_AND_OOP.md#local-variables).

##### Why

Tavall uses types as architecture documentation. `var` retains compiler typing but hides the type at the use site, making data and API boundaries less visible during review and refactoring.

## Validation and Mutation Ordering

Validate before mutation.

A normal multi-step mutation is:

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

## Concurrency and Operation State

Use Tavall concurrency tools and owning platform schedulers. Do not block latency-sensitive platform threads with database, Redis, network, filesystem, or long computation work.

For ordinary off-thread application work, use the shared Tavall concurrency abstraction. The current checked-in [`AsyncTask`](https://github.com/TavallStudios/TavallMonoRepo/blob/8d3891ec9620e008405f9367b80b0e5c7bd0ab34/tavall-java-tools/tavall-concurrency/src/main/java/org/tavall/internal/utils/concurrent/AsyncTask.java) runs work on a virtual-thread-per-task executor and exposes `CompletableFuture` completion.

Rules:

- ordinary production application code does not create worker threads directly with `new Thread(...)`, `Thread.startVirtualThread(...)`, `Thread.ofVirtual()`, or `Thread.ofPlatform()`;
- ordinary feature code does not create private executors merely to obtain its own thread pool;
- use `AsyncTask` for off-thread Tavall work and the owning platform scheduler for thread-affine platform mutation;
- retain an explicitly typed `CompletableFuture<T>` only when completion is part of the caller's contract;
- direct `Thread` creation is reserved for canonical concurrency infrastructure or a JVM/platform/integration API that structurally requires a `Thread` object, with an explicit reason and lifecycle owner;
- `Thread.currentThread()` inspection, interrupt restoration, and equivalent operations on an already-owning thread are not thread creation;
- every async/scheduled operation has explicit lifecycle/cancellation ownership;
- a dedicated operation/runtime owner may internally own in-flight futures/tasks/cancellation state; ordinary handlers/services/listeners/controllers/orchestrators do not gain arbitrary mutable operation maps.

Project Novus production [`FFARegionControlService`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/FFARegionControlService.java) routes off-thread population/routing work through `AsyncTask` and returns Bukkit-affine work to the Bukkit scheduler. [`NovusDiscordCoreApplication`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-discord/novus-discord-core/src/main/java/org/tavall/discord/core/NovusDiscordCoreApplication.java) is a narrow direct-`Thread` exception because `Runtime.addShutdownHook(...)` structurally requires a `Thread` object.

Detailed anti-pattern: [Direct Thread Ownership](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md#direct-thread-ownership-pattern).

##### Why

Centralized concurrency keeps virtual-thread policy, lifecycle, diagnostics, and future resource balancing behind one owner instead of scattering thread creation across features.

### TODO: ThreadRegistry and CPU/Core Inspection

Build a Tavall concurrency/runtime ownership layer that can account for work across services and machine resources rather than merely launch tasks.

Required direction:

- add a typed `ThreadRegistry` or successor runtime-work registry for Tavall-owned concurrent operations;
- identify work by service/domain/runtime owner instead of only raw JVM thread name;
- expose active work, lifecycle state, cancellation ownership, virtual/platform thread kind, and useful timing/diagnostic data;
- inspect effective processor/core capacity, including container/cgroup limits where applicable;
- collect JVM/thread CPU-time and scheduling evidence where the runtime exposes reliable data;
- support per-service accounting, prioritization, load shedding, and CPU-capacity/time balancing;
- integrate the ownership model into `AsyncTask`/Tavall concurrency rather than asking every service to register raw threads manually;
- preserve platform-thread affinity rules for Paper, UI/event loops, and other runtimes that require a specific scheduler.

This is **planned infrastructure, not current behavior**. Until it exists, application code must still route work through Tavall concurrency so the eventual registry/balancer has one boundary to instrument.

## Tavall Database and Durable Persistence

For Tavall applications using PostgreSQL/JPA, **`tavall-database` owns the persistence runtime and its entity model**.

Application architecture consumes **Tavall Database entity classes and the entity persistence contract defined by the checked-in `tavall-database` version**. This shared document deliberately does **not** prescribe a concrete accessor such as `IPostgresDatabase.entities()`, `.jpa()`, an entity store getter, or any future replacement. That API belongs to `tavall-database` and must be read from that module's current documentation, interfaces, and tests.

Binding rules:

- application modules model durable state with Tavall Database-compatible mapped entity classes as defined by the installed module;
- Tavall Database owns provider bootstrap, entity discovery, entity-manager/factory lifecycle, transaction begin/flush/commit/rollback, locked reads, operation draining, and related persistence mechanics;
- application code does not recreate an `EntityManager`, transaction callback, JPA context, JDBC transaction wrapper, or parallel persistence runtime;
- application code does not create `*Repository` classes/interfaces around Tavall Database;
- ordinary durable behavior follows the entity operations/contracts provided by the checked-in Tavall Database version rather than copying that API into shared docs;
- when required transactional/entity behavior is missing, extend `tavall-database` upstream instead of recreating a local persistence layer;
- mapped entities own their mapping/query metadata according to Tavall Database rules;
- production schema evolution uses checked-in migrations;
- native PostgreSQL behavior is narrowly documented and tested according to Tavall Database policy.

Detailed binding rules: [Entity Persistence](code-architecture/ENTITY_PERSISTENCE.md).

##### Why

Tavall Database is itself an evolving shared module. The application rule is about ownership: use Tavall Database entities and its current entity contract; do not rebuild or freeze the persistence runtime downstream.

## Redis

Redis is distributed runtime infrastructure, not durable authority unless a system explicitly assigns that authority and defines recovery.

Every key family defines owner, prefix, value schema, TTL/staleness behavior, missing-key behavior, and reconciliation source.

## Registries

Use `tavall-registry` for typed runtime lookup ownership: loaded definitions, providers/strategies, active runtime objects, and sessions without cache semantics.

The canonical Registry model intentionally preserves Java collection behavior: `AbstractRegistry<K, V>` extends `ConcurrentHashMap<K, V>` and layers the `IAbstractRegistry<K, V>` registry vocabulary over it. Ordinary consumers should prefer the registry-named methods when they express the operation cleanly. Registry subclasses and framework code may use inherited `Map` / `ConcurrentMap` operations when the canonical tool contract supports them.

Do not treat collection inheritance itself as a defect or require composition merely to hide inherited operations. If a specialized registry adds additional lookup structures or invariants, those invariants must remain coherent across every mutation path that the registry continues to support.

Do not make `AbstractIndexedRegistry` a blanket architecture requirement. Several lookup dimensions still have one Registry owner; first use the current canonical `tavall-registry` vocabulary and only add specialized lookup machinery when the owning registry genuinely requires it.

## Caches

Use `tavall-cache` for disposable/reloadable/expiring/stale-able fast state. Cache authority, hit/miss/stale behavior, TTL, invalidation, reconnect/reload/shutdown behavior, and failed-write recovery are explicit.

A cache never becomes durable authority by convenience.

## Mutable Keyed State Classification

Application-owned mutable maps/sets are prohibited by default. Classify keyed state by behavior:

1. durable state -> Tavall Database entity model/current entity contract;
2. expiring/reloadable/stale-able state -> Tavall Cache;
3. runtime identity/definitions/providers/sessions -> Tavall Registry;
4. several lookup dimensions over one runtime identity -> one Registry owner using the current canonical registry contract, with any additional lookup structures owned coherently by that registry;
5. in-flight futures/tasks/retries/cancellation -> dedicated typed operation/runtime owner;
6. method-local bounded transformations -> local collection when it never escapes;
7. immutable lookup/data snapshots -> immutable typed collections.

Detailed rules: [Application-Owned Mutable Maps](code-architecture/APPLICATION_OWNED_MUTABLE_MAPS.md).

## Cross-Storage Mutation

For PostgreSQL-authoritative state, the normal order is:

```text
validate
  -> commit through the current Tavall Database entity contract
  -> update/invalidate Redis/cache/registry
  -> publish typed result/event
```

Any alternative documents source of truth, idempotency, commit boundary, retry owner/lifetime, partial-failure visibility, restoration, reconciliation, audit, and rollback.

## Platform Boundaries

Platform adapters remain thin. Paper/Velocity/web/Discord/Cloud-specific objects and lifecycle mechanics stay in their owning platform modules. Platform listeners/controllers/commands adapt typed input/output and do not own durable persistence mechanics.

## Lifecycle and Cleanup

Every long-lived object has an owner. Define creation, registration, replacement, close semantics, partial-startup cleanup, unload behavior, async draining/cancellation, and reverse-order teardown where applicable.

Do not leave generation-owned caches, listeners, tasks, registries, threads, classloaders, database contexts, or subscriptions reachable after unload.

## Error Handling

Expected rejections use typed results. Infrastructure failures propagate operation-specific failures. Fallbacks have an owner/reason, remain observable, never report success for a failed required durable write, and define recovery/reconciliation.

## Testing

Test real behavior at the narrowest meaningful boundary.

- Unit: policies, resolvers, builders, typed transitions, validation, serialization.
- Integration: Tavall Database entity behavior, PostgreSQL-specific contracts, Redis, DI registration/cleanup, Registry behavior and any specialized lookup invariants, cache TTL/invalidation, module lifecycle.
- Simulation/E2E: complete runtime flows, retries, cleanup, routing, reconnect/transfer, and user interaction where applicable.

Test package/class names mirror production. Validation reports exactly what ran and what remains untested.

## Extended Architecture Chapters

| Chapter | Extended detail |
| --- | --- |
| [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md) | DI ownership, default consumers, cleanup, orchestration. |
| [Entity Persistence](code-architecture/ENTITY_PERSISTENCE.md) | Tavall Database entity ownership and persistence-runtime prohibitions. |
| [Registries, Caches, and Persistence](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md) | State classification, registry/cache semantics, durable-state ownership. |
| [Testing and Git Discipline](code-architecture/TESTING_AND_GIT.md) | Test structure and commit-boundary expectations. |

## Architecture Review Checklist

Before accepting a change, confirm:

- [ ] Owner/module/package are correct.
- [ ] Class/method names state exact responsibility.
- [ ] No new Tavall-owned production type ends in `Repository`.
- [ ] Existing `*Repository` names are treated only as migration debt and the debt set never grows.
- [ ] Interfaces represent real DI/module/substitution contracts.
- [ ] Tavall-managed dependencies resolve through the owning `IDependencyMap`, not constructors/static locators.
- [ ] Builders construct typed output and do not wire managed behavior.
- [ ] Handler/Service/Orchestrator/Router responsibilities remain distinct.
- [ ] Tavall tools are reused rather than recreated.
- [ ] Shared docs and application rules were checked against the current canonical Tavall tool contract before changing that tool's API, inheritance, lifecycle, or naming assumptions.
- [ ] Production Java locals use explicit declared types rather than `var`.
- [ ] Off-thread application work uses Tavall concurrency/owning platform schedulers rather than direct thread ownership.
- [ ] Any direct `Thread` creation has an explicit infrastructure/JVM/platform reason and lifecycle owner.
- [ ] `CompletableFuture<T>` is retained only when completion is actually part of the caller's contract.
- [ ] Durable persistence follows Tavall Database entity classes and the entity contract defined by the checked-in Tavall Database version.
- [ ] Shared application docs do not freeze a concrete Tavall Database accessor.
- [ ] Application code does not own JPA/JDBC/transaction/factory lifecycle.
- [ ] Runtime keyed state is Registry/Cache/typed operation state, not consumer-owned maps.
- [ ] Canonical tool collection inheritance is not rejected merely for exposing supported Java collection behavior.
- [ ] Cross-storage authority, ordering, recovery, and reconciliation are explicit.
- [ ] Async/lifecycle cleanup is explicit.
- [ ] Requests/results/keys/state are typed.
- [ ] Validation precedes mutation.
- [ ] Tests exercise real contracts and meaningful failure/cleanup paths.
- [ ] Current architecture tests pass or any pre-existing migration debt is explicitly baselined and cannot grow.
