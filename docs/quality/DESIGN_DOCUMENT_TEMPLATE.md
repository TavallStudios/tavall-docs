# <SYSTEM OR MODULE NAME> — DESIGN

> **Document Type:** `DESIGN`  
> **Scope:** `MODULE` / `SYSTEM`  
> **Lifecycle:** `FINAL_DRAFT` / `FINAL_DRAFT_NHV` / `FINAL`  
> **Status:** Designing / Validating / Accepted / Superseded  
> **Owning Product / Platform:** TODO  
> **Primary Repository:** TODO  
> **Owning Module:** TODO / N/A for system scope  
> **Owning GENERAL:** TODO / N/A when no GENERAL exists  
> **Technical Document:** TODO / combined with this document when intentionally shared  
> **Progression Document:** TODO

DESIGN defines the accepted or proposed **behavior, ownership, composition, boundaries, and developer-facing shape** of one module or aggregate system. It answers what the thing is supposed to do and how its pieces are supposed to fit together without turning implementation evidence into design authority.

Every real source/build module with an independent responsibility boundary has one module-scoped DESIGN document. Systems composed from modules or subordinate systems have a system-scoped DESIGN document when aggregate behavior, composition, or cross-module ownership is meaningful.

Every maintained DESIGN document is one logical **1:1 GitHub ↔ Notion** document. Surface-native formatting may differ, but the substantive contract, lifecycle, scope, and status must remain equivalent.

## About

Describe the module/system in a few high-information paragraphs.

- What capability does it own?
- Why does this boundary exist?
- Who or what consumes it?
- What is explicitly outside its scope?

## Scope & Ownership

### Owns

- TODO

### Does Not Own

- TODO

### Parent / Child Boundaries

For `MODULE` scope, identify the owning parent system and sibling boundaries that materially constrain this module.

For `SYSTEM` scope, identify the child modules/subsystems that compose the system and what remains authoritative in each child.

## Design Contract

Define the accepted behavior and invariants that implementation must preserve.

Cover only the dimensions that apply, such as:

- lifecycle and state transitions;
- public/consumer-facing capabilities;
- composition and orchestration;
- concurrency/lifecycle expectations;
- persistence/cache/state ownership at a design level;
- failure, cancellation, recovery, reload, and shutdown behavior;
- extension points and compatibility rules;
- security/access boundaries;
- user/operator/developer-visible behavior.

Do not copy implementation history here. PROGRESSION owns evidence of what currently exists.

## Public / Consumer Shape

Document the intended consumer surface at the level needed to prevent architectural drift.

Examples may include:

- primary interfaces/classes;
- builder or fluent consumer shape;
- route/command/event/API families;
- generated symbols or code-generation contracts;
- module entrypoints and adapters;
- optional versus required consumer classes.

Use code examples when the API shape itself is part of the accepted design. Examples must reflect the owning implementation or an explicitly identified target migration, never remembered pseudo-APIs presented as current fact.

## Composition

### MODULE scope

Explain how this module participates in its parent system, including dependencies and the boundaries it must not absorb.

### SYSTEM scope

Explain how child modules/subsystems compose into the aggregate system. Link child DESIGN documents rather than duplicating their full contracts.

## Data & State Boundaries

When applicable, identify authoritative state ownership, caches, files, databases, registries, generated assets, and runtime-only state at the level necessary to preserve design boundaries.

Detailed schemas and migration mechanics belong in Technical or delegated schema documents unless they are themselves part of the behavioral contract.

## Runtime / Interaction Flows

Document the important success and failure flows readers need to understand the design. Include only flows that materially define the contract.

## Integrations

List adjacent Tavall systems, external providers, adapters, and transport boundaries that materially affect this design.

For each integration, state which side owns domain authority and which side merely adapts or projects it.

## Validation Requirements

Define what must be proven before this design can be considered implemented or accepted.

Examples:

- architecture tests;
- unit/integration tests;
- E2E/browser/game/runtime validation;
- consumer compilation/adoption;
- failure/recovery tests;
- manual visual or human acceptance when automation cannot observe the requirement.

Validation requirements are design acceptance criteria. Actual results and exact evidence belong in PROGRESSION.

## Design Decisions & Open Questions

Use this section only while the document is in a draft lifecycle.

### Accepted Decisions

- TODO

### Open Questions

- TODO

Remove resolved questions or convert them into explicit accepted rules before promotion to `FINAL`.

## Documentation

### Parent / Aggregate DESIGN

- TODO / N/A

### Child DESIGN Documents

- TODO / N/A

### GENERAL

- TODO / N/A

### Technical

- TODO

### PROGRESSION

- TODO

### Deployment

- TODO / N/A

### Implementation

- TODO repository/module/source locations

## Final Rules Summary

End with the small set of rules a developer or reviewer must remember when changing this module/system.

## DOC TODO:

### Document next steps

- [ ] Keep GitHub and Notion copies synchronized 1:1.
- [ ] Keep lifecycle and scope explicit.
- [ ] Link parent/child DESIGN documents without duplicating their contracts.
- [ ] Remove stale target-design language after implementation or supersession.

### System next steps

- [ ] Record only design work here. Implementation state belongs in PROGRESSION.

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
| TODO | GitHub | `CREATED` | TODO | — | TODO | Created from the canonical Tavall DESIGN template. |
| TODO | Notion | `CREATED` | TODO | — | TODO | Created as the 1:1 Notion twin. |

</details>
