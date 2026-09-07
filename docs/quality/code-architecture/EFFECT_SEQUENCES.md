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

##### Why

A sequence introduces scheduling, lifecycle, state identity, and cleanup that an immediate utility call does not need. Using the sequence layer for every presentation operation would turn simple platform adaptation into a durable workflow for no architectural benefit.

The utility-first split keeps one-shot effects cheap and predictable while reserving sequence ownership for behavior that actually needs coordinated time or cleanup.

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

##### Why

Effect delivery is runtime behavior with the same replacement and module-generation semantics as the rest of the application. Capturing or constructing utility implementations locally creates a second ownership path that can outlive or disagree with the DI-managed instance.

Using generated access keeps presentation behavior attached to the same lifecycle and substitution rules as every other managed dependency.

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

##### Why

One delivery entry point gives audience ownership and sequence construction a single predictable shape. Competing entry points tend to diverge in validation, lifecycle registration, defaults, and cleanup even when they initially look equivalent.

A stable fluent contract also keeps generated examples and review tooling from having to infer which of several aliases is the real lifecycle boundary.

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

##### Why

A reusable visual definition should mean the same thing regardless of who sees it or when it is sent. Adding audience and timing to the definition couples presentation data to one delivery workflow and makes the same visual harder to reuse in another sequence.

Separating definition from delivery also prevents builders from becoming hidden schedulers whose lifecycle cannot be inferred from the object they return.

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

##### Why

Timing is easier to review when the source order resembles the user-visible timeline. Splitting offsets across nested builders or delayed callbacks forces readers to reconstruct the chronology mentally and makes insertion-order behavior difficult to reason about.

One sequence owner also provides a natural place for cancellation, same-tick ordering, and lifecycle teardown across every cue in the workflow.

## Snapshot Rule

When an effect builder is added to a sequence, the sequence snapshots its current definition immediately.

Therefore:

```java
sequence.bossBar(bar.progress(1.0F), 0);
sequence.bossBar(bar.progress(0.5F), 3);
```

creates two independent cue snapshots. Mutating `bar` for the second cue must not retroactively modify the first cue.

Stateful builder object identity only tells one sequence that later cues refer to the same live visual object.

##### Why

A timeline is a record of intended states at specific offsets. If later builder mutation can rewrite earlier cues, the timeline depends on future calls and becomes impossible to inspect reliably at construction time.

Snapshotting preserves temporal intent while still allowing builder identity to express that several snapshots update the same sequence-local visual.

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

##### Why

Sequence-local identity exists only to correlate cues inside one running presentation. Publishing that identity as a durable-looking key invites callers to store it, compare it across sequences, or treat it as application state even though it has no meaning outside the sequence owner.

Builder identity gives consumers the minimum handle they need while keeping internal correlation private and disposable.

## Sequence Timing

- Every cue uses an absolute offset from sequence start.
- `0` is the first execution point.
- Seconds overloads are convenience methods over `Duration`.
- Cues with the same resolved tick execute in insertion order.
- Animated subframes belong to the sequence handle and are cancelled with it.
- Paper mutations execute on the Paper server thread.
- The sequence owner closes or cancels live handles during lifecycle teardown.

Timing belongs only to the sequence. An effect definition must remain reusable without knowing when it will be sent.

##### Why

Absolute offsets make cue placement independent of the duration or failure of neighboring effects. Relative chains compound timing changes and make inserting one cue unexpectedly shift every later cue.

Keeping timing on one owner also lets task cancellation and Paper-thread execution be enforced consistently rather than delegated to each individual effect definition.

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

##### Why

Typed Tavall enums are valuable when Tavall owns the finite behavior set. Native Paper types already have a stable contract and wrapping them only adds conversion code, duplicate naming, and another place for versions to drift.

The type boundary should exist where ownership changes, not wherever an additional enum can technically be invented.

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

##### Why

Framework effects are reusable presentation primitives; custom entities carry product-specific identity, lifecycle, and gameplay meaning. Pulling the entity runtime into the shared effect contract would reverse that dependency and force generic presentation code to know about one product's catalog.

Keeping the boundary clean lets mode modules orchestrate both systems without making either system own the other.

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

##### Why

Geometry describes mathematical shape, not Paper rendering. Keeping the sampler platform-free allows particles, block projections, previews, tests, and future renderers to share one definition without duplicating shape math.

Typed geometry parameters also prevent one generic numeric field from quietly meaning radius for one shape, turns for another, and some third mystery value by Friday.

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

##### Why

Particle payload requirements vary by native particle type, and raw `Object` pushes those rules to runtime casts scattered across callers. A typed payload boundary centralizes validation and makes invalid combinations visible before Paper receives them.

That keeps rendering failures deterministic instead of relying on whichever caller most recently guessed the correct payload class.

## Layered Presets

Generic reusable visual presets may live in the framework when they have no FFA, Kingdom, team, reward, punishment, or product meaning.

A preset may contain multiple particle layers. Each layer owns:

- native Paper particle type;
- geometry shape and request;
- optional typed particle data;
- optional material palette;
- default animation.

Product modules decide why and when the preset is sent.

##### Why

A shared preset is reusable only while it describes appearance rather than product meaning. Once a preset encodes “victory,” “punishment,” a team, or a specific mode concept, the framework becomes responsible for semantics owned by a higher-level module.

Keeping presets visual-only lets products reuse the same presentation vocabulary while retaining authority over why the effect occurs.

## Client-Only State

Block projections and other view overrides never become gameplay truth.

A sequence owns temporary state it creates and restores it on cancellation. Block restoration reads current authoritative world `BlockData`.

Boss bars created by a sequence are hidden during sequence cleanup.

##### Why

Client-only visuals are projections over authoritative server state. Treating them as truth would let a preview, tutorial, or animation overwrite gameplay assumptions that other systems rely on.

Explicit restoration also prevents temporary presentation from surviving after the workflow that created it has ended.

## Cleanup and Lifecycle

Cancelling or closing a sequence:

- cancels scheduled cue and animation tasks;
- hides sequence-owned boss bars;
- restores sequence-owned block projections;
- leaves authoritative gameplay state untouched.

Updating the same block-projection builder in one sequence restores the previous projection before rendering the new snapshot.

##### Why

Scheduling and client-only state create resources even when no Java object requires `close()` in the traditional sense. Without one cleanup owner, cancelled matches, module unloads, or disconnected workflows can leave tasks and visuals alive after their domain context is gone.

Sequence-owned cleanup gives every temporary effect the same lifecycle as the sequence that created it.

## Dependency Rule

No third-party particle or effect library is required.

Use Paper primitives, Tavall-owned geometry, the existing `IBukkit*Util` adapters, and the effect-sequence orchestration layer.

##### Why

The current stack already owns the primitives, geometry, scheduling, and cleanup behavior the system needs. Adding another effect runtime would duplicate lifecycle and rendering abstractions while introducing version and dependency risk for behavior Tavall already controls.

A dependency is justified when it adds a capability we do not reasonably own, not merely because an effect library exists and has impressive particles in its README.

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