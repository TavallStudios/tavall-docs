# Public Repository README Template

> **Status:** Active template  
> **Use when:** Creating or materially restructuring the root README of a public Tavall repository  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md)

Use only sections that apply. Delete instructional placeholders when instantiating the template.

```markdown
# <Project Name>

> **<Public Name> (`<technical-name>`) — <Descriptor>**
>
> **What it does:** <One concrete sentence grounded in current accepted ownership and current source.>
>
> **Does not own:** <Explicit boundary callout — only where confusion creates material risk; delete this line when it does not apply.>
>
> **Descriptor status:** `PROPOSED` / `REVIEWED` / `APPROVED` / `STALE`

<Logo, screenshot, or useful project visual when applicable.>

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

- The first screen must carry the standardized descriptor orientation block from [README_STANDARDS.md](README_STANDARDS.md) "Human-readable descriptors (What is this?)": `Public Name (technical-name) — <Descriptor>`, one "What it does" sentence, an optional "Does not own" callout, and the descriptor status.
- The descriptor answers "What kind of thing is this?" in 2–6 plain-language words. It does not replace or reword the project name, and it never carries a claim the project cannot support today.
- The first screen should make the project understandable without requiring repository archaeology.
- Public READMEs prioritize value, proof, usage, and contribution over internal operational structure.
- Curate documentation instead of exposing the complete private/internal document map.
- Do not expose private deployment targets, internal progression records, credentials, private infrastructure topology, or non-public system relationships.
- A public README may summarize architecture, but authoritative architecture remains in the owning documentation.
- When a repository moves from private to public, restructure the README against this template instead of merely deleting sensitive lines from the private README.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | 2026-11-26 | `#156` descriptor standardization. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality template; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | Same path | `#156` descriptor standardization. | Added the standardized top descriptor orientation block (public name, technical name, descriptor, one-sentence "What it does", optional "Does not own", descriptor status). |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/PUBLIC_REPOSITORY_README_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical public root README template. |

</details>
