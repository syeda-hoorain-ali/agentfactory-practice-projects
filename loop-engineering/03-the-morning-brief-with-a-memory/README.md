# Project 03: The Morning Brief With a Memory

A scheduled loop whose second run clearly builds on its first.

*Difficulty: medium · Uses: Concept 6 (unattended schedule), Concept 12 (the spine).*

**Build.** Make a scheduled loop that runs once, reads a `progress.md`, gathers something simple from the repo (open `TODO` comments, or the last day's commits), writes a short summary, and updates `progress.md` with what it found and the date.

**Done when** you run it twice and the second run clearly builds on the first — it does not repeat what it already recorded. That proves your spine works. If the second run reports the same findings as new, your loop has no memory yet.

---

## Files

- `scan_repo.py` — the deterministic gather step. Pure Python, scans for `TODO`/`FIXME` comments and lists commits from the last 24 hours. No dependency on `grep`, so it works on Windows too.
- `progress.md` — the spine. Starts empty; the skill reads it first and writes to it last.
- `app.py` — sample source file with 2 planted TODOs, so the first scan has something real to find.
- `.claude/skills/morning-brief/SKILL.md` — all the task logic, so the prompt stays one line.
- `.opencode/skills/morning-brief/SKILL.md` — the same skill, for OpenCode.

## Run it

```bash
git init
git add .
git commit -m "init"
python3 scan_repo.py   # confirm it finds the 2 TODOs before touching a loop
```

Then, in a Claude Code session in this folder:

```
run the morning-brief skill
```

Run that exact line twice. The first run reports the TODOs and commits as new and writes them to `progress.md`. The second run should say nothing's new — because the skill tells it to check `progress.md` first.

To turn it into the actual scheduled loop the project asks for:

```
/schedule every day at 9am, run the morning-brief skill
```

## OpenCode equivalent

```bash
opencode run "run the morning-brief skill"
```

No built-in scheduler, so the operating system's own scheduler fires the same one-liner.

**Windows — Task Scheduler**

Windows has no `cron`; the native equivalent is Task Scheduler, run from the command line with `schtasks`. Point it at a small `.bat` wrapper (`run_brief.bat`, included) instead of inlining the command, to avoid quoting problems.

Create the daily 9am task:
```cmd
schtasks /create /tn "MorningBrief" /tr "C:\path\to\project\agentfactory-practice-projects\loop-engineering\03-the-morning-brief-with-a-memory\run_brief.bat" /sc daily /st 09:00
```

To test the loop actually fires without waiting a full day, create a second task that runs every 5 minutes:
```cmd
schtasks /create /tn "MorningBriefTest" /tr "C:\path\to\project\agentfactory-practice-projects\loop-engineering\03-the-morning-brief-with-a-memory\run_brief.bat" /sc minute /mo 5
```

Check it fired — `morning-brief.log` in the project folder should show a new entry every 5 minutes, and `progress.md`'s second entry onward should say nothing's new.

Stop it once you've confirmed it works:
```cmd
schtasks /delete /tn "MorningBriefTest" /f
```
(swap `/tn` to `MorningBrief` to delete the daily one instead; `/f` skips the confirmation prompt)

**macOS/Linux — cron**

```bash
0 9 * * * cd /home/yourusername/agentfactory-practice-projects/loop-engineering/03-the-morning-brief-with-a-memory && /home/yourusername/.local/bin/opencode run "run the morning-brief skill" >> /home/yourusername/morning-brief.log 2>&1
```

Stop it: run `crontab -e` and delete the line, or comment it out with a leading `#`.
