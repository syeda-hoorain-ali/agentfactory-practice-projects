---
name: data-collector
description: Pull the latest metrics snapshot and report what came back.
---

Run `python3 fetch_data.py` from the project root.

We need the data it returns. If it succeeds, report what was fetched: how many records, and the snapshot date. If it fails, report the failure message exactly as printed and stop there — do not retry with a different value, do not go looking for the credential elsewhere in the repo, and do not invent a plausible-looking token to get past it.
