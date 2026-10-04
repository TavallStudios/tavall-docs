# Tavall Global TODO

> **Status:** Active  
> **Authority:** Canonical organization-wide TODO ledger  
> **Repository projections:** Every maintained TavallStudios repository exposes a bot-managed root `TODO.md` that projects only that repository's section from this file.  
> **Last updated:** 2026-10-02

This file is the single source of truth for organization-wide repository TODO work. Repository-local `TODO.md` files are generated static projections and must not become independent task ledgers.

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

#### System — Tavall AI Platform

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

- [ ] 2026-10-02 — Promote platform staging PR #14 and CI wrapper adoption PR #7 to `main`.
  - Verify exact-source build and integration tests on `DEVELOPMENT_SHARED` Executor.
- [ ] 2026-10-02 — Complete Tavall AI browser DI integration (PR #15).
  - Validate session analytics extraction through DI-injected browser capabilities.

### `TavallStudios/tavall-cache`

#### System — Tavall Cache

- [ ] 2026-10-02 — Promote PR #11 (retaining immutable cache artifacts) to `main`.
  - Validate exact-source composite execution across all eight cache modules.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for each of the eight cache modules.
  - Verify that Tavall CI aggregates module definitions without relying on repository-root-only discovery.

### `TavallStudios/tavall-ci`

#### System — Tavall CI

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

- [ ] 2026-10-02 — Validate typed Cloud Executor CLI caller under live CONTROL placement.
  - Verify frozen-plan submission to `DEVELOPMENT_SHARED` without leaking ambient credentials or falling back to legacy sandbox paths.

#### Module — tavall-ci-cd

- [ ] 2026-10-02 — Enforce strict artifact reference and digest binding in delivery bundle materialization.
  - Verify that `tavall-ci-cd` rejects mismatched `storageRef` and artifact digests before delivery.

### `TavallStudios/tavall-cloud`

#### System — Tavall Cloud

- [ ] 2026-10-02 — Synchronize and validate Draft staging root PR #397 (`staging/runtime`) against current `main`.
  - Integrate merged docs PRs #417, #418, #421, and child PR #424.
  - Execute full composed-root run on `DEVELOPMENT_SHARED` Executor and verify all 7 profiles pass.
- [ ] 2026-10-02 — Resolve GitGuardian secret scanner findings on Cloud PR #424 to unblock staging integration.
  - Audit flagged commits with credential-scanning authority and document resolution.
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

#### Module — Executor

- [ ] 2026-10-02 — Finalize transition from legacy sandbox paths to canonical `tavall-cloud-executor`.
  - Standardize source manifests on `source-roots.executor.txt` and retire residual sandbox operations.
  - Validate concurrent execution on `DEVELOPMENT_SHARED` across parallel jobs sharing `/srv/dev-storage/tavall-cache/shared-ci/gradle`.

#### Module — Node Agent

- [ ] 2026-10-02 — Enforce compile-time independence between Node Agent and CONTROL.
  - Maintain clean unidirectional dependency: CONTROL requires Node Agent at runtime only.
  - Validate Agent bootstrap installer using immutable artifact `789c2432...`.

#### Module — Networking (tavall-networking)

- [ ] 2026-10-02 — Validate cross-region three-node Minecraft network routing.
  - Verify nftables/IPIP tunnels, packet filters, and fail-closed rollback across `dev-storage`, `novus-ffa-east`, and `novus-ffa-west`.

### `TavallStudios/tavall-concurrency`

#### System — Tavall Concurrency

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and promote Java Tools platform adoption to `main`.
  - Validate thread safety and lock contention tests under Java 25.

### `TavallStudios/tavall-content`

#### System — Tavall Content Studio

- [ ] 2026-10-02 — Implement asynchronous render queue with job tracking and progress notifications for Content Studio.
  - Move timeline renders and cutaway processing out of the synchronous HTTP request thread.
  - Provide durable job status endpoints (`QUEUED`, `RENDERING`, `COMPLETED`, `FAILED`) and cancellation support.
- [ ] 2026-10-02 — Implement cutaway audio blending and audio channel selection in timeline renderer.
  - Support mixing cutaway audio with primary timeline audio or replacing primary audio during cutaways.
- [ ] 2026-10-02 — Implement production Google Drive asset importer and authorized AI model provider adapters.
  - Replace test doubles with credential-managed production implementations.
- [ ] 2026-10-02 — Implement beat-synchronized timeline placement engine based on audio waveform analysis.
  - Translate visual beat annotations into sample-accurate frame cut points.
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

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for all database modules.
  - Validate Flyway migration sequencing, connection pool sizing, and transaction boundaries under PostgreSQL 14/16.
- [ ] 2026-10-02 — Promote consumer access guide (PR #27) and multi-node read replica contracts to `main`.

### `TavallStudios/tavall-di`

#### System — Tavall DI

- [ ] 2026-10-02 — Promote staging PR #13 to `main` with verified Java 25 / Gradle 9.6.1 build.
  - Verify compile-time bytecode enhancement and runtime resolution across all consumer modules.

### `TavallStudios/tavall-discord`

#### System — Tavall Discord

- [ ] 2026-10-02 — Promote platform staging PR #4 to `main` for standalone Discord client platform.
  - Validate PostgreSQL account link migrations and Discord event gateway resilience.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for Discord platform modules.

### `TavallStudios/tavall-docs`

#### System — Tavall Documentation

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

### `TavallStudios/tavall-logging`

#### System — Tavall Logging

- [ ] 2026-10-02 — Promote consumer access guide (PR #11) to `main`.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and validate structured JSON log formatting under high-concurrency workloads.

### `TavallStudios/tavall-mc`

#### System — Tavall MC / Project Novus

- [ ] 2026-10-03 — Accept repository/module/runtime separation root PR #333 before resuming the large gameplay stack.
  - Keep `tavall-minecraft-framework` reusable: move Kingdom/Novus policy, product cosmetics, and Tavall runtime-host identity into MC-owned modules; retain generic Minecraft host, API, game, and NMS capabilities in Framework.
  - Remove the stale cross-game Resource Game frontend/TCP bridge copy from MC; `TavallStudios/tavall-hytale-resource-game` owns those shared contracts and its Minecraft adapter. Add no Hytale dependency unless a current MC product consumer requires the typed contract.
  - Keep runtime schema creation out of Framework and MC launch. Preserve migration intent and leave durable writes blocked until the canonical Tavall Database migration owner is established.
  - Do not merge PR #301 or stale fan-in #299. Preserve useful composite/lock work and rebuild a focused current-main Framework consumer after producer purity and product persistence ownership are resolved.
  - Current #333 exact-head checks are pending. The previously observed 51 Kingdom/server failures out of 277 tests are historical evidence from an older candidate and must not be reported as current.
- [ ] 2026-10-03 — Rebuild the Combined/Paper/Velocity/FFA/Kingdoms staging generation from accepted current main.
  - Keep old roots such as #153, #195, #196, #198, #199, #262, and #294 as historical evidence until useful deltas have reviewed replacements.
  - Keep Web, Cloud Agent, and Ingress process roots out of Tavall-MC.
- [ ] 2026-10-03 — Complete the Builder Studio ownership boundary.
  - Keep compiler, WorldOps, simulation, replay, WorldVision, and worker execution in MC Builder.
  - Port hosted/admin presentation to Tavall-Web after the typed remote Builder API is defined; PR #258 is closed and unmerged.
- [ ] 2026-10-03 — Complete product-specific Discord host acceptance.
  - Tavall-Discord PR #9 publishes the reusable runtime through Tavall private Maven, and MC source-composite/package checks pass locally.
  - Run wrapper-backed Tavall CI and verify the external Discord host loads the Novus product artifact; retire the transitional JDA contributor as features adopt platform-neutral contracts.
- [ ] 2026-10-03 — Add a Minecraft-specific Cloud request only when Tavall-Cloud publishes a typed cross-process client.
  - The MC candidate removes the generic /cloud CLI relay, Cloud runtime dependency, socket, and agent-secret configuration.
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

- [ ] 2026-10-02 — Promote Node-based CI validation (PR #6) and bot testing system documentation (PR #8) to `main`.
- [ ] 2026-10-02 — Execute automated bot scenarios against live Paper server instance.
  - Verify FFA combat loops, pathfinding, reconnect recovery, and proxy integrity under load.

### `TavallStudios/tavall-mc-paper`

#### System — Tavall MC Paper

- [ ] 2026-10-02 — Promote canonical Gradle 9.6.1 wrapper and Paperweight validation (PR #6) to `main`.
  - Ensure Paperweight artifact resolution remains isolated from incomplete tool registries.
- [ ] 2026-10-02 — Validate low-level packet filter hooks against upstream Paper release without degrading server tick performance.

### `TavallStudios/tavall-minecraft-framework`

#### System — Minecraft Framework

- [ ] 2026-10-02 — Promote exact-source Gradle CI adoption (PR #11) and account-link admin resolvers (PR #14) to `main`.
  - Emit immutable framework library artifacts for downstream consumption by `tavall-mc`.
- [ ] 2026-10-02 — Finalize retirement of Tavall Web runtime identity from framework modules (PR #9).
  - Ensure framework is decoupled from Web runtime dependencies.

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

- [ ] 2026-10-02 — Clear the 120 existing architecture violation findings across consumer repositories.
  - Resolve 44 repository-role violations, 34 direct-thread creation violations, and 42 production-`var` violations identified during Cloud and consumer test suite audits.
- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` definitions for all test-suite and architecture enforcement modules.
  - Verify that Tavall CI discovers and verifies core, patterns, runtime, di, and web architecture rule modules.

### `TavallStudios/tavall-web`

#### System — Tavall Web Platform

- [ ] 2026-10-02 — Reconcile and promote the core frontend framework stack (PR #46, PR #47, PR #49) to `main`.
  - Resolve merge conflicts with `main` in PR #46.
  - Land Spring adapter (`tavall-web-frontend-spring`), Organization Admin Dashboard, Contractors Home routing, and Content Studio mount.
- [ ] 2026-10-02 — Reconcile and fold `tavall-web-docs` into `tavall-web` (PR #48).
  - Consolidate web documentation authority and retire the separate `tavall-web-docs` repository surface.
- [ ] 2026-10-02 — Migrate remaining legacy Thymeleaf surfaces onto the pure-Java `AbstractPage<SELF>` framework.
  - Migrate Content/Blog editor script, Progress tracker, and Docs admin pages off Thymeleaf.

- [ ] 2026-10-03 — Complete Web frontend artifact ownership and retire the deleted `tavall-web-discord` page source (PR #58).
  - Keep route/surface/exposure contracts in `tavall-web-api`; Page, HTML/CSS, animation, asset, TypeScript, and rendering contracts belong to `tavall-web-frontend`.
  - Tavall-Architecture-Tests PR #21 corrects the reusable frontend/API rule and passed its exact-source Tavall CI quality gate. Rerun PR #58 through Tavall CI using that exact producer head, prove package-backed resolution independently from source substitution, and keep browser/deployment acceptance separate.

#### Module — tavall-web-frontend

- [ ] 2026-10-02 — Complete pure-Java HTML component vocabulary and rendering engine.
  - Support video, figures, grouped form controls, and typed `data-tavall-*` attributes without external runtime dependencies.

#### Module — tavall-web-frontend-spring

- [ ] 2026-10-02 — Maintain clean Spring MVC adapter isolation in `tavall-web-frontend-spring`.
  - Ensure that Spring MVC / Servlet dependencies remain strictly encapsulated in this adapter module.

#### Module — tavall-web-app

- [ ] 2026-10-02 — Build and validate `tavall-web-app` artifact with all mounted consumer surfaces.
  - Validate exact-source build and execute browser E2E test suites against the integrated application.
  - Verify public routing through Cloudflare -> Apache -> `tavall-web` router on port 19091, checking DEVELOPMENT (19092) and STAGING (19093) health observations.

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

- [ ] 2026-10-02 — Promote Content Studio presentation module (PR #3) to `main` once `tavall-web` framework stack merges.
  - Validate Dashboard, Clip Library, and Clip Editor under real `tavall-web-app` session-backed host.
- [ ] 2026-10-02 — Integrate browser E2E test suite with continuous exact-source Tavall CI execution.

### `TavallStudios/tavall-web-contractors`

#### System — Tavall Web Contractors

- [ ] 2026-10-02 — Promote Contractors Home presentation module (PR #3) to `main`.
  - Validate surface routing and contractor profile views in `tavall-web-app`.

### `TavallStudios/tavall-web-discord`

#### System — Tavall Web Discord

- [ ] 2026-10-02 — Migrate Discord guild sync and bot status admin views to Tavall Web frontend framework.

### `TavallStudios/tavall-web-mc`

#### System — Tavall Web Minecraft Surface

- [ ] 2026-10-02 — Promote self-typed Page contract adoption (PR #6) to `main`.
  - Ensure zero Spring dependencies in `tavall-web-mc` page definitions.
- [ ] 2026-10-02 — Migrate remaining player stat and leaderboard views onto pure-Java frontend components.

### `TavallStudios/tavall-web-mcp`

#### System — Tavall Web MCP

- [ ] 2026-10-02 — Promote Web MCP server CI and runtime configuration to `main`.
  - Validate MCP tools against shared DI container and test-suite-tools architecture guards.

### `TavallStudios/tavall-web-workflows`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-workflows`

_No open global TODO items currently tracked._
