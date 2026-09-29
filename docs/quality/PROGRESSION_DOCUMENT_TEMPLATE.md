# Progression Document Template

> **Status:** Active template  
> **Document type:** `PROGRESSION`  
> **Use when:** Tracking evidence-backed implementation progression for a real Tavall module or an aggregate system  
> **Authority:** [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md), [MODULE_TYPES.md](MODULE_TYPES.md), and [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)

Progression documents answer **what is demonstrably implemented, integrated, validated, blocked, superseded, or still missing**. They are historical evidence records, not design contracts, deployment logs, or task dumps.

Every real source/build module with an independent responsibility boundary has one module-scoped Progression document. Systems that aggregate modules or subordinate systems also have a system-scoped Progression document when aggregate state is meaningful.

## Scope Model

| Scope | Required for | Owns |
| --- | --- | --- |
| `MODULE` | Every real source/build module with an independent responsibility boundary | Detailed implementation history, integration state, validation, blockers, dependencies, and next work for that module. |
| `SYSTEM` | A system composed from modules or subordinate systems when aggregate progression is meaningful | Aggregate state, cross-module milestones, system-level validation, dependencies, blockers, readiness, and remaining system work. |

Module Progression is authoritative for module state. System Progression is authoritative for the aggregate interpretation of its child module/system states.

A system document must not copy every child timeline row. It links child Progression documents and records only transitions that materially change system capability, integration, validation, readiness, ownership, or architecture.

## Timeline Rules

The canonical Progression Timeline is a table ordered **oldest → newest**.

| Date / Time | State | Progression | Evidence | Result / Remaining Work |
| --- | --- | --- | --- | --- |
| `YYYY-MM-DD h:mm AM/PM PST/PDT` | `<STATE>` | <meaningful progression transition> | <PR / SHA / test / runtime evidence> | <what became true and what remained> |

For system-scoped documents, use:

| Date / Time | State | System Progression | Affected Modules / Systems | Evidence | Result / Remaining Work |
| --- | --- | --- | --- | --- | --- |
| `YYYY-MM-DD h:mm AM/PM PST/PDT` | `<STATE>` | <system-significant transition> | <modules/systems> | <evidence> | <result> |

Rows represent meaningful state transitions or completed slices, not every commit. Preserve superseded historical evidence rather than rewriting history to match the latest state.

Useful evidence-backed states include:

- `DESIGNED`
- `IN_PROGRESS`
- `PARTIAL`
- `BLOCKED`
- `VALIDATING`
- `VALIDATED`
- `COMPLETE`
- `MERGED_PRODUCTION`
- `MERGED_STAGING`
- `VALID_UNMERGED_PR`
- `HISTORICAL_EVIDENCE`
- `SUPERSEDED`

Use a narrower explicit state when it communicates the evidence more accurately. Do not invent completion from file counts, test-file counts, branch names, or confident prose.

## Module-Type Progression Lens

The structure remains consistent across modules, but the meaning of progression follows the module's primary type.

| Module Type | Progression primarily measures |
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

Combined module types may combine the applicable lenses, but the document must still identify one owning module boundary.

## Module Template

```markdown
# <Module> Progression

> **Status:** Active progression record  
> **Document Type:** `PROGRESSION`  
> **Progression Scope:** `MODULE`  
> **Module Type:** `<RUNTIME | APPLICATION | API | LIBRARY | PROVIDER | ADAPTER | INTEGRATION | TOOLING | TEST_SUITE>`  
> **Owning System:** `<system>`  
> **Owns:** Audited implementation, integration, validation, and historical progression for `<module>`  
> **Does Not Own:** Product/design rules, aggregate system progression, deployment history, or Git workflow policy  
> **Audited Against:** `<repository>@<commit>`  
> **Last Reconciled:** `YYYY-MM-DD h:mm AM/PM PST/PDT`

## About

`<module>` is a `<module type>` responsible for <responsibility> within `<owning system>`.

<Explain briefly what progression means for this module type and boundary.>

## Module Context

| Field | Value |
| --- | --- |
| Repository | `<owner/repository>` |
| Module | `<module>` |
| Module Type | `<type>` |
| Owning System | `<system>` |
| Runtime Owner | `<Self / runtime-module / None>` |
| Primary Consumers | `<modules/systems>` |
| Current Branch / PR Stack | `<evidence>` |
| Audited Revision | `<SHA>` |

## Current Status

| Field | State |
| --- | --- |
| Overall State | `<DESIGNED / IN_PROGRESS / PARTIAL / VALIDATING / COMPLETE / BLOCKED>` |
| Current Phase | `<phase>` |
| Implementation | `<state>` |
| Integration | `<state>` |
| Validation | `<state>` |
| Runtime / Consumer Acceptance | `<state or N/A>` |
| Deployment Verification | `<state or N/A>` |
| Primary Blocker | `<blocker or None>` |
| Next Slice | `<next concrete work>` |

## Progression Timeline

| Date / Time | State | Progression | Evidence | Result / Remaining Work |
| --- | --- | --- | --- | --- |
| `YYYY-MM-DD h:mm AM/PM PST/PDT` | `<STATE>` | ... | ... | ... |

## Validation State

| Validation | State | Evidence | Remaining Work |
| --- | --- | --- | --- |
| Architecture | ... | ... | ... |
| Unit | ... | ... | ... |
| Integration | ... | ... | ... |
| Consumer / Runtime | ... | ... | ... |
| End-to-End | ... | ... | ... |

Only retain validation rows applicable to the module type.

## Dependencies and Integration

| Dependency / Consumer | Relationship | State | Evidence |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Blockers

| Blocker | Impact | Resolution |
| --- | --- | --- |
| ... | ... | ... |

If none, state `No known progression blockers.`

## Next Slice

<Next concrete implementation or validation slice for this module.>

## Related Documentation

| Type | Document |
| --- | --- |
| Module README | ... |
| Design / Final | ... |
| Technical | ... |
| System Progression | ... |
| Deployment | ... / N/A |

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## System Template

```markdown
# <System> Progression

> **Status:** Active progression record  
> **Document Type:** `PROGRESSION`  
> **Progression Scope:** `SYSTEM`  
> **Owns:** Aggregate implementation, integration, validation, and historical progression for `<system>`  
> **Aggregates:** Module and subordinate-system Progression documents  
> **Does Not Own:** Detailed child implementation history, product/design rules, deployment history, or Git workflow policy  
> **Last Reconciled:** `YYYY-MM-DD h:mm AM/PM PST/PDT`

## About

This document tracks implementation progression for `<system>` as a whole. Detailed child history remains owned by each child Progression document.

## Current Status

| Field | State |
| --- | --- |
| Overall State | `<state>` |
| Current Phase | `<phase>` |
| Module Completion | `<x/y or descriptive state>` |
| System Integration | `<state>` |
| System Validation | `<state>` |
| Production Readiness | `<state / N/A>` |
| Primary Blocker | `<blocker or None>` |
| Next System Slice | `<next slice>` |

## Module / Child Progression

| Module / System | Type | State | Integration | Validation | Blocker / Next Slice | Progression |
| --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | [Progression](...) |

## System Progression Timeline

| Date / Time | State | System Progression | Affected Modules / Systems | Evidence | Result / Remaining Work |
| --- | --- | --- | --- | --- | --- |
| `YYYY-MM-DD h:mm AM/PM PST/PDT` | `<STATE>` | ... | ... | ... | ... |

Do not duplicate ordinary child milestones here. Add a child event only when it changes system-level capability, integration, validation, readiness, ownership, or architecture.

## System Validation

| Validation | State | Modules / Systems | Evidence | Remaining Work |
| --- | --- | --- | --- | --- |
| Architecture | ... | ... | ... | ... |
| Cross-module integration | ... | ... | ... | ... |
| End-to-End | ... | ... | ... | ... |
| Runtime | ... | ... | ... | ... |
| Production | ... | ... | ... | ... |

## System Blockers

| Blocker | Affected Scope | Impact | Resolution |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Next System Slice

<Next system-level objective. Link child Progression documents for detailed work.>

## Related Documentation

| Type | Document |
| --- | --- |
| Design / Final | ... |
| Technical | ... |
| Deployment | ... / N/A |
| Child Progression | ... |

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## Ownership Rules

- Every real source/build module with an independent responsibility boundary has one module-scoped Progression document.
- Aggregate system Progression exists when a system composes modules or subordinate systems and has meaningful cross-boundary state to report.
- Module Progression is authoritative for module state; system Progression is authoritative for aggregate interpretation.
- Parent documents link to child Progression instead of duplicating child history.
- Current Status is the present snapshot. Progression Timeline is the historical path to that snapshot.
- Timeline rows are oldest → newest.
- Progression is evidence-backed. Use source, commits, PRs, tests, runtime evidence, and accepted design/technical documents appropriately.
- Progression does not define new product behavior.
- Progression and Deployment are separate: Progression owns implementation/validation state; Deployment owns what release/runtime is or was actually deployed.
- Every maintained Progression document is a required 1:1 GitHub ↔ Notion document.
- Every maintained Progression document ends with the canonical collapsed `Documentation Update State` footer. That footer records document metadata only and must never be mixed into the software Progression Timeline.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/PROGRESSION_DOCUMENT_TEMPLATE.md` | 2026-09-27 2:58 PM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 2:58 PM PDT | Quality template; instantiated Progression documents carry the required 1:1 sync rule. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 2:58 PM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/PROGRESSION_DOCUMENT_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added module/system Progression scopes, table timelines, module-type lenses, aggregation rules, and required document-state footer. |

</details>
