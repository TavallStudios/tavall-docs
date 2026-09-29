# Tavall Notion System Record Template — Compatibility Entry

> **Status:** Compatibility path  
> **Current document type:** `GENERAL`

This filename is retained so existing links do not break.

New GENERAL records should use [GENERAL_DOCUMENT_TEMPLATE.md](GENERAL_DOCUMENT_TEMPLATE.md).

The complete Tavall document-type model is defined in [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md), including:

- `GENERAL`
- `ARTICLE`
- `PRODUCT`
- `USER EXPERIENCE`
- Design
- Technical
- `PROGRESSION`
- Deployment

GENERAL is Notion-only by default. Notion is a documentation surface, not a separate documentation type.

Every real source/build module with an independent responsibility boundary has its own module-scoped PROGRESSION document. Aggregate systems use system-scoped PROGRESSION when cross-module/system state is meaningful. See [PROGRESSION_DOCUMENT_TEMPLATE.md](PROGRESSION_DOCUMENT_TEMPLATE.md).

## DOC TODO:

### Document next steps

- [ ] Remove this compatibility entry only after inbound references have migrated to `GENERAL_DOCUMENT_TEMPLATE.md`.

### System next steps

- No system implementation work is owned by this compatibility document.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md` | 2026-09-27 3:03 PM PDT | Direct docs-only update to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-27 3:03 PM PDT | Compatibility entry only; GENERAL instances are Notion-only by default. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 3:03 PM PDT | GitHub | `UPDATED` | `TavallStudios/tavall-docs/docs/quality/NOTION_SYSTEM_DESIGN_RECORD_TEMPLATE.md` | Same path | Direct docs-only update to `main`. | Aligned compatibility wording with GENERAL surface rules, PROGRESSION scopes, Deployment, and required footer metadata. |

</details>
