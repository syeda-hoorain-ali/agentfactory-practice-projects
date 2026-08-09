#!/usr/bin/env python3
"""Deterministic gather step: lists commits from the last 24 hours."""
import subprocess
import sys
from datetime import datetime

def get_recent_commits():
    result = subprocess.run(
        ["git", "log", "--since=24 hours ago", "--pretty=format:%h %ad %s", "--date=short"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("ERROR: not a git repo, or git log failed.", file=sys.stderr)
        sys.exit(1)
    return [line for line in result.stdout.splitlines() if line.strip()]

def main():
    commits = get_recent_commits()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"## Commits — {today}\n")
    if not commits:
        print("No commits in the last 24 hours.")
    else:
        for line in commits:
            print(f"- {line}")

if __name__ == "__main__":
    main()
