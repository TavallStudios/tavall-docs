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

## Production Reference System

The rule is already visible across production code. No single subsystem currently demonstrates every target convention perfectly, so this chapter deliberately uses several real classes whose responsibilities line up into the intended ownership model.

| Responsibility | Production source | What it demonstrates |
| --- | --- | --- |
| Ordinary DI consumer | [`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) | Consumer resolves a registry, data handler, and resolver through `DependencyAccess` and calls domain methods instead of owning keyed state. |
| Runtime registry | [`AchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/AchievementListRegistry.java) | Achievement definitions live behind `AbstractRegistry<AchievementKey, AchievementListData>` and domain methods such as `find`, `save`, and `snapshot`. |
| Cache | [`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java) | Player achievement state is owned by `AbstractCache<UUID, PlayerAchievementData>` with TTL, load, retain, remove, and cleanup behavior. |
| Data/persistence boundary | [`PlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) | Load/save workflow coordinates the cache and persistence access rather than exposing either backing store to consumers. |
| Typed short-lived/session data | [`FFAActivePlayerSessionData`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionData.java) | Session values are modeled as named typed fields instead of a primitive-keyed metadata map. |
| Multiple secondary indexes | [`BattleInstanceRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java) | Secondary maps exist inside an `AbstractIndexedRegistry`, where the registry owns validation, index/unindex behavior, and domain lookup methods. |
| Registry infrastructure | [`AbstractRegistry`](https://github.com/TavallStudios/tavall-registry/blob/main/src/main/java/org/tavall/registry/AbstractRegistry.java) | Tavall Registry is itself the map-backed infrastructure boundary. |
| Cache infrastructure | [`AbstractCache`](https://github.com/TavallStudios/tavall-cache/blob/main/abstract-cache-system/src/main/java/org/tavall/abstractcache/cache/AbstractCache.java) | Tavall Cache owns its internal concurrent map and adds cache semantics around it. |

These sources are architectural evidence, not permission to copy compatibility-era details that conflict with newer Tavall DI guidance. When a production class contains older dependency-map construction or another migration artifact, use the current binding architecture rule for that concern and the production source only for the responsibility being demonstrated here.

## Production Example: Consumer Calls Boundaries Instead of Owning Maps

[`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) is a real consumer that declares the dependencies it needs and asks those dependencies for behavior:

```java
@DelegatesTo
public final class AchievementPointSummaryHandler
        implements DependencyAccess<
                IAchievementListRegistry,
                IPlayerAchievementDataHandler,
                AchievementPointTitleResolver
        > {

    private IAchievementListRegistry getDefinitionRegistry() {
        return getInstance().achievementListRegistry();
    }

    private IPlayerAchievementDataHandler getDataHandler() {
        return getInstance().playerAchievementDataHandler();
    }

    public AchievementPointSummary summarize(
            UUID playerId,
            AchievementPointType pointType
    ) {
        PlayerAchievementData data = getDataHandler().load(playerId);

        for (AchievementListData definition : getDefinitionRegistry().snapshot()) {
            // domain calculation
        }

        // return typed summary
    }
}
```

The handler does not create a `Map<AchievementKey, AchievementListData>` or `Map<UUID, PlayerAchievementData>`. Definition ownership belongs to the registry. Player-data load/cache/persistence policy belongs to the data handler and cache.

The current production class still carries compatibility-era dependency-map construction. That detail is not the pattern being endorsed here; the relevant production behavior is that the consumer declares Tavall dependencies and calls their domain surfaces instead of recreating their storage.

## Production Example: Registry Owns Runtime Keyed State

[`AchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/AchievementListRegistry.java) owns the achievement-definition key space:

```java
@DelegatesTo(IAchievementListRegistry.class)
public final class AchievementListRegistry
        extends AbstractRegistry<AchievementKey, AchievementListData>
        implements IAchievementListRegistry, IDependencyAccess {

    @Override
    public Optional<AchievementListData> find(AchievementKey achievementKey) {
        if (achievementKey == null) {
            return Optional.empty();
        }
        return Optional.ofNullable(getRegistryData(achievementKey));
    }

    @Override
    public AchievementListData save(AchievementListData achievementListData) {
        if (achievementListData == null) {
            return null;
        }
        cacheAchievementDefinition(achievementListData);
        persistAchievementDefinition(achievementListData);
        return achievementListData;
    }

    @Override
    public List<AchievementListData> snapshot() {
        ArrayList<AchievementListData> achievements = new ArrayList<>(values());
        // stable domain ordering
        return List.copyOf(achievements);
    }
}
```

The important ownership decision is `AchievementKey -> AchievementListData` lives in a registry. Consumers ask `find(...)`, `save(...)`, or `snapshot()` rather than owning or receiving a mutable backing map.

## Production Example: Cache Owns Expiring State

[`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java) shows cache-shaped state routed through Tavall Cache:

```java
@DelegatesTo(IPlayerAchievementCache.class)
public final class PlayerAchievementCache
        extends AbstractCache<UUID, PlayerAchievementData>
        implements IPlayerAchievementCache {

    @Override
    public Optional<PlayerAchievementData> find(UUID playerId) {
        return Optional.ofNullable(
                getIfPresent(playerId, DOMAIN, TYPE, VERSION, SOURCE)
        );
    }

    @Override
    public PlayerAchievementData getOrLoad(
            UUID playerId,
            Function<UUID, PlayerAchievementData> loader
    ) {
        ICacheKey<UUID> key = cacheKey(playerId);
        return get(key, ignored -> loader.apply(playerId), onlineTtlMillis);
    }

    @Override
    public PlayerAchievementData retainAfterQuit(PlayerAchievementData data) {
        return putWithTtl(data, postQuitTtlMillis);
    }
}
```

A handler-level `ConcurrentHashMap<UUID, PlayerAchievementData>` would duplicate the ownership already provided here while losing TTL, cache-key metadata, cleanup, and lifecycle semantics.

## Production Example: Data Handler Hides Cache and Persistence Coordination

[`PlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) demonstrates why consumers should usually call a data boundary instead of coordinating a repository and cache themselves:

```java
@Override
public PlayerAchievementData load(UUID playerId) {
    if (playerId == null) {
        return null;
    }
    return cache.getOrLoad(playerId, id -> dataBuilder.buildPlayerAchievementData(
            id,
            achievementAccess.findPlayerAchievementProgress(id),
            Instant.now()
    ));
}

@Override
public Optional<PlayerAchievementData> findCached(UUID playerId) {
    return cache.find(playerId);
}
```

The current class still uses constructor-captured managed dependencies, which is compatibility-era composition and not the target DI style. Its **data-boundary responsibility** is the useful production example: callers do not need to know how cache misses, persistence reads, save batching, or post-quit retention are implemented.

## Production Example: Primitive Identity Does Not Require a Map

[`FFAActivePlayerSessionData`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionData.java) is the simple-data case:

```java
public record FFAActivePlayerSessionData(
        String worldName,
        UUID activeRoundUUID,
        UUID activeEngagementUUID,
        Instant joinedAt,
        Instant lastStateChangeAt
) {
}
```

Those values could have been hidden inside `Map<String, Object>` or split across several `Map<UUID, ...>` structures. They are instead one named domain value. Primitive/platform types such as `UUID`, `String`, `long`, and enums are perfectly valid fields and keys; they do not justify an untyped value model.

## Production Example: Secondary Maps Belong Inside the Registry Owner

[`BattleInstanceRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java) is the important exception that proves the ownership rule:

```java
@DelegatesTo(IBattleInstanceRegistry.class)
public final class BattleInstanceRegistry
        extends AbstractIndexedRegistry<UUID, BattleInstance>
        implements IBattleInstanceRegistry {

    private final Map<UUID, UUID> battleIdByPlayerId =
            new ConcurrentHashMap<>();
    private final Map<UUID, BattleParticipant> participantByPlayerId =
            new ConcurrentHashMap<>();

    @Override
    public Optional<BattleInstance> findBattleByPlayer(UUID playerId) {
        return Optional.ofNullable(battleIdByPlayerId.get(playerId))
                .flatMap(this::findBattle);
    }

    @Override
    protected void index(UUID battleId, BattleInstance battleInstance) {
        battleInstance.participants().forEach((playerId, participant) -> {
            battleIdByPlayerId.put(playerId, battleId);
            participantByPlayerId.put(playerId, participant);
        });
    }

    @Override
    protected void unindex(UUID battleId, BattleInstance battleInstance) {
        battleInstance.participants().forEach((playerId, participant) -> {
            battleIdByPlayerId.remove(playerId, battleId);
            participantByPlayerId.remove(playerId, participant);
        });
    }
}
```

Those mutable maps are allowed **because they are implementation indexes owned by the registry responsible for keeping them coherent**. Moving either map into a battle handler, listener, command, or service would violate the rule.

This is the difference between a map being an implementation detail and a map becoming application architecture.

## Rejected Consumer Pattern

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

This is a registry implemented locally inside a consumer. Thread safety does not change the ownership problem.

Prefer a typed registry boundary with domain methods:

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

Production examples include immutable map-bearing result/data types such as [`RoundPerformanceGradeResult`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/rating/grading/RoundPerformanceGradeResult.java), which snapshots its component map with `Map.copyOf(...)`.

Canonical shape:

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

- [`tavall-registry` `AbstractRegistry`](https://github.com/TavallStudios/tavall-registry/blob/main/src/main/java/org/tavall/registry/AbstractRegistry.java) provides typed registry ownership over keyed runtime state.
- [`tavall-cache` `AbstractCache`](https://github.com/TavallStudios/tavall-cache/blob/main/abstract-cache-system/src/main/java/org/tavall/abstractcache/cache/AbstractCache.java) provides typed cache ownership, TTL, invalidation, snapshots, and cache lifecycle behavior.

Application code should consume those boundaries rather than recreate their internal map mechanics.

The current `tavall-registry` implementation still inherits directly from `ConcurrentHashMap`, which exposes raw map operations on concrete registries. That is an infrastructure encapsulation concern, not permission for application consumers to use raw map APIs. Domain-specific registry methods remain the preferred application surface.

## Review Rule

Any new mutable map/set field or parallel keyed collection in production application code requires architecture review and should be rejected unless it is clearly inside an allowed infrastructure/data boundary.

`Map<String, Object>`, raw `Map`, nested arbitrary maps, and map-shaped behavior APIs are especially strong violation signals.
