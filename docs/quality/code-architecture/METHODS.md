# Project Novus Method Rules

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Methods

### Method Rules

Methods should be easy to read from top to bottom.

A method should have one clear job. If the method starts doing setup, validation, storage, formatting, cache mutation, and command output all at once, congratulations, we made soup again.

Rules:

* Method names should explain the action.
* Method bodies should be readable without guessing.
* Important values should be extracted into local variables.
* Avoid hiding logic inside chained calls.
* Keep command/event methods focused on receiving input and delegating work.
* Keep data methods focused on moving data.
* Keep builder methods focused on creating objects.
* Keep utility methods stateless.
* Keep database methods persistence-only.
* Keep cache methods cache-only.

##### Why

Methods are the smallest unit where ownership can become unclear. A method that validates, persists, mutates cache state, formats output, and performs delivery makes every caller depend on all of those concerns at once.

Keeping one coherent action per method makes failure paths visible, lets behavior be reused at the correct layer, and keeps refactoring from turning one innocent call into a hidden workflow.

### Method Naming

Method names should describe the actual action being performed.

Do not name methods after the class role.

Bad:

handlePlayerJoin();
handleRankUpdate();
process();
run();
doThing();
update();

##### Why

"PlayerJoinHandler#handlePlayerJoin()" repeats the class name instead of explaining the work being done.

The class already tells us this is handling player join behavior. The method should tell us what part of the behavior is happening.

Good:

loadPlayerAccountData();
buildPlayerRankMetaData();
sendWelcomeMessage();
refreshPlayerTabFormat();
savePunishmentData();
refreshPlayerAccountCache();

Boolean methods should read like a question.

Good:

hasPermission();
canPunish();
isVanished();
shouldSendWelcomeMessage();

#### Rule

The class name explains the ownership.

The method name explains the action.

Example:

public final class PlayerJoinHandler {

    public void loadPlayerAccountData(Player player) {
    }

    public void sendWelcomeMessage(Player player) {
    }

    public void refreshPlayerTabFormat(Player player) {
    }
}

Bad:

public final class PlayerJoinHandler {

    public void handlePlayerJoin(Player player) {
    }
}

The bad version tells us almost nothing. Spectacularly brave of it.

### Method Parameters

Method parameters should be specific and typed.

Bad:

ban(String player, String reason);
set(String key, Object value);

Good:

banPlayer(PunishmentRequest punishmentRequest);
updatePlayerRank(PlayerRankUpdateRequest rankUpdateRequest);

Prefer request objects when a method needs several related values.

Example:

public PunishmentResult banPlayer(PunishmentRequest punishmentRequest) {
    UUID staffUUID = punishmentRequest.getStaffUUID();
    UUID targetUUID = punishmentRequest.getTargetUUID();
    String reason = punishmentRequest.getReason();

    PunishmentResult punishmentResult = punishmentHandler.banPlayer(
        staffUUID,
        targetUUID,
        reason
    );

    return punishmentResult;
}

Use raw values only when the method is very small and the meaning is obvious.

##### Why

Typed parameters make invalid combinations harder to express and give related values one named contract. A long list of primitive or string parameters pushes meaning into parameter order and caller memory instead of the type system.

Request objects also let validation and future fields evolve without turning every call site into a synchronized signature-editing exercise.

### Method Local Variables

Important values should be extracted into local variables before use.

Bad:

rankMetaDataHandler.refresh(playerAccountDataHandler.load(player.getUniqueId()));

Good:

UUID playerUUID = player.getUniqueId();
PlayerAccountData playerAccountData = playerAccountDataHandler.load(playerUUID);

rankMetaDataHandler.refresh(playerAccountData);

This keeps stack traces, debugging, and reading from turning into ritual suffering.

##### Why

Named locals expose intermediate domain values and failure points. Deep chains hide which operation returned an unexpected value and make breakpoints, logging, stack inspection, and future validation harder to insert cleanly.

The goal is not ceremonial variable creation; it is making meaningful steps visible when those steps matter to ownership or debugging.

### Method Size

Methods should stay small enough to understand quickly.

A method is probably too large when:

* It has multiple unrelated responsibilities.
* It has several levels of nested logic.
* It creates data, validates it, saves it, caches it, and sends messages.
* It is hard to name without using "and".

Split large methods by responsibility.

Good split:

receive command input
  -> build request
  -> delegate to handler
  -> send result message

##### Why

Method size is a symptom, not a line-count contest. A large method usually matters because it has accumulated several reasons to change or several owners' responsibilities.

Splitting by responsibility makes each phase independently testable and lets storage, validation, formatting, and delivery evolve without forcing every change through one giant method.

### Handler Methods

Handler methods receive input, coordinate behavior, and delegate work.

Handlers are the default place for game behavior.

Example:

public CommandResult updatePlayerRank(RankUpdateRequest rankUpdateRequest) {
    UUID staffUUID = rankUpdateRequest.getStaffUUID();
    UUID targetUUID = rankUpdateRequest.getTargetUUID();

    PlayerAccountData staffAccountData = playerAccountDataHandler.load(staffUUID);
    PlayerAccountData targetAccountData = playerAccountDataHandler.load(targetUUID);

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

Handlers may use:

Data handlers
Metadata handlers
Builders
Caches
Databases
Other handlers

Handlers should not become storage classes.

##### Why

A handler is an operation owner, not a data structure owner. It may coordinate the dependencies needed for one behavior, but storing durable or keyed runtime state inside the handler gives the input-facing class a second lifecycle responsibility.

Delegating storage and reusable rules keeps the handler focused and allows the same domain behavior to be invoked from commands, events, web, Discord, or tests without copying implementation details.

### Data Handler Methods

Data handler methods move normal data between storage and the codebase.

Examples:

loadPlayerAccountData();
savePlayerAccountData();
updatePlayerRankData();
deleteExpiredPunishmentData();

Data handlers may call database classes.

They should not own gameplay rules.

Good:

public PlayerAccountData loadPlayerAccountData(UUID playerUUID) {
    PlayerAccountEntity playerAccountEntity = playerAccountDatabase.find(playerUUID);

    PlayerAccountData playerAccountData = playerAccountDataBuilder.buildPlayerAccountData(
        playerAccountEntity
    );

    return playerAccountData;
}

##### Why

Data-handler methods give storage translation and consistency behavior one reusable boundary. Gameplay rules change because product behavior changes; persistence mapping changes because storage changes. Combining them makes either kind of change unnecessarily risky.

A data handler may coordinate repository/cache mechanics when that coordination is part of data access policy, but it should not decide whether the gameplay operation itself is allowed.

### Builder Methods

Builder methods create objects.

They should not save, cache, send messages, or run permission checks.

##### Why

A build call should be predictable from its explicit inputs. If building performs persistence, cache mutation, permission resolution, or delivery, construction gains hidden side effects and failure modes.

Keeping builders pure enough to construct values makes them safe in tests, migrations, handlers, repositories, and other composition paths.

### Data Builder Methods

Data builder methods create normal data objects.

Good:

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

### Meta Data Builder Methods

Metadata builder methods create resolved or display-ready metadata from normal data.

Good:

public PlayerRankMetaData buildPlayerRankMetaData(
    PlayerAccountData playerAccountData,
    RankDefinition rankDefinition
) {
    RankKey rankKey = playerAccountData.getRankKey();
    String displayName = rankDefinition.getDisplayName();
    String legacyColor = rankDefinition.getLegacyColor();

    PlayerRankMetaData playerRankMetaData = new PlayerRankMetaData(
        rankKey,
        displayName,
        legacyColor
    );

    return playerRankMetaData;
}

##### Why

Separating source-data construction from metadata construction keeps persisted/runtime truth distinct from derived or presentation-ready values. The two types often have different rebuild and invalidation rules even when one is produced from the other.

That separation prevents convenience metadata from leaking back into durable schemas simply because one builder happened to know both shapes.

### Utility Methods

Utility methods should be focused and stateless.

Good:

public static String translateLegacyColors(String message) {
    String translatedMessage = ChatColor.translateAlternateColorCodes(
        '&',
        message
    );

    return translatedMessage;
}

Utility methods should not touch:

Databases
Caches
Commands
Paper events
Player state

If a utility needs system state, it probably is not a utility. Wild concept, I know.

##### Why

Utility methods are safe to call broadly only when their result depends on explicit input rather than hidden runtime state. Once a utility touches caches, persistence, players, scheduling, or events, it acquires lifecycle and substitution requirements that static helper syntax cannot express.

Stateful runtime behavior belongs behind DI-managed classes where ownership and replacement remain visible.

### Database Methods

Database methods own persistence access.

Project Novus persistence classes should use `tavall-database` and JPA where they fit the owning schema and query model. Explicit SQL remains valid for migrations, performance-sensitive queries, JSONB operations, and storage behavior that JPA cannot express cleanly.

Project Novus targets Java 21. Records, sealed types, pattern matching, virtual threads, and other modern features may be used when they improve ownership and clarity rather than merely shortening syntax.

Database methods should:

* Read entities.
* Save entities.
* Update entities.
* Delete entities.
* Use typed entity classes.
* Keep gameplay rules out.

Example find method:

public PlayerAccountEntity find(UUID playerUUID) {
    EntityManager entityManager = entityManagerProvider.getEntityManager();

    PlayerAccountEntity playerAccountEntity = entityManager.find(
        PlayerAccountEntity.class,
        playerUUID
    );

    return playerAccountEntity;
}

Example save method:

public void save(PlayerAccountEntity playerAccountEntity) {
    EntityManager entityManager = entityManagerProvider.getEntityManager();
    EntityTransaction entityTransaction = entityManager.getTransaction();

    entityTransaction.begin();

    entityManager.persist(playerAccountEntity);

    entityTransaction.commit();
}

Database classes should not decide whether a staff member can punish someone, whether a rank change is allowed, or whether a command should succeed.

That belongs in handlers.

##### Why

Persistence methods should be reusable for every caller that needs the same durable operation. Embedding gameplay authorization or command outcomes into database methods ties domain behavior to one storage implementation and makes transactions responsible for decisions they do not own.

Keeping database methods persistence-only also makes retries, migrations, transaction tests, and alternate storage implementations possible without duplicating game rules.

### Cache Methods

Cache methods own temporary fast-access state.

Good method names:

putPlayerAccountData();
getPlayerAccountData();
removePlayerAccountData();
refreshPlayerAccountData();
containsPlayerAccountData();

Example:

public void refreshPlayerAccountData(UUID playerUUID) {
    PlayerAccountData playerAccountData = playerAccountDataHandler.loadPlayerAccountData(
        playerUUID
    );

    playerAccountCache.putPlayerAccountData(
        playerUUID,
        playerAccountData
    );
}

Cache methods should not be treated as the permanent source of truth unless that system explicitly says so.

##### Why

Cache operations describe disposable state with explicit invalidation and lifetime semantics. Treating cache methods as durable writes or authoritative reads makes eviction and restart indistinguishable from data loss.

Keeping cache behavior narrow allows callers to reason about misses, reloads, TTL, and invalidation without pretending the fast path is also the persistence model.

### Test Methods

Test method rules are defined in the "Testing" section of this document.

Do not duplicate the full testing rules here.

For method naming, test methods should describe the behavior being tested.

Good:

modCannotPunishAdmin();
ownerCanPunishManager();
rankUpdateRefreshesPlayerAccountCache();
missingPlayerAccountReturnsFallbackData();

##### Why

Behavior-oriented test names document the contract that failed, not merely the method that happened to execute. That makes regressions readable in CI and avoids generic names such as `testUpdate()` that require opening the test just to learn what broke.