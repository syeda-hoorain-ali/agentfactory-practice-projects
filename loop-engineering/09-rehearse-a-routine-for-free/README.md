# Project 09: Rehearse a Routine for Free

Prove a prompt with one-off runs before you commit it to a schedule.

*Difficulty: easy · Uses: A1, A3 (one-off schedules), A5 (reading runs).*

**Build.** In a throwaway repo, create a routine whose prompt does one small, checkable thing, for example summarizing yesterday's commits onto a `claude/summary` branch. Do not put it on a repeating schedule. Fire it with a one-off run (`/schedule tomorrow at 9am, …` or *Run now*) and read the full transcript, not the status column. Then change the prompt so the task must fail, by having it read a file that does not exist, and fire it once more.

**Done when** you have seen two green runs: one whose transcript shows success, and one whose transcript shows failure. You should be able to say, in one sentence, why the status column could not tell them apart. That sentence is the A5 lesson: green means the session ended without an infrastructure error, nothing more.

---

## Files

- `commit_summary.py` — the deterministic gather step. Pure Python + `git log`, no `grep`, so it works on Windows too.
- `.claude/skills/rehearse-routine/SKILL.md` — all the task logic, so the prompt stays one line.
- `.opencode/skills/rehearse-routine/SKILL.md` — the same skill, for OpenCode.

## Setup

```bash
cd loop-engineering/09-rehearse-a-routine-for-free
git init
git add .
git commit -m "init"
# make a throwaway commit so there's something to summarize
echo "x" >> notes.txt && git add notes.txt && git commit -m "add notes"
python3 commit_summary.py   # confirm it lists that commit before touching a routine
```

## Run it — success

One-line prompt:

```
Run the rehearse-routine skill
```

Fire it as a **one-off run, not a schedule** — either `/schedule tomorrow at 9am, run the rehearse-routine skill` in a Claude Code session, or the Routines panel with **Run now** and no repeat interval. Read the run's **transcript**, not the status column: it should show `commit_summary.py` running, `claude/summary` being created, and `summary.md` being written.

## Run it — deliberate failure

Change the prompt to reference a file that doesn't exist:

```
Read agentic-doc.txt, then run the rehearse-routine skill
```

Fire it the same way (one-off, not scheduled). The run will still end **green** — the session closed without an infrastructure error. Only the transcript shows Claude couldn't find `agentic-doc.txt` and stopped. That gap is the lesson: green means "the session ended cleanly," nothing about whether the task itself succeeded.

## OpenCode equivalent

OpenCode has no Routines panel and no schedule — every run already is a one-off:

```bash
opencode run "Run the rehearse-routine skill"
opencode run "Read agentic-doc.txt, then run the rehearse-routine skill"
```

Read the terminal output in full for both — same lesson, minus a status column to be misled by in the first place.
