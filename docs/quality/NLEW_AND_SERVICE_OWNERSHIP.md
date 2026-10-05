# NLEW and Service Ownership

> **Status:** Active
> **Authority:** Binding Tavall-wide terminology and ownership policy for Nodes, Lanes, Environments, Workspaces, Executors, and service placement
> **CI authority:** [CI_CD.md](CI_CD.md)
> **Supersedes:** General-purpose Cloud Environment wording and any Environment-first source/CI workflow

## Canonical rule

Tavall NLEW means **Nodes, Lanes, Environments, and Workspaces**. Executors are reusable execution capabilities selected by Tavall Cloud. These are distinct concepts, not a mandatory parent-child ladder and not the CI execution sequence.

Cloud Environments are reserved for registered logical-service runtime targets. Source repositories, branches, pull requests, CI jobs, Executors, and operation Workspaces do not create or require Environments.

The two paths are:

```text
Source and CI:
source provider -> exact repository and commit -> Tavall CI -> shared Cloud Executor
                -> operation-scoped Workspace -> typed evidence and immutable artifact

Service runtime:
registered logical service -> DEVELOPMENT / STAGING / PRODUCTION Environment
                           -> runtime generation, readiness, and routing
```

A service Environment remains attached to its registered logical service as source revisions, artifacts, runtime generations, and production slots advance. BLUE/GREEN are runtime slots beneath one stable service identity.

## Environment: service runtime only

A Cloud Environment represents one runtime target for one registered logical service. Create or resolve it through the service deployment/runtime lifecycle. Do not create an Environment for repository work, a branch, a PR, a build, a test, an Executor invocation, or a source Workspace.

The canonical runtime targets are:

- **DEVELOPMENT** for deployed development services and Development Staging validation;
- **STAGING** for production-equivalent validation of promoted immutable artifacts;
- **PRODUCTION** for accepted releases and their runtime slots.

Development Staging is a workflow role on DEVELOPMENT infrastructure, not a fourth Environment type. A service Environment carries that service's desired and observed runtime state, configuration, generation, health, and deployment evidence. It does not own source checkouts or CI jobs.

## NLEW responsibilities

### Node

A Node provides infrastructure capacity and placement capabilities. A host name or filesystem path is not a logical workload identity.

### Lane

A Lane coordinates related source work, PR ancestry, policy, and provenance when a workflow needs that coordination. A Git branch or staging PR is not automatically a Lane. A Lane does not own service Environments.

### Environment

An Environment is the runtime target for a registered logical service in one canonical runtime classification. It is not a general-purpose repository, CI, or developer-workspace container.

### Workspace

A Workspace is bounded source materialization and mutable execution state. Tavall CI may materialize one repository workspace folder per exact source inside a job's operation Workspace. Such folders do not become repository identity or service Environment state. A Cloud Workspace domain object is used only when an explicitly typed Cloud operation requires one; ordinary CI does not require it.

### Executor

An Executor is a reusable execution capability selected and managed by Tavall Cloud. Shared machine execution is the default. Executor lifetime and identity are independent of any service Environment or individual invocation; per-job mutable output remains isolated in that operation's Workspace.

## CI relationship

Tavall CI owns repository/module definition parsing, exact-source composition, Gradle/build planning, dependency resolution, typed checks, evidence, and immutable artifact identity. The repository owns its Gradle project graph and build intent. The Cloud Executor provides execution placement, Java/Gradle provisioning, filesystem isolation, and cache access.

Ordinary CI uses the exact source and the shared Executor without creating or resolving a service Environment. A workflow may carry Lane or Node policy when required, but an ordered NLEW chain is not a prerequisite for a CI job. See [CI_CD.md](CI_CD.md) for the required execution and evidence contract.

## Git and staging

Git integration and Cloud runtime topology remain separate:

```text
Git:   feature -> sub-staging -> repository staging -> main
Cloud: exact source -> Tavall CI -> shared Executor
       validated artifact -> registered service Environment
```

A persistent staging PR does not imply a persistent service Environment, Workspace, or dedicated Executor. Service Environments exist because a registered service has a runtime target, not because GitHub contains a branch named `staging`.

## Service filesystem rule

A host filesystem path is never canonical service identity or ownership. Logical service and Environment identity come from Tavall Cloud CONTROL and typed service/runtime definitions. Tavall Storage owns durable configuration, artifacts, evidence, and lineage; provider paths are materialization details. Changing a provider path must not change service identity.

## Compatibility and migration

Older documents and records may describe general-purpose Environments or attach source repositories and CI jobs to Environments. Treat those as historical implementation evidence and migration compatibility only. They do not authorize new Environment-bound source or CI work.

Migrate existing non-service Environment materializations through CONTROL after checking exact source, dirty/unmerged work, active operations, and durable evidence. Preserve active or unknown work; do not use a bulk deletion or reset to make the model appear clean. New source and CI work follows the Envless shared-Executor path defined by [CI_CD.md](CI_CD.md).

## Cross-repository authority

- `tavall-docs` owns this Tavall-wide terminology and service-only Environment rule.
- `tavall-ci` owns provider-neutral CI orchestration, exact-source composition, evidence, and delivery semantics.
- `tavall-cloud` owns concrete Nodes, Lanes, service Environments, Executors, storage, service placement, providers, and runtime behavior.

## OCI Images vs. Tavall Environment Definitions

Tavall architectures strictly distinguish between an **OCI image** (the immutable userspace artifact) and a **Tavall Environment Definition** (the runtime execution and placement policy).

```text
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│           OCI Image                  │     │     Tavall Environment Definition     │
│   (Immutable Userspace Artifact)     │     │     (Runtime Execution Policy)       │
├──────────────────────────────────────┤     ├──────────────────────────────────────┤
│ • Root filesystem layers             │     │ • Hardware & compute (CPU, RAM, GPU) │
│ • System packages, libraries, tools  │  +  │ • Volume mounts & persistent storage │
│ • Application binaries and runtimes  │     │ • Port bindings & ingress routing    │
│ • Base default user & PATH           │     │ • Secret & credential injections     │
│ • Default ENTRYPOINT / CMD           │     │ • Capability grants & security opts  │
└──────────────────────────────────────┘     │ • Placement rules & restart policy   │
                                             └──────────────────┬───────────────────┘
                                                                │
                                                                ▼
                                             ┌──────────────────────────────────────┐
                                             │     Running Service Container        │
                                             │  (OCI Image instantiated under       │
                                             │   Environment Policy)                │
                                             └──────────────────────────────────────┘
```

### What an OCI Image Is

An **OCI Image** is an immutable, portable userspace filesystem artifact stored in a container registry:
- **Filesystem Layers**: The Linux distribution rootfs, packages, shared libraries, and application runtime binaries (e.g. JDK, Node.js).
- **Default Baseline Environment**: Declares the default non-root user (`USER`), working directory (`WORKDIR`), default PATH, and default execution entrypoint (`ENTRYPOINT` / `CMD`).
- **Build Output**: It is produced by a build process (Dockerfile / buildx / kaniko) and identified by a content digest (SHA-256).

### What a Tavall Environment Definition Is

A **Tavall Environment Definition** is the declared, versioned runtime policy that governs how and where an OCI image executes:
- **Compute & Resource Limits**: CPU allocations, memory limits, swap constraints, and GPU reservations.
- **Mounts & Storage Volumes**: Bind mounts, ephemeral scratch disks, and persistent stateful volume attachments.
- **Networking & Ingress**: Virtual network attachments, port mappings, internal DNS identities, and TLS ingress routing.
- **Secrets & Configuration Bindings**: Injection of runtime credentials, environment variable values, configuration files, and token resolvers.
- **Capability Grants & Security Profiles**: AppArmor / SELinux profiles, seccomp filters, Linux capability drops (`CAP_DROP`), and user namespace mappings.
- **Persistence & State Semantics**: Ephemeral vs stateful lifecycle guarantees, backup triggers, and snapshot boundaries.
- **Lifecycle & Placement Rules**: Node affinity, anti-affinity, tolerations, health probes (liveness, readiness), restart policies, and rollout strategies (e.g. Blue/Green slots).

---

## Prohibited Anti-Patterns

### 1. Prohibited: Treating OCI Images as Environments
An OCI image is NOT an environment. Running an image with ambient host defaults is strictly prohibited in production. A container is only an instantiated Environment when combined with an explicit, versioned Tavall Environment Definition governing its resources, secrets, and network placement.

### 2. Prohibited: Treating Environment Definitions as Image Builds
Environment definitions must not compile source code or build OCI images. The OCI image must already exist as an immutable, verified artifact prior to environment instantiation.

### 3. Prohibited: Host-Leaking Paths (`/srv/...`)
Environment definitions must specify portable, logical volume names and mount paths (e.g. `volume: data-storage -> /var/data/tavall`). Host paths (such as `/srv/dev-storage/...` or `/home/...`) must NEVER be embedded into canonical environment definitions or image configurations. Physical host placement is managed dynamically by Tavall Cloud Nodes at instantiation time.

### 4. Prohibited: Conflating Node, Lane, Environment, and Workspace
- A **Node** is compute capacity, not an application environment.
- A **Lane** is workflow/PR ancestry, not a runtime target.
- An **Environment** is a logical service runtime target (DEVELOPMENT, STAGING, PRODUCTION), not a Git branch.
- A **Workspace** is isolated source checkouts and temporary CI build folders, never service runtime state.

