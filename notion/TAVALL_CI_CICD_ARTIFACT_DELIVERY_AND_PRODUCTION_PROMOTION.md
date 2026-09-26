<page url="https://app.notion.com/p/3d838458ddfd81b1b7d0ecfdcde18d3d" icon="🚦">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3d538458ddfd81499004db3381c81444" title="Platform & Infrastructure"/>
<ancestor-2-page url="https://app.notion.com/p/3d538458ddfd81b9984cd65f01c92e27" title="Tavall"/>
</ancestor-path>
<properties>
{"title":"Tavall CI — CI/CD, Artifact Delivery & Production Promotion"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"🚦"}</iconMetadata>
<content>
<callout icon="🚦" color="green_bg">
	**Status:** `TavallStudios/tavall-ci` is canonical for reusable CI/CD policy. Tavall CI main is `00ac2dad0c5c3854357d9cf6252c7962885d1159` after extraction PR #2, P1 hardening successor #3, file-bound provider/Architecture Tests alignment PR #5, and staging PRs #4 and #6. Cloud executable ownership cleanup is merged at `277c13dcd9cdd5d114a6aa829764775fa539dc21` and final Cloud documentation is merged at `32811a30a9f6d091f03f5ab1a160ccde022d3263`. Final Cloud DEVELOPMENT validation used durable environment `ca9d8873-9a9b-4faf-b3cd-9f582630033b` and job `afd86507-8421-4d3a-a729-6b08c61215d1`: exact `tavall-ci@main` source `00ac2dad`, Java 25, Gradle 9.6.1, file-bound GitHub Packages credential, `SUCCEEDED`, exit 0, and verified sandbox destruction.
</callout>
## Purpose
Make `TavallStudios/tavall-ci` the reusable Tavall Continuous Integration and Continuous Delivery system. Tavall Cloud provides execution, lane/environment/node placement, sandboxing, console, deployment, service-runtime, and storage capabilities through an explicit provider boundary; it does not own CI/CD policy.
## Module Boundary
- `TavallStudios/tavall-ci` owns reusable CI orchestration, exact-source organization aggregation, dependency/source validation, version/build identity, typed evidence, architecture-test orchestration, Continuous Delivery, and promotion logic. `tavall-ci-runtime` is the executable/application boundary; there is no generic CI `core` module.
- `tavall-ci-cd` owns candidate delivery, deployment evidence, readiness gates, rollback preparation, and promotion orchestration. `tavall-ci-cloud` is the provider/adapter boundary into existing Tavall Cloud capabilities and must not recreate Cloud execution, environment, lane, node, console, deployment, Docker, or Kubernetes machinery. It invokes the target-aware Tavall service deployment/scaling path in <mention-page url="https://app.notion.com/p/3d938458ddfd8138a2c8d60217396971"/>.
## Delivery Model
1. Materialize exact source in an authorized DEVELOPMENT environment.
2. Run scoped build/tests/architecture checks and produce immutable artifact identity.
3. Freeze a delivery bundle that binds source, artifact digests, runtime selection, validation evidence, and deployment instructions.
4. Test the deployment/promotion script in DEVELOPMENT before formal STAGING.
5. Compose required runtime candidates through Development Staging and the Combined Runtime Staging PR.
6. Deploy the production-equivalent candidate to STAGING and run readiness/acceptance.
7. Require explicit human production authorization.
8. Promote through the production A/B slot model, retaining last-known-good rollback.
## Node Model
Any Tavall node with an authorized executor can perform bounded CI/CD work. Templates/artifacts may be distributed from Tavall storage; placement is chosen by Cloud rather than hard-coding a single "CI server."
## Data Safety
Scoped testing may exercise real production-shaped infrastructure, but must explicitly protect player/user data. Destructive validation must use isolated or non-production data boundaries unless a production-safe read/projection path is specifically designed.
## Evidence Contract
Every promotion should be explainable from exact source → tests → artifact digest → deployment generation → readiness → authorization → active production slot. PR status alone is not release evidence.
## Direct Java Caller Boundary & Remaining Extraction — recovered 2026-09-19
**RECOVERED DESIGN / implementation in progress.** Tavall CI's canonical reusable surface is a typed Java CI capability. Same-JVM Tavall callers should submit/inspect CI through that Java boundary directly; CLI/application/transport surfaces adapt the same semantics rather than becoming independent CI implementations.
Independent processes such as `tavall-github-bot` use a narrow typed client/ingress over the same CI identities and evidence. They must not reconstruct Cloud command payloads, Cloud Job arguments, provider internals, or repository-specific Gradle graphs.
Current active implementation evidence is Tavall CI PR #7 (`working/github-bot-boundary-20260918` -> `staging/platform`, recovered head `72ac256f0f58463b31c634a532c48d507b2e8b5f`), which introduces `CiRunSubmission`, `CiRunResult`, `CiExecutionRequestResolver`, and `CiRunCoordinator` plus exact-source origin/profile fencing. Continue/reconcile this lineage rather than replacing it with a parallel caller model.
A committed `tavall-ci-api` module is now **VERIFIED IN CODE** after PR #7 merged into `staging/platform` at `a5f8919e6511ea0f6fbd6407d3c11b7f278ccba8`. It contains the smallest caller contracts (`CiCallerService`, `CiRunSubmission`, and `CiRunResult`) and does not contain Cloud execution, GitHub, Gradle, deployment, or application bootstrap. This supersedes the earlier “no committed module” snapshot.
The CI/CD ownership extraction is **not fully operationally complete** while Tavall Cloud still owns reusable CI semantic types such as CI origin/profile/invocation/request policy. Cloud should retain provider/runtime concerns (environment/executor selection, bounded sandbox/shared execution, credentials projection, logs/artifact storage, placement/resource bounds), while reusable CI check/profile/source/build/release/promotion semantics live in Tavall CI.
**Execution update 2026-09-19:**
- **VERIFIED IN CODE:** PR #7's typed caller boundary and `tavall-ci-api` are merged; Cloud PR #287 removed the deleted `CloudDeveloperCi*` types and retained provider/runtime concerns.
- **VERIFIED IN TESTS:** Tavall CI staging `check` passes; the exact-head `scripts/ci/run --profile all` path now passes with `TAVALL_ARCHITECTURE_TESTS_BUILD` propagated by PR #8 at `b8e94ea0df5789c84529d0aca9ff3c263a60901b`.
- **NOT VERIFIED LIVE:** a concrete Tavall CI Cloud provider transport and GitHub Bot end-to-end Check publication are not yet proven; GitHub Bot PR #1 remains the active extraction surface.
Cloud Job IDs are provider metadata beneath Tavall CI evidence, not the semantic CI identity published to callers or GitHub. GitHub Checks are bound to exact source/head and represent executable Tavall CI evidence only.
## Current Implementation
Tavall Cloud PR #230/#257 introduced the first CI/CD implementation. That implementation has now been replaced as the reusable policy owner: `TavallStudios/tavall-ci` main owns exact-source aggregation, distinct source/release/build/resolution identities, explicit dependency modes, Gradle composite/source substitution, typed evidence serialization, frozen delivery bundles, readiness, human authorization, A/B promotion, and rollback policy. Cloud PR #261 and staging PR #262 removed the duplicate Cloud modules and active writer while retaining environment-owned LOCAL_CI, placement, executors, sandboxing, Console, deployment/scaling, Docker/Kubernetes, storage, and service lifecycle. Development candidate composition uses exact repository + exact SHA source identity rather than an implicit cross-repository `SNAPSHOT` protocol.

## Execution update 2026-09-26 — exact Git source materialization
- **VERIFIED IN CODE:** Tavall CI PR #14 at `6890de3048939953bbc53624a76f0069c2113132` implements a Git materializer behind the existing source-materialization contract. A source locator supplies the remote/ref; CI verifies the requested SHA and Git tree digest, isolates each request's checkout, and releases those trees after planning/evidence persistence.
- **VERIFIED IN TESTS:** Java 25 / Gradle 9.6.1 TCI `check` passes with exact Architecture Tests source `c0863bfe` and exact Cloud API source `ff727c5d`; source-provider, cleanup, request-replay, and architecture tests pass.
- **NOT VERIFIED LIVE:** the materializer is not wired into an independent GitHub Bot caller or live Cloud source binding. The current DEVELOPMENT CI Environment remains `BLOCKED`; no new Cloud CI artifact, delivery bundle, DEVELOPMENT deployment, or STAGING readiness was produced by this implementation checkpoint.

## Source Evidence
- [Tavall CI main](https://github.com/TavallStudios/tavall-ci/tree/main) — `00ac2dad0c5c3854357d9cf6252c7962885d1159`
- [Tavall CI implementation PR #2](https://github.com/TavallStudios/tavall-ci/pull/2) — merged into staging
- [Tavall CI P1 hardening successor PR #3](https://github.com/TavallStudios/tavall-ci/pull/3) — merged into staging at `149b7cc`
- [Tavall CI staging PR #4](https://github.com/TavallStudios/tavall-ci/pull/4) — merged to main at `e9d6787`
- [Tavall CI provider credential/Architecture Tests PR #5](https://github.com/TavallStudios/tavall-ci/pull/5) — merged into staging at `6796c09`
- [Tavall CI staging PR #6](https://github.com/TavallStudios/tavall-ci/pull/6) — merged to main at `00ac2d`
- [Tavall CI staging PR #1](https://github.com/TavallStudios/tavall-ci/pull/1) — superseded by #4/#6
- [Tavall Cloud ownership cleanup PR #261](https://github.com/TavallStudios/tavall-cloud/pull/261) — merged into staging
- [Tavall Cloud staging PR #262](https://github.com/TavallStudios/tavall-cloud/pull/262) — executable cleanup merged to main at `277c13d`
- [Tavall Cloud documentation staging PR #265](https://github.com/TavallStudios/tavall-cloud/pull/265) — final Cloud main at `32811a3`
- [Tavall Cloud CI/provider PR #267](https://github.com/TavallStudios/tavall-cloud/pull/267) — exact-source workspace materialization, merged into staging at `05fee507`
- [Tavall Cloud CI credential PR #268](https://github.com/TavallStudios/tavall-cloud/pull/268) — file-bound package credentials, merged into staging at `ee4e765`
- [Tavall Cloud sandbox/runtime PR #269](https://github.com/TavallStudios/tavall-cloud/pull/269) — transient sandbox unit scope, merged into staging at `39a3bd4`
- [Tavall Cloud storage projection PR #270](https://github.com/TavallStudios/tavall-cloud/pull/270) — configured DEVELOPMENT storage scope, merged into staging at `ed63610`
- [Tavall Cloud sandbox compatibility PR #272](https://github.com/TavallStudios/tavall-cloud/pull/272) — lifecycle metadata compatibility, merged into staging at `8fb011e`
- [Tavall Cloud current sandbox child PR #273](https://github.com/TavallStudios/tavall-cloud/pull/273) — merged into operator/runtime PR #266
- [Tavall Cloud exact-source materialization child PR #274](https://github.com/TavallStudios/tavall-cloud/pull/274) — merged into operator/runtime PR #266
- [Tavall Cloud sandbox transient-unit child PR #275](https://github.com/TavallStudios/tavall-cloud/pull/275) — merged into operator/runtime PR #266
- <mention-page url="https://app.notion.com/p/3d838458ddfd81d29188edb39c470113"/>
## Documentation Links
### Design Source(s)
- [DEVELOPER_JOB_AND_LOCAL_CI_FINAL_DRAFT.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/architecture/DEVELOPER_JOB_AND_LOCAL_CI_FINAL_DRAFT.md)
- [SERVICE_DEPLOYMENT_FINAL_DRAFT.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/deployment/SERVICE_DEPLOYMENT_FINAL_DRAFT.md)
- <mention-page url="https://app.notion.com/p/3d838458ddfd81d29188edb39c470113"/>
### Final / Canonical Documentation
- **Not finalized yet.** Current CI/deployment candidates are the Final Drafts above and the Cloud system Final Draft.
### Progression / Evidence Documentation
- [SERVICE_DEPLOYMENT_PROGRESSION.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/deployment/SERVICE_DEPLOYMENT_PROGRESSION.md)
- [TAVALL_CLOUD_PROGRESSION.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/progression/TAVALL_CLOUD_PROGRESSION.md)
### Implementation
- Historical source: `TavallStudios/tavall-cloud` → `tavall-cloud-ci` + `tavall-cloud-cd` from PR #230/#257; those Cloud modules are retired.
- Canonical destination: `TavallStudios/tavall-ci` main at `00ac2d`, with `tavall-ci-runtime` as the application boundary and capability-named modules/adapters beneath it.
- Canonical architecture tests: `TavallStudios/Tavall-Architecture-Tests` current main, consumed through `tavall-ci-test-suite` against real Tavall CI production source/classes rather than copied into Tavall CI.
- Cloud provider boundary: `Tavall Cloud` main at `32811a3` retains infrastructure/runtime execution and bounded environment-owned LOCAL_CI only.
---
## DOC TODO:
### Document next steps
- [ ] Reconcile the older local-CI/deployment Final Draft terminology with Runtime PR, Development Staging, Combined Runtime Staging, formal STAGING, and production A/B.
- [ ] Promote accepted CI/CD/deployment contracts through the documentation lifecycle and replace candidate links with Finals.
- [ ] Keep progression/evidence tied to exact source/artifact/deployment generations.
### System next steps
- [ ] Finish the operational Tavall CI caller/API cutover and remove remaining reusable CI semantic ownership from Tavall Cloud. The reusable CI/CD module extraction is merged; Cloud retains provider/runtime execution only.
- [x] Validate exact-source cross-repository aggregation, explicit source/release/build-policy/resolution identities, typed check classification/evidence, canonical architecture-test execution, frozen delivery bundles, formal staging gates, human production authorization, A/B promotion, and rollback in repository/consumer tests.
- [x] Complete the Cloud DEVELOPMENT LOCAL_CI profile for the exact promoted Tavall CI main source; durable job `afd86507-8421-4d3a-a729-6b08c61215d1` returned `SUCCEEDED` with exit 0 after Java 25, Gradle 9.6.1, current Architecture Tests, exact-head fencing, file-bound package credentials, and verified sandbox teardown.
- [ ] Prove scoped production-shaped tests cannot mutate protected user/player data outside authorized boundaries.
## Execution update 2026-09-19 — caller and provider evidence reconciliation
- **VERIFIED IN CODE:** `tavall-ci-api` and PR #7's typed caller boundary remain the canonical same-JVM contracts; PR #8 propagates the local Architecture Tests provider through `scripts/ci/run`.
- **VERIFIED IN TESTS:** the exact-head `scripts/ci/run --profile all` path passes with the local Tavall Architecture Tests build; `tavall-github-bot` PR #1 passes its full local Gradle check after its architecture/test-runtime corrections.
- **VERIFIED LIVE:** the existing Cloud agent, GitHub bridge, and bot services are running; Cloud PR #288's provider path now reaches exact-source Job authority after cache repair.
- **NOT VERIFIED LIVE:** an independent `tavall-github-bot` typed ingress through Tavall CI to an exact-head GitHub Check is still not proven. PR #1 remains draft and the existing Cloud-owned Bot path remains active; no premature cutover is claimed.
## Current Cloud execution-state contract
Tavall CI owns CI semantics, profiles, source/build policy, typed evidence, and delivery/promotion semantics. Tavall Cloud owns provider execution, environment/executor placement, live Job lifecycle, Redis coordination, Storage materialization/evidence, and runtime recovery. `tavall-ci-cloud` is the typed adapter; Tavall CI does not access Cloud Redis or PostgreSQL keys directly.
PostgreSQL Job/environment rows are historical/audit projections only for this execution boundary. A Cloud Job ID is provider metadata inside Tavall CI evidence, not CI semantic identity.
## Execution update 2026-09-20 — live Cloud-backed CI evidence
- **VERIFIED IN CODE:** Cloud staging authority cutover integrated at `79f1e31751ea55b4208e42b1f25a9c88f895143f`; Tavall CI main remains exact `00ac2dad0c5c3854357d9cf6252c7962885d1159`.
- **VERIFIED LIVE:** typed Cloud-backed Job `37a06859-22fd-4d49-a9d5-b14a012213f3` ran `tavall-ci/manual/all` through `DEVELOPMENT_SHARED`, returned `SUCCEEDED` exit 0, and wrote Storage evidence with expectedHead == actualHead `00ac2dad…`, `gradlew clean check`, `failureClass=NONE`, and empty stderr. Final state/evidence survived Cloud agent restart.
- **VERIFIED LIVE:** cancellation Job `cb9e3c41-8f9b-44cd-8cd2-3a03c4a2bc62` returned `CANCELLED`; the earlier stale-materialization attempt was truthfully classified `SOURCE_FAILED`/exit 126.
- **NOT VERIFIED LIVE:** independent `tavall-github-bot` typed ingress through Tavall CI to an exact-head GitHub Check, including the mandatory A-to-B race proof, remains unresolved. GitHub Actions is not used as compute.
## Execution update 2026-09-20 — integrated staging and Bot boundary
- PR #8 was merged through `staging/platform` with expected head `b8e94ea0df5789c84529d0aca9ff3c263a60901b`; integrated head: `1482aec5b2e4ab915d616ee9aa8a53bd57730c7d`.
- Exact integrated CI validation passed: `./gradlew check`, `:tavall-ci-test-suite:check`, and `scripts/ci/run --profile all` with `actualHead == expectedHead` and `failureClass=NONE`. The run used the canonical Architecture Tests composite provider and produced durable evidence metadata.
- The live Cloud-backed CI path remains proven by Job `37a06859-22fd-4d49-a9d5-b14a012213f3`: exact repository `TavallStudios/tavall-ci`, exact source `00ac2dad0c5c3854357d9cf6252c7962885d1159`, Cloud execution provider `DEVELOPMENT_SHARED`, exit code `0`, storage evidence `tavall-storage://dev-storage/jobs/37a06859-22fd-4d49-a9d5-b14a012213f3`, and logs available after runtime restart.
- The Bot exact-head A-to-B race test is persisted at PR #1 head `cbd4001`; the stale result is rejected without Check publication. Independent live Bot ingress and Check publication remain unresolved because Tavall CI currently exposes only in-process caller/provider contracts; no raw Redis, PostgreSQL, Cloud command, or GitHub Actions fallback is authorized.
## Documentation fence update 2026-09-20
Cloud authority-language fence PR #289 is integrated at `staging/runtime` head `58e2c7817ddd675a59293742557ae0f6289b2be8`; CI documentation remains aligned with the typed Cloud boundary and does not claim raw Redis/PostgreSQL ownership.
## Historical-plan fence update 2026-09-20
Cloud PR #290 is integrated at `staging/runtime` head `25a8d546ad3ec7a00967da9a82b73d2bb1b5d4eb`; legacy plans now clearly mark superseded PostgreSQL live-authority wording while preserving the CI/Cloud ownership boundary.
## Authority correction 2026-09-20 — CI/Cloud has no PostgreSQL state
Tavall CI owns CI semantics, exact-source identity, profiles, checks, and evidence semantics. Tavall Cloud owns Redis execution state and Tavall Storage/filesystem materialization/evidence. PostgreSQL is not used by the current Tavall Cloud runtime and is not a CI, Job, environment, audit, or fallback authority. Legacy PostgreSQL source/migration artifacts are provenance only and current code must not read or write them.
Integrated Cloud staging/runtime: `c7d5db81332f330c5d9987e9c16921a6090ca1ca`.
Live exact-source Cloud-backed CI proof: Job `9b74d8a9-2385-464f-a7f5-91f022db4917`, repository `TavallStudios/tavall-ci`, source `00ac2dad0c5c3854357d9cf6252c7962885d1159`, provider `DEVELOPMENT_SHARED`, exit `0`, `failureClass=NONE`, durable Storage evidence `tavall-storage://dev-storage/jobs/9b74d8a9-2385-464f-a7f5-91f022db4917`; Agent restart recovery preserved the final state. Cancellation proof: Job `2a5c445c-b66f-46dd-a60e-e59834ef1dc4` => `CANCELLED`.
## Final source reconciliation 2026-09-20
Cloud staging/runtime is `15434688b6f61753df30471806f65060e1f46e89`; the active Cloud source graph has no PostgreSQL runtime dependency or PostgresCloud/IPostgresDatabase implementation references. CI remains behind the typed Cloud execution boundary and does not own Redis internals or any database state.
## Final integrated validation 2026-09-20
Tavall Cloud staging/runtime `15434688b6f61753df30471806f65060e1f46e89` passed the full Cloud validation graph with no PostgreSQL runtime sources. The live typed CI execution through Cloud remains proven by Job `9b74d8a9-2385-464f-a7f5-91f022db4917` at exact source `00ac2dad0c5c3854357d9cf6252c7962885d1159`, exit `0`, `failureClass=NONE`, durable Storage evidence, restart recovery, and cancellation proof Job `2a5c445c-b66f-46dd-a60e-e59834ef1dc4`.
## Final deployment proof 2026-09-20
Exact final Cloud staging/runtime `15434688b6f61753df30471806f65060e1f46e89` is deployed with matching Agent artifact SHA-256 `27f2bec683d47df874a319626cfd670fa12f50e65b379cffda2b5408baf2ddb1`. Agent is READY and final Console/Cloud execution remains Redis-only; no PostgreSQL Cloud runtime source or dependency remains.
## Authority correction 2026-09-20 — Redis-only Cloud execution
Tavall CI owns CI semantics and evidence semantics; it does not own Cloud state. The typed tavall-ci-cloud boundary submits to Tavall Cloud, which owns execution through Redis-backed Job/runtime state and materializes durable logs/evidence through Tavall Storage/filesystem.
PostgreSQL is not used by Tavall Cloud or Tavall CI for execution, audit/history authority, fallback, generation reconstruction, or CI control. Any older PostgreSQL wording in this page is historical provenance and is superseded by this section. CI must not access raw Redis keys or introduce a database state model; it uses the typed Cloud provider/client boundary.
## Execution update 2026-09-20 — final Cloud-backed CI boundary
Cloud staging/runtime is integrated at 2858ae2a576d77a4a2fee162a776d5d7425d4752 after PR #299. The typed Cloud Job proof for TavallStudios/tavall-ci exact SHA 00ac2dad0c5c3854357d9cf6252c7962885d1159 completed through DEVELOPMENT_SHARED with SUCCEEDED/exit 0 and Storage evidence handle tavall-storage://dev-storage/jobs/37495124-5d00-4989-a6e1-c9e694460e06. Redis-only Cloud state survived Agent restart.
Tavall CI remains the owner of CI semantics/evidence; Cloud owns Job execution/runtime coordination. No raw Redis or PostgreSQL access is permitted in CI. Independent tavall-github-bot live ingress/exact-head Check publication remains unresolved and is not claimed complete.
## Promotion update 2026-09-20 — Cloud main
The validated Redis-only Cloud staging/runtime tree was promoted through existing PR #285 to main merge 225f952e70f70c12fb2a18c3da17a24da283c683. This does not claim independent GitHub Bot ingress/Check E2E; that remains a separate open boundary.
## Rollout checkpoint 2026-09-26 — typed Cloud transport and live gate
- **VERIFIED IN CODE:** Tavall CI PR #14 head `565e870e0160c38780d09ed83de682da5bffc19b` adds provider-neutral exact Git source materialization and typed Tavall Cloud CLI job/evidence adapters. Tavall Cloud PR #395 head `6c314ce65dd7f15b9df312ea1384e62a03bd0689` exposes job-evidence `put/get` through CONTROL Storage and binds each record to the exact Environment, repository, source revision, durable job, frozen plan, and content identity.
- **VERIFIED IN TESTS:** Tavall CI `check` passes on Java 25 / Gradle 9.6.1 with exact Architecture Tests source `c0863bfe`. Cloud focused Storage/CLI tests pass. The Cloud architecture suite is red for repository-type, production-var, and direct-thread-creation violations; no full Cloud architecture pass is claimed.
- **VERIFIED IN LIVE CONTROL:** Existing DEVELOPMENT Environment `5848c5ff-a2a2-4da4-bd25-9cff8e558433` was re-resolved to exact source snapshot `29ce13c6e19db68a295f4106e728044f7febda8375a47aff85ae1f64121ef694` (Architecture Tests `c0863bfe`, Tavall CI `565e870e`, Tavall Cloud `6c314ce6`). DURABLE lifecycle, DEDICATED work, SHARED services, and inherited resources were preserved.
- **BLOCKED LIVE:** The Environment remains `BLOCKED`; workspace and development-tool components are `UNKNOWN`. The installed Agent/CLI does not expose the plan-bound job fields or typed Storage evidence commands from these PR heads. No new CONTROL job, artifact, frozen bundle, DEVELOPMENT deployment, or STAGING readiness evidence was produced. Production remains unchanged.
- **VERIFIED IN PLAN:** Tavall CI's current planner accepted `.tavallci/ci.yaml` from 57 active PR heads at their exact source SHAs. This includes all seven designated remote-only repositories; none received a canonical local workspace. PR branches are unmerged and plan results do not claim builds or artifacts. Planning caught a missing `selector: gitlink` in Tavall Java Tools PR #3; the selector was added at head `e3dee56` and that definition now plans successfully.
- **WRAPPER AUDIT:** all 34 Gradle PR definitions specify Java 25 / Gradle 9.6.1, and their exact heads contain `gradlew`, `gradle-wrapper.jar`, and `gradle-wrapper.properties` pointing to Gradle 9.6.1. Across the 57 definitions, build types are 34 Gradle, 3 Node, 19 `none`, and 1 Shell.
- **SOURCE BLOCKER:** `TavallStudios/tavall-roblox` is the only non-excluded organization repository with no commit and no default branch. It has no source identity to materialize or validate; no initial source or replacement workspace was created.
- **GITHUB ACTIONS:** the exact PR inventory contains 27 workflow-file removals across active CI branches. Tavall-MC PR #271's branch also removes its Gradle/runtime/deployment workflows while preserving the unrelated upstream-PR source automation, but GitHub currently reports the PR `CONFLICTING` against a base 378 commits ahead; those removals are not integrated. The Architecture Tests source-integrity check and Java Tools gitlink-sync workflows were retained as SCM/source-maintenance automation, not build/test compute.
- **NOT VERIFIED:** Independent GitHub Bot caller/runtime wiring remains incomplete; `GitHubBotApplication` is still a stub. GitHub Checks and PR state are not used as release evidence.
- **REPOSITORY ONBOARDING:** Hytale PR #3 head `304304d` carries the repository's Java 25 / Gradle 9.6.1 `.tavallci`, exact-source Tavall dependencies, and retired Maven Local bootstrap. Tavall CI `ci validate` and `ci plan` pass locally for that definition; a Tavall Cloud Executor build is not yet available.
## Exact-source binding addition — 2026-09-26
- **VERIFIED IN CODE:** Tavall CI PR #14 now includes `TavallCloudCliExactSourceBindingProvider` and `composeTavallCloudCli`. The adapter resolves only `required-source` entries from the selected Environment's exact repository/SHA/role snapshot, fences Environment/lane/primary identity and pinned SHAs, and composes it with exact Git materialization, typed job execution, and typed Storage evidence.
- **VERIFIED IN TESTS:** `:tavall-ci-cloud:test` passes with exact Cloud API source `6c314ce6` and Architecture Tests source `c0863bfe`. The 57 active `.tavallci` PR definitions also plan successfully at current exact heads.
- The root TCI `check` was attempted outside the full source-aggregation Executor and stopped before tests because exact Architecture Tests modules were absent from ordinary repositories. This is a dependency-source/bootstrap limitation, not a passing root check.
- DEVELOPMENT Environment `5848c5ff-a2a2-4da4-bd25-9cff8e558433` was re-resolved to snapshot `b6a8b43b314ad2a5b017f271f4974d9562327d13ef66d132ccf14ccca2ea7484` with Architecture Tests `c0863bfe`, TCI `a6872ae`, and Cloud `6c314ce6`. Policies remain unchanged; observed state is still `BLOCKED` with WORKSPACE and DEVELOPMENT_TOOL `UNKNOWN`.
- No CONTROL job, immutable artifact, frozen bundle, DEVELOPMENT deployment, or STAGING readiness has been produced for this candidate. Production is unchanged.
## Live Executor recheck — 2026-09-26
- The lane has one existing DEVELOPMENT Environment; no alternate Environment with the rollout snapshot is available. It was re-resolved to `b15ffefbb6cf4f2beafbad0d30d25b8118be5f4f32c5ddd54a520299a0da3062` to bind TCI PR #14 head `ad695b3` and Cloud PR #395 head `56fb9a66`, preserving DURABLE / DEDICATED / SHARED / inherited resource policy.
- The Environment-owned TCI checkout is clean but at `ef59a10f97668bf38f47616649353e8cca1199bb`, while the snapshot pins `tavall-ci@ad695b3270ac844fbc0db7405c01500bbeef54a7`. Cloud's `environment repository refresh` rejects it with `STALE_VERSION` because the mounted workspace is not the pinned exact source.
- The Environment-owned Cloud checkout is clean at `main@2f1c94b47d38d86a1724067c0ab8be39bd512178`, while the current snapshot pins `tavall-cloud@56fb9a66a79666e09c8a39ee0caaf23c9c5a1f20`. The Architecture Tests shared dependency is present clean at the exact pinned `c0863bfe9e3ea38e4872eb295856e69bed30eb28`.
- A read-only `environment console execute` probe failed before starting a command: Sandbox creation returned `PROVIDER_FAILURE` / exit 125 because `/srv/dev-storage/environments/env-5848c5ff/repositories/TavallStudios/Tavall-Architecture-Tests` is missing or outside the approved DEVELOPMENT root. The Environment still reports WORKSPACE and DEVELOPMENT_TOOL as `UNKNOWN`.
- These probes produced no CI job, build evidence, artifact, delivery bundle, or deployment. Exact-source DEVELOPMENT validation and STAGING readiness remain blocked; production remains unchanged.
## Dedicated Environment execution-path correction — 2026-09-26
- Tavall Cloud PR #395 commit `04d2f2efa52857f1c6ea4a3bda7169a82ed396c8` binds the logical Environment repository path to a clean exact `PRIMARY` workspace at the current source-snapshot generation. `SHARED_DEP` and `ENVIRONMENT_DEP` inputs remain dependencies and cannot become a job/Console workspace.
- An Environment Console request without `repository` now resolves to the `PRIMARY` source explicitly. Tests cover exact-generation link recovery, preservation of stale generations, and primary selection when dependencies sort first.
- These tests have not run at commit `56fb9a66`. The Cloud `.tavallci` runtime profile declares `tavall-cloud-agent` from the existing self-contained `:tavall-cloud-node:allJar` task, which has not been built or published.
## Cloud Agent artifact plan — 2026-09-26
- Cloud PR #395 commit `bf70bd5b1dfa87c69652869a82729394759efa24` declares immutable artifact `tavall-cloud-agent` at `tavall-cloud-node/build/libs/tavall-cloud-agent-all.jar` and runs `:tavall-cloud-node:allJar` in the required runtime profile. This matches the active Agent installer package path.
- The installed Tavall CI runtime accepted the Cloud `.tavallci` definition and plan at digest `ea834befe4e6da9072f93043e61efffde7ac9d54f714f3d0c95a8af77d10b5ee`; this was definition/plan validation only. No Cloud Executor build or artifact publication occurred.
## Service-template identity reconciliation — 2026-09-26
- The registered `tavall-cloud-control` template identity is `services/tavall-cloud-control`, matching the TCI `ServiceRuntimeTemplateLoader` identity. Cloud PR #395 at `56fb9a66` aligns Cloud's metadata store to this provider-neutral identity; the template SHA is `5033fa2b198c3f6c47065eb3e2db202d9203048a350fcda9a240c195b570c9fa` and the TCI loader parsed it.
- The installed Cloud Agent is older and its CD status response omits template identity/runtime fields, so live Cloud hot-load is unverified. The CONTROL service remains MANUAL/disabled with no deployment identity. Production was not changed.
## Immutable service-deployment configuration — 2026-09-26
- Cloud PR #395 at `56fb9a66` removes GitHub URLs, Gradle module names, mutable artifact paths, and build timeouts as required Cloud deployment configuration. Cloud deploy metadata now binds the canonical source owner/repository, exact revision, `.tavallcd` artifact selector, artifact digest/reference, CI run/evidence, frozen bundle digest, and matching template identity/hash.
- The changed Cloud production classes compile against the available module outputs. Cloud unit tests and real deployment validation remain unrun; the current Agent/Environment does not provide the plan-bound job or exact source materialization.
## CD adapter and runtime-slot validation — 2026-09-26
- TCI PR #14 head `ad695b3` now freezes the selected immutable `ArtifactIdentity` in `DeliveryBundle`, including artifact name/version, exact source, digest, channel, and immutable storage reference; focused `:tavall-ci-cd:test` passes on Java 25 / Gradle 9.6.1 in an isolated local build directory. This is not Cloud Executor validation.
- Current TCI code still has no deployment adapter in `tavall-ci-cloud` to invoke Cloud's existing `service deploy plan/apply/verify/rollback` operations with that frozen identity.
- Cloud PR #395 adds exact deployment-lineage validation to the Cloud provider, but the installed CLI predates those arguments. Its live `service deploy` help does not expose source repository, bundle digest, or service-template identity/hash inputs.
- Cloud's current managed provider activates one `current` release symlink. No Cloud service runtime-slot state or stable-service traffic-switch implementation was found for the plugin template's `A_B` policy. The template records intent; it is not evidence that production A/B is implemented.
- Local combined TCI CD/Cloud tests could not configure because the exact-source Architecture Tests plugin was unavailable in the ordinary build context. Typed `executor ci run` was rejected without CONTROL Environment context; the Environment Console request failed `STALE_VERSION` because its TCI checkout is not at pinned `ad695b3`. No Cloud CI artifact, delivery deployment, readiness, or promotion was produced; production remains unchanged.
## Source CI onboarding follow-up — 2026-09-26
- The current GitHub inventory has 55 repositories: 47 canonical `/srv/dev-storage/workspaces/<repo>/repo_root` mappings, seven explicit remote-only repositories, and excluded `TavallMonoRepo`. `tavall-roblox` has an empty GitHub repository and empty local clone with no source commit.
- Current canonical checkout heads now contain 17 `.tavallci/ci.yaml` definitions. Additional definitions are in open source PRs, including Tavall AI #44 and Custom Enum #8; the earlier 57 active definitions were plan-validated at their exact PR heads.
- Tavall-MC Bot Testing PR #6 adds a Node profile using its exact `package-lock.json`, `npm ci --ignore-scripts`, and existing `npm test`. The current TCI parser accepts the source/build/check definition; local Node `22.22.0` install and layout validation pass. No Cloud Executor evidence exists for this PR.
- The Bot Testing repository's existing `ubuntu-latest` workflow remains in place until Tavall CI can project a replacement check. The `tavall-github-bot` caller PR #1 remains a Draft stub, so removing the current Action now would remove its only live CI check.
</content>
</page>
