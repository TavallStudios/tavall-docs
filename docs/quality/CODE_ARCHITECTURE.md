# Project Novus Code Architecture

> **Status:** Active  
> **Authority:** Binding for all Project Novus code, reviews, generation, and refactoring  
> **Applies to:** All modules, contributors, automation, and AI-assisted development

This document defines the required code architecture for Project Novus.

The files under [`docs/quality/code-architecture/`](code-architecture/README.md) may retain extended examples, specialized rules, and historical explanation. This file remains the primary document that engineers and AI agents must read before changing code.

## Purpose

Project Novus spans shared Java APIs, Paper, Velocity, Spring web, Discord, PostgreSQL, Redis, module runtimes, and distributed Cloud components. Architecture must make ownership and data flow obvious across those boundaries.

The goal is not maximum abstraction. The goal is:

- Clear ownership.
- Small coherent classes.
- Typed data flow.
- Stable lifecycle behavior.
- Reusable Tavall infrastructure.
- Testable boundaries.
- Honest failure and recovery semantics.

A class is not well designed merely because it has an interface, a builder, and a name ending in `Service`. Decorative abstraction is still decoration, only now it has more files.

## Reading and Enforcement

Before changing code:

1. Read this entire file.
2. Read the relevant detailed chapter when the change touches a specialized boundary.
3. Read module-local documentation and tests.
4. Inspect the current composition root and lifecycle owner.
5. Reuse real checked-in production patterns.

When rules conflict:

1. This file wins over detailed chapters.
2. A narrower module rule may strengthen this file but may not weaken it silently.
3. Tests document behavior but do not override an explicit architecture rule.
4. Temporary compatibility seams must be labeled and owned.

Architecture review is required when a change introduces:

- A new cross-module dependency.
- A new persistence or cache authority.
- A new lifecycle owner.
- A new global registry.
- A new distributed fallback.
- More than four managed dependencies in one class.
- A new reflective or static dependency lookup.
- A new bridge across Paper, Velocity, web, Discord, or Cloud.

## Module and Package Ownership

### Module Rules

- Shared contracts belong in shared API modules.
- Paper classes stay in Paper/server modules.
- Velocity classes stay in proxy modules.
- Web classes stay in web modules.
- Discord classes stay in Discord modules.
- Mode-specific code stays in the owning mode module.
- A module does not import a platform adapter merely because that adapter currently provides the only implementation.
- Cross-module access goes through a stable interface or typed request/result boundary.
- Runtime module classes must not leak into stable parent code unless the parent explicitly owns that contract.

### Package Rules

Packages describe ownership and role.

Preferred package shapes:

```text
<domain>/data
<domain>/request
<domain>/result
<domain>/handler
<domain>/service
<domain>/resolver
<domain>/router
<domain>/registry
<domain>/cache
<domain>/repository
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

Rules:

- Avoid broad packages such as `util`, `misc`, `common`, or `manager` for new code.
- Place an interface in the same owning domain as its implementation or in an `interfaces` child package when the domain already uses that shape consistently.
- Package names do not repeat redundant hierarchy.
- Data and implementation packages do not import platform adapters.
- A package should not become a dumping ground for unrelated lifecycle phases.

## Naming and Class Roles

Use names that state the exact job.

| Suffix | Role |
| --- | --- |
| `Handler` | Performs focused domain behavior or handles one input family |
| `Service` | Coordinates a cohesive domain capability |
| `Orchestrator` | Coordinates several focused collaborators across a workflow |
| `Router` | Selects and delegates to handlers |
| `Resolver` | Derives one typed answer from inputs |
| `Registry` | Owns typed runtime lookup state |
| `Cache` | Owns bounded or expiring fast-access state |
| `Repository` | Owns persistence access |
| `Builder` | Assembles or builds a result; does not become a service locator |
| `Mapper` | Converts between representations |
| `Serializer` | Converts typed data to a serialized representation |
| `Reader` | Reads a source |
| `Writer` | Writes a source |
| `Publisher` | Publishes events or updates |
| `Consumer` | Consumes queued, streamed, or published data |
| `Listener` | Adapts platform events into domain behavior |
| `Bootstrap` | Wires startup and lifecycle ownership |
| `Runtime` | Owns a live generation or active system lifecycle |
| `Timer` | Owns actual time progression or timer state |

Avoid `Manager` unless maintaining an external established API that cannot be changed.

### One Class, One Coherent Reason to Change

A class may coordinate several collaborators when they belong to one workflow. It should not own unrelated domains because they happen to run on the same thread or share a player UUID.

Split when a class mixes:

- Persistence and presentation.
- Authorization and rendering.
- Routing and business mutation.
- Cache ownership and unrelated event handling.
- Several independent command families.
- Several independent lifecycle phases.
- Platform adaptation and durable domain rules.

Do not split by creating forwarding wrappers with no independent policy, behavior, or lifecycle. A responsibility split moves behavior and ownership into a focused class.

## Interfaces and Abstraction

Use an interface when there is a real substitution boundary:

- Platform adapter.
- Persistence implementation.
- Distributed versus local implementation.
- Test fake.
- Module boundary.
- External provider.
- Strategy or policy family.

Do not create an interface solely because a class exists. Interfaces should communicate stable capabilities.

Rules:

- Consumers depend on the narrowest stable interface.
- Implementations may also be registered under their concrete type when diagnostics or explicit advanced access require it.
- Interface methods use typed requests, results, keys, states, and domain data.
- Avoid `Object`, arbitrary maps, and raw strings when a stable type exists.
- Abstract classes provide real shared behavior or lifecycle, not naming prestige.

## Dependency Injection

Project Novus uses `tavall-di` as the default runtime composition system.

### Direct Typed Access

For ordinary classes with a small coherent dependency set, use expanded `DependencyAccess`.

Production source: [`MessageRenderHandler`](minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/message/render/MessageRenderHandler.java)

```java
@DelegatesTo(IMessageRenderHandler.class)
public final class MessageRenderHandler
        implements IMessageRenderHandler,
        DependencyAccess<
                IMessageRegistryHandler,
                IPlaceholderResolver,
                IMessageStyleResolver
        > {

    @Override
    public MessageRenderResult render(MessageRenderRequest request) {
        IDependencyMap dependencies = getInstance();
        Optional<MessageMetaData> messageMetaData = dependencies
                .iMessageRegistryHandler()
                .find(request.lookupKey());
        // focused rendering behavior
    }
}
```

Rules:

- Use generated typed getters rather than repeated raw class-token lookup.
- Capture `getInstance()` once when a method reads several dependencies.
- Use `findInstance(...)` only when the dependency is intentionally optional.
- Missing required dependencies fail fast.
- Do not use reflective dependency lookup in normal production paths.

### After Four Dependencies

More than four dependencies is a design review signal, not a hard runtime limit.

Choose one of these patterns:

#### Keep Expanded Direct Access

Use when the class remains cohesive and the dependencies all serve one narrow behavior.

Production source: [`MessageSynchronizationHandler`](minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/message/sync/MessageSynchronizationHandler.java)

```java
@DelegatesTo(IMessageSynchronizationHandler.class)
public final class MessageSynchronizationHandler
        implements IMessageSynchronizationHandler,
        DependencyAccess<
                IMessagePostgresRepository,
                IMessageRedisProjectionHandler,
                IMessageRedisSnapshotHydrationHandler,
                IMessageRegistryHandler,
                IMessageRedisUpdatePublisher,
                IMessageKeyBootstrapHandler
        > {
    // one synchronization workflow
}
```

#### Use a Domain Bundle

Use a bundle when several collaborators form one durable domain boundary used by multiple consumers.

A valid bundle:

- Has a domain name.
- Contains cohesive collaborators.
- Is immutable.
- Does not perform service lookup.
- Is not a second dependency container.
- Is registered and replaced as one lifecycle unit.

```java
public record AccountLinkDependencies(
        AccountLinkAccess accountLinkAccess,
        AccountProviderRegistry accountProviderRegistry,
        AccountLinkTokenHandler accountLinkTokenHandler,
        AccountLinkPolicy accountLinkPolicy
) {
}
```

A bundle must not be named `Dependencies`, `Services`, or `Context` without a real domain prefix.

#### Split Responsibilities

Split when the class owns several distinct behaviors or lifecycle phases.

Production source: [`BuildingInteractionService`](minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/building/BuildingInteractionService.java)

The service delegates debug permission, selection, state mutation, and UI rendering to focused collaborators rather than retaining one giant dependency surface.

### Managed Concrete Registration

Managed concrete implementations declare their interface aliases with `@DelegatesTo`.

```java
@DelegatesTo(IMessageRenderHandler.class)
public final class MessageRenderHandler implements IMessageRenderHandler {
}
```

Rules:

- The concrete class token is implicit.
- Every delegated type must be assignable from the concrete.
- Register one object identity under every alias.
- Replace and remove aliases atomically.
- Do not add injectable marker interfaces to new code.
- Existing marker interfaces are migration debt, not templates.

### Composition Ownership

- Every dependency map has one clear owner.
- Module generations use isolated maps.
- Stable parent code must not retain child-generation objects after unload.
- Replacement tears down the previous owner before publishing the new one when state must not overlap.
- Constructors may accept immutable object state, configuration, builder inputs, or genuinely externally owned platform handles. Tavall-managed application dependencies are not constructor-injected into ordinary production behavior classes.
- Production dependency lookup resolves through the owning `IDependencyMap`.

### DI Anti-Patterns

#### Dependency Constructor Injection

Do not constructor-inject Tavall-managed application dependencies into ordinary production handlers, services, orchestrators, routers, listeners, repositories, or other DI-managed behavior classes.

Anti-pattern:

```java
@DelegatesTo(IMessageRenderHandler.class)
public final class MessageRenderHandler implements IMessageRenderHandler {
    private final IMessageRegistryHandler messageRegistryHandler;
    private final IPlaceholderResolver placeholderResolver;
    private final IMessageStyleResolver messageStyleResolver;

    public MessageRenderHandler(
            IMessageRegistryHandler messageRegistryHandler,
            IPlaceholderResolver placeholderResolver,
            IMessageStyleResolver messageStyleResolver
    ) {
        this.messageRegistryHandler = messageRegistryHandler;
        this.placeholderResolver = placeholderResolver;
        this.messageStyleResolver = messageStyleResolver;
    }
}
```

Why this is rejected:

- It moves dependency-graph ownership into constructor callers instead of the owning `IDependencyMap`.
- It captures dependency identities at construction time and can bypass Tavall DI replacement, reload, and generation semantics.
- It encourages manual wiring trees and test-only construction paths that drift from production composition.
- It makes lifecycle ownership less visible and easier to leak across module generations.

Use the normal `tavall-di` access style instead:

```java
@DelegatesTo(IMessageRenderHandler.class)
public final class MessageRenderHandler
        implements IMessageRenderHandler,
        DependencyAccess<
                IMessageRegistryHandler,
                IPlaceholderResolver,
                IMessageStyleResolver
        > {

    @Override
    public MessageRenderResult render(MessageRenderRequest request) {
        IDependencyMap dependencies = getInstance();
        Optional<MessageMetaData> messageMetaData = dependencies
                .iMessageRegistryHandler()
                .find(request.lookupKey());
        // focused rendering behavior
    }
}
```

Constructors are still normal Java construction tools for immutable object state, configuration, builder inputs, and externally owned platform handles that are not Tavall-managed application dependencies. Builders and composition objects may use constructors while assembling objects; they must not turn constructor injection into a parallel application dependency system.

#### Static Dependency Access

Do not turn static methods into a second dependency system.

Tavall-managed runtime behavior resolves through the owning DI map. Focused default instance methods may expose that DI-backed behavior for readability, but they must continue to resolve through the owning dependency access rather than a static service locator.

Allowed static calls are narrow and dependency-free: constants, pure value parsing or transformation, private pure helpers, and factory/builder entry points that only construct or configure returned values.

A static `builder()`, `of(...)`, `from(...)`, or `create(...)` call is allowed when it is only construction syntax. It is not allowed to resolve managed dependencies, perform I/O, access mutable runtime state, schedule work, or become a hidden composition root.

Platform and application utilities that touch server state, messaging, effects, persistence, caches, scheduling, networking, or other runtime behavior remain instance dependencies and route through DI. Wrap third-party static APIs behind an injected boundary when they carry runtime behavior or need substitution.

Detailed static-access examples: [Validation, Fallbacks, and Anti-Patterns](code-architecture/VALIDATION_FALLBACKS_AND_ANTI_PATTERNS.md#static-dependency-access-pattern)

### Dependency Injection Rejections

Do not:

- Constructor-inject Tavall-managed application dependencies into ordinary production behavior classes.
- Add static service locators.
- Add global mutable dependency maps.
- Use reflection for normal dependency access.
- Inject one giant application object into every class.
- Replace a broad bundle with another broad bundle under a better name.
- Resolve dependencies inside data records.
- Let a child module register objects in a stable parent map without explicit ownership.

Detailed examples: [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md)

## Builders

Builders assemble typed output. They do not become services, repositories, or dependency containers.

Use a builder when:

- Construction has several optional values.
- Validation belongs at build time.
- Defaults are meaningful behavior.
- The result is immutable or expensive to assemble.

Rules:

- Builder methods return the builder.
- The build method returns the final typed result.
- Validation happens before publication.
- Required values fail clearly.
- Defaults are tested.
- A builder does not save to a repository unless the class is explicitly a persistence workflow builder and the name states that role.
- A builder does not resolve arbitrary dependencies.

Do not create a builder for a two-field record with one obvious constructor.

## Handlers, Services, Orchestrators, and Routers

### Handler

A handler owns one focused behavior or input family.

Examples:

- `MessageRenderHandler`
- `ResourceAssignmentHandler`
- `BuildingUpgradeTimerHandler`
- `ResourcePackStatusListener`

### Service

A service coordinates a cohesive domain capability.

Examples:

- `BuildingUpgradeService`
- `FarmProductionService`
- `StorageService`
- `CurrencyService`

### Orchestrator

An orchestrator coordinates several focused collaborators across a workflow. It does not absorb their implementation details.

Use an orchestrator when:

- Several domain steps must run in order.
- Compensation or recovery spans several components.
- The workflow crosses persistence, cache, event, or platform boundaries.

### Router

A router chooses a handler and delegates.

Rules:

- Paper and Velocity events route through the event router.
- Command routers select command families; they do not implement every command.
- A router does not own durable state.
- Unknown routes return an explicit result or documented no-op.
- Route registration has duplicate policy.

## Data, Requests, Results, and Typed Keys

Use immutable records for data transfer and operation boundaries.

### Requests

A request contains inputs needed to perform one operation.

```java
public record MessageRenderRequest(
        MessageLookupKey lookupKey,
        Map<String, String> placeholders
) {
}
```

### Results

A result represents expected operation outcomes.

```java
public record MessageRenderResult(
        boolean success,
        Component component,
        MessageRenderFailureType failureType
) {
}
```

Use exceptions for infrastructure failure or violated invariants, not every expected rejection.

### Typed Keys

Use typed keys for:

- Registry identity.
- Cache dimensions.
- Message lookup.
- Achievement identity.
- Timer identity.
- Distributed idempotency.
- Cross-platform routing.

Avoid composite string concatenation when a record can represent the key.

```java
public record MessageLookupKey(
        String messageKey,
        Locale locale,
        MessagePlatformType platformType
) {
}
```

### Metadata Maps

Metadata maps are allowed at integration edges where fields are intentionally extensible.

Rules:

- Core identity and behavior fields remain typed.
- Metadata keys are documented constants when reused.
- Metadata is not a substitute for a domain model.
- Persistence JSONB metadata is validated before use.

## Methods

Methods should:

- Do one clear operation.
- Use verb names.
- Keep validation near the entry boundary.
- Return typed results.
- Avoid hidden global mutation.
- Keep blocking I/O away from Paper and Velocity event threads.

Prefer:

```java
findByPlayerId(UUID playerId)
savePlayerProfile(PlayerProfileData data)
resolveDestination(RegionRoutingRequest request)
publishState(ServerStateData state)
```

Avoid:

```java
doThing()
process()
handleData()
managePlayer()
getOrCreateAndSaveAndPublish()
```

A long method is reviewed for phase extraction. Do not split a method into private one-line wrappers solely to reduce line count.

## Validation and Mutation Ordering

Validate before mutation.

For multi-step mutation:

1. Validate request shape.
2. Resolve required dependencies.
3. Check authorization and invariants.
4. Prepare durable mutation.
5. Commit the authoritative store.
6. Update caches and registries.
7. Publish events or projections.
8. Return a typed result.

If a system intentionally uses a different order, document the authority and recovery policy.

Do not publish partial state when one duplicate key, missing dependency, or invalid field can be detected first.

## Concurrency and Async Work

Project Novus uses Tavall concurrency tools and platform schedulers according to ownership.

Rules:

- Do not block Paper or Velocity event threads with database, Redis, network, filesystem, or long computation work.
- Use `AsyncTask` or the owning scheduler abstraction for asynchronous work.
- Use virtual-thread-compatible blocking I/O where the owning tool expects it.
- Return to the platform thread before mutating Bukkit or proxy state that requires it.
- Every scheduled or async operation has cancellation or lifecycle ownership.
- Module unload cancels generation-owned work.
- Futures and tasks are not automatically caches or registries.
- Cross-thread mutable state uses thread-safe structures or one-thread ownership.

Do not add arbitrary executors to individual handlers. Reuse the owning concurrency boundary.

## Events and Data Flow

### Paper and Velocity Events

- Route through the project event router.
- Listeners adapt platform events into typed domain calls.
- Listeners do not perform durable I/O directly.
- Cancellation and priority policy are explicit.
- Event publication does not hide required mutation failure.

### Distributed Events

- Use typed payloads.
- Include event identity, source, timestamp, and schema version where relevant.
- Consumers are idempotent or explicitly document duplicate behavior.
- Retry and dead-letter ownership are defined.
- Redis streams, pub/sub, PostgreSQL outbox, and Cloud events are not interchangeable.

### User-Facing Messages

All user-facing messages route through the message system unless the architecture explicitly defines a bootstrap or fatal-fallback exception.

Do not hardcode player-facing strings inside domain services.

## Schemas

Schemas encode contracts between code, persistence, cache, messages, and distributed runtimes. They are not just SQL syntax wearing a tie.

### Schema Categories

| Category | Purpose | Example |
| --- | --- | --- |
| Definition | Configurable rules and presentation | `chat_formats`, `message_config`, achievement definitions |
| State | Current durable gameplay or account state | player profile, currency, castle state |
| Audit | Append-oriented history | purchase events, rating events, timer audits |
| Projection | Derived read model | Redis server state, Discord feed projection |
| Runtime | Ephemeral active state | in-memory registry entries, active offers |

### PostgreSQL Tables

Prefer minimal schemas with typed core columns and JSONB for extensible data.

Rules:

- Identity, ownership, status, timestamps, and indexed query fields are typed columns.
- Extensible settings, metadata, snapshots, and versioned payloads may use JSONB.
- Enums are represented consistently.
- Every table has one clear authority.
- Unique constraints enforce real identity.
- Indexes match real query patterns.
- JSONB is not used to avoid modeling core identity.
- Production schema evolution uses checked-in migrations.
- Runtime code does not create, alter, or probe production schema.

Definition example:

```sql
CREATE TABLE chat_formats (
    format_key TEXT PRIMARY KEY,
    channel_type TEXT NOT NULL,
    format_json JSONB NOT NULL,
    enabled BOOLEAN NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
```

### `message_config`

The message system is a first-class schema domain.

Rules:

- Message identity is typed by key, locale, and platform.
- Delivery, style, content, placeholder schema, metadata, hash, and timestamps are explicit.
- PostgreSQL owns durable definitions.
- Redis may project hot message state.
- Registry state is a runtime projection.
- Message synchronization defines durable and projection ordering.

### Schema Versioning

- Serialized distributed payloads include schema version where compatibility matters.
- Readers reject unsupported required versions explicitly.
- Migrations are ordered and repeatable according to the owning migration tool.
- Schema compatibility is tested across rolling deployment boundaries.

## PostgreSQL, JPA, and Tavall Database

JPA through `tavall-database` is the normal PostgreSQL repository boundary.

Rules:

- Configure every managed entity package in the owning database composition.
- Repositories consume `IPostgresDatabase.jpa()` or `IPostgresJpaContext`.
- `tavall-database` owns provider bootstrap, transactions, entity managers, read-only enforcement, operation draining, and shared factory lifecycle.
- Repositories return domain data or explicit persistence results, not entities to normal handlers.
- Ordinary lookup, insert, update, and delete use typed JPA entities and queries.
- Native SQL is reserved for database-specific contracts such as PostgreSQL `ON CONFLICT`, JSONB operators, locking, bulk mutation, or aggregation that JPA cannot express cleanly.
- Every native query has a nearby `Native SQL reason:` comment.
- Repositories do not create or close shared `EntityManagerFactory` instances.
- Commands, listeners, controllers, runtime support classes, and gameplay services never open JDBC connections.
- Production schema changes are migrations; `generateSchema(true)` is test or development behavior only.
- Runtime `CREATE TABLE IF NOT EXISTS` is prohibited outside explicitly baselined migration debt.
- PostgreSQL-specific behavior receives PostgreSQL integration coverage.

Production entity: [`NovusWebContentDocumentEntity`](novus-web/src/main/java/org/tavall/novus/web/content/entity/NovusWebContentDocumentEntity.java)

```java
@Entity
@Table(name = "novus_web_content_document")
public class NovusWebContentDocumentEntity {
    @Id
    private String documentKey;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode documentJson;
}
```

Production repository boundary: [`PostgresNovusWebContentStore`](novus-web/src/main/java/org/tavall/novus/web/content/PostgresNovusWebContentStore.java)

```java
return database.jpa().read(entityManager -> Optional.ofNullable(
        entityManager.find(
                NovusWebContentDocumentEntity.class,
                documentKey
        )
));
```

The storage audit baseline tracks existing JDBC, DDL, factory-owner, and native-query debt. Existing debt may shrink; new unapproved debt fails validation.

## Redis

Redis is a distributed runtime tool, not automatically durable authority.

Use Redis for:

- Hot projections.
- Coordination.
- Leases and locks.
- Streams and pub/sub.
- Short-lived sessions.
- Cross-server routing state.
- Rate limits and bounded distributed counters.

Rules:

- Every key family has an owner, prefix, value schema, and TTL policy.
- Missing keys have defined behavior.
- Stale values have defined behavior.
- Required durable writes do not become optional because Redis succeeded.
- Redis fallback does not silently change authority.
- Reconciliation source is explicit.

Do not store required permanent truth only in Redis unless the architecture explicitly assigns Redis that authority and defines recovery.

## Registries

Registries own typed runtime lookup state.

Use a registry for:

- Loaded definitions.
- Providers and strategies.
- Active runtime objects.
- Player or module sessions without TTL semantics.
- Typed indexes over current process state.

Rules:

- Use `tavall-registry`.
- Use typed keys and values.
- Expose domain methods.
- Return immutable snapshots.
- Define duplicate and replacement policy.
- Validate all ownership before publication.
- Use `AbstractIndexedRegistry` when one value has secondary indexes that must remain synchronized.
- Aggregate parallel maps keyed by the same identity into one typed session when they represent one lifecycle.
- Clear generation-owned state on unload.
- Callers do not use inherited generic map methods as the domain API.

Production simple registry: [`AccountProviderRegistry`](minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/account/provider/AccountProviderRegistry.java)

Production indexed registry: [`BattleInstanceRegistry`](minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java)

Do not:

- Maintain secondary indexes through independent `put()` and `remove()` choreography.
- Mutate a registered value in a way that invalidates its indexes.
- Use a registry as durable authority accidentally.
- Return mutable internal collections.
- Quietly replace another module's provider.

## Caches

Process-local TTL caches use `tavall-cache`.

Rules:

- Define authority, hit, miss, stale, and negative-cache behavior.
- Use typed key dimensions.
- Define TTL explicitly.
- Define quit, reconnect, reload, and shutdown behavior.
- Clear generation-owned caches on unload.
- Restore dirty or retry state when a durable write fails.
- Use Tavall Cache live snapshots and filtered invalidation for grouped state instead of maintaining a shadow key map.
- A cache never becomes durable authority by convenience.

Production TTL cache: [`FFARegionPromptCooldownCache`](novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/cache/FFARegionPromptCooldownCache.java)

Production typed grouped cache: [`BattleAbilityCooldownCache`](minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleAbilityCooldownCache.java)

Small bounded helper indexes may remain focused helpers when they have explicit add, remove, and snapshot ownership and store no durable identity. [`OnlinePlayerNameCompletionCache`](minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/identity/OnlinePlayerNameCompletionCache.java) is the current narrow example.

Do not hide an unbounded map inside a handler and call it temporary.

## Repositories

Repositories own persistence mechanics.

Rules:

- Depend on repository interfaces across substitution boundaries.
- Use Tavall Database-provided JPA and lifecycle.
- Own transactions, queries, entity mapping, idempotency, and failure translation.
- Keep database-specific native operations narrow and documented.
- Return domain data or explicit persistence results.
- Do not send messages, mutate Bukkit objects, or decide gameplay outcomes.
- Do not own shared factory shutdown.
- Do not create schema at runtime.

## Files

Use files for:

- Static configuration.
- Checked-in definitions.
- Local development fixtures.
- Explicit backup/export formats.

Rules:

- File authority is explicit.
- Reload behavior is explicit.
- Writes are atomic when required.
- Corrupt data has typed failure behavior.
- Runtime module files are owned by the module lifecycle.
- Files are not used as an invisible fallback for failed durable writes.

## Storage Classification

Every map-like field is classified by behavior:

1. State that must survive restart uses a repository.
2. Disposable or reloadable state with expiry, misses, or staleness uses a cache.
3. Loaded definitions, providers, strategies, sessions, or current runtime ownership use a registry.
4. Parallel indexes use an indexed registry or one aggregate.
5. Futures, scheduled tasks, pending writes, queues, and cancellation handles remain operation state with explicit teardown.
6. Static immutable lookup tables and DTO metadata remain immutable collections.
7. In-memory repository substitutes remain repositories.

The validation runner prints loose map candidates as cache-shaped, registry-shaped, operation state, or review-required state.

## Cross-Storage Mutation

For PostgreSQL-authoritative mutation, the normal order is:

```text
validate
  -> commit PostgreSQL
  -> update or invalidate Redis/cache/registry
  -> publish typed result or event
```

Any different order documents:

- Source of truth.
- Idempotency key.
- Durable commit boundary.
- Retry owner and lifetime.
- What callers observe during partial failure.
- Cache or registry restoration.
- Reconciliation source.
- Audit and rollback behavior.

A failed required durable write cannot be reported as success because an in-memory map accepted the value.

Detailed examples: [Registries, Caches, and Repositories](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md)

## Platform Boundaries

### Paper

- Bukkit object mutation occurs on the owning server thread unless the API explicitly permits otherwise.
- Listeners adapt and delegate.
- Paper classes do not become durable domain models.
- Plugin disable closes module-owned resources.

### Velocity

- Proxy commands and events delegate into shared domain boundaries.
- Connection and routing state is explicit.
- Proxy code does not import Paper classes.
- Transfer authorization and server registry state remain typed.

### Web

- Controllers adapt HTTP input and output.
- Controllers do not own business rules or persistence mechanics.
- Web views consume typed view models.
- Authentication and authorization are separate from rendering.

### Discord

- Discord events adapt into typed requests.
- Outbox or durable event boundaries own retry.
- Discord delivery failure does not roll back unrelated committed gameplay state unless the workflow explicitly requires it.

### Tavall Cloud

- Cloud clients use typed operations and results.
- Authorization is exact and temporary where required.
- Deployment state is version guarded.
- Runtime sandboxes have explicit isolation, logs, cleanup, and artifact ownership.

## Lifecycle and Cleanup

Every long-lived object has an owner.

Define:

- Who creates it.
- Where it is registered.
- Who closes it.
- Whether close is idempotent.
- What happens during replacement.
- What happens during partial startup.
- What happens during module unload.
- Whether async work drains or cancels.

Use `AutoCloseable` for resources with explicit shutdown when appropriate.

Close order normally reverses construction order.

Do not leave generation-owned caches, listeners, tasks, registries, threads, classloaders, database contexts, or Redis subscriptions reachable after unload.

## Error Handling and Fallbacks

### Expected Rejections

Return typed results for expected outcomes:

- Not found.
- Unauthorized.
- Invalid state.
- Cooldown active.
- Insufficient currency.
- Duplicate request.
- Unsupported route.

### Infrastructure Failures

Throw or propagate an operation-specific exception for:

- Database failure.
- Redis failure when required.
- Serialization corruption.
- Invariant violation.
- Missing required dependency.
- Failed deployment or authorization.

### Fallback Rules

- A fallback has an owner and a reason.
- A fallback cannot report success for a failed required write.
- Fallback state is observable.
- Recovery and reconciliation are defined.
- Avoid broad `catch (Exception)` with silent continuation.
- Log enough typed context to diagnose the operation without leaking secrets.

## Testing

Test real behavior at the narrowest meaningful boundary.

### Unit Tests

Use unit tests for:

- Policies.
- Resolvers.
- Builders.
- Typed state transitions.
- Duplicate validation.
- Serialization.

### Integration Tests

Use integration tests for:

- PostgreSQL and JPA behavior.
- Redis behavior.
- DI map registration and cleanup.
- Registry index rollback.
- Cache TTL, live snapshots, and grouped invalidation.
- Module loading and unloading.
- Paper and Velocity adapters when practical.

### Simulation Tests

Use simulation for:

- Full plugin lifecycles.
- Combat and rating flows.
- Timers and retries.
- Distributed routing.
- Player join, quit, reconnect, transfer, and cleanup.

Rules:

- Test class names match the production class plus `Test`.
- Test package structure matches production package structure.
- Cover success, rejection, failure, cleanup, retry, expiry, shutdown, reload, and reconciliation where those paths exist.
- PostgreSQL-specific behavior receives PostgreSQL integration coverage.
- DI tests verify implicit concrete bindings, alias metadata identity, source lowering, map isolation, replacement, and teardown.
- Registry and cache tests verify duplicate policy, immutable snapshots, TTL, misses, stale state, and lifecycle cleanup.
- Validation reports state exactly what ran and what remains untested.

## Extended Architecture Chapters

The chapter directory retains detailed examples and specialized rules. This document remains the binding authority.

| Chapter | Extended detail |
| --- | --- |
| [Dependency Injection and Orchestration](code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md) | Module scopes, cleanup, compatibility, and orchestration |
| [Registries, Caches, and Repositories](code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md) | State classification, production examples, JPA, indexed registries, cache TTL, failure, and migration rules |
| [Testing and Git Discipline](code-architecture/TESTING_AND_GIT.md) | Test structure, commit boundaries, and branch expectations |

## Architecture Review Checklist

Before accepting a change, confirm:

- [ ] The owning module and package are correct.
- [ ] Shared code does not import platform adapter types.
- [ ] Interfaces and handler packages follow the owning child-package rules.
- [ ] Class and method names describe exact roles and actions.
- [ ] Dependency-injected behavior depends on interfaces where a real substitution boundary exists.
- [ ] Managed concretes use `@DelegatesTo`; their concrete token is implicit.
- [ ] Every additional delegated token is assignable from the concrete.
- [ ] New DI code does not require injectable marker interfaces.
- [ ] Classes with two to four managed dependencies normally use expanded `DependencyAccess`.
- [ ] Every larger declaration identifies why direct access, a domain bundle, or a responsibility split is correct.
- [ ] Domain bundles name a real durable boundary and do not become second containers or object bags.
- [ ] Responsibility splits move behavior into focused owners instead of adding forwarding wrappers around an oversized class.
- [ ] Production dependency lookup resolves through the owning `IDependencyMap`.
- [ ] Tavall-managed application dependencies are not constructor-injected into ordinary production behavior classes.
- [ ] Static calls do not locate, cache, or own Tavall-managed runtime dependencies; allowed statics stay pure or construction-only.
- [ ] Constructor parameters are limited to object state, configuration, builder inputs, or genuinely externally owned handles outside the Tavall DI dependency graph.
- [ ] Builders build or assemble; they do not save, authorize, or become service locators.
- [ ] Handlers, routers, commands, and listeners retain their distinct responsibilities.
- [ ] Tavall tools are reused instead of recreated.
- [ ] Every loose map is classified as registry, cache, operation state, immutable snapshot, or repository substitute.
- [ ] Runtime keyed state uses typed registries or caches.
- [ ] Parallel indexes mutate through `AbstractIndexedRegistry` or one aggregate.
- [ ] Cache TTL, misses, live snapshots, invalidation, and lifecycle ownership are explicit.
- [ ] JPA through Tavall Database is the normal PostgreSQL boundary.
- [ ] Native SQL has a nearby database-specific reason.
- [ ] Runtime code does not create schema or open JDBC connections.
- [ ] Repositories do not create or close shared persistence factories.
- [ ] Durable, cached, distributed, runtime, and file authority are explicit.
- [ ] PostgreSQL, Redis, registries, caches, repositories, and files follow documented ownership.
- [ ] Cross-storage ordering and recovery are defined.
- [ ] Async work does not block Paper or Velocity threads.
- [ ] Lifecycle, cancellation, recovery, cleanup, and rollback behavior are defined.
- [ ] Requests, results, keys, states, and expected failures are typed.
- [ ] Validation happens before mutation.
- [ ] Tests exercise real contracts and meaningful boundaries.
- [ ] Exact validation and remaining gaps are recorded honestly.
- [ ] Java examples link to real checked-in classes.
- [ ] Documentation ownership and links remain valid.
