# Project 04: A fix loop with a real checker

An implementer drafts, a separate reviewer grades, and only PASS opens a PR.

*Difficulty: medium–hard · Uses: Concept 8 (worktree), Concept 9 (skill), Concept 11 (maker–checker).*

**Build.** A smaller version of the Part 5 loop. Write a short skill with your fix steps, and a reviewer agent that replies `PASS` or `FAIL`. Take one real bug, have the implementer draft a fix in its own checkout (worktree or branch), and let the reviewer grade it. Open a PR only on `PASS`.

**Done when** two things are both true: a good fix gets a `PASS` and a PR, *and* a deliberately bad fix you plant gets a `FAIL` with reasons. If the reviewer passes the bad fix, your checker is too soft — tighten it. A checker that approves everything is no checker.

---


Run the fix-loop skill.