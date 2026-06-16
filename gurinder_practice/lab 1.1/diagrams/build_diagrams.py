"""Regenerate lab 1.1 SVG diagrams — polished layout, clear arrows."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, Sans-serif"

SHADOW = """
    <filter id="sh" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.12"/>
    </filter>"""

GRAD_AWS = """
    <linearGradient id="aws" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF9900"/><stop offset="100%" stop-color="#E65100"/>
    </linearGradient>"""


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def mk(color: str, id_: str) -> str:
    return (
        f'<marker id="{id_}" viewBox="0 0 12 12" refX="10" refY="6" '
        f'markerWidth="8" markerHeight="8" orient="auto">'
        f'<path d="M1 2 L10 6 L1 10" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker>'
    )


def arr(d: str, color: str, mid: str, label: str = "") -> str:
    mid_attr = f' marker-mid="url(#{mid})"' if mid else ""
    lbl = ""
    if label:
        lx, ly = label.split(",")
        lbl = (
            f'<rect x="{int(lx)-36}" y="{int(ly)-11}" width="72" height="18" rx="9" '
            f'fill="#FFF" stroke="{color}" stroke-width="1"/>'
            f'<text x="{lx}" y="{int(ly)+4}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="10" font-weight="600" fill="{color}">{label.split(",")[2] if len(label.split(","))>2 else ""}</text>'
        )
    # label format: "x,y,text" via separate - simplify with explicit params in calls
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{mid})"{mid_attr}/>{lbl}'


def labeled_path(d, color, mid, tx, ty, text):
    w = len(text) * 6 + 16
    return f"""
  <path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{mid})"/>
  <rect x="{tx - w//2}" y="{ty - 12}" width="{w}" height="20" rx="10" fill="#FFF" stroke="{color}" stroke-width="1"/>
  <text x="{tx}" y="{ty + 2}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="{color}">{text}</text>"""


# ── 01 Architecture ──────────────────────────────────────────────────────────
write("01-architecture.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" role="img" aria-label="Lab architecture">
  <defs>
    {SHADOW}
    {GRAD_AWS}
    {mk("#2563EB", "ssh")}
    {mk("#16A34A", "http")}
    {mk("#64748B", "net")}
  </defs>
  <rect width="900" height="480" fill="#F1F5F9"/>
  <rect x="24" y="24" width="852" height="432" rx="16" fill="#FFF" stroke="#E2E8F0" filter="url(#sh)"/>

  <text x="450" y="58" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">Lab Architecture</text>
  <text x="450" y="78" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Your PC connects over the internet to EC2 inside AWS</text>

  <!-- Internet -->
  <rect x="48" y="96" width="804" height="40" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="1.5"/>
  <circle cx="72" cy="116" r="10" fill="#0284C7" opacity="0.2"/>
  <circle cx="72" cy="116" r="5" fill="none" stroke="#0284C7" stroke-width="1.5"/>
  <text x="450" y="122" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#0369A1">Internet</text>

  <!-- Your PC -->
  <g filter="url(#sh)">
    <rect x="48" y="160" width="200" height="200" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  </g>
  <rect x="68" y="178" width="36" height="28" rx="6" fill="#2563EB"/>
  <rect x="74" y="184" width="24" height="16" rx="2" fill="#DBEAFE" stroke="#FFF" stroke-width="1"/>
  <text x="128" y="198" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Your PC</text>
  <text x="128" y="218" font-family="{FONT}" font-size="11" fill="#475569">VS Code + browser</text>
  <text x="128" y="236" font-family="{FONT}" font-size="11" fill="#475569">soc-lab-key.pem</text>
  <g>
    <rect x="68" y="258" width="76" height="28" rx="6" fill="#2563EB"/>
    <text x="106" y="277" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">SSH :22</text>
    <rect x="152" y="258" width="76" height="28" rx="6" fill="#16A34A"/>
    <text x="192" y="277" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">HTTP :80</text>
  </g>

  <!-- VPC -->
  <rect x="280" y="148" width="572" height="224" rx="12" fill="#FAFAFA" stroke="#94A3B8" stroke-width="2" stroke-dasharray="8 4"/>
  <text x="300" y="172" font-family="{FONT}" font-size="12" font-weight="700" fill="#64748B">VPC (Virtual Private Cloud)</text>

  <!-- Security Group -->
  <rect x="300" y="184" width="532" height="172" rx="10" fill="#FFF7ED" stroke="#F59E0B" stroke-width="2"/>
  <text x="320" y="208" font-family="{FONT}" font-size="12" font-weight="700" fill="#92400E">Security Group</text>
  <rect x="320" y="216" width="88" height="24" rx="5" fill="#DC2626"/>
  <text x="364" y="232" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="700" fill="#FFF">ALLOW :22</text>
  <rect x="416" y="216" width="88" height="24" rx="5" fill="#DC2626"/>
  <text x="460" y="232" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="700" fill="#FFF">ALLOW :80</text>
  <text x="520" y="232" font-family="{FONT}" font-size="9" fill="#64748B">deny all other ports</text>

  <!-- EC2 -->
  <rect x="320" y="252" width="492" height="88" rx="10" fill="url(#aws)" stroke="#C2410C" stroke-width="2"/>
  <text x="340" y="278" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">EC2</text>
  <text x="340" y="296" font-family="{FONT}" font-size="10" fill="#FFF7ED">Amazon Linux 2023 · t2.medium</text>
  <rect x="520" y="264" width="130" height="56" rx="8" fill="rgba(255,255,255,0.25)" stroke="#FFF" stroke-width="1.5"/>
  <text x="585" y="288" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#FFF">nginx</text>
  <text x="585" y="304" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#FFF7ED">listens :80</text>
  <rect x="660" y="264" width="140" height="56" rx="8" fill="rgba(255,255,255,0.25)" stroke="#FFF" stroke-width="1.5"/>
  <text x="730" y="288" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">access.log</text>
  <text x="730" y="304" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#FFF7ED">telemetry</text>

  <!-- Arrows through internet to EC2 -->
  {labeled_path("M248 272 L248 116 L400 116 L400 252", "#2563EB", "ssh", 280, 108, "SSH")}
  {labeled_path("M248 286 L248 116 L680 116 L680 272", "#16A34A", "http", 520, 108, "HTTP")}

  <rect x="48" y="400" width="804" height="36" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
  <rect x="68" y="412" width="12" height="12" rx="2" fill="#2563EB"/>
  <text x="88" y="422" font-family="{FONT}" font-size="10" fill="#475569">SSH = remote terminal</text>
  <rect x="210" y="412" width="12" height="12" rx="2" fill="#16A34A"/>
  <text x="230" y="422" font-family="{FONT}" font-size="10" fill="#475569">HTTP = web browser</text>
  <rect x="380" y="412" width="12" height="12" rx="2" fill="#FF9900"/>
  <text x="400" y="422" font-family="{FONT}" font-size="10" fill="#475569">Orange = AWS resources</text>
</svg>
""")


# ── 02 VPC ────────────────────────────────────────────────────────────────
write("02-vpc-networking.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 400" role="img" aria-label="VPC networking">
  <defs>
    {SHADOW}
    {mk("#334155", "in")}
    {mk("#16A34A", "ok")}
  </defs>
  <rect width="860" height="400" fill="#F1F5F9"/>
  <text x="430" y="40" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">VPC &amp; Security Group</text>
  <text x="430" y="62" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Firewall rules filter traffic before it reaches your instance</text>

  <!-- Internet source -->
  <rect x="40" y="88" width="100" height="72" rx="10" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" filter="url(#sh)"/>
  <text x="90" y="118" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#0369A1">Internet</text>
  <text x="90" y="136" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">incoming</text>

  <path d="M140 124 L175 124" fill="none" stroke="#334155" stroke-width="2.5" marker-end="url(#in)"/>
  <text x="158" y="116" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="600" fill="#334155">ingress</text>

  <!-- VPC outer -->
  <rect x="180" y="80" width="640" height="260" rx="14" fill="#FFF" stroke="#64748B" stroke-width="2" stroke-dasharray="8 4" filter="url(#sh)"/>
  <text x="200" y="104" font-family="{FONT}" font-size="12" font-weight="700" fill="#475569">VPC</text>
  <text x="500" y="104" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Subnet</text>

  <!-- Security Group -->
  <rect x="210" y="120" width="280" height="190" rx="12" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="350" y="148" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#991B1B">Security Group</text>
  <text x="350" y="166" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#7F1D1D">Virtual firewall</text>
  <rect x="240" y="182" width="110" height="30" rx="6" fill="#DC2626"/>
  <text x="295" y="202" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">TCP :22</text>
  <rect x="360" y="182" width="110" height="30" rx="6" fill="#DC2626"/>
  <text x="415" y="202" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">TCP :80</text>
  <rect x="240" y="224" width="230" height="30" rx="6" fill="#64748B"/>
  <text x="355" y="244" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">implicit deny (all else blocked)</text>
  <text x="350" y="278" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Only listed ports pass through</text>

  <path d="M490 215 L530 215" fill="none" stroke="#16A34A" stroke-width="3" marker-end="url(#ok)"/>
  <text x="510" y="206" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="600" fill="#15803D">allowed</text>

  <!-- EC2 -->
  <rect x="530" y="160" width="260" height="130" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <rect x="550" y="178" width="220" height="48" rx="8" fill="#FFF" stroke="#86EFAC"/>
  <text x="660" y="200" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">EC2 Instance</text>
  <text x="660" y="218" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">Amazon Linux 2023</text>
  <text x="660" y="262" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Traffic must match SG rules</text>

  <rect x="40" y="360" width="780" height="28" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="430" y="379" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#1E40AF">Think of the Security Group as a bouncer — only ports 22 and 80 get in.</text>
</svg>
""")


# ── 03 SSH ────────────────────────────────────────────────────────────────
write("03-ssh-keys.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 300" role="img" aria-label="SSH key authentication">
  <defs>
    {SHADOW}
    {mk("#2563EB", "k")}
  </defs>
  <rect width="860" height="300" fill="#F1F5F9"/>
  <text x="430" y="40" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">SSH Key Authentication</text>
  <text x="430" y="62" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Private key on your PC matches public key on the server</text>

  <g filter="url(#sh)">
    <rect x="48" y="96" width="240" height="160" rx="14" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  </g>
  <text x="168" y="128" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Your PC</text>
  <rect x="76" y="144" width="184" height="52" rx="8" fill="#FFF" stroke="#93C5FD" stroke-width="2"/>
  <path d="M96 168 L96 184 L108 184 L108 176 L120 188 L132 176 L132 184 L144 184" fill="none" stroke="#2563EB" stroke-width="2"/>
  <text x="168" y="176" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">soc-lab-key.pem</text>
  <text x="168" y="216" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Private key (secret)</text>
  <text x="168" y="234" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#DC2626" font-weight="600">Never share this file</text>

  <g filter="url(#sh)">
    <rect x="572" y="96" width="240" height="160" rx="14" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  </g>
  <text x="692" y="128" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">EC2 Server</text>
  <rect x="600" y="144" width="184" height="52" rx="8" fill="#FFF" stroke="#86EFAC" stroke-width="2"/>
  <rect x="620" y="160" width="28" height="36" rx="4" fill="none" stroke="#16A34A" stroke-width="2"/>
  <path d="M634 188 L634 200" fill="none" stroke="#16A34A" stroke-width="2"/>
  <text x="692" y="176" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">authorized_keys</text>
  <text x="692" y="216" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Public key (from AWS)</text>
  <text x="692" y="234" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Login: ec2-user</text>

  <!-- Key pair link -->
  <rect x="320" y="132" width="220" height="88" rx="12" fill="#FFF" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="6 3"/>
  <text x="430" y="158" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#2563EB">Encrypted tunnel</text>
  <text x="430" y="178" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Port 22 · no password</text>
  <text x="430" y="198" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">VS Code Remote-SSH</text>

  <path d="M288 176 L318 176" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#k)"/>
  <path d="M542 176 L572 176" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#k)"/>
</svg>
""")


# ── 04 chmod ─────────────────────────────────────────────────────────────
write("04-chmod-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 260" role="img" aria-label="chmod flow">
  <defs>
    {SHADOW}
    {mk("#475569", "f")}
  </defs>
  <rect width="880" height="260" fill="#F1F5F9"/>
  <text x="440" y="36" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">chmod +x — Make a Script Runnable</text>

  <!-- Step 1 -->
  <circle cx="80" cy="100" r="18" fill="#F59E0B"/>
  <text x="80" y="106" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">1</text>
  <rect x="40" y="128" width="110" height="72" rx="10" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2" filter="url(#sh)"/>
  <text x="95" y="156" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#92400E">hello.sh</text>
  <text x="95" y="178" text-anchor="middle" font-family="monospace" font-size="11" fill="#78350F">-rw-r--r--</text>
  <text x="95" y="192" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">not executable</text>

  <path d="M150 164 L178 164" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#f)"/>
  <rect x="178" y="148" width="72" height="22" rx="11" fill="#2563EB"/>
  <text x="214" y="163" text-anchor="middle" font-family="monospace" font-size="10" font-weight="600" fill="#FFF">chmod +x</text>

  <!-- Step 2 -->
  <circle cx="214" cy="100" r="18" fill="#2563EB"/>
  <text x="214" y="106" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">2</text>
  <rect x="174" y="128" width="110" height="72" rx="10" fill="#DCFCE7" stroke="#22C55E" stroke-width="2" filter="url(#sh)"/>
  <text x="229" y="156" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#166534">hello.sh</text>
  <text x="229" y="178" text-anchor="middle" font-family="monospace" font-size="11" fill="#15803D">-rwxr-xr-x</text>
  <text x="229" y="192" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">executable</text>

  <path d="M284 164 L312 164" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#f)"/>
  <rect x="312" y="148" width="76" height="22" rx="11" fill="#7C3AED"/>
  <text x="350" y="163" text-anchor="middle" font-family="monospace" font-size="10" font-weight="600" fill="#FFF">./hello.sh</text>

  <!-- Step 3 -->
  <circle cx="350" cy="100" r="18" fill="#16A34A"/>
  <text x="350" y="106" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">3</text>
  <rect x="310" y="128" width="110" height="72" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="405" y="168" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Hello SOC</text>
  <text x="405" y="188" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">script output</text>

  <!-- rwx legend -->
  <rect x="520" y="108" width="320" height="100" rx="12" fill="#FFF" stroke="#E2E8F0" filter="url(#sh)"/>
  <text x="680" y="132" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#334155">Permission bits (rwx)</text>
  <text x="548" y="156" font-family="{FONT}" font-size="10" fill="#64748B">owner</text>
  <text x="620" y="156" font-family="{FONT}" font-size="10" fill="#64748B">group</text>
  <text x="692" y="156" font-family="{FONT}" font-size="10" fill="#64748B">other</text>
  <rect x="536" y="164" width="56" height="24" rx="4" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="564" y="180" text-anchor="middle" font-family="monospace" font-size="10" fill="#92400E">rw-</text>
  <rect x="600" y="164" width="56" height="24" rx="4" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="628" y="180" text-anchor="middle" font-family="monospace" font-size="10" fill="#92400E">r--</text>
  <rect x="664" y="164" width="56" height="24" rx="4" fill="#DCFCE7" stroke="#22C55E"/>
  <text x="692" y="180" text-anchor="middle" font-family="monospace" font-size="10" fill="#166534">r-x</text>
  <text x="680" y="198" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">+x adds execute for all three</text>
</svg>
""")


# ── 05 SetUID ────────────────────────────────────────────────────────────
write("05-setuid-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 280" role="img" aria-label="SetUID flow">
  <defs>
    {SHADOW}
    {mk("#475569", "u")}
  </defs>
  <rect width="880" height="280" fill="#F1F5F9"/>
  <text x="440" y="36" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">SetUID — Privilege Escalation Risk</text>
  <text x="440" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Program runs as the file owner, not who launched it</text>

  <rect x="48" y="88" width="180" height="110" rx="14" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="138" y="120" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">ec2-user</text>
  <text x="138" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">normal privilege</text>
  <text x="138" y="162" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">runs passwd</text>

  <path d="M228 143 L268 143" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#u)"/>
  <rect x="240" y="128" width="56" height="18" rx="9" fill="#FFF" stroke="#94A3B8"/>
  <text x="268" y="141" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">executes</text>

  <rect x="268" y="88" width="220" height="110" rx="14" fill="#FEE2E2" stroke="#EF4444" stroke-width="2" filter="url(#sh)"/>
  <text x="378" y="120" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#991B1B">/usr/bin/passwd</text>
  <text x="378" y="142" text-anchor="middle" font-family="monospace" font-size="12" fill="#7F1D1D">-rwsr-xr-x</text>
  <rect x="368" y="130" width="10" height="14" rx="2" fill="#DC2626" opacity="0.25"/>
  <text x="378" y="164" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#7F1D1D">s = SetUID bit (runs as root)</text>

  <path d="M488 143 L528 143" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#u)"/>
  <rect x="500" y="128" width="64" height="18" rx="9" fill="#FFF" stroke="#94A3B8"/>
  <text x="532" y="141" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">runs as</text>

  <rect x="528" y="88" width="180" height="110" rx="14" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" filter="url(#sh)"/>
  <text x="618" y="120" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">root</text>
  <text x="618" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">effective user</text>
  <text x="618" y="162" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">elevated privileges</text>

  <rect x="48" y="218" width="784" height="44" rx="10" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="440" y="238" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">Defender action: inventory SetUID binaries on every Linux host</text>
  <text x="440" y="254" text-anchor="middle" font-family="monospace" font-size="10" fill="#78350F">find / -perm -4000 -exec ls -l &#123;&#125; &#92;; 2&gt;/dev/null</text>
</svg>
""")


# ── 06 nginx ────────────────────────────────────────────────────────────
write("06-nginx-telemetry.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 260" role="img" aria-label="nginx telemetry">
  <defs>
    {SHADOW}
    {mk("#475569", "n")}
  </defs>
  <rect width="880" height="260" fill="#F1F5F9"/>
  <text x="440" y="36" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">HTTP Request to Telemetry</text>
  <text x="440" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Each web hit writes one line to access.log for future AI detection labs</text>

  <g filter="url(#sh)">
    <rect x="40" y="100" width="130" height="80" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  </g>
  <circle cx="105" cy="88" r="16" fill="#2563EB"/>
  <text x="105" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">1</text>
  <text x="105" y="132" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#1E40AF">Browser</text>
  <text x="105" y="152" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">GET /</text>

  <path d="M170 140 L208 140" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#n)"/>

  <g filter="url(#sh)">
    <rect x="208" y="100" width="130" height="80" rx="12" fill="#FFF7ED" stroke="#F59E0B" stroke-width="2"/>
  </g>
  <circle cx="273" cy="88" r="16" fill="#D97706"/>
  <text x="273" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">2</text>
  <text x="273" y="132" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#92400E">nginx</text>
  <text x="273" y="156" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#78350F">port 80</text>

  <path d="M338 140 L376 140" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#n)"/>

  <g filter="url(#sh)">
    <rect x="376" y="100" width="150" height="80" rx="12" fill="#F1F5F9" stroke="#64748B" stroke-width="2"/>
  </g>
  <circle cx="451" cy="88" r="16" fill="#64748B"/>
  <text x="451" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">3</text>
  <text x="451" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#334155">access.log</text>
  <text x="451" y="156" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">1 line per hit</text>

  <path d="M526 140 L564 140" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#n)"/>

  <g filter="url(#sh)">
    <rect x="564" y="100" width="150" height="80" rx="12" fill="#DCFCE7" stroke="#22C55E" stroke-width="2"/>
  </g>
  <circle cx="639" cy="88" r="16" fill="#16A34A"/>
  <text x="639" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">4</text>
  <text x="639" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#166534">Lab 1.2+</text>
  <text x="639" y="156" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">AI detection</text>

  <rect x="740" y="100" width="120" height="80" rx="10" fill="#FFF" stroke="#CBD5E1"/>
  <text x="800" y="124" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">Sample line</text>
  <text x="800" y="142" text-anchor="middle" font-family="monospace" font-size="8" fill="#64748B">GET / 200</text>
  <text x="800" y="156" text-anchor="middle" font-family="monospace" font-size="8" fill="#64748B">IP time agent</text>
</svg>
""")


# ── 00 Roadmap ────────────────────────────────────────────────────────
write("00-complete-roadmap.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 860" role="img" aria-label="Lab roadmap">
  <defs>
    {SHADOW}
    {mk("#475569", "dn")}
    {mk("#2563EB", "db")}
    {mk("#16A34A", "dg")}
    {mk("#D97706", "do")}
    {mk("#DC2626", "dr")}
  </defs>
  <rect width="800" height="860" fill="#F1F5F9"/>

  <rect x="24" y="24" width="752" height="812" rx="16" fill="#FFF" stroke="#E2E8F0" filter="url(#sh)"/>
  <text x="400" y="58" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="#0F172A">Lab 1.1 Roadmap</text>
  <text x="400" y="80" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">8 steps · us-east-1 · personal AWS</text>

  <circle cx="400" cy="108" r="24" fill="#16A34A"/>
  <text x="400" y="114" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">GO</text>
  <line x1="400" y1="132" x2="400" y2="152" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 1 -->
  <rect x="48" y="148" width="704" height="130" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
  <text x="68" y="174" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Phase 1 · AWS Setup</text>
  <g>
    <rect x="80" y="188" width="200" height="68" rx="10" fill="#FFF" stroke="#2563EB" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="104" cy="214" r="16" fill="#2563EB"/><text x="104" y="219" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">1</text>
    <text x="190" y="214" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Create SSH key</text>
    <text x="190" y="232" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">soc-lab-key.pem</text>
  </g>
  <line x1="280" y1="222" x2="308" y2="222" stroke="#2563EB" stroke-width="2.5" marker-end="url(#db)"/>
  <g>
    <rect x="308" y="188" width="200" height="68" rx="10" fill="#FFF" stroke="#2563EB" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="332" cy="214" r="16" fill="#2563EB"/><text x="332" y="219" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">2</text>
    <text x="418" y="214" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Launch EC2</text>
    <text x="418" y="232" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">ports 22, 80</text>
  </g>
  <line x1="508" y1="222" x2="536" y2="222" stroke="#2563EB" stroke-width="2.5" marker-end="url(#db)"/>
  <g>
    <rect x="536" y="188" width="200" height="68" rx="10" fill="#FFF" stroke="#2563EB" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="560" cy="214" r="16" fill="#2563EB"/><text x="560" y="219" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">3</text>
    <text x="646" y="222" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Get public IP</text>
  </g>
  <line x1="400" y1="278" x2="400" y2="296" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 2 -->
  <rect x="48" y="296" width="704" height="130" rx="12" fill="#ECFDF5" stroke="#16A34A" stroke-width="2"/>
  <text x="68" y="322" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">Phase 2 · Connect</text>
  <g>
    <rect x="210" y="336" width="200" height="68" rx="10" fill="#FFF" stroke="#16A34A" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="234" cy="362" r="16" fill="#16A34A"/><text x="234" y="367" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">4</text>
    <text x="320" y="370" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">SSH config</text>
  </g>
  <line x1="410" y1="370" x2="438" y2="370" stroke="#16A34A" stroke-width="2.5" marker-end="url(#dg)"/>
  <g>
    <rect x="438" y="336" width="200" height="68" rx="10" fill="#FFF" stroke="#16A34A" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="462" cy="362" r="16" fill="#16A34A"/><text x="462" y="367" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">5</text>
    <text x="548" y="370" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">Connect EC2</text>
  </g>
  <line x1="400" y1="426" x2="400" y2="444" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 3 -->
  <rect x="48" y="444" width="704" height="130" rx="12" fill="#fffbeb" stroke="#D97706" stroke-width="2"/>
  <text x="68" y="470" font-family="{FONT}" font-size="14" font-weight="700" fill="#92400E">Phase 3 · Linux</text>
  <g>
    <rect x="210" y="484" width="200" height="68" rx="10" fill="#FFF" stroke="#D97706" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="234" cy="510" r="16" fill="#D97706"/><text x="234" y="515" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">6</text>
    <text x="320" y="518" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">Scripts &amp; chmod</text>
  </g>
  <line x1="410" y1="518" x2="438" y2="518" stroke="#D97706" stroke-width="2.5" marker-end="url(#do)"/>
  <g>
    <rect x="438" y="484" width="200" height="68" rx="10" fill="#FFF" stroke="#D97706" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="462" cy="510" r="16" fill="#D97706"/><text x="462" y="515" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">7</text>
    <text x="548" y="518" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">SetUID find</text>
  </g>
  <line x1="400" y1="574" x2="400" y2="592" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 4 -->
  <rect x="48" y="592" width="704" height="130" rx="12" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="68" y="618" font-family="{FONT}" font-size="14" font-weight="700" fill="#991B1B">Phase 4 · Web</text>
  <g>
    <rect x="300" y="632" width="200" height="68" rx="10" fill="#FFF" stroke="#DC2626" stroke-width="1.5" filter="url(#sh)"/>
    <circle cx="324" cy="658" r="16" fill="#DC2626"/><text x="324" y="663" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFF">8</text>
    <text x="410" y="662" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#991B1B">nginx + access.log</text>
  </g>
  <line x1="400" y1="722" x2="400" y2="740" stroke="#16A34A" stroke-width="2.5" marker-end="url(#dg)"/>

  <rect x="320" y="740" width="160" height="48" rx="24" fill="#16A34A" filter="url(#sh)"/>
  <text x="400" y="770" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#FFF">Done</text>
</svg>
""")

print("Wrote 7 polished diagrams")
