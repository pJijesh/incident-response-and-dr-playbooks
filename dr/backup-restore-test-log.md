# Backup and restore test log

A backup you have never restored is a hope, not a control. This log records each restore test so that you can evidence it to auditors, insurers and your own board, and so that failures lead to fixes.

Use this file as a guide and keep the live log in [backup-restore-test-log.csv](backup-restore-test-log.csv) (or your ticketing or GRC tool). The CSV contains one fictional example row, which you should delete.

## How to run a restore test

1. Pick a system, tier and test type from the schedule in the [tier table](rto-rpo-tiers.md).
2. Choose the restore point **before** you start, so you cannot pick the one you know works.
3. Restore into an isolated location, never over production.
4. Time each phase: retrieve, restore, validate.
5. Validate with a business user: can they open and use the data? Check integrity, not only that files exist.
6. Compare with the RTO and RPO, and record the result honestly, including partial results.
7. Raise an action for every failure and for every step that took longer than expected.
8. Reset the test environment and record the cleanup.

## Test types

| Type | What it proves | Suggested use |
|---|---|---|
| File or item restore | Single files or mailbox items can be recovered | Monthly sample |
| Application or database restore | A service can be brought up and works from backup | Per tier schedule |
| Bare-metal or VM restore | A server can be rebuilt | T0 and T1, every 6 months |
| Identity restore | Directory and identity can be rebuilt | T0, every 6 months |
| Immutable or offline copy restore | Ransomware-resistant copy is usable | At least annually |
| Full DR exercise | The whole recovery sequence works within the RTO | Annually |

## Log fields

| Field | Description |
|---|---|
| test_id | Unique ID, for example RT-2026-014 |
| date | Date of test |
| system | System or data set |
| tier | T0 to T4 |
| test_type | One of the types above |
| backup_source | Tool and location, including which copy (local, offsite, immutable, offline) |
| restore_point | Date and time of the backup restored |
| rto_target_hours | From the BIA |
| actual_restore_hours | Measured, including validation |
| rpo_target_hours | From the BIA |
| actual_data_age_hours | Age of the restored data at the moment of the simulated failure |
| result | Pass, Partial, Fail |
| validated_by | Role of the business or technical validator |
| issues | What went wrong or was slow |
| actions | Actions raised, with IDs |
| tester | Role of the person who ran the test |
| evidence_link | Screenshot or log location |

## Pass criteria (suggested)

- Pass: restored within RTO, data within RPO, validated by a business user, no blocking issues.
- Partial: restored but outside RTO or RPO, or with data integrity issues that were fixed.
- Fail: could not restore, or the restored system could not be used.

Report Partial and Fail results to the executive sponsor with the actions needed, not only the passes.
