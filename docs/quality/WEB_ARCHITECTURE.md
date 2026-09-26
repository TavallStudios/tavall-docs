# Tavall Web Architecture

> **Status:** Active  
> **Authority:** Binding Tavall Studios web architecture guidance  
> **Applies to:** Tavall-owned web applications, Spring web modules, controllers, endpoint definitions, templates, clients, automation, generated code, reviews, and AI-assisted development

Tavall web architecture keeps externally reachable routes explicit, typed, centrally owned, and mechanically discoverable. Public exposure is treated as a deliberate boundary. Internal infrastructure and internal-only APIs do not become public merely because HTTP could technically reach them.

## Endpoints & Routing

Application route paths have one compile-time source of truth: `Routes.java`. Endpoint enums attach semantic endpoint identity and Spring `RequestMethod` metadata to those paths. Tavall Registry provides the runtime and compile-time endpoint mapping/indexing layer where endpoint discovery, validation, or lookup is required.

Controllers, security configuration, templates, clients, and generated configuration consume declared routes. They do not redeclare application route literals.

### Canonical Shape

```text
Routes.java
    compile-time route path source of truth
        |
        +-- Routes.Auth
        +-- Routes.Tracking
        +-- Routes.Dashboard
        |      +-- Routes.Dashboard.Merchant
        |      +-- Routes.Dashboard.Driver
        |      `-- Routes.Dashboard.Superuser
        `-- Routes.Api
               `-- bounded API route groups

*Endpoints.java
    semantic endpoint identity
    route reference + Spring RequestMethod
        |
        `-- registered/indexed through Tavall Registry

Consumers
    controllers
    security configuration
    templates
    clients
    generated client configuration
    architecture validation
```

The route definition and endpoint metadata are related but intentionally distinct:

- `Routes.java` owns path strings and path composition;
- `*Endpoints` enums identify callable endpoints and their HTTP methods;
- Tavall Registry owns endpoint registration, keyed lookup, indexing, and runtime discovery when those capabilities are needed;
- controllers and other adapters consume the contract rather than becoming route owners.

##### Why

A route path is shared compile-time vocabulary. Spring annotations require compile-time constants, so the canonical path must remain directly usable from annotations without introducing duplicate `*_PATH` constants or forwarding wrappers.

Endpoint metadata has a different job. An enum can pair the canonical route with a typed `RequestMethod` while remaining compact, enumerable, and suitable for registry-backed discovery. Tavall Registry already owns Tavall runtime identity and lookup semantics, so a second endpoint catalog abstraction would duplicate infrastructure we already have.

### `Routes.java`

`Routes.java` is a final, construction-inaccessible namespace for application route constants. It groups routes hierarchically by web surface and bounded context.

```java
public final class Routes {

    private Routes() {}

    public static final String ROOT = "/";

    public static final class Auth {
        public static final String LOGIN = "/login";
        public static final String LOGOUT = "/logout";

        private Auth() {}
    }

    public static final class Dashboard {
        public static final String ROOT = "/dashboard";
        public static final String LOGIN = ROOT + "/login";

        private Dashboard() {}

        public static final class Merchant {
            public static final String ROOT = Dashboard.ROOT + "/merchant";
            public static final String SHIPMENTS = ROOT + "/shipments";
            public static final String ROUTES = ROOT + "/routes";
            public static final String ROUTE_DETAILS = ROUTES + "/{routeId}/details";

            private Merchant() {}
        }
    }

    public static final class Api {
        public static final String ROOT = "/api/v1";

        private Api() {}

        public static final class Merchant {
            public static final String ROOT = Api.ROOT + "/merchant";
            public static final String CREATE_SHIPMENT = ROOT + "/shipment/create";
            public static final String CREATE_ROUTE = ROOT + "/routes/create";

            private Merchant() {}
        }
    }
}
```

The hierarchy is part of the contract. Prefer composition such as `Dashboard.ROOT + "/merchant"` over repeatedly spelling the full path.

Do not add convenience methods to `Routes.java` for runtime behavior, authorization, persistence, I/O, service lookup, or endpoint discovery. It is a compile-time route namespace, not a web service disguised as a constants class.

##### Why

Flat route constant files eventually become unstructured lists where ownership can only be inferred from increasingly long names. Nested namespaces preserve the relationship between a surface, its bounded context, and its children while keeping every value a Java compile-time constant.

This is also a rare acceptable Tavall inner-class pattern: the nested classes are static namespace groupings with no runtime object graph, mutable state, hidden lifecycle, or enclosing-instance coupling. They make the route hierarchy visible without creating dozens of tiny files whose only job is holding constants.

### Endpoint Enums

Endpoint enums attach typed HTTP behavior to canonical route constants. They do not own duplicate route literals.

```java
public enum MerchantEndpoints {

    SHIPMENTS(
            Routes.Dashboard.Merchant.SHIPMENTS,
            RequestMethod.GET
    ),

    CREATE_SHIPMENT(
            Routes.Api.Merchant.CREATE_SHIPMENT,
            RequestMethod.POST
    ),

    CREATE_ROUTE(
            Routes.Api.Merchant.CREATE_ROUTE,
            RequestMethod.POST
    );

    private final String route;
    private final RequestMethod method;

    MerchantEndpoints(String route, RequestMethod method) {
        this.route = route;
        this.method = method;
    }

    public String route() {
        return route;
    }

    public RequestMethod method() {
        return method;
    }
}
```

Use Spring `RequestMethod` directly for Spring web endpoint metadata. Do not introduce an `AppEndpoint` interface merely to expose `route()` and `method()` when the enum already owns those values and no genuine polymorphic boundary is required.

Do not represent methods as strings such as `"GET"` or `"POST"`.

##### Why

The enum is already the typed endpoint definition. Adding a one-method or two-method interface solely because multiple endpoint enums happen to have the same fields creates abstraction without behavior. Typed `RequestMethod` values also eliminate invalid method strings and make the Spring contract explicit.

### Tavall Registry Endpoint Mapping

When the application needs a complete endpoint index, endpoint lookup, generated client map, validation pass, diagnostics, or runtime discovery, register endpoint definitions through Tavall Registry rather than introducing an `EndpointCatalog` singleton or maintaining another manually aggregated list.

The registry mapping should preserve at minimum:

- endpoint identity;
- canonical route;
- `RequestMethod`;
- owning endpoint group or bounded context when useful to the consumer.

Registration/bootstrap code may enumerate endpoint enums and register their definitions. Consumers query the registry contract rather than knowing every endpoint enum class.

The exact registry API is governed by the checked-in `tavall-registry` version. Web architecture must consume that contract rather than recreating registry behavior locally.

##### Why

Endpoint discovery is keyed runtime identity and lookup. That is Registry ownership under Tavall architecture. A hand-maintained `EndpointCatalog` would become a second registry with worse lifecycle semantics and another list that somebody, eventually a sleep-deprived human or an extremely confident agent, forgets to update.

### Controllers

Spring controllers consume `Routes` constants directly:

```java
@GetMapping(Routes.Dashboard.Merchant.SHIPMENTS)
public String shipments() {
    return "dashboard/merchant/shipments";
}
```

Do not write application route literals directly in `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`, or `@RequestMapping` when the route belongs to the application contract.

Controllers remain input adapters. Centralizing a route does not move domain behavior into the controller or into `Routes`.

##### Why

A controller should answer what happens when input reaches the application, not independently define where the application exists. Central route ownership prevents annotations, templates, security rules, and clients from silently drifting onto different paths.

### Security Consumers

Security configuration consumes the same route constants:

```java
.requestMatchers(
        Routes.ROOT,
        Routes.Auth.LOGIN,
        Routes.Dashboard.LOGIN
).permitAll()
```

Authorization policy does not belong in `Routes.java`. Security patterns such as `Routes.Dashboard.ROOT + "/**"` may be derived by security-owned configuration where wildcard matching is required.

A route being public does not imply unrestricted access. Publicly reachable routes remain gated according to their authentication, authorization, rate-limiting, validation, and application security requirements.

##### Why

Location and access policy are separate concerns. Routes define stable addresses. Security defines who may use them and under what conditions. Combining the two turns route constants into a policy engine and makes security behavior harder to audit.

### Public and Internal Network Boundaries

Tavall distinguishes application routes from network exposure.

Public domains and public origin IP addresses are for intentionally public web surfaces only. Internal infrastructure must not be exposed through public domain links or public origin IPs merely to make service-to-service communication convenient.

Internal infrastructure communication uses Tavall private networking. Internal-code-only APIs remain internal and are reached through private network boundaries appropriate to the owning service/runtime. Public applications may expose intentionally public API routes, but those routes remain gated and must not reveal private infrastructure topology.

Therefore:

- public route does not mean unauthenticated route;
- internal route does not mean "public URL with an obscure path";
- internal services communicate over private networking rather than public origins;
- private infrastructure addresses are not published as application links;
- public-facing services do not expose private origin IPs as a supported access path;
- internal-code-only APIs are not promoted into public API surface for implementation convenience.

##### Why

Path naming is not a security boundary. `/internal/...` on a public origin is still public infrastructure if the network can reach it. Keeping internal traffic on the private network reduces accidental exposure, prevents public routing conventions from becoming infrastructure discovery mechanisms, and makes the application's declared public surface match its actual network boundary.

### URI Expansion

Parameterized route templates remain canonical constants:

```java
public static final String ROUTE_DETAILS = ROUTES + "/{routeId}/details";
```

Code that needs a concrete URI expands the template through the web/framework URI-building facility used by that module. Do not mutate `Routes` into a collection of unrelated runtime helper methods merely to replace path variables.

##### Why

The template is part of the route contract. Concrete URI construction is runtime transformation. Keeping those responsibilities separate preserves `Routes.java` as a compile-time namespace and avoids ad hoc string replacement becoming routing infrastructure.

### Prohibited Duplication

Do not create parallel representations such as:

```java
CREATE_ROUTE("/api/v1/merchant/routes/create", RequestMethod.POST);

public static final String CREATE_ROUTE_PATH =
        "/api/v1/merchant/routes/create";
```

or:

```java
public static final String MERCHANT_CREATE_ROUTE =
        MerchantEndpoints.CREATE_ROUTE_PATH;
```

The canonical form is:

```java
// Routes.java
public static final String CREATE_ROUTE = ROOT + "/routes/create";

// MerchantEndpoints.java
CREATE_ROUTE(Routes.Api.Merchant.CREATE_ROUTE, RequestMethod.POST);
```

One path, one owner.

##### Why

Aliases look harmless until one changes without the other. Duplicate route constants create multiple apparent sources of truth, weaken architecture validation, and force callers to guess which layer owns the contract.

### Architecture Validation

Tavall Architecture Tests should enforce the routing contract where mechanically practical. Validation should detect at least:

- application route literals in Spring mapping annotations outside the canonical route definition;
- duplicate canonical route values where duplicates are not explicitly intentional;
- endpoint enums that redeclare route literals instead of referencing `Routes`;
- string HTTP methods where `RequestMethod` should be used;
- malformed paths, accidental `//`, and invalid path-variable syntax;
- duplicate endpoint method + route registrations;
- application-owned endpoint catalogs or mutable endpoint maps that duplicate Tavall Registry ownership.

Network-boundary validation belongs with deployment, service, and infrastructure policy rather than pretending a Java architecture test can prove a private network exists by staring very intensely at source code.

##### Why

The pattern is valuable only if drift is detectable. Architecture tests should enforce source-level ownership, while deployment and network controls enforce reachability. Each layer verifies the thing it can actually know.

### Review

Reject endpoint/routing code when:

- an application route literal is duplicated outside `Routes.java` without a framework-required reason;
- a route namespace inner class owns runtime behavior or mutable state;
- an endpoint enum duplicates route strings;
- HTTP methods are represented as arbitrary strings instead of `RequestMethod`;
- an `AppEndpoint`-style abstraction exists only to mirror fields already owned by endpoint enums;
- a local endpoint catalog duplicates Tavall Registry;
- controllers become route-definition owners;
- authorization policy is embedded into route constants;
- an internal API depends on a public domain or public origin IP when private networking is available;
- `/internal` or similar naming is treated as a security boundary;
- private infrastructure topology is exposed as part of the public application contract.
