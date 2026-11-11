# Decision log template

The decision log is the single most valuable record of an incident. It shows what you knew, what you decided, who decided, and why. It supports insurance claims, regulators, auditors and learning.

**Rules**

1. Assign a **Scribe** whose only job is the log.
2. Keep it on a system the attacker cannot reach: a clean device, an unaffected tenant, or paper.
3. Record times consistently (UK local time or UTC, say which) and in 24-hour format.
4. Record facts and decisions, not opinions or blame.
5. Log decisions not to act as well as decisions to act.
6. Copy it into the incident record when the incident closes.

## Incident header

| Field | Entry |
|---|---|
| Incident reference | {{}} |
| Playbook(s) in use | {{}} |
| Time of first awareness | {{}} (this is also the start of the 72-hour assessment clock if personal data may be involved) |
| Incident Manager | {{role}} |
| Scribe | {{role}} |
| Time zone used | {{UK local or UTC}} |

## Decision log

| # | Time | Decision or event | Options considered | Decision made | Made by | Rationale | Information known at the time | Follow-up and owner |
|---|---|---|---|---|---|---|---|---|
| 1 | {{}} | {{Incident declared at P1}} | {{P1, P2}} | {{P1}} | {{Incident Manager}} | {{Servers encrypted, backups unknown}} | {{}} | {{Open bridge: Technical Lead}} |
| 2 | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |

## Timeline of facts and actions

| Time | Source | What happened or was done | By |
|---|---|---|---|
| {{}} | {{User report, EDR alert, supplier, log}} | {{}} | {{}} |

## Notification tracker

| Obligation | Required? (Y, N, TBC) | Deadline | Decision-maker | Sent (time and reference) | Reason if not required |
|---|---|---|---|---|---|
| ICO | {{}} | {{72 hours from awareness}} | {{}} | {{}} | {{}} |
| Affected individuals | {{}} | {{without undue delay}} | {{}} | {{}} | {{}} |
| Insurer | {{}} | {{per policy}} | {{}} | {{}} | {{}} |
| NCSC | {{}} | {{}} | {{}} | {{}} | {{}} |
| Police and Report Fraud | {{}} | {{}} | {{}} | {{}} | {{}} |
| Customers per contract | {{}} | {{}} | {{}} | {{}} | {{}} |
| Card acquirer | {{}} | {{}} | {{}} | {{}} | {{}} |
| Other | {{}} | {{}} | {{}} | {{}} | {{}} |

## Evidence register

| Item | Collected by | Date and time | Location and hash (where relevant) | Chain of custody notes |
|---|---|---|---|---|
| {{}} | {{}} | {{}} | {{}} | {{}} |

## Closure

| Field | Entry |
|---|---|
| Time declared resolved | {{}} |
| Approved by | {{}} |
| Post-incident review date | {{}} |
| Open actions handed to | {{}} |
