# Tavall Documentation Standards

> **Status:** Active  
> **Applies to:** Tavall system, architecture, command, message, format, progression, operational, and quality documentation  
> **Purpose:** Keep each document's authority clear and prevent planned behavior, implementation status, and final contracts from collapsing into one contradictory pile.

## 1. Core Rules

Documentation is part of the engineering contract.

- Every document must state what it owns and what it must not define.
- One subject must have one canonical source of truth.
- Final documents define accepted behavior; progression documents report audited implementation status.
- Draft documents may propose behavior but must not claim that the behavior is implemented or approved.
- Code, schemas, tests, issues, and pull requests provide implementation evidence. A confident paragraph does not.
- Extend an existing owning document before creating a parallel document for the same rules.
- Split a supporting document only when the main owning document would become materially harder to read.
- The main system document must summarize and link any delegated command, permission, format, message, schema, or integration document.
- Maintained Tavall system documents must link their working Notion record when one exists, and the Notion record must link the system's design, final/canonical, progression/evidence, and implementation sources.
- Every maintained Tavall document ends with a `DOC TODO:` maintenance handoff as defined below.

Architecture and pattern documentation must explain both **what** the rule is and **why** the rule exists. A rule without its ownership, lifecycle, testing, failure-mode, or maintainability rationale is easy to copy mechanically and easy to misuse.

For architecture pattern sections, use a concise `##### Why` subsection after a major rule or bad/good example when the rationale is not already obvious from the surrounding text. The rationale should explain the architectural consequence, not merely restate the rule. Production code references remain inline with the rule they support and link back to the source class rather than being collected into a separate evidence catalog.

Documentation should reduce ambiguity. Producing three files that disagree with each other is merely distributed ambiguity with better filenames.

## 2. Shared Quality Policy vs Repository/System Specialization

Cross-project engineering policy belongs under `docs/quality`, including:

- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- this document
- [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md)
- the detailed chapters under `docs/quality/code-architecture/`

Shared quality documents define Tavall defaults. Repository- or module-specific documents may **strengthen or specialize** those defaults when a narrower runtime/product boundary requires it, but they must not silently weaken or contradict shared policy.

Project Novus and other production systems may appear as examples inside shared quality documents. An example does not narrow the policy scope.

##### Why

A shared quality repository cannot simultaneously claim cross-project authority and label its binding rules as one product's private architecture. Explicit precedence prevents copied examples from becoming accidental scope restrictions and gives agents one place to resolve conflicts.

## 3. Notion Working Records and Cross-Surface Linkage

Notion is the working cross-repository design and reconciliation surface for a Tavall system. GitHub/repository documentation remains the portable, reviewable system contract and implementation-evidence surface.

A Notion working system record does not replace a repository `FINAL`, `FINAL_DRAFT`, progression document, schema, test suite, or implementation. It connects them.

Use [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md) as the portable contract for a new Notion system record. Create a new Notion record only when there is a genuinely distinct system/domain/authority boundary. Otherwise update the existing record.

Every maintained Notion system record must include these link classes:

1. **Design Source(s)**
   - The material that established or materially changed the design.
   - May be a repository design/final-draft document, another Notion design page, or a PR/issue when the PR/issue genuinely contains the design.
2. **Final / Canonical Documentation**
   - Link the accepted `*_FINAL.md` when it exists.
   - If no accepted final exists, state **Not finalized yet** and link the current `FINAL_DRAFT` / `FINAL_DRAFT_NHV` / explicit design candidate.
3. **Progression / Evidence Documentation**
   - Link the current `*_PROGRESSION.md`, acceptance record, exact-source validation, or other evidence owner that answers what is actually implemented and validated.
4. **Implementation**
   - Link the owning repository/module and current PR/staging/runtime lineage where useful.
   - PRs are implementation/evidence references, not substitutes for final documentation.

Repository system documents should include a **Working Notion Record** or equivalent backlink when a maintained Notion record exists. Delegated/reference documents may link through their owning system document instead of duplicating every cross-surface link.

When Notion and GitHub disagree:

- an accepted repository `FINAL` owns accepted system behavior;
- a progression/evidence document owns audited implementation state at its recorded source;
- the Notion record owns working cross-repository design/reconciliation context;
- the conflict must be reconciled explicitly rather than selecting whichever paragraph is newer or more convenient.

A copied `docs/quality` tree in a consumer repository is a projection of shared quality policy. It does **not** create a new system authority or justify a duplicate Notion page.

##### Why

Design conversations, repository contracts, and implementation evidence evolve at different speeds. Explicit cross-surface links let a reader move from the working design to the accepted contract and then to actual implementation status without treating chat history, PR prose, or a copied policy file as accidental authority.

## 4. System Document Lifecycle and Naming

The filename patterns in this section apply to **product/system design documents**, not shared quality chapters such as `CLASSES.md`, `BUILDERS.md`, or `GIT_WORKFLOW.md`.

System documents use uppercase descriptive filenames with the system name first.

| State | File Name Pattern | Authority |
| --- | --- | --- |
| Working design | `SOME_SYSTEM_FINAL_DRAFT.md` | Proposed behavior still open to material design changes. |
| Complete candidate without human validation | `SOME_SYSTEM_FINAL_DRAFT_NHV.md` | Candidate final contract awaiting human review and approval. |
| Accepted final contract | `SOME_SYSTEM_FINAL.md` | Canonical product and technical contract for the system. |
| Implementation tracker | `SOME_SYSTEM_PROGRESSION.md` | Audited implementation, integration, and verification status only. |
| Commands and permissions draft | `SOME_SYSTEM_COMMANDS_AND_PERMISSIONS_DRAFT.md` | Proposed command/access contract delegated by the system document. |
| Formats and messages draft | `SOME_SYSTEM_MESSAGES_AND_FORMATS_DRAFT.md` | Proposed visual/message contract delegated by the system document. |

### Promotion Rules

- `FINAL_DRAFT` may change freely while the design is being developed.
- `FINAL_DRAFT_NHV` means the candidate is structurally complete but has not received confirmed human validation.
- `FINAL` requires human review of the current candidate and removal of unresolved draft language.
- Renaming a file does not promote its authority by itself. Owning content, links, status header, and review evidence must also be updated.
- A progression document never becomes a final document. They answer different questions.
- Planned behavior in a final contract must still be reported accurately in progression as `Designed`, `Partially Implemented`, or another evidence-backed status.

## 5. Final Tech and Design Document

The final tech/design document is the main source of truth for one system.

Use only sections that apply, normally in this order:

1. **About**
   - Purpose and user/operator/developer value.
   - Scope and non-goals.
2. **Ownership Rules**
   - What the system owns.
   - What connected systems own.
   - Behavior the system must not duplicate.
3. **System Rules and Behavior**
   - Canonical product rules.
   - State transitions and invariants.
4. **Technical Structure**
   - Owning modules/packages.
   - Important handlers, services, orchestrators, registries, caches, persistence boundaries, routers, interfaces, and platform adapters.
5. **Data Model and Storage**
   - Authoritative storage.
   - Cache/registry/file/runtime/distributed ownership.
   - Recovery, reconciliation, migration, and audit requirements.
6. **Runtime Flows**
   - Success paths.
   - Failure, cancellation, expiration, reload, shutdown, and recovery paths.
7. **Commands and Permissions Summary**
8. **Formats and System Messages Summary**
9. **Integrations**
10. **Validation Requirements**
11. **Final Rules Summary**
12. **DOC TODO:** maintenance handoff

Do not add empty sections merely to satisfy the list.

## 6. Delegated Command and Permission Documents

Use a delegated command/permission document only when command/access complexity justifies it.

It owns detailed command syntax and access behavior. It must not redefine the system's product rules, storage model, or shared architecture.

Every command identifies its owning runtime. Shared backend behavior may be platform-neutral, but registration, sender types, and delivery belong to the platform exposing the command.

Recommended content:

- ownership/access rules;
- command syntax/aliases/arguments/defaults;
- permission/rank/power requirements;
- targeting/cooldown/confirmation/audit behavior;
- success/failure behavior;
- permission nodes/matrix.

## 7. Delegated Format and Message Documents

Use a delegated format/message document when a system has substantial visual formats, placeholders, reusable messages, or delivery-specific behavior.

Formats describe rendered structure. Messages describe user-facing/operational communication. They may share a document because both communicate system state rather than store or mutate it.

Cover:

- ownership;
- placeholder keys/data ownership/missing behavior/escaping;
- player/staff/admin/log/web/Discord/native-UI formats where applicable;
- success/failure/permission/admin/recovery messages;
- delivery/rendering/reload/cache behavior.

The document must provide raw format text or a precise textual description even when images exist.

## 8. Progression Documents

Progression documents report what is demonstrably implemented, integrated, tested, blocked, or missing at an exact audited commit.

They must not:

- define new product behavior;
- replace the final system contract;
- infer completion from file/class/test-file counts;
- claim visual success from a harness that cannot observe visuals;
- hide omitted tests, manual checks, blockers, or unverified recovery paths.

Update progression in the same coherent change as the implementation/audit evidence it reports.

## 9. Folder and Delegation Rules

System documentation lives beneath the narrowest owning system folder when the repository has a system-doc tree:

```text
docs/<system>/
├── SOME_SYSTEM_FINAL.md
├── SOME_SYSTEM_PROGRESSION.md
├── SOME_SYSTEM_COMMANDS_AND_PERMISSIONS_DRAFT.md
├── SOME_SYSTEM_MESSAGES_AND_FORMATS_DRAFT.md
└── imgs/
```

Only create files the system actually needs.

Rules:

- Keep executable schemas/migrations with executable source; summarize/link them from owning docs.
- Keep images beneath the owning system folder unless genuinely shared.
- Do not create global command/message/schema documents that erase system ownership.
- Delegated documents link back to their owning final document once it exists.
- Final documents summarize delegated rules so readers do not reconstruct the contract through a scavenger hunt.

## 10. Archive Rules

Archive a document when it is obsolete, conflicts with an active owner, or would otherwise compete as a source of truth.

- Archived documents are historical evidence only.
- Every archive identifies former path/authority, reason, and current replacement/owner.
- Update normal inbound links to active replacements.
- Do not rewrite archived content to look current.
- Record archives in the repository's archive index when one exists.

## 11. `DOC TODO:` Maintenance Handoff

Every maintained Tavall document ends with a `DOC TODO:` section. Use it as a handoff for what must happen next to keep the document and its represented system coherent.

Use this shape:

```markdown
## DOC TODO:

### Document next steps

- [ ] Reconcile or add missing design/final/progression/implementation links.
- [ ] Promote, archive, supersede, or clarify the document when its lifecycle changes.

### System next steps

- [ ] Record only the next system design/implementation/validation work directly represented by this document.
```

Rules:

- **Document next steps** are documentation work: missing sources, stale links, lifecycle promotion, supersession, ownership cleanup, validation description, archive work, or evidence reconciliation.
- **System next steps** are only the engineering/design/validation steps directly represented by the document.
- The section is not a second unsorted product backlog and does not replace Linear/GitHub issues/project planning.
- A TODO does not authorize implementation or turn proposed behavior into accepted behavior.
- Completed TODOs should be reflected in the owning document/progression/evidence and then removed rather than accumulating forever.
- Delegated/reference documents may keep their system TODOs narrow and point to the owning system record for broader work.
- An accepted `FINAL` document still carries `DOC TODO:`. If there is no open documentation maintenance, say so explicitly. New material contract changes must enter a new design/draft lineage rather than appearing as stealth future requirements in a Final's TODO list.
- A progression document may list implementation/verification next steps, but must continue to report current evidence separately from future work.

##### Why

A document without an explicit maintenance handoff becomes stale silently. A document with an unbounded TODO list becomes a shadow project tracker. Splitting document maintenance from system work preserves both accountability and authority.

## 12. Change and Review Rules

Documentation changes follow [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

Before accepting a documentation change, confirm:

- [ ] Document type/lifecycle/authority are explicit.
- [ ] Shared quality policy and repository/system specialization have correct precedence.
- [ ] The owning system/folder are correct.
- [ ] The document does not duplicate another source of truth.
- [ ] Proposed behavior is not presented as implemented behavior.
- [ ] Final behavior has required human validation.
- [ ] Progress claims name evidence and an audited commit.
- [ ] Delegated documents are summarized/linked by their owner.
- [ ] Commands, permissions, formats, messages, schemas, and integrations are defined in the correct document.
- [ ] Architecture pattern rules explain why the pattern exists rather than only prescribing shape.
- [ ] Production examples are linked inline to source instead of copied into a competing evidence catalog.
- [ ] The working Notion record is linked when one exists.
- [ ] The Notion record links Design Source(s), Final/Canonical, Progression/Evidence, and Implementation.
- [ ] `DOC TODO:` is present, split into document and system next steps, and does not smuggle unapproved behavior into a Final.
- [ ] Links resolve and examples use current repository/module/class names.
- [ ] Obsolete drafts are removed, archived, or clearly marked so they cannot compete with accepted contracts.

---

## DOC TODO:

### Document next steps

- [ ] Apply this linkage/footer contract to existing maintained Tavall system documentation as those documents are touched or reconciled.
- [ ] Keep the Notion system-record template and this standard synchronized when the documentation contract changes.
- [ ] Reconcile repositories that currently have active system implementation but no lifecycle-compliant design/final documentation.

### System next steps

- [ ] Add automated architecture/documentation checks where a rule can be enforced mechanically without pretending automation can decide human design acceptance.
