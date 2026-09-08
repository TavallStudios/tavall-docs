# Tavall Class Roles

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Classes should have one coherent reason to change. Role suffixes are architectural contracts, not decorative nouns added after the implementation is already a small government.

## Class Rules

A class should primarily do one of these things:

- hold typed data/state;
- construct typed values;
- perform focused domain behavior;
- adapt external input;
- coordinate an ordered workflow;
- resolve/format/route a typed value;
- own runtime registry/cache state;
- request durable operations through the owning persistence boundary;
- provide focused platform adaptation or pure utility behavior.

Avoid vague names such as `Manager`, `Helper`, `Common`, or `Misc`.

##### Why

A class name and role should predict what the class is allowed to own. When storage, presentation, validation, routing, lifecycle, and data construction accumulate in one type, callers can no longer tell where a rule belongs or which lifecycle owns the state.

## Naming Rules

- Name the domain subject and role: `PlayerRankMetaDataHandler`, not `MetaHandler`.
- Preserve established acronyms such as `UUID`, `UI`, `HTTP`, `JSON`, and `Redis`.
- Match interface/implementation names where practical: `ITimerResolver` / `TimerResolver`.
- Platform names appear only when the class owns that platform boundary.
- Reusable data/request/result/state/definition/metadata types remain top-level records/classes.
- Rename when responsibility becomes materially clearer, not merely because a newer suffix feels fashionable.

##### Why

Precise names make ownership visible before a file is opened and give architecture tests/reviewers useful signals. A class called `Cache` that performs durable persistence or a `Builder` that wires services is immediately suspicious instead of merely unconventional.

## Domain Handler

A domain `*Handler` owns one focused behavior or operation/input family.

Examples:

```text
RankUpdateHandler
AchievementCompletionHandler
MessageRenderHandler
```

A domain handler **may own core rules for that focused behavior**. It should not absorb unrelated rules, durable storage mechanics, raw cache/registry collections, or platform input parsing.

##### Why

“Handlers should never contain core rules” was too broad and conflicted with Tavall's default behavior pattern. The useful distinction is between a domain handler, which exists to implement focused behavior, and an input adapter/listener/command, which should not become the reusable domain rule merely because it received the event first.

## Input Adapters, Commands, and Listeners

Commands, controllers, listeners, and other platform adapters receive external input, build/resolve typed operation input, delegate to domain behavior, and adapt the result back to the platform.

They should not own reusable domain policy, persistence mechanics, or keyed runtime stores.

##### Why

Platform input changes for different reasons than the domain rule. Keeping the adapter thin allows the same behavior to serve game, web, Discord, jobs, tests, or future surfaces without importing each surface's event model.

## Service

A `*Service` provides a cohesive reusable domain capability shared by multiple consumers.

Examples may include:

```text
CurrencyService
StorageService
FarmProductionService
```

A service is **not** defined by being “long-running.” Lifecycle may matter for some services, but the defining property is a coherent reusable capability broader than one focused operation/input family.

Do not use `Service` as the default suffix for arbitrary logic. Prefer a Handler, Resolver, Registry, Cache, Orchestrator, Router, etc. when that role is more exact.

##### Why

Using runtime duration as the Service test produced contradictory guidance: capability classes such as permission/currency services can be valid without being daemons, while a long-lived object may actually be a Runtime, Registry, or Cache. Responsibility is a better classification than how long the object happens to exist.

## Orchestrator

A `*Orchestrator` coordinates ordered work/lifecycle across several focused collaborators.

It owns:

- sequencing;
- operation lifecycle;
- cross-boundary coordination;
- startup/shutdown/compensation when those are part of the workflow.

It does not absorb collaborator rules, caches, registries, persistence mechanics, or storage maps.

##### Why

Sequencing across several focused boundaries is real behavior. Without one owner it leaks into commands, listeners, schedulers, or oversized handlers until each surface performs a slightly different workflow.

## Data and State

`*Data`, `*State`, `*Request`, `*Result`, and `*MetaData` are typed values.

They do not resolve Tavall-managed dependencies, open databases, mutate caches/registries, schedule work, or become hidden service objects.

Metadata is derived/resolved/display-ready state and should normally be rebuildable from its source data/definitions.

##### Why

A data value should remain understandable as a value. If reading it can perform I/O or reach runtime services, passing the object across a boundary also passes hidden behavior and failure modes.

## Data Handler

A `*DataHandler` owns domain data load/save/update policy when application code needs a focused data boundary.

It may coordinate Tavall Database entity operations and cache behavior when that coordination is the data policy. It does not own unrelated gameplay/product authorization rules.

Do not require a DataHandler for every entity. If ordinary behavior can correctly use the typed Tavall Database entity boundary directly without duplicating cache/persistence policy, another wrapper adds no value.

##### Why

Data policy is useful when several callers need the same cache/load/save/retry behavior. It is not useful as mandatory ceremony around every `database.entities().find(...)`.

## MetaData Handler

A `*MetaDataHandler` derives, refreshes, validates, enriches, or exposes metadata when that work is behavior rather than passive construction.

It should not mutate primary durable data merely because the metadata came from it.

##### Why

Metadata derivation and primary persistence have different authority. Combining them means a presentation refresh can unexpectedly become a durable mutation path.

## Builder

A `*Builder` constructs one explicit typed output. Builders do not save, cache, register managed behavior, schedule, authorize, orchestrate, or resolve Tavall-managed dependencies.

Runtime/bootstrap composition is not a builder pattern even when legacy production classes still use `*RuntimeBuilder` names.

##### Why

Construction should be deterministic from explicit inputs. Once a builder performs runtime composition or I/O, object creation becomes a hidden workflow with lifecycle/failure behavior callers cannot infer from `build()`.

## Registry

A `*Registry` owns typed keyed runtime identity/lookup state and exposes domain methods rather than a generic mutable-map API.

Use Tavall Registry and `AbstractIndexedRegistry` where appropriate.

##### Why

Runtime keyed state needs duplicate, replacement, indexing, snapshot, and cleanup policy. A dedicated registry gives those invariants one owner instead of scattering maps through behavior classes.

## Cache

A `*Cache` owns disposable/reloadable/expiring fast-access state using Tavall Cache.

A cache is not durable truth unless a narrower architecture explicitly assigns that authority, which should be rare and loudly documented.

##### Why

Eviction, expiration, restart, and invalidation must be safe. If losing a cache entry means losing authoritative data, the thing was not merely a cache.

## Persistence Classes

Tavall Database owns normal PostgreSQL/JPA persistence mechanics.

Do **not** create `PlayerAccountDatabase`, `PostgresPlayerRepository`, `PlayerStore`, or similar generic CRUD wrappers whose only role is forwarding ordinary entity operations.

Mapped entities own mapping/query definitions. Application code uses `database.entities()` or another typed Tavall Database operation.

A `*Repository` is reserved for a real stable domain persistence/substitution contract beyond ordinary Tavall Database entity CRUD.

##### Why

Generic database/repository wrappers duplicate Tavall Database and create additional places for query, transaction, exception, and lifecycle behavior to diverge. A persistence class earns its existence only when it owns a real contract Tavall Database does not already provide directly.

## Utility Classes

Pure Java utility classes are focused, stateless, final, and have no hidden runtime dependencies.

Platform/application utility behavior that touches runtime state remains a DI-managed adapter/capability rather than a static global helper.

##### Why

Static mutable/runtime access bypasses replacement and lifecycle ownership. Pure helpers stay safe because their result depends only on explicit input.

## Inner Classes

Avoid inner classes for reusable domain data, metadata, services, handlers, builders, registries, caches, or other concepts with identity outside the parent implementation.

A small private implementation detail may remain inner when it has no value outside the parent.

##### Why

Top-level domain types are searchable, independently testable, and reusable without forcing callers to depend on an unrelated parent class.

## Review Checklist

- [ ] The class has one coherent responsibility/lifecycle.
- [ ] The suffix matches the responsibility actually owned.
- [ ] Domain handlers may own focused rules; platform input adapters stay thin.
- [ ] Services represent reusable cohesive capabilities, not merely “logic” or “long-running things.”
- [ ] Orchestrators own sequencing, not collaborator rules/storage.
- [ ] Data/metadata remain values without hidden runtime behavior.
- [ ] Builders construct typed output only.
- [ ] Registries/caches own keyed runtime/cache state through Tavall infrastructure.
- [ ] Ordinary persistence uses Tavall Database entity/typed operations rather than generic CRUD wrappers.
- [ ] Repositories exist only for real domain persistence/substitution contracts.
- [ ] Static classes remain pure/stateless.
