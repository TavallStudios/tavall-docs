# Tavall Quality Documentation

> **Status:** Active index

Use this directory for shared Tavall engineering and documentation policy.

## Documentation System

- [DOCUMENT_ROUTING.yml](DOCUMENT_ROUTING.yml) — small machine-readable exact-signal routing index for selecting only the documentation relevant to the current task.
- [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) — authority, lifecycle, delegation, evidence, archive, and `DOC TODO:` rules.
- [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) — GENERAL, ARTICLE, PRODUCT, USER EXPERIENCE, Design, Technical, and Progression/Evidence responsibilities.
- [GENERAL_DOCUMENT_TEMPLATE.md](GENERAL_DOCUMENT_TEMPLATE.md) — readable product/system overview.
- [ARTICLE_DOCUMENT_TEMPLATE.md](ARTICLE_DOCUMENT_TEMPLATE.md) — reasoning/argument/explainer.
- [PRODUCT_DOCUMENT_TEMPLATE.md](PRODUCT_DOCUMENT_TEMPLATE.md) — commercial/product operating model.
- [USER_EXPERIENCE_DOCUMENT_TEMPLATE.md](USER_EXPERIENCE_DOCUMENT_TEMPLATE.md) — user archetypes and end-to-end experience flows.
- [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md) — compatibility path for older links; GENERAL is the current type.

## Engineering Policy

- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
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
