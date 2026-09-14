#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
from pathlib import Path


def load_validator():
    validator_path = Path(__file__).with_name("verify_docs.py")
    spec = importlib.util.spec_from_file_location("tavall_docs_verify", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load verify_docs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected={expected!r} actual={actual!r}")


def expect_exit_one(callback, message: str) -> None:
    diagnostics = io.StringIO()
    try:
        with contextlib.redirect_stderr(diagnostics):
            callback()
    except SystemExit as exception:
        assert_equal(exception.code, 1, message)
    else:
        raise AssertionError(f"expected validation failure: {message}")


def test_route_specificity(validator) -> None:
    routes = {
        "architecture-overview": ["architecture", "architecture policy"],
        "architecture-testing": ["architecture test", "canonical architecture test"],
        "git-workflow": ["git workflow"],
    }
    assert_equal(
        validator.resolve_routes("architecture", routes),
        {"architecture-overview"},
        "generic architecture route",
    )
    assert_equal(
        validator.resolve_routes("architecture test", routes),
        {"architecture-testing"},
        "longest overlapping signal must win",
    )
    assert_equal(
        validator.resolve_routes("canonical architecture test", routes),
        {"architecture-testing"},
        "most-specific nested signal must win",
    )
    assert_equal(
        validator.resolve_routes("architecture test and git workflow", routes),
        {"architecture-testing", "git-workflow"},
        "non-overlapping concerns must union",
    )


def test_markdown_link_validation(validator) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        docs = root / "docs"
        docs.mkdir()
        source = docs / "source.md"
        target = docs / "target.md"
        target.write_text("# Target\n", encoding="utf-8")
        source.write_text(
            "# Source\n\n[Target](target.md#section)\n[External](https://example.com/path)\n",
            encoding="utf-8",
        )
        validator.validate_markdown_links(root, [Path("docs/source.md"), Path("docs/target.md")])

        source.write_text("# Source\n\n[Missing](missing.md)\n", encoding="utf-8")
        expect_exit_one(
            lambda: validator.validate_markdown_links(
                root,
                [Path("docs/source.md"), Path("docs/target.md")],
            ),
            "broken local link exit code",
        )


def test_text_integrity(validator) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        docs = root / "docs"
        docs.mkdir()
        healthy = docs / "healthy.md"
        healthy.write_text("# Healthy\n", encoding="utf-8")
        validator.validate_text_integrity(root, [Path("docs/healthy.md")])

        conflicted = docs / "conflicted.md"
        conflicted.write_text("<<<<<<< ours\ntext\n>>>>>>> theirs\n", encoding="utf-8")
        expect_exit_one(
            lambda: validator.validate_text_integrity(root, [Path("docs/conflicted.md")]),
            "conflict marker exit code",
        )


def main() -> int:
    validator = load_validator()
    test_route_specificity(validator)
    test_markdown_link_validation(validator)
    test_text_integrity(validator)
    print("tavall-docs CI validator self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
