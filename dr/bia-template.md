# Business impact analysis (BIA) template

A BIA tells you which business processes matter most, what happens if they stop, and how quickly and with how little data loss they must come back. It is the input for tiering ([RTO and RPO tiers](rto-rpo-tiers.md)), the [DR plan](dr-plan-template.md), and the severity calls in every [playbook](../playbooks/README.md).

Files:

- This guide and scales.
- [bia-template.csv](bia-template.csv): the blank sheet to fill in (one row per business process).
- [bia-worked-example.md](bia-worked-example.md) and [bia-worked-example.csv](bia-worked-example.csv): a completed example for a fictional company.

## How to run a BIA in four short workshops

1. **List the processes** (not systems) with each department lead. Ask "what must happen for us to serve customers, pay people and stay legal?" Aim for 10 to 25 processes.
2. **Rate the impact over time** (1 hour, 4 hours, 24 hours, 72 hours) using the scale below, and record the highest rating across the categories.
3. **Set the targets**: the MTPD (when the impact becomes unacceptable), the RTO (shorter than the MTPD), and the RPO (how much data you can afford to lose).
4. **Map the dependencies**: systems, people, suppliers, sites, data. Update the [dependency map](dependency-map.md). Assign a tier. Check that every dependency is at the same tier or higher.

Have the executive sponsor challenge and sign off the result. Repeat annually and after any significant change.

## Impact scale

| Rating | Label | Description |
|---|---|---|
| 1 | Negligible | Inconvenience, absorbed by normal working |
| 2 | Minor | Some delay or extra work, no customer or regulatory effect |
| 3 | Moderate | Visible customer impact, minor financial loss, or a contractual target at risk |
| 4 | Major | Customer loss or contract breach likely, notable financial loss, or regulatory attention |
| 5 | Severe | Safety risk, serious regulatory breach, loss of a key customer or licence, or threat to the business |

Rate the following categories and record the highest rating in the sheet:

- Financial (revenue, penalties, extra cost).
- Customer and reputational.
- Legal, regulatory and contractual (customs, data protection, audit conditions, customer SLAs).
- Safety and security.
- Staff and operational.

## Column guide for the CSV

| Column | What to enter |
|---|---|
| id | Short unique code, for example BP01 |
| name | Process name |
| owner_role | A role (for example "Warehouse Manager"), not a named person, so that it survives staff changes |
| description | One line |
| primary_systems | Systems the process uses |
| impact_1h, impact_4h, impact_24h, impact_72h | Highest impact rating (1 to 5) after that outage length |
| mtpd_hours | Maximum tolerable period of disruption in hours |
| rto_hours | Recovery time objective in hours (must not exceed mtpd_hours) |
| rpo_hours | Recovery point objective in hours (0.25 means 15 minutes) |
| tier | T0 to T4, see [tier table](rto-rpo-tiers.md). The tier's maximum RTO and RPO must not be exceeded |
| peak_periods | When the impact is worse |
| workaround | What people do while the system is down |
| key_dependencies | Systems, suppliers and sites, separated by semicolons |
| regulatory_contractual_driver | Legal, regulatory, customer or audit drivers |
| notes | Assumptions, accepted risks |

Keep the CSV in the repository (or your document system) and treat it as a controlled document. The [checker](../tools/check_playbooks.py) does not read it, but the repository's tests validate the structure of the worked example, and you can reuse that test for your own file.

## Common mistakes

- Listing systems instead of processes.
- Giving every process a 1-hour RTO. If everything is critical, nothing is.
- Forgetting people, premises, suppliers and data as dependencies.
- Not testing whether the stated RTO is achievable.
- Setting an RPO tighter than the backup frequency can deliver.
- Treating a SaaS provider's uptime as the same thing as your recovery time. The supplier restores their service, not your data, your configuration or your workarounds.
