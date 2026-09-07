# Project Novus Dependency Injection and Orchestration

> **Status:** Active  
> **Authority:** Supporting chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Module scopes, runtime composition, lifecycle cleanup, and orchestration

The binding Project Novus dependency access patterns live directly in [`CODE_ARCHITECTURE.md`](../CODE_ARCHITECTURE.md#dependency-injection-patterns). This chapter owns only the runtime-scope and composition details that would make the primary architecture document needlessly swollen.

Java examples are either shortened excerpts from linked production code or explicitly labeled canonical examples. If an excerpt stops matching production, update the document rather than preserving architectural fan fiction for sentimental reasons.

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

##### Why

Interface and concrete aliases must describe one owned dependency, not two parallel instances that merely happen to implement the same contract.

Sharing metadata preserves replacement, lifecycle, cleanup, and identity semantics regardless of which token a consumer resolves. Otherwise alias registration can quietly create multiple owners for what the architecture treats as one dependency.

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

##### Why

Module generations need isolation so unload, reload, and replacement affect only the generation that owns the object.

Resolving generation-owned state globally can retain stale objects after reload and turns lifecycle cleanup into a guessing game. Local-first lookup keeps short-lived ownership local while still allowing explicit stable application dependencies as a compatibility fallback.

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

##### Why

Generated access only works as a stable dependency surface when the dependencies it exposes already belong to the same map.

Registering in this order makes replacement visible through existing access objects and prevents consumers from capturing a half-built graph. The dependency map remains the owner; generated access is merely the typed way consumers reach it.

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

##### Why

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

##### Why

A static locator erases dependency ownership from the class declaration and makes any caller able to reach runtime state without participating in its lifecycle.

That weakens replacement, reload safety, test isolation, and architecture review. Pure static helpers remain harmless because their result depends only on explicit input; runtime services do not have that property.

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

##### Why

DI ownership should model objects Tavall can actually replace and lifecycle-manage.

Immutable values and externally owned platform handles have different ownership semantics. Forcing them into Tavall DI would blur the boundary between application dependencies and values/platform objects, making the graph larger without improving replacement or lifecycle behavior.

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
| `*Orchestrator` | Coordinate ordered work and lifecycle across several focused boundaries. Do not absorb the handlers, routers, schedulers, services, storage, or rules being coordinated. |
| `*Router` | Delegate a typed request or transition to the selected handler. The router does not become the implementation. |
| `*Builder` | Construct a typed value. Builders do not resolve dependencies or become service locators. |
| `*Handler` / `*Service` | Invoke focused behavior through DI. Do not reach into another component's collections to perform that behavior manually. |

##### Why

The table separates **behavior consumption** from **behavior ownership**.

Without that distinction, a consumer can slowly become a registry, cache, repository, router, orchestrator, and builder at once simply because all of those operations were convenient to perform in one class. Naming the role makes it easier to keep lifecycle, storage, sequencing, and data transformation behind the boundaries designed to own them.

[`AchievementProgressMutationHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementProgressMutationHandler.java) is a production consumer with four managed dependencies and no consumer-owned keyed store. The excerpt below is shortened from the class; the compatibility-era dependency-map constructor in the source is not part of the target pattern.

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

The important shape is that the consumer declares its capabilities, builds typed operation data, invokes focused behavior, and lets the data/cache owners own storage. [`AchievementPointSummaryHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java) shows the registry-facing side of the same pattern:

```java
PlayerAchievementData data = getDataHandler().load(playerId);

for (AchievementListData definition : getDefinitionRegistry().snapshot()) {
    if (!definition.enabled() || definition.pointType() != pointType) {
        continue;
    }
    // calculate typed summary values
}
```

That consumer asks [`IPlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/interfaces/IPlayerAchievementDataHandler.java) for player data and [`IAchievementListRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/achievement/registry/IAchievementListRegistry.java) for definitions. The underlying [`PlayerAchievementDataHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) coordinates [`PlayerAchievementCache`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/cache/PlayerAchievementCache.java) and persistence so the consumer does not reproduce that workflow.

##### Why

A default consumer should be easy to understand from its declared dependencies and method body.

When storage, cache policy, registry ownership, routing, and orchestration stay behind focused dependencies, the consumer can be tested as behavior rather than as a miniature runtime. The same shape also gives architecture tooling enough information to reason about what the class is allowed to own.

### Data and Metadata Boundary

A primitive key does not justify a generic map value.

Bad:

```java
Map<UUID, Map<String, Object>> playerData;
```

[`FFAActivePlayerSessionData`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionData.java) is the production counterexample: the session has primitive/platform identifiers, but the values remain one named domain type.

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

If metadata must be derived from several sources, the derivation becomes a DI-managed `*MetaDataHandler`. If it is merely passive values already supplied by the caller, use the typed metadata/data value directly. Known fields remain typed; `Map<String, Object>` is not a substitute for deciding what the fields are.

##### Why

Named data gives fields meaning, validation, searchability, and refactor safety that a primitive-keyed or string-keyed map cannot provide.

It also stops metadata from becoming a disguised service boundary. If deriving metadata is behavior, the handler owns that behavior through DI; if the values are already known, the data object should remain passive.

### Consumer-Owned Collection Rejection

Ordinary consumers must not own mutable keyed domain state merely because the state is private or short-lived.

Rejected:

```java
public final class MatchHandler {
    private final Map<UUID, MatchState> activeMatches =
            new ConcurrentHashMap<>();
}
```

[`FFAActivePlayerSessionRegistry`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/player/session/FFAActivePlayerSessionRegistry.java) shows the production ownership pattern:

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

The registry owns collection semantics and lifecycle. A consumer calls the registry through the appropriate Tavall DI surface instead of embedding another `ConcurrentHashMap`.

The same rule applies to caches, repositories, pending-operation state, and metadata: select the owning pattern first, then consume that pattern through DI. See [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md) for the full ownership rule.

##### Why

Private state is still architecture when the class owns it across calls or lifecycle events.

Moving keyed state behind its real owner prevents behavior classes from accumulating hidden storage responsibilities and gives cleanup, replacement, indexing, and synchronization one consistent place to live.

### More Than Four Dependencies

More than four managed dependencies remains a design-review signal. It is not a reason to hide dependencies behind a giant `Dependencies` object, a raw map, or static access.

Choose among:

- keep expanded direct access when the behavior is still clearly cohesive;
- introduce a real domain bundle when several collaborators form one reusable lifecycle boundary;
- split independent phases into focused handlers/services;
- move storage/cache coordination behind the data handler or persistence boundary that actually owns it.

The dependency count is a signal to review the behavior, not an invitation to hide the count.

##### Why

A growing dependency list can mean the class owns too many phases, but hiding the list does not make the coupling disappear.

Reviewing the class at that point forces a useful decision: keep a genuinely cohesive operation explicit, create a real lifecycle/domain boundary, or split unrelated behavior. The goal is clearer ownership, not winning a dependency-count beauty contest.

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

##### Why

Runtime composition creates ownership obligations, not merely convenient references.

Reverse-order cleanup mirrors construction dependencies, while clearing the generation map ensures closed objects cannot remain resolvable. Best-effort cleanup also prevents one failing resource from stranding every resource registered after it.

## Orchestration Pattern

An `*Orchestrator` coordinates an ordered workflow that crosses several already-focused boundaries. It owns **sequencing, lifecycle, and cross-boundary coordination**, not the internal rules or storage of the collaborators it invokes.

Use an orchestrator when the meaningful behavior is the order in which several handlers, routers, schedulers, services, gateways, or runtime boundaries must participate. Do not create an orchestrator merely to rename a large service or to provide a general place where unrelated dependencies can accumulate.

The FFA round lifecycle already demonstrates the pattern in production. [`FFARoundOrchestrator`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/round/orchestrator/FFARoundOrchestrator.java) coordinates the live round tick while [`FFARoundHandler`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/round/handler/FFARoundHandler.java) remains the round state machine, `IFFARoundRuntimeHandler` owns runtime maintenance, `IFFARoundTransitionRouter` routes meaningful transitions, and `IFFARoundTaskScheduler` owns scheduler adaptation. The same ownership split is documented in [`FFA_SYSTEM_FINAL_DRAFT.md`](https://github.com/TavallStudios/tavall-project-novus/blob/main/docs/pvp/FFA_SYSTEM_FINAL_DRAFT.md#round-lifecycle-orchestration).

A shortened production excerpt shows the orchestration responsibility without copying the compatibility-era constructor style from the current class:

```java
@Override
public synchronized RoundMutationResult tick() {
    Instant now = clock.instant();
    Duration elapsed = Duration.between(lastTickAt, now);
    lastTickAt = now;

    FFARoundSnapshot before = roundHandler.snapshot();
    int activeParticipantCount = runtimeHandler.activeParticipantCount();

    runtimeHandler.advanceRuntime(
            now,
            participationElapsed(before, elapsed)
    );

    RoundMutationResult mutation = roundHandler.tick(
            now,
            activeParticipantCount
    );

    transitionRouter.route(mutation, now);
    return mutation;
}
```

The current production class still uses compatibility-era constructor injection and an older injectable marker. Those details are not the pattern being endorsed. The production evidence is the responsibility split and the ordered coordination itself.

An orchestrator may own operation-level state that exists only to coordinate its workflow, such as whether the workflow is running or the timestamp needed to calculate the next step. Durable state, registry state, cache state, and collaborator-specific state remain with their owning boundaries.

##### Why

Sequencing is real behavior. When no class explicitly owns it, the sequence usually leaks into listeners, controllers, schedulers, commands, or one oversized handler, and each caller eventually runs a slightly different version of the workflow.

An orchestrator gives that sequence one testable owner while preserving the focused responsibilities of the components being coordinated. It also gives startup, shutdown, compensation, ordering, and cross-boundary failure handling a natural home without turning the orchestrator into a god class.

## Runtime Rules

- Generated access objects and consumers use the same owning map.
- Interface and concrete aliases share metadata.
- Stable application fallback must not return stale module-generation objects.
- Register dependencies before generated access objects and consumers.
- Tavall-managed application dependencies resolve through the owning dependency map rather than behavior-class constructors.
- Immutable state, builder inputs, configuration, and genuinely externally owned platform handles may remain constructor inputs.
- Orchestrators own workflow sequencing and operation lifecycle, not the domain rules or storage of their collaborators.
- Every resource and dependency has one lifecycle owner.
- Module close clears the generation map and compatibility scope.

## Testing Requirements

Tests verify:

- interface and concrete aliases share metadata and instance identity;
- two module generations use different maps;
- closing one generation does not mutate another generation;
- generated access resolves from the owning module map;
- replacement is visible through an existing generated access instance;
- orchestrators invoke collaborators in the required order and preserve collaborator ownership boundaries;
- orchestrator start/close behavior is deterministic when the orchestrator owns operation lifecycle;
- resources close in reverse order;
- module cleanup clears every owned dependency.

Existing coverage:

- [`ScopedNovusModuleContextTest`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContextTest.java)
- [`NovusModuleReconciliationHandlerTest`](https://github.com/TavallStudios/tavall-project-novus/blob/main/minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/handler/NovusModuleReconciliationHandlerTest.java)
- [`FFARoundOrchestratorTest`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/test/java/org/tavall/minecraft/ffa/round/FFARoundOrchestratorTest.java)
- [`Tavall DI access styles`](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md)
