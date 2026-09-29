# Tavall README Standards

> **Status:** Active  
> **Applies to:** Tavall repository root READMEs and real module READMEs  
> **Purpose:** Keep READMEs useful as orientation and routing surfaces without duplicating the documents that actually own behavior, architecture, progression, deployment, or shared engineering policy.

## Core Rule

**READMEs orient and route. Documents define. Progression proves. Deployment records what is running.**

A README must help a human or agent answer where they are, what the repository/module owns, which documents govern the work, and where current development/deployment ownership lives. It must not become a second architecture document, Git workflow manual, deployment ledger, or progression tracker.

## Repository README Types

Repository visibility determines the default root README shape:

- **Private repository README** — operational repository map for getting work done.
- **Public repository README** — external project front door for understanding, evaluating, using, and contributing to the project.

Changing repository visibility requires restructuring the README against the corresponding template. Do not merely redact a private README or bolt marketing copy onto an operational README.

Use:

- [PRIVATE_REPOSITORY_README_TEMPLATE.md](PRIVATE_REPOSITORY_README_TEMPLATE.md)
- [PUBLIC_REPOSITORY_README_TEMPLATE.md](PUBLIC_REPOSITORY_README_TEMPLATE.md)

## Module README Requirement

Every real source/build module with an independent responsibility boundary has its own `README.md`.

A module README is contextual, not comprehensive. It links only the documents and runtime/development relationships that materially govern that module. The repository root README remains the repository-wide map.

Generated source directories, fixtures, trivial build helpers, and other folders without an independent responsibility boundary do not require their own README.

Use [MODULE_README_TEMPLATE.md](MODULE_README_TEMPLATE.md).

## Repository Structure Graphs

Root READMEs show the repository's meaningful module/directory tree.

Module READMEs show enough of the repository tree to orient the reader and must mark the current module using both:

1. **bold formatting** for the current module path/name; and
2. the literal suffix `← This Module`.

Example:

```text
tavall-cloud/
├── tavall-cloud-api/
├── **tavall-cloud-node/ ← This Module**
├── tavall-cloud-kubernetes/
└── tavall-cloud-test-suite/
```

When Markdown rendering inside a fenced tree would prevent bold formatting, render the tree outside a fenced code block or use another readable tree representation that visibly preserves the bold current-module marker.

## Documentation Section

The README `Documentation` section is the navigation surface for documents relevant to the repository or module. Do **not** add a second `Documentation Index` section.

Repository root README:

- provides the repository-level document map;
- includes every maintained repository document through direct links or the narrow owning document/router that enumerates them;
- may group documents by type or owning system when useful;
- does not duplicate document content.

Module README:

- links only documents that govern or materially affect the module;
- links the owning Design/Technical/Progression/Deployment documents where applicable;
- does not repeat the full repository document catalog.

Applicable document types include:

- `GENERAL`;
- `ARTICLE`;
- `PRODUCT`;
- `USER EXPERIENCE`;
- Design Draft / Final;
- Technical Draft / Final;
- Progression / Evidence;
- Deployment.

Only list types/documents that actually exist. Do not create empty documents to make a README table look complete.

## Deployment Summary

A README contains only enough deployment information to orient the reader.

For an independently deployable repository/module, show the current target/source/state and link the owning Deployment document. Historical deployments, rollback/replacement events, deployment evidence, and complete target details belong in the Deployment document.

For a non-runtime/non-deployable module, state that the module is not independently deployed and point to the owning runtime module and Deployment document when applicable.

See [DEPLOYMENT_DOCUMENT_TEMPLATE.md](DEPLOYMENT_DOCUMENT_TEMPLATE.md).

## Development Section

The README `Development` section contains **repository/module-specific current development routing**, not shared Git instructions.

A repository root may include:

- canonical/current development branches when materially useful;
- active PR or PR-stack routing;
- repository-specific development constraints;
- links to repository-local contribution/development documents;
- links to the shared Tavall Git/architecture owners when needed.

A module README records:

- module type from [MODULE_TYPES.md](MODULE_TYPES.md);
- runtime owner (`Self`, another module, or `None`);
- current PR stack when one exists;
- owning runtime PR when a non-runtime module's current work is carried by or depends on that runtime;
- repository/module-specific development notes that are not already owned elsewhere.

Do not add a generic `Git Workflow` metadata row. Shared Git policy belongs to [GIT_WORKFLOW.md](GIT_WORKFLOW.md), and repository-local workflow specialization belongs in its existing owning document.

## Content That Does Not Belong in Private/Module READMEs

Do not duplicate:

- generic build/test commands already owned by repository docs or Tavall CI;
- shared Git workflow;
- shared Java/code architecture rules;
- DI/logging/cache/database conventions;
- full architecture/design contracts;
- full progression/evidence tables;
- full deployment history;
- generic contribution philosophy.

A short repository-specific command or note is allowed when omitting it would make the README fail as an orientation surface, but duplication is the exception, not the default.

## Public README Rule

Public READMEs prioritize external understanding and adoption:

1. what the project is;
2. why it is useful or distinctive;
3. proof/examples/demos where applicable;
4. quick start / usage;
5. curated documentation;
6. building/contributing/license information.

Public READMEs curate documentation rather than exposing the full private operational map. Internal infrastructure, private deployment details, internal progression records, and private system relationships must not leak merely because the repository was made public.

## Authority

A README may summarize an owning document, but the owning document remains authoritative. If a README summary conflicts with its linked Design, Technical, Progression, Deployment, or shared Tavall policy owner, treat the README as stale and correct it.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/README_STANDARDS.md` | 2026-09-27 11:45 AM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality/reference document; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/README_STANDARDS.md` | — | Direct docs-only update to `main`. | Added canonical private/public/module README ownership and delegation rules. |

</details>
