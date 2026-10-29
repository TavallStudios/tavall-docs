# Tavall Technical Diagram Standards

> **Status:** Active — Agent WebMCP SVG visual language selected 2026-10-29
> **Authority:** Delegated technical-diagram presentation standard under [Tavall Documentation Standards](DOCUMENTATION_STANDARDS.md)
> **Applies to:** Architecture, module ownership, lifecycle, integration, execution-flow and safety diagrams in Tavall technical docs, READMEs and approved Notion counterparts
> **Does not own:** System architecture facts, module responsibilities, runtime state, Notion page authority, or image-generation policy

## Default Design Reference: Agent WebMCP SVG

Tavall's default **SVG visual style** is the **authored Agent WebMCP hackathon diagram system**. Do not recreate the three 2026-10-29 draft Semantic Flow / Blueprint / Capability Atlas SVGs as the default. Existing accurate diagrams are not invalid solely because they use another style; adopt this visual language on creation or intentional revision.

Source references (review the current source SVG before drawing, not only screenshots):

- [Human + Agent Operations Flow](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/human-agent-operations-flow.svg): multiple input paths converging on typed operation authority.
- [Service and Durable Job Architecture](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/service-job-architecture.svg): one inventory feeding deterministic versus reasoning-assisted work and a durable owner.
- [One Catalog, Multiple Surfaces](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/one-catalog-multiple-surfaces.svg): one canonical implementation projected to multiple interfaces.
- [Bounded Safety Model](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/bounded-safety-model.svg): permitted versus excluded capability boundaries.
- [WebMCP Registration Flow](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/webmcp-registration-flow.svg): ordered execution states and integration behavior.
- [Human-Agent Collaboration Loop](https://github.com/tjXJNOOBIE/agent-webmcp/blob/main/docs/hackathon/devpost/human-agent-collaboration-loop.svg): feedback/collaboration cycle.

These are visual design references by the user's own hackathon project; do not duplicate their product-specific labels as Tavall architectural authority.

## Visual Grammar

The source SVGs use a 1600×900 `viewBox`, dark gradient canvas from `#090B0F` to `#10151D`, and restrained panels `#111823` (`#2B3646` stroke) and `#0D141E` (`#263243` stroke). Start there for a wide architecture plate; use the **same grammar** rather than forcing every topology into 16:9.

Typography follows the source fallback chain `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`. Wide-plate reference sizes: title 60px, subtitle 27px, panel heading 30px, body 24px, supporting text 21px. Typography must be adjusted for the actual number of nodes, available panel dimensions and Notion embed size; never shrink labels into illegibility merely to preserve the reference measurements.

Reference semantic colors:
- **Main text:** `#F8FAFC`; secondary text: `#A8B3C4`.
- **Normal directed flow:** `#7DD3FC` cyan, solid stroke / matching arrow marker.
- **Alternative, conditional, or separately qualified flow:** `#A78BFA` violet, dashed, labeled with its real meaning.
- **Capability-specific emphasis:** restrained teal `#2DD4BF` / dark teal panel when the example requires emphasis, not a blanket claim that all Handlers are teal or all Services amber.

Use rounded solid cards, generous interior spacing and readable editorial labels. Arrows must visibly terminate at the correct boundary, avoid text/crossovers, and match underlying dependency or event semantics. A dashed line never means "optional" unless the diagram legend/context states that explicitly.

## Pick Topology From Meaning

The **visual language is singular; the graph topology is not**. Use the layout matching the actual facts:

| Intent | Graph topology |
| --- | --- |
| Dependency ownership or shared operation catalog | Hub with projections / directed ownership |
| Lifecycle or sequence | Directed step flow |
| Human/agent/tools convergence | Multiple inputs entering one typed owning boundary |
| Safety/permissions | Side-by-side permitted versus excluded boundary |
| Continued process or retry | Explicit cycle with state/guard labels |
| Module graph | Nested owners or directed edges, with the current module visibly **bold** and `← This Module` in module READMEs |

Avoid adding decorative layers, fictitious transport edges, extra Services, or any nodes not justified by source. Domain/module architecture remains owned by its canonical documents, not the visualization.

## Authorship and Verification

1. Read the canonical source document, the actual component ownership and one or more WebMCP SVG reference files.
2. Model real nodes, typed boundaries and edges. Specify the topology and relationship meanings **before** drawing.
3. Author editable SVG with `viewBox`, `role="img"`, `<title>`, `<desc>`, meaningful labels and safe self-contained vector styles. Use stable IDs for gradients and markers.
4. Inspect the SVG at native size and at the expected Notion/readme embed width; check title/panel overflow, clipped labels, contrast, arrow endpoints, overlapping connectors, hidden edges and legibility.
5. Keep an accessible textual description of the architecture immediately adjacent to the diagram. The diagram must not be the sole owner of an implementation rule.
6. Store the canonical SVG/source with its owning GitHub document or suitable referenced visual artifact. When Notion requires a raster preview, render a matching PNG from **the same SVG source** and link the editable source; do not allow independent diagrams to drift.
7. Record file path, source revision, render revision, surface destination, Notion synchronization receipt and acceptance evidence. If render/Notion verification is unavailable, say **unverified**, not completed.

Notion and GitHub remain coordinated **according to the owning document's actual surface-placement rule**. Do not blanket-sync Notion-only GENERAL documents to GitHub. Do not rewrite existing Notion pages across Tavall just to roll out the new style.

## Adoption Plan

- **Selected:** Agent WebMCP visual style as default for newly authored technical diagrams.
- **Pending:** reusable SVG authoring/layout helpers and automated render/overflow/a11y checks; format-specific light-background or printable variant.
- **Pending:** redraw the [Class Role Ownership Graph](code-architecture/CLASSES.md#class-role-ownership-graph-conceptual) using verified role boundaries and this style. The existing Mermaid graph remains a source-backed structural reference, not the newly approved visual template.
- **Pending:** a real Notion embedding test and an audited GitHub/Notion asset synchronization workflow. Do not claim deployment to Notion until observed.

##### Why

The hackathon references are editorial, readable diagrams that emphasize one real control or capability boundary and faithfully depict alternatives/flows. Standardizing their **visual semantics** makes Tavall recognizable without turning different architectural questions into the same misleading row of boxes.
