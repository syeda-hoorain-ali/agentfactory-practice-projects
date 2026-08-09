# The secrets drill

Fail the .env way once, on purpose, so you never do it by accident.

*Difficulty: easy to medium · Uses: A4 (secrets), A2 (the environment).*

**Build.** Write a prompt that needs one secret. A dummy token is fine, because the drill is about where the value lives, not what it unlocks. First run: put the token in a gitignored `.env` file and fire the routine. Watch it fail to find the value, and read the transcript to see what Claude tried instead. Second run: move the token into the environment-variables panel, and add the one prompt line the appendix recommends: *"credentials are available as environment variables; do not look for a `.env` file."*

**Done when** the second run reads the token from the environment, and you can explain the mechanical reason the first run could not: gitignored files never reach GitHub, so the fresh cloud clone never contains them.

---

## Files

- `fetch_data.py` — checks `SECRET_TOKEN` against a value; on match, prints the dataset; logs every attempt to `fetch-log.md`.
- `.env` — gitignored, holds the correct token locally. The script never reads it.
- `.claude/skills/data-collector/SKILL.md` / `.opencode/skills/data-collector/SKILL.md` — the one-line prompt's logic, framed as an ordinary data task.
- `.github/workflows/10-opencode-data-collector.yml` — manual (`workflow_dispatch`) OpenCode Action.

## Run it locally

```bash
git init && git add . && git commit -m "init"
python3 fetch_data.py            # SECRET_TOKEN unset → fails
export SECRET_TOKEN=my-super-secret-token
python3 fetch_data.py            # now matches → succeeds
```

Prompt (same line both runs):

```
Run the data-collector skill
```

## Run it on OpenCode / GitHub Actions

1. Push this repo. Don't add a `SECRET_TOKEN` repo secret yet.
2. Actions tab → **opencode-data-collector** → **Run workflow**. Watch it fail.
3. Add `SECRET_TOKEN` under Settings → Secrets and variables → Actions (value: `my-super-secret-token`).
4. Run the workflow again. It succeeds.

**Transcript:** click into the run → the `anomalyco/opencode/github@latest` step's log is the full transcript — every tool call and decision, same thing A5 has you read on a Routine's session page. The run also uploads a `fetch-log` artifact (`fetch-log.md`) since the job's filesystem disappears once the run ends — that artifact is your durable record, downloadable from the run's summary page for 90 days by default.
