# Tavall Validation, Fallbacks, and Anti-Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Validation Pattern

Validate before mutation. Validation should be typed, readable, and performed at the boundary that owns the invariant.

Bad:

```java
public void updateRank(String rankName) {
    if (rankName != null) {
        // mutate
    }
}
```

Good:

```java
public RankUpdateResult updatePlayerRank(
        RankUpdateRequest request
) {
    if (!getRankRegistry().contains(request.rankKey())) {
        return RankUpdateResult.invalidRank();
    }

    getRankDataHandler().updatePlayerRankData(request);
    return RankUpdateResult.success();
}
```

##### Why

Typed validation rejects invalid state before side effects begin and makes expected rejection explicit rather than leaving later storage/platform code to discover the problem accidentally.

## Fallback Pattern

Fallbacks are intentional, typed, visible, and owned. They must not convert failed required writes or violated invariants into fake success.

A presentation fallback may provide safe output for missing optional metadata. A durable write failure may not silently become “success with in-memory state.”

##### Why

A fallback changes failure semantics. If its ownership/reconciliation is not explicit, degraded behavior becomes an undocumented second source of truth.

# Anti-Patterns

## God Class

Bad:

```java
public final class ProjectCoreManager {
}
```

A god class owns unrelated domains, lifecycle, storage, routing, and presentation.

##### Why

Every change touches the same owner and tests must recreate unrelated systems. Split by real responsibility/lifecycle instead of adding forwarding wrappers.

## Manager Pattern

Avoid new `*Manager` classes unless maintaining an external established API that cannot be changed.

Use an exact role:

```text
RankUpdateHandler
RankRegistry
PlayerAccountDataHandler
PlayerRankMetaDataBuilder
FFARoundOrchestrator
```

##### Why

`Manager` does not state what the class owns. Exact suffixes give callers, reviewers, and architecture tests a contract.

## Helper Pattern

Avoid vague `*Helper`, `Common`, and `Misc` classes.

##### Why

They become junk drawers because the name provides no boundary for rejecting the next unrelated method.

## Static Dependency Access

Static syntax is not the problem. Static ownership/lookup of runtime behavior is.

Tavall-managed application dependencies resolve through the owning DI map.

Bad:

```java
public static IEconomyService economyService() {
    return DependencyLoaderAccess.findInstance(IEconomyService.class);
}
```

Allowed statics are dependency-free:

- constants/immutable constant values;
- pure parsing/normalization/transformation;
- private pure helpers;
- construction-only `of(...)`, `from(...)`, `builder()`, `create(...)` methods.

A static factory/builder must not resolve DI, perform I/O, touch mutable runtime state, schedule work, or become a hidden composition root.

##### Why

A static locator erases dependency ownership from the class declaration and bypasses replacement, generation, lifecycle, and test composition semantics.

## Application-Owned Mutable Map Pattern

Application-owned mutable keyed state is prohibited by default.

Bad:

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

Route state by semantics:

- runtime identity/session/definitions -> Tavall Registry;
- expiring/reloadable/disposable state -> Tavall Cache;
- durable state -> Tavall Database mapped entity/typed operation;
- distributed runtime state -> owning Redis/distributed boundary;
- in-flight tasks/futures/retries -> dedicated typed operation/runtime owner;
- immutable value/snapshot -> typed data;
- repository -> only a real persistence/substitution contract beyond ordinary entity CRUD.

Full rule: [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md).

##### Why

A thread-safe map still has authority/lifecycle semantics. Putting it in an ordinary consumer silently makes that consumer the registry/cache/runtime/persistence owner.

## Raw String Pattern

Bad:

```java
permissionHandler.has(player, "punishment.ban");
```

Good:

```java
permissionHandler.has(player, PermissionNode.PUNISHMENT_BAN);
```

##### Why

Typed keys are searchable/refactorable and let the compiler reject category mistakes. Raw strings compile typos with tremendous confidence.

## Hidden Side Effect Pattern

A method name must not hide unrelated mutation.

Bad:

```java
public PlayerAccountData getPlayerAccountData(UUID playerUUID) {
    PlayerAccountData data = load(playerUUID);
    cache.put(playerUUID, data);
    tabHandler.refresh(playerUUID);
    return data;
}
```

Prefer explicit actions with honest names and owners.

##### Why

Callers reason from method contracts. Hidden cache/presentation/persistence effects turn innocent reads into workflows and make retry/error behavior impossible to infer.

## Generic CRUD Wrapper Pattern

Bad:

```java
public final class PostgresPlayerRepository {
    public Optional<PlayerEntity> find(UUID id) {
        return database.entities().find(PlayerEntity.class, id);
    }

    public void save(PlayerEntity entity) {
        database.entities().save(entity);
    }
}
```

Ordinary Tavall Database entity CRUD does not need this wrapper.

##### Why

The class adds no domain persistence contract and creates another place for transaction/query/failure behavior to drift. Use the Tavall Database entity boundary directly from the owning behavior/data policy.

## JPA Callback Ownership Pattern

Production application code must not own:

```text
EntityManager
EntityTransaction
IPostgresJpaContext callbacks
database.jpa().read(...)
database.jpa().write(...)
raw JDBC transaction wrappers
```

Use mapped entities/typed Tavall Database operations. Add missing multi-entity operations upstream to Tavall Database instead of recreating callbacks downstream.

##### Why

Transaction/entity-manager lifecycle is infrastructure-wide ownership. Local callback wrappers reproduce the persistence runtime inside feature code.

## Review Checklist

- [ ] Validation occurs before mutation where possible.
- [ ] Fallbacks have explicit ownership/reconciliation and never fake required-write success.
- [ ] No God/Manager/Helper bucket hides unrelated behavior.
- [ ] Static methods do not locate Tavall-managed runtime dependencies.
- [ ] Mutable keyed state has Registry/Cache/Tavall Database/distributed/runtime ownership.
- [ ] Stable keys/values use typed representations rather than raw strings/maps.
- [ ] Method names disclose side effects.
- [ ] Ordinary Tavall Database CRUD is not wrapped in generic repositories/databases/stores.
- [ ] Application code owns no JPA callbacks/JDBC transaction lifecycle.
