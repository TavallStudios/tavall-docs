# Module README Template

> **Status:** Active template  
> **Use when:** Creating or materially restructuring the README of a real Tavall source/build module  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md), [MODULE_TYPES.md](MODULE_TYPES.md), [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md), and [CI_CD.md](CI_CD.md)

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

<Show enough of the parent repository to orient the reader. The current module must be bold and suffixed with `← This Module`. Every source/build module carries its own `.tavallci/` definition.>

<repo>/
├── module-a/
├── **module-name/ ← This Module**
│   ├── .tavallci/
│   │   └── ci.yaml
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
| `PROGRESSION` | ... | Required module-scoped audited implementation state and history | GitHub ↔ Notion |
| Deployment | ... | Runtime deployment state/history when applicable | GitHub ↔ Notion |
| `PRODUCT` | ... | Commercial behavior when applicable | As designated |
| `USER EXPERIENCE` | ... | User experience when applicable | As designated |
| `ARTICLE` | ... | Reasoning/explanation when applicable | As designated |

Every real source/build module with an independent responsibility boundary must route to its own module-scoped Progression document. Only include other documents that govern or materially affect this module. Do not repeat the repository-wide document catalog.

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
- **CI Definition:** [`.tavallci/ci.yaml`](.tavallci/ci.yaml) — required for every Tavall source/build module; repository-root `.tavallci` may aggregate but does not replace this module-local definition.
- **Current PR Stack:** ...
- **Runtime PR:** ... <only when a non-runtime module's current work is carried by or depends on an owning runtime PR>
- **Progression:** [`<MODULE>_PROGRESSION.md`](...) <required for every real source/build module with an independent responsibility boundary>
- **Development workflow owner/docs:** ... <link the existing repository/module-local development or contribution document when one exists; otherwise delegate to Tavall Docs without restating shared rules>
- Repository/module-specific development notes: ...

Shared Git policy remains delegated to Tavall Docs. Shared CI/CD and versioning policy remain delegated to `CI_CD.md` and `VERSIONING.md`. Do not add a generic `Git Workflow` metadata row.

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## Template Rules

- Module READMEs are contextual routing surfaces, not mini root READMEs.
- The repository structure graph must visibly mark the current module as **bold** and `← This Module`.
- Every Tavall source/build module must carry `.tavallci/ci.yaml`; root repository CI aggregation cannot substitute for the module-local definition.
- Every real source/build module with an independent responsibility boundary has one module-scoped Progression document and the README links it.
- Non-runtime modules point to the runtime module and current runtime PR/PR stack when applicable.
- Deployment history belongs in the Deployment document, not here.
- Do not duplicate shared build/test/Git/architecture/progression/versioning rules.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | 2026-09-27 2:58 PM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 2:58 PM PDT | Quality template; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 2:58 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | Same path | Direct docs-only update to `main`. | Required a dedicated module Progression link while preserving module-local CI/versioning routing. |
| 2026-09-27 2:46 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | Same path | Docs sync branch `docs/ci-versioning-notion-sync-20260927` | Added required module-local `.tavallci/ci.yaml` shape and CI/versioning routing. |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/MODULE_README_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical module README template including current-module tree marking and runtime/PR routing. |

</details>
