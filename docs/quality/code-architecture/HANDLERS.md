# Tavall Handler Patterns

> **Status:** Active  
> **Authority:** Binding specialization of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

This chapter owns Handler, DataHandler, MetaDataHandler, and input-adapter behavior. Read the root architecture first and also read any specialized DI, persistence, Registry/Cache, mutable-state, or orchestration chapter touched by the handler.

## Domain Handler Pattern

A domain handler owns one focused behavior or operation family.

Handlers are a common/default Tavall behavior role when the behavior is narrower than a reusable Service capability and does not primarily represent routing, resolution, persistence infrastructure, caching, registry ownership, or orchestration.

A domain handler may own the rule it exists to implement. It should not absorb unrelated policies or the storage mechanics of its collaborators.

#### Bad

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

#### Good

The rank-update operation illustrates the default stateless consumer pattern. The named getters are live Tavall DI accessors, not stored dependencies. The request/result are ordinary typed values, not a reason to introduce request/result builders.

```java
@DelegatesTo(IRankUpdateHandler.class)
public final class RankUpdateHandler
        implements IRankUpdateHandler,
                   DependencyAccess<
                           IPlayerAccountDataHandler,
                           IPowerLevelHandler,
                           IPlayerRankDataHandler
                   > {

    private IPlayerAccountDataHandler getPlayerAccountDataHandler() {
        return getInstance().playerAccountDataHandler();
    }

    private IPowerLevelHandler getPowerLevelHandler() {
        return getInstance().powerLevelHandler();
    }

    private IPlayerRankDataHandler getPlayerRankDataHandler() {
        return getInstance().playerRankDataHandler();
    }

    @Override
    public RankUpdateResult updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
        UUID staffUUID = rankUpdateRequest.staffUUID();
        UUID targetUUID = rankUpdateRequest.targetUUID();

        PlayerAccountData staffAccountData =
                getPlayerAccountDataHandler().load(staffUUID);
        PlayerAccountData targetAccountData =
                getPlayerAccountDataHandler().load(targetUUID);

        boolean canRankEdit = getPowerLevelHandler().canRankEdit(
                staffAccountData,
                targetAccountData
        );
        if (!canRankEdit) {
            return RankUpdateResult.targetTooPowerful();
        }

        getPlayerRankDataHandler().updatePlayerRankData(rankUpdateRequest);
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

When durable persistence is involved, the DataHandler consumes the **entity classes and entity persistence contract defined by the checked-in `tavall-database` version**. This Handler chapter deliberately does not copy a concrete Tavall Database accessor into an example.

A DataHandler must not create an `EntityManager` callback, JDBC transaction wrapper, generic database wrapper, or new Tavall-owned `*Repository` type. Required persistence rules: [Entity Persistence](ENTITY_PERSISTENCE.md).

##### Why

A DataHandler is useful only when it centralizes real data policy. Copying the current persistence accessor into Handler guidance would make this chapter a competing Tavall Database API document.

Data handlers do not decide unrelated product/gameplay authorization merely because they perform the eventual write.

## Metadata Handler Pattern

A metadata handler resolves, refreshes, validates, enriches, or exposes derived metadata.

It does not mutate primary durable data unless the class is explicitly a different persistence/domain behavior owner. The following `fromRankDefinition` is a **proposed** record-owned method to show the ownership split, not an existing production API.

```java
@DelegatesTo(IPlayerRankMetaDataHandler.class)
public final class PlayerRankMetaDataHandler
        implements IPlayerRankMetaDataHandler,
                   DependencyAccess<
                           IPlayerAccountDataHandler,
                           IRankRegistry
                   > {

    private IPlayerAccountDataHandler getPlayerAccountDataHandler() {
        return getInstance().playerAccountDataHandler();
    }

    private IRankRegistry getRankRegistry() {
        return getInstance().rankRegistry();
    }

    @Override
    public PlayerRankMetaData loadPlayerRankMetaData(UUID playerUUID) {
        PlayerAccountData playerAccountData =
                getPlayerAccountDataHandler().load(playerUUID);

        RankKey rankKey = playerAccountData.rankKey();
        Optional<RankDefinition> rankDefinitionLookup =
                getRankRegistry().find(rankKey);
        RankDefinition rankDefinition = rankDefinitionLookup.orElseThrow();

        PlayerRankMetaData playerRankMetaData =
                PlayerRankMetaData.fromRankDefinition(
                        playerAccountData,
                        rankDefinition
                );

        return playerRankMetaData;
    }
}
```

The record owns its conversion logic and any private normalization helpers. An illustrative value-owner method is:

```java
public static PlayerRankMetaData fromRankDefinition(
        PlayerAccountData playerAccountData,
        RankDefinition rankDefinition
) {
    return new PlayerRankMetaData(
            playerAccountData.rankKey(),
            rankDefinition.displayName(),
            rankDefinition.color()
    );
}
```

The record's internal `new` is legitimate value construction. It does **not** make `PlayerRankMetaData` a DI-managed runtime dependency or justify creating a `MetaDataBuilder` for a trivial copy. If metadata construction genuinely needs options, formatting, or complex assembly, use the specialized [Metadata Builder Pattern](BUILDERS.md#metadata-builder-pattern) and keep resolution in this Handler.

##### Why

Metadata is derived state with its own refresh/rebuild behavior. Keeping primary mutation elsewhere prevents a display refresh from quietly becoming a durable write path.

## Handler Ownership Rules

Handlers may coordinate focused dependencies, but they do not:

- constructor-capture Tavall-managed collaborators;
- manually construct/populate Data/MetaData records inline instead of invoking their owning conversion/creation method;
- directly `new` another DI-managed implementation or bypass its public interface contract;
- statically locate Tavall-managed services;
- own mutable registry/cache-shaped maps;
- open JDBC/EntityManager/transaction callbacks;
- create generic CRUD repository/database wrappers;
- absorb routing/scheduling/lifecycle behavior that belongs in an Orchestrator/Router/Runtime;
- hide several unrelated operations behind one generic `handle()` method;
- introduce forwarding-only public methods that merely echo a collaborator's signature and call;
- expose one-use public helpers simply to relocate a condition that belongs in an existing domain operation;
- nest meaningful lookup/results inside downstream delegations rather than separating typed values and handling failure;
- evaluate data accessors directly in conditions (for example `if (progressMutationResult.completedNow())`) instead of outlining a named boolean;
- name a method `get...` when it actually loads, constructs or fills domain data.

##### Why

Handlers remain easy to understand only while their operation boundary is visible. Once they become dependency containers, storage owners, routers, and schedulers simultaneously, `Handler` is just `Manager` with better public relations.

## Review Checklist

- [ ] Root architecture and every additional relevant delegated chapter were read.
- [ ] The handler owns one focused behavior/data/metadata responsibility.
- [ ] Input adapters remain thin and delegate reusable rules.
- [ ] Managed collaborators resolve through Tavall DI.
- [ ] Durable operations follow the checked-in Tavall Database entity contract rather than local transaction/database wrappers.
- [ ] No new Tavall-owned production type ends in `Repository`.
- [ ] No consumer-owned mutable keyed store is hidden in the handler.
- [ ] A Service/Orchestrator/Router/Resolver/Registry/Cache is used when that role is more accurate.
