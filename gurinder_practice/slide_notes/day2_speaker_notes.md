# Day 2 — Speaker Notes

Use with **Cybersecurity-AI-day2.pdf**. One section per slide (from slide 2).

---

## Slide 2 — From Detection To Investigation

### From Detection to Investigation — Day 2 Overview

Day 1 established the security monitoring foundation. Participants deployed cloud resources, collected evidence, configured monitoring controls, and created an initial security posture baseline.

Day 2 shifts from **identifying security findings** to **investigating and responding to security events**. Participants will learn how AWS-native AI and security services work together to detect threats, analyze evidence, identify root causes, and support incident response activities.

---

### Day 1 Foundation

The following components were established on Day 1:








Key outcomes:

* Running EC2 environment
* CloudTrail audit logging
* GuardDuty threat detection
* Security Hub findings aggregation
* IAM and S3 security assessments
* Security findings baseline
* AI-assisted security analysis workflow

---

### Day 2 Focus Areas

Day 2 connects these building blocks into a complete investigation pipeline.








---

---

---

## Slide 3 — From Detection To Investigation

### What You Will Build Today

Day 2 moves beyond finding security issues and focuses on **investigating, analyzing, and responding to security events using AI-assisted cloud security operations**.

Participants will build a complete detection-to-investigation workflow that combines AWS logging, CloudWatch, AI-powered analysis, automated alerting, and incident reporting.

---

### End-of-Day Outcome

By the end of Day 2, participants will be able to:

* Investigate AWS security findings
* Analyze CloudTrail evidence
* Correlate multiple security signals
* Use AI to accelerate investigations
* Identify root causes of security incidents
* Generate investigation reports
* Recommend remediation actions

---

---

---

## Slide 4 — What Is A Security Information And

### What is a Security Information and Event Management (SIEM) System?

A **Security Information and Event Management (SIEM)** system is a centralized platform that collects, stores, normalizes, correlates, analyzes, and alerts on security-related events generated across an organization's infrastructure.

SIEM platforms help security teams answer critical questions:

* What happened?
* When did it happen?
* Who performed the action?
* Which systems were affected?
* Is the activity malicious?
* What should we investigate next?

SIEM solutions form the operational backbone of modern Security Operations Centers (SOCs).

---

### Why SIEM Systems Exist

Modern organizations generate millions of events every day.

- Firewalls
- Endpoints
- Servers
- Applications
- Cloud Services
- Identity Systems
- Network Devices

Without a SIEM:








With a SIEM:








---

### Architecture








---

---

## Slide 5 — Untitled

### Example SIEM Investigation

Suppose an attacker gains access to an AWS account.

### Common SIEM Data Sources

| Source            | Example Events        |
| ----------------- | --------------------- |
| AWS CloudTrail    | API calls             |
| VPC Flow Logs     | Network traffic       |
| Windows Logs      | Authentication events |
| Linux Syslog      | System activity       |
| Firewalls         | Connection attempts   |
| DNS Logs          | Domain lookups        |
| Endpoint Security | Malware detections    |
| Applications      | User actions          |

---

### SIEM in the SOC Workflow








Security analysts spend much of their day working within this workflow.

---

---

---

## Slide 6 — Cloud-Native Monitoring Vs.

### Cloud-Native Monitoring vs. Traditional SIEMs

As organizations move workloads from on-premises data centers to the cloud, security monitoring approaches have evolved significantly. Traditional SIEM platforms were built for physical infrastructure, whereas cloud-native monitoring services are designed specifically for elastic cloud environments.

---

### SIEM Architecture








---

### Cloud-Native Monitoring Architecture

Cloud-native monitoring services are integrated directly into cloud infrastructure.

---

---

## Slide 7 — Architecture Overview

### Amazon CloudWatch — Architecture Overview

Amazon CloudWatch is AWS's native observability platform that provides monitoring, logging, alerting, visualization, and operational intelligence across AWS environments. It acts as the central monitoring layer for cloud-native applications and infrastructure.

---

### CloudWatch Architecture








---

---

---

## Slide 8 — Architecture Overview

### CloudWatch for Security Operations

CloudWatch is frequently used as the monitoring layer in AWS SOC environments.

Security data sources include:

- CloudTrail
- VPC Flow Logs
- Route53 DNS Logs
- Application Logs
- Security Hub Findings
- GuardDuty Findings

Common detection scenarios:

---

---

## Slide 9 — The Cloudwatch Agent And Log

### The CloudWatch Agent and Log Ingestion

CloudWatch can automatically collect metrics from many AWS services, but it cannot see inside an EC2 instance by default. To collect operating system logs, application logs, and custom metrics, AWS uses the **CloudWatch Agent**.

---

### Why the CloudWatch Agent Exists

Without the CloudWatch Agent:








CloudWatch only receives:

* EC2 infrastructure metrics
* AWS service metrics
* Cloud-managed service telemetry

It cannot access:

* Linux log files
* Windows Event Logs
* Application logs
* Security logs
* Custom performance counters

---

### What is the CloudWatch Agent?

The CloudWatch Agent is a lightweight software service installed on:

* Amazon EC2 instances
* On-premises servers
* Virtual machines
* Hybrid infrastructure

Its purpose is to collect:

---

---

## Slide 10 — The Cloudwatch Agent And Log

### Log Group and Log Stream Organization

CloudWatch stores logs using:

---

---

## Slide 11 — Cloudwatch Logs Insights — Query

### Logs

`/var/log/secure`

 `/var/log/messages`

 `/var/log/auth.log`

 `Apache Logs`

 `Nginx Logs`

 `Application Logs`

---

### Why Logs Insights Matters

A modern AWS environment can generate millions of log events per day.

Examples:

- Authentication Events
- Application Logs
- CloudTrail Events
- VPC Flow Logs
- Web Server Logs
- System Logs

Without a query engine, finding suspicious activity becomes extremely difficult.

Logs Insights enables:

* Rapid threat hunting
* Incident investigation
* Security monitoring
* Operational troubleshooting
* Compliance reporting

---

### Query Structure

Most queries follow a simple pattern:

```sql
fields

| filter
| stats
| sort
| limit
```

Example:

```sql
fields @timestamp,@message

| filter @message like /Failed password/
| sort @timestamp desc
| limit 20
```

---

### Security Investigation

Learn how to investigate findings using:

* CloudTrail event history
* User activity analysis
* Resource change tracking
* Timeline reconstruction
* Security evidence collection

---

---

---

## Slide 12 — Ai-Powered Query Generation In

### CloudWatch

`Stores Event`

### AWS

```json
{
  "userIdentity": {
    "userName": "admin"
  }
}
```

SIEM normalizes them into a common schema:

 `Username = admin`

This enables consistent searching and reporting.

---

### Example








Log Events:

 `User login successful`

 `Failed password attempt`

 `sudo command executed`

 `Service restarted`

---

---

## Slide 13 — Ai-Powered Query Generation In

### Human-in-the-Loop Model








The analyst remains responsible for the final investigation.

---

### Step 3

Agent forwards new log entries.








---

---

---

## Slide 14 — Cloudwatch Ai Operations —

### CloudWatch AI Operations

CloudWatch AI Operations introduces generative AI capabilities.

Examples:

### What is CloudWatch?

CloudWatch collects and processes:

---

---

## Slide 15 — Cloudwatch Ai Operations —

### CloudWatch AI Operations — Investigation Hypotheses and Analyst Review

*§11/22 · CloudWatch AI Operations*

### What Is a Hypothesis?

A hypothesis is a possible explanation for observed evidence.

For example, if multiple failed SSH logins are detected:

### AI Investigation Process








Instead of showing only logs, AI provides possible explanations supported by evidence.

---

---

---

## Slide 16 — How Ai Investigations Work

### High-Level Investigation Pipeline








---

### Step 1

Application writes log entries.

Example:

- Failed password for ubuntu
- from 203.0.113.25

---

### Step 2

CloudWatch Agent monitors the log file.

 `/var/log/secure`

---

---

---

## Slide 17 — How Ai Investigations Work

### Human-in-the-Loop Review

The investigation is not automatically accepted.

The analyst reviews:

* Evidence
* Hypotheses
* Findings
* Recommendations

Possible actions:

---

---

## Slide 18 — Signal Vs. Noise In Log Data

### Noise

Noise consists of routine events that provide little investigative value.

Examples:

- Successful user logins
- Normal application requests
- Routine health checks
- Scheduled backup jobs
- Expected system activity

Most log data falls into this category.

---

---

---

## Slide 19 — Signal Vs. Noise In Log Data

### Signal vs. Noise in Log Data — Common Sources of Noise

*§14/22 · CloudWatch AI Operations*

### How AI Helps Reduce Noise

CloudWatch AI Operations can automatically:

### Analyst Best Practice

During investigations:

1. Understand what "normal" looks like.
2. Identify recurring benign events.
3. Build filters to exclude known noise.
4. Focus on anomalies and unusual patterns.
5. Continuously refine dashboards and alarms.

Effective security monitoring is not about collecting more logs—it is about reducing noise and increasing visibility into meaningful signals.

---

---

---

## Slide 20 — Mitre Att&Ck Mapping In

### Why ATT&CK Mapping Helps

ATT&CK provides:

---

---

## Slide 21 — Mitre Att&Ck Mapping In

### Techniques

Specific methods used to achieve those goals.

Examples:

- T1078 – Valid Accounts
- T1059 – Command and Scripting Interpreter
- T1110 – Brute Force
- T1021 – Remote Services
- T1003 – OS Credential Dumping

---

### Example Detection Workflow

Suppose audit logs contain:

- exe="/usr/bin/sudo"
- res=failed
- exe="/usr/bin/sudo"
- res=failed
- exe="/usr/bin/sudo"
- res=failed

Metric filter matches:

 `sudo res=failed`

---

Pipeline:








---

---

---

## Slide 22 — Iam Roles For Cloudwatch Access

### IAM Role

Represents a set of permissions assumed by:

- EC2 Instances
- Lambda Functions
- AWS Services
- Applications

For CloudWatch monitoring, IAM roles are preferred.

---

---

---

## Slide 23 — Iam Roles For Cloudwatch Access

### IAM Roles for CloudWatch Access — Required Roles

*§15/22 · Amazon CloudWatch*

### Principle of Least Privilege

Always grant only the permissions required.

---

---

## Slide 24 — Log Retention And Investigation

### Investigation Retention

Each investigation is stored for future review.

Typical contents include:

- Evidence
- Hypotheses
- Analysis Results
- Analyst Decisions

Organizations can configure retention policies.

Example:

- 30 Days
- 90 Days
- 180 Days
- 1 Year

depending on compliance requirements.

---

### Why Retention Matters

Security logs and AI investigations consume storage and incur ongoing costs. Retaining data indefinitely is rarely necessary and may increase compliance, privacy, and operational risks.

Organizations should define retention policies that balance:

* Security investigation requirements
* Compliance obligations
* Storage costs
* Data privacy considerations
* Incident response needs

---

---

---

## Slide 25 — Log Retention And Investigation

**Speaker notes:** Expand on the on-slide bullets using your own examples.

---

---

## Slide 26 — Evaluating Ai-Generated

### Generated Hypotheses

- Internal Security Scan
- SSH Brute Force Attack
- Automation Failure

### Speaker Notes – Evaluating AI-Generated Hypotheses (Analyst Validation Framework)

**Key message:** A good analyst does not ask "What did the AI say?" They ask "Why did the AI say it, and does the evidence support it?"

---

---

---

## Slide 27 — Evaluating Ai-Generated

### Generate

- Hypotheses
- Evidence References
- Investigation Summaries

The service role grants CloudWatch controlled access to the required resources.

---

### Why Human Review Is Important

AI does not understand the environment perfectly.

Potential issues:

### Limitations of AI Query Generation

AI-generated queries are not always correct.

Analysts must verify:

* Selected fields
* Filters used
* Time ranges
* Regex patterns
* Aggregation logic
* Log source assumptions

Never assume the generated query is accurate without validation.

---

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

## Slide 30 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 31 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 32 — Lab 2.1

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 33 — What Is A Soc Dashboard?

### Speaker Notes – What is a SOC Dashboard?

**Key message:** A SOC dashboard is the analyst's command center. It provides immediate visibility into security posture, active threats, and operational health without requiring analysts to manually search through logs.

---

### Purpose

* Organize logs by application, service, or environment
* Apply retention policies
* Manage permissions
* Simplify searches and investigations

---

---

## Slide 34 — What Is A Soc Dashboard?

### The Three-Panel SOC Dashboard

For today's lab environment, the most useful design includes:

### Dashboard Components

* Security alerts
* Investigation metrics
* Login failures
* Privilege escalation events
* Geographic activity distribution
* Alert severity trends

---

---

## Slide 35 — Metric Filters — Turning Log Events

### Metric Filter

- Pattern:
- "Failed password"

### Metric

`FailedSSHLogins`

### Pattern Type 1: Literal String Matching

Simplest filter type.

Example:

 `exe="/usr/bin/sudo"`

Matches:

- exe="/usr/bin/sudo"
- user=alice

Does NOT match:

 `exe="/usr/bin/passwd"`

Use when:

* Exact values are known
* Specific commands must be tracked
* Security events contain predictable text

---

---

---

## Slide 36 — Metric Filters — Turning Log Events

### Speaker Notes – Metric Filters: Turning Log Events into Numbers

**Key message:** Metric filters are one of the most important CloudWatch concepts. They transform log messages into measurable metrics that can drive alarms, dashboards, and automated responses.

---

### Example: SSH Failure Detection

Log:

 `Failed password for invalid user`

Filter:

 `Failed password`

Metric:

 `SSHFailedLogins`

Result:

 `Every failed login increments the metric`

---

### Privilege Escalation

`IAM policy changes`

---

---

## Slide 37 — Writing Effective Metric Filter

### Speaker Notes – Writing Effective Metric Filter Patterns

**Key message:** The effectiveness of your monitoring depends heavily on the quality of your metric filter patterns. Poor filters create noise and false positives. Good filters create reliable security signals.

---

### Testing Checklist

Before saving a metric filter ask:

✓ Does it match the intended events?

✓ Does it ignore routine events?

✓ Does it produce meaningful metrics?

✓ Would I trust an alarm generated by this filter?

✓ Have I tested against real logs?

---

### SOC Design Recommendation

Create filters for:

---

---

## Slide 38 — Configuration And Thresholds

### Alarm

- FailedSSHLogins > 10
- within 5 minutes

### Alarm States

CloudWatch alarms operate in three states.

### ALARM

`Metric exceeds threshold`

Example:

- ErrorCount = 23
- Threshold = 20

---

---

---

## Slide 39 — Configuration And Thresholds

### Key Configuration Decision #1: Statistic

CloudWatch stores multiple datapoints during an evaluation period.

The statistic determines how those datapoints are interpreted.

---

### Speaker Notes – CloudWatch Alarms: Configuration and Thresholds

**Key message:** CloudWatch Alarms are the decision-making layer of the monitoring pipeline. Metrics provide measurements, but alarms determine when those measurements require attention or action.

---

### Evaluation Period

How long must the condition exist?

Example:

 `5 minutes`

---

### Alarm Tuning Strategy

A good process is:

---

---

## Slide 40 — Alert Runbooks & Documentation

### OK

`Metric below threshold`

Example:

- ErrorCount = 5
- Threshold = 20

---

### Why Runbooks Matter

Imagine a CloudWatch alarm fires at:

 `2:00 AM`

A Tier-1 analyst receives the alert.

Without documentation they must figure out:

* What triggered the alert?
* Is it a real issue?
* Where should they investigate?
* Who owns the system?
* When should they escalate?

This wastes valuable response time.

A runbook provides these answers immediately.

---

### Runbook Section 1: Alert Description

Start by explaining:

---

---

## Slide 41 — Connecting Alarms To Ai

### Speaker Notes – Connecting Alarms to AI Investigations

**Key message:** The real power of CloudWatch AI Operations comes from automation. Instead of waiting for an analyst to manually investigate every alert, CloudWatch alarms can automatically trigger AI investigations and generate initial findings within seconds.

---

### Automated AI Workflow

With AI Operations:








The investigation begins immediately when the alarm triggers.

By the time the analyst opens the alert:

* Relevant logs are already analyzed
* Hypotheses are already generated
* Evidence is already cited

---

### Why Connect Alarms to AI Operations?

Traditional SOC workflow:








The problem:

* Investigation starts only after a human notices the alert
* Valuable response time is lost
* Analysts spend time gathering context before analyzing

---

---

---

## Slide 42 — Privilege Escalation Detection —

### Example: Privilege Escalation Detection

Log:

- exe="/usr/bin/sudo"
- res=failed

Filter:

 `exe="/usr/bin/sudo" res=failed`

Metric:

 `FailedSudoAttempts`

Alarm:

 `FailedSudoAttempts > 10`

---

### Understanding `sudo`

`sudo` stands for:

 `Super User Do`

It allows an authorized user to execute commands with elevated privileges.

Example:

```bash
sudo systemctl restart apache2
```

The command runs with root permissions even though the user is not logged in as root.

---

---

---

## Slide 43 — Privilege Escalation Detection —

### Signal

Signal refers to information that helps identify a meaningful event or security issue.

Examples:

- Repeated failed SSH logins
- Privilege escalation attempt
- Root account usage
- Unauthorized API calls
- Suspicious outbound connections

These events may indicate malicious activity or operational risk.

---

### Speaker Notes – Privilege Escalation Detection: `sudo`, `su`, and SetUID Abuse

**Key message:** Detecting privilege escalation is not limited to monitoring failed `sudo` commands. Security teams should also monitor `su` usage, modifications to privilege-control files, and suspicious SetUID executions. Together, these signals help identify attackers attempting to gain administrative control of Linux systems.

---

### Why Audit Logs Matter

Linux audit logging records:

* Commands executed
* Authentication attempts
* File modifications
* Privilege changes
* Security policy changes

Think of auditd as:

> The system's security flight recorder.
Most privilege escalation attempts leave evidence in audit logs even if they fail.

---

---

---

## Slide 44 — Red And Purple Team

### What is a Red Team?

A Red Team is an offensive security team that acts like a real attacker.

Their goal is not simply to find vulnerabilities.

Their goal is to:

- Compromise systems
- Evade detection
- Achieve objectives

while remaining as realistic as possible.

---

### What is a Purple Team?

Purple Teaming combines:

- Red Team
- +
- Blue Team

working together.

Rather than attacking secretly,

the teams collaborate throughout the exercise.

---

### Purple Team Goal

Purple Teaming focuses on:

- Learning
- Improvement
- Validation

instead of simply measuring success or failure.

---

---

---

## Slide 45 — Creating A Test Attacker Account

### Speaker Notes – Creating a Test Attacker Account

**Key message:** To safely perform attack simulations in a lab environment, we create a dedicated low-privilege user account that represents an attacker. This allows us to generate realistic security events while ensuring the system remains controlled and recoverable.

---

### Why Create a Test Attacker Account?

In real-world security investigations, attacks originate from:

* Compromised user accounts
* Insider threats
* Stolen credentials
* Low-privilege users attempting escalation

To simulate these scenarios safely, we create a dedicated account specifically for testing.

Example:

```bash
attacker
```

or

```bash
redteam
```

---

### Objective

Use CloudWatch AI Operations and natural language queries to analyze cloud security logs without writing complex search syntax.

---

---

## Slide 46 — Dashboard Design For Security

### Security

* Security Hub
* GuardDuty
* AWS Config
* IAM Access Analyzer

---

---

## Slide 47 — Dashboard Design For Security

### Good Dashboard Design Principles

A dashboard should support analyst workflows.

### Security Operations Perspective

Think of metrics as sensors.

Think of alarms as detectors.

Example:

- Metric:
- Temperature = 95°C

The metric only reports information.

The alarm decides:

 `95°C > 80°C`

and triggers action.

Same concept applies to security events.

---

---

---

## Slide 48 — Cloudwatch Dashboard Widgets

### CloudWatch Dashboard

`SOC Dashboard`

---

### Speaker Notes – CloudWatch Dashboard Widgets

**Key message:** Choosing the correct widget type is just as important as choosing the correct data source. Effective dashboards present information in a format that helps analysts quickly identify trends, anomalies, and actionable events rather than overwhelming them with raw data.

---

---

---

## Slide 49 — The Full Detection Pipeline

### Detection Pipeline








---

### Speaker Notes – The Full Detection Pipeline

**Key message:** Security monitoring is not a single tool. It is a chain of connected components that transforms raw operating system activity into actionable intelligence for analysts. Understanding every stage helps identify where detection failures occur and ensures reliable security operations.

---

### Step 1: Logs

Everything starts with raw log events.

Examples:

- ERROR User login failed
- ERROR Access denied
- ERROR Authentication failure

CloudWatch Logs stores these events exactly as they arrive.

At this stage:

* Data is unstructured text
* Cannot trigger alarms directly
* Requires analysis or filtering

The log group is essentially the evidence repository.

---

---

---

## Slide 50 — Att&Ck Techniques In The Lab

### Technique

Attackers attempt multiple passwords against one or more accounts.

### Example Attack Scenarios

Participants may choose:

* Multiple failed login attempts
* Root account activity
* Public S3 bucket exposure
* IAM privilege escalation
* Unauthorized API activity
* Security group modification
* Access key misuse

---

---

---

## Slide 51 — Testing And Validating

### Speaker Notes – Testing and Validating Detection Rules

**Key message:** A detection rule is only valuable if it has been tested. Detection engineering is not complete when a metric filter or alarm is created—it is complete when the entire detection pipeline has been validated end-to-end using known test events.

---

### Runbook Section 3: Validation Steps

Help analysts determine:

> Is this a real incident?
Example workflow:

---

---

## Slide 52 — Testing And Validating

### Speaker Notes – Testing and Validating Detection Rules (Validation Workflow)

**Key message:** Detection validation should follow a repeatable process. A rule is not considered operational until every stage of the detection pipeline has been verified, documented, and cleaned up after testing.

---

### SOC Best Practice

For security detections:

- Statistic = Sum
- Period = 1 Minute
- Threshold = Risk-Based
- Action = SNS + Investigation

Always test alarms using real events before production deployment.

---

---

---

## Slide 53 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 54 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 55 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 56 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 57 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 58 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 59 — Lab 2.2

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 60 — Detection Engineering — What

### Detection

- Event generates
- an alert or investigation

---

Many organizations have visibility but lack detection.

---

### The Detection Engineering Mindset

Detection engineering follows the same principle as software development:








A rule without testing is equivalent to software that was never executed.

---

---

---

## Slide 61 — Detection Engineering — What

### Incident Response

Apply structured response procedures:








---

### Speaker Notes – Detection Engineering: What It Is

**Key message:** Detection engineering is the process of designing, building, testing, tuning, and maintaining security detections that identify adversary behavior. It transforms raw telemetry into actionable alerts that analysts can investigate.

---

---

---

## Slide 62 — Choosing What To Detect

### Speaker Notes – Choosing What to Detect

**Key message:** Detection engineering is about prioritization. Since resources, visibility, and analyst time are limited, organizations should focus on detecting the threats that are most likely, most impactful, and most visible through available telemetry.

---

### Threat Prioritization

Privilege escalation techniques receive higher attention.

---

---

---

## Slide 63 — Choosing What To Detect

### Speaker Notes – Choosing What to Detect (Prioritization Framework)

**Key message:** Detection engineering is a resource allocation problem. The best detections are not necessarily the most advanced—they are the ones that provide the highest security value with the strongest signal and the lowest noise.

---

### Coverage Measurement

Teams can identify:

- Techniques We Detect
- Techniques We Partially Detect
- Techniques We Do Not Detect

---

---

---

## Slide 64 — Linux Endpoint Threat Catalog

### Linux

`user=root`

### Speaker Notes – Linux Endpoint Threat Catalog

**Key message:** Effective detection engineering begins with a threat catalog. Before building alerts, we must understand which attacker behaviors matter most, what evidence they generate, and how they map to MITRE ATT&CK techniques.

---

---

---

## Slide 65 — Auditd — The Linux Audit Daemon

### Step 2 – auditd Captures the Event

Linux auditd records security-relevant activity.

Audit records are written to:

```bash
/var/log/audit/audit.log
```

This becomes the authoritative source of host security events.

---

### Speaker Notes – auditd: The Linux Audit Daemon

**Key message:** auditd is the foundation of Linux detection engineering. It provides highly reliable, kernel-level visibility into system activity and serves as the primary data source for security monitoring, threat detection, and forensic investigations.

---

### Why auditd Matters

Auditd provides:

* Detailed system visibility
* User activity tracking
* Command execution monitoring
* Privilege escalation auditing
* Compliance evidence

Without logging, detection is impossible.

---

---

---

## Slide 66 — Auditd — The Linux Audit Daemon

### Missing Audit Rules

Event never logged.

---

---

---

## Slide 67 — File Permission & Access Monitoring

### Speaker Notes – File Permission & Access Monitoring (ATT&CK Mapping)

**Key message:** File permissions and sensitive file access are some of the most valuable Linux security signals. Attackers frequently modify permissions to gain elevated privileges and access protected files to steal credentials. These actions generate highly reliable audit events that map directly to MITRE ATT&CK techniques.

---

### Sensitive File Access Monitoring

Attackers rarely stop at privilege escalation.

Their next objective is often:

 `Credential theft`

Linux stores valuable credentials in files such as:

- /etc/passwd
- /etc/shadow
- ~/.ssh/id_rsa
- ~/.ssh/authorized_keys

Unauthorized access to these files is a strong indicator of compromise.

---

---

---

## Slide 68 — File Permission & Access Monitoring

### Why Permission Changes Matter

Attackers frequently modify permissions to:

* Gain persistence
* Hide malware
* Enable unauthorized access
* Expose sensitive files
* Create backdoors

Examples:

```bash
chmod 777 sensitive_file
chmod +s binary
chmod 600 evidence.log
```

Monitoring permission changes provides valuable security visibility.

---

### File

`/tmp/audit-chmod.txt`

Permissions changed to:

 `0777`

This helps determine scope.

Analysts need to know exactly what systems and files were involved.

---

---

---

## Slide 69 — Designing A Detection — From

### Speaker Notes – Designing a Detection: From Technique to Rule

**Key message:** Detection engineering starts with attacker behavior, not technology. We begin with an ATT&CK technique, identify observable actions, determine what logs are generated, and then build detection logic around those artifacts.

---

### Detection Rules

Are metric filters matching?

---

---

---

## Slide 70 — Designing A Detection — From

### Speaker Notes – Designing a Detection: From Technique to Rule (Example: Detecting `su` Abuse)

**Key message:** This slide demonstrates the complete thought process a detection engineer follows when transforming an ATT&CK technique into a working detection rule, metric, and alarm.

---

### Threat-to-Detection Workflow

Each catalog entry follows the same process:








This creates consistency across all detections.

---

---

---

## Slide 71 — Simulating Attacks Safely

### Speaker Notes – Simulating Attacks Safely

**Key message:** Effective detection engineering requires generating realistic attack activity, but it must be done in a controlled and safe manner. The objective is to create the same logs a real attacker would generate without causing harm to systems, data, or users.

---

### Speaker Notes – Red Team and Purple Team Operations

**Key message:** Red Teams simulate real-world attackers to identify weaknesses in security controls, while Purple Teams bring attackers and defenders together to improve detection, alerting, and incident response capabilities. Both are critical for measuring and improving SOC effectiveness.

---

---

---

## Slide 72 — Simulating Attacks Safely

### Speaker Notes – Simulating Attacks Safely (Lab Rules & Operational Guidelines)

**Key message:** Detection testing must be realistic, but it must also be disciplined. These rules ensure participants generate useful security telemetry without creating risk to systems, other users, or the environment.

---

---

---

## Slide 73 — Reading Auditd Log Entries

### Read

- CloudWatch Logs
- Metrics
- Alarms
- Investigation Data

### Linux audit logs

`auditd`

---

---

---

## Slide 74 — Reading Auditd Log Entries

### Speaker Notes – Reading auditd Log Entries

**Key message:** Every detection begins with understanding the log data. Detection engineers must be able to read auditd records, identify important fields, and determine which values can be used to build reliable detection logic.

---

---

---

## Slide 75 — Incident Reporting — Structure

### Reporting

Executives and auditors understand attack coverage.

---

### Step 7: Investigation Report Generation

The AI creates a structured investigation summary.

Typical report sections:

### Structured Incident Report

Each participant will produce a professional incident report containing:

---

---

## Slide 76 — Incident Reporting — Structure

### Speaker Notes – Incident Reporting: Structure and Purpose

---

### Executive Summary

- What happened?
- When did it occur?
- Who was involved?
- Impact level?

### Investigation Evidence

- CloudTrail Events
- Affected Resources
- User Activity
- Timeline

---

---

## Slide 77 — Untitled

### Final Message

Cybersecurity is a constantly evolving field.

Attackers continuously develop new techniques.

Defenders continuously improve visibility and detection capabilities.

The most successful security professionals are those who remain curious, continuously test assumptions, validate detections, and learn from every investigation.

---

---

### Course Takeaway

**You now understand the complete lifecycle of modern detection and response: collecting telemetry, engineering detections, validating alerts, investigating incidents, evaluating AI-generated hypotheses, documenting outcomes, and measuring ATT&CK coverage. These skills form the foundation of effective Security Operations and Detection Engineering programs.**

**Congratulations on successfully completing the course.** 🎉

---

*Generated from [`day2_notes.md`](../day2_notes.md). Edit the source and rebuild — do not edit this file by hand.*

### Investigation

Analysts determine:

* What happened
* Who was involved
* Scope of impact
* Severity

---

---

---

## Slide 78 — Ai Hypothesis Triage

### Hypothesis

`Internal Security Scanner`

### Speaker Notes – AI Hypothesis Triage

---

### Speaker Notes – Evaluating AI-Generated Hypotheses

**Key message:** AI-generated hypotheses are suggestions, not conclusions. The analyst remains responsible for validation and decision-making.

---

---

---

## Slide 79 — Detection Coverage And Gaps

### Speaker Notes – Detection Coverage and Gaps

---

### Why Coverage Gaps Matter

Attackers do not care which techniques we monitor.

They look for techniques we do not monitor.

A single uncovered technique may allow:

* Credential theft
* Persistence
* Data exfiltration
* Privilege escalation

without generating any alert.

Detection gaps often become the path attackers choose.

---

---

---

## Slide 80 — Detection Coverage And Gaps

### Better Detection Coverage

Blind spots become visible.

---

### ATT&CK Coverage Example

| Technique | Description                      | Detection Status |
| --------- | -------------------------------- | ---------------- |
| T1110     | Brute Force                      | Covered          |
| T1078     | Valid Accounts                   | Covered          |
| T1021     | Remote Services                  | Covered          |
| T1003     | Credential Dumping               | Partial          |
| T1555     | Credentials from Password Stores | Not Covered      |

This helps guide future detection engineering efforts.

---

---

---

## Slide 81 — Closing An Investigation —

### Speaker Notes – Closing an Investigation: Decision Framework

---

### Closure

Document:

* Root cause
* Lessons learned
* Follow-up actions

---

---

---

## Slide 82 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 83 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 84 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 85 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 86 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 87 — Pop Quiz:

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 88 — Lab 2.3

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

---

## Slide 89 — Congratulations

### Speaker Notes – Course Conclusion / Congratulations

---
