# Project Rules

## Rules

- [morning-brief-scope] The morning-brief skill only reports TODOs and commits from the last 24 hours.
- [commit-style] Keep commit messages under 72 characters on the summary line.
- [missing-remote] Check that a git remote is configured before running `git log`; if missing, log it and skip commit gathering instead of retrying.
