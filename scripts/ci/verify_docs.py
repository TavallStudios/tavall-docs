#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ROUTE_ID = re.compile(r"^  - id:\s*([a-z0-9-]+)\s*$")
ROUTE_ITEM = re.compile(r"^      -\s+(.+?)\s*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def tracked_docs(root: Path) -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "docs"], cwd=root
    )
    paths = [Path(item.decode("utf-8")) for item in output.split(b"\0") if item]
    if not paths:
        fail("no tracked documentation exists beneath docs/")
    return paths


def read_utf8(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    if b"\x00" in raw:
        fail(f"NUL byte found in documentation file {path}")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"documentation file is not UTF-8: {path}: {exc}")


def validate_text_integrity(root: Path, docs: list[Path]) -> None:
    for relative in docs:
        path = root / relative
        if not path.is_file():
            fail(f"tracked documentation path is not a file: {relative}")
        text = read_utf8(path)
        if not text.strip():
            fail(f"documentation file is empty: {relative}")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("<<<<<<< ") or stripped.startswith(">>>>>>> "):
                fail(f"merge-conflict marker in {relative}:{line_number}")


def markdown_without_fenced_code(text: str) -> str:
    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = None
        if stripped.startswith("```"):
            marker = "```"
        elif stripped.startswith("~~~"):
            marker = "~~~"
        if marker is not None:
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "\n".join(output)


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(None, 1)[0]
    return target.strip()


def validate_markdown_links(root: Path, docs: list[Path]) -> None:
    failures: list[str] = []
    for relative in docs:
        if relative.suffix.lower() != ".md":
            continue
        path = root / relative
        text = markdown_without_fenced_code(read_utf8(path))
        for match in MARKDOWN_LINK.finditer(text):
            target = normalize_link_target(match.group(1))
            if not target or target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            decoded_path = unquote(parsed.path)
            if not decoded_path:
                continue
            if decoded_path.startswith("/"):
                resolved = (root / decoded_path.lstrip("/")).resolve()
            else:
                resolved = (path.parent / decoded_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                failures.append(f"{relative}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{relative}: missing local link target: {target}")
    if failures:
        fail("broken local Markdown links:\n  " + "\n  ".join(sorted(set(failures))))


def parse_scalar(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return stripped[1:-1]
    return stripped


def parse_routing(path: Path) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, str]]:
    text = read_utf8(path)
    routes: dict[str, list[str]] = {}
    documents: dict[str, list[str]] = {}
    matching: dict[str, str] = {}
    current_route: str | None = None
    current_section: str | None = None
    in_routes = False
    in_matching = False

    for line in text.splitlines():
        if line == "matching:":
            in_matching = True
            in_routes = False
            continue
        if line == "resolution:":
            in_matching = False
            continue
        if line == "routes:":
            in_routes = True
            in_matching = False
            current_route = None
            current_section = None
            continue
        if line == "rules:":
            in_routes = False
            current_route = None
            current_section = None
            continue

        if in_matching:
            match = re.match(r"^  ([a-z0-9_]+):\s*(.+?)\s*$", line)
            if match:
                matching[match.group(1)] = parse_scalar(match.group(2))
            continue

        if not in_routes:
            continue

        route_match = ROUTE_ID.match(line)
        if route_match:
            current_route = route_match.group(1)
            if current_route in routes:
                fail(f"duplicate routing id: {current_route}")
            routes[current_route] = []
            documents[current_route] = []
            current_section = None
            continue

        if current_route is None:
            continue
        if line == "    signals:":
            current_section = "signals"
            continue
        if line == "    documents:":
            current_section = "documents"
            continue

        item_match = ROUTE_ITEM.match(line)
        if item_match and current_section:
            value = parse_scalar(item_match.group(1))
            if current_section == "signals":
                routes[current_route].append(value)
            else:
                documents[current_route].append(value)

    if not routes:
        fail("DOCUMENT_ROUTING.yml defines no routes")
    return routes, documents, matching


def signal_pattern(signal: str) -> re.Pattern[str]:
    escaped = re.escape(signal).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![\w-]){escaped}(?![\w-])", re.IGNORECASE)


def resolve_routes(text: str, routes: dict[str, list[str]]) -> set[str]:
    matches: list[tuple[int, int, str, str]] = []
    for route_id, signals in routes.items():
        for signal in signals:
            for match in signal_pattern(signal).finditer(text):
                matches.append((match.start(), match.end(), route_id, signal))

    selected: set[str] = set()
    for start, end, route_id, signal in matches:
        contained_by_longer = False
        for other_start, other_end, _other_route, _other_signal in matches:
            if other_start <= start and other_end >= end and (other_end - other_start) > (end - start):
                contained_by_longer = True
                break
        if not contained_by_longer:
            selected.add(route_id)
    return selected


def validate_routing(root: Path) -> None:
    path = root / "docs/quality/DOCUMENT_ROUTING.yml"
    if not path.exists():
        return

    routes, documents, matching = parse_routing(path)
    required_matching = {
        "mode": "exact_whole_term_or_phrase",
        "fuzzy_matching": "false",
        "recursive_fallback": "false",
        "overlapping_signal_precedence": "longest_declared_signal_span",
        "equal_specificity_routes": "union",
    }
    for key, expected in required_matching.items():
        actual = matching.get(key)
        if actual != expected:
            fail(f"DOCUMENT_ROUTING.yml matching.{key} must be {expected!r}; actual={actual!r}")

    for route_id, signals in routes.items():
        if not signals:
            fail(f"routing id has no signals: {route_id}")
        if len(signals) != len(set(signal.casefold() for signal in signals)):
            fail(f"routing id contains duplicate signals: {route_id}")
        if not documents[route_id]:
            fail(f"routing id has no documents: {route_id}")
        for document in documents[route_id]:
            if not document.startswith("docs/quality/"):
                fail(f"routing document must stay beneath docs/quality: {route_id}: {document}")
            if not (root / document).is_file():
                fail(f"routing document does not exist: {route_id}: {document}")

    expectations = {
        "architecture": {"architecture-overview"},
        "architecture test": {"architecture-testing"},
        "canonical architecture test": {"architecture-testing"},
        "dependency injection": {"dependency-injection-and-composition"},
        "architecture test and git workflow": {"architecture-testing", "git-workflow"},
    }
    for query, expected in expectations.items():
        actual = resolve_routes(query, routes)
        if actual != expected:
            fail(f"routing resolution mismatch for {query!r}: expected={sorted(expected)} actual={sorted(actual)}")


def write_evidence(mode: str, docs_count: int) -> None:
    raw_directory = os.environ.get("TAVALL_CI_EVIDENCE_DIRECTORY")
    if not raw_directory:
        return
    directory = Path(raw_directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "docs-validation.txt").write_text(
        f"mode={mode}\ntrackedDocs={docs_count}\nresult=PASS\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("build", "integration"), required=True)
    args = parser.parse_args()

    root = repository_root()
    docs = tracked_docs(root)
    validate_text_integrity(root, docs)
    if args.mode == "integration":
        validate_markdown_links(root, docs)
        validate_routing(root)
    write_evidence(args.mode, len(docs))
    print(f"tavall-docs validation passed: mode={args.mode} trackedDocs={len(docs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
