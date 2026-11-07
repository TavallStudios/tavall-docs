# Tavall Global TODO

> **Status:** Active  
> **Authority:** Canonical organization-wide TODO ledger  
> **Repository projections:** Every maintained TavallStudios repository exposes a bot-managed root `TODO.md` that projects only that repository's section from this file.  
> **Last updated:** 2026-10-29

**Transition notice (2026-10-22):** We are moving to [GitHub Issue-owned work tracking](docs/quality/WORK_TRACKING.md). For rows that contain a **canonical issue** link, that issue owns future task state and acceptance; the checkbox and prose here are **historical migration snapshots**. Unlinked rows retain their previous ledger authority until individually reconciled. Root TODO projections stay on their established v1 protocol until the GitHub Bot v2 generator is tested. See the [migration inventory](docs/progression/TAVALL_WORK_GRAPH_LEGACY_TODO_MIGRATION_20261022.md).

## Projection contract

- Each maintained TavallStudios repository has one root `TODO.md`.
- The repository's own section from this document is the first substantive section rendered in that local file.
- Local projections link back to this document and carry machine-readable HTML comments describing their source, repository, managing bot, format version, last source commit, and synchronization time.
- `TavallStudios/tavall-github-bot` owns synchronization. Human edits belong here first; the bot propagates the repository slice outward.
- Empty repository sections remain explicit so absence of work is distinguishable from a missing projection.

## Repository TODOs

### `TavallStudios/CustomMinecraftServer`

#### System — Custom Minecraft Server

- [ ] 2026-10-02 — Promote validated exact-source Gradle 9.6.1 build and Settings-to-build configuration to `main`.
  - Reconcile PR #4 against `main`.
  - Verify standalone server artifact production on `DEVELOPMENT_SHARED` executor.

### `TavallStudios/HyRhythm`

#### System — HyRhythm

- [ ] 2026-10-02 — Promote exact-source Gradle build and dependency configuration to `main`.
  - Reconcile PR #3 against `main`.
  - Verify plugin and patched server artifacts produced by Tavall CI.

### `TavallStudios/MCRSpeedrun`

#### System — MCR Speedrun

- [ ] 2026-10-02 — Promote multi-module lockfile refresh and exact-source build configuration to `main`.
  - Merge PR #4 to `main`.
  - Validate speedrun timer synchronization and tournament state transitions against current Minecraft server baseline.

### `TavallStudios/Tavall-Talent-and-Contractors-`

_No open global TODO items currently tracked._

### `TavallStudios/TavallContractors`

#### System — Tavall Contractors

- [ ] 2026-10-22 — Decide legacy Contractors executable ownership before changing the `spring-webview` RUNTIME module's noncompliant name.  ([canonical issue](https://github.com/TavallStudios/TavallContractors/issues/9))
  - If maintained independently, migrate the actual Gradle runtime/artifact toward `tavall-contractors-web-runtime` and the `internal-contractor-api` consumer references; if folded into the unified Tavall Web platform, prefer an API/presentation migration and retirement instead of a pointless legacy rename.
  - Do not change the `TavallContractors` repository root solely for suffix compliance; require exact-source Spring boot, request routing, provider/data integration and deployment rollback validation.


- [ ] 2026-10-02 — Promote local CI workflow removal and unified Gradle platform adoption to `main`.
  - Reconcile PR #3 onto `main`.
  - Validate contractor registry queries with current Tavall Database entity store.

### `TavallStudios/TavallCouriers`

#### System — Tavall Couriers

- [ ] 2026-10-02 — Establish canonical Tavall Cloud service template and development database contract.
  - Define `.tavallcd/cd.yaml` service template under `/srv/dev-storage/templates/services/tavallcouriers`.
  - Replace direct Spring Data JPA / Flyway credentials with canonical Tavall Database environment bindings.
  - Promote PR #4 (exact-source CI and refreshed lockfiles) to `main`.

### `TavallStudios/TavallMonoRepo`

_No open global TODO items currently tracked._

### `TavallStudios/Webstore`

#### System — Webstore

- [ ] 2026-10-02 — Complete retirement of legacy Webstore codebase in favor of Tavall Web unified store module.
  - Reconcile remaining store data models with `tavall-web` Web Store platform contracts.
  - Promote PR #4 to `main`.

### `TavallStudios/function-catalog`

#### System — Function Catalog

- [ ] 2026-10-22 — Bring the independently executable `mcp-server` Gradle module into Tavall naming as `tavall-function-catalog-mcp-runtime`, preserving the `function-catalog` repository name.  ([canonical issue](https://github.com/TavallStudios/function-catalog/issues/39))
  - Confirm module type against actual HTTP/stdio launchers, migrate Gradle project/artifact/entrypoints, provider consumers, packaging and Tavall CI/CD/service references in a compatibility-reviewed slice. `agent-runtime` is documented as a non-process LIBRARY and must **not** be misclassified as a separate RUNTIME just because of the old suffix.
  - Verify catalog scoped discovery, authenticated MCP transport, HTTP/stdio launch, provider-neutral function views, deployment artifact identity and rollback. Do not introduce a duplicate model runtime or Cloud authority.


- [ ] 2026-10-02 — Promote PR #14 (staging/platform) to `main` for Cloud developer CI capability contracts and legacy CI removal.
  - Verify immutable MCP server ZIP artifact generation on Tavall CI.
- [ ] 2026-10-02 — Resolve Linux Cloud Executor integration test prerequisites for Codex CLI.
  - Provision authenticated Codex CLI environment or mock provider for integration profile test suites.
- [ ] 2026-10-02 — Route public package publication through approved Tavall CI release flow rather than unauthenticated local scripts.

### `TavallStudios/hytale-bots`

#### System — Hytale Bots

- [ ] 2026-10-02 — Promote Node-based Tavall CI configuration to `main`.
  - Reconcile PR #2 to `main`.
  - Validate bot simulation scenarios against Hytale protocol definitions.

### `TavallStudios/minecraft-bot`

#### System — Minecraft Bot

- [ ] 2026-10-02 — Promote Node-based Tavall CI configuration to `main`.
  - Reconcile PR #2 to `main`.
  - Ensure protocol parser compatibility with current Paper 1.21 packet stream.

### `TavallStudios/tavall-ai`

- [ ] 2026-10-29 — Review [`GitWorktreeManager`](https://github.com/TavallStudios/tavall-ai/blob/main/tavall-ai-core/src/main/java/org/tavall/ai/app/orchestration/GitWorktreeManager.java) against the [`*Manager` role gate](docs/quality/code-architecture/CLASSES.md#the-manager-anti-pattern).
  - Existing class owns worktree preparation plus Git diff/status inspection. Identify whether these belong to one focused Git workspace operation Handler or already established Tavall Cloud Git/tool capabilities, before choosing a target name; preserve workspace lifecycle, current Spring integration and callers.
  - Verify the actual active Tavall AI branch/source and tests before migration. Avoid redundant Services, managers or parallel Git runtime facilities.


#### System — Tavall AI Platform

- [ ] 2026-10-22 — Normalize Tavall AI module types and suffixes without treating agents or non-process capabilities as independent runtimes.  ([canonical issue](https://github.com/TavallStudios/tavall-ai/issues/74))
  - Inventory active `settings.gradle.kts` modules versus the unlisted legacy `tavall-ai-core` source and move only validated active consumers. Reclassify `AGENT_PACKAGE`/`RUNTIME_CAPABILITY` as canonical primary types plus secondary roles; agents remain behavior packages loaded by the runtime, not RUNTIME/SYSTEM by assumption.
  - If the model-execution, browser, distributed-execution or project-context capability is confirmed as a SYSTEM, name its actual Gradle module `*-system`; the `tavall-ai-runtime` executable keeps its existing suffix. Do not rename a pure provider adapter to RUNTIME based on an old `runtime-` prefix.
  - Coordinate the planned dedicated Tavall AI Memory cutover and Docs Agent index regeneration; retain exact source, typed DI, Function Catalog policy, Cloud leases, provider permissions and agent registry compatibility. E2E: runtime bootstrap, opt-in capability disable/reload and no stale-generation capability access.


- [ ] 2026-10-02 — Promote Tavall Agent Stack V2 implementation from `working/tavall-agent-stack-v2` into plugin staging and `main`.
  - Integrate renamed agent providers (`LedgerAgentProvider`, `PrWorkflowAgentProvider`, `CodeArchitectureAgentProvider`, `PrReviewAgentProvider`, `PrReconciliationAgentProvider`, `E2EValidationAgentProvider`).
  - Verify all 57 Java architecture tests and 43 agent definitions pass validation.
- [ ] 2026-10-02 — Enforce mandatory work entry sequence (`tavall-agent-memory` -> `tavall-agent-ledger` -> `tavall-docs-agent` -> `tavall-orchestrator` -> selected agents) in runtime harness hooks.
  - Ensure callers never route directly to internal skills, tools, or MCPs.
  - Require all `AI_SUBAGENT` instances to register and claim scope in `tavall-agent-ledger`.
- [ ] 2026-10-02 — Promote reusable Tavall AI browser capability (PR #50) and integrate with consumers.
  - Wire browser capability through Tavall DI for `tavall-analytics` and content exploration.
- [ ] 2026-10-02 — Complete video explorer agent routing and plugin navigation links (PR #52, PR #53).

### `TavallStudios/tavall-ai-memory`

#### System — Tavall AI Memory

- [ ] 2026-10-22 — Select the canonical primary type and module/artifact name for the dedicated memory owner before migrating `tavall-ai-runtime-memory`.  ([canonical issue](https://github.com/TavallStudios/tavall-ai-memory/issues/4))
  - Keep the new repository name `tavall-ai-memory` unchanged. If the extracted memory composition is a SYSTEM, use an internal module such as `tavall-ai-memory-system`; if it remains an API/library capability, do not manufacture an independent RUNTIME. Migrate old imports and storage contracts only after consumers and exact-source validation pass.


- [ ] 2026-10-02 — Establish canonical graph-backed memory plane contracts and persistence models.
  - Define provider-neutral storage interfaces for entity relationships, decision histories, and context retrieval.
  - Implement memory retrieval constraints ensuring memory remains contextual evidence and cannot override canonical docs or live runtime truth.
- [ ] 2026-10-02 — Promote repository-owned `.tavallci` definition (PR #1) to `main` and execute exact-head CI validation.
- [ ] 2026-10-02 — Cleanly move `tavall-ai-runtime-memory` out of `TavallStudios/tavall-ai` into the dedicated `TavallStudios/tavall-ai-memory` repository.
  - Preserve module ownership and relevant history where practical, migrate runtime-memory code, tests, documentation, and configuration without leaving duplicate authority behind.
  - Update package, dependency, build, CI, agent, and consumer references before removing the old module from `tavall-ai`.
  - Validate exact-source builds for both repositories and the end-to-end memory-plane integration after cutover.

### `TavallStudios/tavall-analytics`

#### System — Tavall Analytics

- [ ] 2026-10-22 — Introduce explicit SYSTEM names and host-owned collector lifecycle in Analytics, replacing legacy blanket LIBRARY labels through reviewed slices.  ([canonical issue](https://github.com/TavallStudios/tavall-analytics/issues/18))
  - Candidate fan-in: `tavall-analytics-collection-system` for genuinely independent passive collectors and `tavall-analytics-analysis-system` for the `tavall-analytics-core` owner **if** source consumers justify SYSTEM classification. Review attribution, experiments, reporting and first-party modules for actual SYSTEM versus package/adapter ownership; require `-system` on each accepted SYSTEM, not on generic producer libraries.
  - Preserve `tavall-analytics-api`, `tavall-analytics-app` (APPLICATION), storage/provider adapters, the existing Minecraft passive-source modules and immutable-evidence semantics. Complete planned retirement of `tavall-analytics-content` after API consumer migration instead of inventing a second Content SYSTEM.
  - Validate exact-source ingestion, independent collector disable/reload only where the owning host supports it, PostgreSQL/NFS consistency, evidence provenance, module-local CI, and module-scoped Progression; do not represent collector host E2E as already implemented.


- [ ] 2026-10-09 — Consolidate Content-facing metrics, findings, and attribution contracts in `tavall-analytics-api`; retire the separate `tavall-analytics-content` module after dependent consumers are migrated.
  - Keep observation/metric implementations and evidence authority inside Tavall Analytics. Content consumes typed API views only.
  - Stage Analytics module migration independently; do not expand the current Content implementation scope into Analytics internals.

- [ ] 2026-10-02 — Promote platform staging PR #14 and CI wrapper adoption PR #7 to `main`.
  - Verify exact-source build and integration tests on `DEVELOPMENT_SHARED` Executor.
- [ ] 2026-10-02 — Complete Tavall AI browser DI integration (PR #15).
  - Validate session analytics extraction through DI-injected browser capabilities.

### `TavallStudios/tavall-cache`

#### System — Tavall Cache

- [ ] 2026-10-22 — Classify the current `abstract-cache-system` contract module and `abstract-cache-semantic` owner before applying suffixes.  ([canonical issue](https://github.com/TavallStudios/tavall-cache/issues/16))
  - Existing `abstract-cache-system` is documented as a non-runtime LIBRARY/API-style foundational contract, not automatically a primary SYSTEM because of its name. Confirm API classification and plan a compatibility-safe `tavall-cache-api` coordinate only if that reduces misleading naming. If semantic routing truly has SYSTEM fan-in, migrate it to a compliant name such as `tavall-cache-semantic-system` with a real consumer and profile tests; otherwise leave it a library.
  - Storage backends remain secondary PROVIDER/ADAPTER roles until independent FEATURE lifecycle is proven. Integrate existing per-module CI TODOs; do not create a standalone cache runtime.


- [ ] 2026-10-02 — Promote PR #11 (retaining immutable cache artifacts) to `main`.
  - Validate exact-source composite execution across all eight cache modules.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for each of the eight cache modules.
  - Verify that Tavall CI aggregates module definitions without relying on repository-root-only discovery.

### `TavallStudios/tavall-ci`

#### System — Tavall CI

- [ ] 2026-10-10 — Integrate source-owned language modules as selectable immutable CI toolchains, starting with `TavallStudios/tavall-jdk/tavall-jdk-25`.
  - Extend the existing typed CI/Cloud boundary for toolchain artifact name/version/platform/exact source SHA and SHA-256; do not invent another registry or source materialization mechanism.
  - Cloud installs/selects the immutable JDK archive for an Executor, and Gradle/application checks use that explicit toolchain rather than silently choosing the host Java runtime.
  - Test consumer builds with exact pinned source and artifact identities, reject mismatched digests/platforms, confirm no OpenJDK native rebuild during ordinary app checks.
- [ ] 2026-10-10 — Extend `tavall-ci-cd` artifact promotion with non-service toolchain delivery semantics.
  - Reuse the existing artifact/evidence/promotion contracts and Cloud-owned tool provisioning; do not create a fake service deployment for Java.
  - Prove a built toolchain is promoted byte-for-byte, safely installed, selected and rolled back without mutating all application builds.

- [ ] 2026-10-02 — Enforce canonical internal snapshot versioning and channel rules under `VERSIONING.md`.
  - Fix artifact metadata production in `tavall-ci-versioning` to emit valid `<version>-SNAPSHOT` with channel metadata (`SNAPSHOT`, `RELEASE`, `DEV`).
  - Evidence: rerun exact staging head on `DEVELOPMENT_SHARED` and verify artifact version/channel validation passes.
- [ ] 2026-10-02 — Enforce provider-neutral `ACCEPTED_MAIN` gate in `PromotionService` before Production A/B promotion.
  - Require explicit main merge verification and human approval record before generating production deployment manifests.

#### Module — tavall-ci-definition

- [ ] 2026-10-02 — Implement module-local `.tavallci/ci.yaml` discovery and multi-module aggregation in `tavall-ci-definition`.
  - Discover each module's local `.tavallci/ci.yaml`, validate schema, and compose them into the aggregate execution plan.
  - Blocks: multi-module validation in `tavall-cloud`, `tavall-cache`, `tavall-database`, `tavall-discord`, and `tavall-test-suite-tools`.

#### Module — tavall-ci-cloud

- [ ] 2026-10-08 — Complete exact-source invocation validation through Tavall CI's canonical caller and Cloud's shared Executor.
  - Tavall CI owns source aggregation, frozen checks, and the unified Gradle plan; Cloud owns execution, operation isolation, caches, and evidence storage. Do not add a second Cloud Gradle planner.
  - Capture typed evidence for Web PR #63 request `e1f9379e-0f9d-4e7e-94eb-f67dfc025afd`, then submit Tavall-MC #333's current exact head when the shared Executor is free.
  - Use the repository-owned `scripts/ci/run` / `tavall-ci-cloud` caller path; absence of `tavall ci` from the installed Cloud CLI is not a reason to run raw Gradle or create a GitHub App dependency.

#### Module — tavall-ci-cd

- [ ] 2026-10-02 — Enforce strict artifact reference and digest binding in delivery bundle materialization.
  - Verify that `tavall-ci-cd` rejects mismatched `storageRef` and artifact digests before delivery.

### `TavallStudios/tavall-cli`

#### System — Tavall CLI organization migration

- [ ] 2026-10-24 — Complete and validate the source-backed CLI migration matrix under the existing `tavall-cli` owner PR #4.
  - Matrix includes Cloud, CI, Open Harness, AI legacy sources, Minecraft/Novus game commands and embedded server console, Hytale sim/control console, `TAL`, build/test mains, infrastructure tools, and the planned-but-absent `tavall module` / `tavall-cd-cli` rows. It records each current owner, source revision/path, target owner/dependencies, status, and priority. The current matrix is in the Draft [`tavall-cli` PR #4](https://github.com/TavallStudios/tavall-cli/pull/4); its CLI code/config source commit is `3dc58ae0354c78a36a37ce4596292e639f7e5908`.
  - CLI #4, Open Harness #2 source/config `033013b8`, and CI #38 source/config `39ce1cf5` select TST `patterns+cli` and bind the CLI rule artifact to exact TST source `:modules:cli`; exact owner/consumer TCI remains pending while Web PR #84 uses the shared Executor.
  - Cloud #469's tested production source `29154920` remains main-based; its exact `all` run failed at the pre-existing architecture finding before behavior. The targeted `behavior` profile is pending. Cloud #114 root CLI-rule config source `e207e875` also contains unrelated Browser feature work and remains Draft; do not merge it as a CLI-only change. Cloud #186 is a separate Browser video child and remains unchanged.
  - Do not claim a unified installed distribution until approved package composition loads the Cloud, CI, and Harness providers. Keep in-game Paper/Velocity handlers, the TypeScript `hytale-sim` CLI, and build/test entrypoints with their owning runtime/tool.

#### Canonical CLI contract reconciliation

- [ ] 2026-10-24 — Keep the shared CLI architecture examples aligned with current `tavall-cli` source: `ICLICommand.execute(CLICommandInput)`, `CLICommandResult`, `ICLIBootstrap.registerCommands(ICLICommandRegistry)`, and `CLICommandBuilder`; track API/progression evidence in the owner documents.
- [ ] 2026-10-24 — Reconcile the Cloud CLI command reference with Cloud main parser source `40954a97208b57b04edf7fd1d3b0f94f07eab939`: 138 accepted forms/17 families, including the current 15-form `executor` family. Preserve the Cloud CONTROL/local-socket authority boundary and keep the currently pending exact-source/package evidence separate.

### `TavallStudios/tavall-cloud`

#### System — Tavall Cloud

- [ ] 2026-10-22 — Finish source-to-module classification and naming cutover for Cloud CONTROL and Node Agent without splitting the unified Cloud distribution.  ([canonical issue](https://github.com/TavallStudios/tavall-cloud/issues/460))
  - `tavall-cloud-node` currently declares primary `RUNTIME` but lacks `-runtime`: either migrate the real process owner to `tavall-cloud-node-runtime`, or explicitly split the actual Node SYSTEM from the runtime shell after dependency and host evidence. Keep `tavall-cloud-runtime` unchanged as the unified runtime/distribution owner; do not create duplicate process authority.
  - Extract the source-bearing `tavall-cloud/` **Gradle aggregate** into its true existing domain owners; create `tavall-cloud-control-system` only for validated CONTROL fan-in, never a new CONTROL process by implication. Do not rename the repository root or the aggregate folder simply to add a suffix.
  - Classify `tavall-cloud-jobs`, `tavall-networking`, Edge Director and provider modules by their verified responsibilities before any optional SYSTEM/FEATURE renames; preserve existing typed Cloud/NLEW/Database/Filesystem authority. E2E: real CONTROL/Node boot, service reconciliation, Executor placement, node reconnect, existing profiles and rollback.


- [x] 2026-10-12 — Merge Cloud PR #424's shared-Executor exact-source CI path through root PR #397.
  - PR #424 merged into `staging/runtime` at `adeb136`; root PR #397 merged to `main` at `a0788c5`. PR #397 records all seven required profiles passing on its exact root and a DEVELOPMENT Agent artifact deployed through the existing Agent-only bootstrap. No Production cutover is claimed.
- [x] 2026-10-12 — Promote the refreshed Cloud staging root PR #397 to `main`.
  - Exact-root Executor validation and the DEVELOPMENT artifact identity are recorded in PR #397. Later mainline source changes require their own current-head validation.
- [ ] 2026-10-18 — Resolve the neutral GitGuardian result associated with Cloud PR #424 history.
  - PR #424 check `114642643440` and root PR #397 check `114645986164` concluded `neutral`, not `success`. Reconcile the scanner finding/skip disposition with security evidence and rotate any affected credential as required; do not treat the merge as secret-scan clearance.
- [ ] 2026-10-02 — Complete Redis state machine recovery and lease fencing validation across all 3 nodes (`dev-storage`, `novus-ffa-east`, `novus-ffa-west`).
  - Validate disconnect replay, CAS fence contention, and node restart reconciliation.

#### Module — CONTROL

- [ ] 2026-10-02 — Register an immutable deployment strategy for the `tavall-cloud-control` service template.
  - Add `deployment.strategy` label and CD configuration under `/srv/dev-storage/templates/services/tavall-cloud-control` to allow managed Control plane updates without bypassing desired-state reconciliation.
- [ ] 2026-10-02 — Safely retire legacy loopback `tavall-cloud-chatgpt-plugin.service` listening on port 17445.
  - Reconcile base systemd ownership so the retired sandbox catalog process stops without breaking the active managed Cloud router on port 7445.
- [ ] 2026-10-02 — Enforce strict artifact reference and digest equality in the Cloud delivery materializer.
  - Reject delivery requests where `storageRef` points to a different digest than declared.
- [ ] 2026-10-02 — Correct service removal cascade in CONTROL registry projections.
  - Advance tombstones from the higher of local projection and CONTROL versions so `tavall service remove` moves service and runtime projections cleanly to `REMOVED/STOPPED`.
- [ ] 2026-10-10 — Wire new-node enrollment and approval into the durable CONTROL inventory.
  - Rechecked against Tavall Cloud main `f89207e` on 2026-10-18: `CloudDevelopmentInfrastructureInventorySeeder` still seeds only the owner plus `novus-ffa-east` and `novus-ffa-west`. The `node approve`/`node reject` parser entries still have no command handler; `CloudNodeAdmissionService` and unit tests exist but are not connected to the CLI path, and `CloudNodeInventoryCommandHandler` handles only list/inspect.
  - Implement the enrollment and approval path through durable node authority, then redeploy CONTROL and admit the installed `work-0` host after verifying its registered identity and capabilities.
- [ ] 2026-10-10 — Register the `work-0-storage` NFS export in CONTROL topology.
  - Rechecked current main: the checked-in topology examples contain no `work-0` node or `work-0-storage` export. Reconcile the previously verified read-only NFSv4.2 export into `developerTopology.networkStorage`, validate the authorized client mount, and reconcile its mount intent.

#### Module — Executor

- [ ] 2026-10-02 — Finalize transition from legacy sandbox paths to canonical `tavall-cloud-executor`.
  - Standardize source manifests on `source-roots.executor.txt` and retire residual sandbox operations.
  - Validate concurrent execution on `DEVELOPMENT_SHARED` across parallel jobs sharing `/srv/dev-storage/tavall-cache/shared-ci/gradle`.

#### Module — Node Agent

- [ ] 2026-10-02 — Enforce compile-time independence between Node Agent and CONTROL.
  - Maintain clean unidirectional dependency: CONTROL requires Node Agent at runtime only.
  - Validate Agent bootstrap installer using immutable artifact `789c2432...`.
- [ ] 2026-10-10 — Make the Node Agent installer work on a fresh Ubuntu 26.04 host.
  - Rechecked current main: `CloudAgentInstaller` still emits wildcard `systemctl start/stop/restart tavall-cloud-*.service` sudo rules and includes `/run/netns` and `/run/tavall-executor` in `ReadWritePaths` without creating those directories. Make sudo-rs-compatible rules, create the runtime paths before service start, and validate on a fresh Ubuntu 26.04 image.
  - A pre-placed `/etc/tavall-cloud/control.secret` must be `0640 root:tavall-cloud`; document or enforce that mode when joining an existing CONTROL.

#### Module — Networking (tavall-networking)

- [ ] 2026-10-02 — Validate cross-region three-node Minecraft network routing.
  - Verify nftables/IPIP tunnels, packet filters, and fail-closed rollback across `dev-storage`, `novus-ffa-east`, and `novus-ffa-west`.
- [ ] 2026-10-10 — Restore and verify the DEVELOPMENT Nebula lighthouse/relay.
  - The 2026-10-10 observation was `novus-ffa-west` lighthouse/relay (`10.91.0.2`) and peer `novus-ffa-east` (`10.91.0.3`) offline since about 2026-10-05. Current live reachability has not been rechecked in this docs update.
  - Verify the current CONTROL and endpoint state; retain a live lighthouse/relay or document and validate the approved static topology from `dev-storage` and `work-0`.

### `TavallStudios/tavall-concurrency`

#### System — Tavall Concurrency

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and promote Java Tools platform adoption to `main`.
  - Validate thread safety and lock contention tests under Java 25.

### `TavallStudios/tavall-content`

#### System — Tavall Content Opportunities

- [ ] 2026-10-10 — TODO / DEFERRED: research and integrate additional clipping-campaign aggregators into the existing Tavall Content opportunities/radar capability **after** its current provider-backed E2E and Account authorization gates pass.
  - Evaluate **ClipRadar** (existing draft adapter/reference), **Clipper Hub**, **Clipping Atlas**, **StreamClipping AI**, **ClippingDeals**, and the **Apify Clipping Campaigns Aggregator**. Treat **Clipping.work** as a platform directory for source discovery, not a confirmed live campaign feed. Record actual coverage, upstream marketplaces, freshness, costs, API/MCP/access requirements, rate limits, licensing/terms, and source reliability; do not assume reported campaign counts are unique or currently available.
  - Prefer explicitly authorized provider APIs and contract-compliant programmatic feeds (investigate Apify and Clipping Atlas first); use user-authorized browser observation only when permitted. Do not bypass credentials, payment gates, anti-bot controls, or redistribution limits. No new paid accounts, credentials, polling, scraping, or enabled adapters are authorized by this TODO.
  - Reuse the existing `tavall-content-opportunities` domain and Content source/provider abstractions instead of inventing an aggregator platform or duplicating Tavall Analytics. Normalize source-of-truth marketplace, aggregator referral, campaign identity/URL, provenance, observation time, rights/eligibility, statuses, budgets, CPM, caps, platform/payout fees, and withdrawal rails. Deduplicate listings across overlapping aggregators and native marketplaces; preserve uncertainty and stale/out-of-budget indicators.
  - Support comparable **net expected earning** and **small-account eligibility** views: follower minimum, per-clip views, cumulative campaign views, Tier 1/Tier 2 audience restrictions, withdrawal minimum, payout hold, region, verified fee schedule, and funded balance. Unknown requirements remain `UNKNOWN`, never silently treated as zero or eligible.
  - Acceptance when scheduled: typed contracts, source-specific opt-in configuration and capability checks, automated normalization/deduplication/failure tests, and authorized read-only operator E2E proving eligible/ineligible/unknown explanations, source links, and no publication or payout side effects. Keep this research/integration **deferred** until the current Content runtime/Account and provider gates are complete.

#### System — Tavall Content Auto Post

- [ ] 2026-10-10 — Implement `tavall-content-auto-post-system` as the SYSTEM module for the Content operations team, aggregating independently loadable, disableable and reloadable FEATURE modules.
  - Initial feature boundaries: `tavall-content-auto-post-discovery-feature` (research and candidate discovery), `tavall-content-auto-post-video-watch-feature` (external video observation), `tavall-content-auto-post-creative-feature` (scripts, hooks and content proposals), `tavall-content-auto-post-engagement-feature` (outbound comment and inbound reply drafts), `tavall-content-auto-post-publishing-feature` (approval-gated scheduling through the existing publishing pipeline), and `tavall-content-auto-post-reporting-feature` (analytics findings and operator briefs). Confirm names and module graph against canonical Tavall module architecture before creation.
  - SYSTEM owns composition, lifecycle and fan-in. FEATURE modules own their feature-specific contracts and behavior; reuse existing Content core, Content Studio, `tavall-content-tools`, `tavall-content-app`, Tavall DI, event routing and durable state instead of duplicating platforms, publishers or schedulers.
  - Use the **existing Tavall AI MCP integration** to discover/request centrally installed agents and tools from Tavall AI and the Function Catalog. Do not implement a parallel agent aggregator, agent installation, registry or model runtime inside `tavall-content-ai`; that module remains the existing domain-specific AI capability/adaptation boundary.
  - An MCP call is a capability boundary, not authorization: preserve campaign/account/source access checks, tool-scoped execution grants, action audit trails and failure semantics; removing a FEATURE does not erase durable work.
- [ ] 2026-10-10 — Add evidence-backed external video discovery and actual multimodal video review to the Auto Post Video Watch feature and Content dashboard.
  - Discover relevant public or explicitly authorized videos for configured topics/communities, respect platform-access policies and rate limits, and record platform/video identities, creators, links, timestamps, source rights and collection provenance.
  - When authorized video playback/media access is available, analyze sampled frames/scenes, audio, speech/transcripts and surrounding context instead of pretending a title, caption or thumbnail represents watching the video; explicitly mark partial/unsupported observations and do not invent observed scenes.
  - Surface observed videos as dashboard cards with playable links/previews where permitted, reason for relevance, cited evidence, proposed engagement opportunity, target account and audit status. Never manufacture views, likes, watch time or platform engagement.
- [ ] 2026-10-10 — Add a unified human approval queue for *outbound comments on other creators' videos* and *inbound replies*.
  - For each authorized account and target post/comment, generate distinct context-specific draft comments/replies informed by actual observed evidence; include account identity, target link, intended purpose, provenance and compliance checks.
  - Human can APPROVE, EDIT, REJECT or SKIP; edits create a new version and invalidate prior approval. Only the exact approved snapshot may dispatch through a permitted platform integration, with idempotency, expiry/revalidation, throttling and observable delivery status.
  - Keep unsolicited engagement genuine and relevant: no automated bulk commenting, repetitive generic messages, deceptive impersonation, artificial view-generation, unsolicited DM spam, or circumvention of platform limits. Dashboard review alone must never post.
  - Acceptance: authorized external video -> real observed evidence -> suggested outbound comment -> human approval -> optional permitted send -> audited result, plus inbound reply equivalent; rejected/stale/unauthorized/unsupported cases must fail closed.
- [ ] 2026-10-12 — Implement approval-gated post-publication campaign actions in `tavall-content-auto-post-engagement-feature` and `tavall-content-auto-post-publishing-feature`, reusing the existing Tavall Content campaign, account, publication, audit and approval contracts.
  - Ingest the actual Clipster campaign brief and link each approved clip/platform/account to its publishing record and direct post URL. Prefer a supported first-party Clipster API/SDK for campaign rules, submission and status; fall back to the canonical Tavall AI cloud-browser capability for explicitly authorized browser steps when no supported API exists. Do not reverse-engineer private endpoints or claim unsupported automation as available.
  - For each campaign, distinguish optional suggested first comments, mandatory first comments, pins and requested creator-comment likes. Draft/version each comment with evidence, and only publish or like a creator-owned comment after approval and when the platform/provider supports the action. Never use engagement automation to manipulate metrics or evade platform policy; unsupported and prohibited actions stay as a human checklist.
  - After publishing, resolve and verify the platform's real post URL, submit eligible URLs to Clipster within the campaign-specific submission window (24 hours where required), and capture submission receipts, campaign identity, source account, timestamps, external state, errors and retries without double-submission.
  - Present operator checklist and reconciliation status per post/platform: PUBLISHED, COMMENT_PENDING/POSTED/UNSUPPORTED, LIKE_REQUIRED/DONE/MANUAL, CAMPAIGN_SUBMITTED/ACCEPTED/REJECTED. Missing permissions, stale campaign terms, failed content checks, expired windows or missing URLs fail closed and surface corrective steps.
  - Follow the `Tavall AI` skill and read canonical `tavall-docs` before implementation; use Tavall agent ledger, existing MCP/tool governance, typed API-first contracts, event routing and idempotent persistence. Acceptance: approved clip -> verified publish -> first comment -> optional platform-permitted creator like -> Clipster submission/status, with verified manual fallbacks for unsupported API/browser actions and complete E2E audit evidence.
- [ ] 2026-10-10 — Validate a complete Auto Post System workflow across enabled FEATURE modules and existing Content Studio.
  - Research -> evidence-backed candidate -> script/clip draft -> existing native render and metadata compliance checks -> human approval -> supported account publishing/scheduling -> `tavall-analytics-api` evidence/findings -> operator morning briefing and exception alerts.
  - Verify independent FEATURE enable/disable/reload, MCP failure and revocation handling, cross-account authorization, durable retries, persistence, exact-head architecture/unit/integration tests and real browser E2E without claiming unsupported provider-backed behavior.

#### System — Tavall Content Studio

- [ ] 2026-10-22 — Rename the verified headless `tavall-content-render-worker` RUNTIME module to a suffix-compliant identity such as `tavall-content-render-worker-runtime`, without moving the Tavall Content repository.  ([canonical issue](https://github.com/TavallStudios/tavall-content/issues/72))
  - Preserve `tavall-content-runtime` (already compliant), `tavall-content-app` and the existing `tavall-content-auto-post-system`/`tavall-content-auto-account-system` FEATURE graphs. Rename Gradle artifact, immutable worker distribution, Tavall CD template/service selector, CLI/CI references, persisted job/lease identity and documentation only through an audited compatibility plan.
  - Acceptance: exact-source producer and Studio consumer tests, real DB job claim/recovery/cancel/resume, worker replacement and rollback, no duplicate lease ownership or published state loss.


- [ ] 2026-10-09 — TODO / DEFERRED: integrate future Tavall Commerce offers, product references, campaign CTAs and transaction attribution after the Tavall Content end-to-end loop passes acceptance.
  - No Tavall Commerce runtime, data model, checkout or payment work is in the present scope. Reuse future Commerce-owned typed APIs; preserve Analytics ownership of measurement and attribution.

- [ ] 2026-10-09 — Add a human-reviewed publishing metadata and campaign compliance gate to Tavall Content.
  - For each approved render and selected channel, produce editable/versioned post metadata: title, description or caption, hashtags, creator credits, required `@mentions` and account tags, platform-specific links/affiliate link, and intended CTA. Record AI suggestions separately from human edits with source and approval provenance.
  - Parse/refer to the campaign's actual approved guidelines as requirements, attach source references and check results (e.g. whole-home opening, exact on-screen/caption spelling, allowed source, creator identity, mandatory tagging, prohibited topics). Differentiate campaign requirements from separate legal or platform disclosure judgments; show unsupported/ambiguous obligations for human decision, never infer legal clearance from a campaign brief.
  - Persist a per-clip/per-platform review record and immutable metadata snapshot with explicit `APPROVE`, `REVISE` or `REJECT` decisions, reviewer, timestamp, rule evidence and optional rationale. A post must not be queued or dispatched without current explicit approval; changed metadata, edited render, changed guidelines or revoked source authorization invalidate the affected approval and require re-review.
  - Reuse Tavall Content's existing artifact, approval, authorization and optional publishing contracts. The Studio does not create a second publishing subsystem; no auto-posting is authorized by this TODO.
  - Acceptance: typed API/client contracts, persistence, positive/negative contract tests and real browser E2E for TikTok, Instagram Reels and YouTube Shorts; test X affiliate-link rules only when X is selected. Use the BOXABL campaign as a representative test fixture without hardcoding its rules into the generic platform.

- [ ] 2026-10-02 — Implement asynchronous render queue with job tracking and progress notifications for Content Studio.
  - Move timeline renders and cutaway processing out of the synchronous HTTP request thread.
  - Provide durable job status endpoints (`QUEUED`, `RENDERING`, `COMPLETED`, `FAILED`) and cancellation support.
- [ ] 2026-10-02 — Implement cutaway audio blending and audio channel selection in timeline renderer.
  - Support mixing cutaway audio with primary timeline audio or replacing primary audio during cutaways.
- [ ] 2026-10-02 — Implement production Google Drive asset importer and authorized AI model provider adapters.
  - Replace test doubles with credential-managed production implementations.
- [ ] 2026-10-02 — Implement beat-synchronized timeline placement engine based on audio waveform analysis.
  - Translate visual beat annotations into sample-accurate frame cut points.
- [ ] 2026-10-12 — Implement campaign-specific TikTok Audio Lock as a first-class Content Studio edit-to-publish flow, following [the technical design](https://github.com/TavallStudios/tavall-content/blob/main/docs/technical/TIKTOK_AUDIO_LOCK.md).
  - One non-destructive timeline: resolve official campaign sound ID/URL, account/region availability and requirements from actual approved campaign evidence; acquire an authorized **exact-version** timing reference or mark lock unverified. Record fingerprint/version, sample offset, playback speed, tempo landmarks, confidence and drift. A generic same-title song must not count as the matched reference.
  - Extend existing `MUSIC_SYNC` / `VISUAL_BEAT` annotations and the deferred beat placement engine: correlate legitimate audio references where available, store integer-sample timing, quantize output cuts to the output frame grid, account for encoder padding and selected TikTok segment start. Target <= one frame *offline* measured residual for validated reference/offset; do not promise native playback precision without evidence.
  - Reuse existing Content Studio, `tavall-content-tools`, `tavall-ffmpeg`, campaign/publishing approvals, `tavall-content-client`, and `tavall-web-content`. Add versioned audio stem policy: a licensed full mix for eligible destinations, and dialogue/SFX-only TikTok export where an official native sound must be selected. Warn about music-dependent edits that cannot survive native sound replacement.
  - Present the exact sound/offset, alignment confidence, export preview and supported native attachment **or manual TikTok handoff** in the existing Clip Editor. Never invent a TikTok sound-ID posting parameter or private API; unsupported capabilities fail closed until explicit human in-app selection and sync preview verification.
  - Persist manifest, timing map, revisioned handoff record, audit and verification; invalidate approval when source/version, campaign rule, sound, timing, render, account/region, or export changes. Require campaign/media rights and source authorization; avoid uncontrolled music caching.
  - Acceptance: real test media with 0/100/250-ms offsets, alternate intros, drift, 30/60-fps rounding, encoder delay, stem separation; negative authorization/unsupported-provider paths; browser and campaign publishing E2E with verified manual fallback. Follow `Tavall AI` skill, canonical `tavall-docs`, Tavall agent ledger, repo architecture, typed API-first contracts, event routing and appropriate exact-source validation.
- [ ] 2026-10-02 — Reconcile persistent product staging root PR #7 against `main` following PR #23 promotion.

### `TavallStudios/tavall-content-tools`

#### System — Tavall Content Tools

- [ ] 2026-10-02 — Validate headless FFmpeg and OpenCV native bindings on Linux Cloud Executor.
  - Ensure deterministic video segment extraction and filter pipeline execution without display server dependencies.

### `TavallStudios/tavall-custom-enum-java`

#### System — Custom Enum Java

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate reflection-free enum expansion under Java 25.

### `TavallStudios/tavall-database`

#### System — Tavall Database

- [ ] 2026-10-22 — Reconcile Database's legacy primary provider/library classifications against canonical module types before any `-system` migration.  ([canonical issue](https://github.com/TavallStudios/tavall-database/issues/31))
  - Keep `tavall-database-core-contracts`, `tavall-database-redis-api`, existing provider implementations and their tested contract boundaries. Add `-system` only to a verified domain fan-in SYSTEM; no suffix requirement for plain API, selected provider, consumer aggregate or repository root. Validate live PostgreSQL/Redis consumers, ServiceLoader, pool/lease cleanup, and exact-source compatibility.


- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for all database modules.
  - Validate Flyway migration sequencing, connection pool sizing, and transaction boundaries under PostgreSQL 14/16.
- [ ] 2026-10-02 — Promote consumer access guide (PR #27) and multi-node read replica contracts to `main`.

### `TavallStudios/tavall-di`

#### System — Tavall DI

- [ ] 2026-10-02 — Promote staging PR #13 to `main` with verified Java 25 / Gradle 9.6.1 build.
  - Verify compile-time bytecode enhancement and runtime resolution across all consumer modules.

### `TavallStudios/tavall-discord`

#### System — Tavall Discord

- [ ] 2026-10-22 — Resolve Discord's in-process lifecycle module primary type and apply suffix naming only after classification.  ([canonical issue](https://github.com/TavallStudios/tavall-discord/issues/10))
  - The existing `tavall-discord-runtime` suffix is syntactically compliant but its README says it is **not independently executable**; if classified as SYSTEM, migrate to a semantically accurate `tavall-discord-lifecycle-system` rather than falsely declaring RUNTIME. If `tavall-discord-data` becomes a SYSTEM, likewise use `tavall-discord-data-system`; otherwise retain its appropriate API/library identity.
  - Keep `tavall-discord-api`, JDA and Minecraft integration interfaces separate; consumer products own Discord behavior. E2E: actual host startup, feature registration/disable/teardown and client shutdown without a second Discord daemon.


- [ ] 2026-10-08 — Finish reusable Discord producer PR #9 and publish its generic runtime/API artifacts.
  - Current head is `ca83559`; generic client/JDA lifecycle, immutable gateway contracts, ordered dispatch, and process-host ownership remain here.
  - Recorded local producer tests pass; wrapper-backed Tavall CI, internal package resolution, and external host boot remain open. Do not move Tavall-MC product policy or persistence into this repository.

### `TavallStudios/tavall-docs`

#### System — Tavall Documentation

- [ ] 2026-10-29 — Implement and validate the **Agent WebMCP SVG visual standard** for Tavall technical diagrams.
  - **Style selected and documented:** [Tavall Technical Diagram Standards](docs/quality/DIAGRAM_STANDARDS.md) now adopts SVG styling from [Agent WebMCP source diagrams](https://github.com/tjXJNOOBIE/agent-webmcp/tree/main/docs/hackathon/devpost); reject the three earlier generic draft designs as the default. Distinct topologies remain valid under one graphic language.
  - Build reusable editable SVG layout/style helpers with accessible labels, and a truthful visual verification workflow for clipping, arrow endpoints, readable Notion widths and printable/light fallback. Keep source facts with their original architecture owners, not in a graph-specific second database.
  - Redraw the [Class Role Ownership Graph](docs/quality/code-architecture/CLASSES.md#class-role-ownership-graph-conceptual) with WebMCP styling while preserving verified responsibilities, then test actual Notion and GitHub rendering. Preserve module-README current-module highlighting and "← This Module" requirements.
  - Publish/sync Notion render and canonical SVG source together only for documents requiring or requesting a Notion counterpart. Record actual synchronization receipts; the style's documentation merge is not evidence of a completed Notion rollout.

- [ ] 2026-10-29 — **Simplify Tavall Docs to local document retrieval**, replacing generated per-section skill proliferation while retaining the existing Docs Agent and canonical GitHub/Notion authorities.
  - **Explicit architecture decision:** no new Java system, service, daemon, hosted Docs API, database authority, or standalone "Knowledge Plane" platform. Reuse installed `rg`, `python3`, the existing `hooks/policy.py`, `agents/tavall-docs-agent/tools/doc-sections/sections.py`, and canonical `DOCUMENT_ROUTING.yml`. The installed host already supports Python `sqlite3` FTS5; only introduce a derived FTS index if plain text search proves insufficient.
  - Keep one concise procedural Docs skill (plus actual workflow skills when independently justified). Replace generated per-heading `SKILL.md` wrappers with a **derived, non-authoritative section manifest**, initially created or read on demand by the current Python section parser. No duplicate documentation text or independent policy database.
  - Route from task/file/module context → targeted `rg`/declared route candidate discovery → exact document heading read → document/section SHA and source-revision receipt. Fail closed for missing/ambiguous policy authority; optional local semantic search can suggest candidates but never decide policy authority.
  - First fix the current stale `section-index.json` against an **exact current, clean Docs checkout**; review drift and test real section reads without guessing heading renames. Compare the minimal lookup path with existing skills for context volume, correctness, latency and change tolerance before retiring generated wrappers.
  - Keep Notion/GitHub reconciliation and [Agent WebMCP SVG diagrams](docs/quality/DIAGRAM_STANDARDS.md) as **optional bounded workflows using existing tools**; no mandatory renderer service or new runtime. The old section skill flow stays available until the local path is verified and all provider entrypoints are updated.
  - Explore existing local Markdown tools such as [QMD](https://github.com/tobi/qmd) **only if needed** for relevance or scale; it is not currently installed on Tavall Cloud and must not be introduced by default or treated as an authority source.

- [ ] 2026-10-22 — Enforce the canonical `-system` / `-runtime` suffix rule for **actual** modules, excluding parent repositories, organizational aggregates, APPLICATIONs and secondary-role labels.  ([canonical issue](https://github.com/TavallStudios/tavall-docs/issues/78))
  - Apply [Module Types](docs/quality/MODULE_TYPES.md#module-name-suffix-contract-2026-10-22) and [Module Separation](docs/quality/code-architecture/MODULE_SEPARATION.md#module-identity-naming-during-separation); classify from source before proposing each migration. A `System —` TODO heading or the word `runtime` in a folder is not proof of primary type.
  - Coordinate per-repository rollout through this ledger; require exact-source consumer imports/Gradle coordinates, module IDs/descriptors, DI and registry wiring, `.tavallci`/CD references, per-module Progression, rollback and owning host acceptance. Repository-local TODOs are bot projections, not separately edited work queues.
  - After the canonical docs revision merges, regenerate the Tavall Docs Agent exact-section index/skill metadata against the new `tavall-docs/main` SHA; validate its native drift checker before declaring remote skills synchronized.


- [ ] 2026-10-08 — Define a safe migration path for legacy untyped `.tavallai` roots before provenance updates resume.
  - The current provenance writer requires a schema-valid `schemaVersion`, `directoryType: PROVENANCE`, and typed scope. Existing V1 roots with only `version` and `scope.type` are read-only under the current fail-closed contract.
  - Document an explicit owner-approved migration procedure; do not infer or reclassify directory type from the path. Validate the result against `docs/schemas/tavallai-directory.schema.json` before starting lifecycle writes.
- [ ] 2026-10-10 — Create dedicated source-editable repositories for other programming languages, patterned after `tavall-jdk`.
  - Evaluate versioned compiler/runtime modules for Kotlin, C#, Python and C/C++ first; confirm ownership and repo names before creating each repository.
  - Each repo should own full Git-tracked upstream source in versioned language modules, preserve official update ancestry and licenses, and expose exact-source native build verification and immutable toolchain artifacts through Tavall CI/CD.
  - Keep languages independently owned; do not collapse them into one source monorepo or misrepresent lightweight wrappers as patched compilers.
- [ ] 2026-10-01 — Keep the global TODO repository inventory synchronized as TavallStudios repositories are created, renamed, archived, or retired.
- [ ] 2026-10-02 — Maintain documentation routing index (`docs/quality/DOCUMENT_ROUTING.yml`) with exact whole-term matching for all new architecture documents.
  - Prevent routing degradation and eliminate fuzzy search fallbacks.
- [ ] 2026-10-02 — Ensure 100% DESIGN, Technical, and PROGRESSION coverage for all active modules across TavallStudios without recursive directory preloading.
- [ ] 2026-10-02 — Reconcile and promote `staging/quality` root PR #34 to `main` with exact-head validation evidence.

### `TavallStudios/tavall-docs-private`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-eventbus`

#### System — Tavall EventBus

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate high-throughput typed event dispatching on Java 25.

### `TavallStudios/tavall-github-bot`

#### System — Tavall GitHub Bot

- [ ] 2026-10-21 — Automatically finalize one-shot GitHub operation issues after a verified terminal execution outcome.
  - Implement in the existing `tavall-github-bot` GitHub adapter, not a new GitHub Actions workflow or Cloud CI scheduler; preserve Tavall Cloud and Function Catalog operation authority.
  - Require an explicit one-shot marker/allowlisted issue type, immutable operation identity, trusted bot evidence and a final SUCCESS/FAILED/REJECTED/CANCELLED result before making a closure decision. Do not close on inactivity or mere dispatch acknowledgment.
  - Publish a sanitized terminal summary and preserve links to immutable execution evidence; close successful requests as completed and terminal unsuccessful attempts as not planned, with retry work tracked separately as needed.
  - Keep durable command channels, ongoing work trackers, security approvals, active retries and ambiguous statuses open. Respect human/repository ownership and least-privilege GitHub App permissions.
  - Make retries/idempotency safe: no duplicate comments, no double-close, no closure of newer operation generations. Add provider/API and integration tests, verify exact-source CI, then merge and deploy through the existing Tavall workflow.
  - Reconcile historical one-shot operation tickets only with their individually verified outcome; do not mass-close engineering issues by age.
- [ ] 2026-10-01 — Implement canonical repository TODO projection management.
  - Watch `TavallStudios/tavall-docs/TODO.md` and repository inventory changes.
  - Parse each repository's section and render it as the first substantive section of that repository's root `TODO.md`.
  - Preserve canonical generated HTML metadata comments including source, repository, managing bot, projection format version, source commit, and synchronization timestamp.
  - Open or update one deterministic synchronization PR targeting `main` per affected repository instead of creating duplicate PRs.
  - Reconcile repository creation, rename, archive, and reactivation events.
  - Never treat a local generated projection as authority or ingest local edits back into the global TODO automatically.
  - Validate that the rendered repository slice exactly matches the authoritative global section before marking synchronization complete.
- [ ] 2026-10-02 — Deploy persistent `tavall-github-bot` service identity with least-privilege CLI invocation permissions.
  - Resolve sudo boundary limitation for `tavall-cloud-github-bot` service account so it can execute authorized Tavall CLI commands.
- [ ] 2026-10-02 — Transition GitHub event ingress from manual/polled execution to persistent webhook delivery.
  - Validate signature verification, idempotency deduplication, and Check projection across high-concurrency PR events.

### `TavallStudios/tavall-hytale-resource-game`

#### Companion System Future Work

- [ ] 2026-10-01 — Add custom companion skins and cosmetic rarity rules.
- [ ] 2026-10-01 — Add full companion duel animations and richer cast particles.
- [ ] 2026-10-01 — Add advanced morale event chains, bonding, voice, and emote hooks.
- [ ] 2026-10-01 — Add battle replay companion commentary.
- [ ] 2026-10-01 — Add full wall section visuals for assigned companions.
- [ ] 2026-10-01 — Expand companion injury and recovery depth beyond first-pass status fields.
- [ ] 2026-10-01 — Add companion behavior hooks driven by the canonical Kingdom Clock.
- [ ] 2026-10-01 — Add companion and citizen/job interaction hooks.
- [ ] 2026-10-01 — Add companion quests, party training, and realm-specific skills.

### `TavallStudios/tavall-java-tools`

#### System — Tavall Java Tools

- [ ] 2026-10-02 — Promote PR #3 (canonical gitlinks and central Git workflow routing) to `main`.
  - Ensure standalone builds across all 9 Java Tools platform repositories resolve dependencies without monorepo coupling.

### `TavallStudios/tavall-java-utils`

#### System — Tavall Java Utils

- [ ] 2026-10-02 — Promote central workflow and documentation updates to `main`.

### `TavallStudios/tavall-jdk`

#### System — Tavall JDK

- [ ] 2026-10-10 — Import the complete OpenJDK 25 baseline into the tracked `tavall-jdk-25/openjdk/` module through the pinned Git subtree import; currently blocked by unavailable upstream Git transfer in the connected execution session.
  - Confirm the exact official tag and commit, legal notices, large-object and total Git repository sizes. Import in a working branch, review source, and preserve normal Git history and upstream identity.
  - No builds or CD releases may claim success until the full source is committed and verified on an exact source SHA.
- [ ] 2026-10-10 — Run `tavall-jdk-25` exact-source CI end-to-end with a native toolchain, JDK 24 bootstrap and canonical Gradle 9.6.1 wrapper.
  - Validate Java 25 images, upstream tier-1 tests, Tavall compatibility, platform packaging and immutable artifact/source digest evidence.
- [ ] 2026-10-10 — Update to an appropriately maintained OpenJDK 25u security source baseline before shipping a custom runtime.
  - Use official upstream Git subtree updates in the same versioned module; run compiler/HotSpot/runtime compatibility and security regression checks.

### `TavallStudios/tavall-logging`

#### System — Tavall Logging

- [ ] 2026-10-02 — Promote consumer access guide (PR #11) to `main`.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate structured JSON log formatting under high-concurrency workloads.

### `TavallStudios/tavall-mc`

#### System — Tavall MC / Project Novus

- [ ] 2026-10-29 — Migrate the legacy `*Manager` classes in the account-link backend to actual Tavall class roles, after ownership/consumer review.
  - Follow the [canonical Manager anti-pattern gate](docs/quality/code-architecture/CLASSES.md#the-manager-anti-pattern), [Handlers](docs/quality/code-architecture/HANDLERS.md), [Interfaces/DI](docs/quality/code-architecture/INTERFACES_AND_ABSTRACTIONS.md) and the existing production migration TODO. Do not auto-replace `Manager` with `Service` or break runtime DI.
  - [`AccountLinkAdminManager`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-backend/src/main/java/org/tavall/api/minecraft/backend/account/AccountLinkAdminManager.java): already delegates to three `I*AdminHandler` roles; remove redundant forwarding if no meaningful aggregate operation remains, otherwise preserve its established `IAccountLinkAdminHandler` contract.
  - [`AccountLinkManager`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-backend/src/main/java/org/tavall/api/minecraft/backend/account/AccountLinkManager.java): largest risk, with player link completion/fallback, token inspection, audit and provider mutations; review security, idempotency, replay/audit behavior and existing `IPlayerAccountLinkHandler` before extracting or renaming.
  - [`AccountLinkSessionManager`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-backend/src/main/java/org/tavall/api/minecraft/backend/account/AccountLinkSessionManager.java): evaluate `AccountLinkSessionHandler`, preserving session state, token expiry and consumer DI.
  - [`CreatorAccountManager`](https://github.com/TavallStudios/tavall-mc/blob/main/novus-backend/src/main/java/org/tavall/api/minecraft/backend/account/CreatorAccountManager.java): evaluate `CreatorAccountLinkHandler`; inspect `creatorStatus` read-side upsert separately rather than silently preserving or changing it.
  - Check current worktree/PR ancestry and tests before implementation; preserve already accepted changes and verify caller imports, interfaces, DI tokens, persisted identities and runtime lifecycle. No mass rename or parallel layer.

- [ ] 2026-10-29 — **Incrementally migrate existing Tavall MC Java implementations to the approved class-role and DI patterns**; preserve behavior and validate exact-source caller contracts.
  - Source of truth: [Tavall Class Roles](docs/quality/code-architecture/CLASSES.md), [Interfaces and Abstractions](docs/quality/code-architecture/INTERFACES_AND_ABSTRACTIONS.md), [Utilities](docs/quality/code-architecture/UTILITIES.md), [Enums](docs/quality/code-architecture/ENUMS.md), [Dependency Injection](docs/quality/code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md), and [Handler guidance](docs/quality/code-architecture/HANDLERS.md). Proposed additions under [Tavall Docs PR #89](https://github.com/TavallStudios/tavall-docs/pull/89) must be promoted/accepted before being treated as binding production migration requirements.
  - [Production AchievementPointTitleResolver](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointTitleResolver.java): evaluate and migrate to `AchievementPointTitleViewer`, updating its interface, [AchievementPointSummaryHandler](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java), all consumers/tests and DI boundaries together. Preserve title calculation; do not retain a redundant compatibility Resolver.
  - [Production FFARoundOrchestrator](https://github.com/TavallStudios/tavall-mc/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/round/orchestrator/FFARoundOrchestrator.java): evaluate a genuine long-lived `FFARoundService` replacing the old owner rather than adding a new layer. Preserve scheduling, thread ownership, rollback and progression, and migrate runtime bindings/tests.
  - [Production PlayerAchievementDataHandler](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/data/handler/PlayerAchievementDataHandler.java) and [AchievementPointSummaryHandler](https://github.com/TavallStudios/tavall-mc/blob/main/novus-achievements/src/main/java/org/tavall/minecraft/achievement/points/AchievementPointSummaryHandler.java): audit constructor-captured managed collaborators against current `DependencyAccess` / `@DelegatesTo`, including bare concrete-only registration when an interface has no meaningful behavioral contract.
  - Utility families: review production Paper/Bukkit utilities independently using the [historical composable IInventoryUtils example](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/main/java/dev/tjxjnoobie/ctf/util/bukkit/interfaces/IInventoryUtils.java) and [current Tavall Utility pattern](docs/quality/code-architecture/UTILITIES.md#default-utility-pattern-interface-composition). Prefer useful interface `default` methods with concrete overrides, never force unsafe null/no-op or obsolete static DI lookup.
  - [FFAKitSessionRegistry](https://github.com/TavallStudios/tavall-mc/blob/main/novus-ffa/src/main/java/org/tavall/minecraft/ffa/kit/registry/FFAKitSessionRegistry.java): separately revisit typed kit identity and consumer access once the [Tavall Registry Access Styles](https://github.com/TavallStudios/tavall-registry/blob/main/docs/REGISTRY_ACCESS_STYLES.md) design is finalized; preserve existing `put` replacement semantics and tests.
  - [FarmProductionService](https://github.com/TavallStudios/tavall-mc/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/backend/kingdom/building/FarmProductionService.java), [QuarryProductionService](https://github.com/TavallStudios/tavall-mc/blob/main/minecraft-kingdom-server/src/main/java/org/tavall/backend/kingdom/building/QuarryProductionService.java), and [DiscordOutboxService](https://github.com/TavallStudios/tavall-mc/blob/main/novus-discord/novus-discord-core/src/main/java/org/tavall/discord/core/outbox/DiscordOutboxService.java): reevaluate unwarranted Service wrappers and database-mechanics leakage before any rename or migration; leave Tavall Database ownership intact.
  - Do **not** mass rename classes or add a new `CustomEnum` API. Prefer the current `ThreadType.register(name)` example where applicable. Retain uppercase acronyms (`FFARoundService`, `playerUUID`), expanded braces, and meaningful JavaDoc. Require focused unit/integration tests and actual module lifecycle verification before rollout.

- [ ] 2026-10-22 — Audit actual primary types before applying suffix naming to Novus product modules and future gameplay SYSTEM extractions.  ([canonical issue](https://github.com/TavallStudios/tavall-mc/issues/360))
  - `novus-runtime` already complies. `novus-ffa`, `novus-lobby`, `novus-essentials`, and `minecraft-kingdom-server` currently declare `APPLICATION`: do **not** rename them based solely on being runtime-loaded gameplay. Reclassify to SYSTEM and suffix only when validated fan-in responsibilities warrant it; API, LIBRARY, and product adapter modules remain type-correct.
  - **Confirmed additional mismatch:** `tavall-mc-world` is explicitly classified as primary `SYSTEM` in both its module README and `docs/progression/modules/TAVALL_MC_WORLD_PROGRESSION.md`, but the actual module lacks `-system`. Plan the target `tavall-mc-world-system` with a compatibility mapping for module IDs, Gradle coordinates, embedded descriptors, Paper host references, world data, `/world` behavior, and existing validation; avoid duplicating World SYSTEM state.
  - Future independently composed PvP, Kingdom, and security SYSTEMs must end in `-system`, retaining their Paper/Velocity host and the single first-party `application.jar`. Fix Kingdom module-scoped DI and reconstructibility before asserting live reload; update descriptors/profile IDs, Gradle, artifact references, CI and client tests in an exact-root branch without altering stale PR ancestry blindly.


- [ ] 2026-10-18 — Reconcile current-main separation PR #333 before promoting the Minecraft PR stack.
  - PR #333 remains open Draft at head `d0edf7f`, based on `main@fd2abaa`; current Tavall-MC main is `218e46f`. Merge current main into the existing root branch, resolve overlaps using the accepted ownership split, and rerun exact-head validation before promotion.
  - The root is a documentation-led follow-up to implementation source `52210806`. It removes embedded Framework, Web, Paper-fork, generic Discord, bot-testing, Architecture Tests, Cloud-agent, and Java-ingress ownership from Tavall-MC.
  - Keep Kingdom/Novus policy, product persistence, cosmetics, and Paper/Velocity composition in MC-owned modules. Framework owns reusable Minecraft host, API, game, and NMS capabilities.
  - Remove the stale cross-game Resource Game frontend/TCP bridge copy from MC; `TavallStudios/tavall-hytale-resource-game` owns those shared contracts and its Minecraft adapter. Add no Hytale dependency unless a current MC product consumer requires the typed contract.
  - Keep runtime schema creation out of Framework and MC launch. Preserve migration intent and leave durable writes with the canonical Tavall Database owner.
  - The root and module CI manifests pin Tavall DI PR #19 source `96b4afce` and Test Suite Tools PR #22 code source `4f15f10`; no current-head Tavall CI result is recorded for PR #333 after its base fell behind main. Submit on the refreshed exact source graph.
  - Architecture findings (246 on the root code source, 230 on #337 code source `cd5060df`, and 245 on #338 code source `6b6bef8`) were last measured on older source heads. Rerun Architecture Tests on refreshed exact heads; fix source-owned contracts without suppressing rules or adding debt baselines. The historical 785-test root pass is not current acceptance.
  - Preserve #301/#299 composite and lock work, but do not merge their stale consumer lineage. Rebuild package-backed Framework consumption against the pure producer and current MC modules.
- [ ] 2026-10-18 — Reconcile the child stack after refreshing PR #333.
  - Current children #334–#338 are open Draft at heads `fc21e3b`, `49163ee`, `e1a26fe`, `d2599e0`, and `6fb0369`; all target `working/repository-separation@dbe6ba0`, which differs from PR #333 head `d0edf7f`. Reconnect children to the refreshed root while preserving each PR identity and useful deltas.
  - Preserve old roots #153, #194–#199, #204–#211, #294, and `staging/runtime-paper`/`staging/runtime-velocity` descendants as history while reclassifying each open PR and porting useful deltas onto the new product parents.
  - Paper/Velocity are the process hosts; FFA and Kingdoms are Paper product modules. Web, Cloud Agent, and public Ingress remain outside Tavall-MC.
- [ ] 2026-10-08 — Complete the Builder ownership and Web presentation boundary.
  - Keep the compiler, WorldOps, simulation, replay, WorldVision, schematic/world tools, and Minecraft worker execution in MC Builder.
  - Port/reconcile Builder Studio browser and admin presentation into Tavall Web after the typed MC Builder API and Web facade are accepted. Keep Minecraft-specific view code in `tavall-web-mc` only where its DESIGN assigns that responsibility; PR #258 remains historical and unmerged.
- [ ] 2026-10-08 — Complete the product Discord adapter cutover after producer publication and host acceptance.
  - Tavall-MC owns Novus persistence, outbox, product features, and product policy; `tavall-discord` PR #9 owns generic JDA lifecycle, gateway contracts, and runtime.
  - Keep the transitional JDA contributor only until the product feature contract has a package-backed host check. PR #284's old consumer extraction lineage is not the current owner graph.
- [ ] 2026-10-08 — Keep Cloud and ingress integration out until typed Minecraft requests have a canonical external client.
  - The current MC candidate removes the generic `/cloud` command, Cloud runtime dependency, socket, agent-secret configuration, standalone Java ingress, and result journal. Tavall Cloud owns agent/API/runtime; Networking owns ingress and dataplane.
- [ ] 2026-10-08 — Reclassify the remaining Tavall-MC PR stack after the separation root is stable.
  - Record exact parent/head, owner module, DESIGN/PROGRESSION, persistence owner, host runtime, and remaining checks for each PR. Preserve valuable stale-branch deltas and refresh their parent before implementation resumes.
- [ ] 2026-10-02 — Reconcile divergent worktree progression trackers across the 24 identified high-risk systems.
  - Consolidate branch-only progression evidence into canonical `main` documents for Runtime Module System, FFA, Effect, Moderation, Commerce, and Chat.
  - Remove prunable stale worktrees following evidence preservation.

#### Module — FFA & PvP Systems

- [ ] 2026-10-02 — Promote recovered PvP and FFA system designs and progression trackers (PRs #308–#326, #328, #330) to `main`.
  - Merge combat attribution, focused FFA translucency, rating simulation, placement reconciliation, and presentation trackers.
- [ ] 2026-10-02 — Execute live Paper lifecycle and 50-player load test acceptance for FFA.
  - Validate player respawn protection, regional routing, kill attribution, and Glicko-2 rating persistence.

#### Module — Runtime Module System

- [ ] 2026-10-02 — Eliminate transitional global backend ownership and parent-coupled singletons.
  - Implement clean lifecycle boundaries ensuring dynamic modules can unload and reload without restarting the Paper process.

#### Module — Player Identity & Store

- [ ] 2026-10-03 — Preserve the Player Identity and Crown Store design owners (PR #310) and schedule implementation under the accepted product runtime graph.
  - Verify PostgreSQL migration, entitlement caching, and in-game transaction fulfillment when the product implementation branch is created.

#### Module — Discord Integration

- [ ] 2026-10-03 — Finish the Tavall-MC Discord adapter migration under the external Tavall-Discord runtime.
  - Keep product persistence/outbox and feature policy in Tavall-MC; generic JDA lifecycle and ordered dispatch belong to tavall-discord.
  - Validate isolated-guild startup, shutdown, permissions, outbox retry, and role/support projections.

### `TavallStudios/tavall-mc-bot-testing`

#### System — Tavall MC Bot Testing

- [ ] 2026-10-08 — Finish reusable bot-testing producer PR #10 on a current parent.
  - PR #10 currently targets the older `working/repair-ffa-bot-entity-resolution` branch; preserve the scenario fixes and refresh its parent after the MC separation generation is accepted.
  - Keep the generic Mineflayer harness/platform and reusable scenarios here. Tavall-MC may own product-specific acceptance scenarios but must not copy the harness back into its reactor.
- [ ] 2026-10-08 — Run Mineflayer acceptance against the accepted Paper/Velocity product artifact.
  - Verify FFA combat loops, pathfinding, reconnect recovery, and proxy integrity; keep client/session evidence separate from source, build, and runtime evidence.

### `TavallStudios/tavall-mc-paper`

#### System — Tavall MC Paper

- [ ] 2026-10-08 — Finish Paper producer baseline PR #6 and publish a reproducible fork identity.
  - Current head is `797d8aa`; implementation code source `3fe0575` passes the recorded local full check and produces normalized Paperclip SHA-256 `a2527623…`.
  - Run wrapper-backed Tavall CI, complete package/source identity publication, and prove MC consumer resolution. Keep Paper limited to engine/fork patches; product gameplay remains in Tavall-MC.
- [ ] 2026-10-08 — Validate packet-filter hooks against the exact upstream Paper source without degrading server tick performance.
  - Keep server startup, live Paper behavior, Minecraft-client acceptance, and deployment as separate gates.

### `TavallStudios/tavall-minecraft-framework`

#### System — Minecraft Framework

- [ ] 2026-10-18 — Finish producer-purity and exact-source CI PR #11.
  - Current head is `4fa0946` (base `main@377260a`); retain reusable Minecraft UI/game/NMS and host/runtime-host APIs only. Keep Tavall-MC backend/product policy, Kingdom APIs, Novus essentials, and process topology out of Framework.
  - Publish/resolve the canonical framework artifacts and validate the MC consumer through exact-source substitution and package-backed resolution as separate paths.
  - Preserve useful work from consumer PR #301 and stale fan-in #299, but do not merge their old ancestry. PR #14 account-link admin/product resolvers are not Framework ownership.

### `TavallStudios/tavall-open-harness`

#### System — Tavall Open Harness

- [ ] 2026-10-02 — Promote Linux main harness runtime v0 (PR #2) to `main`.
  - Validate immutable harness distribution artifact emission under Java 25 / Gradle 9.6.1.
- [ ] 2026-10-02 — Implement and execute packaged daemon/CLI E2E lifecycle test suite on Linux.
  - Validate daemon background startup, Unix-socket command dispatch, PTY process attach/detach, process termination exit codes, and external-PID inspection.
  - Evidence: recorded execution transcript and zero-failure test suite.

#### Module — tavall-main-harness

- [ ] 2026-10-02 — Expand harness registry to support composition of specialized harnesses.
  - Provide typed registration for security-isolated harnesses, agent worktree runners, and coding adapters without port or socket collisions.

### `TavallStudios/tavall-rating-glicko2`

#### System — Tavall Rating Glicko-2

- [ ] 2026-10-02 — Promote immutable rating calculation engine to `main`.
  - Verify match rating and confidence interval computations against standard test vectors.

### `TavallStudios/tavall-reflection`

#### System — Tavall Reflection

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate JVM class inspection under Java 25 strong encapsulation.

### `TavallStudios/tavall-registry`

#### System — Tavall Registry

- [ ] 2026-10-02 — Promote consumer access guide (PR #12) to `main`.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate concurrent registry lookup and registration under load.

### `TavallStudios/tavall-roblox`

- [ ] 2026-10-01 — Initialize Git history and the canonical `main` branch so the repository can receive its root `TODO.md` projection through a PR, then add the standard `docs/global-todo-projection` synchronization PR.

### `TavallStudios/tavall-scheduler`

#### System — Tavall Scheduler

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate cron/heartbeat task execution without thread leaks under Java 25 virtual threads.

### `TavallStudios/tavall-test-suite-tools`

#### System — Tavall Test Suite Tools

- [ ] 2026-10-29 — **Restore organization-wide consumer architecture-test execution after a validated replacement suite is available** (temporary pause policy: [Tavall Docs PR #86](https://github.com/TavallStudios/tavall-docs/pull/86)).
  - Scope of suspension: architecture-test Gradle plugins, `architectureTest` / `architectureAnalyze` tasks, task-facing ArchUnit tools, and architecture-only CI gates. Do not disable ordinary compiler, JUnit, contract, integration, runtime, quality, E2E, or test-authoring validation.
  - Keep canonical written architecture rules enforceable through source-aware implementation review while the executable suite is paused; preserve historical test findings and repository-root `.tavallci/` / `.tavallcd/` metadata.
  - Re-enable only after the owning `tavall-test-suite-tools` producer establishes verified replacement API/artifact, positive/negative fixtures, compatibility against representative actual consumers, and exact-head Tavall CI evidence. Update [Testing and Git](docs/quality/code-architecture/TESTING_AND_GIT.md) and affected architecture/CI docs together, then reconcile Docs Agent section-index/skill projections.

- [ ] 2026-10-22 — Add canonical module-name/type validation to the shared architecture test rules after existing source/module inventory is reconciled.  ([canonical issue](https://github.com/TavallStudios/tavall-test-suite-tools/issues/25))
  - Inspect actual Gradle projects and declared **primary** type. For new SYSTEM and RUNTIME definitions require `-system` and `-runtime` respectively; explicitly exempt repository/aggregate roots, APPLICATIONs, API/FEATURE/TOOLING/TEST_SUITE modules and provider/adapter roles. Report legacy names with mapped migration tasks rather than breaking all existing consumers before coordinated cutover.
  - Verify positive/negative fixtures, exact-source source/build metadata and per-module `.tavallci` lint integration. Do not key off a folder's mere text or a README heading like `System —`.


- [ ] 2026-10-08 — Finish architecture-rule producer PR #22 and publish a reproducible rule artifact.
  - Current PR head is `0f4c2fe`; the validated rule implementation source is `4f15f10`. Verify wrapper-backed Tavall CI and package-backed rule resolution independently from source-composite use.
  - Keep rule code and reusable policy here. Consumer repositories own their source violations and fix them without suppressing rules or expanding debt baselines; Tavall-MC keeps only its repository-specific architecture targets.

### `TavallStudios/tavall-qa`

#### System — Tavall QA Task Board

- [ ] 2026-10-23 — Complete authorized data onboarding and DEVELOPMENT/STAGING acceptance for the QA Board in the shared Tavall Web runtime.
  - `tavall-qa-system` is the `SYSTEM` / `PROVIDER` owner of mapped-JPA task, evidence, assignment, audit, VQC, and weighted-public-progress state. `tavall-web-app` owns the runtime and Account request boundary; `tavall-web-qa` owns the accepted Forge presentation; `tavall-web-dashboard` owns discovery only.
  - Keep migrations `027` and `028` with `tavall-qa`. Do not restore `progress_task`, `publicProgressTaskId`, a duplicate Web schema, runtime DDL, or an independent QA runtime.
  - Current live DEVELOPMENT serves the accepted public project index and legacy `/task-board/**` redirects. The public projection contains the two seeded projects and zero publicly visible tasks; the private task count is unknown. Add or publish real tasks only through the QA authority with an authorized Account subject. Verify migration `028` and the staff Account/QA permission matrix independently.
  - The current Web candidate has local exact-source `check`, standalone-artifact, 1440px/390px browser, NHV/privacy, Focus Workspace, editor-routing, and save-return evidence. These results do not replace exact-head Tavall CI, an immutable release, STAGING delivery, or authenticated Account-backed acceptance.
  - Live reconciliation (2026-10-23 5:02 PM PDT): Development was healthy/active at Web source `bc03a38733cf3ba3c6878ca91304a8c7c6cc7c01`, artifact `6e36b9537d4ecf65792c503b1bc2d9fefadef777d7620552e95aee85518eae30`, generation `450`; Staging was healthy/standby at source `a6220d237685cea72d38bb9c16ecd479b1cd0d83`, artifact `9d22a738650d70e1ace3f77390b2988f652e897005ef4331819f95b1f1838e22`, generation `343`. Public QA root/health and both project pages returned HTTP `200`; each project showed zero public tasks and the private task count remains unknown. Direct Development served the QA root (`200`); direct Staging returned `404`. No task data was changed. Evidence: `qa-board-live-reconciliation-20261024.json` (observed 2026-10-24 12:02 AM UTC).
  - Exact-source TCI remains open. Request `f6de3e64-27b9-4275-9ec6-62fbb09240f1` for Web main `ccc4436bed4e6284aaba7a9c53fd59027848803e` stopped at missing `jakarta.persistence:jakarta.persistence-api:3.2.0`. Web PR #84 pins the immutable mirror digest `c945956c42d0e49f28ec925d62956d94668c0b3fab0293d9dd2db028b26d9cd2`; retry `445d385b-302d-46e5-83ca-1a0f32b4705f` used Web source `8cd36de689284fc016e97b2e648cdf5947dc6c25`, Tavall CI runtime `1d04fb820b2d2cf83ebafca8e80fc26d7d660848`, profile `all`, and no Lane or Environment. It failed before application checks with unresolved `org.tavall:tavall-web-api:0.1.1-SNAPSHOT`; evidence is `tavall-storage://ci/runs/445d385b-302d-46e5-83ca-1a0f32b4705f/ci-evidence.json` (SHA-256 `c46c64f59a16df7483486b0c633d150b18feb9b307a577b9b903b17c7ad8d0cf`). No artifact was delivered and no deployment was attempted. A local publish/offline-consumer diagnostic for `tavall-web-api` passed at `8cd36de`, but does not establish Cloud Executor composition. PR #84 remains Draft at head `2c1ccedb8702355566a7e4b55c895fe832c733e3`; its current-head retry is recorded below. The Development artifact is 11 commits behind target `ccc4436` and cannot be reused; it predates merged Message Editor A/C changes from PR #80.
  - Latest exact-head retry (2026-10-24 01:00 UTC): request `5a87ccae-736b-46f1-b3eb-7df401e70eed` tested Web PR #84 head `2c1ccedb8702355566a7e4b55c895fe832c733e3` with Tavall CI `1d04fb820b2d2cf83ebafca8e80fc26d7d660848`, profile `all`, source aggregate SHA-256 `c7a29ea7207bab8466db6a50c7bac331818a04c0711b5fda50081b55fc7e676e`, resolution SHA-256 `c8a5cb798d009bc3f3069ca5d70bf734cd0fbe1b4e805d6f3f70a47a7583e198`, and no Lane or Environment. It failed before product checks with `DEPENDENCY_BOOTSTRAP_UNAVAILABLE` for unresolved `org.tavall:tavall-web-api:0.1.1-SNAPSHOT`; evidence is `tavall-storage://ci/runs/5a87ccae-736b-46f1-b3eb-7df401e70eed/ci-evidence.json` (SHA-256 `cb1b7ebae2abda71e430d04cb6b35d7e3193b7155cb84a48a816a732dacdc237`). No product acceptance, artifact delivery, or deployment resulted. Keep this task open while exact-source composition is investigated and retried.

- [ ] 2026-10-23 — Complete typed progress integrations through their existing owners after API and delivery contracts are verified.
  - The QA progress aggregator remains the PostgreSQL-backed authority. Check the current Cache/Event, CMS, Roadmap, Discord publisher, and public-proof owners for typed consumer contracts before connecting subscribers.
  - Exact-owner recheck on 2026-10-23: `tavall-qa@516a77c` provides `ITaskBoardProgressAggregator` inside the QA authority; `tavall-cache@e6e78fd` and `tavall-eventbus@00866ad` expose generic cache/event infrastructure but no Task Board progress consumer; `tavall-web-content@edde476` and `tavall-content@95e8284` expose no Task Board progress/roadmap contract; `tavall-web-dashboard@61246e9` provides discovery only; `tavall-discord@41d1904` has no Task Board progress/milestone consumer. Web's `ProgressDataStore` / `IProgressEventService` are its separate legacy progress path and remain outside Task Board authority.
  - Preserve idempotent replay and audience filtering before counts and derived events. Private task changes must not leak through cache, event, CMS, Discord, or public-proof payloads.
  - No cross-system subscriber or event was introduced during this check. Keep the item open until each owning repository exposes a typed producer/consumer contract and exact-source acceptance can be recorded.
  - Do not create placeholder publishers, subscribers, duplicate progress stores, or treat Redis/cache projections as durable authority. Record each integration's owner and acceptance when its typed boundary is available.

### `TavallStudios/tavall-web`

#### System — Tavall Web Platform

- [ ] 2026-10-22 — Define only evidence-backed Account/Commerce fan-in SYSTEMs with compliant module names, while retaining `tavall-web-app` as APPLICATION.  ([canonical issue](https://github.com/TavallStudios/tavall-web/issues/77))
  - Candidate modules: `tavall-web-account-system` (shared identity/organization business authority) and `tavall-web-commerce-system` only if contracts and consumers justify extraction from `tavall-web-app`. Leave the `tavall-web` repository root and existing `tavall-web-account`/`tavall-web-content` presentation repos unchanged.
  - Keep Spring process, OAuth host security, session and routing inside the existing app; preserve Account's canonical identity authority and product backend boundaries. Acceptance: exact-source Spring startup, OAuth denial flows, organization/checkout persistence and browser tests, no new service processes.


- [ ] 2026-10-02 — Reconcile and fold `tavall-web-docs` into `tavall-web` (PR #48).
  - Consolidate web documentation authority and retire the separate `tavall-web-docs` repository surface.
- [ ] 2026-10-02 — Migrate remaining legacy Thymeleaf surfaces onto the pure-Java `AbstractPage<SELF>` framework.
  - Migrate Content/Blog editor script, Progress tracker, and Docs admin pages off Thymeleaf.

- [ ] 2026-10-03 — Complete Web frontend artifact ownership and retire the deleted Discord page source (PR #58).
  - Keep route/surface/exposure contracts in `tavall-web-api`; Page, HTML/CSS, animation, asset, TypeScript, and rendering contracts belong to `tavall-web-frontend`.
  - Current PR #58 head is `e3e27ea`; its source graph removes the deleted `tavall-web-discord` dependency, artifact, and page controller. Earlier exact-source request `42a84c3a-01a2-435e-a6e6-e6c78ebfc5e2` passed on older code source `b87706b`, not this head.
  - The public `discord.tavall.org` route still serves the old Link Discord page. Validate the current integrated Web source and browser behavior, then use only the documented DEVELOPMENT delivery path if runtime acceptance passes; no Production runtime exists.

#### Module — tavall-web-frontend

- [ ] 2026-10-02 — Complete pure-Java HTML component vocabulary and rendering engine.
  - Support video, figures, grouped form controls, and typed `data-tavall-*` attributes without external runtime dependencies.
- [ ] 2026-10-04 — Verify package-backed Page/rendering artifact resolution for Web consumers.
  - Keep route/surface/exposure in `tavall-web-api`; resolve Page, rendering, and frontend AST contracts from `tavall-web-frontend` independently from source substitution.

#### Module — tavall-web-frontend-spring

- [ ] 2026-10-02 — Maintain clean Spring MVC adapter isolation in `tavall-web-frontend-spring`.
  - Ensure that Spring MVC / Servlet dependencies remain strictly encapsulated in this adapter module.

#### Module — tavall-web-app

- [ ] 2026-10-18 — Reconcile Web private-preview and Account acceptance after PR #63's branch merge.
  - PR #63 merged to `working/content-publishing-operator-20261005` at `f90608e` on 2026-10-15; it did not merge to Web `main` (`fcab2b9`). The exact GitGuardian check passed on head `0691309`; no Tavall TCI aggregate was emitted on that refreshed head. All-profile request `5c07d137-03cc-425b-8eaa-7a41c6be1d31` referred to an earlier head and is not current acceptance evidence.
  - Reconcile any desired source delta onto the current Web mainline, then run exact-head TCI and the private-preview browser suite. Provider SSO, Account schema/CONTROL wiring, package-backed dependency resolution, and delivery remain separate gates. Public-host deployment state was not rechecked in this TODO update.

### `TavallStudios/tavall-web-account`

#### System — Tavall Web Account

- [ ] 2026-10-02 — Implement Tavall Account platform contracts under unified Web architecture.
  - Provide SSO, profile management, and Minecraft account linking APIs decoupled from legacy web templates.

### `TavallStudios/tavall-web-blog`

#### System — Tavall Web Blog

- [ ] 2026-10-02 — Migrate blog post presentation onto Tavall Web pure-Java frontend framework.
  - Replace legacy template rendering with `AbstractPage<SELF>` components.

### `TavallStudios/tavall-web-cloud`

#### System — Tavall Web Cloud Operations

- [ ] 2026-10-02 — Validate Cloud operations admin dashboards against live Tavall Cloud CONTROL and Executor status endpoints.

### `TavallStudios/tavall-web-commerce`

#### System — Tavall Web Commerce

- [ ] 2026-10-02 — Migrate web store product catalog and checkout flows to Tavall Web frontend framework.
  - Implement Web Store System Design contracts under pure-Java Page model.

### `TavallStudios/tavall-web-content`

#### System — Tavall Web Content Studio

- [ ] 2026-10-09 — Add per-platform posting metadata and campaign-rule human review to the existing Content Dashboard.
  - Extend the review-ready clip/detail state within the current three-page Studio: playback preview, editable title/description/caption/hashtags/tags/links, campaign rule checklist with pass/fail/unknown evidence and source, disclosure/uncertainty flags, and explicit approve/revise/reject actions.
  - Show pending review and approval history, keep the final reviewer-approved metadata copyable/exportable, and prevent a publish/queue action until Tavall Content confirms the exact approved version and authorization.
  - Consume typed `tavall-content-client` contracts; Tavall Content owns metadata, rule evaluation, decisions and publishing state. No browser-owned shadow validation or extra standalone dashboard.
  - Acceptance: authenticated browser E2E for per-platform edits, missing required `@boxabl`/tag rules, uncertain disclosure checks, stale approvals and rejected/unauthorized publication.

- [ ] 2026-10-02 — Promote Content Studio presentation module (PR #3) to `main` once `tavall-web` framework stack merges.
  - Validate Dashboard, Clip Library, and Clip Editor under real `tavall-web-app` session-backed host.
- [ ] 2026-10-02 — Integrate browser E2E test suite with continuous exact-source Tavall CI execution.

### `TavallStudios/tavall-web-contractors`

#### System — Tavall Web Contractors

- [ ] 2026-10-02 — Promote Contractors Home presentation module (PR #3) to `main`.
  - Validate surface routing and contractor profile views in `tavall-web-app`.

### `TavallStudios/tavall-web-mc`

#### System — Tavall Web Minecraft Surface

- [ ] 2026-10-02 — Migrate remaining player stat and leaderboard views onto pure-Java frontend components.
- [ ] 2026-10-08 — Add the Minecraft-specific Builder Studio browser view after the MC Builder API and Web app facade contracts are accepted.
  - Keep the hosted route/session and browser presentation in Tavall Web; consume typed same-origin view data from MC Builder. Keep compiler, WorldOps, simulation/replay, worker execution, and Minecraft filesystem authority in Tavall-MC.

### `TavallStudios/tavall-web-mcp`

#### System — Tavall Web MCP

- [ ] 2026-10-02 — Promote Web MCP server CI and runtime configuration to `main`.
  - Validate MCP tools against shared DI container and test-suite-tools architecture guards.

### `TavallStudios/tavall-web-workflows`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-workflows`

_No open global TODO items currently tracked._
