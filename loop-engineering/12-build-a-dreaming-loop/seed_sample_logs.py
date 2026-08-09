#!/usr/bin/env python3
"""
TEST-ONLY. Plants a week of sample progress.md entries in the Project 3
and Project 8 folders (creating them if missing), including a failure
tagged [missing-remote] repeated 3 times, and seeds a root CLAUDE.md /
AGENTS.md with one rule that this sample data never references, so the
deletion path has something real to catch.

Run this once, before your first `run the dreaming-loop skill`. Never
run it against real project data -- it will duplicate entries if run twice.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

PROJECT_3 = REPO_ROOT / "loop-engineering" / "03-the-morning-brief-with-a-memory" / "progress.md"
PROJECT_8 = REPO_ROOT / "loop-engineering" / "08-your-own-daily-loop" / "progress.md"

PROJECT_3_CONTENT = """# Progress Log

## 2026-07-27
- Scanned repo: found 2 new TODOs, 1 commit in last 24h. Stayed within [morning-brief-scope], only last 24h reported.
- Updated progress.md.

## 2026-07-28
- Nothing new: 0 new TODOs, 0 new commits.

## 2026-07-29
- NEEDS HUMAN [missing-remote]: `git log` failed, no remote configured, skipped commit gather.
- Scanned repo: found 1 new TODO.

## 2026-07-30
- Scanned repo: found 0 new TODOs, 3 new commits, respected [commit-style] when summarizing.

## 2026-07-31
- NEEDS HUMAN [missing-remote]: `git log` failed, no remote configured, skipped commit gather.

## 2026-08-01
- Scanned repo: found 1 new TODO, 1 new commit.

## 2026-08-02
- NEEDS HUMAN [missing-remote]: `git log` failed, no remote configured, skipped commit gather.
- CORRECTION [flaky-network]: retried scan once after a timeout, succeeded on retry.
"""

PROJECT_8_CONTENT = """# Progress Log

## 2026-07-28
- Dependency audit: 0 outdated packages found.

## 2026-07-30
- Dependency audit: 1 outdated package found (lodash), opened claude/deps-2026-07-30.

## 2026-08-01
- Dependency audit: 0 outdated packages found. Respected [commit-style].

## 2026-08-03
- CORRECTION [audit-timeout]: audit command timed out once, retried with longer timeout, succeeded.
"""

RULES_CONTENT = """# Project Rules

## Rules

- [morning-brief-scope] The morning-brief skill only reports TODOs and commits from the last 24 hours.
- [env-vars] Credentials are available as environment variables; do not look for a `.env` file.
- [commit-style] Keep commit messages under 72 characters on the summary line.
"""


def write_if_missing(path: Path, content: str, force: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"Skipped (already exists): {path}")
        return
    path.write_text(content)
    print(f"Wrote: {path}")


def main():
    write_if_missing(PROJECT_3, PROJECT_3_CONTENT, force=True)
    write_if_missing(PROJECT_8, PROJECT_8_CONTENT, force=True)
    write_if_missing(REPO_ROOT / "CLAUDE.md", RULES_CONTENT)
    write_if_missing(REPO_ROOT / "AGENTS.md", RULES_CONTENT)
    print("\nSeed complete. Run analyze_logs.py next to sanity-check detection.")


if __name__ == "__main__":
    main()
