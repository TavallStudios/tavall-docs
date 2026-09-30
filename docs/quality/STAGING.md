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

## Staging checkpoint — 2026-09-30

The staging branch was refreshed from current `main` at `6e1951b9d30bfe3202b125762d0c5e141c7cb262` in commit `38c7c5ba73728be823c627f4a8b253c0d9cf6637`. Its root PR is [#34](https://github.com/TavallStudios/tavall-docs/pull/34). The CI/CD evidence child PR #31 merged at `b635ed000f686ad5b0dcf0ba6ead7398564d1541`; Cloud acceptance child PR #41 at `be1524db391249ea66eb1c1915a161a27185d82b`; staging-status PR #42 at `884a244823890a51dd215d5af0d1880402b40001`; status-evidence PR #43 at `d3241ae50932e1c950353d56fe88611399c0f65b`; and this follow-up at `d5a696013ffe1245a66c2904eed418b6ed473656`.

Root #34 remains Draft. Its composed heads `b635ed000f686ad5b0dcf0ba6ead7398564d1541`, `be1524db391249ea66eb1c1915a161a27185d82b`, `884a244823890a51dd215d5af0d1880402b40001`, `d3241ae50932e1c950353d56fe88611399c0f65b`, and `d5a696013ffe1245a66c2904eed418b6ed473656` each passed `QUALITY` and `REQUIRED_ALL` on the shared Executor in jobs `46be4d4d-a5c0-4f69-b434-f7dcc1b713d7`, `5a117cec-0e26-4dd1-8839-8167e65e6814`, `c809aaa3-5937-41de-8430-0bf4a26fdb4f`, `eb43376d-ea4a-406c-9c7a-37e6b3983717`, and `1a1aec9c-d288-480a-bdeb-a858abf7912a`, respectively. These are exact-source Tavall CI results at each checkpoint. A later child merge requires a fresh exact-root validation; this checkpoint does not authorize a public-route or Production cutover.
