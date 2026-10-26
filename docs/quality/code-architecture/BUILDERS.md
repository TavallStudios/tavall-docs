# Tavall Builder Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Builders are construction tools. They construct typed values, definitions, requests, results, entities, configuration, or another explicit output. They do **not** become runtime composition roots, dependency containers, services, repositories, registries, or orchestrators.

## Pattern Rules

Use a builder when construction is meaningfully clearer because:

- several optional values exist;
- defaults are part of the contract;
- validation belongs before publication;
- the result is immutable or expensive to assemble;
- parsing/conversion produces one typed output.

Do not use a builder merely because a constructor has many Tavall-managed dependencies. A large dependency declaration is a design-review signal, not permission to hide the same graph behind setters.

##### Why

A build call should be predictable from the inputs supplied to the builder. Once a builder resolves managed dependencies, registers services, performs I/O, schedules work, or wires application behavior, construction becomes a hidden lifecycle with failure and replacement semantics callers cannot see.

Keeping builders construction-only makes them safe to reuse in handlers, persistence, tests, migrations, serializers, and other composition paths.

## Bad Pattern: Generic Builder as Dependency Container

```java
public final class RankUpdateHandlerBuilder {
    private IPlayerAccountDataHandler dataHandler;
    private IPlayerAccountCache cache;
    private IPermissionHandler permissionHandler;

    public RankUpdateHandler build() {
        return new RankUpdateHandler(
                dataHandler,
                cache,
                permissionHandler
        );
    }
}
```

##### Why

This does not remove constructor injection. It merely stores the same managed graph in a mutable builder first.

The builder becomes an alternate composition root, callers decide dependency identities, and Tavall DI replacement/reload semantics can be bypassed.

Use `DependencyAccess<...>` on the managed behavior class. If the dependency count is too large, keep direct access when the class is genuinely cohesive, introduce one real immutable domain bundle, or split responsibilities.

## Direct Record Construction and Data Builder Pattern

**Default:** Construct simple `record` values directly. A record's canonical/compact constructor may validate or normalize its own components. Do not add a `DataBuilder` merely to copy constructor parameters, wrap one `new` expression, or satisfy a field-count threshold.

```java
// Typed request data: no builder needed.
RankUpdateRequest rankUpdateRequest = new RankUpdateRequest(
        staffUUID,
        targetUUID,
        rankKey,
        reason,
        false
);
```

A `DataBuilder` becomes useful when the data object has its **own meaningful construction options**: defaults requiring coordination, optional branches, multiple source values that must be assembled, or a nontrivial conversion/hydration process. Those options belong to the data object's construction contract, not to managed dependency wiring.

Project Novus has a substantive example: [`PlayerAchievementDataBuilder`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/builder/PlayerAchievementDataBuilder.java) builds player achievement data from a player ID and optional progress rows, merges the rows, and marks a loaded timestamp. This does more than populate a record's canonical constructor.

```java
public final class PlayerAchievementDataBuilder {

    public PlayerAchievementData buildPlayerAchievementData(
            UUID playerId,
            Collection<PlayerAchievementProgressData> progressRows,
            Instant loadedAt
    ) {
        PlayerAchievementData playerAchievementData = new PlayerAchievementData(playerId);
        if (progressRows != null) {
            progressRows.stream()
                    .filter(Objects::nonNull)
                    .forEach(playerAchievementData::mergeProgress);
        }
        Instant resolvedLoadedAt = loadedAt == null ? Instant.now() : loadedAt;
        return playerAchievementData.markLoaded(resolvedLoadedAt);
    }
}
```

The example's optional progress collection and loaded-time fallback are meaningful assembly decisions. A plain record with a canonical constructor and no additional construction options should not be given this builder.

## Metadata Builder Pattern

The same test applies to `MetaDataBuilder`. Simple metadata records may be constructed directly by the owner that already has their inputs. A metadata builder earns its place when the output requires meaningful derivation, formatting, normalization, optional display settings, or more complex assembly.

A real production example is [`WorldCommandMetaDataBuilder`](https://github.com/TavallStudios/tavall-mc/blob/main/tavall-mc-world/src/main/java/org/tavall/minecraft/world/command/builder/WorldCommandMetaDataBuilder.java). It transforms a `WorldData` value and loaded/current flags into a display-ready metadata object, including a formatted spawn position:

```java
public final class WorldCommandMetaDataBuilder {

    public WorldCommandMetaData buildWorldCommandMetaData(
            WorldData worldData,
            boolean loaded,
            boolean current
    ) {
        WorldData world = Objects.requireNonNull(worldData, "worldData");
        String formattedSpawn = String.format(
                Locale.ROOT,
                "%.2f %.2f %.2f %.1f %.1f",
                world.spawn().x(),
                world.spawn().y(),
                world.spawn().z(),
                world.spawn().yaw(),
                world.spawn().pitch()
        );

        return new WorldCommandMetaData(
                world.worldName(),
                world.displayName(),
                world.serverType().name(),
                world.environment().name(),
                world.enabled(),
                current,
                loaded,
                world.loadOnStartup(),
                world.sortOrder(),
                world.version(),
                formattedSpawn
        );
    }
}
```

The metadata owner resolves the source data/definitions; the builder transforms supplied values. A builder never becomes an excuse for lookup, persistence, cache access, DI graph ownership, or runtime composition.

## Request Builder Pattern

Use a request builder when external input needs parsing, defaults, or conversion before one typed request can be produced.

The builder may receive collaborators as **explicit method inputs** or already-resolved values. A Tavall-managed request builder must not constructor-capture or statically locate managed services merely because parsing needs them.

Simple request values, including ordinary records, do not require a builder (see [Direct Record Construction](#direct-record-construction-and-data-builder-pattern)):

```java
RankUpdateRequest request = new RankUpdateRequest(
        staffUUID,
        targetUUID,
        rankKey,
        reason,
        false
);
```

Use a builder when the construction itself is meaningful:

```java
public final class RankUpdateRequestBuilder {

    public RankUpdateRequest build(
            UUID staffUUID,
            UUID targetUUID,
            RankKey rankKey,
            String reason,
            boolean silent
    ) {
        Objects.requireNonNull(staffUUID, "staffUUID");
        Objects.requireNonNull(targetUUID, "targetUUID");
        Objects.requireNonNull(rankKey, "rankKey");

        return new RankUpdateRequest(
                staffUUID,
                targetUUID,
                rankKey,
                reason,
                silent
        );
    }
}
```

##### Why

The builder owns request construction, not command handling, target lookup, permission checks, or service access. External input adapters resolve those concerns and then ask the builder for one typed value.

## Result Builder Pattern

A result builder is useful only when result construction itself has meaningful optional fields, validation, or reusable defaults.

Prefer typed factories when the result is simple:

```java
return CommandResult.failure(
        CommandFailureReason.TARGET_TOO_POWERFUL
);
```

Do not create `CommandResultBuilder` merely to wrap a one-line typed factory.

##### Why

Builders should reduce construction complexity. Wrapping already-clear factories adds ceremony without ownership value and makes simple result creation harder to read.

## Persistence Entity Builder Pattern

Entity builders may convert domain values into mapped JPA entities.

```java
public final class PlayerAccountEntityBuilder {

    public PlayerAccountEntity buildPlayerAccountEntity(
            PlayerAccountData data
    ) {
        PlayerAccountEntity entity = new PlayerAccountEntity();
        entity.setPlayerUUID(data.getPlayerUUID());
        entity.setPlayerName(data.getPlayerName());
        entity.setRankKey(data.getRankKey());
        return entity;
    }
}
```

The builder does **not** save the entity. Persistence goes through the Tavall Database entity/typed operation boundary.

##### Why

Entity construction and entity persistence are separate responsibilities. The builder maps one value shape to another; Tavall Database owns the persistence lifecycle and transaction behavior.

## Configuration and Definition Builders

Builders are appropriate for immutable definitions with optional configuration:

```java
BukkitBossBarEffectBuilder overtimeBar = new BukkitBossBarEffectBuilder()
        .name(Component.text("OVERTIME"))
        .progress(1.0F)
        .color(BossBar.Color.RED);
```

The builder may snapshot/validate configuration but must not choose audience, schedule work, register services, or perform delivery unless the owning type is explicitly not a builder and represents a workflow/runtime boundary.

##### Why

Definitions remain reusable when they describe **what** should exist rather than **when**, **where**, or **through which runtime dependency** it should be used.

## Runtime Composition Is Not a Builder Pattern

Classes that create/register several managed services, handlers, caches, registries, schedulers, or module objects own **bootstrap/runtime composition**, not ordinary builder behavior.

Use names such as:

```text
AchievementRuntime
AchievementBootstrap
ModuleComposition
FeatureRuntime
```

when those names match the actual lifecycle.

Existing production classes named `*RuntimeBuilder` may remain during migration, but their name is not a template for new code. When touched coherently, move runtime assembly toward explicit bootstrap/runtime composition and Tavall DI registration.

##### Why

Runtime composition creates object identity, registration, replacement, startup order, and cleanup ownership. Calling that a builder hides lifecycle semantics under a construction suffix and encourages ordinary builders to start wiring services.

## Builder Review Checklist

- [ ] The builder produces one explicit typed output.
- [ ] A simple record/immutable value is directly constructed rather than wrapped in a ceremonial DataBuilder.
- [ ] A DataBuilder or MetaDataBuilder exists only for meaningful options, defaults, validation, or assembly beyond simple constructor arguments.
- [ ] Construction complexity justifies the builder.
- [ ] Required values are validated before publication.
- [ ] Defaults are intentional and tested.
- [ ] The builder does not resolve or capture Tavall-managed application dependencies.
- [ ] The builder does not persist, cache, register, schedule, authorize, deliver, or orchestrate runtime behavior.
- [ ] The builder is not being used to hide a large dependency graph.
- [ ] Simple typed factories/constructors are preferred when they are clearer.
- [ ] Runtime composition uses a runtime/bootstrap owner rather than a new `*Builder` pattern.
