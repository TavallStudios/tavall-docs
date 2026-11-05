# Tavall Work Graph — GitHub Issues, QA Board, Linear and Notion Reconciliation

**Type:** TECHNICAL DESIGN / authority reconciliation DRAFT
**Date:** 2026-11-01
**Scope:** Tavall business/engineering tasks, not private personal reminders
**Owners:** `tavall-qa` (task execution/QA authority), `tavall-github-bot` (GitHub intake/API/CI projection), Tavall AI orchestrator (authorized cross-app adapter workflow), existing Linear and Notion connectors
**Related:** [Work Graph issue #9](https://github.com/TavallStudios/tavall-github-bot/issues/9), [Work Tracking](../quality/WORK_TRACKING.md), [QA Task Board technical design](https://github.com/TavallStudios/tavall-qa/blob/main/docs/technical/TAVALL_QA_TASK_BOARD_TECHNICAL_DESIGN.md).

## Recovered history and inconsistency

- Earlier Tavall work used Linear `TJ-...` issues with GitHub PR/Issue attachments; `linear-code[bot]` linked GitHub mirrors to Linear. One documented incident **incorrectly canceled Linear TJ-224** when an obsolete GitHub mirror closed. That must never recur.
- 2026-09-28: Notion human-facing Kanban and GitHub projections were emphasized.
- 2026-10-23: Work Graph #9 adopted **canonical owner-repository GitHub Issues** for engineering work, optional organization-wide GitHub Project views, generated repository TODOs; migration #9–#13 remains open and unfinished.
- 2026-10-24 through 10-30: `tavall-qa`/QA Board became **canonical task execution, evidence, checkpoint and Human Verify authority**; its technical design already defines an authorized Notion 1:1 task sync contract (Phase 6). Linear migration remains unresolved.
- 2026-11-01: Founder wants all these systems joined so delegating an action never requires remembering accounts, switching dashboards or reconstructing a task from prose.

**This design reconciles different kinds of authority; it does not retroactively relabel old GitHub or Linear records, change implemented QA APIs, silently replace Notion decisions, or claim a running synchronization service.** Existing draft technical designs and live runtime capability must be audited before promotion.

## Authority by field and object (not four task databases)

| Object/field | Write authority | External treatment |
| --- | --- | --- |
| Tavall execution task ID, scope, parent/child task graph, run/checkpoint/leases, task acceptance, evidence, QA state, Human Verify | `tavall-qa` via its typed handlers | Linked/projection only; source revisions protected |
| Repository-owned code/engineering work request, canonical GitHub Issue URL, PRs, check runs, source closure reason | GitHub Issue/PR in actual owning repository; GitHub Bot is authorized adapter | Link into QA; issue close is not sufficient for task acceptance |
| User planning/cycles/priorities and existing `TJ-...` Linear task records | Linear for its existing planning properties, and QA for execution truth | Map 1:1 when justified; do not invent a new Linear task if one already represents the work; external cancellation never automatically closes another authority |
| Human planning text and project/context databases | Notion for Notion-owned planning fields; QA ingests with existing `ITaskBoardNotionSyncHandler` under an approved map | No new Notion credentials, polling loop or QA-owned Notion state outside the accepted sync adapter |
| Global/repository `TODO.md` and dashboard/agent queue | **Generated views**, derived from canonical owner objects after migration | No reverse-import from generated text, no independent checkbox truth |
| CI, source, run/deployment evidence | Tavall CI / Cloud/Storage and GitHub SCM; QA references accepted receipts | Neither Linear status nor PR merge is runtime proof |
| Private/personal reminders | Existing private Notion + personal automations | **Separate scope**; no leakage into public company tasks or organization dashboards |

**Concrete resolution of the October conflict:** a Github Issue is the canonical **repository engineering issue identity**; QA is the canonical **execution/verification task identity**. Both may refer to the same actionable work via a stable mapping, but neither duplicates the other's permitted data. A Linear issue is a planning/workflow projection or an already existing legacy planning record; its close/cancel event is never a forced QA acceptance/GitHub close. A GitHub Project is optional read-only view, not a required additional authoritative planning board when Linear is already the operator view.

## November 5 founder authority and visualization direction

- **Engineering ledger = GitHub Issues in each owning repository.** No separate active JSON Agent Ledger, even for worker claims. Existing `tavall-agent-ledger` compatibility role must resolve GitHub issue identity and use QA typed APIs for active worker and execution state, or be retired after migrating consumers. Historical ledger snapshots remain read-only until audited.
- **QA owns execution**, including parent/child task graph, assignments, leases, checkpoints, evidence and acceptance. GitHub owns native issue/PR closure; CI/Cloud own their respective execution proof. Neither a GitHub Issue nor an issue board automatically constitutes a QA acceptance.
- **Permanent visual Work Graph** is an approved *design direction*, not deployed functionality: endpoint/venture and department navigation, persistent Tavall AI Employees/agents, scoped memory, linked work and evidence. Reuse Account/Organization authority, Tavall AI Chat's existing Tavs/Employees concept, its Memory Plane, QA read projections and the existing network file/graph representation only after verifying its exact owner and format.
- **Narrow acceptance slice:** one authorized endpoint → department → existing employee identity → GitHub Issue → QA task/lease/checkpoint/evidence, with refresh/restart and tenant/privacy E2E. Do not invent a new graph server, agent DB, task authority or scheduler.

## Cross-system mapping

Maintain a canonical, durable, owner-scoped mapping at an existing QA Task Board source-reference/sync boundary, not in a new stand-alone tracking database:

```
qaTaskId             stable QA-owned UUID
ownerRepository      e.g. TavallStudios/tavall-content
githubIssue          immutable GitHub owner/repo/issue_number and URL
linearIssue          optional existing or projected TJ-identifier + UUID
notionPage           optional workspace/database/page ID with approved mapping
sourceFingerprint    normalized intent+owner+source revision (not title alone)
lastObservedVersion  per-source revision/updatedAt/webhook/event identifier
lastAppliedVersion   per-destination accepted revision
syncRevision         QA monotonic revision, plus per-provider cursor
syncState            CONNECTED | PENDING | CONFLICT | ACTION_REQUIRED | FAILED
```

Do not use mutable issue title, PR number alone, Notion URL slug or Linear display name as identity. Prefer matching existing exact IDs and traceable original source before provisional fuzzy title matches; ambiguities go to an operator queue. Must support multiple PRs per issue and one QA initiative with several owner-repository child issues. Migration retains the original Linear UUID/ID and link associations.

## Updated upstream orchestration and document-type reconciliation (November 4, 2026)

The existing durable Tavall AI primary supervisory context is the *coordinator*, not a task store, runner or new long-lived scheduler. Its logical goal stores scoped source references, accepted decisions, dependencies, owner issues, budget caps and next action; provider-native Codex/Claude/Gemini harness sessions remain with their provider. Rehydrate from owned memory/temporal graph **as context** and confirm current owner API/PR/CI/QA state before each action. QA owns canonical task IDs, execution graph, leases and checkpoints, while QA remains the active owner of worker assignments, leases and checkpoints; execution receipts refer to QA or source-scoped provenance. The old Agent Ledger is historical, read-only and must not receive new task/worker state.

For each conversation turn or observed operational event: (1) classify accepted/proposed/revoked/superseded/private/actionable; (2) locate owner GENERAL, PRODUCT, DESIGN, TECHNICAL, PROGRESSION, MARKETING, and OPERATIONS/DEPLOYMENT documents as applicable; (3) update current document and approved Notion ↔ GitHub twin, preserving source/date/provenance and prior rationale; (4) identify existing owner issue by stable key and search open/closed/PRs; (5) update or create a narrow GitHub engineering issue only for a testable work slice; (6) use typed QA API to reuse/create linked task when authorized; (7) select granted provider/Cloud execution; (8) collect real CI/Cloud/Content/Commerce/Analytics receipts; (9) QA accepts work and independently requests Human Verify where appropriate. No new Notion recap page and no task status stored in arbitrary chat summary.

**Launch-aware prioritization:** Current founder-directed focus is P0 Content clip-publish-marketplace-submission-payout verification and P0 Tavall Times original Blog + Deals + Releases + eligible Impact affiliate conversion evidence; P1 TavallTech tech-watch launch and narrowly scoped Studio commercial-service pilots. Build dependency graph from existing owner Issues and QA; critical CI/Cloud/Account/Browser/Analytics issues become P0 only if proved to block a current release. Avoid holding initial revenue hostage to full Tavall AI Chat, autonomous operations, new paid-ad services or model training. Score READY candidates using minimum verifiable outcome, dependency criticality, approval/rights readiness, real external payment/public proof, estimated human effort/provider quotas and total cost per verified outcome. Tie-break with source-backed urgency, not speculative TAM or age.

**Negative paths:** revoked approval, stale source/brief, two identical chat intents, conflicting Linear versus GitHub status, provider rate-limit handoff, QA upsert unavailable, merchant/affiliate ineligible, unknown payout and protected tenant scope must fail into actual BLOCKED/ACTION_REQUIRED/PENDING/CONFLICT without issuing new IDs or writing fictional completion. A project board column or closed GitHub mirror never triggers QA acceptance or Linear cancellation; an accepted clip or PR is not received funds.

## Event and command flow

```
Operator/chat/agent request
   -> Tavall AI orchestrator: classify personal vs Tavall work, dedup, scope permissions
   -> owner GitHub Issue (create only when no exact work item exists)
   -> typed QA task identity / link (not a competing GitHub implementation DB)
   -> Tavall GitHub Bot: webhooks, PR / CI / accepted source receipts
   -> authorized Linear adapter: link existing TJ issue or project into the chosen Linear view
   -> authorized Notion adapter: planning context / approved one-to-one sync
   -> QA agent view: task, blocked reason, approval, lease, checkpoint, evidence
   -> Tavall AI provider harness + Cloud Executor / Cloud Browser as needed
   -> QA receipt and acceptance, human verify separately
   -> GitHub issue update, Linear plan status, Notion planning view, generated TODO projection
```

Prefer webhook/event ingestion where supported; use existing Orchestrator/Automations execution facilities for rate-limit-safe reconciliations. No new poller, service-wide cron, scheduler, outbound browser with privileged cookies, or second model agent framework. Callers use typed source adapters and `tavall-qa` owner mutations; external tool integrations do not update QA mapped JPA entities directly.

## Status mapping and conflict policy

- **Planning:** `INBOX/TODO/BACKLOG`, `READY`, `BLOCKED/ACTION_REQUIRED`, `DEFERRED` originate as planning changes that QA validates against current task scope and capability.
- **Execution:** `ACTIVE/IN_PROGRESS`, `REVIEW`, `VERIFY` use QA execution/lease/checkpoint and actual CI/source evidence. `COMPLETED` execution is only an observation.
- **Completion:** QA accepts task after verified current evidence and domain checks; `HUMAN_VERIFIED` is an independent, later grant-guarded action where applicable. GitHub native `closed/completed` applies only on issue-specific acceptance and authorized closure, never merely a green check, merged PR, Linear Done, or expired reminder. Linear Done may reflect QA-accepted work, but legacy stand-alone Linear tasks are not automatically converted or canceled.
- **Cancellation and deletion:** Closing duplicate/obsolete GitHub mirror with reason `duplicate`/`not_planned` updates only that mirror. **Do not cancel TJ-224-style Linear tasks, delete Notion pages, or set QA DONE** from the mirror event. Legitimate user-authorized cancellation targets an explicit QA task and per-service linked identity after permissions and revision checks.
- **Conflict:** A newer authorized Notion/Linear planning edit can propose priority, assignment or text changes; it cannot overwrite newer QA execution truth or human verification. Conflicting edits are recorded with source versions and surfaced for human/agent review. Fail closed on missing authority, missing source ID, unauthorized tenant, stale event or unknown closure semantics.
- **Privacy:** Private Notion pages, personal tasks, browser profiles, account data and agent continuation payloads never migrate into public or cross-company Linear/GitHub projects by default.

## Exact first pilot: Tavall Content Auto Account

Use [Tavall Content #76](https://github.com/TavallStudios/tavall-content/issues/76) as a **single end-to-end mapping case**, linked to existing parent [Tavall Content #52](https://github.com/TavallStudios/tavall-content/issues/52), existing Content/Linear planning [TJ-176](https://linear.app/projectnovus/issue/TJ-176/complete-tavall-content-authorized-media-platform) and the browser dependency [Tavall AI Browser PR #6](https://github.com/TavallStudios/tavall-ai-browser/pull/6). Do not duplicate the engineering task when attaching it to Linear.

1. Detect #76 once and resolve correct Content owner and related existing Linear work. Register a unique QA task only if current QA authority lacks an exact mapping.
2. Show state in the existing QA Board, Content operator dashboard, and Linear as linked work, respecting actual permissions. No fictional ready state.
3. For authorized tasks that need social-account signup, the Cloud Browser should use **durable user-owned logged-in profiles plus revocable task AuthLease**, so a task can pause for provider email/2FA/consent and resume. Provider signup requirements are not bypassed; headless automation resumes where allowed. Profile data stays with Cloud/Account; QA tracks only work state and safe references.
4. When the provider requires human action, persist `ACTION_REQUIRED`, precise next step and link via QA/Content task; use the user's **existing follow-up system** when authorized. No extra notifier and no indefinite silent stall.
5. Prove completion only after verified provider channel IDs/scopes and actual Content Auto Account consumer readiness, then appropriate QA acceptance. Browser execution success alone is not account creation success.

## Tests and adoption gates

- Read-only discovery first across current GitHub open/closed issues, Linear `TJ-...`, QA tasks, Notion pages and legacy 150-item TODO. Keep counts, exact source IDs and false-positive review.
- Pilot #76 with two identical ingestions: same QA ID, GitHub issue, Linear link, and Notion reference; no duplicates. Test direct edits from each authorized surface, event replay/out-of-order messages, retry after crash, partial external API outages, rate limits and permission loss.
- Verify PR merge/CI evidence does not prematurely close issue or QA task; demonstrate distinct SOURCE_MERGED, SOURCE_VALIDATED, DELIVERED, RUNTIME_VERIFIED; Human Verify remains separate.
- Explicit regression for **GitHub mirror closure not canceling Linear TJ-224** and for a closed original implementation issue (#52) having a separate open completion/verification issue (#76) without reopening #52.
- Validate no private Notion content or Cloud Browser credential fields are projected to unauthorized UI. Per-organization and per-task authorizations and human commitment approvals are rechecked.
- Verify durable QA mapped PostgreSQL state, exact source SHAs, source-owned CI, restart/replay after outage and UI/browser E2E at desktop/mobile.
- Once and only once all source mappings/reviews reconcile, archive prior `tavall-docs/TODO.md`, enable read-only generated per-repo TODO and cross-system views. Validate two byte-identical reruns and rollback.
- Update the existing [Work Graph initiative #9](https://github.com/TavallStudios/tavall-github-bot/issues/9), its #10–#13 slices and QA consumer issue with a single ownership map. Do not create a mandatory GitHub Projects workflow that duplicates Linear/QA without demonstrated operator value.

**Current implementation status:** Conceptual reconciliation from current docs, prior user decisions, live GitHub/Linear connected reads. No live cross-system sync E2E, Cloud Browser production profile, Notion adapter runtime or generated TODO cutover has been proven. This design is a reviewable handoff, not runtime acceptance.
