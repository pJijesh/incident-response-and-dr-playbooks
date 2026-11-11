# Facilitator guide: ransomware tabletop

## 1. Before the day

**Two to four weeks before**

- [ ] Agree the objectives in the [README](README.md) with the executive sponsor, and choose the date. Block a room (or a video call) for 2 hours.
- [ ] Choose participants. Aim for people who would genuinely be on the response team: Incident Manager, Technical Lead, service desk or infrastructure engineer, Communications Lead, Data Protection Lead (DPO), operations or customs lead, finance lead, HR, executive sponsor. Add a deputy for each critical role.
- [ ] Appoint an **inject controller** (delivers injects, keeps time) and an **observer** (scores the [evaluation form](evaluation-form.md), notes behaviours). The facilitator should not also be a participant.
- [ ] Customise the scenario: replace Fernhill Freight details with your own sites, systems and supplier names where that helps, and keep it clearly marked as an exercise. Keep the timeline realistic for your environment.
- [ ] Read the [injects](injects.md) and decide which to use. Pre-print each inject on a separate sheet.
- [ ] Check the playbooks, contact sheet and decision log are available to participants as they would be in a real incident (some on paper).

**One week before**

- [ ] Send participants a short invitation: purpose, time, "no preparation needed", "it is a test of the plan, not of you", and the [participant handout](participant-handout.md) (scenario background and ground rules only, not the injects).
- [ ] Tell any suppliers or external contacts who might be involved.
- [ ] Prepare a flipchart or whiteboard with the five columns: Decisions, Actions, Questions, Gaps, Good practice.

**On the day**

- [ ] Printed playbooks, role cards, decision log sheets and pens on the table.
- [ ] Phones set to silent. Real incidents take priority: agree a signal for stopping the exercise.

## 2. Ground rules to read out

1. This is a test of the plan and our preparation, not of individuals. It is blameless.
2. Treat the scenario as real, but you may only use information and resources you would have in a real incident.
3. Say what you would actually do, and who would do it. "We would escalate" is not enough: to whom, how, and when?
4. If you do not know, say so. That is a finding, not a failure.
5. The facilitator may ask "why?" and "what if?" a lot. That is the job.
6. Decisions are written in the decision log by the scribe participant as they are made.
7. One conversation at a time.
8. What is said in the room stays in the room. The output is the lessons-learned record, not individuals' performance.

## 3. Run sheet (2 hours)

| Real time | Activity | Lead |
|---|---|---|
| 00:00 to 00:10 | Welcome, objectives, ground rules, introductions, scenario background | Facilitator |
| 00:10 to 00:25 | Inject 1 and 2: detection and first response | Inject controller |
| 00:25 to 00:40 | Inject 3 and 4: backups affected, extortion email | Inject controller |
| 00:40 to 00:55 | Inject 5 and 6: customers, insurer | Inject controller |
| 00:55 to 01:10 | Inject 7 and 8: scope, data theft, media | Inject controller |
| 01:10 to 01:25 | Inject 9 and 10: board and ransom decision, recovery reality | Inject controller |
| 01:25 to 01:40 | Inject 11 and 12: the 72-hour clock and recovery planning | Inject controller |
| 01:40 to 01:55 | Hot debrief: what worked, what did not, top three actions | Facilitator |
| 01:55 to 02:00 | Close, thanks, next steps, evaluation forms | Facilitator |

The timeline in the scenario runs from Friday 16:10 to the following Monday morning, so the inject controller announces the jump in scenario time before each inject. "Simulated time" is in the [injects](injects.md).

### Shorter variants

- **90 minutes:** use injects 1, 2, 3, 4, 6, 7, 9, 10, 11. Shorten the debrief to 10 minutes.
- **45 minutes (technical team):** use injects 1, 2, 3, 7, 10. Focus on containment, backup validity and restore order.
- **45 minutes (executive team):** use injects 4, 6, 8, 9, 11. Focus on decisions, regulators, communications and the ransom question.

## 4. Facilitation tips

- **Pace.** Give each inject 5 to 8 minutes of discussion, then move on. Use time pressure deliberately but not artificially.
- **Quiet voices.** Ask each role in turn: "What would you be doing right now?"
- **Challenge assumptions.** "Where is that document stored if the file server is encrypted?" "Who has the number for the insurer?" "Is that email going through a compromised system?"
- **Stay out of the answer.** Ask questions. Do not teach during the exercise, save it for the debrief.
- **Park tangents.** Use the whiteboard Questions column.
- **Use the decision log.** Check that decisions are recorded with time, owner and rationale.
- **Injects are adjustable.** If participants "solve" something early, tighten the next inject. If they are stuck, add a nudge.
- **Watch for fatigue.** Real incidents last longer than 2 hours, so discuss handovers and shift patterns.
- **Keep realism.** If a participant says "we would call the supplier", the inject controller can answer in character, or say it goes to voicemail.

## 5. Hot debrief questions

1. What went well that we should protect?
2. What surprised you?
3. Where did we waste time?
4. Which decisions were hardest, and why? What information would have made them easier?
5. Did we know who was in charge at each stage?
6. Which documents, contacts or access did we not have?
7. Where might the plan break under real stress (night, weekend, key person away)?
8. What are the top three things to fix in the next 30 days?

## 6. After the exercise

- [ ] Collect the [evaluation forms](evaluation-form.md) and the decision log.
- [ ] Complete the [lessons-learned record](lessons-learned-template.md) within 5 working days, with owners and dates.
- [ ] Share a short, blameless summary with participants and the executive sponsor.
- [ ] Update the playbooks, contact sheet and DR plan where the exercise found gaps.
- [ ] Track actions to closure and report progress at the next leadership meeting.
- [ ] Schedule the next exercise within 6 to 12 months, with a different scenario or variation such as "key person unavailable", "weekend", or "supplier is the entry point".

## 7. Evidence for audit

Keep the date, attendees (by role), scenario, evaluation forms, lessons-learned record and the action tracker. Auditors and assessors generally look for evidence that the plan is tested and that findings lead to action. For example, PCI DSS has requirements for reviewing and testing the incident response plan, and ISO/IEC 27001 expects incident management to be planned and improved. See [references](../../docs/references.md#standards-and-audit) and the [audit mapping](../../docs/audit-mapping.md).
