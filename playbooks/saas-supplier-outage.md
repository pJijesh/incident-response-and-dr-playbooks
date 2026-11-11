# Playbook: Critical SaaS or supplier outage

| Field | Value |
|---|---|
| Version | 1.0 |
| Owner | IT Manager |
| Last reviewed | 2026-11-04 |
| Review cycle | At least every 12 months, and after every real incident or exercise |
| Related | [DDoS and service outage](ddos-service-outage.md), [Personal data breach](personal-data-breach.md), [Dependency map](../dr/dependency-map.md), [BIA template](../dr/bia-template.md) |

> This playbook is operational guidance, not legal advice. Contractual rights (service credits, termination, liability) depend on your actual agreements, so ask your legal adviser or procurement lead.

## 1. Purpose

To keep the business running, and informed, when a cloud service or supplier that the business depends on is unavailable, degraded or compromised, and the fix is not in your hands. Examples: a freight or warehouse management SaaS, a customs declaration service, a payment gateway, a managed service provider, an ISP, Microsoft 365, an identity provider or a carrier portal.

Your levers are: workarounds, escalation, communication, and recording the evidence you will need for contractual recovery.

## 2. Triggers

- Users report that a SaaS application is slow, unreachable or throwing errors.
- The supplier's status page, email or account manager reports an incident.
- Your monitoring (synthetic checks, uptime monitors) fails against the supplier's endpoint.
- Integrations or scheduled data exchanges fail (EDI, API, file transfers).
- The supplier tells you they have had a cyber incident or data breach.
- An ISP or MSP outage cuts a site off.
- A public cloud region or a major platform (for example identity or email) has a widespread outage.

## 3. Severity matrix

Severity should follow the business impact analysis. Find the service on the [BIA](../dr/bia-template.md) and compare its RTO with the time already lost.

| Level | Examples |
|---|---|
| P1 Critical | A Tier 0 or Tier 1 service (see [RTO and RPO tiers](../dr/rto-rpo-tiers.md)) is down and its RTO is at risk or breached; customer deliveries, customs declarations or payments cannot be processed; a supplier security incident involving your data |
| P2 High | An important service is degraded or down but a workaround exists, or an outage is limited to one site or team |
| P3 Medium | A Tier 3 service is unavailable, or degradation with minimal impact |
| P4 Low | Planned maintenance, or a short blip with no impact |

## 4. Roles

| Role | Duties |
|---|---|
| Incident Manager | Declares the incident, sets severity, chairs updates and invokes workarounds |
| Technical Lead | Verifies the outage independently, tests workarounds, manages supplier technical contact |
| Supplier liaison | Escalates through the supplier's support, account manager and contract channels. Records ticket numbers and time stamps |
| Business process owners | Run workarounds, record manual activity, reconcile later |
| Communications Lead | Updates staff, customers and partners |
| Executive Sponsor | Approves emergency spending, switching suppliers and customer commitments |

## 5. First 15 minutes

1. **Confirm it is the supplier, not you.** Check from a second network, a different device and a different user. Check the supplier's status page and independent monitoring. Rule out local causes: DNS, firewall, ISP, expired certificate, changed proxy or Conditional Access.
2. **Open a ticket** with the supplier and record the ticket number, time and the name of the person you spoke to. Use the escalation path in the contract, not only the standard support route.
3. **Note the start time** of the outage as users first experienced it. You will need it for service credits and RTO tracking.
4. **Identify the business impact**: which processes, sites and customers are affected. Use the [dependency map](../dr/dependency-map.md) to find downstream effects.
5. **Declare the incident** and set a provisional severity. Start the [decision log](../comms/decision-log-template.md).
6. **Tell staff** what is known and how to work in the meantime, using the [staff notice](../comms/staff-notice.md). Name the workaround owners.
7. **Ask the supplier** the four standard questions: what is the cause (if known), what is the scope, what is the estimated time to restore and when is your next update, and has any of our data been affected or accessed?

## 6. Containment

In a supplier outage, "containment" means limiting the business impact and the risk from the supplier's own incident.

- [ ] Activate the documented workaround for each affected process: manual forms, offline spreadsheets, alternative portals, direct phone or email contact with carriers and customers, or authority contingency procedures where they exist.
- [ ] Pause automated integrations that could send bad or partial data, and queue outbound transactions for replay.
- [ ] Capture and export any data you can still reach from the supplier (reports, extracts, downloads) before the situation worsens.
- [ ] If the supplier reports a security incident: rotate API keys, tokens and service credentials, review access logs on your side, and restrict integration accounts to the minimum.
- [ ] If the supplier is an MSP or has privileged access: suspend or monitor their access while their incident is understood.
- [ ] Redirect work to other sites or teams if one site or connection is down.
- [ ] Track the RTO clock against the target for the affected service.

## 7. Eradication

For outages, eradication means ending the dependency on the failure.

- Obtain the root cause and the fix from the supplier in writing.
- If the cause is on your side (configuration, credentials, network), fix it and tell the supplier.
- If the supplier suffered a security incident, require evidence that the cause is removed: scope, timeline, indicators, and confirmation of whether your data was affected. Review the integration credentials and tokens again.
- Check for data left in an inconsistent state: partially processed transactions, duplicates and missing messages.

## 8. Recovery

1. Confirm with the supplier that service is restored, and verify it yourself with a named test: a business user completes a real transaction end to end.
2. Replay queued transactions in order. Reconcile manual work against the system of record and record variances.
3. Re-enable integrations and scheduled jobs gradually, and watch for duplicates and errors.
4. Check data integrity against the RPO: what was lost and what has to be re-entered?
5. Inform affected parties that service is restored, and what they need to do, such as resubmit a document.
6. Stand down the workaround and confirm that the staff have returned to normal procedures.
7. Record the actual duration of the outage and compare it to the RTO. Feed the result into the [BIA](../dr/bia-template.md) and the [DR test report](../dr/dr-test-report-template.md).

## 9. Evidence handling

- Keep the **timeline** of the outage with times of first symptom, supplier acknowledgement, workaround activation and restoration.
- Keep **supplier communications**: status page screenshots, tickets, emails, call notes.
- Keep **impact evidence**: orders delayed, declarations late, overtime, penalties, goodwill gestures. These support service credit claims and, if needed, a contractual dispute.
- Preserve **your own logs** showing the failures (monitoring, API logs, error messages).
- If the supplier suffered a security incident, preserve integration logs and request the supplier's incident report.

## 10. Communications

| Audience | Template | Notes |
|---|---|---|
| Staff | [Staff notice](../comms/staff-notice.md) | State what works, what does not, the workaround and the next update time |
| Customers and partners | [Customer notice](../comms/customer-notice.md) | Be factual, avoid naming the supplier without agreement unless it is already public. Say what you are doing for them |
| Board | [Board update](../comms/board-update.md) | For P1 or when contractual obligations are at risk |
| Supplier | Written, in the contract's notice format if required | Record every request and response |

Say what you know, what you do not know, and when you will next update. Do not blame the supplier in external messages.

## 11. Regulatory and contractual notifications

| Who | When |
|---|---|
| Customers | If your contracts or SLAs require notice of service interruption, and as early as they will notice |
| Supplier | Formal notice of the incident and claim for service credits, within the contractual notice period. Check it now rather than later |
| ICO | If the supplier's incident involves personal data and is likely to result in a risk to individuals, the controller must report within 72 hours of becoming aware. A processor must tell you without undue delay. See the [personal data breach playbook](personal-data-breach.md) |
| Insurer | If the outage may be covered under contingent business interruption or cyber cover. Check the policy and its waiting period |
| NCSC | If the supplier incident is a significant cyber incident, report via the NCSC reporting service |
| Customs and sector authorities | If declarations or record-keeping are affected, follow the contingency arrangements published by the relevant authority and your internal compliance procedure |
| Card acquirer | If a payment gateway or cardholder data environment is affected |

## 12. Decision points

| # | Decision | Owner |
|---|---|---|
| D1 | Is this a supplier incident, a local fault or both? | Technical Lead |
| D2 | Invoke workarounds now, or wait for the supplier ETA? | Incident Manager with process owners |
| D3 | Escalate within the supplier and to executive level | Supplier liaison, Executive Sponsor |
| D4 | Notify customers and partners, and how | Communications Lead |
| D5 | Switch to an alternative provider or invoke an exit or failover plan, if one exists | Executive Sponsor |
| D6 | Is there a data breach element at the supplier? | Data Protection Lead |
| D7 | Close the incident and confirm recovery | Incident Manager with process owners |

## 13. Post-incident actions

- Blameless [post-incident review](../comms/post-incident-review-template.md), including the supplier where appropriate.
- Claim service credits and recover costs in line with the contract.
- Update the [BIA](../dr/bia-template.md) and [dependency map](../dr/dependency-map.md) if the outage revealed an unknown dependency.
- Improve supplier management: security and resilience clauses, incident notification times, right to audit, data export and exit provisions, financial standing, subprocessor transparency. The NCSC supply chain guidance gives a framework (see [references](../docs/references.md#supply-chain-and-suppliers)).
- Reduce single points of failure: second ISP, regular data exports, offline copies of critical reference data (customer lists, tariff files, contact details), documented workarounds tested with the business.
- Update this playbook and the supplier contact register.

## 14. Quick-reference checklist

- [ ] Confirm it is not you: second network, second device, supplier status page
- [ ] Open a supplier ticket; record ticket number, time, person
- [ ] Note when users first experienced the problem (RTO clock starts)
- [ ] Declare the incident, set severity from the BIA tier, start the decision log
- [ ] Ask the supplier: cause, scope, ETA and next update, any data affected
- [ ] Activate workarounds; assign owners; record manual activity
- [ ] Pause integrations that could send bad data; queue transactions
- [ ] Export whatever data you can still reach
- [ ] Rotate integration credentials if the supplier reports a security incident
- [ ] Update staff, customers and the board per the templates
- [ ] Check contract notice periods, SLA and service credit rules
- [ ] On restoration: verify with a real end-to-end transaction; replay and reconcile
- [ ] Record actual downtime against the RTO; run the review
