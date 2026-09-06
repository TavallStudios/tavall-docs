# Project Novus Dependency Injection and Orchestration

> **Status:** Active  
> **Authority:** Supporting chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Module scopes, runtime composition, lifecycle cleanup, and orchestration

The binding Project Novus dependency access patterns live directly in [`CODE_ARCHITECTURE.md`](../CODE_ARCHITECTURE.md#dependency-injection-patterns). This chapter owns only the runtime-scope and composition details that would make the primary architecture document needlessly swollen.

Every Java example is a shortened excerpt from linked production code. If an excerpt stops matching production, update the document rather than preserving architectural fan fiction for sentimental reasons.

## Module Registration Pattern

Register interface and concrete aliases against the same metadata-owned instance.

Source: [`ScopedNovusModuleContext`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

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

Source: [`ScopedNovusModuleContext`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

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

Source: [`AchievementRuntimeBuilder`](../../../novus-achievements/src/main/java/org/tavall/minecraft/achievement/runtime/AchievementRuntimeBuilder.java)

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

Source: [`AchievementCompletionHandler`](../../../novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementCompletionHandler.java)

```java
public final class AchievementCompletionHandler {
    private final JavaPlugin plugin;

    public AchievementCompletionHandler(JavaPlugin plugin) {
        this.plugin = Objects.requireNonNull(plugin, "plugin");
    }
}
```

Do not move a Paper, Velocity, Spring, or other externally owned object into generated DI access merely to make declarations look uniform. This exception does not permit constructor injection of Tavall-managed handlers, services, repositories, registries, caches, gateways, or other application dependencies.

## Module Cleanup Pattern

Close resources in reverse ownership order, then clear the generation map and compatibility scope.

Source: [`ScopedNovusModuleContext`](../../../minecraft-framework/backend-api/src/main/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContext.java)

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

- [`ScopedNovusModuleContextTest`](../../../minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/runtime/ScopedNovusModuleContextTest.java)
- [`NovusModuleReconciliationHandlerTest`](../../../minecraft-framework/backend-api/src/test/java/org/tavall/api/minecraft/runtime/module/handler/NovusModuleReconciliationHandlerTest.java)
- [`Tavall DI access styles`](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md)
