# Project Novus Testing and Git Discipline

> **Status:** Active  
> **Authority:** Binding chapter of [Project Novus Code Architecture](../CODE_ARCHITECTURE.md)  
> **Applies to:** All Project Novus modules, contributors, automation, generated code, and AI-assisted development

This chapter is separated for navigation only. Its rules are part of the authoritative Project Novus code architecture and are not optional supplemental guidance.

## Testing
### Testing Stack

* JUnit 5: Core unit, contract, and integration test execution.
* Mockito: Narrow mocking of Paper or Velocity platform boundaries when a delegate or test implementation is impractical.
* Testcontainers: PostgreSQL, Redis, and other real infrastructure dependencies.
* Mineflayer with raw TypeScript: Minecraft command, routing, lifecycle, and interaction scenarios.
* Gradle test suites: Repository unit, contract, and explicit integration-test execution.

### How to Write Tests / Testing Rules

We want to write **delegate-style integration tests**.

That means tests should use real data objects, real enums, real interfaces, and real concrete behavior from the codebase whenever possible.

The test should build realistic input, call real system behavior, and let JUnit tell us what happened.

Some things can still be faked:

* UUIDs
* In-memory repositories
* Test clocks
* Fake players/senders
* Test-only data sources

Do not mock the thing being tested.  
Do not test private methods.  
Do not write tests that only prove Mockito knows how to lie.

#### Test Class Rules

* Test helper objects used by a test should live at the class level inside that test class when they are part of the repeated test setup.
* Use real domain objects.
* Use real behavior when possible.
* Fake only external boundaries.
* Keep setup readable.
* Extract important values into local variables.
* Put repeated test setup at the class level.
* Match the test package structure to the main package structure.
* Name test classes after the tested class with Test at the end.

**Test classes should be named directly after the class they are testing, with `Test` at the end.**

Example:

```text
PowerLevelService.java
PowerLevelServiceTest.java
```
**The test source package structure should match the main source package structure.**

Example:
```text
src/main/java/org/tavall/permissions/power/PowerLevelService.java
src/test/java/org/tavall/permissions/power/PowerLevelServiceTest.java
```

#### Example Bad Test
```java
@Test
public void testCanPunish() {
IPowerLevelService powerLevelService = Mockito.mock(IPowerLevelService.class);

    Player staff = Mockito.mock(Player.class);
    Player target = Mockito.mock(Player.class);

    Mockito.when(powerLevelService.canPunish(staff, target)).thenReturn(true);

    boolean canPunish = powerLevelService.canPunish(staff, target);

    assertTrue(canPunish);
}
```
_Why?_

This does not test the power level system.

It tests that a mocked method returns the value we told it to return. Stunning. We successfully asked a mirror if we look good.

#### Example Good Test

```java
public final class PowerLevelServiceTest {

    private final UUID staffUUID = UUID.fromString("00000000-0000-0000-0000-000000000001");
    private final UUID targetUUID = UUID.fromString("00000000-0000-0000-0000-000000000002");

    private final StaffPowerProfile staffProfile = new StaffPowerProfile(
        staffUUID,
        RankKey.MOD,
        300
    );

    private final StaffPowerProfile targetProfile = new StaffPowerProfile(
        targetUUID,
        RankKey.ADMIN,
        700
    );

    private final IPowerLevelService powerLevelService = new PowerLevelService();

    @Test
    public void modCannotPunishAdmin() {
        boolean canPunish = powerLevelService.canPunish(
            staffProfile,
            targetProfile
        );

        assertFalse(canPunish);
    }
}
```

_Why?_

The test class is named after the class being tested.

The setup objects live at the class level because they are part of the repeated test context.

The test uses real profiles, real rank keys, real power values, and the real power-level service.

No fake answer. No mock theater. Just behavior.

#### Example Good Full Delegate Test

```java
public final class BanCommandTest {

    private final UUID staffUUID = UUID.fromString("00000000-0000-0000-0000-000000000001");
    private final UUID targetUUID = UUID.fromString("00000000-0000-0000-0000-000000000002");

    private final StaffPowerProfile staffProfile = new StaffPowerProfile(
        staffUUID,
        RankKey.MOD,
        300
    );

    private final StaffPowerProfile targetProfile = new StaffPowerProfile(
        targetUUID,
        RankKey.ADMIN,
        700
    );

    private final FakePermissionRepository permissionRepository = new FakePermissionRepository();
    private final IPermissionService permissionService = new PermissionService(permissionRepository);
    private final IPowerLevelService powerLevelService = new PowerLevelService();
    private final IPunishmentService punishmentService = new FakePunishmentService();

    private final BanCommand banCommand = new BanCommand(
        permissionService,
        powerLevelService,
        punishmentService
    );

    @Test
    public void rejectsTargetWithHigherPower() {
        PermissionNode permissionNode = PermissionNode.PUNISHMENT_BAN;
        permissionRepository.grant(staffUUID, permissionNode);

        String reason = "Testing punishment power checks.";

        BanCommandRequest request = new BanCommandRequest(
            staffProfile,
            targetProfile,
            reason
        );

        CommandResult result = banCommand.execute(request);

        assertFalse(result.isSuccess());
        assertEquals(CommandFailureReason.TARGET_POWER_TOO_HIGH, result.getFailureReason());
    }
}
```
_Why?_

This delegates through the real command flow.

The test uses real permission logic, real power-level logic, and realistic request data. Only the outside boundary is fake.

The setup is readable, class-level, and reusable. The test method only contains the behavior being tested, which is the whole point before someone invents BanCommandIntegrationUnitMockDelegateTestV2Final.

#### Best Example Usage of Mocking

**Delegate testing can simulate complete plugin lifecycles from bootstrap through shutdown while still keeping platform boundaries replaceable.**

The linked class demonstrates how to simulate a complete plugin lifecycle while mocking only true platform boundaries.

[See class FullPluginSimulationTest.java in public Minecraft-CTF plugin by TJ](https://github.com/tjXJNOOBIE/Minecraft-CTF/blob/main/ctf-paper/src/test/java/dev/tjxjnoobie/ctf/game/FullPluginSimulationTest.java)

## Git Commits

### Commit Message Rules

Every commit must use a structured message with a typed subject and body.

Allowed types only:

```text
Build:
Added:
Changed:
Removed:
Fixed:
Clean:
Test:
Docs:
License:
```

Required format:

```text
<Type>: <specific action>

Reason:
- Why this commit exists.

Changes:
- What changed.

Validation:
- What was checked, or `Not run: <reason>`.
```

Rules:

* Always include the colon after the type.
* Wrap file paths, class names, commands, and literal references in backticks.
* Capitalize the first word after the commit type so the subject reads like a sentence.
* No vague subjects or reasons like `update`, `cleanup`, `fix stuff`, or `sync`.
* One commit should represent one real system boundary.
* Split the commit if it touches unrelated files, systems, or reasons.
* Do not claim validation that was not actually run.

Multiple commit types are allowed in one commit message when the changes all belong to the same logical boundary.

Use multiple typed subject lines at the top of the commit message, one per meaningful change type.

Example:

```text
Added: Implement dependency bundle access
Test: Cover dependency bundle hydration
Docs: Document bundle usage

Reason:
- Introduce dependency bundle access as one coherent feature boundary.
- Keep the implementation, matching tests, and direct usage documentation together because they explain one completed system slice.

Changes:
- Added dependency bundle access contracts.
- Added bundle hydration tests.
- Added documentation for bundle-based dependency access.

Validation:
- Ran bundle access tests.
- Confirmed the staged files only belong to dependency bundle access.
```
### Multi-Type Commits

Use multiple typed subject lines only when all lines describe the same coherent commit boundary.

Do not combine unrelated work just because the files were edited at the same time.

Good combined commit:

```text
Added: Implement dependency access grant descriptors
Test: Cover dependency access grant descriptors
Docs: Document descriptor behavior
```

Bad combined commit:

```text
Added: Implement dependency loader
Docs: Update README badges
Clean: Rename unrelated test package
```

Splitting rule:

* If the `Reason` section can explain all subject lines as one system boundary, the combined commit is allowed.
* If each subject line needs its own unrelated reason, split it into separate commits.
* If the combined commit touches unrelated packages or behavior, split it.
* If docs/tests directly explain or prove the same feature added in the commit, they may stay with it.

### Git Branches

The authoritative branch, pull-request, review, and production-promotion rules live in [GIT_WORKFLOW.md](../GIT_WORKFLOW.md). This section keeps the architectural expectations that affect code organization and commit boundaries.

```text
working/* -> staging/* -> main
```

* Working branches contain one coherent feature, fix, refactor, documentation change, or investigation outcome.
* Staging branches collect one reviewable integration or release scope.
* `main` is production and changes through accountable GitHub review.
* Architecture migrations remain separate from unrelated feature work.
* Code, tests, DI bindings, imports, and documentation move together when a contract changes.
