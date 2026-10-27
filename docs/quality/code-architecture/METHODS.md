# Tavall Method Rules

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Method Rules

Methods should be readable top to bottom and perform one coherent operation.

Rules:

- Method names and the owning class role indicate whether an operation reads existing data, loads, constructs/fills, derives, mutates, or delivers; see [Data State and Method Name Contracts](#data-state-and-method-name-contracts).
- Outline meaningful input values, intermediate results and branch-driving booleans in explicitly typed, domain-named locals before consuming them; see [Variable Outlining](#variable-outlining).
- Production local variables use explicit Java types rather than `var`.
- Avoid hiding meaningful logic inside deep chained calls.
- Input-adapter methods receive input and delegate.
- Domain-handler methods perform one focused behavior.
- Data methods move/transform data policy without absorbing unrelated product rules.
- Builder methods construct typed output only.
- Managed consumers call typed data-owned conversion methods instead of manually populating records with inline `new`; constructors remain valid within value/builder/factory owners.
- Pure utility methods remain stateless.
- Cache methods own cache behavior only.
- Durable application operations follow Tavall Database entity classes/current typed contract rather than local transaction/database helper methods.

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

## Data State and Method Name Contracts

**A caller must know from the class role and method name whether the value is already filled or whether the method will fill, produce, or change it.** These conventions apply to new Tavall application-domain APIs and coherent migrations; canonical Tavall Tool interfaces remain authoritative for their existing API vocabulary.

| Name / role | Caller expectation |
| --- | --- |
| `get...` or record component accessor | Read an already-available value. Do not silently initialize missing domain data. Record booleans such as `completedNow()` retain Java's accessor name. |
| `find...` | Look up existing data without creating it, with explicit absence (typically `Optional<T>`). |
| `require...` | Read existing required data, failing explicitly if unavailable. |
| `load...` in a DataHandler/Reader | Obtain data through a potentially expensive loading/hydration/cache policy. May assemble a value under that documented policy. |
| `from...` / `create...` / `of...` on a value type | Construct and return a complete new value with the type's own validation/defaults. |
| `build...` on a DataBuilder/MetaDataBuilder | Construct a complete typed value when meaningful optional inputs, defaults or assembly justify a separate Builder. |
| `resolve...` / `calculate...` / `format...` on an owning role | Derive/read a computed or presentation result, not silently persist or mutate state. |
| `is...` / `has...` / `can...` / `should...` | Read/evaluate a boolean condition without changing state. |
| `fill...` / `populate...` / `merge...` / `update...` / `apply...` on a data owner | Change the contents/state of the explicitly owned target, not silently create a different object or conceal a load. |
| `save...` / `send...` / `publish...` | Perform the named persistence, delivery or event side effect through its owner. |

For example, a `getPlayerAchievementData()` method must not covertly create an account when missing. `loadPlayerAchievementData()` signals access through a loading path; `AchievementProgressEventData.fromProgressRequest(...)` signals construction of a newly filled record; `PlayerAchievementData.mergeCommittedProgress(...)` signals mutation of an existing data owner. Do not add a Builder solely to avoid a record's constructor.

**The verb is a semantic contract, not a prefix to add mechanically.** A record's `completedNow()` is an existing-value read, not a fill command. A getter returning a DI-managed collaborator is a live dependency accessor as defined by Tavall DI, not a call to construct that collaborator. Preserve canonical tool naming where its real behavior is documented differently.

## Method Visibility and Ownership

A public method on a DI-managed Handler/Service/DataHandler expresses an operation that belongs in that role's interface contract. Do not expose raw DI wiring, constructor internals, or one-off convenience methods as public domain APIs.

Private named DI getters (for example `getPlayerAchievementDataHandler()`) resolve live through `DependencyAccess<...>` and keep dependency mechanics out of the operation body. Private non-DI helpers should implement genuine class-local behavior; avoid unnecessary wrappers created only to hide an unclear design.

Records/value objects may expose **public value-specific methods** (for example `AchievementProgressEventData.fromProgressRequest(...)`) while keeping construction, validation, normalization, and auxiliary helpers private/internal. Domain authorization or persistence does **not** become record behavior merely because the record can define methods. Record factories/converters may call their own constructors internally. This is different from an ordinary DI consumer calling `new` for a data object or another managed component.

The complete [consumer pattern](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md#multi-dependency-expanded-access) demonstrates the proposed record-owned conversion and DataHandler-owned cache reconciliation. The concrete source/interfaces must be updated before those methods exist in production.

**Pure forwarding is an anti-pattern:** a new public method that only calls another method with the same parameters and returns its result adds no behavior, policy, translation, or ownership. Keep the underlying capability public when it truly is the supported operation; otherwise give the adapter a real input/output translation job. Private named DI getters remain an intentional exception because they own live typed lookup, not domain forwarding.

**One-use method extraction is not always separation:** avoid promoting a one-line predicate such as `canReplace(...)` to a new public API merely because it can be moved from the actual data owner's merge operation. Method visibility is based on a real external contract or reuse need; keep localized implementation details private or inline with their owner.

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

Outline meaningful domain reads, intermediate results and boolean conditions before calling another capability or branching. See [Variable Outlining](#variable-outlining). Production source uses explicit local types; detailed `var` rules live in [Namespaces, Variables, OOP, DRY, and Type Safety](NAMESPACES_VARIABLES_AND_OOP.md#local-variables).

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

## Variable Outlining

**Outline meaningful domain values before they are evaluated, delegated or mutated.** This includes boolean-returning accessors even when their value controls only one `if` statement. Use explicit Java types, stable domain names and separate lines for distinct operation stages.

Bad:

```java
if (progressMutationResult.completedNow()) {
    getAchievementCompletionHandler().sendAchievementCompletionMessage(
            progressMutationResult.updatedProgress(),
            achievementProgressRequest.achievementDefinition()
    );
}
```

Good (after the mutation result and progress have been validated):

```java
boolean achievementCompletedNow = progressMutationResult.completedNow();

if (achievementCompletedNow) {
    getAchievementCompletionHandler().sendAchievementCompletionMessage(
            updatedProgress,
            achievementDefinition
    );
}
```

The reader sees *what data exists* (`updatedProgress`, `achievementDefinition`), *what was checked* (`achievementCompletedNow`), and *what is performed* (`sendAchievementCompletionMessage`). The boolean local is not ceremonial, even when used once. Likewise, extract `UUID playerUUID`, `AchievementProgressEventData progressEventData`, and `AchievementProgressMutationResult progressMutationResult` before dependent validation or calls.

Do not outline literal constants, trivial loop mechanics or unconsumed void commands. Do not assign generated DI access to a local alias as a substitute for separating the **domain values**. Name booleans after the actual fact (`achievementCompletedNow`, `shouldMergeProgress`, `canRankEdit`), not `flag`, `valid` or `check`.

## Intermediate Values and Delegation Anti-Patterns

Keep meaningful operations readable as explicit stages. Separate a value when its result is checked, reused, changes domain ownership, carries an error state, or would otherwise be buried in a call chain. Use the **full Java type** and a **domain-specific variable name**. Do not create an alias for the generated DI access object or local getters solely to remove a method call.

Bad:

```java
getPlayerAchievementDataHandler().applyCommittedPlayerAchievementProgress(
        achievementProgressRequest.playerUUID(),
        getAchievementEventMutationAccess().applyEventProgressOnce(
                AchievementProgressEventData.fromProgressRequest(achievementProgressRequest),
                achievementProgressRequest.achievementDefinition()
        ).updatedProgress()
);
```

This collapses conversion, durable mutation, possible-null result validation, and cache reconciliation into one call. Instead keep `AchievementProgressEventData progressEventData`, `AchievementProgressMutationResult progressMutationResult`, `PlayerAchievementProgressData updatedProgress`, and `UUID playerUUID` separate as shown in the [full consumer example](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md#multi-dependency-expanded-access).

Bad forwarding wrapper:

```java
public void applyCommittedPlayerAchievementProgress(
        UUID playerUUID,
        PlayerAchievementProgressData updatedProgress
) {
    getPlayerAchievementDataHandler().applyCommittedPlayerAchievementProgress(
            playerUUID, updatedProgress
    );
}
```

This method owns no translation, data policy, cache mutation, or domain rule; it only copies the signature. A DataHandler implementation that **loads player data, locks its state, merges newer progress, and updates the Cache** is different: those are real responsibilities.

Also avoid ceremonial locals that only rename a one-time literal/return expression. Extractions are for meaningful stages and diagnostics, not adding lines for their own sake.

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

A domain handler method may own the focused rule it exists to implement. The canonical complete method example now lives in [Handler Patterns](HANDLERS.md#domain-handler-pattern): `RankUpdateHandler.updatePlayerRank(RankUpdateRequest)`.

That example shows explicit, meaningful locals (`staffAccountData`, `targetAccountData`, `canRankEdit`), named live DI getters, a typed outcome, and no manually captured dependency-access variable. Keep the method naming and code-shape rules here; keep full Handler examples in their owning chapter so the two documents do not drift apart.

A handler is an operation owner, not a storage/runtime-container owner. Domain rules may live there while persistence/cache/registry mechanics stay behind the capabilities designed to own them.

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

When it touches durable entities, it consumes the entity classes and entity persistence contract defined by the checked-in `tavall-database` module. This shared chapter intentionally does not copy a concrete Tavall Database accessor into application examples.

A data handler is not mandatory ceremony around every entity operation. It should not decide unrelated product authorization rules and must not recreate a `*Repository` layer.

##### Why

Data policy deserves one reusable owner when policy actually exists. A forwarding wrapper around one Tavall Database call adds no ownership value.

## Builder Methods

Builder methods construct typed values. Simple records and immutable data are constructed directly; a DataBuilder/MetaDataBuilder is for meaningful options, defaults, validation, or nontrivial assembly, not copying record components. The owning [Builder Patterns](BUILDERS.md#record-owned-construction-and-data-builder-pattern) chapter has the examples. Builders do not persist, cache, register managed behavior, schedule, or authorize.

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

Application code does **not** own `EntityManager`, transaction callbacks, JDBC lifecycle, generic database helper classes, or `*Repository` types for ordinary persistence.

Application methods use the Tavall Database entity classes and the entity persistence/operation contract exposed by the checked-in module. If a required multi-entity transaction or durable operation is missing, add the typed capability upstream to Tavall Database rather than introducing a local callback or wrapper.

Native PostgreSQL behavior remains at the mapped entity/typed Tavall Database boundary with an explicit database-specific reason according to Tavall Database policy.

##### Why

Persistence runtime and transaction lifecycle belong to Tavall Database. Shared application docs should preserve that ownership without freezing whichever accessor the module happens to expose today.

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
