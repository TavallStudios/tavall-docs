# Tavall Descriptor Inventory and Coverage Projection

> **Status:** Active derived projection  
> **Applies to:** current `TavallStudios` repositories, and verified independent build/source modules and tools  
> **Authority:** [README_STANDARDS.md](README_STANDARDS.md) owns the descriptor format, field definitions, status vocabulary, and non-goals. This document is a **derived projection from source**, not a second authority, not an approval mechanism, and not a task ledger.  
> **Related:** [TAVALL_TERMINOLOGY.md](TAVALL_TERMINOLOGY.md), [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md), [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md), [MODULE_TYPES.md](MODULE_TYPES.md)

## 1. What this document is

This projection records which current Tavall repositories and verified modules have a **human-readable "What is this?" descriptor** in the canonical format, which are still candidates, and which are blocked on an ownership conflict.

It is intentionally *only* a coverage projection:

- The owning README, accepted Design/Technical document, and current source remain authoritative for every claim written here. If a row conflicts with its owner, the row is wrong and must be corrected.
- It does not approve, rename, or rebrand anything. A descriptor here is presentation metadata (see [README_STANDARDS.md](README_STANDARDS.md) "Non-goals").
- It is not a work ledger. Implementation and review tracking stay on GitHub Issues and the QA Task Board.
- It does not restate full ownership contracts. "What it does" is one sentence; the owning document carries the contract.

## 2. Method and evidence basis

| Step | Source and exact command | Result |
| --- | --- | --- |
| Repository enumeration | `gh api --paginate "orgs/TavallStudios/repos?per_page=100"` | 97 repositories: 91 not archived, 6 archived |
| Repository description | same call, `.description` field | Used only when no README exists |
| Repository README grounding | `gh api "repos/TavallStudios/<repo>/readme" -H "Accept: application/vnd.github.raw"` (current default branch) | 85 of 97 repositories have a README; 12 do not |
| Local workspace cross-check | `<workspaces>/*/repo_root/README.md` | 83 local checkouts; used to cross-check, not to override origin READMEs |
| Module grounding | `settings.gradle*` `include(...)` blocks and owning README module tables on the current default branch | Module rows below name only modules verified from one of those two sources |
| Absence check | `gh api "repos/TavallStudios/tavall-profiling"` and an organization-wide repository search for `tavall-profiling` | HTTP 404 / zero results; the repository does not exist (see §8.2) |

Two evidence caveats are recorded rather than hidden:

1. **Local checkouts lag origin.** The local `<workspaces>/*/repo_root` snapshots were last fetched in October 2026 for several repositories; `origin/main` READMEs are newer. Descriptor text in this pass follows the `origin/main` README, and local snapshots were used only for cross-checking. Where the two visibly diverge, the divergence is listed in §8 rather than silently resolved.
2. **No descriptor in this projection is approved.** Every row is `PROPOSED` at best. Publication of a descriptor still requires the owning reviewer per [README_STANDARDS.md](README_STANDARDS.md).

### Surface exposure

The inventory is published in the public `tavall-docs` repository. Rows therefore record **only** what the owning repository already publishes on its own default branch or already states in its own public repository description. A private repository's row names the repository (which organization membership already discloses) and never adds private topology, deployment targets, hostnames, credentials, node/Environment layouts, or internal relationships that the owning repository does not itself publish. Where a private repository's README is itself the private detail, the row deliberately stays at the level of the README's opening self-description.

## 3. Field and status vocabulary

Fields, formatting, and non-goals are owned by [README_STANDARDS.md](README_STANDARDS.md) "Human-readable descriptors (What is this?)". This projection adds one inventory-only status value:

| Status | Meaning in this projection |
| --- | --- |
| `APPROVED` | The owning reviewer accepted the descriptor for publication. |
| `REVIEWED` | Checked against the owning README/source/accepted design; no ownership conflict recorded. |
| `PROPOSED` | Candidate only. Not reviewed, not published. |
| `NEEDS_OWNER_REVIEW` | A `PROPOSED` candidate that is **blocked** by a recorded ownership or terminology conflict in §8. It must not be published until the owner resolves the conflict. |
| `STALE` | A previously published descriptor now contradicted by current ownership/source. |

`APPROVED`, `REVIEWED`, and `STALE` are all `0` in this pass because no descriptor has been published yet.

## 4. Active repositories

Classification `ACTIVE` means the repository currently carries accepted or in-progress ownership for its stated responsibility. It is **not** a statement that every capability is implemented or deployed; that remains owned by the repository's Progression and Deployment documents.

| Technical name | Public name | Descriptor | What it does | Does not own | Status |
| --- | --- | --- | --- | --- | --- |
| `tavall-ai` | Tavall AI | Autonomous Work Orchestrator | Packages reusable agents, process/skill contracts, model-execution capabilities, and the executable Tavall AI runtime that coordinates authorized work. | Authorization, CI policy, Cloud placement, or product behavior. | `PROPOSED` |
| `tavall-cloud` | Tavall Cloud | Distributed Compute Fabric | Owns the typed control plane, node domain, service lifecycle, execution providers, and Cloud networking boundaries. | Product behavior in hosted services; CI policy; shared engineering policy. | `PROPOSED` |
| `tavall-cloud-networking` | Tavall Cloud Networking | Cloud Network Subsystem Integration | Owns Cloud-specific network subsystem contracts, state, policy, and provider integration for the Cloud Node runtime. | The Cloud Node process lifecycle, or generic reusable networking primitives. | `PROPOSED` |
| `tavall-ci` | Tavall CI | Verifiable Software Delivery | Turns repository-owned `.tavallci` definitions into exact-source graphs, typed checks, evidence, immutable artifacts, readiness gates, and promotion decisions. | Gradle/build policy, Cloud scheduling, environment or Executor placement, GitHub App mechanics. | `PROPOSED` |
| `tavall-docs` | Tavall Docs | Living Engineering Rulebook | Owns shared engineering, architecture, workflow, quality, and documentation policy, and routes system-specific contracts to their owners. | System-specific architecture, implementation state, or deployment records. | `PROPOSED` |
| `tavall-docs-private` | Tavall Docs Private | Private Documentation Boundary | Records the repository boundary for private Tavall documentation; the recorded branch defines no source, module, or artifact. | Any source, build module, runtime, or deployment artifact. | `NEEDS_OWNER_REVIEW` |
| `tavall-qa` | Tavall QA | Task Board and QA Authority | Owns the mapped-JPA Task Board, QA verification plane, and their projections as Tavall's authoritative task and verification backend. | GitHub Issue authority, product runtime, identity, or CI policy. | `PROPOSED` |
| `tavall-nlew` | Tavall NLEW | Typed Environment Topology Library | Owns typed Nodes/Lanes/Environments/Workspaces identities, records, policies, fenced Environment generation transitions, and metadata migration; it has no runtime of its own. | Execution, isolation, placement, and enforcement, which belong to Cloud and the Executor contract (§8.1). | `NEEDS_OWNER_REVIEW` |
| `tavall-di` | TIDI | Type-Safe Dependency Wiring | Owns dependency discovery, metadata, instance lifecycle, typed dependency access, explicit delegation, and source lowering. | Consumer application composition, scheduling, or service lifecycle. | `PROPOSED` |
| `tavall-database` | Tavall Database | Multi-Database Access Layer | Owns shared database contracts plus separate PostgreSQL, MongoDB, Redis, and Qdrant provider modules. | Application persistence policy, schema ownership, or a second cache/registry runtime. | `PROPOSED` |
| `tavall-cache` | Tavall Cache | Semantic Multi-Store Cache | Separates shared cache contracts and semantic routing from memory, disk, Redis, MongoDB, PostgreSQL, and Qdrant adapters. | The authoritative data store for any consumer. | `PROPOSED` |
| `tavall-concurrency` | tavall-concurrency | Async Helpers and Write-Once State | Provides a virtual-thread-backed asynchronous task runner and an immutable-after-assignment value holder. | Scheduling policy, thread lifecycle ownership of consumers, or event routing. | `PROPOSED` |
| `tavall-eventbus` | Tavall EventBus | Domain-Aware Event Routing | Provides listener registration and removal, event domains, middleware, and event metadata in one Java library module. | Domain event schemas or consumer-side handling behavior. | `PROPOSED` |
| `tavall-logging` | tavall-logging | Leveled Logging Helpers | Provides leveled log entry points, exception output, and styled text helpers. | Log aggregation, transport, or retention policy. | `PROPOSED` |
| `tavall-reflection` | tavall-reflection | Reflection and Class-Loading Helpers | Centralizes low-level reflection and class-loading helpers for classes, fields, methods, method handles, and file-based library loading. | Any consumer's type model or lifecycle. | `PROPOSED` |
| `tavall-scheduler` | tavall-scheduler | Delayed and Repeating Task Scheduling | Defines delayed, repeating, cancellation, and shutdown scheduling APIs and their implementation. | Executor placement or durable job scheduling. | `PROPOSED` |
| `tavall-registry` | tavall-registry | Thread-Safe Keyed Registries | Provides an abstract map-backed keyed registry with indexed and cache variants and collection views. | Domain registry semantics owned by consumers. | `PROPOSED` |
| `tavall-custom-enum-java` | tavall-custom-enum-java | Extensible Typed Enum Library | Provides the low-level `CustomEnum`/`EnumValues` library for typed, dynamically registered enum-like values. | Consumer enum families and their registration. | `PROPOSED` |
| `tavall-java-tools` | Tavall Java Tools | Shared Java Tool Aggregate | Records direct Git submodule pointers for the shared Tavall Java tool repositories. | The source, releases, and review of any individual tool. | `PROPOSED` |
| `tavall-java-utils` | Tavall Java Utils | Java Utility Aggregate | Records the canonical source revisions of standalone low-level Java utility repositories as submodule pointers. | The implementation of any utility. | `PROPOSED` |
| `tavall-jdk` | Tavall JDK | Versioned JDK Source Ownership | Owns versioned OpenJDK source and runtime customization, with Java 25 isolated in its own source/build module. | Consumer build policy or a shared default toolchain decision. | `PROPOSED` |
| `tavall-cli` | Tavall CLI Framework | Command-Line Mechanics Framework | Owns command routing, argument and option parsing, validation, help rendering, output formatting, and CLI execution lifecycle. | Domain subcommands or business logic, which stay with their owning systems. | `PROPOSED` |
| `tavall-test-suite-tools` | Tavall Test Suite Tools | Executable Architecture Rules | Packages reusable architecture rules and a Gradle plugin that turn written architecture policy into tests consumers can execute. | The written architecture policy itself, which `tavall-docs` owns. | `PROPOSED` |
| `tavall-filesystem` | Tavall Filesystem | Immutable Byte Storage and Verification | Stores, verifies, publishes, and materializes immutable digest-bound bytes through independently controlled ZFS and NFS features. | Version selection, the durable CURRENT authority, leases or fencing policy, pointer schemas, database reconciliation, Cloud topology. | `PROPOSED` |
| `tavall-networking` | Tavall Networking | Reusable Networking System | Owns the reusable networking API, implementation, and test-suite modules. | Cloud-specific network state and provider integration. | `PROPOSED` |
| `tavall-mc` | Tavall MC | Minecraft Product and Plugin Composition | Owns the Minecraft product behavior, API, verification, and lifecycle Gradle modules plus the unified first-party runtime artifact composition. | Paper/Velocity host processes, deployment infrastructure, or the Project Novus MMO authority. | `PROPOSED` |
| `tavall-mc-paper` | Tavall MC Paper | Paper Fork and Patch Queue | Stores the reproducible pinned Paper commit, fork build configuration, Tavall-owned patch queue, and validation tooling. | A generated or vendored Paper source tree. | `PROPOSED` |
| `tavall-minecraft-framework` | Tavall Minecraft Framework | Reusable Minecraft Framework Source | Owns the standalone reusable source and artifacts for Minecraft framework capabilities extracted from Tavall MC. | Minecraft product behavior, module lifecycle, runtime composition, consumer acceptance. | `PROPOSED` |
| `tavall-mc-anticheat` | Tavall Minecraft Anti-Cheat | Gameplay Heuristics and Replay | Owns gameplay heuristics, observation evidence, and deterministic replay against authoritative server state. | Packet-level protocol filtering, ban verdicts, or resource-pack identity extraction. | `PROPOSED` |
| `tavall-mc-packet-filter` | Tavall Minecraft Packet Filter | Application Protocol Legality Filtering | Owns Minecraft application-protocol legality and abuse filtering through typed filter, verdict, and evidence contracts. | Linux nftables/NFQUEUE, DDoS mitigation, version translation, or gameplay cheat verdicts. | `PROPOSED` |
| `tavall-mc-bot-testing` | Tavall MC Bot Testing | Simulated-Player Test Harness | Owns Minecraft simulated-player, protocol, black-box, and end-to-end bot testing and its scenario suites. | Mechanically enforceable architecture rules or Minecraft product behavior. | `PROPOSED` |
| `tavall-web` | Tavall Web | Shared Spring Web Runtime | Owns the reusable Java Web platform, the executable Spring composition, and the host for product presentation modules. | Product page composition, gameplay, persistence, or purchase fulfillment. | `PROPOSED` |
| `tavall-web-account` | Tavall Account | Account and Identity Pages | Owns the account.tavall.org browser pages for one Tavall identity, passwordless sign-in, linked identities, and organizations. | Identity authority, credentials storage, or product-local passwords. | `PROPOSED` |
| `tavall-web-ai-chat` | Tavall AI Chat Web | AI Chat Presentation Module | Owns Tavall AI Chat browser presentation, including the Work Graph and decision-card pages, against host-authorized snapshots. | Employee/Department contracts, authorization, host lifecycle, or deployed routes. | `PROPOSED` |
| `tavall-web-blog` | Tavall Web Blog | Blog Pages Module | Owns the Tavall blog browser pages as a module consumed by the shared Web runtime. | Blog content authority or hosting. | `PROPOSED` |
| `tavall-web-contractors` | Tavall Web Contractors | Contractors Presentation Module | Owns Tavall Contractors page composition, canonical CSS/assets, and browser route vocabulary. | Contractors marketplace, job, matching, escrow, checkout, or talent-domain authority. | `PROPOSED` |
| `tavall-web-dashboard` | tavall-web-dashboard | Reusable Dashboard Shell | Owns transport-neutral Forge dashboard pages and the reusable, composable dashboard shell for Tavall Web products. | Service health, product data, or product dashboard ownership. | `PROPOSED` |
| `tavall-web-docs` | Tavall Web Docs | Documentation Browser Pages | Owns the docs.tavall.org browser pages as a product module of the shared Web runtime. | Documentation authority, which stays with the owning documentation repositories. | `PROPOSED` |
| `tavall-web-mcp` | Tavall Web MCP | Hosted MCP HTTP Entry Point | Owns the Spring MVC HTTP host boundary and route declaration for the public MCP surface. | MCP protocol or domain execution, which stay with the owning backend service. | `PROPOSED` |
| `tavall-web-ops` | Tavall Ops | Private Operations Control Plane | Owns the private operations HTTP host and browser presentation with operator grants, short-lived sessions, per-request authorization, and audited recovery operations. | Hardware-backed credential verification (recorded as unavailable), password fallback, or a claimed runtime deployment. | `PROPOSED` |
| `tavall-web-workflows` | tavall-web-workflows | Workflows Browser Pages | Presents Tavall Workflows pages through the shared Web runtime. | Workflow repositories, releases, runners, or the marketplace. | `PROPOSED` |
| `tavall-commerce` | Tavall Commerce | Commerce Transaction Runtime | Owns checkout, paid orders, subscriptions, receipts, settlement records, creator ledger entries, refunds, disputes, and signed entitlement verification. | Payment-provider APIs, which Tavall Pay owns; browser presentation. | `PROPOSED` |
| `tavall-pay` | Tavall Pay | Payment Provider Platform | Owns the payment platform API, separate Stripe/PayPal provider APIs and implementations, and their test suite. | Minecraft, web controllers, stores, ledgers, player entitlement, or order authority. | `PROPOSED` |
| `tavall-pay-mc` | Tavall Pay Minecraft | Minecraft Payment Adapters | Owns Minecraft player-UUID-aware payment contracts and adapters that map player/order identity onto Tavall Pay provider operations. | Payment processing, money ledgers, or granting items after a browser redirect. | `PROPOSED` |
| `tavall-pay-web` | Tavall Pay Web | Web Payment Event Adapters | Owns verified processor event handoff into web commerce through typed, provider-scoped evidence. | HTTP controllers, signature-free processing, or reward/entitlement granting. | `PROPOSED` |
| `tavall-content` | Tavall Content | Idea-to-Publication Content Pipeline | Turns authorized sources into evidence-backed content candidates, editorial decisions, artifacts, publishing work, and measurable outcomes. | External analytics, payment/settlement, identity, or runner placement. | `PROPOSED` |
| `tavall-content-personal` | Tavall Content Personal | Private Campaign Radar | Keeps personal source access, channel profiles, preferences, and fit assessments inside a private consumer boundary of Tavall Content. | Any personal-radar runtime, browser connector, or dashboard route in the recorded state. | `PROPOSED` |
| `tavall-analytics` | Tavall Analytics | Evidence-First Analytics | Owns evidence-first analytics, first-party telemetry, creator intelligence, attribution, and Minecraft market observability. | Resource/execution profiling reasoning (see §8.2), or the products whose events it analyzes. | `NEEDS_OWNER_REVIEW` |
| `tavall-workflows` | Tavall Workflows | Installable Automation Marketplace | Owns publisher, product, release, installation, update, entitlement, and execution-receipt semantics for installable workflows. | Payment verification and settlement, runner placement and execution, or identity. | `PROPOSED` |
| `tavall-open-harness` | Tavall Open Harness | CLI Process Host and PTY Runtime | Hosts CLI processes behind Tavall's own process lifecycle and PTY boundary on Linux. | Model execution, Cloud placement, or a second scheduler. | `PROPOSED` |
| `tavall-ai-chat` | Tavall AI Chat | Chat Goal and Session Libraries | Owns the chat product's goal/session contracts, orchestration integration, project/thread relationships, and execution/UX state projections. | Canonical model execution, provider quotas, placement, identity, task state, or deployed Chat service behavior. | `PROPOSED` |
| `tavall-github-bot` | Tavall GitHub Bot | GitHub Check Publication | Owns GitHub App installation discovery, repository and pull-request reconciliation, exact-head fencing, and GitHub Check publication. | CI/CD policy, build policy, Cloud scheduling, environments, Executors, or runtime placement. | `PROPOSED` |
| `tavall-discord` | Tavall Discord | Reusable Discord Platform | Owns the generic Discord client integration and in-process lifecycle boundaries for Tavall products. | Consumer domain behavior, persistence, permissions, messages, or authoritative state. | `PROPOSED` |
| `tavall-project-novus` | Project Novus | Cross-Platform Persistent MMO | Owns the combined connected MMO vision and its cross-platform composition. | The Minecraft implementation in Tavall MC, or the independent Kingdoms product/system documents. | `PROPOSED` |
| `tavall-affiliates` | Tavall Affiliates | Affiliate Program Backend | Owns affiliate business authority for inbound partner referrals and outbound Tavall-operated affiliate monetization through typed API contracts. | Browser presentation, payouts performed by provider systems, or identity authority. | `PROPOSED` |
| `TavallMonoRepo` | TavallMonoRepo | Cross-Repository Aggregate Checkout | Records child repositories as Git submodule pointers for cross-project discovery and integration validation. | Any child repository's source, branches, PRs, releases, or documentation. | `PROPOSED` |
| `TavallContractors` | Tavall Contractors | Contractor Marketplace Application | Owns the contractor marketplace and intake application with a Spring Boot web application and an internal API module. | Browser presentation owned by `tavall-web-contractors`; escrow or payment authority. | `PROPOSED` |
| `function-catalog` | Tavall Function Catalog | Typed Function Catalog and MCP Server | Provides typed Java function definitions, scoped discovery and invocation, provider integrations, and an executable MCP server. | Agent orchestration policy, model execution, or Cloud placement. | `PROPOSED` |
| `tavall-rating-glicko2` | Tavall Rating Glicko-2 | Glicko-2 Rating Calculations | Provides rating, rating-deviation, and volatility profiles plus two-player outcome and rating-period calculation. | Matchmaking, ladders, or persistence of rating history. | `PROPOSED` |
| `workflow-deepai-code-runner` | workflow-deepai-code-runner | Headless DeepAI Worker Pool Workflow | Packages a releasable Tavall Workflow that runs the DeepAI Code desktop app headless on a Linux host as a local AI worker pool. | The Workflows runner contract, model-provider quotas, or Cloud placement. | `PROPOSED` |
| `tavall-ai-memory` | Tavall AI Memory | AI Memory Documentation Surface | Records memory documentation and resources for Tavall AI without owning an executable runtime or a second provider graph. | Provider-neutral Java memory contracts and durable write semantics, owned by the AI runtime memory module. | `PROPOSED` |
| `UnrealEngine` | UnrealEngine | Vendored Unreal Engine Source | Holds upstream Unreal Engine source under its own EULA as a private reference checkout. | Any Tavall-owned capability, contract, or product boundary. | `NEEDS_OWNER_REVIEW` |
| `TavallCouriers` | Tavall Couriers | Courier Platform Application | Carries the Tavall couriers platform and Spring webview application. | Recorded only from the organization repository description; see §8.4. | `NEEDS_OWNER_REVIEW` |
| `Webstore` | Webstore | Multi-Tenant Commerce Platform | Carries the multi-tenant commerce platform with admin and control-plane modules. | Recorded only from the organization repository description; Commerce transaction authority is not confirmed. | `NEEDS_OWNER_REVIEW` |

## 5. Prototype / experimental repositories

Classification `PROTOTYPE / EXPERIMENTAL` means bootstrap-only, design-only, experiment, or placeholder state. A descriptor here must never imply available capability.

### 5.1 Bootstrap, design-only, and experiment repositories

| Technical name | Public name | Descriptor | What it does | Does not own | Status |
| --- | --- | --- | --- | --- | --- |
| `tavall-mc-studio` | Tavall Minecraft Studio | Minecraft Authoring Studio | Holds the design and progression bootstrap for a unified Minecraft authoring and validation product. | The Studio application source or a hosted runtime, neither of which exists in the recorded state. | `PROPOSED` |
| `tavall-web-mc-studio` | Tavall Web Minecraft Studio | Studio Browser Bootstrap | Holds the bootstrap for browser-facing Minecraft Studio presentation. | Any interactive hosted Builder UI, which is not implemented in the recorded state. | `PROPOSED` |
| `tavall-ai-browser` | Tavall AI Browser | Task-Scoped Browser Capabilities | Records the migration foundation for typed, task-scoped browser capability contracts with least-authority policy. | A deployed or authenticated browser, identity, credentials, or node execution. | `PROPOSED` |
| `TAL` | TAL | Typed Agent Language Compiler | Holds the accepted Phase 0 architecture for a compiler-first, strongly typed DSL that reuses symbols from existing languages. | Any implemented compiler, Gradle frontend, language runtime, source bridge, or working CLI. | `PROPOSED` |
| `tavall-hytale-resource-game` | Tavall Hytale Resource Game | Hytale Resource Game Slice | Carries the Hytale resource, kingdom, and gameplay vertical slice plus the control-plane runtime and Minecraft adapters in its Gradle build. | A released Hytale product or the Minecraft product authority. | `PROPOSED` |
| `CustomMinecraftServer` | Custom Minecraft Server | Experimental Minecraft Server Runtime | Proves that an own networking, session, and protocol pipeline can accept real Java and Bedrock clients without a Bukkit/Paper/Velocity/Fabric/Forge/Minestom host. | Paper compatibility, plugin hosting, or Tavall MC product behavior. | `PROPOSED` |
| `HyRhythm` | HyRhythm | Hytale Rhythm Game Plugin | Carries a Gradle-built Hytale Java rhythm-game plugin and server-patch experiments. | A released Hytale product or shared framework ownership. | `PROPOSED` |
| `MCRSpeedrun` | MCRSpeedrun | Speedrun Platform Prototype | Carries an in-development solo speedrun platform with game, store, and web modules and a rating-system prototype. | A productionised platform, live store, or the shared rating library. | `PROPOSED` |
| `hytale-bots` | hytale-bots | Hytale Bot Harness | Carries a TypeScript bot harness, protocol codec, and scenario runner for Hytale. | Any released product surface. | `PROPOSED` |
| `minecraft-bot` | minecraft-bot | Minecraft Bot Protocol Experiments | Carries Node.js Minecraft bot and protocol experiments. | The canonical Minecraft bot-testing harness, which Tavall MC Bot Testing owns. | `PROPOSED` |
| `workflow-java-architecture-check` | Java Architecture Check | Java Architecture Check Workflow | Defines a runnable Tavall Workflow that checks Java source in a repository worktree against CLI architecture rules with an advisory quick gate. | A new execution format, the Workflows runner contract, or a deployed runtime. | `PROPOSED` |

### 5.2 Placeholder repositories without recorded implementation

These repositories have no README on the current default branch, an empty README stub, or a README-only boundary with no recorded source. They are listed so that no repository is silently skipped; none may be used as an authority. See §8.4.

| Technical name | Public name | Descriptor | Recorded state | Status |
| --- | --- | --- | --- | --- |
| `tavall-NLEWs` | tavall-NLEWs | NLEW Name Placeholder | Empty README stub; the implemented NLEW library is `tavall-nlew`. | `NEEDS_OWNER_REVIEW` |
| `tavall-marketing` | tavall-marketing | Marketing Placeholder | Empty README stub; no source or recorded ownership. | `NEEDS_OWNER_REVIEW` |
| `tavall-orgs` | tavall-orgs | Organizations Placeholder | Empty README stub; no source or recorded ownership. | `NEEDS_OWNER_REVIEW` |
| `tavall-networking-tools` | tavall-networking-tools | Networking Tools Placeholder | Empty README stub; no source or recorded ownership. | `NEEDS_OWNER_REVIEW` |
| `tavall-roblox` | tavall-roblox | Roblox Boundary Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-ventures` | tavall-ventures | Ventures Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-web-ventures` | tavall-web-ventures | Ventures Web Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-biz` | tavall-biz | Business Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-labs` | tavall-labs | Labs Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-web-labs` | tavall-web-labs | Labs Web Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-web-biz` | tavall-web-biz | Business Web Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |
| `tavall-support` | tavall-support | Support Placeholder | No README and no recorded source. | `NEEDS_OWNER_REVIEW` |

## 6. Archived / legacy repositories

`ARCHIVED` is taken from GitHub's archived flag. `LEGACY` marks a repository that is still readable and not archived, but whose own README records that it is superseded, compatibility-only, or a bare boundary that must not be extended.

| Technical name | Public name | Descriptor | What it does now | Classification | Status |
| --- | --- | --- | --- | --- | --- |
| `tavall-web-mc` | tavall-web-mc | Minecraft Browser Presentation (superseded) | Holds the former Minecraft/Novus browser presentation module; archived on GitHub. | `ARCHIVED` | `NEEDS_OWNER_REVIEW` |
| `tavall-web-content` | tavall-web-content | Content Studio Browser Presentation (superseded) | Holds the former Content Studio browser presentation; archived on GitHub. | `ARCHIVED` | `NEEDS_OWNER_REVIEW` |
| `tavall-web-commerce` | tavall-web-commerce | Commerce Browser Presentation (superseded) | Holds the former organization-aware commerce browser pages; archived on GitHub. | `ARCHIVED` | `NEEDS_OWNER_REVIEW` |
| `tavall-web-cloud` | tavall-web-cloud | Cloud Browser Surface (superseded) | Holds the former reserved cloud.tavall.org browser surface; archived on GitHub. | `ARCHIVED` | `NEEDS_OWNER_REVIEW` |
| `tavall-web-affiliates` | Tavall Web Affiliates | Affiliates Browser Presentation (superseded) | Holds the former presentation-only affiliate browser module; archived on GitHub while its README still describes the surface. | `ARCHIVED` | `NEEDS_OWNER_REVIEW` |
| `tavall-web-qa-ARCHIVED` | Tavall Web QA | QA Board Browser Presentation (consolidated) | Records the QA Board browser product consolidated into `tavall-qa` as its web frontend module; archived on GitHub. | `ARCHIVED` | `PROPOSED` |
| `tavall-ai-chat-broken-20261105` | tavall-ai-chat-broken-20261105 | Unwritable AI Chat Copy (replaced) | Records a repository made non-updatable on 2026-11-04 and replaced by `tavall-ai-chat`. | `LEGACY` | `PROPOSED` |
| `tavall-web-store-tools` | tavall-web-store-tools | Legacy Payment Compatibility Source | Holds superseded store payment provider source whose typed implementations moved to Tavall Pay; new provider logic must not be added there. | `LEGACY` | `PROPOSED` |
| `tavall-content-tools` | Tavall Content Tools | Content Tools Boundary Stub | Records a README-only repository boundary; the `tavall-content-tools` Gradle module is built inside `tavall-content`. | `LEGACY` | `NEEDS_OWNER_REVIEW` |
| `Tavall-Talent-and-Contractors-` | Tavall Talent and Contractors | Contractors Naming Legacy | Holds only a README and repository Git-workflow guidance under a legacy name; defines no source or build module. | `LEGACY` | `NEEDS_OWNER_REVIEW` |

## 7. Verified module and tool inventory

Module rows name only modules verified from the owning `settings.gradle*` include list or the owning README module table on the current default branch. Public name repeats the technical name when no distinct public name exists; inventing a brand for a Gradle project is explicitly prohibited.

### 7.1 Tavall AI (`tavall-ai`)

| Technical name | Descriptor | What it does | Status |
| --- | --- | --- | --- |
| `tavall-ai-bootstrap` | Agent package discovery and composition | Provides reusable composition contracts and discovery for agent packages and runtime capability modules. | `PROPOSED` |
| `tavall-ai-runtime` | Executable agent runtime composition | Composes the installed agent packages and runtime capabilities into the executable process module. | `PROPOSED` |
| `tavall-ai-runtime-project-context` | Project-context request contracts | Provides provider-neutral project-context request, item, provenance, and normalized-bundle contracts. | `PROPOSED` |
| `tavall-ai-runtime-model-execution` | Single-model invocation and budgets | Provides provider-neutral single-model invocation, capability-view scoping, and execution-budget enforcement. | `PROPOSED` |
| `tavall-ai-runtime-memory` | Memory semantics and retrieval | Provides provider-neutral memory semantics, authority scopes, exact-state caching, and retrieval contracts. | `PROPOSED` |
| `tavall-ai-runtime-distributed-execution` | Authorized execution-target routing | Routes among already authorized execution targets and provider attempts. | `PROPOSED` |
| `tavall-ai-runtime-codex` | Codex model-process adapter | Adapts Codex model/process invocation behind host-provided workspace and isolation boundaries. | `PROPOSED` |
| `tavall-ai-runtime-agy` | agy model-process adapter | Adapts the agy (Antigravity) model/process path behind the same host boundaries as the other runtime adapters. | `NEEDS_OWNER_REVIEW` |
| `tavall-ai-runtime-claude` | Claude model-process adapter | Adapts the Claude model/process path behind the same host boundaries as the other runtime adapters. | `NEEDS_OWNER_REVIEW` |
| `tavall-ai-runtime-remote-bridge` | Remote runtime bridge | Bridges execution to a remote host through the runtime capability boundary. | `NEEDS_OWNER_REVIEW` |
| `tavall-ai-runtime-spi` | Runtime capability interface | Defines the service-provider interface that runtime capability modules implement. | `NEEDS_OWNER_REVIEW` |
| `tavall-ai-cloud-host` | Cloud-host runtime integration | Integrates AI runtime execution with the authorized Cloud host boundary. | `NEEDS_OWNER_REVIEW` |
| `tavall-ai-browser` | Task-scoped browser capability | Provides typed, task-scoped browser capability contracts with least-authority policy. | `PROPOSED` |
| `tavall-agent-orchestration` | Work coordination role package | Coordinates specialized work inside an already placed top-level model session. | `PROPOSED` |
| `tavall-agent-ledger` | Ledger role package | Owns the agent package that records authorized ledger work on GitHub Issues and the QA Task Board. | `PROPOSED` |
| `tavall-agent-pr-workflow` | Pull-request workflow role package | Owns the agent package for typed Git delivery and pull-request workflow. | `PROPOSED` |
| `tavall-agent-pr-review` | Review role package | Owns independent exact-head review and acceptance-gap assessment. | `PROPOSED` |
| `tavall-agent-pr-reconciliation` | Reconciliation role package | Reconciles repository, pull-request, ownership, and migration state before more work is added. | `PROPOSED` |
| `tavall-agent-e2e-validation` | End-to-end validation role package | Validates exact heads in an authorized realistic development runtime. | `PROPOSED` |
| `tavall-agent-code-architecture` | Structural architecture role package | Owns explicitly approved structural migrations and systemic architecture repairs. | `PROPOSED` |
| `tavall-agent-documentation` | Documentation role package | Produces durable documentation grounded in accepted implementations and concrete evidence. | `PROPOSED` |
| `tavall-agent-builder` | Builder role package | Provides builder planning, critique, repair, and simulation for the Project Novus Builder platform. | `PROPOSED` |
| `tavall-agent-recovery` | Recovery role package | Provides evidence-based health inspection and low-risk authorized recovery coordination. | `PROPOSED` |
| `tavall-agent-web` | Web product role package | Provides evidence-based web product design quality and product-intelligence workflows. | `PROPOSED` |

### 7.2 Tavall Cloud (`tavall-cloud`)

| Technical name | Descriptor | What it does | Status |
| --- | --- | --- | --- |
| `tavall-cloud-api` | Cloud control contracts | Owns the typed control-plane contracts consumed by Cloud capabilities and clients. | `PROPOSED` |
| `tavall-cloud-node` | Node agent and inventory | Owns the node-side agent, managed-service inventory, and node observations. | `PROPOSED` |
| `tavall-cloud-executor` | Durable execution surface | Owns Executor selection, lifecycle, and execution hosting for authorized agent, console, and CI work. | `PROPOSED` |
| `tavall-cloud-executor-host-operations` | Executor host operations | Owns host-side operational actions for Executor hosting. | `NEEDS_OWNER_REVIEW` |
| `tavall-cloud-jobs` | Durable scheduled jobs | Owns durable job scheduling, including the bounded organization check-in cadence. | `PROPOSED` |
| `tavall-cloud-runtime` | Cloud runtime packaging | Composes the Cloud process identities without collapsing their architectural owners. | `PROPOSED` |
| `tavall-cloud` | Cloud composition module | Composes Cloud capabilities into the deployable Cloud composition. | `PROPOSED` |
| `tavall-cloud-mcp` | Cloud MCP control plane | Serves the Cloud-hosted MCP/control-plane surface. | `PROPOSED` |
| `tavall-cloud-cli` | Cloud command surface | Owns Cloud subcommands on the shared CLI framework. | `PROPOSED` |
| `tavall-cloud-ai-broker-protocol` | AI broker protocol | Owns the protocol contracts for brokered AI execution requests. | `NEEDS_OWNER_REVIEW` |
| `tavall-cloud-github-runner` | GitHub runner integration | Integrates GitHub runner execution with Cloud placement. | `PROPOSED` |
| `tavall-cloud-kubernetes` | Kubernetes provider | Provides the Kubernetes execution provider integration. | `PROPOSED` |
| `tavall-cloud-docker` | Docker provider | Provides the Docker execution provider integration. | `PROPOSED` |
| `tavall-cloud-database-docker` | Database container provisioning | Provides containerised database provisioning for Cloud environments. | `NEEDS_OWNER_REVIEW` |
| `tavall-cloud-web-frontend` | Cloud web frontend | Owns shared Cloud web frontend construction used by Cloud surfaces. | `NEEDS_OWNER_REVIEW` |
| `tavall-connector` | Connector boundary | Owns the connector boundary used by Cloud-connected clients. | `NEEDS_OWNER_REVIEW` |
| `tavall-cloud-test-suite` | Cloud verification suite | Holds Cloud verification modules, including the CD acceptance fixture. | `PROPOSED` |

### 7.3 Tavall CI (`tavall-ci`)

| Technical name | Descriptor | What it does | Status |
| --- | --- | --- | --- |
| `tavall-ci-api` | CI caller contracts | Owns typed CI caller and CD operation contracts and results. | `PROPOSED` |
| `tavall-ci-definition` | CI definition interpretation | Owns source-controlled `.tavallci` definitions, validation, and plans. | `PROPOSED` |
| `tavall-ci-versioning` | Source and release identity | Owns source, release, build-policy, and resolution identities. | `PROPOSED` |
| `tavall-ci-evidence` | Typed checks and evidence | Owns typed checks, failure classes, runtime identity, and evidence. | `PROPOSED` |
| `tavall-ci-dependencies` | Exact-source dependency modes | Owns explicit exact-source and immutable-artifact dependency modes. | `PROPOSED` |
| `tavall-ci-source-aggregation` | Exact-source aggregation | Owns exact-source aggregate manifests. | `PROPOSED` |
| `tavall-ci-gradle` | Gradle composite planning | Owns Gradle composite planning, substitutions, and lock-resolution inputs. | `PROPOSED` |
| `tavall-ci-cd` | Frozen delivery and promotion | Owns frozen delivery, readiness, promotion, and rollback semantics. | `PROPOSED` |
| `tavall-ci-cloud` | Cloud CD provider adapter | Provides the non-executable Cloud deployment provider adapter. | `PROPOSED` |
| `tavall-gh` | Typed GitHub CLI wrapper | Provides the typed official GitHub CLI wrapper for CI-owned source and check semantics. | `PROPOSED` |
| `tavall-ci-service` | CI/CD composition service | Composes CI/CD with typed service registration, orchestration, and provider binding. | `PROPOSED` |
| `tavall-ci-cli` | CI command surface | Owns `.tavallci` commands that call the typed CI caller service. | `PROPOSED` |
| `tavall-cd-cli` | Delivery command surface | Owns typed stored-run deployment and router rollback commands. | `PROPOSED` |
| `tavall-ci-test-suite` | CI verification suite | Holds regular Gradle verification for CI modules. | `PROPOSED` |

### 7.4 Shared Java libraries and small systems

| Technical name | Descriptor | What it does | Status |
| --- | --- | --- | --- |
| `tavall-di` | Dependency wiring library | Single library module owning dependency discovery, metadata, lifecycle, typed access, and delegation. | `PROPOSED` |
| `tavall-database-core-contracts` | Database builder and query contracts | Owns shared builder, configuration, and query contracts. | `PROPOSED` |
| `tavall-database-core` | Database shared core | Owns cross-provider database core behavior. | `PROPOSED` |
| `tavall-database-postgres` | PostgreSQL provider | Provides the PostgreSQL database provider. | `PROPOSED` |
| `tavall-database-mongo` | MongoDB provider | Provides the MongoDB database provider. | `PROPOSED` |
| `tavall-database-redis` | Redis provider | Provides the Redis database provider. | `PROPOSED` |
| `tavall-database-qdrant` | Qdrant provider | Provides the Qdrant database provider. | `PROPOSED` |
| `tavall-database-test-suite` | Database verification suite | Holds cross-provider database verification. | `PROPOSED` |
| `tavall-filesystem-api` | Filesystem contracts | Owns filesystem contracts and records with no provider dependencies. | `PROPOSED` |
| `tavall-filesystem` | Filesystem fan-in and lifecycle | Owns consumer-facing fan-in, lifecycle cascade, DI composition, and atomic primitives. | `PROPOSED` |
| `tavall-filesystem-zfs` | ZFS materialization feature | Provides verified immutable releases on an observed ZFS dataset. | `PROPOSED` |
| `tavall-filesystem-nfs` | NFS publication feature | Provides fenced immutable generation publication and verified reads on an observed NFS export. | `PROPOSED` |
| `tavall-filesystem-test-suite` | Filesystem verification suite | Holds behavior, composition, boundary, and architecture checks for filesystem modules. | `PROPOSED` |
| `tavall-networking-api` | Networking contracts | Owns reusable networking contracts. | `PROPOSED` |
| `tavall-networking` | Networking implementation | Owns the reusable networking implementation. | `PROPOSED` |
| `tavall-networking-test-suite` | Networking verification suite | Holds networking behavior and boundary verification. | `PROPOSED` |
| `tavall-nlew-api` | NLEW identity contracts | Owns typed NLEW identity and reference contracts. | `PROPOSED` |
| `tavall-nlew` | NLEW domain library | Owns NLEW records, policies, relationships, and fenced generation transitions. | `PROPOSED` |
| `tavall-nlew-test-suite` | NLEW verification suite | Holds NLEW behavior and boundary verification. | `PROPOSED` |
| `tavall-qa-api` | QA task contracts | Owns typed task, progress, and verification contracts. | `PROPOSED` |
| `tavall-qa-system` | QA authority system | Owns the mapped-JPA task board and QA verification behavior. | `PROPOSED` |
| `tavall-qa-cli` | QA command surface | Owns QA subcommands on the shared CLI framework. | `PROPOSED` |
| `tavall-qa-web-frontend` | QA board web frontend | Owns the QA Board browser presentation consolidated from the archived web QA repository. | `PROPOSED` |
| `tavall-qa-test-suite` | QA verification suite | Holds QA system and contract verification. | `PROPOSED` |
| `workflows-api` | Marketplace contracts | Owns workflow marketplace and owner-boundary contracts with no runtime. | `PROPOSED` |
| `workflows-system` | Marketplace system | Owns marketplace and installation behavior above the contracts. | `NEEDS_OWNER_REVIEW` |
| `workflows-cli` | Workflow command surface | Owns workflow subcommands on the shared CLI framework. | `NEEDS_OWNER_REVIEW` |
| `tavall-workflows-web-frontend` | Workflows web frontend | Owns shared Workflows web frontend construction. | `NEEDS_OWNER_REVIEW` |
| `tavall-main-harness` | Main process harness | Hosts CLI processes with lifecycle, PTY I/O, and detach/reattach. | `PROPOSED` |
| `tavall-security-harness` | Security harness | Provides the security-scoped harness for hosted process execution. | `NEEDS_OWNER_REVIEW` |
| `tavall-jdk-25` | Java 25 JDK build | Owns the Java 25 OpenJDK source and runtime customization build. | `PROPOSED` |
| `tavall-cli-api` | CLI contracts | Owns the typed CLI contracts consumed by owning command surfaces. | `PROPOSED` |
| `tavall-ai-chat-api` | Chat goal and session contracts | Owns typed goal, session, project, and thread contracts. | `PROPOSED` |
| `tavall-ai-chat-system` | Chat integration system | Owns orchestration integration and execution/UX state projections. | `PROPOSED` |
| `tavall-web-ops` | Operations browser presentation | Owns bounded Ops browser presentation and typed Ops values/contracts. | `PROPOSED` |
| `tavall-web-ops-runtime` | Operations HTTP host | Owns the independently executable private Ops host and its authorization boundary. | `PROPOSED` |
| `tavall-mc-anticheat-api` | Anti-cheat contracts | Owns immutable gameplay observation, mechanics-profile, evidence, and heuristic contracts. | `PROPOSED` |
| `tavall-mc-anticheat-system` | Anti-cheat heuristics | Owns the heuristic and observation system over authoritative server state. | `PROPOSED` |
| `tavall-mc-anticheat-replay-system` | Deterministic replay | Owns deterministic replay of observed gameplay evidence. | `PROPOSED` |
| `tavall-mc-anticheat-test-suite` | Anti-cheat verification suite | Holds anti-cheat contract and behavior verification. | `PROPOSED` |
| `tavall-mc-packet-filter-api` | Packet filter contracts | Owns typed filter, verdict, and evidence contracts. | `PROPOSED` |
| `tavall-mc-packet-filter-system` | Packet filter chain | Owns the deterministic filter chain and connection, phase, and rate checks. | `PROPOSED` |
| `tavall-mc-packet-filter-test-suite` | Packet filter verification suite | Holds the packet-filter behavioral contract suite. | `PROPOSED` |
| `minecraft-framework-core` | Minecraft framework foundation | Owns reusable Minecraft UI, screen, asset, and action foundations. | `PROPOSED` |
| `minecraft-framework-game` | Minecraft game framework | Owns reusable Minecraft game-side framework behavior. | `NEEDS_OWNER_REVIEW` |
| `tavall-pay-api` | Payment contracts | Owns provider identity and verified notification contracts. | `PROPOSED` |
| `tavall-pay-stripe-api` | Stripe contracts | Owns the Stripe provider contracts. | `PROPOSED` |
| `tavall-pay-stripe` | Stripe provider | Owns Stripe payments, refunds, customer methods, and signature verification. | `PROPOSED` |
| `tavall-pay-paypal-api` | PayPal contracts | Owns the PayPal provider contracts. | `PROPOSED` |
| `tavall-pay-paypal` | PayPal provider | Owns PayPal approval/capture, refunds, OAuth, and remote signature verification. | `PROPOSED` |
| `tavall-pay-test-suite` | Payment verification suite | Holds payment platform and provider verification. | `PROPOSED` |
| `tavall-pay-mc-api` | Minecraft payment contracts | Owns player-UUID-aware payment contracts. | `PROPOSED` |
| `tavall-pay-mc-adapter` | Minecraft payment adapter | Maps player/order identities onto Tavall Pay provider operations. | `PROPOSED` |
| `tavall-pay-mc-test-suite` | Minecraft payment verification | Covers player/order correlation and rejection behavior. | `PROPOSED` |
| `tavall-pay-web-api` | Web payment contracts | Owns verified processor event handoff contracts to web commerce. | `PROPOSED` |
| `tavall-pay-web-adapter` | Web payment adapter | Injects provider clients and maps valid events into provider-scoped evidence. | `PROPOSED` |
| `tavall-pay-web-test-suite` | Web payment verification | Covers invalid/valid event filtering and API surface. | `PROPOSED` |
| `tavall-discord-api` | Discord contracts | Owns JDA-free client, feature, event, gateway-intent, and lifecycle contracts. | `PROPOSED` |
| `tavall-discord-data` | Discord data routing | Owns typed data requests/results, handler registration, and routing. | `PROPOSED` |
| `tavall-discord-jda` | JDA binding | Provides the JDA-backed implementation of the Discord contracts. | `PROPOSED` |
| `tavall-discord-runtime` | Discord runtime | Owns the in-process Discord client runtime and lifecycle. | `PROPOSED` |
| `tavall-discord-minecraft` | Minecraft Discord integration | Provides the Minecraft-side Discord integration. | `PROPOSED` |
| `tavall-discord-host` | Discord host composition | Composes Discord modules into a host composition. | `NEEDS_OWNER_REVIEW` |
| `tavall-rating-glicko2` | Glicko-2 rating engine | Single module owning rating profiles and rating-period calculation. | `PROPOSED` |
| `tavall-architecture-tests` | Architecture rule set | Provides the executable architecture rule modules and Gradle plugin entry points. | `PROPOSED` |
| `ai-core` | Function catalog core | Provides the shared typed function-definition and catalog core. | `PROPOSED` |
| `agent-runtime` | Agent runtime functions | Provides agent-runtime function definitions in the catalog. | `PROPOSED` |
| `codex-agent-provider` | Codex function provider | Provides Codex-backed function provider integration. | `PROPOSED` |
| `openai-sdk` | OpenAI SDK binding | Provides the OpenAI SDK function binding. | `NEEDS_OWNER_REVIEW` |
| `claude-sdk` | Claude SDK binding | Provides the Claude SDK function binding. | `NEEDS_OWNER_REVIEW` |
| `gemini-sdk` | Gemini SDK binding | Provides the Gemini SDK function binding. | `NEEDS_OWNER_REVIEW` |
| `mcp-server` | Catalog MCP server | Serves catalog functions through an executable MCP server. | `PROPOSED` |
| `internal-contractor-api` | Contractors internal API | Owns the internal contractor intake and scope API. | `PROPOSED` |
| `spring-webview` | Contractors Spring web application | Provides the Contractors Spring Boot web application surface. | `PROPOSED` |

### 7.5 Module coverage gaps in this pass

The following active repositories carry large module graphs whose individual module responsibilities are not re-derived here. Their repository-level row above is the descriptor, and the module-level gap is recorded rather than silently omitted:

| Repository | Modules included on the current default branch | Recorded gap |
| --- | --- | --- |
| `tavall-content` | About 30, including content AI, client, app, runtime, tools, ffmpeg, open-cv, TikTok/yt-dlp integrations, and the auto-account/auto-post feature families | Module-level descriptors not derived in this pass |
| `tavall-mc` | About 40, including product, NMS, kingdom, lobby, FFA, achievements, cosmetics, backend, resource-admin, and resource-pack projects | Module-level descriptors not derived in this pass |
| `tavall-analytics` | About 24, including api, core, storage, reporting, ai, content, attribution, experiments, first-party, Minecraft market, commerce, discord, mock, app, and web | Module-level descriptors blocked by §8.2 |
| `tavall-commerce` | Single module `tavall-commerce`, owned by the repository row | Covered by the repository row |
| `tavall-web` | Platform modules `tavall-web-api`, `tavall-web-app`, `tavall-web-frontend`, `-frontend-spring`, `-frontend-codegen`, `-frontend-gradle`, and the test suite | Covered by the repository row; module rows to be added when the platform README table is stabilized |
| `tavall-affiliates` | `tavall-affiliates` plus shared library composites | Covered by the repository row |

## 8. Owner-review flags and recorded conflicts

### 8.1 `tavall-nlew` descriptor "Multi-Level Dynamic Sandbox" — blocked

The third-pass candidate descriptor for `tavall-nlew` is recorded as **`NEEDS_OWNER_REVIEW`** and must not be published in its current wording.

| Conflict | Source | Effect |
| --- | --- | --- |
| Ephemeral sandbox execution is retired and must not be reintroduced as a default | [TAVALL_TERMINOLOGY.md](TAVALL_TERMINOLOGY.md) §1 "Executor": the canonical lifecycle is `DURABLE` shared execution with bounded `TEMPORARY` overflow only; "Ephemeral sandbox execution is retired and must not be reintroduced as a default." | "Sandbox" in a published descriptor would reintroduce retired sandbox-era terminology. |
| No Agent may introduce sandbox-era terminology for ordinary work | [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) §9 item 9 "Durable Executor Execution Only" | A descriptor is publication text; publishing "Sandbox" as the mental model conflicts with the accepted rule. |
| Sandbox-era accounts and grants are retired | [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md) "Executor lifecycle" | Reinforces that "sandbox" no longer describes any current execution concept. |
| `tavall-nlew` owns topology and policy, not enforcement | `tavall-nlew` README | The repository provides typed identities, records, policies, and fenced generation transitions and has no runtime of its own. |
| Enforcement belongs to Cloud and the Executor contract | `tavall-cloud` README; [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md) | Isolation, placement, and execution must never be attributed to the NLEW library. |

The issue text itself already separates positioning from enforcement ("The phrase is positioning, **not** a claim that the NLEW library itself enforces isolation"). That separation is insufficient for publication because the word "Sandbox" is the retired execution term, not merely an imprecise one.

Working candidate for owner decision (not approved, not applied): `tavall-nlew` → **Typed Environment Topology Library**. Supporting evidence: the repository README describes a reusable domain library for Nodes, Lanes, Environments, and Workspaces with typed identities, records, policies, and fenced Environment generation transitions, and states that it has no runtime of its own.

Corroborating repository fact: the local October snapshot of `tavall-cloud` still contains a `tavall-cloud-local-sandbox` directory, while the current default-branch `settings.gradle.kts` include list no longer includes that project. This is consistent with the retired sandbox model and is the reason no entry in this inventory advertises "sandbox" as an execution surface.

### 8.2 `tavall-profiling` does not exist — Analytics and Profiling split must be preserved

The third-pass candidate table lists "Tavall Profiling (`tavall-profiling`, identity/status to verify)" with the descriptor "Resource & Execution Observatory".

| Check | Result |
| --- | --- |
| `gh api "repos/TavallStudios/tavall-profiling"` | HTTP 404 — repository not found |
| Organization-wide repository search for `tavall-profiling` | Zero results |
| `TavallStudios` repository inventory | No profiling repository exists under any similar name |

Consequences recorded here:

- No descriptor can be assigned to a repository that does not exist. The candidate is **`NEEDS_OWNER_REVIEW`** at the organization level: either the repository is planned and will need a source-of-truth row when created, or the capability is owned by an existing repository that must be named explicitly.
- The **collection-versus-reasoning split must be preserved**. `tavall-analytics` owns evidence-first analytics, first-party telemetry, creator intelligence, attribution, and market observability. A "Resource & Execution Observatory" descriptor describes reasoning over execution/resource evidence, which is not Analytics' recorded ownership. Folding that descriptor into `tavall-analytics` would misattribute a capability.
- Because the reported owner is unverified, `tavall-analytics` is recorded as `NEEDS_OWNER_REVIEW` rather than `PROPOSED`: its candidate descriptor "Evidence-First Analytics" is supportable from its own README, but the neighbouring Profiling candidate cannot be resolved without the owner naming the real owner of resource/execution observability.

### 8.3 `tavall-ai-browser` Environment wording — reviewed, no conflict

The `tavall-ai-browser` README describes task-scoped Environments (EPHEMERAL, MUTABLE, DEDICATED, ISOLATED) with SYSTEM resources. Because Environment lifecycle is NLEW-owned and execution is Cloud/Executor-owned, this inventory's descriptor ("Task-Scoped Browser Capabilities") deliberately describes only the capability contracts and claims no isolation, sandbox, or execution ownership. Recorded so the omission is a decision, not an oversight.

### 8.4 Repositories needing an owner decision before publication

| Repository | Conflict | Required decision |
| --- | --- | --- |
| `tavall-profiling` | Does not exist; candidate descriptor "Resource & Execution Observatory" | Name the real owner of resource/execution profiling, or confirm the planned repository and its boundary. |
| `tavall-analytics` | Candidate descriptor may absorb the unverified Profiling capability | Confirm Analytics remains collection/evidence ownership and does not absorb execution/resource reasoning. |
| `tavall-nlew` | Candidate descriptor "Multi-Level Dynamic Sandbox" conflicts with the retired sandbox model | Approve replacement wording that describes topology/policy ownership only. |
| `tavall-web-mc`, `tavall-web-content`, `tavall-web-commerce`, `tavall-web-cloud`, `tavall-web-affiliates` | Archived on GitHub, but their READMEs still describe current product ownership; `tavall-web-workflows`, `tavall-web-account`, `tavall-web-blog`, `tavall-web-docs`, `tavall-web-mcp`, `tavall-web-contractors`, `tavall-web-dashboard`, and `tavall-web-ai-chat` remain unarchived | Name the current owner of each archived surface, and confirm whether the remaining `tavall-web-*` repositories are the canonical presentation owners. |
| `tavall-web-qa` | The repository no longer exists under that name: it is archived as `tavall-web-qa-ARCHIVED` and its README records consolidation into `tavall-qa` as `tavall-qa-web-frontend`. The local October checkout still presents it as current. | Confirm the archived row is the only record and that the local checkout is retired. |
| `tavall-web-affiliates` | Archived, while `tavall-affiliates` README still names it as the browser presentation owner. | Confirm the current affiliate presentation owner. |
| `tavall-web-store-tools` | Recorded as legacy payment compatibility; existing Stripe code in `tavall-web-app` is still described as the live legacy implementation. | Confirm the removal gate and whether the legacy descriptor may be published as-is. |
| `tavall-content-tools`, `Tavall-Talent-and-Contractors-`, `tavall-docs-private` | README-only or legacy-named boundaries with no source | Confirm intended disposition: keep as boundary records, convert to a source owner, or archive. |
| `tavall-NLEWs`, `tavall-marketing`, `tavall-orgs`, `tavall-networking-tools`, `tavall-roblox`, `tavall-ventures`, `tavall-web-ventures`, `tavall-biz`, `tavall-labs`, `tavall-web-labs`, `tavall-web-biz`, `tavall-support` | Empty README stub or no README at all; ownership and intent unrecorded | Record intended owner and disposition, then re-classify. |
| `TavallCouriers`, `Webstore` | No README on the default branch; only the organization description is available | Add an owning README before publishing any descriptor. |
| `tavall-scheduler` | Its own README still labels the implementation unfinished and the API experimental | Confirm whether the descriptor may be published while the implementation is labelled experimental. |
| `TavallMonoRepo`, `tavall-java-tools`, `tavall-java-utils` | Aggregate pointer repositories; "What it does" must never be read as source ownership | Confirm aggregate-only wording is acceptable for publication. |
| `UnrealEngine` | Third-party upstream source under the Unreal EULA, not a Tavall-owned capability | Confirm the repository is retained and how it should be described externally. |
| `tavall-ai` runtime adapters (`-agy`, `-claude`, `-remote-bridge`, `-spi`, `-cloud-host`) and several Cloud/Workflows/Discord modules | Descriptors in §7 are derived from module name and owning-repository context; no per-module README claim was verified in this pass | Verify per module, then promote from `NEEDS_OWNER_REVIEW` to `PROPOSED`. |

## 9. Coverage summary

### 9.1 Repository classification

| Classification | Count | Notes |
| --- | --- | --- |
| `ACTIVE` | 64 | Repository carries accepted or in-progress ownership for its stated responsibility. |
| `PROTOTYPE / EXPERIMENTAL` | 23 | 11 bootstrap/design/experiment repositories plus 12 placeholder repositories. |
| `ARCHIVED / LEGACY` | 10 | 6 GitHub-archived repositories plus 4 readable legacy/placeholder boundaries. |
| **Total** | **97** | Matches `gh api --paginate "orgs/TavallStudios/repos?per_page=100"` exactly. |

### 9.2 Descriptor status

| Status | Repositories | Modules |
| --- | --- | --- |
| `APPROVED` | 0 | 0 |
| `REVIEWED` | 0 | 0 |
| `PROPOSED` | 72 | 110 |
| `NEEDS_OWNER_REVIEW` | 25 | 19 |
| `STALE` | 0 | 0 |
| **Total** | **97** | **129** |

`STALE` is zero because no descriptor has been published yet: the status is reserved for a published descriptor that later conflicts with its owner. The staleness that would otherwise be recorded lives in §8.4, where a checkout or README description conflicts with the repository's current GitHub state.

### 9.3 Readiness projection

| Measure | Value |
| --- | --- |
| Repositories with a groundable "What it does" sentence | 85 of 97 (those with a README on the current default branch) |
| Repositories groundable only from the organization description | 2 (`TavallCouriers`, `Webstore`) |
| Repositories with no recorded intent | 10 (empty stub or absent README) |
| Blocking owner decisions | 15 rows in §8.4 |
| Published descriptors | 0 |

## 10. What this projection does not do

- It does not authorize, approve, or publish any descriptor.
- It does not rename any repository, module, Gradle project, package, or artifact.
- It does not replace an owning README, Design/Technical document, Progression document, or Deployment document.
- It does not track implementation or review work; GitHub Issues and the QA Task Board remain the ledger.
- It does not claim that a `PROPOSED` or `NEEDS_OWNER_REVIEW` capability is implemented, available, or deployed.
- It does not advertise a sandbox, namespace, container, or per-command Executor as an execution model.

## DOC TODO:

### Document next steps

- [ ] Resolve the fifteen owner decisions in §8.4, then re-derive the affected rows and their statuses.
- [ ] Derive module-level descriptors for `tavall-content`, `tavall-mc`, `tavall-analytics`, `tavall-web`, and `tavall-affiliates` (§7.5) and remove the gap rows.
- [ ] Verify the name-derived module descriptors flagged in §8.4 against each module README, then promote them to `PROPOSED`.
- [ ] Re-run the enumeration after any repository is created, archived, renamed, or made public, and refresh §9's counts in the same change.
- [ ] Replace the four duplicate-name repository rows once an owning README exists for `TavallCouriers` and `Webstore` and a disposition is recorded for the placeholder repositories.

### System next steps

- No product, runtime, or repository implementation work is owned by this projection.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/TAVALL_DESCRIPTOR_INVENTORY.md` | 2026-11-26 | `#156` descriptor standardization. |
| Notion | `NOT_APPLICABLE` | — | 2026-11-26 | Quality projection; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/TAVALL_DESCRIPTOR_INVENTORY.md` | — | `#156` descriptor standardization. | Created the derived descriptor inventory and coverage projection over the 97-repository organization inventory, verified module rows, and open owner-review conflicts. |

</details>
