# Tavall Utility Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Utilities require an **isolated pattern review** because their shape depends on the actual capability. **Interface composition with reusable default methods is the preferred utility pattern**, especially for managed/platform utilities; pure static and concrete-only shapes remain supported when composition adds no real value. Supported shapes include pure static utilities, composable Java interface defaults, and DI-managed concrete platform utilities. They must not become global junk drawers, alternate service locators, or convenient places to hide domain behavior.

## Default Utility Pattern: Interface Composition

Start with the smallest cohesive utility interface. Put shared, working behavior in `default` methods and override only necessary platform- or implementation-specific mechanics in a concrete class. An optional null/no-op default remains valid when its contract **explicitly** defines absence as safe; required operations remain abstract.

A managed concrete utility registers with `@DelegatesTo(IUtility.class)`. A concrete-only managed utility may use bare `@DelegatesTo`; it does not need an invented empty interface. A utility whose defaults are complete does not require an empty concrete wrapper. Pure Java helpers with no useful composition boundary may remain static.

This default is based on the [Minecraft-CTF composed utility pattern](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/interfaces/IInventoryUtils.java), without retaining obsolete static dependency lookup.

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

## Interface Default-Method and Concrete-Override Utility Pattern

The original [Minecraft-CTF `InventoryGuardUtil`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/inventory/InventoryGuardUtil.java) and [`IInventoryUtils`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/interfaces/IInventoryUtils.java) use composed interface `default` methods; the concrete [`InventoryUtils`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/inventory/InventoryUtils.java) inherits them. [`BukkitMessageSender`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/message/BukkitMessageSender.java) uses guarded default forwarding into a concrete delivery utility. These are historical source evidence for **flexible interface composition**, not authority to keep the retired static `DependencyLoaderAccess` lookup pattern.

A utility may expose optional `default` behavior in its interface and let a concrete implementation override it. A null-returning default or no-op default is supported only when "unavailable" / "no work" is the **declared** and safe operation outcome. Never hide a required capability failure behind `return null` or an empty body. When the behavior must always be implemented, use an abstract interface method instead. A utility that is complete as interface defaults need not manufacture an empty concrete class unless Tavall DI/composition really requires an instance/alias.

```java
/**
 * A composed Bukkit utility with real common defaults and an
 * optional display-name extension.
 */
public interface IBukkitInventoryUtil {

    default boolean hasDisplayName(ItemStack item) {
        return item != null
                && item.hasItemMeta()
                && item.getItemMeta().hasDisplayName();
    }

    /**
     * @return display name or null when unavailable
     */
    default Component findDisplayName(ItemStack item) {
        return null;
    }
}
```

```java
@DelegatesTo(IBukkitInventoryUtil.class)
public final class BukkitInventoryUtil implements IBukkitInventoryUtil {

    @Override
    public Component findDisplayName(ItemStack item) {
        if (!hasDisplayName(item)) {
            return null;
        }

        return item.getItemMeta().displayName();
    }
}
```

The example is **illustrative**, not an existing CTF API. The concrete inherits the working `hasDisplayName` default and overrides only `findDisplayName`. Pure defaults can implement complete behavior without an override. Managed platform utilities still register normally through Tavall DI, not an interface default locator. Review each utility family separately before converting between static, interface-default and concrete-managed styles.

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
- [ ] Start with composed utility interfaces and default methods when reusable behavior exists; use a pure static or concrete-only utility when composition is unnecessary.
- [ ] The concrete overrides only necessary behavior; no ornamental interface or implementation exists solely to satisfy a template.
- [ ] A null/no-op default is documented as a valid optional outcome, not hidden failure; required methods are abstract.
- [ ] Historical CTF composition is preserved without resurrecting static dependency lookup.
