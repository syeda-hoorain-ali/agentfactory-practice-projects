---
name: dreaming-loop
description: Weekly loop that reads other loops' progress.md logs since the last dream, finds failures/corrections that repeat, and proposes the smallest rules-file fix as a PR.
---

# Dreaming Loop

This is the maker-checker pair for Project 12. Do NOT skip steps or improvise
the analysis yourself — the counting step must come from the script, not
your own reading of the logs. You are the checker/drafter on top of it.

## Step 1 — Run the deterministic gather step

```bash
python3 analyze_logs.py
```

This writes `dreaming-report.json` in this folder. Read that file. It contains:

- `repeated_issues`: tags that appeared more than once as a failure/correction
  since `last_dream_date`, each with the exact source file, date, and line
  for every occurrence (this is your evidence — never invent evidence).
- `unused_rule_candidates`: rules in the root rules file whose tag was not
  referenced anywhere in this window (your deletion candidate).
- `rules_file`: which file to edit — `CLAUDE.md` or `AGENTS.md` (mirror the
  edit into whichever of the two also exists at the repo root, so both stay
  in sync).

## Step 2 — Nothing to dream about?

If `repeated_issues` is an empty list: do not create a branch or a PR.
Just append one line to `dreaming-state.md` under `## Dream Log`:

```
- YYYY-MM-DD: nothing repeated since last dream, no PR opened.
```

Then update `last_dream_date` to today's date and stop.

## Step 3 — Draft the smallest fix, per repeated issue

Cap yourself at the 3 highest-count issues from `repeated_issues`, even if
more exist — a PR proposing ten rule changes at once is not "the smallest
change," it's a rewrite. For each one you address:

- Write ONE new bullet line for the rules file, in the same
  `- [tag] rule text` style as the existing rules, tagged with the same tag
  as the issue.
- The line must be the smallest instruction that would have prevented that
  specific failure — not a general reminder. ("Check that a git remote is
  configured before running `git log`; if missing, log it and skip commit
  gathering instead of retrying" beats "Be careful with git.")
- Do not touch any other part of the rules file.

## Step 4 — Propose exactly one deletion

Take the first entry from `unused_rule_candidates` (if any). Mark that
existing bullet line for removal. If `unused_rule_candidates` is empty,
skip this — do not force a deletion that has no evidence.

## Step 5 — Isolate and commit — never a direct commit to main

```bash
git checkout -b claude/dreaming-$(date +%Y-%m-%d)
```

Apply the additions and the one deletion to `CLAUDE.md` (and `AGENTS.md` if
it also exists — keep them identical). Commit:

```bash
git add CLAUDE.md AGENTS.md
git commit -m "dreaming loop: propose N rule fix(es) from repeated failures"
```

## Step 6 — Open the PR with cited evidence

Push the branch and open a **draft** PR (draft = the human gate: nothing
merges without a person). Use `gh`:

```bash
git push -u origin claude/dreaming-$(date +%Y-%m-%d)
gh pr create --draft --base main \
  --title "Dreaming loop: N rule fix(es) from repeated failures" \
  --body-file pr-body.md
```

Before that, write `pr-body.md` in this folder with this shape, one section
per issue you addressed:

```markdown
## Evidence
- Tag: missing-remote — 3 occurrences
  - loop-engineering/03-the-morning-brief-with-a-memory/progress.md, 2026-07-29
  - loop-engineering/03-the-morning-brief-with-a-memory/progress.md, 2026-07-31
  - loop-engineering/03-the-morning-brief-with-a-memory/progress.md, 2026-08-02

## Why this line stops it
[one or two sentences: what the new rule tells the agent to do differently
next time it hits this exact situation]

## Proposed deletion
- [tag] rule text — not referenced by any run since <last_dream_date>
```

If `gh` isn't available or there's no GitHub remote configured, stop after
the commit, tell the user the branch name, and give them the exact `gh pr
create` command to run themselves once they've pushed.

## Step 7 — Update the spine

Append to `dreaming-state.md` under `## Dream Log`:

```
- YYYY-MM-DD: N issue(s) addressed (tags: ...), 1 deletion proposed, PR: <url or "not opened, gh unavailable">.
```

Then update `last_dream_date` to today's date, so the next dream only reads
what's new. This last edit happens on `main` directly (it's bookkeeping
about the loop itself, not the codebase) — commit it separately from the
PR branch.
