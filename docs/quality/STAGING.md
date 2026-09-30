# Tavall Docs Staging

This file records the persistent repository/release staging boundary for the
canonical documentation repository.

- Branch: `staging/quality`
- Parent: `main`
- Role: repository/release staging
- State: `ACTIVE`
- Promotion: manual through the staging pull request

The staging pull request is the integration root for documentation changes that
must be reviewed as a composed tree. Child pull requests target this branch or
an active dependency branch that reaches it. GitHub pull requests and their
current heads remain authoritative; this file is only a repository-local
topology marker.

## Current composition

The staging branch was refreshed from current `main` at `6e1951b9d30bfe3202b125762d0c5e141c7cb262` in commit `38c7c5ba73728be823c627f4a8b253c0d9cf6637`. Its active root is [PR #34](https://github.com/TavallStudios/tavall-docs/pull/34). Child PR #31 merged into this root at `b635ed000f686ad5b0dcf0ba6ead7398564d1541` after its exact-source Executor profile passed. The active documentation child is now [PR #41](https://github.com/TavallStudios/tavall-docs/pull/41), targeting this branch and recording the September 30 Cloud CI/CD runtime acceptance.

Root #34 remains Draft. Its exact composed head `b635ed000f686ad5b0dcf0ba6ead7398564d1541` passed `QUALITY` and `REQUIRED_ALL` on the shared Executor in job `46be4d4d-a5c0-4f69-b434-f7dcc1b713d7`. PR #41 still needs exact child validation and a new exact-root run after merge. This staging branch does not authorize a public-route or Production cutover.
