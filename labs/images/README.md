# Lab images

Visual assets for the SOC lab guides. All paths in lab markdown use `/labs/images/<filename>`.

## Architecture diagrams (SVG)

| File | Used in |
|------|---------|
| `lab-1.1-architecture.svg` | Lab 1.1 — EC2, SSH, nginx setup |
| `lab-1.2-attack-triage-flow.svg` | Lab 1.2 — attack simulation and AI triage |
| `lab-1.3-detection-flow.svg` | Lab 1.3 — GuardDuty and Security Hub |
| `lab-1.3-s3-defender-loop.svg` | Lab 1.3 — S3 misconfiguration loop |
| `lab-2.1-cloudwatch-pipeline.svg` | Lab 2.1 — CloudWatch log streaming |
| `lab-2.2-detection-pipeline.svg` | Lab 2.2 — metric filters, alarms, dashboard |
| `lab-2.3-capstone-loop.svg` | Lab 2.3 — attack and detect capstone |

## Console screenshots (PNG)

| File | Used in |
|------|---------|
| `aws-cloudshell-download.png` | Lab 1.1 — download SSH key |
| `remote-ssh.png` | Lab 1.1 — VS Code Remote SSH settings |
| `remote-ssh-connect.png` | Lab 1.1 — connect to SOC-Instance |
| `remote-ssh-open-home.png` | Lab 1.1 — open home folder |
| `ssh-new-terminal.png` | Lab 1.1 — terminal on EC2 |
| `bedrock-api-keys.png` | Lab 1.2 — Bedrock API key generation |
| `guardduty-enable.png` | Lab 1.3 — enable GuardDuty |
| `security-hub-get-started.png` | Lab 1.3 — enable Security Hub |
| `guard-duty-findings.png` | Lab 1.3 — GuardDuty findings |
| `security-hub-all-findings.png` | Lab 1.3 — Security Hub findings |
| `log-analytics-build-query.png` | Lab 2.1 — Log Analytics AI query |
| `log-analytics-file-view.png` | Lab 2.1 — log file view |
| `investigation-query.png` | Labs 2.1, 2.3 — AI Operations investigation |
| `create-investigation.png` | Labs 2.1, 2.3 — create investigation |
| `create-log-filter.png` | Labs 2.2, 2.3 — metric filter creation |
| `log-filter-metric.png` | Lab 2.2 — filter pattern |
| `metric-details.png` | Lab 2.2 — metric namespace and name |
| `new-widget.png` | Lab 2.2 — dashboard widget |
| `graphed-metrics.png` | Lab 2.2 — graphed metrics |
| `log-widget.png` | Lab 2.2 — logs table widget |
| `Generate-new-query.png` | Lab 2.2 — query generator |
| `create-alarm.png` | Labs 2.2, 2.3 — create alarm |

> Do not add API keys, `.pem` files, instance IPs, or account IDs to images committed to this repo.
