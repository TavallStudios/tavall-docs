# Tavall Handler Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Domain Handler Pattern

A domain handler owns one focused behavior or operation family.

Handlers are a common/default Tavall behavior role when the behavior is narrower than a reusable Service capability and does not primarily represent routing, resolution, persistence infrastructure, caching, registry ownership, or orchestration.

A domain handler may own the rule it exists to implement. It should not absorb unrelated policies or the storage mechanics of its collaborators.

Bad:

```java
public final class RankCommand {
    public void execute(Player staff, Player target, String rankName) {
        if (staff.isOp()) {
            target.setDisplayName(rankName);
        }
    }
}
```

##### Why

The command owns reusable rank/authority behavior, uses raw input, and mutates platform state directly. The external input surface became the domain rule merely because it received the command first.

Good shape:

```java
@DelegatesTo(IRankUpdateHandler.class)
public final class RankUpdateHandler
        implements IRankUpdateHandler,
        DependencyAccess<
                IPlayerAccountDataHandler,
                IPowerLevelHandler,
                IPlayerRankDataHandler
        > {

    @Override
    public RankUpdateResult updatePlayerRank(
            RankUpdateRequest request
    ) {
        IDependencyMap dependencies = getInstance();

        PlayerAccountData staff = dependencies
                .iPlayerAccountDataHandler()
                .load(request.staffUUID());

        PlayerAccountData target = dependencies
                .iPlayerAccountDataHandler()
                .load(request.targetUUID());

        if (!dependencies.iPowerLevelHandler().canRankEdit(staff, target)) {
            return RankUpdateResult.targetTooPowerful();
        }

        dependencies
                .iPlayerRankDataHandler()
                .updatePlayerRankData(request);

        return RankUpdateResult.success();
    }
}
```

##### Why

The handler owns one rank-update operation, declares its capabilities through Tavall DI, and delegates data policy/authority sub-rules to focused boundaries. It does not own their backing collections or transaction mechanics.

## Input Adapter Pattern

Commands, listeners, controllers, GUI actions, plugin messages, and other external-input surfaces are adapters.

They should:

1. receive transport/platform input;
2. resolve/build typed operation input;
3. call the domain handler/service/orchestrator;
4. adapt the typed result back to the surface.

They should not perform durable I/O directly or become the reusable domain rule.

##### Why

Transport syntax and lifecycle change independently from domain behavior. Thin adapters let the same behavior serve multiple surfaces and keep platform-specific failure/cancellation concerns at the edge.

## Data Handler Pattern

A data handler owns reusable **data policy** when policy exists, such as:

- Tavall Database entity + cache coordination;
- domain/entity mapping;
- dirty-state/retry behavior;
- batching/retention;
- one consistent load/save/update policy used by several consumers.

A data handler is not mandatory around every entity operation.

Example:

```java
@DelegatesTo(IPlayerAccountDataHandler.class)
public final class PlayerAccountDataHandler
        implements IPlayerAccountDataHandler,
        DependencyAccess<IPostgresDatabase> {

    @Override
    public PlayerAccountData load(UUID playerUUID) {
        Optional<PlayerAccountEntity> entity = getInstance()
                .entities()
                .find(PlayerAccountEntity.class, playerUUID);

        return entity
                .map(PlayerAccountData::fromEntity)
                .orElse(null);
    }
}
```

##### Why

A data handler is useful when it centralizes real data behavior. A class that only forwards one `database.entities().find()` call adds no policy and should not exist by habit.

Data handlers do not decide unrelated product/gameplay authorization merely because they perform the eventual write.

## Metadata Handler Pattern

A metadata handler resolves, refreshes, validates, enriches, or exposes derived metadata.

It does not mutate primary durable data unless the class is explicitly a different persistence/domain behavior owner.

Example shape:

```java
@DelegatesTo(IPlayerRankMetaDataHandler.class)
public final class PlayerRankMetaDataHandler
        implements IPlayerRankMetaDataHandler,
        DependencyAccess<
                IPlayerAccountDataHandler,
                IRankRegistry
        > {

    public PlayerRankMetaData load(UUID playerUUID) {
        IDependencyMap dependencies = getInstance();
        PlayerAccountData account = dependencies
                .iPlayerAccountDataHandler()
                .load(playerUUID);

        RankDefinition definition = dependencies
                .iRankRegistry()
                .find(account.rankKey())
                .orElseThrow();

        return new PlayerRankMetaData(
                account.rankKey(),
                definition.displayName(),
                definition.color()
        );
    }
}
```

##### Why

Metadata is derived state with its own refresh/rebuild behavior. Keeping primary mutation elsewhere prevents a display refresh from quietly becoming a durable write path.

## Handler Ownership Rules

Handlers may coordinate focused dependencies, but they do not:

- constructor-capture Tavall-managed collaborators;
- statically locate Tavall-managed services;
- own mutable registry/cache-shaped maps;
- open JDBC/EntityManager/transaction callbacks;
- create generic CRUD repository/database wrappers;
- absorb routing/scheduling/lifecycle behavior that belongs in an Orchestrator/Router/Runtime;
- hide several unrelated operations behind one generic `handle()` method.

##### Why

Handlers remain easy to understand only while their operation boundary is visible. Once they become dependency containers, storage owners, routers, and schedulers simultaneously, `Handler` is just `Manager` with better public relations.

## Review Checklist

- [ ] The handler owns one focused behavior/data/metadata responsibility.
- [ ] Input adapters remain thin and delegate reusable rules.
- [ ] Managed collaborators resolve through Tavall DI.
- [ ] Durable operations use Tavall Database/data policy rather than local transaction/database wrappers.
- [ ] No consumer-owned mutable keyed store is hidden in the handler.
- [ ] A Service/Orchestrator/Router/Resolver/Registry/Cache is used when that role is more accurate.
