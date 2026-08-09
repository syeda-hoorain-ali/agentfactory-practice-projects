---
name: publish-digest
description: Merge a single human-approved claude/digest-* branch into main. Only acts on the branch it is explicitly told about.
---

## Task
1. Read the branch name from the trigger's freeform text (the API trigger's `text` field, or whatever the invoking prompt states).
2. Verify the branch exists and matches `claude/digest-*`. If not, stop and append to `progress.md`: `<timestamp> — publish REJECTED, branch <name> not found or not a claude/ branch`. Do nothing else.
3. If valid, merge that branch into main with a merge commit (no squash), push main.
4. Append to `progress.md`: `<timestamp> — PUBLISHED <branch> to main, approved by human review`.

## Constraints
- Act only on the single branch named at trigger time. Never scan for "the latest" claude/ branch — that would remove the human's choice of which draft was approved.
- Never fire itself.
