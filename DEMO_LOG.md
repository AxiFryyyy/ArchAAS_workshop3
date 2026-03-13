# Project Demo Log — Smart Triage for Customer Support Tickets

**Workshop 3 Assignment — Multi-Agent AI System**

This file contains a full demo run of the smart triage system using sample tickets from `sample_tickets.txt`. The run was executed with `uv run python main.py`.

---

## Highlights (Key Interactions, Tool Usage, Final Outcome)

- **Flow:** For each ticket, the **Orchestrator** (rule-based) drives the sequence: **Classifier** → **Prioritizer** → **Triage Summarizer**, then waits for the next user input.
- **Agent interactions:**  
  - **Classifier** outputs `[Classifier] Category: ...` and a reason (uses tools: `analyze_keywords`, `history_stats` internally to inform the LLM).  
  - **Prioritizer** outputs `[Prioritizer] Priority: ...`, SLA, and reason (uses tools: `analyze_keywords`, `sla_rules_lookup` internally).  
  - **Triage Summarizer** consumes shared state (classification + priority) and produces the final **=== TRIAGE SUMMARY ===** block (no tools; summary + routing + notes).
- **Tool usage:** Tools are invoked inside the Classifier and Prioritizer agents (keyword analysis, SLA rules, history stats). Their results are passed to the LLM prompts; the terminal does not print raw tool output, but the category/priority/SLA and reasons reflect tool-informed decisions.
- **Final outcome:** Each ticket ends with a **TRIAGE SUMMARY** section: summary text, category, priority, recommended routing queue, and operational notes for the support team.

---

## Full Demo Run Log

```
PS D:\学工\5008\Architecting Agentic AI Solutions\Lecture Notes\Day 4\workshop3\ArchAAS_workshop3> uv run python main.py
=== SMART TRIAGE FOR CUSTOMER SUPPORT TICKETS ===
Enter ticket descriptions one at a time. Type 'exit' when you are done.


Enter the customer ticket description (or type 'exit' to quit):
> Our entire team cannot log in to the dashboard since this morning. It shows a 500 error after we enter our credentials. This is blocking our work. Please fix this as soon as possible.
[Classifier] Category: technical_issue (confidence: high)
Reason: The ticket reports a 500 server error preventing the whole team from logging in, indicating a backend/service failure rather than an individual account or credential issue.
[Prioritizer] Priority: P2_high (impact: multiple_users)
SLA: Initial response within 1 hour; restore service ASAP
Reason: The entire team cannot log in to the dashboard (500 error) and their work is blocked, indicating core functionality is impacted. Multiple users affected and business operations are impeded, so this should be escalated above normal priority.

=== TRIAGE SUMMARY ===

Summary: The entire team cannot log in to the dashboard due to a 500 server error, blocking operations.
Category: technical_issue
Priority: P2_high (multiple_users)
Recommended routing: Tech Support - L1
Notes: This looks like a backend/service outage; collect logs, check service status, and be ready to escalate to backend/SRE if the issue persists beyond initial response.

Enter the customer ticket description (or type 'exit' to quit):
> I was charged twice for my subscription last month. I only signed up once but my credit card shows two identical payments. I need a refund for the duplicate charge. Can you look into this?
[Classifier] Category: billing (confidence: high)
Reason: User reports being charged twice for a subscription and requests a refund for the duplicate charge, which directly relates to billing/payments.
[Prioritizer] Priority: P3_normal (impact: single_user)
SLA: Respond within 1 business day
Reason: The user reports a duplicate subscription charge affecting only their account and requests a refund, with no sign of broader impact. This is a standard billing investigation/refund case suitable for the normal single-user SLA.

=== TRIAGE SUMMARY ===

Summary: User reports being charged twice for their subscription and requests a refund for the duplicate charge.
Category: billing
Priority: P3_normal (single_user)
Recommended routing: Billing Team - L1
Notes: Verify the two charge IDs, confirm if a duplicate charge occurred, and process the refund; update the user within the 1-business-day SLA.

Enter the customer ticket description (or type 'exit' to quit):
> I forgot my password and the reset link is not working. I tried three times and it says "link expired" every time. I am locked out of my account and need to access my project files urgently.
[Classifier] Category: account_access (confidence: high)
Reason: The user is unable to log in due to a nonworking/expired password reset link and is locked out of their account, which is a clear account access issue.
[Prioritizer] Priority: P2_high (impact: single_user)
SLA: Respond within 4 hours, resolve within 1 business day
Reason: The user is locked out and cannot access urgent project files because the password reset link repeatedly expires, preventing account access. Urgent language and a failing recovery flow justify elevated priority for a quick response and resolution.

=== TRIAGE SUMMARY ===

Summary: User is locked out due to an expired password reset link and cannot access project files; urgent access required.
Category: account_access
Priority: P2_high (single_user)
Recommended routing: Account Support
Notes: Prioritize quick restoration; investigate why resets expire and issue a fresh link or manual reset.

Enter the customer ticket description (or type 'exit' to quit):
> It would be great if you could add dark mode to the app. Many of us work at night and the current bright theme is hard on the eyes. Also would love to see an option to export reports as PDF. Thanks for considering!
[Classifier] Category: feature_request (confidence: high)
Reason: The user is explicitly asking for new functionality (dark mode and PDF export of reports), which fits a feature request.
[Prioritizer] Priority: P4_low (impact: multiple_users)
SLA: Respond within 2–3 business days
Reason: This is a feature request (dark mode and PDF export) that would benefit multiple users but does not affect core functionality or cause an outage. Schedule for product/roadmap consideration per normal prioritization.

=== TRIAGE SUMMARY ===

Summary: User requests two new features: dark mode in the app and the ability to export reports as PDFs. These changes would benefit multiple users.
Category: feature_request
Priority: P4_low (multiple_users)
Recommended routing: Product Management
Notes: Route to Product Management for roadmap consideration; please gather details on scope (which reports, platform, and preferred export options) to aid prioritization.

Enter the customer ticket description (or type 'exit' to quit):
> The API is down for everyone in our company. We are getting timeouts on all requests since 2 hours ago. Our production environment is affected and we have multiple customers complaining. This is critical – we need an immediate response.
[Classifier] Category: technical_issue (confidence: high)
Reason: The ticket describes the API being down with timeouts affecting the production environment for all users (system-wide outage), indicating a clear technical service failure requiring immediate investigation.
[Prioritizer] Priority: P1_critical (impact: system_wide)
SLA: Respond within 1 hour, resolve within 4 hours
Reason: API is down for the entire company causing production outages and customer complaints for two hours; multiple users and core functionality are affected. Signals (critical, everyone, production) and the ticket text warrant immediate, high-priority response.

=== TRIAGE SUMMARY ===

Summary: The API is down for everyone in the company with timeouts on all requests, affecting production for about 2 hours and causing customer complaints. This is a system-wide outage requiring immediate attention.
Category: technical_issue
Priority: P1_critical (system_wide)
Recommended routing: Tech Support - L1
Notes: Escalate to on-call engineering immediately; gather logs, metrics, and deployment context, and prepare a status update for stakeholders.

Enter the customer ticket description (or type 'exit' to quit):
> Hi, I wanted to ask whether your enterprise plan includes dedicated support and what the SLA is for response times. We are evaluating vendors for next quarter.
[Classifier] Category: billing (confidence: high)
Reason: The user is asking about the enterprise plan and SLA/response times, which pertains to subscription/plan details and support offerings covered under billing/pricing inquiries.
[Prioritizer] Priority: P4_low (impact: single_user)
SLA: Respond within 3 business days
Reason: This is a pre-sales/billing inquiry from a single prospect about enterprise plan support and SLAs, not a production outage. It does not impact system functionality or multiple users, so it can be handled as low priority.

=== TRIAGE SUMMARY ===

Summary: The customer is evaluating our enterprise plan and asks whether it includes dedicated support and what the response-time SLA would be. This is a pre-sales/billing inquiry for a single user.

Category: billing
Priority: P4_low (single_user)
Recommended routing: Billing Team - L2
Notes: Please provide enterprise support options and SLA specifics, and attach any relevant pre-sales documentation.

Enter the customer ticket description (or type 'exit' to quit):
> We were overcharged by thousands of dollars on our last invoice. The amount does not match our contract. We need this corrected urgently before our finance team closes the books this week.
[Classifier] Category: billing (confidence: high)
Reason: The customer reports being overcharged on their invoice and the amount doesn't match their contract, requesting an urgent correction—this is clearly a billing/invoice dispute.
[Prioritizer] Priority: P2_high (impact: single_user)
SLA: Respond within 4 hours, resolve within 1 business day
Reason: The customer reports a large, incorrect invoice amount and explicitly states urgency due to their finance team closing books this week. This is time-sensitive and affects the customer's billing and cashflow, so it warrants high priority and rapid resolution.

=== TRIAGE SUMMARY ===

Summary: Customer reports a large overcharge on the latest invoice that doesn't match their contract and needs urgent correction before their finance team closes books this week.
Category: Billing
Priority: P2_high (single_user)
Recommended routing: Billing Team - L2
Notes: Urgent — verify contract terms and line items, coordinate with finance, and apply the correct adjustment; update the customer on progress within SLA.

Enter the customer ticket description (or type 'exit' to quit):
> My account was suspended and I don't know why. I didn't receive any email explaining the reason. I need to get back in to download our data. Please advise.
[Classifier] Category: account_access (confidence: high)
Reason: The user reports their account was suspended and they cannot access it or received an explanation, which clearly pertains to login/account suspension and access issues.
[Prioritizer] Priority: P3_normal (impact: single_user)
SLA: Respond within 1 business day
Reason: The report describes a single suspended account with no indication of a system-wide issue or multiple users affected. User needs access to download data, but there are no urgency signals or business-critical impact stated. Treat as standard account-access incident: investigate suspension reason and next steps within the normal SLA.

=== TRIAGE SUMMARY ===

Summary: The user's account is suspended without explanation and they cannot access it to download data. They're requesting guidance to regain access and understand the suspension.
Category: account_access
Priority: P3_normal (single_user)
Recommended routing: Account Support
Notes: Please verify user identity and the suspension reason, then provide a clear reactivation path and ETA; ensure data download access is restored after reactivation.

Enter the customer ticket description (or type 'exit' to quit):
> The app keeps crashing when I open a large file. I'm on the latest version. It works for smaller files but anything over 50MB causes an error. Can you fix this bug?
[Classifier] Category: technical_issue (confidence: high)
Reason: The user reports the app crashing with an error when opening files over 50MB and explicitly asks to fix a bug, which matches crash/bug behavior. Several similar tickets have been reported recently, reinforcing this as a technical issue.
[Prioritizer] Priority: P3_normal (impact: single_user)
SLA: Respond within 1 business day
Reason: The app crashes only when opening large files (>50MB), which appears to affect a limited use case rather than the whole system or many users. No outage or widespread impact is indicated, so standard bug-fix triage and investigation within normal SLA is appropriate.

=== TRIAGE SUMMARY ===

Summary: The app crashes when opening files larger than 50MB on the latest version, and the user requests a bug fix.

Category: technical_issue
Priority: P3_normal (single_user)
Recommended routing: Tech Support - L1
Notes: Request crash logs and reproduction steps (OS/device/app version) to aid triage; this is a recurring large-file crash.

Enter the customer ticket description (or type 'exit' to quit):
> Several people on my team are unable to sign in today. We get an error message saying "verification failed" after entering the OTP. This started happening after your last update. We need access to complete a client deliverable.
[Classifier] Category: account_access (confidence: high)
Reason: Multiple team members cannot sign in due to an OTP "verification failed" error after the last update, which is clearly an account access/login issue affecting access for several users.
[Prioritizer] Priority: P2_high (impact: multiple_users)
SLA: Respond within 4 hours, resolve within 1 business day
Reason: Multiple team members cannot complete sign-in (OTP verification failed) after the last update, blocking access to a client deliverable. This affects core account access for several users and should be addressed promptly.

=== TRIAGE SUMMARY ===

Summary: Multiple team members cannot sign in due to an OTP verification failure after the last update, blocking access to a client deliverable.
Category: account_access
Priority: P2_high (multiple_users)
Recommended routing: Account Support
Notes: Investigate recent update affecting OTP/auth, determine if issue is widespread or tenant-specific, and check for any temporary sign-in workarounds.

Enter the customer ticket description (or type 'exit' to quit):
> exit

Goodbye!
```
