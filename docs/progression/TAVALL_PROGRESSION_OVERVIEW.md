# Tavall Progression Overview

> **Document Type:** Progression / Evidence Roll-up  
> **Status:** Active consolidation snapshot  
> **Audit Date:** 2026-09-21  
> **Purpose:** Give one Tavall-wide view of demonstrated implementation state, remaining gates, and unreconciled progression evidence without replacing the owning progression documents.  
> **Must Not Define:** Product behavior, architecture contracts, schemas, command contracts, deployment authorization, or validation that the owning progression documents do not claim.

## 1. Authority and source-selection rules

This document is a roll-up. The owning `*_PROGRESSION.md` document remains the source of truth for its system at the exact repository revision it records.

Use this authority order when collecting or acting on progression evidence:

1. The owning repository's current `main` progression document is the production baseline.
2. An explicitly selected staging branch or open pull-request branch may contribute newer **unmerged evidence**, but that evidence does not silently replace the `main` baseline.
3. A worktree, executor workspace, temporary checkout, `.codex-worktrees` directory, or legacy `/srv/workspace` path is never authoritative merely because it exists on disk.
4. Before reading implementation or progression state, resolve the selected repository root, remote repository identity, branch/ref, and exact head SHA.
5. When the same logical progression path has multiple blobs across reachable worktrees, reconcile the variants before using branch-only claims as current system state.
6. Merged, superseded, abandoned, and prunable worktrees should be removed after useful evidence is preserved in GitHub history or the owning progression document.

AI and automation should therefore search **inside the selected repository/ref**, not recursively across all of `/srv/workspace`, `/srv/dev-storage`, `.codex-worktrees`, or `/tmp` and then trust whichever matching filename appears first.

## 2. Snapshot boundary

The GitHub production baselines observed during this audit were:

- `TavallStudios/tavall-mc` `main` at `db26e3297c5ac8a96914e6222776cbb2cb82c69c`.
- `TavallStudios/tavall-cloud` `main` at `aad9af1c2bf9c1b4a2d63cbf34bf16f5666427b9`.
- `TavallStudios/tavall-docs` `main` as the base of `working/progression-consolidation-20260921`.

The remote filesystem audit also inspected registered Git worktree heads so branch-only progression updates would not be discarded as noise.

### Inventory and divergence

| Repository | Production progression inventory | Reachable worktree heads inspected | Logical trackers with multiple observed blobs | Notes |
| --- | ---: | ---: | ---: | --- |
| `tavall-mc` | 46 | 35 | 24 | Existing `docs/progression/README.md` lists only 38 systems and is stale relative to current tracker headers. |
| `tavall-cloud` | 4 | 31 | 3 | Networking was identical across inspected heads; Cloud overview, service deployment, and GitHub operations bridge had divergent variants. |

Highest observed `tavall-mc` divergence:

- 9 variants: Runtime Module, FFA, Effect, Tavall Web Cloud Operations, Tavall Web Moderation Admin.
- 7 variants: Moderation and Support.
- 6 variants: Purchase Commerce.
- 4 variants: Website, Essentials, PvP Achievement, Minecraft Cloud, Chat Format.
- 3 variants: World, FFA Region and Respawn, Message, Kingdom, Discord, Player Identity and Store, Account.
- 2 variants: Resource Pack, Lobby, Currency, Building, Battle.

A variant count greater than one does **not** mean the newest timestamp wins. It means the logical tracker requires lineage-aware reconciliation.

## 3. Tavall MC / Project Novus current-state matrix

The status column reflects the production tracker on `main` when the tracker exposes a single status. Table-driven trackers are summarized without inventing a stronger claim. The final column records the number of distinct progression blobs observed across the audited worktree heads.

| System | Production baseline | Major remaining gate | Variants observed |
| --- | --- | --- | ---: |
| Account | Source Implemented / Integration Unverified | Java 25 checks, PostgreSQL migration/concurrency, browser and game E2E | 3 |
| Player Identity and Store | Automated Tests Passed (Backend / FFA / Velocity) / Paper Unverified | Paper runtime and client verification | 3 |
| Achievement | Partially Implemented | Execute registry/persistence tests and one duplicate-safe E2E completion | 1 |
| Anti-Cheat | Implemented / Existing | Proxy integrity matrix, backend-switch enforcement, reconnect recovery | 1 |
| Battle | Implemented / In Progress | Backend/Paper tests, castle battle smoke, manual hotbar review | 2 |
| Building | Implemented / In Progress | Definition/repository/production/upgrade tests and representative gameplay flows | 2 |
| Chat Format and Placeholder | Automated Tests Passed / Live Integration Unverified | PostgreSQL registry overrides and live multi-player Velocity command matrix | 4 |
| Citizen | Implemented / In Progress | Grouped-storage/command tests and create/group/assign/restart flow | 1 |
| Minecraft Cloud | Predominantly Live / Reactor and Mineflayer matrix passing | Routine monitoring plus expansion only as command scope grows | 4 |
| Command Mode | Partially Implemented | MVP tests and manual selection/render/cancel/reconnect/transfer review | 1 |
| Purchase Commerce | Source Implemented / Integration Pending | Java 25 gates, linked/unlinked identity flows, payment/provider integration | 6 |
| Companion | Implemented / In Progress | Stat/trait/mood/repository tests and lifecycle/restart flows | 1 |
| Cosmetic | Partially Implemented | Authorization tests, entitlement storage audit, apply/remove lifecycle | 1 |
| Currency | Implemented / In Progress | Currency/balance/shop/persistence tests and overflow/reconnect smoke | 2 |
| Custom Entity | Implemented / In Progress | Registry/spawn/identity/cleanup tests and unload/restart flow | 1 |
| Custom Item | Partially Implemented | Item/timer tests and acquisition/serialization/consume/retry/reconnect | 1 |
| Cutscene | Implemented / Existing | Command tests and manual playback/skip/cancel/disconnect/death/transfer review | 1 |
| Discord | Source Implemented / Integration Unverified | Java 25/storage checks, PostgreSQL migrations, live Discord/account projection | 3 |
| Moderation and Support | Source Merged / Live Acceptance Pending | Java 25 persistence/concurrency, permissions matrix, live Velocity/Discord/Web acceptance | 7 |
| Effect | Implementation Started / Unverified | Repository checks, Paper scheduler/order tests, visual client verification | 9 |
| Event | Designed | Audit current contracts, then define typed lifecycle and settlement ownership | 1 |
| Guild | Implemented / In Progress | Persistence/command/territory tests and claim/contest/settle/restart flows | 1 |
| Backend Infrastructure | Implemented / Existing | Full clean check plus architecture audit of raw dependency and service patterns | 1 |
| Interior | Implemented / In Progress | Unit/integration/live routing plus create/enter/leave/reconnect/failure/restart | 1 |
| Kingdom | Implemented / In Progress | Java 25/Paper lifecycle verification and remaining module-scoped backend ownership | 3 |
| Lobby | Implemented / Unverified | Live join/protection/recovery/unload/reload verification | 2 |
| Live Market | Designed | Audit existing listing/order contracts, then define lifecycle/escrow/fees/settlement | 1 |
| Message | Implemented / In Progress | Reproducible dependency lock and complete message/placeholder/render/DI checks | 3 |
| Morale and Mood | Implemented / Existing | Tests plus mutation/reload/restart/duplicate-event flows | 1 |
| Permission | Implemented / Existing | Full command permission inventory and player/console/Paper/proxy rank matrix | 1 |
| Placement | Partially Implemented | Inventory all `/place` targets and validate building/capital restrictions | 1 |
| FFA Region and Respawn | Source Implemented / Validation Pending | Java 25, Redis/proxy authority, Paper/client respawn and regional routing validation | 3 |
| FFA | Integration Tested | Current Java 25 gate, live Paper lifecycle, migrations, translucency, 50-player load and client review | 9 |
| PvP Achievement | Implemented / Testing | PostgreSQL concurrency, cross-node retry, final AP/definition acceptance | 4 |
| Resource Node | Implemented / In Progress | Lifecycle/gather/persistence tests and concurrency/Redis-loss/restart flows | 1 |
| Resource Pack | Implemented / Existing | Deterministic assembly/install tests and accept/decline/fail/reconnect/backend-switch matrix | 2 |
| Runtime Module System | Implemented / Unverified | Java 25/artifact matrix, Paper/Velocity lifecycle, remove transitional global backend ownership | 9 |
| Speedrun | Not Audited | Establish or confirm accepted speedrun boundary before claiming implementation state | 1 |
| Essentials | Automated Tests Passed / Live Integration Unverified | Live Velocity/Paper routing, transfers, messaging, permissions and UI behavior | 4 |
| Timer and Speed-Up | Implemented / Testing | Unit/persistence/Redis/backup/live gameplay tests across every timer type | 1 |
| Troop | Implemented / In Progress | Grouped storage/simulation/commands and station/battle/restart flows | 1 |
| Native UI | Implemented / In Progress | Canvas/session/input/adapter tests and manual supported-resolution interaction review | 1 |
| Tavall Web Cloud Operations | Source surface implemented; runtime/browser validation pending | Rebuilt Tavall execution path, Cloud lifecycle validation, browser tests | 9 |
| Tavall Web Moderation Admin | Mostly source implemented; adapter/runtime/browser validation pending | Typed authenticated-principal adapter, permissions matrix, PostgreSQL and browser acceptance | 9 |
| Website and Live Progress | Implemented / In Progress | Web Java 25 tests plus desktop/tablet/mobile/keyboard/accessibility review | 4 |
| World and Server Flow | Implemented / In Progress | Routing/state harnesses and stale-TTL/Redis-loss/destination-failure/reconnect/restart | 3 |

## 4. Tavall Cloud current-state matrix

| Tracker | Production baseline | Major remaining gate | Variants observed |
| --- | --- | --- | ---: |
| Tavall Cloud | Mixed; most domain/control/provider paths implemented or live, Redis-only Job/environment authority active | Exact staging-head deployment, remaining failure/recovery matrices, remote storage and regional/network soak | 5 |
| Service Deployment | Source Implemented / Automated and Live Validation Pending | Focused/full tests, disposable install, apply/verify/rollback, unhealthy-release auto-rollback | 2 |
| Tavall Networking | Domain/edge implemented; Linux data plane, persistence, agent integration, probes and rollback live-validated; Minecraft partial | Extended soak, broader Minecraft cross-region matrix, future regional ingress | 1 |
| GitHub Actions Operations Bridge | **Superseded historical progression** | Do not use its pre-Redis PostgreSQL authority claims; replace/reconcile current evidence before treating it as active design | 2 |

## 5. What the consolidated picture says

The system is no longer primarily blocked on writing first-pass source. The dominant unfinished work is now:

1. **Validation debt:** Java 25 repository gates, real PostgreSQL/Redis behavior, Paper/Velocity runtime matrices, browser/client checks, and load/soak testing.
2. **Reconciliation debt:** branch-only progression evidence and stale worktrees contain competing snapshots of the same system.
3. **Lifecycle ownership debt:** the runtime module path still has transitional global/parent-owned backend composition that blocks clean unload/reload guarantees.
4. **Cross-surface acceptance:** account, commerce, Discord, moderation, Web, and Minecraft flows are implemented far enough that integration boundaries now matter more than additional isolated source.
5. **A smaller design backlog:** Event and Live Market remain designed rather than materially implemented; Speedrun remains explicitly not audited.

The strongest demonstrated production-facing areas are Minecraft Cloud integration, the FFA original gameplay/integration pass, and several Tavall Cloud control/network paths. Even those retain explicit soak, load, human/client, or failure-path gates.

## 6. Reconciliation queue

Reconcile tracker variants in this order because they combine high divergence with high architectural blast radius:

1. Runtime Module System.
2. FFA System.
3. Tavall Web Cloud Operations.
4. Tavall Web Moderation Admin.
5. Effect System.
6. Moderation and Support.
7. Purchase Commerce.
8. Chat / Essentials / Minecraft Cloud / PvP Achievement / Website.
9. Remaining 2-3 variant trackers.

For each logical tracker:

1. Identify all reachable blob variants and their branch/PR lineage.
2. Compare each variant to current `main` and to any accepted staging/integration ref.
3. Preserve only evidence that is still true under current architecture.
4. Merge that evidence into the owning tracker on a focused PR.
5. Mark superseded historical claims explicitly when deletion would erase useful audit history.
6. Remove or prune stale worktrees after their useful state is durable in GitHub.

## 7. Guardrails to prevent workspace-driven regressions

The Tavall agent/executor path should enforce these rules mechanically:

- Resolve `git rev-parse --show-toplevel` before reading repository policy or progression documents.
- Record repository identity, origin URL, branch/ref, head SHA, base ref, environment, lane, workspace, and executor in durable executor metadata.
- Reject or warn when the selected path is a nested worktree that was not explicitly bound to the task.
- Ignore `.codex-worktrees`, `/tmp` worktrees, prunable worktrees, and legacy workspace roots during ordinary source discovery.
- Never use a global `find /srv ... '*PROGRESSION*'` result as source selection.
- Prefer Git/GitHub lineage over filesystem modification time.
- When branch-only progression is newer, label it **unmerged evidence** until reconciled into the owning production tracker.
- Add a check that the per-repository progression index contains every tracked progression document and that its displayed status matches the owning tracker header or declared table-driven summary.

## 8. Immediate follow-up & Execution Status

1. **`tavall-mc/docs/progression/README.md` index:** COMPLETED via PR #304. Full 46-tracker inventory accurately indexed and linked with current statuses and audit rules.
2. **Dating of all 46 `tavall-mc` progression trackers:** COMPLETED via PR #304. Every tracker now enforces `YYYY-MM-DD` ISO dates with commit SHAs and verified evidence states.
3. **Dating of all 4 `tavall-cloud` progression trackers:** COMPLETED via PR #393.
4. **Dating of `tavall-web` progression trackers:** COMPLETED via PR #38 and PR #39.
5. **Java tool repository workflow centralization:** COMPLETED across all 9 Java repositories (PRs merged to `main`).
6. **Cross-repo Git workflow centralization:** COMPLETED across all 24 repositories containing stale copies.
7. **Tavall Docs master policy promotion:** COMPLETED via PR #14 -> `staging/quality` -> PR #2 -> `main` (`docs/quality/CI_CD.md` and `docs/quality/DOCUMENT_ROUTING.yml` live on `main`).
8. **Prune merged/superseded/prunable worktrees** after preserving useful branch/PR evidence.

## 9. Reconciliation Ledger and Active PR Tracking

The authoritative cross-repository inventory and authority model is maintained in [`TAVALL_DOCUMENTATION_RECONCILIATION_LEDGER.md`](TAVALL_DOCUMENTATION_RECONCILIATION_LEDGER.md).

### Merged Production & Staging PRs:
- **Tavall MC Progression Dating (46 trackers)**: [`TavallStudios/tavall-mc#304`](https://github.com/TavallStudios/tavall-mc/pull/304) (`MERGED_PRODUCTION`)
- **Tavall MC Bot-Testing Link Repair**: [`TavallStudios/tavall-mc#303`](https://github.com/TavallStudios/tavall-mc/pull/303) (`MERGED_PRODUCTION`)
- **Paper Fork Progression**: [`TavallStudios/tavall-mc-paper#4`](https://github.com/TavallStudios/tavall-mc-paper/pull/4) (`MERGED_PRODUCTION`)
- **Architecture Tests Progression**: [`TavallStudios/Tavall-Architecture-Tests#11`](https://github.com/TavallStudios/Tavall-Architecture-Tests/pull/11) (`MERGED_PRODUCTION`)
- **Minecraft Bot Testing Progression**: [`TavallStudios/tavall-mc-bot-testing#3`](https://github.com/TavallStudios/tavall-mc-bot-testing/pull/3) (`MERGED_PRODUCTION`)
- **Tavall Web Runtime Progression**: [`TavallStudios/tavall-web#38`](https://github.com/TavallStudios/tavall-web/pull/38) (`MERGED_PRODUCTION`)
- **Tavall Web Website Progression**: [`TavallStudios/tavall-web#39`](https://github.com/TavallStudios/tavall-web/pull/39) (`MERGED_PRODUCTION`)
- **Tavall Cloud Progression Dating**: [`TavallStudios/tavall-cloud#393`](https://github.com/TavallStudios/tavall-cloud/pull/393) (`MERGED_PRODUCTION`)
- **Tavall Discord Progression**: [`TavallStudios/tavall-discord#4`](https://github.com/TavallStudios/tavall-discord/pull/4) (`MERGED_STAGING`)
- **Tavall Minecraft Framework Progression**: [`TavallStudios/tavall-minecraft-framework#6`](https://github.com/TavallStudios/tavall-minecraft-framework/pull/6) (`MERGED_PRODUCTION`)
- **Tavall AI Git Workflow Disambiguation**: [`TavallStudios/tavall-ai#41`](https://github.com/TavallStudios/tavall-ai/pull/41) (`MERGED_PRODUCTION`)
- **Java Tools Standalone Workflow Migration**: 9 Repositories Merged to `main` (`MERGED_PRODUCTION`)
- **Consumer Quality Git Workflow Centralization**: 15 Repositories Merged to default branches (`MERGED_PRODUCTION`)

### Active Pending PRs:
- **Tavall Content Publishing Queue**: [`TavallStudios/tavall-content#11`](https://github.com/TavallStudios/tavall-content/pull/11) (`VALID_UNMERGED_WORK`)
- **Tavall MC Web Retirement & Store Boundary**: [`TavallStudios/tavall-mc#290`](https://github.com/TavallStudios/tavall-mc/pull/290) (`VALID_UNMERGED_PR`)
- **Tavall MC Selective Documentation Preflight**: [`TavallStudios/tavall-mc#285`](https://github.com/TavallStudios/tavall-mc/pull/285) (`VALID_UNMERGED_PR`, unblocked & rebased)
- **Tavall Docs Master Consolidation & Ledger**: [`TavallStudios/tavall-docs#24`](https://github.com/TavallStudios/tavall-docs/pull/24) (`VALID_UNMERGED_PR`)

