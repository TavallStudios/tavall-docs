# Tavall GENERAL System Record Template

> **Status:** Active template  
> **Document type:** `GENERAL`  
> **Applies to:** Tavall working GENERAL records for systems, products, platforms, architecture families, workflows, and infrastructure  
> **Purpose:** Provide the broad system context and navigation layer that connects detailed Design and Technical documentation, implementation/progression evidence, and next documentation/system actions.

This is the portable GitHub copy of the Tavall GENERAL-record template. A GENERAL document may live in Notion or GitHub. Current Tavall Notion system records are GENERAL documents and may use native Notion mentions/tables/callouts, but they must preserve the same information contract.

A GENERAL document is not a substitute for detailed Design or Technical documentation. It summarizes the system boundary, current cross-repository context, and documentation graph. Detailed Design and Technical `DRAFT`/candidate/`FINAL` documents link back to their owning GENERAL document.

## Document Identity

- **Document Type:** `GENERAL`
- **System / Domain:** TODO
- **Working Status:** Idea / Designing / Designed / Implementing / Validating / Finalized / Parked
- **Owning Repository / Module:** TODO
- **Owning Product / Platform:** TODO
- **Last Reconciled:** TODO

## Documentation Links

### Design Documentation

Link the current detailed **Design** document or document set and state its lifecycle (`DRAFT`, candidate, or `FINAL`). The GENERAL record may summarize design context but does not replace the Design contract.

- TODO

### Technical Documentation

Link the current detailed **Technical** document or document set and state its lifecycle (`DRAFT`, candidate, or `FINAL`). The GENERAL record may summarize architecture/implementation context but does not replace the Technical contract.

- TODO

If the repository still uses one combined Final Tech & Design document, link that same document under both Design and Technical until the documentation is naturally split or promoted. Do not create churn solely to rename historical documentation.

### Design Source(s)

Link the material that actually established or materially changed the design. Sources may be chat-derived Notion records, repository design documents, GitHub PRs/issues when they genuinely contain the design, or another explicit Tavall record.

- TODO

### Final / Canonical Documentation

Link the currently accepted Design and Technical contract(s). If either side is not final, state that explicitly and link its current draft/candidate instead.

- TODO

### Progression / Evidence Documentation

Link implementation/progression docs, acceptance records, exact-source evidence, or dashboards that answer **what is actually implemented and validated now**.

- TODO

### Implementation

Link owning repositories/modules and current PR/staging/runtime lineage where useful. PR links are implementation/evidence references, not substitutes for Design or Technical final documentation.

- TODO

## Purpose

What problem this system solves and who/what consumes it.

## Scope & Non-Goals

State the broad system boundary. Detailed behavioral rules belong in Design documentation; detailed implementation architecture belongs in Technical documentation.

## Authority & Ownership Summary

Summarize:

- the domain/system authority;
- connected systems and their ownership;
- owning runtime/platform/repositories;
- security/authorization boundaries where useful.

Do not duplicate the full Design or Technical contract here.

## Current Design Summary

Summarize the current agreed direction and important invariants at a navigation level. Link to the owning Design document for the detailed behavior.

## Current Technical Summary

Summarize the current implementation/architecture direction at a navigation level. Link to the owning Technical document for modules, data ownership, runtime flows, recovery, and failure behavior.

## Cross-Repository / Cross-System Context

Record context that is useful precisely because the GENERAL document sits above individual implementation documents: related repositories, products, runtimes, shared platform dependencies, migrations, and supersession relationships.

## Validation & Current State

Summarize the current evidence boundary and link to progression/acceptance records. Do not turn the GENERAL record into the implementation tracker.

## Decisions, Open Questions & Supersession

Record unresolved cross-document decisions and identify older GENERAL/design/technical records this page supersedes or narrows.

---

## DOC TODO:

### Document next steps

- [ ] Reconcile all Design Source links.
- [ ] Link the current Design document and lifecycle state.
- [ ] Link the current Technical document and lifecycle state.
- [ ] Link the current Final/canonical documentation or explicitly state which Design/Technical side is not finalized yet.
- [ ] Link progression/evidence and current implementation lineage.
- [ ] Remove stale/duplicate authority links and mark superseded material clearly.
- [ ] Keep backlinks from Design, Technical, and progression documents to this GENERAL owner current.

### System next steps

- [ ] Record only next engineering/design/validation steps directly represented by this GENERAL record.
- [ ] Keep implementation claims evidence-backed; document completion does not imply system completion.
- [ ] Remove completed items once they are reflected in the owning Design/Technical/progression/evidence documentation.

## `DOC TODO:` Rules

Every maintained Tavall document ends with a `DOC TODO:` section.

- The section is the document's maintenance handoff, not a second unsorted product backlog.
- Separate **Document next steps** from **System next steps**.
- GENERAL document TODOs primarily cover documentation-graph reconciliation, missing Design/Technical links, supersession, ownership, and cross-repository context.
- System TODOs contain only work directly represented by the document and must not imply approval or implementation.
- Completed items should move into the appropriate Design/Technical/final/progression/evidence content and then be removed from the TODO list.
- Accepted Design or Technical `FINAL` documents still carry their own footer, but material future contract changes enter a new draft lineage rather than hiding in TODOs.
