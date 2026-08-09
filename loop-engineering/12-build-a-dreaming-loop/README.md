# Build a dreaming loop

A weekly loop that reads your other loops' logs and proposes rule changes as a PR.

*Difficulty: capstone · Uses: Concept 12 (spine and improvement loop), Concept 11 (maker-checker), Concept 6 (schedule), Part 5 (human gate).*

**Build.** You need a loop that has already run for a week and left dated entries in `progress.md` (Project 3 or Project 8 gives you one). Now build a second loop over it. On a weekly schedule, it reads all log entries since the date in its own `dreaming-state.md`, looks for any failure or correction that appears more than once, and drafts the smallest rules-file or skill change that would prevent it, as a PR on a `claude/` branch, never a direct commit. The PR description must cite its evidence: which runs, how often, and why this line stops it. Have it also propose one deletion: a rule no recent run needed. Finish by updating `dreaming-state.md`.

**Done when** three things are true. The PR's proposed change traces to real, cited log entries, not a plausible-sounding guess. A deliberately planted repeated failure in the logs (add one by hand) gets caught and turned into a proposal. And nothing changed in your rules file without you merging it. If the loop proposes changes with no evidence attached, tighten the prompt: an improvement loop that guesses is worse than no improvement loop, because its guesses steer every future run.

---
