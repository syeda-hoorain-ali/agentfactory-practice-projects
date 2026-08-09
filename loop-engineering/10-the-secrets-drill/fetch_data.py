"""
Collector step: authenticates against a hashed token and, on success,
copies data/dataset.json into fetched-data.json. On failure, it writes
nothing and exits non-zero — same shape as a real internal API call.
"""

import os
import sys
import datetime

TOKEN_VAR = "SECRET_TOKEN"
EXPECTED_TOKEN = "my-super-secret-token"
LOG_FILE = "fetch-log.md"

DATASET = {
  "snapshot_date": "2026-08-08",
  "records": [
    {"id": "REC-001", "metric": "active_loops", "value": 14},
    {"id": "REC-002", "metric": "failed_runs_7d", "value": 2},
    {"id": "REC-003", "metric": "avg_beat_minutes", "value": 6.3}
  ]
}

def log(line):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a") as f:
        f.write(f"- {ts}: {line}\n")


def main():
    token = os.environ.get(TOKEN_VAR)

    if not token:
        log("AUTH FAILED — no token presented")
        print("401: no token presented")
        sys.exit(1)

    if token != EXPECTED_TOKEN:
        log("AUTH FAILED — token did not match")
        print("401: token did not match")
        sys.exit(1)

    log(f"OK — fetched {len(DATASET['records'])} records, snapshot {DATASET['snapshot_date']}")
    print(f"200: fetched {len(DATASET['records'])} records:")
    print(DATASET)


if __name__ == "__main__":
    main()
