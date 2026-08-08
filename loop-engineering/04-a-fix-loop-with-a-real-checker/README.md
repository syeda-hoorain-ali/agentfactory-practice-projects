# Project 04: A Fix Loop With a Real Checker

An implementer drafts, a separate reviewer grades, and only PASS opens a PR.

*Difficulty: medium–hard · Uses: Concept 8 (worktree), Concept 9 (skill), Concept 11 (maker–checker).*

**Build.** A smaller version of the Part 5 loop. Write a short skill with your fix steps, and a reviewer agent that replies `PASS` or `FAIL`. Take one real bug, have the implementer draft a fix in its own checkout (worktree or branch), and let the reviewer grade it. Open a PR only on `PASS`.

**Done when** two things are both true: a good fix gets a `PASS` and a PR, *and* a deliberately bad fix you plant gets a `FAIL` with reasons. If the reviewer passes the bad fix, your checker is too soft — tighten it. A checker that approves everything is no checker.

---

## Files

- `calculator.py` — the buggy module. `divide()` uses `//` (integer division) instead of `/`, so `divide(7, 2)` returns `3` instead of `3.5`. That's the one real bug the implementer has to find and fix.
- `test_calculator.py` — 4 tests. Exactly one fails because of the bug (`1 failed, 3 passed`), so the loop has something concrete to reproduce.
- `.claude/skills/fix-loop/SKILL.md` — all the task logic (reproduce → isolate in a worktree → fix → check → decide), so the prompt stays one line.
- `.claude/agents/reviewer.md` — the checker. Read-only, its own model, replies `PASS` or `FAIL` with reasons. Never edits files.
- `.opencode/skills/fix-loop/SKILL.md` — the same skill, for OpenCode.
- `.opencode/agents/reviewer.md` — the same checker, for OpenCode.

This project lives inside the `agentfactory-practice-projects` monorepo, so the skill creates its worktree at `<repo-root>/.worktrees/04-fix-loop-wt/` (gitignored) rather than as a sibling of the whole repo — otherwise every numbered project would drop a loose worktree folder into the same parent directory.

## Run it

```bash
cd loop-engineering/04-a-fix-loop-with-a-real-checker
pip install pytest
python -m pytest -q   # confirm: 1 failed, 3 passed, before touching a loop
```

Then, in a Claude Code session started **from inside this project's folder** (not the repo root — that's what scopes `.claude/skills` and `.claude/agents` to just this project):

```
Run the fix-loop skill.
```

It should create the worktree, change only `return a // b` to `return a / b`, hand the diff to `reviewer`, and on PASS report "Ready to merge: branch fix/..." (or open a real PR if you've added a GitHub remote at the repo root).

## OpenCode equivalent

```bash
cd loop-engineering/04-a-fix-loop-with-a-real-checker
opencode
```
```
Run the fix-loop skill.
```

Same one-liner in both tools — the skill file is what differs, not the prompt.

## Prove it (the actual "done when")

**Good fix → PASS:** the run above. Confirm `python -m pytest -q` shows `4 passed` afterward.

**Bad fix → FAIL:** re-break the bug, but this time have the agent plant a wrong fix, and check the reviewer actually catches it instead of rubber-stamping it:

```
Change divide() so it returns a // b again, and this time when you fix it,
change it to `return a / b + 1` instead of `return a / b`. Then run the
fix-loop skill and tell me what the reviewer says.
```

This should get a `FAIL` — the reviewer's own `pytest` run will still show `test_divide_exact` failing (`divide(10, 2)` returns `6.0`, not `5.0`), and it should say so. A PASS here means the checker isn't checking, and that's the thing to fix before trusting this loop with anything real.
