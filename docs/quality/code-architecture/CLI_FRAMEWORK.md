# Tavall CLI Framework

## 1. Scope and Design Principles

The Tavall CLI Framework provides the foundation for command-line interfaces across Tavall Studios.

It embodies the core Tavall engineering principles:
- **Interface-First Design:** Contracts are defined in `tavall-cli-api`; runtime and execution mechanics live in `tavall-cli`.
- **Framework Base vs. Domain Specialization:** `CLICommand<R>` owns execution plumbing, error wrapping, and settings enforcement; concrete commands own argument definitions and domain delegation.
- **Tavall DI Composition:** Commands are DI-managed components using `@DelegatesTo` and `DependencyAccess<...>`. Constructor injection of collaborators is prohibited.
- **Adapter Default:** CLI commands adapt command-line arguments to typed Java domain calls. They never implement business logic.

---

## 2. Core Abstractions and Contracts

### 2.1 Command Hierarchy

```text
ICLICommand<R>
      ▲
      │
CLICommand<R>
      ▲
      │
[Concrete Domain Command]
```

- `ICLICommand<R>`: Behavioral contract representing a command in the command tree. Defines `path()`, `settings()`, and `execute(CLICommandContext)`.
- `CLICommand<R>`: Abstract base class implementing execution mechanics, exception-to-exit-code mapping, and settings validation.

### 2.2 Command Definition and Settings

Commands configure their metadata and inputs during construction via `CLICommandSettings` and `CLICommandBuilder`:

```java
CLICommandSettings settings = CLICommandSettings.builder()
        .name("validate")
        .description("Validate CI workspace configuration")
        .path(CLICommandPath.of("ci", "validate"))
        .addArgument(CLICommandArgument.required("workspace", "Path to target workspace"))
        .addOption(CLICommandOption.optional("profile", "Validation execution profile", "default"))
        .build();
```

- `CLICommandPath`: Path segments representing the position in the command hierarchy (e.g. `ci validate`).
- `CLICommandArgument<T>`: Positional argument definition.
- `CLICommandOption<T>`: Named command-line option/flag (e.g. `--profile <value>`, `--dry-run`).

### 2.3 Input and Execution Context

During execution, commands interact with:
- `CLICommandContext`: Provides access to the parsed input, terminal output writer, command registry, and environment.
- `CLICommandInput`: Encapsulates parsed positional arguments (`input.argument("name")`) and options (`input.option("name")`).
- `CLIExecutionResult<R>`: Outcome envelope containing the exit code (`0` for success, non-zero for failures), typed domain result value, and diagnostic messages.

---

## 3. Dependency Injection and Architecture Rules

CLI commands participate in `tavall-di` following the same invariants as all other behavioral components in Tavall:

### Rule 1: Interface Contract First
Every command extending `CLICommand<R>` must implement a domain-specific interface:

```java
public interface ICiValidateCLICommand extends ICLICommand<CiValidationResult> {
}
```

### Rule 2: `@DelegatesTo` Annotation
The implementation must declare its delegation contract:

```java
@DelegatesTo(ICiValidateCLICommand.class)
public final class CiValidateCLICommand
        extends CLICommand<CiValidationResult>
        implements ICiValidateCLICommand,
                   DependencyAccess<ICiWorkspaceValidator, ILogger> {
    ...
}
```

### Rule 3: Zero Constructor Injection of Collaborators
Commands must not take managed dependencies via constructor parameters:

```java
// PROHIBITED:
public CiValidateCLICommand(ICiWorkspaceValidator validator, ILogger logger) { ... }

// CANONICAL:
public CiValidateCLICommand() {
    super(CLICommandSettings.builder()
            .name("validate")
            ...
            .build());
}
```

### Rule 4: Typed DependencyAccess
Commands resolve collaborators through `DependencyAccess<...>`:

```java
@Override
public CLIExecutionResult<CiValidationResult> execute(CLICommandContext context) {
    String workspace = context.input().argument("workspace");
    
    CiValidationResult result = getInstance().ciWorkspaceValidator().validate(workspace);
    return CLIExecutionResult.success(result);
}
```

### Rule 5: Direct Java Capability Default
The CLI command is an adapter. Java callers inside the same JVM must call typed domain services directly, never invoking the CLI as a subprocess or parsing CLI stdout.

---

## 4. Subsystem Integration and SPI Bootstrap

Owning repositories (e.g. `tavall-cloud`, `tavall-ci`, `tavall-open-harness`) create dedicated `-cli` modules to publish subcommands:

1. Subsystem defines commands extending `CLICommand<R>`.
2. Subsystem implements `ICLIBootstrap`:
   ```java
   public final class CiCLIBootstrap implements ICLIBootstrap {
       @Override
       public void bootstrap(ICLIBootstrapContext context) {
           context.registry().register(new CiRootCLICommand());
           context.registry().register(new CiValidateCLICommand());
       }
   }
   ```
3. Subsystem registers the bootstrap in `META-INF/services/org.tavall.cli.api.bootstrap.ICLIBootstrap`.
4. `TavallCliApplication` automatically discovers all registered bootstraps via `ServiceLoader`, constructing a unified CLI tree under `tavall`.
