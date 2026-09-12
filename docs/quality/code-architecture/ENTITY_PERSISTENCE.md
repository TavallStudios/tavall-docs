# Tavall Database Entity Persistence

> **Status:** Active  
> **Authority:** Binding persistence specialization of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Production Tavall application code, generated code, automation, reviews, and AI-assisted changes

Tavall application modules model durable state with the **entity classes and entity persistence contract defined by the checked-in `tavall-database` version**. Tavall Database owns the persistence runtime. Application code does not own an `EntityManager`, transaction callback, factory, connection, prepared statement, generic CRUD wrapper, or application `*Repository` layer.

## Binding Rule

Shared Tavall application architecture deliberately does **not** prescribe a concrete Tavall Database accessor.

Do not copy module-owned API shapes such as these into global application policy:

```text
IPostgresDatabase.entities()
database.entities()
database.jpa()
IPostgresJpaContext
future accessor names that belong to tavall-database
```

Instead, inspect the checked-in `tavall-database` dependency and use its current entity classes, interfaces, operations, lifecycle, tests, and documentation.

Application code must not create a local equivalent around `EntityManager`, `EntityManagerFactory`, `EntityTransaction`, JPA callbacks, or JDBC transaction ownership.

##### Why

The persistence API belongs to the module that implements it. Hard-coding one Tavall Database accessor in shared application documentation makes the docs stale as soon as Tavall Database improves its entity model.

The stable architecture rule is ownership: Tavall Database owns persistence mechanics; application code models and uses entities according to the installed Tavall Database contract.

## Entity Ownership

A durable table is represented by an owning mapped entity or a small cohesive entity family according to Tavall Database rules.

Entity classes own durable mapping concerns such as:

- table/column mapping;
- primary/composite identity;
- enum, JSON, and timestamp mapping;
- query metadata supported by the current Tavall Database entity model;
- conversion to/from domain values when a separate domain value is useful.

Entities do not own:

- gameplay/product orchestration;
- command/controller behavior;
- caches/registries;
- delivery/network behavior;
- manual connection/transaction lifecycle;
- schema migration execution.

##### Why

An entity describes durable representation. Mixing unrelated application behavior into it couples persistence shape to product rules and makes storage evolution responsible for concerns it does not own.

## `*Repository` Name Prohibition

**New Tavall-owned production classes, interfaces, records, enums, or other declared types whose simple name ends in `Repository` are prohibited.**

Rejected examples:

```text
PlayerRepository
IPlayerRepository
PostgresPlayerRepository
MessageRepository
AccountLinkRepository
```

Existing `*Repository` types are migration debt only. They do not authorize new repository types, new repository consumers, or a renamed replacement that preserves the same redundant layer.

The legacy set may only shrink.

When migrating existing repository-shaped code:

1. model/complete the Tavall Database entity classes required by the durable state;
2. use the entity persistence contract defined by the checked-in `tavall-database` module;
3. move real domain sequencing to the Handler/Service/Orchestrator that owns that behavior;
4. give any genuine external/provider boundary a name describing that capability rather than `Repository`;
5. delete the legacy `*Repository` type and its DI token once consumers move;
6. shrink the executable architecture-test debt baseline in the same coherent migration.

Do not evade the rule with names such as `RepositoryImpl`, `RepositoryAdapter`, `RepositoryStore`, or `PersistenceRepository`. A forwarding layer whose only purpose is preserving repository architecture remains the same problem with fresh stationery.

##### Why

`Repository` became a compatibility magnet. Old JPA/JDBC wrappers survived because new code could always add one more repository and call it abstraction. Prohibiting the production name forces persistence changes to converge on Tavall Database instead of generating another wrapper around it.

## Query Rules

Query behavior follows the **current Tavall Database entity model**.

Application handlers, services, orchestrators, controllers, listeners, and compatibility code must not invent ad hoc JPA/JDBC query ownership outside the boundaries explicitly provided by Tavall Database.

PostgreSQL-specific native behavior is allowed only where the current Tavall Database contract supports it and the database-specific reason is documented and tested.

##### Why

Query and transaction semantics are persistence-runtime behavior. Keeping them with Tavall Database prevents every application feature from inventing a slightly different persistence dialect and lifecycle policy.

## Transaction Rules

Tavall Database owns:

- entity-manager/factory lifecycle;
- transaction begin/flush/commit/rollback;
- locked reads and database-specific operation mechanics;
- operation draining/shutdown;
- provider bootstrap and entity discovery.

Application code requests durable behavior through the installed Tavall Database entity contract. It does not receive a transaction callback and become a persistence runtime by accident.

When application behavior requires a missing multi-entity or transactional capability, add that capability to `tavall-database` first rather than rebuilding transaction ownership downstream.

##### Why

Transaction ownership determines what commits together, rolls back together, and may still be active during shutdown. One shared owner makes those semantics deterministic and testable.

## Discovery and Composition

Mapped types participate in discovery/composition according to the current Tavall Database module. Application platform surfaces do not create parallel entity factories, package catalogs, or transaction runtimes.

Do not:

- initialize a second entity factory for one feature;
- borrow a shared factory into a module-local transaction wrapper;
- maintain duplicate persistence discovery systems when Tavall Database owns discovery;
- let web, Discord, Paper, Velocity, game modes, or other product surfaces own separate transaction mechanics.

##### Why

Persistence discovery should follow one runtime contract. Parallel discovery/composition paths drift and split lifecycle ownership across the same process.

## Enforcement

Architecture tests must treat `*Repository` production declarations as a prohibited-name rule.

Existing declarations present at the adopted migration cutoff may be grandfathered only as explicit migration debt. Enforcement must prevent any new declaration from being added after that cutoff, and cleanup must never require adding another repository type.

Persistence audits should also reject application-owned JPA/JDBC/transaction mechanics that bypass the current Tavall Database entity contract.

##### Why

A naming rule without executable enforcement eventually becomes a suggestion. A debt ratchet allows existing code to migrate incrementally while making the obsolete architecture impossible to grow.
