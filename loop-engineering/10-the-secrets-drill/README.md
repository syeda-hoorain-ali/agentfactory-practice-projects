# The secrets drill

Fail the .env way once, on purpose, so you never do it by accident.

*Difficulty: easy to medium · Uses: A4 (secrets), A2 (the environment).*

**Build.** Write a prompt that needs one secret. A dummy token is fine, because the drill is about where the value lives, not what it unlocks. First run: put the token in a gitignored `.env` file and fire the routine. Watch it fail to find the value, and read the transcript to see what Claude tried instead. Second run: move the token into the environment-variables panel, and add the one prompt line the appendix recommends: *"credentials are available as environment variables; do not look for a `.env` file."*

**Done when** the second run reads the token from the environment, and you can explain the mechanical reason the first run could not: gitignored files never reach GitHub, so the fresh cloud clone never contains them.

---
