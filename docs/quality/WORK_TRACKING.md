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

## 4. GitHub Issue Types and Priority

The TavallStudios organization defines native GitHub Issue **Types** and a native org **Priority** field. These are the canonical classification dimensions for every owner-repository issue. They supersede ad-hoc kind/priority labels and replace the JSON agent ledger as a task source (see §2 and §3). **A missing native type is `UNCLASSIFIED`, not implicitly `TODO`, `Task`, or `Other`; type assignment is not yet complete across the organization.**

### Issue Types

- **Task** — a single bounded, actionable unit of work.
- **Bug** — a defect or incorrect behavior to fix.
- **Feature** — a bounded new capability implemented through FEATURE PRs; relates to PR Type FEATURE / DEVELOPMENT_STAGING / RUNTIME / STAGING.
- **TODO** — a lightweight loose reminder or follow-up, not yet promoted to a planned Task.
- **Idea** — a proposal or suggestion; never auto-converted into a Task until explicitly accepted.
- **Epic** — a Notion goal/milestone parent that groups child sub-issues.
- **Migration** — a move, port, or cutover of code, data, or ownership.
- **Infrastructure** — platform, build, CI, or operational-environment work.
- **Test** — test coverage, harness, or verification work.
- **Documentation** — docs, standards, or authored reference content.
- **Security** — vulnerability, hardening, or compliance work.
- **Research** — investigation, spike, or evaluation without a committed deliverable.
- **Design** — product, UX, or technical design artifact.
- **Incident** — an active or post-mortem production/service disruption.

### Issue title prefixes and TODO promotion

All newly created or materially retitled Tavall Issues must use **one uppercase type prefix followed by `: `**. Titles are a searchable human/agent projection; the native GitHub Issue **Type** is the classification authority. Never infer a type from a prefix alone or use a label as a substitute when the native field is available.

| Native Issue Type | Required title prefix | Meaning |
| --- | --- | --- |
| TODO | `TODO:` | Captured follow-up or loose reminder; owner/acceptance/scheduling may be incomplete. |
| Task | `TASK:` | Accepted, bounded actionable work with an owner and testable completion conditions. |
| Bug | `BUG:` | Confirmed incorrect behavior, with reproduction and expected behavior where possible. |
| Feature | `FEATURE:` | Accepted new user/system capability. |
| Idea | `IDEA:` | Unaccepted proposal; does not imply implementation authorization. |
| Epic | `EPIC:` | Parent outcome coordinating linked child issues. |
| Migration | `MIGRATION:` | Governed cutover or ownership/data/code migration. |
| Infrastructure | `INFRA:` | Infrastructure, CI, deployment, or operational platform work. |
| Test | `TEST:` | Tests, simulations, test harnesses, or verification. |
| Documentation | `DOCS:` | Documentation, policy, templates, and reference material. |
| Security | `SECURITY:` | Security hardening, vulnerabilities, or compliance controls. |
| Research | `RESEARCH:` | Investigation or experiment, with uncertainty and evidence as the deliverable. |
| Design | `DESIGN:` | UX, product, architectural, or technical design deliverable. |
| Incident | `INCIDENT:` | Production disruption, impact, mitigation, or postmortem. |

**Other/unknown:** Reserve `OTHER:` only as an explicit short-lived triage fallback when no existing Type applies. Use the native **Other** type *only if it is actually configured in the organization*; otherwise leave the native type unassigned, record `NEEDS_TYPE_TRIAGE` and the reason, and never claim the issue was typed. Prefer an existing type over adding a catch-all. Do not treat `OTHER` as a generic TODO.

- Choose the **primary intent**, not every activity inside an issue. A `BUG:` issue can require tests; a `FEATURE:` issue can contain implementation checklists. Those are not automatically separate `TASK:` or `TEST:` issues.
- Use `TODO:` when a follow-up is worth retaining but **not yet approved/scoped**; use `TASK:` when the work is accepted and the owner, result, and acceptance evidence are known. Promote by updating the **same issue** (native type, title prefix, body, status/priority as warranted), preserving issue number, discussion, and links. Do not silently turn `IDEA:` or `RESEARCH:` into committed work.
- Before creating/updating, deduplicate against open/closed issues and linked PRs; read back both **native type** and **title prefix** after mutation. If the client cannot write native Issue Types, record the blocker and leave the item pending rather than misreporting success. Never create duplicate issues merely to change type.
- Use exactly one prefix, not `TODO: TASK:` or new stacked prefixes. Existing PR title/branch conventions are separate and unchanged.
- **Historical rollout:** inventory native types and titles first; review untyped or mismatched issues per owner repository in reversible batches. Preserve identity/acceptance, do not mass-rename all existing issues without a verified mapping, and do not claim the prefix policy has already retroactively classified the backlog.
- Search/report separately for **unclassified**, **TODO**, **planned actionable**, **research/ideas**, and **closed**. `open` is a status, not synonymous with `TODO`.

Examples: `TODO: Audit current blog attribution configuration`, `TASK: Add verified footer links to live hosts`, `BUG: Fix OAuth redirect loop`, `RESEARCH: Evaluate credential-safe browser import`.

### Priority

The native org **Priority** field carries `Urgent / High / Medium / Low`, derived from launch directives and Notion goals:

- **P0 → Urgent** — resolve immediately; blocks launch or safety.
- **P1 → High** — required for the current goal/milestone.
- **P2 → Medium** — scheduled but not blocking.
- **P3 / none → Low** — backlog, nice-to-have, or deferred.

### Authority and consumer

GitHub Issues feed the QA Task Board; **QA remains the task authority** and `qa.tavall.org` is unchanged. The JSON agent ledger is **retired as a task source** — issues, not ledger entries, are now the canonical task identity.

## 5. Intake and deduplication

1. Recover owning repo/module and the accepted Tavall contract. Classify the smallest actionable task or parent initiative, and identify original request, source SHA, and supporting docs.
2. Search **open and closed** issues and linked PRs in that owner and adjacent authority repos. Identify EXACT_MATCH / OVERLAP_REVIEW / NEW / HISTORICAL / VERIFIED_DONE. An approximate title match is review evidence, not permission to create a duplicate.
3. For a NEW item, create the issue in its implementation owner's repo with constraints, an acceptance checklist, source link, stable source provenance and no claims of running code. For an exact existing match, link it; ambiguous overlaps remain pending triage.
4. For repeated runs, use a stable source key / issue link and a read-before-create, commit-after-write journal. Dry-run output precedes mutation, with idempotent retry, permission checks, rate-limit awareness, crash recovery, and conflict detection.
5. Agents may propose work and record execution evidence. Only authorized bot/users mutate GitHub task state. Human approval continues to govern privileged product/publication/deployment actions.

Migration provenance `source_commit + source_line` links in first-wave issues identify the immutable historical document; the bot must also derive a **content fingerprint** independent of mutable line numbers and reuse an already linked canonical Issue URL.

## 6. Completion and evidence

An issue is **not** complete merely because a PR was merged. Completion requires the acceptance claimed by that issue: typed contracts, exact accepted SHA, test/CI outcome, consumer integration, operational rollout, and human verification when the scope calls for them. Explicitly distinguish `SOURCE_MERGED`, `SOURCE_VALIDATED`, `DELIVERED`, and `RUNTIME_VERIFIED` evidence. Do not require production deployment for docs-only work or static tools that have no runtime. Stale heads, missing CI evidence, partial accepted branches, and unreadable host state cannot silently transition to DONE. Rollback may reopen affected acceptance if authorized and demonstrably regressed.

## 7. Migration and projection cutover

**Current baseline:** [legacy global ledger](../../TODO.md) at snapshot `7022d23f9be07ddd7fd0539ae9e928a0550e1f9a` contains 150 unchecked and 2 checked tasks across 55 repository sections. The GitHub open-issue search returned 63 issues, including potential overlaps; this is a discovery snapshot, not an exhaustive dedup verdict.

During migration:
- The old `TODO.md` remains an immutable-provenance-compatible transitional ledger for items without issues. The **14 items linked to migrated issues** are now tracked by those issues, not by editing their checkbox state. See [migration inventory](../progression/TAVALL_WORK_GRAPH_LEGACY_TODO_MIGRATION_20261022.md).
- The prior [TODO Static Projections](TODO_STATIC_PROJECTIONS.md) contract and root repository files remain v1 until the new generator actually passes owner-repository pilot tests. Do **not** swap the authoritative source preemptively.
- Subsequent batches triage duplicate, stale, already completed and deferred entries **before** creating Issues. Older out-of-scope/Hytale work is not migrated in this user-approved batch.
- Verify one GitHub Issue source mapping per task, no lost requirements, no missing repositories, retained historical links and stable duplicate-safe repeat runs.
- After complete audited mapping, preserve/archive the legacy document and change root `TODO.md` into a **generated, read-only view** of GitHub Issues with canonical URLs, deterministic metadata and no feedback loop. Keep the legacy Git history intact.
- The GitHub Projects org-wide board requires a UI/operator or a correctly scoped integration because the currently available GitHub connector has no Projects mutation capability. The bot must not claim the board exists before a successful read-back.

## 8. Implementation and proof

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
