# Project Novus Dependency Injection and Orchestration

> **Status:** Active  
> **Authority:** Supporting chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Module scopes, runtime composition, lifecycle cleanup, and orchestration

The binding Project Novus dependency access patterns live directly in [`CODE_ARCHITECTURE.md`](../CODE_ARCHITECTURE.md#dependency-injection-patterns). This chapter owns only the runtime-scope and composition details that would make the primary architecture document needlessly swollen.

Java examples are either shortened excerpts from linked production code or are explicitly labeled canonical adaptations derived from production. If an excerpt stops matching production, update the document rather than preserving architectural fan fiction for sentimental reasons.

## Module Registration Pattern

Register interface and concrete aliases against the same metadata-owned instance.

Source: [`ScopedNovusModuleContext`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

```java
IDependencyMetaData<?, ?> existingMetaData = findMetadataForInstance(dependencyInstance);
if (existingMetaData == null) {
    dependencyMap.registerInstance(dependencyType, dependencyInstance);
} else {
    dependencyMap.registerDependency(dependencyType, existingMetaData);
}
```

This permits:

```java
registerDependency(IPlayerAchievementDataHandler.class, dataHandler);
registerDependency(PlayerAchievementDataHandler.class, dataHandler);
```

Both tokens resolve to one metadata object and one instance.

The named loader registration remains only as a migration bridge for existing module code. New module behavior resolves from `dependencyMap()`.

## Module Lookup Pattern

A module resolves generation-owned dependencies first and stable application dependencies second.

Source: [`ScopedNovusModuleContext`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

```java
T moduleDependency = dependencyMap.findInstance(dependencyType);
if (moduleDependency != null) {
    return moduleDependency;
}
return DependencyLoaderAccess.findInstance(dependencyType);
```

The fallback is for stable application dependencies only. A child-generation object must never be placed in the global loader.

## Generated Access Composition Pattern

Register dependencies before the generated access type, then register the consumer.

Source: [`AchievementRuntimeBuilder`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/runtime/AchievementRuntimeBuilder.java)

```java
register(context, IPlayerAchievementDataHandler.class, dataHandler);
register(context, IPlayerAchievementCache.class, cache);
register(context, AchievementEventMutationAccess.class, eventMutationAccess);
register(context, AchievementCompletionHandler.class, completionHandler);

AchievementProgressMutationHandlerDependencyAccess mutationDependencies =
        new AchievementProgressMutationHandlerDependencyAccess(context.dependencyMap());
register(
        context,
        AchievementProgressMutationHandlerDependencyAccess.class,
        mutationDependencies
);

AchievementProgressMutationHandler mutationHandler =
        new AchievementProgressMutationHandler(context.dependencyMap());
register(context, IAchievementProgressMutationHandler.class, mutationHandler);
register(context, AchievementProgressMutationHandler.class, mutationHandler);
```

The generated access object is stable. Its getters resolve the current metadata-owned dependency each time.

## DI Anti-Patterns

### Dependency Constructor Injection

Tavall-managed application dependencies must not be passed through constructors of ordinary production behavior classes. Constructor injection creates a parallel dependency-access style that bypasses the generated `DependencyAccess` surface and moves graph ownership into whichever caller happens to construct the class.

Anti-pattern:

```java
public final class PlayerRewardHandler {
    private final IPlayerData playerData;
    private final IEconomyService economyService;

    public PlayerRewardHandler(
            IPlayerData playerData,
            IEconomyService economyService
    ) {
        this.playerData = playerData;
        this.economyService = economyService;
    }
}
```

Preferred Tavall DI shape:

```java
@DelegatesTo(IPlayerRewardHandler.class)
public final class PlayerRewardHandler
        implements IPlayerRewardHandler,
        DependencyAccess<IPlayerData, IEconomyService> {

    @Override
    public void handlePlayerReward(long amount) {
        var dependencies = getInstance();
        dependencies.iPlayerData().addCoins(amount);
        dependencies.iEconomyService().recordTransaction(amount);
    }
}
```

The exact generated getter names and access contract come from the checked-in `tavall-di` version. The architectural rule is that Tavall-managed dependencies resolve through the owning dependency map rather than being captured by behavior-class constructors.

Why constructor injection is rejected for managed dependencies:

- replacement and reload semantics stay owned by the map and metadata;
- module generations do not accidentally retain constructor-captured objects;
- tests exercise the same dependency graph mechanics as production;
- callers do not become ad hoc composition roots;
- dependency access remains consistent across the codebase.

### Static Dependency Access

Do not use static methods as an alternate dependency-access channel.

A static method that resolves a Tavall-managed service from `DependencyLoaderAccess`, an `IDependencyMap`, or another container is a service locator with friendlier punctuation. It hides the dependency from the behavior type, bypasses the owning generated access surface, and can retain the wrong assumptions about replacement or module-generation ownership.

Use focused default instance methods when they make dependency-backed behavior easier to read. The implementing object still participates in the DI contract, and the default method continues to resolve through its dependency-access interface rather than a global static accessor.

Source: [Minecraft-CTF `MessageAccess`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/config/message/interfaces/MessageAccess.java)

```java
public interface MessageAccess extends MessageConfigDependencyAccess {

    default MessageHandler getMessageService() {
        MessageConfigHandler handler = getMessageConfigHandler();
        return handler;
    }

    private static Component missingMessageServiceText(String key) {
        return Component.text("Missing message service: " + key);
    }
}
```

The default method exposes DI-managed behavior. The private static helper is acceptable because it only constructs a fallback value from its explicit input and owns no runtime dependency.

Static methods remain acceptable only when they do not own or locate runtime dependencies. Typical valid cases are immutable constants, pure value parsing or normalization, private pure helpers, and static builder/factory entry points that merely construct a value or builder. If the call performs I/O, touches runtime state, schedules work, resolves a service, or needs lifecycle/replacement semantics, it belongs behind DI.

## Non-DI Constructor Inputs

Constructors remain valid for values that are not Tavall-managed application dependencies, such as immutable object state, builder inputs, configuration, and genuinely externally owned platform handles.

Source: [`AchievementCompletionHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementCompletionHandler.java)

```java
public final class AchievementCompletionHandler {
    private final JavaPlugin plugin;

    public AchievementCompletionHandler(JavaPlugin plugin) {
        this.plugin = Objects.requireNonNull(plugin, "plugin");
    }
}
```

Do not move a Paper, Velocity, Spring, or other externally owned object into generated DI access merely to make declarations look uniform. This exception does not permit constructor injection of Tavall-managed handlers, services, repositories, registries, caches, gateways, or other application dependencies.

## Default Consumer Pattern

A **consumer** is an ordinary production class that uses Tavall-managed capabilities to perform one focused operation. Handlers, services, orchestrators, listeners, command handlers, controllers, and adapters are consumers when they call domain boundaries owned elsewhere.

The default consumer should be deliberately boring:

- one coherent behavior;
- one typed request or explicit method input family;
- one typed result when the operation has meaningful outcomes;
- Tavall-managed collaborators declared through `DependencyAccess<...>`;
- `getInstance()` captured once when several collaborators are used;
- no constructor-captured Tavall dependencies;
- no static dependency lookup;
- no mutable map/set fields for domain state;
- no raw registry/cache/repository maps exposed to the consumer;
- no hidden persistence, cache, or registry ownership.

The consumer calls domain methods. The owning dependency decides how its state is represented internally.

### Pattern Responsibilities

| Pattern | Consumer rule |
| --- | --- |
| `*Data` / `*State` | Pass or return typed values. Do not replace them with generic maps. |
| `*Request` | Carry operation input across a meaningful boundary. Validate before mutation. |
| `*Result` | Represent expected success/rejection outcomes explicitly. |
| `*DataHandler` | Consume through DI for domain data load/save/update policy. The consumer does not reproduce repository/cache coordination. |
| `*MetaData` | Use a typed value for known metadata. Extensible maps remain encapsulated at real integration edges only. |
| `*MetaDataHandler` | Use through DI only when metadata needs derivation, normalization, validation, enrichment, or cross-source resolution. Passive metadata needs only a value type. |
| `*Registry` | Consume through DI and call domain lookup/registration methods. Do not call or expose backing-map methods. |
| `*Cache` | Consume through DI only when the consumer genuinely owns cache-facing behavior. Prefer a data handler/service to encapsulate cache policy when cache mechanics are not the consumer's job. |
| `*Repository` | Usually sits behind a data handler or persistence service. Direct repository consumption is reserved for a consumer that truly owns persistence workflow. |
| `*Router` | Delegate a typed request to the selected handler. The router does not become the implementation. |
| `*Builder` | Construct a typed value. Builders do not resolve dependencies or become service locators. |
| `*Handler` / `*Service` | Invoke focused behavior through DI. Do not reach into another component's collections to perform that behavior manually. |

### Production Reference Chain

The default consumer pattern is not hypothetical. Its pieces already exist in production and can be followed directly:

- [`AchievementProgressMutationHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementProgressMutationHandler.java) — four-dependency consumer using `DependencyAccess`.
- [`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) — consumer of a registry, data handler, and resolver.
- [`AchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/AchievementListRegistry.java) and [`IAchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/IAchievementListRegistry.java) — typed runtime registry surface.
- [`PlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) and [`IPlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/interfaces/IPlayerAchievementDataHandler.java) — data boundary over cache/persistence workflow.
- [`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java) — Tavall Cache-backed player data.
- [`AchievementRuntimeBuilder`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/runtime/AchievementRuntimeBuilder.java) — composition/registration of the achievement runtime.

Production is still carrying compatibility-era dependency-map constructors in some of these classes. Those constructors are migration artifacts, not a second approved dependency style. The useful production evidence is the ownership boundary and `DependencyAccess` behavior; the binding rule above remains authoritative where old composition code differs.

### Exact Production Consumer Example

[`AchievementProgressMutationHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementProgressMutationHandler.java) is already extremely close to the default consumer shape:

```java
@DelegatesTo(IAchievementProgressMutationHandler.class)
public final class AchievementProgressMutationHandler
        implements IAchievementProgressMutationHandler,
        DependencyAccess<
                IPlayerAchievementDataHandler,
                IPlayerAchievementCache,
                AchievementEventMutationAccess,
                AchievementCompletionHandler
        > {

    private IPlayerAchievementDataHandler getDataHandler() {
        return getInstance().playerAchievementDataHandler();
    }

    private IPlayerAchievementCache getCache() {
        return getInstance().playerAchievementCache();
    }

    private AchievementEventMutationAccess getEventMutationAccess() {
        return getInstance().achievementEventMutationAccess();
    }

    private AchievementCompletionHandler getCompletionHandler() {
        return getInstance().achievementCompletionHandler();
    }

    @Override
    public AchievementProgressMutationResult applyProgress(
            String eventId,
            UUID playerId,
            AchievementListData definition,
            long amount,
            String actionType,
            String sourceServerId,
            String sourceContext,
            Instant occurredAt
    ) {
        AchievementProgressEventData eventData =
                new AchievementProgressEventDataBuilder()
                        .eventId(eventId)
                        .playerId(playerId)
                        .triggerType(definition.triggerType())
                        .amount(amount)
                        .actionType(actionType)
                        .sourceServerId(sourceServerId)
                        .sourceContext(sourceContext)
                        .occurredAt(occurredAt)
                        .buildAchievementProgressEventData();

        AchievementProgressMutationResult result =
                getEventMutationAccess().applyEventProgressOnce(
                        eventData,
                        definition
                );

        PlayerAchievementData data = getDataHandler().load(playerId);
        if (data != null) {
            getCache().saveOnline(data);
        }

        if (result != null && result.completedNow()) {
            getCompletionHandler().handleCompletion(
                    result.updatedProgress(),
                    definition
            );
        }
        return result;
    }
}
```

The excerpt is shortened, but the calls and dependency roles are production. The consumer has four declared managed dependencies, constructs typed event data, calls focused boundaries, and does not own a map as a substitute for any of them.

[`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) provides the registry-facing half of the same pattern:

```java
PlayerAchievementData data = getDataHandler().load(playerId);

for (AchievementListData definition : getDefinitionRegistry().snapshot()) {
    if (!definition.enabled() || definition.pointType() != pointType) {
        continue;
    }
    // calculate typed summary values
}
```

The consumer asks the data handler for player data and the registry for a snapshot. It does not own `Map<UUID, PlayerAchievementData>` or `Map<AchievementKey, AchievementListData>`.

### Canonical Target Adaptation

The following remains a **canonical adaptation**, not a verbatim production excerpt. It removes compatibility-era dependency-map construction and shows the stricter target consumer shape. The `IAchievementProgressMetaDataHandler` and typed request shown here define the metadata-handler seam; they are pattern examples, not a claim that those exact classes already exist in production.

```java
@DelegatesTo(IAchievementProgressMutationHandler.class)
public final class AchievementProgressMutationHandler
        implements IAchievementProgressMutationHandler,
        DependencyAccess<
                IAchievementListRegistry,
                IPlayerAchievementDataHandler,
                AchievementEventMutationAccess,
                IAchievementProgressMetaDataHandler
        > {

    @Override
    public AchievementProgressMutationResult applyProgress(
            AchievementProgressMutationRequest request
    ) {
        IDependencyMap dependencies = getInstance();

        AchievementListData definition = dependencies
                .iAchievementListRegistry()
                .find(request.achievementKey())
                .orElse(null);

        if (definition == null
                || !definition.enabled()
                || request.amount() <= 0L) {
            return AchievementProgressMutationResult.rejected();
        }

        PlayerAchievementData playerData = dependencies
                .iPlayerAchievementDataHandler()
                .load(request.playerId());

        if (playerData == null) {
            return AchievementProgressMutationResult.playerNotFound();
        }

        AchievementProgressEventData eventData = dependencies
                .iAchievementProgressMetaDataHandler()
                .resolveEventData(
                        new AchievementProgressMetaDataRequest(
                                request,
                                definition
                        )
                );

        return dependencies
                .achievementEventMutationAccess()
                .applyEventProgressOnce(eventData, definition);
    }
}
```

The important part is not the exact achievement method names. The shape is the contract:

1. The caller supplies typed operation input.
2. The consumer resolves its declared Tavall dependencies through the owning DI map.
3. A registry resolves typed runtime definitions through a domain method.
4. A data handler owns domain data access rather than exposing repository/cache internals.
5. A metadata handler derives a typed metadata/data value when derivation is real behavior.
6. A focused mutation boundary performs the state transition.
7. The consumer returns a typed result.
8. No consumer-owned map is created as a shortcut for any of those systems.

### Data and Metadata Boundary

A primitive key does not justify a generic map value.

Bad:

```java
Map<UUID, Map<String, Object>> playerData;
```

A real production counterexample is [`FFAActivePlayerSessionData`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionData.java):

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

The session has primitive/platform identifiers, but its values are still modeled as one named domain type instead of `Map<UUID, Map<String, Object>>` or several parallel maps.

If metadata must be derived from several sources, the derivation becomes a DI-managed handler. Canonical shape:

```java
public interface IPlayerActionMetaDataHandler {
    PlayerActionMetaData resolve(PlayerActionMetaDataRequest request);
}
```

If it is merely passive values already supplied by the caller, do not create a metadata handler. Use the data type directly.

Known fields remain typed. A `Map<String, Object>` is not a substitute for deciding what the fields are.

### Consumer-Owned Collection Rejection

Ordinary consumers must not own mutable keyed domain state merely because the state is private or short-lived.

Rejected:

```java
public final class MatchHandler {
    private final Map<UUID, MatchState> activeMatches =
            new ConcurrentHashMap<>();
}
```

The production ownership pattern already exists in [`FFAActivePlayerSessionRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionRegistry.java):

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

    public Collection<FFAActivePlayerSession> snapshot() {
        return List.copyOf(values());
    }
}
```

The registry owns collection semantics, duplicate policy, snapshots, replacement, indexing, and lifecycle. A consumer should receive the registry through the appropriate Tavall DI surface and call its domain methods instead of owning another `ConcurrentHashMap`.

The same rule applies to caches, repositories, pending-operation state, and metadata: select the owning pattern first, then consume that pattern through DI rather than embedding a collection in the caller.

See also [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md) for production cache, indexed-registry, data-handler, and infrastructure examples.

### More Than Four Dependencies

The default consumer example intentionally stops at four managed dependencies.

More than four remains a design-review signal. Do not respond by creating one giant `Dependencies` object or by hiding extra dependencies behind maps or static access.

Choose among:

- keep expanded direct access when the behavior is still clearly cohesive;
- introduce a real domain bundle when several collaborators form one reusable lifecycle boundary;
- split independent phases into focused handlers/services;
- move storage/cache coordination behind the data handler or persistence boundary that actually owns it.

The dependency count is a signal to review the behavior, not an invitation to hide the count.

## Module Cleanup Pattern

Close resources in reverse ownership order, then clear the generation map and compatibility scope.

Source: [`ScopedNovusModuleContext`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

```java
while (!resources.isEmpty()) {
    OwnedResource resource = resources.removeLast();
    resource.closeable().close();
}

dependencyMap.clear();
DependencyLoaderAccess.clear(scopeName());
```

Cleanup remains best-effort across all resources. Failures are accumulated and reported after every owned resource receives a close attempt.

## Orchestration Pattern

## Runtime Rules

- Generated access objects and consumers use the same owning map.
- Interface and concrete aliases share metadata.
- Stable application fallback must not return stale module-generation objects.
- Register dependencies before generated access objects and consumers.
- Tavall-managed application dependencies resolve through the owning dependency map rather than behavior-class constructors.
- Immutable state, builder inputs, configuration, and genuinely externally owned platform handles may remain constructor inputs.
- Every resource and dependency has one lifecycle owner.
- Module close clears the generation map and compatibility scope.

## Testing Requirements

Tests verify:

- interface and concrete aliases share metadata and instance identity;
- two module generations use different maps;
- closing one generation does not mutate another generation;
- generated access resolves from the owning module map;
- replacement is visible through an existing generated access instance;
- resources close in reverse order;
- module cleanup clears every owned dependency.

Existing coverage:

- [`ScopedNovusModuleContextTest`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContextTest.java)
- [`NovusModuleReconciliationHandlerTest`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/handler/NovusModuleReconciliationHandlerTest.java)
- [`Tavall DI access styles`](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md)
