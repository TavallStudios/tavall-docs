# Tavall Minecraft Effect Sequence Architecture

> **Status:** Active  
> **Authority:** Binding Minecraft presentation specialization of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall Minecraft modules using reusable Paper/Bukkit presentation utilities, timing, animation, particles, client-only views, and cleanup

Effect sequences coordinate reusable presentation utilities. They do not replace the utility layer, message resolution, gameplay handlers, custom-entity runtimes, or authoritative state.

## Utility-First Rule

Use the existing `IBukkit*Util` surface for one immediate platform operation.

Use the effect-sequence layer only when behavior needs one or more of:

- several presentation surfaces coordinated together;
- absolute timing;
- reusable effect definitions;
- animation frames;
- sequence-owned cleanup;
- stateful visual updates such as one boss bar changing over a timeline.

Do not route every sound, particle, title, or fake block through a sequence merely because the sequence API exists.

##### Why

A sequence introduces scheduling, lifecycle, state identity, and cleanup that an immediate utility call does not need. The split keeps one-shot effects cheap/predictable and reserves sequence ownership for coordinated time/state.

## DI Access

Consumers and the sequence handler resolve managed utilities through Tavall DI with `DependencyAccess<...>`.

```java
public final class MatchPresentationHandler
        implements DependencyAccess<
                IBukkitEffectUtil,
                IBukkitEffectSequenceHandler
        > {

    public void show(MatchPresentationRequest request) {
        IDependencyMap dependencies = getInstance();
        dependencies.iBukkitEffectUtil();
        dependencies.iBukkitEffectSequenceHandler();
    }
}
```

Do not constructor-capture managed utility implementations or instantiate replacement utilities with `new Bukkit*Util()`.

##### Why

Effect delivery is runtime behavior with replacement/module-generation semantics. Local construction or captured instances create a second ownership path that can outlive or disagree with the DI-managed instance.

## Delivery Entry Point

Actual sequence delivery enters through the owning sequence handler:

```java
getEffectSequenceHandler().send(players)
```

or:

```java
getEffectSequenceHandler().send(player)
```

The terminal operation remains `.start()` unless the owning API intentionally changes its canonical contract.

Do not add parallel aliases such as `.to(...)` or `effects.play(...)` that duplicate delivery ownership.

##### Why

One entry point gives audience ownership, defaults, lifecycle registration, and cleanup one predictable path.

## Effect Definition Builders

Focused builders describe one visual definition without audience or absolute sequence timing.

Examples:

```text
BukkitTitleEffectBuilder
BukkitBossBarEffectBuilder
BukkitParticleEffectBuilder
BukkitBlockProjectionEffectBuilder
BukkitFireworkEffectBuilder
```

A definition builder owns only data required to describe the visual.

It must not own:

- audience selection;
- delay/absolute offset;
- scheduling;
- sequence/module lifecycle;
- cleanup timing;
- Tavall-managed dependency lookup.

##### Why

A reusable visual definition should mean the same thing regardless of who sees it or when it is sent. Audience/timing belongs to the workflow that delivers the definition.

## Chronological Sequence Pattern

The sequence receives configured definitions and owns all timing.

```java
getEffectSequenceHandler()
        .send(players)
        .bossBar(overtimeBar, 0)
        .sound(Sound.ENTITY_CREEPER_PRIMED, 1.0F, 0.8F, 0)
        .title(overtimeTitle, 1)
        .particle(rune, 1)
        .bossBar(overtimeBar.progress(0.5F), 3)
        .particle(EffectPresetType.ENERGY_RELEASE, center, 4)
        .hideBossBar(overtimeBar, 5)
        .start();
```

Calls read in timeline order. Effect builders describe state; the sequence describes when that state is sent.

##### Why

A visible timeline is easier to review than delays distributed through nested callbacks/builders. One sequence owner also provides cancellation and same-tick ordering.

## Snapshot Rule

When a definition builder is added to a sequence, snapshot its current definition immediately.

```java
sequence.bossBar(bar.progress(1.0F), 0);
sequence.bossBar(bar.progress(0.5F), 3);
```

creates independent cue snapshots. Mutating `bar` for a later cue must not rewrite the earlier cue.

##### Why

A timeline is a record of intended states at specific offsets. If future builder mutation rewrites earlier cues, the timeline cannot be understood at construction time.

## Stateful Visual Identity

Do not expose sequence-local keys/reference classes as durable-looking public concepts for boss bars/block projections.

The builder/definition object may act as the consumer handle while the sequence assigns private local identity.

Sequence-local IDs are:

- private to one sequence;
- not durable UUIDs/database keys;
- not cross-sequence addresses;
- not authoritative application state.

##### Why

Sequence-local identity exists only to correlate cues inside one presentation. Publishing it invites callers to store/compare it outside the lifecycle where it has meaning.

## Sequence Timing

- Every cue uses an absolute offset from sequence start.
- `0` is the first execution point.
- Seconds overloads may delegate to `Duration`.
- Cues resolving to the same tick execute in insertion order.
- Animated subframes belong to the sequence handle and cancel with it.
- Paper mutations execute on the required Paper thread.
- The owner closes/cancels live handles during lifecycle teardown.

##### Why

Absolute offsets make cue placement independent of neighboring effect duration. Relative chains compound timing changes and make insertion unexpectedly shift every later cue.

## Native Types and Effect Categories

Use Tavall enums for finite Tavall-owned behavior categories such as animation/presets/shapes.

Keep native Paper types native when Tavall does not own a competing semantic layer:

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

##### Why

Type boundaries should exist where ownership changes. Wrapping Paper enums merely creates conversion code and another version-drift surface.

## Custom Entity Boundary

Shared effect contracts do not depend on product-specific custom-entity catalogs/runtimes.

A product/module may orchestrate a custom-entity runtime beside a shared effect sequence, but that composition does not make custom entities a parent-framework capability.

##### Why

Framework effects are reusable presentation primitives; custom entities carry product-specific identity/lifecycle/gameplay meaning. Pulling product catalogs into the framework reverses the dependency.

## Animation and Geometry

Reusable generic animation mechanics remain in a focused animation handler/capability. Animation settings belong to the visual definition while cue offset remains sequence-owned.

Reusable effect geometry is platform-light/Bukkit-free where practical and produces relative vectors consumed by particle/block-projection renderers.

Shapes may include:

```text
POINT LINE RAY RING ARC SPIRAL HELIX SPHERE DOME CONE
CYLINDER CUBOID GRID POLYGON WAVE VORTEX BEZIER
```

Do not repurpose unrelated numeric fields as hidden shape-specific data.

##### Why

Geometry is mathematical shape, not Paper rendering. Sharing one sampler avoids duplicated shape math while typed parameters stop one magic number from meaning radius, turns, and some third mystery value depending on enum choice.

## Typed Particle Data

Caller-facing particle payloads use a typed boundary rather than raw `Object` values.

Validate:

- whether the particle accepts data;
- native payload type compatibility;
- block-data/material requirements;
- mutually exclusive data sources;
- rendering through the owning Bukkit effect utility.

##### Why

Paper particle payload requirements vary by particle type. Raw `Object` pushes casts/validation into callers and makes invalid combinations runtime surprises.

## Layered Presets

Shared framework presets remain product-neutral visual definitions. They may contain multiple particle layers with native particle type, geometry, optional typed data/material palette, and default animation.

Product modules decide why/when the preset is sent.

##### Why

A shared preset remains reusable only while it describes appearance rather than “victory,” “punishment,” team identity, reward identity, or one mode's semantics.

## Client-Only State

Block projections, fake equipment, fake health/experience, per-viewer weather/time, and other view overrides never become gameplay truth.

The sequence/workflow restores temporary state during cancellation/close. Block restoration reads current authoritative world state rather than assuming the original state is still correct.

##### Why

Client-only visuals are projections over authoritative server state. Treating them as truth lets previews/tutorials/animations overwrite gameplay assumptions and leaves stale views after the workflow ends.

## Cleanup and Lifecycle

Cancelling/closing a sequence:

- cancels scheduled cues/animation tasks;
- hides sequence-owned boss bars;
- restores sequence-owned client-only block/view state;
- leaves authoritative gameplay state untouched.

Updating the same block-projection handle restores/reconciles the previous projection before rendering the new snapshot where required.

##### Why

Scheduling and client-only state create resources even when no traditional Java resource is open. Without one cleanup owner, cancelled matches/module unloads can leave tasks and visuals alive after their domain context disappears.

## Dependency Rule

Do not add a third-party effect runtime merely to reproduce capabilities already owned by Paper primitives, Tavall geometry, `IBukkit*Util` adapters, and the effect-sequence layer.

##### Why

A new runtime duplicates scheduling/render/lifecycle abstractions and adds version/dependency risk. Add a dependency when it provides a capability Tavall does not reasonably own, not because its README has impressive particles.

## Review Checklist

- [ ] Immediate one-shot operations use the appropriate `IBukkit*Util`.
- [ ] Managed utilities/sequence handlers resolve through Tavall DI.
- [ ] Effect definitions contain no audience/absolute timing/dependency lookup.
- [ ] Sequence calls read chronologically.
- [ ] Cue definitions snapshot at insertion.
- [ ] Stateful visual identity stays sequence-local.
- [ ] Paper work runs on the required thread.
- [ ] Particle/block projection share reusable geometry where appropriate.
- [ ] Particle data is typed/validated.
- [ ] Client-only state restores on cancellation/close.
- [ ] Product/custom-entity meaning remains outside shared framework contracts.
- [ ] No duplicate third-party effect runtime is added without a real capability need.
