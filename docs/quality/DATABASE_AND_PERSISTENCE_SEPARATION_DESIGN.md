# Tavall Database and Persistence Environment Separation — DESIGN

> **Document Type:** `DESIGN`  
> **Scope:** `SYSTEM`  
> **Lifecycle:** `FINAL_DRAFT`  
> **Status:** Proposed / Accepted Baseline  
> **Owning Product / Platform:** Tavall Cloud Infrastructure & Application Platform  
> **Primary Repository:** `TavallStudios/tavall-docs`  
> **Owning Module:** N/A (`SYSTEM` scope)  
> **Owning GENERAL:** [NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md)  
> **Technical Document:** Combined with this design record  
> **Progression Document:** [TAVALL_PROGRESSION_OVERVIEW.md](../progression/TAVALL_PROGRESSION_OVERVIEW.md)  

---

## 1. About

This system DESIGN defines the binding Tavall-wide architecture for database isolation, persistent schema ownership, application role permissions, credential injection, and migration lifecycle across all software environments.

Historically, multiple services (`tavall-web`, `tavall-qa`, and legacy `tavall-mc` components) co-located disparate data domains within a single mixed development database (`novus_web`), while service runtime environments (DEVELOPMENT, STAGING, PRODUCTION) lacked strict operational database fences.

This specification institutes complete, non-negotiable database and credential boundaries:
1. **Clean Environmental Separation:** Every registered logical service has isolated databases, roles, and secret bindings for each environment classification (`DEVELOPMENT`, `STAGING`, `PRODUCTION`).
2. **Zero Shared Data Boundaries:** STAGING and PRODUCTION runtimes must never connect to, read from, write to, or share credentials with DEVELOPMENT databases.
3. **Role & Privilege Minimization:** Administrative database owners (who own DDL and run migrations) are strictly separated from runtime application roles (which possess least-privilege DML only).
4. **Out-of-Band Migrations:** Database schema migrations are executed by authorized deployment procedures prior to runtime activation, never implicitly by application code on boot.

---

## 2. Scope & Ownership

### 2.1 Owns
- Cross-system naming standards for relational databases, database roles, and schemas across all runtime environments.
- Least-privilege role separation: Administrative Owner vs. Application Runtime Role.
- Filesystem layout and permission standards for environment database credentials under `/etc/tavall-cloud/secrets/`.
- Safe out-of-band migration execution lifecycle, rollout ordering, and rollback compatibility requirements.
- Backup mandates, retention topology, and disaster recovery verification procedures (`pg_dump -Fc`).
- The transition checklist required before deploying or provisioning PRODUCTION persistence.

### 2.2 Does Not Own
- Module-local entity mappings, JPA annotations, or domain queries (owned by domain service repositories per [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)).
- Redis live coordination keyspaces or Cloud job fences (owned by `tavall-cloud` and `tavall-database-redis-api`).
- Physical disk pool allocation or ZFS dataset volume layout (owned by `tavall-filesystem`).

### 2.3 Sibling Boundaries
- **[NLEW_AND_SERVICE_OWNERSHIP.md](NLEW_AND_SERVICE_OWNERSHIP.md):** Governs Node, Lane, Environment, and Workspace definitions. A service Environment represents a deployed runtime target; database attachments map directly to that Environment's classification.
- **[CI_CD.md](CI_CD.md):** Enforces CD fences, exact-source CI evidence, and immutable artifact verification prior to staging or production migration.

---

## 3. Environment Separation Architecture

### 3.1 Canonical Service Runtime Classifications
Per Tavall NLEW doctrine, services exist in three canonical classifications:
- **DEVELOPMENT (`dev`):** Iterative development, local worker testing, and Development Staging verification.
- **STAGING (`staging`):** Exact production-equivalent validation of promoted, immutable release artifacts. Must run against clean staging data stores.
- **PRODUCTION (`prod`):** Accepted live releases serving real users, transactions, and authoritative production state.

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          TAVALL DATA ISOLATION MODEL                            │
├──────────────────────┬──────────────────────────┬───────────────────────────────┤
│     DEVELOPMENT      │         STAGING          │          PRODUCTION           │
├──────────────────────┼──────────────────────────┼───────────────────────────────┤
│ • dev-storage host   │ • Isolated staging DB    │ • Production node / cluster   │
│ • Local PG14 / Redis │ • Clean schema copy      │ • Dedicated hardware / failover│
│ • Dev test data only │ • Prod-equivalent seed   │ • Encrypted at rest & transit │
│ • App Role: *_dev    │ • App Role: *_staging    │ • App Role: *_prod            │
│ • Secret: *-dev.env  │ • Secret: *-staging.env  │ • Secret: *-prod.env (prod)   │
└──────────────────────┴──────────────────────────┴───────────────────────────────┘
  ▲                      ▲                          ▲
  │                      │                          │
  └── No Cross-Access ───┴── Strictly Forbidden ────┘
```

### 3.2 Prohibited Anti-Patterns
1. **No Shared Databases Between Environments:** Pointing a STAGING service at a DEVELOPMENT database or vice versa is strictly prohibited.
2. **No Shared Roles or Credentials:** An application runtime role created for DEVELOPMENT must not have access to STAGING or PRODUCTION databases.
3. **No Mixed Multi-Service Databases:** Co-locating distinct microservice domains (e.g. Content vs. Web SSO vs. Ops vs. QA) within a single database creates unmanageable migration locks and breaks failure domains. Each service owns its dedicated database.

---

## 4. Database & Role Naming Conventions

### 4.1 Relational Database Naming
PostgreSQL databases must follow the uniform naming pattern:
```text
<service_identifier>_<environment>
```

| Service | DEVELOPMENT DB | STAGING DB | PRODUCTION DB |
|---|---|---|---|
| Tavall Web (SSO / Account) | `tavall_web_development` | `tavall_web_staging` | `tavall_web_production` |
| Tavall Web Ops | `tavall_ops_development` | `tavall_ops_staging` | `tavall_ops_production` |
| Tavall Content | `tavall_content_development` | `tavall_content_staging` | `tavall_content_production` |
| Tavall QA Task Board | `tavall_qa_development` | `tavall_qa_staging` | `tavall_qa_production` |
| Tavall FFA / Game Backend | `novus_ffa_development` | `novus_ffa_staging` | `novus_ffa_production` |

*Migration note:* Existing legacy database `novus_web` serves as the transitional DEVELOPMENT database during active feature work and is decoupled into isolated `tavall_web_*` and `tavall_qa_*` targets.

### 4.2 Role Naming & Separation of Privilege
Every service environment requires two distinct database roles:

#### 1. Schema Owner / Migration Role
- **Name:** `postgres` (or `<service_identifier>_<environment>_owner` in delegated environments).
- **Attributes:** `NOSUPERUSER` (when delegated), owns the schema and all objects.
- **Grants:** Full DDL authority: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `INDEX`, `TRIGGER`.
- **Usage:** Used exclusively by automated migration tools during deployment. Application runtimes never receive owner credentials.

#### 2. Application Runtime Role
- **Name:** `<service_identifier>_<environment>` (e.g. `tavall_web_staging`, `tavall_ops_development`).
- **Attributes:** `NOSUPERUSER`, `NOCREATEDB`, `NOCREATEROLE`, `NOINHERIT`, `LOGIN`.
- **Grants:** Least-privilege DML only:
  - `CONNECT ON DATABASE <service>_<environment>`
  - `USAGE ON SCHEMA <schema>`
  - `SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema>`
  - `USAGE, SELECT ON ALL SEQUENCES IN SCHEMA <schema>`
- **Explicit Denials:** No DDL rights. Cannot `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, or bypass table policies.

---

## 5. Secret File Layout & Ingestion

### 5.1 Storage Directory & File Hierarchy
Runtime credentials and database connection parameters are provisioned exclusively on the host filesystem under `/etc/tavall-cloud/secrets/`:

```text
/etc/tavall-cloud/secrets/
├── <service>-development.env
├── <service>-staging.env
└── [PRODUCTION on production nodes only]
```

### 5.2 Filesystem Permissions
Database secret files must strictly enforce POSIX ownership and permissions:
- **Owner:** `root:tavall-cloud`
- **Mode:** `0640` (`-rw-r-----`)
- **Validation:** Deployments and health checks fail immediately if permissions allow world readability (`0004` or `0002`).

### 5.3 Systemd Service Ingestion
Tavall Cloud deployments inject environment secrets via unit drop-ins:
```ini
# /etc/systemd/system/tavall-cloud-deployment@<service>-<env>-<gen>.service.d/10-database.conf
[Service]
EnvironmentFile=-/etc/tavall-cloud/secrets/<service>-<env>.env
```
Application runtimes receive database connection parameters (`DB_URL`, `DB_USER`, `DB_PASS`) directly in memory via environment variables. Secret values must never be checked into Git, printed in logs, or exposed in CI/CD artifacts.

---

## 6. Migration Lifecycle & Rollout Strategy

### 6.1 Out-of-Band Execution Mandate
Applications must **never** execute database migrations on application startup.
- Starting a service against an unmigrated database must log an error and exit gracefully.
- Schema migrations are executed out-of-band by the deployment pipeline (`deploy-dev.sh` or staging/production CD gates) *before* activating the new runtime generation.

### 6.2 Backward Compatibility Window (Expand / Contract)
All schema changes in STAGING and PRODUCTION must support rolling or blue/green deployments:
1. **Phase 1 (Expand):** Add columns (with `NULL` or default), new tables, and views. Existing running code continues to function without error.
2. **Phase 2 (Promote Runtime):** Deploy and verify the new service generation.
3. **Phase 3 (Contract):** Once the old generation is completely stopped and drained, execute cleanup migrations to remove obsolete columns or drop temporary triggers.

---

## 7. Backup, Restore, and Disaster Recovery

### 7.1 Pre-Mutation Backup Rule
**No direct database modification, migration, or structural repair may occur without a verified full backup taken immediately prior to execution.**

- **Target Path:** `/srv/storage-0/backups/<database_name>/`
- **Format:** PostgreSQL custom archive format (`pg_dump -Fc`), which supports compressed storage and granular object restoration.
- **Naming Pattern:** `<database_name>_pre_<change_description>_<YYYYMMDDTHHMMSSZ>.dump`

### 7.2 Verification & Restoration
Backups must be verifiable using `pg_restore --list <dump_file>`. A database recovery procedure must be documented and tested for every production-bound service.

---

## 8. Production Database Readiness Checklist

Before any production database or role is provisioned, the owner and release engineering must verify:

- [ ] **Infrastructure Fencing:** Dedicated production database cluster isolated from `dev-storage`.
- [ ] **Network ACLs:** PostgreSQL port bound only to private overlay interfaces (`10.x.x.x`), blocked from public ingress.
- [ ] **Role Isolation:** App role granted only DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`); DDL restricted to administrative migration identity.
- [ ] **Connection Pooling:** Sized according to node capacity with explicit connection limits per role (`ALTER ROLE <name> CONNECTION LIMIT 50;`).
- [ ] **Automated Backup Schedule:** Daily automated `pg_dump -Fc` with encrypted offsite replication and 30-day retention.
- [ ] **Secret Rotation:** Automated or documented credential rotation procedure without application downtime.
- [ ] **Telemetry & Slow Query Logging:** `pg_stat_statements` enabled, slow queries logged above 250ms threshold.
- [ ] **Disaster Recovery Drill:** Documented recovery runbook with RPO < 15 minutes and RTO < 1 hour.
