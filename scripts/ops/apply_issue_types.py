#!/usr/bin/env python3
"""Read-back-verified one-off native GitHub Issue Type migration.

Default is offline and read-only. --apply requires an authorized gh api
session. This tool does not create issues or change labels, bodies, states,
assignees, or milestones. Native Issue Types, not title prefixes, are authoritative.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ALLOWED_TYPES = frozenset({"TODO", "Bug", "Idea", "Research", "Other"})
ISSUE_URL = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/issues/([0-9]+)$")


def github_api(*args):
    result = subprocess.run(
        ["gh", "api", *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        # Never print command environment, auth tokens or full HTTP headers.
        raise RuntimeError(
            "GitHub API failed or is unauthorized: "
            + (result.stderr.strip().splitlines() or ["No details"])[0][:180]
        )
    return json.loads(result.stdout)


def read_manifest(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2:
        raise ValueError("Unsupported issue-type migration schema")
    seen = set()
    for row in data["entries"]:
        url = row["issue_url"]
        match = ISSUE_URL.fullmatch(url)
        if not match or url in seen:
            raise ValueError("Duplicate or invalid issue URL: " + url)
        seen.add(url)
        proposed = row["proposed_native_type"]
        title = row["proposed_title"]
        if proposed is None:
            if title is not None:
                raise ValueError("Excluded issue cannot have proposed title")
            continue
        if proposed not in ALLOWED_TYPES:
            raise ValueError("Unsupported native issue type: " + proposed)
        expected_prefix = proposed.upper() + ":"
        if not title or not title.startswith(expected_prefix):
            raise ValueError("Title prefix/type mismatch: " + url)
        # The migration includes both untyped and previously typed legacy issues.
        # A non-null old Type is a compare-and-swap precondition, not an error.
        current_type = row.get("current_native_type")
        if current_type is not None and not isinstance(current_type, str):
            raise ValueError("Invalid existing Type value: " + url)
        if row["current_state"] not in ("open", "closed"):
            raise ValueError("Invalid state: " + url)
    return data


def run(path, *, apply, states, limit):
    data = read_manifest(path)
    selected = [item for item in data["entries"]
                if item["current_state"] in states
                and item["proposed_native_type"] is not None]
    print("REVIEWED", len(selected), "of", len(data["entries"]),
          "manifest rows. APPLY" if apply else "manifest rows. OFFLINE DRY RUN")
    summary = {"applied": 0, "already_applied": 0, "skipped_drift": 0, "errors": 0}
    if not apply:
        for item in selected:
            print("PLAN", item["issue_url"], item["proposed_native_type"],
                  repr(item["proposed_title"]))
        return 0

    # Do not run if the authorized gh session is absent or read-only.
    subprocess.run(["gh", "auth", "status"], check=True, capture_output=True, text=True)
    for item in selected:
        if summary["applied"] >= limit:
            break
        match = ISSUE_URL.fullmatch(item["issue_url"])
        endpoint = "repos/{}/{}/issues/{}".format(*match.groups())
        try:
            issue = github_api(endpoint)
            current_type = (issue.get("type") or {}).get("name")
            actual_state = issue.get("state")
            actual_title = issue.get("title")
            expected_type = item["proposed_native_type"]
            expected_title = item["proposed_title"]
            if actual_state != item["current_state"]:
                print("SKIP_STATE_DRIFT", item["issue_url"])
                summary["skipped_drift"] += 1
                continue
            if current_type == expected_type and actual_title == expected_title:
                summary["already_applied"] += 1
                continue
            if (current_type != item.get("current_native_type")
                    or actual_title != item["source_title"]):
                print("SKIP_TYPE_OR_TITLE_DRIFT", item["issue_url"])
                summary["skipped_drift"] += 1
                continue
            github_api(
                "-X", "PATCH", endpoint, "-f", "type=" + expected_type,
                "-f", "title=" + expected_title,
            )
            verified = github_api(endpoint)
            if (verified.get("type") or {}).get("name") != expected_type \
                    or verified.get("title") != expected_title:
                raise RuntimeError("PATCH returned but read-back type/title mismatch")
            summary["applied"] += 1
            print("APPLIED", item["issue_url"], expected_type)
        except (RuntimeError, ValueError) as exc:
            print("ERROR", item["issue_url"], str(exc), file=sys.stderr)
            summary["errors"] += 1
            # Fail closed on API/auth failure; no blind retry after uncertain mutation.
            break
    print("SUMMARY", json.dumps(summary, sort_keys=True))
    return 1 if summary["errors"] or summary["skipped_drift"] else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parents[2] /
                        "docs/progression/GITHUB_ISSUE_TYPE_REVIEW_20261108.json")
    parser.add_argument("--apply", action="store_true",
                        help="Write bounded native Types and titles using authorized gh api")
    parser.add_argument("--state", choices=("open", "closed", "all"), default="open")
    parser.add_argument("--limit", type=int, default=25,
                        help="Maximum successful native type updates per invocation")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 100:
        parser.error("--limit must be between 1 and 100")
    states = {"open", "closed"} if args.state == "all" else {args.state}
    try:
        return run(args.manifest, apply=args.apply, states=states, limit=args.limit)
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print("BLOCKED", str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
