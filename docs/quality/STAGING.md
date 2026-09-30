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

The staging branch was refreshed from current `main` at `6e1951b9d30bfe3202b125762d0c5e141c7cb262` in commit `38c7c5ba73728be823c627f4a8b253c0d9cf6637`. Its active root is [PR #34](https://github.com/TavallStudios/tavall-docs/pull/34). The CI/CD evidence child PR #31 merged into this root at `b635ed000f686ad5b0dcf0ba6ead7398564d1541`; Cloud acceptance child PR #41 merged at `be1524db391249ea66eb1c1915a161a27185d82b`; and staging-status child PR #42 merged at `884a244823890a51dd215d5af0d1880402b40001`.

Root #34 remains Draft. The composed root head `b635ed000f686ad5b0dcf0ba6ead7398564d1541` passed `QUALITY` and `REQUIRED_ALL` on the shared Executor in job `46be4d4d-a5c0-4f69-b434-f7dcc1b713d7`. After PR #41 merged, head `be1524db391249ea66eb1c1915a161a27185d82b` passed the same profiles in job `5a117cec-0e26-4dd1-8839-8167e65e6814`. After PR #42 merged, head `884a244823890a51dd215d5af0d1880402b40001` passed the same profiles in job `c809aaa3-5937-41de-8430-0bf4a26fdb4f`. These are exact-source Tavall CI Executor results; this staging branch does not authorize a public-route or Production cutover.
