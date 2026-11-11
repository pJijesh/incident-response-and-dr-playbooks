# BIA worked example: Fernhill Freight Ltd (fictional)

This example is for a fictional company and fictional systems, invented to show how a completed BIA reads. The ratings and targets are illustrative and are not benchmarks for any real organisation.

**Fernhill Freight Ltd** is a made-up freight forwarder of about 120 people with two offices and a bonded warehouse. It runs Microsoft 365 with hybrid Active Directory, a SaaS freight management system, a supplier-hosted customs declaration service, a card payment gateway and a managed service provider for network support.

The full data is in [bia-worked-example.csv](bia-worked-example.csv). Impact is rated 1 (negligible) to 5 (severe) after the stated outage length. See the [scale](bia-template.md#impact-scale).

## Summary view

| ID | Process | Impact at 4h | Impact at 24h | MTPD | RTO | RPO | Tier |
|---|---|---|---|---|---|---|---|
| BP10 | Identity and access | 5 | 5 | 8 h | 2 h | 15 min | T0 |
| BP11 | Network and internet connectivity | 5 | 5 | 8 h | 2 h | 15 min | T0 |
| BP01 | Shipment booking and tracking | 4 | 5 | 24 h | 4 h | 1 h | T1 |
| BP02 | Customs declarations | 5 | 5 | 12 h | 4 h | 1 h | T1 |
| BP03 | Warehouse receipt, pick and dispatch | 4 | 5 | 24 h | 4 h | 1 h | T1 |
| BP04 | Customer service and phone lines | 4 | 4 | 24 h | 4 h | 1 h | T1 |
| BP05 | Email and collaboration | 4 | 4 | 24 h | 4 h | 4 h | T1 |
| BP06 | Invoicing and credit control | 2 | 3 | 72 h | 24 h | 4 h | T2 |
| BP07 | Supplier payments and payroll | 2 | 4 | 48 h | 24 h | 4 h | T2 |
| BP08 | Card payments from customers | 2 | 3 | 72 h | 24 h | 4 h | T2 |
| BP09 | File shares and scanned documents | 3 | 4 | 48 h | 24 h | 4 h | T2 |
| BP12 | Sales CRM and quoting | 1 | 2 | 7 d | 72 h | 24 h | T3 |
| BP13 | HR records and recruitment | 1 | 2 | 7 d | 72 h | 24 h | T3 |
| BP14 | Management reporting | 1 | 1 | 14 d | 7 d | 24 h | T4 |

## What the exercise revealed (fictional findings)

These illustrate the kind of findings a real BIA surfaces. They are examples, not claims about any real organisation.

1. **Customs declarations have the shortest MTPD of any business application** (12 hours), because declarations feed customer clearance and the company's customs authorisation conditions. The customs team's workaround depends on the authority's published contingency procedure, which nobody had printed. Action: print it, test the process, and store it with the contact sheet.
2. **Identity is a hidden single point of failure.** Almost every T1 process depends on Entra ID and on-premises Active Directory, so these are T0. Action: break-glass accounts, a tested domain controller restore, offline copy of directory configuration.
3. **Email is T1 but its RPO of 4 hours depends on a third-party backup of Microsoft 365.** The native retention features were not designed as a backup. Action: confirm the third-party backup frequency and test restores of mailboxes and SharePoint.
4. **Warehouse paper fallback has a limit.** The warehouse can run on paper for about 8 hours before stock accuracy suffers. This sets BP03's RTO of 4 hours with a margin.
5. **Payroll day lifts BP07 to a T1-like target for that day.** Recorded in peak periods.
6. **Managed service provider is a dependency of three T0 and T1 services.** Action: review the contract for incident response times against the RTOs.

## From BIA to action

| BIA finding | Where it goes |
|---|---|
| Tiers and targets | [RTO and RPO tier table](rto-rpo-tiers.md) and [DR plan](dr-plan-template.md) recovery order |
| Dependencies | [Dependency map](dependency-map.md) |
| Workarounds | Business continuity procedures, referenced in each [playbook](../playbooks/README.md) |
| Restore tests | [Backup and restore test log](backup-restore-test-log.md) and [DR test report](dr-test-report-template.md) |
| Accepted risks | Risk register, reviewed by the executive sponsor |
