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

## Data Builder Pattern

Data builders create one typed data value from explicit source values.

```java
public final class PlayerAccountDataBuilder {

    public PlayerAccountData buildPlayerAccountData(
            PlayerAccountEntity entity
    ) {
        UUID playerUUID = entity.getPlayerUUID();
        String playerName = entity.getPlayerName();
        RankKey rankKey = entity.getRankKey();

        return new PlayerAccountData(
                playerUUID,
                playerName,
                rankKey
        );
    }
}
```

##### Why

The class says what data it builds and the source-to-domain conversion stays separate from persistence/runtime behavior.

A builder may validate or normalize its explicit inputs, but it does not load them from a service, cache, registry, or database by itself.

## Metadata Builder Pattern

Metadata builders create resolved or display-ready values from source data already provided to them.

```java
public final class PlayerRankMetaDataBuilder {

    public PlayerRankMetaData buildPlayerRankMetaData(
            PlayerAccountData accountData,
            RankDefinition rankDefinition
    ) {
        return new PlayerRankMetaData(
                accountData.getRankKey(),
                rankDefinition.getDisplayName(),
                rankDefinition.getLegacyColor(),
                rankDefinition.getPowerLevel()
        );
    }
}
```

##### Why

Metadata is derived state with different rebuild/invalidation semantics from its source data. The builder expresses that transformation without becoming the owner that looks up the source values.

## Request Builder Pattern

Use a request builder when external input needs parsing, defaults, or conversion before one typed request can be produced.

The builder may receive collaborators as **explicit method inputs** or already-resolved values. A Tavall-managed request builder must not constructor-capture or statically locate managed services merely because parsing needs them.

Simple request values do not require a builder:

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
- [ ] Construction complexity justifies the builder.
- [ ] Required values are validated before publication.
- [ ] Defaults are intentional and tested.
- [ ] The builder does not resolve or capture Tavall-managed application dependencies.
- [ ] The builder does not persist, cache, register, schedule, authorize, deliver, or orchestrate runtime behavior.
- [ ] The builder is not being used to hide a large dependency graph.
- [ ] Simple typed factories/constructors are preferred when they are clearer.
- [ ] Runtime composition uses a runtime/bootstrap owner rather than a new `*Builder` pattern.
