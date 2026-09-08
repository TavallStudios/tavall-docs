# Tavall Method Rules

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Method Rules

Methods should be readable top to bottom and perform one coherent operation.

Rules:

- Method names explain the action.
- Important values are extracted into named locals when that improves ownership/debugging.
- Avoid hiding meaningful logic inside deep chained calls.
- Input-adapter methods receive input and delegate.
- Domain-handler methods perform one focused behavior.
- Data methods move/transform data policy without absorbing unrelated product rules.
- Builder methods construct typed output only.
- Pure utility methods remain stateless.
- Cache methods own cache behavior only.
- Durable application operations use Tavall Database entity/typed operations rather than local transaction/database helper methods.

##### Why

Methods are the smallest unit where ownership can become unclear. A method that validates, persists, mutates cache state, formats output, and performs delivery makes every caller depend on all of those concerns at once.

## Method Naming

The class name explains ownership. The method name explains the action.

Avoid:

```text
handlePlayerJoin()
handleRankUpdate()
process()
run()
doThing()
update()
```

Prefer:

```text
loadPlayerAccountData()
buildPlayerRankMetaData()
sendWelcomeMessage()
refreshPlayerTabFormat()
savePunishmentData()
refreshPlayerAccountCache()
```

Boolean methods read like questions:

```text
hasPermission()
canPunish()
isVanished()
shouldSendWelcomeMessage()
```

##### Why

`PlayerJoinHandler#handlePlayerJoin()` repeats the class name instead of explaining the work. Precise method names make call sites and stack traces describe the actual operation.

## Parameters and Requests

Use specific typed parameters. Prefer a request object when several values belong to one operation.

Bad:

```java
ban(String player, String reason);
set(String key, Object value);
```

Good:

```java
banPlayer(PunishmentRequest request);
updatePlayerRank(PlayerRankUpdateRequest request);
```

Raw values are fine when the method is tiny and their meaning is obvious.

##### Why

Typed parameters make invalid combinations harder to express. Request objects give related values one named contract and let the operation evolve without turning every caller into a synchronized signature-editing exercise.

## Local Variables

Extract meaningful intermediate values before nested calls when they help reading, debugging, validation, or failure diagnosis.

Bad:

```java
rankMetaDataHandler.refresh(
        playerAccountDataHandler.load(player.getUniqueId())
);
```

Good:

```java
UUID playerUUID = player.getUniqueId();
PlayerAccountData playerAccountData =
        playerAccountDataHandler.load(playerUUID);

rankMetaDataHandler.refresh(playerAccountData);
```

##### Why

Named locals expose domain values and failure points. The goal is not ceremonial variables; it is making meaningful steps visible.

## Method Size

A method is probably too large when it:

- owns multiple unrelated responsibilities;
- has several levels of nested policy;
- creates data, validates it, persists it, caches it, and sends output itself;
- is hard to name without using “and.”

Split by responsibility, not arbitrary line count.

##### Why

Method size matters because it often reveals several reasons to change. Extracting real phases makes behavior independently testable; private one-line wrappers created only to reduce line count accomplish nothing except vertical scrolling.

## Domain Handler Methods

A domain handler method may own the focused rule it exists to implement.

Example shape:

```java
public RankUpdateResult updatePlayerRank(
        RankUpdateRequest request
) {
    PlayerAccountData staff = getDataHandler().load(request.staffUUID());
    PlayerAccountData target = getDataHandler().load(request.targetUUID());

    if (!getPowerLevelHandler().canRankEdit(staff, target)) {
        return RankUpdateResult.targetTooPowerful();
    }

    getRankDataHandler().updatePlayerRankData(request);
    return RankUpdateResult.success();
}
```

The handler may coordinate focused dependencies through Tavall DI. It does not own their backing maps, transaction callbacks, or unrelated rules.

##### Why

A handler is an operation owner, not a storage/runtime-container owner. Domain rules can live there while persistence/cache/registry mechanics stay behind the dependencies designed to own them.

## Input Adapter Methods

Commands, listeners, controllers, and other external-input methods should:

1. read/validate transport input;
2. resolve/build typed operation input;
3. call the domain handler/service/orchestrator;
4. adapt the typed result back to the transport.

They should not become the reusable domain rule simply because the event arrived there first.

##### Why

Platform syntax and lifecycle change for different reasons than domain behavior. Thin adapters let one rule serve multiple surfaces.

## Data Handler Methods

A data handler is useful when several callers need the same data policy, such as Tavall Database + cache coordination, mapping, batching, retry, or retention.

```java
public PlayerAccountData loadPlayerAccountData(UUID playerUUID) {
    Optional<PlayerAccountEntity> entity =
            getDatabase().entities().find(
                    PlayerAccountEntity.class,
                    playerUUID
            );

    return entity
            .map(playerAccountDataBuilder::buildPlayerAccountData)
            .orElse(null);
}
```

A data handler is not mandatory ceremony around every entity operation. It should not decide unrelated product authorization rules.

##### Why

Data policy deserves one reusable owner when policy actually exists. A wrapper that only forwards `entities().find()` adds no ownership value.

## Builder Methods

Builder methods construct typed values. They do not persist, cache, register managed behavior, schedule, authorize, or resolve Tavall-managed dependencies.

##### Why

A build call should be predictable from explicit inputs. Hidden runtime effects turn construction into an undocumented workflow.

## Data and Metadata Builder Methods

Data builders convert one explicit value shape to another.

```java
public PlayerAccountData buildPlayerAccountData(
        PlayerAccountEntity entity
) {
    return new PlayerAccountData(
            entity.getPlayerUUID(),
            entity.getPlayerName(),
            entity.getRankKey()
    );
}
```

Metadata builders produce derived/display-ready values from already-provided source data/definitions.

##### Why

Construction stays separate from lookup/persistence ownership, and derived metadata remains easy to rebuild when source definitions change.

## Pure Utility Methods

Pure static utility methods may transform explicit inputs without hidden runtime state.

They must not access Tavall-managed services, persistence, caches, registries, schedulers, platform state, or global mutable state.

##### Why

Pure helpers are broadly safe because their result depends only on explicit input. Runtime behavior needs DI/lifecycle ownership and therefore is not a pure utility.

## Tavall Database Methods

Application code does **not** own `EntityManager`, transaction callbacks, or generic database helper classes for ordinary persistence.

Use:

```java
Optional<PlayerAccountEntity> entity =
        getDatabase().entities().find(
                PlayerAccountEntity.class,
                playerUUID
        );

getDatabase().entities().save(playerAccountEntity);
```

For multi-entity transaction semantics, use/add a typed Tavall Database operation rather than writing a local callback wrapper.

Native PostgreSQL behavior remains at the mapped entity/typed Tavall Database boundary with an explicit `Native SQL reason:`.

##### Why

Transaction and entity-manager lifecycle belong to Tavall Database. A local `find()` method that manually grabs an `EntityManager` recreates the persistence runtime inside application code and is precisely the architecture being removed.

## Cache Methods

Cache methods own disposable fast-access behavior such as lookup, put, invalidation, TTL refresh, grouped removal, and snapshots through Tavall Cache.

They do not become durable writes or authoritative reads by convenience.

##### Why

Eviction, expiration, restart, and invalidation must remain safe. If a cache operation is the only permanent write, the boundary is misclassified.

## Test Methods

Test method names describe the behavior being tested:

```text
modCannotPunishAdmin()
ownerCanPunishManager()
rankUpdateRefreshesPlayerAccountCache()
missingPlayerAccountReturnsFallbackData()
```

##### Why

Behavior-oriented names make CI failures explain the contract that broke rather than forcing readers to open `testUpdate()` and conduct archaeology.
