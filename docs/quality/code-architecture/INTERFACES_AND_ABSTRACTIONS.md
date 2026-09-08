# Tavall Interfaces and Abstractions

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Interfaces exist to describe stable capabilities and substitution boundaries. They are not a tax every class pays for existing.

## Interface Rule

Use an interface when at least one real contract boundary exists, including:

- a Tavall DI-managed capability exposed through `@DelegatesTo`;
- a module boundary;
- a platform adapter;
- an external provider family;
- a strategy/policy family;
- local versus distributed implementations;
- a real persistence substitution boundary beyond ordinary Tavall Database entity CRUD;
- a test fake that represents the same production contract.

A single current implementation may still justify an interface when the interface is the stable DI/module contract. Tiny data values, records, implementation-private helpers, and concrete classes with no substitution boundary generally do not need one.

##### Why

Interfaces are useful when callers should depend on **what can be done** while implementation identity may change. Creating one automatically for every concrete class adds navigation and maintenance cost without creating a meaningful boundary.

The goal is explicit substitution, not abstraction cosplay.

## Naming

Where the owning codebase uses Tavall's standard interface naming, use `I` followed by the concrete/capability name:

```text
PermissionService -> IPermissionService
PlayerAchievementCache -> IPlayerAchievementCache
AchievementListRegistry -> IAchievementListRegistry
```

The name should describe the same capability as the implementation. Do not invent different nouns merely to make the interface sound more abstract.

##### Why

Matching names make DI aliases and implementations easy to pair during review, generation, and diagnostics. Different nouns for the same capability force readers to rediscover relationships that the type system could have made obvious.

## Tavall DI Consumption

Managed behavior depends on interface contracts through Tavall DI, not constructor-captured managed dependencies.

```java
@DelegatesTo(IPunishmentHandler.class)
public final class PunishmentHandler
        implements IPunishmentHandler,
        DependencyAccess<
                IPermissionHandler,
                IPostgresDatabase
        > {

    @Override
    public PunishmentResult ban(PunishmentRequest request) {
        IDependencyMap dependencies = getInstance();
        IPermissionHandler permissionHandler = dependencies.iPermissionHandler();
        IPostgresDatabase database = dependencies.iPostgresDatabase();

        if (!permissionHandler.canPunish(
                request.staffProfile(),
                request.targetProfile()
        )) {
            return PunishmentResult.denied();
        }

        PunishmentEntity entity = PunishmentEntity.from(request);
        database.entities().save(entity);

        return PunishmentResult.success();
    }
}
```

##### Why

The handler declares the contracts it needs while the owning `IDependencyMap` retains replacement and lifecycle ownership. Constructor injection would move graph ownership into callers and can capture stale generation objects.

The persistence example also demonstrates the Tavall Database rule: ordinary entity persistence does not require inventing `IPunishmentRepository` merely to wrap `save()`.

## Depending on Concrete Classes

Depending on a concrete class is acceptable when the concrete type itself is the intended non-substitutable value/implementation boundary.

It is suspicious when:

- the class is Tavall DI-managed under an interface alias;
- callers should survive implementation replacement;
- platform/provider/test substitution is expected;
- the concrete type exposes implementation details the caller does not need.

Do not create an interface retroactively just to silence a stylistic preference. Identify the actual contract first.

##### Why

“Always interface” and “never interface” are both lazy rules. The correct question is whether callers need a stable capability independent of implementation identity.

## Persistence Interfaces

Ordinary Tavall Database entity CRUD does **not** justify an application repository interface.

Bad:

```java
public interface IPlayerRepository {
    Optional<PlayerEntity> find(UUID playerId);
    void save(PlayerEntity entity);
}
```

when the implementation only forwards those calls to:

```java
database.entities().find(PlayerEntity.class, playerId);
database.entities().save(entity);
```

Use a repository interface only when there is a genuine domain persistence/substitution contract beyond ordinary entity CRUD, such as multiple provider families or persistence behavior with independent domain semantics.

##### Why

A pass-through repository interface duplicates Tavall Database without adding a contract. It creates more DI tokens, more files, and another place for persistence behavior to drift while accomplishing exactly the same entity operation.

## Data and Value Types

Do not create interfaces for passive data merely because behavior classes use interfaces.

Prefer typed records/classes:

```java
public record RankUpdateRequest(
        UUID staffUUID,
        UUID targetUUID,
        RankKey rankKey
) {
}
```

An interface is justified only when the value itself represents a polymorphic contract with multiple meaningful implementations.

##### Why

Data values already communicate their schema through their fields and type. Adding `IRankUpdateRequest` to one immutable record provides no substitution value and makes construction/serialization needlessly indirect.

## Abstract Classes

Interfaces define contracts. Abstract classes share implementation mechanics or lifecycle.

Use an abstract class only when multiple implementations genuinely share:

- state whose ownership is part of the abstraction;
- lifecycle behavior;
- validated mutation mechanics;
- reusable algorithmic implementation that subclasses specialize narrowly.

Tavall Registry and Tavall Cache base classes are examples of legitimate shared mechanics. Application code should not create a new abstract base merely to avoid a few repeated lines.

##### Why

Inheritance couples implementations to one shared state/lifecycle model. That is valuable when the shared mechanics are real, but expensive when the only goal was code deduplication.

## Review Checklist

- [ ] The interface represents a real DI/module/substitution contract.
- [ ] A single implementation is justified by a stable contract, not by habit.
- [ ] Passive data/value types are not given interfaces without polymorphic need.
- [ ] Managed behavior resolves interface contracts through Tavall DI rather than constructor injection.
- [ ] Ordinary Tavall Database entity CRUD is not wrapped in a repository interface.
- [ ] Concrete dependencies are used only when concrete identity is intentionally part of the contract.
- [ ] Abstract classes share real mechanics/state/lifecycle rather than naming prestige.
