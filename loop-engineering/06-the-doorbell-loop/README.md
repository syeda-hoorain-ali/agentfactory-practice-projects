# Project 06: The Doorbell Loop

A loop that reacts to a pull request, with no prompt typed.

*Difficulty: medium · Uses: Concept 7 (event-driven), Concept 10 (connectors).*

**Build.** Make your throwaway repo review its own pull requests. On the OpenCode approach, run `opencode github install` and accept the workflow it generates. On the Claude Code approach, create a Routine with a GitHub pull-request trigger (the appendix walks through the filters). Then open a PR that contains one planted bug, such as an off-by-one or a deleted null check, and wait.

**Done when** the PR gets a review you never asked for, and the review flags the planted bug. If the review misses it, tighten the prompt and push again. The push fires the loop once more through the synchronize event, and that re-fire is the event heartbeat working. With Projects 1 to 3, this completes all four heartbeats: in-session, conditional, scheduled, and event-driven.

---

## Files

- `greet.py` — the correct baseline. Two functions, each hiding one of the project's two bug patterns.
- `test_greet.py` — 4 tests, all passing against the correct baseline.
- `.claude/skills/doorbell-review/SKILL.md` — the reviewer's task logic, kept inside this project folder. The workflow prompt is one line that points straight at this file's path, since a GitHub Action `uses:` step always starts from the repo root and can't `cd` into a subfolder first.
- `.opencode/skills/doorbell-review/SKILL.md` — same skill, same folder, for OpenCode.
- Root-level `.github/workflows/06-claude-doorbell.yml` and `.github/workflows/06-opencode-review.yml` — required at repo root; GitHub only reads workflows from there.

Needs a real GitHub remote — check `git remote -v` before starting.

## Set it up

1. Commit `greet.py`, `test_greet.py`, both `.claude`/`.opencode` skill folders (inside this project folder), and whichever workflow file you're testing (at repo root).
2. Add the model secret your workflow needs (`ANTHROPIC_API_KEY` for Claude, `GEMINI_API_KEY` for OpenCode) under **Settings → Secrets and variables → Actions**.
3. Push `main`.

## Run it (confirm the baseline first)

```bash
cd loop-engineering/06-the-doorbell-loop
pip install pytest
python -m pytest -q   # confirm: 4 passed, before planting a bug
```

## Plant the bug and open the PR

```bash
git checkout -b doorbell/planted-bug
```

Pick **one**:

**Off-by-one** — in `greet.py`, change:
```python
    return items[len(items) - 1]
```
to:
```python
    return items[len(items)]
```

Verify it:
```bash
python -m pytest -q   # confirm: 2 failed, 2 passed
```
Crashes with `IndexError` every time. `test_get_last_multiple` and `test_get_last_single` both catch it.

**Deleted null check** — in `greet.py`, delete these 2 lines entirely:
```python
    if user is None:
        return "Hello, stranger!"
```

Verify it:
```bash
python -m pytest -q   # confirm: 3 failed, 1 passed
```
Crashes with `TypeError` the moment `user` is `None`. `test_greet_with_none` catches it.

```bash
git add greet.py
git commit -m "refactor greet for clarity"
git push -u origin doorbell/planted-bug
gh pr create --title "Refactor greet" --body "Small cleanup, no behavior change."
```

Wait about a minute.

## Prove it

Open the PR's **Conversation** tab. You should see a review you never asked for — `Changes requested` starting `FAIL:` naming the exact line and a breaking input, or `Approved` starting `PASS:` if you didn't actually plant a bug.

If it misses the bug, tighten `SKILL.md`'s bug-pattern section, then re-fire with an empty commit:
```bash
git commit --allow-empty -m "nudge the reviewer"
git push
```
That `synchronize` re-fire is the event heartbeat working. With Projects 1–3, this completes all four heartbeats.

## Alternative: Claude Code Routine (per the chapter's literal instructions)

Appendix A3: Routine GitHub filters cover author, title, body, base branch, head branch, labels, draft state, merged state — **no changed-files-path filter**. In this monorepo a Routine fires on every PR, not just this folder's. Workaround: filter on **head branch**, `matches regex` → `doorbell/.*` (remember A3 — regex matches the *whole* field, so `doorbell/.*`, not `doorbell`). Needs the **Claude GitHub App** installed (`/web-setup` alone won't do it). Prompt: `Follow the skill at loop-engineering/06-the-doorbell-loop/.claude/skills/doorbell-review/SKILL.md to review this pull request.`
