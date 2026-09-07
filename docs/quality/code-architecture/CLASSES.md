# Project Novus Class Roles

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Classes

### Class Rules

Classes should have one clear job.

A class should either:

* Hold data.
* Build data.
* Handle input.
* Coordinate behavior.
* Talk to storage.
* Provide shared utility behavior.

Do not mix all of those together because then we have invented `EverythingManager`, and civilization loses again.

Rules:

* Avoid vague class names like `Manager`, `Helper`, `Common`, or `Misc`.
* Prefer clear names based on the class role.
* Keep data classes separate from behavior classes.
* Keep metadata classes separate from normal data classes.
* Inner classes should be avoided unless they improve clarity.
* Services should own reusable system behavior, not event-specific routing.
* Handlers should receive input and delegate work.
* Builders should create objects, not save them.
* Database classes should only handle persistence.
* Cache classes should only handle cached state.

##### Why

A class name and role should predict what the class is allowed to own. When storage, presentation, validation, routing, lifecycle, and data construction accumulate in one type, callers can no longer tell where a rule belongs or which lifecycle owns the state.

Role boundaries keep changes local, make dependency graphs reviewable, and let tests target one responsibility instead of recreating half the runtime just to exercise one method.

### Class Naming Rules

* Use names that identify both the domain subject and the class role.
* Preserve established acronym capitalization, such as `UUID`, `UI`, `HTTP`, `JSON`, and `Redis`.
* Match interface and implementation names where practical: `ITimerResolver` and `TimerResolver`.
* Suffixes are contracts. A `Repository` persists, a `Cache` caches, a `Resolver` derives, and a `Renderer` renders.
* Platform names appear only when the class owns that platform boundary, such as `PaperWorldSnapshotGateway` or `VelocityServerRoutingHandler`.
* Reusable domain, request, result, state, definition, and metadata types remain top-level classes or records.
* Do not rename a class merely to follow fashion. Rename when responsibility becomes materially clearer.

##### Why

Precise names make ownership visible before a file is opened. That matters in a large codebase where several systems may all contain a handler, cache, registry, or resolver for different subjects.

Treating suffixes as contracts also gives architecture tests and reviewers a useful signal: a class called `Cache` that performs durable persistence or a class called `Builder` that resolves services is immediately suspicious instead of merely unconventional.

### Inner Classes

Avoid inner classes when they reduce clarity.

Inner classes are only acceptable when the class is small, private to the parent, and has no value outside that parent.

Do not use inner classes for domain data, metadata, services, handlers, builders, or anything likely to be reused.

#### Example

Bad:

```java
public final class PlayerAccountService {

    private static final class RankData {

        private final RankKey rankKey;

        private RankData(RankKey rankKey) {
            this.rankKey = rankKey;
        }
    }
}
```

Good:

```java
public final class PlayerRankData {

    private final RankKey rankKey;

    public PlayerRankData(RankKey rankKey) {
        this.rankKey = rankKey;
    }

    public RankKey getRankKey() {
        return rankKey;
    }
}
```

The good version is easier to find, test, reuse, and document.

##### Why

A reusable domain concept hidden inside another class inherits the parent's discoverability and lifecycle whether that relationship is real or not.

Top-level types make the contract searchable, independently testable, and reusable without forcing callers to depend on an unrelated parent class. Inner classes remain useful only when the concept truly has no identity outside the parent implementation.

### Behaviour Classes

Behavior classes do work.

They should act on data objects, metadata objects, repositories, services, handlers, builders, or caches.

They should not pretend to be data containers.

#### Behavior Class Data Flow

Player account rank load flow:

```text
Database
  -> PlayerAccountDataHandler
  -> PlayerAccountDataBuilder
  -> PlayerAccountData
  -> PlayerRankMetaDataBuilder
  -> PlayerRankMetaData
  -> PlayerRankMetaDataHandler
  -> PlayerAccountService
  -> PlayerJoinHandler / RankCommandHandler / TabHandler
```

Example:

```text
player_account.rank_key
  -> loaded from database
  -> converted into PlayerAccountData
  -> converted into PlayerRankMetaData
  -> cached in the player account service
  -> used by chat, tab, permissions, and staff tools
```

Write/update flow:

```text
RankCommandHandler
  -> PlayerAccountService
  -> PlayerAccountDataHandler
  -> Database
  -> Cache
  -> TabHandler / ChatHandler refresh
```

Example:

```text
Admin changes player rank
  -> command handler receives request
  -> service validates permission and power level
  -> data handler saves new rank
  -> cache updates player account data
  -> tab and chat visuals refresh
```

##### Why

Explicit data flow prevents behavior classes from becoming accidental authorities for data they only consume. Storage, derived metadata, cache state, and presentation each have different invalidation and lifecycle rules.

When those phases stay visible, failures and refreshes can be handled at the boundary that owns them instead of being hidden inside a convenient all-purpose object.

#### Service Classes

Handlers are the default behavior classes for Project Novus game systems.

Most game behavior is handling input, data, state, commands, events, GUI actions, or player actions.

That means handlers are usually better than service classes.

Only use service classes for actual long-running services, like a match-making service.

##### Why

`Service` should communicate a cohesive, reusable capability with a meaningful lifetime, not simply mean “class that contains logic.”

Keeping handlers as the default makes input ownership and operation boundaries visible. Reserving services for durable capabilities stops the codebase from filling with generic services whose actual responsibility must be rediscovered from their methods.

#### Handler Classes

Handler classes receive input and delegate behavior.

Examples:

```text
PlayerJoinHandler
RankCommandHandler
ChatMessageHandler
PunishmentCommandHandler
```

Handlers should not contain core rules.

Bad:

```java
if (staffPower > targetPower) {
    target.setRank(newRank);
}
```

Good:

```java
boolean canRankEdit = powerLevelService.canRankEdit(staffProfile, targetProfile);

if (!canRankEdit) {
    return CommandResult.targetTooPowerful();
}

rankService.setRank(targetProfile, newRank);
```

##### Why

Handlers sit close to input surfaces, so putting reusable domain rules directly in them duplicates those rules as soon as another command, event, web endpoint, or Discord surface needs the same behavior.

Delegating the rule keeps the handler focused on the operation while the domain owner remains reusable and testable independently of the input source.

#### Data Handler Classes

Data handler classes move normal data between storage and the codebase.

Examples:

```text
PlayerAccountDataHandler
PunishmentDataHandler
RankDataHandler
```

They should load, save, update, and delete data.

They should not run gameplay rules.

##### Why

Data access has consistency, mapping, cache, retry, and persistence concerns that should behave the same regardless of who requested the data.

Keeping gameplay rules out prevents persistence mechanics from becoming a hidden policy layer and lets data handlers evolve storage behavior without changing the domain decision that caused the read or write.

#### Meta Data Classes

Metadata classes hold derived or display-ready information.

Metadata is usually built from normal data.

Example:

```text
PlayerAccountData
  -> PlayerRankMetaData
```

`PlayerAccountData` may store:

```text
uuid
name
rankKey
powerLevel
```

`PlayerRankMetaData` may expose:

```text
rank display name
rank color
tab format
chat format
power level
```

##### Why

Derived values often have different refresh and presentation lifetimes than the source data they come from.

Separating metadata from primary data keeps persisted truth small and stable while allowing display-ready or resolved values to be rebuilt when definitions, formats, or presentation rules change.

#### Meta Data Handler Classes

Metadata handler classes resolve, refresh, or expose metadata.

Examples:

```text
PlayerRankMetaDataHandler
ChatFormatMetaDataHandler
TabFormatMetaDataHandler
```

They should not save primary data unless explicitly designed to.

##### Why

Metadata derivation is behavior, while primary persistence belongs to the data owner. Combining the two means a display refresh can unexpectedly become a durable mutation path.

A dedicated metadata handler gives derivation, refresh, fallback, and invalidation one place to live without granting presentation-oriented code authority over source data.

#### Builder Classes

Builder classes create objects.

They should not save objects, cache objects, or run permission checks.

##### Why

Construction should be deterministic from the inputs supplied to the builder. Once a builder resolves services, performs I/O, or mutates runtime state, object creation becomes a hidden workflow with lifecycle and failure behavior callers cannot see from the build call.

Keeping builders construction-only makes them safe to reuse in persistence, tests, handlers, and migrations without accidentally triggering unrelated system behavior.

##### Data Builder Classes

Data builders create data objects from raw input.

Example:

```java
UUID playerUUID = resultSet.getObject("uuid", UUID.class);
String playerName = resultSet.getString("name");
RankKey rankKey = RankKey.valueOf(resultSet.getString("rank_key"));

PlayerAccountData playerAccountData = playerAccountDataBuilder.build(
    playerUUID,
    playerName,
    rankKey
);
```

##### Meta Data Builder Classes

Metadata builders create metadata from normal data.

Example:

```java
RankKey rankKey = playerAccountData.getRankKey();
RankDefinition rankDefinition = rankRegistry.get(rankKey);

PlayerRankMetaData rankMetaData = playerRankMetaDataBuilder.build(
    playerAccountData,
    rankDefinition
);
```

#### Behavior Interfaces

Behavior interfaces should describe a usable contract.

Prefer interface names that match the concrete class with an `I` prefix.

Examples:

```text
IPowerLevelService -> PowerLevelService
IRankService -> RankService
IPlayerAccountDataHandler -> PlayerAccountDataHandler
```

Use interfaces for dependency-injected behavior.

Do not create interfaces for tiny data objects just to worship abstraction like it owes us money.

##### Why

Behavior interfaces are useful when callers depend on a stable capability rather than a particular implementation. That supports DI replacement, platform substitution, and focused test doubles.

Data objects already are their contract. Giving every passive value an interface creates another type without adding a substitution boundary, which increases navigation cost while contributing approximately nothing to architecture.

### Static Classes

Static classes should be rare.

Use static classes only for focused, stateless utility behavior.

Good:

```text
ChatColorUtil
UUIDUtil
TimeFormatUtil
```

Bad:

```text
PlayerUtil
ServerUtil
CommonUtil
MiscUtil
```

Static classes should not hold mutable system state.

##### Why

Static mutable state has process lifetime and global reach whether callers intended that ownership or not. It bypasses DI replacement, module-generation cleanup, and explicit lifecycle boundaries.

Restricting static classes to pure helpers keeps static syntax useful without turning it into an invisible registry, cache, or service locator.

### Data Object Classes

Data object classes hold normal persisted or runtime data.

They should not contain business behavior.

Examples:

```text
PlayerAccountData
PunishmentData
RankData
PermissionNodeData
```

Data objects may contain small validation or getters, but should not talk to services, databases, commands, or caches.

##### Why

A data object should remain understandable as a value. If reading or mutating it can perform I/O, access runtime services, or trigger commands, passing the value across a boundary also passes hidden behavior and failure modes.

Keeping data passive makes serialization, persistence mapping, snapshots, testing, and migration predictable.

### Meta Data Object Classes

Metadata object classes hold derived, resolved, or display-ready data.

Examples:

```text
PlayerRankMetaData
ChatFormatMetaData
TabFormatMetaData
PermissionMetaData
```

Metadata objects should be easy to rebuild from source data.

##### Why

Derived metadata is disposable by design. Treating it as easy-to-rebuild state prevents presentation or resolution artifacts from quietly becoming a second source of truth.

That makes invalidation straightforward when source data or definitions change and keeps durable authority with the underlying data model.

### Utility Classes

Utility classes provide focused stateless helpers.

Examples:

```text
LegacyColorUtil
UUIDUtil
DurationFormatUtil
```

Utility classes should be final and have a private constructor.

```java
public final class LegacyColorUtil {

    private LegacyColorUtil() {
    }
}
```

Do not create god utility classes.

##### Why

A utility is useful precisely because its behavior has no independent runtime ownership. Broad utility buckets erase that property by accumulating unrelated domain and platform behavior behind convenient static calls.

Focused utilities remain easy to test and reuse; broad utilities become dependency systems with worse names and no lifecycle controls.

### Orchestration Classes

Orchestration classes coordinate multiple services.

They are useful when one flow touches several systems.

Examples:

```text
PlayerLoginOrchestrator
RankUpdateOrchestrator
PunishmentOrchestrator
```

Example flow:

```text
RankUpdateOrchestrator
  -> PowerLevelService
  -> RankService
  -> PlayerAccountService
  -> TabHandler
  -> ChatFormatMetaDataHandler
```

Orchestrators should coordinate.

They should not become dumping grounds for every rule ever written.

##### Why

Ordering across several focused collaborators is real behavior and deserves one explicit owner. Without an orchestrator, the sequence tends to be copied into commands, listeners, schedulers, or controllers until each surface performs a slightly different workflow.

The orchestrator owns sequencing and operation lifecycle while each collaborator retains its own rules and state. That makes the workflow testable without converting the orchestrator into another god class.

### Service Classes

Service classes own core reusable behavior.

Examples:

```text
PowerLevelService
RankService
PermissionService
PlayerAccountService
```

Services may use:

```text
Data handlers
Metadata handlers
Registries
Caches
Other services
```

Services should not directly parse commands or listen to Paper events.

##### Why

A service should be reusable independently of the transport or platform surface that invoked it. Command parsing and Paper event adaptation are platform/input concerns that change for different reasons than the underlying domain capability.

Keeping those edges outside the service lets the same capability serve game, web, Discord, tests, or future surfaces without importing each surface's event model.

### Database Classes

Database classes own persistence access.

They should know how to read and write data.

They should not know gameplay rules.

Examples:

```text
PlayerAccountDatabase
PunishmentDatabase
RankDatabase
```

##### Why

Persistence code already owns database-specific failure, mapping, transaction, and query concerns. Giving it gameplay authority couples business decisions to one storage implementation and makes those decisions difficult to reuse or test without the database.

Database boundaries should answer storage questions; handlers and services should decide what the application is allowed to do.

### Cache Classes

Cache classes own temporary fast-access state.

They should never be treated as the permanent source of truth unless the system explicitly says so.

Examples:

```text
PlayerAccountCache
RankMetaDataCache
PermissionCache
```

Cache flow:

```text
Database
  -> Data Handler
  -> Cache
  -> Service
```

##### Why

A cache is disposable optimization state. Treating it as durable truth changes failure and recovery semantics: eviction, restart, expiration, or invalidation suddenly becomes data loss.

Keeping authority elsewhere lets cache entries be rebuilt safely and gives TTL, invalidation, and cleanup behavior one explicit owner.