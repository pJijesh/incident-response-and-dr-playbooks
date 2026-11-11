# Playbooks

Six playbooks for the incidents a small IT team is most likely to face. All use the same fourteen sections in the same order, so that people who have used one can use any of them under pressure.

| Playbook | Use when | Typical first action |
|---|---|---|
| [Ransomware](ransomware.md) | Files encrypted, ransom note, backups tampered with, extortion claim | Isolate affected devices, protect backups, declare P1 |
| [M365 account compromise and BEC](m365-account-compromise-bec.md) | Phished credentials, suspicious sign-ins, hidden mailbox rules, payment diversion fraud | Call the bank if money moved, disable the account, revoke sessions |
| [Personal data breach](personal-data-breach.md) | Any incident that may involve personal data | Write down the time of awareness, open the breach record |
| [Lost or stolen device](lost-or-stolen-device.md) | Laptop, phone, security key or drive missing | Revoke sessions, lock or wipe, assess data |
| [Critical SaaS or supplier outage](saas-supplier-outage.md) | A supplier or cloud service the business depends on is down or compromised | Confirm it is not you, open a supplier ticket, start workarounds |
| [DDoS and service outage](ddos-service-outage.md) | Internet-facing service slow or unreachable | Classify attack, surge or fault, call the upstream provider |

Several playbooks often run together. A ransomware attack usually starts the personal data breach playbook as well, and a supplier breach can start three.

## The fourteen sections

1. Purpose
2. Triggers
3. Severity matrix
4. Roles
5. First 15 minutes
6. Containment
7. Eradication
8. Recovery
9. Evidence handling
10. Communications
11. Regulatory and contractual notifications
12. Decision points
13. Post-incident actions
14. Quick-reference checklist (one page, printable)

The [checker](../tools/check_playbooks.py) enforces this structure, so a playbook added by a contributor cannot silently drop a section.

## Shared material

- [Severity model, lifecycle and standard roles](../docs/severity-model.md)
- [Contact sheet template](../comms/contact-sheet-template.md)
- [Decision log](../comms/decision-log-template.md)
- [Communication templates](../comms/README.md)
- [References and sources](../docs/references.md)

## Printing the checklists

Section 14 of each playbook is written to fit on one page. Print them, put one set in each office and one in a sealed envelope off-site, and check them whenever you review the playbook.

## Adding a playbook

Copy the structure from an existing playbook, keep the section headings exactly as above, then run `python tools/check_playbooks.py --all-links`. See [CONTRIBUTING](../CONTRIBUTING.md).
