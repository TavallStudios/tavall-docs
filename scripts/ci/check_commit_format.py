#!/usr/bin/env python3
"""Deterministic Tavall commit-subject and pull-request title format validator.

Canonical grammar authority: docs/quality/GIT_WORKFLOW.md section 5.2
("Commit messages and pull-request titles").

Grammar enforced (identical for commit subjects and PR titles):

    Type: Capitalized concise action

Allowed type prefixes (exact canonical list):

    Build, Added, Changed, Removed, Fixed, Refactor, Clean, Test,
    Docs, License, TODO, Misc

Prohibited:

    - lowercase Conventional Commit prefixes (feat:, fix:, chore:, ...)
    - untyped subjects (no allowed Type: prefix)
    - untyped catch-all subjects; unrelated multi-file work must be split
      into separate typed commits (GIT_WORKFLOW.md section 5.1)
    - vague one-word subjects (Update, Changes, Stuff, Fix, Final, WIP)

Exempt (Git/GitHub-generated subjects only):

    - merge subjects ("Merge pull request #N from ...", "Merge branch ...")
    - revert subjects ('Revert "Original typed subject"')

Usage:

    check_commit_format.py --subject "Changed: Something"
    check_commit_format.py --pr-title "Fixed: Reject bad titles"
    check_commit_format.py --git-range origin/main..HEAD
    check_commit_format.py            # reads one subject per stdin line

Exit code 0 when every input conforms (or is exempt); exit code 1 with a
per-line failure report otherwise. Historical commits predating the rule
are not rewritten retroactively; gates apply the validator to new work.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Exact canonical list from docs/quality/GIT_WORKFLOW.md section 5.2.
# scripts/ci/test_commit_format.py asserts this list stays synchronized
# with the document.
ALLOWED_TYPES: tuple[str, ...] = (
    "Build",
    "Added",
    "Changed",
    "Removed",
    "Fixed",
    "Refactor",
    "Clean",
    "Test",
    "Docs",
    "License",
    "TODO",
    "Misc",
)

# Vague subjects explicitly prohibited by GIT_WORKFLOW.md section 5.2.
VAGUE_SUBJECTS = frozenset({"update", "changes", "stuff", "fix", "final", "wip"})

MERGE_SUBJECT = re.compile(r"^Merge ")
REVERT_SUBJECT = re.compile(r'^Revert "')
# Lowercase Conventional Commit style: type, optional scope, optional "!", colon.
CONVENTIONAL_PREFIX = re.compile(r"^[a-z]+(?:\([a-z0-9._/-]+\))?!?: ")
# A subject is either fully untyped, or "Type: description".
TYPED_SUBJECT = re.compile(r"^([A-Za-z]+):\s*(.*)$")


def is_exempt(subject: str) -> bool:
    """Return True for Git/GitHub-generated merge and revert subjects."""
    return bool(MERGE_SUBJECT.match(subject) or REVERT_SUBJECT.match(subject))


def validate_subject(subject: str) -> str | None:
    """Validate one commit subject or PR title.

    Returns None when the subject conforms (or is exempt), otherwise a
    deterministic reason string.
    """
    text = subject.strip()
    if not text:
        return "empty subject"
    if is_exempt(text):
        return None
    if CONVENTIONAL_PREFIX.match(text):
        return "lowercase Conventional Commit prefix is prohibited; use an allowed capitalized Type: prefix"
    match = TYPED_SUBJECT.match(text)
    if match is None:
        return "untyped subject; use one of the allowed Type: prefixes"
    type_word, description = match.group(1), match.group(2)
    if type_word not in ALLOWED_TYPES:
        return f"unknown type prefix {type_word!r}; allowed types are: {', '.join(ALLOWED_TYPES)}"
    if not re.match(r"^[A-Z]", description):
        return "description after the colon must start with a capital letter"
    if description.casefold() in VAGUE_SUBJECTS:
        return "vague subject; describe the result instead"
    return None


def validate_typed_block(subject: str) -> list[str]:
    """Validate a possibly multi-line typed subject block.

    Every non-empty line of a multi-line subject block must itself conform.
    """
    failures: list[str] = []
    lines = [line for line in subject.splitlines() if line.strip()]
    if not lines:
        return ["empty subject"]
    for line in lines:
        reason = validate_subject(line)
        if reason is not None:
            failures.append(f"{line!r}: {reason}")
    return failures


def validate_git_range(root: Path, git_range: str) -> list[str]:
    """Validate every commit subject reachable in <base>..<head>."""
    try:
        output = subprocess.check_output(
            ["git", "log", "--format=%s", git_range],
            cwd=root,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", "replace").strip()
        return [f"cannot enumerate git range {git_range!r}: {detail or exc}"]
    subjects = [line.decode("utf-8") for line in output.splitlines()]
    failures: list[str] = []
    for subject in subjects:
        reason = validate_subject(subject)
        if reason is not None:
            failures.append(f"commit subject {subject!r}: {reason}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--subject", action="append", default=[], help="commit subject to validate (repeatable)")
    parser.add_argument("--pr-title", action="append", default=[], help="pull-request title to validate (repeatable)")
    parser.add_argument("--git-range", help="validate every commit subject in <base>..<head>")
    args = parser.parse_args()

    failures: list[str] = []
    for subject in args.subject:
        failures.extend(validate_typed_block(subject))
    for title in args.pr_title:
        reason = validate_subject(title)
        if reason is not None:
            failures.append(f"PR title {title!r}: {reason}")
    if args.git_range is not None:
        root = Path(__file__).resolve().parents[2]
        failures.extend(validate_git_range(root, args.git_range))
    if not args.subject and not args.pr_title and args.git_range is None:
        for line in sys.stdin.read().splitlines():
            reason = validate_subject(line)
            if reason is not None:
                failures.append(f"{line!r}: {reason}")

    if failures:
        print("commit/PR title format validation FAILED:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("commit/PR title format validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
