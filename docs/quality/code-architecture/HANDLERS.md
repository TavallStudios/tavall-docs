# Project Novus Handler Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

### Handler Pattern

Handlers are the default behavior classes for Project Novus game systems.

Most game behavior is handling input, data, state, commands, events, GUI actions, or player actions.

That means handlers are usually better than service classes.

#### Bad Handler Pattern

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

The command owns the rule.

The rank is a raw string.

The permission check is fake.

The command mutates player state directly.

This is less architecture and more vibes with a keyboard.

#### Good Handler Pattern

```java
public final class RankUpdateHandler {

    private final PlayerAccountDataHandler playerAccountDataHandler;
    private final PowerLevelHandler powerLevelHandler;
    private final PlayerRankDataHandler playerRankDataHandler;
    private final PlayerAccountCache playerAccountCache;

    public CommandResult updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
        UUID staffUUID = rankUpdateRequest.getStaffUUID();
        UUID targetUUID = rankUpdateRequest.getTargetUUID();

        PlayerAccountData staffAccountData = playerAccountDataHandler.loadPlayerAccountData(
            staffUUID
        );

        PlayerAccountData targetAccountData = playerAccountDataHandler.loadPlayerAccountData(
            targetUUID
        );

        boolean canRankEdit = powerLevelHandler.canRankEdit(
            staffAccountData,
            targetAccountData
        );

        if (!canRankEdit) {
            return CommandResult.targetTooPowerful();
        }

        playerRankDataHandler.updatePlayerRankData(rankUpdateRequest);
        playerAccountCache.refreshPlayerAccountData(targetUUID);

        return CommandResult.success();
    }
}
```

##### Why

The handler coordinates the behavior.

The request object carries the input.

The power-level handler owns the authority check.

The data handler updates rank data.

The cache refresh is explicit.

#### Input Handler Pattern

Input handlers receive external input and convert it into internal requests.

Examples:

* Commands
* Paper events
* GUI clicks
* Chat input
* Plugin messages

Bad:

```java
public final class PlayerJoinListener {

    public void onJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();

        player.sendMessage("Welcome");
        player.setDisplayName("Subject");
        database.save(player.getName());
    }
}
```

##### Why

The listener owns too much behavior.

It sends messages, mutates display state, and saves data directly.

That makes the listener hard to test and easy to break.

Good:

```java
public final class PlayerJoinListener {

    private final PlayerJoinHandler playerJoinHandler;

    public void onJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();

        playerJoinHandler.loadPlayerAccountData(player);
        playerJoinHandler.sendWelcomeMessage(player);
        playerJoinHandler.refreshPlayerTabFormat(player);
    }
}
```

##### Why

The listener receives input.

The handler owns the behavior.

The method names say what actions happen after join.

No `handlePlayerJoin()` nonsense. The class already said that part.

#### Data Handler Pattern

Data handlers move normal data between storage and the codebase.

They may call database classes and builders.

They should not run gameplay rules.

Bad:

```java
public final class PlayerAccountDataHandler {

    public void updateRank(UUID staffUUID, UUID targetUUID, RankKey rankKey) {
        boolean staffIsAllowed = permissionHandler.canRankEdit(
            staffUUID,
            targetUUID
        );

        if (!staffIsAllowed) {
            return;
        }

        playerAccountDatabase.updateRank(targetUUID, rankKey);
    }
}
```

##### Why

The data handler is running authority rules.

That belongs in a behavior handler.

Data handlers should move data. They should not decide whether the action is allowed.

Good:

```java
public final class PlayerRankDataHandler {

    private final PlayerRankDatabase playerRankDatabase;

    public void updatePlayerRankData(RankUpdateRequest rankUpdateRequest) {
        UUID targetUUID = rankUpdateRequest.getTargetUUID();
        RankKey rankKey = rankUpdateRequest.getRankKey();

        playerRankDatabase.updatePlayerRank(
            targetUUID,
            rankKey
        );
    }
}
```

##### Why

The data handler updates data.

It does not decide if the staff member is allowed to do it.

The behavior handler should already have made that decision.

#### MetaData Handler Pattern

MetaData handlers resolve, refresh, and expose metadata.

They should not save primary data unless explicitly designed to.

Bad:

```java
public final class PlayerRankMetaDataHandler {

    public void setRank(UUID playerUUID, RankKey rankKey) {
        playerRankDatabase.updatePlayerRank(playerUUID, rankKey);
    }
}
```

##### Why

This is changing primary player data.

A metadata handler should not own rank writes.

It should resolve or refresh metadata built from that rank data.

Good:

```java
public final class PlayerRankMetaDataHandler {

    private final PlayerAccountDataHandler playerAccountDataHandler;
    private final RankRegistry rankRegistry;
    private final PlayerRankMetaDataBuilder playerRankMetaDataBuilder;

    public PlayerRankMetaData loadPlayerRankMetaData(UUID playerUUID) {
        PlayerAccountData playerAccountData = playerAccountDataHandler.loadPlayerAccountData(
            playerUUID
        );

        RankKey rankKey = playerAccountData.getRankKey();
        RankDefinition rankDefinition = rankRegistry.getRankDefinition(rankKey);

        PlayerRankMetaData playerRankMetaData = playerRankMetaDataBuilder.buildPlayerRankMetaData(
            playerAccountData,
            rankDefinition
        );

        return playerRankMetaData;
    }
}
```

##### Why

The metadata handler loads source data, resolves the rank definition, and builds metadata.

It does not mutate the player rank.
