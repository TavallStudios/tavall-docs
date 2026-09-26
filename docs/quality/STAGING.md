# Tavall Docs Staging

This file records the persistent repository/release staging boundary for the
canonical documentation repository.

- Branch: `staging/quality`
- Parent: `main`
- Role: repository/release staging
- State: `ACTIVE`
- Promotion: manual through the staging pull request

The staging pull request is the integration root for documentation changes that
must be reviewed as a composed tree. Child pull requests target this branch or
an active dependency branch that reaches it. GitHub pull requests and their
current heads remain authoritative; this file is only a repository-local
topology marker.

## Current composition

The staging branch was refreshed from `main` at `7b620605c9a9eb9f97394309c7a8a429eaeefdf2` after the previous staging root was promoted. The active documentation child is [PR #31](https://github.com/TavallStudios/tavall-docs/pull/31), head `bb4c13d96b2c3743496286a1e95569f530379ebc`, targeting this branch. It updates CI/CD ownership guidance, the Notion page source mirrors, and the rollout evidence record.

PR #31 remains Draft. The documentation validator passes, while its evidence record explicitly leaves the Cloud Executor bootstrap, immutable Agent artifact, DEVELOPMENT validation, and STAGING readiness incomplete. This staging root therefore remains Draft and does not authorize a production promotion.
