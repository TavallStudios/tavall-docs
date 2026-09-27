# Module README Template

> **Status:** Active template  
> **Use when:** Creating or materially restructuring the README of a real Tavall source/build module  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md) and [MODULE_TYPES.md](MODULE_TYPES.md)

Use only sections that apply. Delete instructional placeholders when instantiating the template.

```markdown
# <module-name>

<One or two sentences describing exactly what this module owns.>

## Responsibility

### Owns
- ...

### Does Not Own
- ...

## Repository Structure

<Show enough of the parent repository to orient the reader. The current module must be bold and suffixed with `← This Module`.>

<repo>/
├── module-a/
├── **module-name/ ← This Module**
│   ├── src/main/...
│   └── src/test/...
├── module-c/
└── ...

## Relationships

| Module / System | Relationship |
| --- | --- |
| `module-a` | ... |
| `module-runtime` | Runtime owner / consumer / provider relationship |
| External system | ... |

## Documentation

| Type | Document | Purpose | Surface |
| --- | --- | --- | --- |
| `GENERAL` | ... | Readable system/module context when applicable | Notion |
| Design | ... | Accepted behavior | GitHub ↔ Notion |
| Technical | ... | Module/system architecture | GitHub ↔ Notion |
| Progression / Evidence | ... | Current audited implementation state | GitHub ↔ Notion |
| Deployment | ... | Runtime deployment state/history when applicable | GitHub ↔ Notion |
| `PRODUCT` | ... | Commercial behavior when applicable | As designated |
| `USER EXPERIENCE` | ... | User experience when applicable | As designated |
| `ARTICLE` | ... | Reasoning/explanation when applicable | As designated |

Only include documents that govern or materially affect this module. Do not repeat the repository-wide document catalog.

## Deployment

### Deployable module

<Use only when this module has an independent deployable identity.>

| Runtime | Target | Source | State |
| --- | --- | --- | --- |
| `<runtime>` | `<environment/service>` | `<SHA/release>` | `ACTIVE` |

Full deployment record: [`<SYSTEM>_DEPLOYMENT.md`](...)

### Non-runtime / non-deployable module

<Use instead when the module is not independently deployed.>

> This module is not independently deployed.

Runtime owner: [`<runtime-module>`](../<runtime-module>/README.md)  
Current runtime PR / PR stack: ...  
Deployment record: [`<RUNTIME>_DEPLOYMENT.md`](...)

## Development

- **Module Type:** `API` / `RUNTIME` / `APPLICATION` / `LIBRARY` / `PROVIDER` / `ADAPTER` / `INTEGRATION` / `TOOLING` / `TEST_SUITE`
- **Runtime:** `Self` / `<runtime-module>` / `None`
- **Current PR Stack:** ...
- **Runtime PR:** ... <only when a non-runtime module's current work is carried by or depends on an owning runtime PR>
- **Development workflow owner/docs:** ... <link the existing repository/module-local development or contribution document when one exists; otherwise delegate to Tavall Docs without restating shared rules>
- Repository/module-specific development notes: ...

Shared Git policy remains delegated to Tavall Docs. Do not add a generic `Git Workflow` metadata row.

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## Template Rules

- Module READMEs are contextual routing surfaces, not mini root READMEs.
- The repository structure graph must visibly mark the current module as **bold** and `← This Module`.
- Non-runtime modules point to the runtime module and current runtime PR/PR stack when applicable.
- Deployment history belongs in the Deployment document, not here.
- Do not duplicate shared build/test/Git/architecture rules.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | 2026-09-27 11:45 AM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality template; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical module README template including current-module tree marking and runtime/PR routing. |

</details>
