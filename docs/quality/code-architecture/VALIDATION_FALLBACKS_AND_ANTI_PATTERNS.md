# Project Novus Validation, Fallbacks, and Anti-Patterns

> **Status:** Active  
> **Authority:** Supporting chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Validation boundaries, fallback behavior, runtime recovery, and prohibited implementation patterns

The binding Project Novus validation and anti-pattern rules live directly in [`CODE_ARCHITECTURE.md`](../CODE_ARCHITECTURE.md#validation-and-failure-contracts) and [`CODE_ARCHITECTURE.md`](../CODE_ARCHITECTURE.md#anti-patterns). This chapter owns detailed examples and boundary guidance.

## Validation Boundary Pattern

Validate input at the boundary that first owns its meaning.

A parser validates syntax. A resolver validates lookup success. A domain handler validates domain invariants. A repository validates persistence-specific constraints. A consumer must not duplicate every downstream validation rule preemptively.

Validation should produce a typed expected outcome when rejection is part of normal control flow. Throw only when the caller violated a programming contract or the system cannot continue coherently.

## Fallback Ownership Pattern

Fallback behavior must have one owner and one explicit trigger.

Do not scatter fallback selection across callers. If several consumers independently decide when to use a secondary provider, stale snapshot, compatibility implementation, or default value, the fallback policy has no real owner.

A fallback owner should expose the domain operation rather than the fallback mechanism:

```java
public interface IPlayerProfileResolver {
    PlayerProfileResult resolve(PlayerProfileRequest request);
}
```

The implementation may attempt the primary source and then an approved fallback. Callers consume the result without reconstructing that policy.

## Expected Failure Pattern

Expected rejection should use typed results when the caller needs to distinguish outcomes.

```java
public record PurchaseResult(
        PurchaseStatus status,
        PurchaseReceiptData receipt
) {
}
```

Avoid returning `null`, magic strings, or unrelated exceptions for normal domain rejection such as insufficient balance, disabled feature, unavailable target, stale request, or missing optional data.

## Degraded Runtime Pattern

A subsystem may continue in degraded mode only when the degraded behavior is explicitly safe and observable.

Required properties:

- the degraded state has a defined owner;
- the trigger is logged or surfaced through operational state;
- the fallback cannot silently violate persistence, security, authorization, or ordering guarantees;
- recovery behavior is defined;
- callers do not need to guess whether the subsystem is degraded.

## Anti-Patterns

### God Class Pattern

A class that owns unrelated state, orchestration, persistence, formatting, scheduling, and integration behavior is not "centralized." It is several systems wearing one filename.

Split by real ownership boundaries. Do not split mechanically into equally arbitrary helper classes.

### Manager Pattern

Do not use `*Manager` as a generic suffix for a class that "does things."

Choose the name from the actual role:

- `*Handler` for focused behavior;
- `*Service` for a coherent reusable capability;
- `*Orchestrator` for multi-step coordination;
- `*Router` for selection/delegation;
- `*Registry` for keyed runtime ownership;
- `*Cache` for disposable or expiring fast state;
- `*Repository` for durable persistence;
- `*Builder` for constructing typed values;
- `*Resolver` for selecting or deriving a typed answer.

### Helper Pattern

A `*Helper` class is a design-review signal because it usually means behavior has not been assigned to an owner.

Pure stateless utilities may use a narrow utility name when the functions truly have no lifecycle, state, replacement, or domain owner. Runtime behavior belongs on a DI-managed boundary.

### Static Dependency Access Pattern

Static methods must not resolve or hide Tavall-managed runtime dependencies.

Bad:

```java
public static PlayerProfile load(UUID playerId) {
    return DependencyLoaderAccess
            .findInstance(IPlayerProfileService.class)
            .load(playerId);
}
```

Use a Tavall-managed consumer that declares the dependency through the approved DI access surface.

Runtime utility behavior should normally remain an injected instance dependency. Static methods are reserved for pure helpers, immutable constants, and value/factory construction that does not resolve services, perform I/O, own mutable state, or participate in lifecycle behavior.

When behavior needs replacement, lifecycle ownership, runtime configuration, deterministic testing, or access to Tavall-managed state, route it through DI.

#### Application-Owned Mutable Map Pattern

Application-owned mutable maps are prohibited by default.

The problem is not that Java has a `Map` type. The problem is ordinary application code owning keyed mutable state that should belong to Tavall Registry, Tavall Cache, persistence, distributed-state infrastructure, or a typed operation/data boundary.

This includes `Map`, `ConcurrentMap`, `HashMap`, `ConcurrentHashMap`, mutable `Set`, and parallel keyed collections used for domain state.

The detailed binding rule lives in [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md), where the rule is explained alongside linked production code from the owning repositories.

Bad:

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

That is a registry implemented inside a consumer. Use a typed Registry through DI instead.

Likewise, expiring/reloadable keyed state belongs in Tavall Cache, durable state belongs behind Repository/Data Handler ownership, and short-lived operation values should be typed `*Data`, `*Request`, `*Result`, `*State`, or `*MetaData` rather than generic maps.

Infrastructure implementations may use maps internally. Ordinary consumers do not own or expose those backing collections.

### Raw String Pattern

Do not use raw strings for stable domain concepts when a typed key, enum, identifier, or value object exists.

Bad:

```java
if (type.equals("ranked")) {
    ...
}
```

Prefer a typed value whose legal states and comparisons are explicit.

### Hidden Side Effect Pattern

A method whose name implies lookup, formatting, validation, or calculation must not secretly persist data, schedule work, mutate unrelated state, or publish network effects.

If the side effect is necessary, name the operation accordingly or move the effect to the owner that is responsible for it.

## Review Questions

Before accepting fallback or recovery behavior, ask:

- Who owns the primary operation?
- Who owns the fallback decision?
- Is the fallback safe for persistence and security semantics?
- Can callers distinguish expected rejection from system failure?
- Is degraded mode observable?
- Is recovery defined?
- Does any consumer recreate fallback policy locally?
- Does any consumer own mutable keyed state that should be Registry, Cache, Repository, distributed state, or typed operation data?
