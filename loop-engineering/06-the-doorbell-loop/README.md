# Project 06: The doorbell loop

A loop that reacts to a pull request — with no prompt typed.

*Difficulty: medium · Uses: Concept 7 (event-driven), Concept 10 (connectors).*

**Build.** Make your throwaway repo review its own pull requests. On the OpenCode approach, run `opencode github install` and accept the workflow it generates. On the Claude Code approach, create a Routine with a GitHub pull-request trigger (the [appendix](#appendix-routines) walks through the filters). Then open a PR that contains one planted bug — an off-by-one, a deleted null check — and wait.

**Done when** the PR gets a review you never asked for, and the review flags the planted bug. If the review misses it, tighten the prompt and push again — the push fires the loop once more through the synchronize event, and that re-fire is the event heartbeat working. With Projects 1–3, this completes all four heartbeats: in-session, conditional, scheduled, and event-driven.

---
