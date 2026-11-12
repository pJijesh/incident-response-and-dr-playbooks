"""Tests for tools/check_dr.py.

Run from the repository root with:

    python -m unittest discover -s tests -v
"""

import datetime as dt
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import check_dr as dr  # noqa: E402

D = dt.date
AS_OF = D(2026, 11, 2)


def proc(pid="BP01", name="Process", systems="System A", mtpd="24", rto="4", rpo="1", tier="T1",
         deps="", impacts=("1", "2", "3", "4")):
    row = {"id": pid, "name": name, "primary_systems": systems, "mtpd_hours": mtpd, "rto_hours": rto,
           "rpo_hours": rpo, "tier": tier, "key_dependencies": deps}
    for column, value in zip(dr.IMPACT_COLUMNS, impacts):
        row[column] = value
    return row


def test_row(tid="RT-1", date="2026-09-01", system="System A", tier="T1", rto="4", actual="2",
             rpo="1", age="0.5", result="Pass"):
    return {"test_id": tid, "date": date, "system": system, "tier": tier, "rto_target_hours": rto,
            "actual_restore_hours": actual, "rpo_target_hours": rpo, "actual_data_age_hours": age,
            "result": result}


def check(bia, log=None, as_of=AS_OF):
    report = dr.Report()
    dr.check_bia(bia, report)
    if log is not None:
        dr.check_restore_log(bia, log, as_of, report)
    return report


def codes(items):
    return [i.split(" ", 1)[0] for i in items]


class HelperTests(unittest.TestCase):
    def test_tokens_drop_qualifiers_and_case(self):
        self.assertEqual(dr.tokens("Finance system (SaaS); Bank portal ;"), ["finance system", "bank portal"])

    def test_names_match_either_way_round(self):
        self.assertTrue(dr.names_match("entra id", "entra id"))
        self.assertTrue(dr.names_match("telephony", "telephony supplier"))
        self.assertFalse(dr.names_match("dns", "finance system"))

    def test_number_handles_bad_values(self):
        self.assertEqual(dr.number("0.25"), 0.25)
        self.assertIsNone(dr.number("{{hours}}"))


class BiaRuleTests(unittest.TestCase):
    def test_clean_bia_has_no_errors(self):
        report = check([proc()])
        self.assertEqual(report.errors, [])

    def test_duplicate_id_is_an_error(self):
        self.assertIn("DR01", codes(check([proc(), proc()]).errors))

    def test_non_numeric_hours_is_an_error(self):
        report = check([proc(rto="{{hours}}")])
        self.assertIn("DR01", codes(report.errors))

    def test_unknown_tier_is_an_error(self):
        self.assertIn("DR02", codes(check([proc(tier="T9")]).errors))

    def test_rto_over_tier_maximum_is_an_error(self):
        report = check([proc(rto="5", tier="T1")])
        self.assertIn("DR02", codes(report.errors))
        self.assertIn("longer than the T1 maximum", report.errors[0])

    def test_rpo_over_tier_maximum_is_an_error(self):
        self.assertIn("DR02", codes(check([proc(rpo="25", tier="T2", rto="24", mtpd="48")]).errors))

    def test_values_at_the_tier_maximum_are_allowed(self):
        self.assertEqual(check([proc(rto="4", rpo="4", tier="T1")]).errors, [])

    def test_rto_must_be_shorter_than_mtpd(self):
        self.assertIn("DR03", codes(check([proc(rto="4", mtpd="4")]).errors))
        self.assertEqual(check([proc(rto="4", mtpd="5")]).errors, [])

    def test_falling_impact_is_a_warning(self):
        report = check([proc(impacts=("3", "2", "4", "5"))])
        self.assertEqual(codes(report.warnings), ["DR06"])
        self.assertEqual(report.errors, [])

    def test_dependency_with_slower_rto_is_an_error(self):
        bia = [
            proc("BP01", systems="App", rto="4", deps="Identity"),
            proc("BP02", systems="Identity", rto="24", tier="T1", mtpd="48"),
        ]
        report = check(bia)
        self.assertIn("DR04", codes(report.errors))
        self.assertIn("committed for identity (BP02)", "\n".join(report.errors))

    def test_dependency_with_equal_or_faster_rto_is_allowed(self):
        bia = [
            proc("BP01", systems="App", rto="4", deps="Identity"),
            proc("BP02", systems="Identity", rto="2", tier="T0", rpo="0.25", mtpd="8"),
        ]
        self.assertEqual(check(bia).errors, [])

    def test_dependency_in_a_lower_tier_is_an_error(self):
        bia = [
            proc("BP01", systems="App", rto="4", tier="T1", deps="Directory"),
            proc("BP02", systems="Directory", rto="4", tier="T2", mtpd="48"),
        ]
        self.assertIn("DR05", codes(check(bia).errors))

    def test_system_commitment_is_the_strictest_among_users(self):
        # Two processes list the system. The 4 hour one sets the commitment, so the 24 hour user is fine.
        bia = [
            proc("BP01", systems="Shared", rto="4", tier="T1"),
            proc("BP02", systems="Shared", rto="24", tier="T2", mtpd="48"),
            proc("BP03", systems="Other", rto="24", tier="T2", mtpd="48", deps="Shared"),
        ]
        self.assertEqual(check(bia).errors, [])

    def test_a_process_is_not_compared_with_its_own_system(self):
        bia = [proc("BP01", systems="Telephony; Microsoft 365", deps="Telephony supplier; Microsoft 365")]
        report = check(bia)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.notes, [])

    def test_unmatched_dependencies_are_notes_not_errors(self):
        report = check([proc(deps="Internet; Power"), proc("BP02", systems="System B", deps="Internet")])
        self.assertEqual(report.errors, [])
        self.assertEqual(codes(report.notes), ["DR07", "DR07"])
        self.assertIn("BP01, BP02", report.notes[0])


class RestoreLogTests(unittest.TestCase):
    def test_pass_that_missed_the_rto_is_an_error(self):
        report = check([proc()], [test_row(actual="5")])
        self.assertIn("DR10", codes(report.errors))

    def test_pass_that_missed_the_rpo_is_an_error(self):
        report = check([proc()], [test_row(age="2")])
        self.assertIn("DR10", codes(report.errors))

    def test_fail_that_missed_the_rto_is_not_inconsistent(self):
        report = check([proc()], [test_row(actual="5", result="Fail")])
        self.assertNotIn("DR10", codes(report.errors))
        self.assertIn("DR13", codes(report.warnings))

    def test_process_without_a_test_is_a_warning(self):
        report = check([proc()], [])
        self.assertEqual(codes(report.warnings), ["DR11"])
        self.assertEqual(report.process_rows[0][3], "none")

    def test_current_passing_test_gives_no_warnings(self):
        report = check([proc()], [test_row()])
        self.assertEqual(report.warnings, [])
        self.assertEqual(report.process_rows[0][5], "Current and within targets")

    def test_overdue_test_is_a_warning_by_tier(self):
        old = test_row(date="2026-03-01")
        self.assertIn("DR12", codes(check([proc(tier="T1")], [old]).warnings))
        t2 = proc(tier="T2", rto="24", rpo="24", mtpd="48")
        self.assertEqual(check([t2], [old]).warnings, [])

    def test_latest_test_is_the_one_that_counts(self):
        log = [test_row("RT-1", date="2025-01-01"), test_row("RT-2", date="2026-10-01")]
        self.assertEqual(check([proc()], log).warnings, [])

    def test_latest_failed_test_is_a_warning_even_if_an_older_one_passed(self):
        log = [test_row("RT-1", date="2026-08-01"), test_row("RT-2", date="2026-10-01", result="Fail")]
        self.assertEqual(codes(check([proc()], log).warnings), ["DR13"])

    def test_bia_targets_are_used_not_the_logged_targets(self):
        # The log says RTO 24, but the BIA promises 4 hours and the restore took 6.
        log = [test_row(rto="24", actual="6", rpo="24")]
        report = check([proc(rto="4")], log)
        self.assertIn("against a BIA RTO of 4h", report.warnings[0])

    def test_system_names_are_matched_loosely(self):
        log = [test_row(system="System A database (immutable copy)")]
        self.assertEqual(check([proc(systems="System A (SaaS)")], log).warnings, [])

    def test_bad_log_date_is_an_input_error(self):
        with self.assertRaises(dr.InputError):
            check([proc()], [test_row(date="02/11/2026")])


class FileAndCommandLineTests(unittest.TestCase):
    def call(self, args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = dr.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_missing_file_exits_two(self):
        code, _, err = self.call(["--bia", "does-not-exist.csv"])
        self.assertEqual(code, 2)
        self.assertIn("file not found", err)

    def test_missing_column_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bia.csv"
            path.write_text("id,name\nBP01,x\n", encoding="utf-8")
            code, _, err = self.call(["--bia", str(path)])
        self.assertEqual(code, 2)
        self.assertIn("missing column(s)", err)

    def test_worked_example_has_no_errors(self):
        code, out, _ = self.call(["--as-of", "2026-11-02"])
        self.assertEqual(code, 0, msg=out)
        self.assertIn("0 error(s)", out)

    def test_strict_mode_fails_on_warnings(self):
        code, _, _ = self.call(["--as-of", "2026-11-02", "--strict"])
        self.assertEqual(code, 1)

    def test_errors_exit_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bia.csv"
            header = ",".join(dr.BIA_COLUMNS)
            row = "BP01,Name,Sys,1,2,3,4,24,30,1,T1,"
            path.write_text(header + "\n" + row + "\n", encoding="utf-8")
            code, out, _ = self.call(["--bia", str(path)])
        self.assertEqual(code, 1)
        self.assertIn("DR02", out)

    def test_example_report_is_current(self):
        code, _, err = self.call(["--check", str(dr.EXAMPLE_REPORT)])
        self.assertEqual(code, 0, msg=err)

    def test_stale_report_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "old.md"
            path.write_text("old", encoding="utf-8")
            code, _, err = self.call(["--check", str(path)])
        self.assertEqual(code, 1)
        self.assertIn("STALE", err)

    def test_markdown_output_lists_findings_and_limits(self):
        code, out, _ = self.call(["--markdown", "--as-of", "2026-11-02"])
        self.assertEqual(code, 0)
        self.assertIn("# DR gap report", out)
        self.assertIn("## Restore evidence by process", out)
        self.assertIn("What this report cannot tell you", out)


class WorkedExampleDataTests(unittest.TestCase):
    def test_shipped_example_is_internally_consistent(self):
        report, processes, tests = dr.run(dr.EXAMPLE_BIA, dr.EXAMPLE_LOG, dr.EXAMPLE_AS_OF)
        self.assertEqual(report.errors, [])
        self.assertEqual((processes, tests), (14, 9))

    def test_example_shows_each_kind_of_restore_warning(self):
        report, _, _ = dr.run(dr.EXAMPLE_BIA, dr.EXAMPLE_LOG, dr.EXAMPLE_AS_OF)
        self.assertTrue({"DR11", "DR12", "DR13"} <= set(codes(report.warnings)))

    def test_hr_system_is_not_left_slower_than_payroll(self):
        # Regression: the first draft rated the HR system T3 although payroll (T2) depends on it.
        rows = {r["id"]: r for r in dr.read_csv(dr.EXAMPLE_BIA, dr.BIA_COLUMNS)}
        self.assertEqual(rows["BP13"]["tier"], "T2")
        self.assertLessEqual(float(rows["BP13"]["rto_hours"]), float(rows["BP07"]["rto_hours"]))


if __name__ == "__main__":
    unittest.main()
