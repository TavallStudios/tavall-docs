# Project Novus Validation, Fallbacks, and Anti-Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

### Validation Pattern

Validation should happen before mutation.

Validation should be readable and typed.

#### Bad Validation Pattern

```java
public void updateRank(String rankName) {
    if (rankName != null) {
        database.update(rankName);
    }
}
```

##### Why

The validation is weak.

The rank is a raw string.

The method still allows bad values to slip through.

#### Good Validation Pattern

```java
public CommandResult updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
    RankKey rankKey = rankUpdateRequest.getRankKey();
    boolean rankExists = rankRegistry.containsRank(rankKey);

    if (!rankExists) {
        return CommandResult.invalidRank();
    }

    playerRankDataHandler.updatePlayerRankData(rankUpdateRequest);

    return CommandResult.success();
}
```

##### Why

The validation uses a typed rank key.

The failure result is explicit.

The mutation only happens after validation passes.

### Fallback Pattern

Fallbacks prevent missing data from crashing player-facing systems.

Fallbacks should be intentional and visible in code.

#### Bad Fallback Pattern

```java
String rankName = playerRankMetaData.getDisplayName();
player.sendMessage(rankName);
```

##### Why

If metadata is missing, this can throw or send bad output.

Player-facing systems need safe fallback behavior.

#### Good Fallback Pattern

```java
public String resolveRankDisplayName(PlayerRankMetaData playerRankMetaData) {
    if (playerRankMetaData == null) {
        return "Subject";
    }

    String displayName = playerRankMetaData.getDisplayName();

    if (displayName == null) {
        return "Subject";
    }

    return displayName;
}
```

##### Why

The fallback is clear.

The player still receives safe output.

The system fails softly instead of making the console scream.

### Anti-Patterns

Anti-patterns are patterns we do not want in this codebase.

These usually make ownership unclear, testing harder, and future changes worse.

#### God Class Pattern

Bad:

```java
public final class ProjectCoreManager {
}
```

##### Why

A god class owns too much.

If one class controls chat, ranks, profiles, punishments, cache, database, and commands, then every change touches the same monster.

Split by system and role.

#### Manager Pattern

Bad:

```java
public final class RankManager {
}
```

##### Why

`Manager` does not describe what the class actually does.

Use a role name.

Good:

```text
RankUpdateHandler
RankRegistry
RankDataHandler
PlayerRankMetaDataBuilder
```

#### Helper Pattern

Bad:

```java
public final class PlayerHelper {
}
```

##### Why

`Helper` is vague.

It usually becomes a junk drawer for unrelated methods.

Use focused class names instead.

#### Static Dependency Access Pattern

Static syntax is not the problem. Static ownership of runtime behavior is.

Tavall-managed application dependencies must resolve through the owning DI map. Do not hide a service, repository, registry, cache, gateway, scheduler, runtime, or other managed dependency behind a static method.

Bad:

```java
public final class EconomyAccess {

    public static IEconomyService getEconomyService() {
        return DependencyLoaderAccess.findInstance(IEconomyService.class);
    }
}
```

```java
EconomyAccess.getEconomyService().credit(playerUUID, amount);
```

##### Why

The call site no longer declares that it needs economy behavior.

The static method becomes a service locator, bypasses the owning dependency-access surface, and makes replacement, reload, lifecycle ownership, and tests less trustworthy.

Use the normal `DependencyAccess` path, including focused default access methods where they make repeated calls easier to read.

The Minecraft-CTF `MessageAccess` pattern is a useful reference: default instance methods expose DI-managed behavior, while a private static helper is limited to pure fallback-value construction.

Reference: [Minecraft-CTF `MessageAccess`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/config/message/interfaces/MessageAccess.java)

Allowed static calls are intentionally narrow:

- Compile-time constants and immutable constant values.
- Enum or value-object parsing and conversion such as `fromKey(...)`, when the result depends only on explicit inputs.
- Pure normalization, formatting, or transformation functions with no hidden runtime dependency.
- Static factory or builder entry points such as `builder()`, `of(...)`, `from(...)`, or `create(...)` when they only construct or configure the returned value.
- Private static helpers that are pure implementation details and depend only on their arguments.
- Third-party static helpers only when they are equivalently pure and stateless.

A static builder or factory is construction syntax, not a composition root. It must not resolve DI, perform persistence or network I/O, access server or plugin runtime state, schedule work, mutate global state, or smuggle managed dependencies into the returned object.

Runtime utility behavior should normally remain an injected instance dependency and may be exposed through focused default access methods. Calls such as sounds, messages, effects, scheduling, persistence, cache access, and other platform/runtime behavior do not become valid static calls merely because a utility class could technically hold them.

When behavior needs replacement, lifecycle ownership, runtime configuration, deterministic testing, or access to Tavall-managed state, route it through DI.

#### Raw String Pattern

Bad:

```java
permissionHandler.has(player, "punishment.ban");
```

Good:

```java
PermissionNode permissionNode = PermissionNode.PUNISHMENT_BAN;

boolean hasPermission = permissionHandler.has(
    player,
    permissionNode
);
```

##### Why

Typed keys are safer, searchable, and refactorable.

Raw strings are tiny runtime landmines.

#### Hidden Side Effect Pattern

Bad:

```java
public PlayerAccountData getPlayerAccountData(UUID playerUUID) {
    PlayerAccountData playerAccountData = database.load(playerUUID);

    cache.put(playerUUID, playerAccountData);
    tabHandler.refresh(playerUUID);

    return playerAccountData;
}
```

##### Why

A method named `getPlayerAccountData` should not secretly mutate cache and refresh tab state.

The method name lies.

Code should not lie. Humans already overachieved there.

Good:

```java
public PlayerAccountData loadPlayerAccountData(UUID playerUUID) {
    PlayerAccountData playerAccountData = playerAccountDataHandler.loadPlayerAccountData(
        playerUUID
    );

    return playerAccountData;
}

public void refreshPlayerAccountData(UUID playerUUID) {
    PlayerAccountData playerAccountData = loadPlayerAccountData(playerUUID);

    playerAccountCache.putPlayerAccountData(
        playerUUID,
        playerAccountData
    );
}
```

##### Why

Loading and refreshing are separate actions.

The method names match what happens.
