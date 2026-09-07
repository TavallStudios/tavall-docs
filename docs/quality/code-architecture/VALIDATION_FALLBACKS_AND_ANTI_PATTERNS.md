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

#### Loose or Untyped Map Pattern

A loose map is a `Map`, `ConcurrentMap`, `HashMap`, `ConcurrentHashMap`, `Set`, or parallel keyed collection that is used as an unnamed domain model, storage system, runtime registry, cache, operation payload, or behavior API instead of a typed Tavall boundary.

Loose maps are prohibited in ordinary production consumers such as handlers, services, orchestrators, routers, listeners, commands, controllers, gateways, and adapters.

Bad:

```java
public final class PlayerSessionHandler {
    private final Map<UUID, Map<String, Object>> sessions =
            new ConcurrentHashMap<>();

    public void put(UUID playerId, String key, Object value) {
        sessions.computeIfAbsent(playerId, ignored -> new ConcurrentHashMap<>())
                .put(key, value);
    }

    public Object get(UUID playerId, String key) {
        Map<String, Object> data = sessions.get(playerId);
        return data == null ? null : data.get(key);
    }
}
```

This is rejected even when the collection is private, thread-safe, short-lived, or named `data`, `state`, `entries`, `sessions`, or `metadata`.

##### Why

A loose map erases the architecture the collection is already implementing.

The key type does not state the full identity contract. The value shape is not enforced. Duplicate, replacement, expiry, persistence, cleanup, indexing, and failure behavior become scattered `put`, `get`, `compute`, and `remove` calls. Consumers start owning state rather than consuming the boundary that owns it.

Thread safety does not make a map a registry. A generic value type does not make a map metadata. A short lifetime does not make a map harmless.

##### Required Replacement

Classify the state before choosing a replacement:

1. **Durable state** uses a repository and the owning data handler or persistence workflow.
2. **Loaded definitions, providers, strategies, sessions, active runtime objects, or keyed process state** use a Tavall Registry.
3. **Disposable, reloadable, stale-able, or expiring state** uses Tavall Cache.
4. **Several indexes over one identity** use `AbstractIndexedRegistry` or one typed aggregate rather than parallel maps.
5. **A short-lived operation payload or result** uses a typed `*Data`, `*Request`, `*Result`, `*State`, or `*MetaData` class.
6. **Extensible integration metadata** may contain a typed map only inside the owning data or metadata type, and only when the external schema is intentionally open-ended.
7. **Static lookup data** belongs in a dedicated immutable data/configuration/value type rather than mutable state inside a behavior class.

If the key is a primitive or platform value such as `UUID`, `String`, `long`, or an enum, that is not a reason to make the value loose. Give the value a domain type.

Prefer:

```java
public record PlayerSessionData(
        UUID playerId,
        SessionId sessionId,
        Instant startedAt,
        PlayerSessionState state
) {
}
```

Then place keyed lifecycle behavior behind a registry:

```java
public interface IPlayerSessionRegistry {
    Optional<PlayerSessionData> find(UUID playerId);

    PlayerSessionData start(UUID playerId);

    void end(UUID playerId);
}
```

The registry owns the collection. Normal consumers receive the registry through Tavall DI and call domain methods. They do not receive, expose, mutate, or recreate the backing map.

##### Collection Construction Rule

Mutable map or set construction for domain state belongs only inside the dedicated data/storage boundary that owns that state, such as a registry, cache, repository substitute, indexed state implementation, or intentionally map-backed `*Data`/`*MetaData` type.

Ordinary behavior consumers do not instantiate mutable maps to hold domain state. They consume typed dependencies through DI.

A method-local map is allowed only for a bounded, non-domain algorithmic transformation when all of the following are true:

- the key and value types are concrete and meaningful;
- the collection never escapes the method;
- it is not returned as an operation result;
- it is not stored on an object;
- it does not represent durable, cached, registry, session, lifecycle, or authorization state;
- replacing it with a named data type would not improve the domain contract.

This exception is intentionally narrow. If the map represents something engineers can name, model the named thing.

##### API Rule

Do not expose generic map behavior as the domain API.

Bad:

```java
sessionRegistry.getSessions().put(playerId, session);
metadata.put("region", regionId);
state.compute(playerId, mutation);
```

Good:

```java
sessionRegistry.start(playerId);
playerMetaDataHandler.resolve(request);
playerStateHandler.applyMutation(request);
```

Behavior such as lookup, registration, replacement, mutation, invalidation, persistence, expiry, snapshotting, and cleanup belongs behind focused methods on DI-managed dependencies.

Do not create `getMap()`, `entries()`, or mutable snapshot access merely to let consumers perform the behavior the owning boundary should provide itself.

##### Metadata Rule

`Map<String, Object>` is not a metadata model.

Use a `*MetaData` type for known metadata. Add a `*MetaDataHandler` only when metadata needs derivation, normalization, validation, enrichment, or cross-source resolution. Passive metadata does not require a handler merely to satisfy a naming pattern.

An intentionally extensible metadata map is permitted only at a real integration edge and remains encapsulated inside its owning metadata/data type. Core identity, authorization, lifecycle, state transitions, and behavior fields remain typed.

##### Enforcement Rule

Architecture review should treat a newly added mutable map/set field or `Map<String, Object>`-style API in production code as a violation candidate by default. The author must show that it fits one of the narrow allowed data/storage cases above rather than asking reviewers to infer that a generic collection is probably fine.

The canonical architecture-test repository should encode enforceable cases as the static-analysis surface evolves. Documentation exceptions do not silently become code-generation defaults.

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
