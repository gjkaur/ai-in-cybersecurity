# Lab 1.1 — Visual Reference (Mermaid)

Use these in **GitHub**, **VS Code** (with [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)), or [Mermaid Live Editor](https://mermaid.live/).

Export PNG/SVG from Mermaid Live Editor into `lab 1.1 screenshots/` if you need image files.

---

## 1. Complete lab architecture

```mermaid
graph TB
    subgraph AWS["AWS Cloud (us-east-1)"]
        subgraph VPC["VPC"]
            subgraph Subnet["Public Subnet"]
                EC2["EC2 Instance<br/>Amazon Linux 2023<br/>t2.medium"]
                ENI["Elastic Network Interface<br/>Public IP assigned<br/>Security Group attached"]
            end
            SG["Security Group: soc-lab-sg<br/>Inbound: SSH 22, HTTP 80<br/>Outbound: all traffic"]
        end
        KeyPair["Key Pair: soc-lab-key<br/>RSA · .pem · private key only"]
    end

    subgraph Local["Your Windows PC"]
        VSCode["VS Code<br/>Remote - SSH"]
        Browser["Browser<br/>http://PUBLIC_IP"]
        SSHKey["soc-lab-key.pem<br/>Downloads folder"]
    end

    subgraph Services["Services on EC2"]
        Nginx["nginx · port 80<br/>index.html · access.log"]
        SSHD["sshd · port 22"]
    end

    VSCode -->|"SSH :22"| SSHD
    Browser -->|"HTTP :80"| Nginx
    SSHKey -.->|"authenticates"| KeyPair
    KeyPair -.->|"authorizes"| EC2
    SSHD --> EC2
    Nginx --> EC2
    EC2 --> ENI
    ENI --> SG

    style AWS fill:#f0f0ff,stroke:#333
    style VPC fill:#e6f2ff,stroke:#0066cc
    style EC2 fill:#ff9900,stroke:#232f3e,color:#fff
    style SG fill:#6c9bcf,stroke:#232f3e,color:#fff
    style KeyPair fill:#8c6cf0,stroke:#232f3e,color:#fff
    style Local fill:#f5f5f5,stroke:#999
    style Nginx fill:#009639,stroke:#232f3e,color:#fff
    style SSHD fill:#cc3333,stroke:#232f3e,color:#fff
```

---

## 2. SSH connection flow

```mermaid
sequenceDiagram
    participant User as You (Windows)
    participant VSCode as VS Code Remote-SSH
    participant SSH as SSH Client
    participant EC2 as EC2 Instance
    participant Key as soc-lab-key.pem

    User->>VSCode: Connect to SOC-Instance
    VSCode->>SSH: Start connection
    SSH->>Key: Read IdentityFile
    SSH->>EC2: Handshake on port 22
    EC2->>EC2: Verify public key match
    EC2->>SSH: Authentication success
    Note over EC2: User ec2-user · session open
    SSH->>VSCode: Terminal ready
    VSCode->>User: SSH: SOC-Instance connected
    Note over User,VSCode: whoami → ec2-user<br/>pwd → /home/ec2-user
```

---

## 3. Security group detail

```mermaid
graph LR
    subgraph Internet["Internet"]
        SSH_Client["SSH client<br/>your PC"]
        Web_Client["Web browser"]
    end

    subgraph SG["Security Group: soc-lab-sg"]
        direction TB
        subgraph Inbound["Inbound rules"]
            SSH_Rule["TCP 22 · SSH<br/>Source 0.0.0.0/0 · Allow"]
            HTTP_Rule["TCP 80 · HTTP<br/>Source 0.0.0.0/0 · Allow"]
        end
        subgraph Outbound["Outbound rules"]
            All_Traffic["All traffic · Allow"]
        end
    end

    subgraph Instance["EC2 Instance"]
        Port22["Port 22 · sshd"]
        Port80["Port 80 · nginx"]
    end

    SSH_Client -->|"TCP 22"| SSH_Rule
    Web_Client -->|"TCP 80"| HTTP_Rule
    SSH_Rule --> Port22
    HTTP_Rule --> Port80

    style Internet fill:#e8f5e9,stroke:#2e7d32
    style SG fill:#fff3e0,stroke:#e65100
    style Inbound fill:#ffebee,stroke:#c62828
    style SSH_Rule fill:#ffcdd2,stroke:#c62828
    style HTTP_Rule fill:#ffcdd2,stroke:#c62828
    style Port22 fill:#bbdefb,stroke:#1565c0
    style Port80 fill:#bbdefb,stroke:#1565c0
```

---

## 4. Linux permissions and chmod

```mermaid
graph TB
    subgraph Create["1. Create file"]
        A["echo 'Hello SOC' > hello.sh<br/>Default: rw-r--r-- (644)"]
    end

    subgraph Bits["2. Permission bits"]
        B["-rw-r--r-- ec2-user ec2-user<br/>owner · group · other<br/>r=read w=write x=execute"]
    end

    subgraph Chmod["3. chmod +x hello.sh"]
        Before["Before: -rw-r--r--<br/>not executable"]
        Cmd["chmod +x hello.sh<br/>adds x for u, g, o"]
        After["After: -rwxr-xr-x<br/>executable"]
        Before --> Cmd --> After
    end

    subgraph Run["4. Run script"]
        Exec["./hello.sh"]
        Out["Output: Hello SOC"]
        Exec --> Out
    end

    Create --> Bits --> Chmod
    After --> Run

    style Create fill:#e3f2fd,stroke:#1565c0
    style Bits fill:#f3e5f5,stroke:#6a1b9a
    style Chmod fill:#e8f5e9,stroke:#2e7d32
    style Run fill:#fff3e0,stroke:#e65100
    style Before fill:#ffcdd2,stroke:#c62828
    style After fill:#c8e6c9,stroke:#2e7d32
```

---

## 5. SetUID privilege escalation

```mermaid
graph TB
    subgraph Normal["Normal execution"]
        U1["User: ec2-user"]
        P1["Program owned by ec2-user"]
        R1["Runs with user privileges"]
        U1 --> P1 --> R1
    end

    subgraph SetUID["SetUID execution"]
        U2["User: ec2-user"]
        P2["/usr/bin/passwd<br/>-rwsr-xr-x · owner root"]
        R2["Runs as root (UID 0)"]
        Shadow["/etc/shadow"]
        U2 --> P2 --> R2
        R2 --> Shadow
    end

    subgraph Detect["Defender detection"]
        Find["find / -perm -4000 -exec ls -l {} \\; 2>/dev/null"]
        Examples["Common: passwd, sudo, mount, ping"]
        Find --> Examples
    end

    style Normal fill:#e3f2fd,stroke:#1565c0
    style SetUID fill:#ffebee,stroke:#c62828
    style Detect fill:#e8f5e9,stroke:#2e7d32
    style R2 fill:#ffcdd2,stroke:#c62828
```

---

## 6. nginx setup and logging

```mermaid
graph TB
    subgraph Install["1. Install"]
        DNF["sudo dnf install -y nginx"]
        DNF --> Bin["/usr/sbin/nginx"]
    end

    subgraph Service["2. Start service"]
        Enable["systemctl enable nginx"]
        Start["systemctl start nginx"]
        Enable --> Start
    end

    subgraph Page["3. Custom page"]
        HTML["index.html → /usr/share/nginx/html/"]
        HTML --> Serve["Serves on port 80"]
    end

    subgraph Logs["4. Access logs"]
        Curl["curl http://localhost x5"]
        Log["/var/log/nginx/access.log<br/>one line per request"]
        Curl --> Log
    end

    subgraph Test["5. Test"]
        Local["curl on EC2"]
        Browser["http://PUBLIC_IP from Windows"]
        Local --> Browser
    end

    Install --> Service --> Page --> Logs --> Test

    style Install fill:#e3f2fd,stroke:#1565c0
    style Service fill:#e8f5e9,stroke:#2e7d32
    style Page fill:#fff3e0,stroke:#e65100
    style Logs fill:#f3e5f5,stroke:#6a1b9a
    style Test fill:#ffebee,stroke:#c62828
```

---

## 7. Lab workflow (steps 1–8)

```mermaid
graph LR
    S1["1 Create key"] --> S2["2 Launch EC2"] --> S3["3 Get IP"]
    S3 --> S4["4 VS Code config"] --> S5["5 Connect SSH"]
    S5 --> S6["6 chmod script"] --> S7["7 SetUID find"] --> S8["8 nginx + browser"]

    style S1 fill:#e1f5fe,stroke:#01579b
    style S2 fill:#e1f5fe,stroke:#01579b
    style S3 fill:#e1f5fe,stroke:#01579b
    style S4 fill:#e1f5fe,stroke:#01579b
    style S5 fill:#e1f5fe,stroke:#01579b
    style S6 fill:#e1f5fe,stroke:#01579b
    style S7 fill:#e1f5fe,stroke:#01579b
    style S8 fill:#c8e6c9,stroke:#2e7d32
```

### Steps with verification

```mermaid
graph LR
    S1["Step 1<br/>create-key-pair"] --> V1["Key in Downloads"]
    V1 --> S2["Step 2<br/>run-instances"]
    S2 --> V2["Instance running"]
    V2 --> S3["Step 3<br/>describe-instances"]
    S3 --> V3["Public IP saved"]
    V3 --> S4["Step 4<br/>~/.ssh/config"]
    S4 --> V4["SOC-Instance listed"]
    V4 --> S5["Step 5<br/>Connect"]
    V5["whoami = ec2-user"] --> S6["Step 6<br/>chmod +x"]
    S5 --> V5
    S6 --> V6["Hello SOC"]
    V6 --> S7["Step 7<br/>find SetUID"]
    S7 --> V7["sudo in list"]
    V7 --> S8["Step 8<br/>nginx"]
    S8 --> V8["Browser OK"]

    style V1 fill:#c8e6c9,stroke:#2e7d32
    style V2 fill:#c8e6c9,stroke:#2e7d32
    style V3 fill:#c8e6c9,stroke:#2e7d32
    style V4 fill:#c8e6c9,stroke:#2e7d32
    style V5 fill:#c8e6c9,stroke:#2e7d32
    style V6 fill:#c8e6c9,stroke:#2e7d32
    style V7 fill:#c8e6c9,stroke:#2e7d32
    style V8 fill:#c8e6c9,stroke:#2e7d32
```

---

## 8. Troubleshooting flowchart

```mermaid
graph TD
    Start["Problem?"] --> C1{"SSH timeout?"}
    C1 -->|Yes| T1["Instance running?<br/>Correct IP in config?<br/>SG allows port 22?"]
    C1 -->|No| C2{"Permission denied?"}
    C2 -->|Yes| T2["User = ec2-user<br/>Correct .pem path<br/>chmod 400 on key"]
    C2 -->|No| C3{"Browser won't load?"}
    C3 -->|Yes| T3["curl localhost on EC2<br/>SG allows port 80<br/>nginx running?"]
    C3 -->|No| C4{"CloudShell vars lost?"}
    C4 -->|Yes| T4["Copy Instance ID from console<br/>Re-run describe-instances"]
    C4 -->|No| C5{"IP changed?"}
    C5 -->|Yes| T5["Get new public IP<br/>Update VS Code SSH config"]
    C5 -->|No| T6["Check SG: TCP 22 and 80 open"]
    T1 --> OK["Resolved"]
    T2 --> OK
    T3 --> OK
    T4 --> OK
    T5 --> OK
    T6 --> OK

    style Start fill:#ffebee,stroke:#c62828
    style OK fill:#c8e6c9,stroke:#2e7d32
```

---

## 9. AWS services and cost (us-east-1)

```mermaid
pie title Lab cost breakdown (approximate)
    "EC2 t2.medium (~$0.05/hr)" : 85
    "Data transfer (minimal)" : 10
    "EBS 8 GB root volume" : 5
```

```mermaid
graph LR
    EC2["EC2 t2.medium<br/>Virtual server"]
    EBS["EBS 8 GB<br/>Root disk"]
    VPC["Default VPC<br/>No extra charge"]
    SG["Security Group<br/>No extra charge"]
    KP["Key Pair<br/>No extra charge"]

    EC2 --> EBS
    EC2 --> VPC
    EC2 --> SG
    EC2 --> KP

    style EC2 fill:#ff9900,color:#fff,stroke:#232f3e
    style EBS fill:#6c9bcf,color:#fff,stroke:#232f3e
    style VPC fill:#1a73e8,color:#fff,stroke:#232f3e
    style SG fill:#34a853,color:#fff,stroke:#232f3e
    style KP fill:#ea4335,color:#fff,stroke:#232f3e
```

---

## Static SVG fallbacks

If Mermaid does not render, use the generated SVG files (run `python build_diagrams.py`):

| Topic | File |
|-------|------|
| Architecture | `01-architecture.svg` |
| VPC / Security Group | `02-vpc-networking.svg` |
| SSH keys | `03-ssh-keys.svg` |
| chmod | `04-chmod-flow.svg` |
| SetUID | `05-setuid-flow.svg` |
| nginx logs | `06-nginx-telemetry.svg` |
| Roadmap | `00-complete-roadmap.svg` |
