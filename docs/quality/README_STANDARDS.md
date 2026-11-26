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

## Human-readable descriptors (What is this?)

Every repository root README and every real module README opens with a standardized orientation block that answers **"What is this?"** before any other section. A technical identifier such as `tavall-nlew` or `tavall-di` is a necessary but insufficient answer: it names the thing without telling a new developer, user, or agent what kind of thing it is.

The orientation block is one line plus one sentence:

```text
Public Name (technical-name) — <Descriptor>

<What it does: one concrete sentence.>

Does not own: <explicit boundary callout, only where confusion creates material risk>
```

Worked example:

```text
TIDI (tavall-di) — Type-Safe Dependency Wiring

Discovers, owns, and hands out application dependencies through typed access and explicit delegation.
```

### Fields

| Field | Required | Definition |
| --- | --- | --- |
| Technical name | Yes | The unchanged canonical repository slug, Gradle project, module directory, or artifact identifier (for example `tavall-di`). Never renamed, abbreviated, or replaced by the descriptor. |
| Public name | Yes | The established product or project name when one exists and differs from the slug (for example `TIDI` for `tavall-di`, `Tavall Cloud` for `tavall-cloud`). When no distinct public name exists, repeat the technical name rather than inventing a brand. |
| Descriptor | Yes | 2–6 plain-language words answering "What kind of thing is this?". |
| What it does | Yes | One concrete sentence grounded in current accepted ownership and current source. |
| Does not own | Optional | An explicit boundary callout placed only where confusing ownership creates material risk. Omit it when the boundary is not materially confusable. |
| Status | Yes | `PROPOSED`, `REVIEWED`, `APPROVED`, or `STALE`. |

### Descriptor rules

- Answer the category question first. "Type-Safe Dependency Wiring" beats "Dependency Injection Platform Solution".
- Prefer a mental model over a feature list. A descriptor is not a summary of every capability.
- Do not repeat generic buzzwords. A descriptor that is mostly `Platform`, `Framework`, `Intelligence`, `Solution`, `System`, or a restatement of the slug conveys nothing; rewrite it.
- Do not invent capabilities, availability, or maturity. A component whose enforcement lives elsewhere does not own enforcement in its descriptor.
- No slogans, superlatives, or marketing adjectives (`revolutionary`, `next-generation`, `world-class`).
- Keep the public name, technical identifier, and descriptor visibly distinct. Never present a technical slug as the public brand when an established public name exists, and never let a descriptor displace the technical name.
- Ground the descriptor and the "What it does" sentence in the owning README, accepted Design/Technical document, or current source. If the evidence is missing, publish the entry as `PROPOSED` or `STALE`, not as an approved claim.
- Respect exposure boundaries. A private repository's descriptor must not leak private topology, deployment targets, or internal system relationships into a public surface.
- Keep the same descriptor consistent across the repository root README, repository description/catalog surfaces, and any future discovery or search surface. Where two surfaces disagree, the descriptor is stale on one of them.

### Descriptor status

| Status | Meaning |
| --- | --- |
| `PROPOSED` | A candidate descriptor that has not been validated against current ownership and source. Default for any new or unresearched entry. |
| `REVIEWED` | Checked against the owning README, accepted design, and current source by someone other than the person who drafted it; no ownership conflict recorded. |
| `APPROVED` | Accepted for publication by the owning repository/module reviewer. Only `APPROVED` descriptors may be treated as the project's public-facing positioning. |
| `STALE` | Previously published but now contradicted by current ownership, source, or an accepted document. A `STALE` descriptor must not be presented as current and needs a new candidate before it can be re-published. |

Status describes the descriptor text only. It never describes the repository, module, or product state; those remain owned by Progression, Deployment, and the owning Design/Technical documents.

### Non-goals

A descriptor is **presentation metadata**, and this section grants no authority beyond that:

- **Not an execution contract.** A descriptor creates no runtime behavior, permission, boundary, or acceptance requirement. It cannot be cited to authorize, forbid, or scope code changes.
- **Not a rebranding.** Repository slugs, artifact coordinates (`org.tavall:*`), Java package names, Gradle project paths, module types, and architecture boundaries are unchanged. A descriptor never justifies renaming a repository, module, package, or directory, and never introduces a new abstraction layer.
- **Not a second architecture document.** A README stays a routing surface. One descriptor line and one sentence do not license capability tables, ownership contracts, or design detail that belong to the owning document.
- **Not an availability claim.** A descriptor may not imply that unimplemented, bootstrap-only, archived, or experimental capability is available.
- **Not a substitute for the technical name.** External surfaces that require an exact identifier (artifacts, build configuration, imports, URLs, CI definitions) always use the technical name.

### Coverage inventory

[TAVALL_DESCRIPTOR_INVENTORY.md](TAVALL_DESCRIPTOR_INVENTORY.md) is a derived projection that inventories current repositories and verified modules against this format, together with coverage counts and open owner-review conflicts. It is evidence of current coverage, not a second authorization source: the owning README, accepted design, and source remain authoritative, and open conflicts are resolved there before a descriptor is promoted to `APPROVED`.

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
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/README_STANDARDS.md` | 2026-11-26 | `#156` descriptor standardization. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality/reference document; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/README_STANDARDS.md` | Same path | `#156` descriptor standardization. | Added the canonical human-readable descriptor format, field definitions, status vocabulary, and explicit non-goals; routed coverage to the derived descriptor inventory. |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/README_STANDARDS.md` | — | Direct docs-only update to `main`. | Added canonical private/public/module README ownership and delegation rules. |

</details>
