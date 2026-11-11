# Playbook: DDoS and internet-facing service outage

| Field | Value |
|---|---|
| Version | 1.0 |
| Owner | IT Manager |
| Last reviewed | 2026-11-04 |
| Review cycle | At least every 12 months, and after every real incident or exercise |
| Related | [Critical SaaS or supplier outage](saas-supplier-outage.md), [Ransomware](ransomware.md), [Dependency map](../dr/dependency-map.md), [Severity model](../docs/severity-model.md) |

> This playbook is operational guidance, not legal advice. Specific mitigation steps depend on your ISP, DNS provider and any CDN or web application firewall, so agree and test them with those providers before an incident.

## 1. Purpose

To restore availability of internet-facing services (website, customer portal, API, VPN, email gateway, DNS) when they become slow or unreachable because of a denial of service attack, or because of a failure that looks like one. A denial of service attack aims to make a service unreliable or unresponsive. It need not touch confidentiality or integrity of data, but it can be used as a distraction or an extortion lever.

The first job is to work out which of these you are dealing with, because the responses differ:

- Distributed denial of service (DDoS) volumetric or application-layer attack.
- Legitimate traffic surge (a campaign, a media mention, a month-end peak).
- Internal fault (misconfiguration, certificate expiry, capacity, a failed deployment, DNS error).
- Upstream provider failure (ISP, DNS, cloud region, CDN).

## 2. Triggers

- Website, portal, API or VPN becomes slow, or times out, for many users at once.
- Monitoring shows traffic spikes, high connection counts, exhausted firewall sessions or saturated bandwidth.
- ISP or hosting provider sends a DDoS alert or nulls an IP address.
- Ransom or extortion email threatening or claiming a DDoS attack.
- Many requests to one URL from varied or unusual sources, or unusual User-Agent strings.
- Security tooling alerts for flood, SYN flood or amplification patterns.

## 3. Severity matrix

| Level | Examples |
|---|---|
| P1 Critical | A Tier 0 or Tier 1 internet-facing service is unreachable (customer ordering, tracking, remote access for most staff); sustained for longer than the RTO; extortion demand received; attack used to mask an intrusion |
| P2 High | Significant degradation of a customer-facing service, partial outage, or one connection or site affected |
| P3 Medium | Short-lived or mitigated attack with little visible impact |
| P4 Low | Scanning and low-volume probing, logged |

Targets are in the [shared severity model](../docs/severity-model.md).

## 4. Roles

| Role | Duties |
|---|---|
| Incident Manager | Declares the incident, decides on trade-offs such as blocking regions or serving a reduced site |
| Technical Lead | Diagnosis, mitigation, and liaison with ISP, DNS, CDN or WAF provider |
| Network or MSP contact | Applies upstream filtering, rate limiting and rerouting |
| Communications Lead | Status page and customer messages |
| Executive Sponsor | Approves emergency spend (scrubbing service, extra capacity) and any extortion response, which should be "do not pay" without strong reasons |
| Scribe | Timeline and decision log |

## 5. First 15 minutes

1. **Confirm and classify.** Check from outside your network. Compare current traffic with the normal baseline: bandwidth, requests per second, source diversity. Is it an attack, a surge or a fault?
2. **Check the basics**: certificate expiry, DNS resolution, recent changes and deployments, firewall session table, server and database health, ISP status page.
3. **Call your ISP, hosting provider, CDN or WAF provider** and ask for DDoS support. Provide time, target IPs, ports and symptoms. Open tickets and note numbers.
4. **Open the decision log** and declare an incident, noting the time and provisional severity.
5. **Put up a status message** on an independent channel (a status page hosted elsewhere, social account, phone message) saying that you are aware, investigating, and when you will update.
6. **Protect essential services**: if the attack is on the website, make sure staff access to email, identity and key business systems still works. Check that critical remote access has a fallback.
7. **Capture evidence** while the attack is happening: traffic graphs, top talkers, sample packets and web server logs.

## 6. Containment

Typical measures, in the order that is usually cheapest and least disruptive. Use the ones that your providers support.

- [ ] Enable or increase DDoS protection and rate limiting at the upstream provider, CDN or WAF. Ask the provider to apply scrubbing or to filter by protocol.
- [ ] Put the target behind a CDN or protective proxy if it is not already, and restrict origin servers to accept traffic only from that proxy.
- [ ] Block or rate-limit abusive sources, user agents, URLs or request patterns. Block by geography only if you are sure that it will not block genuine customers, and record the decision.
- [ ] Serve a static or reduced version of the site or portal, shut non-essential features, and disable expensive endpoints (search, login, report generation).
- [ ] Scale capacity if it is quick and affordable, but do not assume that scaling alone will outlast a determined attack.
- [ ] Change DNS (lower TTLs beforehand) to move traffic to a protected endpoint, if your plan supports it.
- [ ] Protect login endpoints: stricter rate limits, CAPTCHA, temporary lockouts. Remember that attackers sometimes use a DDoS to distract from a credential attack or intrusion, so watch for other signs.
- [ ] Keep a clear record of every change so that you can undo it afterwards.

NCSC guidance on denial of service sets out the four practices to build before an attack: understand your service, understand your defences, create a response plan and test your response (see [references](../docs/references.md#denial-of-service)).

## 7. Eradication

For DDoS, eradication means removing the exposure that made the attack effective.

- Fix any application weakness that was exploited (expensive queries, unauthenticated endpoints, missing caching).
- Remove unnecessary exposure: closed ports, unused services, and origin IP addresses that have leaked.
- Review whether your public IP addresses and DNS records reveal origin servers behind a CDN, and change them if they do.
- If the cause was an internal fault, fix and document the root cause. If upstream, record the supplier's remedial actions.
- Check whether the attack coincided with other activity (intrusion, credential stuffing, defacement). If so, open the [ransomware](ransomware.md) or [account compromise](m365-account-compromise-bec.md) playbooks as needed.

## 8. Recovery

1. Return services gradually. Remove emergency blocks in stages and watch traffic and error rates.
2. Restore any features that were turned off, and update the status page to say so.
3. Confirm that the DNS and routing changes made during the attack are reverted or deliberately kept.
4. Check data and queues: failed transactions, partial uploads and backlogs, and process them.
5. Keep the heightened monitoring and the upstream protection for at least 7 days in case of a repeat. Attackers often return.
6. Tell customers when service is back to normal and apologise for the disruption, as appropriate.

## 9. Evidence handling

- Preserve **traffic captures** or flow records (NetFlow or similar), firewall logs, web server logs, CDN or WAF logs, and DNS query logs for the attack window.
- Record **attacker indicators**: source IP ranges, ASNs, request signatures, user agents, URLs targeted, amplification vectors.
- Preserve **extortion emails** with full headers. Do not reply.
- Take **screenshots** of monitoring graphs and provider dashboards, with time stamps.
- Keep the **provider ticket history** and the log of all changes made, with times.
- Keep **impact evidence** (orders lost, SLA breaches) for insurance and contract purposes.

## 10. Communications

| Audience | Template | Notes |
|---|---|---|
| Customers | [Customer notice](../comms/customer-notice.md), and a status message | Honest about the effect, without speculation on cause or attacker |
| Staff | [Staff notice](../comms/staff-notice.md) | Which services are affected and the workarounds |
| Board | [Board update](../comms/board-update.md) | If P1 or an extortion demand has been received |
| Providers | Direct calls and tickets | Name one contact per provider |
| Media | [Media holding statement](../comms/media-holding-statement.md) | Only if enquiries arrive |

## 11. Regulatory and contractual notifications

| Who | When |
|---|---|
| ISP, CDN or hosting provider | Immediately, to engage their DDoS support and as per contract |
| Customers | If SLAs or contracts require notice of service interruptions |
| Police and Report Fraud | If an extortion demand was made, report it. Report Fraud covers England, Wales and Northern Ireland, and in Scotland, contact Police Scotland on 101 |
| NCSC | Denial of service is a category of cyber incident that can be reported through the NCSC reporting service |
| ICO | A DDoS alone rarely involves a personal data breach, but loss of availability of personal data can be a breach. If personal data was unavailable in a way likely to risk individuals, or if there was an intrusion alongside, follow the [personal data breach playbook](personal-data-breach.md) |
| Insurer | If cover for business interruption or cyber extortion may respond, check the policy |
| Card acquirer | If a payment page was affected |
| Customs and sector authorities | If declaration or record-keeping services were unavailable, follow your compliance procedure |

## 12. Decision points

| # | Decision | Owner |
|---|---|---|
| D1 | Attack, surge, internal fault or upstream failure? | Technical Lead |
| D2 | Engage upstream mitigation and accept the cost | Incident Manager, Executive Sponsor |
| D3 | Serve a reduced or static site, or take a service offline | Incident Manager |
| D4 | Block by geography, user agent or IP ranges, and the risk of blocking genuine users | Technical Lead |
| D5 | Respond to an extortion demand (default: do not pay, and report) | Executive Sponsor |
| D6 | Is there a concurrent intrusion? | Technical Lead |
| D7 | When to lift emergency measures | Incident Manager |

## 13. Post-incident actions

- Blameless [post-incident review](../comms/post-incident-review-template.md).
- Resilience improvements: DDoS protection from the upstream provider or a CDN or WAF, origin hiding, rate limiting, caching, capacity headroom, secondary ISP and DNS provider, monitoring and alert thresholds.
- Write a short **service-specific runbook** for each public service: baseline traffic, protective controls, provider contacts, how to put up a reduced version.
- Test the plan: a tabletop or a controlled load test with the provider's agreement.
- Update the [dependency map](../dr/dependency-map.md), and the contact sheet.
- Check the NCSC denial of service guidance for improvements to your defences.

## 14. Quick-reference checklist

- [ ] Confirm from outside; compare with baseline; attack, surge or fault?
- [ ] Check certificates, DNS, recent changes, firewall sessions, ISP status
- [ ] Call the ISP, CDN, WAF or hosting provider; open tickets
- [ ] Declare the incident; start the decision log
- [ ] Post a status message on an independent channel
- [ ] Protect core staff services (identity, email, remote access)
- [ ] Capture evidence: traffic graphs, top sources, logs, extortion email
- [ ] Enable upstream mitigation, rate limiting and protective proxy
- [ ] Serve a reduced or static version if needed
- [ ] Watch for a concurrent intrusion or credential attack
- [ ] Do not pay an extortion demand without exec and legal discussion; report it
- [ ] Lift measures in stages; keep monitoring for 7 days
- [ ] Hold the blameless review
