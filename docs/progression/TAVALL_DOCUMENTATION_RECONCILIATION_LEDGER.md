# Tavall Documentation Reconciliation Ledger

> **Document Type:** Governance / Reconciliation Ledger  
> **Source of Truth For:** Cross-repository documentation ownership, canonical authority mapping, historical evidence preservation, and durable environment resolution  
> **Canonical Owner:** `TavallStudios/tavall-docs`  
> **Branch:** `working/progression-consolidation-20260921`  
> **Tracking PR:** `TavallStudios/tavall-docs#24`  
> **Last Audited Date:** 2026-09-23  

---

## 1. Authority Model & Governance Principles

### Organization-Wide Authority (`TavallStudios/tavall-docs`)
`TavallStudios/tavall-docs` is the sole canonical written authority for organization-wide engineering and documentation policy across all 54 `TavallStudios` repositories. This includes:
- Architecture policy, taxonomy, and system guidelines (`docs/quality/code-architecture/*`);
- Quality standards and documentation taxonomy (`docs/quality/DOCUMENTATION_STANDARDS.md`, `docs/quality/DOCUMENT_TYPES.md`);
- Git workflows, staging PR conventions, and branching policies (`docs/quality/GIT_WORKFLOW.md`);
- CI/CD engineering policy and verification boundaries (`docs/quality/CI_CD.md`);
- Canonical documentation routing index (`docs/quality/DOCUMENT_ROUTING.yml`);
- Shared Java tools consumer guidance and platform conventions (`docs/quality/code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md`);
- Master progression rollup and cross-system status (`docs/progression/TAVALL_PROGRESSION_OVERVIEW.md`).

Product and platform repositories consume and link to these policies; they must not fork them into local copies.

### Repository-Specific Authority
Each active repository owns its own:
- GENERAL / product overview where applicable;
- Repository / component architecture;
- Design contracts (Draft / Final);
- Technical contracts (Draft / Final);
- Progression / Evidence documents;
- Operations specific to that repository;
- Migration / extraction provenance;
- Product-specific QA and test checklists;
- Repository-specific staging descriptor and runbooks.

Duplicate detection is governed by `logical responsibility/topic + document type + lifecycle + owner + source state`, not mere filename similarity.

### Critical Progression Requirement
All maintained Progression/Evidence documents across the entire organization mandate **chronologically reconcilable milestones**. Every meaningful historical milestone must carry a real chronological date in `YYYY-MM-DD` format recovered from Git history, pull requests, commits, and verified evidence:
```text
- **YYYY-MM-DD - [Milestone Title] (`[commit-sha]`, PR #[number])**
  - Details and changes introduced.
  - State: `MERGED_PRODUCTION` | `MERGED_STAGING` | `VALID_UNMERGED_PR` | `HISTORICAL_EVIDENCE` | `SUPERSEDED` | `BLOCKED`
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
   - `/srv/dev-storage/workspaces/shared-dependencies/**` (immutable build cache only, never canonical editable workspace)
   - Bootstrap backups (`/var/lib/tavall-cloud/bootstrap-backups`)
   - Temporary directories (`/tmp`, `/var/tmp`)
   - Legacy `/srv/workspace` abandoned copies.

---

## 2. Canonical DURABLE Environment Inventory & Classification

| Repository | Canonical GitHub Source | Canonical Branch | Canonical DURABLE Env ID | Canonical Local Checkout | Environment Status | Operational Verification State |
| --- | --- | --- | --- | --- | --- | --- |
| `TavallStudios/tavall-docs` | `tavall-docs.git` | `main` | `env-43f14931` (`43f14931-0ebe-4d90-b516-a34b20080052`) | `/srv/workspace/tavall-docs-current` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` (Local git/CI verified) |
| `TavallStudios/tavall-cloud` | `tavall-cloud.git` | `main` | `env-fe721951` (`fe721951-c5a6-4b48-b128-8fbcfe750bc8`) | `/srv/workspace/tavall-cloud` | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-mc` | `tavall-mc.git` | `main` | `env-081a137e` (`081a137e-db07-476d-8619-f1f0fd5190f0`) | `/srv/workspace/tavall-project-novus` / `/home/ubuntu/tavall-mc` | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-minecraft-framework` | `tavall-minecraft-framework.git` | `main` | `env-9c4a23d9` (`9c4a23d9-5b0f-4109-8926-9fb839835d2b`) | Standalone Clone | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-web` | `tavall-web.git` | `main` | `env-f7e9a31f` (`f7e9a31f-2b72-4a02-8337-5d512d87592a`) | `/srv/workspace/tavall-web` | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-discord` | `tavall-discord.git` | `staging/platform` | `env-583fae32` (`583fae32-3bc2-491f-b421-1c9fcc040b5a`) | Standalone Clone | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-di` | `tavall-di.git` | `staging/platform` | `env-12d58fc2` (`12d58fc2-bd5a-4e08-a01b-25018004d526`) | `/srv/workspace/tavall-di` | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/Tavall-Architecture-Tests` | `Tavall-Architecture-Tests.git` | `main` | `env-96dd6c18` (`96dd6c18-03aa-4802-a438-e3c12f30826a`) | `/srv/workspace/Tavall-Architecture-Tests` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` (Gradle plugin verified) |
| `TavallStudios/tavall-ci` | `tavall-ci.git` | `staging/platform` | Platform Staging | `/srv/workspace/tavall-ci` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` |
| `TavallStudios/tavall-content` | `tavall-content.git` | `main` | Standalone Feature Staging | Standalone Clone | `REGISTERED_CANONICAL` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` |
| `TavallStudios/tavall-mc-paper` | `tavall-mc-paper.git` | `main` | Standalone Pinned Fork | `/home/ubuntu/tavall-mc-paper` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` |
| `TavallStudios/tavall-mc-bot-testing` | `tavall-mc-bot-testing.git` | `main` | Subtree Extraction | `/home/ubuntu/tavall-mc-bot-testing` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` |
| `TavallStudios/tavall-ai` | `tavall-ai.git` | `main` | Plugin Staging | `/srv/workspace/tavall-ai-staging-aware-agents` | `REGISTERED_CANONICAL` | `OPERATIONALLY_VERIFIED` |

> [!NOTE]
> All paths under `/srv/dev-storage/workspaces/shared-dependencies/**` are classified as `BUILD_CACHE_NOT_CANONICAL`. They are immutable build-time dependencies, not active workspaces or documentation authority.
> Environment operations attempting JSON mutation in `/srv/dev-storage/environments/` encounter the known `STALE_VERSION` write lock, accurately recorded above as `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION`.

---

## 3. Master Documentation Reconciliation Ledger

| Repository | Logical Responsibility | Document Type | Lifecycle | Canonical Owner | Canonical Production Path | Production Branch | Production SHA | Staging/PR Evidence | Evidence State | Historical Variants | Canonical DURABLE Env | Environment Verification State | Disposition | Remaining Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `tavall-docs` | Organization CI/CD Policy | Policy | Final | `tavall-docs` | `docs/quality/CI_CD.md` | `main` | `978f1ec` | PR #2, PR #23 | `MERGED_PRODUCTION` | 2 | `env-43f14931` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-docs` | Documentation Routing Index | Index / Policy | Final | `tavall-docs` | `docs/quality/DOCUMENT_ROUTING.yml` | `main` | `978f1ec` | PR #14, PR #2 | `MERGED_PRODUCTION` | 1 | `env-43f14931` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-docs` | Documentation Standards | Policy | Final | `tavall-docs` | `docs/quality/DOCUMENTATION_STANDARDS.md` | `main` | `978f1ec` | Incorporates historical `DOC_DESIGN_RULES.MD` | `MERGED_PRODUCTION` | 2 | `env-43f14931` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-docs` | Documentation Types & Taxonomy | Policy | Final | `tavall-docs` | `docs/quality/DOCUMENT_TYPES.md` | `main` | `978f1ec` | Formally supersedes historical rules | `MERGED_PRODUCTION` | 2 | `env-43f14931` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-docs` | Git Workflow Policy | Policy | Final | `tavall-docs` | `docs/quality/GIT_WORKFLOW.md` | `main` | `978f1ec` | Central authority for 24 consumer repos | `MERGED_PRODUCTION` | 24 | `env-43f14931` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Consumer repos routed |
| `tavall-mc-paper` | Paper Fork Progression | Progression | Historical / Final | `tavall-mc-paper` | `docs/progression/PAPER_FORK_PROGRESSION.md` | `main` | `ff8d6a0` | PR #4 | `MERGED_PRODUCTION` | 2 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-mc-paper` | Combat Baseline | Architecture | Final | `tavall-mc-paper` | `docs/COMBAT_BASELINE.md` | `main` | `0cbdb3a` | PR #3 | `MERGED_PRODUCTION` | 1 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-mc-paper` | Upstream Sync Contract | Contract | Final | `tavall-mc-paper` | `UPSTREAM.md` | `main` | `0cbdb3a` | PR #3 | `MERGED_PRODUCTION` | 1 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `Tavall-Architecture-Tests` | Architecture Tests Progression | Progression | Final | `Tavall-Architecture-Tests` | `docs/progression/ARCHITECTURE_TESTS_PROGRESSION.md` | `main` | `b0e8aac` | PR #11 | `MERGED_PRODUCTION` | 1 | `env-96dd6c18` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `Tavall-Architecture-Tests` | Architecture Enforcement Contract | Contract | Final | `Tavall-Architecture-Tests` | `README.md` | `main` | `3e71575` | PR #10 | `MERGED_PRODUCTION` | 2 | `env-96dd6c18` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-mc-bot-testing` | Bot Testing Progression | Progression | Final | `tavall-mc-bot-testing` | `docs/progression/BOT_TESTING_PROGRESSION.md` | `main` | `39aa5a1` | PR #3 | `MERGED_PRODUCTION` | 1 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-mc-bot-testing` | Bot Testing Migration Provenance | Migration | Final | `tavall-mc-bot-testing` | `MIGRATION.md` | `main` | `791acb6` | Byte-for-byte tree identity | `MERGED_PRODUCTION` | 1 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-discord` | Discord Platform Progression | Progression | Final | `tavall-discord` | `docs/progression/DISCORD_PLATFORM_PROGRESSION.md` | `staging/platform` | `8c5012a4` | PR #4 | `MERGED_STAGING` | 2 | `env-583fae32` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Ready for main promotion |
| `tavall-discord` | Discord Platform Architecture | Architecture | Final | `tavall-discord` | `docs/architecture/DISCORD_PLATFORM_ARCHITECTURE.md` | `staging/platform` | `8c5012a4` | PR #4 | `MERGED_STAGING` | 2 | `env-583fae32` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Ready for main promotion |
| `tavall-minecraft-framework` | Minecraft Framework Progression | Progression | Final | `tavall-minecraft-framework` | `docs/progression/MINECRAFT_FRAMEWORK_PROGRESSION.md` | `main` | `7ef34d9` | PR #6 | `MERGED_PRODUCTION` | 2 | `env-9c4a23d9` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-web` | Web Runtime Progression | Progression | Final | `tavall-web` | `docs/TAVALL_WEB_RUNTIME_PROGRESSION.md` | `main` | `6310679` | PR #38 | `MERGED_PRODUCTION` | 4 | `env-f7e9a31f` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-web` | Website System Progression | Progression | Final | `tavall-web` | `docs/website/WEBSITE_SYSTEM_PROGRESSION.md` | `main` | `af1f74c` | PR #39 | `MERGED_PRODUCTION` | 2 | `env-f7e9a31f` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-web` | Web Store System Design | Design | Final | `tavall-web` | `docs/website/WEB_STORE_SYSTEM_DESIGN.md` | `main` | `af1f74c` | PR #39 | `MERGED_PRODUCTION` | 2 | `env-f7e9a31f` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Browser UX authority |
| `tavall-cloud` | Cloud System Progression (4 trackers) | Progression | Final | `tavall-cloud` | `docs/**/PROGRESSION.md` | `main` | `c7d4ea5` | PR #393 | `MERGED_PRODUCTION` | 4 | `env-fe721951` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | All 4 trackers dated on main |
| `tavall-mc` | 46 System Progression Trackers | Progression | Final | `tavall-mc` | `docs/**/*_PROGRESSION.md` | `main` | `768f8b7` | PR #304 | `MERGED_PRODUCTION` | 46 | `env-081a137e` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | All 46 trackers dated on main |
| `tavall-mc` | Bot Testing URL Repair (7 docs) | Maintenance | Final | `tavall-mc` | `docs/**` | `main` | `593e4c33` | PR #303 | `MERGED_PRODUCTION` | 7 | `env-081a137e` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Complete on `main` |
| `tavall-mc` | Minecraft Web & Store Integration | Progression / Design | Final | `tavall-mc` | `docs/website/**` | `working/promote-novus-web-retirement-20260919` | `341d1013` | PR #290 | `VALID_UNMERGED_PR` | 2 | `env-081a137e` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | In-game command & fulfillment scope |
| `tavall-mc` | Selective Documentation Preflight | Architecture / Workflow | Final | `tavall-mc` | `AGENTS.md`, `docs/quality/**` | `working/selective-documentation-preflight` | `da8963f4` | PR #285 | `VALID_UNMERGED_PR` | 3 | `env-081a137e` | `UNVERIFIED_DUE_TO_CONTROL_STALE_VERSION` | `CANONICAL_CURRENT` | Rebased on main; unblocked |
| `tavall-ai` | AgentTaskManager Git Workflow | Architecture / Tooling | Final | `tavall-ai` | `docs/architecture/AGENT_TASK_MANAGER_GIT_WORKFLOW.md` | `main` | `4b55365` | PR #41 | `MERGED_PRODUCTION` | 2 | `/srv/workspace/tavall-ai-staging-aware-agents` | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | Complete on `main` |
| `Java Tools (9 repos)` | Standalone Workflow & Central Routing | Workflow / Architecture | Final | 9 Java Repos | `AGENTS.md`, `CONTRIBUTING.md`, `docs/quality/GIT_WORKFLOW.md` | `main` | `HEAD` | PRs #12, #10, #24, #15, #8, #8, #8, #9, #8 | `MERGED_PRODUCTION` | 27 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | All 9 repos merged to main |
| `Consumer Repos (15 repos)` | Central Git Workflow Routing | Workflow / Routing | Final | 15 Repos | `docs/quality/GIT_WORKFLOW.md` | default branches | `HEAD` | PRs in HyRhythm, MCRSpeedrun, etc. | `MERGED_PRODUCTION` | 15 | Standalone | `OPERATIONALLY_VERIFIED` | `CANONICAL_CURRENT` | All 15 consumer repos merged |

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

## 5. Verification and Maintenance

This ledger must be updated whenever:
1. A new standalone repository is extracted from a monorepo or product repository.
2. A staging or consumer cutover PR is promoted to `main`.
3. An environment retirement pass is executed after verifying all durable GitHub lineage.
4. A previously branch-only proposal or final draft is accepted into production.
