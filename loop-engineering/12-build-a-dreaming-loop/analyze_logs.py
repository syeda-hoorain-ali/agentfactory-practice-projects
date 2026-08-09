#!/usr/bin/env python3
"""
Deterministic gather step for the dreaming loop (Project 12).

Reads dreaming-state.md for the last-processed date and the list of
source progress.md files. Scans every dated entry newer than that date
across all sources. Groups any line tagged with [some-tag] and counts
how many times each tag recurs. Also checks which rules in the root
CLAUDE.md / AGENTS.md were referenced (by tag) in this window, so an
unreferenced rule can be proposed for deletion.

Writes dreaming-report.json. Prints nothing else, no network calls,
no LLM calls -- this is the "command decides" half of maker-checker.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent  # loop-engineering/12-.../ -> loop-engineering/ -> repo root
STATE_FILE = HERE / "dreaming-state.md"
REPORT_FILE = HERE / "dreaming-report.json"

DATE_HEADER_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")
TAG_RE = re.compile(r"\[([a-z0-9\-]+)\]")
FAILURE_MARKERS = ("NEEDS HUMAN", "FAIL", "CORRECTION", "ERROR", "SKIPPED")


def parse_state():
    if not STATE_FILE.exists():
        sys.exit(f"Missing {STATE_FILE}. Create it first (see README).")
    text = STATE_FILE.read_text()
    date_match = re.search(r"last_dream_date:\s*(\d{4}-\d{2}-\d{2})", text)
    if not date_match:
        sys.exit("dreaming-state.md has no 'last_dream_date: YYYY-MM-DD' line.")
    last_date = date_match.group(1)

    sources = []
    in_sources = False
    for line in text.splitlines():
        if line.strip() == "sources:":
            in_sources = True
            continue
        if in_sources:
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                sources.append(m.group(1).strip())
            elif line.strip() == "" or not line.startswith(" "):
                in_sources = False
    if not sources:
        sys.exit("dreaming-state.md lists no sources under 'sources:'.")
    return last_date, sources


def parse_progress_md(path: Path):
    """Yields (date_str, [lines]) for each dated section in a progress.md."""
    if not path.exists():
        return
    current_date = None
    current_lines = []
    for raw_line in path.read_text().splitlines():
        m = DATE_HEADER_RE.match(raw_line)
        if m:
            if current_date:
                yield current_date, current_lines
            current_date = m.group(1)
            current_lines = []
        elif current_date and raw_line.strip().startswith("-"):
            current_lines.append(raw_line.strip().lstrip("- ").strip())
    if current_date:
        yield current_date, current_lines


def collect_rule_tags():
    """Returns {tag: rule_line_text} from CLAUDE.md (falls back to AGENTS.md)."""
    for fname in ("CLAUDE.md", "AGENTS.md"):
        rules_file = REPO_ROOT / fname
        if rules_file.exists():
            rules = {}
            for line in rules_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("- ["):
                    m = TAG_RE.search(line)
                    if m:
                        rules[m.group(1)] = line.lstrip("- ").strip()
            if rules:
                return fname, rules
    return None, {}


def main():
    last_date, sources = parse_state()

    occurrences = {}  # tag -> list of {source, date, line}
    referenced_tags = set()
    entries_scanned = 0

    for source in sources:
        source_path = (HERE / source).resolve()
        source_label = source
        for entry_date, lines in parse_progress_md(source_path):
            if entry_date <= last_date:
                continue
            entries_scanned += 1
            for line in lines:
                tags_in_line = TAG_RE.findall(line)
                is_failure = any(marker in line for marker in FAILURE_MARKERS)
                for tag in tags_in_line:
                    referenced_tags.add(tag)
                    if is_failure:
                        occurrences.setdefault(tag, []).append(
                            {"source": source_label, "date": entry_date, "line": line}
                        )

    repeated_issues = [
        {"tag": tag, "count": len(hits), "occurrences": hits}
        for tag, hits in occurrences.items()
        if len(hits) > 1
    ]
    repeated_issues.sort(key=lambda x: -x["count"])

    rules_file, rules = collect_rule_tags()
    unused_rules = [
        {"tag": tag, "rule_line": text}
        for tag, text in rules.items()
        if tag not in referenced_tags
    ]

    report = {
        "run_date": str(date.today()),
        "since_date": last_date,
        "sources_scanned": sources,
        "entries_scanned": entries_scanned,
        "repeated_issues": repeated_issues,
        "rules_file": rules_file,
        "unused_rule_candidates": unused_rules,
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2))
    print(f"Wrote {REPORT_FILE}")
    print(f"  entries scanned: {entries_scanned}")
    print(f"  repeated issues (>1 occurrence): {len(repeated_issues)}")
    print(f"  unused-rule candidates: {len(unused_rules)}")


if __name__ == "__main__":
    main()
