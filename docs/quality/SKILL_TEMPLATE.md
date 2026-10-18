# Tavall Skill Template

> **Status:** Active  
> **Applies to:** First-party Tavall Agent skills across all plugin and agent packages  
> **Authority:** `TavallStudios/tavall-docs/docs/quality/DOCUMENTATION_STANDARDS.md`  
> **Purpose:** Standardize the structure of Tavall skills, providing explicit templates for both tiny document-backed section adapters and concise procedural or execution skills.

Skills are internal implementation details owned by Agents. They are **never top-level routing targets**.

---

## Form A: Tiny Document-Backed Section Adapter (Default for Governance)

Use this form for skills whose role is to apply a section of canonical Tavall documentation. The skill acts as a lightweight pointer and adapter: it **must not** duplicate policy or preload whole documents.

```markdown
---
name: <normalized-hyphenated-skill-name>
agent: <owning-tavall-agent-id>
authority: TavallStudios/tavall-docs@main
document: docs/quality/<CANONICAL_DOCUMENT>.md
section: "<Exact Canonical Section Title>"
---

# <Exact Canonical Section Title>

## Activate when

- <Specific condition or trigger requiring this section>
- <Second trigger, e.g. state transition, review requirement, or pre-implementation gate>

## Read

- `<canonical-document-path>`
- `<Exact Canonical Section Title>`

## Apply

- Apply the canonical section policy directly.
- Follow only directly referenced governing sections required by the active concern.

## Context discipline

- Do not load the entire document.
- Do not duplicate the section body or policy here.
- Do not treat this skill as policy authority; the referenced document controls.
```

---

## Form B: Concise Non-Document-Backed Skill (Procedural / Tool / Algorithmic)

Use this form for skills that execute tools, run algorithms, enforce procedural steps, or coordinate internal agent mechanics.

```markdown
---
name: <skill-name>
description: <One-line concise summary of what this skill does>
agent: <owning-tavall-agent-id>
type: <tool-backed | algorithm-backed | procedural | composite-internal>
---

# <Skill Title>

## Use when

- <Concrete scenario or task where this skill is needed>
- <Specific input or state condition>

## Do not use when

- <Scenario where a different agent or skill should be used instead>
- <Boundary condition where this skill does not apply>

## Authority

- Primary authority: `<canonical doc or tool owner>`
- Precedence: Policy docs override local procedures.

## Inputs

- `<Input 1: name, type, description>`
- `<Input 2: name, type, description>`

## Checklist / Procedure

1. [ ] **<Step 1 Name>**: <Concrete action or tool invocation>
2. [ ] **<Step 2 Name>**: <Validation or state check>
3. [ ] **<Step 3 Name>**: <Execution or output generation>

## Output contract

- Return `<expected structured output, artifact, or status>`.
- Preserves exact source or evidence identifiers.

## Mutation boundaries

- Allowed mutations: `<Allowed paths, branches, files, or states>`
- Prohibited mutations: `<Off-limit files, production state, or unrelated scope>`

## Failure and escalation

- If `<condition>`, pause and report `<failure state>` to owning Agent.
- Escalation path: Hand off to `<fallback Agent>` or halt with explicit blocker.

## Context discipline

- Load only the minimal metadata and tool interfaces required for execution.
- Discard intermediate logs once final output evidence is produced.
```
