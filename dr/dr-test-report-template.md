# DR test report template

Use one report per DR test, exercise or real invocation. Keep it to two or three pages. The audience is the executive sponsor, internal audit and external assessors, so write plainly and be honest about what did not work. A report that shows a failure and a fix is more convincing than one that shows only passes.

> Generic template. Not legal advice.

## 1. Summary

| Field | Value |
|---|---|
| Report reference | {{DR-TEST-YYYY-NN}} |
| Date and duration of test | {{date, start and end time}} |
| Test type | {{restore test, failover test, full DR exercise, real invocation}} |
| Services in scope | {{list with tiers}} |
| Test lead | {{role}} |
| Participants | {{roles, not names, if the report is circulated widely}} |
| Overall result | {{Pass, Partial, Fail}} |
| One-paragraph summary | {{what was tested, what happened, the main finding}} |

## 2. Objectives and scope

| Objective | Success criterion | Achieved? |
|---|---|---|
| {{Restore the customs declaration service to a test environment}} | {{Within RTO, data within RPO, validated by customs team}} | {{Yes, Partly, No}} |
| {{}} | {{}} | {{}} |

Scope exclusions and simulated elements: {{what was not tested, and what was simulated instead}}.

Test conditions: {{announced or unannounced, time of day, restore environment, how production was protected}}.

## 3. Results against recovery objectives

| Service | Tier | RTO target | RTO actual | RPO target | RPO actual | Result | Notes |
|---|---|---|---|---|---|---|---|
| {{}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |

Record actual times from the start of the test clock to business validation sign-off, not only to technical completion.

## 4. Timeline

| Time | Event | Who |
|---|---|---|
| {{}} | {{}} | {{}} |

## 5. What worked well

- {{}}

## 6. What did not work

| Issue | Impact | Root cause | Severity (H, M, L) |
|---|---|---|---|
| {{}} | {{}} | {{}} | {{}} |

Typical issues to look for: backup completeness, missing credentials or keys, undocumented dependencies, runbook gaps, licensing, network access to the restore environment, restore speed, time to find the right person, out-of-band communication failures, and sign-off delays.

## 7. Actions

| ID | Action | Owner (role) | Due | Priority | Status |
|---|---|---|---|---|---|
| {{ACT-01}} | {{}} | {{}} | {{}} | {{}} | {{Open}} |

Actions are tracked until closed, and the report is updated when they are.

## 8. Changes to documents

| Document | Change needed |
|---|---|
| [DR plan](dr-plan-template.md) | {{}} |
| [BIA](bia-template.md) and [tier table](rto-rpo-tiers.md) | {{RTO or RPO targets that were not achievable and a decision to fund or accept}} |
| [Dependency map](dependency-map.md) | {{newly found dependencies}} |
| [Playbooks](../playbooks/README.md) | {{}} |

## 9. Risk position and conclusion

- Are the stated RTO and RPO achievable today? {{Yes, No, Partly, with evidence}}
- Residual risks and decisions needed from the executive sponsor: {{}}
- Recommended date of next test: {{}}

## 10. Sign-off

| Role | Name | Date |
|---|---|---|
| Test lead | {{}} | {{}} |
| IT Manager | {{}} | {{}} |
| Executive sponsor | {{}} | {{}} |
