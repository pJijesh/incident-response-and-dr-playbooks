# Playbook: Ransomware

| Field | Value |
|---|---|
| Version | 1.0 |
| Owner | IT Manager |
| Last reviewed | 2026-11-04 |
| Review cycle | At least every 12 months, and after every real incident or exercise |
| Related | [Personal data breach](personal-data-breach.md), [M365 account compromise](m365-account-compromise-bec.md), [Severity model](../docs/severity-model.md), [DR plan template](../dr/dr-plan-template.md) |

> This playbook is operational guidance, not legal advice. Take advice from a qualified solicitor, your insurer and, where appropriate, an NCSC-assured incident response provider before making legal or regulatory decisions.

## 1. Purpose

To give a small IT team a clear, rehearsed way to respond when ransomware encrypts, or threatens to encrypt or publish, business data. The goals, in order, are: protect people and safety, stop the spread, preserve evidence, restore critical services from clean backups, and meet legal and contractual duties on time.

Scope: Windows and Linux servers, endpoints, hybrid Active Directory and Entra ID, Microsoft 365 data, file shares and hosted line-of-business systems. It assumes extortion with data theft is possible, because stealing data before encrypting it is now common (see the NCSC guidance on ransom payments in [references](../docs/references.md#ransomware-and-disruptive-attacks)).

## 2. Triggers

Start this playbook when any of the following is seen, even if only one is confirmed:

- Files renamed with an unfamiliar extension, or ransom notes (text files, wallpaper changes, printed pages) on a device or share.
- Multiple users reporting files that will not open at about the same time.
- EDR or antivirus alerts for mass file modification, shadow copy deletion, backup tampering or known ransomware tooling.
- Backup jobs failing, or backup repositories or consoles inaccessible, unexpectedly.
- A threat actor contacts the business claiming to hold its data, or data appears on a leak site.
- A supplier or MSP reports a ransomware incident that could affect your data or connectivity (also run the [supplier outage playbook](saas-supplier-outage.md)).

If unsure, treat it as ransomware until a technical lead says otherwise.

## 3. Severity matrix

Response targets are in the [shared severity model](../docs/severity-model.md).

| Level | Ransomware examples |
|---|---|
| P1 Critical | Encryption on servers, hypervisors or identity systems; multiple sites affected; backups affected; data theft claimed or likely; any customer-facing or customs-critical service down |
| P2 High | Encryption confined to one server or a small group of endpoints, contained within minutes, no sign of data theft, backups intact |
| P3 Medium | Ransomware detected and blocked by EDR before encryption, single endpoint, no lateral movement indicators |
| P4 Low | Known-bad file quarantined by email or endpoint controls with no execution |

Default to P1 until a Technical Lead has confirmed the scope in writing in the decision log.

## 4. Roles

Roles are defined in the [severity model](../docs/severity-model.md#standard-roles). Names and numbers belong on the [contact sheet](../comms/contact-sheet-template.md).

| Role | Ransomware-specific duties |
|---|---|
| Incident Manager | Declares P1, convenes the bridge, owns the "pay or not" escalation path, controls the pace of recovery |
| Technical Lead | Isolation, scoping, credential reset plan, backup validation, restore sequence |
| Communications Lead | Staff stand-down messages, customer and supplier holding messages, media holding statement |
| Data Protection Lead | Determines whether personal data was affected or taken, runs the 72-hour assessment |
| Executive Sponsor | Authorises shutting services, engaging external responders, and any ransom decision with legal advice |
| Scribe | Timeline and decision log on an unaffected system |
| Supplier liaison | Insurer notification line, incident response retainer, MSP, solicitors |

## 5. First 15 minutes

Goal: stop the spread and get the right people on a call. Do not start restoring anything yet.

1. **Note the time** you became aware. Start the [decision log](../comms/decision-log-template.md). This is also the start of the 72-hour assessment clock if personal data may be involved.
2. **Isolate, do not wipe.** Disconnect affected devices from the network (unplug cable, disable Wi-Fi, or use EDR network isolation). Prefer isolation to powering off, because memory evidence is lost on power-off. If encryption is visibly spreading and you cannot isolate fast enough, powering off is an acceptable decision: record it.
3. **Protect backups.** Disconnect backup repositories and consoles from the network, and disable scheduled jobs that could overwrite good restore points or expire them. Do not log in to backup consoles from a device that may be compromised.
4. **Move to out-of-band communication.** Stop using email and chat for incident coordination if identity may be compromised. Use the agreed phone tree and messaging group.
5. **Call the Incident Manager** and declare P1. Open the bridge.
6. **Tell staff to stop.** Short message: do not use the affected systems, do not shut down or reboot unless told, do not open ransom notes beyond taking a photograph, report anything odd. Template: [staff notice](../comms/staff-notice.md).
7. **Take photographs** of ransom notes and screens (phone camera is fine). Do not click links in a note or contact the attacker.
8. **Call the insurer's incident line and your incident response provider** if you have them. Many cyber policies require prompt notification and may require use of panel providers, so check the policy first (see decision points).

## 6. Containment

Aim for a controlled, evidence-preserving shutdown of the attacker's reach.

- [ ] Block known attacker indicators at the firewall, DNS filter and EDR as they are identified.
- [ ] Disable or isolate compromised accounts, especially privileged and service accounts. Work from a known clean administrative device.
- [ ] Segment: disable VPN or remote access if it is a suspected entry point, and cut inter-site links to unaffected offices if lateral movement is suspected.
- [ ] Pause or restrict synchronisation (Entra Connect or similar) if on-premises identity is suspected, so that attacker changes do not replicate to the cloud.
- [ ] Revoke Microsoft 365 sessions for suspected accounts and review risky sign-ins. See the [M365 account compromise playbook](m365-account-compromise-bec.md).
- [ ] Identify patient zero and the likely entry route (phishing, exposed remote access, vulnerable edge device, stolen credentials, supplier), using EDR timelines, VPN logs, mail trace and firewall logs.
- [ ] Check whether data left the network: unusual outbound volume, cloud storage uploads, archive tools, remote access tools.
- [ ] Keep a list of every system you isolate and why, so that you can later prove what was and was not touched.

Do not reboot, reimage or delete anything you cannot afford to lose as evidence until the Technical Lead and the Incident Manager agree (see evidence handling below).

## 7. Eradication

Eradication begins once the scope is understood well enough to be confident that removal will be complete. If the scope is uncertain, keep containing.

- Rebuild affected servers and endpoints from known-good images rather than "cleaning" them in place.
- Reset credentials in a safe order, from a clean device: privileged and service accounts first, then all users. In hybrid Active Directory environments, include resetting the KRBTGT account twice, with a replication wait between resets, if domain compromise is suspected. Follow the vendor guidance for your Active Directory version, and take specialist advice if unsure.
- Rotate secrets: API keys, certificates, local administrator passwords (LAPS), backup service credentials, VPN pre-shared keys, SaaS admin tokens.
- Remove persistence: new accounts, scheduled tasks, services, GPOs, remote access tools, OAuth app consents, mail forwarding rules.
- Patch or close the entry route before reconnecting anything. If the route is unknown, state that explicitly in the decision log and monitor closely.
- Confirm removal with EDR sweeps and log review for the indicators identified.

## 8. Recovery

Recover in the priority order set by your [business impact analysis](../dr/bia-template.md) and [RTO and RPO tiers](../dr/rto-rpo-tiers.md): foundation services (network, DNS, identity), then Tier 1 applications, and so on.

1. **Establish a clean room.** Rebuild identity and the management network first, on clean infrastructure. Do not reconnect restored systems to a network where the attacker may still have access.
2. **Validate backups before use.** Check that restore points pre-date the compromise, scan them for malware, and connect backup storage only to known clean systems. The NCSC makes the same point in its malware and ransomware guidance (see [references](../docs/references.md#ransomware-and-disruptive-attacks)).
3. **Restore to minimum viable operation first.** The NCSC recovery guidance describes recovering to "minimum viable operations" before a full rebuild. Agree what that means for each business area beforehand.
4. **Verify before release.** Each restored service is checked by a technical owner and a business owner, and signed off in the decision log. Record the actual recovery time and data loss against the RTO and RPO.
5. **Heightened monitoring** for at least 30 days: EDR alerting at high sensitivity, sign-in anomaly review, DNS and egress monitoring, and a daily review of any attacker-linked indicators.
6. **Return to business as usual** only after the Incident Manager records that eradication is confirmed and monitoring is in place.

Use manual workarounds (paper, offline spreadsheets, supplier portals, phone) for business continuity while systems are rebuilt, and write down what was done manually so it can be reconciled later.

## 9. Evidence handling

Keep evidence in a way that supports an insurer claim, a police investigation, and any regulator query.

- Start a **chain of custody** record for every item: what, from where, who collected it, when, how it was stored, who has accessed it.
- Prefer **forensic images** or EDR evidence collection to ad hoc copying. If you cannot image everything, prioritise patient zero, domain controllers, a representative file server, and firewall and VPN logs.
- **Preserve logs** before they roll over: firewall, VPN, EDR, Entra ID sign-in and audit logs, Microsoft Purview audit log, DNS, proxy, backup console logs. Export to a location the attacker cannot reach.
- **Do not wipe** compromised devices until evidence has been taken and the Incident Manager has agreed.
- **Photograph** ransom notes and screens. Record the attacker's contact details and wallet addresses exactly as shown, without making contact.
- Record all actions in the decision log with times in UTC or UK local time, stating which. Be consistent.
- If a specialist provider is engaged, follow their evidence instructions and let them lead forensic collection.

## 10. Communications

Use the templates in [comms](../comms/). Principles: be accurate, say what you know and do not know, say when you will update next, never speculate on cause or attacker identity.

| Audience | Template | Timing |
|---|---|---|
| All staff | [Staff notice](../comms/staff-notice.md) | Within the first hour, then at each update |
| Executive team and board | [Board update](../comms/board-update.md) | Within 1 hour (P1), then on the agreed cadence |
| Customers and partners | [Customer notice](../comms/customer-notice.md) | When service impact is confirmed, or earlier if they will notice |
| Regulator | [Regulator notification](../comms/regulator-notification.md) | Within the legal time limits, see section 11 |
| Media | [Media holding statement](../comms/media-holding-statement.md) | Only if enquiries arrive or the incident is public |

Staff should be told not to speak to the media or post on social media, and to send enquiries to the Communications Lead. Do not confirm the attacker's claims, and do not negotiate in public.

## 11. Regulatory and contractual notifications

Work through this list at the first decision point and again when scope is known. Record "not required" decisions and the reasoning, not only the notifications made.

| Who | When | Notes |
|---|---|---|
| Cyber insurer | As soon as possible, check policy conditions | Late notice or use of non-panel providers can affect cover. Check your own policy |
| ICO | Within 72 hours of becoming aware, if personal data is affected and the breach is likely to result in a risk to individuals | Phased reporting is allowed. Follow the [personal data breach playbook](personal-data-breach.md). Paying a ransom does not remove the duty to report |
| Affected individuals | Without undue delay if the breach is likely to result in a high risk to them | See the personal data breach playbook |
| NCSC | As soon as practicable | Report via the NCSC reporting service. Reports to the NCSC are not passed to the ICO, so report to both where relevant |
| Police / Report Fraud | Promptly | Report Fraud replaced Action Fraud in England, Wales and Northern Ireland on 4 December 2025. In Scotland, contact Police Scotland on 101 |
| Card acquirer or payment brands | If the cardholder data environment may be affected | Check the merchant agreement and PCI DSS incident response requirements |
| Customers and suppliers | As per contract clauses | Check notification clauses and SLAs for security incidents and data incidents |
| Customs or sector authorities | If you hold customs authorisations (for example AEO status) and declaration or record-keeping systems are affected | Check the conditions of your authorisations with your compliance lead. This repository does not state a specific duty |
| Lenders, auditors, certification body | If agreements require it | ISO 27001 certification bodies may expect to be told of significant incidents, check your contract |

Sources and links are in [references](../docs/references.md).

## 12. Decision points

Record each decision, who made it, the options considered and the time, in the decision log.

| # | Decision | Owner | Inputs |
|---|---|---|---|
| D1 | Declare P1 and open the bridge | Incident Manager | Triggers, initial scope |
| D2 | Power off versus isolate | Technical Lead | Spread speed, evidence need |
| D3 | Engage external incident response and insurer panel | Executive Sponsor | Cover terms, internal capability |
| D4 | Shut down business services proactively | Executive Sponsor | Technical advice, customer impact, safety |
| D5 | Ransom: pay or not pay | Executive Sponsor, with legal advice | NCSC guidance, backups, sanctions check, data theft, insurer position |
| D6 | Whether and when to notify the ICO and individuals | Data Protection Lead, Executive Sponsor | Data affected, risk assessment, 72-hour clock |
| D7 | Restore sequence and "minimum viable" definition | Incident Manager | BIA tiers, backup validity |
| D8 | When to declare eradication complete and return to BAU | Incident Manager | Scoping confidence, monitoring in place |

On D5: the NCSC states that law enforcement does not encourage, endorse or condone payment, that payment gives no guarantee of recovery, that payment may be unlawful if it goes to a sanctioned entity, and that paying does not remove regulatory obligations. The decision is the victim's. Take your time, get legal advice and keep a record. Details: [references](../docs/references.md#ransomware-and-disruptive-attacks).

## 13. Post-incident actions

Within 5 working days of stand-down, run a blameless [post-incident review](../comms/post-incident-review-template.md). Typical outputs:

- Root cause and contributing factors, with evidence.
- Whether backups, RTO and RPO assumptions held, recorded in the next [DR test report](../dr/dr-test-report-template.md).
- Control improvements with owners and dates: MFA coverage, privileged access separation, patching of edge devices, backup immutability and offline copy, EDR coverage, logging retention.
- Updates to this playbook, contact sheet and templates.
- Notifications closed out: ICO case updates, insurer, customers, auditors.
- Staff acknowledgement and any training changes.
- A repeat exercise using the [ransomware tabletop pack](../exercises/ransomware-tabletop/README.md) within 6 months.

## 14. Quick-reference checklist

Print this page. Tick as you go, and write times in the margin.

- [ ] Note the time of discovery and start the decision log
- [ ] Isolate affected devices from the network (do not wipe, avoid powering off)
- [ ] Disconnect backup repositories and consoles; pause backup expiry
- [ ] Move to out-of-band communication
- [ ] Call the Incident Manager; declare P1; open the bridge
- [ ] Tell staff to stop using affected systems (staff notice)
- [ ] Photograph ransom notes; do not contact the attacker
- [ ] Call insurer incident line and incident response provider
- [ ] Start the personal data assessment (72-hour clock)
- [ ] Identify entry route and scope; list every isolated system
- [ ] Disable compromised accounts from a clean device; revoke sessions
- [ ] Preserve logs and take forensic evidence; start chain of custody
- [ ] Brief the Executive Sponsor and board (board update template)
- [ ] Decide on external help, shutting services, and ransom (log each decision)
- [ ] Report to NCSC and police; notify ICO and others as assessed
- [ ] Rebuild identity first; validate backups; restore in BIA tier order
- [ ] Verify each service with business owner sign-off; monitor for 30 days
- [ ] Hold the blameless review within 5 working days
