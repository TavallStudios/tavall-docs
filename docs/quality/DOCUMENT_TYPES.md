# Tavall Documentation Types

> **Status:** Active  
> **Applies to:** Tavall GENERAL, ARTICLE, PRODUCT, USER EXPERIENCE, Design, Technical, Progression/Evidence, Deployment, and related documentation  
> **Purpose:** Make each document answer one kind of question well instead of forcing product explanation, reasoning, commercial strategy, UX, technical architecture, implementation evidence, and live deployment state into one giant file.

Document **type** and document **lifecycle** are separate dimensions.

## Type Map

| Type | Primary question | Authority / role |
| --- | --- | --- |
| `GENERAL` | What is this product/system? | Broad readable product/system overview and documentation map. |
| `ARTICLE` | Why do we believe or choose this? | Reasoning, argument, policy position, and explainer. |
| `PRODUCT` | How does this create and capture value? | Commercial/product operating model for systems that sell or should sell something. |
| `USER EXPERIENCE` | What is it actually like for different users? | Target journeys, archetypes, friction, outcomes, recovery, and cross-surface continuity. |
| Design | What behavior is accepted? | Detailed product/system behavior according to the current Draft/Final lifecycle. |
| Technical | How is it built and operated? | Detailed implementation/architecture contract according to the current Draft/Final lifecycle. |
| Progression / Evidence | What is actually implemented and validated? | Audited implementation state tied to source/evidence. |
| Deployment | What is deployed where now, and what deployment transitions occurred? | Current and historical deployment state for one independently deployable system tied to exact source/release/runtime evidence. |

These types are complementary. A monetizable product may legitimately have GENERAL + PRODUCT + USER EXPERIENCE + ARTICLEs + Design + Technical + Progression + Deployment. A small internal library may need only GENERAL + Design + Technical and no Deployment document at all.

## GENERAL

GENERAL is the readable product/system overview.

A reader should understand the system in roughly five minutes without needing implementation knowledge. GENERAL should be bursty, highly informative, and product-oriented.

A strong GENERAL document:

- opens with a clear product/system promise;
- explains the gap/problem before features;
- states the Tavall thesis or bet;
- presents major capabilities and differentiators in readable bursts;
- explains how the major pieces compose;
- identifies important audiences and boundaries;
- distinguishes live, being-built, designed, unresolved, and retired behavior;
- links applicable PRODUCT, USER EXPERIENCE, ARTICLE, Design, Technical, Progression/Evidence, Deployment, and implementation sources.

GENERAL is normally continuously maintained rather than promoted to a frozen Final state.

Use [GENERAL_DOCUMENT_TEMPLATE.md](GENERAL_DOCUMENT_TEMPLATE.md).

### Style reference

The Tavall PvP Notion overview, **Tavall PvP — Competitive Minecraft PvP, Built Like a Game**, is the style reference: strong product claim, problem, readable differentiators, coherent system story, honest roadmap/evidence context.

## ARTICLE

ARTICLE preserves Tavall's reasoning.

An ARTICLE normally:

1. opens with a strong claim;
2. names the real problem or conventional approach;
3. argues Tavall's position;
4. uses actual systems/evidence as support;
5. connects technical/product choices to human value;
6. distinguishes implemented, being built, and designed behavior;
7. ends with a memorable thesis.

ARTICLE is persuasive/explanatory, not a substitute for Design or Technical authority.

ARTICLEs may later feed public website copy, partner briefs, videos, social material, or other Tavall Content outputs after review.

Use [ARTICLE_DOCUMENT_TEMPLATE.md](ARTICLE_DOCUMENT_TEMPLATE.md).

### Style references

The TavallMC Product Essays & Explainers library is the canonical precedent. Strong examples include **Ping Is Gameplay — How TavallMC Routes Players Instead of Making Them Pick a Server** and **From Fight to Career — How TavallMC Builds Persistent Competitive History**.

## PRODUCT

PRODUCT exists for a system that can or should sell something: software, access, services, currency, subscriptions, marketplace inventory, paid capabilities, commerce-enabled content, or another explicit value exchange.

PRODUCT answers questions such as:

- Who are the customer, buyer, payer, provider/seller/creator, and partner?
- What is being offered and what outcome is valuable?
- How is it packaged: SKU, plan, service page, entitlement, bundle, marketplace listing, currency, subscription, usage, fee, commission, etc.?
- How does discovery → consideration → conversion → fulfillment → retention/renewal work?
- What is free, paid, earned, subsidized, bundled, or cross-sold?
- How does acquisition/distribution work?
- What are the monetization/fairness boundaries?
- How do fulfillment, support, refunds, disputes, cancellation, and reconciliation work?
- What legal/payment/provider questions remain unresolved?
- What evidence proves commercial readiness versus designed intent?

PRODUCT does not replace GENERAL. GENERAL explains the whole product/system; PRODUCT zooms into the value and commercial machine.

Not every system needs PRODUCT. A low-level internal library usually does not.

Use [PRODUCT_DOCUMENT_TEMPLATE.md](PRODUCT_DOCUMENT_TEMPLATE.md).

### Style reference

**Tavall Contractors — Product, Marketplace & Growth Operating Record** is the strongest current precedent: product thesis, customer/provider flows, marketplace surfaces, fulfillment, acquisition, monetization, evidence boundaries, and commercial priorities.

## USER EXPERIENCE

USER EXPERIENCE explains the product from the user's point of view.

It should include multiple archetypes whenever materially different motivations create different experiences. Define users by goals, behavior, experience level, constraints, and success criteria rather than decorative demographics.

Useful archetypes may include:

- first-time/new user;
- casual user;
- competitive/power user;
- progression/collector user;
- returning/lapsed user;
- creator/publisher/provider;
- buyer/customer;
- guild/team/community participant;
- admin/moderator/operator;
- developer/technical integrator for developer-facing products.

For each meaningful archetype, document:

- starting context;
- discovery/entry;
- core flow and meaningful branches;
- feedback/confidence;
- success moment;
- progression/repeat use;
- failure/interruption/recovery;
- cross-surface continuity;
- friction and guardrails.

UX docs may include journey tables, branching scenarios, screenshots, prototypes, visual references, analytics/playtest evidence, or narrative walkthroughs.

USER EXPERIENCE should tell Design, QA, and engineering what human experience must be preserved without dictating implementation internals.

Use [USER_EXPERIENCE_DOCUMENT_TEMPLATE.md](USER_EXPERIENCE_DOCUMENT_TEMPLATE.md).

### Existing source precedents

The promoted Notion records **Cross-product first-join routing and product-specific lobby identities** and **Gameplay-first progressive tutorials after product selection** are useful UX-source examples. They are not full USER EXPERIENCE documents yet, but already capture first-time vs returning behavior, product-specific journeys, skip/replay, re-entry, accessibility, and cross-product handoff concerns.

## DEPLOYMENT

Deployment is the operational record for one **independently deployable system**.

It answers:

- which deployment targets exist;
- what exact source/release/artifact is currently running at each target;
- which runtime/service identity owns that deployment;
- when the current deployment changed;
- what evidence proves the deployment event;
- what previous deploy/promote/replace/rollback/restore/disable/retire/failure events occurred.

Deployment does **not** own:

- deployment architecture or runtime design — Technical owns that contract;
- CI/CD, promotion, release, or Git policy — the owning CI/CD and Git documents own those rules;
- accepted product behavior — Design owns that contract;
- implementation completeness or validation state — Progression / Evidence owns that evidence.

The README for a deployable repository/module provides only a basic current deployment summary and links the Deployment document for the complete current and historical record.

Naming:

- use `<DEPLOYABLE_SYSTEM>_DEPLOYMENT.md` in a repository with multiple deployable systems;
- use plain `DEPLOYMENT.md` only when one deployable system is unambiguous.

Deployment History is append-only operational evidence. Replacing a deployment does not erase the previous event.

Every maintained Deployment document for a deployable Tavall system is a required **1:1 GitHub ↔ Notion** document.

Use [DEPLOYMENT_DOCUMENT_TEMPLATE.md](DEPLOYMENT_DOCUMENT_TEMPLATE.md).

## Relationship to Design, Technical, Evidence, and Deployment

GENERAL is the rendezvous point for applicable specialized docs.

```text
GENERAL
├── ARTICLE(s)             reasoning / arguments
├── PRODUCT                commercial model, when applicable
├── USER EXPERIENCE        lived user journeys, when applicable
├── Design Draft / Final   accepted behavior contract
├── Technical Draft / Final implementation/architecture contract
├── Progression / Evidence audited implementation state
└── Deployment             current + historical deployed runtime state, when applicable
```

Important authority rules:

- A persuasive ARTICLE does not override Design/Technical Final authority.
- A PRODUCT pricing or packaging idea does not silently become an entitlement or payment contract.
- A USER EXPERIENCE story does not prove implementation.
- GENERAL summarizes; it does not duplicate every specialist document.
- Accepted Design/Technical docs own their assigned contract.
- Progression/Evidence owns audited implementation state at its recorded source.
- Deployment owns actual deployed runtime/source state and deployment-event history, not implementation completeness or deployment design.

Every specialized document should backlink to its owning GENERAL document where one exists. GENERAL should link all applicable specialized docs.

## Lifecycle

Type and lifecycle are independent.

- GENERAL is normally active/continuously maintained.
- ARTICLE may be Draft / Reviewed / Published / Historical.
- PRODUCT may be Idea / Designing / Validating / Launching / Active / Retired, with explicit approval where commercial commitments require it.
- USER EXPERIENCE may be Exploring / Draft / Reviewed / Accepted / Needs Revalidation.
- Design and Technical retain the formal Draft/Final lifecycle originally defined in the early repository `DOC_DESIGN_RULES.md` lineage (Project Novus/Tavall MC `b5e690859` / `dff1d0818`) and now fully codified and superseded by [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) (Sections 3–8) and this taxonomy.
- Progression/Evidence remains evidence at a recorded source state.
- Deployment remains an active operational record while the deployable system exists; its current snapshot changes, while Deployment History remains append-only.

Existing combined Tech + Design Final documents may satisfy both Design and Technical links until there is a material reason to split them. Do not create mass rename churn merely because the taxonomy improved.

## `DOC TODO:`

All maintained documents follow the shared `DOC TODO:` maintenance-handoff contract in [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md).

## DOC TODO:

### Document next steps

- [ ] Keep templates synchronized with this taxonomy.
- [x] Reconcile the detailed Design/Technical type and lifecycle rules with the active `DOC_DESIGN_RULES.md` lineage (completed: lineage verified through commits `b5e690859`/`dff1d0818` and fully superseded by canonical `DOCUMENTATION_STANDARDS.md` and `DOCUMENT_TYPES.md`).
- [x] Add the Deployment document type and template for independently deployable systems.
- [ ] Add explicit examples/templates for additional document types only when a real recurring documentation responsibility appears.

### System next steps

- [ ] Classify existing Tavall documents by type as they are touched; avoid rename churn for healthy existing documents.
- [ ] Split mixed documents only when separation materially improves readability or authority.
- [ ] Build USER EXPERIENCE docs for major Tavall products from existing flow/onboarding/player-experience evidence.
- [ ] Add/synchronize Deployment documents as deployable modules and services are touched; do not fabricate historical deployments that cannot be evidenced.
