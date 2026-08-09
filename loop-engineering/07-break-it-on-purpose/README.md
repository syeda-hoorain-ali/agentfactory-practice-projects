# Project 07: Break It on Purpose

Sabotage your own loop, then diagnose it from the spine alone.

*Difficulty: medium · Uses: Observability, Concept 13 (cost), Concept 14.*

**Build.** Take your Project 3 loop. First, measure one beat: note roughly how many tokens a run reads and writes, and multiply by your cadence to get a monthly cost — Concept 13's math on your own loop. Then sabotage it: point the prompt at a file that does not exist, or give it a success condition it can never meet (with a limit set). Let it fire on schedule and fail. Now diagnose the failure using only what the loop left behind — the log line and `progress.md` — without replaying the full run.

**Done when** three things are true. You can say what failed, and when, from the spine alone. The loop left a clear "needs a human" note instead of failing silently. And you know your loop's monthly cost at its current cadence. If it failed silently, fix that before anything else by adding the log line. You are rehearsing the overnight failure now, while it is cheap and you are watching.

---

## What this project actually does

Project 3's loop, with one line of its gather step changed: instead of
running `scan_repo.py`, it reads `overnight-events.json`, a file that does
not exist in this folder. That's the entire sabotage. Everything else —
the spine, the one-line prompt, the schedule shape — stays the same as
Project 3.

## Files

- `scan_repo.py` — reused unchanged from Project 3.
- `app.py` — reused unchanged from Project 3 (the 2 planted TODOs).
- `progress.md` — the spine, seeded with 3 days of real history so there's
  something established to compare a failure against.
- `run_log.md` — the log, seeded with 3 matching `OK` lines. The run you
  fire next should append the first `FAIL` line.
- `.claude/skills/morning-brief/SKILL.md` — the skill. Reads as an ordinary skill 
  with normal failure handling — points at `overnight-events.json` file that does not exist
- `.opencode/skills/morning-brief/SKILL.md` — same, for OpenCode.
- `measure_beat.py` — Concept 13's cost math. Takes the token counts you
  observe from one real run and gives you a monthly cost at your cadence.
- `diagnose.py` — reads only `run_log.md` and `progress.md`'s "Open / needs
  a human" section and reports what failed and when. This is the "diagnose
  without replaying the full run" step, and it's a plain script, not an
  agent call — it doesn't need to be kept in the dark about anything.
- `run_brief.bat` — Windows Task Scheduler wrapper, same pattern as
  Project 3's `run_brief.bat`.

Note: `overnight-events.json` does **not** exist in this folder. Do not
create it until you're done rehearsing the failure.

## Run it

### Step 1 — measure one real beat (do this BEFORE firing anything here)

If you still have Project 3's working skill available, run it once for
real and note the token usage Claude Code reports at the end of the
session (or check the Routine's run page if it's scheduled). Then:

```bash
cd agentfactory-practice-projects/loop-engineering/07-break-it-on-purpose
python3 measure_beat.py --input-tokens 40000 --output-tokens 6000 \
    --beats-per-day 1 --days-per-month 30

# override pricing if you're on a different model / current pricing:
python3 measure_beat.py --input-tokens 40000 --output-tokens 6000 \
    --beats-per-day 1 --days-per-month 30 \
    --input-price-per-million 3 --output-price-per-million 15
```

### Step 2 — fire the loop exactly as you normally would

In a Claude Code session in this folder:

```
Run the morning-brief skill
```

That's the whole prompt. It's the same line you'd use on a working loop,
because from the agent's side, nothing is different — it just reads
`progress.md`, tries to read `overnight-events.json`, and finds out from
there that the file doesn't exist. What happens next is entirely the
skill's own Step 3, not something you told it to expect.

To fire it on a schedule instead of by hand:

```
/schedule every day at 9am, run the morning-brief skill
```

### Step 3 — diagnose without replaying the run

Don't reopen the transcript. Read only what the loop left behind:

```bash
python3 diagnose.py
```

This prints the last beat's timestamp and status, confirms whether a
"needs a human" note exists, and tells you plainly if the loop failed
silently instead (which would mean the skill's failure handling is
broken, not just the file it's looking for).

## OpenCode equivalent

```bash
opencode run "Run the morning-brief skill"
```

No built-in scheduler, so the operating system's own scheduler fires the
same one-liner — identical pattern to Project 3.

**Windows — Task Scheduler**

```cmd
schtasks /create /tn "BreakItOnPurpose" /tr "C:\path\to\project\agentfactory-practice-projects\loop-engineering\07-break-it-on-purpose\run_brief.bat" /sc daily /st 09:00
```

To test without waiting a day:

```cmd
schtasks /create /tn "BreakItOnPurposeTest" /tr "C:\path\to\project\agentfactory-practice-projects\loop-engineering\07-break-it-on-purpose\run_brief.bat" /sc minute /mo 5
```

Check `morning-brief.log` for output, and `run_log.md` for the `FAIL`
line. Stop it once confirmed:

```cmd
schtasks /delete /tn "BreakItOnPurposeTest" /f
```

**macOS/Linux — cron**

```bash
0 9 * * * cd /home/yourusername/agentfactory-practice-projects/loop-engineering/07-break-it-on-purpose && /home/yourusername/.local/bin/opencode run "run the morning-brief skill" >> /home/yourusername/morning-brief.log 2>&1
```

Stop it: `crontab -e`, then delete or comment out the line.

## Checking the three "Done when" conditions

1. **What failed, and when, from the spine alone** — run `python3
   diagnose.py`. It prints the last beat's timestamp, status, and the
   "needs a human" note, reading nothing but `run_log.md` and
   `progress.md`.
2. **A clear "needs a human" note, not a silent failure** — open
   `progress.md` and confirm a new dated entry sits under "Open / needs
   a human," and that "Done" was not touched.
3. **Your loop's monthly cost at its current cadence** — the number
   `measure_beat.py` printed in Step 1, using your own token counts and
   your own schedule (once a day, every weekday, whatever you actually
   set).

## Putting the loop back together

Once you're satisfied with the diagnosis, either create a real
`overnight-events.json`, or point Step 2 of the skill back at
`scan_repo.py` the way Project 3 had it. Either way, that's a decision
you make outside the skill — the skill itself never needs to know it was
ever broken.



<!-- 
python3 measure_beat.py --input-tokens 10000 --output-tokens 3000 --beats-per-day 1 --days-per-month 26 --input-price-per-million 0.10 --output-price-per-million 0.40
Monthly cost:       $0.06

schtasks /create /tn "BreakItOnPurposeTest" /tr "D:\my-projects\agentfactory-practice-projects\loop-engineering\07-break-it-on-purpose\run_brief.bat" /sc minute /mo 5
-->

