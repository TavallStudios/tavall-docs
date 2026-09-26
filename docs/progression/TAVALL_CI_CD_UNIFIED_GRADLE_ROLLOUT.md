# Tavall CI/CD, Unified Gradle, and Deployment Rollout

> **Document type:** Progression / evidence snapshot
> **Snapshot date:** 2026-09-26
> **Scope:** Continue the Tavall CI/CD, unified Gradle, and service/runtime delivery rollout without replacing existing Tavall Cloud execution or deployment authorities.

This is a progression record, not a second architecture authority. The accepted boundary is in [`docs/quality/CI_CD.md`](../quality/CI_CD.md): repositories own build intent and project topology; Tavall CI owns build policy, planning, exact-source composition, evidence, and delivery identity; Cloud Executors own provisioning and execution; Tavall Cloud owns environments, service state, deployment materialization, routing, and runtime readiness.

## Current source and Environment identities

| Item | Exact identity |
| --- | --- |
| Tavall CI PR #14 | `f3ad7942eb775a232e1e92a91a6baf101cac1444` on `working/unified-gradle-cicd-20260924`, base `staging/platform`, Draft |
| Tavall Cloud PR #395 | `2f061cd9f42cd4f44c813d3f8aa0e62b50d1ddac` on `working/executor-canonical-architecture`, base `staging/runtime`, Draft |
| Architecture Tests dependency | `c0863bfe9e3ea38e4872eb295856e69bed30eb28` on `working/unified-ci-exact-artifact-versions-20260925` |
| Existing DEVELOPMENT Environment | `5848c5ff-a2a2-4da4-bd25-9cff8e558433` in lane `f75e1548-c7ab-470a-85aa-b38a770dae78` |
| Resolved exact source snapshot | `6b6c3b49eaeed98cc0d6d505243a76d19e78ff8ec90a2e5284854b4000e834b3` |
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
| `TavallStudios/Tavall-Architecture-Tests` | `/srv/dev-storage/workspaces/Tavall-Architecture-Tests/repo_root` (working/unified-ci-exact-artifact-versions-20260925@c0863bfe9e3e) | local `working/unified-ci-exact-artifact-versions-20260925@c0863bfe9e3e`; PR #14@c0863bfe9e3e | 9.6.1; wrapper PR #14 |
| `TavallStudios/tavall-cache` | `/srv/dev-storage/workspaces/tavall-cache/repo_root` (main@c8ed248a895e) | PR #11@7af38d81537f | 9.6.1 |
| `TavallStudios/tavall-ci` | `/srv/dev-storage/workspaces/tavall-ci/repo_root` (working/unified-gradle-cicd-20260924@f3ad7942eb77) | local `working/unified-gradle-cicd-20260924@f3ad7942eb77`; PR #14@f3ad7942eb77 | 9.6.1 |
| `TavallStudios/tavall-cloud` | `/srv/dev-storage/workspaces/tavall-cloud/repo_root` (working/executor-canonical-architecture@2f061cd9f42c) | local `working/executor-canonical-architecture@2f061cd9f42c`; PR #395@2f061cd9f42c | 9.6.1 |
| `TavallStudios/tavall-concurrency` | `/srv/dev-storage/workspaces/tavall-concurrency/repo_root` (main@a83f7bd74d17) | PR #7@ad055f1e3ab2 | 9.6.1 |
| `TavallStudios/tavall-content` | `/srv/dev-storage/workspaces/tavall-content/repo_root` (working/tavall-java-tools-platform-adoption-v2@382361335b28) | local `working/tavall-java-tools-platform-adoption-v2@382361335b28`; PR #7@90650f2405dc, #14@1b7ddcf6a13e, #17@e85797afba1d | 9.6.1; wrapper PR #14 |
| `TavallStudios/tavall-content-tools` | `/srv/dev-storage/workspaces/tavall-content-tools/repo_root` (main@21f70d880200) | PR #1@deeb123af88e | non-Gradle (none) |
| `TavallStudios/tavall-custom-enum-java` | `/srv/dev-storage/workspaces/tavall-custom-enum-java/repo_root` (main@30900ddcb2ca) | PR #8@b1b2d96827bc | 9.6.1 in PR #8 (selected local ref pending) |
| `TavallStudios/tavall-database` | `/srv/dev-storage/workspaces/tavall-database/repo_root` (main@ec7672bc4358) | PR #17@7e437de57578 | 9.6.1 |
| `TavallStudios/tavall-di` | `/srv/dev-storage/workspaces/tavall-di/repo_root` (main@d8ecc0230252) | PR #13@1b638153f114 | 9.6.1 |
| `TavallStudios/tavall-discord` | `/srv/dev-storage/workspaces/tavall-discord/repo_root` (main@a37665d66b27) | PR #6@5cc474a13c5f | 9.6.1 in PR #6 (selected local ref pending) |
| `TavallStudios/tavall-docs` | `/srv/dev-storage/workspaces/tavall-docs/repo_root` (working/tavall-ci-evidence-provenance-20260925@9dd0803bb17b) | local `working/tavall-ci-evidence-provenance-20260925@9dd0803bb17b` | no Gradle build on selected ref |
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
- The approved Cloud Executor Java is `/opt/jdk-25.0.1`. Its shared execution surface maps `/var/cache/tavall-local-sandbox/gradle` to `/tavall/shared-tools/gradle`; the live service sets `GRADLE_USER_HOME=/tavall/shared-tools/gradle`. The durable sandbox service is active. The `DEVELOPMENT_SHARED` runner has a separate Tavall-owned shared cache at `/srv/dev-storage/tavall-cache/shared-ci/gradle`, selected by `/usr/local/libexec/tavall-development-shared-ci` and isolated from per-job HOME/output state. Both are executor-owned shared caches, not repository identity. Project `.gradle` state under current canonical source roots, exact-source shared-dependency materializations, and the blocked DEVELOPMENT Environment were retained as active or unknown; no source worktree was removed.
- Cache classification from current configuration: `/var/cache/tavall-local-sandbox/gradle` is canonical/current and active; `/srv/dev-storage/tavall-cache/shared-ci/gradle` is active for the existing shared-CI provider; `/srv/dev-storage/tavall-cache/host-local-sandbox/gradle` is an empty but still referenced provider cache, retained. `/var/lib/tavall-local-sandbox/home/.gradle` (155 MB, last wrapper distribution files from 2026-08-15) and 86 aged operation-home `.gradle` caches (1.58 GB total, owned by `tavall-sandbox`, last modified 13.4–28.6 days ago) were retired after confirming no running Gradle process or active sandbox unit used those Gradle homes. The operation directories and evidence/source files remain. The user-owned `/home/ubuntu/.gradle` cache used by local validation was preserved.
- Tavall CI remains a typed `GRADLE` executor. The exact-source composite planner records repository/SHA identities and source manifests. Maven Local, mutable sibling substitutions, and SNAPSHOT workspace references are not the internal dependency contract.

## GitHub Actions ownership audit

The current open-PR audit found 27 branches that delete `.github/workflows/*` files used for Tavall build, test, release, integration, or source-based deployment work. The exact CI migration branches in the repository table retire build/test workflows; private `publish.yml` jobs for internal artifacts are retired where exact-source or immutable Tavall artifact composition replaces them. These PRs remain unmerged, so default-branch retirement is not claimed.

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
| `tavall-cloud-chatgpt-plugin` | Template exists; live service is DEVELOPMENT/SINGLE and carries a legacy SNAPSHOT artifact (`ba454965…`) with blank CI run/evidence IDs. It is not a rollout candidate. |
| `tavall-cloud-control` | Template exists; CONTROL_PLANE is RUNNING but its current bootstrap has no immutable Tavall CI artifact lineage and CD remains manual. It was not redeployed. |
| `novus-ffa-east-backend` | Registry entry is RUNNING desired / UNKNOWN observed; no canonical service template was found and Cloud reports invalid CD request. No template was guessed. |
| `tavall-cloud-redis` | Infrastructure service; no application `.tavallcd` required. |
| `tavall-cloud-storage-prepare` | Infrastructure service; no application `.tavallcd` required. |

PR #14 binds frozen artifact, exact source, build/CI evidence, template identity and digest, runtime identity, deployment generation, and typed readiness into the existing Cloud CLI flow. PR #395 adds Cloud runtime-instance isolation, durable `.tavallcd` deployment lineage, generation-fenced readiness observations, standby deployment, and an exact-bundle authorized production promotion command. These branches preserve the existing `tavall service deploy` and CONTROL path.

## Live validation boundary

The existing DEVELOPMENT Environment was re-resolved to current exact heads and preserves its established identity and policies. It remains **BLOCKED**: CONTROL reports WORKSPACE and DEVELOPMENT_TOOL as `UNKNOWN`. A read-only repository operation returns `STALE_VERSION` for the environment-owned `TavallStudios/tavall-ci` path because that clean checkout is at `ef59a10f97668bf38f47616649353e8cca1199bb` while the snapshot requests `f3ad7942eb775a232e1e92a91a6baf101cac1444`. The old commit is an ancestor of the requested commit and the origin/branch match. PR #395 adds fail-closed recovery that advances only a clean, same-origin, same-branch fast-forward; dirty or divergent checkouts remain blocked. The installed Agent has not been updated to that PR head, and its job command does not expose the new serialized-plan input.

No Tavall CI Cloud job, immutable artifact, frozen delivery bundle, DEVELOPMENT deployment, STAGING readiness evidence, or production promotion was produced. The live service and production traffic were not changed. The existing service registry and templates are not being treated as proof of rollout deployment.

## Validation evidence

- Cloud focused core/node/ChatGPT suites on the PR source: **658 tests, 0 failures, 0 errors, 2 skipped sandbox tests**.
- Cloud `:tavall-cloud-test-suite:architectureTest` fails with 120 existing findings: 44 repository-role, 34 direct-thread, and 42 production-`var` violations across unrelated Cloud modules. The changed clean-worktree recovery provider is not listed; no Architecture Test pass is claimed.
- Tavall CI full `check`, its Architecture Tests suite, and runtime distribution packaging passed on Java 25 / Gradle 9.6.1 with exact Cloud API and Architecture Tests composites (46 actionable tasks in the prior validation run).
- Exact-head CI definition planning: **60/60 pass**, correct source identity, zero plan failures. This does not claim any configured repository build ran.
- Live Cloud status: Agent, Control, and developer storage are ready; the selected DEVELOPMENT Environment remains blocked as described above.
- `tavall-docs` checked-in architecture/progression exports are updated through PR #31. This client has no live Notion connector, so Notion was not written or represented as updated.

## Open rollout pull requests

- [`tavall-cloud#395`](https://github.com/TavallStudios/tavall-cloud/pull/395) — current head `2f061cd9f42cd4f44c813d3f8aa0e62b50d1ddac`, Draft, base `staging/runtime`.
- [`tavall-ci#14`](https://github.com/TavallStudios/tavall-ci/pull/14) — current head `f3ad7942eb775a232e1e92a91a6baf101cac1444`, Draft, base `staging/platform`.
- [`tavall-docs#31`](https://github.com/TavallStudios/tavall-docs/pull/31) — existing evidence-provenance branch, updated by this record and the architecture clarification.
- Source-owned `.tavallci` and wrapper work remains in the 60 existing PR heads shown above; no duplicate source PRs were opened.

## Remaining blockers

- **Architecture/design:** none found that prevents preserving the agreed ownership model.
- **Implementation:** install the exact Cloud Agent recovery and serialized-plan support through the existing immutable-artifact/CONTROL authority path; complete any required GitHub Bot application composition before treating event ingress as operational.
- **Validation:** clear the existing Cloud Architecture Tests backlog and run representative exact Gradle jobs on the real Tavall Cloud Executor; validate shared-cache concurrency there.
- **Deployment:** provision an immutable bootstrap artifact for `tavall-cloud-control`, repair the exact-source Environment via updated CONTROL, then produce artifact/bundle lineage, DEVELOPMENT readiness, and STAGING readiness.
- **External/provider:** no GitHub provider outage was observed. Live Notion update remains unavailable in this client.
