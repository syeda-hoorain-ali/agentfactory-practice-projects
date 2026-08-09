# Project 11: Build the Two-Routine Gate

A drafts, you decide, and only your decision fires B.

*Difficulty: medium to hard · Uses: A3 (the API trigger), A4 (the gate), A6 (the checklist).*

**Build.** Routine A, on a one-off schedule, drafts something reviewable: a `claude/` branch, or a short summary posted through a connector. Routine B has an API trigger and performs one small follow-up action. Store B's bearer token the moment it is shown, because it is shown once. Review A's draft yourself. Then approve it by firing B with the `curl` call from A3.

**Done when** three things are true: B ran only because you fired it, B's transcript shows the action actually happened, and you have run the A6 checklist over both routines, with connectors pruned, unrestricted pushes off, and a state file chosen. This is the human gate from Part 5, and now you have built it out of real parts.

---

## Files

- `.claude/skills/draft-daily-digest/SKILL.md` — Routine A's logic, Claude Code path.
- `.claude/skills/publish-digest/SKILL.md` — Routine B's logic, Claude Code path.
- `.opencode/skills/draft-daily-digest/SKILL.md`, `.opencode/skills/publish-digest/SKILL.md` — the same two skills, OpenCode path.
- `.github/workflows/draft-digest.yml` — OpenCode's Routine A: scheduled, plus `workflow_dispatch` for a free one-off test.
- `.github/workflows/publish-digest.yml` — OpenCode's Routine B: fires on `repository_dispatch`, the API-trigger equivalent.
- `fire_routine_b.py` — fires Claude Code's Routine B with the A3 curl call, reading the token from a local `.env`.
- `.env.example` — vars `fire_routine_b.py` needs.
- `progress.md` — the spine for this project.

## Claude Code: 

### Set up Routine A

Remote routine (A1), this repo only, unrestricted pushes **off**. Prompt: `Run the draft-daily-digest skill.` No connectors. Trigger: one-off schedule first — `/schedule tomorrow at 9am, run the draft-daily-digest skill`, or *Run now*. Read the transcript (A5), confirm `DIGEST.md` on a new `claude/digest-<date>` branch and a `progress.md` line, main untouched.

### Set up Routine B

Same repo. Prompt: `Run the publish-digest skill.` No connectors. Trigger: **API**. Generate the token, paste it into `.env` immediately — shown once (A3).

```bash
cp .env.example .env
# fill in ROUTINE_B_ID and ROUTINE_B_TOKEN
```

### Rehearse locally first (Project 9 style)

```
run the draft-daily-digest skill
```
```
run the publish-digest skill; the approved branch is claude/digest-2026-08-09
```
Confirm B merges only that branch, and rejects a name that doesn't exist or doesn't start with `claude/`.

### Approve a real draft

1. Read `DIGEST.md` on the branch Routine A printed (`BRANCH: claude/digest-...`). This is the gate — nothing ships until you do this.
2. Fire Routine B:

```bash
python3 fire_routine_b.py claude/digest-2026-08-09
```

Open B's transcript and confirm the merge happened — green only means no infra error (A5).

### A6 checklist, both routines

Repos scoped, unrestricted pushes off. Prompts self-contained one-liners. No connectors. No secrets in either routine's own environment. Triggers chosen on purpose (schedule / API). State is `progress.md`, committed. Human gate: B only ever touches the one branch named at trigger time. Both fired once and transcripts read, not just the status color.

---

## OpenCode equivalent

No Routines dashboard here — everything above maps to GitHub Actions, per the appendix's own mapping: the environment-variables panel becomes **repository secrets**, the connector list becomes the `mcp` section of `opencode.json`, and schedule/PR triggers become `on: schedule` / `on: pull_request`.

### Set up Routine A: `draft-digest.yml`

Set one repo secret first: **Settings → Secrets and variables → Actions → New repository secret**, name `GEMINI_API_KEY`. This is the "environment variables panel" equivalent from A4 — never a committed `.env`.

Rehearse it for free, the same way Project 9 rehearses a routine: go to **Actions → opencode-draft-digest → Run workflow** (this is what `workflow_dispatch` gives you — a one-off run with no schedule attached, same purpose as a one-off `/schedule`). Open the run log and confirm `DIGEST.md` landed on a new `claude/digest-<date>` branch, `progress.md` got a line, and main was untouched — reading the log is your A5 step here too: green just means the job finished, not that the digest is good.

Once it looks right, leave the `schedule:` cron in the file as-is and it fires daily on its own.

### Set up Routine B: `publish-digest.yml`

Same repo secret (`GEMINI_API_KEY`) covers this workflow too — no separate token needed for the workflow itself. What you *do* need to generate and store immediately is a **GitHub personal access token** (fine-grained, scoped to just this repo, `contents: write` + the ability to dispatch): **Settings → Developer settings → Personal access tokens**. Copy it into your own local `.env` (or a password manager) the moment it's shown — GitHub won't show the full value again either. This token plays the same role B's Claude Code bearer token does: it's what lets *you*, the human, fire B on purpose.

### Approve a real draft

1. Read `DIGEST.md` on the branch Routine A's workflow run printed. This is the human gate.
2. Fire Routine B with the PAT you stored:

```bash
curl -X POST https://api.github.com/repos/<owner>/agentfactory-practice-projects/dispatches \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <GITHUB_PAT>" \
  -d '{"event_type":"approve-publish","client_payload":{"branch":"claude/digest-2026-08-09"}}'
```

Open the `opencode-publish-digest` run in **Actions** and confirm the merge actually happened in the log — a green checkmark on the workflow means the job completed, not that the merge succeeded on its own terms, so read it.

### A6 checklist, OpenCode version

Repo secrets set, no `.env` committed. Both workflows scoped to `paths: - 'loop-engineering/11-build-the-two-routine-gate/**'` so they never fire on unrelated changes elsewhere in the monorepo-style layout. Branch protection on `main` stands in for "unrestricted pushes off" (A5's OpenCode note: this is a rule you set yourself, not a toggle in a dashboard). State is `progress.md`, committed. Human gate: B's workflow only ever acts on the branch named in `client_payload.branch` — nothing scans for "the latest" branch on its own. Both workflows run once via manual dispatch first, and the run logs read, not just the checkmark.

