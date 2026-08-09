# Project 08: Your Own Daily Loop

The full six-part loop on a real chore, run unattended for a week — the capstone.

*Difficulty: capstone · Uses: all six parts (heartbeat, worktree, skill, maker–checker, connector, spine).*

**Build.** Pick one real, boring, recurring chore in a project you actually work on — a dependency audit, a docs-freshness check, a changelog draft, a lint sweep. Build the full loop: heartbeat, worktree, skill, maker–checker, connector, and the spine. Add budget guards. Let it run.

**Done when** it has run unattended for a week and you trust what it ships *because you read it* — not because you stopped reading. Then answer Concept 15 honestly: did your understanding of the project keep up with what the loop changed? If not, slow the loop down until it does.

---

## The chore: a daily lint sweep

Find Python files with mechanical style issues (missing docstrings, leftover `print()` debug statements, lines over 100 chars), fix up to 3 files a run in an isolated worktree, have a separate reviewer grade each fix, and open a PR — or leave a reviewed branch — only on PASS.

## Files

- `src/lint_check.py` — the deterministic checker. Pure Python, no dependencies. Also doubles as the reviewer's proof step (`--file` checks one file).
- `src/app.py`, `src/utils.py` — sample source files with planted lint issues, so the first run has real work to do.
- `progress.md` — the spine. Starts empty; the skill reads it first and writes to it last.
- `.claude/skills/daily-lint-sweep/SKILL.md` — all six parts wired together: budget guard (max 3 files/run), worktree, maker–checker, connector (PR or branch note), spine.
- `.claude/agents/reviewer.md` — the checker subagent (Claude Code).
- `.opencode/skills/daily-lint-sweep/SKILL.md` — the same skill, unchanged, for OpenCode.
- `.opencode/agents/reviewer.md` — the checker subagent (OpenCode).
- `run_lint_sweep.bat` — Windows Task Scheduler wrapper.

## Before you run it

The skill creates git worktrees at `../../.worktrees/` (the repo root shared by every project), so run everything from inside `loop-engineering/08-your-own-daily-loop/` in a checkout of the full `agentfactory-practice-projects` repo.

Confirm the checker works and finds the planted issues before touching a loop:

```bash
python3 src/lint_check.py
```

You should see 4 issues across `src/app.py` and `src/utils.py`.

## Run it

In a Claude Code session in this folder:

```
Run the daily-lint-sweep skill
```

Run it once, read `progress.md`, then run it again — the second run should skip whatever was already handled today and pick up any remaining flagged files.

To turn it into the actual scheduled loop the project asks for:

```
/schedule every day at 9am, run the daily-lint-sweep skill
```

## OpenCode equivalent

```bash
opencode run "Run the daily-lint-sweep skill"
```

**macOS/Linux — cron**

```
0 9 * * * cd /path/to/agentfactory-practice-projects/loop-engineering/08-your-own-daily-loop && opencode run "run the daily-lint-sweep skill" >> ~/lint-sweep.log 2>&1
```

**Windows — Task Scheduler**

```cmd
schtasks /create /tn "DailyLintSweep" /tr "C:\path\to\agentfactory-practice-projects\loop-engineering\08-your-own-daily-loop\run_lint_sweep.bat" /sc daily /st 09:00
```

To test without waiting a full day:

```cmd
schtasks /create /tn "DailyLintSweepTest" /tr "C:\path\to\...\run_lint_sweep.bat" /sc minute /mo 5
```

Check `lint-sweep.log` and `progress.md` for new entries every 5 minutes. Stop it once confirmed:

```cmd
schtasks /delete /tn "DailyLintSweepTest" /f
```

(swap `/tn` to `DailyLintSweep` to delete the daily one instead)

## The connector step, and why it has a fallback

`gh pr create` only fires if this repo has a GitHub remote and an authenticated `gh` CLI. If it doesn't, the skill never merges to `main` on its own either way — it just leaves the fix on a `claude/lint-*` branch and notes it as "ready to merge" in `progress.md`. That's the human gate from Part 5: safe work goes to a branch a person reviews, never straight to `main`.

## Budget guards (Concept 13, made concrete)

- **Item cap:** never more than 3 files touched in one run.
- **Scope cap:** never edit anything `lint_check.py` didn't flag — no drive-by refactors.
- **Cheap checker:** the reviewer runs on `claude-haiku-4-5-20251001`, not the same model doing the fixing.
- **Merge cap:** the loop itself never merges to `main` — only a human does, so a bad week of runs can't compound unattended.
