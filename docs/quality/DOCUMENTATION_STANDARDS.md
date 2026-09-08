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

Architecture and pattern documentation must explain both **what** the rule is and **why** the rule exists. A rule without its ownership, lifecycle, testing, failure-mode, or maintainability rationale is easy to copy mechanically and easy to misuse.

For architecture pattern sections, use a concise `##### Why` subsection after a major rule or bad/good example when the rationale is not already obvious from the surrounding text. The rationale should explain the architectural consequence, not merely restate the rule. Production code references remain inline with the rule they support and link back to the source class rather than being collected into a separate evidence catalog.

Documentation should reduce ambiguity. Producing three files that disagree with each other is merely distributed ambiguity with better filenames.

### 1.1 Canonical Implementation and Tool Authority

When shared documentation describes an existing Tavall library, framework, runtime, or Java tool, the canonical owning repository is the source of truth for that tool's API shape, inheritance model, lifecycle semantics, supported low-level surfaces, and naming vocabulary.

Before adding or materially changing architecture guidance for an existing Tavall tool:

1. inspect the canonical repository at its current accepted revision;
2. read its owning interfaces, implementation classes, tests, `AGENTS.md`, and system documentation where present;
3. identify which behavior is intended for ordinary application consumers versus framework/tool implementation;
4. preserve intentional library contracts and terminology in shared docs;
5. treat a desired redesign as a separate upstream proposal or migration, not as documentation cleanup.

Shared docs may classify **when** a Tavall tool should be used and may impose cross-project consumer rules, but they must not silently redesign the tool itself.

Examples of prohibited documentation drift include:

- replacing intentional collection inheritance with composition because composition is generically fashionable;
- declaring an inherited API forbidden when the canonical tool intentionally supports it for framework or advanced use;
- inventing a new abstraction or naming layer for behavior already represented by the canonical tool;
- documenting a remembered or proposed API as if it were the current checked-in contract;
- using one downstream consumer's wrapper as the source of truth for the shared tool.

##### Why

Shared architecture exists to make Tavall's real systems coherent. If documentation can redefine a canonical tool without inspecting that tool first, it stops being governance and becomes a parallel implementation written in Markdown.

## 2. Shared Quality Policy vs Repository/System Specialization

Cross-project engineering policy belongs under `docs/quality`, including:

- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- this document
- the detailed chapters under `docs/quality/code-architecture/`

Shared quality documents define Tavall defaults. Repository- or module-specific documents may **strengthen or specialize** those defaults when a narrower runtime/product boundary requires it, but they must not silently weaken or contradict shared policy.

Project Novus and other production systems may appear as examples inside shared quality documents. An example does not narrow the policy scope.

##### Why

A shared quality repository cannot simultaneously claim cross-project authority and label its binding rules as one product's private architecture. Explicit precedence prevents copied examples from becoming accidental scope restrictions and gives agents one place to resolve conflicts.

## 3. System Document Lifecycle and Naming

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

## 4. Final Tech and Design Document

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

Do not add empty sections merely to satisfy the list.

## 5. Delegated Command and Permission Documents

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

## 6. Delegated Format and Message Documents

Use a delegated format/message document when a system has substantial visual formats, placeholders, reusable messages, or delivery-specific behavior.

Formats describe rendered structure. Messages describe user-facing/operational communication. They may share a document because both communicate system state rather than store or mutate it.

Cover:

- ownership;
- placeholder keys/data ownership/missing behavior/escaping;
- player/staff/admin/log/web/Discord/native-UI formats where applicable;
- success/failure/permission/admin/recovery messages;
- delivery/rendering/reload/cache behavior.

The document must provide raw format text or a precise textual description even when images exist.

## 7. Progression Documents

Progression documents report what is demonstrably implemented, integrated, tested, blocked, or missing at an exact audited commit.

They must not:

- define new product behavior;
- replace the final system contract;
- infer completion from file/class/test-file counts;
- claim visual success from a harness that cannot observe visuals;
- hide omitted tests, manual checks, blockers, or unverified recovery paths.

Update progression in the same coherent change as the implementation/audit evidence it reports.

## 8. Folder and Delegation Rules

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

## 9. Archive Rules

Archive a document when it is obsolete, conflicts with an active owner, or would otherwise compete as a source of truth.

- Archived documents are historical evidence only.
- Every archive identifies former path/authority, reason, and current replacement/owner.
- Update normal inbound links to active replacements.
- Do not rewrite archived content to look current.
- Record archives in the repository's archive index when one exists.

## 10. Change and Review Rules

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
- [ ] Existing canonical Tavall tools were inspected before their API, inheritance, lifecycle, or naming patterns were documented or changed.
- [ ] Shared docs preserve accepted tool contracts unless a separate upstream migration has changed the canonical owner first.
- [ ] Production examples are linked inline to source instead of copied into a competing evidence catalog.
- [ ] Links resolve and examples use current repository/module/class names.
- [ ] Obsolete drafts are removed, archived, or clearly marked so they cannot compete with accepted contracts.
