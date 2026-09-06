# Project Novus Builder Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Patterns

### Pattern Rules

Patterns should make the code easier to understand, test, and change.

Do not use a pattern just because it sounds official. That is how a five-line problem becomes a shrine to suffering.

Patterns should:

* Make ownership clearer.
* Keep data flow readable.
* Keep behavior in the right class.
* Avoid raw strings and magic values.
* Work with Java 21 and the owning Paper, Velocity, web, or standalone runtime.
* Match the class and method rules already defined in this document.

#### Bad Pattern Usage

```java
public final class PlayerManager {

    private final Map<String, Object> data = new HashMap<String, Object>();

    public void update(String key, Object value) {
        data.put(key, value);
    }
}
```

##### Why

This hides every real responsibility behind vague names.

There is no clear system ownership, no type safety, no real data shape, and no readable behavior.

#### Good Pattern Usage

```java
public final class PlayerAccountDataHandler {

    private final PlayerAccountDatabase playerAccountDatabase;
    private final PlayerAccountDataBuilder playerAccountDataBuilder;

    public PlayerAccountData loadPlayerAccountData(UUID playerUUID) {
        PlayerAccountEntity playerAccountEntity = playerAccountDatabase.findPlayerAccountEntity(
            playerUUID
        );

        PlayerAccountData playerAccountData = playerAccountDataBuilder.buildPlayerAccountData(
            playerAccountEntity
        );

        return playerAccountData;
    }
}
```

##### Why

The class name explains the role.

The method name explains the action.

The database class reads persistence data.

The builder creates the data object.

The handler coordinates the flow.

### Builder Pattern

Builders are a default preferred pattern in Project Novus.

Builders are not only for creating simple data objects.

Builders may safely assemble, hydrate, configure, mutate, register, or prepare a system object or flow.

The builder name must make the responsibility clear.

Builders are preferred over long constructor injection when construction needs several dependencies, setup values, or ordered setup steps.

#### Builder Class Rule

Use a builder when construction or setup needs more than a tiny obvious constructor.

Bad:

```java
public final class RankUpdateHandler {

    public RankUpdateHandler(
        PlayerAccountDataHandler playerAccountDataHandler,
        PlayerRankDataHandler playerRankDataHandler,
        PlayerRankMetaDataHandler playerRankMetaDataHandler,
        PlayerAccountCache playerAccountCache,
        RankRegistry rankRegistry,
        PermissionHandler permissionHandler,
        PowerLevelHandler powerLevelHandler
    ) {
    }
}
```

##### Why

The constructor is doing too much.

It is noisy, easy to break, and annoying to read.

Long constructor injection turns class setup into a parameter hostage situation.

Good:

```java
public final class RankUpdateHandlerBuilder {

    private PlayerAccountDataHandler playerAccountDataHandler;
    private PlayerRankDataHandler playerRankDataHandler;
    private PlayerRankMetaDataHandler playerRankMetaDataHandler;
    private PlayerAccountCache playerAccountCache;
    private RankRegistry rankRegistry;
    private PermissionHandler permissionHandler;
    private PowerLevelHandler powerLevelHandler;

    public RankUpdateHandlerBuilder withPlayerAccountDataHandler(
        PlayerAccountDataHandler playerAccountDataHandler
    ) {
        this.playerAccountDataHandler = playerAccountDataHandler;

        return this;
    }

    public RankUpdateHandlerBuilder withPlayerRankDataHandler(
        PlayerRankDataHandler playerRankDataHandler
    ) {
        this.playerRankDataHandler = playerRankDataHandler;

        return this;
    }

    public RankUpdateHandler buildRankUpdateHandler() {
        RankUpdateHandler rankUpdateHandler = new RankUpdateHandler(
            playerAccountDataHandler,
            playerRankDataHandler,
            playerRankMetaDataHandler,
            playerAccountCache,
            rankRegistry,
            permissionHandler,
            powerLevelHandler
        );

        return rankUpdateHandler;
    }
}
```

##### Why

The setup has a real object.

The builder owns construction.

The handler can stay focused on behavior.

The caller can read what is being assembled without counting constructor parameters like a cursed spreadsheet.

#### Data Builder Pattern

Data builders create normal data objects.

Data builders usually build data from:

* Database entities
* Config values
* Runtime input
* Request objects
* Other domain data

Bad:

```java
public final class DataBuilder {

    public Object build(Object input) {
        return input;
    }
}
```

##### Why

This does not tell us what data is being built.

It also throws away type safety, which is not exactly a trust-building exercise.

Good:

```java
public final class PlayerAccountDataBuilder {

    public PlayerAccountData buildPlayerAccountData(PlayerAccountEntity playerAccountEntity) {
        UUID playerUUID = playerAccountEntity.getPlayerUUID();
        String playerName = playerAccountEntity.getPlayerName();
        RankKey rankKey = playerAccountEntity.getRankKey();

        PlayerAccountData playerAccountData = new PlayerAccountData(
            playerUUID,
            playerName,
            rankKey
        );

        return playerAccountData;
    }
}
```

##### Why

The class says what data it builds.

The method says what object it creates.

The values are extracted into readable local variables before the object is created.

#### MetaData Builder Pattern

MetaData builders create resolved or display-ready metadata from normal data.

Metadata should be easy to rebuild from source data.

Bad:

```java
public final class MetaBuilder {

    public PlayerRankMetaData build(PlayerAccountData playerAccountData) {
        return new PlayerRankMetaData(playerAccountData.getRankKey().name());
    }
}
```

##### Why

The class name is vague.

The method name is vague.

The chained call hides the value being used.

The builder also does not show where display data comes from.

Good:

```java
public final class PlayerRankMetaDataBuilder {

    public PlayerRankMetaData buildPlayerRankMetaData(
        PlayerAccountData playerAccountData,
        RankDefinition rankDefinition
    ) {
        RankKey rankKey = playerAccountData.getRankKey();
        String displayName = rankDefinition.getDisplayName();
        String legacyColor = rankDefinition.getLegacyColor();
        int powerLevel = rankDefinition.getPowerLevel();

        PlayerRankMetaData playerRankMetaData = new PlayerRankMetaData(
            rankKey,
            displayName,
            legacyColor,
            powerLevel
        );

        return playerRankMetaData;
    }
}
```

##### Why

The metadata is built from clear source objects.

The result is display-ready.

The builder still only builds metadata.

#### Request Builder Pattern

Request builders create request objects from command input, event input, GUI input, or other external data.

Bad:

```java
RankUpdateRequest rankUpdateRequest = new RankUpdateRequest(
    staffUUID,
    targetUUID,
    rankKey,
    reason,
    silent
);
```

##### Why

This is fine when the object is tiny.

It becomes bad when request creation needs parsing, defaults, validation, sender conversion, fallback values, or player lookup.

Good:

```java
public final class RankUpdateRequestBuilder {

    public RankUpdateRequest buildRankUpdateRequest(
        CommandSender sender,
        String targetName,
        String rankInput,
        String reason
    ) {
        UUID staffUUID = senderUUIDResolver.resolveSenderUUID(sender);
        UUID targetUUID = playerUUIDResolver.resolvePlayerUUID(targetName);
        RankKey rankKey = rankKeyResolver.resolveRankKey(rankInput);
        boolean silent = false;

        RankUpdateRequest rankUpdateRequest = new RankUpdateRequest(
            staffUUID,
            targetUUID,
            rankKey,
            reason,
            silent
        );

        return rankUpdateRequest;
    }
}
```

##### Why

The builder owns the messy input conversion.

The command can stay focused on command flow.

#### Result Builder Pattern

Result builders create result objects when success/failure output has multiple paths.

Bad:

```java
return new CommandResult(false, "target-too-powerful");
```

##### Why

The failure reason is a raw string.

The result shape is being rebuilt manually.

That is how result handling becomes a pile of slightly different lies.

Good:

```java
public final class CommandResultBuilder {

    public CommandResult buildTargetTooPowerfulResult() {
        CommandFailureReason failureReason = CommandFailureReason.TARGET_TOO_POWERFUL;

        CommandResult commandResult = CommandResult.failure(failureReason);

        return commandResult;
    }

    public CommandResult buildSuccessResult() {
        CommandResult commandResult = CommandResult.success();

        return commandResult;
    }
}
```

##### Why

Result creation stays consistent.

Handlers do not need to rebuild the same result shapes everywhere.

#### Database Entity Builder Pattern

Database entity builders create persistence entities.

Database entity builders should be used with `tavall-database` and JPA-shaped entity classes where appropriate.

Bad:

```java
public final class PlayerAccountDatabase {

    public void savePlayerAccountData(PlayerAccountData playerAccountData) {
        PlayerAccountEntity playerAccountEntity = new PlayerAccountEntity();

        playerAccountEntity.setPlayerUUID(playerAccountData.getPlayerUUID());
        playerAccountEntity.setPlayerName(playerAccountData.getPlayerName());
        playerAccountEntity.setRankKey(playerAccountData.getRankKey());

        savePlayerAccountEntity(playerAccountEntity);
    }
}
```

##### Why

The database class is building entities and saving them.

Persistence access and entity construction are now mixed together.

Good:

```java
public final class PlayerAccountEntityBuilder {

    public PlayerAccountEntity buildPlayerAccountEntity(PlayerAccountData playerAccountData) {
        UUID playerUUID = playerAccountData.getPlayerUUID();
        String playerName = playerAccountData.getPlayerName();
        RankKey rankKey = playerAccountData.getRankKey();

        PlayerAccountEntity playerAccountEntity = new PlayerAccountEntity();

        playerAccountEntity.setPlayerUUID(playerUUID);
        playerAccountEntity.setPlayerName(playerName);
        playerAccountEntity.setRankKey(rankKey);

        return playerAccountEntity;
    }
}
```

##### Why

The data object and JPA entity stay separate.

The database class can persist entities without knowing how every domain object is assembled.

#### Runtime Builder Pattern

Runtime builders assemble runtime objects, handlers, registries, caches, or feature flows.

They may wire dependencies, register handlers, or prepare state.

Runtime builders should still have clear names.

Bad:

```java
public final class SetupBuilder {
}
```

##### Why

`SetupBuilder` tells us nothing.

Setup for what?

A feature?

A handler?

A ritual?

Good:

```java
public final class ChatRuntimeBuilder {

    public ChatRuntime buildChatRuntime() {
        ChatFormatRegistry chatFormatRegistry = buildChatFormatRegistry();
        ChatFormatResolver chatFormatResolver = buildChatFormatResolver(chatFormatRegistry);
        ChatMessageHandler chatMessageHandler = buildChatMessageHandler(chatFormatResolver);

        ChatRuntime chatRuntime = new ChatRuntime(
            chatFormatRegistry,
            chatFormatResolver,
            chatMessageHandler
        );

        return chatRuntime;
    }
}
```

##### Why

The builder owns runtime assembly.

The name explains the system being assembled.
