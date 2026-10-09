# NLEW and Service Ownership

> **Status:** Active
> **Authority:** Binding Tavall-wide terminology and ownership policy for Nodes, Lanes, Environments, Workspaces, Executors, and service placement
> **CI authority:** [CI_CD.md](CI_CD.md)
> **Supersedes:** The service-only Environment wording restored by PR #56 (`ffd501f`, 2026-10-03). The general-purpose Environment model from `d36588f` is restored; the Envless source/CI default from PR #56 is retained.
> **Code owners:** reusable NLEW contracts and domain behavior — [`TavallStudios/tavall-nlew`](https://github.com/TavallStudios/tavall-nlew); concrete Cloud operation — [`TavallStudios/tavall-cloud`](https://github.com/TavallStudios/tavall-cloud)

## Canonical rule

Tavall NLEW is **Nodes, Lanes, Environments, and Workspaces**. Executors are reusable execution capabilities selected by Tavall Cloud and are not NLEWs. These are distinct ownership and execution concepts. They are not a mandatory containment ladder, not the CI execution sequence, and their names must not be used as aliases for Git branches, pull requests, staging tiers, source checkouts, or host filesystem paths.

Relationships between NLEWs are **explicitly typed and individually optional**. No concept is implicitly the parent of another:

- an Environment may exist without a Lane, a Workspace, or any service;
- a Lane may be used without creating an Environment;
- a Workspace is not automatically an Environment or Lane child;
- execution does not require an Environment, and an Executor does not require a Workspace unless the typed operation needs bounded materialization.

An **Environment is general-purpose**. It is an ownership/context boundary that may hold workloads, resources, repository/runtime context, integration context, services, or other durable/ephemeral state allowed by its policy. Its lifecycle (`DURABLE` / `EPHEMERAL`), mutability (`MUTABLE` / `IMMUTABLE`), work, service, resource, and runtime policies are independent dimensions. A service is **not** what makes an Environment an Environment.

## Service default

Registered logical services **default to Environment ownership and placement**, so long-lived service runtime state, configuration, generations, provider materialization, readiness, scaling, and service-local resources are not owned by a Lane, an operation Workspace, or an Executor merely because those scopes built or deployed the service.

The canonical service runtime classifications are:

- **DEVELOPMENT** for deployed development services and Development Staging validation;
- **STAGING** for production-equivalent validation of promoted immutable artifacts;
- **PRODUCTION** for accepted releases and their runtime slots.

Development Staging is a workflow role on DEVELOPMENT infrastructure, not a fourth classification. BLUE/GREEN are runtime slots beneath one stable service identity. A service Environment remains attached to its registered logical service as source revisions, artifacts, runtime generations, and production slots advance.

```text
source / engineering work
        |
        v
      Lane (when coordination is needed)
        |
        +--> Executor --> operation Workspace --> artifact / evidence
        |
        v
Environment  <--- default durable owner for a deployed logical service
    |
    +--> service runtime generations / provider materialization
    +--> other Environment-owned workloads/resources as policy allows
```

The diagram shows a common workflow, not a required parent/child hierarchy.

## NLEW responsibilities

### Node

A Node provides placement, infrastructure capacity, capabilities, available providers, classification, and runtime hosting references. A host name or filesystem path is not a logical workload identity.

### Lane

A Lane is an optional coordination, source, provenance, and policy scope. A Git branch or staging PR is not automatically a Lane. A Lane does not own Environments; a Lane-to-Environment relationship is an explicit typed relationship when one exists.

### Environment

An Environment is a reusable general-purpose ownership/context boundary with independently configured lifecycle, mutability, work, service, resource, and runtime policies. An Environment with zero services is valid.

Do not state or implement any of the following:

- `Environment == service runtime`;
- an Environment is service-only or may only be created during deployment;
- every Environment requires a service, a Lane, or a Workspace;
- every source operation or Executor invocation requires an Environment.

### Workspace

A Workspace is a bounded work/materialization scope used for source materialization, edits, builds, tests, generated files, and other bounded work when an operation requires one. Workspace sharing (`SHARED` / `DEDICATED`) is its own typed classification, independent of resource modes such as `SYSTEM`. Workspaces must not silently become durable service owners because deployment was initiated from them.

### Executor

An Executor executes authorized work. Executor identity, selection, permissions, leases, and lifetime are independent of any Environment, Lane, Workspace, or individual invocation. Shared machine execution is the default; per-job mutable output remains isolated in that operation's Workspace. Executor contracts are owned by Tavall Cloud, not by `tavall-nlew`; NLEW relationships may reference an Executor by typed identity.

## CI relationship

Tavall CI owns repository/module definition parsing, exact-source composition, Gradle/build planning, dependency resolution, typed checks, evidence, and immutable artifact identity. The repository owns its Gradle project graph and build intent. The Cloud Executor provides execution placement, Java/Gradle provisioning, filesystem isolation, and cache access.

Ordinary CI uses the exact source and the shared Executor without creating or resolving an Environment:

```text
source provider -> exact repository and commit -> Tavall CI -> shared Cloud Executor
                -> operation-scoped Workspace -> typed evidence and immutable artifact
```

This is the source/CI default, not an Environment type restriction. A workflow may carry Lane or Node policy when required, and an integration workflow may explicitly use an Environment only when Environment ownership is materially required by the runtime being exercised. An ordered NLEW chain is never a prerequisite for a CI job. See [CI_CD.md](CI_CD.md).

## Git and staging

Git integration and Cloud runtime topology remain separate:

```text
Git:   feature -> Development Staging / Runtime PR -> repository/release Staging -> main
Cloud: Node / Lane / Environment / Workspace / Executor relationships chosen by execution need
```

A persistent staging PR does not imply a persistent Lane, Environment, Workspace, or dedicated Executor.

## Service filesystem rule

A host filesystem path is **never** canonical service, Environment, Lane, Workspace, or Node identity.

- Logical identity comes from Tavall Cloud CONTROL and typed NLEW/service definitions.
- Physical materialization roots are configured provider details. Changing a provider path must not change identity.
- `/srv` and `/srv/<service>` must not become a service registry, state namespace, or configuration authority because a provider materializes bytes there.
- Durable configuration, artifacts, evidence, and lineage use their canonical Tavall authorities: physical file mechanics in [`tavall-filesystem`](https://github.com/TavallStudios/tavall-filesystem), durable/coordination stores in [`tavall-database`](https://github.com/TavallStudios/tavall-database).

## Compatibility and migration

Older documents and records may describe service-only Environments, Environment-bound CI, or require a Lane for every Environment. Treat those as historical implementation evidence and migration compatibility only.

- Service-only wording (`Cloud Environments are service-runtime targets only`) is read as the service-default workflow, not as Environment ontology.
- Environment-bound CI remains unauthorized for new source work; the Envless shared-Executor path is the default.
- Stored Environment records that carry a mandatory lane identity are read through `tavall-nlew`'s `INlewMetadataMigrationHandler`, which turns the stored lane into an explicit optional `LANE_COORDINATES_ENVIRONMENT` relationship; the lane reference is preserved, not dropped. Consumers persist the migrated v4 document themselves.

Migrate existing materializations through CONTROL after checking exact source, dirty/unmerged work, active operations, and durable evidence. Preserve active or unknown work; do not bulk delete or reset to make the model appear clean.

## Cross-repository authority

- `tavall-docs` owns this Tavall-wide terminology and ownership rule.
- `tavall-nlew` owns the reusable NLEW API: typed identities, records, policies, relationship types, state transitions, metadata schema versions and migrations, and provider-neutral domain behavior. It does not depend on Tavall Cloud, Tavall Filesystem, or Redis.
- `tavall-cloud` consumes `tavall-nlew` (consumer migration: TavallStudios/tavall-cloud#434, stacked on #424) and owns CONTROL, node-agent execution, NLEW placement/orchestration and Cloud-specific policy, command dispatch and CLI/MCP adapters, service orchestration and default Environment ownership, Executors and provider adapters, networking, desired/observed host topology, mount/export reconciliation, deployment, and runtime activation.
- `tavall-filesystem` owns physical release bytes, manifest/digest verification, ZFS materialization, NFS publication, atomic filesystem operations, and physical locking. It does not own version selection or a durable `CURRENT` pointer.
- `tavall-database` owns Redis (`tavall-database-redis-api` contracts, `tavall-database-redis` provider). Domain keys, schemas, projections, and reconciliation policy stay with the domain owner.
- `tavall-ci` owns provider-neutral CI orchestration, exact-source composition, evidence, and delivery semantics.

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
An OCI image is NOT an environment. Running an image with ambient host defaults is strictly prohibited in production. A container becomes a running service instance only when combined with an explicit, versioned Tavall Environment Definition governing its resources, secrets, and network placement. (An Environment Definition is runtime execution policy; the general-purpose Environment that owns the service is a separate NLEW concept.)

### 2. Prohibited: Treating Environment Definitions as Image Builds
Environment definitions must not compile source code or build OCI images. The OCI image must already exist as an immutable, verified artifact prior to environment instantiation.

### 3. Prohibited: Host-Leaking Paths (`/srv/...`)
Environment definitions must specify portable, logical volume names and mount paths (e.g. `volume: data-storage -> /var/data/tavall`). Host paths (such as `/srv/dev-storage/...` or `/home/...`) must NEVER be embedded into canonical environment definitions or image configurations. Physical host placement is managed dynamically by Tavall Cloud Nodes at instantiation time.

### 4. Prohibited: Conflating Node, Lane, Environment, and Workspace
- A **Node** is compute capacity, not an application environment.
- A **Lane** is optional coordination/source/provenance policy scope, not a runtime target and not an Environment parent.
- An **Environment** is a general-purpose ownership/context boundary (services default here under DEVELOPMENT, STAGING, or PRODUCTION classification), not a Git branch.
- A **Workspace** is a bounded work/materialization scope, never durable service runtime state.
- Relationships between them are explicit typed references, never inferred containment.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/NLEW_AND_SERVICE_OWNERSHIP.md` | 2026-10-09 2:49 PM PDT | PR restoring the general-purpose Environment model and recording tavall-nlew, tavall-filesystem, and tavall-database-redis-api ownership. |
| Notion | `PARTIAL` (explicit temporary drift) | Tavall Cloud — Lanes, Environments & Executors; Tavall NLEW — GENERAL | 2026-10-09 3:10 PM PDT | Notion pages received supersession notes; they are not a verified 1:1 copy of this document. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-03 2:15 AM PDT | GitHub | `CREATED` | this document | — | `d36588f` | General-purpose Environment model. |
| 2026-10-03 3:35 AM PDT | GitHub | `UPDATED` | this document | Same path | `ffd501f` (PR #56) | Service-only Environment policy; Envless CI default. |
| 2026-10-04 8:58 PM PDT | GitHub | `UPDATED` | this document | Same path | `1bd25de` | OCI image vs Environment Definition. |
| 2026-10-09 2:49 PM PDT | GitHub | `UPDATED` | this document | Same path | PR #61 (`e107275`) | General-purpose Environment restored by user direction; Envless CI default, OCI section, and host-path rule retained; repository ownership for tavall-nlew, tavall-filesystem, and tavall-database Redis recorded. |

</details>

