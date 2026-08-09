---
name: daily-lint-sweep
description: >-
  Runs the daily lint-sweep maintenance loop. Reads the progress file, finds
  Python files with lint issues (missing docstrings, leftover print()
  statements, lines over 100 chars), fixes up to 3 files per run in isolated
  worktrees, has a separate reviewer grade each fix, opens a PR (or leaves a
  reviewed branch) for what passes, and writes anything risky to the progress
  file for a human. Use this for the scheduled daily lint-sweep loop.
---
# Daily lint sweep

You are the daily lint-sweep loop. Work through these steps in order.
Do not skip the progress file. It is your only memory between runs.

## 1. Read your memory first
- Open `progress.md`. Read the "In progress" and "Open / needs a human" sections.
- Do not redo anything already listed under "Done" for today's date.

## 2. Find the work
- Run `python3 lint_check.py` from this folder.
- Group the output by file. Stop once you have at most 3 files — this run's
  budget guard. If more than 3 files have issues, take the first 3 by path
  order and leave the rest for tomorrow's run.

## 3. Work each file
- Create an isolated worktree at the shared repo-root `.worktrees/` folder,
  on a new branch:
  `git worktree add ../../.worktrees/lint-<short-slug> -b claude/lint-<short-slug>`
- In that worktree, fix only what `lint_check.py` flagged for this file: add
  a one-line docstring, remove or comment the `print()`, wrap the long line.
  Do not change behaviour. Do not touch anything the checker did not flag.
- Send the diff to the reviewer subagent. Wait for its verdict before going on.

## 4. Decide from the verdict
- PASS: leave the fix on its `claude/lint-<short-slug>` branch. Do NOT merge
  to `main` yourself — that decision is the human gate. If a GitHub remote is
  configured and the `gh` CLI is available, open a PR:
  `gh pr create --head claude/lint-<short-slug> --fill --body "Automated lint fix. lint_check.py: clean. Reviewed by: reviewer subagent (PASS)."`
  If `gh` is not available, just note the branch name as "ready to merge" in
  progress.md instead. Either way, remove the worktree working directory
  afterward (`git worktree remove ../../.worktrees/lint-<short-slug>`) — the
  branch itself stays.
- FAIL: do not open a PR and do not note it as ready. Add a short entry to
  "Open / needs a human" in progress.md saying what was tried and why it
  failed. Leave the worktree in place for a human to inspect.

## 5. Update your memory last
- Move finished files to "Done" with today's date.
- Save `progress.md`. This is the file tomorrow's run will read.

## Rules (budget guards)
- Never touch more than 3 files in one run.
- Never edit anything `lint_check.py` did not flag — a lint sweep is not a
  refactor.
- Never merge to `main` directly. Only `claude/*` branches, and only a human
  merges them.
- When in doubt, escalate. A flagged file a human checks is always safer than
  a wrong "fix" shipped while no one was watching.
  