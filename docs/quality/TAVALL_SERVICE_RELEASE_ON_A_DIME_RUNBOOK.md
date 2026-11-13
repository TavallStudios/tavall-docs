# Tavall Service Release on a Dime Runbook

> **Status:** Active Operational Runbook  
> **Document Type:** Deployment / Technical Runbook  
> **Authority:** [CI_CD.md](CI_CD.md) § CD boundary, [GIT_WORKFLOW.md](GIT_WORKFLOW.md) § 6. Production promotion and deployment  
> **Audited Git Base:** `9e2b1a99bd02617271fdf9b8151724d62176d67b`  
> **Owns:** Typed service release promotion across DEVELOPMENT → STAGING → PRODUCTION, immutable artifact propagation without rebuilds, release verification, rollback execution, and service-specific release checklists.  
> **Does not own:** Application source logic, database schema migrations (owned by wDB), or infrastructure network topology.

---

## 1. Core Operating Principles

1. **Zero-Rebuild Immutable Promotion**:
   CI validates exact source commits and builds content-addressed immutable artifacts (`tavall-storage://artifacts/sha256/<digest>`). The exact same artifact bytes and digest that pass CI and achieve health verification in DEVELOPMENT are promoted directly to STAGING and PRODUCTION. Source code is never recompiled per environment.

2. **Typed Cloud CLI Path**:
   All release mutations execute strictly via the authoritative Tavall Cloud CLI:
   - `tavall service deploy plan <service-id> [options]`
   - `tavall service deploy apply <service-id> [options]`
   - `tavall service deploy verify <service-id> [options]`
   - `tavall service deploy promote <service-id> [options]` (shifts STANDBY to ACTIVE in A/B production)
   - `tavall service deploy rollback <service-id> [--revision <sha>]`

3. **Separation of Concerns**:
   - Merging source into Git `main` does not deploy software.
   - Database credentials and migrations are separated per environment (coordinated with wDB; see `DATABASE_AND_PERSISTENCE_SEPARATION_DESIGN.md`).
   - Production promotion is pre-authorized (Owner Directive 2026-11-07: deploy aggressively, zero users) following an exact-head REQUIRED_ALL PASS, typed Cloud deployment, deployer actor record, and documented rollback target. Backup via `pg_dump` is mandatory before any production DB migrations.

---

## 2. Universal Promotion Pipeline (DEV → STAGING → PRODUCTION)

```text
+-------------------------------------------------------------+
| 1. CI Validation: exact source -> tests -> immutable artifact|
|    (Harness CI Gate: REQUIRED_ALL PASS)                     |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 2. Development Deployment & Verification                    |
|    plan -> apply -> verify (Runtime: DEVELOPMENT / ACTIVE)   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 3. Staging Promotion (Exact Artifact Reuse)                  |
|    plan (PLAN_ONLY=1) -> apply -> verify                    |
|    (Runtime: STAGING / STANDBY / port 19093/19103)          |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 4. Production Pre-Authorization & Rollback Pinning          |
|    Deployer records actor identity & verified rollback target|
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 5. Production A/B Deployment & Traffic Promotion            |
|    apply (STANDBY) -> verify -> promote (STANDBY -> ACTIVE) |
|    (Automatic rollback to LAST_KNOWN_GOOD if unhealthy)     |
+-------------------------------------------------------------+
```

---

## 3. Step-by-Step Command Execution

### Step 1: Resolve Artifact and Delivery Bundle
From the passing CI gate run (`/srv/dev-storage/ci-evidence/runs/<ci-run-id>/ci-evidence.json`):
```bash
# Extract artifact digest, version, and repository
ARTIFACT_DIGEST="<sha256-from-ci-evidence>"
ARTIFACT_NAME="<artifact-name>"
ARTIFACT_VERSION="<version>"
SOURCE_REPO="<owner/repo>"
SOURCE_SHA="<exact-40-char-sha>"
CI_RUN_ID="<ci-request-id>"
```

Freeze the delivery bundle combining the CI evidence and service `.tavallcd` template:
```bash
TID="services/<service-id>"
TSHA=$(sudo -n tavall service cd status <service-id> | jq -r '.data.serviceTemplateSha256')
RID=$(sudo -n tavall service cd status <service-id> | jq -r '.data.runtimeId')

BUNDLE=$(cd /srv/dev-storage/workspaces/tavall-ai/repo_root && \
  java --class-path '/srv/dev-storage/workspaces/tavall-ci/diagnostics/accepted-f30a5da-01a175ae/caller/tavall-ci-cloud-caller-0.1.0-SNAPSHOT/lib/*' \
  FreezeDeliveryBundle.java /srv/dev-storage/ci-evidence/runs/$CI_RUN_ID/ci-evidence.json \
  /srv/dev-storage/templates/$TID delivery-bundle.json | sed -n 's/^frozenDeliveryBundle=//p')
```

### Step 2: Dry-Run Plan for Target Environment
Execute plan with `mutatesHost=false`:
```bash
sudo -n tavall service deploy plan <service-id> \
  --revision "$SOURCE_SHA" \
  --artifact-digest "$ARTIFACT_DIGEST" \
  --artifact-ref "tavall-storage://artifacts/sha256/$ARTIFACT_DIGEST" \
  --artifact-name "$ARTIFACT_NAME" \
  --artifact-version "$ARTIFACT_VERSION" \
  --ci-run-id "$CI_RUN_ID" \
  --ci-evidence-id "tavall-storage://ci/runs/$CI_RUN_ID" \
  --source-repository "$SOURCE_REPO" \
  --target-environment STAGING \
  --service-template-id "$TID" \
  --service-template-sha256 "$TSHA" \
  --delivery-bundle-digest "$BUNDLE" \
  --runtime-id "$RID" \
  --runtime-slot SINGLE \
  --runtime-traffic STANDBY
```

### Step 3: Apply Deployment to Target Environment
```bash
sudo -n tavall service deploy apply <service-id> \
  --revision "$SOURCE_SHA" \
  --artifact-digest "$ARTIFACT_DIGEST" \
  --artifact-ref "tavall-storage://artifacts/sha256/$ARTIFACT_DIGEST" \
  --artifact-name "$ARTIFACT_NAME" \
  --artifact-version "$ARTIFACT_VERSION" \
  --ci-run-id "$CI_RUN_ID" \
  --ci-evidence-id "tavall-storage://ci/runs/$CI_RUN_ID" \
  --source-repository "$SOURCE_REPO" \
  --target-environment STAGING \
  --service-template-id "$TID" \
  --service-template-sha256 "$TSHA" \
  --delivery-bundle-digest "$BUNDLE" \
  --runtime-id "$RID" \
  --runtime-slot SINGLE \
  --runtime-traffic STANDBY
```

### Step 4: Verify Runtime Health
Probes loopback health endpoint (e.g. `http://127.0.0.1:19093/health`) requiring 3 consecutive healthy observations:
```bash
sudo -n tavall service deploy verify <service-id> \
  --target-environment STAGING \
  --runtime-slot SINGLE \
  --runtime-traffic STANDBY
```

### Step 5: Production Traffic Promotion (A/B)
Production deployment is pre-authorized (Owner Directive 2026-11-07: deploy aggressively, zero users). For PRODUCTION target, candidate is deployed to STANDBY, health-verified, and then shifted to ACTIVE:
```bash
sudo -n tavall service deploy promote <service-id> \
  --revision "$SOURCE_SHA" \
  --artifact-digest "$ARTIFACT_DIGEST" \
  --artifact-ref "tavall-storage://artifacts/sha256/$ARTIFACT_DIGEST" \
  --runtime-instance-id "<prod-runtime-instance-id>" \
  --deployment-generation <generation> \
  --promotion-authorization-bundle-digest "$BUNDLE" \
  --promotion-authorization-actor "<deploying-agent-identity>" \
  --promotion-authorized-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 6: Rollback Procedure (Emergency or Failed Health)
When health verification fails or an operational defect occurs:
```bash
# Rollback to the previous complete health-verified release:
sudo -n tavall service deploy rollback <service-id>

# Or explicitly rollback to a known revision:
sudo -n tavall service deploy rollback <service-id> --revision <known-good-sha>
```

---

## 4. Per-Service Release Checklists

### A. Tavall Web (`tavall-web`)
- [ ] **Exact-Source CI Gate**: REQUIRED_ALL PASS on `staging/runtime-web` or `main`.
- [ ] **Artifact Verification**: `tavall-web.jar` content-addressed SHA-256 confirmed in `/srv/tavall-storage/development/artifacts/sha256/`.
- [ ] **Account Everywhere Check**:
  - `account.tavall.org/sign-in` reachable and active.
  - Navbar sign-in links resolve properly.
  - All protected dashboard / creator endpoints return HTTP 302 redirect to Account SSO.
- [ ] **Admin Boundary**: Public Apache vhosts deny `/admin/*`, `/control/*`, `/internal/*`. Runtimes bound to loopback `127.0.0.1:19092` / `127.0.0.1:19093`.
- [ ] **Database Coordination**: Check with wDB that Postgres schema migrations (if any) are applied.
- [ ] **Health Probe**: `GET http://127.0.0.1:19092/health` (DEV) or `19093/health` (STAGING) returns HTTP 200 `UP`.

### B. Tavall Content (`tavall-content`)
- [ ] **Exact-Source CI Gate**: REQUIRED_ALL PASS on `tavall-content`.
- [ ] **Artifact Verification**: `tavall-content-runtime` artifact digest verified.
- [ ] **Account Connection Check**: Social link callbacks (TikTok / YouTube) point to `account.tavall.org/connections`.
- [ ] **Render Worker Dependency**: `tavall-content-render-worker` is RUNNING and accepting job RPCs on port 19110.
- [ ] **Storage Mounts**: Media storage `/srv/tavall-storage/tavall-content/studio-media` mounted and writable.
- [ ] **Health Probe**: `GET http://127.0.0.1:19101/actuator/health` returns HTTP 200 `UP`.

### C. Tavall Content Render Worker (`tavall-content-render-worker`)
- [ ] **Exact-Source CI Gate**: REQUIRED_ALL PASS.
- [ ] **Artifact Verification**: `tavall-content-render-worker` jar content-addressed SHA-256 verified.
- [ ] **Private Ingress**: Gated strictly to loopback (`127.0.0.1:19110`). No public Apache exposure.
- [ ] **Health Probe**: `GET http://127.0.0.1:19110/actuator/health` returns HTTP 200 `UP`.

### D. Tavall Web Ops (`tavall-web-ops`)
- [ ] **Exact-Source CI Gate**: REQUIRED_ALL PASS on `tavall-web-ops`.
- [ ] **Artifact Verification**: `tavall-web-ops-runtime` digest verified.
- [ ] **Private Overlay Only**: Accessible strictly via Tailscale (`100.100.155.72`) or Nebula (`10.91.0.1`) SSH tunnel on port 19081. Public Apache routing completely absent.
- [ ] **Owner Authorization**: Operator token and bootstrap credentials active (`~/.config/tavall/ops/owner-bootstrap.txt`).
- [ ] **Health Probe**: `GET http://127.0.0.1:19081/health` returns HTTP 200 `UP`.

---

## 5. Documentation Update State

- **Document Version:** 1.0.0
- **Governing Revisions:** `tavall-docs@9e2b1a99`, `tavall-web@3aac710`, `tavall-content@2a99949`, `tavall-web-ops@9a81068`
- **Audit Receipt:** Validated against canonical Cloud CLI `tavall service deploy` on 2026-11-07.
