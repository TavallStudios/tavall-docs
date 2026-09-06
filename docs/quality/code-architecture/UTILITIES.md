# Project Novus Utility Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Utility Pattern

Project Novus utilities are purpose-scoped adapters or pure helpers. They must not become global junk drawers, alternate service locators, or convenient places to hide domain behavior.

Use an interface when the utility is a real substitution boundary, such as a Paper adapter that callers may replace in tests or another runtime. Use a final static utility class only when behavior is pure, stateless, Java-only, and does not need dependency access or platform substitution.

## Utility Naming

A one-to-one utility interface uses `I` followed by the exact concrete class name.

Good:

```text
IBukkitMessageUtil     -> BukkitMessageUtil
IBukkitEffectUtil      -> BukkitEffectUtil
IBukkitBossBarUtil     -> BukkitBossBarUtil
IBukkitFireworkUtil    -> BukkitFireworkUtil
IBukkitPlayerViewUtil  -> BukkitPlayerViewUtil
IBukkitBlockVisualUtil -> BukkitBlockVisualUtil
IBukkitEntityViewUtil  -> BukkitEntityViewUtil
```

Bad:

```text
BukkitMessageSender -> BukkitMessageUtil
BukkitEffectApplier -> BukkitEffectUtil
```

The role does not change between the interface and implementation. The `I` prefix is the only naming difference.

Do not put dependency lookup or a fallback singleton in the interface. The interface declares the capability; the concrete class owns the behavior; the composition root or constructor owns selection.

## Utility Class Rule

Use utility classes only for focused helper behavior.

Bad:

```java
public final class PlayerUtil {
}
```

### Why

`PlayerUtil` is vague and will collect unrelated player methods until it becomes a landfill.

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

### Why

The utility is focused, stateless, Java-only, and cannot be mistaken for a platform service.

## Paper Utility Pattern

Reusable Paper and Bukkit adapters belong in:

```text
:minecraft-framework:minecraft-nms-framework
```

Preferred package shape:

```text
org.tavall.minecraft.nms.bukkit.<purpose>
```

Examples:

```text
org.tavall.minecraft.nms.bukkit.effect
org.tavall.minecraft.nms.bukkit.message
org.tavall.minecraft.nms.bukkit.bossbar
org.tavall.minecraft.nms.bukkit.firework
org.tavall.minecraft.nms.bukkit.view
org.tavall.minecraft.nms.bukkit.inventory
org.tavall.minecraft.nms.bukkit.location
```

Paper utilities may accept Paper platform objects such as:

```text
Player
LivingEntity
ItemStack
Inventory
Location
World
WorldBorder
BlockData
CommandSender
```

A Paper utility owns only reusable platform adaptation. It does not own game rules, permissions, message templates, arena selection, persistence, scheduling policy, random celebration selection, or mode-specific presentation.

Good:

```java
public interface IBukkitEffectUtil {
    void setGlowing(Entity entity, boolean glowing);
}
```

```java
@DelegatesTo(IBukkitEffectUtil.class)
public final class BukkitEffectUtil implements IBukkitEffectUtil {

    @Override
    public void setGlowing(Entity entity, boolean glowing) {
        if (entity == null) {
            return;
        }
        entity.setGlowing(glowing);
    }
}
```

The caller still owns when the effect happens and why. The utility merely adapts that decision to Paper.

## Player-Facing Presentation Split

Player-facing presentation must stay split by platform responsibility instead of accumulating in one general `PlayerUtil` or `BukkitUtil` class.

`BukkitMessageUtil` owns:

- Legacy color translation.
- Adventure component delivery.
- Action bars.
- Title construction, display, clearing, and reset.
- Online Paper player resolution.
- Player, broadcast, and console delivery.

`BukkitEffectUtil` owns:

- Player-local and world sounds.
- Sound stopping.
- Player-local and world particles.
- Potion-effect application and removal.
- Hurt and hand-swing animations.
- Glowing and visual-fire flags.

`BukkitBossBarUtil` owns:

- Adventure boss bar construction.
- Progress clamping.
- Showing and hiding bars for one or many players.
- Updating bar names and progress.

`BukkitFireworkUtil` owns:

- Firework-effect construction.
- Firework spawning through Paper item data components.
- Immediate or caller-triggered detonation.
- Paper-supported flight-duration clamping.

`BukkitPlayerViewUtil` owns client-only player presentation for:

- Fake experience progress and level.
- Fake health, food, and saturation updates.
- Player-list headers and footers.
- Compass targets.
- Per-player time and weather.
- Per-player world borders.
- Resetting those client overrides to authoritative server state.

`BukkitBlockVisualUtil` owns:

- Visual-only block changes for one or many viewers.
- Visual-only block break progress.
- Progress clamping and explicit damage clearing.

`BukkitEntityViewUtil` owns per-viewer entity presentation for:

- Fake single-slot and multi-slot equipment changes.
- Fake potion-effect additions and removals.

Client-only view utilities must never be treated as gameplay state. They do not replace repositories, registries, entity equipment, block mutation, player health, player experience, or durable settings. The owning workflow must also restore temporary views when its session, preview, tutorial, match, or module lifecycle ends.

The caller owns:

- Which players receive an effect.
- Positive, negative, team, arena, kingdom, or FFA meaning.
- Message keys and placeholders.
- Colors selected from domain state.
- Random effect selection.
- Repetition, delayed detonation, and all scheduling.
- Cleanup tied to module or match lifecycle.

This keeps reusable presentation broad enough to be useful without converting the framework into a theme park ride controller with opinions about who captured which flag.

## Product Boundary

Product-specific orchestration remains in the owning server or mode module.

For example, a Novus message sender may own:

- Message-key lookup.
- Locale selection.
- Placeholder rendering.
- Audience policy.
- Missing-message fallback policy.

Moving the platform calls does not move the product rules. Humanity has tried solving ownership problems by renaming folders before; the results were predictably inspiring.

## Java Utility Pattern

Java-only utilities must not depend on Paper.

Examples:

```text
UUID
Duration
String
Math
Collections
Enums
Dates
```

Preferred package shapes:

```text
org.tavall.java.uuid
org.tavall.java.duration
org.tavall.java.string
org.tavall.java.collection
```

Good class examples:

```text
UUIDFormatUtil
DurationFormatUtil
StringSanitizerUtil
EnumNameUtil
```

## Bad Paper and Java Utility Mixing

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

### Why

The utility mixes Java-only time formatting with Paper player messaging. Anything that wants duration formatting now drags Paper into the room, and the room was already crowded.

## Good Paper and Java Utility Split

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
public final class BukkitCooldownMessageUtil {

    private BukkitCooldownMessageUtil() {
    }

    public static void sendCooldown(Player player, long millis) {
        if (player == null) {
            return;
        }
        player.sendMessage(DurationFormatUtil.formatDuration(millis));
    }
}
```

### Why

Java-only formatting stays Java-only. Paper messaging stays at the Paper boundary. The dependency direction remains obvious.
