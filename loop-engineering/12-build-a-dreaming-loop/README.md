# Project 12: Build a Dreaming Loop

A weekly loop that reads your other loops' logs and proposes rule changes as a PR.

*Difficulty: capstone · Uses: Concept 12 (spine and improvement loop), Concept 11 (maker-checker), Concept 6 (schedule), Part 5 (human gate).*

**Build.** You need a loop that has already run for a week and left dated entries in `progress.md` (Project 3 or Project 8 gives you one). Now build a second loop over it. On a weekly schedule, it reads all log entries since the date in its own `dreaming-state.md`, looks for any failure or correction that appears more than once, and drafts the smallest rules-file or skill change that would prevent it, as a PR on a `claude/` branch, never a direct commit. The PR description must cite its evidence: which runs, how often, and why this line stops it. Have it also propose one deletion: a rule no recent run needed. Finish by updating `dreaming-state.md`.

**Done when** three things are true. The PR's proposed change traces to real, cited log entries, not a plausible-sounding guess. A deliberately planted repeated failure in the logs (add one by hand) gets caught and turned into a proposal. And nothing changed in your rules file without you merging it. If the loop proposes changes with no evidence attached, tighten the prompt: an improvement loop that guesses is worse than no improvement loop, because its guesses steer every future run.

---

## Prerequisite
 
This project reads log entries written by Project 3 and Project 8, so it depends on:
 
- `../03-the-morning-brief-with-a-memory/progress.md`
- `../08-your-own-daily-loop/progress.md`
If your Project 8 folder has a different slug, change the two `sources:` lines in `dreaming-state.md` to match — that's the only place the path is hardcoded.
 
## Files
 
- `analyze_logs.py` — the deterministic gather step. Pure Python, no dependencies. Reads `dreaming-state.md` for the last dream date and the source list, scans both `progress.md` files for entries newer than that date, groups any `[tag]`ged failure/correction line and counts repeats, and checks which rules in the root `CLAUDE.md`/`AGENTS.md` went unreferenced in the window. Writes `dreaming-report.json`. This script decides what counts as "repeated" — the agent never eyeballs the raw logs and guesses.
- `dreaming-state.md` — the spine for *this* loop. Tracks `last_dream_date` and the list of source logs, plus an append-only `## Dream Log`.
- `.claude/skills/dreaming-loop/SKILL.md` — all the task logic (steps 1–7: run the script, draft fixes, propose one deletion, branch, commit, open a draft PR, update the spine), so the prompt stays one line.
- `.opencode/skills/dreaming-loop/SKILL.md` — the same skill, for OpenCode.
- `seed_sample_logs.py` — **test-only.** Writes a week of sample entries into both source `progress.md` files, including a failure tagged `[missing-remote]` planted 3 times (the "deliberately planted repeated failure" the Done-when criteria asks for) and one-off noise that should *not* trigger a proposal. Also seeds a root `CLAUDE.md`/`AGENTS.md` with one rule that's genuinely unused in that window, so the deletion path has something to catch. Run this once before your first test; never run it against real data.
- `.opencode/scripts/run_dream.bat` — Windows Task Scheduler wrapper, matching Project 8's convention. `cd`s into the project folder before calling `opencode run`, so Task Scheduler's working directory doesn't matter.
- `/.github/workflows/opencode-dreaming-loop.yml` — the GitHub Actions workflow (repo root, not this folder). This is OpenCode's equivalent of a Claude Code Routine: a scheduled cloud run, `cron: '0 9 * * 1'` (weekly, Monday 9am UTC), plus `workflow_dispatch` so you can trigger a test run by hand from the Actions tab.

## Prerequisites on your machine
 
- `gh` (GitHub CLI), authenticated, with this repo's remote already set — the skill opens the PR with it.
- The two rules `git checkout -b claude/dreaming-...` needs: you're not already mid-rebase or with uncommitted changes on `main` when the skill runs.

## Test it (seeded data, dry run first)
 
From the repo root:
 
```bash
cd loop-engineering/12-build-a-dreaming-loop
python3 seed_sample_logs.py     # only once — plants the test data
python3 analyze_logs.py         # confirm it finds exactly 1 repeated issue, 1 unused rule
cat dreaming-report.json        # sanity-check the evidence before trusting the skill with it
```
 
You should see `repeated issues (>1 occurrence): 1` and `unused-rule candidates: 1`. If you see 0 of either, the seed didn't write correctly — check the two `progress.md` paths.
 
Then, in a Claude Code session **in this folder**:
 
```
run the dreaming-loop skill
```
 
**Done-when checklist to verify yourself:**
 
1. Open the draft PR the skill created. Confirm the "Evidence" section lists the real dates/lines from `progress.md` — not paraphrased guesses.
2. Confirm the proposed deletion matches the rule `seed_sample_logs.py` planted as unused.
3. Confirm `main`'s `CLAUDE.md`/`AGENTS.md` is untouched — the changes only exist on the `claude/dreaming-*` branch until you merge the PR yourself.
To prove the "nothing to dream about" path also works, run it a second time without seeding new data — `repeated_issues` will be empty (everything's now before `last_dream_date`), and the skill should append a "nothing repeated" line to `dreaming-state.md` with no new branch or PR.
 
## Isolating the branch work (optional, matches your worktree convention)
 
The skill's own git operations (checkout, commit, push) don't need a worktree — they just create a new branch. But if you'd rather keep `main`'s working directory untouched while this runs, do the run from a worktree instead of this canonical folder:
 
```bash
git worktree add .worktrees/loop-engineering/12-build-a-dreaming-loop -b dream-work
cd .worktrees/loop-engineering/12-build-a-dreaming-loop/loop-engineering/12-build-a-dreaming-loop
# run the skill from here instead
```
 
The canonical `loop-engineering/12-build-a-dreaming-loop/` folder stays the source of truth for the script and skill files either way.
 
## Turn it into the actual weekly loop (Claude Code)
 
```
/schedule every monday at 9am, run the dreaming-loop skill
```
 
A Claude Code Routine runs on Anthropic's servers — no machine of yours needs to stay on.
 
## OpenCode equivalent
 
```bash
opencode run "run the dreaming-loop skill"
```
 
OpenCode has no built-in scheduler, so something else has to fire that one-liner weekly. Same as Project 8, GitHub Actions is the real unattended path.

This is OpenCode's answer to a Claude Code Routine, and it's the same pattern Project 8 uses: no machine of yours has to stay on. The workflow lives at the repo root, `.github/workflows/opencode-dreaming-loop.yml`, fires weekly at 9am UTC on Monday via `schedule`, and also has `workflow_dispatch` so you can fire it by hand from the Actions tab to test — the GitHub Actions version of a one-off run.
 
Add a `GEMINI_API_KEY` repository secret (Settings → Secrets and variables → Actions), then either wait for Monday 9am UTC or trigger it manually: **Actions tab → opencode-dreaming-loop → Run workflow.**
 
`gh` is preinstalled and pre-authenticated on GitHub-hosted runners via `GITHUB_TOKEN`, so the skill's `gh pr create` step in Step 6 fires reliably here — this is the one environment where the connector step never falls back to "just leave a branch and tell the user the command to run."
 
The workflow prompt points the agent at the same skill file and tells it to run every step (including `analyze_logs.py`) from inside `loop-engineering/12-build-a-dreaming-loop/` — the script resolves its own paths from `__file__`, not the current working directory, so it behaves identically whether it's invoked locally or from a repo-root checkout on a runner.
