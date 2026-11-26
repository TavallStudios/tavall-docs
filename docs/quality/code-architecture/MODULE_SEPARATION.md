# Tavall Module Separation and Ownership Boundaries

> **Status:** Active
> **Authority:** Binding specialization of [Tavall Module Types](../MODULE_TYPES.md), [Code Architecture](../CODE_ARCHITECTURE.md), [DI and Orchestration](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md), and [Testing and Git](TESTING_AND_GIT.md).
> **Applies to:** New modules, repository extractions, SYSTEM/FEATURE composition, API ownership, packages, Gradle dependencies, runtime lifecycle, CI, and Tavall AI engineering-policy routing.
> **Rule:** Module classification, responsibility role, runtime owner, repository location, Gradle module identity, artifact identity, package identity, and deployment host are **separate decisions**. Current checked-in producer contracts and accepted system design take precedence over illustrative trees.
> **Owns:** The decision process and integration acceptance for separating Tavall modules, assigning their runtime/API owner, and connecting module-aware CD and host lifecycle.
> **Does not own:** The module type vocabulary, producer-specific API implementation, generic DI/registry internals, Cloud placement, canonical Gradle/CI policy, or assertion that future operators/deployments already work.

## 1. Boundary Selection: Package Before Module

For each proposed split record: **capability**, current owner and consumers, non-goal, smallest viable boundary, reason a smaller boundary fails, composing parent/fan-in, runtime owner, dependency direction, and an observable end-to-end acceptance path.

Choose the lowest sufficient boundary:

1. Existing class or package when there is one cohesive owner and no independently managed lifecycle.
2. Internal component when behavior needs its own interfaces/tests but ships and operates together.
3. Separate source/build module when typed dependency enforcement, reuse, ownership, tests, independently selected provider/configuration, or lifecycle actually require it.
4. Separate repository when the module has meaningful independent change/release/ownership pressure; a repo is **not** evidence of a new runtime.
5. Independently deployed `RUNTIME` only when a separate executable/process/service lifecycle exists.
6. Platform/exposed capability only with real cross-product consumers and an owned semantic API; HTTP, CLI, MCP, or UI exposure alone does not make a platform.

Do **not** create a FEATURE simply because a domain has several classes, a storage backend exists, or a directory has a memorable name. Stateless NLEW handlers, records, policy helpers, and cohesive logic remain packages until independent enable/disable/reload, provider selection, failure isolation, configuration, or test ownership is demonstrated. Record the **future split trigger** without prebuilding it.

## 2. Six Independent Identity Axes

Every real module records the following independently in its README and module-scoped Progression:

| Axis | Required answer | Non-equivalence |
| --- | --- | --- |
| Repository location | Owning Git repository and directory; whether the module is that repository's root build, a subdirectory module, or still a standalone repository awaiting consolidation | A repository is not a runtime, a new domain authority, or permanent ownership |
| Gradle module | Gradle project path and the build that includes it (for example `:tavall-content-web-frontend` in the Content build) | A Gradle module does not imply an independently deployable process, and a repository root is not the module identity |
| Artifact and Java package | Published Maven coordinate/artifact name and Java package root, including any intentionally preserved compatibility coordinate | Moving a module or repository is not a package rename and grants no new domain authority |
| Primary type | One of `RUNTIME`, `APPLICATION`, `SYSTEM`, `FEATURE`, `API`, `TOOLING`, `TEST_SUITE`, with zero or more secondary roles (`LIBRARY`, `PROVIDER`, `ADAPTER`, `INTEGRATION`) recorded beside it | `LIBRARY`/`PROVIDER`/`ADAPTER`/`INTEGRATION` are secondary roles, not primary types; a `PROVIDER` role does not imply its own process |
| Runtime, composition, and contract owner | Runtime owner (`Self`, a named runtime module, or `None`); composition parent/consumer of the module; which producer/runtime owns each typed API and its compatibility | `SYSTEM`/`FEATURE` does not imply `RUNTIME`; a source tree root is not automatically a SYSTEM; importing an API does not transfer ownership |
| Deployment host | The hostname/process/host boundary that actually serves the artifact today and the deployment document that records it | Being composed into a host is not deployment ownership, and exposing a route does not create a runtime |

A `SYSTEM` owns aggregation, fan-in, lifecycle coordination and an explicit consumer-facing capability surface. A `FEATURE` is an independently controllable child where independently controlled behavior has been justified. `RUNTIME` owns its executable lifecycle, host registration, deployment and APIs exposed by that runtime. A runtime-neutral API is owned by the domain producer/system that defines it, not automatically by the first FEATURE or adapter to import it. A `TEST_SUITE` verifies production modules but is not another implementation owner.

Each source/build module has its own `.tavallci/ci.yaml` and one module-scoped `PROGRESSION` document; SYSTEM-level Progression aggregates, but never replaces, child module evidence. Do not infer deployed state from a design diagram or the presence of a module folder.

### Module identity naming during separation

For independently defined source/build modules, a primary `SYSTEM` must use a module/artifact name ending in `-system`; a primary `RUNTIME` must end in `-runtime`. This does **not** apply to a parent repository directory, aggregate root, Java package, process selector, or an `APPLICATION` that happens to own an executable lifecycle. Use the real primary type, not an assumed type inferred from `*core`, `*app`, `*node`, `*worker`, or historical `*runtime` words. A secondary provider/adapter role does not change the naming rule.

Conflating these axes is the usual source of consolidation mistakes. A module named `<product>-web-frontend` is only a descriptive name: it does not create a module type, a new layer, or a new runtime, and the same name can describe a module in a product repository, an in-repository Web primitive library, or a standalone repository that has not been consolidated yet. Section 8 applies the axes to Tavall Web and its product browser surfaces.

A rename is an explicit *identity migration*: capture old/new Gradle paths, Maven coordinates, module IDs/descriptors, DI/registry bindings, dependency edges, module-local `.tavallci`, CD service profiles/templates, references in documentation and all callers. Prove consumer compilation, exact-source runtime composition, original module retirement, persisted desired-state/generation migration or compatible aliasing, artifact rollback and observed host behavior. Keep the previous identity until validation; no unverified bulk rename, no duplicate runtime authority, and no renaming repository roots just to satisfy a module rule. See [Module Types](../MODULE_TYPES.md#module-name-suffix-contract-2026-10-22) for canonical vocabulary.

## 3. Contracts and Dependency Direction

Write and inspect a dependency graph **before** moving code. The default direction is consumer/feature/adapter → stable typed API → selected implementation through Tavall DI and the canonical module registry. No consumer should need the implementation module's internals.

- Use Tavall's existing interface-first (`I*`) contracts, typed request/result/key/config/event models and generated `DependencyAccess`. Do not introduce a second DI container, static service locator, ad-hoc global map or per-SYSTEM lifecycle registry.
- A FEATURE imports only approved APIs/capabilities; it must not reach a sibling FEATURE through its concrete packages or silently depend on a second provider implementation.
- A runtime adapter (Paper, Velocity, Spring/HTTP, Discord, CLI, MCP/WebMCP) translates at the host boundary. It does not own the reusable business/domain rules it exposes.
- A provider/integration wrapper owns vendor-specific configuration, invocation, error translation, lifecycle and dependencies under the canonical Tavall wrapper boundary. Domain code does not scatter raw vendor SDK imports.
- A `tavall-*-api` artifact is justified by actual callers, a contract/version boundary, or independently consumable capability. Do not manufacture APIs for every SYSTEM or FEATURE.
- Shared contracts have an explicit owner and import direction. Cyclic module dependencies, duplicate domain authority and a generic `core/common/util` dumping ground are rejected. Existing package hierarchy guidance remains binding; module type names do not mandate `system` or `feature` Java package prefixes.

When a change crosses repositories, update the contract producer before downstream consumers, migrate imports through the approved API, and prove all intended consumers still work against the exact accepted artifact/version. The original consumer's responsibilities must be removed, not merely copied.

## 4. SYSTEM, FEATURE, and Runtime Lifecycle

Record for every FEATURE: parent SYSTEM, owning runtime, required capabilities/API imports, optional provider selection, enabled/disabled desired state, observed state and generation, activation order, failure path, teardown order, and what survives reload. The canonical Tavall DI/module-lifecycle infrastructure owns transition mechanics.

- Disabling a parent SYSTEM denies its dependent FEATURES and its aggregate capability. It must **not** disable unrelated SYSTEMs or restart the owning RUNTIME.
- Disabling/reloading one FEATURE isolates that FEATURE and its declared dependents; unrelated siblings remain available. A removed dependency, stale generation, denied capability, or failed rebinding fails closed.
- Use generation-safe registration/unregistration. Replacement must retire prior listeners, scheduler work, cache/registry handles, dependency aliases and references. A failed activation must leave the last healthy generation serving or fail closed, report the observed failure, and follow the authorized rollback/reconciliation policy. Artifact rollback and desired-profile rollback are **separate explicit CD decisions**, not side effects of pure DI profile resolution.
- API compatibility, startup/shutdown ordering, host permissions, failover, and rollback belong to the actual owning RUNTIME and deployment system. Do not claim dynamic loading/reload support until the host passes an E2E test.
- The universal `tavall module` command is a **planned** central operator surface in Tavall CLI, with intended `tavall-cd-cli` ownership in Tavall CI. The currently checked-in `tavall-ci-cli` supports `tavall ci` commands, **not** verified universal `tavall module` commands. Document planned permissions and contracts without representing that future interface as shipped.

## 5. Concrete Separation Examples and Package Layout

The following examples distinguish **accepted ownership direction** from **verified current deployment**; confirm exact source and deployed composition in the owning repository before describing any edge as implemented.

```text
Filesystem:
  tavall-filesystem-api         API, byte/integrity contracts
  tavall-filesystem             SYSTEM, composition/fan-in
    tavall-filesystem-zfs       FEATURE; secondary PROVIDER
    tavall-filesystem-nfs       FEATURE; secondary PROVIDER
  tavall-filesystem-test-suite  TEST_SUITE, validation only
  Tavall Cloud                  consuming RUNTIME / placement authority

Redis: tavall-database owns Redis and DB-facing state; it is not a Filesystem backend.
NLEW: tavall-nlew owns reusable Node/Lane/Environment/Workspace contracts and
  domain behavior; Cloud owns concrete control/placement/execution. Stateless
  NLEW per-record handlers can remain packages, not automatic FEATURES.
Web: tavall-web owns generic web runtime/framework concerns; tavall-web-mc
  owns the Minecraft Web surface; tavall-mc keeps Minecraft gameplay authority.
MC anti-cheat: tavall-mc-anticheat-system is presently a SYSTEM with
  bounded heuristic/observation behavior; its README explicitly says **no
  independently controllable FEATURE modules are introduced in this source slice**.
  The separate replay SYSTEM handles offline evaluation, not punishment.
  MC runtime linkage and later FEATURE extraction remain separately evidenced.
Content auto-post: tavall-content-auto-post-system has seven separately
  declared Gradle FEATURE modules (discovery, video-watch, creative, engagement,
  inbound, publishing, reporting). The Content runtime has a real lifecycle
  registry, generation-fenced operator API and PostgreSQL desired-state CAS.
  This is implemented in source with bounded PostgreSQL runtime tests, not
  evidence of external-platform posting or production deployment.
  Engagement owns approval/dispatch semantics; Inbound requires Engagement.
  Human approval remains mandatory before publication.
```

Example **illustrative** internal layout; preserve existing approved `org.tavall.<domain>` roots and package conventions instead of renaming packages by taxonomy:

```text
<system-module>/
  src/main/java/org/tavall/<domain>/
    api/                  (only contracts actually owned here)
    service/              (domain orchestration and fan-in)
    handler/              (bounded behavior)
    runtime/              (host binding when genuinely owned here)
<feature-module>/
  src/main/java/org/tavall/<domain>/<capability>/
    service/
    handler/
    adapter/              (only where an adapter role really exists)
```

A SYSTEM may contain stateless domain policy without a FEATURE. A repository may contain several modules without containing multiple runtimes. Minecraft keeps **one final plugin JAR** by design, even if its Gradle source contains numerous SYSTEM/FEATURE modules. One JAR does not grant Java hot-code replacement: enabling/disabling compiled-in functionality is different from installing new bytecode, which needs an explicitly supported classloader/isolation or full host update. Paper/Velocity reload and Kingdoms live-state constraints require host-specific E2E proof.

## 6. Migration and E2E Acceptance Checklist

Before coding: resolve current `tavall-docs` sections and producer source; classify every touched module; identify consumer/fan-in and ownership; map typed API imports; locate the actual DI registration and runtime host; list the concrete old responsibilities to remove; capture exact revision/PRs in the existing Tavall agent ledger/provenance.

During migration: keep one owning semantic contract, move implementation and tests together, update Gradle/composite project relationships and `.tavallci`, rewrite concrete consumers to APIs, retain required compatible contracts intentionally, and record actual lifecycle support rather than guessing.

Acceptance uses real classes and integration-first tests where practical:

1. **Static architecture**: canonical `tavall-test-suite-tools` inspects compiled production classes and test evidence; reject forbidden imports, dependency cycles, sibling implementation leaks, wrong package ownership and direct vendor imports outside wrappers.
2. **Composition**: bootstrap actual owning RUNTIME and Tavall DI; verify each declared SYSTEM/FEATURE is registered and reachable through the expected API/caller.
3. **Isolation**: disable/reload one FEATURE, prove unrelated siblings continue and stale references fail closed; disable SYSTEM and prove its aggregate is unavailable.
4. **Failure/rollback**: exercise unavailable dependency, failed startup, partial cleanup and rollback of artifact plus module state.
5. **End-to-end**: exercise real host surface (Paper/Velocity/Cloud/Web/CLI as relevant), runtime packaging, API compatibility, permission checks, restarts and observability. Validate on an exact source SHA and the actual target environment.
6. **Documentation/progression**: update each owning module README, module-scoped Progression and consumer migrations, report which tests ran and which did not; do not mistake design completion for deployed acceptance.

Route adjacent concerns to [Module Types](../MODULE_TYPES.md), [Namespaces and Package Rules](NAMESPACES_VARIABLES_AND_OOP.md), [DI](DEPENDENCY_INJECTION_AND_ORCHESTRATION.md), [Interfaces and Abstractions](INTERFACES_AND_ABSTRACTIONS.md), [Testing](TESTING_AND_GIT.md), [CI/CD](../CI_CD.md), and [Git Workflow](../GIT_WORKFLOW.md). This chapter specializes separation decisions and **does not duplicate** those authorities.

## 7. Module-Aware CI/CD, Profiles, and Host Loading

**Purpose:** make one validated set of source modules deployable to different authorized runtime targets with selectively active capabilities, without multiplying executable processes or rebuilding untracked variants. Compilation granularity, release granularity, desired composition and observed runtime state are independent; **neither a Gradle subproject nor a separate Git repository is intrinsically a hot-loadable Java module**.

### Exact source → artifact → target → runtime

```text
Tavall CI (canonical single Gradle orchestration)
  source repos @ exact SHAs -> composite Gradle / module checks / test suites
  -> immutable artifacts + source/dependency/artifact digests + CI evidence
  -> frozen delivery bundle and deployment policy (.tavallcd for deployable runtimes)
  -> Tavall CD authorization / release profile selection
  -> Tavall Cloud service Environment + concrete runtime placement
  -> RUNTIME composition using available artifact catalog + module profile
     Tavall DI: validate requested/disabled IDs, dependencies and load order
     Tavall Registry + host: actually activate, observe, unload, drain, rebind
  -> health/readiness evidence -> staged traffic promotion / explicit rollback
```

Source CI uses approved shared Executors and bounded operation workspaces; it does **not** require a service Environment, and Cloud does not replace the repository's Gradle structure or Tavall CI's policy. CD deploys the **same verified bytes** from the frozen bundle, never rebuilds a supposed equivalent per-target result. For targets using different module sets, the selected desired profile is a separate versioned configuration identity tied to the available artifact catalog, target and release; the profile is **not** the artifact digest.

The current `tavall-di` source already defines typed `DeploymentModuleProfile`, `EffectiveDeploymentModuleProfile` and `IModuleProfileResolver` / `ModuleProfileResolver` for immutable desired composition. They carry schema version, profile identity, runtime target, configuration generation, explicitly enabled/disabled IDs and dependency-first order. Unknown module IDs, disabled required dependencies and cycles fail closed. The producer's module-profile documentation explicitly states this is **pure resolution**; it does not persist desired state, mutate running registrations or implement dynamic reload. These profile APIs also require exact-source/dependency acceptance before implying a published runtime-compatible version.

`tavall-registry` and the consuming runtime own observed per-module/per-generation activation state and live transition orchestration. Cloud owns service Environment, placement and runtime recovery. Durable desired profile storage and operator mutation authority must be resolved at their designated CD/control owner; Redis/cache state is not independent durable authority. A SYSTEM cascades disable only to its dependent FEATURES; unrelated SYSTEMs remain available. Runtime health must expose requested generation, observed generation, failure reason, activation/readiness and cleanup progress before CD promotes traffic.

### What load, reload, and deploy mean

| Requested action | Intended owner | Required distinction / proof |
| --- | --- | --- |
| Enable/disable compiled-in FEATURE | Runtime/registry through canonical module lifecycle, with resolved profile | Register/unregister contract surfaces and stop/reject work; no bytecode swap implied |
| Reload FEATURE configuration or generation | Runtime host and Tavall DI/registry generation binding | Drain in-flight work, unregister listeners/tasks/aliases, atomically publish new generation and close old; unaffected siblings remain |
| Load/unload new binary/module bytecode | Only a host with an actual supported loader/isolation mechanism | Verify classloader ownership, linkage, transitive versions, platform hooks, cleanup and rollback; otherwise requires new runtime artifact/restart |
| Deploy module code through CD | Tavall CI/CD + Cloud runtime deployment authority | Exact-source build, immutable bundle, profile compatibility, service readiness and authorized promotion |
| Disable a SYSTEM | Its owning RUNTIME/module registry | Cascade to dependent FEATURES, reject stale calls; do not stop the entire application |
| Restore a failed promotion | CD orchestration + Cloud/host, by policy | Roll back artifact and/or desired profile to an explicitly accepted version and verify observed state; do not infer rollback from DI resolution alone |

### Verified and illustrative target scenarios

```text
Tavall Content source-backed composition (not a claim of live external posting):
  RUNTIME: tavall-content-runtime hosted/composed by tavall-content-app
  SYSTEM: tavall-content-auto-post-system
    discovery-feature          discovery capability
    video-watch-feature        verified video observations
    creative-feature           creative proposals
    engagement-feature         approvals/dispatch; required by inbound
    inbound-feature            incoming commentary / reply proposals
    publishing-feature         approved artifact → existing queue
    reporting-feature          analytics projection
  host: ModuleLifecycleRegistry with PostgreSQL desired-state CAS
  studio: generation-fenced API for enable/disable/reload of installed modules
  acceptance: opt-in PostgreSQL runtime tests; external provider E2E still open

Illustrative target-specific profile selection using that available artifact:
  content-development -> publishing FEATURE disabled
  content-production  -> publishing FEATURE enabled only with required
                         approvals, integrations and verified host acceptance

Tavall MC application (single plugin JAR; accepted packaging constraint)
  RUNTIME: stable Paper/Velocity hosts, product module descriptors in app jar
  SYSTEM: gameplay anti-cheat
    current audited slice: heuristic/observation behaviors inside SYSTEM
    later separately validated FEATURE loading: optional, not assumed
  Minecraft-specific /module exists on Paper; it does not install new code
  across releases and is not the planned global tavall module CLI

Tavall Web (checked-in Spring app composition, not a dynamic plugin claim)
  RUNTIME: tavall-web-app
  API: tavall-web-api owned by Web runtime
  frontend: frontend and Spring adapter modules as distinct capabilities
  product surfaces: independently owned repos selected as build inputs
    (web-mc remains presentation; tavall-mc retains game authority)
```

The Content FEATURE names above correspond to checked-in modules; the two deployment-target profile examples are **illustrative**, not verified production configuration. The runtime README documents `AutoPostRuntimeLifecyclePostgresTest` (7 cases) as environment-gated on `TAVALL_CONTENT_TEST_DATABASE_URL` and explicitly notes missing external account, AI, analytics and queue bridges. Disabled publishing must not be bypassed by alternate adapters, and account/post authorization remains mandatory. The Web example illustrates typed Gradle/source boundaries; current Spring app module mounting must not be portrayed as supporting zero-downtime live class replacement.

The approved operational acceptance suite exercises: exact candidate source, artifact and profile digests; target authorization; unavailable/disabled/cyclic dependencies; idempotent enable/disable; one-FEATURE reload and sibling isolation; parent cascade; concurrent requests during draining; stale generation access; restart reconstruction; failed activation rollback/fail-closed; health/traffic promotion; and runtime compatibility. Real host E2E is required for claims about hot loading or zero-downtime transitions. The generic `tavall module` operator CLI and universal any-target module-aware CD remain planned until their implementation and tests are verified.

See [CI/CD](../CI_CD.md) for source, evidence, frozen delivery and promotion authority; [NLEW and Service Ownership](../NLEW_AND_SERVICE_OWNERSHIP.md) for service Environments; [Module Types](../MODULE_TYPES.md) for classifications; and [Tavall DI module profiles](https://github.com/TavallStudios/tavall-di/blob/main/docs/module-profiles/README.md) for the current checked-in *desired-composition-only* contract.

## 8. Product Web Frontend Repository Consolidation (Tavall Web)

> **Status:** Active policy, partially executed in source. This section is the shared engineering rule for Tavall Web browser surfaces; it does not assert that every repository migration below is finished.
> **Coordination record:** [tavall-web#185](https://github.com/TavallStudios/tavall-web/issues/185) (closed coordination issue; the still-open per-repository issues cited below remain the actionable record) and [tavall-docs#127](https://github.com/TavallStudios/tavall-docs/issues/127).

### 8.1 Decision

Product-owned browser presentation should ordinarily live in the repository that owns the platform or product, as a correctly classified `<product>-web-frontend` module, and be composed by the shared `tavall-web-app` Spring HTTP/application host in `TavallStudios/tavall-web`.

Two Web-owned modules are intentionally *not* product presentation and stay in the Web repository:

- `tavall-web-frontend` (`:tavall-web-frontend`) is Web's pure Java rendering/Forge primitive library — reusable page contracts, typed HTML/CSS/animation composition, assets and rendering. It owns no product presentation and no host lifecycle.
- `tavall-web-dashboard` is the shared dashboard shell. Under the accepted decision it belongs to Web as a distinct dashboard module rather than to whichever product mounts a dashboard, promoting only genuinely reusable UI primitives into `tavall-web-frontend`. Dashboard *authorization* stays with the owning host/domain. It is still an active standalone repository today and is **not** yet a Web-repository module (8.6).

This is **source and repository consolidation**, not domain-authority, contract, or runtime consolidation. No product gains Web's authority, and Web gains none of the product's: moving pages does not move persistence, business rules, session security, or a Spring process. `*-web-frontend` is a descriptive module name, never a new module type, a new layer, or an automatic `SYSTEM`/`RUNTIME`/`APPLICATION` classification — the real type is read from the module's own README and source.

### 8.2 The six axes applied

Use this table when auditing or moving a browser surface. Fill every row from current source, never from the module name.

| Axis | Answers | Applied pattern | Non-equivalence to watch |
| --- | --- | --- | --- |
| Repository location | Which Git repository owns the presentation source? | The platform/product repository, for example the `tavall-content-web-frontend` module lives in `TavallStudios/tavall-content`; a legacy `tavall-web-<product>` repository is retired only after cutover acceptance | A repository is not a runtime, and a `tavall-web-*` repository name is not proof of Web ownership |
| Gradle module | Which Gradle project path builds it? | `:tavall-content-web-frontend` in the Content build, `:tavall-mc-web-frontend` in the MC build; declared in that repository's `settings.gradle.kts` | A module does not imply an independent process; a repository root build and its modules are different identities |
| Artifact and Java package | Which coordinate is consumed, which package root is declared? | The Web host consumes a typed artifact coordinate and the owner module keeps its Java package root; Web's exact-source manifest substitutes the consumed coordinate with the owner project (8.4) | A coordinate mapping or package move is not a domain-authority transfer. Verify the artifact identity in the owning repository; do not assume the directory name is the coordinate |
| Primary module type | What is recorded in the module README? | Consolidated product browser modules record `APPLICATION` with runtime `tavall-web-app` (the composed bounded product browser surface) — confirm per module instead of inferring | `APPLICATION` here is about the bounded browser surface it assembles, not about owning a deployable Web process |
| Runtime, composition, and contract owner | Which runtime loads it, who composes it, who owns the typed contract? | Runtime owner `tavall-web-app`; composition owner the shared Web application; the owning product keeps its API/client contract and Web keeps host, session and route authorization | Being composed by the host does not make Web the domain owner; importing a client contract does not transfer it |
| Deployment host | Which public host actually serves it, recorded where? | The product host (`content.tavall.org`, `mc.tavall.org`, …) served by the shared Web runtime, recorded in the owning runtime deployment record and the public host routing contract | A route or hostname does not create a new runtime; a successful compile is not deployment acceptance |

### 8.3 Ownership exceptions (verified capabilities, not name prefixes)

Some browser-facing capabilities must **not** be pushed into an arbitrary product owner. Each exception below is justified by what the repository or module actually owns today, not by a shared prefix.

| Capability | Current owner and verified capability | Why it is an exception |
| --- | --- | --- |
| Web Account, host, and security (shared auth/session boundary) | `TavallStudios/tavall-web-account` is an active single-module repository whose README states it provides pages and route constants only, is not a separately deployed auth service, and that Account security/MFA is served by the shared Web runtime; Web declares it as a source dependency (8.4). Parent-issue candidate `tavall-web-account` → `tavall-cloud/tavall-cloud-account-web-frontend` is **not started** and is sequenced behind account-security work, so it is not accepted policy | Identity, session, MFA and host security are one cross-product boundary. A product frontend module must never own or fork them |
| MCP transports | `TavallStudios/tavall-web-mcp` is an active repository publishing `org.tavall:tavall-web-mcp`; its README states it owns the browser-facing Spring MVC HTTP host boundary for `mcp.tavall.org` and the `POST /mcp/{service}` route declaration, and that MCP protocol/domain execution stays with its owning backend service | One transport/host-protocol boundary serves every product. It is not product presentation and must not be re-implemented per product |
| Docs | `TavallStudios/tavall-web-docs` is an active separate repository that owns the documentation-hub presentation surface and renders/links `TavallStudios/tavall-docs` as the canonical documentation source. The `tavall-web-docs/` directory in the Web repository is a boundary record only — explicitly *not* an independent Gradle module, artifact, service, or deployment unit | Documentation presentation is organization-wide, so it has no single product owner to move into |
| Store Tools and independently versioned libraries | `TavallStudios/tavall-web-store-tools` is legacy payment-compatibility source (`tavall-web-store-{stripe,paypal}[-api]` plus `tavall-web-store-test-suite`) whose README hands new provider development to `tavall-pay`; `tavall-web-frontend` is Web's Forge/rendering primitive module; `tavall-web-dashboard` is an active standalone Java-library repository whose README calls it the transport-neutral reusable dashboard shell consuming `tavall-web-api` and `tavall-web-frontend` | These are genuinely reusable, independently versioned libraries or deprecating compatibility source that is **Web-owned, not product-owned**. Burying one inside a product module would create a second copy of a shared contract |

Rules that follow from the exceptions:

- A product frontend module must not take ownership of sessions, login, MFA, authorization policy, MCP transport, documentation source, or payment provider logic.
- Web-host/identity tooling and genuinely reusable independently versioned tools are audited as exceptions; every other `tavall-web-*` repository is audited individually against this section before any move, because a similar name is not evidence that the repository is only frontend.
- Deprecating compatibility source is handled by its own migration gates, not by relocating it into a product owner.

### 8.4 Operational consolidation contract

**Exact-source CI module-local manifests.** Every moved module keeps its own build and module-local manifest in the owning repository, and the consuming Web source stays pinned to an exact owner revision:

- The owner repository's `.tavallci/ci.yaml` (repository root, or module-local where the repository keeps per-module manifests) declares the modules it builds and the sources it resolves. A moved module must be listed there and compile in the owner's own gate before Web consumes it.
- The Web repository's root `.tavallci/ci.yaml` declares each consumed product source as a pinned source dependency (identity + digest) plus a `substitutions` map from consumed Maven coordinates to owner Gradle project paths, and lists its own `modules`.
- Neither side may depend on a composite build of the other in a cycle: the owner builds its module, Web composes it. A move updates the owner manifest and the Web dependency pin; a move that only edits one side is incomplete.
- The Web application excludes each product module's transitive `org.tavall:tavall-web-frontend` so exactly one Forge primitive version is composed by the host.

**Dependency mapping and compatibility coordinates.** Read from the Web repository's root `.tavallci/ci.yaml` at the revision inspected for this policy (2026-11-26). Treat that file as the authority; the table is a projection of it, not a second contract.

| Owner source | Consumed coordinate | Owner Gradle project |
| --- | --- | --- |
| `TavallStudios/tavall-content` | `org.tavall:tavall-web-content` | `:tavall-content-web-frontend` |
| `TavallStudios/tavall-content` | `org.tavall.content:tavall-content-client` | `:tavall-content-client` |
| `TavallStudios/tavall-cloud` | `org.tavall:tavall-web-cloud` | `:tavall-cloud-web-frontend` |
| `TavallStudios/tavall-workflows` | `org.tavall:tavall-web-workflows` | `:tavall-workflows-web-frontend` |
| `TavallStudios/tavall-workflows` | `org.tavall.workflows:workflows-api`, `org.tavall.workflows:workflows-system` | `:workflows-api`, `:workflows-system` |
| `TavallStudios/tavall-commerce` | `org.tavall:tavall-web-commerce` | `:tavall-commerce-web-frontend` |
| `TavallStudios/tavall-qa` | `org.tavall:tavall-qa-web-frontend` | `:tavall-qa-web-frontend` |
| `TavallStudios/tavall-qa` | `org.tavall:tavall-qa-api`, `org.tavall:tavall-qa-system` | `:tavall-qa-api`, `:tavall-qa-system` |
| `TavallStudios/tavall-web-account` | `org.tavall:tavall-web-account` | `:` (account builds a single root module) |

Consequences of keeping consumed coordinates stable: the Web host can move from standalone source to owner source by changing the owner pin and the substitution, without rewriting product Java packages. Publish a coordinate rename only as a deliberate compatibility-tested migration (section 2 naming rules), never as a side effect of a file move.

**Pending PR and issue migration.** A repository move relinks its work rather than duplicating it:

1. The owning-repository issue records the move (old → new Gradle project, coordinate mapping, CI source identity, preserved package roots, route/host parity evidence).
2. Open PRs in the legacy repository stop taking new work: each is moved to the owner repository or closed with a stated reason and its remaining scope relinked. A move PR does not silently absorb unrelated pending work.
3. Documentation and progression move with the module: module README, module-scoped Progression and the owning runtime deployment record are updated in the same change set; the Web consolidation record links them.
4. The legacy repository is archived only after 8.4 closure criteria pass — never in the same step that first lands the source move.

**Rollout order.** Owner module source → owner exact-source CI gate → Web consumer pin + substitution update → Web exact-source CI gate on the exact candidate revision → deployment to a non-production environment → public route/host/asset parity verification → production promotion → legacy repository archival. Each step records the tested commit and artifact; a green compile is not route, deployment, or browser acceptance.

**Reversion.** Revert the Web consumer pin and substitution first: that is a single-manifest change restoring the last accepted source, and it leaves the owner module intact for the next attempt. Artifact rollback and deployment-profile rollback remain separate explicit deployment decisions (section 7). Do not delete owner module source to revert a Web integration, and do not archive a legacy repository while it is still the revert target.

**Archived-repository closure criteria.** A legacy `tavall-web-<product>` repository may be archived only when all of the following hold:

- the module source and tests live in the owner repository and pass that repository's exact-source CI gate;
- the Web consumer manifest pins the owner source and the Web gate passed on the exact composed revision;
- public hosts, routes, authentication, endpoint ownership and visuals were verified after deployment to the product host, with browser evidence recorded on the owning issue;
- no open consumer, branch, or pending PR still reads the legacy repository, and any remaining issue is relinked;
- the reversion path above is documented and was exercised or explicitly accepted;
- an explicit archival decision is recorded on the owning issue.

### 8.5 Consolidation status (verified 2026-11-26)

Status is reported per capability, not as a general claim that consolidation happened. Repository archival state was read from the GitHub API; module presence was read from the owner `settings.gradle.kts` where verified here.

| Legacy source | Owner module | Repository state | Evidence |
| --- | --- | --- | --- |
| `tavall-web-mc` | `tavall-mc` / `:tavall-mc-web-frontend` | Archived | Project path present in the MC build; [tavall-mc#431](https://github.com/TavallStudios/tavall-mc/issues/431) closed |
| `tavall-web-content` | `tavall-content` / `tavall-content-web-frontend` | Archived | Project path present in the Content build; [tavall-content#122](https://github.com/TavallStudios/tavall-content/issues/122) closed; Web substitution declared in 8.4 |
| `tavall-web-cloud` | `tavall-cloud` / `tavall-cloud-web-frontend` | Archived | Project path present in the Cloud build; [tavall-cloud#551](https://github.com/TavallStudios/tavall-cloud/issues/551) closed |
| `tavall-web-commerce` | `tavall-commerce` / `:tavall-commerce-web-frontend` | Archived | Consolidation PR merged into the Commerce staging line; project path **not** found on the Commerce `main` branch inspected for this policy, so main-line module location is unverified here. [tavall-commerce#4](https://github.com/TavallStudios/tavall-commerce/issues/4) closed |
| `tavall-web-qa` | `tavall-qa` / `tavall-qa-web-frontend` | Archived (`tavall-web-qa-ARCHIVED`) | Project path present in the QA build; [tavall-qa#22](https://github.com/TavallStudios/tavall-qa/issues/22) closed |
| `tavall-web-affiliates` | `tavall-affiliates` / `:tavall-affiliates-web-frontend` | Archived | Consolidation PR merged into the Affiliates staging line; project path **not** found on the Affiliates `main` branch inspected for this policy, so main-line module location is unverified here. [tavall-affiliates#7](https://github.com/TavallStudios/tavall-affiliates/issues/7) closed |
| `tavall-web-workflows` | `tavall-workflows` / `:tavall-workflows-web-frontend` | **Not archived** | Project path present in the Workflows build and consolidation PR merged into its staging line; archival deferred while owner-P0 work remains in the legacy repository — [tavall-workflows#17](https://github.com/TavallStudios/tavall-workflows/issues/17) open |

Web-owned exception modules in the same manifest era: `:tavall-web-frontend` (Forge/rendering primitives) and `:tavall-web-app` (host runtime) are Web modules; `tavall-web-mcp`, `tavall-web-account`, `tavall-web-docs` and `tavall-web-store-tools` remain separate repositories per 8.3.

### 8.6 Not migrated — open future work

These are **not** executed. Do not describe any of them as consolidated, and do not prebuild their target modules:

- Shared dashboard shell as a Web module — [tavall-web#186](https://github.com/TavallStudios/tavall-web/issues/186); `tavall-web-dashboard` remains an active standalone repository, and it is not in the Web repository's module list.
- AI Chat presentation — [tavall-ai#137](https://github.com/TavallStudios/tavall-ai/issues/137), pending an ownership/implementation inspection.
- Analytics dashboard presentation — [tavall-analytics#31](https://github.com/TavallStudios/tavall-analytics/issues/31), a new module only when justified.
- Ops and Account presentation consolidation — [tavall-cloud#570](https://github.com/TavallStudios/tavall-cloud/issues/570) and the Account item in [tavall-web#185](https://github.com/TavallStudios/tavall-web/issues/185), sequenced behind account-security and edge-routing work.
- Blog/Times, Biz, Contractors, Labs, MC Studio, Ventures and remaining `tavall-web-*` repositories — individually audited per 8.3, not batched.
- Any Web-side consumption of product modules that the Web `main` manifest does not declare (for example the MC frontend consumed through Web staging work): the manifest, not this table, decides.

See [Module Types](../MODULE_TYPES.md#repository-module-names-that-are-not-types-2026-11-26) for the name-versus-type rule, [CI/CD](../CI_CD.md) for manifest, evidence and promotion authority, [VERSIONING](../VERSIONING.md) for artifact/source identity, [Web Architecture](../WEB_ARCHITECTURE.md) for route ownership, and [NLEW and Service Ownership](../NLEW_AND_SERVICE_OWNERSHIP.md) for host/service placement.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `PRIMARY` | `TavallStudios/tavall-docs/docs/quality/code-architecture/MODULE_SEPARATION.md` | 2026-11-26 | [tavall-docs #127](https://github.com/TavallStudios/tavall-docs/issues/127); module, coordinate and archival facts read from the owning repositories on 2026-11-26 |
| Notion | `UNVERIFIED` | — | 2026-11-26 | Twin **not** reconciled: this consolidation policy has not been mirrored to or confirmed against Notion. Pending Notion reconciliation under #127; do not treat Notion as updated |

### Update History

| Date | Surface | Event | Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-10-21 | GitHub | `CREATED` | Same canonical path | [PR #74](https://github.com/TavallStudios/tavall-docs/pull/74) | Added canonical SYSTEM/FEATURE separation, runtime/contract ownership, source-backed examples, module-aware CD/profile/host lifecycle and integration acceptance. |
| 2026-10-22 | GitHub | `UPDATED` | Same canonical path | [PR #77](https://github.com/TavallStudios/tavall-docs/pull/77) | Added Gradle module identity suffix migration rules and explicit repository-root exemptions. |
| 2026-11-26 | GitHub | `UPDATED` | Same canonical path | [Issue #127](https://github.com/TavallStudios/tavall-docs/issues/127) | Separated repository location, Gradle module, artifact/package, primary type, runtime/composition/contract owner and deployment host as distinct axes; added the Web product-frontend repository consolidation policy, capability-grounded ownership exceptions, the exact-source manifest/coordinate contract, rollout/reversion/archival criteria, verified per-repository status and open unmigrated work. |

</details>
