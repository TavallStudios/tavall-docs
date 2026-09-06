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

### Class Naming Rules

* Use names that identify both the domain subject and the class role.
* Preserve established acronym capitalization, such as `UUID`, `UI`, `HTTP`, `JSON`, and `Redis`.
* Match interface and implementation names where practical: `ITimerResolver` and `TimerResolver`.
* Suffixes are contracts. A `Repository` persists, a `Cache` caches, a `Resolver` derives, and a `Renderer` renders.
* Platform names appear only when the class owns that platform boundary, such as `PaperWorldSnapshotGateway` or `VelocityServerRoutingHandler`.
* Reusable domain, request, result, state, definition, and metadata types remain top-level classes or records.
* Do not rename a class merely to follow fashion. Rename when responsibility becomes materially clearer.

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

#### Service Classes

Handlers are the default behavior classes for Project Novus game systems.

Most game behavior is handling input, data, state, commands, events, GUI actions, or player actions.

That means handlers are usually better than service classes.

Only use service classes for actual long-running services, like a match-making service.

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

#### Meta Data Handler Classes

Metadata handler classes resolve, refresh, or expose metadata.

Examples:

```text
PlayerRankMetaDataHandler
ChatFormatMetaDataHandler
TabFormatMetaDataHandler
```

They should not save primary data unless explicitly designed to.

#### Builder Classes

Builder classes create objects.

They should not save objects, cache objects, or run permission checks.

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
