#!/usr/bin/env python3
"""Check a business impact analysis (BIA) and a restore test log for consistency.

Standard library only. The playbook linter (check_playbooks.py) checks prose. This
tool checks the numbers behind the DR plan, using the rules written in
dr/rto-rpo-tiers.md:

BIA rules (errors)
  DR01  required columns present, ids unique, hours are numbers
  DR02  tier is T0 to T4 and the RTO and RPO sit inside the tier maximum
  DR03  RTO is shorter than the MTPD
  DR04  a process does not promise a faster RTO than the system it depends on
  DR05  a process is not in a faster tier than the system it depends on

A dependency is matched to the other processes that list that system as a primary system. The
system's commitment is taken as the strictest RTO and tier among them.

BIA notes and warnings
  DR06  impact ratings fall as the outage gets longer
  DR07  a dependency does not match any process on the BIA (listed, not failed)

Restore log rules
  DR10  a row recorded as Pass although it missed its own RTO or RPO (error)
  DR11  a process has no restore test on record (warning)
  DR12  the latest test is older than the tier's test frequency (warning)
  DR13  the latest test did not pass, or missed the BIA RTO or RPO (warning)

Exit status: 0 when there are no errors, 1 when there are errors (or warnings with
--strict), 2 on usage or file problems.

Usage::

    python tools/check_dr.py --bia dr/bia-worked-example.csv \\
        --restore-log dr/backup-restore-test-log-worked-example.csv --as-of 2026-11-02
    python tools/check_dr.py --bia my-bia.csv --restore-log my-log.csv --markdown
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_BIA = ROOT / "dr" / "bia-worked-example.csv"
EXAMPLE_LOG = ROOT / "dr" / "backup-restore-test-log-worked-example.csv"
EXAMPLE_REPORT = ROOT / "docs" / "dr-gap-report-example.md"
EXAMPLE_AS_OF = dt.date(2026, 11, 2)

BIA_COLUMNS = (
    "id", "name", "primary_systems", "impact_1h", "impact_4h", "impact_24h", "impact_72h",
    "mtpd_hours", "rto_hours", "rpo_hours", "tier", "key_dependencies",
)
LOG_COLUMNS = (
    "test_id", "date", "system", "tier", "rto_target_hours", "actual_restore_hours",
    "rpo_target_hours", "actual_data_age_hours", "result",
)

# From dr/rto-rpo-tiers.md. T1 allows a 1 hour RPO for transactional systems, but 4 hours is the tier maximum.
TIERS: Dict[str, Dict[str, float]] = {
    "T0": {"rto": 2, "rpo": 0.25, "test_days": 183},
    "T1": {"rto": 4, "rpo": 4, "test_days": 183},
    "T2": {"rto": 24, "rpo": 24, "test_days": 366},
    "T3": {"rto": 72, "rpo": 24, "test_days": 366},
    "T4": {"rto": 168, "rpo": 168, "test_days": 366},
}
TIER_ORDER = ["T0", "T1", "T2", "T3", "T4"]
IMPACT_COLUMNS = ("impact_1h", "impact_4h", "impact_24h", "impact_72h")


class InputError(Exception):
    """A file is missing, unreadable or lacks a column."""


@dataclass
class Report:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    process_rows: List[List[str]] = field(default_factory=list)

    def error(self, rule: str, where: str, message: str) -> None:
        self.errors.append(f"{rule} {where}: {message}")

    def warn(self, rule: str, where: str, message: str) -> None:
        self.warnings.append(f"{rule} {where}: {message}")

    def note(self, rule: str, where: str, message: str) -> None:
        self.notes.append(f"{rule} {where}: {message}")


Row = Dict[str, str]


def read_csv(path: Path, required: Sequence[str]) -> List[Row]:
    if not path.is_file():
        raise InputError(f"{path}: file not found")
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            missing = [c for c in required if c not in header]
            if missing:
                raise InputError(f"{path}: missing column(s): {', '.join(missing)}")
            rows = []
            for row in reader:
                clean = {k: (v or "").strip() for k, v in row.items() if k is not None}
                if any(clean.values()):
                    rows.append(clean)
            return rows
    except UnicodeDecodeError as exc:
        raise InputError(f"{path}: not valid UTF-8 ({exc.reason})") from exc


def number(value: str) -> Optional[float]:
    try:
        return float(value)
    except ValueError:
        return None


def tokens(text: str) -> List[str]:
    """Split a semicolon list and drop bracketed qualifiers, so 'Finance system (SaaS)' becomes 'finance system'."""
    out = []
    for part in text.split(";"):
        part = re.sub(r"\([^)]*\)", "", part).strip().lower()
        if part:
            out.append(part)
    return out


def names_match(a: str, b: str) -> bool:
    return a == b or a in b or b in a


# --------------------------------------------------------------------------- #
# BIA checks
# --------------------------------------------------------------------------- #


def check_bia(rows: List[Row], report: Report) -> None:
    seen = set()
    for row in rows:
        pid = row["id"] or "(no id)"
        if pid in seen:
            report.error("DR01", pid, "duplicate id")
        seen.add(pid)
        for column in ("mtpd_hours", "rto_hours", "rpo_hours"):
            if number(row[column]) is None:
                report.error("DR01", pid, f"{column} '{row[column]}' is not a number")
        tier = row["tier"]
        rto, rpo, mtpd = number(row["rto_hours"]), number(row["rpo_hours"]), number(row["mtpd_hours"])
        if tier not in TIERS:
            report.error("DR02", pid, f"tier '{tier}' is not one of {', '.join(TIER_ORDER)}")
        else:
            if rto is not None and rto > TIERS[tier]["rto"]:
                report.error("DR02", pid, f"RTO {rto:g}h is longer than the {tier} maximum of {TIERS[tier]['rto']:g}h")
            if rpo is not None and rpo > TIERS[tier]["rpo"]:
                report.error("DR02", pid, f"RPO {rpo:g}h is longer than the {tier} maximum of {TIERS[tier]['rpo']:g}h")
        if rto is not None and mtpd is not None and rto >= mtpd:
            report.error("DR03", pid, f"RTO {rto:g}h is not shorter than MTPD {mtpd:g}h")
        impacts = [number(row[c]) for c in IMPACT_COLUMNS]
        if all(i is not None for i in impacts):
            if any(b < a for a, b in zip(impacts, impacts[1:])):
                report.warn("DR06", pid, "impact rating falls as the outage gets longer: "
                            + ", ".join(f"{i:g}" for i in impacts))

    unresolved: Dict[str, List[str]] = {}
    for row in rows:
        pid = row["id"]
        own = tokens(row["primary_systems"])
        for dep in tokens(row["key_dependencies"]):
            if any(names_match(dep, o) for o in own):
                continue  # the process's own system
            providers = [
                other for other in rows
                if other["id"] != pid and any(names_match(dep, t) for t in tokens(other["primary_systems"]))
            ]
            if not providers:
                unresolved.setdefault(dep, []).append(pid)
                continue
            my_rto, my_tier = number(row["rto_hours"]), row["tier"]
            # A system's recovery commitment is the strictest RTO among the other processes that rely on it.
            timed = [(number(p["rto_hours"]), p) for p in providers if number(p["rto_hours"]) is not None]
            if my_rto is not None and timed:
                best_rto, best = min(timed, key=lambda item: item[0])
                if best_rto > my_rto:
                    report.error("DR04", pid, f"RTO {my_rto:g}h is shorter than the {best_rto:g}h committed for "
                                 f"{dep} ({best['id']})")
            ranked = [p for p in providers if p["tier"] in TIER_ORDER]
            if my_tier in TIER_ORDER and ranked:
                best = min(ranked, key=lambda p: TIER_ORDER.index(p["tier"]))
                if TIER_ORDER.index(best["tier"]) > TIER_ORDER.index(my_tier):
                    report.error("DR05", pid, f"{my_tier} depends on {dep}, which is only {best['tier']} ({best['id']})")
    for dep, users in sorted(unresolved.items()):
        report.note("DR07", ", ".join(users), f"dependency '{dep}' matches no process on the BIA; "
                    "check it is covered by the dependency map or a supplier arrangement")


# --------------------------------------------------------------------------- #
# Restore log checks
# --------------------------------------------------------------------------- #


def parse_log_date(value: str, where: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise InputError(f"{where}: date '{value}' is not an ISO date (YYYY-MM-DD)") from exc


def check_restore_log(bia: List[Row], log: List[Row], as_of: dt.date, report: Report) -> None:
    for row in log:
        tid = row["test_id"] or "(no id)"
        parse_log_date(row["date"], tid)
        restore, target = number(row["actual_restore_hours"]), number(row["rto_target_hours"])
        age, rpo_target = number(row["actual_data_age_hours"]), number(row["rpo_target_hours"])
        if row["result"].lower() == "pass":
            if restore is not None and target is not None and restore > target:
                report.error("DR10", tid, f"recorded as Pass but the restore took {restore:g}h against an RTO of {target:g}h")
            if age is not None and rpo_target is not None and age > rpo_target:
                report.error("DR10", tid, f"recorded as Pass but the data was {age:g}h old against an RPO of {rpo_target:g}h")

    for process in bia:
        pid = process["id"]
        own = tokens(process["primary_systems"])
        matches = [r for r in log if any(names_match(t, s) for t in tokens(r["system"]) for s in own)]
        tier = process["tier"]
        if not matches:
            report.warn("DR11", pid, f"{process['name']}: no restore test on record")
            report.process_rows.append([pid, process["name"], tier, "none", "", "No test on record"])
            continue
        latest = max(matches, key=lambda r: parse_log_date(r["date"], r["test_id"]))
        tested = parse_log_date(latest["date"], latest["test_id"])
        days = (as_of - tested).days
        status = []
        window = TIERS.get(tier, {}).get("test_days")
        if window is not None and days > window:
            report.warn("DR12", pid, f"{process['name']}: last test {tested.isoformat()} ({days} days ago); "
                        f"{tier} needs one every {int(window)} days")
            status.append("overdue")
        restore, age = number(latest["actual_restore_hours"]), number(latest["actual_data_age_hours"])
        rto, rpo = number(process["rto_hours"]), number(process["rpo_hours"])
        problems = []
        if latest["result"].lower() != "pass":
            problems.append(f"result was {latest['result']}")
        if restore is not None and rto is not None and restore > rto:
            problems.append(f"restore took {restore:g}h against a BIA RTO of {rto:g}h")
        if age is not None and rpo is not None and age > rpo:
            problems.append(f"data was {age:g}h old against a BIA RPO of {rpo:g}h")
        if problems:
            report.warn("DR13", pid, f"{process['name']}: latest test {latest['test_id']} " + "; ".join(problems))
            status.append("target missed")
        report.process_rows.append([pid, process["name"], tier, tested.isoformat(), latest["result"],
                                    ", ".join(status) or "Current and within targets"])


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #


def long_date(d: dt.date) -> str:
    return f"{d.day} {d.strftime('%B %Y')}"


def md_table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> List[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for row in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")
    return out


def finding_rows(report: Report) -> List[List[str]]:
    rows = []
    for level, items in (("error", report.errors), ("warning", report.warnings), ("note", report.notes)):
        for item in items:
            rule, rest = item.split(" ", 1)
            where, message = rest.split(": ", 1)
            rows.append([level, rule, where, message])
    return rows


def render_markdown(report: Report, as_of: dt.date, processes: int, tests: int, note: str = "") -> str:
    lines = ["# DR gap report", "",
             f"Position as at {long_date(as_of)}. Generated by `tools/check_dr.py`; do not edit by hand.", ""]
    if note:
        lines += [note, ""]
    lines += [
        f"Read {processes} BIA processes and {tests} restore tests.",
        f"Result: {len(report.errors)} errors, {len(report.warnings)} warnings, {len(report.notes)} notes.",
        "",
        "## Restore evidence by process",
        "",
    ]
    lines += md_table(["ID", "Process", "Tier", "Latest test", "Result", "Status"], report.process_rows)
    lines += ["", "## Findings", ""]
    rows = finding_rows(report)
    if rows:
        lines += md_table(["Level", "Rule", "Item", "Finding"], rows)
    else:
        lines.append("No findings.")
    lines += [
        "",
        "## What this report cannot tell you",
        "",
        "It checks that the numbers agree with each other and with the tier table. It cannot tell you whether a restore "
        "test was honest, whether the validation was done by a business user, or whether a tier is the right one for the "
        "business. A process is matched to a test by system name, so check the matches that matter.",
        "",
    ]
    return "\n".join(lines)


def render_text(report: Report, as_of: dt.date, processes: int, tests: int) -> str:
    lines = [f"DR check as at {as_of.isoformat()}: {processes} processes, {tests} restore tests"]
    for level, items in (("ERROR", report.errors), ("WARNING", report.warnings), ("NOTE", report.notes)):
        for item in items:
            lines.append(f"{level:<8}{item}")
    lines.append(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s), {len(report.notes)} note(s)")
    return "\n".join(lines) + "\n"


def run(bia_path: Path, log_path: Optional[Path], as_of: dt.date) -> Tuple[Report, int, int]:
    report = Report()
    bia = read_csv(bia_path, BIA_COLUMNS)
    check_bia(bia, report)
    log: List[Row] = []
    if log_path is not None:
        log = read_csv(log_path, LOG_COLUMNS)
        check_restore_log(bia, log, as_of, report)
    return report, len(bia), len(log)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check a BIA and a restore test log for consistency.")
    parser.add_argument("--bia", type=Path, default=EXAMPLE_BIA, help="BIA CSV (default: the worked example)")
    parser.add_argument("--restore-log", type=Path, default=None,
                        help="restore test log CSV (default for the worked example: its example log)")
    parser.add_argument("--as-of", type=dt.date.fromisoformat, default=None, help="date to report as at (default: today)")
    parser.add_argument("--markdown", action="store_true", help="print a Markdown report instead of plain text")
    parser.add_argument("--output", type=Path, help="write the Markdown report to this file")
    parser.add_argument("--check", type=Path,
                        help="fail if this file differs from the report generated for the worked example")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args(argv)

    example_note = ("Example run against the fictional Fernhill Freight BIA and restore log in `dr/`. "
                    "The date is fixed so that the output is stable; run the tool with your own files and today's date.")
    try:
        if args.check:
            report, n_bia, n_log = run(EXAMPLE_BIA, EXAMPLE_LOG, EXAMPLE_AS_OF)
            expected = render_markdown(report, EXAMPLE_AS_OF, n_bia, n_log, example_note)
            current = args.check.read_text(encoding="utf-8") if args.check.is_file() else None
            if current != expected:
                print(f"STALE   {args.check} is out of date; run: python tools/check_dr.py --markdown "
                      f"--as-of {EXAMPLE_AS_OF.isoformat()} --output {args.check}", file=sys.stderr)
                return 1
            print(f"OK {args.check} matches the worked example")
            return 0

        as_of = args.as_of or dt.date.today()
        log_path = args.restore_log
        using_example = args.bia.resolve() == EXAMPLE_BIA.resolve()
        if log_path is None and using_example:
            log_path = EXAMPLE_LOG
        report, n_bia, n_log = run(args.bia, log_path, as_of)
        note = example_note if (using_example and log_path is not None and log_path.resolve() == EXAMPLE_LOG.resolve()
                                and as_of == EXAMPLE_AS_OF) else ""
    except InputError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(render_markdown(report, as_of, n_bia, n_log, note))
        print(f"Wrote {args.output}")
    elif args.markdown:
        sys.stdout.write(render_markdown(report, as_of, n_bia, n_log, note))
    else:
        sys.stdout.write(render_text(report, as_of, n_bia, n_log))

    if report.errors or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
