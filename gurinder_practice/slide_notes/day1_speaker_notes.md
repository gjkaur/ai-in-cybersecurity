# Day 1 — Speaker Notes

Use with **Cybersecurity-AI-day1.pdf**. One section per slide (from slide 6).

---

## Slide 6 — What Is Cybersecurity?

### Instructor Opening (How to Start Teaching)

Ask the class:

> "How many of you use online banking?"

> "How many use Gmail?"

> "How many use Amazon or online shopping?"
Then ask:

> "What would happen if someone stole your password?"

> "What if a hacker modified your bank balance?"

> "What if Amazon's website stopped working for 24 hours?"
Tell them:

> Cybersecurity exists to prevent exactly these situations.

### Formal Definition

Cybersecurity is the practice of protecting:

* Systems
* Networks
* Applications
* Devices
* Data

from:

* Unauthorized access
* Theft
* Damage
* Disruption
* Cyber attacks

### Simple Definition for Beginners

Tell students:

> Cybersecurity is like security guards, locks, cameras, and alarm systems for the digital world.
Physical World:

- House
- Door Lock
- Security Camera
- Alarm System

Digital World:

- Computer System
- Password
- Firewall
- Security Monitoring

### Why Cybersecurity Exists

Organizations depend on:

* Websites
* Databases
* Cloud systems
* Email
* Mobile apps

Without cybersecurity:

- Hackers
- Malware
- Ransomware
- Data Theft
- Service Outages
- Financial Loss

become common.

---

---

## Slide 7 — The Cia Triad

### CIA Triad

Every cybersecurity framework is built around these three principles.

### Availability

Known as:

### Advanced Concept: Security Controls Map to CIA

Show this table:

| Control            | C | I | A |
| ------------------ | - | - | - |
| Encryption         | ✓ |   |   |
| MFA                | ✓ |   |   |
| IAM Policies       | ✓ |   |   |
| Hashing            |   | ✓ |   |
| Digital Signatures |   | ✓ |   |
| Audit Logs         |   | ✓ |   |
| Backups            |   |   | ✓ |
| Load Balancer      |   |   | ✓ |
| Auto Scaling       |   |   | ✓ |
| Disaster Recovery  |   |   | ✓ |

### Key Takeaway for Students

At the end of this slide, say:

> Cybersecurity is not just about stopping hackers.

> It is about protecting the confidentiality, integrity, and availability of digital systems while managing risks from constantly evolving threats.

> In this course, we will learn how AI helps security teams detect, investigate, and respond to those threats more efficiently.

---

---

## Slide 8 — The Modern Threat Landscape

### Threat

Something capable of causing harm.

Examples:

- Hacker
- Malware
- Insider

---

### Important Concept: Attack Surface

This is not directly on the slide but extremely important.

### Ransomware

Files become inaccessible.

### 2. Credential Theft

The slide states:

> Credential theft is now the leading initial access technique.
This is extremely important.

### 3. Supply Chain Attacks

Most students struggle with this concept.

---

### 4. Cloud Misconfigurations

This is probably the most important topic for your AWS-based course.

---

### Key Takeaway

> AWS secures the cloud infrastructure, but customers secure everything they deploy within that infrastructure. Most cloud security incidents are caused by customer-controlled misconfigurations, making identity management, access controls, logging, encryption, and proper configuration critical responsibilities for every cloud security team.

---

---

## Slide 9 — Cloud Computing And The New Perimeter

### Cloud Computing and the New Perimeter

This is one of the most important conceptual slides in modern cybersecurity.

Many beginners think cybersecurity means:

- Firewall
- +
- Antivirus
- +
- Passwords

That was largely true 15–20 years ago.

Today, cybersecurity is much more about:

- Identity
- Access Control
- Cloud Security
- Zero Trust

This slide explains **why cloud computing fundamentally changed security**.

### Castle-and-Moat Security

Like a medieval castle.








The firewall was the moat.

Once inside:

 `Trust was assumed.`

### Identity is the New Firewall

This phrase appears everywhere in cloud security.

Old model:








Modern model:








### Traditional Office

Imagine a company in 2005.








Security looked like a castle.








Everything important was inside.

---

Now ask:

---

---

## Slide 10 — Cloud Computing And The New Perimeter

### Shared Responsibility Model

Important AWS concept.

AWS secures:

 `Cloud Infrastructure`

Customer secures:

- Applications
- Data
- IAM
- Configurations

Misconfiguration is usually the customer's responsibility.

### Cloud Provider Responsibility

AWS secures:

### Customer Responsibility

The customer secures:

- Data
- Users
- Passwords
- IAM
- Applications
- Configurations

This is where most breaches occur.

---

---

## Slide 11 — Aws And Cloud Infrastructure

### AWS and Cloud Infrastructure

This slide is introducing AWS before diving into security services like IAM, CloudTrail, CloudWatch, Security Hub, and GuardDuty.

As an instructor, don't just explain AWS. Explain **why AWS exists**, **how cloud computing evolved**, and **why cybersecurity professionals must understand cloud infrastructure**.

### What is AWS?

AWS stands for:

### /

Entire operating system.

---

### -w

`Watch this file`

File:

 `/etc/passwd`

---

---

---

## Slide 12 — Aws And Cloud Infrastructure

### Regions

A region is a geographical location.

Examples:

- Canada Central
- US East (Virginia)
- US West (Oregon)
- Europe (Ireland)
- Asia Pacific (Tokyo)

### Availability Zones (AZs)

Each region contains multiple AZs.

Example:








Purpose:

- High Availability
- Fault Tolerance

### Overly Permissive IAM

```json
{
  "Action":"*",
  "Resource":"*"
}
```

Too much access.

---

### 4. VPC

Virtual Private Cloud

Think:

 `Private Network Inside AWS`

---

---

## Slide 13 — Aws And Cloud Infrastructure

### EC2 (IaaS)

Customer manages:

- OS
- Applications
- Data
- Users

Most responsibility.

### Connecting Everything Together

Draw this on the whiteboard:








### Where is the resource?








---

---

## Slide 14 — Virtual Machines And Ec2 Instances

### Q: Is AWS just virtual machines?

No.

AWS provides:

- Compute
- Storage
- Databases
- Networking
- Security
- AI
- Analytics

Hundreds of services.

### C2

`Suspicious Outbound Traffic`

---

---

## Slide 15 — Launching Ec2 Instances Safely

### Launching EC2 Instances Safely

This slide is extremely practical.

Previous slides explained:

- What is EC2?
- What is IAM?
- What is a Security Group?
- What is a Key Pair?

This slide answers:

> "Now that we know how to launch an EC2 instance, how do we launch it securely?"
Tell students:

> "Most AWS security incidents don't happen because AWS is insecure. They happen because someone launched a server with bad security settings."
This slide is basically an **EC2 Security Checklist**.

### EC2 Security Checklist

Let's go through each recommendation.

### Open Security Groups

`0.0.0.0/0`

Allows access from anywhere.

---

### 3. Key Pair

One of the most important security concepts.

---

---

## Slide 16 — Ssh — Secure Shell

### Weak SSH Access

`Port 22 Open`

to everyone.

---

### Secure Shell

Used for:

 `Remote Administration`

Example:

```bash
ssh -i mykey.pem ec2-user@server
```

---

---

## Slide 17 — Ssh Key-Based Authentication

### SSH Key-Based Authentication

This slide explains **how SSH actually proves your identity** when connecting to a Linux server or AWS EC2 instance.

As an instructor, tell students:

> "Passwords answer the question: 'Do you know the secret?'

> SSH keys answer the question: 'Can you prove you own the cryptographic key?'"
This is one of the most important concepts in cloud security.

### 2. Use Key-Based Authentication

The slide recommends:

> Disable password-based SSH login.
This is a huge security improvement.

### Can someone log in with only the public key?

No.

The public key is meant to be public.

Authentication requires:

 `Private Key`

### What happens if I lose the private key?

Access becomes difficult.

This is a common AWS beginner mistake.

---

---

## Slide 18 — Navigating The Linux Filesystem

### Navigating the Linux Filesystem

This slide is extremely important because cybersecurity professionals spend much of their time investigating Linux systems.

Tell students:

> "When an incident happens, you become a digital detective. To investigate, you must know where Linux stores logs, configurations, user accounts, running processes, and evidence."
This slide teaches the **Linux File System Hierarchy (FHS)**.

### Controls Used

* Passwords
* MFA
* Encryption
* IAM permissions

AWS Example:

 `IAM Policy`

determines who can access an S3 bucket.

---

---

## Slide 19 — Linux File Permissions

### Linux File Permissions

This is one of the most important Linux security topics because **permissions determine who can access, modify, or execute files**.

Tell students:

> "Many Linux compromises don't happen because of a software vulnerability. They happen because someone gave the wrong permissions to the wrong file."
For cybersecurity professionals, understanding permissions is essential for:

- Access Control
- Privilege Escalation Prevention
- System Hardening
- Incident Response
- Forensics

### Why chmod 600 key.pem?

```bash
chmod 600 key.pem
```

This is extremely important in AWS.

### Q: What does rwx mean?








---

---

## Slide 20 — Setuid Binaries And Privilege Risk

### SetUID Binaries and Privilege Risk

This is one of the most important **Linux Privilege Escalation** topics in cybersecurity.

Tell students:

> "Most attackers don't start with root access. Their goal is to become root. SetUID is one of the most common paths used to gain elevated privileges."
This slide introduces a concept frequently seen in:

- Penetration Testing
- Red Teaming
- Privilege Escalation
- Incident Response
- Linux Hardening

### Risk

Likelihood that a threat exploits a vulnerability.

Formula:

 `Risk = Threat × Vulnerability × Impact`

### SUID Files

```bash
find / -perm -4000
```

---

---

## Slide 21 — Setuid Binaries And Privilege Risk

### Finding and Investigating SetUID Binaries

This slide builds on the previous SetUID concept and teaches students **how security analysts actually discover dangerous SetUID programs on Linux systems**.

Tell students:

> "Knowing what SetUID is is only half the job. The real cybersecurity skill is being able to find unexpected SetUID files before attackers use them."
This is a common activity in:

- Threat Hunting
- Incident Response
- Linux Hardening
- Security Audits
- Penetration Testing

---

---

## Slide 22 — Security Groups As Firewalls

### Group

Collection of users.

Example:

- Developers
- Administrators
- Security Team

---

### Security Groups as Firewalls

This is one of the most important AWS security concepts.

Tell students:

> "If IAM controls who can access AWS resources, Security Groups control who can reach your servers over the network."
A huge percentage of cloud breaches happen because:

 `A Security Group Was Misconfigured`

### Inbound Traffic

Traffic entering server.

Examples:

- SSH
- HTTPS
- HTTP
- Database Connections

### Outbound Traffic

Traffic leaving server.

Examples:

- Internet Access
- API Calls
- Database Queries

---

---

## Slide 23 — Running And Securing A Web Service

### Amazon Web Services

Launched:

 `2006`

by Amazon.

Today AWS is the world's largest cloud provider.

### Nginx

Pronounced:

 `Engine-X`

Popular because it is:

- Fast
- Lightweight
- Scalable

### Why Nginx?

The slide uses:

 `Nginx`

because it is one of the most widely deployed web servers today.

Major websites use Nginx.

### Running and Securing a Web Service

This slide brings together many concepts you've already covered:

- Linux
- EC2
- Security Groups
- SSH
- Permissions
- Logs
- Monitoring

Tell students:

> "A web server is one of the most commonly attacked systems on the internet. The moment you expose a website to the public, attackers begin scanning it automatically."
This slide teaches how to run a web service securely.

---

---

## Slide 24 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 25 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 26 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 27 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 28 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 29 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 30 — Lab 1.1

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 31 — The Soc Analyst Role

### What does a SOC analyst see?

Not hackers directly.

They see:

- Failed Logins
- Suspicious API Calls
- New IAM Users
- Unusual Network Traffic
- Privilege Escalation Attempts

Their job is to determine:

- Threat
- or
- False Positive

AI helps with that decision-making process.

---








### How SOC Teams Use SSH Logs

SOC analysts investigate:

- Repeated Login Failures
- Logins From Foreign Countries
- Root Login Attempts
- New SSH Keys Added

These often indicate attacks.

### What Does a SOC Monitor?

SOC analysts continuously monitor:

- Servers
- Cloud Infrastructure
- Networks
- Applications
- Databases
- User Activity
- Endpoints

---

---

## Slide 32 — The Cyber Kill Chain

### The Cyber Kill Chain

This is one of the most important cybersecurity frameworks you'll teach.

Tell students:

> "Most attacks don't happen in a single step. Attackers follow a sequence of activities. If defenders can detect and stop any one of those stages, the attack can be prevented."
The Cyber Kill Chain was developed by Lockheed Martin to understand how cyber attacks progress.

### Reconnaissance

Analyze large datasets quickly.

---

---

## Slide 33 — The Cyber Kill Chain

### Vulnerability Exploitation

Outdated software.

### Malware Installation

Compromised servers.

### Action

```json
"s3:GetObject"
```

Means:

 `Read Objects`

only.

---

---

## Slide 34 — Mitre Att&Ck Framework

### Cyber Kill Chain vs MITRE ATT&CK

Students may ask.

### MITRE ATT&CK

Focuses on:

 `Specific Attacker Techniques`

Hundreds of detailed behaviors.

---

---

## Slide 35 — Brute Force And Credential Attacks —

### Brute Force SSH

Trying passwords repeatedly.

### BRUTE FORCE AND CREDENTIAL ATTACKS (MITRE ATT&CK T1110)

This is one of the most common real-world attacks and a favorite topic in cybersecurity interviews, SOC operations, and cloud security.

---

---

## Slide 36 — Privilege Escalation — T1548

### Detect Privilege Escalation

Example:








AI identifies unusual behavior.

### PRIVILEGE ESCALATION (MITRE ATT&CK T1548)

This is one of the most important concepts in cybersecurity because attackers rarely start with full administrative access.

Most attacks follow this pattern:








A great statement for class:

> "Getting into a system is often easy. Becoming root is where the real battle begins."

---

---

## Slide 37 — Why Logs Are The Foundation Of

### Logs

```bash
/var/log
```

### Why?

Imagine attacker exploits Nginx.

Question:

What permissions does attacker get?

---

If Nginx runs as:

 `root`

attacker gains:

 `root access`

---

Very bad.

---

---

## Slide 38 — Linux Logging — Journald And

### LINUX LOGGING — JOURNALD AND AUDITD

This slide introduces the two most important logging systems on modern Linux servers:

1. **systemd-journald (journald)**
2. **Linux Audit Daemon (auditd)**

A SOC analyst will frequently use both when investigating Linux incidents.

### auditd

Focuses on:

- Security auditing
- System calls
- File access
- Privilege changes
- Process execution

Examples:

- Sensitive file access
- Privilege escalation
- User creation
- Policy violations

### Linux

Linux uses:

 `/`

called:

---

---

## Slide 39 — Collecting Ssh Evidence

### COLLECTING SSH EVIDENCE

This slide introduces one of the most important evidence sources for SOC analysts: **SSH authentication logs**.

Every Linux server exposed to the internet receives SSH traffic. Analysts use these logs to identify:

* Brute-force attacks
* Password spraying
* Successful logins
* Unauthorized access attempts
* Automated scanning activity
* Initial access events

---

---

## Slide 40 — Evidence And The Analyst Workflow

### EVIDENCE AND THE ANALYST WORKFLOW

This slide introduces the core investigative process used by SOC analysts. The key message is simple:

> **Good decisions come from good evidence.**
Analysts should never jump directly from an alert to a conclusion. Instead, they follow a structured workflow to collect, validate, analyze, and document evidence.

---

---

## Slide 41 — Risk Scoring Fundamentals

### RISK SCORING FUNDAMENTALS

This slide introduces one of the most important concepts in modern SOC operations:

> **Not every alert deserves the same level of attention.**
Risk scoring helps analysts prioritize investigations by assigning a numerical value to suspicious activity, users, hosts, IP addresses, or alerts.

### Example: User Risk Score

Events observed:

- 5 Failed Logins = 10 points
- Successful Login from New Country = 30 points
- Privilege Escalation = 40 points

Total:

 `Risk Score = 80`

Result:

 `Very High Risk`

Immediate analyst review required.

---

---

## Slide 42 — Risk Scoring Fundamentals

### Why Risk Scoring Exists

A SOC may receive:

 `10,000+ alerts per day`

Analysts cannot investigate everything immediately.

Without prioritization:

- Critical attacks may be missed
- Analysts waste time on low-value alerts
- Alert fatigue increases
- Response times slow down

Risk scoring helps answer:

 `What should I investigate first?`

### PYTHON FOR SECURITY AUTOMATION

Python is the most widely used programming language for security automation because it combines simplicity, readability, and a powerful standard library. Security analysts use Python to automate repetitive tasks such as log parsing, threat detection, IOC enrichment, reporting, and alert generation.

### Security Automation

Reduce analyst workload.

---

---

## Slide 43 — Python For Security Automation

### Why Python Is Popular in Cybersecurity

* Easy to learn and maintain
* Cross-platform (Windows, Linux, macOS)
* Extensive security ecosystem
* Excellent support for APIs and cloud services
* Large community and open-source tooling

Common cybersecurity use cases:

* Log analysis
* Threat intelligence processing
* Vulnerability scanning
* Security monitoring
* Incident response automation
* Malware analysis
* SIEM integrations

### Example Security Automation Workflow








### Scoring Is a Triage Tool, Not a Verdict

Risk scoring helps prioritize investigations but does not prove malicious activity.

Analyst responsibilities:

1. Review supporting evidence
2. Validate event context
3. Eliminate false positives
4. Determine actual impact
5. Decide response actions

Example:

- Risk Score: 75
- Reason:
- Administrator performed approved maintenance
- Result:
- False Positive

High score does not automatically mean compromise.

---

---

## Slide 44 — Triage Notes And Documentation

### TRIAGE NOTES AND DOCUMENTATION

A triage note is the analyst’s written record of an investigation. It captures what was observed, why it matters, and what actions should follow. Good documentation ensures investigations can be reviewed, validated, escalated, and audited later.

### Why Documentation Matters

Documentation enables:

- Handoffs
- Escalations
- Management reporting
- Incident response
- Legal review
- Compliance audits

---

---

## Slide 45 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 46 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 47 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 48 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 49 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 50 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 51 — Lab 1.2

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 52 — Ai In Cybersecurity — Overview

### How CIA Relates to AI in Cybersecurity

This is the bridge to the rest of your course.

AI helps security teams:

- Detect Confidentiality Violations
- Detect Integrity Violations
- Detect Availability Attacks

Examples:

* AI detecting data exfiltration
* AI detecting suspicious changes
* AI detecting service outages

### AI IN CYBERSECURITY — OVERVIEW

Artificial Intelligence (AI) is transforming cybersecurity by helping security teams analyze large volumes of data, detect threats faster, automate repetitive tasks, and improve decision-making. Rather than replacing analysts, AI acts as a force multiplier that allows security professionals to focus on higher-value investigations.

---

---

## Slide 53 — Ai In Cybersecurity — Overview

### How This Relates to AI in Cybersecurity

Later in the course:

### AI IN CYBERSECURITY — OVERVIEW (PRACTICAL APPLICATIONS)

Artificial Intelligence is rapidly becoming an operational tool within Security Operations Centers (SOCs), cloud security teams, and incident response workflows. Rather than replacing analysts, AI helps automate repetitive tasks, accelerate investigations, and surface insights hidden within large datasets.

### Limitations of AI

AI is powerful but imperfect.

Common challenges:

##### False Positives

Benign activity may be flagged as malicious.

##### False Negatives

Real threats may be missed.

##### Hallucinations

Generative AI may provide incorrect information.

##### Bias

Training data can influence model behavior.

##### Lack of Context

AI often lacks business-specific knowledge.

---

---

## Slide 54 — Ai Coding Assistants For Security

### AI CODING ASSISTANTS FOR SECURITY WORK

AI-powered coding assistants such as Amazon Q, Claude, ChatGPT, GitHub Copilot, and Cursor have become valuable productivity tools for cybersecurity professionals. They enable analysts, engineers, and responders to generate scripts, queries, detection rules, and automation workflows using natural language instructions instead of writing everything from scratch.

### Why Security Teams Use AI Coding Assistants

Security work often requires:

* Parsing large log files
* Writing automation scripts
* Building detection logic
* Creating cloud security policies
* Investigating incidents

AI assistants reduce development time by generating initial working code that analysts can review, test, and refine.

---

---

## Slide 55 — Prompt Engineering For Security

### PROMPT ENGINEERING FOR SECURITY TASKS

Prompt engineering is the process of crafting clear, structured instructions that guide AI systems to produce accurate, useful, and secure outputs. In cybersecurity, the quality of generated scripts, detection rules, policies, and investigations depends heavily on the quality of the prompt provided.

### Example SOC Prompt

- Analyze these SSH logs and identify
- suspicious authentication activity.
- Provide:
- - Summary
- - Risk level
- - Supporting evidence
- - Recommended next steps

Possible AI Output:

- Risk: High
- Evidence:
- - 27 failed logins
- - Password spray behavior
- - Successful login from same IP
- Recommendation:
- Investigate account compromise and
- review subsequent activity.

---

---

## Slide 56 — Reviewing And Validating Ai Output

### REVIEWING AND VALIDATING AI OUTPUT

As AI-generated code becomes more common in cybersecurity operations, validation becomes a critical skill. While AI can rapidly generate scripts, detection rules, IAM policies, and automation workflows, it can also introduce security flaws, logical errors, and unsafe practices. Security professionals must treat AI output as a draft that requires thorough review before use.

---

---

## Slide 57 — Iam Fundamentals

### IAM

Identity and permissions.

Most directly related.

### What is IAM?

IAM stands for:

---

---

## Slide 58 — Iam Policy Structure

### Policy

Permission document.

Example:

```json
Allow:
Read S3
```

### IAM Policy Structure

Every policy contains:

---

---

## Slide 59 — The Principle Of Least Privilege

### Principle of Least Privilege

Very important security concept.

Give only:

 `Minimum Required Access`

Example:

Bad:

```json
Action: *
Resource: *
```

---

Good:

 `Read Specific Bucket`

Only.

### Principle of Least Privilege and Cybersecurity

This principle exists everywhere.

---

---

## Slide 60 — The Principle Of Least Privilege

### IAM Roles, Least Privilege, EC2, VPC and S3 Access

This slide is extremely important because it introduces one of the **most fundamental security principles in cloud security**:

### 6. Lambda

Serverless Computing

Run code without managing servers.

Example:

- Upload Function
- Run When Needed

---

---

## Slide 61 — Lambda Execution Roles

### Execution

Run malicious code.

Examples:

- PowerShell
- Python
- Shell Scripts

---

### Role

Temporary permissions.

Used by:

- EC2
- Lambda
- Applications

---

---

---

## Slide 62 — S3 Resource-Level Access Control

### Resource

```json
"arn:aws:s3:::my-app-data/*"
```

Means:

 `Only This Bucket`

### Source

Who is allowed?

Example:

 `203.0.113.15/32`

means:

 `Only One IP`

---

---

## Slide 63 — Detecting Iam Misconfigurations

### Misconfigurations

Most common issue.

Examples:

- Public S3 Bucket
- Open Security Group
- Weak IAM Policy

---

---

---

## Slide 64 — Human-In-The-Loop Validation

### Human-in-the-Loop Security

The most effective security model combines:








AI assists.

Humans remain accountable for security decisions.

### Human-in-the-Loop Principle

The most effective model is:








The analyst remains responsible for final decisions.

---

---

## Slide 65 — Ai Limitations In Security Contexts

### AI Limitations in Security Contexts

Artificial Intelligence can significantly improve analyst productivity, automate repetitive tasks, and accelerate investigations. However, AI is not a replacement for security expertise. Understanding its limitations is critical to using it safely in security operations.

Security decisions impact confidentiality, integrity, and availability. A single incorrect recommendation can introduce vulnerabilities, expose sensitive data, or disrupt business operations.

---

### Security

Compromised credentials cause less damage.

---

---

## Slide 66 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 67 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 68 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 69 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 70 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 71 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 72 — Cloud Security Posture Management

### Cloud Security Posture Management (CSPM)

Cloud Security Posture Management (CSPM) is a continuous security discipline focused on discovering, assessing, prioritizing, and remediating misconfigurations across cloud environments. CSPM solutions provide automated visibility into cloud resources and compare configurations against security best practices, compliance frameworks, and organizational policies.

As cloud environments scale, manual reviews become impractical. CSPM helps organizations continuously monitor their security posture and reduce the risk of breaches caused by configuration mistakes.

---

### Why CSPM Matters

Industry studies consistently show that cloud misconfigurations are one of the leading causes of cloud security incidents.

Common examples include:

* Publicly accessible S3 buckets
* Overly permissive IAM policies
* Unrestricted security groups
* Unencrypted storage resources
* Disabled logging and monitoring
* Unused privileged accounts

A single configuration error can expose sensitive data or create opportunities for attackers.

### What?

`What action occurred?`

Example:

- Login
- File deletion
- Program execution

---

---

## Slide 73 — Cloud Security Posture Management

### The CSPM Lifecycle








CSPM is not a one-time audit—it is an ongoing process.

---

---

## Slide 74 — Aws Security Services Overview

### AWS Security Services Overview

AWS provides a comprehensive set of native security services that help organizations detect threats, monitor configurations, enforce access controls, identify vulnerabilities, and maintain compliance. Rather than relying on a single security product, AWS follows a defense-in-depth approach where multiple services work together to provide visibility across the entire cloud environment.

### Integration with Other AWS Security Services

| Service          | Contribution              |
| ---------------- | ------------------------- |
| GuardDuty        | Threat detection findings |
| Inspector        | Vulnerability findings    |
| AWS Config       | Configuration compliance  |
| Access Analyzer  | External access findings  |
| Firewall Manager | Network security findings |
| CloudTrail       | Investigation evidence    |

Security Hub becomes the central investigation portal.

---

---

## Slide 75 — Aws Security Hub

### Security Hub

Finds security issues.

### AWS Security Hub

Centralized security findings aggregation.

Capabilities:

* CIS benchmark checks
* Security scorecards
* Cross-service visibility

---

---

---

## Slide 76 — Aws Security Hub

### Security Hub Findings

AWS Security Hub can identify:

* Root account usage
* Missing MFA
* Excessive permissions
* IAM best-practice violations

---

### Finding Aggregation

Collects findings from multiple AWS security services and partner tools.

### GuardDuty

Detects threats.

---

---

## Slide 77 — Amazon Guardduty

**Speaker notes:** Expand on the on-slide bullets using your own examples.

---

---

## Slide 78 — Root Account Security And Mfa

### /root

Home directory of the root user.

### Multi-Factor Authentication (MFA)

- Password
- +
- Phone Verification

### User

Represents a person.

Example:

- gurinder
- john
- alice

---

---

---

## Slide 79 — Iam Credential Hygiene

### IAM Credential Hygiene

IAM credential hygiene is the ongoing process of managing identities, credentials, and permissions to minimize security risk. Poor credential management is one of the most common causes of cloud security incidents because attackers frequently target forgotten accounts, exposed access keys, and excessive permissions.

Credential hygiene ensures that only authorized users have access, credentials are regularly reviewed, and unused access paths are removed before they can be exploited.

### Why use Roles instead of Access Keys?

Roles provide:

- Temporary Credentials
- Automatic Rotation
- No Secrets Stored

Much safer.

### What Is an IAM Credential?

IAM credentials include:

---

---

## Slide 80 — Network Exposure — Security Groups

### Security Groups

Virtual firewalls.

Extremely important.

### su

Switch user accounts.

---

These are expected.

---

---

## Slide 81 — Network Exposure — Security Groups

### 4. Security Groups

This is the most important part of the slide.

### Network Exposure — Security Groups

A security group acts as a virtual firewall that controls inbound and outbound traffic for AWS resources such as EC2 instances, RDS databases, and load balancers. Misconfigured security groups are one of the most common causes of cloud security incidents because they can unintentionally expose services directly to the internet.

An open security group rule allowing traffic from **0.0.0.0/0** or **::/0** makes a service reachable from anywhere in the world.

### SSH Login

```bash
ssh -i mykey.pem ec2-user@server
```

The private key proves your identity.

---

---

## Slide 82 — S3 Bucket Security

### S3 Bucket Security

Amazon S3 is one of the most widely used AWS services and one of the most frequent sources of cloud security incidents. Misconfigured S3 buckets have led to major data breaches involving customer records, financial data, healthcare information, source code, and intellectual property.

Because S3 is designed for scalable data sharing, security controls must be carefully configured to prevent accidental public exposure.

### Why S3 Security Matters

A single misconfigured bucket can expose millions of records.

```text
Sensitive Data
      ↓
Misconfigured Bucket
      ↓
Public Access
      ↓
Data Breach
```

Examples of exposed data:

* Customer information
* Financial records
* Source code repositories
* Backup files
* Internal documents
* Application logs

### Block Public Access

Prevents accidental public exposure.

---

---

## Slide 83 — Aws Cloudtrail — Audit Logging

### CloudTrail

Records:

- Who modified IAM?
- Who deleted S3 bucket?
- Who changed permissions?

CloudTrail primarily supports integrity and accountability.

### Logging

`Monitor access.log`

---

---

## Slide 84 — Finding Prioritization And Severity

### Finding Prioritization








### Severity Thresholds

Organizations define thresholds to classify risk levels.

Example:

| Score Range | Severity |
| ----------- | -------- |
| 0–19        | Low      |
| 20–39       | Medium   |
| 40–69       | High     |
| 70+         | Critical |

As additional suspicious activity occurs, an entity can move from Low to Critical.

Example:

- Current Score = 35 (Medium)
- Privilege Escalation Event = +25
- New Score = 60 (High)

---

---

## Slide 85 — Controlled Remediation Principles

### Controlled Remediation Principles

Cloud security findings should never be remediated through large-scale, untested changes. Every remediation action must be planned, tested, documented, and reversible. The objective is to reduce security risk without introducing service outages, data loss, or operational instability.

Security teams must balance **risk reduction** with **business continuity**.

---

---

## Slide 86 — Controlled Remediation Principles

### Why Controlled Remediation Matters

A poorly executed fix can be more damaging than the original security issue.

Example:








Instead:








### 5. Remediation Guidance

Modern CSPM tools provide:

* Detailed findings
* Recommended fixes
* Infrastructure-as-Code remediation
* Automated remediation workflows

Example:

- Finding:
- S3 Bucket Publicly Accessible
- Recommendation:
- Disable Public Access Block
- Remove Public ACLs
- Review Bucket Policy

---

---

## Slide 87 — Continuous Compliance Monitoring

### Compliance

Track sensitive resources.

### 3. Compliance Monitoring

Map configurations to standards such as:

* CIS AWS Foundations Benchmark
* NIST Cybersecurity Framework
* ISO 27001
* SOC 2
* PCI DSS
* HIPAA

Example:

- Control:
- S3 buckets must be encrypted
- Status:
- PASS / FAIL

---

---

---

## Slide 88 — Building A Security Findings Baseline

### Finding

`SSH Open to 0.0.0.0/0`

Bad remediation:

 `Remove Port 22 Immediately`

Possible impact:

 `Administrators Locked Out`

Controlled remediation:








### Building a Security Findings Baseline

A security findings baseline is a documented snapshot of the security posture of an environment at a specific point in time. It establishes a measurable starting point that organizations can use to track improvement, demonstrate compliance progress, and identify trends in security risk over time.

Without a baseline, it is difficult to answer critical questions such as:

* Are we becoming more secure?
* Which findings were newly introduced?
* Which risks have been successfully remediated?
* How quickly are issues being resolved?

---

---

## Slide 89 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 90 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 91 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 92 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 93 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 94 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 95 — Lab 1.3

**Speaker notes:** Discuss the question; reveal answer after student responses.
