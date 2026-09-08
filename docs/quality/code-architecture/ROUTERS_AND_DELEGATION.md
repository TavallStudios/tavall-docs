# Tavall Routers and Delegation

> **Status:** Active  
> **Authority:** Binding chapter of [Tavall Studios Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** Tavall production modules, contributors, automation, generated code, reviews, and AI-assisted development

## Router Pattern

A Router selects one or more focused handlers/capabilities and delegates. It does not become the behavior being routed.

Routers should:

- receive typed/platform input;
- select/delegate intentionally;
- define ordering where multiple targets run;
- define duplicate/unknown-route behavior;
- remain easy to test;
- avoid durable persistence, cache/registry ownership, and unrelated domain rules.

##### Why

Routing is selection and ordering. Once the router owns the rule, storage, and output, the selection boundary disappears and the class becomes an oversized Handler wearing a fake mustache.

## Event Router Pattern

Platform event routers adapt events to focused handlers.

Bad:

```java
public void onPlayerInteract(PlayerInteractEvent event) {
    if (!event.getPlayer().hasPermission("admin")) {
        event.setCancelled(true);
    }
}
```

Good shape:

```java
@DelegatesTo(IPlayerInteractRouter.class)
public final class PlayerInteractRouter
        implements IPlayerInteractRouter,
        DependencyAccess<
                IFlagInteractHandler,
                IStaffToolInteractHandler
        > {

    @Override
    public void route(PlayerInteractEvent event) {
        IDependencyMap dependencies = getInstance();
        dependencies.iFlagInteractHandler().onPlayerInteract(event);
        dependencies.iStaffToolInteractHandler().onPlayerInteract(event);
    }
}
```

##### Why

The event router owns which handlers receive the event and in what order. The handlers own their focused behavior. Managed collaborators stay visible through Tavall DI rather than constructor-captured fields.

## Command/Controller Delegation

Commands, web controllers, Discord actions, and other external-input adapters should parse/validate transport input and delegate one typed operation.

```java
public void execute(CommandSender sender, String[] args) {
    RankUpdateRequest request = parseRankUpdateRequest(sender, args);
    RankUpdateResult result = getRankUpdateHandler().updatePlayerRank(request);
    sendRankUpdateResult(sender, result);
}
```

Transport parsing and output adaptation remain at the edge; reusable rank-update policy remains in the domain handler/service/orchestrator.

##### Why

Input syntax changes independently from domain behavior. Typed delegation lets one domain operation serve commands, web, Discord, jobs, tests, or future surfaces without copying the rule.

## Listener Delegation

Listeners receive platform events and delegate. They should not perform durable I/O, generic CRUD, cache ownership, or reusable domain policy directly.

Good shape:

```java
@DelegatesTo(IChatListener.class)
public final class ChatListener
        implements IChatListener,
        DependencyAccess<IChatMessageHandler> {

    public void onChat(ChatEvent event) {
        ChatMessageRequest request = new ChatMessageRequest(
                event.playerId(),
                event.message()
        );

        ChatMessageResult result = getInstance().process(request);
        applyResult(event, result);
    }
}
```

##### Why

A listener is a platform lifecycle adapter. Keeping domain behavior elsewhere makes the rule testable without constructing the platform event and keeps asynchronous/thread rules at the correct edge.

## Persistence and State Rejections

Routers/listeners/commands/controllers do not:

- open JDBC/EntityManager/JPA callbacks;
- create `Postgres*Repository`, `*Database`, or `*Store` wrappers for ordinary entity CRUD;
- own mutable keyed runtime/cache state;
- maintain operation task maps;
- statically locate managed dependencies.

Durable work goes through Tavall Database/owning data policy. Runtime keyed state goes through Registry/Cache/dedicated runtime owners.

##### Why

Routing/input surfaces are invoked because something happened externally. Giving them storage ownership couples authority/lifetime to event delivery frequency rather than the domain system that actually owns the state.

## Review Checklist

- [ ] The router selects/delegates rather than implementing domain behavior.
- [ ] Ordering/unknown-route behavior is explicit.
- [ ] External-input adapters build/resolve typed requests and adapt typed results.
- [ ] Managed collaborators use Tavall DI.
- [ ] Routers/listeners/controllers own no durable or keyed runtime storage.
- [ ] Platform/input behavior does not duplicate reusable domain rules.
