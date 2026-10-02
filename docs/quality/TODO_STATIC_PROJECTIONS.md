# Repository TODO Static Projections

> **Status:** Active  
> **Applies to:** Every maintained `TavallStudios` repository  
> **Authority:** `TavallStudios/tavall-docs/TODO.md` is the only canonical organization-wide TODO ledger  
> **Purpose:** Give every repository an immediately visible root TODO without creating fifty-five independent task authorities, because apparently distributed consensus was not already causing enough problems.

## Contract

Every maintained TavallStudios repository exposes a root `TODO.md`.

For `TavallStudios/tavall-docs`, that file is the canonical global ledger.

For every other repository, root `TODO.md` is a **static generated projection** owned by `TavallStudios/tavall-github-bot`. It is not an independently maintained documentation source and it is not a new Tavall documentation type.

## Required projection shape

The first substantive section after the file title and generated metadata must be the repository's own section from the global TODO ledger.

A generated projection must then point back to the canonical global document and explain that human changes belong in the global source first.

Canonical shape:

```markdown
# Repository TODO

<!-- tavall-todo-projection
source: https://github.com/TavallStudios/tavall-docs/blob/main/TODO.md
repository: TavallStudios/example
managed-by: TavallStudios/tavall-github-bot
format-version: 1
source-commit: <commit sha>
synced-at: <ISO-8601 timestamp>
-->

## Repository TODO

<verbatim projected contents from the repository's global TODO section>

## Global authority

Canonical source: https://github.com/TavallStudios/tavall-docs/blob/main/TODO.md

This file is generated. Add or change tasks in the global TODO first.
```

The comments are machine metadata, not decorative prose. The bot may update them whenever the projection changes even when the visible task list is otherwise identical.

## Synchronization rules

`tavall-github-bot` owns synchronization.

The bot must:

1. Watch changes to `TavallStudios/tavall-docs/TODO.md`.
2. Detect repository creation, rename, archive, reactivation, and other inventory changes that affect the global ledger.
3. Parse repository sections by exact `owner/repository` identity.
4. Render the matching repository section as the first substantive section in root `TODO.md`.
5. Preserve the canonical generated metadata comment block.
6. Use one deterministic synchronization branch/PR per repository and update an existing synchronization PR instead of opening duplicates.
7. Target `main` unless the repository's documented canonical branch explicitly differs.
8. Validate that the projected task body exactly matches the source section before considering the repository synchronized.
9. Never ingest ad-hoc local edits back into the global TODO automatically.
10. Leave explicit empty-state text when a repository currently has no open global TODO entries.

## Human editing rules

- Add, remove, reorder, or rewrite repository tasks in `TavallStudios/tavall-docs/TODO.md`.
- Do not treat a generated repository `TODO.md` as authority.
- A local emergency edit may be used only to repair broken generated metadata or rendering, and must be reconciled back through the global source immediately.
- Repository-specific implementation documents may still contain `DOC TODO:` maintenance handoffs; those are document-maintenance state and do not replace this repository work ledger.

## Relationship to `DOC TODO:`

`DOC TODO:` belongs to an individual document and carries maintenance handoff for that document under `DOCUMENTATION_STANDARDS.md`.

Root `TODO.md` is different: it is a repository-level projection of organization work owned by the global TODO ledger. The GitHub bot must not scrape every `DOC TODO:` block into the global backlog unless a separate workflow explicitly promotes an item.

## Rollout

The initial organization-wide rollout creates root projections through PRs targeting each repository's `main` branch. `tavall-docs/TODO.md` and this policy are updated directly on `main` as shared documentation authority.

The long-term bot implementation is tracked in the `TavallStudios/tavall-github-bot` section of the global TODO.

## DOC TODO:

### Document next steps

- [ ] Keep this contract synchronized with the GitHub bot implementation once projection automation lands.
- [ ] Add exact implementation evidence and bot command/event names after the automation is built.

### System next steps

- [ ] Complete initial root `TODO.md` rollout across every maintained TavallStudios repository.
- [ ] Implement and validate GitHub-bot-managed synchronization.

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/TODO_STATIC_PROJECTIONS.md` | 2026-10-01 | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-10-01 | Generated repository-control policy; no 1:1 Notion twin assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-01 | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/TODO_STATIC_PROJECTIONS.md` | — | Direct docs-only update to `main`. | Established the canonical global TODO and repository projection contract. |

</details>
