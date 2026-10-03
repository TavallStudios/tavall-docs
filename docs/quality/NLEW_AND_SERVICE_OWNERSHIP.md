# NLEW and Service Ownership

> **Status:** Active
> **Authority:** Binding Tavall-wide terminology and ownership policy for Nodes, Lanes, Environments, Workspaces, Executors, and service placement
> **Supersedes:** Any narrower wording that defines Cloud Environments as service-only, including the service-only Environment policy introduced by PR #53 and synchronization wording derived from it

## Canonical rule

Tavall NLEW is **Nodes, Lanes, Environments, and Workspaces**, with Executors as the execution capability used across those scopes. These are distinct ownership and execution concepts. They are not a mandatory containment ladder and their names must not be used as aliases for Git branches, pull requests, staging tiers, source checkouts, or host filesystem paths.

An **Environment is general-purpose**. It may own or contain any Cloud workload, resource, repository/runtime context, integration context, service, or other durable/ephemeral state allowed by its policy. Environment lifecycle, mutability, resource policy, work policy, and service policy remain independent dimensions.

A service is **not** what makes an Environment an Environment.

## Service default

Registered logical services **default to Environment ownership and placement**.

This default exists so long-lived service runtime state, configuration, generations, provider materialization, readiness, scaling, and service-local resources do not become owned by a Lane, an operation Workspace, or an Executor merely because those scopes participated in building or deploying the service.

```text
source / engineering work
        |
        v
      Lane
        |
        +--> Executor
        |      |
        |      v
        |   Workspace
        |      |
        |      v
        |   artifact
        |
        v
Environment  <--- default durable owner for a deployed logical service
    |
    +--> service
    +--> runtime generations / provider materialization
    +--> other Environment-owned workloads/resources as policy allows
```

The diagram shows a common workflow, not a required parent/child hierarchy. An Environment may exist without a Lane, a Lane may be used without creating an Environment, and a Workspace is not automatically an Environment child in every operation.

## NLEW responsibilities

### Node

A Node is placement and infrastructure capability. It exposes compute, storage, networking, provider, and execution capabilities. A node name or host path never becomes logical workload identity.

### Lane

A Lane coordinates related development/execution work, source composition, policy, and provenance. Git staging branches or staging PRs may use a Lane, but they are not themselves Lanes and must not create one merely by existing.

### Environment

An Environment is a reusable general-purpose Cloud ownership/context boundary. It can hold any appropriate workload or resource. Services default here, but service ownership is only one use of an Environment.

Do not state or implement any of the following:

- `Environment == service runtime`.
- `Environment` is service-only.
- An Environment may only be created during deployment.
- Every Environment requires a service.
- Every source operation requires an Environment.

### Workspace

A Workspace is operation/work scope used for source materialization, edits, builds, tests, generated files, and other bounded work. Workspaces must not silently become durable service owners simply because deployment was initiated from them.

### Executor

An Executor executes authorized work. Executor identity and lifetime are separate from Environment identity. A shared/durable Executor may serve many Lanes, Environments, and Workspaces according to policy.

## CI and source-work default

Ordinary Tavall CI does **not** create an Environment merely because a repository, branch, PR, build, test, or Executor invocation exists.

The normal source-validation path remains:

```text
exact source
    -> Lane when coordination is needed
    -> Executor
    -> operation Workspace
    -> immutable artifact/evidence
```

This is a workflow default, not an Environment type restriction. A build or integration workflow may explicitly use an Environment when Environment ownership is materially required by the test or runtime being exercised.

## Git and staging

Git integration topology and Cloud execution topology remain separate:

```text
Git:
feature -> sub-staging -> repository staging -> main

Cloud:
Node / Lane / Environment / Workspace / Executor relationships chosen by execution need
```

A persistent staging PR does not imply a persistent Lane or Environment. A Lane or Environment exists because CONTROL policy and the workload require it, not because GitHub contains a branch with `staging` in its name.

## Service filesystem rule

A host filesystem path is **never** canonical service identity or ownership.

In particular, `/srv` and `/srv/<service>` must not become Tavall's canonical service registry, service state namespace, service configuration authority, or durable service identity simply because a native/provider runtime happens to materialize bytes there.

Rules:

- Logical service identity comes from Tavall Cloud CONTROL/service registries and typed service/runtime declarations.
- Environment ownership comes from the Cloud model, not from a directory location.
- Durable configuration, artifacts, evidence, and state use their canonical Tavall Storage/Cloud authorities.
- Provider/runtime materialization paths are configured implementation details.
- An absolute host path must not be persisted or exposed as the logical identity of a service.
- Provider-local use of `/srv` is permitted only when explicitly configured as an implementation path; changing that path must not change service identity.
- Documentation and APIs must describe logical ownership first and filesystem materialization second.

## Compatibility and migration

Older documents may still contain wording such as:

- `Cloud Environments are service deployment/runtime targets`.
- `service-only Environment`.
- `a service Environment is recorded only at deployment`.
- `environment executor`.

Read those statements as historical workflow-default wording where they do not conflict with this document. They must not be interpreted as Environment ontology.

Repository owners should remove or rewrite conflicting language when those documents are next touched. Current implementations must follow this contract now rather than waiting for every historical sentence to be edited.

## Cross-repository authority

`tavall-docs` owns the Tavall-wide terminology and workflow rule in this document.

`tavall-cloud` owns the concrete NLEW, service placement, runtime, provider, registry, and filesystem-materialization implementation contract. Cloud documentation may add stricter implementation rules but must preserve the general-purpose Environment model and service-to-Environment default.
