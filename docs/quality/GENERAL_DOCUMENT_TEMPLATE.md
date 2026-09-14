# Tavall GENERAL Document Template

> **Document type:** `GENERAL`  
> **Purpose:** Readable, bursty, high-information overview of one Tavall product/system.

A GENERAL document should let a new reader understand the product/system, why it matters, what makes it distinct, how its major pieces fit together, and where to go deeper in roughly five minutes.

It should read like a strong product overview, not an architecture questionnaire.

## Document Identity

- **System / Product:** TODO
- **Status:** Idea / Designing / Building / Validating / Active / Parked
- **Owning Product / Platform:** TODO
- **Primary Repository / Runtime:** TODO
- **Last Reconciled:** TODO

## The Product / System

Open with the strongest understandable description of what this thing is.

> **One-line promise:** TODO

Use short, high-information paragraphs. Explain the product/system in human language before introducing implementation vocabulary.

## The Gap

What is broken, missing, confusing, expensive, fragmented, unfair, slow, or otherwise worth solving?

Explain the problem before dumping features.

## The Bet

What does Tavall believe can be done differently or better?

State the crisp product/system thesis.

## What Makes It Different

Use readable capability/value bursts.

### TODO capability / differentiator

Explain what it does and why somebody cares.

### TODO capability / differentiator

Explain what it does and why somebody cares.

### TODO capability / differentiator

Explain what it does and why somebody cares.

## How It Fits Together

Describe the major products, systems, surfaces, or actors and how they compose into one coherent experience.

Use a diagram when relationships matter, but keep the prose understandable without the diagram.

## Who It Is For

Name the important user/customer/operator/partner groups at a high level.

Do not turn this into the full USER EXPERIENCE document.

## What It Is Not

State important boundaries and misconceptions explicitly.

This is especially useful when the product/system can be confused with an adjacent Tavall system, generic category, or older architecture.

## Current Direction

Explain what is live, being built, designed, intentionally unresolved, or retired.

Do not market designed behavior as shipped behavior.

## Product / Business Snapshot

If the system sells or should sell something, summarize its commercial role in a few readable lines and link PRODUCT.

Otherwise state `N/A`.

## Experience Snapshot

Summarize the most important user experience goals and user types. Link USER EXPERIENCE for detailed journeys.

## Key Arguments & Explainers

Link ARTICLEs that explain important reasoning.

- TODO

## Documentation

### Design

- TODO — current Design Draft/Final and lifecycle state.

### Technical

- TODO — current Technical Draft/Final and lifecycle state.

### PRODUCT

- TODO / N/A

### USER EXPERIENCE

- TODO / N/A

### ARTICLEs

- TODO / N/A

### Progression / Evidence

- TODO

### Implementation

- TODO repository/module/PR/runtime lineage

If one existing combined Tech + Design Final currently owns both detailed contracts, link it under both Design and Technical until there is a material reason to split it.

## The Short Version

End with the few sentences or bullets somebody should remember after closing the page.

---

## DOC TODO:

### Document next steps

- [ ] Keep the product/system promise and Current Direction accurate.
- [ ] Link current Design and Technical documents.
- [ ] Link PRODUCT, USER EXPERIENCE, and important ARTICLEs where applicable.
- [ ] Link progression/evidence and implementation lineage.
- [ ] Remove stale/superseded claims instead of letting GENERAL become a museum.

### System next steps

- [ ] Record only major next system steps useful at GENERAL altitude; detailed implementation work belongs in Design/Technical/Progression/task tracking.
