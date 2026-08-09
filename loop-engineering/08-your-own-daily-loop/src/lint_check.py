#!/usr/bin/env python3
"""Deterministic checker for the daily-lint-sweep loop.

Scans Python files for three mechanical issues:
  - functions with no docstring
  - leftover print() debug statements
  - lines longer than 100 characters

Pure Python, no dependencies, works the same on Windows/macOS/Linux.

Always scans THIS SCRIPT'S OWN FOLDER, never the caller's current directory.
That matters because this loop runs two ways: locally (you cd into the
project folder first) and from GitHub Actions (which checks out the whole
repo and runs from the repo root, without cd-ing anywhere). Pinning the scan
to the script's own location means both callers scan the same files, and a
repo with many practice projects never gets cross-scanned by accident.

Usage:
    python3 src/lint_check.py                 # scan this project's folder only
    python3 src/lint_check.py --file app.py   # scan a single file (used by the reviewer)
"""
import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SKIP = {"lint_check.py", "__pycache__"}
MAX_LINE = 100


def find_py_files(root=None):
    root = root or PROJECT_ROOT
    for path in sorted(Path(root).rglob("*.py")):
        if any(part in SKIP for part in path.parts):
            continue
        if ".worktrees" in path.parts:
            continue
        yield path


def check_file(path):
    issues = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > MAX_LINE:
            issues.append(f"{path}:{i}: line too long ({len(line)} > {MAX_LINE} chars)")
        stripped = line.strip()
        if stripped.startswith("print(") or stripped.startswith("print ("):
            issues.append(f"{path}:{i}: leftover print() statement")

    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as e:
        issues.append(f"{path}: syntax error, cannot parse ({e})")
        return issues

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                issues.append(f"{path}:{node.lineno}: function '{node.name}' has no docstring")

    return issues


def main():
    target = None
    if len(sys.argv) == 3 and sys.argv[1] == "--file":
        target = Path(sys.argv[2])
        if not target.exists():
            # caller passed a bare filename ("app.py") from a different cwd
            # (e.g. the repo root) — resolve it against this project's folder
            target = PROJECT_ROOT / target.name

    files = [target] if target else list(find_py_files())
    all_issues = []
    for f in files:
        all_issues.extend(check_file(f))

    if not all_issues:
        print("lint_check: clean, 0 issues")
        return 0

    for issue in all_issues:
        print(issue)
    print(f"lint_check: {len(all_issues)} issue(s) found")
    return 1


if __name__ == "__main__":
    sys.exit(main())
