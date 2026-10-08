# Tavall Agent Stack V2 Architecture

> **Status:** Active  
> **Applies to:** Tavall AI stack, Agent definitions, skills, runtime modules, plugins, and harnesses  
> **Authority:** `TavallStudios/tavall-docs/docs/quality/TAVALL_TERMINOLOGY.md`  
> **Purpose:** Establish the canonical architecture for the Tavall Agent Stack V2, standardizing Agents as the only top-level capability abstraction, defining the mandatory work entry path, and formalizing the coordination, design, PR workflow, acceptance, and delivery agent families.

## 1. Core Architectural Principle

Tavall exposes **Agents as the only top-level AI capability abstraction**.

AI workers, orchestrators, harnesses, users, automations, and callers route strictly to **Agents**. Callers never route directly to:
- skills;
- MCPs;
- tools;
- scripts;
- CLIs;
- model adapters;
- documentation readers;
- plugins.

These mechanisms are internal implementation details owned and orchestrated by Agents.

```text
Agents = Tavall AI API
Skills = agent implementation
Docs = authority
Tools/MCPs/scripts/etc. = implementation mechanisms
```

## 2. Mandatory Work Entry Sequence

All Tavall work enters through this exact sequence:

```text
INPUT (User / AI / Harness / Event / Automation)
  ↓
tavall-agent-memory
  ↓
tavall-agent-ledger
  ↓
tavall-agent-provenance : START
  ↓
tavall-docs-agent
  ↓
tavall-orchestrator
  ↓
selected Tavall Agents
  ↕
tavall-agent-provenance : UPDATE
  ↓
tavall-agent-provenance : FINALIZE
  ↓
HANDOFF / OUTPUT
```

### Hierarchy of Context, Coordination, and Authority

1. **Memory (`tavall-agent-memory`)**: Reads the shared typed `MEMORY_PLANE` for exact, structural, semantic-candidate, and temporal context. Memory is **contextual evidence** and **must never override current canonical documentation, code, or runtime evidence**. Durable writes use the explicit `recordMemory` boundary; ordinary prompts and provider results are retrieval-only.
2. **Ledger (`tavall-agent-ledger`)**: Resolves worker identity, claims scope, inspects concurrent workers, prevents collisions, and records dependencies before substantive work begins.
3. **Provenance (`tavall-agent-provenance`)**: Maintains the repo-local and module-local raw AI work provenance layer (`.tavallai`). Operates strictly as a `ROLE` to link active runs, threads, and handoffs into Git, Cloud, Memory, and Ledger authorities using deterministic JSON.
4. **Docs (`tavall-docs-agent`)**: Executes a **skinny JIT pass** to identify likely governing documents and section pointers without preloading bodies.
5. **Orchestrator (`tavall-orchestrator`)**: Coordinates the smallest valid Agent graph for the task.

The provider roles, authority order, ingestion, rebuild, and retrieval contract are defined in [Tavall AI Memory Plane](../architecture/TAVALL_AI_MEMORY_PLANE.md).

## 3. Canonical Agent Groups

```text
COORDINATION
├── tavall-agent-memory
├── tavall-agent-ledger
├── tavall-agent-provenance
├── tavall-docs-agent
└── tavall-orchestrator

DESIGN
├── tavall-code-design-agent
├── tavall-agent-code-architecture
├── tavall-agent-module-boundaries
├── tavall-agent-product-design
└── tavall-agent-user-experience

SELF-EVOLUTION
└── tavall-agent-authoring

PR WORKFLOW
├── tavall-agent-pr-workflow
├── tavall-agent-pr-intake
├── tavall-agent-pr-topology
├── tavall-agent-pr-development
├── tavall-agent-pr-readiness
├── tavall-agent-pr-review
├── tavall-agent-pr-reconciliation
├── tavall-agent-pr-integration
└── tavall-agent-pr-promotion

ACCEPTANCE
├── tavall-agent-acceptance
├── tavall-agent-ci-validation
├── tavall-agent-architecture-validation
├── tavall-agent-integration-validation
├── tavall-agent-e2e-validation
└── tavall-agent-acceptance-finalization

DELIVERY
├── tavall-agent-versioning
├── tavall-agent-artifact
├── tavall-agent-release-readiness
├── tavall-agent-deployment
└── tavall-agent-post-deployment-validation

DOCUMENT STATE
├── tavall-agent-readme
└── tavall-agent-progression

DOMAIN
├── tavall-agent-platform
├── tavall-agent-cloud
├── tavall-agent-networking
├── tavall-agent-security
├── tavall-agent-data
├── tavall-agent-minecraft
├── tavall-agent-web
├── tavall-agent-builder
├── tavall-agent-ci-cd
└── coding-with-jev-agent
```

## 4. Agent Modes

First-party Tavall Agents support two normalized execution modes:
- **`ROLE`**: The active AI context assumes the Agent responsibility directly. No distinct worker is created. This is the preferred default mode for low-overhead, in-context operations.
- **`AI_SUBAGENT`**: A separate, bounded AI worker is spawned in an isolated context. The worker **must register with `tavall-agent-ledger`** before performing any mutations.

## 5. Main Document Skills and 1:1 Section Adapters

Document-backed skills act as tiny section adapters:

```text
canonical document
  ↓
main document skill (index of all routable sections)
  ↓
section skill (1:1 with canonical section title)
  ↓
exact canonical document section
```

## 6. Typed Tavall AI Directory Format (`.tavallai`)

`.tavallai/` is a typed directory format, not a path-based guess. Every root has a `tavallai.json` discovery entrypoint validated against `docs/schemas/tavallai-directory.schema.json`; `schemaVersion` and `directoryType` are required.

### Directory types and owners

| `directoryType` | Scope | Authority | Allowed mutation |
| --- | --- | --- | --- |
| `PROVENANCE` | `REPOSITORY_ROOT` or `MODULE_ROOT` | `tavall-agent-provenance` | Raw run/thread/work/handoff records and references only. It must not store or mutate durable Memory Plane state. |
| `MEMORY_PLANE` | `TAVALL_INSTALLATION` | `tavall-agent-memory` and its authorized ingestion/provider tools | Shared provider manifests, source identity/checkpoints, derived exports, and rebuildable indexes. |

The canonical installed Memory Plane root is `/srv/dev-storage/.ai/plugins/Tavall/.tavallai`. Repository and module roots remain `PROVENANCE`; they reference shared memory rather than copying it.

### Architectural principles

1. **Explicit type**: Never infer semantics from the directory path. A missing, unknown, or invalid `directoryType` is a fail-closed condition; do not mutate it automatically.
2. **Owner gate**: `tavall-agent-provenance` may mutate only validated `PROVENANCE` roots. Only the Memory Plane owner may mutate validated `MEMORY_PLANE` state. Unknown types are read-only until an explicit migration classifies them.
3. **JSON exclusively**: `.tavallai` metadata and state use deterministic JSON (2-space indentation, stable key ordering), never YAML or Markdown.
4. **References, not duplication**: `PROVENANCE` roots reference authorities (`authority`, `ref`, `observedAt`, `revision`) and do not duplicate docs, provider stores, Git history, or Cloud execution state. The `MEMORY_PLANE` stores manifests and derived indexes, not duplicate authoritative databases or full source corpora.
5. **Scope hierarchy**: Each repository has a `PROVENANCE` root; each independently testable/deployable source or build module may have a `PROVENANCE` root with a relative parent reference. Circular links are forbidden.
6. **Pass lifecycle**: `START` binds active run, provider thread, Ledger scope, Git/Cloud/Memory authorities; `UPDATE` records meaningful transitions, not every tool call; `FINALIZE` records a handoff and clears active state.

Main document skills list every routable section in canonical order without duplicating policy. Section skills provide minimal trigger and pointer instructions, ensuring context budget is preserved.

## 7. Plugin-Native Skill Surface Architecture

Tavall standardizes a **single-source capability architecture** where core business logic, behavioral requirements, and execution instructions exist in exactly one canonical location and project outward into multiple client surfaces via thin, stateless surface adapters.

```text
               ┌────────────────────────────────────────────────────────┐
               │  Canonical Single-Source Skill                         │
               │  /srv/dev-storage/.ai/plugins/Tavall/.../SKILL.md      │
               └───────────────────────────┬────────────────────────────┘
                                           │
             ┌─────────────────────────────┼────────────────────────────┐
             ▼                             ▼                            ▼
   ┌───────────────────┐         ┌───────────────────┐        ┌───────────────────┐
   │    Web Adapter    │         │    CLI Adapter    │        │    MCP Adapter    │
   │  (Web console,    │         │  (Headless stream,│        │  (Tool schema,    │
   │   markdown/UI)    │         │   CLI arguments)  │        │   JSON RPC)       │
   └───────────────────┘         └───────────────────┘        └───────────────────┘
```

### Architectural Principles

1. **One Canonical Capability / Skill**:
   Every skill is declared once inside its owning Agent directory within the canonical plugin (`/srv/dev-storage/.ai/plugins/Tavall/agents/<agent>/skills/<skill>/SKILL.md`). Business logic, validation rules, and domain policies must never be duplicated across surfaces.

2. **Multiple Surface Adapters**:
   Surface adapters project the canonical skill into specific caller environments without modifying its core contract:
   - **Web Surface**: Formats inputs for web chat/console interaction, renders rich markdown/diagrams, and supports interactive prompts.
   - **CLI Surface**: Invoked via command-line arguments and stdin/stdout streams, supports headless batch execution, and emits POSIX exit codes.
   - **MCP Surface**: Exposes the skill as a standard Model Context Protocol tool with validated JSON schema parameters and structured tool results.
   - **Harness Surface**: Enables automated CI testing, regression sweeps, and deterministic mock evaluation.

3. **Surface Metadata Schema**:
   Every projected adapter exposes standard capability metadata:
   - `mode`: `HEADLESS` (non-interactive, automation-safe) vs `INTERACTIVE` (requires user dialogue or confirmation).
   - `input_schema`: Strict JSON Schema defining accepted arguments, types, required fields, and validation constraints.
   - `output_representation`: Expected format (`JSON`, `STREAMING_TEXT`, `STRUCTURED_MARKDOWN`, `EXIT_CODE`).
   - `permission_profile`: Bounded access rights (`READ_ONLY`, `WORKSPACE_MUTATION`, `NETWORK_OUTBOUND`, `PRIVILEGED`).

4. **Projection & Anti-Drift Rules**:
   - **Never Hand-Edit Projections**: Surface manifests, tool declarations, and CLI wrappers are strictly derived from the canonical skill. Hand-editing projected copies is strictly prohibited.
   - **Automated Regeneration**: Projections are regenerated deterministically via adapter toolchains.
   - **Stale Projection Detection**: Projected adapter manifests record the canonical source SHA-256 content hash (`canonical_source_hash`). During build, CI, and agent execution, drift detection verifies that the projection matches the active canonical skill file; mismatches fail validation.
