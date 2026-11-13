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

This branch is the persistent repository-level integration root for Tavall Docs (Generation 3). Normal documentation PRs target `staging/quality-v2`. Pull requests remain the work and review records; this manifest identifies the integration root and tracks active composition.

## Baseline Reconciliation

This staging root incorporates all commits from `main` up to `f2dbabe46eebc58401abcc62662ff914c0722f06`.

## Active Staging Membership

| PR | Branch | Target Base | Scope |
|---|---|---|---|
| [#93](https://github.com/TavallStudios/tavall-docs/pull/93) | `docs/manager-class-role-gate-20261029` | `staging/quality-v2` | Docs: Define the Tavall *Manager anti-pattern and migration ownership gate |
| [#95](https://github.com/TavallStudios/tavall-docs/pull/95) | `design/work-graph-linear-qa-github-reconciliation-20261101` | `staging/quality-v2` | docs(work): reconcile QA execution with GitHub Issues, Linear, Notion and TODO projections |
| [#97](https://github.com/TavallStudios/tavall-docs/pull/97) | `working/ten-day-discussion-reconciliation-20261103` | `staging/quality-v2` | docs: approve non-rejected Tavall ideas for existing document types, Work Graph and launch-first intake |
| — | `working/w15-docs-todo-retirement-107` | `staging/quality-v2` | Work Graph: retire legacy unlinked TODO.md items and transition to generated GitHub Issues views (#107) |
