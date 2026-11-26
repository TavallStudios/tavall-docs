# AGENTS READ HERE - Tavall Architecture & Documentation

**Technology stack inventory:** [TECH_STACK.md](TECH_STACK.md) (implementation and deployment evidence remain with their owning documents).

The shared engineering, architecture, workflow, and quality reference for TavallStudios repositories.

Tavall Docs keeps shared engineering policy in one public source and routes system-specific contracts to their owning repositories and Notion twins.

## Why Tavall Documentation

- One canonical home for cross-repository engineering and documentation rules.
- Clear ownership boundaries between policy, architecture, design, progression, and deployment records.
- Routing rules that help contributors find the relevant authority without reading every document.
- One GitHub Issue per actionable work item, with Tavall GitHub Bot projections and a reversible legacy TODO migration.

## Features

- Repository README and document-type standards
- Git, staging, CI/CD, NLEW, service-ownership, and code-architecture guidance
- Per-repository system and progression documentation maintained by owning repositories
- Document routing and reconciliation records
- GitHub Issue-owned Work Graph transition with bot-managed TODO projections

## Quick Start

Start with the applicable documentation owner in the list below. The source lives in this repository's docs/ tree; select the relevant quality rule or system owner before changing a repository.

Shared policy is selected through DOCUMENT_ROUTING.yml; do not treat a generic documentation index as the policy source.

For Cloud topology and service placement, [NLEW and Service Ownership](docs/quality/NLEW_AND_SERVICE_OWNERSHIP.md) is the current Tavall-wide authority. It explicitly supersedes the service-only Environment wording introduced by PR #53 and any synchronized wording derived from it. Environments remain general-purpose; registered services default to Environment ownership.

Repository work tracking is moving to [Work Graph policy](docs/quality/WORK_TRACKING.md): **GitHub Issues own migrated tasks**; [legacy TODO](TODO.md) remains an authoritative transition source only for items not yet mapped. The existing repository-local TODO v1 projections remain in place until a tested issue-backed generator replaces them.

## Project Structure

This repository is documentation-only; it has no executable product module.

## Documentation

| Document | Purpose |
| --- | --- |
| [Work Graph](docs/quality/WORK_TRACKING.md) | Canonical work ownership, issue intake, verification and migration policy. |
| [Legacy TODO](TODO.md) | Migration source for unmapped tasks and linked historical rows. |
| [Work Graph Wave 1 Audit](docs/progression/TAVALL_WORK_GRAPH_LEGACY_TODO_MIGRATION_20261022.md) | One-time source-to-issue mapping; not a second task ledger. |
| [Repository TODO Static Projections](docs/quality/TODO_STATIC_PROJECTIONS.md) | Contract for bot-managed root `TODO.md` projections across TavallStudios repositories. |
| [Documentation Standards](docs/quality/DOCUMENTATION_STANDARDS.md) | Applicable repository guidance. |
| [Agent Architecture](docs/quality/AGENT_ARCHITECTURE.md) | Tavall Agent Stack V2 entry sequence, Agent groups, orchestration authority, and the durable Executor execution rule. |
| [Tavall Terminology](docs/quality/TAVALL_TERMINOLOGY.md) | Canonical organization vocabulary for Agents, workers, skills, tools, Executors, and the authority hierarchy. |
| [Product Design Standards](docs/quality/PRODUCT_DESIGN_STANDARDS.md) | Tavall-wide product, value, monetization, capacity-access, and UX standards; specialist product visuals remain separately owned. |
| [README Standards](docs/quality/README_STANDARDS.md) | Applicable repository guidance. |
| [NLEW and Service Ownership](docs/quality/NLEW_AND_SERVICE_OWNERSHIP.md) | Binding Node/Lane/Environment/Workspace/Executor terminology, general-purpose Environment model, service-to-Environment default, and non-canonical host-path rule. |
| [Git Workflow](docs/quality/GIT_WORKFLOW.md) | Applicable repository guidance. Git staging is separate from NLEW topology. |
| [CI/CD](docs/quality/CI_CD.md) | Applicable repository guidance. NLEW ontology is owned by the NLEW policy above. |
| [Code Architecture](docs/quality/CODE_ARCHITECTURE.md) | Applicable repository guidance. |
| [Module Separation](docs/quality/code-architecture/MODULE_SEPARATION.md) | Module separation decisions and the product Web frontend repository consolidation policy: repository location vs Gradle module vs artifact/package vs type vs runtime/contract owner vs deployment host, ownership exceptions, exact-source manifests, rollout/reversion/archival criteria. |
| [Discoverable by Design (ARTICLE)](docs/articles/DISCOVERABLE_BY_DESIGN_ENGINEERING.md) | Draft ARTICLE explaining the rationale for typed, AST-discoverable, glanceable, agent-reusable code; founder publication review pending. |
| [CLI Architecture](docs/quality/CLI_ARCHITECTURE.md) | Canonical CLI command ownership, arguments, and execution boundaries. |
| [Workflow Repository and Registry Ownership](docs/quality/WORKFLOW_REPOSITORY_AND_REGISTRY_OWNERSHIP.md) | Public workflow source repository, canonical registry/index, and web listing link ownership; executable format and Workflows MCP bridge remain separately owned. |
| [AI Memory Plane](docs/architecture/TAVALL_AI_MEMORY_PLANE.md) | Memory provider, ingestion, and retrieval contract referenced by the Agent architecture. |
| [Document Routing](docs/quality/DOCUMENT_ROUTING.yml) | Applicable repository guidance. |
| [Progression Overview](docs/progression/TAVALL_PROGRESSION_OVERVIEW.md) | Status overview of progression sources. |
| [Agent Stack V2 Progression](docs/progression/TAVALL_AGENT_STACK_V2_PROGRESSION.md) | Delivery record for the current Tavall Agent Stack. |
| [Work Graph Cross-System Sync Technical Design](docs/technical/TAVALL_WORK_GRAPH_CROSS_SYSTEM_SYNC_TECHNICAL_DESIGN.md) | Technical design for Work Graph synchronization across systems. |
| [Documentation Reconciliation Ledger](docs/progression/TAVALL_DOCUMENTATION_RECONCILIATION_LEDGER.md) | Recent documentation reconciliation record. |

## Requirements / Compatibility

GitHub-based documentation; no software runtime required.

## Building From Source

```bash
Documentation repository; no application build is defined.
```

## Contributing

See the repository's [Git workflow guidance](docs/quality/GIT_WORKFLOW.md).

Repository TODO changes belong in the canonical [global TODO](TODO.md); generated repository projections are synchronized from there.

## License

No tracked license file is present in the current repository tree.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | PRIMARY | TavallStudios/tavall-docs/README.md | 2026-11-26 9:37 AM PST | Indexed the Discoverable by Design draft ARTICLE (`#159`). |
| Notion | NOT_APPLICABLE | — | 2026-11-26 | README files are not synchronized as Notion twins. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 12:29 PM PDT | GitHub | CREATED | TavallStudios/tavall-docs/README.md | — | https://github.com/TavallStudios/tavall-docs/pull/36. | Reworked the public README to describe the current project, module boundary, usage, and documentation. |
| 2026-10-01 | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | Direct docs-only update to `main`. | Indexed the canonical global TODO ledger and repository static-projection policy. |
| 2026-10-03 | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | Direct docs-only correction on `main`. | Indexed the canonical NLEW/service-ownership authority and made its precedence over PR #53's service-only wording explicit. |
| 2026-11-26 9:37 AM PST | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | `#159` draft ARTICLE integration | Indexed the Discoverable by Design engineering ARTICLE as an unpublished draft. |
| 2026-11-26 9:34 AM PST | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | `#139` workflow repository and registry ownership policy | Indexed the new workflow repository/registry ownership policy document. |
| 2026-11-26 | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | `#167` section-index refresh | Indexed the missing Agent architecture, Tavall terminology, CLI architecture, AI Memory Plane, Agent Stack progression, and Work Graph sync technical design documents. |

</details>
