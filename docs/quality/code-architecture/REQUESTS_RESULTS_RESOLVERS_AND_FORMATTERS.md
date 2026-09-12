# Tavall Requests, Results, Resolvers, and Formatters

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Request Pattern

Requests group related input for one operation when several values form one meaningful contract.

Bad:

```java
updateRank(
        UUID staffUUID,
        UUID targetUUID,
        RankKey rankKey,
        String reason,
        boolean silent
);
```

Good:

```java
public record RankUpdateRequest(
        UUID staffUUID,
        UUID targetUUID,
        RankKey rankKey,
        String reason,
        boolean silent
) {
}
```

##### Why

The request gives related input a real shape, prevents order-based meaning from dominating the API, and allows validation/evolution without turning every call site into a synchronized signature edit.

Do not create a request object for one or two obvious values merely to satisfy a pattern checklist.

## Result Pattern

Results describe expected operation outcomes when a boolean/null cannot explain what happened.

Bad:

```java
public boolean updatePlayerRank(RankUpdateRequest request) {
    return false;
}
```

Good:

```java
public record RankUpdateResult(
        boolean success,
        RankUpdateFailureType failureType
) {
    public static RankUpdateResult success() {
        return new RankUpdateResult(true, null);
    }

    public static RankUpdateResult targetTooPowerful() {
        return new RankUpdateResult(
                false,
                RankUpdateFailureType.TARGET_TOO_POWERFUL
        );
    }
}
```

##### Why

`false` does not say whether permission failed, state was invalid, the target was too powerful, or some expected domain rejection occurred. Typed results let callers respond correctly without guessing.

Infrastructure failures and violated invariants still use operation-specific exceptions rather than forcing every catastrophic failure into an expected result enum.

## Resolver Pattern

A Resolver derives one typed answer from explicit input and managed capabilities.

Examples:

```text
MessageResolver
PlaceholderResolver
RankDisplayResolver
FormatResolver
DestinationResolver
```

Bad:

```java
String message = config.getString("chat.player.format");
```

Good shape:

```java
@DelegatesTo(IChatFormatResolver.class)
public final class ChatFormatResolver
        implements IChatFormatResolver,
        DependencyAccess<IChatFormatRegistry> {

    @Override
    public ChatFormatDefinition resolve(
            ChatMessageFormatKey key
    ) {
        return getInstance()
                .find(key)
                .orElseThrow();
    }
}
```

##### Why

The caller uses a typed key while the resolver owns lookup/fallback/derivation behavior. Managed collaborators stay behind Tavall DI instead of becoming constructor-captured fields.

A Resolver should not become a repository, cache owner, or generic service locator.

## Formatter Pattern

A Formatter converts already-known data into a presentation representation.

It should not load data, save data, resolve permissions, mutate caches, or perform unrelated domain decisions.

Bad:

```java
public String format(UUID playerUUID) {
    PlayerAccountData data = dataHandler.load(playerUUID);
    return data.rankKey().name();
}
```

Good:

```java
public String formatPlayerRank(
        PlayerRankMetaData metaData
) {
    return metaData.legacyColor() + metaData.displayName();
}
```

##### Why

Formatting is deterministic from already-known input. Once the formatter starts loading data or resolving authority, it becomes hidden behavior with I/O and failure semantics that callers cannot infer from `format()`.

## Review Checklist

- [ ] Requests group genuinely related operation input.
- [ ] Results explain meaningful expected outcomes.
- [ ] Resolvers derive one typed answer and use Tavall DI for managed collaborators.
- [ ] Formatters receive the values they format rather than loading them.
- [ ] Raw strings/maps are not used where a stable typed key/value exists.
- [ ] These roles do not become hidden persistence/cache/registry/service-locator boundaries.
