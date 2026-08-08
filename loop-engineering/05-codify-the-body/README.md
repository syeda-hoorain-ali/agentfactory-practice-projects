# Project 05: Codify the body

Turn Project 4's orchestration into one re-runnable unit — then prove it is not a loop.

*Difficulty: medium–hard · Uses: the dynamic-workflows interlude, Concepts 8 and 11.*

**Build.** Take the fix loop you built in Project 4 and codify its body. On the Claude Code approach, describe it in plain words: "use a workflow to draft fixes for these three issues in parallel worktrees, and have a reviewer grade each one." Let the runtime write and run the script. When a run does what you want, save it from the `/workflows` view as a `/command`. On the OpenCode approach, write the same thing as a shell script: a `for` loop over the candidates, `&`/`wait` for the fan-out, and the reviewer's exit code as the checker. Run it twice.

**Done when** two things are true. First, one command (or one script) runs the whole draft-and-review body — several candidates, isolated checkouts, a verdict for each — with no step-by-step prompting from you. Second, you have proved the interlude's warning on your own machine: start a fresh session (or a fresh shell) and confirm the workflow remembers nothing from its last run. Then name what it would need to become a loop: a heartbeat to fire it, and a progress file its agents write. If you can name those two, you understand the difference between an engine and a loop. (Dynamic workflows are a research preview; where this project and the live docs disagree, the docs win.)

---
