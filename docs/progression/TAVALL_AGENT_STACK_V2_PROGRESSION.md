# Tavall Agent Stack V2 Progression

> **Document Type:** Progression / Evidence  
> **Source of Truth For:** Tavall Agent Stack V2 implementation, architectural refactor, agent family taxonomy, and validation evidence  
> **Canonical Owner:** `TavallStudios/tavall-ai` & `TavallStudios/tavall-docs`  
> **Branch:** `working/tavall-agent-stack-v2`  
> **Last Audited Date:** 2026-10-02  
> **Status:** Fully Implemented / Verified

---

## 1. Executive Summary

Tavall Agent Stack V2 transitions Tavall AI architecture from ad-hoc skill routing and monolithic scheduler execution to a disciplined, agent-centric model where:

1. **Agents are the only top-level AI capability abstraction** (`Agents = Tavall AI API`, `Skills = agent implementation`, `Docs = authority`, `Tools/MCPs = implementation mechanisms`). Callers and automations route strictly to Agents, never directly to skills, MCPs, or internal tools.
2. **Mandatory work entry path** is enforced:
   ```text
   INPUT (User / AI / Harness / Event / Automation)
     ↓
   tavall-agent-memory (Context recovery; historical evidence)
     ↓
   tavall-agent-ledger (AI coordination graph; registration & conflict detection)
     ↓
   tavall-docs-agent (Skinny JIT document routing; governing doc identification)
     ↓
   tavall-orchestrator (Agent graph selection; smallest valid specialist set)
     ↓
   Selected Tavall Agents (Execution through owned skills, tools, and MCPs)
   ```
3. **Scheduler is replaced by Ledger** (`tavall-agent-ledger`). Scheduling is an internal ledger capability; Ledger acts as the AI coordination graph tracking worker identity, scope claims, dependencies, and state without overriding Git/GitHub or Tavall Cloud authorities.
4. **Document-backed skills become 1:1 section adapters**: Skills mirror exact canonical section names from `tavall-docs` with strict context discipline (no complete document preloading, no section body duplication).
5. **Agent Mode is normalized**: Every agent explicitly defines `agent_mode: [ROLE, AI_SUBAGENT]` accompanied by a collapsible explanation spoiler block.

---

## 2. Chronological Milestones

### 2026-10-02 — Milestone 1: Canonical Quality Policy, Terminology & Skill Standards
- **Commit:** `7d3e8bda5f244ac61a383407934ff6bba21dd863` in `TavallStudios/tavall-docs` (`working/tavall-agent-stack-v2`)
- **Deliverables:**
  - `docs/quality/TAVALL_TERMINOLOGY.md`: Authoritative definitions for Agent, Worker, Agent Ledger, Agent Mode (`ROLE`, `AI_SUBAGENT`), Skill, Tool, MCP, Plugin, Harness, and Orchestrator.
  - `docs/quality/SKILL_TEMPLATE.md`: Standardized templates for both tiny document-section adapters and procedural checklists.
  - `docs/quality/AGENT_ARCHITECTURE.md`: Canonical architectural specification of V2 agent families, mandatory entry flow, and naming contracts.
  - `docs/quality/DOCUMENT_ROUTING.yml`: Updated routing index for new quality documents.
- **Verification:**
  - `python3 scripts/ci/verify_docs.py --mode build` -> `OK (43 docs)`
  - `python3 scripts/ci/verify_docs.py --mode integration` -> `OK`

### 2026-10-02 — Milestone 2: Java Core Architecture & Agent Runtime Modularization
- **Repository:** `TavallStudios/tavall-ai` (`working/tavall-agent-stack-v2`)
- **Refactors:**
  - Renamed `tavall-agent-scheduler` → `tavall-agent-ledger` (`LedgerAgentProvider`, `AGENT_ID = "ledger"`).
  - Renamed `tavall-agent-implementation` → `tavall-agent-pr-workflow` (`PrWorkflowAgentProvider`, `AGENT_ID = "pr-workflow"`).
  - Renamed `tavall-agent-architecture` → `tavall-agent-code-architecture` (`CodeArchitectureAgentProvider`, `AGENT_ID = "code-architecture"`).
  - Renamed `tavall-agent-review` → `tavall-agent-pr-review` (`PrReviewAgentProvider`, `AGENT_ID = "pr-review"`).
  - Renamed `tavall-agent-reconciliation` → `tavall-agent-pr-reconciliation` (`PrReconciliationAgentProvider`, `AGENT_ID = "pr-reconciliation"`).
  - Renamed `tavall-agent-e2e` → `tavall-agent-e2e-validation` (`E2EValidationAgentProvider`, `AGENT_ID = "e2e-validation"`).
  - Updated Gradle settings, build scripts, naming tests, and runtime integration test.
- **Verification:**
  - `./gradlew check verifyTavallAISystem` -> `BUILD SUCCESSFUL in 3s` (57 actionable tasks: 10 executed, 47 up-to-date).

### 2026-10-02 — Milestone 3: Plugin Packages & Runtime Projection
- **Locations:**
  - Live projection: `/srv/dev-storage/.ai/plugins/Tavall`
  - Workspace repository: `/srv/dev-storage/workspaces/tavall-ai/repo_root/plugins/tavall-ai`
- **Deliverables:**
  - Built 43 specialized agents across Coordination, Design, Self-Evolution, PR Workflow, Acceptance, Delivery, Documentation, and Domain families.
  - Deployed 132 tiny section-backed skills referencing `tavall-docs` 1:1.
  - Updated `registry.yaml` (v10) with mandatory entry path policy and legacy aliases.
  - Updated client adapters (`codex`, `claude`, `gemini`, `agents`) and root `skills` symlink projection.
  - Generated and validated source digest seeds (`bootstrap-seed.json`).
- **Verification:**
  - `/srv/dev-storage/.ai/plugins/Tavall/.tavallci/validate.py all` -> `check=all status=PASS`
  - `/srv/dev-storage/workspaces/tavall-ai/repo_root/plugins/tavall-ai/.tavallci/validate.py all` -> `check=all status=PASS`

### 2026-10-02 — Milestone 4: End-to-End Behavioral Suite & Test Coverage
- **Suite:** `test_tavall_agent_stack_v2.py`
- **Verification:**
  - Test 1 (Agent loading, schema compliance, unique skill ownership): `PASS`
  - Test 2 (Mandatory entry path order): `PASS`
  - Test 3 (PR workflow lifecycle states and transitions): `PASS`
  - Test 4 (Ledger registration and conflict detection): `PASS`
  - Test 5 (Section skill 1:1 references against `tavall-docs`): `PASS` (132/132 verified)
  - Test 6 (Behavioral Scenarios A through E): `PASS`
    - Scenario A: New PR implementation request
    - Scenario B: Colliding worker detection
    - Scenario C: Skinny JIT doc expansion
    - Scenario D: Recovery without ambient authority
    - Scenario E: Self-evolution from repetitive prompt pattern

---

## 3. Evidence Matrix

| Check / Gate | Target | Command / Script | Result |
| --- | --- | --- | --- |
| Documentation CI | `tavall-docs` | `python3 scripts/ci/verify_docs.py --mode build && python3 scripts/ci/verify_docs.py --mode integration` | `PASS` (43 tracked docs valid) |
| Java Architecture Checks | `tavall-ai` | `./gradlew check verifyTavallAISystem` | `BUILD SUCCESSFUL` (57 tasks) |
| Plugin Packaging CI/CD | `/srv/dev-storage/.ai/plugins/Tavall` | `python3 .tavallci/validate.py all` | `check=all status=PASS` |
| Plugin Packaging CI/CD | `plugins/tavall-ai` | `python3 .tavallci/validate.py all` | `check=all status=PASS` |
| E2E Behavioral Suite | `tavall-ai` | `python3 test_tavall_agent_stack_v2.py` | `ALL TESTS PASSED` |
| Section Mapping 1:1 | `tavall-ai` & `tavall-docs` | `python3 test_tavall_agent_stack_v2.py` (Test 5) | `PASS` (132 sections matching) |
