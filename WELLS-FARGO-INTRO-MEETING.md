# Wells Fargo — Introductory Call Prep

**Purpose:** 30-minute introductory call with your Wells Fargo contact to review **their class procedures** before you deliver *AI in Cybersecurity*.

**Your role:** Listen, take notes, and confirm logistics. You are not expected to teach the course on this call.

---

## Before the Call (10 minutes)

### Have these open

| Item | Location / notes |
|------|------------------|
| Course overview | [`README.md`](README.md) |
| Lab sequence (6 labs, 2 days) | [`labs/`](labs/) |
| Student VM roster | [`vms.md`](vms.md) — **do not share credentials on the call** |
| Your calendar | Block time for delivery dates, setup, and any pre-class tech check |

### Know your course at a glance

| Detail | Value |
|--------|-------|
| **Title** | AI in Cybersecurity |
| **Format** | Instructor-led, hands-on |
| **Duration** | 2 days |
| **Audience** | SOC analysts, detection engineers, security practitioners |
| **Platform** | AWS (`us-east-1`), EC2, GuardDuty, Security Hub, CloudWatch, Amazon Bedrock |
| **Student tools** | VS Code + Remote SSH, Python 3, Bash, AWS Console / CloudShell |
| **Labs** | 6 sequential labs — Day 1: 1.1–1.3 · Day 2: 2.1–2.3 |

### Pre-call checklist

- [ ] Confirm meeting link, dial-in, and time zone
- [ ] Confirm who is attending (training coordinator, tech support, security liaison, etc.)
- [ ] Test audio/video if the call is on Teams/Zoom/WebEx
- [ ] Have a blank notes section ready (see [During the Call](#during-the-call))
- [ ] Know your delivery dates (or note that you need them from Wells Fargo)

---

## Suggested Agenda (30 minutes)

Use this if the Wells Fargo contact does not provide one. They may lead entirely — that is fine.

| Time | Topic | Your goal |
|------|-------|-----------|
| **0–5 min** | Introductions | Names, roles, delivery dates, class size |
| **5–20 min** | **Wells Fargo class procedures** | Listen and document their process |
| **20–27 min** | Course-specific logistics | Confirm AWS access, VMs, software, timing |
| **27–30 min** | Next steps | Pre-class tech check, materials handoff, follow-up contacts |

---

## What Wells Fargo Will Likely Cover

Listen for and write down specifics on each area:

### 1. Before class

- How far in advance students receive invites and materials
- Who provisions AWS / lab accounts (Wells Fargo IT vs. Innovation in Software)
- Required pre-work or prerequisites communication to students
- Whether students use **personal AWS accounts** or **corporate-provided accounts**
- VPN, proxy, or firewall rules that affect AWS Console, SSH, or Bedrock

### 2. Day-of logistics

- Class start/end times and breaks (lunch, bio breaks)
- Virtual vs. in-person (or hybrid) setup
- How students join (Teams, Zoom, WebEx, internal LMS)
- Screen sharing: instructor only, or can students share for help?
- Co-instructor or Wells Fargo TA on the call?
- Escalation path if a student is locked out or behind

### 3. Technical environment

- Student machine requirements (admin rights, VS Code install, browser)
- Whether labs run on **provided VMs** (see `vms.md`) or student laptops
- AWS region restrictions (course uses **`us-east-1`**)
- Bedrock model access — enabled in student accounts?
- GuardDuty / Security Hub — who enables them, and when?
- Recording policy (class sessions, labs, or instructor screen)

### 4. Security and compliance

- Data handling rules (logs, screenshots, incident reports)
- Whether attack simulations (sudoers backdoor, failed SSH, etc.) need extra approval
- Credential handling (`.pem` keys, access codes) — distribution method
- What students are **not** allowed to do on corporate networks or accounts

### 5. After class

- Survey or feedback process
- Lab environment teardown timeline
- Follow-up support channel for students
- Invoice / PO / administrative close-out

---

## Questions to Ask (pick what they do not cover)

### Class procedures

1. What is the standard **day-of run sheet** (login, attendance, breaks, end-of-day)?
2. Who is my **primary point of contact** during the two delivery days?
3. Is there a **help desk or Slack/Teams channel** for live student issues?
4. How do you handle students who arrive **without prerequisites** (no AWS access, no VS Code)?
5. What is the **late-join / early-leave** policy?

### Technical

6. Are students using the **pre-provisioned IIS student accounts** (`iis-student##`), or their own?
7. Is **`us-east-1`** acceptable, or must we use another region?
8. Has **Amazon Bedrock** been enabled and tested in student accounts?
9. Do students have permission to create EC2 instances, IAM roles, GuardDuty, and Security Hub?
10. Is there a **pre-class tech check** date with 2–3 pilot students?

### Content and timing

11. Expected **class size** and skill mix (beginner vs. experienced SOC)?
12. Any topics to **emphasize or avoid** for Wells Fargo context?
13. Is the full **2-day / 6-lab** schedule confirmed, or should we plan cut points?  
    - Day 1 minimum: Labs 1.1–1.2  
    - Day 1 stretch: Lab 1.3 (GuardDuty findings can lag 10–30 min)  
    - Day 2 minimum: Labs 2.1–2.2  
    - Capstone 2.3 is optional if time is short
14. Will sessions be **recorded**? If yes, who receives the recording?

### Administrative

15. Who sends the **student welcome email**, and what should it link to?
16. What **materials** do you need from me (slides, lab PDFs, instructor guide)?
17. What are the **payment / SOW / sign-off** steps after delivery?

---

## Course Facts to Share (if they ask)

Keep answers short — defer deep technical questions to the pre-class tech check.

| Topic | Short answer |
|-------|----------------|
| **What students build** | A mini-SOC on AWS: EC2 lab host, auditd/nginx telemetry, Bedrock triage, GuardDuty, CloudWatch pipelines, dashboards, AI investigations |
| **Attack activity** | Controlled, non-destructive simulations only (failed SSH, web probes, sudoers backdoor) — no malware or exploit frameworks |
| **AWS cost** | Training accounts; GuardDuty/Security Hub have a 30-day free trial |
| **Timing risks** | GuardDuty findings may take 10–30 minutes; Security Hub posture findings up to 60 minutes on new accounts |
| **Prerequisites** | Basic Python, foundational security concepts, AWS account with EC2/IAM/GuardDuty permissions, VS Code + Remote SSH |
| **Instructor needs** | Same AWS access as students, ability to share screen, stable internet, slides + lab guides |

---

## During the Call

### Introduction script (~30 seconds)

> "Thanks for making time. I'm [your name], instructor for **AI in Cybersecurity** — a two-day hands-on course on AWS security operations and AI-assisted investigation. I understand today is mainly for you to walk me through Wells Fargo's class procedures. I'll take notes and follow up on anything that needs a tech check before we go live."

### Notes template

Copy this section and fill in during the call.

```
Date:
Wells Fargo attendees:
Delivery dates:
Class size:
Format (virtual / in-person):

─── BEFORE CLASS ───
Student invite timeline:
Materials distribution:
AWS account model:
Pre-work sent to students:
Pre-class tech check date:

─── DAY OF ───
Start / end times:
Break schedule:
Platform (Teams / Zoom / etc.):
Wells Fargo support on call:
Student escalation path:

─── TECHNICAL ───
Student VMs or laptops:
AWS region:
Bedrock enabled (Y/N):
GuardDuty / Security Hub — who enables:
VPN / firewall issues:
Recording allowed (Y/N):

─── SECURITY / COMPLIANCE ───
Credential distribution method:
Restricted activities:
Approval needed for attack sims (Y/N):

─── AFTER CLASS ───
Feedback / survey:
Environment teardown:
Admin / invoice contact:

─── ACTION ITEMS ───
| Owner | Action | Due |
|-------|--------|-----|
|       |        |     |
|       |        |     |

─── CONTACTS ───
Primary WF contact:
Tech support:
Backup instructor / IIS contact:
```

---

## After the Call

### Same day

- [ ] Email a brief **summary + action items** to your Wells Fargo contact
- [ ] Flag any **blockers** (Bedrock access, region, IAM permissions, VM access)
- [ ] Schedule **pre-class tech check** if not already set
- [ ] Update internal docs if procedures differ from prior deliveries

### One week before class

- [ ] Run through **Lab 1.1** end-to-end in a test account matching student permissions
- [ ] Verify Bedrock invoke works from EC2 / CloudShell
- [ ] Confirm student roster matches `vms.md` (or updated list from Wells Fargo)
- [ ] Send instructor one-pager or welcome email draft if WF requested it

---

## Red Flags to Escalate Early

Raise these immediately — they can block the entire class if unresolved:

| Issue | Why it matters |
|-------|----------------|
| Bedrock not enabled | Lab 1.2+ depends on AI triage |
| Students cannot create EC2 / IAM roles | Lab 1.1 cannot start |
| Wrong AWS region | Lab AMI and steps assume `us-east-1` |
| SSH blocked from student networks | VS Code Remote SSH will fail |
| GuardDuty org-level restrictions | Lab 1.3 findings may never appear |
| No admin rights on student laptops | Cannot install VS Code or SSH keys |

---

## Quick Reference Links

| Resource | Link |
|----------|------|
| Course README | [`README.md`](README.md) |
| Lab 1.1 — Instance Setup | [`labs/1.1-Instance-Setup.md`](labs/1.1-Instance-Setup.md) |
| Glossary | [`labs/glossary.md`](labs/glossary.md) |
| Student accounts | [`vms.md`](vms.md) |

---

*Innovation In Software Corporation · AI in Cybersecurity · Wells Fargo delivery prep*
