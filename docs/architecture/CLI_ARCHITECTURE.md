# Tavall CLI Architecture

## 1. Overview and Primary Objective

`TavallStudios/tavall-cli` is the canonical reusable **Tavall CLI framework**.

The root executable is:

```text
tavall
```

Product and system command families are separate owning modules:

```text
tavall cloud ...       (owned by TavallStudios/tavall-cloud via tavall-cloud-cli)
tavall ci ...          (owned by TavallStudios/tavall-ci via tavall-ci-cli)
tavall harness ...     (owned by TavallStudios/tavall-open-harness via tavall-main-harness)
tavall process ...     (owned by TavallStudios/tavall-open-harness via tavall-main-harness)
```

The CLI framework never accumulates domain behavior (Cloud, CI, AI, Minecraft, deployment, or worker infrastructure).

- **The CLI framework** owns command mechanics (parsing, routing, validation, error mapping, exit codes, output formatting, discovery).
- **Owning systems** own their subcommands and CLI adapters in dedicated `-cli` modules.
- **Typed Java capabilities** own actual business and domain behavior.
- **Tavall DI** owns object graphs, lifecycle, and composition.

Provider discovery is scoped to the modules present on a `TavallCliApplication` runtime classpath. The source-level Cloud, CI, and Harness providers do not by themselves prove that one approved installed distribution loads all three.

---

## 2. Canonical Ownership and Dependency Model

```text
                     ┌─────────────────────────┐
                     │       tavall-cli        │
                     │ framework + executable  │
                     └────────────┬────────────┘
                                  │
                           tavall-cli-api
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      tavall-cloud-cli       tavall-ci-cli      other *-cli module
             │                    │                    │
             ▼                    ▼                    ▼
       Cloud Java API         CI Java API         owning Java API
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                              tavall-di
```

### Critical Separation Principle

```text
CLI command
    -> parse/adapt typed CLI input
    -> construct/call typed domain request/capability
    -> receive typed result
    -> render result

CLI command != business implementation
```

Same-JVM Java code **must** call typed Java capabilities directly. 

**Prohibited Anti-Pattern:**
```text
Java consumer
    -> launch tavall CLI subprocess
    -> parse stdout
    -> recover Java object
```

When both sides share a JVM, the CLI is an external ingress adapter, not an internal IPC protocol.

---

## 3. Tavall DI as a First-Class Citizen

**Constructor injection is NOT the Tavall managed-dependency pattern.**

CLI commands are behavioral components within the Tavall architecture. Consequently, they participate fully in `tavall-di`:

1. **Interface Contract First:** Every concrete command implements a domain command interface (e.g. `ICloudServiceDeployCLICommand`, `ICiValidateCLICommand`).
2. **`@DelegatesTo` Declaration:** The concrete implementation declares `@DelegatesTo(IDomainCLICommand.class)`.
3. **`DependencyAccess` for Collaborators:** Commands implement `DependencyAccess<...>` or domain bundles to access collaborators via `getInstance().myCapability()`.
4. **No Constructor Injection:** Commands must never declare constructors accepting managed collaborators.
5. **No Direct Map Access:** Commands do not interact directly with `IDependencyMap` or `DependencyMap`. Dependency lookup infrastructure is restricted to `@CompositionBoundary` roots.

### Canonical CLI Command Pattern

```java
public interface ICloudServiceDeployCLICommand extends ICLICommand<CloudServiceDeployResult> {
}

@DelegatesTo(ICloudServiceDeployCLICommand.class)
public final class CloudServiceDeployCLICommand
        extends CLICommand<CloudServiceDeployResult>
        implements ICloudServiceDeployCLICommand,
                   DependencyAccess<ICloudServiceOperations, ILogger> {

    public CloudServiceDeployCLICommand() {
        super(CLICommandBuilder.create("cloud", "service", "deploy")
                .description("Deploy a service")
                .argument(CLICommandArgument.required("service", "Target service name"))
                .option(CLICommandOption.optional("image", "Image reference", "latest"))
                .build());
    }

    @Override
    protected CloudServiceDeployResult handle(CLICommandInput input) {
        String service = input.argument("service");
        String image = input.findOption("image").orElse("latest");
        return getInstance().cloudServiceOperations().deploy(new CloudDeployRequest(service, image));
    }
}
```

`ICLICommand.execute(CLICommandInput)` returns `CLICommandResult`. `CLICommand<R>` validates input, maps execution errors, and converts the typed `R` returned by `handle` into that non-generic result.

---

## 4. Extensibility and Bootstrap Discovery

Command modules register with the root executable via the Java Service Provider Interface (SPI):

```text
META-INF/services/org.tavall.cli.api.bootstrap.ICLIBootstrap
```

Each owning module supplies an `ICLIBootstrap` implementation (e.g. `CloudCLIBootstrap`, `CiCLIBootstrap`, `HarnessCLIBootstrap`) that registers its subcommands into the shared `CLICommandRegistry`:

```java
public final class CiCLIBootstrap implements ICLIBootstrap {
    @Override
    public void registerCommands(ICLICommandRegistry registry) {
        registry.registerCommand(new CiRootCLICommand());
        registry.registerCommand(new CiValidateCLICommand());
        registry.registerCommand(new CiPlanCLICommand());
        registry.registerCommand(new CiExecuteCLICommand());
        ...
    }
}
```

`TavallCliApplication` discovers bootstrap providers present on its runtime classpath, initializes the shared CLI composition, constructs the command tree, and executes incoming requests. The owning distribution determines which provider modules are packaged.
