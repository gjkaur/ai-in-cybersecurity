# Screenshot naming — `gurinder_practice`

Personal lab evidence stays **local only**. Screenshot folders are **gitignored** — never push them to GitHub.

---

## Folder layout

| Lab | Save screenshots here |
|-----|------------------------|
| 1.1 | `gurinder_practice/lab 1.1/lab 1.1 screenshots/` |
| 1.2 | `gurinder_practice/lab 1.2/lab 1.2 screenshots/` |
| 1.3 | `gurinder_practice/lab 1.3/lab 1.3 screenshots/` |
| 2.1 | `gurinder_practice/lab 2.1/lab 2.1 screenshots/` |
| 2.2 | `gurinder_practice/lab 2.2/lab 2.2 screenshots/` |
| 2.3 | `gurinder_practice/lab 2.3/lab 2.3 screenshots/` |

Create the folder if it does not exist. The space in `lab X.Y` matches the lab directory names.

---

## File naming rules

| Rule | Example |
|------|---------|
| Prefix with two-digit step number | `step-03-...` |
| Lowercase words separated by hyphens | `step-04-vscode-config.png` |
| Use `.png` | not `.jpg` or `.jpeg` |
| Match the step in the lab guide | Step 5 → `step-05-...` |
| Skip steps with no screenshot | Lab 1.1 has no `step-06` or `step-07` |

**Pattern:** `step-NN-short-description.png`

---

## Lab 1.1 — Instance setup

Guide: [lab 1.1/1.1-Instance-Setup-Guide.md](lab%201.1/1.1-Instance-Setup-Guide.md)

| Filename | Step | What to capture |
|----------|------|-----------------|
| `step-01-key.png` | 1 | CloudShell `ls -la ~/soc-lab-key.pem` or downloaded `.pem` in File Explorer |
| `step-02-instance.png` | 2 | `Instance ID:` in CloudShell or EC2 instance **running** |
| `step-03-ip.png` | 3 | Public IP in terminal or EC2 **Public IPv4** |
| `step-04-vscode-config.png` | 4 | SSH config (`HostName`, `IdentityFile`) — redact IP if sharing |
| `step-05-connected.png` | 5 | VS Code `SSH: SOC-Instance` + `whoami` / `pwd` |
| `step-08-nginx.png` | 8 | Browser **SOC Lab Service Running** or nginx access log |

Steps 6–7 have no required screenshot (terminal-only exercises).

---

## Lab 1.2 — Suspicious activity & AI triage

Guide: [lab 1.2/1.2-Suspicious-Activity-AI-Triage-Guide.md](lab%201.2/1.2-Suspicious-Activity-AI-Triage-Guide.md)

| Filename | Step | What to capture | Redact if sharing |
|----------|------|-----------------|-------------------|
| `step-01-baseline.png` | 1 | Baseline audit + nginx tail | IPs, hostnames |
| `step-02-ssh-fail.png` | 2 | journalctl failed SSH lines | Source IPs |
| `step-03-nginx-404.png` | 3 | access.log with suspicious paths | Client IPs |
| `step-04-auditctl.png` | 4 | `auditctl -l` with `sudoers_watch` | — |
| `step-05-ausearch.png` | 5 | ausearch CREATE event | — |
| `step-06-bedrock-key.png` | 6 | Bedrock API keys console page | **Key + account ID** |
| `step-07-ai-triage.png` | 7 | AI triage terminal output | IPs; never the `export` line |

---

## Lab 1.3 — GuardDuty & Security Hub

Guide: [lab 1.3/1.3-AI-Threat-Detection-Guide.md](lab%201.3/1.3-AI-Threat-Detection-Guide.md)

| Filename | Step | What to capture | Redact if sharing |
|----------|------|-----------------|-------------------|
| `step-01-guardduty-enabled.png` | 1 | GuardDuty enabled | Account ID |
| `step-02-security-hub-enabled.png` | 2 | Security Hub + standards | Account ID |
| `step-03-guardduty-finding.png` | 3 | SSH brute-force finding | Resource ARNs |
| `step-04-security-hub-findings.png` | 4 | Security Hub findings list | Account ID |
| `step-05-s3-misconfig.png` | 5 | S3 bucket public block off | Bucket name |
| `step-06-s3-remediated.png` | 6 | Finding resolved / block on | — |

---

## Lab 2.1 — CloudWatch log streaming

Guide: [lab 2.1/2.1-CloudWatch-Log-Streaming-Guide.md](lab%202.1/2.1-CloudWatch-Log-Streaming-Guide.md)

| Filename | Step | What to capture | Redact if sharing |
|----------|------|-----------------|-------------------|
| `step-01-iam-role.png` | 1 | EC2 with IAM role attached | Account ID |
| `step-02-agent-running.png` | 2 | CloudWatch agent active | — |
| `step-03-log-groups.png` | 3 | `/soc-lab/audit` + `/soc-lab/nginx` | — |
| `step-04-log-analytics.png` | 4 | Log Analytics query results | IPs in log lines |
| `step-05-ai-ops-enabled.png` | 5 | AI Operations configuration | Account ID |
| `step-06-investigation.png` | 6 | Investigation hypotheses | IPs, account ID |

---

## Lab 2.2 — Dashboard & automated detection

Guide: [lab 2.2/2.2-Security-Monitoring-Dashboard-Guide.md](lab%202.2/2.2-Security-Monitoring-Dashboard-Guide.md)

| Filename | Step | What to capture | Redact if sharing |
|----------|------|-----------------|-------------------|
| `step-01-metric-filter.png` | 1 | nginx 404 metric filter | — |
| `step-02-probe-signal.png` | 2 | Probe + nginx 404 lines | Source IP |
| `step-03-dashboard.png` | 3 | `soc-lab-web-monitor` dashboard | IPs in widgets |
| `step-04-alarm-ai-action.png` | 4 | Alarm + AI Operations action | — |
| `step-05-audit-filter.png` | 5 | Audit persistence filter | — |

---

## Lab 2.3 — Attack & detect capstone

Guide: [lab 2.3/2.3-Attack-Detect-Capstone-Guide.md](lab%202.3/2.3-Attack-Detect-Capstone-Guide.md)

| Filename | Step | What to capture | Redact if sharing |
|----------|------|-----------------|-------------------|
| `step-01-testattacker.png` | 1 | `id testattacker` | — |
| `step-02-threat-choice.png` | 2 | Threat selection notes | — |
| `step-03-pipeline.png` | 3 | Filter + alarm config | — |
| `step-04-attack-sim.png` | 4 | Simulation output | Passwords |
| `step-05-alarm-fired.png` | 5 | Alarm in ALARM state | — |
| `step-06-investigation.png` | 6 | AI investigation | IPs |
| `step-07-incident-report.png` | 7 | Report summary | IPs, account context |

---

## Never commit

- Screenshot files or folders
- `.pem` SSH keys
- Bedrock API keys
- `output.txt` or full terminal logs with account IDs
- Worksheet rows filled with real IPs or instance IDs
