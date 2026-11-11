# Disaster recovery plan template

How to use: copy this file, replace every `{{field}}`, delete guidance in italics when you are done, and store the finished plan where it can be reached when your main systems are down (printed copy, offline copy, second tenant). Keep it short enough that it will be read. Attach detailed technical runbooks as appendices.

> This template is generic guidance and not legal advice. It does not replace contractual, insurance or regulatory requirements that apply to your organisation.

## 1. Document control

| Field | Value |
|---|---|
| Organisation | {{company name}} |
| Plan owner | {{role, for example IT Manager}} |
| Approved by | {{executive sponsor role}} |
| Version and date | {{version}}, {{date}} |
| Next review | {{date, at least every 12 months}} |
| Distribution | {{who holds copies, including offline copies}} |
| Related documents | [BIA](bia-template.md), [RTO and RPO tiers](rto-rpo-tiers.md), [Dependency map](dependency-map.md), [Playbooks](../playbooks/README.md) |

## 2. Purpose and scope

*State what this plan covers and what it does not.*

- Purpose: to restore {{services}} within the recovery objectives agreed in the BIA following a disruption such as {{ransomware, loss of a site, loss of a data centre or cloud region, extended supplier outage, loss of identity services}}.
- In scope: {{systems, sites, data, suppliers}}.
- Out of scope: {{for example business continuity arrangements for staff accommodation, covered in the BCP}}.
- Assumptions: {{for example backups are intact, key staff can be reached, internet is available}}.

## 3. Invocation: when does DR start?

DR is invoked when an incident has made, or will make, a service unavailable for longer than its RTO, or when a site or platform is lost.

| Item | Detail |
|---|---|
| Authority to invoke | {{role, deputy}} |
| Criteria | {{for example any T0 or T1 service unavailable for more than 60 minutes with no fix in sight}} |
| How invoked | Incident Manager declares in the [decision log](../comms/decision-log-template.md) and notifies the DR team via {{out-of-band channel}} |
| Standing down | Incident Manager, after business owners sign off |

Link to the incident: DR is the recovery stage of the incident response playbooks. For a cyber incident, containment and eradication come first, so that you do not restore into a compromised environment (see the [ransomware playbook](../playbooks/ransomware.md)).

## 4. Roles and contacts

| Role | Primary | Deputy | Responsibilities |
|---|---|---|---|
| DR Manager | {{name}} | {{name}} | Leads recovery, owns priorities |
| Infrastructure recovery lead | {{name}} | {{name}} | Network, servers, identity, backup restore |
| Application recovery lead | {{name}} | {{name}} | Line-of-business apps and integrations |
| Business recovery representative | {{name}} | {{name}} | Business validation and workarounds |
| Communications Lead | {{name}} | {{name}} | Staff, customer and supplier updates |
| Supplier liaison | {{name}} | {{name}} | MSP, vendors, ISPs |

Full contact details are on the [contact sheet](../comms/contact-sheet-template.md).

## 5. Recovery objectives and priorities

| Tier | RTO | RPO | Services in this tier |
|---|---|---|---|
| T0 Foundation | {{from tier table}} | {{from tier table}} | {{list}} |
| T1 Critical | {{}} | {{}} | {{list}} |
| T2 Important | {{}} | {{}} | {{list}} |
| T3 Standard | {{}} | {{}} | {{list}} |
| T4 Deferrable | {{}} | {{}} | {{list}} |

Recovery order: T0 first, then T1, and so on, within the limits of dependencies in the [dependency map](dependency-map.md). Where a service has a minimum viable operation (MVO) definition, recover to MVO first.

## 6. Recovery strategy per service

*One row per service, derived from the BIA. Detailed procedures go in appendices.*

| Service | Tier | Recovery strategy | Backup source and location | Last successful restore test | Runbook | Owner |
|---|---|---|---|---|---|---|
| {{Identity}} | T0 | {{rebuild domain controller from backup, restore Entra Connect}} | {{backup tool, immutable copy, offline copy}} | {{date}} | {{link}} | {{role}} |
| {{Network and internet}} | T0 | {{failover circuit, firewall config restore}} | {{config backup location}} | {{date}} | {{link}} | {{role}} |
| {{Service}} | {{T}} | {{}} | {{}} | {{}} | {{}} | {{}} |

## 7. Backup arrangements

| Item | Standard to meet |
|---|---|
| Method | Follow the 3-2-1 idea as a minimum: at least three copies, on two types of storage, with one offsite. Add an immutable or offline copy that an attacker with administrative credentials cannot delete |
| Coverage | Servers, databases, Microsoft 365 (mail, SharePoint, OneDrive, Teams) via a separate backup, SaaS data exports, network configuration, directory and identity configuration, encryption keys and certificates |
| Frequency | Matches the RPO of each tier |
| Retention | {{days, with a rationale linked to legal and operational needs}} |
| Access | Backup administration accounts separate from daily admin accounts, with MFA, and not synchronised with the main identity system where possible |
| Monitoring | Daily job status review, with alerting on failure |
| Testing | Restore tests per the tier table, logged in the [backup and restore test log](backup-restore-test-log.md) |

## 8. Alternative working arrangements

| Scenario | Arrangement |
|---|---|
| Office unusable | {{work from home, other site, serviced office}} |
| Network down | {{mobile hotspots, secondary circuit}} |
| Identity down | {{break-glass accounts, manual access for T1 apps}} |
| Email down | {{secondary communication channel, off-network contact list}} |
| Key supplier down | See the [supplier outage playbook](../playbooks/saas-supplier-outage.md) |

## 9. Communications during DR

| Audience | Who | How | Frequency |
|---|---|---|---|
| Staff | Communications Lead | {{out-of-band channel}} | {{every x hours}} |
| Customers | Communications Lead | {{status page, email}} | {{}} |
| Executive team and board | Incident Manager | {{call, board update}} | {{}} |
| Suppliers and MSP | Supplier liaison | {{phone}} | {{}} |

Templates are in [comms](../comms/).

## 10. Recovery procedures (outline)

*Each service gets a runbook with these headings. Write them so that a competent person who did not build the system can follow them.*

1. Preconditions and dependencies.
2. Where backups and credentials are, and how to access them with the main systems down.
3. Step-by-step restore or rebuild, with expected durations.
4. Validation tests, including a named business user for sign-off.
5. Data reconciliation after restore (what could have been lost between the RPO point and the failure).
6. Rollback if the restore fails.
7. Hand-back to business as usual.

## 11. Return to normal

- Confirm the root cause is resolved and the environment is clean.
- Reconcile data and manual records.
- Reinstate backup jobs and monitoring for recovered systems, and take a fresh full backup.
- Review security configuration of recovered systems before they return to production.
- Hold a blameless [post-incident review](../comms/post-incident-review-template.md).

## 12. Testing and maintenance

| Activity | Frequency | Evidence |
|---|---|---|
| Backup restore tests | Per tier | [Test log](backup-restore-test-log.md) |
| Full DR test or exercise | At least annually, tier 0 and 1 services | [DR test report](dr-test-report-template.md) |
| Tabletop exercise | At least annually | [Exercise pack](../exercises/ransomware-tabletop/README.md) |
| Plan review | At least annually and after any major change | Version history |
| Contact sheet check | Quarterly | Date of last check |
| BIA review | Annually | Signed-off BIA |

## 13. Appendices

- A. Contact sheet.
- B. Service runbooks.
- C. Dependency map.
- D. Supplier and contract summary (incident contacts, SLAs, notice periods).
- E. Backup inventory.
- F. Network diagrams and IP plan.
- G. Licence keys and escrow details (stored securely).
