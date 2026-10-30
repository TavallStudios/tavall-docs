# Tavall Product Design Standards

> **Status:** Active, accepted organization-wide product-design policy  
> **Scope:** Tavall products, games, platforms, services, marketplaces, content tools, and developer-facing products  
> **Authority:** Cross-product value design, packaging, monetization, and common experience principles; specialist design systems retain product-specific visual and implementation rules.  
> **Owning location:** `TavallStudios/tavall-docs/docs/quality/PRODUCT_DESIGN_STANDARDS.md`  
> **Decision date:** October 11, 2026 (PDT)

## Purpose and Authority

Build products that people can meaningfully use for free, then sell compelling **adjacent value** around the product. Treat access and adoption as the engine of the ecosystem, not a paid preview of a deliberately crippled experience.

This is the default for new Tavall offerings and a review standard for existing offerings. It is not a promise of unlimited, cost-free compute or a mandate to run an insolvent service. Every exception needs explicit product-level reasoning, cost evidence, and a documented alternative.

The shared product standard owns *why the product creates value and how users encounter value and payment*. It does **not** replace product-specific DESIGN/PRODUCT/USER EXPERIENCE contracts, Tavall Forge's web implementation/tokens, Tavall MC's visual/naming rules, `WEB_ARCHITECTURE.md`, or `DOCUMENTATION_STANDARDS.md`.

## 1. Free Product First

1. **Start with a genuinely useful free core.** A user should be able to achieve the primary product outcome without buying anything. No artificial broken workflows or intentionally poor experiences.
2. **Monetize what surrounds the core.** Sell optional convenience, service, support, premium personalization, commerce, physical/digital goods, distribution, collaboration, managed work, meaningful enhancements, or clearly valuable adjacent products. An upsell must stand on its own.
3. **Prefer scale and trust to premature conversion.** Design a free experience worth recommending. Paid revenue should grow from genuine value, not coercion, dark patterns, or anxiety.
4. **Do not hide ordinary usability behind payment.** Baseline clarity, safety, accessibility, correctness, data ownership, and recovery are not luxury features.
5. **Make the paid offer honest.** Show price, duration, renewal, charges, entitlements, limits, and cancellation/fulfillment terms before commitment. Never fabricate adoption, demand, scarcity, performance, or savings.

### No Manufactured Friction

**Never create a worse product on purpose so payment becomes the escape hatch.** Tavall must not intentionally add delay, extra steps, degraded interoperability, awkward export or migration paths, reduced reliability, artificial cooldowns, needless setup, or other avoidable inconvenience whose primary purpose is to pressure users into upgrading.

- Paid tiers must win by adding **real value**: additional capability, economically meaningful capacity, managed service, support, convenience that genuinely costs or improves the product, collaboration, distribution, or other clearly beneficial extras.
- Do not remove ordinary usability from a product merely so it can be sold back as relief. If Tavall can make a common workflow materially simpler, faster, or more interoperable at negligible marginal cost, the default should be to improve the product rather than preserve friction for conversion.
- Real constraints are allowed when they are real: compute, storage, bandwidth, third-party fees, abuse prevention, safety, legal/platform rules, operational capacity, or other evidenced costs. Make them transparent and proportionate to the underlying constraint.
- Pricing and packaging may create differentiated tiers; **intentional user pain may not be the differentiation strategy**.
- A monetization review should be suspicious of any proposal whose strongest upgrade pitch is effectively, “the paid tier stops Tavall from inconveniencing you.”

This principle applies across free and paid plans. Existing customers must not be deliberately inconvenienced to manufacture demand for a higher tier.

### Cost constraint: limit users before product quantity

If a meaningful free core cannot sustainably serve everyone, first evaluate **limiting how many users can access it** (capacity-based cohorts, admission queues, invite waves, account/seat allocation, or regional rollout), **rather than restricting how much of the core product each admitted user can meaningfully use or own**.

- Protect the complete core experience for admitted users. Prefer 500 users getting a useful product over 50,000 users each receiving a demo that barely functions.
- Make capacity limits transparent, fair, measurable, reversible, and based on actual resource budgets. No fake waitlists or invented scarcity.
- Admission is different from a hidden paywall: paid priority may not compromise fairness, safety, or advertised free entitlements; product-specific policy must review any paid-access exception.
- Per-user fair-use and abuse limits remain legitimate when required by real marginal cost, legal/platform constraints, or system safety. **Do not** promise unlimited expensive inference, storage, networking, or third-party API calls.
- Revisit access limits as unit economics and infrastructure improve. Expand the audience before weakening the free core.
- If even bounded admission is unaffordable, document the economics and choose a narrower free product or a transparent paid service instead of disguising an unsustainable promise as policy.

### Offer design examples (illustrative, not live SKUs)

- **Content tooling:** free usable clipping/editing and publishing workflows; paid managed editing, premium production assistance, brand services, or clearly costed high-compute options.
- **Games:** free meaningful gameplay and fair competition; sell aesthetic identity, cosmetics, supporter benefits, direct-value goods, and voluntary services. Product-specific rules govern any progression/collection effects; no paid competitive dominance.
- **Developer/cloud tooling:** free useful workflow within economically justified access; paid managed hosting, priority support, reserved capacity, enterprise operations, and services with measurable benefit.
- **Marketplaces:** free meaningful participation where viable; transparent optional promoted services or fulfillment fees, never deceptive ranking or hidden charges.

## 2. Common Product Experience Standards

- **Clarity before spectacle:** state the product, the immediate outcome, and the next action without making users decode internal architecture.
- **One obvious primary action** on a surface; secondary actions are discoverable but subordinate.
- **Dense but readable:** compact, high-information typography and layout with progressive disclosure; never sacrifice accessibility or comprehension to density.
- **Consequence-first commitment:** purchases, permissions, publishing, destructive actions, and durable changes show the specific result, cost, scope, and reversibility before confirmation.
- **Fast path to first value:** reduce setup friction; treat login, account linking, integrations, and activation as deliberate transitions. Do not force unnecessary work merely to inflate engagement.
- **Truthful proof:** show real demos, live status, sourced claims, or clearly labeled examples. Do not invent testimonials, customer counts, metrics, prices, deployment state, or product readiness.
- **User control and recovery:** clear opt-in/opt-out, permission boundaries, accessible responsive behavior, errors that explain next steps, and safe undo/recovery when feasible.
- **Coherent cross-surface identity:** a product feels like itself across web, games, desktop, mobile, Discord, and account/commerce surfaces; reuse shared identity/navigation patterns instead of creating unrelated brands.
- **Test the actual UI:** review real renders at desktop/mobile sizes, accessibility/reduced motion, and full primary + failure workflows. Record A/B/C decisions and accepted/rejected rationale rather than an untraceable visual preference.

These are product/experience invariants. Tavall Forge, Tavall MC, and other owning design systems control their exact tokens, components, CSS, naming, composition, and surface-specific visual implementation.

## 3. Fairness, Trust, and Revenue Boundaries

- Do not design bait-and-switch free tiers, involuntary subscriptions, coerced urgency, confusing cancellations, or intentionally weakened unpaid experiences.
- No paid randomized rewards, gambling-style monetization, misleading expected outcomes, or pay-to-win competitive advantages in Tavall-owned games. Any narrower accepted product policy may be stricter.
- When evaluating promotions/affiliate campaigns, apply the personal-outcome test: **Would we be comfortable if someone we cared about acted on this promotion and lost money or suffered the downside?** Review campaign-specific claims, disclosure, legal/platform requirements, and harm; reject offers that fail this test.
- Do not treat growth metrics as permission to compromise safety, privacy, accessibility, or informed consent.

## 4. Product Review and Exceptions

Before finalizing a PRODUCT or USER EXPERIENCE design, answer:

1. What is the complete, usable **free** outcome?
2. What compelling **adjacent paid value** exists, and why would someone choose it voluntarily?
3. What are estimated incremental costs per admitted user (storage, compute, inference, bandwidth, support, third-party fees)?
4. If costs constrain access, why is the chosen **user/capacity limit** preferable to restricting product quantity or core capability?
5. Which fairness, disclosure, accessibility, privacy, abuse, and safety limits apply?
6. What proves the experience and commercial claims, and what is merely proposed?
7. What metric/evidence would trigger expansion of free access or revision of the model?

Any departure from free-first, or choice to impose restrictive product-quantity caps first, belongs in the product's owning `PRODUCT` document with cost/evidence, impact on first value, alternatives considered, review date, and owner. It must not be silently imposed through implementation.

## 5. Migration and Ownership of Existing Standards

This document **consolidates cross-product policy**, not all implementation specifications into one massive file. Migrate *shared* product design rules here; replace duplicate general rule text in narrower documents with a link. Retain context-specific rules under their canonical systems, linked from this hub. Do not delete historical decisions, design test results, source evidence, or distinctive per-product variants.

| Existing authority | What remains owned there | Relationship to this standard |
| --- | --- | --- |
| [Tavall Forge Design System](https://github.com/TavallStudios/tavall-web/blob/main/docs/design/TAVALL_FORGE_DESIGN_SYSTEM.md) ([Notion](https://app.notion.com/p/3ee38458ddfd817a8345e37f248b7668)) | Shared Tavall Web visual system, typography floors, tokens, components, chosen A/B/C direction | Implements these shared principles for web; retained as specialist DESIGN |
| [Tavall MC Visual, UI & Naming](https://app.notion.com/p/3dc38458ddfd81b08316c045cd89c4b4) | Tavall MC identity, palette, semantic Minecraft colors, naming, player-facing design | Retained as specialist product authority |
| [Tavall Web Architecture](WEB_ARCHITECTURE.md) | Typed frontend/backend routes, endpoint ownership, network/access architecture | Engineering authority, not duplicated as product UI policy |
| [Documentation Standards](DOCUMENTATION_STANDARDS.md) and [Document Types](DOCUMENT_TYPES.md) | Canonical authoring, design/technical lifecycle, dual-surface rules | Governs this document's lifecycle and every product-specific DESIGN |
| Product-specific `PRODUCT`, `USER EXPERIENCE`, and `DESIGN` documents | Offers, safety boundaries, journeys, interactions, accepted implementation contracts | Specialize these cross-product defaults; link back instead of copying |

The [PRODUCT document template](PRODUCT_DOCUMENT_TEMPLATE.md) must route future monetization decisions here. Keep separate actual implementation/deployment evidence in PROGRESSION/Deployment records; designed intent is not a launched feature.

## Final Rules Summary

**Free core first. Sell compelling adjacent value. Never manufacture friction to force an upgrade. If scale is unaffordable, prioritize limiting admitted users over limiting the amount of core product they receive. Prove the economics. Design for trust, legibility, fairness, and consistency. Keep specialized design authority with its owning product.**

## DOC TODO:

### Document next steps

- [ ] Audit existing product-specific PRODUCT/USER EXPERIENCE/DESIGN documents for duplicated global standards and replace only duplicated prose with links, preserving unique rules and history.
- [ ] Reconcile each discovered design-standard source on Notion/GitHub and record any migration/supersession explicitly.
- [ ] Add per-product cost/admission/offer evidence as products mature; do not invent commercial readiness.

### System next steps

- [ ] Apply free-first/capacity-first review to new or materially redesigned Tavall product offers.

## Documentation Update State

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | 1:1 | `TavallStudios/tavall-docs/docs/quality/PRODUCT_DESIGN_STANDARDS.md` | 2026-10-11 | New canonical shared policy |
| Notion | 1:1 | Tavall / Tavall Product Design Standards | 2026-10-11 | Same policy mirrored in Notion |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-11 8:22 PM PDT | GitHub + Notion | CREATED | Tavall Product Design Standards | Shared design principles dispersed among specialized product/design records | User decision, 2026-10-11 | Established free-first + user-capacity-before-product-quantity policy, shared UX rules, source-owner migration index. |\n| 2026-10-30 | GitHub | UPDATED | Tavall Product Design Standards | Same path | User decision, 2026-10-30 | Added explicit No Manufactured Friction principle: upgrades must earn conversion through real added value, not intentionally degraded UX or avoidable inconvenience. |
