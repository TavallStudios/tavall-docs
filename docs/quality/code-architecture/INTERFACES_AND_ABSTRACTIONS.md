# Tavall Interfaces and Abstractions

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Interfaces define stable behavioral capabilities and substitution or lifecycle boundaries.

> **Governing Doctrine:** Tavall-owned behavior is DI-managed by default. **Interface-first remains the default for meaningful reusable capabilities**, but not every managed concrete class needs a separate interface. The concrete can be registered directly with bare `@DelegatesTo`.

```text
Meaningful shared capability:
consumer → typed interface contract → Tavall DI → concrete implementation

Concrete-only managed capability:
consumer → typed concrete token → Tavall DI → concrete implementation
```

## Interface Creation Gate

**An interface can be valuable with only one implementation.** A good interface documents behavior independent of its implementation and makes module fan-in, stable access, replacement, testing, or lifecycle guarantees explicit.

| Class role | When to use an interface |
| --- | --- |
| Handler / DataHandler / MetaDataHandler | Normally when consumed as a domain operation or shared across class/module boundaries. |
| Service | Normally; sustained capabilities need stable lifecycle and consumer contracts. |
| Router / Resolver / DataResolver / Viewer / Provider / Gateway | When they expose a real shared, pluggable, testable or substitutable capability. |
| Registry / Cache | Follow the owning Tavall Java Tool's real contracts. No ornamental wrapper interfaces. |
| Platform utility / Adapter | Composition interfaces with reusable defaults are preferred; see [Utilities](UTILITIES.md). |
| Bootstrap / Runtime | Use existing module lifecycle interfaces or introduce one only for independently controlled runtime capability. |
| Data / State / Snapshot / MetaData / Request / Result / enum / CustomEnum / Exception | Normally no interface, unless a distinct real API demands one. |
| Pure Formatter / Mapper / Builder / private helper | Interface optional; justify actual substitution or ownership rather than generating `IWhatever` automatically. |

An interface should expose a **narrow, useful behavioral contract** with real consumers. Before adding one, identify what responsibility it protects, whether multiple callers need it, how it supports substitution/test replacement/module access/lifecycle, and whether an existing Tavall interface or Java Tool already serves that purpose.

**Do not equate DI registration with the need for an interface.** A single concrete implementation can still be managed by Tavall DI. Conversely, one implementation is not proof that an interface is unnecessary: stable cross-module APIs may deserve an interface before alternatives exist.

## Explicit Exceptions Where Interfaces Are Not Forced

Do not force meaningless interfaces onto pure data structures. Reasonable exceptions include:

- immutable values;
- records;
- DTOs;
- serialization models;
- configuration value objects;
- enums;
- exceptions;
- builders whose sole responsibility is object construction;
- factories / composition roots;
- generated code;
- foreign/framework objects Tavall does not own;
- tiny ephemeral local implementation-detail objects with no architectural dependency role;
- test fixtures, mocks, and fakes.

Empty interfaces without behavioral methods created solely to satisfy a syntactic rule MUST NOT be created. The purpose of interface contracts is architectural boundaries, substitution, testing, lifecycle control, and dependency ownership.

## Dependency Access and Concrete Registration

The [Tavall DI `@DelegatesTo` implementation](https://github.com/TavallStudios/tavall-di/blob/main/src/main/java/org/tavall/dependency/annotations/DelegatesTo.java) declares `Class<?>[] value() default {}`. It **always registers the annotated concrete**. Optional parameters register additional assignable interface or supertype tokens that point to the same managed implementation and metadata.

**Concrete only: no interface is required solely for DI.**

```java
/**
 * Provides diagnostic information owned by one FFA runtime.
 */
@DelegatesTo
public final class FFARoundDiagnostics {

    public String getSummary() {
        return "FFA round diagnostics";
    }
}
```

**Real behavioral contract: declare and register the interface.**

```java
public interface IFFARoundService extends AutoCloseable {

    void start();

    boolean isRunning();

    @Override
    void close();
}
```

```java
@DelegatesTo(IFFARoundService.class)
public final class FFARoundService implements IFFARoundService {
    // Illustrative declaration only; provide the actual lifecycle methods.
}
```

Multiple interface parameters are supported only when they are **assignable from the same concrete class** and each interface carries a real capability (e.g., `@DelegatesTo({IPlayerSessionReader.class, IPlayerSessionWriter.class})`). Do not generate arbitrary Reader/Writer contracts merely because several annotation parameters are available.

Managed consumers use `DependencyAccess<...>` to resolve the narrowest meaningful interface or, when the class has no useful contract, its registered concrete token. Avoid constructor-captured managed collaborators, static service locators, direct DI map queries and duplicate dependency containers. [Tavall DI access styles](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md) own the exact resolution API.

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

## Direct Java Capability and Adapter Default

Tavall-owned Java capabilities expose their typed semantic Java API as the canonical reusable boundary.

```text
same JVM:
consumer
    -> typed Java capability
         +-> CLI adapter
         +-> HTTP/MCP adapter
         +-> Web/UI adapter

separate process:
consumer Java
    -> typed integration client
    -> stable transport
    -> owning runtime
```

### Same JVM / Composition

When caller and capability share one JVM composition boundary, ordinary Java consumers call that typed API directly.

Bad defaults:
- Java -> CLI process -> parse stdout/JSON -> same Java application;
- Java -> localhost HTTP -> controller -> domain service;
- Java -> MCP tool dispatch -> tool adapter -> same JVM capability.

Correct default:
- `Java caller -> typed Java capability`

External adapters (CLI, HTTP, MCP, Web/UI) project that same capability; they do not become duplicate domain/business authorities.

### Separate Process / Runtime

For a separate runtime or process, the Java consumer uses a typed integration client that encapsulates the stable transport and protocol details. Business, domain, and controller code do not scatter raw HTTP requests, JSON envelopes, CLI commands, MCP tool names, socket framing, or remote service ports.

### No Decorative Over-Abstraction

If an existing canonical Tavall tool (`tavall-database`, `tavall-registry`, `tavall-cache`, `tavall-di`, `tavall-concurrency`, etc.) already exposes the correct semantic API, use it directly. Do not add:
- `FooFacade`
- `FooWrapper`
- `IFooRepository`
- `FooApiServiceFactory`

merely to restate an existing library API. A new interface requires a real ownership, substitution, dependency-direction, or process boundary.

## Review

Before adding or reviewing an interface, verify it defines a real behavioral contract. Reject the interface when:

- it is an empty marker interface with no behavioral methods created merely to satisfy a syntactic rule;
- it hides a Tavall-managed dependency behind static lookup;
- it exposes raw mutable storage;
- it is a new `*Repository`/`I*Repository` type;
- it creates decorative wrappers around already-correct Tavall library APIs;
- its only purpose is preserving a generic CRUD wrapper around Tavall Database.
