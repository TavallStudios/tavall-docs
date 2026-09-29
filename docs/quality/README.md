# Tavall Quality Documentation

> **Status:** Active index

Use this directory for shared Tavall engineering and documentation policy.

## Documentation System

- [DOCUMENT_ROUTING.yml](DOCUMENT_ROUTING.yml) — small machine-readable exact-signal routing index for selecting only the documentation relevant to the current task.
- [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) — authority, lifecycle, delegation, evidence, archive, and `DOC TODO:` rules.
- [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) — GENERAL, ARTICLE, PRODUCT, USER EXPERIENCE, Design, Technical, PROGRESSION, and Deployment responsibilities.
- [README_STANDARDS.md](README_STANDARDS.md) — canonical private/public repository README and module README routing/ownership rules.
- [PRIVATE_REPOSITORY_README_TEMPLATE.md](PRIVATE_REPOSITORY_README_TEMPLATE.md) — operational private repository root README template.
- [PUBLIC_REPOSITORY_README_TEMPLATE.md](PUBLIC_REPOSITORY_README_TEMPLATE.md) — external-facing public repository root README template.
- [MODULE_README_TEMPLATE.md](MODULE_README_TEMPLATE.md) — per-module orientation, runtime, module-local `.tavallci`, documentation, deployment-summary, progression, and development-routing template.
- [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md) — canonical module/system Progression structure, table timeline rules, module-type lenses, and aggregation ownership.
- [DEPLOYMENT_DOCUMENT_TEMPLATE.md](DEPLOYMENT_DOCUMENT_TEMPLATE.md) — current/historical deployment record template for independently deployable systems.
- [GENERAL_DOCUMENT_TEMPLATE.md](GENERAL_DOCUMENT_TEMPLATE.md) — readable product/system overview.
- [ARTICLE_DOCUMENT_TEMPLATE.md](ARTICLE_DOCUMENT_TEMPLATE.md) — reasoning/argument/explainer.
- [PRODUCT_DOCUMENT_TEMPLATE.md](PRODUCT_DOCUMENT_TEMPLATE.md) — commercial/product operating model.
- [USER_EXPERIENCE_DOCUMENT_TEMPLATE.md](USER_EXPERIENCE_DOCUMENT_TEMPLATE.md) — user archetypes and end-to-end experience flows.
- [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md) — compatibility path for older links; GENERAL is the current type.

## Engineering Policy

- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
- [CI_CD.md](CI_CD.md) — organization-wide CI/CD, module-local `.tavallci`, exact-source, evidence, artifact, staging, and promotion policy.
- [VERSIONING.md](VERSIONING.md) — source/build/resolution/artifact/release identity, snapshot numbering, and artifact-channel policy.
- [MODULE_TYPES.md](MODULE_TYPES.md) — canonical `RUNTIME`, `APPLICATION`, `API`, `LIBRARY`, `PROVIDER`, `ADAPTER`, `INTEGRATION`, `TOOLING`, and `TEST_SUITE` module classifications plus runtime and progression-ownership rules.
- [WEB_ARCHITECTURE.md](WEB_ARCHITECTURE.md) — canonical Tavall web architecture, beginning with endpoint and routing ownership.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- [`code-architecture/`](code-architecture/)

## Selective resolution

Shared Tavall policy consumers should resolve this repository's current `main` branch and select only the files required by the task. `DOCUMENT_ROUTING.yml` is the lightweight routing contract for exact prompt/reasoning signals; it is not a replacement for the selected documents themselves.

Do not recursively preload this directory as a generic engineering preflight. Detailed architecture chapters may be selected directly without automatically loading `CODE_ARCHITECTURE.md`, and templates should be loaded only when the corresponding document type is being created or materially restructured.

## Authority

Shared quality documents define Tavall-wide defaults. Repository-local documentation may specialize them where the owning runtime/product requires stricter rules, but may not silently weaken shared policy.

The historical `DOC_DESIGN_RULES.md` lineage (Project Novus/Tavall MC `b5e690859` / `dff1d0818`) has been fully reconciled and superseded by [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) and [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md), which own the binding Design/Technical subtype, delegation, and lifecycle rules organization-wide.

## Production Examples

Binding architecture documentation should link to canonical production implementations once those examples exist and have been validated as representative of the documented pattern. Production examples are evidence and reference implementations; they do not replace the owning documentation contract.

Do not link temporary branches, experiments, migration code, or known-debt implementations as canonical examples merely because they happen to contain similar code.

## DOC TODO:

### Document next steps

- [ ] Keep this index synchronized as shared quality documents are added, renamed, or superseded.
- [ ] Keep `DOCUMENT_ROUTING.yml` synchronized when an owning document or exact routing signal changes.
- [ ] Add canonical production-example links to `WEB_ARCHITECTURE.md`, `CLASSES.md`, and other applicable architecture chapters as validated production implementations of each pattern are created.
- [x] Link the canonical `DOC_DESIGN_RULES.md` location once reconciled (completed: superseded by `DOCUMENTATION_STANDARDS.md` and `DOCUMENT_TYPES.md`).

### System next steps

- No product/runtime implementation work is owned by this index.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/README.md` | 2026-09-27 3:04 PM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 3:04 PM PDT | GitHub quality index; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 3:04 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README.md` | Same path | Direct docs-only update to `main`. | Indexed canonical PROGRESSION rules/template and added the required document-state footer. |

</details>
