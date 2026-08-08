#!/usr/bin/env bash
# long_task.sh — simulates a long-running task (e.g. a deploy or a migration).
# It sleeps for a while, then writes a file to signal it's done.
# Run this in the background, then have your loop watch for the output file.
 
echo "$(date '+%H:%M:%S') — task started, will finish in ~3 minutes..."
 
sleep 180   # pretend to do real work for 3 minutes
 
echo "status: done" > task-status.txt
echo "finished_at: $(date '+%Y-%m-%d %H:%M:%S')" >> task-status.txt
 
echo "$(date '+%H:%M:%S') — task finished, wrote task-status.txt"
