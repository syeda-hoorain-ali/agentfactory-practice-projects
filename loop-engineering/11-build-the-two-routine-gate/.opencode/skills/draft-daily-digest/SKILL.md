---
name: draft-daily-digest
description: Gather yesterday's commits into a short digest and push it to a review branch, never main.
---

## Task
1. Compute yesterday's date (UTC).
2. Run `git log --since="yesterday 00:00" --until="today 00:00" --oneline` against main.
3. Write a short digest (3–6 plain-English bullets, one line per commit max) to `DIGEST.md` at repo root.
4. Create branch `claude/digest-<YYYY-MM-DD>` from main, commit `DIGEST.md`, push it. Do not open a PR. Do not merge.
5. Append one line to `progress.md`: `<timestamp> — drafted claude/digest-<date>, N commits, awaiting review`.
6. Print the branch name as the final line of output, exactly: `BRANCH: claude/digest-<date>`.

## Constraints
- Never push to main.
- Never merge any branch.
- Zero commits is still a valid draft — write a one-line digest that says so.
