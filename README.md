# Tavall Documentation

The shared engineering, architecture, workflow, and quality reference for TavallStudios repositories.

Tavall Docs keeps shared engineering policy in one public source and routes system-specific contracts to their owning repositories and Notion twins.

## Why Tavall Documentation

- One canonical home for cross-repository engineering and documentation rules.
- Clear ownership boundaries between policy, architecture, design, progression, and deployment records.
- Routing rules that help contributors find the relevant authority without reading every document.
- One global TODO authority projected into every maintained repository without creating competing local backlogs.

## Features

- Repository README and document-type standards
- Git, staging, CI/CD, and code-architecture guidance
- Per-repository system and progression documentation maintained by owning repositories
- Document routing and reconciliation records
- Organization-wide TODO ledger with bot-managed repository projections

## Quick Start

Start with the applicable documentation owner in the list below. The source lives in this repository's docs/ tree; select the relevant quality rule or system owner before changing a repository.

Shared policy is selected through DOCUMENT_ROUTING.yml; do not treat a generic documentation index as the policy source.

Repository work tracking starts in [TODO.md](TODO.md). Repository-local root `TODO.md` files are generated projections, not independent authorities.

## Project Structure

This repository is documentation-only; it has no executable product module.

## Documentation

| Document | Purpose |
| --- | --- |
| [Global TODO](TODO.md) | Canonical organization-wide repository TODO ledger. |
| [Repository TODO Static Projections](docs/quality/TODO_STATIC_PROJECTIONS.md) | Contract for bot-managed root `TODO.md` projections across TavallStudios repositories. |
| [Documentation Standards](docs/quality/DOCUMENTATION_STANDARDS.md) | Applicable repository guidance. |
| [README Standards](docs/quality/README_STANDARDS.md) | Applicable repository guidance. |
| [Git Workflow](docs/quality/GIT_WORKFLOW.md) | Applicable repository guidance. |
| [CI/CD](docs/quality/CI_CD.md) | Applicable repository guidance. |
| [Code Architecture](docs/quality/CODE_ARCHITECTURE.md) | Applicable repository guidance. |
| [Document Routing](docs/quality/DOCUMENT_ROUTING.yml) | Applicable repository guidance. |
| [Progression Overview](docs/progression/TAVALL_PROGRESSION_OVERVIEW.md) | Status overview of progression sources. |
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
| GitHub | PRIMARY | TavallStudios/tavall-docs/README.md | 2026-10-01 | Direct docs-only update to `main`. |
| Notion | NOT_APPLICABLE | — | 2026-10-01 | README files are not synchronized as Notion twins. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 12:29 PM PDT | GitHub | CREATED | TavallStudios/tavall-docs/README.md | — | https://github.com/TavallStudios/tavall-docs/pull/36. | Reworked the public README to describe the current project, module boundary, usage, and documentation. |
| 2026-10-01 | GitHub | UPDATED | TavallStudios/tavall-docs/README.md | Same path | Direct docs-only update to `main`. | Indexed the canonical global TODO ledger and repository static-projection policy. |

</details>
