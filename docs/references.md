# References

All factual and regulatory claims in this repository are based on the sources below. Links were checked on **4 November 2026**. Guidance changes, so check the current version before relying on it.

**Status key**

- **Read:** the page was retrieved and read for this repository on the date above.
- **Search only:** the page appeared in search results but its content was not read in full. Treat with more caution.
- **Not retrieved:** the page could not be retrieved. The claim it supports is stated from general knowledge and flagged in the notes.

This repository is not legal advice.

## Ransomware and disruptive attacks

| Source | Used for | Status |
|---|---|---|
| [NCSC: Mitigating malware and ransomware attacks](https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks) | Offline and separate backups, testing restores, scanning backups before restoring, connecting backups only to known clean devices, law enforcement does not encourage payment, reporting | Read |
| [NCSC: Guidance for organisations considering payment in ransomware incidents](https://www.ncsc.gov.uk/guidance/organisations-considering-payment-in-ransomware-incidents) | Payment decision factors, sanctions risk, payment does not meet regulatory obligations, keeping decision records on unaffected systems, data theft in most incidents | Read |
| [NCSC: Ransomware attack (respond and recover)](https://www.ncsc.gov.uk/section/respond-recover/ml-ransomware-attack) | Triage between disruptive and other incidents, links to response guidance and assured providers | Read |
| [NCSC: Disruptive cyber attacks (collection)](https://www.ncsc.gov.uk/collection/disruptive-cyber-attacks) | Structure of preparing, reducing risk and recovering from highly disruptive attacks | Read |
| [NCSC: Recovering from a highly disruptive cyber attack](https://www.ncsc.gov.uk/collection/disruptive-cyber-attacks/recovering) | Immediate activities, recovery to minimum viable operations, rebuild | Read (structure and summary) |
| [NCSC: Incident management (collection)](https://www.ncsc.gov.uk/collection/incident-management) | Plan, build, develop and maintain an incident response capability; link to DR, BCP and crisis plans | Read |
| [NCSC: Small Business Guide, Response and Recovery](https://www.ncsc.gov.uk/collection/small-business-guidance--response-and-recovery) | Five-step structure (prepare, identify, resolve, report, learn). States 0300 123 2040 for a live attack in progress | Read (landing page only) |
| [NCSC: Cyber Incident Response scheme](https://www.ncsc.gov.uk/schemes/cyber-incident-response) | NCSC-assured incident response providers | Read |

## Denial of service

| Source | Used for | Status |
|---|---|---|
| [NCSC: Denial of Service (DoS) guidance collection](https://www.ncsc.gov.uk/collection/denial-service-dos-guidance-collection) | Four practices: understand your service, understand your defences, create a response plan, test your response. Definition of DoS impact | Read (landing page) |

The sub-pages (upstream defences, scaling, response plan, testing and monitoring, responding to a DoS attack) were not read in full. The DDoS playbook's specific containment steps are common practice, not quotations from the NCSC.

## Data protection and the ICO

| Source | Used for | Status |
|---|---|---|
| [ICO: Personal data breaches, a guide](https://ico.org.uk/for-organisations/guide-to-dp/guide-to-the-uk-gdpr/personal-data-breaches) | Report when a risk to individuals is likely, 72 hours from awareness, phased reporting, notification content, tell individuals if high risk, record all breaches, processors notify controllers without undue delay | Read |
| [ICO: 72 hours, how to respond to a personal data breach (SME web hub)](https://ico.org.uk/for-organisations/sme-web-hub/72-hours-how-to-respond-to-a-personal-data-breach) | Practical steps, clock runs from discovery, reporting with missing details then following up, self-assessment tool, advice line | Read |
| [ICO: Report a personal data breach](https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach/) | Reporting by online form or by phone (0303 123 1113, opening hours stated on the page) | Read |
| [UK GDPR, Articles 33 and 34 on legislation.gov.uk](https://www.legislation.gov.uk/eur/2016/679/article/33) | The legal text for notification. "not later than 72 hours after having become aware of it" | Read. The page notes amendments to wording over time, so check the current consolidated text. Rely on the ICO guidance for working use |

The ICO phone line hours and the structure of its guidance may change. Check before relying on them. This repository does not state the penalty regime or any enforcement statistics.

## Reporting routes

| Source | Used for | Status |
|---|---|---|
| [GOV.UK: Report a cyber incident](https://www.gov.uk/report-cyber) | Signposting to the NCSC and, for personal data breaches, the ICO. States that information given to the NCSC is not shared with the ICO | Read |
| [NCSC: Report an incident](https://www.ncsc.gov.uk/report-an-incident) and [report.ncsc.gov.uk](https://report.ncsc.gov.uk/) | Online incident reporting service for organisations. No phone line for organisations was listed on the page | Read |
| [Report Fraud: service goes live](https://www.reportfraud.police.uk/news/report-fraud-service-goes-live/) | Report Fraud replaced Action Fraud for England, Wales and Northern Ireland on 4 December 2025. Phone 0300 123 2040. Scotland is excluded: Police Scotland on 101 | Read |

**Note on Action Fraud:** many older documents still refer to Action Fraud. This repository uses Report Fraud, and uses "Police Scotland on 101" for Scotland.

## Microsoft 365 and endpoint management

| Source | Used for | Status |
|---|---|---|
| [Microsoft Learn: Responding to a compromised email account](https://learn.microsoft.com/en-gb/defender-office-365/responding-to-a-compromised-email-account) | Disable account, revoke sessions (`Revoke-MgUserSignInSession`), review MFA methods, app consents, admin roles, forwarding and inbox rules, audit logs, remove from the Restricted entities page | Read |
| [Microsoft Learn: Wipe devices with Microsoft Intune](https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe) | Wipe action, platform behaviour, tenant daily limit, cleanup after wipe | Read |

The PowerShell in the BEC playbook is based on the first page for disabling, revoking sessions and checking forwarding and inbox rules. These commands were **not executed** in a tenant for this repository. Test all commands before relying on them. Other actions named in the playbooks (delegate review, mail flow rule review, Conditional Access review, Intune lock and locate actions) are described in general terms and should be confirmed against current Microsoft documentation.

## Supply chain and suppliers

| Source | Used for | Status |
|---|---|---|
| [NCSC: Supply chain security guidance](https://www.ncsc.gov.uk/guidance/supply-chain-security) | Supplier risk framework: understand the risks, establish control, check arrangements, continuous improvement. Cyber Essentials as supplier assurance | Read (landing page) |

## Exercising

| Source | Used for | Status |
|---|---|---|
| [NCSC: Exercise in a Box](https://www.ncsc.gov.uk/section/exercise-in-a-box/overview) | Free online tool with ransomware, phishing, supply chain and other exercises, in micro and tabletop formats | Read |
| [NCSC: Cyber Incident Exercising scheme](https://www.ncsc.gov.uk/schemes/cyber-incident-exercising/information-for-buyers) | NCSC-assured exercise providers | Search only |

## Standards and audit

| Source | Used for | Status |
|---|---|---|
| [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) | Annex A incident management and continuity controls referenced in the [audit mapping](audit-mapping.md) | Not retrieved. Control names are from the published 2022 control set and from secondary summaries. Check the standard itself |
| [PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/) | PCI DSS v4.0.1, including requirement 12.10 on incident response, referenced in the audit mapping | Library page read. The requirement text was **not** read in the standard. Wording is from secondary summaries, so check it |
| Secondary summaries used to confirm control and requirement names: [ISMS.online Annex A 5.24](https://www.isms.online/iso-27001/annex-a-2022/5-24-incident-management-planning-and-preparation-2022/), [Annex A 5.26](https://www.isms.online/iso-27001/annex-a-2022/5-26-response-to-information-security-incidents-2022/), [Annex A 5.27](https://www.isms.online/iso-27001/annex-a-2022/5-27-learning-from-information-security-incidents-2022/), [PCI DSS 12.10 summary](https://ce.prod.cloudaware.com/frameworks/pci-dss-v4.0/12/10/) | Cross-checking names only | Search only |

## Claims in this repository that rest on general practice, not on a cited source

These are common professional practice and are marked as such where they appear. Review them for your environment.

- Isolating before powering off to preserve volatile evidence.
- Resetting the KRBTGT account twice in hybrid Active Directory compromise (follow the vendor's current guidance).
- Suggested internal checkpoints during the 72-hour period, the response-time targets in the [severity model](severity-model.md), and the tier values in the [tier table](../dr/rto-rpo-tiers.md).
- The 3-2-1 backup rule of thumb.
- The UK police non-emergency number (101) and obtaining a crime reference for theft.
- Typical device wipe, lock and token revocation sequence for lost devices, apart from the Intune wipe behaviour cited above.
- Customs, AEO or other sector-authority notification duties. This repository **does not** state a specific duty. Check your own authorisation conditions.
- Insurer notification requirements, which depend on your policy.
- Card scheme and acquirer notification requirements, which depend on your merchant agreement.

## Not included on purpose

No breach statistics, cost figures, case studies or fine amounts are quoted, because they date quickly and would need their own sources. The example company, systems and numbers in the BIA, tabletop and templates are fictional.
