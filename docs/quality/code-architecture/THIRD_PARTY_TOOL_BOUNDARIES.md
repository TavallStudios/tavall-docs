# Third-Party Tool Boundaries

> **Status:** Active  
> **Authority:** Binding specialization of Tavall Code Architecture  
> **Applies to:** Third-party binaries, CLIs, SDKs, MCP servers, services, runtimes, native libraries, and reusable external tool integrations

Third-party technology may implement a Tavall capability, but it does not define Tavall's application architecture. Tavall owns the semantic boundary, lifecycle, configuration, failure model, and observability that consumers depend on.

## Canonical Wrapper Rule

Every reusable third-party tool integration is owned behind a Tavall module/artifact named `tavall-<tool>`.

Examples:

| Upstream | Canonical Tavall wrapper |
| --- | --- |
| OpenCV | `tavall-open-cv` |
| FFmpeg / FFprobe | `tavall-ffmpeg` |
| Playwright | `tavall-playwright` |
| Chromium | `tavall-chromium` |
| HyperFrames | `tavall-hyperframes` |
| Remotion | `tavall-remotion` |
| Animotion MCP | `tavall-animotion` |

The wrapper may live in an umbrella repository, but the module/artifact is still independently named and owned. Do not hide reusable vendor integrations inside a generic `tools`, `common`, `util`, product, or application module.

## What The Wrapper Owns

A Tavall wrapper owns all upstream-specific mechanics needed by ordinary consumers, including where applicable:

- binary/library/service discovery and supported-version checks;
- executable paths and process construction;
- SDK/native binding initialization;
- vendor-specific command arguments, request envelopes, protocol messages, and MCP tool names;
- environment/configuration mapping;
- capability discovery;
- lifecycle/start/stop/cleanup;
- timeouts, cancellation, retries, and process exit handling;
- stderr/stdout or remote-error translation into typed Tavall results/exceptions;
- metrics, logs, tracing, and provenance needed to identify the provider actually used;
- security restrictions around raw commands, scripts, paths, or untrusted parameters.

Consumers should be able to express the operation they need without learning the upstream invocation syntax.

## Consumer Rule

Product, domain, controller, workflow, and orchestration code consumes Tavall semantics. It must not directly:

- launch third-party executables;
- construct raw vendor CLI argument lists;
- import vendor SDK/native types outside the owning wrapper boundary;
- call vendor HTTP endpoints or vendor MCP tools;
- read vendor-specific environment variables;
- depend on installation paths;
- parse vendor-specific stdout/stderr formats.

If the required semantic operation is missing, extend the Tavall wrapper rather than bypassing it downstream.

## API And Provider Shape

Use the narrowest honest shape:

1. If the wrapper is a simple in-process capability, its typed Java API may be the canonical boundary.
2. If multiple implementations/providers exist, keep the caller-facing contract provider-neutral and put vendor mechanics in the `tavall-<tool>` provider module.
3. If the tool runs in another process/runtime, expose a typed integration client or Tavall-owned process boundary rather than leaking transport details.
4. If Spring wiring is needed, keep Spring-specific composition in the appropriate sibling Spring/application module. Do not contaminate a pure reusable API with framework ownership.
5. CLI, HTTP, MCP, and UI adapters project the same Tavall capability. They do not become alternate business authorities.

## Natural-Language And Agent Use

Agents route natural-language intent to Tavall capabilities, not directly to vendor tools. An agent may select `tavall-open-cv`, `tavall-ffmpeg`, or another wrapper because the requested operation requires that capability, but its instructions must describe the Tavall-owned operation and stage ordering.

This keeps prompts stable when an upstream executable, model, service, transport, or provider changes.

## Media Example

A video workflow should normally route through owned stages:

```text
natural-language request
  -> Tavall video workflow
  -> tavall-ffmpeg: probe/decode/timing/audio
  -> tavall-open-cv: frame sampling/scene/motion/tracking when visual analysis is required
  -> Tavall AI: semantic reasoning only when required, preferably after candidate reduction
  -> Tavall composition providers when requested
  -> tavall-ffmpeg: final encode/mux/audio/QC
```

Cheap deterministic operations such as probe, trim, remux, or transcode do not invoke OpenCV or AI merely because those stages exist. The orchestrator selects the minimum sufficient path.

## Migration Rule

Existing direct vendor calls are migration debt. When touching a direct integration:

1. identify the reusable upstream-specific behavior;
2. move that behavior behind the canonical `tavall-<tool>` owner;
3. leave product/domain semantics with their existing owner;
4. migrate callers to the Tavall boundary;
5. remove duplicate raw vendor invocation paths rather than preserving permanent compatibility layers.

A migration is incomplete if the new wrapper exists while ordinary production code still contains an equivalent direct invocation path without a documented exception.

## Exceptions

A one-off developer command, test fixture, or bootstrap script may invoke an upstream tool directly when it is not a reusable production capability. The exception must remain local to tooling/test/bootstrap scope and must not become the de facto production integration surface.

Architecture review is required when a production consumer believes direct upstream access is structurally unavoidable.

## Review Checklist

- Is the upstream integration owned by a `tavall-*` module/artifact?
- Does that owner hide raw vendor invocation/protocol details from ordinary consumers?
- Are product/domain semantics still owned outside the vendor wrapper?
- Can the provider be changed without rewriting callers around vendor syntax?
- Are lifecycle, failure, security, and observability concerns owned once?
- Are agents and MCP/CLI adapters routing through Tavall semantics rather than vendor commands?
- Has duplicate direct integration debt been removed or explicitly tracked?

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/code-architecture/THIRD_PARTY_TOOL_BOUNDARIES.md` | 2026-09-29 5:08 PM PDT | PR to `main`. |
| Notion | `NOT_APPLICABLE` | — | 2026-09-29 5:08 PM PDT | Quality/reference document; no 1:1 requirement assigned. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-29 5:08 PM PDT | GitHub | `CREATED` | `TavallStudios/tavall-docs/docs/quality/code-architecture/THIRD_PARTY_TOOL_BOUNDARIES.md` | — | PR to `main`. | Added canonical Tavall-owned third-party wrapper rules and media routing example. |

</details>
