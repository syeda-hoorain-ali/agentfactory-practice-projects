---
name: fix-loop
description: >-
  Finds a failing test, drafts the smallest fix in an isolated worktree,
  sends the diff to the reviewer subagent, and opens a PR only when the
  reviewer replies PASS. Scoped to loop-engineering/04-a-fix-loop-with-a-real-checker/
  inside this monorepo. Use whenever asked to "run the fix-loop skill."
---

# Fix loop

This project lives inside a larger repo (agentfactory-practice-projects),
at `loop-engineering/04-a-fix-loop-with-a-real-checker/`. Every step below
must stay scoped to that folder — never touch other projects in this repo.

## 1. Reproduce
- Confirm you are in `loop-engineering/04-a-fix-loop-with-a-real-checker/`
  (check with `pwd`; `cd` there first if not).
- Run `python -m pytest -q` from inside this folder.
- Read the failing test and its traceback. Identify the exact bug — not
  just the symptom.

## 2. Isolate
- Find the repo root: `git rev-parse --show-toplevel`.
- Create the worktree **inside the repo**, under `.worktrees/`, so it
  never leaks out into the parent folder that holds other repos:
  `git worktree add <repo-root>/.worktrees/04-fix-loop-wt -b fix/<short-slug>`
  (Run this from anywhere inside the repo — it doesn't need to be from
  this project's folder. `.worktrees/` is gitignored at the repo root, so
  this never gets committed.)
- A worktree checks out the **entire repo**, not just this project. Your
  real working folder is:
  `<repo-root>/.worktrees/04-fix-loop-wt/loop-engineering/04-a-fix-loop-with-a-real-checker/`
- `cd` into that exact path and do all editing there. Never edit the
  original checkout, and never touch any other project folder inside the
  worktree either.
- The `04-` prefix on the worktree name matters: other numbered projects
  (`01-`, `02-`, ...) will create their own worktrees under the same
  `.worktrees/` folder, and each needs a name that won't collide with the
  others.

## 3. Fix
- Inside the worktree's copy of this project folder, make the smallest
  possible change that fixes the bug.
- Do not touch unrelated code, formatting, comments, other tests, or any
  other project in the repo.

## 4. Check
- Run `pytest -q` again inside the worktree's
  `loop-engineering/04-a-fix-loop-with-a-real-checker/` folder. All tests
  must pass.
- From the worktree root, run:
  `git diff main -- loop-engineering/04-a-fix-loop-with-a-real-checker`
  This scopes the diff to only this project, even inside a monorepo.
- Invoke the `@reviewer` subagent and give it that diff. Wait for its
  verdict. Do not decide "done" yourself.

## 5. Decide
- **PASS:** commit the change (from the worktree root, so the commit stays
  scoped to this project's files), then:
  - if a GitHub remote exists, push the branch and run `gh pr create --fill`
  - if there is no remote, report: "Ready to merge: branch fix/<short-slug>"
    and show the diff
- **FAIL:** do not commit, do not open a PR. Report the reviewer's exact
  reasons and stop.

## Rules
- Never edit files outside `loop-engineering/04-a-fix-loop-with-a-real-checker/`.
- Never edit files outside the worktree once one exists.
- Never commit directly to main.
- Never open a PR without a PASS verdict from the reviewer subagent.
- If pytest shows more than one failing test, fix only the one matching the
  bug you were asked about (or the first one, if none was specified), and
  report the rest instead of fixing everything at once.
