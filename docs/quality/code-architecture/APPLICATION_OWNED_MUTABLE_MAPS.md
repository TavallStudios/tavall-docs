# Application-Owned Mutable Maps

> **Status:** Active  
> **Authority:** Binding supporting chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production application code, reviews, generation, automation, and AI-assisted development

Application-owned mutable maps are prohibited by default.

The rule is about **ownership**, not whether Java's `Map` type is inherently bad. Tavall Registry, Tavall Cache, Tavall Database internals, distributed-state adapters, dedicated operation/runtime owners, and other canonical infrastructure may use maps internally. Ordinary application consumers should not recreate those systems with `HashMap`, `ConcurrentHashMap`, `ConcurrentMap`, mutable `Set`, or parallel keyed collections.

## Classification Rule

Before introducing mutable keyed state, classify the semantics:

- runtime identity/definitions/sessions/providers/strategies -> Tavall Registry;
- expiring/reloadable/stale-able/disposable fast state -> Tavall Cache;
- durable state that must survive restart -> Tavall Database entity classes and the entity persistence contract defined by the checked-in `tavall-database` version;
- distributed/shared runtime state -> owning Redis/distributed abstraction;
- several indexes over one identity -> indexed Registry or one typed aggregate;
- in-flight futures/tasks/retries/cancellation -> dedicated typed operation/runtime owner;
- short-lived payload/result/value -> typed `*Data`, `*Request`, `*Result`, `*State`, or `*MetaData`;
- bounded algorithmic transform that never escapes -> method-local collection.

**`*Repository` is not a classification target.** Do not fix an application-owned map by moving it into a new repository class.

##### Why

The same map can technically store sessions, cooldowns, durable records, or in-flight work, but those categories have different lifecycle, expiry, persistence, recovery, and test requirements. Classification routes the state to the infrastructure that owns those semantics.

## Rejected Consumer Pattern

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions = new ConcurrentHashMap<>();
}
```

This is registry-shaped state owned by a behavior consumer. Thread safety does not solve the ownership problem.

Prefer a focused Registry with domain methods such as `start`, `find`, `remove`, and `snapshot`.

##### Why

The consumer should own behavior, not silently become the lifecycle/storage primitive for that behavior.

## Cache-Shaped State

A map of cooldowns, reloadable definitions, stale-able data, or disposable fast state is cache-shaped. Use Tavall Cache so TTL, invalidation, stale behavior, misses, snapshots, and cleanup have one owner.

##### Why

Cache behavior is more than lookup. Hand-rolled maps duplicate expiry and invalidation policy while losing the shared lifecycle semantics Tavall Cache already provides.

## Durable State

If the state must survive restart, model it through **Tavall Database entity classes and the current entity persistence contract owned by `tavall-database`**.

This chapter deliberately does not prescribe a concrete accessor. It also does not permit an application `*Repository` wrapper around Tavall Database.

##### Why

Durable persistence mechanics belong to Tavall Database. A mutable map or repository wrapper in application code creates a competing owner for consistency and recovery.

## Typed Data Is Not Runtime Ownership

Maps may appear inside typed immutable data when the map itself is genuinely part of the value. Snapshot mutable inputs with `Map.copyOf(...)` or another appropriate immutable representation.

Known fields should become named fields instead of `Map<String,Object>`.

##### Why

Typed immutable data describes a value at a point in time. It does not own changing keyed state across time.

## Method-Local Exception

A method-local mutable collection is allowed for a bounded algorithmic transformation only when it:

- never escapes the method;
- is not stored on an object;
- does not represent registry/cache/durable/distributed/session/authorization/lifecycle state;
- uses meaningful key/value types;
- would not gain domain clarity from a named value type.

##### Why

Local grouping/counting/sorting has no independent lifecycle to architect. This exception prevents ceremony without reopening the long-lived state loophole.

## Infrastructure Exception

Canonical infrastructure may own mutable maps as implementation details, including:

- Tavall Registry implementations and indexes;
- Tavall Cache internals;
- Tavall Database persistence internals;
- Redis/distributed-state adapters;
- dedicated operation/runtime owners;
- dynamic serialization/integration adapters where the external schema is actually dynamic.

Consumers do not depend on or mutate those backing maps directly.

## API Rule

Do not expose generic map mutation as a domain API.

Rejected:

```java
registry.getEntries().put(id, value);
cache.getMap().remove(id);
state.compute(id, mutation);
```

Prefer focused behavior such as `start`, `save`, `find`, `invalidate`, `applyMutation`, and immutable snapshots.

##### Why

Map methods expose storage mechanics. Domain methods can preserve validation, duplicate policy, lifecycle transitions, audit, persistence effects, and cleanup behind the owner that understands them.

## `*Repository` Does Not Fix Map Ownership

New Tavall-owned production types ending in `Repository` are prohibited by the primary architecture rule.

Existing repository types are migration debt only. A map migration must not create or expand that debt. Durable map-shaped state goes to Tavall Database; runtime map-shaped state goes to Registry/Cache/operation ownership according to semantics.

## Review Rule

Any new mutable map/set field or parallel keyed collection in production application code requires architecture review and should be rejected unless clearly inside an allowed infrastructure/data boundary.

Strong violation signals include raw/nested arbitrary maps, mutable keyed fields in ordinary consumers, backing-map exposure, and attempts to move the state into a newly named `*Repository`.

##### Why

Mutable keyed state is cheap to add and expensive to unwind after callers depend on its shape. Ownership review at introduction is far cheaper than later discovering one convenient map became a cache, registry, persistence layer, and API at the same time.
