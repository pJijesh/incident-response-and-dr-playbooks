# Audit mapping

This page shows where the repository's artefacts can serve as evidence for common audit topics. It supports audit preparation. It does **not** claim that using these documents makes an organisation compliant or certified, and it is not legal advice. Control names were confirmed from secondary sources, not from the paid standards (see [references](references.md#standards-and-audit)). Check the standards directly.

| Audit topic | Typical expectation | Where this repository helps | Evidence to keep |
|---|---|---|---|
| ISO/IEC 27001:2022 Annex A 5.24, Incident management planning and preparation | Defined process, roles and responsibilities for incident management | [Playbooks](../playbooks/README.md), [severity model](severity-model.md) roles, [contact sheet](../comms/contact-sheet-template.md) | Approved playbooks, version history, role assignments |
| Annex A 5.25, Assessment and decision on information security events | Events are assessed and classified | Severity matrices and decision points in each playbook | Completed [decision logs](../comms/decision-log-template.md) |
| Annex A 5.26, Response to information security incidents | Documented response procedures followed | Playbook sections: first 15 minutes, containment, eradication, recovery | Incident records with timelines |
| Annex A 5.27, Learning from incidents | Lessons are fed back to improve controls | [Post-incident review template](../comms/post-incident-review-template.md), [lessons-learned template](../exercises/ransomware-tabletop/lessons-learned-template.md) | Reviews with owned, dated actions, and closure evidence |
| Annex A 5.28, Collection of evidence | Evidence identified, collected and preserved | Evidence handling sections, evidence register in the decision log | Chain of custody records |
| Annex A 5.29 and 5.30, Information security during disruption and ICT readiness for business continuity | Continuity planned and tested to objectives | [BIA](../dr/bia-template.md), [tier table](../dr/rto-rpo-tiers.md), [DR plan](../dr/dr-plan-template.md), [test report](../dr/dr-test-report-template.md) | Signed BIA, test reports, restore logs |
| Annex A 8.13, Information backup | Backups taken and tested | [Backup and restore test log](../dr/backup-restore-test-log.md) | Test logs with results and actions |
| Annex A 5.19 to 5.22, Supplier relationships | Supplier security managed | [Supplier outage playbook](../playbooks/saas-supplier-outage.md), [dependency map](../dr/dependency-map.md) | Supplier register, contract clauses, incident contacts |
| PCI DSS v4.0.1 requirement 12.10, Incident response | A plan exists, is ready to be activated, is reviewed and tested at least annually, with trained and designated personnel | [Ransomware](../playbooks/ransomware.md) and [personal data breach](../playbooks/personal-data-breach.md) playbooks, [tabletop pack](../exercises/ransomware-tabletop/README.md) | Annual exercise records, training records, contact sheet. Check the exact sub-requirements in the standard |
| UK GDPR Articles 33 and 34, and accountability | Breaches recorded, assessed, reported where required, individuals told where high risk | [Personal data breach playbook](../playbooks/personal-data-breach.md), [regulator notification template](../comms/regulator-notification.md) | Breach register with reasoning for every breach, including unreported ones |
| Customs or sector authorisations (for example AEO) | Conditions about record-keeping, security and contingency vary | [BIA](../dr/bia-template.md) workaround and regulatory driver columns | Not mapped here. Check conditions with your compliance lead |

## Evidence checklist for an assessor visit

- [ ] Approved, current playbooks with a review date within the last 12 months.
- [ ] A signed BIA and tier table.
- [ ] Contact sheet checked in the last quarter.
- [ ] At least one exercise in the last 12 months, with scored evaluation and an action tracker.
- [ ] Restore tests per the schedule, with failures actioned.
- [ ] Breach register with decisions and reasons.
- [ ] Post-incident reviews for P1 and P2 incidents, with action closure.
- [ ] Supplier incident contacts and contract notification clauses.
