# Tavall Studios Code Review, Git Hygiene, and Engineering Issue Workflow

> **Status:** Active  
> **Applies to:** Contributors, maintainers, repository owners, automation, and AI-assisted development  
> **Purpose:** Protect production, preserve professional traceability, and keep engineering decisions understandable after their original context fades.

## 1. Applicability and precedence

This document owns shared Git review, PR topology, integration, and promotion policy for all Tavall and personal projects. Repository runbooks own deployment mechanics; this workflow does not redefine product architecture or claim implementation status.

Repository-specific files such as `AGENTS.md`, `CONTRIBUTING.md`, release procedures, synchronization contracts, staging manifests, and deployment runbooks may impose stricter requirements. Stricter repository-specific rules take precedence when they protect public source-of-truth history, automated synchronization, release integrity, security, or production safety.

A repository-specific supplement may not silently remove accountable review, truthful validation reporting, or production traceability. Any intentional exception must be explicit and attributable to an authorized maintainer or repository owner.

## 2. Core policy

GitHub is the authoritative record for repository review and active integration work.

A pull request is not merely a final merge request. For Tavall development, an open pull request is the durable GitHub-visible work surface for its remote branch: implementation, review history, dependency relationships, validation, agent handoff, and reconciliation all continue on that PR until its scope is merged, superseded, or intentionally abandoned.

There is no organization-wide limit on the number of open pull requests and no global rule that freezes creation of unrelated pull requests merely because reconciliation is active elsewhere. Large open-PR counts are normal for sufficiently active repositories. Coordination happens through accurate targets, stacking, dependency metadata, staging files, and reconciliation, not by serializing the entire organization behind one integration queue.

Ordinary contributor changes may not enter `main` without accountable review recorded on GitHub.

Accountable pull-request review uses one of two paths:

1. **Independent review**
   - The current change is presented through a GitHub pull request.
   - At least one qualified human other than the author approves the current diff.
   - Reviewable changes after approval require renewed approval.
2. **Owner self-promotion**
   - This path is limited to an authorized repository owner when they authored the pull request and no separate qualified reviewer is available.
   - The owner reviews the complete current diff and posts an **Owner Self-Review** record on the pull request.
   - The record names scope, validation, untested paths, risks, rollback, and the merge decision.
   - Reviewable changes after the record require a renewed Owner Self-Review.

Pull-request promotion requires configured checks to pass unless an authorized owner explicitly accepts an override, blocking conversations to be resolved, requested changes to be cleared, and the change to reach `main` through the GitHub merge flow.

GitHub does not allow an author to approve their own pull request. Owner self-promotion therefore uses a visible review record and, when required, repository-owner or ruleset-bypass merge control instead of fictional self-approval.

Automated reviews, AI reviews, status checks, comments, or reactions support review but satisfy neither independent human approval nor Owner Self-Review.

Authorized repository owners retain direct commit, push, force-push, check-bypass, and merge-bypass authority where repository-specific synchronization or protection rules do not impose a stricter path.

When an owner changes `main` directly:

- the pushed change should be surfaced for human review on GitHub by configured review automation when available;
- review may occur after the push but before the corresponding production deployment;
- the owner may explicitly override review when they accept responsibility for the change;
- the change must be reconciled into affected active pull-request branches, staging state, or synchronization branches;
- direct owner authority does not extend to ordinary contributors or automation merely because those actors have write access.

A commit reaching `main` does not automatically mean that a production service has been updated.

### Operational flows

Independent work:

```text
remote working branch <-> open PR
-> active Sub-Staging/Staging PR ancestry
-> exact-head integrated validation at every staging tier
-> accountable review
-> explicit repository/release staging promotion to main
-> manual production deployment
```

Stacked dependent work:

```text
PR A: architecture branch -> active Sub-Staging/Staging PR branch
PR B: behavior branch -> PR A branch
PR C: follow-up branch -> PR B branch

A merges
-> B rebases/retargets to the integration target
-> C continues on B until B merges
```

Parallel work:

```text
PR A ---------> integration target
PR B ---------> integration target
PR C ---------> integration target

staging file records intended composition, dependencies, validation, and conflicts
```

Owner-authored pull-request work follows the same graph but uses Owner Self-Review or independent human review for promotion.

Trusted owner direct work, when repository-specific rules permit it:

```text
owner push to main
-> GitHub human review of the pushed change
-> reconcile affected open PRs and staging state
-> manual production deployment
```

An authorized owner may explicitly override review when necessary. Deployment remains a separate decision.

## 3. Branch and integration model

The canonical model is PR-first rather than queue-first:

```text
working branch <-> pull request
        |            |
        |            +-> may target another PR branch when stacked
        |
        +-> active Sub-Staging PR (when used) -> active repository/release Staging PR -> main
```

A repository-specific contribution or synchronization workflow may use `working/**`, personal-fork branches, `sync/**`, `upstream/**`, `staging/**`, or another documented path while preserving the same review and production boundaries.

`main` is the authoritative production source. Deployment from `main` is manual unless another production document explicitly changes that behavior.

### 3.1 Working branches and pull-request branches

Ordinary changes begin on a focused remote branch such as:

```text
working/<short-description>
```

Examples:

```text
working/runtime-audit-recovery
working/docs-quality-foundation
working/release-validation
```

Once a pull request exists for that branch, treat the PR and its branch as one durable unit of work.

- Continue meaningful work on the existing PR branch instead of creating replacement PRs for the same scope.
- Push coherent commits to GitHub while work is in progress. Do not leave the authoritative or most useful state only in a local worktree or ephemeral agent sandbox.
- Keep the PR description, dependencies, validation, and linked issues current as the branch evolves.
- Draft status means the work is still active or not yet reviewable; it does not mean the branch is disposable.
- A PR may stay open across multiple implementation and reconciliation passes when it remains the correct work boundary.
- A large number of open PRs is not itself a workflow defect. Duplicate, stale, ownerless, contradictory, or misleading PRs are defects.

A working branch should contain one coherent feature, fix, refactor, documentation change, investigation outcome, or dependency layer. Split unrelated systems into separate branches, but do not fragment one coherent system merely to keep PR counts or diff sizes artificially low.

An authorized repository owner may work directly on `main` when another branch provides no meaningful review, integration, synchronization, or safety benefit and repository-specific rules permit it.

### 3.2 Staging state, staging files, and staging branches

Staging is persistent integration state represented by active Sub-Staging and Staging pull requests and their branches. Every active normal PR must reach this graph through its dependency ancestry. A staging file or manifest records composition and evidence; it does not substitute for an active integration PR.

- **Sub-Staging PRs** integrate a coherent domain, dependency stack, or subsystem and target the next active integration tier.
- **Repository/release Staging PRs** form the top-level integration and normal promotion boundary toward `main`.
- **Staging files or manifests**, when used, record intended composition, parent relationships, exact source heads, conflicts, validation, supersession, and promotion decisions. GitHub PRs remain the authoritative work surfaces.

Reuse the appropriate persistent integration PR rather than recreating it for each feature. Keep integration roots in Draft while they are continuously collecting or validating work; readiness for an authorized promotion is a separate transition. A green child does not authorize merging a persistent root into `main`.

Every active staging branch must have a corresponding active staging PR. Integration trees must remain coherent and independently testable. Superseded staging lines must identify their replacement, reconnect active descendants, and reconcile metadata before retirement. Do not leave closed roots with active dependents or retain competing active roots without an unambiguous scope boundary.

Normal focused PRs do not promote directly to `main`. Repository/release staging promotion receives the full accountable production review defined here. The narrow explicit owner and incident exceptions in Sections 3.4, 3.5, and 11 retain their authority; they are not a default path for contributors or automation.

#### PR work-graph metadata

Tavall PR metadata describes one recoverable work graph. It has three independent axes. Implementations, staging manifests, CONTROL projections, or automation MUST NOT collapse these axes into one status field.

**PR Type** describes structural location in the Git integration graph:

- `FEATURE`: bounded implementation, repair, test, migration, documentation, or product work;
- `SUB_STAGING`: persistent integration root for a bounded product, subsystem, or domain contained inside a broader runtime or staging graph;
- `RUNTIME`: persistent integration PR for a deployable or runtime boundary such as Paper, Velocity, Discord, Web, Agent, or Ingress;
- `STAGING`: top-level persistent composition/integration PR before production.

PR Type is explicit metadata. Branch naming may help a human locate work but MUST NOT be treated as sufficient evidence for type.

**PR State** describes human/agent lifecycle intent:

- `ACTIVE`: actively being worked or immediately resumable;
- `PAUSED`: intentionally preserved but temporarily stopped, including work interrupted by session/model limits, infrastructure failure, priority switching, or planned handoff;
- `BLOCKED`: unable to progress because of a concrete external dependency;
- `NEEDS_RECONCILIATION`: historical or migrated work whose intent, ownership, or relationships cannot yet be classified safely;
- `REVIEW_READY`: implementation is complete and awaiting review/checks;
- `MERGE_READY`: required review, validation, synchronization, and acceptance are satisfied;
- `MERGED`: successfully integrated into its parent;
- `SUPERSEDED`: intentionally replaced by another PR/source lineage and accompanied by a `supersededBy` relationship;
- `ABANDONED`: explicitly discontinued without a replacement.

`ACTIVE`, `PAUSED`, `BLOCKED`, and `NEEDS_RECONCILIATION` are protected lifecycle states for cleanup purposes. `ABANDONED` MUST NOT be inferred solely from age, inactivity, stopped executors, missing worktrees, closed/inactive GitHub state, or a temporary infrastructure failure. Ambiguous legacy work defaults to `NEEDS_RECONCILIATION`.

CONTROL coordination values such as `CANONICAL` and `SUPERSEDED` describe environment/domain coordination. They are not PR lifecycle states. A feature environment may be superseded at a broad domain while the PR remains `ACTIVE` or `PAUSED`.

**Execution Attachment State** describes current physical/runtime attachment independently of PR lifecycle:

- `LOGICAL_ONLY`: PR/source/lane/environment linkage exists but no current physical worktree exists;
- `MATERIALIZED_SYNCED`: a physical worktree exists and matches authoritative source identity;
- `MATERIALIZED_DIRTY`: a physical worktree contains local uncommitted work;
- `MATERIALIZED_STALE`: a physical worktree exists but local source differs from authoritative remote/CONTROL source;
- `ORPHANED_PHYSICAL`: a physical workspace exists without an authoritative CONTROL/PR owner;
- `ORPHANED_CONTROL`: CONTROL claims a physical attachment that cannot be located;
- `AMBIGUOUS`: conflicting potential owners or identities exist.

`LOGICAL_ONLY` is valid. Reconciliation MUST NOT create a worktree merely to make metadata symmetrical. `MATERIALIZED_DIRTY`, `MATERIALIZED_STALE`, `ORPHANED_PHYSICAL`, `ORPHANED_CONTROL`, and `AMBIGUOUS` are protected attachment states: automation MUST NOT reset, overwrite, relocate, condense, or delete them as cleanup.

##### Canonical source identity

The exact work identity tuple is:

```text
repository
+ branch
+ exact commit SHA
+ pull request
+ parent pull request
```

Directory names, historical path conventions, branch-name patterns, timestamps, or process liveness are evidence only. They are never authoritative identity.

A canonical PR metadata document may evolve in storage shape, but it must preserve at least:

```json
{
  "schemaVersion": "tavall-pr:v1",
  "repository": "TavallStudios/example",
  "pullRequest": 123,
  "type": "FEATURE",
  "state": "PAUSED",
  "stateDetail": "Paused after execution limit; safe to resume.",
  "source": {
    "branch": "working/example",
    "headSha": "..."
  },
  "relations": {
    "parentPullRequest": 100,
    "stagingPullRequest": 50,
    "runtimePullRequest": 100,
    "subStagingPullRequest": null,
    "supersededBy": null
  },
  "callbacks": {
    "canonicalLaneId": "...",
    "laneHistory": [],
    "currentEnvironmentId": "...",
    "environmentHistory": [],
    "executor": {
      "environmentId": "...",
      "lastJobId": null,
      "lastOperationId": null
    },
    "work": {
      "attachmentState": "MATERIALIZED_SYNCED",
      "workPath": "...",
      "backingWorkPath": "...",
      "localHeadSha": "...",
      "remoteHeadSha": "...",
      "dirty": false
    }
  },
  "resume": {
    "currentTask": "...",
    "nextAction": "...",
    "blockers": [],
    "reason": "SESSION_LIMIT"
  }
}
```

The example is semantic, not a frozen serialization contract. Implementations may normalize or split storage when the current architecture has a better ownership boundary, but they must preserve the three axes, exact identity, relationships, histories, resume intent, and cleanup safety.

##### Bidirectional callbacks and reconciliation

PR/source metadata, Tavall Cloud lanes, immutable environment generations, execution jobs/operations, and physical workspaces form one graph. Reconciliation must make ownership traversable in both directions rather than maintaining disconnected lists that happen to contain similar strings.

- PR metadata callbacks identify repository, branch, exact SHA, parent PR, staging/runtime/sub-staging owners, canonical lane, lane history, current environment, environment history, executor/job/operation evidence, and physical workspace when materialized.
- Lane metadata callbacks identify owning PR/source identities and environment generations.
- Environment metadata callbacks identify lane, PR, repository, branch, exact SHA, parent PR, and physical worktree when materialized.
- Workspace metadata callbacks identify owning PR, lane, environment, source identity, and executor evidence where appropriate.
- Executor/job/operation metadata callbacks identify the environment and PR/source identity that authorized execution.

Existing Tavall Cloud callback/index structures should be extended when they own these relationships; implementations should not create a parallel registry merely because migration data is untidy.

Reconciliation is metadata-first and non-destructive by default. It inventories authoritative GitHub PRs and branches, CONTROL lanes/environments, and physical shared worktrees; joins them by exact source identity; reads explicit PR lifecycle state; calculates attachment state; preserves lane/environment/executor history; updates safe callbacks; and emits conflicts as unresolved evidence. A dry-run/audit mode must exist before mutations that can affect physical state. Initial graph reconciliation MUST NOT perform mass deletion, condensation, reset, or relocation.

Age is not abandonment. `STOPPED` is not abandonment. No running executor is not abandonment. No physical worktree is not abandonment. Cleanup becomes eligible only after lifecycle intent is explicitly safe, protected attachment conditions are absent, source/history is preserved, and repository-specific retention rules permit it.

### 3.3 `main`

`main` is production and must normally:

- reject direct pushes from ordinary contributors;
- require pull requests for ordinary contributor changes;
- require independent approval or a current Owner Self-Review for pull-request changes;
- dismiss stale approvals after reviewable changes;
- require renewed accountable review after the latest reviewable push;
- require blocking conversations to be resolved;
- require configured checks unless an authorized owner records an override;
- block deletion and force pushes by ordinary contributors;
- restrict merges to trusted maintainers;
- preserve explicit owner bypass authority where stricter repository-specific rules do not prohibit it.

Direct owner changes should be surfaced for human review before the corresponding production deployment unless the owner explicitly overrides review.

### 3.4 Repository owner authority

Repository owner authority is determined by repository or organization access controls and is not enumerated in this public workflow.

When GitHub requires an explicit account or team for mechanical ownership, that assignment belongs in `.github/CODEOWNERS`, organization roles, repository permissions, ruleset bypass configuration, or an access-controlled operational record.

An authorized repository owner may, subject to stricter repository-specific synchronization rules:

- use Owner Self-Review for an authored pull request;
- merge an owner-authored pull request through an explicit ruleset bypass;
- commit or push directly to `main`;
- force-push shared branches when recovery or history repair genuinely requires it;
- bypass a failed or incomplete check while accepting the resulting risk;
- alter release scope;
- authorize production deployment.

Before rewriting shared history, an owner should, when practical, preserve the previous branch state, inspect the rewritten range, identify affected pull requests and branches, communicate the rewrite, and verify that contributors and automation can recover cleanly.

Owner authority exists to preserve operational control, not to force every owner action through ceremony that contributes no safety.

### 3.5 Hotfixes

A production hotfix should:

1. start from the current `main` state;
2. contain only the minimum safe correction;
3. use a pull request when that path remains useful and safe;
4. receive independent approval or Owner Self-Review when using a pull request;
5. run the checks available during the incident;
6. be reconciled into every affected open PR branch, staging state, or synchronization branch;
7. link an incident, blocker, or follow-up issue when work remains.

An authorized repository owner may apply the correction directly to `main` where repository-specific rules permit it. Urgency changes the size of the process, not whether engineering judgment exists.

## 4. Code review and pull-request flow

### PR Flow: mandatory active staging ancestry

Every active normal pull request MUST always have a valid transitive path into an active Sub-Staging or Staging PR, continuing through every Sub-Staging tier to one unambiguous active repository/release staging root. This includes feature, fix, architecture, infrastructure, agent, documentation, and dependency work, including Draft PRs and PRs that implement this policy. There is no staging-less grace period.

A valid path uses current open PRs, their actual base/head branches, and the repository's authoritative staging relationships. Branch naming, a body link, a historical merge, or stale manifest membership alone does not establish a valid path. A dependency child may target its parent's working branch; only the appropriate stack root needs direct staging attachment. Preserve dependency ordering and review boundaries rather than retargeting every child directly to staging.

For example:

```text
feature follow-up PR -> feature PR -> foundation PR
                     -> domain Sub-Staging PR
                     -> repository/release Staging PR -> main
```

The final edge to `main` identifies the authorized promotion boundary. It does not exempt intermediate Sub-Staging PRs from active upward ancestry or permit ordinary focused PRs to bypass staging.

#### Creation, update, and recovery

PR tooling and agents own resolving and validating staging ancestry as part of the PR operation. Humans must not need a second manual attachment ritual.

1. Resolve the authorized repository, existing same-scope PR, dependency parents, current exact heads, and correct active integration root before mutation. Reuse coherent existing work and reject conflicting active ownership or ambiguous staging destinations.
2. Ensure the correct persistent Draft integration PR and its upward ancestry first when missing, following repository authority. Do not create a replacement root merely because the existing root is inconvenient.
3. Create or update the focused PR and its staging membership as one recoverable workflow. Preserve the existing stack, record expected source and target heads, and fail closed if they change concurrently.
4. Re-read GitHub and authoritative staging state, verify the complete resulting ancestry and exact heads, and only then report success.

GitHub and staging storage are not one atomic database transaction. Tooling must persist operation identity, intended changes, completed effects, and a bounded retry or compensation plan before a multi-step mutation. Retries must resume idempotently without duplicate PRs or roots. A partial failure is incomplete and not accepted as a valid PR workflow; it must report the actual surviving PRs, branches, heads, and metadata, block integration/promotion, and repair or safely compensate immediately. Do not describe a partially created orphan as successful or leave it awaiting an unspecified future attachment pass. If recovery requires unavailable external authority, report that concrete blocker and retain durable recovery evidence.

Retarget, merge, close, rotate, supersede, and rebase operations must plan and preserve the ancestry of all affected descendants. Establish replacement ancestry before retiring a parent; revalidate after every transition. Never close a parent or delete a branch while active children still rely on it without completing their reconnection. Concurrent mutations require repository-scoped coordination and current-head guards rather than overwriting newer work.

#### Exact-head integration acceptance

Feature, Sub-Staging, and repository/release Staging validation must identify their exact current heads, composition, execution result, and evidence. A head or composition change invalidates prior acceptance for the changed integration state and affected higher tiers. Run relevant integrated build, architecture, regression, and runtime checks at every changed staging tier. Passing child tests do not replace testing the composed head, and intended membership must not be reported as integrated until the current integration tree actually contains the accepted work.

GitHub is SCM, review, checks, and reporting. Tavall/local execution remains the authoritative build, test, and runtime execution surface according to repository policy; GitHub-hosted Actions are not the primary execution infrastructure. Publish truthful evidence for the exact source that ran. Distinguish source failures from provider, infrastructure, timeout, termination, stale-head, and missing-evidence failures.

Topology validation must detect orphan normal PRs and stack roots, orphan Sub-Staging PRs, active staging branches without active staging PRs, cycles, incompatible or ambiguous roots, closed/superseded parents with active descendants, deleted PR references, stale metadata or head mismatches, incorrectly flattened dependency stacks, false integration membership, and stale acceptance. Ordinary PR creation and maintenance are valid only when these checks pass; explicitly authorized narrow exceptions remain attributable and reviewable under Section 11.

### 4.1 Before implementation

- Read `AGENTS.md`, this workflow, `CODE_ARCHITECTURE.md`, and relevant quality, design, progression, and operational documents.
- Search open and closed issues and pull requests for blockers, accepted directions, rejected approaches, overlapping work, and investigations.
- Inspect the existing implementation before proposing new classes or systems.
- Identify owning modules, expected tests, migration risk, failure behavior, rollback, and likely PR dependencies.
- Create or link an issue when the work crosses the issue threshold in Section 7.

### 4.2 During implementation

- Keep the change focused.
- Commit at meaningful working checkpoints.
- Push coherent checkpoints to the remote PR branch while work is ongoing.
- Avoid unrelated cleanup.
- Update linked issues and PR dependency metadata when evidence changes the direction.
- Keep tests and documentation with the behavior they explain.
- Treat generated code as untrusted until its APIs and behavior are verified.
- Extend established systems instead of creating parallel implementations.
- If new work depends on an unmerged PR, prefer an explicit stack over copying, reimplementing, or waiting solely to preserve a flat PR graph.

### 4.3 Before requesting review

The author must:

- review the complete diff;
- remove temporary logging, debug code, dead code, and accidental generated files;
- run relevant automated checks;
- perform required bot or manual verification;
- document untested paths honestly;
- synchronize with the target branch or parent PR and resolve obvious conflicts;
- update documentation and progression evidence when behavior changed;
- link issues accurately with `Closes #...`, `Fixes #...`, or `Refs #...`;
- identify stacked parents or children and any required merge order.

Use `Closes` or `Fixes` only when the pull request fully resolves the issue. Use `Refs` when the work contributes without completing it.

### 4.4 Pull requests are working branches

Treat pull requests as durable branches with review metadata attached, not as paperwork created only after implementation is complete.

#### Open-PR scale

Tavall repositories may have tens, hundreds, or eventually more open pull requests when development volume justifies it. Do not invent a low global PR-count ceiling and do not pause unrelated PR creation because another area is being reconciled.

Scale is managed by making each PR legible:

- clear scope and ownership;
- accurate base branch;
- explicit parent and child relationships for stacks;
- current validation status;
- linked issues and design decisions;
- valid transitive active staging ancestry and current composition metadata;
- supersession or conflict metadata when another PR changes its assumptions.

The goal is not a small PR list. The goal is a truthful dependency graph.

#### Existing PR reuse

If a PR already represents the intended scope, continue using it.

Do not create `v2`, `replacement`, `fixed`, or similarly redundant PRs merely because:

- the implementation needs substantial repair;
- architecture changed underneath it;
- another agent takes over the work;
- validation failed;
- the branch needs a rebase or retarget;
- the work spent time in draft state.

Create a new PR when there is a genuinely separate work boundary, a useful independent review boundary, a new stack layer, or the existing branch is intentionally abandoned or unrecoverable.

#### No global reconciliation freeze

Reconciliation does not impose an organization-wide new-PR freeze.

Before opening or extending a PR, inspect relevant active work. Then choose the correct relationship:

- **independent:** keep the PR parallel;
- **dependent:** stack it on the required parent PR;
- **overlapping:** reconcile shared code or scope explicitly;
- **superseded:** close or redirect the obsolete PR with an explanation;
- **same scope:** continue the existing PR instead of duplicating it.

A reconciliation process may temporarily block edits, retargeting, or promotion for the specific PRs it owns while rewriting or validating their relationship. That lock is local to the affected graph, not a global stop-the-world mutex for Tavall development. Civilization has suffered enough global locks already.

### 4.5 Stacked pull requests

Stacking is a first-class workflow, not an exception to apologize for.

Use a stack when one reviewable change logically depends on another unmerged change and waiting for the parent would unnecessarily serialize development.

A typical stack is:

```text
active Sub-Staging/Staging PR branch
└── PR A: architecture/foundation
    └── PR B: behavior using PR A
        └── PR C: follow-up or integration using PR B
```

Mechanically, the child PR targets the parent PR's branch. The PR body and staging state should name the relationship and expected merge order.

When a parent merges:

1. update the child branch from the parent's new destination;
2. retarget the child PR to the appropriate active parent or Sub-Staging/Staging PR branch, preserving its path to the repository/release staging root;
3. verify that the child diff now contains only its intended changes;
4. rerun affected validation;
5. update the staging file or dependency metadata;
6. continue using the same child PR.

Do not flatten a stack by duplicating parent commits into unrelated branches when Git ancestry can express the dependency directly.

Do not merge a child into its parent merely to make the graph disappear unless consolidation is intentionally the better review boundary.

#### Stacking examples

**Architecture before behavior**

```text
PR A: change the unified-JAR/module packaging boundary
PR B: FFA behavior work that must use the new runtime/package boundary

PR B targets PR A's branch.
```

The behavior PR should not continue implementing against an architecture already being replaced, and it should not duplicate the architecture work. It stacks on the architecture PR, keeps its own behavior diff reviewable, and retargets after PR A merges.

**Foundation plus feature plus tests**

```text
PR A: introduce an API or domain model
PR B: implement a feature using that API
PR C: add broad integration or runtime validation that needs both
```

All three can progress simultaneously. Reviewers can inspect each layer independently while staging state records that PR C is not promotable until A and B are reconciled.

**Parallel independent work**

```text
PR A: website commerce UI
PR B: tournament scheduler
PR C: analytics ingestion
```

If they do not depend on one another, they remain parallel. A reconciliation run in the tournament graph is not a reason to forbid the commerce or analytics PRs from existing.

**Architecture changes under an existing PR**

```text
Existing PR B was authored against old architecture.
New PR A establishes the accepted replacement architecture.
```

Prefer rebasing or retargeting PR B onto PR A, repairing B in place, and preserving its issue/review/history context. Do not automatically close B and manufacture another PR that represents the same work.

### 4.6 GitHub review readiness

GitHub Draft/ready-for-review status is a review-presentation signal. It is separate from the Tavall PR lifecycle state defined in Section 3.2. A PR may, for example, be lifecycle `PAUSED` while GitHub still shows it as Draft, or lifecycle `REVIEW_READY` when it is moved out of Draft.

Keep a pull request in **Draft** while implementation, validation, dependency reconciliation, or its description is incomplete.

Mark it ready only when its current scope is complete, the author reviewed the diff, validation is recorded, risks and gaps are disclosed, documentation is current, dependency state is accurate, and the change is reasonably reviewable as one coherent boundary.

Large coherent systems are allowed. Do not split one system into artificial fragments merely to satisfy an arbitrary line-count preference.

#### Pull request attribution and review assignment

Pull requests created by Tavall automation, ChatGPT, Codex, or another bot must preserve both human ownership and machine contribution instead of letting GitHub's single-opener field erase who actually did the work.

- Attribute `tjXJNOOBIE` as the human owner/requester on Tavall pull requests created on their behalf.
- Attribute every bot or automation that materially authored implementation, documentation, tests, commits, or the pull-request change set.
- GitHub exposes only one pull-request opener. Additional authors or contributors must therefore be named in the pull-request body, and real commit-level co-authorship should use `Co-authored-by:` trailers when an attributable commit identity is available.
- Do not list passive integrations, linkback bots, or status-only automation as authors when they did not materially produce the change.
- Request `tjXJNOOBIE` as a reviewer when they are not the pull-request author. GitHub does not permit an author to review or approve their own pull request, so an owner-authored pull request uses the Owner Self-Review path instead of a fake self-review request.
- Codex automatic review is the required advisory bot review for reviewable Tavall pull requests. Keep repository automatic review enabled; when automatic review does not appear, explicitly trigger it with `@codex review` and treat a missing or configuration-error response as an integration problem to fix rather than silently skipping the review.

### 4.7 Accountable review

Reviewers evaluate:

- correctness against requested behavior;
- compatibility with `CODE_ARCHITECTURE.md` and relevant quality documents;
- system ownership and duplicate-system risk;
- stack and dependency correctness;
- failure and recovery behavior;
- persistence and migration safety;
- concurrency and lifecycle behavior;
- permission and security boundaries;
- performance and operational impact;
- logging and audit behavior;
- test quality and missing validation;
- naming and maintainability;
- unrelated work hidden in the diff;
- fabricated APIs or shallow assumptions in generated code.

Independent approval means the reviewer accepts responsibility for the reviewed state. It is not a ceremonial green button awarded because the diff projected confidence.

Owner Self-Review uses this pull-request comment:

```text
Owner Self-Review

Scope:
- What is being promoted.

Validation:
- Checks, tests, harnesses, and manual verification actually completed.

Untested:
- Known validation not performed.

Risks:
- Material production, data, security, migration, or operational risks.

Rollback:
- Exact revert or recovery approach.

Decision:
- Ready for merge on the current reviewed pull-request state.
```

GitHub records the pull-request head and change history. Contributors are not required to manually locate and paste a commit SHA into the review record. A later reviewable change invalidates the Owner Self-Review.

### 4.8 Changes after review

Review is required again when new commits alter executable or operational behavior, conflict resolution changes the diff, a rebase or stack collapse introduces meaningful changes, generated files or dependency locks change, migration or deployment instructions change, scope expands, or automated fixes modify the implementation.

Approval applies to the current reviewable state, not an older and more emotionally convenient diff.

### 4.9 Automated review and `AGENTS.md`

Codex automatic GitHub review is the advisory automated reviewer. It should run when a pull request is opened, updated with reviewable changes, or moved from draft to ready.

Codex repository access is controlled by the installed integration. This workflow does not require reducing its repository permissions.

When reviewing, Codex:

- follows repository guidance in `AGENTS.md`;
- reviews against this workflow, `CODE_ARCHITECTURE.md`, and linked quality and system documents;
- inspects existing implementations, open PR dependencies, and linked issues before proposing replacements;
- prioritizes correctness, production safety, and architectural consistency over style preferences;
- does not satisfy independent human approval or Owner Self-Review.

When Codex authors or pushes a correction, that correction becomes a new reviewable change and invalidates stale human or owner review.

When Codex is implementing work on an existing PR, it must push coherent commits to that PR branch as it works rather than preserving meaningful progress only in a local sandbox. This keeps the PR usable as the work ledger and lets other agents inspect, stack on, reconcile with, or continue the exact GitHub-visible state.

Repository-level `AGENTS.md` should link this workflow, `CODE_ARCHITECTURE.md`, relevant quality documents, and owning system documents. Its review guidance should direct Codex to flag meaningful risks involving runtime failures, lifecycle and concurrency defects, unsafe platform APIs, dependency incompatibility, persistence and cache consistency, permissions and trust boundaries, cross-service state, resource leaks, hot paths, duplicated systems, unsafe defaults, missing tests, fabricated APIs, incomplete rollback or logging, and incorrect stack relationships.

Each meaningful automated finding should include severity, affected code, a realistic failure scenario, why it matters, and a concrete correction. Speculative formatting preferences are not defects unless they create a real correctness, compatibility, or maintainability problem.

### 4.10 Merge guidance

- Preserve a PR's branch and identity while its scope remains active; do not replace it merely to obtain cleaner history.
- Use squash merge when intermediate history has no long-term value and squashing does not obscure a stack relationship that still matters.
- Preserve meaningful working commits when their history is intentional.
- Use a merge commit when preserving an integration, release, or stack boundary is useful.
- For stacked PRs, merge the parent first unless an intentional consolidation changes the review boundary.
- After a parent merges, rebase or update and retarget its children, verify their diffs, and continue using the same child PRs.
- Delete merged working branches unless intentionally retained.
- Do not rewrite shared branch history without coordination.
- Repository-specific synchronization workflows take precedence for mirrored public modules.
- Authorized owners retain final merge-method discretion.

## 5. Git hygiene

### 5.1 Atomic commits

Each commit represents one understandable change. It should contain related code, tests, and documentation, remain reviewable within its coherent boundary, leave the branch usable or document an intentional intermediate state, and be revertible without unrelated work.

Avoid mixing formatting with behavior changes, unrelated refactors with features, dependency upgrades with unrelated work, separate fixes without a shared boundary, or generated output without its source or explanation.

Atomic does not mean artificially tiny. A commit may be large when one coherent system boundary genuinely requires it.

### 5.2 Commit messages

Every commit uses one or more typed subject lines followed by the structured body:

```text
Type: Capitalized concise action

Reason:
- Why the change is needed.

Changes:
- What changed.

Validation:
- What was run or inspected.
```

Allowed subject types:

- `Build`
- `Added`
- `Changed`
- `Removed`
- `Fixed`
- `Refactor`
- `Clean`
- `Test`
- `Docs`
- `License`
- `TODO`
- `Misc`

`Meta` is not an allowed type.

Multiple typed subject lines may appear when every line describes the same coherent boundary.

Subject rules:

- Use `Type: Action`, not Conventional Commit syntax.
- Capitalize the first word after the colon.
- Describe the result, not the act of editing files.
- Avoid vague subjects such as `Update`, `Changes`, `Stuff`, `Fix`, `Final`, or `WIP`.
- Use `Refactor`, not the legacy misspelling `Refractor`, for new commits.
- State validation truthfully. Use `Not run: <reason>` when validation was not performed.

### 5.3 Working tree discipline

Before committing, inspect `git status` and the staged diff, stage only intended files, verify the branch, remove temporary artifacts, confirm environment files are ignored, check line-ending churn, and verify that no secrets or sensitive data are included.

Never commit API keys, tokens, passwords, private keys, production credentials, unredacted user data, sensitive database dumps, or local-only environment state.

If a secret reaches Git history, rotate and invalidate it. Deleting the visible line is not remediation. It is putting a blanket over a fire.

### 5.4 Synchronization, reconciliation, and history

Update local knowledge of target branches and relevant open PRs before significant work. Use fast-forward pulls where possible. Rebase personal working branches when it improves clarity. Never rewrite a branch other contributors or synchronization automation use without coordination.

Reconciliation is graph maintenance: determine whether active PRs are independent, dependent, overlapping, superseded, or instances of the same scope. Preserve useful PR history and review context while correcting bases and dependencies.

Use `--force-with-lease` when force-pushing a personal branch. Force pushes to shared staging, synchronization, or production branches follow repository-specific rules and owner authority.

### 5.5 Scope control

Do not make unrelated drive-by changes. Leave unrelated work unchanged, record it in an issue when it meets the threshold, and handle it separately. A small cleanup may remain only when it directly supports the current change and does not obscure review.

### 5.6 AI-assisted work

The human contributor remains responsible for every committed line regardless of who or what typed it.

Provide relevant repository documents, active PR relationships, and issues; require repository discovery; verify referenced APIs and dependencies; run tests rather than trusting generated claims; inspect the complete diff; disclose uncertainty; treat AI-authored fixes as new reviewable changes; preserve established architecture and ownership; and push meaningful progress to GitHub instead of leaving it trapped in an ephemeral execution environment.

## 6. Production promotion and deployment

A production-promotion pull request or staged promotion must explain release scope, included issues and pull requests, stack relationships where relevant, important behavior changes, migrations and configuration, automated and manual evidence, risks and untested paths, rollback, and post-deployment verification.

Before merging:

- [ ] The target and source branches are correct.
- [ ] Stack parents are merged, included, or intentionally promoted together.
- [ ] Staging files or manifests reflect the intended integration state when used by the repository.
- [ ] The current diff has independent approval or a valid Owner Self-Review.
- [ ] Stale review was renewed.
- [ ] Checks pass or an authorized owner override is documented.
- [ ] Blocking conversations are resolved.
- [ ] Issues and included pull requests are linked.
- [ ] Migration, configuration, rollback, and post-deployment steps are documented.
- [ ] Automated output is not being treated as independent review.
- [ ] Deployment remains a separate authorized action.

### 6.1 Deployment remains separate

Merging into `main` does not automatically authorize or perform deployment.

The production source may be identified through a pull request, merge record, release, tag, build metadata, artifact metadata, staging manifest, or deployment tooling. Contributors are not expected to manually hunt through Git history for a commit SHA when GitHub or the build system already records the source revision.

Before deploying:

- [ ] The production source and artifact are identified.
- [ ] Review and validation status are known.
- [ ] Untested paths are documented.
- [ ] Configuration, secrets, and migrations are ready.
- [ ] Backups, rollback artifacts, or recovery procedures exist where appropriate.
- [ ] The deployment owner and affected services are known.
- [ ] Post-deployment checks and monitoring are defined.
- [ ] Active PR branches, staging state, or synchronization branches include direct production corrections that must not be overwritten later.

After deployment, verify service health, migrations, expected behavior, warnings and errors, and dependent systems. Record the deployed source and begin rollback when acceptance checks fail.

## 7. GitHub Issues as engineering context

Issues are a durable engineering record, not merely a task list.

Create or update an issue when a challenge blocks progress, may change architecture, exposes a limitation, requires investigation, affects multiple systems, creates production or security risk, records a temporary compromise, has important tradeoffs, or cannot be responsibly explained only in a commit or pull request.

Do not create issues for every tiny task, routine formatting change, temporary note, or trivial correction fully explained by one small pull request.

Direction-setting issues should document summary, current behavior, why it matters, evidence, constraints, options, current direction, acceptance criteria, related work, and AI implementation context.

Record rejected approaches, link implementation work, and close issues only when acceptance criteria are satisfied.

## 8. Author checklist

- [ ] Branch and target are correct.
- [ ] Existing PRs were checked for same-scope or dependency relationships.
- [ ] Existing same-scope PR was reused instead of duplicated.
- [ ] Stack parent/child relationships are explicit when applicable.
- [ ] Every active normal PR has valid transitive ancestry to an active repository/release staging root; any manifests match the current graph and exact heads.
- [ ] PR Type, PR State, and Execution Attachment State are not conflated when graph metadata is present or reconciled.
- [ ] Ambiguous legacy work is preserved as `NEEDS_RECONCILIATION` rather than inferred abandoned or superseded.
- [ ] Every changed integration tier has its own exact-head validation; child acceptance is not substituted for integrated acceptance.
- [ ] Complete diff was self-reviewed.
- [ ] Scope is focused.
- [ ] Relevant issues, architecture, and quality documents were reviewed.
- [ ] Tests and checks were actually run and recorded.
- [ ] Manual or bot verification is documented where required.
- [ ] Gaps, configuration, migration, rollback, and recovery are documented.
- [ ] No secrets or accidental artifacts are included.
- [ ] Generated code and APIs were verified.
- [ ] Meaningful in-progress work is pushed to the remote PR branch.
- [ ] The pull request explains what changed and why.
- [ ] `tjXJNOOBIE` and every materially authoring bot or automation are attributed in the pull-request body; real commit-level co-authorship is recorded when available.
- [ ] `tjXJNOOBIE` is requested as reviewer when they are not the author; owner-authored pull requests use Owner Self-Review instead.
- [ ] Codex automatic review completed, or `@codex review` was explicitly triggered and any integration failure was recorded.
- [ ] Codex review completed when available and meaningful findings were addressed or explained.

## 9. Reviewer checklist

- [ ] Review is independent, or the author is an authorized owner using valid Owner Self-Review.
- [ ] Requested behavior is implemented correctly.
- [ ] Architecture and repository-specific rules are respected.
- [ ] No duplicate or parallel system was introduced.
- [ ] PR base and stack relationships are correct.
- [ ] PR lifecycle intent is not inferred from GitHub Draft/closed status, CONTROL coordination state, executor liveness, age, or worktree presence.
- [ ] Protected dirty, stale, orphaned, ambiguous, paused, blocked, active, or reconciliation-required work is not treated as cleanup-safe.
- [ ] The displayed diff excludes already-reviewed parent work where expected.
- [ ] Failure, recovery, data, security, permission, lifecycle, performance, and operational behavior were considered.
- [ ] Tests are meaningful and passing.
- [ ] Documentation and migration notes are sufficient.
- [ ] Issue decisions were followed or intentionally amended.
- [ ] Codex findings and blocking conversations were inspected.
- [ ] Review applies to the current diff.
- [ ] Deployment remains separate from merge approval.

## 10. Recommended repository configuration

### Pull-request branches / `working/*`

- Allow contributor and authorized automation pushes and draft pull requests.
- Treat an existing PR branch as the durable work ledger for that scope.
- Run relevant checks on pushed checkpoints.
- Allow child PRs to target these branches for explicit stacks.
- Allow `--force-with-lease` on personal branches where repository policy permits it.
- Delete after merge unless intentionally retained.
- Do not impose an arbitrary organization-wide open-PR cap.

### Staging state and `staging/*`

- Keep repository-defined staging files or manifests authoritative for intended integration composition when that mechanism is enabled.
- Maintain a corresponding active persistent Draft integration PR for every active staging branch. Reuse the correct root and connect every Sub-Staging tier upward.
- Enforce the mandatory PR Flow invariant on creation and every topology transition; reject ambiguous roots and stale head/metadata matches.
- Allow trusted owner integration where repository-specific rules permit it.
- Run configured checks and automatic Codex review on reviewable promotion diffs.
- Block deletion of active shared staging branches and discourage uncoordinated history rewrites.

### `main`

- Require pull requests for ordinary contributors.
- Require independent approval or Owner Self-Review for pull-request promotion.
- While there is only one qualified maintainer, set required approving reviews to zero or grant that owner an explicit ruleset bypass.
- Do not require CODEOWNERS approval until another qualified code owner can approve owner-authored pull requests.
- Dismiss stale review, require conversation resolution, and run configured checks.
- Block deletion and force pushes by ordinary actors.
- Preserve explicitly authorized owner bypass authority where repository-specific synchronization rules permit it.
- Surface direct owner pushes for review through repository automation when available.
- Use CODEOWNERS to identify responsibility without creating an impossible self-approval requirement.

### Codex and `AGENTS.md`

- Enable automatic Codex pull-request review.
- Treat `@codex review` as the explicit fallback when automatic review does not appear on a reviewable pull request.
- Link this workflow, `CODE_ARCHITECTURE.md`, and relevant quality and system documents from `AGENTS.md`.
- Keep repository-specific review priorities in `AGENTS.md`.
- Teach implementation agents to inspect active PRs, staging state, and stack relationships before choosing a base, preserve dependency stacks, and establish or repair active staging ancestry as part of creating or updating the PR.
- Require agents to push coherent implementation checkpoints to the remote PR branch while working.
- Treat Codex-authored fixes as new reviewable changes.
- Do not treat automated review as independent approval.

## 11. Adoption and exceptions

Changes to this workflow should be introduced through a documentation pull request and reviewed before enforcement rules change, unless an authorized owner intentionally applies the organization-wide canonical policy directly.

Any exception must be explicit, narrow, attributable to an authorized maintainer or owner, and reviewable on GitHub when practical.

Automation cannot grant itself an exception or convert automated output into independent human acceptance.

An undocumented contributor exception is not flexibility. It is policy decay wearing business casual.
