# Tavall Enums & Extensible Enum Values

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

Tavall systems distinguish between **closed enum sets** and **extensible enum families**. Using the wrong mechanism leads to either fragile closed sets that break multi-module plugins, or over-engineered open sets for strictly closed domains.

---

## The Core Distinction

| Dimension | Native Java `enum` | `CustomEnum<T>` (`tavall-custom-enum-java`) |
|---|---|---|
| **Set Nature** | **Closed set**, fully known at compile-time within a single compilation unit. | **Extensible family**, dynamically expandable at runtime across independent plugins/modules. |
| **Declaration** | `public enum Priority { LOW, HIGH }` | `public final class ThreadType extends CustomEnum<ThreadType>` |
| **Extension** | Impossible across modules without recompiling the original enum. | Any authorized module or plugin can call `Family.register("NAME")`. |
| **Identity Semantics** | Reference equality (`==`) and identity hash code. | Reference equality (`==`) and `System.identityHashCode(this)`. |
| **Lookup** | `Enum.valueOf(Class, String)` | `CustomEnum.valueOf(Class<T>, String)` |
| **Iteration** | `Enum.values()` (array copy) | `CustomEnum.values(Class<T>)` (immutable `List<T>`) |
| **Concurrency** | Built into JVM classloader guarantees. | Thread-safe registration via synchronized `EnumValues` and `ConcurrentHashMap`. |
| **Canonical Usage** | Fixed domain choices, states, modes, priorities. | Mod/plugin extension points, runtime thread types, cross-module capability identifiers. |

---

## When to Use Native Java `enum`

Use native Java `enum` when the set of values is **closed and invariant**:
- Life-cycle phases within a known domain (e.g. `EventStatus.PENDING`, `EventStatus.FIRED`, `EventStatus.SUCCESS`).
- Fixed configuration tiers (e.g. `EventPriority.LOW`, `EventPriority.NORMAL`, `EventPriority.HIGH`, `EventPriority.CRITICAL`).
- HTTP/REST status mappings, core mathematical axes, or single-module protocol states.
- When `switch` exhaustive pattern matching across the complete set is required at compile-time.

```java
public enum EventPriority {
    LOW(0),
    NORMAL(5),
    HIGH(10),
    CRITICAL(15);

    private final int level;
    EventPriority(int level) { this.level = level; }
    public int getLevel() { return level; }
}
```

---

## When to Use `CustomEnum`

Use `CustomEnum<T>` when the set of values is **open and extensible**:
- A base platform or core library defines the type, but independent plugins, modules, or game modes must register additional values without editing the core library.
- Thread types, task dispatch categories, database capability providers, or Minecraft custom item categories contributed across separate JARs.
- Multiple separate contributors may reference the same conceptual value (e.g. `DATABASE`), where repeated registration converges safely on the exact same canonical instance.

### Canonical `CustomEnum` Definition Pattern

```java
package org.tavall.thread;

import org.tavall.util.CustomEnum;

public final class ThreadType extends CustomEnum<ThreadType> {

    private ThreadType(String name) {
        super(name);
    }

    /**
     * Registers or retrieves the canonical ThreadType for the given name.
     */
    public static ThreadType register(String name) {
        return CustomEnum.register(ThreadType.class, name, ThreadType::new);
    }
}
```

### Contributing Values from Independent Modules

Independent modules can contribute values without altering core classes:

```java
// In tavall-database:
public final class DatabaseThreadTypes {
    public static final ThreadType DATABASE = ThreadType.register("DATABASE");
    private DatabaseThreadTypes() {}
}

// In tavall-ai:
public final class AiThreadTypes {
    public static final ThreadType AI = ThreadType.register("AI");
    private AiThreadTypes() {}
}
```

---

## Runtime Semantics & Contracts

### 1. Identity and Equality (`==`)
`CustomEnum` overrides `equals` and `hashCode` to enforce identity semantics:
- `equals(Object other)` returns `this == other`.
- `hashCode()` returns `System.identityHashCode(this)`.
- Never use `.equals()` on `CustomEnum` values; treat them identically to native Java enums with `==`.

### 2. Idempotent Registration
Repeated calls to `register(type, name, factory)` for the same family and name return the **same canonical instance**. No duplicate instances exist for a single name within an enum family.

### 3. Strict Name Validation
Names must:
- Not be null.
- Not be blank.
- Not contain leading or trailing whitespace (`name.equals(name.trim())`).
- Exact case matters: lookup via `CustomEnum.valueOf(ThreadType.class, "AI")` will not match `"ai"`.

### 4. Concurrency & Thread Safety
`CustomEnum` internally manages a `ConcurrentHashMap` of families (`VALUES`), where each family's internal storage (`EnumValues<T>`) synchronizes mutation. Registration and lookups are safe under concurrent multi-threaded execution.

### 5. Immutability of Values Snapshot
`CustomEnum.values(type)` returns an immutable snapshot list (`List.copyOf`). Consumers cannot mutate the registry by modifying the returned list.

---

## Anti-Patterns

❌ **Stringly-Typed Enums**:
Using raw `String` constants (`public static final String TYPE = "DATABASE";`) scattered across projects instead of `CustomEnum` or native `enum`. Leads to typos and eliminates compiler type safety.

❌ **Extending Native Enums via Interface**:
Defining an interface `IEventTag` and implementing it across multiple standard `enum` types. This destroys `switch` pattern matching, breaks identity semantics across classes, and causes comparison bugs.

❌ **Public Constructor on `CustomEnum`**:
Allowing `new MyCustomEnum("NAME")` outside `CustomEnum.register(...)`. Direct construction bypasses canonical instance caching and violates identity equality (`==`). Always keep constructors `private` or package-private to the registering factory.

❌ **Using `CustomEnum` for Static Closed Sets**:
Using `CustomEnum` where the set of values is guaranteed never to change across modules (e.g. `DayOfWeek`, `Direction`). Native `enum` is simpler, faster, and supported directly by the JVM and compiler.
