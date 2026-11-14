# Tavall Work Graph — Work Tracking Authority and Migration

> **Status:** ACTIVE / ISSUE-DRIVEN WORK TRACKING<br>
> **Document Type:** Engineering operations policy and technical migration contract<br>
> **Authority:** Tavall Docs (policy); each owner-repository GitHub Issue is the origin for its task<br>
> **GitHub integration:** [`tavall-gh`](https://github.com/TavallStudios/tavall-cli/issues/9), the typed GitHub CLI wrapper registered in the Tavall CLI<br>
> **Date:** 2026-11-14

## 1. Decision and non-goals

**GitHub Issues in the actual owning repositories are the origin and canonical identity for work.** `tavall-gh` is the typed GitHub CLI wrapper registered in the Tavall CLI; it owns `gh` invocation, authentication, environment mapping, and error translation. People and authorized Tavall tools use it for GitHub operations. GitHub issues feed the QA Task Board, which is the aggregate execution surface across Tavall tools for assignments, runs, checkpoints, evidence, review, and acceptance. The board does not replace issue identity, title-based Type, explicit Priority, or native open/closed state. Tavall Docs and Notion remain design, policy, PROGRESSION and deployment-document authorities. PRs implement work and Tavall CI provides immutable validation evidence.

This does not introduce a new task database, a replacement GitHub App, a new Tavall Cloud scheduler, an agent framework, or a second task origin. The Tavall GitHub Bot is retired. `tavall-gh` is a typed CLI wrapper, not a bot, issue ledger, scheduler, task owner, or QA Task Board implementation.

## 2. Ownership graph

```text
Human / Agent proposal
   -> Tavall CLI / authorized Tavall tool
   -> tavall-gh (typed official GitHub CLI invocation)
   -> Canonical owner-repository GitHub Issue
         -> QA Task Board (aggregate assignments, runs, checkpoints, evidence, review, acceptance)
         -> Linked sub-issues and explicitly typed blockers
         -> Linked implementation PR(s) / review decisions
         -> Exact Tavall CI check/evidence
         -> Runtime/deployment acceptance only where applicable
```

The **repository issue URL** is the canonical task identity and origin. QA Task Board records are keyed to that issue and aggregate execution evidence; they do not create a second task identity. Project item IDs, wrapper invocations, task titles, README bullets, PR numbers and AI ledger execution IDs are not task origins. A cross-repo initiative chooses one primary owning repository and links the actual child-owner issues; do not move domain ownership to the parent initiative.

## 3. Work item fields

A task has: issue URL, owning repository and module/system, kind (initiative / actionable task / bug / verification), priority (P0–P6), dependencies and blocked reason, required consumer / approval, acceptance tests, design authority links, implementation PR(s), verification evidence / accepted SHA, and source provenance.

QA Task Board statuses describe execution and acceptance (for example `ACTIVE`, `BLOCKED`, and `REVIEW`); the owning GitHub issue's open/closed state remains the task closure authority. The board is updated from issue identity and linked work evidence. Do not maintain competing workflow state in TODO text, an issue body, or a Bot-owned file.

The QA Task Board provides the aggregate execution view across Tavall tools. Keep its task keyed by the owner-repository issue URL and use its assignments, runs, checkpoints, evidence, review, and acceptance fields for execution tracking.

## 4. GitHub Issue Types and Priority

GitHub issues are the canonical work-item identity and title prefixes remain the human-readable classification source. TavallStudios also configures native GitHub Issue Types and a single-select Priority field; the issue write path synchronizes those fields from the issue's own title, labels, and body. The QA Task Board is an execution/checkpoint tracking surface, not the source for issue Type or Priority.

### Issue Types

The title prefix determines native **Type**. Normalize known prefixes to the existing organization types:

- `TODO` → `TODO`; `BUG` → `Bug`; `RESEARCH` → `Research`.
- `Test` / `Tests` and `Validation` → `Tests`.
- `arch(consumer)` / `Architecture` → `Architecture`.
- `Docs` / `Documentation` → `Documentation`.
- `Deploy`, `Build`, `Cloud operation`, `Cloud live logs`, `Cloud live read`, and `Cloud read` → `Infrastructure`.
- `Build tavall-content-auto-account-system` → `Feature`.
- Other exact canonical type names retain their corresponding type (including `Task`, `Feature`, `Idea`, `Epic`, `Migration`, `Security`, `Design`, and `Incident`).

`V0` and `Closed` are version/state markers, not types. Unrecognized or absent prefixes leave native Type unset; do not invent types from arbitrary title text. `Test` is retained as an existing legacy org type, while new `Test` / `Tests` title prefixes normalize to `Tests`.

### Priority

The organization Priority field is a single-select with `P0` through `P6`. Existing option identities were remapped as `Urgent → P0`, `High → P1`, `Medium → P2`, and `Low → P3`:

- **P0** — critical and immediate; blocks launch or safety and must be resolved now.
- **P1** — required for the current goal or milestone.
- **P2** — scheduled work that is not blocking.
- **P3** — normal backlog work.
- **P4** — lower-priority backlog work.
- **P5** — deferred work.
- **P6** — someday work; the lowest priority.

Priority is sourced only from a P0–P6 marker already present in an issue label or body. A single explicit priority label takes precedence over body markers. If the selected source has conflicting markers, leave Priority unset and report the conflict. With no marker, leave Priority unset. Do not infer priority from a title, QA Task Board value, Notion priority, or issue type.

### Creating and updating issues

After a successful GitHub issue create or edit through `tavall-gh`, the owning issue workflow synchronizes native Type from the current title prefix and Priority from existing labels/body markers. It clears stale values when no recognized type or priority exists. The paced open-issue backfill follows the same rules. This issue-classification policy belongs to the workflow; `tavall-gh` owns typed CLI invocation and result translation. Never source issue metadata from the QA Task Board client.

The 2026-11-09 title-prefix review in `docs/progression/GITHUB_ISSUE_TYPE_REVIEW_20261108.json` was a classification-only inventory; its report that existing native values were not modified describes that historical review, not the subsequent metadata sync. The owner-authorized metadata backfill later examined 222 open issues, updated 2, found 220 already current, and encountered 0 errors.

### Authority and consumer

Each owner-repository GitHub Issue is the canonical work-item identity and source for its title-based Type and explicit Priority markers. The QA Task Board may track execution and verification checkpoints; it does not populate or override GitHub issue metadata. The retired JSON Agent Ledger is not a task source.

## 5. Intake and deduplication

1. Recover owning repo/module and the accepted Tavall contract. Classify the smallest actionable task or parent initiative, and identify original request, source SHA, and supporting docs.
2. Search **open and closed** issues and linked PRs in that owner and adjacent authority repos. Identify EXACT_MATCH / OVERLAP_REVIEW / NEW / HISTORICAL / VERIFIED_DONE. An approximate title match is review evidence, not permission to create a duplicate.
3. For a NEW item, create the issue in its implementation owner's repo with constraints, an acceptance checklist, source link, stable source provenance and no claims of running code. For an exact existing match, link it; ambiguous overlaps remain pending triage.
4. For repeated runs, use a stable source key / issue link and a read-before-create, commit-after-write journal. Dry-run output precedes mutation, with idempotent retry, permission checks, rate-limit awareness, crash recovery, and conflict detection.
5. Authorized users and Tavall tools perform GitHub issue operations through `tavall-gh`; authorization remains enforced by the configured GitHub identity and repository permissions. Agents may propose work and record execution evidence. Human approval continues to govern privileged product/publication/deployment actions.

Migration provenance `source_commit + source_line` links in first-wave issues identify the immutable historical document. Reuse an already linked canonical Issue URL and retain source provenance when revisiting historical migration records.

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
- Issue intake and current execution tracking use owner-repository GitHub Issues and the QA Task Board. The retired GitHub Bot's planned generated TODO and GitHub Projects automation are not delivered by `tavall-gh`; the wrapper only provides typed GitHub CLI invocation and translation.

## 8. Implementation and proof

The former Bot initiative and slices ([#9](https://github.com/TavallStudios/tavall-github-bot/issues/9), [#10](https://github.com/TavallStudios/tavall-github-bot/issues/10), [#11](https://github.com/TavallStudios/tavall-github-bot/issues/11), [#12](https://github.com/TavallStudios/tavall-github-bot/issues/12), and [#13](https://github.com/TavallStudios/tavall-github-bot/issues/13)) are superseded by direct GitHub CLI use through [`tavall-gh`](https://github.com/TavallStudios/tavall-cli/issues/9) and issue-driven intake. Preserve the old issue links as migration history; they no longer own execution.

`tavall-gh` owns only typed GitHub CLI invocation, authentication, environment mapping, and error translation. Tavall CI and Cloud remain the CI and execution authorities; the QA Task Board aggregates execution tracking across Tavall tools. Module naming, DI and testing follow [Module Separation](code-architecture/MODULE_SEPARATION.md) and `Tavall AI`/`tavall-engineering-policy`. No GitHub Actions execution bridge or second work scheduler.

**Historical implementation checkpoint, 2026-11-07:** Organization-wide backlog intake completed across all 50+ repositories; 206 open engineering issues were cataloged and triaged in `BACKLOG.md`. Manual unchecked TODO tracking was formally retired. This checkpoint predates the issue-driven QA Task Board execution flow.

**Current decision, 2026-11-14:** The Tavall GitHub Bot is retired. GitHub Issues remain the ledger origin and feed the QA Task Board; direct GitHub CLI operations use `tavall-gh`. The former Bot issues #9–#13 are to be closed as superseded after this documentation change merges.

## DOC TODO:

### Document next steps
- [ ] Reconcile or archive the historical Bot-owned TODO projection contract so it cannot be mistaken for an active automation owner.
- [ ] Track any future projection work from an owner-repository GitHub Issue and its linked QA Task Board task.

### System next steps
- [ ] Finish audit of the remaining unmatched legacy items and accept/close their issue mappings.
- [ ] Validate a repeat-run-safe pilot and preserve a reversible backup before switching generated root TODOs.

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | 2026-11-14 3:47 PM PST | This change is pending PR; branch `working/docbot-retire-github-bot-20261114`. |
| Notion | `UPDATED_PENDING_NOTION_SYNC` | No matching 1:1 twin identified by search | 2026-11-14 3:47 PM PST | Sync applicability remains unresolved; search did not identify a matching page. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-08 11:13 PM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | [Draft PR #115](https://github.com/TavallStudios/tavall-docs/pull/115) | Added initial P0–P6 guidance; superseded by the corrected source mapping below. |
| 2026-11-08 11:59 PM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | [Draft PR #115](https://github.com/TavallStudios/tavall-docs/pull/115) | Previous revision still used QA task metadata; corrected by the next event. |
| 2026-11-09 12:01 AM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | [Draft PR #115](https://github.com/TavallStudios/tavall-docs/pull/115) | GitHub title prefixes supply Type; labels/body supply Priority; no QA-derived classification. |
| 2026-11-09 12:04 AM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | [Draft PR #115](https://github.com/TavallStudios/tavall-docs/pull/115) | Reconciled docs and implementation source with the GitHub issue owner correction. |
| 2026-11-09 12:51 AM PST | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | [Staging PR #108](https://github.com/TavallStudios/tavall-docs/pull/108) | Reconciled concurrent main policy with the owner directive: native Type follows GitHub title prefix; Priority comes only from explicit issue labels/body markers. |
| 2026-11-14 3:47 PM PST | GitHub | `UPDATED_PENDING_NOTION_SYNC` | `TavallStudios/tavall-docs/docs/quality/WORK_TRACKING.md` | Same path | Branch `working/docbot-retire-github-bot-20261114`; PR pending. | Retired Bot ownership, made issue-driven intake and QA Task Board execution explicit, and linked the `tavall-gh` intake issue. Notion twin search found no matching page; sync applicability is recorded for follow-up. |

</details>
