# Tavall Module Types

> **Status:** Active  
> **Applies to:** Tavall repository modules, module READMEs, architecture documentation, development routing, progression ownership, and deployment ownership  
> **Purpose:** Give every real module a small, explicit responsibility classification and make runtime and progression ownership obvious without turning module names into guesswork.

Module type describes the module's **primary responsibility**. Runtime ownership is recorded separately because not every module executes independently.

## Canonical Module Types

| Type | Responsibility |
| --- | --- |
| `RUNTIME` | Independently executable runtime or long-lived process that owns its own lifecycle and may be independently deployed. |
| `APPLICATION` | Application composition/entry module that assembles capabilities into an executable application or bounded application surface; it may or may not be independently deployed. |
| `API` | Caller-facing contracts, request/result/data types, and stable capability boundaries without owning the main runtime implementation. |
| `LIBRARY` | Reusable implementation capability consumed in-process by other modules and not independently deployed. |
| `PROVIDER` | Pluggable concrete implementation of a provider/capability contract, commonly selected by a runtime or application owner. |
| `ADAPTER` | Translation boundary between existing APIs, protocols, platforms, or representations; it does not become a second domain authority. |
| `INTEGRATION` | Boundary that connects Tavall behavior to an external product, service, protocol, or platform and owns the integration-specific contract. |
| `TOOLING` | Build, development, administration, migration, generation, or operator tooling that is not the product/runtime itself. |
| `TEST_SUITE` | Test-only or validation-focused module that verifies one or more production modules and does not ship as a production runtime. |

## Classification Rules

- Every real source/build module records one **primary** module type in its module README.
- Use a combined type such as `RUNTIME / PROVIDER` only when the module genuinely owns both responsibilities. Combined types should be uncommon.
- Module type does not replace ownership documentation. The README still states what the module owns and does not own.
- A directory, fixture, generated source tree, or trivial build helper does not become a module merely because it has a folder.
- Do not invent a new module type for a one-off naming preference. Extend this taxonomy only when a recurring responsibility does not fit an existing type.

## Runtime Ownership

Module READMEs record runtime ownership independently from module type:

- `Self` — the module owns its own executable runtime.
- `<module-name>` — another module owns the runtime that loads/uses this module.
- `None` — the module has no runtime relationship, such as pure tooling or isolated validation.

A non-runtime module that supports a runtime must point to:

1. the owning runtime module README;
2. the current runtime PR or PR stack when active development depends on it;
3. the owning Deployment document when deployment state is relevant.

`RUNTIME` modules are normally independently deployable. `APPLICATION` modules may be independently deployable when they own an executable deployment boundary. Other module types may participate in deployment through their owning runtime but do not receive independent deployment records unless they actually have an independent deployable identity.

## Progression Ownership

Every real source/build module with an independent responsibility boundary has one module-scoped `PROGRESSION` document, regardless of whether it is independently deployable.

The Progression document uses the module's primary type to determine what implementation progress means:

| Type | Progression primarily measures |
| --- | --- |
| `RUNTIME` | Runtime behavior, lifecycle, composition, service integration, operational acceptance, and deployment readiness. |
| `APPLICATION` | End-to-end application capabilities, dependency composition, user/system flows, and runtime acceptance. |
| `API` | Contract implementation, exposed operations, consumer adoption, compatibility, and contract validation. |
| `LIBRARY` | Shared capability implementation, API stability, consumer integration, compatibility, and tests. |
| `PROVIDER` | Provided capability, registration/discovery, lifecycle, consuming modules, and failure behavior. |
| `ADAPTER` | Boundary translation, supported contracts, mapping correctness, compatibility, and failure handling. |
| `INTEGRATION` | Cross-system connectivity, authentication/data exchange, failure/recovery behavior, and end-to-end validation. |
| `TOOLING` | Supported workflows, command/tool capabilities, automation correctness, operator/developer usability, and validation. |
| `TEST_SUITE` | Coverage boundaries, enforced scenarios, regression protection, execution state, and evidence quality. |

Combined module types may combine the applicable progression lenses, but one Progression document still owns the module boundary.

System-scoped Progression documents aggregate their module/subsystem Progression documents. They do not replace them and must not duplicate every module timeline event.

See [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md) for the canonical module/system Progression structure.

## README Representation

The module's `Development` section records at minimum:

- **Module Type** — one canonical type from this document;
- **Runtime** — `Self`, an owning runtime module, or `None`;
- **Current PR Stack** — active branch/PR chain when one exists;
- **Runtime PR** — for a non-runtime module when its current work is carried by or blocked on an owning runtime PR.

The module README `Documentation` section must route to the module's dedicated Progression document in addition to applicable Design, Technical, and Deployment owners.

Shared Git policy remains owned by [GIT_WORKFLOW.md](GIT_WORKFLOW.md). Do not duplicate generic Git workflow rules as module metadata.

See [README_STANDARDS.md](README_STANDARDS.md) and [MODULE_README_TEMPLATE.md](MODULE_README_TEMPLATE.md) for the canonical module README shape.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | 2026-09-27 2:58 PM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 2:58 PM PDT | Quality/reference document; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | — | Direct docs-only update to `main`. | Added the canonical Tavall module-type and runtime-ownership vocabulary. |
| 2026-09-27 2:58 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | Same path | Direct docs-only update to `main`. | Added required module Progression ownership and type-specific progression lenses. |

</details>
