# Tavall Work Graph — Work Tracking Authority and Migration

> **Status:** ACTIVE TRANSITION / ISSUES PILOT  
> **Document Type:** Engineering operations policy and technical migration contract  
> **Authority:** Tavall Docs (policy); each GitHub Issue owns its own task state  
> **Execution owner:** [Tavall GitHub Bot](https://github.com/TavallStudios/tavall-github-bot/issues/9)  
> **Date:** 2026-10-22

## 1. Decision and non-goals

**Canonical execution work lives in GitHub Issues belonging to the actual owning repository.** Use one TavallStudios organization-wide GitHub Projects board as a cross-repository **view and workflow field**, never as an alternate task store. Tavall Docs and Notion remain design, policy, PROGRESSION and deployment-document authorities, not copies of task status. PRs implement work and Tavall CI provides immutable validation evidence. Tavall AI ledger records active agent execution/locks rather than a second TODO catalog.

This does not introduce a new task database, a replacement GitHub App, a new Tavall Cloud scheduler, an agent framework, or a source-of-truth in the Web/QA UI. Existing QA and Web views consume read-only task/evidence projections when later authorized.

## 2. Ownership graph

```text
Human / Agent proposal
   -> Tavall GitHub Bot (authorized intake, GitHub discovery, dedup, links)
   -> Canonical owner-repository GitHub Issue
         -> Optional GitHub Projects board row (status and filtered views)
         -> Linked sub-issues and explicitly typed blockers
         -> Linked implementation PR(s) / review decisions
         -> Exact Tavall CI check/evidence
         -> Runtime/deployment acceptance only where applicable
   -> Bot-generated read-only TODO.md and agent/QA views
```

The **repository issue URL** is the canonical task identity. Project item IDs, bot state keys, task titles, README bullets, PR numbers and AI ledger execution IDs are not a second task authority. A cross-repo initiative chooses one primary owning repository and links the actual child-owner issues; do not move domain ownership to the parent initiative.

## 3. Work item fields

A task has: issue URL, owning repository and module/system, kind (initiative / actionable task / bug / verification), priority (P0–P3), dependencies and blocked reason, required consumer / approval, acceptance tests, design authority links, implementation PR(s), verification evidence / accepted SHA, and source provenance.

Workflow values: `INBOX → READY → IN_PROGRESS → REVIEW → VERIFY → DONE` plus `BLOCKED` and `DEFERRED`. The GitHub Projects **Status** custom field is the intended workflow projection once the board is installed. Until then, newly imported issues are triage-only INBOX unless separately supported by work evidence. Issue `open/closed` (including GitHub's `not_planned`/`duplicate` reason) is the native closure authority; `DONE` requires the issue's acceptance criteria, not merely an updated Project field. Do not maintain mutable status simultaneously in TODO text, an issue body, a bot file, and a Project field.

Suggested board views: **Next & Ready**, **Blocked**, **Active Agent Work**, **By System/Repository**, **Awaiting Verification**, **Deferred**. Use existing GitHub capabilities rather than building a separate visual dashboard in the first phase.

## 4. Intake and deduplication

1. Recover owning repo/module and the accepted Tavall contract. Classify the smallest actionable task or parent initiative, and identify original request, source SHA, and supporting docs.
2. Search **open and closed** issues and linked PRs in that owner and adjacent authority repos. Identify EXACT_MATCH / OVERLAP_REVIEW / NEW / HISTORICAL / VERIFIED_DONE. An approximate title match is review evidence, not permission to create a duplicate.
3. For a NEW item, create the issue in its implementation owner's repo with constraints, an acceptance checklist, source link, stable source provenance and no claims of running code. For an exact existing match, link it; ambiguous overlaps remain pending triage.
4. For repeated runs, use a stable source key / issue link and a read-before-create, commit-after-write journal. Dry-run output precedes mutation, with idempotent retry, permission checks, rate-limit awareness, crash recovery, and conflict detection.
5. Agents may propose work and record execution evidence. Only authorized bot/users mutate GitHub task state. Human approval continues to govern privileged product/publication/deployment actions.

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
- The GitHub Projects org-wide board requires a UI/operator or a correctly scoped integration because the currently available GitHub connector has no Projects mutation capability. The bot must not claim the board exists before a successful read-back.

## 7. Implementation and proof

Owning [initiative #9](https://github.com/TavallStudios/tavall-github-bot/issues/9) has implementation slices: [ingestion/dedup #10](https://github.com/TavallStudios/tavall-github-bot/issues/10), [PR/CI and completion evidence #11](https://github.com/TavallStudios/tavall-github-bot/issues/11), [projections + full migration #12](https://github.com/TavallStudios/tavall-github-bot/issues/12), [org Project views #13](https://github.com/TavallStudios/tavall-github-bot/issues/13).

Tavall GitHub Bot remains a GitHub integration adapter, and Tavall CI/Cloud remain the only CI and execution authorities. Module naming, DI and testing follow [Module Separation](code-architecture/MODULE_SEPARATION.md) and `Tavall AI`/`tavall-engineering-policy`. Each production implementation PR requires source-backed unit/integration acceptance, read-after-write evidence, projection idempotence and a correct unprivileged failure mode. No GitHub Actions execution bridge or second work scheduler.

**Implementation state, 2026-10-22:** Issue authority established for the first migration wave; bot-based ingestion, org-wide Project board, generated TODO replacement and runtime verification are **not deployed or verified**.

## DOC TODO:

### Document next steps
- [ ] Link the accepted Bot producer TECHNICAL DESIGN and proof of idempotent migration.
- [ ] Retire the v1 projection contract only after real v2 generator and Project integration acceptance.

### System next steps
- [ ] Finish audit of the remaining unmatched legacy items and accept/close their issue mappings.
- [ ] Validate a repeat-run-safe pilot and preserve a reversible backup before switching generated root TODOs.
