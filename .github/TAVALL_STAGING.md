# Tavall Documentation Staging Root

```text
<!-- tavall-staging:v1 -->
Type: REPOSITORY_INTEGRATION
State: ACTIVE
Branch: staging/quality-v2
Parent: main
Promotion: MANUAL
ChildMergeTarget: staging/quality-v2
```

This branch is the persistent repository-level integration root for Tavall Docs (Generation 2). Normal documentation PRs target `staging/quality-v2`. Pull requests remain the work and review records; this manifest identifies the integration root and tracks active composition.

## Historical Reconciliation (`NEEDS_RECONCILIATION`)

The following pull requests were merged directly into `main` without passing through staging ancestry between 2026-11-01 and 2026-11-07:

| PR | Branch | Head SHA | Merged At (UTC) | Description |
|---|---|---|---|---|
| [#96](https://github.com/TavallStudios/tavall-docs/pull/96) | `working/tech-stack-docs-reconciliation-20261103` | `b3bcada` | 2026-11-03T21:40:00Z | docs: reconcile Tavall-wide technology stack and domain owners |
| [#102](https://github.com/TavallStudios/tavall-docs/pull/102) | `working/wdoct-issue-types-priority-20261104` | `9e2b1a9` | 2026-11-06T04:45:00Z | docs(quality): add GitHub Issue Types and Priority section to WORK_TRACKING |
| [#104](https://github.com/TavallStudios/tavall-docs/pull/104) | `working/wdb-database-design-20261107` | `b60a5d7` | 2026-11-07T02:05:00Z | docs(architecture): add Database and Persistence Environment Separation DESIGN |

All historical commits up to `3f9f3716de4ca3a5c90d9db250f397f131f87ff2` are included in `staging/quality-v2`.

## Intended Child PRs (Active Membership)

| PR | Branch | Target Base | Head | Scope |
|---|---|---|---|---|
| [#93](https://github.com/TavallStudios/tavall-docs/pull/93) | `docs/manager-class-role-gate-20261029` | `staging/quality-v2` | `e971eb9` | Docs: Define the Tavall *Manager anti-pattern and migration ownership gate |
| [#95](https://github.com/TavallStudios/tavall-docs/pull/95) | `design/work-graph-linear-qa-github-reconciliation-20261101` | `staging/quality-v2` | `6bf8bc8` | docs(work): reconcile QA execution with GitHub Issues, Linear, Notion and TODO projections |
| [#97](https://github.com/TavallStudios/tavall-docs/pull/97) | `working/ten-day-discussion-reconciliation-20261103` | `staging/quality-v2` | `649eb72` | docs: approve non-rejected Tavall ideas for existing document types, Work Graph and launch-first intake |
| [#103](https://github.com/TavallStudios/tavall-docs/pull/103) | `working/wrel-release-runbook-20261107` | `staging/quality-v2` | `584acfe` | docs(quality): add Tavall service Release on a Dime runbook |
