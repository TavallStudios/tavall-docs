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
        super(CLICommandSettings.builder()
                .name("deploy")
                .description("Deploy a service")
                .path(CLICommandPath.of("cloud", "service", "deploy"))
                .addArgument(CLICommandArgument.required("service", "Target service name"))
                .addOption(CLICommandOption.optional("image", "Image reference", "latest"))
                .build());
    }

    @Override
    public CLIExecutionResult<CloudServiceDeployResult> execute(CLICommandContext context) {
        String service = context.input().argument("service");
        String image = context.input().option("image").orElse("latest");

        CloudServiceDeployResult result = getInstance().cloudServiceOperations()
                .deploy(new CloudDeployRequest(service, image));

        return CLIExecutionResult.success(result);
    }
}
```

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
    public void bootstrap(ICLIBootstrapContext context) {
        ICLICommandRegistry registry = context.registry();
        registry.register(new CiRootCLICommand());
        registry.register(new CiValidateCLICommand());
        registry.register(new CiPlanCLICommand());
        registry.register(new CiExecuteCLICommand());
        ...
    }
}
```

`TavallCliApplication` discovers all registered bootstraps dynamically, initializes DI composition roots, constructs the command tree, and executes incoming requests.
