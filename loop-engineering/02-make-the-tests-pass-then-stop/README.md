# Project 02: Make the Tests Pass, Then Stop

Loop until a command — not the agent — decides the work is done.

*Difficulty: easy–medium · Uses: Concept 5 (conditional loop), Concept 11 (maker–checker).*

**Build.** Put 2–3 small failing tests in your repo. Build a loop that keeps working until the tests pass — but let a *command* (the test runner), not the agent, decide when it is done. Cap it at, say, 6 tries.

**Done when** the loop stops because the tests actually passed, not because it hit the cap. If it keeps hitting the cap, your stop condition or your prompt needs work. That is the lesson.

---

## Files

- `math_utils.py` — the source file. Ships with 3 deliberate bugs.
- `test_math_utils.py` — 3 small tests that fail against the buggy source.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install pytest
pytest   # confirm 3 tests fail before touching a loop
```

Then, in a Claude Code session in this folder:

```
/goal All tests in test_math_utils.py should pass, shown by running `pytest`. Stop after 6 tries if they still fail.
```

`/goal` has no built-in give-up, so the 6-try limit lives in the prompt itself. A separate checker reads the transcript after each turn — it can't run commands, so the agent has to actually run `pytest` and show the output for the checker to see it pass.

## OpenCode equivalent

No `/goal` command in OpenCode, so the checker is a plain shell `if`:

```bash
opencode serve -port 4096
for i in $(seq 1 6); do          # cap the tries — never loop forever
  opencode run --attach http://localhost:4096 "Make the tests in test_math_utils.py pass."
  if pytest; then
    echo "✔ Goal achieved ($i turn)"; break
  fi
done
```

`pytest`'s exit code is the checker: 0 on all-pass, non-zero otherwise.
