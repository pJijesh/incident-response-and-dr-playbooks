# Shared severity model and incident lifecycle

Every playbook in this repository uses the same four severity levels so that people do not have to relearn them under pressure. Each playbook adds scenario-specific examples to the matrix, but the response targets below are common.

> These targets are sensible starting points for a small IT team, not standards. Set your own in your incident response policy and have your executive sponsor approve them.

## Severity levels and response targets

| Level | Meaning | Incident Manager engaged | Executive sponsor told | Update cadence to leadership |
|---|---|---|---|---|
| P1 Critical | Core business services down or at serious risk, confirmed or probable data loss or exposure, or regulatory or contractual deadlines clearly engaged | Immediately (within 15 minutes of detection) | Within 30 minutes | Every 60 minutes, or at each decision point |
| P2 High | Significant degradation, a single important service or site affected, or a contained but serious security event | Within 30 minutes | Within 2 hours | Every 2 to 4 hours |
| P3 Medium | Limited impact, workaround available, few users affected, no evidence of data exposure | Within 4 hours (working hours) | In the next daily summary | Daily |
| P4 Low | Minor event, no business impact, logged for trend analysis | Next working day | Not required | In monthly reporting |

Rules of thumb:

- If you are unsure between two levels, choose the higher one and downgrade later. Downgrading is cheap, a late escalation is not.
- Severity is reviewed at every decision point and recorded in the [decision log](../comms/decision-log-template.md).
- Any incident that may involve personal data also starts the [personal data breach playbook](../playbooks/personal-data-breach.md) in parallel, whatever its severity, because the notification clock runs separately.

## Incident lifecycle used across the playbooks

```text
Detect -> Triage and declare -> Contain -> Eradicate -> Recover -> Review and improve
             |                                                  |
             +--- Communicate and notify (runs throughout) -----+
```

1. **Detect.** Someone notices something: an alert, a user report, a supplier email, a call from a customer.
2. **Triage and declare.** The first responder records what is known, picks a playbook and a provisional severity, and tells the Incident Manager. A declared incident gets a reference and a decision log.
3. **Contain.** Stop the harm spreading. Preserve evidence while doing so.
4. **Eradicate.** Remove the cause: malware, attacker access, faulty configuration.
5. **Recover.** Restore services in priority order from the [RTO and RPO tier table](../dr/rto-rpo-tiers.md), and verify them before handing back to users.
6. **Review and improve.** A blameless [post-incident review](../comms/post-incident-review-template.md) produces owned, dated actions.

This follows the same broad shape as NCSC incident management guidance (plan, respond, recover, learn). See [references](references.md).

## Standard roles

Small teams will combine roles. The point is that every role is named in advance and every decision has an owner.

| Role | Responsibilities in one line |
|---|---|
| Incident Manager | Runs the response, owns the severity call, keeps the decision log moving, makes or escalates decisions |
| Technical Lead | Directs investigation, containment and recovery work |
| Communications Lead | Owns messages to staff, customers, suppliers and media, using approved templates |
| Data Protection Lead | Assesses personal data impact, owns the ICO and data subject decisions (the DPO, where one is appointed) |
| Executive Sponsor | Authorises business-impacting decisions such as shutting a service, paying for external help, or notifying regulators |
| Scribe | Keeps the timeline and decision log, and nothing else |
| Supplier liaison | Single point of contact for the MSP, vendors, insurer and external responders |

Keep the named people and their deputies on the [contact sheet](../comms/contact-sheet-template.md), stored somewhere that does not depend on the systems that may be down (printed copy, personal phones, a second cloud tenant or a password manager with offline access).

## Out-of-band communication

If identity, email or chat may be compromised, assume attackers can read them. Agree in advance a separate channel (for example a phone call tree and a messaging group created on personal devices) and a code phrase process for confirming that a person is who they say they are. Keep the incident log on a system the attacker cannot reach. The NCSC makes the same point about keeping records of decisions on unaffected systems in its ransomware payment guidance, see [references](references.md).
