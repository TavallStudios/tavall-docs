# Tavall Workflow Repository and Registry Ownership

> **Status:** Active  
> **Applies to:** Published Tavall Workflows, their source repositories, `TavallStudios/tavall-workflows`, the Tavall web workflow listing, and every future Workflows MCP bridge contract  
> **Purpose:** Fix one stable public publication and discoverability rule for published Tavall Workflows without defining an executable workflow format or claiming runtime/bridge capability.

## Canonical rule

**A published Tavall Workflow may live in its own public `TavallStudios` repository. `TavallStudios/tavall-workflows` remains the canonical workflow registry/index. The Tavall web listing links to the workflow's source repository.**

The three surfaces are separate authorities and must never be merged:

| Surface | Owns | Does not own |
| --- | --- | --- |
| Public workflow source repository, `TavallStudios/<workflow-repository>` | That workflow's source, documentation, examples, releases, and repository-scoped Issues/PRs. | Organization-wide discovery, the registry entry, or another workflow's contracts. |
| `TavallStudios/tavall-workflows` | The canonical registry/index: which workflows are published, their canonical names, and the registry entry that points at the source repository. | The workflow's implementation, a copy of its source, or runner/execution semantics. |
| Tavall web workflow listing | Presentation of registry entries plus the outbound link to each source repository. | A second registry, source authority, or entitlement/execution state. |

## Publication rule

Publishing a Tavall Workflow in its own repository is authorized when all of the following hold:

- the repository is owned by the `TavallStudios` organization and is public;
- its root README follows the public README shape and human-readable descriptor rules in [README_STANDARDS.md](README_STANDARDS.md), and any real source/build modules it contains are classified under [MODULE_TYPES.md](MODULE_TYPES.md);
- the repository is the single source of truth for that workflow's source and releases — the registry and the web listing link to it instead of restating it;
- a registry entry exists in `TavallStudios/tavall-workflows` that names the workflow and points at the source repository;
- delivery follows [GIT_WORKFLOW.md](GIT_WORKFLOW.md); a repository being public is not review, test, release, or publication acceptance.

A workflow repository does not become an organization-level workflow authority. It owns one workflow's implementation, not the set of published workflows.

## Registry rule

`TavallStudios/tavall-workflows` owns the canonical, ordered index of published Tavall Workflows. The registry entry is the stable identity consumers follow:

```text
workflow name -> registry entry -> source repository (TavallStudios/<workflow-repository>)
```

The registry records discovery identity — canonical workflow name, the source repository it points at, and the short purpose statement a listing needs. It must not:

- hold a duplicated working copy of a workflow's source;
- become the implementation home for any individual workflow;
- claim a workflow is executable, installed, entitled, or running;
- invent workflow names, owners, or links that no source repository and Issue record support.

A workflow without a registry entry is not discoverable as a published Tavall Workflow even when its source repository is public. A registry entry without a resolvable public source repository is a broken index entry and is corrected or removed, not re-pointed at the registry itself.

## Web listing rule

The Tavall web workflow listing presents registry entries and links out to the source repository. It is a projection, not a second registry:

- a listing record resolves from a registry entry; it does not create publication identity on its own;
- the primary call to action for a published workflow is the source repository link;
- listing metadata stays consistent with the registry entry and the source repository's README descriptor, and where the two disagree the registry/source owner is corrected first;
- the listing may not present an unpublished, unlisted, or non-resolving workflow as available.

## Boundary: what this rule does not define

This document is a publication and discoverability rule only. It deliberately does not:

- **define an executable workflow format** — packaging, manifests, step/command schema, runtime inputs and outputs, and execution contracts are owned by the current Workflows runtime/bridge contract, not by this document;
- **claim the Workflows MCP bridge is live** — bridge/MCP exposure, tool names, and client wiring remain owned by and blocked on that same Workflows runtime/bridge contract;
- **grant execution, runner, entitlement, or marketplace authority** — runner placement, execution receipts, payment verification, and settlement keep their own owning documents and repositories;
- **assert publication acceptance for any specific workflow** — a public repository, a registry entry, or a listing link proves discovery routing, not tested behavior.

When the Workflows runtime/bridge contract is accepted, executable-format and bridge rules are added to their owning document and linked from here. This rule must not be cited to justify a workflow format or a bridge capability that the current contract has not accepted.

## Related owners

- [README_STANDARDS.md](README_STANDARDS.md) — public repository README and descriptor requirements referenced by the publication rule.
- [MODULE_TYPES.md](MODULE_TYPES.md) — module classification for any real module inside a workflow repository.
- [WEB_ARCHITECTURE.md](WEB_ARCHITECTURE.md) — web surface and route ownership for the listing projection.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) — branch, review, and delivery rules for workflow repositories.

## DOC TODO:

### Document next steps

- [ ] Link the accepted Workflows runtime/bridge contract once executable-format and bridge questions are decided in their owning repository.
- [ ] Record the actual current registry mechanism once `TavallStudios/tavall-workflows` publishes a machine-readable index rather than prose entries.

### System next steps

- No product/runtime implementation work is owned by this document.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/WORKFLOW_REPOSITORY_AND_REGISTRY_OWNERSHIP.md` | 2026-11-26 9:34 AM PST | `#139` public workflow repository and registry ownership rule. |
| Notion | `NOT_APPLICABLE` | — | 2026-11-26 9:34 AM PST | Shared quality policy; no 1:1 Notion twin assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 9:34 AM PST | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/WORKFLOW_REPOSITORY_AND_REGISTRY_OWNERSHIP.md` | — | `#139` (parent work: `TavallStudios/tavall-workflows#20`) | Defined public workflow repository, canonical registry/index, and web listing link ownership, and bounded it away from executable-format and Workflows MCP bridge claims. |

</details>
