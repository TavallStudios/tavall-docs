# Tavall Testing and Git Discipline

> **Status:** Active  
> **Authority:** Binding architecture/testing chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

This chapter defines testing expectations and the architecture implications of Git boundaries. The authoritative branch, pull-request, staging, review, owner-authority, and production-promotion rules live in [GIT_WORKFLOW.md](../GIT_WORKFLOW.md). Do not duplicate a simplified branch graph here and accidentally create a second workflow.

# Testing

## Testing Stack

Use the tools appropriate to the repository/runtime, commonly:

- JUnit 5 for unit/contract/integration execution;
- Mockito only for narrow external/platform boundaries when a real delegate/fake is impractical;
- Testcontainers for PostgreSQL, Redis, and real infrastructure dependencies;
- Mineflayer or equivalent client harnesses for Minecraft command/routing/lifecycle/interaction scenarios;
- Gradle test suites for explicit unit/contract/integration separation.

Repository-specific test skills and canonical Tavall architecture tests may impose additional requirements.

## Canonical Architecture-Test Boundary

[`TavallStudios/Tavall-Architecture-Tests`](https://github.com/TavallStudios/Tavall-Architecture-Tests) owns the reusable executable subset of Tavall-wide architecture policy. This documentation remains the human-readable authority for the policy itself; an executable rule implements policy, it does not replace or silently redefine it.

The default consumer boundary is the repository's canonical testing suite:

1. a multi-module repository owns one `*-test-suite` or equivalent repository-level verification suite;
2. that suite consumes the published Tavall architecture-test plugin/modules as dependencies rather than copying canonical test source;
3. the suite declares the real production projects/modules it owns as architecture targets;
4. those targets' compiled `main` classes, `main` Java source roots, and production/runtime classpaths are fed through the architecture-test boundary;
5. repository/root `check` reaches the suite's architecture gate once;
6. production subprojects do not each need to apply and execute duplicate canonical Tavall architecture gates.

A genuinely single-module repository may use its root verification project as the suite boundary. The important invariant is that the architecture engine inspects the real production source/classes that are built and shipped rather than a copied fixture, stale source mirror, or independently reconstructed model of the application.

Repository-specific tests remain responsible for behavior that cannot or should not be generalized into Tavall-wide architecture rules, including product-specific adapters, runtime simulations, live infrastructure/platform behavior, and explicit temporary architecture debt. When a repository-specific rule becomes reusable Tavall-wide policy, move the reusable enforcement into `Tavall-Architecture-Tests` and update this documentation in the same coherent design/review boundary.

##### Why

Putting the canonical dependency at the repository test-suite boundary gives each repository one verification authority while still allowing the shared architecture engine to inspect every applicable production module. Applying the same canonical gate independently to every production subproject duplicates configuration and execution, makes cross-module architecture harder to inspect, and encourages local copies to drift from the shared policy.

## Real Behavior First

Tests should use real domain values, real enums, real concrete behavior, and the production contract whenever practical.

Fake or mock only boundaries whose implementation is not the behavior under test, such as:

- platform/server objects;
- external providers;
- clocks;
- network clients;
- filesystem/data-source boundaries;
- real repository contracts when a repository genuinely exists;
- Tavall Database itself only when the test specifically targets behavior above persistence and a focused fake boundary is appropriate.

Do not mock the thing being tested. Do not test private methods. Do not write tests that only prove a configured mock returns the configured value.

##### Why

A test should fail when production behavior regresses. Mocking the behavior under test only proves the mocking framework can recite the answer we gave it, which is technically a skill but not one worth putting in CI.

## Tavall DI Test Composition

Tests of Tavall-managed behavior should exercise the same dependency-access model as production.

Do **not** construct a managed Handler/Service/Orchestrator with Tavall-managed dependencies through a special test constructor merely because it is convenient.

Preferred shape:

1. create the owning `IDependencyMap` or repository-approved test composition;
2. register real/fake boundary dependencies under the same interface aliases production uses;
3. create/register generated `DependencyAccess` metadata where required by the checked-in Tavall DI version;
4. instantiate/register the behavior through its production-equivalent composition path;
5. invoke the public behavior contract.

##### Why

A constructor-only test path can pass while production replacement, alias, generation, or lifecycle semantics are broken. Production-equivalent composition tests the code **and** the dependency relationship the code actually relies on.

## Test Class Rules

- Name the test after the production type with `Test` at the end.
- Match the production package structure.
- Use behavior-oriented test method names such as `modCannotPunishAdmin()` rather than `testCanPunish()`.
- Keep repeated test setup at class level when it is stable context.
- Keep behavior-specific setup inside the test when it matters only to that case.
- Extract important values into readable locals.
- Cover expected rejection/failure/cleanup paths, not only success.

```text
src/main/java/org/tavall/permissions/power/PowerLevelService.java
src/test/java/org/tavall/permissions/power/PowerLevelServiceTest.java
```

##### Why

Behavior-oriented names make CI failures describe the contract that broke. Matching packages and readable setup keep tests discoverable and prevent test-only organization from becoming another architecture to learn.

## Infrastructure Tests

Use real infrastructure when the behavior belongs to the infrastructure contract.

Examples:

- Tavall Database entity mapping, transaction rollback, native PostgreSQL behavior, migrations;
- Redis streams/TTL/locking semantics;
- Tavall Cache TTL, misses, live snapshots, invalidation;
- Tavall Registry duplicate/index/rollback behavior;
- module load/unload/replacement;
- platform-thread rules where practical.

H2/in-memory substitutes may test provider-neutral mechanics, but they must not claim PostgreSQL-specific behavior is verified.

## Full-Flow Tests

Delegate-style integration/simulation tests should exercise a meaningful real flow while faking only true external boundaries.

For plugin/application lifecycle tests, bootstrap through the same runtime/composition entry point production uses where practical and assert shutdown/cleanup as well as startup.

A useful public example of lifecycle-style testing remains [Minecraft-CTF `FullPluginSimulationTest`](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/test/java/dev/tjxjnoobie/ctf/game/FullPluginSimulationTest.java), but current Tavall DI/composition rules take precedence over any older constructor-wiring shape in external examples.

# Git and Commit Discipline

## Authoritative Workflow

[GIT_WORKFLOW.md](../GIT_WORKFLOW.md) owns:

- working-branch rules;
- PR-first durable work surfaces;
- staging files/branches and ancestry when required;
- stacked/parallel PR behavior;
- owner direct-push/self-review authority;
- review/check requirements;
- production promotion;
- hotfix/reconciliation behavior.

This chapter intentionally does **not** state `working/* -> staging/* -> main` as a universal mandatory topology because the canonical workflow may represent staging through manifests, branches, stacked ancestry, or repository-specific rules.

##### Why

Branch topology is operational policy and evolves. Duplicating a simplified diagram in architecture docs creates a stale second authority that agents will eventually choose when it is more convenient. Naturally, convenience is undefeated in finding the wrong paragraph.

## Main and Review

`main` is production source.

- Ordinary contributor changes follow accountable GitHub review and configured checks under `GIT_WORKFLOW.md`.
- Authorized repository owners retain the explicit self-review/direct/bypass authority defined by `GIT_WORKFLOW.md` where repository-specific rules permit it.
- Direct owner authority is an exception owned by the workflow; it does not become permission for ordinary contributors or automation to bypass review.

##### Why

Saying “all changes must be reviewed before main” contradicted the explicit owner-authority path. The correct rule distinguishes normal contributor safety from deliberate owner responsibility instead of pretending GitHub can approve an author's own PR by force of documentation.

## Commit Messages

Use the structured commit format defined by the current Tavall Git workflow. At minimum, commit history must state:

- the typed/specific change;
- why it exists;
- what changed;
- what validation actually ran or why it did not.

Do not claim validation that did not run. Keep one commit to one coherent system boundary; implementation, tests, and docs for the same boundary may belong together.

## Coherent Change Boundaries

- Architecture migrations stay separate from unrelated feature work.
- Code, tests, DI bindings, imports, schemas, and docs move together when one contract changes.
- A PR remains the durable work surface for its branch until merged/superseded/abandoned according to `GIT_WORKFLOW.md`.
- Large PR counts are not themselves a defect; duplicate, contradictory, ownerless, or misleading work is.

# Review Checklist

- [ ] Tests exercise real behavior rather than mocking the subject under test.
- [ ] Tavall architecture tests are consumed through the repository test-suite boundary and inspect real production `main` outputs/source roots.
- [ ] Tavall-managed behavior uses production-equivalent DI composition in tests.
- [ ] External/platform boundaries are the primary fake/mock targets.
- [ ] PostgreSQL-specific behavior uses PostgreSQL-capable integration coverage.
- [ ] Failure, cleanup, reload, retry, and shutdown paths are covered where they exist.
- [ ] Test names describe behavior and packages match production.
- [ ] Branch/review/staging/promotion decisions follow `GIT_WORKFLOW.md`, not a duplicated diagram.
- [ ] Ordinary contributor review rules and explicit owner authority are not conflated.
- [ ] Commit messages report truthful validation and one coherent reason for the change.
