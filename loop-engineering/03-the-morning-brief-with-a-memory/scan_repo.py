#!/usr/bin/env python3
"""
scan_repo.py — the deterministic 'gather' step of the morning-brief loop.

Why Python here: gathering the raw facts (TODOs, commits) should be a
command a human can verify, not something the model guesses at from
memory. This script is the loop's source of truth for "what's out there."
The agent's job is to read this output and decide what's NEW vs progress.md.

Usage:
    python3 scan_repo.py
"""
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone

TODO_PATTERN = re.compile(r"(TODO|FIXME)[:(]")
SCAN_EXTENSIONS = (".py", ".md", ".js", ".ts")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def get_todos():
    """Find TODO/FIXME comments tracked in the repo.

    Pure Python (os.walk + regex) on purpose — no dependency on a
    'grep' binary, which does not exist on Windows by default.
    """
    matches = []
    this_file = os.path.abspath(__file__)
    try:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if not name.endswith(SCAN_EXTENSIONS):
                    continue
                path = os.path.join(root, name)
                if os.path.abspath(path) == this_file:
                    continue  # don't flag scan_repo.py's own TODO/FIXME mentions
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for lineno, line in enumerate(f, start=1):
                            if TODO_PATTERN.search(line):
                                matches.append(f"{path}:{lineno}:{line.strip()}")
                except (IOError, OSError):
                    continue
        return matches
    except Exception as e:
        return [f"(could not scan for TODOs: {e})"]


def get_recent_commits(hours=24):
    """List commits made in the last N hours."""
    try:
        since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        out = subprocess.run(
            ["git", "log", f"--since={since}",
             "--pretty=format:%h %ad %s", "--date=short"],
            capture_output=True, text=True, timeout=10
        )
        return [l for l in out.stdout.splitlines() if l.strip()]
    except Exception as e:
        return [f"(could not read git log: {e})"]


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    todos = get_todos()
    commits = get_recent_commits()

    print(f"=== Repo scan for {today} ===\n")
    print(f"Open TODO/FIXME comments: {len(todos)}")
    for line in todos:
        print(f"  {line}")
    print()
    print(f"Commits in the last 24h: {len(commits)}")
    for line in commits:
        print(f"  {line}")


if __name__ == "__main__":
    main()
