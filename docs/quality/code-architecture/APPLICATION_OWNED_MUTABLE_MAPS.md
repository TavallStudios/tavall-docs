# Application-Owned Mutable Maps

> **Status:** Active  
> **Authority:** Binding supporting chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All production application code, reviews, generation, and AI-assisted development

Application-owned mutable maps are prohibited by default.

The rule is about **ownership**, not whether Java's `Map` type is inherently bad. Tavall Registry, Tavall Cache, repositories, persistence adapters, distributed-state adapters, and other canonical infrastructure may use maps internally. Ordinary application consumers should not recreate those systems with `HashMap`, `ConcurrentHashMap`, `ConcurrentMap`, mutable `Set`, or parallel keyed collections.

A mutable keyed collection in a handler, service, orchestrator, router, listener, command, controller, gateway, adapter, or similar consumer is a violation candidate by default.

## Classification Rule

Before introducing mutable keyed state, classify what the state actually is:

- **Runtime identity, definitions, sessions, active objects, providers, strategies, or keyed process state** → Tavall Registry.
- **Expiring, reloadable, stale-able, disposable, or fast-access state** → Tavall Cache.
- **Durable state** → Repository plus the owning data handler or persistence workflow.
- **Distributed/shared state** → the owning Redis or distributed-state abstraction.
- **Several indexes over one identity** → `AbstractIndexedRegistry` or one typed aggregate.
- **Short-lived operation payload/state/result** → typed `*Data`, `*Request`, `*Result`, `*State`, or `*MetaData`.

If a collection represents something engineers can name, model the named thing instead of adding a mutable map.

## Rejected Consumer Pattern

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

This is a registry implemented locally inside a consumer. Thread safety does not change the ownership problem.

Prefer:

```java
public interface IPlayerSessionRegistry {
    Optional<PlayerSessionData> find(UUID playerId);

    PlayerSessionData start(UUID playerId);

    void end(UUID playerId);
}
```

The registry owns the collection and its duplicate, replacement, lifecycle, snapshot, and cleanup semantics. Consumers receive the registry through Tavall DI and call domain methods.

## Cache-Shaped State

```java
private final Map<UUID, CooldownData> cooldowns =
        new ConcurrentHashMap<>();
```

is cache-shaped state. If entries expire, become stale, reload, or are disposable, use Tavall Cache rather than hand-rolling lifecycle and invalidation behavior.

## Data Is Not Runtime Ownership

Maps remain valid inside typed immutable or encapsulated data when the map itself is genuinely part of the value.

```java
public record PlaceholderData(
        Map<PlaceholderKey, String> values
) {
    public PlaceholderData {
        values = Map.copyOf(values);
    }
}
```

This is data, not a mutable runtime store.

Known fields should still become named fields instead of `Map<String, Object>`.

## Method-Local Exception

A method-local mutable map is allowed only for a bounded algorithmic transformation when all of the following are true:

- it never escapes the method;
- it is not stored on an object;
- it does not represent registry, cache, durable, distributed, lifecycle, authorization, or session state;
- its key and value types are concrete and meaningful;
- replacing it with a named type would not improve the domain contract.

This exception is intentionally narrow.

## Infrastructure Exception

Canonical infrastructure may own mutable maps as implementation details. Examples include:

- Tavall Registry implementations;
- Tavall Cache implementations;
- repository and persistence adapters;
- Redis/distributed-state adapters;
- indexes inside dedicated registry/cache/storage implementations;
- serialization/integration adapters where the external schema itself is dynamic.

Consumers should not depend on or mutate those backing maps directly.

## API Rule

Do not expose map operations as the domain API.

Rejected:

```java
registry.getEntries().put(playerId, session);
cache.getMap().remove(playerId);
state.compute(playerId, mutation);
```

Preferred:

```java
sessionRegistry.start(playerId);
playerCache.invalidate(playerId);
playerStateHandler.applyMutation(request);
```

Lookup, registration, replacement, mutation, invalidation, expiry, persistence, snapshotting, and cleanup belong behind focused methods on DI-managed boundaries.

## Tavall Registry and Tavall Cache

This rule matches the purpose of the shared infrastructure:

- `tavall-registry` provides typed registry ownership over keyed runtime state.
- `tavall-cache` provides typed cache ownership, TTL, invalidation, snapshots, and cache lifecycle behavior.

Application code should consume those boundaries rather than recreate their internal map mechanics.

The current `tavall-registry` implementation still inherits directly from `ConcurrentHashMap`, which exposes raw map operations on concrete registries. That is an infrastructure encapsulation concern, not permission for application consumers to use raw map APIs. Domain-specific registry methods remain the preferred application surface.

## Review Rule

Any new mutable map/set field or parallel keyed collection in production application code requires architecture review and should be rejected unless it is clearly inside an allowed infrastructure/data boundary.

`Map<String, Object>`, raw `Map`, nested arbitrary maps, and map-shaped behavior APIs are especially strong violation signals.
