# Tavall Registries, Caches, and Persistence

> **Status:** Active  
> **Authority:** Detailed chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall application modules, contributors, automation, generated code, reviews, and AI-assisted development

This chapter classifies runtime, cached, distributed, operation, and durable state. The file name retains `REPOSITORIES` only for link/history compatibility. **Repository is not an approved Tavall application class role.**

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
4. Do several indexes describe one identity? Use an indexed registry or typed aggregate.
5. Is it in-flight work? Give it a typed operation/runtime owner with teardown.
6. Is it a bounded method-local transform? Keep it local if it never escapes.
7. Is it a value snapshot? Make it immutable.

Do not route durable state into a new `*Repository` merely because the state is keyed.

## Tavall Registry

Use `tavall-registry` for runtime lookup ownership.

Rules:

- typed keys/values;
- domain methods rather than backing-map APIs;
- duplicate/replacement policy;
- immutable snapshots;
- generation cleanup;
- `AbstractIndexedRegistry` when secondary indexes must remain coherent;
- aggregate parallel maps when they represent one lifecycle.

Infrastructure registries may own maps internally. Consumers do not.

##### Why

A registry is a lifecycle/identity owner, not a prettier `Map`. Domain methods let one owner preserve indexing, replacement, validation, snapshot, and unload invariants.

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

- registry duplicate/replacement/index rollback;
- immutable snapshots and unload cleanup;
- cache hit/miss/TTL/stale/invalidation/cleanup;
- Tavall Database entity behavior and database-specific contracts using the current module test surface;
- Redis/distributed partial failures and reconciliation;
- operation cancellation/shutdown;
- migration enforcement preventing new `*Repository` production types.

A test that requires persistence substitution should use the test/entity facilities provided by the current Tavall Database module or a correctly named domain-capability fake. Do not create an `InMemory*Repository` merely to make a test convenient.
