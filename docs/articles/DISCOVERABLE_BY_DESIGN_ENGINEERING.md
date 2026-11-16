# Discoverable by Design: Code for Humans and Autonomous Agents

> **Document type:** `ARTICLE`  
> **Audience:** Engineers, coding-agent designers, collaborators, and technical partners  
> **State:** Draft, founder rationale captured November 9, 2026  
> **Owning GENERAL:** [Tavall Code Design Agent & Build Doctrine — GENERAL](https://app.notion.com/p/3ef38458ddfd81dca3d7cef9b8114537)

## Thesis

**Code should be designed so humans can understand it at a glance and autonomous agents can discover, reason about, and reproduce its patterns reliably.** This is an architectural objective, not a formatting preference.

## Where this came from

After seeing agents write, run, and test software in Qodo Gen, I began thinking beyond asking an agent to generate another method: what if it could recognize a proven implementation pattern, understand its place in the system, and apply it to another system without needing to rediscover the design each time?

The way I was structuring dependency injection and the surrounding Java code suggested an answer. The hierarchy visible through an abstract syntax tree (AST), combined with type information, symbol resolution, and explicit dependency contracts, could provide a map that an agent can traverse instead of a pile of loosely connected text.

That was a reason for emphasizing type safety, explicit roles, predictable ownership, and clear variable boundaries. It was not an effort to make code resemble a particular style guide.

## The problem with code that merely works

An implementation can compile and pass tests while making the next change harder for both its human maintainer and its automated maintainer. Implicit dependencies, overloaded responsibilities, deeply nested expressions, and inconsistent module boundaries force each reader to reconstruct intent from incidental syntax.

Agents are not exempt from this problem. Generating code is one capability; finding the correct owner, understanding the actual contract, adapting a known pattern, and proving the resulting behavior are different capabilities. Human reviewers likewise should not have to mentally execute an entire expression just to discover the value being passed to the next operation.

## Tavall's position: discoverability is a design property

- **Typed relationships first.** Prefer explicit inputs, outputs, contracts, and domain types so tooling can distinguish valid compositions from plausible-looking guesses. Type safety narrows ambiguity; it does not guarantee correct behavior.
- **Meaningful interface boundaries.** Use interfaces where substitution, shared behavior, ownership, testing, or lifecycle creates a real contract. Tavall DI can also manage concrete-only capabilities. Interfaces are not decorations for every class.
- **Dependencies and ownership must be traversable.** Composition should expose who owns a capability, which module consumes it, and where implementation is selected. Avoid hidden construction and accidental duplicate authority.
- **Name intermediate states.** Deliberate local variables separate steps, make data flow glanceable, and provide inspection points for debugging and automated analysis. Do not compress distinct operations into nested expressions merely to save lines.
- **Predictable modules and class roles.** A class, package, or module should have a discoverable responsibility and lifecycle. Reuse a pattern where responsibilities match; do not force a pattern onto a different domain.
- **Readable by humans before it is clever.** A person should be able to scan a method and understand its progression, especially when attention and working memory are limited. Glanceability is a maintenance property, not cosmetic formatting.

## What an agent should be able to do

The intended discovery chain is:

```txt
Source AST
  -> symbols and resolved types
  -> dependency and module ownership graph
  -> recognizable implementation pattern
  -> context-aware adaptation
  -> compile + behavioral tests + integration evidence
  -> accepted change
```

An AST exposes syntax and structure. It does **not** by itself prove intent, semantics, runtime wiring, or business behavior. The additional typed contracts, dependency graph, and executable validation make reuse more trustworthy.

The long-term ambition is for agents to identify a verified Tavall pattern and apply it across systems with minimal human re-explanation while still checking that the target context actually warrants it. "Copy and paste" is the intuitive starting idea, not permission for blind cloning.

## Why Java remains useful

Java offers explicit types, mature parsing and refactoring tools, approachable control flow, and a long-lived ecosystem for complex services. Its verbosity can be an advantage when it names meaningful steps and exposes stable contracts. This is not a rule against other languages; the same discoverability goals can apply across languages and ASTs.

## Alternatives and tradeoffs

Minimal lines of code, clever inlining, runtime reflection everywhere, and blanket interface creation can all look convenient locally. None guarantees understandable or reusable systems.

Explicitness has a cost too: meaningless temporary variables, interfaces without actual contracts, or modules without a lifecycle purpose add noise. The objective is **meaningful structure with low cognitive load**, not maximum ceremony.

Likewise, agents should not refactor working code merely to resemble a preferred shape. Evaluate correctness, architecture, maintainability, operational behavior, and measured performance together.

## Reality check

- **Existing foundation:** Tavall has [Code Architecture](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/CODE_ARCHITECTURE.md), [Module Types](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/MODULE_TYPES.md), and [Tavall DI](https://github.com/TavallStudios/tavall-di) contracts and implementations that express parts of this approach.
- **Founder rationale now documented:** The connection between agent pattern reproduction, AST-aware discovery, type safety, explicit data flow, human glanceability, and the decision to keep using Java.
- **Intended future work, not claimed implemented:** Agent-wide pattern extraction, AST/type/dependency-graph-based transformations, automated architecture compliance, and reproducible cross-system adaptation with verified tests.

This ARTICLE explains *why*. The binding engineering rules and actual APIs remain in their respective owners.

## Related documentation

- [Tavall Code Architecture](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/CODE_ARCHITECTURE.md)
- [Namespaces, Variables, OOP and Type Safety](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/code-architecture/NAMESPACES_VARIABLES_AND_OOP.md)
- [Dependency Injection and Orchestration](https://github.com/TavallStudios/tavall-docs/blob/main/docs/quality/code-architecture/DEPENDENCY_INJECTION_AND_ORCHESTRATION.md)
- [Tavall DI access styles](https://github.com/TavallStudios/tavall-di/blob/main/docs/DI_ACCESS_STYLES.md)
- [Tavall Code Design Agent & Build Doctrine — GENERAL](https://app.notion.com/p/3ef38458ddfd81dca3d7cef9b8114537)
- [Tavall Software Engineering, AI Development & Acceptance Policy](https://app.notion.com/p/3bb38458ddfd813f9f72d2deb9fccb52)

## Closing thesis

**Make intent visible enough for a human to recognize and structure explicit enough for a machine to verify. Then reuse patterns without reusing mistakes.**

## DOC TODO

- [ ] Confirm the historical account with the founder during publication review.
- [ ] Evaluate whether to link this rationale from Tavall's binding code-architecture documents without changing the rules themselves.
- [ ] Keep future implementation claims evidence-backed in owning DESIGN/PROGRESSION records.

## Documentation update state

| Surface | Sync state | Location |
| --- | --- | --- |
| GitHub | Draft / working branch | `TavallStudios/tavall-docs/docs/articles/DISCOVERABLE_BY_DESIGN_ENGINEERING.md` |
| Notion | Synced draft | [Notion ARTICLE](https://app.notion.com/p/41338458ddfd8172a52be866f2cf06a7) |

**Change history:** November 9, 2026: initial founder rationale captured and synchronized as an ARTICLE. This document is not a substitute for binding architecture or canonical tool contracts.
