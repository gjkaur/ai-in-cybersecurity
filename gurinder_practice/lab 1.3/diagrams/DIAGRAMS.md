# Lab 1.3 — Visual Reference (Mermaid)

Diagrams for GuardDuty, Security Hub, and the S3 misconfiguration loop.

Render in **GitHub** or VS Code with **Markdown Preview Mermaid Support**. Export PNG from [Mermaid Live Editor](https://mermaid.live/) into `lab 1.3 screenshots/` if needed.

---

## 1. Lab flow overview

```mermaid
graph TB
    subgraph Enable["Steps 1–2 — Enable"]
        GD["GuardDuty"]
        SH["Security Hub"]
    end

    subgraph Detect["Steps 3–4 — Review"]
        F1["SSH brute-force finding"]
        F2["Posture + ATT&CK findings"]
    end

    subgraph S3Loop["Steps 5–6 — S3 loop"]
        C["Create bucket<br/>public block OFF"]
        D["Security Hub S3.1"]
        R["Remediate<br/>public block ON"]
    end

    L12["Lab 1.2 telemetry"] --> GD
    GD --> SH
    SH --> F1
    SH --> F2
    C --> D
    D --> R
    R --> SH
```

---

## 2. Data sources GuardDuty analyzes

```mermaid
graph LR
    CT["CloudTrail<br/>API calls"] --> GD["GuardDuty ML"]
    VPC["VPC Flow Logs<br/>network"] --> GD
    DNS["DNS logs<br/>queries"] --> GD
    GD --> FIND["Findings"]
    FIND --> SH["Security Hub"]
```

---

## 3. S3 defender loop

```mermaid
graph LR
    A["Misconfigure S3<br/>block public access OFF"] --> B["Security Hub<br/>S3.1 finding ACTIVE"]
    B --> C["Fix permissions<br/>block ON"]
    C --> D["Finding RESOLVED"]
```

---

## 4. Lab chain (1.1 → 1.3)

```mermaid
graph LR
    L11["Lab 1.1<br/>EC2 + nginx"] --> L12["Lab 1.2<br/>simulate attacks"]
    L12 --> L13["Lab 1.3<br/>GuardDuty detects"]
```

---

*More diagrams will be added when the full guide is expanded.*
