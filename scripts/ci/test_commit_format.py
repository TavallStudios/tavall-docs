#!/usr/bin/env python3
"""Self-tests for scripts/ci/check_commit_format.py (Tavall issue #164)."""
from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKER_PATH = Path(__file__).with_name("check_commit_format.py")
ROOT = Path(__file__).resolve().parents[2]

GOOD_SUBJECTS = [
    f"{type_word}: Some meaningful result"
    for type_word in (
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
]

BAD_CASES = [
    ("feat: add validator", "Conventional Commit"),
    ("fix(ui): correct rendering", "Conventional Commit"),
    ("chore: bump dependencies", "Conventional Commit"),
    ("feat!: breaking change", "Conventional Commit"),
    ("Meta: something", "unknown type prefix"),
    ("Update README", "untyped subject"),
    ("WIP", "untyped subject"),
    ("Changed: stuff", "must start with a capital letter"),
    ("Fixed: update", "must start with a capital letter"),
    ("Changed: Update", "vague subject"),
    ("Fixed: Fix", "vague subject"),
    ("Changed: lowercase after colon", "must start with a capital letter"),
    ("", "empty subject"),
    ("   ", "empty subject"),
]

EXEMPT_SUBJECTS = [
    "Merge pull request #123 from TavallStudios/working/example",
    "Merge branch 'working/example'",
    'Revert "Changed: Some typed subject"',
]


def run_checker(*args: str) -> tuple[int, str]:
    process = subprocess.run(
        [sys.executable, str(CHECKER_PATH), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return process.returncode, (process.stdout + process.stderr)


def load_checker():
    import importlib.util

    spec = importlib.util.spec_from_file_location("tavall_check_commit_format", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load check_commit_format.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected={expected!r} actual={actual!r}")


def test_allowed_types_are_canonical() -> None:
    checker = load_checker()
    document = (ROOT / "docs/quality/GIT_WORKFLOW.md").read_text(encoding="utf-8")
    for type_word in checker.ALLOWED_TYPES:
        assert f"- `{type_word}`" in document, f"allowed type missing from GIT_WORKFLOW.md section 5.2: {type_word}"
    assert checker.ALLOWED_TYPES == (
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
    ), "canonical allowed-type list drifted from GIT_WORKFLOW.md"


def test_good_subjects_pass() -> None:
    checker = load_checker()
    for subject in GOOD_SUBJECTS:
        assert_equal(checker.validate_subject(subject), None, f"good subject must pass: {subject}")
    code, output = run_checker("--subject", GOOD_SUBJECTS[0], "--pr-title", GOOD_SUBJECTS[1])
    assert_equal(code, 0, f"good subject/PR title CLI exit: {output}")


def test_bad_subjects_fail() -> None:
    checker = load_checker()
    for subject, expectation in BAD_CASES:
        reason = checker.validate_subject(subject)
        if reason is None:
            raise AssertionError(f"bad subject must be rejected: {subject!r}")
        assert expectation in reason, f"reason mismatch for {subject!r}: {reason}"


def test_exemptions_pass() -> None:
    checker = load_checker()
    for subject in EXEMPT_SUBJECTS:
        assert checker.is_exempt(subject), f"exemption missing: {subject!r}"
        assert_equal(checker.validate_subject(subject), None, f"exempt subject must pass: {subject}")


def test_pr_title_rejects_conventional_prefix() -> None:
    checker = load_checker()
    assert checker.validate_subject("feat: add feature") is not None
    assert_equal(checker.validate_subject("Added: Add feature"), None, "typed PR title")


def test_multi_line_typed_block() -> None:
    checker = load_checker()
    block = "Changed: Codify format\nDocs: Document routing"
    assert_equal(checker.validate_typed_block(block), [], "mixed typed lines must pass")
    failures = checker.validate_typed_block("Changed: Codify format\nfix: regress")
    assert_equal(len(failures), 1, "one failing line in typed block")


def test_git_range_end_to_end() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary)
        def git(*args: str) -> None:
            subprocess.check_call(["git", *args], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        git("init", "-q", "-b", "main")
        git("config", "user.email", "ci@example.invalid")
        git("config", "user.name", "Tavall CI")
        (repo / "file.txt").write_text("one\n", encoding="utf-8")
        git("add", "file.txt")
        git("commit", "-q", "-m", "Added: Establish baseline")
        git("branch", "base")

        # A conforming range passes, including a merge commit subject.
        (repo / "other.txt").write_text("x\n", encoding="utf-8")
        git("add", "other.txt")
        git("commit", "-q", "-m", "Changed: Add composed work")
        (repo / "file.txt").write_text("three\n", encoding="utf-8")
        git("add", "file.txt")
        git("commit", "-q", "-m", "Merge branch 'base' into main")

        # The module API validates the temporary repository range directly.
        checker = load_checker()
        failures = checker.validate_git_range(repo, "base..main")
        assert_equal(failures, [], "conforming range with merge commit must pass")

        (repo / "file.txt").write_text("four\n", encoding="utf-8")
        git("add", "file.txt")
        git("commit", "-q", "-m", "feat: lowercase regression")
        (repo / "file.txt").write_text("five\n", encoding="utf-8")
        git("add", "file.txt")
        git("commit", "-q", "-m", "untyped regression subject")
        failures = checker.validate_git_range(repo, "base..main")
        assert_equal(len(failures), 2, "range regressions must be caught")
        assert any("untyped" in failure for failure in failures), failures
        assert any("Conventional Commit" in failure for failure in failures), failures


def main() -> int:
    test_allowed_types_are_canonical()
    test_good_subjects_pass()
    test_bad_subjects_fail()
    test_exemptions_pass()
    test_pr_title_rejects_conventional_prefix()
    test_multi_line_typed_block()
    test_git_range_end_to_end()
    print("tavall commit/PR title format validator self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
