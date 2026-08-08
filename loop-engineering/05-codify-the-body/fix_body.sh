#!/usr/bin/env bash
# Project 05 — codify the body (OpenCode version).
#
# This script IS the body of one beat: draft, in parallel, isolated
# worktrees; grade each with the reviewer; report each verdict. It has no
# heartbeat (nothing fires it on its own) and no spine (nothing here
# writes a progress file that a later run reads). Run it twice and prove
# that to yourself — see the README's "prove it's not a loop" section.

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_DIR="loop-engineering/05-codify-the-body"
CANDIDATES=(subtract divide is_even)
LOG_DIR="$REPO_ROOT/.worktrees/05-logs"
mkdir -p "$LOG_DIR"

echo "== fanning out ${#CANDIDATES[@]} candidates in parallel worktrees =="

pids=()

for candidate in "${CANDIDATES[@]}"; do
  (
    WT="$REPO_ROOT/.worktrees/05-fix-${candidate}-wt"
    BRANCH="fix/${candidate}"

    # Fresh worktree each run — remove a stale one from a previous attempt.
    git worktree remove "$WT" --force >/dev/null 2>&1 || true
    git branch -D "$BRANCH" >/dev/null 2>&1 || true
    git worktree add "$WT" -b "$BRANCH" -q

    cd "$WT/$PROJECT_DIR" || exit 1

    echo "[$candidate] drafting fix..."
    opencode run "In calculator.py, fix only the ${candidate} function — it has exactly one bug. Do not touch any other function or any test. Run 'pytest -q -k ${candidate}' yourself to confirm your fix works before finishing." \
      > "$LOG_DIR/${candidate}.maker.log" 2>&1

    echo "[$candidate] sending diff to reviewer..."
    DIFF=$(git diff main -- "$PROJECT_DIR")
    VERDICT=$(opencode run "@reviewer You are reviewing the '${candidate}' candidate. Here is the diff:
$DIFF" 2>&1)

    echo "$VERDICT" > "$LOG_DIR/${candidate}.verdict.log"

    if echo "$VERDICT" | grep -q "^PASS"; then
      echo "[$candidate] PASS"
      exit 0
    else
      echo "[$candidate] FAIL"
      exit 1
    fi
  ) &
  pids+=($!)
done

# Collect each background job's own exit code — this IS the checker.
overall=0
for i in "${!pids[@]}"; do
  candidate="${CANDIDATES[$i]}"
  if wait "${pids[$i]}"; then
    echo "RESULT: $candidate -> PASS"
  else
    echo "RESULT: $candidate -> FAIL"
    overall=1
  fi
done

echo "== all candidates finished =="
echo "Verdicts (full text) are in $LOG_DIR/*.verdict.log"
exit $overall
