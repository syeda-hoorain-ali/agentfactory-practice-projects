# Project 01: A Watch Loop

Make a loop watch a long task and tell you the moment it finishes.

*Difficulty: easy · Uses: Concept 4 (in-session loop).*

**Build.** Start a long task in your repo (for example, a script that sleeps for a while and then writes a file). Set up an in-session loop that checks every minute whether the task has finished, and tells you the moment it has.

**Done when** the loop notices the task finished, says so once, and you can stop it cleanly — and you never sat watching the terminal.

---

## Files

- `long_task.sh` — the "long task." Sleeps for 3 minutes, then writes `task_status.txt`.

## Run it

```bash
chmod +x long_task.sh
./long_task.sh &
```

Then, in a Claude Code session in this folder:

```
/loop 30s check if task-status.txt exists. If it does, read it, tell me the task is done and show its contents, then stop this loop. If it doesn't exist yet, just say "still running" and nothing else.
```

When it reports done, cancel it:

```
show my running loops
cancel the task-watch loop
```

## OpenCode equivalent

No `/loop` command in OpenCode, so the heartbeat is a shell loop:

```bash
while true; do
  if [ -f task-status.txt ]; then
    opencode run "read task-status.txt and tell me if the task is done and show its contents. If it doesn't exist, just say "still running" and nothing else"
    break
  fi
  sleep 30
done
```
