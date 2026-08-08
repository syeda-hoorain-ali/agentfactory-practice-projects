---
name: doorbell-review
description: >-
  Reviews the diff of a pull request that touches loop-engineering/06-the-doorbell-loop/ 
  for planted bugs (off-by-one errors, deleted null/None checks) and posts a PASS/FAIL 
  verdict as a real PR review. Use when triggered by a GitHub pull_request event.
---

# Doorbell Review

Nobody typed this prompt to you. A GitHub `pull_request` event fired this run.
Follow these steps exactly.

## 1. Read the diff
Run `gh pr diff <PR_NUMBER>` to see exactly what changed. The PR number is in
the GitHub Actions event payload (`$GITHUB_EVENT_PATH`). Review only the
changed lines — do not re-review the whole repo.

## 2. Check for these two bug patterns first
- **Off-by-one errors** — loop bounds, slice indices, or comparisons that are
  off by one (`<` vs `<=`, `range(n)` vs `range(n + 1)`, a boundary variable
  that no longer includes the edge case it used to).
- **Deleted or weakened null/None checks** — a guard clause
  (`if x is None: return`, a truthiness check, an early return) that existed
  before the diff and is now missing or narrowed.

After that, flag anything else genuinely wrong that you notice — but these
two patterns are the ones this project plants on purpose, so look hard for
them before anything else.

## 3. Decide a verdict
- **FAIL** — a real bug exists, especially an off-by-one or a missing null
  check. Name the exact line, explain why it's wrong, and give one concrete
  input that breaks it.
- **PASS** — only if the diff is genuinely correct.

## 4. Post the review
Post an actual PR review, not a plain comment:

```
# on FAIL
gh pr review <PR_NUMBER> --request-changes --body "<verdict + reasoning>"

# on PASS
gh pr review <PR_NUMBER> --approve --body "<verdict + reasoning>"
```

Start the body with `FAIL:` or `PASS:` on its own first line so the verdict
is scannable without opening the diff.

## 5. Never edit files
This skill only reads and reviews. It never pushes a fix — that would remove
the human's chance to see the bug flagged. If you see the fix, describe it in
the review instead of applying it.
