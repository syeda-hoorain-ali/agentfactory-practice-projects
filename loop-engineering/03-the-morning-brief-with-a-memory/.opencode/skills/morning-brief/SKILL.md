---
name: morning-brief
description: >-
  Gathers open TODO/FIXME comments and the last day's commits from the repo,
  compares them against progress.md, and reports only what's new. Updates
  progress.md with today's findings and the date. Use this for the scheduled
  morning-brief loop.
---

# Morning brief

You are the morning-brief loop. Work through these steps in order.
Do not skip progress.md. It is your only memory between runs.

## 1. Read your memory first
- Open `progress.md` at the project root. Read the "Done" section 
  to see what was already reported.

## 2. Gather the facts
- Run `python3 scan_repo.py`. This prints open TODO/FIXME comments and
  commits from the last 24 hours. Trust its output over your own guess.

## 3. Compare and summarize
- Compare the scan's output against what's already listed under "Done".
- Write a short summary (a few bullet points) of only what's NEW since the
  last run. If nothing is new, say so plainly — do not repeat old findings.

## 4. Update your memory last
- Add today's new findings under "Done" with today's date.
- If anything is unclear or needs a person, add it under "Open / needs a human".
- Save progress.md at the project root. This is the file tomorrow's run will read.
