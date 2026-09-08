# Tavall Registries, Caches, and Durable State

> **Status:** Active  
> **Authority:** Detailed chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall application modules, contributors, automation, generated code, reviews, and AI-assisted development

This chapter explains how keyed and durable state is classified. Storage names are not decoration. They state authority, lifetime, replacement, recovery, and cleanup behavior.

Project Novus production classes are used as concrete examples because they exercise these boundaries heavily. The ownership rules are shared Tavall rules.

# Classify State Before Naming It

Use the behavior of the state, not the current field name.

| Boundary | Use it when | Authority | Normal lifetime |
| --- | --- | --- | --- |
| Tavall Registry | Typed definitions, providers, strategies, active runtime ownership, or keyed session state need domain lookup | Process/generation runtime only unless explicitly projected from durable state | Owning runtime generation |
| Tavall Cache | State is disposable, reloadable, stale-able, or time-limited and exists to avoid work | Never durable authority | Entry TTL and owning generation |
| Tavall Database entity / typed operation | State must survive restart and is durable application truth | Authoritative durable store | Database lifecycle |
| Redis / distributed-state boundary | State coordinates processes, streams, leases, locks, sessions, or distributed projections | Only when explicitly assigned | Cross-process key policy |
| Typed operation/runtime owner | Futures, scheduled tasks, pending writes, cancellation handles, retries, or other in-flight state need lifecycle ownership | Operation/runtime only | Until completion, cancellation, or owner teardown |
| Immutable value/snapshot | A built value is passed to consumers and never mutated through that value | Source that built it | Value/snapshot owner |
| Repository | A real stable domain persistence/substitution contract exists beyond ordinary Tavall Database entity CRUD | Contract-dependent | Contract owner |

##### Why

The same `Map<K,V>` can technically hold every category in this table, but the categories have different authority, lifetime, failure, cleanup, and recovery semantics. Choosing the boundary from behavior first prevents the collection implementation from silently deciding the architecture.

Losing a cache entry is a miss. Losing registry state may require runtime reconstruction. Losing Tavall Database state is durable data loss. Cancelling an operation should clear its in-flight state. Those are not interchangeable events merely because all four can be keyed.

## Keyed-State Classification Test

When a class contains a mutable `Map`, `Set`, or parallel keyed collections, answer these questions in order:

1. **Must the value survive restart?** Use a mapped entity or typed durable operation through Tavall Database, or another explicitly selected durable provider.
2. **Can the value be discarded and rebuilt?** Use Tavall Cache when expiry, misses, or stale values are meaningful.
3. **Does the value represent loaded definitions, provider ownership, or active keyed runtime identity?** Use Tavall Registry.
4. **Do several indexes address the same runtime value?** Use `AbstractIndexedRegistry` or one typed aggregate.
5. **Is it an in-flight future, task, pending write, queue item, cancellation handle, or retry?** Give it a dedicated typed operation/runtime owner with explicit teardown. Do not hide it in an ordinary consumer.
6. **Is it a bounded immutable snapshot or static constant table?** Keep it immutable.
7. **Is there genuinely a persistence substitution/domain contract beyond Tavall Database entity CRUD?** A repository may own that contract. Do not create one merely because persistence exists.

A map named `data`, `state`, `entries`, `sessions`, `operations`, or `pending` still receives this review. Renaming the evidence has yet to defeat architecture.

##### Why

The test forces ownership questions before implementation convenience. Without it, temporary state becomes a cache, caches become unofficial truth, operation maps become permanent runtime registries, and ordinary CRUD gets wrapped in application repositories because someone wanted another class between the caller and the database.

## Narrow Non-Owner Collections

The application-owned mutable-map rule does not require turning every temporary collection into infrastructure.

Allowed narrow cases include:

- method-local grouping or transformation maps that never escape the method;
- immutable DTO/record metadata where the map itself is genuinely part of the value;
- static immutable lookup tables;
- internal indexes inside a dedicated Registry/Cache/Tavall Database/distributed-state implementation;
- typed operation/runtime owners whose in-flight collections exist solely to manage that owner's lifecycle.

An ordinary handler, service, orchestrator, listener, command, controller, or adapter does **not** gain a raw-map exception merely by calling the field `pendingOperations`.

##### Why

Local algorithmic collections have no independent lifecycle. Dedicated runtime owners do. The distinction prevents ceremony for harmless local work while still stopping long-lived keyed state from leaking back into consumers through a newly fashionable noun.

# Tavall Registry

Tavall runtime lookup state uses `tavall-registry`. Normal consumers call domain methods, not inherited map methods.

## Simple Typed Registry

Use `AbstractRegistry<K,V>` when one primary key owns one runtime value and no secondary index must remain synchronized.

Project Novus production source: [`AccountProviderRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/backend/account/provider/AccountProviderRegistry.java)

```java
public final class AccountProviderRegistry
        extends AbstractRegistry<AccountProviderType, AccountProviderAdapter> {

    public Optional<AccountProviderAdapter> find(
            AccountProviderType providerType
    ) {
        return Optional.ofNullable(getRegistryData(providerType));
    }
}
```

##### Why

A registry represents runtime ownership, not merely fast lookup. Publishing one validated key-to-value relation gives duplicate policy, replacement, snapshots, and unload cleanup one owner.

Domain lookup methods also prevent ordinary consumers from depending on backing-collection mechanics.

## Aggregate Parallel State

Several maps keyed by the same identity usually represent one aggregate.

Project Novus production source: [`ResourceGameplayStateTracker`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/resource/gameplay/ResourceGameplayStateTracker.java)

The production registry stores a typed `ResourceGameplaySession` rather than publishing selected-node, operation, and assignment maps independently.

##### Why

Parallel maps allow one logical state to be partly updated or partly cleared. A typed aggregate gives mutation, snapshotting, validation, and cleanup one coherent value.

## Atomic Secondary Indexes

Use `AbstractIndexedRegistry<K,V>` when one runtime value is found through several keys. Validate first, then publish the primary value and secondary indexes through one lifecycle.

Project Novus production source: [`BattleInstanceRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java)

`BattleInstanceRegistry` owns secondary `battleIdByPlayerId` and `participantByPlayerId` maps internally. Those maps are allowed because the registry owns their invariants and updates them with primary registration/removal.

##### Why

Secondary indexes are only correct while they agree with the primary value. Independent map mutation creates contradictory lookup results. One indexed-registry lifecycle can validate, publish, roll back, and remove all indexes atomically.

## Registry Rules

- Return immutable snapshots.
- Sort snapshots when order is part of the caller contract.
- Define duplicate and replacement policy.
- Clear generation-owned state on unload.
- Remove secondary indexes through the same lifecycle as primary state.
- A registry may project durable data, but it does not become durable authority.
- Register the concrete/interface through Tavall DI when other components consume it.
- Consumers call domain methods; they do not treat the registry as a generic `Map` API.

Do not:

- maintain indexes through unrelated `put()` calls;
- expose mutable internal maps or collections;
- use raw composite strings when a typed key exists;
- quietly replace another module's provider/strategy;
- store TTL-shaped data indefinitely because the class already says `Registry`.

##### Why

A registry is useful only while one owner controls runtime identity coherently. Raw mutation, hidden indexes, or TTL drift creates alternate write/lifecycle paths that invalidate that promise.

# Tavall Cache

Process-local cache state uses `tavall-cache`. A cache improves access; it does not decide durable truth.

Project Novus production source: [`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java)

```java
public PlayerAchievementData getOrLoad(
        UUID playerId,
        Function<UUID, PlayerAchievementData> loader
) {
    ICacheKey<UUID> key = cacheKey(playerId);
    return get(key, ignored -> loader.apply(playerId), onlineTtlMillis);
}
```

The loader reads authoritative persistence. It does not recursively call the cache.

## Cache Rules

A cache defines:

- authoritative source;
- hit, miss, stale, and negative-cache behavior;
- TTL and any per-state variation;
- quit/reconnect/reload/shutdown behavior where applicable;
- dirty-state/retry restoration when a durable write fails;
- group invalidation without shadow key maps;
- one lifecycle owner.

Use typed key dimensions where domain, type, source, or version distinguish meaning.

Use Tavall Cache live snapshots/filtered invalidation instead of maintaining a second key collection merely for iteration.

Do not:

- cache `null` without explicit negative-cache policy;
- treat process lifetime as a replacement for generation lifetime;
- treat Redis or local cache data as durable truth by convenience;
- hide an unbounded cache-shaped map in a handler;
- duplicate cache entries into a second mutable map for iteration.

##### Why

A cache is defined as much by miss, expiry, invalidation, and cleanup as by lookup. Centralizing those mechanics keeps stale/reload behavior consistent and preserves the core property that cached state can disappear without changing durable truth.

# Tavall Database and Durable State

For PostgreSQL-backed Tavall applications, **Tavall Database is the durable persistence runtime**.

Ordinary durable operations use mapped entities and the typed Tavall Database entity boundary:

```java
Optional<MyEntity> entity = database.entities().find(MyEntity.class, id);
database.entities().save(entityToSave);
```

Application code must not use `database.jpa().read(...)`, `database.jpa().write(...)`, `IPostgresJpaContext` callbacks, `EntityManager` callbacks, raw JDBC, or local transaction wrappers.

Mapped entities own normal query definitions through named JPQL. Named native operations are reserved for documented PostgreSQL contracts such as `ON CONFLICT`, JSONB operators, locking, bulk mutation, or aggregation that JPA cannot express cleanly.

For multi-entity transaction behavior, add/use a typed Tavall Database operation. Do not recreate callback ownership in application code.

Detailed rules: [Entity Persistence](ENTITY_PERSISTENCE.md).

##### Why

Provider bootstrap, entity discovery, transactions, entity managers, operation draining, and shutdown are one infrastructure lifecycle. Feature code should request durable behavior, not become a miniature persistence runtime.

# Repository Exception

Repositories are not Tavall's default persistence layer.

Do **not** create `Postgres*Repository`, `*Database`, `*Store`, or equivalent ordinary CRUD wrappers around `database.entities()`.

A repository is valid only when there is a genuine stable domain persistence/substitution contract beyond ordinary entity CRUD, such as:

- an external provider family;
- multiple interchangeable persistence implementations;
- a cohesive persistence capability whose contract has domain semantics not equivalent to generic `find/save/delete`.

Even then:

- consume typed Tavall Database/provider operations;
- do not own `EntityManager`, JPA callbacks, JDBC, schema creation, or shared factory lifecycle;
- expose domain persistence methods rather than generic storage plumbing;
- keep unrelated product rules outside the repository.

In-memory repository implementations remain valid test/development substitutes **only when the production architecture genuinely has that repository contract**. They are not a reason to invent a repository around ordinary entity CRUD.

##### Why

A pass-through repository duplicates Tavall Database and immediately creates another place for query, transaction, failure, and mapping policy to diverge. Repository abstraction earns its existence only when there is an actual contract to substitute.

# Redis and Distributed State

Redis may own explicitly assigned distributed runtime semantics such as hot projections, streams, leases, locks, short-lived distributed sessions, coordination, routing state, or bounded counters.

Every Redis key family defines:

- owner/prefix;
- value schema;
- TTL where relevant;
- stale/missing behavior;
- reconciliation source;
- whether Redis is authority or projection.

Do not turn a failed required Tavall Database write into success because Redis accepted a value.

##### Why

Redis availability and PostgreSQL durability answer different questions. Explicit authority prevents a convenient projection from becoming an accidental source of truth during failure.

# Cross-Storage Ordering and Failure

For PostgreSQL-authoritative mutation, the normal order is:

```text
validate
  -> commit through Tavall Database
  -> invalidate/update Redis/cache/registry
  -> publish typed result/event
```

Any different order documents:

- source of truth;
- idempotency key;
- durable commit boundary;
- retry owner/lifetime;
- caller-visible partial-failure behavior;
- cache/registry restoration;
- reconciliation source/order;
- audit/rollback behavior.

A fallback cannot turn a failed required durable write into apparent success. An in-memory recovery buffer is named, bounded, observable, and reconciled; it is not a second authority hidden behind an exception handler.

##### Why

Cross-storage failures create the hardest state bugs because each system can individually be healthy while disagreeing with another. Explicit commit/recovery ordering gives reconciliation one known truth instead of asking runtime timing to decide.

# Migration Debt

Existing application `.jpa()` callback owners, raw JDBC, generic CRUD repositories/database/store wrappers, runtime DDL, and consumer-owned loose keyed stores are migration debt.

Migration rules:

- existing debt may decline;
- new debt must not be added to a baseline;
- when a missing typed Tavall Database operation blocks migration, add it upstream first;
- when a repository adds no domain contract beyond entity CRUD, remove it rather than modernizing its wrapper internals;
- migrate touched code and adjacent coherent paths when practical rather than preserving obsolete examples as templates.

# Testing Requirements

## Registry Tests

Verify:

- typed lookup;
- duplicate-owner rejection before mutation;
- secondary-index replacement/removal;
- rollback after failed index publication;
- immutable/deterministic snapshots where order matters;
- generation cleanup.

## Cache Tests

Verify:

- hit/miss/loader count;
- TTL and logical-clock behavior;
- grouped invalidation;
- live snapshots;
- dirty-state restoration after durable failure;
- close/unload cleanup.

## Tavall Database Tests

Verify:

- empty/populated entity reads;
- save/update/delete behavior;
- transaction rollback through typed operations;
- duplicate/concurrency behavior;
- JSONB/UUID/timestamp/enum mapping;
- PostgreSQL-specific semantics for native operations and migrations;
- application code does not own callbacks/factories/JDBC.

## Operation Runtime Tests

When a runtime owner manages futures/tasks/pending work, verify:

- registration/removal;
- cancellation;
- completion cleanup;
- shutdown/unload teardown;
- no in-flight collection escapes as a general application map API.

# Review Checklist

- [ ] Every keyed mutable field is classified by behavior, not its field name.
- [ ] Registry keys/values are typed and consumers use domain methods.
- [ ] Parallel runtime state is aggregated or indexed atomically.
- [ ] Cache authority, TTL, misses, invalidation, and lifecycle are explicit.
- [ ] Operation/task collections live only in a dedicated typed runtime owner with teardown.
- [ ] Ordinary PostgreSQL CRUD uses Tavall Database entities/typed operations.
- [ ] Application code does not call `.jpa()` callbacks or own `EntityManager`/JDBC/transactions.
- [ ] Generic CRUD repository/database/store wrappers are not added.
- [ ] Any remaining repository represents a real domain persistence/substitution contract.
- [ ] Native PostgreSQL behavior has an explicit reason and focused integration coverage.
- [ ] Runtime code does not create production schema.
- [ ] Cross-storage ordering, retry, rollback, and reconciliation are defined.
- [ ] Tests cover failure and cleanup, not merely successful lookup.
- [ ] Validation states exactly what ran and what remains unverified.
