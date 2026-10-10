# Tavall Global TODO

> **Status:** Active  
> **Authority:** Canonical organization-wide TODO ledger  
> **Repository projections:** Every maintained TavallStudios repository exposes a bot-managed root `TODO.md` that projects only that repository's section from this file.  
> **Last updated:** 2026-10-10

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
- [ ] 2026-10-10 — Let CONTROL admit new nodes instead of a hard-coded inventory.
  - The DEVELOPMENT node inventory is hard-coded in `CloudDevelopmentInfrastructureInventorySeeder` (`dev-storage`, `novus-ffa-east`, `novus-ffa-west`), and `node approve` is parsed (`CloudCommandLineParser`) but has no handler, so a newly installed agent never appears in `node list`.
  - Implement enrollment and `node approve`/`reject` against the Redis node inventory, then redeploy CONTROL and admit `work-0` (`10.91.0.4`, AGENT, `compute`), whose agent has been running since 2026-10-10.
- [ ] 2026-10-10 — Register the `work-0-storage` network-storage export in CONTROL topology.
  - `work-0` serves ZFS `tavallwork0/development` → `/srv/tavall-storage/development` read-only over NFSv4.2 to `10.91.0.1/32` (installed with `install-network-storage-export.sh`, verified by a real mount). Add it to `developerTopology.networkStorage` and reconcile its mount intent; this needs a CONTROL restart.

#### Module — Executor

- [ ] 2026-10-02 — Finalize transition from legacy sandbox paths to canonical `tavall-cloud-executor`.
  - Standardize source manifests on `source-roots.executor.txt` and retire residual sandbox operations.
  - Validate concurrent execution on `DEVELOPMENT_SHARED` across parallel jobs sharing `/srv/dev-storage/tavall-cache/shared-ci/gradle`.

#### Module — Node Agent

- [ ] 2026-10-02 — Enforce compile-time independence between Node Agent and CONTROL.
  - Maintain clean unidirectional dependency: CONTROL requires Node Agent at runtime only.
  - Validate Agent bootstrap installer using immutable artifact `789c2432...`.
- [ ] 2026-10-10 — Make the Node Agent installer work on a fresh Ubuntu 26.04 host.
  - Ubuntu 26.04 ships sudo-rs, which rejects the wildcard rules (`systemctl start tavall-cloud-*.service`) in `/etc/sudoers.d/tavall-cloud-agent`; `install` aborts at `visudo -cf` before chown/enable. `work-0` was switched to classic `sudo.ws` as a workaround.
  - The generated unit lists `/run/netns` and `/run/tavall-executor` in `ReadWritePaths`; neither exists on a fresh host, so the service fails with `226/NAMESPACE`. Ship a tmpfiles.d entry or create them in `install`.
  - A pre-placed `control.secret` must be `0640 root:tavall-cloud` for the agent to read it; document or enforce this when joining an existing CONTROL.

#### Module — Networking (tavall-networking)

- [ ] 2026-10-02 — Validate cross-region three-node Minecraft network routing.
  - Verify nftables/IPIP tunnels, packet filters, and fail-closed rollback across `dev-storage`, `novus-ffa-east`, and `novus-ffa-west`.
- [ ] 2026-10-10 — Restore a Nebula lighthouse/relay for the DEVELOPMENT overlay.
  - `novus-ffa-west` (lighthouse/relay `10.91.0.2`, `152.44.44.84:42420`) and `novus-ffa-east` (`10.91.0.3`) have been unreachable since about 2026-10-05; CONTROL reports both OFFLINE.
  - `dev-storage` and `work-0` currently reach each other through direct `static_host_map` entries (backup `config.yml.before-work-0-20261010`). Replace that with a live lighthouse or a documented static topology.

### `TavallStudios/tavall-concurrency`

#### System — Tavall Concurrency

- [ ] 2026-10-02 — Author module-local `.tavallci/ci.yaml` and promote Java Tools platform adoption to `main`.
  - Validate thread safety and lock contention tests under Java 25.

### `TavallStudios/tavall-content`

#### System — Tavall Content Studio

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

- [ ] 2026-10-02 — Complete `tavall-minecraft-framework` consumption cutover (PR #301 / PR #299).
  - Remove duplicate framework implementations in `tavall-mc` and switch dependency bindings to the extracted library.
  - Remove retired `.github/workflows/cloud-runtime-deployment.yml` and validate `novus-runtime-deploy.jar` build through Tavall CI.
- [ ] 2026-10-02 — Reconcile and promote runtime staging PR #294 (`promotion/runtime-staging-current-20260920`) to `main`.
  - Validate exact-source composite build on Java 25 / Gradle 9.6.1 on Cloud Executor.
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

- [ ] 2026-10-02 — Validate Paper runtime and client verification for Player Identity and Crown Store (PR #310).
  - Verify PostgreSQL migration, entitlement caching, and in-game transaction fulfillment.

#### Module — Discord Integration

- [ ] 2026-10-02 — Complete extraction of reusable Discord client into `tavall-discord` (PR #284).
  - Remove legacy embedded Discord bot classes from `tavall-mc`.

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

#### Module — tavall-web-api

- [ ] 2026-10-02 — Formalize self-typed Page contract in `tavall-web-api`.
  - Maintain strict transport and container neutrality: zero Spring, Servlet, or HTTP server dependencies in `tavall-web-api`.

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