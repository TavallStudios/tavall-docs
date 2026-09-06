# Project Novus Routers and Delegation

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

### Event Router Pattern

Event routers receive Paper events and route them to one or more handlers.

Event routers should stay thin.

They should not own game rules.

They should not become event handlers with a fake mustache.

#### Bad Event Router Pattern

```java
public final class PlayerInteractRouter {

    public void onPlayerInteract(PlayerInteractEvent event) {
        Player player = event.getPlayer();

        if (player.hasPermission("admin")) {
            event.setCancelled(false);
            return;
        }

        event.setCancelled(true);
    }
}
```

##### Why

The router owns the rule.

The permission is a raw string.

The router is no longer routing.

#### Good Event Router Pattern

```java
public final class PlayerInteractRouter {

    private final FlagInteractHandler flagInteractHandler;
    private final StaffToolInteractHandler staffToolInteractHandler;

    public void onPlayerInteract(PlayerInteractEvent event) {
        flagInteractHandler.onPlayerInteract(event);
        staffToolInteractHandler.onPlayerInteract(event);
    }
}
```

##### Why

The router receives the event.

The router delegates to the handlers that own behavior.

Multiple handlers can subscribe to the same Paper event without stuffing everything into one listener.

#### Event Router Rules

Event routers should:

* Receive Paper events.
* Delegate to one or more handlers.
* Keep ordering intentional.
* Stay easy to test.
* Avoid gameplay rules.
* Avoid database work.
* Avoid cache mutation unless the router is explicitly designed for a tiny routing-only cache concern.

### Command Delegation Pattern

Command classes should parse command input and delegate behavior.

They should not own core system rules.

#### Bad Command Delegation Pattern

```java
public final class BanCommand {

    public void execute(CommandSender sender, String[] args) {
        Player target = server.getPlayer(args[0]);

        target.banPlayer(args[1]);
    }
}
```

##### Why

The command directly finds the target, assumes arguments are valid, and applies punishment.

No request object.

No result object.

No permission flow.

No power-level flow.

No dignity.

#### Good Command Delegation Pattern

```java
public final class BanCommand {

    private final PunishmentRequestBuilder punishmentRequestBuilder;
    private final PunishmentHandler punishmentHandler;
    private final PunishmentResultMessageHandler punishmentResultMessageHandler;

    public void execute(CommandSender sender, String[] args) {
        PunishmentRequest punishmentRequest = punishmentRequestBuilder.buildPunishmentRequest(
            sender,
            args
        );

        PunishmentResult punishmentResult = punishmentHandler.banPlayer(
            punishmentRequest
        );

        punishmentResultMessageHandler.sendPunishmentResultMessage(
            sender,
            punishmentResult
        );
    }
}
```

##### Why

The command builds a request.

The handler owns punishment behavior.

The result controls output.

### Event Delegation Pattern

Paper event listeners should receive the event and delegate behavior.

They should not own system rules.

#### Bad Event Delegation Pattern

```java
public final class AsyncPlayerChatListener {

    public void onChat(AsyncPlayerChatEvent event) {
        Player player = event.getPlayer();
        String message = event.getMessage();

        if (message.contains("&k")) {
            event.setCancelled(true);
        }

        event.setFormat(player.getName() + ": " + message);
    }
}
```

##### Why

The listener owns formatting rules, color rules, and event mutation.

That logic will grow fast because chat systems are apparently born feral.

#### Good Event Delegation Pattern

```java
public final class AsyncPlayerChatListener {

    private final ChatMessageHandler chatMessageHandler;

    public void onChat(AsyncPlayerChatEvent event) {
        Player player = event.getPlayer();
        String rawMessage = event.getMessage();

        ChatMessageRequest chatMessageRequest = new ChatMessageRequest(
            player,
            rawMessage
        );

        ChatMessageResult chatMessageResult = chatMessageHandler.processChatMessage(
            chatMessageRequest
        );

        boolean cancelled = chatMessageResult.isCancelled();
        String formattedMessage = chatMessageResult.getFormattedMessage();

        event.setCancelled(cancelled);
        event.setFormat(formattedMessage);
    }
}
```

##### Why

The listener receives the event.

The handler processes the chat message.

The result tells the listener what to do.
