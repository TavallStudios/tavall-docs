<page url="https://app.notion.com/p/3d838458ddfd817998becb19aaded57e" icon="💾">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3d538458ddfd81499004db3381c81444" title="Platform & Infrastructure"/>
<ancestor-2-page url="https://app.notion.com/p/3d538458ddfd81b9984cd65f01c92e27" title="Tavall"/>
</ancestor-path>
<properties>
{"title":"Tavall Cloud — Storage Topology & Environment Materialization"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"💾"}</iconMetadata>
<content>
<callout icon="💾" color="blue_bg">
	**Status:** active infrastructure design + recovery work. Reconciled from recent Cloud storage/MCP work and the shared infrastructure topology.
</callout>
## Purpose
Provide durable shared and development storage without making filesystem paths the product model.
## Design
- Storage is a Tavall Cloud service consumed by environments, repository materializers, CI/CD, runtimes, and artifacts.
- DEVELOPMENT source/work materialization is environment-first: resolve lane/environment, then create or attach the required repository generation on authorized storage/executor capacity.
- Shared storage can hold templates, cached dependencies, artifacts, and cross-node development data where safe.
- Exact-source working trees and mutable build state remain bounded to the environment/execution generation that owns them.
- Network storage must be observable and recoverable when NFS/provider mounts fail. A successful environment record with a missing mount is not a successful runtime.
- Artifacts are immutable by identity/digest once they participate in CI/CD promotion.
## Physical Topology
The broader node/storage capacity model is maintained in <mention-page url="https://app.notion.com/p/3d538458ddfd81ed9429e68cd1d9952c"/>. That page owns provider-neutral DATA/STO/WRK/GAME capacity planning; this record owns the Cloud-facing materialization and authority boundary.
## Current Work
PR #255/#254 recovered co-hosted DEVELOPMENT storage and MCP behavior, NFS mount/provider handling, and source identity. The remaining direction is to eliminate legacy paths that treat a standalone workspace ID or host path as the durable authority.
## Sources
- [Tavall Cloud PR #255](https://github.com/TavallStudios/tavall-cloud/pull/255)
- [Tavall Cloud PR #254](https://github.com/TavallStudios/tavall-cloud/pull/254)
## Documentation Links
### Design Source(s)
- [DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/architecture/DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md)
- [ENVIRONMENT_SHARED_WORKSPACE.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/developer/ENVIRONMENT_SHARED_WORKSPACE.md)
- [REPOSITORY_CACHE_SYNC_IMPLEMENTATION.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/developer/REPOSITORY_CACHE_SYNC_IMPLEMENTATION.md)
### Final / Canonical Documentation
- **Not finalized yet.** Current storage/control candidate is `DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md` under the Cloud-level Final Draft.
### Progression / Evidence Documentation
- [TAVALL_CLOUD_PROGRESSION.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/progression/TAVALL_CLOUD_PROGRESSION.md)
- Exact-source storage/MCP recovery evidence in Cloud PRs #254/#255.
### Implementation
- `TavallStudios/tavall-cloud` storage providers, environment workspace/materialization, repository cache/sync and artifact paths.
---
## DOC TODO:
### Document next steps
- [ ] Reconcile environment-first ownership with any remaining leased-worktree/workspace-first implementation documents and mark superseded paths.
- [ ] Identify/link the final storage owner after the Cloud Final Draft is promoted.
- [ ] Keep physical-capacity topology separate from Cloud materialization authority while linking both records.
### System next steps
- [ ] Prove NFS/provider mount failure and recovery are observable and reconcile correctly.
- [ ] Eliminate durable authority based on host paths or standalone workspace IDs.
- [ ] Preserve immutable artifact identity/digests through cross-node CI/CD delivery.
## Execution update 2026-09-20 — materialization versus live state
- Tavall Storage and the configured filesystem remain authoritative for environment configuration, source/work materialization, manifests, artifacts, logs, and evidence bytes.
- Redis is the live Cloud Job/environment coordination authority for current generations, leases, CAS fences, executor/runtime presence, and desired/observed operational state.
- PostgreSQL Job/environment rows are audit/history observations for this boundary and cannot veto an ordinary valid Redis-backed execution.
- Live evidence: exact Tavall CI source `00ac2dad0c5c3854357d9cf6252c7962885d1159` completed Job `37a06859-22fd-4d49-a9d5-b14a012213f3` with Storage evidence available; the evidence remained readable after agent restart.
## Authority correction 2026-09-20 — Storage is the durable Cloud materialization boundary
PostgreSQL is not used by Tavall Cloud. Redis owns live operational coordination; Tavall Storage/filesystem owns durable configuration, exact source/work materialization, manifests, logs, artifacts, and evidence. There is no PostgreSQL audit/history exception in the current runtime. The Redis-only staging/runtime proof at `c7d5db81332f330c5d9987e9c16921a6090ca1ca` produced Storage-backed Job evidence and preserved it across Agent restart.
## Final integrated validation 2026-09-20
The final integrated Cloud head is `15434688b6f61753df30471806f65060e1f46e89`; full Cloud validation passed. The successful Job's stdout/stderr and evidence remained Storage-backed and available after Agent restart; no PostgreSQL writer or reader exists in the active Cloud source graph.
## Authority correction 2026-09-20 — storage boundary
Tavall Storage/filesystem is the durable authority for configuration, source/work materialization, manifests, artifacts, logs, and evidence. Redis is the live Cloud authority for mutable coordination, generations, leases/CAS, Jobs, and runtime projections.
PostgreSQL is absent from Tavall Cloud: it is not a storage-topology authority, writer-fence source, audit/history sink, migration dependency, or execution fallback. Older PostgreSQL storage wording remains historical provenance only and must not be used to design or deploy current Cloud storage.
## Execution update 2026-09-20 — final evidence materialization
At integrated Cloud staging/runtime head 2858ae2a576d77a4a2fee162a776d5d7425d4752, the exact-source Cloud Job 37495124-5d00-4989-a6e1-c9e694460e06 completed successfully and exposed its logs/evidence through tavall-storage://dev-storage/jobs/37495124-5d00-4989-a6e1-c9e694460e06. Agent restart preserved the final Job state and evidence handle. PostgreSQL was not used by the runtime or evidence path.
</content>
</page>