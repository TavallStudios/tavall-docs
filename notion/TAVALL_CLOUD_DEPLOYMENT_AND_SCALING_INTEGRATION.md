<page url="https://app.notion.com/p/3d938458ddfd8138a2c8d60217396971" icon="🚀">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3d538458ddfd81499004db3381c81444" title="Platform & Infrastructure"/>
<ancestor-2-page url="https://app.notion.com/p/3d538458ddfd81b9984cd65f01c92e27" title="Tavall"/>
</ancestor-path>
<properties>
{"title":"Tavall Cloud — Deployment & Scaling Integration"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"🚀"}</iconMetadata>
<content>
<callout icon="🚀" color="blue_bg">
	**Status:** active integration decision. This page connects existing Tavall Cloud authorities; it does not redefine environments, nodes, CONTROL, storage, CI/CD, or provider internals.
</callout>
## Purpose / Integration Point
Deployment and scaling are Tavall orchestration operations over existing Cloud targets. This page adds the missing connective contract between <mention-page url="https://app.notion.com/p/3d838458ddfd8199aabccb87f2fc82ca"/>, <mention-page url="https://app.notion.com/p/3d538458ddfd81ed9429e68cd1d9952c"/>, <mention-page url="https://app.notion.com/p/3d838458ddfd8169bb49e929826651cc"/>, <mention-page url="https://app.notion.com/p/3d838458ddfd81b1b7d0ecfdcde18d3d"/>, and <mention-page url="https://app.notion.com/p/3d838458ddfd817998becb19aaded57e"/>.
## Decisions Introduced or Corrected
- **Tavall targets are the public deployment model.** Normal operations use `tavall service deploy ...` and `tavall service scale ...`. A deployment or scale operation resolves an existing lane, environment, node, or service scope when that target type is valid for the operation.
- **Reuse existing type and capability authority.** Target resolution consumes the machine, virtual, node, environment-resource, provider, and capability models already owned by Tavall Cloud. It must not introduce a parallel host/runtime enum merely for deploy or scale.
- **Mutable desired state is normal.** In a MUTABLE environment, changing source revision, template revision, image, service configuration, runtime topology, or instance count updates desired state inside the same environment. Environment identity stays stable while generation/evidence advances. Exact source revision, generation, configuration/source digest, artifact/image identity, and deployment evidence remain immutable records of what actually ran.
- **Docker and Kubernetes are providers beneath Tavall orchestration.** They materialize desired state after CONTROL/placement resolution. Native-process and VM-backed providers may do the same. Provider-specific commands can remain for debugging or administration, but are not the normal application deployment contract.
- **Desired count and scaling policy are separate.** `service scale` changes desired service instance count. The existing `cluster scale-mode` concept, or its reconciled successor, controls policy such as `MANUAL` versus `AUTO`; it does not become a synonym for replica count.
- **Service/runtime definitions join the existing file-template architecture.** Defaults belong under the existing `/srv/dev-storage/templates/` registry described by the environment/materialization design rather than becoming Java-authored defaults or a second template system. The exact service/runtime template leaf should reuse the current registry conventions rather than being invented here.
## Deployment / Scale Resolution Flow
```plain text
tavall service deploy / tavall service scale
    -> resolve existing Tavall target
    -> lane / environment / node / service scope
    -> existing target type + capabilities + policy
    -> mutate desired service state
    -> CONTROL
    -> placement / Node Manager
    -> Docker / Kubernetes / native / VM provider
    -> generation + deployment evidence
```
Placement, machine classes, regions, Node Managers, private networking, and capacity remain owned by <mention-page url="https://app.notion.com/p/3d538458ddfd81ed9429e68cd1d9952c"/>. Persistent source/runtime materialization and evidence storage remain owned by <mention-page url="https://app.notion.com/p/3d838458ddfd817998becb19aaded57e"/>.
## Relationship to Existing Systems
<mention-page url="https://app.notion.com/p/3d838458ddfd8199aabccb87f2fc82ca"/> owns lane/environment lifecycle, mutability, executor authority, and template-backed defaults. This design only says deployment and scaling resolve those identities and normally mutate desired state rather than minting a new environment for every revision.
<mention-page url="https://app.notion.com/p/3d838458ddfd8169bb49e929826651cc"/> owns the client entry path. MCP remains a tiny authenticated bootstrap into Tavall Console; permission-aware Console execution should prefer the `tavall` CLI instead of exposing Docker, Kubernetes, deployment jobs, or provider operations as a giant MCP surface.
<mention-page url="https://app.notion.com/p/3d838458ddfd81b1b7d0ecfdcde18d3d"/> owns build, delivery evidence, readiness, rollback, and promotion. CD invokes this deployment path after candidate validation; it does not own a second Docker/Kubernetes deployment implementation.
<mention-page url="https://app.notion.com/p/3d838458ddfd81d29188edb39c470113"/> continues to own DEVELOPMENT → STAGING → PRODUCTION, Runtime PRs, Development Staging, Combined Runtime Staging, and production A/B semantics.
## Implementation Implications / Open Edges
- Add or reconcile `tavall service deploy` and `tavall service scale` around one target resolver and CONTROL desired-state contract instead of provider-specific public flows.
- Route Docker/Kubernetes reconciliation, native process execution, and VM-backed materialization through the same runtime-neutral workload lifecycle boundary.
- Persist desired instance count independently from scaling policy; preserve the existing scale-mode behavior through migration/aliasing if command spelling changes.
- Register service/runtime templates in the existing file-template registry and hot-load path. Do not add Java-authoritative defaults.
- Make environment generation/evidence advance on meaningful desired-state transitions without replacing mutable environment identity.
- **Open implementation detail:** choose the exact service/runtime template leaf and migration path inside the existing `/srv/dev-storage/templates/` registry after inspecting the current template loader. This is a registry-layout decision, not a new architecture layer.
## Logical Service / Runtime Refinement — 2026-09-13
This refinement corrects the service identity used by the deployment path above. `CloudServiceDefinition` represents one stable logical Tavall service. Ordinary redundancy, lifecycle variants, and BLUE/GREEN promotion are runtime-instance state owned by that logical service, not separately registered services and not ordinary `CloudServiceClusterDefinition` membership.
- **Runtime ownership:** one logical service may own multiple runtime instances. Runtime state carries instance/runtime ID, owning node, DEVELOPMENT/STAGING/PRODUCTION environment, deployment slot or generation, source revision, artifact digest, application health, lifecycle state, and router traffic state.
- **Stable endpoint:** the externally stable application endpoint inside this model is the selected node/server port. Every Tavall-managed deployment owns a small generic service-local router on that port; the router forwards only to healthy runtime/application instances belonging to that service. There is no mandatory central `tavall-cloud-router` service.
- **Promotion and rollback:** BLUE/GREEN are production runtime slots. Promotion changes service-router traffic state while service identity and configured port remain stable; rollback switches traffic back to the prior verified runtime. DEVELOPMENT and STAGING use the same topology even when only one runtime exists.
- **Network visibility:** add reusable networking classification `CloudNetworkVisibility` with `INTERNAL` and `PUBLIC`. It is independent of DEVELOPMENT/STAGING/PRODUCTION and changes node/network placement eligibility, not deployment topology or CLI command families. PUBLIC and INTERNAL use the same logical-service/runtime/router model.
- **Distribution visibility naming:** rename `CloudVisibilityScope` to `CloudDistributionVisibility` so distribution scope cannot be confused with network reachability. Preserve compatibility for persisted/serialized values where required.
- **Location cleanup:** remove `CELL`, `CloudLocationData.cell`, `CloudLocationDistance.SAME_CELL`, and placement/configuration behavior based on CELL. Keep concrete continent, country, region, zone, provider, provider region, datacenter, and failure-domain metadata. Provider remains placement metadata, not a distance tier.
- **Placement:** deployment resolution considers network visibility, requested lifecycle environment, node classification/network eligibility, node health/capacity, and existing placement/failure-domain constraints. PUBLIC does not get a separate deployment system.
- **Evidence:** deployment verification must reconcile requested source revision → built artifact digest → deployed runtime instance → node/environment/slot → runtime health → router traffic state, and fail when those facts disagree.
- **Routing boundary:** the service-local router is application/runtime routing only. `tavall-networking-edge-director` retains packet/network routing, tunnels, endpoint selection, regional/source decisions, and flow pinning; it is not merged into this router or made a central application load balancer.
- **ChatGPT migration:** migrate the current per-environment/per-slot registrations to one logical `tavall-cloud-chatgpt-plugin` service. Preserve the MCP `2026-07-28` protocol boundary, existing tool surface, and Console-first `tavall ...` operational model. Retire old registrations only after DEVELOPMENT, STAGING, redundant PRODUCTION, promotion, rollback, evidence, MCP, and Console validation succeed.
- **Cleanup boundary:** cleanup in this pass is limited to provably merged/completed/superseded environment/workspace debris. Active or unmerged work is preserved; no canonical-environment succession redesign is introduced.
The existing service deployment commands remain the public surface: `register`, `configure`, `plan`, `apply`, `verify`, `rollback`, and `releases`. Evolve their state model before adding command families; ordinary service operations remain Tavall CLI/Console operations rather than new MCP tools.
## Edge Director Placement Refinement — recovered 2026-09-19
**RECOVERED DESIGN; current staging still requires correction.** Edge Director placement is driven by accepted networking configuration plus host capability, not by CONTROL/AGENT identity and not by coarse NodeType.
An eligible Tavall Cloud node may launch Edge Director when networking and Edge Director are enabled in its accepted configuration and required host capabilities are present, including the current nftables/NFQUEUE/policy-routing/tunnel/IP capability set. CONTROL remains authoritative for desired-state mutation, endpoint commissioning/drain policy, reconciliation, and accepted configuration. CONTROL authority is not runtime placement.
The bootstrap boundary therefore must not require `CloudAgentMode.CONTROL`, must not gate on `NodeType.EDGE`, and should not depend directly on a concrete CONTROL coordinator server where a networking command/client abstraction is sufficient. Local accepted node/network metadata remains the safe boot source when CONTROL/PostgreSQL is temporarily unavailable; stale/unknown endpoint readiness must not be promoted to healthy merely to continue routing.
As of Tavall Cloud staging `a926302795eb9478756a218e0f1ff80f329d2e3f` (PR #287 on top of PR #286), the obsolete CONTROL-only Edge bootstrap restriction is **VERIFIED IN CODE as removed**. `EdgeDirectorBootstrap` accepts the typed networking boundary without requiring `CloudControlCoordinatorServer`, and the integration coverage exercises AGENT-mode startup plus local accepted metadata recovery. `EdgeDirectorNodeBootstrap` remains only as a deprecated compatibility subclass. Classify this as **VERIFIED IN CODE / VERIFIED IN TESTS**, not VERIFIED LIVE; no production networking mutation was performed.
The later NodeType classifier is orthogonal. Coarse NodeType may describe a node but does not authorize or prohibit Edge launch; service/runtime registration and networking config/capability remain authoritative.
## Tavall Web / Apache ingress refinement — 2026-09-18
Tavall Web uses the same logical-service/runtime-router model defined above, but public HTTP ingress has an additional outer layer:
```plain text
Internet
    -> Apache ingress / TLS / host + path routing
        -> Tavall Web stable logical-service endpoint/router
            -> healthy Tavall Web runtime
                -> owning service stable endpoint/router
                    -> healthy owning service runtime
```
- Apache is the outer HTTP/TLS ingress; Tavall Web is the shared Tavall application host. They are separate failure boundaries.
- Public MCP identity is path-based: `https://mcp.tavall.org/mcp/<specific-mcp>`. Backend service/runtime ports are hidden deployment details.
- The bare `https://mcp.tavall.org/` host redirects to `https://workflows.tavall.org/`.
- Apache normally routes Tavall Web-owned/application-hosted paths to the Tavall Web stable logical-service endpoint. It must not target one BLUE/GREEN runtime slot directly.
- Selected API/MCP routes may have an explicitly designed Apache continuity/direct proxy to the owning service's stable logical-service endpoint so the endpoint can remain available when the Tavall Web Spring application is offline. This forwards to existing authority; Apache never implements product/MCP semantics.
- Tavall Web may therefore host substantial shared Web/API/MCP/Discord HTTP surfaces while domain authority remains in the owning service and backend services retain independent deployment/redundancy.
- Private MCP services stay on private/Nebula or approved local endpoints and receive no automatic public route.
The Tavall Web canonical routing/module contract lives in [TAVALL_WEB_HOST_AND_MCP_ROUTING.md](https://github.com/TavallStudios/tavall-web/blob/main/docs/architecture/TAVALL_WEB_HOST_AND_MCP_ROUTING.md).
<page url="https://app.notion.com/p/3df38458ddfd81538e98dd5a14341683">Minecraft Edge Director Live Origin-Hiding State — 2026-09-18</page>
## Execution update 2026-09-19 — current Cloud lineage
- **VERIFIED IN CODE / VERIFIED IN TESTS:** the Edge Director CONTROL-only restriction remains removed in the current Cloud lineage; typed networking bootstrap and AGENT-mode coverage are preserved in the PR #288 continuation.
- **NOT VERIFIED LIVE:** no production networking mutation was performed. The live development agent is READY, but Edge placement acceptance remains a source/test result rather than production-network proof.
## Execution update 2026-09-26 — current CD template and bootstrap boundary
- The current loader uses `/srv/dev-storage/templates/services/<service-id>/.tavallcd/cd.yaml`. The existing deployable `tavall-cloud-chatgpt-plugin` template is hot-loaded with AUTO CD.
- Its current service deployment still points to artifact `ba4549655ea561430dcb75e20900e62a20a9a356818e41f713bd0d980c4ab986` from `tavall-cloud@d4fad9dbcee62d3210c14262d65cdea2e6f529ac`; CI run/evidence IDs are empty. This is not a rollout delivery bundle.
- A provider-neutral `tavall-cloud-control/.tavallcd/cd.yaml` file is present in the service template registry. It binds runtime `control-plane-agent` to artifact `tavall-cloud-agent`, requires the six Cloud CI checks, targets DEVELOPMENT/STAGING/PRODUCTION, and uses `SINGLE` production traffic for this CONTROL_PLANE runtime. Its TCI template identity is `services/tavall-cloud-control`, digest `5033fa2b198c3f6c47065eb3e2db202d9203048a350fcda9a240c195b570c9fa`; the TCI `ServiceRuntimeTemplateLoader` parsed it successfully.
- Cloud PR #395 commit `a6a34717` aligns Cloud's metadata store to TCI's `services/<service-id>` template identity; current head `0df90c24` removes GitHub URLs, Gradle module names, and mutable output paths as deployment requirements. Immutable deployment lineage now requires the canonical source repository, template-selected artifact, CI run/evidence, delivery bundle, and template digest. Local `:tavall-cloud:test` and `:tavall-cloud-node:test` pass at `0df90c24`; the live Agent/Environment path remains unverified.
- The installed Agent is older and its `service cd inspect` response does not expose template identity/runtime fields, so Cloud hot-load of the control template is not yet verified.
- `tavall-cloud-control` remains a CONTROL_PLANE service with CD `MANUAL`/disabled and no deployment identity. Its installed systemd unit starts a fixed `/opt/tavall-cloud/tavall-cloud-agent.jar`; Cloud `.tavallci` declares the existing self-contained `allJar` artifact and its plan validates, but the artifact has not been built/published and no safe immutable-artifact bootstrap is configured. No restart or deployment was attempted.
- The current Cloud service registry also contains `novus-ffa-east-backend` (`MINECRAFT_GAME_SERVER`), `tavall-cloud-redis` (`REDIS`), and `tavall-cloud-storage-prepare` (`SHARED_FILE_SYSTEM`, `EXTERNAL_SYSTEMD`). Redis and storage-preparation remain infrastructure services; Storage reports CD unsupported. The Novus backend has no deployment-strategy label, observed state `UNKNOWN`, and `tavall service cd status` returns `INVALID_REQUEST`; its deployment owner/runtime template is unresolved, so no `.tavallcd` was guessed.
- No rollout artifact, frozen delivery bundle, new DEVELOPMENT deployment, or STAGING readiness evidence exists. Production remains unchanged.
## CD adapter and production runtime slots — 2026-09-26
- TCI PR #14 head `ad695b3` now freezes the selected artifact's exact source, name/version, digest, channel, and immutable storage reference; focused TCI CD unit tests pass locally. Its reusable Cloud module still has no `DeploymentProvider` adapter for the existing `tavall service deploy plan/apply/verify/rollback` path.
- Cloud PR #395 validates artifact, source, CI, bundle, and template lineage in the service deploy provider. The installed CLI predates the matching request fields, and the DEVELOPMENT Environment still rejects exact-source execution because its mounted TCI checkout is stale.
- Cloud already contains Redis-backed runtime records, BLUE/GREEN slot types, a stable logical-service router, and a health-monitoring orchestrator. The immutable deployment provider still activates one shared `current` release and restarts one service unit; the authority handler derives slot/traffic/environment from static service labels. The plugin remains `runtime.slot=SINGLE` while its template requests `A_B`, so deployment does not yet use the existing router/slot foundation. No production traffic changed.
- Cloud PR #395 head `0df90c24` passes local `:tavall-cloud:test` (312 tests, 2 skipped) and `:tavall-cloud-node:test` (249 tests). These repository tests are not Cloud Executor deployment evidence.
- The requested CI-to-CD-to-Cloud deployment path remains blocked before DEVELOPMENT deployment and STAGING readiness. Production remains unchanged.
</content>
</page>
