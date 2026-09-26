<page url="https://app.notion.com/p/3d838458ddfd81d29188edb39c470113" icon="🧭">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3d538458ddfd81499004db3381c81444" title="Platform & Infrastructure"/>
<ancestor-2-page url="https://app.notion.com/p/3d538458ddfd81b9984cd65f01c92e27" title="Tavall"/>
</ancestor-path>
<properties>
{"title":"Tavall Runtime Promotion & Environment Workflow"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"🧭"}</iconMetadata>
<content>
<callout icon="🧭" color="blue_bg">
	**Design status:** Draft canonical workflow definition. This document captures the agreed release/runtime model before implementation. No Tavall repositories or `GIT_WORKFLOW.md` changes are part of this step.
</callout>
## Purpose
Define a single Tavall workflow for durable DEVELOPMENT, STAGING, and PRODUCTION environments, runtime-specific PRs, combined application staging, multi-runtime projects, and production promotion.
The first concrete consumer is Tavall-owned MCP infrastructure, but the model is intended to become the common release pattern for Tavall services that use the environment/lane system.
## Core Environment Model
Tavall environments and lanes are **durable by default** and explicitly classified as one of:
- `DEVELOPMENT`
- `STAGING`
- `PRODUCTION`
Environment classification describes the runtime purpose and promotion level. It is not simply inferred from whether a branch happens to be temporary.
For MCP services, the initial runtime topology is:
<table fit-page-width="true" header-row="true">
<tr>
<td>Stage</td>
<td>Default topology</td>
<td>Role</td>
</tr>
<tr>
<td>PRODUCTION</td>
<td>A/B runtime slots</td>
<td>Current production plus safe candidate / last-known-good runtime for promotion and rollback</td>
</tr>
<tr>
<td>STAGING</td>
<td>Production-equivalent copies</td>
<td>Validate the fully deployed application and production release behavior before main</td>
</tr>
<tr>
<td>DEVELOPMENT</td>
<td>Durable integration environments plus isolated development lanes as needed</td>
<td>Feature work, runtime-specific work, experimentation, isolated testing, and Development Staging</td>
</tr>
</table>
### Production A/B
MCP production uses A/B deployment slots. A new production build is deployed to the inactive slot, validated, and only then promoted to active traffic. The previous known-good slot remains available for rollback until the next successful production iteration replaces it.
Production redundancy here primarily protects against application/process/release failures. Multiple slots on one physical node do not by themselves provide node-level hardware redundancy.
## PR Hierarchy
The workflow separates **change type** from **runtime/promotion role**. Existing PR/change types such as Feature remain useful and should not be replaced by runtime terminology.
### Runtime PR
A **Runtime PR** represents work for one runtime in a project.
- It belongs to that runtime's implementation lifecycle.
- It does **not** become the application's combined STAGING deployment merely because it is open or testable.
- It may be deployed and tested in isolation in a DEVELOPMENT environment/lane.
- In a multi-runtime project, several Runtime PRs may exist concurrently for different runtimes.
Examples of runtimes can include application backend, proxy, game server, web runtime, bot/runtime adapter, worker, or another independently deployed execution surface defined by the project.
### Combined Runtime Staging PR
A **Combined Runtime Staging PR** represents the actual fully deployed application candidate.
It combines the required runtime iterations and deploys them together using the existing runtime-selection/runtime-flag mechanisms already designed for Tavall systems.
Its job is to answer a different question than a Runtime PR:
> Does the complete application, with the intended combination of runtimes and runtime flags, function as the candidate we are prepared to promote?
Combined Runtime Staging is therefore the primary pre-production integration boundary.
### Development Staging
The previous workflow term **Sub-Staging** should be renamed to **Development Staging**.
Development Staging is staging performed on `DEVELOPMENT` environments/lanes. It may apply to any relevant PR/runtime combination and exists below formal STAGING.
Development Staging can include:
- isolated Runtime PR staging
- combined runtime staging before formal STAGING
- feature/integration candidates
- temporary or durable development deployment arrangements
- validation of runtime flags and runtime combinations
Development Staging is not a fourth environment classification. It is a **workflow role performed on DEVELOPMENT infrastructure**.
This distinction keeps the environment model simple:
```plain text
DEVELOPMENT -> STAGING -> PRODUCTION
```
while still allowing multiple levels of integration before a change reaches formal STAGING.
## Multi-Runtime Projects
`GIT_WORKFLOW.md` must continue to support projects with multiple independently developed runtimes.
The intended structure is:
```plain text
Feature / Fix / other change type
        |
        +--> Runtime PR: Runtime A
        |       +--> isolated DEVELOPMENT testing
        |
        +--> Runtime PR: Runtime B
        |       +--> isolated DEVELOPMENT testing
        |
        +--> Runtime PR: Runtime C
                +--> isolated DEVELOPMENT testing

required runtime iterations
        |
        v
Development Staging
        |
        v
Combined Runtime Staging PR
        |
        v
STAGING deployment
        |
        v
production promotion / main
```
A Runtime PR should therefore be able to advance independently without pretending that its isolated deployment is the complete application staging candidate.
## Branch and PR Semantics
The next `GIT_WORKFLOW.md` revision should update **branch type definitions** to reflect runtime and promotion roles while preserving the current change taxonomy.
The workflow needs to distinguish at least these concepts:
<table fit-page-width="true" header-row="true">
<tr>
<td>Concept</td>
<td>Meaning</td>
</tr>
<tr>
<td>Feature / Fix / existing PR types</td>
<td>What kind of change is being made</td>
</tr>
<tr>
<td>Runtime PR</td>
<td>Which independently deployed runtime is being iterated</td>
</tr>
<tr>
<td>Development Staging</td>
<td>Pre-STAGING integration/testing role on DEVELOPMENT infrastructure</td>
</tr>
<tr>
<td>Combined Runtime Staging PR</td>
<td>Full deployed application candidate composed from required runtimes</td>
</tr>
<tr>
<td>STAGING</td>
<td>Production-equivalent release validation</td>
</tr>
<tr>
<td>main / PRODUCTION</td>
<td>Accepted production state</td>
</tr>
</table>
Branch naming/type definitions should encode the workflow clearly enough that automation can determine the branch's role without erasing the underlying Feature/Fix/etc. change type.
## Commit Types
**Existing commit types remain intact.**
The runtime/environment workflow should not invent replacement commit semantics merely because PR and branch roles are becoming more explicit. Commit types continue to describe the change itself. Runtime, staging, and environment metadata belong at the branch, PR, deployment, and environment layers.
## Main as Production
`main` is the accepted production state.
It is useful to think of `main` as the final production promotion boundary, but it is **not literally another PR type**. The workflow documentation should make that distinction explicit.
The intended end state is:
```plain text
Runtime PR(s)
    -> Development Staging
    -> Combined Runtime Staging PR
    -> STAGING deployment/acceptance
    -> merge/promotion to main
    -> PRODUCTION A/B deployment
```
The existing Tavall documentation around qualification and merge-to-main should be completed so that promotion to `main` has a defined acceptance contract rather than functioning as an informal final merge.
## Runtime Flags
Combined Runtime Staging must use the project's established runtime flags/runtime-selection mechanisms rather than inventing an unrelated deployment mechanism.
This is especially important for multi-runtime systems such as Tavall Cloud and Tavall MC, where the deployed application may intentionally select or combine runtime implementations during development, staging, and migration.
The workflow documentation should define the contract around these flags, while runtime-specific implementation details remain owned by the relevant project.
## MCP as the First Dogfood Consumer
Tavall MCP infrastructure is the first internal service family to fully exercise this workflow.
The intended MCP progression is:
```plain text
DEVELOPMENT
    durable dev environment
    + isolated lanes
    + Development Staging

STAGING
    production-equivalent topology
    + combined candidate validation

PRODUCTION
    A/B slots
    + candidate validation
    + traffic switch
    + last-known-good rollback
```
Using internal MCP tooling as the first real consumer gives Tavall a production release path with an actual user before imposing the model on external consumers.
## Recovery and Supervision
Automated recovery is deliberately **not part of this immediate documentation step**.
A future Recovery Agent can monitor release health, runtime promotion, failed candidates, rollback conditions, and environment drift after the agent platform is in a sufficiently stable state.
The underlying service supervisor/recovery path should still remain capable of operating below the MCP it supervises so a broken MCP does not need to repair itself.
## Required Documentation Changes Later
When implementation begins, update `tavall-docs/GIT_WORKFLOW.md` with the following scoped changes:
- [ ] Rename **Sub-Staging** to **Development Staging** throughout the workflow.
- [ ] Define Development Staging as a workflow role using DEVELOPMENT environments/lanes, not a fourth environment class.
- [ ] Preserve existing commit types.
- [ ] Preserve existing change/PR types such as Feature.
- [ ] Define Runtime PR semantics for single-runtime and multi-runtime projects.
- [ ] Define Combined Runtime Staging PR semantics as the full deployed application candidate.
- [ ] Update branch type definitions so runtime and promotion roles are explicit alongside existing change types.
- [ ] Document durable-by-default DEVELOPMENT, STAGING, and PRODUCTION environment/lane classification.
- [ ] Finish the previously designed qualification/merge-to-main definition.
- [ ] Define `main` as the accepted production source state without pretending it is itself a PR.
- [ ] Document exact-source/runtime promotion expectations and runtime-flag usage.
- [ ] Push the completed documentation change through the Tavall Docs workflow and ultimately to `main`.
## Open Implementation Decisions
The workflow is conceptually defined, but these details should be resolved against current repository documentation and implementations when work begins:
- Exact branch naming syntax for Runtime PRs, Development Staging, and Combined Runtime Staging.
- Whether runtime identity is encoded only in branch/PR metadata or also enforced as structured Tavall Cloud metadata.
- Exact acceptance gates required before a Combined Runtime Staging PR can promote to formal STAGING.
- Exact qualification gates for merge/promotion to `main`.
- How A/B slot identity and last-known-good generations are represented in Tavall Cloud environment metadata.
- Which runtime flags are universal Tavall concepts versus project-specific implementation details.
<callout icon="⛔" color="yellow_bg">
	**Scope guard:** This document records the workflow only. Repository edits, Tavall Cloud implementation, deployment changes, and `GIT_WORKFLOW.md` modification should begin in a separate execution step after this design is reviewed.
</callout>
## Documentation Links
### Design Source(s)
- This working Notion record is the current cross-repository design source for Runtime PR / Development Staging / Combined Runtime Staging / production A/B semantics.
- [DEVELOPER_RUNTIME_STAGING.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/developer/DEVELOPER_RUNTIME_STAGING.md)
- [GIT_WORKFLOW.md](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/GIT_WORKFLOW.md)
### Final / Canonical Documentation
- **Not finalized yet.** The accepted repository contract must ultimately live in `tavall-docs` `GIT_WORKFLOW.md` plus owning runtime/deployment Final documents after the terminology and acceptance gates are implemented/reviewed.
### Progression / Evidence Documentation
- [TAVALL_CLOUD_PROGRESSION.md](https://github.com/TavallStudios/tavall-cloud/blob/main/docs/progression/TAVALL_CLOUD_PROGRESSION.md)
- Product/runtime-specific staging/progression evidence in consuming repositories.
### Implementation
- `TavallStudios/tavall-cloud` environment/staging/promotion implementation and `TavallStudios/tavall-docs` workflow policy.
- Documentation-policy reconciliation is tracked by [tavall-docs PR #10](https://github.com/TavallStudios/tavall-docs/pull/10); runtime-workflow changes remain a separate implementation boundary.
---
## DOC TODO:
### Document next steps
- [ ] Move the existing “Required Documentation Changes Later” checklist into the actual `GIT_WORKFLOW.md` change when that work begins, then remove completed/stale items here.
- [ ] Link the resulting GitHub Final/workflow authority and mark this page's working-design role explicitly after human acceptance.
- [ ] Reconcile any older `Sub-Staging` language across Cloud/product docs and archive or supersede conflicts.
### System next steps
- [ ] Implement and validate structured Runtime PR / Development Staging / Combined Runtime Staging semantics.
- [ ] Define exact formal-STAGING and merge-to-main gates.
- [ ] Implement/validate production A/B slot identity, candidate validation, traffic switch and last-known-good rollback.
## Authority correction 2026-09-20
The current Tavall Cloud runtime does not use PostgreSQL. Redis owns live lanes, environments, generations, leases, Jobs, runtime presence, desired/observed projections, and CAS; Tavall Storage/filesystem owns durable materialization and evidence. PostgreSQL migrations/classes are historical provenance only and are not current runtime authority or fallback.
## Authority correction 2026-09-20 — runtime promotion
Runtime promotion and DEVELOPMENT/STAGING/PRODUCTION execution use the same Redis-backed Cloud state authority and Tavall Storage/filesystem materialization/evidence boundary. PostgreSQL is not present in the Cloud runtime or build and does not own current deployment, environment, generation, or recovery state.
Any older relational/PostgreSQL runtime wording is superseded historical provenance. Redis loss fails closed or follows the explicit Redis recovery path; promotion never reconstructs or falls back to PostgreSQL state.
## Execution update 2026-09-20 — integrated Redis-only runtime
The accepted integrated staging/runtime head is 2858ae2a576d77a4a2fee162a776d5d7425d4752. Agent deployment from this exact source is READY; live Console and exact-source Cloud Job execution succeeded through Redis-backed coordination and Tavall Storage evidence. PostgreSQL is absent from the Cloud runtime/build and is not a recovery or promotion dependency.
## Promotion update 2026-09-20
Validated Redis-only Cloud staging/runtime 2858ae2a576d77a4a2fee162a776d5d7425d4752 is now promoted to main at 225f952e70f70c12fb2a18c3da17a24da283c683. Production deployment is intentionally separate from this source promotion.
## Execution update 2026-09-26 — no promotable candidate yet
- The existing DEVELOPMENT CI Environment `5848c5ff-a2a2-4da4-bd25-9cff8e558433` now binds exact source snapshot `29ce13c6e19db68a295f4106e728044f7febda8375a47aff85ae1f64121ef694`, preserving its DURABLE / DEDICATED / SHARED / inherited policies, but remains `BLOCKED` with workspace and development-tool components `UNKNOWN`.
- No exact-source Tavall CI job, immutable artifact, frozen delivery bundle, deployment-generation readiness record, or STAGING candidate exists for this rollout. Therefore no DEVELOPMENT-to-STAGING or production A/B promotion was performed.
- The currently running ChatGPT plugin service has AUTO CD but its existing deployment has empty CI run/evidence identifiers; it is not a candidate for this promotion chain. Production slots and traffic were not changed.
</content>
</page>
