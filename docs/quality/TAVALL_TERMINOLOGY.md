# Tavall Terminology Authority

> **Status:** Active  
> **Applies to:** Tavall system, AI architecture, Agent stack, workflow, tooling, runtime, and documentation  
> **Purpose:** Provide the single canonical organization authority for Tavall-specific vocabulary so humans and AI workers use terms consistently and avoid conflating architectural abstractions with low-level implementation mechanisms.

## 1. Core Abstractions

### Agent

The **only first-class Tavall AI capability abstraction exposed for routing**. AI workers, orchestrators, harnesses, users, automations, and callers route strictly to Agents, never directly to skills, MCPs, tools, scripts, CLIs, or documentation readers.

An Agent owns a durable operating role, lifecycle boundary, or system domain. Internally, an Agent may contain and orchestrate:
- skills (reusable procedural/context workflows);
- tools (executable capabilities);
- MCPs (transport/integration bridges);
- scripts and CLIs;
- documentation readers and section adapters;
- models and prompt adapters;
- plugins and runtime mechanisms.

### Agent Definition

A persistent, reusable structural and behavioral specification of an Agent (for example, its metadata in `agent.yaml`, contract in `agent.md`, and ServiceLoader provider in Java). An Agent Definition is not a running worker; multiple active workers may instantiate the same Agent Definition simultaneously.

### Worker

One concrete, running AI execution acting through an Agent definition within a specific scope, workspace, and lifecycle. A worker has a unique worker identity and registers with the Agent Ledger before performing substantive work.

### Agent Ledger

The canonical AI coordination graph for active Tavall AI work. The Ledger tracks:
- worker identity and Agent being executed;
- parent/child worker relationships;
- worker scope and claimed paths/modules;
- repository, working PR, branch, and exact source commit SHA;
- Tavall Cloud lane, environment, workspace, and execution leases;
- worker lifecycle states (`ACTIVE`, `PAUSED`, `BLOCKED`, `COMPLETE`, `FAILED`);
- active blockers, handoff artifacts, current task, next action, and evidence.

The Ledger links AI workers into external authorities: GitHub remains authoritative for Git/PR/source state; Tavall Cloud/CONTROL remains authoritative for Cloud execution state.

### Agent Mode

A supported execution mode declared by an Agent definition:
- `ROLE`: The Agent behavior is assumed directly by the active AI context without launching a separate worker. Used by default to preserve context continuity and eliminate coordination overhead.
- `AI_SUBAGENT`: A distinct, bounded AI worker is spawned in an isolated context. The worker must register, claim scope, and coordinate state through the Agent Ledger.

### Skill

An internal procedural or context-delivery capability owned by an Agent. A skill is an implementation detail of its owning Agent and is **never a top-level routing target**. Skills are categorized into:
- Document-backed section adapters;
- Tool-backed execution contracts;
- Algorithm / behavior-backed procedural checklists;
- Composite agent-internal workflows.

### Tool

An executable function or command capability owned internally by an Agent. Tools are implementation mechanisms, not top-level routing abstractions.

### MCP (Model Context Protocol)

A transport and integration mechanism used to connect external systems, runtimes, or databases to an Agent. MCP names and protocol endpoints do not define Tavall conceptual ownership.

### Plugin

A distributable packaging mechanism (such as the Tavall AI plugin) that bundles Agents, their internal skills, tools, MCP adapters, and client discovery metadata.

### Harness

A runtime or container environment (such as Tavall Open Harness or AgentTaskManager) that hosts Agents and provides system facilities, process isolation, environment variables, credentials, and transport bridges.

### Orchestrator

The specialist Agent (`tavall-orchestrator`) that evaluates the active work request, contextual Memory, Ledger state, and skinny Docs routing to select and coordinate the smallest valid Agent graph necessary to satisfy the request.

### Memory

Contextual and historical evidence recovered from prior interactions, past decisions, session transcripts, or previous handoffs. Memory informs work but is strictly contextual evidence: it **must never override current canonical documentation, accepted code, or live runtime evidence**.

### Validation

Evidence-producing verification of a candidate change against an exact source SHA or runtime environment generation (for example, local CI, architecture tests, or E2E suites).

### Acceptance

The formal decision that all required verification evidence for a bounded acceptance unit exists, is tied to the exact candidate head, remains current, and satisfies all governing criteria. Acceptance must fail closed on stale or missing evidence.

### Integration

The composition of accepted, bounded source units into the next durable staging boundary (such as Development Staging, Runtime, or Staging pull requests). Any change to composed integration state requires fresh verification evidence.

### Promotion

Advancing accepted source or artifact state to a higher canonical tier (such as merging an integrated Staging PR into `main`, or advancing an artifact from development to release channels). Promotion is an authoritative state transition and does **not** inherently mean deployment.

### Deployment

The physical or operational transition of live running software (services, server instances, edge directors, database schemas) to a target environment generation. Deployment remains separate from source promotion.

### Canonical Source

The exact, immutable authoritative source identity (repository URL + exact commit SHA). A filesystem directory or floating branch name is never by itself a canonical source identity.

### Handoff

The durable, inspectable state transfer artifact passed between workers, stages, or Agents (such as uncommitted patch context, acceptance evidence, or blocker descriptions).

## 2. Architectural Hierarchy

The Tavall architectural hierarchy is strictly ordered:

```text
Docs     = Policy, design, and organizational authority
Code     = Implementation evidence
Runtime  = Operational evidence
Memory   = Contextual and historical evidence
```

When evidence conflicts with authority, canonical documentation controls until an explicitly authorized change is made to that documentation.

## 3. Mandatory Work Entry Sequence

All Tavall AI work enters through this exact sequence:

```text
INPUT (User / AI / Harness / Event / Automation)
  ↓
tavall-agent-memory (Context recovery; historical evidence)
  ↓
tavall-agent-ledger (AI coordination graph; registration and conflict check)
  ↓
tavall-docs-agent (Skinny JIT document routing; governing doc identification)
  ↓
tavall-orchestrator (Agent graph selection; smallest valid specialist set)
  ↓
Selected Tavall Agents (Execution through owned skills, tools, and MCPs)
```
