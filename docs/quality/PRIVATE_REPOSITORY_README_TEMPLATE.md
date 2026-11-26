# Private Repository README Template

> **Status:** Active template  
> **Use when:** Creating or materially restructuring the root README of a private Tavall repository  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md)

Use only sections that apply. Delete instructional placeholders when instantiating the template.

```markdown
# <Repository Name>

> **<Public Name> (`<technical-name>`) — <Descriptor>**
>
> **What it does:** <One concrete sentence grounded in current accepted ownership and current source.>
>
> **Does not own:** <Explicit boundary callout — only where confusion creates material risk; delete this line when it does not apply.>
>
> **Descriptor status:** `PROPOSED` / `REVIEWED` / `APPROVED` / `STALE`

## Ownership

### Owns
- ...

### Does Not Own
- ...

## Repository Structure

<Repository tree containing real modules and meaningful supporting directories. Link module names to their READMEs when practical.>

## Modules

| Module | Type | Responsibility | Runtime |
| --- | --- | --- | --- |
| [`module-a`](module-a/README.md) | `API` | ... | `module-runtime` |
| [`module-runtime`](module-runtime/README.md) | `RUNTIME` | ... | `Self` |
| [`module-provider`](module-provider/README.md) | `PROVIDER` | ... | `module-runtime` |

## Documentation

| Type | Document | Authority / Purpose | Surface |
| --- | --- | --- | --- |
| `GENERAL` | ... | Product/system overview | Notion |
| Design | ... | Accepted behavior | GitHub ↔ Notion |
| Technical | ... | Architecture / implementation contract | GitHub ↔ Notion |
| Progression / Evidence | ... | Audited implementation state | GitHub ↔ Notion |
| Deployment | ... | Current and historical deployments | GitHub ↔ Notion |
| `PRODUCT` | ... | Commercial/product model when applicable | As designated |
| `USER EXPERIENCE` | ... | User journeys when applicable | As designated |
| `ARTICLE` | ... | Reasoning/explainer when applicable | As designated |

Only include document types that actually exist. Do not add a separate Documentation Index section.

## Deployment

<Only when the repository owns one or more independently deployable systems. Keep this to current orientation and delegate history/details.>

| System | Current Target | Source | State | Deployment Record |
| --- | --- | --- | --- | --- |
| ... | ... | ... | `ACTIVE` | [`<SYSTEM>_DEPLOYMENT.md`](...) |

## Development

- Canonical/current development branch or branch family when materially useful: ...
- Current PR / PR stack: ...
- Repository-specific development owner/docs: ...
- Runtime/module relationship notes that materially affect current work: ...

Shared Git and architecture rules remain delegated to Tavall Docs and repository-local owning documents.

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## Template Rules

- The README opens with the standardized descriptor orientation block from [README_STANDARDS.md](README_STANDARDS.md) "Human-readable descriptors (What is this?)": `Public Name (technical-name) — <Descriptor>`, one "What it does" sentence, an optional "Does not own" callout, and the descriptor status. The "What it does" sentence carries the factual repository/system-boundary statement; do not add a second competing summary above `Ownership`.
- The descriptor is presentation metadata only. It does not rename the repository, modules, packages, or artifact coordinates, and it does not authorize claims about unimplemented or archived capability.
- Private READMEs are operational maps, not project showcase pages.
- The root README owns the repository-wide module map and documentation routing surface.
- Every real module links to its own README.
- Do not duplicate full build/test/Git/architecture/progression/deployment rules already owned elsewhere.
- If the repository has no independently deployable system, omit `Deployment`.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/PRIVATE_REPOSITORY_README_TEMPLATE.md` | 2026-11-26 | `#156` descriptor standardization. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality template; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/PRIVATE_REPOSITORY_README_TEMPLATE.md` | Same path | `#156` descriptor standardization. | Added the standardized top descriptor orientation block and replaced the loose summary sentence with the required "What it does" line. |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/PRIVATE_REPOSITORY_README_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical private root README template. |

</details>
