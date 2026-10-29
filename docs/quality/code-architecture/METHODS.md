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
- Managed consumers use typed DI getters for managed capabilities and value-owned creation or conversion APIs for data; avoid routine inline application object instantiation. See [Object Instantiation](#object-instantiation-in-managed-consumer-methods).
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

**Keep method vocabulary small and consistent with the existing examples.** Favor `get`, `set`, `has`, `is`, `can`, `should`, `add` and `remove`, followed by the **exact domain action or value**. Use established specialized verbs (`load`, `save`, `build`, `resolve`, `send`, `refresh`, `update`, `merge`) when the class role and actual behavior call for them. This is guidance, **not** an exhaustive word dictionary or an automatic rewrite of canonical Java Tool APIs.

```text
getAchievementListData()          // Named DI getter for the available typed class
hasAchievementProgress()
isAchievementEnabled()
canRankEdit()
shouldSendWelcomeMessage()
addAchievementProgress()
removeAchievementProgress()
loadPlayerAccountData()           // DataHandler owns loading
buildPlayerRankMetaData()         // Meaningful metadata construction
sendAchievementCompletionMessage()
```

A method name should communicate whether data is already available or will be filled/changed. Do not hide initialization or mutation inside an ordinary `get...` method, add a builder for a trivial record, or create a forwarding class merely to rename an existing tool API. The **class role, actual operation, and current tests** determine the correct name.

A private DI getter such as `getAchievementListData()` accesses an already registered typed instance. Registry identity/key selection and backing storage are not consumer responsibilities. The owning runtime must ensure the appropriate instance is bound for the operation. Native Java record component accessors such as `completedNow()` keep their language-defined names; [Variable Outlining](#variable-outlining) governs named boolean locals at call sites.

## Method Visibility and Ownership

A public method on a DI-managed Handler/Service/DataHandler expresses an operation that belongs in that role's interface contract. Do not expose raw DI wiring, constructor internals, or one-off convenience methods as public domain APIs.

Private named DI getters (for example `getPlayerAchievementDataHandler()`) resolve live through `DependencyAccess<...>` and keep dependency mechanics out of the operation body. Private non-DI helpers should implement genuine class-local behavior; avoid unnecessary wrappers created only to hide an unclear design.

Records/value objects may expose **public value-specific methods** (for example `AchievementProgressEventData.fromProgressRequest(...)`) while keeping construction, validation, normalization, and auxiliary helpers private/internal. Pure static value factories are permitted when they perform actual construction with their supplied inputs. Domain authorization or persistence does **not** become record behavior merely because the record can define methods. Record factories/converters may call their own constructors internally. This is different from an ordinary DI consumer calling `new` for a data object or another managed component.

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

Outline **new computed/loaded operation results** and named decisions before using them. Do **not** alias fields, record components or DI getter results already accessible through their owning instances merely for outlining. See [Variable Outlining](#variable-outlining). Production source uses explicit local types; detailed `var` rules live in [Namespaces, Variables, OOP, DRY, and Type Safety](NAMESPACES_VARIABLES_AND_OOP.md#local-variables).

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

**Outline decisions and genuinely new operation results; do not duplicate already-owned data through local accessor aliases.** An explicit local is useful when an operation *produces* a result, when a boolean expresses a condition, or when a stable snapshot/identity is actually required. Simply reading an existing record component or a named DI getter does not justify copying it.

Bad: locals that only re-name existing data.

```java
UUID playerUUID = achievementProgressRequest.playerUUID();
AchievementListData achievementDefinition = getAchievementListData();
PlayerAchievementProgressData updatedProgress =
        progressMutationResult.updatedProgress();
```

Good: call the existing owner directly; outline branch decisions.

```java
boolean hasUpdatedProgress =
        progressMutationResult.updatedProgress() != null;
boolean achievementCompletedNow =
        progressMutationResult.completedNow();

if (hasUpdatedProgress && achievementCompletedNow) {
    getAchievementCompletionHandler().sendAchievementCompletionMessage(
            progressMutationResult.updatedProgress(),
            getAchievementListData()
    );
}
```

Good: outline a genuinely new load or computation result **where that operation belongs**:

```java
PlayerAchievementData playerAchievementData =
        getPlayerAchievementDataHandler().load(playerUUID);
```

When the caller **already receives** `AchievementProgressMutationResult progressMutationResult`, use its populated `updatedProgress()` directly rather than recreating an event or defining an alias.

Variables still use explicit Java types, domain-specific names and meaningful scopes. Avoid pointless one-use aliases for record accessors, `getInstance()`, named DI getters, constants, and data already available from their owner. Extract a getter result only if a **real** requirement exists, such as an intentional immutable snapshot, required reuse of an expensive calculation, an identity/consistency boundary, or mutation of an independently owned local value. These are exceptions justified by semantics, not stylistic ceremony.

## Object Instantiation in Managed Consumer Methods

**Default: ordinary Tavall DI-managed consumers do not instantiate application classes inside their behavior methods with `new SomeClass(...)`.** Managed instances come from Tavall DI through typed named getters. Data/value creation belongs to the record, real Builder, factory or owning composition boundary. Consumer methods primarily operate on typed inputs and managed capabilities rather than constructing collaborators or filling domain objects manually.

Bad in an ordinary Handler:

```java
AchievementProgressEventData progressEventData =
        new AchievementProgressEventData(
                eventId,
                playerUUID,
                triggerType,
                progressAmount,
                actionType,
                sourceServerId,
                sourceContext,
                occurredAt
        );

IAchievementCompletionHandler completionHandler =
        new AchievementCompletionHandler(plugin);
```

Good: if progress is already filled, use that existing data with its owner. No construction is required:

```java
getPlayerAchievementDataHandler().updatePlayerAchievementProgress(
        progressMutationResult.updatedProgress()
);
```

**This is not a ban on static calls.** A pure record factory such as `AchievementProgressEventData.fromProgressRequest(...)`, `Objects.requireNonNull(...)`, `Math.max(...)`, enum constants, and legitimate JDK/platform utility methods may be called directly when appropriate. A static method that secretly locates a managed dependency, mutates shared runtime state, or bypasses its DI owner remains prohibited **because of its behavior**, not because the syntax is static. Typed declarations such as `AchievementProgressEventData progressEventData` are also entirely valid; they do not create an object.

### Construction exceptions

- **Value/data owners:** record compact/canonical constructors and genuine value conversion/factory methods may use `new` internally to create complete immutable results.
- **Actual Builders and factories:** meaningful DataBuilder/MetaDataBuilder, parsing, serialization, and construction adapters may create the object they own. Do not add ceremonial Builders merely to remove a single `new` from a consumer.
- **DI infrastructure and composition boundaries:** bootstrap, providers, lifecycle setup and tool-governed managed constructor bridges may construct and register their declared instances according to Tavall DI policy.
- **Explicitly permitted lightweight objects:** local standard-library structures, exceptions, immutable utilities and other short-lived nonmanaged objects may be instantiated in ordinary methods when construction is incidental, has no domain ownership implications, and no Tavall tool contract says otherwise.
- **Tests and generated/framework code:** fixtures, mocks, code generators and low-level adapters follow their own verified creation contracts.

The review question is **who owns this instance and its lifecycle?** If the class is Tavall DI-managed, resolve it through DI. If it is a domain data object, favor its actual value owner or purposeful Builder. If `new` is an essential local Java construct with no competing owner, the exception may apply. Never create an extra class solely to satisfy this rule.

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

This collapses event creation, durable mutation, result validation and cache reconciliation into one consumer call. The problem is crossing **operation ownership boundaries**, not that the static value factory is syntactically static. When the caller already has a completed `AchievementProgressMutationResult`, use `progressMutationResult.updatedProgress()` directly and do not invoke the event mutation a second time. See the [full update consumer example](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md#multi-dependency-expanded-access).

Bad forwarding wrapper:

```java
public void updatePlayerAchievementProgress(
        PlayerAchievementProgressData playerAchievementProgressData
) {
    getPlayerAchievementDataHandler().updatePlayerAchievementProgress(
            playerAchievementProgressData
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
