# Tavall CI/CD, Unified Gradle, and Deployment Rollout

> **Document type:** Progression / evidence snapshot
> **Snapshot date:** 2026-09-26
> **Scope:** Continue the Tavall CI/CD, unified Gradle, and service/runtime delivery rollout without replacing existing Tavall Cloud execution or deployment authorities.

This is a progression record, not a second architecture authority. The accepted boundary is in [`docs/quality/CI_CD.md`](../quality/CI_CD.md): repositories own build intent and project topology; Tavall CI owns build policy, planning, exact-source composition, evidence, and delivery identity; Cloud Executors own provisioning and execution; Tavall Cloud owns environments, service state, deployment materialization, routing, and runtime readiness.

## Documentation consolidation update — 2026-09-27

The repository-level documentation pass is complete for the priority repositories. These merges record documentation state only and do not establish runtime readiness.

| Repository | Documentation change | Main state |
| --- | --- | --- |
| `TavallStudios/tavall-ci` | PR #16 consolidated the CI system design, progression, and module references. | Merged to `main` at `3147a350f30d6c4004f9e6819400c7b9801564b1`. |
| `TavallStudios/tavall-cloud` | PRs #400–406 and #408–414 consolidated the system and module surfaces, retired Actions-route status, and progression metadata. PR #407 was a duplicate closed without merge. | Latest documentation merge is PR #414 at `cb9c293f2d6b7d6e4ea05aab51b57569848cb7ea`. |
| Cloud Progression Notion twin | Full content was synchronized from the merged GitHub progression after PR #414. | Verified at 2026-09-27 10:06 AM PDT. |

The GitHub Actions bridge is documented as retired from Tavall CI/CD. Its host runner and broker are disabled; Cloud PR #399 remains open against `staging/runtime` to remove the remaining Cloud Actions workflows. Tavall CI PR #17 defines the typed local caller through Cloud Executors, but remains Draft because the immutable CI runtime artifact has not yet been materialized and no exact-source live run is claimed.

Cloud CONTROL and storage are ready, but no DEVELOPMENT Environment is attached to this session. No exact-source live Executor run, artifact, DEVELOPMENT readiness, or STAGING readiness is claimed; documentation merges and static checks do not clear those gates.

## Current source and Environment identities

| Item | Exact identity |
| --- | --- |
| Tavall CI staging PR #15 | `bde88767288ab38df8a157818e923d11bb6537ae` on `staging/platform`, base `main`, Draft |
| Tavall CI feature source merged by PR #14 | `f3ad7942eb775a232e1e92a91a6baf101cac1444` on `working/unified-gradle-cicd-20260924`; staging merge `bde88767288ab38df8a157818e923d11bb6537ae` |
| Tavall Cloud PR #395 | `2738f25a9c8c979e1b25673d8734002f29eaf061` on `working/executor-canonical-architecture`, base `staging/runtime`, Draft |
| Architecture Tests dependency | `c0863bfe9e3ea38e4872eb295856e69bed30eb28` on `working/unified-ci-exact-artifact-versions-20260925` |
| Existing DEVELOPMENT Environment | `5848c5ff-a2a2-4da4-bd25-9cff8e558433` in lane `f75e1548-c7ab-470a-85aa-b38a770dae78` |
| Resolved exact source snapshot | `77f16b7bf0d9ac6e152d12c7e18d26f4bf4a157a831d9042ed474cdf316288ed` |
| DEVELOPMENT Environment policy | DURABLE / DEDICATED work / SHARED services / inherited resources; unchanged |

## TavallStudios repository and source-definition inventory

Live GitHub inventory found **55 repositories**. There are **47 canonical local roots** at the required `/srv/dev-storage/workspaces/<repo>/repo_root` location (46 with commits and the empty `tavall-roblox` repository), the seven user-designated GitHub-only repositories, and excluded `TavallMonoRepo`. The `tavall-project-novus/repo_root` path and `tavall-mc/repo_root` share the same device/inode; this is one materialization, not two. A separate dirty Novus worktree is retained under `tavall-mc/tavall-mc`.

The active source-side inventory contains **60 open `.tavallci/ci.yaml` PR heads across 52 repositories**. The additional local `tavall-docs` branch has its own `.tavallci`; `tavall-roblox` is empty and has no source commit or default branch, so it cannot yet own a CI definition. All 60 PR definitions passed exact-head `ci plan` parsing/planning through Tavall CI with exact Architecture Tests and Cloud API source composites. This is schema and plan evidence, not build/test execution.

| GitHub repository | Canonical local repository | `.tavallci/ci.yaml` source | Gradle / build tool |
| --- | --- | --- | --- |
| `TavallStudios/CustomMinecraftServer` | GitHub only; no local repo | PR #3@f90161599a1e | 9.6.1 (PR-head wrapper verified; no local repo) |
| `TavallStudios/function-catalog` | `/srv/dev-storage/workspaces/function-catalog/repo_root` (main@6e27cbef4b65) | PR #14@ae64f58f1a07 | 9.6.1 |
| `TavallStudios/HyRhythm` | GitHub only; no local repo | PR #2@a3ed66ed302f | 9.6.1 (PR-head wrapper verified; no local repo) |
| `TavallStudios/hytale-bots` | GitHub only; no local repo | PR #2@f1b55fe22eea | non-Gradle (node) |
| `TavallStudios/MCRSpeedrun` | GitHub only; no local repo | PR #3@b4a3493b6b82 | 9.6.1 (PR-head wrapper verified; no local repo) |
| `TavallStudios/minecraft-bot` | GitHub only; no local repo | PR #2@791f48b9c9a9 | non-Gradle (node) |
| `TavallStudios/tavall-ai` | `/srv/dev-storage/workspaces/tavall-ai/repo_root` (working/orchestrator-hook/tj@d8d87938922b) | PR #44@b323bf5d5b3a | 9.6.1 |
| `TavallStudios/tavall-ai-memory` | `/srv/dev-storage/workspaces/tavall-ai-memory/repo_root` (main@5b3ff8c0e558) | PR #1@ea82182854f6 | non-Gradle (none) |
| `TavallStudios/tavall-analytics` | `/srv/dev-storage/workspaces/tavall-analytics/repo_root` (feature/full-analytics-platform@16001c3a0e8a) | local `feature/full-analytics-platform@16001c3a0e8a`; PR #1@16001c3a0e8a, #7@415e5cf6dea7, #9@6431d5823636 | 9.6.1; wrapper PR #1, #7 |
| `TavallStudios/tavall-test-suite-tools` (renamed from `Tavall-Architecture-Tests`) | `/srv/dev-storage/workspaces/tavall-test-suite-tools/repo_root` (working/unified-ci-exact-artifact-versions-20260925@f69499397fa9) | local `working/unified-ci-exact-artifact-versions-20260925@f69499397fa9`; PR #14@f69499397fa9 | 9.6.1; wrapper PR #14 |
| `TavallStudios/tavall-cache` | `/srv/dev-storage/workspaces/tavall-cache/repo_root` (main@c8ed248a895e) | PR #11@7af38d81537f | 9.6.1 |
| `TavallStudios/tavall-ci` | `/srv/dev-storage/workspaces/tavall-ci/repo_root` (working/unified-gradle-cicd-20260924@f3ad7942eb77) | local source branch `f3ad7942eb77`; integrated into `staging/platform` at `bde88767288ab38df8a157818e923d11bb6537ae` by PR #14; root PR #15 remains Draft | 9.6.1 |
| `TavallStudios/tavall-cloud` | `/srv/dev-storage/workspaces/tavall-cloud/repo_root` (working/executor-canonical-architecture@2738f25a9c8c) | local `working/executor-canonical-architecture@2738f25a9c8c`; PR #395@2738f25a9c8c | 9.6.1 |
| `TavallStudios/tavall-concurrency` | `/srv/dev-storage/workspaces/tavall-concurrency/repo_root` (main@a83f7bd74d17) | PR #7@ad055f1e3ab2 | 9.6.1 |
| `TavallStudios/tavall-content` | `/srv/dev-storage/workspaces/tavall-content/repo_root` (working/tavall-java-tools-platform-adoption-v2@382361335b28) | local `working/tavall-java-tools-platform-adoption-v2@382361335b28`; PR #7@90650f2405dc, #14@1b7ddcf6a13e, #17@e85797afba1d | 9.6.1; wrapper PR #14 |
| `TavallStudios/tavall-content-tools` | `/srv/dev-storage/workspaces/tavall-content-tools/repo_root` (main@21f70d880200) | PR #1@deeb123af88e | non-Gradle (none) |
| `TavallStudios/tavall-custom-enum-java` | `/srv/dev-storage/workspaces/tavall-custom-enum-java/repo_root` (main@30900ddcb2ca) | PR #8@b1b2d96827bc | 9.6.1 in PR #8 (selected local ref pending) |
| `TavallStudios/tavall-database` | `/srv/dev-storage/workspaces/tavall-database/repo_root` (main@ec7672bc4358) | PR #17@7e437de57578 | 9.6.1 |
| `TavallStudios/tavall-di` | `/srv/dev-storage/workspaces/tavall-di/repo_root` (main@d8ecc0230252) | PR #13@1b638153f114 | 9.6.1 |
| `TavallStudios/tavall-discord` | `/srv/dev-storage/workspaces/tavall-discord/repo_root` (main@a37665d66b27) | PR #6@5cc474a13c5f | 9.6.1 in PR #6 (selected local ref pending) |
| `TavallStudios/tavall-docs` | `/srv/dev-storage/workspaces/tavall-docs/repo_root` (working/tavall-ci-evidence-provenance-20260925@161f15229fb9 before this update) | local `working/tavall-ci-evidence-provenance-20260925`; this rollout update continues PR #31 | no Gradle build on selected ref |
| `TavallStudios/tavall-docs-private` | `/srv/dev-storage/workspaces/tavall-docs-private/repo_root` (main@412731ab2a98) | PR #1@98399a7ff95d | non-Gradle (none) |
| `TavallStudios/tavall-eventbus` | `/srv/dev-storage/workspaces/tavall-eventbus/repo_root` (main@d66d9c7b7b33) | PR #7@db22c5b9d599 | 9.6.1 |
| `TavallStudios/tavall-github-bot` | `/srv/dev-storage/workspaces/tavall-github-bot/repo_root` (working/extract-github-bot-20260918@2984a157cff1) | local `working/extract-github-bot-20260918@2984a157cff1`; PR #1@2984a157cff1 | 9.6.1; wrapper PR #1 |
| `TavallStudios/tavall-hytale-resource-game` | `/srv/dev-storage/workspaces/tavall-hytale-resource-game/repo_root` (working/local-ci-workflow-removal@304304d165fc) | local `working/local-ci-workflow-removal@304304d165fc`; PR #3@304304d165fc | 9.6.1 |
| `TavallStudios/tavall-java-tools` | `/srv/dev-storage/workspaces/tavall-java-tools/repo_root` (working/verify-canonical-gitlinks@e3dee56ab2f7) | local `working/verify-canonical-gitlinks@e3dee56ab2f7`; PR #1@85965871ca65, #2@ed16dedfa031, #3@e3dee56ab2f7 | non-Gradle (none,shell) |
| `TavallStudios/tavall-java-utils` | `/srv/dev-storage/workspaces/tavall-java-utils/repo_root` (main@d9056d88b845) | PR #2@c74d9c22cda9 | non-Gradle (none) |
| `TavallStudios/tavall-logging` | `/srv/dev-storage/workspaces/tavall-logging/repo_root` (main@793e26bd9969) | PR #7@f3f3fbf344d8 | 9.6.1 |
| `TavallStudios/tavall-mc` | `/srv/dev-storage/workspaces/tavall-mc/repo_root` (working/combined-ci-profile-semantics-20260829@cab4fba24982) | local `working/combined-ci-profile-semantics-20260829@cab4fba24982`; PR #271@cab4fba24982, #301@32e3ce039c57 | 9.6.1 |
| `TavallStudios/tavall-mc-bot-testing` | `/srv/dev-storage/workspaces/tavall-mc-bot-testing/repo_root` (working/tavallci-node-20260926@40e3f4233ffe) | local `working/tavallci-node-20260926@40e3f4233ffe`; PR #5@7bbed95e555e, #6@40e3f4233ffe | non-Gradle (node) |
| `TavallStudios/tavall-mc-paper` | `/srv/dev-storage/workspaces/tavall-mc-paper/repo_root` (working/canonical-gradle-wrapper-20260925@ddafabdd4e57) | local `working/canonical-gradle-wrapper-20260925@ddafabdd4e57`; PR #6@ddafabdd4e57 | 9.6.1; wrapper PR #6 |
| `TavallStudios/tavall-minecraft-framework` | `/srv/dev-storage/workspaces/tavall-minecraft-framework/repo_root` (working/unified-gradle-cicd-20260925@f8302030cbbd) | local `working/unified-gradle-cicd-20260925@f8302030cbbd`; PR #11@f8302030cbbd | 9.6.1; wrapper PR #11 |
| `TavallStudios/tavall-rating-glicko2` | `/srv/dev-storage/workspaces/tavall-rating-glicko2/repo_root` (working/tavall-java-tools-platform-adoption@7062c80bdbbf) | PR #2@42027d34bca1 | 9.6.1 |
| `TavallStudios/tavall-reflection` | `/srv/dev-storage/workspaces/tavall-reflection/repo_root` (main@8d7ea5937c50) | PR #7@89a321cdf969 | 9.6.1 |
| `TavallStudios/tavall-registry` | `/srv/dev-storage/workspaces/tavall-registry/repo_root` (main@7d8f64d05332) | PR #8@5349f8a726a8 | 9.6.1 |
| `TavallStudios/tavall-roblox` | `/srv/dev-storage/workspaces/tavall-roblox/repo_root` (main@UNBORN) | no source commit; remote is empty | no build; empty repository |
| `TavallStudios/tavall-scheduler` | `/srv/dev-storage/workspaces/tavall-scheduler/repo_root` (main@2738e7925470) | PR #7@a5183ff8fee7 | 9.6.1 |
| `TavallStudios/Tavall-Talent-and-Contractors-` | `/srv/dev-storage/workspaces/Tavall-Talent-and-Contractors-/repo_root` (main@284ccaaf0922) | PR #2@144134ceba7f | non-Gradle (none) |
| `TavallStudios/tavall-web` | `/srv/dev-storage/workspaces/tavall-web/repo_root` (working/tavallci-unified-gradle-20260925@9cc29d2b3255) | local `working/tavallci-unified-gradle-20260925@9cc29d2b3255`; PR #43@9cc29d2b3255 | 9.6.1; wrapper PR #43 |
| `TavallStudios/tavall-web-account` | `/srv/dev-storage/workspaces/tavall-web-account/repo_root` (main@bc9e625a167c) | PR #1@0692dbf5d8c4 | non-Gradle (none) |
| `TavallStudios/tavall-web-blog` | `/srv/dev-storage/workspaces/tavall-web-blog/repo_root` (main@01b6293e301e) | PR #1@27da8b35ee34 | non-Gradle (none) |
| `TavallStudios/tavall-web-cloud` | `/srv/dev-storage/workspaces/tavall-web-cloud/repo_root` (main@1383bf8da322) | PR #1@9e7017a8e9bb | non-Gradle (none) |
| `TavallStudios/tavall-web-commerce` | `/srv/dev-storage/workspaces/tavall-web-commerce/repo_root` (main@d969d40c1b15) | PR #1@eb5ec22523ee | non-Gradle (none) |
| `TavallStudios/tavall-web-content` | `/srv/dev-storage/workspaces/tavall-web-content/repo_root` (main@3e0dca327178) | PR #1@23811b49de11 | non-Gradle (none) |
| `TavallStudios/tavall-web-contractors` | `/srv/dev-storage/workspaces/tavall-web-contractors/repo_root` (main@ea2a521b7d94) | PR #1@1172b4d1ff55 | non-Gradle (none) |
| `TavallStudios/tavall-web-discord` | `/srv/dev-storage/workspaces/tavall-web-discord/repo_root` (main@fdce6666353e) | PR #1@6b5dd6278946 | non-Gradle (none) |
| `TavallStudios/tavall-web-docs` | `/srv/dev-storage/workspaces/tavall-web-docs/repo_root` (main@d91e54f17841) | PR #1@11959c6ba2d9 | non-Gradle (none) |
| `TavallStudios/tavall-web-mc` | `/srv/dev-storage/workspaces/tavall-web-mc/repo_root` (working/tavallci-unified-gradle-20260925@d8ff175d10f1) | local `working/tavallci-unified-gradle-20260925@d8ff175d10f1`; PR #4@d8ff175d10f1 | 9.6.1; wrapper PR #4 |
| `TavallStudios/tavall-web-mcp` | `/srv/dev-storage/workspaces/tavall-web-mcp/repo_root` (working/tavallci-unified-gradle-20260925@97090a606381) | local `working/tavallci-unified-gradle-20260925@97090a606381`; PR #2@97090a606381 | 9.6.1; wrapper PR #2 |
| `TavallStudios/tavall-web-workflows` | `/srv/dev-storage/workspaces/tavall-web-workflows/repo_root` (main@57cef2916aa6) | PR #1@355f815254ca | non-Gradle (none) |
| `TavallStudios/tavall-workflows` | `/srv/dev-storage/workspaces/tavall-workflows/repo_root` (main@fe69b7ee329a) | PR #2@5ea2e155ee73 | non-Gradle (none) |
| `TavallStudios/TavallContractors` | `/srv/dev-storage/workspaces/TavallContractors/repo_root` (working/local-ci-workflow-removal@ecd5940b43fb) | local `working/local-ci-workflow-removal@ecd5940b43fb`; PR #3@ecd5940b43fb | 9.6.1 |
| `TavallStudios/TavallCouriers` | GitHub only; no local repo | PR #3@756052cb348e | 9.6.1 (PR-head wrapper verified; no local repo) |
| `TavallStudios/TavallMonoRepo` | Excluded; no canonical local repo | excluded | excluded |
| `TavallStudios/Webstore` | GitHub only; no local repo | PR #4@18077eb9126d | 9.6.1 (PR-head wrapper verified; no local repo) |

The seven GitHub-only repositories each have source-owned CI configuration in the open branch shown in the table; no local workspace was created for them. `TavallMonoRepo` was excluded from mapping, dependency composition, and aggregation.

## Unified Gradle status

- Every Gradle `.tavallci` PR head with a committed wrapper was checked at its exact SHA: **36 Gradle PR heads, all Gradle Wrapper 9.6.1 with `gradlew` present**.
- Twelve active PRs change wrapper files; every exact wrapper-properties blob reports Gradle 9.6.1. The two canonical local `main` refs that still lack wrappers, `tavall-custom-enum-java` and `tavall-discord`, have open PRs #8 and #6 that add the 9.6.1 standard wrapper.
- The approved Cloud Executor Java is `/opt/jdk-25.0.1`. Its shared execution surface maps `/var/cache/tavall-local-sandbox/gradle` to `/tavall/shared-tools/gradle`; the live service sets `GRADLE_USER_HOME=/tavall/shared-tools/gradle`. The durable sandbox service is active. The `DEVELOPMENT_SHARED` machine Executor has a separate Tavall-owned shared cache at `/srv/dev-storage/tavall-cache/shared-ci/gradle`, selected by `/usr/local/libexec/tavall-development-shared-ci` and isolated from per-job HOME/output state. Both are Executor-owned shared caches, not repository identity. Project `.gradle` state under canonical roots, exact-source shared-dependency materializations, the blocked DEVELOPMENT Environment, and older `/srv/workspace/.codex-worktrees` were retained as active or unknown; no source worktree was removed.
- Cache classification from current configuration: `/var/cache/tavall-local-sandbox/gradle` is canonical/current and active; `/srv/dev-storage/tavall-cache/shared-ci/gradle` is active for the existing shared-CI provider; `/srv/dev-storage/tavall-cache/host-local-sandbox/gradle` is an empty but still referenced provider cache, retained. `/var/lib/tavall-local-sandbox/home/.gradle` (155 MB, last wrapper distribution files from 2026-08-15) and 86 aged operation-home `.gradle` caches (1.58 GB total, owned by `tavall-sandbox`, last modified 13.4–28.6 days ago) were retired after confirming no running Gradle process or active sandbox unit used those Gradle homes. The operation directories and evidence/source files remain. The user-owned `/home/ubuntu/.gradle` cache used by local validation was preserved.

| Historical path class inspected | Count / finding | Classification and disposition |
| --- | --- | --- |
| `/var/lib/tavall-local-sandbox/operations/**/.gradle` | 86 directories, 1.58 GB, all older than 7 days; no active operation used them | Superseded per-operation caches; removed. Operation roots and source/evidence content preserved. |
| `/var/lib/tavall-local-sandbox/home/.gradle` | 155 MB; wrapper distribution files last modified 2026-08-15 | Superseded legacy home; removed after confirming current sandboxes set `GRADLE_USER_HOME` elsewhere. |
| `/var/lib/tavall-cloud/.gradle` | 458 MB; Tavall Cloud service user's default Gradle home; no Gradle process or open files, while both canonical Executor caches contain Gradle 9.6.1 | Superseded service-home cache; wrapper, module, native, and task caches removed. The 1.9 MB daemon log directory was retained. |
| `/var/cache/tavall-local-sandbox/gradle` | Active shared executor cache; mounted as `/tavall/shared-tools/gradle` | Canonical/current; retained. |
| `/srv/dev-storage/tavall-cache/shared-ci/gradle` | Active `DEVELOPMENT_SHARED` machine Executor cache | Active provider cache; retained. |
| `/srv/dev-storage/tavall-cache/host-local-sandbox/gradle` | Empty directory, still referenced by public-network sandbox scripts | Active but transitional; retained. |
| `/srv/workspace/**/.gradle` | 50 project-state directories, including old worktrees and `.codex-worktrees` | Unknown/preserve; source worktrees may contain unmerged work. No separate wrapper distribution was found in these project-state directories. |
| `/srv/dev-storage/workspaces/**/.gradle` | 26 project-state directories, including canonical roots, exact-source caches, and active/dirty work | Active/unknown; retained. No source tree was cleaned. |
| `/srv/dev-storage/environments/**/.gradle` | One cache under the blocked DEVELOPMENT Environment | Active environment materialization; retained. |
| `/srv/dev-storage/lanes/**/.gradle`, `/var/tmp/**/.gradle` | None found in the targeted scan | No cleanup target found. |
| `/home/ubuntu/.gradle` | User-owned wrapper cache used by local validation | Outside Tavall ownership; preserved. |
- Tavall CI remains a typed `GRADLE` executor. A scan of the 47 canonical local repository roots found no `mavenLocal()` declarations. During typed execution, TCI composes only source roots from the exact aggregate manifest and removes Maven Local, Tavall internal GitHub Package, and mutable file repositories from dependency/project resolution. Some repository-owned build files still declare `SNAPSHOT` coordinates; in TCI plans those are substituted by the declared exact-source composite inputs, so the mutable coordinate is not the source-composition identity. Upstream SNAPSHOT API dependencies remain external inputs where their owners require them.

## GitHub Actions ownership audit

The source migration audit found 27 open PR branches deleting `.github/workflows/*` files used for Tavall build, test, release, integration, or source-based deployment work. Those source removals remain unmerged. Following the 2026-09-27 clarification, the active GitHub workflow definitions for Tavall CI/CD were disabled in GitHub immediately; the repository PRs remain the durable source cleanup path. No GitHub Actions job is an allowed trigger, transport, runner, publisher, or gate for Tavall CI/CD.

Cloud's `.tavallci/ci.yaml` declares immutable Agent/runtime artifacts through Tavall CI. Cloud's Actions `Publish`, `Tavall Cloud operation`, and `CONTROL agent bootstrap` workflows have been disabled; Build and Integration Test were already disabled. Cloud PR #399 removes the remaining issue-operation and validation workflow files from `staging/runtime`. The host's `tavall-github-runner` Actions service and local broker are stopped and disabled. The separate server-owned Bot service is inactive and is not an Executor.

The independent GitHub Bot extraction PR #1 contains the typed `TavallCiCallerClient`, but `GitHubBotApplication.main` still fails closed because its transport adapters are not wired. The Bot-to-Tavall-CI event runtime is therefore not live yet; the source adapter and Check projection code are present, but that PR is not an execution cutover.

Command/authorization audit: the latest approved Cloud bootstrap request is issue #334, pinned to Cloud `43ee260a2b3422bcc0c6b3a7eaf6e4b4ddcc363e` and repository-staging `feaeb9970b3451992e365083ead347685a27acd8`. Its later comments record successful activation and follow-on Cloud updates, so it is completed historical lineage and was not rewritten or replayed for PR #395. The dedicated GitHub command-channel issue #241 was last updated on 2026-09-11 and has no recent typed CI manifest. The live CLI exposes `tavall executor ci run` with exact repository/head/profile inputs, but the installed Agent cannot accept the frozen TCI plan required by the current adapter. `tavall github authorization list` returns `DEPENDENCY_UNAVAILABLE` because GitHub operation authorization is not configured in the current Redis-only runtime. I did not reapply any old approval label. I briefly granted `INSPECT` on `shared-b37849b3e60796f28778b6d9d449f263` to inspect the existing runtime, confirmed it is `HOST_LOCAL_SANDBOX`/`SHARED_USER` (not the `DEVELOPMENT_SHARED` CI Executor), then revoked that grant; no authorization from this check remains active.

The analytics ingestion stack PR #7 now removes its manual `ubuntu-latest` Gradle validation workflow and carries the exact source-owned Tavall CI plan plus the Gradle 9.6.1 Wrapper. Its exact-head plan passes; no build green is claimed. In Tavall MC PR #294, `.github/workflows/open-upstream-pr.yml` was restored from that PR's exact base because it only opens a contribution PR from the maintainer's personal fork and does not perform Tavall build/deploy compute. PR #294 head is now `937f90f4d0e2eb45b410485dcc0b8adb706f3de8`.

Tavall MC PR #301 (`working/complete-minecraft-framework-extraction-20260920`) now removes `.github/workflows/cloud-runtime-deployment.yml` and declares the exact-source build plus `novus-runtime-deploy.jar` artifact in `.tavallci`; its four-check plan passes. PR #294 also retires the old source workflow in the existing promotion lineage. Neither branch has run through the live Cloud Executor. PR #271’s `open-upstream-pr.yml` automation remains a contribution-PR integration; PR #294 restores that file from its exact base. `TavallMonoRepo` workflow work is excluded from this rollout.
Function Catalog is public. The rollout PR #14 removes its old Gradle CI workflow but keeps `publish.yml`. Separate open PRs #12 and #18 delete that public package-publishing workflow and add scripts that invoke `./gradlew publish` locally. Those branches are not part of this CI migration and should not be promoted until public publication is routed through an approved Tavall CI release flow or explicitly retained as a release-only provider operation. Private `tavall-discord` and `tavall-minecraft-framework` package-publish workflows are internal and are removed by their exact-source migration PRs.

| GitHub workflow boundary | Exact PR head | Status |
| --- | --- | --- |
| `tavall-analytics#7` | `415e5cf6dea783069f4fe28a901fd44d01d19617` | Manual `ubuntu-latest` validation workflow removed; exact `.tavallci` and wrapper added; plan passes |
| `tavall-mc#301` | `32e3ce039c57f33f14ac8a401cff70743f12b230` | GitHub runtime build/deployment workflow removed; exact-source `.tavallci` and `novus-runtime-deploy.jar` artifact added; plan passes |
| `tavall-mc#294` | `937f90f4d0e2eb45b410485dcc0b8adb706f3de8` | Old source deployment and test workflows removed; unrelated personal-fork upstream PR automation restored |
| `tavall-mc#271` | `cab4fba24982af0c199f6c143c38a18ada95f55d` | Keeps the unrelated upstream PR workflow; source CI profiles remain in its `.tavallci` |
| `function-catalog#12` | `e60606c305b0de57fc14120aaa4c9afdf38e93cf` | Separate branch removes public `publish.yml`; do not promote with the local Gradle publisher |
| `function-catalog#18` | `6a28c5d7371b29f3a213909b5542b6ead1036937` | Separate branch removes public `publish.yml`; do not promote with the local Gradle publisher |


## Service/runtime CD state

The current template loader resolves `/srv/dev-storage/templates/services/<service-id>/.tavallcd/cd.yaml`; no new template leaf was introduced. Deployed lineage is under the existing environment-scoped service roots, for example `/srv/dev-storage/services/environments/tavall-cloud-chatgpt-plugin/.tavallcd/{metadata.json,deployment.json}`.

| Current Cloud service | `.tavallcd` / deployment state |
| --- | --- |
| `tavall-cloud-chatgpt-plugin` | Template exists; live Redis read on 2026-09-26 reports configuration 10, runtime generation 60, actual RUNNING in DEVELOPMENT/SINGLE. The legacy artifact lineage (`ba454965…`) still has blank CI run/evidence IDs. It is not a rollout candidate. |
| `tavall-cloud-control` | The live `.tavallcd/cd.yaml` is SHA-256 `5033fa2b…`; Cloud PR #398 packages those exact bytes under the canonical services template leaf and merged into `staging/runtime` at `c8ed22d9…`. CONTROL_PLANE remains RUNNING from `/opt/tavall-cloud/tavall-cloud-agent.jar` (SHA-256 `b3edfd20…`), which is absent from the 14 immutable artifacts. CD remains disabled/MANUAL; no immutable bootstrap artifact is registered and the service was not redeployed. |
| `novus-ffa-east-backend` | Registry entry is RUNNING desired / UNKNOWN observed; no canonical service template was found and Cloud reports invalid CD request. No template was guessed. |
| `tavall-cloud-redis` | Infrastructure service; no application `.tavallcd` required. |
| `tavall-cloud-storage-prepare` | Infrastructure service; no application `.tavallcd` required. |

PR #14 binds frozen artifact, exact source, build/CI evidence, template identity and digest, runtime identity, deployment generation, and typed readiness into the existing Cloud CLI flow. PR #395 adds Cloud runtime-instance isolation, durable `.tavallcd` deployment lineage, generation-fenced readiness observations, standby deployment, and an exact-bundle authorized production promotion command. These branches preserve the existing `tavall service deploy` and CONTROL path.

## Live validation boundary

The canonical DEVELOPMENT Environment `5848c5ff-a2a2-4da4-bd25-9cff8e558433` remains in lane `f75e1548-c7ab-470a-85aa-b38a770dae78`, durable, generation 21, and **BLOCKED**. A live CONTROL read on 2026-09-26 reports source snapshot `93fbaec4293756233c2dc230d3f1496f5912620be4a460fbd2340711c545fc28`: TCI `staging/platform@bde88767288ab38df8a157818e923d11bb6537ae`, Cloud `staging/runtime@7a822eb5abae923b92a085b768f19026ec2f0ea6`, and Architecture Tests `working/unified-ci-exact-artifact-versions-20260925@c0863bfe9e3ea38e4872eb295856e69bed30eb28`. WORKSPACE and DEVELOPMENT_TOOL still report `UNKNOWN`.

The live Environment Git-status command returns `STALE_VERSION` for TCI and Cloud because their bound paths do not match the exact Environment sources. The TCI path is clean at `ef59a10f97668bf38f47616649353e8cca1199bb` on `working/unified-gradle-cicd-20260924`, while the Environment binds `staging/platform@bde88767288ab38df8a157818e923d11bb6537ae`. The Cloud path is clean at `2f1c94b47d38d86a1724067c0ab8be39bd512178` on `main`, while the Environment binds `staging/runtime@7a822eb5abae923b92a085b768f19026ec2f0ea6`. These branch/source mismatches were preserved. Cloud PR #395 is merged into the existing `staging/runtime` branch at `7a822eb5…`; its tree matches the PR source `2738f25a…` (tree `668d2ff…`). The active Agent still runs `/opt/tavall-cloud/tavall-cloud-agent.jar` at SHA-256 `b3edfd20…`, and the shared-CI helper remains SHA-256 `5f91dfc9…`; neither matches the plan-aware staged runtime path.

### Cloud CI exact-source Environment — 2026-09-27

Cloud's `.tavallci` selects `function-catalog@ae385f8885a218c5b075dcdb1f0bac2892681ea4` and requires exact shared sources for Cache, Concurrency, Database, DI, Event Bus, Logging, Reflection, Registry, Scheduler, and Architecture Tests. I created a separate **EPHEMERAL** Environment `d93dc1c9-8c3f-43fd-9d2a-76adf1582b01` in lane `f75e1548-c7ab-470a-85aa-b38a770dae78`, then re-resolved it in place after Cloud `staging/runtime` advanced to `c8ed22d9c1cafa6d6ba651ef08050b3c9a94b5f3`. It is generation 2, source snapshot `b0fff546bff5670a703a736b048f91afbf5851296a7d0ab6cf7700e0bf1e6ad9`, `EPHEMERAL`, `DEDICATED` work, `SHARED` services, and inherits the lane's `SYSTEM` resources. The durable TCI Environment `5848c5ff…` was not changed.

CONTROL confirms the Function Catalog, Cache, and Architecture Tests workspaces are clean at their exact bound SHAs. Cloud primary status fails before a Job starts with `PROVIDER_FAILURE: Workspace UUID mismatch` at `/srv/dev-storage/workspaces/tavall-cloud` (existing workspace ID `6cbfdbc7-8c75-43e3-b84c-79d637fdd332`, requested `8dc5a485-b849-4c43-8af9-771f2e8b415e`). Its WORKSPACE and DEVELOPMENT_TOOL components remain `UNKNOWN`. The staged Cloud source contains the dedicated, source-snapshot-scoped workspace authority; the installed Agent predates it. The EPHEMERAL Environment is retained for reuse after that Agent is provisioned. No Cloud build Job was submitted.

### Cloud CI exact-source Environment — 2026-09-27

To bind the Cloud `.tavallci` required sources, I created an additional **EPHEMERAL** Environment in the existing lane `f75e1548-c7ab-470a-85aa-b38a770dae78`; the durable TCI Environment above was not replaced or edited. After Cloud PR #398 advanced `staging/runtime`, the same ephemeral Environment was re-resolved in place to source snapshot `b0fff546bff5670a703a736b048f91afbf5851296a7d0ab6cf7700e0bf1e6ad9`, generation 2, with `DEDICATED` work and `SHARED` services. Resource policy inherits the lane's `SYSTEM` default.

| Role | Exact source binding |
| --- | --- |
| `PRIMARY` | `TavallStudios/tavall-cloud@c8ed22d9c1cafa6d6ba651ef08050b3c9a94b5f3` (`staging/runtime`) |
| `SHARED_DEP` | `TavallStudios/function-catalog@ae385f8885a218c5b075dcdb1f0bac2892681ea4` (`agent/pr-1219763363-20-c5dadb1db245`, pinned by Cloud `.tavallci`) |
| `SHARED_DEP` | `TavallStudios/tavall-cache@c8ed248a895ea0853c107aadd058165b61aae29d` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-concurrency@a83f7bd74d1753f44bbf099c98c8f40345612beb` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-database@ec7672bc435872c999e6955c34ca90dab35bc9c4` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-di@d8ecc02302522e3acecc586c3f9e918007c82ca3` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-eventbus@d66d9c7b7b3329d8f852e7986c20111b454308a8` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-logging@793e26bd9969ef372d3f9410e5a563e78499ed43` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-reflection@8d7ea5937c505da8a9c9fdf84112b2a137217dcd` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-registry@7d8f64d05332dacbe04e55a3b68ad82ad702068d` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-scheduler@2738e7925470f739e596971fa7a1a3213a7694b1` (`main`) |
| `SHARED_DEP` | `TavallStudios/tavall-test-suite-tools@c0863bfe9e3ea38e4872eb295856e69bed30eb28` (`working/unified-ci-exact-artifact-versions-20260925`) |

CONTROL Git status confirms the Function Catalog, Cache, and Architecture Tests materializations are clean at those exact SHAs. The Cloud primary checkout is blocked with `PROVIDER_FAILURE: Workspace UUID mismatch` at `/srv/dev-storage/workspaces/tavall-cloud` (existing workspace ID `6cbfdbc7-8c75-43e3-b84c-79d637fdd332`, requested `8dc5a485-b849-4c43-8af9-771f2e8b415e`). The Environment remains `BLOCKED`; no job was started. The staged Cloud source contains the dedicated, source-snapshot-scoped workspace authority, but the installed Agent still predates it. The new ephemeral Environment is retained for reuse after the plan-aware Agent is provisioned.

A read-only inventory of `/opt/tavall-cloud/tavall-cloud-agent.jar` and its retained backups found no candidate with the frozen-plan CLI option; every inspected JAR reports it absent. The shared CI runtime tool cache is empty, and the content-addressed Cloud artifact root has no object matching the installed Agent digest. No retained binary is a safe substitute for a newly built plan-aware artifact.

The broader artifact search found `/srv/tavall-storage/development/workspaces/tavall-ci/repo_root/tavall-ci-runtime/build/distributions/tavall-ci-runtime-0.1.0.zip` (SHA-256 `33c85b8f799e408a5eb8527e99f3afac4ee27c2cf0df160344a75fd8b5f6cc13`). Its enclosing `workspace.json` claims `main@00ac2dad0c5c3854357d9cf6252c7962885d1159`, while the nested Git checkout is clean at `working/unified-gradle-cicd-20260924@f3ad7942eb775a232e1e92a91a6baf101cac1444`; no TCI job result or artifact-reference record was found beside it. This is an `unknown/preserve` workspace build output, not a verified immutable TCI artifact, and it was not deployed. A retained Cloud `allJar` at `/srv/tavall-storage/development/workspaces/tavall-cloud-github-credential-fix` hashes to the installed Agent SHA and likewise lacks the frozen-plan interface.

The default-branch `control-agent-bootstrap.yml` was an owner-label-gated recovery workflow; its latest run `35649180862` did not replace the Agent, and the workflow is now disabled. The host account `tavall-github-runner` was the unprivileged identity for GitHub's `Runner.Listener` (UID 996, nologin). It is separate from `tavall-cloud-github-bot`; the Bot unit is inactive. The Actions service has been stopped and disabled, so the runner account is no longer an event adapter or build machine.

The staged Tavall CI Cloud adapter submits plan-bound durable jobs with `--execution-provider DEVELOPMENT_SHARED`; its test asserts that provider. Cloud materializes exact inputs inside the per-job Executor workspace and runs the shared-CI broker without GitHub or GitHub Packages credentials. The staged Cloud source uses a frozen-plan broker contract; the installed Agent and 8-argument helper still use the retired script-based contract. GitHub Actions is not a caller or execution plane for this route; the server-owned Bot is the intended GitHub adapter and remains inactive. Cloud staging root PR #397 remains Draft until the plan-aware Agent/helper are installed through the Cloud/Executor bootstrap path and a real durable CI job succeeds.

### Live command and Executor recheck — 2026-09-26

The installed `tavall` command catalog reports 181 forms. The current `tavall executor ci run --help` exposes operation ID, repository, expected head, profile, and evidence handle, but no frozen Tavall CI plan. The installed `tavall environment repository job start --help` also omits `--execution-plan-json` and immutable runtime-artifact identity fields, although these are present in the staged Cloud source. The advertised `tavall environment repository refresh` form is rejected by the installed Agent as an unknown command. The live command catalog/runtime is therefore stale relative to the staged Cloud command contract.

The GitHub command-channel issue #241 still contains its 2026-09-11 `LIST_SERVICES` request, not a CI plan. It was left unchanged and is not used. Its Actions workflow is disabled and removed from the current Cloud staging source. Tavall CI requests must use the provider-neutral Tavall CI caller through CONTROL to `DEVELOPMENT_SHARED`; `tavall executor ci run` is not a substitute.

The generic `tavall executor acquire` command reused the existing `shared-b37849b3e60796f28778b6d9d449f263` host-local Executor (`SHARED_USER`). No invocation or grant was created. This Executor is distinct from the environment-bound `DEVELOPMENT_SHARED` machine Executor used for Tavall CI, so it was not used to build or deploy the CI runtime.

### Actions retirement and shared Executor probe — 2026-09-27

The live host confirms `tavall-github-runner` was the unprivileged OS account for `actions.runner.TavallStudios.dev-control-github-operations.service` (UID 996, nologin). It is separate from `tavall-cloud-github-bot`; the Bot unit is also installed but currently inactive. The Actions runner and bridge units are now stopped and disabled. The runner account is not a Tavall Bot identity or Executor.

I reviewed the live command list and issue #241 before using a command. The installed CLI advertises the generic `environment repository job start` contract with `--execution-provider DEVELOPMENT_SHARED`, so I submitted a read-only exact-head probe to the existing ephemeral Cloud CI Environment (`d93dc1c9-8c3f-43fd-9d2a-76adf1582b01`) for Cloud `c8ed22d9c1cafa6d6ba651ef08050b3c9a94b5f3`. CONTROL rejected materialization before Executor execution with `PROVIDER_FAILURE: Workspace UUID mismatch` at `/srv/dev-storage/workspaces/tavall-cloud` (existing workspace `6cbfdbc7-8c75-43e3-b84c-79d637fdd332`, requested workspace `90d74324-261f-4bd6-8e19-3f89dffacacb`). No job or Executor invocation was created. The canonical workspace metadata was not edited; the fix remains deployment of the staged plan-aware Agent and dedicated environment workspace authority through the Cloud/Executor bootstrap path.

The current Notion CI/CD contract places execution on authorized Tavall Cloud Executors. Tavall CI/CD now explicitly forbids GitHub Actions jobs from triggering, scheduling, executing, carrying, publishing, or gating CI/CD work; GitHub Checks remain a Bot/API projection. I found no queued or in-progress Actions runs across the 54 in-scope organization repositories. Thirty-two active build, validation, deployment, and artifact-publication workflow definitions were disabled across 18 Tavall repositories: `function-catalog`, `tavall-cache`, `tavall-concurrency`, `tavall-di`, `tavall-eventbus`, `tavall-logging`, `tavall-reflection`, `tavall-scheduler`, `tavall-database`, `tavall-registry`, `tavall-mc`, `tavall-cloud`, `tavall-analytics`, `tavall-custom-enum-java`, `tavall-test-suite-tools` (renamed from `Tavall-Architecture-Tests`), `tavall-discord`, `tavall-minecraft-framework`, and `tavall-mc-bot-testing`. A current-default-branch file/status comparison confirms every Tavall build, test, validation, deployment, integration, and package-publish workflow is disabled, including the seven designated remote-only repositories. The only enabled default-branch workflows left in the 54-repository scope are the personal-fork upstream-PR workflow in `tavall-mc` and canonical-source sync in `tavall-java-utils`; Tavall AI's dependency-graph automation is separate. Cloud's operation, bootstrap, and publish workflows were disabled; Build, Integration Test, and earlier validation workflows were already disabled. Cloud PR #399 removes the remaining Actions workflow files from `staging/runtime`. The dedicated Actions runner and broker systemd units are disabled. `TavallMonoRepo` and unrelated dependency/source-sync automation were not changed.

An additional Cloud build output exists at `/srv/tavall-storage/development/workspaces/tavall-cloud/repo_root/tavall-cloud-node/build/libs/tavall-cloud-agent.jar`, SHA-256 `633a6b7f959b8916e65a3415932e7b7d15b13dd27d15fe33e82837450098894a`. Its nested checkout is clean at Cloud PR source `2738f25a…`; the JAR contains the frozen-plan guard. No CI result, durable evidence, or immutable artifact reference was found for this output. It remains an unverified workspace build output and was not installed or deployed.

### Storage pressure cleanup — 2026-09-26

Before cleanup, `/` was 194 GB total with 1.9 GB available (reported 100%); `/srv/dev-storage` was 8.2 GB total with 1.8 GB available (79%). `/var/log/syslog.1` was a closed, rotated 1,815,071,907-byte log. It was gzip-compressed to 88,417,583 bytes; the SHA-256 of the compressed stream was verified against the original (`0c8a415536985f094d2749f6adbe12a4e26c8aac22172396c0a4eac8e3a9db16`). No log content was discarded.

Three 15 MB Tavall artifact files under `/tmp/tavall-ci-artifact-store-*` were byte-compared with their same-digest objects under `/var/lib/tavall-cloud/artifacts/sha256`; only those temporary duplicates and their empty directories were removed. The regenerable APT download cache was cleaned. The stale `/var/lib/tavall-cloud/.gradle` service-home cache was retired as described above. After cleanup, `/` had 4.2 GB available (98% reported) and `/srv/dev-storage` remained at 1.8 GB available (79%).

The canonical `/var/cache/tavall-local-sandbox/gradle` cache (1.0 GB) and active `/srv/dev-storage/tavall-cache/shared-ci/gradle` cache (286 MB) remain. After disabling the Actions runner, I removed its 494 MB `.gradle` cache, 8.4 MB `.m2` cache, 303 MB cached Temurin JDK, two runner checkout `.gradle` directories, and 458 MB of downloaded Actions/update staging files. The runner checkout repositories were retained: Function Catalog is clean at `feaeb9970b3451992e365083ead347685a27acd8`; the Cloud checkout is detached at `43ee260a2b3422bcc0c6b3a7eaf6e4b4ddcc363e` with an unmerged `AGENTS.md` deletion and was preserved. The runner work area is now 67 MB. User-owned `/home/ubuntu/.gradle`, active Executor operation roots, the 976 MB Cloud rollback-backup tree, stale-environment quarantine, immutable artifacts, source materializations, and unrelated product files remain. No repository worktree, active execution, or durable evidence was deleted. Root free space is 5.2 GB; `/srv/dev-storage` remains at 1.8 GB.

The Environment inventory contains two other RUNNING DEVELOPMENT environments, but neither is a valid substitute: one is owned by `web-design-agent/e2e` and binds personal Portfolio/Agent sources; the other is owned by `tavall-web/repository-extraction` and binds Web sources. Both and the canonical durable Environment were left unchanged; the Cloud validation Environment above is separate and EPHEMERAL.

No Tavall CI Cloud job, immutable artifact, frozen delivery bundle, DEVELOPMENT deployment, STAGING readiness evidence, or production promotion was produced. The live service and production traffic were not changed. The existing service registry and templates are not being treated as proof of rollout deployment.

## Validation evidence

- Cloud focused core/node/ChatGPT suites on the PR source: **658 tests, 0 failures, 0 errors, 2 skipped sandbox tests**.
- Cloud `:tavall-cloud-test-suite:architectureTest` fails with 120 existing findings: 44 repository-role, 34 direct-thread, and 42 production-`var` violations across unrelated Cloud modules. The changed clean-worktree recovery provider is not listed; no Architecture Test pass is claimed.
- Tavall CI full `check`, its Architecture Tests suite, and runtime distribution packaging passed on Java 25 / Gradle 9.6.1 with exact Cloud API and Architecture Tests composites (46 actionable tasks in the prior validation run).
- On Java 25 / Gradle 9.6.1, `:tavall-ci-cloud:test --tests org.tavall.ci.cloud.TavallCloudCliJobServiceTest` passed using exact source composites for Tavall CI `f3ad7942eb775a232e1e92a91a6baf101cac1444`, Tavall Cloud `2738f25a9c8c979e1b25673d8734002f29eaf061`, and Architecture Tests `c0863bfe9e3ea38e4872eb295856e69bed30eb28` (27 tasks; test executed). This local wrapper run validates the provider contract, not live Cloud Executor placement. A plain Gradle run without the composite correctly failed to resolve Cloud API from Maven Central; no GitHub Packages fallback was added.
- The GitHub Bot runtime test task passed on Java 25 / Gradle 9.6.1 using exact Bot `2984a157cff1e2a7552cf7fe82ef126667c088a3`, TCI `f3ad7942eb775a232e1e92a91a6baf101cac1444`, and Architecture Tests `c0863bfe9e3ea38e4872eb295856e69bed30eb28` composites (15 tasks; tests executed). This validates the typed CI caller and GitHub projection contracts, not a live Bot process; `GitHubBotApplication.main` remains unwired.
- TCI PR #14 was merged into the existing Draft `staging/platform` root as merge commit `bde88767288ab38df8a157818e923d11bb6537ae`. This integrates the source implementation for staging; it does not claim live Cloud execution or authorize promotion to `main`.
- The staged tree at `bde88767288ab38df8a157818e923d11bb6537ae` is byte-for-byte the same Git tree (`6b91391885c7ac3b0b880e16ec79e33690362276`) as tested feature head `f3ad7942eb775a232e1e92a91a6baf101cac1444`; earlier exact-source TCI checks therefore cover the staged source tree. Live Cloud Executor acceptance remains pending.
- Cloud's `scripts/test-shared-development-ci-contract.sh` passed against the current PR source; it checks the frozen-plan invocation and that the Executor broker receives no GitHub or GitHub Packages credentials.
- A later plain Gradle composite attempt for `check`, `architectureTest`, and `distZip` stopped before the architecture task because `org.tavall:tavall-architecture-core:1.1.0` and `org.tavall:tavall-architecture-patterns:1.1.0` were unavailable from Maven Central. That manual invocation did not create the per-job Architecture Tests repository that TCI's frozen plan provides; classify it as a dependency-bootstrap miss, not source/test failure or live Executor evidence. The prior full exact-source TCI check remains historical evidence only.
- The docs staging child PR #31 now includes the current `staging/quality` root commit, and Draft root PR #34 restores the active `staging/quality` -> `main` ancestry after the prior root was promoted. Both PRs remain Draft; no merge to `main` occurred. Docs validation on the merged child head passed (`trackedDocs=33`).
- Exact-head CI definition planning: **60/60 pass**, correct source identity, zero plan failures. This does not claim any configured repository build ran.
- Live Cloud status: Agent, Control, and developer storage are ready; the selected DEVELOPMENT Environment remains blocked as described above.
- At the 2026-09-26 snapshot, the checked-in Notion exports were the available mirror and no live Notion write was made. The Cloud Progression twin was synchronized from the merged GitHub progression on 2026-09-27 after Cloud PR #414.

## Open rollout pull requests

- [`tavall-cloud#397`](https://github.com/TavallStudios/tavall-cloud/pull/397) — Draft `staging/runtime` root to `main`; head contains the Cloud #395 merge at `7a822eb5…`.
- [`tavall-cloud#395`](https://github.com/TavallStudios/tavall-cloud/pull/395) — merged into `staging/runtime` at `7a822eb5abae923b92a085b768f19026ec2f0ea6`; not promoted to `main`.
- [`tavall-cloud#398`](https://github.com/TavallStudios/tavall-cloud/pull/398) — merged into `staging/runtime` at `c8ed22d9c1cafa6d6ba651ef08050b3c9a94b5f3`; packages the byte-identical live `tavall-cloud-control/.tavallcd/cd.yaml` under Cloud's existing services template leaf.
- [`tavall-cloud#399`](https://github.com/TavallStudios/tavall-cloud/pull/399) — Draft child of `staging/runtime`; removes the remaining Cloud Actions operation/validation workflows. The host runner and broker are disabled; the documentation retirement is merged through Cloud PRs #410–414.
- [`tavall-ci#15`](https://github.com/TavallStudios/tavall-ci/pull/15) — Draft `staging/platform` root to `main`, head `bde88767288ab38df8a157818e923d11bb6537ae`.
- [`tavall-ci#14`](https://github.com/TavallStudios/tavall-ci/pull/14) — merged exact-source CI/CD implementation into `staging/platform` at `bde88767288ab38df8a157818e923d11bb6537ae`; feature source head `f3ad7942eb775a232e1e92a91a6baf101cac1444`.
- [`tavall-github-bot#2`](https://github.com/TavallStudios/tavall-github-bot/pull/2) — Draft Bot staging root to `main`.
- [`tavall-github-bot#1`](https://github.com/TavallStudios/tavall-github-bot/pull/1) — Draft Bot extraction child to `staging/platform`.
- [`tavall-docs#34`](https://github.com/TavallStudios/tavall-docs/pull/34) — Draft `staging/quality` root to `main`.
- [`tavall-docs#31`](https://github.com/TavallStudios/tavall-docs/pull/31) — Draft CI/CD architecture and rollout evidence child to `staging/quality`.
- Source-owned `.tavallci` and wrapper work remains in the 60 existing PR heads shown above; no duplicate source PRs were opened.

## Remaining blockers

- **Architecture/design:** none found that prevents preserving the agreed ownership model.
- **Implementation:** install the exact Cloud Agent recovery and serialized-plan support through the existing immutable-artifact/CONTROL authority path; complete any required GitHub Bot application composition before treating event ingress as operational.
- **Validation:** clear the existing Cloud Architecture Tests backlog and run representative exact Gradle jobs on the real Tavall Cloud Executor; validate shared-cache concurrency there.
- **Deployment:** provision an immutable bootstrap artifact for `tavall-cloud-control`, repair the exact-source Environment via updated CONTROL, then produce artifact/bundle lineage, DEVELOPMENT readiness, and STAGING readiness.
- **External/provider:** no GitHub provider outage was observed. The prior Notion update limitation was cleared for the Cloud Progression twin; the CI/CD, DEVELOPMENT, and STAGING readiness gates remain separate.

## Live continuation — 2026-09-28

This entry supersedes the earlier live-blocker snapshots above where current state differs.

- GitHub renamed `TavallStudios/Tavall-Architecture-Tests` to `TavallStudios/tavall-test-suite-tools`. The canonical local repository is `/srv/dev-storage/workspaces/tavall-test-suite-tools/repo_root`; the exact `c0863bfe…` source commit is reachable from the renamed repository. Three registered environments were re-resolved to the renamed source identity and refreshed without changing their desired states or lane policies. The two clean old-name shared-source checkouts, their metadata projections, and one old-name environment symlink were retired. Open PR #14 remains on its existing branch at `f69499397fa9766ae64a4db3a7e9b6c1e51454a2`.
- Tavall Cloud PR #399 at `69fc6800195fadebf4110927d1be1b3701616ae9` passed the live `all` profile on the `DEVELOPMENT_SHARED` Executor: dependencies, architecture, behavior, integration, quality, runtime, and required aggregate all passed. Evidence records Java 25, Gradle 9.6.1, build-policy digest `781e2265…`, source aggregate `28ac2944…`, and exact job `69fc6800-195f-4a4e-9181-b371de462a63`.
- The same exact source then produced a frozen delivery bundle (`df3b305e…`) from CI job `69fc6800-195f-4a4e-9181-b371de462a64`, artifact `98ec6e29…`, and template `services/tavall-cloud-chatgpt-plugin` (`b2112c0d…`). Tavall Cloud deployed it through the existing service path to DEVELOPMENT runtime `chatgpt-web-adapter`; generation 68 recorded three healthy observations for runtime instance `tavall-cloud-chatgpt-plugin-development-single-91c0f5b96e18e1a5`. The deployed `.tavallcd/deployment.json` preserves CI, bundle, template, source, artifact, runtime, generation, and readiness lineage. The previous service release remains the rollback baseline.
- The Cloud Agent artifact built from that exact Cloud source (`fd25775d…`) is installed and active. The `tavall-ci` caller can read durable CI evidence through the Control socket ACL. The prior stable DEVELOPMENT service remains healthy while the new exact artifact runs in its isolated runtime.
- Tavall CI itself passed the full profile on `DEVELOPMENT_SHARED` at `b844c83e20cfa050d293567eed3c3c148985bb78` (job `b844c83e-20cf-4050-8d29-3567c3c14899`). Dependencies, architecture, behavior, integration, runtime, quality, and required aggregate passed on Java 25 / Gradle 9.6.1. The exact source aggregate is `b04e4d4c…`; evidence records the renamed `tavall-test-suite-tools` source.
- Two concurrent Cloud `all` jobs at the same exact source (`69fc6800…`) completed successfully on the shared Executor (jobs `69fc6800-195f-4a4e-9181-b371de462a67` and `69fc6800-195f-4a4e-9181-b371de462a68`). They used distinct job workspaces, the same `/tavall/shared-tools/gradle` cache, Java 25, Gradle 9.6.1, and the same source/build plan identities; all required checks and durable evidence passed.
- The `tavall-cloud-control` template exists, but the registered `CONTROL_PLANE` service currently uses the bootstrap-owned `tavall-cloud-agent.service` without an immutable deployment strategy. A read-only `tavall service deploy plan tavall-cloud-control` returned `INVALID_REQUEST: service label deployment.strategy is required`. The new Cloud Agent is therefore installed from the verified immutable artifact through the existing installer/bootstrap path; the generic runtime template has not been applied to the Control service.
- STAGING remains behind the template's `ACCEPTED_MAIN` promotion gate while Cloud PR #399 and TCI PR #17 are unmerged; both are ready for review. No production promotion was attempted. The wider audit of historical workspace, environment, lane, and UUID materializations continues. `/srv/tavall-storage/development` and `/srv/dev-storage` are two mounts of the same ZFS dataset, so they are not separate copies to prune.
- Filesystem cleanup retired 14 clean merged linked worktrees, 24 clean merged or superseded `/tmp` repository snapshots, two old-name architecture-test source caches, two obsolete temporary Cloud Agent JAR copies, extracted TCI caller/runtime bundles after their verified use, old temporary Maven/Gradle architecture-test outputs, and 52 empty `namespace-dev-*` roots. Dirty worktrees, current environments/lanes, active systemd `PrivateTmp` roots, and the 316-root stale-environment evidence quarantine were preserved.
- GitHub Actions remain disabled as a Tavall CI/CD execution plane. GitHub supplies source and SCM/check projection; the build and deployment above ran through Tavall CI and the Tavall Cloud Executor/CONTROL path.
