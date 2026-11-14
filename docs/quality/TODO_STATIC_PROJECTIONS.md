# Repository TODO Static Projections

> **Status:** RETIRED / HISTORICAL V1 PROJECTION POLICY<br>
> **Applies to:** Every maintained `TavallStudios` repository<br>
> **Authority:** Current work tracking follows [Work Tracking](WORK_TRACKING.md); this page preserves the retired static projection proposal for historical reference<br>
> **Purpose:** Record the former root `TODO.md` projection proposal. It is not an active work intake or synchronization contract.

## Transition contract (2026-10-22)

The former proposal was canonical owner-repository GitHub Issues, a GitHub Projects board, and Bot-generated repository TODOs. The owner retired the Tavall GitHub Bot on 2026-11-04. Current work originates in owner-repository GitHub Issues and feeds the QA Task Board; direct GitHub CLI operations use the typed `tavall-gh` wrapper. The Bot-based projection proposal and its v1/v2 rollout are superseded. See [Work Tracking](WORK_TRACKING.md) and the historical [Wave 1 Audit](../progression/TAVALL_WORK_GRAPH_LEGACY_TODO_MIGRATION_20261022.md).

## Current work tracking

Create and update active work in the owning repository's GitHub Issues through `tavall-gh`, then track execution on the QA Task Board using the issue URL as the key. Root `TODO.md` files are not work origins, task ledgers, or an active Bot-generated projection contract.

`tavall-gh` provides typed GitHub CLI invocation, authentication, environment mapping, and error translation. It does not generate, synchronize, or own repository `TODO.md` files.

Historic generated files and old instructions may remain in repository history. Do not add new active work there; reconcile any still-open legacy item into its canonical owner-repository issue.

## Required projection shape

The format below is a historical example only; it is not a current requirement.

The previous proposal pointed back to the canonical global document and routed human changes through that source.

Historical v1 example:

```markdown
# Repository TODO

<!-- tavall-todo-projection
source: https://github.com/TavallStudios/tavall-docs/blob/main/TODO.md
repository: TavallStudios/example
managed-by: TavallStudios/tavall-github-bot (retired)
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

The comments were proposed as machine metadata for a generator that was not accepted as the current work-tracking path.

## Synchronization rules

The former GitHub Bot synchronization plan is retired. No active tool owns root `TODO.md` generation. The issue-driven Work Tracking policy supersedes the former watch, render, and branch/PR synchronization requirements. Any future projection work must begin from an owner-repository issue and its linked QA Task Board task; do not assign it to `tavall-gh` without an explicit scope change.

## Human editing rules

- Create and update active work in the canonical owner-repository GitHub Issue through `tavall-gh`, then update the linked QA Task Board task.
- Do not add active tasks to global or repository `TODO.md` files or use a checkbox as task state.
- Existing `TODO.md` content may be retained as historical context while open legacy items are reconciled into canonical issues.
- Repository-specific implementation documents may still contain `DOC TODO:` maintenance handoffs; those are document-maintenance state and do not replace this repository work ledger.

## Relationship to `DOC TODO:`

`DOC TODO:` belongs to an individual document and carries maintenance handoff for that document under `DOCUMENTATION_STANDARDS.md`.

Root `TODO.md` is different: it is a repository-level legacy file, not active issue intake or a QA execution task. No GitHub Bot is active to scrape `DOC TODO:` blocks, and `tavall-gh` does not generate projections. Promote new work only through an owner-repository GitHub Issue and its linked QA Task Board task.

## Rollout

The former rollout proposed generated root projections and a long-term Bot implementation. That rollout is retired; it is not an active integration or a deliverable owned by `tavall-gh`.

## DOC TODO:

### Document next steps

- [ ] Retain this retired policy as historical context until its legacy projection references have been reconciled.

### System next steps

- No active projection automation work is owned by this document. Any future projection work starts from an owner-repository GitHub Issue and its QA Task Board task.

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/TODO_STATIC_PROJECTIONS.md` | 2026-11-14 3:47 PM PST | Change pending PR on `working/docbot-retire-github-bot-20261114`. |
| Notion | `NOT_APPLICABLE` | — | 2026-10-01 | Generated repository-control policy; no 1:1 Notion twin assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-01 | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/TODO_STATIC_PROJECTIONS.md` | — | Direct docs-only update to `main`. | Established the canonical global TODO and repository projection contract. |
| 2026-11-14 3:47 PM PST | GitHub | `UPDATED_PENDING_NOTION_SYNC` | `TavallStudios/tavall-docs/docs/quality/TODO_STATIC_PROJECTIONS.md` | Same path | Branch `working/docbot-retire-github-bot-20261114`; PR pending. | Marked the Bot-based projection proposal retired and directed active work to owner-repository issues and the QA Task Board. The existing Notion status is `NOT_APPLICABLE`. |

</details>
