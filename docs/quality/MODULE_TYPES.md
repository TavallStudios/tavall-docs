# Tavall Module Types

> **Status:** Active  
> **Applies to:** Tavall repository modules, module READMEs, architecture documentation, development routing, progression ownership, and deployment ownership  
> **Purpose:** Give every real module a small, explicit responsibility classification and make runtime and progression ownership obvious without turning module names into guesswork.

Module type describes the module's **primary responsibility**. Runtime ownership is recorded separately because not every module executes independently.

## Canonical Module Types

| Type | Responsibility |
| --- | --- |
| `RUNTIME` | Independently executable runtime or long-lived process that owns its own lifecycle and may be independently deployed. |
| `SYSTEM` | Consumer-facing fan-in and lifecycle boundary that composes related independently controllable FEATURE modules and/or existing capabilities through the owning runtime's DI/registry. A SYSTEM does not imply a new process. |
| `FEATURE` | Bounded behavior with its own declared enable/disable/load/reload lifecycle under a parent SYSTEM, where independence is justified by meaningful operational or dependency boundaries. A FEATURE does not imply a separate runtime. |
| `APPLICATION` | Application composition/entry module that assembles capabilities into an executable application or bounded application surface; it may or may not be independently deployed. |
| `API` | Caller-facing contracts, request/result/data types, and stable capability boundaries without owning the main runtime implementation. |
| `TOOLING` | Build, development, administration, migration, generation, or operator tooling that is not the product/runtime itself. |
| `TEST_SUITE` | Test-only or validation-focused module that verifies one or more production modules and does not ship as a production runtime. |

## Secondary responsibility roles

MOD-01 and MOD-02 classify APPLICATION, RUNTIME, SYSTEM, FEATURE, API, TOOLING and TEST_SUITE as primary types. LIBRARY, PROVIDER, ADAPTER and INTEGRATION describe secondary responsibilities, recorded independently from primary type, runtime owner, repository and artifact identity.

| Role | Responsibility |
| --- | --- |
| `LIBRARY` | Reusable implementation capability consumed in-process; it does not identify an independently deployed runtime. |
| `PROVIDER` | Pluggable concrete capability implementation selected by the owning SYSTEM/runtime. |
| `ADAPTER` | Translation between APIs, protocols, platforms or representations without a second domain authority. |
| `INTEGRATION` | External product/service/protocol boundary with integration-specific contracts. |

Existing older primary LIBRARY/PROVIDER/ADAPTER/INTEGRATION labels are migration debt. Reclassify a module when its actual ownership is inspected and changed; preserve unrelated modules until that review rather than globally inferring type from a suffix. A reusable stateless domain SYSTEM may have a secondary LIBRARY role without manufacturing FEATURE modules.

## Classification Rules

- Every real source/build module records one **primary** module type in its module README. `SYSTEM` and `FEATURE` are first-class primary types, not descriptive aliases for `LIBRARY` or `PROVIDER`.
- Record one primary type and optional explicitly labeled secondary roles. For example, `FEATURE` primary with `PROVIDER` secondary for `tavall-filesystem-zfs`, or `RUNTIME` primary with `PROVIDER` secondary for an independently executing provider. A role does not imply a separate runtime.
- Module type does not replace ownership documentation. The README still states what the module owns and does not own.
- A directory, fixture, generated source tree, or trivial build helper does not become a module merely because it has a folder.
- Do not invent a new module type for a one-off naming preference. Extend this taxonomy only when a recurring responsibility does not fit an existing type.

## SYSTEM and FEATURE Lifecycle Ownership (2026-10-11)

These classifications implement the accepted MOD-01 and MOD-02 directions while retaining the pre-existing module taxonomy and runtime separation. They are **not** new package namespaces or an excuse to split stateless components into modules.

- A `SYSTEM` composes cohesive capabilities; independently controllable `FEATURE` modules are optional when the system owns stateless domain contracts with one consumer-facing lifecycle/composition surface. It delegates concrete behavior to its FEATURES and existing Tavall interfaces, and acts through Tavall DI and the canonical module registry; it does not own another container, scheduler, backend, or API by implication.
- A `FEATURE` warrants a module only when independent activation/reload, separate provider configuration, failure containment, or consumer/test ownership is real. Stateless policies, NLEW Node/Lane/Environment/Workspace record handlers and simple cohesive classes remain packages unless a real lifecycle pressure is demonstrated.
- Enable, disable, load, unload and reload operate at the **individual FEATURE** boundary where the host supports them. Disabling the parent SYSTEM disables its dependent FEATURES; reloading a FEATURE does not implicitly restart unrelated FEATURES or the owning RUNTIME. Dependency removal or a denied capability fails closed. Live module-state transitions must be owned by canonical `tavall-di` and module lifecycle infrastructure, not per-SYSTEM handmade maps.
- A `RUNTIME` owns executable lifecycle, process boundary and composition, including the API module(s) that the runtime itself exposes. Consumer-facing API modules remain separate typed `API` artifacts but are **owned by that RUNTIME**, not accidentally reassigned to a FEATURE. A reusable library/system-level API with no dedicated runtime remains owned by its actual producer/consumer system. Do not interpret this rule as requiring every SYSTEM or FEATURE to manufacture an API module.
- An API's owner, import direction and current implementation/runtime consumer are explicit in documentation. A FEATURE imports its approved contracts; it must not pull its sibling FEATURES in through hidden classpaths or become another product authority.
- The general `tavall module` operator command is a planned central CLI ownership boundary in `tavall-cd-cli` / Tavall CLI integration; do not add one `/module` command per Minecraft system or claim the universal command is already fully implemented without source and E2E evidence.

### Concrete fan-in example: verified Filesystem modules

```text
Tavall Cloud RUNTIME
    -> tavall-filesystem-api             API (immutable byte/integrity contracts)
    -> tavall-filesystem                 SYSTEM (fan-in, no separate process)
        -> tavall-filesystem-zfs         FEATURE; secondary PROVIDER role
        -> tavall-filesystem-nfs         FEATURE; secondary PROVIDER role

Validation only (outside runtime composition):
    tavall-filesystem-test-suite         TEST_SUITE (source/behavior contract)
```

Filesystem FEATURES must not depend on Redis: `tavall-database` owns Redis and any consumer pointer/reconciliation authority, while Cloud owns placement, durable version selection, and fencing policy.

### Illustrative Minecraft fan-in (example, not a statement of current implementation)

```text
tavall-mc RUNTIME (Velocity/Paper composed into established application artifact)
    -> runtime-owned caller API modules
    -> gameplay anti-cheat SYSTEM
        -> movement heuristic FEATURE
        -> packet/evidence observation FEATURE
        -> resource-pack identity FEATURE
    -> Minecraft platform ADAPTERs

Validation only: relevant TEST_SUITE modules
```

Each FEATURE can be independently controlled at the canonical registry boundary; the anti-cheat SYSTEM can disable its children as a unit. Existing package and architecture canon still decides internal class/package structure. The real anti-cheat source currently has a separate `tavall-mc-anticheat` extraction PR with unverified runtime linkage, so this diagram is an intended **composition shape only**, not a deployed plugin or present class list.

## Boundary test expectations

- At module level: assert allowed compile/runtime dependency direction; FEATURES do not import undeclared siblings, forbidden backend abstractions, or provider SDKs outside permitted wrappers.
- At integration level: start the owning RUNTIME with DI registration; individually disable/reload a FEATURE, prove unrelated FEATURES remain active and stale references fail closed; disable SYSTEM and verify its aggregate capability is unavailable.
- At runtime: prove the final application/JAR composition, restart/rollback behavior, API caller compatibility and module command permission checks through actual host acceptance. No mocked registration-only test establishes lifecycle acceptance.

## Third-Party Tool Wrapper Ownership

Third-party tools are never exposed as an unowned implementation detail of an arbitrary Tavall product module.

- Every third-party binary, CLI, SDK, MCP server, external runtime, or tool-specific protocol used as a reusable Tavall capability **must be owned behind a Tavall module whose canonical module/artifact name begins with `tavall-`**.
- Prefer `tavall-<upstream-tool>` when one upstream tool is the boundary, for example `tavall-open-cv`, `tavall-ffmpeg`, `tavall-playwright`, `tavall-chromium`, `tavall-hyperframes`, or `tavall-remotion`.
- The wrapper records an actual primary type and `INTEGRATION`, `ADAPTER` or `PROVIDER` secondary roles. It owns upstream discovery/version checks, invocation, configuration/environment mapping, protocol/command construction, error translation, lifecycle, and tool-specific observability.
- Product/domain modules depend on Tavall semantic APIs or Tavall wrapper modules. They do **not** scatter direct vendor imports, raw process commands, MCP tool names, vendor HTTP calls, executable paths, or tool-specific environment variables through business code.
- A wrapper may live inside an umbrella repository when that is the coherent ownership boundary; the module/artifact name still follows the `tavall-*` rule.
- Generic modules such as `*-tools`, `common`, or `util` must not become vendor dumping grounds. If a third-party integration is reusable or has meaningful lifecycle/configuration of its own, give it an explicit Tavall wrapper boundary.
- External adapters such as CLI, HTTP, MCP, or UI surfaces project the Tavall-owned semantic capability. They do not become a second business authority merely because the upstream tool speaks that protocol.

Detailed integration-boundary rules and migration guidance: [Third-Party Tool Boundaries](code-architecture/THIRD_PARTY_TOOL_BOUNDARIES.md).

## Runtime Ownership

Module READMEs record runtime ownership independently from module type:

- `Self` — the module owns its own executable runtime.
- `<module-name>` — another module owns the runtime that loads/uses this module.
- `None` — the module has no runtime relationship, such as pure tooling or isolated validation.

A non-runtime module that supports a runtime must point to:

1. the owning runtime module README;
2. the current runtime PR or PR stack when active development depends on it;
3. the owning Deployment document when deployment state is relevant.

`RUNTIME` modules are normally independently deployable. `APPLICATION` modules may be independently deployable when they own an executable deployment boundary. Other primary module types may participate in deployment through their owning runtime but do not receive independent deployment records unless they actually have an independent deployable identity.

## Progression Ownership

Every real source/build module with an independent responsibility boundary has one module-scoped `PROGRESSION` document, regardless of whether it is independently deployable.

The Progression document uses the module's primary type to determine what implementation progress means:

| Type | Progression primarily measures |
| --- | --- |
| `RUNTIME` | Runtime behavior, lifecycle, composition, service integration, operational acceptance, and deployment readiness. |
| `SYSTEM` | Composition/fan-in behavior, independent FEATURE orchestration, aggregate disable/reload semantics, API consumption and runtime E2E integration. |
| `FEATURE` | Feature-specific behavior, independent load/disable/reload, dependency isolation, failure and recovery, and parent SYSTEM/runtime acceptance. |
| `APPLICATION` | End-to-end application capabilities, dependency composition, user/system flows, and runtime acceptance. |
| `API` | Contract implementation, exposed operations, consumer adoption, compatibility, and contract validation. |
| `TOOLING` | Supported workflows, command/tool capabilities, automation correctness, operator/developer usability, and validation. |
| `TEST_SUITE` | Coverage boundaries, enforced scenarios, regression protection, execution state, and evidence quality. |

Secondary roles add their behavioral acceptance to the primary progression lens; one Progression document owns the module boundary.

System-scoped Progression documents aggregate their module/subsystem Progression documents. They do not replace them and must not duplicate every module timeline event.

See [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md) for the canonical module/system Progression structure.

## README Representation

The module's `Development` section records at minimum:

- **Module Type** — one canonical type from this document;
- **Runtime** — `Self`, an owning runtime module, or `None`;
- **SYSTEM/FEATURE relationship** — the parent SYSTEM for a FEATURE, and the independently controllable FEATURES composed by a SYSTEM, when applicable;
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
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | 2026-10-12 | PR #67 reconciles first-class SYSTEM/FEATURE lifecycle and runtime API ownership; runtime acceptance remains consumer-owned. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-29 5:08 PM PDT | Quality/reference document; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | — | Direct docs-only update to `main`. | Added the canonical Tavall module-type and runtime-ownership vocabulary. |
| 2026-09-27 2:58 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | Same path | Direct docs-only update to `main`. | Added required module Progression ownership and type-specific progression lenses. |
| 2026-09-29 5:08 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_TYPES.md` | Same path | PR to `main`. | Canonized Tavall-owned `tavall-*` wrapper modules for reusable third-party tools. |

</details>
