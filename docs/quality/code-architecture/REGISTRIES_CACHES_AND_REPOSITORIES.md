# Tavall Registries, Caches, and Persistence

> **Status:** Active  
> **Authority:** Detailed chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall application modules, contributors, automation, generated code, reviews, and AI-assisted development

This chapter classifies runtime, cached, distributed, operation, and durable state. The file name retains `REPOSITORIES` only for link/history compatibility. **Repository is not an approved Tavall application class role.**

## Canonical Tool Authority

`tavall-registry`, `tavall-cache`, `tavall-database`, and the other canonical Tavall Java tool repositories own the API shape and implementation model of their respective tools.

Shared architecture documentation classifies when a tool should be used and records accepted cross-project policy. It must not silently redesign a canonical tool, replace an intentional inheritance model with a generic composition preference, hide supported APIs, or invent a parallel vocabulary because another implementation style appears cleaner in isolation.

Before changing a Tavall Java tool pattern in shared docs:

1. inspect the current canonical repository, its interfaces, tests, and owning documentation;
2. distinguish the tool's supported low-level/framework surface from the preferred application-consumer surface;
3. document the existing accepted pattern first;
4. propose an upstream tool change separately when a real defect or architectural migration is needed.

##### Why

The shared docs are policy for Tavall's actual libraries, not a replacement design exercise for them. If documentation can redefine a library without first reading that library, the docs become a source of architecture drift rather than a guard against it.

## Classify State Before Naming It

| Boundary | Use it when | Authority | Lifetime |
| --- | --- | --- | --- |
| Tavall Registry | Typed definitions, providers, strategies, active objects, sessions, keyed runtime identity | Runtime only | Owning runtime/generation |
| Tavall Cache | State is disposable, reloadable, stale-able, expiring, or exists to avoid work | Never durable authority | TTL + owning lifecycle |
| Tavall Database entity model | State must survive restart and is durable application truth | Durable authority | Database lifecycle |
| Redis/distributed-state boundary | State coordinates processes, streams, leases, locks, sessions, projections | Only when explicitly assigned | Key-family policy |
| Typed operation/runtime owner | Futures, scheduled tasks, in-flight writes, retries, cancellation state | Operation owner | Completion/cancellation |
| Immutable value/snapshot | Built value observed by consumers | Source that built it | Value owner |

##### Why

A collection implementation cannot tell us whether loss means a cache miss, runtime reconstruction, cancelled work, or durable data loss. Classifying semantics first gives state the correct lifecycle and recovery owner.

## Loose Map Classification

Before adding or preserving a mutable keyed collection, ask:

1. Must it survive restart? Use the Tavall Database entity model/current entity contract.
2. Can it be discarded/rebuilt or expire? Use Tavall Cache.
3. Does it represent active keyed runtime identity/definitions/providers/sessions? Use Tavall Registry.
4. Do several lookup dimensions describe one runtime identity? Keep one Registry owner and follow the current `tavall-registry` contract for lookup/view behavior rather than publishing unrelated maps as independent owners.
5. Is it in-flight work? Give it a typed operation/runtime owner with teardown.
6. Is it a bounded method-local transform? Keep it local if it never escapes.
7. Is it a value snapshot? Make it immutable.

Do not route durable state into a new `*Repository` merely because the state is keyed.

## Tavall Registry

Use `tavall-registry` for runtime lookup ownership.

The canonical base deliberately models a registry as a thread-safe map-backed collection. `AbstractRegistry<K, V>` extends `ConcurrentHashMap<K, V>` and implements `IAbstractRegistry<K, V>`. That inheritance is an accepted part of the tool contract, not an implementation accident that shared docs should automatically replace with composition.

`IAbstractRegistry` provides Tavall-named registry access such as:

- `createRegistry(key, data)`;
- `getRegistryData(key)`;
- `getRegistryKeyByData(data)`;
- `getRegistryKeysAsSet/List/Collection()`;
- `getRegistryDataAsSet/List/Collection()`;
- `hasRegistryKey(key)`;
- `hasRegistryData(data)`.

These methods are the normal semantic registry-facing vocabulary when they fit the caller. Registry subclasses and framework code may also use the inherited `ConcurrentMap` operations when those operations are the correct implementation mechanism. Do not describe the inherited map contract as forbidden or accidental when the canonical tool intentionally exposes it.

Rules:

- use typed keys and values;
- preserve one clear runtime/lifecycle owner;
- use the established registry-named accessors/views where they express the operation cleanly;
- use inherited map operations inside registry/framework implementation when the canonical contract supports them;
- define duplicate/replacement behavior where domain semantics require more than the underlying map contract;
- clear generation-owned registry state on unload;
- do not expose a second independent mutable map as a competing owner for the same identity;
- do not introduce a new registry abstraction or terminology merely to restate behavior already represented by `AbstractRegistry` / `IAbstractRegistry`.

##### Why

Tavall Registry intentionally combines Java collection interoperability with a clearer registry vocabulary. The named API makes common registry intent readable, while the underlying concurrent-map contract remains available to the tool and advanced/framework code. Replacing that design in documentation adds abstraction cost and can break behavior that the library intentionally supports.

### Multiple Lookup Dimensions

Several lookup dimensions over the same runtime identity still have one Registry owner.

Before adding a new “indexed” abstraction, check whether the canonical registry API already expresses the required lookup or view. For example, `getRegistryKeyByData(...)` already provides reverse key lookup over registered data, and the key/data collection accessors provide registry-named views/snapshots for common traversal needs.

If a concrete registry genuinely requires additional maintained lookup structures for performance or domain-specific identity, those structures are implementation details owned by that registry. Their mutation behavior must remain coherent with the primary registry state across every supported mutation path.

`AbstractIndexedRegistry` currently exists in `tavall-registry`, but shared architecture does **not** treat it as a mandatory replacement for the established Registry model or use it to justify hiding the canonical map contract. Any future promotion, redesign, or removal of that abstraction must be reconciled in `tavall-registry` first and then reflected here.

##### Why

“Indexed” describes one implementation technique. Registry callers care about registry identity and lookup behavior. Keeping implementation terminology subordinate to the canonical Registry vocabulary prevents shared docs from forcing one optimization strategy across every registry.

## Tavall Cache

Use `tavall-cache` for disposable/reloadable/expiring/stale-able fast state.

A cache defines:

- authority/source;
- hit/miss/stale/negative-cache behavior;
- key dimensions;
- TTL;
- invalidation/group removal;
- reconnect/reload/shutdown behavior;
- failed durable-write recovery;
- one lifecycle owner.

Do not maintain shadow key maps for cache iteration when Tavall Cache already owns live snapshots/filtering.

##### Why

Cache semantics are expiry and recovery semantics, not merely lookup. Centralizing them prevents callers from inventing inconsistent stale/miss policies.

## Tavall Database Durable State

For PostgreSQL/JPA-backed Tavall applications, Tavall Database owns durable persistence.

Application code uses **entity classes and the entity persistence contract defined by the checked-in `tavall-database` version**. This chapter intentionally does not name a concrete accessor or reproduce Tavall Database's API.

Application code must not own:

- `EntityManager`/factory lifecycle;
- transaction callbacks/lifecycle;
- raw JDBC transaction wrappers;
- duplicate entity discovery/bootstrap;
- generic CRUD wrappers;
- new Tavall-owned production types ending in `Repository`.

If a durable capability is missing, extend `tavall-database` rather than creating another persistence layer in the consumer repository.

##### Why

The persistence module is the source of truth for its own entity API. Duplicating that API in application docs makes application architecture stale and preserves abstractions after the underlying module changes.

## `*Repository` Is Migration Debt

New Tavall-owned production declared types ending in `Repository` are prohibited.

Existing `*Repository` types may remain temporarily only as explicitly grandfathered migration debt. They are not examples, extension points, substitution templates, or justification for another repository.

Migration rules:

- no new `*Repository` declaration;
- no new `I*Repository` interface;
- no replacement `RepositoryImpl`/`RepositoryAdapter`/`RepositoryStore` layer;
- move ordinary durable behavior to Tavall Database entities/current entity contract;
- move real domain behavior to a correctly named Handler/Service/Orchestrator/Reader/Writer/Gateway/etc. based on its actual responsibility;
- remove legacy types and shrink the executable debt ratchet as migrations land.

##### Why

Grandfathering is for migration, not design. The debt set has one legal direction: down.

## Redis and Distributed State

Redis is not durable authority by convenience.

Every key family defines owner, schema, prefix, TTL/staleness, missing-key behavior, idempotency where relevant, and reconciliation source. Required durable writes do not become successful merely because Redis accepted a projection.

## Operation State

Futures, tasks, retries, pending writes, queues, and cancellation handles are not automatically caches or registries.

When they need keyed mutable ownership, place them inside a dedicated typed operation/runtime owner with explicit teardown. Ordinary handlers/services/orchestrators do not receive a raw-map exception simply because the values are temporary.

## Cross-Storage Mutation

For PostgreSQL-authoritative state, the normal order is:

```text
validate
  -> commit through the current Tavall Database entity contract
  -> update/invalidate Redis/cache/registry projections
  -> publish typed result/event
```

Any different order documents authority, idempotency, durable commit boundary, retry ownership, partial-failure visibility, restoration, reconciliation, audit, and rollback.

## Testing

Cover:

- registry duplicate/replacement behavior when specialized by the concrete registry;
- registry-named key/data views and reverse lookup where used;
- coherence of any registry-owned secondary lookup structures across every supported mutation path;
- unload cleanup;
- cache hit/miss/TTL/stale/invalidation/cleanup;
- Tavall Database entity behavior and database-specific contracts using the current module test surface;
- Redis/distributed partial failures and reconciliation;
- operation cancellation/shutdown;
- migration enforcement preventing new `*Repository` production types.

A test that requires persistence substitution should use the test/entity facilities provided by the current Tavall Database module or a correctly named domain-capability fake. Do not create an `InMemory*Repository` merely to make a test convenient.
