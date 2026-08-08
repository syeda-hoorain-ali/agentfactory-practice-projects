# Project 05: Codify the body

Turn Project 4's orchestration into one re-runnable unit — then prove it is not a loop.

*Difficulty: medium–hard · Uses: the dynamic-workflows interlude, Concepts 8 and 11.*

**Build.** Take the fix loop you built in Project 4 and codify its body. On the Claude Code approach, describe it in plain words: "use a workflow to draft fixes for these three issues in parallel worktrees, and have a reviewer grade each one." Let the runtime write and run the script. When a run does what you want, save it from the `/workflows` view as a `/command`. On the OpenCode approach, write the same thing as a shell script: a `for` loop over the candidates, `&`/`wait` for the fan-out, and the reviewer's exit code as the checker. Run it twice.

**Done when** two things are true. First, one command (or one script) runs the whole draft-and-review body — several candidates, isolated checkouts, a verdict for each — with no step-by-step prompting from you. Second, you have proved the interlude's warning on your own machine: start a fresh session (or a fresh shell) and confirm the workflow remembers nothing from its last run. Then name what it would need to become a loop: a heartbeat to fire it, and a progress file its agents write. If you can name those two, you understand the difference between an engine and a loop. (Dynamic workflows are a research preview; where this project and the live docs disagree, the docs win.)

---

## Files

- `calculator.py` — three independent bugs, one per function (`subtract`, `divide`, `is_even`). Independent on purpose: three candidates that can be fixed in three parallel worktrees with zero risk of collision.
- `test_calculator.py` — 6 tests, 5 failing across the 3 functions (`5 failed, 1 passed`). Each candidate's tests can be run alone with `pytest -q -k <candidate>`.
- `.claude/agents/reviewer.md` — the checker. Told which candidate it's grading, runs `python -m pytest -q -k <candidate>` itself, confirms the diff touches only that one function, replies `PASS`/`FAIL`.
- `.opencode/agents/reviewer.md` — the same checker, for OpenCode.
- `.opencode/scripts/fix_body.sh` — the OpenCode version of the body: fans out one maker + one checker per candidate in parallel worktrees, `wait`s on all three, turns each reviewer verdict into that job's exit code.

Same monorepo pattern as Project 4: worktrees are created inside the repo, under the already-gitignored `.worktrees/`, prefixed `05-` so they never collide with `01-`, `02-`, `03-`, `04-`'s own worktrees.

## Setup (run once)

```bash
cd loop-engineering/05-codify-the-body
pip install pytest
python -m pytest -q   # confirm: 5 failed, 1 passed
```

## Claude Code — the dynamic workflow

Start a session **from inside this project's folder**, then describe the body in plain words — no skill needed here, this is what a dynamic workflow is for:

```
Use a workflow to draft fixes for the subtract, divide, and is_even bugs in
calculator.py, each in its own isolated worktree, in parallel. For each
one, have the reviewer subagent grade the diff PASS or FAIL before you
report back. Give me all three verdicts.
```

Watch it run: three isolated worktrees, three drafts, three reviewer calls, one report. Then:

1. Open the `/workflows` view.
2. If the run did what you wanted, press `s` to save it as a `/command`.
3. Re-run it with that saved command — that's your "one command runs the whole body" proof.

## OpenCode — the shell script

```bash
cd loop-engineering/05-codify-the-body
chmod +x .opencode/scripts/fix_body.sh
./.opencode/scripts/fix_body.sh
```

You should see all three candidates draft and get reviewed in parallel, then a final `RESULT: <candidate> -> PASS/FAIL` line for each. Full verdict text lands in `.worktrees/05-logs/<candidate>.verdict.log`.

Run it a second time — it cleans up its own worktrees from the last run first (`git worktree remove --force` at the top of each subshell), so it's safe to re-run without manual cleanup.

## Prove it's not a loop (the actual "done when")

A workflow — the `/command` you saved, or `fix_body.sh` — runs once, does real orchestration, and then forgets everything. Prove it:

**Claude Code:** close the session entirely, start a brand-new one, and ask:
```
What did the fix-workflow do last time it ran?
```
It shouldn't know. Nothing wrote that down anywhere the new session can read.

**OpenCode:** just look at the script. There's no file it writes to that a second run reads from — `.worktrees/05-logs/*.verdict.log` gets overwritten every run, not appended to or checked first. Run `./.opencode/scripts/fix_body.sh` twice in a row and confirm the second run redoes all three candidates from scratch, exactly like the first — it doesn't know it already fixed `subtract` five minutes ago.

**Now name the two things missing, out loud, before you check below:**

<details>
<summary>Answer</summary>

1. **A heartbeat.** Nothing here fires this on its own — you (or you typing the saved `/command`) start every run. Wire a schedule or event onto it (Concept 6 or 7) and it starts firing without you.
2. **A progress file — the spine.** Nothing here reads "what did I already fix" before starting, or writes "here's what I fixed" when it's done. Without that, even a scheduled version of this script would just refix the same three candidates every single run — Concept 12's exact warning: no spine, no loop.

That's the whole distinction this project is testing. The workflow is the **engine**. A heartbeat and a spine are what turn an engine into a **loop**.
</details>
