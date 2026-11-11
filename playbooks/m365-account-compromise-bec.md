# Playbook: Microsoft 365 account compromise and business email compromise

| Field | Value |
|---|---|
| Version | 1.0 |
| Owner | IT Manager |
| Last reviewed | 2026-11-04 |
| Review cycle | At least every 12 months, and after every real incident or exercise |
| Related | [Personal data breach](personal-data-breach.md), [Ransomware](ransomware.md), [Lost or stolen device](lost-or-stolen-device.md), [Severity model](../docs/severity-model.md) |

> This playbook is operational guidance, not legal advice. Commands shown are examples to adapt and test in your tenant before an incident, and should be checked against current Microsoft documentation, which changes often.

## 1. Purpose

To contain and investigate a compromised Microsoft 365 or Entra ID account, and to stop or recover from business email compromise (BEC): fraudulent emails sent from a genuine or spoofed business account to trick staff, customers or suppliers into paying money, changing bank details or sharing data.

It covers: phished credentials, session or token theft, malicious OAuth app consent, mailbox rules used to hide or forward messages, and payment diversion fraud.

## 2. Triggers

- A user reports a phishing message they clicked, or credentials they entered on a fake page.
- Impossible-travel, unfamiliar location or risky sign-in alerts; MFA fatigue (repeated prompts the user did not trigger).
- Mailbox rules that forward, redirect or delete messages that the user did not create.
- Staff, customers or suppliers receive unexpected messages from the account, or replies to messages the user did not send.
- A supplier or customer reports changed bank details, an unusual invoice or a payment request that came from "us".
- Microsoft Defender or Entra ID Protection raises compromised-user or suspicious-mailbox-activity alerts.
- A payment has already been made to new or changed bank details, which is a financial emergency as well as a security incident.

## 3. Severity matrix

Targets are in the [shared severity model](../docs/severity-model.md).

| Level | Examples |
|---|---|
| P1 Critical | Privileged or finance-approver account compromised; money already sent; many mailboxes affected; data exfiltration from mailboxes or SharePoint; attacker has OAuth persistence |
| P2 High | Single standard user compromised and used to send phishing or access data; mailbox rules found; no payment made |
| P3 Medium | Credentials entered on a phishing page but no sign-in by the attacker, password reset and session revocation completed quickly |
| P4 Low | Phishing received, not clicked, reported and removed |

If a payment has left the bank, treat as P1 regardless of the technical scope.

## 4. Roles

Standard roles are defined in the [severity model](../docs/severity-model.md#standard-roles).

| Role | BEC-specific duties |
|---|---|
| Incident Manager | Coordinates technical containment and the finance response in parallel |
| Technical Lead | Account containment, audit log review, tenant-wide hunting for the same indicators |
| Finance lead | Contacts the bank, freezes or recalls payments, verifies supplier details by independent call |
| Communications Lead | Notifies affected customers and suppliers, and warns staff |
| Data Protection Lead | Assesses whether mailbox content included personal data, see the [personal data breach playbook](personal-data-breach.md) |
| Executive Sponsor | Authorises financial recovery actions and external reporting |

## 5. First 15 minutes

1. **Note the time** and start the [decision log](../comms/decision-log-template.md).
2. **If money has moved, call the bank first.** Ask the fraud team to recall or freeze the payment and to flag the receiving account. Speed matters, so do this in parallel with technical steps, not after them. Note the call reference.
3. **Disable the account** (preferred) or reset the password from an admin session. Use a strong unique password and do not email it. Microsoft's guidance is to disable the account where possible, and to reset twice for directory-synchronised accounts.
4. **Revoke sessions and refresh tokens** so the attacker is signed out everywhere.
5. **Check MFA methods** registered to the account and remove any the user does not recognise.
6. **Check for forwarding and hidden inbox rules** and remove them.
7. **Tell the Incident Manager** and open a bridge if P1 or P2. Stop using the compromised account for any communication.
8. **Warn the finance team** by phone: no changes to bank details and no urgent payments without call-back verification.

Example PowerShell (Microsoft Graph and Exchange Online), run from an admin device. Adapt, test in advance and confirm against [Microsoft's compromised account guidance](../docs/references.md#microsoft-365-and-endpoint-management):

```powershell
# Disable the account and revoke sign-in sessions
Update-MgUser -UserId user@example.com -AccountEnabled:$false
Revoke-MgUserSignInSession -UserId user@example.com

# Forwarding configured on the mailbox
Get-Mailbox -Identity user@example.com | Format-List ForwardingAddress,ForwardingSmtpAddress,DeliverToMailboxAndForward

# Inbox rules, including hidden ones
Get-InboxRule -Mailbox user@example.com -IncludeHidden |
  Format-List Name,Enabled,RedirectTo,ForwardTo,ForwardAsAttachmentTo,DeleteMessage
```

## 6. Containment

- [ ] Account disabled or password reset; all sessions and refresh tokens revoked.
- [ ] MFA methods reviewed; unrecognised methods and devices removed. Re-register only after the user is verified in person or by video.
- [ ] Application consents reviewed: remove OAuth apps the user or an admin did not approve. Malicious consent survives a password reset.
- [ ] Administrative roles reviewed: remove any unexpected role assignments (Entra roles, Exchange roles, SharePoint admin).
- [ ] Mailbox checked for forwarding, inbox rules, delegates (Full Access, Send As, Send on Behalf) and calendar sharing changes.
- [ ] Tenant-level mail flow rules and connectors checked for new rules created by the attacker.
- [ ] Sent Items and Deleted Items reviewed. Malicious messages purged from recipients' mailboxes using Defender for Office 365 or Exchange search and purge, after preserving a copy as evidence.
- [ ] Blocklist attacker sender domains, IP addresses and URLs in mail filtering and DNS filtering.
- [ ] Conditional Access checked for exclusions or policies the attacker could have altered.
- [ ] Search sign-in logs for the same IP addresses, user agents or app IDs across **all** users, to find other compromised accounts.

## 7. Eradication

- Complete investigation of sign-in and audit logs (Entra ID sign-in and audit logs, Microsoft Purview audit log, message trace) from before the first suspicious activity.
- Remove all attacker-created artefacts: rules, delegates, apps, MFA methods, device registrations, shared links, mail flow rules.
- Reset passwords for any other account whose credentials may have been exposed, such as accounts that share the same password or were reachable from the same phishing campaign.
- Confirm the entry route: phishing link and kit, token theft (adversary-in-the-middle), legacy authentication, password spray, reused credentials. Close it: block legacy authentication, enforce MFA, move to phishing-resistant methods for administrators and finance approvers.
- Check endpoint of the user for infostealer or remote access tools; reimage if in doubt. See the [ransomware playbook](ransomware.md) for scoping if malware is found.

## 8. Recovery

1. Re-enable the account only after the account is clean, credentials are reset and MFA is re-registered with the verified user. If the account was used to send spam, remove it from the Restricted entities page.
2. Restore any deleted content from the recoverable items folder or backup if the attacker deleted mail or files.
3. Reverse fraudulent changes: supplier bank details, invoice approvals, remittance instructions. Re-verify every changed supplier record by calling a known number from a trusted source, not the number in the email.
4. If a payment was made, follow bank and Report Fraud processes, and keep the recall request and bank reference in the decision log.
5. Monitor the account and the user for 30 days: sign-ins, rule creation, consent grants.
6. Confirm to affected customers and suppliers that the issue is resolved and how to verify genuine communications in future.

## 9. Evidence handling

- Export the **audit logs and sign-in logs** to a safe location before they age out. Retention differs by licence, so check yours now rather than during an incident.
- Preserve **original phishing messages** with full headers (export as .eml or .msg). Do not forward them in a way that changes the headers.
- Preserve a **message trace** and copies of malicious messages before purging them.
- Record **screenshots** of rules, delegates, app consents and MFA methods before removal.
- Record the **timeline** of the attacker's activity from first sign-in to containment, with IP addresses, user agents and applications.
- Keep **bank and payment evidence**: instruction emails, invoices, payment references, bank call references.
- Maintain a chain of custody record for anything that may be passed to the police or an insurer.

## 10. Communications

| Audience | Template | Notes |
|---|---|---|
| Affected user | Direct, supportive call. It is a blameless process, people who report quickly should be thanked | Verify identity before sharing sensitive details |
| All staff | [Staff notice](../comms/staff-notice.md) | Describe the lure, ask people to report similar messages, remind them about call-back verification for payment changes |
| Recipients of fraudulent messages | [Customer notice](../comms/customer-notice.md) | Short, factual, tells them to disregard and report, and how to confirm genuine requests |
| Board | [Board update](../comms/board-update.md) | For P1, or when money is lost |

Do not use the compromised mailbox to send the warning. Use another channel or a fresh account.

## 11. Regulatory and contractual notifications

| Who | When | Notes |
|---|---|---|
| Bank | Immediately if funds moved | Fraud team. Record the reference |
| Report Fraud | Promptly if fraud occurred | Replaced Action Fraud in England, Wales and Northern Ireland on 4 December 2025. In Scotland, Police Scotland on 101 |
| NCSC | If significant, or part of a wider campaign | Report via the NCSC reporting service |
| ICO | Within 72 hours of becoming aware if personal data was exposed and the breach is likely to result in a risk to individuals | Mailboxes and files often contain personal data. Follow the [personal data breach playbook](personal-data-breach.md) |
| Cyber or crime insurer | Promptly | Funds-transfer fraud and social engineering cover varies. Check the policy |
| Customers and suppliers | If their data or payments were affected, or they were targeted from your account | Check contract clauses |
| Microsoft | If you need support on a tenant-level incident | Use your support channel |

## 12. Decision points

| # | Decision | Owner |
|---|---|---|
| D1 | Disable versus reset the account (disabling is preferred when feasible) | Technical Lead |
| D2 | Whether a payment recall or bank freeze is needed now | Finance lead with Incident Manager |
| D3 | Whether to force password reset and re-registration for a wider group | Incident Manager |
| D4 | Whether other mailboxes are affected and need the same treatment | Technical Lead |
| D5 | Whether personal data is involved and the ICO clock starts | Data Protection Lead |
| D6 | Whether to notify customers or suppliers who received malicious messages | Communications Lead, Executive Sponsor |
| D7 | Whether to engage a specialist provider (tenant-wide compromise, privileged accounts) | Executive Sponsor |

## 13. Post-incident actions

- Blameless [post-incident review](../comms/post-incident-review-template.md) within 5 working days.
- Control improvements, with owners and dates: enforce MFA, move admins and finance approvers to phishing-resistant MFA, block legacy authentication, restrict user consent to apps, enable alerting for new forwarding rules and mailbox delegations, tighten Conditional Access, review audit log retention.
- Process improvements: mandatory call-back verification for any change to bank details, dual authorisation above an agreed payment threshold, a standing contact list for supplier verification.
- Phishing awareness refresh using the real (anonymised) lure.
- Update this playbook and the PowerShell snippets after testing them.

## 14. Quick-reference checklist

- [ ] Note the time; start the decision log
- [ ] Money moved? Call the bank fraud team now and note the reference
- [ ] Disable the account (or reset password); revoke all sessions
- [ ] Remove unknown MFA methods, app consents and admin roles
- [ ] Remove forwarding, hidden inbox rules, delegates
- [ ] Check tenant mail flow rules and Conditional Access for tampering
- [ ] Search logs for the same indicators on all other accounts
- [ ] Purge malicious messages from recipients after preserving copies
- [ ] Warn finance and staff by phone or another channel; require call-back verification
- [ ] Preserve audit logs, message trace, original phishing email
- [ ] Assess personal data exposure; start 72-hour clock if relevant
- [ ] Report to Report Fraud (or Police Scotland), insurer and NCSC as needed
- [ ] Re-enable only after clean, reset and re-registered MFA
- [ ] Monitor for 30 days; run the blameless review
