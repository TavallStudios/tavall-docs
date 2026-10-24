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

- `ICLICommand<R>`: Behavioral contract representing a command in the command tree. Defines `path()`, `settings()`, and `execute(CLICommandInput)`, which returns `CLICommandResult`.
- `CLICommand<R>`: Abstract base class implementing execution mechanics, exception-to-exit-code mapping, and settings validation. Concrete subclasses implement typed `handle(CLICommandInput)` behavior.

### 2.2 Command Definition and Settings

Commands configure their metadata and inputs during construction with `CLICommandBuilder`:

```java
CLICommandSettings settings = CLICommandBuilder.create("ci", "validate")
        .description("Validate CI workspace configuration")
        .argument(CLICommandArgument.required("workspace", "Path to target workspace"))
        .option(CLICommandOption.optional("profile", "Validation execution profile", "default"))
        .build();
```

- `CLICommandPath`: Path segments representing the position in the command hierarchy (e.g. `ci validate`).
- `CLICommandArgument<T>`: Positional argument definition.
- `CLICommandOption<T>`: Named command-line option/flag (e.g. `--profile <value>`, `--dry-run`).
- `CLICommandBuilder.trailingArguments(name, description)`: Opts in to an opaque token tail after the declared positional arguments. The default remains strict; the parser preserves token boundaries in `CLICommandInput.trailingArguments()`.

### 2.3 Input and Execution Context

During execution, commands receive:
- `CLICommandInput`: Immutable command path, raw tokens, parsed positional arguments and options, optional opaque trailing tokens, caller id, and metadata.
- `CLICommandResult`: Non-generic outcome carrying success, exit code, message, failure reason, data, and an optional payload. `CLICommand<R>` maps its typed domain result into this outcome.

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
    super(CLICommandBuilder.create("ci", "validate")
            .description("Validate CI workspace configuration")
            .argument(CLICommandArgument.required("workspace", "Path to target workspace"))
            .option(CLICommandOption.optional("profile", "Validation execution profile", "default"))
            .build());
}
```

### Rule 4: Typed DependencyAccess
Commands resolve collaborators through `DependencyAccess<...>`:

```java
@Override
protected CiValidationResult handle(CLICommandInput input) {
    String workspace = input.argument("workspace");
    
    return getInstance().ciWorkspaceValidator().validate(workspace);
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
       public void registerCommands(ICLICommandRegistry registry) {
           registry.registerCommand(new CiRootCLICommand());
           registry.registerCommand(new CiValidateCLICommand());
       }
   }
   ```
3. Subsystem registers the bootstrap in `META-INF/services/org.tavall.cli.api.bootstrap.ICLIBootstrap`.
4. `TavallCliApplication` discovers bootstrap providers present on its runtime classpath via `ServiceLoader`. The owning distribution determines which provider modules are packaged; source-level provider discovery alone does not prove that one installed organization-wide distribution loads every provider.
