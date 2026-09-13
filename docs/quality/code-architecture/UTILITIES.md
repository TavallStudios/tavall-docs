# Tavall Utility Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Utilities are either **pure stateless helpers** or **focused runtime/platform adapters**. They must not become global junk drawers, alternate service locators, or convenient places to hide domain behavior.

## Pure Java Utility Pattern

Use a final static utility class only when behavior is:

- pure;
- stateless;
- dependent only on explicit inputs;
- free of Tavall-managed/runtime/platform state;
- free of persistence, cache, registry, scheduling, network, or lifecycle behavior.

Good:

```java
public final class DurationFormatUtil {
    private DurationFormatUtil() {
    }

    public static String formatDuration(long millis) {
        return millis + "ms";
    }
}
```

##### Why

Pure helpers are safe to call broadly because they cannot retain generation state, bypass DI, or hide runtime ownership. Their result depends only on their arguments.

## Runtime/Platform Utility Pattern

A utility that touches runtime/platform state is an instance capability and participates in Tavall DI when Tavall manages it.

Examples include:

```text
IBukkitMessageUtil     -> BukkitMessageUtil
IBukkitEffectUtil      -> BukkitEffectUtil
IBukkitBossBarUtil     -> BukkitBossBarUtil
IBukkitFireworkUtil    -> BukkitFireworkUtil
IBukkitPlayerViewUtil  -> BukkitPlayerViewUtil
IBukkitBlockVisualUtil -> BukkitBlockVisualUtil
IBukkitEntityViewUtil  -> BukkitEntityViewUtil
```

Managed utilities use `@DelegatesTo` and are resolved through the owning `DependencyAccess` surface. Do not select them through a constructor, fallback singleton, global static accessor, or service locator.

```java
@DelegatesTo(IBukkitEffectUtil.class)
public final class BukkitEffectUtil implements IBukkitEffectUtil {
    @Override
    public void setGlowing(Entity entity, boolean glowing) {
        if (entity != null) {
            entity.setGlowing(glowing);
        }
    }
}
```

##### Why

Runtime utilities need replacement, testing, and lifecycle semantics just like other managed behavior. Static/global access or constructor selection creates a second dependency path and can retain the wrong generation/implementation.

## Naming

A one-to-one utility interface normally uses `I` followed by the exact concrete capability name where the owning codebase follows that convention.

Do not rename the interface and implementation as different roles just to sound more abstract.

Bad:

```text
BukkitMessageSender -> BukkitMessageUtil
BukkitEffectApplier -> BukkitEffectUtil
```

Good:

```text
IBukkitMessageUtil -> BukkitMessageUtil
IBukkitEffectUtil  -> BukkitEffectUtil
```

##### Why

The interface and implementation expose the same capability. Matching names make DI aliases and diagnostics obvious without requiring readers to infer a secret vocabulary mapping.

## Scope Rule

A runtime utility adapts platform mechanics. It does not own:

- product/gameplay rules;
- permissions/authorization;
- message template selection;
- persistence;
- cache/registry authority;
- scheduling policy;
- random product behavior;
- mode-specific meaning;
- lifecycle orchestration beyond cleanup intrinsic to the adapter itself.

The caller/domain owner decides **why** and **when** the capability is used. The utility adapts that decision to the platform.

##### Why

Platform adaptation is reusable only while it remains neutral about product meaning. Once `BukkitEffectUtil` decides who won a match or which punishment occurred, the framework owns a product rule it cannot correctly generalize.

## Presentation Utility Split

Player-facing presentation stays split by platform responsibility instead of accumulating in one `PlayerUtil`/`BukkitUtil` class.

Examples of focused roles:

- message/component/action-bar/title delivery;
- sound/particle/effect application;
- boss-bar construction/update/show/hide;
- firework construction/spawn/detonation;
- client-only player view overrides;
- visual-only block changes/break progress;
- per-viewer entity equipment/effect presentation.

Client-only view utilities never become authoritative gameplay state. The owning workflow restores temporary views during cancellation/shutdown.

##### Why

A broad `PlayerUtil` erases both platform responsibility and cleanup ownership. Focused adapters make it clear which capability owns temporary client state and which domain workflow must eventually restore it.

## Java and Platform Separation

Pure Java formatting/normalization should not import Paper/Velocity/Spring/Discord APIs.

Bad:

```java
public final class TimeUtil {
    public static String formatDuration(long millis) {
        return millis + "ms";
    }

    public static void sendCooldown(Player player, long millis) {
        player.sendMessage(formatDuration(millis));
    }
}
```

Good split:

```java
public final class DurationFormatUtil {
    private DurationFormatUtil() {
    }

    public static String formatDuration(long millis) {
        return millis + "ms";
    }
}
```

```java
@DelegatesTo(IBukkitCooldownMessageUtil.class)
public final class BukkitCooldownMessageUtil
        implements IBukkitCooldownMessageUtil,
        DependencyAccess<IBukkitMessageUtil> {

    @Override
    public void sendCooldown(Player player, long millis) {
        String message = DurationFormatUtil.formatDuration(millis);
        getInstance().send(player, Component.text(message));
    }
}
```

##### Why

Java-only formatting remains reusable anywhere. Runtime delivery remains behind a DI-managed platform boundary rather than becoming a static helper with hidden server state.

## Product Boundary

Product-specific orchestration remains in the owning product/module.

For example, a message workflow may own:

- message-key lookup;
- locale selection;
- placeholder rendering;
- audience policy;
- missing-message fallback policy.

The platform utility owns only delivery mechanics.

##### Why

Moving platform calls into a utility does not transfer product authority. Renaming folders has, once again, failed to repeal ownership.

## Review Checklist

- [ ] Pure static utilities depend only on explicit inputs and own no runtime state.
- [ ] Runtime/platform utilities are instance capabilities and use Tavall DI where managed.
- [ ] No utility interface/singleton/static method locates managed dependencies.
- [ ] Platform adapters do not own product rules or durable/cache/registry authority.
- [ ] Client-only presentation is restored by the owning lifecycle.
- [ ] Java-only helpers do not import platform APIs.
- [ ] Utility names are focused and do not become generic buckets.
