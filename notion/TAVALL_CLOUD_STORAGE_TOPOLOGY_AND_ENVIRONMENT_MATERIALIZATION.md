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
<callout icon="📎" color="gray_bg">
	**Document Type:** Technical / Design Final Draft surface · **Canonical GitHub twin:** `TavallStudios/tavall-cloud/docs/architecture/DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md` · **Owning system design:** <mention-page url="https://app.notion.com/p/3e838458ddfd81c9950bf35de8a86c7e"/>. This page remains the human-readable CONTROL/STORAGE and materialization twin rather than an independent storage architecture fork.
</callout>
<callout icon="💾" color="blue_bg">
	**Status:** active infrastructure design + recovery work. Reconciled from recent Cloud storage/MCP work and the shared infrastructure topology.
</callout>
## Purpose
Provide durable shared and development storage without making filesystem paths the product model.
## Design
- Storage is a Tavall Cloud service consumed by service Environments, exact-source Executor workspaces, CI/CD, runtimes, and immutable artifacts.
- Cloud Environments represent deployed logical-service runtime targets only. They carry service configuration, desired/observed state, deployment generations, and runtime evidence; they do not own repository source trees, build jobs, or CI workspaces.
- DEVELOPMENT source/work materialization is Lane + exact-source first: resolve the repository and commit, then create the operation-scoped Workspace on an authorized shared Executor. A source checkout, branch, CI job, or Executor invocation does not create an Environment.
- The current Cloud Environment source-materialization adapter is a migration blocker, not canonical storage or execution authority. Tavall CI must move source work to the Envless shared-Executor job path while durable operation/evidence records stay in their existing Storage authority. Service Environment storage does not create repository `workspaces/` subtrees or full-UUID aliases; operation Workspaces remain under Executor invocation authority.
- Shared storage can hold templates, cached dependencies, artifacts, and cross-node development data where safe.
- Exact-source working trees and mutable build state remain bounded to the Lane + Executor invocation Workspace that owns them. They are independent of service Environment generations.
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
- `TavallStudios/tavall-cloud` storage providers, service Environment materialization, operation-scoped Executor Workspaces, repository cache/sync, and artifact paths.
---
## DOC TODO:
### Document next steps
- [x] Reconcile source materialization as Lane + exact source + Executor Workspace; service Environments do not own repository/CI work. Remaining runtime code migration is tracked separately.
- [ ] Identify/link the final storage owner after the Cloud Final Draft is promoted.
- [ ] Keep physical-capacity topology separate from Cloud materialization authority while linking both records.
### System next steps
- [ ] Prove NFS/provider mount failure and recovery are observable and reconcile correctly.
- [ ] Eliminate durable authority based on host paths or standalone workspace IDs.
- [ ] Preserve immutable artifact identity/digests through cross-node CI/CD delivery.
## Execution update 2026-09-20 — materialization versus live state
- Tavall Storage and the configured filesystem remain authoritative for service Environment configuration, exact-source Workspace materialization, manifests, artifacts, logs, and evidence bytes.
- Redis is the live Cloud Job and service Environment coordination authority for job/invocation fences, service runtime generations, Executor/runtime presence, and desired/observed operational state.
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
<details>
<summary>Documentation Update State</summary>
	\<table header-row="true"\>\<tr\>\<td\>Surface\</td\>\<td\>Sync State\</td\>\<td\>Location\</td\>\<td\>Last Updated\</td\>\<td\>Evidence\</td\>\</tr\>\<tr\>\<td\>GitHub\</td\>\<td\>`1:1`\</td\>\<td\>`docs/architecture/DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md`\</td\>\<td\>2026-10-02 11:56 PM PDT\</td\>\<td\>Draft Cloud PR #424, branch `working/chatgpt-web-executor-catalog-20260930`.\</td\>\</tr\>\<tr\>\<td\>Notion\</td\>\<td\>`1:1`\</td\>\<td\>Current page\</td\>\<td\>2026-10-02 11:56 PM PDT\</td\>\<td\>Updated to match the current Cloud contract.\</td\>\</tr\>\</table\>
	</table>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	### Update History
	\<table header-row="true"\>\<tr\>\<td\>Timestamp\</td\>\<td\>Surface\</td\>\<td\>Event\</td\>\<td\>Location\</td\>\<td\>Previous Location\</td\>\<td\>Evidence\</td\>\<td\>Notes\</td\>\</tr\>\<tr\>\<td\>2026-09-26 8:42 PM PDT\</td\>\<td\>Notion\</td\>\<td\>`SYNCED`\</td\>\<td\>Current page\</td\>\<td\>Standalone storage/materialization topic page\</td\>\<td\>Cloud module consolidation\</td\>\<td\>Bound to `DEVELOPER_CONTROL_AND_STORAGE_FINAL_DRAFT.md` as one logical document.\</td\>\</tr\>\<tr\>\<td\>2026-10-02 11:56 PM PDT\</td\>\<td\>GitHub + Notion\</td\>\<td\>`UPDATED`\</td\>\<td\>1:1 CONTROL/STORAGE pair\</td\>\<td\>2026-09-26 synchronized content\</td\>\<td\>Draft Cloud PR #424, branch `working/chatgpt-web-executor-catalog-20260930`; this Notion page\</td\>\<td\>Recorded service-only Environment storage; Environment-bound source materialization remains a migration blocker.\</td\>\</tr\>\</table\>
	</table>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
	\</table\>
</details>
</content>
</page>
