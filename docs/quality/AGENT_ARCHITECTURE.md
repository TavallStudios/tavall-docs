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

1. **Memory (`tavall-agent-memory`)**: Recovers past decisions, uncommitted context, and historical intent. Memory is **contextual evidence** and **must never override current canonical documentation, code, or runtime evidence**.
2. **Ledger (`tavall-agent-ledger`)**: Resolves worker identity, claims scope, inspects concurrent workers, prevents collisions, and records dependencies before substantive work begins.
3. **Provenance (`tavall-agent-provenance`)**: Maintains the repo-local and module-local raw AI work provenance layer (`.tavallai`). Operates strictly as a `ROLE` to link active runs, threads, and handoffs into Git, Cloud, Memory, and Ledger authorities using deterministic JSON.
4. **Docs (`tavall-docs-agent`)**: Executes a **skinny JIT pass** to identify likely governing documents and section pointers without preloading bodies.
5. **Orchestrator (`tavall-orchestrator`)**: Coordinates the smallest valid Agent graph for the task.

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

## 6. Local AI Work Provenance Layer (`.tavallai`)

`.tavallai` is the repository- and module-local **raw AI work provenance layer**. It is maintained exclusively by `tavall-agent-provenance` operating as a `ROLE`.

### Architectural Principles

1. **JSON Exclusively**: All structures use deterministic JSON (2-space indent, stable key order), never YAML or Markdown.
2. **References, Not Duplication**: `.tavallai` references existing authorities (`authority`, `ref`, `observedAt`, `revision`). It does NOT duplicate architecture documentation, memory stores, Git history, or Cloud execution state.
3. **Scope Hierarchy**:
   - Every included repository exposes a repository root `.tavallai/` with `tavallai.json` as discovery entrypoint.
   - Every independently testable/deployable source or build module boundary exposes a module-local `.tavallai/` referencing its parent repository root. Circular links are strictly forbidden.
4. **Pass Lifecycle**:
   - **START**: Associates active run, provider thread, Ledger worker claims, and Git/Cloud/Memory authorities into `runs/active.json`.
   - **UPDATE**: Updates active run only on meaningful transitions (subagents, scope crossing, handoffs, blockers); never logs per-tool-call events.
   - **FINALIZE**: Records completed run in `runs/history.json`, clears active state, and emits structured handoff in `runs/handoffs/<run-id>.json` allowing future AI resumption.

Main document skills list every routable section in canonical order without duplicating policy. Section skills provide minimal trigger and pointer instructions, ensuring context budget is preserved.
