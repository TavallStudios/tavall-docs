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
