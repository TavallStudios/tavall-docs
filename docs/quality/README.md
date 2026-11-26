# Tavall Quality Documentation

> **Status:** Active index

Use this directory for shared Tavall engineering and documentation policy.

## Documentation System

- [DOCUMENT_ROUTING.yml](DOCUMENT_ROUTING.yml) — small machine-readable exact-signal routing index for selecting only the documentation relevant to the current task.
- [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) — authority, lifecycle, delegation, evidence, archive, and `DOC TODO:` rules.
- [PRODUCT_DESIGN_STANDARDS.md](PRODUCT_DESIGN_STANDARDS.md) — free-first core product, adjacent paid value, capacity-first admissions, trust, shared UX, and specialist design-system routing.
- [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) — GENERAL, ARTICLE, PRODUCT, USER EXPERIENCE, Design, Technical, PROGRESSION, and Deployment responsibilities.
- [WORK_TRACKING.md](WORK_TRACKING.md) — canonical GitHub Issue types, title prefixes, TODO-to-Task promotion, issue ownership and Work Graph migration.
- [TODO_STATIC_PROJECTIONS.md](TODO_STATIC_PROJECTIONS.md) — canonical contract for the global TODO ledger and bot-managed root `TODO.md` projections in every maintained TavallStudios repository.
- [README_STANDARDS.md](README_STANDARDS.md) — canonical private/public repository README and module README routing/ownership rules.
- [PRIVATE_REPOSITORY_README_TEMPLATE.md](PRIVATE_REPOSITORY_README_TEMPLATE.md) — operational private repository root README template.
- [PUBLIC_REPOSITORY_README_TEMPLATE.md](PUBLIC_REPOSITORY_README_TEMPLATE.md) — external-facing public repository root README template.
- [MODULE_README_TEMPLATE.md](MODULE_README_TEMPLATE.md) — per-module orientation, runtime, module-local `.tavallci`, documentation, deployment-summary, progression, and development-routing template.
- [TAVALL_DESCRIPTOR_INVENTORY.md](TAVALL_DESCRIPTOR_INVENTORY.md) — derived projection of current repository/module “What is this?” descriptors, coverage counts, and open owner-review conflicts.
- [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md) — canonical module/system Progression structure, table timeline rules, module-type lenses, and aggregation ownership.
- [DEPLOYMENT_DOCUMENT_TEMPLATE.md](DEPLOYMENT_DOCUMENT_TEMPLATE.md) — current/historical deployment record template for independently deployable systems.
- [DESIGN_DOCUMENT_TEMPLATE.md](DESIGN_DOCUMENT_TEMPLATE.md) — Design document template for module/system scope.
- [GENERAL_DOCUMENT_TEMPLATE.md](GENERAL_DOCUMENT_TEMPLATE.md) — readable product/system overview.
- [ARTICLE_DOCUMENT_TEMPLATE.md](ARTICLE_DOCUMENT_TEMPLATE.md) — reasoning/argument/explainer.
- [PRODUCT_DOCUMENT_TEMPLATE.md](PRODUCT_DOCUMENT_TEMPLATE.md) — commercial/product operating model.
- [USER_EXPERIENCE_DOCUMENT_TEMPLATE.md](USER_EXPERIENCE_DOCUMENT_TEMPLATE.md) — user archetypes and end-to-end experience flows.
- [MARKETING_DOCUMENT_TEMPLATE.md](MARKETING_DOCUMENT_TEMPLATE.md) — marketing document template.
- [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md) — compatibility path for older links; GENERAL is the current type.

## Engineering Policy

- [TAVALL_TERMINOLOGY.md](TAVALL_TERMINOLOGY.md) — canonical Tavall vocabulary for Agents, workers, skills, tools, Executors, and the authority hierarchy.
- [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md) — binding Node/Lane/Environment/Workspace/Executor terminology, durable shared Executor default, Linux-user permission roles, and service-to-Environment default.
- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
- [CI_CD.md](CI_CD.md) — organization-wide CI/CD, module-local `.tavallci`, exact-source, evidence, artifact, staging, and promotion policy.
- [VERSIONING.md](VERSIONING.md) — source/build/resolution/artifact/release identity, snapshot numbering, and artifact-channel policy.
- [MODULE_TYPES.md](MODULE_TYPES.md) — canonical `RUNTIME`, `APPLICATION`, `API`, `LIBRARY`, `PROVIDER`, `ADAPTER`, `INTEGRATION`, `TOOLING`, and `TEST_SUITE` module classifications plus runtime and progression-ownership rules.
- [WEB_ARCHITECTURE.md](WEB_ARCHITECTURE.md) — canonical Tavall web architecture, beginning with endpoint and routing ownership.
- [CLI_ARCHITECTURE.md](CLI_ARCHITECTURE.md) — canonical Tavall CLI architecture, command ownership, and execution boundaries.
- [DATABASE_AND_PERSISTENCE_SEPARATION_DESIGN.md](DATABASE_AND_PERSISTENCE_SEPARATION_DESIGN.md) — Database and persistence environment separation design.
- [DIAGRAM_STANDARDS.md](DIAGRAM_STANDARDS.md) — Tavall technical diagram, SVG, and Notion visual-presentation standards.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- [STAGING.md](STAGING.md) — persistent repository/release staging boundary for this documentation repository.
- [TAVALL_SERVICE_RELEASE_ON_A_DIME_RUNBOOK.md](TAVALL_SERVICE_RELEASE_ON_A_DIME_RUNBOOK.md) — typed service release promotion, immutable artifact propagation, verification, and rollback runbook.
- [`code-architecture/`](code-architecture/) — delegated architecture chapters; [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) Required Topic Routing indexes which chapter owns which topic.

## Agent and AI Policy

- [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) — Tavall Agent Stack V2 architecture, mandatory work entry sequence, Agent groups, skill-candidate review, orchestration authority, and the durable Executor execution rule.
- [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) — canonical first-party Agent skill structure for section-adapter and procedural skills.

## Selective resolution

Shared Tavall policy consumers should resolve this repository's current `main` branch and select only the files required by the task. `DOCUMENT_ROUTING.yml` is the lightweight routing contract for exact prompt/reasoning signals; it is not a replacement for the selected documents themselves.

Do not recursively preload this directory as a generic engineering preflight. Detailed architecture chapters may be selected directly without automatically loading `CODE_ARCHITECTURE.md`, and templates should be loaded only when the corresponding document type is being created or materially restructured.

The organization-wide work ledger lives at repository root [`TODO.md`](../../TODO.md). Every other maintained TavallStudios repository receives only its own generated slice according to [TODO_STATIC_PROJECTIONS.md](TODO_STATIC_PROJECTIONS.md).

## Authority

Shared quality documents define Tavall-wide defaults. Repository-local documentation may specialize them where the owning runtime/product requires stricter rules, but may not silently weaken shared policy.

The historical `DOC_DESIGN_RULES.md` lineage (Project Novus/Tavall MC `b5e690859` / `dff1d0818`) has been fully reconciled and superseded by [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) and [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md), which own the binding Design/Technical subtype, delegation, and lifecycle rules organization-wide.

Root repository `TODO.md` projections do not supersede `DOC TODO:` blocks. `DOC TODO:` remains per-document maintenance handoff; repository TODO projections remain global-work views managed from `tavall-docs/TODO.md`.

## Production Examples

Binding architecture documentation should link to canonical production implementations once those examples exist and have been validated as representative of the documented pattern. Production examples are evidence and reference implementations; they do not replace the owning documentation contract.

Do not link temporary branches, experiments, migration code, or known-debt implementations as canonical examples merely because they happen to contain similar code.

## DOC TODO:

### Document next steps

- [ ] Keep this index synchronized as shared quality documents are added, renamed, or superseded.
- [ ] Keep `DOCUMENT_ROUTING.yml` synchronized when an owning document or exact routing signal changes.
- [x] Re-index every current `docs/quality` document, the delegated architecture chapters, and the Agent/AI policy surface (completed 2026-11-26: `#167`).
- [ ] Keep the TODO projection policy indexed here as bot behavior evolves.
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
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/README.md` | 2026-11-26 | `#156` descriptor standardization. |
| Notion | `NOT_APPLICABLE` | — | 2026-11-26 | GitHub quality index; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README.md` | Same path | `#156` descriptor standardization. | Indexed `TAVALL_DESCRIPTOR_INVENTORY.md` and the standardized README descriptor format routed by `DOCUMENT_ROUTING.yml`. |
| 2026-09-27 3:04 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README.md` | Same path | Direct docs-only update to `main`. | Indexed canonical PROGRESSION rules/template and added the required document-state footer. |
| 2026-10-01 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README.md` | Same path | Direct docs-only update to `main`. | Indexed the canonical repository TODO static-projection contract and clarified its relationship to `DOC TODO:`. |
| 2026-11-26 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README.md` | Same path | `#167` section-index refresh | Indexed every `docs/quality` document that was missing (terminology, NLEW, Agent architecture, CLI architecture, skills, design template, diagram standards, staging, release runbook, design record) and added the Agent and AI Policy section. |

</details>
