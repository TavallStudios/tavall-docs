# Application-Owned Mutable Maps

> **Status:** Active  
> **Authority:** Binding supporting chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production application code, reviews, generation, automation, and AI-assisted development

Application-owned mutable maps are prohibited by default.

The rule is about **ownership**, not whether Java's `Map` type is inherently bad. Tavall Registry, Tavall Cache, Tavall Database/persistence infrastructure, distributed-state adapters, dedicated runtime-operation owners, and other canonical infrastructure may use maps internally. Ordinary application consumers should not recreate those systems with `HashMap`, `ConcurrentHashMap`, `ConcurrentMap`, mutable `Set`, or parallel keyed collections.

A mutable keyed collection in a handler, service, orchestrator, router, listener, command, controller, ordinary gateway/adapter, or similar consumer is a violation candidate by default.

## Classification Rule

Before introducing mutable keyed state, classify what the state actually is:

- **Runtime identity, definitions, sessions, active objects, providers, strategies, or keyed process state** -> Tavall Registry.
- **Expiring, reloadable, stale-able, disposable, or fast-access state** -> Tavall Cache.
- **Durable state that must survive restart** -> mapped entity or typed durable operation through Tavall Database, or another explicitly selected durable provider.
- **Distributed/shared runtime state** -> the owning Redis/distributed-state abstraction.
- **Several indexes over one runtime identity** -> `AbstractIndexedRegistry` or one typed aggregate.
- **In-flight futures, scheduled tasks, pending writes, retries, queues, cancellation handles** -> a dedicated typed operation/runtime owner with explicit teardown.
- **Short-lived operation payload/result/value** -> typed `*Data`, `*Request`, `*Result`, `*State`, or `*MetaData`.
- **Real persistence substitution/domain contract beyond ordinary Tavall Database entity CRUD** -> Repository, only when that contract genuinely exists.

If a collection represents something engineers can name, model the named thing instead of adding a mutable map.

##### Why

Classification prevents implementation details from deciding architecture by accident. A `ConcurrentHashMap` can hold sessions, cooldowns, durable records, tasks, or retries, but those categories have different lifecycle, expiry, persistence, replacement, recovery, and test requirements.

Naming the ownership category first routes the state into the system that already owns those semantics.

## Rejected Consumer Pattern

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

This is a registry implemented locally inside a consumer. Thread safety does not change the ownership problem.

Project Novus production already demonstrates the correct ownership shape in [`FFAActivePlayerSessionRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionRegistry.java).

##### Why

A consumer should own behavior, not silently become the storage primitive for that behavior. A registry gives keyed runtime state one lifecycle/domain owner and one API for duplicate policy, replacement, cleanup, indexing, and snapshots.

## Cache-Shaped State

```java
private final Map<UUID, CooldownData> cooldowns =
        new ConcurrentHashMap<>();
```

is cache-shaped state when entries expire, become stale, reload, or are disposable. Use Tavall Cache rather than hand-rolling lifecycle and invalidation behavior.

Project Novus production source: [`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java).

##### Why

Cache behavior is more than fast lookup. Expiry, invalidation, stale handling, reload behavior, statistics, and cleanup become duplicated policy when every consumer owns a private map.

## Durable State Is Tavall Database State

A mutable application map is never a durable-state substitute merely because a future save is planned.

Ordinary PostgreSQL durable state uses Tavall Database:

```java
Optional<PlayerAccountEntity> entity =
        database.entities().find(
                PlayerAccountEntity.class,
                playerUUID
        );

database.entities().save(entityToSave);
```

Do not route durable keyed state into a generic `Postgres*Repository`, `*Database`, or `*Store` wrapper merely to avoid the map. That replaces one unnecessary ownership layer with another.

A repository is valid only when it represents a real stable persistence/substitution contract beyond ordinary Tavall Database entity CRUD.

##### Why

Durability has transaction, rollback, migration, recovery, and process-lifecycle semantics. Tavall Database already owns those mechanics. A map or pass-through CRUD repository cannot become durable authority by naming convention.

## Data Handler and Persistence Policy

A data handler may coordinate Tavall Database and cache behavior when several consumers genuinely need one shared data policy, such as cache-aside load, dirty-state retry, batching, mapping, or retention.

A data handler is not mandatory around every entity operation and must not recreate JPA callbacks, JDBC, or generic repository mechanics.

##### Why

Cache/persistence coordination can be real reusable behavior, but wrapper layers should exist because policy exists, not because every durable operation is expected to march through a predetermined class stack.

## Operation Runtime State

In-flight state sometimes needs a mutable collection:

```text
futureByOperationId
taskByPlayerId
pendingWriteByKey
cancellationByOperationId
```

That state is allowed only inside a **dedicated typed operation/runtime owner** whose job includes registration, completion removal, cancellation, shutdown, and cleanup.

Rejected:

```java
public final class RewardHandler {
    private final Map<UUID, CompletableFuture<?>> pending =
            new ConcurrentHashMap<>();
}
```

Preferred ownership shape:

```text
RewardOperationRuntime
RewardTaskRuntime
PendingRewardOperationRegistry  // when registry semantics truly fit
```

The runtime owner exposes operation methods, not its backing map.

##### Why

Futures/tasks are not automatically caches or registries, but they still have lifecycle. Giving them a dedicated runtime owner preserves cancellation/teardown semantics without turning every ordinary handler into a permitted map owner under the phrase “operation state.”

## Data Is Not Runtime Ownership

Maps remain valid inside typed immutable or encapsulated data when the map itself is genuinely part of the value.

Project Novus [`RoundPerformanceGradeResult`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/rating/grading/RoundPerformanceGradeResult.java) snapshots its map:

```java
public record RoundPerformanceGradeResult(
        FFALetterGrade letterGrade,
        double score,
        Map<FFARoundGradeComponent, Double> components
) {
    public RoundPerformanceGradeResult {
        components = Map.copyOf(components);
    }
}
```

Known fields should still become named fields instead of `Map<String,Object>`.

##### Why

Typed data describes a value at a point in time; runtime storage owns changing state across time. Immutable map-valued data does not give callers a mutation channel back into another component's runtime state.

## Method-Local Exception

A method-local mutable map is allowed for a bounded algorithmic transformation when all of the following are true:

- it never escapes the method;
- it is not stored on an object;
- it does not represent registry, cache, durable, distributed, lifecycle, authorization, session, or in-flight runtime ownership;
- key/value types are concrete and meaningful;
- replacing it with a named type would not improve the domain contract.

##### Why

A local collection used to group, count, sort, or transform values has no independent lifecycle to architect. Promoting every temporary collection into infrastructure would be ceremony without ownership value.

## Infrastructure Exception

Canonical infrastructure may own mutable maps as implementation details, including:

- Tavall Registry implementations;
- Tavall Cache implementations;
- Tavall Database/persistence internals;
- Redis/distributed-state adapters;
- secondary indexes inside dedicated registry/cache/storage implementations;
- typed operation/runtime owners;
- serialization/integration adapters where the external schema itself is dynamic.

Consumers do not depend on or mutate those backing maps directly.

Project Novus [`BattleInstanceRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java) owns secondary mutable maps internally because the registry owns their invariants.

##### Why

Infrastructure boundaries exist specifically to own mechanics such as maps, indexes, expiry structures, task tables, storage records, and serialization shapes. The mechanics are safe only while the same owner controls their invariants and lifecycle.

## API Rule

Do not expose map operations as the domain API.

Rejected:

```java
registry.getEntries().put(playerId, session);
cache.getMap().remove(playerId);
runtime.pending().compute(operationId, mutation);
```

Prefer focused methods such as:

```text
start(...)
find(...)
invalidate(...)
registerOperation(...)
cancelOperation(...)
applyMutation(...)
snapshot()
```

##### Why

`put`, `compute`, and `remove` describe storage mechanics, not domain intent. Focused methods can express validation, duplicate policy, audit behavior, lifecycle transitions, persistence effects, cancellation, and cache invalidation behind the owning boundary.

## Tavall Registry and Tavall Cache

Shared infrastructure already owns the common map-backed semantics:

- [`tavall-registry` `AbstractRegistry`](https://github.com/TavallStudios/tavall-registry/blob/main/src/main/java/org/tavall/registry/AbstractRegistry.java)
- [`tavall-cache` `AbstractCache`](https://github.com/TavallStudios/tavall-cache/blob/main/abstract-cache-system/src/main/java/org/tavall/abstractcache/cache/AbstractCache.java)

The current `tavall-registry` implementation may still expose raw map methods through inheritance. That is an infrastructure encapsulation concern, not permission for application consumers to use those operations as domain APIs.

##### Why

Shared infrastructure only pays for itself when application code stops reimplementing it. Central ownership also gives architecture tests stable boundaries to enforce instead of inferring intent from thousands of unrelated maps.

## Review Rule

Any new mutable map/set field or parallel keyed collection in production application code requires architecture review and should be rejected unless it is clearly inside an allowed infrastructure/data/operation-runtime boundary.

Strong violation signals include:

- `Map<String,Object>`;
- raw/nested arbitrary maps;
- mutable map fields in ordinary consumers;
- map-shaped behavior APIs;
- durable state buffered indefinitely without Tavall Database authority;
- generic CRUD repositories introduced merely to relocate map-shaped persistence.

##### Why

Mutable keyed state is cheap to add and expensive to unwind once callers depend on its shape. Reviewing ownership at introduction time is far cheaper than discovering later that a convenient map became the unofficial registry, cache, task runtime, persistence layer, and API for half a subsystem.
