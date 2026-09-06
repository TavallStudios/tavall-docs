# Project Novus Requests, Results, Resolvers, and Formatters

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

### Request Object Pattern

Request objects group related input for a behavior.

Use request objects when a method needs several related values.

#### Bad Request Object Pattern

```java
public CommandResult updateRank(
    UUID staffUUID,
    UUID targetUUID,
    RankKey rankKey,
    String reason,
    boolean silent
) {
    return CommandResult.success();
}
```

##### Why

The method has too many related parameters.

Callers can pass values in the wrong order.

Adding another value makes the method worse.

This is how method signatures become centipedes.

#### Good Request Object Pattern

```java
public final class RankUpdateRequest {

    private final UUID staffUUID;
    private final UUID targetUUID;
    private final RankKey rankKey;
    private final String reason;
    private final boolean silent;

    public RankUpdateRequest(
        UUID staffUUID,
        UUID targetUUID,
        RankKey rankKey,
        String reason,
        boolean silent
    ) {
        this.staffUUID = staffUUID;
        this.targetUUID = targetUUID;
        this.rankKey = rankKey;
        this.reason = reason;
        this.silent = silent;
    }

    public UUID getStaffUUID() {
        return staffUUID;
    }

    public UUID getTargetUUID() {
        return targetUUID;
    }

    public RankKey getRankKey() {
        return rankKey;
    }

    public String getReason() {
        return reason;
    }

    public boolean isSilent() {
        return silent;
    }
}
```

```java
public CommandResult updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
    UUID staffUUID = rankUpdateRequest.getStaffUUID();
    UUID targetUUID = rankUpdateRequest.getTargetUUID();

    return CommandResult.success();
}
```

##### Why

The request object gives the input a real shape.

The method receives one meaningful object instead of a pile of loose values.

### Result Object Pattern

Result objects describe what happened.

Use result objects when behavior can succeed, fail, or return a reason.

#### Bad Result Object Pattern

```java
public boolean updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
    return false;
}
```

##### Why

`false` tells us nothing.

Was permission denied?

Was the target too powerful?

Was the rank missing?

Did the database fail?

Nobody knows. The boolean sits there smugly contributing nothing.

#### Good Result Object Pattern

```java
public final class CommandResult {

    private final boolean success;
    private final CommandFailureReason failureReason;

    private CommandResult(
        boolean success,
        CommandFailureReason failureReason
    ) {
        this.success = success;
        this.failureReason = failureReason;
    }

    public static CommandResult success() {
        CommandResult commandResult = new CommandResult(
            true,
            null
        );

        return commandResult;
    }

    public static CommandResult targetTooPowerful() {
        CommandResult commandResult = new CommandResult(
            false,
            CommandFailureReason.TARGET_TOO_POWERFUL
        );

        return commandResult;
    }

    public boolean isSuccess() {
        return success;
    }

    public CommandFailureReason getFailureReason() {
        return failureReason;
    }
}
```

##### Why

The result object explains the outcome.

Callers can respond correctly without guessing.

### Resolver Pattern

Resolvers turn a key or placeholder into a resolved value.

Examples:

* Message resolver
* Placeholder resolver
* Rank display resolver
* Format resolver

#### Bad Resolver Pattern

```java
String message = config.getString("chat.player.format");
```

##### Why

The key is a raw string.

The caller knows too much about config structure.

There is no central fallback behavior.

#### Good Resolver Pattern

```java
public final class ChatFormatResolver {

    private final ChatFormatRegistry chatFormatRegistry;

    public String resolveChatFormat(ChatMessageFormatKey chatMessageFormatKey) {
        ChatFormatDefinition chatFormatDefinition = chatFormatRegistry.getChatFormatDefinition(
            chatMessageFormatKey
        );

        String formatValue = chatFormatDefinition.getFormatValue();

        return formatValue;
    }
}
```

##### Why

The caller uses a typed key.

The resolver owns lookup behavior.

Fallbacks can live in one place instead of being copied into every caller.

### Formatter Pattern

Formatters turn already-known data into display text.

Formatters should not load data, save data, or run permission checks.

#### Bad Formatter Pattern

```java
public final class RankFormatter {

    public String format(UUID playerUUID) {
        PlayerAccountData playerAccountData = playerAccountDataHandler.loadPlayerAccountData(
            playerUUID
        );

        RankKey rankKey = playerAccountData.getRankKey();

        return rankKey.name();
    }
}
```

##### Why

The formatter is loading data.

That makes it secretly a handler.

Formatters should format values they are given.

#### Good Formatter Pattern

```java
public final class PlayerRankFormatter {

    public String formatPlayerRank(PlayerRankMetaData playerRankMetaData) {
        String legacyColor = playerRankMetaData.getLegacyColor();
        String displayName = playerRankMetaData.getDisplayName();

        String formattedRank = legacyColor + displayName;

        return formattedRank;
    }
}
```

##### Why

The formatter receives metadata and formats it.

No storage.

No cache.

No rules.

Just formatting. A rare moment of restraint.
