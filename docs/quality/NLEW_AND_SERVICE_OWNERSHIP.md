# NLEW and Service Ownership

> **Status:** Active
> **Authority:** Binding Tavall-wide terminology and ownership policy for Nodes, Lanes, Environments, Workspaces, Executors, and service placement
> **CI authority:** [CI_CD.md](CI_CD.md)
> **Supersedes:** Any narrower wording that defines Cloud Environments as service-only, or that turns NLEW into a mandatory CI pipeline

## Canonical rule

Tavall NLEW is **Nodes, Lanes, Environments, and Workspaces**, with Executors as an execution capability used across those scopes.

These are distinct Cloud concepts. They are **not** a mandatory containment ladder and they are **not** the Tavall CI execution sequence.

Do not translate NLEW into diagrams such as:

```text
Lane -> Environment -> Workspace -> Executor
```

or:

```text
Lane -> Executor -> Workspace
```

and call that "the CI flow." Tavall CI owns its own much simpler execution/composition model in `CI_CD.md`.

## Environment

An **Environment is general-purpose**. It may own or contain any Cloud workload, resource, repository/runtime context, integration context, service, or other durable/ephemeral state allowed by policy.

A service is **not** what makes an Environment an Environment.

Environment lifecycle, mutability, resource policy, work policy, and service policy remain independent dimensions.

An Environment can exist with zero services.

## Service default

Registered logical services **default to Environment ownership and placement**.

This keeps long-lived service state, configuration, generations, readiness, scaling, traffic state, provider materialization, and service-local resources from becoming owned by whichever Lane, Workspace, Executor, Node path, or command happened to create them.

A different supported owner requires an explicit typed policy. It must not be inferred from the current directory or execution path.

## NLEW responsibilities

### Node

A Node is placement and infrastructure capability. It exposes compute, storage, networking, provider, and execution capabilities.

A node name or host path is not workload identity.

### Lane

A Lane coordinates related work, source composition, policy, provenance, or other scoped activity when a workflow actually needs that coordination.

A Git branch or persistent staging PR is not automatically a Lane.

### Environment

An Environment is a reusable general-purpose Cloud ownership/context boundary.

Services default here, but service ownership is only one use of an Environment.

### Workspace

A Workspace is a bounded Cloud work/materialization scope where a workflow chooses to use one.

A Cloud Workspace is not the same thing as the simple per-repository workspace-folder layout used by Tavall CI. CI may materialize repository workspace folders as execution files without turning each folder into a separate Cloud Workspace domain object.

### Executor

An Executor executes authorized work. Executor identity and lifetime are independent of Environment identity.

An Executor may serve many operations and scopes according to policy.

## CI relationship

NLEW is **available to CI**, not **the shape of CI**.

The canonical CI model is:

```text
Tavall CI
  -> one shared Gradle orchestration/composition system
  -> separate exact-source workspace folder per repository
  -> build/test/evidence
```

Cloud capabilities may be selected around that execution:

```text
CI execution
├── may use a Node
├── may run on an Executor
├── may carry Lane context
├── may use a Cloud Workspace
├── may use an Environment when Environment-owned state is actually required
└── may use an optional supported container boundary
```

None of those choices creates a required ordered NLEW chain.

Ordinary CI also does **not** create an Environment merely because a repository, branch, PR, build, test, or CI invocation exists.

That is a default usage rule, not an Environment type restriction.

## Git and staging

Git integration topology and Cloud execution topology remain separate.

```text
Git:
feature -> sub-staging -> repository staging -> main

Cloud:
select only the NLEW/execution capabilities actually required by the operation
```

A persistent staging PR does not imply a persistent Lane, Environment, Workspace, or Executor.

## Service filesystem rule

A host filesystem path is **never** canonical service identity or ownership.

In particular, `/srv`, `/srv/<service>`, or any other absolute host path must not become Tavall's canonical service registry, service state namespace, service configuration authority, or durable service identity simply because a provider/runtime happens to materialize files there.

Rules:

- Logical service identity comes from Tavall Cloud CONTROL/service registries and typed service/runtime declarations.
- Environment ownership comes from the Cloud model, not from a directory location.
- Durable configuration, artifacts, evidence, and state use their canonical Tavall Storage/Cloud authorities.
- Provider/runtime materialization paths are configured implementation details.
- Changing a provider-local path must not change service identity.
- Documentation and APIs describe logical ownership first and filesystem materialization second.

## Compatibility and migration

Older documents may still contain wording such as:

- `Cloud Environments are service deployment/runtime targets`.
- `service-only Environment`.
- `a service Environment is recorded only at deployment`.
- `environment executor`.
- `Lane -> Executor -> Workspace` as if it were the canonical CI pipeline.

Those statements are historical or workflow-specific where they do not conflict with this document. They must not be interpreted as Tavall-wide ontology.

Repository owners should remove or rewrite conflicting language when those documents are touched. Current implementations must follow this contract now.

## Cross-repository authority

`tavall-docs` owns the Tavall-wide terminology and workflow rules in this document.

`tavall-ci` owns the simple CI orchestration/composition model.

`tavall-cloud` owns concrete NLEW, service placement, runtime, provider, registry, execution, and filesystem-materialization implementation contracts.
