# Public Repository README Template

> **Status:** Active template  
> **Use when:** Creating or materially restructuring the root README of a public Tavall repository  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md)

Use only sections that apply. Delete instructional placeholders when instantiating the template.

```markdown
# <Project Name>

<Logo, screenshot, or useful project visual when applicable.>

<One strong sentence explaining what the project does.>

<Short supporting paragraph explaining why it exists or what makes it useful.>

<Only meaningful badges: CI, release, license, language/runtime, etc.>

## Why <Project>

- ...
- ...
- ...

## Features

- ...
- ...
- ...

## Quick Start

### Install / Dependency

...

### Minimal Example

...

## How It Works

<Short external-facing architectural explanation. Link detailed architecture instead of reproducing it.>

## Example / Demo

<Screenshots, GIFs, CLI output, code samples, protocol traces, or other proof when useful.>

## Project Structure

<Include only when it materially helps users/contributors.>

## Documentation

Curated external-facing links only, for example:

- Getting Started
- API / Usage
- Architecture
- Examples
- Contributing

## Requirements / Compatibility

...

## Building From Source

...

## Contributing

...

## License

...
```

## Template Rules

- The first screen should make the project understandable without requiring repository archaeology.
- Public READMEs prioritize value, proof, usage, and contribution over internal operational structure.
- Curate documentation instead of exposing the complete private/internal document map.
- Do not expose private deployment targets, internal progression records, credentials, private infrastructure topology, or non-public system relationships.
- A public README may summarize architecture, but authoritative architecture remains in the owning documentation.
- When a repository moves from private to public, restructure the README against this template instead of merely deleting sensitive lines from the private README.

### Published workflow repositories

A published Tavall Workflow may live in its own public `TavallStudios/workflow-<kebab-name>` repository when the workflow is publishable without secrets, private Tavall source, or customer data. The workflow repository is the canonical source for that workflow's runnable definition, user documentation, version history, and changelog.

`TavallStudios/tavall-workflows` owns the aggregate workflow registry and is the index of published workflow sources; a registry entry points to the canonical workflow repository and its selected version. Tavall web workflow listings link to that repository as the canonical source/discovery destination. These links do not imply that a workflow is executable through a deployed Workflows runtime or MCP endpoint.

Use only the manifest and execution contract implemented by the current Tavall Workflows owner. A repository or registry entry must not claim Tavall Workflows/MCP execution until that contract is available and the workflow has been verified through it. Do not invent a competing manifest format to fill a runtime gap. Keep workflows containing private source, customer data, or secrets out of public repositories; retain them privately until a safe, publishable definition can be separated.

Apply the owning Tavall open-source/license policy when one exists. This template does not grant a license or choose one on behalf of a workflow owner; when the applicable policy or a repository's chosen license cannot be established, record the gap and do not imply that public visibility grants reuse rights.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | 2026-11-16 8:51 AM PST | [Docs issue #139](https://github.com/TavallStudios/tavall-docs/issues/139), parent [Workflows issue #20](https://github.com/TavallStudios/tavall-workflows/issues/20); PR evidence pending. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality template; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical public root README template. |
| 2026-11-16 8:51 AM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | Same path | [Docs issue #139](https://github.com/TavallStudios/tavall-docs/issues/139); PR evidence pending | Added the public workflow repository, registry-index, web-link, runtime-contract, and licensing-gap rules. |

</details>
