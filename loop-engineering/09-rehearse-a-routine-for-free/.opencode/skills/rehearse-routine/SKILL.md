---
name: rehearse-routine
description: Summarize the last 24 hours of git commits onto a claude/summary branch. Use when asked to "run the rehearse-routine skill".
---

# Rehearse Routine

One small, checkable task: turn yesterday's commits into a summary on their own branch.

## Steps

1. Run `python3 commit_summary.py` and capture its output.
2. Create (or check out, if it already exists) a branch named `claude/summary`.
3. Write the captured output to `summary.md` on that branch, overwriting any previous content. Add a `Generated: <today's date>` line at the top.
4. Commit with the message `docs: summarize commits (<today's date>)`.
5. Switch back to the branch you started on.
6. Report back in one line: how many commits were summarized, and the branch name.

## Notes

- This is a one-off rehearsal, not a scheduled loop — do not create or modify any schedule.
- If `commit_summary.py` exits with an error (e.g. no such file), stop and report the error. Do not invent commit data.
