#!/usr/bin/env python3
"""Lint the incident response playbooks in this repository.

Standard library only. Checks every playbook in ``playbooks/`` (README.md
excluded) for:

* the required sections, in the required order, each with some content;
* a one-page quick-reference checklist (checkbox items, not too long);
* leftover placeholders marked TODO, FIXME or TBD;
* broken internal links and broken heading anchors;
* house style: no em-dashes.

It can also check internal links across every Markdown file in the
repository (``--all-links``) and prints a summary table.

Exit status: 0 when there are no errors, 1 when there are errors, 2 on
usage problems. Warnings never change the exit status unless
``--strict-review`` is given.

Usage::

    python tools/check_playbooks.py
    python tools/check_playbooks.py --all-links
    python tools/check_playbooks.py --root path/to/repo --markdown
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

# Canonical section names, in the order they must appear.
REQUIRED_SECTIONS: Tuple[str, ...] = (
    "purpose",
    "triggers",
    "severity matrix",
    "roles",
    "first 15 minutes",
    "containment",
    "eradication",
    "recovery",
    "evidence handling",
    "communications",
    "regulatory and contractual notifications",
    "decision points",
    "post-incident actions",
    "quick-reference checklist",
)

# Accepted alternative spellings, mapped to the canonical name.
SECTION_ALIASES: Dict[str, str] = {
    "quick reference checklist": "quick-reference checklist",
    "quick-reference": "quick-reference checklist",
    "post incident actions": "post-incident actions",
    "regulatory and contractual notification": "regulatory and contractual notifications",
    "first fifteen minutes": "first 15 minutes",
}

REQUIRED_METADATA: Tuple[str, ...] = ("Version", "Owner", "Last reviewed")
PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|TBD)\b")
FIELD_RE = re.compile(r"\{\{[^}]*\}\}")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
LINK_RE = re.compile(r"!?\[(?:[^\]\\]|\\.)*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+\S")
EM_DASH = chr(0x2014)  # written this way so the source itself contains no em-dash

MIN_CHECKLIST_ITEMS = 8
MAX_CHECKLIST_LINES = 45
DEFAULT_REVIEW_DAYS = 366

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".github"}


@dataclass
class Issue:
    """A single finding. ``level`` is ``error`` or ``warning``."""

    level: str
    path: Path
    line: int
    message: str

    def format(self, root: Path) -> str:
        try:
            shown = self.path.relative_to(root)
        except ValueError:
            shown = self.path
        where = f"{shown}:{self.line}" if self.line else str(shown)
        return f"{self.level.upper():7} {where}: {self.message}"


@dataclass
class Heading:
    level: int
    text: str
    line: int


@dataclass
class PlaybookReport:
    path: Path
    sections_found: int = 0
    sections_required: int = len(REQUIRED_SECTIONS)
    checklist_items: int = 0
    lines: int = 0
    links_checked: int = 0
    broken_links: int = 0
    todos: int = 0
    fields: int = 0
    issues: List[Issue] = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(1 for i in self.issues if i.level == "error")

    @property
    def warnings(self) -> int:
        return sum(1 for i in self.issues if i.level == "warning")

    @property
    def status(self) -> str:
        if self.errors:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "OK"


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def iter_unfenced(lines: Sequence[str]) -> Iterable[Tuple[int, str]]:
    """Yield (1-based line number, text) for lines outside code fences."""
    fence: Optional[str] = None
    for number, text in enumerate(lines, start=1):
        match = FENCE_RE.match(text)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield number, text


def parse_headings(lines: Sequence[str]) -> List[Heading]:
    headings: List[Heading] = []
    for number, text in iter_unfenced(lines):
        match = HEADING_RE.match(text)
        if match:
            headings.append(Heading(len(match.group(1)), match.group(2), number))
    return headings


def github_slug(text: str) -> str:
    """Approximate GitHub's heading anchor generation."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links keep their text
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def heading_slugs(headings: Sequence[Heading]) -> set:
    """All anchors a page offers, with GitHub's -1, -2 suffixes for repeats."""
    seen: Dict[str, int] = {}
    slugs = set()
    for heading in headings:
        base = github_slug(heading.text)
        count = seen.get(base, 0)
        slugs.add(base if count == 0 else f"{base}-{count}")
        seen[base] = count + 1
    return slugs


def normalise_section(title: str) -> str:
    """Lower-case a section heading and drop any leading number such as '5.'."""
    title = re.sub(r"^\s*\d+[.)]?\s*", "", title)
    title = title.strip().lower()
    return SECTION_ALIASES.get(title, title)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_sections(path: Path, lines: Sequence[str], headings: Sequence[Heading],
                   report: PlaybookReport) -> None:
    h2 = [h for h in headings if h.level == 2]
    names = [(normalise_section(h.text), h) for h in h2]

    found: Dict[str, Heading] = {}
    for name, heading in names:
        if name in REQUIRED_SECTIONS:
            if name in found:
                report.issues.append(Issue(
                    "error", path, heading.line,
                    f"duplicate section '{name}' (first at line {found[name].line})"))
            else:
                found[name] = heading

    report.sections_found = len(found)
    for required in REQUIRED_SECTIONS:
        if required not in found:
            report.issues.append(Issue("error", path, 0, f"missing required section '{required}'"))

    # Order check, using only the sections that are present.
    present_order = [name for name, _ in names if name in found]
    expected_order = [name for name in REQUIRED_SECTIONS if name in found]
    deduped: List[str] = []
    for name in present_order:
        if name not in deduped:
            deduped.append(name)
    if deduped != expected_order:
        report.issues.append(Issue(
            "error", path, 0,
            "required sections are out of order (expected: " + ", ".join(expected_order) + ")"))

    # Each required section needs real content before the next H2.
    h2_lines = [h.line for h in h2] + [len(lines) + 1]
    for name, heading in found.items():
        index = h2_lines.index(heading.line)
        end = h2_lines[index + 1]
        body = [t for t in lines[heading.line:end - 1] if t.strip()]
        if not body:
            report.issues.append(Issue("error", path, heading.line, f"section '{name}' is empty"))


def check_title_and_metadata(path: Path, lines: Sequence[str], headings: Sequence[Heading],
                             report: PlaybookReport, strict_review: bool,
                             today: dt.date, review_days: int) -> None:
    h1 = [h for h in headings if h.level == 1]
    if not h1:
        report.issues.append(Issue("error", path, 0, "missing H1 title"))
    else:
        if len(h1) > 1:
            report.issues.append(Issue("error", path, h1[1].line, "more than one H1 heading"))
        if not h1[0].text.lower().startswith("playbook:"):
            report.issues.append(Issue(
                "warning", path, h1[0].line, "H1 title should start with 'Playbook:'"))

    head = "\n".join(lines[:25])
    for key in REQUIRED_METADATA:
        if not re.search(rf"^\|\s*{re.escape(key)}\s*\|", head, flags=re.M | re.I):
            report.issues.append(Issue("error", path, 0, f"metadata table is missing '{key}'"))

    match = re.search(r"^\|\s*Last reviewed\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", head,
                      flags=re.M | re.I)
    if match:
        try:
            reviewed = dt.date.fromisoformat(match.group(1))
        except ValueError:
            report.issues.append(Issue("error", path, 0, "'Last reviewed' is not a valid date"))
        else:
            age = (today - reviewed).days
            if age < 0:
                report.issues.append(Issue("error", path, 0, "'Last reviewed' date is in the future"))
            elif age > review_days:
                level = "error" if strict_review else "warning"
                report.issues.append(Issue(
                    level, path, 0, f"last reviewed {age} days ago (limit {review_days})"))
    elif re.search(r"^\|\s*Last reviewed\s*\|", head, flags=re.M | re.I):
        report.issues.append(Issue(
            "error", path, 0, "'Last reviewed' must be an ISO date (YYYY-MM-DD)"))


def check_quick_reference(path: Path, lines: Sequence[str], headings: Sequence[Heading],
                          report: PlaybookReport) -> None:
    h2 = [h for h in headings if h.level == 2]
    for index, heading in enumerate(h2):
        if normalise_section(heading.text) != "quick-reference checklist":
            continue
        end = h2[index + 1].line if index + 1 < len(h2) else len(lines) + 1
        body = lines[heading.line:end - 1]
        items = [t for t in body if CHECKBOX_RE.match(t)]
        report.checklist_items = len(items)
        if len(items) < MIN_CHECKLIST_ITEMS:
            report.issues.append(Issue(
                "error", path, heading.line,
                f"quick-reference checklist has {len(items)} checkbox items "
                f"(minimum {MIN_CHECKLIST_ITEMS})"))
        length = len([t for t in body if t.strip()])
        if length > MAX_CHECKLIST_LINES:
            report.issues.append(Issue(
                "error", path, heading.line,
                f"quick-reference checklist is {length} lines, which will not fit one page "
                f"(maximum {MAX_CHECKLIST_LINES})"))
        return


def check_text_rules(path: Path, lines: Sequence[str], report: PlaybookReport) -> None:
    for number, text in enumerate(lines, start=1):
        for match in PLACEHOLDER_RE.finditer(text):
            report.todos += 1
            report.issues.append(Issue(
                "error", path, number, f"leftover placeholder '{match.group(1)}'"))
        if EM_DASH in text:
            report.issues.append(Issue(
                "error", path, number, "em-dash found (house style uses commas, colons or hyphens)"))
        report.fields += len(FIELD_RE.findall(text))


def extract_links(lines: Sequence[str]) -> List[Tuple[int, str]]:
    links: List[Tuple[int, str]] = []
    for number, text in iter_unfenced(lines):
        cleaned = INLINE_CODE_RE.sub("", text)
        for match in LINK_RE.finditer(cleaned):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            links.append((number, target))
    return links


def is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target))


class AnchorCache:
    """Caches the set of heading anchors for each Markdown file."""

    def __init__(self) -> None:
        self._cache: Dict[Path, set] = {}

    def slugs(self, path: Path) -> set:
        resolved = path.resolve()
        if resolved not in self._cache:
            try:
                headings = parse_headings(read_lines(resolved))
            except (OSError, UnicodeDecodeError):
                headings = []
            self._cache[resolved] = heading_slugs(headings)
        return self._cache[resolved]


def check_links(path: Path, lines: Sequence[str], anchors: AnchorCache,
                report: Optional[PlaybookReport] = None) -> List[Issue]:
    issues: List[Issue] = []
    checked = 0
    for number, target in extract_links(lines):
        if not target or is_external(target):
            continue
        checked += 1
        raw_path, _, fragment = target.partition("#")
        raw_path = urllib.parse.unquote(raw_path)
        fragment = urllib.parse.unquote(fragment)

        if raw_path == "":
            destination = path
        else:
            destination = (path.parent / raw_path)
            if not destination.exists():
                issues.append(Issue("error", path, number, f"broken link: '{target}' does not exist"))
                continue
        if fragment and destination.is_file() and destination.suffix.lower() == ".md":
            if fragment.lower() not in anchors.slugs(destination):
                issues.append(Issue(
                    "error", path, number, f"broken anchor: '#{fragment}' not found in "
                    f"{destination.name}"))
    if report is not None:
        report.links_checked = checked
        report.broken_links = len(issues)
    return issues


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def find_playbooks(root: Path) -> List[Path]:
    folder = root / "playbooks"
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if p.name.lower() != "readme.md")


def find_markdown(root: Path) -> List[Path]:
    found: List[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        found.append(path)
    return sorted(found)


def lint_playbook(path: Path, anchors: AnchorCache, strict_review: bool = False,
                  today: Optional[dt.date] = None,
                  review_days: int = DEFAULT_REVIEW_DAYS) -> PlaybookReport:
    today = today or dt.date.today()
    report = PlaybookReport(path=path)
    try:
        lines = read_lines(path)
    except (OSError, UnicodeDecodeError) as exc:
        report.issues.append(Issue("error", path, 0, f"cannot read file: {exc}"))
        return report
    report.lines = len(lines)
    headings = parse_headings(lines)

    check_title_and_metadata(path, lines, headings, report, strict_review, today, review_days)
    check_sections(path, lines, headings, report)
    check_quick_reference(path, lines, headings, report)
    check_text_rules(path, lines, report)
    report.issues.extend(check_links(path, lines, anchors, report))
    return report


def lint_all_links(root: Path, anchors: AnchorCache,
                   skip: Iterable[Path] = ()) -> Tuple[int, List[Issue]]:
    skip_set = {p.resolve() for p in skip}
    issues: List[Issue] = []
    files = 0
    for path in find_markdown(root):
        if path.resolve() in skip_set:
            continue
        files += 1
        issues.extend(check_links(path, read_lines(path), anchors))
    return files, issues


def render_table(reports: Sequence[PlaybookReport], root: Path, markdown: bool = False) -> str:
    headers = ["Playbook", "Sections", "Checklist", "Lines", "Links", "TODOs", "Fields", "Err", "Warn", "Status"]
    rows: List[List[str]] = []
    for r in reports:
        try:
            name = str(r.path.relative_to(root))
        except ValueError:
            name = str(r.path)
        rows.append([
            name,
            f"{r.sections_found}/{r.sections_required}",
            str(r.checklist_items),
            str(r.lines),
            f"{r.links_checked - r.broken_links}/{r.links_checked}",
            str(r.todos),
            str(r.fields),
            str(r.errors),
            str(r.warnings),
            r.status,
        ])
    if markdown:
        out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
        out.extend("| " + " | ".join(row) + " |" for row in rows)
        return "\n".join(out)

    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
              for i in range(len(headers))]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells: Sequence[str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    out = [line, fmt(headers), line]
    out.extend(fmt(row) for row in rows)
    out.append(line)
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lint incident response playbooks for structure, placeholders and links.")
    parser.add_argument("--root", type=Path, default=None,
                        help="repository root (default: the parent of the tools/ folder)")
    parser.add_argument("--all-links", action="store_true",
                        help="also check internal links and anchors in every Markdown file")
    parser.add_argument("--strict-review", action="store_true",
                        help="treat a stale 'Last reviewed' date as an error, not a warning")
    parser.add_argument("--review-days", type=int, default=DEFAULT_REVIEW_DAYS,
                        help=f"maximum age of 'Last reviewed' in days (default {DEFAULT_REVIEW_DAYS})")
    parser.add_argument("--markdown", action="store_true",
                        help="print the summary as a Markdown table")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    root = (args.root or Path(__file__).resolve().parent.parent).resolve()
    if not root.is_dir():
        print(f"error: root folder not found: {root}", file=sys.stderr)
        return 2

    playbooks = find_playbooks(root)
    if not playbooks:
        print(f"error: no playbooks found in {root / 'playbooks'}", file=sys.stderr)
        return 2

    anchors = AnchorCache()
    reports = [lint_playbook(p, anchors, args.strict_review, review_days=args.review_days)
               for p in playbooks]

    print(render_table(reports, root, markdown=args.markdown))
    print()

    extra_issues: List[Issue] = []
    if args.all_links:
        files, extra_issues = lint_all_links(root, anchors, skip=playbooks)
        print(f"Link check of {files} other Markdown files: "
              f"{len(extra_issues)} broken link(s) or anchor(s)")
        print()

    all_issues = [i for r in reports for i in r.issues] + extra_issues
    for issue in all_issues:
        print(issue.format(root))

    errors = sum(1 for i in all_issues if i.level == "error")
    warnings = sum(1 for i in all_issues if i.level == "warning")
    total_fields = sum(r.fields for r in reports)
    print()
    print(f"{len(reports)} playbook(s) checked: {errors} error(s), {warnings} warning(s). "
          f"{total_fields} {{{{field}}}} placeholder(s) left for you to complete.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
