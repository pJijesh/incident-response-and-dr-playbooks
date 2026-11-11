# Participant handout: ransomware tabletop

**EXERCISE ONLY. Everything in this document is fictional.**

## What this is

A 2-hour discussion exercise to test how we would respond to a ransomware incident. Nothing will happen to real systems. You will hear new information at intervals (called "injects"), and discuss what you would do, who would do it, and what you would say. There are no trick questions, and no marks for individuals. It is a test of the plan.

## Ground rules

1. Blameless. We are testing the plan, not you.
2. Treat it as real, using only the information, tools and authority you would really have.
3. Be specific: who, what, when, and how.
4. "I don't know" is a useful answer. It shows where to improve.
5. One conversation at a time. Keep phones on silent.
6. If a real incident occurs, tell the facilitator and we stop immediately.
7. What is said in the room stays in the room. The output is a list of improvements, not a performance review.

## The company: Fernhill Freight Ltd (fictional)

- A freight forwarder of about 120 people, with a head office, a second office and a bonded warehouse.
- Works with importers and exporters, shipping lines, airlines and hauliers.
- Holds customs authorisations, and submits customs declarations through a supplier-hosted service.
- Takes some card payments through a hosted payment gateway.
- Has cyber insurance with a panel of approved providers.

### The IT environment (simplified)

| Area | Summary |
|---|---|
| Identity | On-premises Active Directory synchronised to Microsoft Entra ID, MFA in place for most staff, but not all legacy groups |
| Email and collaboration | Microsoft 365 |
| Core applications | SaaS freight management system, supplier-hosted customs declaration service, warehouse scanning and stock system on-premises, finance system, HR system |
| Files | On-premises file servers for finance, HR and customer documents, and SharePoint for newer content |
| Endpoints | Windows laptops and desktops managed by Intune, EDR deployed on most devices, handheld scanners at the warehouse |
| Network | Two internet circuits, firewalls with VPN, support from a managed service provider |
| Backups | Nightly backups to a NAS, copied to a cloud bucket, with a quarterly offline set kept in a safe. Backup retention and immutability are not fully consistent across systems |
| Plans | An incident response policy, the playbooks in this repository, a contact sheet, a BIA completed 12 months ago |

### Recovery tiers (from the BIA)

| Tier | Examples | RTO |
|---|---|---|
| T0 | Identity, network and internet | 2 hours |
| T1 | Freight management, customs declarations, warehouse, telephony, email | 4 hours |
| T2 | Finance, payroll, card payments, file shares | 24 hours |
| T3 | CRM, HR system | 72 hours |
| T4 | Reporting | 7 days |

(See the [BIA worked example](../../dr/bia-worked-example.md) for the full picture.)

## Your role

You will play your real role. If you are acting as someone else, the facilitator will tell you.

| Role | You are responsible for |
|---|---|
| Incident Manager | Declaring and running the response, severity, decisions, pace |
| Technical Lead | Investigation, containment, backup validation, recovery order |
| Infrastructure or service desk engineer | First response, isolation, technical facts |
| Communications Lead | Messages to staff, customers, board and media, using templates |
| Data Protection Lead (DPO) | Personal data assessment, ICO and individual notifications |
| Executive Sponsor | Authorisation of major decisions: shutting services, external help, ransom position |
| Operations and customs leads | Business impact, workarounds, customer needs |
| Finance lead | Insurance, payments, bank, fraud risk |
| HR lead | Staff communications, support to affected staff |
| Scribe | Keeps the [decision log](../../comms/decision-log-template.md) and nothing else |

## What you have on the table

- Printed [ransomware playbook](../../playbooks/ransomware.md), [personal data breach playbook](../../playbooks/personal-data-breach.md), [severity model](../../docs/severity-model.md).
- Contact sheet (blank template to be filled with fictional numbers) and [communication templates](../../comms/README.md).
- Decision log sheets.

## Questions to keep asking yourself

- Who is in charge right now?
- What do we know, and what do we not know?
- What is the worst realistic case?
- What decisions are we making, and who owns them?
- Who needs to be told, by when, and by what channel?
- What would we regret not having done in the first hour?

## Decision log sheet (copy as needed)

| Time (scenario) | Decision | Options | Made by | Reason |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
