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
- `.opencode/scripts/run_lint_sweep.bat` — Windows Task Scheduler wrapper. OpenCode-only — Claude Code Routines don't need a local script at all, the schedule lives on Anthropic's servers.
- `/.github/workflows/opencode-daily-lint-sweep.yml` — the GitHub Actions workflow (repo root). This is OpenCode's equivalent of a Claude Code Routine: a scheduled cloud run, no machine of yours needs to be on.

## Before you run it

`src/lint_check.py` always scans its own folder — the folder it lives in, `loop-engineering/08-your-own-daily-loop/` — no matter where you invoke it from. That matters because this loop runs two different ways: locally (you `cd` into the project folder first) and from GitHub Actions (which checks out the whole repo and runs everything from the repo root, without `cd`-ing anywhere). Same reason the skill finds the repo root with `git rev-parse --show-toplevel` instead of a relative `../../` path — it has to work from both places.

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

## Heartbeat: GitHub Actions (the real unattended path — do this one)

This is OpenCode's answer to a Claude Code Routine: no machine of yours has to stay on. The workflow lives at the repo root, `.github/workflows/opencode-daily-lint-sweep.yml`, fires daily at 9am UTC on `schedule`, and also has `workflow_dispatch` so you can fire it manually from the Actions tab to test — the GitHub Actions version of a one-off run.

Add a `GEMINI_API_KEY` repository secret, then either wait for 9am UTC or trigger it by hand: **Actions tab → opencode-daily-lint-sweep → Run workflow.** `gh` is preinstalled and pre-authenticated on GitHub-hosted runners via `GITHUB_TOKEN`, so `gh pr create` in the skill fires reliably here — this is the one environment where the connector step never falls back to "just leave a branch."

## Heartbeat: your own machine (alternative — laptop must stay on)

**macOS/Linux — cron**

```
0 9 * * * cd /path/to/agentfactory-practice-projects/loop-engineering/08-your-own-daily-loop && opencode run "run the daily-lint-sweep skill" >> ~/lint-sweep.log 2>&1
```

**Windows — Task Scheduler**

```cmd
schtasks /create /tn "DailyLintSweep" /tr "C:\path\to\agentfactory-practice-projects\loop-engineering\08-your-own-daily-loop\.opencode\scripts\run_lint_sweep.bat" /sc daily /st 09:00
```

To test without waiting a full day:

```cmd
schtasks /create /tn "DailyLintSweepTest" /tr "C:\path\to\...\.opencode\scripts\run_lint_sweep.bat" /sc minute /mo 5
```

Check `lint-sweep.log` and `progress.md` for new entries every 5 minutes. Stop it once confirmed:

```cmd
schtasks /delete /tn "DailyLintSweepTest" /f
```

(swap `/tn` to `DailyLintSweep` to delete the daily one instead)

## The connector step, and why it has a fallback

On GitHub Actions, `gh` is always available and authenticated — the skill's `gh pr create` step fires every time. Running locally, it depends on whether you've set up `gh` yourself; if not, the skill never merges to `main` on its own either way — it just leaves the fix on a `claude/lint-*` branch and notes it as "ready to merge" in `progress.md`. That's the human gate from Part 5: safe work goes to a branch a person reviews, never straight to `main`.

## Budget guards (Concept 13, made concrete)

- **Item cap:** never more than 3 files touched in one run.
- **Scope cap:** never edit anything `src/lint_check.py` didn't flag — no drive-by refactors.
- **Cheap maker:** the maker runs on `gemini-3.5-flash-lite`, not the same model doing the reviewing.
- **Merge cap:** the loop itself never merges to `main` — only a human does, so a bad week of runs can't compound unattended.

<!-- schtasks /create /tn "DailyLintSweepTest" /tr "D:\my-projects\agentfactory-practice-projects\loop-engineering\08-your-own-daily-loop\.opencode\scripts\run_lint_sweep.bat" /sc minute /mo 5 -->
