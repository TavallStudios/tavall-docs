# Tavall Versioning Architecture

> **Status:** Active
> **Document Type:** Technical / Organization Policy
> **Authority:** Binding for Tavall source, build, artifact, channel, dependency, and release identity
> **Notion Counterpart:** [Tavall Versioning Architecture](https://app.notion.com/p/3e838458ddfd8124a2e9ed5ba5b6ccce)
> **CI/CD Authority:** [CI_CD.md](CI_CD.md)

This document defines Tavall's versioning architecture. Different identities represent different facts; source, build, dependency resolution, artifact, and release state must not be collapsed into one generic version string.

## Identity Layers

### Source Identity

A source identity is an exact repository and exact Git object ID.

```text
repository + exact Git SHA
```

Example:

```text
TavallStudios/tavall-ci@35ff...
```

Branches, pull-request numbers, workspace paths, and labels such as `latest` are selectors or locations, not immutable source identity.

### Build Policy Identity

Build-policy identity identifies the exact Tavall build/CI platform policy used for an execution: toolchain policy, approved Gradle/build-platform rules, and any canonical policy digest required to reproduce the build.

### Resolution Identity

Resolution identity identifies the exact resolved dependency/lock graph. Dependency intent and dependency resolution are not interchangeable; two builds from the same source can differ if their resolved graphs differ.

### Build Identity

A build identity binds:

```text
source identity
+ optional release identity
+ build-policy identity
+ resolution identity
```

Development builds normally have no release identity. The canonical `tavall-ci-versioning` `BuildIdentity` models exactly this distinction.

### Artifact Identity

An artifact identity binds the produced bytes to:

- Artifact name.
- Artifact version string.
- Artifact channel.
- Exact source identity.
- SHA-256 digest.
- Immutable storage reference.

Changing the bytes changes artifact identity even when a human-facing version string is unchanged. Artifact version is useful metadata; the digest and source binding are what make the artifact immutable.

### Release Identity

A release identity is an explicitly approved immutable release identifier. It is absent for ordinary unreleased development candidates.

A Git SHA is not a release. A snapshot version is not automatically a release. A successful CI run is not automatically a release. Promotion creates or selects release state only through the owning release/delivery workflow.

## Version Number Policy

### Internal Development Versions

Tavall internal development artifacts use incremental snapshot numbering:

```text
0.<iteration>.<sub>-SNAPSHOT
```

Example:

```text
0.292.1-SNAPSHOT
```

The numeric value is a human/tool-facing artifact version. It does **not** replace exact source identity, build identity, resolution identity, or artifact digest.

Incremental snapshot numbers may advance as internal work advances. They must not be used to guess another repository's current development head.

### Public and Approved Releases

Public/open-source or explicitly approved releases use the product/module's declared release numbering policy, normally a stable semantic-style version such as `0.1.0`, `1.0.0`, or an explicitly documented compatibility variant.

Release numbering communicates compatibility/product lineage. Release identity additionally binds the approved immutable release state and must remain traceable to source/build/artifact evidence.

## Artifact Channels

Canonical Tavall artifact channels are:

| Channel | Meaning |
| --- | --- |
| `SNAPSHOT` | Internal/unreleased development artifact. |
| `ALPHA` | Explicit early release/testing channel with release intent. |
| `BETA` | Explicit broader pre-release/testing channel. |
| `RELEASE` | Approved stable release artifact. |

The canonical `tavall-ci-versioning` implementation exposes these channels directly.

`SNAPSHOT` is valid as an artifact channel or artifact-version suffix. **It is not valid as a floating cross-repository dependency-selection protocol.**

## Dependency Versioning

First-party Tavall dependency selection is explicit. A dependency resolves through one of these modes:

1. Exact source identity.
2. Approved immutable Tavall artifact/release.
3. Approved public OSS release.

Development composition prefers exact source when validating coordinated changes across repositories/modules. Released consumption prefers approved immutable release/artifact identity.

Forbidden implicit authorities include:

- `latest` development artifact.
- Whichever `SNAPSHOT` was published most recently.
- Maven Local as organizational truth.
- An arbitrary sibling checkout.
- A stale executor workspace.
- GitHub Packages as a silent fallback for private source composition.

Missing version/source information fails closed.

## Cross-Repository Development

Cross-repository development candidates are composed from exact source identities:

```text
repo-a @ exact SHA
repo-b @ exact SHA
repo-c @ exact SHA
        |
        v
 exact candidate
```

Tavall CI may materialize those sources and compose them through Gradle composite builds and dependency substitution. No fake intermediate release is required merely to test coordinated changes.

## Build and Artifact Promotion

The canonical progression is:

```text
exact source
    |
    v
build identity
    |
    v
immutable artifact identity + digest
    |
    v
STAGING validation
    |
    v
explicit release / production authorization
    |
    v
promotion of the same artifact
```

STAGING and PRODUCTION should consume the already validated artifact. Rebuilding from the same source in every environment creates a new build/artifact identity and defeats the point of promotion evidence.

## Version Changes and Evidence

A change to any of the following may require fresh evidence or a new identity:

- Source SHA.
- `.tavallci` definition affecting the build.
- Build-policy identity.
- Resolved dependency graph.
- Produced artifact bytes/digest.
- Artifact channel/version.
- Release identity.
- Delivery configuration used for promotion.

Human-facing version equality does not make two builds equivalent.

## Implementation Mapping

The canonical reusable implementation lives in `TavallStudios/tavall-ci/tavall-ci-versioning`:

- `SourceIdentity`
- `BuildIdentity`
- `BuildPolicyIdentity`
- `ResolutionIdentity`
- `ReleaseIdentity`
- `ArtifactIdentity`
- `ArtifactChannel`
- `ImmutableArtifactReference`

`TavallStudios/tavall-ci/docs/architecture/IDENTITIES.md` remains the implementation-level CI identity reference. This document owns the Tavall-wide policy and numbering/channel semantics above it.

## Final Rules

- Never overload one generic version string with source, build, resolution, artifact, and release meaning.
- Exact source is repository + exact Git SHA.
- Development build identity does not require a fake release identity.
- Internal development artifacts use incremental `0.<iteration>.<sub>-SNAPSHOT` numbering.
- Snapshot numbering never selects another repository's development head.
- Artifact identity binds version/channel to exact source, digest, and immutable storage reference.
- `SNAPSHOT`, `ALPHA`, `BETA`, and `RELEASE` are artifact channels, not substitutes for source identity.
- Cross-repository development resolves exact source.
- Released consumption resolves explicit immutable releases/artifacts.
- STAGING/PRODUCTION promote validated artifact identity instead of rebuilding.

## Delegated Documents

- [CI_CD.md](CI_CD.md) — CI/CD execution, evidence, artifact and promotion policy.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) — branch/PR/release integration workflow.
- `TavallStudios/tavall-ci/docs/architecture/IDENTITIES.md` — CI implementation identity model.
- `TavallStudios/tavall-ci/docs/architecture/SOURCE_AGGREGATION.md` — exact-source development composition.

## Documentation Update State

<details>
<summary>Documentation Update State</summary>

### Current Locations

| Surface | Sync State | Location | Last Updated | Evidence |
| --- | --- | --- | --- | --- |
| GitHub | `1:1` | `TavallStudios/tavall-docs/docs/quality/VERSIONING.md` | 2026-09-27 2:46 PM PDT | Docs sync branch `docs/ci-versioning-notion-sync-20260927`. |
| Notion | `1:1` | `Tavall / Platform & Infrastructure / Tavall Versioning Architecture` | 2026-09-27 2:46 PM PDT | Notion counterpart `3e838458-ddfd-8124-a2e9-ed5ba5b6ccce`. |

### Update History

| Timestamp | Surface | Event | Location | Previous Location | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-27 2:46 PM PDT | GitHub + Notion | `CREATED` | Canonical VERSIONING 1:1 pair | Identity/versioning rules split across CI docs, implementation, and prior design | Current documentation reconciliation | Separated source/build/artifact/release identity and canonized internal snapshot numbering plus artifact channels. |

</details>
