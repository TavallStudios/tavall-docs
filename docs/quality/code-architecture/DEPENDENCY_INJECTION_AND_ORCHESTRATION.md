# Tavall Dependency Injection and Orchestration

> **Status:** Active  
> **Authority:** Binding specialization of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall DI-managed modules, runtime composition, lifecycle cleanup, consumers, and orchestration

This chapter owns detailed Tavall DI access, managed registration, default-consumer, orchestration, and cleanup rules. Read the root architecture first: [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md).

> **Governing Doctrine:** Tavall-owned behavior is interface-first and DI-managed by default.
>
> Ordinary consumers depend on contracts and access dependencies via typed `DependencyAccess<...>`.
> `IDependencyMap` and `DependencyMap` are **DI infrastructure**; ordinary consumers MUST NOT interact with them directly.

When a DI-managed consumer also touches durable persistence, Registry/Cache state, mutable keyed state, Handler behavior, or another delegated topic, the corresponding specialized chapter is also required. This chapter does not redefine those boundaries.

## Managed Registration

A managed concrete implementation registers one object identity under its concrete token and every declared interface alias.

```java
@DelegatesTo(IMessageRenderHandler.class)
public final class MessageRenderHandler
        implements IMessageRenderHandler,
        DependencyAccess<IMessageRegistryHandler> {
}
```

Registration rules:

- concrete token is implicit where the checked-in Tavall DI version provides it;
- each delegated type is assignable from the concrete;
- aliases share one metadata/instance owner;
- replacement/removal updates aliases atomically;
- new code does not add legacy injectable marker interfaces merely to satisfy old composition paths.

##### Why

Interface and concrete aliases must describe one owned dependency, not parallel instances that happen to implement the same contract. Shared metadata preserves replacement, cleanup, and identity regardless of token used by the consumer.

## Module and Generation Lookup

Generation-owned dependencies resolve from the owning module `IDependencyMap`. Stable parent/application dependencies may be available through explicitly defined parent composition, but child-generation objects must not be leaked into a process-global loader.

Rules:

- module generations own isolated dependency maps;
- child-generation dependencies stay in the child map;
- stable parent code does not retain child objects after unload;
- replacement/unload removes or closes old generation-owned objects before the generation becomes unreachable;
- compatibility fallback loaders are migration seams, not target composition for new code.

##### Why

Generation isolation lets unload/reload/replacement affect only the owner. Globalizing a child object creates stale references that survive the generation designed to own them.

## Generated Access Pattern

Managed consumers declare Tavall-managed collaborators through `DependencyAccess<...>` and use the generated typed access surface.

### Multi-Dependency Expanded Access

The default consumer is **the public domain operation plus private, live, named DI getters**. The example below is a **proposed architecture migration** adapted from the actual [Project Novus `AchievementProgressMutationHandler`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/handler/AchievementProgressMutationHandler.java). It is **not current compiling production source**: `AchievementProgressRequest`, its conversion method, and the DataHandler synchronization operation below would need to be implemented and tested together.

```java
@DelegatesTo(IAchievementProgressMutationHandler.class)
public final class AchievementProgressMutationHandler
        implements IAchievementProgressMutationHandler,
                   DependencyAccess<
                           IPlayerAchievementDataHandler,
                           AchievementEventMutationAccess,
                           IAchievementCompletionHandler
                   > {

    // Private: the consumer's live Tavall DI access surface.
    private IPlayerAchievementDataHandler getPlayerAchievementDataHandler() {
        return getInstance().playerAchievementDataHandler();
    }

    private AchievementEventMutationAccess getAchievementEventMutationAccess() {
        return getInstance().achievementEventMutationAccess();
    }

    private IAchievementCompletionHandler getAchievementCompletionHandler() {
        return getInstance().achievementCompletionHandler();
    }

    // Public: the operation exposed through IAchievementProgressMutationHandler.
    @Override
    public AchievementProgressMutationResult applyProgress(
            AchievementProgressRequest progressRequest
    ) {
        Objects.requireNonNull(progressRequest, "progressRequest");

        AchievementListData achievementDefinition =
                progressRequest.achievementDefinition();

        if (progressRequest.playerUUID() == null
                || achievementDefinition == null
                || progressRequest.progressAmount() <= 0L
                || !achievementDefinition.enabled()) {
            return null; // Existing production behavior, not a recommended new result API.
        }

        // Conversion belongs to the record; no inline construction in this Handler.
        AchievementProgressEventData progressEventData =
                progressRequest.toProgressEventData();

        AchievementProgressMutationResult mutationResult =
                getAchievementEventMutationAccess().applyEventProgressOnce(
                        progressEventData,
                        achievementDefinition
                );

        if (mutationResult == null || mutationResult.updatedProgress() == null) {
            return mutationResult;
        }

        // The data owner performs timestamp reconciliation, synchronization,
        // and cache projection. The Handler does not implement that policy.
        getPlayerAchievementDataHandler().synchronizeCommittedProgress(
                progressRequest.playerUUID(),
                mutationResult.updatedProgress()
        );

        if (mutationResult.completedNow()) {
            getAchievementCompletionHandler().handleCompletion(
                    mutationResult.updatedProgress(),
                    achievementDefinition
            );
        }

        return mutationResult;
    }
}
```

### Data-owned conversion and mutation methods

The corresponding **proposed** typed request is a record carrying operation input. It owns the **public, pure conversion method** that produces the existing validated `AchievementProgressEventData` record. Its ordinary constructor is the Java record's own implementation detail, not a DI-managed behavior consumer call.

```java
public record AchievementProgressRequest(
        String eventId,
        UUID playerUUID,
        AchievementListData achievementDefinition,
        long progressAmount,
        String actionType,
        String sourceServerId,
        String sourceContext,
        Instant occurredAt
) {
    public AchievementProgressEventData toProgressEventData() {
        return new AchievementProgressEventData(
                eventId,
                playerUUID,
                achievementDefinition.triggerType(),
                progressAmount,
                actionType,
                sourceServerId,
                sourceContext,
                occurredAt
        );
    }
}
```

The **proposed** `IPlayerAchievementDataHandler.synchronizeCommittedProgress(UUID, PlayerAchievementProgressData)` operation would contain the existing synchronization and cache-save sequence. A data-owned method on `PlayerAchievementData`, such as `acceptCommittedProgress(PlayerAchievementProgressData)`, would encapsulate the existing timestamp comparison and `upsertProgress` decision. These are **separate source/interface changes**, not methods claimed to exist today.

Ownership is not a one-size-fits-all mechanical split:

- **Public interface operation:** externally meaningful Handler/DataHandler/Resolver/Service contract.
- **Private consumer getter:** named dynamic `DependencyAccess<...>` lookup; no fields, constructor capture, or local accessor alias.
- **Public record/data method:** a meaningful value conversion or data-specific operation. Compact record constructors and private normalization helpers keep value invariants with the value.
- **Private owner helper:** one owner's internal algorithm or implementation detail, not a cross-class API.
- **Builder:** options/defaults/hydration that merit a separate construction owner, never a ceremonial wrapper for `new Record(...)`.
- **Cache/Registry/Database:** lifecycle and storage behavior remain behind their owning tool/domain contracts.

**Anti-pattern:** `new SomeClass(...)` inside a DI-managed consumer merely to populate a domain record, create another managed class, or assemble its collaborator graph. In ordinary domain consumers, call a data/record-owned factory or transformation when there is a meaningful value boundary, or call an existing DI-managed owner. The `new` expression itself is **not prohibited inside** the record's own methods, a legitimate value builder, an authorized construction factory, or a composition boundary. Do not introduce fake factories that only add a redundant forwarding layer.

The existing `AchievementProgressMutationHandler` and its callers have not been migrated by this documentation example. Before a production change, update the interface, record methods, DataHandler contract, cache policy, generation-owned DI registration, and real tests as one coherent refactor. See [Tavall DI Access Styles](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md) for access semantics and [Handler Patterns](HANDLERS.md) for domain/DataHandler responsibilities.

### Single-Dependency Direct Access

For a single managed dependency, `getInstance()` returns the typed contract directly. Prefer a named getter for repeated use; compact one-off calls may use `getInstance()` directly.

```java
@DelegatesTo(IPlayerRewardHandler.class)
public final class PlayerRewardHandler
        implements IPlayerRewardHandler,
                   DependencyAccess<IEconomyService> {

    private IEconomyService getEconomyService() {
        return getInstance();
    }

    @Override
    public void rewardPlayer(PlayerId playerId, int amount) {
        getEconomyService().deposit(playerId, amount);
    }
}
```

Rules:

- prefer named dependency getters for repeated collaborators; direct `getInstance().namedCapability()` is fine when shorter and clear;
- do not assign `getInstance()` to a method-local generated access or bundle variable as routine consumer style;
- do not constructor-capture or field-cache ordinary Tavall-managed dependencies;
- use generated typed getters instead of repeated class-token lookup;
- ordinary production code MUST NOT cast or assign `getInstance()` to `IDependencyMap`;
- optional dependencies use the repository-approved optional lookup path;
- missing required dependencies fail fast.

##### Why

Typed access preserves Tavall DI metadata identity and replacement semantics. Private named getters improve call sites without becoming cached state. The owning DI guide defines supported access alternatives; this chapter establishes the default ordinary-consumer style.

## Dependency Constructor Injection Is Rejected

Do not constructor-inject Tavall-managed application dependencies into ordinary production handlers, services, orchestrators, routers, listeners, utilities, controllers, or other DI-managed behavior.

#### Bad

```java
public final class PlayerRewardHandler {
    private final IEconomyService economyService;

    public PlayerRewardHandler(IEconomyService economyService) {
        this.economyService = economyService;
    }
}
```

Use `DependencyAccess<IEconomyService>` instead.

Constructors remain valid for:

- immutable object/value state;
- configuration values;
- builder inputs;
- genuinely externally owned platform handles that Tavall DI does not manage;
- infrastructure internals whose owning repository explicitly defines constructor composition outside Tavall application DI.

The canonical [Java Tools adoption policy](https://github.com/TavallStudios/tavall-java-tools/blob/main/docs/CONSUMER_ADOPTION.md#shared-architecture-test-distribution) recognizes a narrow **builder-owned managed-constructor** exception, governed by `DependencyArchitecturePolicy`: every managed production invocation is builder-owned and that builder resolves managed collaborators through Tavall DI. Do not generalize the exception to ordinary Handler constructors or to pure Data/MetaData builders. The owning tool's test policy is authoritative for those call sites.

##### Why

Managed constructor injection moves graph ownership into callers, captures dependency identity at construction time, and can bypass replacement/reload/generation semantics.

## Static Dependency Access Is Rejected

Do not hide Tavall-managed services, registries, caches, persistence, gateways, schedulers, runtimes, or utilities behind static locators.

Allowed statics are pure/dependency-free:

- constants;
- value parsing/normalization;
- private pure helpers;
- construction-only factories/builders such as `of(...)`, `from(...)`, or `builder()`.

A static construction call must not perform I/O, resolve DI, touch mutable runtime state, schedule work, or become a composition root.

##### Why

A static locator erases dependency ownership from the class declaration and lets any caller reach runtime state without participating in its lifecycle.

## Default Consumer Pattern

A consumer is an ordinary production class using Tavall-managed capabilities to perform one focused operation.

The default consumer has:

- one coherent behavior;
- typed request/input where useful;
- typed result for meaningful expected outcomes;
- managed collaborators declared through `DependencyAccess<...>`;
- no constructor-captured Tavall dependencies;
- no static dependency lookup;
- no mutable keyed domain store;
- no raw registry/cache backing-map access;
- no `EntityManager`, JPA callback, JDBC, or application `*Repository` ownership;
- no hidden runtime composition.

### Pattern Responsibilities

| Pattern | Consumer rule |
| --- | --- |
| `*Data` / `*State` | Pass/return typed values. Do not replace known fields with generic maps. |
| `*Request` | Carry operation input across a meaningful boundary. |
| `*Result` | Represent expected success/rejection outcomes explicitly. |
| `*DataHandler` | Use when reusable data policy exists; it may coordinate Tavall Database/cache behavior. Do not require one around every entity call. |
| `*MetaData` | Typed derived/resolved value; extensible maps stay at real integration edges. |
| `*MetaDataHandler` | Derive/refresh/enrich metadata; do not mutate primary data by accident. |
| `*Registry` | Call domain lookup/registration methods; never backing-map APIs. |
| `*Cache` | Consume cache-facing behavior only when cache policy is actually the consumer's responsibility. |
| `*Repository` | Prohibited for new Tavall-owned production declared types; existing names are migration debt only. |
| `*Orchestrator` | Coordinate ordered work/lifecycle; do not absorb collaborator rules/storage. |
| `*Router` | Select/delegate; do not become the implementation. |
| `*Builder` | Construct typed output only; never resolve/wire managed dependencies. |
| `*Handler` | Own one focused domain behavior/operation family. |
| `*Service` | Provide one cohesive reusable domain capability. |

##### Why

The table separates behavior consumption from behavior ownership. Without that distinction, one consumer slowly becomes registry, cache, persistence runtime, router, orchestrator, and builder because all those operations were convenient to perform in one class.

## More Than Four Managed Dependencies

More than four managed dependencies is a **design-review signal**, not a runtime cap.

Review in this order:

1. **Keep direct `DependencyAccess`** when the class is genuinely cohesive and each dependency serves one narrow behavior.
2. **Use one immutable domain bundle** only when the collaborators form a durable domain boundary reused by several consumers.
3. **Split responsibilities** when the class owns several distinct behaviors/lifecycle phases.

Do not:

- hide the same dependencies inside a builder;
- constructor-inject them instead;
- create a generic `Services`, `Dependencies`, or `Context` bag;
- introduce a bundle used by only one class merely to reduce the visible count.

##### Why

Dependency count is evidence of coupling, not a style error. Hiding the count does not remove the coupling and usually makes ownership less visible.

## Data and Persistence Consumption

Durable consumers use the **entity classes and entity persistence contract defined by the checked-in `tavall-database` version**. This DI chapter does not copy or freeze a concrete Tavall Database accessor.

A consumer/DataHandler does not create an `EntityManager` callback, JDBC transaction wrapper, generic database wrapper, or new Tavall-owned `*Repository` type merely to wrap ordinary persistence.

A DataHandler may exist when it owns reusable policy such as cache-aside load, mapping, dirty/retry handling, batching, or retention.

Required persistence rules: [Entity Persistence](ENTITY_PERSISTENCE.md).

##### Why

DI explains how a consumer reaches managed capabilities. The persistence module owns the API and transaction lifecycle behind the durable capability, so duplicating its accessor here would create a second source of truth.

## Consumer-Owned Collection Rejection

A consumer does not own long-lived mutable keyed state merely because the field is private/thread-safe.

Route state by semantics:

- Registry for keyed runtime identity;
- Cache for disposable/expiring state;
- Tavall Database for durable state;
- dedicated typed operation/runtime owner for futures/tasks/pending work;
- immutable typed data for snapshots/values.

Required state rules: [Registries, Caches, and Persistence](REGISTRIES_CACHES_AND_REPOSITORIES.md) and [Application-Owned Mutable Maps](APPLICATION_OWNED_MUTABLE_MAPS.md).

##### Why

Private mutable keyed state is still architecture. It still needs lifecycle, replacement, concurrency, cleanup, and authority semantics.

## Orchestration Pattern

An `*Orchestrator` owns sequencing/lifecycle across several already-focused boundaries.

Use one when behavior is primarily the **order** of handlers, routers, schedulers, services, runtime boundaries, persistence/cache updates, or compensation steps.

Project Novus production source: [`FFARoundOrchestrator`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/round/orchestrator/FFARoundOrchestrator.java).

The production responsibility split is the useful evidence: the orchestrator obtains time/participant count, advances runtime maintenance, invokes the round state machine, and routes the resulting transition. Compatibility-era constructor composition in that source is not the target DI pattern.

An orchestrator may own operation-level coordination state such as `running` or a last-tick timestamp when that state belongs to the workflow. It does not own durable/cache/registry state for collaborators.

##### Why

Sequencing is real behavior. Without one testable owner it leaks into listeners, commands, schedulers, controllers, or oversized handlers until each surface performs a slightly different workflow.

## Lifecycle and Cleanup

Composition creates cleanup responsibility.

For every managed runtime define:

- creator/owner;
- registration point;
- close/unload behavior;
- replacement order;
- cancellation/draining of async work;
- reverse-order cleanup where appropriate;
- dependency-map cleanup after owned resources close.

##### Why

DI replacement and module reload are only safe when old generations actually release listeners, tasks, caches, registries, database/runtime handles, and references.

## Testing Requirements

Verify where applicable:

- interface/concrete aliases share one identity/metadata owner;
- module dependency maps isolate generations;
- replacement makes new dependencies visible to existing generated access surfaces;
- missing required dependencies fail predictably;
- ordinary managed behavior is tested through production-equivalent DI composition;
- constructor-only test paths do not replace production DI;
- consumers do not own raw keyed stores or JPA callbacks;
- orchestrators invoke collaborators in required order;
- orchestrator start/close behavior is deterministic when it owns operation lifecycle;
- cleanup removes generation-owned work/state.

## Review Checklist

- [ ] Root architecture and every additional relevant delegated chapter were read.
- [ ] Tavall-owned behavior is interface-first and DI-managed by default.
- [ ] Consumers depend on contracts/interfaces rather than concrete implementations.
- [ ] Tavall-managed collaborators use `DependencyAccess` and typed accessors; `IDependencyMap` / `DependencyMap` is not accessed directly.
- [ ] Direct construction of DI-managed implementations is prohibited outside approved composition boundaries.
- [ ] No ordinary managed behavior constructor-captures Tavall dependencies.
- [ ] Static methods do not locate managed runtime behavior.
- [ ] Aliases share one metadata/instance owner.
- [ ] Generation-owned dependencies stay generation-local.
- [ ] Dependency counts above four receive design review without hiding them.
- [ ] Builders do not become dependency containers.
- [ ] Durable behavior follows the checked-in Tavall Database entity contract without this chapter freezing an accessor.
- [ ] No new Tavall-owned production type ends in `Repository`.
- [ ] Consumers do not own mutable keyed stores.
- [ ] Orchestrators own sequence/lifecycle, not collaborator rules/storage.
- [ ] Cleanup/replacement/unload behavior is explicit and tested.
