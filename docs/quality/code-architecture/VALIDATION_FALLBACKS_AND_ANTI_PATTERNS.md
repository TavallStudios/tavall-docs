# Tavall Validation, Fallbacks, and Anti-Patterns

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Validation Pattern

Validate before mutation. Validation should be typed, readable, and performed at the boundary that owns the invariant.

Bad:

```java
public void updateRank(String rankName) {
    if (rankName != null) {
        // mutate
    }
}
```

Good:

```java
public RankUpdateResult updatePlayerRank(
        RankUpdateRequest request
) {
    if (!getRankRegistry().contains(request.rankKey())) {
        return RankUpdateResult.invalidRank();
    }

    getRankDataHandler().updatePlayerRankData(request);
    return RankUpdateResult.success();
}
```

##### Why

Typed validation rejects invalid state before side effects begin and makes expected rejection explicit rather than leaving later storage/platform code to discover the problem accidentally.

## Fallback Pattern

Fallbacks are intentional, typed, visible, and owned. They must not convert failed required writes or violated invariants into fake success.

A presentation fallback may provide safe output for missing optional metadata. A durable write failure may not silently become “success with in-memory state.”

##### Why

A fallback changes failure semantics. If its ownership/reconciliation is not explicit, degraded behavior becomes an undocumented second source of truth.

# Anti-Patterns

## God Class

Bad:

```java
public final class ProjectCoreManager {
}
```

A god class owns unrelated domains, lifecycle, storage, routing, and presentation.

##### Why

Every change touches the same owner and tests must recreate unrelated systems. Split by real responsibility/lifecycle instead of adding forwarding wrappers.

## Manager Pattern

Avoid new `*Manager` classes unless maintaining an external established API that cannot be changed.

Use an exact role:

```text
RankUpdateHandler
RankRegistry
PlayerAccountDataHandler
PlayerRankMetaDataBuilder
FFARoundOrchestrator
```

##### Why

`Manager` does not state what the class owns. Exact suffixes give callers, reviewers, and architecture tests a contract.

## Helper Pattern

Avoid vague `*Helper`, `Common`, and `Misc` classes.

##### Why

They become junk drawers because the name provides no boundary for rejecting the next unrelated method.

## Static Dependency Access

Static syntax is not the problem. Static ownership/lookup of runtime behavior is.

Tavall-managed application dependencies resolve through the owning DI map.

Bad:

```java
public static IEconomyService economyService() {
    return DependencyLoaderAccess.findInstance(IEconomyService.class);
}
```

Allowed statics are dependency-free:

- constants/immutable constant values;
- pure parsing/normalization/transformation;
- private pure helpers;
- construction-only `of(...)`, `from(...)`, `builder()`, `create(...)` methods.

A static factory/builder must not resolve DI, perform I/O, touch mutable runtime state, schedule work, or become a hidden composition root.

##### Why

A static locator erases dependency ownership from the class declaration and bypasses replacement, generation, lifecycle, and test composition semantics.

## Application-Owned Mutable Map Pattern

Application-owned mutable keyed state is prohibited by default.

Bad:

```java
public final class PlayerSessionHandler {
    private final Map<UUID, PlayerSessionData> sessions =
            new ConcurrentHashMap<>();
}
```

Route state by semantics:

- runtime identity/session/definitions -> Tavall Registry;
- expiring/reloadable/disposable state -> Tavall Cache;
- durable state -> Tavall Database entity model/current entity contract;
- distributed runtime state -> owning Redis/distributed boundary;
- in-flight tasks/futures/retries -> dedicated typed operation/runtime owner;
- immutable value/snapshot -> typed data.

Full rule: [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md).

##### Why

A thread-safe map still has authority/lifecycle semantics. Putting it in an ordinary consumer silently makes that consumer the registry/cache/runtime/persistence owner.

## Direct Thread Ownership Pattern

Ordinary Tavall production application code must not create or own worker threads directly. Do not introduce application work through `new Thread(...)`, `Thread.startVirtualThread(...)`, `Thread.ofVirtual()`, `Thread.ofPlatform()`, or a feature-local executor merely to obtain a thread.

Use Tavall concurrency infrastructure for off-thread work and the owning platform scheduler for thread-affine platform mutation. The checked-in [`AsyncTask`](https://github.com/TavallStudios/TavallMonoRepo/blob/8d3891ec9620e008405f9367b80b0e5c7bd0ab34/tavall-java-tools/tavall-concurrency/src/main/java/org/tavall/internal/utils/concurrent/AsyncTask.java) implementation uses a virtual-thread-per-task executor and returns `CompletableFuture` from `runAsync`/`supplyAsync`.

#### Bad

```java
Thread workerThread = new Thread(this::runControlLoop, "region-control");
workerThread.start();
```

#### Good: Async work without retained completion

```java
AsyncTask.runAsync(() -> populationGateway.publishCurrentPopulation(
        playerCount,
        maximumPlayerCount
));
```

Project Novus production source [`FFARegionControlService`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/region/FFARegionControlService.java) routes off-thread work through `AsyncTask` and returns Bukkit-affine mutation to the Bukkit scheduler.

#### Good: Completion is part of the caller contract

```java
CompletableFuture<RoutingPlanData> routingFuture =
        AsyncTask.supplyAsync(this::loadRoutingPlanData);
```

Keep the `CompletableFuture<T>` only when the caller actually owns, chains, awaits, cancels, or records completion. Do not retain a future merely because `AsyncTask` returns one.

#### Allowed exceptional Thread API

Direct `Thread` creation is allowed only when a JVM/platform/integration API structurally requires a `Thread` object or canonical concurrency infrastructure itself owns thread construction. The reason and lifecycle must be explicit.

Project Novus production source [`NovusDiscordCoreApplication`](https://github.com/TavallStudios/tavall-project-novus/blob/main/novus-discord/novus-discord-core/src/main/java/org/tavall/discord/core/NovusDiscordCoreApplication.java) constructs a `Thread` specifically because `Runtime.addShutdownHook(...)` requires one; the JVM owns when that hook starts. Tavall concurrency infrastructure may likewise use `Thread.ofVirtual()` internally to implement the shared abstraction.

`Thread.currentThread()` inspection, interrupt restoration, and equivalent operations on the already-owning thread are not thread creation and are not prohibited by this rule.

##### Why

Direct thread creation bypasses Tavall concurrency ownership, virtual-thread policy, observability, and future resource balancing. Centralizing creation lets application code express work while infrastructure owns how that work receives CPU time.

## Raw String Pattern

Bad:

```java
permissionHandler.has(player, "punishment.ban");
```

Good:

```java
permissionHandler.has(player, PermissionNode.PUNISHMENT_BAN);
```

##### Why

Typed keys are searchable/refactorable and let the compiler reject category mistakes. Raw strings compile typos with tremendous confidence.

## Hidden Side Effect Pattern

A method name must not hide unrelated mutation.

Bad:

```java
public PlayerAccountData getPlayerAccountData(UUID playerUUID) {
    PlayerAccountData data = load(playerUUID);
    cache.put(playerUUID, data);
    tabHandler.refresh(playerUUID);
    return data;
}
```

Prefer explicit actions with honest names and owners.

##### Why

Callers reason from method contracts. Hidden cache/presentation/persistence effects turn innocent reads into workflows and make retry/error behavior impossible to infer.

## Repository Type Pattern

New Tavall-owned production declared types ending in `Repository` are prohibited.

#### Bad

```text
PlayerRepository
IPlayerRepository
PostgresPlayerRepository
PlayerRepositoryAdapter
```

#### Good

Name the behavior that actually exists, such as a `PlayerDataHandler`, `PlayerHistoryWriter`, `AccountLinkGateway`, or another precise capability. Ordinary durable entity persistence follows Tavall Database entity classes and the current checked-in Tavall Database contract without a new application Repository layer.

##### Why

`Repository` repeatedly recreated a generic persistence wrapper and kept obsolete mechanics alive. The ban forces persistence behavior either into Tavall Database or into a precisely named capability with real semantics.

## JPA Callback Ownership Pattern

Production application code must not own:

```text
EntityManager
EntityTransaction
IPostgresJpaContext callbacks
database.jpa().read(...)
database.jpa().write(...)
raw JDBC transaction wrappers
```

Use Tavall Database entity classes and the entity persistence contract defined by the checked-in module. Add missing multi-entity operations upstream to Tavall Database instead of recreating callbacks downstream.

##### Why

Transaction/entity-manager lifecycle is infrastructure-wide ownership. Local callback wrappers reproduce the persistence runtime inside feature code.

## Review Checklist

- [ ] Validation occurs before mutation where possible.
- [ ] Fallbacks have explicit ownership/reconciliation and never fake required-write success.
- [ ] No God/Manager/Helper bucket hides unrelated behavior.
- [ ] Static methods do not locate Tavall-managed runtime dependencies.
- [ ] Mutable keyed state has Registry/Cache/Tavall Database/distributed/runtime ownership.
- [ ] Worker/concurrent application work uses Tavall concurrency or an owning platform scheduler rather than direct Thread creation.
- [ ] Any direct Thread construction has an explicit JVM/platform/infrastructure reason and lifecycle owner.
- [ ] Stable keys/values use typed representations rather than raw strings/maps.
- [ ] Method names disclose side effects.
- [ ] No new Tavall-owned production type ends in `Repository`.
- [ ] Application code owns no JPA callbacks/JDBC transaction lifecycle.
