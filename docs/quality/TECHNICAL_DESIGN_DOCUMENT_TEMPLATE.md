# <SYSTEM OR MODULE NAME> — TECHNICAL DESIGN

> **Document Type:** `TECHNICAL DESIGN`  
> **Scope:** `MODULE` / `SYSTEM`  
> **Lifecycle:** `FINAL_DRAFT` / `FINAL_DRAFT_NHV` / `FINAL`  
> **Status:** Designing / Validating / Accepted / Superseded  
> **Owning Product / Platform:** TODO  
> **Primary Repository:** TODO  
> **Owning Module:** TODO / N/A for system scope  
> **Owning GENERAL:** TODO / N/A  
> **DESIGN Document:** TODO / N/A  
> **Progression Document:** TODO

TECHNICAL DESIGN defines the accepted or proposed **architecture, behavior, ownership, consumer contracts, module/runtime boundaries, class/type shape, state mechanics, integrations, failure semantics, security boundaries, and implementation structure** of one module or aggregate system.

It describes what implementation must become. It does not prove that implementation currently exists. `PROGRESSION` owns implementation and validation evidence; Deployment owns deployed runtime state.

Every maintained TECHNICAL DESIGN document is one logical **1:1 GitHub ↔ Notion** document. Surface-native formatting may differ, but the substantive contract, lifecycle, scope, and status must remain equivalent.

## Decision Summary

State the design in a few dense bullets:

- chosen boundary and owner;
- primary consumers;
- module type;
- runtime owner;
- most important architectural decisions;
- most important non-goals.

## Problem & Objective

What technical problem is being solved now? What concrete outcome must become possible?

## Scope & Ownership

### Owns
- TODO

### Does Not Own
- TODO

### Parent / Child Boundaries
- TODO

## Consumers & Public Contract

| Consumer | Need | Contract / Surface | Lifecycle expectation |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

Design for real consumers before hypothetical reuse.

## Boundary Classification

### Chosen boundary

Select the lowest justified boundary:

```text
existing class/package
  → internal component
  → module
  → independently owned module/runtime
  → repository/system
  → platform/exposed capability
```

### Evidence / pressure

- ownership pressure:
- lifecycle/replacement pressure:
- consumer pressure:
- data/security pressure:
- runtime/deployment pressure:
- compatibility/versioning pressure:
- test/acceptance pressure:
- complexity pressure:

### Rejected alternatives

| Candidate | Why rejected now |
| --- | --- |
| Keep inside parent | TODO |
| Internal/package component | TODO |
| Module | TODO |
| Repository/platform | TODO |

Every separation must name the parent/fan-in consumer and the E2E path proving the separated capability works. API/MCP exposure alone is not proof of platform status.

## Module & Runtime Model

| Module | Canonical Type | Runtime owner | Owns | Does not own | Consumers |
| --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO | TODO |

Module type and runtime ownership are separate dimensions. Use [MODULE_TYPES.md](MODULE_TYPES.md) as the canonical Tavall module taxonomy.

## Architecture Graph

Use a real diagram when relationships benefit from one.

```text
<consumer/runtime>
  └── <module>
      ├── <api/contracts>
      ├── <implementation>
      └── <provider/adapter/integration>
```

## Source / Package Structure

Show the intended repository/module/package tree with meaningful classes and files.

```text
<module>/
├── README.md
├── docs/
├── src/main/...
└── src/test/...
```

Do not invent decorative boilerplate.

## Core Types & Class Roles

| Type | Role | Owns | Does not own | Lifecycle |
| --- | --- | --- | --- | --- |
| TODO | Service / Handler / Orchestrator / Router / Builder / Resolver / Provider / Adapter / contract | TODO | TODO | TODO |

Prefer explicit responsibility vocabulary over catch-all `*Manager` classes.

## Typed Contracts

Define the important request/result/data/key/config/event/provider interfaces and extension points. Include signatures or examples when the shape itself is part of the contract.

Examples must reflect current source or an explicitly labeled target migration. Remembered pseudo-APIs are not evidence.

## Construction & Dependency Access

Document:

- dependency ownership and registration;
- injection/access pattern;
- reload/replacement behavior;
- lifecycle boundaries;
- why no competing container, hidden singleton graph, or parallel authority is introduced.

For Tavall/Java, reuse canonical Tavall DI patterns and current source.

## State, Persistence, Cache, Registry & Events

For every applicable stateful concern identify:

- source of truth;
- in-memory representation;
- persistence boundary;
- cache semantics and invalidation;
- registry/discovery behavior;
- event publication and consumption;
- concurrency, ordering, and idempotency requirements.

Omit irrelevant machinery instead of fabricating complexity.

## Primary Runtime / Consumer Flows

Show important success and failure sequences. Include fan-in through the parent consumer when a capability is separated.

## Failure & Recovery

Document failure modes, retries, idempotency, cancellation, cleanup, restart/reload, rollback/degraded behavior, and operator recovery where relevant.

## Security & Permissions

Document authentication, authorization, trust boundaries, sensitive data, secrets/tokens, validation, and privilege transitions that materially affect the design.

## Compatibility & Migration

Define versioning, backwards compatibility, migrations, rollout/coexistence, deprecation, and removal rules when relevant.

## Observability & Operator Surface

Document minimum logs, metrics, traces, diagnostics, health/readiness, commands/admin endpoints, and debug evidence needed to operate the system.

## Concrete Implementation Examples

Use compile-shape or otherwise idiomatic examples for the active stack.

For Tavall/Java, prefer current Tavall Java tools and real consumer patterns such as Tavall DI, cache, event, registry, scheduler, database, concurrency, logging, reflection, and utility modules. Extend existing authority when it fits rather than building a competing framework inside a product module.

For non-Tavall systems, preserve the architecture principles but use the actual language/framework idiomatically.

## Validation & Acceptance

| Layer | What must be proven | Evidence |
| --- | --- | --- |
| Unit | TODO | TODO |
| Integration | TODO | TODO |
| Architecture | TODO | TODO |
| E2E / runtime | TODO | TODO |

Validation requirements belong here. Actual evidence/results belong in PROGRESSION.

## Implementation / PR Graph

Split implementation around independently verifiable capability boundaries.

```text
PR 1: contracts + boundary
  ↓
PR 2: implementation
  ↓
PR 3: fan-in consumer + integration
  ↓
PR 4: E2E / acceptance / docs promotion
```

Parallelize only genuinely independent work.

## Future Separation Triggers

Record observable evidence that would justify the next boundary promotion. Do not pre-create modules/platforms solely because they might someday be useful.

## Alternatives Rejected

Record serious alternatives and why they lost.

## Open Questions

Keep unresolved choices explicit. Resolve or convert them into accepted rules before `FINAL` promotion.

## Documentation Relationships

### Parent / Aggregate TECHNICAL DESIGN
- TODO / N/A

### Child TECHNICAL DESIGN Documents
- TODO / N/A

### GENERAL
- TODO / N/A

### DESIGN
- TODO / N/A

### PROGRESSION
- TODO

### Deployment
- TODO / N/A

### Implementation
- TODO

## Final Technical Rules

End with the small set of architecture rules a developer/reviewer must preserve.

## DOC TODO:

### Document next steps
- [ ] Keep GitHub and Notion copies synchronized 1:1.
- [ ] Keep scope, lifecycle, module type, and runtime ownership explicit.
- [ ] Link parent/child technical designs rather than duplicating full contracts.
- [ ] Remove stale target-migration language after implementation or supersession.

### System next steps
- [ ] Record architecture/design authority here. Implementation state belongs in PROGRESSION.

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `1:1` | TODO | TODO | TODO |
| Notion | `1:1` | TODO | TODO | TODO |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| TODO | GitHub | `CREATED` | TODO | — | TODO | Created from the canonical Tavall TECHNICAL DESIGN template. |
| TODO | Notion | `CREATED` | TODO | — | TODO | Created as the 1:1 Notion twin. |

</details>
