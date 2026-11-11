# Injects: ransomware tabletop

Each inject lists the **simulated time** (Friday to Monday), the delivery method, the content, what a good response looks like, and prompts for the facilitator. Print each inject on its own sheet. Everything is fictional.

The inject controller says the scenario time aloud each time. Participants only see the inject text. The "Expected response" and "Prompts" are for facilitator and observer.

---

## Inject 1: Slow files (Friday 16:10)

**Delivered by:** Service desk phone call (read aloud)

> "Hi, it's the warehouse supervisor at the Fernhill bonded site. Several of us can't open shared files, and the handheld scanners are very slow. Some documents have strange names with `.frnh7` on the end. It started about ten minutes ago. Is something going on?"

**Expected response**

- Service desk records the report with time, escalates to the Technical Lead, and does not tell the user to reboot.
- Recognises possible ransomware trigger in the [playbook](../../playbooks/ransomware.md#2-triggers); starts the decision log; notes time of awareness.

**Prompts**

- Who do you tell, and how, right now?
- Is this an incident? What severity would you give it, and why?
- What do you tell the supervisor to do and not do?
- Where is the playbook and contact sheet if the file server is down?

---

## Inject 2: EDR alert and ransom note (Friday 16:25)

**Delivered by:** Written note handed to the Technical Lead

> EDR console: 14 endpoints and 3 servers reporting mass file modification and deletion of shadow copies in the last 12 minutes. Two users have emailed screenshots of a text file called `README_RESTORE.txt` that says: "Your files are encrypted. Do not contact the police. Contact us at the address below within 72 hours."

**Expected response**

- Declare P1; open the bridge; use out-of-band communication.
- Isolate affected devices with EDR, do not power off, protect backups, disable compromised accounts from a clean device.
- Tell staff to stop using the affected systems.

**Prompts**

- Who declares P1 and who runs the call? What if they are on leave?
- What are your first 15 minutes? (Check [first 15 minutes](../../playbooks/ransomware.md#5-first-15-minutes).)
- Isolate or power off? Who decides?
- How do you tell 120 staff when email may be compromised?

---

## Inject 3: Backups (Friday 16:50)

**Delivered by:** Infrastructure engineer, verbally

> "I can't log in to the backup console with my admin account. The last job log I can see from the NAS shows retention was changed from 30 days to 1 day at 02:40 this morning. I'm not sure what is left. The offsite copy goes to a cloud bucket, and we have a quarterly offline USB set that is in the safe at head office."

**Expected response**

- Disconnect and protect all backup repositories; stop jobs and retention policies; use a clean device; engage the backup vendor.
- Recognise the attacker was in the environment for hours before encryption.
- Start validating backups before relying on them.

**Prompts**

- Who has access to the immutable or offline copy, and how long to get it?
- How do you know the backups are clean?
- What is the age of the offline set and what would that mean for RPO?

---

## Inject 4: Extortion email (Friday 17:20)

**Delivered by:** Email printout addressed to the CEO

> **From:** an anonymous mail account  
> **Subject:** We have your data  
> We have been in your network for several days. We have copied about 200 GB, including HR files, customer contracts and shipping documents. Pay within 72 hours or the files will be published and your customers informed. Do not involve police or insurers. We will contact you again.

**Expected response**

- Do not reply or negotiate. Preserve the email. Consider whether the claim is credible, and that stealing data is common in ransomware cases.
- Start the personal data assessment and the 72-hour clock; tell the Data Protection Lead.
- Insurer and incident response provider called; legal advice sought.

**Prompts**

- Who owns the decision on the demand? What is the default position?
- Do you tell the board now? What do you say?
- Is the 72-hour deadline in the email the same as the ICO's 72 hours? (No. They are unrelated clocks.)
- What does the NCSC say about paying? (See the [playbook](../../playbooks/ransomware.md#12-decision-points) and [references](../../docs/references.md#ransomware-and-disruptive-attacks).)

---

## Inject 5: Customers and customs (Friday 18:00)

**Delivered by:** Customs team lead, phone call

> "We have a vessel arriving at 06:00 tomorrow with 31 customers' consignments. Declarations are prepared in the freight management system, and that is slow. The customs service itself is run by the supplier, but we cannot reach our files. Also, two key customers are calling about tracking."

**Expected response**

- Identify the business impact using the [BIA](../../dr/bia-worked-example.md): customs is T1 with a short MTPD.
- Use the documented customs contingency procedure and supplier support. Identify what works (supplier-hosted service) and what does not (our files).
- Plan a customer holding message; check contractual notification duties.

**Prompts**

- What is the workaround? Is it written down? Where?
- Who talks to customers and what do they say? Can they say "cyber attack" yet?
- What are the customs and contractual consequences of late declarations? Who would know?

---

## Inject 6: Insurer call (Friday 18:40)

**Delivered by:** Insurer hotline (fictional policy), read by the inject controller

> "We have your notification. Under your policy you must use one of our panel incident response providers and our panel solicitors. We can connect you now. Please do not engage other providers or pay any third party without our consent. We need to be told of any ransom demand immediately. Do you have a list of your backups and your network diagram?"

**Expected response**

- Accept the panel provider if that is the policy condition, and confirm what the policy covers, with authority from the executive sponsor.
- Provide documents: network diagram, asset inventory, backup inventory. (Do these exist in a place we can reach?)
- Log the notification and the decisions.

**Prompts**

- Who has the policy number and authority to engage?
- What if the insurer's provider is not the one you would have chosen?
- What information would the provider need first, and can you get it with the file server down?

---

## Inject 7: Scoping findings (Friday 21:30)

**Delivered by:** Incident response provider update (written)

> Initial findings: the attacker signed in to the VPN at 03:12 on Wednesday using a standard user account that was not covered by MFA because it was in a legacy group. They moved to a domain administrator account on Thursday. Data was copied from the HR and finance file shares, which contain payroll files with staff names, addresses, national insurance numbers and bank details, and customer contracts. Encryption began Friday 16:00.

**Expected response**

- Personal data confirmed: special attention to staff financial data and identifiers; Data Protection Lead starts formal risk assessment; likely a reportable breach with a high risk to staff.
- Credential reset plan; forced re-registration of MFA; close the VPN route.
- Start the notification tracker.

**Prompts**

- What is the time of awareness for the ICO clock? (Discuss: when did you become aware of a breach of personal data?)
- Who tells staff, and when? What will you tell them?
- What do you reset first, and from where?
- Is the identity system trustworthy at all?

---

## Inject 8: Media and social media (Saturday 09:00)

**Delivered by:** Communications Lead receives an email from a local trade journalist, and a staff member posts a message on a social platform

> **Journalist:** "We understand Fernhill Freight has suffered a cyber attack and that its systems are down. Can you confirm, and say whether customer or staff data has been stolen? We are publishing at noon."
>
> **Staff post:** "Our systems are down, the whole company is locked out, rumour is we got hacked. Weekend shift is cancelled."

**Expected response**

- Communications Lead uses the [media holding statement](../../comms/media-holding-statement.md), checks with the Executive Sponsor and legal, and does not confirm speculation or discuss ransom.
- Staff reminded not to post; staff notice sent through the out-of-band channel.
- Align with customer and staff communications.

**Prompts**

- Who approves the statement? How fast?
- What can you say honestly now?
- How do you handle staff speculation without blame?

---

## Inject 9: Board and ransom decision (Saturday 11:30)

**Delivered by:** Board chair, phone call

> "I've heard about this from a journalist. What's going on? I need a briefing in 30 minutes. I'm told the attackers are offering a 'proof of decryption' and a discount if we pay by tonight. Our insurer's negotiator says it is an option. What do you recommend?"

**Expected response**

- Use the [board update template](../../comms/board-update.md), lead with decisions and facts, say what is unknown.
- Record that payment is an Executive Sponsor decision with legal advice, informed by NCSC guidance: no guarantee, possible sanctions issues, does not remove regulatory obligations, data may still be published.
- Compare payment with the backup-based recovery option. Identify what additional information is needed.

**Prompts**

- Who answers the board chair? What does the one-page update say?
- What is our position on payment, and who must agree?
- What would change our mind?
- Where do we record the decision?

---

## Inject 10: Recovery reality (Saturday 15:00)

**Delivered by:** Infrastructure engineer, written note

> Backup review: the immutable cloud copy of the file servers is intact and 16 hours old. The offline USB set is 9 weeks old. The domain controller backups exist, but a restore has never been tested. The freight management system is SaaS and unaffected, but sign-in depends on Entra ID, whose on-premises sync server is encrypted. Domain admin credentials are believed to be compromised.

**Expected response**

- Plan a clean-room rebuild of identity first, then T1 services in BIA order; validate backups; define minimum viable operation.
- Decide what to do about the sync server and cloud sign-in: isolate the sync, break-glass accounts, revoke sessions.
- Discuss realistic timescales and be honest with the business.

**Prompts**

- What is your recovery order and why? Which BIA tier does each item belong to?
- What is minimum viable operation for Monday morning?
- What can be done manually? Who needs to be told?
- What are the risks of restoring too early?

---

## Inject 11: The clock and the leak site (Saturday 19:40)

**Delivered by:** Data Protection Lead update, read aloud

> It is now about 27 hours since the incident response provider confirmed data theft. The attackers have posted a sample on a leak site that includes ten payroll records. The ICO online form needs the nature of the breach, categories and approximate numbers of individuals and records, likely consequences, and measures taken. You think around 180 current and former staff are affected, but it could be more. Staff have not yet been told.

**Expected response**

- Decide to report to the ICO promptly with the information available, reporting in phases if needed, rather than waiting for certainty. Use the [regulator notification template](../../comms/regulator-notification.md).
- Decide to notify staff directly because of high risk (financial data and identifiers), with advice and a contact point. Draft with the [staff notice](../../comms/staff-notice.md).
- Consider reports to the NCSC and police (Report Fraud, or Police Scotland if in Scotland).

**Prompts**

- Who signs off the ICO report? What do you say about numbers you do not know?
- Do you tell staff before the ICO or the other way around? Why?
- What support do you offer affected staff and former staff?
- Which other notifications are due: customers, insurer, card acquirer, authorities, certification body?

---

## Inject 12: Monday planning (Sunday 20:00)

**Delivered by:** Operations Director, verbal

> "We need a plan for Monday. Warehouse opens at 06:00, customs team at 07:00, customer service at 08:00. Our freight management supplier says they have seen unusual API calls from our integration account and recommend rotating the credentials. What are we doing, and what do I tell people?"

**Expected response**

- A Monday plan covering minimum viable operations, paper workarounds, communication to all teams, and a rota that rests the response team.
- Rotate integration credentials; also run the [supplier outage](../../playbooks/saas-supplier-outage.md) steps if the supplier is affected.
- Define heightened monitoring and handover.

**Prompts**

- Who is on the response rota? When do the first responders rest?
- What do staff need to hear on Monday morning at 06:00?
- What goes in the next board update?
- What is the post-incident plan?

---

## Optional wildcard injects

Use these to stress specific weaknesses.

| Wildcard | When | Content |
|---|---|---|
| Key person away | Any time | "The Incident Manager's phone goes to voicemail. They are on a flight for the next 9 hours." |
| Out-of-band failure | After inject 2 | "The messaging group you set up includes someone who left the company last month." |
| Wrong data | After inject 7 | "The incident response provider revises: the stolen data may also include customer contact lists." |
| Supplier is the entry point | After inject 7 | "Logs suggest the attacker first used the managed service provider's remote access account." |
| Regulator call | After inject 11 | "The ICO case officer phones to ask why a notification was not sent earlier." |
| Insurer disputes | After inject 9 | "The insurer says paying the ransom needs prior consent, and your negotiator has already made contact." |
