# Tavall Notion System Design Record Template

> **Status:** Active template  
> **Applies to:** Tavall working Notion records for system, product, platform, architecture, workflow, and infrastructure design  
> **Purpose:** Keep Notion design records connected to their design sources, accepted final documentation, implementation/progression evidence, and next documentation/system actions.

This is the portable GitHub copy of the Tavall Notion system-record template. The working Notion template may use native Notion mentions/tables/callouts, but it must preserve the same information contract.

## Document Identity

- **System / Domain:** TODO
- **Working Status:** Idea / Designing / Designed / Implementing / Validating / Finalized / Parked
- **Owning Repository / Module:** TODO
- **Owning Product / Platform:** TODO
- **Last Reconciled:** TODO

## Documentation Links

### Design Source(s)

Link the material that actually established or materially changed the design. Sources may be Notion design records, repository design documents, GitHub PRs/issues when they contain the design, or another explicit Tavall design record.

- TODO

### Final / Canonical Documentation

Link the current accepted contract. Prefer the repository's `*_FINAL.md` or the applicable shared Tavall quality document once it exists. If no final exists, write **Not finalized yet** and link the current `FINAL_DRAFT` / `FINAL_DRAFT_NHV` candidate instead.

- TODO

### Progression / Evidence Documentation

Link implementation/progression docs, acceptance records, exact-source evidence, or dashboards that answer **what is actually implemented and validated now**.

- TODO

### Implementation

Link owning repositories/modules and current PR/staging/runtime lineage where useful. PR links are implementation/evidence references, not substitutes for final documentation.

- TODO

## Purpose

What problem this system solves and who/what consumes it.

## Scope & Non-Goals

State the system boundary explicitly. Include what this system **must not own** when adjacent Tavall systems have authority.

## Authority & Ownership

- Authoritative state/behavior owned here.
- Connected systems and what they own.
- Runtime/platform adapters.
- Security/authorization boundary where relevant.

## Design & Invariants

Record current agreed behavior, lifecycle, state transitions, and invariants. Distinguish designed behavior from implementation evidence.

## Technical Structure

Owning modules/packages/services/handlers/orchestrators, important interfaces, routing, registries/caches/persistence, and platform adapters.

## Data, Recovery & Reconciliation

Authoritative storage, cache/projection behavior, restart/recovery expectations, migrations, idempotency, reconciliation, and audit behavior where applicable.

## Runtime Flows

Describe important success paths and relevant failure/cancellation/expiration/reload/shutdown/recovery paths.

## Integrations & Dependencies

List typed dependencies and consumers. Avoid claiming another system's authority merely because it is called from this one.

## Validation & Acceptance

State how the system proves correctness: tests, architecture gates, exact-source runtime validation, client/browser/bot acceptance, human visual review, production readiness, or other applicable evidence.

## Decisions, Open Questions & Supersession

Record unresolved design decisions and explicitly identify older design/documents this record supersedes or narrows.

---

## DOC TODO:

### Document next steps

- [ ] Reconcile all Design Source links.
- [ ] Link the current Final / canonical documentation or explicitly state that none exists yet.
- [ ] Link progression/evidence and current implementation lineage.
- [ ] Remove stale/duplicate authority links and mark superseded material clearly.
- [ ] Promote accepted design changes into the owning GitHub/Notion final documentation according to the documentation lifecycle.

### System next steps

- [ ] Record only next engineering/design/validation steps directly represented by this document.
- [ ] Keep implementation claims evidence-backed; document completion does not imply system completion.
- [ ] Remove completed items once they are reflected in final/progression/evidence documentation.

## `DOC TODO:` Rules

Every maintained Tavall system document ends with a `DOC TODO:` section.

- The section is the document's maintenance handoff, not a second unsorted product backlog.
- Separate **Document next steps** from **System next steps**.
- Document TODOs cover reconciliation, missing links, supersession, promotion, missing validation descriptions, or other work needed to make the document accurate and authoritative.
- System TODOs contain only work directly represented by the document and must not imply approval or implementation.
- Completed items should move into the appropriate final/progression/evidence content and then be removed from the TODO list.
- An accepted `FINAL` contract still carries the footer, but it must not become a stealth backlog of unapproved future behavior. If no document work remains, state that no document TODOs are open and direct future design changes into a new design/draft lineage. Implementation progress belongs in progression/evidence unless it changes the accepted contract.
