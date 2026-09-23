# Tavall Documentation Reconciliation Ledger

> **Document Type:** Governance / Reconciliation Ledger  
> **Source of Truth For:** Cross-repository documentation ownership, canonical authority mapping, historical evidence preservation, and durable environment resolution  
> **Canonical Owner:** `TavallStudios/tavall-docs`  
> **Branch:** `working/progression-consolidation-20260921`  
> **Tracking PR:** `TavallStudios/tavall-docs#24`  
> **Last Audited Date:** `2026-09-23`

---

## 1. Authority Model & Governance Principles

### Repository-Specific Authority
1. **GitHub for each repository is the canonical, persisted source of truth.**
2. There is **exactly one canonical DURABLE Tavall Cloud environment per repository** designated as the primary active development and documentation workspace.
3. Other environments, worktrees, and ephemeral workspaces represent historical evidence, branch-specific work, or temporary test execution. Their existence on disk does not grant them architectural or documentation authority.

### Organization-Wide Authority (`TavallStudios/tavall-docs`)
Tavall-wide engineering and architecture policies reside exclusively in `TavallStudios/tavall-docs`. This includes:
- Architecture policy, taxonomy, and system guidelines (`docs/quality/code-architecture/*`);
- Quality standards and documentation rules (`docs/quality/DOCUMENTATION_STANDARDS.md`, templates);
- Git workflows, staging PR conventions, and branching policies (`docs/quality/GIT_WORKFLOW.md`);
- CI/CD engineering policy and verification boundaries (`docs/quality/CI_CD.md`);
- Shared Java tools consumer guidance and platform conventions (`docs/quality/code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md`);
- Master progression rollup and cross-system status (`docs/progression/TAVALL_PROGRESSION_OVERVIEW.md`).

Product and platform repositories consume and link to these policies; they must not fork them into local copies.

### Critical Progression Rule
Every meaningful historical milestone in a `*_PROGRESSION.md` document must contain an explicit ISO date (`YYYY-MM-DD`), structured as:
```text
- **YYYY-MM-DD - description (<sha>, PR #<n>)**: Details...
```
Chronological ordering with exact SHA, PR, and branch lineage prevents older discovered caches from overwriting newer production evidence.

### Source-Selection Guardrails
Agentic and automated workers must follow a strict resolution ladder:
1. Identify the repository and remote (`git rev-parse --show-toplevel`, `git remote -v`).
2. Identify the active GitHub ref/SHA.
3. Resolve the canonical DURABLE environment for that repository.
4. Read canonical documentation from that environment.
5. Explicitly ignore and exclude the following paths from default documentation authority:
   - `.codex-worktrees`
   - `tavall-pr-campaign*`
   - Stale `developer-workspaces/work/*` caches
   - Immutable `shared-dependencies` build snapshots
   - Bootstrap backups (`/var/lib/tavall-cloud/bootstrap-backups`)
   - Temporary directories (`/tmp`, `/var/tmp`)
   - Legacy `/srv/workspace` abandoned copies.

---

## 2. Canonical DURABLE Environment Inventory

| Repository | Canonical GitHub Source | Canonical Branch | Canonical DURABLE Env ID | Canonical Local Checkout | Environment Status |
| --- | --- | --- | --- | --- | --- |
| `TavallStudios/tavall-docs` | `TavallStudios/tavall-docs.git` | `main` | `43f14931-0ebe-4d90-b516-a34b20080052` (`env-43f14931`) | `/srv/workspace/tavall-docs-current` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-cloud` | `TavallStudios/tavall-cloud.git` | `main` | `fe721951-c5a6-4b48-b128-8fbcfe750bc8` (`env-fe721951`) | `/srv/workspace/tavall-cloud` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-mc` | `TavallStudios/tavall-mc.git` | `main` | `081a137e-db07-476d-8619-f1f0fd5190f0` (`env-081a137e`) | `/home/ubuntu/tavall-mc` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-minecraft-framework` | `TavallStudios/tavall-minecraft-framework.git` | `main` | `9c4a23d9-5b0f-4109-8926-9fb839835d2b` (`env-9c4a23d9`) | `/srv/dev-storage/workspaces/shared-dependencies-...` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-web` | `TavallStudios/tavall-web.git` | `main` | `f7e9a31f-2b72-4a02-8337-5d512d87592a` (`env-f7e9a31f`) | `/srv/workspace/tavall-web` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-discord` | `TavallStudios/tavall-discord.git` | `staging/platform` | `583fae32-3bc2-491f-b421-1c9fcc040b5a` (`env-583fae32`) | Standalone Clone | ACTIVE_CANONICAL |
| `TavallStudios/tavall-di` | `TavallStudios/tavall-di.git` | `staging/platform` | `12d58fc2-bd5a-4e08-a01b-25018004d526` (`env-12d58fc2`) | `/srv/workspace/tavall-di` | ACTIVE_CANONICAL |
| `TavallStudios/Tavall-Architecture-Tests` | `TavallStudios/Tavall-Architecture-Tests.git` | `main` | `96dd6c18-03aa-4802-a438-e3c12f30826a` (`env-96dd6c18`) | `/srv/workspace/Tavall-Architecture-Tests` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-ci` | `TavallStudios/tavall-ci.git` | `staging/platform` | Active Platform Staging | `/srv/workspace/tavall-ci` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-content` | `TavallStudios/tavall-content.git` | `main` / PR #11 | Active Feature Staging | Standalone Clone | ACTIVE_CANONICAL |
| `TavallStudios/tavall-mc-paper` | `TavallStudios/tavall-mc-paper.git` | `main` | Pinned Standalone Fork | `/home/ubuntu/tavall-mc-paper` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-mc-bot-testing` | `TavallStudios/tavall-mc-bot-testing.git` | `main` | Pinned Subtree Extraction | `/home/ubuntu/tavall-mc-bot-testing` | ACTIVE_CANONICAL |
| `TavallStudios/tavall-ai` | `TavallStudios/tavall-ai.git` | `staging/plugin` | Portable Plugin Staging | `/srv/workspace/tavall-ai-staging-aware-agents` | ACTIVE_CANONICAL |

### Auxiliary & Secondary Environments Classification
- `77cf98b6-9616-46e9-8739-c1fc1f06778f` (`tavall-docs`): Active PR #25 (`working/nle-vocabulary-20260922`). Keep until PR #25 is merged.
- `0fb831fa-db6a-41ef-a94c-3a1e9374de92` (`tavall-mc`): Active PR #301 (`working/complete-minecraft-framework-extraction-20260920`). Keep until PR #301 is merged.
- `3ed86e38-b6a8-4be8-bc66-c82c46342061` (`tavall-web`): Active branch `working/web-frontend-consumer-plugin-20260922`. Keep until PR is merged.
- `415d97b1-0bd3-4daf-aded-942b56bfdf2c`, `7e47fc16-e397-4fe2-a2ae-c833d38fb5ce` (`tavall-web`): Historical recovery branches for Account Org Dashboard. Safe to retire once PR #38 lands on main.
- `01407c54-3156-4e39-ad3d-bed936500aed`, `043f3d44-93fd-4252-ba43-9a0a8e369b4a`, `23b84e94-89f7-4afc-80a0-363d9d45c3aa` (`Tavall-Architecture-Tests`): Historical bootstrap environments. Safe to retire; superseded by `96dd6c18`.
- `448d831f-b1da-45c7-8c3d-4edbe74554a7`, `aaefb643-2559-44ad-b614-56df6e9df043`, `cb08acbb-8ab6-477e-a437-cd4145768802` (`tavall-cloud`): Intermediate feature test environments. Safe to retire after verification.

---

## 3. Master Documentation Reconciliation Ledger

| Repository | Logical Document | Type | Historical Variants | Canonical Owner | Current Canonical Path | Latest Canonical Evidence | Historical Evidence Preserved | Action |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| `tavall-mc-paper` | Paper Fork Progression | Progression | 2 | `tavall-mc-paper` | `docs/progression/PAPER_FORK_PROGRESSION.md` | `ff8d6a0` (PR #4) | 2026-09-19 bootstrap, PR #1 extraction, PR #2 rename, PR #3 pinned 26.2 hard-fork workflow | `CANONICAL_CURRENT` |
| `tavall-mc-paper` | Combat Baseline | Architecture / Baseline | 1 | `tavall-mc-paper` | `docs/COMBAT_BASELINE.md` | `0cbdb3a` (PR #3) | Pinned Paper 26.2 build 125, movement/knockback/charge invariant | `CANONICAL_CURRENT` |
| `tavall-mc-paper` | Upstream Sync Contract | Contract | 1 | `tavall-mc-paper` | `UPSTREAM.md` | `0cbdb3a` (PR #3) | Stable build inspection script and promotion gates | `CANONICAL_CURRENT` |
| `Tavall-Architecture-Tests` | Architecture Tests Progression | Progression | 1 | `Tavall-Architecture-Tests` | `docs/progression/ARCHITECTURE_TESTS_PROGRESSION.md` | `b0e8aac` (PR #11) | 2026-09-07 bootstrap/import, PR #3/#6 executable gates, PR #7 suite boundary, PR #10 DI debt aggregation | `CANONICAL_CURRENT` |
| `Tavall-Architecture-Tests` | Architecture Enforcement Contract | Contract | 2 | `Tavall-Architecture-Tests` | `README.md` | `3e71575` (PR #10) | Executable Gradle plugin consumer model (`org.tavall.architecture-tests`) | `CANONICAL_CURRENT` |
| `tavall-mc-bot-testing` | Bot Testing Progression | Progression | 1 | `tavall-mc-bot-testing` | `docs/progression/BOT_TESTING_PROGRESSION.md` | `39aa5a1` (PR #3) | 2026-09-19 payload staging, 2026-09-20 extraction/import, PR #2 validation workflow | `CANONICAL_CURRENT` |
| `tavall-mc-bot-testing` | Bot Testing Migration Provenance | Migration | 1 | `tavall-mc-bot-testing` | `MIGRATION.md` | `791acb6` | Byte-for-byte tree identity: `bots/` (`075070bf`), `minecraft-bot-testing/` (`2ea26b53`) | `CANONICAL_CURRENT` |
| `tavall-mc` | Battle System Progression | Progression | 3 | `tavall-mc` | `docs/battles/BATTLE_SYSTEM_PROGRESSION.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | FFA System Progression | Progression | 9 | `tavall-mc` | `docs/pvp/FFA_SYSTEM_PROGRESSION.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | Currency System Progression | Progression | 2 | `tavall-mc` | `docs/currency/CURRENCY_SYSTEM_PROGRESSION.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | Building System Progression | Progression | 2 | `tavall-mc` | `docs/buildings/BUILDING_SYSTEM_PROGRESSION.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | Moderation & Support Operations | Operations | 3 | `tavall-mc` | `docs/discord/MODERATION_AND_SUPPORT_OPERATIONS.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | Novus Custom Entity Runtime | Architecture / Archive | 2 | `tavall-mc` | `docs/archives/custom-entities/NOVUS_CUSTOM_ENTITY_RUNTIME.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-mc` | UI Canvas Live Test Checklist | QA / Validation | 2 | `tavall-mc` | `docs/UI_CANVAS_LIVE_TEST_CHECKLIST.md` | `593e4c33` (PR #303) | Repaired corrupted tripled bot-testing URLs to canonical `tavall-mc-bot-testing` | `CANONICAL_CURRENT` |
| `tavall-content` | Multi-Account Publishing Queue Final Draft | Final Contract / Architecture | 3 | `tavall-content` | `docs/MULTI_ACCOUNT_PUBLISHING_QUEUE_FINAL_DRAFT.md` | `4d9bedc3` (PR #11) | Newer characterized state: PlatformConnection, PublishingPort, ContentStore, monotonic claim fence | `VALID_UNMERGED_WORK` |
| `tavall-ai` | Tavall AI Memory Runtime | Architecture | 4 | `tavall-ai` | `docs/architecture/TAVALL_AI_MEMORY_RUNTIME.md` | `a8964dcc` | Provider-neutral runtime module, authority-scoped supersession; supersedes branch-only drafts | `CANONICAL_CURRENT` |
| `tavall-ai` | Local Memory Embeddings / Write Consistency | Design / Spec | 4 | `tavall-ai` | `docs/architecture/TAVALL_AI_MEMORY_RUNTIME.md` | `a8964dcc` | Historical branch-only proposals superseded by runtime module `tavall-ai-runtime-memory` | `SUPERSEDED` |
| `tavall-ai` | Tavall AI Repository Architecture | Architecture | 2 | `tavall-ai` | `docs/ARCHITECTURE.md` | `main` | Distinct from Codex client architecture; covers portable plugin and agent roles | `CANONICAL_CURRENT` |
| `tavall-ai` | Codex Client Platform Architecture | Architecture | 1 | `tavall-ai` | `docs/codex-client-platform/ARCHITECTURE.md` | `main` | Distinct system contract for Codex client bridge/companion | `CANONICAL_CURRENT` |
| `tavall-ci` | CD Engine Architecture | Architecture | 2 | `tavall-ci` | `docs/architecture/CD.md` | `main` | Engine-specific implementation architecture for Tavall CI runner | `CANONICAL_CURRENT` |
| `tavall-ci` | Evidence Engine Architecture | Architecture | 2 | `tavall-ci` | `docs/architecture/EVIDENCE.md` | `main` | Storage and manifest collection internal mechanics for Tavall CI | `CANONICAL_CURRENT` |
| `tavall-docs` | Binding CI/CD Engineering Policy | Policy | 2 | `tavall-docs` | `docs/quality/CI_CD.md` | `24431cb6` (PR #23) | Cross-project CI/CD standards, `.tavallci` specification, promotion/rollback gates | `CANONICAL_CURRENT` |
| `tavall-di` | Tavall DI Final System Contract | Final Contract | 1 | `tavall-di` | `docs/TAVALL_DI_SYSTEM_FINAL.md` | `main` | Library runtime contract, metadata ownership, `@DelegatesTo` source lowerer | `CANONICAL_CURRENT` |
| `tavall-di` | Tavall DI Access Styles | Architecture / Guide | 2 | `tavall-di` | `docs/DI_ACCESS_STYLES.md` | `main` | Style rankings for `@DelegatesTo`, `DependencyAccess`, `DependencyMap` | `CANONICAL_CURRENT` |
| `tavall-docs` | Dependency Injection Architecture Policy | Policy | 1 | `tavall-docs` | `docs/quality/code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md` | `main` | Cross-project code architecture policy for DI and orchestration boundaries | `CANONICAL_CURRENT` |
| `tavall-discord` | Discord Platform Architecture | Architecture | 2 | `tavall-discord` | `docs/architecture/DISCORD_PLATFORM_ARCHITECTURE.md` | `main` | Reusable Java Discord platform decoupling API, Data, and JDA adapters | `CANONICAL_CURRENT` |
| `tavall-discord` | Discord Platform Progression | Progression | 2 | `tavall-discord` | `docs/progression/DISCORD_PLATFORM_PROGRESSION.md` | `8c5012a4` (PR #4) | Dated standalone extraction history; Tavall MC consumer cutover tracked in PR #284 | `CANONICAL_CURRENT` |
| `tavall-web` | Organization Unified Dashboard | Design | 2 | `tavall-web` | `docs/design/ORGANIZATION_UNIFIED_DASHBOARD.md` | `main` | Unified dashboard design across organization resources and account access | `CANONICAL_CURRENT` |
| `tavall-web` | Tavall Account Platform Contract | Final Contract / Design | 3 | `tavall-web` | `docs/design/TAVALL_ACCOUNT_PLATFORM.md` | `70d6533` | Canonical human Tavall Account / SSO / org identity; supersedes Novus final draft | `CANONICAL_CURRENT` |
| `tavall-web` | Web Surface Consolidation | Migration | 2 | `tavall-web` | `docs/migration/TAVALL_WEB_SURFACE_CONSOLIDATION.md` | `537ce60` | Maps Account, Contractors, Commerce, Content, Docs, and Admin surfaces | `CANONICAL_CURRENT` |
| `tavall-web` | Web Runtime Progression | Progression | 4 | `tavall-web` | `docs/TAVALL_WEB_RUNTIME_PROGRESSION.md` | `6310679` (PR #38) | Preserves 2026-09-11 extraction, 2026-09-18 Account contract, 2026-09-21 composite boundary | `CANONICAL_CURRENT` |
| `tavall-web` | Web Runtime Lane | Architecture / Operations | 2 | `tavall-web` | `docs/runtime-lanes/WEB.md` | `main` | Web HTTP runtime environment and actuator health requirements | `CANONICAL_CURRENT` |
| `tavall-minecraft-framework` | Minecraft Framework Progression | Progression | 2 | `tavall-minecraft-framework` | `docs/progression/MINECRAFT_FRAMEWORK_PROGRESSION.md` | `7ef34d9` (PR #6) | Dated standalone producer extraction; Tavall MC consumer cutover tracked in PR #301 | `CANONICAL_CURRENT` |
| Multi-Repo (9 repos) | Tavall Java Tools Architecture | Policy / Migration | 9 | `tavall-docs` | `docs/quality/code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md` | `tavall-docs#9` | Historical copies across 9 repos superseded by central Tavall Docs policy & standalone tool repos | `MOVE_TO_TAVALL_DOCS` |

---

## 4. Historical Novus / Tavall MC High-Risk Documents Disposition

| Historical Document Path | Type | Current Canonical Owner | Successor Path / Contract | Action | Disposition Summary |
| --- | --- | --- | --- | --- | --- |
| `docs/DOC_DESIGN_RULES.MD` | Quality / Policy | `tavall-docs` | `docs/quality/DOCUMENTATION_STANDARDS.md` | `SUPERSEDED` | Unified into canonical documentation standards and templates in `tavall-docs`. |
| `docs/builder/WORLD_VISION_FFA_VERIFICATION_CHECKPOINT.md` | QA / Validation | `tavall-mc-bot-testing` | `bots/ffa/` & Novus Builder Studio | `HISTORICAL_EVIDENCE_ONLY` | Preserved as historical E2E verification evidence for branch `build-repair-novus-runtime-discord-jar-acceptance-20260823`. |
| `docs/design/CROSS_PRODUCT_FIRST_JOIN_ACCEPTANCE_FINAL_DRAFT.md` | Design / Contract | `tavall-web` & `tavall-mc` | `tavall-web/docs/design/TAVALL_ACCOUNT_PLATFORM.md` & `tavall-mc` Lobby | `PROGRESSION_MERGED` | First-join onboarding moved to Web SSO; in-game lobby routing moved to Tavall MC framework. |
| `docs/minecraft/MINECRAFT_PACKET_FILTER_FINAL_DRAFT.md` | Design / Spec | `tavall-mc-paper` & `tavall-mc` | `tavall-mc-paper/docs/COMBAT_BASELINE.md` & `working/tj-224-minecraft-packet-filter-boundary` | `VALID_UNMERGED_WORK` | Valid packet filtering design; low-level packet hooks belong in `tavall-mc-paper`, gameplay policy in `tavall-mc`. |
| `docs/qa/TAVALL_PVP_QA_PROGRESSION.md` | Progression | `tavall-mc` | `docs/pvp/FFA_SYSTEM_PROGRESSION.md` | `SUPERSEDED` | Legacy redirect file superseded by specific PvP/FFA system progression documents. |
| `docs/qa/TAVALL_PVP_QA_SYSTEM_FINAL_DRAFT.md` | Final Contract | `tavall-mc-bot-testing` & `tavall-mc` | `tavall-mc-bot-testing/README.md` & `docs/pvp/FFA_SYSTEM_PROGRESSION.md` | `MERGED_INTO_SUCCESSOR` | Executable QA tests moved to `tavall-mc-bot-testing`; product progression tracked in `tavall-mc`. |
| `docs/qa/TAVALL_PVP_QA_SYSTEM_PROGRESSION.md` | Progression | `tavall-mc-bot-testing` & `tavall-mc` | `tavall-mc-bot-testing/docs/progression/BOT_TESTING_PROGRESSION.md` | `PROGRESSION_MERGED` | Merged into standalone bot testing progression and Tavall MC FFA progression. |
| `docs/runtime/TAVALL_RUNTIME_NAMING_MIGRATION.md` | Migration | `tavall-mc` | Repository Provenance (PR #153) | `HISTORICAL_EVIDENCE_ONLY` | Completed migration from Project Novus to Tavall MC; preserved as historical audit record. |
| `docs/superpowers/plans/2026-08-15-world-vision-ffa-verification-e2e.md` | Plan | `tavall-mc-bot-testing` | `bots/ffa/ffa-gameplay-pass.ts` | `HISTORICAL_EVIDENCE_ONLY` | Historical implementation plan fully executed; bot scenarios preserved in canonical bot-testing repo. |
| `docs/superpowers/specs/2026-08-13-staging-pr-workflow-design.md` | Spec / Process | `tavall-docs` | `docs/quality/GIT_WORKFLOW.md` | `SUPERSEDED` | Fully adopted into canonical Tavall Git workflow and `tavall-staging-pr-workflow` skill. |
| `docs/superpowers/specs/2026-08-15-minecraft-equivalent-simulation-kernel-design.md` | Spec | `tavall-mc-bot-testing` | `minecraft-bot-testing/src/support/minecraft-server-protocol.ts` | `MERGED_INTO_SUCCESSOR` | Implemented in standalone bot testing harness protocol support. |
| `docs/superpowers/specs/2026-08-16-builder-multimodal-vision-evidence-design.md` | Spec | Novus Builder Platform | Builder Platform & `tavall-agent-builder` | `HISTORICAL_EVIDENCE_ONLY` | Governs multimodal observation products in Builder Studio. |
| `docs/superpowers/specs/2026-08-18-ffa-complete-runtime-integration-design.md` | Spec | `tavall-mc` | `docs/pvp/FFA_SYSTEM_PROGRESSION.md` (PR #252) | `PROGRESSION_MERGED` | Completed production integration for FFA runtime; tracked in FFA progression. |
| `docs/superpowers/specs/2026-08-18-player-command-alias-wardrobe-permissions-design.md` | Spec | `tavall-mc` | `working/player-command-alias-wardrobe-permissions` | `PROGRESSION_MERGED` | Implemented on Tavall MC feature branch and merged into permissions/command progression. |
| `docs/superpowers/specs/2026-08-20-builder-studio-native-shell-design.md` | Spec | Novus Builder Platform | Project Novus Builder Studio | `HISTORICAL_EVIDENCE_ONLY` | Governs Builder Studio native shell architecture. |
| `docs/superpowers/specs/2026-08-21-builder-studio-web-admin-design.md` | Spec | `tavall-web` | `docs/migration/TAVALL_WEB_SURFACE_CONSOLIDATION.md` | `MERGED_INTO_SUCCESSOR` | Implemented in Tavall Web admin redesign. |
| `docs/web/TAVALL_ACCOUNT_FINAL_DRAFT.md` | Final Contract | `tavall-web` | `docs/design/TAVALL_ACCOUNT_PLATFORM.md` | `SUPERSEDED` | Superseded by canonical Tavall Web Account Platform contract; Minecraft links stay in Tavall MC. |
| `docs/web/TAVALL_WEB_PRODUCT_EXPERIENCE_FINAL_DRAFT.md` | Final Contract | `tavall-web` | `docs/TAVALL_WEB_RUNTIME_PROGRESSION.md` | `SUPERSEDED` | Superseded by Tavall Web runtime extraction and surface consolidation documents. |
| `docs/world/WORLD_SYSTEM_FINAL_DRAFT.md` | Final Contract | `tavall-mc` | `docs/world/WORLD_AND_SERVER_FLOW_PROGRESSION.md` | `VALID_UNMERGED_WORK` | Active world lifecycle contract on branch `working/restore-shared-world-lifecycle`. |

---

## 5. Active Migration Pull Requests Reference

| Domain / Platform | Standalone Producer PR | Consumer / Integration Cutover PR | Current Architecture State |
| --- | --- | --- | --- |
| **Paper Hard Fork** | `TavallStudios/tavall-mc-paper#4` | Standalone compile / artifact boundary | Paper 26.2 build 125 pinned; combat baseline frozen |
| **Architecture Tests** | `TavallStudios/Tavall-Architecture-Tests#11` | Adopted across repository test suites | Reusable Gradle plugin `org.tavall.architecture-tests` published |
| **Minecraft Bot Testing** | `TavallStudios/tavall-mc-bot-testing#3` | `TavallStudios/tavall-mc#303` (URL fix) | Standalone repository canonical; consumer doc links repaired |
| **Discord Platform** | `TavallStudios/tavall-discord#4` | `TavallStudios/tavall-mc#284` | Standalone platform extracted; consumer JDA cutover in PR #284 |
| **Minecraft Framework** | `TavallStudios/tavall-minecraft-framework#6` | `TavallStudios/tavall-mc#301` | Reusable framework published; consumer cutover in PR #301 |
| **Tavall Web & Account** | `TavallStudios/tavall-web#38` | `tavall-mc` link sessions preserved | Web owns human SSO/account platform; Web progression preserved |
| **Tavall Content** | `TavallStudios/tavall-content#11` | General content queue dispatch | Characterized publishing substrate; claim/side-effect fencing active |
| **Tavall Docs Master Rollup** | `TavallStudios/tavall-docs#24` | Organization-wide reference | Master progression overview & reconciliation ledger |

---

## 6. Verification and Maintenance

This ledger must be updated whenever:
1. A new standalone repository is extracted from a monorepo or product repository.
2. A staging or consumer cutover PR is promoted to `main`.
3. An environment retirement pass is executed after verifying all durable GitHub lineage.
4. A previously branch-only proposal or final draft is accepted into production.
