---
name: morning-brief
description: >-
  Gathers overnight events from overnight-events.json, compares them against
  progress.md, and reports only what's new. Updates progress.md with today's
  findings and the date. Use this for the scheduled morning-brief loop.
---

# Morning brief

You are the morning-brief loop. Work through these steps in order.
Do not skip progress.md. It is your only memory between runs.
Every run writes exactly one line to run_log.md, whether it succeeds or
fails. A silent failure is the worst kind.

## 1. Read your memory first
- Open `progress.md` at the project root. Read the "Done" section to see
  what was already reported, and the "Open / needs a human" section to see
  what is still waiting on a person.

## 2. Gather the facts
- Read the file `overnight-events.json` at the project root and treat its
  contents as this run's raw facts.

## 3. If the gather step fails (the file is missing, unreadable, or empty)
- Do not proceed to comparing or summarizing. Do not touch the "Done"
  section — nothing new was actually found, so nothing is "done."
- Append one line to `run_log.md`, in this exact format:
  `[<ISO-8601 timestamp>] FAIL — <what you tried, and what broke>`
- Add one dated entry to the "Open / needs a human" section of `progress.md`:
  what you tried, and why you stopped.
- Save `progress.md`. Stop. Do not retry within this run, and do not
  substitute a different data source to force a result.

## 4. If the gather step succeeds
- Compare the facts gathered against what's already listed under "Done".
- Write a short summary of only what's NEW since the last run.
- Append one line to `run_log.md`:
  `[<ISO-8601 timestamp>] OK — gathered facts, wrote <n> new item(s) to progress.md`
- Add today's new findings under "Done" with today's date in `progress.md`.
- Save `progress.md`.

## Rules
- Never fabricate a plausible-sounding result to keep the run "green."
  A clear failure beats a quiet, wrong success.
- Every run ends with exactly one new line in `run_log.md`. No exceptions.
- Only step 3 or step 4 runs in a given beat, never both.
