"""Tests for tools/check_playbooks.py and for the DR data files.

Run from the repository root with::

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import contextlib
import csv
import datetime as dt
import io
import re
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import check_playbooks as cp  # noqa: E402  (import after sys.path change)

TODAY = dt.date(2026, 11, 4)
SECTION_TITLES = [
    "Purpose", "Triggers", "Severity matrix", "Roles", "First 15 minutes",
    "Containment", "Eradication", "Recovery", "Evidence handling", "Communications",
    "Regulatory and contractual notifications", "Decision points",
    "Post-incident actions", "Quick-reference checklist",
]


def build_playbook(skip=(), reorder=False, extra="", empty=(), checklist_items=9,
                   reviewed="2026-10-01", numbered=True, checklist_pad=0):
    """Return the text of a small, valid playbook, optionally with one defect."""
    titles = [t for t in SECTION_TITLES if t not in skip]
    if reorder:
        titles[1], titles[2] = titles[2], titles[1]
    out = [
        "# Playbook: Test",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Version | 1.0 |",
        "| Owner | IT Manager |",
        f"| Last reviewed | {reviewed} |",
        "",
    ]
    for number, title in enumerate(titles, start=1):
        heading = f"{number}. {title}" if numbered else title
        out.append(f"## {heading}")
        out.append("")
        if title in empty:
            continue
        if title == "Quick-reference checklist":
            out.extend(f"- [ ] Step {i}" for i in range(checklist_items))
            out.extend(f"Note {i}" for i in range(checklist_pad))
        else:
            out.append(f"Content for {title}.")
        out.append("")
    out.append(extra)
    return "\n".join(out) + "\n"


class TempRepo:
    """A throwaway repository with a playbooks folder."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "playbooks").mkdir()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def cleanup(self):
        self._tmp.cleanup()


class LintCase(unittest.TestCase):
    def setUp(self):
        self.repo = TempRepo()
        self.addCleanup(self.repo.cleanup)

    def lint(self, text, name="p.md", **kwargs):
        path = self.repo.write(f"playbooks/{name}", text)
        return cp.lint_playbook(path, cp.AnchorCache(), today=TODAY, **kwargs)

    def messages(self, report, level="error"):
        return [i.message for i in report.issues if i.level == level]


class SlugAndHeadingTests(unittest.TestCase):
    def test_github_slug_basic(self):
        self.assertEqual(cp.github_slug("5. First 15 minutes"), "5-first-15-minutes")
        self.assertEqual(cp.github_slug("Risk assessment: ICO and individuals"),
                         "risk-assessment-ico-and-individuals")
        self.assertEqual(cp.github_slug("Post-incident actions"), "post-incident-actions")

    def test_slug_keeps_link_text_and_drops_punctuation(self):
        self.assertEqual(cp.github_slug("Use [the guide](x.md) (v2)?"), "use-the-guide-v2")

    def test_duplicate_headings_get_suffixes(self):
        headings = [cp.Heading(2, "Notes", 1), cp.Heading(2, "Notes", 5)]
        self.assertEqual(cp.heading_slugs(headings), {"notes", "notes-1"})

    def test_headings_inside_code_fences_are_ignored(self):
        lines = ["# Title", "```powershell", "# a comment, not a heading", "```", "## Real"]
        self.assertEqual([h.text for h in cp.parse_headings(lines)], ["Title", "Real"])

    def test_normalise_section_strips_numbers_and_aliases(self):
        self.assertEqual(cp.normalise_section("14. Quick reference checklist"),
                         "quick-reference checklist")
        self.assertEqual(cp.normalise_section("3) Severity Matrix"), "severity matrix")


class StructureTests(LintCase):
    def test_valid_playbook_passes(self):
        report = self.lint(build_playbook())
        self.assertEqual(report.errors, 0, self.messages(report))
        self.assertEqual(report.sections_found, 14)
        self.assertEqual(report.status, "OK")

    def test_unnumbered_headings_are_accepted(self):
        report = self.lint(build_playbook(numbered=False))
        self.assertEqual(report.errors, 0, self.messages(report))

    def test_missing_section_is_an_error(self):
        report = self.lint(build_playbook(skip=("Eradication",)))
        self.assertIn("missing required section 'eradication'", self.messages(report))
        self.assertEqual(report.sections_found, 13)
        self.assertEqual(report.status, "FAIL")

    def test_out_of_order_sections_are_an_error(self):
        report = self.lint(build_playbook(reorder=True))
        self.assertTrue(any("out of order" in m for m in self.messages(report)))

    def test_empty_section_is_an_error(self):
        report = self.lint(build_playbook(empty=("Containment",)))
        self.assertIn("section 'containment' is empty", self.messages(report))

    def test_duplicate_section_is_an_error(self):
        report = self.lint(build_playbook(extra="## Containment\n\nAgain.\n"))
        self.assertTrue(any("duplicate section 'containment'" in m for m in self.messages(report)))

    def test_missing_metadata_is_an_error(self):
        text = build_playbook().replace("| Owner | IT Manager |\n", "")
        report = self.lint(text)
        self.assertIn("metadata table is missing 'Owner'", self.messages(report))

    def test_title_must_start_with_playbook(self):
        report = self.lint(build_playbook().replace("# Playbook: Test", "# Something else"))
        self.assertTrue(any("start with 'Playbook:'" in m for m in self.messages(report, "warning")))


class ChecklistTests(LintCase):
    def test_short_checklist_is_an_error(self):
        report = self.lint(build_playbook(checklist_items=3))
        self.assertTrue(any("minimum 8" in m for m in self.messages(report)))

    def test_checklist_too_long_for_one_page(self):
        report = self.lint(build_playbook(checklist_items=10, checklist_pad=60))
        self.assertTrue(any("will not fit one page" in m for m in self.messages(report)))

    def test_checklist_items_are_counted(self):
        report = self.lint(build_playbook(checklist_items=12))
        self.assertEqual(report.checklist_items, 12)


class TextRuleTests(LintCase):
    def test_todo_marker_is_an_error(self):
        report = self.lint(build_playbook(extra="TODO: finish this section"))
        self.assertEqual(report.todos, 1)
        self.assertTrue(any("placeholder 'TODO'" in m for m in self.messages(report)))

    def test_fixme_and_tbd_are_errors_inside_code_blocks_too(self):
        report = self.lint(build_playbook(extra="```\nFIXME later\nTBD\n```"))
        self.assertEqual(report.todos, 2)

    def test_embedded_or_lowercase_words_are_not_flagged(self):
        report = self.lint(build_playbook(extra="Mastodon and todolist are fine."))
        self.assertEqual(report.todos, 0)

    def test_em_dash_is_an_error(self):
        report = self.lint(build_playbook(extra="Isolate " + chr(0x2014) + " do not wipe."))
        self.assertTrue(any("em-dash" in m for m in self.messages(report)))

    def test_template_fields_are_counted_not_errors(self):
        report = self.lint(build_playbook(extra="Call {{name}} on {{phone}}."))
        self.assertEqual(report.fields, 2)
        self.assertEqual(report.errors, 0, self.messages(report))


class ReviewDateTests(LintCase):
    def test_stale_review_is_a_warning_by_default(self):
        report = self.lint(build_playbook(reviewed="2024-01-01"))
        self.assertEqual(report.errors, 0)
        self.assertEqual(report.warnings, 1)
        self.assertEqual(report.status, "WARN")

    def test_stale_review_is_an_error_when_strict(self):
        report = self.lint(build_playbook(reviewed="2024-01-01"), strict_review=True)
        self.assertEqual(report.errors, 1)

    def test_future_date_is_an_error(self):
        report = self.lint(build_playbook(reviewed="2030-01-01"))
        self.assertIn("'Last reviewed' date is in the future", self.messages(report))

    def test_invalid_date_is_an_error(self):
        report = self.lint(build_playbook(reviewed="2026-13-45"))
        self.assertIn("'Last reviewed' is not a valid date", self.messages(report))

    def test_non_iso_date_is_an_error(self):
        report = self.lint(build_playbook(reviewed="4 November 2026"))
        self.assertIn("'Last reviewed' must be an ISO date (YYYY-MM-DD)", self.messages(report))


class LinkTests(LintCase):
    def test_valid_relative_link_and_anchor(self):
        self.repo.write("docs/other.md", "# Other\n\n## Useful part\n")
        text = build_playbook(extra="See [other](../docs/other.md#useful-part) and [self](#purpose).")
        report = self.lint(text.replace("## 1. Purpose", "## Purpose", 1))
        self.assertEqual(report.errors, 0, self.messages(report))
        self.assertEqual(report.links_checked, 2)

    def test_broken_file_link(self):
        report = self.lint(build_playbook(extra="See [missing](../docs/nothing.md)."))
        self.assertTrue(any("broken link" in m for m in self.messages(report)))
        self.assertEqual(report.broken_links, 1)

    def test_broken_anchor_in_other_file(self):
        self.repo.write("docs/other.md", "# Other\n\n## Useful part\n")
        report = self.lint(build_playbook(extra="See [x](../docs/other.md#no-such-heading)."))
        self.assertTrue(any("broken anchor" in m for m in self.messages(report)))

    def test_broken_anchor_in_same_file(self):
        report = self.lint(build_playbook(extra="Jump to [nowhere](#nowhere)."))
        self.assertTrue(any("broken anchor" in m for m in self.messages(report)))

    def test_numbered_heading_anchor_matches(self):
        report = self.lint(build_playbook(extra="See [first](#5-first-15-minutes)."))
        self.assertEqual(report.errors, 0, self.messages(report))

    def test_external_links_and_code_are_ignored(self):
        extra = ("[web](https://example.org/x) [mail](mailto:a@example.org)\n"
                 "Inline `[not](a-link.md)` code.\n"
                 "```\n[also not](nope.md)\n```")
        report = self.lint(build_playbook(extra=extra))
        self.assertEqual(report.errors, 0, self.messages(report))
        self.assertEqual(report.links_checked, 0)

    def test_link_with_title_and_images(self):
        self.repo.write("docs/pic.png", "x")
        extra = '[a](../docs/pic.png "title") ![img](../docs/pic.png)'
        report = self.lint(build_playbook(extra=extra))
        self.assertEqual(report.errors, 0, self.messages(report))
        self.assertEqual(report.links_checked, 2)

    def test_all_links_mode_checks_other_files(self):
        self.repo.write("README.md", "[bad](docs/missing.md)\n")
        self.repo.write("docs/ok.md", "[good](../README.md)\n")
        files, issues = cp.lint_all_links(self.repo.root, cp.AnchorCache())
        self.assertEqual(files, 2)
        self.assertEqual(len(issues), 1)
        self.assertIn("docs/missing.md", issues[0].message)


class CommandLineTests(unittest.TestCase):
    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cp.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_exit_zero_and_table_for_a_clean_repo(self):
        repo = TempRepo()
        self.addCleanup(repo.cleanup)
        repo.write("playbooks/a.md", build_playbook(reviewed=dt.date.today().isoformat()))
        code, out, _ = self.run_main("--root", str(repo.root))
        self.assertEqual(code, 0, out)
        self.assertIn("playbooks/a.md", out)
        self.assertIn("14/14", out)
        self.assertIn("0 error(s)", out)

    def test_exit_one_when_there_are_errors(self):
        repo = TempRepo()
        self.addCleanup(repo.cleanup)
        repo.write("playbooks/a.md", build_playbook(skip=("Recovery",)))
        code, out, _ = self.run_main("--root", str(repo.root))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)

    def test_readme_in_playbooks_folder_is_not_linted(self):
        repo = TempRepo()
        self.addCleanup(repo.cleanup)
        repo.write("playbooks/README.md", "# Index only\n")
        repo.write("playbooks/a.md", build_playbook(reviewed=dt.date.today().isoformat()))
        self.assertEqual([p.name for p in cp.find_playbooks(repo.root)], ["a.md"])

    def test_exit_two_without_playbooks_or_root(self):
        repo = TempRepo()
        self.addCleanup(repo.cleanup)
        code, _, err = self.run_main("--root", str(repo.root))
        self.assertEqual(code, 2)
        self.assertIn("no playbooks found", err)
        code, _, err = self.run_main("--root", str(repo.root / "does-not-exist"))
        self.assertEqual(code, 2)

    def test_markdown_table_option(self):
        repo = TempRepo()
        self.addCleanup(repo.cleanup)
        repo.write("playbooks/a.md", build_playbook(reviewed=dt.date.today().isoformat()))
        code, out, _ = self.run_main("--root", str(repo.root), "--markdown")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("| Playbook |"))


class RealRepositoryTests(unittest.TestCase):
    """The shipped playbooks must satisfy their own linter."""

    def test_six_playbooks_exist(self):
        names = sorted(p.name for p in cp.find_playbooks(REPO))
        self.assertEqual(names, [
            "ddos-service-outage.md", "lost-or-stolen-device.md",
            "m365-account-compromise-bec.md", "personal-data-breach.md",
            "ransomware.md", "saas-supplier-outage.md",
        ])

    def test_every_shipped_playbook_passes(self):
        anchors = cp.AnchorCache()
        for path in cp.find_playbooks(REPO):
            report = cp.lint_playbook(path, anchors, today=TODAY)
            self.assertEqual(report.errors, 0,
                             f"{path.name}: {[i.message for i in report.issues]}")
            self.assertEqual(report.sections_found, len(cp.REQUIRED_SECTIONS), path.name)
            self.assertEqual(report.todos, 0, path.name)
            self.assertEqual(report.fields, 0, path.name)

    def test_internal_links_across_the_whole_repository(self):
        files, issues = cp.lint_all_links(REPO, cp.AnchorCache())
        self.assertGreater(files, 20)
        self.assertEqual(issues, [], [i.format(REPO) for i in issues])

    def test_command_line_run_on_the_repository_exits_zero(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cp.main(["--all-links"])
        self.assertEqual(code, 0, out.getvalue())

    def test_no_em_dashes_anywhere_in_text_files(self):
        offenders = []
        for path in REPO.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix in {".png", ".pyc"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            # The linter and its tests build the character with chr(0x2014), so they are clean.
            if chr(0x2014) in text:
                offenders.append(str(path.relative_to(REPO)))
        self.assertEqual(offenders, [])


# ---------------------------------------------------------------------------
# DR data files
# ---------------------------------------------------------------------------

def parse_hours(text):
    """First duration in a cell such as '4 hours (1 hour for ...)', in hours."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|h|days?|d)\b", text)
    if not match:
        raise ValueError(f"no duration in {text!r}")
    value, unit = float(match.group(1)), match.group(2)
    scale = {"m": 1 / 60, "h": 1, "d": 24}[unit[0]]
    return value * scale


def tier_limits():
    """Read the maximum RTO and RPO per tier from dr/rto-rpo-tiers.md."""
    limits = {}
    for line in (REPO / "dr" / "rto-rpo-tiers.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"T[0-4]", cells[0]) and len(cells) >= 6:
            limits[cells[0]] = (parse_hours(cells[3]), parse_hours(cells[4]))
    return limits


def read_csv(relative):
    with open(REPO / relative, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class DrDataTests(unittest.TestCase):
    def test_tier_table_has_five_tiers_in_increasing_rto(self):
        limits = tier_limits()
        self.assertEqual(sorted(limits), ["T0", "T1", "T2", "T3", "T4"])
        rtos = [limits[t][0] for t in sorted(limits)]
        self.assertEqual(rtos, sorted(rtos))
        self.assertEqual(limits["T0"], (2.0, 0.25))
        self.assertEqual(limits["T4"][0], 168.0)

    def test_template_and_example_share_the_same_header(self):
        with open(REPO / "dr/bia-template.csv", newline="", encoding="utf-8") as a, \
                open(REPO / "dr/bia-worked-example.csv", newline="", encoding="utf-8") as b:
            self.assertEqual(next(csv.reader(a)), next(csv.reader(b)))

    def test_template_row_is_all_placeholders(self):
        rows = read_csv("dr/bia-template.csv")
        self.assertEqual(len(rows), 1)
        for key, value in rows[0].items():
            if key != "id":
                self.assertTrue(value.startswith("{{") and value.endswith("}}"), (key, value))

    def test_worked_example_is_internally_consistent(self):
        limits = tier_limits()
        rows = read_csv("dr/bia-worked-example.csv")
        self.assertGreaterEqual(len(rows), 10)
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "duplicate process ids")
        for r in rows:
            label = r["id"]
            self.assertIn(r["tier"], limits, label)
            mtpd, rto, rpo = (float(r[k]) for k in ("mtpd_hours", "rto_hours", "rpo_hours"))
            self.assertLessEqual(rto, mtpd, f"{label}: RTO must not exceed MTPD")
            self.assertLessEqual(rto, limits[r["tier"]][0], f"{label}: RTO above tier maximum")
            self.assertLessEqual(rpo, limits[r["tier"]][1], f"{label}: RPO above tier maximum")
            impacts = [int(r[k]) for k in ("impact_1h", "impact_4h", "impact_24h", "impact_72h")]
            self.assertTrue(all(1 <= i <= 5 for i in impacts), label)
            self.assertEqual(impacts, sorted(impacts), f"{label}: impact must not fall over time")
            for key in ("owner_role", "workaround", "key_dependencies"):
                self.assertTrue(r[key].strip(), f"{label}: {key} is empty")
            self.assertFalse(re.search(r"\{\{", "".join(r.values())), label)

    def test_every_worked_example_dependency_tier_is_not_slower_than_dependent(self):
        # Identity and network (T0) must be at least as fast as everything that needs them.
        rows = {r["id"]: r for r in read_csv("dr/bia-worked-example.csv")}
        t0_rto = min(float(r["rto_hours"]) for r in rows.values() if r["tier"] == "T0")
        for r in rows.values():
            if r["tier"] != "T0":
                self.assertGreaterEqual(float(r["rto_hours"]), t0_rto, r["id"])

    def test_worked_example_summary_table_matches_the_csv(self):
        text = (REPO / "dr/bia-worked-example.md").read_text(encoding="utf-8")
        rows = {r["id"]: r for r in read_csv("dr/bia-worked-example.csv")}
        found = 0
        for line in text.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 8 and re.fullmatch(r"BP\d+", cells[0]):
                found += 1
                row = rows[cells[0]]
                self.assertEqual(cells[1], row["name"])
                self.assertEqual(cells[2], row["impact_4h"], cells[0])
                self.assertEqual(cells[3], row["impact_24h"], cells[0])
                self.assertEqual(cells[7], row["tier"], cells[0])
                self.assertAlmostEqual(parse_hours(cells[5]), float(row["rto_hours"]), msg=cells[0])
        self.assertEqual(found, len(rows))

    def test_restore_test_log_csv_is_well_formed(self):
        with open(REPO / "dr/backup-restore-test-log.csv", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            rows = list(reader)
        documented = re.findall(r"^\| (\w+) \|", (REPO / "dr/backup-restore-test-log.md")
                                .read_text(encoding="utf-8").split("## Log fields")[1], flags=re.M)
        documented = [d for d in documented if d not in {"Field"}]
        self.assertEqual(header, documented)
        for row in rows:
            self.assertEqual(len(row), len(header))

    def test_mermaid_block_matches_the_source_file(self):
        source = (REPO / "dr/dependency-map.mmd").read_text(encoding="utf-8")
        page = (REPO / "dr/dependency-map.md").read_text(encoding="utf-8")
        match = re.search(r"```mermaid\n(.*?)```", page, flags=re.S)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1).strip(), source.strip())

    def test_dependency_map_image_exists_and_is_a_png(self):
        data = (REPO / "docs/dependency-map.png").read_bytes()
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertGreater(len(data), 10_000)


if __name__ == "__main__":
    unittest.main()
