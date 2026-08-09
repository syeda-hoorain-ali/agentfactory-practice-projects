# Build the two-routine gate

A drafts, you decide, and only your decision fires B.

*Difficulty: medium to hard · Uses: A3 (the API trigger), A4 (the gate), A6 (the checklist).*

**Build.** Routine A, on a one-off schedule, drafts something reviewable: a `claude/` branch, or a short summary posted through a connector. Routine B has an API trigger and performs one small follow-up action. Store B's bearer token the moment it is shown, because it is shown once. Review A's draft yourself. Then approve it by firing B with the `curl` call from A3.

**Done when** three things are true: B ran only because you fired it, B's transcript shows the action actually happened, and you have run the A6 checklist over both routines, with connectors pruned, unrestricted pushes off, and a state file chosen. This is the human gate from Part 5, and now you have built it out of real parts.

---
