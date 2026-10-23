# Tavall Work Graph — Legacy TODO Import Audit (Wave 1)

> **Status:** Source preservation + first 14 issues created; bulk import NOT completed  
> **Date:** 2026-10-22  
> **Immutable source:** [Tavall Docs TODO at 7022d23](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md)  
> **Owner:** [Tavall GitHub Bot #9](https://github.com/TavallStudios/tavall-github-bot/issues/9)  
> **Authority:** Existing mapped issues for their tasks; original TODO for unmatched items. This is a *one-time migration audit*, not an additional issue status ledger.

## Snapshot and safeguards

| Metric | Observed |
| --- | ---: |
| Legacy tasks | 152 |
| Unchecked | 150 |
| Checked | 2 |
| Mapped to newly created canonical owner Issues | 14 |
| Unmapped, requiring dedup/owner/acceptance review | 136 |
| Previously requested Hytale exclusion (untouched, within unmapped) | 10 |
| Remaining in-scope items to triage after exclusion | 126 |
| Previously discovered open org GitHub Issues (snapshot before wave) | 63 |

The original body, children and lineage are retained at the immutable source SHA. GitHub Issues created in this wave carry that exact commit + line in a metadata comment. Do not interpret an issue's existence as source implementation, tests, or runtime deployment.

## Wave 1: source-to-issue map

| Repo / owner | Legacy source | Canonical issue | Work summary |
| --- | --- | --- | --- |
| `TavallContractors` | [L52](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L52) | [#9](https://github.com/TavallStudios/TavallContractors/issues/9) | Decide legacy Contractors executable ownership before changing the spring-webview RUNTIME module's noncompliant name. |
| `function-catalog` | [L86](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L86) | [#39](https://github.com/TavallStudios/function-catalog/issues/39) | Bring the independently executable mcp-server Gradle module into Tavall naming as tavall-function-catalog-mcp-runtime, preserving the function-catalog repository name. |
| `tavall-ai` | [L117](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L117) | [#74](https://github.com/TavallStudios/tavall-ai/issues/74) | Normalize Tavall AI module types and suffixes without treating agents or non-process capabilities as independent runtimes. |
| `tavall-ai-memory` | [L137](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L137) | [#4](https://github.com/TavallStudios/tavall-ai-memory/issues/4) | Select the canonical primary type and module/artifact name for the dedicated memory owner before migrating tavall-ai-runtime-memory. |
| `tavall-analytics` | [L154](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L154) | [#18](https://github.com/TavallStudios/tavall-analytics/issues/18) | Introduce explicit SYSTEM names and host-owned collector lifecycle in Analytics, replacing legacy blanket LIBRARY labels through reviewed slices. |
| `tavall-cache` | [L173](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L173) | [#16](https://github.com/TavallStudios/tavall-cache/issues/16) | Classify the current abstract-cache-system contract module and abstract-cache-semantic owner before applying suffixes. |
| `tavall-cloud` | [L223](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L223) | [#460](https://github.com/TavallStudios/tavall-cloud/issues/460) | Finish source-to-module classification and naming cutover for Cloud CONTROL and Node Agent without splitting the unified Cloud distribution. |
| `tavall-content` | [L323](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L323) | [#72](https://github.com/TavallStudios/tavall-content/issues/72) | Rename the verified headless tavall-content-render-worker RUNTIME module to a suffix-compliant identity such as tavall-content-render-worker-runtime, without moving the Tavall Content repository. |
| `tavall-database` | [L373](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L373) | [#31](https://github.com/TavallStudios/tavall-database/issues/31) | Reconcile Database's legacy primary provider/library classifications against canonical module types before any -system migration. |
| `tavall-discord` | [L392](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L392) | [#10](https://github.com/TavallStudios/tavall-discord/issues/10) | Resolve Discord's in-process lifecycle module primary type and apply suffix naming only after classification. |
| `tavall-docs` | [L405](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L405) | [#78](https://github.com/TavallStudios/tavall-docs/issues/78) | Enforce the canonical -system / -runtime suffix rule for **actual** modules, excluding parent repositories, organizational aggregates, APPLICATIONs and secondary-role labels. |
| `tavall-mc` | [L508](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L508) | [#360](https://github.com/TavallStudios/tavall-mc/issues/360) | Audit actual primary types before applying suffix naming to Novus product modules and future gameplay SYSTEM extractions. |
| `tavall-test-suite-tools` | [L642](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L642) | [#25](https://github.com/TavallStudios/tavall-test-suite-tools/issues/25) | Add canonical module-name/type validation to the shared architecture test rules after existing source/module inventory is reconciled. |
| `tavall-web` | [L655](https://github.com/TavallStudios/tavall-docs/blob/7022d23f9be07ddd7fd0539ae9e928a0550e1f9a/TODO.md#L655) | [#77](https://github.com/TavallStudios/tavall-web/issues/77) | Define only evidence-backed Account/Commerce fan-in SYSTEMs with compliant module names, while retaining tavall-web-app as APPLICATION. |

## Owner inventory for remaining triage

These are **counts only**. The immutable TODO retains task text, all source constraints and owner-specific documentation; there is no copied second backlog here.

| Owning repository | Source unchecked | Linked to issues | Unmapped |
| --- | ---: | ---: | ---: |
| `CustomMinecraftServer` | 1 | 0 | 1 |
| `HyRhythm` | 1 | 0 | 1 |
| `MCRSpeedrun` | 1 | 0 | 1 |
| `TavallContractors` | 2 | 1 | 1 |
| `TavallCouriers` | 1 | 0 | 1 |
| `Webstore` | 1 | 0 | 1 |
| `function-catalog` | 4 | 1 | 3 |
| `hytale-bots` | 1 | 0 | 1 |
| `minecraft-bot` | 1 | 0 | 1 |
| `tavall-ai` | 5 | 1 | 4 |
| `tavall-ai-memory` | 4 | 1 | 3 |
| `tavall-analytics` | 4 | 1 | 3 |
| `tavall-cache` | 3 | 1 | 2 |
| `tavall-ci` | 7 | 0 | 7 |
| `tavall-cloud` | 14 | 1 | 13 |
| `tavall-concurrency` | 1 | 0 | 1 |
| `tavall-content` | 15 | 1 | 14 |
| `tavall-content-tools` | 1 | 0 | 1 |
| `tavall-custom-enum-java` | 1 | 0 | 1 |
| `tavall-database` | 3 | 1 | 2 |
| `tavall-di` | 1 | 0 | 1 |
| `tavall-discord` | 2 | 1 | 1 |
| `tavall-docs` | 7 | 1 | 6 |
| `tavall-eventbus` | 1 | 0 | 1 |
| `tavall-github-bot` | 4 | 0 | 4 |
| `tavall-hytale-resource-game` | 9 | 0 | 9 |
| `tavall-java-tools` | 1 | 0 | 1 |
| `tavall-java-utils` | 1 | 0 | 1 |
| `tavall-jdk` | 3 | 0 | 3 |
| `tavall-logging` | 2 | 0 | 2 |
| `tavall-mc` | 13 | 1 | 12 |
| `tavall-mc-bot-testing` | 2 | 0 | 2 |
| `tavall-mc-paper` | 2 | 0 | 2 |
| `tavall-minecraft-framework` | 1 | 0 | 1 |
| `tavall-open-harness` | 3 | 0 | 3 |
| `tavall-rating-glicko2` | 1 | 0 | 1 |
| `tavall-reflection` | 1 | 0 | 1 |
| `tavall-registry` | 2 | 0 | 2 |
| `tavall-roblox` | 1 | 0 | 1 |
| `tavall-scheduler` | 1 | 0 | 1 |
| `tavall-test-suite-tools` | 2 | 1 | 1 |
| `tavall-web` | 8 | 1 | 7 |
| `tavall-web-account` | 1 | 0 | 1 |
| `tavall-web-blog` | 1 | 0 | 1 |
| `tavall-web-cloud` | 1 | 0 | 1 |
| `tavall-web-commerce` | 1 | 0 | 1 |
| `tavall-web-content` | 3 | 0 | 3 |
| `tavall-web-contractors` | 1 | 0 | 1 |
| `tavall-web-mc` | 2 | 0 | 2 |
| `tavall-web-mcp` | 1 | 0 | 1 |

## Next wave sequencing

1. Check all existing **open and closed** owner-repository issues and PRs, not just title similarity; map matches, skip verified DONE, and review ambiguous overlaps. Prioritize Cloud, Content, MC, Web, AI, CI and deployment blockers.
2. For remaining actionable tasks, create issues with source provenance and real acceptance gates. Defer ideas that aren't actionable; preserve excluded domains untouched.
3. Implement and test Bot dry-run intake and stable fingerprint reconciliation; re-run same source and verify it creates zero duplicates.
4. Build and verify Projects board access, then update issue workflow fields; no Project row is considered a canonical task.
5. Only after complete verified coverage and a deterministic projection pilot may the Bot replace the legacy source/projection policy. Preserve this snapshot and its Git history.

**Do not use this report as a live progress tracker.** Issue URLs own work state once linked; the global TODO remains a transition document for all still-unmapped entries.
