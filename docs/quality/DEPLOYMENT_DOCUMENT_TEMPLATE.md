# Deployment Document Template

> **Status:** Active template  
> **Document type:** Deployment  
> **Use when:** A repository/module owns an independently deployable system  
> **Authority:** [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) and [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)

Deployment documents answer **what is deployed where now, what was deployed before, and what deployment events occurred**. They do not replace deployment architecture, release policy, CI/CD design, or Progression/Evidence.

## Naming

Use:

- `<DEPLOYABLE_SYSTEM>_DEPLOYMENT.md` when the repository has multiple deployable systems/runtimes;
- `DEPLOYMENT.md` only when the repository has exactly one unambiguous deployable system.

Examples:

```text
TAVALL_CLOUD_NODE_DEPLOYMENT.md
TAVALL_CLOUD_CHATGPT_WEB_DEPLOYMENT.md
TAVALL_CI_RUNTIME_DEPLOYMENT.md
```

## Template

```markdown
# <System> Deployment

> **Status:** Active deployment record  
> **Owns:** Current and historical deployment state for `<system>`  
> **Does not own:** Deployment architecture, CI/CD policy, product behavior, implementation progression, or release design

## About

<Identify the deployable system/runtime and its deployment boundary.>

## Deployment Targets

| Target | Type | Runtime / Service | Authority |
| --- | --- | --- | --- |
| Development | `DEVELOPMENT` | ... | ... |
| Staging | `STAGING` | ... | ... |
| Production | `PRODUCTION` | ... | ... |

Only include targets that actually exist.

## Current Deployments

| Target | Source | Artifact / Release | Runtime / Service | State | Deployed | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ... | `<repository>@<commit>` | ... | ... | `ACTIVE` | `YYYY-MM-DD h:mm AM/PM PST/PDT` | ... |

Current Deployments is the present-state snapshot. One current row per active target/runtime identity is preferred unless parallel deployment is intentional, such as a production A/B pair.

## Deployment History

| Timestamp | Target | Source | Event | Replaced / Previous | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `YYYY-MM-DD h:mm AM/PM PST/PDT` | ... | ... | `DEPLOYED` | ... | `SUCCESS` | ... |

Deployment History is append-only operational evidence. Do not delete an old deployment event merely because a newer deployment replaced it.

Canonical event vocabulary:

- `DEPLOYED`
- `PROMOTED`
- `REPLACED`
- `ROLLED_BACK`
- `RESTORED`
- `DISABLED`
- `RETIRED`
- `FAILED`

Use a different explicit event only when none of these accurately describes the deployment transition.

## Current Deployment Notes

<Only current exceptional operational context that materially affects interpreting the deployment table. Do not turn this into an operations journal.>

## Related Documentation

- Design / Final: ...
- Technical / deployment architecture: ...
- Progression / Evidence: ...
- Runtime module README: ...
- CI/CD / release owner: ...

## Documentation Update State

<Use the canonical Documentation Update State footer from DOCUMENTATION_STANDARDS.md.>
```

## Ownership Rules

- Deployment documents are operational records, not design contracts.
- The current deployment table must identify exact source/release evidence whenever available; avoid floating branch names as the only identity.
- Deployment history preserves successful and failed transitions, including rollback/restoration.
- Progression/Evidence answers whether the deployment capability or system behavior is implemented and validated. Deployment answers what instance/release is actually running or was run.
- The repository/module README shows only a basic current deployment summary and links here for the full record.
- One Deployment document owns one independently deployable system. A multi-runtime repository uses system-qualified deployment documents instead of one giant mixed ledger.
- Deployment documents are required 1:1 GitHub ↔ Notion documents for deployable Tavall systems.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/DEPLOYMENT_DOCUMENT_TEMPLATE.md` | 2026-09-27 11:45 AM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 11:45 AM PDT | Quality template; deployment instances, not this template, carry the required 1:1 sync rule. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 11:45 AM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/DEPLOYMENT_DOCUMENT_TEMPLATE.md` | — | Direct docs-only update to `main`. | Added canonical Deployment document structure, event vocabulary, and 1:1 surface rule. |

</details>
