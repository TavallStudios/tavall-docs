# <PRODUCT OR SURFACE NAME> — DESIGN

> **Document Type:** `DESIGN`  
> **Scope:** `PRODUCT` / `SURFACE` / `SYSTEM EXPERIENCE`  
> **Lifecycle:** `FINAL_DRAFT` / `FINAL_DRAFT_NHV` / `FINAL`  
> **Status:** Exploring / Designing / Validating / Accepted / Superseded  
> **Owning Product / Platform:** TODO  
> **Owning GENERAL:** TODO / N/A  
> **USER EXPERIENCE Document:** TODO / N/A  
> **TECHNICAL DESIGN Document:** TODO / N/A  
> **Progression Document:** TODO / N/A

DESIGN defines the accepted or proposed **visual direction, composition, interaction feel, motion, spatial hierarchy, identity, and intended vibe** of a product or surface.

It tells implementation what experience and presentation must be preserved without becoming the authority for module boundaries, class structure, dependency construction, persistence, runtime ownership, or implementation mechanics. Those belong in `TECHNICAL DESIGN`.

Every maintained DESIGN document is one logical **1:1 GitHub ↔ Notion** document. Surface-native formatting may differ, but the substantive contract, lifecycle, scope, and status must remain equivalent.

## About

Describe the product/surface and the intended experience in a few high-information paragraphs.

- What should this feel like?
- What should a person immediately understand?
- What visual or interaction problem are we solving?
- Which existing Tavall/product identity must it inherit or intentionally break from?

## Design Intent

### Core feeling

- TODO

### Visual thesis

- TODO

### Interaction thesis

- TODO

### Non-goals

- TODO

## References & Direction

Capture relevant screenshots, references, mood boards, products, games, sites, UI patterns, physical references, or other inspiration.

For each reference, state **what is being borrowed** and **what is not**. A pile of screenshots with no reasoning is just digital hoarding with better lighting.

## Visual Language

Document only what materially defines the direction:

- color behavior and contrast;
- typography hierarchy;
- spacing/density;
- shape language;
- borders, depth, shadows, texture, materials;
- iconography/illustration/photo treatment;
- data visualization style;
- environmental/world/build style when applicable.

Link canonical brand/design-system authority instead of copying it wholesale.

## Composition & Hierarchy

Describe page/screen/world composition, dominant areas, information hierarchy, responsive behavior, and how attention should move through the surface.

Use actual diagrams, annotated images, wireframes, or prototypes when relationships are materially visual.

## Interaction & Motion

Define important interaction behavior:

- hover/focus/pressed/selected states;
- transitions and animation intent;
- loading/progress behavior;
- direct manipulation;
- navigation feel;
- audio/haptic/game feedback where relevant;
- interruption/error/recovery presentation.

Do not specify backend orchestration here unless a technical constraint must be preserved to achieve the experience. Link TECHNICAL DESIGN for that contract.

## Component / Surface Inventory

| Surface / Component | Purpose | Visual / interaction contract | Reuse / variation |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

## Responsive / Platform Variants

Describe meaningful differences across desktop, mobile, game client, web, embedded surfaces, accessibility modes, or other platforms.

## Accessibility & Human Constraints

Record visual, motion, input, contrast, readability, sensory, and accessibility constraints that materially affect the design.

## States & Edge Cases

Show or describe important states such as:

- empty;
- loading;
- success;
- error;
- disabled/unavailable;
- partially configured;
- offline/degraded;
- first-time vs returning;
- permission-restricted.

## Design Acceptance

Define what must be visually or interactively accepted before the design is considered implemented.

Possible evidence includes screenshots, prototypes, browser/game captures, visual regression, recorded interaction, accessibility checks, and human review.

Implementation evidence itself belongs in PROGRESSION.

## Design Decisions & Open Questions

### Accepted Decisions

- TODO

### Open Questions

- TODO

Remove resolved questions or convert them into explicit accepted rules before promotion to `FINAL`.

## Documentation Relationships

### GENERAL
- TODO / N/A

### USER EXPERIENCE
- TODO / N/A

### TECHNICAL DESIGN
- TODO / N/A

### PROGRESSION
- TODO / N/A

### Deployment
- TODO / N/A

### Implementation / Design Assets
- TODO

## Final Design Rules

End with the small set of visual/interaction rules a designer, developer, builder, or reviewer must preserve.

## DOC TODO:

### Document next steps
- [ ] Keep GitHub and Notion copies synchronized 1:1.
- [ ] Keep lifecycle and scope explicit.
- [ ] Replace stale references after design evolution.
- [ ] Keep technical architecture in TECHNICAL DESIGN rather than duplicating it here.

### System next steps
- [ ] Record only design-direction work here. Architecture belongs in TECHNICAL DESIGN; implementation state belongs in PROGRESSION.

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `1:1` | TODO | TODO | TODO |
| Notion | `1:1` | TODO | TODO | TODO |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| TODO | GitHub | `CREATED` | TODO | — | TODO | Created from the canonical Tavall DESIGN template. |
| TODO | Notion | `CREATED` | TODO | — | TODO | Created as the 1:1 Notion twin. |

</details>
