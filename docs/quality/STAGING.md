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

## Staging checkpoint — 2026-11-09 12:33 AM PST

The active `staging/quality-v2` branch advanced from
`2478bb5600333383a28e6c6b3a16e9a7063d4a37` to
`356d14ac9fdfbb52f5ad34f57790a799e682bb94` by merging focused Docs PR #115.
That child contains GitHub issue title-prefix Type and issue label/body Priority
source guidance. Its exact source head
`abafe5de1c56de19413477b02ff042b9ca1cfde3` passed `REQUIRED_ALL` in request
`59687e94-fa0b-4e9a-8c6a-1170bb2de1d2`. A fresh `REQUIRED_ALL` check of the
composed staging head is pending; this checkpoint does not claim that result.

## Staging reconciliation — 2026-11-09 12:50 AM PST

The prior composed head `edb15187aff6aba2e586ac6f96f1ee4f352454cd`
passed `REQUIRED_ALL` in request
`3f0c3e33-ed24-4a15-9e20-61b8a4da6b0c`. Current `main` later advanced to
`ec5c161e6b1cbc7a198cc21bbce25791c45cfed9`; that source was merged into this
staging line. The overlapping Work Tracking policy was reconciled to retain
GitHub title prefixes as the Type source, native issue Type synchronization,
and P0-P6 Priority derived only from existing issue labels/body markers, per
the explicit owner correction. This changed composition requires a fresh
exact-head `REQUIRED_ALL` check; the earlier result does not cover it.

Current reconciled staging head is
`2a0813d399a7c6dbe14b697930d05188498ff95a`. It includes the current main
baseline, focused Docs PR #115, and the owner-corrected Work Tracking policy.
Its fresh exact-head composed validation is pending.

## Staging root succession — 2026-11-09 1:10 AM PST

Generation 3 root PR #108 was promoted to `main` at merge commit
`7ab2ad1bdd02c41149d2546fbd643307c56f00c1` after the exact composed head
`5f07bfdd5bc77485d613885593fafff8d142fc66` passed `REQUIRED_ALL` in request
`da9ad924-eec3-4b58-81bf-2a8990a49f2f`. The `staging/quality-v2` branch is
preserved as the base for active child PRs #93, #95, and #97. A successor
active staging root is being established on this same branch before further
child integration.

Successor root PR #116 is open in Draft as the active Generation 4 root. Its
branch is `staging/quality-v2`; initial head was
`4bdfef92bfeccc049dfe0e786dc72976f90f8554`. The head will advance with this
manifest checkpoint before exact-head validation. Active children #93, #95,
and #97 continue to target the same staging branch.

## Staging root succession — 2026-11-09 1:37 AM PST

Generation 4 root PR #116 was promoted to `main` at merge commit
`aa5f18ee508d9947db5ed50f32e9672b7403a9b3` after exact composed head
`8ad13b961cec9e86dc966cba64adf394ae47d200` passed `REQUIRED_ALL` in request
`30a90b71-9340-490c-bad8-ab718e0784cb`. Active child PRs #93, #95, and #97
remain based on `staging/quality-v2`; the successor root will use that same
branch to preserve their ancestry.

Successor root PR #117 is open in Draft as the active Generation 5 root. It
uses the same `staging/quality-v2` branch; its initial head was
`5a4a1f56f5e46c87f7bb8870d49c74121eef6fda`. Active child PRs #93, #95, and
#97 remain attached to this branch. Exact-head CI is pending.

## Staging root succession — 2026-11-09 2:27 AM PST

Generation 5 root PR #117 was promoted to `main` at merge commit
`5efdc7b2a5ec3b91095fc9b4e9a12cb38a69b615` after exact composed head
`8a8598a57b248e1c695fe5acdf9849429cb0f9cc` passed `REQUIRED_ALL` in request
`e2676e12-9b1f-45d1-ab48-2f2b13492d32`. Active child PRs #93, #95, and #97
remain based on `staging/quality-v2`; the successor root will use the same
branch to preserve their staging ancestry.
