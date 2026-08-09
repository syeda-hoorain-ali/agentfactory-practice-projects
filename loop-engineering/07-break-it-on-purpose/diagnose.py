#!/usr/bin/env python3
"""
diagnose.py — read only what the loop left behind: run_log.md and
progress.md. No replaying the run, no calling the model. This is the
"read the spine first" habit from Part 6's "When an unattended loop fails."

Usage:
    python3 diagnose.py
"""
import re

LOG_LINE = re.compile(r"^\[(?P<ts>[^\]]+)\]\s+(?P<status>OK|FAIL)\s+—\s+(?P<detail>.*)$")


def read_log(path="run_log.md"):
    entries = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = LOG_LINE.match(line.strip())
                if m:
                    entries.append(m.groupdict())
    except FileNotFoundError:
        pass
    return entries


def read_needs_a_human(path="progress.md"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return []
    m = re.search(r"## Open / needs a human\s*\n(.*?)(\n## |\Z)", text, re.S)
    if not m:
        return []
    block = m.group(1).strip()
    if not block or block.startswith("("):
        return []
    return [line.strip("- ").strip() for line in block.splitlines() if line.strip()]


def main():
    log = read_log()
    needs_human = read_needs_a_human()

    if not log:
        print("run_log.md has no parseable entries. That is itself the finding:")
        print("a loop that leaves nothing behind cannot be diagnosed — see Part 6.")
        return

    last = log[-1]
    fails = [e for e in log if e["status"] == "FAIL"]

    print("=== Diagnosis, from the spine alone ===\n")
    print(f"Last beat:   {last['ts']}  [{last['status']}]")
    print(f"Detail:      {last['detail']}\n")

    if last["status"] == "FAIL":
        print("This beat failed. Checking for a 'needs a human' note...")
        if needs_human:
            print("Found it in progress.md:")
            for line in needs_human:
                print(f"  - {line}")
            print("\nVerdict: the loop failed loudly, as designed. No silent failure.")
        else:
            print("No 'needs a human' entry found in progress.md.")
            print("Verdict: this loop failed SILENTLY. Fix the skill's failure")
            print("handling before trusting it unattended again (Part 6).")
    else:
        print("Last beat succeeded. Nothing to diagnose.")

    if len(fails) > 1:
        print(f"\nHeads up: {len(fails)} FAIL entries total in run_log.md.")
        print("A single failure is a rehearsal. A repeated one is a broken schedule.")


if __name__ == "__main__":
    main()
