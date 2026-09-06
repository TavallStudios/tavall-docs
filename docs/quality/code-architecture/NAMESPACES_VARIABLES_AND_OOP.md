# Project Novus Namespaces, Variables, OOP, DRY, and Type Safety

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Code Design & Principles

This section lays out the general code design and principles we'll use here in Project Novus.

Examples use Project Novus account, rank, permission, chat, timer, building, resource, and platform concepts where practical. A small number of generic moderation examples remain because they demonstrate authority, request, result, repository, and delegation boundaries without defining a production moderation system.

### Namespaces

* **Package names**: Domain + purpose > short and vague
    * **Example**: `org.tavall.api.minecraft.backend.message.format.placeholder` > `org.tavall.api.minecraft.backend.message`
    * **Example**: `org.tavall.api.minecraft.backend.rank.permission.power` > `org.tavall.api.minecraft.backend.rank.permission`
    * **Example**: `org.tavall.api.minecraft.backend.account.data.handler` > `org.tavall.api.minecraft.backend.account`
    * **Why**: Packages should make it obvious what system the code belongs to and what layer it lives in. Short packages look clean for about five minutes, then every class becomes a scavenger hunt.

* **Package names should follow system ownership**
    * Chat system code should live under chat packages.
    * Rank and permission code should live under permission/rank packages.
    * Player profile code should live under profile packages.
    * Punishment code should live under punishment packages.
    * UI/menu code should live under UI/menu packages.
    * Shared utilities should only go into shared utility packages when they are truly shared.

* **Avoid vague package buckets**
    * Bad:
        * `org.tavall.backend.core.manager`
        * `org.tavall.backend.core.util`
        * `org.tavall.backend.core.common`
        * `org.tavall.backend.core.misc`
    * Good:
        * `org.tavall.api.minecraft.backend.message.format`
        * `org.tavall.api.minecraft.backend.message.placeholder`
        * `org.tavall.api.minecraft.backend.rank.permission.power`
        * `org.tavall.api.minecraft.backend.account.data`
        * `org.tavall.backend.audit.history`

* **Class names**: Precise > short
    * **Example**: `PlayerRankMetaDataHandler` > `RankHandler`
    * **Example**: `ChatFormatPlaceholderResolver` > `PlaceholderResolver`
    * **Example**: `StaffPowerLevelHandler` > `PowerHandler`
    * **Example**: `PlayerAccountDataBuilder` > `AccountBuilder`
    * **Example**: `PlayerRankMetaDataBuilder` > `MetaBuilder`
    * **Example**: `PunishmentRecordDataBuilder` > `DataBuilder`
    * **Why**: This project has overlapping systems. A rank can appear in chat, tab, permissions, profile data, staff tools, and punishments. Precision prevents confusion.

* **Class names should describe the exact role**
    * `Handler` classes receive input, coordinate behavior, and delegate work.
    * `DataHandler` classes move data between storage and the codebase.
    * `Builder` classes construct objects.
    * `DataBuilder` classes construct normal data objects.
    * `MetaDataBuilder` classes construct resolved/display-ready metadata objects.
    * `MetaData` classes hold resolved/display-ready information.
    * `Database` classes talk to persistence.
    * `Cache` classes own temporary cached state.
    * `Service` classes should only exist for actual long-standing services.
    * `Util` classes must be focused, stateless, and rare.

* **Service classes should be rare**
    * Most game logic should be handled through handlers, not services.
    * A service should represent something long-standing, lifecycle-owned, or continuously available.
    * Do not name normal game behavior as a service just because it sounds official.

* **Avoid names that hide responsibility**
    * Bad:
        * `RankManager`
        * `PlayerHelper`
        * `ChatUtil`
        * `CoreService`
        * `DataManager`
        * `MetaBuilder`
        * `DataBuilder`
    * Good:
        * `RankHandler`
        * `PlayerAccountDataHandler`
        * `ChatFormatHandler`
        * `LegacyColorUtil`
        * `PlayerAccountCache`
        * `PlayerAccountDataBuilder`
        * `PlayerRankMetaDataBuilder`

* **Rule**
    * Package names should tell us where the class belongs.
    * Class names should tell us what the class actually does.
    * Handler classes are the default for game behavior.
    * Service classes are only for real long-standing services.
    * Data builders should say what data they build.
    * Metadata builders should say what metadata they build.
    * Clean is good, but clear wins.

### Variables & Constants

### Local Variables

Important values should be extracted into named local variables before they are passed into nested calls. Locals make ownership, debugging, breakpoints, and stack traces readable.

* Example bad variable usage
```java
SomeClass localVar;
someMethod(localVar.getSomething());
```
* Example good variable usage

```java 
SomeClass localVar;
SomeObject localObject = localVar.getSomething()
someMethod(localObject);
```

#### Naming Local Variables

* Names describe the value's domain meaning, not merely its Java type.
* Preserve established acronym capitalization, such as `playerUUID`, `nativeUI`, `httpRequest`, and `jsonPayload`.
* Avoid numbered locals unless the number is part of the domain.
* Avoid one-letter names except conventional tiny scopes such as a mathematical coordinate or short lambda.
* Do not reuse one local for several meanings.

Example bad:
```java
UUID playerUuid = player.getUniqueId();
```

Example good:
```java
UUID playerUUID = player.getUniqueId();
```

### Global Variables

Class fields represent owned state or injected dependencies.

* Fields are `private` unless a framework requires another visibility.
* Dependencies and immutable state are `final`.
* Mutable state has one clear owner and documented concurrency behavior.
* Public mutable static state is prohibited.
* Static state must not become a hidden dependency graph, cache, registry, or service locator.
* Shared runtime state belongs in a typed registry, cache, repository, or runtime handler.
* Field names describe the subject, not merely the type.

### Constants

Create constants for stable values that are truly code-owned.

* Use `UPPER_SNAKE_CASE`.
* Prefer typed keys, enums, and definitions over collections of raw string constants.
* Values operators must tune belong in configuration or a persisted definition, not hard-coded constants.
* Do not create a constant merely to avoid writing a clear literal once.
* Time values include their unit in the name or use `Duration`.
* Permission, message, resource, registry, and configuration keys have one owning typed definition.
* Never place secrets, credentials, protected tokens, or environment-specific endpoints in constants.

### OOP, DRY, Type-Safety, & Abstractions

### OOP

We are doing proper OOP in this codebase.

Classes should have clear ownership, clear responsibility, and meaningful behavior. Objects should represent real concepts in the system, not random bags of static methods wearing a trench coat.

#### Bad OOP

```java
public class PlayerUtils {

    public static boolean canBan(Player staff, Player target) {
        return getPower(staff) > getPower(target);
    }

    public static int getPower(Player player) {
        return 100;
    }
}
```

##### Why

This hides real domain logic inside a vague utility class. The class has no ownership, no state, no clear responsibility, and no real connection to the permission system. It also makes future changes harder because punishment rules, rank rules, and player authority rules can get scattered everywhere.

#### Good OOP

```java
public final class PermissionProfile { // This class can also probably be a record

    private final UUID playerUUID;
    private final int powerLevel;

    public PermissionProfile(UUID playerUUID, int powerLevel) {
        this.playerUUID = playerUUID;
        this.powerLevel = powerLevel;
    }
}
```

##### Why

This gives the permission data a real object with real behavior. We can later call 'PermissionProfile' and it will have all the data objects related to the player profile, instead of having them scattered around the code base. The code becomes easier to read, test, and reuse.

### DRY

DRY means shared rules should live in one place.

It does **not** mean every similar-looking line of code needs to be abstracted.

Do not force DRY when two systems only look similar but may change for different reasons.

#### Bad DRY

```java
public final class BanCommand {

    public void execute(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        if (staffProfile.powerLevel() <= targetProfile.powerLevel()) {
            throw new IllegalStateException("You cannot punish this player.");
        }

        // ban player
    }
}
```

```java
public final class MuteCommand {

    public void execute(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        if (staffProfile.powerLevel() <= targetProfile.powerLevel()) {
            throw new IllegalStateException("You cannot punish this player.");
        }

        // mute player
    }
}
```
**We SHOULD NOT make this code DRY.**

##### Why

The same punishment authority rule is duplicated in multiple commands.

If the rule changes, every command has to be updated. One will be missed. Then production gets spicy for no reason.

#### Good DRY

```java
public final class PermissionService {

    public boolean canPunish(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        return staffProfile.powerLevel() > targetProfile.powerLevel();
    }
}
```

```java
public final class BanCommand {

    private final PermissionService permissionHandler;

    public BanCommand(PermissionService permissionHandler) {
        this.permissionHandler = permissionHandler;
    }

    public void execute(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        if (!permissionHandler.canPunish(staffProfile, targetProfile)) {
            throw new IllegalStateException("You cannot punish this player.");
        }

        // ban player
    }
}
```

```java
public final class MuteCommand {

    private final PermissionService permissionHandler;

    public MuteCommand(PermissionService permissionHandler) {
        this.permissionHandler = permissionHandler;
    }

    public void execute(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        if (!permissionHandler.canPunish(staffProfile, targetProfile)) {
            throw new IllegalStateException("You cannot punish this player.");
        }

        // mute player
    }
}
```

##### Why

The authority rule now lives in one place. Commands use the rule, but they do not own it.

This is proper DRY.

#### Bad DRY: Forced Abstraction

```java
public final class CommandMessageHelper {

    public String buildActionMessage(String actor, String target, String action) {
        return actor + " used " + action + " on " + target + ".";
    }
}
```

```java
String banMessage = commandMessageHelper.buildActionMessage(
    staffName,
    targetName,
    "ban"
);

String muteMessage = commandMessageHelper.buildActionMessage(
    staffName,
    targetName,
    "mute"
);
```

##### Why

These messages only look similar right now.

Ban messages may later need duration, appeal info, IP data, or broadcast rules. Mute messages may need expiration info, chat-channel rules, or silent moderation behavior.

Forcing them into one helper creates fake reuse. Fake reuse is just duplication with extra steps and worse stack traces.

#### Good Duplication: Different Rules, Different Code

```java
String banMessage = messageResolver.resolve(
    PunishmentMessageKey.BAN_APPLIED,
    placeholders
);
```

```java
String muteMessage = messageResolver.resolve(
    PunishmentMessageKey.MUTE_APPLIED,
    placeholders
);
```

##### Why

Both messages use the same message system, but each punishment keeps its own message key.

This avoids hardcoding while still allowing ban and mute messages to evolve separately.

A little duplication is better than the wrong abstraction. The wrong abstraction is how a five-line problem becomes a framework nobody asked for.

### Type-Safety

Prefer typed keys, enums, IDs, and domain objects over raw strings and magic numbers.

#### Bad Type-Safety

```java
messageResolver.resolve("chat.player.format");
```

##### Why

Raw strings are easy to mistype, hard to refactor, and impossible for the compiler to protect. If the config key changes, this can silently break at runtime, because apparently bugs enjoy waiting until production to introduce themselves.

#### Good Type-Safety

```java
messageResolver.resolve(ChatMessageKey.PLAYER_FORMAT);
```

##### Why

The compiler can track this. Refactors are safer, usage is easier to find, and the key has a single source of truth. This makes message resolution predictable instead of string-based guesswork.

#### Bad Permission Check

```java
permissionHandler.has(player, "punishment.ban");
```

##### Why

The permission node is just a loose string. A typo like `"punishment.bna"` can compile perfectly and fail silently. This is how codebases become archaeological dig sites.

#### Good Permission Check

```java
permissionHandler.has(player, PermissionNode.PUNISHMENT_BAN);
```

##### Why

The permission node is type-safe, searchable, reusable, and harder to mess up. The code clearly says what permission is being checked without relying on fragile raw strings.
