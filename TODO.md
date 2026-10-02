# Tavall Global TODO

> **Status:** Active  
> **Authority:** Canonical organization-wide TODO ledger  
> **Repository projections:** Every maintained TavallStudios repository exposes a bot-managed root `TODO.md` that projects only that repository's section from this file.  
> **Last updated:** 2026-10-01

This file is the single source of truth for organization-wide repository TODO work. Repository-local `TODO.md` files are generated static projections and must not become independent task ledgers.

## Projection contract

- Each maintained TavallStudios repository has one root `TODO.md`.
- The repository's own section from this document is the first substantive section rendered in that local file.
- Local projections link back to this document and carry machine-readable HTML comments describing their source, repository, managing bot, format version, last source commit, and synchronization time.
- `TavallStudios/tavall-github-bot` owns synchronization. Human edits belong here first; the bot propagates the repository slice outward.
- Empty repository sections remain explicit so absence of work is distinguishable from a missing projection.

## Repository TODOs

### `TavallStudios/CustomMinecraftServer`

_No open global TODO items currently tracked._

### `TavallStudios/HyRhythm`

_No open global TODO items currently tracked._

### `TavallStudios/MCRSpeedrun`

_No open global TODO items currently tracked._

### `TavallStudios/Tavall-Talent-and-Contractors-`

_No open global TODO items currently tracked._

### `TavallStudios/TavallContractors`

_No open global TODO items currently tracked._

### `TavallStudios/TavallCouriers`

_No open global TODO items currently tracked._

### `TavallStudios/TavallMonoRepo`

_No open global TODO items currently tracked._

### `TavallStudios/Webstore`

_No open global TODO items currently tracked._

### `TavallStudios/function-catalog`

_No open global TODO items currently tracked._

### `TavallStudios/hytale-bots`

_No open global TODO items currently tracked._

### `TavallStudios/minecraft-bot`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-ai`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-ai-memory`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-analytics`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-cache`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-ci`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-cloud`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-concurrency`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-content`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-content-tools`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-custom-enum-java`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-database`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-di`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-discord`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-docs`

- [ ] 2026-10-01 — Keep the global TODO repository inventory synchronized as TavallStudios repositories are created, renamed, archived, or retired.

### `TavallStudios/tavall-docs-private`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-eventbus`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-github-bot`

- [ ] 2026-10-01 — Implement canonical repository TODO projection management.
  - Watch `TavallStudios/tavall-docs/TODO.md` and repository inventory changes.
  - Parse each repository's section and render it as the first substantive section of that repository's root `TODO.md`.
  - Preserve canonical generated HTML metadata comments including source, repository, managing bot, projection format version, source commit, and synchronization timestamp.
  - Open or update one deterministic synchronization PR targeting `main` per affected repository instead of creating duplicate PRs.
  - Reconcile repository creation, rename, archive, and reactivation events.
  - Never treat a local generated projection as authority or ingest local edits back into the global TODO automatically.
  - Validate that the rendered repository slice exactly matches the authoritative global section before marking synchronization complete.

### `TavallStudios/tavall-hytale-resource-game`

#### Companion System Future Work

- [ ] 2026-10-01 — Add custom companion skins and cosmetic rarity rules.
- [ ] 2026-10-01 — Add full companion duel animations and richer cast particles.
- [ ] 2026-10-01 — Add advanced morale event chains, bonding, voice, and emote hooks.
- [ ] 2026-10-01 — Add battle replay companion commentary.
- [ ] 2026-10-01 — Add full wall section visuals for assigned companions.
- [ ] 2026-10-01 — Expand companion injury and recovery depth beyond first-pass status fields.
- [ ] 2026-10-01 — Add companion behavior hooks driven by the canonical Kingdom Clock.
- [ ] 2026-10-01 — Add companion and citizen/job interaction hooks.
- [ ] 2026-10-01 — Add companion quests, party training, and realm-specific skills.

### `TavallStudios/tavall-java-tools`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-java-utils`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-logging`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-mc`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-mc-bot-testing`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-mc-paper`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-minecraft-framework`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-open-harness`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-rating-glicko2`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-reflection`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-registry`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-roblox`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-scheduler`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-test-suite-tools`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-account`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-blog`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-cloud`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-commerce`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-content`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-contractors`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-discord`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-mc`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-mcp`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-web-workflows`

_No open global TODO items currently tracked._

### `TavallStudios/tavall-workflows`

_No open global TODO items currently tracked._
