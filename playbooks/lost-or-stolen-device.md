# Playbook: Lost or stolen device

| Field | Value |
|---|---|
| Version | 1.0 |
| Owner | IT Manager |
| Last reviewed | 2026-11-04 |
| Review cycle | At least every 12 months, and after every real incident or exercise |
| Related | [Personal data breach](personal-data-breach.md), [M365 account compromise](m365-account-compromise-bec.md), [Severity model](../docs/severity-model.md) |

> This playbook is operational guidance, not legal advice. Device management capabilities vary by platform, licence and configuration, so test every action here on a spare device before you need it.

## 1. Purpose

To limit harm when a laptop, phone, tablet, security key, removable drive or other company-issued or personally owned (BYOD) device that holds or can access business data is lost or stolen. The two questions that decide everything are: is the data on it protected, and can the device still reach company systems?

## 2. Triggers

- A staff member reports a device lost, stolen, left in a taxi, or confiscated.
- A device is missing at the end of a shift, at a site audit, or after a break-in.
- A device has not checked in to device management for an unexpected period.
- A delivery or courier loses a shipment of devices.
- A staff member leaves a bag with several devices unattended.

Staff should report immediately, including out of hours, and without fear of blame. A quick report is worth more than a perfect one.

## 3. Severity matrix

| Level | Examples |
|---|---|
| P1 Critical | Unencrypted device with sensitive or large volumes of personal data; privileged administrator device or security key; device with persistent access (VPN, saved sessions) to critical systems; theft linked to a targeted attack |
| P2 High | Managed, encrypted device with some business data or active sessions, not yet confirmed remote-wiped; phone with email and company apps |
| P3 Medium | Encrypted, PIN-protected, managed device with no local data (cloud only), sessions revoked and wipe or lock confirmed |
| P4 Low | Device found and returned unopened; spare device with no data or access |

Use the [shared severity model](../docs/severity-model.md) for response targets.

## 4. Roles

| Role | Duties |
|---|---|
| Incident Manager | Usually the IT Manager. Decides severity, and escalates to P1 if personal data or privileged access is involved |
| Technical Lead | Remote lock, wipe, session revocation, certificate and token revocation |
| Data Protection Lead | Assesses the personal data impact, see [personal data breach playbook](personal-data-breach.md) |
| Communications Lead | Staff reminders, and customer notices if needed |
| Line manager | Gets the facts from the user, supports the person, arranges a replacement |
| Facilities or security lead | For thefts from premises: CCTV, access logs, police liaison |

## 5. First 15 minutes

1. **Take the report** and record: who, which device (asset tag, serial, IMEI), when and where it was last seen, how it was lost, whether it was locked, and whether there is anything sensitive on it.
2. **Check device management**: last check-in, encryption status, user, compliance state, enrolled apps.
3. **Revoke access first.** Revoke the user's Entra ID sessions and refresh tokens, and remove the device from trusted or compliant sets so that Conditional Access blocks it. A remote wipe may remain pending until the device is online, but token revocation takes effect straight away.
4. **Lock the device** and display a return message if the platform supports it.
5. **Issue a remote wipe** when the data is sensitive, encryption cannot be confirmed, or the device is stolen rather than misplaced. Keep a record of the time and the status. Retire (remove company data only) is suitable for personally owned devices.
6. **Reset passwords** for any accounts that were saved or cached on the device, and rotate secrets stored there.
7. **Tell the Incident Manager** and open the [decision log](../comms/decision-log-template.md). If personal data may be involved, tell the Data Protection Lead now.

Example actions in Microsoft Intune (names vary by portal version, check current documentation, see [references](../docs/references.md#microsoft-365-and-endpoint-management)): Wipe, Retire, Lock (where available), Locate (supervised devices where available), and Remote lock. Intune caps the daily number of wipe actions per tenant, which matters only in mass incidents.

## 6. Containment

- [ ] User sessions and tokens revoked; sign-in logs checked for use since the loss.
- [ ] Device marked non-compliant or blocked in Conditional Access.
- [ ] Wipe or retire issued and the status monitored. If the device does not check in, the wipe stays pending, so record that the device was not confirmed wiped.
- [ ] Certificates, VPN profiles, Wi-Fi profiles and device certificates revoked or removed.
- [ ] Saved credentials and keys on the device rotated: browser-saved passwords, SSH keys, API tokens, shared mailbox passwords.
- [ ] Security keys or tokens (FIDO2, smartcards) removed from the user's account; hardware lost with the device.
- [ ] SIM barred by the mobile provider if the device is a phone, to prevent SMS interception and call fraud.
- [ ] Removable media inventory checked: what data was on any lost drive?
- [ ] For theft from premises, preserve CCTV and access records and report to the police.

## 7. Eradication

- Confirm the device is wiped or that the device can no longer authenticate. Remove the device record from Entra ID, Autopilot and device management only after the wipe is confirmed, or after you decide to accept the residual risk and record it.
- If a wiped device is recovered, treat it as untrusted: do not reconnect it. Reimage or replace.
- Assess whether the loss hides a targeted attack: look for sign-in attempts from unfamiliar locations after the loss, unusual password reset requests, and attempts to access cloud storage.
- Verify that data could not be recovered: full disk encryption enabled (BitLocker on Windows, FileVault on macOS, default encryption on modern iOS and Android) and the encryption key is held in the directory and not with the device.

## 8. Recovery

- Issue a replacement device, enrol it, and restore the user's data from cloud services or backup.
- Reissue MFA methods and security keys, and re-register devices with identity verification of the user.
- Update the asset register to show the device as lost, stolen or recovered, with dates.
- Confirm that the user can work and that the replaced access is complete.
- If the device is later found, return it to IT for inspection, do not reuse it directly.

## 9. Evidence handling

- Keep the user's report, the device record, encryption status screenshot, and the timeline of IT actions (token revocation, lock, wipe) with times.
- Record the **police crime reference number** for insurance and audit. Non-emergency thefts can normally be reported to the police on 101, and online in some areas, so check your local force.
- Preserve CCTV, door access logs and visitor logs for thefts from premises, and hand them to the police on request.
- Preserve sign-in logs for the user and device after the loss.
- If the device had sensitive data and no encryption, keep documentation that explains what data it held, as it feeds the breach assessment.

## 10. Communications

| Audience | Notes |
|---|---|
| The user | Calm, supportive, thank them for reporting quickly. No blame |
| Line manager | Facts, actions and replacement plan |
| All staff | Occasional reminder via the [staff notice](../comms/staff-notice.md): report immediately, do not leave devices in vehicles, use privacy screens, lock screens |
| Customers | Only if their personal data may be at risk, using the [customer notice](../comms/customer-notice.md) after the [personal data breach assessment](personal-data-breach.md) |
| Police | Provide device identifiers and last-known location |

## 11. Regulatory and contractual notifications

| Who | When |
|---|---|
| ICO | If the device held personal data that was not adequately protected and the breach is likely to result in a risk to individuals, within 72 hours of becoming aware. Encryption that is strong and with keys secure is a key factor in the assessment. Follow the [personal data breach playbook](personal-data-breach.md) |
| Individuals | If a high risk to them exists |
| Police | Report thefts. Obtain a crime reference |
| Insurer | For theft claims and where cyber cover may respond |
| Customers | Where contract requires notice of device loss involving their data |
| Card acquirer | Where cardholder data may have been on the device, check merchant agreements and PCI DSS incident response procedures |

## 12. Decision points

| # | Decision | Owner |
|---|---|---|
| D1 | Wipe or retire now, or wait for a short recovery window | Technical Lead, with the user's manager |
| D2 | Was the device encrypted and was the key safe? Document the evidence | Technical Lead |
| D3 | Is personal data involved and is a breach report needed? | Data Protection Lead |
| D4 | Does the loss indicate a targeted attack? Escalate to the [account compromise playbook](m365-account-compromise-bec.md)? | Incident Manager |
| D5 | Notify police and insurer | Incident Manager |
| D6 | Issue a replacement and when | Line manager and IT |

## 13. Post-incident actions

- Short blameless review, with the user included where appropriate.
- Confirm full-disk encryption coverage across the estate, with a monthly report of any exceptions.
- Review device compliance policy: screen lock timeout, PIN complexity, auto-wipe after repeated failed attempts where supported, Conditional Access requiring compliant devices.
- Review travel and storage guidance: do not leave devices in vehicles, use cable locks and privacy screens, carry only what is needed.
- Review how fast people report. Treat slow reporting as a process problem and fix it.
- Reconcile the asset register.
- Update this playbook if remote actions did not work as described.

## 14. Quick-reference checklist

- [ ] Record who, what device, when, where, how, and whether it was locked
- [ ] Check device management: encryption, last check-in, enrolled apps
- [ ] Revoke the user's sessions and tokens; block the device in Conditional Access
- [ ] Lock the device; issue wipe (corporate) or retire (BYOD)
- [ ] Reset passwords and rotate secrets saved on the device
- [ ] Bar the SIM if it is a phone
- [ ] Remove lost security keys from the account
- [ ] Report theft to the police and note the crime reference number
- [ ] Check sign-in logs for use since the loss
- [ ] Assess personal data: encrypted? how much? which people?
- [ ] Notify the Data Protection Lead; start the 72-hour clock if a breach is likely
- [ ] Issue a replacement; restore data; update the asset register
- [ ] Record outcome and lessons
