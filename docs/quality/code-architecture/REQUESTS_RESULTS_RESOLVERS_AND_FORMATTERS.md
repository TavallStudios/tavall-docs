# Tavall Requests, Results, Resolvers, Viewers, and Formatters

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Request Pattern

Requests group related input for one operation when several values form one meaningful contract.

Bad:

```java
updateRank(
        UUID staffUuid,
        UUID targetUuid,
        RankKey rankKey,
        String reason,
        boolean silent
);
```

Good:

```java
public record RankUpdateRequest(
        UUID staffUuid,
        UUID targetUuid,
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

A Resolver selects or retrieves an **existing typed answer** from explicit input and an identified authority, applying only lookup/selection or narrowly specified fallback rules. It does not generate UI labels, format titles, build a view, render output, or own persistence/Registry/Cache mechanics.

Examples:

```text
MessageDataResolver
PlaceholderDataResolver
PlayerAccountDataResolver
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

## DataResolver Pattern

Prefer a concrete subtype name such as `*DataResolver` when the resolved output is domain data. For example, a `PlayerAccountDataResolver` may resolve an already-authorized account value from a typed identity and its owning data capability, without reimplementing loading, persistence, caching, or authorization. A `*Resolver` is still valid when its resolution responsibility is specific and does not fit a narrower subtype; do not add a parent class or interface solely to model a suffix hierarchy.

## Viewer Pattern

A `*Viewer` maps **already supplied typed data** to a caller-facing view or domain presentation (titles, labels, presentation metadata). A Viewer does not perform source resolution, data loading, permission checks, persistence, or platform rendering. It may use a focused Formatter or other supplied pure presentation values; do not create one solely to forward a Formatter.

`AchievementPointTitleResolver` currently calculates a point-title label from `AchievementPointType`, earned points and obtainable points without retrieving data. Its correct role is a proposed `AchievementPointTitleViewer`, and the interface and callers must migrate together. Do not introduce `AchievementPointTitleViewer` as a parallel second implementation while the original continues to be used.

The existing title implementation's `@ExplicitNonDi` is explicitly justified by pure deterministic behavior. That is a valid exception if the Viewer remains pure and non-managed, **not** proof that every Viewer must bypass DI. If the Viewer is managed or substitutable, register its contract using `@DelegatesTo` and consume it via typed DI instead; remove the non-DI marker.

## Formatter Pattern

A Formatter converts already-known data into a presentation representation.

It should not load data, save data, resolve permissions, mutate caches, or perform unrelated domain decisions.

Bad:

```java
public String format(UUID playerUuid) {
    PlayerAccountData data = dataHandler.load(playerUuid);
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
- [ ] Resolvers retrieve/select existing typed values without becoming display-title helpers or data stores.
- [ ] DataResolvers resolve typed data from named input and the existing authority.
- [ ] Viewers derive presentation from already known data, without fetching or rendering.
- [ ] Formatters receive the values they format rather than loading them.
- [ ] Raw strings/maps are not used where a stable typed key/value exists.
- [ ] These roles do not become hidden persistence/cache/registry/service-locator boundaries.
