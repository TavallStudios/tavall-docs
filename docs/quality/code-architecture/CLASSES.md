# Tavall Class Roles

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Classes should have one coherent reason to change. Role suffixes are architectural contracts, not decorative nouns added after implementation.

## Core Roles

| Role | Responsibility |
| --- | --- |
| `*Data` / `*State` | Typed values/state. Not service lookup or mutable storage infrastructure. |
| `*Request` | Operation input. |
| `*Result` | Typed operation outcomes. |
| `*Handler` | One focused behavior/operation family. |
| `*DataHandler` | Domain data access/update policy when application behavior genuinely needs that boundary. |
| `*MetaDataHandler` | Derivation/normalization/enrichment of metadata. |
| `*Service` | One cohesive reusable domain capability. |
| `*Orchestrator` | Ordered workflow/lifecycle coordination across focused collaborators. |
| `*Router` | Select and delegate. |
| `*Resolver` | Derive one typed answer from explicit input. |
| `*Registry` | Runtime keyed identity/lookup ownership. |
| `*Cache` | Disposable/expiring/reloadable fast-state ownership. |
| `*Builder` | Construct typed values/definitions/requests/results/configuration. |
| `*Mapper` | Convert representations. |
| `*Reader` / `*Writer` | Read/write a real source or capability when that is the actual role. |
| `*Bootstrap` | Startup/composition ownership. |
| `*Runtime` | Active-generation/system lifecycle ownership. |

##### Why

Naming a real role makes ownership visible before reading implementation. The suffix should answer what kind of behavior or lifecycle the class owns, not merely provide a respectable-sounding noun.

## Handler, Service, and Orchestrator

A **Handler** owns one focused behavior or operation family. A **Service** owns one reusable cohesive capability used across consumers. An **Orchestrator** owns ordering/lifecycle across several focused boundaries.

Input adapters such as commands/listeners/controllers receive external input and delegate. They do not become the reusable domain owner merely because input arrived there first.

##### Why

These roles separate operation behavior, reusable capability, and multi-step sequencing. Without that distinction, one class slowly absorbs rules, storage, routing, and lifecycle until its suffix stops meaning anything.

## Builders

Builders construct typed output. They do not resolve Tavall-managed dependencies, wire runtime graphs, register managed behavior, persist, authorize, or schedule work.

##### Why

Construction should remain predictable from explicit inputs. Hidden runtime behavior turns a builder into an alternate service/composition system.

## Registry and Cache

Registry and Cache are infrastructure-backed ownership roles:

- Registry for runtime identity/definitions/providers/sessions/indexes;
- Cache for disposable/reloadable/expiring/stale-able fast state.

Ordinary consumers do not recreate these with mutable maps.

## Durable Persistence

Tavall application persistence is modeled through **Tavall Database entity classes and the entity persistence contract defined by the checked-in `tavall-database` version**.

Shared class-role docs do not prescribe a concrete Tavall Database accessor and do not create a parallel persistence class role around it.

## Prohibited `*Repository` Class Name

**New Tavall-owned production declared types ending in `Repository` are prohibited.** This applies to classes, interfaces, records, enums, and other production type declarations.

Rejected:

```text
PlayerRepository
IPlayerRepository
PostgresPlayerRepository
MessageRepository
```

Existing `*Repository` types are migration debt only and must be deleted/renamed as their behavior moves to the correct owner. They are not templates or substitution boundaries for new work.

Do not evade the ban with `RepositoryImpl`, `RepositoryAdapter`, `RepositoryStore`, or an equivalent wrapper whose purpose is preserving repository architecture.

##### Why

The Repository role repeatedly preserved obsolete persistence layers after Tavall Database had already taken ownership. A hard naming prohibition prevents generators and engineers from recreating the same wrapper under the comforting banner of abstraction.

## Static Classes

Static classes/methods are for constants, pure transformations, parsing, formatting, and construction-only factories. Runtime behavior requiring DI, state, I/O, replacement, scheduling, persistence, or platform access remains instance-owned.

## Persistence-Adjacent Capability Names

If behavior near persistence is real application behavior, name what it actually does: `HistoryReader`, `AuditWriter`, `SynchronizationHandler`, `SnapshotService`, `ImportHandler`, `ExportWriter`, or another precise capability. Do not default back to Repository.

## Review

Reject a class when:

- its role/name does not match its ownership;
- it mixes unrelated domains/lifecycle phases;
- it owns mutable keyed state that belongs to Registry/Cache/Tavall Database/operation runtime;
- it constructor-injects Tavall-managed dependencies;
- it ends in `Repository` and is not already grandfathered migration debt;
- it exists mainly as a forwarding wrapper with no independent behavior or lifecycle.
