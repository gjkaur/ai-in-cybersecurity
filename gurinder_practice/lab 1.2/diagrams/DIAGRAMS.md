# Lab 1.2 — Visual Reference (Mermaid)

Diagrams for suspicious-activity simulation, evidence collection, and AI triage.

Render in **GitHub** or VS Code with **Markdown Preview Mermaid Support**. Export PNG from [Mermaid Live Editor](https://mermaid.live/) into `lab 1.2 screenshots/` if needed.

---

## 1. Complete lab flow

```mermaid
graph TB
    subgraph Prereq["Prerequisites"]
        L11["Lab 1.1 complete<br/>EC2 + nginx running"]
    end

    subgraph Simulate["Simulate attack (CloudShell)"]
        SSH["Failed SSH x5<br/>fakeuser@PUBLIC_IP"]
        WEB["curl suspicious paths<br/>/admin /.env /wp-admin ..."]
    end

    subgraph Collect["Collect evidence (EC2)"]
        J["journalctl -u sshd"]
        N["nginx access.log"]
        A["auditd + ausearch"]
    end

    subgraph Triage["AI triage (EC2)"]
        B["Bedrock API key"]
        P["soc_triage.py"]
        R["SOC analysis output"]
    end

    L11 --> SSH
    L11 --> WEB
    SSH --> J
    WEB --> N
    J --> P
    N --> P
    A --> P
    B --> P
    P --> R

    style Simulate fill:#ffebee,stroke:#c62828
    style Collect fill:#e3f2fd,stroke:#1565c0
    style Triage fill:#e8f5e9,stroke:#2e7d32
```

---

## 2. SSH brute-force simulation

```mermaid
sequenceDiagram
    participant CS as CloudShell
    participant SG as Security Group
    participant EC2 as EC2 sshd
    participant Log as journalctl

    CS->>SG: SSH fakeuser@PUBLIC_IP:22
    SG->>EC2: Allow TCP 22
    EC2->>EC2: Reject — no such user / bad key
    EC2->>Log: Failed auth event
    Note over CS,Log: Repeat 5 times · T1110
```

---

## 3. Web recon probes

```mermaid
graph LR
    CS["CloudShell / Browser"] -->|"GET /admin"| NGX["nginx :80"]
    CS -->|"GET /.env"| NGX
    CS -->|"GET /wp-admin"| NGX
    NGX --> LOG["access.log<br/>404 entries"]
    LOG --> AI["Later: AI + CloudWatch"]

    style CS fill:#fff3e0,stroke:#e65100
    style NGX fill:#e8f5e9,stroke:#2e7d32
    style LOG fill:#f3e5f5,stroke:#6a1b9a
```

---

## 4. auditd sudoers watch

```mermaid
graph TB
    subgraph Setup["Step 4 — audit rule"]
        D["auditctl -D<br/>remove suppression"]
        R["auditctl -a ... dir=/etc/sudoers.d/<br/>-k sudoers_watch"]
        D --> R
    end

    subgraph Attack["Step 5 — persistence sim"]
        T["echo ... | sudo tee<br/>/etc/sudoers.d/lab-backdoor"]
    end

    subgraph Evidence["Evidence"]
        AS["ausearch -k sudoers_watch"]
        RAW["grep lab-backdoor audit.log"]
    end

    R --> T
    T --> AS
    T --> RAW

    style Attack fill:#ffebee,stroke:#c62828
    style Evidence fill:#e8f5e9,stroke:#2e7d32
```

---

## 5. SetUID vs sudoers persistence (context)

```mermaid
graph LR
    U["ec2-user"] -->|"tee command"| F["/etc/sudoers.d/lab-backdoor"]
    F -->|"NOPASSWD ALL"| P["Persistent root access"]
    A["auditd CREATE event"] -.->|"detects"| F

    style F fill:#ffcdd2,stroke:#c62828
    style A fill:#c8e6c9,stroke:#2e7d32
```

---

## 6. AI SOC triage pipeline

```mermaid
graph LR
    subgraph Inputs["Last 50 lines each"]
        AL["/var/log/audit/audit.log"]
        NL["/var/log/nginx/access.log"]
    end

    subgraph Bedrock["Amazon Bedrock us-east-1"]
        M["mistral.mistral-large-2402-v1:0"]
    end

    subgraph Output["SOC analysis"]
        O1["Findings"]
        O2["ATT&CK mapping"]
        O3["Risk level"]
        O4["Next steps"]
    end

    AL --> P["soc_triage.py"]
    NL --> P
    K["Bedrock API key"] --> P
    P --> M
    M --> O1
    M --> O2
    M --> O3
    M --> O4
```

---

## 7. ATT&CK technique map

```mermaid
graph TB
    subgraph Techniques["MITRE ATT&CK"]
        T1110["T1110 Brute Force"]
        T1190["T1190 Exploit Public-Facing Application"]
        T1548["T1548 Abuse Elevation Control"]
    end

    subgraph Lab["Lab 1.2 activity"]
        SSH["5x failed SSH"]
        WEB["404 path scans"]
        SUDO["sudoers.d backdoor"]
    end

    T1110 --> SSH
    T1190 --> WEB
    T1548 --> SUDO

    style T1110 fill:#ffcdd2,stroke:#c62828
    style T1190 fill:#fff9c4,stroke:#f9a825
    style T1548 fill:#ffcdd2,stroke:#c62828
```

---

## 8. Lab workflow with verification

```mermaid
graph LR
    S1["1 Baseline"] --> V1["Logs captured"]
    V1 --> S2["2 SSH fails"]
    S2 --> V2["journalctl shows failures"]
    V2 --> S3["3 Web probes"]
    S3 --> V3["404s in access.log"]
    V3 --> S4["4 auditd rule"]
    S4 --> V4["sudoers_watch active"]
    V4 --> S5["5 Backdoor file"]
    S5 --> V5["ausearch CREATE"]
    V5 --> S6["6 Bedrock key"]
    S6 --> S7["7 soc_triage.py"]
    S7 --> V7["AI analysis printed"]

    style V1 fill:#c8e6c9,stroke:#2e7d32
    style V2 fill:#c8e6c9,stroke:#2e7d32
    style V3 fill:#c8e6c9,stroke:#2e7d32
    style V4 fill:#c8e6c9,stroke:#2e7d32
    style V5 fill:#c8e6c9,stroke:#2e7d32
    style V7 fill:#c8e6c9,stroke:#2e7d32
```

---

## 9. Troubleshooting flowchart

```mermaid
graph TD
    Start["Problem?"] --> C1{"No SSH failures?"}
    C1 -->|Yes| T1["Check PUBLIC_IP<br/>Re-run CloudShell loop"]
    C1 -->|No| C2{"No nginx 404s?"}
    C2 -->|Yes| T2["nginx running<br/>Re-run curls"]
    C2 -->|No| C3{"No audit event?"}
    C3 -->|Yes| T3["Re-add auditctl rule<br/>Re-run tee backdoor"]
    C3 -->|No| C4{"Bedrock error?"}
    C4 -->|Yes| T4["API key + model access<br/>sudo pip install boto3"]
    T1 --> OK["Resolved"]
    T2 --> OK
    T3 --> OK
    T4 --> OK

    style Start fill:#ffebee,stroke:#c62828
    style OK fill:#c8e6c9,stroke:#2e7d32
```

---

## 10. Connection to later labs

```mermaid
graph LR
    L12["Lab 1.2 logs"] --> CW["Day 2 CloudWatch"]
    CW --> DET["Automated detection"]
    L12 --> L21["Lab 2.1<br/>backdoor + rule remain"]
    BACK["lab-backdoor file"] --> L21
    RULE["sudoers_watch rule"] --> L21
```
