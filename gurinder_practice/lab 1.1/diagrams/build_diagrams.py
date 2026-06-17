"""Regenerate lab 1.1 SVG diagrams — validated layout, no overlaps."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, Sans-serif"

SHADOW = """
    <filter id="sh" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.10"/>
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


def label(tx: int, ty: int, text: str, color: str) -> str:
    w = len(text) * 6 + 20
    return f"""
  <rect x="{tx - w // 2}" y="{ty - 11}" width="{w}" height="20" rx="10" fill="#FFF" stroke="{color}" stroke-width="1"/>
  <text x="{tx}" y="{ty + 4}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="{color}">{text}</text>"""


def arrow_path(d: str, color: str, mid: str) -> str:
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{mid})"/>'


# ── 01 Architecture ──────────────────────────────────────────────────────────
write("01-architecture.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 440" role="img" aria-label="Lab architecture">
  <defs>{SHADOW}{GRAD_AWS}{mk("#2563EB", "ssh")}{mk("#16A34A", "http")}</defs>
  <rect width="900" height="440" fill="#F8FAFC"/>
  <rect x="20" y="20" width="860" height="400" rx="14" fill="#FFF" stroke="#E2E8F0"/>

  <text x="450" y="52" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">Lab Architecture</text>
  <text x="450" y="72" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Your PC connects over the internet to EC2 in AWS</text>

  <!-- Arrows FIRST (behind boxes) -->
  {arrow_path("M248 268 L248 108 L360 108 L360 248", "#2563EB", "ssh")}
  {arrow_path("M248 282 L248 108 L585 108 L585 258", "#16A34A", "http")}
  {label(300, 100, "SSH", "#2563EB")}
  {label(480, 100, "HTTP", "#16A34A")}

  <!-- Internet -->
  <rect x="48" y="88" width="804" height="36" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="1.5"/>
  <text x="450" y="111" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#0369A1">Internet</text>

  <!-- Your PC -->
  <rect x="48" y="140" width="200" height="180" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="148" y="168" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Your PC</text>
  <text x="148" y="188" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">VS Code + browser</text>
  <text x="148" y="206" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">soc-lab-key.pem</text>
  <rect x="68" y="248" width="72" height="26" rx="6" fill="#2563EB"/>
  <text x="104" y="265" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">SSH :22</text>
  <rect x="148" y="248" width="72" height="26" rx="6" fill="#16A34A"/>
  <text x="184" y="265" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">HTTP :80</text>

  <!-- VPC -->
  <rect x="280" y="132" width="572" height="200" rx="12" fill="#FAFAFA" stroke="#94A3B8" stroke-width="2" stroke-dasharray="8 4"/>
  <text x="300" y="154" font-family="{FONT}" font-size="11" font-weight="700" fill="#64748B">VPC</text>

  <rect x="300" y="164" width="532" height="48" rx="8" fill="#FFF7ED" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="320" y="184" font-family="{FONT}" font-size="11" font-weight="700" fill="#92400E">Security Group</text>
  <rect x="430" y="176" width="72" height="22" rx="4" fill="#DC2626"/>
  <text x="466" y="191" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="700" fill="#FFF">:22</text>
  <rect x="510" y="176" width="72" height="22" rx="4" fill="#DC2626"/>
  <text x="546" y="191" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="700" fill="#FFF">:80</text>
  <text x="600" y="191" font-family="{FONT}" font-size="9" fill="#64748B">deny rest</text>

  <rect x="300" y="224" width="532" height="96" rx="10" fill="url(#aws)" stroke="#C2410C" stroke-width="2"/>
  <text x="320" y="248" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">EC2</text>
  <text x="320" y="264" font-family="{FONT}" font-size="10" fill="#FFF7ED">Amazon Linux 2023</text>
  <rect x="500" y="236" width="120" height="68" rx="8" fill="rgba(255,255,255,0.28)" stroke="#FFF"/>
  <text x="560" y="264" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#FFF">nginx :80</text>
  <text x="560" y="282" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#FFF7ED">web server</text>
  <rect x="640" y="236" width="170" height="68" rx="8" fill="rgba(255,255,255,0.28)" stroke="#FFF"/>
  <text x="725" y="264" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">access.log</text>
  <text x="725" y="282" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#FFF7ED">telemetry</text>

  <rect x="48" y="348" width="804" height="32" rx="8" fill="#F1F5F9" stroke="#E2E8F0"/>
  <text x="450" y="369" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Blue = SSH (port 22) · Green = HTTP (port 80) · Orange = AWS</text>
</svg>
""")


# ── 02 VPC ────────────────────────────────────────────────────────────────
write("02-vpc-networking.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 360" role="img" aria-label="VPC networking">
  <defs>{SHADOW}{mk("#334155", "in")}{mk("#16A34A", "ok")}</defs>
  <rect width="860" height="360" fill="#F8FAFC"/>
  <text x="430" y="38" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">VPC and Security Group</text>
  <text x="430" y="58" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Firewall rules filter traffic before it reaches your instance</text>

  {arrow_path("M148 180 L208 180", "#334155", "in")}
  {label(178, 168, "ingress", "#334155")}
  {arrow_path("M488 180 L528 180", "#16A34A", "ok")}

  <rect x="40" y="140" width="108" height="80" rx="10" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" filter="url(#sh)"/>
  <text x="94" y="172" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#0369A1">Internet</text>
  <text x="94" y="190" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">incoming</text>

  <rect x="208" y="100" width="612" height="220" rx="14" fill="#FFF" stroke="#64748B" stroke-width="2" stroke-dasharray="8 4" filter="url(#sh)"/>
  <text x="228" y="124" font-family="{FONT}" font-size="11" font-weight="700" fill="#475569">VPC · Subnet</text>

  <rect x="232" y="140" width="260" height="160" rx="12" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="362" y="168" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#991B1B">Security Group</text>
  <rect x="258" y="182" width="100" height="28" rx="6" fill="#DC2626"/>
  <text x="308" y="201" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">ALLOW :22</text>
  <rect x="368" y="182" width="100" height="28" rx="6" fill="#DC2626"/>
  <text x="418" y="201" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="#FFF">ALLOW :80</text>
  <rect x="258" y="222" width="210" height="28" rx="6" fill="#64748B"/>
  <text x="363" y="241" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">implicit deny</text>
  <text x="362" y="278" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Only listed ports pass</text>

  <rect x="528" y="150" width="260" height="140" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="658" y="190" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">EC2 Instance</text>
  <text x="658" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">Amazon Linux 2023</text>
  <text x="658" y="258" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Traffic must match SG rules</text>

  <rect x="40" y="328" width="780" height="24" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="430" y="344" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#1E40AF">Security Group = bouncer — only ports 22 and 80 enter</text>
</svg>
""")


# ── 03 SSH ────────────────────────────────────────────────────────────────
write("03-ssh-keys.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 280" role="img" aria-label="SSH key authentication">
  <defs>{SHADOW}{mk("#2563EB", "k")}</defs>
  <rect width="860" height="280" fill="#F8FAFC"/>
  <text x="430" y="36" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">SSH Key Authentication</text>
  <text x="430" y="56" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Private key on your PC matches public key on the server</text>

  {arrow_path("M268 150 L308 150", "#2563EB", "k")}
  {arrow_path("M552 150 L592 150", "#2563EB", "k")}

  <rect x="48" y="88" width="220" height="140" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="158" y="116" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Your PC</text>
  <rect x="72" y="130" width="172" height="44" rx="8" fill="#FFF" stroke="#93C5FD" stroke-width="1.5"/>
  <text x="158" y="158" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">soc-lab-key.pem</text>
  <text x="158" y="192" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Private key — keep secret</text>
  <text x="158" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#DC2626" font-weight="600">Never share this file</text>

  <rect x="308" y="108" width="244" height="84" rx="12" fill="#FFF" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="6 3"/>
  <text x="430" y="136" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#2563EB">Encrypted tunnel</text>
  <text x="430" y="156" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Port 22 · no password</text>
  <text x="430" y="176" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">VS Code Remote-SSH</text>

  <rect x="592" y="88" width="220" height="140" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" filter="url(#sh)"/>
  <text x="702" y="116" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#166534">EC2 Server</text>
  <rect x="616" y="130" width="172" height="44" rx="8" fill="#FFF" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="702" y="158" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">authorized_keys</text>
  <text x="702" y="192" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Public key from AWS</text>
  <text x="702" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Login: ec2-user</text>
</svg>
""")


# ── 04 chmod ──────────────────────────────────────────────────────────────
write("04-chmod-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 240" role="img" aria-label="chmod flow">
  <defs>{SHADOW}{mk("#475569", "f")}</defs>
  <rect width="860" height="240" fill="#F8FAFC"/>
  <text x="430" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">chmod +x — Make a Script Runnable</text>

  {arrow_path("M152 148 L168 148", "#475569", "f")}
  {arrow_path("M292 148 L308 148", "#475569", "f")}
  {arrow_path("M432 148 L448 148", "#475569", "f")}

  <rect x="42" y="118" width="110" height="60" rx="10" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2" filter="url(#sh)"/>
  <text x="97" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#92400E">hello.sh</text>
  <text x="97" y="162" text-anchor="middle" font-family="monospace" font-size="10" fill="#78350F">-rw-r--r--</text>

  <rect x="168" y="136" width="68" height="24" rx="12" fill="#2563EB"/>
  <text x="202" y="152" text-anchor="middle" font-family="monospace" font-size="10" font-weight="600" fill="#FFF">chmod +x</text>

  <rect x="236" y="118" width="110" height="60" rx="10" fill="#DCFCE7" stroke="#22C55E" stroke-width="2" filter="url(#sh)"/>
  <text x="291" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#166534">hello.sh</text>
  <text x="291" y="162" text-anchor="middle" font-family="monospace" font-size="10" fill="#15803D">-rwxr-xr-x</text>

  <rect x="308" y="136" width="72" height="24" rx="12" fill="#7C3AED"/>
  <text x="344" y="152" text-anchor="middle" font-family="monospace" font-size="10" font-weight="600" fill="#FFF">./hello.sh</text>

  <rect x="380" y="118" width="110" height="60" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="435" y="152" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Hello SOC</text>

  <rect x="520" y="100" width="300" height="88" rx="10" fill="#FFF" stroke="#E2E8F0" filter="url(#sh)"/>
  <text x="670" y="122" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#334155">Permission bits</text>
  <text x="548" y="142" font-family="{FONT}" font-size="10" fill="#64748B">r = read</text>
  <text x="548" y="158" font-family="{FONT}" font-size="10" fill="#64748B">w = write</text>
  <text x="548" y="174" font-family="{FONT}" font-size="10" fill="#64748B">x = execute</text>
  <text x="680" y="150" text-anchor="middle" font-family="monospace" font-size="10" fill="#92400E">-rw-  r--  r-x</text>
  <text x="680" y="172" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">+x adds run permission</text>
</svg>
""")


# ── 05 SetUID ─────────────────────────────────────────────────────────────
write("05-setuid-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 260" role="img" aria-label="SetUID flow">
  <defs>{SHADOW}{mk("#475569", "u")}</defs>
  <rect width="860" height="260" fill="#F8FAFC"/>
  <text x="430" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">SetUID — Privilege Escalation Risk</text>
  <text x="430" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Program runs as file owner, not who launched it</text>

  {arrow_path("M218 148 L252 148", "#475569", "u")}
  {arrow_path("M472 148 L506 148", "#475569", "u")}
  {label(235, 98, "runs", "#64748B")}
  {label(489, 98, "as root", "#64748B")}

  <rect x="48" y="108" width="170" height="80" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="133" y="136" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">ec2-user</text>
  <text x="133" y="158" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">runs passwd</text>
  <text x="133" y="174" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">normal user</text>

  <rect x="252" y="108" width="220" height="80" rx="12" fill="#FEE2E2" stroke="#EF4444" stroke-width="2" filter="url(#sh)"/>
  <text x="362" y="136" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#991B1B">/usr/bin/passwd</text>
  <text x="362" y="158" text-anchor="middle" font-family="monospace" font-size="11" fill="#7F1D1D">-rwsr-xr-x</text>
  <text x="362" y="176" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#7F1D1D">s = SetUID bit</text>

  <rect x="506" y="108" width="170" height="80" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" filter="url(#sh)"/>
  <text x="591" y="136" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#166534">root</text>
  <text x="591" y="158" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">elevated privileges</text>
  <text x="591" y="174" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">effective user</text>

  <rect x="48" y="206" width="764" height="40" rx="8" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="430" y="224" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#92400E">Defender: find SetUID binaries with find / -perm -4000</text>
  <text x="430" y="240" text-anchor="middle" font-family="monospace" font-size="9" fill="#78350F">find / -perm -4000 -exec ls -l &#123;&#125; &#92;; 2&gt;/dev/null</text>
</svg>
""")


# ── 06 nginx ──────────────────────────────────────────────────────────────
write("06-nginx-telemetry.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 240" role="img" aria-label="nginx telemetry">
  <defs>{SHADOW}{mk("#475569", "n")}</defs>
  <rect width="820" height="240" fill="#F8FAFC"/>
  <text x="410" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">HTTP Request to Telemetry</text>
  <text x="410" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Each web hit writes one line to access.log</text>

  {arrow_path("M158 138 L182 138", "#475569", "n")}
  {arrow_path("M298 138 L322 138", "#475569", "n")}
  {arrow_path("M448 138 L472 138", "#475569", "n")}

  <rect x="48" y="108" width="110" height="60" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" filter="url(#sh)"/>
  <text x="103" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#1E40AF">1 Browser</text>
  <text x="103" y="152" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">GET /</text>

  <rect x="182" y="108" width="116" height="60" rx="10" fill="#FFF7ED" stroke="#F59E0B" stroke-width="2" filter="url(#sh)"/>
  <text x="240" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#92400E">2 nginx</text>
  <text x="240" y="152" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#78350F">port 80</text>

  <rect x="322" y="108" width="126" height="60" rx="10" fill="#F1F5F9" stroke="#64748B" stroke-width="2" filter="url(#sh)"/>
  <text x="385" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#334155">3 access.log</text>
  <text x="385" y="152" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">1 line per hit</text>

  <rect x="472" y="108" width="126" height="60" rx="10" fill="#DCFCE7" stroke="#22C55E" stroke-width="2" filter="url(#sh)"/>
  <text x="535" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="#166534">4 Lab 1.2+</text>
  <text x="535" y="152" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">AI detection</text>

  <rect x="630" y="108" width="160" height="60" rx="10" fill="#FFF" stroke="#CBD5E1"/>
  <text x="710" y="128" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">Sample log line</text>
  <text x="710" y="146" text-anchor="middle" font-family="monospace" font-size="9" fill="#64748B">192.0.2.1 GET / 200</text>
  <text x="710" y="160" text-anchor="middle" font-family="monospace" font-size="9" fill="#64748B">IP · time · status</text>
</svg>
""")


# ── 00 Roadmap ────────────────────────────────────────────────────────────
write("00-complete-roadmap.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 820" role="img" aria-label="Lab roadmap">
  <defs>{SHADOW}{mk("#475569", "dn")}{mk("#2563EB", "db")}{mk("#16A34A", "dg")}{mk("#D97706", "do")}</defs>
  <rect width="780" height="820" fill="#F8FAFC"/>
  <rect x="20" y="20" width="740" height="780" rx="14" fill="#FFF" stroke="#E2E8F0" filter="url(#sh)"/>

  <text x="390" y="54" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="#0F172A">Lab 1.1 Roadmap</text>
  <text x="390" y="76" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">8 steps · us-east-1 · personal AWS</text>

  <circle cx="390" cy="102" r="22" fill="#16A34A"/>
  <text x="390" y="108" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">GO</text>
  <line x1="390" y1="124" x2="390" y2="142" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 1 -->
  <rect x="40" y="142" width="700" height="120" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
  <text x="58" y="166" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Phase 1 · AWS Setup</text>
  <rect x="68" y="178" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
  <circle cx="90" cy="207" r="14" fill="#2563EB"/><text x="90" y="212" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">1</text>
  <text x="168" y="204" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E3A8A">Create SSH key</text>
  <text x="168" y="220" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">soc-lab-key.pem</text>
  <line x1="258" y1="207" x2="278" y2="207" stroke="#2563EB" stroke-width="2.5" marker-end="url(#db)"/>
  <rect x="278" y="178" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
  <circle cx="300" cy="207" r="14" fill="#2563EB"/><text x="300" y="212" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">2</text>
  <text x="378" y="204" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E3A8A">Launch EC2</text>
  <text x="378" y="220" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">ports 22, 80</text>
  <line x1="468" y1="207" x2="488" y2="207" stroke="#2563EB" stroke-width="2.5" marker-end="url(#db)"/>
  <rect x="488" y="178" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
  <circle cx="510" cy="207" r="14" fill="#2563EB"/><text x="510" y="212" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">3</text>
  <text x="598" y="211" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E3A8A">Get public IP</text>
  <line x1="390" y1="262" x2="390" y2="278" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 2 -->
  <rect x="40" y="278" width="700" height="120" rx="10" fill="#ECFDF5" stroke="#16A34A" stroke-width="2"/>
  <text x="58" y="302" font-family="{FONT}" font-size="13" font-weight="700" fill="#166534">Phase 2 · Connect</text>
  <rect x="198" y="314" width="190" height="58" rx="8" fill="#FFF" stroke="#16A34A"/>
  <circle cx="220" cy="343" r="14" fill="#16A34A"/><text x="220" y="348" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">4</text>
  <text x="308" y="349" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#166534">SSH config</text>
  <line x1="388" y1="343" x2="408" y2="343" stroke="#16A34A" stroke-width="2.5" marker-end="url(#dg)"/>
  <rect x="408" y="314" width="190" height="58" rx="8" fill="#FFF" stroke="#16A34A"/>
  <circle cx="430" cy="343" r="14" fill="#16A34A"/><text x="430" y="348" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">5</text>
  <text x="518" y="349" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#166534">Connect EC2</text>
  <line x1="390" y1="398" x2="390" y2="414" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 3 -->
  <rect x="40" y="414" width="700" height="120" rx="10" fill="#FFFBEB" stroke="#D97706" stroke-width="2"/>
  <text x="58" y="438" font-family="{FONT}" font-size="13" font-weight="700" fill="#92400E">Phase 3 · Linux</text>
  <rect x="198" y="450" width="190" height="58" rx="8" fill="#FFF" stroke="#D97706"/>
  <circle cx="220" cy="479" r="14" fill="#D97706"/><text x="220" y="484" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">6</text>
  <text x="308" y="485" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">Scripts and chmod</text>
  <line x1="388" y1="479" x2="408" y2="479" stroke="#D97706" stroke-width="2.5" marker-end="url(#do)"/>
  <rect x="408" y="450" width="190" height="58" rx="8" fill="#FFF" stroke="#D97706"/>
  <circle cx="430" cy="479" r="14" fill="#D97706"/><text x="430" y="484" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">7</text>
  <text x="518" y="485" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">SetUID find</text>
  <line x1="390" y1="534" x2="390" y2="550" stroke="#475569" stroke-width="2.5" marker-end="url(#dn)"/>

  <!-- Phase 4 -->
  <rect x="40" y="550" width="700" height="120" rx="10" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="58" y="574" font-family="{FONT}" font-size="13" font-weight="700" fill="#991B1B">Phase 4 · Web</text>
  <rect x="278" y="586" width="224" height="58" rx="8" fill="#FFF" stroke="#DC2626"/>
  <circle cx="300" cy="615" r="14" fill="#DC2626"/><text x="300" y="620" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">8</text>
  <text x="404" y="619" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#991B1B">nginx + access.log</text>
  <line x1="390" y1="670" x2="390" y2="686" stroke="#16A34A" stroke-width="2.5" marker-end="url(#dg)"/>

  <rect x="310" y="686" width="160" height="44" rx="22" fill="#16A34A"/>
  <text x="390" y="714" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">Done</text>
</svg>
""")


def validate_all() -> list[str]:
    errors: list[str] = []
    hex_re = re.compile(r'(?:fill|stroke)="(#[^"]+)"')
    for path in sorted(OUT.glob("*.svg")):
        text = path.read_text(encoding="utf-8")
        try:
            ET.fromstring(text)
        except ET.ParseError as e:
            errors.append(f"{path.name}: invalid XML — {e}")
        for m in hex_re.finditer(text):
            color = m.group(1)
            if not re.fullmatch(r"#[0-9A-Fa-f]{3,8}", color):
                errors.append(f"{path.name}: invalid color {color}")
        if "FFGapic" in text or "call" in text.lower() and "%call" in text:
            errors.append(f"{path.name}: corrupted coordinate or color")
        if text.count("<svg") != 1:
            errors.append(f"{path.name}: expected one root svg")
    return errors


if __name__ == "__main__":
    print("Wrote 7 diagrams")
    issues = validate_all()
    if issues:
        print("VALIDATION FAILED:")
        for i in issues:
            print(f"  - {i}")
        raise SystemExit(1)
    print("All diagrams passed validation")
