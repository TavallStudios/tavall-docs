# Tavall Docs staging

This branch is the integration root for Phase 6 incremental-verification artifact documentation.

- Parent: `main` at `d670ee5ec1066a00e1b3780e58cf77ba70087c1a`.
- Child merge target: `staging/increlease-docs-20261115`.
- PR Type: `STAGING`; PR State: `ACTIVE` (successor root PR #129).
- QA Task: `orchestrator/20261105/increlease-20261115`.
- Issue: none; this lane is tracked by its orchestrator QA task.
- Work Graph Node: `orchestrator/20261105/increlease-20261115`.
- Active descendants: Docs PR #130 updates VERSIONING.md and CI_CD.md.
- Root validation: not run; run composed `all` after the focused documentation child is integrated.
- Scope: document local immutable package release indexing and Maven file-repository evidence without introducing a second build system or GitHub dependency.
- Promotion to `main` requires exact-head `REQUIRED_ALL` PASS and valid task metadata. No review wait is authorized or required.
