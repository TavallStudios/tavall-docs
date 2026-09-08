# Tavall Namespaces, Variables, OOP, DRY, and Type Safety

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Namespaces and Class Names

Package and class names communicate ownership before anyone opens the file.

### Package Rules

- Prefer domain + purpose over short vague buckets.
- Package ownership follows the system/domain that owns the behavior.
- Avoid broad new packages such as `manager`, `misc`, `common`, or generic `util`.
- Shared utilities belong in shared utility packages only when they are genuinely shared and focused.
- Platform-specific code remains beneath the platform boundary that owns it.

Examples:

```text
org.tavall.api.minecraft.backend.message.format.placeholder
org.tavall.api.minecraft.backend.rank.permission.power
org.tavall.api.minecraft.backend.account.data.handler
```

##### Why

Packages are navigation and dependency signals. A vague package saves a few characters today and turns future maintenance into a scavenger hunt conducted by imports.

### Class Naming

Names identify both subject and role:

```text
PlayerRankMetaDataHandler
ChatFormatPlaceholderResolver
PlayerAccountDataBuilder
AchievementListRegistry
PlayerAchievementCache
FFARoundOrchestrator
```

Role expectations:

- `Handler`: focused domain behavior/operation family.
- `DataHandler`: reusable domain data policy when one is needed.
- `Builder`: constructs typed output only.
- `MetaDataBuilder`: constructs metadata values.
- `MetaDataHandler`: derives/refreshes/enriches metadata behavior.
- `Registry`: owns keyed runtime lookup state.
- `Cache`: owns disposable/expiring fast-access state.
- `Service`: cohesive reusable domain capability shared by consumers.
- `Orchestrator`: ordered cross-boundary workflow/lifecycle coordination.
- `Repository`: prohibited for new Tavall-owned production declared types; existing names are shrinking migration debt only.
- `Util`: focused pure/stateless helper, or a clearly named DI-managed platform adapter where the existing utility convention applies.

Do not use generic application `*Database` classes as the normal persistence role. Tavall Database owns ordinary PostgreSQL/JPA persistence mechanics. Do not replace them with a new `*Repository` layer.

##### Why

Precise suffixes give reviewers and architecture tests a usable contract. `Service` is about reusable capability, not how many minutes the object stays alive, and `Repository` no longer exists as an approved Tavall application role.

## Variables and Fields

### Local Variables

Extract important domain values into named locals when it improves reading, debugging, validation, or failure diagnosis.

#### Bad

```java
var currentPlan = populationGateway.routingPlan(serverData.getServerId());
var destination = populationGateway.snapshot(offer.destination().serverId());
var target = destination.get();
var valid = target.online() && target.spareCapacity() > 0;
```

#### Good

```java
Optional<FFARegionRoutingPlan> currentPlan =
        populationGateway.routingPlan(serverData.getServerId());
Optional<FFARegionServerSnapshot> destination =
        populationGateway.snapshot(offer.destination().serverId());
FFARegionServerSnapshot target = destination.get();
boolean valid = target.online() && target.spareCapacity() > 0;
```

Project Novus production source [`FFARegionControlService`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/FFARegionControlService.java) uses explicit local types across routing, snapshot, candidate, state, and validation flows.

Production Tavall Java code under `src/main/java` uses explicit local variable types. Do not use Java `var` in production source, including loop variables, generic results, builder results, DI-backed values, entity/data values, optionals, collections, or operation results.

Tests, fixtures, generated source, and tooling may define narrower rules independently; this production rule does not silently expand into those surfaces.

Naming rules:

- names describe domain meaning, not merely Java type;
- preserve established acronym capitalization such as `playerUUID`, `nativeUI`, `httpRequest`, `jsonPayload`;
- avoid numbered locals unless the number is domain meaning;
- avoid one-letter names outside tiny conventional scopes;
- do not reuse one local for several meanings.

##### Why

`var` keeps compiler type safety but removes type visibility from source. Explicit locals keep domain and API boundaries obvious in reviews and make type-changing refactors surface at the use site.

### Fields

Class fields represent owned state, immutable values, externally owned handles, or Tavall-managed dependency-access metadata according to the owning architecture.

Rules:

- fields are `private` unless a framework requires another visibility;
- immutable owned state is `final`;
- mutable state has one clear owner and documented concurrency/lifecycle behavior;
- public mutable static state is prohibited;
- static state must not become a hidden dependency graph, cache, registry, service locator, or persistence layer;
- keyed runtime state belongs in Tavall Registry/Cache or a dedicated typed runtime owner;
- durable state belongs through Tavall Database or another explicitly selected durable provider;
- Tavall-managed collaborators are resolved through Tavall DI rather than constructor-captured fields in ordinary managed behavior classes.

##### Why

A field is long-lived relative to a method. Putting mutable keyed or managed dependency state there implicitly declares lifecycle ownership, whether the author intended to or not.

## Constants

Use constants for stable code-owned values.

- `UPPER_SNAKE_CASE`.
- Prefer typed keys/enums/definitions over raw string collections.
- Operator-tuned values belong in configuration/persisted definitions when they are not code invariants.
- Time values include units or use `Duration`.
- Permission/message/resource/config keys have one typed owner.
- Never store secrets/credentials/protected tokens/environment endpoints in constants.

##### Why

Constants should encode real code invariants, not freeze operational configuration or sensitive runtime state into source because typing a literal twice felt emotionally unacceptable.

# OOP

Objects represent real concepts with clear ownership/responsibility. Avoid vague static bags of domain logic.

Bad:

```java
public final class PlayerUtils {
    public static boolean canPunish(PermissionProfile staff, PermissionProfile target) {
        return staff.powerLevel() > target.powerLevel();
    }
}
```

Good:

```java
@DelegatesTo(IPowerLevelHandler.class)
public final class PowerLevelHandler implements IPowerLevelHandler {
    @Override
    public boolean canPunish(
            PermissionProfile staff,
            PermissionProfile target
    ) {
        return staff.powerLevel() > target.powerLevel();
    }
}
```

##### Why

The permission rule has a named domain owner and can participate in DI/testing/replacement. A vague static utility hides the rule among unrelated convenience methods.

# DRY

DRY means **shared rules** should have one owner. It does not mean every similar-looking line must be abstracted.

### Bad Duplication: Same Rule, Several Owners

If Ban and Mute commands each implement the same power comparison, the authority rule is duplicated.

Good ownership:

```java
boolean canPunish = getPowerLevelHandler().canPunish(
        staffProfile,
        targetProfile
);
```

Each input adapter calls the same domain rule through its DI-managed boundary.

##### Why

When one rule changes, one owner changes. Commands adapt input/result; they do not each become a second permission engine.

### Bad DRY: Forced Abstraction

Two messages or flows that currently look similar may evolve for different reasons.

Prefer separate typed message keys:

```java
messageResolver.resolve(PunishmentMessageKey.BAN_APPLIED, placeholders);
messageResolver.resolve(PunishmentMessageKey.MUTE_APPLIED, placeholders);
```

over a generic helper that accepts arbitrary action strings and forces unrelated semantics into one method.

##### Why

Fake reuse couples systems that only resemble each other today. A little duplication is cheaper than the wrong abstraction plus the meetings required to remove it later.

# Type Safety

Prefer typed keys, enums, IDs, requests, results, and domain values over raw strings/magic numbers.

Bad:

```java
messageResolver.resolve("chat.player.format");
permissionHandler.has(player, "punishment.ban");
```

Good:

```java
messageResolver.resolve(ChatMessageKey.PLAYER_FORMAT);
permissionHandler.has(player, PermissionNode.PUNISHMENT_BAN);
```

##### Why

Typed values are searchable/refactorable and let the compiler reject invalid categories. Raw strings happily compile typos and wait until production to become interesting.

# Review Checklist

- [ ] Packages describe domain + role rather than broad buckets.
- [ ] Class suffixes match current Tavall role definitions.
- [ ] Services represent reusable cohesive capabilities, not merely long-lived objects.
- [ ] No new Tavall-owned production type ends in `Repository`.
- [ ] Generic application `*Database` wrappers are not introduced as a replacement persistence layer.
- [ ] Production locals use explicit Java types rather than `var`.
- [ ] Fields have explicit state/lifecycle ownership.
- [ ] Tavall-managed dependencies are not constructor-captured in ordinary managed behavior.
- [ ] Constants represent code invariants rather than operational secrets/configuration.
- [ ] Shared rules have one domain owner without forced abstraction.
- [ ] Stable domain keys/values are typed instead of raw strings/magic values.
