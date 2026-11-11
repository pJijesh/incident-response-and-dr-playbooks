# RTO and RPO tier table

Tiering turns a long list of systems into a small number of recovery commitments that people can remember and the business can fund. Every system on the [BIA](bia-template.md) is assigned to exactly one tier, and the tier sets the recovery target, the backup design and the test frequency.

> The values below are starting points for a small or mid-size organisation, not a standard. Set yours from the business impact analysis and have the executive sponsor sign them off. A target that nobody has paid for is a wish, not a plan.

## Definitions

| Term | Meaning |
|---|---|
| MTPD (maximum tolerable period of disruption) | The point at which the business impact becomes unacceptable (for example a lost customer, a regulatory breach, safety risk). Sometimes called MAO |
| RTO (recovery time objective) | The target time to restore a service after disruption. Always shorter than the MTPD |
| RPO (recovery point objective) | The maximum acceptable data loss, measured in time (how old the restored data may be) |
| MVO (minimum viable operation) | The smallest set of functions and data needed to keep operating at an acceptable level while full recovery continues |
| WRT (work recovery time) | The time after technical restoration needed to reconcile, validate and catch up |

## Tier table

| Tier | Name | Typical examples | RTO (max) | RPO (max) | Backup and resilience design | Restore test frequency |
|---|---|---|---|---|---|---|
| T0 | Foundation | Identity (Active Directory, Entra ID), DNS, network and internet, firewalls, backup platform itself | 2 hours | 15 minutes | Redundant paths, configuration backups after every change, break-glass accounts, documented rebuild, offline copy of critical configuration | Every 6 months, plus after major change |
| T1 | Critical | Core line-of-business applications, customs and shipment systems, email and telephony, warehouse systems | 4 hours | 4 hours (1 hour for transactional systems) | Frequent backups or replication, immutable or offline copy, documented workaround, supplier SLA aligned to RTO | Every 6 months |
| T2 | Important | Finance, payroll, card payments, file shares | 24 hours | 24 hours (4 hours for transaction data) | Daily backups with immutable copy, tested restore, documented manual process | Every 12 months |
| T3 | Standard | CRM, HR systems, internal tools | 72 hours | 24 hours | Daily backups or supplier-managed backups with verified export | Every 12 months (sample) |
| T4 | Deferrable | Reporting, archives, development and test | 7 days | 7 days | Weekly backup or rebuild from code | Every 12 months (sample) |

Rules for using the table:

- The **RTO of a service cannot be shorter than that of anything it depends on.** If your freight management system is T1 and depends on Entra ID, then Entra ID must be T0 (see the [dependency map](dependency-map.md)).
- **Peak periods** can raise a tier temporarily: payroll day, month end, peak shipping season. Record these in the BIA.
- **SaaS services** are not exempt. If the supplier's recovery commitment is longer than your RTO, record the gap, agree a workaround, and either negotiate or accept the risk formally.
- **Backups are not DR.** A backup is an input. DR is the tested ability to restore a working service within the RTO.
- **Immutable or offline copies** matter for ransomware. The NCSC advises keeping backups separate from your network and testing that restores work (see [references](../docs/references.md#ransomware-and-disruptive-attacks)).

## Reading the table against a real service

Example: customs declarations are assigned T1.

- RTO 4 hours: if the supplier-hosted service is unavailable for longer, manual contingency procedures start and declarations may be late.
- RPO 1 hour: declarations drafted in the last hour could be lost, so the team keeps a list of work in progress to re-enter.
- Test: every 6 months, a person from customs compliance takes part in the restore verification.

## Governance

| Item | Owner | Frequency |
|---|---|---|
| Review tier definitions and values | IT Manager and executive sponsor | Annually |
| Review tier assignment for each service | Business process owners with IT | Annually, and on significant change |
| Report exceptions to the executive team | IT Manager | Quarterly |
| Evidence of restore tests | IT Manager | After each test, via the [test log](backup-restore-test-log.md) and [test report](dr-test-report-template.md) |
