# Project Novus Interfaces and Abstractions

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

### Abstracts

This codebase uses an interface-first design.

Most service, repository, cache, resolver, registry, command, and handler classes should have an interface. Dependencies should be wired against interfaces, not concrete classes.

The goal is decoupling, safer refactors, cleaner testing, easier replacement, and better control over dependency wiring.

#### Interfaces

Interfaces define what a class provides without forcing callers to care about how that behavior is implemented.

Use interfaces for:

* Services
* Repositories
* Caches
* Resolvers
* Registries
* Commands
* Handlers
* Formatters
* Loaders
* Writers
* Readers

An interface with one current implementation is still valid when it is part of the dependency graph. The interface is the contract. The concrete class is just the current implementation.

##### Interface Naming

Interfaces should be named after their concrete class or describe the role or contract.

Preferred: matching the concrete class name with `I` before the name.

Example:
`PermissionService` → `IPermissionService`

This makes it easy to tell what is and is not an interface by name alone, because apparently opening the file was too much cardio.

#### Bad Abstraction: Depending on Concrete Classes

```java
public final class PunishmentCommand {

    private final PermissionService permissionHandler;
    private final PunishmentService punishmentService;
    private final MessageResolver messageResolver;

    public PunishmentCommand(
        PermissionService permissionHandler,
        PunishmentService punishmentService,
        MessageResolver messageResolver
    ) {
        this.permissionHandler = permissionHandler;
        this.punishmentService = punishmentService;
        this.messageResolver = messageResolver;
    }
}
```

##### Why

This command is locked directly to concrete classes.

If the implementation changes, the command has to change too. That defeats the point of using an interface-first dependency system.

#### Good Abstraction: Depending on Interfaces

```java
public interface IPermissionService {

    boolean has(PermissionProfile profile, PermissionNode node);

    boolean canPunish(PermissionProfile staffProfile, PermissionProfile targetProfile);
}
```

```java
public interface IPunishmentService {

    PunishmentResult ban(PunishmentRequest request);

    PunishmentResult mute(PunishmentRequest request);
}
```

```java
public interface IMessageResolver {

    String resolve(MessageKey key);

    String resolve(MessageKey key, Map<String, String> placeholders);
}
```

```java
public final class PermissionService implements IPermissionService {

    @Override
    public boolean has(PermissionProfile profile, PermissionNode node) {
        return profile.has(node);
    }

    @Override
    public boolean canPunish(PermissionProfile staffProfile, PermissionProfile targetProfile) {
        return staffProfile.powerLevel() > targetProfile.powerLevel();
    }
}
```

```java
public final class PunishmentCommand {

    private final IPermissionService permissionHandler;
    private final IPunishmentService punishmentService;
    private final IMessageResolver messageResolver;

    public PunishmentCommand(
        IPermissionService permissionHandler,
        IPunishmentService punishmentService,
        IMessageResolver messageResolver
    ) {
        this.permissionHandler = permissionHandler;
        this.punishmentService = punishmentService;
        this.messageResolver = messageResolver;
    }
}
```

##### Why

The command depends on contracts, not implementations.

It does not care how permissions are checked, how punishments are stored, or how messages are resolved. It only cares that those behaviors exist.

That keeps command logic clean and lets the underlying systems change without dragging every caller into the mud.

#### Data Handler Example

```java
public interface IPunishmentDataHandler {

    void save(Punishment punishment);

    Optional<Punishment> findActiveByTarget(UUID targetId, PunishmentType type);
}
```

```java
public final class PunishmentDataHandler implements IPunishmentDataHandler {

    @Override
    public void save(Punishment punishment) {
        // write punishment to Postgres
    }

    @Override
    public Optional<Punishment> findActiveByTarget(UUID targetId, PunishmentType type) {
        // read active punishment from Postgres
        return Optional.empty();
    }
}
```

```java
public final class PunishmentHandler implements IPunishmentService {

    private final IPunishmentRepository punishmentRepository;
    private final IPermissionHandler permissionHandler;

    public PunishmentHandler(
        IPunishmentRepository punishmentRepository,
        IPermissionHandler permissionHandler
    ) {
        this.punishmentRepository = punishmentRepository;
        this.permissionHandler = permissionHandler;
    }

    @Override
    public PunishmentResult ban(PunishmentRequest request) {
        PermissionProfile staffProfile = request.staffProfile();
        PermissionProfile targetProfile = request.targetProfile();

        if (!permissionHandler.canPunish(staffProfile, targetProfile)) {
            return PunishmentResult.denied();
        }

        Punishment punishment = Punishment.ban(request);
        punishmentRepository.save(punishment);

        return PunishmentResult.success();
    }

    @Override
    public PunishmentResult mute(PunishmentRequest request) {
        PermissionProfile staffProfile = request.staffProfile();
        PermissionProfile targetProfile = request.targetProfile();

        if (!permissionHandler.canPunish(staffProfile, targetProfile)) {
            return PunishmentResult.denied();
        }

        Punishment punishment = Punishment.mute(request);
        punishmentRepository.save(punishment);

        return PunishmentResult.success();
    }
}
```

##### Why

The service uses repository and permission interfaces instead of concrete implementations.

That means the persistence layer can change without changing punishment logic. Postgres, memory, test fake, or some future storage crime scene can all implement the same interface.

#### Abstract Classes

Interfaces are for contracts.

Abstract classes are for shared behavior.

Use abstract classes only when multiple implementations truly share logic, state, or lifecycle.

```java
public interface IRegistry<KeyType, ValueType> {

    void register(KeyType key, ValueType value);

    Optional<ValueType> find(KeyType key);
}
```

```java
public abstract class AbstractRegistry<KeyType, ValueType> implements IRegistry<KeyType, ValueType> {

    private final Map<KeyType, ValueType> values = new HashMap<>();

    @Override
    public void register(KeyType key, ValueType value) {
        validateKey(key);
        validateValue(value);

        values.put(key, value);
    }

    @Override
    public Optional<ValueType> find(KeyType key) {
        return Optional.ofNullable(values.get(key));
    }

    protected abstract void validateKey(KeyType key);

    protected abstract void validateValue(ValueType value);
}
```

```java
public interface IPermissionNodeRegistry extends IRegistry<PermissionNode, PermissionDefinition> {
}
```

```java
public final class PermissionNodeRegistry
    extends AbstractRegistry<PermissionNode, PermissionDefinition>
    implements IPermissionNodeRegistry {

    @Override
    protected void validateKey(PermissionNode node) {
        if (node == null) {
            throw new IllegalArgumentException("Permission node cannot be null.");
        }
    }

    @Override
    protected void validateValue(PermissionDefinition definition) {
        if (definition == null) {
            throw new IllegalArgumentException("Permission definition cannot be null.");
        }
    }
}
```

##### Why

The interface gives the dependency graph a clean contract.

The abstract class provides shared registry behavior.

The concrete class provides the domain-specific validation.

This keeps the code decoupled without turning it into inheritance lasagna, which is somehow less delicious than regular lasagna and much harder to debug.

#### Rule

Use interfaces by default for dependency-injected classes.

Depend on interfaces, not concrete implementations.

Use abstract classes only when shared implementation logic actually exists.

Interfaces define the contract. Concrete classes provide the implementation. Abstract classes share mechanics when reuse is real.
