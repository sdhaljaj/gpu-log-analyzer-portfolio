from pathlib import Path
import argparse
import json
import sys


def normalize_level(level: str) -> str:
    """Return a canonical known log level or UNKNOWN."""
    normalized = level.strip().upper()
    if normalized in {"ERROR", "WARNING", "INFO"}:
        return normalized
    return "UNKNOWN"


def read_log(path: Path) -> str:
    """Return the UTF-8 contents of path."""
    return path.read_text(encoding="utf-8")


def count_levels(levels: list[str]) -> dict[str, int]:
    """Return counts for known normalized log levels."""
    counts = {
        "ERROR": 0,
        "WARNING": 0,
        "INFO": 0,
    }
    for level in levels:
        normalized_level = normalize_level(level)
        if normalized_level in counts:
            counts[normalized_level] += 1
    return counts


def extract_level(line: str) -> str:
    """Return the normalized level before the first colon, or UNKNOWN."""
    if ":" not in line:
        return "UNKNOWN"
    return normalize_level(line.split(':', 1)[0])


def analyze_log_text(text: str) -> dict[str, int]:
    """Return known-level counts from log text."""
    levels = []
    for line in text.splitlines():
        levels.append(extract_level(line))
    return count_levels(levels)


def analyze_log_file(path: Path) -> dict[str, int]:
    """Read a UTF-8 log file and return known-level counts."""
    return analyze_log_text(read_log(path))


def format_summary(counts: dict[str, int]) -> str:
    """Return the known-level counts in a stable three-line report."""
    lines = [
        f'ERROR: {counts["ERROR"]}',
        f'WARNING: {counts["WARNING"]}',
        f'INFO: {counts["INFO"]}',
    ]
    return "\n".join(lines)


def exit_code_for_counts(counts: dict[str, int]) -> int:
    """Return 1 when ERROR entries exist; otherwise return 0."""
    if counts["ERROR"] > 0:
        return 1
    return 0


def format_json_summary(counts: dict[str, int]) -> str:
    """Return a JSON string."""
    return json.dumps(counts)


def write_report(path: Path, report: str) -> None:
    """Write a report with a trailing newline as UTF-8 text."""
    path.write_text(report + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Print a known-level report for one log file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("log_path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        counts = analyze_log_file(Path(args.log_path))
    except FileNotFoundError:
        print(f"ERROR: log file not found: {args.log_path}", file=sys.stderr)
        return 2
    if args.json:
        report = format_json_summary(counts)
    else:
        report = format_summary(counts)
    if args.output is not None:
        write_report(Path(args.output), report)
    else:
        print(report)
    return exit_code_for_counts(counts)


if __name__ == "__main__":
    raise SystemExit(main())
