# Lab 2.2 — Visual Reference (Mermaid)

Diagrams for metric filters, dashboards, alarms, and automated AI triage.

Render in **GitHub** or VS Code with **Markdown Preview Mermaid Support**. Export PNG from [Mermaid Live Editor](https://mermaid.live/) into `lab 2.2 screenshots/` if needed.

---

## 1. Detection pipeline

```mermaid
graph LR
  LOG["nginx access.log<br/>404 responses"] --> MF["Metric filter<br/>nginx-scan-attempts"]
  MF --> MET["SOCLab/WebScanAttempts"]
  MET --> DASH["Dashboard<br/>soc-lab-web-monitor"]
  MET --> ALM["Alarm<br/>web-scan-alarm"]
  ALM --> AIO["AI Operations<br/>investigation"]
```

---

## 2. Dashboard widget types

```mermaid
graph TB
  D["soc-lab-web-monitor"] --> W1["404 rate over time"]
  D --> W2["Top scanned paths"]
  D --> W3["Source IPs"]
  D --> W4["Audit highlights"]
  D --> W5["Alarm status"]
```

---

## 3. Web probe signal (Step 2)

```mermaid
sequenceDiagram
    participant CS as CloudShell
    participant EC2 as EC2 nginx
    participant CW as CloudWatch
    CS->>EC2: curl /admin /login /.env ...
    EC2->>EC2: 404 access.log lines
    EC2->>CW: agent ships logs
    CW->>CW: metric WebScanAttempts++
```

---

*More diagrams will be added when the full guide is expanded.*
