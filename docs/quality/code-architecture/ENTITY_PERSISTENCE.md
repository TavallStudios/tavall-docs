# Project Novus Entity Persistence

> **Status:** Active  
> **Authority:** Binding persistence specialization of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All production Project Novus modules, generated code, automation, and AI-assisted changes

Project modules declare mapped JPA entities. Tavall Database owns the persistence runtime and exposes entity-oriented operations. Feature code does not own an `EntityManager`, transaction callback, factory, connection, prepared statement, or generic CRUD repository.

## Binding Rule

Production application code must not call:

```java
database.jpa().read(...);
database.jpa().write(...);
```

It must not create a local equivalent around `IPostgresJpaContext`, `EntityManagerFactory`, or `EntityTransaction` either. Replacing one forbidden callback with another wrapper only adds upholstery to the same architectural mistake.

Use the Tavall Database entity boundary:

```java
Optional<NovusWebContentDocumentEntity> document =
        database.entities().find(
                NovusWebContentDocumentEntity.class,
                documentKey
        );

database.entities().save(entity);
```

The `IPostgresDatabase.jpa()` compatibility surface belongs to Tavall Database migration and infrastructure internals. It is not an application API.

##### Why

Entity and transaction lifecycle are infrastructure concerns with process-wide failure, shutdown, retry, and consistency consequences. Letting feature code own callbacks or entity managers turns every caller into a partial persistence runtime with slightly different cleanup and transaction behavior.

The typed entity boundary keeps application code focused on durable operations while Tavall Database owns the mechanics required to make those operations safe and replaceable.

## Entity Ownership

A durable table is represented by an owning mapped entity or a small cohesive entity family.

The entity owns:

- table and column mapping;
- primary or composite identity;
- enum, JSON, and timestamp mapping;
- named JPQL queries for domain lookup;
- named native operations only when PostgreSQL behavior cannot be expressed correctly through entity operations;
- conversion to and from the domain value when a separate domain record is useful.

The entity does not own:

- gameplay orchestration;
- command or controller behavior;
- caches or registries;
- network delivery;
- manual connection or transaction lifecycle;
- schema creation or migration.

##### Why

An entity defines how durable data maps to storage; it should not become the application behavior that happens to use that data. Mixing gameplay or delivery into entities couples persistence shape to product rules and makes migrations responsible for unrelated behavior.

Keeping entity ownership narrow also lets the same durable representation serve handlers, jobs, web, Discord, and tests without dragging those surfaces into the persistence model.

## Repository Removal

Do not create a `Postgres*Repository` for ordinary entity lookup, save, update, or delete.

When migrating an existing repository:

1. Add or complete the mapped entity.
2. Move query definitions onto that entity as named queries.
3. Route operations through `IPostgresDatabase.entities()`.
4. Move domain sequencing into a service or handler only when sequencing is real business behavior.
5. Reduce the old repository to a temporary compatibility adapter when callers cannot move atomically.
6. Delete the adapter and its DI token once callers use the entity boundary.
7. Remove the old class from the storage debt baseline in the same coherent migration.

A compatibility adapter may translate domain records and exceptions. It must not contain SQL, JPQL, an `EntityManager`, a transaction callback, or lifecycle ownership.

##### Why

A repository that merely forwards generic CRUD to JPA duplicates an abstraction Tavall Database already owns. Each duplicate becomes another place to invent transaction behavior, exception handling, query strings, and lifecycle policy.

Removing pass-through repositories leaves repositories or handlers only where they add real domain or persistence policy, instead of preserving a class layer whose main achievement is making `save()` travel farther.

## Query Rules

Prefer named JPQL queries on the entity:

```java
@NamedQuery(
        name = MessageConfigEntity.FIND_BY_LOOKUP,
        query = """
                SELECT entity
                FROM MessageConfigEntity entity
                WHERE entity.messageKey = :messageKey
                  AND entity.locale = :locale
                  AND entity.platformType = :platformType
                """
)
```

Use named native queries only for a documented PostgreSQL contract such as atomic `ON CONFLICT`, JSONB operators, advisory locking, bulk mutation, or aggregation that JPA cannot express cleanly. Include a nearby `Native SQL reason:` comment.

Ad hoc query strings inside services, handlers, controllers, listeners, and compatibility adapters are forbidden.

##### Why

Named queries keep persistence contracts discoverable beside the mapped data they operate on and give one place to review parameter names, result shape, and database assumptions.

Native SQL remains available when PostgreSQL semantics are the feature, but requiring an explicit reason prevents ordinary CRUD from bypassing typed entity operations simply because writing a string happened to be faster that afternoon.

## Transaction Rules

Tavall Database owns:

- `EntityManager` creation and closure;
- transaction begin, flush, commit, and rollback;
- locked entity reads;
- operation draining and database shutdown;
- provider bootstrap and entity discovery.

A Project Novus class may request an entity operation. It may not receive an `EntityManager` callback and become the transaction owner by accident.

Multi-entity business changes require an explicit Tavall Database operation type supplied by the database module. Do not recreate transaction callbacks in Project Novus while waiting for that operation to exist. Add the missing typed operation upstream first.

##### Why

Transaction ownership determines what commits together, what rolls back together, and what can still be running during shutdown. Those semantics cannot be safely distributed among arbitrary feature classes without creating overlapping owners and partial failure behavior that differs by caller.

Typed database operations make the transaction boundary explicit while preserving one runtime owner for resource lifecycle and rollback behavior.

## Discovery and Composition

Tavall Database discovers available first-party mapped types beneath `org.tavall` before its lazy entity runtime initializes. Project modules contribute `@Entity`, `@Embeddable`, `@MappedSuperclass`, and `@Converter` classes by placing them in their owning domain packages. They do not maintain parallel package lists in Bukkit, Velocity, web, Discord, or FFA composition roots.

Explicit package registration remains available for non-Tavall integration types. The entity scanner may skip unrelated optional classes that cannot load in the current process, but an available mapped entity must be discovered and validated by focused integration coverage.

Do not:

- initialize a second entity factory for one feature;
- borrow a shared factory into a module-local transaction wrapper;
- maintain feature-specific entity-package registries for first-party types;
- let Discord, web, Velocity, Bukkit, or FFA own separate transaction mechanics.

##### Why

First-party entity discovery should follow code ownership, not require every runtime surface to maintain a second catalog of persistence types. Parallel package lists drift as modules evolve and make correctness depend on which composition root remembered to update its copy.

One discovery path also prevents each platform from bootstrapping its own entity factory and splitting transaction, connection, and shutdown ownership across the same process.

## Enforcement

`.github/scripts/audit_storage_architecture.py` fails on direct `.jpa().read(...)` and `.jpa().write(...)` calls in production source. Existing callback wrappers are printed as migration debt and must decline over time.

A pull request may not add a callback owner to a baseline. It must either use mapped entities through Tavall Database or extend Tavall Database with the missing typed entity operation first.

##### Why

Persistence ownership is easy to regress because a local callback can look harmless while reintroducing the exact lifecycle boundary the architecture removed. Automated enforcement turns the rule into a ratchet: known debt can disappear, but new debt cannot quietly become precedent.

Requiring the missing operation to be added upstream also improves the shared persistence API instead of teaching each feature to route around it.