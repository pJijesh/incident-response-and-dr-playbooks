# Post-incident review template (blameless)

**Purpose:** to learn, not to blame. People make reasonable decisions with the information they have at the time. The question is "what made that the sensible thing to do, and how do we change the system so that the next decision is easier?"

**When:** within 5 working days of stand-down, while memories are fresh, for every P1 and P2 incident, and for near misses worth learning from.

**Who:** everyone involved, a neutral facilitator (not the Incident Manager if possible), and a scribe. Invite business representatives.

**Ground rules**

1. Blameless: describe actions and decisions, not people's character.
2. Focus on systems, processes, tools and information.
3. Everyone speaks. Hierarchy stays outside the room.
4. Evidence over memory: use the [decision log](decision-log-template.md) and timelines.
5. Every finding that matters becomes an action with an owner and a date.

---

## 1. Summary

| Field | Entry |
|---|---|
| Incident reference and title | {{}} |
| Date and duration | {{start, detection, containment, recovery, closure}} |
| Severity (initial and final) | {{}} |
| Playbook(s) used | {{}} |
| Review date and attendees | {{}} |
| One-paragraph summary | {{}} |

## 2. Impact

| Area | Impact |
|---|---|
| Customers and services | {{}} |
| Data | {{what, whose, confidentiality, integrity, availability}} |
| People | {{}} |
| Financial | {{estimate, with confidence}} |
| Regulatory and contractual | {{notifications made, outstanding}} |
| Reputation | {{}} |

## 3. Timeline

| Time | Event | Source |
|---|---|---|
| {{}} | {{}} | {{}} |

Key intervals: time to detect {{}}, time to declare {{}}, time to contain {{}}, time to recover {{}}. Compare them with the targets in the [severity model](../docs/severity-model.md) and, for services, the RTOs in the [BIA](../dr/bia-template.md).

## 4. Root cause and contributing factors

| Question | Answer |
|---|---|
| What was the technical root cause? | {{}} |
| How did the attacker or fault get in or arise? | {{}} |
| What contributing factors made it possible or worse? (process, tooling, access, visibility, supplier, workload) | {{}} |
| Why was it not prevented or detected sooner? | {{}} |

Use "five whys" or a similar method and stop at causes you can act on.

## 5. What went well

- {{}}

## 6. What could have gone better

| Area | Observation | Effect |
|---|---|---|
| Detection | {{}} | {{}} |
| Escalation and decisions | {{}} | {{}} |
| Technical response | {{}} | {{}} |
| Communications | {{}} | {{}} |
| Regulatory and legal | {{}} | {{}} |
| Recovery | {{}} | {{}} |
| Documentation and tooling | {{}} | {{}} |

## 7. Where we were lucky

{{Things that could have made the incident worse, which we should not rely on next time.}}

## 8. Actions

| ID | Action | Type (prevent, detect, respond, recover) | Owner (role) | Due | Priority | Status |
|---|---|---|---|---|---|---|
| {{A-01}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{Open}} |

Review open actions monthly until closed. Report overdue actions to the executive sponsor.

## 9. Document and plan changes

| Document | Change |
|---|---|
| Relevant [playbook](../playbooks/README.md) | {{}} |
| [DR plan](../dr/dr-plan-template.md), [BIA](../dr/bia-template.md), [dependency map](../dr/dependency-map.md) | {{}} |
| Contact sheet and templates | {{}} |
| Risk register | {{}} |

## 10. Sign-off

| Role | Name | Date |
|---|---|---|
| Facilitator | {{}} | {{}} |
| IT Manager | {{}} | {{}} |
| Executive sponsor | {{}} | {{}} |
