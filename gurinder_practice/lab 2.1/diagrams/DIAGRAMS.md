# Lab 2.1 — Visual Reference (Mermaid)

Diagrams for CloudWatch log streaming and AI Operations investigations.

Render in **GitHub** or VS Code with **Markdown Preview Mermaid Support**. Export PNG from [Mermaid Live Editor](https://mermaid.live/) into `lab 2.1 screenshots/` if needed.

---

## 1. Lab flow overview

```mermaid
graph TB
    subgraph EC2["EC2 instance"]
        AUD["/var/log/audit/audit.log"]
        NGX["/var/log/nginx/access.log"]
        AG["CloudWatch agent"]
    end

    subgraph AWS["CloudWatch"]
        LG1["/soc-lab/audit"]
        LG2["/soc-lab/nginx"]
        LA["Log Analytics AI"]
        AIO["AI Operations"]
    end

    AUD --> AG
    NGX --> AG
    AG --> LG1
    AG --> LG2
    LG1 --> LA
    LG2 --> LA
    LG1 --> AIO
```

---

## 2. IAM instance profile

```mermaid
graph LR
    EC2["EC2"] --> IP["Instance profile<br/>soc-lab-ec2-monitoring"]
    IP --> ROLE["IAM role"]
    ROLE --> CW["CloudWatchAgentServerPolicy"]
    ROLE --> SSM["AmazonSSMManagedInstanceCore"]
```

---

## 3. Lab chain (1.2 → 2.1 → 2.2)

```mermaid
graph LR
    L12["Lab 1.2<br/>attacks + logs"] --> L21["Lab 2.1<br/>stream to CloudWatch"]
    L21 --> L22["Lab 2.2<br/>dashboard + alarms"]
    L22 --> L23["Lab 2.3<br/>capstone"]
```

---

*More diagrams will be added when the full guide is expanded.*
