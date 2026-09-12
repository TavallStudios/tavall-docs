# Tavall Documentation Standards

> **Status:** Active  
> **Applies to:** Tavall GENERAL, Design, Technical, architecture, command, message, format, progression, operational, and quality documentation  
> **Purpose:** Keep each document's authority clear and prevent broad context, detailed design, technical contracts, implementation status, and final authority from collapsing into one contradictory pile.

## 1. Core Rules

Documentation is part of the engineering contract.

- Every document must state what it owns and what it must not define.
- One subject must have one canonical owner for each documentation responsibility.
- `GENERAL` documents provide broad system context, navigation, cross-repository reconciliation, and links to detailed documentation.
- Design documents own detailed product/system behavior and design decisions according to their Draft/Final lifecycle.
- Technical documents own detailed implementation/architecture contracts according to their Draft/Final lifecycle.
- Progression documents report audited implementation status and evidence.
- Draft documents may propose behavior but must not claim that the behavior is implemented or approved.
- Code, schemas, tests, issues, and pull requests provide implementation evidence. A confident paragraph does not.
- Extend an existing owning document before creating a parallel document for the same rules.
- Split a supporting document only when the owning document would become materially harder to read.
- Detailed Design, Technical, and progression documents must link back to their owning GENERAL document when one exists.
- The GENERAL document must link forward to current Design, Technical, progression/evidence, and implementation sources.
- Every maintained Tavall document ends with a `DOC TODO:` maintenance handoff as defined below.

### Delegated Architecture Documentation

When one architecture document delegates a topic to a specialized chapter:

- put the routing/index information **before** enough topic detail exists for a reader to reasonably stop;
- the root/owning document defines shared invariants, precedence, and routing;
- the delegated chapter owns detailed mechanics, examples, exceptions, and topic-specific review criteria;
- the root may summarize a delegated rule, but it must not become a competing mini-chapter that can drift independently;
- readers and agents must read every delegated chapter relevant to the code being changed; a root summary is not a substitute;
- multi-boundary work may require several delegated chapters;
- delegated chapters link back to the root and state their specialization scope;
- a direct contradiction between root and delegated guidance is a documentation defect and must not be silently resolved by choosing the more convenient paragraph.

Until a discovered contradiction is reconciled, the owning/root invariant controls unless a narrower repository/module authority explicitly and validly strengthens it.

##### Why

Early routing preserves context budget for the document that actually owns the detail. Keeping examples and mechanics in one specialized owner also reduces duplicate policy that can drift into contradictory instructions.

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

Where an active `DOC_DESIGN_RULES.md` defines more specific Design/Technical document types, lifecycle states, or naming, those rules remain authoritative for those detailed document types. This standard adds the GENERAL relationship and cross-surface linkage contract; it does not erase more specific Design/Technical rules.

##### Why

A shared quality repository cannot simultaneously claim cross-project authority and label its binding rules as one product's private architecture. Explicit precedence prevents copied examples from becoming accidental scope restrictions and gives agents one place to resolve conflicts.

## 3. Document Types and GENERAL Ownership

### GENERAL

A `GENERAL` document is the broad system/product/platform record. It answers questions such as:

- What is this system and why does it exist?
- What is its scope and ownership boundary?
- Which Design and Technical documents currently define it?
- Which repositories/runtimes/products participate?
- What implementation/progression evidence is current?
- Which older records are superseded?

A GENERAL document may live in Notion or GitHub. The Tavall Notion system records created from [NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md](NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md) are `GENERAL` documents.

GENERAL is a **document type**, not a Draft/Final lifecycle state. It is intentionally broad and may remain active while its linked Design and Technical documents move independently through Draft, candidate, and Final states.

A GENERAL document may summarize design and technical context for navigation, but it must not become a second full copy of the detailed Design or Technical contracts.

### Design

Design documents own the detailed product/system design contract: behavior, user/operator/developer experience, domain rules, state semantics, interactions, and other design decisions assigned to the Design document by current Tavall design rules.

Design documents link back to the owning GENERAL record.

### Technical

Technical documents own the detailed technical/architecture contract: modules, interfaces, data ownership, persistence/projections, runtime flows, failure/recovery, integrations, deployment/runtime constraints, and validation requirements assigned to the Technical document by current Tavall design rules.

Technical documents link back to the owning GENERAL record.

### Progression / Evidence

Progression documents report what is demonstrably implemented, integrated, tested, blocked, or missing at an exact audited source state. They link back to the owning GENERAL record and to the Design/Technical contracts they are measuring where practical.

### Compatibility with Existing Combined Finals

Some current repositories use one combined Final Tech & Design document such as `SOME_SYSTEM_FINAL.md` or its Draft variants. That document may temporarily satisfy both the Design and Technical links from GENERAL.

Do **not** create repository-wide churn merely to rename or split a healthy existing document. Split or promote documentation when the owning system is naturally touched, when the separation materially improves authority, or when current Design/Technical rules require it.

## 4. GENERAL Records and Cross-Surface Linkage

Notion is a strong working cross-repository surface for GENERAL records, but GENERAL is not Notion-specific. A GENERAL record may be stored in either Notion or GitHub when that is the appropriate owning surface.

Every maintained GENERAL record must include these link classes:

1. **Design Documentation**
   - Link the current detailed Design document(s) and lifecycle state.
   - If Design is not final, state that and link the current Draft/candidate.
2. **Technical Documentation**
   - Link the current detailed Technical document(s) and lifecycle state.
   - If Technical is not final, state that and link the current Draft/candidate.
3. **Design Source(s)**
   - Link material that established or materially changed the design, including Notion/chat-derived records, repository docs, and PRs/issues when they genuinely contain design work.
4. **Final / Canonical Documentation**
   - Link the accepted Design and Technical contract(s). If either side is not final, say so explicitly.
5. **Progression / Evidence Documentation**
   - Link the current progression/acceptance/exact-source evidence owner.
6. **Implementation**
   - Link the owning repository/module and current PR/staging/runtime lineage where useful.

Detailed Design and Technical Draft/Final documents must contain a **GENERAL Document** or equivalent backlink to the owning GENERAL record. Progression documents should backlink as well.

Delegated/reference documents may link through their owning Design/Technical document instead of duplicating every GENERAL link.

When documentation disagrees:

- accepted Design/Technical Finals own their assigned accepted contract;
- progression/evidence owns audited implementation state at its recorded source;
- GENERAL owns broad context, navigation, cross-repository reconciliation, and the current documentation graph;
- the conflict must be reconciled explicitly rather than selecting whichever paragraph is newer or more convenient.

A copied `docs/quality` tree in a consumer repository is a projection of shared quality policy. It does **not** create a new system authority or justify a duplicate GENERAL record.

##### Why

The broad system record, product/design contract, technical implementation contract, and audited implementation state evolve at different speeds. GENERAL gives them one stable rendezvous point without forcing one document to become all four things.

## 5. Existing System Lifecycle Compatibility

The existing filename lifecycle remains valid for repositories currently using combined system documents:

| State | File Name Pattern | Authority |
| --- | --- | --- |
| Working combined design/technical contract | `SOME_SYSTEM_FINAL_DRAFT.md` | Proposed behavior still open to material design or technical changes. |
| Complete combined candidate without human validation | `SOME_SYSTEM_FINAL_DRAFT_NHV.md` | Candidate final contract awaiting human review and approval. |
| Accepted combined contract | `SOME_SYSTEM_FINAL.md` | Canonical combined Design + Technical contract until/if split. |
| Implementation tracker | `SOME_SYSTEM_PROGRESSION.md` | Audited implementation, integration, and verification status only. |
| Commands and permissions draft | `SOME_SYSTEM_COMMANDS_AND_PERMISSIONS_DRAFT.md` | Proposed command/access contract delegated by the owning Design/Technical docs. |
| Formats and messages draft | `SOME_SYSTEM_MESSAGES_AND_FORMATS_DRAFT.md` | Proposed visual/message contract delegated by the owning Design/Technical docs. |

Promotion rules remain:

- Drafts may change while design/technical work is being developed.
- NHV candidates are structurally complete but await human validation.
- Final authority requires human review of the current candidate and removal of unresolved draft language.
- Renaming a file does not promote its authority by itself.
- A progression document never becomes a Design or Technical Final.
- Planned behavior in a Final must still be represented truthfully in progression as designed, partial, blocked, or implemented according to evidence.

## 6. Design and Technical Final Documents

Use the current Tavall Design/Technical rules for exact subtype content and naming. At minimum:

### Design owns

- purpose, scope, and user/operator/developer value;
- domain/product rules and invariants;
- states and behavior;
- interaction/experience rules;
- commands/messages/formats at the appropriate design-summary level;
- connected-system ownership from the design perspective.

### Technical owns

- module/package/service/handler/orchestrator boundaries;
- interfaces, routers, registries, caches, persistence, schemas and platform adapters;
- authoritative storage and projection ownership;
- recovery, reconciliation, migration, audit and idempotency;
- success/failure/cancellation/reload/shutdown flows;
- integration and validation requirements.

A combined Final may continue to contain both sets until separation is useful or required.

## 7. Delegated Command and Permission Documents

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

## 8. Delegated Format and Message Documents

Use a delegated format/message document when a system has substantial visual formats, placeholders, reusable messages, or delivery-specific behavior.

Formats describe rendered structure. Messages describe user-facing/operational communication. They may share a document because both communicate system state rather than store or mutate it.

Cover:

- ownership;
- placeholder keys/data ownership/missing behavior/escaping;
- player/staff/admin/log/web/Discord/native-UI formats where applicable;
- success/failure/permission/admin/recovery messages;
- delivery/rendering/reload/cache behavior.

The document must provide raw format text or a precise textual description even when images exist.

## 9. Progression Documents

Progression documents report what is demonstrably implemented, integrated, tested, blocked, or missing at an exact audited commit.

They must not:

- define new product behavior;
- replace Design or Technical final authority;
- infer completion from file/class/test-file counts;
- claim visual success from a harness that cannot observe visuals;
- hide omitted tests, manual checks, blockers, or unverified recovery paths.

Update progression in the same coherent change as the implementation/audit evidence it reports.

## 10. Folder and Delegation Rules

System documentation lives beneath the narrowest owning system folder when the repository has a system-doc tree. A repository may keep a GENERAL document there, or use a Notion GENERAL record and backlink from repository docs.

Example compatibility layout:

```text
docs/<system>/
├── SOME_SYSTEM_GENERAL.md                 # optional when GENERAL lives in GitHub
├── SOME_SYSTEM_FINAL.md                   # existing combined Design + Technical Final
├── SOME_SYSTEM_PROGRESSION.md
├── SOME_SYSTEM_COMMANDS_AND_PERMISSIONS_DRAFT.md
├── SOME_SYSTEM_MESSAGES_AND_FORMATS_DRAFT.md
└── imgs/
```

Do not infer this compatibility layout overrides a more specific active Design/Technical naming rule.

Rules:

- Keep executable schemas/migrations with executable source; summarize/link them from owning Technical docs.
- Keep images beneath the owning system folder unless genuinely shared.
- Do not create global command/message/schema documents that erase system ownership.
- Delegated documents link back to their owning Design/Technical document.
- Design and Technical docs link back to GENERAL.
- GENERAL links forward to Design, Technical, progression/evidence, and implementation.

## 11. Archive Rules

Archive a document when it is obsolete, conflicts with an active owner, or would otherwise compete as a source of truth.

- Archived documents are historical evidence only.
- Every archive identifies former path/authority, reason, and current replacement/owner.
- Update normal inbound links to active replacements.
- Do not rewrite archived content to look current.
- Record archives in the repository's archive index when one exists.

## 12. `DOC TODO:` Maintenance Handoff

Every maintained Tavall document ends with a `DOC TODO:` section. Use it as a handoff for what must happen next to keep the document and its represented system coherent.

Use this shape:

```markdown
## DOC TODO:

### Document next steps

- [ ] Reconcile or add missing GENERAL/Design/Technical/progression/implementation links.
- [ ] Promote, archive, supersede, or clarify the document when its lifecycle changes.

### System next steps

- [ ] Record only the next system design/implementation/validation work directly represented by this document.
```

Rules:

- **Document next steps** are documentation work: missing sources, stale links, lifecycle promotion, supersession, ownership cleanup, validation description, archive work, or evidence reconciliation.
- **System next steps** are only engineering/design/validation steps directly represented by the document.
- The section is not a second unsorted product backlog and does not replace Linear/GitHub issues/project planning.
- A TODO does not authorize implementation or turn proposed behavior into accepted behavior.
- Completed TODOs should be reflected in the owning GENERAL/Design/Technical/progression/evidence content and then removed rather than accumulating forever.
- Accepted Design or Technical Finals still carry `DOC TODO:`. If there is no open documentation maintenance, say so explicitly. Material contract changes enter a new Draft lineage rather than appearing as stealth future requirements in a Final's TODO list.
- A GENERAL record may carry cross-document/system next steps but must not become the replacement for the project's real task tracker.

##### Why

A document without an explicit maintenance handoff becomes stale silently. A document with an unbounded TODO list becomes a shadow project tracker. Splitting document maintenance from system work preserves both accountability and authority.

## 13. Change and Review Rules

Documentation changes follow [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

Before accepting a documentation change, confirm:

- [ ] Document type/lifecycle/authority are explicit.
- [ ] A GENERAL owner exists or the absence is intentional.
- [ ] Design and Technical Draft/Final docs backlink to GENERAL when one exists.
- [ ] GENERAL links current Design, Technical, progression/evidence, and implementation sources.
- [ ] Shared quality policy and repository/system specialization have correct precedence.
- [ ] Root/delegated routing appears before enough duplicate detail for readers to stop early.
- [ ] A root summary does not compete with a delegated chapter for the same mechanics/examples.
- [ ] Multi-topic architecture guidance names every specialized chapter readers must inspect.
- [ ] The owning system/folder are correct.
- [ ] The document does not duplicate another source of truth.
- [ ] Proposed behavior is not presented as implemented behavior.
- [ ] Final behavior has required human validation.
- [ ] Progress claims name evidence and an audited commit.
- [ ] Delegated documents are summarized/linked by their owner.
- [ ] Commands, permissions, formats, messages, schemas, and integrations are defined in the correct document.
- [ ] Architecture pattern rules explain why the pattern exists rather than only prescribing shape.
- [ ] Production examples are linked inline to source instead of copied into a competing evidence catalog.
- [ ] `DOC TODO:` is present, split into document and system next steps, and does not smuggle unapproved behavior into a Final.
- [ ] Links resolve and examples use current repository/module/class names.
- [ ] Obsolete drafts are removed, archived, or clearly marked so they cannot compete with accepted contracts.

---

## DOC TODO:

### Document next steps

- [ ] Apply the GENERAL backlink/link-graph contract to existing maintained Tavall documentation as those systems are touched or reconciled.
- [ ] Keep the GENERAL Notion template and this standard synchronized when the documentation contract changes.
- [ ] Reconcile repositories that currently have active system implementation but no lifecycle-compliant Design/Technical documentation.
- [ ] Reconcile the active `DOC_DESIGN_RULES.md` lineage/location into `tavall-docs` so its detailed Design/Technical taxonomy is directly discoverable from main.

### System next steps

- [ ] Add automated documentation checks where GENERAL backlinks/link classes and `DOC TODO:` presence can be enforced mechanically without pretending automation can decide human design acceptance.
