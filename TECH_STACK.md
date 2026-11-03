# Tavall Technology Stack

> Document class: cross-project technology inventory and selection policy
> Reviewed: 2026-11-03
> Owner: Tavall Docs
> Status: reconciled documentation; not a deployment or test receipt

## Scope and precedence

This file describes the default technology choices for new Tavall capabilities and links to domain-owned inventories. It is not a second owner of implementation contracts. The governing [Code Architecture](docs/quality/CODE_ARCHITECTURE.md), [state and persistence chapter](docs/quality/code-architecture/REGISTRIES_CACHES_AND_REPOSITORIES.md), [module boundaries](docs/quality/code-architecture/MODULE_SEPARATION.md), and each tool's own API and tests take precedence for mechanics. Domain owners record justified exceptions. Do not rewrite production code merely to match an inventory.

The baseline is **Java 25 + repository-owned Gradle wrappers**, Tavall DI, Database, Cache, Registry, Concurrency, Scheduler, EventBus and associated Java Tools when relevant. Tavall CI owns build planning, exact-source evidence and promotion policy; Tavall Cloud owns execution, service state and deployment placement. Neither replaces the other.

## State selection, not a one-database rule

| Question | Default owner / technology | Authority and failure |
| --- | --- | --- |
| Queryable, transactional, durable application truth | Tavall Database with PostgreSQL and mapped entities | PostgreSQL commit is authority |
| Evolving structured attributes | PostgreSQL JSONB alongside typed relational columns | Same PostgreSQL transaction |
| Disposable fast views, TTL, negative caching | Tavall Cache, usually JVM memory first | Rebuild from authoritative state |
| Registered in-process identities, active runtime definitions | Tavall Registry | Owning runtime/generation |
| Cross-process leases, fences, sessions, coordination or live projections | Redis through Tavall Database Redis API when needed | Explicit key-family owner, recovery and loss behavior |
| Owner-local durable records, content-addressed blobs, artifacts | Tavall Filesystem over configured Tavall NFS/storage | Atomic writes, checksums, ownership and retention |
| In-flight work / futures / cancellation | Typed operation/runtime owner | Completion, cancellation or explicit durable recovery |
| Semantic recall and graph/temporal context | Provider-specific Qdrant/Graphiti/Graphify integrations only where the domain requires them | Not a substitute for exact canonical authority |

Stable identifiers, relationships and frequently filtered dimensions normally remain typed PostgreSQL columns; use JSONB for extensible metadata and payloads, not to hide all data modeling in one blob. PostgreSQL is **the default for queryable durable application domains**, not a requirement for every Cloud/Executor or filesystem owner.

The default cross-storage mutation order is validation -> authoritative durable commit -> cache/Redis/registry/file-mirror projection -> typed event/result. For each key family or mirror document ownership, TTL or retention, invalidation, idempotency, stale handling, retries and reconciliation. Redis acceptance does not imply PostgreSQL commit success.

### Accepted exceptions and boundaries

- **Tavall Cloud:** Redis owns fenced live operational generations, jobs, queues, leases and presence. **Tavall NFS**, via Tavall Filesystem/Storage, owns durable manifests, materialized configuration, source/work, artifacts, evidence and logs. Cloud PostgreSQL proposals were superseded; do not reintroduce Postgres as Cloud Job authority. NFS is physical storage, never a logical service or Environment identity.
- **Tavall Workflows:** current system stores catalog/runtime-owned state and immutable release packages through Tavall Filesystem on NFS. This remains accepted until concrete transactional/query needs justify a migration.
- **Tavall Analytics:** PostgreSQL owns queryable evidence/observation/metric metadata; content-addressed immutable evidence bytes live on mounted NFS.
- **Tavall Content:** PostgreSQL owns domain and durable job state. Google Drive is the documented long-term media store; workers may materialize temporary media. A production Drive importer is not yet confirmed.
- **Tavall AI memory:** canonical exact state and outbox are specified for PostgreSQL, with hot state/revisions, semantic retrieval and temporal providers as separate optional adapters. Source contracts do not establish all provider adapters as deployed.
- **Project Novus:** Paper/Velocity runtime state is not automatically database or cache state; PostgreSQL/JSONB, Tavall Cache/Registry and selective Redis projections have distinct roles.

## Domain inventories

| File | Owner |
| --- | --- |
| [JAVA_TECH_STACK.md](https://github.com/TavallStudios/tavall-java-tools/blob/main/JAVA_TECH_STACK.md) | Tavall Java Tools |
| [DATA_TECH_STACK.md](https://github.com/TavallStudios/tavall-database/blob/main/DATA_TECH_STACK.md) | Tavall Database |
| [WEB_TECH_STACK.md](https://github.com/TavallStudios/tavall-web/blob/main/WEB_TECH_STACK.md) | Tavall Web |
| [ACCOUNT_TECH_STACK.md](https://github.com/TavallStudios/tavall-web-account/blob/main/ACCOUNT_TECH_STACK.md) | Tavall Account presentation |
| [AI_TECH_STACK.md](https://github.com/TavallStudios/tavall-ai/blob/main/AI_TECH_STACK.md) | Tavall AI |
| [CLOUD_TECH_STACK.md](https://github.com/TavallStudios/tavall-cloud/blob/main/CLOUD_TECH_STACK.md) | Tavall Cloud |
| [CONTENT_TECH_STACK.md](https://github.com/TavallStudios/tavall-content/blob/main/CONTENT_TECH_STACK.md) | Tavall Content |
| [ANALYTICS_TECH_STACK.md](https://github.com/TavallStudios/tavall-analytics/blob/main/ANALYTICS_TECH_STACK.md) | Tavall Analytics |
| [WORKFLOWS_TECH_STACK.md](https://github.com/TavallStudios/tavall-workflows/blob/main/WORKFLOWS_TECH_STACK.md) | Tavall Workflows |
| [MC_TECH_STACK.md](https://github.com/TavallStudios/tavall-mc/blob/main/MC_TECH_STACK.md) | Project Novus |
| [CI_CD_TECH_STACK.md](https://github.com/TavallStudios/tavall-ci/blob/main/CI_CD_TECH_STACK.md) | Tavall CI/CD |

## Inventory status rules

- **CURRENT SOURCE:** confirmed on an inspected default branch; does not imply deployment.
- **ACCEPTED DESIGN:** documented intended boundary; deployment or acceptance may still be pending.
- **PROPOSED:** future idea, not installed or approved infrastructure.
- **SUPERSEDED:** retained only for provenance; must not silently be restored.
- **UNVERIFIED:** source or runtime check not completed; no optimistic assumptions.

Use system TECHNICAL DESIGN for detailed architecture and contracts, PROGRESSION for implementation evidence, and DEPLOYMENT for runtime acceptance. README files route to those owners; stack inventories are concise maps of technologies and their authority. A new framework, database, broker, queue or separate runtime requires an observed pressure point, an identified consumer and an explicit owner.