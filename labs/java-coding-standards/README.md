<sub>[← all labs](../../README.md)</sub>

# A Java quality gate in the Maven build

> SonarQube shows you the issues. A gate in the build stops them from being merged.

`Java 21` · `Maven` · `Checkstyle` · `JUnit 5`

**Companion to:**
- [Enforcing Java Coding Standards with SONAR (SonarQube)](https://www.linkedin.com/pulse/enforcing-java-coding-standards-sonar-sonarqube-tony-honesto-ku4lc/)

## What it shows

- Checkstyle runs in Maven's `validate` phase and fails the build on any violation.
- The rules target what SonarQube flags: `==` on strings, empty catch blocks, missing `default`, fall-through, magic numbers, `System.out` in library code.
- JaCoCo enforces 80% line coverage at `verify`, the other half of a quality gate.
- CI proves the gate works both ways: the project passes, and the same project plus one bad file fails.

## Run it

```bash
bash labs/java-coding-standards/ci.sh
# or:
mvn verify
```

Real output (from this lab's CI run):

```text
== quality gate passed: checkstyle clean, tests green, line coverage >= 80%
Best lap formatted: 1:23.456
Representative pace (in/out laps dropped): 83.800 s
Laps to pay back a stop at 0.9 s/lap: 25
== same build with samples/BadExample.java added:
  BadExample.java:3:17: Using the '.*' form of import should be avoided - java.util.*. [AvoidStarImport]
  BadExample.java:7:16: Variable 'count' must be private and have accessor methods. [VisibilityModifier]
  BadExample.java:10:9: 'if' construct must use '{}'s. [NeedBraces]
  BadExample.java:10:18: Literal Strings should be compared using equals(), not '=='. [StringLiteralEquality]
  BadExample.java:12:26: '250' is a magic number. [MagicNumber]
  BadExample.java:13:42: Empty catch block. [EmptyCatchBlock]
  BadExample.java:15:9: switch without "default" clause. [MissingSwitchDefault]
  BadExample.java:17: Use a logger, not System.out/err [RegexpSinglelineJava]
  BadExample.java:18:13: Fall through from previous branch of the switch statement. [FallThrough]
  BadExample.java:22:23: '57' is a magic number. [MagicNumber]
== gate failed as expected
```

## What's in here

| File | Purpose |
|---|---|
| `pom.xml` | Compiler (-Werror), Checkstyle and JaCoCo gates |
| `checkstyle.xml` | The rule set |
| `src/` | Clean code and JUnit 5 tests |
| `samples/BadExample.java` | Breaks the rules on purpose |
| `ci.sh` | Pass, then prove the gate fails |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Checkstyle + JaCoCo | SonarQube / SonarCloud analysis with a quality gate on new code |
| Fails the build | Also blocks the pull request through branch protection |
| One rule file | A shared rule set published as a Maven artifact |
