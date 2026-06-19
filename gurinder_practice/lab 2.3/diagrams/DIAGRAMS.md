# Lab 2.3 — Visual Reference (Mermaid)

Diagrams for the attack-and-detect capstone.

Render in **GitHub** or VS Code with **Markdown Preview Mermaid Support**. Export PNG from [Mermaid Live Editor](https://mermaid.live/) into `lab 2.3 screenshots/` if needed.

---

## 1. Capstone loop

```mermaid
graph TB
    T["Choose threat A–E"] --> B["Build pipeline<br/>filter + alarm + widget"]
    B --> S["Simulate attack"]
    S --> V["Verify alarm fires"]
    V --> AI["AI investigation"]
    AI --> R["Incident report"]
```

---

## 2. End-to-end telemetry path

```mermaid
graph LR
    ATK["testattacker / probe"] --> AUD["auditd"]
    AUD --> CW["/soc-lab/audit"]
    CW --> MF["Your metric filter"]
    MF --> ALM["Your alarm"]
    ALM --> AIO["AI Operations"]
```

---

## 3. Threat menu overview

```mermaid
graph TB
    M["Threat menu"] --> A["A SSH brute force"]
    M --> B["B New account"]
    M --> C["C /etc/shadow read"]
    M --> D["D su abuse"]
    M --> E["E Cron persistence"]
```

---

*More diagrams will be added when the full guide is expanded.*
