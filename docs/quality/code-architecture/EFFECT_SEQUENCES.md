# Project Novus Effect Sequence Architecture

> **Status:** Active
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)
> **Applies to:** Reusable Minecraft player-facing effect composition, timing, animation, particle rendering, and cleanup

Effect sequences coordinate reusable presentation utilities. They do not replace the utility layer, message resolution, gameplay handlers, custom-entity runtimes, or authoritative state.

## Utility-First Rule

Use the existing `IBukkit*Util` surface for one immediate Paper operation.

Examples:

```java
getEffectUtil().playSound(player, Sound.BLOCK_NOTE_BLOCK_PLING, 1.0F, 1.0F);
getMessageUtil().sendActionBar(player, message);
getFireworkUtil().spawnInstantFirework(location, fireworkEffect);
getBlockVisualUtil().sendBlockChange(player, location, blockData);
```

The effect-sequence layer is for behavior that needs one or more of:

- several presentation surfaces coordinated together;
- absolute timing;
- reusable effect definitions;
- animation frames;
- sequence-owned cleanup;
- stateful visual updates such as one boss bar changing over a timeline.

Do not route every sound, particle, title, or fake block through a sequence merely because the sequence API exists.

## Modern DI Access

Consumers use Tavall DI's ranked production style: `DependencyAccess<...>` with named local getters.

For an expanded dependency set:

```java
public final class MatchPresentationHandler
        implements DependencyAccess<
                IBukkitEffectUtil,
                IBukkitEffectSequenceHandler
        > {

    private IBukkitEffectUtil getEffectUtil() {
        return getInstance().bukkitEffectUtil();
    }

    private IBukkitEffectSequenceHandler getEffectSequenceHandler() {
        return getInstance().bukkitEffectSequenceHandler();
    }
}
```

For a single dependency:

```java
public final class OvertimePresentationHandler
        implements DependencyAccess<IBukkitEffectSequenceHandler> {

    private IBukkitEffectSequenceHandler getEffectSequenceHandler() {
        return getInstance();
    }
}
```

Do not add a dependency field merely to avoid the generated access path. Named getters resolve the metadata-owned dependency and preserve replacement/reload behavior.

The sequence handler itself follows the same rule for `IBukkitMessageUtil`, `IBukkitEffectUtil`, `IBukkitBossBarUtil`, `IBukkitFireworkUtil`, and `IBukkitBlockVisualUtil`. It must not instantiate replacement utility objects with `new Bukkit*Util()`.

## Entry Point

Actual sequence delivery begins through:

```java
getEffectSequenceHandler().send(players)
```

or:

```java
getEffectSequenceHandler().send(player)
```

The terminal operation remains:

```java
.start();
```

Do not introduce `.to(...)`, `effects.play(...)`, or a second delivery entry point.

## Effect Definition Builders

Rich visual configuration lives in focused builders without audience or timing.

Current builder roles:

```text
BukkitTitleEffectBuilder
BukkitBossBarEffectBuilder
BukkitParticleEffectBuilder
BukkitBlockProjectionEffectBuilder
BukkitFireworkEffectBuilder
```

A definition builder owns only the data required to describe that visual.

Example:

```java
BukkitTitleEffectBuilder overtimeTitle = new BukkitTitleEffectBuilder()
        .title(Component.text("OVERTIME"))
        .subtitle(Component.text("Next point wins"))
        .animation(EffectAnimationType.REVEAL);

BukkitBossBarEffectBuilder overtimeBar = new BukkitBossBarEffectBuilder()
        .name(Component.text("OVERTIME"))
        .progress(1.0F)
        .color(BossBar.Color.RED);
```

Definition builders must not own:

- audience selection;
- delay or absolute offset;
- scheduling;
- sequence lifecycle;
- module lifecycle;
- cleanup timing.

Do not add `at(...)`, `showAt(...)`, `delay(...)`, or similar timing methods to the effect-definition builders.

## Chronological Sequence Pattern

The sequence builder receives configured effect builders and owns all timing.

```java
BukkitTitleEffectBuilder overtimeTitle = new BukkitTitleEffectBuilder()
        .title(Component.text("OVERTIME"))
        .subtitle(Component.text("Next point wins"))
        .animation(EffectAnimationType.REVEAL);

BukkitBossBarEffectBuilder overtimeBar = new BukkitBossBarEffectBuilder()
        .name(Component.text("OVERTIME"))
        .progress(1.0F)
        .color(BossBar.Color.RED);

BukkitParticleEffectBuilder rune = BukkitParticleEffectBuilder
        .preset(EffectPresetType.GROUND_RUNE)
        .location(center);

getEffectSequenceHandler()
        .send(players)
        .bossBar(overtimeBar, 0)
        .sound(Sound.ENTITY_CREEPER_PRIMED, 1.0F, 0.8F, 0)
        .title(overtimeTitle, 1)
        .particle(rune, 1)
        .bossBar(overtimeBar.progress(0.5F), 3)
        .particle(EffectPresetType.ENERGY_RELEASE, center, 4)
        .bossBar(overtimeBar.progress(0.0F).name(Component.text("GO!")), 4)
        .hideBossBar(overtimeBar, 5)
        .start();
```

This code reads in timeline order. Effect builders describe state; the sequence describes when that state is sent.

## Snapshot Rule

When an effect builder is added to a sequence, the sequence snapshots its current definition immediately.

Therefore:

```java
sequence.bossBar(bar.progress(1.0F), 0);
sequence.bossBar(bar.progress(0.5F), 3);
```

creates two independent cue snapshots. Mutating `bar` for the second cue must not retroactively modify the first cue.

Stateful builder object identity only tells one sequence that later cues refer to the same live visual object.

## Stateful Visual Identity

Do not expose sequence-local key or reference classes to consumers for boss bars or block projections.

The consumer handle is the builder itself:

```text
BukkitBossBarEffectBuilder
BukkitBlockProjectionEffectBuilder
```

Internally, each `BukkitEffectSequenceBuilder` assigns state IDs by builder identity. Those IDs are:

- private to one sequence;
- not UUIDs;
- not Bukkit object identity;
- not database keys;
- not durable state;
- not cross-sequence addresses.

A builder reused in another sequence receives independent sequence-local state.

## Sequence Timing

- Every cue uses an absolute offset from sequence start.
- `0` is the first execution point.
- Seconds overloads are convenience methods over `Duration`.
- Cues with the same resolved tick execute in insertion order.
- Animated subframes belong to the sequence handle and are cancelled with it.
- Paper mutations execute on the Paper server thread.
- The sequence owner closes or cancels live handles during lifecycle teardown.

Timing belongs only to the sequence. An effect definition must remain reusable without knowing when it will be sent.

## Effect Categories

Effect identity, shape, animation, preset, and material selection use enums when behavior is finite and code-owned.

Native Paper types remain native:

```text
Particle
Sound
Material
BlockData
BossBar.Color
BossBar.Overlay
FireworkEffect
Color
```

Do not wrap Paper enums merely to create another translation layer.

## Custom Entity Boundary

Shared effect modules must not depend on the Novus/Kingdom custom-entity catalog or runtime.

The following do not belong in `minecraft-framework` effect contracts:

```text
LIGHT
PURPLE_CREEPER
Novus custom-entity IDs
custom-entity spawn/remove cues
custom-entity spawner/registry bridges
entity-rig animation state
```

A product or server module may coordinate its own custom-entity runtime beside a shared effect sequence. That composition does not make custom entities a parent-framework capability.

## Animation

Generic sequence animation is selected with `EffectAnimationType`.

Reusable animation mechanics remain in `BukkitEffectAnimationHandler`.

Current generic animation behavior:

```text
NONE
REVEAL
DRAW
EXPAND
CONTRACT
ROTATE
BUILD
DISSOLVE
```

`EffectAnimationSettings` carries duration and frame interval. It is part of the visual definition, while the cue's absolute offset remains part of the sequence.

## Geometry

Reusable effect geometry is Bukkit-free and produces relative `EffectVector` values.

Particle and block-projection rendering share the same sampler.

Current shapes:

```text
POINT
LINE
RAY
RING
ARC
SPIRAL
HELIX
SPHERE
DOME
CONE
CYLINDER
CUBOID
GRID
POLYGON
WAVE
VORTEX
BEZIER
```

`EffectGeometryRequest` owns radius, height/amplitude, length, point count, polygon side count, turn count, and Bézier control points.

Do not repurpose unrelated numeric fields as hidden shape-specific data.

## Typed Particle Data

Paper particle payloads use `BukkitParticleData` rather than caller-facing raw `Object` values.

Supported payload categories include:

```text
BlockData
Particle.DustOptions
Particle.DustTransition
Color
Particle.Trail
Float
Integer
Particle.Spell
```

Rules:

- no-data particles reject typed data;
- non-block particles reject material palettes;
- block-data particles require exactly one block-data source;
- typed data must match the native Paper particle payload class;
- validated rendering routes through `IBukkitEffectUtil`.

## Layered Presets

Generic reusable visual presets may live in the framework when they have no FFA, Kingdom, team, reward, punishment, or product meaning.

A preset may contain multiple particle layers. Each layer owns:

- native Paper particle type;
- geometry shape and request;
- optional typed particle data;
- optional material palette;
- default animation.

Product modules decide why and when the preset is sent.

## Client-Only State

Block projections and other view overrides never become gameplay truth.

A sequence owns temporary state it creates and restores it on cancellation. Block restoration reads current authoritative world `BlockData`.

Boss bars created by a sequence are hidden during sequence cleanup.

## Cleanup and Lifecycle

Cancelling or closing a sequence:

- cancels scheduled cue and animation tasks;
- hides sequence-owned boss bars;
- restores sequence-owned block projections;
- leaves authoritative gameplay state untouched.

Updating the same block-projection builder in one sequence restores the previous projection before rendering the new snapshot.

## Dependency Rule

No third-party particle or effect library is required.

Use Paper primitives, Tavall-owned geometry, the existing `IBukkit*Util` adapters, and the effect-sequence orchestration layer.

## Review Checklist

- [ ] One immediate platform operation uses the appropriate `IBukkit*Util`.
- [ ] Consumers use modern `DependencyAccess<...>` with named getters.
- [ ] The sequence handler resolves utilities through DI rather than constructing duplicate utilities.
- [ ] Actual sequence delivery enters through `getEffectSequenceHandler().send(...)`.
- [ ] Effect-definition builders contain no timing or audience state.
- [ ] Sequence calls read chronologically.
- [ ] Builder state is snapshotted when a cue is added.
- [ ] Stateful visuals use builder identity internally rather than public key/ref classes.
- [ ] Paper work stays on the server thread.
- [ ] Particle and block-projection renderers share geometry.
- [ ] Client-only state is restored on cancellation.
- [ ] Custom-entity ownership remains outside the shared framework.
- [ ] No third-party effect dependency was added.
- [ ] Gameplay meaning remains outside the framework.
