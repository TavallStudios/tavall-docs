# Tavall Interfaces and Abstractions

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Interfaces describe stable capabilities and substitution boundaries. They are not a tax every class pays for existing.

## Interface Rule

Use an interface when a real contract boundary exists, including:

- a Tavall DI-managed capability exposed through `@DelegatesTo`;
- a module boundary;
- a platform adapter;
- local/distributed or provider strategy;
- an external provider boundary;
- a test fake where substitution is part of the contract;
- a policy/strategy family.

A single implementation may still justify an interface when that interface is the stable DI/module contract. Passive values and implementation-private helpers usually do not.

##### Why

Interfaces are valuable when they protect a capability boundary. Creating one merely because a class exists adds files without creating ownership or substitutability.

## Dependency Access

Managed consumers depend on the narrowest stable capability interface and resolve it through Tavall DI. They do not constructor-inject Tavall-managed dependencies or use static service locators.

Concrete implementations may also be registered under their concrete type when diagnostics or explicit advanced access requires it.

## Prohibited Repository Interfaces

**Do not create new Tavall-owned production interfaces or other declared types ending in `Repository`.**

Rejected:

```text
IPlayerRepository
PlayerRepository
IMessageConfigRepository
PostgresAccountRepository
```

Existing repository interfaces are migration debt only. Their current presence is not proof that persistence requires an interface of the same shape.

Ordinary durable persistence follows Tavall Database entity classes and the entity persistence contract defined by the checked-in `tavall-database` version. Shared Tavall application docs do not invent a Repository abstraction over that module.

If a persistence-adjacent capability genuinely needs substitution, name the **capability**, not its storage stereotype. Examples might include a domain-specific `HistoryReader`, `AuditWriter`, `SnapshotService`, `ImportHandler`, `ExportWriter`, `SynchronizationHandler`, or a precise external `Gateway` when it really represents an outside system.

##### Why

`IWhateverRepository` made the old persistence layer look permanent because consumers depended on the abstraction even after the implementation mechanism changed. Naming the actual capability lets persistence evolve without preserving a generic Repository seam forever.

## Abstract Classes

Use an abstract class only when multiple implementations genuinely share behavior, state, lifecycle, validation, or mechanics. Abstract classes are not status symbols.

Registry and Cache base classes are valid because they centralize real shared lifecycle/collection behavior. Domain implementations still expose focused methods rather than backing-map mechanics.

## Method Contracts

Interface methods use typed requests, results, keys, states, and domain data. Avoid `Object`, raw strings, arbitrary mutable maps, and storage-mechanic APIs when a stable type or domain action exists.

## Review

Before adding an interface, identify the actual substitution/contract boundary. Reject the interface when:

- it exists only because the concrete exists;
- it hides a Tavall-managed dependency behind static lookup;
- it exposes raw mutable storage;
- it is a new `*Repository`/`I*Repository` type;
- its only purpose is preserving a generic CRUD wrapper around Tavall Database.
