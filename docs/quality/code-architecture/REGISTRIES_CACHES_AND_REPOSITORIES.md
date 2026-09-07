# Project Novus Registries, Caches, and Repositories

> **Status:** Active  
> **Authority:** Detailed chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter carries the reasoning, production examples, and failure rules behind the binding storage rules in `CODE_ARCHITECTURE.md`. Storage names are not decoration. They state authority, lifetime, replacement, and recovery behavior.

## Example Policy

Every Java example below is a shortened excerpt from linked production code or an owning Tavall tool PR. Examples on the storage migration branch are production candidates until their stacked PRs merge; their validation status must not be overstated.

Do not replace these examples with fictional APIs. Imaginary libraries have exceptional uptime because nobody has attempted to compile them.

# Classify State Before Naming It

Use the behavior of the state, not the current field name.

| Boundary | Use it when | Authority | Normal lifetime |
| --- | --- | --- | --- |
| Tavall Registry | Typed definitions, providers, strategies, active runtime ownership, or keyed session state need domain lookup | Process or generation runtime only, unless paired with persistence | Owning application or module generation |
| Tavall Cache | State is disposable, reloadable, stale-able, or time-limited and exists to avoid work | Never durable authority | Entry TTL and owning generation |
| Redis | State must coordinate processes, carry streams, leases, locks, sessions, or distributed projections | Only when explicitly assigned | Cross-process key policy |
| Repository through Tavall Database | State must survive restart and is durable gameplay, account, configuration, administration, or audit truth | Usually authoritative | Database lifecycle |
| Operation/task state | Futures, scheduled tasks, in-flight writes, cancellation tokens, and retries describe ongoing work | Operation owner | Until completion or cancellation |
| Immutable snapshot or lookup constant | A built immutable value is passed to consumers and never mutated | Source that built it | Snapshot owner |

##### Why

The same `Map<K,V>` can technically hold every category in this table, but the categories have different authority, lifetime, failure, cleanup, and recovery semantics. Choosing the boundary from behavior first prevents the collection implementation from silently deciding the architecture.

Classification also makes failure meaningful: losing a cache entry is a miss, losing registry state may require runtime reconstruction, and losing repository state is durable data loss. Those are not interchangeable events merely because all three can be keyed.

## Loose Map Classification Test

When a class contains a `Map`, `Set`, or parallel keyed collections, answer these questions in order:

1. **Must the value survive restart?** Use a repository and durable schema.
2. **Can the value be discarded and rebuilt?** Use Tavall Cache when expiry, misses, or stale values are meaningful.
3. **Does the value represent loaded definitions, provider ownership, or active keyed runtime state?** Use Tavall Registry.
4. **Do several maps index the same value?** Use `AbstractIndexedRegistry` or a typed aggregate; do not publish indexes independently.
5. **Is it an in-flight future, scheduled task, cancellation handle, or retry?** Keep it with the operation owner and define cancellation. It is not automatically a cache.
6. **Is it a bounded immutable snapshot or static constant table?** Keep it as an immutable collection.
7. **Is it an in-memory repository used only for tests or development?** Keep the repository contract. Do not rename persistence substitution into a registry.

A map named `data`, `state`, `entries`, or `sessions` still receives this review. Humans did not evade architecture by choosing a less incriminating noun.

##### Why

The test forces ownership questions before implementation convenience. Without it, temporary state tends to become a cache, caches become unofficial truth, and in-memory test repositories get renamed into runtime registries even though their contracts still represent durable persistence.

The ordering is intentional: survival, rebuildability, runtime ownership, indexing, and operation lifetime answer different questions that a collection type cannot answer for us.

## Do Not Auto-Migrate These

- Method-local grouping or transformation maps.
- DTO or record metadata fields.
- Static immutable lookup tables.
- Test/dev `InMemory*Repository` implementations.
- Futures, tasks, in-flight writes, and cancellation ownership.
- Immutable composition snapshots such as installed module artifacts.
- Small bounded helper indexes with explicit ownership and no durable identity, such as [`OnlinePlayerNameCompletionCache`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/identity/OnlinePlayerNameCompletionCache.java).

##### Why

Not every collection has an independent lifecycle worth turning into infrastructure. Method-local transforms and immutable snapshots are values or algorithms, while operation handles belong to the workflow that created them.

Blind migration would replace one ownership mistake with ceremony: a registry or cache is useful only when its lifecycle semantics match the state being moved into it.

# Tavall Registry

Project Novus registries use `tavall-registry`. Normal consumers call domain methods, not inherited map methods.

## Simple Typed Registry

Use `AbstractRegistry<K, V>` when one primary key owns one value and no secondary index must remain synchronized.

Source: [`AccountProviderRegistry`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/account/provider/AccountProviderRegistry.java)

```java
public final class AccountProviderRegistry
        extends AbstractRegistry<AccountProviderType, AccountProviderAdapter> {

    public AccountProviderRegistry(List<AccountProviderAdapter> adapters) {
        validateAdapters(adapters);
        adapters.forEach(adapter ->
                createRegistry(adapter.providerType(), adapter)
        );
    }

    public Optional<AccountProviderAdapter> find(
            AccountProviderType providerType
    ) {
        return Optional.ofNullable(getRegistryData(providerType));
    }
}
```

The constructor validates the complete provider set before publication. Two providers cannot silently claim the same type.

##### Why

A registry represents runtime ownership, not merely fast lookup. Publishing one validated key-to-value relation gives duplicate policy, replacement, snapshots, and unload cleanup one owner.

Domain lookup methods also prevent ordinary consumers from depending on the registry's backing collection mechanics, which keeps future registry implementation changes from leaking through the application.

## Aggregate Parallel State Before Registering It

Three maps keyed by the same player are usually one session aggregate.

Source: [`ResourceGameplayStateTracker`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/resource/gameplay/ResourceGameplayStateTracker.java)

```java
public final class ResourceGameplayStateTracker
        extends AbstractRegistry<UUID, ResourceGameplaySession> {

    public void selectedNodeId(UUID playerId, UUID nodeId) {
        mutate(playerId, session -> session.withSelectedNodeId(nodeId));
    }

    private void mutate(
            UUID playerId,
            UnaryOperator<ResourceGameplaySession> mutation
    ) {
        compute(playerId, (ignored, existing) -> {
            ResourceGameplaySession current = existing == null
                    ? new ResourceGameplaySession(null, null, null)
                    : existing;
            ResourceGameplaySession updated = mutation.apply(current);
            return updated.isEmpty() ? null : updated;
        });
    }
}
```

This prevents selected node, operation, and assignment state from being updated or cleared independently.

##### Why

Parallel maps usually reveal one logical value split across several collections. Independent mutation allows those pieces to drift, leaving combinations of state that the domain never intended to exist.

A typed aggregate makes one mutation replace one coherent session value and gives serialization, snapshots, validation, and cleanup a single unit to reason about.

## Atomic Secondary Indexes

Use `AbstractIndexedRegistry<K, V>` when one value is found through several keys. Validate first, then publish the primary value and every secondary index through one lifecycle.

Owning tool source: [`AbstractIndexedRegistry`](https://github.com/TavallStudios/tavall-registry/blob/agent/atomic-indexed-registry/src/main/java/org/tavall/registry/AbstractIndexedRegistry.java)

```java
public abstract class AbstractIndexedRegistry<K, V>
        extends AbstractRegistry<K, V> {

    protected void validateRegistration(K key, V value, V previous) {
    }

    protected abstract void index(K key, V value);

    protected abstract void unindex(K key, V value);
}
```

The base routes `put`, `remove`, `replace`, `compute`, `merge`, and clear operations through validation, indexing, unindexing, and rollback.

Production consumer: [`BattleInstanceRegistry`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java)

```java
public final class BattleInstanceRegistry
        extends AbstractIndexedRegistry<UUID, BattleInstance> {
    private final Map<UUID, UUID> battleIdByPlayerId =
            new ConcurrentHashMap<>();
    private final Map<UUID, BattleParticipant> participantByPlayerId =
            new ConcurrentHashMap<>();

    @Override
    protected void index(UUID battleId, BattleInstance battle) {
        battle.participants().forEach((playerId, participant) -> {
            battleIdByPlayerId.put(playerId, battleId);
            participantByPlayerId.put(playerId, participant);
        });
    }

    @Override
    protected void unindex(UUID battleId, BattleInstance battle) {
        battle.participants().forEach((playerId, participant) -> {
            battleIdByPlayerId.remove(playerId, battleId);
            participantByPlayerId.remove(playerId, participant);
        });
    }
}
```

A player conflict is rejected before mutation. Failed secondary-index publication restores the previous primary value and indexes.

##### Why

Secondary indexes are only correct while they agree with the primary value. If callers can mutate them independently, lookup results depend on which index happened to be updated or cleaned up successfully.

Atomic index ownership makes registration and rollback one operation, so a failure cannot publish half a registry state and leave later callers debugging two mutually contradictory truths.

## Registry Snapshots and Lifecycle

- Return immutable snapshots.
- Sort snapshots when order is part of the caller contract.
- Clear module-generation state on unload.
- Remove secondary indexes through the same lifecycle as primary state.
- A registry may project durable data, but it does not become durable authority.
- Register the concrete and interface through Tavall DI when other components consume the registry.

Production examples:

- [`FFAActivePlayerSessionRegistry`](../../../novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionRegistry.java)
- [`KingdomActivePlayerSessionRegistry`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/player/session/KingdomActivePlayerSessionRegistry.java)
- [`PaperNovusEntityRuntimeRegistry`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/customentity/PaperNovusEntityRuntimeRegistry.java)
- [`FFARegionSwitchOfferRegistry`](../../../novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/FFARegionSwitchOfferRegistry.java)
- [`InMemoryCastleLocationRegistry`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/backend/kingdom/castle/cache/InMemoryCastleLocationRegistry.java)

##### Why

Snapshots are observation boundaries, not alternate mutation APIs. Immutability prevents a caller from changing registry state without going through duplicate policy, indexing, or lifecycle hooks.

Generation cleanup is equally important: runtime ownership that survives unload has become a leak or accidental global. Registry lifetime must follow the component that owns the registered values.

## Registry Rejections

Do not:

- Maintain two or more indexes with unrelated `put()` calls.
- Mutate a registered value in a way that invalidates its indexes.
- Expose mutable internal maps or collections.
- Use raw composite strings when a typed key exists.
- Quietly replace another module's provider or strategy.
- Store TTL state indefinitely because the class already has `Registry` in its name.

##### Why

Every rejection protects the registry's claim that one owner controls runtime identity coherently. Raw mutation and unrelated indexes create alternate write paths; TTL state changes lifetime semantics; silent replacement changes ownership without an explicit policy.

A registry remains useful only while every mutation preserves the invariants its lookup methods promise.

# Tavall Cache

Project Novus process-local cache state uses `tavall-cache`. A cache improves access; it does not decide truth.

## Typed Key Dimensions

Use domain, type, source, and version dimensions where they distinguish meaning.

Source: [`FFARegionPromptCooldownCache`](../../../novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/cache/FFARegionPromptCooldownCache.java)

```java
private static final CacheDomain DOMAIN = CacheDomain.ROUTES;
private static final CacheType TYPE = CacheType.MEMORY;
private static final CacheSource SOURCE = CacheSource.MINECRAFT;
private static final CacheVersion VERSION = CacheVersion.V1_0;

public Instant record(UUID playerUUID, Instant promptedAt) {
    put(cacheKey(playerUUID), promptedAt, ttlMillis);
    return promptedAt;
}
```

The configured prompt cooldown is also the entry TTL. Player quit removes the entry and module shutdown clears the cache.

##### Why

Typed key dimensions prevent unrelated cache entries from colliding merely because they share a primitive identifier. They also make version, source, and domain part of the contract instead of hiding those distinctions in naming conventions or string concatenation.

When those dimensions matter to invalidation or migration, making them explicit lets the cache enforce the distinction consistently.

## Cache-Aside and Dirty-State Recovery

Source: [`PlayerAchievementCache`](../../../novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java)

```java
public PlayerAchievementData getOrLoad(
        UUID playerId,
        Function<UUID, PlayerAchievementData> loader
) {
    ICacheKey<UUID> key = cacheKey(playerId);
    return get(key, ignored -> loader.apply(playerId), onlineTtlMillis);
}
```

The loader reads authoritative persistence. It does not recursively call the cache. When a durable write fails, the owning data handler restores dirty markers and retry state before rethrowing.

##### Why

Cache-aside works only when misses have a clear authoritative source and failed durable writes cannot be mistaken for successful cache updates. Recursive loading or silent dirty-state loss creates loops and false success paths that are difficult to reconcile later.

Keeping the loader authoritative and retry ownership explicit preserves the core cache promise: cached state can disappear without changing durable truth.

## Grouped Cache Invalidation

Grouped TTL state uses a typed key and Tavall Cache live snapshots instead of maintaining a second key collection.

Source: [`BattleAbilityCooldownKey`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleAbilityCooldownKey.java)

```java
public record BattleAbilityCooldownKey(
        UUID playerId,
        UUID battleId,
        UUID companionId,
        UUID abilityId
) {
}
```

Source: [`BattleAbilityCooldownCache`](../../../minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleAbilityCooldownCache.java)

```java
public int removeBattle(UUID battleId) {
    return removeIf((ignored, state) ->
            battleId.equals(state.battleId())
    );
}

public List<BattleAbilityCooldownState> activeFor(
        UUID playerId,
        UUID battleId
) {
    return snapshotValues().stream()
            .filter(state -> playerId.equals(state.playerId()))
            .filter(state -> battleId.equals(state.battleId()))
            .toList();
}
```

Owning tool source: [`AbstractCache`](https://github.com/TavallStudios/tavall-cache/blob/agent/live-entry-snapshots/abstract-cache-system/src/main/java/org/tavall/abstractcache/cache/AbstractCache.java)

The cache tool owns expiration, live snapshots, and filtered removal. Domain code owns the meaning of the filter.

##### Why

A shadow key collection is a second index with its own cleanup problem. Expiration can remove the cache entry while leaving the shadow key behind, or manual invalidation can update one structure without the other.

Using the cache's live snapshot keeps expiration and membership under one owner while letting domain code express grouped meaning through typed predicates.

## Cache Rules

A cache defines:

- Authoritative source.
- Hit, miss, stale, and negative-cache behavior.
- TTL and any per-state TTL variation.
- Quit, reconnect, reload, and shutdown behavior.
- Dirty-state and retry restoration when durable writes fail.
- Group invalidation without shadow key maps.
- One lifecycle owner.

Do not:

- Cache `null` without an explicit negative-cache policy.
- Use process lifetime for generation-owned data.
- Treat Redis or local cache data as durable truth by convenience.
- Hide an unbounded map in a handler.
- Duplicate cache entries in a second map for iteration.

##### Why

A cache is defined as much by miss, expiry, invalidation, and cleanup behavior as by `get` and `put`. Leaving those rules implicit means callers invent their own interpretation of stale or absent data and the cache stops being a coherent boundary.

One lifecycle owner makes restart, reload, and failed-write behavior deterministic instead of depending on which consumer last touched the entry.

# Tavall Database and Repositories

Repositories own durable persistence mechanics. JPA through `tavall-database` is the normal PostgreSQL boundary.

## Shared JPA Runtime

Owning tool source: [`IPostgresJpaContext`](https://github.com/TavallStudios/tavall-database/blob/agent/jpa-context-runtime/tavall-database-postgres/src/main/java/org/tavall/database/postgres/jpa/IPostgresJpaContext.java)

```java
public interface IPostgresJpaContext extends AutoCloseable {
    EntityManagerFactory entityManagerFactory();

    <T> T read(Function<EntityManager, T> operation);

    <T> T write(Function<EntityManager, T> operation);
}
```

`tavall-database` owns provider bootstrap, configured entity-package discovery, transaction begin/commit/rollback, entity-manager closure, read-only enforcement, operation draining, and factory lifecycle.

Repositories do not create or close shared factories. Module-local transaction wrappers are compatibility seams only and should be deleted as consumers move to `IPostgresDatabase.jpa()` or `IPostgresJpaContext`.

##### Why

An `EntityManagerFactory` and transaction runtime are shared process resources. Multiple owners create competing shutdown, configuration, connection-pool, and transaction semantics inside one application.

Centralizing the runtime in Tavall Database lets repositories focus on durable operations while provider lifecycle and draining remain consistent for every caller.

## JPA Entity

Source: [`NovusWebContentDocumentEntity`](../../../novus-web/src/main/java/org/tavall/novus/web/content/entity/NovusWebContentDocumentEntity.java)

```java
@Entity
@Table(name = "novus_web_content_document")
public class NovusWebContentDocumentEntity {
    @Id
    @Column(name = "document_key", nullable = false, length = 64)
    private String documentKey;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "document_json", nullable = false,
            columnDefinition = "jsonb")
    private JsonNode documentJson;
}
```

Persistence entities live under the owning domain's persistence or entity package. Repositories map them to domain data; normal handlers and adapters do not receive entities.

##### Why

Entities expose storage mapping details that ordinary domain consumers should not need to understand. Passing entities through handlers couples application behavior to JPA annotations, lazy-loading assumptions, and schema shape.

Mapping at the persistence boundary keeps the domain model usable even when the durable representation changes.

## JPA Repository Boundary

Source: [`PostgresNovusWebContentStore`](../../../novus-web/src/main/java/org/tavall/novus/web/content/PostgresNovusWebContentStore.java)

```java
private <T> Optional<T> loadDocument(
        String documentKey,
        Class<T> documentType
) {
    return database.jpa().read(entityManager -> Optional.ofNullable(
                    entityManager.find(
                            NovusWebContentDocumentEntity.class,
                            documentKey
                    )
            )
            .map(NovusWebContentDocumentEntity::getDocumentJson)
            .map(json -> convertDocument(documentKey, json, documentType)));
}
```

The store no longer opens JDBC connections, creates tables, or maintains separate H2 and PostgreSQL write paths.

##### Why

A repository/store should own persistence semantics for its domain, not database bootstrap or schema lifecycle. Removing connection creation and runtime DDL prevents each repository from becoming a miniature database platform with its own test and shutdown behavior.

It also keeps provider-specific differences in the database layer instead of branching ordinary write behavior by environment.

## Native SQL Exception

Native SQL is allowed only when JPA or JPQL cannot express the required database contract cleanly, such as:

- PostgreSQL `ON CONFLICT` atomic upsert.
- JSONB path/operator mutation.
- Advisory or row locking.
- Bulk update or insert where entity loading is wrong.
- PostgreSQL-specific aggregation or indexing behavior.

Every native query includes a nearby `Native SQL reason:` comment. Ordinary lookup, insert, update, and delete use typed JPA entities and queries.

Source: [`MessagePostgresRepository`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/message/postgres/MessagePostgresRepository.java)

```java
// Native SQL reason: PostgreSQL ON CONFLICT atomically owns the
// message-key, locale, and platform composite identity.
entityManager.createNativeQuery("""
        INSERT INTO message_config (...)
        VALUES (...)
        ON CONFLICT (message_key, locale, platform_type) DO UPDATE SET ...
        """);
```

##### Why

Native SQL is valuable when PostgreSQL semantics are the actual requirement, but it bypasses some of the typed mapping and portability benefits of JPA. Requiring a nearby reason makes the tradeoff explicit and reviewable.

That keeps native queries narrow instead of allowing ordinary CRUD to drift back into ad hoc SQL simply because it was locally convenient.

## Schema Ownership

Production schema evolution uses checked-in migration scripts.

Source: [`022_novus_web_content_document.sql`](../../../novus-web/src/main/resources/schema/postgres/022_novus_web_content_document.sql)

Rules:

- No runtime `CREATE TABLE IF NOT EXISTS` in repositories, services, handlers, controllers, or listeners.
- `generateSchema(true)` is test/development behavior only.
- Migrations own columns, constraints, indexes, data backfills, and compatibility transitions.
- Repository code does not inspect `DatabaseMetaData` to select between historical production shapes. Migrate the schema instead.
- PostgreSQL-specific semantics receive PostgreSQL integration tests. H2 may test provider-neutral entity mechanics, not impersonate every PostgreSQL feature through a growing branch maze.

##### Why

Schema changes are durable production events that require ordering, review, rollback planning, and a record of what changed. Runtime DDL hides that history inside application startup and makes two instances capable of racing to define infrastructure.

Checked-in migrations give every environment the same transition path and let repository code target one known current schema instead of carrying branches for every historical shape forever.

## Repository Rules

A repository:

- Uses Tavall Database-provided JPA and database lifecycle.
- Owns transactions, queries, entities, mapping, and low-level failure translation.
- Returns domain data or explicit persistence results.
- Keeps database-specific native operations narrow and documented.
- Keeps transaction boundaries visible.
- Defines idempotency and duplicate behavior.

A repository does not:

- Decide rewards, authorization, combat, or presentation.
- Send messages or mutate Bukkit objects.
- Create or close a shared `EntityManagerFactory`.
- Open JDBC from a command, listener, controller, runtime support class, or gameplay service.
- Swallow a failed durable write and report success.

##### Why

Repositories are durable-state boundaries. Giving them gameplay, presentation, or platform responsibilities makes those rules depend on persistence and hides domain behavior behind storage calls.

Visible transaction and failure semantics are especially important because callers must know whether a durable mutation committed. A repository that swallows failure or performs unrelated side effects makes reconciliation and retry correctness impossible to reason about.

# Cross-Storage Ordering and Failure

For PostgreSQL-authoritative mutation, the normal order is:

```text
validate
  -> commit PostgreSQL
  -> invalidate or update Redis/cache/registry
  -> publish typed result or event
```

Any different order is documented by the owning system.

A flow touching several stores defines:

- Source of truth.
- Idempotency key.
- Transaction or durable commit boundary.
- Retry owner and retry lifetime.
- What callers observe during partial failure.
- Cache/registry restoration when persistence fails.
- Reconciliation source and ordering.
- Audit and rollback behavior.

A fallback cannot turn a failed required write into apparent success. An in-memory recovery buffer is named, bounded, observable, and reconciled; it is not a second authority hidden behind `catch (SQLException)`.

##### Why

Once a mutation crosses several stores there is no single local transaction protecting all of them. The order therefore determines which system is allowed to be temporarily stale and which failure must be repaired.

Committing authoritative persistence first prevents a cache or event from advertising state that never became durable. Explicit retry and reconciliation ownership turns partial failure into a recoverable state instead of an accidental second source of truth.

# Migration Inventory

This architecture pass establishes the destination and migrates representative production paths. Existing debt is tracked rather than blessed.

## Migrated in This Stack

- Account providers and active FFA/Kingdom sessions use Tavall Registry.
- Resource gameplay parallel maps are one registry session aggregate.
- UI, command-mode, resource-pack, custom-entity, traveler, and outbox maps use Tavall Registry.
- Battle instances, region offers, castle ownership, and custom items use atomic indexed registries.
- FFA region prompt throttling and battle ability cooldowns use Tavall Cache.
- FFA and message transaction mechanics delegate to Tavall Database.
- Novus web JSONB documents use a JPA entity and checked-in migration.
- Composite builds can validate exact Tavall Database, Cache, and Registry revisions.

## Explicit Remaining Migration Debt

- Kingdom and shared backend JDBC repositories require a stable entity-package catalog in the Paper persistence composition before JPA entities can be discovered safely.
- Account-link, achievement, rank, identity, commerce, resource-pack, kingdom, companion, resource, timer, and interior repository families still contain raw JDBC.
- FFA repositories still use native tuples for several ordinary reads; those reads should become entities while PostgreSQL JSONB/upsert mutations remain narrow native operations.
- SQL still present outside repository packages is P0 extraction work.
- Multi-index companion, combat-attribution, focused-engagement, and active-render registries require the indexed lifecycle plus careful handling of Redis or platform side effects.
- Futures, scheduled tasks, and in-flight write maps require cancellation/lifecycle review rather than cache conversion.

The storage audit baseline may contain these known classes so validation can ratchet: existing debt may be removed, but new unapproved JDBC, runtime DDL, or loose storage maps fail the audit.

##### Why

A migration inventory distinguishes accepted destination architecture from known compatibility debt. Without that distinction, old code is easily mistaken for a current production pattern simply because it still exists and compiles.

A ratcheting baseline lets large migrations proceed incrementally while preventing new work from increasing the debt being removed.

# Testing Requirements

## Registry Tests

Verify:

- Typed lookup.
- Duplicate-owner rejection before mutation.
- Secondary-index replacement and removal.
- Rollback after failed index publication.
- Immutable and deterministic snapshots where order matters.
- Generation cleanup.

## Cache Tests

Verify:

- Hit, miss, and loader count.
- TTL and logical-clock behavior.
- Quit/reconnect behavior.
- Group invalidation.
- Live snapshot behavior.
- Dirty-state restoration after durable failure.
- Close and unload cleanup.

## Repository Tests

Verify:

- Empty and populated reads.
- Persist and update behavior.
- Transaction rollback.
- Duplicate and concurrency behavior.
- JSONB, UUID, timestamp, and enum mapping.
- Factory and entity-manager ownership.
- Real PostgreSQL semantics for native SQL and migrations.

##### Why

The most dangerous storage failures are ownership and failure-path bugs, not successful `get` and `put` calls. These tests prove duplicate policy, expiry, rollback, cleanup, and transaction semantics where the boundary earns its architectural complexity.

Testing only the happy path would verify that the collection or database library works while leaving Tavall's actual ownership guarantees untested.

# Review Checklist

- [ ] Every loose map was classified by behavior, not its field name.
- [ ] Registry keys and values are typed.
- [ ] Parallel state was aggregated or indexed atomically.
- [ ] Duplicate and replacement behavior is explicit.
- [ ] External snapshots are immutable and deterministic where required.
- [ ] Cache authority, miss behavior, TTL, and lifecycle are explicit.
- [ ] No cache maintains a shadow map merely for iteration.
- [ ] JPA through Tavall Database is the normal PostgreSQL path.
- [ ] Every native query states its database-specific reason.
- [ ] Runtime code does not create schema or open JDBC connections.
- [ ] Repositories do not own shared factory shutdown.
- [ ] Cross-storage ordering, retry, rollback, and reconciliation are defined.
- [ ] Tests cover failure and cleanup, not merely successful lookup.
- [ ] Validation states exactly what ran and what remains unverified.