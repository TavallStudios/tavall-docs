# Application-Owned Mutable Maps

> **Status:** Active  
> **Authority:** Binding supporting chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production application code, reviews, generation, automation, and AI-assisted development

Application-owned mutable maps are prohibited by default.

The rule is about **ownership**, not whether Java's `Map` type is inherently bad. Canonical Tavall infrastructure may intentionally model a system as a Java collection. In those cases the collection contract is part of the tool's accepted design unless the owning tool explicitly changes it.

Current examples include:

- `tavall-registry` `AbstractRegistry<K, V>`, which intentionally extends `ConcurrentHashMap<K, V>` while adding `IAbstractRegistry` registry-named access;
- `tavall-di` `DependencyMap`, which intentionally remains a `ConcurrentHashMap<Class<?>, IDependencyMetaData<?, ?>>` and keeps inherited mutation available for advanced/framework use.

Shared application architecture must not reinterpret those intentional tool contracts as generic “backing-map exposure” defects.

## Classification Rule

Before introducing mutable keyed state, classify the semantics:

- runtime identity/definitions/sessions/providers/strategies -> Tavall Registry;
- expiring/reloadable/stale-able/disposable fast state -> Tavall Cache;
- durable state that must survive restart -> Tavall Database entity classes and the entity persistence contract defined by the checked-in `tavall-database` version;
- distributed/shared runtime state -> owning Redis/distributed abstraction;
- several lookup dimensions over one runtime identity -> one Registry owner using the current `tavall-registry` contract, with any additional lookup structures owned coherently by that registry;
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

Prefer a focused Registry owner.

##### Why

The consumer should own behavior, not silently become the lifecycle/storage primitive for that behavior.

## Canonical Tool Collection Contracts

Do not apply the application-owned-map prohibition mechanically inside a canonical Tavall tool or a type extending that tool's intended collection abstraction.

For example, `AbstractRegistry` is itself a concurrent map-backed registry. Registry implementations may use inherited `Map` / `ConcurrentMap` operations when those operations are part of the accepted registry implementation contract. The Tavall-named methods on `IAbstractRegistry`, including `createRegistry`, `getRegistryData`, `getRegistryKeyByData`, and the key/data `AsSet` / `AsList` / `AsCollection` accessors, provide a clearer registry vocabulary for common access without erasing the underlying collection behavior.

Likewise, `DependencyMap` intentionally preserves inherited map mutation for advanced/framework use while named Tavall DI APIs own coherent registration/replacement semantics.

When reviewing one of these tools, distinguish:

1. **ordinary application consumer ownership**, which should not invent its own raw keyed store;
2. **tool-facing semantic APIs**, which are normally preferred when they describe the operation cleanly;
3. **tool implementation / framework use**, where the canonical library may intentionally expose and use Java collection operations.

##### Why

A blanket “composition over inheritance” or “never use backing-map APIs” rule would contradict existing Tavall tools that deliberately use Java collection inheritance for interoperability and low abstraction overhead. The correct boundary is ownership and invariant preservation, not aesthetic dislike of `Map`.

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

Canonical infrastructure may own mutable maps as implementation details or intentional public/framework contracts, including:

- Tavall Registry implementations and registry-owned lookup structures;
- Tavall DI dependency maps;
- Tavall Cache internals;
- Tavall Database persistence internals;
- Redis/distributed-state adapters;
- dedicated operation/runtime owners;
- dynamic serialization/integration adapters where the external schema is actually dynamic.

Whether a collection surface is internal, semantic, or intentionally inherited is decided by the canonical owning tool. Shared docs must not guess.

## API Rule

Ordinary application consumers should use the semantic API exposed by the owning Tavall tool when one exists and fits the operation.

Rejected consumer ownership:

```java
public final class SessionService {
    private final Map<UUID, Session> sessions = new ConcurrentHashMap<>();
}
```

Preferred ownership:

```java
public final class SessionRegistry
        extends AbstractRegistry<UUID, Session> {
}
```

Inside the registry itself, inherited operations such as `compute`, `putIfAbsent`, iteration, or other supported `ConcurrentMap` behavior are not automatically violations. They are valid when they preserve the registry's actual invariants and the canonical tool contract.

If a specialized registry adds additional invariants or lookup structures, every supported mutation path must preserve those invariants. The fix for a missed mutation path is to repair the invariant or explicitly narrow the owning tool contract, not to assume the base inheritance was accidental.

##### Why

Semantic APIs communicate intent to ordinary consumers, while canonical infrastructure still needs implementation power and Java interoperability. Conflating those layers produces needless wrappers and can make shared docs contradict the libraries they are supposed to govern.

## `*Repository` Does Not Fix Map Ownership

New Tavall-owned production types ending in `Repository` are prohibited by the primary architecture rule.

Existing repository types are migration debt only. A map migration must not create or expand that debt. Durable map-shaped state goes to Tavall Database; runtime map-shaped state goes to Registry/Cache/operation ownership according to semantics.

## Review Rule

Any new mutable map/set field or parallel keyed collection in ordinary production application code requires architecture review and should be rejected unless clearly inside an allowed infrastructure/data boundary.

Strong violation signals include raw/nested arbitrary maps, mutable keyed fields in ordinary consumers, and attempts to move the state into a newly named `*Repository`.

Do **not** flag an inherited or internally used collection API merely because it is a `Map`. First identify whether the owning canonical Tavall tool intentionally exposes that behavior and which invariants it requires.

##### Why

Mutable keyed state is cheap to add and expensive to unwind after callers depend on its shape. Ownership review at introduction is far cheaper than later discovering one convenient map became a cache, registry, persistence layer, and API at the same time. The same review must also avoid “fixing” deliberate infrastructure contracts into unnecessary abstraction layers.
