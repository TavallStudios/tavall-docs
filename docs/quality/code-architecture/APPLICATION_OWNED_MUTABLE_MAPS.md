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

The registry case already exists in production. [`AchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/AchievementListRegistry.java) owns `AchievementKey -> AchievementListData` through `AbstractRegistry` and exposes domain methods rather than requiring consumers to own the key space themselves:

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
}
```

The source still contains compatibility-era dependency-map construction. That is not the behavior being endorsed here; the relevant production pattern is that keyed runtime ownership belongs to a registry and consumers call its domain surface.

## Rejected Consumer Pattern

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

This is a registry implemented locally inside a consumer. Thread safety does not change the ownership problem.

Production already uses this ownership shape in [`FFAActivePlayerSessionRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionRegistry.java):

```java
public final class FFAActivePlayerSessionRegistry
        extends AbstractRegistry<UUID, FFAActivePlayerSession> {

    public FFAActivePlayerSession save(FFAActivePlayerSession session) {
        put(session.playerUUID(), session);
        return session;
    }

    public Optional<FFAActivePlayerSession> find(UUID playerUUID) {
        return Optional.ofNullable(getRegistryData(playerUUID));
    }

    public Optional<FFAActivePlayerSession> remove(UUID playerUUID) {
        return Optional.ofNullable(super.remove(playerUUID));
    }
}
```

The registry owns collection semantics, duplicate policy, snapshots, replacement, indexing, and lifecycle. Consumers receive the registry through the appropriate Tavall DI surface and call domain methods rather than creating another mutable map.

## Cache-Shaped State

```java
private final Map<UUID, CooldownData> cooldowns =
        new ConcurrentHashMap<>();
```

is cache-shaped state. If entries expire, become stale, reload, or are disposable, use Tavall Cache rather than hand-rolling lifecycle and invalidation behavior.

[`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java) shows the production shape:

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

A consumer-level `ConcurrentHashMap<UUID, PlayerAchievementData>` would reproduce ownership already provided by Tavall Cache while losing TTL, cache-key metadata, cleanup, and cache lifecycle semantics.

## Data and Persistence Ownership

Consumers should not coordinate a cache and durable store merely because both happen to be keyed. The data handler or persistence boundary owns that workflow.

[`PlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) already hides cache-miss and persistence behavior behind `load(...)`:

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

The class currently contains constructor-captured managed dependencies, which is compatibility-era composition and not the target DI style. Its data-boundary responsibility is the production pattern: callers should not need to know how cache misses, persistence reads, save batching, or post-quit retention are implemented.

## Data Is Not Runtime Ownership

Maps remain valid inside typed immutable or encapsulated data when the map itself is genuinely part of the value. Known fields should still become named fields instead of `Map<String, Object>`.

[`FFAActivePlayerSessionData`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionData.java) demonstrates the simple case where primitive and platform values become one named domain type rather than several maps:

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

A map can still be legitimate data when the map itself is part of the value. [`RoundPerformanceGradeResult`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/rating/grading/RoundPerformanceGradeResult.java) snapshots its component map rather than exposing mutable runtime ownership:

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

This is data, not a mutable runtime store.

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

Secondary indexes are a concrete example. [`BattleInstanceRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/minecraft/server/battle/BattleInstanceRegistry.java) owns two mutable maps inside `AbstractIndexedRegistry` and keeps them coherent through `index(...)` and `unindex(...)`:

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

Those maps are allowed because they are implementation indexes owned by the registry responsible for their invariants. Moving either map into a battle handler, listener, command, or service would violate the rule.

## API Rule

Do not expose map operations as the domain API.

Rejected:

```java
registry.getEntries().put(playerId, session);
cache.getMap().remove(playerId);
state.compute(playerId, mutation);
```

Prefer focused methods such as `start(...)`, `find(...)`, `invalidate(...)`, `applyMutation(...)`, and typed snapshots.

[`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) shows the consumer side of this rule. It asks the data handler for player data and the registry for a snapshot rather than owning either map:

```java
PlayerAchievementData data = getDataHandler().load(playerId);

for (AchievementListData definition : getDefinitionRegistry().snapshot()) {
    if (!definition.enabled() || definition.pointType() != pointType) {
        continue;
    }
    // calculate typed summary values
}
```

The current production class still carries compatibility-era dependency-map construction. The relevant pattern is the domain interaction: the consumer asks owners for behavior instead of manipulating their collections.

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
