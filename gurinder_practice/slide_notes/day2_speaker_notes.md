# Day 2 — Speaker Notes

Use with **Cybersecurity-AI-day2.pdf**. Each section matches one slide (from slide 2).

---

## Slide 2 — From Detection To Investigation

**On slide:**

- — DAY 2 OVERVIEW
- Day 1 built the foundation: a running EC2
- instance, structured log evidence, AI-assisted
- scripting, and a cloud security posture
- baseline.
- Day 2 connects those pieces into a live
- detection and investigation pipeline using
- AWS-native AI tooling.

**Speaker notes:**

### From Detection to Investigation — Day 2 Overview

Day 1 established the security monitoring foundation. Participants deployed cloud resources, collected evidence, configured monitoring controls, and created an initial security posture baseline.

Day 2 shifts from **identifying security findings** to **investigating and responding to security events**. Participants will learn how AWS-native AI and security services work together to detect threats, analyze evidence, identify root causes, and support incident response activities.

---

### Day 1 Foundation

The following components were established on Day 1:

![Day 1 Foundation](day2_diagrams/from-detection-to-investigation-day-2-overview-001.svg)

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

![Day 2 Focus Areas](day2_diagrams/from-detection-to-investigation-day-2-overview-002.svg)

---

---

## Slide 3 — From Detection To Investigation

**On slide:**

- — DAY 2 OVERVIEW
- What you will build today:
- Lab 2.2 — Query security logs with
- natural language and run AI-assisted
- investigations using CloudWatch AI
- Operations
- Lab 2.3 — Build a real-time SOC
- dashboard with metric filters, alarms,
- and automated investigation triggers
- Lab 2.4 — Choose a real attack
- technique, simulate it, build the full
- detection pipeline independently, and
- write a structured incident report

**Speaker notes:**

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

## Slide 4 — What Is A Security Information And

**On slide:**

- EVENT MANAGEMENT SYSTEM?
- A Security Information and Event Management (SIEM) system collects, normalizes, and correlates log data
- from across an environment to surface security-relevant events in one place.
- SIEMs are the central tool in most SOC workflows. Analysts spend the majority of their time working within
- or alongside one.
- Core SIEM functions:
- Log aggregation — collect events from endpoints, network devices, cloud services, and applications
- Normalization — convert heterogeneous log formats into a consistent schema for querying
- Correlation rules — detect patterns across multiple event sources that no single source would surface
- alone
- Alerting — notify analysts when correlation rules or thresholds trigger
- Search and investigation — allow analysts to query historical data during incident response

**Speaker notes:**

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

![Why SIEM Systems Exist](day2_diagrams/what-is-a-security-information-and-event-management-siem-system-009.svg)

With a SIEM:

![Why SIEM Systems Exist](day2_diagrams/what-is-a-security-information-and-event-management-siem-system-010.svg)

---

### Architecture

![Architecture](day2_diagrams/what-you-will-build-today-006.svg)

---

## Slide 5 — Untitled

**Speaker notes:**

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

![SIEM in the SOC Workflow](day2_diagrams/what-is-a-security-information-and-event-management-siem-system-014.svg)

Security analysts spend much of their day working within this workflow.

---

---

## Slide 6 — Cloud-Native Monitoring Vs.

**On slide:**

- TRADITIONAL SIEMS
- Traditional SIEMs were designed for on-premises
- environments where logs had to be shipped over the
- network from physical devices.
- Cloud-native monitoring takes a different approach,
- logs are generated, stored, and analyzed within the
- same cloud infrastructure.
- Dimension
- Traditional SIEM
- Cloud-Native
- (CloudWatch)
- Log collection
- Agent-based, network
- push
- Native service
- integration
- Scaling
- Manual capacity
- planning
- Automatic
- Query language
- SPL, KQL, vendor-
- specific
- CloudWatch Logs
- Insights
- Cost model
- License +
- infrastructure
- Pay per
- ingestion/query
- AI integration
- Add-on or third-party
- Built into the service

**Speaker notes:**

### Cloud-Native Monitoring vs. Traditional SIEMs

As organizations move workloads from on-premises data centers to the cloud, security monitoring approaches have evolved significantly. Traditional SIEM platforms were built for physical infrastructure, whereas cloud-native monitoring services are designed specifically for elastic cloud environments.

---

### SIEM Architecture

![SIEM Architecture](day2_diagrams/siem-security-information-and-event-management-025.svg)

---

### Cloud-Native Monitoring Architecture

Cloud-native monitoring services are integrated directly into cloud infrastructure.

---

## Slide 7 — Architecture Overview

**On slide:**

- CloudWatch is AWS's native
- observability service.
- It collects metrics (numerical
- time-series data) and logs
- (text events) from AWS
- services and custom sources,
- then provides query,
- alerting, and visualization
- tools on top of them.

**Speaker notes:**

### Amazon CloudWatch — Architecture Overview

Amazon CloudWatch is AWS's native observability platform that provides monitoring, logging, alerting, visualization, and operational intelligence across AWS environments. It acts as the central monitoring layer for cloud-native applications and infrastructure.

---

### CloudWatch Architecture

![CloudWatch Architecture](day2_diagrams/amazon-cloudwatch-architecture-overview-041.svg)

---

---

## Slide 8 — Architecture Overview

**On slide:**

- Key components:
- Log groups — containers for related log streams (e.g., /soc-
- lab/secure for endpoint auth events)
- Log streams — individual sequences of log events from a
- single source (e.g., one EC2 instance)
- Metrics — numerical measurements over time (e.g.,
- CPUUtilization, or custom SudoFailedAttempts)
- Alarms — monitors a metric against a threshold; triggers
- actions when breached
- Dashboards — configurable visualization panels combining
- metrics and log queries

**Speaker notes:**

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

## Slide 9 — The Cloudwatch Agent And Log

**On slide:**

- INGESTION
- The CloudWatch agent is a software process that runs
- on an EC2 instance and continuously ships log data to
- CloudWatch.
- Without it, CloudWatch has no visibility into the host,
- only into AWS-managed services.

**Speaker notes:**

### The CloudWatch Agent and Log Ingestion

CloudWatch can automatically collect metrics from many AWS services, but it cannot see inside an EC2 instance by default. To collect operating system logs, application logs, and custom metrics, AWS uses the **CloudWatch Agent**.

---

### Why the CloudWatch Agent Exists

Without the CloudWatch Agent:

![Why the CloudWatch Agent Exists](day2_diagrams/amazon-cloudwatch-key-components-050.svg)

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

## Slide 10 — The Cloudwatch Agent And Log

**On slide:**

- INGESTION
- How log ingestion works:
- The agent runs on the EC2 instance as a system service
- A configuration file tells it which log files to watch and
- which log group to send them to
- The agent tails configured files and forwards new entries to
- CloudWatch in near real time
- Entries land in a log stream named after the instance ID
- All streams within one log group can be searched together
- via Logs Insights

**Speaker notes:**

### Log Group and Log Stream Organization

CloudWatch stores logs using:

---

## Slide 11 — Cloudwatch Logs Insights — Query

**On slide:**

- LANGUAGE
- Logs Insights is the query engine for CloudWatch log
- data. It uses a structured query language purpose-built
- for log analysis. It is simpler than SQL, but powerful
- enough for most SOC investigation tasks.
- Common query patterns:
- fields — select which columns to display
- filter — apply conditions (supports regex with like /pattern/)
- stats — aggregate; count(), sum(), avg()
- sort and limit — control output order and volume

**Speaker notes:**

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

## Slide 12 — Ai-Powered Query Generation In

**On slide:**

- CLOUDWATCH
- CloudWatch Log Analytics includes
- an AI interface that converts plain
- English questions into Logs Insights
- query syntax. This lowers the barrier
- to log analysis for analysts who
- don't know the query language.
- This does not replace query
- knowledge, it accelerates writing the
- first draft. Analysts still need to
- validate that the generated query
- matches the actual log structure in
- their environment.

**Speaker notes:**

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

![Example](day2_diagrams/amazon-cloudwatch-key-components-045.svg)

Log Events:

 `User login successful`

 `Failed password attempt`

 `sudo command executed`

 `Service restarted`

---

## Slide 13 — Ai-Powered Query Generation In

**On slide:**

- CLOUDWATCH
- 1.
- You type a natural language
- prompt: *"Find failed SSH attempts
- in the last hour"*
- 2.
- The AI generates a complete Logs
- Insights query targeting the fields it
- infers are relevant
- 3.
- You review the generated query
- before running it — the AI output is
- editable
- 4.
- Results appear in the same interface
- as a manually written query

**Speaker notes:**

### Human-in-the-Loop Model

![Human-in-the-Loop Model](day2_diagrams/cloudwatch-logs-insights-query-language-070.svg)

The analyst remains responsible for the final investigation.

---

### Step 3

Agent forwards new log entries.

![Step 3](day2_diagrams/amazon-cloudwatch-key-components-052.svg)

---

---

## Slide 14 — Cloudwatch Ai Operations —

**On slide:**

- WHAT IT IS
- AI Operations is a new CloudWatch feature that
- runs structured investigations over your log and
- metric data using AI.
- Unlike a simple query, an investigation forms
- multiple hypotheses, evaluates evidence across
- data sources, and presents conclusions for analyst
- review.

**Speaker notes:**

### CloudWatch AI Operations

CloudWatch AI Operations introduces generative AI capabilities.

Examples:

### What is CloudWatch?

CloudWatch collects and processes:

---

## Slide 15 — Cloudwatch Ai Operations —

**On slide:**

- WHAT IT IS
- AI Operations is not a black box:
- Every hypothesis includes the
- evidence the AI cited
- The analyst reviews and accepts,
- rejects, or escalates each finding
- Investigations can be triggered
- manually or automatically by a
- CloudWatch alarm
- Each investigation has a
- configurable retention period
- (deleted after expiry)
- The AI may conclude that an event
- is *not* a threat — ruling
- something out is a legitimate
- analytical outcome

**Speaker notes:**

### CloudWatch AI Operations — Investigation Hypotheses and Analyst Review

*§11/22 · CloudWatch AI Operations*

### What Is a Hypothesis?

A hypothesis is a possible explanation for observed evidence.

For example, if multiple failed SSH logins are detected:

### AI Investigation Process

![AI Investigation Process](day2_diagrams/cloudwatch-ai-operations-investigation-hypotheses-and-analyst-review-077.svg)

Instead of showing only logs, AI provides possible explanations supported by evidence.

---

---

## Slide 16 — How Ai Investigations Work

**On slide:**

- An AI Operations investigation follows a
- structured pipeline. The analyst sets the
- scope, the AI runs the analysis, and the
- analyst reviews the output to make a
- final call.
- The analyst is always the decision-maker.
- AI provides a starting hypothesis, not a
- verdict.

**Speaker notes:**

### High-Level Investigation Pipeline

![High-Level Investigation Pipeline](day2_diagrams/cloudwatch-ai-operations-investigation-hypotheses-and-analyst-review-080.svg)

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

## Slide 17 — How Ai Investigations Work

**On slide:**

- 1.
- Scope — define the log group, time range, and
- starting query
- 2.
- Analysis — AI runs the query, examines the
- matching events, and evaluates patterns
- 3.
- Hypothesis generation — AI produces one or
- more theories about what the activity
- represents
- 4.
- Evidence citation — each hypothesis cites
- specific log events supporting the conclusion
- 5.
- Analyst review — confirm, challenge, or
- escalate based on what you know about the
- environment

**Speaker notes:**

### Human-in-the-Loop Review

The investigation is not automatically accepted.

The analyst reviews:

* Evidence
* Hypotheses
* Findings
* Recommendations

Possible actions:

---

## Slide 18 — Signal Vs. Noise In Log Data

**On slide:**

- A high-volume production environment can
- generate tens of millions of log events per day.
- The challenge for a SOC analyst is not finding
- logs. It is finding the events that matter within an
- ocean of routine activity.
- AI-assisted investigation helps by grouping similar
- events, identifying patterns, and surfacing the
- highest-anomaly items first, reducing the manual
- filtering burden significantly.

**Speaker notes:**

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

## Slide 19 — Signal Vs. Noise In Log Data

**On slide:**

- Noise sources that overwhelm raw log analysis:
- Scheduled jobs and automated health checks
- generating repeated identical entries
- Infrastructure-level retries and timeouts that are
- expected and benign
- Background internet scanner activity probing open
- ports continuously
- Verbose application debug logging enabled
- unintentionally in production

**Speaker notes:**

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

## Slide 20 — Mitre Att&Ck Mapping In

**On slide:**

- INVESTIGATIONS
- Mapping detected events to ATT&CK
- techniques gives investigations a
- structured language and connects
- findings to known adversary behaviors.
- It also helps analysts prioritize. A
- confirmed T1078 (Valid Accounts abuse)
- demands different urgency than a
- routine T1059 (script execution).

**Speaker notes:**

### Why ATT&CK Mapping Helps

ATT&CK provides:

---

## Slide 21 — Mitre Att&Ck Mapping In

**On slide:**

- INVESTIGATIONS
- T1110 — Brute Force: repeated failed SSH
- login events from a single source
- T1087 — Account Discovery: enumeration
- commands that appear in audit logs
- T1059 — Command and Scripting Interpreter:
- shell commands executed on the host
- T1078 — Valid Accounts: authentication with
- legitimate credentials at unexpected times or
- locations
- T1526 — Cloud Service Discovery:
- enumeration of IAM, S3, and EC2 resources
- via API

**Speaker notes:**

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

![Example Detection Workflow](day2_diagrams/detection-strategy-148.svg)

---

---

## Slide 22 — Iam Roles For Cloudwatch Access

**On slide:**

- CloudWatch AI Operations and the CloudWatch
- agent both require IAM permissions to function.
- Configuring these permissions correctly is a
- prerequisite. Without them, the agent cannot ship
- logs and AI Operations cannot read them.

**Speaker notes:**

### IAM Role

Represents a set of permissions assumed by:

- EC2 Instances
- Lambda Functions
- AWS Services
- Applications

For CloudWatch monitoring, IAM roles are preferred.

---

---

## Slide 23 — Iam Roles For Cloudwatch Access

**On slide:**

- EC2 instance profile — attached to the instance;
- grants the CloudWatch agent permission to write
- logs (CloudWatchAgentServerPolicy)
- AI Operations role — an account-level role that
- CloudWatch assumes to read logs, metrics, and
- alarms when running an investigation
- Both roles should follow least privilege — the AI
- Operations role needs read access, not write access,
- to your resources
- Auto-creating the AI Operations role is the safe
- default in a lab environment

**Speaker notes:**

### IAM Roles for CloudWatch Access — Required Roles

*§15/22 · Amazon CloudWatch*

### Principle of Least Privilege

Always grant only the permissions required.

---

## Slide 24 — Log Retention And Investigation

**On slide:**

- RETENTION
- Logs and investigations stored indefinitely cost
- money and create data management risk.
- Setting appropriate retention periods for both is a
- standard part of configuring any monitoring
- environment.

**Speaker notes:**

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

## Slide 25 — Log Retention And Investigation

**On slide:**

- RETENTION
- Default: indefinite (logs are never deleted automatically —
- you pay for all stored data)
- Configurable per log group: 1 day to 10 years
- Typical SOC practice: 90 days hot (immediately queryable),
- archive to S3 for long-term compliance retention
- AI Operations investigation retention:
- Configurable at the account level: default 7 days in a lab
- environment is appropriate
- Expired investigations are deleted automatically — no
- manual cleanup needed

**Speaker notes:** Expand on the on-slide bullets using your own examples.

---

## Slide 26 — Evaluating Ai-Generated

**On slide:**

- HYPOTHESES
- An AI hypothesis is a starting point, not a
- conclusion. Evaluating it correctly requires the
- analyst to apply domain knowledge about the
- environment, the activity that generated the logs,
- and the plausibility of the AI's interpretation.
- A hypothesis you cannot verify with evidence
- should not be escalated

**Speaker notes:**

### Generated Hypotheses

- Internal Security Scan
- SSH Brute Force Attack
- Automation Failure

### Speaker Notes – Evaluating AI-Generated Hypotheses (Analyst Validation Framework)

**Key message:** A good analyst does not ask "What did the AI say?" They ask "Why did the AI say it, and does the evidence support it?"

---

---

## Slide 27 — Evaluating Ai-Generated

**On slide:**

- HYPOTHESES
- Questions to ask when reviewing a hypothesis:
- What evidence did the AI cite? Can you locate those
- specific log events yourself?
- Is the conclusion consistent with the data? Or is the
- AI pattern-matching on surface features?
- Is the activity expected? A "suspicious" event may be
- routine if you know what generated it
- What did the AI not consider? Investigations are
- bounded by the query scope — related signals
- outside that scope are invisible to the AI

**Speaker notes:**

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

## Slide 28 — Pop Quiz:

**On slide:**

- An AI Operations investigation concludes: *"This activity is consistent with
- a routine automated health check, not an active threat."* How should an
- analyst respond?
- A. Discard the finding immediately — if the AI says it is safe, no further action is needed
- B. Escalate the finding regardless of the AI's conclusion, because AI tools cannot be trusted to rule out threats
- C. Review the evidence the AI cited, confirm it aligns with your knowledge of expected environment behavior, then
- close the investigation with a documented rationale
- D. Re-run the investigation with a broader query scope to force a different result

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 29 — Pop Quiz:

**On slide:**

- An AI Operations investigation concludes: *"This activity is consistent with
- a routine automated health check, not an active threat."* How should an
- analyst respond?
- A. Discard the finding immediately — if the AI says it is safe, no further action is needed
- B. Escalate the finding regardless of the AI's conclusion, because AI tools cannot be trusted to rule out threats
- C. Review the evidence the AI cited, confirm it aligns with your knowledge of expected environment
- behavior, then close the investigation with a documented rationale
- D. Re-run the investigation with a broader query scope to force a different result

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 30 — Pop Quiz:

**On slide:**

- A student opens CloudWatch and finds the /soc-lab/secure log group is
- empty. Which of the following is the most likely cause and correct first
- remediation step?
- A. The log group does not exist yet — create it manually in the CloudWatch console
- B. The CloudWatch agent on the EC2 instance is not running or has lost its configuration — restart it with `sudo
- systemctl restart amazon-cloudwatch-agent`
- C. The IAM policy attached to the analyst's user does not include `logs:GetLogEvents` — update the policy
- D. CloudWatch Logs Insights requires a 30-minute warm-up period before new log groups become queryable

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 31 — Pop Quiz:

**On slide:**

- A student opens CloudWatch and finds the /soc-lab/secure log group is
- empty. Which of the following is the most likely cause and correct first
- remediation step?
- A. The log group does not exist yet — create it manually in the CloudWatch console
- B. The CloudWatch agent on the EC2 instance is not running or has lost its configuration — restart it with
- `sudo systemctl restart amazon-cloudwatch-agent`
- C. The IAM policy attached to the analyst's user does not include `logs:GetLogEvents` — update the policy
- D. CloudWatch Logs Insights requires a 30-minute warm-up period before new log groups become queryable

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 32 — Lab 2.1

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 33 — What Is A Soc Dashboard?

**On slide:**

- A SOC dashboard is a visual workspace
- that displays the most important security
- signals in one place, allowing an analyst
- to assess the current threat picture at a
- glance without running queries from
- scratch.
- Good dashboards are designed around
- analyst workflows, not technical
- capabilities.

**Speaker notes:**

### Speaker Notes – What is a SOC Dashboard?

**Key message:** A SOC dashboard is the analyst's command center. It provides immediate visibility into security posture, active threats, and operational health without requiring analysts to manually search through logs.

---

### Purpose

* Organize logs by application, service, or environment
* Apply retention policies
* Manage permissions
* Simplify searches and investigations

---

## Slide 34 — What Is A Soc Dashboard?

**On slide:**

- Actionable signals — every widget should
- lead to a decision or investigation
- Time-range consistency — all widgets
- should show the same window for
- meaningful comparison
- Layered views — high-level counts on top;
- event detail available on drill-down
- Alert integration — surface active alarms
- directly on the dashboard, not in a
- separate tab
- Dashboards that display everything
- simultaneously are as useless as
- dashboards that display nothing

**Speaker notes:**

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

## Slide 35 — Metric Filters — Turning Log Events

**On slide:**

- INTO NUMBERS
- A CloudWatch metric filter reads a log group and increments a custom metric counter each
- time a log entry matches a specified pattern. This converts unstructured log text into a
- time-series number that can be graphed, alarmed on, and analyzed over time.
- Why this matters for detection:
- Raw log events cannot be alarmed on directly, they must first become a metric
- A metric filter creates a countable signal: "how many sudo failures occurred in the last minute?"
- Custom metrics live in a namespace you define (e.g., SOCLab)
- Metric filters are the bridge between log data and the rest of the CloudWatch alerting ecosystem
- One metric filter can feed multiple alarms and dashboard widgets simultaneously

**Speaker notes:**

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

## Slide 36 — Metric Filters — Turning Log Events

**On slide:**

- INTO NUMBERS

**Speaker notes:**

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

## Slide 37 — Writing Effective Metric Filter

**On slide:**

- PATTERNS
- Test your pattern against real log data in the Test
- pattern step of the metric filter wizard before
- saving.
- Pattern syntax:
- Literal string — exe="/usr/bin/sudo" matches
- any log entry containing that exact string
- AND logic — [a, b] or space-separated terms:
- exe="/usr/bin/sudo" res=failed
- Wildcard — % matches zero or more characters
- within a term
- Field-based — for JSON logs: { $.eventType =
- "AuthenticationFailure" }

**Speaker notes:**

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

## Slide 38 — Configuration And Thresholds

**On slide:**

- A CloudWatch alarm monitors a single metric and
- transitions between states based on whether the
- metric value crosses a defined threshold.
- State transitions can trigger actions notifications,
- Lambda invocations, or AI Operations
- investigations.

**Speaker notes:**

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

## Slide 39 — Configuration And Thresholds

**On slide:**

- Alarm states:
- OK — metric is within the acceptable range
- In alarm — metric has crossed the threshold
- Insufficient data — not enough data points yet to evaluate
- Key configuration decisions:
- Statistic — Sum for counting security events; Average for
- rate or latency metrics
- Period — the evaluation window; 1 minute is appropriate
- for near-real-time security alerting
- Threshold — >= 1 for security events: any single match
- should trigger the alarm
- Alarm actions — what happens when the alarm fires (the
- most important field for a SOC pipeline)

**Speaker notes:**

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

## Slide 40 — Alert Runbooks & Documentation

**On slide:**

- All alerts should be documented in a centralized wiki
- with an associated runbook. This ensures consistent
- response and reduces time to investigate incidents.
- Each alert links to a runbook
- Where to look: dashboards, logs, metrics
- Suggested remediation steps
- Clear escalation path
- Notes on common causes / patterns

**Speaker notes:**

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

## Slide 41 — Connecting Alarms To Ai

**On slide:**

- INVESTIGATIONS
- Wiring a CloudWatch alarm to an AI
- Operations investigation creates an
- automatic triage pipeline:
- A suspicious event occurs, the metric
- increments, the alarm fires, and an
- investigation starts without analyst
- intervention. An analyst will review,
- investigate and act on the results.

**Speaker notes:**

### Speaker Notes – Connecting Alarms to AI Investigations

**Key message:** The real power of CloudWatch AI Operations comes from automation. Instead of waiting for an analyst to manually investigate every alert, CloudWatch alarms can automatically trigger AI investigations and generate initial findings within seconds.

---

### Automated AI Workflow

With AI Operations:

![Automated AI Workflow](day2_diagrams/iam-roles-for-cloudwatch-access-required-roles-140.svg)

The investigation begins immediately when the alarm triggers.

By the time the analyst opens the alert:

* Relevant logs are already analyzed
* Hypotheses are already generated
* Evidence is already cited

---

### Why Connect Alarms to AI Operations?

Traditional SOC workflow:

![Why Connect Alarms to AI Operations?](day2_diagrams/iam-roles-for-cloudwatch-access-required-roles-139.svg)

The problem:

* Investigation starts only after a human notices the alert
* Valuable response time is lost
* Analysts spend time gathering context before analyzing

---

---

## Slide 42 — Privilege Escalation Detection —

**On slide:**

- `SUDO` AND `SU`
- Privilege escalation is one of the highest-priority
- attack categories because success may gives an
- attacker the same power as a system
- administrator.
- Detecting failed attempts is critical. It reveals that
- escalation is being actively attempted even before
- it succeeds.

**Speaker notes:**

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

## Slide 43 — Privilege Escalation Detection —

**On slide:**

- `SUDO` AND `SU`
- Detection signals in auditd:
- Failed sudo — exe="/usr/bin/sudo" res=failed in
- /var/log/audit/audit.log
- Failed su — exe="/usr/bin/su" res=failed
- Sudoers modification — write access to /etc/sudoers
- or /etc/sudoers.d/
- Unexpected SUID execution — a binary with SetUID
- bit run by a low-privilege user
- MITRE ATT&CK mapping:
- T1548.003 — Abuse Elevation Control Mechanism:
- sudo
- T1548.001 — Abuse Elevation Control Mechanism:
- SetUID

**Speaker notes:**

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

## Slide 44 — Red And Purple Team

**On slide:**

- Red and Purple Teams are used to test and improve an
- organization’s security posture through simulated
- attacks and collaboration.
- Red Team: Simulates real attackers (offensive
- security)
- Focuses on exploitation, evasion, and bypassing
- controls
- Tests people, processes, and technology
- Purple Team: Collaboration between Red & Blue
- teams
- Improves detection, alerting, and response
- Focuses on learning and continuous improvement

**Speaker notes:**

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

## Slide 45 — Creating A Test Attacker Account

**On slide:**

- To safely simulate attacks without risking the
- integrity of your lab environment, a dedicated
- low-privilege test account is used for attack
- simulation steps.
- This mirrors real red team / purple team exercise
- practices.

**Speaker notes:**

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

## Slide 46 — Dashboard Design For Security

**On slide:**

- OPERATIONS
- A well-designed SOC dashboard is an
- analyst's first stop, not their last. It
- should answer the most common
- questions immediately without requiring
- the analyst to build queries from scratch
- each time they sit down.
- Each widget should have a clear, specific
- Logs Insights query behind it. Not a
- broad "show me everything" query.

**Speaker notes:**

### Security

* Security Hub
* GuardDuty
* AWS Config
* IAM Access Analyzer

---

## Slide 47 — Dashboard Design For Security

**On slide:**

- OPERATIONS
- What to include in a SOC dashboard:
- Event volume over time — a line chart showing total
- auth events per 5-minute window
- Failed auth by source — a ranked table of IPs with
- the most failures
- Privilege escalation attempts — a counter or time-
- series for sudo/su failures
- Active alarms — current alarm state for all security
- metrics
- Recent raw events — a log table showing the last 20
- matching events for quick context

**Speaker notes:**

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

## Slide 48 — Cloudwatch Dashboard Widgets

**On slide:**

- CloudWatch dashboards support multiple
- widget types. Choosing the right type for each
- signal makes the difference between a
- dashboard that accelerates decision-making
- and one that just looks busy.
- For a SOC lab dashboard, a combination of a line
- chart (trend), a logs table (event detail), and an
- alarm status widget (current alert state) gives an
- analyst the most useful three-panel view.
- Widget Type
- Best For
- Line chart
- Event counts over time; trend
- detection
- Number widget
- Current alarm count; total findings
- today
- Logs table
- Showing raw recent events with
- @timestamp and @message
- Alarm status
- At-a-glance current state of all
- configured alarms
- Bar chart
- Comparing counts across discrete
- categories (e.g., by source IP)

**Speaker notes:**

### CloudWatch Dashboard

`SOC Dashboard`

---

### Speaker Notes – CloudWatch Dashboard Widgets

**Key message:** Choosing the correct widget type is just as important as choosing the correct data source. Effective dashboards present information in a format that helps analysts quickly identify trends, anomalies, and actionable events rather than overwhelming them with raw data.

---

---

## Slide 49 — The Full Detection Pipeline

**On slide:**

- Building a detection pipeline means
- connecting every component from raw
- host activity through to analyst action.
- Understanding the full chain helps you
- diagnose failures. If an alarm never
- fires, you need to know which link
- broke.

**Speaker notes:**

### Detection Pipeline

![Detection Pipeline](day2_diagrams/amazon-cloudwatch-key-components-054.svg)

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

## Slide 50 — Att&Ck Techniques In The Lab

**On slide:**

- ENVIRONMENT
- Mapping your detection to ATT&CK validates coverage
- and identifies gaps.
- A few techniques not yet covered (gap):
- T1053 — Scheduled Task/Job (cron) →no metric filter
- exists yet
- T1136 — Create Account →ADD_USER event not yet
- alerted
- Technique
- ID
- Detection Signal
- Brute Force
- T1110
- Failed SSH auth
- events
- Valid Accounts —
- abuse
- T1078
- Auth from
- unexpected
- accounts
- Abuse Elevation:
- sudo
- T1548.003
- exe="/usr/bin/sud
- o" res=failed
- Command and
- Scripting
- T1059
- Shell command
- execution in audit
- log

**Speaker notes:**

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

## Slide 51 — Testing And Validating

**On slide:**

- DETECTION RULES
- A detection rule that has never fired is not a
- tested rule, it is a hypothesis.
- Every metric filter and alarm must be validated by
- generating known test events and confirming the
- pipeline responds as expected.

**Speaker notes:**

### Speaker Notes – Testing and Validating Detection Rules

**Key message:** A detection rule is only valuable if it has been tested. Detection engineering is not complete when a metric filter or alarm is created—it is complete when the entire detection pipeline has been validated end-to-end using known test events.

---

### Runbook Section 3: Validation Steps

Help analysts determine:

> Is this a real incident?
Example workflow:

---

## Slide 52 — Testing And Validating

**On slide:**

- DETECTION RULES
- Generate test events — run the action the rule
- should detect (controlled and documented)
- Verify log entry — confirm the expected log line
- appears in CloudWatch within 60 seconds
- Verify metric increment — confirm the custom metric
- value increased in the CloudWatch console
- Verify alarm state — confirm the alarm transitions to
- "In alarm"
- Verify investigation — confirm an AI Operations
- investigation was automatically created
- Clean up — remove test artifacts (e.g., sudo userdel -
- r testattacker) after validation

**Speaker notes:**

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

## Slide 53 — Pop Quiz:

**On slide:**

- You want to create a metric filter that counts failed sudo attempts from the
- auditd log. Which filter pattern is correct for auditd log entries?
- A. `Failed sudo attempt`
- B. `{ $.result = "FAILED" && $.command = "sudo" }`
- C. `exe="/usr/bin/sudo" res=failed`
- D. `sudo: authentication failure`

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 54 — Pop Quiz:

**On slide:**

- You want to create a metric filter that counts failed sudo attempts from the
- auditd log. Which filter pattern is correct for auditd log entries?
- A. `Failed sudo attempt`
- B. `{ $.result = "FAILED" && $.command = "sudo" }`
- C. `exe="/usr/bin/sudo" res=failed`
- D. `sudo: authentication failure`

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 55 — Pop Quiz:

**On slide:**

- You are configuring a CloudWatch alarm to detect sudo privilege
- escalation attempts. Which configuration is most appropriate?
- A. Statistic: Average, Period: 1 hour, Threshold: greater than 100
- B. Statistic: Sum, Period: 1 minute, Threshold: greater than or equal to 1
- C. Statistic: Minimum, Period: 5 minutes, Threshold: less than 1
- D. Statistic: Sum, Period: 24 hours, Threshold: greater than 1000

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 56 — Pop Quiz:

**On slide:**

- You are configuring a CloudWatch alarm to detect sudo privilege
- escalation attempts. Which configuration is most appropriate?
- A. Statistic: Average, Period: 1 hour, Threshold: greater than 100
- B. Statistic: Sum, Period: 1 minute, Threshold: greater than or equal to 1
- C. Statistic: Minimum, Period: 5 minutes, Threshold: less than 1
- D. Statistic: Sum, Period: 24 hours, Threshold: greater than 1000

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 57 — Pop Quiz:

**On slide:**

- A student generates failed sudo attempts on their EC2 instance but the
- CloudWatch alarm never fires. Assuming the alarm and metric filter are
- configured correctly, which component is the most likely point of failure?
- A. The CloudWatch alarm has not been given enough time — alarms take up to 24 hours to activate after creation
- B. The CloudWatch agent on the EC2 instance is not running or is not configured to ship `/var/log/audit/audit.log`
- C. The metric filter pattern is too specific — it should use a wildcard to match more events
- D. The IAM role attached to the alarm does not have permission to read the audit log file

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 58 — Pop Quiz:

**On slide:**

- A student generates failed sudo attempts on their EC2 instance but the
- CloudWatch alarm never fires. Assuming the alarm and metric filter are
- configured correctly, which component is the most likely point of failure?
- A. The CloudWatch alarm has not been given enough time — alarms take up to 24 hours to activate after creation
- B. The CloudWatch agent on the EC2 instance is not running or is not configured to ship
- `/var/log/audit/audit.log`
- C. The metric filter pattern is too specific — it should use a wildcard to match more events
- D. The IAM role attached to the alarm does not have permission to read the audit log file

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 59 — Lab 2.2

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 60 — Detection Engineering — What

**On slide:**

- IT IS
- Detection engineering is the discipline of building,
- testing, and maintaining the rules and pipelines
- that alert analysts to adversary behavior. It sits at
- the intersection of threat intelligence, log analysis,
- and software development.
- Detection engineering is not a one-time task. It is
- an ongoing operational discipline.

**Speaker notes:**

### Detection

- Event generates
- an alert or investigation

---

Many organizations have visibility but lack detection.

---

### The Detection Engineering Mindset

Detection engineering follows the same principle as software development:

![The Detection Engineering Mindset](day2_diagrams/the-three-panel-soc-dashboard-166.svg)

A rule without testing is equivalent to software that was never executed.

---

---

## Slide 61 — Detection Engineering — What

**On slide:**

- IT IS
- A detection engineer:
- Translates threat intelligence and ATT&CK
- techniques into actionable detection logic
- Tests rules against both real attack data and benign
- activity to calibrate false positive rates
- Maintains and tunes detections as the environment
- and attacker techniques evolve
- Documents every rule: what it detects, what evidence
- it needs, and what the analyst should do when it fires

**Speaker notes:**

### Incident Response

Apply structured response procedures:

![Incident Response](day2_diagrams/from-detection-to-investigation-day-2-overview-003.svg)

---

### Speaker Notes – Detection Engineering: What It Is

**Key message:** Detection engineering is the process of designing, building, testing, tuning, and maintaining security detections that identify adversary behavior. It transforms raw telemetry into actionable alerts that analysts can investigate.

---

---

## Slide 62 — Choosing What To Detect

**On slide:**

- Not every possible attacker technique can be
- detected with the same signal quality. A practical
- detection strategy starts with the techniques most
- likely to target your environment and the
- techniques where you have reliable, high-fidelity
- log data.
- For a Linux EC2 environment with auditd and
- CloudWatch: SSH brute force, privilege escalation,
- new account creation, and sensitive file access all
- score high on all four dimensions.

**Speaker notes:**

### Speaker Notes – Choosing What to Detect

**Key message:** Detection engineering is about prioritization. Since resources, visibility, and analyst time are limited, organizations should focus on detecting the threats that are most likely, most impactful, and most visible through available telemetry.

---

### Threat Prioritization

Privilege escalation techniques receive higher attention.

---

---

## Slide 63 — Choosing What To Detect

**On slide:**

- Prioritization framework:
- Signal fidelity — does the technique produce a
- distinctive, low-noise log event?
- ATT&CK prevalence — how commonly is this
- technique used in real-world attacks against your
- type of environment?
- Detection gap — is this technique currently
- unmonitored?
- Blast radius — if this technique succeeds undetected,
- how severe is the impact?

**Speaker notes:**

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

## Slide 64 — Linux Endpoint Threat Catalog

**On slide:**

- Five specific threat techniques are relevant to the
- lab environment.
- Each produces a distinctive auditd log signature
- and maps to a documented ATT&CK technique.
- Threat
- What Happens
- auditd Signal
- ATT&CK
- SSH brute
- force
- Repeated failed
- SSH logins
- from one
- source
- exe="/usr/sbin/
- sshd"
- res=failed
- T1110
- New account
- backdoor
- useradd
- creates a
- persistence
- account
- type=ADD_US
- ER
- T1136
- Sensitive file
- access
- Read attempt
- on /etc/shadow
- name="/etc/sha
- dow"
- T1003
- su abuse
- Repeated failed
- su - root
- attempts
- exe="/usr/bin/s
- u" res=failed
- T1548
- Cron
- persistence
- Cron job
- installed by
- non-root user
- crontab
- keyword in
- audit log
- T1053

**Speaker notes:**

### Linux

`user=root`

### Speaker Notes – Linux Endpoint Threat Catalog

**Key message:** Effective detection engineering begins with a threat catalog. Before building alerts, we must understand which attacker behaviors matter most, what evidence they generate, and how they map to MITRE ATT&CK techniques.

---

---

## Slide 65 — Auditd — The Linux Audit Daemon

**On slide:**

- auditd is the kernel-level auditing
- system for Linux. It records system
- calls, file accesses, and process
- execution events at a level of detail
- no userspace logging tool can
- match.
- Since it runs in the kernel, it is
- extremely difficult for a user-level
- attacker to suppress without root
- access.
- ^^  Audit reads to a file

**Speaker notes:**

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

## Slide 66 — Auditd — The Linux Audit Daemon

**On slide:**

- Audit rules — configured with auditctl;
- define what events to record
- Keys — labels attached to rules (e.g., -
- k shadow-access) for filtering with
- ausearch
- /var/log/audit/audit.log — the primary
- output file; plain-text key-value format
- auditd must be installed and running:
- sudo systemctl enable --now auditd
- The CloudWatch agent ships this file
- to the /soc-lab/secure log group
- ^^  Audit “chmod” and related commands

**Speaker notes:**

### Missing Audit Rules

Event never logged.

---

---

## Slide 67 — File Permission & Access Monitoring

**On slide:**

- (ATT&CK MAPPING)
- Monitoring file permission changes and access events helps
- detect privilege escalation and credential theft. Changes like
- setUID/setGID and sensitive file reads are strong indicators of
- malicious activity.
- chmod Monitoring (setUID / setGID)
- Detects privilege escalation via modified binaries
- Example: chmod u+s /usr/bin/bash
- Maps to: MITRE ATT&CK T1548 – Abuse Elevation
- Control Mechanism
- Sensitive File Access Monitoring
- Tracks reads of /etc/passwd, /etc/shadow, SSH keys
- Detects credential harvesting activity
- Maps to: MITRE ATT&CK T1003 – OS Credential
- Dumping

**Speaker notes:**

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

## Slide 68 — File Permission & Access Monitoring

**On slide:**

- (ATT&CK MAPPING)

**Speaker notes:**

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

## Slide 69 — Designing A Detection — From

**On slide:**

- TECHNIQUE TO RULE
- Building a detection for a specific ATT&CK
- technique requires working backwards from the
- observable behavior to the log event it produces,
- then writing the filter that matches it precisely.

**Speaker notes:**

### Speaker Notes – Designing a Detection: From Technique to Rule

**Key message:** Detection engineering starts with attacker behavior, not technology. We begin with an ATT&CK technique, identify observable actions, determine what logs are generated, and then build detection logic around those artifacts.

---

### Detection Rules

Are metric filters matching?

---

---

## Slide 70 — Designing A Detection — From

**On slide:**

- TECHNIQUE TO RULE
- Example: detecting su abuse (T1548)
- 1. Technique: attacker runs su - root with a wrong
- password to attempt privilege escalation
- 2. System behavior: su calls PAM, PAM fails, auditd
- records the failure
- 3. Log entry: type=USER_AUTH msg=audit(...):
- exe="/usr/bin/su" res=failed
- 4. Filter pattern: exe="/usr/bin/su" res=failed
- 5. Metric: SuAbuse in the SOCLab namespace
- 6. Alarm: >= 1 occurrences in 1 minute

**Speaker notes:**

### Speaker Notes – Designing a Detection: From Technique to Rule (Example: Detecting `su` Abuse)

**Key message:** This slide demonstrates the complete thought process a detection engineer follows when transforming an ATT&CK technique into a working detection rule, metric, and alarm.

---

### Threat-to-Detection Workflow

Each catalog entry follows the same process:

![Threat-to-Detection Workflow](day2_diagrams/detection-engineering-vs-incident-response-196.svg)

This creates consistency across all detections.

---

---

## Slide 71 — Simulating Attacks Safely

**On slide:**

- Attack simulation in a lab is controlled, documented,
- and scoped to an isolated environment. The goal is to
- generate the same log events a real attacker would
- produce, without doing any actual damage.
- This approach mirrors a purple team exercise: the
- attacker and defender role are played by the same
- person, with full visibility into both sides.

**Speaker notes:**

### Speaker Notes – Simulating Attacks Safely

**Key message:** Effective detection engineering requires generating realistic attack activity, but it must be done in a controlled and safe manner. The objective is to create the same logs a real attacker would generate without causing harm to systems, data, or users.

---

### Speaker Notes – Red Team and Purple Team Operations

**Key message:** Red Teams simulate real-world attackers to identify weaknesses in security controls, while Purple Teams bring attackers and defenders together to improve detection, alerting, and incident response capabilities. Both are critical for measuring and improving SOC effectiveness.

---

---

## Slide 72 — Simulating Attacks Safely

**On slide:**

- Run attack commands only on your own lab instance,
- never against any other system
- Use the testattacker account for steps that require a non-
- privileged user
- Steps requiring sudo must be run as ec2-user —
- testattacker has no sudo
- Document what you ran, when, and what log events it
- produced
- Clean up test artifacts after validation: remove test
- accounts, cron entries, and audit rules

**Speaker notes:**

### Speaker Notes – Simulating Attacks Safely (Lab Rules & Operational Guidelines)

**Key message:** Detection testing must be realistic, but it must also be disciplined. These rules ensure participants generate useful security telemetry without creating risk to systems, other users, or the environment.

---

---

## Slide 73 — Reading Auditd Log Entries

**On slide:**

- auditd log entries are dense but
- follow a consistent key-value
- format. Learning to read them is
- a prerequisite for writing accurate
- filter patterns and validating that
- your detection rules fire on the
- right events.

**Speaker notes:**

### Read

- CloudWatch Logs
- Metrics
- Alarms
- Investigation Data

### Linux audit logs

`auditd`

---

---

## Slide 74 — Reading Auditd Log Entries

**On slide:**

- Example entry — failed su attempt:
- Key fields:
- exe — the binary that triggered the
- event
- res — success or failed
- acct — the account being targeted
- auid — the audit UID of the user
- who initiated the action
- type — the event category
- (USER_AUTH, ADD_USER, SYSCALL,
- etc.)

**Speaker notes:**

### Speaker Notes – Reading auditd Log Entries

**Key message:** Every detection begins with understanding the log data. Detection engineers must be able to read auditd records, identify important fields, and determine which values can be used to build reliable detection logic.

---

---

## Slide 75 — Incident Reporting — Structure

**On slide:**

- AND PURPOSE
- An incident report is the formal record
- of a security event from initial detection
- through closure.
- It serves as documentation for the
- current event, an artifact for compliance,
- and a learning record for improving
- future detections.

**Speaker notes:**

### Reporting

Executives and auditors understand attack coverage.

---

### Step 7: Investigation Report Generation

The AI creates a structured investigation summary.

Typical report sections:

### Structured Incident Report

Each participant will produce a professional incident report containing:

---

## Slide 76 — Incident Reporting — Structure

**On slide:**

- AND PURPOSE
- Incident summary — one paragraph: what
- happened, when, and how it was detected
- Timeline — ordered list of key events with
- UTC timestamps
- Attack details — which technique, which
- account or source, what was targeted
- Detection details — which metric filter and
- alarm fired; what the AI investigation
- concluded
- Analyst assessment — do you agree with the
- AI hypothesis? What did you verify?
- Closure — confirmed mitigated, confirmed
- false positive, or escalated for further action

**Speaker notes:**

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

## Slide 77 — Untitled

**Speaker notes:**

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

## Slide 78 — Ai Hypothesis Triage

**On slide:**

- An AI Operations investigation may generate multiple
- competing hypotheses for the same set of events. Deciding
- which is most credible requires applying analyst judgment
- to the AI's evidence citations.
- Read all hypotheses before accepting any. AI may have
- found something more important than the first item
- listed
- Locate the cited evidence in the raw log data
- Apply environment context. Is this activity expected
- given what you know about the system?
- Identify the most specific hypothesis. A hypothesis that
- cites a specific account, IP, and technique is more
- actionable than a vague "unusual activity" conclusion
- Document your decision, even if you close the
- investigation as a false positive

**Speaker notes:**

### Hypothesis

`Internal Security Scanner`

### Speaker Notes – AI Hypothesis Triage

---

### Speaker Notes – Evaluating AI-Generated Hypotheses

**Key message:** AI-generated hypotheses are suggestions, not conclusions. The analyst remains responsible for validation and decision-making.

---

---

## Slide 79 — Detection Coverage And Gaps

**On slide:**

- Building one detection rule is the start, not the
- end. A mature detection program maps every
- monitored technique against the full ATT&CK
- matrix to understand what is covered, what is
- partial, and what is a complete blind spot.
- For the lab environment after Lab 2.4: you will
- have coverage for 3-5 techniques. Identifying the
- remaining gaps and explaining what data source
- and rule would close each one is a core detection
- engineering skill.

**Speaker notes:**

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

## Slide 80 — Detection Coverage And Gaps

**On slide:**

- Which ATT&CK techniques affect my environment
- and have no detection rule at all?
- Which detections exist but have never been tested
- with real attack data?
- Which detections fire frequently but rarely result in
- confirmed true positives (noise)?
- Which techniques require data sources that are not
- yet collected?

**Speaker notes:**

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

## Slide 81 — Closing An Investigation —

**On slide:**

- DECISION FRAMEWORK
- Every investigation must be formally closed with a
- documented decision. Leaving investigations
- open or marking everything as "resolved" without
- review is as bad as having no detection in the first
- place.
- Always document *why* you made the decision,
- not just what it was. This record is the input for
- tuning the detection rule to reduce future false
- positives.
- Decision
- Meaning
- Required
- documentation
- True Positive
- Real attack
- activity confirmed
- Timeline,
- technique, impact,
- remediation taken
- False Positive
- Expected or
- benign activity
- Why the alert
- fired, why it is not
- a threat
- Inconclusive
- Evidence is
- ambiguous
- What was
- checked, what
- additional data is
- needed
- Escalated
- Requires higher-
- tier analyst
- What was found,
- why escalation is
- needed

**Speaker notes:**

### Speaker Notes – Closing an Investigation: Decision Framework

---

### Closure

Document:

* Root cause
* Lessons learned
* Follow-up actions

---

---

## Slide 82 — Pop Quiz:

**On slide:**

- You want to detect read attempts against /etc/shadow using a
- CloudWatch metric filter on the auditd log. Which filter pattern is correct?
- A. `shadow file read detected`
- B. `name="/etc/shadow"`
- C. `{ $.file = "/etc/shadow" && $.action = "read" }`
- D. `cat /etc/shadow`

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 83 — Pop Quiz:

**On slide:**

- You want to detect read attempts against /etc/shadow using a
- CloudWatch metric filter on the auditd log. Which filter pattern is correct?
- A. `shadow file read detected`
- B. `name="/etc/shadow"`
- C. `{ $.file = "/etc/shadow" && $.action = "read" }`
- D. `cat /etc/shadow`

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 84 — Pop Quiz:

**On slide:**

- A detection engineer wants to build a rule for T1136. Create Account (an
- attacker runs useradd to create a backdoor persistence account). Which
- approach correctly implements this detection?
- A. Create a metric filter on the sshd log group for the pattern `new user created`
- B. Create a metric filter on `/soc-lab/secure` for the auditd pattern `type=ADD_USER`, then create an alarm
- triggering on `>= 1` in 1 minute
- C. Set a CloudWatch alarm on the EC2 `CPUUtilization` metric, which spikes when `useradd` runs
- D. Install a third-party agent on the EC2 instance — auditd cannot detect account creation events

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 85 — Pop Quiz:

**On slide:**

- A detection engineer wants to build a rule for T1136 — Create Account (an attacker
- runs useradd to create a backdoor persistence account). Which approach correctly
- implements this detection?
- A. Create a metric filter on the sshd log group for the pattern `new user created`
- B. Create a metric filter on `/soc-lab/secure` for the auditd pattern `type=ADD_USER`, then create an alarm
- triggering on `>= 1` in 1 minute
- C. Set a CloudWatch alarm on the EC2 `CPUUtilization` metric, which spikes when `useradd` runs
- D. Install a third-party agent on the EC2 instance — auditd cannot detect account creation events

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 86 — Pop Quiz:

**On slide:**

- An AI Operations investigation was automatically triggered by a sudo failure alarm.
- The investigation concludes the failed attempt was made by ec2-user running a
- mistyped command. You confirm this by reviewing the raw audit log. What is the
- correct closure decision and documentation?
- A. True Positive — escalate to Tier 2 for further investigation of the `ec2-user` account
- B. False Positive — document that the alarm fired on an expected user running a mistyped command, and consider
- tuning the alarm to exclude `ec2-user`
- C. Inconclusive — close without documentation since it was clearly benign
- D. Escalated — all `sudo` failures involving `ec2-user` must be sent to the security team regardless of context

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 87 — Pop Quiz:

**On slide:**

- An AI Operations investigation was automatically triggered by a sudo failure alarm. The
- investigation concludes the failed attempt was made by ec2-user running a mistyped
- command. You confirm this by reviewing the raw audit log. What is the correct closure decision
- and documentation?
- A. True Positive — escalate to Tier 2 for further investigation of the `ec2-user` account
- B. False Positive — document that the alarm fired on an expected user running a mistyped command, and
- consider tuning the alarm to exclude `ec2-user`
- C. Inconclusive — close without documentation since it was clearly benign
- D. Escalated — all `sudo` failures involving `ec2-user` must be sent to the security team regardless of context

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 88 — Lab 2.3

**Speaker notes:** Discuss the question; reveal answer after student responses.

---

## Slide 89 — Congratulations

**On slide:**

- Over two days you built a complete, working
- security detection and investigation pipeline on
- AWS with an automated AI-assisted investigations
- triggered by real attack simulations.
- The skills you practiced here, telemetry
- configuration, detection engineering, AI
- hypothesis evaluation, and structured incident
- closure, are the same skills used in production
- SOC environments every day.
- Take the pipeline you built, adapt it to your own
- log sources, and keep expanding your ATT&CK
- coverage one detection at a time.

**Speaker notes:**

### Speaker Notes – Course Conclusion / Congratulations

---
