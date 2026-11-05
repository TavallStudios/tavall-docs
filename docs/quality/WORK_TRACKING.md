# Tavall Work Graph — Work Tracking Authority and Migration

> **Status:** ACTIVE AUTHORITY RECONCILIATION / QA EXECUTION PILOT  
> **Document Type:** Engineering operations policy and technical migration contract  
> **Authority:** Tavall Docs (policy); each GitHub Issue owns its own task state  
> **Execution authority:** [Tavall QA](https://github.com/TavallStudios/tavall-qa/issues/6); GitHub adapter: [Tavall GitHub Bot](https://github.com/TavallStudios/tavall-github-bot/issues/16)  
> **Established:** 2026-10-22; **reconciled:** 2026-11-04

## 1. Decision and non-goals

**One Work Graph, distinct authority by object.** GitHub owner-repository Issues own engineering requirement identities and GitHub-native issue closure; Tavall QA owns executable task graph, grants, claims/leases, checkpoints, acceptance evidence and Human Verify. Existing Linear TJ issues retain their planning fields. Notion owns product, design, technical, progression and portfolio decisions. Tavall AI provides the persistent supervisory context, context retrieval, task decomposition and cross-provider dispatch; it does not own another task database. The old Agent Ledger is retired. GitHub Issues are the engineering-work ledger; QA owns current worker assignments/claims, execution checkpoints and receipts. CI owns exact-source verification/promotion evidence; Cloud owns deployment/run-state; Content/Commerce/Analytics own actual external results. A GitHub Project/dashboard/TODO is a derived view, never a competing task authority.

This does not introduce a new task database, a replacement GitHub App, a new Tavall Cloud scheduler, an agent framework, or a source-of-truth in the Web/QA UI. Existing QA and Web views consume read-only task/evidence projections when later authorized.

### November 5, 2026: Founder decision — retire Agent Ledger authority

**GitHub Issues are the engineering ledger.** Preserve GitHub owner/repository/immutable issue identity, including issues created or updated by authorized Tavall AI agents. The retired JSON Agent Ledger is historical, read-only material until reconciliation. No separate live Agent Ledger task list, claims file, scheduler, or second status authority is permitted. Any compatibility Agent named `tavall-agent-ledger` must act only as a GitHub Issues + typed QA adapter, or be renamed/retired with its consumers migrated; it cannot revive ledger storage.

**QA Task Board owns execution.** Scope, parent/child tasks, assignments, leases, checkpoints, evidence, acceptance and Human Verify remain QA-owned. Engineering issue close is separate from execution acceptance. Preserve private/personal reminders outside the company work graph.

**Permanent visual Work Graph (approved direction; not implemented).** Project endpoint/venture → department → Tavall AI Employee/agent relationships with linked GitHub issues, QA execution state, CI/Cloud evidence, and authorized memory context. Reuse Tavall Account/Organization identity, existing Tavall AI Chat Tavs/Employees design, QA, Graphify/Graphiti and the existing network-accessible work representation after its exact path/contract is verified. The UI is a projection, not a new database, worker scheduler or identity provider; shared agents may serve multiple endpoints with scoped grants. Prototype one endpoint, department, employee and QA task with restart/authorization/E2E evidence before any broader build.

## 2. Orchestrated Work Graph and source-to-task flow

Operator/chat/monitor → Tavall AI durable supervisor (intent, constraints, permission, memory source pointers, accepted decision and goal) → existing owner PRODUCT/DESIGN/TECHNICAL/PROGRESSION/MARKETING documentation → GitHub Bot owner-repository issue dedup → Tavall QA typed task creation/reuse → provider-native Codex/Claude/Gemini worker through authorized Cloud or Personal Computer execution → QA-owned lease/checkpoint and source-linked execution receipt → CI/Cloud/product-specific evidence → QA acceptance / Human Verify → authorized GitHub/Linear/Notion/Projects projections.

Each discussion is classified as ACCEPTED_DECISION, PROPOSED, RESEARCH, REVOKED, SUPERSEDED, EXISTING_WORK, ACTIONABLE, VERIFIED_COMPLETE, PRIVATE_ONLY or NONACTIONABLE. Preserve source pointers, date, rationale, confidence, supersession and owner. **Capture all valuable decisions in the right existing document types, not a new global Notion backfill page and not a new issue per idea.** Create an engineering issue only for a verifiable owned work slice. Update existing issues for changed requirements after searching open and closed issues and PRs.

**Document type routing:** GENERAL = what/why/boundaries; PRODUCT = audience, commercial promise and launch gates; DESIGN = chosen product behavior and alternatives; TECHNICAL = interfaces, module ownership, storage, permissions and failure contracts; PROGRESSION = observed source, CI, QA, deployment evidence and blockers; MARKETING = channels, offers, growth and revenue measurement; DEPLOYMENT/OPERATIONS = verified production state and operator runbooks. Preserve existing Notion ↔ GitHub design/progression twins and lifecycle status rather than generating duplicate documents. Not every conversation requires every type; each relevant type is kept current.

**Orchestration continuity:** A single durable primary supervisory context is scoped to authorized owner/goal and delegates to provider-native harnesses, including different providers and their own optional subagents. Retrieve history from owned memory/temporal graphs and source pointers; do not copy whole provider web chats or mix tenants. QA owns persisted task/checkpoint/lease states; Cloud owns placement/permissions, CI owns exact-source checks, QA owns active worker coordination through authorized typed task APIs. Recover safely after provider quota, restart, cancellation or failed validation. Friction-driven meta-loop proposes tested task-specific loops through existing Workflows, not a new service or scheduler.

**Authority reconciliation:** A GitHub Issue is the canonical engineering issue identity; a QA task is the canonical executable task/verification identity. Existing Linear IDs are planning references, not a second QA status. Notion owns human planning and design. A closed duplicate GitHub mirror must never cancel a Linear task or close QA work. No GitHub Project workflow edit may silently override QA truth. Full mapping, idempotency, negative paths and the TJ-224 incident are documented in the existing [cross-system TECHNICAL DESIGN PR #95](https://github.com/TavallStudios/tavall-docs/pull/95) and [GitHub Bot #16](https://github.com/TavallStudios/tavall-github-bot/issues/16); this policy sets precedence without duplicating that implementation spec.

## November 4, 2026: founder clarification on default intake approval

**Default policy for the Tavall conversation backlog:** every substantive Tavall idea, feature, improvement, architecture direction, venture opportunity, reusable workflow, research question, or launch proposal discussed during the current ten-day reconciliation is **approved for documentation and backlog intake unless the founder explicitly rejected, revoked, replaced or scoped it out**. This supersedes the previous overly conservative approach that required a second confirmation to *write* a specification or *queue* a verifiable task. It does **not** assert that every idea was previously accepted as a finalized design, built, prioritized P0, or authorized for external execution.

- **Capture in place:** update the canonical existing GENERAL, PRODUCT, MARKETING, USER EXPERIENCE, DESIGN, TECHNICAL, PROGRESSION, ARTICLE and Deployment owners relevant to each topic, with source/decision date and owner. An existing issue/PR/document counts as coverage only if it **actually specifies** the distinct requirement and acceptance. Do not dump all ideas into a standalone Notion recap or auto-generate one issue per utterance.
- **Approve intake, not spend:** non-rejected candidates carry `INTAKE_APPROVED` and their actual maturity (`ACCEPTED_DESIGN`, `DESIGN_CANDIDATE`, `RESEARCH_CANDIDATE` or `IMPLEMENTATION_READY`) independently. An unresolved vendor choice, pricing number, model benchmark, architecture alternative or legal/financial term remains an explicitly testable choice, not a secretly finalized decision. Rights/terms and product claims need owner-specific proof before publication, purchase, external connection, training, deployment, or signing.
- **Hard exclusions:** explicit founder revocation and supersession govern. The abandoned standalone tiered Suggest skill and typed Flow Recipes as a Workflows core feature must not be reactivated; Web Chat flow experiences and ordinary contextual suggestions remain separate accepted design. Rejected campaign opportunities, prohibited footage rights and previous exact brand/artifact edits retain their own local exclusions. Keep personal/private conversations out of public engineering sources.
- **Deduplicate by goal and owner:** search owner open/closed issues, PRs, existing Linear and Notion source before new issue creation; reuse/update when a ticket already represents the same independently verifiable acceptance. When a major feature has distinct owner implementations, file scoped child tickets with a parent link; keep QA as the executable task authority after actual typed upsert/read-back.
- **Revenue-led prioritization:** retain P0 eligible Content clip account/post/marketplace and Times+Deals publication proof, P1 actual paid Studios services and editorials, and P2/P3 later platform enhancements/research. Approval to capture the whole backlog must not create a 200-ticket artificial P0 queue or alter real deployed-state truth.

## 3. Work item fields

An engineering issue has its repo/owner/module, kind, source and decision pointers, launch lane, priority (P0–P3), dependencies, authorization, acceptance criteria, source SHA, PRs and CI receipts. A QA task additionally has its own stable ID, parent/child execution graph, lease/checkpoint/retry state, acceptance and Human Verify. Do not invent QA IDs or reflect mutable QA status in issue-body checkboxes.

INBOX/READY/IN_PROGRESS/REVIEW/VERIFY/DONE, plus BLOCKED/ACTION_REQUIRED/DEFERRED, are human-facing projections of actual QA task state when mapped. GitHub open/closed owns issue closure only; Linear planning state is separate. QA acceptance requires current evidence and Human Verify is independent. If a typed QA registration is not accessible, explicitly record PENDING_QA_API instead of fabricating a task ID, claim or status. A GitHub Project, if installed, must not introduce a competing editable status.

Suggested role-based QA/operational projections: **Launch & Revenue**, **Next & Ready**, **Blocked / Needs Action**, **Active Agent Work**, **By Owner Repository**, **Awaiting Verification**, **Deferred/Research**. Reuse existing QA/Web rather than building another status dashboard.

## 4. Intake and deduplication

1. Capture the original request and classify accepted, research, revoked, personal-private and implementation-ready decisions. Find and update the **existing owner document types** with provenance; identify true engineering requirements and owner/module, source SHA and dependencies.
2. Search **open and closed** issues and linked PRs in that owner and adjacent authority repos. Identify EXACT_MATCH / OVERLAP_REVIEW / NEW / HISTORICAL / VERIFIED_DONE. An approximate title match is review evidence, not permission to create a duplicate.
3. For a NEW item, create the issue in its implementation owner's repo with constraints, an acceptance checklist, source link, stable source provenance and no claims of running code. For an exact existing match, link it; ambiguous overlaps remain pending triage.
4. For repeated runs, use a stable source key / issue link and a read-before-create, commit-after-write journal. Dry-run output precedes mutation, with idempotent retry, permission checks, rate-limit awareness, crash recovery, and conflict detection.
5. An authorized Tavall AI supervisor chooses READY/approved QA work and delegates to provider-native harnesses. Only typed QA handlers mutate task state/leases/evidence, and authorized GitHub actors mutate engineering issue state. Human approval remains distinct for external publishing, contracts, provider accounts, payments, advertising and deployment.

Migration provenance `source_commit + source_line` links in first-wave issues identify the immutable historical document; the bot must also derive a **content fingerprint** independent of mutable line numbers and reuse an already linked canonical Issue URL.

## 5. Completion and evidence

An issue is **not** complete merely because a PR was merged. Completion requires the acceptance claimed by that issue: typed contracts, exact accepted SHA, test/CI outcome, consumer integration, operational rollout, and human verification when the scope calls for them. Explicitly distinguish `SOURCE_MERGED`, `SOURCE_VALIDATED`, `DELIVERED`, and `RUNTIME_VERIFIED` evidence. Do not require production deployment for docs-only work or static tools that have no runtime. Stale heads, missing CI evidence, partial accepted branches, and unreadable host state cannot silently transition to DONE. Rollback may reopen affected acceptance if authorized and demonstrably regressed.

## 6. Migration and projection cutover

**Current baseline:** [legacy global ledger](../../TODO.md) at snapshot `7022d23f9be07ddd7fd0539ae9e928a0550e1f9a` contains 150 unchecked and 2 checked tasks across 55 repository sections. The GitHub open-issue search returned 63 issues, including potential overlaps; this is a discovery snapshot, not an exhaustive dedup verdict.

During migration:
- The old `TODO.md` remains an immutable-provenance-compatible transitional ledger for items without issues. The **14 items linked to migrated issues** are now tracked by those issues, not by editing their checkbox state. See [migration inventory](../progression/TAVALL_WORK_GRAPH_LEGACY_TODO_MIGRATION_20261022.md).
- The prior [TODO Static Projections](TODO_STATIC_PROJECTIONS.md) contract and root repository files remain v1 until the new generator actually passes owner-repository pilot tests. Do **not** swap the authoritative source preemptively.
- Subsequent batches triage duplicate, stale, already completed and deferred entries **before** creating Issues. Older out-of-scope/Hytale work is not migrated in this user-approved batch.
- Verify one GitHub Issue source mapping per task, no lost requirements, no missing repositories, retained historical links and stable duplicate-safe repeat runs.
- After complete audited mapping, preserve/archive the legacy document and change root `TODO.md` into a **generated, read-only view** of GitHub Issues with canonical URLs, deterministic metadata and no feedback loop. Keep the legacy Git history intact.
- GitHub Projects remains optional and requires scoped integration/real read-back; do not maintain a second writable workflow status alongside QA/Linear. Existing QA↔GitHub/Linear/Notion synchronization also requires live typed API evidence before claiming it works.

## 7. Implementation and proof

Owning [initiative #9](https://github.com/TavallStudios/tavall-github-bot/issues/9) has implementation slices: [ingestion/dedup #10](https://github.com/TavallStudios/tavall-github-bot/issues/10), [PR/CI and completion evidence #11](https://github.com/TavallStudios/tavall-github-bot/issues/11), [projections + full migration #12](https://github.com/TavallStudios/tavall-github-bot/issues/12), [org Project views #13](https://github.com/TavallStudios/tavall-github-bot/issues/13).

Tavall GitHub Bot remains a GitHub integration adapter, and Tavall CI/Cloud remain the only CI and execution authorities. Module naming, DI and testing follow [Module Separation](code-architecture/MODULE_SEPARATION.md) and `Tavall AI`/`tavall-engineering-policy`. Each production implementation PR requires source-backed unit/integration acceptance, read-after-write evidence, projection idempotence and a correct unprivileged failure mode. No GitHub Actions execution bridge or second work scheduler.

**Evidence boundary as of 2026-11-04:** owner Issues, QA modules, provider harness code and technical drafts exist, but end-to-end Bot/QA/Linear/Notion sync, generated TODO replacement and actual GitHub Projects integration are **not verified by this policy update**. The October 22 inventory above is a historical migration snapshot.

## 8. Founder launch and finance priorities (November 4, 2026)

**Purpose:** deliver immediate publicly useful outcomes and reconcile real revenue from ventures Tavall can operate now, using existing infrastructure and explicit permissions. This is a prioritization decision, not authorization to spend, publish without rights, sign contracts, mint tokens or deploy without owner grants. Canonical planning: [Portfolio Operating Charter](https://app.notion.com/p/40738458ddfd81e080bcefc92a8c1105) and [Marketing Revenue Portfolio](https://app.notion.com/p/40b38458ddfd81d5bbcccf85c07fe8e8).

| Focus / priority | Owner issues and unblock path | Real acceptance |
| --- | --- | --- |
| **P0 NOW: clipping income** | [Content accounts #76](https://github.com/TavallStudios/tavall-content/issues/76), [marketplace submissions #59](https://github.com/TavallStudios/tavall-content/issues/59), [Content campaigns #80](https://github.com/TavallStudios/tavall-content/issues/80), existing publisher queues and Analytics; support permitted manual operating path until automation verified | Rights/brief compliant source and edit, verified post ID, qualified campaign submission, evidence of approval and **separately** settled/withdrawable/received cash. Prior dashboard-approved $3.37 is not bank receipt. |
| **P0 NOW: Tavall Times + Deals/Hot Releases** | [Blog #10](https://github.com/TavallStudios/tavall-web-blog/issues/10), [Web #101](https://github.com/TavallStudios/tavall-web/issues/101), [Affiliate #2](https://github.com/TavallStudios/tavall-affiliates/issues/2), [Web affiliate #2](https://github.com/TavallStudios/tavall-web-affiliates/issues/2), [Content #78](https://github.com/TavallStudios/tavall-content/issues/78) | Verified public article and shared /deals /releases nav, currently eligible Impact offers and disclosures, honest empty/expired states, measured clicks/purchases; newsletter at article end; **AdSense not a blocker**. |
| **P1 NEXT: TavallTech original tech/news/Deal Watch** | [Channel registry #81](https://github.com/TavallStudios/tavall-content/issues/81), Content account #76 and current channel DESIGN/Content Studio | Real authorized X/Instagram/TikTok links where supported, sourced useful articles/posts, measured affiliate response. No invented profiles. |
| **P1 NEXT: sell already-built outcomes** | [Studios PRODUCT](https://app.notion.com/p/40938458ddfd8120922cf24b89396940), [AI Product Agent #89](https://github.com/TavallStudios/tavall-ai/issues/89), [Docs strategy #98](https://github.com/TavallStudios/tavall-docs/issues/98), Workflows/Studio existing offers | Validate 1–3 narrow done-for-you research/monitoring/integration/maintenance or licensed software offers; genuine user demand and actual Tavall Pay/Commerce settlement. Do not require new Tavall AI Chat platform. |
| **Support only as blockers: CI/Cloud/QA/Analytics** | CI/Cloud/QA owners and [GitHub Bot #16](https://github.com/TavallStudios/tavall-github-bot/issues/16) | Source-pinned tests, authorized deployment, correct metrics/permission reconciliation; no hypothetical perfect automation as launch prerequisite. |
| **P2/P3 RESEARCH** | Execution-native model, RSI, AR, Cloud Phone, token design, paid ad automation and speculative new services | Research and independent authorization only; do not block near-term launches. |

Allocate a bounded **flagship Content shipping lane**, **Times/tech publication and revenue lane**, and **critical reliability lane**. Keep non-blocking research tracked but parked; no new perpetual infrastructure dependency before first paid outcome. Track **gross offered, eligible, pending, approved, invoiced, settled, withdrawn/received, fees, operating cost and net contribution** independently; a launch, impression or approved clip is not cash.

## 9. Acceptance / next implementation gate

- [ ] Merge this policy with the already-open Work Graph TECHNICAL DESIGN PR #95 after reviewing source/API differences; do not invent QA upsert APIs or automatically cancel external tasks.
- [ ] Reconcile existing Notion and GitHub PRODUCT/DESIGN/TECHNICAL/PROGRESSION/MARKETING and update the correct owner issue without creating a standalone chat-backfill Notion page.
- [ ] Verify each launch's real release blocker and QA mapping before P0 work starts. Source merge, tests, production route, provider post, campaign approval, actual received money and HUMAN_VERIFIED are distinct.
- [ ] Preserve private personal reminders/health/legal material in existing private Notion/automation authorities only, never the public Work Graph.
## DOC TODO:

### Document next steps
- [ ] Link the accepted Bot producer TECHNICAL DESIGN and proof of idempotent migration.
- [ ] Retire the v1 projection contract only after real v2 generator and Project integration acceptance.

### System next steps
- [ ] Finish audit of the remaining unmatched legacy items and accept/close their issue mappings.
- [ ] Validate a repeat-run-safe pilot and preserve a reversible backup before switching generated root TODOs.
